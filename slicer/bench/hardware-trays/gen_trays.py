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
# Plastic levers (ideas from HuMa's "Gridfinity Ultra Light Bins", Printables 627719; no
# geometry used). All on by default; `--levers` picks a subset for the per-lever comparison.
LEVER_NAMES = ("settings", "thin", "ledges", "coves", "base")
# Hollow ledges and coves cost plastic at 10 % infill (each void adds two perimeters per layer,
# more than the sparse infill it replaces; README § Ultra-light), so they are off by default.
DEFAULT_LEVERS = ("settings", "thin", "base")
LEVERS: set[str] = set(DEFAULT_LEVERS)
# Two perimeters of the HF0.4 BALANCED preset: width w = 0.45 at 0.2 mm layers, spacing
# w - h(1 - pi/4) = 0.407, so two lines make w + spacing = 0.857 mm: a 0.86 wall slices as
# exactly two perimeters, no gap fill.
T2 = 0.86
FLOOR_PLATE_TOP = 5.8       # hollow base: floor plate from the base top (4.75) to 5.8 (5 layers)
POCKET_FLOOR = 0.6          # hollow base: the foot pocket's floor, three 0.2 mm layers
SHELF = 1.0                 # solid under a label ledge's top, above its hollow
WALL = LIP_DEPTH            # outer wall (T2 with the `thin` lever; the lip then sits on a 45° support)
FLOOR_Z = BASE_HEIGHT       # compartment floor (FLOOR_PLATE_TOP with the `base` lever)
DIVIDER = 1.8               # wall between compartments in a row (T2 with `thin`)
R_CAV = 2.8                 # cavity corner radius (rebuilt r_f2; 2.9 with `thin`, so the
                            # outer wall keeps its thickness round the r3.75 corners)


def apply_levers(levers: set[str]) -> None:
    global WALL, FLOOR_Z, DIVIDER, R_CAV
    LEVERS.clear()
    LEVERS.update(levers)
    thin = "thin" in levers
    WALL = T2 if thin else LIP_DEPTH
    DIVIDER = T2 if thin else 1.8
    R_CAV = 2.9 if thin else 2.8
    FLOOR_Z = FLOOR_PLATE_TOP if "base" in levers else BASE_HEIGHT
    _PLAN.clear()


def ring_band() -> float:
    """Height of the 45° support under the lip's inner tip when the wall is thinner than it."""
    return LIP_DEPTH - WALL
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
    def thick(self) -> float:
        """Smallest envelope dimension: how high one piece stands lying flat."""
        return min(float(v) for v in re.findall(r"[\d.]+", self.env_desc))

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

    wall_len: float = 0.0

    @property
    def usable(self) -> float:
        return usable_volume(self.w, self.h, self.depth) - ring_band() ** 2 / 2 * self.wall_len

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
    """The scoop cove is always SCOOP_R (Alex: the rounded front edge is for hard-to-pick-up
    parts; never shrink it to save room). MIN_H and MIN_U keep every compartment longer and
    deeper than it."""
    if h < SCOOP_R + 4 or depth < SCOOP_R + 4:
        raise SystemExit(f"a {h:.1f} x {depth:.1f} mm compartment cannot take the R{SCOOP_R:g} cove")
    return SCOOP_R


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
    return [max(min_w(it) + edge_extra(k, len(items)), (it.need + fixed) / per_w)
            for k, it in enumerate(items)]


def edge_extra(k: int, n: int) -> float:
    """A compartment against a side wall needs its label clear of the lip's support band,
    LIP_DEPTH in from the outside rather than WALL: this much more width."""
    return (LIP_DEPTH - WALL) * ((k == 0) + (k == n - 1))


def label_x(c: "Cell", W_outer: float) -> float:
    """Label centre: the middle of the compartment's span clear of the lip support band."""
    lo = max(c.x0, LIP_DEPTH)
    hi = min(c.x1, W_outer - LIP_DEPTH)
    return (lo + hi) / 2


def row_min_h(items: list[Item], depth: float, nx: int) -> float | None:
    W = inner_w(nx)
    gaps = DIVIDER * (len(items) - 1)
    if sum(min_w(it) + edge_extra(k, len(items)) for k, it in enumerate(items)) + gaps > W:
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
    return WALL + LIP_DEPTH + sum(h + LEDGE for h in plan[1])


DEPTH_MARGIN = 2.0          # a piece lying flat stays this far below the rim
UNITS_MAX = 5               # 5 x 42 - 0.5 = 209.5 mm fits both bed axes (250 x 220)
MIN_U = 4                   # no tray lower than this (Alex: parts must not spill when it tilts)
HEIGHT_RANGE = tuple(range(MIN_U, 7))


def lowest_u(items: list[Item], nx: int, ny: int) -> int | None:
    """Lowest height at which the group fits an nx x ny bin: fill and finger floor, and every
    piece lying flat sits DEPTH_MARGIN below the rim (so a stacked bin cannot catch it)."""
    floor = max(i.thick for i in items) + DEPTH_MARGIN
    for u in HEIGHT_RANGE:
        if usable_depth(u) >= floor and needed_y(items, u, nx) <= GRID * ny - GAP:
            return u
    return None


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
    slack = tray.D - (WALL + LIP_DEPTH + sum(h + LEDGE for h in hs))
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
            c = Cell(it, x, x + w, y, y + h, depth)
            # the lip's 45° support takes a ring_band() x ring_band() / 2 sliver off the top of
            # every cavity side that is the outer wall
            c.wall_len = ((h if abs(x - WALL) < 1e-6 else 0.0)
                          + (h if abs(x + w - (WALL + W)) < 1e-6 else 0.0)
                          + (w if abs(y - WALL) < 1e-6 else 0.0))
            cells.append(c)
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


def foot_pocket(cx: float, cy: float):
    """The void inside a hollow foot: the base profile inset T2, from POCKET_FLOOR up to the base
    top, where the floor plate closes it. Its walls follow the 45° foot profile."""
    top = GRID - GAP
    outer = lambda z: (2.95 - z) if z <= 0.8 else 2.15 if z <= 2.6 else 2.15 - (z - 2.6)
    zs = (POCKET_FLOOR, 0.8, 2.6, BASE_PROFILE[-1][1])
    return profile_loft(cx, cy, top, top, BASE_TOP_R, [(outer(z) + T2, z) for z in zs])


def build_shell(tray: Tray, holes: str = "none", hollow: bool = False):
    """The Gridfinity bin without compartments: bases (hollow with the `base` lever), body, the
    stacking lip, the empty space above the rim inside the lip, and optional holes. `hollow`
    also clears the interior down to the floor (the plain bin `--validate` compares)."""
    import cadquery as cq
    W, D, u = tray.W, tray.D, tray.u
    zb = UNIT_H * u
    top = zb + LIP_H - LIP_TOP_FLAT          # lip cut back to a flat LIP_TOP_FLAT wide
    zf = BASE_PROFILE[-1][1]
    body = rr_prism(W, D, BASE_TOP_R, 0, 0, zf, top - zf)
    centres = [(GRID / 2 - GAP / 2 + GRID * i, GRID / 2 - GAP / 2 + GRID * j)
               for i in range(tray.nx) for j in range(tray.ny)]
    feet = [base_unit(cx, cy) for cx, cy in centres]
    if "base" in LEVERS and holes == "none":
        feet = [f.cut(foot_pocket(cx, cy)) for f, (cx, cy) in zip(feet, centres)]
    z0 = FLOOR_Z if hollow else rim_z(u)
    inset = WALL if hollow else LIP_DEPTH
    cuts = [rr_prism(W - 2 * inset, D - 2 * inset, BASE_TOP_R - inset, inset, inset, z0, zb - z0),
            lip_cut(tray)]
    if holes != "none":
        dia, depth = (MAGNET_D, MAGNET_DEPTH) if holes == "magnet" else (SCREW_D, SCREW_DEPTH)
        off = GRID / 2 - HOLE_FROM_SIDE
        for ux, uy in centres:
            for sx, sy in itertools.product((-1, 1), repeat=2):
                cuts.append(cq.Workplane("XY").center(ux + sx * off, uy + sy * off)
                            .circle(dia / 2).extrude(depth).translate((0, 0, -0.01)).val())
    return body.fuse(*feet).cut(*cuts)


def lip_support(tray: Tray):
    """With a wall thinner than the lip, the solid that carries the lip's inner tip: a 45° ring
    from the wall face (WALL in) at rim - band up to the tip line (LIP_DEPTH in) at the rim,
    then straight up to the bin height. None when the wall is as deep as the lip."""
    band = ring_band()
    if band < 1e-6:
        return None
    rim, zb = rim_z(tray.u), UNIT_H * tray.u
    outer = rr_prism(tray.W, tray.D, BASE_TOP_R, 0, 0, rim - band, zb - rim + band)
    void = profile_loft(tray.W / 2, tray.D / 2, tray.W, tray.D, BASE_TOP_R,
                        [(WALL - 0.01, rim - band - 0.01), (LIP_DEPTH, rim), (LIP_DEPTH, zb + 0.01)])
    return outer.cut(void)


def ledge_void(tray: Tray, ly0: float, ly1: float):
    """Hollow under a label ledge: T2 walls front and back, vertical sides, a 45° roof (no
    support) to an apex SHELF below the ledge top. None if there is no room."""
    import cadquery as cq
    rim = rim_z(tray.u)
    y0, y1 = ly0 + T2, ly1 - T2
    half = (y1 - y0) / 2
    apex = rim - EMBOSS - SHELF
    za = apex - half
    if half < 1.0 or za < FLOOR_Z + 1.0:
        return None
    pts = [(y0, FLOOR_Z), (y1, FLOOR_Z), (y1, za), (y0 + half, apex), (y0, za)]
    return (cq.Workplane("YZ").workplane(offset=WALL).polyline(pts).close()
            .extrude(tray.W - 2 * WALL)).val()


def cove_void(c: Cell):
    """Hollow inside a scoop cove: a right triangle on the floor against the front face, its 45°
    hypotenuse kept T2 inside the cove's arc, T2 behind the front face. None if too small."""
    import cadquery as cq
    r = c.scoop
    s = 2 * r - math.sqrt(2) * (r + T2) - T2
    if s < 1.5 or c.w - 2 * R_CAV < 2:
        return None
    y0 = c.y0 + T2
    pts = [(y0, FLOOR_Z), (y0 + s, FLOOR_Z), (y0, FLOOR_Z + s)]
    return (cq.Workplane("YZ").workplane(offset=c.x0 + R_CAV).polyline(pts).close()
            .extrude(c.w - 2 * R_CAV)).val()


def build_tray(tray: Tray, holes: str = "none"):
    import cadquery as cq
    W, u = tray.W, tray.u
    rim = rim_z(u)
    cuts, adds, voids = [], [], []
    for row, (ly0, ly1) in zip(tray.rows, tray.ledges):
        cuts.append(cq.Workplane("XY").box(W - 2 * WALL, ly1 - ly0, EMBOSS + 0.01,
                                           centered=False)
                    .translate((WALL, ly0, rim - EMBOSS)).val())
        if "ledges" in LEVERS:
            v = ledge_void(tray, ly0, ly1)
            if v is not None:
                voids.append(v)
        for c in row:
            cav = rr_prism(c.w, c.h, R_CAV, c.x0, c.y0, FLOOR_Z, rim - FLOOR_Z + 0.01)
            cuts.append(cav)
            r = c.scoop
            wedge = cq.Workplane("XY").box(c.w, r, r, centered=False).translate(
                (c.x0, c.y0, FLOOR_Z))
            roll = (cq.Workplane("YZ").workplane(offset=c.x0 - 1)
                    .center(c.y0 + r, FLOOR_Z + r).circle(r).extrude(c.w + 2))
            adds.append(wedge.cut(roll).intersect(cq.Workplane().add(cav)).val())
            if "coves" in LEVERS:
                v = cove_void(c)
                if v is not None:
                    voids.append(v)
            cx = label_x(c, W)
            for txt, cap, yy in ((c.item.line1, CAP1, ly1 - 1.2 - CAP1 / 2),
                                 (c.item.line2, CAP2, ly0 + 1.2 + CAP2 / 2)):
                adds.extend(text_solid(txt, cap, EMBOSS + 0.2)
                            .translate((cx, yy, rim - EMBOSS - 0.2)).vals())
    solid = build_shell(tray, holes).cut(*cuts).fuse(*adds)
    if voids:
        solid = solid.cut(*voids)
    ring = lip_support(tray)
    if ring is not None:
        solid = solid.fuse(ring)
    if WALL >= NAME_SINK + 2 * 0.45:     # the name needs two perimeters of wall behind it
        zf = BASE_PROFILE[-1][1]
        name = front_text(f"TRAY {tray.letter} · {tray.title}", NAME_CAP, W / 2,
                          (zf + UNIT_H * u) / 2)
        solid = solid.cut(*name.vals())
    return solid.clean()


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
    if "settings" in LEVERS:
        # Ultra-light print settings: the trays are walls, so perimeters carry them.
        cfg.update([("perimeters", "2"), ("top_solid_layers", "3"), ("bottom_solid_layers", "3"),
                    ("top_solid_min_thickness", "0"), ("bottom_solid_min_thickness", "0"),
                    ("fill_density", "10%")])
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
    gap = text.count(";TYPE:Gap fill")
    return dict(hours=hours, grams=grams, raw=raw, log=log, issues=issues, gapfill=gap,
                top=cfg.get("top_solid_layers"), bottom=cfg.get("bottom_solid_layers"),
                xmin=min(xs), xmax=max(xs),
                ymin=min(ys), ymax=max(ys), zmax=max(zs), perimeters=cfg.get("perimeters"),
                fill=cfg.get("fill_density"), support=cfg.get("support_material"))


# ------------------------------------------------------------------ render
def section_png(stl: Path, x0: float, out: Path, title: str, res: float = 0.05) -> None:
    """A Y-Z section of the STL at x = x0, filled from the mesh itself (crossing parity per
    height), front of the tray on the left."""
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from geom import read_stl
    t = np.array(read_stl(stl), dtype=np.float64)
    d = t[:, :, 0] - x0
    # each crossing triangle contributes exactly two edge points: pair them per triangle
    cross = ((d > 0).any(1)) & ((d < 0).any(1))
    pts = []
    for tri, dd in zip(t[cross], d[cross]):
        q = []
        for i, j in ((0, 1), (1, 2), (2, 0)):
            if (dd[i] > 0) != (dd[j] > 0):
                q.append(tri[i] + dd[i] / (dd[i] - dd[j]) * (tri[j] - tri[i]))
        if len(q) == 2:
            pts.append((q[0][1], q[0][2], q[1][1], q[1][2]))
    S = np.array(pts)
    ymax, zmax = t[:, :, 1].max(), t[:, :, 2].max()
    zs = np.arange(res / 2, zmax, res)
    ys = np.arange(0, ymax, res)
    img = np.zeros((len(zs), len(ys)), bool)
    lo, hi = np.minimum(S[:, 1], S[:, 3]), np.maximum(S[:, 1], S[:, 3])
    for k, z in enumerate(zs):
        m = (lo <= z) & (hi > z)
        if not m.any():
            continue
        s_ = S[m]
        yc = np.sort(s_[:, 0] + (z - s_[:, 1]) / (s_[:, 3] - s_[:, 1]) * (s_[:, 2] - s_[:, 0]))
        for a, b in zip(yc[0::2], yc[1::2]):
            img[k, int(a / res):int(b / res) + 1] = True
    fig = plt.figure(figsize=(16, 16 * zmax / ymax + 1.2), dpi=150)
    ax = fig.add_axes([0.04, 0.12, 0.94, 0.78])
    ax.imshow(img, origin="lower", extent=(0, ymax, 0, zmax), cmap="Blues", vmin=0, vmax=1.6,
              interpolation="nearest", aspect="equal")
    ax.set_xlabel("y, mm (front of the tray at 0)")
    ax.set_ylabel("z, mm")
    ax.set_title(title)
    fig.savefig(out)
    plt.close(fig)


def split_at_z(tris, z0: float):
    """Cut every triangle that crosses the plane z = z0 into pieces wholly above or below it."""
    import numpy as np
    d = tris[:, :, 2] - z0
    cross = (d.max(1) > 0) & (d.min(1) < 0)
    keep = [tris[~cross]]
    new = []
    for t, dd in zip(tris[cross], d[cross]):
        # rotate so vertex 0 is alone on its side
        for k in range(3):
            if (dd[k] > 0) != (dd[(k + 1) % 3] > 0) and (dd[k] > 0) != (dd[(k + 2) % 3] > 0):
                break
        a, b, c = t[k], t[(k + 1) % 3], t[(k + 2) % 3]
        da, db, dc = dd[k], dd[(k + 1) % 3], dd[(k + 2) % 3]
        p = a + (b - a) * (da / (da - db))
        q = a + (c - a) * (da / (da - dc))
        new += [(a, p, q), (p, b, c), (p, c, q)]
    if new:
        keep.append(np.array(new))
    return np.concatenate(keep)


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
    # Split long slivers (wall strips fan-triangulated over 200 mm) before rasterising: the
    # rasteriser's depth interpolation over them let a hidden strip show through the front wall.
    # Edges are split by their own length, so both triangles on an edge split it the same way
    # (no T-junction cracks).
    for _ in range(12):
        L = np.linalg.norm(tris[:, [1, 2, 0]] - tris, axis=2) > 6.0     # edge i: vertex i -> i+1
        if not L.any():
            break
        pieces = [tris[~L.any(1)]]
        for mask_key in range(1, 8):
            pat = L[:, 0] * 1 + L[:, 1] * 2 + L[:, 2] * 4
            sel = pat == mask_key
            if not sel.any():
                continue
            t = tris[sel]
            # rotate so the pattern starts at edge 0
            n_long = bin(mask_key).count("1")
            if n_long == 3:
                a, b, c = t[:, 0], t[:, 1], t[:, 2]
                ab, bc, ca = (a + b) / 2, (b + c) / 2, (c + a) / 2
                pieces += [np.stack(q, 1) for q in ((a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca))]
                continue
            k = {1: 0, 2: 1, 4: 2, 3: 0, 6: 1, 5: 2}[mask_key]
            t = np.roll(t, -k, axis=1)       # long edge(s) now start at edge 0
            a, b, c = t[:, 0], t[:, 1], t[:, 2]
            ab = (a + b) / 2
            if n_long == 1:
                pieces += [np.stack((a, ab, c), 1), np.stack((ab, b, c), 1)]
            else:                            # edges 0 and 1 long
                bc = (b + c) / 2
                pieces += [np.stack((ab, b, bc), 1), np.stack((a, ab, bc), 1), np.stack((a, bc, c), 1)]
        tris = np.concatenate(pieces)
    tris = split_at_z(tris, accent_z + 0.001)       # a clean colour boundary on the walls
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
           "| tray | bin | thickest piece lying flat (mm) | lowest height the fill allows |",
           "|---|---|---:|---|"]
    for t in trays:
        thick = max(i.thick for i in t.items)
        fill_u = next((u for u in HEIGHT_RANGE
                       if needed_y(t.items, u, t.nx) <= t.D), None)
        out.append(f"| {t.letter} | {t.nx} × {t.ny} × {t.u}U | {thick:g} | {fill_u}U |")
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
        txt += "; ".join((", ".join(v[:-1]) + " and " + v[-1]) for v in same)
        txt += " share a footprint: any of them stacks on any other"
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
            "slicer stability notes: " + ", ".join(warned)
            + " (the base grooves and the hollow feet's 40 mm roofs, expected)")
    gaps = sum(r["gapfill"] for _n, r in results)
    out += ["", f"All trays: **{th:.1f} h, {tg:.0f} g**. PrusaSlicer 2.9.6 CLI estimates, one "
            f"tray per bed, not GUI-arranged; {r['perimeters']} perimeters, {r['top']} top / "
            f"{r['bottom']} bottom layers, {r['fill']} infill; {gaps} gap-fill extrusions; "
            f"{note}. The colour-change Z is the first label layer, checked against each G-code."]
    return "\n".join(out)


# ------------------------------------------------------------------ driver
MAX_TRAYS = 3

# Hardware families: the units a tray is made of. A family stays whole.
FAMILIES = (
    ("M2/M3 screws", lambda i: i.group == "screw" and i.order[0] == 0),
    ("M4/M5 screws", lambda i: i.group == "screw" and i.order[0] == 1),
    ("roll-in T-nuts", lambda i: i.order[1] == FAMILY["ROLL-IN"] and i.group == "other"),
    ("hammer-head T-nuts", lambda i: i.order[1] == FAMILY["HAMMER"] and i.group == "other"),
    ("small parts", lambda i: i.group == "other"
     and i.order[1] not in (FAMILY["ROLL-IN"], FAMILY["HAMMER"])),
)


def families(items: list[Item]) -> list[tuple[str, list[Item]]]:
    out = [(name, [i for i in items if pred(i)]) for name, pred in FAMILIES]
    if sorted(i.bom for _n, f in out for i in f) != sorted(i.bom for i in items):
        raise SystemExit("FAMILIES must place every item exactly once")
    return [(n, f) for n, f in out if f]


def set_partitions(xs: list, k_max: int):
    """Every partition of xs into at most k_max blocks."""
    if not xs:
        yield []
        return
    first, rest = xs[0], xs[1:]
    for part in set_partitions(rest, k_max):
        for i in range(len(part)):
            yield part[:i] + [[first] + part[i]] + part[i + 1:]
        if len(part) < k_max:
            yield [[first]] + part


def bin_units(groups) -> int:
    """Plastic proxy: the sum of n x m x U over the trays."""
    return sum(nx * ny * u for _g, (nx, ny, u) in groups)


def size_partition(part, nx: int, ny: int) -> list | None:
    out = []
    for block in part:
        its = sorted((i for _n, f in block for i in f), key=lambda i: i.order)
        u = lowest_u(its, nx, ny)
        if u is None:
            return None
        out.append((its, (nx, ny, u), [n for n, _f in block]))
    out.sort(key=lambda g: g[0][0].order)            # tray A holds the first BOM rows
    return out


def ranked_partitions(items: list[Item]) -> list[list]:
    """Every grouping of whole families into at most MAX_TRAYS trays on one common footprint
    (any n x m up to 5 x 5), each tray at its lowest height, that fits; best first: fewest
    trays, then fewest bin units, then the smallest footprint."""
    fams = families(items)
    parts = list(set_partitions(fams, MAX_TRAYS))
    found = []
    for nx in range(1, UNITS_MAX + 1):
        for ny in range(1, UNITS_MAX + 1):
            for part in parts:
                g = size_partition(part, nx, ny)
                if g:
                    found.append(g)
    found.sort(key=lambda g: (len(g), sum(nx * ny * u for _i, (nx, ny, u), _n in g),
                              g[0][1][0] * g[0][1][1], -g[0][1][0]))
    return found


def partition_desc(g) -> str:
    units = sum(nx * ny * u for _i, (nx, ny, u), _n in g)
    return (f"{len(g)} trays, {units} bin units: "
            + " | ".join(f"{' + '.join(names)} {nx}×{ny}×{u}U" for _i, (nx, ny, u), names in g))


def choose(items: list[Item], rank: int = 0) -> tuple[list[Tray], str, list]:
    """Group whole families into at most MAX_TRAYS trays: fewest trays, then least plastic (bin
    units). `rank` picks a lower-ranked grouping (the slicing comparison uses it)."""
    ranked = ranked_partitions(items)
    if not ranked:
        raise SystemExit(f"no grouping of whole families fits {MAX_TRAYS} trays: check the counts")
    chosen = ranked[rank]
    trays = [Tray(chr(ord("A") + i), its, nx, ny, u)
             for i, (its, (nx, ny, u), _n) in enumerate(chosen)]
    lines = [f"{len(ranked)} groupings of whole families fit ≤ {MAX_TRAYS} trays on one common "
             "footprint, each tray at its lowest height. Best five by bin units (Σ n·m·U, the "
             "plastic proxy):", ""]
    lines += [f"{k + 1}. {partition_desc(g)}" + (" ← chosen" if g is chosen else "")
              for k, g in enumerate(ranked[:5])]
    return trays, "\n".join(lines), ranked


def slice_groupings(groupings: list) -> list[tuple[float, float, list[str]]]:
    """Build and slice each grouping in a temp dir: (grams, hours, per-tray notes) each."""
    import tempfile as _t
    tmp = Path(_t.mkdtemp(prefix="trays-cmp-"))
    ini = tmp / "x.ini"
    write_ini(ini)
    global HERE
    here0, HERE = HERE, tmp
    out = []
    try:
        for k, g in enumerate(groupings):
            th = tg = 0.0
            parts = []
            for i, (its, (nx, ny, u), names) in enumerate(g):
                t = Tray(chr(ord("A") + i), its, nx, ny, u)
                layout(t)
                stl = tmp / f"tray-{k}{t.letter}.stl"
                export_stl(build_tray(t), stl)
                proj, _log = make_project(stl, ini, stl.stem)
                r = slice_project(proj, tmp, [rim_z(u) - EMBOSS, colour_z(t), rim_z(u)])
                th += r["hours"]
                tg += r["grams"]
                parts.append(f"{t.letter} {nx}×{ny}×{u}U {r['raw']} {r['grams']:.0f} g")
            out.append((tg, th, parts))
    finally:
        HERE = here0
        shutil.rmtree(tmp, ignore_errors=True)
    return out


def compare(items: list[Item], n: int) -> int:
    """Real slicing of the n best groupings: confirms the bin-unit proxy."""
    ranked = ranked_partitions(items)[:n]
    for k, (g, (tg, th, parts)) in enumerate(zip(ranked, slice_groupings(ranked))):
        print(f"{k + 1}. {partition_desc(g)}\n   " + "; ".join(parts)
              + f"\n   total {th:.2f} h, {tg:.0f} g")
    return 0


def group_key(g) -> tuple:
    return (len(g), sum(nx * ny * u for _i, (nx, ny, u), _n in g))


def resolve_tie(ranked: list) -> tuple[int, str]:
    """When the best groupings tie on trays and bin units, slice them and keep the lightest."""
    tied = [g for g in ranked if group_key(g) == group_key(ranked[0])]
    if len(tied) < 2:
        return 0, ""
    res = slice_groupings(tied)
    best = min(range(len(tied)), key=lambda k: res[k][0])
    note = (f"{len(tied)} groupings tie at {group_key(tied[0])[1]} bin units; sliced: "
            + "; ".join(f"{k + 1}. {res[k][0]:.0f} g, {res[k][1]:.1f} h" for k in range(len(tied)))
            + f". Chosen: {best + 1}, the lightest.")
    return best, note


def lever_study() -> int:
    """Slice all trays with the levers switched on one at a time, cumulatively (the grouping and
    heights are re-chosen each time, so a lever that frees a height unit shows it)."""
    import tempfile as _t
    global HERE
    here0 = HERE
    steps = [[]] + [list(LEVER_NAMES[:k + 1]) for k in range(len(LEVER_NAMES))]
    for levers in steps:
        apply_levers(set(levers))
        items, _s = load_items()
        trays, _c, _r = choose(items)
        tmp = Path(_t.mkdtemp(prefix="trays-lever-"))
        HERE = tmp
        try:
            ini = tmp / "x.ini"
            write_ini(ini)
            th = tg = 0.0
            parts = []
            for t in trays:
                layout(t)
                stl = tmp / f"tray-{t.letter}.stl"
                export_stl(build_tray(t), stl)
                proj, _log = make_project(stl, ini, stl.stem)
                r = slice_project(proj, tmp, [rim_z(t.u) - EMBOSS, colour_z(t), rim_z(t.u)])
                th += r["hours"]
                tg += r["grams"]
                parts.append(f"{t.letter} {t.nx}×{t.ny}×{t.u}U {r['grams']:.0f} g {r['hours']:.2f} h"
                             f" gap-fill {r['gapfill']}")
            print(f"+{levers[-1] if levers else 'none'}: {tg:.0f} g, {th:.2f} h | "
                  + "; ".join(parts), flush=True)
        finally:
            HERE = here0
            shutil.rmtree(tmp, ignore_errors=True)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--plan", action="store_true", help="print options and fill, write nothing")
    ap.add_argument("--no-slice", action="store_true", help="skip PrusaSlicer")
    ap.add_argument("--holes", choices=("none", "magnet", "screw"), default="none",
                    help="Gridfinity base holes (default none: Clickfinity holds bins without)")
    ap.add_argument("--copy-renders", type=Path, help="also copy the PNGs here")
    ap.add_argument("--levers", default=",".join(DEFAULT_LEVERS),
                    help="plastic levers to apply (comma list of " + ", ".join(LEVER_NAMES)
                    + "; 'none' for the plain bins)")
    ap.add_argument("--lever-study", action="store_true",
                    help="slice the trays with the levers added one at a time, print g and h, stop")
    ap.add_argument("--rank", type=int, default=0,
                    help="build the n-th best grouping instead of the best (0)")
    ap.add_argument("--compare", type=int, metavar="N",
                    help="build and slice the N best groupings in a temp dir, print time and grams, stop")
    ap.add_argument("--validate", type=Path, metavar="REF_STL",
                    help="compare a plain 1x1x6U bin with a reference Gridfinity bin and stop")
    args = ap.parse_args()
    apply_levers(set() if args.levers == "none" else set(args.levers.split(",")) - {""})
    if args.lever_study:
        return lever_study()
    if args.validate:
        for line in validate(args.validate):
            print(line)
        return 0

    items, skipped = load_items()
    trays, choice, ranked = choose(items, args.rank)
    if args.compare:
        return compare(items, args.compare)
    if not args.plan and args.rank == 0:
        best, note = resolve_tie(ranked)
        if note:
            trays, choice, ranked = choose(items, best)
            choice += "\n\n" + note
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
        sec = RENDERS / f"{name}-section.png"
        section_png(path, t.W / 3, sec,
                    f"Tray {t.letter}, {t.nx} × {t.ny} × {t.u}U: Y–Z section at x = {t.W / 3:.0f} mm "
                    f"(the R{SCOOP_R:g} scoop coves on each compartment's front wall)")
        print(f"wrote {sec.relative_to(REPO)}")
        if args.copy_renders:
            args.copy_renders.mkdir(parents=True, exist_ok=True)
            shutil.copy2(sec, args.copy_renders / sec.name)
            shutil.copy2(sec, args.copy_renders / f"section-{t.letter}.png")
        for view, az, el in (("top", -90.0, 90.0), ("34", -60.0, 38.0)):
            out = RENDERS / f"{name}-{view}.png"
            render(path, out, az, el, rim_z(t.u) - EMBOSS)
            print(f"wrote {out.relative_to(REPO)}")
            if args.copy_renders:
                args.copy_renders.mkdir(parents=True, exist_ok=True)
                for stale in args.copy_renders.glob("*.png"):
                    if not (RENDERS / stale.name).exists() and not stale.name.startswith("section-"):
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
