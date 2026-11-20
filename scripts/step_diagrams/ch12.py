"""Chapter 12 (software) step-column diagrams, 1201 onwards.

Geometry sources: LDO's Rev D finished-bay and general-placement photos
(LDOVoron2 Images/WiringGuide/RevD/VS9, S0General_Placement), the Leviathan repo photos at
878c3c4 (frontsw1sw2.jpg, frontsw1sw2_V1.3.jpg, rpi4_installed_V1.3.jpg), LDO's Nitehawk-SB V2
button/LED photo (reset_boot_buttons.jpg), the LDO Leviathan V1.2 / V1.3 guides (fetched
2026-11-20) and the chapter's own config text. Proportions are schematic; sides, order and
every label follow the sources.

Bay positions are read off LDO's photo of the bay seen from below, front edge up, as fractions
(u across, machine left = 0; v down, front = 0). For the machine on its side they are turned so
the floor is the machine's right side: the rear is on the left and the front on the right.
"""
import draw_diagrams as dd
from draw_diagrams import (AMBER, AMBER_F, BLACKPART, BLACKPART_F, BLUE, BLUE_F, GREY, GREY_F,
                           INK, MONO, MUTED, OK, OK_F, ORANGE, ORANGE_F, PANEL, RED, RULE, STEEL,
                           Doc, T_LAB, T_MIN, callout, label_bg, step_header)

PCB = "#262B31"
PCB_EDGE = "#11151A"
RED_F = "#F6D5D1"
PI_GREEN = "#2F8F4E"
PI_GREEN_F = "#D7EEDD"


# ------------------------------------------------------------------ helpers ---
def bench_tag(d: Doc, x, y, s, anchor="start", size=T_MIN):
    """An amber chip for a fact that is checked on the bench."""
    w = len(s) * size * 0.56 + 24
    x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
    d.rect(x0, y - size * 0.95, w, size * 1.4, fill=AMBER_F, stroke=AMBER, sw=2.5, rx=8)
    d.text(x0 + w / 2, y + size * 0.05, s, size=size, anchor="middle", weight=700, fill=INK)


def cross(d: Doc, x, y, r=22, sw=7):
    d.line(x - r, y - r, x + r, y + r, stroke=RED, sw=sw)
    d.line(x - r, y + r, x + r, y - r, stroke=RED, sw=sw)


def arrow(d: Doc, x0, y0, x1, y1, col=INK, sw=6, mk="arw", dash=None):
    d.path(f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}", stroke=col, sw=sw, marker=mk, dash=dash)


def led(d: Doc, x, y, col, r=11):
    d.circle(x, y, r + 7, fill=col, stroke="none", sw=0)
    d.circle(x, y, r, fill="#FFFFFF", stroke=col, sw=4)


# Bay parts as (u0, u1, v0, v1) fractions of LDO's from-below photo (front edge up).
BAY = {
    "frame": (0.057, 0.947, 0.057, 0.947),
    "screen": (0.40, 0.60, 0.035, 0.125),
    "board": (0.28, 0.567, 0.33, 0.50),
    "pi": (0.235, 0.42, 0.336, 0.44),
    "chip": (0.44, 0.48, 0.385, 0.425),
    "usb": (0.64, 0.71, 0.36, 0.45),
    "front_rail": (0.21, 0.78, 0.405, 0.435),
    "duct_front": (0.23, 0.77, 0.26, 0.29),
    "duct_mid": (0.23, 0.77, 0.50, 0.53),
    "duct_rear": (0.23, 0.77, 0.815, 0.84),
    "rear_rail": (0.23, 0.45, 0.61, 0.65),
    "ssr": (0.28, 0.35, 0.56, 0.69),
    "psu": (0.45, 0.81, 0.54, 0.735),
    "psu_term": (0.45, 0.475, 0.545, 0.73),
    "wago": (0.26, 0.41, 0.84, 0.875),
    "inlet": (0.20, 0.32, 0.875, 0.947),
}


class Bay:
    """Maps the photo fractions onto the drawing: machine on its right side, bay toward you."""

    def __init__(self, x0, y0, s):
        self.x0, self.y0, self.s = x0, y0, s

    def pt(self, u, v):
        return self.x0 + (1 - v) * self.s, self.y0 + u * self.s

    def box(self, key):
        u0, u1, v0, v1 = BAY[key]
        xa, ya = self.pt(u0, v1)
        xb, yb = self.pt(u1, v0)
        return xa, ya, xb - xa, yb - ya

    def draw(self, d: Doc, k=1.0, highlight_board=False):
        s = self.s
        fx, fy, fw, fh = self.box("frame")
        d.rect(fx, fy, fw, fh, fill=BLACKPART_F, stroke=BLUE, sw=10 * k, rx=6)
        d.rect(fx + 0.07 * s, fy + 0.07 * s, fw - 0.14 * s, fh - 0.14 * s, fill="#ECEDEF",
               stroke=BLUE, sw=3 * k)
        for key in ("duct_front", "duct_mid", "duct_rear"):
            d.rect(*self.box(key), fill=PANEL, stroke=FAINT_DUCT, sw=2 * k)
        for key in ("front_rail", "rear_rail"):
            d.rect(*self.box(key), fill=STEEL, stroke=GREY, sw=2 * k)
        x, y, w, h = self.box("screen")
        d.rect(x, y, w, h, fill=PCB, stroke=INK, sw=2 * k, rx=4)
        bx, by, bw, bh = self.box("board")
        d.rect(bx, by, bw, bh, fill=PCB, stroke=ORANGE if highlight_board else PCB_EDGE,
               sw=(6 if highlight_board else 2) * k, rx=6)
        d.rect(*self.box("pi"), fill=PI_GREEN_F, stroke=PI_GREEN, sw=3 * k, rx=4)
        d.rect(*self.box("chip"), fill="#4A5059", stroke=INK, sw=2 * k)
        d.rect(*self.box("usb"), fill=PCB, stroke=PCB_EDGE, sw=2 * k, rx=3)
        # mains parts in red: SSR, the PSU's terminal block, inlet and WAGO blocks
        d.rect(*self.box("psu"), fill=GREY_F, stroke=GREY, sw=3 * k, rx=4)
        for key in ("ssr", "psu_term", "wago", "inlet"):
            d.rect(*self.box(key), fill=RED_F, stroke=RED, sw=4 * k, rx=4)


FAINT_DUCT = "#B9C0C9"


def pointer(d: Doc, x1, y1, x2, y2, col):
    """A leader thick enough to follow at 480 px: dot on the part, line to the label."""
    d.line(x1, y1, x2, y2, stroke=col, sw=3)
    d.circle(x1, y1, 5, fill=col, stroke="none", sw=0)


def down_arrow(d: Doc, x, y0, y1, col_top, col, sw=8):
    """A vertical arrow with its own head, so any colour works."""
    d.line(x, y0, x, y1 - 26, stroke=col, sw=sw)
    d.circle(x, y0, 8, fill=col_top, stroke="none", sw=0)
    d.poly([(x - 18, y1 - 30), (x + 18, y1 - 30), (x, y1)], fill=col, stroke=col, sw=1)


def floor(d: Doc, y, x0, x1):
    d.line(x0, y, x1, y, stroke=INK, sw=4)
    for x in range(int(x0) + 10, int(x1), 34):
        d.line(x, y + 4, x - 16, y + 22, stroke=MUTED, sw=2)


# ============================================================ diagram 1201 ===
def d1201_power_on_stance() -> Doc:
    d = Doc(1070, "Power-on: stand to the side, hand on the rocker, watch these")
    top = step_header(d, "Power on: where to stand and look")
    d.panel(30, top + 16, 1140, d.h - top - 32)

    s = 580
    bay = Bay(575, 420, s)                       # bay square: x 575-1155, y 420-1000
    fl = bay.y0 + 0.947 * s + 8                  # machine resting on its right side
    floor(d, fl, 50, 1160)
    bay.draw(d)

    # rocker: on the inlet's outer face, pointing out of the rear (left)
    ix, iy, iw, ih = bay.box("inlet")
    rx, ry = bay.x0 + 0.053 * s - 6, iy + ih / 2
    d.rect(rx - 30, ry - 26, 30, 52, fill=RED_F, stroke=RED, sw=4, rx=6)
    d.rect(rx - 44, ry - 18, 16, 36, fill=OK, stroke=INK, sw=2, rx=4)

    # cord: inlet down to the floor and away left to the wall socket
    d.path(f"M {rx - 10} {ry + 30} C {rx - 40} {ry + 160} {rx - 30} {fl - 10} {rx - 140} "
           f"{fl - 8} L 70 {fl - 8} L 70 {fl - 120}", stroke=INK, sw=7)
    d.rect(52, fl - 190, 44, 70, fill=PANEL, stroke=INK, sw=3, rx=6)
    callout(d, 140, fl - 150, 2)

    # the adult, to the side of the machine (not in front of the bay), not to scale
    px, head_y = 300, 290
    d.circle(px, head_y, 42, fill=PANEL, stroke=INK, sw=6)
    sh_y = head_y + 70
    d.line(px, head_y + 42, px, fl - 280, stroke=INK, sw=10)         # body
    d.line(px, fl - 280, px - 50, fl - 4, stroke=INK, sw=10)          # legs
    d.line(px, fl - 280, px + 40, fl - 4, stroke=INK, sw=10)
    d.line(px, sh_y, px - 60, sh_y + 170, stroke=INK, sw=10)          # other arm, down
    hx, hy = rx - 54, ry - 4                                          # hand on the rocker
    d.path(f"M {px} {sh_y} L {px + 110} {sh_y + 100} L {hx} {hy}", stroke=INK, sw=10)
    d.circle(hx, hy, 15, fill=INK, stroke=INK, sw=1)
    callout(d, hx - 30, hy - 74, 3)
    d.text(px - 20, fl + 52, "stand to the side", size=T_LAB, anchor="middle", weight=700)

    # where to look (green = should light)
    psu_led = bay.pt(0.46, 0.556)
    led(d, *psu_led, OK)
    pi_led = bay.pt(0.40, 0.345)
    led(d, *pi_led, RED, r=9)
    led(d, pi_led[0], pi_led[1] + 26, OK, r=9)
    sx, sy, sw_, sh = bay.box("screen")
    d.rect(sx - 6, sy - 6, sw_ + 12, sh + 12, fill="none", stroke=OK, sw=5, rx=6)

    d.text(575, 340, "PSU LED: green", size=T_LAB, weight=700, fill=OK)
    pointer(d, psu_led[0] - 8, psu_led[1] - 22, 700, 352, OK)
    d.text(1150, 210, "Pi: red PWR,", size=T_LAB, anchor="end", weight=700)
    d.text(1150, 248, "green ACT flickers", size=T_LAB, anchor="end", weight=700)
    pointer(d, pi_led[0], pi_led[1] - 22, pi_led[0], 260, INK)
    d.text(1150, 330, "screen lights", size=T_LAB, anchor="end", weight=700, fill=OK)
    pointer(d, sx + sw_ / 2, sy - 10, sx + sw_ / 2, 342, OK)

    # toolboard LEDs live on the printhead, not in the bay
    tx, ty = 50, 116
    d.rect(tx, ty, 250, 120, fill=PCB, stroke=PCB_EDGE, sw=2, rx=10)
    for i, col in enumerate((OK, OK, GREY, GREY, GREY)):
        led(d, tx + 38 + i * 44, ty + 84, col, r=8)
    d.text(tx + 125, ty + 44, "printhead", size=T_MIN, anchor="middle", weight=700,
           fill="#FFFFFF")
    d.text(tx + 270, ty + 96, "3V3, 24V lit", size=T_LAB, weight=700, fill=OK)

    d.text(bay.x0 + 0.5 * s, fl + 52, "red: mains, eyes only", size=T_LAB, anchor="middle",
           weight=700, fill=RED)
    d.text(bay.x0 + 0.06 * s, bay.y0 + 0.04 * s, "REAR", size=T_MIN, weight=800, fill=BLUE)
    d.text(bay.x0 + 0.94 * s, bay.y0 + 0.04 * s, "FRONT", size=T_MIN, weight=800, fill=BLUE,
           anchor="end")
    return d


# ============================================================ diagram 1202 ===
def d1202_sw1_reach() -> Doc:
    # landscape: 12.15 renders stacked, the picture capped at 40vh
    d = Doc(700, "Leviathan SW1 and SW2: where they are and how to reach them")
    top = step_header(d, "SW1 and SW2: reach from above")

    # left: the whole bay, the reach path and the line not to pass
    d.panel(30, top + 14, 570, d.h - top - 30)
    s = 420
    bay = Bay(110, top + 100, s)
    bay.draw(d, k=0.7, highlight_board=True)
    sw1 = bay.pt(0.455, 0.443)
    d.circle(*sw1, 9, fill=ORANGE, stroke=PANEL, sw=2)
    arrow(d, sw1[0], top + 40, sw1[0], sw1[1] - 26, col=OK, sw=8, mk="arwg")
    d.text(sw1[0] - 16, top + 66, "reach in from above", size=T_LAB, anchor="end", weight=700,
           fill=OK)
    # the line not to pass: the front edge of the PSU and SSR, at the middle duct
    rx = bay.pt(0, 0.535)[0]
    d.line(rx, bay.y0 + 0.05 * s, rx, bay.y0 + 0.97 * s + 20, stroke=RED, sw=6, dash="18 12")
    d.text(rx + 10, d.h - 66, "never past the red line:", size=T_MIN, anchor="middle",
           weight=700, fill=RED)
    d.text(rx + 10, d.h - 30, "PSU, SSR, mains WAGOs", size=T_MIN, anchor="middle",
           weight=700, fill=RED)
    d.text(bay.x0 + 0.06 * s, bay.y0 + 0.04 * s, "REAR", size=T_MIN, weight=800, fill=BLUE)
    d.text(bay.x0 + 0.94 * s, bay.y0 + 0.04 * s, "FRONT", size=T_MIN, weight=800, fill=BLUE,
           anchor="end")

    # right: the buttons beside the processor, same orientation, close up
    ox = 620
    d.panel(ox, top + 14, 550, d.h - top - 30)
    d.text(ox + 20, top + 60, "Close up", size=T_MIN, weight=700, fill=MUTED)
    by0, by1 = top + 84, d.h - 34
    d.rect(ox + 16, by0, 518, by1 - by0, fill=PCB, stroke=PCB_EDGE, sw=3, rx=12)
    # heatsink (rear side), J9 with the Pi's power lead, the buttons, the processor (front side)
    d.rect(ox + 30, by0 + 20, 50, by1 - by0 - 40, fill="#3A4048", stroke=INK, sw=2)
    for i in range(3):
        d.line(ox + 42 + i * 13, by0 + 30, ox + 42 + i * 13, by1 - 30, stroke="#20252B", sw=4)
    jx = ox + 130
    d.rect(jx, by0 + 150, 44, 230, fill="#F2F2F2", stroke=GREY, sw=3, rx=4)
    for i in range(6):
        d.path(f"M {jx + 8} {by0 + 168 + i * 38} C {jx - 30} {by0 + 168 + i * 38} "
               f"{jx - 24 + i * 5} {by0 + 90} {jx - 16 + i * 8} {by0 + 4}", stroke="#111",
               sw=7)
    d.text(jx + 50, by0 + 40, "Pi lead", size=T_MIN, weight=700, fill="#FFFFFF")
    bxs = ox + 270
    for (yy, name, sub) in ((by0 + 150, "SW1", "RESET"), (by0 + 360, "SW2", "BOOT")):
        d.rect(bxs - 36, yy - 36, 72, 72, fill=STEEL, stroke=GREY, sw=3, rx=8)
        d.circle(bxs, yy, 20, fill="#E6E6E6", stroke=INK, sw=3)
        d.text(bxs + 52, yy - 2, name, size=40, weight=800, fill=ORANGE)
        d.text(bxs + 52, yy + 34, sub, size=T_MIN, weight=700, fill="#FFFFFF")
    d.rect(ox + 420, by0 + 200, 100, 120, fill="#4A5059", stroke=INK, sw=3)
    d.text(ox + 470, by0 + 268, "chip", size=T_MIN, anchor="middle", weight=700,
           fill="#FFFFFF")
    return d


# ============================================================ diagram 1203 ===
def d1203_board_markings() -> Doc:
    d = Doc(1060, "Where the Leviathan says which version it is")
    top = step_header(d, "Which Leviathan: read the chip")
    # board as LDO photographs it (stepper sockets along the top), 1215 x 730 photo px
    k = 0.86
    ox, oy = 78, top + 70

    def P(u, v):
        return ox + u * 1215 * k, oy + v * 730 * k
    W, H = 1215 * k, 730 * k
    d.rect(ox, oy, W, H, fill=PCB, stroke=PCB_EDGE, sw=3, rx=16)
    for i in range(7):                                         # motor sockets
        x = ox + 70 + i * 140
        d.rect(x, oy + 12, 74, 34, fill="#F2F2F2", stroke=GREY, sw=2, rx=3)
    d.rect(*P(0.05, 0.22), 0.55 * W, 0.07 * H, fill="#3A4048", stroke=INK, sw=2)
    tx, ty = P(0.02, 0.33)
    d.rect(tx, ty, 0.06 * W, 0.30 * H, fill="#3A4048", stroke=INK, sw=2)
    for i in range(6):
        d.circle(tx + 0.03 * W, ty + 16 + i * 0.30 * H / 6.4, 11, fill=STEEL, stroke=GREY, sw=2)
    # processor
    cx0, cy0 = P(0.325, 0.45)
    cw, ch = 0.15 * W, 0.20 * H
    d.rect(cx0, cy0, cw, ch, fill="#4A5059", stroke=ORANGE, sw=5)
    d.text(cx0 + cw / 2, cy0 + ch / 2 + 10, "STM32…", size=T_MIN, anchor="middle",
           weight=700, fill="#FFFFFF")
    # the two buttons above it
    for u in (0.366, 0.432):
        x, y = P(u, 0.42)
        d.circle(x, y - 6, 10, fill=STEEL, stroke=GREY, sw=2)
    # revision text spot, under the Pi
    rx, ry = P(0.55, 0.88)
    d.text(rx, ry - 30, "VORON", size=T_LAB, weight=800, fill="#FFFFFF")
    d.text(rx, ry + 6, "Leviathan V1.x", size=T_MIN, weight=700, fill="#FFFFFF")
    # the Pi, drawn see-through, as mounted in Ch 09
    px0, py0 = P(0.50, 0.33)
    px1, py1 = P(1.0, 0.92)
    d.rect(px0, py0, px1 - px0, py1 - py0, fill=PI_GREEN_F, stroke=PI_GREEN, sw=5, rx=10,
           dash="16 10", op=0.55)
    d.text((px0 + px1) / 2 + 30, py0 + 70, "the Pi covers it", size=T_LAB, anchor="middle",
           weight=700, fill=PI_GREEN)

    # labels under the board
    ly = oy + H + 70
    pointer(d, cx0 + cw / 2, cy0 + ch + 6, 250, ly - 36, ORANGE)
    d.text(60, ly, "Read the chip:", size=T_LAB, weight=700, fill=ORANGE)
    d.mono(60, ly + 50, "STM32F446…", size=34, weight=700)
    d.text(330, ly + 50, "= V1.1 or V1.2", size=T_LAB, weight=600)
    d.mono(60, ly + 96, "STM32H743…", size=34, weight=700)
    d.text(330, ly + 96, "= V1.3", size=T_LAB, weight=600)
    pointer(d, rx + 120, ry + 16, 900, ly - 36, MUTED)
    d.text(1140, ly, "Version line:", size=T_LAB, anchor="end", weight=700, fill=MUTED)
    d.text(1140, ly + 50, "hidden once the", size=T_LAB, anchor="end", weight=600, fill=MUTED)
    d.text(1140, ly + 96, "Pi is mounted", size=T_LAB, anchor="end", weight=600, fill=MUTED)
    return d


# ============================================================ diagram 1204 ===
def d1204_serial_paths() -> Doc:
    # landscape: 12.23 renders stacked, the picture capped at 40vh
    d = Doc(700, "Which serial line goes into [mcu] and which into [mcu nhk]")
    top = step_header(d, "Which line goes where")
    ms = 30                                         # mono size, ~18 units a character

    # the terminal output
    y0 = top + 24
    d.rect(40, y0, 1120, 210, fill=PCB, stroke=PCB_EDGE, sw=3, rx=12)
    d.mono(70, y0 + 50, "$ ls /dev/serial/by-id/", size=ms, fill="#C9D1D9")
    l1, l2 = y0 + 112, y0 + 172
    for yy, chip, col, who in ((l1, "stm32f446xx", "#8CC4FF", "mainboard"),
                               (l2, "stm32g0b1xx", "#FFB27A", "toolboard")):
        d.mono(70, yy, "usb-Klipper_", size=ms, fill="#FFFFFF")
        d.mono(70 + 12 * 18, yy, chip, size=ms, weight=800, fill=col)
        d.mono(70 + 23 * 18, yy, "_<id>-if00", size=ms, fill="#FFFFFF")
        d.text(720, yy, who, size=T_LAB, weight=700, fill=col)

    # the two config sections, side by side
    by, bh, bw = y0 + 290, 270, 545
    for i, (sec, chip, col, colf, note, x_arrow, y_from, top_col) in enumerate((
            ("[mcu nhk]", "stm32g0b1xx", ORANGE, ORANGE_F, "never rp2040", 300, l2,
             "#FFB27A"),
            ("[mcu]", "stm32f446xx", BLUE, BLUE_F, "or stm32h743xx: V1.3", 1000, l1,
             "#8CC4FF"))):
        x = 40 + i * (bw + 30)
        d.rect(x, by, bw, bh, fill=colf, stroke=col, sw=4, rx=12)
        d.mono(x + 26, by + 52, sec, size=34, weight=800, fill=col)
        d.mono(x + 26, by + 104, "serial: …/by-id/", size=ms)
        d.mono(x + 56, by + 150, "usb-Klipper_", size=ms)
        d.mono(x + 56, by + 196, chip + "_…", size=ms, weight=800, fill=col)
        d.text(x + 26, by + 246, note, size=T_MIN, weight=700, fill=MUTED)
        down_arrow(d, x_arrow, y_from + 14, by - 4, top_col, col)
    return d


# ============================================================ diagram 1205 ===
LEV_COMMON_TOP = [
    "[*] Enable extra low-level configuration options",
    "    Micro-controller Architecture: STMicroelectronics STM32",
]
LEV_ROWS = [
    ("Processor model", "STM32F446", "STM32H743"),
    ("Bootloader offset", "32KiB bootloader", "128KiB bootloader"),
    ("Clock Reference", "12 MHz crystal", "25 MHz crystal"),
]


def d1205_menuconfig_card() -> Doc:
    # landscape: 12.14 renders stacked, the picture capped at 40vh
    d = Doc(660, "Leviathan make menuconfig settings: F446 and H743")
    top = step_header(d, "Leviathan menuconfig")
    ms = 30
    d.rect(40, top + 20, 1120, 200, fill=GREY_F, stroke=GREY, sw=3, rx=12)
    d.text(64, top + 62, "Both boards, the tick first:", size=T_LAB, weight=700)
    d.mono(64, top + 110, LEV_COMMON_TOP[0], size=ms, weight=700)
    d.mono(64, top + 154, "Micro-controller Architecture: STMicroelectronics STM32", size=ms)
    d.mono(64, top + 198, "Communication interface: USB (on PA11/PA12)", size=ms)

    # the three lines that differ, one column per board
    ty = top + 244
    c0, c1, c2 = 40, 470, 820
    d.rect(c1 - 10, ty, 340, 62, fill=BLUE_F, stroke=BLUE, sw=3, rx=8)
    d.rect(c2 - 10, ty, 340, 62, fill=ORANGE_F, stroke=ORANGE, sw=3, rx=8)
    d.text(c1 + 160, ty + 42, "F446: V1.1, V1.2", size=T_LAB, anchor="middle", weight=800,
           fill=BLUE)
    d.text(c2 + 160, ty + 42, "H743: V1.3", size=T_LAB, anchor="middle", weight=800,
           fill=ORANGE)
    ry = ty + 116
    for i, (lab, f, h) in enumerate(LEV_ROWS):
        yy = ry + i * 70
        if i:
            d.line(c0, yy - 44, 1160, yy - 44, stroke=RULE, sw=2)
        d.text(c0 + 24, yy, lab, size=T_LAB, weight=700)
        d.mono(c1, yy, f, size=ms, weight=700, fill=BLUE)
        d.mono(c2, yy, h, size=ms, weight=700, fill=ORANGE)
    return d


# ============================================================ diagram 1206 ===
def d1206_safe_z_home() -> Doc:
    # landscape: 12.33 renders stacked, the picture capped at 40vh
    d = Doc(700, "Why -10,-10 is outside travel, and where the nozzle-probe pin is")
    top = step_header(d, "Why -10,-10 cannot be reached")
    k = 1.2                                         # px per mm
    X0, Y0 = 200, top + 64 + 350 * k                # machine X0,Y0 (front left) on the page

    def P(x, y):
        return X0 + x * k, Y0 - y * k
    a, b = P(0, 350), P(350, 0)
    d.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=OK_F, stroke=OK, sw=5)
    d.text(*P(175, 270), "travel", size=36, anchor="middle", weight=800, fill=OK)
    d.text(*P(175, 238), "X and Y: 0 to 350", size=T_LAB, anchor="middle", weight=700,
           fill=OK)
    x, y = P(0, 0)
    d.text(x + 14, y - 16, "0,0", size=T_LAB, weight=700)
    x, y = P(350, 350)
    d.text(x, y - 18, "350,350", size=T_LAB, anchor="middle", weight=700)
    x, y = P(175, 0)
    d.text(x, y + 44, "FRONT", size=T_LAB, anchor="middle", weight=800, fill=BLUE)

    # the shipped -10,-10: outside, refused (offset drawn larger than scale)
    x, y = X0 - 34, Y0 + 34
    cross(d, x, y, r=18, sw=7)
    d.text(x - 30, y - 120, "-10,-10:", size=T_LAB, anchor="end", weight=800, fill=RED)
    d.text(x - 30, y - 80, "outside,", size=T_LAB, anchor="end", weight=700, fill=RED)
    d.text(x - 30, y - 40, "refused", size=T_LAB, anchor="end", weight=700, fill=RED)

    # the nozzle-probe pin: right bed extrusion, just behind the plate
    x, y = P(232, 343)
    d.circle(x, y, 16, fill=ORANGE, stroke=INK, sw=3)
    pointer(d, x + 14, y + 6, 735, top + 120, INK)
    d.text(745, top + 120, "nozzle-probe pin,", size=T_LAB, weight=700)
    d.text(745, top + 160, "about here", size=T_LAB, weight=700)
    bench_tag(d, 745, top + 220, "measured in Ch 13")

    # the plausible guess: bed centre, small and in red
    x, y = P(175, 175)
    cross(d, x, y, r=12, sw=5)
    pointer(d, x + 16, y + 6, 735, top + 380, RED)
    for i, ln in enumerate(("a guess such as", "the centre: no pin", "there, the nozzle",
                            "hits the plate")):
        d.text(745, top + 380 + i * 40, ln, size=T_MIN, weight=700, fill=RED)
    return d


# ================================================================= registry ===
DIAGRAMS = [
    {
        "n": 1201,
        "file": "1201-power-on-stance.svg",
        "title": "Power on: where to stand and look",
        "fn": d1201_power_on_stance,
        "shows": [
            "The machine on its side with the bay toward you, the adult standing to the side "
            "at the rear (inlet) end with one hand on the rocker and the other down, the cord "
            "from the inlet to the wall.",
            "Mains parts in red (inlet, WAGO blocks, SSR, the PSU's terminal block); where to "
            "look: PSU LED, the Pi's red PWR and green ACT, the touchscreen, and the "
            "printhead's 3V3 and 24V LEDs.",
            "Callouts 2 and 3 are the Do numbers of Step 12.11.",
        ],
        "insert": [
            ("12-software.md", "Step 12.11", "first image: what the hands do"),
        ],
        "verify": [
            "Which side the machine lies on is not stated in Ch 10 or Ch 12; it is drawn on "
            "its right side, which puts the rear-left inlet and its rocker uppermost.",
            "Bay positions are read off LDO's Rev D finished-bay photo (a Rev D bay, PVC "
            "ducts; this build uses printed B11 conduits) and turned to that orientation. The "
            "person is not to scale.",
            "The Pi LED position (the Pi's short edge away from its USB ports) is from the "
            "Raspberry Pi 4 photo; on the bench the DSI ribbon runs close by.",
        ],
    },
    {
        "n": 1202,
        "file": "1202-leviathan-sw1-sw2.svg",
        "title": "SW1 and SW2: reach from above",
        "fn": d1202_sw1_reach,
        "shows": [
            "Left: the bay in 1201's orientation with the Leviathan outlined, a green reach "
            "path from above straight down to SW1, and a red dashed line at the front edge of "
            "the PSU and SSR (the middle duct) not to be passed.",
            "Right: a close-up in the same orientation: heatsink at the rear, J9 with the Pi's "
            "power lead, SW1 RESET above SW2 BOOT, the processor on the front side.",
        ],
        "insert": [
            ("12-software.md", "Step 12.15", "first image: where the hand goes"),
            ("12-software.md", "Step 12.16", "the same buttons for the DFU press"),
        ],
        "verify": [
            "Button order and side follow LDO's frontsw1sw2.jpg (SW2 Boot left of SW1 Reset "
            "above the processor) turned 180° as the board sits in LDO's Rev D bay photo, then "
            "90° for the machine on its right side.",
            "In LDO's rpi4_installed_V1.3 photo the J9 Pi power lead runs over the buttons; in "
            "the Rev D bay photo it does not. Where it runs on this build is a bench fact.",
            "The reach direction assumes the machine lies on its right side, as in 1201.",
        ],
    },
    {
        "n": 1203,
        "file": "1203-leviathan-chip-marking.svg",
        "title": "Which Leviathan: read the chip",
        "fn": d1203_board_markings,
        "shows": [
            "The Leviathan as LDO photographs it, stepper sockets along the top: the processor "
            "with SW2 and SW1 above it, and the VORON / Leviathan V1.x line at the lower right, "
            "under the Pi drawn see-through as mounted in Ch 09.",
            "STM32F446… = V1.1 or V1.2; STM32H743… = V1.3.",
        ],
        "insert": [
            ("12-software.md", "Step 12.13", "first image: where to look"),
        ],
        "verify": [
            "Chip marking and version text positions from LDO's frontsw1sw2.jpg and "
            "frontsw1sw2_V1.3.jpg (STM32F446ZET6, STM32H743ZIT6); the Pi's footprint from "
            "rpi4_installed_V1.3.jpg and LDO's Rev D bay photo, both of which hide the version "
            "line under the Pi.",
            "In the bay the board is turned (see 1202); the drawing keeps LDO's photo "
            "orientation so the chip text reads the right way up.",
        ],
    },
    {
        "n": 1204,
        "file": "1204-serial-paths.svg",
        "title": "Which line goes where",
        "fn": d1204_serial_paths,
        "shows": [
            "ls /dev/serial/by-id/ output with two usb-Klipper_ lines: the stm32g0b1xx one "
            "(toolboard) arrowed into the [mcu nhk] box on the left, the stm32f446xx one "
            "(mainboard) into the [mcu] box on the right; landscape, because 12.23 renders "
            "stacked with the picture capped at 40vh.",
        ],
        "insert": [
            ("12-software.md", "Step 12.23", "first image"),
        ],
        "verify": [
            "Strings follow the chapter's own code (12.12 table, 12.23 config). The order of "
            "the two lines in a real listing is not fixed; the step says to match by chip "
            "family, not order.",
        ],
    },
    {
        "n": 1205,
        "file": "1205-leviathan-menuconfig.svg",
        "title": "Leviathan menuconfig",
        "fn": d1205_menuconfig_card,
        "shows": [
            "A settings card: the low-level tick, Micro-controller Architecture and "
            "Communication interface for both boards, then Processor model, Bootloader offset "
            "and Clock Reference side by side for F446 (V1.1, V1.2) and H743 (V1.3).",
        ],
        "insert": [
            ("12-software.md", "Step 12.14", "first image: the settings in the code blocks"),
        ],
        "verify": [
            "Values are the step's own code fences, character for character; they match LDO's "
            "Leviathan V1.2 and V1.3 guides (fetched 2026-11-20). LDO writes "
            "'Microcontroller Architecture'; Klipper's menu, and the step, write "
            "'Micro-controller'. The screen layout is a card, not a screenshot.",
        ],
    },
    {
        "n": 1206,
        "file": "1206-safe-z-home.svg",
        "title": "Why -10,-10 cannot be reached",
        "fn": d1206_safe_z_home,
        "shows": [
            "Top view, front at the bottom: the travel square 0 to 350 in X and Y, the "
            "shipped -10,-10 outside its front-left corner (refused), the nozzle-probe pin "
            "near the rear edge right of centre, and, small in red, the bed centre as a guess "
            "with no pin under it.",
        ],
        "insert": [
            ("12-software.md", "Step 12.33", "first image"),
        ],
        "verify": [
            "Travel limits are the config's position_min 0 / position_max 350. The pin is "
            "placed after Ch 09.30 (right bed extrusion's inner face, just behind the plate's "
            "rear edge, extrusions 65 mm either side of centre); its coordinates are measured "
            "in Ch 13 and the drawn spot is approximate.",
        ],
    },
]
