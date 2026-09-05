# Batch B01 — Z drive assemblies

**Time:** 22.8 h (2 plates) — PrusaSlicer 2.9.6 estimates.

**Prerequisites:** B00 printed and the seven-item calibration gate passed. Note: fully completing the
*Z Drives and Idlers* assembly chapter also needs the accent parts from **B02** (`[a]_z_drive_baseplate_a/b`,
`[a]_belt_tensioner_a/b`, `[a]_z_tensioner_9mm_x4`) — plan §9 lists hard prerequisites `B00;B02` for that chapter.

**Printed parts**


| STL | Repo path | Qty | Colour | g ea |
|---|---|---:|---|---:|
| `z_drive_main_a_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | Black | 39.4 |
| `z_drive_main_b_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | Black | 39.4 |
| `z_drive_retainer_a_x2.stl` | Voron-2 `STLs/Z_Drive/` | 1 *(second copy; first was on B00)* | Black | 19.5 |
| `z_drive_retainer_b_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | Black | 19.5 |
| `z_motor_mount_a_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | Black | 11.9 |
| `z_motor_mount_b_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | Black | 11.9 |
| `z_tensioner_bracket_a_x2.stl` | Voron-2 `STLs/Z_Idlers/` | 2 | Black | 13.0 |
| `z_tensioner_bracket_b_x2.stl` | Voron-2 `STLs/Z_Idlers/` | 2 | Black | 13.0 |
| `deck_support_3mm_x8.stl` | Voron-2 `STLs/Panel_Mounting/` | 8 | Black | 1.1 |

⚠ **Deck-support thickness (verify):** LDO's Rev D printed-parts guide says "our kit ships with 4 mm deck
panels, use 4 mm deck support clips," but the Rev D 350 BOM lists the deck panel as **3 mm** acrylic (the
4 mm panel is the *bottom* panel). The size-specific BOM wins: print `deck_support_3mm_x8` ×8 now, and
measure the deck panel on arrival — if it measures 4 mm, reprint `deck_support_4mm_x8` (8 g, 30 min).

**Hardware:** none.

**Read first**

- Checkpoint after B01: 625-2RS (16 mm OD) press-fit into each `z_drive_main` and `z_drive_retainer` bearing
  seat — thumb pressure, no rocking. M3 heat-set bosses on the motor mounts: no bulge, insert flush. Check
  the 4 mm/3 mm deck-support call above.
- Most commonly reprinted here: `z_drive_main_*` — the largest single parts in the batch, most exposed to
  warp at the corners.
- Plate B01-P1 is the longest single plate in the whole build (15.2 h) — start it in the morning, not at bedtime.

## Step B01.1 — Filament prep

**Do:** Confirm Galaxy Black spool loaded, dried within the last 2 weeks or fresh. This batch alone is
301 g — check remaining spool weight before starting B01-P1.
**Check:** Spool has ≥201 g remaining for B01-P1 without a mid-plate runout (a resume seam on a Z-drive
body is not worth the risk — start P1 on a fresh spool if in doubt).

Source: [print plan §4.3 — spool changes](../../voron-print-plan.md#43-spool-changes) · [00-slicer-setup § Drying](00-slicer-setup.md#drying) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B01.2 — Load plate B01-P1

![Plate B01-P1](../assets/plates/B01-P1.png)

**Do:** Open `slicer/plates/B01-P1.3mf` (**File → Open Project**). The arrangement, the per-object brims and every override are already in the project — what follows is what it contains, so you can confirm it loaded right rather than rebuild it. On the plate: `z_drive_main_a` ×2, `z_drive_main_b` ×2, `z_drive_retainer_a` ×1, `z_drive_retainer_b` ×2
together on one plate, `0.20mm STRUCTURAL @COREONE 0.4` with the standing overrides. No brim needed (not on
the tall/narrow or long-flat lists). Do not rotate any part.
**Parts:** the six items above — 15.2 h, 201 g (PrusaSlicer 2.9.6 estimate).
**Check:** Estimated plate time is **15 h 13 m**; if far off, re-verify profile/overrides before committing an overnight print.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim)

## Step B01.3 — Pre-print checks

**Do:** Chamber preheated to ≥40 °C, sheet clean with IPA, spool confirmed dry.
**Check:** Chamber reads ≥40 °C before purge.

Source: [00-slicer-setup § Calibration sequence](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B01.4 — Print plate B01-P1

**Do:** Start overnight or during a full workday — this is the 15.2 h plate.
**Check:** First layer clean; no corner lift on the `z_drive_main` bodies partway through.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B01.5 — Load plate B01-P2

![Plate B01-P2](../assets/plates/B01-P2.png)

**Do:** Open `slicer/plates/B01-P2.3mf` (**File → Open Project**). The arrangement, the per-object brims and every override are already in the project — what follows is what it contains, so you can confirm it loaded right rather than rebuild it. On the plate: `z_motor_mount_a` ×2, `z_motor_mount_b` ×2, `z_tensioner_bracket_a` ×2, `z_tensioner_bracket_b` ×2,
`deck_support_3mm` ×8 together. `z_motor_mount_a/b` are 42.0 mm tall, borderline aspect — **add a brim only if
you see lift on this print** (per [00-slicer-setup.md](00-slicer-setup.md#orientation-brim)).
**Parts:** the five items above — 7.6 h, 100 g (PrusaSlicer 2.9.6 estimate).
**Check:** All 8 deck-support clips accounted for on the plate.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [LDO Rev D printed-parts guide](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d) · [LDO Rev D 350 BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)

## Step B01.6 — Print plate B01-P2

**Do:** Start after P1 is pulled and inspected.
**Check:** No warp at the corners of the motor mounts.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B01.7 — Inspect

**Do:** With calipers and thumb pressure: press a 625-2RS bearing (16 mm OD) into every `z_drive_main` and
`z_drive_retainer` bearing seat — should seat with thumb pressure, no rocking. Check M3 heat-set bosses on
the motor mounts sit flush with no bulge.
**Check:** All bearing seats pass; any that don't → reprint that part, don't proceed with a known-bad Z drive.

Source: [print plan §5.2 — checkpoint after each batch](../../voron-print-plan.md#52-checkpoint-after-each-batch) · [00-slicer-setup § Calibration sequence](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) · [Voron materials — shrinkage 100 %](https://docs.vorondesign.com/materials.html)

## Step B01.8 — Label and bin

**Do:** Bin by assembly chapter: everything on this batch feeds **Z Drives and Idlers**. Group per Z-axis
(4 identical sets): `z_drive_main_a` + `z_drive_main_b` + `z_drive_retainer_a` + `z_drive_retainer_b` +
`z_motor_mount_a` + `z_motor_mount_b` + `z_tensioner_bracket_a` + `z_tensioner_bracket_b`. Deck supports go
in a separate bag labelled "deck panel — verify thickness on arrival."
**Check:** Four matched Z-drive part sets, plus 8 deck supports, labelled and boxed.

Source: [print plan §9 — batch summary](../../voron-print-plan.md#9-machine-readable-batch-summary) · [print plan §2 — which parts gate which step](../../voron-print-plan.md#2-which-parts-gate-the-frame-and-z-drive-steps)

---

## Checkpoint B01
- [ ] 625-2RS bearing press-fit into all `z_drive_main_a/b` seats — thumb pressure, no rocking
- [ ] 625-2RS bearing press-fit into all `z_drive_retainer_a/b` seats — thumb pressure, no rocking
- [ ] M3 heat-set bosses on motor mounts: flush, no bulge
- [ ] Deck panel measured on arrival; correct deck-support thickness confirmed or reprinted
- [ ] No corner lift or delamination on any `z_drive_main` body
- [ ] Parts labelled and binned by Z-axis set

## Common mistakes
- Starting the 15.2 h P1 plate late in the day and having it finish unattended overnight with no chance to
  abort a bad first layer.
- Assuming the deck-support thickness without measuring the actual panel.
- Forcing a tight bearing seat with a press instead of reducing extrusion multiplier for the reprint.

## Next
Assembly: *Z Drives and Idlers* (fully unlocked once B02's accent parts also print). Printing: [B02 — Accent parts (orange)](B02-accent-parts-orange.md).
