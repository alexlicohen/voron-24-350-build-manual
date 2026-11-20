"""Chapter 14 step diagrams (1401 onwards): belts, the hot Z-joint tighten, the
extruder check, the cube caliper and the dead-PSU check before Part H's wiring.

Geometry sources: Voron docs, Secondary printer tuning § Belt tension and V2 Gantry
Squaring steps 14-17 (fetched 2026-11-20); the 2.4r2 CAD index (front idler, XY joint
and Z joint positions, as used for diagrams 604 and 702); `Voron_Design_Cube_v7.stl`
(30 mm, flat faces at mid-height, 0.2 mm bottom chamfer); Ellis' extruder calibration
(tape at 120 mm from where the filament enters the extruder; fetched 2026-11-20); the
Mean Well LRS-200 datasheet (pins 1 AC/L, 2 AC/N, 3 FG, 4-6 -V, 7-9 +V; fetched
2026-11-20). Numbered callouts are the Do numbers of the step each diagram sits in.
"""
import math

import draw_diagrams as dd

T_MIN, T_LAB = dd.T_MIN, dd.T_LAB
HOT_F = "#F8DEDA"          # light red fill: hot or mains
FIL = "#2B3038"            # filament / Z belt, drawn dark


# ------------------------------------------------------------------ helpers ---
def arrow(d, x0, y0, x1, y1, col=dd.INK, sw=5, mk="arw", dash=None):
    d.path(f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}", stroke=col, sw=sw, marker=mk,
           dash=dash)


def pluck(d, x, y, side, col=dd.ORANGE):
    """Three arcs beside a vertical run at (x, y); side = +1 right, -1 left."""
    for i, r in enumerate((22, 38, 54)):
        d.path(f"M {x + side * r:.1f} {y - r * 0.8:.1f} "
               f"Q {x + side * r * 1.35:.1f} {y:.1f} {x + side * r:.1f} {y + r * 0.8:.1f}",
               stroke=col, sw=4, op=1 - i * 0.25)


def bench_tag(d, x, y, s, anchor="start", size=T_MIN):
    """An amber chip for a fact the step marks (verify on bench), as Ch 08's."""
    w = len(s) * size * 0.56 + 24
    x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
    d.rect(x0, y - size * 0.95, w, size * 1.4, fill=dd.AMBER_F, stroke=dd.AMBER, sw=2.5,
           rx=8)
    d.text(x0 + w / 2, y + size * 0.05, s, size=size, anchor="middle", weight=700,
           fill=dd.INK)


def dim_v(d, x, y0, y1, label, sub=None, side=-1, size=40):
    """Vertical dimension with arrowheads and a label beside it."""
    mid = (y0 + y1) / 2
    arrow(d, x, mid, x, y0 + 3, dd.INK, 3.5)
    arrow(d, x, mid, x, y1 - 3, dd.INK, 3.5)
    anchor = "end" if side < 0 else "start"
    tx = x + side * 18
    d.text(tx, mid + 12, label, size=size, anchor=anchor, weight=800)
    if sub:
        d.text(tx, mid + 12 + size, sub, size=T_MIN, anchor=anchor, weight=600,
               fill=dd.MUTED)


# ============================================================== diagram 1401 ===
def d1401_ab_belts() -> dd.Doc:
    """Top view of the gantry's front half, FRONT at the bottom. The plucked run is
    each belt's inner run, front idler to the XY joint's toothed idler (CAD, as 702);
    the outer run passes the joint on its way to the drive. A on the right, B on the
    left; each front idler's M3x40 has its head at the front (screw in = tighter).
    Callouts are Step 14.4's Do numbers: 1 motors, 2 push forward, 3 pluck, 4 back
    and return (Voron secondary tuning, A/B steps 1-4)."""
    d = dd.Doc(1068, "Pluck A and B over the 150 mm span and read the lowest peak")
    top = dd.step_header(d, "A and B: 110 Hz each")
    py = top + 16
    d.panel(30, py, 1140, 680)

    k = 1.6                                   # px per mm along the span
    yJ = py + 230                             # XY joint idler centres
    yF = yJ + 150 * k                         # front idler centres
    xs = {"B": 330, "A": 870}                 # inner (plucked) runs
    cols = {"B": dd.BELT_B, "A": dd.BELT_A}
    yTop = py + 60

    for name, x in xs.items():
        s = 1 if name == "A" else -1          # outward
        # gantry side extrusion, outside the belts
        ex = x + s * 70
        d.rect(ex - 20, yTop, 40, yF + 50 - yTop, fill=dd.BLUE_F, stroke=dd.BLUE, sw=3)
        # front idler block and XY joint block (schematic outlines)
        bx0 = x - 50 if s > 0 else x - 80
        d.rect(bx0, yF - 42, 130, 84, fill="none", stroke=dd.BLACKPART, sw=3, rx=10,
               dash="10 7")
        jx0 = x - 70 if s > 0 else x - 60
        d.rect(jx0, yJ - 50, 130, 96, fill="none", stroke=dd.BLACKPART, sw=3, rx=10,
               dash="10 7")
        # outer run (faint) past the joint to the drive, round the front idler
        xo = x + s * 26
        d.rect(xo - 5, yTop, 10, yF - yTop, fill=cols[name], stroke=cols[name], sw=1,
               op=0.3)
        d.circle(x + s * 13, yF, 17, fill=dd.GREY_F, stroke=dd.GREY, sw=3)
        # inner run: the one you pluck
        d.rect(x - 5, yJ, 10, yF - yJ, fill=cols[name], stroke=cols[name], sw=1)
        # joint's toothed idler, belt turns in towards the carriage
        d.circle(x - s * 14, yJ, 16, fill=dd.ORANGE_F, stroke=dd.ORANGE, sw=3)
        cx0, cx1 = sorted((x - s * 14, 600 + s * 60))
        d.rect(cx0, yJ - 21, cx1 - cx0, 10, fill=cols[name], stroke=cols[name], sw=1,
               op=0.3)
        # tensioner screw: head at the front of the idler block
        sx = x - s * 6
        d.rect(sx - 6, yF + 4, 12, 50, fill=dd.GREY_F, stroke=dd.GREY, sw=2.5)
        d.rect(sx - 15, yF + 54, 30, 24, fill=dd.GREY, stroke=dd.INK, sw=2.5, rx=4)
        # pluck marks, mid-span, on the inside
        pluck(d, x, (yJ + yF) / 2, -s)
        d.text(x + s * 120, (yJ + yF) / 2 - 20, name, size=64, anchor="middle",
               weight=800, fill=cols[name])
        d.text(x + s * 120, (yJ + yF) / 2 + 22, "belt", size=T_MIN, anchor="middle",
               weight=700, fill=cols[name])
        d.text(sx, yF + 116, f"{name} screw", size=T_LAB, anchor="middle", weight=700)

    # X extrusion between the joints, toolhead block in the middle
    d.rect(xs["B"] + 60, yJ - 64, xs["A"] - xs["B"] - 120, 30, fill=dd.BLUE_F,
           stroke=dd.BLUE, sw=3)
    d.rect(560, yJ - 78, 80, 58, fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=3, rx=8)
    d.text(470, yJ - 80, "X extrusion", size=T_MIN, anchor="middle", weight=700,
           fill=dd.BLUE)
    # 2: push it forward to 150 mm
    arrow(d, 680, yJ - 150, 680, yJ - 50, dd.ORANGE, 7, "arwo")
    dd.callout(d, 730, yJ - 112, 2)
    # 4: back a few centimetres, then return
    arrow(d, 800, yJ - 150, 800, yJ - 205, dd.ORANGE, 6, "arwo")
    arrow(d, 800, yJ - 150, 800, yJ - 92, dd.ORANGE, 6, "arwo")
    dd.callout(d, 850, yJ - 150, 4)
    # 150 mm, centre to centre, in the middle
    arrow(d, 600, (yJ + yF) / 2, 600, yJ + 3, dd.INK, 3.5)
    arrow(d, 600, (yJ + yF) / 2, 600, yF - 3, dd.INK, 3.5)
    dd.label_bg(d, 600, (yJ + yF) / 2 - 6, "150 mm", size=40, weight=800)
    dd.label_bg(d, 600, (yJ + yF) / 2 + 36, "centre to centre", size=T_MIN, weight=600,
                fill=dd.MUTED)
    for x in (xs["B"], xs["A"]):
        for y in (yJ, yF):
            d.line(x + (40 if x < 600 else -40), y, 600, y, stroke=dd.MUTED, sw=2,
                   dash="6 6")
    # 3: pluck A, then B
    dd.callout(d, xs["A"] - 50, (yJ + yF) / 2 - 80, 3)
    d.text(600, yF + 116, "in = tighter", size=T_LAB, anchor="middle", weight=700,
           fill=dd.OK)
    d.text(1150, py + 662, "FRONT", size=T_MIN, anchor="end", weight=800, fill=dd.BLUE)
    # 1: what holds the gantry
    dd.callout(d, 84, py + 651, 1, r=24)
    d.text(120, py + 662, "X and Y motors off, Z motors hold", size=T_MIN, weight=700)

    # spectrum: read the lowest peak
    sy = py + 700
    d.panel(30, sy, 1140, d.h - sy - 20)
    base = sy + 172
    x0, x1 = 90, 1110
    d.line(x0, base, x1, base, stroke=dd.MUTED, sw=3)
    hz = lambda f: x0 + (f / 400.0) * (x1 - x0)   # noqa: E731

    def peak(f, h, col, w=26):
        x = hz(f)
        d.path(f"M {x - w * 2:.1f} {base} Q {x - w * 0.6:.1f} {base} {x:.1f} {base - h:.1f} "
               f"Q {x + w * 0.6:.1f} {base} {x + w * 2:.1f} {base}", fill="none",
               stroke=col, sw=5)
    peak(110, 92, dd.OK)
    peak(220, 128, dd.FAINT)
    peak(330, 56, dd.FAINT)
    d.text(hz(110), base + 40, "110 Hz", size=T_LAB, anchor="middle", weight=800,
           fill=dd.OK)
    d.text(60, sy + 50, "read the lowest peak", size=T_LAB, weight=800,
           fill=dd.OK)
    d.text(hz(220) + 70, sy + 72, "louder or higher:", size=T_MIN, weight=600,
           fill=dd.MUTED)
    d.text(hz(220) + 70, sy + 106, "not this one", size=T_MIN, weight=600,
           fill=dd.MUTED)
    dd.callout(d, hz(110) - 110, base - 46, 3)
    return d


# ============================================================== diagram 1402 ===
def d1402_z_joints_hot() -> dd.Doc:
    """Left: the machine from above at the gantry's height, FRONT (door) at the
    bottom; the four lower Z joints at the corners, reached from the open door, the
    rear pair along the sides at an angle. Right: one Z joint from the side, its
    M5x40 run up from below (CAD: head at the joint's bottom face), a ball-end 4 mm
    key in it at an angle."""
    d = dd.Doc(1060, "Tighten the four Z joint screws hot, rear pair first, from the door")
    top = dd.step_header(d, "Lock the Z joints hot")
    py = top + 16

    # ---- left: from above
    d.panel(30, py, 640, 930)
    d.text(54, py + 50, "From above", size=T_LAB, weight=700, fill=dd.MUTED)
    fx0, fx1, fy0, fy1 = 90, 610, py + 90, py + 650
    d.rect(fx0, fy0, fx1 - fx0, fy1 - fy0, fill="none", stroke=dd.BLUE, sw=10)
    # bed
    d.rect(fx0 + 95, fy0 + 70, fx1 - fx0 - 190, fy1 - fy0 - 140, fill=HOT_F,
           stroke=dd.RED, sw=4)
    d.text((fx0 + fx1) / 2, (fy0 + fy1) / 2 - 10, "bed", size=T_LAB, anchor="middle",
           weight=800, fill=dd.RED)
    d.text((fx0 + fx1) / 2, (fy0 + fy1) / 2 + 30, "110 °C", size=T_LAB, anchor="middle",
           weight=800, fill=dd.RED)
    # Z joints at the corners
    corners = [(fx0 + 42, fy0 + 42), (fx1 - 42, fy0 + 42),
               (fx0 + 42, fy1 - 42), (fx1 - 42, fy1 - 42)]
    for x, y in corners:
        d.rect(x - 24, y - 24, 48, 48, fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=4,
               rx=6)
        d.circle(x, y, 9, fill=dd.GREY, stroke="none", sw=0)
    # door: the front edge, open
    d.line(fx0 + 60, fy1, fx1 - 60, fy1, stroke=dd.BG, sw=14)
    d.line(fx0 + 60, fy1, fx0 + 60, fy1 + 110, stroke=dd.BLACKPART, sw=6)
    d.text((fx0 + fx1) / 2, fy1 + 60, "door open", size=T_LAB, anchor="middle",
           weight=700)
    # reach: front pair straight in, rear pair along the sides
    for x, y in corners[2:]:
        s = -1 if x < 350 else 1
        arrow(d, x - s * 70, fy1 + 40, x - s * 30, y + 34, dd.ORANGE, 6, "arwo")
    for x, y in corners[:2]:
        s = -1 if x < 350 else 1
        d.path(f"M {x - s * 120:.1f} {fy1 + 40:.1f} L {x - s * 2:.1f} {fy1 - 120:.1f} "
               f"L {x - s * 2:.1f} {y + 40:.1f}", stroke=dd.ORANGE, sw=7, marker="arwo")
    d.text((fx0 + fx1) / 2, fy0 + 32, "rear pair first", size=T_LAB, anchor="middle",
           weight=800)
    dd.callout(d, (fx0 + fx1) / 2, fy1 + 130, 3)
    d.text(54, py + 840, "Arm off the hot bed.", size=T_LAB, weight=800, fill=dd.RED)
    d.text(54, py + 885, "Out of reach? Take that side panel off.", size=T_MIN,
           weight=600, fill=dd.MUTED)

    # ---- right: one joint from the side
    ox = 690
    d.panel(ox, py, 480, 930)
    d.text(ox + 24, py + 50, "One joint", size=T_LAB, weight=700, fill=dd.MUTED)
    cx = ox + 210
    # gantry corner, upper joint under it, lower joint on its carriage
    d.rect(cx - 150, py + 110, 300, 70, fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=4,
           rx=8)
    d.text(cx, py + 156, "gantry corner", size=T_MIN, anchor="middle", weight=700)
    d.rect(cx - 70, py + 180, 140, 110, fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=4,
           rx=8)
    d.rect(cx - 70, py + 296, 140, 150, fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=4,
           rx=8)
    d.rect(cx + 74, py + 250, 46, 240, fill=dd.GREY_F, stroke=dd.GREY, sw=3, rx=4)
    d.text(cx + 140, py + 470, "Z rail", size=T_MIN, weight=600, fill=dd.MUTED)
    # M5x40 up from below: shank hidden, head under the lower joint
    d.rect(cx - 9, py + 196, 18, 250, fill="none", stroke=dd.GREY, sw=2.5, dash="8 6")
    d.rect(cx - 20, py + 446, 40, 34, fill=dd.GREY_F, stroke=dd.GREY, sw=3, rx=4)
    d.text(cx + 40, py + 640, "M5×40 head,", size=T_LAB, weight=700)
    d.text(cx + 40, py + 678, "from below", size=T_LAB, weight=700)
    d.leader(cx + 22, py + 470, cx + 60, py + 610, col=dd.INK)
    # ball-end key at an angle from below
    a = math.radians(24)
    kx0, ky0 = cx, py + 482
    L = 300
    kx1, ky1 = kx0 - L * math.sin(a), ky0 + L * math.cos(a)
    d.line(kx0, ky0, kx1, ky1, stroke=dd.INK, sw=12)
    d.circle(kx0, ky0 + 4, 9, fill=dd.INK, stroke="none", sw=0)
    d.line(kx1, ky1, kx1 + 110, ky1 + 30, stroke=dd.INK, sw=12)
    d.path(f"M {kx1 + 30:.1f} {ky1 - 60:.1f} Q {kx1 + 120:.1f} {ky1 - 70:.1f} "
           f"{kx1 + 150:.1f} {ky1 - 10:.1f}", stroke=dd.ORANGE, sw=5, marker="arwo")
    d.text(ox + 24, py + 860, "ball-end 4 mm key", size=T_LAB, weight=700)
    d.text(ox + 24, py + 900, "gantry at your noted height", size=T_MIN, weight=600,
           fill=dd.MUTED)
    dd.callout(d, cx - 130, py + 400, 3)
    return d


# ============================================================== diagram 1403 ===
def d1403_extruder_tape() -> dd.Doc:
    """Ellis' method as Step 14.7 words it: the PTFE tube out of the collet, tape on
    the bare filament 120 mm above the collet, extrude 100 mm, measure what is left
    (R). Drawn to scale along the filament (3.3 px per mm); the toolhead is a block.
    The tube's slack to slide ~130 mm up is the step's bench check."""
    d = dd.Doc(1060, "Tape at 120 mm, extrude 100 mm, measure what is left")
    top = dd.step_header(d, "Tape at 120 mm, read R")
    py = top + 16
    k = 3.3
    ent = py + 600                             # extruder entrance

    def toolhead(c, hot):
        d.rect(c - 120, ent, 240, 220, fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=4,
               rx=14)
        d.rect(c - 34, ent - 14, 68, 18, fill=dd.GREY_F, stroke=dd.GREY, sw=3, rx=4)
        d.poly([(c - 26, ent + 220), (c + 26, ent + 220), (c, ent + 262)],
               fill=dd.GREY_F, stroke=dd.GREY, sw=3)
        if hot:
            d.text(c + 46, ent + 262, "260 °C", size=T_LAB, weight=800, fill=dd.RED)
        d.text(c, ent + 120, "toolhead", size=T_MIN, anchor="middle", weight=700)

    def ruler(x, mm):
        d.rect(x, ent - mm * k, 34, mm * k, fill=dd.STEEL, stroke=dd.GREY, sw=2)
        for i in range(0, mm + 1, 10):
            y = ent - i * k
            d.line(x, y, x + (20 if i % 50 == 0 else 12), y, stroke=dd.INK, sw=2)

    def tape(c, y):
        d.rect(c - 46, y - 16, 92, 32, fill=dd.AMBER_F, stroke=dd.AMBER, sw=3, rx=4)

    # ---- before
    d.panel(30, py, 560, 950)
    d.text(54, py + 50, "Before", size=T_LAB, weight=700, fill=dd.MUTED)
    c = 230
    toolhead(c, True)
    dd.callout(d, c + 200, ent + 252, 1)
    d.line(c, ent - 2, c, py + 120, stroke=FIL, sw=9)
    d.rect(c - 14, py + 60, 28, 70, fill=dd.PANEL, stroke=dd.GREY, sw=3, rx=6)
    d.text(c + 30, py + 84, "tube out, slid up", size=T_MIN, weight=600, fill=dd.MUTED)
    d.text(c + 30, py + 116, "about 130 mm:", size=T_MIN, weight=600, fill=dd.MUTED)
    bench_tag(d, c + 26, py + 152, "check on the bench")
    ruler(c + 60, 130)
    tape(c, ent - 120 * k)
    dd.callout(d, c - 100, ent - 120 * k, 2)
    dim_v(d, c + 150, ent - 120 * k, ent, "120", "mm", side=1)
    d.text(c - 40, ent - 50, "collet:", size=T_MIN, anchor="end", weight=700)
    d.text(c - 40, ent - 16, "ring down", size=T_MIN, anchor="end", weight=700)

    # ---- after
    d.panel(610, py, 560, 950)
    d.text(634, py + 50, "After 100 mm", size=T_LAB, weight=700, fill=dd.MUTED)
    c = 810
    toolhead(c, False)
    d.line(c, ent - 2, c, py + 250, stroke=FIL, sw=9)
    ruler(c + 60, 100)
    tape(c, ent - 20 * k)
    d.line(c + 46, ent - 20 * k, c + 140, ent - 20 * k, stroke=dd.MUTED, sw=2,
           dash="6 6")
    d.line(c + 46, ent, c + 140, ent, stroke=dd.MUTED, sw=2, dash="6 6")
    d.line(c + 120, ent - 20 * k, c + 120, ent, stroke=dd.INK, sw=4)
    d.text(c + 160, ent - 20 * k + 12, "R", size=56, weight=800)
    d.text(c + 160, ent + 40, "about 20 mm", size=T_MIN, weight=700)
    arrow(d, c - 90, ent - 110 * k, c - 90, ent - 30 * k, dd.MUTED, 5, "arwm")
    d.text(c - 110, ent - 80 * k, "down", size=T_MIN, anchor="end", weight=600,
           fill=dd.MUTED)
    d.text(c - 110, ent - 80 * k + 36, "100 mm", size=T_MIN, anchor="end", weight=600,
           fill=dd.MUTED)
    d.text(890, py + 150, "pushed through", size=T_LAB, anchor="middle", weight=800,
           fill=dd.OK)
    d.text(890, py + 200, "= 120 − R", size=44, anchor="middle", weight=800,
           fill=dd.OK)
    return d


# ============================================================== diagram 1404 ===
def d1404_cube_caliper() -> dd.Doc:
    """The 30 mm cube from the front, its first-layer bulge exaggerated: the caliper
    jaws close on the faces at mid-height for X and Y; Z is the total height; the
    first layer is measured only for its own row of the table."""
    d = dd.Doc(980, "Caliper the cube at mid-height, not across the first layer")
    top = dd.step_header(d, "Measure at mid-height")
    py = top + 16
    d.panel(30, py, 1140, 860)

    x0, x1 = 360, 840                          # 30 mm = 480 px
    yt, yb = py + 260, py + 740
    foot = 18
    d.path(f"M {x0} {yt} L {x1} {yt} L {x1} {yb - 26} Q {x1 + 4} {yb - 8} {x1 + foot} {yb} "
           f"L {x0 - foot} {yb} Q {x0 - 4} {yb - 8} {x0} {yb - 26} Z",
           fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=4)
    d.text((x0 + x1) / 2, yt + 90, "30 mm cube", size=T_LAB, anchor="middle", weight=700)
    ym = (yt + yb) / 2

    # caliper: beam above, two jaws down to mid-height
    by = py + 150
    d.rect(200, by - 26, 800, 40, fill=dd.GREY_F, stroke=dd.GREY, sw=3, rx=4)
    for xj, s in ((x0, -1), (x1, 1)):
        d.poly([(xj + s * 70, by + 14), (xj + s * 34, by + 14), (xj + s * 34, ym - 30),
                (xj, ym - 14), (xj, ym + 14), (xj + s * 70, ym + 14)],
               fill=dd.GREY_F, stroke=dd.GREY, sw=3)
    d.line(x0 + 4, ym, x1 - 4, ym, stroke=dd.OK, sw=4, dash="10 8")
    d.text((x0 + x1) / 2, ym - 18, "X, then Y", size=T_LAB, anchor="middle", weight=800,
           fill=dd.OK)
    d.text(80, by - 50, "caliper", size=T_MIN, weight=700, fill=dd.MUTED)
    d.text(x0 - 86, ym + 10, "mid-height", size=T_LAB, anchor="end", weight=800,
           fill=dd.OK)

    # first layer: wider, its own row only
    d.line(x0 - foot, yb + 30, x1 + foot, yb + 30, stroke=dd.AMBER, sw=4)
    for x in (x0 - foot, x1 + foot):
        d.line(x, yb + 18, x, yb + 42, stroke=dd.AMBER, sw=4)
    d.text((x0 + x1) / 2, yb + 80, "first layer is wider: its own row only", size=T_LAB,
           anchor="middle", weight=700, fill=dd.AMBER)
    # Z: total height
    dim_v(d, x1 + 110, yt, yb, "Z", "total height", side=1, size=48)
    d.line(x1 + 6, yt, x1 + 120, yt, stroke=dd.MUTED, sw=2, dash="6 6")
    d.line(x1 + foot + 6, yb, x1 + 120, yb, stroke=dd.MUTED, sw=2, dash="6 6")
    return d


# ============================================================== diagram 1405 ===
def d1405_psu_dead() -> dd.Doc:
    """The precondition from Step 14.30's Do 1-2, then the LRS-200's nine-screw
    terminal strip as the datasheet numbers it (AC/L, AC/N, FG, three -V, three +V),
    the AC end in red, and the meter on -V and +V."""
    d = dd.Doc(1060, "Prove the PSU dead: only after the Pi is down and the cord is out")
    top = dd.step_header(d, "Prove it dead: 0 V")
    py = top + 16

    # ---- precondition
    d.panel(30, py, 1140, 300)
    d.text(54, py + 54, "Only after:", size=T_LAB, weight=800)
    y = dd.legend_row(d, 54, py + 116, 1, ["Pi shut down, its light stopped"])
    y = dd.legend_row(d, 54, y + 30, 2, ["rocker off, cord out of the wall,",
                                         "then the inlet, then the room"])
    d.text(1146, py + 54, "one adult only", size=T_LAB, anchor="end", weight=800,
           fill=dd.RED)
    # unplugged cord, drawn red (mains)
    px, pyy = 930, py + 172
    d.path(f"M {px - 110} {pyy + 70} C {px - 60} {pyy + 70} {px - 60} {pyy} {px} {pyy}",
           stroke=dd.RED, sw=8)
    d.rect(px, pyy - 26, 70, 52, fill=HOT_F, stroke=dd.RED, sw=4, rx=8)
    for dy in (-12, 12):
        d.line(px + 70, pyy + dy, px + 100, pyy + dy, stroke=dd.RED, sw=6)
    d.rect(px + 160, pyy - 50, 50, 100, fill=dd.GREY_F, stroke=dd.GREY, sw=3, rx=6)
    for dy in (-12, 12):
        d.line(px + 170, pyy + dy, px + 186, pyy + dy, stroke=dd.INK, sw=5)
    arrow(d, px + 150, pyy + 74, px + 40, pyy + 74, dd.RED, 5, "arwr")
    d.text(px + 95, pyy + 112, "out", size=T_LAB, anchor="middle", weight=800, fill=dd.RED)

    # ---- the measurement
    my = py + 320
    d.panel(30, my, 1140, d.h - my - 20)
    d.text(54, my + 54, "On its side, bottom panel open:", size=T_LAB, weight=700)
    dd.callout(d, 620, my + 43, 3)
    labels = ["L", "N", "FG", "−V", "−V", "−V", "+V", "+V", "+V"]
    tx0, tw, ty = 110, 96, my + 150
    for i, lab in enumerate(labels):
        x = tx0 + i * tw
        mains = i < 3
        d.rect(x, ty, tw, 150, fill=HOT_F if mains else "#3A3F46",
               stroke=dd.RED if mains else dd.INK, sw=3)
        d.circle(x + tw / 2, ty + 98, 24, fill=dd.STEEL,
                 stroke=dd.RED if mains else dd.GREY, sw=3)
        d.line(x + tw / 2 - 14, ty + 98, x + tw / 2 + 14, ty + 98, stroke=dd.INK, sw=4)
        d.text(x + tw / 2, ty + 46, lab, size=T_LAB, anchor="middle", weight=800,
               fill=dd.RED if mains else "#FFFFFF")
    d.text(tx0 + 1.5 * tw, ty - 22, "mains: never probe", size=T_MIN, anchor="middle",
           weight=800, fill=dd.RED)
    # LED beside the +V end, dark
    lx = tx0 + 9 * tw + 60
    d.circle(lx, ty + 40, 14, fill="#3A3F46", stroke=dd.INK, sw=2)
    d.text(lx, ty - 10, "LED", size=T_MIN, anchor="middle", weight=700)
    d.text(lx, ty + 90, "dark", size=T_MIN, anchor="middle", weight=700)

    # meter and probes
    mx, mw, mty = 360, 340, my + 362
    d.rect(mx, mty, mw, 230, fill=dd.AMBER_F, stroke=dd.AMBER, sw=4, rx=18)
    d.rect(mx + 40, mty + 34, mw - 80, 90, fill=dd.PANEL, stroke=dd.INK, sw=3, rx=6)
    d.text(mx + mw / 2, mty + 98, "0 V", size=56, anchor="middle", weight=800, fill=dd.OK)
    d.text(mx + mw / 2, mty + 180, "DC volts", size=T_MIN, anchor="middle", weight=700)
    nx, px_ = tx0 + 4 * tw + tw / 2, tx0 + 7 * tw + tw / 2
    d.path(f"M {mx + 90} {mty} C {mx + 90} {mty - 60} {nx} {mty - 60} {nx} {ty + 124}",
           stroke=dd.INK, sw=7)
    d.path(f"M {mx + mw - 90} {mty} C {mx + mw - 90} {mty - 60} {px_} {mty - 60} "
           f"{px_} {ty + 124}", stroke=dd.RED, sw=7)
    d.text(mx + mw + 40, mty + 90, "holds 0 V", size=T_LAB, weight=800, fill=dd.OK)
    d.text(mx + mw + 40, mty + 130, "for 10 s", size=T_LAB, weight=800, fill=dd.OK)
    return d


# ============================================================== diagram 1406 ===
def d1406_z_belt_span() -> dd.Doc:
    """One Z corner from the side, looking along the idler axle. p.117's section: the
    fixed mount hooks over the top extrusion, the sliding body (`[a]_z_tensioner`,
    accent) carries the pulley, and the M3 tensioner's head points DOWN inside the
    sliding body just above the pulley, threading up into the fixed mount, so
    clockwise looking up raises the idler. Voron secondary tuning: move the gantry
    up until the fixed side (idler to the gantry's top clip) is 150 mm; pluck that
    run. Callouts are Step 14.5's Do numbers."""
    d = dd.Doc(1040, "Z belts: jog up to a 150 mm fixed run, pluck it, 140 Hz")
    top = dd.step_header(d, "Z belts: 140 Hz each")
    py = top + 16
    d.panel(30, py, 1140, d.h - py - 20)

    k = 2.8                                   # px per mm on the span
    ix, ir = 600, 46
    iy = py + 260                             # Z idler pulley centre
    # top extrusion and the fixed mount hooked under it (black part)
    d.rect(380, py + 30, 440, 70, fill=dd.BLUE_F, stroke=dd.BLUE, sw=3)
    d.text(836, py + 76, "top extrusion", size=T_MIN, weight=600, fill=dd.BLUE)
    d.rect(490, py + 100, 220, 42, fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=4, rx=6)
    # sliding body (accent) round the pulley
    d.path(f"M {ix - 82} {py + 142} L {ix - 82} {iy + 20} A 82 82 0 0 0 {ix + 82} {iy + 20} "
           f"L {ix + 82} {py + 142} Z", fill=dd.ORANGE_F, stroke=dd.ORANGE, sw=4)
    d.circle(ix, iy, ir, fill=dd.GREY_F, stroke=dd.GREY, sw=3)
    d.circle(ix, iy, 9, fill=dd.GREY, stroke="none", sw=0)
    d.text(ix - 100, py + 200, "Z idler", size=T_LAB, anchor="end", weight=700)
    # tensioner screw: shank up into the fixed mount, head down in the sliding body
    sx = ix - 22
    d.rect(sx - 7, py + 104, 14, 46, fill=dd.GREY_F, stroke=dd.GREY, sw=2.5)
    d.rect(sx - 19, py + 150, 38, 22, fill=dd.GREY, stroke=dd.INK, sw=2.5, rx=4)
    d.path(f"M {sx - 42} {py + 178} A 42 8 0 1 0 {sx + 38} {py + 182}", stroke=dd.ORANGE,
           sw=5, marker="arwo")
    d.leader(sx + 22, py + 161, 720, py + 161, col=dd.INK)
    d.text(732, py + 160, "tensioner head, down", size=T_MIN, weight=700)
    d.text(732, py + 194, "in the blue sliding body:", size=T_MIN, weight=700)
    d.text(732, py + 236, "clockwise, looking up,", size=T_MIN, weight=700, fill=dd.OK)
    d.text(732, py + 270, "is tighter", size=T_MIN, weight=700, fill=dd.OK)

    # belt: the fixed run down to the gantry's top clip, the other side to the drive
    lx, rx = ix - ir, ix + ir
    clip_y = iy + 150 * k
    d.path(f"M {lx} {clip_y} L {lx} {iy} A {ir} {ir} 0 0 1 {rx} {iy} L {rx} {d.h - 22}",
           stroke=FIL, sw=10, cap="butt")
    d.text(rx + 20, py + 560, "to the Z drive:", size=T_MIN, weight=600, fill=dd.MUTED)
    d.text(rx + 20, py + 594, "not this run", size=T_MIN, weight=600, fill=dd.MUTED)
    # gantry corner with the top clip, belt clamped under the clip
    d.rect(lx - 300, clip_y + 30, 300, 80, fill=dd.BLACKPART_F, stroke=dd.BLACKPART, sw=4,
           rx=8)
    d.rect(lx - 200, clip_y, 200, 30, fill=dd.ORANGE_F, stroke=dd.ORANGE, sw=3, rx=4)
    d.path(f"M {lx} {clip_y} L {lx} {clip_y + 30} L {lx - 200} {clip_y + 30}",
           stroke=FIL, sw=8, cap="butt")
    d.text(lx - 280, clip_y + 78, "gantry corner", size=T_MIN, weight=700)
    d.text(lx - 190, clip_y - 16, "top clip", size=T_MIN, weight=700)

    # 1: jog Z up until the clip is 150 mm below the idler centre
    dx = 150
    d.line(ix - 12, iy, dx - 14, iy, stroke=dd.MUTED, sw=2, dash="6 6")
    d.line(lx - 210, clip_y, dx - 14, clip_y, stroke=dd.MUTED, sw=2, dash="6 6")
    arrow(d, dx, (iy + clip_y) / 2, dx, iy + 3, dd.INK, 3.5)
    arrow(d, dx, (iy + clip_y) / 2, dx, clip_y - 3, dd.INK, 3.5)
    dd.label_bg(d, dx, (iy + clip_y) / 2 + 12, "150 mm", size=40, weight=800)
    arrow(d, lx - 150, clip_y + 210, lx - 150, clip_y + 124, dd.ORANGE, 7, "arwo")
    dd.callout(d, lx - 210, clip_y + 168, 1)
    d.text(lx - 110, clip_y + 182, "jog Z up", size=T_LAB, weight=700)

    # 2: pluck the fixed run, on its outer side
    my = (iy + clip_y) / 2
    pluck(d, lx, my, -1)
    dd.callout(d, lx - 110, my - 70, 2)
    d.text(lx - 80, my + 92, "pluck this run:", size=T_LAB, anchor="end", weight=700)
    d.text(lx - 80, my + 132, "about 140 Hz", size=T_LAB, anchor="end", weight=800,
           fill=dd.OK)

    # 3: all four, then down and back up
    dd.legend_row(d, 700, py + 760, 3, ["all four corners, then", "Z down and back up,",
                                        "and read them again"], size=T_MIN)
    return d


# ================================================================= registry ===
DIAGRAMS = [
    {
        "n": 1401,
        "file": "1401-ab-belts-110hz.svg",
        "title": "A and B: 110 Hz each",
        "fn": d1401_ab_belts,
        "shows": [
            "Top view of the gantry's front half, FRONT at the bottom: X and Y motors off "
            "while the Z motors hold (1); the X extrusion pushed forward (2) until each XY "
            "joint's toothed idler is 150 mm, centre to centre, from its front idler; the A "
            "belt's inner run on the right and the B belt's on the left, the runs to pluck "
            "(3); the X extrusion moved back a few centimetres and returned before both "
            "are plucked again (4); the two front tensioner screws, heads at the front, "
            "in = tighter.",
            "A spectrum strip: read the lowest peak, about 110 Hz, not a louder or higher "
            "one (3).",
        ],
        "insert": [
            ("14-calibration.md", "Step 14.4", "first, before the app screenshot"),
        ],
        "verify": [
            "Which run is plucked and the screw head at the front follow diagram 702 (2.4r2 "
            "CAD, 250 build); block outlines and the spacing across X are schematic.",
            "The spectrum is illustrative: peak heights and the harmonics are not a "
            "measurement.",
        ],
    },
    {
        "n": 1402,
        "file": "1402-z-joints-hot.svg",
        "title": "Lock the Z joints hot",
        "fn": d1402_z_joints_hot,
        "shows": [
            "From above, door open at the front: the four lower Z joints at the corners, "
            "the front pair reached straight in and the rear pair along the sides, rear pair "
            "first (3); the bed at 110 °C in red, arm off it; a side panel off if a rear "
            "joint is out of reach.",
            "One joint from the side: the M5×40 runs up from below, its head under the "
            "lower joint, turned with a ball-end 4 mm key at an angle, the gantry at the "
            "height noted at 14.3.",
        ],
        "insert": [
            ("14-calibration.md", "Step 14.6", "first, before any other image"),
        ],
        "verify": [
            "Joint, bed and frame proportions are schematic, and so is the reach path "
            "beside the bed; whether an arm reaches the rear pair through the door on this "
            "350 is the step's own fallback (take that side panel off).",
            "Screw head at the bottom of the lower joint: 2.4r2 CAD (head z 11-16, tip "
            "z 56) and Step 06b.13 ('run one M5×40 up into each from below').",
        ],
    },
    {
        "n": 1403,
        "file": "1403-extruder-tape-r.svg",
        "title": "Tape at 120 mm, read R",
        "fn": d1403_extruder_tape,
        "shows": [
            "Before: the hotend at 260 °C (1); the PTFE tube out of the collet, its ring "
            "pressed down, and slid about 130 mm up (check on the bench); tape on the bare "
            "filament 120 mm above the collet (2), a rule beside it.",
            "After 100 mm: the tape has moved down to R above the collet, about 20 mm; "
            "pushed through = 120 − R.",
        ],
        "insert": [
            ("14-calibration.md", "Step 14.7", "replaces the no-image placeholder"),
        ],
        "verify": [
            "Tube out of the collet so the tape sits on bare filament: Ellis marks where "
            "the filament enters the extruder, and the reverse-bowden covers it up to the "
            "collet (Ch 08: collet and clip, SB p.21). The ~130 mm of tube slack is the "
            "step's bench check.",
            "Filament, tape and R are to scale (3.3 px/mm); the toolhead is a block.",
        ],
    },
    {
        "n": 1404,
        "file": "1404-cube-mid-height.svg",
        "title": "Measure at mid-height",
        "fn": d1404_cube_caliper,
        "shows": [
            "The 30 mm cube from the front with its first layer bulging (exaggerated): the "
            "caliper jaws on the faces at mid-height for X, then Y; Z as the total height; "
            "the wider first layer measured only for its own table row.",
        ],
        "insert": [
            ("14-calibration.md", "Step 14.11", "replaces the no-image placeholder"),
        ],
        "verify": [
            "Voron_Design_Cube_v7.stl is 30 × 30 × 30 mm with flat faces at mid-height "
            "(0.2 mm chamfer on the bottom edge); the bulge is exaggerated.",
        ],
    },
    {
        "n": 1405,
        "file": "1405-psu-prove-dead.svg",
        "title": "Prove it dead: 0 V",
        "fn": d1405_psu_dead,
        "shows": [
            "The step's precondition first: the Pi shut down (1); rocker off and the cord "
            "out of the wall, the inlet and the room (2); one adult only.",
            "On its side with the bottom panel open (3): the LRS-200's nine terminals, "
            "L, N and FG in red (mains, never probed), three −V and three +V; black probe "
            "on −V, red on +V; the LED dark; the meter on DC volts holding 0 V for 10 s.",
        ],
        "insert": [
            ("14-calibration.md", "Step 14.30", "replaces the no-image placeholder"),
        ],
        "verify": [
            "Terminal order from the Mean Well LRS-200 datasheet (pin 1 AC/L, 2 AC/N, 3 FG, "
            "4-6 −V, 7-9 +V); the LED's place beside the +V end follows Step 11.67. Which "
            "way up the strip appears with the machine on its side is not drawn.",
        ],
    },
    {
        "n": 1406,
        "file": "1406-z-belt-span-140hz.svg",
        "title": "Z belts: 140 Hz each",
        "fn": d1406_z_belt_span,
        "shows": [
            "One Z corner from the side: the gantry jogged up (1) until its top clip is 150 mm "
            "below the Z idler pulley centre; the fixed run between them plucked on its "
            "outer side, about 140 Hz (2); the other run, down to the Z drive, not plucked.",
            "The tensioner from p.117: the M3 head points down inside the blue sliding body "
            "above the pulley and threads up into the fixed mount; clockwise, looking up, is "
            "tighter. All four corners, then Z down and back up and read again (3).",
        ],
        "insert": [
            ("14-calibration.md", "Step 14.5", "first, in place of Ch 06's 604"),
        ],
        "verify": [
            "Screw head down in the sliding body above the pulley: p.117 section view; "
            "the hex key reaches it from below. Proportions are schematic; the span is to "
            "scale (2.8 px/mm).",
            "Fixed run = idler to the gantry's top clip: Voron secondary tuning, Z belts "
            "step 1.",
        ],
    },
]
