# Print batches — overview

22 plates, **157.1 h**, **1812 g Galaxy Black + 279 g Prusa Orange**. Every hour and gram on this page is a
**PrusaSlicer 2.9.6 estimate**, sliced from the committed project for that plate (`slicer/plates/*.3mf`) —
not a throughput model. Method and what these figures replaced:
[print plan §4.1](../../voron-print-plan.md#41-how-these-numbers-were-produced). Per-plate detail with the
previous figure beside each one, and the exact unrounded values, are in `slicer/estimates.csv`;
`python3 slicer/check_docs.py` re-checks every number on this page against it.

**Print order.** Six batches need only **Gate A** (the cube, Step B00.5) and print before the kit arrives:
**B00 → B02 → B07 → (Gen 2 belt upgrade, cube re-passed) → B08 → B09 → B10** — 98.6 h. The five with
bearing seats and shaft bores need **Gate B** (Step B00.7: 625-2RS bore, MGN12 rail, real inserts) and start
the day the kit lands: **B01 → B03 → B04 → B05 → B06** — 58.5 h, printing under Ch 00–05. The "print gate"
column is the *print* prerequisite; which assembly chapter consumes a batch is the "feeds" column, and the
chapter-level prerequisite lists live in [00-index.md](../00-index.md#chapters).

| batch | plates | hours | g black | g orange | feeds (assembly chapter) | print gate |
|---|---:|---:|---:|---:|---|---|
| [B00](B00-calibration-and-jigs.md) | 1 | 4.0 | 52 | 0 | Ch 00 (heat-set coupon, rail guides); Ch 02 / 05 (rail guides); Ch 02 / 04 (`pulley_jig`); B01 (one retainer) | — (it is the gate) |
| [B02](B02-accent-parts-orange.md) | 3 | 21.9 | 0 | 279 | accent for Ch 02, 04, 05, 06, 07, 08, 10, 11; `Handle` for B10 | Gate A |
| [B07](B07-electronics-bay-and-lighting.md) | 2 | 16.0 | 226 | 0 | Ch 09 Electronics bay; Ch 10 Wiring; Ch 11 (handlebar spacers) | Gate A |
| [B08](B08-skirts-and-front-modules.md) | 4 | 29.2 | 398 | 0 | Ch 11 Part A Skirts | Gate A, re-passed after the Gen 2 upgrade |
| [B09](B09-panels-filtration-spool.md) | 5 | 21.8 | 297 | 0 | Ch 11 Panels, Nevermore, spool | Gate A (after B08) |
| [B10](B10-clicky-clack-door.md) | 1 | 5.7 | 76 | 0 | Ch 11 Clicky-Clack door | Gate A (after B09) |
| [B01](B01-z-drive-assemblies.md) | 2 | 22.8 | 301 | 0 | Ch 02 Z Drives and Idlers | **Gate B** (kit day) |
| [B03](B03-ab-drive-units-and-front-idlers.md) | 1 | 8.5 | 119 | 0 | Ch 04 A/B Drives and Idlers | Gate B |
| [B04](B04-xy-joints-and-x-carriage.md) | 1 | 8.6 | 117 | 0 | Ch 05 Gantry | Gate B |
| [B05](B05-z-joints-and-z-chain.md) | 1 | 6.4 | 78 | 0 | Ch 06 Z joints; Ch 10 (chain anchor, guide) | Gate B |
| [B06](B06-toolhead-sb-cw2-klicky.md) | 1 | 12.2 | 148 | 0 | Ch 08 Stealthburner (Klicky set bagged, Ch 08.54) | Gate B |
| **TOTAL** | **22** | **157.1** | **1812** | **279** | | |

All 22 diagrams on one page: [Plate plans](../../print/plate-plans.md).

**Filament margin:** Black 1812 g needed / 2400 g on hand → **588 g margin (32 %)**. Orange 279 g needed /
800 g on hand → **521 g margin (187 %)**. Setup and the full override table:
[00-slicer-setup.md](00-slicer-setup.md).

## Bins

Every printed part has **one bin** — the assembly chapter that fits it, split into sub-bins where a chapter is
part-heavy (the four Z corners, the A and B drive sides, the 4 mm and 6 mm panel clips). The bin id is what
you write on the part and on the box; the plate diagram at the top of every Load step shows each part
numbered and filled in its bin's colour with the id on it, and each batch's *Sort into bins* step lists
bin → parts per plate. The scheme lives in `slicer/bins.py` (the diagrams, the `bin` column in
`docs/manual/assets/parts/MANIFEST.csv`, the [bin labels](../../print/bin-labels.md) and the bin map are all
generated from it); `python3 slicer/check_docs.py` cross-checks this table, the batch chapters and the
manifest against it. Z corner map (Ch 02 Step 02.02): `_a` parts build Z0 (front-left) and Z2 (rear-right),
`_b` parts build Z1 (rear-left) and Z3 (front-right); a `_x2` file with an `_a` / `_b` hand puts one copy in
each of its two corners, a `_x4` file one in each corner.

25 bins, 218 printed pieces:

| bin | label | chapter · steps | parts (qty) | from batches |
|---|---|---|---|---|
| **00-jigs** | Jigs and coupons | Ch 00 · 00.14–00.22 (rail guides again at 02.06, 05.11, 05.33; pulley jig at 02.18, 04.24, 04.33; cube at 14.11) | `Voron_Design_Cube_v7`, `Heatset_Practice`, `MGN12_rail_guide` ×2, `MGN9_rail_guide` ×2, `pulley_jig` | B00 |
| **02-Z0** | Z0 corner (front-left, `_a` hand) | Ch 02 · 02.01–02.44 (drive 02.17–02.36, idler 02.37–02.43) | `z_drive_retainer_a`, `z_drive_main_a`, `z_motor_mount_a`, `z_tensioner_bracket_a`, `[a]_z_drive_baseplate_a`, `[a]_belt_tensioner_a`, `[a]_z_tensioner_9mm` | B00, B01, B02 |
| **02-Z1** | Z1 corner (rear-left, `_b` hand) | Ch 02 · 02.01–02.44 (drive 02.17–02.36, idler 02.37–02.43) | `z_drive_main_b`, `z_drive_retainer_b`, `z_motor_mount_b`, `z_tensioner_bracket_b`, `[a]_z_drive_baseplate_b`, `[a]_belt_tensioner_b`, `[a]_z_tensioner_9mm` | B01, B02 |
| **02-Z2** | Z2 corner (rear-right, `_a` hand) | Ch 02 · 02.01–02.44 (drive 02.17–02.36, idler 02.37–02.43) | `z_drive_main_a`, `z_drive_retainer_a`, `z_motor_mount_a`, `z_tensioner_bracket_a`, `[a]_z_drive_baseplate_a`, `[a]_belt_tensioner_a`, `[a]_z_tensioner_9mm` | B01, B02 |
| **02-Z3** | Z3 corner (front-right, `_b` hand) | Ch 02 · 02.01–02.44 (drive 02.17–02.36, idler 02.37–02.43) | `z_drive_main_b`, `z_drive_retainer_b`, `z_motor_mount_b`, `z_tensioner_bracket_b`, `[a]_z_drive_baseplate_b`, `[a]_belt_tensioner_b`, `[a]_z_tensioner_9mm` | B01, B02 |
| **02-deck** | Deck panel clips | Ch 02 · 02.11–02.15 (confirm thickness at 02.12) | `deck_support_3mm` ×8 | B01 |
| **04-A** | A drive unit + A (right) front idler | Ch 04 · 04.1–04.24 (A idler 04.6–04.9, A drive 04.20–04.24) | `[a]_tensioner_right`, `a_drive_frame_lower`, `a_drive_frame_upper`, `front_idler_right_lower`, `front_idler_right_upper` | B02, B03 |
| **04-B** | B drive unit + B (left) front idler | Ch 04 · 04.1–04.33 (B idler 04.13–04.16, B drive 04.29–04.33) | `[a]_tensioner_left`, `b_drive_frame_lower`, `b_drive_frame_upper`, `front_idler_left_lower`, `front_idler_left_upper` | B02, B03 |
| **05-XY** | XY joints, cable bridge, endstop pod | Ch 05 · 05.3, 05.25–05.38 (endstop pod fitted at 09.32–09.33) | `[a]_endstop_pod_D2F_switch`, `[a]_xy_joint_cable_bridge_2hole`, `XY_cable_chain_bridge-Igus-3mm_backer`, `xy_joint_left_lower_MGN12`, `xy_joint_left_upper_MGN12`, `xy_joint_right_lower_MGN12`, `xy_joint_right_upper_MGN12` | B02, B04 |
| **06-Z-joints** | Z joints, belt clips, rail stops | Ch 06 · 06.3–06.10, 06.26 (rail stops optional at 02.10) | `[a]_z_belt_clip_lower` ×4, `[a]_z_belt_clip_upper` ×4, `z_joint_lower` ×4, `z_joint_upper` ×4, `z_rail_stop` ×4 | B02, B05 |
| **07-X** | X carriage halves, probe bracket, cable cover | Ch 07 · 07.6–07.39 (staged at 05.45; probe 07.35; cover 07.39) | `[a]_cable_cover`, `x_frame_V2TR_MGN12_left`, `x_frame_V2TR_MGN12_right`, `probe_retainer_bracket` | B02, B04 |
| **08-SB** | Stealthburner body, printhead, LEDs | Ch 08 · 08.2–08.62 (printhead 08.28–08.30, LEDs 08.35–08.37, body 08.62) | `[a]_stealthburner_main_body`, `stealthburner_printhead_revo_voron_front`, `stealthburner_printhead_revo_voron_rear_cw2`, `[o]_stealthburner_LED_carrier`, `[o]_stealthburner_LED_diffuser_mask` | B02, B06 |
| **08-CW2** | Clockwork 2 extruder + toolboard cover | Ch 08 · 08.3–08.20 (cover 08.51) | `[a]_guidler_a`, `[a]_guidler_b`, `[a]_latch`, `[a]_latch_shuttle`, `main_body`, `motor_plate`, `cw2_captive_pcb_cover` | B02, B06 |
| **09-bay** | Electronics bay: inlet, WAGO, PSU, USB, DIN clips | Ch 09 · 09.7–09.25 (inlet 09.10–09.12, WAGO 09.13, PSU 09.15–09.16, USB 09.25) | `wago_221-415_mount_3by5`, `lrs_200_psu_bracket` ×2, `PSU_stabilizer_50mm`, `usb_adapter_mount_partial_cover`, `pcb_din_clip` ×3, `power_inlet_IECGS_1mm` | B07 |
| **10-chains** | Z cable chain anchor, guide, retainer | Ch 10 · 10.62–10.64 (inserts at 10.35) | `[a]_z_chain_retainer_bracket` ×2, `z_chain_bottom_anchor`, `z_chain_guide` | B02, B05 |
| **10-lights** | COB light-strip mounts | Ch 10 · 10.35–10.36 | `cob_light_strip_mount_100mm` ×6, `cob_light_strip_mount_50mm` ×2 | B07 |
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

The margin above is a prediction. This table is where it gets checked. **Weigh the spool before and after
each plate** and write the difference into *actual g*. A plate that misses its slicer figure by more than
about 5 g means the flow is off, not that the estimate is wrong — check extrusion multiplier before the next
plate rather than after five more.

Spool numbering: **#1 · #2 · #3** are the three 800 g Galaxy Black spools, **O1** the single 800 g Prusa
Orange. *Remaining* is what should be left on the active spool once that plate is off the bed, if every
plate lands on its slicer number. Rows are in **print order** — the six pre-kit batches, then the five
kit-day batches.

**When to swap.** Never mid-plate on purpose — but a runout *during* a plate is fine on a part with no
bearing seat: the Core One+ runout sensor pauses, you load the next spool and it resumes. One runout is
predicted, on such a plate:

- **B09-P2** (Nevermore cartridge, exhaust cover) — spool #1 has about 61 g left when it starts.

Two rules that override the ledger:

- **B01-P1 needs ≥ 201 g on the spool at start** (the ledger has it on spool #2 with ~551 g — fine). If a
  reprint or an extra plate has pushed the active spool under ~230 g, start B01-P1 on a fresh one and
  re-derive the ledger from your weighings — a resume seam on a Z-drive body is not worth it.
- **B05-P1 starts spool #3** even though #2 still has ~14 g: a resume seam on a Z joint's shaft bore is not
  worth 13 g. Keep the stub for a clip reprint.
- **B02-P1/P2/P3** run back to back on the one accent spool — two colour changes in the entire build, and
  that is the point ([print plan §4.3](../../voron-print-plan.md#43-spool-changes)).

| plate | slicer g | actual g (weigh) | spool # | remaining |
|---|---:|---:|---|---:|
| B00-P1 | 52 | | #1 | 748 |
| B02-P1 | 90 | | O1 | 710 |
| B02-P2 | 93 | | O1 | 617 |
| B02-P3 | 96 | | O1 | 521 |
| B07-P1 | 102 | | #1 | 646 |
| B07-P2 | 124 | | #1 | 522 |
| B08-P1 | 99 | | #1 | 423 |
| B08-P2 | 108 | | #1 | 315 |
| B08-P3 | 121 | | #1 | 194 |
| B08-P4 | 70 | | #1 | 124 |
| B09-P1 | 63 | | #1 | 61 |
| B09-P2 | 67 | | **#1 → #2 mid-plate** | 794 |
| B09-P3 | 55 | | #2 | 739 |
| B09-P4 | 56 | | #2 | 683 |
| B09-P5 | 56 | | #2 | 627 |
| B10-P1 | 76 | | #2 | 551 |
| *— kit day: Gate B —* | | | | |
| B01-P1 | 201 | | #2 | 350 |
| B01-P2 | 100 | | #2 | 250 |
| B03-P1 | 119 | | #2 | 131 |
| B04-P1 | 117 | | #2 | 14 |
| B05-P1 | 78 | | **#3 (fresh; #2's 14 g kept)** | 722 |
| B06-P1 | 148 | | #3 | 574 |
| **TOTAL black** | **1812** | | 3 × 800 g | **588 g margin** (574 on #3 + 14 on #2) |
| **TOTAL orange** | **279** | | 1 × 800 g | **521 g margin** |
