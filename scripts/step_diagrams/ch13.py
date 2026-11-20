"""Chapter 13 step diagrams (1301 onwards): first power-on, homing, Z=0, first print and
the nozzle-scrubber measurements.

Drawn after the Voron startup wizard (docs.vorondesign.com/build/startup), the Voron
manual p.161 (Z endstop), LDO's Rev D wiring photos and build-plate mapping, the LDO
`leviathan-printer-rev-d-sbv2.cfg` (667521d) and the chapter's own steps. Numbered
callouts are the Do numbers of the step each diagram is placed in.
"""
import math

import draw_diagrams as dd

FIL = "#1F2329"           # black ASA filament
TAPE_F = "#F4E2B8"        # masking tape
TAPE = "#B8913E"
SKIN_F = "#F6EDE4"        # a hand: light fill, ink outline


def _arrow(d, x0, y0, x1, y1, col=dd.INK, sw=6, mk="arw", dash=None):
    d.path(f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}", stroke=col, sw=sw, marker=mk,
           dash=dash)


def _hand(d, x, y, ang_deg, s=1.0):
    """A flat hand seen from the side, fingers pointing along ang_deg, palm facing
    'up' on screen when ang_deg is 0. (x, y) is the middle of the palm's top edge."""
    a = math.radians(ang_deg)
    ux, uy = math.cos(a), math.sin(a)
    vx, vy = -uy, ux                                  # 'down' from the palm

    def P(u, v):
        return x + (u * ux + v * vx) * s, y + (u * uy + v * vy) * s
    pts = [P(-70, 0), P(60, 0), P(88, 4), P(96, 14), P(88, 24), P(60, 28),
           P(-20, 30), P(-60, 40), P(-160, 92), P(-176, 62), P(-80, 16)]
    dpath = "M " + " L ".join(f"{px:.1f} {py:.1f}" for px, py in pts) + " Z"
    d.path(dpath, fill=SKIN_F, stroke=dd.INK, sw=3)
    # thumb along the top, two finger creases
    t0, t1, t2 = P(-40, 0), P(-6, -14), P(30, -4)
    d.path(f"M {t0[0]:.1f} {t0[1]:.1f} Q {t1[0]:.1f} {t1[1]:.1f} {t2[0]:.1f} {t2[1]:.1f}",
           fill=SKIN_F, stroke=dd.INK, sw=3)
    for v in (9, 19):
        c0, c1 = P(30, v), P(80, v)
        d.line(*c0, *c1, stroke=dd.MUTED, sw=1.8)


def _nozzle(d, cx, tip_y, w=60, h=70, col=dd.GREY, fill=dd.GREY_F):
    """A nozzle drawn point down, tip at (cx, tip_y)."""
    d.poly([(cx - w / 2, tip_y - h), (cx + w / 2, tip_y - h), (cx + w / 6, tip_y - 12),
            (cx + 6, tip_y), (cx - 6, tip_y), (cx - w / 6, tip_y - 12)], fill=fill,
           stroke=col, sw=3)


def _vdim(d, x, y1, y2, label, col=dd.INK, side=1, size=dd.T_LAB, weight=700, tick=12):
    """Vertical dimension with end ticks and a label beside it."""
    d.line(x, y1, x, y2, stroke=col, sw=3)
    for y in (y1, y2):
        d.line(x - tick, y, x + tick, y, stroke=col, sw=3)
    anchor = "start" if side > 0 else "end"
    d.text(x + side * (tick + 10), (y1 + y2) / 2 + size * 0.35, label, size=size,
           anchor=anchor, weight=weight, fill=col)


def _hdim(d, y, x1, x2, label, col=dd.INK, above=True, size=dd.T_LAB, weight=700,
          tick=12):
    d.line(x1, y, x2, y, stroke=col, sw=3)
    for x in (x1, x2):
        d.line(x, y - tick, x, y + tick, stroke=col, sw=3)
    d.text((x1 + x2) / 2, y - 18 if above else y + size + 12, label, size=size,
           anchor="middle", weight=weight, fill=col)


def _letter(d, x, y, s, col=dd.INK, r=27):
    """A measured quantity's letter in a white box with a coloured border."""
    d.rect(x - r, y - r, 2 * r, 2 * r, fill=dd.PANEL, stroke=col, sw=3.5, rx=8)
    d.text(x, y + 12, s, size=36, anchor="middle", weight=800, fill=col, italic=True)


def _cross(d, x, y, r=22, col=dd.RED, sw=7):
    d.line(x - r, y - r, x + r, y + r, stroke=col, sw=sw)
    d.line(x - r, y + r, x + r, y - r, stroke=col, sw=sw)


# ============================================================= diagram 1301 ===
def d1301_hand_under_gantry() -> dd.Doc:
    d = dd.Doc(1000, "A hand under the gantry before M84, then lower it to a third")
    top = dd.step_header(d, "Hand under the gantry first")
    k = 1.55                                          # px per mm of Z
    plate_y = 860                                     # plate top
    fx0, fx1 = 70, 820                                # frame verticals (centres)

    def zy(z):
        return plate_y - z * k

    # frame: two verticals and the top extrusion, front view
    for fx in (fx0, fx1):
        d.rect(fx - 16, top + 20, 32, 940 - top - 20, fill=dd.BLUE_F, stroke=dd.BLUE, sw=3)
    d.rect(fx0 - 16, top + 20, fx1 - fx0 + 32, 30, fill=dd.BLUE_F, stroke=dd.BLUE, sw=3)
    # bed: plate on its extrusions, fixed
    d.rect(170, plate_y, 550, 16, fill=dd.GREY_F, stroke=dd.GREY, sw=3)
    d.rect(240, plate_y + 16, 34, 40, fill=dd.BLUE_F, stroke=dd.BLUE, sw=2.5)
    d.rect(616, plate_y + 16, 34, 40, fill=dd.BLUE_F, stroke=dd.BLUE, sw=2.5)
    dd.label_bg(d, 445, plate_y + 52, "plate", size=dd.T_MIN, fill=dd.MUTED, weight=600)

    def gantry(z_tip, ghost=False):
        ty = zy(z_tip)                                # nozzle tip
        by = ty - 125                                 # gantry beam, top
        op = 0.35 if ghost else None
        dash = "14 10" if ghost else None
        d.rect(fx0 + 16, by, fx1 - fx0 - 32, 34, fill="none" if ghost else dd.BLUE_F,
               stroke=dd.BLUE, sw=3, dash=dash, op=op)
        cx = 445
        d.rect(cx - 60, by - 20, 120, 115, fill="none" if ghost else dd.BLACKPART_F,
               stroke=dd.BLACKPART, sw=3, rx=10, dash=dash, op=op)
        if not ghost:
            _nozzle(d, cx, ty, w=34, h=30)
        return by

    by0 = gantry(300, ghost=True)
    by = gantry(100)
    # lowered by hand: arrow from the old height to the new
    _arrow(d, 640, by0 + 40, 640, by - 20, sw=5)
    # hand flat under the beam, left of the toolhead
    _hand(d, 245, by + 34, 0, 1.0)
    dd.callout(d, 150, by + 150, 1)
    # about 100 mm, nozzle to plate
    _vdim(d, 520, zy(100), plate_y, "about 100 mm", side=1)
    # push the toolhead to the middle
    _arrow(d, 760, by + 70, 525, by + 70, col=dd.MUTED, sw=4, mk="arwm", dash="12 9")
    dd.callout(d, 445, by - 70, 2)

    # legend, right-hand column
    lx = 860
    d.text(lx, top + 110, "M84", size=40, weight=800, family=dd.MONO)
    d.text(lx, top + 160, "lets go of", size=dd.T_LAB, weight=600)
    d.text(lx, top + 200, "every motor:", size=dd.T_LAB, weight=600)
    d.text(lx, top + 240, "the gantry", size=dd.T_LAB, weight=700, fill=dd.RED)
    d.text(lx, top + 280, "sinks", size=dd.T_LAB, weight=700, fill=dd.RED)
    y = dd.legend_row(d, lx - 6, top + 430, 1, ["hand under,", "M84, lower"],
                      size=dd.T_MIN)
    dd.legend_row(d, lx - 6, y + 40, 2, ["toolhead to", "the middle"], size=dd.T_MIN)
    return d


# ============================================================= diagram 1302 ===
def d1302_rotation_distance_tape() -> dd.Doc:
    d = dd.Doc(1060, "Tape at 120 mm above the extruder entrance; after 100 mm, R is what is left")
    top = dd.step_header(d, "Tape at 120 mm, then read R")
    k = 4.2                                            # px per mm of filament
    entry = 880                                        # the collet, extruder entrance
    tube_top = top + 90
    tube_end = entry - 140 * k                          # the PTFE, lifted clear

    def column(cx, tape_mm, title):
        d.text(cx, top + 62, title, size=36, weight=700, anchor="middle")
        # Clockwork 2.5 top and its collet
        d.rect(cx - 130, entry + 22, 260, 64, fill=dd.BLACKPART_F, stroke=dd.BLACKPART,
               sw=3, rx=10)
        d.rect(cx - 26, entry, 52, 22, fill=dd.GREY_F, stroke=dd.GREY, sw=3, rx=3)
        # the filament, bare from the collet up to the lifted PTFE, then inside it
        d.line(cx, entry + 50, cx, tube_top, stroke=FIL, sw=7, cap="butt")
        d.rect(cx - 17, tube_top, 34, tube_end - tube_top, fill=dd.STEEL, stroke=dd.GREY,
               sw=3, op=0.8)
        # steel rule beside the filament, zero at the entrance
        rx = cx + 40
        d.rect(rx, entry - 130 * k, 34, 130 * k, fill=dd.GREY_F, stroke=dd.GREY, sw=2.5)
        for mm in range(0, 131, 10):
            y = entry - mm * k
            d.line(rx, y, rx + (22 if mm % 50 == 0 else 13), y, stroke=dd.INK, sw=2)
        # tape flag on the filament
        ty = entry - tape_mm * k
        d.rect(cx - 74, ty - 16, 86, 32, fill=TAPE_F, stroke=TAPE, sw=3, rx=3)
        return ty

    # before
    cx1 = 250
    ty1 = column(cx1, 120, "Before")
    _vdim(d, cx1 + 120, ty1, entry, "120 mm", side=1)
    dd.callout(d, cx1 - 120, ty1, 3)
    d.text(cx1 - 40, tube_top + 70, "PTFE,", size=dd.T_MIN, anchor="end", weight=700,
           fill=dd.MUTED)
    d.text(cx1 - 40, tube_top + 108, "lifted off", size=dd.T_MIN, anchor="end",
           weight=700, fill=dd.MUTED)
    # after
    cx2 = 850
    ty2 = column(cx2, 20, "After")
    _vdim(d, cx2 + 120, ty2, entry, "R", side=1, size=44)
    d.text(cx2 - 90, ty2 + 11, "about 20 mm", size=dd.T_MIN, anchor="end", weight=600,
           fill=dd.MUTED)
    # between: the extrude
    _arrow(d, 480, 560, 610, 560, sw=6)
    d.text(545, 520, "G1 E100 F60", size=dd.T_MIN, anchor="middle", weight=700,
           family=dd.MONO)
    # the entrance
    d.text(560, entry - 150, "extruder", size=dd.T_MIN, anchor="middle", weight=700)
    d.text(560, entry - 112, "entrance", size=dd.T_MIN, anchor="middle", weight=700)
    d.leader(cx1 + 28, entry + 6, 480, entry - 110, col=dd.INK)
    dd.step_note(d, "what went in = 120 − R", size=dd.T_LAB)
    return d


# ============================================================= diagram 1303 ===
def d1303_probe_under_nozzle() -> dd.Doc:
    d = dd.Doc(1000, "The nozzle-probe shaft directly under the nozzle, 2 to 3 mm behind the plate")
    top = dd.step_header(d, "Shaft under the nozzle")
    py = top + 18

    # ---- left: from above, rear at the top
    d.panel(30, py, 420, 870)
    d.text(240, py + 52, "From above", size=dd.T_LAB, anchor="middle", weight=700)
    d.text(240, py + 92, "rear", size=dd.T_MIN, anchor="middle", fill=dd.MUTED)
    s = 1.0                                            # px per mm, plate 350 wide
    px0, py0 = 65, py + 200                             # plate's rear-left corner
    # bed extrusions run front to back under the plate and past its rear edge
    ex = [px0 + 100 * s, px0 + 250 * s]
    for x in ex:
        d.rect(x - 10, py + 120, 20, py0 + 350 + 30 - py - 120, fill=dd.BLUE_F,
               stroke=dd.BLUE, sw=2.5)
    d.rect(px0, py0, 350 * s, 350 * s, fill=dd.GREY_F, stroke=dd.GREY, sw=3, op=0.92)
    dd.label_bg(d, px0 + 175, py0 + 210, "plate", size=dd.T_MIN, fill=dd.MUTED,
                weight=600, bg=dd.GREY_F)
    # the probe on the right extrusion's inner face, just behind the plate
    pb = (ex[1] - 10 - 22, py0 - 30)
    d.rect(pb[0], pb[1], 22, 24, fill=dd.BLACKPART, stroke=dd.INK, sw=2)
    d.circle(pb[0] + 11, pb[1] + 18, 5, fill=dd.STEEL, stroke=dd.INK, sw=2)
    # toolhead parked at the rear-right after G28 X Y, jogged left to the probe
    hx, hy = px0 + 350 * s + 10, py0 - 18
    d.circle(hx, hy, 15, fill=dd.ORANGE_F, stroke=dd.ORANGE, sw=3)
    _arrow(d, hx - 22, hy - 30, pb[0] + 20, hy - 30, sw=6)
    dd.callout(d, (hx + pb[0]) / 2 + 30, hy - 82, 1)
    d.text(240, py + 650, "nozzle probe", size=dd.T_MIN, anchor="middle", weight=700)
    d.leader(pb[0] + 6, pb[1] + 26, 210, py + 620, col=dd.INK)
    d.text(240, py + 690, "on the right", size=dd.T_MIN, anchor="middle", fill=dd.MUTED)
    d.text(240, py + 726, "bed extrusion", size=dd.T_MIN, anchor="middle", fill=dd.MUTED)
    d.text(240, py + 800, "front", size=dd.T_MIN, anchor="middle", fill=dd.MUTED)

    # ---- right: from the middle of the bed, looking right; rear to the left
    ox = 470
    d.panel(ox, py, 700, 870)
    d.text(ox + 350, py + 52, "From the side", size=dd.T_LAB, anchor="middle", weight=700)
    ey = py + 620                                      # extrusion top
    k = 6.0
    # bed extrusion (blue) along Y
    d.rect(ox + 190, ey, 490, 20 * k, fill=dd.BLUE_F, stroke=dd.BLUE, sw=3)
    # plate: rear edge at xe, on a spacer
    xe = ox + 400
    gap = 26                                           # 2 to 3 mm, drawn wide
    d.rect(xe + 7 * k - 30, ey - 8 * k, 60, 8 * k, fill=dd.GREY_F, stroke=dd.GREY, sw=2.5)
    d.rect(xe, ey - 8 * k - 10 * k, 300, 10 * k, fill=dd.GREY_F, stroke=dd.GREY, sw=3)
    dd.label_bg(d, xe + 175, ey - 13 * k + 12, "plate", size=dd.T_MIN, fill=dd.MUTED,
                weight=600, bg=dd.GREY_F)
    # probe body against the extrusion's inner face, collar on top, shaft up
    sx = xe - gap - 7                                  # shaft centre
    bx0, bx1 = sx - 120, sx + 40
    d.rect(bx0, ey - 30, bx1 - bx0, 150, fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=3.5,
           rx=10)
    d.rect(sx - 26, ey - 62, 52, 32, fill=dd.STEEL, stroke=dd.GREY, sw=3, rx=4)
    shaft_top = ey - 8 * k - 10 * k - 26
    d.rect(sx - 7, shaft_top, 14, ey - 62 - shaft_top, fill=dd.STEEL, stroke=dd.GREY, sw=3)
    # the two M3×25 heads, into the extrusion's slot
    for hx2 in (bx0 + 40, bx0 + 100):
        d.circle(hx2, ey + 60, 17, fill=dd.GREY_F, stroke=dd.GREY, sw=3)
        d.circle(hx2, ey + 60, 6, fill=dd.GREY, stroke="none", sw=0)
    dd.callout(d, ox + 70, ey + 10, 2)
    d.text(ox + 30, ey + 90, "two", size=dd.T_MIN, weight=700)
    d.text(ox + 30, ey + 128, "M3×25", size=dd.T_MIN, weight=700)
    d.leader(bx0 + 28, ey + 62, ox + 140, ey + 100, col=dd.INK)
    # slide along the extrusion
    sy = ey + 175
    _arrow(d, bx0 + 70, sy, bx0 - 30, sy, col=dd.MUTED, sw=5, mk="arwm")
    _arrow(d, bx0 + 70, sy, bx0 + 170, sy, col=dd.MUTED, sw=5, mk="arwm")
    d.text(bx0 + 70, sy + 45, "slide", size=dd.T_MIN, anchor="middle", weight=600,
           fill=dd.MUTED)
    # nozzle above the shaft, centre line
    tip = shaft_top - 70
    d.rect(sx - 70, py + 110, 140, tip - 60 - py - 110, fill=dd.BLACKPART_F,
           stroke=dd.BLACKPART, sw=3, rx=10)
    _nozzle(d, sx, tip, w=40, h=60)
    d.line(sx, tip + 8, sx, ey - 62, stroke=dd.OK, sw=3.5, dash="12 9")
    d.text(sx + 90, tip - 40, "nozzle", size=dd.T_MIN, weight=700)
    d.text(sx + 90, tip + 2, "over the shaft", size=dd.T_MIN, weight=700, fill=dd.OK)
    # the gap to the plate's rear edge
    gy = shaft_top - 22
    for x in (sx + 7, xe):
        d.line(x, gy - 14, x, (shaft_top - 4) if x < xe else (ey - 18 * k - 4),
               stroke=dd.INK, sw=2)
    _arrow(d, sx - 50, gy, sx + 5, gy, sw=3)
    _arrow(d, xe + 55, gy, xe + 2, gy, sw=3)
    d.text(xe + 66, gy + 11, "2 to 3 mm", size=dd.T_LAB, weight=800)
    d.text(ox + 30, py + 850, "rear", size=dd.T_MIN, fill=dd.MUTED)
    d.text(ox + 680, py + 850, "front", size=dd.T_MIN, anchor="end", fill=dd.MUTED)
    return d


# ============================================================= diagram 1304 ===
def d1304_paper_test() -> dd.Doc:
    d = dd.Doc(1060, "The paper test: TESTZ step sizes and the first drag")
    top = dd.step_header(d, "Paper test: step down to the first drag")
    py = top + 18

    # ---- top left: nozzle over the paper on the plate
    plate_y = py + 470
    cx = 270
    d.rect(40, plate_y, 470, 34, fill=dd.GREY_F, stroke=dd.GREY, sw=3)
    d.rect(60, plate_y - 10, 430, 10, fill=dd.PANEL, stroke=dd.INK, sw=2.5)
    d.rect(cx - 70, py + 120, 140, 200, fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=3,
           rx=10)
    _nozzle(d, cx, plate_y - 60, w=56, h=90)
    _arrow(d, cx, plate_y - 52, cx, plate_y - 16, sw=4)
    d.text(470, plate_y - 34, "paper", size=dd.T_LAB, anchor="end", weight=700)
    dd.callout(d, 90, plate_y - 60, 1)
    # slide the paper
    _arrow(d, 150, plate_y + 80, 70, plate_y + 80, col=dd.MUTED, sw=5, mk="arwm")
    _arrow(d, 150, plate_y + 80, 230, plate_y + 80, col=dd.MUTED, sw=5, mk="arwm")
    d.text(250, plate_y + 92, "slide it", size=dd.T_MIN, weight=600, fill=dd.MUTED)

    # ---- top right: the step sizes
    lx = 560
    dd.callout(d, lx + 28, py + 70, 2)
    rows = [("TESTZ Z=-1", "down, until close", "big"),
            ("TESTZ Z=-0.1", "down, to the drag", "small"),
            ("TESTZ Z=0.1", "back up", "up")]
    y = py + 160
    for cmd, what, kind in rows:
        ax = lx + 20
        if kind == "big":
            _arrow(d, ax, y - 44, ax, y + 40, sw=4)
        elif kind == "small":
            _arrow(d, ax, y - 4, ax, y + 26, sw=4)
        else:
            _arrow(d, ax, y + 26, ax, y - 18, sw=4, col=dd.MUTED, mk="arwm")
        d.text(lx + 60, y, cmd, size=dd.T_LAB, weight=700, family=dd.MONO)
        d.text(lx + 60, y + 42, what, size=dd.T_MIN, weight=600, fill=dd.MUTED)
        y += 130

    # ---- bottom: three feels
    by = py + 590
    d.line(40, by, d.w - 40, by, stroke=dd.RULE, sw=2)
    cols = [(40, "slides free", "keep going", dd.MUTED, None),
            (420, "light drag", "ACCEPT", dd.OK, 3),
            (800, "pinned", "back up", dd.RED, None)]
    for x0, feel, act, col, n in cols:
        w = 360
        cxx = x0 + w / 2
        gap = {dd.MUTED: 40, dd.OK: 12, dd.RED: 0}[col]
        p_y = by + 210
        d.rect(x0 + 30, p_y, w - 60, 22, fill=dd.GREY_F, stroke=dd.GREY, sw=2.5)
        d.rect(x0 + 50, p_y - 8, w - 100, 8, fill=dd.PANEL, stroke=dd.INK, sw=2)
        tip = p_y - 8 - gap
        if col == dd.RED:
            tip = p_y - 3
        _nozzle(d, cxx, tip, w=40, h=60)
        d.text(cxx, by + 60, feel, size=dd.T_LAB, anchor="middle", weight=700, fill=col)
        d.text(cxx, by + 300, act, size=dd.T_LAB, anchor="middle", weight=800,
               fill=col, family=dd.MONO if act == "ACCEPT" else dd.FONT)
        if n:
            dd.callout(d, x0 + w - 30, by + 50, n)
    return d


# ============================================================= diagram 1305 ===
def d1305_scrubber_measurements() -> dd.Doc:
    d = dd.Doc(1020, "Where H, w, d, G and O are measured behind the plate")
    top = dd.step_header(d, "H, w, d, G and O")
    k = 9.0                                            # px per mm
    ey = 800                                           # left bed extrusion top
    xe = 430                                           # plate's rear edge
    H, dd_, O, OM = 20.0, 3.0, 4.5, 25.0               # d drawn 3 mm: not to scale
    plate_top = ey - H * k
    nx = xe + O * k                                    # nozzle at full Y
    ox = nx + OM * k                                   # Omron centre, 25 mm behind
    # bed extrusion along Y (rear to the right), plate stack ending at its rear edge
    d.rect(60, ey, 1080, 100, fill=dd.BLUE_F, stroke=dd.BLUE, sw=3)
    d.path(f"M 50 {ey + 100} L 1150 {ey + 100}", stroke=dd.BG, sw=8)
    d.path(f"M 50 {ey + 104} L 300 {ey + 94} L 600 {ey + 104} L 900 {ey + 94} "
           f"L 1150 {ey + 104}", stroke=dd.BLUE, sw=3)
    dd.label_bg(d, 840, ey + 64, "left bed extrusion", size=dd.T_MIN, fill=dd.BLUE,
                bg=dd.BLUE_F)
    d.rect(xe - 7 * k - 30, ey - 8 * k, 60, 8 * k, fill=dd.GREY_F, stroke=dd.GREY, sw=2.5)
    d.rect(60, ey - 8 * k - 10 * k, xe - 60, 10 * k, fill=dd.GREY_F, stroke=dd.GREY, sw=3)
    d.rect(60, plate_top, xe - 60, H * k - 18 * k, fill=dd.PANEL, stroke=dd.INK, sw=2.5)
    dd.label_bg(d, 230, ey - 13 * k + 12, "plate", size=dd.T_MIN, fill=dd.MUTED,
                bg=dd.GREY_F)
    d.text(130, plate_top - 24, "flex plate", size=dd.T_MIN, weight=600, fill=dd.MUTED)
    # H at the rear edge
    _vdim(d, xe - 46, plate_top, ey, "", col=dd.ORANGE)
    _letter(d, xe - 100, (plate_top + ey) / 2 + 40, "H", col=dd.ORANGE)
    # toolhead at full Y, nozzle at Z0 (on the plate's level), Omron behind
    th_y = plate_top - 240
    d.rect(nx - 80, th_y, ox - nx + 170, 150, fill=dd.BLACKPART_F, stroke=dd.BLACKPART,
           sw=3, rx=12)
    d.text(nx + 30, th_y + 90, "toolhead", size=dd.T_MIN, weight=700)
    _nozzle(d, nx, plate_top, w=46, h=110)
    om_face = plate_top - dd_ * k
    d.rect(ox - 8.5 * k, th_y + 150, 17 * k, om_face - th_y - 150, fill=dd.GREY_F,
           stroke=dd.GREY, sw=3, rx=4)
    d.text(ox, th_y + 150 + 44, "Omron", size=dd.T_MIN, anchor="middle", weight=700)
    # level lines
    d.line(nx - 10, plate_top, ox + 130, plate_top, stroke=dd.FAINT, sw=2.5, dash="10 8")
    d.line(ox - 70, om_face, ox + 130, om_face, stroke=dd.FAINT, sw=2.5, dash="10 8")
    # d: Omron face above the nozzle tip
    _letter(d, ox + 175, (plate_top + om_face) / 2 - 10, "d", col=dd.BELT_B)
    d.line(ox + 120, om_face, ox + 120, plate_top, stroke=dd.BELT_B, sw=3)
    # G: Omron face above the extrusion top
    gx = ox + 30
    d.line(gx, om_face + 3, gx, ey - 3, stroke=dd.BELT_A, sw=3)
    for y in (om_face, ey):
        d.line(gx - 12, y, gx + 12, y, stroke=dd.BELT_A, sw=3)
    _letter(d, gx + 60, ey - 80, "G", col=dd.BELT_A)
    # O: nozzle past the plate's rear edge
    oy = plate_top + 60
    d.line(xe, plate_top - 4, xe, oy + 14, stroke=dd.FAINT, sw=2.5)
    d.line(nx, plate_top + 4, nx, oy + 14, stroke=dd.FAINT, sw=2.5)
    _hdim(d, oy, xe, nx, "", col=dd.OK, tick=10)
    _letter(d, nx + 40, oy + 56, "O", col=dd.OK)

    # wiper, measured in the hand
    wx, wy = 780, top + 40
    d.panel(wx - 10, wy - 20, 400, 250)
    d.text(wx + 10, wy + 26, "A1 wiper, in the hand", size=dd.T_MIN, weight=700)
    base_y = wy + 190
    d.rect(wx + 40, base_y - 14, 230, 14, fill=dd.BLACKPART, stroke=dd.INK, sw=2)
    for i in range(12):
        bx = wx + 50 + i * 19
        d.line(bx, base_y - 14, bx, base_y - 90, stroke=dd.MUTED, sw=6)
    _vdim(d, wx + 310, base_y - 90, base_y, "", col=dd.BROWN)
    _letter(d, wx + 355, base_y - 45, "w", col=dd.BROWN)

    d.text(60, top + 70, "rear", size=dd.T_MIN, fill=dd.MUTED)
    _arrow(d, 140, top + 60, 220, top + 60, col=dd.MUTED, sw=4, mk="arwm")
    dd.step_note(d, "d and G are read at Z10: take 10 off each", size=dd.T_LAB)
    return d


# ============================================================= diagram 1306 ===
def d1306_power_on_rocker() -> dd.Doc:
    d = dd.Doc(1000, "First power-on: hand on the inlet rocker, standing to the side, bay eyes only")
    top = dd.step_header(d, "Hand on the rocker, eyes on the bay")
    # the machine on its side, bay toward you; rear end on the left
    mx0, mx1, my0, my1 = 400, 1110, top + 90, top + 610
    d.rect(mx0, my0, mx1 - mx0, my1 - my0, fill=dd.PANEL, stroke=dd.BLUE, sw=18)
    d.rect(mx0 + 36, my0 + 36, mx1 - mx0 - 72, my1 - my0 - 72, fill="url(#hatch)",
           stroke=dd.RED, sw=4, dash="16 10")
    d.rect(mx0 + 190, my0 + 170, 330, 170, fill=dd.PANEL, stroke=dd.RED, sw=3, rx=10)
    d.text(mx0 + 355, my0 + 242, "live bay", size=dd.T_LAB + 4, anchor="middle",
           weight=800, fill=dd.RED)
    d.text(mx0 + 355, my0 + 294, "eyes only", size=dd.T_LAB + 4, anchor="middle",
           weight=800, fill=dd.RED)
    d.text(mx0 + 10, my1 + 50, "rear", size=dd.T_MIN, fill=dd.MUTED)
    d.text(mx1 - 10, my1 + 50, "front", size=dd.T_MIN, anchor="end", fill=dd.MUTED)
    # the inlet on the rear end, near the top corner; the mains lead in red
    ix, iy = mx0 - 9, my0 + 80
    d.rect(ix - 34, iy - 40, 34, 80, fill=dd.BLACKPART, stroke=dd.INK, sw=2.5, rx=4)
    d.rect(ix - 30, iy - 32, 20, 26, fill=dd.RED, stroke=dd.INK, sw=2)       # rocker
    d.path(f"M {ix - 34} {iy + 24} C {ix - 70} {iy + 40} {ix - 60} {iy + 120} "
           f"{ix - 60} {iy + 200} L {ix - 60} {my1 - 20} Q {ix - 60} {my1 + 20} "
           f"{ix - 100} {my1 + 20} L 40 {my1 + 20}", stroke=dd.RED, sw=7)
    d.text(44, my1 - 4, "mains lead", size=dd.T_MIN, weight=700, fill=dd.RED)
    d.text(ix - 82, iy + 92, "rocker", size=dd.T_MIN, anchor="end", weight=700)
    # you, standing to the side at the rear end, hand on the rocker
    hx, hy = 130, top + 250
    d.circle(hx, hy - 120, 32, fill=dd.PANEL, stroke=dd.INK, sw=4)
    d.line(hx, hy - 88, hx, hy + 110, stroke=dd.INK, sw=7)
    d.line(hx, hy + 110, hx - 38, hy + 260, stroke=dd.INK, sw=7)
    d.line(hx, hy + 110, hx + 38, hy + 260, stroke=dd.INK, sw=7)
    d.line(hx, hy - 50, ix - 56, iy - 20, stroke=dd.INK, sw=7)
    d.line(hx, hy - 40, hx - 44, hy + 60, stroke=dd.INK, sw=7)
    d.circle(ix - 48, iy - 20, 13, fill=SKIN_F, stroke=dd.INK, sw=3)
    # sight line into the bay
    _arrow(d, hx + 26, hy - 128, mx0 + 180, my0 + 200, col=dd.MUTED, sw=3, mk="arwm",
           dash="8 8")
    dd.callout(d, hx, hy - 200, 1)
    dd.callout(d, ix - 20, iy - 84, 2)
    dd.callout(d, mx0 + 100, my0 + 108, 3)
    # what the three numbers are
    ly = my1 + 120
    y = dd.legend_row(d, 40, ly, 1, ["one adult, nobody else in reach"], size=dd.T_MIN)
    y = dd.legend_row(d, 40, y + 30, 2, ["plug in, stand to the side, switch on"],
                      size=dd.T_MIN)
    dd.legend_row(d, 40, y + 30, 3, ["ten seconds: look, listen, smell"], size=dd.T_MIN)
    return d


# ============================================================= diagram 1307 ===
def d1307_first_layer_squish() -> dd.Doc:
    d = dd.Doc(780, "First-layer lines in section: too high, right, too low")
    top = dd.step_header(d, "First layer, cut across the lines")
    py = top + 30
    cols = [(40, "gaps", "too high", dd.RED, "high"),
            (420, "touching, each", "line still shows", dd.OK, "right"),
            (800, "ridged, glassy", "too low", dd.RED, "low")]
    for x0, l1, l2, col, kind in cols:
        w = 360
        d.panel(x0, py, w, 600)
        base = py + 340
        d.rect(x0 + 20, base, w - 40, 40, fill=dd.GREY_F, stroke=dd.GREY, sw=3)
        n = 4
        pitch = (w - 60) / n
        for i in range(n):
            cx = x0 + 30 + pitch * (i + 0.5)
            if kind == "high":
                d.circle(cx, base - 30, 28, fill=FIL, stroke=dd.INK, sw=2)
            elif kind == "right":
                d.add(f'<ellipse cx="{cx:.1f}" cy="{base - 16:.1f}" rx="{pitch / 2 + 2:.1f}" '
                      f'ry="21" fill="{FIL}" stroke="{dd.PANEL}" stroke-width="2.5"/>')
            else:
                d.rect(cx - pitch / 2 - 1, base - 20, pitch + 2, 20, fill=FIL, stroke=FIL, sw=1)
                d.add(f'<ellipse cx="{cx + pitch / 2:.1f}" cy="{base - 22:.1f}" rx="13" '
                      f'ry="12" fill="{FIL}" stroke="none"/>')
        d.text(x0 + w / 2, py + 90, l1, size=dd.T_LAB, anchor="middle", weight=700, fill=col)
        d.text(x0 + w / 2, py + 132, l2, size=dd.T_LAB, anchor="middle", weight=700,
               fill=col)
        if kind == "right":
            d.text(x0 + w / 2, base + 140, "keep this", size=dd.T_LAB, anchor="middle",
                   weight=800, fill=dd.OK)
        elif kind == "high":
            d.text(x0 + w / 2, base + 120, "closer:", size=dd.T_MIN, anchor="middle",
                   weight=600, fill=dd.MUTED)
            d.text(x0 + w / 2, base + 162, "Z_ADJUST=-0.01", size=dd.T_MIN, anchor="middle",
                   weight=700, family=dd.MONO)
        else:
            d.text(x0 + w / 2, base + 120, "further:", size=dd.T_MIN, anchor="middle",
                   weight=600, fill=dd.MUTED)
            d.text(x0 + w / 2, base + 162, "Z_ADJUST=0.01", size=dd.T_MIN, anchor="middle",
                   weight=700, family=dd.MONO)
    return d


DIAGRAMS = [
    {
        "n": 1301,
        "file": "1301-hand-under-gantry-m84.svg",
        "title": "Hand under the gantry first",
        "fn": d1301_hand_under_gantry,
        "shows": [
            "Front view of the machine: a hand flat under the gantry beam, `M84` sent, and "
            "the gantry lowered by hand from high up to a third of its travel, nozzle about "
            "100 mm above the plate (callout 1); the toolhead pushed to the middle (2).",
        ],
        "insert": [
            ("13-initial-startup.md", "Step 13.17", "the hand under the gantry and the "
             "lowered height"),
        ],
        "verify": [
            "Frame, gantry, toolhead and hand are schematic; the gantry's starting height "
            "is drawn high and dashed because the step does not say where it is.",
            "100 mm is the step's figure (a third of the 330 mm Z travel, "
            "`[stepper_z] position_max: 330`), drawn to scale against the plate.",
        ],
    },
    {
        "n": 1302,
        "file": "1302-rotation-distance-tape.svg",
        "title": "Tape at 120 mm, then read R",
        "fn": d1302_rotation_distance_tape,
        "shows": [
            "The top of the Clockwork 2.5 with its collet (the extruder entrance), the PTFE "
            "lifted off the filament, and a rule with zero at the entrance: tape at 120 mm "
            "before (callout 3), and after `G1 E100 F60` the tape at R, about 20 mm.",
        ],
        "insert": [
            ("13-initial-startup.md", "Step 13.40", "where the tape goes and where R is "
             "read from"),
        ],
        "verify": [
            "The Clockwork 2.5 body, collet and tube are schematic; lengths along the rule "
            "are to scale (120 mm, 20 mm).",
            "How far the PTFE has to be lifted to bare 120 mm of filament depends on the "
            "tube's slack at the park position: check on the bench.",
        ],
    },
    {
        "n": 1303,
        "file": "1303-probe-under-nozzle.svg",
        "title": "Shaft under the nozzle",
        "fn": d1303_probe_under_nozzle,
        "shows": [
            "From above: the toolhead after `G28 X Y` at the rear-right, jogged left along "
            "the rear to the nozzle probe on the right bed extrusion's inner face (callout "
            "1), after LDO's build-plate mapping.",
            "From the side, rear to the left: the probe body on the extrusion with its two "
            "M3×25 screws (2), slid until the shaft is directly under the nozzle, and the "
            "2 to 3 mm gap between the shaft and the plate's rear edge, after Voron manual "
            "p.161 and the startup wizard's Bed locating.",
        ],
        "insert": [
            ("13-initial-startup.md", "Step 13.24", "the nozzle over the shaft, the gap "
             "and the two screws"),
        ],
        "verify": [
            "The 2 to 3 mm gap is drawn wider than scale so it can be seen; the plate, "
            "spacer and probe body are schematic (the LDO body is taller than p.161's).",
            "Bed-extrusion spacing in the top view is schematic; the probe's side and "
            "face follow LDO's build-plate mapping and Ch 09 Step 09.30.",
        ],
    },
    {
        "n": 1304,
        "file": "1304-paper-test-testz.svg",
        "title": "Paper test: step down to the first drag",
        "fn": d1304_paper_test,
        "shows": [
            "The nozzle over a sheet of paper on the plate (callout 1); `TESTZ Z=-1` until "
            "close, `TESTZ Z=-0.1` to the drag, `TESTZ Z=0.1` to back up (2); three feels: "
            "slides free (keep going), light drag (`ACCEPT`, 3), pinned (back up).",
        ],
        "insert": [
            ("13-initial-startup.md", "Step 13.36", "the step sizes and the feel to "
             "accept at"),
        ],
        "verify": [
            "Heights are schematic; the step sizes are the wizard's and Klipper's "
            "`TESTZ` values as the step sends them.",
        ],
    },
    {
        "n": 1305,
        "file": "1305-scrubber-measurements.svg",
        "title": "H, w, d, G and O",
        "fn": d1305_scrubber_measurements,
        "shows": [
            "Side view behind the plate, rear to the right: H from the left bed "
            "extrusion's top to the flex plate's top at its rear edge; the toolhead at "
            "full Y with the nozzle O past the plate's edge; the Omron 25 mm behind it, its "
            "face d above the nozzle tip and G above the extrusion top; the A1 wiper's "
            "height w measured in the hand.",
        ],
        "insert": [
            ("13-initial-startup.md", "Step 13.45", "where H and w are measured"),
            ("13-initial-startup.md", "Step 13.46", "where d, G and O are measured"),
        ],
        "verify": [
            "d is drawn as 3 mm so it can be seen (expected about 0.6 mm); the plate "
            "stack, toolhead and wiper are schematic. H 20 mm, the Omron's 25 mm "
            "`y_offset` and 17 mm body and O 4.5 mm are drawn to scale.",
            "No callouts: the diagram serves two steps whose Do numbers differ, so the "
            "quantities carry their letters instead.",
        ],
    },
    {
        "n": 1306,
        "file": "1306-power-on-hand-on-rocker.svg",
        "title": "Hand on the rocker, eyes on the bay",
        "fn": d1306_power_on_rocker,
        "shows": [
            "The machine on its side with the bay toward you, the open bay marked live, "
            "eyes only; one adult standing beside the rear end, not in front of the bay "
            "(callout 1), hand on the inlet's rocker with the mains lead in red (2), "
            "looking into the bay (3).",
        ],
        "insert": [
            ("13-initial-startup.md", "Step 13.3", "where to stand and where the hand "
             "goes"),
        ],
        "verify": [
            "Which side the machine lies on is not stated (Step 10.1 'on its side'); the "
            "drawing lays it on its right side, which puts the rear end on your left and "
            "the inlet, at the rear-left corner (Ch 09 Step 09.2), at the top of that "
            "end. On its left side both are mirrored: check on the bench.",
            "The person, frame and bay are schematic; the bottom door is left out.",
        ],
    },
    {
        "n": 1307,
        "file": "1307-first-layer-squish.svg",
        "title": "First layer, cut across the lines",
        "fn": d1307_first_layer_squish,
        "shows": [
            "Three sections across first-layer lines on the plate: round lines with gaps "
            "(too high, `Z_ADJUST=-0.01` brings it closer), flattened lines that touch but "
            "each still shows (right), and a ridged, glassy sheet (too low, "
            "`Z_ADJUST=0.01`).",
        ],
        "insert": [
            ("13-initial-startup.md", "Step 13.42", "what the right squish looks like"),
        ],
        "verify": [
            "Line shapes are schematic, after the step's Check (no gaps, no ridging, each "
            "line visible) and Voron's first-print page (which shows no first-layer "
            "example).",
        ],
    },
]
