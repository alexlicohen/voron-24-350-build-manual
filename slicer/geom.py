#!/usr/bin/env python3
"""Mesh reading, footprints and plate packing - stdlib only.

PrusaSlicer 2.9.6's CLI cannot arrange for us: `--merge` + arrange segfaults,
and arranging a merged 3MF is a silent no-op that leaves objects stacked on top
of each other and still exits 0. So the arrangement is computed here, committed
in the 3MF, and every plate is sliced with `--dont-arrange`.
"""
from __future__ import annotations

import math
import struct
from pathlib import Path

Vec3 = tuple[float, float, float]
Tri = tuple[Vec3, Vec3, Vec3]


# ---------------------------------------------------------------- mesh input

def read_stl(path: Path) -> list[Tri]:
    """Read a binary or ASCII STL into a list of triangles."""
    data = path.read_bytes()
    if len(data) >= 84:
        (count,) = struct.unpack_from("<I", data, 80)
        if 84 + count * 50 == len(data):
            tris: list[Tri] = []
            off = 84
            unpack = struct.Struct("<12fH").unpack_from
            for _ in range(count):
                v = unpack(data, off)
                tris.append(((v[3], v[4], v[5]), (v[6], v[7], v[8]), (v[9], v[10], v[11])))
                off += 50
            return tris
    # ASCII fallback
    tris = []
    pts: list[Vec3] = []
    for line in data.decode("utf-8", "replace").splitlines():
        parts = line.split()
        if parts and parts[0] == "vertex":
            pts.append((float(parts[1]), float(parts[2]), float(parts[3])))
            if len(pts) == 3:
                tris.append((pts[0], pts[1], pts[2]))
                pts = []
    return tris


def bbox(tris: list[Tri]) -> tuple[float, float, float, float, float, float]:
    xs = [v[0] for t in tris for v in t]
    ys = [v[1] for t in tris for v in t]
    zs = [v[2] for t in tris for v in t]
    return min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)


# ------------------------------------------------------------- convex hull

def convex_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Monotone-chain hull of the XY projection. Points are deduplicated first
    because an STL repeats every vertex across its adjacent facets."""
    pts = sorted(set((round(x, 3), round(y, 3)) for x, y in points))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower: list[tuple[float, float]] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list[tuple[float, float]] = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def rotated_extent(hull: list[tuple[float, float]], deg: float
                   ) -> tuple[float, float, float, float]:
    """(min_x, min_y, max_x, max_y) of the hull rotated `deg` about Z."""
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    xs = [x * c - y * s for x, y in hull]
    ys = [x * s + y * c for x, y in hull]
    return min(xs), min(ys), max(xs), max(ys)


# ---------------------------------------------------------------- packing

BED_X, BED_Y = 250.0, 220.0
EDGE_MARGIN = 4.0  # room for the 1-loop skirt at its 3 mm gap, all four sides


class Piece:
    """One object instance waiting to be placed."""

    def __init__(self, key: str, name: str, hull: list[tuple[float, float]],
                 brim: float, z_min: float):
        self.key = key
        self.name = name
        self.hull = hull
        self.brim = brim
        self.z_min = z_min
        self.rot = 0.0
        self.x = 0.0
        self.y = 0.0

    def extent(self, deg: float | None = None) -> tuple[float, float, float, float]:
        return rotated_extent(self.hull, self.rot if deg is None else deg)

    def size(self, deg: float | None = None) -> tuple[float, float]:
        x0, y0, x1, y1 = self.extent(deg)
        return x1 - x0, y1 - y0


ORDERINGS = {
    "longest-side": lambda s: (-max(s), -s[0] * s[1]),
    "area": lambda s: (-s[0] * s[1], -max(s)),
    "height": lambda s: (-s[1], -s[0]),
    "width": lambda s: (-s[0], -s[1]),
    "perimeter": lambda s: (-(s[0] + s[1]), -max(s)),
}


def _maxrects(sizes: list[tuple[float, float]], bin_w: float, bin_h: float,
              keyfn) -> list[tuple[float, float, bool]] | None:
    """MaxRects best-short-side-fit with 90 deg rotation.

    `sizes` must already include each part's brim and clearance. Returns one
    (x, y, rotated) per input in input order, or None if anything overflows.
    """
    free: list[tuple[float, float, float, float]] = [(0.0, 0.0, bin_w, bin_h)]
    out: list[tuple[float, float, bool] | None] = [None] * len(sizes)
    order = sorted(range(len(sizes)), key=lambda i: keyfn(sizes[i]))

    eps = 1e-6
    for idx in order:
        w, h = sizes[idx]
        best = None  # (short_leftover, long_leftover, x, y, w, h, rotated)
        for fx, fy, fw, fh in free:
            for ww, hh, rot in ((w, h, False), (h, w, True)):
                if ww <= fw + eps and hh <= fh + eps:
                    short = min(fw - ww, fh - hh)
                    long_ = max(fw - ww, fh - hh)
                    cand = (short, long_, fy, fx, ww, hh, rot)
                    if best is None or cand[:4] < best[:4]:
                        best = cand
        if best is None:
            return None
        _s, _l, y, x, ww, hh, rot = best
        out[idx] = (x, y, rot)
        placed = (x, y, ww, hh)
        # split every free rect this placement overlaps
        nxt: list[tuple[float, float, float, float]] = []
        for r in free:
            nxt.extend(_split(r, placed))
        free = _prune(nxt)
    return [o for o in out if o is not None]


def _split(r, p):
    rx, ry, rw, rh = r
    px, py, pw, ph = p
    if px >= rx + rw or px + pw <= rx or py >= ry + rh or py + ph <= ry:
        return [r]
    out = []
    if py > ry:
        out.append((rx, ry, rw, py - ry))
    if py + ph < ry + rh:
        out.append((rx, py + ph, rw, ry + rh - (py + ph)))
    if px > rx:
        out.append((rx, ry, px - rx, rh))
    if px + pw < rx + rw:
        out.append((px + pw, ry, rx + rw - (px + pw), rh))
    return [q for q in out if q[2] > 1e-6 and q[3] > 1e-6]


def _prune(rects):
    keep = []
    for i, a in enumerate(rects):
        contained = False
        for j, b in enumerate(rects):
            if i != j and a[0] >= b[0] - 1e-9 and a[1] >= b[1] - 1e-9 \
               and a[0] + a[2] <= b[0] + b[2] + 1e-9 and a[1] + a[3] <= b[1] + b[3] + 1e-9 \
               and (a != b or j < i):
                contained = True
                break
        if not contained:
            keep.append(a)
    return keep


CLEARANCE = 3.0  # bare mm between two parts once each one's brim is accounted for


def pack(pieces: list[Piece], bed: tuple[float, float] = (BED_X, BED_Y)
         ) -> tuple[bool, list[str]]:
    """Place every piece on the bed. Sets `rot`, `x`, `y` (the piece's own
    bounding-box origin, brim excluded) and returns (fits, [what didn't fit]).

    Each piece is inflated by its own brim plus half the clearance, so two
    neighbours end up `brim_i + brim_j + CLEARANCE` apart and a 5 mm-brimmed
    part does not push every other part on the plate away from it.

    Axis-aligned bounding boxes rather than no-fit polygons: conservative, so a
    plate this reports as fitting really does fit, and the packing is
    deterministic, so the committed 3MF is reviewable and reproducible.
    """
    usable_w = bed[0] - 2 * EDGE_MARGIN
    usable_h = bed[1] - 2 * EDGE_MARGIN

    infl = [p.brim + CLEARANCE / 2.0 for p in pieces]
    sizes = [(p.size(0.0)[0] + 2 * i, p.size(0.0)[1] + 2 * i)
             for p, i in zip(pieces, infl)]
    # Try every ordering and keep the tightest result: a compact, roughly square
    # arrangement means shorter travel moves and a preview that reads well.
    best = None
    for _name, keyfn in ORDERINGS.items():
        cand = _maxrects(sizes, usable_w, usable_h, keyfn)
        if cand is None:
            continue
        w = max(x + (s[1] if r else s[0]) for (x, _y, r), s in zip(cand, sizes))
        h = max(y + (s[0] if r else s[1]) for (_x, y, r), s in zip(cand, sizes))
        score = (w * h, abs(w / bed[0] - h / bed[1]))
        if best is None or score < best[0]:
            best = (score, cand)
    placements = best[1] if best else None
    if placements is None:
        bad = []
        for p, (w, h) in zip(pieces, sizes):
            if min(w, h) > min(usable_w, usable_h) or max(w, h) > max(usable_w, usable_h):
                bad.append(f"{p.name} needs {w:.1f} x {h:.1f} mm with brim")
        if not bad:
            worst = sorted(zip(pieces, sizes), key=lambda t: -t[1][0] * t[1][1])[:3]
            bad = [f"{p.name} ({w:.1f} x {h:.1f} mm with brim)" for p, (w, h) in worst]
        return False, bad

    for p, i, (x, y, rot) in zip(pieces, infl, placements):
        p.rot = 90.0 if rot else 0.0
        p.x, p.y = x + i, y + i

    used_x0 = min(p.x - i for p, i in zip(pieces, infl))
    used_y0 = min(p.y - i for p, i in zip(pieces, infl))
    used_x1 = max(p.x + p.size()[0] + i for p, i in zip(pieces, infl))
    used_y1 = max(p.y + p.size()[1] + i for p, i in zip(pieces, infl))
    off_x = (bed[0] - (used_x1 - used_x0)) / 2.0 - used_x0
    off_y = (bed[1] - (used_y1 - used_y0)) / 2.0 - used_y0
    for p in pieces:
        p.x += off_x
        p.y += off_y
    return True, []
