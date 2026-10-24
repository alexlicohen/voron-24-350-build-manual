"""Top-down footprints of a mesh: rotation about Z, first-layer clip, conservative raster, dilation.

Cell convention: at resolution `res`, global cell (i, j) of a frame is the closed square
[i*res, (i+1)*res] x [j*res, (j+1)*res]. A raster is a bool array `m[j - j0, i - i0]` plus
its integer origin (i0, j0), so rasters of one frame can be combined without resampling.

Conservative means every cell the closed geometry touches is set: the true footprint is a
subset of the union of the set cells, so a clearance measured between rasters is never
larger than the real one.
"""
from __future__ import annotations

import math
from typing import Optional, Tuple

import numpy as np

try:  # scipy is optional: faster, multi-threaded, float32 FFTs
    import scipy.fft as _sfft
except Exception:  # pragma: no cover - exercised only without scipy
    _sfft = None

TOL = 1e-9  # mm: geometry that only touches a cell boundary (within TOL) does not set the
            # neighbouring cell; the closed cell on the other side already covers it


# ------------------------------------------------------------------ FFT helpers

def next_fast_len(n: int) -> int:
    if _sfft is not None:
        return int(_sfft.next_fast_len(int(n), real=True))
    m = int(n)
    while True:  # 5-smooth
        k = m
        for p in (2, 3, 5):
            while k % p == 0:
                k //= p
        if k == 1:
            return m
        m += 1


def rfft2(a: np.ndarray, s: Tuple[int, int]) -> np.ndarray:
    if _sfft is not None:
        return _sfft.rfft2(a.astype(np.float32, copy=False), s=s, axes=(-2, -1), workers=-1)
    return np.fft.rfft2(a.astype(np.float64, copy=False), s=s, axes=(-2, -1))


def irfft2(a: np.ndarray, s: Tuple[int, int]) -> np.ndarray:
    if _sfft is not None:
        return _sfft.irfft2(a, s=s, axes=(-2, -1), workers=-1)
    return np.fft.irfft2(a, s=s, axes=(-2, -1))


# ------------------------------------------------------------------ rotation

def rot_cs(deg: float) -> Tuple[float, float]:
    """cos, sin of a Z rotation; exact for multiples of 90 degrees."""
    k = int(round(deg / 90.0))
    if abs(deg - 90.0 * k) < 1e-12:
        return ((1.0, 0.0), (0.0, 1.0), (-1.0, 0.0), (0.0, -1.0))[k % 4]
    r = math.radians(deg)
    return math.cos(r), math.sin(r)


def rotate_xy(xy: np.ndarray, deg: float) -> np.ndarray:
    """Rotate points (..., 2) counter-clockwise about the origin."""
    c, s = rot_cs(deg)
    x = xy[..., 0]
    y = xy[..., 1]
    return np.stack([c * x - s * y, s * x + c * y], axis=-1)


def rotation_set(rot_step: float) -> list:
    """Every multiple of rot_step in [0, 360), plus 0/90/180/270 exactly."""
    angles = {0.0, 90.0, 180.0, 270.0}
    if rot_step and rot_step > 0:
        n = int(math.floor(360.0 / rot_step + 1e-9))
        for k in range(n):
            a = round(k * rot_step, 9)
            if a < 360.0 - 1e-9:
                angles.add(a)
    return sorted(angles)


# ------------------------------------------------------------------ mesh -> 2D triangles

def mesh_triangles(vertices, triangles) -> np.ndarray:
    v = np.asarray(vertices, dtype=np.float64).reshape(-1, 3)
    t = np.asarray(triangles, dtype=np.int64).reshape(-1, 3)
    if len(t) == 0:
        raise ValueError("mesh has no triangles")
    return v[t]  # (n, 3, 3)


def clip_below(tri3: np.ndarray, zcut: float) -> np.ndarray:
    """The parts of 3D triangles with z <= zcut, as triangles (m, 3, 3)."""
    z = tri3[:, :, 2]
    below = z <= zcut
    nb = below.sum(axis=1)
    out = [tri3[nb == 3]]
    part = tri3[(nb == 1) | (nb == 2)]
    if len(part):
        npart = nb[(nb == 1) | (nb == 2)]
        order = np.argsort(part[:, :, 2], axis=1, kind="stable")
        q = np.take_along_axis(part, order[:, :, None], axis=1)
        a, b, c = q[:, 0], q[:, 1], q[:, 2]

        def cut(p, r):
            t = (zcut - p[:, 2]) / (r[:, 2] - p[:, 2])
            return p + t[:, None] * (r - p)

        one = npart == 1
        if one.any():
            a1, b1, c1 = a[one], b[one], c[one]
            out.append(np.stack([a1, cut(a1, b1), cut(a1, c1)], axis=1))
        two = ~one
        if two.any():
            a2, b2, c2 = a[two], b[two], c[two]
            pbc, pac = cut(b2, c2), cut(a2, c2)
            out.append(np.stack([a2, b2, pbc], axis=1))
            out.append(np.stack([a2, pbc, pac], axis=1))
    return np.concatenate(out, axis=0)


def silhouette_tris(tri3: np.ndarray) -> np.ndarray:
    """Projected triangles (n, 3, 2), dropping those with zero projected area.

    For a closed mesh the dropped (vertical) faces project onto segments that the
    neighbouring non-vertical faces already cover, so the union is unchanged. If that
    would drop everything (a flat, open mesh), all triangles are kept.
    """
    xy = tri3[:, :, :2]
    d1 = xy[:, 1] - xy[:, 0]
    d2 = xy[:, 2] - xy[:, 0]
    a2 = np.abs(d1[:, 0] * d2[:, 1] - d1[:, 1] * d2[:, 0])
    keep = a2 > 1e-12
    return xy[keep] if keep.any() else xy


# ------------------------------------------------------------------ rasteriser

def rasterise(tri: np.ndarray, res: float) -> Tuple[np.ndarray, int, int]:
    """Conservative raster of the union of 2D triangles (n, 3, 2): (mask, i0, j0).

    A triangle sets every closed cell it overlaps; one that merely touches a cell's
    boundary line (within TOL) is covered by the cell on the other side of that line.
    """
    xs = tri[:, :, 0]
    ys = tri[:, :, 1]
    xmin, xmax = xs.min(axis=1), xs.max(axis=1)
    ymin, ymax = ys.min(axis=1), ys.max(axis=1)
    inv = 1.0 / res
    i0 = np.floor((xmin + TOL) * inv).astype(np.int64)
    i1 = np.maximum(np.ceil((xmax - TOL) * inv).astype(np.int64) - 1, i0)
    j0 = np.floor((ymin + TOL) * inv).astype(np.int64)
    j1 = np.maximum(np.ceil((ymax - TOL) * inv).astype(np.int64) - 1, j0)
    gi0, gj0 = int(i0.min()), int(j0.min())
    w = int(i1.max()) - gi0 + 1
    h = int(j1.max()) - gj0 + 1

    one = j0 == j1
    rows, los, his = [j0[one]], [i0[one]], [i1[one]]

    multi = np.nonzero(~one)[0]
    if len(multi):
        n = (j1 - j0 + 1)[multi]
        rep = np.repeat(multi, n)
        start = np.cumsum(n) - n
        off = np.arange(int(n.sum()), dtype=np.int64) - np.repeat(start, n)
        j = j0[rep] + off
        yl = j * res
        yh = (j + 1) * res
        lo = np.full(len(rep), np.inf)
        hi = np.full(len(rep), -np.inf)
        t = tri[rep]
        for e in range(3):
            x0, y0 = t[:, e, 0], t[:, e, 1]
            x1, y1 = t[:, (e + 1) % 3, 0], t[:, (e + 1) % 3, 1]
            a = np.maximum(yl, np.minimum(y0, y1))
            b = np.minimum(yh, np.maximum(y0, y1))
            ok = a <= b
            dy = y1 - y0
            flat = dy == 0.0
            sdy = np.where(flat, 1.0, dy)
            xa = np.where(flat, x0, x0 + (a - y0) / sdy * (x1 - x0))
            xb = np.where(flat, x1, x0 + (b - y0) / sdy * (x1 - x0))
            lo = np.where(ok, np.minimum(lo, np.minimum(xa, xb)), lo)
            hi = np.where(ok, np.maximum(hi, np.maximum(xa, xb)), hi)
        good = lo <= hi
        il = np.floor((lo[good] + TOL) * inv).astype(np.int64)
        ih = np.ceil((hi[good] - TOL) * inv).astype(np.int64) - 1
        rr = rep[good]
        il = np.clip(il, i0[rr], i1[rr])
        ih = np.clip(np.maximum(ih, il), i0[rr], i1[rr])
        rows.append(j[good])
        los.append(il)
        his.append(ih)

    r = np.concatenate(rows) - gj0
    lo_i = np.concatenate(los) - gi0
    hi_i = np.concatenate(his) - gi0 + 1
    width = w + 1
    size = h * width
    diff = (np.bincount(r * width + lo_i, minlength=size)
            - np.bincount(r * width + hi_i, minlength=size))
    mask = np.cumsum(diff.reshape(h, width), axis=1)[:, :w] > 0
    return mask, gi0, gj0


# ------------------------------------------------------------------ dilation

def structuring_element(rho: float, res: float) -> np.ndarray:
    """Cell offsets (dx, dy) whose closed squares are closer than `rho` to each other.

    If two parts are closer than rho_a + rho_b, an open patch of bed is within rho_a of
    one and rho_b of the other; the cell holding it is then within (strictly less than)
    rho of a set cell of each raster. So rasters dilated by this element that share no
    cell prove the parts are >= rho_a + rho_b apart. The centre cell is always in, so
    with rho = 0 the parts may touch but never overlap.
    """
    r = rho / res
    R = 1 + int(math.ceil(r))
    d = np.arange(-R, R + 1)
    gx = np.maximum(np.abs(d) - 1, 0)
    dd = gx[None, :] ** 2 + gx[:, None] ** 2
    se = dd < r * r - 1e-9
    se[R, R] = True
    # trim empty border rows/cols (keeps it centred)
    while se.shape[0] > 1 and not se[0].any() and not se[-1].any() \
            and not se[:, 0].any() and not se[:, -1].any():
        se = se[1:-1, 1:-1]
    return se


def dilate_many(masks, origins, rho: float, res: float):
    """Dilate several rasters by the same structuring element (batched FFT).

    Returns [(mask, i0, j0)] with each origin moved out by the element's radius.
    """
    se = structuring_element(rho, res)
    R = se.shape[0] // 2
    if R == 0 or not masks:
        return [(m.copy(), i, j) for m, (i, j) in zip(masks, origins)]
    hmax = max(m.shape[0] for m in masks) + 2 * R
    wmax = max(m.shape[1] for m in masks) + 2 * R
    s = (next_fast_len(hmax), next_fast_len(wmax))
    out = []
    se_hat = rfft2(se[None].astype(np.float32), s)
    batch = 16
    for b0 in range(0, len(masks), batch):
        chunk = masks[b0:b0 + batch]
        stack = np.zeros((len(chunk), hmax - 2 * R, wmax - 2 * R), dtype=np.float32)
        for k, m in enumerate(chunk):
            stack[k, :m.shape[0], :m.shape[1]] = m
        conv = irfft2(rfft2(stack, s) * se_hat, s)
        for k, m in enumerate(chunk):
            h, w = m.shape
            dm = conv[k, :h + 2 * R, :w + 2 * R] > 0.5
            i0, j0 = origins[b0 + k]
            out.append((dm, i0 - R, j0 - R))
    return out


def union(a, b):
    """Union of two (mask, i0, j0) rasters of the same frame."""
    ma, ia, ja = a
    mb, ib, jb = b
    i0, j0 = min(ia, ib), min(ja, jb)
    i1 = max(ia + ma.shape[1], ib + mb.shape[1])
    j1 = max(ja + ma.shape[0], jb + mb.shape[0])
    out = np.zeros((j1 - j0, i1 - i0), dtype=bool)
    out[ja - j0:ja - j0 + ma.shape[0], ia - i0:ia - i0 + ma.shape[1]] |= ma
    out[jb - j0:jb - j0 + mb.shape[0], ib - i0:ib - i0 + mb.shape[1]] |= mb
    return out, i0, j0


# ------------------------------------------------------------------ prepared mesh

class MeshFootprints:
    """Per-rotation silhouette and first-layer rasters of one mesh.

    Rotation r works in its own frame s = R(deg) . v + phase[r], where the phase puts the
    rotated silhouette's bbox corner exactly on a cell corner (0, 0): a part then costs
    ceil(width / res) cells, never one more. `extents[r]` / `fl_extents[r]` are the exact
    (x0, y0, x1, y1) of the silhouette / first layer in that frame.
    """

    def __init__(self, tri3: np.ndarray, rotations, res: float, first_layer: float):
        self.res = res
        self.rotations = list(rotations)
        zmin = float(tri3[:, :, 2].min())
        sil = silhouette_tris(tri3)
        fl3 = clip_below(tri3, zmin + max(first_layer, 1e-6))
        fl = silhouette_tris(fl3) if len(fl3) else sil
        self.sil_masks, self.sil_org, self.fl_masks, self.fl_org = [], [], [], []
        ext, flext, phase = [], [], []
        for deg in self.rotations:
            s = rotate_xy(sil, deg)
            f = rotate_xy(fl, deg)
            ph = (-float(s[..., 0].min()), -float(s[..., 1].min()))
            s = s + ph
            f = f + ph
            phase.append(ph)
            m, i0, j0 = rasterise(s, res)
            self.sil_masks.append(m)
            self.sil_org.append((i0, j0))
            m, i0, j0 = rasterise(f, res)
            self.fl_masks.append(m)
            self.fl_org.append((i0, j0))
            ext.append((s[..., 0].min(), s[..., 1].min(), s[..., 0].max(), s[..., 1].max()))
            flext.append((f[..., 0].min(), f[..., 1].min(), f[..., 0].max(), f[..., 1].max()))
        self.extents = np.array(ext)
        self.fl_extents = np.array(flext)
        self.phase = np.array(phase)
        r0 = self.rotations.index(0.0)
        self.area = float(self.sil_masks[r0].sum()) * res * res
        e = self.extents[r0]
        self.size0 = (float(e[2] - e[0]), float(e[3] - e[1]))

    def nbytes(self) -> int:
        return sum(m.nbytes for m in self.sil_masks) + sum(m.nbytes for m in self.fl_masks)


class Kernels:
    """What the placer moves: per rotation, the clearance raster and brim extents.

    clearance = silhouette (+) gap/2  U  first layer (+) (gap/2 + brim): two items whose
    clearance rasters share no cell are >= gap apart, and their brims >= gap apart.
    brim extents = silhouette extents U first-layer extents grown by brim (exact).
    """

    def __init__(self, fp: MeshFootprints, gap: float, brim: float, need_brim_mask: bool):
        res = fp.res
        half = gap / 2.0
        a = dilate_many(fp.sil_masks, fp.sil_org, half, res)
        if brim > 0:
            b = dilate_many(fp.fl_masks, fp.fl_org, half + brim, res)
            k = [union(x, y) for x, y in zip(a, b)]
        else:
            k = a
        self.masks = [m for m, _i, _j in k]
        self.org = np.array([(i, j) for _m, i, j in k], dtype=np.int64)
        ext = fp.extents.copy()
        if brim > 0:
            fe = fp.fl_extents
            ext[:, 0] = np.minimum(ext[:, 0], fe[:, 0] - brim)
            ext[:, 1] = np.minimum(ext[:, 1], fe[:, 1] - brim)
            ext[:, 2] = np.maximum(ext[:, 2], fe[:, 2] + brim)
            ext[:, 3] = np.maximum(ext[:, 3], fe[:, 3] + brim)
        self.ext = ext
        self.brim_masks: Optional[list] = None
        if need_brim_mask:
            if brim > 0:
                bb = dilate_many(fp.fl_masks, fp.fl_org, brim, res)
                bm = [union((m, i, j), x) for m, (i, j), x in zip(fp.sil_masks, fp.sil_org, bb)]
            else:
                bm = [(m, i, j) for m, (i, j) in zip(fp.sil_masks, fp.sil_org)]
            self.brim_masks = bm

    def nbytes(self) -> int:
        return sum(m.nbytes for m in self.masks)
