#!/usr/bin/env python3
"""Build and check the hot first-layer check project: five 30 x 30 x 0.2 mm squares.

The pre-B00 hot check (docs/manual/print/B00-calibration-and-jigs.md, "Before B00: belt and
hot-bed checks") prints one ASA layer at the corners and centre of the bed, at the 110 C bed
of the Voron plates, and calipers it. This writes that project so nobody lays it out by hand:

    slicer/checks/hot-first-layer.3mf

It is not a plate of the run: it is not in plates.py, estimates.csv or any total.

Everything comes from `voron-coreone-asa.ini`, the same bundle B00-P1 was built from:
printer `Prusa CORE One HF0.4 nozzle` with the vendored cold-probe start G-code, filament
`Prusament ASA @COREONE HF0.4 - Voron black`, print `0.20mm STRUCTURAL @COREONE 0.4`. The
geometry and config go into the 3MF the way build_plates.py does it (its `run`, `inject_3mf`
and `read_footer` are reused, not copied), then the project is sliced with **no** `--load`
and the G-code is checked: one layer, five objects, bed 110 C, the cold start in place.

    python3 slicer/hot_check.py           # write the 3MF, slice it, check it
    python3 slicer/hot_check.py --check   # slice and check the committed 3MF only

Re-run it (no flag) after `sync_start_gcode.py` changes the start G-code in the inis: that
script patches the 22 plates only, and this project takes the ini's value when rebuilt.
"""
from __future__ import annotations

import re
import shutil
import struct
import sys
import tempfile
from pathlib import Path

from build_plates import INI, PRUSA, inject_3mf, read_footer, run
from geom import BED_X, BED_Y
from sync_start_gcode import ini_value

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "checks" / "hot-first-layer.3mf"
INI_BLACK = INI["black"]

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

# what the sliced G-code must say; each value is the ini's own, so a drift shows here
REQUIRED = ("printer_settings_id", "filament_settings_id", "print_settings_id",
            "first_layer_bed_temperature", "bed_temperature", "first_layer_height",
            "first_layer_temperature", "chamber_minimal_temperature")


def box_stl(path: Path, cx: float, cy: float) -> None:
    """A SIDE x SIDE x HEIGHT box centred on (cx, cy), sitting on z = 0, binary STL."""
    h = SIDE / 2
    x0, x1, y0, y1, z0, z1 = cx - h, cx + h, cy - h, cy + h, 0.0, HEIGHT
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
    print(f"wrote {OUT.relative_to(ROOT.parent)}")


def check() -> int:
    if not OUT.exists():
        raise SystemExit(f"{OUT} does not exist - run without --check to create it")
    tmp = Path(tempfile.mkdtemp(prefix="hot-check-"))
    try:
        gcode = tmp / "hot-first-layer.gcode"
        # deliberately no --load: the committed 3MF must carry its own config
        run([PRUSA, "--dont-arrange", "--binary-gcode=0",
             "--export-gcode", "-o", str(gcode), str(OUT)])
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
    head, _, _ = text.partition("G29 A ; activate mbl")
    if "M104 S0 ; cold nozzle for MBL" not in head or re.search(r"^G29 P9", head, re.M) \
            or re.search(r"^M10[49] (?:T\d+ )?[SR](?!0\b)\d", head, re.M):
        bad.append("the cold-probe start G-code did not take: a nozzle target before the mesh")
    layers = text.count(";LAYER_CHANGE")
    if layers != 1:
        bad.append(f"{layers} layers, expected 1")
    objects = sorted(set(re.findall(r"^M486 A(\S+)$", text, re.M)))
    if len(objects) != len(SQUARES):
        bad.append(f"{len(objects)} labelled objects, expected {len(SQUARES)}: {objects}")
    print(f"hot-first-layer.3mf: {raw_time}, {grams:.1f} g, {layers} layer, "
          f"{len(objects)} objects, bed {cfg.get('first_layer_bed_temperature')} C, "
          f"nozzle {cfg.get('first_layer_temperature')} C")
    for b in bad:
        print(f"  FAIL {b}")
    print("PASS" if not bad else "FAIL")
    return 1 if bad else 0


def main() -> int:
    if "--check" not in sys.argv[1:]:
        build()
    return check()


if __name__ == "__main__":
    raise SystemExit(main())
