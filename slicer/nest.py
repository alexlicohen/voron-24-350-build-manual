#!/usr/bin/env python3
"""Outline-aware plate nesting - stdlib only, drop-in for geom.pack.

PrusaSlicer 2.9.6's CLI cannot arrange (there is no `--arrange`; the implicit
arrange on a loaded multi-object 3MF is a no-op; separate inputs without
`--merge` export one file each; `--merge` plus the implicit arrange segfaults in
`Slic3r::CLI::process_transform`), so the arrangement has to be computed here.
`geom.pack` does it on axis-aligned bounding boxes, which throws away the bed
around every L-shaped, C-shaped or skirt-shaped part. This packs the real
bottom-facing silhouette instead, the way libnest2d does inside the GUI.

The GUI stays the final QC authority: this proposes a layout and proves a set of
parts fits.

Method
  footprint   every triangle of the STL projected to XY and unioned - the
              silhouette, not the bottom face - rasterised conservatively (any
              cell a triangle touches) at RES mm into one int per row, bit x =
              cell x. Conservative means the raster is never smaller than the
              part, so a clearance measured on it is never optimistic.
  clearance   each footprint is dilated by a discrete disc of `brim + gap/2`, so
              two neighbours end up `brim_i + brim_j + gap` apart and a 5 mm brim
              does not push every other part on the plate away from it. The
              on-the-bed test is against footprint + brim only, so a clearance
              halo may hang over the bed edge but a brim never does.
  rotation    0/90/180/270 about Z only - never a different bed face, the
              orientations in docs/manual/00-slicer-setup.md are load-bearing.
              Only the 0 raster is built from the mesh: 90 is its transpose,
              180/270 are bit-reversals of those two.
  placement   five candidate layouts, the tightest wins. Measured like for like
              (`--compare --gap=3`, geom.pack's own clearance) that is tighter on
              19 of the 27 plates, 47.0% -> 52.6% mean outline fill, and never more
              than 1.7% looser on the rest - the conservative raster and the extra
              cell `_bbox_layouts` adds cost up to RES mm a side:
                * largest-area-first and longest-side-first, each with a
                  centre-out first fit (libnest2d's centre bias - compact, and
                  keeps ASA shrinkage symmetric) and with a bottom-left first
                  fit (which is what rescues a plate of two long parts, where
                  centre-out parks the first part where the second can no longer
                  clear it),
                * geom.pack's own MaxRects bounding-box layout, snapped to the
                  raster and re-checked: boxes that do not overlap cannot have
                  overlapping outlines.
              Each of the four first-fit layouts then gets one improvement pass
              that lifts parts smallest-first and re-inserts them, keeping the
              new spot only when it scores better. No randomness anywhere: same
              inputs, same plate, byte for byte.
  fallback    a plate that will not fit at `gap` is retried down GAP_LADDER (to
              3 mm, the clearance geom.pack has always used) and the relaxation
              is reported on stderr. Only then does it fail, naming the part.

    python3 slicer/nest.py --compare     # every plate: committed 3MF vs this packer
    python3 slicer/nest.py --selftest    # clearance + on-bed + determinism asserts
    python3 slicer/nest.py --compare --gap=3   # like-for-like against geom.pack
"""
from __future__ import annotations

import math
import struct
import sys
import time
from pathlib import Path

from geom import BED_X, BED_Y, EDGE_MARGIN, ORDERINGS, Piece, _maxrects, read_stl

ROOT = Path(__file__).resolve().parent
STL_DIR = ROOT / "stl"

RES = 0.5           # mm per raster cell
GAP = 6.0           # mm of bare bed between any two outlines, brims excluded
GAP_LADDER = (5.0, 4.0, 3.0)   # only if the plate will not fit at GAP; 3.0 = geom.CLEARANCE
STEP = 2            # first-fit lattice in cells -> 1.0 mm
ROTATIONS = (0, 90, 180, 270)
IMPROVE = True      # second pass: re-insert parts smallest-first, keep if better


class NoFit(RuntimeError):
    """A part could not be placed. `part` names it."""

    def __init__(self, part: str, msg: str):
        super().__init__(msg)
        self.part = part


# ------------------------------------------------------------- rasterising

def _tri_xy(path: Path) -> list[tuple[float, float, float, float, float, float]]:
    """(ax, ay, bx, by, cx, cy) per triangle. Binary STL fast path, geom.read_stl otherwise."""
    data = path.read_bytes()
    if len(data) >= 84:
        (count,) = struct.unpack_from("<I", data, 80)
        if 84 + count * 50 == len(data):
            return [(v[3], v[4], v[6], v[7], v[9], v[10])
                    for v in struct.iter_unpack("<12fH", data[84:])]
    return [(t[0][0], t[0][1], t[1][0], t[1][1], t[2][0], t[2][1]) for t in read_stl(path)]


def _rasterise(tris, minx: float, miny: float, w: int, h: int) -> list[int]:
    """Union of the projected triangles as `h` row bitmasks of `w` cells."""
    inv = 1.0 / RES
    rows = [0] * h
    wm1, hm1 = w - 1, h - 1
    for ax, ay, bx, by, cx, cy in tris:
        ylo = ay if ay < by else by
        if cy < ylo:
            ylo = cy
        yhi = ay if ay > by else by
        if cy > yhi:
            yhi = cy
        j0 = int((ylo - miny) * inv)
        j1 = int((yhi - miny) * inv)
        if j0 < 0:
            j0 = 0
        if j1 > hm1:
            j1 = hm1
        if j1 < j0:
            continue
        if j1 - j0 <= 1:
            # spans one or two rows: the triangle's own bbox is tight enough to fill
            xlo = ax if ax < bx else bx
            if cx < xlo:
                xlo = cx
            xhi = ax if ax > bx else bx
            if cx > xhi:
                xhi = cx
            i0 = int((xlo - minx) * inv)
            i1 = int((xhi - minx) * inv)
            if i0 < 0:
                i0 = 0
            if i1 > wm1:
                i1 = wm1
            if i1 < i0:
                continue
            m = ((1 << (i1 - i0 + 1)) - 1) << i0
            rows[j0] |= m
            if j1 != j0:
                rows[j1] |= m
            continue
        # tall triangle: exact x extent per row band, from the three edges
        edges = ((ax, ay, bx, by), (bx, by, cx, cy), (cx, cy, ax, ay))
        for j in range(j0, j1 + 1):
            yl = miny + j * RES
            yh = yl + RES
            lo, hi = 1e30, -1e30
            for x0, y0, x1, y1 in edges:
                e0, e1 = (y0, y1) if y0 <= y1 else (y1, y0)
                a = yl if yl > e0 else e0
                b = yh if yh < e1 else e1
                if a > b:
                    continue
                dy = y1 - y0
                if dy == 0.0:
                    xa, xb = x0, x1
                else:
                    xa = x0 + (a - y0) / dy * (x1 - x0)
                    xb = x0 + (b - y0) / dy * (x1 - x0)
                if xa > xb:
                    xa, xb = xb, xa
                if xa < lo:
                    lo = xa
                if xb > hi:
                    hi = xb
            if hi < lo:
                continue
            i0 = int((lo - minx) * inv)
            i1 = int((hi - minx) * inv)
            if i0 < 0:
                i0 = 0
            if i1 > wm1:
                i1 = wm1
            if i1 < i0:
                continue
            rows[j] |= ((1 << (i1 - i0 + 1)) - 1) << i0
    return rows


_REV8 = bytes(int(format(i, "08b")[::-1], 2) for i in range(256))


def _revbits(x: int, w: int) -> int:
    """Reverse the low `w` bits of x."""
    nb = (w + 7) // 8
    b = x.to_bytes(nb, "little")
    return int.from_bytes(bytes(_REV8[c] for c in b)[::-1], "little") >> (nb * 8 - w)


def _transpose(rows: list[int], w: int, h: int) -> list[int]:
    """Raster of the 90 deg CCW rotation: cell (cx, cy) -> (h-1-cy, cx)."""
    out = [0] * w
    for cy, row in enumerate(rows):
        if not row:
            continue
        bit = 1 << (h - 1 - cy)
        r = row
        while r:
            low = r & -r
            out[low.bit_length() - 1] |= bit
            r ^= low
    return out


def _flip(rows: list[int], w: int) -> list[int]:
    """Raster of the 180 deg rotation."""
    return [_revbits(x, w) for x in reversed(rows)]


def _dilate(rows: list[int], w: int, h: int, r: int) -> tuple[list[int], int, int]:
    """Dilate by a discrete disc of radius `r` cells; pads r cells all round."""
    if r <= 0:
        return list(rows), w, h
    cur = [x << r for x in rows]
    horiz = [cur]
    for _ in range(r):
        cur = [(x | (x << 1) | (x >> 1)) for x in cur]
        horiz.append(cur)
    out = [0] * (h + 2 * r)
    for v in range(-r, r + 1):
        src = horiz[math.isqrt(r * r - v * v)]
        base = r + v
        for y in range(h):
            if src[y]:
                out[y + base] |= src[y]
    return out, w + 2 * r, h + 2 * r


# --------------------------------------------------------------- footprints

class _Foot:
    """Rotation-0 footprint of one STL, in raster cells."""
    __slots__ = ("rows", "w", "h", "minx", "miny", "maxx", "maxy", "cells")

    def __init__(self, key: str):
        tris = _tri_xy(STL_DIR / key)
        if not tris:
            raise ValueError(f"{key}: no triangles")
        xs = [t[0] for t in tris] + [t[2] for t in tris] + [t[4] for t in tris]
        ys = [t[1] for t in tris] + [t[3] for t in tris] + [t[5] for t in tris]
        self.minx, self.maxx = min(xs), max(xs)
        self.miny, self.maxy = min(ys), max(ys)
        self.w = int((self.maxx - self.minx) / RES) + 1
        self.h = int((self.maxy - self.miny) / RES) + 1
        self.rows = _rasterise(tris, self.minx, self.miny, self.w, self.h)
        self.cells = sum(bin(r).count("1") for r in self.rows)


class Shape:
    """One STL at one rotation with one brim and one gap: what the placer moves around.

    `rows` is the clearance-dilated raster; `pad` is how many cells of it lie outside
    the footprint on each side. `ex`/`ey` carry the sub-cell offset between the raster
    box corner and the part's true rotated bbox corner, which is what `Piece.x`/`y` mean.
    """
    __slots__ = ("key", "rot", "brim", "gap", "rows", "fw", "fh", "ex", "ey",
                 "pad", "pw", "ph", "nz", "area")

    def __init__(self, key: str, rot: int, brim: float, gap: float, foot: _Foot):
        self.key, self.rot, self.brim, self.gap = key, rot, brim, gap
        slack_x = foot.minx + foot.w * RES - foot.maxx
        slack_y = foot.miny + foot.h * RES - foot.maxy
        gw, gh = foot.maxx - foot.minx, foot.maxy - foot.miny
        if rot == 0:
            rows, w, h = list(foot.rows), foot.w, foot.h
            self.ex, self.ey, self.fw, self.fh = 0.0, 0.0, gw, gh
        elif rot == 90:
            rows, w, h = _transpose(foot.rows, foot.w, foot.h), foot.h, foot.w
            self.ex, self.ey, self.fw, self.fh = slack_y, 0.0, gh, gw
        elif rot == 180:
            rows, w, h = _flip(foot.rows, foot.w), foot.w, foot.h
            self.ex, self.ey, self.fw, self.fh = slack_x, slack_y, gw, gh
        elif rot == 270:
            rows, w, h = _flip(_transpose(foot.rows, foot.w, foot.h), foot.h), foot.h, foot.w
            self.ex, self.ey, self.fw, self.fh = 0.0, slack_x, gh, gw
        else:
            raise ValueError(f"rotation {rot} is not a multiple of 90")
        self.pad = int(math.ceil((brim + gap / 2) / RES - 1e-9))
        self.rows, self.pw, self.ph = _dilate(rows, w, h, self.pad)
        self.nz = [(y, m) for y, m in enumerate(self.rows) if m]
        self.area = foot.cells * RES * RES


_foot_cache: dict[str, _Foot] = {}
_shape_cache: dict[tuple[str, int, float, float], Shape] = {}


def _foot(key: str) -> _Foot:
    f = _foot_cache.get(key)
    if f is None:
        f = _foot_cache[key] = _Foot(key)
    return f


def shape(key: str, rot: int, brim: float, gap: float) -> Shape:
    ck = (key, rot, brim, gap)
    sh = _shape_cache.get(ck)
    if sh is None:
        sh = _shape_cache[ck] = Shape(key, rot, brim, gap, _foot(key))
    return sh


def footprint_area(key: str) -> float:
    """mm^2 of the rasterised silhouette (rotation invariant to within one cell)."""
    return _foot(key).cells * RES * RES


# ------------------------------------------------------------------- grid

class _Grid:
    """The bed as row bitmasks, plus a gap/2 border the clearance halos may use."""
    __slots__ = ("bed", "gap", "gw", "gh", "ox", "oy", "rows")

    def __init__(self, bed: tuple[float, float], gap: float):
        border = int(math.ceil((gap / 2) / RES - 1e-9))
        self.bed, self.gap = bed, gap
        self.gw = int(round((bed[0] - 2 * EDGE_MARGIN) / RES)) + 2 * border
        self.gh = int(round((bed[1] - 2 * EDGE_MARGIN) / RES)) + 2 * border
        self.ox = self.oy = EDGE_MARGIN - border * RES
        self.rows = [0] * self.gh

    def free(self, sh: Shape, gx: int, gy: int) -> bool:
        rows = self.rows
        for y, m in sh.nz:
            if rows[gy + y] & (m << gx):
                return False
        return True

    def add(self, sh: Shape, gx: int, gy: int) -> None:
        for y, m in sh.nz:
            self.rows[gy + y] |= m << gx

    def remove(self, sh: Shape, gx: int, gy: int) -> None:
        for y, m in sh.nz:
            self.rows[gy + y] &= ~(m << gx)

    def limits(self, sh: Shape) -> tuple[int, int, int, int]:
        """Placement range in cells: halo inside the grid, footprint + brim on the bed."""
        lo_x = max(0, math.ceil(((EDGE_MARGIN + sh.brim) - self.ox - sh.ex) / RES
                                - sh.pad - 1e-9))
        hi_x = min(self.gw - sh.pw,
                   math.floor(((self.bed[0] - EDGE_MARGIN - sh.brim - sh.fw)
                               - self.ox - sh.ex) / RES - sh.pad + 1e-9))
        lo_y = max(0, math.ceil(((EDGE_MARGIN + sh.brim) - self.oy - sh.ey) / RES
                                - sh.pad - 1e-9))
        hi_y = min(self.gh - sh.ph,
                   math.floor(((self.bed[1] - EDGE_MARGIN - sh.brim - sh.fh)
                               - self.oy - sh.ey) / RES - sh.pad + 1e-9))
        return lo_x, hi_x, lo_y, hi_y

    def origin(self, sh: Shape, gx: int, gy: int) -> tuple[float, float]:
        """Bed mm of the part's own rotated bbox corner - what Piece.x / Piece.y mean."""
        return (self.ox + (gx + sh.pad) * RES + sh.ex,
                self.oy + (gy + sh.pad) * RES + sh.ey)


_templates: dict[tuple[int, int], list[tuple[int, int]]] = {}


def _template(gw: int, gh: int) -> list[tuple[int, int]]:
    """Lattice offsets in STEP units, nearest the centre first, ties bottom-left."""
    t = _templates.get((gw, gh))
    if t is None:
        ru, rv = gw // STEP + 1, gh // STEP + 1
        raw = sorted((u * u + v * v, v, u)
                     for v in range(-rv, rv + 1) for u in range(-ru, ru + 1))
        t = _templates[(gw, gh)] = [(u, v) for _r, v, u in raw]
    return t


# ---------------------------------------------------------------- placement

def _search(grid: _Grid, sh: Shape, bias: str) -> tuple[float, int, int] | None:
    """First collision-free lattice cell for `sh`. Returns (score, gx, gy)."""
    lo_x, hi_x, lo_y, hi_y = grid.limits(sh)
    if lo_x > hi_x or lo_y > hi_y:
        return None
    rows, nz = grid.rows, sh.nz
    if bias == "centre":
        cx = (grid.bed[0] / 2 - sh.fw / 2 - sh.ex - grid.ox) / RES - sh.pad
        cy = (grid.bed[1] / 2 - sh.fh / 2 - sh.ey - grid.oy) / RES - sh.pad
        bx, by = int(round(cx / STEP)), int(round(cy / STEP))
        for u, v in _template(grid.gw, grid.gh):
            gx = (bx + u) * STEP
            if gx < lo_x or gx > hi_x:
                continue
            gy = (by + v) * STEP
            if gy < lo_y or gy > hi_y:
                continue
            for y, m in nz:
                if rows[gy + y] & (m << gx):
                    break
            else:
                x0, y0 = grid.origin(sh, gx, gy)
                dx = x0 + sh.fw / 2 - grid.bed[0] / 2
                dy = y0 + sh.fh / 2 - grid.bed[1] / 2
                return dx * dx + dy * dy, gx, gy
        return None
    sx = -(-lo_x // STEP) * STEP
    for gy in range(-(-lo_y // STEP) * STEP, hi_y + 1, STEP):
        for gx in range(sx, hi_x + 1, STEP):
            for y, m in nz:
                if rows[gy + y] & (m << gx):
                    break
            else:
                return gy * (grid.gw + 1) + gx, gx, gy
    return None


def _best(grid: _Grid, p: Piece, gap: float, bias: str
          ) -> tuple[float, Shape, int, int] | None:
    """Cheapest (score, rotation) over the four rotations."""
    best = None
    for rot in ROTATIONS:
        sh = shape(p.key, rot, p.brim, gap)
        hit = _search(grid, sh, bias)
        if hit is not None and (best is None or (hit[0], rot) < (best[0], best[1])):
            best = (hit[0], rot, sh, hit[1], hit[2])
    return None if best is None else (best[0], best[2], best[3], best[4])


_ORDERS = {
    "area": lambda sh: (-sh.area, -max(sh.fw, sh.fh)),
    "longest": lambda sh: (-max(sh.fw, sh.fh), -sh.area),
}
STRATEGIES = (("area", "centre"), ("area", "bottom-left"),
              ("longest", "centre"), ("longest", "bottom-left"))

Layout = list[tuple[Shape, int, int]]


def _first_fit(pieces: list[Piece], bed: tuple[float, float], gap: float,
               order: str, bias: str) -> tuple[Layout | None, str]:
    grid = _Grid(bed, gap)
    key = _ORDERS[order]
    seq = sorted(range(len(pieces)),
                 key=lambda i: key(shape(pieces[i].key, 0, pieces[i].brim, gap))
                 + (pieces[i].key, pieces[i].name))
    out: Layout = [None] * len(pieces)          # type: ignore[list-item]
    score = [0.0] * len(pieces)
    for i in seq:
        hit = _best(grid, pieces[i], gap, bias)
        if hit is None:
            return None, pieces[i].name
        score[i], sh, gx, gy = hit
        grid.add(sh, gx, gy)
        out[i] = (sh, gx, gy)
    if IMPROVE:
        for i in reversed(seq):
            sh, gx, gy = out[i]
            grid.remove(sh, gx, gy)
            hit = _best(grid, pieces[i], gap, bias)
            if hit is not None and hit[0] < score[i] - 1e-9:
                score[i], sh, gx, gy = hit
                out[i] = (sh, gx, gy)
            grid.add(sh, gx, gy)
    return out, ""


def _bbox_layouts(pieces: list[Piece], bed: tuple[float, float], gap: float):
    """geom.pack's MaxRects layouts, snapped onto the raster and re-checked.

    Two parts whose inflated bounding boxes do not overlap cannot have overlapping
    outlines, so anything geom.pack fits, this fits - that is what makes the outline
    packer a strict improvement rather than a different set of trade-offs. MaxRects
    packs boxes edge to edge, though, and both the conservative raster and snapping a
    placement outwards onto it cost up to RES mm, so the boxes are inflated by one
    extra cell to buy that back; each placement is still re-tested on the grid and
    the layout dropped if it does not hold.
    """
    usable = (bed[0] - 2 * EDGE_MARGIN, bed[1] - 2 * EDGE_MARGIN)
    infl = [p.brim + gap / 2 + RES for p in pieces]
    s0 = [shape(p.key, 0, p.brim, gap) for p in pieces]
    sizes = [(sh.fw + 2 * i, sh.fh + 2 * i) for sh, i in zip(s0, infl)]
    for keyfn in ORDERINGS.values():
        cand = _maxrects(sizes, usable[0], usable[1], keyfn)
        if cand is None:
            continue
        grid = _Grid(bed, gap)
        out: Layout = []
        for p, i, (x, y, rot) in zip(pieces, infl, cand):
            sh = shape(p.key, 90 if rot else 0, p.brim, gap)
            gx = math.ceil((EDGE_MARGIN + x + i - sh.ex - grid.ox) / RES - 1e-9) - sh.pad
            gy = math.ceil((EDGE_MARGIN + y + i - sh.ey - grid.oy) / RES - 1e-9) - sh.pad
            lo_x, hi_x, lo_y, hi_y = grid.limits(sh)
            if not (lo_x <= gx <= hi_x and lo_y <= gy <= hi_y) or not grid.free(sh, gx, gy):
                out = []
                break
            grid.add(sh, gx, gy)
            out.append((sh, gx, gy))
        if out:
            yield out


def _rank(layout: Layout, bed: tuple[float, float], gap: float) -> tuple[float, float]:
    grid = _Grid(bed, gap)
    xs: list[float] = []
    ys: list[float] = []
    for sh, gx, gy in layout:
        x0, y0 = grid.origin(sh, gx, gy)
        xs += [x0, x0 + sh.fw]
        ys += [y0, y0 + sh.fh]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    # geom.pack's own score: tightest first, then the arrangement whose proportions
    # are closest to the bed's, which keeps travel moves short and heating even.
    return w * h, abs(w / bed[0] - h / bed[1])


def _nest_at(pieces: list[Piece], bed: tuple[float, float], gap: float
             ) -> tuple[Layout | None, str]:
    best: tuple[tuple[float, float, int], Layout] | None = None
    culprit = ""
    n = 0
    for order, bias in STRATEGIES:
        layout, fail = _first_fit(pieces, bed, gap, order, bias)
        if layout is None:
            culprit = culprit or fail
        else:
            r = _rank(layout, bed, gap) + (n,)
            if best is None or r < best[0]:
                best = (r, layout)
        n += 1
    for layout in _bbox_layouts(pieces, bed, gap):
        r = _rank(layout, bed, gap) + (n,)
        if best is None or r < best[0]:
            best = (r, layout)
        n += 1
    return (None, culprit) if best is None else (best[1], "")


def nest(pieces: list[Piece], bed: tuple[float, float] = (BED_X, BED_Y),
         gap: float | None = None) -> float:
    """Place every piece, or raise NoFit. Sets `rot`, `x`, `y`; returns the gap used."""
    if not pieces:
        return GAP if gap is None else gap
    want = GAP if gap is None else gap
    culprit = ""
    for used in (want,) + tuple(g for g in GAP_LADDER if g < want):
        layout, culprit = _nest_at(pieces, bed, used)
        if layout is None:
            continue
        if used != want:
            print(f"nest.py: relaxed the gap to {used:g} mm - the plate does not fit at "
                  f"{want:g} mm", file=sys.stderr)
        grid = _Grid(bed, used)
        for p, (sh, gx, gy) in zip(pieces, layout):
            p.rot = float(sh.rot)
            p.x, p.y = grid.origin(sh, gx, gy)
        _recentre(pieces, bed, used)
        verify(pieces, bed, used)
        return used
    p = next(q for q in pieces if q.name == culprit)
    sh = shape(p.key, 0, p.brim, want)
    raise NoFit(culprit,
                f"{culprit} does not fit: it needs {sh.fw + 2 * p.brim:.1f} x "
                f"{sh.fh + 2 * p.brim:.1f} mm with its brim, and no packing strategy left "
                f"room for it on the {bed[0] - 2 * EDGE_MARGIN:.0f} x "
                f"{bed[1] - 2 * EDGE_MARGIN:.0f} mm of usable bed, down to a "
                f"{min(GAP_LADDER):g} mm gap. Move it to another plate "
                f"(docs/voron-print-plan.md §3) rather than scaling anything down.")


def _recentre(pieces: list[Piece], bed: tuple[float, float], gap: float) -> None:
    """Centre the whole arrangement on the bed, in whole cells so the raster phase -
    and with it the clearance the placer proved - is preserved exactly."""
    ext = [(p.x, p.y, shape(p.key, int(p.rot), p.brim, gap), p.brim) for p in pieces]
    x0 = min(x - b for x, _y, _s, b in ext)
    y0 = min(y - b for _x, y, _s, b in ext)
    x1 = max(x + s.fw + b for x, _y, s, b in ext)
    y1 = max(y + s.fh + b for _x, y, s, b in ext)
    kx = int(round(((bed[0] - (x1 - x0)) / 2 - x0) / RES))
    ky = int(round(((bed[1] - (y1 - y0)) / 2 - y0) / RES))
    kx = max(math.ceil((EDGE_MARGIN - x0) / RES - 1e-9),
             min(kx, math.floor((bed[0] - EDGE_MARGIN - x1) / RES + 1e-9)))
    ky = max(math.ceil((EDGE_MARGIN - y0) / RES - 1e-9),
             min(ky, math.floor((bed[1] - EDGE_MARGIN - y1) / RES + 1e-9)))
    for p in pieces:
        p.x += kx * RES
        p.y += ky * RES


def verify(pieces: list[Piece], bed: tuple[float, float] = (BED_X, BED_Y),
           gap: float | None = None) -> None:
    """Re-derive the layout from the public rot/x/y and assert both invariants: no two
    clearance halos overlap, and every footprint + brim is inside the printable area."""
    g = GAP if gap is None else gap
    grid = _Grid(bed, g)
    for p in pieces:
        sh = shape(p.key, int(p.rot), p.brim, g)
        if (p.x - p.brim < EDGE_MARGIN - 1e-6 or p.y - p.brim < EDGE_MARGIN - 1e-6
                or p.x + sh.fw + p.brim > bed[0] - EDGE_MARGIN + 1e-6
                or p.y + sh.fh + p.brim > bed[1] - EDGE_MARGIN + 1e-6):
            raise NoFit(p.name, f"{p.name} sticks out of the printable area: "
                                f"x {p.x - p.brim:.2f}..{p.x + sh.fw + p.brim:.2f}, "
                                f"y {p.y - p.brim:.2f}..{p.y + sh.fh + p.brim:.2f} mm")
        fx = (p.x - sh.ex - grid.ox) / RES - sh.pad
        fy = (p.y - sh.ey - grid.oy) / RES - sh.pad
        gx, gy = int(round(fx)), int(round(fy))
        if abs(fx - gx) > 1e-6 or abs(fy - gy) > 1e-6:
            raise NoFit(p.name, f"{p.name} is off the {RES} mm raster")
        if not grid.free(sh, gx, gy):
            raise NoFit(p.name, f"{p.name} is closer than {g:g} mm to another outline")
        grid.add(sh, gx, gy)


def pack(pieces: list[Piece], bed: tuple[float, float] = (BED_X, BED_Y)
         ) -> tuple[bool, list[str]]:
    """geom.pack's contract: place every piece, return (fits, [what didn't fit]).

    Sets `rot` (0/90/180/270) and `x`, `y` - the piece's own rotated bbox corner,
    brim excluded - exactly as geom.pack does, so build_plates.py needs no other
    change. Unlike geom.pack, two parts' bounding boxes may overlap: that is the
    whole point. The clearance is checked on the outlines instead, by `verify`.
    """
    try:
        nest(pieces, bed)
    except NoFit as e:
        return False, [str(e)]
    return True, []


# ------------------------------------------------------------------- CLI

def pieces_for(plate_id: str) -> list[Piece]:
    """The plate's membership from plates.py, built exactly as build_plates.build does."""
    from build_plates import hull_and_bbox, source_stl
    from plates import PLATES, brim_for
    out: list[Piece] = []
    for repo, path, qty in PLATES[plate_id]["parts"]:
        rel = source_stl(repo, path)
        hull, bb = hull_and_bbox(rel)
        base = path.rsplit("/", 1)[-1]
        for i in range(qty):
            nm = base if qty == 1 else f"{base}#{i + 1}"
            out.append(Piece(rel, nm, hull, brim_for(path), bb[2]))
    return out


def _committed(plate_id: str) -> tuple[float, float, int]:
    """(bbox w, bbox h, object count) of the committed 3MF's outlines.

    Read the way scripts/render_plate_bins.py reads them - threemf.read_plate, world
    coordinates, so a plate re-arranged in the GUI is measured as it now stands. A
    silhouette's bbox is the XY bbox of its vertices, so the outlines themselves do
    not have to be traced to measure the arrangement.
    """
    import threemf
    plate = threemf.read_plate(ROOT / "plates" / f"{plate_id}.3mf")
    xs = [v[0] for o in plate.objects for v in o.vertices]
    ys = [v[1] for o in plate.objects for v in o.vertices]
    return max(xs) - min(xs), max(ys) - min(ys), len(plate.objects)


def _extent(pieces: list[Piece], gap: float) -> tuple[float, float]:
    ext = [(p.x, p.y, shape(p.key, int(p.rot), p.brim, gap)) for p in pieces]
    return (max(x + s.fw for x, _y, s in ext) - min(x for x, _y, _s in ext),
            max(y + s.fh for _x, y, s in ext) - min(y for _x, y, _s in ext))


def compare(plate_ids: list[str] | None = None) -> int:
    from plates import PLATES
    ids = plate_ids or list(PLATES)
    t_all = time.time()
    print(f"{'plate':8s} {'parts':>5s}  {'committed 3MF':>16s} {'fill':>6s}   "
          f"{'nest.py':>16s} {'fill':>6s} {'delta':>7s} {'gap':>4s} {'fits':>4s} {'s':>5s}")
    rows = []
    for pid in ids:
        t0 = time.time()
        pieces = pieces_for(pid)
        area = sum(footprint_area(p.key) for p in pieces)
        cw, ch, nobj = _committed(pid)
        cur = 100.0 * area / (cw * ch)
        try:
            used = nest(pieces)
            nw, nh = _extent(pieces, used)
            new, fits = 100.0 * area / (nw * nh), True
        except NoFit as e:
            used, nw, nh, new, fits = float("nan"), float("nan"), float("nan"), \
                float("nan"), False
            print(f"  {pid}: {e}", file=sys.stderr)
        secs = time.time() - t0
        note = "" if nobj == len(pieces) else f"  (3MF holds {nobj} objects)"
        print(f"{pid:8s} {len(pieces):5d}  {cw:6.1f} x {ch:7.1f} {cur:5.1f}%   "
              f"{nw:6.1f} x {nh:7.1f} {new:5.1f}% {new - cur:+6.1f} {used:4.0f} "
              f"{'yes' if fits else 'NO':>4s} {secs:5.1f}{note}")
        rows.append((cur, new, fits))
    ok = [r for r in rows if r[2]] or [(0.0, 0.0, True)]
    print(f"\n{len(rows)} plates, {sum(1 for r in rows if r[2])} fit, "
          f"mean outline fill {sum(r[0] for r in ok) / len(ok):.1f}% -> "
          f"{sum(r[1] for r in ok) / len(ok):.1f}%, {time.time() - t_all:.1f} s total")
    return 0 if all(r[2] for r in rows) else 1


def selftest(plate_ids: list[str] | None = None) -> int:
    ids = plate_ids or ["B00-P1", "B01-P1", "B06-P1", "B07-P2", "B08-P1", "B09-P4", "B10-P1"]
    for pid in ids:
        pieces = pieces_for(pid)
        used = nest(pieces)
        verify(pieces, gap=used)          # clearance + on-bed, from the public rot/x/y
        again = pieces_for(pid)
        assert nest(again) == used, f"{pid}: gap not deterministic"
        a = [(p.name, p.rot, round(p.x, 6), round(p.y, 6)) for p in pieces]
        b = [(p.name, p.rot, round(p.x, 6), round(p.y, 6)) for p in again]
        assert a == b, f"{pid}: not deterministic"
        for p in pieces:
            assert p.rot in (0.0, 90.0, 180.0, 270.0), f"{pid}: {p.name} rot {p.rot}"
        w, h = _extent(pieces, used)
        print(f"{pid:8s} {len(pieces):2d} parts  ok: no two outlines closer than {used:g} mm, "
              f"all inside {BED_X:.0f} x {BED_Y:.0f} less {EDGE_MARGIN:g} mm, deterministic; "
              f"arrangement {w:.1f} x {h:.1f} mm")
    print(f"selftest passed on {len(ids)} plates")
    return 0


def main(argv: list[str]) -> int:
    global GAP
    args = [a for a in argv if not a.startswith("--")]
    for a in argv:
        if a.startswith("--gap="):
            GAP = float(a.split("=", 1)[1])
            print(f"# gap {GAP:g} mm between outlines")
    if "--compare" in argv:
        return compare(args or None)
    if "--selftest" in argv:
        return selftest(args or None)
    print(__doc__.strip().rsplit("\n\n", 1)[-1])
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
