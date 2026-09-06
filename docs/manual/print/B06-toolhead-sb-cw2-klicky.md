# Batch B06 — Toolhead: Stealthburner, Clockwork 2, Klicky

The Stealthburner and Clockwork 2 black parts and the Klicky probe set share one plate. The Klicky set is
printed here and **bagged as the alternative probe** — this build fits the inductive probe, and Ch 08 Step
08.54 is where the bag is set aside, unbuilt.

**Time:** 12.2 h (1 plate) — PrusaSlicer 2.9.6 estimates.

**Sessions:** 1 plate start (~5 min hands-on, 12.2 h unattended) + ~15 min inspect and bin.

**Prerequisites:** **Gate B passed** (Step B00.7, kit day — the hotend seat and the CW2 gear bores). B02 (SB
main body, faceplate, guidler, latch, latch shuttle, pcb spacer) and B04 feed the same assembly chapter and
are not print prerequisites; the toolhead chapter also needs `probe_retainer_bracket.stl` from B04, fitted
in Ch 07/08, not in a batch.

**Printed parts**


| STL | Repo path | Qty | Colour | g ea | Bin |
|---|---|---:|---|---:|---|
| `stealthburner_printhead_revo_voron_front.stl` | Stealthburner `STLs/Stealthburner/Printheads/revo_voron/` | 1 | Black | 40.6 | 08-SB |
| `stealthburner_printhead_revo_voron_rear_cw2.stl` | Stealthburner `STLs/Stealthburner/Printheads/revo_voron/` | 1 | Black | 15.0 | 08-SB |
| `[o]_stealthburner_LED_carrier.stl` | Stealthburner `STLs/Stealthburner/` | 1 | Black (opaque) | 0.9 | 08-SB |
| `[o]_stealthburner_LED_diffuser_mask.stl` | Stealthburner `STLs/Stealthburner/` | 1 | Black (opaque) | 0.3 | 08-SB |
| `main_body.stl` (Clockwork 2) | Stealthburner `STLs/Clockwork2/Direct_Drive/` | 1 | Black | 23.7 | 08-CW2 |
| `motor_plate.stl` (Clockwork 2) | Stealthburner `STLs/Clockwork2/Direct_Drive/` | 1 | Black | 14.1 | 08-CW2 |
| `cw2_captive_pcb_cover.stl` | Nitehawk-SB `STLs/` | 1 | Black | 10.9 | 08-CW2 |
| `KlickyProbe_v2.stl` | Klicky `Probes/KlickyProbe/STL/` | 2 *(1 + spare, per the mod's own advice)* | Black | 2.5 | spare-alt |
| `Probe_Dock_v2.1.stl` | Klicky `Probes/KlickyProbe/STL/` | 1 | Black | 3.1 | spare-alt |
| `Probe_magnet_holder.stl` | Klicky `Probes/KlickyProbe/STL/` | 1 | Black | 2.3 | spare-alt |
| `Probe_magnet_pressfit_helper.stl` | Klicky `Probes/KlickyProbe/STL/` | 1 | Black | 1.6 | spare-alt |
| `Probe_pressfit_holder.stl` | Klicky `Probes/KlickyProbe/STL/` | 1 | Black | 4.6 | spare-alt |
| `KlickyProbe_AB_mount_v2.stl` | Klicky `Printers/Voron/v1.8_v2.4_Legacy_Trident/v1.8_v2.4_Legacy_Trident_STL/` | 1 | Black | 4.4 | spare-alt |
| `KlickyProbe_AB_mount_v2_holder.stl` | Klicky (same folder) | 1 | Black | 1.6 | spare-alt |
| `Mount_magnet_holder.stl` | Klicky (same folder) | 1 | Black | 2.3 | spare-alt |
| `Mount_magnet_pressfit_helper.stl` | Klicky (same folder) | 1 | Black | 1.6 | spare-alt |
| `Mount_pressfit_holder_v2.stl` | Klicky (same folder) | 1 | Black | 6.6 | spare-alt |
| `Dock_mount_fixed_v2.stl` | Klicky (same folder) | 1 | Black | 22.7 | spare-alt |

**Do not print:** an ADXL mount (Nitehawk-SB has one on board); the CW2 chain anchor (kit supplies "CW2
Chain Anchor Tilted" printed).

**Hardware:** none.

**Read first**

- Checkpoint after B06: the Revo Voron heatsink (the glossary's *Revo HF* — same part, HF nozzle fitted) must
  sit flat in the printhead front with 4× M3×8. Klicky: **count and bag, do not build** — no magnets are
  pressed in this batch or anywhere else in this manual (Ch 08 Step 08.54).
- Most commonly reprinted here: `KlickyProbe_v2` — that's why two are printed, in case the option is ever taken up.
- Hotend file choice is settled: E3D Revo Voron → the `revo_voron` folder, `..._rear_cw2` for Clockwork 2.
- `cw2_captive_pcb_cover` is LDO's improved cable door (captive screw + external chamber thermistor); the
  stock alternative is `Clockwork2/cable_door_for_pcb.stl` if you'd rather use it.
- Klicky dock: **fixed** mount chosen for simplicity. If you later add the Decontaminator purge bucket, you
  need `Dock_sidemount_fixed_v2.stl` + `Dock_sidemount_left_v2.stl` instead (~25 g, 1.5 h) — not printed here.
- The `Probe_*_pressfit_helper` / `_holder` parts are jigs for pressing the 6×3 magnets in square. Print
  them and bag them with the set — if Klicky is ever built, a crooked magnet is a probe that doesn't repeat.

## Step B06.1 — Filament prep

**Do:** Galaxy Black, spool #3 after B05. Confirm ≥148 g remaining for the plate. Sheet per
[00-slicer-setup § Print sheet](00-slicer-setup.md#print-sheet).
**Check:** Clean purge.

Source: [print plan §4.3 — spool changes](../../voron-print-plan.md#43-spool-changes) · [00-slicer-setup § Drying](00-slicer-setup.md#drying) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B06.2 — Load plate B06-P1

![Plate B06-P1 — sorting diagram](../assets/plates/B06-P1.png)

*Sorting diagram, drawn from the committed project: every part numbered and filled in the colour of its bin, bin id on the part; the legend reads # · STL · bin (chapter · steps). Sort at Step B06.5.*

**Do:** Open `slicer/plates/B06-P1.3mf` with **File → Open Project**. Do not rebuild the arrangement.
Confirm the loaded objects match the Parts list and that the printhead files came from the `revo_voron`
folder.
**Parts:** 18 files, 19 objects, no brim in the project — 12.2 h, 148 g (PrusaSlicer 2.9.6 estimate);
`stealthburner_printhead_revo_voron_front`; `stealthburner_printhead_revo_voron_rear_cw2`;
`[o]_stealthburner_LED_carrier`; `[o]_stealthburner_LED_diffuser_mask`; `main_body` (CW2);
`motor_plate` (CW2); `cw2_captive_pcb_cover`; then the Klicky set — `KlickyProbe_v2` ×2;
`Probe_Dock_v2.1`; `Probe_magnet_holder`; `Probe_magnet_pressfit_helper`; `Probe_pressfit_holder`;
`KlickyProbe_AB_mount_v2`; `KlickyProbe_AB_mount_v2_holder`; `Mount_magnet_holder`;
`Mount_magnet_pressfit_helper`; `Mount_pressfit_holder_v2`; `Dock_mount_fixed_v2`.
**Check:** Printhead files confirmed from `revo_voron/`; the dock is the *fixed* variant; no brim outline in the preview.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [Stealthburner printhead README](https://github.com/VoronDesign/Voron-Stealthburner/blob/main/STLs/Stealthburner/Printheads/README.md)

## Step B06.3 — Print plate B06-P1

**Do:** Print with standing overrides.
**Check:** LED carrier, diffuser mask and magnet-holder pockets print crisp, the finest features on the plate.

Pause: ~5 min since the last pause — plate started; nothing to do until it finishes.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B06.4 — Inspect

**Do:**

1. Dry-fit the Revo Voron heatsink in the printhead front: flat, no rock, takes 4× M3×8.
2. Count the Klicky parts against the table: 12 pieces, magnet pockets clean.
3. Bag them unbuilt, press no magnets, label the bag `KLICKY — alternative probe only, see Ch 08.54`.
**Check:** Hotend sits flat, no rocking. Klicky bag closed, 12 pieces plus the spare `KlickyProbe_v2`, labelled.

Pause: ~10 min since the last pause — hotend dry-fitted and removed, Klicky bag closed. Nothing pressed, no magnets.

Source: [print plan §5.2 — checkpoint after each batch](../../voron-print-plan.md#52-checkpoint-after-each-batch) · [Ch 08 Step 08.54 — bag the Klicky set](../08-toolhead.md#step-0854-confirm-the-probe-decision-and-bag-the-klicky-set) · [Klicky — what to print](https://github.com/jlas1/Klicky-Probe/tree/main/Printers/Voron/v1.8_v2.4_Legacy_Trident)

## Step B06.5 — Sort into bins

**Do:**

1. Sort the plate off its diagram: number to legend, colour to bin, bin id on the part.
2. Print labels from the [bin-labels sheet](../../print/bin-labels.md).
3. The Klicky bag goes into **spare-alt** closed.

**B06-P1**

| bin | parts off this plate |
|---|---|
| **08-SB** — Stealthburner body, printhead, LEDs | `stealthburner_printhead_revo_voron_front`, `stealthburner_printhead_revo_voron_rear_cw2`, `[o]_stealthburner_LED_carrier`, `[o]_stealthburner_LED_diffuser_mask` |
| **08-CW2** — Clockwork 2 extruder + toolboard cover | `main_body`, `motor_plate`, `cw2_captive_pcb_cover` |
| **spare-alt** — Spares / alternates (not fitted) | `KlickyProbe_v2` ×2, `Probe_Dock_v2.1`, `Probe_magnet_holder`, `Probe_magnet_pressfit_helper`, `Probe_pressfit_holder`, `KlickyProbe_AB_mount_v2`, `KlickyProbe_AB_mount_v2_holder`, `Mount_magnet_holder`, `Mount_magnet_pressfit_helper`, `Mount_pressfit_holder_v2`, `Dock_mount_fixed_v2` |

**Check:** All toolhead parts in 08-SB / 08-CW2; the Klicky bag closed in spare-alt.

Source: [print plan §9 — batch summary](../../voron-print-plan.md#9-machine-readable-batch-summary) · [print plan §2 — which parts gate which step](../../voron-print-plan.md#2-which-parts-gate-the-frame-and-z-drive-steps) · [print/README § Bins](README.md#bins)

---

## Checkpoint B06
- [ ] Gate B passed before B06-P1 started
- [ ] Revo Voron heatsink sits flat in the printhead front, ready for 4× M3×8
- [ ] Klicky set counted (12 pieces incl. the spare `KlickyProbe_v2`), bagged in spare-alt, labelled "alternative probe only — Ch 08.54", no magnets pressed

## Common mistakes
- Slicing the wrong hotend printhead folder (not `revo_voron`).
- Building Klicky because the parts are on the bench — the kit's config, wiring and pre-terminated cable are all for the inductive probe (Ch 08.54).

## Next
Assembly: *Stealthburner* (p.146–147, then the separate Stealthburner manual). Printing: this is the last kit-day batch — if B07–B10 printed before the kit, all 22 plates are done; if not, continue with [B07 — Electronics bay + lighting](B07-electronics-bay-and-lighting.md).
