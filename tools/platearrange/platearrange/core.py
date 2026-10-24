"""The placer: every collision-free translation at once (FFT correlation), scored like a
centre-aligned PrusaSlicer arrange, first-fit-decreasing over as many beds as needed.

See README.md § Objective for the score and why it approximates PrusaSlicer.
"""
from __future__ import annotations

import hashlib
import itertools
import math
import os
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Hashable, List, Optional, Sequence, Tuple

import numpy as np

from .footprint import (Kernels, MeshFootprints, irfft2, mesh_triangles, next_fast_len,
                        rfft2, rot_cs, rotation_set)

# Score weights per objective (README § Objective), all terms normalised to the usable bed:
#   area  pile bounding-box area / bed area        side  larger pile side / that bed side
#   dist  part bbox centre to the sink / diagonal  rad   pile radius (farthest part+brim
#                                                        bbox corner from the sink) / half diagonal
OBJECTIVES = {
    "box": dict(area=1.0, side=0.5, dist=0.1, rad=0.0),     # tight rectangle
    "round": dict(area=1.0, side=0.5, dist=0.1, rad=0.5),   # tight and round about the centre
}
# Strategy choice and improvement moves: the pile's area and side terms, plus the mean and
# the largest distance of part centres from the pile centre.
SELECT = dict(area=1.0, side=0.5, mean=0.1, max=0.5)

ORDERINGS = ("area", "longest")
SINKS = ("centre", "corner")
# Tried only when the full rotation search needs more beds than the parts' area requires:
# a greedy that may turn every part can wall off the slot a later part needed (PrusaSlicer's
# own arrange does not rotate unless asked).
FALLBACK_ROTATIONS = ((0.0, 180.0), (0.0, 90.0, 180.0, 270.0))


class NoFit(RuntimeError):
    """An item cannot be placed even on an empty bed (or within max_beds)."""

    def __init__(self, item_id, msg: str):
        super().__init__(msg)
        self.item_id = item_id


@dataclass
class Item:
    """One part. `vertices` (n, 3) and `triangles` (m, 3) in any frame; `brim` is the
    outer brim reach in mm (PrusaSlicer: brim_width + brim_separation). Items whose
    meshes are identical up to an XY translation share footprints automatically; `key`
    overrides that detection."""
    id: Any
    vertices: Any
    triangles: Any
    brim: float = 0.0
    key: Optional[Hashable] = None


@dataclass(frozen=True)
class Placement:
    """World XY = R(rot_deg) @ item XY + (x, y): rotation about the item frame's origin
    (counter-clockwise, about Z), then translation. Z is never touched."""
    item_id: Any
    bed: int
    rot_deg: float
    x: float
    y: float

    def apply(self, xy) -> np.ndarray:
        xy = np.asarray(xy, dtype=np.float64)
        c, s = rot_cs(self.rot_deg)
        out = np.empty(xy.shape[:-1] + (2,))
        out[..., 0] = c * xy[..., 0] - s * xy[..., 1] + self.x
        out[..., 1] = s * xy[..., 0] + c * xy[..., 1] + self.y
        return out


@dataclass
class Result:
    placements: List[Placement]          # input order
    beds: int
    strategy: str
    piles: List[Tuple[float, float, float, float]]   # per bed, part+brim bbox
    params: dict = field(default_factory=dict)


# ------------------------------------------------------------------ caches

_FP: "OrderedDict[tuple, MeshFootprints]" = OrderedDict()
_K: "OrderedDict[tuple, Kernels]" = OrderedDict()
CACHE_BYTES = 1_500_000_000


def clear_cache() -> None:
    _FP.clear()
    _K.clear()


def _trim() -> None:
    total = sum(v.nbytes() for v in _FP.values()) + sum(v.nbytes() for v in _K.values())
    while total > CACHE_BYTES and (_K or _FP):
        d = _K if _K else _FP
        _k, v = d.popitem(last=False)
        total -= v.nbytes()


class _Prep:
    """One item ready to place."""
    __slots__ = ("index", "item", "offset", "fp", "k", "area", "longest")


def _prepare(items: Sequence[Item], rotations, res, first_layer, gap, need_brim_mask):
    preps = []
    for idx, it in enumerate(items):
        tri3 = mesh_triangles(it.vertices, it.triangles)
        ox = float(tri3[:, :, 0].min())
        oy = float(tri3[:, :, 1].min())
        tri3 = tri3.copy()
        tri3[:, :, 0] -= ox
        tri3[:, :, 1] -= oy
        mkey = it.key
        if mkey is None:   # copies of one mesh (any XY position) share footprints
            mkey = hashlib.sha1(np.ascontiguousarray(np.round(tri3, 9)).tobytes()).hexdigest()
        fkey = (mkey, res, first_layer, tuple(rotations))
        fp = _FP.get(fkey)
        if fp is None:
            fp = _FP[fkey] = MeshFootprints(tri3, rotations, res, first_layer)
        kkey = fkey + (gap, round(float(it.brim), 9), need_brim_mask)
        k = _K.get(kkey)
        if k is None:
            k = _K[kkey] = Kernels(fp, gap, float(it.brim), need_brim_mask)
        p = _Prep()
        p.index, p.item, p.offset, p.fp, p.k = idx, it, (ox, oy), fp, k
        p.area = fp.area
        r0 = rotations.index(0.0)
        e = k.ext[r0]
        p.longest = float(max(e[2] - e[0], e[3] - e[1]))
        preps.append(p)
    _trim()
    return preps


# ------------------------------------------------------------------ bed

def _point_seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    L = dx * dx + dy * dy
    t = np.clip(((px - ax) * dx + (py - ay) * dy) / np.where(L > 0, L, 1.0), 0.0, 1.0)
    return np.hypot(px - (ax + t * dx), py - (ay + t * dy))


class _Bed:
    def __init__(self, bed, edge_margin: float, res: float, gap: float, exclusions):
        poly = None
        if len(bed) == 2 and np.isscalar(bed[0]):
            x0, y0, x1, y1 = 0.0, 0.0, float(bed[0]), float(bed[1])
        else:
            pts = np.asarray(bed, dtype=np.float64).reshape(-1, 2)
            x0, y0 = pts.min(axis=0)
            x1, y1 = pts.max(axis=0)
            on_box = np.all((np.isclose(pts[:, 0], x0) | np.isclose(pts[:, 0], x1))
                            & (np.isclose(pts[:, 1], y0) | np.isclose(pts[:, 1], y1)))
            if not (len(pts) == 4 and on_box):
                poly = pts
        self.x0, self.y0, self.x1, self.y1 = float(x0), float(y0), float(x1), float(y1)
        self.m = float(edge_margin)
        self.poly = poly
        self.res = res
        P = int(math.ceil(gap / 2.0 / res)) + 4
        self.X0 = self.x0 - P * res
        self.Y0 = self.y0 - P * res
        self.Gw = int(math.ceil((self.x1 - self.x0) / res - 1e-9)) + 2 * P
        self.Gh = int(math.ceil((self.y1 - self.y0) / res - 1e-9)) + 2 * P
        self.fs = (next_fast_len(self.Gh), next_fast_len(self.Gw))
        self.uw = self.x1 - self.x0 - 2 * self.m
        self.uh = self.y1 - self.y0 - 2 * self.m
        if self.uw <= 0 or self.uh <= 0:
            raise ValueError("edge margin leaves no usable bed")
        self.cx = (self.x0 + self.x1) / 2.0
        self.cy = (self.y0 + self.y1) / 2.0
        self.excl = np.zeros((self.Gh, self.Gw), dtype=bool)
        for ex in exclusions or ():
            a, b, c, d = (float(v) for v in ex)
            i0 = max(0, int(math.floor((min(a, c) - self.X0) / res - 1e-9)))
            i1 = min(self.Gw - 1, int(math.floor((max(a, c) - self.X0) / res + 1e-9)))
            j0 = max(0, int(math.floor((min(b, d) - self.Y0) / res - 1e-9)))
            j1 = min(self.Gh - 1, int(math.floor((max(b, d) - self.Y0) / res + 1e-9)))
            if i0 <= i1 and j0 <= j1:
                self.excl[j0:j1 + 1, i0:i1 + 1] = True
        self.has_excl = bool(self.excl.any())
        self.forbid = None
        if poly is not None:
            # a brim cell is allowed only if all of it is inside the polygon by >= margin
            ii = self.X0 + (np.arange(self.Gw) + 0.5) * res
            jj = self.Y0 + (np.arange(self.Gh) + 0.5) * res
            px, py = np.meshgrid(ii, jj)
            inside = np.zeros(px.shape, dtype=bool)
            dmin = np.full(px.shape, np.inf)
            n = len(poly)
            for k in range(n):
                ax, ay = poly[k]
                bx, by = poly[(k + 1) % n]
                cond = (ay > py) != (by > py)
                xint = ax + (py - ay) * (bx - ax) / np.where(by != ay, by - ay, 1.0)
                inside ^= cond & (px < xint)
                dmin = np.minimum(dmin, _point_seg_dist(px, py, ax, ay, bx, by))
            self.forbid = ~(inside & (dmin >= self.m + res * math.sqrt(0.5) + 1e-9))
            self.forbid_hat = rfft2(self.forbid[None].astype(np.float32), self.fs)

    def ranges(self, k: Kernels, r: int):
        """Grid positions (gx_lo, gx_hi, gy_lo, gy_hi) where rotation r's brim is on the bed."""
        res = self.res
        mask = k.masks[r]
        ki0, kj0 = k.org[r]
        e = k.ext[r]
        gx_lo = math.ceil(ki0 + (self.x0 + self.m - e[0] - self.X0) / res - 1e-9)
        gx_hi = math.floor(ki0 + (self.x1 - self.m - e[2] - self.X0) / res + 1e-9)
        gy_lo = math.ceil(kj0 + (self.y0 + self.m - e[1] - self.Y0) / res - 1e-9)
        gy_hi = math.floor(kj0 + (self.y1 - self.m - e[3] - self.Y0) / res + 1e-9)
        gx_lo, gy_lo = max(gx_lo, 0), max(gy_lo, 0)
        gx_hi = min(gx_hi, self.Gw - mask.shape[1])
        gy_hi = min(gy_hi, self.Gh - mask.shape[0])
        return int(gx_lo), int(gx_hi), int(gy_lo), int(gy_hi)

    def translation(self, k: Kernels, r: int, gx: int, gy: int):
        ki0, kj0 = k.org[r]
        return self.X0 + (gx - ki0) * self.res, self.Y0 + (gy - kj0) * self.res


class _BedState:
    def __init__(self, bed: _Bed):
        self.occ = bed.excl.copy()
        self.pile: Optional[List[float]] = None
        self.rad = 0.0                  # farthest placed bbox corner from the sink
        self.placed: List[tuple] = []   # (prep, r, gx, gy)


# ------------------------------------------------------------------ placement

def _bed_ok_maps(bed: _Bed, k: Kernels):
    """For a polygon bed: per rotation, where the brim raster avoids forbidden cells."""
    if bed.forbid is None:
        return None
    out = []
    masks = k.brim_masks
    for r, (m, bi0, bj0) in enumerate(masks):
        hat = rfft2(m[None].astype(np.float32), bed.fs)
        corr = irfft2(np.conj(hat) * bed.forbid_hat, bed.fs)[0]
        out.append((corr, bi0 - k.org[r][0], bj0 - k.org[r][1]))
    return out


class _KHat:
    """conj(FFT) of an item's clearance rasters, computed per rotation on first use."""

    def __init__(self, bed: _Bed, k: Kernels):
        self.bed, self.k = bed, k
        self.kh = max(m.shape[0] for m in k.masks)
        self.kw = max(m.shape[1] for m in k.masks)
        self.cache: dict = {}

    def get(self, rs) -> np.ndarray:
        need = [r for r in rs if r not in self.cache]
        if need:
            stack = np.zeros((len(need), self.kh, self.kw), dtype=np.float32)
            for i, r in enumerate(need):
                m = self.k.masks[r]
                stack[i, :m.shape[0], :m.shape[1]] = m
            hat = np.conj(rfft2(stack, self.bed.fs))
            for i, r in enumerate(need):
                self.cache[r] = hat[i]
        return np.stack([self.cache[r] for r in rs])


def _kernel_hat(bed: _Bed, k: Kernels) -> _KHat:
    return _KHat(bed, k)


CHUNK = 12   # rotations correlated per FFT batch, in lower-bound order


def _best_on(bed: _Bed, st: _BedState, p: _Prep, khat, okmaps, sink, w, allowed=None):
    k = p.k
    R = len(k.masks)
    res = bed.res
    empty = not st.occ.any()
    ohat = None if empty else rfft2(st.occ[None].astype(np.float32), bed.fs)
    corr: dict = {}
    A = bed.uw * bed.uh
    diag = math.hypot(bed.uw, bed.uh)
    sx, sy = sink
    W_AREA, W_SIDE, W_DIST, W_RAD = w["area"], w["side"], w["dist"], w["rad"]
    best = (math.inf, -1, 0, 0)
    cand = []
    for r in (range(R) if allowed is None else allowed):
        gx_lo, gx_hi, gy_lo, gy_hi = bed.ranges(k, r)
        if gx_lo > gx_hi or gy_lo > gy_hi:
            continue
        e = k.ext[r]
        ki0, kj0 = k.org[r]
        tx = bed.X0 + (np.arange(gx_lo, gx_hi + 1) - ki0) * res
        ty = bed.Y0 + (np.arange(gy_lo, gy_hi + 1) - kj0) * res
        ix0, ix1 = e[0] + tx, e[2] + tx
        iy0, iy1 = e[1] + ty, e[3] + ty
        if st.pile is None:
            W, H = ix1 - ix0, iy1 - iy0
        else:
            px0, py0, px1, py1 = st.pile
            W = np.maximum(px1, ix1) - np.minimum(px0, ix0)
            H = np.maximum(py1, iy1) - np.minimum(py0, iy0)
        dx = (ix0 + ix1) / 2.0 - sx
        dy = (iy0 + iy1) / 2.0 - sy
        fx = np.maximum(np.abs(ix0 - sx), np.abs(ix1 - sx))     # farthest corner from the sink
        fy = np.maximum(np.abs(iy0 - sy), np.abs(iy1 - sy))
        lb = (W_AREA * W.min() * H.min() / A + W_SIDE * max(W.min() / bed.uw, H.min() / bed.uh)
              + W_DIST * math.hypot(np.abs(dx).min(), np.abs(dy).min()) / diag
              + W_RAD * max(st.rad, math.hypot(fx.min(), fy.min())) / (diag / 2))
        cand.append((lb, r, gx_lo, gx_hi, gy_lo, gy_hi, W, H, dx, dy, fx, fy))
    cand.sort(key=lambda c: (c[0], c[1]))
    f32 = np.float32
    for ci, (lb, r, gx_lo, gx_hi, gy_lo, gy_hi, W, H, dx, dy, fx, fy) in enumerate(cand):
        if lb >= best[0]:
            break
        if ohat is not None:
            if r not in corr:   # correlate the next chunk of still-promising rotations
                rs = [c[1] for c in cand[ci:ci + CHUNK] if c[0] < best[0]]
                out = irfft2(khat.get(rs) * ohat, bed.fs)
                corr.update(zip(rs, out))
            feas = corr[r][gy_lo:gy_hi + 1, gx_lo:gx_hi + 1] < 0.5
        else:
            feas = None
        if okmaps is not None:
            cm, oi, oj = okmaps[r]
            ok = cm[gy_lo + oj:gy_hi + oj + 1, gx_lo + oi:gx_hi + oi + 1] < 0.5
            feas = ok if feas is None else (feas & ok)
        if feas is not None and not feas.any():
            continue
        score = np.multiply.outer((H * (W_AREA / A)).astype(f32), W.astype(f32))
        tmp = np.maximum.outer((H * (W_SIDE / bed.uh)).astype(f32), (W * (W_SIDE / bed.uw)).astype(f32))
        score += tmp
        np.add.outer((dy * dy).astype(f32), (dx * dx).astype(f32), out=tmp)
        np.sqrt(tmp, out=tmp)
        tmp *= f32(W_DIST / diag)
        score += tmp
        if W_RAD > 0:
            np.add.outer((fy * fy).astype(f32), (fx * fx).astype(f32), out=tmp)
            np.sqrt(tmp, out=tmp)
            np.maximum(tmp, f32(st.rad), out=tmp)
            tmp *= f32(W_RAD / (diag / 2))
            score += tmp
        if feas is not None:
            score[~feas] = np.inf
        flat = int(np.argmin(score))
        val = float(score.flat[flat])
        if val < best[0] or (val == best[0] and r < best[1]):
            j, i = divmod(flat, gx_hi - gx_lo + 1)
            best = (val, r, gx_lo + i, gy_lo + j)
    if best[1] < 0:
        return None
    _, r, gx, gy = best
    m = k.masks[r]
    window = st.occ[gy:gy + m.shape[0], gx:gx + m.shape[1]]
    if (window & m).any():   # an FFT rounding slip; never seen, but never trusted
        raise AssertionError(f"internal: correlation missed a collision for item {p.item.id}")
    return best


def _commit(bed: _Bed, st: _BedState, p: _Prep, r: int, gx: int, gy: int, sink):
    m = p.k.masks[r]
    st.occ[gy:gy + m.shape[0], gx:gx + m.shape[1]] |= m
    tx, ty = bed.translation(p.k, r, gx, gy)
    e = p.k.ext[r]
    box = [e[0] + tx, e[1] + ty, e[2] + tx, e[3] + ty]
    if st.pile is None:
        st.pile = box
    else:
        st.pile = [min(st.pile[0], box[0]), min(st.pile[1], box[1]),
                   max(st.pile[2], box[2]), max(st.pile[3], box[3])]
    st.placed.append((p, r, gx, gy))
    fx = max(abs(box[0] - sink[0]), abs(box[2] - sink[0]))
    fy = max(abs(box[1] - sink[1]), abs(box[3] - sink[1]))
    st.rad = max(st.rad, math.hypot(fx, fy))


def _box(bed: _Bed, p: _Prep, r: int, gx: int, gy: int):
    tx, ty = bed.translation(p.k, r, gx, gy)
    e = p.k.ext[r]
    return (e[0] + tx, e[1] + ty, e[2] + tx, e[3] + ty)


def pile_metric(bed: _Bed, placed) -> float:
    """Translation-invariant pile quality (lower is better, weights in SELECT): pile bbox
    area / bed area, larger pile side / bed side, and the mean (/ bed diagonal) and largest
    (/ half diagonal) distance of the parts' bbox centres from the pile's bbox centre.
    Picks between strategies and accepts improvement moves."""
    boxes = np.array([_box(bed, p, r, gx, gy) for p, r, gx, gy in placed])
    x0, y0 = boxes[:, 0].min(), boxes[:, 1].min()
    x1, y1 = boxes[:, 2].max(), boxes[:, 3].max()
    W, H = x1 - x0, y1 - y0
    cx = (boxes[:, 0] + boxes[:, 2]) / 2 - (x0 + x1) / 2
    cy = (boxes[:, 1] + boxes[:, 3]) / 2 - (y0 + y1) / 2
    diag = math.hypot(bed.uw, bed.uh)
    d = np.hypot(cx, cy)
    return float(SELECT["area"] * W * H / (bed.uw * bed.uh)
                 + SELECT["side"] * max(W / bed.uw, H / bed.uh)
                 + SELECT["mean"] * d.mean() / diag + SELECT["max"] * d.max() / (diag / 2))


def _rebuild(bed: _Bed, placed, sink) -> "_BedState":
    st = _BedState(bed)
    for p, r, gx, gy in placed:
        _commit(bed, st, p, r, gx, gy, sink)
    return st


def _improve(bed: _Bed, st: "_BedState", sink, w, passes: int, allowed=None):
    """Lift each part (last placed first) and re-place it on the rest of the pile; keep
    the move only if the pile metric improves. Deterministic."""
    for _ in range(passes):
        moved = False
        for idx in reversed(range(len(st.placed))):
            placed = st.placed
            if len(placed) < 2:
                break
            p, r, gx, gy = placed[idx]
            others = placed[:idx] + placed[idx + 1:]
            rest = _rebuild(bed, others, sink)
            hit = _best_on(bed, rest, p, _kernel_hat(bed, p.k), _bed_ok_maps(bed, p.k), sink, w,
                           allowed)
            if hit is None or (hit[1], hit[2], hit[3]) == (r, gx, gy):
                continue
            cand = placed[:idx] + [(p, hit[1], hit[2], hit[3])] + placed[idx + 1:]
            if pile_metric(bed, cand) < pile_metric(bed, placed) - 1e-12:
                st = _rebuild(bed, cand, sink)
                moved = True
        if not moved:
            break
    return st


def _order(preps, ordering: str):
    if ordering == "area":
        key = lambda p: (-p.area, -p.longest, p.index)
    elif ordering == "longest":
        key = lambda p: (-p.longest, -p.area, p.index)
    else:
        raise ValueError(f"unknown ordering {ordering!r}")
    return sorted(preps, key=key)


def _run(bed: _Bed, preps, ordering, sink_name, objective, max_beds, improve: int,
         allowed=None):
    w = OBJECTIVES[objective]
    sink = (bed.cx, bed.cy) if sink_name == "centre" else (bed.x0 + bed.m, bed.y0 + bed.m)
    states: List[_BedState] = []
    for p in _order(preps, ordering):
        khat = _kernel_hat(bed, p.k)
        okmaps = _bed_ok_maps(bed, p.k)
        placed = False
        for st in states:
            hit = _best_on(bed, st, p, khat, okmaps, sink, w, allowed)
            if hit is not None:
                _commit(bed, st, p, *hit[1:], sink)
                placed = True
                break
        if not placed:
            if max_beds is not None and len(states) >= max_beds:
                raise NoFit(p.item.id, f"item {p.item.id!r} does not fit within {max_beds} bed(s)")
            st = _BedState(bed)
            hit = _best_on(bed, st, p, khat, okmaps, sink, w, allowed)
            if hit is None:
                e = p.k.ext[0]
                raise NoFit(p.item.id,
                            f"item {p.item.id!r} ({e[2] - e[0]:.1f} x {e[3] - e[1]:.1f} mm with "
                            f"brim) does not fit on an empty "
                            f"{bed.uw:.0f} x {bed.uh:.0f} mm usable bed in any rotation")
            _commit(bed, st, p, *hit[1:], sink)
            states.append(st)
    if improve:
        states = [_improve(bed, st, sink, w, improve, allowed) for st in states]
    return states


def _recentre(bed: _Bed, st: _BedState):
    """Shift (dx, dy) that centres the pile's bbox on the bed, clamped to the bed."""
    px0, py0, px1, py1 = st.pile
    lo_x, hi_x = bed.x0 + bed.m - px0, bed.x1 - bed.m - px1
    lo_y, hi_y = bed.y0 + bed.m - py0, bed.y1 - bed.m - py1
    dx = min(max(bed.cx - (px0 + px1) / 2.0, lo_x), hi_x)
    dy = min(max(bed.cy - (py0 + py1) / 2.0, lo_y), hi_y)
    if not bed.has_excl and bed.forbid is None:
        return dx, dy, 0, 0
    # exclusions or a polygon bed: whole cells only, re-checked against the fixed cells
    res = bed.res
    cx_lo, cx_hi = math.ceil(lo_x / res - 1e-9), math.floor(hi_x / res + 1e-9)
    cy_lo, cy_hi = math.ceil(lo_y / res - 1e-9), math.floor(hi_y / res + 1e-9)
    for t in (1.0, 0.75, 0.5, 0.25, 0.0):
        cx = min(max(int(round(t * dx / res)), cx_lo), cx_hi)
        cy = min(max(int(round(t * dy / res)), cy_lo), cy_hi)
        if cx == 0 and cy == 0:
            return 0.0, 0.0, 0, 0
        ok = True
        for p, r, gx, gy in st.placed:
            m = p.k.masks[r]
            x, y = gx + cx, gy + cy
            if x < 0 or y < 0 or y + m.shape[0] > bed.Gh or x + m.shape[1] > bed.Gw:
                ok = False
                break
            if (bed.excl[y:y + m.shape[0], x:x + m.shape[1]] & m).any():
                ok = False
                break
            if bed.forbid is not None:
                bm, bi0, bj0 = p.k.brim_masks[r]
                oi, oj = bi0 - p.k.org[r][0], bj0 - p.k.org[r][1]
                yy, xx = y + oj, x + oi
                if (yy < 0 or xx < 0 or yy + bm.shape[0] > bed.Gh or xx + bm.shape[1] > bed.Gw
                        or (bed.forbid[yy:yy + bm.shape[0], xx:xx + bm.shape[1]] & bm).any()):
                    ok = False
                    break
        if ok:
            return cx * res, cy * res, cx, cy
    return 0.0, 0.0, 0, 0


# ------------------------------------------------------------------ public API

def arrange_detailed(items: Sequence[Item], bed=(250.0, 220.0), gap: float = 6.0,
                     rot_step: float = 5.0, edge_margin: float = 0.0, exclusions=(),
                     res: float = 0.5, first_layer: float = 0.2,
                     orderings: Sequence[str] = ORDERINGS, sinks: Sequence[str] = SINKS,
                     objectives: Sequence[str] = tuple(OBJECTIVES),
                     max_beds: Optional[int] = None,
                     rotations: Optional[Sequence[float]] = None,
                     improve: int = 0, threads: Optional[int] = None) -> Result:
    """Arrange `items` on as few beds as possible; see `arrange`."""
    if not items:
        return Result([], 0, "", [], {})
    if gap < 0 or res <= 0 or edge_margin < 0:
        raise ValueError("gap and edge_margin must be >= 0, res > 0")
    rots = sorted({round(float(a) % 360.0, 9) for a in rotations}) if rotations is not None \
        else rotation_set(rot_step)
    if 0.0 not in rots:
        rots = [0.0] + rots
    b = _Bed(bed, edge_margin, res, gap, exclusions)
    preps = _prepare(items, rots, res, first_layer, gap, b.forbid is not None)

    best = None
    last_err: Optional[NoFit] = None
    n = 0
    lower = max(1, math.ceil(sum(p.area for p in preps) / (b.uw * b.uh) - 1e-9))
    families = [("", None)]
    for fam in FALLBACK_ROTATIONS:
        allowed = [rots.index(a) for a in fam if a in rots]
        families.append(("/rot" + "-".join(f"{a:g}" for a in fam), allowed))
    tasks = list(itertools.product(objectives, orderings, sinks))

    def one(task, allowed):
        objective, ordering, sink = task
        try:
            return _run(b, preps, ordering, sink, objective, max_beds, improve, allowed)
        except NoFit as e:
            return e

    nthreads = max(1, min(len(tasks), threads if threads else (os.cpu_count() or 2) // 2))
    with ThreadPoolExecutor(max_workers=nthreads) as pool:
        for fi, (tag, allowed) in enumerate(families):
            if fi > 0 and best is not None and best[0][0] <= lower:
                break           # the full rotation search already reached the area bound
            # strategies are independent; results are taken in task order (deterministic)
            for (objective, ordering, sink), states in zip(
                    tasks, pool.map(lambda t: one(t, allowed), tasks)):
                if isinstance(states, NoFit):
                    last_err = states
                    n += 1
                    continue
                score = (len(states), round(sum(pile_metric(b, s.placed) for s in states), 9), n)
                if best is None or score < best[0]:
                    best = (score, f"{objective}/{ordering}/{sink}{tag}", states)
                n += 1
    if best is None:
        raise last_err  # type: ignore[misc]

    _, name, states = best
    out: List[Optional[Placement]] = [None] * len(items)
    piles = []
    for bi, st in enumerate(states):
        dx, dy, _cx, _cy = _recentre(b, st)
        for p, r, gx, gy in st.placed:
            tx, ty = b.translation(p.k, r, gx, gy)
            deg = p.fp.rotations[r]
            c, s = rot_cs(deg)
            ox, oy = p.offset
            phx, phy = p.fp.phase[r]
            x = tx + phx + dx - (c * ox - s * oy)
            y = ty + phy + dy - (s * ox + c * oy)
            out[p.index] = Placement(p.item.id, bi, float(deg), float(x), float(y))
        q = st.pile
        piles.append((q[0] + dx, q[1] + dy, q[2] + dx, q[3] + dy))
    params = dict(gap=gap, rot_step=rot_step, rotations=len(rots), edge_margin=edge_margin,
                  res=res, first_layer=first_layer, exclusions=[list(e) for e in exclusions or ()])
    return Result(out, len(states), name, piles, params)  # type: ignore[arg-type]


def arrange(items: Sequence[Item], bed=(250.0, 220.0), gap: float = 6.0,
            rot_step: float = 5.0, edge_margin: float = 0.0, exclusions=(),
            res: float = 0.5, **kw) -> List[Placement]:
    """Place every item; return one Placement per item, in input order.

    bed          (w, h) for [0, w] x [0, h], or a polygon [(x, y), ...] in bed coordinates
    gap          mm of clear bed between any two parts' brims (PrusaSlicer default 6)
    rot_step     Z rotations tried every rot_step degrees; 0/90/180/270 always included
    edge_margin  mm between any part or brim and the bed edge
    exclusions   [(x0, y0, x1, y1), ...] bed areas no part, brim or clearance may touch
    res          raster cell in mm; a measured gap is never below `gap` and exceeds it by
                 at most about one cell per part
    Extra keywords go to arrange_detailed: first_layer (mm of base the brim grows from),
    orderings, sinks, objectives, max_beds, rotations (explicit angle list), improve (passes),
    threads (strategies run in parallel; default half the CPUs; the result does not depend on it).
    """
    return arrange_detailed(items, bed, gap, rot_step, edge_margin, exclusions, res,
                            **kw).placements
