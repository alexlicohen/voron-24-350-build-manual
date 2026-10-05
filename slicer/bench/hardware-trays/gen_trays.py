#!/usr/bin/env python3
"""Generate the bench hardware trays for the LDO Voron 2.4 350 kit's fastener box.

One flat PLA tray per group, a compartment per hardware row of the kit BOM, two raised label
lines on a ledge behind each compartment, a scoop cove along each compartment's front wall,
rounded outer corners, a chamfered first-layer edge, and a drop-on lid per tray.

Everything comes from the data: the rows of box "Fasteners, Tools & Misc" in
scripts/data/ldo-350-bom.yml (re-pinned on kit day, Step 00.2), and the `tool` roles in
scripts/data/hardware-ownership.yml. A row this script cannot classify stops it, so a re-pinned
BOM with a new hardware line fails loudly instead of losing a compartment.

    venv-cq/bin/python slicer/bench/hardware-trays/gen_trays.py            # everything
    venv-cq/bin/python slicer/bench/hardware-trays/gen_trays.py --plan     # layout report only
    venv-cq/bin/python slicer/bench/hardware-trays/gen_trays.py --no-slice # skip the slicer

Writes, next to this file: tray-A.stl, tray-B.stl, lid-A.stl, lid-B.stl, one PrusaSlicer 2.9.6
project per STL (*.3mf, config embedded: 0.20mm BALANCED @COREONE HF0.4 + Prusament PLA
@COREONE HF0.4 + the CORE One HF0.4 printer, with this repo's cold start and AFS flap lines),
renders/*.png, and the generated blocks of README.md.
"""
from __future__ import annotations

import argparse
import math
import re
import shutil
import subprocess
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
# Not in a compartment: cut stock, a 100-pack, two bar handles and the iron tip (Step 00.7).
EXCLUDE = ("Teflon Tube", "Zip Ties", "Aluminium Handle", "Brass Heatset Insert tool")

# ------------------------------------------------------------------ geometry constants (mm)
TRAY_W_MAX, TRAY_D_MAX = 236.0, 206.0   # the lid adds 2 x 2.0, so lid <= 240 x 210 (bed 250 x 220)
FLOOR = 1.6            # 8 layers at 0.2
DEPTH = 20.0           # compartment depth above the floor
H = FLOOR + DEPTH      # 21.6: top of walls and ledges, a layer boundary at 0.2 mm layers
EMBOSS = 0.6           # raised text, rim and divider tops: 21.6 -> 22.2, three 0.2 mm layers
WALL_OUT = 2.4         # outer wall
DIVIDER = 1.8          # wall between compartments in a row (four 0.45 mm lines)
R_OUT = 6.0            # outer vertical corners
R_CAV = R_OUT - WALL_OUT   # cavity corners: keeps the outer wall 2.4 thick round the corners
CHAMFER = 0.6          # first-layer outer edge
SCOOP_R = 10.0         # cove along each compartment's front wall
MIN_W, MIN_H = 25.0, 18.0  # finger floor: compartment width (X) x row height (Y)
PACK = 2.5             # loose-packing factor on the per-piece envelope volume
CAP1, CAP2 = 5.0, 4.0  # label cap heights: line 1 (size), line 2 (type + count)
LEDGE = 1.2 + CAP1 + 1.8 + CAP2 + 1.2   # 13.2: the label ledge behind each row
LABEL_PAD = 3.0        # label width + this <= compartment width
FONT_NAME, FONT_KIND = "DejaVu Sans", "bold"   # the face scripts/nameplate.py uses
DEJAVU_CAP = 0.729     # cap height / CadQuery font size for DejaVu Sans Bold (measured)
TOOLS_MIN_H = 30.0     # hex keys lie flat, the screwdriver's handle is ~20 mm

# Lid: plate on the walls, skirt over the outside of the tray.
LID_CLEAR, LID_WALL, LID_PLATE, LID_SKIRT = 0.4, 1.6, 1.2, 5.0
NAME_CAP, NAME_SINK = 4.0, 0.5   # tray name cut into the front outer face of tray and lid

# ------------------------------------------------------------------ per-piece envelopes (mm)
# Head (diameter, height) by thread size. ISO 4762 / 7380 / 10642 nominal maxima; wafer,
# captive and the M2 pan head are estimates. Envelope = head cylinder + shank cylinder.
HEADS = {
    "SHCS": {2: (3.8, 2.0), 3: (5.5, 3.0), 4: (7.0, 4.0), 5: (8.5, 5.0)},
    "BHCS": {3: (5.7, 1.65), 4: (7.6, 2.2), 5: (9.5, 2.75)},
    "FHCS": {3: (6.72, 1.86), 4: (8.96, 2.48), 5: (11.2, 3.1)},   # length includes the head
    "WAFER": {3: (7.0, 1.5)},
    "CAPTIVE": {3: (5.5, 3.0)},
    "SELF-TAP": {2: (4.0, 1.6), 3: (5.6, 2.1)},
}
NUT = {3: (6.01, 2.4), 4: (7.66, 3.2), 5: (8.79, 4.0)}          # across corners, height
TNUT = {"ROLL-IN": (11.0, 10.0, 6.0), "HAMMER": (11.0, 6.0, 6.5)}  # 2020 box estimates
WASHER = {3: (7.0, 0.5), 4: (9.0, 0.8), 5: (10.0, 1.0)}
LOCK = {3: (6.2, 0.8), 4: (7.6, 1.0), 5: (9.2, 1.2)}
KNURL = {3: (8.0, 4.0), 4: (10.0, 5.0), 5: (12.0, 6.0)}            # estimate


def cyl(d: float, h: float) -> float:
    return math.pi / 4 * d * d * h


@dataclass
class Item:
    bom: str          # exact BOM item text
    qty: int
    group: str        # "screw" | "other"
    order: tuple      # row order within a tray
    line1: str
    line2: str
    piece: float      # envelope volume of one piece, mm3
    min_w: float = MIN_W     # compartment width floor from the part's own length
    alone: bool = False      # gets a full row (Tools)
    note: str = ""

    @property
    def need(self) -> float:
        """Loose volume, mm3."""
        return self.qty * self.piece * PACK


FAMILY = {"SHCS": 0, "BHCS": 1, "FHCS": 2, "WAFER": 3, "CAPTIVE": 4, "SELF-TAP": 5, "SET": 6,
          "NUT": 10, "ROLL-IN": 11, "HAMMER": 12, "INSERT": 13, "WASHER": 14, "SPACER": 15,
          "LOCK": 16, "KNURL": 17, "MAGNET": 18, "TOOLS": 30}


def classify(row: dict) -> Item | None:
    t, q = row["item"], int(row["qty"])
    m = re.fullmatch(r"Machine Screw, (BHCS|SHCS|FHCS|Wafer head|Captive), M(\d+)x(\d+)", t)
    if m:
        head = {"Wafer head": "WAFER", "Captive": "CAPTIVE"}.get(m.group(1), m.group(1))
        d, L = int(m.group(2)), int(m.group(3))
        hd, hh = HEADS[head][d]
        shank = L - hh if head == "FHCS" else L
        total = L if head == "FHCS" else L + hh
        return Item(t, q, "screw", (FAMILY[head], d, L), f"M{d}×{L}", f"{head} {q}",
                    cyl(hd, hh) + cyl(d, shank), min_w=max(MIN_W, total + 6))
    m = re.fullmatch(r"Self-tapping Screw, M(\d+)x(\d+)", t)
    if m:
        d, L = int(m.group(1)), int(m.group(2))
        hd, hh = HEADS["SELF-TAP"][d]
        return Item(t, q, "screw", (FAMILY["SELF-TAP"], d, L), f"M{d}×{L}", f"SELF-TAP {q}",
                    cyl(hd, hh) + cyl(d, L), min_w=max(MIN_W, L + hh + 6))
    m = re.match(r"Set Screw, M(\d+)x(\d+)", t)
    if m:
        d, L = int(m.group(1)), int(m.group(2))
        return Item(t, q, "screw", (FAMILY["SET"], d, L), f"M{d}×{L}", f"SET {q}", cyl(d, L))
    m = re.fullmatch(r"Hexnut, M(\d+)", t)
    if m:
        d = int(m.group(1))
        return Item(t, q, "other", (FAMILY["NUT"], d), f"M{d} NUT", f"HEX {q}", cyl(*NUT[d]))
    m = re.fullmatch(r"T-nut, (Roll-in|Hammer Head), 2020, M(\d+)", t)
    if m:
        kind = "ROLL-IN" if m.group(1) == "Roll-in" else "HAMMER"
        d = int(m.group(2))
        a, b, c = TNUT[kind]
        return Item(t, q, "other", (FAMILY[kind], d), f"M{d} T-NUT", f"{kind} {q}", a * b * c)
    m = re.fullmatch(r"Heatset Insert, Brass, M(\d+)x([\d.]+)x([\d.]+)", t)
    if m:
        d, od, L = int(m.group(1)), float(m.group(2)), float(m.group(3))
        return Item(t, q, "other", (FAMILY["INSERT"], d), f"M{d} INSERT", f"HEAT-SET {q}",
                    cyl(od, L))
    m = re.fullmatch(r"Washer, M(\d+)(?:, ([\d.]+)mm)?", t)
    if m:
        d = int(m.group(1))
        od, th = WASHER[d]
        th = float(m.group(2)) if m.group(2) else th
        l2 = f"{m.group(2)} mm · {q}" if m.group(2) else str(q)
        return Item(t, q, "other", (FAMILY["WASHER"], d), f"M{d} WASHER", l2, cyl(od, th))
    m = re.fullmatch(r"Precision Spacer, M(\d+), ([\d.]+)mm", t)
    if m:
        d, th = int(m.group(1)), float(m.group(2))
        return Item(t, q, "other", (FAMILY["SPACER"], d), f"M{d} SPACER",
                    f"{m.group(2)} mm · {q}", cyl(WASHER[d][0], th))
    m = re.fullmatch(r"Locking Washer, M(\d+)", t)
    if m:
        d = int(m.group(1))
        return Item(t, q, "other", (FAMILY["LOCK"], d), f"M{d} LOCK", f"WASHER {q}",
                    cyl(*LOCK[d]))
    m = re.fullmatch(r"Knurled Nut, M(\d+)", t)
    if m:
        d = int(m.group(1))
        return Item(t, q, "other", (FAMILY["KNURL"], d), f"M{d} KNURLED", f"NUT {q}",
                    cyl(*KNURL[d]))
    m = re.fullmatch(r"(\d+)x(\d+)mm Neodymium Magnet", t)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return Item(t, q, "other", (FAMILY["MAGNET"], a), f"{a}×{b} MAGNET", str(q), cyl(a, b))
    return None


def tools_item(rows: list[dict]) -> Item:
    """One long slot for the kit's hand tools (hex wrenches, the drill bit, the screwdriver)."""
    hexes = sorted(float(re.search(r"([\d.]+)mm", r["item"]).group(1))
                   for r in rows if r["item"].startswith("Hex Wrench"))
    parts = []
    if hexes:
        parts.append("HEX " + " ".join(f"{h:g}" for h in hexes))
    for r in rows:
        m = re.match(r"Drill bit, ([\d.]+)mm", r["item"])
        if m:
            parts.append(f"DRILL {m.group(1)}")
        m = re.match(r"Slot head screwdriver, ([\d.]+)mm", r["item"])
        if m:
            parts.append(f"SLOT {m.group(1)}")
    known = {r["item"] for r in rows if r["item"].startswith(("Hex Wrench", "Drill bit",
                                                               "Slot head screwdriver"))}
    unknown = sorted({r["item"] for r in rows} - known)
    if unknown:
        raise SystemExit(f"tool rows with no label rule: {unknown} - extend tools_item()")
    return Item(" + ".join(r["item"] for r in rows), sum(int(r["qty"]) for r in rows), "other",
                (FAMILY["TOOLS"],), "TOOLS", " · ".join(parts), 0.0, alone=True)


def load_items() -> tuple[list[Item], list[str]]:
    bom = yaml.safe_load(BOM.read_text())
    own = yaml.safe_load(OWNERSHIP.read_text())
    tool_rows = {k for k, v in own.get("unreconciled", {}).items() if str(v).startswith("tool")}
    rows = [r for r in bom["rows"] if r.get("box") == BOX]
    if not rows:
        raise SystemExit(f"{BOM}: no rows in box {BOX!r}")
    items, tools, skipped, unknown = [], [], [], []
    for r in rows:
        if r["item"].startswith(EXCLUDE):
            skipped.append(r["item"])
        elif r["item"] in tool_rows:
            tools.append(r)
        else:
            it = classify(r)
            (items.append(it) if it else unknown.append(r["item"]))
    if unknown:
        raise SystemExit("BOM rows in the fastener box with no tray rule (classify()): "
                         + "; ".join(unknown))
    if tools:
        items.append(tools_item(tools))
    return items, skipped


# ------------------------------------------------------------------ text metrics
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

    @property
    def w(self) -> float:
        return self.x1 - self.x0

    @property
    def h(self) -> float:
        return self.y1 - self.y0

    @property
    def scoop(self) -> float:
        return scoop_r(self.h)

    @property
    def capacity(self) -> float:
        """Open volume, mm3: the box less the cove (r^2 (1 - pi/4) x width); corners ignored."""
        r = self.scoop
        return self.w * self.h * DEPTH - r * r * (1 - math.pi / 4) * self.w


@dataclass
class Tray:
    letter: str
    title: str
    items: list[Item]
    W: float = 0.0
    D: float = 0.0
    rows: list[list[Cell]] = field(default_factory=list)
    ledges: list[tuple[float, float]] = field(default_factory=list)   # (y0, y1) per row


def inner_w() -> float:
    return TRAY_W_MAX - 2 * WALL_OUT


def min_w(it: Item) -> float:
    return max(it.min_w, label_w(it) + LABEL_PAD)


def scoop_r(h: float) -> float:
    return min(SCOOP_R, 0.4 * h, DEPTH - 4)


def row_widths(items: list[Item], h: float) -> list[float]:
    """Width that holds `need` at row height h: the open section is the box less the cove."""
    r = scoop_r(h)
    section = DEPTH * h - r * r * (1 - math.pi / 4)
    return [min_w(it) if it.alone else max(min_w(it), it.need / section) for it in items]


def row_min_h(items: list[Item]) -> float | None:
    """Smallest cavity height (Y) at which the row's compartments fit the inner width."""
    W = inner_w()
    if any(it.alone for it in items) and len(items) > 1:
        return None
    lo = max([MIN_H] + [TOOLS_MIN_H for it in items if it.alone])
    gaps = DIVIDER * (len(items) - 1)
    if sum(min_w(it) for it in items) + gaps > W:
        return None
    if sum(row_widths(items, lo)) + gaps <= W:
        return lo
    hi = 2000.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if sum(row_widths(items, mid)) + gaps <= W:
            hi = mid
        else:
            lo = mid
    return hi


def plan_rows(items: list[Item]) -> tuple[list[list[Item]], list[float]]:
    """Partition the ordered items into rows minimising the tray depth (DP over break points)."""
    n = len(items)
    best: list[tuple[float, int, float]] = [(0.0, -1, 0.0)] + [(math.inf, -1, 0.0)] * n
    for j in range(1, n + 1):
        for i in range(j):
            if best[i][0] == math.inf:
                continue
            h = row_min_h(items[i:j])
            if h is None:
                continue
            cost = best[i][0] + h + LEDGE
            if cost < best[j][0] - 1e-9:
                best[j] = (cost, i, h)
    if best[n][0] == math.inf:
        raise SystemExit("no row partition fits the tray width")
    rows, hs, j = [], [], n
    while j > 0:
        _c, i, h = best[j]
        rows.append(items[i:j])
        hs.append(h)
        j = i
    return rows[::-1], hs[::-1]


def needed_depth(hs: list[float]) -> float:
    return WALL_OUT + sum(h + LEDGE for h in hs) + WALL_OUT   # last ledge + the back rim


def layout(tray: Tray, D: float) -> None:
    rows, hs = plan_rows(tray.items)
    slack = D - needed_depth(hs)
    if slack < -1e-6:
        raise SystemExit(f"tray {tray.letter}: needs {needed_depth(hs):.1f} mm of depth, "
                         f"{D:.1f} available")
    total = sum(hs)
    hs = [h + slack * h / total for h in hs]
    tray.W, tray.D = TRAY_W_MAX, D
    W = inner_w()
    y = WALL_OUT
    tray.rows, tray.ledges = [], []
    for items, h in zip(rows, hs):
        ws = row_widths(items, h)
        free = W - sum(ws) - DIVIDER * (len(items) - 1)
        ws = [w + free * w / sum(ws) for w in ws]
        x = WALL_OUT
        cells = []
        for it, w in zip(items, ws):
            cells.append(Cell(it, x, x + w, y, y + h))
            x += w + DIVIDER
        tray.rows.append(cells)
        tray.ledges.append((y + h, y + h + LEDGE))
        y += h + LEDGE


# ------------------------------------------------------------------ solids
def rrect(cq, w: float, d: float, r: float, x: float, y: float, z0: float, h: float):
    """Rounded-rectangle prism, corner (x, y), from z0 up h."""
    return (cq.Workplane("XY").workplane(offset=z0).center(x + w / 2, y + d / 2)
            .rect(w, d).extrude(h).edges("|Z").fillet(r))


def build_tray(tray: Tray):
    """The tray as one solid. Booleans are batched (one cut, one fuse): OCCT's multi-argument
    operations are many times faster than a union per glyph."""
    import cadquery as cq
    W, D = tray.W, tray.D
    body = (cq.Workplane("XY").box(W, D, H, centered=False)
            .edges("|Z").fillet(R_OUT)
            .faces("<Z").edges().chamfer(CHAMFER)).val()
    cavities, adds = [], []
    for row in tray.rows:
        for c in row:
            cav = rrect(cq, c.w, c.h, R_CAV, c.x0, c.y0, FLOOR, DEPTH + 1)
            cavities.append(cav.val())
            r = c.scoop
            wedge = (cq.Workplane("XY").box(c.w, r, r, centered=False)
                     .translate((c.x0, c.y0, FLOOR)))
            roll = (cq.Workplane("YZ").workplane(offset=c.x0 - 1)
                    .center(c.y0 + r, FLOOR + r).circle(r).extrude(c.w + 2))
            adds.append(wedge.cut(roll).intersect(cav).val())      # the scoop cove
    body = body.cut(*cavities)

    # The raised top: outer rim, the dividers inside each row, and the labels. One plane at
    # H + EMBOSS, so the lid sits flat on it and a colour change at Z = H + 0.2 takes all three.
    rim = (cq.Workplane("XY").workplane(offset=H)
           .center(W / 2, D / 2).rect(W, D).extrude(EMBOSS).edges("|Z").fillet(R_OUT)
           .cut(rrect(cq, W - 2 * WALL_OUT, D - 2 * WALL_OUT, R_CAV, WALL_OUT, WALL_OUT,
                      H - 0.1, EMBOSS + 0.2)))
    adds.append(rim.val())
    for row in tray.rows:
        for a, b in zip(row, row[1:]):
            adds.append(cq.Workplane("XY").box(b.x0 - a.x1, a.h, EMBOSS, centered=False)
                        .translate((a.x1, a.y0, H)).val())
    for row, (ly0, ly1) in zip(tray.rows, tray.ledges):
        for c in row:
            cx = (c.x0 + c.x1) / 2
            y1 = ly1 - 1.2 - CAP1 / 2
            y2 = ly0 + 1.2 + CAP2 / 2
            for txt, cap, yy in ((c.item.line1, CAP1, y1), (c.item.line2, CAP2, y2)):
                # 0.2 mm sunk into the ledge so the glyphs fuse to it
                adds.extend(text_solid(txt, cap, EMBOSS + 0.2)
                            .translate((cx, yy, H - 0.2)).vals())
    name = front_text(f"TRAY {tray.letter} · {tray.title}", NAME_CAP, W / 2, H / 2)
    return body.fuse(*adds).cut(*name.vals()).clean()


def build_lid(tray: Tray):
    """Drawn in use (plate on top, skirt down over the tray), then turned over about Y for
    printing: plate face on the bed, skirt standing up, no supports. Its name is cut into the
    front outer face, so it reads upright once the lid is on."""
    import cadquery as cq
    ow, od = tray.W + 2 * (LID_CLEAR + LID_WALL), tray.D + 2 * (LID_CLEAR + LID_WALL)
    hh = LID_SKIRT + LID_PLATE
    lid = (cq.Workplane("XY").box(ow, od, hh, centered=False).edges("|Z")
           .fillet(R_OUT + LID_CLEAR + LID_WALL))
    lid = lid.cut(rrect(cq, tray.W + 2 * LID_CLEAR, tray.D + 2 * LID_CLEAR, R_OUT + LID_CLEAR,
                        LID_WALL, LID_WALL, -1, LID_SKIRT + 1))
    lid = lid.cut(front_text(f"TRAY {tray.letter} · {tray.title}", NAME_CAP, ow / 2, hh / 2))
    lid = (lid.rotate((0, 0, 0), (0, 1, 0), 180).translate((ow, 0, hh))
           .faces("<Z").edges().chamfer(CHAMFER))
    return lid


def export_stl(shape, path: Path, tol: float = 0.05, ang: float = 0.3) -> None:
    """Binary STL from one OCCT tessellation of the whole solid (0.05 mm chord error, finer
    than the nozzle). A third of the size of CadQuery's exporter at the same tolerance, and
    deterministic. Refuses a mesh that is not closed or is inside out."""
    import struct
    import numpy as np
    shape = shape.val() if hasattr(shape, "val") else shape
    verts, tris = shape.tessellate(tol, ang)
    V = np.array([v.toTuple() for v in verts], dtype=np.float64)
    T = np.array(tris, dtype=np.int64)
    key = np.round(V, 5)
    _u, inv = np.unique(key, axis=0, return_inverse=True)
    edges = np.sort(np.stack([inv.ravel()[T][:, [0, 1, 2]], inv.ravel()[T][:, [1, 2, 0]]], -1)
                    .reshape(-1, 2), axis=1)
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
    overrides = [
        ("start_gcode", cold_start_gcode()),
        ("start_filament_gcode", _append_gcode(fil["start_filament_gcode"], FLAPS_ON)),
        ("end_filament_gcode", _append_gcode(fil["end_filament_gcode"], FLAPS_OFF)),
        ("support_material", "0"),
        ("support_material_auto", "0"),
    ]
    cfg.update(overrides)
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


def make_project(stl: Path, ini: Path, name: str, tmp: Path) -> tuple[Path, str]:
    from build_plates import PRUSA, inject_3mf, run
    cx, cy, _bw, _bd = bed_centre(ini)
    dst = HERE / f"{name}.3mf"
    p = run([PRUSA, "--load", str(ini), "--dont-arrange", "--center", f"{cx:g},{cy:g}",
             "--export-3mf", "-o", str(dst), str(stl)])
    inject_3mf(dst, ini, {}, {stl.name: name})
    return dst, (p.stdout + p.stderr).strip()


def slice_project(project: Path, tmp: Path) -> dict:
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
    xs, ys = [], []
    for m in re.finditer(r"^G1 (?:[^;\n]*?)X([-\d.]+) Y([-\d.]+)[^;\n]*E[\d.]", text, re.M):
        xs.append(float(m.group(1)))
        ys.append(float(m.group(2)))
    zs = [float(z) for z in re.findall(r"^;Z:([\d.]+)", text, re.M)]
    if project.stem.startswith("tray"):
        layers = {round(z, 2) for z in zs}
        want = {round(H, 2), round(H + 0.2, 2), round(H + EMBOSS, 2)}
        if not want <= layers:
            raise SystemExit(f"{project.name}: layers {sorted(want - layers)} missing - the "
                             "colour-change Z in README.md would be wrong")
    return dict(hours=hours, grams=grams, raw=raw, log=(p.stdout + p.stderr).strip(),
                xmin=min(xs), xmax=max(xs), ymin=min(ys), ymax=max(ys), zmax=max(zs),
                perimeters=cfg.get("perimeters"), fill=cfg.get("fill_density"),
                support=cfg.get("support_material"))


# ------------------------------------------------------------------ render
def render(stl: Path, out: Path, azim: float, elev: float, px: int = 2000) -> None:
    """Orthographic z-buffer render (scripts/cad_render/render.py) of one tray. Everything above
    the wall tops (labels, rim, divider tops: the colour-change layers) is drawn in the accent
    blue; edges are drawn only where the surface turns (> ~20 deg), steps to another plane, or
    changes colour, not
    along every mesh triangle, so the glyphs stay legible."""
    import numpy as np
    from PIL import Image
    from render import basis, compose, project, shade
    from geom import read_stl
    tris = np.array(read_stl(stl), dtype=np.float64)          # (n, 3, 3)
    V = tris.reshape(-1, 3)
    T = np.arange(len(V)).reshape(-1, 3)
    zc = tris[:, :, 2].mean(1)
    top = zc > H + 0.01
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
    off = (n * tris[:, 0]).sum(1)              # plane offset: same plane, same value
    ob = np.zeros(tid.shape)
    ob[mask] = off[tid[mask]]
    edge = np.zeros(tid.shape, bool)
    for ax in (0, 1):
        dn = (nb * np.roll(nb, 1, ax)).sum(-1) < 0.94
        dc = cb != np.roll(cb, 1, ax)
        do = np.abs(ob - np.roll(ob, 1, ax)) > 0.3
        edge |= dn | dc | do
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


def layout_md(trays: list[Tray], skipped: list[str], alt: str) -> str:
    out = [f"Generated from `scripts/data/ldo-350-bom.yml` (box *{BOX}*, fetched "
           f"{yaml.safe_load(BOM.read_text()).get('fetched')}). Size = compartment floor "
           f"width × length in mm, {DEPTH:g} mm deep. *Need* = count × one piece's envelope "
           f"× {PACK:g}; *room* = the compartment's open volume (cove deducted).", ""]
    for t in trays:
        n = sum(len(r) for r in t.rows)
        out += [f"**Tray {t.letter} — {t.title}:** {t.W:g} × {t.D:g} × {H + EMBOSS:g} mm, "
                f"{n} compartments in {len(t.rows)} rows (row 1 is the front).", "",
                "| row | label | BOM item | count | size mm | need cm³ | room cm³ |",
                "|---:|---|---|---:|---|---:|---:|"]
        for ri, row in enumerate(t.rows, 1):
            for c in row:
                it = c.item
                need = "—" if it.alone else f"{it.need / 1000:.1f}"
                out.append(f"| {ri} | {it.line1} · {it.line2} | {it.bom} | {it.qty} | "
                           f"{c.w:.0f} × {c.h:.0f} | {need} | {c.capacity / 1000:.0f} |")
        out.append("")
    out += ["Not in a compartment: " + "; ".join(skipped) + ".", "", alt]
    return "\n".join(out)


def slice_md(results: list[tuple[str, dict]]) -> str:
    out = ["| file | time | g PLA | extents on the bed, mm | perimeters / infill | supports |",
           "|---|---|---:|---|---|---|"]
    th, tg = 0.0, 0.0
    for name, r in results:
        th += r["hours"]
        tg += r["grams"]
        out.append(f"| `{name}.3mf` | {r['raw']} | {r['grams']:.0f} | "
                   f"X {r['xmin']:.1f}–{r['xmax']:.1f}, Y {r['ymin']:.1f}–{r['ymax']:.1f}, "
                   f"Z ≤ {r['zmax']:.2f} | {r['perimeters']} / {r['fill']} | "
                   f"{'none' if r['support'] == '0' else r['support']} |")
    trays_h = sum(r["hours"] for n, r in results if n.startswith("tray"))
    trays_g = sum(r["grams"] for n, r in results if n.startswith("tray"))
    out += ["", f"Trays alone: **{trays_h:.1f} h, {trays_g:.0f} g**. Trays and lids: "
            f"**{th:.1f} h, {tg:.0f} g**. PrusaSlicer 2.9.6 CLI estimates, one part per bed, "
            f"not GUI-arranged. Every tray slices with layer tops at {H:.1f}, {H + 0.2:.1f} and "
            f"{H + EMBOSS:.1f} mm (checked by the script)."]
    return "\n".join(out)


# ------------------------------------------------------------------ driver
# Tray groups, in order. A screw goes by thread size; everything else by family.
GROUPS = (
    ("A", "M2 · M3 SCREWS", lambda i: i.group == "screw" and i.order[1] <= 3),
    ("B", "M4 · M5 SCREWS · NUTS · INSERTS",
     lambda i: (i.group == "screw" and i.order[1] > 3)
     or (i.group == "other" and i.order[0] not in (FAMILY["ROLL-IN"], FAMILY["HAMMER"])
         and not i.alone)),
    ("C", "T-NUTS · TOOLS",
     lambda i: i.order[0] in (FAMILY["ROLL-IN"], FAMILY["HAMMER"]) or i.alone),
)


def make_trays(items: list[Item]) -> list[Tray]:
    trays = [Tray(letter, title, sorted((i for i in items if pred(i)), key=lambda i: i.order))
             for letter, title, pred in GROUPS]
    placed = [i.bom for t in trays for i in t.items]
    if sorted(placed) != sorted(i.bom for i in items):
        raise SystemExit("GROUPS must place every item exactly once")
    return trays


def depth_needed(trays: list[Tray]) -> list[float]:
    return [needed_depth(plan_rows(t.items)[1]) for t in trays]


def best_two_tray_depth(items: list[Item]) -> tuple[float, str]:
    """The deepest tray of the best two-tray split of the whole ordered list (cut anywhere a
    family or thread size changes): the number that decides whether two trays can do."""
    seq = sorted(items, key=lambda i: i.order)
    best = (math.inf, "")
    for k in range(1, len(seq)):
        if seq[k].order[:2] == seq[k - 1].order[:2]:
            continue
        d = max(needed_depth(plan_rows(seq[:k])[1]), needed_depth(plan_rows(seq[k:])[1]))
        if d < best[0]:
            best = (d, f"{seq[k - 1].line1} {seq[k - 1].line2} | {seq[k].line1} {seq[k].line2}")
    return best


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--plan", action="store_true", help="print the layout, write nothing")
    ap.add_argument("--no-slice", action="store_true", help="skip PrusaSlicer")
    ap.add_argument("--copy-renders", type=Path, help="also copy the PNGs here")
    args = ap.parse_args()

    items, skipped = load_items()
    two, cut = best_two_tray_depth(items)
    trays = make_trays(items)
    need = depth_needed(trays)
    alt = (f"Why three trays: the best two-tray split of the whole list (cut at {cut}) still "
           f"needs a {two:.0f} mm deep tray against the {TRAY_D_MAX:g} mm that leaves room for "
           f"a lid on the bed. Three trays need "
           + " / ".join(f"{d:.0f}" for d in need) + " mm; all are made "
           "the same size, the deepest, so they stack and any lid fits any tray.")
    print(alt)
    if max(need) > TRAY_D_MAX:
        raise SystemExit(f"a tray needs {max(need):.1f} mm > {TRAY_D_MAX} - re-balance GROUPS "
                         "or add a tray")
    D = min(TRAY_D_MAX, math.ceil(max(need) / 2) * 2)
    for t in trays:
        layout(t, D)
        print(f"\nTray {t.letter} ({t.title}) {t.W:g} x {t.D:g} mm")
        for ri, row in enumerate(t.rows, 1):
            for c in row:
                print(f"  r{ri} {c.item.line1:>12} {c.item.line2:<34} {c.w:6.1f} x {c.h:5.1f}"
                      f"  need {c.item.need / 1000:6.1f}  room {c.capacity / 1000:6.1f} cm3")
    if args.plan:
        return 0

    RENDERS.mkdir(exist_ok=True)
    stls = {}
    for t in trays:
        for kind, build in (("tray", build_tray), ("lid", build_lid)):
            name = f"{kind}-{t.letter}"
            path = HERE / f"{name}.stl"
            export_stl(build(t), path)
            stls[name] = path
            print(f"wrote {path.relative_to(REPO)}")
        for view, az, el in (("top", -90.0, 90.0), ("34", -60.0, 38.0)):
            out = RENDERS / f"tray-{t.letter}-{view}.png"
            render(stls[f"tray-{t.letter}"], out, az, el)
            print(f"wrote {out.relative_to(REPO)}")
            if args.copy_renders:
                args.copy_renders.mkdir(parents=True, exist_ok=True)
                shutil.copy2(out, args.copy_renders / out.name)
    put_block("layout", layout_md(trays, skipped, alt))

    if args.no_slice:
        return 0
    tmp = Path(tempfile.mkdtemp(prefix="trays-"))
    try:
        ini = tmp / "bench-trays-pla.ini"
        write_ini(ini)
        _cx, _cy, bw, bd = bed_centre(ini)
        results = []
        for name in [f"{k}-{t.letter}" for t in trays for k in ("tray", "lid")]:
            proj, log = make_project(stls[name], ini, name, tmp)
            r = slice_project(proj, tmp)
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
