# Hardware trays (bench print)

Three ultra-light Gridfinity bins on one common footprint (5 × 4 units), each only as tall as its contents
need, that hold the LDO Voron 2.4 350 kit's fastener bags: one
compartment per hardware row of the kit BOM, two raised label lines (size; type and kit count) on a ledge
behind each row, and a scoop cove along each compartment's front wall. They sit on any Gridfinity baseplate
(Clickfinity included), and any of them stacks on any other. The bags are emptied into them on kit day,
[Ch 00 Step 00.12](../../../docs/manual/00-before-you-start.md#step-0012-empty-the-fastener-bags-into-the-hardware-trays).
A bench print: on no plate, in no batch, run total or spool ledger
([print/README § Bench prints](../../../docs/manual/print/README.md#bench-prints-outside-the-plates)).

| Tray | Holds |
|---|---|
| A | M2 and M3 screws: SHCS by length, BHCS, FHCS, wafer, captive, M2 self-tappers, M3 set screws |
| B | M4 and M5 screws (M5 SHCS, M4 and M5 BHCS, M4 set screws) and the roll-in T-nuts |
| C | the small parts (hex nuts, heat-set inserts, washers, spacers, lock washers, knurled nuts, magnets) and the hammer-head T-nuts, in a low bin |

The kit's hand tools (hex keys, the 2 mm drill bit, the slot screwdriver, the brass insert tip) are not
stored in the trays. Renders (blue = the layers above the label ledges, i.e. the colour-change layers):
`renders/tray-{A,B,C}-top.png` and `renders/tray-{A,B,C}-34.png`.

## Files

| File | What |
|---|---|
| `gen_trays.py` | the only generator (CadQuery, `venv-cq`; no other dependency) |
| `tray-{A,B,C}.stl` | print-ready meshes, as oriented |
| `tray-{A,B,C}.3mf` | PrusaSlicer 2.9.6 projects, one tray per bed, config embedded |
| `renders/*.png` | top and 3/4 views of each tray, and a Y–Z section (`-section.png`) |

## Regenerate

```sh
venv-cq/bin/python slicer/bench/hardware-trays/gen_trays.py            # STLs, renders, 3MFs, slice, README blocks
venv-cq/bin/python slicer/bench/hardware-trays/gen_trays.py --plan     # groupings and fill table only, writes nothing
venv-cq/bin/python slicer/bench/hardware-trays/gen_trays.py --compare 3  # build and slice the 3 best groupings, print h and g
venv-cq/bin/python slicer/bench/hardware-trays/gen_trays.py --lever-study  # slice with the plastic levers added one by one
venv-cq/bin/python slicer/bench/hardware-trays/gen_trays.py --levers none  # the plain (solid-base, 2.6 mm wall) bins
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
  - screws: 1.0 at envelope length/diameter ≤ 2 down to 0.8 at ≥ 8, linear between (from the pour
    simulation below; Alex 2026-10-30, was 0.55 → 0.45). Above 1 because the bounding cylinder pads the
    shank out to the head diameter and heads nest against shanks; random packings still loosen as screws
    get longer.
  - set screws, inserts, washers, spacers, T-nuts: 0.55 (short, blocky or flat pieces that interlock or
    shingle).
  - hex nuts, knurled nuts: 0.58; magnets: 0.60 (they chain and stack).
- **Usable volume** = compartment floor area × depth from the floor to the rim (the divider tops), less the
  rounded vertical corners (R2.9), the scoop cove (always R12: compartments are at least 18 mm long and 21 mm deep, so it never shrinks), and
  on a side against the outer wall the 1.74 × 1.74 mm 45° sliver of the lip support.
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

**Validation (2026-10-30, rigid-body pour simulation, MuJoCo 3.17).** Each BOM line was poured loose
into its compartment's footprint (steel, friction 0.35 and 0.7) and the bulk read as the volume under the
settled pile. Steel balls came out at 0.63–0.64 (real loose pours ≈ 0.60), so the method packs about 6 %
dense. Short screws that settled cleanly (M3×6 FHCS, M3×12, M2×10, M5×10/16 BHCS) gave an envelope φ of
1.1–1.8 against this script's 0.54–0.55: heads nest against shanks, so those compartments are 2–3× the
room the pieces need. The hammer-head T-nut boxes gave 0.57–0.84 against 0.55: about right, ~70 % full.
Long screws (M3×25 and up, M5×30/40) and the 283 M3×8 did not settle stably and give no number; the
unstable M3×20 run (0.91–1.01) and M5×40 runs (0.77–0.90) are the only hints. Rev D+ fastener counts
equal the pinned Rev D rows (checked 2026-10-30). Taken (Alex 2026-10-30, before any tray was printed):
screws 1.0 → 0.8, which shrinks the set from three 5 × 5 trays (375 bin units, 18.6 h, 652 g) to three
5 × 4 (280). The two-tray 5 × 5 grouping (300 bin units, 16.4 h, 575 g) lost on plastic. Risk: the long
screws; at the M5×40 runs' low 0.77 that compartment is about 80 % full instead of 70 %.

**Packing method before the simulation.** No published loose-bulk figure for small screws was found (a
search for loose bulk density of M3 screws or small fasteners turned up only solid density and per-piece
masses), so the φ values (screws 0.55 → 0.45) were judgement within the brief's ranges, not measured. The implied solid fraction
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
| Interior | floor at 5.8 (a floor over solid, infilled feet, below); dividers and labels stop 1.2 below the bin height (rebuilt's lip support height), so a bin stacked on top never touches them |
| Holes (option) | magnet Ø6.5 × 2.4, or M3 Ø3 × 6, 8 mm in from each side of every unit; none by default (Clickfinity baseplates hold bins without magnets) |

Deliberate differences: the lip's knife-edge top is cut back to a 0.3 mm flat, so the bin is 0.3 mm under
the spec's height (rebuilt rounds the same edge with r0.6 instead); the inside is ultra-light (§ Ultra-light
below). The outside, feet and lip included, is unchanged, and the validation below is of these bins.

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

Core One+, satin sheet (the PLA sheet, per `docs/manual/print/00-slicer-setup.md` § Print sheet), any PLA, door open. Each project carries its config, flattened from the
PrusaSlicer 2.9.6 system presets `0.20mm BALANCED @COREONE HF0.4` + `Prusament PLA @COREONE HF0.4` +
`Prusa CORE One HF0.4 nozzle` (`slicer/resolve_preset.py`), with this repo's printer-wide lines: the vendored
cold start (`slicer/coreone-cold-start.gcode`), Z offset +0.05 (the hot nozzle sits lower than the cold
probe found; ASA on satin needed +0.08, Alex 2026-10-30) and `M106 P3 S160` / `M106 P3 R` in the filament start/end
G-code (AFS bypass flaps, as `slicer/bay-ducts-petg.ini` does for PETG). Supports off. Ultra-light settings:
2 perimeters, 3 top and 3 bottom layers (minimum-thickness rules off, so it is 3 layers), 10 % infill; nothing
else is overridden (0.2 mm layers, 0.45 mm lines). The base's 45° steps print without support.

**Two-colour labels:** the labels, the top 0.6 mm of the dividers and the stacking lip are everything above
the label ledges. Each 3MF carries a colour change (M600) at the tray's *colour change Z* in the slice table
below (the first layer above the ledges; Alex 2026-10-30), so the printer stops there by itself: load the
label colour when it asks. For one colour, delete the change in the layer slider or just reload the same
spool.

**No lids.** A bin stacked on a tray of the same footprint closes it (its base sits in the stacking lip), and
the bins sit on any Gridfinity baseplate. Which trays stack, and which fit the optional closed carry box,
[Gridfinity 5×4 rugged case, Voron Edition](https://www.printables.com/model/857097) (Akio, CC BY-NC-SA; a
5 × 4 grid of 6U bins), is worked out in the generated block below.

**Grouping.** The generator groups whole hardware families (M2/M3 screws, M4/M5 screws, roll-in T-nuts,
hammer-head T-nuts, small parts) into at most three trays on one common footprint, each tray at its lowest
height: the fewest bin units (Σ n·m·U, a plastic proxy), then the fewest trays (Alex 2026-10-30: three 5 × 4
over two 5 × 5); groupings that tie on bin units are sliced and the lightest wins. No tray is lower than **`MIN_U` = 4** (Alex: parts must not spill when a
tray tilts), and every piece lying flat stays at least 2 mm below the rim. At the screw φ of 1.0 → 0.8 the
result is the generated block below: three 5 × 4 trays, 15.1 h, 547 g (solid feet). History: at the earlier φ of 0.55 → 0.45
only 5 × 5 held the M2/M3 screws; with `MIN_U` = 4 the best three groupings then, all sliced (`--compare 3`,
ultra-light, 2026-10-05):

| Grouping (A / B / C) | Bin units | Time | PLA |
|---|---:|---|---:|
| M2/M3 6U / M4/M5 + hammer-head T-nuts 5U / roll-in T-nuts + small parts 4U (built to 2026-10-30, never printed) | 375 | 18.6 h | 652 g |
| M2/M3 6U / M4/M5 5U / all T-nuts + small parts 4U | 375 | 18.9 h | 663 g |
| M2/M3 6U / M4/M5 + roll-in T-nuts 6U / hammer-head T-nuts + small parts 4U | 400 | 19.2 h | 676 g |

The 4U floor costs 16 g and 0.4 h against the 3U small-parts tray it replaces (636 g, 18.2 h). The extra depth
moves nothing: the first two tie on bin units, so the slice decides, and the grouping then built was the
lighter by 11 g. Putting all the T-nuts with the M4/M5 screws still does not fit a 6U bin.

Every compartment has the full R12 scoop cove on its front wall, solid. `renders/tray-{A,B,C}-section.png`
are Y–Z sections through each tray at a third of its width, drawn from the STL, showing the coves, the label
ledges, the infilled feet and the lip.

## Ultra-light

Ideas from **HuMa**, *Gridfinity Ultra Light Bins* ([Printables 627719](https://www.printables.com/model/627719),
CC BY-NC-SA: 37 % less filament than a standard bin, a 3 × 4 × 6 bin 62 g instead of 98 g at 2 walls, 3 top
and bottom layers, 10 % infill). Ideas only; no geometry is used. Each lever, sliced with the others before it
(`--lever-study`, 2026-10-05, before `MIN_U` = 4 and the fixed R12 cove; grouping and heights re-chosen at
each step):

| Lever | A | B | C | All | Change | Kept |
|---|---:|---:|---:|---:|---:|---|
| none (the bins as approved: solid 7 mm base, 2.6 mm wall, 1.8 mm dividers) | 359 g 6U | 329 g 6U | 227 g 3U | 915 g, 23.8 h | | |
| `settings`: 2 perimeters, 3 top / 3 bottom, 10 % infill | 306 | 278 | 187 | 771 g, 20.3 h | −144 g | yes |
| `thin`: outer wall and dividers 0.86 mm (exactly 2 perimeters); lip on a 45° support | 271 | 214 (5U) | 207 (4U) | 692 g, 18.8 h | −79 g | yes |
| `ledges`: hollow under each label ledge, 45° roof | 269 | 219 | 219 | 707 g, 20.2 h | +15 g | **no** |
| `coves`: hollow inside each scoop cove, 45° roof | 274 | 225 | 225 | 724 g, 20.9 h | +17 g | **no** |
| `base`: hollow feet under a floor plate (with the two above still on) | 259 | 212 | 184 (3U) | 655 g, 19.8 h | −69 g | yes |
| **built**: `settings` + `thin` + `base` | 262 | 207 | 167 | **636 g, 18.2 h** | **−279 g (−30 %)** | |

- **Settings** pays most: the trays are almost all wall, so cutting top layers and infill takes plastic off
  every floor and ledge. All three trays slice with **0 gap-fill extrusions**.
- **Thin walls**: a 0.45 mm line at 0.2 mm layers spaces at 0.407, so two perimeters make a 0.86 mm wall
  with nothing between them. With a wall thinner than the 2.6 mm lip, the lip's inner tip sits on a 45° ring
  (from the wall face 1.74 mm below the rim up to the tip line at the rim, then straight up to the bin
  height): the same support gridfinity-rebuilt uses, and the load path for a stacked bin. The lip itself
  is left as the spec draws it: its 6.8 mm² section is at most ~5 g a tray, and it carries the stack. The
  tray name on the front face is dropped: a cut into a 0.86 mm wall leaves less than two perimeters.
- **Hollow ledges and coves cost plastic.** At 10 % infill a void inside a 13 mm ledge or a cove adds two
  perimeters round it on every layer, more than the sparse infill it replaces, and more print time. Both are
  implemented (`--levers settings,thin,ledges,coves,base`) and off.
- **Low floor (`base`)**: the compartment floor is flat at 5.8, 1.05 mm over the base top (z 4.75), 1.2 mm
  lower than before. The feet under it are **solid** and slice with the 10 % infill (Alex 2026-10-30): as
  closed shells (`pockets`, now off: 0.86 mm walls, a 0.6 mm pocket floor) they got no infill and the floor
  bridged about 40 mm over each pocket; solid, the floor's first layer spans one 10 % grid cell (~9 mm).
  Solid feet cost 16 g (547 against 531 g) and no time. The call: a **flat floor**, not floors dipping
  into the feet as HuMa's bins do. Dipped floors would leave a 5 mm ridge every 42 mm across every
  compartment, wells with 45° sides where washers, magnets and set screws collect, and V-notches where a
  divider crosses a well; the coves would hang over the wells. PrusaSlicer's stability check lists the floor's first
  layer over sparse infill with the base grooves as "Long bridging extrusions" (no supports). No tray drops a height unit from
  the lower floor alone (2026-10-05, at the old φ): A still needed 6U, and `MIN_U` keeps C at 4U. Holes (`--holes`) need
  solid feet, which is now the default.

**Strength.** Tray A full is about 0.5 kg of steel.
- *Lifted by one end*: the tray is a box 209.5 × 209.5 × 42 mm with 0.86 mm walls. Every 25–80 mm a 0.86 mm
  divider is fused to the outer wall, and every row ends in a solid 13.2 mm label ledge running wall to wall
  (ribs). The floor sits on 20 infilled feet. The worst case, held at one edge with the steel
  spread evenly, puts about 0.5 N·m of bending on that section: well under 1 MPa in PLA, which yields near
  50 MPa. The lip is solid, so it is a sound place to grip.
- *Two full trays stacked*: about 5 N rests on the lower tray's lip ring, about 820 mm long, carried by the
  45° support into the walls: a few kPa.
- *Floor*: carried by the feet's 10 % grid; the longest span is one ~9 mm cell.
- Every wall and divider is at least 2 perimeters, the floors at least 3 layers. Nothing here is close to
  a limit; the limit in use is a drop, not a load.

<!-- BEGIN generated:layout -->
Generated from `scripts/data/ldo-350-bom.yml` (box *Fasteners, Tools & Misc*, fetched 2026-10-30). Each tray is sized on its own: the smallest footprint, then the lowest height, that holds its group at ≤ 70% fill with the finger floor.

20 groupings of whole families fit ≤ 3 trays on one common footprint, each tray at its lowest height. Best five by bin units (Σ n·m·U, the plastic proxy):

1. 3 trays, 280 bin units: M2/M3 screws 5×4×5U | M4/M5 screws + roll-in T-nuts 5×4×5U | hammer-head T-nuts + small parts 5×4×4U ← chosen
2. 3 trays, 280 bin units: M2/M3 screws 5×4×5U | M4/M5 screws + hammer-head T-nuts 5×4×5U | roll-in T-nuts + small parts 5×4×4U
3. 2 trays, 300 bin units: M2/M3 screws + roll-in T-nuts 5×5×6U | M4/M5 screws + hammer-head T-nuts + small parts 5×5×6U
4. 3 trays, 300 bin units: M2/M3 screws 5×4×5U | M4/M5 screws 5×4×4U | roll-in T-nuts + hammer-head T-nuts + small parts 5×4×6U
5. 3 trays, 300 bin units: M2/M3 screws 4×5×6U | M4/M5 screws 4×5×4U | roll-in T-nuts + hammer-head T-nuts + small parts 4×5×5U

2 groupings tie at 280 bin units; sliced: 1. 547 g, 15.1 h; 2. 563 g, 15.5 h. Chosen: 1, the lightest.

Usable depth (floor to rim) by height: 4U 21.0 mm, 5U 28.0 mm, 6U 35.0 mm.

| tray | bin | thickest piece lying flat (mm) | lowest height the fill allows |
|---|---|---:|---|
| A | 5 × 4 × 5U | 8 | 5U |
| B | 5 × 4 × 5U | 9.5 | 5U |
| C | 5 × 4 × 4U | 8 | 4U |

Stacking: a bin rests on another bin's stacking lip only if both have the same footprint (the lip runs round the rim, so a smaller bin's feet would drop inside). A, B and C share a footprint: any of them stacks on any other.
Trays A, B, C fit the 5 × 4, 6U rugged case, but not all at once.

**Tray A — M2 · M3 SCREWS:** Gridfinity 5 × 4 × 5U (209.5 × 167.5 × 35 mm + lip), 17 compartments in 4 rows (row 1 is the front); fullest M3×40 SHCS at 68%.

| row | label | count | piece envelope mm | φ | bulk cm³ | size mm | usable cm³ | fill |
|---:|---|---:|---|---:|---:|---|---:|---:|
| 1 | M3×8 · SHCS 283 | 283 | cyl 5.68 × 11 | 1.00 | 78.9 | 109 × 40 × 28.0 | 119.3 | 66% |
| 1 | M3×12 · SHCS 50 | 50 | cyl 5.68 × 15 | 0.98 | 19.4 | 30 × 40 × 28.0 | 33.1 | 59% |
| 1 | M3×16 · SHCS 30 | 30 | cyl 5.68 × 19 | 0.96 | 15.1 | 31 × 40 × 28.0 | 33.3 | 45% |
| 1 | M3×20 · SHCS 40 | 40 | cyl 5.68 × 23 | 0.93 | 25.0 | 35 × 40 × 28.0 | 37.8 | 66% |
| 2 | M3×25 · SHCS 12 | 12 | cyl 5.68 × 28 | 0.90 | 9.4 | 38 × 20 × 28.0 | 19.6 | 48% |
| 2 | M3×30 · SHCS 44 | 44 | cyl 5.68 × 33 | 0.87 | 42.1 | 120 × 20 × 28.0 | 63.4 | 67% |
| 2 | M3×35 · SHCS 6 | 6 | cyl 5.68 × 38 | 0.84 | 6.8 | 48 × 20 × 28.0 | 25.2 | 27% |
| 3 | M3×40 · SHCS 34 | 34 | cyl 5.68 × 43 | 0.81 | 45.5 | 79 × 32 × 28.0 | 67.1 | 68% |
| 3 | M3×50 · SHCS 4 | 4 | cyl 5.68 × 53 | 0.80 | 6.7 | 61 × 32 × 28.0 | 51.8 | 13% |
| 3 | M3×6 · BHCS 14 | 14 | cyl 5.7 × 7.65 | 1.00 | 2.7 | 30 × 32 × 28.0 | 25.0 | 11% |
| 3 | M3×25 · BHCS 6 | 6 | cyl 5.7 × 26.65 | 0.91 | 4.5 | 36 × 32 × 28.0 | 30.0 | 15% |
| 4 | M3×6 · FHCS 42 | 42 | cyl 6 × 6 | 1.00 | 7.1 | 32 × 20 × 28.0 | 16.0 | 44% |
| 4 | M3×10 · FHCS 8 | 8 | cyl 6 × 10 | 1.00 | 2.3 | 31 × 20 × 28.0 | 15.6 | 14% |
| 4 | M3×25 · WAFER 3 | 3 | cyl 8 × 26.5 | 0.96 | 4.2 | 35 × 20 × 28.0 | 17.6 | 24% |
| 4 | M3×6 · CAPTIVE 2 | 2 | cyl 5.68 × 9 | 1.00 | 0.5 | 36 × 20 × 28.0 | 18.4 | 2% |
| 4 | M2×10 · SELF-TAP 43 | 43 | cyl 4 × 11.6 | 0.97 | 6.5 | 42 × 20 × 28.0 | 21.5 | 30% |
| 4 | M3×2 · SET 5 | 5 | cyl 3 × 2 | 0.55 | 0.1 | 28 × 20 × 28.0 | 14.4 | 1% |

**Tray B — M4 · M5 SCREWS · T-NUTS:** Gridfinity 5 × 4 × 5U (209.5 × 167.5 × 35 mm + lip), 10 compartments in 2 rows (row 1 is the front); fullest M5×40 SHCS at 70%.

| row | label | count | piece envelope mm | φ | bulk cm³ | size mm | usable cm³ | fill |
|---:|---|---:|---|---:|---:|---|---:|---:|
| 1 | M5×40 · SHCS 26 | 26 | cyl 8.72 × 45 | 0.89 | 78.1 | 76 × 54 × 28.0 | 111.9 | 70% |
| 1 | M4×6 · BHCS 8 | 8 | cyl 7.6 × 8.2 | 1.00 | 3.0 | 25 × 54 × 28.0 | 37.0 | 8% |
| 1 | M5×6 · BHCS 1 | 1 | cyl 9.5 × 8.75 | 1.00 | 0.6 | 25 × 54 × 28.0 | 37.0 | 2% |
| 1 | M5×10 · BHCS 54 | 54 | cyl 9.5 × 12.75 | 1.00 | 48.8 | 47 × 54 × 28.0 | 70.0 | 70% |
| 1 | M5×14 · BHCS 4 | 4 | cyl 9.5 × 16.75 | 1.00 | 4.7 | 31 × 54 × 28.0 | 45.4 | 10% |
| 2 | M5×16 · BHCS 43 | 43 | cyl 9.5 × 18.75 | 1.00 | 57.1 | 36 × 84 × 28.0 | 82.0 | 70% |
| 2 | M5×30 · BHCS 26 | 26 | cyl 9.5 × 32.75 | 0.95 | 63.4 | 40 × 84 × 28.0 | 91.1 | 70% |
| 2 | M4×4 · SET 32 | 32 | cyl 4 × 4 | 0.55 | 2.9 | 25 × 84 × 28.0 | 57.9 | 5% |
| 2 | M3 T-NUT · ROLL-IN 135 | 135 | box 12.5 × 7.7 × 4.3 | 0.55 | 101.6 | 63 × 84 × 28.0 | 145.9 | 70% |
| 2 | M5 T-NUT · ROLL-IN 80 | 80 | box 13 × 7.7 × 4.3 | 0.55 | 62.6 | 41 × 84 × 28.0 | 93.9 | 67% |

**Tray C — NUTS · INSERTS · WASHERS · MAGNETS · T-NUTS:** Gridfinity 5 × 4 × 4U (209.5 × 167.5 × 28 mm + lip), 11 compartments in 3 rows (row 1 is the front); fullest M3 T-NUT HAMMER at 58%.

| row | label | count | piece envelope mm | φ | bulk cm³ | size mm | usable cm³ | fill |
|---:|---|---:|---|---:|---:|---|---:|---:|
| 1 | M3 NUT · HEX 14 | 14 | cyl 6.35 × 2.4 | 0.58 | 1.8 | 42 × 36 × 21.0 | 30.6 | 6% |
| 1 | M5 NUT · HEX 30 | 30 | cyl 9.24 × 4.7 | 0.58 | 16.3 | 40 × 36 × 21.0 | 29.1 | 56% |
| 1 | M3 INSERT · HEAT-SET 153 | 153 | cyl 5.35 × 4 | 0.55 | 25.0 | 60 × 36 × 21.0 | 44.0 | 57% |
| 1 | M3 WASHER · 6 | 6 | cyl 7 × 0.55 | 0.55 | 0.2 | 63 × 36 × 21.0 | 46.1 | 1% |
| 2 | M5 WASHER · 1 mm · 9 | 9 | cyl 10 × 1 | 0.55 | 1.3 | 56 × 26 × 21.0 | 28.8 | 4% |
| 2 | M5 SPACER · 1 mm · 46 | 46 | cyl 10 × 1 | 0.55 | 6.6 | 50 × 26 × 21.0 | 25.8 | 25% |
| 2 | M5 LOCK · WASHER 2 | 2 | cyl 9.2 × 2.4 | 0.55 | 0.6 | 40 × 26 × 21.0 | 20.7 | 3% |
| 2 | M4 KNURLED · NUT 4 | 4 | cyl 14.08 × 8 | 0.58 | 8.6 | 59 × 26 × 21.0 | 30.6 | 28% |
| 3 | 6×3 MAGNET · 16 | 16 | cyl 6 × 3 | 0.60 | 2.3 | 66 × 62 × 21.0 | 83.5 | 3% |
| 3 | M3 T-NUT · HAMMER 75 | 75 | box 10.92 × 9.14 × 4.85 | 0.55 | 66.0 | 90 × 62 × 21.0 | 113.9 | 58% |
| 3 | M5 T-NUT · HAMMER 16 | 16 | box 11 × 9.2 × 5 | 0.55 | 14.7 | 50 × 62 × 21.0 | 62.7 | 23% |

Piece data and sources:

| BOM item | solid mm³ | envelope mm³ | solid/bulk | source |
|---|---:|---:|---:|---|
| Machine Screw, SHCS, M3x8 | 133 | 279 | 0.48 | ISO 4762 |
| Machine Screw, SHCS, M3x12 | 161 | 380 | 0.41 | ISO 4762 |
| Machine Screw, SHCS, M3x16 | 189 | 481 | 0.38 | ISO 4762 |
| Machine Screw, SHCS, M3x20 | 217 | 583 | 0.35 | ISO 4762 |
| Machine Screw, SHCS, M3x25 | 253 | 709 | 0.32 | ISO 4762 |
| Machine Screw, SHCS, M3x30 | 288 | 836 | 0.30 | ISO 4762 |
| Machine Screw, SHCS, M3x35 | 323 | 963 | 0.28 | ISO 4762 |
| Machine Screw, SHCS, M3x40 | 359 | 1090 | 0.27 | ISO 4762 |
| Machine Screw, SHCS, M3x50 | 429 | 1343 | 0.26 | ISO 4762 |
| Machine Screw, BHCS, M3x6 | 85 | 195 | 0.43 | ISO 7380 |
| Machine Screw, BHCS, M3x25 | 219 | 680 | 0.29 | ISO 7380 |
| Machine Screw, FHCS, M3x6 | 58 | 170 | 0.34 | ISO 10642 |
| Machine Screw, FHCS, M3x10 | 87 | 283 | 0.31 | ISO 10642 |
| Machine Screw, Wafer head, M3x25 | 252 | 1332 | 0.18 | EST (wafer head 8 × 1.5) |
| Machine Screw, Captive, M3x6 | 118 | 228 | 0.52 | EST (as ISO 4762 head) |
| Self-tapping Screw, M2x10 | 52 | 146 | 0.34 | ISO 14583 pan head; CAD 4.0 × 11.6 |
| Set Screw, M3x2, Pre-applied Threadlocker | 14 | 14 | 0.55 | ISO 4026 (d × L) |
| Machine Screw, SHCS, M5x40 | 1084 | 2687 | 0.36 | ISO 4762 |
| Machine Screw, BHCS, M4x6 | 175 | 372 | 0.47 | ISO 7380 |
| Machine Screw, BHCS, M5x6 | 313 | 620 | 0.50 | ISO 7380 |
| Machine Screw, BHCS, M5x10 | 391 | 904 | 0.43 | ISO 7380 |
| Machine Screw, BHCS, M5x14 | 470 | 1187 | 0.40 | ISO 7380 |
| Machine Screw, BHCS, M5x16 | 509 | 1329 | 0.38 | ISO 7380 |
| Machine Screw, BHCS, M5x30 | 784 | 2321 | 0.32 | ISO 7380 |
| Set Screw, M4x4, Pre-applied Threadlocker | 50 | 50 | 0.55 | ISO 4026 (d × L) |
| T-nut, Roll-in, 2020, M3 | 286 | 414 | 0.38 | CAD |
| T-nut, Roll-in, 2020, M5 | 272 | 430 | 0.35 | CAD |
| Hexnut, M3 | 46 | 76 | 0.35 | ISO 4032 s, m |
| Hexnut, M5 | 168 | 315 | 0.31 | ISO 4032 s, m |
| Heatset Insert, Brass, M3x5x4 | 62 | 90 | 0.38 | NAME; CAD knurl 5.35 |
| Washer, M3 | 17 | 21 | 0.45 | ISO 7089 |
| Washer, M5, 1mm | 59 | 79 | 0.41 | ISO 7089; NAME thickness |
| Precision Spacer, M5, 1mm | 59 | 79 | 0.41 | CAD (M5 1mm Shim 10 × 1) |
| Locking Washer, M5 | 56 | 160 | 0.19 | EST (DIN 127 split, twisted) |
| Knurled Nut, M4 | 747 | 1246 | 0.35 | CAD (DIN 466-B) |
| 6x3mm Neodymium Magnet | 85 | 85 | 0.60 | NAME; CAD |
| T-nut, Hammer Head, 2020, M3 | 185 | 484 | 0.21 | CAD |
| T-nut, Hammer Head, 2020, M5 | 190 | 506 | 0.21 | EST |

Not in a compartment: Teflon Tube (4mm OD 3mm ID) - 1.2m; Zip Ties, 3x150mm; Brass Heatset Insert tool (for M3 Brass Inserts); Drill bit, 2mm; Hex Wrench, 1.5mm; Hex Wrench, 2mm; Hex Wrench, 2.5mm; Hex Wrench, 3mm; Hex Wrench, 4mm; Slot head screwdriver, 2.5mm; Aluminium Handle.
<!-- END generated:layout -->

<!-- BEGIN generated:slice -->
| file | bin | time | g PLA | colour change Z | extents on the bed, mm | supports |
|---|---|---|---:|---:|---|---|
| `tray-A.3mf` | 5 × 4 × 5U | 5h 51m 3s | 211 | 33.40 | X 20.4–229.6, Y 26.4–193.6, Z ≤ 39.00 | none |
| `tray-B.3mf` | 5 × 4 × 5U | 4h 40m 25s | 172 | 33.40 | X 20.4–229.6, Y 26.4–193.6, Z ≤ 39.00 | none |
| `tray-C.3mf` | 5 × 4 × 4U | 4h 32m 18s | 164 | 26.40 | X 20.4–229.6, Y 26.4–193.6, Z ≤ 32.00 | none |

All trays: **15.1 h, 547 g**. PrusaSlicer 2.9.6 CLI estimates, one tray per bed, not GUI-arranged; 2 perimeters, 3 top / 3 bottom layers, 10% infill; 0 gap-fill extrusions; slicer stability notes: Long bridging extrusions (the base grooves and the floor's first layer over the feet's sparse infill, expected). The colour-change Z is the first label layer, checked against each G-code.
<!-- END generated:slice -->

## Credit and licence

Inspired by **r0bdawg11**, *INDX Upgrade Hardware Organizer*, <https://www.printables.com/model/1794124>
(CC BY): one flat tray, a compartment per hardware type, raised labels, a scoop fillet. Inspiration only;
no geometry is copied. The ultra-light construction takes its ideas from **HuMa**, *Gridfinity Ultra Light
Bins* (Printables 627719, CC BY-NC-SA); ideas only, no geometry used. The Gridfinity system is **Zack Freedman**'s; the base and lip here are built from
the published spec numbers, not from any Gridfinity model file.

Licence: **CC BY-NC-SA 4.0** (<https://creativecommons.org/licenses/by-nc-sa/4.0/>), the same as the rest of
this repository's own content (root `LICENSE`), which also matches what the Gridfinity design reference asks of
derived projects.
