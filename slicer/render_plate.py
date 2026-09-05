#!/usr/bin/env python3
"""Draw the top-down plate preview committed to docs/manual/assets/plates/.

PrusaSlicer 2.9.6's CLI emits no thumbnails - the `thumbnails` setting reaches
the G-code config block but no image data is written, in either ASCII or binary
G-code, because thumbnail rasterisation lives in the GUI. So the preview is
drawn here from the same arrangement that goes into the 3MF, which also lets it
carry what a screenshot could not: a numbered part index the builder can count
against, and the brim outline where a brim is applied.

Needs Pillow (`pip install -r slicer/requirements.txt`).
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from geom import BED_X, BED_Y

SCALE = 3.4  # px per mm
PAD = 24
LEGEND_W = 430
FONT_DIRS = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
]
FONT_BOLD = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]

BG = (250, 250, 249)
BED = (232, 232, 230)
BED_EDGE = (150, 150, 148)
GRID = (216, 216, 214)
TEXT = (30, 30, 32)
MUTED = (110, 110, 115)
FILL = {"black": (62, 64, 70), "orange": (232, 116, 28)}
EDGE = {"black": (28, 29, 33), "orange": (150, 68, 8)}
BRIM = {"black": (150, 152, 158), "orange": (245, 186, 132)}


def _offset(poly, dist):
    """Outward offset of a convex polygon: each vertex moves along the bisector
    of its two edge normals, which keeps the brim ring a uniform width."""
    import math
    area = sum(poly[i][0] * poly[(i + 1) % len(poly)][1]
               - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))
    if area < 0:  # normals below assume a counter-clockwise ring
        poly = list(reversed(poly))
    n = len(poly)
    out = []
    for i in range(n):
        px, py = poly[i]
        ax, ay = poly[(i - 1) % n]
        bx, by = poly[(i + 1) % n]
        norms = []
        for (sx, sy), (ex, ey) in (((ax, ay), (px, py)), ((px, py), (bx, by))):
            dx, dy = ex - sx, ey - sy
            ln = max(math.hypot(dx, dy), 1e-9)
            norms.append((dy / ln, -dx / ln))
        mx, my = norms[0][0] + norms[1][0], norms[0][1] + norms[1][1]
        ln = max(math.hypot(mx, my), 1e-9)
        mx, my = mx / ln, my / ln
        # miter: move far enough along the bisector that both edges end up
        # `dist` away, not just the vertex
        proj = max(mx * norms[0][0] + my * norms[0][1], 0.25)
        out.append((px + mx * dist / proj, py + my * dist / proj))
    return out


def _font(size: int, bold: bool = False):
    for p in (FONT_BOLD if bold else FONT_DIRS):
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default()


def _ranges(nums: list[int]) -> str:
    """[3,4,5,6,7,8] -> "3-8"; [1,2,5] -> "1, 2, 5"."""
    parts, start = [], nums[0]
    prev = start
    for n in nums[1:] + [None]:
        if n != prev + 1:
            parts.append(str(start) if start == prev
                         else (f"{start}, {prev}" if prev == start + 1 else f"{start}-{prev}"))
            start = n
        prev = n
    return ", ".join(parts)


def render(plate_id: str, colour: str, pieces, hours: float, grams: float,
           brim_note: str, out_path: Path) -> None:
    """`pieces` are packed geom.Piece objects (x/y/rot already set)."""
    bed_w = int(BED_X * SCALE)
    bed_h = int(BED_Y * SCALE)
    head_h = 54
    W = PAD * 2 + bed_w + LEGEND_W
    H = PAD * 2 + bed_h + head_h
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    f_title = _font(26, bold=True)
    f_sub = _font(15)
    f_num = _font(15, bold=True)
    f_leg = _font(14)
    f_small = _font(12)

    d.text((PAD, PAD - 4), f"Plate {plate_id}", font=f_title, fill=TEXT)
    d.text((PAD, PAD + 26),
           f"{len(pieces)} parts  ·  {hours:.1f} h  ·  {grams:.0f} g  ·  "
           f"{'Galaxy Black' if colour == 'black' else 'Prusa Orange'} ASA  ·  bed 250 × 220 mm",
           font=f_sub, fill=MUTED)

    ox, oy = PAD, PAD + head_h

    def to_px(x: float, y: float) -> tuple[float, float]:
        # bed Y runs back-to-front; image Y runs top-down
        return ox + x * SCALE, oy + (BED_Y - y) * SCALE

    d.rectangle([ox, oy, ox + bed_w, oy + bed_h], fill=BED, outline=BED_EDGE, width=2)
    for gx in range(0, int(BED_X) + 1, 50):
        px, _ = to_px(gx, 0)
        d.line([px, oy, px, oy + bed_h], fill=GRID, width=1)
    for gy in range(0, int(BED_Y) + 1, 50):
        _, py = to_px(0, gy)
        d.line([ox, py, ox + bed_w, py], fill=GRID, width=1)

    # front-left origin marker, so the reader can orient the plate on the bed
    d.text((ox + 6, oy + bed_h - 20), "front-left (0,0)", font=f_small, fill=MUTED)

    order = sorted(range(len(pieces)),
                   key=lambda i: (-pieces[i].y, pieces[i].x))
    numbers: dict[int, int] = {}
    for n, i in enumerate(order, 1):
        numbers[i] = n

    for i, p in enumerate(pieces):
        x0, y0, _x1, _y1 = p.extent()
        poly = []
        import math
        r = math.radians(p.rot)
        c, s = math.cos(r), math.sin(r)
        for hx, hy in p.hull:
            rx, ry = hx * c - hy * s, hx * s + hy * c
            poly.append(to_px(p.x + (rx - x0), p.y + (ry - y0)))
        if p.brim:
            d.polygon(_offset(poly, p.brim * SCALE), outline=BRIM[colour], width=2)
        d.polygon(poly, fill=FILL[colour], outline=EDGE[colour])
        cx = sum(q[0] for q in poly) / len(poly)
        cy = sum(q[1] for q in poly) / len(poly)
        label = str(numbers[i])
        tb = d.textbbox((0, 0), label, font=f_num)
        d.text((cx - tb[2] / 2, cy - tb[3] / 2), label, font=f_num,
               fill=(255, 255, 255) if colour == "black" else (40, 20, 0))

    # legend: one row per distinct part, listing the numbers it was given
    lx = ox + bed_w + 22
    ly = oy + 2
    d.text((lx, ly), "Parts on this plate", font=_font(15, bold=True), fill=TEXT)
    ly += 24
    groups: dict[str, list[int]] = {}
    for i, p in enumerate(pieces):
        groups.setdefault(p.name.rsplit("#", 1)[0], []).append(numbers[i])
    rows = []
    for name, nums in sorted(groups.items(), key=lambda kv: min(kv[1])):
        rows.append((_ranges(sorted(nums)), name, len(nums)))
    gutter = max((d.textlength(t, font=f_leg) for t, _n, _c in rows), default=0) + 14
    for tag, name, count in rows:
        d.text((lx, ly), tag, font=f_leg, fill=MUTED)
        label = name if count == 1 else f"{name}  x{count}"
        d.text((lx + gutter, ly), label, font=f_leg, fill=TEXT)
        ly += 19
        if ly > oy + bed_h - 60:
            d.text((lx, ly), "...", font=f_leg, fill=MUTED)
            break
    if brim_note:
        d.text((lx, oy + bed_h - 40), brim_note, font=f_small, fill=MUTED)
    d.text((lx, oy + bed_h - 22),
           "PrusaSlicer 2.9.6 · slicer/build_plates.py", font=f_small, fill=MUTED)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG", optimize=True)
