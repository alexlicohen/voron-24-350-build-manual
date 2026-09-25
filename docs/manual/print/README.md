# Print batches — overview

22 plates, **157.0 h**, **1813 g Galaxy Black + 279 g ASA Blue**. Every hour and gram on this page is a
**PrusaSlicer 2.9.6 estimate**, sliced from the committed project for that plate (`slicer/plates/*.3mf`) —
not a throughput model. Method and what these figures replaced:
[print plan §4.1](../../voron-print-plan.md#41-how-these-numbers-were-produced). Per-plate detail with the
previous figure beside each one, and the exact unrounded values, are in `slicer/estimates.csv`. Totals here are
sums of the rounded plate figures, so they can differ from that file's TOTAL rows by 0.1–0.2 h or a gram or two;
`python3 slicer/check_docs.py` re-checks every number on this page against it.

**B11**, the PETG V0 bay ducting, is a separate batch outside this run: 5 plates, 25.0 h, 348 g of Jet Black
PETG V0 on its own spool. None of its numbers are in the run's totals; it has its own table, run schedule
and ledger [at the end of this page](#b11-bay-ducting-petg-v0).

```mascot
pose: print
caption: Twenty two plates, start to finish. The printer works while the kit is still in transit.
```

**Print order.** The Voron kit is not expected before **late November 2026**, so the whole run goes down
first, in numeric batch order: pre-B00 checks on the current Gen 1 belts, then **B00 → B01 → B02 → … → B10**
— all 157.0 h, finished before the cartons land. **Gate A** (the cube, Step B00.5) releases the batches with no press fit;
**Gate B** (Step B00.7) releases the bearing-seat and bore batches and now runs *early*: the inserts come
from the KADRICK kit already on the bench and the bores are calipered against their STL nominals. Only the
bearing press and the MGN12 rail check wait for the kit, and the rail check gates nothing but a reprint of
the ASA `MGN12_rail_guide` (3 g, 20 min). The "print gate" column is the *print*
prerequisite; which assembly chapter consumes a batch is the "feeds" column, and the chapter-level
prerequisite lists live in [00-index.md](../00-index.md#chapters).

| batch | plates | hours | g black | g blue | feeds (assembly chapter) | print gate |
|---|---:|---:|---:|---:|---|---|
| [B00](B00-calibration-and-jigs.md) | 1 | 4.0 | 52 | 0 | Ch 00 (heat-set coupon, rail guides); Ch 02 / 05 (rail guides); Ch 04 (`pulley_jig`); B01 (one retainer) | — (it is the gate) |
| [B01](B01-z-drive-assemblies.md) | 2 | 22.8 | 301 | 0 | Ch 02 Z Drives and Idlers | **Gate B** (bore, inserts) |
| [B02](B02-accent-parts-orange.md) | 3 | 21.9 | 0 | 279 | accent for Ch 02, 04, 05, 06, 07, 08, 10, 11; `Handle` for B10 | Gate A |
| [B03](B03-ab-drive-units-and-front-idlers.md) | 1 | 8.5 | 119 | 0 | Ch 04 A/B Drives and Idlers | Gate B |
| [B04](B04-xy-joints-and-x-carriage.md) | 1 | 8.6 | 117 | 0 | Ch 05 Gantry | Gate B |
| [B05](B05-z-joints-and-z-chain.md) | 1 | 6.4 | 78 | 0 | Ch 06 Z joints; Ch 10 (chain anchor, guide) | Gate B |
| [B06](B06-toolhead-sb-cw2-klicky.md) | 1 | 12.1 | 148 | 0 | Ch 08 Stealthburner (Klicky set bagged, Ch 08.54) | Gate B |
| [B07](B07-electronics-bay-and-lighting.md) | 2 | 16.0 | 226 | 0 | Ch 09 Electronics bay; Ch 10 Wiring; Ch 11 (handlebar spacers) | Gate A |
| [B08](B08-skirts-and-front-modules.md) | 4 | 29.2 | 399 | 0 | Ch 11 Part A Skirts | Gate A — on Gen 1 GT2 belts, like every other plate in the run |
| [B09](B09-panels-filtration-spool.md) | 5 | 21.8 | 297 | 0 | Ch 11 Panels, Nevermore, spool | Gate A (after B08) |
| [B10](B10-clicky-clack-door.md) | 1 | 5.7 | 76 | 0 | Ch 11 Clicky-Clack door | Gate A (after B09) |
| **TOTAL** | **22** | **157.0** | **1813** | **279** | | |

All 22 diagrams on one page: [Plate plans](../../print/plate-plans.md).

**Filament margin:** Black 1813 g needed / 2400 g on hand → **587 g margin (32 %)**. Blue 279 g needed /
800 g on hand → **521 g margin (187 %)**. Setup and the full override table:
[00-slicer-setup.md](00-slicer-setup.md).

## Run schedule

All 22 plates in run order, at about two swaps a day: a plate of **7 h or more** starts in the evening and
runs overnight; anything shorter is a day plate, so two of them fit between breakfast and bedtime. The
longest plate in the build, B01-P1 at 15.2 h, is the exception — start it in the morning so its first layer
is watched, and let it run into the night. Spool column is the [ledger](#spool-ledger).

| # | plate | hours | colour | slot | spool |
|---:|---|---:|---|---|---|
| 1 | B00-P1 | 4.0 | black | day | #1 |
| 2 | B01-P1 | 15.2 | black | overnight (start in the morning) | #1 |
| 3 | B01-P2 | 7.6 | black | overnight | #1 |
| 4 | B02-P1 | 7.0 | blue | overnight | A1 |
| 5 | B02-P2 | 7.3 | blue | overnight | A1 |
| 6 | B02-P3 | 7.6 | blue | overnight | A1 |
| 7 | B03-P1 | 8.5 | black | overnight | #1 |
| 8 | B04-P1 | 8.6 | black | overnight | #1 |
| 9 | B05-P1 | 6.4 | black | day | #1 |
| 10 | B06-P1 | 12.1 | black | overnight | #2 (fresh) |
| 11 | B07-P1 | 7.9 | black | overnight | #2 |
| 12 | B07-P2 | 8.1 | black | overnight | #2 |
| 13 | B08-P1 | 6.3 | black | day | #2 |
| 14 | B08-P2 | 8.4 | black | overnight | #2 |
| 15 | B08-P3 | 9.5 | black | overnight | #2 |
| 16 | B08-P4 | 5.0 | black | day | #2 |
| 17 | B09-P1 | 4.5 | black | day | #2 → #3 |
| 18 | B09-P2 | 4.9 | black | day | #3 |
| 19 | B09-P3 | 3.9 | black | day | #3 |
| 20 | B09-P4 | 4.2 | black | day | #3 |
| 21 | B09-P5 | 4.3 | black | day | #3 |
| 22 | B10-P1 | 5.7 | black | day | #3 |

Twelve overnight plates and ten day plates, 157.0 h in all: about 16 printer-days, three to four weeks at
two swaps a day.

## Bins

Every printed part has **one bin** — the assembly chapter that fits it, split into sub-bins where a chapter is
part-heavy (the four Z corners, the A and B drive sides, the 4 mm and 6 mm panel clips, B11's bay ducts). The bin id is what
you write on the part and on the box; the plate diagram at the top of every Load step shows each part
numbered and filled in its bin's colour with the id on it, and each batch's *Sort into bins* step lists
bin → parts per plate.

**Mark the plate too.** As a plate is sorted, write its plate id and the date beside the bin id, on a
face that will not show once the part is fitted, with a fine paint marker — `B03-P1 2026-09-20`. A
reprinted part gets the new plate id with an **R** after it, plus the extrusion multiplier if that changed
— `B03-P1R 94.5%`. The [run schedule](#run-schedule) and the [spool ledger](#spool-ledger) are the lookup:
plate id → date, spool and slicer settings, so a part that fits badly next year can be traced to the run
that made it, and one bad run can be reprinted without guessing which parts came off it. The scheme lives in `slicer/bins.py` (the diagrams, the `bin` column in
`docs/manual/assets/parts/MANIFEST.csv`, the [bin labels](../../print/bin-labels.md) and the bin map are all
generated from it); `python3 slicer/check_docs.py` cross-checks this table, the batch chapters and the
manifest against it. Z corner map (Ch 02 Step 02.02): `_a` parts build Z0 (front-left) and Z2 (rear-right),
`_b` parts build Z1 (rear-left) and Z3 (front-right); a `_x2` file with an `_a` / `_b` hand puts one copy in
each of its two corners, a `_x4` file one in each corner.

27 bins, 271 printed pieces: 218 from the ASA run and 53 from B11.

| bin | label | chapter · steps | parts (qty) | from batches |
|---|---|---|---|---|
| **00-jigs** | Jigs and coupons | Ch 00 · 00.14–00.22 (rail guides again at 02.06, 05.11, 05.33; pulley jig at 04.24, 04.33; cube at 14.11) | `Voron_Design_Cube_v7`, `Heatset_Practice`, `MGN12_rail_guide` ×2, `MGN9_rail_guide` ×2, `pulley_jig` | B00 |
| **02-Z0** | Z0 corner (front-left, `_a` hand) | Ch 02 · 02.01–02.44 (drive 02.17–02.38, idler 02.39–02.43) | `z_drive_retainer_a`, `z_drive_main_a`, `z_motor_mount_a`, `z_tensioner_bracket_a`, `[a]_z_drive_baseplate_a`, `[a]_belt_tensioner_a`, `[a]_z_tensioner_9mm` | B00, B01, B02 |
| **02-Z1** | Z1 corner (rear-left, `_b` hand) | Ch 02 · 02.01–02.44 (drive 02.17–02.38, idler 02.39–02.43) | `z_drive_main_b`, `z_drive_retainer_b`, `z_motor_mount_b`, `z_tensioner_bracket_b`, `[a]_z_drive_baseplate_b`, `[a]_belt_tensioner_b`, `[a]_z_tensioner_9mm` | B01, B02 |
| **02-Z2** | Z2 corner (rear-right, `_a` hand) | Ch 02 · 02.01–02.44 (drive 02.17–02.38, idler 02.39–02.43) | `z_drive_main_a`, `z_drive_retainer_a`, `z_motor_mount_a`, `z_tensioner_bracket_a`, `[a]_z_drive_baseplate_a`, `[a]_belt_tensioner_a`, `[a]_z_tensioner_9mm` | B01, B02 |
| **02-Z3** | Z3 corner (front-right, `_b` hand) | Ch 02 · 02.01–02.44 (drive 02.17–02.38, idler 02.39–02.43) | `z_drive_main_b`, `z_drive_retainer_b`, `z_motor_mount_b`, `z_tensioner_bracket_b`, `[a]_z_drive_baseplate_b`, `[a]_belt_tensioner_b`, `[a]_z_tensioner_9mm` | B01, B02 |
| **02-deck** | Deck panel clips | Ch 02 · 02.11–02.15 (confirm thickness at 02.12) | `deck_support_3mm` ×8 | B01 |
| **04-A** | A drive unit + A (right) front idler | Ch 04 · 04.1–04.24 (A idler 04.6–04.9, A drive 04.20–04.24) | `[a]_tensioner_right`, `a_drive_frame_lower`, `a_drive_frame_upper`, `front_idler_right_lower`, `front_idler_right_upper` | B02, B03 |
| **04-B** | B drive unit + B (left) front idler | Ch 04 · 04.1–04.33 (B idler 04.13–04.16, B drive 04.29–04.33) | `[a]_tensioner_left`, `b_drive_frame_lower`, `b_drive_frame_upper`, `front_idler_left_lower`, `front_idler_left_upper` | B02, B03 |
| **05-XY** | XY joints, cable bridge, endstop pod | Ch 05 · 05.3, 05.25–05.38 (endstop pod fitted at 09.32–09.33) | `[a]_endstop_pod_D2F_switch`, `[a]_xy_joint_cable_bridge_2hole`, `XY_cable_chain_bridge-Igus-3mm_backer`, `xy_joint_left_lower_MGN12`, `xy_joint_left_upper_MGN12`, `xy_joint_right_lower_MGN12`, `xy_joint_right_upper_MGN12` | B02, B04 |
| **06-Z-joints** | Z joints, belt clips, rail stops | Ch 06 · 06.3–06.10, 06.26 (rail stops optional at 02.10) | `[a]_z_belt_clip_lower` ×4, `[a]_z_belt_clip_upper` ×4, `z_joint_lower` ×4, `z_joint_upper` ×4, `z_rail_stop` ×4 | B02, B05 |
| **07-X** | X carriage halves, probe bracket, cable cover | Ch 07 · 07.6–07.39 (staged at 05.45; probe 07.35; cover 07.39) | `[a]_cable_cover`, `x_frame_V2TR_MGN12_left`, `x_frame_V2TR_MGN12_right`, `probe_retainer_bracket` | B02, B04 |
| **08-SB** | Stealthburner body, printhead, LEDs | Ch 08 · 08.2–08.62 (printhead 08.28–08.30, LEDs 08.35–08.37, body 08.62) | `[a]_stealthburner_main_body`, `stealthburner_printhead_revo_voron_front`, `stealthburner_printhead_revo_voron_rear_cw2`, `[o]_stealthburner_LED_carrier`, `[o]_stealthburner_LED_diffuser_mask` | B02, B06 |
| **08-CW2** | Clockwork 2 extruder + toolboard cover | Ch 08 · 08.3–08.20 (cover 08.51) | `[a]_guidler_a`, `[a]_guidler_b`, `[a]_latch`, `[a]_latch_shuttle`, `main_body`, `motor_plate`, `cw2_captive_pcb_cover` | B02, B06 |
| **09-bay** | Electronics bay: inlet, WAGO, PSU, USB, DIN clips | Ch 09 · 09.7–09.25 (inlet 09.10–09.12, WAGO 09.13, PSU 09.15–09.16, USB 09.25) | `wago_221-415_mount_3by5`, `lrs_200_psu_bracket` ×2, `PSU_stabilizer_50mm`, `usb_adapter_mount_partial_cover`, `pcb_din_clip` ×3, `power_inlet_IECGS_1mm` | B07 |
| **09-ducts** | Bay ducts and lids, B11 | Ch 09 · 09.6, 09.36 (AC lids 10.80, DC lids 11.52; coupon from B11.4) | 52 duct, lid and coupon pieces, listed at [Step B11.8](B11-bay-ducting.md#step-b118-sort-into-bins) and [B11.14](B11-bay-ducting.md#step-b1114-sort-the-after-kit-plates-into-bins) | B11 |
| **10-chains** | Z cable chain anchor, guide, retainer | Ch 10 · 10.62–10.64 (inserts at 10.35) | `[a]_z_chain_retainer_bracket` ×2, `z_chain_bottom_anchor`, `z_chain_guide` | B02, B05 |
| **10-lights** | COB light-strip mounts | Ch 10 · 10.35–10.36 | `cob_light_strip_mount_100mm` ×6, `cob_light_strip_mount_50mm` ×2 | B07 |
| **10-wiring** | Bay wiring: AC strip fin (B11) | Ch 10 · 10.80, appended with the B11 bay ducting | `V2L_STRIP_FIN` | B11 |
| **11-skirts** | Skirt ring, keystone panel, TFT mount | Ch 11 · 11.1–11.17 (TFT 11.5–11.7, keystone 11.10, bestagon 11.19) | `[a]_faceplate`, `[a]_keystone_blank_insert` ×2, `ldo_bestagon_insert`, `rear_center_skirt_350`, `side_fan_support` ×2, `front_skirt_a_350`, `front_skirt_b_350`, `side_skirt_a_350` ×2, `side_skirt_b_350` ×2, `keystone_panel`, `mount` | B02, B08 |
| **11-fans** | Fan grills, retainers, belt guards | Ch 11 · 11.3, 11.9, 11.11, 11.16 | `[a]_fan_grill_a` ×2, `[a]_fan_grill_b` ×2, `[a]_fan_grill_retainer` ×2, `[a]_belt_guard_a` ×2, `[a]_belt_guard_b` ×2 | B02 |
| **11-panels** | Bottom-panel clips/hinges, Z belt covers, handlebar spacers | Ch 11 · 11.20–11.25, 11.60 | `handlebar_spacer` ×4, `z_belt_cover_a` ×2, `z_belt_cover_b` ×2, `bottom_panel_hinge` ×2, `bottom_panel_clip` ×4 | B07, B09 |
| **11-clips-4mm** | Panel clips, 4 mm (back + top panels) | Ch 11 · 11.53, 11.59 | `corner_panel_clip_4mm` ×8, `midspan_panel_clip_4mm` ×7 | B09 |
| **11-clips-6mm** | Panel clips, 6 mm (side panels) | Ch 11 · 11.57–11.58 | `corner_panel_clip_6mm` ×8, `midspan_panel_clip_6mm` ×8 | B09 |
| **11-nevermore** | Nevermore plenum + cartridge, exhaust cover + grill | Ch 11 · 11.26–11.40, 11.54 | `V2_Duo_Plenum`, `V2_Duo_Plenum_LID`, `Regular_Cartridge_Lid(contributed_by_Bucknova)`, `Regular_Cartridge(contributed_by_Bucknova)`, `exhaust_cover`, `exhaust_filter_grill` | B09 |
| **11-spool** | Spool holder + bowden retainer | Ch 11 · 11.42–11.43 | `spool_holder`, `bowden_retainer` | B09 |
| **11-door** | Clicky-Clack door | Ch 11 · 11.44–11.50, 11.62–11.64 | `Handle`, `Handle-Hinge_Bottom`, `Handle-Hinge_Top`, `Hinge-L-sleeve-2X` ×2, `Hinge-L-solid-2X` ×2, `Latch`, `Panel_Clip` | B02, B10 |
| **spare-alt** | Spares / alternates (not fitted) | — · not fitted (Klicky set bagged at 08.54) | `[a]_pcb_spacer`, `KlickyProbe_v2` ×2, `Probe_Dock_v2.1`, `Probe_magnet_holder`, `Probe_magnet_pressfit_helper`, `Probe_pressfit_holder`, `KlickyProbe_AB_mount_v2`, `KlickyProbe_AB_mount_v2_holder`, `Mount_magnet_holder`, `Mount_magnet_pressfit_helper`, `Mount_pressfit_holder_v2`, `Dock_mount_fixed_v2`, `usb_adapter_mount` | B02, B06, B07 |

**Re-arranged a plate in PrusaSlicer?** Save the project over `slicer/plates/<id>.3mf` and run
`python3 slicer/build_plates.py --from-3mf` — it re-slices the committed projects as they are (no re-packing),
refreshes `slicer/estimates.csv` and redraws every diagram from the 3MF, then `python3 slicer/check_docs.py`
tells you which numbers in the chapters need updating.

## Spool ledger

The margin above is a prediction. This table is where it gets checked. The *slicer g* column is the
prediction and it stands on its own; *actual g* is optional and wants a kitchen scale, if you own one —
weigh the spool before and after a plate and write the difference in. A plate that misses its slicer figure
by more than about 5 g means the flow is off, not that the estimate is wrong — check extrusion multiplier
before the next plate rather than after five more. Write each new spool's scale reading on its flange;
remaining = reading − (new reading − 800).

The accent spool is **Prusament ASA Blue** (Amazon, arrived 2026-09-12; exact colour name *(verify on the
spool)*), **superseded 2026-09-14**: the 800 g Prusament ASA Prusa Orange bought 2026-09-04 is now the spare,
and no plate in this build is printed in it.

Spool numbering: **#1 · #2 · #3** are the three 800 g Galaxy Black spools, **A1** the single 800 g accent
spool. *Remaining* is what should be left on the active spool once that plate is off the bed, if every
plate lands on its slicer number. Rows are in **print order** — numeric, B00 → B10, all before kit day.

**When to swap.** Never mid-plate on purpose — but a runout *during* a plate is fine on a part with no
bearing seat: the Core One+ runout sensor pauses, you load the next spool and it resumes. One runout is
predicted, on such a plate:

- **B09-P1** (Nevermore plenum, plenum lid, cartridge lid) — spool #2 has about 27 g left when it starts.

Four rules that override the ledger:

- **B01-P1 needs ≥ 201 g on the spool at start** (the ledger has it on a fresh spool #1 with 748 g — fine).
  If a reprint or an extra plate has pushed the active spool under ~230 g, start B01-P1 on a fresh one and
  re-derive the ledger from your weighings — a resume seam on a Z-drive body is not worth it.
- **B06-P1 starts spool #2** even though #1 still has ~133 g: the plate carries the Revo hotend seat and the
  Clockwork 2 gear bores, and a resume seam there is not worth 133 g. Keep the stub for a clip reprint.
- **B02-P1/P2/P3** run back to back on the one accent spool — two colour changes in the entire build, and
  that is the point ([print plan §4.3](../../voron-print-plan.md#43-spool-changes)).
- **B08-P4 starts with only ~27 g of cushion** on spool #2 (97 g for a 70 g plate). A runout there lands on a
  side skirt, where the seam shows. If #2 looks light or its flange reading says under ~90 g, start B08-P4 on
  #3; B09-P1 then runs whole on #3 and #2's stub is kept for clips.

| plate | slicer g | actual g (weigh) | spool # | remaining |
|---|---:|---:|---|---:|
| B00-P1 | 52 | | #1 | 748 |
| B01-P1 | 201 | | #1 | 547 |
| B01-P2 | 100 | | #1 | 447 |
| B02-P1 | 90 | | A1 | 710 |
| B02-P2 | 93 | | A1 | 617 |
| B02-P3 | 96 | | A1 | 521 |
| B03-P1 | 119 | | #1 | 328 |
| B04-P1 | 117 | | #1 | 211 |
| B05-P1 | 78 | | #1 | 133 |
| B06-P1 | 148 | | **#2 (fresh; #1's 133 g kept)** | 652 |
| B07-P1 | 102 | | #2 | 550 |
| B07-P2 | 124 | | #2 | 426 |
| B08-P1 | 99 | | #2 | 327 |
| B08-P2 | 108 | | #2 | 219 |
| B08-P3 | 122 | | #2 | 97 |
| B08-P4 | 70 | | #2 | 27 |
| B09-P1 | 63 | | **#2 → #3 mid-plate** | 764 |
| B09-P2 | 67 | | #3 | 697 |
| B09-P3 | 55 | | #3 | 642 |
| B09-P4 | 56 | | #3 | 586 |
| B09-P5 | 56 | | #3 | 530 |
| B10-P1 | 76 | | #3 | 454 |
| **TOTAL black** | **1813** | | 3 × 800 g | **587 g margin** (454 on #3 + 133 on #1) |
| **TOTAL blue** | **279** | | 1 × 800 g | **521 g margin** |

## When the printer stops

A plate that stops is almost always one of these five. Read the screen first, and keep hands out of the
chamber until the bed and nozzle have cooled: the nozzle runs at 265 °C and the bed at 110 °C. The helper
never reaches in.

| What you see | What to do |
|---|---|
| **"Filament runout during print, please insert new one"** | Normal: the sensor paused the plate. Follow the screen: it heats and walks you through the change. Load the next spool, check it extrudes clean, press **Continue**. A seam at that layer is fine on a part with no bearing seat; on a bearing-seat part, reprint it. Write the swap in the [ledger](#spool-ledger). |
| **The power went off** | Power Panic saved the plate. When power returns the printer offers to resume. First check every part is still stuck down: a long cut cools the bed and ASA lets go ("The heatbed cooled down during the power outage"). Stuck: resume and stay for 10 minutes. Loose: cancel and reprint the plate. Power Panic does not cover switching the printer off yourself. |
| **"The bed doesn't seem to be aligned properly. Run Z alignment procedure?"** before the plate starts | Cancel the print. Run **Control → Calibrations & Tests → Z alignment calibration**, press **Quit** when it asks, and start the plate again. Prompt again: brass-brush the hot nozzle clean, check nothing is under the sheet, and pass the [hot first-layer check](B00-calibration-and-jigs.md#before-b00-belt-and-hot-bed-checks) before the next plate. |
| **The nozzle taps the same spot over and over** while it probes | Usually ooze or dirt on the tip. Cancel, brass-brush the hot nozzle, wipe the sheet, start again. Still looping on a clean nozzle: stop the run until the cause is found; it is the printer, not the plate. |
| **Spaghetti, a part knocked loose, or a blob on the nozzle** | Stop the print from the knob menu. Let everything cool before you touch it, then clear the sheet. Plastic wrapped round the heater block: stop the run and ask Prusa support before the next plate; never pull on the wires. Reprint the whole plate: a part that stopped halfway is scrap, marked `R` per [Bins](#bins). |

A first layer that looks wrong is not in this table: stop it and fix the cause, as at
[Step B00.4](B00-calibration-and-jigs.md#step-b004-print), and see [troubleshooting](../15-troubleshooting.md) for
parts that print but measure wrong. Still stuck on the Core One+ itself: Prusa's 24/7 support chat, from
[help.prusa3d.com](https://help.prusa3d.com).

Sources: [Prusa KB — Filament runout #31829](https://help.prusa3d.com/article/filament-runout-31829-core-one-35829-core-one-l-17829-xl-26829-mk4s-13829-mk4-27829-mk3-9s-21829-mk3-9-28829-mk3-5s-23829-mk3-5-12829-mini_916077) ·
[Power Panic](https://help.prusa3d.com/article/power-panic_2092) ·
[Heatbed cooled during the outage #31808](https://help.prusa3d.com/article/the-heatbed-cooled-down-during-the-power-outage-31808-core-one-35808-core-one-l-26808-mk4s-27808-mk3-9s-28808-mk3-5s-13808-mk4-21808-mk3-9-23808-mk3-5-17808-xl_899380) ·
[Uneven bed #31111](https://help.prusa3d.com/article/uneven-bed-31111-core-one-35111-core-one-l-36111-core-one-indx_856294)

## B11 — bay ducting (PETG V0)

[B11](B11-bay-ducting.md) replaces LDO's five PVC wire ducts with two printed conduits, layout v3. It is
**outside the ASA run**: Prusament PETG V0 Jet Black on the textured sheet, sliced with
`slicer/bay-ducts-petg.ini`, not to Voron spec. Every hour and gram is a PrusaSlicer 2.9.6 estimate from
the committed projects, whose arrangements are still provisional until GUI QC. `check_docs.py` checks
this table, the run schedule and the ledger below against `slicer/estimates.csv`.

| group | plates | hours | g PETG V0 | feeds (assembly chapter) | print gate |
|---|---:|---:|---:|---|---|
| [B11](B11-bay-ducting.md) before kit | 3 | 11.9 | 173 | Ch 09 ducts; Ch 10 strip fin | none; the coupon, B11-P1, prints first |
| [B11](B11-bay-ducting.md) after the kit-day measurements | 2 | 13.1 | 175 | Ch 09 ducts | kit-day bay measurements; B11-P5 only if the gap is ≥ 25 mm and the coupon passed |
| **B11 total** | **5** | **25.0** | **348** | | |

**Filament:** 348 g needed from one 1 kg spool, **V1**, not yet bought → **652 g margin** if B11-P5 prints.

## B11 run schedule

Print whenever the Core One+ is free: all five are day plates. P1 to P3 need nothing measured; P4 and P5 wait
for the kit-day measurements. The # column carries on from the run schedule above.

| # | plate | hours | colour | slot | spool |
|---:|---|---:|---|---|---|
| 23 | B11-P1 | 0.4 | petg | day (the coupon, first) | V1 |
| 24 | B11-P2 | 6.9 | petg | day | V1 |
| 25 | B11-P3 | 4.6 | petg | day | V1 |
| 26 | B11-P4 | 6.3 | petg | day (after kit-day measurements) | V1 |
| 27 | B11-P5 | 6.8 | petg | day (only if gap ≥ 25 mm) | V1 |

## B11 spool ledger

Spool **V1** is one 1 kg Prusament PETG V0 Jet Black spool, not yet bought; weigh it the same way as the ASA
spools. Nothing else in the build prints from it.

| plate | slicer g | actual g (weigh) | spool # | remaining |
|---|---:|---:|---|---:|
| B11-P1 | 4 | | V1 | 996 |
| B11-P2 | 96 | | V1 | 900 |
| B11-P3 | 73 | | V1 | 827 |
| B11-P4 | 82 | | V1 | 745 |
| B11-P5 | 93 | | V1 | 652 |
| **TOTAL PETG V0** | **348** | | 1 × 1000 g | **652 g margin** |
