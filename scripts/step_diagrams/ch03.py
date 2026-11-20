"""Chapter 03 (build plate) step diagrams, numbered 301 onwards.

Geometry sources: Voron manual p.53, p.54, p.58, p.59, p.60 (300 dpi renders of the
pinned PDF), the Voron 2.4r2 CAD index (250 size: plate holes 7 mm in from the edges,
M4 knurled nut DIN 466-B 8 mm tall with a 12 mm knurled base and an 8 mm collar on top,
roll-in M3 T-nut 1.4-5.7 mm below the slot face), and the chapter's own numbers
(355 x 355 x 10 mm plate, M3x20, 150 mm between the bed extrusions' centres, front
T-nuts 25 mm behind the front extrusion, plate front edge 38 mm behind the frame).
"""
import math

import draw_diagrams as dd
from draw_diagrams import (BLACKPART, BLACKPART_F, BLUE, BLUE_F, FAINT, GREY, GREY_F,
                           INK, MUTED, OK, ORANGE, PANEL, RED, RULE, STEEL, AMBER,
                           AMBER_F, T_LAB, T_MIN, callout, label_bg, legend_row,
                           step_header, step_note)

PLATE = STEEL          # aluminium plate, side and section
PLATE_F = GREY_F
MAG = BLACKPART        # magnetic pad
LINER_F = "#FFFFFF"


# ----------------------------------------------------------------- helpers ---
def _rot(cx, cy, pts, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c)
            for x, y in pts]


def _rect_pts(x, y, w, h):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


def _break_v(d: dd.Doc, x, y0, y1, amp=10):
    """A zig-zag break line: the part carries on past here."""
    n = 4
    pts = []
    for i in range(n + 1):
        yy = y0 + (y1 - y0) * i / n
        pts.append(f"{x + (amp if i % 2 else -amp):.1f} {yy:.1f}")
    d.path("M " + " L ".join(pts), stroke=MUTED, sw=2.5)


def _thumbnut(d: dd.Doc, cx, ybot, k, bore=True):
    """M4 knurled thumb nut in section, wide knurled base DOWN, collar UP (p.58, CAD)."""
    # (height from the base, radius) from the CAD mesh of DIN 466-B
    prof = [(0, 6.0), (3.0, 6.0), (3.0, 5.1), (4.0, 3.9), (5.0, 3.25), (6.0, 3.4),
            (6.5, 4.0), (8.0, 4.0)]
    right = [(cx + r * k, ybot - h * k) for h, r in prof]
    left = [(cx - r * k, ybot - h * k) for h, r in reversed(prof)]
    d.poly(right + left, fill=GREY_F, stroke=GREY, sw=3)
    for i in range(-5, 6):                                   # knurl on the base
        x = cx + i * 1.05 * k
        d.line(x, ybot - 0.3 * k, x, ybot - 2.7 * k, stroke=GREY, sw=1.6)
    if bore:
        d.rect(cx - 2.0 * k, ybot - 8 * k, 4.0 * k, 8 * k, fill=PANEL, stroke=GREY, sw=2)


def _shcs_v(d: dd.Doc, cx, ytop, k, length, col=GREY, fill=GREY_F, hidden_from=None):
    """M3 socket head cap screw, head up, head top at ytop. Shank dashed below
    `hidden_from` (a y) when it runs inside something drawn on top."""
    hr, hh, sr = 2.75, 3.0, 1.5
    d.rect(cx - hr * k, ytop, 2 * hr * k, hh * k, fill=fill, stroke=col, sw=2.5, rx=3)
    d.rect(cx - 1.25 * k, ytop, 2.5 * k, 1.6 * k, fill=INK, stroke="none", sw=0)  # socket
    y0, y1 = ytop + hh * k, ytop + (hh + length) * k
    if hidden_from is None:
        d.rect(cx - sr * k, y0, 2 * sr * k, y1 - y0, fill=fill, stroke=col, sw=2.5)
    else:
        d.rect(cx - sr * k, y0, 2 * sr * k, hidden_from - y0, fill=fill, stroke=col, sw=2.5)
        d.path(f"M {cx - sr * k:.1f} {hidden_from:.1f} L {cx - sr * k:.1f} {y1:.1f} "
               f"L {cx + sr * k:.1f} {y1:.1f} L {cx + sr * k:.1f} {hidden_from:.1f}",
               stroke=col, sw=2.5, dash="8 6")


def _tnut_section(d: dd.Doc, cx, face_y, k):
    """Roll-in M3 T-nut across the top slot: 7.7 wide, 1.4-5.7 mm below the face."""
    pts = [(-2.9, 1.4), (2.9, 1.4), (2.9, 1.8), (3.85, 1.8), (3.85, 4.2), (2.6, 5.7),
           (-2.6, 5.7), (-3.85, 4.2), (-3.85, 1.8), (-2.9, 1.8)]
    d.poly([(cx + x * k, face_y + y * k) for x, y in pts], fill=GREY, stroke=INK, sw=2)


def _arrow(d: dd.Doc, x0, y0, x1, y1, col=INK, sw=5, mk="arw"):
    d.path(f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}", stroke=col, sw=sw, marker=mk)


# ============================================================ diagram 301 ===
def d301_magnet_hinge() -> dd.Doc:
    d = dd.Doc(1130, "Laying the magnet with a tape hinge")
    top = step_header(d, "Lay the magnet with a hinge")
    ph, gap = 330, 12
    X0, X1 = 150, 1040                       # plate, front (left) to back (right)
    TH, LT, MT = 30, 10, 16                  # plate, liner, pad thickness (schematic)
    strip = 115                              # 40-50 mm of a 355 mm pad, in px

    def row(i, title):
        ry = top + 14 + i * (ph + gap)
        d.panel(30, ry, 1140, ph)
        d.text(54, ry + 50, title, size=34, weight=700)
        pt = ry + 236                        # plate top
        d.line(50, pt + TH, 1150, pt + TH, stroke=FAINT, sw=3)            # bench
        d.rect(X0, pt, X1 - X0, TH, fill=PLATE_F, stroke=GREY, sw=3)
        return ry, pt

    def tape(y_top):
        d.poly([(X1 - 60, y_top - 9), (X1 + 10, y_top - 9), (X1 + 10, pt + 20),
                (X1, pt + 20), (X1, y_top), (X1 - 60, y_top)], fill=AMBER, stroke=AMBER,
               sw=2)

    # (a) line it up, tape the back edge
    ry, pt = row(0, "Line it up, tape the back edge")
    d.text(54, ry + 92, "pad size: check on the bench", size=T_MIN, fill=MUTED)
    d.rect(X0, pt - LT, X1 - X0, LT, fill=LINER_F, stroke=MUTED, sw=3)
    d.rect(X0, pt - LT - MT, X1 - X0, MT, fill=MAG, stroke=INK, sw=2)
    tape(pt - LT - MT)
    d.text(X0 + 10, pt - 46, "pad, liner down", size=T_LAB, weight=700)
    d.text(X1 - 30, pt - 52, "flush at the back", size=T_LAB, anchor="end", weight=700)
    callout(d, X1 - 30 - 305 - 40, pt - 63, 1)
    d.text(X1 + 100, pt - 116, "tape hinge", size=T_LAB, anchor="end", weight=700,
           fill=AMBER)
    callout(d, X1 + 66, pt - 46, 2)
    d.text(X0, pt + TH + 42, "FRONT", size=T_MIN, weight=800, fill=MUTED)
    d.text(X1, pt + TH + 42, "BACK", size=T_MIN, anchor="end", weight=800, fill=MUTED)

    # (b) fold it back over the hinge, cut 40-50 mm of liner off
    ry, pt = row(1, "Fold it back, cut off a liner strip")
    hx, hy = X1, pt                                       # the hinge
    ang, L = 104, 205
    d.poly(_rot(hx, hy, _rect_pts(hx - L, hy - MT, L, MT), ang), fill=MAG, stroke=INK,
           sw=2)
    # liner on the pad's former underside, now facing the front; the strip is gone
    d.poly(_rot(hx, hy, _rect_pts(hx - L, hy, L - strip, LT), ang), fill=LINER_F,
           stroke=MUTED, sw=3)
    d.poly([(X1 - 10, pt - 10), (X1 + 10, pt - 10), (X1 + 10, pt + 20), (X1, pt + 20),
            (X1 - 10, pt)], fill=AMBER, stroke=AMBER, sw=2)
    c0 = _rot(hx, hy, [(hx - strip, hy - 6), (hx - strip, hy + LT + 22)], ang)
    d.line(*c0[0], *c0[1], stroke=INK, sw=3)                                  # the cut
    # the cut-off liner strip, falling away to the front
    mx, my = X1 - 190, pt - 80
    d.poly(_rot(mx, my, _rect_pts(mx - strip / 2, my - LT / 2, strip, LT), -40),
           fill=LINER_F, stroke=MUTED, sw=3)
    d.text(mx - 70, my - 12, "cut off:", size=T_LAB, anchor="end", weight=700)
    d.text(mx - 70, my + 28, "40 to 50 mm", size=T_LAB, anchor="end", weight=700)
    callout(d, mx - 330, my - 22, 3)
    ltop = _rot(hx, hy, [(hx - L + 40, hy + LT)], ang)[0]
    d.text(ltop[0] - 70, ltop[1] + 6, "liner", size=T_LAB, anchor="end", weight=700,
           fill=MUTED)
    d.leader(ltop[0] - 4, ltop[1], ltop[0] - 62, ltop[1] - 4, col=MUTED)

    # (c) press the strip, then pull the liner out to the front
    ry, pt = row(2, "Press the strip, pull the liner out")
    xs = X1 - strip                                       # where the bare strip ends
    d.rect(xs, pt - MT, X1 - xs, MT, fill=MAG, stroke=INK, sw=2)
    tape(pt - MT)
    # the rest of the pad, held up off the liner
    x2 = xs - 330
    d.path(f"M {xs:.1f} {pt - MT / 2:.1f} C {xs - 140:.1f} {pt - MT / 2:.1f} "
           f"{x2 + 60:.1f} {pt - 60:.1f} {x2 - 120:.1f} {pt - 150:.1f}", stroke=MAG,
           sw=MT, cap="butt")
    # the liner, lying loose on the plate, pulled out past the front edge
    d.rect(X0 - 50, pt - LT, xs - 24 - (X0 - 50), LT, fill=LINER_F, stroke=MUTED, sw=3)
    _arrow(d, X0 - 58, pt - LT / 2, X0 - 112, pt - LT / 2, col=INK, sw=5)
    d.text(X0, pt + TH + 42, "pull the liner out to the front", size=T_LAB, weight=700)
    # squeegee pressing where pad meets plate, moving to the front
    sq = [(xs - 14, pt - MT - 2), (xs + 14, pt - MT - 2), (xs + 58, pt - 110),
          (xs + 30, pt - 120)]
    d.poly(sq, fill=GREY_F, stroke=INK, sw=3)
    _arrow(d, xs + 70, pt - 150, xs - 60, pt - 150, col=INK, sw=5)
    d.text(xs + 84, pt - 140, "squeegee", size=T_LAB, weight=700)
    callout(d, xs - 100, pt - 150, 3)
    return d


# ============================================================ diagram 302 ===
def d302_trim_counterbore() -> dd.Doc:
    d = dd.Doc(900, "Cutting the magnet clear of a screw hole")
    top = step_header(d, "Cut the magnet clear of each hole")
    py, ph = top + 16, 900 - top - 32

    # left: from above
    d.panel(30, py, 560, ph)
    d.text(54, py + 50, "From above", size=34, weight=700)
    cx, cy, r = 300, py + 380, 105
    d.rect(60, py + 90, 500, 520, fill=MAG, stroke=INK, sw=2)
    d.circle(cx, cy, r + 6, fill="none", stroke="#6B7380", sw=10)        # the dimple
    # the cut, about two thirds of the way round: solid where cut, dashed ahead
    a0, a1 = math.radians(-200), math.radians(40)
    p0 = (cx + r * math.cos(a0), cy + r * math.sin(a0))
    p1 = (cx + r * math.cos(a1), cy + r * math.sin(a1))
    d.path(f"M {p0[0]:.1f} {p0[1]:.1f} A {r} {r} 0 1 1 {p1[0]:.1f} {p1[1]:.1f}",
           stroke="#FFFFFF", sw=5)
    d.path(f"M {p1[0]:.1f} {p1[1]:.1f} A {r} {r} 0 0 1 {p0[0]:.1f} {p0[1]:.1f}",
           stroke="#FFFFFF", sw=3, dash="10 10")
    # craft knife at the end of the cut
    kx, ky = p1
    blade = [(kx, ky), (kx + 22, ky - 70), (kx + 42, ky - 62)]
    d.poly(blade, fill=STEEL, stroke=INK, sw=2)
    hd = _rot(kx + 32, ky - 66, _rect_pts(kx + 18, ky - 196, 28, 130), 20)
    d.poly(hd, fill=ORANGE, stroke=INK, sw=2)
    callout(d, cx - 40, cy - r - 70, 1)
    callout(d, kx + 120, ky - 40, 2)
    y = legend_row(d, 60, py + 664, 1, ["press: find the dimple"], size=T_LAB, r=26)
    legend_row(d, 60, y + 22, 2, ["cut round its edge,", "in light passes"], size=T_LAB,
               r=26)

    # right: cut through the hole
    ox = 610
    d.panel(ox, py, 560, ph)
    d.text(ox + 24, py + 50, "Cut through", size=34, weight=700)
    k = 26.0
    hx = ox + 280
    ptop = py + 300                                  # plate top face
    cbr, cbd, hr, mt = 3.25, 3.0, 1.7, 1.5           # counterbore, hole, magnet (schem.)
    xL, xR = ox + 30, ox + 530
    # plate section, left and right of the hole
    for sgn in (-1, 1):
        xo = xL if sgn < 0 else xR
        pts = [(hx + sgn * cbr * k, ptop), (xo, ptop), (xo, ptop + 10 * k),
               (hx + sgn * hr * k, ptop + 10 * k), (hx + sgn * hr * k, ptop + cbd * k),
               (hx + sgn * cbr * k, ptop + cbd * k)]
        d.poly(pts, fill=PLATE_F, stroke=GREY, sw=3)
        # magnet on top, cut back to the counterbore edge
        m = [(hx + sgn * cbr * k, ptop - mt * k), (xo, ptop - mt * k), (xo, ptop),
             (hx + sgn * cbr * k, ptop)]
        d.poly(m, fill=MAG, stroke=INK, sw=2)
    # the screw: head in the counterbore, top flush with the plate face
    _shcs_v(d, hx, ptop, k, 7.5)
    # hex key down into the socket
    d.rect(hx - 1.25 * k, ptop - 150, 2.5 * k, 150 + 1.2 * k, fill=BLACKPART, stroke=INK,
           sw=2, rx=3)
    d.text(hx + 1.25 * k + 16, ptop - 112, "hex key", size=T_LAB, weight=700)
    d.text(xL + 6, ptop - mt * k - 18, "magnet", size=T_LAB, weight=700)
    d.text(xL + 6, ptop + 7 * k, "plate", size=T_LAB, weight=700, fill=MUTED)
    d.text(ox + 280, py + ph - 108, "head flush,", size=T_LAB, anchor="middle",
           weight=700, fill=OK)
    d.text(ox + 280, py + ph - 66, "under the magnet", size=T_LAB, anchor="middle",
           weight=700, fill=OK)
    callout(d, hx + cbr * k + 70, ptop + 1.5 * k, 3)
    d.leader(hx + cbr * k + 4, ptop + 2, hx + cbr * k + 42, ptop + 1.5 * k, col=INK)
    label_bg(d, hx + cbr * k + 70, ptop + 1.5 * k + 70, "no burr", size=T_LAB,
             bg=PLATE_F)
    return d


# ============================================================ diagram 303 ===
def _stack(d: dd.Doc, cx, ptop, k, xl, xr, labels=True):
    """Section across one bed extrusion at a plate screw: magnet, plate, M3x20,
    thumb nut, T-nut, extrusion. Returns y of the extrusion's top face."""
    cbr, cbd, hr, mt = 3.25, 3.0, 1.7, 1.5
    face = ptop + 18 * k                             # 10 plate + 8 thumb nut
    dd.profile2020(d, cx, face + 10 * k, k)
    _tnut_section(d, cx, face, k)
    _thumbnut(d, cx, face, k)
    for sgn in (-1, 1):
        xo = xl if sgn < 0 else xr
        d.poly([(hx_ := cx + sgn * cbr * k, ptop), (xo, ptop), (xo, ptop + 10 * k),
                (cx + sgn * hr * k, ptop + 10 * k), (cx + sgn * hr * k, ptop + cbd * k),
                (hx_, ptop + cbd * k)], fill=PLATE_F, stroke=GREY, sw=3)
        d.poly([(cx + sgn * cbr * k, ptop - mt * k), (xo, ptop - mt * k), (xo, ptop),
                (cx + sgn * cbr * k, ptop)], fill=MAG, stroke=INK, sw=2)
        _break_v(d, xo, ptop - mt * k - 6, ptop + 10 * k + 6, amp=7)
    _shcs_v(d, cx, ptop, k, 20)
    return face


def d303_plate_stack() -> dd.Doc:
    d = dd.Doc(1000, "One plate screw, cut through: what stacks on what")
    top = step_header(d, "What each screw goes through")
    k = 16.0
    cx = 360
    ptop = top + 110
    face = _stack(d, cx, ptop, k, 70, 650)
    lx = 730

    def lab(y, s, col="currentColor", ly=None, lx0=None):
        d.text(lx, y, s, size=T_LAB, weight=700, fill=col)
        if ly is not None:
            d.leader(lx0, ly, lx - 12, y - 10, col=INK)

    lab(ptop - 1.5 * k - 30, "magnet", ly=ptop - 0.75 * k, lx0=590)
    lab(ptop + 2 * k + 4, "M3×20 screw", ly=ptop + 1.5 * k, lx0=cx + 2.75 * k)
    lab(ptop + 7.5 * k, "plate, 10 mm", col=MUTED, ly=ptop + 7 * k, lx0=600)
    lab(face - 5 * k, "thumb nut:", ly=face - 7.2 * k, lx0=cx + 4 * k)
    d.text(lx, face - 5 * k + 40, "collar up,", size=T_LAB, weight=600)
    d.text(lx, face - 5 * k + 80, "knurled rim down", size=T_LAB, weight=600)
    lab(face + 4.5 * k + 30, "T-nut in the", ly=face + 3.5 * k, lx0=cx + 3.9 * k)
    d.text(lx, face + 4.5 * k + 70, "top slot", size=T_LAB, weight=700)
    d.text(lx, face + 17 * k, "bed extrusion", size=T_LAB, weight=700, fill=BLUE)
    step_note(d, "The screw passes through the thumb nut: it threads only the T-nut.",
              size=T_MIN)
    return d


# ============================================================ diagram 304 ===
def d304_gap_caliper() -> dd.Doc:
    d = dd.Doc(790, "Where the caliper goes to measure the gap")
    top = step_header(d, "Measure the gap at each screw")
    k = 13.0
    ptop = top + 230                                 # plate top
    pf = 560                                         # plate front edge
    hx = pf + 7 * k                                  # screw (front hole, 7 mm in)
    face = ptop + 18 * k                             # extrusion top
    eb = face + 11 * k                               # where the drawn extrusion stops
    # bed extrusion, side view, running on past the plate's front edge
    d.rect(60, face, 1160 - 60, eb - face, fill=BLUE_F, stroke="none", sw=0)
    d.line(60, face, 1160, face, stroke=BLUE, sw=3)
    d.line(64, face + 6.9 * k, 1156, face + 6.9 * k, stroke=BLUE, sw=1.6, op=0.55)
    d.path(f"M 60 {face:.1f} L 60 {eb:.1f}", stroke=BLUE, sw=3)
    for x0 in range(60, 1160, 80):                   # torn-off lower edge
        d.path(f"M {x0} {eb:.1f} L {x0 + 40} {eb - 10:.1f} L {x0 + 80} {eb:.1f}",
               stroke=BLUE, sw=2.5)
    d.text(1150, eb - 22, "bed extrusion", size=T_LAB, anchor="end", weight=700,
           fill=BLUE)
    # plate (with magnet), cut off at the right
    d.rect(pf, ptop - 1.5 * k, 1160 - pf, 1.5 * k, fill=MAG, stroke=INK, sw=2)
    d.rect(pf, ptop, 1160 - pf, 10 * k, fill=PLATE_F, stroke=GREY, sw=3)
    _break_v(d, 1160, ptop - 1.5 * k - 6, ptop + 10 * k + 6, amp=7)
    # thumb nut under the hole, screw hidden through it all
    d.rect(hx - 6 * k, face - 3 * k, 12 * k, 3 * k, fill=GREY_F, stroke=GREY, sw=3)
    d.poly([(hx - 5.1 * k, face - 3 * k), (hx - 3.25 * k, face - 5 * k),
            (hx - 4 * k, face - 6.5 * k), (hx - 4 * k, face - 8 * k),
            (hx + 4 * k, face - 8 * k), (hx + 4 * k, face - 6.5 * k),
            (hx + 3.25 * k, face - 5 * k), (hx + 5.1 * k, face - 3 * k)],
           fill=GREY_F, stroke=GREY, sw=3)
    for i in range(-5, 6):
        d.line(hx + i * 1.05 * k, face - 0.3 * k, hx + i * 1.05 * k, face - 2.7 * k,
               stroke=GREY, sw=1.6)
    d.path(f"M {hx - 1.5 * k:.1f} {ptop + 3 * k:.1f} L {hx - 1.5 * k:.1f} {face + 5 * k:.1f} "
           f"L {hx + 1.5 * k:.1f} {face + 5 * k:.1f} L {hx + 1.5 * k:.1f} {ptop + 3 * k:.1f}",
           stroke=GREY, sw=2.5, dash="8 6")
    # caliper, beam upright in front of the plate: inside jaws (short) point back into
    # the gap, outside jaws (long) point to the front
    gy0, gy1 = ptop + 10 * k, face                   # plate underside, extrusion top
    bx0, bx1 = pf - 130, pf - 76
    d.rect(bx0, top + 30, bx1 - bx0, gy1 - 40 - top - 30, fill=STEEL, stroke=INK, sw=2.5,
           rx=4)
    for i in range(12):                              # scale ticks
        y = top + 50 + i * 22
        d.line(bx1 - 14, y, bx1 - 2, y, stroke=INK, sw=1.6)
    jw = 14                                          # inside jaw thickness
    # sliding jaw: its inside jaw's top edge on the plate underside
    d.poly([(bx0 - 12, gy0 - 60), (bx1 + 12, gy0 - 60), (bx1 + 12, gy0),
            (pf - 3, gy0), (pf - 3, gy0 + jw), (bx1 + 12, gy0 + jw + 10),
            (bx0 - 12, gy0 + jw + 10), (bx0 - 12, gy0 + 4), (bx0 - 190, gy0 + 4),
            (bx0 - 190, gy0 - 8), (bx0 - 12, gy0 - 30)], fill=GREY_F, stroke=INK, sw=2.5)
    # fixed jaw: its inside jaw's bottom edge on the extrusion top
    d.poly([(bx0 - 12, gy1 - jw - 30), (bx1 + 12, gy1 - jw - 30), (bx1 + 12, gy1 - jw),
            (pf - 3, gy1 - jw), (pf - 3, gy1), (bx0 - 12, gy1), (bx0 - 12, gy1 - 8),
            (bx0 - 190, gy1 - 12), (bx0 - 190, gy1 - 24), (bx0 - 12, gy1 - jw - 30)],
           fill=GREY_F, stroke=INK, sw=2.5)
    # the gap, marked
    d.line(pf + 3, gy0 + 2, pf + 3, gy1 - 2, stroke=ORANGE, sw=6)
    callout(d, bx0 - 230, (gy0 + gy1) / 2, 1)
    d.text(bx0 - 24, top + 130, "caliper", size=T_LAB, anchor="end", weight=700)
    d.text(hx + 7 * k, face - 4 * k + 10, "gap: plate to extrusion", size=T_LAB,
           weight=700, fill=ORANGE)
    # eye level along the plate
    ex, ey = 1110, ptop - 110
    d.path(f"M {ex - 34} {ey} Q {ex} {ey - 26} {ex + 34} {ey} Q {ex} {ey + 26} {ex - 34} {ey} Z",
           fill=PANEL, stroke=INK, sw=3)
    d.circle(ex, ey, 10, fill=INK, stroke="none", sw=0)
    d.line(ex - 44, ey + 6, pf + 40, ptop - 1.5 * k - 6, stroke=MUTED, sw=2.5, dash="12 8")
    callout(d, ex - 70, ey - 54, 2)
    d.text(60, eb + 44, "FRONT", size=T_MIN, weight=800, fill=MUTED)
    d.text(1160, eb + 44, "all four gaps the same", size=T_LAB, anchor="end", weight=700)
    return d


# ============================================================ plan helpers ===
# Top view, FRONT at the bottom. Schematic: x 1.5 px/mm, y 1.4 px/mm.
SX, SY = 1.5, 1.4
PCX = 370                                            # printer centreline on the page


def _plan_frame(d: dd.Doc, yr):
    """Rear and front extrusion segments and the two bed extrusions (470 mm).
    yr = rear extrusion's inner face. Returns (yf, xl, xr) with xl/xr the bed
    extrusions' centres and yf the front extrusion's inner face."""
    yf = yr + 470 * SY
    xl, xr = PCX - 75 * SX, PCX + 75 * SX
    for y in (yr - 20 * SY, yf):
        d.rect(60, y, 620, 20 * SY, fill=BLUE_F, stroke=BLUE, sw=2.5)
    for x in (xl, xr):
        d.rect(x - 10 * SX, yr, 20 * SX, yf - yr, fill=BLUE_F, stroke=BLUE, sw=2.5)
        d.line(x, yr + 4, x, yf - 4, stroke=BLUE, sw=1.5, op=0.5)          # top slot
    return yf, xl, xr


def _plate_holes(yf, xl, xr):
    """Plate edge 38 mm behind the frame front = 18 mm behind the front extrusion's
    inner face; holes 7 mm in from the front and rear edges (CAD), over the bed
    extrusions. Returns plate rect and the four hole centres FL, FR, RL, RR."""
    pf = yf - 18 * SY
    pr = pf - 355 * SY
    hf, hr = pf - 7 * SY, pr + 7 * SY
    return (PCX - 177.5 * SX, pr, 355 * SX, 355 * SY), [(xl, hf), (xr, hf), (xl, hr),
                                                          (xr, hr)]


def _tnut_plan(d: dd.Doc, x, y, col=GREY, fill=GREY, w=13.0, h=12.5):
    d.rect(x - w / 2 * SX, y - h / 2 * SY, w * SX, h * SY, fill=fill, stroke=INK, sw=2, rx=3)


# ============================================================ diagram 305 ===
def d305_tnut_plan() -> dd.Doc:
    d = dd.Doc(980, "The eight T-nuts in the bed extrusions, from above")
    top = step_header(d, "Eight T-nuts, from above")
    yr = top + 60
    yf, xl, xr = _plan_frame(d, yr)
    (px, py, pw, ph), holes = _plate_holes(yf, xl, xr)
    d.rect(px, py, pw, ph, fill="none", stroke=MUTED, sw=2.5, dash="12 9")
    d.text(PCX, py + ph * 0.72, "plate goes", size=T_MIN, anchor="middle", fill=MUTED)
    d.text(PCX, py + ph * 0.72 + 36, "here", size=T_MIN, anchor="middle", fill=MUTED)
    for x, y in holes:                                # top-slot T-nuts under the holes
        d.rect(x - 14, y - 13, 28, 26, fill=GREY, stroke=INK, sw=2.5, rx=4)
    # inner side slots, rear half: M3 x2 right (probe), M5 x2 left (WAGO mount)
    m3 = [yr + 52 * SY, yr + 74 * SY]
    m5 = [yr + 150 * SY, yr + 205 * SY]
    for y in m3:
        d.rect(xr - 10 * SX - 9, y - 13, 16, 26, fill=GREY, stroke=INK, sw=2.5, rx=3)
    for y in m5:
        d.rect(xl + 10 * SX - 7, y - 13, 16, 26, fill=BLACKPART, stroke=INK, sw=2.5, rx=3)
    d.text(xr - 10 * SX - 20, (m3[0] + m3[1]) / 2 + 11, "M3 ×2", size=T_MIN,
           anchor="end", weight=700)
    d.text(xl + 10 * SX + 20, (m5[0] + m5[1]) / 2 + 11, "M5 ×2", size=T_MIN, weight=700)
    # half-way mark
    ym = (yr + yf) / 2
    d.line(xl + 10 * SX + 4, ym, xr - 10 * SX - 4, ym, stroke=MUTED, sw=2, dash="6 8")
    d.text(PCX, ym + 38, "half way", size=T_MIN, anchor="middle", fill=MUTED)
    # 25 mm: front T-nuts behind the front extrusion's inner face
    hf = holes[0][1]
    x = xl - 10 * SX - 16
    d.line(x, hf, x, yf, stroke=INK, sw=2.5)
    for yy in (hf, yf):
        d.line(x - 8, yy, x + 8, yy, stroke=INK, sw=2.5)
    d.text(x - 14, (hf + yf) / 2 + 11, "25 mm", size=T_MIN, anchor="end", weight=700)
    d.text(PCX, yf + 20 * SY + 46, "FRONT", size=T_LAB, anchor="middle", weight=800,
           fill=BLUE)
    callout(d, xr + 56, holes[1][1], 1)
    callout(d, xr + 56, holes[3][1], 1)
    callout(d, PCX, (m3[1] + m5[0]) / 2 + 8, 2)
    y = legend_row(d, 700, top + 150, 1, ["top slots: M3,", "two on each"])
    y = legend_row(d, 700, y + 40, 2, ["inner slots,", "rear half:", "M3 ×2 right,",
                                       "M5 ×2 left"])
    legend_row(d, 700, y + 40, 3, ["leave all", "eight loose"])
    return d


# ============================================================ diagram 306 ===
def d306_one_tight() -> dd.Doc:
    d = dd.Doc(980, "One screw tight, three slightly loose")
    top = step_header(d, "One screw tight, three loose")
    yr = top + 60
    yf, xl, xr = _plan_frame(d, yr)
    (px, py, pw, ph), holes = _plate_holes(yf, xl, xr)
    d.rect(px, py, pw, ph, fill=BLACKPART_F, stroke=GREY, sw=3, rx=2)
    for x in (xl, xr):                                # bed extrusions under the plate
        for sgn in (-1, 1):
            d.line(x + sgn * 10 * SX, py + 4, x + sgn * 10 * SX, py + ph - 4, stroke=BLUE,
                   sw=2, dash="10 8", op=0.7)
    fl = holes[0]
    # the plate grows away from the one fixed screw
    for x, y in holes[1:]:
        L = math.hypot(x - fl[0], y - fl[1])
        ux, uy = (x - fl[0]) / L, (y - fl[1]) / L
        _arrow(d, fl[0] + ux * 50, fl[1] + uy * 50, x - ux * 42, y - uy * 42, col=MUTED,
               sw=4, mk="arwm")
    for i, (x, y) in enumerate(holes):
        if i == 0:
            d.circle(x, y, 22, fill=OK, stroke=INK, sw=3)
            d.line(x - 9, y, x + 9, y, stroke="#FFFFFF", sw=4)
        else:
            d.circle(x, y, 22, fill=PANEL, stroke=GREY, sw=4, dash="7 5")
            d.text(x + 32, y + 11, "loose", size=T_MIN, weight=700, fill=MUTED)
    d.text(fl[0] - 32, fl[1] + 11, "tight", size=T_LAB, anchor="end", weight=800,
           fill=OK)
    d.text(700, top + 600, "arrows: the plate", size=T_MIN, weight=600, fill=MUTED)
    d.text(700, top + 640, "grows as it heats", size=T_MIN, weight=600, fill=MUTED)
    d.text(PCX, yf + 20 * SY + 46, "FRONT", size=T_LAB, anchor="middle", weight=800,
           fill=BLUE)
    callout(d, fl[0] - 72, fl[1] - 52, 1)
    callout(d, holes[3][0] + 166, holes[3][1], 2)
    y = legend_row(d, 700, top + 150, 1, ["front-left:", "tighten fully"])
    y = legend_row(d, 700, y + 40, 2, ["the other three:", "slightly loose"])
    legend_row(d, 700, y + 40, 3, ["snug by feel,", "no torque driver"])
    return d


# ================================================================ registry ===
_COMMON_SCHEMATIC = ("Thicknesses of the magnet, liner and tape, and the counterbore's "
                     "size, are schematic.")

DIAGRAMS = [
    {
        "n": 301,
        "file": "301-magnet-hinge.svg",
        "title": "Lay the magnet with a hinge",
        "fn": d301_magnet_hinge,
        "shows": [
            "Three side views, FRONT left, BACK right. (a) The pad, liner down, flush at "
            "the plate's back edge, a strip of masking tape over that edge as the hinge "
            "(Do 1, 2). (b) The pad folded back over the hinge, its liner now facing the "
            "front, a 40 to 50 mm strip of liner cut off at the hinge end (Do 3). (c) "
            "The bare strip pressed down at the back, the rest of the pad held up, the "
            "liner pulled out to the front with the squeegee following (Do 3).",
        ],
        "insert": [("03-build-plate.md", "Step 03.9", "the hinge method")],
        "verify": [
            "The pad's size is not known before kit day (Do 1 says verify on bench): the "
            "drawing shows it flush at the back and carries a 'check on the bench' label.",
            "The fold-back geometry follows the step's own words; the linked lamination "
            "video was not watched. " + _COMMON_SCHEMATIC,
        ],
    },
    {
        "n": 302,
        "file": "302-trim-counterbore.svg",
        "title": "Cut the magnet clear of each hole",
        "fn": d302_trim_counterbore,
        "shows": [
            "Left, from above: the magnet with the counterbore showing through as a "
            "dimple and a craft knife two thirds of the way round its edge (Do 1, 2). "
            "Right, cut through one hole: the magnet cut back to the counterbore's edge, "
            "the M3 head sitting flush with the plate face below the magnet, a hex key "
            "in its socket, and no burr at the rim (Do 3).",
        ],
        "insert": [("03-build-plate.md", "Step 03.10", "the cut and the flush head")],
        "verify": [
            "Head flush with the plate face follows p.53 ('flush/below the surface') and "
            "the 250 CAD (head top level with the plate top). The counterbore's diameter "
            "and depth on LDO's 10 mm plate are not published. " + _COMMON_SCHEMATIC,
        ],
    },
    {
        "n": 303,
        "file": "303-plate-stack.svg",
        "title": "What each screw goes through",
        "fn": d303_plate_stack,
        "shows": [
            "Section across one bed extrusion at a plate screw, to scale from the CAD: "
            "magnet, the 10 mm plate with the M3×20 head flush in its counterbore, the "
            "M4 thumb nut standing knurled rim down and collar up (p.58), and the roll-in "
            "M3 T-nut in the extrusion's top slot, which is the only part the screw "
            "threads into. No callouts: it serves two steps with different Do lists.",
        ],
        "insert": [
            ("03-build-plate.md", "Step 03.13", "the thumb nut's way up"),
            ("03-build-plate.md", "Step 03.15", "the screw's path"),
        ],
        "verify": [
            "Thumb-nut shape and 8 mm height are the CAD's DIN 466-B; the kit's M4 "
            "knurled nut may differ in height (LDO says its spacers are thicker). The "
            "screw tip's depth in the T-nut follows from those numbers. " +
            _COMMON_SCHEMATIC,
        ],
    },
    {
        "n": 304,
        "file": "304-gap-caliper.svg",
        "title": "Measure the gap at each screw",
        "fn": d304_gap_caliper,
        "shows": [
            "Side view at a front screw, FRONT left: the caliper's inside jaws in the gap "
            "between the bed extrusion's top and the plate's underside, beam upright just "
            "in front of the plate's edge (Do 1), and the eye sighting along the plate "
            "(Do 2).",
        ],
        "insert": [("03-build-plate.md", "Step 03.18", "where the caliper goes")],
        "verify": [
            "The caliper is drawn schematically; the jaws sit beside the thumb nut, not "
            "through it. Hole 7 mm in from the plate edge is the 250 CAD's.",
        ],
    },
    {
        "n": 305,
        "file": "305-tnut-plan.svg",
        "title": "Eight T-nuts, from above",
        "fn": d305_tnut_plan,
        "shows": [
            "Top view, FRONT at the bottom: the two bed extrusions with four M3 T-nuts in "
            "their top slots under the plate's holes (the front pair 25 mm behind the "
            "front extrusion, p.58), and in the rear half of the inner side slots two M3 "
            "on the right extrusion and two M5 on the left. Callouts 1 to 3 are the Do "
            "numbers of Step 03.12.",
        ],
        "insert": [("03-build-plate.md", "Step 03.12", "where all eight go")],
        "verify": [
            "Scale is about 1.5 px per mm across and 1.4 front to back. The side-slot "
            "T-nuts' exact place along the rear half is set in Ch 09 and is schematic "
            "here; the rear holes 7 mm in from the plate's rear edge are the 250 CAD's.",
        ],
    },
    {
        "n": 306,
        "file": "306-one-screw-tight.svg",
        "title": "One screw tight, three loose",
        "fn": d306_one_tight,
        "shows": [
            "Top view, FRONT at the bottom: the plate on its two bed extrusions with the "
            "front-left screw tight and the other three loose, and arrows showing the "
            "plate growing away from the fixed screw as it heats. Callouts 1 to 3 are "
            "the Do numbers of Step 03.17.",
        ],
        "insert": [("03-build-plate.md", "Step 03.17", "which screw is tight")],
        "verify": [],
    },
]
