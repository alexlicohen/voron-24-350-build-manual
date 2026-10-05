#!/usr/bin/env python3
"""Generate the bench hardware trays for the LDO Voron 2.4 350 kit's fastener box.

Each tray is a standard Gridfinity bin (42 mm grid, 7 mm height units, the spec's stepped
base on every unit and its stacking lip on top), divided into one compartment per hardware row
of the kit BOM, with two raised label lines on a ledge behind each row and a scoop cove along
each compartment's front wall. Compartments are sized by an explicit fill check (bulk volume of
the loose pieces over the compartment's usable volume, at most FILL_MAX); the script stops if
any compartment would be fuller.

Everything comes from the data: the rows of box "Fasteners, Tools & Misc" in
scripts/data/ldo-350-bom.yml (re-pinned on kit day, Step 00.2) and the `tool` roles in
scripts/data/hardware-ownership.yml (tools are not stored in the trays). A row this script
cannot classify stops it, so a re-pinned BOM with a new hardware line fails loudly.

    venv-cq/bin/python slicer/bench/hardware-trays/gen_trays.py            # everything
    venv-cq/bin/python slicer/bench/hardware-trays/gen_trays.py --plan     # options + fill table
    venv-cq/bin/python slicer/bench/hardware-trays/gen_trays.py --no-slice # skip the slicer
    ... --holes magnet|screw   # Gridfinity magnet (6.5 x 2.4) or M3 screw holes; default none

Writes, next to this file: tray-<X>.stl and a PrusaSlicer 2.9.6 project per tray (config
embedded: 0.20mm BALANCED @COREONE HF0.4 + Prusament PLA @COREONE HF0.4 + the CORE One HF0.4
printer, with this repo's cold start and AFS flap lines), renders/*.png, and the generated
blocks of README.md.
"""
from __future__ import annotations

import argparse
import itertools
import math
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLICER = HERE.parent.parent
REPO = SLICER.parent
sys.path.insert(0, str(SLICER))
sys.path.insert(0, str(REPO / "scripts" / "cad_render"))

import yaml  # noqa: E402

BOM = REPO / "scripts" / "data" / "ldo-350-bom.yml"
OWNERSHIP = REPO / "scripts" / "data" / "hardware-ownership.yml"
README = HERE / "README.md"
RENDERS = HERE / "renders"
BOX = "Fasteners, Tools & Misc"
# Not in a compartment: cut stock, a 100-pack, two bar handles. Rows whose ownership role is
# `tool` (hex keys, drill bit, screwdriver, insert tip) are not stored in the trays either.
EXCLUDE = ("Teflon Tube", "Zip Ties", "Aluminium Handle")

# ------------------------------------------------------------------ Gridfinity (mm)
# gridfinity.xyz/specification ("Gridfinity Design Reference v5", willtree8) and
# kennetek/gridfinity-rebuilt-openscad src/core/standard.scad @910e22d.
GRID = 42.0                 # grid pitch
GAP = 0.5                   # bin outer = 42 n - 0.5
UNIT_H = 7.0                # height unit; bin height 7 u includes the base, excludes the lip
BASE_TOP_R = 3.75           # outer corner radius (7.5 dia) at the top of each base and the bin
# Base profile, from the foot's bottom edge: (outward step, z). 0.8 at 45 deg, 1.8 up, 2.15 at
# 45 deg: bottom 35.6 square, r 0.8; top 41.5 square, r 3.75.
BASE_PROFILE = ((0.0, 0.0), (0.8, 0.8), (0.8, 2.6), (2.95, 4.75))
BASE_HEIGHT = 7.0           # base + the bridge tying the bases together (rebuilt BASE_HEIGHT)
# Stacking lip, from its inner tip at the bin height: (outward, z). 0.7 at 45 deg, 1.8 up,
# 1.9 at 45 deg: 2.6 deep, 4.4 high, sharp outer top edge.
LIP_PROFILE = ((0.0, 0.0), (0.7, 0.7), (0.7, 2.5), (2.6, 4.4))
LIP_DEPTH, LIP_H = 2.6, 4.4
LIP_TOP_FLAT = 0.3          # the spec's knife edge is cut back to a 0.3 mm flat (lip 4.1 high)
LIP_SUPPORT = 1.2           # interior stays this far below the bin height (rebuilt fill height)
MAGNET_D, MAGNET_DEPTH = 6.5, 2.4    # standard.scad MAGNET_HOLE_RADIUS*2, MAGNET_HOLE_DEPTH
SCREW_D, SCREW_DEPTH = 3.0, 6.0
HOLE_FROM_SIDE = 8.0        # hole centre from each side of a unit (d_hole_from_side)

# ------------------------------------------------------------------ tray geometry (mm)
BED_X, BED_Y = 250.0, 220.0
WALL = LIP_DEPTH            # outer wall = lip depth, so the lip sits on solid wall (no overhang)
FLOOR_Z = BASE_HEIGHT       # compartment floor
DIVIDER = 1.8               # wall between compartments in a row (four 0.45 mm lines)
R_CAV = 2.8                 # cavity corner radius (rebuilt r_f2)
SCOOP_R = 12.0              # cove along each compartment's front wall
MIN_W, MIN_H = 25.0, 18.0   # finger floor: compartment width (X) x row length (Y)
FILL_MAX = 0.70             # bulk / usable volume, at most
EMBOSS = 0.6                # label relief: ledge top 0.6 below the divider tops
CAP1, CAP2 = 5.0, 4.0       # label cap heights: line 1 (size), line 2 (type + count)
LEDGE = 1.2 + CAP1 + 1.8 + CAP2 + 1.2   # 13.2: the label ledge behind each row
LABEL_PAD = 3.0             # label width + this <= compartment width
FONT_NAME, FONT_KIND = "DejaVu Sans", "bold"   # the face scripts/nameplate.py uses
DEJAVU_CAP = 0.729          # cap height / CadQuery font size for DejaVu Sans Bold (measured)
NAME_CAP, NAME_SINK = 4.0, 0.5   # tray name cut into the front outer face
UNITS_X = 5                 # 5 x 42 - 0.5 = 209.5 mm across the 250 mm bed axis
UNITS_Y = (3, 4, 5)         # depth options (5 units = 209.5 < 220)
HEIGHTS = (4, 5, 6)         # height options, in units


def rim_z(u: int) -> float:
    """Top of dividers and labels: below the bin height by the lip support, so a bin stacked on
    this one never touches them."""
    return UNIT_H * u - LIP_SUPPORT


def usable_depth(u: int) -> float:
    return rim_z(u) - FLOOR_Z


# ------------------------------------------------------------------ pieces
# Per-piece dimensions. Sources (README § Fill check):
#   ISO   bd_warehouse data tables @eed2da1 (gumyr/bd_warehouse src/bd_warehouse/data/*.csv):
#         ISO 4762 SHCS dk/k, ISO 7380 BHCS dk/k, ISO 10642 FHCS dk/k, ISO 4032 nut s/m,
#         ISO 7089 washer d2/h, ISO 14583 pan head dk/k. Maxima, so the envelopes err large.
#   CAD   bounding boxes in the Voron 2.4r2 assembly STEP (VoronDesign/Voron-2): the part the
#         Voron design itself models for that BOM line.
#   NAME  the dimension is in the LDO BOM item text.
#   EST   estimate; no drawing found.
SHCS = {2: (3.98, 2.0), 3: (5.68, 3.0), 4: (7.22, 4.0), 5: (8.72, 5.0)}      # ISO 4762
BHCS = {3: (5.7, 1.65), 4: (7.6, 2.2), 5: (9.5, 2.75)}                       # ISO 7380
FHCS = {3: (6.0, 1.7), 4: (8.0, 2.3), 5: (10.0, 2.8)}                        # ISO 10642
NUT = {3: (5.5, 2.4), 4: (7.0, 3.2), 5: (8.0, 4.7)}                          # ISO 4032 s, m
WASHER = {3: (7.0, 0.55), 4: (9.0, 0.9), 5: (10.0, 1.1)}                     # ISO 7089
PAN = {2: (4.0, 1.6), 3: (5.6, 2.4)}                                         # ISO 14583
TNUT_BOX = {("ROLL-IN", 3): ((12.5, 7.7, 4.3), 286.0, "CAD"),   # Voron "2020 Drop-in T-nut"
            ("ROLL-IN", 5): ((13.0, 7.7, 4.3), 272.0, "CAD"),
            ("HAMMER", 3): ((10.92, 9.14, 4.85), 185.0, "CAD"),  # Voron "M3 Hammerhead T-Nut"
            ("HAMMER", 5): ((11.0, 9.2, 5.0), 190.0, "EST")}     # not in the Voron CAD
# Random-loose packing fraction of the bounding envelope (README § Fill check).
PHI_SCREW_SHORT, PHI_SCREW_LONG = 0.55, 0.45   # envelope length/diameter <= 2 ... >= 8
PHI = {"SET": 0.55, "NUT": 0.58, "INSERT": 0.55, "WASHER": 0.55, "SPACER": 0.55,
       "LOCK": 0.55, "KNURL": 0.58, "MAGNET": 0.60, "ROLL-IN": 0.55, "HAMMER": 0.55}


def cyl(d: float, h: float) -> float:
    return math.pi / 4 * d * d * h


def phi_screw(length: float, dia: float) -> float:
    r = length / dia
    t = min(1.0, max(0.0, (r - 2.0) / 6.0))
    return PHI_SCREW_SHORT + t * (PHI_SCREW_LONG - PHI_SCREW_SHORT)


@dataclass
class Item:
    bom: str            # exact BOM item text
    qty: int
    group: str          # "screw" | "other"
    order: tuple        # row order
    line1: str
    line2: str
    solid: float        # one piece, mm3
    env: float          # bounding envelope of one piece, mm3
    env_desc: str       # e.g. "cyl 5.68 x 11"
    phi: float          # random-loose packing fraction of the envelope
    source: str
    min_w: float = MIN_W

    @property
    def bulk(self) -> float:
        """Loose volume of all pieces, mm3."""
        return self.qty * self.env / self.phi

    @property
    def need(self) -> float:
        """Usable volume the compartment must have, mm3."""
        return self.bulk / FILL_MAX


FAMILY = {"SHCS": 0, "BHCS": 1, "FHCS": 2, "WAFER": 3, "CAPTIVE": 4, "SELF-TAP": 5, "SET": 6,
          "NUT": 10, "INSERT": 11, "WASHER": 12, "SPACER": 13, "LOCK": 14, "KNURL": 15,
          "MAGNET": 16, "ROLL-IN": 20, "HAMMER": 21}


def screw(t: str, q: int, head: str, d: int, L: int, dk: float, k: float, src: str,
          countersunk: bool = False) -> Item:
    total = L if countersunk else L + k
    if countersunk:
        solid = math.pi / 12 * k * (dk * dk + dk * d + d * d) + cyl(d, L - k)
    else:
        solid = cyl(dk, k) + cyl(d, L)
    env = cyl(dk, total)
    return Item(t, q, "screw", (0 if d <= 3 else 1, FAMILY[head], d, L), f"M{d}×{L}",
                f"{head} {q}", solid, env, f"cyl {dk:g} × {total:g}", phi_screw(total, dk), src,
                min_w=max(MIN_W, total + 6))


def classify(row: dict) -> Item | None:
    t, q = row["item"], int(row["qty"])
    m = re.fullmatch(r"Machine Screw, (BHCS|SHCS|FHCS|Wafer head|Captive), M(\d+)x(\d+)", t)
    if m:
        kind, d, L = m.group(1), int(m.group(2)), int(m.group(3))
        if kind == "SHCS":
            return screw(t, q, "SHCS", d, L, *SHCS[d], "ISO 4762")
        if kind == "BHCS":
            return screw(t, q, "BHCS", d, L, *BHCS[d], "ISO 7380")
        if kind == "FHCS":
            return screw(t, q, "FHCS", d, L, *FHCS[d], "ISO 10642", countersunk=True)
        if kind == "Wafer head":
            return screw(t, q, "WAFER", d, L, 8.0, 1.5, "EST (wafer head 8 × 1.5)")
        return screw(t, q, "CAPTIVE", d, L, *SHCS[d], "EST (as ISO 4762 head)")
    m = re.fullmatch(r"Self-tapping Screw, M(\d+)x(\d+)", t)
    if m:
        d, L = int(m.group(1)), int(m.group(2))
        return screw(t, q, "SELF-TAP", d, L, *PAN[d], "ISO 14583 pan head; CAD 4.0 × 11.6")
    m = re.match(r"Set Screw, M(\d+)x(\d+)", t)
    if m:
        d, L = int(m.group(1)), int(m.group(2))
        return Item(t, q, "screw", (0 if d <= 3 else 1, FAMILY["SET"], d, L), f"M{d}×{L}",
                    f"SET {q}", cyl(d, L), cyl(d, L), f"cyl {d} × {L}", PHI["SET"],
                    "ISO 4026 (d × L)")
    m = re.fullmatch(r"Hexnut, M(\d+)", t)
    if m:
        d = int(m.group(1))
        s, h = NUT[d]
        e = s / math.cos(math.pi / 6)
        solid = 3 * math.sqrt(3) / 2 * (e / 2) ** 2 * h - cyl(d, h)
        return Item(t, q, "other", (2, FAMILY["NUT"], d), f"M{d} NUT", f"HEX {q}", solid,
                    cyl(e, h), f"cyl {e:.2f} × {h:g}", PHI["NUT"], "ISO 4032 s, m")
    m = re.fullmatch(r"T-nut, (Roll-in|Hammer Head), 2020, M(\d+)", t)
    if m:
        kind = "ROLL-IN" if m.group(1) == "Roll-in" else "HAMMER"
        d = int(m.group(2))
        (a, b, c), solid, src = TNUT_BOX[(kind, d)]
        return Item(t, q, "other", (2, FAMILY[kind], d), f"M{d} T-NUT", f"{kind} {q}", solid,
                    a * b * c, f"box {a:g} × {b:g} × {c:g}", PHI[kind], src)
    m = re.fullmatch(r"Heatset Insert, Brass, M(\d+)x([\d.]+)x([\d.]+)", t)
    if m:
        d, od, L = int(m.group(1)), float(m.group(2)), float(m.group(3))
        od = max(od, 5.35)      # CAD knurl tips 5.35 over the nominal 5
        return Item(t, q, "other", (2, FAMILY["INSERT"], d), f"M{d} INSERT", f"HEAT-SET {q}",
                    cyl(od, L) - cyl(d, L), cyl(od, L), f"cyl {od:g} × {L:g}", PHI["INSERT"],
                    "NAME; CAD knurl 5.35")
    m = re.fullmatch(r"Washer, M(\d+)(?:, ([\d.]+)mm)?", t)
    if m:
        d = int(m.group(1))
        od, th = WASHER[d]
        th = float(m.group(2)) if m.group(2) else th
        l2 = f"{m.group(2)} mm · {q}" if m.group(2) else str(q)
        return Item(t, q, "other", (2, FAMILY["WASHER"], d), f"M{d} WASHER", l2,
                    cyl(od, th) - cyl(d, th), cyl(od, th), f"cyl {od:g} × {th:g}",
                    PHI["WASHER"], "ISO 7089" + ("; NAME thickness" if m.group(2) else ""))
    m = re.fullmatch(r"Precision Spacer, M(\d+), ([\d.]+)mm", t)
    if m:
        d, th = int(m.group(1)), float(m.group(2))
        return Item(t, q, "other", (2, FAMILY["SPACER"], d), f"M{d} SPACER",
                    f"{m.group(2)} mm · {q}", cyl(10, th) - cyl(d, th), cyl(10, th),
                    f"cyl 10 × {th:g}", PHI["SPACER"], "CAD (M5 1mm Shim 10 × 1)")
    m = re.fullmatch(r"Locking Washer, M(\d+)", t)
    if m:
        d = int(m.group(1))
        return Item(t, q, "other", (2, FAMILY["LOCK"], d), f"M{d} LOCK", f"WASHER {q}",
                    cyl(9.2, 1.2) - cyl(d, 1.2), cyl(9.2, 2.4), "cyl 9.2 × 2.4",
                    PHI["LOCK"], "EST (DIN 127 split, twisted)")
    m = re.fullmatch(r"Knurled Nut, M(\d+)", t)
    if m:
        d = int(m.group(1))
        return Item(t, q, "other", (2, FAMILY["KNURL"], d), f"M{d} KNURLED", f"NUT {q}",
                    cyl(14.08, 8.0) * 0.6, cyl(14.08, 8.0), "cyl 14.08 × 8", PHI["KNURL"],
                    "CAD (DIN 466-B)")
    m = re.fullmatch(r"(\d+)x(\d+)mm Neodymium Magnet", t)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return Item(t, q, "other", (2, FAMILY["MAGNET"], a), f"{a}×{b} MAGNET", str(q),
                    cyl(a, b), cyl(a, b), f"cyl {a} × {b}", PHI["MAGNET"], "NAME; CAD")
    return None


def load_items() -> tuple[list[Item], list[str]]:
    bom = yaml.safe_load(BOM.read_text())
    own = yaml.safe_load(OWNERSHIP.read_text())
    tool_rows = {k for k, v in own.get("unreconciled", {}).items() if str(v).startswith("tool")}
    rows = [r for r in bom["rows"] if r.get("box") == BOX]
    if not rows:
        raise SystemExit(f"{BOM}: no rows in box {BOX!r}")
    items, skipped, unknown = [], [], []
    for r in rows:
        if r["item"].startswith(EXCLUDE) or r["item"] in tool_rows:
            skipped.append(r["item"])
            continue
        it = classify(r)
        (items.append(it) if it else unknown.append(r["item"]))
    if unknown:
        raise SystemExit("BOM rows in the fastener box with no tray rule (classify()): "
                         + "; ".join(unknown))
    return sorted(items, key=lambda i: i.order), skipped


# ------------------------------------------------------------------ text
_FONT = None
_WIDTH: dict[tuple[str, float], float] = {}


def font_path() -> str:
    global _FONT
    if _FONT is None:
        import matplotlib.font_manager as fm
        _FONT = fm.findfont(f"{FONT_NAME}:{FONT_KIND}", fallback_to_default=False)
    return _FONT


def text_solid(txt: str, cap: float, depth: float):
    import cadquery as cq
    return cq.Workplane("XY").text(txt, cap / DEJAVU_CAP, depth, combine=False, clean=True,
                                   font=FONT_NAME, fontPath=font_path(), kind=FONT_KIND,
                                   halign="center", valign="center")


def front_text(txt: str, cap: float, x: float, z: float, sink: float = NAME_SINK):
    """Text to cut into a front (-Y) face at y = 0, reading upright from the front."""
    import cadquery as cq
    return cq.Workplane("XZ", origin=(x, sink, z)).text(
        txt, cap / DEJAVU_CAP, sink + 0.1, combine=False, clean=True, font=FONT_NAME,
        fontPath=font_path(), kind=FONT_KIND, halign="center", valign="center")


def text_w(txt: str, cap: float) -> float:
    key = (txt, cap)
    if key not in _WIDTH:
        _WIDTH[key] = text_solid(txt, cap, 0.6).val().BoundingBox().xlen
    return _WIDTH[key]


def label_w(it: Item) -> float:
    return max(text_w(it.line1, CAP1), text_w(it.line2, CAP2))


# ------------------------------------------------------------------ layout
@dataclass
class Cell:
    item: Item
    x0: float
    x1: float
    y0: float
    y1: float
    depth: float

    @property
    def w(self) -> float:
        return self.x1 - self.x0

    @property
    def h(self) -> float:
        return self.y1 - self.y0

    @property
    def scoop(self) -> float:
        return scoop_r(self.h, self.depth)

    @property
    def usable(self) -> float:
        return usable_volume(self.w, self.h, self.depth)

    @property
    def fill(self) -> float:
        return self.item.bulk / self.usable


@dataclass
class Tray:
    letter: str
    items: list[Item]
    nx: int = UNITS_X
    ny: int = 4
    u: int = 6
    rows: list[list[Cell]] = field(default_factory=list)
    ledges: list[tuple[float, float]] = field(default_factory=list)

    @property
    def W(self) -> float:
        return GRID * self.nx - GAP

    @property
    def D(self) -> float:
        return GRID * self.ny - GAP

    @property
    def title(self) -> str:
        return tray_title(self.items)


def tray_title(items: list[Item]) -> str:
    parts: list[str] = []
    threads = sorted({i.order[2] for i in items if i.group == "screw"})
    if threads:
        parts.append(" · ".join(f"M{d}" for d in threads) + " SCREWS")
    words = {"NUT": "NUTS", "INSERT": "INSERTS", "WASHER": "WASHERS", "SPACER": "WASHERS",
             "LOCK": "WASHERS", "KNURL": "NUTS", "MAGNET": "MAGNETS", "ROLL-IN": "T-NUTS",
             "HAMMER": "T-NUTS"}
    fam = {v: k for k, v in FAMILY.items()}
    for i in items:
        if i.group != "screw":
            w = words[fam[i.order[1]]]
            if w not in parts:
                parts.append(w)
    return " · ".join(parts)


def inner_w(nx: int = UNITS_X) -> float:
    return GRID * nx - GAP - 2 * WALL


def scoop_r(h: float, depth: float) -> float:
    return min(SCOOP_R, 0.4 * h, depth - 4)


def usable_volume(w: float, h: float, depth: float) -> float:
    """Open volume below the rim: the box, less the four rounded vertical corners and the cove."""
    r = scoop_r(h, depth)
    return depth * (w * h - (4 - math.pi) * R_CAV ** 2) - (1 - math.pi / 4) * r * r * w


def min_w(it: Item) -> float:
    return max(it.min_w, label_w(it) + LABEL_PAD)


def row_widths(items: list[Item], h: float, depth: float) -> list[float]:
    """Narrowest widths at which each compartment's usable volume reaches `need`."""
    r = scoop_r(h, depth)
    per_w = depth * h - (1 - math.pi / 4) * r * r
    fixed = depth * (4 - math.pi) * R_CAV ** 2
    return [max(min_w(it), (it.need + fixed) / per_w) for it in items]


def row_min_h(items: list[Item], depth: float, nx: int) -> float | None:
    W = inner_w(nx)
    gaps = DIVIDER * (len(items) - 1)
    if sum(min_w(it) for it in items) + gaps > W:
        return None
    lo = MIN_H
    if sum(row_widths(items, lo, depth)) + gaps <= W:
        return lo
    hi = 2000.0
    for _ in range(50):
        mid = (lo + hi) / 2
        if sum(row_widths(items, mid, depth)) + gaps <= W:
            hi = mid
        else:
            lo = mid
    return hi


_PLAN: dict = {}


def plan_rows(items: list[Item], depth: float, nx: int) -> tuple[list[list[Item]], list[float]]:
    """Partition the ordered items into rows minimising the tray depth (DP over break points)."""
    key = (tuple(i.bom for i in items), depth, nx)
    if key in _PLAN:
        return _PLAN[key]
    n = len(items)
    best: list[tuple[float, int, float]] = [(0.0, -1, 0.0)] + [(math.inf, -1, 0.0)] * n
    for j in range(1, n + 1):
        for i in range(j):
            if best[i][0] == math.inf:
                continue
            h = row_min_h(items[i:j], depth, nx)
            if h is None:
                continue
            cost = best[i][0] + h + LEDGE
            if cost < best[j][0] - 1e-9:
                best[j] = (cost, i, h)
    if best[n][0] == math.inf:
        _PLAN[key] = None
        return None
    rows, hs, j = [], [], n
    while j > 0:
        _c, i, h = best[j]
        rows.append(items[i:j])
        hs.append(h)
        j = i
    _PLAN[key] = (rows[::-1], hs[::-1])
    return _PLAN[key]


def needed_y(items: list[Item], u: int, nx: int = UNITS_X) -> float:
    plan = plan_rows(items, usable_depth(u), nx)
    if plan is None:
        return math.inf
    return 2 * WALL + sum(h + LEDGE for h in plan[1])


UNITS_MAX = 5               # 5 x 42 - 0.5 = 209.5 mm fits both bed axes (250 x 220)
HEIGHT_RANGE = (2, 3, 4, 5, 6)


def size_group(items: list[Item]) -> tuple[int, int, int] | None:
    """Smallest Gridfinity footprint, then the lowest height, that holds the group at
    <= FILL_MAX with the finger floor. (nx, ny, u); rows run along X. Ties on area: wider."""
    best = None
    for nx in range(1, UNITS_MAX + 1):
        for ny in range(1, UNITS_MAX + 1):
            for u in HEIGHT_RANGE:
                if needed_y(items, u, nx) <= GRID * ny - GAP:
                    key = (nx * ny, u, -nx)
                    if best is None or key < best[0]:
                        best = (key, (nx, ny, u))
                    break               # lowest u for this footprint found
    return best[1] if best else None


def cut_points(items: list[Item]) -> list[int]:
    """Indices where a tray may end: between the M2/M3 and M4/M5 screws, between screws and the
    rest, and between two families of the rest. Never inside a screw band, so a tray is always
    'the M3 screws' or 'the M5 screws', never half of each."""
    def key(i: Item) -> tuple:
        return i.order[:1] if i.group == "screw" else i.order[:2]
    return [k for k in range(1, len(items)) if key(items[k]) != key(items[k - 1])]


def layout(tray: Tray) -> None:
    depth = usable_depth(tray.u)
    plan = plan_rows(tray.items, depth, tray.nx)
    if plan is None:
        raise SystemExit(f"tray {tray.letter}: no row partition fits {tray.nx} units wide")
    rows, hs = plan
    slack = tray.D - (2 * WALL + sum(h + LEDGE for h in hs))
    if slack < -1e-6:
        raise SystemExit(f"tray {tray.letter}: rows need {-slack:.1f} mm more depth")
    total = sum(hs)
    hs = [h + slack * h / total for h in hs]
    W = inner_w(tray.nx)
    y = WALL
    tray.rows, tray.ledges = [], []
    for items, h in zip(rows, hs):
        ws = row_widths(items, h, depth)
        free = W - sum(ws) - DIVIDER * (len(items) - 1)
        ws = [w + free * w / sum(ws) for w in ws]
        x = WALL
        cells = []
        for it, w in zip(items, ws):
            cells.append(Cell(it, x, x + w, y, y + h, depth))
            x += w + DIVIDER
        tray.rows.append(cells)
        tray.ledges.append((y + h, y + h + LEDGE))
        y += h + LEDGE
    over = [c for r in tray.rows for c in r if c.fill > FILL_MAX + 1e-9]
    if over:
        raise SystemExit("compartments over the fill limit: " + "; ".join(
            f"{c.item.bom} {c.fill:.0%}" for c in over))
    small = [c for r in tray.rows for c in r if c.w < MIN_W - 1e-6 or c.h < MIN_H - 1e-6]
    if small:
        raise SystemExit("compartments under the finger floor: "
                         + "; ".join(c.item.bom for c in small))


# ------------------------------------------------------------------ solids
def rr_wire(w: float, d: float, r: float, z: float, cx: float, cy: float):
    import cadquery as cq
    face = cq.Sketch().rect(w, d).vertices().fillet(r)._faces.Faces()[0]
    return face.outerWire().moved(cq.Location(cq.Vector(cx, cy, z)))


def rr_prism(w: float, d: float, r: float, x: float, y: float, z0: float, h: float):
    """Rounded-rectangle prism with its min corner at (x, y), from z0 up h."""
    import cadquery as cq
    return (cq.Workplane("XY").workplane(offset=z0).center(x + w / 2, y + d / 2)
            .rect(w, d).extrude(h).edges("|Z").fillet(r)).val()


def profile_loft(cx: float, cy: float, w: float, d: float, r: float,
                 sections: list[tuple[float, float]]):
    """Ruled loft through rounded rectangles: each section (inset from w x d, z)."""
    import cadquery as cq
    wires = [rr_wire(w - 2 * s, d - 2 * s, max(r - s, 0.05), z, cx, cy) for s, z in sections]
    return cq.Solid.makeLoft(wires, True)


def base_unit(cx: float, cy: float):
    """One Gridfinity base: the spec profile swept round a 41.5 square, r 3.75 at the top."""
    top = GRID - GAP
    zmax = BASE_PROFILE[-1][1]
    return profile_loft(cx, cy, top, top, BASE_TOP_R,
                        [(BASE_PROFILE[-1][0] - x, z) for x, z in BASE_PROFILE])


def lip_cut(tray: Tray):
    """The void inside the stacking lip: inner tip WALL in from the outside at the bin height,
    the spec's 0.7 / 1.8 / 1.9 profile up and out, carried past the top."""
    zb = UNIT_H * tray.u
    secs = [(LIP_DEPTH - x, zb + z) for x, z in LIP_PROFILE]
    secs.append((-1.0, zb + LIP_H + 1.0))
    return profile_loft(tray.W / 2, tray.D / 2, tray.W, tray.D, BASE_TOP_R, secs)


def build_shell(tray: Tray, holes: str = "none", hollow: bool = False):
    """The Gridfinity bin without compartments: bases, body, the stacking lip, the empty space
    above the rim inside the walls, and optional holes. `hollow` also clears the interior down
    to the floor (the plain bin `--validate` compares with a reference)."""
    import cadquery as cq
    W, D, u = tray.W, tray.D, tray.u
    zb = UNIT_H * u
    top = zb + LIP_H - LIP_TOP_FLAT          # lip cut back to a flat LIP_TOP_FLAT wide
    zf = BASE_PROFILE[-1][1]
    body = rr_prism(W, D, BASE_TOP_R, 0, 0, zf, top - zf)
    feet = [base_unit(GRID / 2 - GAP / 2 + GRID * i, GRID / 2 - GAP / 2 + GRID * j)
            for i in range(tray.nx) for j in range(tray.ny)]
    z0 = FLOOR_Z if hollow else rim_z(u)
    cuts = [rr_prism(W - 2 * WALL, D - 2 * WALL, BASE_TOP_R - WALL, WALL, WALL, z0, zb - z0),
            lip_cut(tray)]
    if holes != "none":
        dia, depth = (MAGNET_D, MAGNET_DEPTH) if holes == "magnet" else (SCREW_D, SCREW_DEPTH)
        off = GRID / 2 - HOLE_FROM_SIDE
        for i in range(tray.nx):
            for j in range(tray.ny):
                ux, uy = GRID / 2 - GAP / 2 + GRID * i, GRID / 2 - GAP / 2 + GRID * j
                for sx, sy in itertools.product((-1, 1), repeat=2):
                    cuts.append(cq.Workplane("XY").center(ux + sx * off, uy + sy * off)
                                .circle(dia / 2).extrude(depth).translate((0, 0, -0.01)).val())
    return body.fuse(*feet).cut(*cuts)


def build_tray(tray: Tray, holes: str = "none"):
    import cadquery as cq
    W, u = tray.W, tray.u
    zb = UNIT_H * u
    rim = rim_z(u)
    cuts, adds = [], []
    for row, (ly0, ly1) in zip(tray.rows, tray.ledges):
        cuts.append(cq.Workplane("XY").box(W - 2 * WALL, ly1 - ly0, EMBOSS + 0.01,
                                           centered=False)
                    .translate((WALL, ly0, rim - EMBOSS)).val())
        for c in row:
            cav = rr_prism(c.w, c.h, R_CAV, c.x0, c.y0, FLOOR_Z, zb + LIP_H)
            cuts.append(cav)
            r = c.scoop
            wedge = cq.Workplane("XY").box(c.w, r, r, centered=False).translate(
                (c.x0, c.y0, FLOOR_Z))
            roll = (cq.Workplane("YZ").workplane(offset=c.x0 - 1)
                    .center(c.y0 + r, FLOOR_Z + r).circle(r).extrude(c.w + 2))
            adds.append(wedge.cut(roll).intersect(cq.Workplane().add(cav)).val())
            cx = (c.x0 + c.x1) / 2
            for txt, cap, yy in ((c.item.line1, CAP1, ly1 - 1.2 - CAP1 / 2),
                                 (c.item.line2, CAP2, ly0 + 1.2 + CAP2 / 2)):
                adds.extend(text_solid(txt, cap, EMBOSS + 0.2)
                            .translate((cx, yy, rim - EMBOSS - 0.2)).vals())
    solid = build_shell(tray, holes).cut(*cuts).fuse(*adds)
    zf = BASE_PROFILE[-1][1]
    name = front_text(f"TRAY {tray.letter} · {tray.title}", NAME_CAP, W / 2, (zf + zb) / 2)
    return solid.cut(*name.vals()).clean()


def section_crossings(tris, x0: float, z: float) -> list[float]:
    """y values where the mesh's section by the plane x = x0 crosses height z, sorted."""
    import numpy as np
    d = tris[:, :, 0] - x0
    ys = []
    for t, dd in zip(tris, d):
        if (dd > 0).all() or (dd < 0).all():
            continue
        pts = []
        for i, j in ((0, 1), (1, 2), (2, 0)):
            if (dd[i] > 0) != (dd[j] > 0):
                f = dd[i] / (dd[i] - dd[j])
                pts.append(t[i] + f * (t[j] - t[i]))
        if len(pts) == 2:
            (y1, z1), (y2, z2) = pts[0][1:], pts[1][1:]
            if (z1 - z) * (z2 - z) <= 0 and z1 != z2:
                ys.append(y1 + (z - z1) / (z2 - z1) * (y2 - y1))
    return sorted(ys)


def validate(ref: Path) -> list[str]:
    """Compare a plain 1 x 1 x 6U bin from this script with a reference Gridfinity bin STL, in
    the section through the unit's centre: the outside of the base (z 0-4.75), the outside of
    the wall, and the inside of the stacking lip (from the bin height up to the lower of the two
    tops). Returns report lines; each mesh is centred on its bounding box, bottom at z 0."""
    import numpy as np
    from geom import read_stl
    t = Tray("V", [], 1, 1, 6)
    with tempfile.TemporaryDirectory() as td:
        ours_p = Path(td) / "ours.stl"
        export_stl(build_shell(t, hollow=True), ours_p)
        ours = np.array(read_stl(ours_p), float)
    refm = np.array(read_stl(ref), float)
    for m in (ours, refm):
        lo, hi = m.reshape(-1, 3).min(0), m.reshape(-1, 3).max(0)
        m[:, :, :2] -= (lo[:2] + hi[:2]) / 2
        m[:, :, 2] -= lo[2]
    ref_top = refm[:, :, 2].max()
    ours_top = ours[:, :, 2].max()
    zb = UNIT_H * t.u
    z_lip = min(ref_top, ours_top) - 0.05
    zones = {"base outside (z 0.05-4.7)": (0.05, 4.7, "outer"),
             f"wall outside (z 5-{zb - 0.1:g})": (5.0, zb - 0.1, "outer"),
             f"lip inside (z {zb:g}-{z_lip:.2f})": (zb + 0.05, z_lip, "inner")}
    out = []
    for name, (z0, z1, side) in zones.items():
        worst, at = 0.0, None
        for z in np.arange(z0, z1 + 1e-9, 0.05):
            vals = []
            for m in (ours, refm):
                ys = [y for y in section_crossings(m, 0.0, float(z)) if y > 0]
                vals.append(max(ys) if side == "outer" else min(ys))
            dev = abs(vals[0] - vals[1])
            if dev > worst:
                worst, at = dev, (float(z), vals[0], vals[1])
        out.append(f"{name}: max deviation {worst:.3f} mm"
                   + (f" at z {at[0]:.2f} (ours {at[1]:.3f}, reference {at[2]:.3f})" if at else ""))
    out.append(f"overall height: ours {ours_top:.2f} mm, reference {ref_top:.2f} mm "
               f"(spec {UNIT_H * t.u + LIP_H:g}; ours cuts the lip's knife edge back to a "
               f"{LIP_TOP_FLAT} mm flat)")
    return out


def export_stl(shape, path: Path, tol: float = 0.05, ang: float = 0.3) -> None:
    """Binary STL from one OCCT tessellation of the whole solid (0.05 mm chord error).
    Deterministic; refuses a mesh that is not closed or is inside out."""
    import struct
    import numpy as np
    shape = shape.val() if hasattr(shape, "val") else shape
    verts, tris = shape.tessellate(tol, ang)
    V = np.array([v.toTuple() for v in verts], dtype=np.float64)
    T = np.array(tris, dtype=np.int64)
    _u, inv = np.unique(np.round(V, 5), axis=0, return_inverse=True)
    I = inv.ravel()[T]
    edges = np.sort(np.stack([I, I[:, [1, 2, 0]]], -1).reshape(-1, 2), axis=1)
    _e, counts = np.unique(edges, axis=0, return_counts=True)
    if (counts != 2).any():
        raise SystemExit(f"{path.name}: tessellation is not closed ({(counts != 2).sum()} edges)")
    a, b, c = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]
    if np.einsum("ij,ij->i", a, np.cross(b, c)).sum() <= 0:
        raise SystemExit(f"{path.name}: tessellation is inside out")
    n = np.cross(b - a, c - a)
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    rec = np.zeros(len(T), dtype=np.dtype([("n", "<f4", 3), ("v", "<f4", 9), ("a", "<u2")]))
    rec["n"] = n
    rec["v"] = np.concatenate([a, b, c], 1)
    path.write_bytes(b"gen_trays.py".ljust(80, b" ") + struct.pack("<I", len(T)) + rec.tobytes())


# ------------------------------------------------------------------ slicer
PRINT = "0.20mm BALANCED @COREONE HF0.4"
FILAMENT = "Prusament PLA @COREONE HF0.4"


def write_ini(path: Path) -> None:
    """Flatten the three system presets (resolve_preset.py, as build_config.py does) plus this
    repo's printer-wide lines: the vendored cold start and the AFS flap lift for PLA."""
    from resolve_preset import load_bundle, resolve
    from build_config import (BASE_PRINTER, FLAPS_OFF, FLAPS_ON, _append_gcode, bundle_version,
                              cold_start_gcode)
    sections = load_bundle()
    cfg: dict[str, str] = {}
    cfg.update(resolve(sections, "print", PRINT))
    fil = resolve(sections, "filament", FILAMENT)
    cfg.update(fil)
    cfg.update(resolve(sections, "printer", BASE_PRINTER))
    cfg.update([
        ("start_gcode", cold_start_gcode()),
        ("start_filament_gcode", _append_gcode(fil["start_filament_gcode"], FLAPS_ON)),
        ("end_filament_gcode", _append_gcode(fil["end_filament_gcode"], FLAPS_OFF)),
        ("support_material", "0"),
        ("support_material_auto", "0"),
    ])
    cfg["print_settings_id"] = PRINT
    cfg["filament_settings_id"] = f"{FILAMENT} - bench trays"
    cfg["printer_settings_id"] = BASE_PRINTER
    for junk in ("renamed_from", "compatible_prints", "compatible_printers",
                 "compatible_printers_condition", "compatible_prints_condition"):
        cfg.pop(junk, None)
    head = (f"# Bench hardware trays: {PRINT} + {FILAMENT} + {BASE_PRINTER}, flattened from the\n"
            f"# PrusaSlicer bundle {bundle_version(sections)} by slicer/bench/hardware-trays/gen_trays.py\n")
    path.write_text(head + "\n".join(f"{k} = {v}" for k, v in sorted(cfg.items())) + "\n")


def bed_centre(ini: Path) -> tuple[float, float, float, float]:
    shape = re.search(r"^bed_shape = (.+)$", ini.read_text(), re.M).group(1)
    pts = [tuple(float(v) for v in p.split("x")) for p in shape.split(",")]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, max(xs) - min(xs), max(ys) - min(ys)


def make_project(stl: Path, ini: Path, name: str) -> tuple[Path, str]:
    from build_plates import PRUSA, inject_3mf, run
    cx, cy, _bw, _bd = bed_centre(ini)
    dst = HERE / f"{name}.3mf"
    p = run([PRUSA, "--load", str(ini), "--dont-arrange", "--center", f"{cx:g},{cy:g}",
             "--export-3mf", "-o", str(dst), str(stl)])
    inject_3mf(dst, ini, {}, {stl.name: name})
    return dst, (p.stdout + p.stderr).strip()


def slice_project(project: Path, tmp: Path, colour_z: list[float]) -> dict:
    from build_plates import PRUSA, read_footer, run
    gcode = tmp / (project.stem + ".gcode")
    p = run([PRUSA, "--dont-arrange", "--binary-gcode=0", "--export-gcode", "-o", str(gcode),
             str(project)])
    hours, grams, raw, cfg = read_footer(gcode)
    text = gcode.read_text(errors="replace")
    for key, want in (("support_material", "0"), ("layer_height", "0.2"),
                      ("filament_type", "PLA"), ("print_settings_id", PRINT)):
        if cfg.get(key) != want:
            raise SystemExit(f"{project.name}: sliced with {key} = {cfg.get(key)!r}, want {want!r}")
    if "M106 P3 S160" not in text:
        raise SystemExit(f"{project.name}: the AFS flap line did not reach the G-code")
    log = (p.stdout + p.stderr).strip()
    # The 2.9.6 stability check flags the first layer over the base grooves (z 4.75-5.0, a
    # 0.5 mm gap running the length of the bin, which every Gridfinity bin bridges) as "Long
    # bridging extrusions". That one is expected; any other issue stops the script.
    issues = []
    m = re.search(r"Detected print stability issues:\s*\n\s*\n?\S+\s*\n(.+)", log)
    if m:
        issues = [x.strip() for x in m.group(1).split(",")]
        unexpected = [x for x in issues if x != "Long bridging extrusions"]
        if unexpected:
            raise SystemExit(f"{project.name}: slicer stability issues {unexpected}:\n{log}")
    xs, ys = [], []
    for m in re.finditer(r"^G1 (?:[^;\n]*?)X([-\d.]+) Y([-\d.]+)[^;\n]*E[\d.]", text, re.M):
        xs.append(float(m.group(1)))
        ys.append(float(m.group(2)))
    zs = {round(float(z), 2) for z in re.findall(r"^;Z:([\d.]+)", text, re.M)}
    missing = [z for z in colour_z if round(z, 2) not in zs]
    if missing:
        raise SystemExit(f"{project.name}: layers {missing} missing - the colour-change Z in "
                         "README.md would be wrong")
    return dict(hours=hours, grams=grams, raw=raw, log=log, issues=issues, xmin=min(xs), xmax=max(xs),
                ymin=min(ys), ymax=max(ys), zmax=max(zs), perimeters=cfg.get("perimeters"),
                fill=cfg.get("fill_density"), support=cfg.get("support_material"))


# ------------------------------------------------------------------ render
def render(stl: Path, out: Path, azim: float, elev: float, accent_z: float,
           px: int = 2000) -> None:
    """Orthographic z-buffer render (scripts/cad_render/render.py). Everything above the label
    ledges (labels, divider tops, the lip: the colour-change layers) is drawn in the accent
    blue; edges only where the surface turns (> ~20 deg), steps to another plane, or changes
    colour, so the glyphs stay legible."""
    import numpy as np
    from PIL import Image
    from render import basis, compose, project, shade
    from geom import read_stl
    tris = np.array(read_stl(stl), dtype=np.float64)
    V = tris.reshape(-1, 3)
    T = np.arange(len(V)).reshape(-1, 3)
    top = tris[:, :, 2].mean(1) > accent_z + 0.01
    body, accent = np.array([0.66, 0.67, 0.70]), np.array([0x1F, 0x4E, 0x9C]) / 255
    cols = np.where(top[:, None], accent, body)
    n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    M = basis(azim, elev)
    lo, hi = V.min(0), V.max(0)
    centre = (lo + hi) / 2
    c = (V - centre) @ M.T
    ss = 2
    W = px
    Hh = int(round(px * np.ptp(c[:, 1]) / np.ptp(c[:, 0]))) + 24
    scale = (W * ss * 0.97) / np.ptp(c[:, 0])
    scr = project(V, M, centre, scale, W * ss, Hh * ss)
    rgb, mask, tid = compose(scr, T, shade(V, T, cols), W * ss, Hh * ss)
    nb = np.zeros(tid.shape + (3,))
    nb[mask] = n[tid[mask]]
    cb = np.full(tid.shape, -1)
    cb[mask] = top[tid[mask]]
    off = (n * tris[:, 0]).sum(1)
    ob = np.zeros(tid.shape)
    ob[mask] = off[tid[mask]]
    edge = np.zeros(tid.shape, bool)
    for ax in (0, 1):
        edge |= ((nb * np.roll(nb, 1, ax)).sum(-1) < 0.94) | (cb != np.roll(cb, 1, ax)) \
            | (np.abs(ob - np.roll(ob, 1, ax)) > 0.3)
    edge &= mask | np.roll(mask, 1, 0) | np.roll(mask, 1, 1)
    rgb[edge] *= 0.45
    img = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype("uint8"))
    img.resize((W, Hh), Image.LANCZOS).save(out, optimize=True)


# ------------------------------------------------------------------ README blocks
def put_block(name: str, body: str) -> None:
    text = README.read_text()
    a, b = f"<!-- BEGIN generated:{name} -->", f"<!-- END generated:{name} -->"
    if a not in text or b not in text:
        raise SystemExit(f"README.md has no {a} ... {b} block")
    pre, rest = text.split(a, 1)
    _old, post = rest.split(b, 1)
    README.write_text(f"{pre}{a}\n{body.rstrip()}\n{b}{post}")


def candidates(items: list[Item], n: int = 5) -> list[tuple[int, int, int]]:
    """The n smallest footprints that hold the group, each at its lowest height."""
    out = []
    for nx in range(1, UNITS_MAX + 1):
        for ny in range(1, UNITS_MAX + 1):
            for u in HEIGHT_RANGE:
                if needed_y(items, u, nx) <= GRID * ny - GAP:
                    out.append((nx, ny, u))
                    break
    return sorted(out, key=lambda c: (c[0] * c[1], c[2], -c[0]))[:n]


def sizes_md(trays: list[Tray]) -> str:
    out = ["Usable depth (floor to rim) by height: "
           + ", ".join(f"{u}U {usable_depth(u):.1f} mm" for u in HEIGHT_RANGE) + ".", "",
           "| tray | chosen | other footprints that hold it (lowest U each) |", "|---|---|---|"]
    for t in trays:
        others = [c for c in candidates(t.items) if c != (t.nx, t.ny, t.u)][:4]
        out.append(f"| {t.letter} | {t.nx} × {t.ny} × {t.u}U | "
                   + ", ".join(f"{a} × {b} × {u}U" for a, b, u in others) + " |")
    return "\n".join(out)


def rugged_fit(trays: list[Tray]) -> str:
    """Which trays fit the 5 x 4, 6U rugged case, alone and together (exact cover search)."""
    def fits(rects, W=5, H=4) -> bool:
        grid = [[False] * W for _ in range(H)]
        def place(i):
            if i == len(rects):
                return True
            for w, h in {rects[i], rects[i][::-1]}:
                for y in range(H - h + 1):
                    for x in range(W - w + 1):
                        if all(not grid[y + j][x + k] for j in range(h) for k in range(w)):
                            for j in range(h):
                                for k in range(w):
                                    grid[y + j][x + k] = True
                            if place(i + 1):
                                return True
                            for j in range(h):
                                for k in range(w):
                                    grid[y + j][x + k] = False
            return False
        return place(0)
    ok = [t for t in trays if t.u <= 6 and fits([(t.nx, t.ny)])]
    together = fits([(t.nx, t.ny) for t in ok]) if ok else False
    if not ok:
        return "None of the trays fits the 5 × 4 rugged case."
    names = ", ".join(t.letter for t in ok)
    return (f"Trays {names} fit the 5 × 4, 6U rugged case"
            + (" together." if together and len(ok) > 1 else
               "." if len(ok) == 1 else ", but not all at once.")
            + ("" if len(ok) == len(trays) else
               " " + ", ".join(t.letter for t in trays if t not in ok) + " does not."))


def stacking(trays: list[Tray]) -> str:
    """A bin's feet land on the stacking lip only round the rim of a bin of the same footprint."""
    groups: dict[tuple[int, int], list[str]] = {}
    for t in trays:
        groups.setdefault(tuple(sorted((t.nx, t.ny))), []).append(t.letter)
    same = [v for v in groups.values() if len(v) > 1]
    txt = ("Stacking: a bin rests on another bin's stacking lip only if both have the same footprint "
           "(the lip runs round the rim, so a smaller bin's feet would drop inside). ")
    if same:
        txt += "; ".join(" and ".join(v) for v in same) + " stack on each other"
        lone = [v[0] for v in groups.values() if len(v) == 1]
        txt += (f"; {', '.join(lone)} stack{'s' if len(lone) == 1 else ''} with nothing."
                if lone else ".")
    else:
        txt += "No two trays share a footprint, so none stacks on another."
    return txt


def layout_md(trays: list[Tray], skipped: list[str], choice: str) -> str:
    out = [f"Generated from `scripts/data/ldo-350-bom.yml` (box *{BOX}*, fetched "
           f"{yaml.safe_load(BOM.read_text()).get('fetched')}). Each tray is sized on its own: "
           f"the smallest footprint, then the lowest height, that holds its group at ≤ "
           f"{FILL_MAX:.0%} fill with the finger floor.", "", choice, "", sizes_md(trays), "",
           stacking(trays), rugged_fit(trays), "",
           ]
    for t in trays:
        n = sum(len(r) for r in t.rows)
        worst = max((c for r in t.rows for c in r), key=lambda c: c.fill)
        out += [f"**Tray {t.letter} — {t.title}:** Gridfinity {t.nx} × {t.ny} × {t.u}U "
                f"({t.W:g} × {t.D:g} × {UNIT_H * t.u:g} mm + lip), {n} compartments in "
                f"{len(t.rows)} rows (row 1 is the front); fullest {worst.item.line1} "
                f"{worst.item.line2.split()[0]} at {worst.fill:.0%}.", "",
                "| row | label | count | piece envelope mm | φ | bulk cm³ | size mm | usable cm³ "
                "| fill |",
                "|---:|---|---:|---|---:|---:|---|---:|---:|"]
        for ri, row in enumerate(t.rows, 1):
            for c in row:
                it = c.item
                out.append(f"| {ri} | {it.line1} · {it.line2} | {it.qty} | {it.env_desc} | "
                           f"{it.phi:.2f} | {it.bulk / 1000:.1f} | {c.w:.0f} × {c.h:.0f} × "
                           f"{c.depth:.1f} | {c.usable / 1000:.1f} | {c.fill:.0%} |")
        out.append("")
    out += ["Piece data and sources:", "",
            "| BOM item | solid mm³ | envelope mm³ | solid/bulk | source |",
            "|---|---:|---:|---:|---|"]
    for t in trays:
        for it in t.items:
            out.append(f"| {it.bom} | {it.solid:.0f} | {it.env:.0f} | "
                       f"{it.solid * it.phi / it.env:.2f} | {it.source} |")
    out += ["", "Not in a compartment: " + "; ".join(skipped) + "."]
    return "\n".join(out)


def colour_z(t: Tray) -> float:
    """Top of the first layer above the label ledges: where a colour change takes the labels."""
    return rim_z(t.u) - EMBOSS + 0.2


def slice_md(results: list[tuple[str, dict]]) -> str:
    out = ["| file | bin | time | g PLA | colour change Z | extents on the bed, mm | supports |",
           "|---|---|---|---:|---:|---|---|"]
    th, tg = 0.0, 0.0
    for name, r in results:
        th += r["hours"]
        tg += r["grams"]
        out.append(f"| `{name}.3mf` | {r['size']} | {r['raw']} | {r['grams']:.0f} | "
                   f"{r['colour_z']:.2f} | X {r['xmin']:.1f}–{r['xmax']:.1f}, "
                   f"Y {r['ymin']:.1f}–{r['ymax']:.1f}, Z ≤ {r['zmax']:.2f} | "
                   f"{'none' if r['support'] == '0' else r['support']} |")
    warned = sorted({i for _n, r in results for i in r["issues"]})
    note = ("no slicer warnings" if not warned else
            "slicer stability notes: " + ", ".join(warned) + " (the base grooves, expected)")
    out += ["", f"All trays: **{th:.1f} h, {tg:.0f} g**. PrusaSlicer 2.9.6 CLI estimates, one "
            f"tray per bed, not GUI-arranged; {r['perimeters']} perimeters, {r['fill']} infill; "
            f"{note}. The colour-change Z is the first label layer, checked against each G-code."]
    return "\n".join(out)


# ------------------------------------------------------------------ driver
def group_split(items: list[Item]) -> list[int]:
    """The default split: M2/M3 screws | M4/M5 screws | everything else."""
    return [k for k in range(1, len(items)) if (items[k].group, items[k].order[0])
            != (items[k - 1].group, items[k - 1].order[0])]


def sized(items: list[Item], cs: list[int]) -> list[tuple[list[Item], tuple]] | None:
    bounds = [0, *cs, len(items)]
    out = []
    for a, b in zip(bounds, bounds[1:]):
        size = size_group(items[a:b])
        if size is None:
            return None
        out.append((items[a:b], size))
    return out


def bin_units(groups) -> int:
    """Plastic proxy: the sum of n x m x U over the trays."""
    return sum(nx * ny * u for _g, (nx, ny, u) in groups)


def choose(items: list[Item], least_units: bool = False) -> tuple[list[Tray], str]:
    """Each tray sized on its own (size_group). The group split stays unless another contiguous
    split (cut only between screw bands or between families of the rest) needs fewer trays;
    the split with the fewest bin units (any tray count) is reported, and `least_units` picks
    it instead."""
    default = sized(items, group_split(items))
    if default is None:
        raise SystemExit("a group does not fit a 5 x 5 x 6U bin: check the BOM counts")
    fewer, lean = None, None
    for k in range(1, 6):
        for cs in itertools.combinations(cut_points(items), k - 1):
            if list(cs) == group_split(items):
                continue
            g = sized(items, list(cs))
            if g is None:
                continue
            if len(g) < len(default) and (fewer is None or
                                          (len(g), bin_units(g)) < (len(fewer), bin_units(fewer))):
                fewer = g
            if bin_units(g) < bin_units(default) and (lean is None or
                                                      (bin_units(g), len(g)) < (bin_units(lean), len(lean))):
                lean = g

    def desc(g) -> str:
        return (f"{len(g)} trays, {bin_units(g)} bin units: "
                + " + ".join(f"{tray_title(it)} {nx}×{ny}×{u}U" for it, (nx, ny, u) in g))
    lines = [f"Group split (A = M2/M3 screws, B = M4/M5 screws, C = the rest): {desc(default)}. "
             "Bin units = Σ n·m·U, a plastic proxy."]
    lines.append(f"Fewer trays: {desc(fewer)}." if fewer else
                 "No split needs fewer trays.")
    lines.append(f"Fewest bin units: {desc(lean)}." if lean else
                 "No split needs fewer bin units.")
    chosen = fewer or default
    if least_units and lean:
        chosen = lean
    lines.append("Chosen: " + ("the group split." if chosen is default else
                               "the fewest-units split (--least-units)." if chosen is lean else
                               "the split with fewer trays."))
    trays = [Tray(chr(ord("A") + i), it, nx, ny, u) for i, (it, (nx, ny, u)) in enumerate(chosen)]
    return trays, " ".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--plan", action="store_true", help="print options and fill, write nothing")
    ap.add_argument("--no-slice", action="store_true", help="skip PrusaSlicer")
    ap.add_argument("--holes", choices=("none", "magnet", "screw"), default="none",
                    help="Gridfinity base holes (default none: Clickfinity holds bins without)")
    ap.add_argument("--copy-renders", type=Path, help="also copy the PNGs here")
    ap.add_argument("--least-units", action="store_true",
                    help="use the split with the fewest bin units even if it adds a tray")
    ap.add_argument("--validate", type=Path, metavar="REF_STL",
                    help="compare a plain 1x1x6U bin with a reference Gridfinity bin and stop")
    args = ap.parse_args()
    if args.validate:
        for line in validate(args.validate):
            print(line)
        return 0

    items, skipped = load_items()
    trays, choice = choose(items, args.least_units)
    print(choice)
    for t in trays:
        layout(t)
        print(f"\nTray {t.letter} ({t.title}) {t.nx}x{t.ny}x{t.u}U = {t.W:g} x {t.D:g} mm")
        print(f"  {'type':<28}{'count':>6} {'envelope':<22}{'phi':>5}{'bulk':>8}{'usable':>8}"
              f"{'fill':>6}")
        for row in t.rows:
            for c in row:
                it = c.item
                print(f"  {it.line1 + ' ' + it.line2:<28}{it.qty:>6} {it.env_desc:<22}"
                      f"{it.phi:>5.2f}{it.bulk / 1000:>8.1f}{c.usable / 1000:>8.1f}"
                      f"{c.fill:>6.0%}")
    if args.plan:
        return 0

    RENDERS.mkdir(exist_ok=True)
    keep = {f"tray-{t.letter}" for t in trays}      # drop files of trays that no longer exist
    for old in list(HERE.glob("tray-*.*")) + list(HERE.glob("lid-*.*")) + list(RENDERS.glob("*.png")):
        if old.name.split(".")[0].rsplit("-", 1)[0] not in keep and old.stem not in keep:
            old.unlink()
    stls = {}
    for t in trays:
        name = f"tray-{t.letter}"
        path = HERE / f"{name}.stl"
        export_stl(build_tray(t, args.holes), path)
        stls[name] = path
        print(f"wrote {path.relative_to(REPO)}")
        for view, az, el in (("top", -90.0, 90.0), ("34", -60.0, 38.0)):
            out = RENDERS / f"{name}-{view}.png"
            render(path, out, az, el, rim_z(t.u) - EMBOSS)
            print(f"wrote {out.relative_to(REPO)}")
            if args.copy_renders:
                args.copy_renders.mkdir(parents=True, exist_ok=True)
                for stale in args.copy_renders.glob("*.png"):
                    if not (RENDERS / stale.name).exists():
                        stale.unlink()
                shutil.copy2(out, args.copy_renders / out.name)
    put_block("layout", layout_md(trays, skipped, choice))

    if args.no_slice:
        return 0
    tmp = Path(tempfile.mkdtemp(prefix="trays-"))
    try:
        ini = tmp / "bench-trays-pla.ini"
        write_ini(ini)
        _cx, _cy, bw, bd = bed_centre(ini)
        results = []
        for name in stls:
            proj, log = make_project(stls[name], ini, name)
            t = next(t for t in trays if f"tray-{t.letter}" == name)
            r = slice_project(proj, tmp, [rim_z(t.u) - EMBOSS, colour_z(t), rim_z(t.u)])
            r["colour_z"], r["size"] = colour_z(t), f"{t.nx} × {t.ny} × {t.u}U"
            if not (0 <= r["xmin"] and r["xmax"] <= bw and 0 <= r["ymin"] and r["ymax"] <= bd):
                raise SystemExit(f"{name}: extrusion outside the {bw:g} x {bd:g} bed: {r}")
            print(f"\n== {name}: {r['raw']}, {r['grams']:.1f} g, X {r['xmin']}-{r['xmax']} "
                  f"Y {r['ymin']}-{r['ymax']} Z<={r['zmax']}\n{log or '(slicer: no output)'}"
                  f"\n{r['log'] or ''}")
            results.append((name, r))
        put_block("slice", slice_md(results))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
