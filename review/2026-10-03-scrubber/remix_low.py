#!/usr/bin/env python3
"""Low-profile variant of jinetix's 10 mm-bed scrubber (Printables 796563, CC BY-NC-SA 4.0)
for an Omron-probe build. Run with venv-cq/bin/python from this folder.

  --lower L  drop the A1-wiper seat (and its two locating posts) of the brush bracket by L mm
  --trim T   cut T mm off the top of the 350 mm bucket (its walls stand +1.34 mm proud of the
             design sheet top; T = 2.0 puts them 0.66 mm below it)

Source geometry: src/10mm Bed.stp (solid order: Center Bucket, 350mm Bucket, Decontaminator,
300mm Bucket, Stop Bracket). Installed frame = print frame (base flat at z 20 / 14.5).
Writes stl/low/*.stl (print-oriented, centred) plus _MIRROR copies for the left-side fit.
"""
import argparse
from pathlib import Path

import cadquery as cq

HERE = Path(__file__).resolve().parent
NAMES = ["Center Bucket", "350mm Bucket", "Decontaminator", "300mm Bucket", "Stop Bracket"]
# A1 wiper footprint on the bracket, in the STEP's frame (from the author's assembly:
# wiper 37 x 8 at x 87.64..124.64, y 720.50..728.50, seated on z 37.77).
SEAT = dict(x0=87.40, x1=124.90, y0=720.30, y1=728.75, z_floor=37.77)


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0)).val()


def export(shape, name, mirror):
    bb = shape.BoundingBox()
    s = shape.translate(cq.Vector(-(bb.xmin + bb.xmax) / 2, -(bb.ymin + bb.ymax) / 2, -bb.zmin))
    out = HERE / "stl" / "low"
    out.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(s, str(out / f"{name}.stl"), tolerance=0.01, angularTolerance=0.1)
    if mirror:
        cq.exporters.export(s.mirror("YZ"), str(out / f"{name}_MIRROR.stl"), tolerance=0.01, angularTolerance=0.1)
    b2 = s.BoundingBox()
    print(f"{name}: {b2.xlen:.2f} x {b2.ylen:.2f} x {b2.zlen:.2f} mm, {s.Volume() / 1000:.2f} cm3")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lower", type=float, required=True)
    ap.add_argument("--trim", type=float, required=True)
    a = ap.parse_args()
    solids = dict(zip(NAMES, cq.importers.importStep(str(HERE / "src" / "10mm Bed.stp")).solids().vals()))

    d = solids["Decontaminator"]
    z0, top = SEAT["z_floor"], d.BoundingBox().zmax + 1
    region = box(SEAT["x0"], SEAT["x1"], SEAT["y0"], SEAT["y1"], z0 - a.lower, top)
    posts = d.intersect(box(SEAT["x0"], SEAT["x1"], SEAT["y0"], SEAT["y1"], z0, top))
    low = d.cut(region)
    if posts.Volume() > 1e-6:
        low = low.fuse(posts.translate(cq.Vector(0, 0, -a.lower)))
    export(low.clean(), f"brush_bracket_low{a.lower:g}", mirror=True)

    b = solids["350mm Bucket"]
    bb = b.BoundingBox()
    trimmed = b.intersect(box(bb.xmin - 1, bb.xmax + 1, bb.ymin - 1, bb.ymax + 1, bb.zmin - 1, bb.zmax - a.trim))
    export(trimmed.clean(), f"350mm_bucket_trim{a.trim:g}", mirror=True)


if __name__ == "__main__":
    main()
