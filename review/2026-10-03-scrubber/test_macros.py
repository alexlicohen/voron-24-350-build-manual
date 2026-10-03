#!/usr/bin/env python3
"""Render scrubber.cfg's macros the way Klipper does (jinja2, '{%'/'%}' and '{'/'}'),
with a mock printer, and check the G-code they emit. Run: ../../.venv/bin/python test_macros.py"""
import re, sys, jinja2
from pathlib import Path

txt = Path(__file__).with_name("scrubber.cfg").read_text()
sections = {}
for m in re.finditer(r"^\[([^\]]+)\]\n(.*?)(?=^\[|\Z)", txt, re.S | re.M):
    sections[m.group(1)] = m.group(2)

def parse(body):
    vars_, gcode, ingc = {}, [], False
    for line in body.splitlines():
        if ingc:
            if line.startswith("    ") or not line.strip():
                gcode.append(line[4:]); continue
            ingc = False
        if line.startswith("variable_"):
            k, v = line.split(":", 1); vars_[k[9:]] = eval(v.split("#")[0].strip())
        elif line.startswith("gcode:"):
            ingc = True
    return vars_, "\n".join(gcode)

env = jinja2.Environment("{%", "%}", "{", "}")
class Err(Exception): pass
def raise_error(msg): raise Err(msg)

def render(name, scrub_vars, ymax=355.0, homed="xyz", z=10.0):
    _, tpl = parse(sections[f"gcode_macro {name}"])
    printer = {"gcode_macro _SCRUB": scrub_vars,
               "toolhead": {"axis_maximum": {"y": ymax}, "homed_axes": homed, "position": {"z": z}}}
    class Obj(dict):
        __getattr__ = dict.__getitem__
    def wrap(o): return Obj({k: wrap(v) for k, v in o.items()}) if isinstance(o, dict) else o
    return env.from_string(tpl).render(printer=wrap(printer), action_raise_error=raise_error)

defaults, _ = parse(sections["gcode_macro _SCRUB"])
ok = True
def check(cond, msg):
    global ok
    print(("PASS " if cond else "FAIL ") + msg); ok &= bool(cond)

# 1. placeholders refuse to run
try:
    render("NOZZLE_PARK_BUCKET", dict(defaults)); check(False, "placeholders refused")
except Err as e: check("not measured" in str(e), f"placeholders refused ({e})")

# 2. unhomed refuses
meas = dict(defaults, brush_x_min=52.0, brush_x_max=87.0, edge_y=350.5, z_scrub=-0.45)
try:
    render("NOZZLE_PARK_BUCKET", meas, homed="xy"); check(False, "unhomed refused")
except Err as e: check("home" in str(e), f"unhomed refused ({e})")

def moves(g):
    pos, out = {}, []
    for line in g.splitlines():
        line = line.split(";")[0].strip()
        if not line: continue
        w = line.split(); cmd = w[0]
        args = {a[0]: float(a[1:]) for a in w[1:] if a[0] in "XYZIJF"}
        out.append((cmd, args))
    return out

# 3. overtravel cases: Y max - edge = O
for O in (6.5, 5.5, 4.5, 4.0, 3.5, 2.8):
    m = dict(meas, edge_y=355.0 - O)
    try:
        g = render("NOZZLE_CLEAN", m, ymax=355.0)
    except Err as e:
        check(O < 3.5 + 1e-9, f"O={O}: refused ({e})"); continue
    mv = moves(g)
    ys = [a["Y"] for c, a in mv if "Y" in a]
    circ = [(a, c) for c, a in mv if c in ("G2", "G3")]
    r = circ[0][0]["I"]
    cy = circ[0][0]["Y"]
    xs = [a["X"] for c, a in mv if c in ("G2", "G3")]
    lowz = [a["Z"] for c, a in mv if "Z" in a]
    check(cy + r <= 355.0 - 0.5 + 1e-6 and cy - r >= m["edge_y"] + 1.5 - 1e-6,
          f"O={O}: r={r:.2f} cy-edge={cy - m['edge_y']:.2f}, circle Y {cy - r - m['edge_y']:.2f}..{cy + r - m['edge_y']:.2f} past the edge")
    check(min(xs) >= m["brush_x_min"] + 0.5 - 1e-6 and max(xs) + 2 * r <= m["brush_x_max"] - 0.5 + 1e-6,
          f"O={O}: circles span X {min(xs):.2f}..{max(xs) + 2 * r:.2f} inside brush {m['brush_x_min']}..{m['brush_x_max']}")
    first_z = next(i for i, (c, a) in enumerate(mv) if "Z" in a and a["Z"] == m["z_scrub"])
    check(first_z > 0 and all("X" not in a and "Y" not in a for c, a in mv[first_z:first_z + 1]),
          f"O={O}: Z drops to {m['z_scrub']} on its own line")
    check(lowz[-1] == m["park_z"], f"O={O}: ends lifted to Z{lowz[-1]}")

# 4. park macro: lifts before XY, never lowers before XY
g = moves(render("NOZZLE_PARK_BUCKET", meas, z=0.2))
check(g[1][1].get("Z") == 5.0 and "X" not in g[1][1] and "X" in g[2][1], f"park: lift first ({g[1][1]}), then XY ({g[2][1]})")
check(g[2][1]["X"] == meas["brush_x_min"] - 10, f"park: X = brush_x_min - 10 = {g[2][1]['X']}")
sys.exit(0 if ok else 1)
