#!/usr/bin/env python3
"""Plate sorting diagrams: every part on every plate, numbered, outlined and coloured by the
bin it goes into once it is off the bed.

Source of truth for the arrangement is the committed PrusaSlicer project
(`slicer/plates/<id>.3mf`, read by slicer/threemf.py): if a plate is re-arranged in the GUI
and saved, re-running this script redraws it. Bins come from slicer/bins.py; hours and grams
from slicer/estimates.csv (written by slicer/build_plates.py).

For each plate it writes docs/manual/assets/plates/<id>.png (1600 px wide) and <id>.svg with:
  * the 250 x 220 bed, 50 mm grid, front-left origin marked,
  * the true top-down silhouette of every object (all triangles projected and unioned,
    holes included), filled and stroked in its bin's colour,
  * a number in each part and its bin id (inside; or beside with a leader when the part is
    too small), and the per-object brim ring where the project sets one,
  * a legend `# · STL · bin (chapter · steps)` and a header with plate id, hours, grams.

    python3 scripts/render_plate_bins.py                 # all plates in slicer/plates/
    python3 scripts/render_plate_bins.py B01-P1 B08-P1   # named plates
    python3 scripts/render_plate_bins.py --markdown      # per-plate bin -> parts tables (stdout)
    python3 scripts/render_plate_bins.py --write-manifest  # `bin` column into assets/parts/MANIFEST.csv
    python3 scripts/render_plate_bins.py --check         # 3MF contents vs slicer/plates.py, no drawing

Needs Pillow (`pip install -r slicer/requirements.txt`). Everything else is stdlib.
"""
from __future__ import annotations

import argparse
import csv
import html
import math
import sys
from collections import OrderedDict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO = Path(__file__).resolve().parent.parent
SLICER = REPO / "slicer"
sys.path.insert(0, str(SLICER))
import bins  # noqa: E402
import threemf  # noqa: E402
from plates import PLATES  # noqa: E402

PLATE_DIR = SLICER / "plates"
OUT_DIR = REPO / "docs" / "manual" / "assets" / "plates"
ESTIMATES = SLICER / "estimates.csv"
MANIFEST = REPO / "docs" / "manual" / "assets" / "parts" / "MANIFEST.csv"

BED_X, BED_Y = 250.0, 220.0

# ---- layout, in 1x pixels (the PNG is drawn at 2x and downsampled for anti-aliasing)
OUT_W = 1600
S = 2                      # supersampling factor for the PNG
SCALE = 3.6                # px per mm at 1x -> bed 900 x 792
PAD = 24
HEAD_H = 66
FOOT_H = 34
BED_W = int(round(BED_X * SCALE))
BED_H = int(round(BED_Y * SCALE))
LEGEND_X = PAD + BED_W + 26
LEGEND_W = OUT_W - LEGEND_X - PAD
OUT_H = PAD + HEAD_H + BED_H + FOOT_H + PAD
BED_OX, BED_OY = PAD, PAD + HEAD_H

BG = "#fafaf9"
BED = "#e9e9e6"
BED_EDGE = "#96968f"
GRID = "#d5d5d1"
TEXT = "#1e1e20"
MUTED = "#6e6e73"
LEADER = "#333336"
BRIM_STROKE = "#7a7a80"
UNASSIGNED = "#e53935"

FONT_REG = ["/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
FONT_BOLD = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] + FONT_REG
SVG_FONT = "Arial, Helvetica, 'DejaVu Sans', sans-serif"

_fonts: dict[tuple[int, bool], ImageFont.FreeTypeFont] = {}


def font(size: int, bold: bool = False):
    key = (size, bold)
    if key not in _fonts:
        for p in (FONT_BOLD if bold else FONT_REG):
            if Path(p).exists():
                try:
                    _fonts[key] = ImageFont.truetype(p, size)
                    break
                except OSError:
                    continue
        else:
            _fonts[key] = ImageFont.load_default()
    return _fonts[key]


def text_size(s: str, size: int, bold: bool = False) -> tuple[int, int]:
    f = font(size, bold)
    b = ImageDraw.Draw(Image.new("L", (1, 1))).textbbox((0, 0), s, font=f)
    return b[2] - b[0], b[3] - b[1]


def hex_rgb(h: str) -> tuple[int, int, int]:
    return int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)


def mix(h: str, with_: str, t: float) -> str:
    a, b = hex_rgb(h), hex_rgb(with_)
    return "#%02x%02x%02x" % tuple(int(round(a[i] * (1 - t) + b[i] * t)) for i in range(3))


# ------------------------------------------------------------ dual canvas

class Canvas:
    """Draws the same primitives into a 2x PIL image and an SVG string. Coordinates are 1x px."""

    def __init__(self, w: int, h: int, title: str):
        self.w, self.h = w, h
        self.img = Image.new("RGB", (w * S, h * S), BG)
        self.d = ImageDraw.Draw(self.img, "RGBA")
        self.svg: list[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" font-family="{SVG_FONT}">',
            f"<title>{html.escape(title)}</title>",
            f'<rect x="0" y="0" width="{w}" height="{h}" fill="{BG}"/>',
        ]

    @staticmethod
    def _px(v):
        return v * S

    def rect(self, x, y, w, h, fill=None, stroke=None, width=1.0, rx=0.0, opacity=1.0):
        kw = {}
        if fill:
            r, g, b = hex_rgb(fill)
            kw["fill"] = (r, g, b, int(255 * opacity))
        if stroke:
            kw["outline"] = stroke
            kw["width"] = max(1, int(round(width * S)))
        if rx:
            self.d.rounded_rectangle([x * S, y * S, (x + w) * S, (y + h) * S], radius=rx * S, **kw)
        else:
            self.d.rectangle([x * S, y * S, (x + w) * S, (y + h) * S], **kw)
        attrs = [f'x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"']
        if rx:
            attrs.append(f'rx="{rx:.1f}"')
        attrs.append(f'fill="{fill}"' if fill else 'fill="none"')
        if opacity != 1.0:
            attrs.append(f'fill-opacity="{opacity:.2f}"')
        if stroke:
            attrs.append(f'stroke="{stroke}" stroke-width="{width:.1f}"')
        self.svg.append(f"<rect {' '.join(attrs)}/>")

    def line(self, x0, y0, x1, y1, stroke, width=1.0, dash=None):
        self.d.line([x0 * S, y0 * S, x1 * S, y1 * S], fill=stroke, width=max(1, int(round(width * S))))
        extra = f' stroke-dasharray="{dash}"' if dash else ""
        self.svg.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" '
                        f'stroke="{stroke}" stroke-width="{width:.1f}"{extra}/>')

    def circle(self, cx, cy, r, fill):
        self.d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=fill)
        self.svg.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}"/>')

    def loops(self, loops: list[list[tuple[float, float]]], fill=None, stroke=None,
              width=1.0, dash=None, hole_fill=BED, title=None):
        """Closed polygons; loops whose signed area has the opposite sign to the largest are
        holes (evenodd in SVG, painted in `hole_fill` in the PNG)."""
        if not loops:
            return
        areas = [_signed_area(lp) for lp in loops]
        outer_sign = 1 if areas[max(range(len(loops)), key=lambda i: abs(areas[i]))] >= 0 else -1
        order = sorted(range(len(loops)), key=lambda i: -abs(areas[i]))
        if fill:
            for i in order:
                col = fill if (areas[i] >= 0) == (outer_sign >= 0) else hole_fill
                pts = [(x * S, y * S) for x, y in loops[i]]
                if len(pts) >= 3:
                    self.d.polygon(pts, fill=col)
        if stroke:
            w = max(1, int(round(width * S)))
            for lp in loops:
                pts = [(x * S, y * S) for x, y in lp] + [(lp[0][0] * S, lp[0][1] * S)]
                self.d.line(pts, fill=stroke, width=w, joint="curve")
        path = " ".join("M" + " ".join(f"{x:.1f},{y:.1f}" for x, y in lp) + "Z" for lp in loops)
        attrs = [f'd="{path}"', 'fill-rule="evenodd"']
        attrs.append(f'fill="{fill}"' if fill else 'fill="none"')
        if stroke:
            attrs.append(f'stroke="{stroke}" stroke-width="{width:.1f}" stroke-linejoin="round"')
            if dash:
                attrs.append(f'stroke-dasharray="{dash}"')
        t = f"<title>{html.escape(title)}</title>" if title else ""
        self.svg.append(f"<path {' '.join(attrs)}>{t}</path>" if t else f"<path {' '.join(attrs)}/>")

    def text(self, x, y, s, size, colour=TEXT, bold=False, anchor="lt"):
        """anchor: PIL-style two letters (l/m/r + t/m/b). y is the top for 't', middle for 'm'."""
        f = font(size * S, bold)
        self.d.text((x * S, y * S), s, font=f, fill=colour, anchor=anchor)
        ta = {"l": "start", "m": "middle", "r": "end"}[anchor[0]]
        dy = {"t": size * 0.92, "m": size * 0.36, "b": 0}[anchor[1]]
        weight = ' font-weight="bold"' if bold else ""
        self.svg.append(f'<text x="{x:.1f}" y="{y + dy:.1f}" font-size="{size}" fill="{colour}" '
                        f'text-anchor="{ta}"{weight}>{html.escape(s)}</text>')

    def save(self, png: Path, svg: Path):
        out = self.img.resize((self.w, self.h), Image.LANCZOS)
        out.save(png, "PNG", optimize=True)
        svg.write_text("\n".join(self.svg + ["</svg>"]) + "\n", encoding="utf-8")


def _signed_area(lp):
    return 0.5 * sum(lp[i][0] * lp[(i + 1) % len(lp)][1] - lp[(i + 1) % len(lp)][0] * lp[i][1]
                     for i in range(len(lp)))


# ------------------------------------------------------- raster silhouette

def to_bed_px(x_mm: float, y_mm: float) -> tuple[float, float]:
    """Bed mm (Y back-to-front) -> 1x canvas px (Y top-down)."""
    return BED_OX + x_mm * SCALE, BED_OY + (BED_Y - y_mm) * SCALE


class Silhouette:
    """Top-down footprint of one object as a 1x binary mask, its hole-filled version, and the
    outline loops (canvas px). Built at 2x from every projected triangle, then downsampled."""

    def __init__(self, obj: threemf.PlateObject, brim_mm: float):
        x0, y0, _z0, x1, y1, _z1 = obj.bbox()
        self.margin = int(math.ceil(brim_mm * SCALE)) + 4
        px0, py0 = to_bed_px(x0, y1)      # top-left in canvas px
        px1, py1 = to_bed_px(x1, y0)
        self.ox = int(math.floor(px0)) - self.margin
        self.oy = int(math.floor(py0)) - self.margin
        self.w = int(math.ceil(px1)) - self.ox + self.margin
        self.h = int(math.ceil(py1)) - self.oy + self.margin

        hi = Image.new("L", (self.w * S, self.h * S), 0)
        d = ImageDraw.Draw(hi)
        verts = obj.vertices
        ox, oy = self.ox, self.oy
        pts = [((BED_OX + v[0] * SCALE - ox) * S, (BED_OY + (BED_Y - v[1]) * SCALE - oy) * S)
               for v in verts]
        for a, b, c in obj.triangles:
            pa, pb, pc = pts[a], pts[b], pts[c]
            # skip vertical faces (zero projected area): they add nothing to the footprint
            if abs((pb[0] - pa[0]) * (pc[1] - pa[1]) - (pc[0] - pa[0]) * (pb[1] - pa[1])) < 1e-3:
                continue
            d.polygon([pa, pb, pc], fill=255)
        self.mask = hi.resize((self.w, self.h), Image.BOX).point(lambda v: 255 if v >= 128 else 0)
        self.area_px = sum(1 for v in self.mask.getdata() if v)
        # hole-filled: flood the background from the (always empty) border, invert
        bg = self.mask.copy()
        ImageDraw.floodfill(bg, (0, 0), 128)
        self.filled = bg.point(lambda v: 0 if v == 128 else 255)
        self.loops = [[(x + ox, y + oy) for x, y in lp] for lp in _contours(self.mask)]
        self.brim_loops: list[list[tuple[float, float]]] = []
        if brim_mm > 0:
            k = 2 * int(round(brim_mm * SCALE)) + 1
            dil = self.filled.filter(ImageFilter.MaxFilter(k))
            self.brim_loops = [[(x + ox, y + oy) for x, y in lp] for lp in _contours(dil)]
        self.pole, self.radius = self._pole()

    def _pole(self) -> tuple[tuple[float, float], int]:
        """Centre of the last non-empty erosion of the hole-filled mask, and how many 1 px
        erosions it survived (the inscribed radius)."""
        m = self.filled
        r = 0
        last = m
        while True:
            e = last.filter(ImageFilter.MinFilter(3))
            if e.getbbox() is None:
                break
            last, r = e, r + 1
            if r > 400:
                break
        bb = last.getbbox() or (0, 0, self.w, self.h)
        return ((bb[0] + bb[2]) / 2 + self.ox, (bb[1] + bb[3]) / 2 + self.oy), r

    def rect_inside(self, mask: Image.Image, x, y, w, h) -> bool:
        """True if the 1x rect (canvas px) lies entirely on set pixels of `mask`."""
        lx, ly = int(math.floor(x - self.ox)), int(math.floor(y - self.oy))
        rx, ry = int(math.ceil(x + w - self.ox)), int(math.ceil(y + h - self.oy))
        if lx < 0 or ly < 0 or rx > self.w or ry > self.h or rx <= lx or ry <= ly:
            return False
        return mask.crop((lx, ly, rx, ry)).getextrema()[0] == 255


def _contours(mask: Image.Image) -> list[list[tuple[float, float]]]:
    """Marching squares on a binary L image; returns closed loops in pixel coordinates
    (pixel-area boundaries), simplified. Filled region is on the right of travel."""
    w, h = mask.size
    data = mask.tobytes()
    W = w + 2
    g = bytearray(W * (h + 2))
    for y in range(h):
        row = data[y * w:(y + 1) * w]
        g[(y + 1) * W + 1:(y + 1) * W + 1 + w] = bytes(1 if v else 0 for v in row)

    segs: dict[tuple[int, int], list[tuple[int, int]]] = {}

    def add(x0, y0, x1, y1):
        segs.setdefault((x0, y0), []).append((x1, y1))

    # edge midpoints in doubled coordinates (so they are integers)
    for i in range(h + 1):
        base = i * W
        nbase = base + W
        for j in range(w + 1):
            tl, tr = g[base + j], g[base + j + 1]
            bl, br = g[nbase + j], g[nbase + j + 1]
            case = tl * 8 + tr * 4 + br * 2 + bl
            if case == 0 or case == 15:
                continue
            X, Y = 2 * j, 2 * i
            top, right, bottom, left = (X + 1, Y), (X + 2, Y + 1), (X + 1, Y + 2), (X, Y + 1)
            if case == 1:
                add(*left, *bottom)
            elif case == 2:
                add(*bottom, *right)
            elif case == 3:
                add(*left, *right)
            elif case == 4:
                add(*right, *top)
            elif case == 5:
                add(*right, *top); add(*left, *bottom)
            elif case == 6:
                add(*bottom, *top)
            elif case == 7:
                add(*left, *top)
            elif case == 8:
                add(*top, *left)
            elif case == 9:
                add(*top, *bottom)
            elif case == 10:
                add(*top, *left); add(*bottom, *right)
            elif case == 11:
                add(*top, *right)
            elif case == 12:
                add(*right, *left)
            elif case == 13:
                add(*right, *bottom)
            elif case == 14:
                add(*bottom, *left)

    loops = []
    while segs:
        start = next(iter(segs))
        loop = [start]
        cur = start
        while True:
            nxts = segs.get(cur)
            if not nxts:
                break
            nxt = nxts.pop()
            if not nxts:
                del segs[cur]
            if nxt == start:
                break
            loop.append(nxt)
            cur = nxt
        if len(loop) >= 3:
            # doubled grid -> pixel coords; the padding row/col shifts by 1, pixel area by 0.5
            pts = [((x / 2) - 1 + 0.5, (y / 2) - 1 + 0.5) for x, y in loop]
            loops.append(_simplify(pts, 0.55))
    return loops


def _simplify(pts: list[tuple[float, float]], eps: float) -> list[tuple[float, float]]:
    """Douglas-Peucker on a closed ring (split at the two farthest-apart points)."""
    if len(pts) < 6:
        return pts
    i0 = 0
    i1 = max(range(len(pts)), key=lambda i: (pts[i][0] - pts[0][0]) ** 2 + (pts[i][1] - pts[0][1]) ** 2)
    a = _dp(pts[i0:i1 + 1], eps)
    b = _dp(pts[i1:] + pts[:1], eps)
    out = a[:-1] + b[:-1]
    return out if len(out) >= 3 else pts


def _dp(pts, eps):
    if len(pts) < 3:
        return pts
    (x0, y0), (x1, y1) = pts[0], pts[-1]
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy) or 1e-9
    best, bi = 0.0, 0
    for i in range(1, len(pts) - 1):
        d = abs(dy * (pts[i][0] - x0) - dx * (pts[i][1] - y0)) / ln
        if d > best:
            best, bi = d, i
    if best > eps:
        return _dp(pts[:bi + 1], eps)[:-1] + _dp(pts[bi:], eps)
    return [pts[0], pts[-1]]


# ------------------------------------------------------------- estimates

def load_estimates() -> dict[str, tuple[float, float]]:
    out = {}
    if not ESTIMATES.exists():
        return out
    for r in csv.DictReader(ESTIMATES.open()):
        if r["plate"] != "TOTAL":
            out[r["plate"]] = (float(r["hours"]), float(r["grams"]))
    return out


def plan_parts(plate_id: str) -> dict[str, int]:
    """STL basename -> copies, from slicer/plates.py."""
    out: dict[str, int] = {}
    for _r, p, q in PLATES[plate_id]["parts"]:
        out[p.rsplit("/", 1)[-1]] = out.get(p.rsplit("/", 1)[-1], 0) + q
    return out


# --------------------------------------------------------------- per plate

class Part:
    def __init__(self, obj: threemf.PlateObject, bin_id: str):
        self.obj = obj
        self.bin = bin_id
        self.sil: Silhouette | None = None
        self.number = 0


def load_plate(plate_id: str) -> tuple[threemf.Plate, list[Part], list[str]]:
    plate = threemf.read_plate(PLATE_DIR / f"{plate_id}.3mf", set(bins.ASSIGN))
    warnings: list[str] = []
    counts: dict[str, int] = {}
    parts: list[Part] = []
    for o in plate.objects:
        counts[o.stl] = counts.get(o.stl, 0) + 1
    seen: dict[str, int] = {}
    for o in plate.objects:
        seen[o.stl] = seen.get(o.stl, 0) + 1
        if o.stl in bins.ASSIGN:
            # copy order: the `#n` suffix when present, else order of appearance
            idx = (o.copy - 1) if o.copy else (seen[o.stl] - 1)
            bin_id = bins.copies_bins(plate_id, o.stl, max(idx + 1, counts[o.stl]))[idx]
        else:
            bin_id = "?"
            warnings.append(f"{plate_id}: object {o.name!r} is not in slicer/bins.py - drawn red")
        parts.append(Part(o, bin_id))
    if plate_id in PLATES:
        want = plan_parts(plate_id)
        if counts != want:
            diff = sorted(set(want) | set(counts))
            desc = ", ".join(f"{s}: plan {want.get(s, 0)} / 3mf {counts.get(s, 0)}"
                             for s in diff if want.get(s, 0) != counts.get(s, 0))
            warnings.append(f"{plate_id}: 3MF contents differ from slicer/plates.py - {desc}")
    return plate, parts, warnings


def number_parts(parts: list[Part]) -> None:
    """Reading order: back of the bed (top of the image) to front, left to right in 25 mm bands."""
    def key(p: Part):
        x0, _y0, _z0, _x1, y1, _z1 = p.obj.bbox()
        return (-round(y1 / 25.0), x0)
    for n, p in enumerate(sorted(parts, key=key), 1):
        p.number = n


def _fmt_ranges(nums: list[int]) -> str:
    nums = sorted(nums)
    out, start, prev = [], nums[0], nums[0]
    for n in nums[1:] + [None]:
        if n != prev + 1:
            out.append(str(start) if start == prev else
                       (f"{start}, {prev}" if prev == start + 1 else f"{start}–{prev}"))
            start = n
        prev = n
    return ", ".join(out)


def legend_rows(parts: list[Part]) -> list[tuple[str, str, str, list[int]]]:
    """(stl, bin, numbers) grouped by (stl, bin), ordered by first number."""
    groups: "OrderedDict[tuple[str, str], list[int]]" = OrderedDict()
    for p in sorted(parts, key=lambda p: p.number):
        groups.setdefault((p.obj.stl, p.bin), []).append(p.number)
    return [(stl, b, _fmt_ranges(nums), nums) for (stl, b), nums in groups.items()]


def bin_colour(bin_id: str) -> str:
    return bins.BINS[bin_id]["colour"] if bin_id in bins.BINS else UNASSIGNED


def bin_steps_short(bin_id: str) -> str:
    if bin_id not in bins.BINS:
        return ""
    return bins.BINS[bin_id]["steps"].split(" (")[0]


def render(plate_id: str, estimates: dict[str, tuple[float, float]], out_dir: Path
           ) -> list[str]:
    plate, parts, warnings = load_plate(plate_id)
    number_parts(parts)
    for p in parts:
        p.sil = Silhouette(p.obj, p.obj.brim)

    colour_name = "Prusa Orange" if PLATES.get(plate_id, {}).get("colour") == "orange" else "Galaxy Black"
    hours, grams = estimates.get(plate_id, (float("nan"), float("nan")))
    cv = Canvas(OUT_W, OUT_H, f"Plate {plate_id} — sorting diagram")

    # header
    cv.text(PAD, PAD - 2, f"Plate {plate_id}", 26, TEXT, bold=True)
    hg = (f"{hours:.1f} h  ·  {grams:.0f} g" if hours == hours else "not sliced yet")
    cv.text(PAD, PAD + 32, f"{len(parts)} parts  ·  {hg}  ·  {colour_name} ASA  ·  bed 250 × 220 mm  ·  "
            f"PrusaSlicer 2.9.6 estimate", 14, MUTED)

    # bed
    cv.rect(BED_OX, BED_OY, BED_W, BED_H, fill=BED, stroke=BED_EDGE, width=1.5)
    for gx in range(50, int(BED_X), 50):
        x, _ = to_bed_px(gx, 0)
        cv.line(x, BED_OY, x, BED_OY + BED_H, GRID, 1)
    for gy in range(50, int(BED_Y), 50):
        _, y = to_bed_px(0, gy)
        cv.line(BED_OX, y, BED_OX + BED_W, y, GRID, 1)
    cv.text(BED_OX + 6, BED_OY + BED_H - 16, "front-left (0,0)", 11, MUTED)
    cv.text(BED_OX + BED_W - 6, BED_OY + 4, "rear", 11, MUTED, anchor="rt")

    # brims first (under the parts), then parts
    for p in parts:
        if p.sil.brim_loops:
            cv.loops(p.sil.brim_loops, fill=mix(bin_colour(p.bin), BED, 0.78), stroke=BRIM_STROKE,
                     width=0.8, dash="4 3", hole_fill=BED,
                     title=f"brim {p.obj.brim:g} mm — {p.obj.stl}")
    for p in parts:
        col = bin_colour(p.bin)
        cv.loops(p.sil.loops, fill=col, stroke=mix(col, "#000000", 0.45), width=1.0,
                 title=f"#{p.number} {p.obj.stl} → {p.bin}")

    # labels: occupancy = every part footprint + the area outside the bed (+ a small overhang)
    occ = Image.new("L", (OUT_W, OUT_H), 255)
    ImageDraw.Draw(occ).rectangle([BED_OX - 12, BED_OY - 8, BED_OX + BED_W + 12, BED_OY + BED_H + 8], fill=0)
    for p in parts:
        occ.paste(p.sil.mask, (p.sil.ox, p.sil.oy), p.sil.mask)
    occ_d = ImageDraw.Draw(occ)

    n_size, b_size = 17, 12
    for p in sorted(parts, key=lambda p: -p.sil.area_px):
        col = bin_colour(p.bin)
        tcol = bins.text_colour(col)
        num, bid = str(p.number), p.bin
        nw, nh = text_size(num, n_size, True)
        bw, bh = text_size(bid, b_size)
        block_w, block_h = max(nw, bw) + 8, nh + bh + 8
        cx, cy = p.sil.pole
        placed = False
        # 1. whole block inside solid material
        if p.sil.rect_inside(p.sil.mask, cx - block_w / 2, cy - block_h / 2, block_w, block_h):
            cv.text(cx, cy - block_h / 2 + 2, num, n_size, tcol, bold=True, anchor="mt")
            cv.text(cx, cy + block_h / 2 - bh - 3, bid, b_size, tcol, anchor="mt")
            placed = True
        # 2. inside the outer contour but over holes/ribs: same, on a translucent pill
        elif p.sil.rect_inside(p.sil.filled, cx - block_w / 2 - 2, cy - block_h / 2 - 2,
                               block_w + 4, block_h + 4):
            cv.rect(cx - block_w / 2 - 1, cy - block_h / 2 - 1, block_w + 2, block_h + 2,
                    fill="#ffffff", opacity=0.82, rx=3)
            cv.text(cx, cy - block_h / 2 + 2, num, n_size, TEXT, bold=True, anchor="mt")
            cv.text(cx, cy + block_h / 2 - bh - 3, bid, b_size, TEXT, anchor="mt")
            placed = True
        # 3. number inside, bin beside with a leader
        elif p.sil.rect_inside(p.sil.filled, cx - nw / 2 - 2, cy - nh / 2 - 2, nw + 4, nh + 4):
            on_solid = p.sil.rect_inside(p.sil.mask, cx - nw / 2 - 1, cy - nh / 2 - 1, nw + 2, nh + 2)
            if not on_solid:
                cv.rect(cx - nw / 2 - 2, cy - nh / 2 - 1, nw + 4, nh + 2, fill="#ffffff", opacity=0.82, rx=2)
            cv.text(cx, cy, num, n_size, tcol if on_solid else TEXT, bold=True, anchor="mm")
            _outside_label(cv, occ, occ_d, p, [bid], b_size, col, leader_from=(cx, cy))
            placed = True
        if not placed:
            _outside_label(cv, occ, occ_d, p, [f"#{num}", bid], b_size, col, leader_from=(cx, cy),
                           first_bold=True)

    # legend
    lx, ly = LEGEND_X, BED_OY
    used_bins = list(OrderedDict.fromkeys(p.bin for p in sorted(parts, key=lambda p: p.number)))
    cv.text(lx, PAD + 4, "Bins on this plate", 13, MUTED, bold=True)
    chip_x = lx
    chip_y = PAD + 24
    for b in used_bins:
        col = bin_colour(b)
        w = text_size(b, 12, True)[0] + 14
        if chip_x + w > OUT_W - PAD:
            chip_x, chip_y = lx, chip_y + 22
        cv.rect(chip_x, chip_y, w, 18, fill=col, rx=4)
        cv.text(chip_x + w / 2, chip_y + 9, b, 12, bins.text_colour(col), bold=True, anchor="mm")
        chip_x += w + 6

    rows = legend_rows(parts)
    cv.text(lx, ly, "Parts on this plate  —  # · STL · bin (chapter · steps)", 13, TEXT, bold=True)
    ly += 24
    avail = BED_OY + BED_H - ly - 8
    row_h = max(24, min(36, avail / max(1, len(rows))))
    two_line = row_h >= 30
    gutter = max((text_size(tag, 12, True)[0] for _s, _b, tag, _n in rows), default=20) + 8
    for stl, b, tag, nums in rows:
        col = bin_colour(b)
        cv.rect(lx, ly + 2, 12, 12, fill=col, rx=2)
        cv.text(lx + 18, ly, tag, 12, MUTED, bold=True)
        label = stl if len(nums) == 1 else f"{stl}  ×{len(nums)}"
        cv.text(lx + 18 + gutter, ly, label, 13, TEXT, bold=True)
        meta = bins.BINS.get(b)
        detail = (f"{b} · {meta['label'].replace('`', '')} · {meta['chapter']} · {bin_steps_short(b)}"
                  if meta else f"{b} · NOT IN slicer/bins.py")
        if two_line:
            cv.text(lx + 18 + gutter, ly + 16, detail, 11, MUTED)
        else:
            cv.text(lx + 18 + gutter + text_size(label, 13, True)[0] + 8, ly + 1, f"→ {b}", 11, MUTED)
        ly += row_h

    # footer
    fy = BED_OY + BED_H + 8
    brims = sorted({p.obj.brim for p in parts if p.obj.brim > 0})
    if brims:
        note = "brim (dashed ring) is set per object in the project: " + ", ".join(
            f"{b:g} mm on {sum(1 for p in parts if p.obj.brim == b)} part(s)" for b in brims)
    else:
        note = "no brim on this plate — the preview should show none"
    cv.text(BED_OX, fy, note, 11, MUTED)
    cv.text(BED_OX, fy + 15, f"outlines from slicer/plates/{plate_id}.3mf (the committed project) · "
            "scripts/render_plate_bins.py · bins: slicer/bins.py", 11, MUTED)

    out_dir.mkdir(parents=True, exist_ok=True)
    cv.save(out_dir / f"{plate_id}.png", out_dir / f"{plate_id}.svg")
    return warnings


def _outside_label(cv: Canvas, occ: Image.Image, occ_d, p: Part, lines: list[str], size: int,
                   col: str, leader_from: tuple[float, float], first_bold: bool = False) -> None:
    """Put a small labelled box in free space near the part and draw a leader to it."""
    sizes = [text_size(t, size + (3 if first_bold and i == 0 else 0), first_bold and i == 0)
             for i, t in enumerate(lines)]
    w = max(s[0] for s in sizes) + 10
    h = sum(s[1] for s in sizes) + 6 + 3 * (len(lines) - 1)
    sx0, sy0 = p.sil.ox + p.sil.margin, p.sil.oy + p.sil.margin
    sx1, sy1 = p.sil.ox + p.sil.w - p.sil.margin, p.sil.oy + p.sil.h - p.sil.margin
    cx, cy = leader_from
    cands = []
    for gap in (5, 12, 22, 34, 50, 70, 95):
        cands += [
            (sx1 + gap, cy - h / 2), (sx0 - gap - w, cy - h / 2),
            (cx - w / 2, sy0 - gap - h), (cx - w / 2, sy1 + gap),
            (sx1 + gap, sy0 - gap - h), (sx0 - gap - w, sy0 - gap - h),
            (sx1 + gap, sy1 + gap), (sx0 - gap - w, sy1 + gap),
        ]
    for x, y in cands:
        ix0, iy0, ix1, iy1 = int(x) - 2, int(y) - 2, int(math.ceil(x + w)) + 2, int(math.ceil(y + h)) + 2
        if ix0 < 0 or iy0 < 0 or ix1 > OUT_W or iy1 > OUT_H:
            continue
        if occ.crop((ix0, iy0, ix1, iy1)).getbbox() is None:
            break
    else:
        x, y = sx1 + 5, cy - h / 2   # nothing free: overlap rather than drop the label
    # leader from the box edge nearest the anchor
    bx = min(max(cx, x), x + w)
    by = min(max(cy, y), y + h)
    cv.line(cx, cy, bx, by, LEADER, 1.2)
    cv.circle(cx, cy, 2.2, LEADER)
    cv.rect(x, y, w, h, fill="#ffffff", stroke=col, width=1.4, rx=3, opacity=0.94)
    ty = y + 3
    for i, (t, (tw, th)) in enumerate(zip(lines, sizes)):
        bold = first_bold and i == 0
        cv.text(x + w / 2, ty, t, size + (3 if bold else 0), TEXT, bold=bold, anchor="mt")
        ty += th + 3
    occ_d.rectangle([x - 2, y - 2, x + w + 2, y + h + 2], fill=255)


# --------------------------------------------------------------- helpers

def markdown_tables(plate_ids: list[str]) -> str:
    """Per plate: bin -> parts table for the batch chapters' "Sort into bins" step."""
    out = []
    for pid in plate_ids:
        _plate, parts, _w = load_plate(pid)
        groups: "OrderedDict[str, dict[str, int]]" = OrderedDict()
        for b in bins.BINS:
            for p in parts:
                if p.bin == b:
                    groups.setdefault(b, {})
                    groups[b][p.obj.stl] = groups[b].get(p.obj.stl, 0) + 1
        out.append(f"**{pid}**\n\n| bin | parts off this plate |\n|---|---|")
        for b, stls in groups.items():
            meta = bins.BINS[b]
            cells = []
            for stl, n in stls.items():
                cell = f"`{bins.short_name(stl)}`" + (f" ×{n}" if n > 1 else "")
                cells.append(cell)
            out.append(f"| **{b}** — {meta['label']} | {', '.join(cells)} |")
        out.append("")
    return "\n".join(out)


def write_manifest() -> None:
    rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8")))
    fields = list(rows[0].keys()) if rows else []
    if "bin" not in fields:
        fields.append("bin")
    for r in rows:
        r["bin"] = bins.manifest_value(r["stl"]) if r["stl"] in bins.ASSIGN else ""
    with MANIFEST.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote bin column for {len(rows)} rows -> {MANIFEST.relative_to(REPO)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plates", nargs="*", help="plate ids (default: every slicer/plates/*.3mf)")
    ap.add_argument("--markdown", action="store_true", help="print per-plate bin tables and exit")
    ap.add_argument("--write-manifest", action="store_true", help="write the `bin` column into MANIFEST.csv")
    ap.add_argument("--check", action="store_true", help="only verify 3MF contents against the plan and bins")
    ap.add_argument("--out", type=Path, default=OUT_DIR)
    a = ap.parse_args()

    problems = bins.check([p.rsplit("/", 1)[-1] for pl in PLATES.values() for _r, p, _q in pl["parts"]])
    for pr in problems:
        print("bins.py:", pr, file=sys.stderr)

    ids = a.plates or sorted(p.stem for p in PLATE_DIR.glob("*.3mf"))
    if a.write_manifest:
        write_manifest()
        if not a.plates and not a.markdown and not a.check:
            return 1 if problems else 0
    if a.markdown:
        print(markdown_tables(ids))
        return 1 if problems else 0

    warnings: list[str] = []
    if a.check:
        for pid in ids:
            _p, parts, w = load_plate(pid)
            warnings += w
            print(f"{pid}: {len(parts)} objects, bins {sorted({p.bin for p in parts})}")
    else:
        est = load_estimates()
        for pid in ids:
            w = render(pid, est, a.out)
            warnings += w
            print(f"{pid}: wrote {a.out.relative_to(REPO) if a.out.is_relative_to(REPO) else a.out}/{pid}.png + .svg")
    for w in warnings:
        print("WARNING:", w, file=sys.stderr)
    return 1 if (problems or warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
