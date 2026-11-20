"""Chapter 06 step diagrams (601 onwards): Z axis install and the Z belts.

Drawn after the Voron 2.4r2 manual pages 111-122 (pinned de7e89d), the Voron docs'
secondary printer tuning page and the 2.4r2 CAD. Numbered callouts are the Do numbers
of the step each diagram is placed in.
"""
import math

import draw_diagrams as dd

BELT = "#2B3038"          # the 9 mm Z belt, drawn dark
RUBBER = "#3A3F47"        # rubber stopper


def _arrow(d, x0, y0, x1, y1, col=dd.INK, sw=6, mk="arw", dash=None):
    d.path(f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}", stroke=col, sw=sw, marker=mk,
           dash=dash)


def _rail_window(d, cx, y0, y1, pitch, rail_w, ext_w, first_hole_y, screwed):
    """Front view of a vertical with its MGN9 rail, holes every `pitch` px.
    `screwed(i)` says whether hole i (counted down the window) holds a screw."""
    d.rect(cx - ext_w / 2, y0, ext_w, y1 - y0, fill=dd.BLUE_F, stroke=dd.BLUE, sw=3)
    for sgn in (-1, 1):
        d.line(cx + sgn * ext_w * 0.31, y0, cx + sgn * ext_w * 0.31, y1, stroke=dd.BLUE,
               sw=1.6, op=0.55)
    d.rect(cx - rail_w / 2, y0, rail_w, y1 - y0, fill=dd.STEEL, stroke=dd.GREY, sw=2.5)
    holes = []
    y, i = first_hole_y, 0
    while y < y1 - 10:
        if y > y0 + 10:
            holes.append((i, y))
        y += pitch
        i += 1
    for i, y in holes:
        if screwed(i):
            d.circle(cx, y, rail_w * 0.36, fill=dd.GREY_F, stroke=dd.GREY, sw=2.5)
            d.circle(cx, y, rail_w * 0.14, fill=dd.GREY, stroke="none", sw=0)
        else:
            d.circle(cx, y, rail_w * 0.26, fill=dd.PANEL, stroke=dd.GREY, sw=2.5)
    # break marks top and bottom
    for yy in (y0, y1):
        d.path(f"M {cx - ext_w / 2 - 14} {yy + 8} L {cx - 8} {yy - 8} L {cx + 8} {yy + 8} "
               f"L {cx + ext_w / 2 + 14} {yy - 8}", stroke=dd.FAINT, sw=3)
    return holes


def _lower_joint(d, cx, top, w, h):
    """z_joint_lower seen from the front: black block with a domed top."""
    d.path(f"M {cx - w / 2} {top + 26} Q {cx - w / 2} {top} {cx} {top} "
           f"Q {cx + w / 2} {top} {cx + w / 2} {top + 26} L {cx + w / 2} {top + h} "
           f"L {cx - w / 2} {top + h} Z", fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=4)


def _stopper(d, cx, cy, r):
    d.circle(cx, cy, r, fill=RUBBER, stroke=dd.INK, sw=2.5)
    d.circle(cx, cy, r * 0.45, fill="#5A616B", stroke="none", sw=0)


# ============================================================== diagram 601 ===
def d601_rubber_stopper_shelf() -> dd.Doc:
    d = dd.Doc(1000, "A rubber stopper as a shelf under each lower Z joint")
    top = dd.step_header(d, "A stopper as a shelf")
    py = top + 18

    # ---- left: one rail, front view
    d.panel(30, py, 690, 880)
    cx, pitch = 260, 92
    y0, y1 = py + 30, py + 850
    first = py + 60
    # screws in every other hole; the hole straight under the carriage is free
    holes = _rail_window(d, cx, y0, y1, pitch, 46, 104, first, lambda i: i % 2 == 0)
    car_h = 2 * pitch + 20
    sy = first + 5 * pitch               # hole 5 is free (screws sit in the even holes)
    _stopper(d, cx, sy, 30)
    car_bot = sy - 30                    # the carriage sits on the stopper
    car_top = car_bot - car_h
    d.rect(cx - 52, car_top, 104, car_h, fill=dd.GREY_F, stroke=dd.GREY, sw=3, rx=6)
    _lower_joint(d, cx, car_top + 8, 170, car_h - 26)
    d.line(cx - 60, car_bot, cx + 60, car_bot, stroke=dd.OK, sw=5)
    _arrow(d, cx + 150, car_top - 70, cx + 150, car_bot - 20, col=dd.MUTED, sw=5, mk="arwm")
    d.text(cx + 168, car_top - 40, "pushed down,", size=dd.T_MIN, weight=600, fill=dd.MUTED)
    d.text(cx + 168, car_top - 4, "it stops here", size=dd.T_MIN, weight=600, fill=dd.MUTED)
    dd.callout(d, cx - 120, sy, 1)
    # labels
    lx = 420
    d.text(lx, car_top + car_h * 0.45, "lower Z joint", size=dd.T_LAB, weight=700)
    d.text(lx, car_top + car_h * 0.45 + 38, "on its carriage", size=dd.T_LAB, weight=700)
    d.leader(cx + 86, car_top + car_h * 0.45 - 10, lx - 12, car_top + car_h * 0.45 - 10,
             col=dd.INK)
    d.text(lx, sy + 10, "rubber stopper", size=dd.T_LAB, weight=700)
    d.text(lx, sy + 48, "in a free hole", size=dd.T_LAB, weight=700)
    d.leader(cx + 32, sy, lx - 12, sy, col=dd.INK)
    scr = [y for i, y in holes if i % 2 == 0 and y > sy][0]
    d.text(lx, scr + 64, "rail screw", size=dd.T_MIN, weight=600, fill=dd.MUTED)
    d.leader(cx + 18, scr + 6, lx - 12, scr + 54, col=dd.MUTED)

    # ---- right: four corners at one height, printed stops on top
    ox = 740
    d.panel(ox, py, 430, 880)
    d.text(ox + 215, py + 52, "All four corners", size=dd.T_LAB, anchor="middle",
           weight=700)
    xs = [ox + 52 + i * 90 for i in range(4)]
    ry0, ry1 = py + 190, py + 640
    jy = py + 380
    for x in xs:
        d.rect(x - 16, ry0 - 40, 32, ry1 - ry0 + 40, fill=dd.BLUE_F, stroke=dd.BLUE, sw=2)
        d.rect(x - 8, ry0, 16, ry1 - ry0, fill=dd.STEEL, stroke=dd.GREY, sw=2)
        d.rect(x - 14, ry0 - 8, 28, 22, fill=dd.BLACKPART, stroke=dd.INK, sw=2, rx=3)
        _lower_joint(d, x, jy, 52, 56)
        _stopper(d, x, jy + 74, 13)
    d.line(ox + 20, jy - 4, ox + 410, jy - 4, stroke=dd.OK, sw=4, dash="14 10")
    dd.callout(d, ox + 394, jy + 74, 2)
    dd.callout(d, ox + 394, ry0 - 2, 3)
    d.text(ox + 215, py + 720, "same hole, counted", size=dd.T_LAB, anchor="middle",
           weight=700, fill=dd.OK)
    d.text(ox + 215, py + 760, "from the same end,", size=dd.T_LAB, anchor="middle",
           weight=700, fill=dd.OK)
    d.text(ox + 215, py + 800, "so the same height", size=dd.T_LAB, anchor="middle",
           weight=700, fill=dd.OK)
    d.text(ox + 200, py + 100, "printed stop on top", size=dd.T_MIN, anchor="middle",
           weight=600, fill=dd.MUTED)
    return d


# ============================================================== diagram 602 ===
def d602_belt_tail_tie() -> dd.Doc:
    d = dd.Doc(980, "The spare Z belt folded back and zip-tied to itself above the clip")
    top = dd.step_header(d, "Fold the tail, tie it to itself")
    py = top + 18
    d.panel(30, py, 1140, 850)

    # the clamp in side section: corner (black part), belt, upper clip (accent), screws
    fx0, fx1 = 470, 960
    fy = py + 600                       # top face of the corner
    d.rect(fx0 - 60, fy, fx1 - fx0 + 200, 110, fill=dd.BLACKPART_F, stroke=dd.BLACKPART,
           sw=4, rx=8)
    bt = 18                             # belt thickness on the page
    cy0 = fy - bt                       # clip underside
    d.rect(fx0, cy0 - 84, fx1 - fx0, 84, fill=dd.ORANGE_F, stroke=dd.ORANGE, sw=4, rx=10)
    for x in (fx0 + 130, fx1 - 130):    # the two M5x16 heads
        d.path(f"M {x - 44} {cy0 - 84} Q {x - 44} {cy0 - 124} {x} {cy0 - 124} "
               f"Q {x + 44} {cy0 - 124} {x + 44} {cy0 - 84} Z", fill=dd.GREY_F,
               stroke=dd.GREY, sw=3)
        d.rect(x - 11, cy0 - 84, 22, 84 + bt + 70, fill=dd.GREY_F, stroke=dd.GREY,
               sw=2, dash="8 6")

    # belt: in from the right under the clip, out on the left, up, folded back down
    xb = fx0 - 70                       # the rising tail, left of the clip
    ytop = py + 140                     # top of the fold
    r1 = 46
    path = (f"M 1150 {fy - bt / 2} L {xb + r1} {fy - bt / 2} "
            f"A {r1} {r1} 0 0 1 {xb} {fy - bt / 2 - r1} L {xb} {ytop + 40} "
            f"A 40 40 0 0 1 {xb + 80} {ytop + 40} L {xb + 80} {py + 420}")
    d.path(path, stroke=BELT, sw=bt, cap="butt")
    # zip tie round both layers, just above the clip
    ty = py + 400
    d.rect(xb - 22, ty - 18, 124, 36, fill=dd.GREY_F, stroke=dd.INK, sw=3, rx=8)
    d.rect(xb + 102, ty - 14, 34, 28, fill=dd.GREY, stroke=dd.INK, sw=2.5, rx=4)
    # its cut tail, flush
    d.line(xb + 136, ty, xb + 146, ty, stroke=dd.INK, sw=3)

    dd.callout(d, xb - 70, ty, 1)
    dd.callout(d, xb + 150, ytop + 10, 2)
    dd.callout(d, xb + 186, ty, 3)
    # legend, top right
    y = dd.legend_row(d, 640, py + 70, 1, ["fold the tail up,", "tie it to itself"])
    y = dd.legend_row(d, 640, y + 24, 2, ["leave enough to", "clamp it once more"])
    dd.legend_row(d, 640, y + 24, 3, ["trim the tie flush"])
    # labels
    d.text((fx0 + fx1) / 2, cy0 - 30, "upper clip", size=dd.T_LAB, anchor="middle",
           weight=700, fill=dd.ORANGE)
    d.text(fx1 - 80, cy0 - 104, "two M5×16", size=dd.T_LAB, weight=700)
    d.text(780, fy + 160, "gantry corner", size=dd.T_LAB, anchor="middle", weight=700)
    d.text(1150, fy - 30, "to the Z idler", size=dd.T_MIN, anchor="end", weight=600,
           fill=dd.MUTED)
    d.text(xb - 30, py + 250, "belt tail", size=dd.T_MIN, anchor="end", weight=600,
           fill=dd.MUTED)
    return d


# ============================================================== diagram 603 ===
def d603_set_gantry_down() -> dd.Doc:
    d = dd.Doc(1000, "Lowering the gantry onto the lower Z joints, and the zip-tie fallback")
    top = dd.step_header(d, "Set it down on the joints")
    py = top + 18

    # ---- left: one corner coming down
    d.panel(30, py, 700, 880)
    cx = 330
    _rail_window(d, cx, py + 20, py + 860, 92, 46, 104, py - 40, lambda i: i % 2 == 0)
    # lower joint on its carriage, parked on its stopper (a free hole)
    jt = py + 380
    d.rect(cx - 52, jt - 8, 104, 206, fill=dd.GREY_F, stroke=dd.GREY, sw=3, rx=6)
    _lower_joint(d, cx, jt, 170, 170)
    d.rect(cx - 13, jt, 26, 120, fill=dd.PANEL, stroke=dd.BLACKPART, sw=3)
    _stopper(d, cx, jt + 224, 26)
    # gantry corner, lower clip and Z bearing block, held a little above
    gy = py + 310                        # underside of the block
    d.rect(cx - 250, py + 120, 350, 80, fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=4,
           rx=8)
    d.text(cx - 230, py + 172, "gantry corner", size=dd.T_MIN, weight=700)
    d.rect(cx - 85, py + 200, 170, 22, fill=dd.ORANGE_F, stroke=dd.ORANGE, sw=3, rx=4)
    d.rect(cx - 85, py + 222, 170, 88, fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=4, rx=8)
    d.rect(cx - 13, gy - 60, 26, 60, fill=dd.PANEL, stroke=dd.BLACKPART, sw=3)
    # holes in line
    d.line(cx, gy - 70, cx, jt + 140, stroke=dd.OK, sw=4, dash="12 9")
    # lower it
    _arrow(d, cx - 200, py + 240, cx - 200, py + 350, sw=8)
    dd.callout(d, cx - 200, py + 410, 1)
    # slide the carriage up or down to meet it
    ax = cx + 150
    _arrow(d, ax, jt + 100, ax, jt + 10, col=dd.MUTED, sw=5, mk="arwm")
    _arrow(d, ax, jt + 100, ax, jt + 190, col=dd.MUTED, sw=5, mk="arwm")
    d.text(ax + 26, jt + 70, "slide the", size=dd.T_MIN, weight=600, fill=dd.MUTED)
    d.text(ax + 26, jt + 106, "carriage", size=dd.T_MIN, weight=600, fill=dd.MUTED)
    d.text(ax + 26, jt + 142, "to line up", size=dd.T_MIN, weight=600, fill=dd.MUTED)
    d.text(cx + 100, gy - 30, "Z block", size=dd.T_LAB, weight=700)
    d.text(ax + 26, jt + 232, "on its stopper", size=dd.T_MIN, weight=600, fill=dd.MUTED)
    d.text(60, py + 720, "holes in line", size=dd.T_LAB, weight=700, fill=dd.OK)
    d.leader(cx - 2, jt + 120, 170, py + 690, col=dd.OK)

    # ---- right: no stoppers, zip-tie each corner up first
    ox = 750
    d.panel(ox, py, 420, 880)
    d.text(ox + 210, py + 52, "No stoppers?", size=dd.T_LAB, anchor="middle", weight=700)
    tcx, tcy = ox + 210, py + 200
    by = py + 560
    # the long zip tie: over the top extrusion, under the gantry corner
    d.rect(tcx - 62, tcy - 58, 124, by + 90 - tcy + 58, fill="none", stroke=dd.GREY, sw=9,
           rx=40)
    dd.profile2020(d, tcx, tcy, 3.6)
    d.rect(ox + 60, by, 300, 70, fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=4, rx=8)
    dd.label_bg(d, tcx, by + 47, "gantry corner", size=dd.T_MIN, weight=700,
                bg=dd.BLACKPART_F)
    dd.label_bg(d, tcx, tcy + 82, "top extrusion", size=dd.T_MIN, weight=600,
                fill=dd.BLUE)
    dd.label_bg(d, tcx, py + 400, "long zip tie", size=dd.T_MIN, weight=600,
                fill=dd.MUTED)
    dd.callout(d, tcx + 120, py + 470, 2)
    d.text(ox + 210, py + 730, "zip-tie it up", size=dd.T_LAB, anchor="middle",
           weight=700)
    d.text(ox + 210, py + 770, "before you lower", size=dd.T_LAB, anchor="middle",
           weight=700)
    return d


# ============================================================== diagram 604 ===
def d604_z_belt_span() -> dd.Doc:
    d = dd.Doc(1100, "Where the 150 mm Z belt span is measured and plucked")
    top = dd.step_header(d, "The 150 mm span")
    py = top + 18
    d.panel(30, py, 1140, 970)

    k = 3.4                                  # px per mm on the span
    ix, iy, ir = 470, py + 200, 46           # Z idler pulley centre
    # idler body (black part) on the top frame extrusion
    d.rect(ix - 130, py + 40, 330, 70, fill=dd.BLUE_F, stroke=dd.BLUE, sw=3)
    d.text(ix + 215, py + 88, "top extrusion", size=dd.T_MIN, weight=600, fill=dd.BLUE)
    d.path(f"M {ix - 80} {py + 110} L {ix - 80} {iy + 30} A 80 80 0 0 0 {ix + 80} {iy + 30} "
           f"L {ix + 80} {py + 110} Z", fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=4)
    d.circle(ix, iy, ir, fill=dd.GREY_F, stroke=dd.GREY, sw=3)
    d.circle(ix, iy, 9, fill=dd.GREY, stroke="none", sw=0)
    # the tensioner screw: head under the idler, turned from below
    hx, hy = ix + 120, py + 150
    d.rect(hx - 9, py + 110, 18, hy - py - 110, fill=dd.GREY_F, stroke=dd.GREY, sw=2.5)
    d.rect(hx - 20, hy, 40, 26, fill=dd.GREY_F, stroke=dd.GREY, sw=3, rx=4)
    d.path(f"M {hx - 46} {hy + 50} A 46 18 0 1 0 {hx + 40} {hy + 58}", stroke=dd.ORANGE,
           sw=5, marker="arwo")
    d.text(hx + 66, hy + 30, "tensioner: clockwise,", size=dd.T_MIN, weight=700)
    d.text(hx + 66, hy + 66, "looking up, is tighter", size=dd.T_MIN, weight=700)

    # belt runs: the fixed side down to the gantry's top clip, the other side to the drive
    lx, rx = ix - ir, ix + ir
    clip_y = iy + 150 * k
    d.path(f"M {lx} {clip_y} L {lx} {iy} A {ir} {ir} 0 0 1 {rx} {iy} L {rx} {py + 960}",
           stroke=BELT, sw=10, cap="butt")
    # gantry corner with the upper clip on top, belt clamped under the clip
    d.rect(lx - 250, clip_y + 30, 300, 80, fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=4,
           rx=8)
    d.rect(lx - 200, clip_y, 200, 30, fill=dd.ORANGE_F, stroke=dd.ORANGE, sw=3, rx=4)
    d.path(f"M {lx} {clip_y} L {lx} {clip_y + 30} L {lx - 200} {clip_y + 30}",
           stroke=BELT, sw=8, cap="butt")
    d.text(lx - 240, clip_y + 160, "top clip on the", size=dd.T_MIN, weight=700)
    d.text(lx - 240, clip_y + 196, "gantry corner", size=dd.T_MIN, weight=700)
    d.text(rx + 20, py + 930, "to the Z drive", size=dd.T_MIN, weight=600, fill=dd.MUTED)

    # 150 mm, axle to clip
    dx = lx - 120
    d.line(ix - 12, iy, dx - 14, iy, stroke=dd.MUTED, sw=2, dash="6 6")
    d.line(lx - 8, clip_y, dx - 14, clip_y, stroke=dd.MUTED, sw=2, dash="6 6")
    _arrow(d, dx, (iy + clip_y) / 2, dx, iy + 3, col=dd.INK, sw=3)
    _arrow(d, dx, (iy + clip_y) / 2, dx, clip_y - 3, col=dd.INK, sw=3)
    dd.label_bg(d, dx, (iy + clip_y) / 2 + 12, "150 mm", size=dd.T_LAB, weight=800,
                bg=dd.PANEL)
    dd.callout(d, dx, iy + 80, 1)

    # pluck in the middle of that span
    my = (iy + clip_y) / 2
    for i, r in enumerate((26, 44, 62)):
        d.path(f"M {lx + r} {my - r * 0.8} Q {lx + r * 1.35} {my} {lx + r} {my + r * 0.8}",
               stroke=dd.ORANGE, sw=4, op=1 - i * 0.25)
    dd.callout(d, lx + 130, my, 2)
    d.text(lx + 175, my - 10, "pluck here:", size=dd.T_LAB, weight=700)
    d.text(lx + 175, my + 30, "about 140 Hz", size=dd.T_LAB, weight=700, fill=dd.OK)
    d.text(ix - 100, iy - 40, "Z idler", size=dd.T_LAB, anchor="end", weight=700)
    return d


# ============================================================== diagram 605 ===
def _gantry_side(d, x0, x1, y, motors_down, rail_col=dd.STEEL):
    """Side view of the gantry from the left, FRONT on the left of the page."""
    d.rect(x0, y - 22, x1 - x0, 44, fill=dd.BLUE_F, stroke=dd.BLUE, sw=3)       # Y extrusion
    rs = 1 if motors_down else -1                                              # rail side
    ry = y + rs * 22 + (0 if motors_down else -12)
    d.rect(x0 + 80, ry, x1 - x0 - 160, 12, fill=rail_col, stroke=dd.GREY, sw=2)  # Y rail
    # front idler (left end) and A/B drive (right end), black parts
    d.rect(x0 - 40, y - 46, 90, 92, fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=4, rx=8)
    d.rect(x1 - 70, y - 50, 120, 100, fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=4, rx=8)
    # motor hanging from the drive
    my = y + 50 if motors_down else y - 50 - 120
    d.rect(x1 - 60, my, 100, 120, fill=dd.GREY_F, stroke=dd.GREY, sw=3, rx=6)
    d.text(x1 - 10, my + 70, "motor", size=dd.T_MIN, anchor="middle", weight=700)
    # X extrusion section mid-way, hanging from the Y carriage on the rail side,
    # its rail on the front face
    xc = (x0 + x1) / 2 - 40
    xy = y + rs * (22 + 12 + 34)
    d.rect(xc - 40, min(ry, xy) + (12 if motors_down else 0), 80,
           abs(xy - ry) - 12 + 26, fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=3, rx=4)
    dd.profile2020(d, xc, xy, 2.6)
    d.rect(xc - 26 - 12, xy - 20, 12, 40, fill=rail_col, stroke=dd.GREY, sw=2)


def _tape(d, x, y, s):
    w = len(s) * dd.T_MIN * 0.62 + 24
    d.rect(x - w / 2, y - 26, w, 44, fill=dd.AMBER_F, stroke=dd.AMBER, sw=3, rx=4)
    d.text(x, y + 6, s, size=dd.T_MIN, anchor="middle", weight=800)


def d605_turn_over_and_mark() -> dd.Doc:
    d = dd.Doc(1120, "Turning the gantry the right way up and taping Front and Back")
    top = dd.step_header(d, "Turn it over, mark the ends")
    py = top + 18
    x0, x1 = 200, 960

    # now: upside down on the bench
    d.panel(30, py, 1140, 400)
    d.text(54, py + 50, "Now: upside down", size=dd.T_LAB, weight=700, fill=dd.MUTED)
    _gantry_side(d, x0, x1, py + 290, motors_down=False)
    d.text(x0 + 5, py + 380, "front", size=dd.T_MIN, anchor="middle", weight=600,
           fill=dd.MUTED)
    d.text(x1 - 10, py + 380, "back", size=dd.T_MIN, anchor="middle", weight=600,
           fill=dd.MUTED)

    # turn over, in the gap between the panels
    ay = py + 455
    d.path(f"M 470 {ay - 30} C 540 {ay + 40} 660 {ay + 40} 730 {ay - 30}",
           stroke=dd.ORANGE, sw=7, marker="arwo")
    dd.callout(d, 400, ay - 20, 1)
    d.text(770, ay + 2, "turn it over", size=dd.T_LAB, weight=700)

    # right way up, marked
    by = py + 510
    d.panel(30, by, 1140, 480)
    d.text(54, by + 50, "Right way up", size=dd.T_LAB, weight=700, fill=dd.OK)
    gy = by + 210
    _gantry_side(d, x0, x1, gy, motors_down=True)
    d.text(x0 + 330, gy + 150, "rails underneath", size=dd.T_MIN, weight=600,
           fill=dd.MUTED)
    d.text(x0 + 70, gy + 150, "X rail", size=dd.T_MIN, weight=600, fill=dd.MUTED)
    d.leader(500, gy + 68, x0 + 150, gy + 125, col=dd.MUTED)
    d.text(x0 + 70, gy + 186, "to the front", size=dd.T_MIN, weight=600, fill=dd.MUTED)
    _tape(d, x0 + 30, gy - 90, "FRONT")
    _tape(d, x1 - 150, gy - 90, "BACK")
    dd.callout(d, x0 - 80, gy - 90, 2)
    d.text(600, by + 445, "Tape the same two marks on the frame.", size=dd.T_LAB,
           anchor="middle", weight=700)
    return d


# ================================================================= registry ===
DIAGRAMS = [
    {
        "n": 601,
        "file": "601-rubber-stopper-shelf.svg",
        "title": "A stopper as a shelf",
        "fn": d601_rubber_stopper_shelf,
        "shows": [
            "Front view of one Z rail mid-way up its vertical: rail screws in every other "
            "hole, the lower Z joint on its carriage, and a rubber stopper in the free hole "
            "straight under the carriage, which stops on it when pushed down (callout 1).",
            "Four rails side by side with the joints at one height on the same hole (2) and "
            "the printed `z_rail_stop_x4` on each rail top (3).",
        ],
        "insert": [
            ("06-z-axis-and-gantry-squaring.md", "Step 06.10", "the shelf and the matched "
             "height"),
        ],
        "verify": [
            "How the rubber stopper holds in the hole (pressed or screwed) is not in any "
            "source: it is drawn as a plug in the hole, and the step text says 'fit'.",
            "Hole pitch, carriage and joint sizes are schematic; the screwed holes follow "
            "Ch 02 (holes 2 to 18).",
        ],
    },
    {
        "n": 602,
        "file": "602-belt-tail-tie.svg",
        "title": "Fold the tail, tie it to itself",
        "fn": d602_belt_tail_tie,
        "shows": [
            "Side section of a gantry corner's top clamp: the belt from the Z idler under "
            "the upper clip and its two M5×16; the tail out the far side, up, folded back "
            "on itself, and one small zip tie round both layers just above the clip, after "
            "p.120 (callouts 1-3 = Do of Step 06.21).",
        ],
        "insert": [
            ("06-z-axis-and-gantry-squaring.md", "Step 06.21", "the fold and the tie"),
        ],
        "verify": [
            "Which side of the clip the running belt enters and the tail leaves, and the "
            "fold's exact path, are schematic; p.120 shows the tail folded over and tied to "
            "itself above the clip.",
        ],
    },
    {
        "n": 603,
        "file": "603-set-gantry-down.svg",
        "title": "Set it down on the joints",
        "fn": d603_set_gantry_down,
        "shows": [
            "Front view of one corner: the gantry corner with its lower clip and Z bearing "
            "block coming down (1) onto the domed top of the lower joint, parked on its "
            "rubber stopper, the carriage slid up or down until the M5 holes are in line.",
            "Side panel: without stoppers, a long zip tie from the gantry corner up over the "
            "top frame extrusion before lowering (2), after p.114.",
        ],
        "insert": [
            ("06-z-axis-and-gantry-squaring.md", "Step 06.13", "lowering and the fallback"),
        ],
        "verify": [
            "Block, joint and clip proportions are schematic; the gap above the joint is "
            "exaggerated to show the move.",
        ],
    },
    {
        "n": 604,
        "file": "604-z-belt-span.svg",
        "title": "The 150 mm span",
        "fn": d604_z_belt_span,
        "shows": [
            "Side view of one Z corner: the Z idler at the top, the run that is fixed to the "
            "gantry going down to the top clip, 150 mm from the idler axle to the clip (1), "
            "and the pluck point in the middle of that run, about 140 Hz (2). The other run "
            "goes on down to the Z drive.",
            "The tensioner screw under the idler, head down: clockwise, looking up at it, "
            "pulls the idler up and tightens the belt (p.117 section).",
        ],
        "insert": [
            ("06-z-axis-and-gantry-squaring.md", "Step 06b.3", "the span and the pluck point"),
        ],
        "verify": [
            "The span is drawn to scale (3.4 px/mm); the idler, its body and the corner are "
            "schematic.",
        ],
    },
    {
        "n": 605,
        "file": "605-turn-over-and-mark.svg",
        "title": "Turn it over, mark the ends",
        "fn": d605_turn_over_and_mark,
        "shows": [
            "The gantry from the left side, front on the left: upside down on the bench "
            "with the A/B motors up (as Ch 05 left it), turned over (1) to motors down, Y "
            "rails underneath and the X rail facing front, then FRONT and BACK tape on its "
            "ends (2) and the same marks on the frame.",
        ],
        "insert": [
            ("06-z-axis-and-gantry-squaring.md", "Step 06.11", "the turn-over and the marks"),
        ],
        "verify": [
            "Which axis the gantry rolls about is not drawn; the front stays on the left in "
            "both views and the tape marks settle it. Parts are blocks, not outlines.",
        ],
    },
]
