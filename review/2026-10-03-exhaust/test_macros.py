#!/usr/bin/env python3
"""Offline checks for the chamber-exhaust add-on (Ch 14 Part H). Run from the repo root:

    .venv/bin/python review/2026-10-03-exhaust/test_macros.py

1. The Klipper block in Ch 14 Step 14.33 is byte-identical to exhaust.cfg (this folder).
2. Its macros render with Klipper's Jinja delimiters and a mock printer, and emit the
   expected commands for every material case (PLA, PETG, ASA with and without a soak).
3. PRINT_START (taken from Ch 12 Step 12.36's block, with Step 14.33's line inserted where the
   step says) sets the exhaust before homing and runs the Nevermore only for a filtered
   FILAMENT (or none given), and _EXHAUST never vents a filtered material; PRINT_END (LDO's
   stock macro, with both inserted lines) purges after TURN_OFF_HEATERS and starts the
   Nevermore scrub after M107; _NEVERMORE_SCRUB runs on only after a filtered print.
4. The real controller: Klipper's temperature_fan.py and temperature_combined.py at the commit
   Ch 13 pins (f0892d8), driven by a mock chamber_temp, behave as the step text says: ceiling 0
   is always off, ceiling 35 switches on at 37 and off at 33, ceiling 1 is flat out, and
   min_temp 0 survives the combined sensor's first reading. Fetched over the network into a temp
   dir; prints SKIP (and does not fail) when offline.
"""
from __future__ import annotations

import importlib.util
import re
import sys
import tempfile
import types
import urllib.request
from pathlib import Path

import jinja2

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
CH12 = REPO / "docs/manual/12-software.md"
CH14 = REPO / "docs/manual/14-calibration.md"
LDO_CFG = REPO / "review/2026-10-03-scrubber/src/leviathan-printer-rev-d-sbv2.cfg"
KLIPPER = "https://raw.githubusercontent.com/Klipper3d/klipper/f0892d8/klippy/extras/"

ok = True


def check(cond, msg):
    global ok
    print(("PASS " if cond else "FAIL ") + msg)
    ok &= bool(cond)


def step_block(md: Path, step: str) -> str:
    text = md.read_text()
    m = re.search(rf"^### Step {re.escape(step)} .*?(?=^### |^## )", text, re.S | re.M)
    if not m:
        raise SystemExit(f"Step {step} not found in {md.name}")
    return m.group(0)


def code_blocks(block: str) -> list[str]:
    return [m.group(1) for m in re.finditer(r"```(?:ini)?\n(.*?)```", block, re.S)]


# ---------------------------------------------------------------- 1. chapter == exhaust.cfg
s1433 = step_block(CH14, "14.33")
blocks = code_blocks(s1433)
cfg = (HERE / "exhaust.cfg").read_text()
check(blocks and blocks[0] == cfg, "Step 14.33's config block is byte-identical to exhaust.cfg")
start_line = next(l for b in blocks[1:] for l in b.splitlines() if "_EXHAUST " in l)
end_line = next(l for b in blocks[1:] for l in b.splitlines() if "_EXHAUST_PURGE" in l)

# ---------------------------------------------------------------- 2. macro rendering
sections = {m.group(1): m.group(2)
            for m in re.finditer(r"^\[([^\]]+)\]\n(.*?)(?=^\[|\Z)", cfg, re.S | re.M)}


def parse(body):
    vars_, gcode, ingc = {}, [], False
    for line in body.splitlines():
        if ingc:
            if line.startswith("    ") or not line.strip():
                gcode.append(line[4:])
                continue
            ingc = False
        if line.startswith("variable_"):
            k, v = line.split(":", 1)
            vars_[k[9:]] = eval(v.split("#")[0].strip())
        elif line.startswith("gcode:"):
            ingc = True
    return vars_, "\n".join(gcode)


ENV = jinja2.Environment("{%", "%}", "{", "}")


class Obj(dict):
    def __getattr__(self, k):  # missing key -> AttributeError, so Jinja falls back to Undefined
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k) from None


def wrap(o):
    return Obj({k: wrap(v) for k, v in o.items()}) if isinstance(o, dict) else o


said = []


def render(tpl, variables=None, params=None, printer=None):
    said.clear()
    ctx = dict(variables or {})
    ctx.update(params=wrap(params or {}), printer=wrap(printer or {}),
               action_respond_info=lambda m: said.append(m) or "")
    return [l.split(";")[0].strip() for l in ENV.from_string(tpl).render(**ctx).splitlines()
            if l.split(";")[0].strip()]


ex_vars, ex_tpl = parse(sections["gcode_macro _EXHAUST"])
_, purge_tpl = parse(sections["gcode_macro _EXHAUST_PURGE"])
SET = "SET_TEMPERATURE_FAN_TARGET TEMPERATURE_FAN=exhaust_fan TARGET="

for label, params, want in (
        ("PLA, Nominal 35, Minimal 0", {"CHAMBER": "0", "TARGET": "35", "FILTER": "0"}, 35.0),
        ("PETG, Nominal 40, Minimal 0", {"CHAMBER": "0", "TARGET": "40", "FILTER": "0"}, 40.0),
        ("PLA, vendor Nominal 20", {"CHAMBER": "0", "TARGET": "20", "FILTER": "0"}, 20.0),
        ("ASA, vendor 55 / 40", {"CHAMBER": "40", "TARGET": "55", "FILTER": "1"}, 0.0),
        ("ASA, Minimal 0 (timed soak), Nominal 55", {"CHAMBER": "0", "TARGET": "55", "FILTER": "1"}, 0.0),
        ("FLEX, filtered, Nominal 30, Minimal 0", {"CHAMBER": "0", "TARGET": "30", "FILTER": "1"}, 0.0),
        ("ceiling exactly hot_above", {"CHAMBER": "0", "TARGET": "45"}, 45.0),
        ("no FILTER param (old start line)", {"CHAMBER": "0", "TARGET": "35"}, 35.0),
        ("no params (hand-run PRINT_START)", {}, 0.0)):
    out = render(ex_tpl, ex_vars, params)
    sets = [l for l in out if l.startswith(SET)]
    check(out[0] == "UPDATE_DELAYED_GCODE ID=_EXHAUST_OFF DURATION=0" and len(sets) == 1
          and float(sets[0][len(SET):]) == want,
          f"_EXHAUST {label}: cancels a pending purge, then {sets[0] if sets else '(none)'}; said {said}")

for label, target, purge, want in (("after PLA", 35.0, 10, ["TARGET=1", "DURATION=600"]),
                                    ("after ASA", 0.0, 10, ["TARGET=0"]),
                                    ("purge_min 0", 35.0, 0, ["TARGET=0"])):
    out = render(purge_tpl, printer={"gcode_macro _EXHAUST": dict(ex_vars, purge_min=purge),
                                     "temperature_fan exhaust_fan": {"target": target}})
    joined = " | ".join(out)
    check(all(w in joined for w in want) and ("DURATION" in joined) == ("DURATION=600" in want),
          f"_EXHAUST_PURGE {label}: {joined}")

# ---------------------------------------------------------------- 3. PRINT_START / PRINT_END
b1236 = code_blocks(step_block(CH12, "12.36"))
ps = b1236[0]
nm_cfg = b1236[1]
nm_end_line = next(l for l in b1236[2].splitlines() if l.strip())
nm_sections = {m.group(1): m.group(2)
               for m in re.finditer(r"^\[([^\]]+)\]\n(.*?)(?=^\[|\Z)", nm_cfg, re.S | re.M)}
ps_lines = ps.splitlines()
anchor = next(i for i, l in enumerate(ps_lines) if l.strip() == "SET_GCODE_OFFSET Z=0")
ps_lines.insert(anchor + 1, start_line)
_, ps_tpl = parse("\n".join(ps_lines[1:]) + "\n")
NM_ON = "SET_FAN_SPEED FAN=nevermore SPEED=1"
NM_CANCEL = "UPDATE_DELAYED_GCODE ID=_NEVERMORE_OFF DURATION=0"
# The Step 13.41 / 14.35 start lines as the 2.9.6 CLI expands them (FILAMENT = filament_type).
for label, params, want_wait, want_filter in (
        ("PLA", {"BED": "60", "EXTRUDER": "230", "CHAMBER": "0", "EXHAUST": "35", "FILAMENT": "PLA"}, False, False),
        ("PETG", {"BED": "85", "EXTRUDER": "255", "CHAMBER": "0", "EXHAUST": "40", "FILAMENT": "PETG"}, False, False),
        ("ASA", {"BED": "110", "EXTRUDER": "260", "CHAMBER": "40", "EXHAUST": "55", "FILAMENT": "ASA"}, True, True),
        ("ABS", {"BED": "110", "EXTRUDER": "255", "CHAMBER": "0", "EXHAUST": "55", "FILAMENT": "ABS"}, False, True),
        ("PC", {"BED": "110", "EXTRUDER": "275", "CHAMBER": "0", "FILAMENT": "PC"}, False, True),
        ("FLEX", {"BED": "50", "EXTRUDER": "240", "CHAMBER": "0", "EXHAUST": "30", "FILAMENT": "FLEX"}, False, True),
        ("PVB", {"BED": "75", "EXTRUDER": "215", "CHAMBER": "0", "FILAMENT": "PVB"}, False, False),
        ("lower-case asa", {"BED": "110", "EXTRUDER": "260", "CHAMBER": "0", "FILAMENT": "asa"}, False, True),
        ("Ch 13 line, no EXHAUST", {"BED": "110", "EXTRUDER": "260", "CHAMBER": "0", "FILAMENT": "ASA"}, False, True),
        ("old line, no FILAMENT", {"BED": "110", "EXTRUDER": "260", "CHAMBER": "0"}, False, True),
        ("hand run, no params", {}, False, True)):
    out = render(ps_tpl, params=params)
    i_ex = next(i for i, l in enumerate(out) if l.startswith("_EXHAUST "))
    i_g28 = out.index("G28")
    waits = any(l.startswith("TEMPERATURE_WAIT SENSOR=\"temperature_sensor chamber_temp\"") for l in out)
    nm_on, nm_cancel = NM_ON in out, NM_CANCEL in out
    nm_ok = (nm_on == want_filter and nm_cancel == want_filter
             and (not nm_on or out.index(NM_CANCEL) < out.index(NM_ON) < out.index(f"M140 S{params.get('BED', '100')}.0")))
    ex_params = dict(re.findall(r"(\w+)=(\S+)", out[i_ex]))
    exhaust_out = render(ex_tpl, ex_vars, ex_params)
    ex_set = [l for l in exhaust_out if l.startswith(SET)][0]
    vented = float(ex_set[len(SET):]) > 0
    check(i_ex < i_g28 and waits == want_wait and nm_ok and ex_params.get("FILTER") == str(int(want_filter))
          and not (vented and want_filter),
          f"PRINT_START {label}: Nevermore {'on' if nm_on else 'off'}, `{out[i_ex]}` before G28, "
          f"chamber wait {'on' if waits else 'off'}; _EXHAUST -> `{ex_set}`")

ldo = LDO_CFG.read_text()
pe = re.search(r"^\[gcode_macro PRINT_END\]\n(.*?)(?=^\[)", ldo, re.S | re.M).group(1)
pe_lines = pe.splitlines()
anchor = next(i for i, l in enumerate(pe_lines) if l.strip() == "TURN_OFF_HEATERS")
pe_lines.insert(anchor + 1, end_line)
anchor = next(i for i, l in enumerate(pe_lines) if l.split(";")[0].strip() == "M107")
pe_lines.insert(anchor + 1, nm_end_line)
_, pe_tpl = parse("\n".join(pe_lines) + "\n")
toolhead = {"position": {"x": 175.0, "y": 175.0, "z": 20.0},
            "axis_maximum": {"x": 350.0, "y": 350.0, "z": 330.0}}
out = render(pe_tpl, printer={"toolhead": toolhead})
check(out.index("_EXHAUST_PURGE") == out.index("TURN_OFF_HEATERS") + 1
      and out.index("_NEVERMORE_SCRUB") == out.index("M107") + 1
      and out[-1].startswith("RESTORE_GCODE_STATE"),
      "PRINT_END: _EXHAUST_PURGE after TURN_OFF_HEATERS, _NEVERMORE_SCRUB after M107, inside the saved state")

nm_vars, nm_tpl = parse(nm_sections["gcode_macro _NEVERMORE_SCRUB"])
_, nm_off_tpl = parse(nm_sections["delayed_gcode _NEVERMORE_OFF"])
for label, speed, scrub, want in (("after a filtered print", 1.0, 10, "UPDATE_DELAYED_GCODE ID=_NEVERMORE_OFF DURATION=600"),
                                   ("after PLA, Nevermore off", 0.0, 10, "SET_FAN_SPEED FAN=nevermore SPEED=0"),
                                   ("scrub_min 0", 1.0, 0, "SET_FAN_SPEED FAN=nevermore SPEED=0")):
    out = render(nm_tpl, dict(nm_vars, scrub_min=scrub), printer={"fan_generic nevermore": {"speed": speed}})
    check(out == [want], f"_NEVERMORE_SCRUB {label}: {out}")
check(render(nm_off_tpl) == ["SET_FAN_SPEED FAN=nevermore SPEED=0"] and nm_vars.get("scrub_min") == 10,
      f"_NEVERMORE_OFF stops the Nevermore; scrub_min {nm_vars.get('scrub_min')}")

# ---------------------------------------------------------------- 4. the real controller
tmp = Path(tempfile.mkdtemp(prefix="klipper-tf-"))
try:
    for name in ("temperature_fan.py", "temperature_combined.py"):
        (tmp / name).write_bytes(urllib.request.urlopen(KLIPPER + name, timeout=20).read())
except Exception as e:  # noqa: BLE001
    print(f"SKIP controller simulation: cannot fetch Klipper f0892d8 ({e})")
    sys.exit(0 if ok else 1)

pkg = types.ModuleType("kx")
pkg.__path__ = [str(tmp)]
sys.modules["kx"] = pkg
fanmod = types.ModuleType("kx.fan")


class Fan:
    def __init__(self, config, default_shutdown_speed=0.):
        self.shutdown = config.getfloat("shutdown_speed", default_shutdown_speed)
        self.speeds = []

    def set_speed(self, value, print_time=None):
        self.speeds.append(value)

    def get_status(self, eventtime):
        return {"speed": self.speeds[-1] if self.speeds else 0.}


fanmod.Fan = Fan
sys.modules["kx.fan"] = fanmod


def load(name):
    spec = importlib.util.spec_from_file_location(f"kx.{name}", tmp / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[f"kx.{name}"] = mod
    spec.loader.exec_module(mod)
    return mod


tf_mod, tc_mod = load("temperature_fan"), load("temperature_combined")
raw = {}
for line in sections["temperature_fan exhaust_fan"].splitlines():
    if ":" in line and not line.startswith("#"):
        k, v = line.split(":", 1)
        raw[k.strip()] = v.split("#")[0].strip()


class Shutdown(Exception):
    pass


class Config:
    def __init__(self, printer, values):
        self.printer, self.values = printer, values

    def get_name(self):
        return "temperature_fan exhaust_fan"

    def get_printer(self):
        return self.printer

    def get(self, k, default=None):
        return self.values.get(k, default)

    def getfloat(self, k, default=None, minval=None, maxval=None, above=None, below=None):
        v = float(self.values[k]) if k in self.values else default
        if v is None:
            raise KeyError(k)
        assert minval is None or v >= minval, (k, v, minval)
        assert maxval is None or v <= maxval, (k, v, maxval)
        assert above is None or v > above, (k, v, above)
        return v

    def getlist(self, k):
        return [s.strip() for s in self.values[k].split(",")]

    def getchoice(self, k, choices, default=None):
        return choices[self.values.get(k, default)]


def build(values, chamber):
    handlers, objects = {}, {}

    class Reactor:
        def register_timer(self, cb):
            return cb

        def update_timer(self, t, when):
            pass

        def monotonic(self):
            return clock[0]

    class Heaters:
        def setup_sensor(self, config):
            return tc_mod.PrinterSensorCombined(config)

        def register_sensor(self, config, obj, gcode_id=None):
            pass

    class Printer:
        def get_reactor(self):
            return reactor

        def load_object(self, config, name):
            return heaters

        def lookup_object(self, name):
            return objects[name]

        def add_object(self, name, obj):
            objects[name] = obj

        def register_event_handler(self, ev, cb):
            handlers.setdefault(ev, []).append(cb)

        def invoke_shutdown(self, msg):
            raise Shutdown(msg)

        def command_error(self, msg):
            return Exception(msg)

    reactor, heaters, printer = Reactor(), Heaters(), Printer()
    objects["gcode"] = types.SimpleNamespace(register_mux_command=lambda *a, **k: None)
    objects["mcu"] = types.SimpleNamespace(estimated_print_time=lambda t: t)
    objects["temperature_sensor chamber_temp"] = types.SimpleNamespace(
        get_status=lambda e: {"temperature": chamber[0]})
    tf = tf_mod.TemperatureFan(Config(printer, values))
    for cb in handlers.get("klippy:connect", []):
        cb()
    return tf, objects["temperature_combined exhaust_fan"]


class Gcmd:
    def __init__(self, **kw):
        self.kw = kw

    def get_float(self, k, default):
        return float(self.kw.get(k, default))


clock = [0.0]


def run(tf, comb, chamber, trace):
    """Feed a temperature trace; return the fan speed after each reading."""
    out = []
    for t in trace:
        chamber[0] = t
        clock[0] += 1.0
        comb._temperature_update_event(clock[0])
        out.append(tf.fan.speeds[-1] if tf.fan.speeds else 0.)
    return out


chamber = [0.0]  # chamber_temp has not reported yet
try:
    tf, comb = build(raw, chamber)
    run(tf, comb, chamber, [0.0])
    check(True, "min_temp 0: the combined sensor's first, empty reading (0.0) does not shut Klipper down")
except Shutdown as e:
    check(False, f"min_temp 0 shut down at start: {e}")
try:
    tf5, comb5 = build(dict(raw, min_temp="5", target_temp="5"), [0.0])
    run(tf5, comb5, [0.0], [0.0])
    print("NOTE min_temp 5 did not shut down at start")
except Shutdown:
    print("     (min_temp 5 would shut Klipper down on that first reading: why the block keeps 0)")

tf, comb = build(raw, chamber)
check(tf.fan.shutdown == 0.0 and tf.target_temp == 0.0,
      f"config: shutdown_speed {tf.fan.shutdown}, boot ceiling {tf.target_temp}")
sp = run(tf, comb, chamber, [22, 30, 45, 60, 40])
check(max(sp) == 0.0, f"ceiling 0 (boot, ASA): fan off at 22-60 C, speeds {sp}")

tf.cmd_SET_TEMPERATURE_FAN_TARGET(Gcmd(TARGET=35))
trace = [30, 34, 36, 36.9, 37.0, 38, 36, 34, 33.1, 33.0, 32, 35, 36.9, 37.5]
sp = run(tf, comb, chamber, trace)
on_at = trace[sp.index(1.0)]
off_at = next(trace[i] for i in range(sp.index(1.0), len(sp)) if sp[i] == 0.0)
check(on_at == 37.0 and off_at == 33.0 and sp[-1] == 1.0,
      f"ceiling 35: on at {on_at}, off at {off_at}, back on above 37 ({list(zip(trace, sp))})")

tf.cmd_SET_TEMPERATURE_FAN_TARGET(Gcmd(TARGET=1))
sp = run(tf, comb, chamber, [30, 25, 22])
check(sp == [1.0, 1.0, 1.0], f"ceiling 1 (purge): flat out at 22-30 C, speeds {sp}")
tf.cmd_SET_TEMPERATURE_FAN_TARGET(Gcmd(TARGET=0))
sp = run(tf, comb, chamber, [30, 50])
check(sp == [0.0, 0.0], f"ceiling 0 after a purge: off at once, speeds {sp}")

sys.exit(0 if ok else 1)
