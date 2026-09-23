# Fit report: four Printables mods on the LDO Voron 2.4 350 Rev D+ (2026-09-23)

Analysis only. Nothing in the repo was touched. Figures and slices are next to this file.

| Mod | Verdict |
|---|---|
| 502306 cable duct (CMD) | **Use with changes.** Use straight pieces only: no bridges, no 90° bridges, no PSU_Bracket-4D. The middle run fits only if the front rail moves ~5 mm forward; otherwise keep PVC there. |
| 505838 AC covers | **Wire-box lid: use with changes. Half-bridge cover: skip.** The inserts are multi-material geometry with zero clearance and do not press-fit as modelled. |
| 502345 wire guides | **Mostly skip.** Two 2-wire guides for the loose earth leads. The 90° rail-earth guides only if the DIN-rail earthing decision says "run PE to the rail". |
| 450348 handle | **Skip.** The bolted foot clashes with every panel edge. The kit already ships two aluminium handlebars for the same strip. |

## Sources and method

- Bay geometry was measured on LDO's `S0General_Placement.jpg` (`docs/manual/assets/remote/09-electronics-bay/bay-general-placement.jpg`). The photo was resampled to printer millimetres with the origin at the frame centre (px 957, 1043) at 3.25 px/mm; +y is the printer rear, +x the printer right. It is a **350**: the LRS-200-24 measures 218 × 115 mm at that scale (datasheet 215 × 115). Frame x reads ±235 mm.
  - **Known anomaly:** frame y reads only ±222 mm. Every absolute position below therefore carries ±6 %. Fit calls rest on local gaps (edge to edge within a few cm), where the error is ±1.5 mm.
  - The DIN-rail-only photo (`din-rails-and-wire-ducts.jpg`) is a different shot with slightly different duct positions. I did not use it for positions.
- Heights come from the Voron 2.4r2 STEP (the 250 machine; the relations hold for a 350):
  - deck face at 0;
  - DIN rail top 7.5 mm;
  - PSU body 22.5–52.5 mm above the deck;
  - controller PCB about 27–29 mm above the deck. That figure is the **Octopus bracket**; LDO's supplied Leviathan brackets were not measured (unverified).
- CMD geometry comes from sections and ray casts of the STLs (trimesh). Print orientation matches the author's Bambu 3MF: ducts and the wire box are flipped (base down), covers and inlays go as-is.
- Panel sizes are from Ch 11 (LDO 350 BOM): side and back 483 × 503, top 483 × 483.
  - The 350 frame is 510 wide and deep (verified from the 470 horizontals).
  - I assumed 530 tall (the vertical length scales by 50 per size; unverified). That gives a **13.5 mm inset from every outer frame edge**. The Voron CAD 250 shows the same ~13 mm inset.

## 1. Cable ducts (502306)

### CMD profile (measured)

- Base footprint 20.1 mm wide.
- The walls bulge to **24.4 mm** at 12.5 mm height.
- The lid is 24.1 mm wide. Installed height with the lid is **26.4 mm**.
- The PVC duct it would replace is 20 × 25 mm.
- Pieces butt-join; there is no interlock. Straight lengths are 82 / 142 / 154 mm.
- Bridge tunnels are **7.50 mm** below the base plane and about 36 mm long. That is 8.5 mm over the deck with 1 mm VHB: 1.0 mm over a bare 7.5 mm rail.
  - The M5 BHCS heads sit inside the hat, below the flanges.
  - **Not needed:** LDO's rails stop about 318 mm long (apparent). Both side runs pass outboard of the rail ends, so no duct crosses a rail.

### Clearances in the LDO bay (apparent mm)

| Run | Neighbours | Gap for a 24.4 mm duct | Call |
|---|---|---|---|
| Front | Leviathan header row −108, front Z motors y ≤ −175 at \|x\| > 150 | ~27 mm to the board | fits |
| Middle | Leviathan PCB edge −14 ↔ PSU edge +11 (PSU body starts 22.5 mm up; the duct with lid is 26.4 mm, so it cannot go under the PSU; the PCB at ~27 mm plus solder pins cannot overhang it) | **25–26.5 mm available vs 24.4 needed** | **does not fit reliably** |
| Rear | SSR tab +101, circle hole +139…+152 (x +7…+22), WAGO mount front ~+200, inlet +222, rear Z mounts x < −150 / > +175 at y ≥ +174 | 17 mm behind the duct, 6 mm in front | fits |
| Left | rail ends −148, Pi ports −110, frame −235 | 15 mm to the rail ends | fits |
| Right | PSU right end ~+189…+195 (top surface magnified), USB adapter +115…+148, frame +235 | shift outboard to x +197…+221 → ~14 mm to the frame | fits |

- The rear wire opening, the deck supports and the skirt line are not reached:
  - no duct lies within 14 mm of the frame;
  - skirts sit outside the frame footprint;
  - the bay is 78 mm deep against a 26.4 mm duct.
- The bed WAGO mount is **above** the deck: bed L is run "down through the deck opening" (Ch 10.14), and no LDO bay photo shows it. So it is not in the duct plane.

### Proposed layout

Figure: `fit-overlay-duct-layout.jpg`. Positions are apparent mm; confirm on the bench.

| Id | File | Qty | Colour | Position (x, y of footprint) | Carries |
|---|---|---|---|---|---|
| F1, F2 | `CMD_V3_1H_154mm_DUCT` + `CMD_V2_6B_154mm_DUCT_COVER` | 2 + 2 | black | x −146…+162, y −160…−136, long axis L-R | DC: front Z motors, Leviathan top headers |
| L1, L2 | same | 2 + 2 | black | x −188…−164, y −154…+154, F-B | DC: both left Z motors (the rear-left motor enters the L2 end, not the AC run) |
| R1, R2 | same | 2 + 2 | black | x +197…+221, y −154…+154, F-B | DC: right Z motors, umbilical to the USB adapter |
| B-DC | same | 1 + 1 | black | x +12…+166, y +158…+182 | DC: from the notch bundle rightward (umbilical, XY endstop, nozzle probe, bed TH, fans) |
| AC | `CMD_V3_1H_142mm_DUCT` + `CMD_V2_6B_142mm_DUCT_COVER` | 1 + 1 | **orange** | x −142…0, y +158…+182 | **AC only:** WAGO→PSU AC, WAGO L→SSR 2, SSR 1→bed L, bed N/PE→WAGO |
| AC caps | `CMD_Remix-V3_DUCT-1M_ENDCAP` (left end), `…_ENDCAP_SLOT` (notch end) | 1 + 1 | orange | ends of AC | keeps DC out of the AC run |
| M1, M2 | 154 duct + cover | 2 + 2 | black | x −146…+162, y −12…+12 | **only if** the bench gap Leviathan edge → PSU edge is **≥ 29 mm**; otherwise keep the PVC duct |
| Box (optional) | `CMD_V3_1H_WIRE_BOX` (+ lid, §2) | 1 | orange | x −106…−29, y +106…+154 | AC collector between the SSR / PSU AC terminals and the AC run |

- **Split at the rear notch.** The gap of about 12 mm at x 0…+12 sits under the harness drop. Bed L/N/PE turn left into AC, and everything else turns right. All mains then lives in the rear-left quadrant.
  - This is stricter than LDO's own bay, which mixes the mains with the Z-motor cables in one rear duct. It satisfies Ch 10.68's "mains group in its own duct run".
- **Middle run.** The cleanest fix is a rail move, not a STEP edit. Slide the **front** DIN rail about 5 mm toward the door: its T-nuts ride in the front-to-back bed extrusions, and Ch 09.5 does not fix the spacing.
  - That opens the gap to about 30 mm and still leaves ~22 mm between the front duct and the Leviathan header row.
  - Narrowing the CMD profile to 20 mm is a redesign of the bulged wall, not a simple edit. The STEP is a flat multi-body export with no history.
  - If you do not want to move the rail, keep the PVC middle duct.
- **Corners.** Leave gaps at the corners like LDO does. The Z-motor leads drop into the duct ends. `CMD_V3_1H_90DEG` / `T_*` would close the loop but are optional.
- **Not needed:** `*BRIDGE*` and `HALF_BRIDGE` (no rail crossings), and **`PSU_Bracket-4D`**. LDO skips the p.169 support bracket, and Ch 09.16 fits `PSU_stabilizer_50mm` only if the PSU rocks. The 4D bracket is a 67 mm arm that reaches over a duct placed behind the PSU in the stock layout. Here the PSU end sits ~40–46 mm from the frame with R1/R2 in that gap, so the geometry does not transfer.

## 2. AC caution covers (505838)

**Placement**

- **Half-bridge + hazard cover:** there is no place for it. No mains run crosses a DIN rail in this bay: the SSR LOAD and PSU AC terminals are all rearward of the rear rail. A half-bridge on flat deck is a 31.7 mm hump with a tunnel over nothing. Skip it.
- **Wire box + WARNING lid:** it fits as an optional AC collector (table above).
  - Depth 48.4 mm (base 44.1) in about 52–56 mm between the SSR tab and the AC run; right edge 6 mm left of the PSU terminal block. Bench-check that the gap is ≥ 52 mm.
  - It covers the leads, **not** the SSR / PSU terminal screws.

**Inlay geometry (measured).** Figures: `fit-inlay-warning-lid.png`, `fit-inlay-hazard-halfbridge.png`.

| | WARNING lid inlay | Hazard insert |
|---|---|---|
| Pieces | **19 separate islands** (letters + triangle + bolt) | 2 islands |
| Thickness | 0.60 mm | 0.60 mm |
| Pocket depth | 0.60 mm | 0.60 mm |
| Flush or proud | flush on the outer face | flush on the outer face |
| XY clearance per side | **0.000 mm**: the walls are coincident | 0.000 mm (0.9 mm² stray sliver) |
| Stroke width | mostly 0.8–1.2 mm (40 % of the area survives a 0.4 mm inset) | ~1 mm |

The author's 3MF puts lid and inlay in **one object, two extruders**: it is designed for multi-colour, not press-fit.

**Press-fit as modelled: no.** Zero clearance means it will not go in, and a 0.6 mm engagement holds nothing without glue.

**If Alex still wants separate inserts:**

- Print the insert object with **XY size compensation −0.10 mm** (~0.1 mm gap per side) and **elephant-foot compensation 0**. The ini's 0.2 would eat a third of a 1 mm stroke on the first of only three layers.
- Pick-and-place each piece and wick in thin CA or ASA/acetone slurry.
- Workable for the 2-piece hazard insert; tedious for the 19-piece WARNING text.

**Better options**

1. Wait for the INDX and print it as the author intended, with two tools.
2. Now, single extruder: make it proud text. Add the inlay as a part filling the pocket (black), plus a second copy raised 0.6 mm; print lid face-up with one `M600` at the lid's top height. The result is orange letters standing 0.6 mm proud.
3. Simplest: print the AC duct, AC cover and wire box in orange and use the plain `CMD_V2_6B_WIRE_BOX_COVER`. That is what the author did for AC runs.

## 3. Wire guides (502345)

- **Print now:** `WIRE_GUIDE_40MM_4F` ×2 (or `15MM`). They are for the two leads that run outside the ducts to a frame extrusion: the frame-PE ring (Ch 10.16) and the USB-adapter ESD lead (09.26). VHB on the deck, 2.5 mm ties.
- **Conditional:** `WIRE_GUIDE_90DEG_30MM_4F` / `_58MM_4F` hold a single earth lead with a tab under a DIN rail. Print one only if the open 00a.7 decision comes back "earth the rail with a PE conductor". That wiring is a mains change for the person who signs off the mains work.
  - The tab goes under the rail, so the rail's M5 screws have to be loosened. Check it does not tilt the rail (tab thickness not measured).
  - 30 vs 58 = the Y drop from the rail edge. For the SSR's rear rail toward the PE WAGO, the 58 mm version reaches further.
- **Skip:** `DIN_BRIDGE` (no lead crosses a rail), `50/75MM`, `90DEG_4F`.

## 4. Handle (450348)

**Frame.** The frame is 2020: the Voron STEP names every frame member `HFSB5-2020-*`, a Misumi 5-series 2020.

**Foot geometry (measured)**

- The bolted plate lies on one face and covers **18.0 mm** of it from the corner edge.
  - Ø4 hole with a Ø7 × 6.2 mm counterbore; the M3 axis is 10.2 mm from the edge, which is the slot centre.
  - An M3×12 protrudes 5.2 mm past the face, which is fine for a T-nut.
- The body on the adjacent face covers **12.3 mm** from the edge, plus a 5.5 mm hook into that face's slot.
- Hole spacing 164.8 mm, overall length 194.3 mm, ~30 mm finger clearance under the grip.
- **Bolts: 2 per handle** (1 per foot), not 4.

**Free faces on a closed 350.** No extrusion has two free adjacent faces. Every outer edge keeps a **13.5 mm strip on each face** (panel inset), and clips interrupt it:

- corner clips occupy ~35 mm from each corner;
- one midspan clip, ~35 mm long, sits at each edge centre.

| Location | Adjacent face (needs 12.3) | Bolted face (needs 18.0) | Result |
|---|---|---|---|
| Top **side** extrusions (L/R) | top: 13.5 free → 1.2 mm to the top panel edge ✓ | outer: side-panel edge 13.5 mm below the top; foot overlaps foam + PC by **4.5 × 6 mm** ✗ | clash along the whole length |
| Top **rear** | top ✓ | back panel (1 mm foam + 3 mm) same overlap ✗ | clash |
| Top **front** | top ✓ | Clicky-Clack door closes on the front face ✗ | blocks the door |
| Bottom extrusions | skirts on the bottom face ✗ | — | no |
| Verticals | 13.5/13.5 strips | — | geometrically closer, but a vertical handle is useless for lifting |

Figure: `fit-handle-foot-vs-panels.png`.

- **With changes it would fit.** Cut a 6.5 mm deep × 5.5 mm rebate on the lower inner edge of the plate (a PrusaSlicer negative-volume box) so it straddles the side-panel edge. The wall to the bolt hole drops to ~0.8 mm.
- Position: on each top side extrusion, centred front-to-back, straddling the midspan clip. Feet at 68–97 mm from the centre clear the clip at ±17.5 mm, and the grip clears the clip's 7 mm height.
- **But** the LDO kit already ships two aluminium handlebars on printed spacers in the top extrusions, "one per side" (Ch 11.60). That is the same strip and the same purpose, so **skip**.
- **T-nuts if used:** 4× M3 2020 for a pair, roll-in or hammerhead. They drop into the outer-face slot, which stays exposed above the panel edge, so they need **not** go in before the frame is closed. Avoid the clip T-nuts. The kit ships 135 roll-in + 75 hammerhead M3 (Ch 11); spares after all uses were not counted.

## 5. Slicing (PrusaSlicer 2.9.6 CLI, `slicer/voron-coreone-asa.ini`)

Voron spec: 0.20 mm, 4 perimeters, 5 top/bottom, 40 % grid.

| Plate | Contents | Time | g ASA |
|---|---|---|---|
| D1 black | 7× 154 duct | 12 h 49 m | 117.2 |
| D2 black | 2× 154 duct + 5× 154 cover | 5 h 35 m | 66.2 |
| D3 black | 4× 154 cover, WARNING lid, 2× guide 40 mm, 1× 90° 30 mm guide | 2 h 54 m | 44.4 |
| A1 orange | 142 duct + cover, wire box, WARNING inlay, 2 endcaps | 3 h 39 m | 38.8 |
| **Black total** | | **21 h 18 m** | **227.8** |
| **Orange total** | | **3 h 39 m** | **38.8** |
| H1 (reference only) | 2 handles | 8 h 00 m | 113.5 |

- **Per piece (derived):** 154 duct ≈ 16.7 g / 1 h 50 m; 154 cover ≈ 6.5 g / 23 m.
- **If the middle run stays PVC,** subtract 2 ducts + 2 covers: about 46.5 g and ~4 h 25 m.
- **In PETG,** the same toolpaths re-weighted at 1.27 g/cm³ (density swap, not a PETG-profile slice; no PETG time):
  - whole duct set (all four plates): **316.5 g** vs 266.7 g ASA;
  - black DC part: 270.4 g.
- Voron spec is overkill for ducts. A 2–3 perimeter, 15 % profile would roughly halve the time; not run.
- **Spool impact:**
  - Black-ASA margin (print/README) drops from 587 g to about 359 g.
  - Alternatives: the blue accent spool (521 g margin, and it matches the frame), or PETG, which the author used and which is fine in the bay.
  - The orange spare covers the AC parts.
- Outputs are in `slice/`: G-code per plate, `results.json`, and the `plates.py` that placed and sliced them.

## Open uncertainties (bench items)

1. Absolute photo metrology is ±6 % (the y-extent anomaly). Measure the Leviathan-edge → PSU-edge gap (the decision number for M1/M2: ≥ 29 mm) and the SSR-tab → rear-duct gap (wire box: ≥ 52 mm).
2. The Leviathan PCB height above the deck on LDO's brackets is unmeasured. If it is ≥ 30 mm, the CMD middle run could tuck under the board edge.
3. The handle / panel inset assumes a 530 mm frame height and foam cut flush with the panel. Measure panel edge → frame edge ≥ 13.5 mm.
4. The LDO handlebar foot positions are unknown.
5. The DIN earthing outcome (00a.7) is open; the 90° guides depend on it.
6. CMD tine strength in ASA is untested (the author used PETG; one ASA prototype is reported as "OK").
