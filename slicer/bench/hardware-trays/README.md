# Hardware trays (bench print)

Three Gridfinity bins, each sized to its contents (sizes in the generated block below), that hold the LDO Voron 2.4 350 kit's fastener bags: one
compartment per hardware row of the kit BOM, two raised label lines (size; type and kit count) on a ledge
behind each row, and a scoop cove along each compartment's front wall. They sit on any Gridfinity baseplate
(Clickfinity included) and stack on each other. The bags are emptied into them on kit day,
[Ch 00 Step 00.12](../../../docs/manual/00-before-you-start.md#step-0012-empty-the-fastener-bags-into-the-hardware-trays).
A bench print: on no plate, in no batch, run total or spool ledger
([print/README § Bench prints](../../../docs/manual/print/README.md#bench-prints-outside-the-plates)).

| Tray | Holds |
|---|---|
| A | M2 and M3 screws: SHCS by length, BHCS, FHCS, wafer, captive, M2 self-tappers, M3 set screws |
| B | M4 and M5 screws: M5 SHCS, M4 and M5 BHCS, M4 set screws |
| C | hex nuts, heat-set inserts, washers, spacers, lock washers, knurled nuts, magnets, roll-in and hammer-head T-nuts |

The kit's hand tools (hex keys, the 2 mm drill bit, the slot screwdriver, the brass insert tip) are not
stored in the trays. Renders (blue = the layers above the label ledges, i.e. the colour-change layers):
`renders/tray-{A,B,C}-top.png` and `renders/tray-{A,B,C}-34.png`.

## Files

| File | What |
|---|---|
| `gen_trays.py` | the only generator (CadQuery, `venv-cq`; no other dependency) |
| `tray-{A,B,C}.stl` | print-ready meshes, as oriented |
| `tray-{A,B,C}.3mf` | PrusaSlicer 2.9.6 projects, one tray per bed, config embedded |
| `renders/*.png` | top and 3/4 views of each tray |

## Regenerate

```sh
venv-cq/bin/python slicer/bench/hardware-trays/gen_trays.py            # STLs, renders, 3MFs, slice, README blocks
venv-cq/bin/python slicer/bench/hardware-trays/gen_trays.py --plan     # options and fill table only, writes nothing
venv-cq/bin/python slicer/bench/hardware-trays/gen_trays.py --no-slice
venv-cq/bin/python slicer/bench/hardware-trays/gen_trays.py --holes magnet   # or screw; default none
venv-cq/bin/python slicer/bench/hardware-trays/gen_trays.py --validate REF.stl   # profile check, below
```

Everything is read from the data: the rows of box *Fasteners, Tools & Misc* in `scripts/data/ldo-350-bom.yml`
(re-pinned to the batch sheet on kit day, Step 00.2) and the `tool` roles in
`scripts/data/hardware-ownership.yml`. Re-run after a re-pin; the grid, the split, the compartment sizes and
the labels follow the counts. The script stops on a BOM row it has no rule for (`classify()`), on any
compartment over 70 % fill or under the finger floor, on a slicer stability warning, and if no split fits
six trays. The STLs and renders are byte-identical between runs. About 5 minutes.

Not in a compartment: the PTFE tube, the zip ties, the two aluminium handles and the hand tools. The Motion
box's loose parts (F695 and 625 bearings, pulleys, GT2 idlers, 5×60 shafts, the nozzle-probe shaft, MR85s,
the IDGA gear set, the Bowden coupler) stay sealed in their own kit bags: they are sealed precision parts
that only pick up grit in an open tray, each bag already holds one part type with its name on it, and they
are opened at a few known drive and toolhead steps, not drawn on every session like the screws.

## Fill check

Every compartment is sized so its loose contents fill at most **70 %** of its usable volume, leaving room to
scoop, and the script fails if one does not. Per hardware row:

- **Envelope:** the bounding shape of one piece: a cylinder of the head diameter over the overall length
  for screws (head height + length; length only for FHCS), a cylinder across the corners for hex nuts,
  diameter × thickness for washers, spacers, inserts and magnets, a box for T-nuts. Shank diameter is the
  nominal thread.
- **Bulk volume** = count × envelope ÷ φ, the random-loose packing fraction of that envelope:
  - screws: 0.55 at envelope length/diameter ≤ 2 down to 0.45 at ≥ 8, linear between. Random packings of
    cylinders loosen as they get longer, and the bounding cylinder already pads the shank out to the head
    diameter.
  - set screws, inserts, washers, spacers, T-nuts: 0.55 (short, blocky or flat pieces that interlock or
    shingle).
  - hex nuts, knurled nuts: 0.58; magnets: 0.60 (they chain and stack).
- **Usable volume** = compartment floor area × depth from the floor to the rim (the divider tops), less the
  rounded vertical corners (R2.8) and the scoop cove (R12, or 0.4 × the compartment length on short rows).
- **Fill** = bulk ÷ usable. Compartments are sized from the 70 % rule, with a floor of 25 mm wide × 18 mm long
  so a finger fits, and wider where the label (or a screw lying along X) needs it; spare space is shared out
  in proportion.

Sources for the piece dimensions (column *source* in the generated table):

- ISO 4762 / 7380 / 10642 / 4032 / 7089 / 14583 / 4026: the dimension tables in
  [gumyr/bd_warehouse @eed2da1](https://github.com/gumyr/bd_warehouse/tree/eed2da118da99007ad2d3904466ac0b24964f84d/src/bd_warehouse/data)
  (`socket_head_cap_`, `button_head_`, `countersunk_head_`, `hex_nut_`, `plain_washer_`, `pan_head_parameters.csv`).
  Maxima where the table gives them (SHCS M3 head 5.68, not the nominal 5.5), so the envelopes err large.
- CAD: bounding boxes in the Voron 2.4r2 assembly STEP (VoronDesign/Voron-2) of the part the Voron design
  itself models for that BOM line: the roll-in T-nuts ("2020 Drop-in T-nut", 12.5–13.0 × 7.7 × 4.3), the M3
  hammer-head (10.92 × 9.14 × 4.85), the M5 1 mm shim (10 × 1), the insert's knurl (5.35), the DIN 466-B
  knurled nut (14.08 × 8), the magnet, the M2×10 self-tapper (4.0 × 11.6).
- NAME: the size in the LDO BOM text (M3x5x4 insert, 6x3 magnet, the 1 mm washer).
- EST, no drawing found: the M3×25 wafer head (Ø8 × 1.5), the M3×6 captive screw (as an ISO 4762 head),
  the M5 hammer-head T-nut (as the M3 one, 11 × 9.2 × 5), the twisted M5 split lock washer (9.2 × 2.4).

**Validation of the packing method: none.** No published loose-bulk figure for small screws was found (a
search for loose bulk density of M3 screws or small fasteners turned up only solid density and per-piece
masses), so the φ values are judgement within the brief's ranges, not measured. The implied solid fraction
of the loose pile (count × solid volume ÷ bulk, column *solid/bulk* below) runs from about 0.1 for long
screws to about 0.5 for washers; loose screws in a tray likely lie flatter than that, so the method errs
roomy for long screws. Kit day is the cheap calibration: tip the 283 M3×8 into their compartment and read the
fill against the table.

## Gridfinity

Implemented in CadQuery from the published spec, no Gridfinity library:
[gridfinity.xyz/specification](https://gridfinity.xyz/specification/) ("Gridfinity Design Reference v5",
willtree8) and the constants in
[kennetek/gridfinity-rebuilt-openscad `src/core/standard.scad` @910e22d](https://github.com/kennetek/gridfinity-rebuilt-openscad/blob/910e22d8607fd7f5f51ad5e5cbc5287a76810bfd/src/core/standard.scad).

| Feature | Value used |
|---|---|
| Grid | 42 mm pitch; bin outer 42 n − 0.5 (5 units: 209.5 mm); corner radius 3.75 (Ø7.5) |
| Base, per unit | from the bottom: 0.8 at 45°, 1.8 vertical, 2.15 at 45° (4.75 high); bottom 35.6 square r0.8, top 41.5 r3.75 |
| Height | 7 mm units; bin height 7 u includes the 7 mm base (profile + bridge) and excludes the lip (6U = 42 mm) |
| Stacking lip | from its inner tip at the bin height: 0.7 at 45°, 1.8 vertical, 1.9 at 45° (2.6 deep, 4.4 high) |
| Interior | floor at 7.0 (top of the base); dividers and labels stop 1.2 below the bin height (rebuilt's lip support height), so a bin stacked on top never touches them |
| Holes (option) | magnet Ø6.5 × 2.4, or M3 Ø3 × 6, 8 mm in from each side of every unit; none by default (Clickfinity baseplates hold bins without magnets) |

Two deliberate differences: the outer wall is 2.6 mm (the lip depth) all the way up, so the lip sits on solid
wall and needs no support chamfer; and the lip's knife-edge top is cut back to a 0.3 mm flat, so the bin is
0.3 mm under the spec's 46.4 mm overall (rebuilt rounds the same edge with r0.6 instead).

**Validation** (`--validate`, section through the unit centre, a plain 1 × 1 × 6U bin from this script
against a reference STL, both centred and bottom-aligned):

| Reference | Base outside | Wall outside | Lip inside |
|---|---|---|---|
| Gridfinity Refined, `Bin Handle w Lip.stl` ([Printables 413761](https://www.printables.com/model/413761), CC BY-SA) | 0.012 mm | 0.000 mm | 0.012 mm |
| Gridfinity Lite, `gridfinity-lite-1x1x6.stl` ([Printables 265271](https://www.printables.com/model/265271), CC BY) | 0.250 mm | 0.001 mm | 0.250 mm |

The Refined bin matches the spec to the mesh tolerance. The Lite bin's base and lip are both 0.25 mm per
side inside the spec numbers everywhere (bottom 35.2, not 35.6; lip 2.85 deep, not 2.6): a uniform offset,
the 0.25 clearance an older gridfinity-rebuilt applied to the profile itself. Either fits a standard
baseplate; these trays follow the current spec numbers.

## Print

Core One+, textured sheet, any PLA, door open. Each project carries its config, flattened from the
PrusaSlicer 2.9.6 system presets `0.20mm BALANCED @COREONE HF0.4` + `Prusament PLA @COREONE HF0.4` +
`Prusa CORE One HF0.4 nozzle` (`slicer/resolve_preset.py`), with this repo's printer-wide lines: the vendored
cold start (`slicer/coreone-cold-start.gcode`) and `M106 P3 S160` / `M106 P3 R` in the filament start/end
G-code (AFS bypass flaps, as `slicer/bay-ducts-petg.ini` does for PETG). Supports off. Nothing else is
overridden (2 perimeters, 15 % infill, 0.2 mm layers). The base's 45° steps print without support.

**Two-colour labels (optional):** the labels, the top 0.6 mm of the dividers and the stacking lip are
everything above the label ledges. In PrusaSlicer's layer slider, add a colour change (M600) at the tray's
*colour change Z* in the slice table below (the first layer above the ledges), then load the label colour
when the printer asks.

**No lids.** A bin stacked on a tray of the same footprint closes it (its base sits in the stacking lip), and
the bins sit on any Gridfinity baseplate. Which trays stack, and which fit the optional closed carry box,
[Gridfinity 5×4 rugged case, Voron Edition](https://www.printables.com/model/857097) (Akio, CC BY-NC-SA; a
5 × 4 grid of 6U bins), is worked out in the generated block below.

**Four-tray option (not built).** Splitting tray C into the small parts (nuts, inserts, washers, spacers,
magnets: 4 × 3 × 3U, 3 h 19 m, 121 g, fullest 65 %) and the T-nuts (5 × 2 × 6U, 3 h 34 m, 142 g, fullest 67 %)
saves about 1.1 h and 44 g against tray C (8 h 03 m, 307 g; sliced 2026-10-05), for one more tray. The
generator builds it with `--least-units`.

<!-- BEGIN generated:layout -->
Generated from `scripts/data/ldo-350-bom.yml` (box *Fasteners, Tools & Misc*, fetched 2026-09-24). Each tray is sized on its own: the smallest footprint, then the lowest height, that holds its group at ≤ 70% fill with the finger floor.

Group split (A = M2/M3 screws, B = M4/M5 screws, C = the rest): 3 trays, 390 bin units: M2 · M3 SCREWS 5×5×6U + M4 · M5 SCREWS 5×4×6U + NUTS · INSERTS · WASHERS · MAGNETS · T-NUTS 5×4×6U. Bin units = Σ n·m·U, a plastic proxy. No split needs fewer trays. Fewest bin units: 4 trays, 366 bin units: M2 · M3 SCREWS 5×5×6U + M4 · M5 SCREWS 5×4×6U + NUTS · INSERTS · WASHERS · MAGNETS 4×3×3U + T-NUTS 5×2×6U. Chosen: the group split.

Usable depth (floor to rim) by height: 2U 5.8 mm, 3U 12.8 mm, 4U 19.8 mm, 5U 26.8 mm, 6U 33.8 mm.

| tray | chosen | other footprints that hold it (lowest U each) |
|---|---|---|
| A | 5 × 5 × 6U |  |
| B | 5 × 4 × 6U | 4 × 5 × 6U, 5 × 5 × 5U |
| C | 5 × 4 × 6U | 4 × 5 × 6U, 5 × 5 × 5U |

Stacking: a bin rests on another bin's stacking lip only if both have the same footprint (the lip runs round the rim, so a smaller bin's feet would drop inside). B and C stack on each other; A stacks with nothing.
Trays B, C fit the 5 × 4, 6U rugged case, but not all at once. A does not.

**Tray A — M2 · M3 SCREWS:** Gridfinity 5 × 5 × 6U (209.5 × 209.5 × 42 mm + lip), 17 compartments in 4 rows (row 1 is the front); fullest M3×40 SHCS at 69%.

| row | label | count | piece envelope mm | φ | bulk cm³ | size mm | usable cm³ | fill |
|---:|---|---:|---|---:|---:|---|---:|---:|
| 1 | M3×8 · SHCS 283 | 283 | cyl 5.68 × 11 | 0.55 | 143.4 | 106 × 59 × 33.8 | 209.6 | 68% |
| 1 | M3×12 · SHCS 50 | 50 | cyl 5.68 × 15 | 0.54 | 35.2 | 29 × 59 × 33.8 | 57.6 | 61% |
| 1 | M3×16 · SHCS 30 | 30 | cyl 5.68 × 19 | 0.53 | 27.4 | 30 × 59 × 33.8 | 58.0 | 47% |
| 1 | M3×20 · SHCS 40 | 40 | cyl 5.68 × 23 | 0.52 | 45.2 | 34 × 59 × 33.8 | 66.0 | 68% |
| 2 | M3×25 · SHCS 12 | 12 | cyl 5.68 × 28 | 0.50 | 17.0 | 35 × 28 × 33.8 | 31.3 | 54% |
| 2 | M3×30 · SHCS 44 | 44 | cyl 5.68 × 33 | 0.49 | 75.6 | 121 × 28 × 33.8 | 110.1 | 69% |
| 2 | M3×35 · SHCS 6 | 6 | cyl 5.68 × 38 | 0.47 | 12.2 | 45 × 28 × 33.8 | 40.5 | 30% |
| 3 | M3×40 · SHCS 34 | 34 | cyl 5.68 × 43 | 0.46 | 81.0 | 77 × 46 × 33.8 | 117.2 | 69% |
| 3 | M3×50 · SHCS 4 | 4 | cyl 5.68 × 53 | 0.45 | 11.9 | 60 × 46 × 33.8 | 90.8 | 13% |
| 3 | M3×6 · BHCS 14 | 14 | cyl 5.7 × 7.65 | 0.55 | 5.0 | 29 × 46 × 33.8 | 44.0 | 11% |
| 3 | M3×25 · BHCS 6 | 6 | cyl 5.7 × 26.65 | 0.51 | 8.1 | 33 × 46 × 33.8 | 50.1 | 16% |
| 4 | M3×6 · FHCS 42 | 42 | cyl 6 × 6 | 0.55 | 13.0 | 31 × 19 × 33.8 | 19.0 | 68% |
| 4 | M3×10 · FHCS 8 | 8 | cyl 6 × 10 | 0.55 | 4.1 | 30 × 19 × 33.8 | 18.0 | 23% |
| 4 | M3×25 · WAFER 3 | 3 | cyl 8 × 26.5 | 0.53 | 7.6 | 33 × 19 × 33.8 | 20.3 | 37% |
| 4 | M3×6 · CAPTIVE 2 | 2 | cyl 5.68 × 9 | 0.55 | 0.8 | 35 × 19 × 33.8 | 21.3 | 4% |
| 4 | M2×10 · SELF-TAP 43 | 43 | cyl 4 × 11.6 | 0.54 | 11.7 | 41 × 19 × 33.8 | 24.8 | 47% |
| 4 | M3×2 · SET 5 | 5 | cyl 3 × 2 | 0.55 | 0.1 | 26 × 19 × 33.8 | 15.6 | 1% |

**Tray B — M4 · M5 SCREWS:** Gridfinity 5 × 4 × 6U (209.5 × 167.5 × 42 mm + lip), 8 compartments in 3 rows (row 1 is the front); fullest M5×10 BHCS at 67%.

| row | label | count | piece envelope mm | φ | bulk cm³ | size mm | usable cm³ | fill |
|---:|---|---:|---|---:|---:|---|---:|---:|
| 1 | M5×40 · SHCS 26 | 26 | cyl 8.72 × 45 | 0.50 | 140.5 | 176 × 37 × 33.8 | 213.9 | 66% |
| 1 | M4×6 · BHCS 8 | 8 | cyl 7.6 × 8.2 | 0.55 | 5.4 | 27 × 37 × 33.8 | 32.2 | 17% |
| 2 | M5×6 · BHCS 1 | 1 | cyl 9.5 × 8.75 | 0.55 | 1.1 | 26 × 28 × 33.8 | 24.1 | 5% |
| 2 | M5×10 · BHCS 54 | 54 | cyl 9.5 × 12.75 | 0.55 | 88.7 | 144 × 28 × 33.8 | 133.3 | 67% |
| 2 | M5×14 · BHCS 4 | 4 | cyl 9.5 × 16.75 | 0.55 | 8.6 | 30 × 28 × 33.8 | 28.0 | 31% |
| 3 | M5×16 · BHCS 43 | 43 | cyl 9.5 × 18.75 | 0.55 | 103.9 | 83 × 58 × 33.8 | 158.1 | 66% |
| 3 | M5×30 · BHCS 26 | 26 | cyl 9.5 × 32.75 | 0.53 | 114.8 | 91 × 58 × 33.8 | 174.6 | 66% |
| 3 | M4×4 · SET 32 | 32 | cyl 4 × 4 | 0.55 | 2.9 | 27 × 58 × 33.8 | 50.7 | 6% |

**Tray C — NUTS · INSERTS · WASHERS · MAGNETS · T-NUTS:** Gridfinity 5 × 4 × 6U (209.5 × 167.5 × 42 mm + lip), 13 compartments in 4 rows (row 1 is the front); fullest M3 T-NUT ROLL-IN at 66%.

| row | label | count | piece envelope mm | φ | bulk cm³ | size mm | usable cm³ | fill |
|---:|---|---:|---|---:|---:|---|---:|---:|
| 1 | M3 NUT · HEX 14 | 14 | cyl 6.35 × 2.4 | 0.58 | 1.8 | 37 × 20 × 33.8 | 23.9 | 8% |
| 1 | M5 NUT · HEX 30 | 30 | cyl 9.24 × 4.7 | 0.58 | 16.3 | 42 × 20 × 33.8 | 26.8 | 61% |
| 1 | M3 INSERT · HEAT-SET 153 | 153 | cyl 5.35 × 4 | 0.55 | 25.0 | 64 × 20 × 33.8 | 41.1 | 61% |
| 1 | M3 WASHER · 6 | 6 | cyl 7 × 0.55 | 0.55 | 0.2 | 57 × 20 × 33.8 | 36.7 | 1% |
| 2 | M5 WASHER · 1 mm · 9 | 9 | cyl 10 × 1 | 0.55 | 1.3 | 53 × 20 × 33.8 | 34.4 | 4% |
| 2 | M5 SPACER · 1 mm · 46 | 46 | cyl 10 × 1 | 0.55 | 6.6 | 49 × 20 × 33.8 | 31.9 | 21% |
| 2 | M5 LOCK · WASHER 2 | 2 | cyl 9.2 × 2.4 | 0.55 | 0.6 | 40 × 20 × 33.8 | 25.6 | 2% |
| 2 | M4 KNURLED · NUT 4 | 4 | cyl 14.08 × 8 | 0.58 | 8.6 | 57 × 20 × 33.8 | 36.6 | 23% |
| 3 | 6×3 MAGNET · 16 | 16 | cyl 6 × 3 | 0.60 | 2.3 | 57 × 32 × 33.8 | 60.0 | 4% |
| 3 | M3 T-NUT · ROLL-IN 135 | 135 | box 12.5 × 7.7 × 4.3 | 0.55 | 101.6 | 146 × 32 × 33.8 | 154.8 | 66% |
| 4 | M5 T-NUT · ROLL-IN 80 | 80 | box 13 × 7.7 × 4.3 | 0.55 | 62.6 | 77 × 38 × 33.8 | 96.0 | 65% |
| 4 | M3 T-NUT · HAMMER 75 | 75 | box 10.92 × 9.14 × 4.85 | 0.55 | 66.0 | 81 × 38 × 33.8 | 101.2 | 65% |
| 4 | M5 T-NUT · HAMMER 16 | 16 | box 11 × 9.2 × 5 | 0.55 | 14.7 | 42 × 38 × 33.8 | 52.7 | 28% |

Piece data and sources:

| BOM item | solid mm³ | envelope mm³ | solid/bulk | source |
|---|---:|---:|---:|---|
| Machine Screw, SHCS, M3x8 | 133 | 279 | 0.26 | ISO 4762 |
| Machine Screw, SHCS, M3x12 | 161 | 380 | 0.23 | ISO 4762 |
| Machine Screw, SHCS, M3x16 | 189 | 481 | 0.21 | ISO 4762 |
| Machine Screw, SHCS, M3x20 | 217 | 583 | 0.19 | ISO 4762 |
| Machine Screw, SHCS, M3x25 | 253 | 709 | 0.18 | ISO 4762 |
| Machine Screw, SHCS, M3x30 | 288 | 836 | 0.17 | ISO 4762 |
| Machine Screw, SHCS, M3x35 | 323 | 963 | 0.16 | ISO 4762 |
| Machine Screw, SHCS, M3x40 | 359 | 1090 | 0.15 | ISO 4762 |
| Machine Screw, SHCS, M3x50 | 429 | 1343 | 0.14 | ISO 4762 |
| Machine Screw, BHCS, M3x6 | 85 | 195 | 0.24 | ISO 7380 |
| Machine Screw, BHCS, M3x25 | 219 | 680 | 0.16 | ISO 7380 |
| Machine Screw, FHCS, M3x6 | 58 | 170 | 0.19 | ISO 10642 |
| Machine Screw, FHCS, M3x10 | 87 | 283 | 0.17 | ISO 10642 |
| Machine Screw, Wafer head, M3x25 | 252 | 1332 | 0.10 | EST (wafer head 8 × 1.5) |
| Machine Screw, Captive, M3x6 | 118 | 228 | 0.29 | EST (as ISO 4762 head) |
| Self-tapping Screw, M2x10 | 52 | 146 | 0.19 | ISO 14583 pan head; CAD 4.0 × 11.6 |
| Set Screw, M3x2, Pre-applied Threadlocker | 14 | 14 | 0.55 | ISO 4026 (d × L) |
| Machine Screw, SHCS, M5x40 | 1084 | 2687 | 0.20 | ISO 4762 |
| Machine Screw, BHCS, M4x6 | 175 | 372 | 0.26 | ISO 7380 |
| Machine Screw, BHCS, M5x6 | 313 | 620 | 0.28 | ISO 7380 |
| Machine Screw, BHCS, M5x10 | 391 | 904 | 0.24 | ISO 7380 |
| Machine Screw, BHCS, M5x14 | 470 | 1187 | 0.22 | ISO 7380 |
| Machine Screw, BHCS, M5x16 | 509 | 1329 | 0.21 | ISO 7380 |
| Machine Screw, BHCS, M5x30 | 784 | 2321 | 0.18 | ISO 7380 |
| Set Screw, M4x4, Pre-applied Threadlocker | 50 | 50 | 0.55 | ISO 4026 (d × L) |
| Hexnut, M3 | 46 | 76 | 0.35 | ISO 4032 s, m |
| Hexnut, M5 | 168 | 315 | 0.31 | ISO 4032 s, m |
| Heatset Insert, Brass, M3x5x4 | 62 | 90 | 0.38 | NAME; CAD knurl 5.35 |
| Washer, M3 | 17 | 21 | 0.45 | ISO 7089 |
| Washer, M5, 1mm | 59 | 79 | 0.41 | ISO 7089; NAME thickness |
| Precision Spacer, M5, 1mm | 59 | 79 | 0.41 | CAD (M5 1mm Shim 10 × 1) |
| Locking Washer, M5 | 56 | 160 | 0.19 | EST (DIN 127 split, twisted) |
| Knurled Nut, M4 | 747 | 1246 | 0.35 | CAD (DIN 466-B) |
| 6x3mm Neodymium Magnet | 85 | 85 | 0.60 | NAME; CAD |
| T-nut, Roll-in, 2020, M3 | 286 | 414 | 0.38 | CAD |
| T-nut, Roll-in, 2020, M5 | 272 | 430 | 0.35 | CAD |
| T-nut, Hammer Head, 2020, M3 | 185 | 484 | 0.21 | CAD |
| T-nut, Hammer Head, 2020, M5 | 190 | 506 | 0.21 | EST |

Not in a compartment: Teflon Tube (4mm OD 3mm ID) - 1.2m; Zip Ties, 3x150mm; Brass Heatset Insert tool (for M3 Brass Inserts); Drill bit, 2mm; Hex Wrench, 1.5mm; Hex Wrench, 2mm; Hex Wrench, 2.5mm; Hex Wrench, 3mm; Hex Wrench, 4mm; Slot head screwdriver, 2.5mm; Aluminium Handle.
<!-- END generated:layout -->

<!-- BEGIN generated:slice -->
| file | bin | time | g PLA | colour change Z | extents on the bed, mm | supports |
|---|---|---|---:|---:|---|---|
| `tray-A.3mf` | 5 × 5 × 6U | 9h 20m 30s | 359 | 40.40 | X 20.4–229.6, Y 5.4–214.6, Z ≤ 46.00 | none |
| `tray-B.3mf` | 5 × 4 × 6U | 7h 7m 30s | 277 | 40.40 | X 20.4–229.6, Y 26.4–193.6, Z ≤ 46.00 | none |
| `tray-C.3mf` | 5 × 4 × 6U | 8h 2m 54s | 307 | 40.40 | X 20.4–229.6, Y 26.4–193.6, Z ≤ 46.00 | none |

All trays: **24.5 h, 943 g**. PrusaSlicer 2.9.6 CLI estimates, one tray per bed, not GUI-arranged; 2 perimeters, 15% infill; slicer stability notes: Long bridging extrusions (the base grooves, expected). The colour-change Z is the first label layer, checked against each G-code.
<!-- END generated:slice -->

## Credit and licence

Inspired by **r0bdawg11**, *INDX Upgrade Hardware Organizer*, <https://www.printables.com/model/1794124>
(CC BY): one flat tray, a compartment per hardware type, raised labels, a scoop fillet. Inspiration only;
no geometry is copied. The Gridfinity system is **Zack Freedman**'s; the base and lip here are built from
the published spec numbers, not from any Gridfinity model file.

Licence: the same as the rest of this repository's own content. None has been chosen yet (root README ›
Attribution and licences), so treat it as all rights reserved until one is added. The Gridfinity design
reference graphic asks derived projects to use CC BY-NC-SA; settle that when a licence is chosen.
