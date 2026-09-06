# Batch B09 — Panels, filtration, spool

**Time:** 21.8 h (5 plates) — PrusaSlicer 2.9.6 estimates.

**Sessions:** 5 plate starts (~5 min hands-on each, 3.9–4.9 h unattended) + ~15 min inspect and bin, plus the
panel-clip test on kit day.

**Prerequisites:** **Gate A** (re-passed after the Gen 2 upgrade, as for B08) and B08 — the pre-kit order runs
B08 → B09 → B10 back to back. No bearing seat here, so Gate B is not needed.

**Printed parts**


| STL | Repo path | Qty | Colour | g ea | Bin |
|---|---|---:|---|---:|---|
| `corner_panel_clip_4mm_x8.stl` | Voron-2 `STLs/Panel_Mounting/` | 8 | Black | 3.0 | 11-clips-4mm |
| `midspan_panel_clip_4mm_x7.stl` | Voron-2 `STLs/Panel_Mounting/` | 7 | Black | 2.0 | 11-clips-4mm |
| `corner_panel_clip_6mm_x8.stl` | Voron-2 `STLs/Panel_Mounting/` | 8 | Black | 4.5 | 11-clips-6mm |
| `midspan_panel_clip_6mm_x8.stl` | Voron-2 `STLs/Panel_Mounting/` | 8 | Black | 2.9 | 11-clips-6mm |
| `bottom_panel_clip_x4.stl` | Voron-2 `STLs/Panel_Mounting/` | 4 | Black | 3.2 | 11-panels |
| `bottom_panel_hinge_x2.stl` | Voron-2 `STLs/Panel_Mounting/` | 2 | Black | 4.3 | 11-panels |
| `z_belt_cover_a_x2.stl` | Voron-2 `STLs/Panel_Mounting/` | 2 | Black | 6.9 | 11-panels |
| `z_belt_cover_b_x2.stl` | Voron-2 `STLs/Panel_Mounting/` | 2 | Black | 6.9 | 11-panels |
| `exhaust_cover.stl` | LDOVoron2 `STLs/` | 1 | Black | 30.2 | 11-nevermore |
| `exhaust_filter_grill.stl` | Voron-2 `STLs/Exhaust_Filter/` | 1 | Black | 9.9 | 11-nevermore |
| `V2_Duo_Plenum.stl` | Nevermore_Micro `V5_Duo/V2/` | 1 | Black | 50.2 | 11-nevermore |
| `V2_Duo_Plenum_LID.stl` | Nevermore_Micro `V5_Duo/V2/` | 1 | Black | 12.3 | 11-nevermore |
| `Regular_Cartridge(contributed_by_Bucknova).3mf` | Nevermore_Micro `V5_Duo/V2/` | 1 | Black | 43.0 | 11-nevermore |
| `Regular_Cartridge_Lid(contributed_by_Bucknova).3mf` | Nevermore_Micro `V5_Duo/V2/` | 1 | Black | 8.4 | 11-nevermore |
| `spool_holder.stl` | Voron-2 `STLs/Spool_Management/` | 1 | Black | 16.6 | 11-spool |
| `bowden_retainer.stl` | Voron-2 `STLs/Spool_Management/` | 1 | Black | 5.6 | 11-spool |

⚠ **Panel-clip mapping is an inference, not a stated spec.** Back panel: 4 corner + 3 midspan → `_4mm_x8` /
`_4mm_x7`. Top panel: 4 corner + 4 midspan → also drawn from the `_4mm` set per the manual's illustrated
counts. Each side panel: 4 corner + 4 midspan → `_6mm_x8` / `_6mm_x8`. The arithmetic lands exactly, and
there is no committed plate that prints a single clip, so the test is at Step B09.12 **after** printing, on
kit day (it needs an extrusion, a panel offcut and the foam tape). The ways it fails: a clip too loose for
its panel-plus-tape → the panel rattles; too tight → it will not seat. Worst case a wrong guess costs one
4.3 h plate (56 g).

You are **not** building the Voron exhaust filter (76 g, 4.5 h saved). Use `exhaust_cover.stl` (LDO) +
`exhaust_filter_grill.stl` (Voron) to seal the back panel. Skip `exhaust_filter_housing`,
`[a]_exhaust_filter_mount_x2`, `[a]_filter_access_cover`, `[a]_exhaust_fan_grill`.

**Nevermore, exactly which files:** the plenum/lid are STLs; the cartridge and its lid are **3MF files** in
the same folder (PrusaSlicer imports them fine). Use the **Regular** cartridge, not XL — XL wants carbon
pellets and a faster/louder fan. 8× 6×3 mm magnets, 6× M3 heat-sets. The cartridge has a **built-in support
you push out**, not cut.

**Hardware:** none.

**Read first**

- Checkpoint after B09: Nevermore plenum lid must slide in its groove; cartridge must snap onto the plenum
  (both testable now). Panel clips: the 4 mm vs 6 mm test waits for kit day (Step B09.12).
- Brims already in the projects: 3 mm on `V2_Duo_Plenum` (P1), `Regular_Cartridge` and `exhaust_cover` (P2),
  `exhaust_filter_grill` (P3); none on the clip plates P4/P5. Verify the outline in the preview; never add one.
- Most commonly reprinted here: the 6 mm corner clips, if the foam tape choice changes.
- Back and top panels use 1 mm foam tape (3 mm panel + 1 mm tape = 4 mm); side panels use 3 mm foam tape
  (3+3 = 6 mm, "to prevent the gantry from rubbing on the panels").

## Step B09.1 — Filament prep

**Do:** Galaxy Black, confirm ≥297 g remaining across all five plates. Stage spool #2: #1 is predicted to
run out during **B09-P2** with ~60 g left when it starts, per the [ledger](README.md#spool-ledger). Sheet per
[00-slicer-setup § Print sheet](00-slicer-setup.md#print-sheet).
**Check:** Clean purge; spool #2 within reach for the runout-sensor pause.

Source: [print plan §4.3 — spool changes](../../voron-print-plan.md#43-spool-changes) · [00-slicer-setup § Drying](00-slicer-setup.md#drying) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B09.2 — Load plate B09-P1

![Plate B09-P1 — sorting diagram](../assets/plates/B09-P1.png)

*Sorting diagram, drawn from the committed project: every part numbered and filled in the colour of its bin, bin id on the part; the legend reads # · STL · bin (chapter · steps). Sort at Step B09.13.*

**Do:** Open `slicer/plates/B09-P1.3mf` with **File → Open Project**. The arrangement, brims and overrides
are already in it. Leave `V2_Duo_Plenum`'s built-in support in place.
**Parts:** `V2_Duo_Plenum`, 3 mm brim already in the project · `V2_Duo_Plenum_LID`, no brim · `Regular_Cartridge_Lid`, no brim — 4.5 h, 63 g (PrusaSlicer 2.9.6 estimate).
**Check:** Plenum's built-in support visible in preview, not suppressed; brim outline on the plenum only.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [Nevermore Micro README](https://github.com/nevermore3d/Nevermore_Micro) · [LDO Nevermore V5 Duo guide](https://ldomotion.com/guides/nevermore-v5-duo---v24)

## Step B09.3 — Print plate B09-P1

**Do:** Print with standing overrides.
**Check:** Plenum lid groove prints crisp.

Pause: ~5 min since the last pause — plate started; nothing to do until it finishes.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B09.4 — Load plate B09-P2

![Plate B09-P2 — sorting diagram](../assets/plates/B09-P2.png)

*Sorting diagram, drawn from the committed project: every part numbered and filled in the colour of its bin, bin id on the part; the legend reads # · STL · bin (chapter · steps). Sort at Step B09.13.*

**Do:** Open `slicer/plates/B09-P2.3mf` with **File → Open Project**. The arrangement, brims and overrides
are already in it. Leave the cartridge's built-in support in place.
**Parts:** `Regular_Cartridge` (3mf), 3 mm brim · `exhaust_cover`, 3 mm brim — 4.9 h, 67 g (PrusaSlicer 2.9.6 estimate) · both brims already in the project.
**Check:** Cartridge support intact in preview; brim outline shows on both.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [Nevermore Micro README](https://github.com/nevermore3d/Nevermore_Micro)

## Step B09.5 — Print plate B09-P2

**Do:** Print with standing overrides.
**Check:** All eight 6×3 mm cartridge magnet pockets print crisp.

Pause: ~5 min since the last pause — plate started; nothing to do until it finishes.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B09.6 — Load plate B09-P3

![Plate B09-P3 — sorting diagram](../assets/plates/B09-P3.png)

*Sorting diagram, drawn from the committed project: every part numbered and filled in the colour of its bin, bin id on the part; the legend reads # · STL · bin (chapter · steps). Sort at Step B09.13.*

**Do:** Open `slicer/plates/B09-P3.3mf` with **File → Open Project**. The arrangement, brims and overrides
are already in it. Confirm it loaded as described rather than rebuilding it.
**Parts:** `exhaust_filter_grill`, 3 mm brim already in the project · `spool_holder`, no brim · `bowden_retainer`, no brim · `z_belt_cover_a` ×2, no brim · `z_belt_cover_b` ×2, no brim · 5 files, 7 objects — 3.9 h, 55 g (PrusaSlicer 2.9.6 estimate).
**Check:** No face re-orientation; brim outline on the grill only.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [LDO Rev D printed-parts guide](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d)

## Step B09.7 — Print plate B09-P3

**Do:** Print with standing overrides.
**Check:** Clean first layer.

Pause: ~5 min since the last pause — plate started; nothing to do until it finishes.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B09.8 — Load plate B09-P4

![Plate B09-P4 — sorting diagram](../assets/plates/B09-P4.png)

*Sorting diagram, drawn from the committed project: every part numbered and filled in the colour of its bin, bin id on the part; the legend reads # · STL · bin (chapter · steps). Sort at Step B09.13.*

**Do:** Open `slicer/plates/B09-P4.3mf` with **File → Open Project**. The arrangement, brims and overrides
are already in it. Confirm it loaded as described rather than rebuilding it.
**Parts:** `corner_panel_clip_4mm` ×8 · `midspan_panel_clip_4mm` ×7 · `bottom_panel_hinge` ×2 · `bottom_panel_clip` ×4 · 4 files, 21 pieces — 4.2 h, 56 g (PrusaSlicer 2.9.6 estimate) · no brim in the project.
**Check:** Counts match: 8 corner, 7 midspan, 2 hinge, 4 bottom clips; no brim outline anywhere.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [print plan §6 — conditional / verify items](../../voron-print-plan.md#6-conditional-verify-items)

## Step B09.9 — Print plate B09-P4

**Do:** Print with standing overrides.
**Check:** Clean first layer.

Pause: ~5 min since the last pause — plate started; nothing to do until it finishes.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B09.10 — Load plate B09-P5

![Plate B09-P5 — sorting diagram](../assets/plates/B09-P5.png)

*Sorting diagram, drawn from the committed project: every part numbered and filled in the colour of its bin, bin id on the part; the legend reads # · STL · bin (chapter · steps). Sort at Step B09.13.*

**Do:** Open `slicer/plates/B09-P5.3mf` with **File → Open Project**. The arrangement, brims and overrides
are already in it. Confirm it loaded as described rather than rebuilding it.
**Parts:** `corner_panel_clip_6mm` ×8 · `midspan_panel_clip_6mm` ×8 · 2 files, 16 pieces — 4.3 h, 56 g (PrusaSlicer 2.9.6 estimate) · no brim in the project.
**Check:** Counts match: 8 corner, 8 midspan; no brim outline anywhere.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [print plan §6 — conditional / verify items](../../voron-print-plan.md#6-conditional-verify-items)

## Step B09.11 — Print plate B09-P5

**Do:** Print with standing overrides.
**Check:** Clean first layer.

Pause: ~5 min since the last pause — plate started; nothing to do until it finishes.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B09.12 — Inspect

**Do:**

1. Snap the brims off. Check the plenum lid slides and the cartridge snaps on.
2. On kit day, test a 4 mm and a 6 mm clip on an extrusion, 3 mm panel offcut plus foam tape.
**Check:** Plenum lid slides freely, cartridge snaps on positively, and each clip grips the panel-plus-tape
stack without rattling or jamming.

Pause: ~10 min since the last pause — Nevermore dry-fitted and apart again, brims off; the clip test is deferred to kit day and the clips are bagged by thickness.

Source: [print plan §5.2 — checkpoint after each batch](../../voron-print-plan.md#52-checkpoint-after-each-batch) · [00-slicer-setup § Calibration sequence](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) · [LDO Nevermore V5 Duo guide](https://ldomotion.com/guides/nevermore-v5-duo---v24)

## Step B09.13 — Sort into bins

**Do:** Sort off each plate diagram; the bin id is printed on every part. Labels: [bin-labels sheet](../../print/bin-labels.md). Bins: [README § Bins](README.md#bins). Keep the 4 mm and 6 mm clips in separate bins, each noted "test one on kit day before use".

**B09-P1**

| bin | parts off this plate |
|---|---|
| **11-nevermore** — Nevermore plenum + cartridge, exhaust cover + grill | `V2_Duo_Plenum`, `V2_Duo_Plenum_LID`, `Regular_Cartridge_Lid(contributed_by_Bucknova)` |

**B09-P2**

| bin | parts off this plate |
|---|---|
| **11-nevermore** — Nevermore plenum + cartridge, exhaust cover + grill | `Regular_Cartridge(contributed_by_Bucknova)`, `exhaust_cover` |

**B09-P3**

| bin | parts off this plate |
|---|---|
| **11-panels** — Bottom-panel clips/hinges, Z belt covers, handlebar spacers | `z_belt_cover_a` ×2, `z_belt_cover_b` ×2 |
| **11-nevermore** — Nevermore plenum + cartridge, exhaust cover + grill | `exhaust_filter_grill` |
| **11-spool** — Spool holder + bowden retainer | `spool_holder`, `bowden_retainer` |

**B09-P4**

| bin | parts off this plate |
|---|---|
| **11-panels** — Bottom-panel clips/hinges, Z belt covers, handlebar spacers | `bottom_panel_hinge` ×2, `bottom_panel_clip` ×4 |
| **11-clips-4mm** — Panel clips, 4 mm (back + top panels) | `corner_panel_clip_4mm` ×8, `midspan_panel_clip_4mm` ×7 |

**B09-P5**

| bin | parts off this plate |
|---|---|
| **11-clips-6mm** — Panel clips, 6 mm (side panels) | `corner_panel_clip_6mm` ×8, `midspan_panel_clip_6mm` ×8 |

**Check:** 31 panel clips counted: 15 in 11-clips-4mm, 16 in 11-clips-6mm; the Nevermore set complete in 11-nevermore.

Source: [print plan §9 — batch summary](../../voron-print-plan.md#9-machine-readable-batch-summary) · [print plan §2 — which parts gate which step](../../voron-print-plan.md#2-which-parts-gate-the-frame-and-z-drive-steps) · [print/README § Bins](README.md#bins)

---

## Checkpoint B09
- [ ] 4 mm vs 6 mm clip-to-panel mapping confirmed against real panel + foam tape stock (kit day, before Ch 11)
- [ ] Nevermore plenum lid slides freely in its groove
- [ ] Nevermore cartridge snaps positively onto the plenum
- [ ] Cartridge built-in support pushed out clean
- [ ] Exhaust sealed with `exhaust_cover` + `exhaust_filter_grill` only — no Voron exhaust-filter parts printed
- [ ] All 31 panel clips counted — 15 in 11-clips-4mm, 16 in 11-clips-6mm

## Common mistakes
- Fitting the clips in Ch 11 without the one-clip test against real panel and tape stock — a wrong thickness costs a 4.3 h plate, not the build.
- Confusing the Nevermore Regular and XL cartridge files.
- Cutting instead of pushing out the cartridge's built-in support.

## Next
Assembly: *Panels* (p.240–259) and the Nevermore install. Printing: [B10 — Clicky-Clack door](B10-clicky-clack-door.md).
