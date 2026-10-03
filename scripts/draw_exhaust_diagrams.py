#!/usr/bin/env python3
"""Diagrams for Ch 14 Part H, the chamber exhaust add-on (Steps 14.25-14.36).

    python3 scripts/draw_exhaust_diagrams.py                # the three SVGs
    python3 scripts/draw_exhaust_diagrams.py --parts-sheet  # + the print-set sheet (needs matplotlib)

Writes docs/manual/assets/diagrams/exhaust-{a-lead-route,b-jumpers,c-control}.svg
and, with --parts-sheet, docs/manual/assets/parts/sheet-addon-exhaust.png.

Same primitives, palette and dark-mode handling as scripts/draw_diagrams.py
(imported, not copied): a light background rect and `color` pinned on the <svg>
root. Kept out of draw_diagrams.py's DIAGRAMS registry so the add-on's pictures
can be dropped with the add-on; that file's MANIFEST.md is not touched.

Every fact is transcribed from Ch 14 Part H, review/2026-10-03-exhaust/DESIGN.md
and LDO's Leviathan V1.3 photos; the footers say what is drawn schematically.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import draw_diagrams as D  # noqa: E402
from draw_diagrams import (Doc, header, footer, INK, MUTED, FAINT, RULE, PANEL, BG,  # noqa: E402
                           ORANGE, ORANGE_F, BLUE, BLUE_F, GREY, GREY_F, STEEL, BLACKPART,
                           BLACKPART_F, RED, GREEN, AMBER, AMBER_F, OK, OK_F, MONO)

OUT = D.OUT
LEAD = "#0E8F86"          # the fan lead: teal (BELT_A's hue), distinct from every part colour
LEAD_F = "#D6EFEC"


# ============================================================== (a) lead route
def _call(d, x, y, tx, ty, lines, anchor="start"):
    """Numbered callout: bold first line, muted rest; the leader stops at the
    near end of the first line instead of running through the text."""
    w = max(len(t) for t, _ in lines) * 6.4
    ex = tx + w + 8 if anchor == "start" else tx - w - 8
    d.leader(x, y, ex, ty - 4)
    for i, (t, c) in enumerate(lines):
        d.text(tx, ty + i * 15, t, size=12.3, anchor=anchor, fill=c, weight=700 if i == 0 else 400)


def da_lead_route() -> Doc:
    d = Doc(780, "Exhaust fan lead route, housing to Leviathan FAN0")
    top = header(d, "Exhaust fan lead: housing to FAN0",
                 "The fan sits outside the chamber. Its lead goes in through the grill, down the "
                 "inside of the back panel to the Z-chain notch, then through the bay to FAN0.",
                 "Ch 14, Steps 14.25 · 14.29 · 14.31")

    # ---------------- left: rear elevation, seen from behind ----------------
    px0, py0, pw, ph = 40, top + 14, 640, 590
    d.panel(px0, py0, pw, ph, "From behind the printer",
            "your right = the printer's left · dashed = inside the chamber")
    s = 0.64                                  # px per mm
    cx = px0 + pw / 2                         # machine centre line
    pan_w, pan_h = 483 * s, 503 * s           # LDO back panel 483 x 503
    pan_top = py0 + 110
    pl, pr = cx - pan_w / 2, cx + pan_w / 2
    pan_bot = pan_top + pan_h
    ext = 20 * s
    fl, fw = pl - ext * 0.6, pan_w + ext * 1.2
    # frame: top rear extrusion, two rear verticals, bottom rear extrusion
    d.rect(fl, pan_top - ext * 0.55, fw, ext, fill=BLUE_F, stroke=BLUE, sw=1.8)
    d.rect(fl, pan_bot - ext * 0.45, fw, ext, fill=BLUE_F, stroke=BLUE, sw=1.8)
    for x in (fl, pr - ext * 0.4):
        d.rect(x, pan_top - ext * 0.55, ext, pan_h + ext * 0.1, fill=BLUE_F, stroke=BLUE, sw=1.8)
    # panel with the centred 147 x 42.5 notch
    nw, nd = 147 * s, 42.5 * s
    nl, nr = cx - nw / 2, cx + nw / 2
    d.path(f"M{pl:.1f},{pan_top:.1f} L{nl:.1f},{pan_top:.1f} L{nl:.1f},{pan_top + nd:.1f} "
           f"L{nr:.1f},{pan_top + nd:.1f} L{nr:.1f},{pan_top:.1f} L{pr:.1f},{pan_top:.1f} "
           f"L{pr:.1f},{pan_bot:.1f} L{pl:.1f},{pan_bot:.1f} Z",
           fill=GREY_F, stroke=GREY, sw=1.6)
    d.text(pl + 10, pan_bot - 12, "back panel 483 x 503", size=11.5, fill=MUTED)
    # bay below the bottom extrusion
    bay_t, bay_b = pan_bot + ext * 0.55, pan_bot + ext * 0.55 + 58
    d.rect(fl, bay_t, fw, bay_b - bay_t, fill=PANEL, stroke=GREY, sw=1.4, dash="5 4")
    d.text(fl + 10, bay_b - 10, "electronics bay, under the deck", size=11.5, fill=MUTED)

    # Z chain inside the chamber, a little to the printer's right of centre
    # (= a little LEFT of centre seen from behind; CAD x 126-142 on the 250)
    zc = cx - 14 * s
    for i in range(8):
        yy = pan_bot - 24 - i * 22
        d.rect(zc - 8, yy - 10, 16, 20, fill="none", stroke=FAINT, sw=1.3, rx=4)
    d.rect(zc - 14, pan_bot - 3, 28, 12, fill=BG, stroke=RED, sw=2, rx=2)

    # housing (outside): 171 wide, top 6.5 below the panel top, 144 tall overall
    hw = 171 * s
    hl, hr = cx - hw / 2, cx + hw / 2
    ht, hb, hbot = pan_top + 6.5 * s, pan_top + 112 * s, pan_top + 144 * s
    d.path(f"M{hl:.1f},{ht:.1f} L{hr:.1f},{ht:.1f} L{hr:.1f},{hb:.1f} "
           f"L{cx + 42 * s:.1f},{hbot:.1f} L{cx - 42 * s:.1f},{hbot:.1f} "
           f"L{hl:.1f},{hb:.1f} Z", fill=BLACKPART_F, stroke=BLACKPART, sw=2.4)
    # notch outline, hidden behind the housing
    d.path(f"M{nl:.1f},{pan_top:.1f} L{nl:.1f},{pan_top + nd:.1f} L{nr:.1f},{pan_top + nd:.1f} "
           f"L{nr:.1f},{pan_top:.1f}", stroke=GREY, sw=1.4, dash="4 3")
    # access cover outline on the outer face
    d.rect(cx - 67 * s, pan_top + 30 * s, 134 * s, 72 * s, fill="none", stroke=ORANGE, sw=2, rx=4)
    # fan + fan grill on the angled bottom face
    fy = hbot
    d.rect(cx - 33 * s, fy, 66 * s, 20 * s, fill=GREY_F, stroke=GREY, sw=2, rx=3)
    d.rect(cx - 33 * s, fy + 20 * s, 66 * s, 4 * s, fill=ORANGE_F, stroke=ORANGE, sw=1.6)
    for k in (-1, 0, 1):
        d.line(cx + k * 14 * s, fy + 30 * s, cx + k * 22 * s, fy + 58 * s, stroke=MUTED, sw=1.6,
               dash="3 4")
    # mounts at the notch ends, on the top rear extrusion
    for mx in (nl + 10 * s, nr - 10 * s):
        d.rect(mx - 10 * s, pan_top - 20 * s, 20 * s, 30 * s, fill=ORANGE_F, stroke=ORANGE, sw=1.8, rx=3)

    # ---- the lead ----
    lx = cx + 40 * s                          # flat on the panel's inside face, beside the chain
    fan_out = (cx + 18 * s, fy + 4 * s)
    p_in = (cx + 18 * s, pan_top + 22 * s)    # up inside the housing to the grill
    d.path(f"M{fan_out[0]:.1f},{fan_out[1]:.1f} L{p_in[0]:.1f},{p_in[1]:.1f}",
           stroke=LEAD, sw=3.2, dash="2 5")
    d.path(f"M{p_in[0]:.1f},{p_in[1]:.1f} L{lx:.1f},{pan_top + 60 * s:.1f} "
           f"L{lx:.1f},{pan_bot - 24:.1f} L{zc + 5:.1f},{pan_bot:.1f} "
           f"L{zc + 5:.1f},{bay_t + 30:.1f}",
           stroke=LEAD, sw=3.2, dash="9 5", marker="arwa")
    for i in range(4):                          # VHB tie points
        ty = pan_top + 120 * s + i * 85 * s
        d.rect(lx - 6, ty - 6, 12, 12, fill=LEAD_F, stroke=LEAD, sw=1.6, rx=2)

    L, Rx = px0 + 16, px0 + pw - 16
    _call(d, hl + 8, pan_top + 60 * s, L, pan_top + 14,
          [("1  Housing, outside", INK), ("over the notch; grill in", MUTED),
           ("the notch, 2 mounts on", MUTED), ("the top rear extrusion", MUTED)])
    _call(d, cx - 30 * s, fy + 10 * s, L, fy - 6,
          [("2  Fan on the angled", INK), ("bottom face, air out", MUTED), ("and down; lead fed", MUTED),
           ("inside the housing", MUTED)])
    _call(d, zc - 8, pan_bot - 120, L, pan_bot - 120,
          [("Z chain (inside)", MUTED)])
    _call(d, p_in[0] + 2, p_in[1], Rx, pan_top - 36,
          [("3  In through a grill", INK), ("opening, into the chamber", MUTED)], anchor="end")
    _call(d, lx + 7, pan_top + 205 * s, Rx, pan_top + 150 * s,
          [("4  Down the panel's inside", INK), ("face on VHB tie points,", MUTED),
           ("flat, beside the Z chain,", MUTED), ("clear of bed and gantry", MUTED)], anchor="end")
    _call(d, zc + 14, pan_bot + 3, Rx, pan_bot - 30,
          [("5  Through the Z-chain", INK), ("notch into the bay", MUTED)], anchor="end")

    # ---------------- right: the bay from below ----------------
    bx0, by0, bw, bh = 700, top + 14, 460, 590
    d.panel(bx0, by0, bw, bh, "In the bay, seen from below",
            "machine on its side, rear at the bottom, as Ch 10's layout photo")
    gx, gy, gw, gh = bx0 + 26, by0 + 84, bw - 52, 400
    d.rect(gx, gy, gw, gh, fill=BG, stroke=BLUE, sw=2.4, rx=6)
    d.text(gx + gw / 2, gy - 8, "FRONT", size=11.5, anchor="middle", fill=MUTED, weight=700)
    d.text(gx + gw - 8, gy + gh + 18, "REAR", size=11.5, anchor="end", fill=MUTED, weight=700)
    # DC conduit loop (layout v3), drawn as a band
    cm = 24
    mid = gy + 40 + (gh - 92) * 0.50
    d.rect(gx + cm, gy + 40, gw - 2 * cm, gh - 92, fill="none", stroke=BLACKPART, sw=11, rx=22, op=0.18)
    d.line(gx + cm, mid, gx + gw - cm, mid, stroke=BLACKPART, sw=9, op=0.18)
    d.text(gx + gw - cm - 4, gy + 30, "printed DC conduit (B11)", size=11, anchor="end", fill=MUTED)
    # Leviathan: front half, left of centre
    lvx, lvy, lvw, lvh = gx + 50, gy + 62, 196, 104
    d.rect(lvx, lvy, lvw, lvh, fill=BLACKPART_F, stroke=BLACKPART, sw=2.2, rx=6)
    d.text(lvx + 12, lvy + 24, "Leviathan", size=13.5, weight=700)
    d.text(lvx + 12, lvy + 42, "fan-header row:", size=11.5, fill=MUTED)
    hdr = ["PRB", "F0", "F1", "F2", "F3"]
    for i, h in enumerate(hdr):
        x = lvx + 12 + i * 36
        new = h == "F0"
        d.rect(x, lvy + lvh - 30, 30, 18, fill=ORANGE_F if new else GREY_F,
               stroke=ORANGE if new else GREY, sw=2 if new else 1.4, rx=2)
        d.text(x + 15, lvy + lvh - 17, h, size=10.5, anchor="middle", weight=700 if new else 500)
    # PSU, SSR, AC side (context only)
    d.rect(gx + gw - 190, gy + 222, 150, 96, fill=PANEL, stroke=GREY, sw=1.4, rx=4)
    d.text(gx + gw - 115, gy + 274, "PSU", size=12, anchor="middle", fill=MUTED)
    d.rect(gx + 60, gy + 222, 66, 58, fill=PANEL, stroke=GREY, sw=1.4, rx=4)
    d.text(gx + 93, gy + 255, "SSR", size=12, anchor="middle", fill=MUTED)
    d.rect(gx + 52, gy + 292, 116, 40, fill=PANEL, stroke=RED, sw=1.4, rx=4, dash="4 3")
    d.text(gx + 110, gy + 317, "AC side", size=11.5, anchor="middle", fill=RED)
    # Z-chain notch at the rear, near the centre
    nx, ny = gx + gw / 2, gy + gh - 16
    d.rect(nx - 15, ny - 8, 30, 16, fill=BG, stroke=RED, sw=2, rx=2)
    d.text(nx - 24, ny + 4, "Z-chain notch", size=11.5, anchor="end", fill=RED, weight=600)
    # route: notch -> DC conduit (rear run, right side, middle run) -> FAN0
    rr = gx + gw - cm
    rb = gy + gh - 52
    f0x, f0y = lvx + 12 + 36 + 15, lvy + lvh - 12
    d.path(f"M{nx:.1f},{ny - 8:.1f} L{nx + 34:.1f},{rb:.1f} L{rr - 18:.1f},{rb:.1f} "
           f"Q{rr:.1f},{rb:.1f} {rr:.1f},{rb - 18:.1f} L{rr:.1f},{mid + 18:.1f} "
           f"Q{rr:.1f},{mid:.1f} {rr - 18:.1f},{mid:.1f} L{f0x + 18:.1f},{mid:.1f} "
           f"Q{f0x:.1f},{mid:.1f} {f0x:.1f},{mid - 18:.1f} L{f0x:.1f},{f0y + 6:.1f}",
           stroke=LEAD, sw=3.2, marker="arwa")
    d.text(f0x + 26, mid - 10, "with the DC bundle, as FILTER FAN", size=11.5, fill=LEAD, weight=600)
    d.text(lvx + lvw + 10, lvy + lvh - 16, "6  FAN0", size=12.5, weight=700)
    d.mono(lvx + lvw + 10, lvy + lvh - 1, "PB7", size=11.5, fill=MUTED)
    # the numbers
    yy = gy + gh + 44
    d.wrap(gx, yy, "Step 14.25 strings this route from the housing's bottom face to FAN0: up to "
           "1250 mm takes the 1 m extension, longer takes 1.5 m.", size=12.3, width_chars=58,
           lh=17, fill=INK)

    footer(d, "Schematic. To scale: the back panel and its centred 147 x 42.5 mm notch (350_Back_Panel.DXF) and "
              "the housing over it (Voron CAD). Drawn from Ch 10's layout v3, not measured: the Z chain's "
              "position, the bay layout, the board's orientation and the lead's exact path. Step 14.25 strings "
              "the real route, and stops the add-on if none exists without cutting.")
    return d


# ======================================================== (b) jumper block
def db_jumpers() -> Doc:
    d = Doc(668, "Leviathan voltage-selection jumpers after Part H")
    top = header(d, "Leviathan jumpers after Part H: three at 24 V",
                 "FAN0 now carries the exhaust fan and a third 24 V jumper. Fan2 and Fan3 are unchanged "
                 "from Step 10.28; Probe and Fan1 stay bare.",
                 "Ch 14, Step 14.31 · Ch 10, Step 10.28")

    # board: the left end of its bottom edge, edge at the bottom as in LDO's photos
    bx, by, bw = 40, top + 18, 700
    jy = by + 104               # top of each selection header
    edge = jy + 176             # the board's bottom edge
    d.rect(bx, by, bw, edge - by, fill=PANEL, stroke=BLACKPART, sw=2.6, rx=10)
    d.text(bx + 20, by + 32, "LDO Leviathan V1.3 — bottom edge, left end", size=15, weight=700)
    d.text(bx + 20, by + 52, "as in LDO's photos: the ports along the edge, each port's selection", size=12,
           fill=MUTED)
    d.text(bx + 20, by + 68, "header just above it, its 24 V pin at the top", size=12, fill=MUTED)

    ports = [("Z-PROBE", ("PF1", "GND", "PWR"), False, "bare"),
             ("FAN0", ("T", "PB7", "+"), True, "exhaust fan · NEW"),
             ("FAN1", ("T", "PB3", "+"), False, "bare"),
             ("FAN2", ("T", "PF7", "+"), True, "2 x 6020 bay fans"),
             ("FAN3", ("T", "PF9", "+"), True, "Nevermore filter fan")]
    colw = 130
    x0 = bx + 30
    pin = 18
    for i, (name, labels, fitted, note) in enumerate(ports):
        x = x0 + i * colw
        new = name == "FAN0"
        if new:
            d.rect(x - 8, jy - 22, colw - 6, edge - jy + 112, fill="none", stroke=ORANGE, sw=2.2, rx=8,
                   dash="7 5")
        # selection header: 3 pins stacked, 24V top, 5V bottom
        hx = x + 46
        for k in range(3):
            d.rect(hx, jy + k * (pin + 6), pin, pin, fill=GREY_F, stroke=GREY, sw=1.6, rx=2)
        if i == 0:
            d.text(hx - 8, jy + 14, "24V", size=11, anchor="end", fill=MUTED, weight=600)
            d.text(hx - 8, jy + 2 * (pin + 6) + 14, "5V", size=11, anchor="end", fill=MUTED, weight=600)
        if fitted:
            d.rect(hx - 5, jy - 5, pin + 10, 2 * pin + 16, fill=OK, stroke=OK, sw=2, rx=4)
            d.text(hx + pin / 2, jy + pin + 8, "24V", size=10.5, anchor="middle", fill="#FFFFFF",
                   weight=700)
        else:
            d.text(hx + pin + 10, jy + pin + 10, "bare", size=11.5, fill=MUTED, weight=600)
        d.mono(x + 56, jy + 94, name, size=13.5, anchor="middle", weight=700)
        d.text(x + 56, jy + 110, note, size=11, anchor="middle", fill=ORANGE if new else MUTED,
               weight=700 if new else 400)
        # the port: JST-XH 3-pin at the board edge
        cy = edge - 40
        for k, t in enumerate(labels):
            d.mono(x + 26 + k * 30, cy - 8, t, size=11, anchor="middle", weight=600)
        d.rect(x + 8, cy, 96, 40, fill=PANEL, stroke=INK, sw=2, rx=3)
        for k in range(3):
            d.circle(x + 26 + k * 30, cy + 20, 5, fill=STEEL, stroke=GREY, sw=1.4)
        if new:
            # the fan's 2-pin plug, from below, on the signal and + pins
            d.rect(x + 38, edge + 2, 66, 24, fill=ORANGE_F, stroke=ORANGE, sw=2, rx=3)
            d.text(x + 71, edge + 18, "2-pin plug", size=10.5, anchor="middle", weight=600)
            d.line(x + 56, edge + 26, x + 56, edge + 70, stroke=INK, sw=2.6)
            d.line(x + 86, edge + 26, x + 86, edge + 70, stroke=RED, sw=2.6)
            d.text(x + 92, edge + 52, "red on +", size=10.5, fill=RED, weight=600)
            d.text(x + 71, edge + 86, "exhaust fan lead", size=11, anchor="middle", fill=MUTED)
    d.text(bx + 20 + 3 * colw, edge + 26, "Silkscreen under each port: T · signal · +;", size=11.5,
           fill=MUTED)
    d.text(bx + 20 + 3 * colw, edge + 42, "Z-PROBE reads signal · GND · PWR.", size=11.5, fill=MUTED)

    # side panels
    nx = 770
    d.panel(nx, by, 390, 236, "After Part H")
    rows = [("FAN0", "PB7", "24 V", "exhaust 6020, Step 14.31"),
            ("FAN1", "PB3", "bare", "unused"),
            ("FAN2", "PF7", "24 V", "bay fans, Step 10.28"),
            ("FAN3", "PF9", "24 V", "filter fan, Step 10.28"),
            ("Z-PROBE", "PF1", "bare", "unused")]
    yy = by + 64
    for a, b, c, e in rows:
        d.mono(nx + 18, yy, a, size=12.3, weight=700)
        d.mono(nx + 100, yy, b, size=12.3, fill=MUTED)
        d.text(nx + 150, yy, c, size=12.3, weight=700, fill=OK if c == "24 V" else MUTED)
        d.text(nx + 198, yy, e, size=11.8, fill=MUTED)
        yy += 26
    d.text(nx + 18, yy + 14, "3 fitted · 2 bare · 5 headers", size=14, weight=700)
    d.text(nx + 18, yy + 33, "Ch 10's 'exactly two' is the machine without Part H.", size=11.5,
           fill=MUTED)

    d.panel(nx, by + 254, 390, 186, "Before power-on")
    yy = d.wrap(nx + 18, by + 254 + 60,
                "A jumper on 5 V, or a 5 V fan on 24 V, destroys the fan or the board. The exhaust "
                "fan is a 24 V part: check its label before the plug goes on.",
                size=12.3, width_chars=50, lh=18, fill=RED)
    d.wrap(nx + 18, yy + 10,
           "Red goes on the + pin, where FAN2's red already is. FAN0 here is the Leviathan's, "
           "not the toolboard's.", size=12.3, width_chars=50, lh=18, fill=INK)

    footer(d, "Header order, the T · signal · + pin labels and the 24 V-top / 5 V-bottom selection pins are read "
              "from LDO's voltageselection_V1.3 photo (MotorDynamicsLab/Leviathan @878c3c4); spacing is "
              "schematic. Read your board's silkscreen before fitting. Diagram 7 (Ch 10) shows the same five "
              "headers before this add-on.")
    return d


# ===================================================== (c) control schematic
def dc_control() -> Doc:
    d = Doc(800, "Exhaust fan control: chamber thermistor to fan")
    top = header(d, "How Klipper drives the exhaust fan",
                 "The chamber thermistor's reading drives a temperature_fan on FAN0. Each print sets a "
                 "ceiling; the fan switches on 2 °C above it and off 2 °C below it.",
                 "Ch 14, Steps 14.33 · 14.34 · 14.35 · 14.36")

    def box(x, y, w, h, title, lines, stroke=INK, fill=PANEL, mono_title=False):
        d.rect(x, y, w, h, fill=fill, stroke=stroke, sw=2.2, rx=8)
        if mono_title:
            d.mono(x + 12, y + 24, title, size=13, weight=700)
        else:
            d.text(x + 12, y + 24, title, size=14, weight=700)
        yy = y + 44
        for ln, col, mono in lines:
            if mono:
                d.mono(x + 12, yy, ln, size=11.3, weight=500, fill=col)
            else:
                d.text(x + 12, yy, ln, size=11.8, fill=col)
            yy += 16

    def arrow(x1, y1, x2, y2, col=INK):
        mk = {INK: "arw", MUTED: "arwm", ORANGE: "arwo", LEAD: "arwa"}.get(col, "arw")
        d.path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}", stroke=col, sw=2.2, marker=mk)

    # ---- signal chain, row 1 ----
    y1, h1 = top + 34, 136
    d.text(40, y1 - 10, "THE LOOP — every 0.3 s", size=12, weight=700, fill=MUTED, ls=0.6)
    box(40, y1, 214, h1, "Chamber thermistor", [
        ("on the toolhead cover", MUTED, False),
        ("CT = nhk:PB2 (Ch 08)", MUTED, False),
        ("[temperature_sensor", INK, True),
        (" chamber_temp]", INK, True),
        ("unchanged from Ch 12", MUTED, False)])
    box(280, y1, 206, h1, "Combined sensor", [
        ("sensor_type:", INK, True),
        (" temperature_combined", INK, True),
        ("sensor_list: chamber_temp", INK, True),
        ("reads the same number;", MUTED, False),
        ("nothing in Ch 12 changes", MUTED, False)])
    box(512, y1, 262, h1, "[temperature_fan exhaust_fan]", [
        ("control: watermark", INK, True),
        ("max_delta: 2.0", INK, True),
        ("target = this print's ceiling", MUTED, False),
        ("target 0 = off, whatever", MUTED, False),
        ("the temperature", MUTED, False)], stroke=ORANGE, fill=ORANGE_F, mono_title=True)
    box(802, y1, 170, h1, "Leviathan FAN0", [
        ("pin: PB7", INK, True),
        ("jumper at 24 V", MUTED, False),
        ("(Step 14.31)", MUTED, False),
        ("shutdown_speed 0", MUTED, False)])
    box(1000, y1, 160, h1, "6020 fan, 24 V", [
        ("in the housing,", MUTED, False),
        ("blows out of", MUTED, False),
        ("the bottom", MUTED, False),
        ("off or flat out", MUTED, False)])
    for xa, xb in ((254, 280), (486, 512), (774, 802), (972, 1000)):
        arrow(xa + 2, y1 + h1 / 2, xb - 4, y1 + h1 / 2)

    # ---- where the ceiling comes from, row 2 ----
    y2, h2 = y1 + h1 + 62, 120
    d.text(40, y2 - 10, "THE CEILING — set once per print", size=12, weight=700, fill=MUTED, ls=0.6)
    box(40, y2, 250, h2, "PrusaSlicer filament preset", [
        ("Chamber temperature:", INK, False),
        ("Nominal = ceiling", INK, False),
        ("Minimal = PRINT_START's wait", MUTED, False),
        ("(Step 14.35)", MUTED, False)])
    box(322, y2, 290, h2, "Printer start G-code", [
        ("PRINT_START ... CHAMBER=", INK, True),
        (" {chamber_minimal_temperature}", INK, True),
        (" EXHAUST={chamber_temperature}", INK, True),
        ("one line, Step 14.35", MUTED, False)])
    box(644, y2, 266, h2, "_EXHAUST (in PRINT_START)", [
        ("CHAMBER > 0, or EXHAUST > 45:", INK, False),
        ("a hot-chamber material, ceiling 0", INK, False),
        ("else ceiling = EXHAUST", INK, False),
        ("SET_TEMPERATURE_FAN_TARGET", MUTED, True)], stroke=ORANGE)
    box(942, y2, 218, h2, "_EXHAUST_PURGE", [
        ("in PRINT_END:", INK, False),
        ("after a vented print, flat", INK, False),
        ("out 10 min, then 0", INK, False),
        ("after ASA: 0 at once", MUTED, False)])
    arrow(292, y2 + h2 / 2, 318, y2 + h2 / 2)
    arrow(614, y2 + h2 / 2, 640, y2 + h2 / 2)
    # _EXHAUST and _EXHAUST_PURGE both set the fan's target
    d.path(f"M{777:.1f},{y2:.1f} L{650 + 0:.1f},{y1 + h1 + 4:.1f}", stroke=ORANGE, sw=2.2, marker="arwo")
    d.path(f"M{1051:.1f},{y2:.1f} L{700:.1f},{y1 + h1 + 4:.1f}", stroke=ORANGE, sw=2.2, marker="arwo",
           dash="6 4")
    d.text(905, y1 + h1 + 32, "sets target", size=11.5, fill=ORANGE, weight=600)

    # ---- per-material bands ----
    y3 = y2 + h2 + 56
    d.text(40, y3 - 14, "PER MATERIAL — chamber_temp scale", size=12, weight=700, fill=MUTED, ls=0.6)
    sx0, sx1, t0, t1 = 250, 1150, 25.0, 60.0
    def X(t): return sx0 + (t - t0) / (t1 - t0) * (sx1 - sx0)
    rows = [("PLA", 35, "ceiling 35 °C"), ("PETG", 40, "ceiling 40 °C"), ("ASA", None, "unvented")]
    rh, gap = 30, 14
    for i, (mat, c, lab) in enumerate(rows):
        y = y3 + i * (rh + gap)
        d.text(40, y + 20, mat, size=15, weight=700)
        d.text(110, y + 20, lab, size=12.3, fill=MUTED)
        if c is None:
            d.rect(X(t0), y, X(t1) - X(t0), rh, fill=GREY_F, stroke=GREY, sw=1.4, rx=4)
            d.text(X(t0) + 12, y + 20, "target 0: the fan never runs. The chamber soaks closed at "
                   "50–60 °C and the Nevermore filters, as before Part H.", size=12, fill=INK)
            continue
        d.rect(X(t0), y, X(c - 2) - X(t0), rh, fill=GREY_F, stroke=GREY, sw=1.4, rx=4)
        d.rect(X(c - 2), y, X(c + 2) - X(c - 2), rh, fill=AMBER_F, stroke=AMBER, sw=1.4)
        d.rect(X(c + 2), y, X(t1) - X(c + 2), rh, fill=LEAD_F, stroke=LEAD, sw=1.4, rx=4)
        d.line(X(c), y - 4, X(c), y + rh + 4, stroke=ORANGE, sw=2.6)
        d.text(X(t0) + 10, y + 20, f"off below {c - 2}", size=11.5, fill=MUTED)
        d.text(X(c - 2) + (X(c + 2) - X(c - 2)) / 2, y + 20, "keeps state", size=10.5,
               anchor="middle", fill=AMBER, weight=600)
        d.text(X(c + 2) + 10, y + 20, f"flat out from {c + 2}", size=11.5, fill=LEAD, weight=600)
    # scale ticks
    ys = y3 + 3 * (rh + gap) + 4
    d.line(X(t0), ys, X(t1), ys, stroke=MUTED, sw=1.4)
    t = t0
    while t <= t1 + 0.01:
        d.line(X(t), ys - 4, X(t), ys + 4, stroke=MUTED, sw=1.4)
        d.text(X(t), ys + 19, f"{t:.0f} °C", size=11, anchor="middle", fill=MUTED)
        t += 5

    footer(d, "Watermark, not PID: Klipper has no PID_CALIBRATE for a temperature_fan, and its PID floors the fan "
              "at min_speed whenever a target is set. The sensor rides on the toolhead and reads a little warm, "
              "so the chamber itself sits a little under the ceiling. Full block: Step 14.33; tested offline in "
              "review/2026-10-03-exhaust/test_macros.py.")
    return d


# ============================================================ print-set sheet
def parts_sheet(out_path: Path) -> None:
    """The four Part H prints + the reused grill, in their print colours, from the
    fetched STLs (slicer/fetch_stls.py). Reuses render_parts.py's renderer."""
    import render_parts as RP
    import matplotlib.pyplot as plt
    stl = RP.STL_DIR / "voron2" / "STLs" / "Exhaust_Filter"
    items = [("exhaust_filter_housing.stl", RP.COLOUR_PRIMARY, "Galaxy Black · job 1"),
             ("[a]_exhaust_fan_grill.stl", RP.COLOUR_ACCENT, "blue accent · job 2"),
             ("[a]_filter_access_cover.stl", RP.COLOUR_ACCENT, "blue accent · job 2"),
             ("[a]_exhaust_filter_mount_x2.stl", RP.COLOUR_ACCENT, "blue accent ×2 · job 2"),
             ("exhaust_filter_grill.stl", "#b9b9b9", "already fitted at 11.54 · reused")]
    fig = plt.figure(figsize=(5 * 2.4, 1 * 2.4), dpi=200)
    fig.patch.set_facecolor(RP.BACKGROUND)
    for i, (name, col, note) in enumerate(items):
        ax = fig.add_subplot(1, 5, i + 1, projection="3d")
        RP._setup_axes(ax)
        RP._draw_part(ax, RP.load_mesh(stl / name), col)
        ax.text2D(0.5, -0.02, name, fontsize=5.2, ha="center", transform=ax.transAxes, color="#222222")
        ax.text2D(0.5, -0.09, note, fontsize=5.2, ha="center", transform=ax.transAxes, color="#555555")
    fig.suptitle("Ch 14 Part H add-on prints (Voron-2 STLs/Exhaust_Filter @a192410, GPL-3.0)", fontsize=8)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.12, wspace=0.05)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, facecolor=RP.BACKGROUND)
    plt.close(fig)


DIAGRAMS = [("exhaust-a-lead-route.svg", da_lead_route),
            ("exhaust-b-jumpers.svg", db_jumpers),
            ("exhaust-c-control.svg", dc_control)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--parts-sheet", action="store_true",
                    help="also render docs/manual/assets/parts/sheet-addon-exhaust.png")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    for name, fn in DIAGRAMS:
        doc = fn()
        p = a.out / name
        p.write_text(doc.render(), encoding="utf-8")
        print(f"  {p}  {doc.w}x{doc.h}  {p.stat().st_size / 1024:.1f} kB")
    if a.parts_sheet:
        p = D.REPO / "docs" / "manual" / "assets" / "parts" / "sheet-addon-exhaust.png"
        parts_sheet(p)
        print(f"  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
