"""Step diagrams for Chapter 07 (A/B belts), numbers 701 onwards.

Geometry sources: manual p.125-141, the 2.4r2 CAD index (~/.cache/voron-cad, 250
build; belt planes A z 80-86 / B z 70-76, front idler and XY-joint idler centres,
MGN12H block face), Voron docs § Secondary printer tuning (150 mm span, 110 Hz)
and the LDO 350 Rev D+ BOM (2000 mm per belt).
"""
import math

import draw_diagrams as dd

T_MIN, T_LAB = dd.T_MIN, dd.T_LAB


# ------------------------------------------------------------------ helpers ---
def belt_h(d, x0, x1, y, col, t=14, teeth=None, op=None):
    """A straight horizontal belt strip, y = its centre line. teeth = -1 marks the
    upper edge, +1 the lower edge, None no teeth."""
    xa, xb = sorted((x0, x1))
    d.rect(xa, y - t / 2, xb - xa, t, fill=col, stroke=col, sw=1, op=op)
    if teeth:
        ey = y + teeth * t / 2
        x = xa + 10
        while x < xb - 6:
            d.line(x, ey, x, ey + teeth * 7, stroke=col, sw=3, cap="butt", op=op)
            x += 16


def belt_v(d, x, y0, y1, col, t=14, teeth=None, op=None):
    """A straight vertical belt strip; teeth = -1 left edge, +1 right edge."""
    ya, yb = sorted((y0, y1))
    d.rect(x - t / 2, ya, t, yb - ya, fill=col, stroke=col, sw=1, op=op)
    if teeth:
        ex = x + teeth * t / 2
        y = ya + 10
        while y < yb - 6:
            d.line(ex, y, ex + teeth * 7, y, stroke=col, sw=3, cap="butt", op=op)
            y += 16


def arrow(d, x0, y0, x1, y1, col=dd.INK, sw=5, mk="arw", dash=None):
    d.path(f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}", stroke=col, sw=sw, marker=mk,
           dash=dash)


def turn_arrow(d, cx, cy, r, a0, a1, col=dd.ORANGE, sw=6, mk="arwo"):
    """Circular arrow from angle a0 to a1 (degrees, screen, clockwise positive)."""
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 1 if a1 > a0 else 0
    d.path(f"M {p0[0]:.1f} {p0[1]:.1f} A {r} {r} 0 {large} {sweep} {p1[0]:.1f} {p1[1]:.1f}",
           stroke=col, sw=sw, marker=mk)


def red_x(d, x, y, r=22):
    d.line(x - r, y - r, x + r, y + r, stroke=dd.RED, sw=7)
    d.line(x - r, y + r, x + r, y - r, stroke=dd.RED, sw=7)


# ============================================================ diagram 701 ===
def d701_fold_cut() -> dd.Doc:
    d = dd.Doc(900, "Cutting both belts to the same length by folding")
    top = dd.step_header(d, "Fold, then cut both at once")
    BK = dd.BLACKPART

    # --- the doubled belt, fold at the left, reel off to the right
    d.panel(30, top + 16, 1140, 450)
    xf, xe, xr = 150, 860, 1080            # fold, free end, reel
    yu, yl = top + 190, top + 236          # upper layer (free end), lower (to the reel)
    t = 16
    belt_h(d, xf, xe, yu, BK, t)
    belt_h(d, xf, xr - 40, yl, BK, t)
    r = (yl - yu) / 2
    d.path(f"M {xf} {yu - t / 2} A {r + t / 2} {r + t / 2} 0 0 0 {xf} {yl + t / 2} "
           f"L {xf} {yl - t / 2} A {r - t / 2} {r - t / 2} 0 0 1 {xf} {yu + t / 2} Z",
           fill=BK, stroke=BK, sw=1)
    d.circle(xr, yl - 6, 56, fill=dd.GREY_F, stroke=dd.GREY, sw=4)
    d.circle(xr, yl - 6, 16, fill=dd.PANEL, stroke=dd.GREY, sw=3)
    d.text(xr, yl - 80, "reel", size=T_LAB, anchor="middle", weight=700, fill=dd.MUTED)
    d.text(xe - 6, yu - 22, "free end", size=T_LAB, anchor="end", weight=700)
    d.text(xf + 4, yu - 22, "fold", size=T_LAB, anchor="start", weight=700)
    # 2000 mm along the upper layer
    dy = top + 112
    for x in (xf - r - t / 2, xe):
        d.line(x, dy - 14, x, yu - t / 2 - 6, stroke=dd.MUTED, sw=2)
    arrow(d, (xf + xe) / 2 - 90, dy, xf - r - t / 2 + 3, dy, dd.MUTED, 3, "arwm")
    arrow(d, (xf + xe) / 2 + 90, dy, xe - 3, dy, dd.MUTED, 3, "arwm")
    d.text((xf + xe) / 2, dy + 11, "2000 mm", size=36, anchor="middle", weight=800)
    dd.callout(d, (xf + xe) / 2 + 150, dy - 2, 1)
    # the two cuts
    for x in (xf - r - t / 2 + 8, xe):
        d.line(x, yu - 44 if x == xe else yu - 40, x, yl + 44, stroke=dd.RED, sw=5,
               dash="12 8")
    d.text(xe + 16, yl + 70, "cut level", size=T_LAB, weight=700, fill=dd.RED)
    d.text(xe + 16, yl + 108, "with the end", size=T_LAB, weight=700, fill=dd.RED)
    d.text(xf - r + 30, yl + 90, "cut the fold", size=T_LAB, weight=700, fill=dd.RED)
    dd.callout(d, xf - r - t / 2 + 8, yl + 150, 2)
    dd.callout(d, xe, yl + 150, 2)

    # --- two equal belts, A marked
    py = top + 486
    d.panel(30, py, 1140, d.h - py - 16)
    xa0, xa1 = 150, 860
    ya, yb = py + 110, py + 200
    belt_h(d, xa0, xa1, ya, BK, t)
    belt_h(d, xa0, xa1, yb, BK, t)
    for x in (xa0, xa1):
        d.line(x, ya - 40, x, yb + 40, stroke=dd.OK, sw=4, dash="10 8")
    for x in (xa0 + 40, xa1 - 40):
        d.circle(x, ya, 9, fill=dd.ORANGE, stroke=dd.PANEL, sw=2)
    d.text(xa0 - 24, ya + 11, "A", size=40, anchor="end", weight=800, fill=dd.BELT_A)
    d.text(xa0 - 24, yb + 11, "B", size=40, anchor="end", weight=800, fill=dd.BELT_B)
    dd.callout(d, xa0 + 110, ya - 52, 3)
    d.text(xa1 + 40, ya + 6, "dot near", size=T_LAB, weight=700)
    d.text(xa1 + 40, ya + 44, "each end", size=T_LAB, weight=700)
    d.text((xa0 + xa1) / 2, yb + 76, "ends flush at both ends", size=T_LAB,
           anchor="middle", weight=700, fill=dd.OK)
    return d


# ============================================================ diagram 702 ===
def d702_span() -> dd.Doc:
    """Top view of the right-hand front corner of the gantry, FRONT at the bottom,
    from the CAD (mm): front idler bearing (303, -7.5), its M3x40 on x 290 with the
    head at y -36; the right XY joint moved so its 20T idler sits 150 mm behind the
    front idler (289.9, 142.5) and its F695 pair at (303, 155.6)."""
    d = dd.Doc(1000, "The 150 mm span and the tensioner screw")
    top = dd.step_header(d, "Pluck the 150 mm span")
    k = 3.0
    X0, Y0 = 640 - k * 290, top + 40 + k * 185

    def P(x, y):
        return X0 + k * x, Y0 - k * y

    def box(x0, y0, x1, y1, **kw):
        a, b = P(x0, y0), P(x1, y1)
        d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], **kw)

    # Y extrusion and the X extrusion stub
    box(312, 190, 332, -8, fill=dd.BLUE_F, stroke=dd.BLUE, sw=3)
    box(150, 179, 262, 159, fill=dd.BLUE_F, stroke=dd.BLUE, sw=3)
    d.text(*P(152, 186), "X extrusion", size=T_MIN, weight=700, fill=dd.BLUE)
    # XY joint and front idler block (schematic outlines), the blue tension arm
    box(262, 182, 334, 133, fill="none", stroke=dd.BLACKPART, sw=3, rx=10, dash="10 7")
    box(284, 20, 334, -32.5, fill="none", stroke=dd.BLACKPART, sw=3, rx=10, dash="10 7")
    box(286, 3.5, 311, -14.5, fill=dd.ORANGE_F, stroke=dd.ORANGE, sw=3, rx=6)
    # M3x40 tensioner screw: head at the front, tip into the arm
    box(288.5, 7, 291.5, -33, fill=dd.GREY_F, stroke=dd.GREY, sw=2.5)
    box(286.5, -33, 293.5, -37, fill=dd.GREY, stroke=dd.INK, sw=2.5)

    # A belt (upper plane): outer run forward to the front idler, 180 deg round it,
    # inner run back to the joint's 20T idler, 90 deg round it towards the carriage
    rb, rt = 6.5, 6.4
    fx, fy = 303, -7.5
    jx, jy = 289.9, 142.5
    col, t = dd.BELT_A, 11
    xo, xi = fx + rb, fx - rb
    c, c2 = P(fx, fy), P(jx, jy)
    d.circle(*c, 7.5 * k, fill=dd.GREY_F, stroke=dd.GREY, sw=3)
    d.circle(*c, 2.5 * k, fill=dd.PANEL, stroke=dd.GREY, sw=2)
    d.circle(*c2, 8 * k, fill=dd.ORANGE_F, stroke=dd.ORANGE, sw=3)
    d.circle(*c2, 3 * k, fill="none", stroke=dd.ORANGE, sw=2, dash="4 3")
    o0, o1 = P(xo, 190), P(xo, fy)
    belt_v(d, o0[0], o0[1], o1[1], col, t, op=0.35)
    i0, i1 = P(xi, fy), P(xi, jy)
    belt_v(d, i0[0], i0[1], i1[1], col, t, teeth=-1)
    c = P(fx, fy)
    R = rb * k
    d.path(f"M {o1[0]:.1f} {o1[1]:.1f} A {R:.1f} {R:.1f} 0 0 1 {i0[0]:.1f} {i0[1]:.1f}",
           stroke=col, sw=t, cap="butt")
    c2 = P(jx, jy)
    R2 = rt * k
    e = P(jx, jy + rt)
    d.path(f"M {i1[0]:.1f} {i1[1]:.1f} A {R2:.1f} {R2:.1f} 0 0 0 {e[0]:.1f} {e[1]:.1f}",
           stroke=col, sw=t, cap="butt")
    l0 = P(150, jy + rt)
    belt_h(d, l0[0], e[0], e[1], col, t, teeth=+1)

    # 150 mm between the two centres
    xd = P(236, 0)[0]
    for x, y in ((fx, fy), (jx, jy)):
        p = P(x, y)
        d.line(xd - 14, p[1], p[0], p[1], stroke=dd.MUTED, sw=2, dash="8 6")
    p0, p1 = P(0, fy), P(0, jy)
    mid = (p0[1] + p1[1]) / 2
    arrow(d, xd, mid + 60, xd, p0[1] - 3, dd.INK, 3.5, "arw")
    arrow(d, xd, mid - 60, xd, p1[1] + 3, dd.INK, 3.5, "arw")
    d.line(xd, mid - 60, xd, mid + 60, stroke=dd.INK, sw=3.5)
    d.text(xd - 18, mid + 4, "150 mm", size=40, anchor="end", weight=800)
    d.text(xd - 18, mid + 44, "centre to centre", size=T_MIN, anchor="end", weight=600,
           fill=dd.MUTED)
    # right-hand labels
    lx = P(332, 0)[0] + 30
    d.text(lx, P(0, 150)[1] + 10, "XY joint", size=T_LAB, weight=700)
    d.text(lx, P(0, 0)[1] + 10, "front idler", size=T_LAB, weight=700)
    pm = P(xi, 75)
    d.leader(pm[0] - 8, pm[1], lx - 6, pm[1] - 20, col=dd.BELT_A)
    d.text(lx, pm[1] - 30, "pluck", size=T_LAB, weight=800, fill=dd.BELT_A)
    d.text(lx, pm[1] + 8, "this run", size=T_LAB, weight=800, fill=dd.BELT_A)

    # the tensioner screw: in = tighter, out = looser
    h = P(290, -37)
    turn_arrow(d, h[0], h[1] + 40, 30, 200, 500, dd.OK, 5, "arwg")
    d.text(h[0] - 60, h[1] + 40, "screw in:", size=T_LAB, anchor="end", weight=700)
    d.text(h[0] - 60, h[1] + 78, "tighter", size=T_LAB, anchor="end", weight=800,
           fill=dd.OK)
    d.text(h[0] + 60, h[1] + 40, "out:", size=T_LAB, weight=700)
    d.text(h[0] + 60, h[1] + 78, "looser", size=T_LAB, weight=800, fill=dd.MUTED)
    d.text(1150, top + 66, "FRONT at the bottom", size=T_MIN, anchor="end", weight=700,
           fill=dd.MUTED)
    dd.step_note(d, "Same on the left, with the B belt.", size=T_LAB)
    return d


# ============================================================ diagram 703 ===
def d703_clamp_section() -> dd.Doc:
    """Section through the X carriage, looking along the X extrusion from its left
    end, FRONT to the left. CAD (mm): extrusion y 173-193 / z 68-88, MGN12H block
    front face y 160 (z 64-91), belts against it y 158.6-160 at z 80-86 (A) and
    70-76 (B), carriage half front y 143.5, M3x8 at z 68 and 88."""
    d = dd.Doc(900, "Belt clamp slots in section: A upper, B lower")
    top = dd.step_header(d, "Belt slots: A upper, B lower")
    k = 10.5
    X0, Y0 = 520, top + 730

    def P(y, z):
        return X0 + k * (y - 140), Y0 - k * (z - 35)

    # X extrusion section (2020), rail, rail carriage block
    c = P(183, 78)
    dd.profile2020(d, c[0], c[1], k)
    a, b = P(165, 84), P(173, 72)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=dd.STEEL, stroke=dd.GREY, sw=2.5)
    a, b = P(159.9, 91.4), P(170, 64.4)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=dd.GREY_F, stroke=dd.GREY, sw=3, rx=4)
    # carriage half (schematic): front wall plus top and bottom lips
    a, b = P(143.5, 100), P(158.4, 40)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=dd.BLACKPART_F, stroke=dd.BLACKPART,
           sw=3, rx=6)
    # belts, teeth to the front (away from the extrusion)
    for z0, col in ((80, dd.BELT_A), (70, dd.BELT_B)):
        a, b = P(157.6, z0 + 6), P(160, z0)          # thickness drawn ~2x
        d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=col, stroke=col, sw=1)
        for i in range(4):
            y = a[1] + 8 + i * (b[1] - a[1] - 16) / 3
            d.line(a[0], y, a[0] - 14, y, stroke=col, sw=6, cap="butt")
    # M3x8 clamp screws through the half into the block
    for z in (67.9, 87.9):
        a, b = P(155.5, z + 1.5), P(163.5, z - 1.5)
        d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=dd.GREY_F, stroke=dd.GREY, sw=2)
        a, b = P(152.5, z + 2.75), P(155.5, z - 2.75)
        d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=dd.GREY, stroke=dd.INK, sw=2)

    # labels, left column
    for z, col, name, slot in ((83, dd.BELT_A, "A belt:", "upper slot"),
                               (73, dd.BELT_B, "B belt:", "lower slot")):
        p = P(157.6, z)
        d.leader(p[0] - 16, p[1], 470, p[1] - 4, col=col)
        d.text(40, p[1] - 8 if z > 78 else p[1] + 4, name, size=T_LAB, weight=800,
               fill=col)
        d.text(170, p[1] - 8 if z > 78 else p[1] + 4, slot, size=T_LAB, weight=700)
    ta, tb = P(158, 60), P(144, 60)
    arrow(d, ta[0], ta[1], tb[0] - 80, tb[1], dd.ORANGE, 6, "arwo")
    d.text(40, ta[1] + 60, "teeth face away from", size=T_LAB, weight=800,
           fill=dd.ORANGE)
    d.text(40, ta[1] + 98, "the extrusion", size=T_LAB, weight=800, fill=dd.ORANGE)
    q = P(173, 89)
    d.text(q[0], q[1] - 16, "extrusion", size=T_LAB, weight=700, fill=dd.BLUE)
    q = P(160, 64.4)
    d.text(q[0] + 20, q[1] + 44, "rail carriage", size=T_MIN, weight=700, fill=dd.MUTED)
    q = P(143.5, 40)
    d.text(q[0], q[1] + 44, "X carriage half", size=T_MIN, weight=700)
    d.text(40, top + 66, "FRONT to the left", size=T_MIN, weight=700, fill=dd.MUTED)
    return d


# ============================================================ diagram 704 ===
def d704_tails() -> dd.Doc:
    """Front view of the closed X carriage, after p.141: both belts enter the right
    half from the right at their own heights and turn down in the seam; the two
    tails stick out below the carriage."""
    d = dd.Doc(980, "Pull both tails until they stick out the same length")
    top = dd.step_header(d, "Same length on both tails")
    BK, BKF = dd.BLACKPART, dd.BLACKPART_F
    d.panel(30, top + 16, 780, d.h - top - 32)

    cx0, cx1, cy0, cy1 = 140, 560, top + 70, top + 520
    seam = 350
    for x0, x1 in ((cx0, seam - 6), (seam + 6, cx1)):
        d.rect(x0, cy0, x1 - x0, cy1 - cy0, fill=BKF, stroke=BK, sw=3, rx=10)
    d.text((cx0 + seam) / 2, cy0 + 60, "left half", size=T_MIN, anchor="middle",
           weight=700, fill=dd.MUTED)
    d.text((seam + cx1) / 2, cy0 + 60, "right half", size=T_MIN, anchor="middle",
           weight=700, fill=dd.MUTED)
    t = 16
    yA, yB = top + 200, top + 290
    xa, xb = seam + 12, seam + 34                 # tail lanes in the seam (schematic)
    tail_end = top + 700
    for y, x, col in ((yA, xa, dd.BELT_A), (yB, xb, dd.BELT_B)):
        belt_h(d, x, 800, y, col, t, op=None)
        belt_v(d, x, y - t / 2, tail_end, col, t)
    d.text(790, yA - 18, "A", size=36, anchor="end", weight=800, fill=dd.BELT_A)
    d.text(790, yB - 18, "B", size=36, anchor="end", weight=800, fill=dd.BELT_B)
    # pull arrows
    for x in (xa, xb):
        arrow(d, x, tail_end + 8, x, tail_end + 70, dd.ORANGE, 6, "arwo")
    dd.callout(d, xb + 70, tail_end + 50, 1)
    # the rule beside the tails and the matching ends
    rx = 220
    d.rect(rx - 26, cy1 + 4, 52, tail_end - cy1 + 20, fill=dd.STEEL, stroke=dd.GREY, sw=2.5,
           rx=3)
    for i in range(0, int(tail_end - cy1 + 14), 14):
        L = 20 if i % 70 == 0 else 10
        d.line(rx + 26 - L, cy1 + 8 + i, rx + 26, cy1 + 8 + i, stroke=dd.INK, sw=2)
    for y in (cy1, tail_end):
        d.line(rx + 26, y, xb + 30, y, stroke=dd.OK, sw=3, dash="10 7")
    d.text(rx - 40, (cy1 + tail_end) / 2 + 10, "rule", size=T_LAB, anchor="end",
           weight=700, fill=dd.MUTED)
    d.text(xb + 40, tail_end - 40, "same", size=T_LAB, weight=800, fill=dd.OK)
    d.text(xb + 40, tail_end - 4, "length", size=T_LAB, weight=800, fill=dd.OK)

    # right column: what the numbers mean, and a small wrong case
    ox = 830
    d.panel(ox, top + 16, 340, d.h - top - 32)
    y = dd.legend_row(d, ox + 20, top + 90, 1, ["pull both", "tails tight"])
    dd.legend_row(d, ox + 20, y + 36, 2, ["A, then B,", "then A again"])
    d.text(ox + 24, top + 430, "Not yet", size=38, weight=700, fill=dd.RED)
    bx, by = ox + 120, top + 470
    belt_v(d, bx, by, by + 220, dd.BELT_A, 14)
    belt_v(d, bx + 34, by, by + 150, dd.BELT_B, 14)
    d.line(bx - 20, by + 150, bx + 60, by + 150, stroke=dd.RED, sw=3, dash="8 6")
    d.line(bx - 20, by + 220, bx + 60, by + 220, stroke=dd.RED, sw=3, dash="8 6")
    red_x(d, bx + 140, by + 60)
    return d


# ============================================================ diagram 705 ===
def d705_move_return() -> dd.Doc:
    d = dd.Doc(950, "Move the gantry away, return to the 150 mm span, measure again")
    top = dd.step_header(d, "Away, back, measure again")
    F0, F1 = 150, 650                      # frame left/right on screen
    yR, yF = top + 70, top + 770           # rear / front of the drawing
    for x in (F0, F1 - 30):
        d.rect(x, yR, 30, yF - yR, fill=dd.BLUE_F, stroke=dd.BLUE, sw=3)
    d.text((F0 + F1) / 2, yF + 50, "FRONT", size=T_LAB, anchor="middle", weight=800,
           fill=dd.BLUE)
    yI = yF - 60                           # front idlers
    for x in (F0 + 15, F1 - 15):
        d.circle(x, yI, 22, fill=dd.GREY_F, stroke=dd.GREY, sw=3)
    y150 = yI - 300                        # the measuring position
    yAway = y150 - 190                     # a few centimetres further back
    d.rect(F0 + 30, yAway - 15, F1 - F0 - 60, 30, fill="none", stroke=dd.BLUE, sw=3,
           dash="12 8")
    d.rect(F0 + 30, y150 - 15, F1 - F0 - 60, 30, fill=dd.BLUE_F, stroke=dd.BLUE, sw=3)
    d.text((F0 + F1) / 2, y150 - 30, "X extrusion", size=T_MIN, anchor="middle",
           weight=700, fill=dd.BLUE)
    # back, then forward again
    xa = (F0 + F1) / 2 - 70
    arrow(d, xa, y150 - 60, xa, yAway + 24, dd.ORANGE, 7, "arwo")
    arrow(d, xa + 140, yAway + 24, xa + 140, y150 - 60, dd.ORANGE, 7, "arwo")
    dd.callout(d, xa + 70, (y150 + yAway) / 2 - 20, 1)
    # 150 mm on both sides
    for x in (F0 + 60, F1 - 60):
        arrow(d, x, (y150 + yI) / 2, x, y150 + 20, dd.INK, 3.5)
        arrow(d, x, (y150 + yI) / 2, x, yI - 26, dd.INK, 3.5)
    d.text((F0 + F1) / 2, (y150 + yI) / 2 + 12, "150 mm", size=36, anchor="middle",
           weight=800)
    dd.callout(d, (F0 + F1) / 2, (y150 + yI) / 2 + 76, 2)
    y = dd.legend_row(d, 720, top + 250, 1, ["back a few cm,", "then forward", "to 150 mm"])
    dd.legend_row(d, 720, y + 50, 2, ["pluck and read", "both belts again"])
    return d


# ============================================================ diagram 706 ===
def d706_tensioner_turns() -> dd.Doc:
    """Front idler from above, FRONT at the bottom (schematic, after p.128 and the
    CAD): the M3x40 enters through the front wall, its head against the washer,
    and threads into the insert at the back of the blue tension arm that carries
    the bearing stack. Turning it in pulls the arm forward."""
    d = dd.Doc(900, "Front-idler tensioner: back it out, then 4 turns in")
    top = dd.step_header(d, "Out to the end, then 4 turns in")

    def idler(ox, arm_dy, title, n):
        d.panel(ox, top + 16, 555, d.h - top - 32)
        d.text(ox + 24, top + 70, title, size=36, weight=700)
        cx = ox + 300
        wall = top + 640                                  # front wall, outer face
        d.rect(cx - 150, top + 170, 300, wall - top - 170, fill="none",
               stroke=dd.BLACKPART, sw=4, rx=16, dash="12 8")
        d.line(cx - 150, wall - 34, cx + 150, wall - 34, stroke=dd.BLACKPART, sw=3)
        # arm with its bearing, moved by arm_dy
        ay0 = top + 300 + arm_dy
        d.rect(cx - 120, ay0, 230, 190, fill=dd.ORANGE_F, stroke=dd.ORANGE, sw=3, rx=10)
        d.circle(cx + 40, ay0 + 95, 62, fill=dd.GREY_F, stroke=dd.GREY, sw=3)
        d.circle(cx + 40, ay0 + 95, 18, fill=dd.PANEL, stroke=dd.GREY, sw=2.5)
        # screw: head against the washer on the front wall, tip into the arm's back
        sx = cx - 80
        d.rect(sx - 10, ay0 - 20, 20, wall - ay0 + 20, fill=dd.GREY_F, stroke=dd.GREY,
               sw=2.5)
        d.rect(sx - 26, wall + 4, 52, 6, fill=dd.STEEL, stroke=dd.GREY, sw=2)
        d.rect(sx - 24, wall + 10, 48, 34, fill=dd.GREY, stroke=dd.INK, sw=2.5, rx=4)
        d.text(cx + 40, top + 155, "bearing stack", size=T_MIN, anchor="middle",
               weight=700, fill=dd.MUTED)
        dd.callout(d, sx - 70, wall + 30, n)
        return cx, sx, wall, ay0

    cx, sx, wall, ay0 = idler(30, -60, "Out to the end", 1)
    arrow(d, cx + 185, ay0 + 150, cx + 185, ay0 + 60, dd.MUTED, 6, "arwm")
    d.text(sx + 40, wall + 40, "unscrew", size=T_LAB, weight=700, fill=dd.MUTED)
    d.text(cx - 230, wall + 140, "arm slides back", size=T_MIN, weight=700, fill=dd.MUTED)
    cx, sx, wall, ay0 = idler(615, 0, "4 turns in", 2)
    arrow(d, cx + 185, ay0 + 60, cx + 185, ay0 + 150, dd.OK, 6, "arwg")
    d.text(sx + 40, wall + 40, "4 turns", size=T_LAB, weight=800, fill=dd.OK)
    d.text(cx - 230, wall + 140, "arm pulled forward", size=T_MIN, weight=700,
           fill=dd.OK)
    d.text(1150, 66, "FRONT at the bottom", size=T_MIN, anchor="end", weight=700,
           fill=dd.MUTED)
    return d


# ================================================================ registry ===
DIAGRAMS = [
    {
        "n": 701,
        "file": "701-belt-fold-cut.svg",
        "title": "Fold, then cut both at once",
        "fn": d701_fold_cut,
        "shows": [
            "The belt folded back on itself 2000 mm from its free end (callout 1), the "
            "cut through the fold and the cut through the reel side level with the free "
            "end (callouts 2), and the two equal belts with dots near each end of A "
            "(callout 3). Callouts are the Do numbers of Step 07.8.",
        ],
        "insert": [
            ("07-ab-belts.md", "Step 07.8", "replaces the no-image placeholder"),
        ],
        "verify": [
            "Lengths are not to scale; 2000 mm per belt is from the LDO 350 Rev D+ BOM "
            "(6.21 m of 6 mm belt) and onetwo3D's 350 BOM (2 x 2000 mm).",
        ],
    },
    {
        "n": 702,
        "file": "702-belt-span-150.svg",
        "title": "Pluck the 150 mm span",
        "fn": d702_span,
        "shows": [
            "Top view of the right front corner of the gantry, FRONT at the bottom: the "
            "A belt's inner run between the XY joint's toothed idler and the front "
            "idler, 150 mm centre to centre, marked as the run to pluck; the outer run "
            "drawn faint.",
            "The front-idler M3x40 head at the front: screw in = tighter, out = looser. "
            "The left side is the mirror, with the B belt.",
        ],
        "insert": [
            ("07-ab-belts.md", "Step 07.30", "first, before the two CAD renders"),
            ("07-ab-belts.md", "Step 07.32", "replaces the no-image placeholder"),
        ],
        "verify": [
            "Positions are from the 2.4r2 CAD (250 build) with the XY joint moved to the "
            "150 mm position; the joint and idler bodies are drawn as dashed outlines.",
            "Which run is plucked is derived: only the inner run has a free length "
            "between those two centres (the outer run passes the joint).",
        ],
    },
    {
        "n": 703,
        "file": "703-belt-clamp-section.svg",
        "title": "Belt slots: A upper, B lower",
        "fn": d703_clamp_section,
        "shows": [
            "Section through the X carriage looking along the X extrusion, FRONT to the "
            "left: extrusion, rail, rail carriage, the A belt in the upper slot and the "
            "B belt in the lower one lying against the rail carriage's face, teeth "
            "towards the front, away from the extrusion, and the two M3x8 above and "
            "below them.",
        ],
        "insert": [
            ("07-ab-belts.md", "Step 07.9", "second, after the p.131 crop"),
            ("07-ab-belts.md", "Step 07.24", "second, after the p.139 crop"),
        ],
        "verify": [
            "Belt heights (A z 80-86, B z 70-76), the rail carriage face and the M3x8 "
            "heights are from the CAD; the carriage half is drawn as a plain block, its "
            "slot shapes are not.",
        ],
    },
    {
        "n": 704,
        "file": "704-belt-tails-equal.svg",
        "title": "Same length on both tails",
        "fn": d704_tails,
        "shows": [
            "Front view of the closed X carriage after p.141: both belts enter the right "
            "half from the right at their own heights, turn down in the seam and stick "
            "out below; a rule beside them shows both tails ending at the same mark. "
            "Callouts are the Do numbers of Step 07.27. A small red case shows unequal "
            "tails.",
        ],
        "insert": [
            ("07-ab-belts.md", "Step 07.27", "first, before the p.141 crop"),
        ],
        "verify": [
            "Which tail sits nearer the seam, and the tail lengths, are schematic.",
        ],
    },
    {
        "n": 705,
        "file": "705-gantry-away-and-back.svg",
        "title": "Away, back, measure again",
        "fn": d705_move_return,
        "shows": [
            "Top view: the X extrusion moved back a few centimetres (dashed) and forward "
            "again to 150 mm from the front idlers on both sides (callout 1), then both "
            "belts read again (callout 2), the Do numbers of Step 07.33.",
        ],
        "insert": [
            ("07-ab-belts.md", "Step 07.33", "replaces the no-image placeholder"),
        ],
        "verify": [
            "Schematic frame; distances are not to scale.",
        ],
    },
    {
        "n": 706,
        "file": "706-tensioner-four-turns.svg",
        "title": "Out to the end, then 4 turns in",
        "fn": d706_tensioner_turns,
        "shows": [
            "A front idler from above, FRONT at the bottom: the M3x40 through the front "
            "wall, head on its washer, threaded into the back of the blue tension arm "
            "that carries the bearing stack. Callout 1: screw backed out, arm slid back "
            "to the end of its travel. Callout 2: 4 turns in, arm pulled forward. The "
            "Do numbers of Step 07.5.",
        ],
        "insert": [
            ("07-ab-belts.md", "Step 07.5", "first, before the p.128 crop"),
        ],
        "verify": [
            "Schematic block and arm shapes; the screw path (front wall, insert at the "
            "rear of the arm) is from the CAD and p.128's section.",
        ],
    },
]
