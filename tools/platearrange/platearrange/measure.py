"""Exact 2D measurement of an arrangement, independent of the placer's raster.

A part's top-down region is the union of its projected triangles (S); its brim is the
first-layer region F grown by the brim reach b. Distances are computed on the projected
outline segments with vector geometry (no raster), so they can check the placer:

  d(part_i + brim_i, part_j + brim_j) = min(d(Si,Sj), d(Si,Fj)-bj, d(Fi,Sj)-bi, d(Fi,Fj)-bi-bj)

Outline segments are every projected triangle edge except those shared by exactly two
triangles that lie on opposite sides of it (interior edges); this keeps every boundary edge
of the union, so the minimum over segment pairs is the exact set distance when the sets are
disjoint. Overlap (crossing outlines, or one set inside the other) gives distance 0.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

import numpy as np

from .footprint import clip_below, mesh_triangles, rasterise, rotate_xy


@dataclass
class Region:
    tris: np.ndarray      # (n, 3, 2)
    segs: np.ndarray      # (k, 2, 2)
    bbox: Tuple[float, float, float, float]


def _region(tri2: np.ndarray) -> Region:
    q = np.round(tri2 * 1e6).astype(np.int64)
    p_idx = np.array([0, 1, 2])
    a = q[:, p_idx]                 # (n,3,2) edge start
    b = q[:, (p_idx + 1) % 3]       # edge end
    c = tri2[:, (p_idx + 2) % 3]    # opposite vertex (float)
    af = tri2[:, p_idx]
    bf = tri2[:, (p_idx + 1) % 3]
    side = np.sign((bf[..., 0] - af[..., 0]) * (c[..., 1] - af[..., 1])
                   - (bf[..., 1] - af[..., 1]) * (c[..., 0] - af[..., 0]))
    a = a.reshape(-1, 2)
    b = b.reshape(-1, 2)
    side = side.reshape(-1)
    swap = (a[:, 0] > b[:, 0]) | ((a[:, 0] == b[:, 0]) & (a[:, 1] > b[:, 1]))
    lo = np.where(swap[:, None], b, a)
    hi = np.where(swap[:, None], a, b)
    side = np.where(swap, -side, side)
    keys = np.concatenate([lo, hi], axis=1)
    _u, inv, cnt = np.unique(keys, axis=0, return_inverse=True, return_counts=True)
    inv = inv.reshape(-1)
    ssum = np.zeros(len(cnt))
    np.add.at(ssum, inv, side)
    sabs = np.zeros(len(cnt))
    np.add.at(sabs, inv, np.abs(side))
    interior = (cnt == 2) & (ssum == 0) & (sabs == 2)
    keep_edge = ~interior[inv]
    # one copy of each kept edge
    order = np.argsort(inv, kind="stable")
    seen = np.ones(len(inv), dtype=bool)
    seen[order[1:]] = inv[order[1:]] != inv[order[:-1]]
    take = keep_edge & seen
    flat_a = tri2[:, p_idx].reshape(-1, 2)
    flat_b = tri2[:, (p_idx + 1) % 3].reshape(-1, 2)
    segs = np.stack([flat_a[take], flat_b[take]], axis=1)
    xs, ys = tri2[..., 0], tri2[..., 1]
    return Region(tri2, segs, (float(xs.min()), float(ys.min()), float(xs.max()), float(ys.max())))


@dataclass
class Part:
    S: Region
    F: Region
    brim: float

    def extents(self) -> Tuple[float, float, float, float]:
        s, f, b = self.S.bbox, self.F.bbox, self.brim
        if b <= 0:
            return s
        return (min(s[0], f[0] - b), min(s[1], f[1] - b), max(s[2], f[2] + b), max(s[3], f[3] + b))


def part_from_mesh(vertices, triangles, brim: float = 0.0, first_layer: float = 0.2) -> Part:
    tri3 = mesh_triangles(vertices, triangles)
    zmin = float(tri3[:, :, 2].min())
    fl = clip_below(tri3, zmin + max(first_layer, 1e-6))
    return Part(_region(tri3[:, :, :2]), _region(fl[:, :, :2]), float(brim))


def placed_part(part: Part, rot_deg: float, x: float, y: float) -> Part:
    def mv(r: Region) -> Region:
        t = rotate_xy(r.tris, rot_deg) + (x, y)
        s = rotate_xy(r.segs, rot_deg) + (x, y)
        return Region(t, s, (float(t[..., 0].min()), float(t[..., 1].min()),
                             float(t[..., 0].max()), float(t[..., 1].max())))
    return Part(mv(part.S), mv(part.F), part.brim)


# ------------------------------------------------------------------ distances

def _bbox_dist(a, b) -> float:
    dx = max(0.0, a[0] - b[2], b[0] - a[2])
    dy = max(0.0, a[1] - b[3], b[1] - a[3])
    return math.hypot(dx, dy)


def _near(segs: np.ndarray, box, d: float) -> np.ndarray:
    lo = segs.min(axis=1)
    hi = segs.max(axis=1)
    dx = np.maximum(0.0, np.maximum(lo[:, 0] - box[2], box[0] - hi[:, 0]))
    dy = np.maximum(0.0, np.maximum(lo[:, 1] - box[3], box[1] - hi[:, 1]))
    return segs[dx * dx + dy * dy <= d * d]


def _pt_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    L = dx * dx + dy * dy
    t = np.clip(((px - ax) * dx + (py - ay) * dy) / np.where(L > 0, L, 1.0), 0.0, 1.0)
    return np.hypot(px - ax - t * dx, py - ay - t * dy)


def _segset_min(A: np.ndarray, B: np.ndarray) -> float:
    best = math.inf
    chunk = max(1, 2_000_000 // max(1, len(B)))
    bx0, by0, bx1, by1 = B[:, 0, 0], B[:, 0, 1], B[:, 1, 0], B[:, 1, 1]
    for i in range(0, len(A), chunk):
        a = A[i:i + chunk]
        ax0, ay0 = a[:, 0, 0][:, None], a[:, 0, 1][:, None]
        ax1, ay1 = a[:, 1, 0][:, None], a[:, 1, 1][:, None]
        d = np.minimum(np.minimum(_pt_seg(ax0, ay0, bx0, by0, bx1, by1),
                                  _pt_seg(ax1, ay1, bx0, by0, bx1, by1)),
                       np.minimum(_pt_seg(bx0, by0, ax0, ay0, ax1, ay1),
                                  _pt_seg(bx1, by1, ax0, ay0, ax1, ay1)))
        # proper crossings
        def orient(px, py, qx, qy, rx, ry):
            return np.sign((qx - px) * (ry - py) - (qy - py) * (rx - px))
        o1 = orient(ax0, ay0, ax1, ay1, bx0, by0)
        o2 = orient(ax0, ay0, ax1, ay1, bx1, by1)
        o3 = orient(bx0, by0, bx1, by1, ax0, ay0)
        o4 = orient(bx0, by0, bx1, by1, ax1, ay1)
        cross = (o1 * o2 < 0) & (o3 * o4 < 0)
        d = np.where(cross, 0.0, d)
        best = min(best, float(d.min()))
        if best == 0.0:
            break
    return best


def _inside(pt, tris: np.ndarray) -> bool:
    """Point in (or on) any triangle of positive projected area. Zero-area triangles are
    segments or points; their edges are outline segments, so the distance test sees them."""
    px, py = pt
    a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
    area2 = (b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) - (b[:, 1] - a[:, 1]) * (c[:, 0] - a[:, 0])
    keep = np.abs(area2) > 1e-12
    a, b, c = a[keep], b[keep], c[keep]

    def cr(p, q):
        return (q[:, 0] - p[:, 0]) * (py - p[:, 1]) - (q[:, 1] - p[:, 1]) * (px - p[:, 0])
    d1, d2, d3 = cr(a, b), cr(b, c), cr(c, a)
    neg = (d1 < 0) | (d2 < 0) | (d3 < 0)
    pos = (d1 > 0) | (d2 > 0) | (d3 > 0)
    return bool(np.any(~(neg & pos)))


def region_distance(X: Region, Y: Region, upper: float = math.inf) -> float:
    """Exact distance between two regions; 0 when they overlap. If the distance exceeds
    `upper`, some value > upper is returned."""
    lb = _bbox_dist(X.bbox, Y.bbox)
    if lb > upper:
        return lb
    if lb == 0.0:
        if (len(Y.segs) and _inside(tuple(Y.segs[0, 0]), X.tris)) or \
                (len(X.segs) and _inside(tuple(X.segs[0, 0]), Y.tris)):
            return 0.0
    cap = upper if math.isfinite(upper) else lb + 2.0
    while True:
        a = _near(X.segs, Y.bbox, cap)
        b = _near(Y.segs, X.bbox, cap)
        d = _segset_min(a, b) if len(a) and len(b) else math.inf
        if d <= cap:
            return d          # every segment pair within cap was kept: exact
        if math.isfinite(upper):
            return d if math.isfinite(d) else cap + 1.0
        cap *= 2.0


def part_distance(P: Part, Q: Part, upper: float = math.inf) -> float:
    """Distance between part+brim regions (0 if they touch or overlap)."""
    best = math.inf
    terms = [(P.S, Q.S, 0.0)]
    if Q.brim > 0:
        terms.append((P.S, Q.F, Q.brim))
    if P.brim > 0:
        terms.append((P.F, Q.S, P.brim))
    if P.brim > 0 and Q.brim > 0:
        terms.append((P.F, Q.F, P.brim + Q.brim))
    for X, Y, off in terms:
        lim = min(best, upper)
        d = region_distance(X, Y, lim + off) - off
        best = min(best, max(d, 0.0))
        if best <= 0.0:
            return 0.0
    return best


def min_gap(parts: Sequence[Part]) -> Tuple[float, Optional[Tuple[int, int]]]:
    """Smallest part+brim to part+brim distance over all pairs, and that pair."""
    ext = [p.extents() for p in parts]
    pairs = sorted((_bbox_dist(ext[i], ext[j]), i, j)
                   for i in range(len(parts)) for j in range(i + 1, len(parts)))
    best, who = math.inf, None
    for lb, i, j in pairs:
        if lb >= best:
            break
        d = part_distance(parts[i], parts[j], best)
        if d < best:
            best, who = d, (i, j)
        if best == 0.0:
            break
    return best, who


def edge_clearance(parts: Sequence[Part], bed) -> float:
    """Smallest distance from any part+brim to the edge of a rectangular bed
    ((w, h) or (x0, y0, x1, y1)); negative when something is off the bed."""
    if len(bed) == 2:
        x0, y0, x1, y1 = 0.0, 0.0, float(bed[0]), float(bed[1])
    else:
        x0, y0, x1, y1 = (float(v) for v in bed)
    best = math.inf
    for p in parts:
        e = p.extents()
        best = min(best, e[0] - x0, e[1] - y0, x1 - e[2], y1 - e[3])
    return best


def pile_bbox(parts: Sequence[Part]) -> Tuple[float, float, float, float]:
    ext = np.array([p.extents() for p in parts])
    return (float(ext[:, 0].min()), float(ext[:, 1].min()),
            float(ext[:, 2].max()), float(ext[:, 3].max()))


def centroid(part: Part, res: float = 0.25) -> Tuple[float, float]:
    """Area centroid of the silhouette (raster at `res`; a summary, not a clearance)."""
    m, i0, j0 = rasterise(part.S.tris, res)
    jj, ii = np.nonzero(m)
    return (float((ii.mean() + i0 + 0.5) * res), float((jj.mean() + j0 + 0.5) * res))
