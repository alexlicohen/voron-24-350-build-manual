#!/usr/bin/env python3
"""Render step illustrations from the mesh cache built by step_extract.py.

Two products per step:
  a  the selected parts alone, framed on themselves
  b  the same parts in place, surrounding assembly ghosted

Pure numpy orthographic z-buffer rasteriser (no GPU, no display server), then a
matplotlib pass for callout labels. Deterministic: same inputs -> same PNG.
"""
import argparse, json, os, re, sys, time

import numpy as np

# --- camera -----------------------------------------------------------------

def basis(azim_deg, elev_deg, up=(0, 0, 1)):
    """Right/up/forward for an orthographic camera orbiting +Z."""
    a, e = np.radians(azim_deg), np.radians(elev_deg)
    fwd = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
    fwd /= np.linalg.norm(fwd)          # camera -> scene points along -fwd
    up = np.asarray(up, float)
    right = np.cross(up, fwd)
    if np.linalg.norm(right) < 1e-6:
        right = np.array([1.0, 0, 0])
    right /= np.linalg.norm(right)
    upv = np.cross(fwd, right)
    upv /= np.linalg.norm(upv)
    return np.stack([right, upv, fwd])   # rows


def project(v, M, centre, scale, W, H):
    """World -> screen. Returns (n,3): x px, y px (down), depth (larger = far)."""
    c = (v - centre) @ M.T
    x = c[:, 0] * scale + W * 0.5
    y = H * 0.5 - c[:, 1] * scale
    return np.stack([x, y, -c[:, 2]], axis=1)


# --- rasteriser -------------------------------------------------------------

DEPTH_BITS, IDX_BITS = 38, 24
EMPTY = np.int64(1) << 62


def _scatter(keybuf, pix, key):
    np.minimum.at(keybuf, pix, key)


def rasterize(scr, tris, W, H, cull=True, max_span=192):
    """Orthographic z-buffer. Returns int32 (H,W) winning triangle index, -1 empty.

    Triangles larger than `max_span` px are subdivided first: the per-triangle
    scatter is bounded by the bbox, so one screen-filling triangle would
    otherwise cost more than the rest of the scene put together.
    """
    if len(tris) == 0:
        return np.full((H, W), -1, np.int32)
    p0, p1, p2 = scr[tris[:, 0]], scr[tris[:, 1]], scr[tris[:, 2]]
    area = ((p1[:, 0] - p0[:, 0]) * (p2[:, 1] - p0[:, 1])
            - (p2[:, 0] - p0[:, 0]) * (p1[:, 1] - p0[:, 1]))
    keep = np.abs(area) > 1e-9
    if cull:
        keep &= area < 0            # screen y is down: front faces wind negative
    parent = np.flatnonzero(keep)
    if len(parent) == 0:
        return np.full((H, W), -1, np.int32)
    p0, p1, p2 = p0[parent], p1[parent], p2[parent]

    def spans(a, b, c):
        xs = np.stack([a[:, 0], b[:, 0], c[:, 0]], 1)
        ys = np.stack([a[:, 1], b[:, 1], c[:, 1]], 1)
        return xs, ys, np.maximum(xs.max(1) - xs.min(1), ys.max(1) - ys.min(1))

    for _ in range(10):                     # 4-way split until every span fits
        _, _, sp = spans(p0, p1, p2)
        big = sp > max_span
        if not big.any():
            break
        a, b, c = p0[big], p1[big], p2[big]
        ab, bc, ca = (a + b) / 2, (b + c) / 2, (c + a) / 2
        sm = ~big
        p0 = np.concatenate([p0[sm], a, ab, ca, ab])
        p1 = np.concatenate([p1[sm], ab, b, bc, bc])
        p2 = np.concatenate([p2[sm], ca, bc, c, ca])
        pb = parent[big]
        parent = np.concatenate([parent[sm], pb, pb, pb, pb])

    area = ((p1[:, 0] - p0[:, 0]) * (p2[:, 1] - p0[:, 1])
            - (p2[:, 0] - p0[:, 0]) * (p1[:, 1] - p0[:, 1]))
    ok = np.abs(area) > 1e-9
    p0, p1, p2, area, parent = p0[ok], p1[ok], p2[ok], area[ok], parent[ok]
    if len(parent) == 0:
        return np.full((H, W), -1, np.int32)
    if len(parent) >= (1 << IDX_BITS):
        sys.exit(f"{len(parent)} triangles exceeds the {1 << IDX_BITS} index budget")

    xs, ys, _ = spans(p0, p1, p2)
    x0 = np.clip(np.floor(xs.min(1)).astype(np.int64), 0, W - 1)
    x1 = np.clip(np.ceil(xs.max(1)).astype(np.int64), 0, W - 1)
    y0 = np.clip(np.floor(ys.min(1)).astype(np.int64), 0, H - 1)
    y1 = np.clip(np.ceil(ys.max(1)).astype(np.int64), 0, H - 1)
    onscreen = (xs.max(1) >= 0) & (xs.min(1) < W) & (ys.max(1) >= 0) & (ys.min(1) < H)

    zs = np.stack([p0[:, 2], p1[:, 2], p2[:, 2]], 1)
    zlo, zhi = zs.min(), zs.max()
    qz = ((zs - zlo) / max(zhi - zlo, 1e-9) * ((1 << DEPTH_BITS) - 1)).astype(np.int64)

    keybuf = np.full(W * H, EMPTY, np.int64)
    size = np.maximum(x1 - x0 + 1, y1 - y0 + 1)
    lo = 0
    while lo < max_span + 2:
        k = max(1, lo * 2)
        sel = np.flatnonzero(onscreen & (size > lo) & (size <= k))
        lo = k
        if len(sel) == 0:
            continue
        kk = k * k
        ox, oy = np.meshgrid(np.arange(k), np.arange(k))
        ox, oy = ox.ravel(), oy.ravel()
        step = max(1, 6_000_000 // kk)
        for s0 in range(0, len(sel), step):
            sub = sel[s0:s0 + step]
            px = (x0[sub][:, None] + ox[None, :]).ravel()
            py = (y0[sub][:, None] + oy[None, :]).ravel()
            tt = np.repeat(sub, kk)
            m = (px <= np.repeat(x1[sub], kk)) & (py <= np.repeat(y1[sub], kk))
            _tri_scatter(keybuf, px[m], py[m], tt[m], p0, p1, p2, area, qz, W)

    out = np.full(W * H, -1, np.int32)
    hit = keybuf < EMPTY
    out[hit] = parent[(keybuf[hit] & ((1 << IDX_BITS) - 1)).astype(np.int64)]
    return out.reshape(H, W)


def _tri_scatter(keybuf, px, py, tt, p0, p1, p2, area, qz, W):
    if len(px) == 0:
        return
    cx, cy = px + 0.5, py + 0.5
    a0, a1, a2 = p0[tt], p1[tt], p2[tt]
    ar = area[tt]
    w0 = ((a1[:, 0] - cx) * (a2[:, 1] - cy) - (a2[:, 0] - cx) * (a1[:, 1] - cy)) / ar
    w1 = ((a2[:, 0] - cx) * (a0[:, 1] - cy) - (a0[:, 0] - cx) * (a2[:, 1] - cy)) / ar
    w2 = 1.0 - w0 - w1
    inside = (w0 >= -1e-9) & (w1 >= -1e-9) & (w2 >= -1e-9)
    if not inside.any():
        return
    px, py, tt = px[inside], py[inside], tt[inside]
    w0, w1, w2 = w0[inside], w1[inside], w2[inside]
    q = qz[tt]
    z = (w0 * q[:, 0] + w1 * q[:, 1] + w2 * q[:, 2]).astype(np.int64)
    np.clip(z, 0, (1 << DEPTH_BITS) - 1, out=z)
    key = (z << IDX_BITS) | tt.astype(np.int64)
    np.minimum.at(keybuf, py * W + px, key)


# --- shading ----------------------------------------------------------------

LIGHTS = [(np.array([0.42, -0.62, 0.66]), 0.62),
          (np.array([-0.60, 0.35, 0.45]), 0.22)]


def shade(verts, tris, colours):
    """Flat per-triangle RGB, float (n,3)."""
    a, b, c = verts[tris[:, 0]], verts[tris[:, 1]], verts[tris[:, 2]]
    n = np.cross(b - a, c - a)
    ln = np.linalg.norm(n, axis=1, keepdims=True)
    n = n / np.maximum(ln, 1e-12)
    lit = np.full(len(tris), 0.30)
    for d, w in LIGHTS:
        lit += w * np.abs(n @ (d / np.linalg.norm(d)))
    lit = np.clip(lit, 0, 1.25)[:, None]
    return np.clip(colours * lit, 0, 1)


# --- scene ------------------------------------------------------------------

def box_mesh(x0, y0, z0, x1, y1, z1):
    v = np.array([[x, y, z] for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)],
                 dtype=np.float32)
    f = np.array([[0,1,3],[0,3,2],[4,7,5],[4,6,7],[0,4,5],[0,5,1],
                  [2,3,7],[2,7,6],[0,2,6],[0,6,4],[1,5,7],[1,7,3]], dtype=np.int32)
    return v, f


PALETTE = [(0.87, 0.36, 0.10), (0.13, 0.42, 0.71), (0.17, 0.55, 0.30),
           (0.62, 0.20, 0.60), (0.85, 0.65, 0.05), (0.75, 0.15, 0.22),
           (0.10, 0.55, 0.60), (0.45, 0.32, 0.20)]
GHOST_RGB = np.array([0.55, 0.58, 0.62])

# "no triangle here" in the part-id buffer. It must not collide with a real part
# id, and schematic boxes are numbered -1, -2, ... — using -1 for empty made the
# first box of every image indistinguishable from the background, so its callout
# anchored on white space and its silhouette got no outline.
NO_PART = -(1 << 30)


class Scene:
    def __init__(self, cache):
        self.index = json.load(open(os.path.join(cache, "index.json")))
        self.npz = np.load(os.path.join(cache, "meshes.npz"), mmap_mode="r")
        self.by_id = {r["id"]: r for r in self.index}
        self.boxes = {}

    def add_box(self, spec):
        """spec = 'x0,y0,z0,x1,y1,z1' -> a negative pseudo-part id."""
        c = [float(x) for x in spec.split(",")]
        pid = -(len(self.boxes) + 1)
        self.boxes[pid] = box_mesh(*c)
        self.by_id[pid] = dict(id=pid, name="(schematic)", path="(schematic box)",
                               bbox=[min(c[0], c[3]), min(c[1], c[4]), min(c[2], c[5]),
                                     max(c[0], c[3]), max(c[1], c[4]), max(c[2], c[5])])
        return pid

    def mesh(self, pid):
        if pid < 0:
            return self.boxes[pid]
        return np.asarray(self.npz[f"v{pid}"]), np.asarray(self.npz[f"t{pid}"])

    def select(self, patterns):
        """Each pattern is either a regex on the part path, or `ids:1,2,3`.

        Prefer the id form in a committed manifest: Fusion instance suffixes
        (`(3)`, `(Mirror)`) are the only thing separating otherwise identical
        parts, so a regex that resolves correctly today can silently resolve to
        a different instance after a CAD re-export. Ids are stable for a given
        cache; re-resolve them from the `resolve:` regex when the cache is
        rebuilt.
        """
        out = []
        for pat in patterns:
            if pat.startswith("ids:"):
                hits = [int(x) for x in pat[4:].replace(" ", "").split(",") if x]
                missing = [i for i in hits if i not in self.by_id]
                if missing:
                    sys.exit(f"ids not in this cache: {missing} "
                             f"(cache has {len(self.index)} parts) - rebuild "
                             f"steps.yml ids from the entry's resolve: regex")
            else:
                rx = re.compile(pat, re.I)
                hits = [r["id"] for r in self.index if rx.search(r["path"])]
            if not hits:
                sys.exit(f"no part matched /{pat}/")
            out.append((pat, hits))
        return out


def gather(scene, ids, shift=None):
    V, T, off = [], [], 0
    owner = []
    for pid in ids:
        v, t = scene.mesh(pid)
        if shift is not None and pid in shift:
            v = v + np.asarray(shift[pid], np.float32)
        V.append(v); T.append(t + off); owner.append(np.full(len(t), pid))
        off += len(v)
    if not V:
        return (np.zeros((0, 3), np.float32), np.zeros((0, 3), np.int32),
                np.zeros(0, np.int32))
    return np.concatenate(V), np.concatenate(T), np.concatenate(owner)


def clip_to_box(V, T, own, lo, hi):
    """Trim a triangle soup to a box. Triangles that straddle the boundary are
    subdivided first, so the framed context does not end in ragged slabs where a
    coarsely tessellated panel happened to cross the edge."""
    TV = V[T].astype(np.float32)
    for _ in range(5):
        bl, bh = TV.min(1), TV.max(1)
        out = (bh < lo).any(1) | (bl > hi).any(1)
        TV, own = TV[~out], own[~out]
        if not len(TV):
            break
        bl, bh = TV.min(1), TV.max(1)
        cross = ((bl < lo) | (bh > hi)).any(1)
        if not cross.any():
            break
        B = TV[cross]
        a, b, c = B[:, 0], B[:, 1], B[:, 2]
        ab, bc, ca = (a + b) / 2, (b + c) / 2, (c + a) / 2
        TV = np.concatenate([TV[~cross],
                             np.stack([a, ab, ca], 1), np.stack([ab, b, bc], 1),
                             np.stack([ca, bc, c], 1), np.stack([ab, bc, ca], 1)])
        own = np.concatenate([own[~cross], np.tile(own[cross], 4)])
    if len(TV):
        cen = TV.mean(1)
        keep = ((cen >= lo) & (cen <= hi)).all(1)
        TV, own = TV[keep], own[keep]
    return (TV.reshape(-1, 3),
            np.arange(len(TV) * 3, dtype=np.int32).reshape(-1, 3), own)


def compose(scr, tris, colours, W, H, cull=True):
    """Returns (rgb float (H,W,3), mask bool, tri index (H,W))."""
    tid = rasterize(scr, tris, W, H, cull=cull)
    rgb = np.ones((H, W, 3))
    m = tid >= 0
    rgb[m] = colours[tid[m]]
    return rgb, m, tid


def outline(idbuf, mask, strength=0.55):
    """Dark seam where the owning part changes or the silhouette ends."""
    e = np.zeros(idbuf.shape, bool)
    for ax in (0, 1):
        d = np.diff(idbuf, axis=ax) != 0
        pad = [(0, 0), (0, 0)]
        pad[ax] = (1, 0)
        e |= np.pad(d, pad)
        pad[ax] = (0, 1)
        e |= np.pad(d, pad)
    return e & (mask | np.roll(mask, 1, 0) | np.roll(mask, 1, 1))


def render(scene, sel, out_png, mode, azim, elev, W, H, ss, ctx_scale,
           labels=True, title=None, subtitle=None, note=None, shift=None,
           ghost_exclude=None, frame=None):
    t0 = time.time()
    hi_ids = [i for _, ids in sel for i in ids]
    hi_col = {}
    for k, (_, ids) in enumerate(sel):
        for i in ids:
            hi_col[i] = PALETTE[k % len(PALETTE)]

    M = basis(azim, elev)
    hb = np.array([scene.by_id[i]["bbox"] for i in hi_ids], float)
    if shift:
        for k, i in enumerate(hi_ids):
            if i in shift:
                hb[k] += np.tile(shift[i], 2)
    lo, hi = hb[:, :3].min(0), hb[:, 3:].max(0)
    centre = (lo + hi) / 2

    # framing: project the corners of the region of interest
    if frame is not None:
        region = np.stack([frame[:3], frame[3:]])
        centre = region.mean(0)
    elif mode == "a":
        region = np.stack([lo, hi])
    else:
        half = np.full(3, (hi - lo).max() / 2 * ctx_scale + 10.0)
        region = np.stack([centre - half, centre + half])
    corners = np.array([[region[i, 0], region[j, 1], region[k, 2]]
                        for i in (0, 1) for j in (0, 1) for k in (0, 1)])
    cc = (corners - centre) @ M.T
    ext = np.maximum(np.abs(cc[:, :2]).max(0), 1e-3)
    Ws, Hs = W * ss, H * ss
    scale = min(Ws / (2 * ext[0] * 1.16), Hs / (2 * ext[1] * 1.16))

    # highlight layer
    V, T, own = gather(scene, hi_ids, shift)
    base = np.array([hi_col[o] for o in own])
    scr = project(V, M, centre, scale, Ws, Hs)
    rgb, mask, tid = compose(scr, T, shade(V, T, base), Ws, Hs)
    idbuf = np.where(tid >= 0, own[np.clip(tid, 0, None)], NO_PART)

    img = np.ones((Hs, Ws, 3))
    if mode == "b":
        keep = set(hi_ids)
        ctx = []
        r0, r1 = region[0] - 30, region[1] + 30
        for r in scene.index:
            if r["id"] in keep:
                continue
            if ghost_exclude and ghost_exclude.search(r["path"]):
                continue
            b = np.array(r["bbox"], float)
            if (b[3:] < r0).any() or (b[:3] > r1).any():
                continue
            ctx.append(r["id"])
        if ctx:
            Vc, Tc, ownc = gather(scene, ctx)
            Vc, Tc, ownc = clip_to_box(Vc, Tc, ownc, region[0] - 4, region[1] + 4)
            sc = project(Vc, M, centre, scale, Ws, Hs)
            gcol = np.tile(GHOST_RGB, (len(Tc), 1))
            grgb, gmask, gtid = compose(sc, Tc, shade(Vc, Tc, gcol), Ws, Hs)
            gid = np.where(gtid >= 0, ownc[np.clip(gtid, 0, None)], NO_PART)
            ge = outline(gid, gmask)
            grgb[ge] *= 0.45
            alpha = np.where(ge, 0.45, np.where(gmask, 0.20, 0.0))[:, :, None]
            img = img * (1 - alpha) + grgb * alpha
        print(f"    ghost: {len(ctx)} context parts", flush=True)

    e = outline(idbuf, mask)
    rgb[e] *= 0.45
    img = np.where((mask | e)[:, :, None], rgb, img)

    # box-downsample to the requested size (antialiasing)
    img = img.reshape(H, ss, W, ss, 3).mean(axis=(1, 3))
    idsmall = idbuf[::ss, ::ss]

    _annotate(img, idsmall, sel, hi_col, out_png, W, H, labels, title, subtitle, note)
    print(f"    wrote {out_png}  [{time.time()-t0:.1f}s]", flush=True)


def _annotate(img, idsmall, sel, hi_col, out_png, W, H, labels, title, subtitle, note):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patheffects import withStroke

    dpi = 100
    fig = plt.figure(figsize=(W / dpi, H / dpi), dpi=dpi, facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
    ax.imshow(np.clip(img, 0, 1), interpolation="nearest")
    ax.set_xlim(0, W); ax.set_ylim(H, 0)

    if labels:
        anchors = []
        for pat, ids in sel:
            ys, xs = np.where(np.isin(idsmall, ids))
            if len(xs) == 0:
                continue
            mx, my = np.median(xs), np.median(ys)
            j = np.argmin((xs - mx) ** 2 + (ys - my) ** 2)   # a pixel really on the part
            anchors.append((float(xs[j]), float(ys[j]), pat, hi_col[ids[0]]))
        left = sorted([a for a in anchors if a[0] < W / 2], key=lambda a: a[1])
        right = sorted([a for a in anchors if a[0] >= W / 2], key=lambda a: a[1])
        for col, xs_lab, ha in ((left, 16, "left"), (right, W - 16, "right")):
            n = len(col)
            for i, (ax_, ay, txt, c) in enumerate(col):
                ly = H * (0.10 + 0.80 * ((i + 0.5) / max(n, 1)))
                ax.annotate(txt, xy=(ax_, ay), xytext=(xs_lab, ly), ha=ha,
                            va="center", fontsize=11.5, color="#101010",
                            arrowprops=dict(arrowstyle="-", color=c, lw=1.6,
                                            shrinkA=0, shrinkB=3,
                                            connectionstyle="arc3,rad=0.08"),
                            bbox=dict(boxstyle="round,pad=0.34", fc="white",
                                      ec=c, lw=1.3, alpha=0.94),
                            path_effects=[withStroke(linewidth=0, foreground="w")])
    y = 22
    if title:
        ax.text(14, y, title, fontsize=15, weight="bold", color="#101010", va="top")
        y += 24
    if subtitle:
        ax.text(14, y, subtitle, fontsize=11, color="#3a3a3a", va="top")
    if note:
        ax.text(W - 14, H - 12, note, fontsize=8.5, color="#8a8a8a",
                ha="right", va="bottom")
    fig.savefig(out_png, dpi=dpi, facecolor="white")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    ap.add_argument("--out", required=True, help="path stem; -a.png / -b.png appended")
    ap.add_argument("--select", action="append", required=True,
                    help="regex on the part path; repeat, one colour each")
    ap.add_argument("--label", action="append", default=[],
                    help="callout text, one per --select (default: the regex)")
    ap.add_argument("--box", action="append", default=[],
                    help="schematic box 'x0,y0,z0,x1,y1,z1:Label' for hardware the "
                         "Voron CAD does not model (LDO/mod parts)")
    ap.add_argument("--offset", action="append", default=[],
                    help="'dx,dy,dz' per --select, in order; shifts that selection")
    ap.add_argument("--azim", type=float, default=-55.0)
    ap.add_argument("--elev", type=float, default=26.0)
    ap.add_argument("--width", type=int, default=1200)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--ss", type=int, default=2, help="supersample factor")
    ap.add_argument("--context-scale", type=float, default=4.0)
    ap.add_argument("--title", default=None)
    ap.add_argument("--subtitle-a", default=None)
    ap.add_argument("--subtitle-b", default=None)
    ap.add_argument("--note", default="Voron 2.4r2 CAD (VoronDesign, GPL-3.0) @ de7e89d")
    ap.add_argument("--only", choices=["a", "b"], default=None)
    ap.add_argument("--frame-a", default=None,
                    help="'x0,y0,z0,x1,y1,z1': frame view (a) on this box instead "
                         "of on the selected parts' own extent")
    ap.add_argument("--ghost-exclude", default=None,
                    help="regex: keep these out of the ghosted context layer")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    scene = Scene(args.cache)
    if args.list:
        for r in scene.index:
            print(r["id"], r["tris"], r["path"])
        return
    sel = scene.select(args.select)
    shift = {}
    for k, off in enumerate(args.offset):
        if off.strip() and k < len(sel):
            d = [float(x) for x in off.split(",")]
            for i in sel[k][1]:
                shift[i] = d
    for i, (pat, ids) in enumerate(sel):
        txt = args.label[i] if i < len(args.label) else pat
        sel[i] = (txt, ids)
        print(f"  {txt}: {len(ids)} part(s) -> "
              f"{[scene.by_id[j]['name'] for j in ids][:6]}", flush=True)

    for spec in args.box:
        geom, _, lbl = spec.rpartition(":")
        pids = [scene.add_box(g) for g in geom.split(";") if g.strip()]
        sel.append((lbl, pids))
        print(f"  {lbl}: {len(pids)} schematic box(es)", flush=True)

    for mode, sub in (("a", args.subtitle_a), ("b", args.subtitle_b)):
        if args.only and args.only != mode:
            continue
        render(scene, sel, f"{args.out}-{mode}.png", mode, args.azim, args.elev,
               args.width, args.height, args.ss, args.context_scale,
               title=args.title, subtitle=sub, note=args.note, shift=shift,
               ghost_exclude=(re.compile(args.ghost_exclude, re.I)
                              if args.ghost_exclude else None),
               frame=(np.array([float(x) for x in args.frame_a.split(",")])
                      if args.frame_a and mode == "a" else None))


if __name__ == "__main__":
    main()
