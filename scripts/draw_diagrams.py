#!/usr/bin/env python3
"""Generate the explanatory diagrams the Voron 2.4r2 manual does not draw.

    python3 scripts/draw_diagrams.py            # write every SVG + MANIFEST.md
    python3 scripts/draw_diagrams.py --only 3 7 # write just those

Output: docs/manual/assets/diagrams/*.svg and docs/manual/assets/diagrams/MANIFEST.md.
Re-runnable and deterministic: it overwrites its own outputs and touches nothing else.
No chapter is edited — MANIFEST.md says where each diagram belongs.

Every fact drawn here is transcribed from a chapter step; the DIAGRAMS registry at
the bottom of this file records, per diagram, which steps it came from and which
details are drawn schematically rather than to a stated dimension.

Hand-built SVG strings: no svgwrite/cairosvg dependency. Dark-mode-safe — a light
background rect plus `color:` pinned on the <svg> root, so `fill="currentColor"`
text stays legible whether the page is light or dark and whether the file is
<img>-referenced or inlined.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "docs" / "manual" / "assets" / "diagrams"
PRINT_README = REPO / "docs" / "manual" / "print" / "README.md"

W = 1200

# ---------------------------------------------------------------- palette ----
INK = "#14181D"          # text + primary line work (pinned as `color` on <svg>)
MUTED = "#5C6675"        # captions, dimensions
FAINT = "#9AA3AF"        # construction lines
RULE = "#D6DAE0"         # panel borders
BG = "#FBFAF8"           # the light background rect
PANEL = "#FFFFFF"
ORANGE = "#E8751A"       # accent, [a]_ printed parts
ORANGE_F = "#FBE6D2"
BLUE = "#2A6FB5"         # frame / extrusion
BLUE_F = "#DCE9F6"
GREY = "#7E8794"         # hardware (bearings, fasteners, pulleys)
GREY_F = "#E7E9EC"
STEEL = "#B6BDC6"
BLACKPART = "#3E4550"    # black printed parts
BLACKPART_F = "#E2E4E8"
BELT_A = "#0E8F86"       # A belt
BELT_B = "#7A4FD6"       # B belt
RED = "#C0392B"          # mains live / warning
GREEN = "#2E7D32"        # protective earth
BROWN = "#8A5A2B"
AMBER = "#D98324"
AMBER_F = "#FBEBD3"
OK = "#2E7D32"
OK_F = "#DFF0DF"

FONT = ("Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, "
        "'Helvetica Neue', Arial, sans-serif")
MONO = "'SF Mono', ui-monospace, Menlo, Consolas, 'Liberation Mono', monospace"


# ------------------------------------------------------------- primitives ----
def esc(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


class Doc:
    """Collects SVG fragments, emits one document."""

    def __init__(self, height: int, title: str, subtitle: str = "", width: int = W):
        self.w = width
        self.h = height
        self.p: list[str] = []
        self.title = title
        self.subtitle = subtitle

    def add(self, frag: str) -> None:
        self.p.append(frag)

    # -- shapes -------------------------------------------------------------
    def rect(self, x, y, w, h, fill="none", stroke=INK, sw=2, rx=0, dash=None, op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{op}"' if op is not None else ""
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
                 f'rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>')

    def line(self, x1, y1, x2, y2, stroke=INK, sw=2, dash=None, cap="round", op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{op}"' if op is not None else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"{d}{o}/>')

    def circle(self, cx, cy, r, fill="none", stroke=INK, sw=2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def path(self, d, fill="none", stroke=INK, sw=2, dash=None, cap="round",
             join="round", marker=None, op=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        mk = f' marker-end="url(#{marker})"' if marker else ""
        o = f' opacity="{op}"' if op is not None else ""
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
                 f'stroke-linecap="{cap}" stroke-linejoin="{join}"{da}{mk}{o}/>')

    def poly(self, pts, fill="none", stroke=INK, sw=2):
        s = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.add(f'<polygon points="{s}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x, y, s, size=15, anchor="start", weight=400, fill="currentColor",
             family=FONT, ls=0, op=None, italic=False):
        o = f' opacity="{op}"' if op is not None else ""
        it = ' font-style="italic"' if italic else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" '
                 f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" '
                 f'letter-spacing="{ls}"{it}{o}>{esc(s)}</text>')

    def mono(self, x, y, s, size=14, anchor="start", weight=500, fill="currentColor"):
        self.text(x, y, s, size=size, anchor=anchor, weight=weight, fill=fill, family=MONO)

    def wrap(self, x, y, s, size=14, width_chars=70, lh=19, anchor="start",
             fill=MUTED, weight=400):
        """Very small greedy wrapper — the strings here are authored to fit."""
        words, line, out = s.split(), "", []
        for wd in words:
            t = (line + " " + wd).strip()
            if len(t) > width_chars and line:
                out.append(line)
                line = wd
            else:
                line = t
        if line:
            out.append(line)
        for i, ln in enumerate(out):
            self.text(x, y + i * lh, ln, size=size, anchor=anchor, fill=fill, weight=weight)
        return y + len(out) * lh

    # -- composites ---------------------------------------------------------
    def chip(self, x, y, w, h, label, fill=GREY_F, stroke=GREY, size=14, weight=600,
             rx=6, tcol="currentColor", mono=False, sw=2):
        self.rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=rx)
        f = MONO if mono else FONT
        self.text(x + w / 2, y + h / 2 + size * 0.36, label, size=size, anchor="middle",
                  weight=weight, fill=tcol, family=f)

    def dim_v(self, x, y1, y2, label, col=MUTED, side=-1, size=13):
        """Vertical dimension line with ticks and a rotated-free label."""
        self.line(x, y1, x, y2, stroke=col, sw=1.4)
        for y in (y1, y2):
            self.line(x - 5, y, x + 5, y, stroke=col, sw=1.4)
        tx = x + side * 9
        anchor = "end" if side < 0 else "start"
        self.text(tx, (y1 + y2) / 2 + 4, label, size=size, anchor=anchor, fill=col, weight=500)

    def dim_h(self, y, x1, x2, label, col=MUTED, above=True, size=13):
        self.line(x1, y, x2, y, stroke=col, sw=1.4)
        for x in (x1, x2):
            self.line(x, y - 5, x, y + 5, stroke=col, sw=1.4)
        self.text((x1 + x2) / 2, y - 8 if above else y + 17, label, size=size,
                  anchor="middle", fill=col, weight=500)

    def panel(self, x, y, w, h, title=None, sub=None):
        self.rect(x, y, w, h, fill=PANEL, stroke=RULE, sw=1.5, rx=10)
        if title:
            self.text(x + 18, y + 30, title, size=17, weight=700)
        if sub:
            self.text(x + 18, y + 51, sub, size=13.5, fill=MUTED)

    def leader(self, x1, y1, x2, y2, col=FAINT):
        self.line(x1, y1, x2, y2, stroke=col, sw=1.3)
        self.circle(x1, y1, 2.4, fill=col, stroke="none", sw=0)

    # -- document -----------------------------------------------------------
    def render(self) -> str:
        head = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'width="{self.w}" height="{self.h}" role="img" '
            f'aria-label="{esc(self.title)}" style="color:{INK}">',
            f'<title>{esc(self.title)}</title>',
            '<defs>',
            f'<marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>',
            f'<marker id="arwm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>',
            f'<marker id="arwa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" '
            f'markerHeight="6.5" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{BELT_A}"/></marker>',
            f'<marker id="arwb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" '
            f'markerHeight="6.5" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{BELT_B}"/></marker>',
            f'<marker id="arwo" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{ORANGE}"/></marker>',
            f'<marker id="arwr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{RED}"/></marker>',
            f'<marker id="arwg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{GREEN}"/></marker>',
            '<pattern id="hatch" width="7" height="7" patternTransform="rotate(45)" '
            'patternUnits="userSpaceOnUse">'
            f'<line x1="0" y1="0" x2="0" y2="7" stroke="{FAINT}" stroke-width="2.6"/></pattern>',
            '</defs>',
            f'<rect width="{self.w}" height="{self.h}" fill="{BG}"/>',
        ]
        return "\n".join(head + self.p + ["</svg>", ""])


def header(d: Doc, title: str, subtitle: str, source: str) -> float:
    """Title left, wrapped subtitle under it, chapter source right-aligned.

    Returns the y of the rule line, so panels can be placed under it.
    """
    d.text(40, 44, title, size=26, weight=700)
    y = 68
    if subtitle:
        y = d.wrap(40, 68, subtitle, size=14, width_chars=92, lh=19, fill=MUTED)
    d.text(d.w - 40, 68, source, size=12.5, anchor="end", fill=MUTED, weight=500)
    rule = max(y + 4, 90)
    d.line(40, rule, d.w - 40, rule, stroke=RULE, sw=1.5)
    return rule


def footer(d: Doc, note: str) -> None:
    """Bottom note, wrapped up from the foot of the page."""
    lines = []
    words, line = note.split(), ""
    for wd in words:
        t = (line + " " + wd).strip()
        if len(t) > 148 and line:
            lines.append(line)
            line = wd
        else:
            line = t
    if line:
        lines.append(line)
    y0 = d.h - 18 - (len(lines) - 1) * 17
    d.line(40, y0 - 22, d.w - 40, y0 - 22, stroke=RULE, sw=1.5)
    for i, ln in enumerate(lines):
        d.text(40, y0 + i * 17, ln, size=12.5, fill=MUTED)


# ------------------------------------------------------- belt path solver ----
def _rot90cw(v):
    return (-v[1], v[0])


def belt_geometry(nodes):
    """Exact tangent belt routing.

    nodes: [(x, y, r, s)] in order; s=-1 wraps clockwise on screen, s=+1
    counter-clockwise, r=0 for a plain endpoint. Returns a list of primitives:
      ('line', (x1,y1), (x2,y2))
      ('arc', (cx,cy), r, a_from, a_to, s)     angles in radians, atan2 convention
    Belt strands are the common tangents; wraps are the arcs between them.
    """
    tan = []
    for i in range(len(nodes) - 1):
        x1, y1, r1, s1 = nodes[i]
        x2, y2, r2, s2 = nodes[i + 1]
        dx, dy = x2 - x1, y2 - y1
        D = math.hypot(dx, dy)
        k = s2 * r2 - s1 * r1
        ratio = max(-1.0, min(1.0, k / D))
        theta = math.atan2(dy, dx) + math.asin(ratio)
        u = (math.cos(theta), math.sin(theta))
        w = _rot90cw(u)
        tan.append(((x1 + s1 * r1 * w[0], y1 + s1 * r1 * w[1]),
                    (x2 + s2 * r2 * w[0], y2 + s2 * r2 * w[1])))

    prims = []
    for i, (t1, t2) in enumerate(tan):
        prims.append(("line", t1, t2))
        if i + 1 < len(tan):
            cx, cy, r, s = nodes[i + 1]
            a = t2
            b = tan[i + 1][0]
            if r > 0:
                aa = math.atan2(a[1] - cy, a[0] - cx)
                bb = math.atan2(b[1] - cy, b[0] - cx)
                prims.append(("arc", (cx, cy), r, aa, bb, s))
            else:
                prims.append(("line", a, b))
    return prims


def prims_to_path(prims) -> str:
    d = []
    for p in prims:
        if p[0] == "line":
            (x1, y1), (x2, y2) = p[1], p[2]
            if not d:
                d.append(f"M {x1:.2f} {y1:.2f}")
            d.append(f"L {x2:.2f} {y2:.2f}")
        else:
            _, (cx, cy), r, aa, bb, s = p
            if s < 0:                                  # clockwise on screen
                delta = (bb - aa) % (2 * math.pi)
                sweep = 1
            else:
                delta = (aa - bb) % (2 * math.pi)
                sweep = 0
            large = 1 if delta > math.pi else 0
            bx, by = cx + r * math.cos(bb), cy + r * math.sin(bb)
            d.append(f"A {r:.2f} {r:.2f} 0 {large} {sweep} {bx:.2f} {by:.2f}")
    return " ".join(d)


def teeth_marks(d: Doc, prims, side, colour, length=6.5, step=13.0, sw=2.0,
                arcs_only=False, straight_mid=True):
    """Draw the toothed face of a belt as short ticks on one side of travel.

    side=+1 -> left of travel (screen), side=-1 -> right of travel.
    """
    for p in prims:
        if p[0] == "line":
            (x1, y1), (x2, y2) = p[1], p[2]
            L = math.hypot(x2 - x1, y2 - y1)
            if L < 12:
                continue
            u = ((x2 - x1) / L, (y2 - y1) / L)
            n = (u[1] * side, -u[0] * side)            # left of travel when side=+1
            if arcs_only:
                continue
            if straight_mid:
                n_ticks = 5
                span = min(L - 8, n_ticks * step)
                t0 = (L - span) / 2
                ts = [t0 + j * (span / max(1, n_ticks - 1)) for j in range(n_ticks)]
            else:
                ts = [t for t in _frange(6, L - 6, step)]
            for t in ts:
                px, py = x1 + u[0] * t, y1 + u[1] * t
                d.line(px, py, px + n[0] * length, py + n[1] * length,
                       stroke=colour, sw=sw, cap="butt")
        else:
            _, (cx, cy), r, aa, bb, s = p
            if s < 0:
                delta = (bb - aa) % (2 * math.pi)
                sgn = 1
            else:
                delta = (aa - bb) % (2 * math.pi)
                sgn = -1
            n_ticks = max(3, int(delta / 0.32))
            for j in range(n_ticks + 1):
                ang = aa + sgn * delta * j / n_ticks
                px, py = cx + r * math.cos(ang), cy + r * math.sin(ang)
                # travel direction along the arc
                u = (-math.sin(ang) * sgn, math.cos(ang) * sgn)
                n = (u[1] * side, -u[0] * side)
                d.line(px, py, px + n[0] * length, py + n[1] * length,
                       stroke=colour, sw=sw, cap="butt")


def _frange(a, b, st):
    x = a
    while x <= b:
        yield x
        x += st


# =============================================================== diagram 1 ===
def d01_bearing_stacks() -> Doc:
    """Six A/B bearing stacks as exploded vertical stacks."""
    d = Doc(1248, "Voron 2.4r2 — the six A/B bearing stacks")
    top = header(d, "The six A/B bearing stacks",
                 "Every F695 pair goes flange-out: the two plain faces touch, one brass M5 "
                 "precision spacer above the pair and one below.",
                 "Ch 04, Steps 04.7 · 04.21 · 04.22 · 04.30")

    PX = 7.0            # px per mm of stack height
    BEAR_H = 4 * PX     # F695 is 5 x 13 x 4 mm
    SPAC_H = 1 * PX     # brass M5 precision spacer, 1 mm
    GAP = 12
    BORE_W, BEAR_W, FLNG_W = 11.0, 13 * PX, 15 * PX

    def stack(x0, y0, cw, ch, title, sub, items, height_mm, bolt, note):
        d.panel(x0, y0, cw, ch)
        d.text(x0 + 18, y0 + 28, title, size=16.5, weight=700)
        d.text(x0 + 18, y0 + 48, sub, size=12.5, fill=MUTED)
        ax = x0 + 118                      # stack axis
        ly = y0 + 76
        total = sum(BEAR_H if it[0] == "b" else SPAC_H for it in items) + GAP * (len(items) - 1)
        d.line(ax, ly - 16, ax, ly + total + 20, stroke=FAINT, sw=1.4, dash="4 4")
        y = ly
        for kind, lbl in items:
            if kind == "b":
                flange_up = "flange up" in lbl
                d.rect(ax - BEAR_W / 2, y, BEAR_W, BEAR_H, fill=STEEL, stroke=GREY, sw=2, rx=2)
                fy = y + BEAR_H - 4 if not flange_up else y
                d.rect(ax - FLNG_W / 2, fy, FLNG_W, 4, fill=GREY, stroke=GREY, sw=1.4, rx=1)
                d.rect(ax - BORE_W / 2, y, BORE_W, BEAR_H, fill=PANEL, stroke=GREY, sw=1.2)
                h = BEAR_H
            else:
                d.rect(ax - FLNG_W / 2 - 4, y, FLNG_W + 8, SPAC_H,
                       fill=ORANGE_F, stroke=BROWN, sw=2, rx=1)
                h = SPAC_H
            d.leader(ax + FLNG_W / 2 + 8, y + h / 2, x0 + 210, y + h / 2)
            d.text(x0 + 216, y + h / 2 + 4.5, lbl, size=13.5, weight=600,
                   fill="currentColor" if kind == "b" else BROWN)
            y += h + GAP
        d.dim_v(x0 + 52, ly, y - GAP, height_mm, side=-1)
        d.text(x0 + 18, y0 + ch - 40, bolt, size=12.3, fill=MUTED)
        d.text(x0 + 18, y0 + ch - 21, note, size=12.3, fill=MUTED)

    PAIR = [("s", "M5 precision spacer"),
            ("b", "F695 — flange down"),
            ("b", "F695 — flange up"),
            ("s", "M5 precision spacer")]
    DOUBLE = PAIR + PAIR

    cw = 570
    cols = (36, 626)
    r0 = top + 20
    tall, short = 366, 250
    rows = (r0, r0 + tall + 16, r0 + 2 * (tall + 16))

    stack(cols[0], rows[0], cw, tall, "A DRIVE — near post",
          "the post nearer the motor bore (drawn left on p.74)", PAIR,
          "10 mm", "on the M5x30 BHCS through a_drive_frame_upper",
          "4 items, one bearing pair, one belt plane.")
    stack(cols[1], rows[0], cw, tall, "A DRIVE — far post",
          "the post farther from the motor bore (drawn right on p.74)", DOUBLE,
          "20 mm", "on the M5x30 BHCS through a_drive_frame_upper",
          "8 items. Two spacers touch in the middle — it carries both belt planes.")
    stack(cols[0], rows[1], cw, tall, "B DRIVE — far post",
          "mirrored: p.78 draws it on the left where p.74 drew it right", DOUBLE,
          "20 mm", "on the M5x30 BHCS through b_drive_frame_upper",
          "8 items. Same 20 mm stack as the A drive.")
    stack(cols[1], rows[1], cw, tall, "B DRIVE — near post",
          "the post nearer the motor bore (drawn right on p.78)", PAIR,
          "10 mm", "on the M5x30 BHCS through b_drive_frame_upper",
          "Six bearings and six spacers per drive — count before closing.")
    stack(cols[0], rows[2], cw, short, "A IDLER — front right",
          "front_idler_right_lower 21.6 mm + _upper 12.0 mm", PAIR,
          "10 mm", "on the M5x40 SHCS — aid bolt first, refitted from the top",
          "From the side: spacer, flange, plain, plain, flange, spacer.")
    stack(cols[1], rows[2], cw, short, "B IDLER — front left",
          "front_idler_left_lower 11.6 mm + _upper 21.6 mm", PAIR,
          "10 mm", "on the M5x40 SHCS — aid bolt first, refitted from the top",
          "A flange in the middle of a stack means one bearing is reversed.")

    footer(d, "16 x F695 flanged bearing (5 x 13 x 4 mm) and 16 x brass M5 precision spacer "
              "— the manual's \"M5 shim\" — in this chapter. Heights are the chapter's own: "
              "four items = 10 mm, eight items = 20 mm. Drawn to scale vertically and "
              "exploded for legibility; the assembled height is the dimension on the left of "
              "each stack.")
    return d


# =============================================================== diagram 2 ===
def d02_pulley_heights() -> Doc:
    """A/B handedness top view + the two pulley elevations."""
    d = Doc(800, "Voron 2.4r2 — A/B handedness and pulley heights")
    header(d, "A/B handedness and pulley height",
           "A = rear right, B = rear left, standing in front of an upright printer. "
           "The two pulley heights are what stack the two belt planes.",
           "Ch 04, Steps 04.2 · 04.24 · 04.26 · 04.33")

    # ---- top view ----
    ox, oy, sw_, sh = 60, 122, 470, 470
    d.panel(ox - 22, oy - 18, sw_ + 44, sh + 78, "Top view — where each assembly ends up")
    fx, fy, fw, fh = ox + 30, oy + 48, sw_ - 60, sh - 92
    d.rect(fx, fy, fw, fh, fill=BLUE_F, stroke=BLUE, sw=2.5, rx=4)
    d.text(fx + fw / 2, fy - 12, "REAR", size=13, anchor="middle", weight=700, fill=BLUE)
    d.text(fx + fw / 2, fy + fh + 24, "FRONT  (you stand here)", size=13,
           anchor="middle", weight=700, fill=BLUE)
    d.text(fx - 10, fy + fh / 2, "LEFT", size=13, anchor="end", weight=700, fill=BLUE)
    d.text(fx + fw + 10, fy + fh / 2, "RIGHT", size=13, weight=700, fill=BLUE)

    def unit(cx, cy, w, h, name, sub, port, colour, fillc):
        d.rect(cx - w / 2, cy - h / 2, w, h, fill=fillc, stroke=colour, sw=2.5, rx=7)
        d.text(cx, cy - 8, name, size=16, anchor="middle", weight=700)
        d.text(cx, cy + 11, sub, size=12, anchor="middle", fill=MUTED)
        if port:
            d.mono(cx, cy + 29, port, size=12, anchor="middle", fill=MUTED)

    ax, ay = fx + fw - 78, fy + 62
    bx, by = fx + 78, fy + 62
    unit(ax, ay, 132, 84, "A DRIVE", "rear right", "HV-STEPPER-1", BLACKPART, BLACKPART_F)
    unit(bx, by, 132, 84, "B DRIVE", "rear left", "HV-STEPPER-0", BLACKPART, BLACKPART_F)
    unit(fx + fw - 78, fy + fh - 58, 132, 74, "A IDLER", "front right", "", ORANGE, ORANGE_F)
    unit(fx + 78, fy + fh - 58, 132, 74, "B IDLER", "front left", "", ORANGE, ORANGE_F)

    # cable exits point at each other
    d.path(f"M {ax - 66:.0f} {ay + 46:.0f} L {bx + 66:.0f} {ay + 46:.0f}",
           stroke=MUTED, sw=1.8, dash="6 5", marker="arwm")
    d.path(f"M {bx + 66:.0f} {ay + 46:.0f} L {ax - 66:.0f} {ay + 46:.0f}",
           stroke=MUTED, sw=1.8, dash="6 5", marker="arwm")
    d.text((ax + bx) / 2, ay + 66, "motor cable exits inboard — \"pointing towards each other\"",
           size=12, anchor="middle", fill=MUTED)

    d.text(fx + fw / 2, fy + fh / 2 + 6, "Idlers are handed by belt plane, not mirrored:",
           size=12, anchor="middle", fill=MUTED)
    d.text(fx + fw / 2, fy + fh / 2 + 24,
           "right_lower 21.6 mm · left_lower 11.6 mm — the 10.0 mm",
           size=12, anchor="middle", fill=MUTED)
    d.text(fx + fw / 2, fy + fh / 2 + 42,
           "difference is 16.5 − 6.5 mm of pulley height", size=12, anchor="middle",
           fill=MUTED)

    # ---- elevations ----
    px, py, pw = 570, 104, 590
    d.panel(px, py, pw, 560, "Motor elevation — set with pulley_jig.stl",
            "both dimensions are motor face → underside of the teeth")

    def motor(x, y, hub_down, h_mm, label, sub, step, dim_side):
        """Side elevation of a stepper with its 20T 6 mm pulley, motor face up."""
        MW, MH = 150, 96
        face = y                                   # motor front face (top here)
        d.rect(x, y, MW, MH, fill=GREY_F, stroke=GREY, sw=2.5, rx=4)
        d.text(x + MW / 2, y + MH / 2 + 5, "0.9° A/B motor", size=12.5, anchor="middle",
               fill=MUTED)
        scale = 4.6                                # px per mm
        shaft_x = x + MW / 2
        teeth_h, hub_h = 6 * scale, 7 * scale
        gap = h_mm * scale
        teeth_bottom = face - gap                  # this is what the dimension measures
        if hub_down:
            # hub between the motor face and the teeth, teeth on top
            d.line(shaft_x, face, shaft_x, teeth_bottom - teeth_h - 10, stroke=STEEL, sw=9)
            d.rect(shaft_x - 13, teeth_bottom, 26, hub_h, fill=GREY_F, stroke=GREY, sw=2, rx=2)
            d.rect(shaft_x - 21, teeth_bottom - teeth_h, 42, teeth_h,
                   fill=ORANGE_F, stroke=ORANGE, sw=2.4, rx=2)
            d.text(shaft_x + 30, teeth_bottom - teeth_h / 2 + 4, "teeth up", size=12.5,
                   weight=600)
            d.text(shaft_x + 30, teeth_bottom + hub_h / 2 + 4, "hub down", size=12.5,
                   fill=MUTED)
        else:
            # teeth first, hub on top, shaft end through the hub
            d.line(shaft_x, face, shaft_x, teeth_bottom - teeth_h - hub_h - 12,
                   stroke=STEEL, sw=9)
            d.rect(shaft_x - 21, teeth_bottom - teeth_h, 42, teeth_h,
                   fill=ORANGE_F, stroke=ORANGE, sw=2.4, rx=2)
            d.rect(shaft_x - 13, teeth_bottom - teeth_h - hub_h, 26, hub_h,
                   fill=GREY_F, stroke=GREY, sw=2, rx=2)
            d.text(shaft_x + 30, teeth_bottom - teeth_h / 2 + 4, "teeth low", size=12.5,
                   weight=600)
            d.text(shaft_x + 30, teeth_bottom - teeth_h - hub_h / 2 + 4,
                   "hub up — shaft through", size=12.5, fill=MUTED)
        dx = x - 18 if dim_side < 0 else x + MW + 18
        d.line(min(dx, shaft_x - 24), face, max(dx, shaft_x - 24) if dim_side < 0 else dx,
               face, stroke=FAINT, sw=1.2, dash="3 3")
        d.line(min(dx, shaft_x - 24), teeth_bottom,
               max(dx, shaft_x - 24) if dim_side < 0 else dx, teeth_bottom,
               stroke=FAINT, sw=1.2, dash="3 3")
        d.dim_v(dx, teeth_bottom, face, f"{h_mm} mm", side=dim_side)
        d.text(x, y + MH + 32, label, size=16, weight=700)
        d.text(x, y + MH + 52, sub, size=12.5, fill=MUTED)
        d.mono(x, y + MH + 72, step, size=12.5, fill=MUTED)

    motor(px + 88, py + 212, True, 16.5, "A drive — 16.5 mm",
          "hub first, teeth up. A = rear right.", "Step 04.24", -1)
    motor(px + 342, py + 212, False, 6.5, "B drive — 6.5 mm",
          "teeth first, hub up. B = rear left.", "Step 04.33", -1)

    d.rect(px + 22, py + 424, pw - 44, 118, fill=AMBER_F, stroke=AMBER, sw=2, rx=8)
    d.text(px + 40, py + 452, "Stand the two motors side by side before you lock anything",
           size=14, weight=700)
    d.wrap(px + 40, py + 476,
           "The A pulley sits high with its teeth on top; the B pulley sits low with its hub "
           "on top. If both look the same, one is wrong — and no amount of Ch 07 belt tension "
           "will fix it. Both use the 20T 6 mm pulley; the four 9 mm 20T pulleys are the Z "
           "drive's.", size=12.8, width_chars=66, lh=18, fill=INK)

    footer(d, "A/B identity is from the LDO wiring guide and the LDO Klipper config "
              "(## A Stepper - Right / ## B Stepper - Left) — the official manual never "
              "states it. Motors are 0.9°, LDO-42STH48-2004MAH(VRN).")
    return d


# =============================================================== diagram 3 ===
def _corexy_panel(d: Doc, ox: float, oy: float, mirror: bool, belt_col: str,
                  marker: str, title: str, sub: str, steps: str,
                  own_drive: str, own_idler: str, other_drive: str):
    """One belt of the CoreXY loop, top view. Local box is 480 x 560 at (ox,oy).

    Geometry is exact: every straight run is a common tangent and every wrap a
    true arc (see belt_geometry). Laid out so the whole loop closes on
    axis-aligned lanes, then mirrored for the other belt.
    """
    LW, LH = 480, 560

    def X(x):
        return ox + (LW - x if mirror else x)

    def Y(y):
        return oy + y

    S = -1 if not mirror else 1          # wrap sense flips with the mirror
    R = 20                               # belt wrap radius
    # toothed face = left of travel for BOTH belts: the mirror flips handedness and
    # the reversed traversal (below) flips it back
    side = +1

    # stations, local coords (unmirrored / A-belt frame)
    XYL = (100, 300)          # left XY joint idler stack
    XYR = (380, 300)          # right XY joint idler stack
    FAR_L = (100, 90)         # rear-left drive unit: 4-bearing far post
    S1 = (380, 90)            # rear-right drive: 4-bearing far post (first wrap)
    PUL = (372, 146)          # rear-right drive: 20T motor pulley
    S2 = (420, 146)           # rear-right drive: 2-bearing near post
    FRI = (420, 480)          # front-right idler
    CAR = (240, 300)          # X carriage centre

    # ---- frame + extrusions ----
    d.rect(X(20) - (0 if not mirror else 440), Y(30), 440, 510,
           fill=BLUE_F, stroke=BLUE, sw=2.5, rx=4)
    # Y extrusions
    for (x0, x1) in ((92, 104), (406, 418)):
        xa, xb = sorted((X(x0), X(x1)))
        d.rect(xa, Y(108), xb - xa, 356, fill=BLUE, stroke=BLUE, sw=1, rx=2, op=0.30)
    xa, xb = sorted((X(104), X(406)))
    d.rect(xa, Y(291), xb - xa, 18, fill=BLUE, stroke=BLUE, sw=1, rx=2, op=0.30)
    d.text(X(240), Y(24), "REAR", size=12, anchor="middle", weight=700, fill=BLUE)
    d.text(X(240), Y(556), "FRONT", size=12, anchor="middle", weight=700, fill=BLUE)

    # ---- printed assemblies ----
    def block(x, y, w, h, label, lab_dy=-8, col=BLACKPART, fill=BLACKPART_F, tsize=12,
              lab_dx=0.0):
        xa2 = X(x + w) if mirror else X(x)
        d.rect(xa2, Y(y), w, h, fill=fill, stroke=col, sw=2, rx=6, dash="5 4")
        d.text(X(x + w / 2) + lab_dx, Y(y + lab_dy), label, size=tsize, anchor="middle",
               weight=700)

    block(334, 50, 122, 126, own_drive, -8)        # this belt's own drive unit
    block(58, 50, 86, 82, other_drive, -8)         # the other drive: a 90° turn only
    block(388, 446, 74, 70, own_idler, 86)
    # B panel: nudge the joint labels left, clear of the run that drops from the
    # rear-right post onto the right joint
    jdx = -12 if mirror else 0
    block(356, 258, 76, 84, "XY joint", -8, BLACKPART, "none", lab_dx=jdx)
    block(64, 258, 76, 84, "XY joint", -8, BLACKPART, "none", lab_dx=jdx)

    # X carriage with its clamp points
    xa2 = X(CAR[0] + 44) if mirror else X(CAR[0] - 44)
    d.rect(xa2, Y(CAR[1] - 42), 88, 84, fill=ORANGE_F, stroke=ORANGE, sw=2.5, rx=6)
    d.text(X(CAR[0]), Y(CAR[1] - 20), "X carriage", size=12.5, anchor="middle", weight=700)
    d.text(X(CAR[0]), Y(CAR[1] - 4), "left half", size=10.5, anchor="middle", fill=MUTED)
    d.text(X(CAR[0]), Y(CAR[1] + 10), "right half", size=10.5, anchor="middle", fill=MUTED)

    # ---- stations ----
    # Plain F695 stacks: the other drive's far post, this drive's two posts, the
    # front idler, and one XY joint (A: the left joint's upper pair, B: the right
    # joint's lower pair) — smooth back on all of them. The other XY joint carries
    # this belt's 20T toothed idler, wrapped teeth-on (A: right joint, Step 07.16;
    # B: left joint, Step 07.17). In local (A-frame) coords the toothed joint is
    # always XYR; the mirror puts B's at screen-left.
    for (cx, cy), lab in ((FAR_L, ""), (S1, ""), (S2, ""), (FRI, ""), (XYL, "")):
        d.circle(X(cx), Y(cy), 15, fill=GREY_F, stroke=GREY, sw=2.2)
    d.circle(X(PUL[0]), Y(PUL[1]), 15, fill=ORANGE_F, stroke=ORANGE, sw=2.6)
    d.circle(X(PUL[0]), Y(PUL[1]), 8, fill="none", stroke=ORANGE, sw=1.6)
    d.circle(X(XYR[0]), Y(XYR[1]), 15, fill=ORANGE_F, stroke=ORANGE, sw=2.6)
    d.circle(X(XYR[0]), Y(XYR[1]), 8, fill="none", stroke=ORANGE, sw=1.6, dash="2.5 2")
    # callouts sit in the free band under the carriage, clear of the belt legs.
    # A leaves smooth (left joint) and returns teeth-on (right joint); B leaves
    # teeth-on (left joint) and returns smooth (right joint).
    if not mirror:
        t1, t2 = "return turn: TEETH ON", "the upper 20T idler here"
        p1, p2 = "leaving turn: smooth back", "on the upper F695 pair"
    else:
        t1, t2 = "leaving turn: TEETH ON", "the lower 20T idler here"
        p1, p2 = "return turn: smooth back", "on the lower F695 pair"
    d.text(X(312), Y(XYR[1] + 74), t1, size=10.8, anchor="middle", fill=ORANGE, weight=700)
    d.text(X(312), Y(XYR[1] + 88), t2, size=10.8, anchor="middle", fill=ORANGE, weight=600)
    d.text(X(132), Y(XYL[1] + 74), p1, size=10.8, anchor="middle", fill=MUTED, weight=600)
    d.text(X(132), Y(XYL[1] + 88), p2, size=10.8, anchor="middle", fill=MUTED)

    # ---- the belt ----
    def N(p, s=S):
        return (X(p[0]), Y(p[1]), R, s)

    if not mirror:
        # A: leaves the LEFT carriage half heading left on the front lane; first
        # turn the left joint (upper F695, smooth), last turn the right joint
        # (upper 20T, teeth-on).
        start = (X(CAR[0] - 44), Y(320), 0, 0)
        end = (X(CAR[0] + 44), Y(280), 0, 0)
        nodes = [start,
                 N(XYL, S), N(FAR_L, S), N(S1, S), N(PUL, -S), N(S2, S), N(FRI, S),
                 N(XYR, -S), end]
    else:
        # B: the same stations mirrored, but traversed the other way round the
        # frame — both belts leave the LEFT carriage half heading left (p.131), so
        # B's first turn is the left joint (screen-left = local XYR: its lower 20T,
        # teeth-on, turning FORWARD to the front idler) and its last the right
        # joint (local XYL: lower F695, smooth). Reversal negates every wrap sense.
        start = (X(CAR[0] + 44), Y(280), 0, 0)      # screen-left edge of the carriage
        end = (X(CAR[0] - 44), Y(320), 0, 0)        # screen-right edge
        nodes = [start,
                 N(XYR, S), N(FRI, -S), N(S2, -S), N(PUL, S), N(S1, -S), N(FAR_L, -S),
                 N(XYL, -S), end]
    prims = belt_geometry(nodes)
    d.path(prims_to_path(prims), stroke=belt_col, sw=3.4)
    teeth_marks(d, prims, side, belt_col, length=6, sw=1.8)

    # travel arrows (A-frame directions; B runs the loop the other way, so flip)
    def arrow(x0, y0, x1, y1):
        if mirror:
            x0, y0, x1, y1 = x1, y1, x0, y0
        d.path(f"M {X(x0)} {Y(y0)} L {X(x1)} {Y(y1)}", stroke=belt_col, sw=3.2,
               marker=marker)

    arrow(80, 210, 80, 178)
    arrow(190, 70, 244, 70)
    arrow(440, 330, 440, 372)
    arrow(400, 408, 400, 366)

    # ---- callouts ----
    d.text(X(250), Y(212), "S-wrap at this belt's OWN drive:", size=11.5,
           anchor="middle", fill=MUTED, weight=600)
    d.text(X(250), Y(228), "stack → 20T motor pulley → stack", size=11.5,
           anchor="middle", fill=MUTED)
    d.text(X(178), Y(152), "90° turn only, on the", size=10.8, anchor="middle", fill=MUTED)
    d.text(X(178), Y(166), "other drive's 4-bearing", size=10.8, anchor="middle",
           fill=MUTED)
    d.text(X(178), Y(180), "stack", size=10.8, anchor="middle", fill=MUTED)
    d.text(X(230), Y(504), "180° U-turn at the front idler —", size=10.8,
           anchor="middle", fill=MUTED)
    d.text(X(230), Y(518), "smooth back on the stack, teeth", size=10.8,
           anchor="middle", fill=MUTED)
    d.text(X(230), Y(532), "outward on both runs", size=10.8, anchor="middle", fill=MUTED)


def d03_belt_path() -> Doc:
    d = Doc(1020, "Voron 2.4r2 — CoreXY belt path")
    top = header(d, "CoreXY belt path — A belt and B belt",
                 "The two belts are stacked at different heights and never cross. Each belt "
                 "stays in one horizontal plane for its whole loop, and its toothed face "
                 "never changes sides.",
                 "Ch 07, Steps 07.3 · 07.4 · 07.9 · 07.13 · 07.15 · 07.16 · 07.17 · 07.22")

    d.panel(30, top + 16, 560, 672, "A belt  —  A drive is rear RIGHT",
            "two parallel runs on the right side, one on the left")
    _corexy_panel(d, 55, top + 78, False, BELT_A, "arwa", "", "", "",
                  "A drive", "A idler", "B drive")

    d.panel(610, top + 16, 560, 672, "B belt  —  B drive is rear LEFT",
            "two parallel runs on the left side, one on the right")
    _corexy_panel(d, 635, top + 78, True, BELT_B, "arwb", "", "", "",
                  "B drive", "B idler", "A drive")

    # legend — two rows
    ly = top + 704
    d.rect(30, ly, 1140, 88, fill=PANEL, stroke=RULE, sw=1.5, rx=8)
    r1, r2 = ly + 24, ly + 60
    lx = 50
    d.line(lx, r1, lx + 34, r1, stroke=BELT_A, sw=3.4)
    for i in range(4):
        d.line(lx + 4 + i * 9, r1, lx + 4 + i * 9, r1 + 7, stroke=BELT_A, sw=1.8,
               cap="butt")
    d.text(lx + 42, r1 + 5, "A belt — ticks mark the toothed face", size=12.5, weight=600)
    lx = 372
    d.line(lx, r1, lx + 34, r1, stroke=BELT_B, sw=3.4)
    for i in range(4):
        d.line(lx + 4 + i * 9, r1, lx + 4 + i * 9, r1 + 7, stroke=BELT_B, sw=1.8,
               cap="butt")
    d.text(lx + 42, r1 + 5, "B belt", size=12.5, weight=600)
    d.circle(530, r1, 9, fill=GREY_F, stroke=GREY, sw=2)
    d.text(546, r1 + 5, "F695 stack — smooth back rides here (drives, front idler, one XY "
                        "joint: A's left, B's right)", size=12.5)
    d.circle(60, r2, 9, fill=ORANGE_F, stroke=ORANGE, sw=2.4)
    d.text(76, r2 + 5, "20T motor pulley — teeth engage here", size=12.5)
    d.circle(400, r2, 9, fill=ORANGE_F, stroke=ORANGE, sw=2.4)
    d.circle(400, r2, 4.5, fill="none", stroke=ORANGE, sw=1.4, dash="2 1.5")
    d.text(416, r2 + 5, "20T idler at the other XY joint — wraps teeth-on (A: right joint, "
                        "Step 07.16 · B: left joint, Step 07.17) — never twist a belt",
           size=12.5)

    footer(d, "Clamp points: one end of BOTH belts goes into the left X carriage half, one "
              "into the upper slot and one into the lower, teeth facing the front of the "
              "machine (Step 07.9); both tails are captured by the right half (Step 07.24). "
              "The toothed face never changes sides: smooth back on every plain F695 "
              "stack, teeth into the motor pulley and into this belt's one toothed "
              "XY-joint idler (A: right joint, B: left). Both X runs physically lie in "
              "front of the X extrusion — each panel draws one behind it so the two lanes "
              "read apart. Lane spacing inside each drive unit is schematic — the chapter "
              "fixes the order of the wraps, not their top-view coordinates.")
    return d


# =============================================================== diagram 4 ===
def d04_z_drive() -> Doc:
    d = Doc(880, "Voron 2.4r2 — Z drive gear train and Z belt loop")
    top = header(d, "Z drive gear train and Z belt loop",
                 "One corner, side view. Motor 16T → 188 mm closed loop → 80T on the shaft "
                 "→ 20T on the same shaft → the Z belt that lifts the gantry. "
                 "gear_ratio: 80:16.",
                 "Ch 02, Steps 02.17 · 02.19 · 02.21 · 02.27 · Ch 06, Step 06.18")

    # ---------- left panel: the whole corner ----------
    px, py = 30, top + 16
    ph = 700
    d.panel(px, py, 344, ph, "One corner, side view",
            "one strand, both ends clamped at the Z joint")
    up_x = px + 74                      # frame upright
    d.rect(up_x, py + 78, 24, ph - 176, fill=BLUE_F, stroke=BLUE, sw=2.5, rx=3)
    d.text(up_x - 6, py + 72, "frame upright", size=11, anchor="middle", fill=BLUE,
           weight=600)

    # Z idler at the top
    idl = (up_x + 72, py + 128)
    d.rect(idl[0] - 32, idl[1] - 38, 70, 78, fill=BLACKPART_F, stroke=BLACKPART, sw=2, rx=6)
    d.circle(idl[0], idl[1], 21, fill=GREY_F, stroke=GREY, sw=2.4)
    d.circle(idl[0], idl[1], 6, fill=PANEL, stroke=GREY, sw=1.6)
    d.text(idl[0] + 46, idl[1] - 14, "z_tensioner_bracket", size=11.5, weight=600)
    d.text(idl[0] + 46, idl[1] + 3, "20T 9 mm idler on an", size=11, fill=MUTED)
    d.text(idl[0] + 46, idl[1] + 18, "M5x30 BHCS axle", size=11, fill=MUTED)
    d.rect(idl[0] - 12, idl[1] + 42, 24, 24, fill=ORANGE_F, stroke=ORANGE, sw=2, rx=3)
    d.text(idl[0] + 46, idl[1] + 52, "[a]_z_tensioner_9mm", size=11, fill=ORANGE, weight=600)
    d.text(idl[0] + 46, idl[1] + 67, "M3x16 into a captive nut", size=11, fill=MUTED)

    # Z drive at the bottom
    drv = (up_x + 72, py + ph - 152)
    d.rect(drv[0] - 44, drv[1] - 50, 92, 104, fill=BLACKPART_F, stroke=BLACKPART, sw=2, rx=6)
    d.circle(drv[0], drv[1], 21, fill=GREY_F, stroke=GREY, sw=2.4)
    d.circle(drv[0], drv[1], 6, fill=PANEL, stroke=GREY, sw=1.6)
    d.text(drv[0] + 56, drv[1] - 22, "z_drive_main", size=11.5, weight=600)
    d.text(drv[0] + 56, drv[1] - 6, "20T 9 mm pulley on", size=11, fill=MUTED)
    d.text(drv[0] + 56, drv[1] + 9, "the 5 x 60 shaft", size=11, fill=MUTED)

    # Z joint on the gantry
    zj_y = py + 380
    d.rect(up_x - 6, zj_y - 24, 92, 48, fill=BLACKPART_F, stroke=BLACKPART, sw=2, rx=5)
    d.text(up_x + 92, zj_y - 4, "Z joint / Z bearing block", size=11.5, weight=600)
    d.text(up_x + 92, zj_y + 12, "both belt ends clamped here", size=11, fill=MUTED)
    d.line(up_x - 36, zj_y, up_x - 8, zj_y, stroke=BLUE, sw=6)
    d.text(up_x - 40, zj_y + 4, "gantry", size=11, anchor="end", fill=BLUE, weight=600)

    # the Z belt: down the inside, round the drive, up the outside, over the idler, back down
    inner_x = drv[0] - 21
    outer_x = drv[0] + 21
    bp = (f"M {inner_x} {zj_y - 4} L {inner_x} {drv[1]} "
          f"A 21 21 0 1 0 {outer_x} {drv[1]} "
          f"L {outer_x} {idl[1]} "
          f"A 21 21 0 0 0 {inner_x} {idl[1]} "
          f"L {inner_x} {zj_y + 4}")
    d.path(bp, stroke=BELT_A, sw=3.4)
    for y in range(int(zj_y) + 34, int(drv[1]) - 28, 26):
        d.line(inner_x, y, inner_x + 7, y, stroke=BELT_A, sw=1.8, cap="butt")
    for y in range(int(idl[1]) + 34, int(zj_y) - 26, 26):
        d.line(inner_x, y, inner_x + 7, y, stroke=BELT_A, sw=1.8, cap="butt")
    for y in range(int(idl[1]) + 40, int(drv[1]) - 36, 26):
        d.line(outer_x, y, outer_x - 7, y, stroke=BELT_A, sw=1.8, cap="butt")
    d.text(px + 18, py + ph - 66, "Z belt — teeth face inward, onto both pulleys",
           size=12, fill=BELT_A, weight=600)
    d.text(px + 18, py + ph - 46, "the belt runs flat, no half-twist: the teeth of the two",
           size=11.3, fill=MUTED)
    d.text(px + 18, py + ph - 30, "vertical runs face each other, smooth back outward on both",
           size=11.3, fill=MUTED)

    # ---------- middle panel: the drive internals ----------
    mx, my, mw, mh = 394, top + 16, 452, 484
    d.panel(mx, my, mw, mh, "Inside the Z drive",
            "16T motor pulley → 188 mm closed loop → 80T")
    mot = (mx + 92, my + 288)
    d.rect(mot[0] - 52, mot[1] - 30, 104, 100, fill=GREY_F, stroke=GREY, sw=2.5, rx=4)
    d.text(mot[0], mot[1] + 42, "Z motor", size=12.5, anchor="middle", fill=MUTED, weight=600)
    d.circle(mot[0], mot[1] - 54, 26, fill=ORANGE_F, stroke=ORANGE, sw=2.6)
    d.circle(mot[0], mot[1] - 54, 9, fill=PANEL, stroke=GREY, sw=1.6)
    d.text(mot[0], mot[1] - 50, "16T", size=13, anchor="middle", weight=700)
    d.line(mot[0] - 60, mot[1] - 30, mot[0] - 28, mot[1] - 30, stroke=FAINT, sw=1.2,
           dash="3 3")
    d.line(mot[0] - 60, mot[1] - 80, mot[0] - 28, mot[1] - 80, stroke=FAINT, sw=1.2,
           dash="3 3")
    d.dim_v(mot[0] - 60, mot[1] - 80, mot[1] - 30, "10.7 mm", side=-1)
    d.text(mx + 18, my + 356, "10.7 mm = motor face → underside of the pulley",
           size=11.5, fill=MUTED)
    d.text(mx + 18, my + 374, "the only 16T pulleys in the printer — check the count",
           size=11.5, fill=MUTED)

    big = (mx + 306, my + 208)
    d.circle(big[0], big[1], 74, fill=GREY_F, stroke=GREY, sw=2.6)
    d.circle(big[0], big[1], 12, fill=PANEL, stroke=GREY, sw=1.8)
    d.text(big[0], big[1] + 5, "80T", size=17, anchor="middle", weight=700)
    d.text(big[0], big[1] + 100, "on the 5 x 60 shaft", size=11.5, anchor="middle",
           fill=MUTED)

    # 188 mm closed loop between 16T and 80T
    dx, dy = big[0] - mot[0], big[1] - (mot[1] - 54)
    L = math.hypot(dx, dy)
    r1, r2 = 26, 74
    ang = math.atan2(dy, dx)
    a = math.acos(max(-1.0, min(1.0, (r2 - r1) / L)))
    p1 = (mot[0] + r1 * math.cos(ang + a), (mot[1] - 54) + r1 * math.sin(ang + a))
    p2 = (big[0] + r2 * math.cos(ang + a), big[1] + r2 * math.sin(ang + a))
    p3 = (big[0] + r2 * math.cos(ang - a), big[1] + r2 * math.sin(ang - a))
    p4 = (mot[0] + r1 * math.cos(ang - a), (mot[1] - 54) + r1 * math.sin(ang - a))
    d.path(f"M {p1[0]:.1f} {p1[1]:.1f} L {p2[0]:.1f} {p2[1]:.1f} "
           f"A {r2} {r2} 0 1 0 {p3[0]:.1f} {p3[1]:.1f} "
           f"L {p4[0]:.1f} {p4[1]:.1f} "
           f"A {r1} {r1} 0 1 0 {p1[0]:.1f} {p1[1]:.1f} Z",
           stroke=BELT_B, sw=3.4)
    d.text(mx + mw / 2, my + 74, "Gates 2GT closed loop, 6 mm x 188 mm", size=12,
           anchor="middle", weight=600, fill=BELT_B)
    d.text(mx + mw / 2, my + 91, "teeth inward — captive once the drive is closed",
           size=11.5, anchor="middle", fill=MUTED)

    # tensioner cam
    d.rect(mx + 26, my + 398, 120, 32, fill=ORANGE_F, stroke=ORANGE, sw=2.4, rx=6)
    d.text(mx + 86, my + 419, "[a]_belt_tensioner", size=11.5, anchor="middle", weight=700,
           fill=ORANGE)
    d.path(f"M {mx + 150} {my + 414} L {mx + 190} {my + 414}", stroke=ORANGE, sw=2.4,
           marker="arwo")
    d.text(mx + 196, my + 410, "closing the cam pushes the motor", size=11.5, fill=MUTED)
    d.text(mx + 196, my + 426, "away from the fixed drive body", size=11.5, fill=MUTED)

    # ---------- right panel: the shaft stack ----------
    rx0, ry0, rw, rh = 866, top + 16, 304, 484
    d.panel(rx0, ry0, rw, rh, "The shaft stack",
            "outward from the 20T pulley (Step 02.19)")
    sx, sy = rx0 + 26, ry0 + 74
    items = [("625-2RS bearing", GREY_F, GREY, 26),
             ("GT2 20T 9 mm pulley", ORANGE_F, ORANGE, 30),
             ("M5 precision spacer", ORANGE_F, BROWN, 11),
             ("M5 precision spacer", ORANGE_F, BROWN, 11),
             ("625-2RS bearing", GREY_F, GREY, 26),
             ("M5 precision spacer", ORANGE_F, BROWN, 11),
             ("M5 precision spacer", ORANGE_F, BROWN, 11),
             ("GT2 80T pulley", GREY_F, GREY, 36),
             ("625-2RS bearing", GREY_F, GREY, 26)]
    total_h = sum(h for *_, h in items) + (len(items) - 1) * 6
    d.line(sx + 26, sy - 24, sx + 26, sy + total_h + 26, stroke=STEEL, sw=10)
    y = sy
    for name, fill, stroke, h in items:
        wgt = 62 if "80T" in name or "20T" in name else 46
        d.rect(sx + 26 - wgt / 2, y, wgt, h, fill=fill, stroke=stroke, sw=2, rx=3)
        d.text(sx + 68, y + h / 2 + 4.5, name, size=12,
               weight=600 if "spacer" not in name else 500,
               fill="currentColor" if "spacer" not in name else BROWN)
        y += h + 6
    d.text(sx + 68, sy - 20, "shaft end", size=11, fill=MUTED)
    d.dim_h(sy + total_h + 46, sx - 8, sx + 60, "33 mm of shaft past the 20T", above=False)

    footer(d, "Z gearing is stock: the LDO Klipper config carries [stepper_z] "
              "rotation_distance: 40 and gear_ratio: 80:16. Four identical drives, two "
              "'a' and two 'b'. The Z idler's pulley must face the same way as the 20T "
              "in the drive directly below it, or the Z belt does not run in one plane. "
              "A tooth visible on the outside of either vertical run means the belt is "
              "twisted (Ch 06).")
    return d


# =============================================================== diagram 5 ===
def d05_mains_pe() -> Doc:
    d = Doc(956, "Voron 2.4r2 — mains path and protective-earth chain")
    header(d, "Mains path and the protective-earth chain",
           "inlet + switch + fuse → WAGO bus → PSU · SSR → bed heater. PE is never "
           "switched and never fused.",
           "Ch 00a, Steps 00a.6 · 00a.10 · Ch 10, Steps 10.5 · 10.10 · 10.27")

    def box(x, y, w, h, title, lines, stroke=INK, fill=PANEL, tsize=15):
        d.rect(x, y, w, h, fill=fill, stroke=stroke, sw=2.4, rx=8)
        d.text(x + 14, y + 24, title, size=tsize, weight=700)
        yy = y + 44
        for ln, col in lines:
            d.text(x + 14, yy, ln, size=12.3, fill=col)
            yy += 16.5

    # ---- the mains chain, left to right ----
    y0 = 118
    box(40, y0, 176, 128, "Wall socket", [
        ("on an RCD / GFCI outlet", MUTED),
        ("you can reach without", MUTED),
        ("reaching over the printer", MUTED),
        ("L  ·  N  ·  PE", MUTED)])

    box(250, y0, 232, 190, "AC inlet module", [
        ("power_inlet_IECGS_1mm", MUTED),
        ("C14 + illuminated rocker", MUTED),
        ("+ fuse drawer, one body", MUTED),
        ("", MUTED),
        ("fuse: in series with LIVE only", RED),
        ("rocker: switches L and N", INK),
        ("earth spade: neither switched", GREEN),
        ("nor fused — straight through", GREEN)])

    box(516, y0, 214, 190, "WAGO bus  (3 x 221-415)", [
        ("labelled left to right", MUTED),
        ("", MUTED),
        ("N   blue    5-way", BLUE),
        ("L   brown   5-way", BROWN),
        ("PE  yellow  5-way", GREEN),
        ("", MUTED),
        ("no copper outside a port", MUTED)])

    box(764, y0, 200, 160, "PSU — Meanwell", [
        ("LRS-200-24 (RSP-200-24 EU)", MUTED),
        ("selector at 115 V for a US", MUTED),
        ("110/120 V supply", MUTED),
        ("", MUTED),
        ("AC screws, from the outer end:", INK),
        ("1 L  ·  2 N  ·  3 FG (earth)", INK),
        ("L outermost, FG beside −V", MUTED)])

    box(998, y0, 162, 160, "24 V out", [
        ("+V / −V feed:", MUTED),
        ("Leviathan Vin 24V", MUTED),
        ("Leviathan Vin 24-48V", MUTED),
        ("USB adapter PCB", MUTED),
        ("", MUTED),
        ("(diagram 6 has the", MUTED),
        ("full 24 V map)", MUTED)])

    def flow(x1, y, x2, col=INK, mk="arw", label=None):
        d.path(f"M {x1} {y} L {x2} {y}", stroke=col, sw=2.6, marker=mk)
        if label:
            d.text((x1 + x2) / 2, y - 9, label, size=11.5, anchor="middle", fill=col,
                   weight=600)

    flow(216, y0 + 64, 248, BROWN, "arw", "C13 cord")
    flow(482, y0 + 96, 514, BROWN)
    flow(730, y0 + 96, 762, BROWN)
    flow(964, y0 + 96, 996, INK)

    # ---- SSR + bed ----
    ys = 372
    box(516, ys, 268, 176, "SSR — Omron G3NB-210B-1", [
        ("1 LOAD 2   AC switching side", INK),
        ("3 + INPUT 4 −   DC control side", INK),
        ("", MUTED),
        ("LOAD 2  ←  mains L, from the L WAGO", BROWN),
        ("LOAD 1  →  bed L", RED),
        ("INPUT 3 +  ←  red, Leviathan HEATBED +", RED),
        ("INPUT 4 −  ←  black", INK),
        ("no terminal cover on this part", MUTED)])

    box(842, ys, 318, 240, "Build plate", [
        ("AC bed heater pad, mains-voltage", MUTED),
        ("125 °C thermal fuse inside the pad", MUTED),
        ("", MUTED),
        ("Bed L   → SSR LOAD 1", RED),
        ("Bed N   → the N WAGO", BLUE),
        ("Bed PE  → the PE WAGO", GREEN),
        ("Bed TH  → 2x2 XH splicer → Leviathan TH1", MUTED),
        ("", MUTED),
        ("PE lands on the plate's own pre-fitted", GREEN),
        ("M4x6 BHCS + serrated washer: back it out", GREEN),
        ("3 turns, ring under the washer, retighten", MUTED)])

    # L from the WAGO down to the SSR, and bed L across
    d.path(f"M {600} {y0 + 190} L {600} {ys}", stroke=BROWN, sw=2.6, marker="arw")
    d.text(608, y0 + 220, "L → LOAD 2", size=11.5, fill=BROWN, weight=600)
    d.path(f"M {784} {ys + 88} L {840} {ys + 88}", stroke=RED, sw=2.6, marker="arwr")
    d.text(812, ys + 78, "bed L", size=11.5, anchor="middle", fill=RED, weight=600)
    d.rect(300, ys + 34, 196, 74, fill=PANEL, stroke=RED, sw=2.2, rx=8)
    d.text(314, ys + 58, "Leviathan HEATBED", size=13.5, weight=700)
    d.text(314, ys + 78, "the only thing that", size=12, fill=MUTED)
    d.text(314, ys + 94, "switches the bed", size=12, fill=MUTED)
    d.path(f"M {496} {ys + 71} L {514} {ys + 71}", stroke=RED, sw=2.6, marker="arwr")

    # ---- PE chain ----
    yp = 626
    d.rect(40, yp, 440, 250, fill=PANEL, stroke=GREEN, sw=2.4, rx=10)
    d.text(58, yp + 28, "The protective-earth chain — five branches", size=16, weight=700,
           fill=GREEN)
    rows = [("Supply", "wall socket earth → C14 E pin, through the C13 cord"),
            ("Bus", "C14 E → the yellow PE WAGO"),
            ("PSU", "PE WAGO → Meanwell screw 3 FG (innermost AC screw)"),
            ("Frame", "PE WAGO → frame extrusion; ring terminal between"),
            ("", "two M5 locking washers, on scraped bare metal"),
            ("Bed", "build plate → PE WAGO, on the plate's own"),
            ("", "M4x6 BHCS and its serrated washer")]
    yy = yp + 56
    for a, b in rows:
        if a:
            d.text(58, yy, a, size=12.8, weight=700)
        d.text(126, yy, b, size=12.3, fill=MUTED)
        yy += 20
    d.text(58, yy + 12, "Never switched, never fused. C14 earth pin to a screw head or T-nut",
           size=12, fill=MUTED)
    d.text(58, yy + 29, "at any frame corner (never the anodised face) must read under 2–3 Ω",
           size=12, fill=MUTED)
    d.text(58, yy + 46, "— the check that makes the whole machine safe to touch (10.18, 10.77).",
           size=12, fill=MUTED)

    # PE arrows on the drawing
    for (x1, y1, x2, y2) in ((622, y0 + 190, 622, 560),):
        pass
    d.path(f"M {706} {y0 + 190} L {706} {ys - 4}", stroke=GREEN, sw=2.4, dash="7 5",
           marker="arwg")
    d.text(716, y0 + 206, "PE bus continues to the", size=11.5, fill=GREEN, weight=600)
    d.text(716, y0 + 222, "frame, the PSU and the", size=11.5, fill=GREEN, weight=600)
    d.text(716, y0 + 238, "bed — five branches below", size=11.5, fill=GREEN, weight=600)

    d.rect(516, yp + 84, 644, 148, fill=AMBER_F, stroke=AMBER, sw=2.2, rx=10)
    d.text(534, yp + 112, "Two things the marking on the SSR does not mean", size=15,
           weight=700)
    d.wrap(534, yp + 136,
           "The SSR body reads EARTH THE MOUNTING RAIL and this build does not run a PE "
           "conductor to the DIN rail — the rail is bonded only incidentally, through "
           "anodising. If your local rules require an earthed rail that is a mains change, "
           "not a bench decision. And the inlet fuse protects the SSR against a short; it "
           "does not protect a person — that is the RCD and this PE chain.",
           size=12.3, width_chars=78, lh=17.5, fill=INK)

    footer(d, "Every mains connection is made with the C13 cord in another room. Screw "
              "terminals (PSU 1 L / 2 N / 3 FG, SSR LOAD 1/2) get VE0508 ferrules; WAGO 221 "
              "levers take bare stranded core stripped to 11 mm. Fuse rating: (verify on "
              "bench) — LDO does not publish the value.")
    return d


# =============================================================== diagram 6 ===
def d06_harness_map() -> Doc:
    LEVI = [
        ("MOTION — steppers", [
            ("A motor cable", "4-pin JST-XH", "HV-STEPPER-1", "TMC5160 · rear right"),
            ("B motor cable", "4-pin JST-XH", "HV-STEPPER-0", "TMC5160 · rear left"),
            ("Z0 motor cable", "4-pin JST-XH", "STEPPER-0", "front left"),
            ("Z1 motor cable", "4-pin JST-XH", "STEPPER-1", "rear left"),
            ("Z2 motor cable", "4-pin JST-XH", "STEPPER-2", "rear right"),
            ("Z3 motor cable", "4-pin JST-XH", "STEPPER-3", "front right"),
            ("— nothing —", "", "STEPPER-4", "empty — extruder is on the toolboard"),
        ]),
        ("SENSE — thermistors, endstops, probe", [
            ("Bed TH", "2-pin JST-XH", "TH1", "PA2 · not TH0"),
            ("— nothing —", "", "TH0", "empty on a Nitehawk build"),
            ("XY endstop — XES / X Stop", "3-pin", "X-ENDSTOP", "gantry endstop PCB"),
            ("XY endstop — YES / Y Stop", "3-pin", "Y-ENDSTOP", "gantry endstop PCB"),
            ("Nozzle probe (Z endstop)", "3-pin", "Z-ENDSTOP", "LDO nozzle probe"),
            ("— nothing —", "", "Z-PROBE", "empty all build — probe is nhk:PC15"),
        ]),
        ("FANS AND LIGHT", [
            ("PCB FAN — 2 x 6020 via a 3x2 XH splicer", "", "FAN2", "PF7 · jumper at 24 V"),
            ("FILTER FAN — Nevermore", "", "FAN3", "PF9 · jumper at 24 V"),
            ("LED STRIP — ceiling junction PCB", "2-pin JST-XH", "LED-Strip",
             "PE6 · dimmable, not Neopixel"),
            ("— nothing —", "", "FAN0 · FAN1", "unused, unjumpered on a Nitehawk"),
        ]),
        ("POWER — 24 V", [
            ("24V PSU to MB   (24V end)", "screw terminal", "Vin 24V / Board",
             "TO MB end on the PSU +V / −V"),
            ("HV to MB HV   (HV end)", "screw terminal", "Vin 24-48V / HV-Steppers",
             "feeds the two TMC5160s"),
            ("SSR to MB   (To SSR end)", "screw terminal", "HEATBED",
             "red = +; SIG end on INPUT 3 / 4"),
        ]),
        ("DATA", [
            ("USB-A ↔ USB-C, short", "", "Leviathan USB-C", "to the Raspberry Pi"),
            ("Ethernet patch", "RJ45", "Pi RJ45 → rear keystone", "CAT6 insert"),
            ("DSI ribbon", "FFC", "Pi DISPLAY → BTT Pi TFT43",
             "contacts forward at the Pi, up at the screen"),
            ("USB", "", "Pi → USB adapter PCB", "carries the toolboard's USB data"),
        ]),
    ]

    NHK = [
        ("THE UMBILICAL", [
            ("Toolhead umbilical — bay end", "Micro-Fit 3.0", "USB adapter PCB",
             "never mate or break it powered"),
            ("Toolhead umbilical — toolboard end", "XT30(2+2)-F",
             "toolboard power/data", "D+ / D− / GND / 24V"),
            ("24V power   (24V IN end)", "screw terminal", "USB adapter 24 V in",
             "TO TOOLHEAD end on the PSU +V / −V"),
        ]),
        ("NITEHAWK-SB V2 — on the toolhead", [
            ("Revo HF heater, 2 x E0508 ferrules", "screw terminal", "HE0",
             "polarity does not matter"),
            ("Revo HF thermistor", "JST-PH2.0 2P", "TH0", "PB12"),
            ("Omron inductive probe", "JST-PH2.0 3P", "PROBE",
             "GND / SIG PC15 / 24V — 24 V only"),
            ("Chamber thermistor", "JST-PH2.0 2P", "CT", "PB2"),
            ("Clockwork 2 extruder motor", "JST-XH2.5 4P", "E MOTOR",
             "reverse side · B02 B01 A1 A2"),
            ("— nothing —", "JST-PH2.0 4P", "XY ENDSTOP",
             "unused — that PCB wires to the Leviathan"),
            ("— nothing —", "JST-PH2.0 4P", "I2C", "unused"),
            ("— nothing —", "JST-ZH1.5 5P", "USB expansion",
             "unused now — the \"+\" in Rev D+"),
        ]),
        ("STEALTHBURNER FAN ADAPTER — 2 x 5 keyed board-to-board", [
            ("4010 axial hotend fan", "JST-PH2.0 3P", "P2", "+ / A1 tacho / −"),
            ("Neopixel LED chain", "JST-PH2.0 3P", "P3", "5V / GND / RGB"),
            ("5015 part-cooling blower", "JST-PH2.0 3P", "P4", "− / A2 tacho / +"),
        ]),
    ]

    def measure(groups):
        return sum(26 + len(rows) * 30 + 22 for _, rows in groups) + 22

    total = 140 + measure(LEVI) + 38 + measure(NHK) + 66
    d = Doc(int(total), "Voron 2.4r2 — harness map")
    top = header(d, "Harness map — every cable to its port",
           "Cable names are the tags printed on the LDO harness. Ports are the silkscreen "
           "names used in Ch 10.",
           "Ch 08, Steps 08.46 · 08.52 · Ch 10, Steps 10.40 · 10.54")

    XL, XM, XR = 40, 430, 636
    y = top + 26

    def section(gtitle, groups, y):
        d.text(XL, y, gtitle, size=19, weight=700)
        y += 22
        for gname, rows in groups:
            d.rect(XL - 10, y, W - 2 * XL + 20, 26 + len(rows) * 30, fill=PANEL,
                   stroke=RULE, sw=1.5, rx=8)
            d.text(XL + 6, y + 20, gname, size=13, weight=700, fill=MUTED, ls=0.6)
            yy = y + 46
            for cable, conn, port, note in rows:
                empty = cable.startswith("— nothing")
                d.text(XM - 12, yy, cable, size=13.5, anchor="end",
                       weight=400 if empty else 600,
                       fill=MUTED if empty else "currentColor")
                if conn:
                    d.text(XM + 4, yy - 1, conn, size=11.5, fill=MUTED)
                d.path(f"M {XM + 108} {yy - 4.5} L {XR - 12} {yy - 4.5}",
                       stroke=FAINT if empty else GREY, sw=1.8,
                       marker=None if empty else "arwm", dash="4 4" if empty else None)
                d.mono(XR, yy, port, size=13.5, weight=600,
                       fill=MUTED if empty else "currentColor")
                d.text(XR + 246, yy, note, size=11.5, fill=MUTED)
                yy += 30
            y += 26 + len(rows) * 30 + 22
        return y

    y = section("Leviathan mainboard", LEVI, y)
    y += 16
    y = section("Toolhead — umbilical and Nitehawk-SB V2", NHK, y)

    footer(d, "Positions in the notes column are read standing in front of an upright "
              "printer. LDO's tags name the cable's destination: the end you hold reads "
              "where the OTHER end goes (TO MB / TO TOOLHEAD sit at the PSU; 24V / 24V IN "
              "at the device). A and B must land on the two TMC5160 ports and nowhere else "
              "— on a 2209 the motor is badly under-driven. Never plug or unplug a stepper, "
              "or the Micro-Fit umbilical, with power on.")
    return d


# =============================================================== diagram 7 ===
def d07_jumpers() -> Doc:
    d = Doc(700, "Voron 2.4r2 — Leviathan voltage-selection jumpers")
    top = header(d, "Leviathan voltage-selection jumper map",
                 "Five voltage-selection headers. Exactly two carry a jumper on this build, "
                 "both at 24 V. Count them before power-on.",
                 "Ch 09, Step 09.19 · Ch 10, Steps 10.3 · 10.28")

    # board outline (schematic)
    bx, by, bw, bh = 60, top + 16, 660, 452
    d.rect(bx, by, bw, bh, fill=PANEL, stroke=BLACKPART, sw=2.6, rx=10)
    for cx, cy in ((bx + 22, by + 22), (bx + bw - 22, by + 22),
                   (bx + 22, by + bh - 22), (bx + bw - 22, by + bh - 22)):
        d.circle(cx, cy, 6, fill=BG, stroke=GREY, sw=1.8)
    d.text(bx + 20, by + 54, "LDO Leviathan V1.3  —  schematic board outline", size=14,
           weight=700)
    d.text(bx + 20, by + 74, "header positions are NOT to the board's real layout; read the",
           size=12, fill=MUTED)
    d.text(bx + 20, by + 91, "silkscreen and LDO's S1_mapping photo before fitting anything.",
           size=12, fill=MUTED)

    def header_block(x, y, name, fitted, note):
        w, h = 288, 74
        col = OK if fitted else GREY
        fill = OK_F if fitted else PANEL
        d.rect(x, y, w, h, fill=fill, stroke=col, sw=2.4, rx=8)
        d.mono(x + 16, y + 26, name, size=14.5, weight=700)
        d.text(x + 16, y + 62, note, size=11.5, fill=MUTED)
        # 3-pin selection header: 5V | common | 24V
        px = x + w - 92
        py = y + 12
        for i in range(3):
            d.rect(px + i * 22, py, 15, 22, fill=GREY_F, stroke=GREY, sw=1.6, rx=2)
        d.text(px + 3, py + 36, "5V", size=10.5, fill=MUTED)
        d.text(px + 42, py + 36, "24V", size=10.5, fill=MUTED)
        if fitted:
            d.rect(px + 20, py - 4, 41, 30, fill=OK, stroke=OK, sw=2, rx=4)
            d.text(px + 40, py + 15, "24V", size=11.5, anchor="middle", weight=700,
                   fill="#FFFFFF")
        else:
            d.text(px + 30, py + 15, "bare", size=11.5, anchor="middle", weight=600,
                   fill=MUTED)

    y = by + 112
    header_block(bx + 24, y, "FAN0", False, "unused — hotend fan is on the toolboard")
    header_block(bx + 348, y, "FAN1", False, "unused — part fan is on the toolboard")
    header_block(bx + 24, y + 90, "FAN2", True, "2 x 6020 electronics-bay fans (PCB FAN)")
    header_block(bx + 348, y + 90, "FAN3", True, "Nevermore filter fan (FILTER FAN)")
    header_block(bx + 24, y + 180, "Z-PROBE voltage", False,
                 "unused — the probe is on the toolboard")
    d.rect(bx + 348, y + 180, 288, 74, fill=BG, stroke=RULE, sw=1.6, rx=8, dash="6 5")
    d.text(bx + 364, y + 208, "3 bare  ·  2 fitted  ·  5 total", size=14, weight=700)
    d.text(bx + 364, y + 229, "a jumper at 24 V with a 5 V device fitted", size=11.5,
           fill=MUTED)
    d.text(bx + 364, y + 246, "destroys the device; 5 V → 24 V cannot bridge",
           size=11.5, fill=RED)

    # side notes
    nx = 760
    d.panel(nx, by, 400, 232, "The rule, in order")
    yy = d.wrap(nx + 18, by + 62,
                "Ch 09 Step 09.19: on the bench, before the board goes on the rail, pull "
                "ALL voltage-selection jumpers — the four fan headers and the Z-probe "
                "header — into a labelled bag taped to the bay wall.",
                size=12.4, width_chars=46, lh=18)
    d.wrap(nx + 18, yy + 14,
           "Ch 10 Step 10.28: fit exactly two back, on Fan2 and Fan3, both in the 24 V "
           "position, after each attached device's voltage is verified.",
           size=12.4, width_chars=46, lh=18)

    d.panel(nx, by + 250, 400, 202, "Ports these jumpers feed")
    rows = [("FAN2", "PF7", "2 x 6020 bay fans, 24 V"),
            ("FAN3", "PF9", "Nevermore filter fan, 24 V"),
            ("LED-Strip", "PE6", "not a jumpered header"),
            ("FAN0 / FAN1", "—", "stay empty on a Nitehawk build"),
            ("Z-PROBE", "—", "stays empty for the whole build")]
    yy = by + 306
    for a, b, c in rows:
        d.mono(nx + 18, yy, a, size=12.3, weight=600)
        d.mono(nx + 150, yy, b, size=12.3, fill=MUTED)
        d.text(nx + 196, yy, c, size=11.8, fill=MUTED)
        yy += 25
    d.text(nx + 18, yy + 12, "Manual p.174–178 is Octopus jumper", size=11.8, fill=MUTED)
    d.text(nx + 18, yy + 29, "configuration — ignore it entirely.", size=11.8, fill=MUTED)

    footer(d, "(verify) The chapters name the five headers and which two carry a jumper, "
              "but not where each header sits on the board or the pin order inside it — the "
              "outline and the 5V/24V pin order above are schematic. LDO's Leviathan V1.3 "
              "guide and S1_mapping photo are the authority for physical position.")
    return d


# =============================================================== diagram 8 ===
def d08_revdplus() -> Doc:
    d = Doc(800, "Voron 2.4r2 Rev D+ — connector differences")
    top = header(d, "Rev D+ vs Rev D — the three connector differences",
                 "Five of the six Rev D+ deltas land on the toolhead. These are the three "
                 "that will not physically fit if you get them wrong.",
                 "Ch 08, Steps 08.46 · 08.62 · Ch 10, Steps 10.55 · 10.57")

    PY_ = top + 16
    PH_ = 596

    # ---- (a) PH2.0 vs XH2.5 ----
    d.panel(30, PY_, 372, PH_, "1 — JST-PH2.0, not JST-XH2.5",
            "the Rev D guide was not updated for V2")

    def connector(x, y, pitch_mm, pins, name, sub, col):
        scale = 8.6                              # px per mm, both drawn to one scale
        p = pitch_mm * scale
        body_h = 26 if pitch_mm < 2.3 else 32
        wdt = p * pins
        d.rect(x, y, wdt, body_h, fill=PANEL, stroke=col, sw=2.4, rx=3)
        for i in range(pins):
            cx = x + p * (i + 0.5)
            d.line(cx, y + body_h, cx, y + body_h + 12, stroke=GREY, sw=2.4)
            d.circle(cx, y + 9, 2.6, fill=col, stroke="none", sw=0)
        d.dim_h(y - 14, x + p * 0.5, x + p * 1.5, f"{pitch_mm} mm pitch")
        d.text(x, y + body_h + 34, name, size=14.5, weight=700)
        d.text(x, y + body_h + 52, sub, size=11.5, fill=MUTED)

    connector(70, PY_ + 94, 2.0, 4, "JST-PH2.0",
              "PROBE 3P · TH0 2P · CT 2P · XY ENDSTOP 4P", ORANGE)
    connector(70, PY_ + 218, 2.5, 4, "JST-XH2.5",
              "E MOTOR 4P only — this one did NOT change", BLUE)

    ty = PY_ + 326
    d.rect(50, ty, 332, 200, fill=AMBER_F, stroke=AMBER, sw=2.2, rx=8)
    d.text(66, ty + 26, "What the old guide says vs the board", size=13.5, weight=700)
    d.text(66, ty + 48, "port", size=11, weight=700, fill=MUTED)
    d.text(150, ty + 48, "Rev D guide", size=11, weight=700, fill=MUTED)
    d.text(258, ty + 48, "V2 board", size=11, weight=700, fill=MUTED)
    rows = [("PROBE", "not specified", "PH2.0 3P, 24 V"),
            ("TH0", "\"XH2.5 two pin\"", "PH2.0 2P"),
            ("XY ENDSTOP", "not specified", "PH2.0 4P, unused"),
            ("HE0", "ferrule / screw", "unchanged")]
    yy = ty + 72
    for a, b, c in rows:
        d.mono(66, yy, a, size=11, weight=600)
        d.text(150, yy, b, size=11, fill=MUTED)
        d.text(258, yy, c, size=11, weight=600)
        yy += 22
    d.text(66, yy + 14, "A PH2.0 body can be forced into the wrong", size=11.2, fill=RED)
    d.text(66, yy + 30, "header — read the silkscreen every time.", size=11.2, fill=RED)

    # ---- (b) keyed 2x5 header ----
    d.panel(418, PY_, 372, PH_, "2 — the fan-adapter header is keyed",
            "V1 was 2 x 4; V2 is 2 x 5, reversed and keyed")

    hx, hy = 480, PY_ + 106
    cell = 34
    d.rect(hx - 12, hy - 12, cell * 5 + 24, cell * 2 + 24, fill=PANEL, stroke=BLACKPART,
           sw=2.6, rx=6)
    d.rect(hx + cell * 2 - 6, hy - 22, 26, 12, fill=BG, stroke=BLACKPART, sw=2.2, rx=2)
    d.text(hx + cell * 2 + 7, hy - 30, "key", size=11, anchor="middle", weight=700,
           fill=BLACKPART)
    for r in range(2):
        for c in range(5):
            cx, cy = hx + c * cell + cell / 2, hy + r * cell + cell / 2
            d.rect(cx - 12, cy - 12, 24, 24, fill=GREY_F, stroke=GREY, sw=1.8, rx=3)
            d.circle(cx, cy, 3.4, fill=GREY, stroke="none", sw=0)
    pins = ["tacho  ·  tacho",
            "fan drive  ·  fan drive",
            "RGB PD3  ·  5 V",
            "GND  ·  NC",
            "NC  ·  24 V"]
    yy = hy + cell * 2 + 46
    d.text(452, yy, "Pin pairs, toolboard side", size=12.5, weight=700)
    for i, ln in enumerate(pins):
        d.text(452, yy + 22 + i * 19, f"{i + 1}.  {ln}", size=11.8, fill=MUTED)

    by2 = PY_ + 420
    d.rect(438, by2, 332, 152, fill=AMBER_F, stroke=AMBER, sw=2.2, rx=8)
    d.text(454, by2 + 26, "The key is the check", size=13.5, weight=700)
    d.wrap(454, by2 + 50,
           "The Stealthburner front drops onto the toolhead and the header seats with no "
           "gap. If it does not drop in, you have it backwards — do not press harder. A V1 "
           "fan adapter physically cannot be reused on a V2 toolboard.",
           size=11.8, width_chars=44, lh=17, fill=INK)

    # ---- (c) partial cover / ground lug ----
    d.panel(806, PY_, 364, PH_, "3 — the partial cover and the ground lug",
            "usb_adapter_mount_partial_cover.stl, V2 repo")

    cx0, cy0 = 852, PY_ + 92
    d.rect(cx0, cy0, 236, 122, fill=GREY_F, stroke=GREY, sw=2.4, rx=6)
    d.text(cx0 + 118, cy0 + 22, "USB adapter PCB", size=12.5, anchor="middle", weight=700)
    for (mx, my) in ((cx0 + 22, cy0 + 96), (cx0 + 214, cy0 + 96),
                     (cx0 + 22, cy0 + 54), (cx0 + 214, cy0 + 54)):
        d.circle(mx, my, 7, fill=PANEL, stroke=GREY, sw=1.8)
    d.rect(cx0 + 8, cy0 + 30, 186, 84, fill=BLACKPART_F, stroke=BLACKPART, sw=2.4, rx=5,
           dash="6 5")
    d.text(cx0 + 100, cy0 + 74, "V2 partial cover", size=11.5, anchor="middle", fill=MUTED)
    d.circle(cx0 + 214, cy0 + 96, 12, fill="none", stroke=GREEN, sw=2.6)
    d.path(f"M {cx0 + 236} {cy0 + 96} L {cx0 + 274} {cy0 + 96}", stroke=GREEN, sw=2.4,
           marker="arwg")
    d.text(cx0 + 118, cy0 + 148, "one mounting point left exposed", size=12,
           anchor="middle", fill=GREEN, weight=600)
    d.text(cx0 + 118, cy0 + 165, "= the ground lug", size=12, anchor="middle", fill=GREEN,
           weight=600)

    gy = cy0 + 202
    d.text(852, gy, "One continuous ESD discharge path", size=13, weight=700)
    chain = ["extruder motor body", "toolboard ground", "umbilical",
             "USB adapter", "frame", "earth"]
    yy = gy + 26
    for i, node in enumerate(chain):
        d.circle(862, yy - 4, 4.5, fill=GREEN, stroke="none", sw=0)
        d.text(880, yy, node, size=12.3)
        if i < len(chain) - 1:
            d.line(862, yy + 2, 862, yy + 20, stroke=GREEN, sw=2)
        yy += 26
    d.text(852, yy + 8, "Use the two supplied grounding cables:", size=11.5, fill=MUTED)
    d.text(852, yy + 24, "larger O-ring connectors can short the PCBs.", size=11.5,
           fill=MUTED)

    footer(d, "If your kit has no grounding cables, or the board doc you have predates the "
              "2026-07-10 update, ask in #ldo_motors on the Voron Discord rather than "
              "improvising a shield or ground connection.")
    return d

# =============================================================== diagram 9 ===
def d09_racking() -> Doc:
    d = Doc(900, "Voron 2.4r2 — gantry racking and de-racking")
    top = header(d, "Racking, and how to measure it",
                 "A racked gantry has one side of the X extrusion further forward than the "
                 "other. You de-rack by pushing the X extrusion fully back against both "
                 "drives and tightening the X/Y joints there.",
                 "Ch 06b, Steps 06b.9 · 06b.11 · 06b.14")

    def view(ox, oy, racked, title, sub, col):
        w, h = 430, 430
        d.panel(ox, oy, w, h + 76, title, sub)
        fx, fy, fw, fh = ox + 46, oy + 72, w - 92, h - 96
        d.rect(fx, fy, fw, fh, fill=BLUE_F, stroke=BLUE, sw=2.5, rx=4)
        d.text(fx + fw / 2, fy - 10, "REAR", size=11.5, anchor="middle", weight=700,
               fill=BLUE)
        d.text(fx + fw / 2, fy + fh + 20, "FRONT", size=11.5, anchor="middle", weight=700,
               fill=BLUE)

        skew = 22 if racked else 0
        yl_top, yl_bot = fy + 66, fy + fh - 30          # left Y extrusion
        yr_top, yr_bot = fy + 54 - skew, fy + fh - 34 - skew
        lx, rx = fx + 62, fx + fw - 62
        d.line(lx, yl_top, lx, yl_bot, stroke=col, sw=9)
        d.line(rx, yr_top, rx, yr_bot, stroke=col, sw=9)
        # X extrusion between the two XY joints
        d.line(lx, (yl_top + yl_bot) / 2, rx, (yr_top + yr_bot) / 2, stroke=col, sw=9)
        for (jx, jy) in ((lx, (yl_top + yl_bot) / 2), (rx, (yr_top + yr_bot) / 2)):
            d.rect(jx - 17, jy - 17, 34, 34, fill=PANEL, stroke=col, sw=2.4, rx=5)
        # drive units at the rear ends
        d.rect(lx - 24, yl_top - 24, 48, 28, fill=BLACKPART_F, stroke=BLACKPART, sw=2, rx=4)
        d.rect(rx - 24, yr_top - 24, 48, 28, fill=BLACKPART_F, stroke=BLACKPART, sw=2, rx=4)
        d.text(lx, yl_top - 6, "B drv", size=10, anchor="middle", fill=MUTED)
        d.text(rx, yr_top - 6, "A drv", size=10, anchor="middle", fill=MUTED)

        # four measurement points
        pts = [("FL", lx, yl_bot, fx), ("RL", lx, yl_top, fx),
               ("FR", rx, yr_bot, fx + fw), ("RR", rx, yr_top, fx + fw)]
        for name, x, y, wall in pts:
            d.line(min(x, wall), y, max(x, wall), y, stroke=RED if racked else OK, sw=2,
                   dash="4 3")
            tx = wall - 8 if wall > x else wall + 8
            anch = "end" if wall > x else "start"
            d.text(tx, y - 6, name, size=11, anchor=anch, weight=700,
                   fill=RED if racked else OK)
        if racked:
            d.text(fx + fw / 2, fy + fh + 42, "front–rear gaps differ on the same side",
                   size=12, anchor="middle", fill=RED, weight=600)
            d.path(f"M {rx + 30} {yr_top + 18} L {rx + 30} {yr_top + 58}", stroke=RED,
                   sw=2.4, marker="arwr")
            d.text(rx + 36, yr_top + 44, "this side leads", size=11, fill=RED, weight=600)
        else:
            d.text(fx + fw / 2, fy + fh + 42,
                   "same side within 0.5 mm · left vs right within 1 mm",
                   size=12, anchor="middle", fill=OK, weight=600)

    vy = top + 16
    view(30, vy, True, "Racked (exaggerated)",
         "the X extrusion is not square to the Y extrusions", RED)
    view(496, vy, False, "Square", "both X/Y joints bottom out together", OK)

    # right-hand column: what to loosen, and the de-rack move
    nx = 962
    d.panel(nx, vy, 208, 506, "What to loosen")
    rows = [("06b.8", "the four M5x40 through the lower Z joints — drop the joints down "
                      "the rails; the gantry hangs on the belts"),
            ("06b.9", "X/Y joints, top and bottom, both sides — enough to slide by hand, "
                      "no looser"),
            ("06b.10", "both A/B drive units and both front idlers, top and bottom"),
            ("06b.12", "retighten everything except the X/Y joints"),
            ("06b.14", "push the X extrusion fully back against both drives, hold, then "
                       "tighten the X/Y joint bolts in a cross pattern")]
    yy = vy + 52
    for step, txt in rows:
        d.mono(nx + 16, yy, "Step " + step, size=12, weight=700)
        yy = d.wrap(nx + 16, yy + 18, txt, size=11.5, width_chars=28, lh=16) + 10
    d.rect(nx + 12, vy + 534, 184, 124, fill=AMBER_F, stroke=AMBER, sw=2.2, rx=8)
    d.wrap(nx + 26, vy + 560,
           "Where an X/Y joint carries a Z belt clamp, do not loosen it far enough for the "
           "Z belt to release. Only enough to allow adjustment.",
           size=11.5, width_chars=26, lh=16, fill=INK)

    # the four-point measurement table
    my2 = vy + 526
    d.rect(30, my2, 908, 132, fill=PANEL, stroke=RULE, sw=1.5, rx=8)
    d.text(48, my2 + 28, "The four-point gap measurement — bench check, not in the "
           "official text", size=15, weight=700)
    d.wrap(48, my2 + 52,
           "With the caliper's depth rod, measure the horizontal gap between each Y extrusion "
           "and the frame upright beside it, at front-left, rear-left, front-right and "
           "rear-right. Front and rear on the SAME side must agree within 0.5 mm — a "
           "difference is the gantry skewed in the frame. Left and right must agree within "
           "1 mm — a difference is the gantry off-centre. Then stand a machinist square on "
           "the front frame extrusion at each front corner, blade against the Y extrusion: "
           "no light under the blade. Write the numbers down; you repeat this three times.",
           size=12.3, width_chars=112, lh=17.5)

    footer(d, "Do all of this on a level surface with the A/B motors disabled and both A/B "
              "belts fully slack, and keep a hand on the gantry while the lower Z joints are "
              "off. Re-tension both belts to 110 Hz afterwards.")
    return d


# ============================================================== diagram 10 ===
def d10_motor_directions() -> Doc:
    d = Doc(860, "Voron 2.4r2 — STEPPER_BUZZ motor-direction cheat sheet")
    top = header(d, "STEPPER_BUZZ — which motor, which corner, which way",
                 "One motor per command. It moves 1 mm positive, pauses, returns, ten "
                 "times. Watch the machine, not the console.",
                 "Ch 13, Steps 13.13 · 13.14 · 13.16 · 13.23")

    # ---- top view ----
    ox, oy = 40, top + 16
    d.panel(ox, oy, 560, 620, "Top view — the corner that must rise FIRST",
            "the bed is bolted to the frame; what rises is the gantry corner")
    fx, fy, fw, fh = ox + 40, oy + 92, 480, 484
    d.rect(fx, fy, fw, fh, fill=BLUE_F, stroke=BLUE, sw=2.5, rx=4)
    d.text(fx + fw / 2, fy - 14, "REAR", size=12.5, anchor="middle", weight=700, fill=BLUE)
    d.text(fx + fw / 2, fy + fh + 24, "FRONT  (you stand here)", size=12.5,
           anchor="middle", weight=700, fill=BLUE)

    bw, bh = 168, 96
    corners = [("Z0", "front left", "stepper_z", "STEPPER-0",
                fx + 14, fy + fh - bh - 14),
               ("Z1", "rear left", "stepper_z1", "STEPPER-1", fx + 14, fy + 14),
               ("Z2", "rear right", "stepper_z2", "STEPPER-2",
                fx + fw - bw - 14, fy + 14),
               ("Z3", "front right", "stepper_z3", "STEPPER-3",
                fx + fw - bw - 14, fy + fh - bh - 14)]
    for name, pos, cmd, port, bxx, byy in corners:
        d.rect(bxx, byy, bw, bh, fill=PANEL, stroke=OK, sw=2.4, rx=8)
        d.text(bxx + 12, byy + 26, name, size=18, weight=700)
        d.text(bxx + 46, byy + 26, pos, size=12, fill=MUTED)
        d.mono(bxx + 12, byy + 50, cmd, size=12.5, weight=600)
        d.mono(bxx + 12, byy + 70, port, size=11.5, fill=MUTED)
        d.path(f"M {bxx + bw - 24} {byy + 80} L {bxx + bw - 24} {byy + 52}",
               stroke=OK, sw=2.6, marker="arwg")
        d.text(bxx + bw - 36, byy + 86, "rises", size=10.5, anchor="end", fill=OK,
               weight=700)

    # A and B on the rear extrusion
    d.rect(fx + fw / 2 - 176, fy + fh / 2 - 46, 168, 92, fill=PANEL, stroke=BELT_B, sw=2.4,
           rx=8)
    d.text(fx + fw / 2 - 164, fy + fh / 2 - 20, "B", size=18, weight=700)
    d.text(fx + fw / 2 - 146, fy + fh / 2 - 20, "rear left", size=12, fill=MUTED)
    d.mono(fx + fw / 2 - 164, fy + fh / 2 + 2, "stepper_x", size=12.5, weight=600)
    d.mono(fx + fw / 2 - 164, fy + fh / 2 + 22, "HV-STEPPER-0", size=11.5, fill=MUTED)

    d.rect(fx + fw / 2 + 8, fy + fh / 2 - 46, 168, 92, fill=PANEL, stroke=BELT_A, sw=2.4,
           rx=8)
    d.text(fx + fw / 2 + 20, fy + fh / 2 - 20, "A", size=18, weight=700)
    d.text(fx + fw / 2 + 40, fy + fh / 2 - 20, "rear right", size=12, fill=MUTED)
    d.mono(fx + fw / 2 + 20, fy + fh / 2 + 2, "stepper_y", size=12.5, weight=600)
    d.mono(fx + fw / 2 + 20, fy + fh / 2 + 22, "HV-STEPPER-1", size=11.5, fill=MUTED)
    d.text(fx + fw / 2, fy + fh / 2 + 68,
           "[stepper_x] is motor B  ·  [stepper_y] is motor A", size=12.5, anchor="middle",
           fill=MUTED, weight=600)

    # ---- right column ----
    nx = 624
    d.panel(nx, oy, 536, 250, "The four Z commands", "run them one at a time")
    yy = oy + 74
    d.text(nx + 20, yy, "command", size=12, weight=700, fill=MUTED)
    d.text(nx + 262, yy, "motor / port", size=12, weight=700, fill=MUTED)
    d.text(nx + 400, yy, "corner that rises", size=12, weight=700, fill=MUTED)
    yy += 10
    d.line(nx + 20, yy, nx + 516, yy, stroke=RULE, sw=1.4)
    yy += 24
    for name, pos, cmd, port, *_ in corners:
        d.mono(nx + 20, yy, f"STEPPER_BUZZ STEPPER={cmd}", size=12)
        d.mono(nx + 262, yy, f"{name} · {port}", size=12, fill=MUTED)
        d.text(nx + 400, yy, pos, size=12.5, weight=600)
        yy += 30

    d.panel(nx, oy + 266, 536, 178, "A and B are NOT direction-checked by buzzing",
            "a single motor's rotation is not a meaningful check by eye")
    d.wrap(nx + 20, oy + 344,
           "What matters at STEPPER_BUZZ is only that the right motor answers and moves "
           "cleanly. Direction is settled at homing: G28 X must travel the toolhead to the "
           "RIGHT, G28 Y to the BACK. Match the observed pair to the chart, then invert "
           "dir_pin on the stepper the chart marks.",
           size=12.6, width_chars=62, lh=18)

    d.panel(nx, oy + 460, 536, 160, "Fixing what you find")
    fixes = [("nothing moved", "check enable_pin / step_pin and driver power"),
             ("buzzed, did not travel", "coil pairs transposed in the connector"),
             ("wrong motor answered", "power down, then move the connector"),
             ("moved the wrong way", "add or remove ! on that dir_pin, RESTART")]
    yy = oy + 512
    for a, b in fixes:
        d.text(nx + 20, yy, a, size=12.3, weight=600)
        d.text(nx + 208, yy, b, size=12, fill=MUTED)
        yy += 26

    footer(d, "The extruder buzzes too — STEPPER_BUZZ STEPPER=extruder with no filament — "
              "but its direction is not tested until the first extrude. Never move a stepper "
              "connector with power on.")
    return d


# ============================================================== diagram 11 ===
def _print_hours() -> tuple[dict[str, float], float]:
    """Per-batch and total print hours, read from the print README's batch table
    (the sliced PrusaSlicer estimates) so the timeline can never drift from it."""
    rows: dict[str, float] = {}
    total = None
    row_re = re.compile(r"^\|\s*\[(B\d\d)\]\([^)]*\)\s*\|\s*\d+\s*\|\s*([\d.]+)\s*\|")
    tot_re = re.compile(r"^\|\s*\*\*TOTAL\*\*\s*\|\s*\*\*\d+\*\*\s*\|\s*\*\*([\d.]+)\*\*\s*\|")
    for line in PRINT_README.read_text(encoding="utf-8").splitlines():
        m = row_re.match(line)
        if m:
            rows[m.group(1)] = float(m.group(2))
            continue
        m = tot_re.match(line)
        if m:
            total = float(m.group(1))
    if len(rows) != 11 or total is None:
        raise SystemExit(f"draw_diagrams: could not read the 11 batch rows + TOTAL from "
                         f"{PRINT_README} (got {sorted(rows)}, total={total})")
    return rows, total


TIMELINE = [
    # (row, kind, label, duration, needs-rows)
    # "P" rows: the duration is replaced at render time by the hours in
    # docs/manual/print/README.md (see _print_hours); the strings here are the
    # values on the day this list was last edited.
    (1, "P", "B00 — Calibration & jigs", "4.0 h print", []),
    (2, "B", "Ch 00 — Before you start", "2.5–4.0 h  KIT", [1]),
    (3, "P", "B01 — Z drive assemblies", "22.8 h print", [1]),
    (4, "B", "Ch 01 — Frame", "2.5–4.0 h  KIT 2P", []),
    (5, "P", "B02 — Accent parts, the orange day", "21.9 h print", [1]),
    (6, "B", "Ch 02 — Z drives, idlers, rails, deck", "4.25–6.25 h  KIT", [3, 5]),
    (7, "P", "B03 — A/B drive units + front idlers", "8.5 h print", [5]),
    (8, "B", "Ch 03 — Build plate", "1.5–2.5 h  KIT", []),
    (9, "P", "B04 — XY joints + X carriage", "8.6 h print", [7]),
    (10, "B", "Ch 04 — A/B drives and front idlers", "3.5–5.0 h  KIT", [7]),
    (11, "P", "B05 — Z joints + Z chain", "6.4 h print", [9]),
    (12, "B", "Ch 05 — Gantry", "5.0–7.0 h  KIT 2P", [9]),
    (13, "P", "B06 — Toolhead: SB, CW2, Klicky", "12.2 h print", [9]),
    (14, "B", "Ch 06 Part A — Z axis, hang the gantry", "3.5–5.0 h  2P lift", [11]),
    (15, "P", "B07 — Electronics bay + lighting", "16.0 h print", []),
    (16, "B", "Ch 07 — A/B belts, provisional tension", "2.5–4.0 h  KIT", [11]),
    (17, "G", "Gen 2 belt-upgrade pause", "~1 day wall clock", []),
    (18, "B", "Ch 08 — Toolhead", "3.0–4.5 h  KIT", [13]),
    (19, "P", "B08 — Skirts and front modules", "29.2 h print", []),
    (20, "B", "Ch 09 — Electronics bay", "2.5–4.0 h  KIT", [15]),
    (21, "B", "Ch 12 Part 1 — image the Pi", "~1.0 h  KIT", []),
    (22, "B", "Ch 10 — Wiring", "5.0–7.0 h  KIT", [15]),
    (23, "P", "B09 — Panels, filtration, spool", "21.8 h print", []),
    (24, "B", "Ch 12 Part 2 — flash both MCUs", "rest of 2.0–3.0 h", []),
    (25, "P", "B10 — Clicky-Clack door", "5.7 h print", []),
    (26, "B", "Ch 11 Part A — skirts, bay fans, panel", "3.0–4.0 h  KIT", [19, 23]),
    (27, "B", "Ch 13 — Initial startup", "2.5–4.0 h + cube  KIT", []),
    (28, "B", "Ch 06b — Gantry squaring", "~1.0 h + soak  KIT 2P", []),
    (29, "B", "Ch 11 Part B — panels, Clicky-Clack door", "1.0–2.0 h  KIT", [25]),
    (30, "B", "Ch 14 — Calibration and tuning", "2.5–4.0 h  KIT", []),
]


def d11_timeline() -> Doc:
    hours, total_print = _print_hours()
    rows = []
    for row, kind, label, dur, needs in TIMELINE:
        if kind == "P":
            dur = f"{hours[label[:3]]:.1f} h print"
        rows.append((row, kind, label, dur, needs))

    ROW_H = 40
    top = 200
    h = int(top + len(rows) * ROW_H + 176)
    d = Doc(h, "Voron 2.4r2 — build timeline")
    header(d, "Build timeline — print batches against assembly chapters",
           "Rows are in execution order, top to bottom. Do a row only when its "
           "dependencies are done; do the print in the same sitting so the Core One+ is "
           "never idle.",
           "docs/manual/00-index.md — The timeline")

    PL, PR = 60, 520          # print lane
    BL, BR = 700, 1160        # build lane
    d.text(PL, top - 26, "PRINT  —  Prusa Core One+", size=14, weight=700, fill=ORANGE,
           ls=0.5)
    d.text(BL, top - 26, "BUILD  —  bench", size=14, weight=700, fill=BLUE, ls=0.5)
    d.line(PL, top - 16, PR, top - 16, stroke=ORANGE, sw=2)
    d.line(BL, top - 16, BR, top - 16, stroke=BLUE, sw=2)

    pos = {}
    for i, (row, kind, label, dur, needs) in enumerate(rows):
        y = top + i * ROW_H
        d.text(46, y + 25, str(row), size=12, anchor="end", fill=FAINT, weight=600)
        if kind == "G":
            d.rect(PL, y + 4, BR - PL, 30, fill=AMBER_F, stroke=AMBER, sw=2.2, rx=6)
            d.text(PL + 14, y + 24, label, size=13.5, weight=700, fill=AMBER)
            d.text(BR - 14, y + 24, dur, size=12.5, anchor="end", fill=AMBER, weight=600)
            pos[row] = (PL, BR, y + 19)
            continue
        x0, x1 = (PL, PR) if kind == "P" else (BL, BR)
        col, fill = (ORANGE, ORANGE_F) if kind == "P" else (BLUE, BLUE_F)
        d.rect(x0, y + 4, x1 - x0, 30, fill=fill, stroke=col, sw=2.2, rx=6)
        d.text(x0 + 12, y + 24, label, size=12.8, weight=600)
        d.text(x1 - 12, y + 24, dur, size=11.8, anchor="end", fill=MUTED)
        pos[row] = (x0, x1, y + 19)

    # dependency arrows through the middle channel
    for row, kind, label, dur, needs in rows:
        for n in needs:
            if n not in pos or row not in pos:
                continue
            sx0, sx1, sy = pos[n]
            tx0, tx1, ty = pos[row]
            if sx1 > tx0:                         # same lane: order already implies it
                continue
            a, b = sx1 + 4, tx0 - 6
            mid = (a + b) / 2
            d.path(f"M {a:.0f} {sy:.0f} C {mid:.0f} {sy:.0f} {mid:.0f} {ty:.0f} "
                   f"{b:.0f} {ty:.0f}",
                   stroke=FAINT, sw=1.8, marker="arwm")

    fy = top + len(rows) * ROW_H + 34
    d.rect(60, fy, 1100, 62, fill=PANEL, stroke=RULE, sw=1.5, rx=8)
    # print total from print/README.md; the other four are 00-index.md's own
    # critical-path figures (§ Critical path) — update them there first.
    facts = [(f"{total_print:.1f} h", "print, 27 plates / 11 batches (sliced)"),
             ("59.5 h", "hands-on"),
             ("~15 printer-days", "printing, elapsed"),
             ("~2.7 weeks", "building, at 22 h/week"),
             ("≈ 3 weeks", "after the kit arrives")]
    x = 84
    for a, b in facts:
        d.text(x, fy + 28, a, size=15, weight=700)
        d.text(x, fy + 48, b, size=11.5, fill=MUTED)
        x += 216

    footer(d, "The vertical axis is execution order, not calendar time — the manual's "
              "timeline is dependency-ordered. Arrows show the batch each chapter needs; "
              "chapters also depend on the chapters above them. Row 17 is the contingency "
              "pause if the Gen 2 belt-upgrade kit turns up mid-run.")
    return d


# ================================================================= registry ===
DIAGRAMS = [
    {
        "n": 1,
        "file": "01-ab-bearing-stacks.svg",
        "title": "The six A/B bearing stacks",
        "fn": d01_bearing_stacks,
        "shows": [
            "All six F695 stacks as exploded vertical stacks in build order: A drive near "
            "post (2 bearings, 10 mm), A drive far post (4 bearings, 20 mm), B drive far "
            "post, B drive near post, A idler (front right), B idler (front left).",
            "Flange orientation item by item — spacer, flange down, flange up, spacer — and "
            "the two spacers that meet in the middle of every 4-bearing stack.",
            "Which bolt each stack builds on (M5x30 BHCS in the drives, M5x40 SHCS in the "
            "idlers) and the handed lower/upper frame heights.",
        ],
        "insert": [
            ("04-ab-drives.md", "Step 04.7", "after the image line, as the reference for "
             "every stack in the chapter"),
            ("04-ab-drives.md", "Step 04.22", "again at the four-bearing stack — the most "
             "often mis-stacked assembly in the build"),
        ],
        "verify": [],
    },
    {
        "n": 2,
        "file": "02-ab-pulley-height-handedness.svg",
        "title": "A/B handedness and pulley height",
        "fn": d02_pulley_heights,
        "shows": [
            "Top view fixing A = rear right and B = rear left, with the idler that belongs "
            "to each and the controller port each motor lands on.",
            "Both motor elevations side by side: A hub-down, teeth up, 16.5 mm; B hub-up, "
            "teeth low, 6.5 mm — both measured motor face to the underside of the teeth.",
            "Motor cable exits pointing inboard, and the 21.6/11.6 mm lower-idler-frame "
            "heights that make the 10.0 mm difference between the two belt planes.",
        ],
        "insert": [
            ("04-ab-drives.md", "Step 04.2", "the handedness half — this is the step that "
             "fixes A/B before anything is assembled"),
            ("04-ab-drives.md", "Step 04.24", "the pulley-height half, and again at "
             "Step 04.33"),
        ],
        "verify": [],
    },
    {
        "n": 3,
        "file": "03-corexy-belt-path.svg",
        "title": "CoreXY belt path — A belt and B belt",
        "fn": d03_belt_path,
        "shows": [
            "Both belt loops as separate top views, the way the manual splits p.126 and "
            "p.127: every 90° turn, the S-wrap at the drive, the 180° U-turn at the front "
            "idler, and the return to the carriage.",
            "The toothed face marked continuously along both belts, so the smooth back on "
            "every plain F695 stack, the teeth on the motor pulley, and the teeth-on wrap "
            "at each belt's one toothed XY joint (A: the right joint's upper 20T, B: the "
            "left joint's lower 20T) are visible at a glance.",
            "The direction each belt is threaded: both leave the LEFT carriage half "
            "heading left (p.131), so the two loops are mirror images traversed in "
            "opposite senses — A's first turn is the left joint's plain stack, B's first "
            "turn is the left joint's toothed idler.",
            "The two-runs-on-one-side asymmetry: A has two parallel runs on the right and "
            "one on the left; B is the mirror.",
            "Where the belt ends are clamped in the X carriage halves.",
        ],
        "insert": [
            ("07-ab-belts.md", "Step 07.3", "the A panel, as the trace reference"),
            ("07-ab-belts.md", "Step 07.4", "the B panel"),
            ("07-ab-belts.md", "Step 07.23", "whole diagram again, as the pre-close check"),
        ],
        "verify": [
            "Lane spacing and the position of the two bearing stacks and the motor pulley "
            "*within* each drive unit are schematic. The chapters fix the order of the "
            "wraps (stack, pulley, stack) and which stack the other belt turns on, not "
            "their top-view coordinates.",
            "The toothed face is stated by the chapter at four places — the carriage "
            "clamp (teeth toward the front, Step 07.9), the drive pulley (teeth seated on "
            "the pulley, Step 07.13), the front idler (smooth back on the stack, teeth "
            "outward on both runs, Step 07.15) and the toothed XY joint (teeth on its 20T "
            "idler — A's return turn at the right joint, Step 07.16; B's first turn at "
            "the left joint, Step 07.17). The face drawn at the "
            "remaining stations follows from belt geometry: a belt cannot change which "
            "face is which along its length. Which joint stack a belt meets (F695 pair "
            "or 20T idler) is fixed by the belt's height and needs no decision.",
            "The diagram does not say which X-carriage slot (upper or lower) each end goes "
            "into, because the chapter assigns the slots by belt plane rather than by side.",
            "Both X runs physically lie in front of the X extrusion (p.131); each panel "
            "draws one of them behind it so the two lanes read apart in a top view.",
        ],
    },
    {
        "n": 4,
        "file": "04-z-drive-gear-train.svg",
        "title": "Z drive gear train and Z belt loop",
        "fn": d04_z_drive,
        "shows": [
            "One corner in side elevation: the Z belt down the inside of the upright, "
            "around the Z drive's 20T pulley, up the outside, over the Z idler, back down "
            "to the Z joint where both ends clamp.",
            "Inside the drive: the motor's 16T at 10.7 mm, the 188 mm closed loop, the 80T "
            "on the 5 x 60 shaft, and the orange cam tensioner that pushes the motor away "
            "from the fixed drive body (the body is held by its two M5x40).",
            "The shaft stack in the order Step 02.19 gives it, with the 33 mm of shaft past "
            "the 20T pulley.",
        ],
        "insert": [
            ("02-z-drives.md", "Step 02.19", "the shaft-stack panel"),
            ("02-z-drives.md", "Step 02.21", "the gear-train panel, where the 188 mm loop "
             "becomes captive"),
            ("06-z-axis-and-gantry-squaring.md", "Step 06.18", "the corner elevation, for "
             "the belt wrap direction"),
        ],
        "verify": [],
    },
    {
        "n": 5,
        "file": "05-mains-and-pe-chain.svg",
        "title": "Mains path and the protective-earth chain",
        "fn": d05_mains_pe,
        "shows": [
            "The mains path end to end: wall socket, C13 cord, the combined C14 + rocker + "
            "fuse inlet, the three labelled WAGO 221-415 blocks, the Meanwell with its AC "
            "screws in datasheet order (1 L, 2 N, 3 FG), the Omron SSR, the bed heater.",
            "Which pole the fuse is in (Live only), which poles the rocker switches (both), "
            "and that the earth spade is neither switched nor fused.",
            "All four SSR terminals with what lands on each, including the red-to-3 / "
            "black-to-4 control pair from the Leviathan's HEATBED terminals.",
            "The five branches of the protective-earth chain, the bed's M4x6 BHCS + "
            "serrated washer, and the thermistor path from the pad to TH1.",
            "What the SSR's EARTH THE MOUNTING RAIL marking does and does not mean on this "
            "build, and what the inlet fuse does not protect.",
        ],
        "insert": [
            ("00a-mains-safety.md", "Step 00a.6", "the whole diagram — this is the step "
             "that teaches the five branches"),
            ("10-wiring.md", "Step 10.10", "the SSR panel, before the terminals are wired"),
        ],
        "verify": [
            "The inlet fuse rating is left unlabelled: LDO does not publish it, and Ch 00a "
            "already asks for it to be read off the part and written in the build log.",
        ],
    },
    {
        "n": 6,
        "file": "06-harness-map.svg",
        "title": "Harness map — every cable to its port",
        "fn": d06_harness_map,
        "shows": [
            "Every LDO harness cable, by the tag printed on it, against the Leviathan port "
            "it lands on: both HV-STEPPER ports, STEPPER-0..3 by corner, STEPPER-4 empty, "
            "TH1, the three endstop headers, FAN2/FAN3 by role, LED-Strip, the three 24 V "
            "feeds, HEATBED, and the data links.",
            "The ports that stay empty and why — STEPPER-4, TH0, Z-PROBE, FAN0, FAN1.",
            "The toolhead umbilical (Micro-Fit at the bay, XT30(2+2) at the toolboard) and "
            "every Nitehawk-SB V2 port with its connector type and pin.",
            "The three fan-adapter ports P2/P3/P4 by function.",
        ],
        "insert": [
            ("10-wiring.md", "Step 10.40", "the Leviathan half, alongside the stepper tag "
             "table"),
            ("10-wiring.md", "Step 10.54", "the toolhead half"),
            ("08-toolhead.md", "Step 08.52", "the toolhead half again, at the "
             "account-for-unused-ports step"),
        ],
        "verify": [],
    },
    {
        "n": 7,
        "file": "07-leviathan-jumper-map.svg",
        "title": "Leviathan voltage-selection jumper map",
        "fn": d07_jumpers,
        "shows": [
            "All five voltage-selection headers by name, which two carry a jumper on this "
            "build (Fan2, Fan3, both at 24 V) and which three stay bare (Fan0, Fan1, the "
            "Z-probe header).",
            "The count check — 5 headers, 2 fitted, 3 bare — and why a jumper at 24 V with "
            "a 5 V device on the port destroys the device (nothing on the block can bridge "
            "5 V to 24 V).",
            "The Ch 09 / Ch 10 sequence: strip every jumper on the bench, fit two back only "
            "after each device's voltage is verified.",
        ],
        "insert": [
            ("09-electronics-bay.md", "Step 09.19", "as the picture of what 'all of them' "
             "means"),
            ("10-wiring.md", "Step 10.28", "as the picture of the end state"),
        ],
        "verify": [
            "Header positions on the board outline are schematic, and so is the 5V / 24V "
            "pin order inside each header. The chapters name the five headers and say which "
            "two are fitted, but never give a physical location or a pin order — LDO's "
            "Leviathan V1.3 guide and the S1_mapping photo are the authority. Every header "
            "in the drawing is therefore labelled by name only.",
        ],
    },
    {
        "n": 8,
        "file": "08-rev-d-plus-connectors.svg",
        "title": "Rev D+ vs Rev D — connector differences",
        "fn": d08_revdplus,
        "shows": [
            "JST-PH2.0 and JST-XH2.5 drawn to the same scale so the 2.0 mm vs 2.5 mm pitch "
            "is visible, with the four ports that are PH2.0 and the one that is not.",
            "What the Rev D wiring guide says against what the V2 board actually is, port "
            "by port.",
            "The 2 x 5 keyed fan-adapter header with its key and the toolboard-side row "
            "order, and why a V1 2 x 4 adapter cannot be reused.",
            "The V2 partial cover with its deliberately exposed mounting point, and the "
            "full ESD ground chain from the extruder motor body to earth.",
        ],
        "insert": [
            ("10-wiring.md", "Step 10.55", "the pitch panel, at the connector-type table"),
            ("10-wiring.md", "Step 10.56", "the keyed-header panel"),
            ("10-wiring.md", "Step 10.57", "the partial-cover panel, carrying into "
             "Step 10.58"),
            ("08-toolhead.md", "Step 08.62", "the keyed-header panel again, where the "
             "board-to-board joint is actually mated"),
        ],
        "verify": [
            "Connector body proportions other than the pitch (housing height, latch shape) "
            "are generic — the chapters give the pitch, pin count and pinout, not a "
            "mechanical drawing.",
        ],
    },
    {
        "n": 9,
        "file": "09-gantry-racking.svg",
        "title": "Racking, and how to measure it",
        "fn": d09_racking,
        "shows": [
            "A racked gantry against a square one in exaggerated top view, with the four "
            "measurement points (front-left, rear-left, front-right, rear-right) marked on "
            "both.",
            "The two tolerances: front and rear on the same side within 0.5 mm, left and "
            "right within 1 mm, plus the machinist-square check at each front corner.",
            "Which fasteners come loose and in what order — lower Z joints, X/Y joints, A/B "
            "joints and front idlers — and the de-racking move itself.",
            "The one thing not to over-loosen: an X/Y joint that also carries a Z belt "
            "clamp.",
        ],
        "insert": [
            ("06-z-axis-and-gantry-squaring.md", "Step 06b.11", "the measurement half, "
             "beside the four-point table"),
            ("06-z-axis-and-gantry-squaring.md", "Step 06b.14", "the de-racking half"),
        ],
        "verify": [
            "The racked view is deliberately exaggerated; real racking is a fraction of a "
            "millimetre. The skew shown is not a measurement.",
        ],
    },
    {
        "n": 10,
        "file": "10-stepper-buzz-directions.svg",
        "title": "STEPPER_BUZZ motor-direction cheat sheet",
        "fn": d10_motor_directions,
        "shows": [
            "A top view naming all four Z corners with the command that must move each one "
            "and the port it is on, and the arrow showing which corner rises first.",
            "That what rises is the gantry corner, not the bed.",
            "A and B on the rear extrusion with the config sections that drive them — "
            "[stepper_x] is motor B, [stepper_y] is motor A.",
            "Why A/B direction is not judged at the buzz, and the homing directions that do "
            "settle it (G28 X to the right, G28 Y to the back).",
            "The four failure modes and the fix for each.",
        ],
        "insert": [
            ("13-initial-startup.md", "Step 13.13", "the whole sheet, replacing nothing — "
             "it is the picture of the step's table"),
            ("13-initial-startup.md", "Step 13.14", "again, for the A/B panel"),
        ],
        "verify": [],
    },
    {
        "n": 11,
        "file": "11-build-timeline.svg",
        "title": "Build timeline — print batches against assembly chapters",
        "fn": d11_timeline,
        "shows": [
            "All 30 timeline rows in execution order on two lanes — print batches B00–B10 "
            "on the Core One+, assembly chapters on the bench — with each row's duration.",
            "Dependency arrows from each batch to the chapter that consumes it.",
            "The Gen 2 belt-upgrade pause as a full-width band at its contingency position, "
            "between B07 and B08.",
            "The critical-path totals: the print hours (per batch and total) are read from "
            "docs/manual/print/README.md at render time so they cannot drift from the "
            "sliced estimates; 59.5 h hands-on and about three calendar weeks once the kit "
            "lands are 00-index.md's own figures.",
        ],
        "insert": [
            ("00-index.md", "The timeline", "at the head of the section, above the row "
             "list — this is the only diagram that belongs in the index rather than in a "
             "chapter step"),
        ],
        "verify": [
            "The vertical axis is execution order, not calendar time. The manual's timeline "
            "is dependency-ordered and gives no per-row calendar date, so none is invented "
            "here; the elapsed figures in the footer strip are the index's own and are "
            "hard-coded in the script — change 00-index.md's Critical path table first.",
        ],
    },
]


# =================================================================== output ===
def write_manifest() -> Path:
    """MANIFEST.md is generated from the registry above so the two cannot drift.

    Note for future editors: this file is built by mkdocs like any other page, so it
    avoids the strings scripts/lint_manual.py treats as raw callout markers, and every
    "Step NN.M" it mentions must match a real heading in the manual.
    """
    L: list[str] = []
    L.append("# Diagram manifest")
    L.append("")
    L.append("Eleven generated SVGs covering the things the official manual states in "
             "prose but never draws. Regenerate with `python3 scripts/draw_diagrams.py`; "
             "the geometry and every label live in that script, not here.")
    L.append("")
    L.append("No chapter has been edited. The **Insert at** column is the proposal: the "
             "chapter file and the step whose image block the diagram belongs in.")
    L.append("")
    L.append("All eleven are 1200 px wide, legible at 800 px, and safe on a dark page — "
             "each carries its own light background rect and pins `color` on the `<svg>` "
             "root, so `currentColor` text stays dark whether the file is referenced with "
             "`<img>` or inlined. Style is uniform: 2 px strokes, orange for `[a]_` accent "
             "parts, blue for the frame and extrusions, grey for hardware, teal and violet "
             "for the A and B belts.")
    L.append("")
    L.append("## Index")
    L.append("")
    L.append("| # | Diagram | File | Insert at |")
    L.append("|---|---|---|---|")
    for spec in DIAGRAMS:
        first = spec["insert"][0]
        where = f"`{first[0]}` — {first[1]}"
        if len(spec["insert"]) > 1:
            where += f" (+{len(spec['insert']) - 1} more)"
        L.append(f"| {spec['n']} | {spec['title']} | "
                 f"[`{spec['file']}`]({spec['file']}) | {where} |")
    L.append("")
    L.append("---")
    L.append("")

    for spec in DIAGRAMS:
        L.append(f"## {spec['n']}. {spec['title']}")
        L.append("")
        L.append(f"`docs/manual/assets/diagrams/{spec['file']}`")
        L.append("")
        L.append("**What it shows**")
        L.append("")
        for s in spec["shows"]:
            L.append(f"- {s}")
        L.append("")
        L.append("**Insert at**")
        L.append("")
        for f, step, why in spec["insert"]:
            L.append(f"- `docs/manual/{f}` — **{step}**: {why}.")
        L.append("")
        if spec["verify"]:
            L.append("**Drawn schematically / left unlabelled (verify)**")
            L.append("")
            for v in spec["verify"]:
                L.append(f"- {v}")
            L.append("")
        L.append("---")
        L.append("")

    L.append("## Markdown to paste in")
    L.append("")
    L.append("Diagrams sit in the step's image block, in the same position a manual page "
             "image would take:")
    L.append("")
    L.append("```markdown")
    L.append("![The six A/B bearing stacks](assets/diagrams/01-ab-bearing-stacks.svg)")
    L.append("```")
    L.append("")
    L.append("From `00-index.md` the path is the same; from a print-batch chapter under "
             "`docs/manual/print/` it is `../assets/diagrams/…`.")
    L.append("")
    L.append("## Regenerating")
    L.append("")
    L.append("```")
    L.append("python3 scripts/draw_diagrams.py            # all eleven + this file")
    L.append("python3 scripts/draw_diagrams.py --only 3 7 # just those two")
    L.append("```")
    L.append("")
    L.append("The script has no third-party dependencies — it emits SVG strings directly. "
             "To check a render: `rsvg-convert -w 1200 -o /tmp/x.png "
             "docs/manual/assets/diagrams/03-corexy-belt-path.svg`.")
    L.append("")

    path = OUT / "MANIFEST.md"
    path.write_text("\n".join(L), encoding="utf-8")
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", nargs="*", type=int, default=None,
                    help="diagram numbers to (re)generate")
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()

    out = args.out
    out.mkdir(parents=True, exist_ok=True)

    # keep the generated pages out of the site nav (awesome-nav)
    (out / ".nav.yml").write_text("hide: true\n", encoding="utf-8")

    wanted = set(args.only) if args.only else {s["n"] for s in DIAGRAMS}
    written = []
    for spec in DIAGRAMS:
        if spec["n"] not in wanted:
            continue
        doc = spec["fn"]()
        path = out / spec["file"]
        path.write_text(doc.render(), encoding="utf-8")
        written.append((path, doc.w, doc.h))

    man = write_manifest()
    for p, w, h in written:
        print(f"  {p.relative_to(REPO)}  {w}x{h}  {p.stat().st_size / 1024:.1f} kB")
    print(f"  {man.relative_to(REPO)}")
    print(f"{len(written)} SVG(s) + manifest -> {out.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
