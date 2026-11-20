"""Chapter 05 (gantry) step-column diagrams, 501 onwards.

Geometry sources: Voron 2.4r2 manual p.89, p.90, p.97, p.99, p.101, p.102, p.106, p.164 at
de7e89d, and the Voron 2.4r2 CAD (250 size, ~/.cache/voron-cad index): T-nut slots and their
order at the extrusion ends, the XY joint / carriage / endstop pod stack, and which carriage
holes take the M3x16 and the M3x30. Lengths are this kit's 350 set (C 450, D 430, rails 400).
"""
import math

import draw_diagrams as dd
from draw_diagrams import (BELT_A, BELT_B, BLACKPART, BLACKPART_F, BLUE, BLUE_F, GREY, GREY_F,
                           INK, MUTED, OK, ORANGE, ORANGE_F, PANEL, RED, STEEL, AMBER, AMBER_F,
                           FAINT, Doc, T_LAB, T_MIN, callout, label_bg, legend_row, profile2020,
                           step_header, step_note)

TI = "#8E97A3"          # titanium backer, a cooler grey than the hardware
TI_F = "#D5DAE0"


# ------------------------------------------------------------------ helpers ---
def _rot(x, y, r):
    """Rotate (x, y) by r quarter turns clockwise on screen."""
    for _ in range(r % 4):
        x, y = -y, x
    return x, y


def tnut_end(d: Doc, cx, cy, k, face, col=GREY, fill=GREY_F):
    """A roll-in T-nut seen end-on, sitting in the slot of `face` (0 top, 1 right,
    2 bottom, 3 left) of a 2020 section centred on (cx, cy), k px per mm."""
    pts = [(-4.9, -8.0), (4.9, -8.0), (4.9, -6.9), (2.6, -4.3), (-2.6, -4.3), (-4.9, -6.9)]
    out = []
    for x, y in pts:
        x, y = _rot(x, y, face)
        out.append((cx + x * k, cy + y * k))
    d.poly(out, fill=fill, stroke=col, sw=2.5)


def strip_on_face(d: Doc, cx, cy, k, face, width, thick, fill, stroke, gap=0.0):
    """A flat part lying on `face` of a 2020 section: `width` mm along the face,
    `thick` mm proud of it."""
    x0, x1 = -width / 2, width / 2
    y0, y1 = -10 - gap - thick, -10 - gap
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    pts = []
    for x, y in corners:
        x, y = _rot(x, y, face)
        pts.append((cx + x * k, cy + y * k))
    d.poly(pts, fill=fill, stroke=stroke, sw=2.5)
    return pts


def rail_on_face(d: Doc, cx, cy, k, face, w, h):
    """An MGN rail section on `face`: w mm wide, h mm tall."""
    strip_on_face(d, cx, cy, k, face, w, h, fill=STEEL, stroke=GREY)


def carriage_on_face(d: Doc, cx, cy, k, face, cw, H, rw, rh):
    """An MGN carriage seen end-on, straddling a rail (rw x rh) on `face`: cw mm wide,
    its top H mm off the extrusion face, its underside 1.5 mm clear of the face."""
    a, c = -10 - 1.5, -10 - H
    r0, r1 = -rw / 2 - 0.6, rw / 2 + 0.6
    local = [(-cw / 2, a), (r0, a), (r0, -10 - rh - 0.6), (r1, -10 - rh - 0.6), (r1, a),
             (cw / 2, a), (cw / 2, c), (-cw / 2, c)]
    pts = []
    for x, y in local:
        x, y = _rot(x, y, face)
        pts.append((cx + x * k, cy + y * k))
    d.poly(pts, fill=GREY_F, stroke=GREY, sw=2.5)


def arrow(d: Doc, x0, y0, x1, y1, col=INK, sw=5, mk="arw"):
    d.path(f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}", stroke=col, sw=sw, marker=mk)


def red_x(d: Doc, x, y, r=24, sw=7):
    d.line(x - r, y - r, x + r, y + r, stroke=RED, sw=sw)
    d.line(x - r, y + r, x + r, y - r, stroke=RED, sw=sw)


def shcs_v(d: Doc, x, y_head_top, k, length, head_up=True, col=GREY, fill=GREY_F,
           d_thread=3.0, head_d=5.5, head_h=3.0, solid=None, dash_from=None):
    """Socket-head screw in side view, vertical. head_up: head on top, shank going down."""
    s = 1 if head_up else -1
    hy0 = y_head_top
    hy1 = y_head_top + s * head_h * k
    d.rect(x - head_d / 2 * k, min(hy0, hy1), head_d * k, head_h * k, fill=fill, stroke=col,
           sw=2.5, rx=3)
    d.rect(x - 0.9 * k, min(hy0, hy1) + (0.6 * k if head_up else head_h * k - 1.6 * k),
           1.8 * k, 1.0 * k, fill=col, stroke="none", sw=0)          # the socket
    sy1 = hy1 + s * length * k
    if dash_from is None:
        d.rect(x - d_thread / 2 * k, min(hy1, sy1), d_thread * k, abs(sy1 - hy1), fill=fill,
               stroke=col, sw=2.5)
    else:
        mid = hy1 + s * dash_from * k
        d.rect(x - d_thread / 2 * k, min(hy1, mid), d_thread * k, abs(mid - hy1), fill=fill,
               stroke=col, sw=2.5)
        d.rect(x - d_thread / 2 * k, min(mid, sy1), d_thread * k, abs(sy1 - mid), fill="none",
               stroke=col, sw=2.5, dash="8 6")
    return sy1


# ============================================================== diagram 501 ===
def d501_x_extrusion_tnuts() -> Doc:
    """Step 05.36: the D extrusion's six M5 T-nuts, end view and front view."""
    d = Doc(1064, "X extrusion: which slot takes the M5 T-nuts")
    top = step_header(d, "X extrusion: M5 T-nuts")

    # ---- end view, left
    d.panel(30, top + 16, 540, 520)
    d.text(54, top + 66, "End view", size=T_LAB, weight=700, fill=MUTED)
    k = 12.0
    cx, cy = 300, top + 270
    profile2020(d, cx, cy, k)
    rail_on_face(d, cx, cy, k, 3, 12, 8)               # MGN12 on the front (left) face
    strip_on_face(d, cx, cy, k, 1, 18, 2.5, fill=TI_F, stroke=TI)   # backer, rear face
    tnut_end(d, cx, cy, k, 0, col=INK, fill=ORANGE_F)  # top slot
    tnut_end(d, cx, cy, k, 2, col=INK, fill=ORANGE_F)  # bottom slot
    callout(d, cx + 66, cy - 186, 1)
    d.leader(cx + 30, cy - 84, cx + 56, cy - 160, col=INK)
    callout(d, cx + 66, cy + 186, 2)
    d.leader(cx + 30, cy + 84, cx + 56, cy + 160, col=INK)
    ly = cy + 205
    d.text(cx - 14 * k, ly, "FRONT", size=T_LAB, anchor="middle", weight=800, fill=BLUE)
    d.text(cx - 14 * k, ly + 40, "rail", size=T_LAB, anchor="middle", weight=700)
    d.text(cx + 13 * k, ly, "REAR", size=T_LAB, anchor="middle", weight=800, fill=BLUE)
    d.text(cx + 13 * k, ly + 40, "backer", size=T_LAB, anchor="middle", weight=700)

    # ---- legend, right
    y = legend_row(d, 610, top + 150, 1, ["top slot:", "2 at each end"])
    y = legend_row(d, 610, y + 60, 2, ["bottom slot:", "1 at each end"])
    d.text(610, y + 70, "Nothing goes in the", size=T_LAB, weight=600, fill=MUTED)
    d.text(610, y + 110, "rail or backer slots.", size=T_LAB, weight=600, fill=MUTED)

    # ---- front view, along the bottom (430 mm D, 400 mm rail, 15 mm each end)
    py = top + 556
    d.panel(30, py, 1140, d.h - py - 16)
    d.text(54, py + 50, "From the front, nuts lifted out", size=T_LAB, weight=700,
           fill=MUTED)
    s = 2.4                                            # px per mm along the length
    x0 = (d.w - 430 * s) / 2
    h = 20 * 5.0                                       # 20 mm tall, drawn 5 px/mm
    ey = py + 170
    d.rect(x0, ey, 430 * s, h, fill=BLUE_F, stroke=BLUE, sw=3)
    d.rect(x0 + 15 * s, ey + h / 2 - 6 * 5, 400 * s, 12 * 5, fill=STEEL, stroke=GREY, sw=2.5)
    d.text(d.w / 2, ey + h / 2 + 11, "MGN12 rail", size=T_MIN, anchor="middle", weight=700)
    nw, nh, lift = 13 * s, 22, 16
    # CAD: top slot nuts 2-15 and 17-30 mm from each end; the bottom single under the outer one
    for end in (0, 1):
        for a in (2, 17):
            xa = x0 + a * s if end == 0 else x0 + (430 - a - 13) * s
            d.rect(xa, ey - nh - lift, nw, nh, fill=ORANGE_F, stroke=INK, sw=2.5, rx=3)
        xb = x0 + 2 * s if end == 0 else x0 + (430 - 15) * s
        d.rect(xb, ey + h + lift, nw, nh, fill=ORANGE_F, stroke=INK, sw=2.5, rx=3)
    for xm in (x0 + 16 * s, x0 + (430 - 16) * s):
        callout(d, xm, ey - nh - lift - 42, 1)
        callout(d, xm, ey + h + nh + lift + 42, 2)
    d.text(d.w / 2, ey - 40, "top", size=T_MIN, anchor="middle", weight=700, fill=MUTED)
    d.text(d.w / 2, ey + h + 52, "bottom", size=T_MIN, anchor="middle", weight=700,
           fill=MUTED)
    return d


# ============================================================== diagram 502 ===
def d502_y_extrusion_end() -> Doc:
    """Step 05.14: one end of a C extrusion, the way it sits in the machine."""
    d = Doc(790, "Y extrusion end: the four T-nuts")
    top = step_header(d, "Y extrusion end: four T-nuts")

    # ---- small end view on the left
    k = 7.0
    ecx, ecy = 150, top + 230
    profile2020(d, ecx, ecy, k)
    rail_on_face(d, ecx, ecy, k, 2, 9, 6.5)          # MGN9 underneath
    d.text(ecx, ecy - 10 * k - 70, "top slot", size=T_LAB, anchor="middle", weight=700)
    d.line(ecx, ecy - 10 * k - 50, ecx, ecy - 9 * k, stroke=INK, sw=2)
    d.text(ecx, ecy + 17 * k + 50, "rail slot", size=T_LAB, anchor="middle", weight=700)
    d.text(ecx, ecy + 17 * k + 90, "underneath", size=T_MIN, anchor="middle", fill=MUTED)

    # ---- side view of the end, extrusion end at the left, 9 px/mm
    s = 9.0
    x0 = 330                                          # the extrusion's end face
    L = 92                                            # mm shown
    yt = top + 140                                    # top face
    h = 20 * s
    d.rect(x0, yt, L * s, h, fill=BLUE_F, stroke=BLUE, sw=3)
    xr = x0 + L * s                                   # broken edge: it carries on
    d.path(f"M {xr} {yt - 8} L {xr - 14} {yt + h * 0.35} L {xr + 10} {yt + h * 0.65} "
           f"L {xr} {yt + h + 8}", stroke=BLUE, sw=3)
    for yy in (yt + 3.1 * s, yt + h - 3.1 * s):      # top and bottom slot lines
        d.line(x0 + 3, yy, xr - 6, yy, stroke=BLUE, sw=1.6, op=0.55)
    nh = 4.3 * s
    # top slot: two M5 from Step 05.13, 2-15 and 17.5-30.5 mm in (CAD)
    for a in (2.0, 17.5):
        d.rect(x0 + a * s, yt + 1.6 * s, 13 * s, nh, fill=GREY_F, stroke=GREY, sw=2.5, rx=3)
        d.text(x0 + (a + 6.5) * s, yt + 1.6 * s + nh / 2 + 11, "M5", size=T_MIN,
               anchor="middle", weight=700, fill=MUTED)
    d.text(x0 + 16 * s, yt - 22, "2 M5 already in", size=T_MIN, anchor="middle", weight=600,
           fill=MUTED)
    # rail slot: M5 outermost (2-15 mm), M3 just inside (17-29.5 mm); rail from 25 mm
    ry = yt + h                                       # rail face
    d.rect(x0 + 25 * s, ry, (L - 25) * s - 8, 6.5 * s, fill=STEEL, stroke=GREY, sw=2.5)
    d.text(x0 + 66 * s, ry + 6.5 * s + 42, "rail", size=T_LAB, anchor="middle", weight=700)
    by = ry - 1.6 * s - nh
    d.rect(x0 + 2 * s, by, 13 * s, nh, fill=ORANGE_F, stroke=INK, sw=3, rx=3)
    d.text(x0 + 8.5 * s, by + nh / 2 + 11, "M5", size=T_MIN, anchor="middle", weight=800)
    d.rect(x0 + 17 * s, by, 12.5 * s, nh, fill=ORANGE_F, stroke=INK, sw=3, rx=3)
    d.text(x0 + 23.25 * s, by + nh / 2 + 11, "M3", size=T_MIN, anchor="middle", weight=800)
    # 25 mm dimension under the rail face
    dy = ry + 6.5 * s + 40
    d.line(x0, ry + 6, x0, dy + 12, stroke=MUTED, sw=2)
    d.line(x0 + 25 * s, ry + 6.5 * s + 4, x0 + 25 * s, dy + 12, stroke=MUTED, sw=2)
    d.path(f"M {x0 + 12.5 * s} {dy} L {x0 + 3} {dy}", stroke=MUTED, sw=2.5, marker="arwm")
    d.path(f"M {x0 + 12.5 * s} {dy} L {x0 + 25 * s - 3} {dy}", stroke=MUTED, sw=2.5,
           marker="arwm")
    d.text(x0 + 12.5 * s, dy + 44, "25 mm", size=T_LAB, anchor="middle", weight=700)
    d.text(x0 - 16, yt + h / 2 + 11, "end", size=T_LAB, anchor="end", weight=700, fill=BLUE)
    # callout 1 = both nuts in the rail slot: a bracket over the pair
    bry = by - 16
    d.path(f"M {x0 + 2 * s} {by - 4} L {x0 + 2 * s} {bry} L {x0 + 29.5 * s} {bry} "
           f"L {x0 + 29.5 * s} {by - 4}", stroke=INK, sw=3)
    callout(d, x0 + 46 * s, bry, 1)
    d.leader(x0 + 29.5 * s, bry, x0 + 46 * s - 30, bry, col=INK)
    # callout 2 = the M5 outermost, from outside the end face
    c2x, c2y = x0 - 48, by + nh / 2
    callout(d, c2x, c2y, 2)
    d.leader(c2x + 28, c2y, x0 + 2 * s, c2y, col=INK)
    step_note(d, "Page 90 draws this end turned over, rail up.", size=T_MIN)
    return d


# ============================================================== diagram 503 ===
def _gantry_top(d: Doc, ox, oy, flipped, with_x):
    """Top view of the gantry from the front, idlers nearest you."""
    W, H = 340, 370
    x0, y0 = ox + (555 - W) / 2, oy + 270
    t = 20
    d.rect(x0, y0, t, H, fill=BLUE_F, stroke=BLUE, sw=3)          # Y extrusions
    d.rect(x0 + W - t, y0, t, H, fill=BLUE_F, stroke=BLUE, sw=3)
    d.rect(x0, y0 - t, W, t, fill=BLUE_F, stroke=BLUE, sw=3)       # rear extrusion
    for xr in (x0 + t / 2, x0 + W - t / 2):
        if flipped:                                                # rails on top
            d.rect(xr - 4, y0 + 30, 8, H - 60, fill=STEEL, stroke=GREY, sw=2)
        else:                                                      # rails underneath
            d.line(xr, y0 + 30, xr, y0 + H - 30, stroke=GREY, sw=4, dash="10 8")
    left, right = ("A", "B") if flipped else ("B", "A")
    cols = {"A": (BELT_A, "#D3EFEC"), "B": (BELT_B, "#E7DEF8")}
    for name, x in ((left, x0 - 34), (right, x0 + W - 54)):       # drives, rear corners
        c, f = cols[name]
        d.rect(x, y0 - t - 60, 88, 88, fill=f, stroke=c, sw=4, rx=8)
        d.circle(x + 44, y0 - t - 16, 22, fill=PANEL if flipped else "none", stroke=c, sw=4,
                 dash=None if flipped else "8 6")
        d.text(x + 44, y0 - t - 74, name, size=40, anchor="middle", weight=800, fill=c)
    for name, x in ((left, x0 - 20), (right, x0 + W - 40)):       # idlers, front corners
        c, f = cols[name]
        d.rect(x, y0 + H - 6, 60, 54, fill=f, stroke=c, sw=4, rx=6)
        d.text(x + 30, y0 + H + 34, name, size=T_LAB, anchor="middle", weight=800, fill=c)
    xy = None
    if with_x:
        xy = y0 + H * 0.42
        d.rect(x0 + t + 30, xy - 10, W - 2 * t - 60, 20, fill=BLUE_F, stroke=BLUE, sw=3)
        for xj in (x0 + t - 4, x0 + W - t - 52):
            d.rect(xj, xy - 30, 56, 60, fill=BLACKPART_F, stroke=BLACKPART, sw=3, rx=6)
        # the cable bridge on the right XY joint, which lands on the left (A) side
        d.rect(x0 + t + 6, xy - 30, 30, 26, fill=ORANGE_F, stroke=ORANGE, sw=3, rx=4)
    return x0, y0, W, H, xy


def d503_gantry_flip() -> Doc:
    """Steps 05.41-05.42: before and after turning the gantry upside down."""
    d = Doc(1060, "Turning the gantry upside down swaps left and right")
    top = step_header(d, "Upside down: left and right swap")
    py, ph = top + 18, 880
    d.panel(30, py, 555, ph)
    d.text(54, py + 52, "Motors down", size=38, weight=700)
    d.text(54, py + 94, "rails underneath", size=T_MIN, fill=MUTED)
    x0, y0, W, H, _ = _gantry_top(d, 30, py, False, False)
    ox = 615
    d.panel(ox, py, 555, ph)
    d.text(ox + 24, py + 52, "Upside down", size=38, weight=700, fill=OK)
    d.text(ox + 24, py + 94, "motors up, rails on top", size=T_MIN, fill=MUTED)
    fx0, fy0, fW, fH, xy = _gantry_top(d, ox, py, True, True)
    d.text(fx0 + 40, xy + 82, "right XY joint", size=T_MIN, weight=700)
    d.text(fx0 + 40, xy + 118, "and cable bridge", size=T_MIN, weight=600, fill=ORANGE)
    d.leader(fx0 + 28, xy + 28, fx0 + 38, xy + 56, col=INK)
    for xx, ww, yy, hh in ((x0, W, y0, H), (fx0, fW, fy0, fH)):
        d.text(xx + ww / 2, yy + hh + 110, "FRONT: you stand here", size=T_MIN,
               anchor="middle", weight=700, fill=BLUE)
    d.text(54, py + ph - 50, "A on your right", size=T_LAB, weight=700, fill=BELT_A)
    d.text(ox + 24, py + ph - 50, "A now on your left", size=T_LAB, weight=700, fill=BELT_A)
    # the roll: a dashed front-to-back axis down the middle of the left gantry and one
    # arrow rolling over it, left side up and across to the right
    ax = x0 + W / 2
    ry = y0 + H * 0.36
    d.line(ax, y0 - 20 - 96, ax, ry + 56, stroke=INK, sw=3, dash="14 10")
    d.line(ax, ry + 152, ax, y0 + H + 62, stroke=INK, sw=3, dash="14 10")
    d.path(f"M {ax - 120} {ry + 30} C {ax - 120} {ry - 80}, {ax + 120} {ry - 80}, "
           f"{ax + 120} {ry + 24}", stroke=INK, sw=6, marker="arw")
    d.text(ax, ry + 92, "roll it over", size=T_MIN, anchor="middle", weight=700)
    d.text(ax, ry + 132, "this line", size=T_MIN, anchor="middle", weight=700)
    step_note(d, "Roll it left to right: the idlers stay nearest you.", size=T_MIN)
    return d


# ============================================================== diagram 504 ===
def d504_endstop_pod() -> Doc:
    """Step 05.49: the pod goes on top of the right XY joint while the gantry is
    upside down; two M3x30 go down through pod and joint into the Y carriage.

    Heights from the CAD (machine z, flipped): Y extrusion 20, rail 6.5, carriage
    top 10 above the extrusion face, joint 14.3 over the carriage, pod 15.4 on it.
    """
    d = Doc(1064, "Endstop pod: on top of the right XY joint, screws down")
    top = step_header(d, "Endstop pod: on top, screws down")
    d.panel(30, top + 16, 1140, 650)
    d.text(54, top + 66, "From the front, gantry upside down", size=T_MIN, weight=700,
           fill=MUTED)
    k = 6.2
    ox = 300                    # the outboard edge of the carriage / joint (CAD x 334)

    def X(mm):                  # mm inboard from the outboard edge
        return ox + mm * k
    base = top + 608            # bottom face of the Y extrusion, resting on the bench

    def Z(mm):                  # mm up from that face
        return base - mm * k
    # Y extrusion (CAD x 312-332 -> 2-22 mm in), its backer now underneath
    profile2020(d, X(12), Z(10), k)
    d.rect(X(3), Z(0), 18 * k, 2.5 * k, fill=TI_F, stroke=TI, sw=2.5)
    # X extrusion, level with the Y extrusion, going off inboard (its end at 42 mm in)
    d.rect(X(42), Z(20), 1150 - X(42), 20 * k, fill=BLUE_F, stroke=BLUE, sw=3)
    # MGN9 rail and the carriage riding on it
    d.rect(X(7.5), Z(26.5), 9 * k, 6.5 * k, fill=STEEL, stroke=GREY, sw=2.5)
    d.rect(X(2), Z(30), 20 * k, 8 * k, fill=GREY_F, stroke=GREY, sw=2.5, rx=4)
    # the right XY joint: a slab on the carriage, its body down round the X extrusion end
    jt, jb = 44.3, 30.0
    d.path(f"M {X(0)} {Z(jt)} L {X(72)} {Z(jt)} L {X(72)} {Z(-4)} L {X(24)} {Z(-4)} "
           f"L {X(24)} {Z(jb)} L {X(0)} {Z(jb)} Z", fill=BLACKPART_F, stroke=BLACKPART, sw=3)
    d.rect(X(42), Z(20), (72 - 42) * k, 20 * k, fill="none", stroke=BLUE, sw=2.5, dash="8 6")
    # the pod on top (CAD x 274-334 -> 0-60 mm in)
    pt = jt + 15.4
    d.rect(X(0), Z(pt), 60 * k, 15.4 * k, fill=ORANGE_F, stroke=ORANGE, sw=3.5, rx=6)
    # two M3x30 down through pod and joint into the carriage (CAD x 314.5 / 329.5)
    for mm in (4.5, 19.5):
        shcs_v(d, X(mm), Z(pt + 3.0), k, 30, head_up=True, dash_from=1.5)
    arrow(d, X(12), Z(pt + 22), X(12), Z(pt + 6), col=INK, sw=6)
    callout(d, X(12) + 60, Z(pt + 16), 2)
    d.text(X(12) + 104, Z(pt + 16) + 11, "two M3×30, down", size=T_LAB, weight=700)
    # labels
    lx = X(80)
    d.text(lx, Z(pt - 6) + 11, "endstop pod", size=T_LAB, weight=700, fill=ORANGE)
    d.leader(X(60), Z(pt - 7), lx - 10, Z(pt - 7), col=ORANGE)
    d.text(lx, Z(jt - 8) + 11, "right XY joint", size=T_LAB, weight=700)
    d.leader(X(72), Z(jt - 8), lx - 10, Z(jt - 8), col=INK)
    d.text(1130, Z(20) - 16, "X extrusion", size=T_LAB, anchor="end", weight=700, fill=BLUE)
    d.text(X(-4), Z(26) + 10, "carriage", size=T_MIN, anchor="end", weight=700)
    d.text(X(-4), Z(10) + 10, "Y extrusion", size=T_MIN, anchor="end", weight=700,
           fill=BLUE)

    # ---- inset: the four carriage holes seen from above, front at the bottom
    iy = top + 686
    d.panel(30, iy, 1140, d.h - iy - 16)
    d.text(54, iy + 50, "From above: which two holes", size=T_MIN, weight=700, fill=MUTED)
    jx, jy, jw, jh = 110, iy + 80, 200, 170
    d.rect(jx, jy, jw, jh, fill=BLACKPART_F, stroke=BLACKPART, sw=3, rx=10)
    for hx in (jx + 55, jx + 145):
        d.circle(hx, jy + 45, 22, fill=GREY, stroke=INK, sw=2.5)         # M3x16, rear pair
        d.circle(hx, jy + 125, 22, fill=PANEL, stroke=ORANGE, sw=6)      # M3x30, front pair
    tx = jx + jw + 40
    d.text(tx, jy + 40, "M3×16 already in:", size=T_MIN, weight=700)
    d.text(tx, jy + 76, "the pair nearer the drives", size=T_MIN, weight=600, fill=MUTED)
    d.text(tx, jy + 130, "M3×30 here:", size=T_MIN, weight=700, fill=ORANGE)
    d.text(tx, jy + 166, "the pair nearer the idlers", size=T_MIN, weight=600, fill=MUTED)
    return d


# ============================================================== diagram 505 ===
def d505_xy_joint_stack() -> Doc:
    """Steps 05.26 / 05.30: spacer, F695 flange down, F695 flange up, spacer, on the
    M5x40 pushed up through the thin plate (p.97, p.99)."""
    d = Doc(1000, "XY joint bearing stack, bottom to top")
    top = step_header(d, "XY joint bearing stack")
    d.panel(30, top + 16, 780, d.h - top - 32)
    d.text(54, top + 70, "flanges face out", size=T_LAB + 4, weight=800, fill=OK)
    k = 16.0
    cx = 240
    plate_top = d.h - 210

    def bearing(yb, flange_down):
        """F695 side view: 13 OD x 4 wide body, 15 OD x 1 flange; yb = bottom y."""
        body_y = yb - 4 * k
        d.rect(cx - 6.5 * k, body_y, 13 * k, 4 * k, fill=STEEL, stroke=GREY, sw=2.5, rx=3)
        fy = yb - 1 * k if flange_down else body_y
        d.rect(cx - 7.5 * k, fy, 15 * k, 1 * k, fill=INK, stroke=INK, sw=2, rx=2)
        return body_y

    def spacer(yb):
        d.rect(cx - 5 * k, yb - 1.2 * k, 10 * k, 1.2 * k, fill=AMBER_F, stroke=AMBER, sw=3,
               rx=2)
        return yb - 1.2 * k
    # the stack as p.97 draws it: the four items touching, plain face to plain face in
    # the middle; only the plate below and the body above are pulled apart
    stack_bot = plate_top - 40
    order = ("spacer", "down", "up", "spacer")
    rows = []
    y = stack_bot
    for kind in order:
        y1 = y - (1.2 * k if kind == "spacer" else 4 * k)
        if kind == "spacer":
            rows.append(((y + y1) / 2, "spacer", AMBER))
        else:
            rows.append(((y + y1) / 2, "F695, flange " + kind, INK))
        y = y1
    stack_top = y
    body_top = stack_top - 200
    shaft_top = body_top + 20
    # the screw: drawn first so the stack sits over it
    d.rect(cx - 2.5 * k, shaft_top, 5 * k, plate_top + 70 - shaft_top, fill=GREY_F,
           stroke=GREY, sw=2.5)
    y = stack_bot
    for kind in order:
        y = spacer(y) if kind == "spacer" else bearing(y, kind == "down")
    # the thin plate at the bottom, the screw head under it
    d.rect(cx - 160, plate_top, 320, 70, fill=BLACKPART_F, stroke=BLACKPART, sw=3, rx=8)
    d.rect(cx - 2.5 * k, plate_top - 1, 5 * k, 72, fill=GREY_F, stroke=GREY, sw=2.5)
    d.rect(cx - 4.25 * k, plate_top + 72, 8.5 * k, 60, fill=GREY_F, stroke=GREY, sw=2.5, rx=6)
    # labels fanned out a little so the thin spacer rows keep clear of the bearing rows
    nudge = (10, 0, 0, -10)
    for (yy, lab, col), dy in zip(rows, nudge):
        d.path(f"M {cx + 8 * k} {yy} L {440} {yy + dy}", stroke=col if col != INK else MUTED,
               sw=2)
        d.text(450, yy + dy + 11, lab, size=T_LAB, weight=700, fill=col)
    # the thick body comes down on top, labelled beside its box
    d.rect(cx - 170, body_top, 340, 110, fill="none", stroke=BLACKPART, sw=3, rx=10,
           dash="12 8")
    arrow(d, cx + 210, body_top + 10, cx + 210, body_top + 100, col=MUTED, sw=4, mk="arwm")
    d.text(cx + 240, body_top + 50, "thick body", size=T_MIN, weight=700, fill=MUTED)
    d.text(cx + 240, body_top + 88, "comes down last", size=T_MIN, weight=600, fill=MUTED)
    d.text(cx + 175, plate_top + 46, "thin plate", size=T_MIN, weight=700)
    d.text(cx + 80, plate_top + 116, "M5×40, pushed up", size=T_MIN, weight=700)
    # Do numbers of Steps 05.26 and 05.30: 2 = the screw up through the plate, 3 = the stack
    callout(d, cx - 130, plate_top + 102, 2)
    d.leader(cx - 102, plate_top + 102, cx - 4.25 * k - 4, plate_top + 102, col=INK)
    smid = (stack_bot + stack_top) / 2
    callout(d, 68, smid, 3)
    d.path(f"M 114 {stack_top + 2} L 104 {stack_top + 2} L 104 {stack_bot - 2} "
           f"L 114 {stack_bot - 2}", stroke=INK, sw=3)
    d.leader(96, smid, 104, smid, col=INK)

    # ---- wrong: flanges in, meeting in the middle
    ox = 830
    d.panel(ox, top + 16, 340, d.h - top - 32)
    d.text(ox + 24, top + 70, "Wrong", size=38, weight=700, fill=RED)
    kw = 9.0
    wx, wy = ox + 170, top + 360
    d.rect(wx - 2.5 * kw, wy - 150, 5 * kw, 300, fill=GREY_F, stroke=GREY, sw=2)
    d.rect(wx - 6.5 * kw, wy - 5 * kw, 13 * kw, 4 * kw, fill=STEEL, stroke=GREY, sw=2)
    d.rect(wx - 6.5 * kw, wy + 1 * kw, 13 * kw, 4 * kw, fill=STEEL, stroke=GREY, sw=2)
    d.rect(wx - 7.5 * kw, wy - 1 * kw, 15 * kw, 1 * kw, fill=RED, stroke=RED, sw=2)
    d.rect(wx - 7.5 * kw, wy, 15 * kw, 1 * kw, fill=RED, stroke=RED, sw=2)
    red_x(d, wx + 100, wy - 120)
    d.text(ox + 24, wy + 230, "flanges in:", size=T_LAB, weight=700, fill=RED)
    d.text(ox + 24, wy + 270, "the belt has", size=T_LAB, weight=700)
    d.text(ox + 24, wy + 310, "no channel", size=T_LAB, weight=700)
    return d


# ============================================================== diagram 506 ===
def d506_backer_faces() -> Doc:
    """Steps 05.17 / 05.34: rail on one face, titanium backer on the opposite one."""
    d = Doc(780, "Rail on one face, titanium backer on the opposite face")
    top = step_header(d, "Rail one side, backer opposite")
    k = 11.0
    # ---- Y extrusion (C): rail and carriage underneath, backer on top
    d.panel(30, top + 16, 555, 590)
    d.text(54, top + 66, "Y extrusion, end on", size=T_LAB, weight=700)
    cx, cy = 200, top + 300
    profile2020(d, cx, cy, k)
    rail_on_face(d, cx, cy, k, 2, 9, 6.5)
    carriage_on_face(d, cx, cy, k, 2, 20, 10, 9, 6.5)
    strip_on_face(d, cx, cy, k, 0, 18, 2.5, fill=TI_F, stroke=TI)
    d.text(cx + 130, cy - 10 * k - 2, "backer: top", size=T_LAB, weight=700)
    d.text(cx + 130, cy + 10 * k + 70, "rail: underneath", size=T_LAB, weight=700)
    # ---- X extrusion (D): rail at the front, backer at the rear
    ox = 615
    d.panel(ox, top + 16, 555, 590)
    d.text(ox + 24, top + 66, "X extrusion, end on", size=T_LAB, weight=700)
    cx2, cy2 = ox + 290, top + 290
    profile2020(d, cx2, cy2, k)
    rail_on_face(d, cx2, cy2, k, 3, 12, 8)
    strip_on_face(d, cx2, cy2, k, 1, 18, 2.5, fill=TI_F, stroke=TI)
    d.text(cx2 - 15 * k, cy2 + 10 * k + 70, "rail", size=T_LAB, anchor="middle", weight=700)
    d.text(cx2 - 15 * k, cy2 + 10 * k + 110, "FRONT", size=T_LAB, anchor="middle",
           weight=800, fill=BLUE)
    d.text(cx2 + 12.5 * k, cy2 + 10 * k + 70, "backer", size=T_LAB, anchor="middle",
           weight=700)
    d.text(cx2 + 12.5 * k, cy2 + 10 * k + 110, "REAR", size=T_LAB, anchor="middle",
           weight=800, fill=BLUE)
    step_note(d, "Never a backer on the rail's own face.", size=T_LAB)
    return d


# ================================================================= registry ===
DIAGRAMS = [
    {
        "n": 501,
        "file": "501-x-extrusion-m5-tnuts.svg",
        "title": "X extrusion: M5 T-nuts",
        "fn": d501_x_extrusion_tnuts,
        "shows": [
            "End view of the D extrusion: the MGN12 rail on the front face, the titanium "
            "backer on the rear face, an M5 T-nut in the top slot (callout 1) and one in the "
            "bottom slot (callout 2).",
            "Front view of the whole 430 mm extrusion: two M5 T-nuts in the top slot at each "
            "end, one in the bottom slot at each end under the outer top nut, and the 400 mm "
            "rail 15 mm short of each end. Callouts 1 and 2 are the Do numbers of Step 05.36.",
        ],
        "insert": [
            ("05-gantry.md", "Step 05.36", "which slot takes which M5 T-nuts"),
        ],
        "verify": [
            "T-nut positions along the extrusion follow the 250-size CAD (2–15 mm and "
            "17–30 mm from each end, the bottom single under the outer top nut); the joint's "
            "own holes set the real position.",
            "Backer thickness (drawn 2.5 mm) is schematic.",
        ],
    },
    {
        "n": 502,
        "file": "502-y-extrusion-end-tnuts.svg",
        "title": "Y extrusion end: four T-nuts",
        "fn": d502_y_extrusion_end,
        "shows": [
            "One end of a C extrusion the way it sits in the machine, rail underneath: two M5 "
            "T-nuts already in the top slot, and in the rail's slot, in the bare 25 mm beyond "
            "the rail end, one M5 outermost and one M3 just inside it (callouts 1 and 2 are the "
            "Do numbers of Step 05.14). A small end view names the top slot and the rail slot.",
        ],
        "insert": [
            ("05-gantry.md", "Step 05.14", "the end as it sits in the machine, not rail-up as "
             "on p.90"),
        ],
        "verify": [
            "Nut lengths and positions follow the 250-size CAD (M5 2–15 mm, M3 17–29.5 mm "
            "from the end); in the CAD the M3 reaches about 4 mm under the rail end.",
        ],
    },
    {
        "n": 503,
        "file": "503-gantry-flip.svg",
        "title": "Upside down: left and right swap",
        "fn": d503_gantry_flip,
        "shows": [
            "Two top views from the front (idler) end. Before: motors down, rails underneath, "
            "B drive and B idler on the left, A on the right, with a dashed front-to-back "
            "line down the middle and one arrow rolling the gantry over it, left to right. "
            "After the roll: motors up, rails on top, A on the left, and the X axis landed "
            "with the right XY joint (the one with the cable bridge) on the A side, your left.",
        ],
        "insert": [
            ("05-gantry.md", "Step 05.41", "what rolling it over does to left and right, and "
             "which end the right XY joint lands on"),
        ],
        "verify": [
            "Proportions are schematic. Any way of turning it over gives the same result once "
            "the idlers are nearest you; the roll about the front-to-back line is drawn "
            "because it keeps them nearest you throughout.",
        ],
    },
    {
        "n": 504,
        "file": "504-endstop-pod-on-joint.svg",
        "title": "Endstop pod: on top, screws down",
        "fn": d504_endstop_pod,
        "shows": [
            "Front view of the right XY joint with the gantry upside down on the bench: Y "
            "extrusion (backer now underneath), rail and carriage on top of it, the joint on "
            "the carriage and round the X extrusion's end, the endstop pod on top of the joint, "
            "and two M3×30 going down through pod and joint into the carriage (callout 2 is "
            "the Do number of Step 05.49).",
            "From above: the joint's four carriage holes, the M3×16 of Step 05.43 in the pair "
            "nearer the drives and the M3×30 in the pair nearer the idlers.",
        ],
        "insert": [
            ("05-gantry.md", "Step 05.49", "which face the pod goes on and where its screws go"),
        ],
        "verify": [
            "Heights and widths come from the 250-size CAD (pod 15.4 mm, joint 14.3 mm over "
            "the carriage, M3×30 in the front pair at y 159, M3×16 in the rear pair at y 175); "
            "the joint's outline and the pod's shape are schematic, and the endstop board "
            "inside the pod is not drawn.",
        ],
    },
    {
        "n": 505,
        "file": "505-xy-joint-bearing-stack.svg",
        "title": "XY joint bearing stack",
        "fn": d505_xy_joint_stack,
        "shows": [
            "Side view as p.97 builds it: the thin plate at the bottom, the M5×40 pushed up "
            "through it (callout 2), then the stack touching item to item, spacer, F695 "
            "flange down, F695 flange up, spacer (callout 3), and the thick body coming down "
            "on top. Callouts 2 and 3 are the Do numbers of Steps 05.26 and 05.30. A small "
            "red panel shows the wrong way: flanges facing in.",
        ],
        "insert": [
            ("05-gantry.md", "Step 05.26", "the stack order on the right joint"),
            ("05-gantry.md", "Step 05.30", "the same stack on the left joint"),
        ],
        "verify": [
            "F695 and spacer sizes are to scale (13/15 mm, 1 mm spacer as in the CAD); the "
            "plate, body and screw head are schematic.",
        ],
    },
    {
        "n": 506,
        "file": "506-rail-and-backer-faces.svg",
        "title": "Rail one side, backer opposite",
        "fn": d506_backer_faces,
        "shows": [
            "End views as the extrusions sit in the machine. Y extrusion: MGN9 rail and "
            "carriage underneath, backer on top. X extrusion: MGN12 rail on the front face, "
            "backer on the rear face.",
        ],
        "insert": [
            ("05-gantry.md", "Step 05.17", "the Y extrusion's faces"),
            ("05-gantry.md", "Step 05.34", "the X extrusion's faces"),
        ],
        "verify": [
            "Backer thickness (drawn 2.5 mm) is schematic; the 18 mm width is from the tanaes "
            "DXFs.",
        ],
    },
]
