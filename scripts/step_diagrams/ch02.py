"""Chapter 02 (Z drives, Z idlers, Z rails, deck panel) step diagrams, numbered 201 onwards.

Geometry sources:
- Voron 2.4r2 manual (pinned PDF), p.25, p.27, p.32, p.33, p.38, p.41, p.43, p.44 rendered
  at 150-400 dpi.
- The Voron 2.4r2 CAD index (250 size, ~/.cache/voron-cad): the Z0 corner ("Z Belt Drive A
  (1)") gives the shaft stack positions along the shaft (625 / 80T / 2 shims / 625 / 2 shims /
  20T / 625, 20T flange 33.2 mm from the long end), the drive and motor positions against
  the frame rails, the M5x40 and M5x10 positions and the closed tensioner's span.
- The STLs under slicer/stl/voron2/STLs (Voron-2 @ de7e89d): outlines below are plane slices
  of z_drive_retainer_a / z_drive_main_a (z = 1 mm), [a]_belt_tensioner_a (z = 1 mm, centred
  on its pivot hole), pulley_jig (z = 0.5 mm) and deck_support_3mm (z = 0.3 mm), simplified
  to 0.15-0.3 mm. Heat-set bores were found by slicing for 4.7 mm circles.
"""
import math

import draw_diagrams as dd
from draw_diagrams import (AMBER, AMBER_F, BLACKPART, BLACKPART_F, BLUE, BLUE_F, FAINT,
                           GREY, GREY_F, INK, MUTED, OK, ORANGE, ORANGE_F, PANEL, RED,
                           RULE, STEEL, T_LAB, T_MIN, callout, label_bg, legend_row,
                           profile2020, step_header, step_note)

# ------------------------------------------------------------ STL outlines ---
# [a]_belt_tensioner_a, mm, origin on the pivot hole; +x runs along the arm to the tab.
CAM = [[-9.07, -4.2], [-9.87, -3.07], [-11.7, -2.42], [-12.43, -1.67], [-12.5, 2.0],
       [-11.74, 4.29], [-10.45, 6.32], [-8.71, 7.99], [-6.62, 9.2], [-2.7, 10.0],
       [22.01, 10.0], [22.92, 9.38], [22.99, 5.9], [22.46, 5.11], [14.16, 4.93],
       [11.46, 3.53], [10.28, 1.65], [9.7, -2.43], [8.62, -5.07], [6.53, -7.57],
       [3.75, -9.27], [-0.25, -10.0], [-3.83, -9.24], [-6.89, -7.24]]
CAM_TAB = (15.0, 6.5, 23.0, 10.0)            # raised tab, x0 y0 x1 y1 (to 8.8 mm tall)

# pulley_jig, mm, as printed. The Z tab is x -7.2..-0.4, y 25.4..32.15; the B tab is
# x -23.5..-18, y 9.6..16.4. Stood on its x = -18 edge, the Z tab spans 10.8-17.6 mm.
JIG = [[-9.37, 3.33], [-8.89, 3.49], [-8.51, 3.09], [-9.0, 1.88], [-8.7, 0.08],
       [-3.4, 0.04], [-3.01, 0.5], [-2.72, 5.27], [-1.68, 6.48], [0.0, 7.0], [1.54, 6.58],
       [2.72, 5.27], [3.01, 0.5], [3.5, 0.01], [8.7, 0.08], [9.0, 1.88], [8.5, 3.01],
       [8.91, 3.49], [10.12, 3.0], [17.79, 3.14], [18.0, 19.6], [23.5, 19.6], [23.5, 26.4],
       [-0.4, 26.4], [-0.4, 32.15], [-7.2, 32.15], [-7.2, 25.4], [-17.79, 25.26],
       [-18.0, 17.51], [-17.53, 16.23], [-17.99, 15.9], [-18.98, 16.39], [-23.5, 16.4],
       [-23.5, 9.6], [-18.0, 9.6], [-18.0, 3.6], [-17.6, 3.04], [-10.12, 3.0]]

# deck_support_3mm, mm, as printed: key (head + neck) at the bottom (y 55.25-61.25),
# body y 61.05-69.73, x 52.5-72.5. Neck centre x 66.31: the short end (x 72.5) is the ledge.
CLIP = [[52.5, 68.76], [52.5, 61.95], [53.03, 61.17], [61.3, 61.05], [61.5, 61.25],
        [64.22, 61.25], [64.22, 59.05], [60.2, 59.05], [60.2, 58.6], [63.55, 55.25],
        [68.75, 55.25], [71.4, 57.9], [71.4, 59.05], [68.4, 59.05], [68.4, 61.25],
        [71.6, 61.06], [72.42, 61.67], [72.5, 68.85], [71.97, 69.63], [66.73, 69.71],
        [64.67, 67.56], [62.6, 66.92], [61.42, 67.07], [60.33, 67.56], [59.44, 68.35],
        [58.68, 69.48], [58.19, 69.73], [53.3, 69.73], [52.73, 69.38]]
CLIP_NECK_X, CLIP_FACE_Y = 66.31, 61.05

# z_drive_retainer_a / z_drive_main_a flat face (z = 1 mm): outer outline + windows.
RET = [[[149.0, 89.3], [130.8, 89.3], [129.8, 90.1], [129.8, 137.5], [130.4, 138.6],
        [149.0, 138.7], [149.9, 137.9], [150.0, 90.5], [149.6, 89.6]],
       [[126.3, 85.0], [158.8, 85.0], [159.7, 85.5], [159.8, 91.7], [157.8, 94.7],
        [157.2, 97.6], [157.2, 130.9], [158.0, 133.8], [159.8, 136.3], [159.8, 143.0],
        [159.4, 143.9], [152.8, 144.0], [152.3, 145.0], [147.5, 145.0], [147.0, 144.0],
        [95.2, 144.0], [93.4, 143.0], [93.2, 103.9], [93.8, 101.5], [94.8, 100.2],
        [96.5, 99.2], [119.7, 93.0], [121.8, 91.7], [123.4, 89.8], [124.2, 88.1],
        [124.5, 85.5]],
       [[100.8, 128.5], [100.8, 109.5], [101.6, 107.0], [103.4, 105.7], [118.0, 102.0],
        [119.8, 102.0], [121.4, 102.7], [122.5, 104.1], [123.0, 105.9], [123.0, 132.0],
        [122.1, 134.4], [120.8, 135.5], [119.3, 136.0], [102.8, 135.9], [101.5, 135.0],
        [100.9, 133.9]]]
MAIN = [[[129.8, 125.7], [130.0, 127.9], [130.8, 128.7], [149.4, 128.4], [150.0, 126.4],
         [150.0, 104.6], [149.3, 102.4], [130.2, 102.6], [129.8, 104.6]],
        [[157.3, 144.5], [114.7, 144.5], [113.9, 143.7], [113.6, 137.5], [111.4, 134.6],
         [109.3, 133.6], [96.5, 130.3], [94.8, 129.3], [93.6, 127.6], [93.2, 125.6],
         [93.2, 87.5], [93.7, 86.1], [95.2, 85.5], [159.5, 85.7], [159.8, 86.5],
         [159.8, 143.5], [159.2, 144.4]],
        [[100.6, 118.5], [99.4, 119.3], [99.4, 121.7], [100.1, 123.0], [111.6, 129.5],
         [113.3, 129.1], [122.9, 123.5], [123.8, 122.7], [124.3, 121.4], [124.3, 119.2],
         [123.4, 118.5]],
        [[100.3, 112.5], [99.4, 111.5], [99.4, 109.3], [100.3, 107.8], [111.6, 101.5],
         [113.3, 101.9], [122.9, 107.5], [123.9, 108.4], [124.3, 109.6], [124.3, 111.8],
         [123.4, 112.5]]]
RET_INSERTS = [(x, y) for x in (97, 126, 153) for y in (103, 125)]
MAIN_CBORES = [(x, y) for x in (97, 126, 153) for y in (105, 126)]


# ----------------------------------------------------------------- helpers ---
def _path(pts, close=True):
    s = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return s + (" Z" if close else "")


def _xf(pts, fx, fy):
    return [(fx(x, y), fy(x, y)) for x, y in pts]


def _rot(pts, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(x * c - y * s, x * s + y * c) for x, y in pts]


def _arrow(d, x0, y0, x1, y1, col=INK, sw=5, mk="arw", dash=None):
    d.path(f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}", stroke=col, sw=sw, marker=mk,
           dash=dash)


def _twoway(d, x0, y0, x1, y1, col=INK, sw=4, mk="arw"):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    _arrow(d, mx, my, x0, y0, col, sw, mk)
    _arrow(d, mx, my, x1, y1, col, sw, mk)


def _bracket_h(d, x0, x1, y, col=MUTED, tick=14):
    d.path(f"M {x0} {y - tick} L {x0} {y} L {x1} {y} L {x1} {y - tick}", stroke=col, sw=3)


# ============================================================= diagram 201 ===
def d201_shaft_stack() -> dd.Doc:
    """02.19: the Z drive shaft, side view, short end left, long end right."""
    d = dd.Doc(1310, "The Z drive shaft stack, in order")
    step_header(d, "The shaft stack, in order")
    k = 13.0
    X0, Yc = 210, 560

    def X(s):                               # s = mm from the shaft's long end
        return X0 + (60 - s) * k

    def disc(s0, s1, dia, fill, stroke, sw=2.5):
        x0, x1 = X(s1), X(s0)
        d.rect(x0, Yc - dia / 2 * k, x1 - x0, dia * k, fill=fill, stroke=stroke, sw=sw, rx=3)
        return x0, x1

    def bearing(s0):
        x0, x1 = disc(s0, s0 + 5, 16, GREY_F, GREY, 3)
        d.rect(x0 + 4, Yc - 4.2 * k, x1 - x0 - 8, 8.4 * k, fill=STEEL, stroke=GREY, sw=2)
        return (x0 + x1) / 2

    # shaft, with the D-cut flat drawn as a line near its top edge
    d.rect(X(60), Yc - 2.5 * k, 60 * k, 5 * k, fill=STEEL, stroke=GREY, sw=2.5, rx=2)
    d.line(X(60) + 6, Yc - 1.6 * k, X(0) - 6, Yc - 1.6 * k, stroke=GREY, sw=1.5)

    # 80T: toothed disc 6.2-17.2, hub 17.2-24.2 toward the 20T
    disc(17.2, 24.2, 32, GREY_F, GREY)
    x0, x1 = disc(6.2, 17.2, 55, GREY_F, GREY, 3)
    for sgn in (-1, 1):                      # flanges and the tooth band
        d.rect(x0 + 13, Yc + sgn * 25.5 * k - (2 * k if sgn > 0 else 0), x1 - x0 - 26, 2 * k,
               fill="url(#hatch)", stroke=GREY, sw=1.5)
    d.circle(X(14), Yc - 12 * k, 0.9 * k, fill=PANEL, stroke=GREY, sw=2)   # set screw
    m80 = (x0 + x1) / 2

    sp = [(24.2, 26.2), (31.2, 33.2)]        # two 1 mm spacers each
    for a, b in sp:
        disc(a, a + 1, 10, AMBER_F, AMBER, 2.5)
        disc(a + 1, b, 10, AMBER_F, AMBER, 2.5)
    mid_b = bearing(26.2)
    b_long = bearing(0)
    b_short = bearing(55.2)

    # 20T: flange 33.2-34.2, teeth 34.2-44, collar 44-53.2 with a set screw
    disc(34.2, 44, 12.2, GREY_F, GREY)
    tx0, tx1 = X(44), X(34.2)
    for i in range(-4, 5):
        y = Yc + i * 1.35 * k
        d.line(tx0 + 3, y, tx1 - 3, y, stroke=GREY, sw=1.5)
    disc(33.2, 34.2, 16, GREY_F, GREY, 2.5)
    cx0, cx1 = disc(44, 53.2, 16, GREY_F, GREY, 2.5)
    d.circle((cx0 + cx1) / 2, Yc, 1.3 * k, fill=PANEL, stroke=GREY, sw=2.5)
    m20 = (tx0 + cx1) / 2

    # 33 mm, long end to the 20T's flange
    dy = 160
    for x in (X(0), X(33.2)):
        d.line(x, dy - 14, x, Yc - 8 * k - 6, stroke=MUTED, sw=2, dash="6 6")
    _twoway(d, X(33.2) + 3, dy, X(0) - 3, dy, col=INK, sw=3)
    d.text((X(33.2) + X(0)) / 2, dy - 16, "33 mm", size=T_LAB + 4, anchor="middle",
           weight=800)

    # part names
    ly = Yc + 8 * k + 50
    for x, s in ((b_short, "625"), (m20, "20T"), (mid_b, "625")):
        d.text(x, ly, s, size=T_LAB, anchor="middle", weight=700)
    for xs, lx in ((X(32.2), 440), (X(25.2), 670)):
        d.text(lx, 300, "2 spacers", size=T_LAB, anchor="middle", weight=700, fill=AMBER)
        d.leader(xs, Yc - 5 * k - 4, lx, 310, col=AMBER)
    d.text(m80, Yc + 27.5 * k + 44, "80T", size=T_LAB, anchor="middle", weight=700)
    d.text(b_long, Yc + 27.5 * k + 44, "625", size=T_LAB, anchor="middle", weight=700)

    # callouts: 1 the first 625, 2 the order after the 20T, 3 push on the inner ring
    callout(d, b_short, ly + 60, 1)
    by = Yc + 27.5 * k + 86
    _bracket_h(d, X(33.2), X(0), by, col=ORANGE, tick=-16)
    callout(d, (X(33.2) + X(0)) / 2, by + 34, 2)
    _arrow(d, X(0) + 90, Yc, X(0) + 10, Yc, col=ORANGE, sw=6, mk="arwo")
    callout(d, X(0) + 120, Yc, 3)

    y = legend_row(d, 60, 1130, 1, ["625 against the collar"])
    y = legend_row(d, 60, y + 26, 2, ["then spacers, 625, spacers, 80T, 625"])
    legend_row(d, 60, y + 26, 3, ["push only on a bearing's inner ring"])
    return d


# ============================================================= diagram 202 ===
def d202_rail_holes_faces() -> dd.Doc:
    """02.06 / 02.09: which holes take a screw, the 3 mm key, and which face each rail is on."""
    d = dd.Doc(1260, "Z rails: which holes, which faces")
    top = step_header(d, "Z rails: holes and faces")

    # ---- side view of one rail, bottom on the 3 mm key (rail length schematic)
    d.panel(30, top + 16, 560, d.h - top - 32)
    kk = 2.25                                    # px per mm along the rail
    ybot = 1080                                  # rail's bottom end
    vx0, vx1 = 160, 290                          # the vertical behind the rail
    rx0, rx1 = 192, 258                          # the rail
    d.rect(vx0, top + 40, vx1 - vx0, 1160 - top - 40 - 40, fill=BLUE_F, stroke=BLUE, sw=3)
    d.rect(60, 1112, 510, 48, fill=BLUE_F, stroke=BLUE, sw=3)          # bottom horizontal
    d.rect(vx0, 1112, vx1 - vx0, 48, fill=BLUE, stroke=BLUE, sw=1)
    ytop = ybot - 400 * kk
    d.rect(rx0, ytop, rx1 - rx0, ybot - ytop, fill=STEEL, stroke=GREY, sw=3, rx=3)
    # the 3 mm hex key standing under the rail's end (gap exaggerated)
    d.rect(rx0 - 4, ybot + 4, rx1 - rx0 + 64, 24, fill=BLACKPART, stroke=INK, sw=2, rx=4)
    for i in range(1, 21):
        y = ybot - (10 + 20 * (i - 1)) * kk
        used = i % 2 == 0 and i <= 18
        if used:
            d.circle((rx0 + rx1) / 2, y, 15, fill=GREY, stroke=INK, sw=2.5)
            d.circle((rx0 + rx1) / 2, y, 5.5, fill=INK, stroke="none", sw=0)
        else:
            d.circle((rx0 + rx1) / 2, y, 13, fill=PANEL, stroke=INK,
                     sw=5 if i in (1, 19, 20) else 2)
        end = i in (1, 19, 20)
        d.text(vx0 - 14, y + 11, str(i), size=T_MIN, anchor="end",
               weight=800 if end else 500, fill=INK if end else MUTED)
    y1 = ybot - 10 * kk
    y19 = ybot - 370 * kk
    y20 = ybot - 390 * kk
    d.text(318, y20 + 4, "19 and 20:", size=T_LAB, weight=700)
    d.text(318, y20 + 44, "leave empty", size=T_LAB, weight=700)
    d.leader(262, (y19 + y20) / 2, 312, y20 + 16, col=INK)
    d.text(318, y1 - 112, "hole 1 is", size=T_LAB, weight=700)
    d.text(318, y1 - 72, "the bottom one:", size=T_LAB, weight=700)
    d.text(318, y1 - 32, "leave empty", size=T_LAB, weight=700)
    d.leader(262, y1, 312, y1 - 40, col=INK)
    d.text(318, 640, "screws in", size=T_LAB, weight=700)
    d.text(318, 680, "2, 4, 6 and", size=T_LAB, weight=700)
    d.text(318, 720, "on up to 18", size=T_LAB, weight=700)
    d.text(336, 1100, "3 mm key", size=T_LAB, weight=700)

    # ---- plan view, front at the bottom
    px0, py0 = 620, top + 16
    d.panel(px0, py0, 550, 640)
    d.text(px0 + 275, py0 + 52, "Seen from above", size=T_LAB, anchor="middle", weight=700,
           fill=MUTED)
    F, c = 330, 30                               # frame square, corner size
    fx0, fy0 = px0 + (550 - F) / 2, py0 + 130
    d.rect(fx0, fy0, F, F, fill="none", stroke=BLUE, sw=6)
    corners = {"Z0": (fx0, fy0 + F), "Z1": (fx0, fy0), "Z2": (fx0 + F, fy0),
               "Z3": (fx0 + F, fy0 + F)}
    for name, (x, y) in corners.items():
        d.rect(x - c / 2, y - c / 2, c, c, fill=BLUE, stroke=BLUE, sw=1)
        front = name in ("Z0", "Z3")
        # rail on the vertical's rear face (front corners) or front face (rear corners)
        ry = y - c / 2 - 12 if front else y + c / 2
        d.rect(x - 12, ry, 24, 12, fill=GREY, stroke=INK, sw=2)
        left = name in ("Z0", "Z1")
        d.text(x + (-26 if left else 26), y + (44 if front else -26), name, size=T_LAB,
               anchor="end" if left else "start", weight=800)
    for x in (fx0 + 40, fx0 + F - 40):
        _twoway(d, x, fy0 + 40, x, fy0 + F - 40, col=INK, sw=4)
    d.text(px0 + 275, fy0 + F / 2 - 6, "face each", size=T_LAB, anchor="middle", weight=700)
    d.text(px0 + 275, fy0 + F / 2 + 34, "other", size=T_LAB, anchor="middle", weight=700)
    d.text(px0 + 275, fy0 + F + 86, "FRONT", size=T_LAB, anchor="middle", weight=800,
           fill=BLUE)
    d.text(px0 + 275, fy0 - 30, "BACK", size=T_LAB, anchor="middle", weight=800, fill=BLUE)

    ny = py0 + 640 + 70
    d.text(px0 + 10, ny, "Front rails go on the", size=T_LAB, weight=600)
    d.text(px0 + 10, ny + 40, "vertical's back face.", size=T_LAB, weight=600)
    d.text(px0 + 10, ny + 100, "Rear rails go on the", size=T_LAB, weight=600)
    d.text(px0 + 10, ny + 140, "vertical's front face.", size=T_LAB, weight=600)
    d.text(px0 + 10, ny + 220, "Same holes and the", size=T_LAB, weight=600, fill=MUTED)
    d.text(px0 + 10, ny + 260, "same gap on all four.", size=T_LAB, weight=600, fill=MUTED)
    return d


# ============================================================= diagram 203 ===
def d203_z0_corner() -> dd.Doc:
    """02.29-02.31: the Z0 corner from above with the printer upside down (CAD positions)."""
    d = dd.Doc(1200, "The Z0 corner with the printer upside down")
    top = step_header(d, "Z0 corner, printer upside down")
    k = 6.2
    ox, oy = 440, 640             # screen position of plan (0, 0)

    def P(xp, y):                 # xp: CAD x mirrored (printer rolled over), y: CAD y
        return ox + xp * k, oy - y * k

    def R(x0, y0, x1, y1, **kw):
        a, b = P(x0, y1), P(x1, y0)
        d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], **kw)

    # frame: front rail along the bottom, the left side rail (now on your right) going back
    R(-75, -38, 58, -18, fill=BLUE_F, stroke=BLUE, sw=3)
    R(58, -18, 78, 72, fill=BLUE_F, stroke=BLUE, sw=3)
    R(58, -38, 78, -18, fill=BLUE, stroke=BLUE, sw=1)
    for y in (-30.9, -25.1):                     # the top slot's edges
        a, b = P(-75, y), P(58, y)
        d.line(a[0], a[1], b[0], b[1], stroke=BLUE, sw=1.5, op=0.5)
    for x in (65.1, 70.9):
        a, b = P(x, -18), P(x, 72)
        d.line(a[0], a[1], b[0], b[1], stroke=BLUE, sw=1.5, op=0.5)
    # FRONT tape on the front rail
    a, b = P(-68, -21), P(-36, -35)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=AMBER_F, stroke=AMBER, sw=2, rx=3)
    d.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 11, "FRONT", size=T_MIN, anchor="middle",
           weight=800)

    # motor and its mount (foot on the front rail, plate, motor behind it)
    R(-11.3, -8, 31.5, 40, fill=GREY_F, stroke=GREY, sw=3)
    R(-11, -38, 31, -8, fill=BLACKPART_F, stroke=BLACKPART, sw=3)
    R(-11, -14, 31, -8, fill=BLACKPART, stroke=BLACKPART, sw=1)
    R(3, -32, 17, -16, fill=GREY_F, stroke=GREY, sw=2.5)          # 16T
    # closed belt loop between the 16T and the 80T
    R(10, -24.5, 40, -18.5, fill=INK, stroke=INK, sw=1, op=0.85)
    # drive body: retainer (inner half) and main (outer half)
    R(38, -42, 54.2, 28.7, fill=BLACKPART_F, stroke=BLACKPART, sw=3)
    R(54.2, -42, 81, 28.7, fill=BLACKPART_F, stroke=BLACKPART, sw=3)
    a, b = P(38, 28.7), P(38, -42)
    d.line(a[0], a[1], b[0], b[1], stroke=ORANGE, sw=8)             # retainer face
    a, b = P(81, 28.7), P(81, -42)
    d.line(a[0], a[1], b[0], b[1], stroke=OK, sw=8)                 # counterbored face
    # screws: M5x40 down the drive's wells into the side rail, M5x10 in the foot
    for y in (2, 18):
        x, yy = P(68, y)
        d.circle(x, yy, 4.2 * k, fill=GREY, stroke=INK, sw=2.5)
        d.circle(x, yy, 1.5 * k, fill=INK, stroke="none", sw=0)
    for xp in (22.7, -2.3):
        x, yy = P(xp, -28)
        d.circle(x, yy, 4.6 * k, fill=GREY_F, stroke=INK, sw=2.5)
        d.circle(x, yy, 1.4 * k, fill=INK, stroke="none", sw=0)

    # labels
    x, y = P(68, 18)
    d.text(1170, 240, "M5×40 ×2:", size=T_LAB, anchor="end", weight=700)
    d.text(1170, 280, "into the side rail", size=T_LAB, anchor="end", weight=700)
    d.leader(x + 14, y - 22, 1060, 290, col=INK)
    xa, ya = P(-2.3, -28)
    xb, yb = P(22.7, -28)
    _twoway(d, xa, ya + 64, xb, yb + 64, col=MUTED, sw=3, mk="arwm")
    d.text((xa + xb) / 2, ya + 112, "25 mm", size=T_MIN, anchor="middle", weight=700,
           fill=MUTED)
    d.text(60, 920, "M5×10 ×2: into", size=T_LAB, weight=700)
    d.text(60, 960, "the front rail", size=T_LAB, weight=700)
    d.leader(xa - 20, ya + 20, 250, 890, col=INK)
    xr, yr = P(38, 28.7)
    d.text(380, 190, "retainer face:", size=T_LAB, weight=700, fill=ORANGE)
    d.text(380, 230, "toward the motor", size=T_LAB, weight=700, fill=ORANGE)
    d.leader(xr - 2, yr + 20, 600, 246, col=ORANGE)
    xc, yc = P(81, -10)
    d.text(962, 700, "counter-", size=T_LAB, weight=700, fill=OK)
    d.text(962, 740, "bored face:", size=T_LAB, weight=700, fill=OK)
    d.text(962, 780, "outward", size=T_LAB, weight=700, fill=OK)
    xm, ym = P(10, 40)
    d.text(xm, ym - 20, "motor", size=T_LAB, anchor="middle", weight=700, fill=MUTED)
    xd, yd = P(67.6, -34)
    d.text(xd, yd, "Z drive", size=T_LAB, anchor="middle", weight=700, fill=MUTED)

    # where you stand
    d.line(40, 1010, 1160, 1010, stroke=RULE, sw=2)
    _arrow(d, 80, 1150, 80, 1070, col=INK, sw=6)
    d.text(120, 1095, "You stand here, facing", size=T_LAB, weight=700)
    d.text(120, 1135, "the FRONT tape.", size=T_LAB, weight=700)
    d.text(1160, 1095, "Z0 (front-left)", size=T_LAB, anchor="end", weight=800, fill=BLUE)
    d.text(1160, 1135, "is on your right.", size=T_LAB, anchor="end", weight=800, fill=BLUE)
    return d


# ============================================================= diagram 204 ===
def d204_cam_stages() -> dd.Doc:
    """02.33 / 02.34: the belt tensioner cam, open, swinging, closed (seen from above,
    printer upside down, Z0: motor on the left, drive on the right)."""
    d = dd.Doc(1230, "The belt tensioner cam in three stages")
    top = step_header(d, "Closing the cam")
    k = 7.5
    row_h = 375
    piv_x = 600                       # pivot screen x in the open rows

    def row(i, title, shift_mm, deg, swing=False):
        ry = top + 10 + i * row_h
        if i:
            d.line(40, ry, d.w - 40, ry, stroke=RULE, sw=2)
        d.text(48, ry + 46, title, size=T_LAB + 2, weight=700)
        rail_y0 = ry + 105                      # rail (front rail) band, 20 mm
        d.rect(40, rail_y0, 1120, 20 * k, fill=BLUE_F, stroke=BLUE, sw=3)
        cy = rail_y0 + 10 * k                   # the rail's centre line = the screws' line
        px = piv_x - shift_mm * k
        # drive body at the right; its side face where the lobe bears
        face = piv_x + 10 * k
        d.rect(face, ry + 70, 1160 - face, 20 * k + 70, fill=BLACKPART_F, stroke=BLACKPART,
               sw=3, rx=4)
        d.text(face + 140, rail_y0 + 10 * k + 12, "Z drive", size=T_LAB, anchor="middle",
               weight=700, fill=MUTED)
        # motor foot to the left of the pivot (outline only: the cam lies under it)
        fx1 = px + 8 * k
        d.rect(fx1 - 42 * k, rail_y0 - 20, 42 * k, 20 * k + 40, fill="none",
               stroke=BLACKPART, sw=3, rx=4, dash="12 8")
        d.text(fx1 - 42 * k - 14, rail_y0 + 10 * k + 12, "motor foot", size=T_MIN,
               anchor="end", weight=700, fill=BLACKPART)
        # the cam, rotated about its pivot (CAD: arm toward the motor when closed)
        pts = _rot(CAM, deg)
        d.path(_path([(px + x * k, cy - y * k) for x, y in pts]), fill=ORANGE_F,
               stroke=ORANGE, sw=3.5)
        tab = [(CAM_TAB[0], CAM_TAB[1]), (CAM_TAB[2], CAM_TAB[1]), (CAM_TAB[2], CAM_TAB[3]),
               (CAM_TAB[0], CAM_TAB[3])]
        d.path(_path([(px + x * k, cy - y * k) for x, y in _rot(tab, deg)]), fill=ORANGE,
               stroke=ORANGE, sw=2)
        d.circle(px, cy, 4.75 * k, fill=GREY_F, stroke=INK, sw=2.5)        # M5x10 head
        d.circle(px, cy, 1.4 * k, fill=INK, stroke="none", sw=0)
        # the far motor-end screw in the foot, 25 mm along
        d.circle(px - 25 * k, cy, 4.75 * k, fill=GREY_F, stroke=INK, sw=2.5)
        d.circle(px - 25 * k, cy, 1.4 * k, fill=INK, stroke="none", sw=0)
        if swing:
            r = 21 * k
            a0, a1 = math.radians(-112), math.radians(-168)
            p0 = (px + r * math.cos(a0), cy - r * math.sin(a0))
            p1 = (px + r * math.cos(a1), cy - r * math.sin(a1))
            d.path(f"M {p0[0]:.1f} {p0[1]:.1f} A {r:.1f} {r:.1f} 0 0 1 {p1[0]:.1f} "
                   f"{p1[1]:.1f}", stroke=ORANGE, sw=7, marker="arwo")
        return ry, cy, px

    row(0, "a   Tab sticking out, both screws loose", 0, -90)
    row(1, "b   Swing the tab toward the motor", 0, -135, swing=True)
    ry, cy, px = row(2, "c   Flat in the notch: motor pushed away", 2.5, 180)
    # the 2-3 mm the foot moved: its open position faint, an arrow along its top edge
    fx_open = piv_x + 8 * k
    rail_y0 = ry + 105
    d.line(fx_open, rail_y0 - 40, fx_open, rail_y0 + 20 * k + 30, stroke=MUTED, sw=2.5,
           dash="6 6")
    yb = rail_y0 + 20 * k + 44
    _arrow(d, fx_open + 60, yb, px + 8 * k + 2, yb, col=INK, sw=4)
    d.text(fx_open - 2.5 * k - 16, yb + 11, "foot moves 2 to 3 mm", size=T_LAB,
           anchor="end", weight=800)
    return d


# ============================================================= diagram 205 ===
def d205_deck_clip() -> dd.Doc:
    """02.14: a deck support clip, end-first into the rail's inward slot, then turned 90°,
    seen along the rail with the printer upside down (panel below)."""
    d = dd.Doc(960, "Fitting a deck clip: in end-first, then turn it")
    top = step_header(d, "Deck clip: in, then turn")
    k = 13.0

    def scene(ox, title):
        d.panel(ox, top + 16, 555, 790)
        d.text(ox + 24, top + 66, title, size=T_LAB + 2, weight=700)
        cx, cy = ox + 170, top + 400            # rail section centre
        profile2020(d, cx, cy, k)
        face = cx + 10 * k
        # deck panel: inverted, its top face flush with the rail's (now lower) face
        d.rect(face + 0.5 * k, cy + 7 * k, ox + 540 - face - 0.5 * k, 3 * k,
               fill=BLACKPART, stroke=INK, sw=2)
        d.text(ox + 535, cy + 10 * k + 46, "deck panel", size=T_LAB, anchor="end",
               weight=700)
        d.text(cx, cy + 10 * k + 46, "frame rail", size=T_LAB, anchor="middle", weight=700,
               fill=BLUE)
        return cx, cy, face

    # (a) edge-on: the 5.8 mm thickness slides through the 6.2 mm slot mouth
    cx, cy, face = scene(30, "a   Thin edge in")
    body0 = face + 3.0 * k                         # still on its way in
    d.rect(body0 - 5.8 * k, cy - 2.9 * k, 14.5 * k, 5.8 * k, fill=BLACKPART_F,
           stroke=BLACKPART, sw=3, rx=3)
    _arrow(d, body0 + 8.7 * k + 120, cy, body0 + 8.7 * k + 20, cy, col=ORANGE, sw=7,
           mk="arwo")
    callout(d, body0 + 8.7 * k + 70, cy - 70, 1)
    d.text(cx - 10 * k, cy - 10 * k - 50, "long side along the slot", size=T_MIN,
           weight=600, fill=MUTED)

    # (b) turned 90°: head behind the slot lips, the short end over the panel
    ox_b = 615
    cx, cy, face = scene(ox_b, "b   Turn it 90°")

    def C(x, y):
        return face + (y - CLIP_FACE_Y) * k, cy + (x - CLIP_NECK_X) * k
    d.path(_path([C(x, y) for x, y in CLIP]), fill=BLACKPART_F, stroke=BLACKPART, sw=3)
    ex, ey = C(72.5, 68)
    d.text(ox_b + 300, cy + 10 * k + 150, "ledge over", size=T_LAB, weight=700)
    d.text(ox_b + 300, cy + 10 * k + 190, "the panel", size=T_LAB, weight=700)
    d.leader(ex - 4, ey - 4, ox_b + 340, cy + 10 * k + 118, col=INK)
    r = 70
    ax, ay = C(56, 66)
    d.path(f"M {ax + r:.1f} {ay - 40:.1f} A {r} {r} 0 0 0 {ax - 10:.1f} {ay - r - 30:.1f}",
           stroke=ORANGE, sw=7, marker="arwo")
    callout(d, ax + 120, ay - 90, 1)
    step_note(d, "Upside down: the panel lies below.", size=T_LAB)
    return d


# ============================================================= diagram 206 ===
def d206_pulley_jig() -> dd.Doc:
    """02.27: pulley_jig stood on the motor face, Z tab level with the underside of the
    16T's teeth, 10.7 mm above the face (p.38)."""
    d = dd.Doc(1060, "Setting the 16T pulley with pulley_jig")
    top = step_header(d, "16T height: 10.7 mm")
    k = 15.0
    face_y = 860                  # motor face
    sx = 470                      # shaft centre x

    def H(h):                     # height above the motor face
        return face_y - h * k

    # motor: 42 mm square body, top part only, with its raised boss
    d.rect(sx - 21 * k, face_y, 42 * k, 150, fill=GREY_F, stroke=GREY, sw=3)
    d.rect(sx - 11 * k, H(2), 22 * k, 2 * k, fill=GREY_F, stroke=GREY, sw=2.5)
    d.text(sx - 21 * k + 20, face_y + 60, "Z motor", size=T_LAB, weight=700, fill=MUTED)
    # shaft
    d.rect(sx - 2.5 * k, H(26), 5 * k, 24 * k, fill=STEEL, stroke=GREY, sw=2.5)
    # 16T: lower flange 9.0-10.7, teeth 10.7-17.6, upper flange, collar to 25
    d.rect(sx - 7 * k, H(10.7), 14 * k, 1.7 * k, fill=GREY_F, stroke=GREY, sw=2.5)
    d.rect(sx - 5.2 * k, H(17.6), 10.4 * k, 6.9 * k, fill=GREY_F, stroke=GREY, sw=2.5)
    for i in range(1, 7):
        x = sx - 5.2 * k + i * 10.4 * k / 7
        d.line(x, H(17.6) + 3, x, H(10.7) - 3, stroke=GREY, sw=1.6)
    d.rect(sx - 7 * k, H(18.6), 14 * k, 1 * k, fill=GREY_F, stroke=GREY, sw=2.5)
    d.rect(sx - 8 * k, H(25.2), 16 * k, 6.6 * k, fill=GREY_F, stroke=GREY, sw=2.5)
    d.circle(sx, H(21.9), 1.5 * k, fill=PANEL, stroke=INK, sw=2.5)

    # jig: stood on its x = -18 edge, B tab hanging over the motor's edge, Z tab toward
    # the pulley. Jig y runs from the pulley outward (screen +x).
    jy0 = 32.15 + 7.3                            # shaft centre, in jig y (p.38: 7.3 mm gap)

    def J(x, y):
        return sx + (jy0 - y) * k, face_y - (x + 18) * k
    d.path(_path([J(x, y) for x, y in JIG]), fill=ORANGE_F, stroke=ORANGE, sw=3)
    zx, zy = J(-3.8, 28.8)
    d.text(zx, zy + 12, "Z", size=T_LAB, anchor="middle", weight=800, fill=ORANGE)
    bx, by = J(-20.75, 13)
    d.text(bx, by + 12, "B", size=T_MIN, anchor="middle", weight=800, fill=ORANGE)
    jx, jy = J(-2, 12)
    d.text(jx, jy, "pulley_jig", size=T_LAB, anchor="middle", weight=700, fill=ORANGE)

    # 10.7 mm dimension, face to the underside of the teeth (and of the Z tab)
    dx = sx - 13 * k
    d.line(dx - 20, H(10.7), sx - 5.2 * k, H(10.7), stroke=MUTED, sw=2, dash="6 5")
    _twoway(d, dx, H(10.7) + 3, dx, face_y - 3, col=INK, sw=3)
    d.text(dx - 18, (H(10.7) + face_y) / 2 + 12, "10.7 mm", size=T_LAB + 4, anchor="end",
           weight=800)

    # callouts: 1 count the teeth, 2 the Z tab, 3 the set screw on the flat
    callout(d, sx - 5.2 * k - 60, H(14.2), 1)
    callout(d, zx + 10, H(17.6) - 70, 2)
    callout(d, sx - 8 * k - 60, H(21.9), 3)
    y = legend_row(d, 50, 170, 1, ["count 16 teeth"])
    y = legend_row(d, 50, y + 26, 2, ["teeth level with the Z tab"])
    legend_row(d, 50, y + 26, 3, ["set screw on the flat"])
    return d


# ============================================================= diagram 207 ===
def d207_insert_map() -> dd.Doc:
    """02.04: where the 9 inserts per drive go. Flat faces as you look at them, the foot
    face (where the baseplate's three screws go) unfolded below each."""
    d = dd.Doc(1150, "Insert map: retainer and main body")
    top = step_header(d, "Inserts: 7 + 2 per drive")
    k = 7.0

    def part(ox, oy, loops, mirror_x, flip_y, thick, foot_y, title, sub):
        allp = [p for L in loops for p in L]
        x0, x1 = min(p[0] for p in allp), max(p[0] for p in allp)
        y0, y1 = min(p[1] for p in allp), max(p[1] for p in allp)

        def M(x, y):
            sxp = ox + ((x1 - x) if mirror_x else (x - x0)) * k
            syp = oy + ((y - y0) if flip_y else (y1 - y)) * k
            return sxp, syp
        outer = max(loops, key=len)
        d.path(_path([M(*p) for p in outer]), fill=BLACKPART_F, stroke=BLACKPART, sw=3)
        for L in loops:
            if L is not outer:
                d.path(_path([M(*p) for p in L]), fill=dd.BG, stroke=BLACKPART, sw=2.5)
        # the foot face, unfolded along its edge (thickness of the part)
        edge = [p[0] for p in outer if abs(p[1] - foot_y) < 1.6]
        fx0, fy0 = M(min(edge), foot_y)
        fx1, _ = M(max(edge), foot_y)
        lo, hi = min(fx0, fx1), max(fx0, fx1)
        d.rect(lo, fy0 + 12, hi - lo, thick * k, fill=BLACKPART_F, stroke=BLACKPART, sw=3,
               dash="10 6")
        d.text(ox, oy - 26, title, size=T_LAB + 2, weight=800)
        d.text(lo, fy0 + 12 + thick * k + 40, sub, size=T_MIN, weight=600, fill=MUTED)
        return M, fy0 + 12

    def insert(x, y, r=2.35 * k):
        d.circle(x, y, r + 3, fill=AMBER, stroke=INK, sw=2)
        d.circle(x, y, r * 0.5, fill=PANEL, stroke="none", sw=0)

    # retainer: flat face (the print face) as you look at it
    M, fy = part(50, 210, RET, True, False, 16.2, 85.0, "Retainer",
                 "foot face (baseplate side)")
    for x, y in RET_INSERTS:
        insert(*M(x, y))
    fx, _ = M(154, 85)
    insert(fx, fy + 5 * k)
    # main body
    M2, fy2 = part(640, 210, MAIN, False, True, 26.8, 144.5, "Main body",
                   "foot face (baseplate side)")
    for x, y in MAIN_CBORES:
        cx, cy = M2(x, y)
        d.circle(cx, cy, 3 * k, fill=dd.BG, stroke=OK, sw=4)
        d.circle(cx, cy, 1.7 * k, fill="none", stroke=OK, sw=2)
    for x in (130, 154):
        fx, _ = M2(x, 144.5)
        insert(fx, fy2 + 5 * k)

    callout(d, M(126, 114)[0], M(126, 114)[1], 1)
    callout(d, M2(126, 116)[0] - 4, M2(126, 116)[1], 2)
    y = legend_row(d, 60, 930, 1, ["7 in each retainer, 2 in each main body"])
    legend_row(d, 60, y + 26, 2, ["counterbores stay empty: screw heads go there"])
    d.circle(80, 1090, 16, fill=AMBER, stroke=INK, sw=2)
    d.text(110, 1101, "insert", size=T_MIN, weight=700)
    d.circle(300, 1090, 18, fill=dd.BG, stroke=OK, sw=4)
    d.text(330, 1101, "counterbore", size=T_MIN, weight=700)
    return d


_SCHEMATIC = ("Line weights, fills and the gaps between parts are schematic; every position "
              "and number comes from the sources named in the module docstring.")

DIAGRAMS = [
    {
        "n": 201,
        "file": "201-z-shaft-stack.svg",
        "title": "The Z drive shaft stack, in order",
        "fn": d201_shaft_stack,
        "shows": [
            "Side view of one 5x60 shaft, short end left: a 625 against the 20T's collar, "
            "the 20T (collar, teeth, flange), two spacers, a 625, two spacers, the 80T with "
            "its hub toward the 20T, and the last 625 on the long end (p.33 side view; CAD "
            "Z0 shaft assembly). The 33 mm runs from the long end to the 20T's flange "
            "(p.32). Callouts 1 to 3 are the Do numbers of Step 02.19.",
        ],
        "insert": [("02-z-drives.md", "Step 02.19", "the stack in order, first image")],
        "verify": [
            "Part widths along the shaft are from the 250 CAD (625 5 mm, 80T 18 mm incl. "
            "hub, 20T 20 mm incl. collar, 1 mm spacers); diameters of the 80T hub and the "
            "20T teeth are estimated from p.32-33. " + _SCHEMATIC,
        ],
    },
    {
        "n": 202,
        "file": "202-z-rail-holes-faces.svg",
        "title": "Z rails: which holes, which faces",
        "fn": d202_rail_holes_faces,
        "shows": [
            "Side view of one MGN9H 400 rail on its vertical: 20 holes numbered from the "
            "bottom, screws in 2, 4 ... 18, holes 1, 19 and 20 empty, the rail standing on "
            "the 3 mm hex key above the bottom horizontal (p.25).",
            "Plan view from above, front at the bottom: the front rails on the front "
            "verticals' back faces, the rear rails on the rear verticals' front faces, so "
            "the two on each side face each other (CAD, Step 02.09 render; p.27).",
        ],
        "insert": [
            ("02-z-drives.md", "Step 02.06", "holes, key and faces, first image"),
            ("02-z-drives.md", "Step 02.09", "faces, before the CAD renders"),
        ],
        "verify": [
            "Counting from the bottom is this manual's choice: p.25 starts its pattern at "
            "the bottom end hole and no source says which end of a 20-hole rail to leave "
            "two holes open at. Rail length, widths and the 3 mm gap are drawn schematic "
            "(the gap is exaggerated).",
        ],
    },
    {
        "n": 203,
        "file": "203-z0-corner-upside-down.svg",
        "title": "The Z0 corner with the printer upside down",
        "fn": d203_z0_corner,
        "shows": [
            "Plan from above with the printer upside down (rolled over sideways, as p.41's "
            "inset shows), standing at the FRONT tape: Z0 is on your right. The drive "
            "body's counterbored face faces outward over the side rail, its retainer face "
            "toward the motor; two M5x40 go into the side rail, the motor foot's two "
            "M5x10 into the front rail, 25 mm apart. Positions from the CAD Z0 corner.",
        ],
        "insert": [
            ("02-z-drives.md", "Step 02.29", "the corner, first image"),
            ("02-z-drives.md", "Step 02.30", "which rail takes which screws, first image"),
            ("02-z-drives.md", "Step 02.31", "which faces point where, first image"),
        ],
        "verify": [
            "Outlines are bounding boxes from the 250 CAD; the baseplate, foot and cam are "
            "left off so the faces and screws show. " + _SCHEMATIC,
        ],
    },
    {
        "n": 204,
        "file": "204-belt-tensioner-cam.svg",
        "title": "The belt tensioner cam in three stages",
        "fn": d204_cam_stages,
        "shows": [
            "From above, printer upside down, Z0 corner: the cam (outline from the STL) on "
            "its loose M5x10 under the motor foot's drive end. (a) Tab sticking straight "
            "out, (b) swinging toward the motor, (c) flat along the rail in the notch, the "
            "lobe pushing the foot about 2.5 mm away from the drive body (p.43-44; CAD "
            "closed position).",
        ],
        "insert": [
            ("02-z-drives.md", "Step 02.33", "where the cam sits, first image"),
            ("02-z-drives.md", "Step 02.34", "the swing, first image"),
        ],
        "verify": [
            "The 2.5 mm throw is the lobe's 12.5 mm reach (closed) less its 10 mm reach "
            "(open) toward the drive, from the STL; the surface it bears on and the foot's "
            "outline are schematic.",
        ],
    },
    {
        "n": 205,
        "file": "205-deck-clip-twist.svg",
        "title": "Fitting a deck clip: in end-first, then turn it",
        "fn": d205_deck_clip,
        "shows": [
            "Section along a bottom frame rail, printer upside down, deck panel below. (a) "
            "The clip goes in edge-on, its 5.8 mm thickness through the slot mouth. (b) "
            "Turned 90°: the head sits behind the slot's lips and the short end of the "
            "body lies over the panel's edge (outline from deck_support_3mm; the short "
            "end stops about 0.8 mm off a 3 mm panel). Callout 1 is Do 1 of Step 02.14.",
        ],
        "insert": [("02-z-drives.md", "Step 02.14", "the twist-in, first image")],
        "verify": [
            "No manual page or CAD shows the clips; the fit is worked out from the STL "
            "(key, body and which end is the short one) and the CAD deck position (panel "
            "top flush with the rail's top). Spacing along the rail stays 'verify on bench'.",
        ],
    },
    {
        "n": 206,
        "file": "206-16t-pulley-jig.svg",
        "title": "Setting the 16T pulley with pulley_jig",
        "fn": d206_pulley_jig,
        "shows": [
            "Side view after p.38: pulley_jig stood on the motor face with its B tab "
            "hooked over the motor's edge and its Z tab toward the pulley; the underside "
            "of the 16T's teeth level with the Z tab's underside, 10.7 mm above the motor "
            "face; collar up. Jig outline from the STL. Callouts 1 to 3 are the Do numbers "
            "of Step 02.27.",
        ],
        "insert": [("02-z-drives.md", "Step 02.27", "the jig in use, first image")],
        "verify": [
            "The 16T's flange, tooth band and collar heights are estimated from p.38; "
            "only the 10.7 mm is a given number.",
        ],
    },
    {
        "n": 207,
        "file": "207-z-drive-insert-map.svg",
        "title": "Insert map: retainer and main body",
        "fn": d207_insert_map,
        "shows": [
            "Both flat faces as you look at them (STL slice), with the foot face unfolded "
            "below each: the retainer's six inserts in its flat face and one in its foot "
            "face; the main body's six counterbores left empty and its two inserts in its "
            "foot face. The three foot-face inserts take the baseplate's M3x8 (CAD).",
        ],
        "insert": [("02-z-drives.md", "Step 02.04", "where the inserts go, first image")],
        "verify": [
            "Drawn from the _a parts; the _b parts are their mirror image. Window and "
            "outline shapes are 0.3 mm simplifications of the STL.",
        ],
    },
]
