#!/usr/bin/env python3
"""Identification renders for every printed part in the Voron manual.

Source of truth for *which* STLs exist and what batch/colour each belongs to
is `slicer/plates.py` (PLATES/REPOS) — the same structure `slicer/*` already
uses to drive slicing, so this script does not re-parse the print plan.

Renderer: pure-Python, headless, deterministic — matplotlib's `Poly3DCollection`
on orthographic 3D axes, shading each face by its normal against a fixed light
direction. `trimesh`/`pyrender` (OSMesa/EGL offscreen) were evaluated first per
the brief, but macOS has no usable OSMesa/EGL and neither package is installed
here (see requirements-render.txt) — this script does not attempt that path,
it goes straight to the matplotlib fallback the brief calls acceptable.

Usage:
    python3 scripts/render_parts.py            # render everything, write MANIFEST.csv
    python3 scripts/render_parts.py --limit 5  # smoke test

Idempotent: re-running overwrites the same PNGs/CSV; nothing is appended.
"""
from __future__ import annotations

import argparse
import csv
import math
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SLICER_DIR = REPO_ROOT / "slicer"
STL_DIR = SLICER_DIR / "stl"
OUT_DIR = REPO_ROOT / "docs" / "manual" / "assets" / "parts"

sys.path.insert(0, str(SLICER_DIR))
import plates  # noqa: E402  (slicer/plates.py — PLATES, REPOS)
import geom  # noqa: E402  (slicer/geom.py — read_stl, bbox; stdlib only)

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402
import numpy as np  # noqa: E402

# --------------------------------------------------------------------- colours

COLOUR_PRIMARY = "#6a6a6a"   # mid-grey — no prefix
COLOUR_ACCENT = "#e8792b"    # orange — [a]_
COLOUR_OPAQUE = "#9a9a9a"    # light grey — [o]_
COLOUR_CLEAR = "#bfe3f0"     # light blue — [c]_ (none actually printed)
BACKGROUND = "#ffffff"

# Fraction of each axis's own extent added as margin when framing a part (not
# a shared cube margin — see _draw_part) so a thin part isn't padded as if it
# were a cube of its longest dimension. FRAME_FLOOR_FRAC is a minimum margin
# (relative to the part's largest dimension) for axes with ~zero extent.
FRAME_PAD_FRAC = 0.04
FRAME_FLOOR_FRAC = 0.02

PREFIX_RE = re.compile(r"^\[([aoc])\]_")


def colour_for(basename: str) -> tuple[str, str]:
    """(category, hex) from the Voron [a]/[o]/[c] filename prefix."""
    m = PREFIX_RE.match(basename)
    if not m:
        return "primary", COLOUR_PRIMARY
    return {"a": ("accent", COLOUR_ACCENT), "o": ("opaque", COLOUR_OPAQUE),
            "c": ("clear", COLOUR_CLEAR)}[m.group(1)]


# --------------------------------------------------------------- part catalog

def unique_parts() -> list[dict]:
    """Every unique (repo, path) across slicer.plates.PLATES, first batch seen,
    resolved to an on-disk .stl file. 3MF-only parts (Nevermore cartridge) fall
    back to the sibling .stl the fetch already pulled down."""
    seen: dict[tuple[str, str], dict] = {}
    for plate_id, pl in plates.PLATES.items():
        batch = pl["batch"]
        for repo, relpath, qty in pl["parts"]:
            key = (repo, relpath)
            if key in seen:
                continue
            basename = relpath.rsplit("/", 1)[-1]
            src = STL_DIR / repo / relpath
            if src.suffix.lower() == ".3mf":
                # geom.read_stl only understands STL; the fetch step already
                # pulled down a sibling .stl for every 3MF-only part.
                candidate = src.with_suffix(".stl")
                if candidate.exists():
                    src = candidate
            category, hexcolour = colour_for(basename)
            seen[key] = dict(
                repo=repo, relpath=relpath, basename=basename,
                batch=batch, category=category, colour=hexcolour, src=src,
            )
    return sorted(seen.values(), key=lambda p: (p["batch"], p["basename"]))


# ------------------------------------------------------------------- mirrors

def mirror_base(stem: str) -> tuple[str, str] | None:
    """If `stem` names one half of a mirrored pair, return (pair_key, side)
    where pair_key is identical for both halves. Handles the two patterns the
    plan actually uses: `..._left_...`/`..._right_...` and a leading/trailing
    `_a`/`_b` (or bracket-prefixed `a_`/`b_`) token."""
    norm = PREFIX_RE.sub("", stem)
    norm = re.sub(r"_x\d+$", "", norm)
    tokens = norm.split("_")
    tokens = [t for t in tokens if t]
    low = [t.lower() for t in tokens]
    if "left" in low:
        i = low.index("left")
        key = tuple(low[:i] + ["*"] + low[i + 1:])
        return key, "left"
    if "right" in low:
        i = low.index("right")
        key = tuple(low[:i] + ["*"] + low[i + 1:])
        return key, "right"
    if low and low[0] == "a":
        return tuple(["*"] + low[1:]), "a"
    if low and low[0] == "b":
        return tuple(["*"] + low[1:]), "b"
    if low and low[-1] == "a":
        return tuple(low[:-1] + ["*"]), "a"
    if low and low[-1] == "b":
        return tuple(low[:-1] + ["*"]), "b"
    return None


def find_pairs(parts: list[dict]) -> dict[str, tuple[dict, dict]]:
    """base-stem (without side token, keyed by first part's stem) -> (left, right)."""
    groups: dict[tuple, dict[str, dict]] = {}
    for p in parts:
        stem = Path(p["basename"]).stem
        mb = mirror_base(stem)
        if mb is None:
            continue
        key, side = mb
        groups.setdefault(key, {})[side] = p
    pairs = {}
    for key, sides in groups.items():
        halves = None
        if "left" in sides and "right" in sides:
            halves = (sides["left"], sides["right"])
        elif "a" in sides and "b" in sides:
            halves = (sides["a"], sides["b"])
        if halves:
            base = re.sub(r"^\[[aoc]\]_", "", Path(halves[0]["basename"]).stem)
            base = re.sub(r"_(left|right|a|b)(_|$)", r"\2", base, count=1)
            pairs[base or Path(halves[0]["basename"]).stem] = halves
    return pairs


# ------------------------------------------------------------------ geometry

def load_mesh(src: Path):
    tris = geom.read_stl(src)
    if not tris:
        raise ValueError("empty/unreadable mesh")
    return tris


def mesh_bbox_mm(tris) -> tuple[float, float, float]:
    minx, miny, minz, maxx, maxy, maxz = geom.bbox(tris)
    return (maxx - minx, maxy - miny, maxz - minz)


def mesh_volume_cm3(tris) -> float:
    """Signed-tetrahedron volume via the divergence theorem, summed over the
    STL's triangle soup (each triangle forms a tet with the origin)."""
    total = 0.0
    for v0, v1, v2 in tris:
        total += (
            v0[0] * (v1[1] * v2[2] - v1[2] * v2[1])
            - v0[1] * (v1[0] * v2[2] - v1[2] * v2[0])
            + v0[2] * (v1[0] * v2[1] - v1[1] * v2[0])
        )
    return abs(total) / 6.0 / 1000.0  # mm^3 -> cm^3


# -------------------------------------------------------------------- render

# Fixed "upper-left" light, chosen relative to the fixed isometric camera
# (elev=30, azim=-135 below) so the faces the camera actually sees are
# well lit rather than mostly self-shadowed — a light direction picked in
# absolute world space (independent of the view) left most visible faces
# near the 0.35 shadow floor and rendered almost black.
LIGHT_DIR = np.array([-0.618, -0.274, 0.737])
LIGHT_DIR = LIGHT_DIR / np.linalg.norm(LIGHT_DIR)


def _shade(tris_arr: np.ndarray, base_hex: str) -> np.ndarray:
    """Vectorised Lambert shading: intensity 0.35 (facing away) .. 1.0
    (facing the light) per face, scaling the base colour."""
    base = np.array(matplotlib_colors_to_rgb(base_hex))
    v0, v1, v2 = tris_arr[:, 0], tris_arr[:, 1], tris_arr[:, 2]
    n = np.cross(v1 - v0, v2 - v0)
    norm = np.linalg.norm(n, axis=1)
    norm = np.where(norm > 0, norm, 1.0)
    n = n / norm[:, None]
    with np.errstate(all="ignore"):  # spurious BLAS FPE flags on matmul, not real NaN/Inf
        dot = n.dot(LIGHT_DIR)
    intensity = 0.35 + 0.65 * np.clip(dot, 0.0, None)
    return np.clip(base[None, :] * intensity[:, None], 0, 1)


def _edge_rgba(base_hex: str) -> tuple[float, float, float, float]:
    """Thin, semi-transparent darker-than-base edge colour so silhouettes and
    internal feature edges (holes, bosses) read against the shaded faces."""
    r, g, b = matplotlib_colors_to_rgb(base_hex)
    return (r * 0.35, g * 0.35, b * 0.35, 0.35)


def matplotlib_colors_to_rgb(hexstr: str) -> tuple[float, float, float]:
    hexstr = hexstr.lstrip("#")
    return tuple(int(hexstr[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def _draw_part(ax, tris, base_hex: str) -> tuple[float, float, float]:
    arr = np.array(tris, dtype=float)  # (n, 3, 3)
    colours = _shade(arr, base_hex)
    coll = Poly3DCollection(arr, facecolor=colours, edgecolor=_edge_rgba(base_hex), linewidths=0.3)
    ax.add_collection3d(coll)

    pts = arr.reshape(-1, 3)
    mins = pts.min(axis=0)
    maxs = pts.max(axis=0)
    dims = maxs - mins
    maxdim = max(float(dims.max()), 1e-6)
    # Per-axis padding (not a shared cube margin) — mplot3d guarantees the
    # full xlim/ylim/zlim box fits the view regardless of rotation, so
    # padding every axis by the *part's* longest dimension (the old
    # behaviour) wastes frame on any part that isn't cube-shaped. Padding
    # each axis by its own extent keeps thin/elongated parts framed tight.
    pads = np.maximum(dims * FRAME_PAD_FRAC, maxdim * FRAME_FLOOR_FRAC)
    lo = mins - pads
    hi = maxs + pads
    ax.set_xlim(lo[0], hi[0])
    ax.set_ylim(lo[1], hi[1])
    ax.set_zlim(lo[2], hi[2])
    return (dims[0], dims[1], dims[2])


def _setup_axes(ax) -> None:
    ax.set_proj_type("ortho")
    ax.view_init(elev=30, azim=-135)  # isometric-ish, from front-top-left
    ax.set_axis_off()
    ax.set_facecolor(BACKGROUND)


def _scale_bar_and_caption(ax, fig, span_mm: float, caption: str, caption_x: float = 0.02) -> None:
    # 10 mm scale bar drawn in data space at the front-bottom-left of the view.
    xlim, ylim, zlim = ax.get_xlim(), ax.get_ylim(), ax.get_zlim()
    x0 = xlim[0] + (xlim[1] - xlim[0]) * 0.08
    y0 = ylim[0] + (ylim[1] - ylim[0]) * 0.08
    z0 = zlim[0]
    ax.plot([x0, x0 + 10], [y0, y0], [z0, z0], color="black", linewidth=2)
    ax.text(x0 + 5, y0, z0, "10 mm", fontsize=6, color="black", ha="center")
    fig.text(caption_x, 0.02, caption, fontsize=6, color="#333333", va="bottom", ha="left")


def render_part_png(part: dict, out_path: Path) -> tuple[float, float, float] | None:
    try:
        tris = load_mesh(part["src"])
    except Exception as exc:  # noqa: BLE001
        part["error"] = str(exc)
        return None
    fig = plt.figure(figsize=(6, 4.5), dpi=100)
    fig.patch.set_facecolor(BACKGROUND)
    ax = fig.add_subplot(111, projection="3d")
    _setup_axes(ax)
    dims = _draw_part(ax, tris, part["colour"])
    _scale_bar_and_caption(ax, fig, max(dims), part["basename"])
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, facecolor=BACKGROUND)
    plt.close(fig)
    part["bbox_mm"] = dims
    part["volume_cm3"] = mesh_volume_cm3(tris)
    return dims


def _pair_side_labels(left: dict, right: dict) -> tuple[str, str]:
    """LEFT/RIGHT if either basename actually carries that token, else A/B."""
    for part, other in ((left, right), (right, left)):
        toks = re.split(r"[_.]", Path(part["basename"]).stem.lower())
        if "left" in toks:
            return ("LEFT", "RIGHT") if part is left else ("RIGHT", "LEFT")
        if "right" in toks:
            return ("RIGHT", "LEFT") if part is left else ("LEFT", "RIGHT")
    return "A", "B"


def render_pair_png(name: str, left: dict, right: dict, out_path: Path) -> None:
    labels = _pair_side_labels(left, right)
    fig = plt.figure(figsize=(6, 3), dpi=100)
    fig.patch.set_facecolor(BACKGROUND)
    for i, part in enumerate((left, right)):
        ax = fig.add_subplot(1, 2, i + 1, projection="3d")
        _setup_axes(ax)
        if "src" in part and part["src"].exists():
            try:
                tris = load_mesh(part["src"])
                dims = _draw_part(ax, tris, part["colour"])
                caption = f"{labels[i]}   {part['basename']}"
                _scale_bar_and_caption(ax, fig, max(dims), caption, caption_x=0.02 + i * 0.5)
            except Exception as exc:  # noqa: BLE001
                ax.text2D(0.5, 0.5, f"render failed:\n{exc}", ha="center", transform=ax.transAxes)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.05, wspace=0.05)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, facecolor=BACKGROUND)
    plt.close(fig)


def render_sheet_png(batch: str, batch_parts: list[dict], out_path: Path) -> None:
    n = len(batch_parts)
    cols = max(1, min(4, n))
    rows = max(1, math.ceil(n / cols))
    # "2x" thumbnail sheet: each cell rendered at the same per-part pixel
    # density as the single-part PNGs (600x450 @ 100dpi), just tiled and then
    # saved at double the resulting figure DPI.
    fig = plt.figure(figsize=(cols * 2.4, rows * 2.0), dpi=200)
    fig.patch.set_facecolor(BACKGROUND)
    for i, part in enumerate(batch_parts):
        ax = fig.add_subplot(rows, cols, i + 1, projection="3d")
        _setup_axes(ax)
        if part["src"].exists():
            try:
                dims = _draw_part(ax, load_mesh(part["src"]), part["colour"])
            except Exception:  # noqa: BLE001
                pass
        ax.text2D(0.5, -0.05, part["basename"], fontsize=5, ha="center",
                   transform=ax.transAxes, color="#222222")
    fig.suptitle(f"Batch {batch}", fontsize=9)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.02, hspace=0.25, wspace=0.05)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, facecolor=BACKGROUND)
    plt.close(fig)


# --------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None, help="render only the first N parts (smoke test)")
    args = ap.parse_args()

    parts = unique_parts()
    if args.limit:
        parts = parts[: args.limit]
    pairs = find_pairs(parts)
    pair_png_for: dict[str, str] = {}

    failed: list[tuple[str, str]] = []
    for part in parts:
        out = OUT_DIR / f"{Path(part['basename']).stem}.png"
        if not part["src"].exists():
            failed.append((part["basename"], f"missing source file: {part['src']}"))
            continue
        dims = render_part_png(part, out)
        if dims is None:
            failed.append((part["basename"], part.get("error", "unknown render error")))
            continue
        part["png"] = str(out.relative_to(REPO_ROOT))

    for base, (left, right) in pairs.items():
        if left["src"].exists() and right["src"].exists():
            out = OUT_DIR / f"pair-{base}.png"
            render_pair_png(base, left, right, out)
            rel = str(out.relative_to(REPO_ROOT))
            pair_png_for[left["basename"]] = rel
            pair_png_for[right["basename"]] = rel

    by_batch: dict[str, list[dict]] = {}
    for part in parts:
        by_batch.setdefault(part["batch"], []).append(part)
    sheet_for: dict[str, str] = {}
    for batch, batch_parts in sorted(by_batch.items()):
        out = OUT_DIR / f"sheet-{batch}.png"
        render_sheet_png(batch, batch_parts, out)
        rel = str(out.relative_to(REPO_ROOT))
        for p in batch_parts:
            sheet_for[p["basename"]] = rel

    manifest_path = OUT_DIR / "MANIFEST.csv"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["stl", "batch", "colour", "png", "sheet", "pair_png", "bbox_mm", "volume_cm3"])
        for part in parts:
            if "png" not in part:
                continue
            dims = part.get("bbox_mm", (0, 0, 0))
            w.writerow([
                part["basename"],
                part["batch"],
                part["category"],
                part["png"],
                sheet_for.get(part["basename"], ""),
                pair_png_for.get(part["basename"], ""),
                f"{dims[0]:.1f},{dims[1]:.1f},{dims[2]:.1f}",
                f"{part.get('volume_cm3', 0):.2f}",
            ])

    n_pngs = sum(1 for p in parts if "png" in p)
    print(f"Rendered {n_pngs}/{len(parts)} parts.")
    if failed:
        print(f"Failed ({len(failed)}):")
        for name, reason in failed:
            print(f"  {name}: {reason}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
