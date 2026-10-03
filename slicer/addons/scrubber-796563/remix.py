#!/usr/bin/env python3
"""The one generator of the scrubber add-on's printed files (Ch 13 Part L, Step 13.47).

Source: jinetix, Printables 796563 (CC BY-NC-SA 4.0), `source/10mm Bed.stp`. Its solids, in file
order: Center Bucket, 350mm Bucket, Decontaminator (the brush bracket), 300mm Bucket, Stop Bracket.
The STEP is drawn installed: bed-extrusion top at z 20, plate rear edge at y 720.5, which is also
the print orientation (bases flat). Everything here is mirrored for the LEFT bed extrusion.

    venv-cq/bin/python slicer/addons/scrubber-796563/remix.py --H 20.4 --w 3.86 --d 0.9 --G 21.3 --O 4.6
        decide from the Part L measurements; write the chosen STLs to measured/ (gitignored)
    venv-cq/bin/python slicer/addons/scrubber-796563/remix.py --defaults
        regenerate the committed default set from NOMINAL (the expected numbers, not measured)

Measurements (mm), all from Ch 13 Part L:
    H  flex-plate top above the bed-extrusion top, behind the plate (Step 13.45, caliper depth)
    w  A1 wiper height, base underside to bristle tips (Step 13.45, caliper)
    d  Omron face above the nozzle tip (Step 13.46, nozzle at Z10 over the plate)
    G  Omron face above the left bed-extrusion top at Z0 (Step 13.46); defaults to H + d
    O  nozzle reach past the plate's rear edge at the brush X (Step 13.46); macro only

Decision (heights above the bed-extrusion top; m = 0.3 margin, first layer at Z 0.2, scrub 0.5 mm
into the bristles). Constants are read from the STEP and asserted:
    S 17.77  wiper-seat floor          F 18.85  bracket top: flick path and pocket rim
    K 20.47  sheet-stop SHCS head top  B 21.39  bucket wall top
    L  (seat lowering)  >= S + w + 0.1 - G          Omron over the wiper while printing the rear rows
                        <= w - 1.88                 nozzle at scrub height clears F by 0.3
    T  (bucket trim)    >= B + 0.1 - G              Omron over the bucket walls while printing
                        >= B - S + 0.8 + L - w - d  Omron over the bucket walls while scrubbing
    sheet-stop screws only if G >= K + 0.1 and H <= 21.0 (head must rise past the flex plate)
    no-go if O < 3.5 or G < 19.75 (no L satisfies both L rows)
L and T round up to 0.5 mm (0 = stock); the measured layout rows (edge, room, collar) are the
gate-calc fence's in Step 13.47.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEP = HERE / "source" / "10mm Bed.stp"
NAMES = ["Center Bucket", "350mm Bucket", "Decontaminator", "300mm Bucket", "Stop Bracket"]
EXT = 20.0                                   # bed-extrusion top in the STEP frame
SEAT = dict(x0=87.40, x1=124.90, y0=720.30, y1=728.75, z_floor=37.77)   # A1 wiper footprint
S, F, K, B = 17.77, 18.85, 20.47, 21.39
M = 0.3
NOMINAL = dict(H=20.05, w=3.85, d=0.6, O=4.5)   # author's LDO 10 mm stack, official wiper, d at its floor


def ceil_step(x: float, step: float = 0.5) -> float:
    return max(0.0, math.ceil(round(x / step, 6)) * step)


def decide(H: float, w: float, d: float, G: float | None, O: float) -> dict:
    G = H + d if G is None else G
    rows, nogo = [], []
    if abs(G - (H + d)) > 0.3:
        nogo.append(f"G {G:.2f} and H + d {H + d:.2f} disagree by more than 0.3: re-measure H, d and G")
    if O < 3.5:
        nogo.append(f"O {O:.2f} < 3.5: the nozzle cannot reach the brush")
    if G < 19.75:
        nogo.append(f"G {G:.2f} < 19.75: no wiper height clears the Omron and the bracket top together")
    l_min, l_max = S + w + 0.1 - G, w - 1.88
    L = ceil_step(l_min)
    if L > l_max:
        L = max(0.0, math.ceil(round(l_min * 10, 6)) / 10)     # 0.1 steps when the 0.5 grid overshoots
    if L > l_max + 1e-9:
        nogo.append(f"L needs {l_min:.2f} but the bracket top allows {l_max:.2f}")
    t_min = max(B + 0.1 - G, B - S + 0.8 + L - w - d)
    T = ceil_step(t_min)
    if T > 3.0:
        nogo.append(f"T needs {t_min:.2f}, more than the 3.0 the bucket can lose")
    stops = G >= K + 0.1 and H <= 21.0
    r = min(2.0, (O - 2.0) / 2.0)
    return dict(H=H, w=w, d=d, G=G, O=O, L=L, T=T, l_min=l_min, l_max=l_max, t_min=t_min,
                stops=stops, r=r, nogo=nogo, rows=rows,
                wiper_top=S - L + w, bucket_h=26.89 - T, z_scrub=S - L + w - 0.5 - H)


def report(x: dict) -> str:
    out = [f"inputs  H {x['H']:.2f}  w {x['w']:.2f}  d {x['d']:.2f}  G {x['G']:.2f}  O {x['O']:.2f}"]
    out += x["rows"]
    if x["nogo"]:
        out += [f"NO-GO  {n}" for n in x["nogo"]] + ["Leave the add-on off. Nothing to print."]
        return "\n".join(out)
    out += [
        f"L  {x['L']:.1f}  (needs >= {x['l_min']:.2f}, allowed <= {x['l_max']:.2f})"
        + ("  = stock seat" if x["L"] == 0 else ""),
        f"T  {x['T']:.1f}  (needs >= {x['t_min']:.2f})" + ("  = stock bucket" if x["T"] == 0 else ""),
        "sheet-stop screws: " + ("FIT both" if x["stops"] else "LEAVE BOTH OUT (Omron or flex-plate height)"),
        f"macro scrub radius {x['r']:.2f} mm; expected z_scrub {x['z_scrub']:+.2f} (Step 13.51 measures it)",
        f"inspect: bracket base to bristle tips {x['wiper_top']:.2f} ±0.2; bucket height {x['bucket_h']:.2f} ±0.2",
    ]
    return "\n".join(out)


def build(L: float, T: float, out: Path) -> list[Path]:
    import cadquery as cq
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.gp import gp_Pnt
    from OCP.TopAbs import TopAbs_IN

    solids = dict(zip(NAMES, cq.importers.importStep(str(STEP)).solids().vals()))
    brk, bkt, stp = solids["Decontaminator"], solids["350mm Bucket"], solids["Stop Bracket"]

    def inside(s, x, y, z):
        return BRepClass3d_SolidClassifier(s.wrapped, gp_Pnt(x, y, z), 1e-4).State() == TopAbs_IN

    # The constants above are this STEP's geometry; refuse to build from a different file.
    assert abs(bkt.BoundingBox().zmax - EXT - B) < 0.02, "bucket top moved: source STEP changed"
    assert abs(brk.BoundingBox().zmax - EXT - F) < 0.02, "bracket top moved: source STEP changed"
    assert inside(brk, 106.1, 724.5, S + EXT - 0.1) and not inside(brk, 106.1, 724.5, S + EXT + 0.1), \
        "wiper seat floor moved: source STEP changed"
    assert inside(brk, 70.2, 729.0, K - 3.0 + EXT - 0.1) and not inside(brk, 70.2, 729.0, K - 3.0 + EXT + 0.1), \
        "sheet-stop boss top moved: source STEP changed"

    def box(x0, x1, y0, y1, z0, z1):
        return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0)).val()

    if L > 0:
        z0, top = SEAT["z_floor"], brk.BoundingBox().zmax + 1
        posts = brk.intersect(box(SEAT["x0"], SEAT["x1"], SEAT["y0"], SEAT["y1"], z0, top))
        brk = brk.cut(box(SEAT["x0"], SEAT["x1"], SEAT["y0"], SEAT["y1"], z0 - L, top))
        if posts.Volume() > 1e-6:
            brk = brk.fuse(posts.translate(cq.Vector(0, 0, -L)))
        brk = brk.clean()
    if T > 0:
        bb = bkt.BoundingBox()
        bkt = bkt.intersect(box(bb.xmin - 1, bb.xmax + 1, bb.ymin - 1, bb.ymax + 1, bb.zmin - 1, bb.zmax - T)).clean()

    out.mkdir(parents=True, exist_ok=True)
    written = []
    for shape, name, mirror in ((brk, f"brush_bracket_L{L:.1f}_MIRROR", True),
                                (bkt, f"bucket350_T{T:.1f}_MIRROR", True),
                                (stp, "stop_bracket", False)):
        bb = shape.BoundingBox()
        s = shape.translate(cq.Vector(-(bb.xmin + bb.xmax) / 2, -(bb.ymin + bb.ymax) / 2, -bb.zmin))
        if mirror:
            s = s.mirror("YZ")
        path = out / f"{name}.stl"
        cq.exporters.export(s, str(path), tolerance=0.01, angularTolerance=0.1)
        b2 = s.BoundingBox()
        print(f"wrote {path.relative_to(HERE)}  {b2.xlen:.2f} x {b2.ylen:.2f} x {b2.zlen:.2f} mm")
        written.append(path)
    return written


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--defaults", action="store_true", help="regenerate the committed default set")
    for k in ("H", "w", "d", "O"):
        ap.add_argument(f"--{k}", type=float)
    ap.add_argument("--G", type=float)
    ap.add_argument("--decide-only", action="store_true", help="print the decision, write nothing")
    a = ap.parse_args()
    if a.defaults:
        x, out = decide(G=None, **NOMINAL), HERE
    else:
        missing = [k for k in ("H", "w", "d", "O") if getattr(a, k) is None]
        if missing:
            ap.error("needs --" + " --".join(missing) + " (or --defaults)")
        x, out = decide(a.H, a.w, a.d, a.G, a.O), HERE / "measured"
    print(report(x))
    if x["nogo"] or a.decide_only:
        return 2 if x["nogo"] else 0
    if a.defaults:
        for old in HERE.glob("*.stl"):
            old.unlink()
    build(x["L"], x["T"], out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
