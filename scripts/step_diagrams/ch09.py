"""Chapter 09 (electronics bay) step-column diagrams, 901 onwards.

Geometry sources: layout v3 (`review/2026-09-23-bay-mods/layout-v3/layout-v3.md` and
`layout-v3.json`, apparent mm on LDO's Rev D placement photo, x to the printer's right,
y to the rear); LDO's placement photo `S0General_Placement.jpg` (identical to the copy on
docs.ldomotors.com, checked 2026-11-20); Voron manual p.156, p.161, p.167, p.171; the
`power_inlet_IECGS_1mm` STL; LDO's inlet layout photo; the Nitehawk-SB V2 USB-adapter
grounding photo. The bay views are drawn the way the chapter works: printer on its head,
seen from its rear, FRONT at the top and the printer's left on the left. Proportions are
schematic; sides, order, counts and every number follow the sources.

Mains parts (inlet, SSR load side, PSU AC terminals, the AC conduit) are drawn in red.
No diagram shows a hand.
"""
import math

import draw_diagrams as dd
from draw_diagrams import (AMBER, AMBER_F, BLACKPART, BLACKPART_F, BLUE, BLUE_F, GREY, GREY_F,
                           INK, MUTED, OK, OK_F, ORANGE, PANEL, RED, STEEL, Doc, T_LAB, T_MIN,
                           callout, label_bg, legend_row, step_header)

PCB = "#262B31"          # a black circuit board
PCB_EDGE = "#11151A"
RED_F = "#F7DEDA"        # pale red fill for mains parts
RAIL = "#C9CED6"         # zinc DIN rail
RAIL_E = "#8A929D"
DUCT_F = "#5A616C"       # black printed duct, seen from the open side


# ------------------------------------------------------------------ helpers ---
def bench_tag(d: Doc, x, y, s, anchor="start", size=T_MIN):
    """An amber chip for a fact the step marks (verify on bench)."""
    w = len(s) * size * 0.56 + 24
    x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
    d.rect(x0, y - size * 0.95, w, size * 1.4, fill=AMBER_F, stroke=AMBER, sw=2.5, rx=8)
    d.text(x0 + w / 2, y + size * 0.05, s, size=size, anchor="middle", weight=700, fill=INK)


def cross(d: Doc, x, y, r=22, sw=7):
    d.line(x - r, y - r, x + r, y + r, stroke=RED, sw=sw)
    d.line(x - r, y + r, x + r, y - r, stroke=RED, sw=sw)


def tick(d: Doc, x, y, r=22, sw=7):
    d.path(f"M {x - r} {y} L {x - r * 0.3} {y + r * 0.7} L {x + r} {y - r * 0.8}", stroke=OK,
           sw=sw)


def arrow(d: Doc, x0, y0, x1, y1, col=INK, sw=6, mk="arw", dash=None):
    d.path(f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}", stroke=col, sw=sw, marker=mk, dash=dash)


def gap_arrows(d: Doc, xa, xb, y, col=INK, sw=3.5, out=70, vertical=False):
    """Two arrowheads pointing in at a small gap between xa and xb (or ya, yb)."""
    mk = {INK: "arw", MUTED: "arwm", RED: "arwr", OK: "arwg"}.get(col, "arw")
    if not vertical:
        d.path(f"M {xa - out} {y} L {xa - 2} {y}", stroke=col, sw=sw, marker=mk)
        d.path(f"M {xb + out} {y} L {xb + 2} {y}", stroke=col, sw=sw, marker=mk)
    else:
        d.path(f"M {y} {xa - out} L {y} {xa - 2}", stroke=col, sw=sw, marker=mk)
        d.path(f"M {y} {xb + out} L {y} {xb + 2}", stroke=col, sw=sw, marker=mk)


def view_tag(d: Doc, x, y, s="FRONT", up=True):
    """FRONT / REAR marker with a small arrow."""
    d.text(x, y, s, size=T_MIN, anchor="middle", weight=800, fill=BLUE)


class Bay:
    """Layout-v3 apparent mm -> page px. x to the printer's right, y to the rear (down)."""

    def __init__(self, ox, oy, s, x0, y0):
        self.ox, self.oy, self.s, self.x0, self.y0 = ox, oy, s, x0, y0

    def X(self, x):
        return self.ox + (x - self.x0) * self.s

    def Y(self, y):
        return self.oy + (y - self.y0) * self.s

    def rect(self, d, x0, x1, y0, y1, **kw):
        d.rect(self.X(x0), self.Y(y0), (x1 - x0) * self.s, (y1 - y0) * self.s, **kw)


def duct(b: Bay, d: Doc, x0, x1, y0, y1, col=BLACKPART, fill=DUCT_F, sw=3, tines=True):
    """A printed duct piece seen from the open side: two walls with tine slots."""
    b.rect(d, x0, x1, y0, y1, fill=fill, stroke=col, sw=sw)
    if not tines:
        return
    tc = "#AEB4BC" if fill == DUCT_F else col
    horiz = (x1 - x0) >= (y1 - y0)
    if horiz:
        n = int((x1 - x0) // 12)
        for i in range(n):
            cx = x0 + 6 + i * 12
            for yy in (y0, y1):
                d.line(b.X(cx), b.Y(yy), b.X(cx), b.Y(yy) + (2.5 if yy == y0 else -2.5) * b.s,
                       stroke=tc, sw=2)
    else:
        n = int((y1 - y0) // 12)
        for i in range(n):
            cy = y0 + 6 + i * 12
            for xx in (x0, x1):
                d.line(b.X(xx), b.Y(cy), b.X(xx) + (2.5 if xx == x0 else -2.5) * b.s, b.Y(cy),
                       stroke=tc, sw=2)


def psu_top(b: Bay, d: Doc, x0, x1, y0, y1, term=True):
    """The LRS-200 from above: perforated lid, terminal strip on its left end; the three
    AC terminals (L, N, FG) at the rear end of the strip, drawn red."""
    b.rect(d, x0, x1, y0, y1, fill=GREY_F, stroke=GREY, sw=3)
    for i in range(int((x1 - x0 - 30) // 14)):
        for j in range(int((y1 - y0 - 16) // 14)):
            cx, cy = x0 + 26 + i * 14, y0 + 10 + j * 14
            if cx < x1 - 6 and cy < y1 - 6:
                d.circle(b.X(cx), b.Y(cy), 1.6 * b.s, fill="none", stroke=STEEL, sw=1.2)
    if term:
        sx0, sx1 = x0, x0 + 12
        n = 9
        pitch = (y1 - y0 - 10) / n
        for i in range(n):
            ty = y0 + 5 + i * pitch
            mains = i >= n - 3
            b.rect(d, sx0, sx1, ty, ty + pitch, fill=RED_F if mains else "#3A3F46",
                   stroke=RED if mains else INK, sw=2)
            d.circle(b.X(sx0 + 6), b.Y(ty + pitch / 2), 2.6 * b.s, fill=STEEL,
                     stroke=RED if mains else GREY, sw=1.5)


def din_rail(b: Bay, d: Doc, x0, x1, yc, w=35):
    b.rect(d, x0, x1, yc - w / 2, yc + w / 2, fill=RAIL, stroke=RAIL_E, sw=2.5)
    b.rect(d, x0, x1, yc - w / 2 + 5, yc + w / 2 - 5, fill="none", stroke=RAIL_E, sw=1.5)
    for i in range(int((x1 - x0 - 20) // 36)):
        cx = x0 + 22 + i * 36
        d.rect(b.X(cx), b.Y(yc - 2.6), 16 * b.s, 5.2 * b.s, fill="#EEF0F3", stroke=RAIL_E,
               sw=1.5, rx=2.6 * b.s)


# ============================================================= diagram 901 ===
def d901_psu_position() -> Doc:
    d = Doc(1300, "PSU on the rear rail: 2 mm from the T's rounded corner, 3 mm from the SSR run")
    top = step_header(d, "Where the PSU stops")
    d.panel(30, top + 16, 1140, 700)
    d.text(54, top + 62, "Seen from the rear, printer on its head", size=T_MIN, weight=700,
           fill=MUTED)
    b = Bay(60, top + 150, 3.05, -128, -22)
    view_tag(d, b.X(30), top + 108, "FRONT")
    # rear rail, SSR (faint), PSU
    din_rail(b, d, -120, 192, 70)
    b.rect(d, -108.5, -63.5, 43.8, 101.8, fill="#EDE6DE", stroke=GREY, sw=2.5, op=0.85)
    d.text(b.X(-86), b.Y(76), "SSR", size=T_MIN, anchor="middle", weight=700, fill=MUTED)
    PX0, PX1, PY0, PY1 = -29, 186, 10.5, 125.5
    psu_top(b, d, PX0, PX1, PY0, PY1)
    label_bg(d, b.X(95), b.Y(64), "PSU", size=40, weight=800, bg=GREY_F)
    # middle run and the right narrowed T (dry-laid DC loop, black)
    duct(b, d, -125, 169.4, -13.2, 8.8)
    tx0, tx1 = 197.0, 221.4
    d.path(f"M {b.X(169.4)} {b.Y(-13.2)} L {b.X(185)} {b.Y(-13.2)} "
           f"Q {b.X(tx0)} {b.Y(-13.2)} {b.X(tx0)} {b.Y(-25)} L {b.X(tx0)} {b.Y(-30)} "
           f"L {b.X(tx1)} {b.Y(-30)} L {b.X(tx1)} {b.Y(32)} L {b.X(tx0)} {b.Y(32)} "
           f"L {b.X(tx0)} {b.Y(20.8)} Q {b.X(tx0)} {b.Y(8.8)} {b.X(185)} {b.Y(8.8)} "
           f"L {b.X(169.4)} {b.Y(8.8)} Z", fill=DUCT_F, stroke=BLACKPART, sw=3)
    d.text(b.X(20), b.Y(-22), "middle run", size=T_MIN, anchor="middle", weight=700,
           fill=BLACKPART)
    d.text(b.X(209), b.Y(-34), "T", size=T_LAB, anchor="middle", weight=800, fill=BLACKPART)
    # the SSR run behind the SSR: AC conduit, mains (red outline)
    b.rect(d, -109.8, -102, 103.8, 128.2, fill=RED_F, stroke=RED, sw=3)
    duct(b, d, -102, -32, 103.8, 128.2, col=RED, fill=RED_F)
    d.text(b.X(-68), b.Y(144), "SSR run (mains)", size=T_MIN, anchor="middle", weight=700,
           fill=RED)
    # magnifier rings on the two gaps
    for (cx, cy) in ((-30.5, 116), (190, 12)):
        d.circle(b.X(cx), b.Y(cy), 46, fill="none", stroke=ORANGE, sw=4, dash="10 7")
    # callouts: 1 = on the rear rail, terminals left; 2 = slide left
    callout(d, b.X(150), b.Y(100), 1)
    arrow(d, b.X(130), b.Y(108), b.X(70), b.Y(108), col=ORANGE, sw=8, mk="arwo")
    callout(d, b.X(48), b.Y(108), 2)
    d.text(b.X(30), b.Y(138), "REAR", size=T_MIN, anchor="middle", weight=800, fill=BLUE)

    # ---- the two gaps, enlarged
    gy = top + 732
    gh = d.h - gy - 16
    # left end: the SSR run's open end, then the PSU's terminal strip
    d.panel(30, gy, 560, gh)
    d.text(54, gy + 48, "Left end", size=36, weight=700)
    y0, y1 = gy + 80, gy + 240
    d.path(f"M 300 {y0 + 20} L 70 {y0 + 20} L 70 {y1 - 20} L 300 {y1 - 20}", fill=RED_F,
           stroke=RED, sw=4)
    d.text(185, (y0 + y1) / 2 + 11, "SSR run", size=T_LAB, anchor="middle", weight=800,
           fill=RED)
    d.text(185, y1 + 22, "open end", size=T_MIN, weight=700, fill=RED)
    d.rect(370, y0, 205, y1 - y0 + 20, fill=GREY_F, stroke=GREY, sw=4)
    for i in range(4):
        d.rect(370, y0 + 10 + i * 50, 48, 50, fill=RED_F if i else "#3A3F46",
               stroke=RED if i else INK, sw=2.5)
    d.text(500, (y0 + y1) / 2 + 11, "PSU", size=T_LAB, anchor="middle", weight=800)
    gap_arrows(d, 300, 370, y1 + 66, col=INK, out=60)
    d.text(335, y1 + 116, "3 mm or more", size=T_LAB, anchor="middle", weight=800)
    bench_tag(d, 310, gy + gh - 34, "check on the bench", anchor="middle")
    # front-right corner: the right T's rounded corner and the PSU's corner
    d.panel(610, gy, 560, gh)
    d.text(634, gy + 48, "Front-right corner", size=36, weight=700)
    sy0, sy1, bx0, bx1, r = gy + 90, gy + 160, 960, 1040, 90
    acx, acy = bx0 - r, sy1 + r
    d.path(f"M 630 {sy0} L {bx0} {sy0} L {bx0} {gy + 66} L {bx1} {gy + 66} "
           f"L {bx1} {gy + gh - 20} L {bx0} {gy + gh - 20} L {bx0} {acy} "
           f"A {r} {r} 0 0 0 {acx} {sy1} L 630 {sy1} Z", fill=DUCT_F, stroke=BLACKPART, sw=4)
    d.text(640, sy1 - 22, "right T", size=T_LAB, weight=800, fill="#FFFFFF")
    c45 = math.cos(math.radians(45))
    fx, fy = acx + r * c45, acy - r * c45
    pcx, pcy = fx - 24, fy + 24
    d.rect(630, pcy, pcx - 630, gy + gh - 20 - pcy, fill=GREY_F, stroke=GREY, sw=4)
    d.line(pcx, pcy, fx, fy, stroke=ORANGE, sw=6)
    d.text(pcx - 16, pcy + 52, "2 mm", size=T_LAB, anchor="end", weight=800)
    d.text(720, gy + gh - 60, "PSU", size=T_LAB, anchor="middle", weight=800)
    d.text(bx1 + 10, acy + 90, "rounded", size=T_MIN, weight=700, fill=BLACKPART)
    d.text(bx1 + 10, acy + 126, "corner", size=T_MIN, weight=700, fill=BLACKPART)
    d.leader(fx + 6, fy + 6, bx1 + 6, acy + 80, col=INK)
    return d


# ============================================================= diagram 902 ===
def d902_vhb_checks() -> Doc:
    d = Doc(1300, "Before the VHB goes down: middle run gaps, stub on the port, 34 mm run over "
                  "the hole")
    top = step_header(d, "Check, then stick")

    # ---- panel 1: middle run between the Leviathan and the PSU (gaps drawn enlarged)
    d.panel(30, top + 16, 1140, 380)
    d.text(54, top + 62, "Middle run, gaps enlarged", size=T_MIN, weight=700, fill=MUTED)
    x0, x1 = 290, 960
    g = 24                                       # 1.5 mm, drawn enlarged
    ly0, ly1 = top + 86, top + 146
    dy0, dy1 = ly1 + g, ly1 + g + 132
    py0, py1 = dy1 + g, dy1 + g + 52
    d.rect(x0, ly0, x1 - x0, ly1 - ly0, fill=PCB, stroke=PCB_EDGE, sw=3, rx=6)
    d.text((x0 + x1) / 2, ly1 - 18, "Leviathan", size=T_LAB, anchor="middle", weight=800,
           fill="#FFFFFF")
    d.rect(x0, dy0, x1 - x0, dy1 - dy0, fill=DUCT_F, stroke=BLACKPART, sw=4)
    for i in range(10):
        x = x0 + 30 + i * 68
        d.line(x, dy0, x, dy0 + 18, stroke="#AEB4BC", sw=3)
        d.line(x, dy1, x, dy1 - 18, stroke="#AEB4BC", sw=3)
    d.text((x0 + x1) / 2, (dy0 + dy1) / 2 + 11, "middle run", size=T_LAB, anchor="middle",
           weight=800, fill="#FFFFFF")
    d.rect(x0, py0, x1 - x0, py1 - py0, fill=GREY_F, stroke=GREY, sw=3)
    d.text((x0 + x1) / 2, py1 - 12, "PSU", size=T_LAB, anchor="middle", weight=800)
    for ya, yb, ty in ((ly1, dy0, ly1 + 4), (dy1, py0, dy1 + 4)):
        gap_arrows(d, ya, yb, 990, col=INK, out=40, vertical=True)
        d.text(1012, ty, "1.5 mm", size=T_LAB, weight=800)
        d.text(1012, ty + 36, "or more", size=T_MIN, weight=700)
    callout(d, 160, (dy0 + dy1) / 2 - 16, 1)
    d.text(160, (dy0 + dy1) / 2 + 54, "centred", size=T_MIN, anchor="middle", weight=700)

    # ---- panel 2: the AC conduit (mains), from the box at the WAGO bus to the 34 mm run
    py = top + 412
    d.panel(30, py, 1140, d.h - py - 16)
    d.text(54, py + 46, "AC conduit", size=T_MIN, weight=700, fill=MUTED)
    bench_tag(d, 1150, py + 46, "stub length: on the bench", anchor="end")
    b = Bay(80, py + 84, 4.0, -125, 62)
    d.text(b.X(-20), py + 110, "FRONT", size=T_MIN, anchor="middle", weight=800, fill=BLUE)
    # SSR (faint), WAGO blocks behind the box
    b.rect(d, -108.5, -63.5, 66, 101.8, fill="#EDE6DE", stroke=GREY, sw=2.5)
    d.text(b.X(-86), b.Y(90), "SSR", size=T_MIN, anchor="middle", weight=700, fill=MUTED)
    for i in range(3):
        b.rect(d, -112 + i * 25.5, -112 + i * 25.5 + 23, 203, 216, fill="#F3C38A",
               stroke=AMBER, sw=2)
    d.text(b.X(-77), b.Y(228) + 8, "mains WAGO blocks", size=T_MIN, anchor="middle",
           weight=700, fill=RED)
    # SSR run: endcap, T_SHORT, 10 mm
    b.rect(d, -109.8, -102, 103.8, 128.2, fill=RED_F, stroke=RED, sw=3)
    duct(b, d, -102, -32, 103.8, 128.2, col=RED, fill=RED_F)
    # stub down into the box's port
    duct(b, d, -84.2, -59.8, 128.2, 152.8, col=RED, fill="#FBEDEB", tines=False)
    # box with the port in its front wall
    b.rect(d, -115.8, -38.4, 152.8, 201.2, fill=RED_F, stroke=RED, sw=3.5)
    d.line(b.X(-81), b.Y(152.8), b.X(-63), b.Y(152.8), stroke="#FBEDEB", sw=6)
    d.text(b.X(-77), b.Y(184), "wire box", size=T_MIN, anchor="middle", weight=700, fill=RED)

    def arc_band(cx, cy, a0, a1, ri=3.3, ro=27.7):
        sa, ea = math.radians(a0), math.radians(a1)
        o0 = (b.X(cx + ro * math.cos(sa)), b.Y(cy + ro * math.sin(sa)))
        o1 = (b.X(cx + ro * math.cos(ea)), b.Y(cy + ro * math.sin(ea)))
        i1 = (b.X(cx + ri * math.cos(ea)), b.Y(cy + ri * math.sin(ea)))
        i0 = (b.X(cx + ri * math.cos(sa)), b.Y(cy + ri * math.sin(sa)))
        R, r = ro * b.s, ri * b.s
        sweep = 1 if a1 > a0 else 0
        d.path(f"M {o0[0]:.1f} {o0[1]:.1f} A {R:.1f} {R:.1f} 0 0 {sweep} {o1[0]:.1f} "
               f"{o1[1]:.1f} L {i1[0]:.1f} {i1[1]:.1f} A {r:.1f} {r:.1f} 0 0 {1 - sweep} "
               f"{i0[0]:.1f} {i0[1]:.1f} Z", fill=RED_F, stroke=RED, sw=3)
    # two R15 curves and the 34 mm run, then the endcap
    arc_band(-38.4, 161.5, 90, 0)
    arc_band(-7.4, 161.5, 180, 270)
    duct(b, d, -7.4, 26.6, 133.8, 158.2, col=RED, fill=RED_F)
    b.rect(d, 26.6, 34.4, 134.2, 157.8, fill=RED_F, stroke=RED, sw=3)
    # round deck hole under the 34 mm run
    d.circle(b.X(14.7), b.Y(146), 7.5 * b.s, fill=PANEL, stroke=INK, sw=4, dash="9 6")
    callout(d, b.X(50), b.Y(146), 2)
    d.text(b.X(50) + 44, b.Y(146) - 26, "34 mm run", size=T_LAB, weight=800, fill=RED)
    d.text(b.X(50) + 44, b.Y(146) + 12, "over the", size=T_LAB, weight=700)
    d.text(b.X(50) + 44, b.Y(146) + 50, "round hole", size=T_LAB, weight=700)
    # stub on the port
    d.circle(b.X(-72), b.Y(150), 54, fill="none", stroke=ORANGE, sw=4, dash="10 7")
    d.text(b.X(-22), b.Y(108), "stub seated", size=T_LAB, weight=700)
    d.text(b.X(-22), b.Y(108) + 38, "on the box port", size=T_LAB, weight=700)
    d.leader(b.X(-60), b.Y(141), b.X(-26), b.Y(112), col=INK)
    d.text(b.X(-20), d.h - 40, "REAR", size=T_MIN, anchor="middle", weight=800, fill=BLUE)
    return d


# ============================================================= diagram 903 ===
def d903_ssr_orientation() -> Doc:
    d = Doc(1000, "SSR on the rear rail: INPUT toward the front, LOAD toward the rear")
    top = step_header(d, "SSR the right way round")
    d.panel(30, top + 16, 700, 870)
    d.text(54, top + 62, "Seen from the rear,", size=T_MIN, weight=700, fill=MUTED)
    d.text(54, top + 98, "printer on its head", size=T_MIN, weight=700, fill=MUTED)
    b = Bay(40, top + 130, 6.0, -128, 24)
    d.text(b.X(-86), top + 150, "FRONT", size=T_MIN, anchor="middle", weight=800, fill=BLUE)
    d.text(b.X(-86), top + 856, "REAR", size=T_MIN, anchor="middle", weight=800, fill=BLUE)
    din_rail(b, d, -126, -20, 70)
    # metal bracket: tabs out front and rear
    b.rect(d, -95, -77, 34, 44, fill=STEEL, stroke=GREY, sw=2.5)
    b.rect(d, -93, -79, 101.8, 110, fill=STEEL, stroke=GREY, sw=2.5)
    # SSR body
    b.rect(d, -108.5, -63.5, 43.8, 101.8, fill="#EDE6DE", stroke=INK, sw=3.5, rx=6)
    # INPUT pair at the front edge, LOAD pair at the rear edge (mains)
    for (tx, ty, mains) in ((-101, 51, False), (-71, 51, False), (-101, 94.5, True),
                            (-71, 94.5, True)):
        col = RED if mains else INK
        b.rect(d, tx - 6, tx + 6, ty - 5.5, ty + 5.5, fill=RED_F if mains else "#D9DDE2",
               stroke=col, sw=3)
        d.circle(b.X(tx), b.Y(ty), 3.4 * b.s, fill=STEEL, stroke=col, sw=2)
        d.line(b.X(tx - 2.4), b.Y(ty - 2.4), b.X(tx + 2.4), b.Y(ty + 2.4), stroke=GREY, sw=3)
    d.circle(b.X(-103), b.Y(63.5), 1.8 * b.s, fill="#F0B020", stroke=AMBER, sw=2)
    d.text(b.X(-84), b.Y(66), "INPUT", size=T_MIN, anchor="middle", weight=800)
    d.text(b.X(-86), b.Y(83), "LOAD", size=T_MIN, anchor="middle", weight=800, fill=RED)
    # PSU's left end to the right
    b.rect(d, -29, -20, 26, 125.5, fill=GREY_F, stroke=GREY, sw=3)
    d.text(b.X(-24.5), b.Y(136), "PSU", size=T_LAB, anchor="middle", weight=800)
    # clear rail between them
    d.line(b.X(-63.5), b.Y(116), b.X(-29), b.Y(116), stroke=MUTED, sw=3)
    for x in (-63.5, -29):
        d.line(b.X(x), b.Y(111), b.X(x), b.Y(121), stroke=MUTED, sw=3)
    d.text(b.X(-46), b.Y(128), "about 30 mm", size=T_MIN, anchor="middle", weight=700,
           fill=MUTED)
    callout(d, b.X(-119), b.Y(70), 2)
    callout(d, b.X(-119), b.Y(51), 3)

    # right column: labels in the step's words
    x = 750
    d.panel(x, top + 16, 420, 870)
    y = legend_row(d, x + 20, top + 110, 2, ["left of", "the PSU"])
    y = legend_row(d, x + 20, y + 50, 3, ["INPUT 3+ 4−", "toward the front"])
    d.text(x + 92, y + 40, "LOAD 1 2", size=T_LAB, weight=800, fill=RED)
    d.text(x + 92, y + 80, "toward the rear:", size=T_LAB, weight=600)
    d.text(x + 92, y + 120, "the mains side", size=T_LAB, weight=700, fill=RED)
    d.text(x + 24, top + 790, "amber LED on", size=T_MIN, weight=600, fill=MUTED)
    d.text(x + 24, top + 826, "the INPUT side", size=T_MIN, weight=600, fill=MUTED)
    return d


# ============================================================= diagram 904 ===
def d904_probe_gap() -> Doc:
    d = Doc(1000, "Nozzle probe pin just behind the plate's rear edge: a 2 mm key fits, a 3 mm "
                  "key does not")
    top = step_header(d, "Probe pin behind the plate")
    d.panel(30, top + 16, 700, 870)
    d.text(54, top + 62, "From above, rear at the top", size=T_MIN, weight=700, fill=MUTED)
    k = 9.0                                      # px per mm
    ex0 = 520                                    # right bed extrusion, inner face x
    pe = top + 470                               # plate rear edge y
    # right bed extrusion running front-back, under everything
    d.rect(ex0, top + 90, 20 * k, 780, fill=BLUE_F, stroke=BLUE, sw=3)
    for sgn in (-1, 1):
        d.line(ex0 + 10 * k + sgn * 3.1 * k, top + 94, ex0 + 10 * k + sgn * 3.1 * k,
               top + 866, stroke=BLUE, sw=1.6, op=0.55)
    d.text(ex0 + 10 * k, top + 830, "bed", size=T_MIN, anchor="middle", weight=700, fill=BLUE)
    d.text(ex0 + 10 * k, top + 862, "extr.", size=T_MIN, anchor="middle", weight=700,
           fill=BLUE)
    # build plate, straight rear edge
    d.rect(60, pe, ex0 + 20 * k - 60, top + 760 - pe, fill="#E9ECEF", stroke=INK, sw=4)
    d.text(260, pe + 150, "build plate", size=T_LAB, anchor="middle", weight=800)
    # probe body against the inner face, behind the plate edge; pin at its front end
    pin_r = 2.5 * k
    gap = 2.5 * k
    pcy = pe - gap - pin_r
    bx1 = ex0
    bx0 = ex0 - 22 * k
    by0, by1 = pcy - 26 * k, pcy + pin_r + 0.6 * k
    d.rect(bx0, by0, bx1 - bx0, by1 - by0, fill=BLACKPART_F, stroke=BLACKPART, sw=4, rx=10)
    pcx = (bx0 + bx1) / 2
    d.circle(pcx, pcy + 0.4 * k, 4.5 * k, fill=STEEL, stroke=GREY, sw=3)      # collar
    d.circle(pcx, pcy, pin_r, fill="#DADFE5", stroke=INK, sw=3)                 # pin
    # two M3x25 heads into the extrusion side (seen end-on, through the body)
    for yy in (by0 + 6 * k, by0 + 15 * k):
        d.rect(bx0 + 3 * k, yy - 1.6 * k, bx1 - bx0 - 1 * k, 3.2 * k, fill=GREY_F, stroke=GREY,
               sw=2, dash="7 5")
        d.circle(bx0 + 3 * k, yy, 2.7 * k, fill=GREY_F, stroke=GREY, sw=2.5)
    d.text(bx0 - 14, by0 + 40, "probe", size=T_MIN, anchor="end", weight=700, fill=BLACKPART)
    # T-nuts slid toward the rear end
    arrow(d, ex0 + 10 * k, top + 330, ex0 + 10 * k, top + 170, col=ORANGE, sw=8, mk="arwo")
    callout(d, ex0 + 10 * k, top + 380, 1)
    callout(d, bx0 - 40, by0 + 15 * k, 2)
    callout(d, pcx - 80, pe - 14, 3)
    d.text(380, top + 120, "REAR", size=T_MIN, anchor="middle", weight=800, fill=BLUE)

    # right column: the hex-key gauge, enlarged
    gx = 750
    d.panel(gx, top + 16, 420, 870)
    d.text(gx + 24, top + 62, "The gap, enlarged", size=T_MIN, weight=700, fill=MUTED)
    K = 26.0

    def gauge(y0, key, ok):
        pr, g = 2.5 * K, 2.5 * K
        ccx, ccy = gx + 300, y0 + pr + 10
        ye = ccy + pr + g                           # plate rear edge
        d.rect(gx + 20, ye, 380, 44, fill="#E9ECEF", stroke="none", sw=0)
        d.line(gx + 20, ye, gx + 400, ye, stroke=INK, sw=5)
        kw = key * K
        kc = ye - g / 2
        d.rect(gx + 24, kc - kw / 2, 340, kw, fill=BLACKPART, stroke=OK if ok else RED,
               sw=3 if ok else 5, rx=3)
        d.circle(ccx, ccy, pr, fill="#DADFE5", stroke=INK, sw=3)
        d.text(gx + 24, ye + 90, f"{key:g} mm key", size=T_LAB, weight=800,
               fill=OK if ok else RED)
        d.text(gx + 24, ye + 130, "slides in" if ok else "does not fit", size=T_LAB,
               weight=700, fill=OK if ok else RED)
        (tick if ok else cross)(d, gx + 360, ye + 100)
    gauge(top + 90, 2, True)
    gauge(top + 470, 3, False)
    d.text(gx + 24, top + 862, "p.161 draws 1.5 mm", size=T_MIN, weight=600, fill=MUTED)
    return d


# ============================================================= diagram 905 ===
def d905_inlet_press() -> Doc:
    d = Doc(1000, "Inlet module pressed in from outside until its tabs snap behind the wall")
    top = step_header(d, "Press the inlet in")
    # left: section through the panel wall
    d.panel(30, top + 16, 640, 870)
    d.text(54, top + 62, "Cut through the panel", size=T_MIN, weight=700, fill=MUTED)
    wx = 330                                    # wall line
    wt = 16
    d.rect(wx, top + 110, wt, 230, fill=BLACKPART_F, stroke=BLACKPART, sw=3)
    d.rect(wx, top + 560, wt, 260, fill=BLACKPART_F, stroke=BLACKPART, sw=3)
    d.text(wx + 8, top + 104, "panel wall", size=T_MIN, anchor="middle", weight=700,
           fill=BLACKPART)
    d.text(110, top + 854, "outside", size=T_LAB, anchor="middle", weight=800)
    d.text(540, top + 854, "inside", size=T_LAB, anchor="middle", weight=800)
    # module: flange outside the wall, body through the opening, spade tails inside
    fy0, fy1 = top + 300, top + 600
    d.rect(wx - 26, fy0, 26, fy1 - fy0, fill=RED_F, stroke=RED, sw=4)        # flange
    d.rect(wx, fy0 + 40, 220, fy1 - fy0 - 80, fill=RED_F, stroke=RED, sw=4)  # body
    for i in range(3):
        yy = fy0 + 80 + i * 70
        d.rect(wx + 220, yy, 46, 14, fill=STEEL, stroke=GREY, sw=2)          # spades
    d.text(wx + 110, fy0 + 160, "inlet", size=T_LAB, anchor="middle", weight=800, fill=RED)
    d.text(wx + 110, fy0 + 200, "module", size=T_LAB, anchor="middle", weight=800, fill=RED)
    # sprung tabs that snap behind the wall
    for sgn, yb in ((-1, fy0 + 40), (1, fy1 - 40)):
        tip = (wx + wt + 4, yb + sgn * 22)
        d.path(f"M {wx + 70} {yb} L {tip[0]} {tip[1]}", stroke=RED, sw=6)
    d.circle(wx + wt + 4, fy0 + 18, 30, fill="none", stroke=ORANGE, sw=4, dash="9 6")
    d.text(wx + 60, fy0 - 40, "tabs snap", size=T_MIN, weight=700)
    d.text(wx + 60, fy0 - 6, "behind the wall", size=T_MIN, weight=700)
    arrow(d, 90, (fy0 + fy1) / 2, wx - 50, (fy0 + fy1) / 2, col=ORANGE, sw=9, mk="arwo")
    callout(d, 150, (fy0 + fy1) / 2 - 60, 1)
    d.text(160, (fy0 + fy1) / 2 + 70, "press", size=T_LAB, anchor="middle", weight=700)
    # nothing on the spades
    cross(d, wx + 300, fy0 + 220, r=20, sw=6)
    callout(d, wx + 300, fy0 + 300, 2)
    d.text(wx + 300, fy0 + 380, "nothing", size=T_MIN, anchor="middle", weight=700, fill=RED)
    d.text(wx + 300, fy0 + 414, "on the", size=T_MIN, anchor="middle", weight=700, fill=RED)
    d.text(wx + 300, fy0 + 448, "spades", size=T_MIN, anchor="middle", weight=700, fill=RED)

    # right: the socket face from outside, printer upright
    gx = 690
    d.panel(gx, top + 16, 480, 870)
    d.text(gx + 24, top + 62, "From outside,", size=T_MIN, weight=700, fill=MUTED)
    d.text(gx + 24, top + 96, "printer upright", size=T_MIN, weight=700, fill=MUTED)
    cx, cy = gx + 240, top + 380
    d.rect(cx - 180, cy - 150, 360, 300, fill=RED_F, stroke=RED, sw=4, rx=16)
    d.rect(cx - 150, cy - 110, 180, 210, fill=PANEL, stroke=RED, sw=3, rx=14)   # C14 recess
    sx = cx - 60
    d.rect(sx - 10, cy - 76, 20, 48, fill=OK_F, stroke=OK, sw=3, rx=3)           # earth pin
    for dx in (-48, 48):
        d.rect(sx + dx - 8, cy + 10, 16, 48, fill=STEEL, stroke=GREY, sw=3, rx=3)
    d.rect(cx + 60, cy - 100, 90, 200, fill="#3A3F46", stroke=INK, sw=3, rx=8)    # rocker
    d.line(cx + 60, cy, cx + 150, cy, stroke="#8A929D", sw=3)
    d.text(sx, cy - 172, "earth pin up", size=T_LAB, anchor="middle", weight=800, fill=OK)
    d.leader(sx, cy - 82, sx, cy - 160, col=OK)
    d.text(cx + 105, cy + 190, "switch", size=T_LAB, anchor="middle", weight=800)
    d.text(cx + 105, cy + 228, "facing out", size=T_LAB, anchor="middle", weight=700)
    d.text(gx + 24, top + 700, "On its head now,", size=T_MIN, weight=600, fill=MUTED)
    d.text(gx + 24, top + 736, "so the earth pin", size=T_MIN, weight=600, fill=MUTED)
    d.text(gx + 24, top + 772, "points at the floor.", size=T_MIN, weight=600, fill=MUTED)
    bench_tag(d, gx + 240, top + 836, "fits either way up", anchor="middle")
    return d


# ============================================================= diagram 906 ===
def d906_usb_adapter_stack() -> Doc:
    d = Doc(1000, "USB adapter stack: DIN clip on the base's back, ring terminal on the bare "
                  "screw")
    top = step_header(d, "USB-adapter stack")
    # left: front view after the Nitehawk-SB V2 grounding photo
    d.panel(30, top + 16, 640, 870)
    d.text(54, top + 62, "Front", size=T_MIN, weight=700, fill=MUTED)
    cx, cy = 340, top + 470
    # diamond base behind
    d.poly([(cx - 250, cy - 10), (cx - 80, cy - 190), (cx + 230, cy - 190), (cx + 230, cy + 170),
            (cx + 30, cy + 330), (cx - 170, cy + 170)], fill=BLACKPART_F, stroke=BLACKPART, sw=4)
    for (hx, hy) in ((cx - 205, cy - 10), (cx + 30, cy + 285)):
        d.circle(hx, hy, 15, fill=PANEL, stroke=BLACKPART, sw=3)
    # PCB
    d.rect(cx - 150, cy - 230, 380, 380, fill=PCB, stroke=PCB_EDGE, sw=3, rx=8)
    # partial cover: leaves the top strip and the top-right corner bare
    d.path(f"M {cx - 170} {cy - 250} L {cx - 30} {cy - 250} L {cx - 30} {cy - 120} "
           f"L {cx + 240} {cy - 120} L {cx + 240} {cy + 170} L {cx - 170} {cy + 170} Z",
           fill="#3E4550", stroke=INK, sw=3)
    d.rect(cx - 20, cy - 222, 150, 92, fill="#1D2126", stroke="#8A929D", sw=3, rx=4)  # Micro-Fit
    d.text(cx + 55, cy - 244, "Micro-Fit", size=T_MIN, anchor="middle", weight=700)
    d.rect(cx + 90, cy + 40, 150, 110, fill="#2B2B2B", stroke=INK, sw=2)      # 24 V terminal
    for i, col in enumerate(("#9AA3AF", "#B5523B")):
        d.circle(cx + 128 + i * 74, cy + 95, 22, fill=STEEL, stroke=GREY, sw=2)
    # three M3x10: top-left and bottom through the cover, top-right bare
    for (sx, sy) in ((cx - 110, cy - 190), (cx + 10, cy + 110)):
        d.circle(sx, sy, 26, fill="#6B5A4C", stroke=INK, sw=3)
        d.circle(sx, sy, 10, fill=INK, stroke="none", sw=0)
    rx, ry = cx + 190, cy - 190
    d.circle(rx, ry, 26, fill="#6B5A4C", stroke=INK, sw=3)
    d.circle(rx, ry, 10, fill=INK, stroke="none", sw=0)
    # ring terminal on the bare screw, lead off to the frame (earth, green)
    d.circle(rx, ry, 40, fill="none", stroke=STEEL, sw=12)
    d.path(f"M {rx + 30} {ry - 28} L {rx + 70} {ry - 80}", stroke=STEEL, sw=16, cap="butt")
    d.path(f"M {rx + 70} {ry - 80} C {rx + 100} {ry - 120} {rx + 110} {ry - 150} "
           f"{rx + 120} {ry - 200}", stroke="#D9A21B", sw=10)
    callout(d, rx - 80, ry - 10, 3)
    callout(d, cx - 110, cy - 110, 1)
    d.text(cx - 200, cy + 230, "partial cover", size=T_MIN, anchor="middle", weight=700)
    d.text(54, top + 846, "3× M3×10 hold the stack", size=T_MIN, weight=700)

    # right: edge view, the layers and the DIN clip on the base's back
    gx = 690
    d.panel(gx, top + 16, 480, 870)
    d.text(gx + 24, top + 62, "From the side", size=T_MIN, weight=700, fill=MUTED)
    lx = gx + 40
    lay = [("cover", "#3E4550", 50), ("PCB", PCB, 40), ("base", BLACKPART_F, 56)]
    y = top + 120
    for name, col, th in lay:
        d.rect(lx, y, 240, th, fill=col, stroke=INK, sw=2.5)
        d.text(lx + 256, y + th / 2 + 11, name, size=T_MIN, weight=700)
        y += th
    # DIN clip on the back of the base, two M2x10 up into the base
    d.rect(lx + 50, y, 140, 44, fill=BLACKPART, stroke=INK, sw=2.5)
    d.text(lx + 256, y + 33, "DIN clip", size=T_MIN, weight=800)
    for sx in (lx + 80, lx + 160):
        d.line(sx, y + 44, sx, y - 40, stroke=GREY, sw=7)
        d.rect(sx - 13, y + 44, 26, 10, fill=GREY_F, stroke=GREY, sw=2)
    callout(d, lx + 120, y + 110, 2)
    d.text(gx + 24, y + 190, "2× M2×10 self-tapping,", size=T_MIN, weight=700)
    d.text(gx + 24, y + 226, "for the clip only", size=T_MIN, weight=700)
    bench_tag(d, gx + 240, y + 292, "clip screws: on the bench", anchor="middle")
    d.rect(lx + 10, y + 420, 220, 30, fill=RAIL, stroke=RAIL_E, sw=2.5)
    d.text(lx + 120, y + 490, "front DIN rail", size=T_MIN, anchor="middle", weight=700,
           fill=MUTED)
    arrow(d, lx + 120, y + 330, lx + 120, y + 410, col=MUTED, sw=4, mk="arwm", dash="10 8")
    return d


# ================================================================= registry ===
DIAGRAMS = [
    {
        "n": 901,
        "file": "901-psu-on-rear-rail.svg",
        "title": "Where the PSU stops on the rear rail",
        "fn": d901_psu_position,
        "shows": [
            "The bay from the rear, printer on its head, FRONT at the top: the rear DIN rail, "
            "the SSR on its left, the PSU on its right with its terminal strip on the left end "
            "(AC terminals red), the dry-laid middle run and right narrowed T in front of it, "
            "and the SSR run of the AC conduit (red) behind the SSR.",
            "Callouts 1 and 2 are the Do numbers of Step 09.16: clip on at the right, slide left.",
            "Two enlargements: the PSU's left end 3 mm or more from the SSR run's open end "
            "(check on the bench), and its front-right corner 2 mm from the T's rounded "
            "corner.",
        ],
        "insert": [
            ("09-electronics-bay.md", "Step 09.16", "first image: where the hands stop the PSU"),
        ],
        "verify": [
            "Positions are layout v3's apparent mm on LDO's placement photo (±6 % absolute, "
            "±1.5 mm local); the PSU is drawn 215 × 115 at x −29…186. The T's fillet radius "
            "and the 2 mm gap in the enlargement are schematic. The 3 mm gap is the step's "
            "(verify on bench); tagged.",
        ],
    },
    {
        "n": 902,
        "file": "902-vhb-checks.svg",
        "title": "Check before the VHB goes down",
        "fn": d902_vhb_checks,
        "shows": [
            "Top: the middle run enlarged between the Leviathan's rear edge and the PSU's front, "
            "1.5 mm or more each side; callout 1 is Do 1 of Step 09.36.",
            "Bottom: the AC conduit (red, mains) from the rear: the SSR run behind the SSR, the "
            "stub up into the port in the wire box's front wall, the box at the mains WAGO "
            "blocks, the two R15 curves and the 34 mm run over the round deck hole; callout 2 "
            "is Do 2.",
        ],
        "insert": [
            ("09-electronics-bay.md", "Step 09.36", "first image: the three checks before VHB"),
        ],
        "verify": [
            "Bottom panel follows layout-v3.json segment coordinates (apparent mm). The stub's "
            "real length is set at B11.10 and is the step's (verify on bench); tagged. The "
            "middle-run gaps are drawn enlarged, not to scale.",
        ],
    },
    {
        "n": 903,
        "file": "903-ssr-orientation.svg",
        "title": "SSR the right way round",
        "fn": d903_ssr_orientation,
        "shows": [
            "The SSR on its metal bracket on the rear rail, from the rear with the printer on "
            "its head: INPUT pair toward the front, LOAD pair (mains, red) toward the rear, "
            "the PSU to its right with about 30 mm of rail between.",
            "Callouts 2 and 3 are the Do numbers of Step 09.18; Do 1 (open the latch) is not "
            "drawn.",
        ],
        "insert": [
            ("09-electronics-bay.md", "Step 09.18", "first image, before p.171"),
        ],
        "verify": [
            "Terminal pairs and the LED side follow LDO's placement photo, which shows INPUT "
            "toward the front and LOAD toward the rear; terminals are labelled as pairs, not "
            "one by one. Which end of the bracket carries the spring latch is not drawn: the "
            "photo does not show it clearly.",
        ],
    },
    {
        "n": 904,
        "file": "904-probe-pin-gap.svg",
        "title": "Probe pin behind the plate",
        "fn": d904_probe_gap,
        "shows": [
            "From above, rear at the top: the right bed extrusion, the build plate's straight "
            "rear edge, the probe body on the extrusion's inner face behind it on two M3×25, "
            "and its pin just behind the edge. Callouts 1–3 are the Do numbers of Step 09.30.",
            "Right: the gauge enlarged, a 2 mm hex key slides between pin and plate, a 3 mm "
            "key does not; p.161 draws 1.5 mm.",
        ],
        "insert": [
            ("09-electronics-bay.md", "Step 09.30", "first image: the gauge"),
        ],
        "verify": [
            "Probe body shape and screw positions are schematic. The straight rear edge "
            "follows LDO's Rev D heater photo (aluminium edge straight); the recess in LDO's "
            "build-plate mapping outline is schematic. 2–3 mm is the Voron startup guide's "
            "gap (fetched 2026-11-20).",
        ],
    },
    {
        "n": 905,
        "file": "905-inlet-press-in.svg",
        "title": "Press the inlet in",
        "fn": d905_inlet_press,
        "shows": [
            "Left: a cut through the inlet panel, the module (red, mains) pressed in from "
            "outside until its sprung tabs snap behind the panel wall; nothing on the spade "
            "terminals. Callouts 1 and 2 are the Do numbers of Step 09.11.",
            "Right: the face from outside with the printer upright: earth pin at the top, "
            "the switch facing out.",
        ],
        "insert": [
            ("09-electronics-bay.md", "Step 09.11", "first image: what the hands do"),
        ],
        "verify": [
            "The panel's cut-out is symmetric top to bottom (STL section), so the module fits "
            "either way up: earth pin up is the step's convention, not LDO's, and is tagged. "
            "The socket outline, the switch's side and the tab shape are schematic.",
        ],
    },
    {
        "n": 906,
        "file": "906-usb-adapter-stack.svg",
        "title": "USB-adapter stack",
        "fn": d906_usb_adapter_stack,
        "shows": [
            "Front, after the Nitehawk-SB V2 grounding photo: base, PCB and partial cover held "
            "by three M3×10, the top-right screw left bare with the DC Ground Wire's ring "
            "terminal on it.",
            "Side: cover, PCB and base in that order, the DIN clip on the base's back on two "
            "M2×10 self-tapping screws. Callouts 1–3 are the Do numbers of Step 09.25.",
        ],
        "insert": [
            ("09-electronics-bay.md", "Step 09.25", "first image, before the Nitehawk photo"),
        ],
        "verify": [
            "Layer thicknesses and the clip's screw positions are schematic. The M2×10 clip "
            "screws are the step's (verify on bench); tagged.",
        ],
    },
]
