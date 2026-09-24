"""Per-step lead crops of the layout-v3 overlay for Ch 10 (10.8-10.16, 10.77, 10.80).

Base: docs/manual/assets/b11/layout-v3-overlay.jpg (made by outputs_v3.py, 1500 px
resized to 1100). Frame = outputs_v3.py's apparent-mm frame: x right = printer right,
y down = rearward, px = (mm + 250) * 2.2. Positions are the overlay's (+/-6 %
absolute, +/-1.5 mm local); the PSU and SSR screws are where LDO's photo shows them
(the v3 PSU sits 6 mm further left). Lead paths are schematic: which conduit, which
screw, not where each core lies inside it.

Terminal positions read off the base photo (bay-general-placement.jpg):
  PSU strip, front to rear: +V x3, -V x3, FG, N, L at y 39.4 ... 115.0 (pitch 9.45),
  i.e. datasheet 9 8 7 | 6 5 4 | 3 2 1. SSR (text upside down in the photo): INPUT
  front, LOAD rear, LOAD 1 at printer right, LOAD 2 at printer left.
  WAGO 221-415 blocks, printer left to right: N, L, PE (LDO S3 mapping photo).

Run from the repo root: python3 review/2026-09-23-bay-mods/layout-v3/work/leads_v3.py
"""
import math
from PIL import Image, ImageDraw, ImageFont

BASE = 'docs/manual/assets/b11/layout-v3-overlay.jpg'
OUT = 'docs/manual/assets/b11/'
PPM = 2.2
FB = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
FR = '/System/Library/Fonts/Supplemental/Arial.ttf'

BROWN, BLUE, YEL, GRN = (150, 75, 20), (25, 95, 230), (250, 215, 0), (20, 150, 60)
MAG = (200, 0, 160)

# Anchors (apparent mm)
WAGO = {'N': -113.5, 'L': -83.0, 'PE': -53.0}          # block centres, port face y 202
PORT_Y = 202.0
def port(block, k):                                    # k = 0..4 across the 5-way block
    return (WAGO[block] - 11.6 + 5.8 * k, PORT_Y)
PSU_X = -12.0                                          # screw heads, photo position
PSU_Y = {'L': 115.0, 'N': 105.5, 'FG': 96.1, '-V': [86.5, 77.3, 67.9], '+V': [58.5, 49.3, 39.4]}
SSR = {'LOAD1': (-73.5, 90.5), 'LOAD2': (-98.5, 90.5)}
HOLE = (14.7, 146.0)
STUB_X = -72.0
LUG_V3, LUG_LDO = (-20.0, 210.0), (105.0, 210.0)
NOTCH = (0.0, 12.0, 195.0, 222.0)


def arc(cx, cy, r, a0, a1, n=12):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

# Bed path: hole -> 34 mm run -> lower R15 -> upper R15 -> box right end (y 177)
def bed_path(dy=0.0):
    r = 15.5 + dy
    return ([(HOLE[0], HOLE[1] + dy), (-7.4, 146.0 + dy)] + arc(-7.4, 161.5, r, 270, 180)[1:]
            + arc(-38.4, 161.5, 15.5 - dy, 0, 90)[1:])


class Crop:
    def __init__(self, x0, x1, y0, y1, scale):
        self.x0, self.y0, self.s = x0, y0, scale
        im = Image.open(BASE).convert('RGB')
        box = tuple(int(round((v + 250) * PPM)) for v in (x0, y0, x1, y1))
        self.im = im.crop(box).resize(((box[2] - box[0]) * scale, (box[3] - box[1]) * scale), Image.LANCZOS)
        self.px0, self.py0 = box[0], box[1]
        self.d = ImageDraw.Draw(self.im)
        self.f = ImageFont.truetype(FB, 14 * scale)
        self.fs = ImageFont.truetype(FR, 13 * scale)

    def P(self, x, y):
        return (((x + 250) * PPM - self.px0) * self.s, ((y + 250) * PPM - self.py0) * self.s)

    def lead(self, pts, col, stripe=None, w=3.2):
        q = [self.P(*p) for p in pts]
        W = int(w * self.s)
        self.d.line(q, fill=(0, 0, 0), width=W + 4, joint='curve')
        self.d.line(q, fill=col, width=W, joint='curve')
        if stripe:                                     # green/yellow: green dashes on yellow
            for a, b in zip(q, q[1:]):
                L = math.dist(a, b); n = int(L // (6 * self.s))
                for i in range(0, n, 2):
                    t0, t1 = i / max(n, 1), min((i + 1) / max(n, 1), 1)
                    self.d.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
                                 (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], fill=stripe, width=W)
        for p in (q[0], q[-1]):
            r = W * 0.9
            self.d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=col, outline=(0, 0, 0), width=2)

    def tag(self, x, y, text, anchor='mm', big=True):
        self.d.text(self.P(x, y), text, fill=(0, 0, 0), font=self.f if big else self.fs,
                    anchor=anchor, stroke_width=3 * self.s // 2, stroke_fill=(255, 255, 255))

    def ring(self, x, y, r, col, dash=False):
        u, v = self.P(x, y); R = r * PPM * self.s
        if dash:
            for a in range(0, 360, 30):
                self.d.arc([u - R, v - R, u + R, v + R], a, a + 15, fill=col, width=3 * self.s)
        else:
            self.d.ellipse([u - R, v - R, u + R, v + R], outline=col, width=3 * self.s)

    def title(self, text):
        lines, cur = [], ''
        for w in text.split():
            t = (cur + ' ' + w).strip()
            if self.fs.getlength(t) > self.im.width - 12 * self.s and cur:
                lines.append(cur); cur = w
            else:
                cur = t
        lines.append(cur)
        lh = 16 * self.s; H = lh * len(lines) + 5 * self.s
        band = Image.new('RGB', (self.im.width, self.im.height + H), (255, 255, 255))
        band.paste(self.im, (0, H))
        bd = ImageDraw.Draw(band)
        for i, t in enumerate(lines):
            bd.text((6 * self.s, 3 * self.s + i * lh), t, fill=(0, 0, 0), font=self.fs)
        return band

    def save(self, name, text):
        self.title(text).save(OUT + name, quality=88)
        print(OUT + name)


NOTE = 'Layout v3, rear at bottom. Lead paths schematic; positions +/-6 %.'
AC_BOX = (-150, 45, 25, 250)


def inlet_leads(c):
    for blk, col, st, k, dx, yy in (('N', BLUE, None, 0, -6, 194), ('L', BROWN, None, 0, 0, 186), ('PE', YEL, GRN, 0, 6, 178)):
        c.lead([(-122 + dx, 226), (-128 + dx, yy), (port(blk, k)[0], yy), port(blk, k)], col, st)


def psu_leads(c):
    for blk, col, st, t, k, dy in (('N', BLUE, None, 'N', 1, 0), ('L', BROWN, None, 'L', 1, 6), ('PE', YEL, GRN, 'FG', 1, -6)):
        px = port(blk, k)
        c.lead([px, (px[0], 186 + dy / 2), (STUB_X + dy / 2, 170), (STUB_X + dy / 2, 116 + dy),
                (-34, 116 + dy), (PSU_X - 4, PSU_Y[t]), (PSU_X, PSU_Y[t])], col, st)


def ssr_live(c):
    px = port('L', 2)
    c.lead([px, (px[0], 186), (STUB_X - 3, 170), (STUB_X - 3, 116), (-96, 116), SSR['LOAD2']], BROWN)


def bed_live(c):
    c.lead(bed_path(0) + [(-60, 176), (STUB_X + 3, 165), (STUB_X + 3, 112), SSR['LOAD1']], BROWN)


def bed_n_pe(c):
    c.lead(bed_path(-3) + [(-90, 180), (port('N', 3)[0], 188), port('N', 3)], BLUE)
    c.lead(bed_path(3) + [(-52, 182), (port('PE', 2)[0], 190), port('PE', 2)], YEL, GRN)


def frame_pe(c):
    c.lead([LUG_V3, (-30, 206), (-40, 198), (port('PE', 4)[0], 196), port('PE', 4)], YEL, GRN)


def wago_tags(c):
    for b in WAGO:
        c.tag(WAGO[b], 229, b)


def psu_tags(c, full=False):
    c.tag(PSU_X + 14, PSU_Y['L'], '1 L', 'lm'); c.tag(PSU_X + 14, PSU_Y['N'], '2 N', 'lm')
    c.tag(PSU_X + 14, PSU_Y['FG'], '3 FG', 'lm')
    if full:
        c.tag(PSU_X + 14, PSU_Y['-V'][1], '4-6  -V', 'lm'); c.tag(PSU_X + 14, PSU_Y['+V'][1], '7-9  +V', 'lm')


def build():
    c = Crop(*AC_BOX, 2); inlet_leads(c); wago_tags(c)
    c.save('v3-lead-10-08-inlet-wago.jpg', 'Step 10.8: inlet -> WAGO N / L / PE, inside the wire box. ' + NOTE)

    c = Crop(*AC_BOX, 2); psu_leads(c); wago_tags(c); psu_tags(c)
    c.tag(-60, 158, 'port stub', 'mm', False)
    c.save('v3-lead-10-09-wago-psu.jpg', 'Step 10.9: WAGO -> box -> stub -> SSR run -> PSU 1 L, 2 N, 3 FG. ' + NOTE)

    c = Crop(*AC_BOX, 2); ssr_live(c); wago_tags(c); c.tag(-98.5, 80, 'LOAD 2'); c.tag(-73.5, 80, 'LOAD 1')
    c.save('v3-lead-10-11-wago-ssr.jpg', 'Step 10.11: WAGO L -> SSR LOAD 2 via stub and T. ' + NOTE)

    c = Crop(*AC_BOX, 2); bed_live(c); c.tag(-73.5, 80, 'LOAD 1')
    c.save('v3-lead-10-14-bed-l-ssr.jpg', 'Step 10.14: Bed L, hole -> 34 mm run -> both curves -> box -> SSR LOAD 1. Magenta ring = bed hole. ' + NOTE)

    c = Crop(*AC_BOX, 2); bed_n_pe(c); wago_tags(c)
    c.save('v3-lead-10-15-bed-n-pe.jpg', 'Step 10.15: Bed N -> WAGO N, bed PE -> WAGO PE, via both curves from the bed hole (magenta ring). ' + NOTE)

    c = Crop(-140, 45, 150, 250, 3); frame_pe(c); wago_tags(c)
    c.ring(*LUG_V3, 5, MAG); c.tag(LUG_V3[0], 232, 'v3 lug', 'mm')
    c.tag(44, 244, 'LDO lug: right of the notch ->', 'rm', False)
    c.save('v3-lead-10-16-frame-pe.jpg', 'Step 10.16: frame PE lug (magenta ring) ~20 mm to the printer\'s left of the Z-chain notch, between the WAGO-mount screw and the notch; lead to WAGO PE. ' + NOTE)

    c = Crop(-115, 30, 25, 135, 3); psu_tags(c, full=True)
    u0, v = c.P(-27.5, 91.3); u1, _ = c.P(-6, 91.3)
    for t in range(int(u0), int(u1), 12):
        c.d.line([(t, v), (min(t + 6, u1), v)], fill=MAG, width=4)
    c.tag(-40, 84, 'fin', 'mm')
    c.save('v3-psu-terminals-10-80.jpg', 'Step 10.80: PSU screws, chapter numbering. Fin between 3 FG and 4 -V. ' + NOTE)


if __name__ == '__main__':
    build()
