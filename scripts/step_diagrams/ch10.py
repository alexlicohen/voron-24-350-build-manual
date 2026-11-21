"""Chapter 10 (wiring) step-column diagrams, 1001 onwards.

Geometry sources: the chapter's own tables (10.18, 10.19, 10.74, 10.77), LDO's Rev D wiring guide
and Leviathan V1.3 photo `rpi4_installed_V1.3.jpg` (the 3/4 HAT adapter over GPIO pins 1-24),
the Leviathan V1.3 schematic (J9 PWR/UART, 6 pins), pinout.xyz (Pi GPIO numbering), the Mean Well
LRS-200 datasheet (terminals 1 AC/L, 2 AC/N, 3 FG, 4-6 -V, 7-9 +V), LDOVoron2 `STLs/COB Light
Strip` (README, `cob_mount_install.png`, both STLs probed), all fetched 2026-11-20. Proportions
are schematic; order, sides, counts and labels follow the sources.
"""
import math

import draw_diagrams as dd
from draw_diagrams import (AMBER, AMBER_F, BLACKPART, BLACKPART_F, BLUE, BROWN, GREEN, GREY,
                           GREY_F, INK, MUTED, OK, OK_F, PANEL, RED, STEEL, Doc, T_LAB, T_MIN,
                           callout, label_bg, legend_row, step_header)

WIRE_N = "#1F5FBF"       # blue neutral
YELLOW = "#E3C21B"       # the yellow of green/yellow PE
RED_F = "#FBE3E0"
PCB = "#262B31"
PCB_EDGE = "#11151A"
PI_GREEN = "#2F7D4A"
PI_GREEN_F = "#CFE6D6"
PAD = "#C9CED6"
GOLD = "#C9A227"


# ------------------------------------------------------------------ helpers ---
def unplugged(d: Doc, x, y, w, text="Unplugged: cord out of the room"):
    """The step's precondition, drawn: a mains plug crossed out in red, and the words."""
    h = 70
    d.rect(x, y, w, h, fill=RED_F, stroke=RED, sw=3, rx=10)
    px, py = x + 58, y + h / 2
    d.rect(px - 26, py - 18, 40, 36, fill=PANEL, stroke=INK, sw=3, rx=6)      # plug body
    d.line(px + 14, py - 9, px + 34, py - 9, stroke=INK, sw=5, cap="butt")     # prongs
    d.line(px + 14, py + 9, px + 34, py + 9, stroke=INK, sw=5, cap="butt")
    d.path(f"M {px - 26} {py} C {px - 46} {py} {px - 40} {py + 26} {px - 50} {py + 30}",
           stroke=INK, sw=4)                                                   # cord
    r = 26
    d.line(px - r + 4, py - r, px + r + 4, py + r, stroke=RED, sw=6)
    d.line(px - r + 4, py + r, px + r + 4, py - r, stroke=RED, sw=6)
    d.text(x + 112, py + 12, text, size=34, weight=800, fill=RED)


def probe(d: Doc, tx, ty, ang_deg, col, s=1.0):
    """A meter probe whose tip touches (tx, ty); the handle lies along ang_deg from the tip."""
    a = math.radians(ang_deg)
    ux, uy = math.cos(a), math.sin(a)
    vx, vy = -uy, ux

    def P(u, v):
        return tx + (u * ux + v * vx) * s, ty + (u * uy + v * vy) * s
    d.line(*P(0, 0), *P(34, 0), stroke=STEEL, sw=5 * s)                        # needle
    d.poly([P(34, -7), P(40, -14), P(46, -14), P(46, 14), P(40, 14), P(34, 7)], fill=col,
           stroke=col, sw=1)                                                    # finger guard
    d.poly([P(46, -10), P(150, -10), P(150, 10), P(46, 10)], fill=col, stroke=col, sw=1)
    e = P(150, 0)
    f = P(200, 0)
    d.line(*e, *f, stroke=col, sw=5 * s)                                        # lead


def pe_wire(d: Doc, x1, y1, x2, y2, sw=8):
    d.line(x1, y1, x2, y2, stroke=GREEN, sw=sw)
    d.line(x1, y1, x2, y2, stroke=YELLOW, sw=sw * 0.45, dash="14 14", cap="butt")


def wire(d: Doc, x1, y1, x2, y2, col, sw=8):
    if col == "PE":
        pe_wire(d, x1, y1, x2, y2, sw)
    else:
        d.line(x1, y1, x2, y2, stroke=col, sw=sw)


def cross(d: Doc, x, y, r=16, sw=6):
    d.line(x - r, y - r, x + r, y + r, stroke=RED, sw=sw)
    d.line(x - r, y + r, x + r, y - r, stroke=RED, sw=sw)


def bench_tag(d: Doc, x, y, s, anchor="start", size=T_MIN):
    """An amber chip for a fact the step marks (verify on bench)."""
    w = len(s) * size * 0.56 + 24
    x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
    d.rect(x0, y - size * 0.95, w, size * 1.4, fill=AMBER_F, stroke=AMBER, sw=2.5, rx=8)
    d.text(x0 + w / 2, y + size * 0.05, s, size=size, anchor="middle", weight=700, fill=INK)


# ============================================================ diagram 1001 ===
def d1001_mains_bus() -> Doc:
    d = Doc(975, "Mains bus: each colour beeps from its C14 pin to every point")
    top = step_header(d, "Mains bus: one colour at a time")
    unplugged(d, 40, top + 16, 1120)

    ay = top + 106
    d.panel(30, ay, 1140, d.h - ay - 16)
    callout(d, 78, ay + 44, 1)
    d.text(120, ay + 56, "park one probe", size=T_MIN, weight=700, fill=MUTED)
    d.text(660, ay + 56, "walk the other along: beeps", size=T_MIN, weight=700, fill=OK)

    rows = [  # (bus label, wire colour, destinations)
        ("PE", "PE", ["PSU screw 3 FG", "frame lug screw", "DIN-rail lead's screw", "far frame corner"]),
        ("L", BROWN, ["PSU screw 1 L"]),
        ("N", WIRE_N, ["PSU screw 2 N"]),
    ]
    pin_label = {"PE": "E", "L": "L", "N": "N"}
    lh, gap = 46, 52
    y = ay + 130
    bx0, bx1 = 60, 340                       # the inlet module: C14 pins, fuse, rocker
    px = 130                                 # the C14 pins
    wx0, wx1 = 420, 540                      # the WAGO blocks
    blocks = []
    for name, col, dests in rows:
        ys = [y + i * lh for i in range(len(dests))]
        cy = (ys[0] + ys[-1]) / 2
        blocks.append((name, col, ys, dests, cy))
        y = ys[-1] + lh + gap
    d.rect(bx0, blocks[0][4] - 70, bx1 - bx0, blocks[-1][4] - blocks[0][4] + 140, fill=PANEL,
           stroke=RED, sw=4, rx=12)
    d.text((bx0 + bx1) / 2, blocks[-1][4] + 112, "C14 inlet module", size=T_MIN,
           anchor="middle", weight=700, fill=RED)
    sw_a, sw_b = 262, 306                    # the rocker's two contacts on each pole
    lever = {}
    for name, col, ys, dests, cy in blocks:
        d.text(bx0 + 14, cy + 11, pin_label[name], size=T_LAB, weight=800)
        if name == "PE":                     # earth: neither fused nor switched
            wire(d, px, cy, wx0, cy, col)
        else:
            wire(d, px, cy, sw_a, cy, col)
            wire(d, sw_b, cy, wx0, cy, col)
            d.circle(sw_a, cy, 7, fill=INK, stroke=INK, sw=1)
            d.circle(sw_b, cy, 7, fill=INK, stroke=INK, sw=1)
            d.line(sw_a, cy, sw_b + 4, cy - 14, stroke=INK, sw=5)     # contact closed: ON
            lever[name] = cy
        if name == "L":                      # the fuse, in series with Live only
            fx = 196
            d.rect(fx - 28, cy - 13, 56, 26, fill=PANEL, stroke=INK, sw=3, rx=4)
            d.line(fx - 28, cy, fx + 28, cy, stroke=INK, sw=2)
            d.text(fx, cy - 26, "fuse", size=T_MIN, anchor="middle", weight=700)
        d.circle(px, cy, 11, fill=INK, stroke=PANEL, sw=2)
        d.rect(wx0, cy - 34, wx1 - wx0, 68, fill=PANEL, stroke=RED, sw=4, rx=8)
        d.text((wx0 + wx1) / 2, cy + 11, name, size=T_LAB, anchor="middle", weight=800)
        for yy, s in zip(ys, dests):
            wire(d, wx1, cy, wx1 + 100, yy, col, sw=6)
            d.circle(wx1 + 108, yy, 10, fill=OK, stroke=PANEL, sw=2)
            d.text(wx1 + 134, yy + 11, s, size=T_MIN, weight=600)
    # the rocker breaks L and N together: one lever, two poles
    mx = (sw_a + sw_b) / 2 + 2
    d.line(mx, lever["L"] - 6, mx, lever["N"] - 6, stroke=INK, sw=3, dash="8 7")
    d.text(mx - 14, (lever["L"] + lever["N"]) / 2 + 10, "rocker", size=T_MIN, anchor="end",
           weight=700, fill=INK)
    # the probes: black parked on the E pin, red on the PE row's last point
    probe(d, px, blocks[0][4] - 4, -55, INK, 0.75)
    probe(d, wx1 + 108, blocks[0][2][-1] + 4, 140, RED, 0.62)
    y = legend_row(d, 54, blocks[-1][4] + 186, 2, ["Rocker ON for L and N; PE beeps either way"],
                   size=T_MIN)
    legend_row(d, 54, y + 30, 3, ["Ω rows: subtract the probes-together reading"],
               size=T_MIN)
    return d


# ============================================================ diagram 1006 ===
def d1006_isolation_pairs() -> Doc:
    d = Doc(740, "L, N and PE isolated: no pair beeps, at the WAGO blocks or the PSU screws")
    top = step_header(d, "Between colours: silent")
    unplugged(d, 40, top + 16, 1120)
    by = top + 106
    d.panel(30, by, 1140, d.h - by - 16)

    def group(x0, n, title, labels, cols, foot):
        callout(d, x0 + 28, by + 46, n)
        d.text(x0 + 70, by + 58, title, size=T_LAB, weight=700)
        xs = [x0 + 85 + i * 170 for i in range(3)]
        ty = by + 230
        for x, lab, col in zip(xs, labels, cols):
            d.rect(x - 64, ty - 36, 128, 72, fill=PANEL, stroke=RED, sw=4, rx=8)
            d.text(x, ty + 11, lab, size=T_LAB, anchor="middle", weight=800)
            wire(d, x, ty + 36, x, ty + 76, col, sw=7)
        for (a, b, h) in ((0, 1, 50), (1, 2, 50), (0, 2, 92)):
            xa, xb = xs[a], xs[b]
            d.path(f"M {xa} {ty - 40} C {xa} {ty - 40 - h * 1.3} {xb} {ty - 40 - h * 1.3} "
                   f"{xb} {ty - 40}", stroke=RED, sw=4, dash="10 8")
            cross(d, (xa + xb) / 2, ty - 40 - h, r=13, sw=5)
        d.text(x0 + 255, ty + 118, foot, size=T_MIN, anchor="middle", weight=600, fill=MUTED)

    # WAGO blocks in their bench order, left to right N, L, PE (Step 10.7);
    # PSU screws in datasheet order 1 L, 2 N, 3 FG
    group(60, 1, "at the WAGO blocks", ["N", "L", "PE"], [WIRE_N, BROWN, "PE"],
          "rocker on, then off")
    group(620, 2, "at the PSU screws", ["1 L", "2 N", "3 FG"], [BROWN, WIRE_N, "PE"],
          "the same three pairs")
    d.text(600, by + 430, "L to N: 100 kΩ or more, or OL", size=T_LAB, anchor="middle",
           weight=700)
    d.text(600, by + 476, "L or N to PE: OL", size=T_LAB, anchor="middle", weight=700)
    return d


# ============================================================ diagram 1002 ===
def d1002_cob_mount() -> Doc:
    d = Doc(1075, "COB light-strip mount: two inserts in the base, the lid on two screws")
    top = step_header(d, "COB mount: inserts, then the lid")
    d.panel(30, top + 16, 1140, 560)
    x0, x1 = 150, 1050
    L = x1 - x0

    def at(mm):                                   # position along a 100 mm mount
        return x0 + L * mm / 100.0
    ins = [at(6.0), at(94.0)]                     # insert bores, STL: 6 mm from each end
    shcs = [at(12.8), at(87.2)]                   # M3x8 SHCS counterbores, 12.8 mm from each end

    # lid half, lifted off (front view), countersunk holes over the inserts
    ly0, ly1 = top + 180, top + 242
    d.rect(x0, ly0, L, ly1 - ly0, fill=BLACKPART_F, stroke=BLACKPART, sw=4, rx=6)
    for x in ins:
        d.poly([(x - 22, ly0), (x + 22, ly0), (x + 9, ly0 + 22), (x - 9, ly0 + 22)], fill=PANEL,
               stroke=BLACKPART, sw=2.5)
        d.rect(x - 9, ly0 + 22, 18, ly1 - ly0 - 22, fill=PANEL, stroke=BLACKPART, sw=2.5)
    d.text(at(50), ly0 + 44, "lid half", size=T_LAB, anchor="middle", weight=700,
           fill=BLACKPART)

    # base half: its top face (inserts) and its front face (screw holes for 10.36)
    by0, bt, by1 = top + 330, top + 380, top + 490
    d.poly([(x0 + 30, by0), (x1 - 30, by0), (x1, bt), (x0, bt)], fill=GREY_F,
           stroke=BLACKPART, sw=4)
    d.rect(x0, bt, L, by1 - bt, fill=BLACKPART_F, stroke=BLACKPART, sw=4, rx=4)
    for x in ins:
        d.circle(x, (by0 + bt) / 2, 19, fill=GOLD, stroke=INK, sw=2.5)
        d.circle(x, (by0 + bt) / 2, 6, fill=PANEL, stroke=INK, sw=1.5)
    for x in shcs:
        d.circle(x, (bt + by1) / 2 + 4, 20, fill=PANEL, stroke=BLACKPART, sw=3)
        d.circle(x, (bt + by1) / 2 + 4, 10, fill=GREY_F, stroke=BLACKPART, sw=2)
    d.text(at(50), by1 - 30, "base half", size=T_LAB, anchor="middle", weight=700,
           fill=BLACKPART)

    # FHCS above the lid, dashed down through the lid into the inserts
    for x in ins:
        sy = top + 72
        d.poly([(x - 20, sy + 30), (x + 20, sy + 30), (x + 6, sy + 48), (x - 6, sy + 48)],
               fill=GREY_F, stroke=GREY, sw=2.5)
        d.rect(x - 6, sy + 48, 12, 40, fill=GREY_F, stroke=GREY, sw=2.5)
        d.line(x, sy + 96, x, (by0 + bt) / 2 - 18, stroke=MUTED, sw=2.5, dash="10 8")
    callout(d, ins[0] + 66, (by0 + bt) / 2 - 4, 1)
    callout(d, ins[1] - 66, (by0 + bt) / 2 - 4, 1)
    callout(d, ins[0] + 62, top + 102, 2)
    callout(d, ins[1] - 62, top + 102, 2)
    d.text(shcs[1] - 36, by1 + 52, "screw holes for step 10.36", size=T_MIN, anchor="end",
           weight=600, fill=MUTED)
    d.leader(shcs[1], (bt + by1) / 2 + 26, shcs[1] - 24, by1 + 30, col=MUTED)
    d.text(1150, top + 64, "Front view, lid lifted", size=T_MIN, anchor="end", weight=700,
           fill=MUTED)

    # ---- what else takes inserts in the same pass
    ty = top + 592
    d.panel(30, ty, 1140, d.h - ty - 16)
    y = legend_row(d, 54, ty + 58, 1, ["2 inserts in each mount's base half, at its ends"])
    y = legend_row(d, 54, y + 20, 2, ["lid on with two M3×6 FHCS"])
    rows = [("8 mounts: per strip, three 100 mm + one 50 mm", 0),
            ("retainer bracket ×2: 1 insert each", 1),
            ("TFT mount: 2 inserts, in its raised pads", 2)]
    yy = y + 30
    for s, n in rows:
        if n:
            d.circle(78, yy - 11, 13, fill=GOLD, stroke=INK, sw=2)
        d.text(110, yy, s, size=T_MIN, weight=600)
        yy += 44
    d.text(110, yy + 4, "20 inserts, one hot session", size=T_MIN, weight=800)
    return d


# ============================================================ diagram 1003 ===
def d1003_hat_pads() -> Doc:
    d = Doc(1070, "5 V check: probe the HAT adapter's pads over GPIO pins 2 and 6")
    top = step_header(d, "5 V check on the HAT adapter")
    unplugged(d, 40, top + 16, 1120)

    p = 48                                         # header pitch on the page
    cx0 = 176
    ye, yi = top + 386, top + 436                  # edge row (even pins), inner row (odd)
    bx0, by0 = 60, top + 330                       # Pi board, its GPIO edge at by0
    d.rect(bx0, by0, 1080, 520, fill=PI_GREEN_F, stroke=PI_GREEN, sw=4, rx=18)
    # bare header pins, columns 13-20
    d.rect(cx0 + 12 * p - 22, ye - 22, 8 * p - 4, yi - ye + 44, fill=INK, stroke=INK, sw=1, rx=4)
    for i in range(12, 20):
        for yy in (ye, yi):
            d.rect(cx0 + i * p - 7, yy - 7, 14, 14, fill=GOLD, stroke="none", sw=0)
    # the HAT adapter over pins 1-24: 2 x 12 bare pads on top
    ax0, ax1 = cx0 - 46, cx0 + 11 * p + 40
    d.rect(ax0, by0 + 12, ax1 - ax0, 330, fill=PCB, stroke=PCB_EDGE, sw=3, rx=10)
    for i in range(12):
        for yy in (ye, yi):
            d.circle(cx0 + i * p, yy, 14, fill=PAD, stroke="#8E959E", sw=2)
    # its 6-pin socket and the cable to J9
    sx, sy = cx0 + 3 * p, by0 + 250
    d.rect(sx - 20, sy - 26, 6 * 34 + 20, 52, fill="#F2F2F0", stroke=INK, sw=2.5, rx=4)
    for k in range(6):
        d.line(sx + k * 34, sy + 26, sx + k * 34 - 40 + k * 4, by0 + 450, stroke=INK, sw=6)
    d.text(sx + 250, by0 + 440, "6 wires to J9", size=T_MIN, weight=700, fill=INK)
    d.text(ax0 + 20, by0 + 192, "HAT adapter", size=T_LAB, weight=700, fill="#FFFFFF")

    # the probes, from above the board edge
    probe(d, cx0, ye, -110, RED, 1.0)
    probe(d, cx0 + 2 * p, ye, -62, INK, 1.0)
    d.text(cx0 - 110, top + 150, "5 V", size=T_LAB + 2, anchor="middle", weight=800, fill=RED)
    d.text(cx0 - 110, top + 190, "pin 2", size=T_MIN, anchor="middle", weight=700, fill=RED)
    d.text(cx0 + 2 * p + 150, top + 150, "GND", size=T_LAB + 2, anchor="middle", weight=800)
    d.text(cx0 + 2 * p + 150, top + 190, "pin 6", size=T_MIN, anchor="middle", weight=700)
    # orientation
    d.text(1120, by0 - 16, "board edge", size=T_MIN, anchor="end", weight=600, fill=MUTED)
    d.text(cx0 + 15 * p, yi + 80, "pins 25 to 40", size=T_MIN, anchor="middle", weight=600,
           fill=MUTED)
    d.text(bx0 + 20, by0 + 495, "microSD end", size=T_MIN, weight=700, fill=PI_GREEN)
    d.text(bx0 + 1060, by0 + 495, "USB and Ethernet end", size=T_MIN, anchor="end",
           weight=700, fill=PI_GREEN)
    dd.step_note(d, "Expect a number, never 0 Ω.", size=T_LAB + 2)
    return d


# ============================================================ diagram 1004 ===
def d1004_24v_points() -> Doc:
    d = Doc(1056, "24 V probe points: the PSU's DC screws and each 24 V input")
    top = step_header(d, "24 V probe points")
    unplugged(d, 40, top + 16, 1120)

    # ---- the PSU terminal strip, nine screws
    py = top + 106
    d.panel(30, py, 1140, 390)
    d.text(54, py + 54, "PSU terminal strip", size=T_LAB + 2, weight=700)
    pitch = 112
    xs = [100 + i * pitch for i in range(3)] + [100 + 3 * pitch + 60 + i * pitch for i in range(6)]
    sy = py + 236
    d.rect(xs[0] - 50, sy - 52, xs[2] - xs[0] + 100, 104, fill=RED_F, stroke=RED, sw=4, rx=8)
    d.rect(xs[3] - 50, sy - 52, xs[8] - xs[3] + 100, 104, fill=GREY_F, stroke=GREY, sw=3, rx=8)
    for x in xs:
        d.circle(x, sy, 30, fill=PANEL, stroke=INK, sw=3)
        d.line(x - 16, sy - 16, x + 16, sy + 16, stroke=INK, sw=4)
        d.line(x - 16, sy + 16, x + 16, sy - 16, stroke=INK, sw=4)
    for x, s in zip(xs[:3], ("1 L", "2 N", "3 FG")):
        d.text(x, sy + 86, s, size=T_LAB, anchor="middle", weight=800, fill=RED)
    # mains screws: 10.18, 10.19 and 10.77 meter 3 FG etc. unplugged; this test does not
    d.text((xs[0] + xs[2]) / 2, py + 112, "mains screws:", size=T_MIN, anchor="middle",
           weight=700, fill=RED)
    d.text((xs[0] + xs[2]) / 2, py + 150, "not in this test", size=T_MIN, anchor="middle",
           weight=700, fill=RED)
    finx = (xs[2] + xs[3]) / 2
    d.rect(finx - 7, sy - 92, 14, 184, fill=BLACKPART, stroke=BLACKPART, sw=1, rx=3)
    d.text(finx, sy - 104, "fin", size=T_MIN, anchor="middle", weight=700, fill=BLACKPART)
    d.text((xs[3] + xs[5]) / 2, sy + 86, "−V", size=T_LAB + 4, anchor="middle", weight=800)
    d.text((xs[6] + xs[8]) / 2, sy + 86, "+V", size=T_LAB + 4, anchor="middle", weight=800,
           fill=RED)
    d.text((xs[3] + xs[5]) / 2, sy + 124, "4 to 6", size=T_MIN, anchor="middle", weight=600,
           fill=MUTED)
    d.text((xs[6] + xs[8]) / 2, sy + 124, "7 to 9", size=T_MIN, anchor="middle", weight=600,
           fill=MUTED)
    probe(d, xs[4], sy - 30, -100, INK, 0.65)
    probe(d, xs[7], sy - 30, -80, RED, 0.65)
    d.text(1150, py + 54, "first: DC V reads 0 V for 10 s", size=T_MIN, anchor="end",
           weight=700, fill=OK)

    # ---- the three 24 V inputs
    iy = py + 406
    d.panel(30, iy, 1140, d.h - iy - 16)
    d.text(54, iy + 54, "Then on Ω, each input, + to −", size=T_LAB + 2, weight=700)
    inputs = [("Leviathan", "Vin 24V"), ("Leviathan", "Vin 24-48V"), ("USB adapter", "24V IN")]
    for i, (a, b) in enumerate(inputs):
        cx = 220 + i * 380
        ty = iy + 196
        d.rect(cx - 90, ty - 40, 180, 80, fill=GREY_F, stroke=INK, sw=3, rx=8)
        for k, sgn in enumerate(("+", "−")):
            x = cx - 44 + k * 88
            d.circle(x, ty, 24, fill=PANEL, stroke=INK, sw=3)
            d.text(x, ty + 13, sgn, size=T_LAB + 4, anchor="middle", weight=800,
                   fill=RED if sgn == "+" else INK)
        probe(d, cx - 44, ty - 24, -105, RED, 0.5)
        probe(d, cx + 44, ty - 24, -75, INK, 0.5)
        d.text(cx, ty + 84, a, size=T_MIN, anchor="middle", weight=700)
        d.mono(cx, ty + 120, b, size=T_MIN, anchor="middle", weight=700)
    d.text(600, iy + 372, "All four read the same, rising. Never 0 Ω.", size=T_LAB,
           anchor="middle", weight=700)
    d.text(600, iy + 414, "To the C14 earth pin: +V about the same, −V a few Ω.", size=T_MIN,
           anchor="middle", weight=600, fill=MUTED)
    return d


# ============================================================ diagram 1005 ===
def d1005_earth_points() -> Doc:
    d = Doc(1075, "Earth bonding: one probe on the C14 earth pin, the other on bare metal")
    top = step_header(d, "Earth: one probe stays on C14 E")
    unplugged(d, 40, top + 16, 1120)

    py = top + 106
    d.panel(30, py, 1140, 560)
    # C14 inlet, seen from outside: E pin centred above L and N
    ix, iy = 170, py + 290
    d.rect(ix - 110, iy - 120, 220, 240, fill=PANEL, stroke=RED, sw=4, rx=18)
    d.rect(ix - 80, iy - 90, 160, 180, fill=GREY_F, stroke=INK, sw=3, rx=26)
    pins = {"E": (ix, iy - 40), "L": (ix - 44, iy + 40), "N": (ix + 44, iy + 40)}
    for k, (x, y) in pins.items():
        d.rect(x - 8, y - 22, 16, 44, fill=INK, stroke=INK, sw=1, rx=3)
    d.text(ix - 30, iy - 32, "E", size=T_MIN, anchor="end", weight=800, fill=GREEN)
    d.text(ix, iy + 168, "C14 inlet", size=T_MIN, anchor="middle", weight=700, fill=RED)
    probe(d, ix + 8, iy - 50, -40, INK, 0.9)
    callout(d, ix - 76, iy - 160, 2)

    targets = [
        ("PE WAGO, any port", None, "< 1 Ω"),
        ("PSU screw 3 FG", None, "< 1 Ω"),
        ("frame PE lug", "its screw head", "< 1 Ω"),
        ("DIN rail", "its lead's screw head, bare rail", "< 1 Ω"),
        ("build plate", "the M4×6 screw head", "< 1 Ω"),
        ("far frame corner", "screw head or T-nut", "< 2–3 Ω"),
    ]
    y = py + 108
    for name, sub, val in targets:
        d.circle(460, y - 10, 13, fill=OK, stroke=PANEL, sw=2)
        d.text(490, y, name, size=T_LAB, weight=700)
        if sub:
            d.text(490, y + 38, sub, size=T_MIN, weight=600, fill=MUTED)
        w = len(val) * 19 + 30
        d.rect(1140 - w, y - 34, w, 50, fill=OK_F, stroke=OK, sw=2.5, rx=8)
        d.text(1140 - w / 2, y + 2, val, size=T_LAB, anchor="middle", weight=800, fill=OK)
        y += 86 if sub else 64
    d.text(470, py + 50, "other probe on bare metal; limits ours, not LDO's", size=T_MIN,
           weight=600, fill=MUTED)

    # ---- callout 1: probes together; and the wrong way, small
    by = py + 576
    d.panel(30, by, 560, d.h - by - 16)
    probe(d, 300, by + 110, -150, INK, 0.9)
    probe(d, 310, by + 110, -30, RED, 0.9)
    callout(d, 305, by + 170, 1)
    d.text(305, by + 226, "probes together:", size=T_MIN, anchor="middle", weight=700)
    d.text(305, by + 260, "subtract this reading", size=T_MIN, anchor="middle", weight=700)
    d.panel(610, by, 560, d.h - by - 16)
    d.text(634, by + 54, "Wrong", size=36, weight=700, fill=RED)
    d.rect(660, by + 130, 460, 60, fill=dd.BLUE_F, stroke=BLUE, sw=4, rx=4)
    d.text(890, by + 170, "anodised face", size=T_MIN, anchor="middle", weight=700, fill=BLUE)
    probe(d, 860, by + 130, -60, RED, 0.6)
    cross(d, 790, by + 84, r=20, sw=7)
    d.text(890, by + 226, "reads OL: the oxide", size=T_MIN, anchor="middle", weight=700,
           fill=RED)
    d.text(890, by + 260, "does not conduct", size=T_MIN, anchor="middle", weight=700,
           fill=RED)
    return d


# ============================================================ diagram 1007 ===
def d1007_din_rail_earth() -> Doc:
    d = Doc(1075, "DIN-rail earth lead: a ring under the rear rail's screw, its lead to the PE WAGO")
    top = step_header(d, "Earth the SSR's DIN rail")
    unplugged(d, 40, top + 16, 1120)

    # ---- plan view: the rear rail, SSR left, PSU right, the screw in the gap
    ay = top + 106
    d.panel(30, ay, 1140, 440)
    d.text(54, ay + 50, "The rear rail, looking into the bay", size=T_MIN, weight=700,
           fill=MUTED)
    ry0, ry1 = ay + 120, ay + 220
    d.rect(50, ry0, 1100, ry1 - ry0, fill=GREY_F, stroke=STEEL, sw=3, rx=4)        # rail
    for x in range(90, 1130, 110):                                                 # slots
        d.rect(x, (ry0 + ry1) / 2 - 10, 70, 20, fill=PANEL, stroke=STEEL, sw=2, rx=10)
    d.rect(120, ry0 - 40, 230, ry1 - ry0 + 80, fill=BLACKPART_F, stroke=BLACKPART, sw=4,
           rx=8)
    d.text(235, (ry0 + ry1) / 2 + 12, "SSR", size=T_LAB, anchor="middle", weight=800)
    d.rect(560, ry0 - 40, 580, ry1 - ry0 + 80, fill=PANEL, stroke=INK, sw=4, rx=8)
    d.text(850, (ry0 + ry1) / 2 + 12, "PSU", size=T_LAB, anchor="middle", weight=800)
    sx, sy = 455, (ry0 + ry1) / 2                                                  # the screw
    d.circle(sx, sy, 40, fill=YELLOW, stroke=GREEN, sw=6)                          # ring
    d.circle(sx, sy, 24, fill=STEEL, stroke=INK, sw=3)                             # head
    d.poly([(sx - 9, sy - 5), (sx, sy - 10), (sx + 9, sy - 5), (sx + 9, sy + 5),
            (sx, sy + 10), (sx - 9, sy + 5)], fill=INK, stroke=INK, sw=1)
    callout(d, sx + 72, ry0 - 18, 1)
    bench_tag(d, 850, ry1 + 84, "screw spot: check on the bench", anchor="middle")
    # the lead: down from the ring to the PE WAGO
    wy = ay + 360
    pe_wire(d, sx - 30, sy + 30, sx - 30, wy - 70, sw=10)
    ports = ["inlet", "PSU", "frame", "rail", "bed"]
    px0, pw = 70, 52
    rx = px0 + 3 * pw + pw / 2                                                     # rail port
    pe_wire(d, sx - 30, wy - 70, rx, wy - 70, sw=10)
    pe_wire(d, rx, wy - 70, rx, wy - 16, sw=10)
    d.rect(px0 - 14, wy - 30, len(ports) * pw + 28, 70, fill=PANEL, stroke=RED, sw=4, rx=8)
    for i, lab in enumerate(ports):
        x = px0 + i * pw + pw / 2
        free = lab == "bed"
        d.rect(x - 18, wy - 16, 36, 42, fill=PANEL if free else GREEN, stroke=INK, sw=2,
               rx=4)
    d.text(px0 + len(ports) * pw + 40, wy + 14, "PE WAGO: one port left for the bed",
           size=T_MIN, weight=700)
    callout(d, rx - 70, wy - 76, 2)

    # ---- section through the screw
    by = ay + 456
    d.panel(30, by, 1140, d.h - by - 16)
    d.text(54, by + 50, "Section through the screw, head up", size=T_MIN, weight=700,
           fill=MUTED)
    bench_tag(d, 1150, by + 50, "M5×12 length: check on the bench", anchor="end")
    cx = 300
    layers = [  # (label, top, height, fill, stroke)
        ("serrated washer", 186, 12, STEEL, INK),
        ("DIN rail, bare steel", 198, 16, GREY_F, STEEL),
        ("deck panel", 214, 40, PANEL, GREY),
    ]
    # extrusion with its slot and T-nut
    ey = by + 254
    d.rect(90, ey, 420, 110, fill=GREY_F, stroke=GREY, sw=3)
    d.rect(cx - 34, ey, 68, 18, fill=PANEL, stroke=GREY, sw=2)                    # slot lip gap
    d.rect(cx - 70, ey + 18, 140, 70, fill=PANEL, stroke=GREY, sw=2)               # slot cavity
    d.rect(cx - 60, ey + 30, 120, 34, fill=STEEL, stroke=INK, sw=2.5, rx=4)        # T-nut
    # screw shank
    d.rect(cx - 13, by + 150, 26, ey + 52 - (by + 150), fill=STEEL, stroke=INK, sw=2)
    # stack layers, drawn over the shank
    for lab, t0, h, fill, stroke in layers:
        d.rect(cx - 150, by + t0, 300, h, fill=fill, stroke=stroke, sw=2.5)
        d.rect(cx - 13, by + t0, 26, h, fill=STEEL, stroke=INK, sw=1.5)
    # washer teeth
    for k in range(-5, 6):
        if abs(k) > 0:
            d.line(cx + k * 24, by + 186, cx + k * 24 + 8, by + 198, stroke=INK, sw=2)
    # ring terminal tongue, with the lead leaving to the left
    d.rect(cx - 70, by + 174, 140, 12, fill=YELLOW, stroke=GREEN, sw=2.5, rx=3)
    pe_wire(d, cx - 70, by + 180, 70, by + 180, sw=10)
    d.rect(cx - 13, by + 174, 26, 12, fill=STEEL, stroke=INK, sw=1.5)
    # BHCS head
    d.path(f"M {cx - 50} {by + 174} C {cx - 46} {by + 120} {cx + 46} {by + 120} "
           f"{cx + 50} {by + 174} Z", fill=STEEL, stroke=INK, sw=3)
    callout(d, cx, by + 104, 1)
    # labels with leaders
    labs = [("M5×12 BHCS", by + 150), ("ring terminal", by + 180),
            ("serrated washer", by + 192), ("DIN rail, bare steel", by + 206),
            ("deck panel", by + 234), ("T-nut, bed extrusion", ey + 47)]
    ly = by + 130
    for s, yy in labs:
        d.leader(cx + 160, yy, 640, ly - 10, col=MUTED)
        d.text(650, ly, s, size=T_MIN, weight=700)
        ly += 44
    return d


# ================================================================= registry ===
DIAGRAMS = [
    {
        "n": 1001,
        "file": "1001-mains-bus-probe-points.svg",
        "title": "Mains bus: one colour at a time",
        "fn": d1001_mains_bus,
        "shows": [
            "The precondition in the picture: unplugged, cord out of the room.",
            "The inlet module: its C14 E, L and N pins, the fuse in series with L, the rocker "
            "breaking L and N together (drawn ON), E neither fused nor switched; each wire in "
            "its colour to its WAGO block and on to every point the 10.18 tables list: PE to PSU 3 FG, the "
            "frame lug, the DIN-rail lead's screw (10.82) and a far frame corner; L to PSU 1 L; N to PSU 2 N. "
            "One probe parked on the pin, the other walked along.",
            "Callouts 1 to 3 are the Do numbers of Step 10.18.",
        ],
        "insert": [
            ("10-wiring.md", "Step 10.18", "replaces the no-image line"),
        ],
        "verify": [
            "A wiring schematic, not a layout: block positions do not match the bay. Fuse and "
            "rocker placement inside the module from LDO's inlet_layout.png. The SSR and bed are "
            "not drawn: as in LDO's order, they are wired after this checkpoint (Section 2b).",
        ],
    },
    {
        "n": 1006,
        "file": "1006-mains-isolation-pairs.svg",
        "title": "Between colours: silent",
        "fn": d1006_isolation_pairs,
        "shows": [
            "The precondition in the picture: unplugged, cord out of the room.",
            "The three pairs L-N, L-PE and N-PE crossed out at the WAGO blocks, drawn in their "
            "bench order N, L, PE (Step 10.7; rocker on, then off) and at the PSU screws 1 L, 2 N, 3 FG, with the expected readings: L to N "
            "100 kΩ or more or OL, L or N to PE OL. Callouts 1 and 2 are the Do numbers of "
            "Step 10.19.",
        ],
        "insert": [
            ("10-wiring.md", "Step 10.19", "replaces the no-image line"),
        ],
        "verify": [],
    },
    {
        "n": 1002,
        "file": "1002-cob-mount-inserts.svg",
        "title": "COB mount: inserts, then the lid",
        "fn": d1002_cob_mount,
        "shows": [
            "Front view of one COB mount with the lid half lifted: two inserts in the base "
            "half's top face, 6 mm from each end; the lid's two countersunk holes over them and "
            "two M3×6 FHCS going in; the base half's two counterbored holes, 12.8 mm from each "
            "end, left for Step 10.36.",
            "Below: the 8 mounts (three 100 mm and one 50 mm per strip), the two retainer "
            "brackets with one insert each and the TFT mount with two, 20 inserts in one pass. "
            "Callouts 1 and 2 are the Do numbers of Step 10.35.",
        ],
        "insert": [
            ("10-wiring.md", "Step 10.35", "replaces the no-image line"),
        ],
        "verify": [
            "Insert and screw positions are from the 100 mm STL (numpy bore probe) and LDO's "
            "cob_mount_install.png; the halves' cross-section is not drawn, and the strip is "
            "left out because the sources do not show how it sits in the mount.",
        ],
    },
    {
        "n": 1003,
        "file": "1003-hat-adapter-5v-pads.svg",
        "title": "5 V check on the HAT adapter",
        "fn": d1003_hat_pads,
        "shows": [
            "Top view of the Pi 4's GPIO edge with the 3/4 HAT adapter over pins 1 to 24 "
            "(2 × 12 bare pads on top), pins 25 to 40 bare beside it, the adapter's 6-pin "
            "socket and its cable to J9.",
            "Red probe on the edge-row pad at the microSD end (pin 2, 5 V), black probe on "
            "the third pad of that row (pin 6, GND); pin 4 also 5 V. Unplugged, in the picture.",
        ],
        "insert": [
            ("10-wiring.md", "Step 10.75", "replaces the no-image line"),
        ],
        "verify": [
            "Board outline and adapter shape are schematic. Pin positions follow pinout.xyz "
            "(pin 1 at the end away from the USB ports, even pins on the board edge) and LDO's "
            "rpi4_installed_V1.3.jpg (12 columns of pads on the adapter).",
        ],
    },
    {
        "n": 1004,
        "file": "1004-24v-probe-points.svg",
        "title": "24 V probe points",
        "fn": d1004_24v_points,
        "shows": [
            "The PSU's nine screws in datasheet order, 1 L, 2 N, 3 FG (mains screws, not part "
            "of this test; 10.18, 10.19 and 10.77 meter them with the cord out), "
            "the fin, then 4 to 6 −V and 7 to 9 +V, with the black probe on −V and the red on "
            "+V; first DC V, 0 V for ten seconds (10.73).",
            "Then on Ω the three 24 V inputs, Leviathan Vin 24V, Vin 24-48V and the USB "
            "adapter's 24V IN, + to −: all read the same, never 0 Ω; and the two rows to the "
            "C14 earth pin (10.74).",
        ],
        "insert": [
            ("10-wiring.md", "Step 10.73", "replaces the no-image line"),
            ("10-wiring.md", "Step 10.74", "replaces the no-image line"),
        ],
        "verify": [
            "Screw order from the Mean Well LRS-200 datasheet; the inputs are drawn as "
            "generic two-screw blocks, not their real shapes or positions on the boards.",
        ],
    },
    {
        "n": 1005,
        "file": "1005-earth-bonding-points.svg",
        "title": "Earth: one probe stays on C14 E",
        "fn": d1005_earth_points,
        "shows": [
            "The C14 inlet seen from outside with the black probe on its E pin, and the six "
            "bonding points from the 10.77 table with their limits: PE WAGO, PSU 3 FG, the "
            "frame lug's screw head, the DIN rail (its lead's screw head from 10.82, then bare "
            "rail), the plate's M4×6 screw head (< 1 Ω each) and a far frame corner's screw "
            "head or T-nut (< 2–3 Ω), labelled as our own limits, not LDO's.",
            "Callout 1: probes touched together, the reading to subtract. Callout 2: the probe "
            "on the earth pin. A small Wrong panel: a probe on an anodised face reads OL.",
        ],
        "insert": [
            ("10-wiring.md", "Step 10.77", "first image: what the hands do"),
        ],
        "verify": [
            "A checklist picture, not a layout. The extruder, heater, C14 L/N and 24 V rows "
            "of the 10.77 table stay in the table.",
        ],
    },
    {
        "n": 1007,
        "file": "1007-din-rail-earth-lead.svg",
        "title": "Earth the SSR's DIN rail",
        "fn": d1007_din_rail_earth,
        "shows": [
            "The precondition in the picture: unplugged, cord out of the room.",
            "Plan view of the rear DIN rail with the SSR on the left and the PSU on the right; "
            "the rail screw in the gap between them carries the ring terminal (callout 1), and "
            "the green/yellow lead runs along the PSU leads to the PE WAGO, whose five ports "
            "are inlet, PSU, frame, rail and one left free for the bed (callout 2).",
            "Section through the screw, head up: M5×12 BHCS, ring terminal, serrated washer, "
            "the rail's bare steel, the deck panel and the T-nut in the bed extrusion. "
            "Callouts 1 and 2 are the Do numbers of Step 10.82.",
        ],
        "insert": [
            ("10-wiring.md", "Step 10.82", "first image: what the hands do"),
        ],
        "verify": [
            "This lead is this build's addition; LDO runs no wire to the rail. The screw in "
            "the SSR-PSU gap is from LDO's S0 placement photo and CAD (two M5×10 BHCS per "
            "rail into deck T-nuts); its spot and the M5×12 length are drawn as bench "
            "checks. Proportions are schematic.",
        ],
    },
]
