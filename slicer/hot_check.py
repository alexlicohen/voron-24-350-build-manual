#!/usr/bin/env python3
"""Build and check the hot first-layer check project: five 30 x 30 x 0.2 mm squares.

The pre-B00 hot check (docs/manual/print/B00-calibration-and-jigs.md, "Before B00: belt and
hot-bed checks") prints one ASA layer at the corners and centre of the bed, at the 110 C bed
of the Voron plates, and calipers it. This writes that project so nobody lays it out by hand:

    slicer/checks/hot-first-layer.3mf

A second project is the same plate with the heat-then-off start G-code, for the A/B:

    slicer/checks/hot-first-layer-heat-off.3mf

Its start (`coreone-heat-off-start.gcode`) is the cold start with the stock probing block put
back and the heater switched off for the taps: idle temp while the bed settles, `M109 R170`,
the `M302 S155` retraction, `M104 S0`, `G29 P9`, `M104 S0` again, then the mesh, and the
deretraction before the purge. Homing and the chamber soak stay cold. The second `M104 S0`
matters once the Gen 2 nozzle wiper is fitted: in Buddy 6.8.1 the wiper's `G29 P9` heats the
nozzle itself and leaves a hold target (cleaning temp - 20) for the mesh. Neither the inis
nor the 20 plates carry this start; it lives in this one project until the bench picks it.

A third project is the brim-gap ladder, printed after the hot check has set Live Adjust Z:

    slicer/checks/brim-gap-ladder.3mf

Six 25 x 25 x 3 mm squares around the bed centre, each with a 5 mm brim (the plates' brim) and
its own brim separation: 0.10, 0.15, 0.20, 0.25, 0.30, 0.40 mm, set per object, so one print
compares them and nothing else differs. The check measures the gap PrusaSlicer actually emits
from the first layer: centreline distance from the external perimeter to the innermost brim
loop, minus one first-layer line width (half of each line), i.e. the air between the two
beads as sliced. On the bed the beads squash wider; that is what the print shows.

None is a plate of the run: they are not in plates.py, estimates.csv or any total.

Everything comes from `voron-coreone-asa.ini`, the same bundle B00-P1 was built from:
printer `Prusa CORE One HF0.4 nozzle` with the vendored cold-probe start G-code, filament
`Prusament ASA @COREONE HF0.4 - Voron black`, print `0.20mm STRUCTURAL @COREONE 0.4`. The
geometry and config go into the 3MF the way build_plates.py does it (its `run`, `inject_3mf`
and `read_footer` are reused, not copied), then the project is sliced with **no** `--load`
and the G-code is checked: one layer, five objects, bed 110 C, the cold start in place.

    python3 slicer/hot_check.py           # write all three 3MFs, slice them, check them
    python3 slicer/hot_check.py --check   # slice and check the committed 3MFs only

Re-run it (no flag) after `build_config.py` changes the start G-code in the inis
(`sync_start_gcode.py` then patches every plate); the cold project takes the ini's value when rebuilt.
"""
from __future__ import annotations

import re
import shutil
from collections import Counter
import struct
import sys
import tempfile
from pathlib import Path

from build_plates import INI, PRUSA, inject_3mf, read_footer, run
from geom import BED_X, BED_Y
from sync_start_gcode import ini_value, patch

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "checks" / "hot-first-layer.3mf"
OUT_HEAT_OFF = ROOT / "checks" / "hot-first-layer-heat-off.3mf"
OUT_BRIM = ROOT / "checks" / "brim-gap-ladder.3mf"
HEAT_OFF_START = ROOT / "coreone-heat-off-start.gcode"
INI_BLACK = INI["black"]
# The first-layer values now come from the ini (build_config, Alex 10-28/29): z_offset +0.08
# and layer_gcode's `M221 S95` on the first layer. History: satin, cold-probe start, Z 0 and
# +0.04 crested (the caliper read the crests, 0.28-0.30), -0.09 worse (0.5-0.6), +0.08 closed;
# the flow ladder at +0.08 picked 95 % (90 pinholed, 80 gapped).
Z_OFFSET = ini_value(INI_BLACK, "z_offset")
OUT_FLOW = ROOT / "checks" / "hot-first-layer-flow-ladder.gcode"
# square name -> M221 flow %; the centre is the control
FLOW_LADDER = {"centre": 100, "front-left": 95, "front-right": 90, "back-left": 85,
               "back-right": 80}

SIDE, HEIGHT = 30.0, 0.2
MARGIN = 15.0          # square edge to bed edge; the 3 mm skirt then sits 12 mm in
_LO_X, _HI_X = MARGIN + SIDE / 2, BED_X - MARGIN - SIDE / 2
_LO_Y, _HI_Y = MARGIN + SIDE / 2, BED_Y - MARGIN - SIDE / 2
# centre of each square, and its object name (PrusaSlicer Y+ is the back of the bed)
SQUARES = [
    ("front-left", _LO_X, _LO_Y),
    ("front-right", _HI_X, _LO_Y),
    ("back-left", _LO_X, _HI_Y),
    ("back-right", _HI_X, _HI_Y),
    ("centre", BED_X / 2, BED_Y / 2),
]

# brim-gap ladder: one square per brim separation, 3 x 2 around the bed centre
GAPS = (0.10, 0.15, 0.20, 0.25, 0.30, 0.40)
LADDER_SIDE, LADDER_HEIGHT, LADDER_BRIM, LADDER_PITCH = 25.0, 3.0, 5.0, 55.0
LADDER = [(g, BED_X / 2 + (i % 3 - 1) * LADDER_PITCH, BED_Y / 2 + (0.5 - i // 3) * LADDER_PITCH)
          for i, g in enumerate(GAPS)]       # back row 0.10-0.20, front row 0.25-0.40

# what the sliced G-code must say; each value is the ini's own, so a drift shows here
REQUIRED = ("printer_settings_id", "filament_settings_id", "print_settings_id",
            "first_layer_bed_temperature", "bed_temperature", "first_layer_height",
            "first_layer_temperature", "chamber_minimal_temperature")


def box_stl(path: Path, cx: float, cy: float, side: float = SIDE, height: float = HEIGHT) -> None:
    """A side x side x height box centred on (cx, cy), sitting on z = 0, binary STL."""
    h = side / 2
    x0, x1, y0, y1, z0, z1 = cx - h, cx + h, cy - h, cy + h, 0.0, height
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
         (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    faces = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4),
             (1, 2, 6), (1, 6, 5), (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7)]
    out = bytearray(b"\0" * 80) + struct.pack("<I", len(faces))
    for a, b, c in faces:
        out += struct.pack("<12fH", 0.0, 0.0, 0.0, *v[a], *v[b], *v[c], 0)
    path.write_bytes(bytes(out))


def build() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="hot-check-"))
    try:
        inputs, names = [], {}
        for i, (name, cx, cy) in enumerate(SQUARES, 1):
            fn = f"{i:02d}_square.stl"
            box_stl(tmp / fn, cx, cy)
            inputs.append(str(tmp / fn))
            names[fn] = f"square-{name}"
        OUT.parent.mkdir(parents=True, exist_ok=True)
        run([PRUSA, "--load", str(INI_BLACK), "--merge", "--dont-arrange",
             "--export-3mf", "-o", str(OUT), *inputs])
        inject_3mf(OUT, INI_BLACK, {}, names)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # same plate, one key different: the start G-code (escaped the way the inis hold it)
    shutil.copyfile(OUT, OUT_HEAT_OFF)
    patch(OUT_HEAT_OFF, "start_gcode",
          HEAT_OFF_START.read_text().rstrip("\n").replace("\n", "\\n"), False)
    for out in (OUT, OUT_HEAT_OFF):
        print(f"wrote {out.relative_to(ROOT.parent)}")


def gap_name(gap: float) -> str:
    return f"brim-gap-{gap:.2f}"


def build_brim() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="brim-check-"))
    try:
        inputs, names, per_object = [], {}, {}
        for i, (gap, cx, cy) in enumerate(LADDER, 1):
            fn = f"{i:02d}_ladder.stl"
            box_stl(tmp / fn, cx, cy, LADDER_SIDE, LADDER_HEIGHT)
            inputs.append(str(tmp / fn))
            names[fn] = gap_name(gap)
            per_object[fn] = {"brim_width": f"{LADDER_BRIM:g}", "brim_separation": f"{gap:g}"}
        run([PRUSA, "--load", str(INI_BLACK), "--merge", "--dont-arrange",
             "--export-3mf", "-o", str(OUT_BRIM), *inputs])
        inject_3mf(OUT_BRIM, INI_BLACK, per_object, names)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"wrote {OUT_BRIM.relative_to(ROOT.parent)}")


_MOVE = re.compile(r"^G[0-3] (.*)$")
_AXIS = re.compile(r"([XYE])(-?[\d.]+)")


def first_layer_paths(text: str) -> dict[str, list[tuple[float, float]]]:
    """Extruding-move end points of the first layer, keyed by `;TYPE:`."""
    first = text.split(";LAYER_CHANGE")[1]
    x = y = 0.0
    kind, out = "", {}
    for line in first.splitlines():
        if line.startswith(";TYPE:"):
            kind = line[6:].strip()
            continue
        m = _MOVE.match(line)
        if not m:
            continue
        ax = dict(_AXIS.findall(m.group(1).split(";")[0]))
        x, y = float(ax.get("X", x)), float(ax.get("Y", y))
        # an extruding move with no X/Y is a deretract wherever the last travel ended: skip it
        if float(ax.get("E", 0)) > 0 and ("X" in ax or "Y" in ax):
            out.setdefault(kind, []).append((x, y))
    return out


def measured_gaps(text: str, width: float) -> dict[float, float]:
    """Brim separation per ladder square: air between perimeter and brim beads, as sliced."""
    paths = first_layer_paths(text)
    near = lambda p: min(LADDER, key=lambda s: (p[0] - s[1]) ** 2 + (p[1] - s[2]) ** 2)
    gaps = {}
    for gap, cx, cy in LADDER:
        per = [max(abs(px - cx), abs(py - cy)) for px, py in paths.get("External perimeter", [])
               if near((px, py))[0] == gap]
        brim = [(px, py) for px, py in paths.get("Skirt/Brim", []) if near((px, py))[0] == gap
                and max(abs(px - cx), abs(py - cy)) < LADDER_SIDE / 2 + LADDER_BRIM + 1]
        if not per or not brim:
            continue
        h = sorted(per)[len(per) // 2]   # the perimeter loop's half-side (centreline)
        # the innermost brim loop: every vertex of a square loop with cut corners lies at the
        # same Chebyshev distance; a lone nearer point is the seam start, so need four hits
        dists = Counter(round(max(abs(px - cx), abs(py - cy)), 3) for px, py in brim)
        loop = [d for d, n in dists.items() if n >= 4]
        if loop:
            gaps[gap] = min(loop) - h - width
    return gaps


def check_brim() -> int:
    if not OUT_BRIM.exists():
        raise SystemExit(f"{OUT_BRIM} does not exist - run without --check to create it")
    tmp = Path(tempfile.mkdtemp(prefix="brim-check-"))
    try:
        gcode = tmp / "brim-gap-ladder.gcode"
        run([PRUSA, "--dont-arrange", "--binary-gcode=0",
             "--export-gcode", "-o", str(gcode), str(OUT_BRIM)])
        hours, grams, raw_time, cfg = read_footer(gcode)
        text = gcode.read_text(errors="replace")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    bad = []
    for key in REQUIRED:
        want = ini_value(INI_BLACK, key)
        if cfg.get(key, "").strip('"') != want.strip('"'):
            bad.append(f"{key} = {cfg.get(key)!r}, ini has {want!r}")
    bad += start_faults(text, heat_off=False)
    objects = sorted(set(re.findall(r"^M486 A(\S+)$", text, re.M)))
    if objects != sorted(gap_name(g) for g in GAPS):
        bad.append(f"labelled objects {objects}, expected one per gap")
    width = float(cfg.get("first_layer_extrusion_width", "0"))
    gaps = measured_gaps(text, width)
    for gap in GAPS:
        got = gaps.get(gap)
        if got is None:
            bad.append(f"{gap_name(gap)}: no brim or perimeter found on the first layer")
        elif abs(got - gap) > 0.05:
            bad.append(f"{gap_name(gap)}: sliced gap {got:.3f} mm, set {gap:.2f}")
    print(f"{OUT_BRIM.name}: {raw_time}, {grams:.1f} g, {text.count(';LAYER_CHANGE')} layers, "
          f"{len(objects)} objects, first-layer line {width:g} mm")
    print("  sliced air gap per square: "
          + ", ".join(f"{g:.2f} -> {gaps[g]:.3f}" for g in GAPS if g in gaps))
    for b in bad:
        print(f"  FAIL {b}")
    print("PASS" if not bad else "FAIL")
    return 1 if bad else 0


def nozzle_target_before(text: str, marker: str) -> str | None:
    """The last nozzle target (M104/M109 S or R value) set before the line starting `marker`."""
    m = re.search(rf"^{re.escape(marker)}", text, re.M)
    if not m:
        return None
    hits = re.findall(r"^M10[49] (?:T\d+ )?[SR](\d+)", text[:m.start()], re.M)
    return hits[-1] if hits else None


def start_faults(text: str, heat_off: bool) -> list[str]:
    head, _, tail = text.partition("G29 A ; activate mbl")
    if not heat_off:
        if "M104 S0 ; cold nozzle for MBL" not in head or re.search(r"^G29 P9", head, re.M) \
                or re.search(r"^M10[49] (?:T\d+ )?[SR](?!0\b)\d", head, re.M):
            return ["the cold-probe start G-code did not take: a nozzle target before the mesh"]
        return []
    bad = []
    # every loadcell tap (homing, cleaning, mesh) must start with the heater off
    for marker in ("G28", "G29 P9", "G29 P1"):
        if nozzle_target_before(head, marker) != "0":
            bad.append(f"heat-then-off start: the heater is not off before `{marker}`")
    if not re.search(r"^M109 R170\b", head, re.M):
        bad.append("heat-then-off start: no `M109 R170` before the taps")
    if not (re.search(r"^M302 S155\b", head, re.M) and re.search(r"^G1 E-2 F2400", head, re.M)):
        bad.append("heat-then-off start: the pre-probe retraction is missing")
    if not re.search(r"^G1 E2 F2400", tail.partition(";LAYER_CHANGE")[0], re.M):
        bad.append("heat-then-off start: the deretraction before the purge is missing")
    return bad


def check(out: Path = OUT) -> int:
    if not out.exists():
        raise SystemExit(f"{out} does not exist - run without --check to create it")
    tmp = Path(tempfile.mkdtemp(prefix="hot-check-"))
    try:
        gcode = tmp / "hot-first-layer.gcode"
        # deliberately no --load: the committed 3MF must carry its own config
        run([PRUSA, "--dont-arrange", "--binary-gcode=0",
             "--export-gcode", "-o", str(gcode), str(out)])
        hours, grams, raw_time, cfg = read_footer(gcode)
        text = gcode.read_text(errors="replace")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    bad = []
    for key in REQUIRED:
        want = ini_value(INI_BLACK, key)
        if cfg.get(key, "").strip('"') != want.strip('"'):
            bad.append(f"{key} = {cfg.get(key)!r}, ini has {want!r}")
    if cfg.get("first_layer_bed_temperature") != "110":
        bad.append("first-layer bed is not 110 C")
    if float(cfg.get("z_offset", "0")) != float(Z_OFFSET):
        bad.append(f"z_offset = {cfg.get('z_offset')!r}, expected {Z_OFFSET}")
    if out == OUT and not re.search(r"^M221 S95 ; first layer.*\n(?:(?!;LAYER_CHANGE).*\n)*;LAYER_CHANGE",
                                    text, re.M):
        bad.append("no `M221 S95` first-layer flow line before layer 1")
    first_z = re.search(r"^;Z:([\d.]+)$", text, re.M)
    want_z = float(ini_value(INI_BLACK, "first_layer_height")) + float(Z_OFFSET)
    if not first_z or abs(float(first_z.group(1)) - want_z) > 1e-6:
        bad.append(f"first layer at Z {first_z and first_z.group(1)}, expected {want_z:.2f}")
    bad += start_faults(text, heat_off=out == OUT_HEAT_OFF)
    layers = text.count(";LAYER_CHANGE")
    if layers != 1:
        bad.append(f"{layers} layers, expected 1")
    objects = sorted(set(re.findall(r"^M486 A(\S+)$", text, re.M)))
    if len(objects) != len(SQUARES):
        bad.append(f"{len(objects)} labelled objects, expected {len(SQUARES)}: {objects}")
    print(f"{out.name}: {raw_time}, {grams:.1f} g, {layers} layer, "
          f"{len(objects)} objects, bed {cfg.get('first_layer_bed_temperature')} C, "
          f"nozzle {cfg.get('first_layer_temperature')} C")
    for b in bad:
        print(f"  FAIL {b}")
    print("PASS" if not bad else "FAIL")
    return 1 if bad else 0


def _e_only(line: str) -> bool:
    """A retract or unretract: a G1 with an E word and no X/Y."""
    w = line.split(";")[0].split()
    return bool(w) and w[0] == "G1" and any(t[0] == "E" for t in w[1:]) \
        and not any(t[0] in "XY" for t in w[1:])


def flow_ladder_gcode(text: str) -> str:
    """Put each square at its own M221 flow. Retracts and unretracts run at 100 % so every
    square starts primed the same; the per-square flow is restored after each one."""
    ids = {int(m.group(1)): m.group(2).removeprefix("square-")
           for m in re.finditer(r"^M486 S(\d+)\nM486 A(\S+)$", text, re.M)}
    out, cur, body = [], 100, False
    for line in text.split("\n"):
        if line.startswith(";LAYER_CHANGE"):
            body = True
        m = re.match(r"^M486 S(-?\d+)$", line)
        if body and m:
            n = int(m.group(1))
            cur = 100 if n < 0 else FLOW_LADDER[ids[n]]
            out.append(line)
            out.append(f"M221 S{cur} ; flow ladder: {ids.get(n, 'between squares')}")
            continue
        if body and _e_only(line) and cur != 100:
            out += ["M221 S100", line, f"M221 S{cur}"]
            continue
        if re.match(r"^M486 A(\S+)$", line):
            name = line.split()[1].removeprefix("Asquare-")
            if name in FLOW_LADDER:
                line = f"M486 Asquare-{name}-{FLOW_LADDER[name]}pct"
        out.append(line)
    return "\n".join(out)


def build_flow_ladder() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="hot-check-"))
    try:
        gcode = tmp / "plain.gcode"
        run([PRUSA, "--dont-arrange", "--binary-gcode=0",
             "--export-gcode", "-o", str(gcode), str(OUT)])
        OUT_FLOW.write_text(flow_ladder_gcode(gcode.read_text(errors="replace")))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"wrote {OUT_FLOW.relative_to(ROOT.parent)}")


def check_flow_ladder() -> int:
    if not OUT_FLOW.exists():
        raise SystemExit(f"{OUT_FLOW} does not exist - run without --check to create it")
    text = OUT_FLOW.read_text()
    bad = start_faults(text, heat_off=False)
    first_z = re.search(r"^;Z:([\d.]+)$", text, re.M)
    want_z = float(ini_value(INI_BLACK, "first_layer_height")) + float(Z_OFFSET)
    if not first_z or abs(float(first_z.group(1)) - want_z) > 1e-6:
        bad.append(f"first layer at Z {first_z and first_z.group(1)}, expected {want_z:.2f}")
    # every extruding XY move inside square n runs at that square's flow; E-only moves at 100
    flow, seen, cur_sq = 100, {}, None
    names = {int(m.group(1)): m.group(2) for m in
             re.finditer(r"^M486 S(\d+)\nM486 Asquare-(\S+)-\d+pct$", text, re.M)}
    body = False
    for line in text.split("\n"):
        if line.startswith(";LAYER_CHANGE"):
            body = True
        if not body:
            continue
        if m := re.match(r"^M221 S(\d+)", line):
            flow = int(m.group(1))
        elif m := re.match(r"^M486 S(-?\d+)$", line):
            cur_sq = names.get(int(m.group(1)))
        elif line.startswith("G1") and " E" in line:
            if _e_only(line):
                if flow != 100:
                    bad.append(f"retract at {flow} %: {line}")
            elif cur_sq is not None:
                seen.setdefault(cur_sq, set()).add(flow)
    for name, pct in FLOW_LADDER.items():
        if seen.get(name) != {pct}:
            bad.append(f"square {name}: flows {sorted(seen.get(name, []))}, expected {pct}")
    print(f"{OUT_FLOW.name}: first layer Z {first_z and first_z.group(1)}, "
          + ", ".join(f"{n} {p} %" for n, p in FLOW_LADDER.items()))
    for b in bad:
        print(f"  FAIL {b}")
    print("PASS" if not bad else "FAIL")
    return 1 if bad else 0


def main() -> int:
    if "--check" not in sys.argv[1:]:
        build()
        build_flow_ladder()
        build_brim()
    return max(check(OUT), check(OUT_HEAT_OFF), check_flow_ladder(), check_brim())


if __name__ == "__main__":
    raise SystemExit(main())
