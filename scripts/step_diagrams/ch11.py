"""Chapter 11 step diagrams (1101 onwards): Clicky-Clack door, front seal, Nevermore
plenum and the Part C side spool holder.

Geometry sources: the Clicky-Clack mod README and STLs (tanaes @62268ed, the repo's
`slicer/stl/whopping/clickyclacky_door/STLs`), its hinge cut-away render, the KB3D install
guide; LDO's Nevermore V5 Duo guide § Installation for Voron V2.4 and the
`V2_Duo_Plenum.stl` (130.0 mm wide, two Ø3.2 bores along X through its end walls);
`slicer/addons/side-spool-608769/remix.scad` and its STL for the side spool frame.
Numbered callouts are the Do numbers of the step each diagram is placed in.
"""
import draw_diagrams as dd
from draw_diagrams import (AMBER, AMBER_F, BLACKPART, BLACKPART_F, BLUE, BLUE_F, GREY, GREY_F,
                           INK, MUTED, OK, ORANGE, ORANGE_F, PANEL, RED, STEEL, Doc, T_LAB,
                           T_MIN, callout, label_bg, legend_row, profile2020, step_header)

FOAM = "#C9A227"
FOAM_F = "#F4E7B5"
PANEL_F = "#EEF3F8"      # clear polycarbonate / acrylic, seen face on
TAPE = "#3B7DD8"         # blue painter's tape


def _arrow(d, x0, y0, x1, y1, col=INK, sw=6, mk="arw", dash=None):
    d.path(f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}", stroke=col, sw=sw, marker=mk,
           dash=dash)


def _rot(x, y, r):
    for _ in range(r % 4):
        x, y = -y, x
    return x, y


def _tnut_end(d, cx, cy, k, face, col=GREY, fill=GREY_F):
    """A T-nut seen end-on in the slot of `face` (0 top, 1 right, 2 bottom, 3 left) of a
    2020 section centred on (cx, cy), k px per mm."""
    pts = [(-4.9, -8.0), (4.9, -8.0), (4.9, -6.9), (2.6, -4.3), (-2.6, -4.3), (-4.9, -6.9)]
    d.poly([(cx + _rot(x, y, face)[0] * k, cy + _rot(x, y, face)[1] * k) for x, y in pts],
           fill=fill, stroke=col, sw=2.5)


def _vbar(d, x, y0, y1, w, slot=True):
    """An extrusion seen side on, running up and down: w px wide, slot lines at +-3.1 mm."""
    d.rect(x, y0, w, y1 - y0, fill=BLUE_F, stroke=BLUE, sw=3)
    if slot:
        for f in (0.345, 0.655):
            d.line(x + w * f, y0 + 3, x + w * f, y1 - 3, stroke=BLUE, sw=1.6, op=0.55)


def _hbar(d, x0, x1, y, h, slot=True):
    d.rect(x0, y, x1 - x0, h, fill=BLUE_F, stroke=BLUE, sw=3)
    if slot:
        for f in (0.345, 0.655):
            d.line(x0 + 3, y + h * f, x1 - 3, y + h * f, stroke=BLUE, sw=1.6, op=0.55)


def _screw_dot(d, x, y, r=9):
    d.circle(x, y, r, fill=GREY_F, stroke=GREY, sw=2.5)
    d.circle(x, y, r * 0.42, fill=GREY, stroke="none", sw=0)


def _xmark(d, x, y, r=20, sw=7):
    d.line(x - r, y - r, x + r, y + r, stroke=RED, sw=sw)
    d.line(x - r, y + r, x + r, y - r, stroke=RED, sw=sw)


def _tick(d, x, y, s=1.0, sw=7):
    d.path(f"M {x - 18 * s:.1f} {y:.1f} L {x - 4 * s:.1f} {y + 14 * s:.1f} "
           f"L {x + 22 * s:.1f} {y - 16 * s:.1f}", stroke=OK, sw=sw)


def _break(d, x0, x1, y):
    """Zig-zag break line across a long part drawn shortened."""
    pts = []
    n = 6
    for i in range(n + 1):
        pts.append((x0 + (x1 - x0) * i / n, y + (10 if i % 2 else -10)))
    d.path("M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts), stroke=MUTED, sw=3)


# ============================================================ 1101 (11.62) ===
def d1101_door_hinges() -> Doc:
    """Left side elevation, front to the right: the printer's front left vertical and,
    behind a visible foam strip, the door frame's left vertical in front of it, both
    hinges with their printer half below and the door half above, pins up. Drawn as a
    top and a bottom window with a band of blue tape across the break."""
    d = Doc(1075, "Door hinges on the left front vertical, pins up")
    top = step_header(d, "Hang the door hinges")
    k = 2.6                                   # px per mm along the verticals
    W = 20 * k
    fo = 14                                   # foam strip, drawn wider than 3 mm
    px = 300                                  # printer vertical, rear (left) face
    dx = px + W + fo                          # door frame vertical, in front
    hh = 55 * k                               # each hinge half is 55 mm tall (STL)
    hw = 21 * k
    pin_x = px + W + fo / 2                   # pin axis on the foam line (schematic)
    clip_h = 12 * k
    gap = 3 * k

    fy = top + 104                            # frame top
    w1 = fy + clip_h + gap + 2 * hh + 22      # end of the top window
    w2 = w1 + 96                              # start of the bottom window
    by = w2 + 22 + 2 * hh + gap + clip_h      # frame bottom

    def window(y0, y1, brk_top, brk_bot):
        _vbar(d, px, y0, y1, W)
        _vbar(d, dx, y0, y1, W)
        d.rect(px + W, y0, fo, y1 - y0, fill=FOAM_F, stroke=FOAM, sw=2)
        if brk_top:
            _break(d, px - 10, dx + W + 10, y0)
        if brk_bot:
            _break(d, px - 10, dx + W + 10, y1)

    window(fy, w1, False, True)
    window(w2, by, True, False)
    _hbar(d, 40, px, fy, W)                   # top horizontal, running back
    _hbar(d, 40, px, by - W, W)               # bottom horizontal

    # corner clips at the top front and bottom front corners of the printer vertical
    d.rect(px - 26, fy - 12, W + 30, 12 + clip_h, fill=BLACKPART_F,
           stroke=BLACKPART, sw=3, rx=8)
    d.rect(px - 26, by - clip_h, W + 30, clip_h + 12, fill=BLACKPART_F,
           stroke=BLACKPART, sw=3, rx=8)

    def hinge(y_top):
        """Door half (sleeve) on the door frame above, printer half (solid) below, one
        pin pressed into the printer half and standing 20 mm up into the door half."""
        yd, yp = y_top, y_top + hh
        d.rect(pin_x - 4, yd, hw, hh, fill=BLACKPART_F, stroke=BLACKPART, sw=3, rx=8)
        d.rect(pin_x - hw + 4, yp, hw, hh, fill=BLACKPART, stroke=INK, sw=3, rx=8)
        for f in (0.3, 0.7):                  # two M3x8 per half into two T-nuts
            _screw_dot(d, dx + W / 2, yd + hh * f, r=8)
            _screw_dot(d, px + W / 2, yp + hh * f, r=8)
        d.line(pin_x, yp - 20 * k, pin_x, yp + hh - 8, stroke=STEEL, sw=7, dash="12 7")
        return yd, yp

    t_d, t_p = hinge(fy + clip_h + gap)
    b_d, b_p = hinge(by - clip_h - gap - 2 * hh)

    # the two verticals, named apart with leaders
    d.text(px + W / 2, fy - 58, "printer", size=T_LAB, anchor="end", weight=700,
           fill=BLUE)
    d.leader(px + W / 2 - 6, fy - 50, px + W / 2, fy - 14, col=BLUE)
    d.text(dx + W / 2 + 10, fy - 58, "door frame", size=T_LAB, weight=700, fill=BLUE)
    d.leader(dx + W / 2 + 6, fy - 50, dx + W / 2, fy - 2, col=BLUE)
    d.text(60, fy + W + 46, "printer's front", size=T_MIN, weight=700, fill=BLUE)
    d.text(60, fy + W + 82, "left vertical", size=T_MIN, weight=700, fill=BLUE)
    d.text(60, fy + W + 128, "foam between", size=T_MIN, weight=700, fill=FOAM)
    d.leader(250, fy + W + 118, px + W + fo / 2, fy + W + 150, col=FOAM)

    # the small gap under the top clip
    gx = dx + W + 46
    d.line(gx - 18, fy + clip_h, gx + 18, fy + clip_h, stroke=INK, sw=2.5)
    d.line(gx - 18, t_d, gx + 18, t_d, stroke=INK, sw=2.5)
    _arrow(d, gx, fy + clip_h - 40, gx, fy + clip_h - 2, sw=3)
    _arrow(d, gx, t_d + 40, gx, t_d + 2, sw=3)
    d.text(gx + 30, fy + clip_h + 12, "small gap", size=T_LAB, weight=700)

    # pins up: an arrow beside the top printer half
    ax = dx + W + 46
    _arrow(d, ax, t_p + hh - 6, ax, t_p + 26, col=ORANGE, sw=7, mk="arwo")
    d.text(ax + 26, t_p + hh / 2 + 6, "pin up", size=T_LAB, weight=700, fill=ORANGE)
    callout(d, ax + 168, t_p + hh / 2 - 6, 2)
    d.text(dx + W + 24, t_d + hh / 2 + 22, "door half", size=T_LAB, weight=700)
    d.text(px - 34, t_p + hh / 2 - 6, "printer", size=T_LAB, anchor="end", weight=700)
    d.text(px - 34, t_p + hh / 2 + 32, "half", size=T_LAB, anchor="end", weight=700)

    # break band: blue tape across both verticals, holding the door while you work
    ty = (w1 + w2) / 2 - 16
    d.rect(px - 30, ty, (dx + W + 30) - (px - 30), 32, fill=TAPE, stroke=TAPE, sw=1,
           op=0.85)
    callout(d, px - 70, ty + 16, 1)
    d.text(dx + W + 46, ty + 27, "blue tape", size=T_LAB, weight=700, fill=TAPE)

    # tighten all eight once the door hangs parallel: on the bottom hinge's screws
    callout(d, dx + W + 52, b_d + hh * 0.5, 3)
    d.leader(dx + W + 24, b_d + hh * 0.5, dx + W / 2 + 10, b_d + hh * 0.7, col=INK)
    d.text(dx + W + 100, b_d + hh * 0.5 + 12, "screws", size=T_LAB, weight=700)

    d.text(px - 30, by + 48, "bottom corner clip", size=T_MIN, anchor="middle",
           weight=700)
    d.text(40, fy - 22, "top corner clip", size=T_MIN, weight=700)
    d.text(dx + W + 46, by + 48, "FRONT \u2192", size=T_LAB, weight=800, fill=BLUE)

    # legend, right column
    lx = 760
    y = legend_row(d, lx, top + 230, 1, ["tape the door; 4 T-nuts", "in each vertical"])
    y = legend_row(d, lx, y + 46, 2, ["hinges on loosely,", "pins up, a small gap", "from each clip"])
    y = legend_row(d, lx, y + 46, 3, ["door hangs parallel:", "tighten all 8 screws"])
    d.text(lx, y + 60, "seen from the left side", size=T_MIN, fill=MUTED)
    return d


# ============================================================ 1102 (11.64) ===
def d1102_handle_latch() -> Doc:
    """Right side elevation, front to the left: door frame's right vertical, the printer's
    front right vertical behind it with the side panel edge, the latch on that edge, the
    handle hinges on the door, the handle over the latch, paper shims, slide arrow."""
    d = Doc(1000, "Handle and latch on the right side, lined up with a paper shim")
    top = step_header(d, "Line up the handle")
    k = 3.5
    W = 20 * k
    dx = 400                                  # door vertical, front (left) face
    px = dx + W + 3 * k                       # printer vertical behind 3 mm of foam
    pe = px + 13.5 * k                        # side panel edge, 13.5 mm behind the front
    y0, y1 = top + 60, d.h - 90
    lc = (y0 + y1) / 2 + 10                   # latch centre
    hH, hW = 60 * k, 68 * k                   # handle (STL 68 x 60)
    gH, gW = 29 * k, 26 * k                   # handle hinge, schematic width
    lH, lW = 58 * k, 26 * k                   # latch (STL 58 tall)
    shim = 7

    # side panel behind the printer vertical, cut off to the right
    d.rect(pe, y0, 700 - pe, y1 - y0, fill=PANEL_F, stroke="none", sw=0)
    d.line(pe, y0, pe, y1, stroke=MUTED, sw=3)
    _vbar(d, dx, y0, y1, W)
    d.rect(dx + W, y0, 3 * k, y1 - y0, fill=FOAM_F, stroke=FOAM, sw=1.5)
    _vbar(d, px, y0, y1, W)
    d.rect(pe, y0, 700 - pe, y1 - y0, fill=PANEL_F, stroke="none", sw=0, op=0.55)
    d.line(pe, y0, pe, y1, stroke=MUTED, sw=3, dash="14 8")
    for x in (dx - 10,):
        _break(d, x, 710, y0)
        _break(d, x, 710, y1)

    # latch on the printer vertical, its panel clip over the panel edge (behind the handle)
    lx0 = px + 2 * k
    d.rect(lx0, lc - lH / 2, lW, lH, fill=BLACKPART, stroke=INK, sw=3, rx=10)
    _screw_dot(d, lx0 + lW / 2, lc - lH / 2 + 34)
    _screw_dot(d, lx0 + lW / 2, lc + lH / 2 - 34)

    # handle hinges on the door frame, handle between them over the latch
    gx0 = dx + 2
    ht = lc - hH / 2
    for gy in (ht - shim - gH, lc + hH / 2 + shim):
        d.rect(gx0, gy, gW, gH, fill=BLACKPART_F, stroke=BLACKPART, sw=3, rx=8)
        _screw_dot(d, gx0 + gW * 0.3, gy + gH / 2)
        _screw_dot(d, gx0 + gW * 0.72, gy + gH / 2)
    d.rect(gx0, ht, hW, hH, fill=ORANGE_F, stroke=ORANGE, sw=4, rx=14, op=0.55)
    d.rect(gx0, ht, hW, hH, fill="none", stroke=ORANGE, sw=5, rx=14)
    d.rect(lx0, lc - lH / 2, lW, lH, fill="none", stroke=INK, sw=3, rx=10, dash="10 7")
    # paper shims at both ends of the handle
    for sy in (ht - shim, lc + hH / 2):
        d.rect(gx0 - 40, sy, gW + 60, shim, fill=PANEL, stroke=INK, sw=2)

    # slide to line up
    ax = dx - 70
    _arrow(d, ax, lc, ax, ht - 16, sw=6)
    _arrow(d, ax, lc, ax, lc + hH / 2 + 16, sw=6)

    # labels
    d.text(ax - 30, lc - 20, "slide to", size=T_LAB, anchor="end", weight=700)
    d.text(ax - 30, lc + 20, "line up", size=T_LAB, anchor="end", weight=700)
    callout(d, ax - 80, lc + 80, 3)
    d.text(gx0 - 48, ht - shim - gH - 14, "handle hinge", size=T_LAB, anchor="end",
           weight=700)
    callout(d, gx0 - 40, ht - shim - gH + 40, 1)
    d.text(gx0 - 56, lc + hH / 2 + 78, "paper shim", size=T_LAB, anchor="end", weight=700)
    d.leader(gx0 - 36, lc + hH / 2 + 6, gx0 - 60, lc + hH / 2 + 52, col=INK)
    d.text(gx0 + hW + 18, ht + 30, "handle", size=T_LAB, weight=800, fill=ORANGE)
    label_bg(d, 860, lc - 20, "latch,", size=T_LAB, bg="#FBFAF8")
    label_bg(d, 860, lc + 20, "behind the handle", size=T_LAB, bg="#FBFAF8")
    d.leader(lx0 + lW - 4, lc - 32, 740, lc - 32, col=INK)
    callout(d, 790, lc + 92, 2)
    d.leader(762, lc + 92, lx0 + lW - 4, lc + 40, col=INK)
    d.text(830, lc + 104, "centre, tighten", size=T_MIN, weight=700)
    d.text(dx, y1 + 56, "← FRONT", size=T_LAB, weight=800, fill=BLUE)
    d.text(dx + W / 2, y0 - 16, "door", size=T_LAB, anchor="middle", weight=700, fill=BLUE)
    d.text(px + W / 2 + 40, y0 - 16, "printer", size=T_LAB, anchor="start", weight=700,
           fill=BLUE)
    d.text(720, y1 - 24, "side panel", size=T_LAB, weight=700, fill=MUTED)
    return d


# ============================================================ 1103 (11.51) ===
def d1103_front_foam() -> Doc:
    """Top: a section seen from above through the left side of the front opening, front
    at the bottom. Bottom: the opening seen from the front, foam corners butted."""
    d = Doc(1075, "3 mm foam on the front face of the front opening, corners butted")
    top = step_header(d, "Foam on the front face")

    # ---- section from above, FRONT at the bottom
    d.panel(30, top + 16, 1140, 500)
    k = 6.6
    W = 20 * k
    cx = 330
    py = top + 50 + W / 2                     # printer vertical centre
    fy0 = py + W / 2                          # its front face
    foam = 3 * k
    dy = fy0 + foam + W / 2                   # door vertical centre
    profile2020(d, cx, py, k)
    profile2020(d, cx, dy, k)
    # foam: on the front face, along the inner edge (toward the opening, right)
    d.rect(cx + 1 * k, fy0, 9 * k, foam, fill=FOAM, stroke=INK, sw=2)
    # acrylic in the door frame's inner slot, running into the opening
    d.rect(cx + 4 * k, dy - 1.5 * k, 290 - 4 * k, 3 * k, fill=PANEL_F, stroke=MUTED, sw=2.5)
    _break(d, cx + 290, cx + 290, dy)
    d.text(cx + 290, dy + 3 * k + 36, "door panel", size=T_LAB, anchor="end", weight=700,
           fill=MUTED)
    # labels
    d.text(cx - W / 2 - 24, py - 8, "printer's front", size=T_LAB, anchor="end",
           weight=700, fill=BLUE)
    d.text(cx - W / 2 - 24, py + 30, "left vertical", size=T_LAB, anchor="end", weight=700,
           fill=BLUE)
    d.text(cx - W / 2 - 24, dy + 12, "door frame", size=T_LAB, anchor="end", weight=700,
           fill=BLUE)
    fx = cx + 5 * k
    d.leader(fx + 30, fy0 + foam / 2, 640, fy0 - 50, col=INK)
    d.text(650, fy0 - 76, "3 mm foam on the", size=T_LAB, weight=700)
    d.text(650, fy0 - 38, "front face, inner edge", size=T_LAB, weight=700)
    d.text(650, py - W / 2 - 4, "inside the chamber", size=T_MIN, fill=MUTED)
    _arrow(d, cx, dy + W / 2 + 74, cx, dy + W / 2 + 12, col=ORANGE, sw=7, mk="arwo")
    d.text(cx + 34, dy + W / 2 + 56, "the door closes onto the foam", size=T_LAB,
           weight=700, fill=ORANGE)
    d.text(1150, top + 500, "seen from above, FRONT at the bottom", size=T_MIN,
           anchor="end", fill=MUTED)
    for i, ln in enumerate(("or on the door frame's", "back face instead: check",
                            "on the bench, never both")):
        d.text(650, fy0 + 12 + 36 * i, ln, size=T_MIN, weight=700, fill=AMBER)

    # ---- the opening from the front: four strips, corners butted
    by = top + 530
    d.panel(30, by, 1140, d.h - by - 16)
    s, e, f = 380, 32, 15                      # opening outline, extrusion, foam (schematic)
    x0, y0 = 90, by + 40
    d.rect(x0, y0, s, s, fill=BLUE_F, stroke=BLUE, sw=3)
    d.rect(x0 + e, y0 + e, s - 2 * e, s - 2 * e, fill=PANEL, stroke=BLUE, sw=3)
    i0, i1 = x0 + e, x0 + s - e
    j0, j1 = y0 + e, y0 + s - e
    for (a, b, w, h) in ((i0 - f, j0 - f, i1 - i0 + 2 * f, f),           # top, full
                         (i0 - f, j1, i1 - i0 + 2 * f, f),               # bottom, full
                         (i0 - f, j0, f, j1 - j0),                       # left, butted
                         (i1, j0, f, j1 - j0)):                          # right, butted
        d.rect(a, b, w, h, fill=FOAM, stroke=INK, sw=2)
    _tick(d, x0 + s + 60, y0 + 40, 1.4)
    d.text(x0 + s + 96, y0 + 42, "corners", size=T_LAB, weight=700, fill=OK)
    d.text(x0 + s + 96, y0 + 80, "butted", size=T_LAB, weight=700, fill=OK)
    d.text(x0 + s + 40, y0 + s - 50, "the opening,", size=T_MIN, fill=MUTED)
    d.text(x0 + s + 40, y0 + s - 12, "from the front", size=T_MIN, fill=MUTED)
    # wrong: overlapped corner, small
    wx, wy = 860, by + 120
    d.rect(wx, wy, 220, 40, fill=FOAM, stroke=INK, sw=2)
    d.rect(wx, wy - 20, 40, 220, fill=FOAM, stroke=INK, sw=2)
    d.rect(wx, wy, 40, 40, fill="#B98C10", stroke=INK, sw=2)
    _xmark(d, wx + 140, wy + 120, 26)
    d.text(wx - 40, wy - 50, "Wrong:", size=T_LAB, weight=700, fill=RED)
    d.text(wx + 80, wy - 50, "overlapped", size=T_LAB, weight=700, fill=RED)
    d.text(wx + 70, wy + 210, "a bump that", size=T_LAB, weight=700, fill=RED)
    d.text(wx + 70, wy + 248, "leaks", size=T_LAB, weight=700, fill=RED)
    return d


# ============================================================ 1104 (11.44) ===
def d1104_door_frame_order() -> Doc:
    """Three rows, one per Do number: screws started in the tapped 470s, the two 530s
    fitted to one 470 through their access holes, the panel slid in and the last side."""
    d = Doc(1075, "Clicky-Clack door frame: the order")
    top = step_header(d, "Door frame, in this order")
    s = 0.55                                   # px per mm along the bars
    e = 30                                     # bar width drawn, schematic
    X0 = 120                                   # left edge of the frame drawings
    L = 470 * s
    fw = L + 2 * e                             # outer width
    vh = 530 * s                               # vertical height
    tx = 640                                   # text column

    def bar_h(x, y):
        _hbar(d, x, x + L, y, e)

    def end_screw(x, y, sign):
        """M5 BHCS started halfway: head and half the 16 mm shank outside the end."""
        dd._bhcs(d, x + sign * 8 * 2.6, y + e / 2, 2.6, -sign, 0, 16, solid=8, head_d=9.5)

    def u_frame(y_top, keys):
        yb = y_top + vh - e
        _vbar(d, X0, y_top, y_top + vh, e)
        _vbar(d, X0 + fw - e, y_top, y_top + vh, e)
        bar_h(X0 + e, yb)
        for x in (X0 - 5, X0 + fw + 5):        # access holes on the outer faces
            d.circle(x, yb + e / 2, 8, fill=INK, stroke=PANEL, sw=2.5)
        if keys:
            for x0, x1 in ((X0 - 90, X0 - 16), (X0 + fw + 90, X0 + fw + 16)):
                _arrow(d, x0, yb + e / 2, x1, yb + e / 2, col=INK, sw=5)
            for x, sg in ((X0 + e, 1), (X0 + fw - e, -1)):      # square corners
                d.path(f"M {x + sg * 34} {yb} L {x + sg * 34} {yb - 34} L {x} {yb - 34}",
                       stroke=OK, sw=5)
        return yb

    # row 1: screws started halfway into both tapped ends of a 470
    ry = top
    by = ry + 110
    bar_h(X0 + e, by)
    end_screw(X0 + e, by, -1)
    end_screw(X0 + e + L, by, 1)
    d.text(X0 + fw / 2, by - 20, "470 mm, tapped ends", size=T_MIN, anchor="middle",
           weight=700, fill=BLUE)
    d.text(X0 + fw / 2, by + e + 44, "two of these", size=T_MIN, anchor="middle", fill=MUTED)
    legend_row(d, tx, ry + 104, 1, ["Start a screw halfway", "into each tapped end"])

    # row 2: the two 530s fitted to one 470, corners squared
    ry = top + 190
    d.line(40, ry, d.w - 40, ry, stroke=dd.RULE, sw=2)
    u_frame(ry + 40, True)
    d.text(X0 + fw / 2, ry + 40 + vh / 2 - 30, "530 mm", size=T_MIN, anchor="middle",
           weight=700, fill=BLUE)
    d.text(X0 + fw / 2, ry + 40 + vh / 2 + 10, "both sides", size=T_MIN, anchor="middle",
           weight=700, fill=BLUE)
    d.text(X0 + fw / 2, ry + 40 + vh + 44, "key in through the access holes", size=T_MIN,
           anchor="middle", fill=MUTED)
    legend_row(d, tx, ry + 140, 2, ["Fit both 530 mm", "pieces, then square", "each corner"])

    # row 3: panel slides into the slots, then the fourth side
    ry = top + 190 + vh + 96
    d.line(40, ry, d.w - 40, ry, stroke=dd.RULE, sw=2)
    u_top = ry + 76
    u_frame(u_top, False)
    d.rect(X0 + e - 5 * s, u_top - 50, 480 * s, vh - e + 50 - 4 * s, fill=PANEL_F,
           stroke=MUTED, sw=2.5, op=0.9)
    d.text(X0 + fw / 2, u_top + vh - 80, "acrylic", size=T_MIN, anchor="middle",
           weight=700, fill=MUTED)
    _arrow(d, X0 + fw / 2, u_top + 30, X0 + fw / 2, u_top + 150, col=ORANGE, sw=8,
           mk="arwo")
    bar_h(X0 + e, ry + 16)
    _arrow(d, X0 + fw + 46, ry + 20, X0 + fw + 46, u_top - 6, col=ORANGE, sw=7, mk="arwo")
    legend_row(d, tx, ry + 150, 3, ["Slide the acrylic in,", "then close the", "fourth side"])
    return d


# ============================================================ 1105 (11.38) ===
def d1105_plenum_mount() -> Doc:
    """Top view, FRONT at the bottom: the plenum filling the 130 mm gap between the bed
    extrusions just behind the front corner brackets, one M3x12 out through each end wall
    into a T-nut in the extrusion's inside face. Below: that face end-on, and the top
    slot marked wrong."""
    d = Doc(1075, "Nevermore plenum between the bed extrusions, T-nuts in the inside faces")
    top = step_header(d, "Plenum between the bed extrusions")
    k = 3.2
    W = 20 * k
    cx = 600
    gap = 130 * k
    lx1, rx0 = cx - gap / 2, cx + gap / 2            # inside faces
    lx0, rx1 = lx1 - W, rx0 + W
    ry0 = top + 520                                   # front rail, its inner (rear) face
    yb = top + 40                                     # where the view stops, rearward
    # front rail and the two bed extrusions running back from its inner face
    _hbar(d, 120, 1080, ry0, W)
    for x in (lx0, rx0):
        _vbar(d, x, yb, ry0, W)
        _break(d, x - 8, x + W + 8, yb)
        d.rect(x - 10, ry0 - 26, W + 20, 26 + W - 6, fill=GREY_F, stroke=GREY, sw=2.5,
               rx=4)                                  # front corner bracket
    # plenum: 130 x 68.6 mm, just behind the brackets; bores 6.2 mm from its rear edge
    pf = ry0 - 30 - 6                                 # front edge (schematic distance)
    pr = pf - 68.6 * k
    d.rect(lx1, pr, gap, pf - pr, fill=BLACKPART_F, stroke=BLACKPART, sw=3.5, rx=10)
    d.text(cx, (pf + pr) / 2 + 24, "plenum", size=T_LAB + 6, anchor="middle", weight=800,
           fill=BLACKPART)
    sy = pr + 6.2 * k
    for x_face, sg in ((lx1, -1), (rx0, 1)):
        # T-nut inside the extrusion just behind its inside face, M3x12 out to it
        tx = x_face + sg * 5.5 * k
        d.rect(min(tx, tx + sg * 3 * k), sy - 5 * k, 3 * k, 10 * k, fill=GREY, stroke=INK,
               sw=2)
        hx = x_face - sg * 6 * k                      # head seat inside the end wall
        d.rect(min(hx, hx - sg * 3 * k), sy - 2.75 * k, 3 * k, 5.5 * k, fill=GREY_F,
               stroke=GREY, sw=2.5)
        d.line(hx, sy, x_face + sg * 6 * k, sy, stroke=GREY, sw=5 * k * 0.5)
    d.text(lx0 - 20, (yb + pr) / 2, "bed", size=T_LAB, anchor="end", weight=700, fill=BLUE)
    d.text(lx0 - 20, (yb + pr) / 2 + 38, "extrusion", size=T_LAB, anchor="end", weight=700,
           fill=BLUE)
    d.leader(rx1 - 18, sy - 2, 900, yb + 60, col=INK)
    d.text(910, yb + 50, "M3\u00d712 into a", size=T_LAB, weight=700)
    d.text(910, yb + 88, "T-nut in the", size=T_LAB, weight=700)
    d.text(910, yb + 126, "inside face", size=T_LAB, weight=700)
    dmy = pr - 70
    _arrow(d, cx, dmy, lx1 + 3, dmy, col=MUTED, sw=3, mk="arwm")
    _arrow(d, cx, dmy, rx0 - 3, dmy, col=MUTED, sw=3, mk="arwm")
    label_bg(d, cx, dmy - 14, "130 mm", size=T_MIN, fill=MUTED, bg=dd.BG)
    d.text(cx, ry0 + W + 44, "FRONT", size=T_LAB, anchor="middle", weight=800, fill=BLUE)
    d.text(1150, ry0 + W + 44, "seen from above", size=T_MIN, anchor="end", fill=MUTED)

    # ---- end-on: inside face right, top slot wrong
    py = ry0 + W + 70
    d.panel(30, py, 1140, d.h - py - 16)
    kk = 5.6
    c1 = (420, py + 160)
    profile2020(d, *c1, kk)
    _tnut_end(d, *c1, kk, 3)
    fx = c1[0] - 10 * kk                              # the inside face
    d.rect(fx - 6 * kk, c1[1] - 16 * kk, 6 * kk, 32 * kk, fill=BLACKPART_F,
           stroke=BLACKPART, sw=3)                    # plenum end wall, 6 mm
    d.rect(fx - 6 * kk - 3 * kk, c1[1] - 2.75 * kk, 3 * kk, 5.5 * kk, fill=GREY_F,
           stroke=GREY, sw=2.5)                       # SHCS head
    d.rect(fx - 6 * kk, c1[1] - 1.5 * kk, 12 * kk, 3 * kk, fill=GREY_F, stroke=GREY, sw=2)
    _tick(d, c1[0] + 10 * kk + 60, c1[1] - 10, 1.6)
    d.text(80, py + 48, "Right: the inside face", size=T_LAB, weight=700, fill=OK)
    d.text(fx - 3 * kk, c1[1] + 16 * kk + 40, "plenum wall", size=T_MIN, anchor="middle",
           fill=MUTED)
    c2 = (930, py + 170)
    k2 = 4.5
    profile2020(d, *c2, k2)
    _tnut_end(d, *c2, k2, 0)
    _xmark(d, c2[0] + 10 * k2 + 50, c2[1] - 10 * k2 - 10, 22)
    d.text(790, py + 48, "Wrong: top slot", size=T_LAB, weight=700, fill=RED)
    return d


# ======================================================= 1106 (11.71, 11.72) ===
# Frame outline from side_spool_frame_puck.stl (remix.scad, view "installed"), as
# (b, d): b mm behind the frame's front face, d mm below the top face.
_FRAME_BODY = [(148.75, 13.1), (211.25, 13.1), (211.25, 46.9), (46.25, 211.9),
               (13.0, 211.9), (13.0, 148.15), (35.0, 148.15), (147.5, 36.9),
               (148.75, 36.9)]
_FOOT_FRONT = (0.0, 147.0, 13.0, 212.0)          # b0, d0, b1, d1 on the front vertical
_FOOT_TOP = (148.75, 0.6, 211.25, 13.0)          # on the top extrusion
_PUCK = (110.4, 110.36)                          # puck axis; boss r 31.5, puck flange 60.2
_SCREWS = [(10.0, 180.0), (180.0, 10.0)]         # frame screws, in the outer slots


def d1106_side_spool() -> Doc:
    """Right side elevation, FRONT to the left: the side spool frame's two feet on the top
    extrusion and the front vertical, a T-nut in each outer slot, the puck and the Drybox
    outline. Callouts 1 and 2 are Step 11.71's Do numbers."""
    d = Doc(1075, "Side spool frame on the right side")
    top = step_header(d, "Hang the side spool frame")
    k = 3.3
    X0, Y0 = 196, top + 96                       # frame front face / top face on the page

    def P(b, dd_):
        return X0 + b * k, Y0 + dd_ * k

    bmax, dmax = 288, 232
    # side panel: covers all but a 13.5 mm strip at the frame edges
    x, y = P(13.5, 13.5)
    d.rect(x, y, P(bmax, 0)[0] - x, P(0, dmax)[1] - y, fill=PANEL_F, stroke=MUTED, sw=2)
    # extrusions: top (side face, d 0..20) and the front vertical (b 0..20)
    _hbar(d, X0, P(bmax, 0)[0], Y0, 20 * k)
    _vbar(d, X0, Y0, P(0, dmax)[1], 20 * k)
    _break(d, P(bmax, 0)[0], P(bmax, 0)[0], Y0 + 10 * k)
    _break(d, X0 - 6, X0 + 20 * k + 6, P(0, dmax)[1])
    # Drybox outline (217 x 219, centred on the puck)
    bx0, dy0 = _PUCK[0] - 109.5, _PUCK[1] - 108.5
    x0, y0 = P(bx0, dy0)
    d.rect(x0, y0, 219 * k, 217 * k, fill="none", stroke=MUTED, sw=3, dash="14 9", rx=10)
    # the frame: body, then the two feet on bare aluminium
    d.poly([P(b, dd_) for b, dd_ in _FRAME_BODY], fill=BLACKPART_F, stroke=BLACKPART, sw=3.5)
    pc = P(*_PUCK)
    d.circle(*pc, 31.5 * k, fill=BLACKPART_F, stroke=BLACKPART, sw=3.5)
    for f in (_FOOT_FRONT, _FOOT_TOP):
        a, c = P(f[0], f[1]), P(f[2], f[3])
        d.rect(a[0], a[1], c[0] - a[0], c[1] - a[1], fill=BLACKPART, stroke=INK, sw=2.5)
    for sc in _SCREWS:
        _screw_dot(d, *P(*sc), r=11)
    # puck (blue accent part) and its four screws
    d.circle(*pc, 30.1 * k, fill=ORANGE_F, stroke=ORANGE, sw=4)
    for sx in (-13, 13):
        for sy in (-13, 13):
            _screw_dot(d, pc[0] + sx * k, pc[1] + sy * k, r=7)

    # 1: a T-nut in each outer slot, under each foot's screw hole
    st, sv = P(*_SCREWS[1]), P(*_SCREWS[0])
    callout(d, X0 + 470, Y0 - 34, 1)
    d.leader(X0 + 496, Y0 - 26, st[0] - 6, st[1] - 8, col=INK)
    d.text(X0, Y0 - 22, "T-nut in each outer slot", size=T_MIN, weight=700)
    callout(d, X0 - 50, sv[1], 1)
    d.leader(X0 - 22, sv[1], sv[0] - 12, sv[1], col=INK)
    # 2: frame up, puck out, both screws snug, feet on bare aluminium
    fx, fy = P(13, 200)
    callout(d, X0 + 130, P(0, dmax)[1] + 54, 2)
    d.leader(X0 + 102, P(0, dmax)[1] + 44, fx - 10, fy, col=INK)
    d.text(X0 + 172, P(0, dmax)[1] + 50, "both dark feet on bare aluminium,", size=T_MIN,
           weight=700)
    d.text(X0 + 172, P(0, dmax)[1] + 88, "screws snug, puck facing out", size=T_MIN,
           weight=700)
    d.text(pc[0] + 36 * k, pc[1] + 10, "puck", size=T_LAB, weight=800, fill=ORANGE)
    d.text(P(bmax, 0)[0] - 4, Y0 + 20 * k + 50, "Drybox outline", size=T_MIN,
           anchor="end", fill=MUTED)
    d.text(X0 - 16, Y0 + 330, "\u2190 FRONT", size=T_LAB, anchor="end", weight=800,
           fill=BLUE)
    d.text(P(bmax, 0)[0] - 4, Y0 + 20 * k + 88, "seen from outside", size=T_MIN,
           anchor="end", fill=MUTED)
    return d


# ============================================================ 1107 (11.72) ===
def d1107_tube_route() -> Doc:
    """Top view, FRONT at the bottom: the top frame, the tube holder in the top right
    extrusion's top slot about 22 cm behind the front, the bowden retainer on the top rear
    extrusion beside the exhaust cover, and one PTFE run from the CW2.5 out through the
    cover's coupler, through the retainer, forward to the holder and down to the spool
    outside the right side. Callouts 1 to 3 are Step 11.72's Do numbers."""
    d = Doc(1000, "One PTFE from the CW2.5 to the side spool, seen from above")
    top = step_header(d, "One new tube, seen from above")
    k = 1.25                                     # px per mm
    W = 20 * k
    F = 510 * k                                  # frame outer width and depth
    X0 = 70                                      # frame left outer edge
    Yr = top + 130                               # frame rear outer edge
    Yf = Yr + F                                  # frame front outer edge
    Xr = X0 + F                                  # frame right outer edge
    # the four top extrusions
    _hbar(d, X0, Xr, Yr, W)
    _hbar(d, X0, Xr, Yf - W, W)
    _vbar(d, X0, Yr + W, Yf - W, W)
    _vbar(d, Xr - W, Yr + W, Yf - W, W)
    d.rect(X0 + W, Yr + W, F - 2 * W, F - 2 * W, fill=PANEL_F, stroke="none", sw=0)
    # back panel edge and the exhaust cover outside it, at the centre
    cxm = X0 + F / 2
    d.line(X0, Yr - 6, Xr, Yr - 6, stroke=MUTED, sw=3)
    d.rect(cxm - 50, Yr - 40, 100, 34, fill=BLACKPART_F, stroke=BLACKPART, sw=3, rx=6)
    cpl = (cxm, Yr - 23)
    d.circle(*cpl, 8, fill=GREY_F, stroke=GREY, sw=2.5)
    d.text(cxm - 62, Yr - 14, "exhaust cover", size=T_MIN, anchor="end", weight=700)
    # bowden retainer on the top rear extrusion, hanging over the back (schematic spot)
    rx = cxm + 150
    d.rect(rx - 22, Yr - 20, 44, W + 26, fill=BLACKPART, stroke=INK, sw=2.5, rx=4)
    # tube holder in the top right extrusion's top slot, about 22 cm behind the front
    hy0 = Yf - 220 * k - 65.5 * k
    d.rect(Xr - W - 4, hy0, W + 8, 65.5 * k, fill=BLACKPART, stroke=INK, sw=2.5, rx=4)
    # the spool and Drybox outside the right side, from the front to about 22 cm back
    sx0 = Xr + 22
    d.rect(sx0, Yf - 221 * k, 120 * k, 219 * k, fill="none", stroke=MUTED, sw=3,
           dash="14 9", rx=10)
    d.text(sx0 + 60 * k, Yf - 66, "spool,", size=T_MIN, anchor="middle",
           fill=MUTED, weight=700)
    d.text(sx0 + 60 * k, Yf - 30, "Drybox", size=T_MIN, anchor="middle",
           fill=MUTED, weight=700)
    # toolhead inside, front left, gantry low
    th = (X0 + 130, Yf - 120)
    d.rect(th[0] - 34, th[1] - 26, 68, 52, fill=BLUE_F, stroke=BLUE, sw=3, rx=8)
    d.text(th[0], th[1] + 60, "CW2.5", size=T_MIN, anchor="middle", weight=700, fill=BLUE)
    # the one tube
    hx, hy = Xr - W / 2, hy0 + 65.5 * k / 2
    sp = (sx0 + 60 * k, Yf - 150 * k)
    d.path(f"M {th[0]:.1f} {th[1] - 26:.1f} C {th[0] + 40:.1f} {Yr + 200:.1f} "
           f"{cpl[0] - 60:.1f} {cpl[1] + 120:.1f} {cpl[0]:.1f} {cpl[1]:.1f} "
           f"C {cpl[0] + 40:.1f} {cpl[1] - 70:.1f} {rx - 40:.1f} {Yr - 70:.1f} {rx:.1f} {Yr:.1f} "
           f"C {rx + 120:.1f} {Yr + 60:.1f} {hx:.1f} {hy - 160:.1f} {hx:.1f} {hy:.1f} "
           f"C {hx:.1f} {hy + 60:.1f} {sp[0]:.1f} {sp[1] - 80:.1f} {sp[0]:.1f} {sp[1]:.1f}",
           stroke=ORANGE, sw=6)
    # 1: the holder; 2: the route; 3: cut square at the spool
    callout(d, Xr + 70, hy0 - 10, 1)
    d.text(Xr + 110, hy0 + 2, "holder, top slot,", size=T_MIN, weight=700)
    d.text(Xr + 110, hy0 + 38, "about 22 cm back", size=T_MIN, weight=700)
    callout(d, rx + 70, Yr - 60, 2)
    d.text(rx + 110, Yr - 48, "retainer", size=T_MIN, weight=700)
    callout(d, sx0 + 120 * k + 44, sp[1], 3)
    d.leader(sx0 + 120 * k + 16, sp[1], sp[0] + 6, sp[1], col=INK)
    d.text(sx0 + 120 * k + 84, sp[1] + 11, "cut square", size=T_MIN, weight=700)
    # 22 cm dimension along the right edge, inside
    dx_ = Xr - W - 40
    _arrow(d, dx_, (Yf + hy0 + 65.5 * k) / 2, dx_, Yf - 4, col=MUTED, sw=3, mk="arwm")
    _arrow(d, dx_, (Yf + hy0 + 65.5 * k) / 2, dx_, hy0 + 65.5 * k + 4, col=MUTED, sw=3,
           mk="arwm")
    label_bg(d, dx_ - 12, (Yf + hy0 + 65.5 * k) / 2 + 10, "22 cm", size=T_MIN, anchor="end",
             fill=MUTED, bg=PANEL_F)
    for i, ln in enumerate(("holder spot:", "check on the bench")):
        d.text(X0 + F / 2, Yf - 300 + 36 * i, ln, size=T_MIN, anchor="middle", weight=700,
               fill=AMBER)
    d.text(X0 + F / 2, Yf + 50, "FRONT", size=T_LAB, anchor="middle", weight=800, fill=BLUE)
    d.text(1150, Yf + 50, "seen from above", size=T_MIN, anchor="end", fill=MUTED)
    return d


DIAGRAMS = [
    {
        "n": 1101,
        "file": "1101-door-hinges-pins-up.svg",
        "title": "Door hinges on the left front vertical, pins up",
        "fn": d1101_door_hinges,
        "shows": [
            "The machine's left side, front to the right: the printer's front left vertical "
            "and, a labelled foam strip in front of it, the door frame's left vertical, each "
            "named with a leader; a band of blue tape across both.",
            "Two hinges, each a printer half below (pin pointing up) and the door half above "
            "it, the top one just under the top corner clip with a small gap, the bottom one "
            "just above the bottom corner clip; two screws per half.",
            "Callouts 1 to 3 are Step 11.62's Do numbers: tape and T-nuts, hinges on loosely "
            "pins up, all eight screws tightened once the door hangs parallel.",
        ],
        "insert": [
            ("11-skirts-panels-door.md", "Step 11.62", "first image: what the hands do"),
        ],
        "verify": [
            "Hinge outlines are schematic boxes. The pin axis is drawn on the foam line between "
            "the two verticals; its exact front-to-back position is not dimensioned.",
            "The printer half carries the pin, pointing up, with the door half on top: from the "
            "README ('pins should point up', the door 'can be easily removed from the hinges "
            "simply by lifting up') and tanaes' hinge cut-away render. KB3D's photos do not "
            "show which half is which clearly.",
            "Heights along the vertical are schematic: KB3D's guide puts the hinges against the "
            "top and bottom corner clips with a little gap. Both halves screw into the outer "
            "side-face slot of their vertical, as KB3D's photos show.",
        ],
    },
    {
        "n": 1102,
        "file": "1102-handle-latch-shim.svg",
        "title": "Handle and latch on the right side, lined up with a paper shim",
        "fn": d1102_handle_latch,
        "shows": [
            "The machine's right side, front to the left: the door frame's right vertical, "
            "3 mm of foam, the printer's front right vertical and the side panel's edge.",
            "The latch on the printer vertical over the panel edge (callout 2: centred and "
            "tightened first), the two handle hinges on the door frame (callout 1), the "
            "handle between them over the latch, a paper shim at each end of the handle, and "
            "the up-and-down slide that lines the handle up (callout 3).",
            "Callouts 1 to 3 are Step 11.64's Do numbers.",
        ],
        "insert": [
            ("11-skirts-panels-door.md", "Step 11.64", "first image: what the hands do"),
        ],
        "verify": [
            "Outlines are schematic: the handle (60 mm) and latch (58 mm) heights are from their "
            "STLs; the handle-hinge widths and the gaps in the stack are not to scale.",
            "The latch takes the place of the side panel's front-edge midspan clip (11.63), "
            "centred on that edge, from the KB3D guide; the side panel edge is drawn 13.5 mm "
            "behind the front face (483 mm panel on a 510 mm frame).",
        ],
    },
    {
        "n": 1103,
        "file": "1103-front-opening-foam.svg",
        "title": "3 mm foam on the front face of the front opening, corners butted",
        "fn": d1103_front_foam,
        "shows": [
            "A section from above through the left side of the front opening: the printer's "
            "front left vertical, 3 mm foam on its front face along the inner edge, and the "
            "door frame with its panel closing onto the foam.",
            "The opening from the front with a foam strip along the inner edge of all four "
            "extrusions, the corners butted; a small overlapped corner marked wrong.",
        ],
        "insert": [
            ("11-skirts-panels-door.md", "Step 11.51", "first image: what the hands do"),
        ],
        "verify": [
            "The foam strip's width (drawn about 9 mm) and its exact place on the face are "
            "schematic; the kit's 3 mm tape width is not published.",
            "The door frame is drawn straight in front of the printer vertical because both "
            "frames are 510 mm wide; the opening's proportions in the lower view are schematic.",
            "KB3D's guide says to put the foam 'on the inner portion of the extrusion' in its "
            "door-frame section, so the door frame's back face may be meant; the step marks "
            "it '(verify on bench)' and the drawing carries a 'check on the bench' note.",
        ],
    },
    {
        "n": 1104,
        "file": "1104-door-frame-order.svg",
        "title": "Clicky-Clack door frame: the order",
        "fn": d1104_door_frame_order,
        "shows": [
            "Row 1: an M5×16 BHCS started halfway into each tapped end of a 470 mm piece "
            "(two such pieces).",
            "Row 2: both 530 mm pieces fitted to one 470 mm piece, the key going in through "
            "the access holes on their outer faces, both corners squared.",
            "Row 3: the acrylic sliding down into the frame's slots, then the second 470 mm "
            "piece closing the fourth side. Callouts 1 to 3 are Step 11.44's Do numbers.",
        ],
        "insert": [
            ("11-skirts-panels-door.md", "Step 11.44", "first image: what the hands do"),
        ],
        "verify": [
            "Bar widths are exaggerated; the 470 and 530 mm lengths are to scale. The panel "
            "(480 × 500 mm) is drawn reaching into the slots of the 530 mm sides.",
            "The access holes are drawn at the ends of the 530 mm pieces on their outer faces, "
            "where a blind joint needs them (Ch 01's diagram 15); not dimensioned from the kit.",
        ],
    },
    {
        "n": 1105,
        "file": "1105-plenum-on-bed-extrusions.svg",
        "title": "Nevermore plenum between the bed extrusions, T-nuts in the inside faces",
        "fn": d1105_plenum_mount,
        "shows": [
            "Top view, FRONT at the bottom: the plenum filling the 130 mm gap between the two "
            "bed extrusions, just behind the front corner brackets.",
            "One M3×12 SHCS out through each end wall, near its rear edge, into a T-nut in the "
            "inside face of each bed extrusion.",
            "Below: the inside-face slot end-on with the T-nut and screw, and the top slot "
            "marked wrong.",
        ],
        "insert": [
            ("11-skirts-panels-door.md", "Step 11.38", "first image: what the hands do"),
        ],
        "verify": [
            "The plenum's distance behind the front corner brackets is schematic; LDO's CAD "
            "image (guide § Installation for Voron V2.4) shows it just behind them.",
            "From V2_Duo_Plenum.stl: 130.0 mm wide, one Ø3.2 bore along X through each end "
            "wall, 6.2 mm from one long edge; that edge is drawn as the rear, as LDO's CAD "
            "image shows the screws.",
        ],
    },
    {
        "n": 1106,
        "file": "1106-side-spool-frame-and-holder.svg",
        "title": "Side spool frame on the right side",
        "fn": d1106_side_spool,
        "shows": [
            "The right side from outside, FRONT to the left, at 3.3 px per mm from the remix "
            "STL: the frame's two feet on the 13.5 mm strip of bare aluminium beside the "
            "panel, one on the top extrusion and one on the front vertical, a screw into a "
            "T-nut in each outer slot.",
            "The puck on its boss and the USS Drybox outline (217 × 219 mm, on the puck). "
            "Callouts 1 and 2 are Step 11.71's Do numbers.",
        ],
        "insert": [
            ("11-skirts-panels-door.md", "Step 11.71", "first image: what the hands do"),
        ],
        "verify": [
            "The panel edge is drawn 13.5 mm in from the frame edges (483 mm panel on a 510 mm "
            "frame); the frame outline, feet and puck axis are from the remix STL.",
        ],
    },
    {
        "n": 1107,
        "file": "1107-side-spool-tube-route.svg",
        "title": "One PTFE from the CW2.5 to the side spool, seen from above",
        "fn": d1107_tube_route,
        "shows": [
            "The top of the frame from above, FRONT at the bottom: the tube holder in the top "
            "right extrusion's top slot about 22 cm behind the front, the bowden retainer on "
            "the top rear extrusion, and the exhaust cover's coupler at the back centre.",
            "One PTFE from the CW2.5 out through the coupler, through the retainer, forward to "
            "the holder and down to the spool outside the right side, cut square there. "
            "Callouts 1 to 3 are Step 11.72's Do numbers.",
        ],
        "insert": [
            ("11-skirts-panels-door.md", "Step 11.72", "first image: what the hands do"),
        ],
        "verify": [
            "The 'about 22 cm' is drawn to the holder's front end; the README says about 22 cm "
            "without naming the end. The holder clearing the box and the top-panel clips is "
            "'(verify on bench)' in the step, so the drawing labels its spot 'check on the "
            "bench'.",
            "The retainer's spot along the rear extrusion follows p.258 (beside the exhaust, "
            "toward the right side) but is not dimensioned; the tube's path and the toolhead "
            "position are schematic.",
        ],
    },
]
