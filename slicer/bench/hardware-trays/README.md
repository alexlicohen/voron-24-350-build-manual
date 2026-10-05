# Hardware trays (bench print)

Three flat PLA trays with drop-on lids that hold the LDO Voron 2.4 350 kit's *Fasteners, Tools & Misc*
box: one compartment per hardware row of the kit BOM, two raised label lines (size; type and kit count) on
a ledge behind each compartment, a scoop cove along each compartment's front wall, rounded outer corners and
a chamfered first-layer edge. The bags are emptied into them on kit day,
[Ch 00 Step 00.12](../../../docs/manual/00-before-you-start.md#step-0012-empty-the-fastener-bags-into-the-hardware-trays).
A bench print: on no plate, in no batch, run total or spool ledger
([print/README § Bench prints](../../../docs/manual/print/README.md#bench-prints-outside-the-plates)).

| Tray | Holds |
|---|---|
| A | M2 and M3 screws: SHCS by length, BHCS, FHCS, wafer, captive, M2 self-tappers, M3 set screws |
| B | M4 and M5 screws, M4 set screws, hex nuts, heat-set inserts, washers, spacers, lock washers, knurled nuts, magnets |
| C | roll-in and hammer-head T-nuts, and one full-width Tools slot (hex keys 1.5–4, the 2 mm drill bit, the slot screwdriver) |

Renders (blue = the three layers above the wall tops, i.e. the colour-change layers):
`renders/tray-{A,B,C}-top.png` and `renders/tray-{A,B,C}-34.png`.

## Files

| File | What |
|---|---|
| `gen_trays.py` | the only generator (CadQuery, `venv-cq`) |
| `tray-{A,B,C}.stl`, `lid-{A,B,C}.stl` | print-ready meshes, as oriented (lids plate-down) |
| `tray-{A,B,C}.3mf`, `lid-{A,B,C}.3mf` | PrusaSlicer 2.9.6 projects, one part per bed, config embedded |
| `renders/*.png` | top and 3/4 views of each tray |

## Regenerate

```sh
venv-cq/bin/python slicer/bench/hardware-trays/gen_trays.py           # STLs, renders, 3MFs, slice, README blocks
venv-cq/bin/python slicer/bench/hardware-trays/gen_trays.py --plan    # layout report only, writes nothing
venv-cq/bin/python slicer/bench/hardware-trays/gen_trays.py --no-slice
```

Everything is read from the data: the rows of box *Fasteners, Tools & Misc* in `scripts/data/ldo-350-bom.yml`
(re-pinned to the batch sheet on kit day, Step 00.2) and the `tool` roles in
`scripts/data/hardware-ownership.yml`. Re-run after a re-pin; the compartment sizes and labels follow the
counts. A row the script has no rule for stops it (`classify()`), so a new hardware line cannot drop out
silently; a tray that no longer fits the bed stops it too (re-balance `GROUPS`). The STLs and renders are
byte-identical between runs. About 3 minutes, most of it the label booleans and the six slices.

Not in a compartment: the PTFE tube, the zip ties, the two aluminium handles and the brass insert tip.
The Motion box's loose parts (F695 and 625 bearings, pulleys, GT2 idlers, 5×60 shafts, the nozzle-probe
shaft, MR85s, the IDGA gear set, the Bowden coupler) stay sealed in their own kit bags. Space is not the
reason (tray A has depth to spare); they are sealed precision parts that only pick up grit in an open tray,
each bag already holds one part type with its name on it, and they are opened at a few known drive and
toolhead steps, not drawn on every session like the screws.

## Sizing rules

- Compartment volume = count × one piece's envelope (head cylinder + shank cylinder for screws, ISO head
  sizes; across-corners cylinder for nuts; a box for T-nuts) × 2.5 for loose packing, at 20 mm depth, cove
  deducted. Floor 25 mm wide × 18 mm long so a finger fits; wider where the label or the screw (length + head
  + 6 mm, lying along X) needs it.
- Rows keep BOM family order (SHCS by length, BHCS, FHCS, …; nuts, T-nuts, inserts, …); a dynamic programme
  picks the row breaks that make each tray shallowest, then the spare depth and width are shared out in
  proportion. The tray depth is the deepest of the three, so all three are the same size and stack, and any
  lid fits any tray.
- Walls: outer 2.4 mm, dividers 1.8 mm, floor 1.6 mm; outer corners R6, cavity corners R3.6 (keeps the
  corner wall 2.4 thick); 0.6 mm chamfer on the first-layer edge; scoop cove R10 (0.4 × the compartment length on
  short rows) on each compartment's front wall, so a finger drags parts up and out towards you.
- Labels: DejaVu Sans Bold (the face `scripts/nameplate.py` uses), line 1 cap height 5.0 mm, line 2 4.0 mm,
  raised 0.6 mm on a 13.2 mm ledge behind the compartment, at the top of the tray so they read when it is
  full. The outer rim and the dividers are raised by the same 0.6 mm, so a lid (or a tray stacked on top)
  sits flat on them and closes every compartment. The tray name is cut 0.5 mm into the front face.
- Lid: 1.2 mm plate, 5 mm skirt over the tray's outside, 0.4 mm clearance per side; 240 × 180 mm.

## Print

Core One+, textured sheet, any PLA, door open. Each project carries its config, flattened from the
PrusaSlicer 2.9.6 system presets `0.20mm BALANCED @COREONE HF0.4` + `Prusament PLA @COREONE HF0.4` +
`Prusa CORE One HF0.4 nozzle` (`slicer/resolve_preset.py`), with this repo's printer-wide lines:
the vendored cold start (`slicer/coreone-cold-start.gcode`) and `M106 P3 S160` / `M106 P3 R` in the filament
start/end G-code (AFS bypass flaps, as `slicer/bay-ducts-petg.ini` does for PETG). Supports off. Nothing else
is overridden (2 perimeters, 15 % infill, 0.2 mm layers).

**Two-colour labels (optional):** the wall tops end at Z 21.6; the labels, rim and divider tops are the three
layers from 21.8 to 22.2. In PrusaSlicer's layer slider, add a colour change (M600) at **21.80 mm**, then load
the label colour when the printer asks. Lids are one colour.

**Lids: yes.** They add about 4.9 h and 216 g to the 15.3 h and 607 g of the trays. The trays sit on the bench
for the whole build with a helper at it; one knock that tips 283 M3×8 into the M3×12 compartment is exactly
the mix Step 00.12 exists to prevent, and the lids keep dust out between sessions. If plastic is short, print
one lid for the top of a stack: each tray's flat bottom closes the tray below it, though nothing keeps a stack
from sliding.

<!-- BEGIN generated:layout -->
Generated from `scripts/data/ldo-350-bom.yml` (box *Fasteners, Tools & Misc*, fetched 2026-09-24). Size = compartment floor width × length in mm, 20 mm deep. *Need* = count × one piece's envelope × 2.5; *room* = the compartment's open volume (cove deducted).

**Tray A — M2 · M3 SCREWS:** 236 × 176 × 22.2 mm, 17 compartments in 4 rows (row 1 is the front).

| row | label | BOM item | count | size mm | need cm³ | room cm³ |
|---:|---|---|---:|---|---:|---:|
| 1 | M3×8 · SHCS 283 | Machine Screw, SHCS, M3x8 | 283 | 151 × 41 | 90.4 | 120 |
| 1 | M3×12 · SHCS 50 | Machine Screw, SHCS, M3x12 | 50 | 38 × 41 | 19.5 | 30 |
| 1 | M3×16 · SHCS 30 | Machine Screw, SHCS, M3x16 | 30 | 38 × 41 | 13.8 | 31 |
| 2 | M3×20 · SHCS 40 | Machine Screw, SHCS, M3x20 | 40 | 52 × 26 | 21.3 | 26 |
| 2 | M3×25 · SHCS 12 | Machine Screw, SHCS, M3x25 | 12 | 42 × 26 | 7.4 | 21 |
| 2 | M3×30 · SHCS 44 | Machine Screw, SHCS, M3x30 | 44 | 77 × 26 | 31.2 | 39 |
| 2 | M3×35 · SHCS 6 | Machine Screw, SHCS, M3x35 | 6 | 54 × 26 | 4.8 | 27 |
| 3 | M3×40 · SHCS 34 | Machine Screw, SHCS, M3x40 | 34 | 76 × 26 | 30.1 | 37 |
| 3 | M3×50 · SHCS 4 | Machine Screw, SHCS, M3x50 | 4 | 73 × 26 | 4.2 | 36 |
| 3 | M3×6 · BHCS 14 | Machine Screw, BHCS, M3x6 | 14 | 36 × 26 | 3.0 | 18 |
| 3 | M3×25 · BHCS 6 | Machine Screw, BHCS, M3x25 | 6 | 41 × 26 | 3.3 | 20 |
| 4 | M3×6 · FHCS 42 | Machine Screw, FHCS, M3x6 | 42 | 33 × 26 | 10.0 | 16 |
| 4 | M3×10 · FHCS 8 | Machine Screw, FHCS, M3x10 | 8 | 34 × 26 | 2.5 | 17 |
| 4 | M3×25 · WAFER 3 | Machine Screw, Wafer head, M3x25 | 3 | 38 × 26 | 1.8 | 19 |
| 4 | M3×6 · CAPTIVE 2 | Machine Screw, Captive, M3x6 | 2 | 40 × 26 | 0.6 | 20 |
| 4 | M2×10 · SELF-TAP 43 | Self-tapping Screw, M2x10 | 43 | 47 × 26 | 5.5 | 23 |
| 4 | M3×2 · SET 5 | Set Screw, M3x2, Pre-applied Threadlocker | 5 | 30 × 26 | 0.2 | 15 |

**Tray B — M4 · M5 SCREWS · NUTS · INSERTS:** 236 × 176 × 22.2 mm, 17 compartments in 4 rows (row 1 is the front).

| row | label | BOM item | count | size mm | need cm³ | room cm³ |
|---:|---|---|---:|---|---:|---:|
| 1 | M5×40 · SHCS 26 | Machine Screw, SHCS, M5x40 | 26 | 99 × 38 | 69.5 | 72 |
| 1 | M4×6 · BHCS 8 | Machine Screw, BHCS, M4x6 | 8 | 26 × 38 | 3.5 | 19 |
| 1 | M5×6 · BHCS 1 | Machine Screw, BHCS, M5x6 | 1 | 26 × 38 | 0.8 | 19 |
| 1 | M5×10 · BHCS 54 | Machine Screw, BHCS, M5x10 | 54 | 75 × 38 | 52.8 | 55 |
| 2 | M5×14 · BHCS 4 | Machine Screw, BHCS, M5x14 | 4 | 30 × 33 | 4.7 | 19 |
| 2 | M5×16 · BHCS 43 | Machine Screw, BHCS, M5x16 | 43 | 88 × 33 | 54.7 | 57 |
| 2 | M5×30 · BHCS 26 | Machine Screw, BHCS, M5x30 | 26 | 82 × 33 | 51.0 | 53 |
| 2 | M4×4 · SET 32 | Set Screw, M4x4, Pre-applied Threadlocker | 32 | 26 × 33 | 4.0 | 17 |
| 3 | M3 NUT · HEX 14 | Hexnut, M3 | 14 | 33 × 28 | 2.4 | 18 |
| 3 | M5 NUT · HEX 30 | Hexnut, M5 | 30 | 34 × 28 | 18.2 | 19 |
| 3 | M3 INSERT · HEAT-SET 153 | Heatset Insert, Brass, M3x5x4 | 153 | 56 × 28 | 30.0 | 31 |
| 3 | M3 WASHER · 6 | Washer, M3 | 6 | 50 × 28 | 0.3 | 28 |
| 3 | M5 WASHER · 1 mm · 9 | Washer, M5, 1mm | 9 | 50 × 28 | 1.8 | 28 |
| 4 | M5 SPACER · 1 mm · 46 | Precision Spacer, M5, 1mm | 46 | 55 × 19 | 9.0 | 20 |
| 4 | M5 LOCK · WASHER 2 | Locking Washer, M5 | 2 | 44 × 19 | 0.4 | 16 |
| 4 | M4 KNURLED · NUT 4 | Knurled Nut, M4 | 4 | 63 × 19 | 3.9 | 23 |
| 4 | 6×3 MAGNET · 16 | 6x3mm Neodymium Magnet | 16 | 64 × 19 | 3.4 | 23 |

**Tray C — T-NUTS · TOOLS:** 236 × 176 × 22.2 mm, 5 compartments in 3 rows (row 1 is the front).

| row | label | BOM item | count | size mm | need cm³ | room cm³ |
|---:|---|---|---:|---|---:|---:|
| 1 | M3 T-NUT · ROLL-IN 135 | T-nut, Roll-in, 2020, M3 | 135 | 144 × 79 | 222.8 | 225 |
| 1 | M5 T-NUT · ROLL-IN 80 | T-nut, Roll-in, 2020, M5 | 80 | 85 × 79 | 132.0 | 133 |
| 2 | M3 T-NUT · HAMMER 75 | T-nut, Hammer Head, 2020, M3 | 75 | 189 × 22 | 80.4 | 81 |
| 2 | M5 T-NUT · HAMMER 16 | T-nut, Hammer Head, 2020, M5 | 16 | 40 × 22 | 17.2 | 17 |
| 3 | TOOLS · HEX 1.5 2 2.5 3 4 · DRILL 2 · SLOT 2.5 | Drill bit, 2mm + Hex Wrench, 1.5mm + Hex Wrench, 2mm + Hex Wrench, 2.5mm + Hex Wrench, 3mm + Hex Wrench, 4mm + Slot head screwdriver, 2.5mm | 7 | 231 × 30 | — | 135 |

Not in a compartment: Teflon Tube (4mm OD 3mm ID) - 1.2m; Zip Ties, 3x150mm; Brass Heatset Insert tool (for M3 Brass Inserts); Aluminium Handle.

Why three trays: the best two-tray split of the whole list (cut at M3 NUT HEX 14 | M5 NUT HEX 30) still needs a 241 mm deep tray against the 206 mm that leaves room for a lid on the bed. Three trays need 141 / 170 / 175 mm; all are made the same size, the deepest, so they stack and any lid fits any tray.
<!-- END generated:layout -->

<!-- BEGIN generated:slice -->
| file | time | g PLA | extents on the bed, mm | perimeters / infill | supports |
|---|---|---:|---|---|---|
| `tray-A.3mf` | 5h 26m 32s | 212 | X 7.2–242.8, Y 22.2–197.8, Z ≤ 22.20 | 2 / 15% | none |
| `lid-A.3mf` | 1h 38m 22s | 72 | X 5.2–244.8, Y 20.2–199.8, Z ≤ 6.20 | 2 / 15% | none |
| `tray-B.3mf` | 5h 30m 40s | 213 | X 7.2–242.8, Y 22.2–197.8, Z ≤ 22.20 | 2 / 15% | none |
| `lid-B.3mf` | 1h 39m 54s | 72 | X 5.2–244.8, Y 20.2–199.8, Z ≤ 6.20 | 2 / 15% | none |
| `tray-C.3mf` | 4h 22m 19s | 181 | X 7.2–242.8, Y 22.2–197.8, Z ≤ 22.20 | 2 / 15% | none |
| `lid-C.3mf` | 1h 38m 18s | 72 | X 5.2–244.8, Y 20.2–199.8, Z ≤ 6.20 | 2 / 15% | none |

Trays alone: **15.3 h, 607 g**. Trays and lids: **20.3 h, 823 g**. PrusaSlicer 2.9.6 CLI estimates, one part per bed, not GUI-arranged. Every tray slices with layer tops at 21.6, 21.8 and 22.2 mm (checked by the script).
<!-- END generated:slice -->

## Credit and licence

Inspired by **r0bdawg11**, *INDX Upgrade Hardware Organizer*, <https://www.printables.com/model/1794124>
(CC BY): one flat tray, a compartment per hardware type, raised labels on the rim, a scoop fillet, rounded
corners. Inspiration only: this design is drawn from scratch by `gen_trays.py`, and no geometry is copied.

Licence: the same as the rest of this repository's own content. None has been chosen yet (root README ›
Attribution and licences), so treat it as all rights reserved until one is added.
