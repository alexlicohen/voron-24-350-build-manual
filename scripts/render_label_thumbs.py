#!/usr/bin/env python3
"""Clean part pictures for the bin labels (docs/print/bin-labels.md).

One PNG per STL that slicer/bins.py contents() puts in a bin, written to docs/print/assets/parts/<stem>.png.
Same renderer and style as scripts/render_parts.py (matplotlib, isometric, [a] blue / grey), but no
caption, no scale bar and a tight crop, because the picture prints 8-14 mm wide on a label.
Covers the add-on bins too (13-scrubber, 14-exhaust), which have no plate and no MANIFEST row.

    python3 scripts/render_label_thumbs.py          # render what is missing
    python3 scripts/render_label_thumbs.py --force  # re-render all

scripts/build_printables.py only references the PNGs; it fails the build when one is missing.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import render_parts as rp
from render_parts import (REPO_ROOT, STL_DIR, BACKGROUND, _draw_part, _setup_axes, colour_for,
                          load_mesh, plt)
import bins  # slicer/bins.py (render_parts put slicer/ on sys.path)
from build_plates import source_stl
from PIL import Image, ImageChops

OUT = REPO_ROOT / "docs" / "print" / "assets" / "parts"
SIZE = 240   # longest side in px after the crop: 14 mm at ~430 dpi


def thumb_path(stl_path: str) -> Path:
    return OUT / f"{Path(stl_path).stem}.png"


def render(repo: str, path: str, out: Path) -> None:
    src = STL_DIR / source_stl(repo, path)
    if src.suffix.lower() == ".3mf":
        src = src.with_suffix(".stl")
    tris = load_mesh(src)
    fig = plt.figure(figsize=(4, 4), dpi=150)
    fig.patch.set_facecolor(BACKGROUND)
    ax = fig.add_subplot(111, projection="3d")
    _setup_axes(ax)
    _draw_part(ax, tris, colour_for(Path(path).name)[1])
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    tmp = out.with_suffix(".tmp.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(tmp, facecolor=BACKGROUND)
    plt.close(fig)
    im = Image.open(tmp).convert("RGB")
    box = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255))).getbbox()
    im = im.crop(box) if box else im
    pad = max(4, round(max(im.size) * 0.03))
    canvas = Image.new("RGB", (im.width + 2 * pad, im.height + 2 * pad), (255, 255, 255))
    canvas.paste(im, (pad, pad))
    canvas.thumbnail((SIZE, SIZE), Image.LANCZOS)
    canvas.save(out, optimize=True)
    tmp.unlink()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    done = failed = 0
    for parts in bins.contents().values():
        for e in parts.values():
            repo, path = e["geom"]
            out = thumb_path(path)
            if out.exists() and not args.force:
                continue
            try:
                render(repo, path, out)
                done += 1
            except Exception as exc:  # noqa: BLE001
                failed += 1
                print(f"FAIL {path}: {exc}", file=sys.stderr)
    print(f"rendered {done}, failed {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
