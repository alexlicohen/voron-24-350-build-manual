#!/usr/bin/env python3
"""Author the Voron manual raven mascot set (viewBox 0 0 512 512).

One anatomy shared by every pose, built from feather ROWS rather than blobs:
skull + heavy hooked bill with nasal bristles, shaggy throat hackles, four
charcoal tones of folded-wing coverts over secondaries over primaries, a
wedge tail, scaled feet. A pale halo pass draws the outer silhouette dilated
before the art, so the bird survives Material's dark slate (#1e2129).

Usage: python3 scripts/gen_mascot.py docs/manual/assets/mascot
"""
import math
import sys
from pathlib import Path

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
W = H = 512

# ---------------------------------------------------------------- palette
K0 = "#0E1116"   # deepest: primaries, bill tip, far leg, separations
K1 = "#161A21"   # body base
K2 = "#222A38"   # greater coverts, mantle, hackle alternate
K3 = "#30394B"   # highest charcoal: nape, breast edge, eye socket
HALO = "#EDF0F4"
WHITE = "#FFFFFF"
BLUE = "#2A6FB5"
BLUEF = "#DCE9F6"
GREY = "#5C6675"
GREYF = "#E7E9EC"
STEEL = "#B6BDC6"
AMBER = "#D98324"
AMBERF = "#FBEBD3"
GREEN = "#2E7D32"
# Revali's Champion scarf and the braid ties: the manual's accent blue (the
# printer's frame), with a lit fold and a shadow crease. Nothing else is blue
# at this value, so the scarf is the one place the character meets the build.
SCARF = "#1F4E9C"
SCARF_LIT = "#3A6DC4"
SCARF_DK = "#163B7A"
EDGE = "#2B3341"   # separation stroke that reads on black
EDGE2 = "#3C465A"  # brighter separation for the dark tail/primary mass

HALO_W = 10.5
HALO_W_THIN = 6.0


# ---------------------------------------------------------------- helpers
def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def pt(p):
    return f"{f(p[0])} {f(p[1])}"


def polar(p, ang, r):
    a = math.radians(ang)
    return (p[0] + r * math.cos(a), p[1] + r * math.sin(a))


def lerp(a, b, t):
    return a + (b - a) * t


def lerp2(a, b, t):
    return (lerp(a[0], b[0], t), lerp(a[1], b[1], t))


def feather(base, ang, length, halfw, bend=0.0, blunt=0.35):
    """Lanceolate feather: base point, direction in screen degrees, length."""
    tip = polar(base, ang, length)
    per = ang + 90
    bx = polar((0, 0), per, bend)
    up1 = polar(base, ang, length * 0.18)
    up1 = (up1[0] + math.cos(math.radians(per)) * halfw + bx[0] * 0.4,
           up1[1] + math.sin(math.radians(per)) * halfw + bx[1] * 0.4)
    up2 = polar(base, ang, length * (1 - blunt * 0.45))
    up2 = (up2[0] + math.cos(math.radians(per)) * halfw * 0.82 + bx[0],
           up2[1] + math.sin(math.radians(per)) * halfw * 0.82 + bx[1])
    dn2 = polar(base, ang, length * (1 - blunt * 0.45))
    dn2 = (dn2[0] - math.cos(math.radians(per)) * halfw * (0.55 + blunt) + bx[0],
           dn2[1] - math.sin(math.radians(per)) * halfw * (0.55 + blunt) + bx[1])
    dn1 = polar(base, ang, length * 0.18)
    dn1 = (dn1[0] - math.cos(math.radians(per)) * halfw * 0.9 + bx[0] * 0.4,
           dn1[1] - math.sin(math.radians(per)) * halfw * 0.9 + bx[1] * 0.4)
    return (f"M{pt(base)}C{pt(up1)} {pt(up2)} {pt(tip)}"
            f"C{pt(dn2)} {pt(dn1)} {pt(base)}Z")


def row(n, b0, b1, a0, a1, l0, l1, w0, w1, bend=0.0, blunt=0.35):
    """A shingled row of feathers; returns back-to-front path list."""
    out = []
    for i in range(n):
        t = i / max(n - 1, 1)
        out.append(feather(lerp2(b0, b1, t), lerp(a0, a1, t), lerp(l0, l1, t),
                           lerp(w0, w1, t), bend, blunt))
    return out


def jitter(i, amp=0.14):
    """Deterministic length wobble so a row reads shaggy, not like lozenges."""
    return 1.0 + amp * ((i * 37 % 7) / 3.0 - 1.0)


def plume(base, ang, length, halfw, bend=0.0, n=3, col=None, op="0.5"):
    """Rachis plus a few barb strokes along one long feather.

    A few strokes, never a hatch: at 256 px a hatch turns into noise.
    """
    col = col or "#3C465A"
    el = [path(taper([polar(base, ang, length * 0.08),
                      polar(base, ang, length * 0.93)], [2.8, 1.0]),
               col, None, None, op)]
    for i in range(n):
        t = 0.3 + i * (0.5 / max(n - 1, 1))
        q = polar(base, ang, length * t)
        far = polar(q, ang + 58, halfw * 1.25 * (1 - t * 0.35) + bend * 0.2)
        el.append(path(taper([q, far], [2.0, 0.9]), col, None, None, op))
    return el


def long_feather(base, ang, ln, hw, bend, blunt, fill, stroke, sw,
                 detail=True, barbs=3, op="0.5"):
    """One flight feather or rectrix: shape, then rachis and barbs."""
    el = [path(feather(base, ang, ln, hw, bend, blunt), fill, stroke, sw)]
    if detail:
        el += plume(base, ang, ln, hw, bend, barbs, op=op)
    return el


def shingle(specs, rim, core, stroke, sw, inner=0.84):
    """A covert row drawn with a lighter rim so the shingling reads as
    feathers rather than as scales."""
    el = []
    for base, ang, ln, hw, bend, blunt in specs:
        el.append(path(feather(base, ang, ln, hw, bend, blunt), rim, stroke, sw))
        el.append(path(feather(base, ang, ln * inner, hw * inner, bend, blunt),
                       core))
    return el


def row_specs(n, b0, b1, a0, a1, l0, l1, w0, w1, bend=0.0, blunt=0.35):
    out = []
    for i in range(n):
        t = i / max(n - 1, 1)
        out.append((lerp2(b0, b1, t), lerp(a0, a1, t), lerp(l0, l1, t),
                    lerp(w0, w1, t), bend, blunt))
    return out


def taper(points, widths):
    """Filled outline of a tapered polyline (legs, toes, lanyards)."""
    left, right = [], []
    n = len(points)
    for i, p in enumerate(points):
        a = points[max(i - 1, 0)]
        b = points[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / ln, dx / ln
        w = widths[i] / 2
        left.append((p[0] + nx * w, p[1] + ny * w))
        right.append((p[0] - nx * w, p[1] - ny * w))
    d = "M" + "L".join(pt(p) for p in left)
    d += "L" + "L".join(pt(p) for p in reversed(right)) + "Z"
    return d


def path(d, fill=None, stroke=None, sw=None, op=None, extra=""):
    a = [f'd="{d}"']
    if fill:
        a.append(f'fill="{fill}"')
    if stroke:
        a.append(f'stroke="{stroke}"')
    if sw:
        a.append(f'stroke-width="{f(sw)}"')
    if op:
        a.append(f'opacity="{op}"')
    if extra:
        a.append(extra)
    return "<path " + " ".join(a) + "/>"


def circle(c, r, fill, op=None, stroke=None, sw=None):
    s = f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="{f(r)}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{f(sw or 2)}"'
    if op:
        s += f' opacity="{op}"'
    return s + "/>"


def g(cls, body, extra=""):
    o = f'<g class="{cls}"' if cls else "<g"
    if extra:
        o += " " + extra
    return o + ">" + "".join(body) + "</g>"


def anchor():
    return f'<rect x="0" y="0" width="{W}" height="{H}" fill="none"/>'


# ---------------------------------------------------------------- anatomy
# Everything below is authored in the base frame: bird standing, facing right,
# feet on y=470, crown at y=112, bill tip at x=482.

TORSO = ("M298 174C290 202 286 222 284 240C240 250 196 274 164 308"
         "C146 328 138 348 142 366C150 390 174 402 204 408"
         "C242 414 288 406 314 382C338 360 350 326 348 292"
         "C346 258 352 230 352 208C352 192 344 180 330 176Z")

TAIL = ("M152 336C116 350 74 370 36 398L52 420C98 414 150 396 184 376"
        "C174 356 162 344 152 336Z")

SKULL = ("M300 176C296 142 316 114 350 110C376 107 392 122 396 140"
         "L398 186C384 202 356 210 332 206C312 202 302 192 300 176Z")

BILL = ("M390 132C426 140 462 154 484 170C486 177 482 182 474 181"
        "C448 187 414 193 386 190Z")

# A fledgling's bill: shorter, blunter, no hook.
BILL_SHORT = ("M390 136C412 142 430 152 440 164C441 170 437 174 430 173"
              "C416 180 402 186 386 187Z")
BILL_SHORT_LOWER = ("M386 174C404 178 420 178 432 172C435 176 433 180 427 181"
                    "C412 186 398 187 386 186Z")

WING = ("M294 232C258 230 210 256 174 290C142 320 116 358 104 392"
        "L130 406C170 382 224 330 260 286C278 264 294 244 294 232Z")

EYE_C = (362, 150)


def legs(lift=False):
    """Near and far leg, ankle to claws. Returns (far, near) element lists."""
    def one(ax, ay, fx, fy, back=False):
        el = []
        col = K0 if back else K1
        line = "#05070A" if back else K0
        el.append(path(taper([(ax, ay), (ax + 4, ay + 28), (fx, fy)],
                             [27, 21, 17]), col))
        for t in (0.3, 0.5, 0.7, 0.88):
            q = lerp2((ax, ay), (fx, fy), t)
            hw = 10 - t * 2
            el.append(path(taper([(q[0] - hw, q[1] - 1), (q[0] + hw, q[1] - 2)],
                                 [3.2, 3.2]), line, None, None, "0.9"))
        toes = [([(fx, fy), (fx + 27, fy + 4), (fx + 54, fy + 6)], [18, 12, 7]),
                ([(fx, fy), (fx + 19, fy + 8), (fx + 37, fy + 11)], [16, 11, 6]),
                ([(fx, fy), (fx + 9, fy + 10), (fx + 17, fy + 13)], [15, 10, 6]),
                ([(fx, fy), (fx - 19, fy + 5), (fx - 39, fy + 8)], [16, 10, 6])]
        for pts, ws in toes:
            el.append(path(taper(pts, ws), col))
            el.append(path(taper([pts[0], pts[1]], [1, 1]), line, None, None, "0"))
            tipd = (pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1])
            ln = math.hypot(*tipd) or 1
            d = (tipd[0] / ln, tipd[1] / ln)
            claw = (pts[-1][0] + d[0] * 11, pts[-1][1] + d[1] * 11 + 4)
            el.append(path(taper([pts[-1], claw], [6.5, 1.4]), line))
        return el

    far = one(238, 386, 242, 458, back=True)
    if lift:
        near = one(280, 388, 292, 436, False)
    else:
        near = one(280, 388, 286, 462, False)
    return far, near


def leg_shapes(lift=False):
    far, near = legs(lift)
    return far, near


# Hackle points project past the throat line so the front silhouette is
# serrated - a raven tell. A solid fringe row just reads as a second wing.
HACKLE_PTS = [((340, 190), 56, 30), ((341, 212), 60, 33), ((343, 236), 64, 35),
              ((343, 260), 68, 33), ((341, 282), 72, 29)]


def hackle_paths():
    return [feather(b, a, ln * jitter(i, 0.16), 9.5, 2, 0.0)
            for i, (b, a, ln) in enumerate(HACKLE_PTS)]


def hackles():
    """Shaggy throat hackles: the raven tell. Serrated throat, not a cape."""
    el = []
    for i, (b, a, ln) in enumerate(HACKLE_PTS):
        el.append(path(feather(b, a + 26, ln * 1.5 * jitter(i, 0.12), 11, 3, 0.0),
                       K2 if i % 2 else K1, EDGE, 1.8, "0.8"))
    for i, d in enumerate(hackle_paths()):
        el.append(path(d, K3 if i % 2 else K2, EDGE, 2.2))
    return el


PRIMARY_SPECS = row_specs(7, (166, 336), (216, 296), 156, 138, 132, 122,
                          13, 16, bend=7, blunt=0.02)
PRIMARIES = [feather(*sp) for sp in PRIMARY_SPECS]


def wing_layers():
    """Folded wing: primaries under secondaries under coverts under sheen."""
    el = [path(WING, K0)]
    for i, sp in enumerate(PRIMARY_SPECS):
        el += long_feather(*sp, "#10141B" if i % 2 else "#1B212C", EDGE2, 2.4)
    # secondaries: rounded tips, emerging from under the greater coverts
    for i, sp in enumerate(row_specs(6, (186, 318), (268, 264), 146, 128,
                                     104, 92, 20, 18, bend=6, blunt=0.5)):
        el += long_feather(*sp, K1 if i % 2 else "#12161E", EDGE2, 2.5,
                           barbs=2)
    el += shingle(row_specs(7, (196, 290), (300, 226), 136, 119, 78, 62,
                            18, 17, bend=5, blunt=0.62), "#333D50", K2, K0, 2.4)
    el += shingle(row_specs(7, (206, 272), (302, 214), 133, 117, 56, 46,
                            16, 15, bend=4, blunt=0.72), "#46536C", K3, K0, 2.2)
    for d in row(7, (206, 272), (302, 214), 133, 117, 46, 38, 13, 12,
                 bend=4, blunt=0.72):
        el.append(path(d, "url(#sheen)", None, None, "0.85"))
    el += shingle(row_specs(6, (232, 248), (300, 204), 131, 115, 36, 30,
                            13, 12, blunt=0.85), "#46536C", K3, K0, 2.0)
    for d in row(6, (232, 248), (300, 204), 131, 115, 29, 24, 10, 9,
                 blunt=0.85):
        el.append(path(d, "url(#sheen)", None, None, "0.6"))
    return el


FAR_OFF = 'transform="translate(-9 -13)"'


def far_folded_profile():
    """The other wing, folded on the far side: only what clears the body."""
    el = [path(WING, K0)]
    for i, d in enumerate(PRIMARIES):
        el.append(path(d, "#0B0E13" if i % 2 else "#12161E", "#2A313D", 2.2))
    return [g("", el, FAR_OFF)]


def far_folded_profile_halo():
    return [g("", [path(WING)] + [path(d) for d in PRIMARIES], FAR_OFF)]


def tail_detail():
    el = [path(TAIL, K0)]
    for i, sp in enumerate(row_specs(5, (180, 376), (154, 340), 172, 158,
                                     106, 134, 13, 15, bend=3, blunt=0.06)):
        el += long_feather(*sp, "#191F29" if i % 2 else "#0F131A", EDGE2, 2.3)
    return el


def body_art():
    el = [path(TORSO, K1)]
    el.append(path("M294 238C248 248 202 272 168 306C150 326 140 346 143 364"
                   "C164 336 206 298 248 278C270 267 286 256 294 238Z", K2))
    el.append(path("M348 292C350 328 338 360 316 382C300 396 276 406 250 410"
                   "C290 398 320 372 332 334C339 312 344 302 348 292Z", K3,
                   None, None, "0.7"))
    el.append(path("M310 382C288 400 248 412 206 408C246 404 290 392 310 382Z",
                   K0, None, None, "0.75"))
    # soft breast scallops, low contrast so the wing stays the focus
    for b0, b1, n, ln in (((292, 348), (340, 296), 4, 44),
                          ((262, 390), (310, 342), 4, 40)):
        for d in row(n, b0, b1, 126, 110, ln, ln - 4, 19, 18, blunt=0.88):
            el.append(path(d, K1, EDGE, 1.6, "0.2"))
    # thigh feathers hiding the top of each tarsus
    for bx, col in ((236, K0), (278, K0)):
        for d in row(3, (bx - 20, 378), (bx + 12, 382), 80, 100, 32, 28, 14, 12,
                     blunt=0.45):
            el.append(path(d, col, EDGE, 1.6, "0.5"))
    return el


def eyelid(c=None, r=20.0, sw=1.0, fill=K1):
    """A rounded upper lid over the eye: friendly, not a stare.

    Crops the top ~20% of the disc. Any deeper and the bird looks sleepy; a
    stroke on the lid edge reads as a monocle, so there is none.
    """
    cx, cy = c or EYE_C
    k = r / 20.0
    return [path(f"M{f(cx-22*k)} {f(cy)}C{f(cx-22*k)} {f(cy-17*k)} "
                 f"{f(cx-13*k)} {f(cy-24*k)} {f(cx)} {f(cy-24*k)}"
                 f"C{f(cx+14*k)} {f(cy-24*k)} {f(cx+24*k)} {f(cy-16*k)} "
                 f"{f(cx+24*k)} {f(cy-1*k)}"
                 f"C{f(cx+19*k)} {f(cy-12*k)} {f(cx+11*k)} {f(cy-17*k)} "
                 f"{f(cx-1*k)} {f(cy-16*k)}"
                 f"C{f(cx-11*k)} {f(cy-15*k)} {f(cx-18*k)} {f(cy-9*k)} "
                 f"{f(cx-22*k)} {f(cy)}Z", fill)]


def head_art(brow=False, bill=None, sw=1.0):
    # braids first: their roots sit under the skull, so they hang from it
    el = braids_profile()[0]
    el.append(path(SKULL, K1))
    # nape + crown in the light charcoal, then sheen
    el.append(path("M300 176C296 142 316 114 350 110C374 108 390 121 395 138"
                   "C372 124 338 126 318 146C306 158 301 168 300 176Z", K3))
    el.append(path("M305 166C305 142 322 121 350 118C370 116 383 125 389 137"
                   "C368 129 341 134 324 152C315 161 308 162 305 166Z",
                   "url(#sheen)", None, None, "0.65"))
    # cheek / ear coverts, slightly lifted tone, plus a pale cheek catch
    el.append(path("M312 190C326 202 352 206 374 198C362 208 336 210 318 202"
                   "C314 199 312 194 312 190Z", K2, None, None, "0.9"))
    el.append(path("M322 190C330 187 338 188 342 192C337 197 329 198 323 196"
                   "C320 195 320 191 322 190Z", "#3A4559", None, None, "0.5"))
    # bill: upper mandible then the darker lower one
    el.append(path(bill or BILL, K1, K0, 2.2 * sw))
    if bill:
        el.append(path(BILL_SHORT_LOWER, K0))
        el.append(path("M382 172C398 176 416 178 432 174", None, K0, 2.4 * sw))
    if not bill:
        el.append(path("M388 176C416 182 448 184 474 178C478 182 476 186 468 188"
                       "C440 192 412 191 389 187Z", K0))
        el.append(path("M392 168C420 172 452 174 478 170", None, K0, 2.4 * sw))
    # nasal bristles over the base of the culmen
    for i in range(6):
        t = i / 5
        b = (388 + t * 4, 138 + t * 14)
        el.append(path(taper([b, polar(b, 14 + t * 6, 30 + t * 14)],
                             [4.4, 1.0]), K3, None, None, "0.85"))
    # gape: the mouth line, hooked up at the hinge so the bill reads friendly
    el.append(path("M326 202C346 209 366 208 377 201C384 197 389 191 392 181",
                   None, K0, 2.4 * sw, None, 'stroke-linecap="round"'))
    if brow:
        el.append(path(taper([(344, 132), (380, 142)], [9, 5]), K0))
    return el


def eye_group(closed=False, r=20.0, c=None, hi=1.0):
    """One eye: socket ring, dark disc, white catchlight, faint lower glint."""
    cx, cy = c or EYE_C
    el = [circle((cx, cy), r + 2.5, K3, "0.9"), circle((cx, cy), r, K0),
          circle((cx, cy), r + 1.4, "none", "0.55", "#5A6780", r * 0.1)]
    if closed:
        el.append(path(f"M{f(cx-r*0.85)} {f(cy+1)}"
                       f"C{f(cx-r*0.3)} {f(cy+r*0.55)}"
                       f" {f(cx+r*0.4)} {f(cy+r*0.55)}"
                       f" {f(cx+r*0.85)} {f(cy+1)}", None, HALO, 3.4))
        return el, False
    el.append(circle((cx + r * 0.25, cy - r * 0.25), r * 0.33 * hi, WHITE))
    el.append(circle((cx - r * 0.35, cy + r * 0.4), r * 0.14 * hi, HALO, "0.75"))
    return el, True


# ---------------------------------------------------------------- Revali cues
# The daughter named the bird Revali, after the Rito Champion. Two cues carry
# the lineage and every adult pose inherits them: the Champion's blue scarf,
# tied at the back with its tails streaming behind (the self-made updraft, in
# cloth), and a pair of braided nape feathers tied with the same blue. The
# anatomy underneath is unchanged. The fledgling gets neither - it is not the
# champion.


def flow(p0, p1, bulge=0.0, wave=0.0, n=7):
    """Points along p0 -> p1 bowed sideways by `bulge` with one S `wave`: the
    line a strip of cloth takes in moving air. Positive is to the left of
    travel (screen up, for a tail streaming back from a right-facing bird)."""
    ang = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
    pts = []
    for i in range(n):
        t = i / (n - 1)
        off = bulge * math.sin(math.pi * t) + wave * math.sin(2 * math.pi * t)
        pts.append(polar(lerp2(p0, p1, t), ang - 90, off))
    return pts


def tail(p0, p1, w0, w1, bulge=0.0, wave=0.0, lit=1):
    """One scarf tail: a flowing strip tapering from w0 at the knot to w1."""
    pts = flow(p0, p1, bulge, wave)
    n = len(pts)
    ws = [lerp(w0, w1, (i / (n - 1)) ** 1.3) for i in range(n)]
    ws[-1] = w1 * 0.55
    return ribbon(pts, ws, lit)


def ribbon(pts, widths, lit=1):
    """A strip of cloth along a polyline: base fill, a dark edge, and a lit
    stripe along one side (`lit` picks the side). Returns (art, halo_d)."""
    base = taper(pts, widths)
    off = []
    n = len(pts)
    for i, p in enumerate(pts):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1.0
        off.append((p[0] - dy / ln * widths[i] * 0.22 * lit,
                    p[1] + dx / ln * widths[i] * 0.22 * lit))
    art = [path(base, SCARF, SCARF_DK, 1.6, None, 'stroke-linejoin="round"'),
           path(taper(off, [w * 0.4 for w in widths]), SCARF_LIT, None, None,
                "0.9")]
    return art, base


def scarf_band(top, bottom, fold, crease):
    """The loop round the neck: base, a lit upper fold, one shadow crease."""
    return [path(top + bottom, SCARF, SCARF_DK, 1.6,
                 extra='stroke-linejoin="round"'),
            path(fold, SCARF_LIT, None, None, "0.9"),
            path(crease, None, SCARF_DK, 2.0, "0.7", 'stroke-linecap="round"')]


def braid(p0, p1, w=11.0, n=4, simple=False):
    """A plait of nape feathers from p0 (under the skull) to p1: a tapered
    strand with chevrons for the weave, a scarf-blue tie near the end and a
    loose tuft past it. `simple` drops the weave for the badge, where it would
    be sub-pixel. Returns (art, halo paths)."""
    ang = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
    mid = polar(lerp2(p0, p1, 0.5), ang + 90, w * 0.3)
    body = taper([p0, mid, p1], [w, w * 0.94, w * 0.66])
    art = [path(body, K2, "#46536C", 1.8, None, 'stroke-linejoin="round"')]
    if not simple:
        for i in range(n):
            t = 0.28 + i * (0.5 / (n - 1))
            q = lerp2(p0, p1, t)
            hw = w * lerp(1.0, 0.66, t) * 0.42
            v = polar(q, ang, w * 0.4)
            art.append(path(f"M{pt(polar(q, ang + 90, hw))}L{pt(v)}"
                            f"L{pt(polar(q, ang - 90, hw))}", None, "#46536C",
                            2.0, "0.85",
                            'stroke-linecap="round" stroke-linejoin="round"'))
    q = lerp2(p0, p1, 0.86)
    hw = w * 0.7 * 0.5 + 1.2
    art.append(path(taper([polar(q, ang + 90, hw), polar(q, ang - 90, hw)],
                          [5.5, 5.5]), SCARF))
    tuft = [feather(polar(q, ang, 4), ang + da, w * 1.35, w * 0.27, 0, 0.0)
            for da in (-24, 0, 24)]
    for k, d in enumerate(tuft):
        art.append(path(d, K3 if k % 2 else K2, EDGE, 1.4))
    return art, [body] + tuft


# -- profile -------------------------------------------------------------
# The band sits on the side of the neck between the skull and the wing's
# shoulder; the wing coverts overlap its back end. The tails leave a small
# knot at the back of the neck, below the braid tips, and stream back over
# the mantle. Asleep (`pause`), there is no updraft: they droop, short, and
# stay clear of the nightcap's tassel.
SCARF_PROFILE = dict(
    top="M288 206C306 212 330 216 352 222",
    bottom="L352 246C330 244 306 242 286 238Z",
    fold="M288 206C306 212 330 216 352 222L352 231C330 226 306 222 287 218Z",
    crease="M289 230C308 232 330 236 352 240")
SCARF_TAILS_PROFILE = [((290, 222), (194, 190), 19, 7, 10, 6),
                       ((290, 228), (210, 226), 15, 6, 2, -6)]
SCARF_TAILS_ASLEEP = [((290, 223), (236, 226), 16, 6, -3, 0),
                      ((290, 228), (240, 238), 13, 5, -4, 0)]
SCARF_KNOT_PROFILE = (289, 226)
BRAIDS_PROFILE = [((306, 150), (272, 208), 11.0), ((300, 166), (262, 200), 9.5)]


def knot(c, r=8.5):
    return [circle(c, r, SCARF_DK), circle((c[0] - 2, c[1] - 2), r * 0.5,
                                           SCARF_LIT)]


def scarf_profile(asleep=False):
    """(band, tails, halo) - band goes under the wing, tails over it."""
    band = scarf_band(**SCARF_PROFILE)
    tails, halo = [], []
    for p0, p1, w0, w1, bulge, wave in (SCARF_TAILS_ASLEEP if asleep
                                        else SCARF_TAILS_PROFILE):
        a, d = tail(p0, p1, w0, w1, bulge, wave, 1)
        tails += a
        halo.append(d)
    return band, knot(SCARF_KNOT_PROFILE) + tails, halo


def braids_profile():
    art, halo = [], []
    for p0, p1, w in BRAIDS_PROFILE:
        a, h = braid(p0, p1, w)
        art += a
        halo += h
    return art, halo


# -- three-quarter ---------------------------------------------------------
# The band wraps the base of the neck over the ruff, whose points spill out
# below it; the tails leave from the far shoulder, where the back of the neck
# is in this view. The braids hang beside the far cheek.
SCARF_3Q = dict(
    top="M206 212C240 232 300 236 332 214",
    bottom="L334 236C300 258 240 254 204 238Z",
    fold="M206 212C240 232 300 236 332 214L333 223C300 244 240 240 205 222Z",
    crease="M208 229C242 246 296 248 331 229")
SCARF_TAILS_3Q = [((207, 231), (130, 196), 15, 6, 9, 5),
                  ((207, 235), (134, 224), 12, 5, 3, -5)]
SCARF_KNOT_3Q = (208, 232)
BRAIDS_3Q = [((212, 118), (186, 206), 10.5), ((208, 140), (192, 220), 9.0)]


def scarf_3q(tails=True):
    band = scarf_band(**SCARF_3Q)
    tl, halo = [], []
    if tails:
        for p0, p1, w0, w1, bulge, wave in SCARF_TAILS_3Q:
            a, d = tail(p0, p1, w0, w1, bulge, wave, 1)
            tl += a
            halo.append(d)
        tl = knot(SCARF_KNOT_3Q) + tl
    return band, tl, halo


def braids_3q(simple=False):
    art, halo = [], []
    specs = BRAIDS_3Q[:1] if simple else BRAIDS_3Q
    for p0, p1, w in specs:
        a, h = braid(p0, p1, w + (3 if simple else 0), simple=simple)
        art += a
        halo += h
    return art, halo


# -- front -----------------------------------------------------------------
# Seen head-on the tails cannot stream behind, so they hang from a knot at
# the side of the bill, short, over the breast. Braid tips show either side
# of the neck.
SCARF_FRONT = dict(
    top="M182 210C220 240 292 240 332 206",
    bottom="L334 230C292 266 220 266 184 236Z",
    fold="M182 210C220 240 292 240 332 206L333 216C292 250 220 250 183 220Z",
    crease="M186 228C222 254 290 254 332 224")
SCARF_TAILS_FRONT = [((296, 250), (288, 334), 14, 6, 6, 4),
                     ((304, 252), (322, 322), 12, 5, -5, 3)]
SCARF_KNOT_FRONT = (299, 247)
BRAIDS_FRONT = [((188, 150), (172, 226), 10.0), ((326, 148), (340, 222), 9.0)]


def scarf_front():
    band = scarf_band(**SCARF_FRONT)
    tails, halo = [], []
    for p0, p1, w0, w1, bulge, wave in SCARF_TAILS_FRONT:
        a, d = tail(p0, p1, w0, w1, bulge, wave, -1)
        tails += a
        halo.append(d)
    return band, tails + knot(SCARF_KNOT_FRONT, 9), halo


def braids_front():
    art, halo = [], []
    for p0, p1, w in BRAIDS_FRONT:
        a, h = braid(p0, p1, w)
        art += a
        halo += h
    return art, halo


def thin_halo(paths, extra=""):
    return g("halo", paths,
             f'fill="{HALO}" stroke="{HALO}" stroke-width="{f(HALO_W_THIN)}" '
             'stroke-linejoin="round" stroke-linecap="round"' + extra)


# ---------------------------------------------------------------- halo pass
def rotg(children, deg, cx=300.0, cy=200.0, sc=1.0):
    """Wrap in a rotation, optionally scaled about the same pivot.

    `deg` is degrees of bill-up tilt. The head's halo shapes go through this
    too, so the rim never slides off the art.
    """
    if not deg and sc == 1.0:
        return list(children)
    t = f"rotate({f(-deg)} {f(cx)} {f(cy)})"
    if sc != 1.0:
        t += (f" translate({f(cx * (1 - sc))} {f(cy * (1 - sc))}) "
              f"scale({f(sc)})")
    return [g("", children, f'transform="{t}"')]


def halo_shapes(lift=False, extra=(), legs_el=None, bill=None, tilt=0.0,
                near_folded=True, far_folded=False, asleep=False):
    if legs_el is None:
        fl, nl = leg_shapes(lift)
        legs_el = fl + nl
    el = [path(d) for d in (TAIL, TORSO)]
    el += rotg([path(SKULL), path(bill or BILL)], tilt)
    if near_folded:
        el.append(path(WING))
        el += [path(d) for d in PRIMARIES]
    if far_folded:
        el += far_folded_profile_halo()
    el += [path(d) for d in hackle_paths()]
    el += [path(d) for d in extra]
    wide = g("halo", el,
             f'fill="{HALO}" stroke="{HALO}" stroke-width="{f(HALO_W)}" '
             'stroke-linejoin="round" stroke-linecap="round"')
    # Scarf tails and braids take the thin rim, like the legs: at their width
    # the body rim would turn them into pale sausages.
    thin = thin_halo(legs_el + [path(d) for d in scarf_profile(asleep)[2]]
                     + rotg([path(d) for d in braids_profile()[1]], tilt))
    return thin + wide


# ---------------------------------------------------------------- assembly
SHEEN_DEF = (
    '<defs><linearGradient id="sheen" x1="0.1" y1="0" x2="0.85" y2="1">'
    f'<stop offset="0" stop-color="#4C7FD3"/>'
    f'<stop offset="1" stop-color="#2A6FB5" stop-opacity="0.35"/>'
    "</linearGradient></defs>")

STYLE = """<style>
@media (prefers-reduced-motion:no-preference){
.mascot .m-body,.mascot .m-head,.mascot .m-eye,.mascot .m-wing,.mascot .m-tail,
.mascot .m-leg-lift,.mascot .m-prop,.mascot .m-zz,.mascot .m-bulb,
.mascot .m-chick,.mascot .m-layer,.mascot .m-tick,
.mascot .m-flap{transform-box:fill-box}
.mascot .m-body{transform-origin:256px 470px;animation:mascot-breathe 4.2s ease-in-out -1.1s infinite}
.mascot .m-head{transform-origin:300px 200px;animation:mascot-look 9s ease-in-out -3.4s infinite}
.mascot .m-eye{transform-origin:362px 150px;animation:mascot-blink 5.4s linear -2.3s infinite}
.mascot .m-tail{transform-origin:170px 356px;animation:mascot-tailset 11s ease-in-out -5s infinite}
.mascot .m-leg-lift{transform-origin:276px 392px;animation:mascot-foot 7.6s ease-in-out -4.6s infinite}
@keyframes mascot-breathe{0%,100%{transform:scaleY(1)}50%{transform:scaleY(1.013)}}
@keyframes mascot-look{0%,15%{transform:rotate(-1.9deg)}30%,44%{transform:rotate(.5deg)}
58%,80%{transform:rotate(2.2deg)}93%,100%{transform:rotate(-1.9deg)}}
@keyframes mascot-blink{0%,96.8%{transform:scaleY(1)}98.2%{transform:scaleY(.08)}99.6%,100%{transform:scaleY(1)}}
@keyframes mascot-sway{0%,100%{transform:rotate(-1.8deg)}50%{transform:rotate(1.8deg)}}
@keyframes mascot-tailset{0%,100%{transform:rotate(0)}50%{transform:rotate(1.4deg)}}
@keyframes mascot-foot{0%,40%{transform:rotate(0) translateY(0)}58%,72%{transform:rotate(-2.5deg) translateY(-5px)}90%,100%{transform:rotate(0) translateY(0)}}
.mascot.wave .m-wing{transform-origin:296px 240px;animation:mascot-wave-wing 1.2s ease-in-out 1 both}
.mascot.wave .m-head{animation:mascot-wave-head 1.2s cubic-bezier(.34,.09,.2,.98) 1 both}
@keyframes mascot-wave-wing{0%{transform:rotate(0)}22%{transform:rotate(-13deg)}52%{transform:rotate(9deg)}78%{transform:rotate(-6deg)}100%{transform:rotate(0)}}
@keyframes mascot-wave-front{0%{transform:rotate(0)}25%{transform:rotate(-4deg)}60%{transform:rotate(3deg)}100%{transform:rotate(0)}}
@keyframes mascot-wave-head{0%{transform:rotate(0)}18%{transform:rotate(-5deg)}46%{transform:rotate(4deg)}72%{transform:rotate(-3deg)}100%{transform:rotate(0)}}
__POSE__}
.mascot.still *{animation:none!important}
</style>"""


def svg(title, label, body, pose_css="", vb=(0, 0, W, H)):
    style = STYLE.replace("__POSE__", pose_css)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[0]} {vb[1]} '
            f'{vb[2]} {vb[3]}" width="{vb[2]}" height="{vb[3]}" class="mascot" '
            f'role="img" aria-label="{label}">'
            f"<title>{title}</title>{SHEEN_DEF}{style}{body}</svg>")


def place(children, tx=0.0, ty=0.0, sc=1.0):
    """Position a subtree. Never carries an animated class: a CSS transform
    animation would override this transform attribute outright."""
    return g("", children, f'transform="translate({f(tx)} {f(ty)}) '
                           f'scale({f(sc)})"')


def wing_flip(ang):
    """Which side the trailing edge falls on: always the downward one."""
    return 1 if math.cos(math.radians(ang)) >= 0 else -1


def spread_wing(ang, span=190, flip=None, origin=(296, 232), droop=0.0):
    """A spread wing, not the folded one rotated.

    Primaries fan out of the wrist with gaps between the tips, secondaries
    fill the inner trailing edge behind them, the coverts are a short
    shingled band on the leading edge only, and an alula bump sits at the
    wrist. The wing broadens toward the tip because the fan opens.
    `droop` adds degrees to the primary angles so the tips hang.
    """
    fl = wing_flip(ang) if flip is None else flip
    o = origin
    elbow = polar(o, ang - fl * 9, span * 0.26)
    wrist = polar(o, ang - fl * 3, span * 0.48)
    prim_sp, sec_sp = [], []
    for i in range(7):
        t = i / 6
        base = lerp2(wrist, polar(wrist, ang + fl * 128, span * 0.10), t)
        prim_sp.append((base, ang + fl * (lerp(-11, 64, t) + droop),
                        span * lerp(0.62, 0.42, t),
                        span * lerp(0.064, 0.053, t), fl * 6, 0.06))
    for j in range(6):
        t = j / 5
        base = polar(lerp2(elbow, wrist, t), ang + fl * 90, span * 0.035)
        sec_sp.append((base, ang + fl * lerp(107, 81, t),
                       span * lerp(0.25, 0.35, t),
                       span * lerp(0.050, 0.045, t), fl * 4, 0.52))
    prim = [feather(*q) for q in prim_sp]
    sec = [feather(*q) for q in sec_sp]
    bar = taper([o, elbow, wrist], [span * 0.24, span * 0.17, span * 0.115])
    lead0 = polar(o, ang - fl * 90, span * 0.095)
    lead1 = polar(wrist, ang - fl * 90, span * 0.045)
    alula = feather(polar(wrist, ang - fl * 76, span * 0.07),
                    ang + fl * 26, span * 0.20, span * 0.068, fl * 4, 0.62)

    el = []
    for j, d in enumerate(sec):
        el.append(path(d, K1 if j % 2 else "#12161E", EDGE2, 2.4))
    for i, d in enumerate(reversed(prim)):
        el.append(path(d, "#10141B" if i % 2 else "#1B212C", EDGE2, 2.6))
    el.append(path(bar, K1, K0, 2.2))
    for d in row(7, lead0, lead1, ang + fl * 88, ang + fl * 66,
                 span * 0.20, span * 0.155, span * 0.052, span * 0.046,
                 bend=fl * 3, blunt=0.6):
        el.append(path(d, K2, K0, 2.2))
    med = row(7, lead0, lead1, ang + fl * 85, ang + fl * 63,
              span * 0.135, span * 0.105, span * 0.046, span * 0.040,
              bend=fl * 2, blunt=0.75)
    for d in med:
        el.append(path(d, K3, K0, 2.0))
    for d in row(7, lead0, lead1, ang + fl * 85, ang + fl * 63,
                 span * 0.118, span * 0.092, span * 0.040, span * 0.035,
                 bend=fl * 2, blunt=0.75):
        el.append(path(d, "url(#sheen)", None, None, "0.82"))
    for d in row(6, lead0, lead1, ang + fl * 82, ang + fl * 60,
                 span * 0.082, span * 0.066, span * 0.038, span * 0.033,
                 blunt=0.85):
        el.append(path(d, K3, K0, 1.8))
    el.append(path(alula, K3, K0, 2.2))

    halo = g("halo", [path(d) for d in prim + sec] + [path(alula)],
             f'fill="{HALO}" stroke="{HALO}" stroke-width="{f(HALO_W_THIN)}" '
             'stroke-linejoin="round" stroke-linecap="round"')
    # m-spread carries no CSS; it is the marker the wing tally counts.
    return g("m-spread", [halo] + el)


FOLDED = "folded"


def SP(ang, span, droop=0.0, origin=None):
    """A spread wing for one side: angle, span, optional droop and shoulder."""
    return (ang, span, droop, origin)


def wing_state(spec, shoulder):
    """(kind, payload) for one side. kind is FOLDED, "spread" or None.

    A side is drawn EITHER folded OR spread, never both - that is the whole
    point of routing every pose through this.
    """
    if spec is None:
        return (None, None)
    if spec == FOLDED:
        return (FOLDED, None)
    ang, span, droop, origin = spec
    return ("spread", (ang, span, droop, origin or shoulder))


def wing_tip(ang, span=190, origin=(296, 232)):
    """Where the outermost primary lands, for hanging a prop on it."""
    fl = wing_flip(ang)
    return polar(polar(origin, ang - fl * 3, span * 0.48),
                 ang - fl * 13, span * 0.62)


def perch_toes(fx, fy, back=False):
    """Toes curled over an edge."""
    col = K0 if back else K1
    line = "#05070A" if back else K0
    el = [path(taper([(fx - 3, fy - 34), (fx, fy - 10), (fx + 2, fy)],
                     [26, 20, 17]), col)]
    for pts, ws in (([(fx, fy), (fx + 17, fy + 4), (fx + 24, fy + 17)],
                     [17, 12, 7]),
                    ([(fx, fy), (fx + 6, fy + 9), (fx + 8, fy + 20)],
                     [15, 10, 6]),
                    ([(fx, fy), (fx - 14, fy + 5), (fx - 20, fy + 16)],
                     [15, 10, 6])):
        el.append(path(taper(pts, ws), col))
        el.append(path(taper([pts[-1], (pts[-1][0] - 2, pts[-1][1] + 11)],
                             [6, 1.4]), line))
    return el


SHOULDER = (298, 240)


def bird(lift=False, closed=False, brow=False, halo_extra=(), behind=(),
         front=(), wing_extra=(), near=FOLDED, far=None, perch=False,
         no_legs=False, bill=None, tilt=0.0):
    """Assemble the raven.

    `arms` = list of (angle, span, behind?[, droop[, origin]]).
    """
    far_leg, near_leg = leg_shapes(lift)
    if perch:
        far_leg = perch_toes(242, 430, back=True)
        near_leg = perch_toes(286, 434)
    if no_legs:
        far_leg = near_leg = []
    eye = eye_group(closed)[0]
    nk, np_ = wing_state(near, (296, 232))
    fk, fp = wing_state(far, (286, 240))
    el = [anchor(),
          halo_shapes(lift, halo_extra, far_leg + near_leg, bill, tilt,
                      near_folded=(nk == FOLDED), far_folded=(fk == FOLDED),
                      asleep=closed)]
    if fk == "spread":
        el.append(spread_wing(fp[0], fp[1], origin=fp[3], droop=fp[2]))
    elif fk == FOLDED:
        el += far_folded_profile()
    el += list(behind)
    el.append(g("m-tail", [anchor()] + tail_detail()))
    el += far_leg
    el.append(g("m-leg-lift", [anchor()] + near_leg) if lift
              else g("", near_leg))
    el += body_art()
    band, tails, _ = scarf_profile(asleep=closed)
    el += band                     # under the wing's shoulder coverts
    if nk == FOLDED:
        el.append(g("m-wing", [anchor()] + wing_layers() + list(wing_extra)))
    el += tails                    # over the mantle, streaming back
    el += hackles()
    el.append(g("m-head", [anchor()] + rotg(
        head_art(brow, bill) + [g("m-eye", [anchor()] + eye)] + eyelid(),
        tilt)))
    if nk == "spread":
        el.append(spread_wing(np_[0], np_[1], origin=np_[3], droop=np_[2]))
    el += list(front)
    return g("m-body", el)


# ============================================================ three-quarter
# Body angled toward the reader, head turned further so both eyes read. The
# far eye sits at the head's edge with the base of the bill across its lower
# corner; the bill is foreshortened to ~0.75 of its profile length.

SKULL_3Q = ("M200 146C198 106 226 78 270 76C314 74 340 102 342 146"
            "C344 186 320 216 272 218C228 220 202 190 200 146Z")
BILL_3Q = ("M228 150C262 142 300 148 328 162C354 176 374 194 384 208"
           "C388 216 383 223 374 220C369 219 367 214 362 210"
           "C332 199 292 188 264 179C242 172 230 160 228 150Z")
TORSO_3Q = ("M244 184C210 196 186 226 176 264C164 304 168 350 186 384"
            "C204 416 236 432 272 432C310 432 342 410 356 374"
            "C370 336 366 290 352 252C340 218 316 192 292 182Z")
WING_3Q_NEAR = ("M342 214C360 246 368 296 362 338C356 378 336 410 306 424"
                "L280 406C308 384 328 338 332 292C336 250 340 226 342 214Z")
WING_3Q_FAR = ("M192 278C178 312 170 354 166 390L190 396C200 360 208 316 212 286Z")
TAIL_3Q = ("M228 384C200 406 160 434 126 454L146 474C184 460 220 438 242 416Z")
EYE_3Q_NEAR = (306, 136)
EYE_3Q_FAR = (222, 148)

# A fledgling: stubby bill, a pale gape flange, a wider gape. Young corvids
# sit with the bill slightly open and the gape skin still pale.
BILL_3Q_JUV = ("M232 154C258 148 284 153 302 163C318 172 330 183 336 192"
               "C339 198 334 203 327 200C308 192 282 185 260 178"
               "C244 172 234 162 232 154Z")
TAIL_3Q_JUV = ("M226 388C208 402 186 420 166 434L180 450C204 440 224 426 238 412Z")

HACKLE_3Q = [((222, 208), 102, 62), ((244, 218), 96, 80), ((268, 224), 90, 64),
             ((298, 222), 84, 78), ((322, 212), 78, 60)]


def hackle_3q_paths(juv=False):
    k, w, bl = (1.22, 19, 0.45) if juv else (1.0, 15, 0.0)
    return [feather(b, a, ln * k * jitter(i, 0.24), w - (i % 2) * 3, 2, bl)
            for i, (b, a, ln) in enumerate(HACKLE_3Q)]


def foot(fx, fy, toes, back=False):
    """A foot: `toes` is a list of (angle, length). Three forward plus the
    hallux, each with scute bands and a claw."""
    col = K0 if back else K1
    line = "#05070A" if back else K0
    band = "#0A0D12" if back else "#242C3A"
    el = []
    for ang, ln in toes:
        tip = polar((fx, fy), ang, ln)
        mid = polar((fx, fy), ang - 5, ln * 0.55)
        w = 17 if ln > 34 else 15
        el.append(path(taper([(fx, fy), mid, tip], [w, w * 0.68, w * 0.42]), col))
        for t in (0.34, 0.6, 0.84):
            q = polar((fx, fy), ang - 3, ln * t)
            hw = w * 0.5 * (1 - t * 0.4)
            el.append(path(taper([polar(q, ang + 90, hw), polar(q, ang - 90, hw)],
                                 [2.4, 2.4]), band, None, None, "0.85"))
        el.append(path(taper([tip, polar(tip, ang + 18, 13)], [6.4, 1.3]), line))
    return el


def legs_3q(lift=False, juv=False):
    def one(ax, ay, fx, fy, back, toes):
        col = K0 if back else K1
        line = "#05070A" if back else K0
        el = [path(taper([(ax, ay), ((ax + fx) / 2 + 2, (ay + fy) / 2),
                          (fx, fy)], [27, 21, 17]), col)]
        for t in (0.34, 0.56, 0.78, 0.92):
            q = lerp2((ax, ay), (fx, fy), t)
            el.append(path(taper([(q[0] - 9, q[1] - 1), (q[0] + 9, q[1] - 2)],
                                 [3.2, 3.2]), line, None, None, "0.9"))
        return el + foot(fx, fy, toes, back=back)
    if juv:
        far = one(228, 424, 220, 460, True,
                  [(16, 36), (54, 26), (150, 28)])
        near = one(296, 426, 302, 464, False,
                   [(0, 42), (38, 34), (80, 24), (174, 32)])
        return far, near
    far = one(228, 402, 218, 460, True,
              [(14, 44), (50, 34), (96, 24), (152, 34)])
    near = one(298, 404, 306, 464, False,
               [(0, 52), (38, 42), (84, 28), (174, 38)])
    return far, near


def head_3q(brow=False, juv=False, simple=False):
    bill = BILL_3Q_JUV if juv else BILL_3Q
    el = [] if juv else braids_3q(simple)[0]
    el.append(path(SKULL_3Q, K1))
    el.append(path("M202 142C202 104 230 80 270 78C312 76 338 100 341 140"
                   "C310 110 238 112 208 138C205 141 203 142 202 142Z", K3))
    el.append(path("M209 128C214 102 238 86 270 84C302 82 328 96 336 120"
                   "C306 96 240 102 213 126C211 128 210 128 209 128Z",
                   "url(#sheen)", None, None, "0.7"))
    el.append(path("M312 160C322 158 332 161 336 167C330 176 318 178 310 174"
                   "C305 171 307 162 312 160Z", "#3A4559", None, None, "0.5"))
    # bill: one wedge, a lit far facet, a dark lower mandible, a culmen ridge
    el.append(path(bill, "#1B212C", K0, 2.4))
    if juv:
        el.append(path("M232 152C260 146 288 152 310 164C288 156 258 154 240 158Z",
                       K3, None, None, "0.5"))
        # the bill held slightly open, with the pale gape flange of a fledgling
        el.append(path("M240 168C266 178 300 190 328 199C332 201 334 204 332 206"
                       "C304 199 268 187 244 177Z", K0))
        el.append(path("M236 157C268 160 306 176 330 194", None, K3, 2.4, "0.5"))
        el.append(path("M238 162C264 168 296 180 320 192", None, "#6B7689",
                       3.2, "0.75", 'stroke-linecap="round"'))
        el.append(path("M250 176C272 186 300 196 322 202", None, "#6B7689",
                       3.0, "0.6", 'stroke-linecap="round"'))
    else:
        el.append(path("M232 152C264 144 302 150 326 163C300 155 262 154 240 158Z",
                       K3, None, None, "0.5"))
        el.append(path("M242 166C272 177 314 191 348 206C364 213 372 217 377 214"
                       "C381 220 374 225 366 221C334 210 288 195 254 181Z", K0))
        el.append(path("M236 157C276 159 326 178 372 209", None, K3, 2.4, "0.5"))
    for i in range(4 if juv else 5):
        t = i / 4
        b = (240 + t * 24, 148 + t * 7)
        el.append(path(taper([b, polar(b, 14 + t * 10,
                                       (22 if juv else 32) + t * 12)],
                             [4.6, 1.0]), K3, None, None, "0.8"))
    # gape: under the near side of the bill, hooked up at the hinge
    el.append(path("M256 180C274 191 294 199 310 200C319 200 325 195 327 187"
                   if juv else
                   "M256 180C278 194 302 204 320 204C330 204 337 198 339 189",
                   None, K0, 2.8, None, 'stroke-linecap="round"'))
    if brow:
        el.append(path(taper([(290, 110), (330, 122)], [10, 5]), K0))
        el.append(path(taper([(206, 122), (242, 110)], [7, 4]), K0))
    return el


def eyes_3q(closed=False, k=1.0):
    """A fledgling's eye is larger relative to its head - pass k."""
    el = eye_group(closed, 11.0 * k, EYE_3Q_FAR, 0.75)[0]
    el += eye_group(closed, 19.0 * k, EYE_3Q_NEAR)[0]
    return el


def body_3q():
    el = [path(TORSO_3Q, K1)]
    el.append(path("M246 192C216 206 194 240 186 276C180 304 180 334 186 358"
                   "C188 320 198 278 216 246C228 224 240 204 246 192Z", K2))
    el.append(path("M296 196C320 220 338 262 342 306C346 348 340 384 322 406"
                   "C332 374 336 334 332 294C328 250 314 216 296 196Z", K3,
                   None, None, "0.6"))
    for b0, b1, n, ln in (((230, 302), (306, 290), 4, 44),
                          ((224, 350), (308, 340), 4, 42),
                          ((230, 396), (306, 388), 4, 38)):
        for d in row(n, b0, b1, 104, 76, ln, ln - 3, 20, 19, blunt=0.88):
            el.append(path(d, K1, EDGE, 1.8, "0.3"))
    return el


def wing_3q_far():
    """The far wing, folded: only the sliver that clears the body."""
    el = [path(WING_3Q_FAR, K0)]
    for i, sp in enumerate(row_specs(4, (180, 386), (202, 312), 118, 100,
                                     80, 70, 16, 15, bend=4, blunt=0.05)):
        el += long_feather(*sp, "#10141B" if i % 2 else "#171C25", EDGE2, 2.2,
                           barbs=2)
    return el


def wing_3q_near():
    """Seen near edge-on, so the wing is a dark mass: primaries at the tip and
    a short covert patch at the shoulder. Full rows compress into stripes."""
    el = [path(WING_3Q_NEAR, K0)]
    for i, sp in enumerate(row_specs(5, (298, 416), (336, 314), 110, 90,
                                     116, 98, 20, 19, bend=5, blunt=0.05)):
        el += long_feather(*sp, "#10141B" if i % 2 else "#1B212C", EDGE2, 2.4)
    for i, sp in enumerate(row_specs(4, (306, 336), (332, 272), 104, 88,
                                     64, 58, 18, 17, bend=4, blunt=0.5)):
        el += long_feather(*sp, K1 if i % 2 else "#12161E", EDGE2, 2.4,
                           barbs=2)
    el += shingle(row_specs(4, (312, 292), (334, 240), 100, 86, 44, 40,
                            17, 16, bend=3, blunt=0.66), "#333D50", K2, K0, 2.2)
    el += shingle(row_specs(4, (316, 272), (334, 226), 98, 84, 32, 29,
                            15, 14, bend=2, blunt=0.8), "#46536C", K3, K0, 2.0)
    for d in row(4, (316, 272), (334, 226), 98, 84, 25, 23, 12, 11,
                 bend=2, blunt=0.8):
        el.append(path(d, "url(#sheen)", None, None, "0.85"))
    return el


def tail_3q(d0=None):
    el = [path(d0 or TAIL_3Q, K0)]
    for i, sp in enumerate(row_specs(5, (240, 412), (222, 388), 158, 142,
                                     102, 118, 15, 16, bend=3, blunt=0.06)):
        el += long_feather(*sp, "#191F29" if i % 2 else "#0F131A", EDGE2, 2.3)
    return el


SH_3Q_NEAR = (338, 218)
SH_3Q_FAR = (198, 234)


def bird_3q(closed=False, brow=False, tilt=4.0, near=FOLDED, far=FOLDED,
            halo_extra=(), behind=(), front=(), no_legs=False, juv=False):
    """`juv` is the fledgling: bigger head, stubby bill, bigger eye, fluffier
    ruff, shorter tail, stubbier legs."""
    bill3q = BILL_3Q_JUV if juv else BILL_3Q
    tail3q = TAIL_3Q_JUV if juv else TAIL_3Q
    hsc = 1.16 if juv else 1.0
    far_leg, near_leg = legs_3q(juv=juv)
    if no_legs:
        far_leg = near_leg = []
    nk, np_ = wing_state(near, SH_3Q_NEAR)
    fk, fp = wing_state(far, SH_3Q_FAR)
    sil = [path(d) for d in (tail3q, TORSO_3Q)]
    if nk == FOLDED:
        sil.append(path(WING_3Q_NEAR))
    if fk == FOLDED:
        sil.append(path(WING_3Q_FAR))
    sil += rotg([path(SKULL_3Q), path(bill3q)], tilt, sc=hsc)
    sil += [path(d) for d in hackle_3q_paths(juv)]
    sil += [path(d) for d in halo_extra]
    band, tails, cue_halo = ([], [], []) if juv else scarf_3q()
    cue_halo = [path(d) for d in cue_halo]
    if not juv:
        cue_halo += rotg([path(d) for d in braids_3q()[1]], tilt, sc=hsc)
    el = [anchor(),
          g("halo", far_leg + near_leg + cue_halo,
            f'fill="{HALO}" stroke="{HALO}" stroke-width="5" '
            'stroke-linejoin="round" stroke-linecap="round"'),
          g("halo", sil,
            f'fill="{HALO}" stroke="{HALO}" stroke-width="{f(HALO_W)}" '
            'stroke-linejoin="round" stroke-linecap="round"')]
    if fk == "spread":
        el.append(spread_wing(fp[0], fp[1], origin=fp[3], droop=fp[2]))
    el += list(behind)
    el.append(g("m-tail", [anchor()] + tail_3q(tail3q)))
    el += far_leg + near_leg + body_3q()
    wing_el = []
    if fk == FOLDED:
        wing_el += wing_3q_far()
    if nk == FOLDED:
        wing_el += wing_3q_near()
    if wing_el:
        el.append(g("m-wing", [anchor()] + wing_el))
    for i, d in enumerate(hackle_3q_paths(juv)):
        el.append(path(d, "#3B465C" if i % 2 else K2, EDGE, 2.4))
    el += band + tails             # over the ruff; its points spill out below
    ek = 1.2 if juv else 1.0
    el.append(g("m-head", [anchor()] + rotg(
        head_3q(brow, juv) + [g("m-eye", [anchor()] + eyes_3q(closed, ek))]
        + eyelid(EYE_3Q_FAR, 11.0 * ek) + eyelid(EYE_3Q_NEAR, 19.0 * ek),
        tilt, sc=hsc)))
    if nk == "spread":
        el.append(spread_wing(np_[0], np_[1], origin=np_[3], droop=np_[2]))
    el += list(front)
    return g("m-body", el)


# ================================================================= front view
# Symmetric: chest and both shoulders square to the reader, bill pointing at
# the viewer with the bristles as a tuft, feet splayed.

# Not quite symmetric: about ten degrees of yaw toward the reader's right, so
# the bird stops being a blob while still reading as facing you. The far side
# of the face is compressed, the far eye is smaller and nearer the edge, and
# the bird's left shoulder sits marginally forward.
SKULL_FR = ("M174 144C174 100 212 74 259 74C304 74 338 100 338 146"
            "C338 190 306 220 256 220C204 220 174 188 174 144Z")
BILL_FR = ("M263 142C287 146 301 158 303 178C305 208 286 236 262 254"
           "C238 236 221 208 223 178C225 158 239 146 263 142Z")
TORSO_FR = ("M258 186C212 188 180 218 168 264C156 310 160 358 180 392"
            "C198 422 226 434 256 434C288 434 316 422 334 390"
            "C354 354 358 306 346 262C334 216 304 184 258 186Z")
EYE_FR_L = (208, 136)
EYE_FR_R = (304, 132)

HACKLE_FR = [((192, 206), 106, 62), ((214, 220), 100, 82), ((240, 228), 94, 68),
             ((280, 226), 86, 66), ((304, 216), 80, 78), ((324, 204), 74, 58)]


def hackle_fr_paths():
    return [feather(b, a, ln * jitter(i, 0.2), 15 - (i % 2) * 3, 0, 0.0)
            for i, (b, a, ln) in enumerate(HACKLE_FR)]


def head_front(brow=False):
    el = braids_front()[0]
    el.append(path(SKULL_FR, K1))
    el.append(path("M176 140C176 98 212 76 259 76C304 76 337 100 337 142"
                   "C302 108 212 108 176 140Z", K3))
    el.append(path("M184 130C188 98 222 82 259 82C296 82 326 98 330 130"
                   "C298 102 216 102 184 130Z", "url(#sheen)", None, None, "0.72"))
    for cx in (188, 324):
        el.append(path(f"M{f(cx-10)} {f(166)}C{f(cx-2)} {f(163)} {f(cx+6)} "
                       f"{f(165)} {f(cx+10)} {f(170)}C{f(cx+4)} {f(177)} "
                       f"{f(cx-6)} {f(178)} {f(cx-11)} {f(175)}"
                       f"C{f(cx-14)} {f(173)} {f(cx-13)} {f(168)} "
                       f"{f(cx-10)} {f(166)}Z", "#3A4559", None, None, "0.45"))
    el.append(path(BILL_FR, "#1B212C", K0, 2.4))
    el.append(path("M263 142C239 146 225 158 223 178C221 208 238 236 262 254"
                   "C250 232 242 206 242 178C242 160 251 148 263 142Z",
                   "#11151C"))
    el.append(path("M263 144L261 250", None, K3, 2.8, "0.5"))
    el.append(path("M239 222C247 238 256 250 262 255C268 250 278 238 286 222"
                   "C282 242 270 256 262 262C254 256 243 242 239 222Z", K0))
    for i in range(6):
        t = i / 5
        sgn = -1 if i % 2 else 1
        b = (263 + sgn * (4 + t * 7), 150 + t * 5)
        el.append(path(taper([b, polar(b, 90 + sgn * (30 + t * 22), 30 + t * 12)],
                             [4.6, 1.0]), K3, None, None, "0.8"))
    el.append(path("M200 176C204 195 219 209 240 213", None, K0, 2.8, None,
                   'stroke-linecap="round"'))
    el.append(path("M318 174C314 192 301 206 282 211", None, K0, 2.8, None,
                   'stroke-linecap="round"'))
    if brow:
        el.append(path(taper([(182, 116), (224, 106)], [10, 5]), K0))
        el.append(path(taper([(330, 116), (288, 106)], [10, 5]), K0))
    return el


def eyes_front(closed=False):
    return eye_group(closed, 20.0, EYE_FR_L)[0] + \
        eye_group(closed, 17.0, EYE_FR_R, 0.85)[0]


def legs_front(lift=False):
    def one(ax, fx, toes):
        el = [path(taper([(ax, 408), (ax, 436), (fx, 462)], [29, 24, 20]), K1)]
        for t in (0.36, 0.58, 0.8):
            q = lerp2((ax, 408), (fx, 462), t)
            el.append(path(taper([(q[0] - 9, q[1]), (q[0] + 9, q[1] - 1)],
                                 [3.2, 3.2]), K0, None, None, "0.9"))
        return el + foot(fx, 462, toes)
    return (one(230, 226, [(134, 28), (90, 26), (46, 28)]),
            one(284, 288, [(46, 28), (90, 26), (134, 28)]))


def body_front():
    el = [path(TORSO_FR, K1)]
    el.append(path("M256 196C284 200 306 224 316 260C326 296 326 342 314 378"
                   "C322 340 322 292 310 256C300 222 280 202 256 196Z", K2))
    el.append(path("M256 214C236 232 226 276 226 318C226 358 234 392 248 414"
                   "C236 396 226 360 224 318C222 274 234 234 256 214Z", K3,
                   None, None, "0.55"))
    for y, n in ((296, 4), (344, 4), (390, 4)):
        for d in row(n, (212, y), (300, y - 6), 98, 82, 46, 42, 21, 20,
                     blunt=0.9):
            el.append(path(d, K1, EDGE, 1.6, "0.2"))
    return el


WING_FR_ENV = {
    -1: ("M184 222C167 254 161 310 167 358C173 400 196 428 234 434"
         "L286 416C244 414 198 388 192 330C186 274 186 242 184 222Z"),
    1: ("M332 216C351 250 357 310 351 360C345 402 320 430 280 436"
        "L224 416C270 414 318 388 324 328C330 270 332 236 332 216Z"),
}


def wing_front(sgn):
    """One flank wing, folded. `sgn` -1 is the reader's left."""
    el = []
    ox = 188 if sgn < 0 else 324
    if True:
        el.append(path(WING_FR_ENV[sgn], K0))
        for i, sp in enumerate(row_specs(5, (ox - sgn * 30, 388),
                                         (ox + sgn * 4, 262), 90 - sgn * 44,
                                         90 - sgn * 8, 120, 112, 17, 18,
                                         bend=sgn * 5, blunt=0.05)):
            el += long_feather(*sp, "#10141B" if i % 2 else "#1B212C",
                               EDGE2, 2.4)
        for i, sp in enumerate(row_specs(4, (ox - sgn * 12, 316),
                                         (ox + sgn * 8, 258), 90 - sgn * 20,
                                         90 - sgn * 4, 54, 58, 16, 17,
                                         bend=sgn * 3, blunt=0.55)):
            el += long_feather(*sp, K1, EDGE2, 2.2, barbs=2)
        el += shingle(row_specs(3, (ox - sgn * 2, 282), (ox + sgn * 10, 240),
                                90 - sgn * 16, 90 - sgn * 2, 40, 42, 15, 16,
                                bend=sgn * 2, blunt=0.72),
                      "#333D50", K2, K0, 2.0)
        el += shingle(row_specs(3, (ox + sgn * 2, 264), (ox + sgn * 12, 232),
                                90 - sgn * 14, 90, 28, 30, 13, 14,
                                bend=sgn * 2, blunt=0.82),
                      "#46536C", K3, K0, 1.8)
        for d in row(3, (ox + sgn * 2, 264), (ox + sgn * 12, 232),
                     90 - sgn * 14, 90, 22, 24, 10, 11, bend=sgn * 2,
                     blunt=0.82):
            el.append(path(d, "url(#sheen)", None, None, "0.85"))
    return el


TAIL_FR = ("M246 396C220 414 190 438 162 456L180 474C212 460 244 440 264 422Z")


SH_FR_LEFT = (192, 230)
SH_FR_RIGHT = (320, 230)


def bird_front(closed=False, brow=False, left=FOLDED, right=FOLDED,
               halo_extra=(), behind=(), front=(), no_legs=False):
    a, b = legs_front()
    legs_el = [] if no_legs else a + b
    lk, lp = wing_state(left, SH_FR_LEFT)
    rk, rp = wing_state(right, SH_FR_RIGHT)
    sil = [path(d) for d in (TAIL_FR, TORSO_FR, SKULL_FR, BILL_FR)]
    if lk == FOLDED:
        sil.append(path(WING_FR_ENV[-1]))
    if rk == FOLDED:
        sil.append(path(WING_FR_ENV[1]))
    sil += [path(d) for d in hackle_fr_paths()] + [path(d) for d in halo_extra]
    band, tails, cue_halo = scarf_front()
    cue_halo = [path(d) for d in cue_halo + braids_front()[1]]
    el = [anchor(),
          g("halo", legs_el + cue_halo,
            f'fill="{HALO}" stroke="{HALO}" stroke-width="5" '
            'stroke-linejoin="round" stroke-linecap="round"'),
          g("halo", sil,
            f'fill="{HALO}" stroke="{HALO}" stroke-width="{f(HALO_W)}" '
            'stroke-linejoin="round" stroke-linecap="round"')]
    for k, q in ((lk, lp), (rk, rp)):
        if k == "spread":
            el.append(spread_wing(q[0], q[1], origin=q[3], droop=q[2]))
    el += list(behind)
    el.append(g("m-tail", [anchor(), path(TAIL_FR, K0)] +
                sum([long_feather(*sp, "#191F29" if i % 2 else "#0F131A",
                                  EDGE2, 2.3)
                     for i, sp in enumerate(
                         row_specs(4, (250, 414), (238, 394), 160, 146, 88,
                                   100, 14, 15, bend=3, blunt=0.06))], [])))
    el += legs_el + body_front()
    wing_el = []
    if lk == FOLDED:
        wing_el += wing_front(-1)
    if rk == FOLDED:
        wing_el += wing_front(1)
    if wing_el:
        el.append(g("m-wing", [anchor()] + wing_el))
    for i, d in enumerate(hackle_fr_paths()):
        el.append(path(d, "#3B465C" if i % 2 else K2, EDGE, 2.4))
    el += band + tails
    el.append(g("m-head", [anchor()] + head_front(brow)
                + [g("m-eye", [anchor()] + eyes_front(closed))]
                + eyelid(EYE_FR_L, 20.0) + eyelid(EYE_FR_R, 17.0)))
    el += list(front)
    return g("m-body", el)


VIEW_CSS = {
    "3q": (".mascot .m-head{transform-origin:268px 214px}"
           ".mascot .m-eye{transform-origin:268px 148px}"
           ".mascot .m-tail{transform-origin:222px 400px}"),
    "front": (".mascot .m-head{transform-origin:256px 208px;"
              "animation:mascot-sway 10s ease-in-out -2.2s infinite}"
              ".mascot .m-eye{transform-origin:256px 145px}"
              ".mascot .m-tail{transform-origin:256px 400px;animation:none}"
              ".mascot.wave .m-wing{transform-origin:256px 250px;"
              "animation:mascot-wave-front 1.2s ease-in-out 1 both}"),
}


# ---------------------------------------------------------------- props
def spool(cx, cy, r=76, band=BLUE):
    """Filament spool, side on: two flanges, a wound band, three lightening holes."""
    el = [circle((cx, cy), r, GREYF), circle((cx, cy), r, "none")]
    el = [path(f"M{f(cx-r)} {f(cy)}A{f(r)} {f(r)} 0 1 0 {f(cx+r)} {f(cy)}"
               f"A{f(r)} {f(r)} 0 1 0 {f(cx-r)} {f(cy)}Z", GREYF, GREY, 4)]
    el.append(circle((cx, cy), r * 0.68, band))
    el.append(circle((cx, cy), r * 0.68, "#FFFFFF", "0.08"))
    el.append(circle((cx, cy), r * 0.3, GREYF))
    el.append(circle((cx, cy), r * 0.3, "none"))
    el.append(path(f"M{f(cx-r*0.3)} {f(cy)}A{f(r*0.3)} {f(r*0.3)} 0 1 0 "
                   f"{f(cx+r*0.3)} {f(cy)}A{f(r*0.3)} {f(r*0.3)} 0 1 0 "
                   f"{f(cx-r*0.3)} {f(cy)}Z", GREYF, GREY, 4))
    el.append(circle((cx, cy), r * 0.13, GREY))
    for a in (30, 150, 270):
        el.append(circle(polar((cx, cy), a, r * 0.48), r * 0.09, GREY, "0.55"))
    return el


def tray(x, y, w=132, h=34, screws=6):
    """A shallow parts tray seen from slightly above, with screws in it."""
    el = [path(f"M{f(x)} {f(y)}L{f(x+w)} {f(y)}L{f(x+w-14)} {f(y+h)}"
               f"L{f(x+14)} {f(y+h)}Z", GREY, GREYF, 5,
               extra='stroke-linejoin="round"'),
          path(f"M{f(x+9)} {f(y+5)}L{f(x+w-9)} {f(y+5)}L{f(x+w-18)} {f(y+h-6)}"
               f"L{f(x+18)} {f(y+h-6)}Z", "#434C5C")]
    for i in range(screws):
        t = (i + 0.5) / screws
        sx = x + 20 + t * (w - 40)
        sy = y + 11 + (7 if i % 2 else 0)
        el.append(circle((sx, sy), 9, STEEL, None, GREY, 2))
        hexp = [polar((sx, sy), 30 + k * 60, 4.4) for k in range(6)]
        el.append(path("M" + "L".join(pt(q) for q in hexp) + "Z", "#434C5C"))
    return el


def magnifier(cx, cy, r=52, ang=52, grip=None):
    el = [circle((cx, cy), r, BLUEF, "0.4"),
          path(f"M{f(cx-r)} {f(cy)}A{f(r)} {f(r)} 0 1 0 {f(cx+r)} {f(cy)}"
               f"A{f(r)} {f(r)} 0 1 0 {f(cx-r)} {f(cy)}Z", "none", STEEL, 11),
          path(f"M{f(cx-r*0.55)} {f(cy-r*0.4)}A{f(r*0.8)} {f(r*0.8)} 0 0 1 "
               f"{f(cx-r*0.05)} {f(cy-r*0.72)}", "none", HALO, 6, "0.55")]
    el.append(path(f"M{f(cx-r*0.82)} {f(cy)}A{f(r*0.82)} {f(r*0.82)} 0 1 0 "
                   f"{f(cx+r*0.82)} {f(cy)}A{f(r*0.82)} {f(r*0.82)} 0 1 0 "
                   f"{f(cx-r*0.82)} {f(cy)}Z", "none", GREYF, 3, "0.8"))
    h0 = polar((cx, cy), ang, r + 4)
    h1 = polar((cx, cy), ang, r + 58)
    el.append(path(taper([h0, h1], [20, 22]), GREY))
    for i in range(5):
        q0 = polar((cx, cy), ang, r + 16 + i * 6)
        el.append(path(taper([polar(q0, ang + 90, 9), polar(q0, ang - 90, 9)],
                             [2.6, 2.6]), "#434C5C", None, None, "0.9"))
    el.append(path(taper([polar((cx, cy), ang, r + 44),
                          polar((cx, cy), ang, r + 58)], [20, 22]), "#434C5C"))
    if grip is not None:
        # three primary tips curled across the grip, so the wing holds it
        gp = polar((cx, cy), ang, grip)
        for k in range(3):
            q = polar(gp, ang, -14 + k * 14)
            a0 = polar(q, ang + 90, 20)
            a1 = polar(q, ang - 90, 18)
            el.append(path(feather(a0, ang - 90, 38, 8.5, 3, 0.35),
                           K1 if k % 2 else K2, EDGE2, 2.2))
            el.append(path(taper([a1, polar(a1, ang - 90, -9)], [7, 3]), K0,
                           None, None, "0.8"))
    return el


def caliper(x, y, ang=-24):
    """Digital caliper: beam, fixed and sliding jaw, a blue readout."""
    c = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    def P(u, v):
        return (x + u * c[0] - v * c[1], y + u * c[1] + v * c[0])
    el = [path(f"M{pt(P(0,0))}L{pt(P(176,0))}L{pt(P(176,17))}L{pt(P(0,17))}Z",
               STEEL, GREY, 5, extra='stroke-linejoin="round"'),
          path(f"M{pt(P(2,0))}L{pt(P(20,0))}L{pt(P(20,-54))}L{pt(P(9,-54))}Z",
               STEEL, GREY, 5, extra='stroke-linejoin="round"'),
          path(f"M{pt(P(62,0))}L{pt(P(80,0))}L{pt(P(71,-54))}L{pt(P(62,-54))}Z",
               STEEL, GREY, 5, extra='stroke-linejoin="round"'),
          path(f"M{pt(P(62,17))}L{pt(P(140,17))}L{pt(P(140,62))}L{pt(P(62,62))}Z",
               GREYF, GREY, 5, extra='stroke-linejoin="round"'),
          path(f"M{pt(P(74,28))}L{pt(P(128,28))}L{pt(P(128,51))}L{pt(P(74,51))}Z",
               BLUE),
          path(f"M{pt(P(146,17))}L{pt(P(164,17))}L{pt(P(164,40))}L{pt(P(146,40))}Z",
               GREY)]
    for i in range(13):
        u = 8 + i * 12
        v = 4 if i % 5 else 9
        el.append(path(f"M{pt(P(u,2))}L{pt(P(u,2+v))}", "none", GREY, 2.2,
                       "0.9"))
    el.append(path(f"M{pt(P(66,20))}L{pt(P(66,26))}", "none", GREYF, 2.4))
    return el


def tick(cx, cy, s=1.0):
    return [path(taper([(cx - 30 * s, cy - 2 * s), (cx - 8 * s, cy + 22 * s),
                        (cx + 34 * s, cy - 32 * s)],
                       [17 * s, 19 * s, 12 * s]), GREEN)]


def nightcap():
    """A slouched cap over the crown, blue with a pale band and bobble."""
    return [path("M292 150C296 112 322 92 356 94C386 96 404 116 406 136"
                 "C384 122 342 120 316 136C304 143 296 147 292 150Z", BLUE),
            path("M292 150C296 112 322 92 356 94C368 95 378 99 386 106"
                 "C352 100 314 118 300 146C296 149 294 150 292 150Z",
                 "#3D8BD6"),
            path("M300 140C284 120 268 104 252 100C241 97 234 105 238 116"
                 "C245 131 268 144 290 150Z", BLUE),
            path("M290 152C296 132 300 122 306 112C336 100 380 104 404 122"
                 "C410 130 412 140 410 148C378 130 324 132 290 152Z", BLUEF),
            path(taper([(244, 106), (224, 124), (215, 150), (218, 174)],
                       [10, 9, 8, 7]), BLUEF),
            circle((216, 196), 23, BLUEF),
            circle((216, 196), 23, "none", None, BLUE, 3)] + [
                path(taper([polar((216, 196), a, 17), polar((216, 196), a, 26)],
                           [9, 5]), BLUEF)
                for a in range(30, 360, 45)]


def hardhat():
    """An amber hard hat: dome, crest rib, brim over the bill base."""
    return [g("", [
        path("M286 148C288 108 316 84 352 86C388 88 410 114 412 150"
             "C380 132 318 130 286 148Z", AMBER),
        path("M330 90C344 86 362 86 376 90C374 112 372 130 372 144"
             "C360 140 344 138 332 140C332 124 332 106 330 90Z", AMBERF,
             None, None, "0.55"),
        path("M278 150C286 142 306 134 330 131C358 127 392 132 418 146"
             "C424 150 424 158 416 160C380 146 322 144 282 160"
             "C275 162 272 155 278 150Z", AMBER),
        path("M282 160C322 144 380 146 416 160C418 163 416 166 410 166"
             "C376 154 324 154 288 166C283 167 280 164 282 160Z", "#B96A18")],
        'transform="translate(0 -34)"')]


def bulb(cx, cy, r=36):
    el = []
    for a in range(0, 360, 45):
        p0 = polar((cx, cy), a, r + 14)
        p1 = polar((cx, cy), a, r + 30)
        el.append(path(taper([p0, p1], [8, 3]), BLUEF, None, None, "0.85"))
    el.append(circle((cx, cy), r, BLUEF))
    el.append(circle((cx, cy), r, "none"))
    el.append(path(f"M{f(cx-r)} {f(cy)}A{f(r)} {f(r)} 0 1 0 {f(cx+r)} {f(cy)}"
                   f"A{f(r)} {f(r)} 0 1 0 {f(cx-r)} {f(cy)}Z", BLUEF, STEEL, 5))
    el.append(path(f"M{f(cx-16)} {f(cy+14)}L{f(cx-16)} {f(cy-2)}"
                   f"C{f(cx-16)} {f(cy-16)} {f(cx+16)} {f(cy-16)} "
                   f"{f(cx+16)} {f(cy-2)}L{f(cx+16)} {f(cy+14)}",
                   "none", BLUE, 6,
                   extra='stroke-linejoin="round" stroke-linecap="round"'))
    el.append(path(f"M{f(cx-15)} {f(cy+r-6)}L{f(cx+15)} {f(cy+r-6)}"
                   f"L{f(cx+12)} {f(cy+r+16)}L{f(cx-12)} {f(cy+r+16)}Z",
                   STEEL, GREY, 4, extra='stroke-linejoin="round"'))
    for dy in (0, 8):
        el.append(path(taper([(cx - 13, cy + r + 1 + dy),
                              (cx + 13, cy + r + 1 + dy)], [3.4, 3.4]), GREY))
    return el


def zmark(cx, cy, s=1.0, op="0.9"):
    w, h = 26 * s, 26 * s
    return path(f"M{f(cx)} {f(cy)}L{f(cx+w)} {f(cy)}L{f(cx)} {f(cy+h)}"
                f"L{f(cx+w)} {f(cy+h)}", "none", STEEL, 7 * s, op,
                'stroke-linejoin="round" stroke-linecap="round"')


def printer(x, y, w=260, h=214):
    """The Core One, front on: steel body, blue-framed window, a first layer."""
    el = [path(f"M{f(x)} {f(y)}L{f(x+w)} {f(y)}L{f(x+w)} {f(y+h)}"
               f"L{f(x)} {f(y+h)}Z", GREY, GREYF, 6,
               extra='stroke-linejoin="round"'),
          path(f"M{f(x)} {f(y)}L{f(x+w)} {f(y)}L{f(x+w)} {f(y+16)}"
               f"L{f(x)} {f(y+16)}Z", GREYF),
          path(f"M{f(x+22)} {f(y+34)}L{f(x+w-22)} {f(y+34)}"
               f"L{f(x+w-22)} {f(y+h-40)}L{f(x+22)} {f(y+h-40)}Z", "#1B2029",
               BLUE, 8, extra='stroke-linejoin="round"'),
          path(f"M{f(x+30)} {f(y+42)}L{f(x+96)} {f(y+42)}"
               f"L{f(x+30)} {f(y+h-70)}Z", BLUEF, None, None, "0.18")]
    bx, by, bw = x + 44, y + h - 70, w - 88
    el.append(path(f"M{f(bx)} {f(by)}L{f(bx+bw)} {f(by)}L{f(bx+bw)} {f(by+13)}"
                   f"L{f(bx)} {f(by+13)}Z", STEEL))
    el.append(g("m-layer", [anchor(),
                            path(f"M{f(bx+8)} {f(by-6)}L{f(bx+bw-8)} {f(by-6)}",
                                 "none", BLUE, 8, None,
                                 'stroke-linecap="round"')]))
    el.append(path(f"M{f(x+w-74)} {f(y+h-28)}L{f(x+w-22)} {f(y+h-28)}"
                   f"L{f(x+w-22)} {f(y+h-10)}L{f(x+w-74)} {f(y+h-10)}Z", BLUE))
    el.append(circle((x + 30, y + h - 19), 8, GREYF))
    return el


def carton(x, y, w=280, h=150):
    """An open shipping carton: grey board, a blue label, two raised flaps."""
    el = [path(f"M{f(x-26)} {f(y-6)}L{f(x+52)} {f(y-52)}L{f(x+62)} {f(y-40)}"
               f"L{f(x-8)} {f(y+8)}Z", STEEL, GREY, 5,
               extra='stroke-linejoin="round"'),
          path(f"M{f(x+w+26)} {f(y-6)}L{f(x+w-52)} {f(y-52)}"
               f"L{f(x+w-62)} {f(y-40)}L{f(x+w+8)} {f(y+8)}Z", STEEL, GREY, 5,
               extra='stroke-linejoin="round"'),
          path(f"M{f(x)} {f(y)}L{f(x+w)} {f(y)}L{f(x+w)} {f(y+h)}"
               f"L{f(x)} {f(y+h)}Z", STEEL, GREY, 6,
               extra='stroke-linejoin="round"'),
          path(f"M{f(x)} {f(y)}L{f(x+w)} {f(y)}L{f(x+w)} {f(y+16)}"
               f"L{f(x)} {f(y+16)}Z", GREYF),
          path(f"M{f(x+w/2-58)} {f(y+46)}L{f(x+w/2+58)} {f(y+46)}"
               f"L{f(x+w/2+58)} {f(y+96)}L{f(x+w/2-58)} {f(y+96)}Z", BLUE),
          path(f"M{f(x+w/2-40)} {f(y+62)}L{f(x+w/2+40)} {f(y+62)}", "none",
               BLUEF, 7, None, 'stroke-linecap="round"'),
          path(f"M{f(x+w/2-40)} {f(y+80)}L{f(x+w/2+14)} {f(y+80)}", "none",
               BLUEF, 7, None, 'stroke-linecap="round"')]
    el.append(path(f"M{f(x+w/2-58)} {f(y+46)}L{f(x+w/2-58)} {f(y+96)}", "none",
                   BLUEF, 4, "0.7"))
    for i in range(4):
        el.append(path(f"M{f(x+w/2+26+i*7)} {f(y+54)}"
                       f"L{f(x+w/2+26+i*7)} {f(y+88)}", "none", BLUEF, 3,
                       "0.8"))
    el.append(path(f"M{f(x)} {f(y+26)}L{f(x+w)} {f(y+26)}", "none", GREY, 4,
                   "0.5"))
    return el


def arrow_reprint(cx, cy, r=34):
    """An amber go-round-again arrow."""
    a0, a1, sw = 130, 392, 13
    head = polar((cx, cy), a1, r)
    d = f"M{pt(polar((cx, cy), a0, r))}A{f(r)} {f(r)} 0 1 1 {pt(head)}"
    # The head points along the tangent (a1 + 90), not at the centre - that
    # was the broken arrowhead.
    tip = polar(head, a1 + 90, sw * 2.1)
    tri = (f"M{pt(polar(head, a1, sw * 1.45))}L{pt(tip)}"
           f"L{pt(polar(head, a1, -sw * 1.45))}Z")
    return [path(d, "none", AMBER, sw, None, 'stroke-linecap="round"'),
            path(tri, AMBER, None, None, None,
                 'stroke-linejoin="round" stroke="' + AMBER +
                 '" stroke-width="2"')]


# ------------------------------------------------------- props for the views
def hardhat_front():
    """The hard hat seen head-on: dome, crest rib, brim across both eyes."""
    return [path("M178 120C178 76 212 50 256 50C300 50 334 76 334 120"
                 "C300 94 212 94 178 120Z", AMBER),
            path("M242 54C250 51 262 51 270 54C270 80 270 100 268 114"
                 "C262 112 250 112 244 114C244 100 244 78 242 54Z", AMBERF,
                 None, None, "0.5"),
            path("M160 122C174 108 208 98 256 98C304 98 338 108 352 122"
                 "C358 127 356 137 347 137C312 118 200 118 165 137"
                 "C156 137 154 127 160 122Z", AMBER),
            path("M165 137C200 118 312 118 347 137C349 141 346 145 340 144"
                 "C306 130 206 130 172 144C166 145 163 141 165 137Z",
                 "#B96A18")]


HARDHAT_FR_HALO = ("M158 120C158 74 208 46 256 46C304 46 354 74 354 120"
                   "C360 126 356 137 347 137C312 118 200 118 165 137"
                   "C156 137 152 126 158 120Z")


def extrusion(x, y, w, h, vert=True):
    """A length of 2020 extrusion, end grain not shown: blue face, grey slot."""
    el = [path(f"M{f(x)} {f(y)}L{f(x+w)} {f(y)}L{f(x+w)} {f(y+h)}"
               f"L{f(x)} {f(y+h)}Z", BLUE, "#1C4E82", 5,
               extra='stroke-linejoin="round"')]
    if vert:
        el.append(path(f"M{f(x+w*0.34)} {f(y)}L{f(x+w*0.66)} {f(y)}"
                       f"L{f(x+w*0.66)} {f(y+h)}L{f(x+w*0.34)} {f(y+h)}Z",
                       "#1C4E82"))
        el.append(path(f"M{f(x+w*0.44)} {f(y)}L{f(x+w*0.56)} {f(y)}"
                       f"L{f(x+w*0.56)} {f(y+h)}L{f(x+w*0.44)} {f(y+h)}Z",
                       "#14395F"))
    else:
        el.append(path(f"M{f(x)} {f(y+h*0.34)}L{f(x+w)} {f(y+h*0.34)}"
                       f"L{f(x+w)} {f(y+h*0.66)}L{f(x)} {f(y+h*0.66)}Z",
                       "#1C4E82"))
        el.append(path(f"M{f(x)} {f(y+h*0.44)}L{f(x+w)} {f(y+h*0.44)}"
                       f"L{f(x+w)} {f(y+h*0.56)}L{f(x)} {f(y+h*0.56)}Z",
                       "#14395F"))
    return el


def bolt(cx, cy, r=15):
    pts = [polar((cx, cy), 30 + i * 60, r) for i in range(6)]
    return [path("M" + "L".join(pt(q) for q in pts) + "Z", STEEL, GREY, 4,
                 extra='stroke-linejoin="round"'),
            path("M" + "L".join(pt(polar((cx, cy), 30 + i * 60, r * 0.52))
                                for i in range(6)) + "Z", "#434C5C")]


def hexkey(cx, cy, ang=-38, long=104, short=44):
    """An L hex key, short arm into the bolt at (cx, cy)."""
    elbow = polar((cx, cy), ang, short)
    end = polar(elbow, ang - 82, long)
    return [path(taper([(cx, cy), elbow], [15, 15]), STEEL),
            path(taper([elbow, end], [15, 13]), GREY),
            path(taper([elbow, end], [7, 6]), "#434C5C"),
            path(taper([(cx, cy), elbow], [7, 7]), "#434C5C")]


def bin_box(x, y, w=210, h=116):
    """A labelled parts bin, front face toward the reader."""
    el = [path(f"M{f(x)} {f(y)}L{f(x+w)} {f(y)}L{f(x+w-10)} {f(y+h)}"
                 f"L{f(x+10)} {f(y+h)}Z", STEEL, GREY, 6,
                 extra='stroke-linejoin="round"'),
            path(f"M{f(x)} {f(y)}L{f(x+w)} {f(y)}L{f(x+w)} {f(y+16)}"
                 f"L{f(x)} {f(y+16)}Z", GREYF),
          path(f"M{f(x+w*0.16)} {f(y+40)}L{f(x+w*0.6)} {f(y+40)}"
               f"L{f(x+w*0.59)} {f(y+86)}L{f(x+w*0.17)} {f(y+86)}Z", BLUE),
            path(f"M{f(x+w*0.22)} {f(y+56)}L{f(x+w*0.52)} {f(y+56)}", "none",
               BLUEF, 7, None, 'stroke-linecap="round"'),
          path(f"M{f(x+w*0.22)} {f(y+72)}L{f(x+w*0.42)} {f(y+72)}", "none",
               BLUEF, 7, None, 'stroke-linecap="round"')]
    for i in range(3):
        for j in range(2):
            el.append(path(f"M{f(x+w*0.63+i*11)} {f(y+50+j*11)}"
                           f"l7 0l0 7l-7 0Z", BLUEF, None, None, "0.75"))
    el.append(path(f"M{f(x+w-36)} {f(y)}L{f(x+w-12)} {f(y)}"
                   f"L{f(x+w-16)} {f(y+18)}L{f(x+w-32)} {f(y+18)}Z", BLUE))
    return el


def cable_run(pts, coil, col=BLUE, w=15):
    """A lead running down to a loose coil on the floor beside the feet."""
    d = "M" + pt(pts[0])
    for i in range(1, len(pts) - 1, 2):
        d += f"Q{pt(pts[i])} {pt(pts[i + 1])}"
    el = [path(d, "none", col, w, None, 'stroke-linecap="round"'),
          path(d, "none", "#1C4E82", w * 0.4, "0.55",
               'stroke-linecap="round"')]
    cx, cy = coil
    for rx, ry, dx, dy in ((48, 17, 0, 0), (36, 13, -13, 9)):
        el.append(path(f"M{f(cx - rx + dx)} {f(cy + dy)}"
                       f"a{f(rx)} {f(ry)} 0 1 0 {f(rx * 2)} 0"
                       f"a{f(rx)} {f(ry)} 0 1 0 {f(-rx * 2)} 0Z",
                       "none", col, w, None, 'stroke-linecap="round"'))
    return el


def connector(cx, cy, ang=-14, tail=True):
    """A low-voltage plug and its cable tail. Never mains."""
    c = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    def P(u, v):
        return (cx + u * c[0] - v * c[1], cy + u * c[1] + v * c[0])
    el = [path(f"M{pt(P(0,-26))}L{pt(P(58,-26))}L{pt(P(58,26))}L{pt(P(0,26))}Z",
               GREY, GREYF, 5, extra='stroke-linejoin="round"')]
    for i in range(4):
        v = -18 + i * 12
        el.append(path(f"M{pt(P(58,v-4))}L{pt(P(82,v-4))}L{pt(P(82,v+4))}"
                       f"L{pt(P(58,v+4))}Z", BLUEF))
    # keyed notch on the top of the shell, so it reads as a signal plug
    el.append(path(f"M{pt(P(16,-26))}L{pt(P(40,-26))}L{pt(P(40,-34))}"
                   f"L{pt(P(16,-34))}Z", GREYF))
    if tail:
        el.append(path(f"M{pt(P(0,-16))}C{pt(P(-46,-30))} {pt(P(-92,10))} "
                       f"{pt(P(-146,4))}", "none", BLUE, 15, None,
                       'stroke-linecap="round"'))
        el.append(path(f"M{pt(P(0,-16))}C{pt(P(-46,-30))} {pt(P(-92,10))} "
                       f"{pt(P(-146,4))}", "none", "#1C4E82", 6, "0.6",
                       'stroke-linecap="round"'))
    return el


def screen(x, y, w=176, h=132):
    """A small Mainsail-style console on a stand: rows and a green bar."""
    el = [path(f"M{f(x)} {f(y)}L{f(x+w)} {f(y)}L{f(x+w)} {f(y+h)}"
               f"L{f(x)} {f(y+h)}Z", GREY, GREYF, 6,
               extra='stroke-linejoin="round"'),
          path(f"M{f(x+12)} {f(y+12)}L{f(x+w-12)} {f(y+12)}"
               f"L{f(x+w-12)} {f(y+h-12)}L{f(x+12)} {f(y+h-12)}Z", "#151A22"),
          path(f"M{f(x+22)} {f(y+26)}L{f(x+w-40)} {f(y+26)}", "none", BLUEF, 7,
               "0.8", 'stroke-linecap="round"'),
          path(f"M{f(x+22)} {f(y+44)}L{f(x+w-62)} {f(y+44)}", "none", BLUE, 7,
               None, 'stroke-linecap="round"'),
          path(f"M{f(x+22)} {f(y+h-46)}L{f(x+w-22)} {f(y+h-46)}"
               f"L{f(x+w-22)} {f(y+h-26)}L{f(x+22)} {f(y+h-26)}Z", "#243040")]
    el.append(g("m-layer", [anchor(),
                            path(f"M{f(x+26)} {f(y+h-36)}L{f(x+w-58)} "
                                 f"{f(y+h-36)}", "none", GREEN, 12, None,
                                 'stroke-linecap="round"')]))
    el.append(path(f"M{f(x+w/2-16)} {f(y+h)}L{f(x+w/2+16)} {f(y+h)}"
                   f"L{f(x+w/2+26)} {f(y+h+40)}L{f(x+w/2-26)} {f(y+h+40)}Z",
                   GREY, GREYF, 5, extra='stroke-linejoin="round"'))
    return el


def chevrons(cx, cy, n=3, s=1.0):
    """Three blue chevrons: the direction a wingtip is pointing."""
    el = []
    for i in range(n):
        x = cx + i * 26 * s
        el.append(path(f"M{f(x)} {f(cy-22*s)}L{f(x+18*s)} {f(cy)}"
                       f"L{f(x)} {f(cy+22*s)}", "none", BLUE, 11 * s,
                       f"{1 - i * 0.28:.2f}",
                       'stroke-linejoin="round" stroke-linecap="round"'))
    return el


# ---------------------------------------------------------------- poses
def bob(origin, dy=7, rot=1.6, dur="3.6s", cls="m-prop"):
    return (f".mascot .{cls}{{transform-origin:{origin};"
            f"animation:mascot-bob {dur} ease-in-out -.9s infinite}}"
            "@keyframes mascot-bob{0%,100%{transform:translateY(0) rotate(0)}"
            f"50%{{transform:translateY(-{dy}px) rotate({rot}deg)}}}}")


def pose_base():
    return svg("Revali, the manual's raven, standing",
               "Revali, a black raven with a blue-violet wing sheen and a blue "
               "scarf, standing and facing right", bird(tilt=4))


def pose_gather():
    t = g("m-prop", [anchor()] + tray(322, 292, 158, 44))
    return svg("Revali with a tray of screws",
               "Revali holding out a parts tray of screws in one wing",
               bird(tilt=4, near=SP(30, 166), far=FOLDED, front=[t]),
               bob("401px 314px", 5, 1.2))


def pose_pause():
    marks = g("m-zz", [anchor(),
                       zmark(360, 150, 1.0),
                       zmark(398, 104, 0.78, "0.75"),
                       zmark(426, 68, 0.56, "0.5")])
    b = place([bird(closed=True, perch=True, halo_extra=[NIGHTCAP_HALO],
                    front=nightcap())], 6, -66, 0.78)
    css = (".mascot .m-zz{animation:mascot-drift 4.6s ease-in-out infinite}"
           "@keyframes mascot-drift{0%{transform:translate(0,0);opacity:.3}"
           "28%{opacity:1}100%{transform:translate(18px,-30px);opacity:0}}")
    return svg("Revali asleep on a spool",
               "Revali asleep in a nightcap, perched on a filament spool",
               g("", spool(214, 392, 88) + [b, marks]), css)


def pose_check():
    # Lens out in front of the eye, handle running down to the wingtip at
    # (450, 274); `grip` puts the curled primaries across the grip itself.
    # Composed at native scale so the lens sits beyond the bill rather than
    # over the eye: wing at 14 deg / span 173 puts its tip at the grip.
    m = g("m-prop", [anchor()] + magnifier(492, 176, 50, 96, grip=102))
    b = g("", [bird(tilt=5, near=SP(14, 173), far=FOLDED), m])
    return svg("Revali checking with a magnifier",
               "Revali holding a magnifier by its handle, looking through "
               "the lens",
               place([b], -26, 6, 0.84),
               bob("492px 176px", 5, -1.2))


def pose_warn():
    b = bird_front(brow=True, halo_extra=[HARDHAT_FR_HALO],
                   left=SP(186, 172), right=SP(-6, 172),
                   front=hardhat_front())
    return svg("Revali in a hard hat",
               "Revali facing the reader in a hard hat, wings spread level",
               b, VIEW_CSS["front"])


def pose_pass():
    cal = g("m-prop", [anchor()] + caliper(250, 28, 8))
    tk = g("m-tick", [anchor()] + tick(78, 322, 1.15))
    b = bird_3q(tilt=6, near=SP(-58, 144), far=SP(-124, 132),
                front=[cal, tk])
    css = (VIEW_CSS["3q"] + ".mascot .m-prop{transform-origin:338px 62px;"
           "animation:mascot-raise 3.2s ease-in-out -.6s infinite}"
           "@keyframes mascot-raise{0%,100%{transform:translateY(0) rotate(0)}"
           "50%{transform:translateY(-9px) rotate(-3deg)}}"
           ".mascot .m-tick{transform-origin:78px 322px;"
           "animation:mascot-pop 3.2s ease-in-out -.6s infinite}"
           "@keyframes mascot-pop{0%,100%{transform:scale(1)}"
           "46%{transform:scale(1.12)}}")
    return svg("Revali passing a gate",
               "Revali cheering toward the reader, caliper up, green tick",
               b, css)


def pose_fail():
    ar = g("m-prop", [anchor()] + arrow_reprint(96, 122, 36))
    b = bird_3q(tilt=-5, near=SP(34, 150, 12), far=SP(146, 144, 12),
                front=spool(430, 404, 52))
    return svg("Revali shrugging at a failed gate",
               "Revali turned toward the reader, both wings low in a shrug",
               g("", [b, ar]), VIEW_CSS["3q"] +
               ".mascot .m-prop{transform-origin:132px 150px;"
               "animation:mascot-turn 6.4s ease-in-out -1s infinite}"
               "@keyframes mascot-turn{0%,62%{transform:rotate(0)}"
               "86%,100%{transform:rotate(360deg)}}")


def pose_helper():
    adult = place([bird_3q()], -48, -8, 0.82)
    chick = place([g("m-chick", [anchor(), bird_3q(tilt=7, juv=True)])],
                  250, 218, 0.44)
    css = (".mascot .m-chick{transform-origin:256px 470px;"
           "animation:mascot-hop 4.4s ease-in-out -1.4s infinite}"
           "@keyframes mascot-hop{0%,62%,100%{transform:translateY(0)}"
           "74%{transform:translateY(-15px)}86%{transform:translateY(0)}}")
    return svg("Revali and a fledgling",
               "An adult raven and a fledgling, both looking at the reader",
               g("", [adult, chick]), VIEW_CSS["3q"] + css)


def pose_print():
    b = place([bird(perch=True, tilt=3)], 22, -14, 0.64)
    css = (".mascot .m-layer{transform-origin:170px 402px;"
           "animation:mascot-lay 5s ease-in-out -1s infinite}"
           "@keyframes mascot-lay{0%{transform:scaleX(.04)}"
           "72%,100%{transform:scaleX(1)}}")
    return svg("Revali watching a first layer",
               "Revali perched on the printer, watching the first layer go "
               "down", g("", printer(106, 272, 300, 200) + [b]), css)


def pose_kitday():
    b = place([bird_front(no_legs=True,
                          left=SP(222, 150), right=SP(-42, 150))],
              6, 30, 0.80)
    css = (".mascot .m-flap{transform-origin:256px 352px;"
           "animation:mascot-flap 5.4s ease-in-out -2s infinite}"
           "@keyframes mascot-flap{0%,100%{transform:rotate(0)}"
           "50%{transform:rotate(-1.4deg)}}")
    return svg("Revali out of the carton",
               "Revali peeking out of an opened carton at the reader",
               g("", [b, g("m-flap", [anchor()] + carton(90, 344, 332, 132))]),
               VIEW_CSS["front"] + css)


def pose_tip():
    bl = g("m-bulb", [anchor()] + bulb(430, 104, 38))
    b = bird_3q(tilt=5, near=SP(-52, 150), far=FOLDED, front=[bl])
    css = (VIEW_CSS["3q"] + ".mascot .m-bulb{transform-origin:430px 104px;"
           "animation:mascot-flicker 4.8s ease-in-out -1.2s infinite}"
           "@keyframes mascot-flicker{0%,44%,100%{opacity:1}"
           "50%{opacity:.6}56%{opacity:1}62%{opacity:.78}68%{opacity:1}}")
    return svg("Revali with an idea",
               "Revali looking at the reader, one wing up beside a lit bulb",
               b, css)


BADGE_PTS = [((236, 214), 100, 56), ((268, 222), 92, 66), ((302, 216), 84, 58)]


def pose_badge():
    """Three-quarter head and shoulders, simplified to survive 40-48 px."""
    hk = [feather(b, a, ln, 15, 2, 0.0) for b, a, ln in BADGE_PTS]
    sil = [path(TORSO_3Q), path(SKULL_3Q), path(BILL_3Q)] + [path(d) for d in hk]
    el = [anchor(),
          g("halo", sil,
            f'fill="{HALO}" stroke="{HALO}" stroke-width="15" '
            'stroke-linejoin="round" stroke-linecap="round"'),
          path(TORSO_3Q, K1),
          path("M246 192C216 206 194 240 186 276C180 304 180 334 186 358"
               "C188 320 198 278 216 246C228 224 240 204 246 192Z", K2),
          path("M296 196C320 220 338 262 342 306C346 348 340 384 322 406"
               "C332 374 336 334 332 294C328 250 314 216 296 196Z", K3,
               None, None, "0.55")]
    for d in row(4, (312, 292), (338, 236), 100, 86, 46, 42, 18, 17,
                 bend=3, blunt=0.66):
        el.append(path(d, K2, K0, 3.0))
    for d in row(4, (316, 272), (338, 228), 98, 84, 34, 31, 16, 15,
                 bend=2, blunt=0.8):
        el.append(path(d, K3, K0, 2.8))
    for d in row(4, (316, 272), (338, 228), 98, 84, 29, 27, 14, 13,
                 bend=2, blunt=0.8):
        el.append(path(d, "url(#sheen)", None, None, "0.85"))
    for i, d in enumerate(hk):
        el.append(path(d, "#47546E" if i % 2 else K2, EDGE, 3.0))
    # The scarf band survives 30 px as one blue stroke under the chin; the
    # tails would not, so the badge has none. One braid, weave dropped.
    el += scarf_3q(tails=False)[0]
    el.append(g("m-head", [anchor()] + rotg(
        head_3q(simple=True) + [g("m-eye", [anchor()] + eyes_3q(k=1.18))]
        + eyelid(EYE_3Q_FAR, 13.0) + eyelid(EYE_3Q_NEAR, 22.4), 4)))
    return svg("Revali, the badge",
               "A small head-and-shoulders badge of Revali the raven",
               place([g("m-body", el)], -300, -108, 1.98), VIEW_CSS["3q"])


NIGHTCAP_HALO = ("M406 136C404 112 386 94 356 94C322 92 296 112 292 150"
                 "C276 126 258 104 246 100C234 96 228 106 234 118"
                 "C224 134 210 158 208 182C206 202 218 216 234 216"
                 "C252 216 242 196 238 178C236 162 244 140 254 126Z")
HARDHAT_HALO = ("M278 116C282 74 314 48 352 50C392 52 414 80 416 112"
                "C424 116 424 124 416 126C380 112 322 110 282 126"
                "C275 128 272 121 278 116Z")

def pose_base_3q():
    return svg("Revali, three-quarter", "Revali turned toward the reader",
               bird_3q(), VIEW_CSS["3q"])


def pose_base_front():
    return svg("Revali, facing the reader",
               "Revali facing the reader, both wings folded",
               bird_front(), VIEW_CSS["front"])


def pose_hexkey():
    prop = (extrusion(424, 96, 58, 330) + extrusion(330, 426, 152, 58, False)
            + bolt(453, 296) + [g("m-prop", [anchor()] + hexkey(453, 296,
                                                                -150, 92, 40))])
    b = bird_3q(tilt=3, near=SP(30, 126), far=FOLDED)
    return svg("Revali turning a hex key",
               "Revali driving a hex key into an extrusion corner",
               place([g("", [b] + prop)], -34, 6, 0.93),
               VIEW_CSS["3q"] +
               ".mascot .m-prop{transform-origin:453px 296px;"
               "animation:mascot-drive 4.4s ease-in-out -1s infinite}"
               "@keyframes mascot-drive{0%,54%{transform:rotate(0)}"
               "80%,100%{transform:rotate(26deg)}}")


def pose_caliper():
    cal = g("m-prop", [anchor()] + caliper(258, 236, -6))
    b = place([bird_3q(tilt=2, near=SP(36, 142), far=FOLDED)],
              -86, -6, 0.92)
    return svg("Revali reading a caliper",
               "Revali holding a caliper up with the display toward the reader",
               g("", [b, cal]), VIEW_CSS["3q"] + bob("346px 262px", 5, -1.2))


def pose_point():
    b = place([bird_3q(tilt=3, near=SP(18, 146), far=FOLDED)],
              -96, 6, 0.9)
    ch = g("m-prop", [anchor()] + chevrons(404, 266, 3, 1.0))
    return svg("Revali pointing", "Revali pointing a wingtip to the right",
               g("", [b, ch]), VIEW_CSS["3q"] +
               ".mascot .m-prop{transform-origin:430px 266px;"
               "animation:mascot-nudge 2.8s ease-in-out -.6s infinite}"
               "@keyframes mascot-nudge{0%,100%{transform:translateX(0)}"
               "50%{transform:translateX(9px)}}")


def pose_carry():
    # Spans and angles solved so each wingtip lands just above its own corner
    # of the bin: near shoulder (338, 218) -> (400, 380), far (198, 234) ->
    # (186, 380). The bin is drawn after the bird, so the wings wrap from
    # behind and only the forearms show above the rim.
    b = g("", [bird_3q(tilt=3, near=SP(78, 132, 8), far=SP(108, 140, 8))]
          + [g("m-prop", [anchor()] + bin_box(164, 372, 196, 108))])
    return svg("Revali carrying a bin",
               "Revali carrying a labelled parts bin in both wings",
               place([b], 0, -26, 0.9),
               VIEW_CSS["3q"] + bob("262px 426px", 5, 0.9))


def pose_cable():
    # Composed at native scale so the plug sits in the wingtip: the wing at
    # 30 deg / span 150 puts its tip at about (490, 288).
    lead = cable_run([(464, 300), (438, 372), (404, 424),
                      (376, 462), (344, 470)], (322, 470))
    plug = g("m-prop", [anchor()] + connector(486, 288, -8, tail=False))
    b = g("", [bird_3q(tilt=3, near=SP(30, 150), far=FOLDED)] + lead + [plug])
    return svg("Revali plugging in a cable",
               "Revali holding a keyed low voltage plug, its lead coiled "
               "on the floor",
               place([b], -84, -8, 0.88),
               VIEW_CSS["3q"] + bob("486px 288px", 4, -1.2))


def pose_screen():
    b = place([bird(tilt=1)], -84, 12, 0.86)
    return svg("Revali watching a console",
               "Revali watching a console with a progress bar",
               g("", screen(306, 210) + [b]),
               ".mascot .m-layer{transform-origin:332px 306px;"
               "animation:mascot-lay 5.6s ease-in-out -1s infinite}"
               "@keyframes mascot-lay{0%{transform:scaleX(.06)}"
               "76%,100%{transform:scaleX(1)}}")


# Grouped by view: profile first, then three-quarter, then front.
POSES = {
    "base": pose_base, "gather": pose_gather, "pause": pose_pause,
    "check": pose_check, "warn": pose_warn, "pass": pose_pass,
    "fail": pose_fail, "helper": pose_helper, "print": pose_print,
    "kitday": pose_kitday, "tip": pose_tip, "badge": pose_badge,
    "hexkey": pose_hexkey, "caliper": pose_caliper, "point": pose_point,
    "carry": pose_carry, "cable": pose_cable, "screen": pose_screen,
    "base-3q": pose_base_3q, "base-front": pose_base_front,
}

VIEW_OF = {
    "profile": ["base", "check", "gather", "pause", "print", "screen"],
    "three-quarter": ["base-3q", "pass", "fail", "tip", "helper", "hexkey",
                      "caliper", "point", "carry", "cable", "badge"],
    "front": ["base-front", "warn", "kitday"],
}
assert sorted(sum(VIEW_OF.values(), [])) == sorted(POSES), "pose/view drift"


def previews(out):
    """Render the review PNGs with rsvg-convert: 512 px light + dark, badge 48."""
    import subprocess
    pre = out / "preview"
    pre.mkdir(parents=True, exist_ok=True)
    for old in pre.glob("*.png"):
        old.unlink()
    jobs = []
    for name in POSES:
        for bg, tag in (("white", "light"), ("#1e2129", "dark")):
            jobs.append((out / f"mascot-{name}.svg", 512,
                         pre / f"mascot-{name}-{tag}.png", bg))
    jobs.append((out / "mascot-badge.svg", 48, pre / "mascot-badge-48.png",
                 "#1e2129"))
    worst = 0
    for src, px, dst, bg in jobs:
        subprocess.run(["rsvg-convert", "-w", str(px), "-h", str(px),
                        "-b", bg, str(src), "-o", str(dst)], check=True)
        if dst.stat().st_size > 56 * 1024:   # headroom under the 60 KB cap
            subprocess.run(["magick", str(dst), "-colors", "128", str(dst)],
                           check=True)
        worst = max(worst, dst.stat().st_size)
    print(f"{len(jobs)} previews, largest {worst / 1024:.1f} KB")


# The profile far wing reuses the near wing's envelope path inside a translate,
# so it cannot be counted by that path alone - the transform is its marker.
FAR_OFF_MARK = FAR_OFF
# Derived from the constants, never retyped: hand-copied prefixes went stale
# the moment a wing envelope was re-drawn, and the guard silently passed.
PROFILE_ENV = WING[:18]
SIDE_MARKS = (WING_3Q_NEAR[:18], WING_3Q_FAR[:18],
              WING_FR_ENV[-1][:18], WING_FR_ENV[1][:18])
# helper holds two birds that share the same envelope paths, so presence
# counting sees one pair; badge is a head crop with no wing envelope.
WING_EXCEPTIONS = {"helper": 2, "badge": 0}


def wing_tally(name, t):
    """Exactly two wings per bird: folded or spread, never both on a side."""
    spread = t.count('class="m-spread"')
    far_off = t.count(FAR_OFF_MARK)
    env = t.count(PROFILE_ENV) - far_off
    folded = (1 if far_off else 0) + (1 if env > 0 else 0)
    folded += sum(1 for m in SIDE_MARKS if m in t)
    total = folded + spread
    want = WING_EXCEPTIONS.get(name)
    if want is not None:
        ok = total == want
    elif spread:
        ok = total == 2
    else:
        ok = total <= 2
    return folded, spread, total, ok


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    bad = []
    for name, fn in POSES.items():
        p = OUT / f"mascot-{name}.svg"
        text = fn() + "\n"
        p.write_text(text)
        kb = p.stat().st_size / 1024
        total += kb
        fo, sp, wn, ok = wing_tally(name, text)
        if not ok:
            bad.append(name)
        print(f"{p.name:22s} {kb:6.1f} KB  wings {wn} "
              f"(folded {fo}, spread {sp}){'' if ok else '   <-- WRONG'}"
              + ("  OVER 80 KB" if kb > 80 else ""))
    print(f"{'total':22s} {total:6.1f} KB")
    if bad:
        raise SystemExit("wing count wrong: " + ", ".join(bad))
    if "--preview" in sys.argv:
        previews(OUT)


if __name__ == "__main__":
    main()
