"""Chapter 04 (A/B drive units and front idlers) step diagrams, numbered 401 onwards.

Geometry sources (all in the repo or the local CAD cache):
- STLs under slicer/stl/voron2/STLs (pinned Voron-2 de7e89d), sliced with numpy:
  a/b_drive_frame_upper: motor centre on the 31 mm M3 square (3 of 4 holes, Ø3.5),
  M5 post holes Ø5.4 at 16.9 mm (near) and 33.9 mm (far) from the motor centre,
  37.0 mm apart, both 15.5 mm off the motor centre on the same side; outlines below are
  the flat face's outline (z 0.5 mm), simplified to 0.25 mm and centred on the motor.
  pulley_jig: 3.2 mm plate; long bottom edge at y 3, two feet y 0-3 (x ±3..±9) around a
  6 mm slot; B tab x -23.5..-18, y 9.6..16.4; A tab x 18..23.5, y 19.6..26.4; N tab
  x -7.2..-0.4 to y 32.15. Standing on the long edge: A tab 16.6-23.4 mm, B tab
  6.6-13.4 mm above the motor face; on the feet, 3 mm higher.
  [a]_tensioner_right: one hole straight through, Ø3.5 for 13 mm then Ø4.7 for 5 mm.
- Voron 2.4r2 CAD (~/.cache/voron-cad index + meshes): A motor centre (273, 347), posts
  at y 362.5, near x 266.2 (upper pair only), far x 303.2 (both pairs); B mirrored
  (near x -12.2 lower pair, far x -49.2). A belt z 80-86, B belt z 70-76. Motor face
  z 63; A pulley teeth 79.5-86.5 (hub below), B teeth 69.45-76.45 (hub above). The A belt
  runs over the near stack, teeth round the pulley's front, over the far stack. The
  M3x40 tensioner enters the arm at the front through the 3.5 mm bore; the insert sits
  at the arm's rear end. GT2 pulley hub: two set screws 90 degrees apart.
- Voron manual p.73-80 (250 dpi renders of the pinned PDF) for the views and the jig's
  use; p.76/p.80 side views are seen from behind the drive.
"""
import math

import draw_diagrams as dd
from draw_diagrams import (AMBER, AMBER_F, BELT_A, BELT_B, BLACKPART, BLACKPART_F, BROWN,
                           FAINT, GREY, GREY_F, INK, MUTED, OK, ORANGE, ORANGE_F, PANEL,
                           RED, STEEL, T_LAB, T_MIN, callout, label_bg, step_header,
                           step_note)

# ------------------------------------------------------------------ geometry ---
# Flat-face outlines of the upper drive frames in STL (x, y) mm, motor centre at 0, 0.
A_OUTER = [(-20.1, 56.0), (-21.8, 54.5), (-22.5, 52.0), (-22.5, -30.2), (-21.9, -33.1),
           (-19.9, -35.6), (-16.7, -37.1), (2.0, -37.2), (4.2, -37.9), (5.0, -38.9),
           (5.5, -40.3), (5.5, -56.4), (6.0, -57.5), (7.0, -58.3), (31.0, -58.3),
           (32.0, -57.5), (32.5, -56.4), (32.5, -41.4), (29.1, -37.0), (27.1, -33.3),
           (25.6, -28.6), (25.2, -23.2), (22.2, -18.2), (20.7, -13.0), (20.5, 16.3),
           (20.1, 19.0), (19.2, 21.0), (17.7, 22.4), (16.0, 22.9), (8.7, 23.1), (7.0, 24.2),
           (6.3, 26.0), (6.3, 34.5), (6.8, 36.4), (7.8, 37.4), (9.1, 38.0), (16.6, 38.2),
           (16.7, 43.7), (16.2, 44.0), (-1.1, 44.2), (-1.5, 44.9), (-1.5, 54.4),
           (-2.1, 55.6), (-3.3, 56.4), (-18.0, 56.5)]
A_BORE = [(11.1, -4.5), (11.8, -2.1), (12.0, 0.7), (11.6, 3.1), (10.7, 5.5), (9.4, 7.5),
          (7.4, 9.5), (5.3, 10.8), (3.0, 11.7), (0.0, 12.0), (-2.2, 11.8), (-4.6, 11.1),
          (-6.8, 9.9), (-9.0, 7.9), (-9.9, 4.6), (-11.9, 1.1), (-11.5, -3.4), (-9.8, -6.9),
          (-6.6, -10.0), (-2.9, -11.6), (1.5, -11.9), (5.5, -10.6), (9.1, -7.9)]
B_OUTER = [(-19.8, -56.1), (-21.8, -54.5), (-22.5, -52.0), (-22.5, 30.2), (-21.9, 33.0),
           (-19.9, 35.6), (-16.7, 37.1), (2.0, 37.2), (4.2, 37.9), (5.0, 38.8), (5.5, 40.2),
           (5.5, 56.3), (6.0, 57.5), (7.0, 58.3), (31.1, 58.3), (32.0, 57.5), (32.5, 56.3),
           (32.5, 41.6), (32.0, 40.5), (29.2, 36.9), (27.1, 33.2), (25.6, 28.5),
           (25.2, 23.2), (22.4, 18.6), (20.9, 13.9), (20.5, 10.0), (20.5, -17.0),
           (19.6, -20.3), (17.7, -23.1), (-0.7, -41.7), (-1.5, -44.1), (-1.5, -54.4),
           (-2.2, -55.8), (-4.0, -56.5), (-18.0, -56.5)]
B_BORE = [(10.8, 5.1), (11.9, 1.3), (11.6, -3.1), (9.8, -7.0), (6.6, -10.1), (3.0, -11.7),
          (-1.5, -12.0), (-6.0, -10.5), (-9.0, -7.9), (-10.1, -4.2), (-11.9, -1.4),
          (-11.9, 1.6), (-11.3, 4.1), (-10.2, 6.3), (-8.8, 8.1), (-6.6, 10.0), (-4.3, 11.1),
          (-1.9, 11.8), (0.8, 11.9), (3.2, 11.5), (5.6, 10.6), (7.6, 9.2), (9.5, 7.3)]
# Post centres, same frame: (x, y) of the near and far M5 holes.
A_POSTS = {"near": (-15.5, 6.8), "far": (-15.5, -30.2)}
B_POSTS = {"near": (-15.5, -6.8), "far": (-15.5, 30.2)}

BEAR_R, FLANGE_R = 6.5, 7.5          # F695: 13 mm OD, 15 mm flange
NEMA = 42.3                          # motor body, square
BOSS_R, BOSS_H = 11.0, 2.0           # motor centring boss (nominal NEMA 17)
SHAFT_R, SHAFT_TOP = 2.5, 24.85      # shaft above the motor face (CAD)


def _pts_path(pts):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"


def _bench_view(pts, ox, oy, k):
    """STL (x, y) seen from above with the flat face down, long axis across the page:
    page u = -y, page up = x (a rotation, not a mirror)."""
    return [(ox - k * y, oy - k * x) for x, y in pts]


def _from_behind(pts, ox, oy, k):
    """The same frame turned the right way up and seen from above with its posts toward
    the bottom of the page (the view that matches p.76/p.80 from behind): u = y, up = x.
    Turning the part over makes this the mirror of _bench_view."""
    return [(ox + k * y, oy - k * x) for x, y in pts]


def _stack_top(d, x, y, k, sw=3):
    """A bearing stack from above: flange ring, bearing, screw end."""
    d.circle(x, y, FLANGE_R * k, fill=GREY_F, stroke=GREY, sw=sw)
    d.circle(x, y, BEAR_R * k, fill=STEEL, stroke=GREY, sw=2)
    d.circle(x, y, 2.5 * k, fill=GREY, stroke=INK, sw=2)


def _arrow(d, x0, y0, x1, y1, col=INK, sw=5, mk="arw"):
    d.path(f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}", stroke=col, sw=sw, marker=mk)


def _cross(d, x, y, r, col=RED, sw=8):
    d.line(x - r, y - r, x + r, y + r, stroke=col, sw=sw)
    d.line(x - r, y + r, x + r, y - r, stroke=col, sw=sw)


# ============================================================= diagram 401 ===
def d401_post_positions() -> dd.Doc:
    d = dd.Doc(725, "Near post and far post on the A and B drive frames")
    top = step_header(d, "Near post, far post")
    k = 4.4
    py, ph = top + 18, 545

    def panel(px, name, outer, bore, posts, colour):
        d.panel(px, py, 555, ph)
        d.text(px + 24, py + 54, f"{name} drive", size=40, weight=700, fill=colour)
        ox, oy = px + 22 + 59 * k, py + 262          # motor centre on the page
        d.path(_pts_path(_bench_view(outer, ox, oy, k)), fill=BLACKPART_F, stroke=BLACKPART,
               sw=3)
        d.path(_pts_path(_bench_view(bore, ox, oy, k)), fill=PANEL, stroke=BLACKPART, sw=3)
        d.line(ox - 12, oy, ox + 12, oy, stroke=INK, sw=2.5)
        d.line(ox, oy - 12, ox, oy + 12, stroke=INK, sw=2.5)
        (nx, ny), = _bench_view([posts["near"]], ox, oy, k)
        (fx, fy), = _bench_view([posts["far"]], ox, oy, k)
        for (x, y) in ((nx, ny), (fx, fy)):
            d.line(ox, oy, x, y, stroke=MUTED, sw=2.5, dash="8 6")
        _stack_top(d, nx, ny, k)
        _stack_top(d, fx, fy, k, sw=5)
        # motor bore label, above the frame
        d.text(ox, py + 102, "motor bore", size=T_MIN, anchor="middle", weight=600,
               fill=MUTED)
        d.leader(ox, oy - 12.2 * k, ox, py + 112, col=MUTED)
        # post labels under the frame, each on the side its post is on
        ly = py + 430
        for (x, y, lines, anchor, lx) in (
                (nx, ny, ("near post", "2 bearings", "about 17 mm"),
                 "start" if nx < fx else "end", px + 30 if nx < fx else px + 525),
                (fx, fy, ("far post", "4 bearings", "about 34 mm"),
                 "end" if nx < fx else "start", px + 525 if nx < fx else px + 30)):
            d.leader(x, y + FLANGE_R * k, x, ly - 40, col=INK)
            d.line(x, ly - 40, lx + (60 if anchor == "start" else -60), ly - 40,
                   stroke=INK, sw=1.3)
            d.text(lx, ly, lines[0], size=T_LAB + 2, anchor=anchor, weight=700)
            d.text(lx, ly + 42, lines[1], size=T_LAB + 2, anchor=anchor, weight=700,
                   fill=colour)
            d.text(lx, ly + 82, lines[2], size=T_MIN, anchor=anchor, weight=600,
                   fill=MUTED)

    panel(30, "A", A_OUTER, A_BORE, A_POSTS, BELT_A)
    panel(615, "B", B_OUTER, B_BORE, B_POSTS, BELT_B)
    step_note(d, "Upper frame flat face down. Measure from the bore's centre.", size=T_MIN)
    return d


# ============================================================= diagram 402 ===
# The jig in its own mm frame (x right, y up), traced from pulley_jig.stl.
_JIG = [(-9, 0), (-3, 0), (-3, 4), "slot", (3, 4), (3, 0), (9, 0), (9, 3), (18, 3),
        (18, 19.6), (23.5, 19.6), (23.5, 26.4), (-0.4, 26.4), (-0.4, 32.15),
        (-7.2, 32.15), (-7.2, 25.4), (-18, 25.4), (-18, 16.4), (-23.5, 16.4),
        (-23.5, 9.6), (-18, 9.6), (-18, 3), (-9, 3)]
_JIG_LETTERS = {"N": (-3.8, 28.6), "A": (20.75, 22.9), "B": (-20.75, 12.9),
                "E": (13.5, 6.2)}
_TAB = {"A": (18, 23.5, 19.6, 26.4), "B": (-23.5, -18, 9.6, 16.4)}


def _jig(d, P, k, hi=None, sw=3):
    """Draw the jig through the mapping P(x, y) -> page; hi = the tab to highlight."""
    out = []
    for p in _JIG:
        if p == "slot":                         # semicircle over the 6 mm slot
            for a in range(180, -1, -15):
                t = math.radians(a)
                out.append(P(3 * math.cos(t), 4 + 3 * math.sin(t)))
            continue
        out.append(P(*p))
    d.path(_pts_path(out), fill=BLACKPART_F, stroke=BLACKPART, sw=sw)
    if hi:
        x0, x1, y0, y1 = _TAB[hi]
        q = [P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1)]
        d.path(_pts_path(q), fill=ORANGE_F, stroke=BLACKPART, sw=sw)
    for ch, (x, y) in _JIG_LETTERS.items():
        X, Y = P(x, y)
        d.text(X, Y + 12, ch, size=34 if k >= 5 else 30, anchor="middle", weight=800,
               fill=BLACKPART)


def _pulley_side(d, S, k, hub_down, teeth_bottom):
    """GT2 20T 6 mm pulley in side view on the shaft. S(s, h) -> page. Heights in mm
    above the motor face; teeth_bottom = the top of the lower flange."""
    def box(s0, s1, h0, h1, fill, stroke, sw=2.5):
        (x0, y0), (x1, y1) = S(s0, h1), S(s1, h0)
        d.rect(x0, y0, x1 - x0, y1 - y0, fill=fill, stroke=stroke, sw=sw, rx=2)
    tb = teeth_bottom
    if hub_down:
        box(-8, 8, tb - 7.85, tb - 1, GREY_F, GREY)           # hub
        box(-7.6, 7.6, tb - 1, tb, STEEL, GREY)                # lower flange
        box(-5.8, 5.8, tb, tb + 7, GREY_F, GREY)               # teeth
        box(-7.6, 7.6, tb + 7, tb + 8.15, STEEL, GREY)         # upper flange
    else:
        box(-7.6, 7.6, tb - 1.15, tb, STEEL, GREY)
        box(-5.8, 5.8, tb, tb + 7, GREY_F, GREY)
        box(-7.6, 7.6, tb + 7, tb + 8, STEEL, GREY)
        box(-8, 8, tb + 8, tb + 15.85, GREY_F, GREY)
    for s in (-4.2, -1.4, 1.4, 4.2):                           # tooth lines
        (x, y0), (_, y1) = S(s, tb + 0.6), S(s, tb + 6.4)
        d.line(x, y0, x, y1, stroke=GREY, sw=2)
    # set screw on the hub
    hc = tb - 4.4 if hub_down else tb + 11.9
    X, Y = S(0, hc)
    d.circle(X, Y, 1.6 * k, fill=PANEL, stroke=GREY, sw=2)


def _motor_top(d, S, k, depth=14):
    (x0, y0), (x1, y1) = S(-NEMA / 2, 0), S(NEMA / 2, -depth)
    d.rect(x0, y0, x1 - x0, y1 - y0, fill=GREY_F, stroke=GREY, sw=3)
    d.line(x0, y1, x1, y1, stroke=PANEL, sw=5)
    d.line(x0, y1, x1, y1, stroke=GREY, sw=2, dash="10 8")
    (x0, y0), (x1, y1) = S(-BOSS_R, BOSS_H), S(BOSS_R, 0)
    d.rect(x0, y0, x1 - x0, y1 - y0, fill=STEEL, stroke=GREY, sw=2)
    (x0, y0), (x1, y1) = S(-SHAFT_R, SHAFT_TOP), S(SHAFT_R, BOSS_H)
    d.rect(x0, y0, x1 - x0, y1 - y0, fill=STEEL, stroke=GREY, sw=2)


JIG_SHIFT = 29.7       # shaft to the jig's centre line with the tab tip in the groove


def d402_pulley_jig() -> dd.Doc:
    d = dd.Doc(932, "Setting the A and B pulley heights with the pulley jig")
    top = step_header(d, "Pulley height with the jig")
    k = 5.8
    py, ph = top + 18, 430

    def main(px, side, height, hub_down, colour):
        """side -1: A, jig left of the pulley; +1: B, jig right of it (p.75, p.79)."""
        d.panel(px, py, 555, ph)
        d.text(px + 24, py + 54, f"{'A' if side < 0 else 'B'}: {height} mm", size=40,
               weight=700, fill=colour)
        sx = px + (324 if side < 0 else 231)            # the shaft on the page
        face = py + 320                                 # the motor face on the page

        def S(s, h):
            return sx + s * k, face - h * k

        def P(x, y):                                    # jig standing on its long edge
            return S(x + side * JIG_SHIFT, y - 3)
        _motor_top(d, S, k)
        _pulley_side(d, S, k, hub_down, height)
        _jig(d, P, k, hi="A" if side < 0 else "B")
        # level line: the tab's underside on the top of the lower flange
        y = S(0, height)[1]
        xa, xb = (S(-26, 0)[0], S(7, 0)[0]) if side < 0 else (S(-7, 0)[0], S(26, 0)[0])
        d.line(xa, y, xb, y, stroke=OK, sw=4, dash="12 7")
        callout(d, S(side * 20, 0)[0], y, 3)
        # dimension: motor face to the teeth underside
        dx = S(-side * 13.5, 0)[0]
        d.line(dx, face, dx, y, stroke=INK, sw=2.5)
        for yy in (face, y):
            d.line(dx - 10, yy, dx + 10, yy, stroke=INK, sw=2.5)
        d.text(dx - side * 14, (face + y) / 2 + 12, f"{height} mm", size=T_LAB,
               anchor="start" if side < 0 else "end", weight=700)
        # 1: which way round the pulley goes; 2: the jig beside it
        c1x, c1y = S(0, 31)
        callout(d, c1x, c1y, 1)
        d.text(c1x - side * 38, c1y + 11, "hub down" if hub_down else "hub up",
               size=T_LAB, anchor="start" if side < 0 else "end", weight=700)
        c2 = P(-5, 12) if side < 0 else P(5, 18)
        callout(d, c2[0], c2[1], 2)

    main(30, -1, 16.5, True, BELT_A)
    main(615, 1, 6.5, False, BELT_B)

    # ---- the two wrong ways, small
    wy = py + ph + 16
    wh = d.h - wy - 16
    k2 = 5.0
    d.panel(30, wy, 555, wh)
    d.text(54, wy + 50, "Wrong: on its feet", size=T_LAB + 2, weight=700, fill=RED)
    base = wy + wh - 50

    def P1(x, y):
        return 230 + x * k2, base - y * k2
    d.line(90, base, 380, base, stroke=GREY, sw=5)
    _jig(d, P1, k2, sw=2.5)
    (x0, y0), (x1, y1) = P1(10, 3), P1(17.5, 0)
    d.rect(x0, y0, x1 - x0, y1 - y0, fill="#F6D5D1", stroke=RED, sw=2.5)
    d.leader(x1 - 4, (y0 + y1) / 2, 384, base - 40, col=RED)
    d.text(390, base - 60, "every height", size=T_MIN, weight=700, fill=RED)
    d.text(390, base - 22, "3 mm high", size=T_MIN, weight=700, fill=RED)

    d.panel(615, wy, 555, wh)
    d.text(639, wy + 50, "Wrong: the tab's top", size=T_LAB + 2, weight=700, fill=RED)
    face2 = wy + wh - 40
    sx2 = 615 + 330

    def S2(s, h):
        return sx2 + s * k2, face2 - h * k2

    def P2(x, y):                                       # the jig held a little off
        return S2(x - JIG_SHIFT - 2.2, y - 3)
    _motor_top(d, S2, k2, depth=6)
    _jig(d, P2, k2, hi="A", sw=2.5)
    _pulley_side(d, S2, k2, True, 23.4)
    y = S2(0, 23.4)[1]
    d.line(S2(-30, 0)[0], y, S2(6, 0)[0], y, stroke=RED, sw=4, dash="12 7")
    d.text(1150, wy + 112, "A: about 23 mm", size=T_MIN, anchor="end", weight=700,
           fill=RED)
    d.text(1150, wy + 152, "B: about 13 mm", size=T_MIN, anchor="end", weight=700,
           fill=RED)
    return d


# ============================================================= diagram 403 ===
# CAD, machine mm. Heights are z; the motor face is z 63.
_FACE = 63.0
_SPACER, _BEAR = 1.0, 4.0


def _stack_side(d, S, u, z0, pairs, k):
    """Bearing stack in side view from z0 upward: per pair spacer, flange-down bearing,
    flange-up bearing, spacer (p.65, p.74)."""
    z = z0
    for _ in range(pairs):
        for kind in ("s", "bd", "bu", "s"):
            h = _SPACER if kind == "s" else _BEAR
            if kind == "s":
                (x0, y0), (x1, y1) = S(u - 5, z + h), S(u + 5, z)
                d.rect(x0, y0, x1 - x0, y1 - y0, fill=AMBER_F, stroke=BROWN, sw=1.5)
            else:
                (x0, y0), (x1, y1) = S(u - BEAR_R, z + h), S(u + BEAR_R, z)
                d.rect(x0, y0, x1 - x0, y1 - y0, fill=STEEL, stroke=GREY, sw=2)
                fz = z if kind == "bd" else z + h - 1
                (x0, y0), (x1, y1) = S(u - FLANGE_R, fz + 1), S(u + FLANGE_R, fz)
                d.rect(x0, y0, x1 - x0, y1 - y0, fill=GREY, stroke=GREY, sw=1)
            z += h


def d403_belt_level() -> dd.Doc:
    dy, dy2 = 70, 110                             # room for the two views' labels
    d = dd.Doc(960 + dy2, "The belt run through each drive, from above and from behind")
    top = step_header(d, "Belt through the drive")
    k = 4.5
    py, ph = top + 18, 830 + dy2
    R = 7.2 * k                                   # belt centre line round a stack
    RP = 7.0 * k                                  # and round the pulley teeth

    def column(px, name, outer, bore, posts, colour, upper, marker):
        d.panel(px, py, 555, ph)
        d.text(px + 24, py + 54, f"{name}: {'upper' if upper else 'lower'} level",
               size=40, weight=700, fill=colour)
        # which way the top view is seen (the posts mirror diagram 401's, which shows
        # the frame upside down on the bench)
        d.text(px + 24, py + 96, "from above, right way up,", size=T_MIN, weight=600,
               fill=MUTED)
        d.text(px + 24, py + 132, "standing behind the printer", size=T_MIN, weight=600,
               fill=MUTED)
        ulo, uhi = min(p[1] for p in outer), max(p[1] for p in outer)
        ox, oy = px + 277.5 - (ulo + uhi) / 2 * k, py + 262 + dy
        mirror = name == "B"
        # ---- from above, X-ray: frame outline dashed, stacks, pulley, belt
        d.path(_pts_path(_from_behind(outer, ox, oy, k)), fill="none", stroke=BLACKPART,
               sw=2.5, dash="10 7")
        (nx, ny), = _from_behind([posts["near"]], ox, oy, k)
        (fx, fy), = _from_behind([posts["far"]], ox, oy, k)
        d.circle(ox, oy, 7.6 * k, fill=GREY_F, stroke=GREY, sw=3)
        d.circle(ox, oy, 5.8 * k, fill=PANEL, stroke=GREY, sw=2, dash="4 4")
        d.circle(ox, oy, SHAFT_R * k, fill=STEEL, stroke=GREY, sw=2)
        _stack_top(d, nx, ny, k)
        _stack_top(d, fx, fy, k)
        sgn = 1 if mirror else -1                   # A: clockwise round the stacks
        start = (px + 545, ny + R) if not mirror else (px + 10, ny + R)
        end = (fx + sgn * R, oy - 30 * k)
        nodes = [(start[0], start[1], 0, 0), (nx, ny, R, sgn), (ox, oy, RP, -sgn),
                 (fx, fy, R, sgn), (end[0], end[1], 0, 0)]
        belt = dd.belt_geometry(nodes)
        d.path(dd.prims_to_path(belt), stroke=colour, sw=7)
        d.path(f"M {end[0]:.1f} {end[1] + 40:.1f} L {end[0]:.1f} {end[1]:.1f}",
               stroke=colour, sw=7, marker=marker)
        callout(d, ox + (-1 if not mirror else 1) * 0, oy - RP - 34, 2)
        lab_y = oy + 23 * k + 50
        d.text(nx, lab_y, "near", size=T_LAB, anchor="middle", weight=700)
        d.text(fx, lab_y, "far", size=T_LAB, anchor="middle", weight=700)
        px_lab = ox + (-1 if mirror else 1) * (9.5 * k)
        d.text(px_lab, oy + 12, "pulley", size=T_MIN, weight=600,
               anchor="end" if mirror else "start", fill=MUTED)

        # ---- from behind, as p.76 / p.80 draw it, larger
        ks = 7.0
        face = py + 732 + dy2
        u_n, u_f = posts["near"][1], posts["far"][1]
        uc = (u_n + u_f) / 2

        def S(u, z):
            return px + 277.5 + (u - uc) * ks, face - (z - _FACE) * ks
        # the side view's own heading, under a rule that closes the top view
        d.line(px + 20, py + 510, px + 535, py + 510, stroke=FAINT, sw=2)
        callout(d, px + 48, py + 548, 1)
        d.text(px + 84, py + 560, f"from behind, as p.{76 if upper else 80}",
               size=T_MIN, weight=700, fill=MUTED)
        # motor below the lower frame, cut off
        (x0, y0), (x1, y1) = S(-NEMA / 2, _FACE), S(NEMA / 2, _FACE - 6)
        d.rect(x0, y0, x1 - x0, y1 - y0, fill=GREY_F, stroke=GREY, sw=2.5)
        d.line(x0, y1, x1, y1, stroke=PANEL, sw=5)
        d.line(x0, y1, x1, y1, stroke=GREY, sw=2, dash="10 8")
        # the two frame plates, schematic, cut off past the stacks
        ua, ub = sorted((u_f, u_n))
        for z0, z1 in ((_FACE, 67.0), (89.0, 94.0)):
            (x0, y0), (x1, y1) = S(ua - 11, z1), S(ub + 11, z0)
            d.rect(x0, y0, x1 - x0, y1 - y0, fill=BLACKPART_F, stroke=BLACKPART, sw=2.5)
        # pulley first (it is farther away), then the stacks
        _pulley_side(d, lambda s, h: S(s, h + _FACE), ks, upper, 16.5 if upper else 6.5)
        _stack_side(d, S, u_f, 68.0, 2, ks)
        _stack_side(d, S, u_n, 78.0 if upper else 68.0, 1, ks)
        # printed boss under (A) or over (B) the near stack
        bz0, bz1 = (67.0, 78.0) if upper else (78.0, 89.0)
        (x0, y0), (x1, y1) = S(u_n - 5, bz1), S(u_n + 5, bz0)
        d.rect(x0, y0, x1 - x0, y1 - y0, fill=BLACKPART_F, stroke=BLACKPART, sw=2)
        # the belt's band across the three
        zb0, zb1 = (80.0, 86.0) if upper else (70.0, 76.0)
        (x0, y0), (x1, y1) = S(ua - 10, zb1), S(ub + 10, zb0)
        d.rect(x0, y0, x1 - x0, y1 - y0, fill=colour, stroke=colour, sw=2, op=0.55)
        # the far post's other pair carries the other belt
        lx = S(u_f, 73.0 if upper else 83.0)
        tx = px + 24 if not mirror else px + 531
        d.text(tx, py + ph - 22, f"other pair: {'B' if upper else 'A'} belt",
               size=T_MIN, weight=600, fill=MUTED, anchor="start" if not mirror else "end")
        d.leader(lx[0], lx[1], lx[0], py + ph - 52, col=MUTED)

    column(30, "A", A_OUTER, A_BORE, A_POSTS, BELT_A, True, "arwa")
    column(615, "B", B_OUTER, B_BORE, B_POSTS, BELT_B, False, "arwb")
    return d


# ============================================================= diagram 404 ===
def _arm_section(d, cx, y0, k, wide_up=True, sw=3):
    """Section through the tension arm along its stepped hole (18 mm long:
    13 mm at 3.5, 5 mm at 4.7). Returns the y of the hole's top opening."""
    W, L = 14.0, 18.0
    x0 = cx - W / 2 * k
    d.rect(x0, y0, W * k, L * k, fill=ORANGE_F, stroke=ORANGE, sw=sw)
    d.rect(x0, y0, W * k, L * k, fill="url(#hatch)", stroke="none", sw=0)
    wide = (y0, y0 + 5 * k) if wide_up else (y0 + 13 * k, y0 + L * k)
    narrow = (y0 + 5 * k, y0 + L * k) if wide_up else (y0, y0 + 13 * k)
    for (a, b), r in ((wide, 2.35), (narrow, 1.75)):
        d.rect(cx - r * k, a, 2 * r * k, b - a, fill=PANEL, stroke="none", sw=0)
        d.line(cx - r * k, a, cx - r * k, b, stroke=ORANGE, sw=sw)
        d.line(cx + r * k, a, cx + r * k, b, stroke=ORANGE, sw=sw)
    ys = y0 + (5 if wide_up else 13) * k                 # the step
    for sgn in (-1, 1):
        d.line(cx + sgn * 1.75 * k, ys, cx + sgn * 2.35 * k, ys, stroke=ORANGE, sw=sw)
    return y0


def _insert(d, cx, y0, k, sw=2.5):
    """Brass heat-set insert, 5 mm across, 4 mm long, knurled, standing upright."""
    w, h = 5.0 * k, 4.0 * k
    d.rect(cx - w / 2, y0, w, h, fill=AMBER_F, stroke=BROWN, sw=sw, rx=3)
    for i in range(1, 5):
        yy = y0 + i * h / 5
        d.line(cx - w / 2 + 4, yy - 8, cx + w / 2 - 4, yy + 8, stroke=AMBER, sw=2)
    d.rect(cx - 1.25 * k, y0, 2.5 * k, h, fill=PANEL, stroke=BROWN, sw=1.5)


def d404_tensioner_insert() -> dd.Doc:
    d = dd.Doc(900, "The tension arm's stepped hole: the insert goes in the wide end")
    top = step_header(d, "Insert into the wide end")
    py = top + 18
    d.panel(30, py, 760, 770)
    k = 21.0
    cx = 250
    y0 = py + 330
    _arm_section(d, cx, y0, k)
    # insert above the wide end, press tip above it, arrow down
    iy = y0 - 4.0 * k - 70
    _insert(d, cx, iy, k)
    d.rect(cx - 1.1 * k, py + 60, 2.2 * k, iy - py - 60 + 1.0 * k, fill=STEEL,
           stroke=GREY, sw=2.5, rx=4)
    d.rect(cx - 3.2 * k, py + 40, 6.4 * k, 60, fill=GREY_F, stroke=GREY, sw=2.5, rx=6)
    d.text(cx - 3.2 * k - 16, py + 80, "press tip", size=T_MIN, anchor="end", weight=600,
           fill=MUTED)
    _arrow(d, cx + 4.2 * k, iy - 10, cx + 4.2 * k, y0 - 12, col=INK, sw=6)
    # labels
    lx = 470
    d.leader(cx + 2.35 * k + 4, y0 + 2.5 * k, lx - 14, y0 + 2.5 * k - 14, col=INK)
    d.text(lx, y0 + 2.5 * k - 20, "4.7 mm end:", size=T_LAB + 2, weight=700, fill=BROWN)
    d.text(lx, y0 + 2.5 * k + 22, "insert here", size=T_LAB + 2, weight=700)
    d.leader(cx + 1.75 * k + 4, y0 + 12 * k, lx - 14, y0 + 12 * k - 14, col=INK)
    d.text(lx, y0 + 12 * k - 20, "3.5 mm:", size=T_LAB + 2, weight=700)
    d.text(lx, y0 + 12 * k + 22, "keep clear,", size=T_LAB + 2, weight=700)
    d.text(lx, y0 + 12 * k + 64, "the screw", size=T_LAB + 2, weight=700)
    d.text(lx, y0 + 12 * k + 106, "slides through", size=T_LAB + 2, weight=700)
    d.text(54, py + 745, "the arm cut in half along the hole", size=T_MIN, fill=MUTED)

    # wrong: insert at the narrow end
    ox = 810
    d.panel(ox, py, 360, 770)
    d.text(ox + 24, py + 52, "Wrong end", size=38, weight=700, fill=RED)
    k2 = 11.0
    c2 = ox + 130
    y2 = py + 330
    _arm_section(d, c2, y2, k2, wide_up=False, sw=2.5)
    _insert(d, c2, y2 - 4 * k2 - 40, k2, sw=2)
    _cross(d, c2 + 7.5 * k2 + 30, y2 - 2 * k2 - 30, 26)
    d.text(ox + 24, py + 610, "the narrow end:", size=T_MIN, weight=700, fill=RED)
    d.text(ox + 24, py + 650, "the insert", size=T_MIN, weight=700, fill=RED)
    d.text(ox + 24, py + 690, "will not fit", size=T_MIN, weight=700, fill=RED)
    return d


# ============================================================= diagram 405 ===
def _frame_side(d, x0, yface, k, face_up):
    """Upper drive frame in side view, schematic: a 6 mm plate (the flat face) with
    walls 9 mm deep on the other side. face_up: the flat face is the top edge."""
    L, T, Wd = 64.0, 6.0, 9.0
    sgn = 1 if face_up else -1                     # direction from the face into the part
    def R(a, b, h0, h1, fill=BLACKPART_F):
        ya, yb = yface + sgn * h0 * k, yface + sgn * h1 * k
        d.rect(x0 + a * k, min(ya, yb), (b - a) * k, abs(yb - ya), fill=fill,
               stroke=BLACKPART, sw=3)
    R(0, L, 0, T)
    for a, b in ((0, 5), (26, 39), (59, 64)):
        R(a, b, T, T + Wd)
    return [x0 + 16 * k, x0 + 53 * k]               # post holes, 37 mm apart


def d405_flip_upper_frame() -> dd.Doc:
    d = dd.Doc(820, "Dropping the two M5x30 screws in and turning the frame over")
    top = step_header(d, "Screws in, then turn it over")
    py, ph = top + 18, 690
    k = 7.0
    # 1: flat face up, the screws drop in from that face
    d.panel(30, py, 555, ph)
    callout(d, 70, py + 50, 1)
    d.text(112, py + 62, "flat face up", size=T_LAB + 2, weight=700)
    yf = py + 420
    x0 = 30 + (555 - 64 * k) / 2
    posts = _frame_side(d, x0, yf, k, face_up=True)
    for x in posts:
        dd._bhcs(d, x, yf - 22 * k, k, 0, 1, 30, solid=30)
        _arrow(d, x + 40, yf - 26 * k, x + 40, yf - 12 * k, col=MUTED, sw=4, mk="arwm")
    # redraw the plate over the shank tips so they read as entering the holes
    (pa, pb) = posts
    for x in posts:
        d.rect(x - 2.7 * k, yf - 1, 5.4 * k, 6 * k + 2, fill=PANEL, stroke="none", sw=0)
    _frame_side(d, x0, yf, k, face_up=True)
    for x in posts:
        d.rect(x - 2.7 * k, yf + 2, 5.4 * k, 6 * k - 4, fill=PANEL, stroke="none", sw=0)
        d.line(x - 2.5 * k, yf + 2, x - 2.5 * k, yf + 6 * k - 2, stroke=GREY, sw=2.5,
               dash="6 5")
        d.line(x + 2.5 * k, yf + 2, x + 2.5 * k, yf + 6 * k - 2, stroke=GREY, sw=2.5,
               dash="6 5")
    d.text(54, py + ph - 30, "M5x30, into the holes by the bore", size=T_MIN,
           fill=MUTED)

    # 2: turned over, heads held, threads standing up
    d.panel(615, py, 555, ph)
    callout(d, 655, py + 50, 2)
    d.text(697, py + 62, "turn it over,", size=T_LAB + 2, weight=700)
    d.text(697, py + 104, "holding the heads", size=T_LAB + 2, weight=700)
    bench = py + ph - 90
    yf2 = bench - 2.75 * k
    x2 = 615 + (555 - 64 * k) / 2
    posts2 = [x2 + 16 * k, x2 + 53 * k]
    for x in posts2:
        dd._bhcs(d, x, yf2, k, 0, -1, 30, solid=30)
    _frame_side(d, x2, yf2, k, face_up=False)
    for x in posts2:                                 # shank through the plate, hidden
        d.rect(x - 2.5 * k + 2, yf2 - 6 * k + 2, 5 * k - 4, 6 * k - 4, fill=GREY_F,
               stroke="none", sw=0)
    d.line(615 + 30, bench, 615 + 525, bench, stroke=GREY, sw=5)
    d.text(615 + 525, py + 190, "threads up", size=T_LAB, anchor="end", weight=700)
    for x in posts2:
        d.leader(x + 2.5 * k + 4, yf2 - 28 * k, 615 + 470, py + 200, col=INK)
    # a curved arrow: over the top, from panel 1 into panel 2
    d.path(f"M 520 {py + 150} Q 600 {py + 40} 680 {py + 160}", stroke=ORANGE, sw=6,
           marker="arwo")
    return d


# ============================================================= diagram 406 ===
def _hub_section(d, cx, cy, k, flat_deg, s1_deg, s2_deg, sw=3):
    """Pulley hub cut across at the set screws: hub, shaft with a flat at flat_deg
    (0 = right, page angles clockwise), two set screws along s1_deg and s2_deg."""
    d.circle(cx, cy, 8 * k, fill=GREY_F, stroke=GREY, sw=sw)
    # shaft: a 5 mm circle with a flat 2.0 mm from the centre
    a = math.radians(flat_deg)
    half = math.degrees(math.acos(2.0 / 2.5))
    pts = []
    for t in range(int(flat_deg + half), int(flat_deg + 360 - half) + 1, 6):
        r = math.radians(t)
        pts.append((cx + 2.5 * k * math.cos(r), cy + 2.5 * k * math.sin(r)))
    t0, t1 = math.radians(flat_deg - half), math.radians(flat_deg + half)
    pts.append((cx + 2.5 * k * math.cos(t0), cy + 2.5 * k * math.sin(t0)))
    d.path(_pts_path(pts), fill=STEEL, stroke=INK, sw=sw)
    for deg, land in ((s1_deg, None), (s2_deg, None)):
        u = (math.cos(math.radians(deg)), math.sin(math.radians(deg)))
        v = (-u[1], u[0])
        # tapped hole from the bore out to the hub surface
        def P(r, w):
            return cx + u[0] * r * k + v[0] * w * k, cy + u[1] * r * k + v[1] * w * k
        d.poly([P(2.4, -1.5), P(8.05, -1.5), P(8.05, 1.5), P(2.4, 1.5)], fill=PANEL,
               stroke=GREY, sw=2)
        # the screw: its tip on whatever it meets along that line
        rin = 2.5
        diff = (deg - flat_deg + 180) % 360 - 180
        if abs(diff) < 1:
            rin = 2.0
        d.poly([P(rin, -1.5), P(rin + 3.6, -1.5), P(rin + 3.6, 1.5), P(rin, 1.5)],
               fill=GREY, stroke=INK, sw=2)
        d.poly([P(rin + 3.6, -0.75), P(rin + 3.0, -0.75), P(rin + 3.0, 0.75),
                P(rin + 3.6, 0.75)], fill=PANEL, stroke=INK, sw=1.5)


def d406_set_screw_flat() -> dd.Doc:
    d = dd.Doc(850, "The first set screw goes onto the flat of the motor shaft")
    top = step_header(d, "First set screw on the flat")
    py = top + 18
    d.panel(30, py, 760, 670)
    k = 24.0
    cx, cy = 290, py + 360
    _hub_section(d, cx, cy, k, flat_deg=0, s1_deg=0, s2_deg=-90)
    d.line(cx + 2.0 * k, cy - 1.75 * k, cx + 2.0 * k, cy + 1.75 * k, stroke=OK, sw=7)
    callout(d, cx + 8 * k + 50, cy, 2)
    d.text(cx + 8 * k + 92, cy - 8, "first screw:", size=T_LAB + 2, weight=700)
    d.text(cx + 8 * k + 92, cy + 34, "on the flat", size=T_LAB + 2, weight=700, fill=OK)
    d.text(cx + 1.5 * k + 60, cy - 8 * k - 40, "second", size=T_LAB, weight=700,
           fill=MUTED)
    d.leader(cx + 1.6 * k, cy - 7 * k, cx + 1.5 * k + 52, cy - 8 * k - 50, col=MUTED)
    d.text(54, cy + 8 * k + 70, "the shaft's flat side", size=T_MIN, weight=600,
           fill=MUTED)
    d.leader(cx + 2.0 * k, cy + 1.4 * k, 200, cy + 8 * k + 44, col=MUTED)
    d.text(54, py + 52, "the pulley hub, cut across", size=T_MIN, fill=MUTED)

    ox = 810
    d.panel(ox, py, 360, 670)
    d.text(ox + 24, py + 52, "Wrong", size=38, weight=700, fill=RED)
    k2 = 13.0
    # the flat under the second screw, the first screw tightened on the round
    _hub_section(d, ox + 170, py + 300, k2, flat_deg=-90, s1_deg=0, s2_deg=-90, sw=2.5)
    _cross(d, ox + 170 + 8 * k2 + 30, py + 300 - 60, 22)
    d.text(ox + 170 + 8.05 * k2 + 8, py + 300 + 52, "1st", size=T_MIN, weight=700,
           fill=RED)
    d.text(ox + 170 - 1.5 * k2 - 10, py + 300 - 8.05 * k2 - 12, "2nd", size=T_MIN,
           weight=700, anchor="end", fill=MUTED)
    d.text(ox + 24, py + 520, "first screw on", size=T_MIN, weight=700, fill=RED)
    d.text(ox + 24, py + 560, "the round part", size=T_MIN, weight=700, fill=RED)
    step_note(d, "Only if your motor shaft has a flat side.", size=T_MIN)
    return d


# ================================================================ registry ===
_SCHEMATIC = ("Proportions are schematic where a part is not traced from an STL or the CAD; "
              "order, side, face, count and every number are from the sources in the "
              "module docstring.")

DIAGRAMS = [
    {
        "n": 401,
        "file": "401-near-far-post.svg",
        "title": "Near post, far post",
        "fn": d401_post_positions,
        "shows": [
            "Both upper drive frames from above, flat face down as on the bench, traced "
            "from the STLs: the motor bore, the near post about 17 mm from its centre "
            "(2 bearings) and the far post about 34 mm away (4 bearings). The far post is "
            "on the right for A and on the left for B, as p.74 and p.78 draw them.",
        ],
        "insert": [
            ("04-ab-drives.md", "Step 04.21", "both posts on A, before the near stack"),
            ("04-ab-drives.md", "Step 04.30", "both posts on B, before the far stack"),
        ],
        "verify": [
            "Outline is the flat face's outline at 0.5 mm, simplified to 0.25 mm; the "
            "walls and pockets above it are left out.",
            "The stacks are drawn at the F695 flange size (15 mm) from above; the far "
            "stack's thicker ring only marks it, both look the same from above.",
        ],
    },
    {
        "n": 402,
        "file": "402-pulley-jig.svg",
        "title": "Pulley height with the jig",
        "fn": d402_pulley_jig,
        "shows": [
            "A and B motors from the side after p.75 and p.79: the jig standing on its "
            "long bottom edge on the motor face beside the pulley, letters upright, its A "
            "(or B) tab in the pulley's groove; the tab's underside level with the top of "
            "the lower flange (16.5 mm on A hub down, 6.5 mm on B hub up). Callouts 1-3 "
            "are the Do numbers of Steps 04.24 and 04.33.",
            "Two wrong ways, small: the jig on its two feet (every height 3 mm high), and "
            "the teeth lined up with the tab's top (about 23 mm on A, 13 mm on B).",
        ],
        "insert": [
            ("04-ab-drives.md", "Step 04.24", "the A side and both wrong ways"),
            ("04-ab-drives.md", "Step 04.33", "the B side"),
        ],
        "verify": [
            "The jig outline and tab heights are from pulley_jig.stl; the pulley "
            "(hub 16 mm, flanges 15.2 mm, teeth 11.65 mm across, 7 mm groove) is from "
            "the CAD and drawn schematically; the motor boss is the nominal NEMA 17 "
            "22 mm x 2 mm, not measured on the LDO motor.",
            "In the 'tab's top' panel the jig is drawn a little away from the pulley so "
            "the hub clears the tab.",
        ],
    },
    {
        "n": 403,
        "file": "403-belt-through-drive.svg",
        "title": "Belt through the drive",
        "fn": d403_belt_level,
        "shows": [
            "Each drive from above, right way up, seen standing behind the printer (so its "
            "posts mirror diagram 401's upside-down bench view), with the frame shown as a "
            "dashed outline so the stacks show: the belt end run over the near stack, teeth "
            "round the pulley's front and over the far stack, as the CAD routes the A and B "
            "belts. Below a rule, the same drive from behind as p.76 and p.80 draw it, "
            "labelled so: the belt's band level across the "
            "near pair, the pulley teeth and the far post's upper pair (A) or lower pair "
            "(B); the far post's other pair carries the other belt. Callouts 1 and 2 are "
            "the Do numbers of Steps 04.28 and 04.37.",
        ],
        "insert": [
            ("04-ab-drives.md", "Step 04.28", "A on the upper level"),
            ("04-ab-drives.md", "Step 04.37", "B on the lower level"),
        ],
        "verify": [
            "Frame plates in the side view are schematic slabs (the real frames have walls "
            "and pockets); stack, pulley and belt heights are the CAD's.",
            "The belt's centre line is drawn 7.2 mm from each stack's axis and 7 mm from "
            "the pulley's; the wrap angles follow the CAD, the strand lengths are "
            "approximate.",
        ],
    },
    {
        "n": 404,
        "file": "404-tensioner-insert.svg",
        "title": "Insert into the wide end",
        "fn": d404_tensioner_insert,
        "shows": [
            "The tension arm cut in half along its one hole: 5 mm at 4.7 mm across at "
            "the top, 13 mm at 3.5 mm below it. The insert sits over the 4.7 mm end under "
            "the press tip; the 3.5 mm part stays clear for the M3x40. A small panel shows "
            "the insert offered to the narrow end, crossed out.",
        ],
        "insert": [("04-ab-drives.md", "Step 04.4", "the whole sheet")],
        "verify": [
            "The arm's material around the hole is drawn as a 14 mm block; the hole's "
            "lengths and diameters are the STL's. Insert 5 x 4 mm and the press tip are "
            "schematic.",
        ],
    },
    {
        "n": 405,
        "file": "405-flip-upper-frame.svg",
        "title": "Screws in, then turn it over",
        "fn": d405_flip_upper_frame,
        "shows": [
            "The upper drive frame from the side, twice: (1) flat face up, the two M5x30 "
            "BHCS dropping in from that face, 37 mm apart; (2) turned over with the heads "
            "held, the frame on the bench on the two heads and both threads standing up. "
            "Callouts 1 and 2 are the Do numbers of Steps 04.20 and 04.29.",
        ],
        "insert": [
            ("04-ab-drives.md", "Step 04.20", "the A frame"),
            ("04-ab-drives.md", "Step 04.29", "the B frame"),
        ],
        "verify": [
            "The frame is a schematic 64 mm slab with three walls; only the post spacing "
            "(37 mm), the 6 mm plate and the screw size are real. p.74 shows the "
            "upside-down frame resting with the heads under it.",
        ],
    },
    {
        "n": 406,
        "file": "406-set-screw-flat.svg",
        "title": "First set screw on the flat",
        "fn": d406_set_screw_flat,
        "shows": [
            "The pulley hub cut across at its two set screws, 90 degrees apart: the first "
            "screw's tip on the flat side of the motor shaft, the second on the round. "
            "Callout 2 is the Do number of Step 04.25. A small panel shows the first screw "
            "tightened on the round part with the flat under the second, crossed out.",
        ],
        "insert": [("04-ab-drives.md", "Step 04.25", "which screw goes on the flat")],
        "verify": [
            "Whether the kit's A/B motor shafts have a flat is not known before kit day "
            "(the step says 'if it has one'); the flat's depth (0.5 mm) is schematic.",
            "Set screw angle (90 degrees) is from the CAD pulley; the kit pulley may "
            "differ (verify on bench).",
        ],
    },
]

