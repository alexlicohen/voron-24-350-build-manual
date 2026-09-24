#!/usr/bin/env python3
"""Serial nameplate for the finished Voron 2.4 350 (Step 14.24).

Generates an STL and a PNG preview of a flat plate that bolts to a 2020
extrusion with two M3x8 SHCS into M3 roll-in T-nuts (kit hardware; the kit has
no M3x8 BHCS) and carries three embossed lines:

    VORON 2.4 350
    <serial>
    <names> · <date>

Mount (see docs/manual/14-calibration.md, Step 14.24): the **front face of the
top front rail**, the horizontal A extrusion above the door opening. The front
*lower* rail is not available — the twelve-segment skirt ring (67 x 20 mm
cross-section) bolts up into its T-nut slots and covers it (Ch 11 Steps 11.1,
11.12, 11.13). The two front uprights are 20 mm wide, so a 90 mm plate across
one of them would overhang 35 mm into the door opening; the left upright's
front slot also already carries the four Clicky-Clack hinge T-nuts (Step 11.62).

Run with the CadQuery venv:

    venv-cq/bin/python scripts/nameplate.py \
        --serial V2.1234 --names "Alex & Helper" --date 2026-12-20 \
        --out docs/manual/assets/nameplate/nameplate.stl

Idempotent: re-running overwrites the same STL/PNG, nothing is appended.
No supports, no brim: the plate prints flat on its back face, text up.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import cadquery as cq
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.font_manager as fm  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.collections import PolyCollection  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "slicer"))
import geom  # noqa: E402  (slicer/geom.py — read_stl, bbox; stdlib only)

# ----------------------------------------------------------------- geometry

LENGTH = 90.0        # mm, along the extrusion
WIDTH = 24.0         # mm, across a 20 mm extrusion face (2 mm proud each side)
THICKNESS = 3.0      # mm, plate body
EMBOSS = 0.8         # mm, text proud of the body
SINK = 0.2           # mm, text is sunk this far into the body so the union is
                     # on overlapping solids, not coincident faces
CHAMFER = 0.8        # mm, all body edges
HOLE_D = 3.4         # mm, M3 clearance
HOLE_PITCH = 70.0    # mm, the two M3 T-nuts, 10 mm in from each end
HOLE_CHAMFER = 0.4   # mm, so the M3x8 SHCS head seats without a raised lip

# Nominal type sizes (CadQuery `fontsize`, i.e. em height in mm). Each line is
# shrunk if it would not fit its lane; none is ever grown.
SIZE_TITLE = 6.5
SIZE_SERIAL = 8.0
SIZE_CREDIT = 5.0
LINE_Y = (7.2, 0.0, -7.2)   # title, serial, credit

# DejaVu Sans Bold stem width / fontsize, measured from the "I" glyph at build
# time (see _stem_width). 0.8 mm is the floor for a 0.4 mm nozzle: two beads.
MIN_STROKE = 0.8

FONT_NAME = "DejaVu Sans"
FONT_KIND = "bold"

# The holes only block the strip |y| < HOLE_D/2 + 1.0. Lines 1 and 3 sit clear
# of it and may run nearly the full plate; line 2 has to stop short of them.
EDGE_MARGIN = 5.0


def _font_path() -> str:
    """matplotlib ships DejaVu Sans, so this resolves in any venv that has it."""
    return fm.findfont(f"{FONT_NAME}:bold", fallback_to_default=False)


def _text_solid(txt: str, size: float, font_path: str):
    return cq.Workplane("XY").text(
        txt, size, EMBOSS + SINK, combine=False, clean=True,
        font=FONT_NAME, fontPath=font_path, kind=FONT_KIND,
        halign="center", valign="center",
    )


def _bbox(txt: str, size: float, font_path: str):
    return _text_solid(txt, size, font_path).val().BoundingBox()


def _stem_width(size: float, font_path: str) -> float:
    """Actual printed stroke width at this type size: the width of an 'I'."""
    return _bbox("I", size, font_path).xlen


def _fit_size(txt: str, nominal: float, max_width: float, font_path: str) -> float:
    """Largest size <= nominal whose rendered width fits max_width."""
    w = _bbox(txt, nominal, font_path).xlen
    if w <= max_width:
        return nominal
    return nominal * max_width / w


def build(serial: str, names: str, date: str, font_path: str):
    """(solid, report dict). Grows the plate length if a line cannot hold the
    0.8 mm stroke floor at the length asked for."""
    lines = [("VORON 2.4 350", SIZE_TITLE), (serial, SIZE_SERIAL),
             (f"{names} · {date}", SIZE_CREDIT)]

    length = LENGTH
    for _ in range(8):
        half = length / 2 - EDGE_MARGIN
        # lane width: lines 1 and 3 clear the holes, line 2 must stop short
        lanes = [2 * half, HOLE_PITCH - HOLE_D - 4.0, 2 * half]
        sizes = [_fit_size(t, s, w, font_path) for (t, s), w in zip(lines, lanes)]
        strokes = [_stem_width(s, font_path) for s in sizes]
        worst = min(strokes)
        if worst >= MIN_STROKE - 1e-6:
            break
        length = math.ceil(length * (MIN_STROKE / worst) * 10) / 10
    else:
        raise SystemExit("could not fit the text at a 0.8 mm stroke")

    plate = (
        cq.Workplane("XY")
        .box(length, WIDTH, THICKNESS, centered=(True, True, False))
        .edges().chamfer(CHAMFER)
        .faces(">Z").workplane()
        .pushPoints([(-HOLE_PITCH / 2, 0.0), (HOLE_PITCH / 2, 0.0)])
        .hole(HOLE_D)
        .edges(cq.selectors.RadiusNthSelector(0)).chamfer(HOLE_CHAMFER)
    )

    solid = plate
    for (txt, _), size, y in zip(lines, sizes, LINE_Y):
        solid = solid.union(
            _text_solid(txt, size, font_path).translate((0, y, THICKNESS - SINK))
        )

    n_solids = len(solid.val().Solids())
    if n_solids != 1:
        raise SystemExit(f"text did not fuse to the plate: {n_solids} separate solids")

    report = {
        "length": length, "width": WIDTH, "thickness": THICKNESS,
        "lines": [(t, round(s, 2), round(k, 2), round(_bbox(t, s, font_path).xlen, 1))
                  for (t, _), s, k in zip(lines, sizes, strokes)],
    }
    return solid, report


# -------------------------------------------------------------- STL checks

def stl_stats(path: Path) -> dict:
    """Watertight (every edge used exactly twice, in opposite directions),
    bbox and signed volume, from the exported triangles. Uses slicer/geom.py's
    reader so this script does not add a mesh dependency."""
    tris = geom.read_stl(path)
    xmin, ymin, zmin, xmax, ymax, zmax = geom.bbox(tris)

    def key(p):
        return (round(p[0], 5), round(p[1], 5), round(p[2], 5))

    edges: dict[tuple, int] = {}
    vol = 0.0
    for tri in tris:
        a, b, c = tri[0], tri[1], tri[2]
        vol += (a[0] * (b[1] * c[2] - b[2] * c[1])
                - a[1] * (b[0] * c[2] - b[2] * c[0])
                + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0
        ka, kb, kc = key(a), key(b), key(c)
        for u, v in ((ka, kb), (kb, kc), (kc, ka)):
            edges[(u, v)] = edges.get((u, v), 0) + 1

    unpaired = [e for e, n in edges.items() if n != 1 or edges.get((e[1], e[0]), 0) != 1]
    return {
        "triangles": len(tris),
        "watertight": not unpaired,
        "unpaired_edges": len(unpaired),
        "bbox": (round(xmax - xmin, 3), round(ymax - ymin, 3), round(zmax - zmin, 3)),
        "volume_mm3": round(abs(vol), 1),
    }


# ------------------------------------------------------------------ preview

def render_png(stl: Path, png: Path, title: str) -> None:
    """Shaded three-quarter preview. Headless matplotlib, same reasoning as
    scripts/render_parts.py (no OSMesa/EGL on macOS), but the projection is done
    here and drawn as a 2D PolyCollection: mplot3d cannot be framed tightly
    enough for a 90 x 24 mm plate and its depth sort shows through the emboss."""
    tris = np.asarray(geom.read_stl(stl), dtype=float)
    zc = tris[:, :, 2].mean(axis=1)              # model z, before centring
    tris = tris - tris.reshape(-1, 3).mean(axis=0)

    tilt = math.radians(-17.0)                   # no in-plane spin: text stays level
    rx = np.array([[1.0, 0.0, 0.0],
                   [0.0, math.cos(tilt), -math.sin(tilt)],
                   [0.0, math.sin(tilt), math.cos(tilt)]])
    view = tris @ rx.T

    n = np.cross(view[:, 1] - view[:, 0], view[:, 2] - view[:, 0])
    ln = np.linalg.norm(n, axis=1)
    ln[ln == 0] = 1.0
    n = n / ln[:, None]
    front = n[:, 2] > 0.0                        # cull back faces: painter's sort
    view, n, zc = view[front], n[front], zc[front]

    # Three tones, by what the facet is: the raised text, the plate face it sits
    # on, and everything vertical (letter walls, chamfers, hole bores). Lambert
    # shading alone cannot separate the first two — both point straight up.
    flat = n[:, 2] > 0.85
    tone = np.tile(np.array([0.055, 0.150, 0.360]), (len(n), 1))          # walls
    tone[flat & (zc < THICKNESS + EMBOSS / 2)] = (0.125, 0.330, 0.690)    # plate
    tone[flat & (zc >= THICKNESS + EMBOSS / 2)] = (0.560, 0.720, 0.960)   # text

    light = np.array([-0.26, 0.24, 0.94])
    light = light / np.linalg.norm(light)
    shade = 0.62 + 0.38 * np.clip(n @ light, 0.0, 1.0)
    cols = np.clip(tone * shade[:, None], 0, 1)
    # Painter's sort on the *model* z first: the plate's top face tessellates
    # into a few huge triangles that span the text, so a centroid sort in view
    # space draws them over it. Nothing on this part overhangs anything.
    order = np.lexsort((view[:, :, 2].mean(axis=1), zc))

    fig, ax = plt.subplots(figsize=(7.4, 2.5), dpi=220)
    ax.add_collection(PolyCollection(view[order][:, :, :2], facecolors=cols[order],
                                     edgecolors=cols[order], linewidths=0.15))
    pts = view.reshape(-1, 3)
    lo, hi = pts[:, :2].min(axis=0), pts[:, :2].max(axis=0)
    pad = (hi - lo).max() * 0.035
    ax.set_xlim(lo[0] - pad, hi[0] + pad)
    ax.set_ylim(lo[1] - pad, hi[1] + pad * 3.2)
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.text(0.5, 0.02, title, transform=ax.transAxes, ha="center", va="bottom",
            fontsize=7, color="#666666")
    fig.patch.set_facecolor("white")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(png, facecolor="white")
    plt.close(fig)


# --------------------------------------------------------------------- main

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--serial", default="V2.0000",
                    help="serial as the Reddit mods issue it, e.g. V2.1234")
    ap.add_argument("--names", default="Alex & Helper",
                    help="who built it (placeholder by default — no real names in the repo)")
    ap.add_argument("--date", default="2026-12-20", help="completion date, ISO")
    ap.add_argument("--out", default="docs/manual/assets/nameplate/nameplate.stl",
                    help="STL path; the PNG preview is written alongside it")
    ap.add_argument("--png", default=None, help="override the PNG path")
    args = ap.parse_args(argv)

    out = Path(args.out)
    if not out.is_absolute():
        out = REPO_ROOT / out
    png = Path(args.png) if args.png else out.with_suffix(".png")
    if not png.is_absolute():
        png = REPO_ROOT / png

    font_path = _font_path()
    solid, report = build(args.serial, args.names, args.date, font_path)

    out.parent.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(solid, str(out), tolerance=0.01, angularTolerance=0.1)
    render_png(out, png, f"{args.serial} — {report['length']:.0f} x {WIDTH:.0f} x "
                         f"{THICKNESS:.0f} mm, text {EMBOSS} mm proud")

    stats = stl_stats(out)
    print(f"font        {font_path}")
    print(f"plate       {report['length']:.1f} x {WIDTH:.1f} x {THICKNESS:.1f} mm, "
          f"chamfer {CHAMFER} mm, 2x M3 clearance {HOLE_D} mm at {HOLE_PITCH:.0f} mm pitch")
    for txt, size, stroke, width in report["lines"]:
        print(f"  line      {txt!r:34} size {size:>5} mm  stroke {stroke:.2f} mm  "
              f"width {width:.1f} mm")
    print(f"stl         {out.relative_to(REPO_ROOT)}")
    print(f"png         {png.relative_to(REPO_ROOT)}")
    print(f"triangles   {stats['triangles']}")
    print(f"watertight  {stats['watertight']} ({stats['unpaired_edges']} unpaired edges)")
    print(f"bbox        {stats['bbox'][0]} x {stats['bbox'][1]} x {stats['bbox'][2]} mm")
    print(f"volume      {stats['volume_mm3']} mm^3  (~{stats['volume_mm3'] * 1.07e-3:.1f} g ASA)")
    return 0 if stats["watertight"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
