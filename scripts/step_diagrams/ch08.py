"""Chapter 08 (toolhead) step-column diagrams, 801 onwards.

Geometry sources: Stealthburner r2 / Clockwork 2.5 manual at 1572a42 (p.31-38, p.54, p.56,
p.60-64, p.75-76), LDO's Nitehawk-SB V2 board doc and Rev D wiring guide (fetched 2026-11-20),
the Nitehawk-SB-V2 repo images (board pinout, fan-adapter pinout, title photo, toolboard ground
routing). Proportions are schematic; sides, order, counts and labels follow the sources.
"""
import math

import draw_diagrams as dd
from draw_diagrams import (AMBER, AMBER_F, BLACKPART, BLACKPART_F, GREY, GREY_F, INK, MUTED,
                           OK, ORANGE, ORANGE_F, PANEL, RED, STEEL, Doc, T_LAB, T_MIN, callout,
                           label_bg, legend_row, step_header)

PCB = "#262B31"          # a black circuit board
PCB_EDGE = "#11151A"
WIRE_RED = "#C0392B"
WIRE_BLK = "#1D2126"


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


def arrow(d: Doc, x0, y0, x1, y1, col=INK, sw=6, mk="arw", dash=None):
    d.path(f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}", stroke=col, sw=sw, marker=mk, dash=dash)


def fhcs(d: Doc, x, y, r=17):
    """A flat-head screw seen head-on: countersunk head with a hex socket."""
    d.circle(x, y, r, fill=GREY_F, stroke=GREY, sw=3)
    pts = []
    for i in range(6):
        a = math.radians(60 * i)
        pts.append((x + r * 0.45 * math.cos(a), y + r * 0.45 * math.sin(a)))
    d.poly(pts, fill=GREY, stroke=GREY, sw=1)


# ============================================================= diagram 801 ===
def d801_fan_adapter() -> Doc:
    d = Doc(1000, "Fan adapter on the back of the 5015 blower")
    top = step_header(d, "Fan adapter on the 5015")
    d.panel(30, top + 16, 760, 870)
    d.text(54, top + 64, "Seen from behind", size=T_MIN, weight=700, fill=MUTED)

    # Stealthburner body, rear view, schematic outline (blue accent part = orange)
    body = [(150, 200), (560, 170), (700, 250), (720, 560), (640, 760), (560, 930),
            (330, 930), (240, 760), (130, 560)]
    d.poly(body, fill=ORANGE_F, stroke=ORANGE, sw=5)
    # 5015 blower in the upper pocket: round scroll and its outlet
    fx, fy, fr = 430, 410, 180
    d.path(f"M {fx - fr} {fy} A {fr} {fr} 0 1 1 {fx + 40} {fy + fr - 4} L {fx + 40} {fy + fr + 70} "
           f"L {fx - 120} {fy + fr + 70} L {fx - 150} {fy + 60} Z", fill=GREY_F, stroke=GREY, sw=4)
    d.circle(fx, fy, 70, fill=PANEL, stroke=GREY, sw=3)
    # the two body holes SB p.64's M3x6 FHCS use: upper left of the fan, and right of its centre
    h1, h2 = (262, 262), (612, 470)
    # adapter PCB: holes at the two ends of its long edge, third corner below
    tri = [(h1[0] - 40, h1[1] - 30), (h2[0] + 44, h2[1] - 8), (400, 600)]
    d.poly(tri, fill=PCB, stroke=PCB_EDGE, sw=3)
    for hx, hy in (h1, h2):
        d.circle(hx, hy, 24, fill=PANEL, stroke=PCB_EDGE, sw=2)
        fhcs(d, hx, hy, 18)
    # P1 pins beside the upper hole, pointing back at the reader (dots)
    px, py = 318, 296
    d.rect(px - 8, py - 8, 56, 132, fill="#3A4048", stroke=PCB_EDGE, sw=2, rx=4)
    for r in range(5):
        for c in range(2):
            d.circle(px + 8 + c * 24, py + 10 + r * 25, 6, fill="#E8C770", stroke="none", sw=0)
    # the three plugs along the lower edges (P2, P3, P4)
    for (cx, cy) in ((420, 540), (490, 506), (560, 474)):
        d.rect(cx - 22, cy - 16, 44, 32, fill=INK, stroke=INK, sw=1, rx=3)

    callout(d, 470, 380, 1)
    callout(d, h2[0] + 26, h2[1] + 30, 2)
    # below the body outline: the toolboard is on the viewer's left in a rear view
    arrow(d, 106, 955, 46, 955, col=MUTED, sw=4, mk="arwm")
    d.text(116, 966, "toolboard side", size=T_MIN, weight=700, fill=MUTED)

    # right column
    y = legend_row(d, 810, top + 120, 1, ["board flat on", "the back of", "the 5015"])
    y = legend_row(d, 810, y + 30, 2, ["two M3×10", "flat-head screws", "through both"])
    d.text(876, y + 40, "P1 pins point", size=T_LAB, weight=600)
    d.text(876, y + 80, "back, at the", size=T_LAB, weight=600)
    d.text(876, y + 120, "toolboard", size=T_LAB, weight=600)
    bench_tag(d, 995, y + 210, "holes: on the bench", anchor="middle")
    return d


# ============================================================= diagram 802 ===
def d802_ground_lug() -> Doc:
    d = Doc(1000, "Ground wire: the ring lug on the extruder motor")
    top = step_header(d, "Ground wire, motor end")
    d.panel(30, top + 16, 760, 870)
    d.text(54, top + 64, "Seen from behind", size=T_MIN, weight=700, fill=MUTED)

    # extruder body (black printed part) and the motor can, after LDO's photo
    d.poly([(170, 190), (640, 180), (740, 300), (740, 700), (660, 790), (220, 790), (170, 720)],
           fill=BLACKPART_F, stroke=BLACKPART, sw=4)
    # toolboard seen edge-on on the left
    d.rect(150, 230, 40, 520, fill=PCB, stroke=PCB_EDGE, sw=2, rx=4)
    d.text(110, 220, "toolboard", size=T_MIN, weight=700, anchor="start")
    mx, my, mr = 460, 450, 205
    d.circle(mx, my, mr, fill="#4A5059", stroke=INK, sw=4)
    d.circle(mx, my, 34, fill=STEEL, stroke=GREY, sw=3)
    d.text(mx, my - 80, "motor", size=T_LAB, anchor="middle", weight=700, fill="#FFFFFF")
    # chain anchor below the motor (LDO's supplied part)
    d.poly([(250, 810), (720, 810), (690, 880), (280, 880)], fill="none", stroke=BLACKPART,
           sw=4)
    d.text(485, 860, "chain anchor", size=T_MIN, anchor="middle", weight=700, fill=BLACKPART)
    # board-end lug under the lower board screw, the wire round the can's left and top
    bx, by = 205, 700
    d.circle(bx, by, 16, fill=GREY_F, stroke=GREY, sw=3)
    lx, ly = 618, 612                         # lower ear of the motor, nearest the anchor
    d.path(f"M {bx + 14} {by - 6} C 250 600 236 320 330 270 C 430 200 600 210 660 330 "
           f"C 700 420 690 520 {lx + 30} {ly - 70}", stroke=WIRE_BLK, sw=9)
    # ring lug: barrel bent up along the can, ring on the screw
    d.path(f"M {lx + 30} {ly - 70} L {lx + 10} {ly - 22}", stroke=STEEL, sw=14, cap="butt")
    d.circle(lx, ly, 22, fill=STEEL, stroke=GREY, sw=3)
    d.circle(lx, ly, 11, fill=GREY, stroke=INK, sw=2)
    callout(d, lx + 72, ly + 34, 1)
    callout(d, lx + 96, ly - 110, 2)

    # small wrong: lug pointing down into the anchor
    d.panel(810, top + 16, 360, 330)
    d.text(834, top + 66, "Wrong", size=36, weight=700, fill=RED)
    wx, wy = 990, top + 160
    d.circle(wx, wy, 70, fill="#4A5059", stroke=INK, sw=3)
    d.path(f"M {wx + 50} {wy + 50} L {wx + 50} {wy + 130}", stroke=STEEL, sw=12, cap="butt")
    d.circle(wx + 50, wy + 50, 14, fill=STEEL, stroke=GREY, sw=2)
    d.line(wx - 80, wy + 136, wx + 120, wy + 136, stroke=BLACKPART, sw=5)
    cross(d, wx + 120, wy + 80)
    d.text(834, top + 336, "hits the anchor", size=T_MIN, weight=700, fill=RED)

    y = legend_row(d, 810, top + 420, 1, ["lug on the", "motor's lower", "ear"])
    y = legend_row(d, 810, y + 24, 2, ["bend it clear", "of the anchor"])
    bench_tag(d, 990, y + 70, "fixing: on the bench", anchor="middle")
    return d


# ============================================================= diagram 803 ===
def d803_cartridge_leads() -> Doc:
    d = Doc(1000, "Tool cartridge pushed up under the extruder and held by its body; heater into HE0, "
                  "thermistor into TH0")
    top = step_header(d, "Cartridge up, leads in")
    d.panel(30, top + 16, 800, 870)
    d.text(54, top + 64, "Toolboard side, front on the left", size=T_MIN, weight=700, fill=MUTED)

    # extruder with the toolboard on its side
    d.rect(150, 190, 640, 380, fill=BLACKPART_F, stroke=BLACKPART, sw=4, rx=12)
    d.rect(200, 220, 520, 320, fill=PCB, stroke=PCB_EDGE, sw=3, rx=10)
    # TH0 (2-pin PH2.0) left of HE0 (screw terminal), lower middle of the board
    tx, ty = 370, 440
    d.rect(tx - 32, ty - 36, 64, 72, fill="#F2F2EE", stroke=GREY, sw=2, rx=4)
    d.mono(tx, ty - 52, "TH0", size=T_LAB, anchor="middle", weight=700, fill="#FFFFFF")
    hx, hy = 540, 440
    d.rect(hx - 70, hy - 40, 140, 80, fill="#3D7A4A", stroke=INK, sw=2, rx=4)
    for sx in (-34, 34):
        d.circle(hx + sx, hy, 22, fill=STEEL, stroke=GREY, sw=2)
        d.line(hx + sx - 14, hy - 14, hx + sx + 14, hy + 14, stroke=GREY, sw=4)
    d.mono(hx, hy - 56, "HE0", size=T_LAB, anchor="middle", weight=700, fill="#FFFFFF")

    # the cartridge just below the extruder: its four screws sit recessed in the top,
    # so nothing stands proud; the body screws at 08.62 hold it, a hand holds it till then
    cy0 = 620
    d.rect(250, cy0, 440, 190, fill=BLACKPART_F, stroke=BLACKPART, sw=4, rx=14)
    d.poly([(450, cy0 + 190), (490, cy0 + 190), (478, cy0 + 222), (462, cy0 + 222)],
           fill="#C9A13B", stroke=INK, sw=2)
    d.text(470, cy0 + 110, "tool cartridge", size=T_LAB, anchor="middle", weight=700)
    arrow(d, 760, cy0 + 150, 760, cy0 - 20, col=ORANGE, sw=8, mk="arwo")
    callout(d, 760, cy0 + 200, 1)
    # fingertips under the cartridge's corners, clear of the nozzle
    for fx in (300, 640):
        d.path(f"M {fx - 40} 868 C {fx - 40} 806 {fx + 40} 806 {fx + 40} 868 Z",
               fill=GREY_F, stroke=GREY, sw=4)
        arrow(d, fx, 916, fx, 878, col=MUTED, sw=4, mk="arwm")
    d.text(470, 950, "hold the cartridge, not the nozzle", size=T_MIN, anchor="middle",
           weight=700, fill=MUTED)

    # heater pair (red) to HE0 with ferrules, thermistor pair (thin) to TH0
    for i, sx in enumerate((-34, 34)):
        x0 = 520 + i * 26
        d.path(f"M {x0} {cy0 - 6} C {x0} 590 {hx + sx} 560 {hx + sx} {hy + 52}",
               stroke=WIRE_RED, sw=8)
        d.rect(hx + sx - 8, hy + 30, 16, 26, fill=STEEL, stroke=GREY, sw=2)
    for i in range(2):
        x0 = 400 + i * 16
        d.path(f"M {x0} {cy0 - 6} C {x0} 600 {tx - 10 + i * 20} 560 {tx - 10 + i * 20} {ty + 36}",
               stroke="#E6E6E6", sw=5)
        d.path(f"M {x0} {cy0 - 6} C {x0} 600 {tx - 10 + i * 20} 560 {tx - 10 + i * 20} {ty + 36}",
               stroke=GREY, sw=1.5)
    callout(d, hx + 110, hy + 10, 2)
    callout(d, tx - 100, ty + 10, 3)

    y = legend_row(d, 850, top + 120, 1, ["push it up,", "hold it by the", "cartridge"])
    y = legend_row(d, 850, y + 30, 2, ["heater leads", "into HE0,", "tug each one"])
    y = legend_row(d, 850, y + 30, 3, ["thermistor", "into TH0"])
    d.text(850, y + 60, "what holds it", size=T_MIN, weight=700)
    d.text(850, y + 98, "before 08.62:", size=T_MIN, weight=700)
    bench_tag(d, 1010, y + 160, "on the bench", anchor="middle")
    return d


# ============================================================= diagram 804 ===
def d804_body_header() -> Doc:
    d = Doc(1075, "Cable cover screws, then the body's header straight onto the toolboard's")
    top = step_header(d, "Cover, header, body")

    # ---- panel A: the cover's two screws, extruder seen from the front
    ay = top + 16
    d.panel(30, ay, 1140, 360)
    d.text(54, ay + 50, "Extruder from the front", size=T_MIN, weight=700, fill=MUTED)
    ex0, ex1, ey0, ey1 = 280, 610, ay + 90, ay + 330
    d.rect(ex0, ey0, ex1 - ex0, ey1 - ey0, fill=BLACKPART_F, stroke=BLACKPART, sw=4, rx=14)
    d.rect(ex1, ey0 + 20, 70, ey1 - ey0 - 30, fill="#B9BFC8", stroke=BLACKPART, sw=4, rx=10)
    d.text(ex1 + 90, ey0 + 80, "cable cover", size=T_MIN, weight=700)
    # latch flipped open, top right; it closes again once both screws are in
    d.poly([(560, ey0 + 4), (640, ey0 - 50), (660, ey0 - 26), (590, ey0 + 18)],
           fill=ORANGE_F, stroke=ORANGE, sw=3)
    d.text(690, ey0 - 14, "latch: open, then close", size=T_MIN, weight=700, fill=ORANGE)
    # M3x16 straight in through the front access hole (into the page)
    sx, sy = 590, ey0 + 70
    d.circle(sx, sy, 24, fill=PANEL, stroke=INK, sw=3)
    d.line(sx - 14, sy - 14, sx + 14, sy + 14, stroke=INK, sw=4)
    d.line(sx - 14, sy + 14, sx + 14, sy - 14, stroke=INK, sw=4)
    d.text(54, ey0 + 82, "M3×16 in from", size=T_LAB, weight=700)
    d.text(54, ey0 + 122, "the front", size=T_LAB, weight=700)
    d.leader(sx - 30, sy + 4, 250, ey0 + 100, col=INK)
    # M3x6 BHCS into the cover's side wall, low at the front
    bx, by = ex1 + 70, ey1 - 50
    arrow(d, bx + 110, by, bx + 8, by, col=INK, sw=7)
    d.text(bx + 130, by + 11, "M3×6 into its side", size=T_LAB, weight=700)
    callout(d, 445, ey0 + 160, 1)
    bench_tag(d, 1160, by + 58, "reach: on the bench", anchor="end")

    # ---- panel B: body onto the toolboard, side view, front on the left
    by0 = ay + 380
    d.panel(30, by0, 1140, d.h - by0 - 16)
    d.text(54, by0 + 46, "Toolboard side, front on the left", size=T_MIN, weight=700,
           fill=MUTED)
    # toolboard (face on) with its socket on the front edge
    tbx0, tbx1, tby0, tby1 = 640, 1100, by0 + 90, by0 + 500
    d.rect(tbx0, tby0, tbx1 - tbx0, tby1 - tby0, fill=PCB, stroke=PCB_EDGE, sw=3, rx=10)
    d.text((tbx0 + tbx1) / 2 + 30, tby1 - 32, "toolboard", size=T_LAB, anchor="middle",
           weight=700, fill="#FFFFFF")
    sk0, sk1 = tbx0 - 60, tbx0 + 20
    rows = [tby0 + 52 + i * 50 for i in range(5)]
    d.rect(sk0, rows[0] - 32, sk1 - sk0, rows[-1] - rows[0] + 64, fill=INK, stroke=INK, sw=2,
           rx=4)
    for ry in rows:
        d.rect(sk0 + 4, ry - 9, 30, 18, fill=PANEL, stroke="none", sw=0, rx=3)
    d.text(tbx0 + 40, rows[0] + 11, "A1 A2 row on top", size=T_MIN, weight=700, fill="#FFFFFF")
    d.text(tbx0 + 40, rows[-1] + 11, "24V row at the bottom", size=T_MIN, weight=700,
           fill="#FFFFFF")
    # fan adapter seen edge-on in the body, its P1 pins pointing back at the socket
    ax = 360
    d.poly([(110, by0 + 76), (ax + 40, by0 + 76), (ax + 40, by0 + 500), (150, by0 + 500),
            (90, by0 + 290)], fill=ORANGE_F, stroke=ORANGE, sw=5)
    d.text(150, by0 + 330, "body", size=T_LAB, weight=700, fill=ORANGE)
    d.rect(ax - 6, rows[0] - 50, 12, rows[-1] - rows[0] + 100, fill=PCB, stroke=PCB_EDGE, sw=2)
    for ry in rows:
        d.line(ax + 6, ry, ax + 120, ry, stroke="#C9A13B", sw=7, cap="butt")
    arrow(d, ax + 150, rows[2], sk0 - 16, rows[2], col=ORANGE, sw=8, mk="arwo")
    callout(d, (ax + 150 + sk0) / 2, rows[2] - 56, 2)
    d.text(ax + 140, by0 + 548, "straight in. Resists: backwards, stop", size=T_LAB,
           anchor="middle", weight=700, fill=RED)
    # the four body screws from the front: two upper, two lower
    for yy, lab in ((by0 + 126, "2 × M3×25"), (by0 + 450, "2 × M3×50")):
        arrow(d, 40 + 10, yy, 150, yy, col=INK, sw=6)
        label_bg(d, 170, yy + 11, lab, size=T_MIN, anchor="start", weight=700, bg=ORANGE_F)
    callout(d, 80, by0 + 290, 3)
    return d


# ============================================================= diagram 805 ===
def d805_revo_leads() -> Doc:
    d = Doc(1000, "Revo leads: the HeaterCore's Micro-Fit plugs stay; only the extension cable "
                  "is cut, at the board end, for ferrules and a PH2.0 housing")
    top = step_header(d, "Ends for HE0 and TH0")

    # ---- top strip: HeaterCore leads end in Micro-Fit plugs (E3D); only the extension
    # cable, at its board end, is ever cut
    d.panel(30, top + 16, 1140, 250)
    y1, y2 = top + 130, top + 180
    d.rect(60, top + 104, 70, 100, fill=STEEL, stroke=GREY, sw=3, rx=8)
    d.text(54, top + 70, "HeaterCore", size=T_MIN, weight=700)
    for yy, col, w in ((y1, WIRE_RED, 8), (y2, "#BDBDBD", 6)):
        d.line(130, yy, 268, yy, stroke=col, sw=w)
        d.rect(268, yy - 18, 64, 36, fill="#F2F2EE", stroke=GREY, sw=3, rx=5)
        d.line(332, yy, 1000, yy, stroke=col, sw=w)
    d.text(300, top + 88, "Micro-Fit", size=T_MIN, anchor="middle", weight=700)
    d.text(600, top + 88, "extension cable", size=T_MIN, anchor="middle", weight=700)
    d.text(1012, (y1 + y2) / 2 + 11, "board", size=T_MIN, weight=700, fill=MUTED)
    d.text(175, top + 246, "never cut", size=T_MIN, anchor="middle", weight=700, fill=RED)
    callout(d, 300, top + 232, 1)
    cut = 880
    d.line(cut, top + 100, cut, top + 206, stroke=RED, sw=4, dash="12 8")
    d.text(cut - 40, top + 246, "cut here, only if needed", size=T_MIN, anchor="end",
           weight=700, fill=RED)
    callout(d, cut, top + 232, 2)
    bench_tag(d, 1150, top + 64, "check on the bench", anchor="end")

    # ---- heater: two E0508 ferrules
    py = top + 290
    d.panel(30, py, 560, d.h - py - 16)
    d.text(54, py + 54, "Heater", size=36, weight=700)
    for i in range(2):
        yy = py + 170 + i * 120
        d.line(70, yy, 300, yy, stroke=WIRE_RED, sw=12)
        d.rect(300, yy - 18, 46, 36, fill=PANEL, stroke=GREY, sw=3, rx=6)    # collar
        d.rect(346, yy - 10, 150, 20, fill=STEEL, stroke=GREY, sw=3)         # 8 mm tube
    d.dim_h(py + 380, 346, 496, "8 mm", size=T_MIN)
    d.text(54, py + 470, "E0508 ferrule ×2", size=T_LAB, weight=700)
    d.text(54, py + 510, "no stray strands", size=T_LAB, weight=600, fill=MUTED)
    callout(d, 530, py + 230, 2)

    # ---- thermistor: PH2.0 2-pin housing
    qx = 610
    d.panel(qx, py, 560, d.h - py - 16)
    d.text(qx + 24, py + 54, "Thermistor", size=36, weight=700)
    hx0, hy0 = qx + 300, py + 150
    d.rect(hx0, hy0, 150, 170, fill="#F2F2EE", stroke=GREY, sw=3, rx=6)
    for i in range(2):
        cx = hx0 + 45 + i * 60
        d.rect(cx - 16, hy0 + 30, 32, 110, fill=PANEL, stroke=GREY, sw=2, rx=3)
        d.path(f"M {qx + 40} {hy0 + 60 + i * 50} C {qx + 180} {hy0 + 60 + i * 50} "
               f"{cx - 60} {hy0 + 85} {cx} {hy0 + 85}", stroke="#BDBDBD", sw=6)
    d.dim_h(hy0 + 200, hx0 + 45, hx0 + 105, "", size=T_MIN)
    d.text(hx0 + 75, hy0 + 250, "2.0 mm", size=T_MIN, anchor="middle", weight=500, fill=MUTED)
    d.text(qx + 24, py + 470, "JST-PH2.0, 2-pin", size=T_LAB, weight=700)
    d.text(qx + 24, py + 510, "XH2.5 will not fit TH0", size=T_LAB, weight=700, fill=RED)
    callout(d, qx + 520, py + 230, 2)
    return d


# ============================================================= diagram 806 ===
def d806_led_index() -> Doc:
    d = Doc(1000, "Toolhead LED index 2 and 3, seen from the front of the printer")
    top = step_header(d, "Toolhead LEDs from the front")
    d.panel(30, top + 16, 1140, 870)

    # Stealthburner front, schematic (blue accent body = orange)
    cx = 600
    body = [(cx - 230, 170), (cx + 230, 170), (cx + 290, 330), (cx + 250, 620), (cx + 170, 760),
            (cx + 60, 760), (cx + 30, 700), (cx - 30, 700), (cx - 60, 760), (cx - 170, 760),
            (cx - 250, 620), (cx - 290, 330)]
    d.poly(body, fill=ORANGE_F, stroke=ORANGE, sw=5)
    d.circle(cx, 420, 130, fill=PANEL, stroke=ORANGE, sw=4)
    # nozzle
    d.poly([(cx - 22, 700), (cx + 22, 700), (cx + 10, 760), (cx - 10, 760)], fill="#C9A13B",
           stroke=INK, sw=2)
    # the two toolhead LEDs in the bottom corners, either side of the nozzle, each pushed
    # in from the outside (Do 1); index 2 on your right, 3 on your left (Do 2)
    for side, idx in ((-1, 3), (1, 2)):
        lx = cx + side * 115
        d.circle(lx, 700, 30, fill="#FFF3B0", stroke=INK, sw=3)
        arrow(d, lx + side * 230, 700, lx + side * 40, 700, col=INK, sw=6)
        label_bg(d, lx + side * 150, 640, f"LED {idx}", size=40, weight=800, bg=PANEL)
    callout(d, cx + 115 + 175, 700, 1)
    callout(d, cx - 115 - 175, 700, 1)

    d.text(200, 830, "your left: LED 3", size=36, anchor="middle", weight=800)
    d.text(985, 830, "your right: LED 2", size=36, anchor="middle", weight=800)
    callout(d, cx - 115 - 150 - 92, 627, 2)
    callout(d, cx + 115 + 150 + 92, 627, 2)
    d.text(cx, 880, "you, facing the printer", size=T_LAB, anchor="middle", weight=700,
           fill=MUTED)
    d.text(cx, 950, "SB p.56 is drawn from behind, upside down", size=T_MIN,
           anchor="middle", weight=600, fill=MUTED)
    return d


# ================================================================ registry ===
DIAGRAMS = [
    {
        "n": 801,
        "file": "801-fan-adapter-on-5015.svg",
        "title": "Fan adapter on the 5015",
        "fn": d801_fan_adapter,
        "shows": [
            "The Stealthburner body from behind with the 5015 in its upper pocket and the "
            "triangular SBurnerFanAdapter V2.0 lying flat on the fan's back, its two end holes "
            "over the two body holes SB p.64's M3×6 FHCS use, two M3×10 flat-head screws "
            "through both.",
            "P1's pins point back, at the toolboard, on the toolboard side of the body.",
            "Callouts 1 and 2 are the Do numbers of Step 08.44.",
        ],
        "insert": [
            ("08-toolhead.md", "Step 08.44", "first image: what the hands do"),
        ],
        "verify": [
            "Body, fan and board outlines are schematic. Hole positions follow SB p.64 (the "
            "two M3×6 FHCS it replaces) and LDO's wiring guide (two M3×10 FHCS directly on the "
            "back of the 5015); that the board's two holes land on those two fan holes, and "
            "the board's exact rotation, are drawn from that and the board photo, not from a "
            "photo of it mounted (none published).",
        ],
    },
    {
        "n": 802,
        "file": "802-ground-lug-motor-end.svg",
        "title": "Ground wire, motor end",
        "fn": d802_ground_lug,
        "shows": [
            "The extruder from behind after LDO's toolboard_ground_routing.jpg: toolboard on "
            "the left edge, the ground wire from the lower board screw round the motor can to "
            "a ring lug on the motor's lower ear, nearest the chain anchor.",
            "The lug bent up along the can, clear of the anchor below; a small Wrong panel "
            "shows it pointing down into the anchor.",
            "Callouts 1 and 2 are the Do numbers of Step 08.53.",
        ],
        "insert": [
            ("08-toolhead.md", "Step 08.53", "first image: what the hands do"),
        ],
        "verify": [
            "Schematic proportions. What holds the lug (the supplied short screw, or a nut on "
            "the tip of the front M3×8 that shares the lower ear, as LDO's top-down photo may "
            "show) is unpublished: drawn generic and tagged for the bench.",
        ],
    },
    {
        "n": 803,
        "file": "803-cartridge-he0-th0.svg",
        "title": "Cartridge up, leads in",
        "fn": d803_cartridge_leads,
        "shows": [
            "Side view from the toolboard side, front on the left: the tool cartridge pushed "
            "up under the extruder, held by the cartridge, not the nozzle (the body screws at 08.62 hold it; "
            "what holds it before then is tagged for the bench); the heater pair with "
            "ferrules into the HE0 screw terminal; the thermistor pair into TH0, the 2-pin "
            "socket to the left of HE0 (board pinout).",
            "Callouts 1 to 3 are the Do numbers of Step 08.61.",
        ],
        "insert": [
            ("08-toolhead.md", "Step 08.61", "first image: what the hands do"),
        ],
        "verify": [
            "Schematic: board, terminal and socket sizes are not to scale. No screw heads or "
            "keyholes are drawn: the cartridge's four M3×8 sit in Ø5.8 counterbores in its top "
            "(STL) and clamp the Revo heatsink (SB p.50). TH0-left-of-HE0 and the board's front edge "
            "forward are from LDO's pinout and ground-routing photo.",
        ],
    },
    {
        "n": 804,
        "file": "804-cover-and-header.svg",
        "title": "Cover, header, body",
        "fn": d804_body_header,
        "shows": [
            "Top: the extruder from the front with the latch open (closed again after), the "
            "M3×16 straight in through the front access hole (SB p.37-38) and the M3×6 BHCS "
            "into the cable cover's side wall, low at the front (SB p.38).",
            "Bottom: side view from the toolboard side, front on the left: the fan adapter's P1 "
            "pins pointing back, the toolboard's socket on its front edge, A1/A2 row on top and "
            "the 24V row at the bottom, the body pushed straight back; two M3×25 upper and two "
            "M3×50 lower from the front.",
            "Callouts 1 to 3 are the Do numbers of Step 08.62.",
        ],
        "insert": [
            ("08-toolhead.md", "Step 08.62", "first image: what the hands do"),
        ],
        "verify": [
            "Schematic outlines. Reaching the M3×6 BHCS with the toolhead on the carriage is "
            "the step's (verify on bench) and is tagged. The socket's key is not drawn: no "
            "source shows where it sits. Row order is from LDO's board pinout.",
        ],
    },
    {
        "n": 805,
        "file": "805-revo-lead-ends.svg",
        "title": "Ends for HE0 and TH0",
        "fn": d805_revo_leads,
        "shows": [
            "Top: the HeaterCore's heater and thermistor leads, each ending in a Micro-Fit "
            "plug (E3D Revo Voron page), marked never cut; the 1 m extension cables beyond "
            "them, with the cut line at their board end, only if LDO's cables do not mate.",
            "Bottom: the heater pair ending in two E0508 ferrules (8 mm tube); the thermistor "
            "pair in a 2-pin JST-PH2.0 housing (2.0 mm pitch), with XH2.5 marked as not "
            "fitting TH0.",
            "Callouts 1 and 2 are the Do numbers of Step 08.33.",
        ],
        "insert": [
            ("08-toolhead.md", "Step 08.33", "first image: what the hands do"),
        ],
        "verify": [
            "What LDO packs for the Revo option is the step's (verify on bench); tagged. "
            "Ferrule collar and housing colours are not specified by the sources.",
        ],
    },
    {
        "n": 806,
        "file": "806-toolhead-led-index.svg",
        "title": "Toolhead LEDs from the front",
        "fn": d806_led_index,
        "shows": [
            "The Stealthburner from the front: the two toolhead LEDs in the bottom corners "
            "either side of the nozzle, pushed in from the outside; index 2 on your right "
            "(SB p.54/p.56 'TOOLHEAD LED RIGHT'), index 3 on your left.",
            "Callouts 1 and 2 are the Do numbers of Step 08.37.",
        ],
        "insert": [
            ("08-toolhead.md", "Step 08.37", "first image, before the p.56 crop"),
        ],
        "verify": [
            "Body outline schematic. Right = your right is read from the SB manual's own "
            "views: p.62 (from behind, upright) draws wires that 'exit on the right side' "
            "leaving to the drawing's left, and p.56 draws the body from behind upside down "
            "(LED pockets next to the 4010 pocket, the 5015 at the far end), so its RIGHT "
            "label sits on your right. No photo of a labelled build was found.",
        ],
    },
]
