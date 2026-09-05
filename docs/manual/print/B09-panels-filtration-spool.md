# Batch B09 — Panels, filtration, spool

**Time:** 21.8 h (5 plates) — PrusaSlicer 2.9.6 estimates.

**Prerequisites:** B00, B08.

**Printed parts**


| STL | Repo path | Qty | Colour | g ea |
|---|---|---:|---|---:|
| `corner_panel_clip_4mm_x8.stl` | Voron-2 `STLs/Panel_Mounting/` | 8 | Black | 3.0 |
| `midspan_panel_clip_4mm_x7.stl` | Voron-2 `STLs/Panel_Mounting/` | 7 | Black | 2.0 |
| `corner_panel_clip_6mm_x8.stl` | Voron-2 `STLs/Panel_Mounting/` | 8 | Black | 4.5 |
| `midspan_panel_clip_6mm_x8.stl` | Voron-2 `STLs/Panel_Mounting/` | 8 | Black | 2.9 |
| `bottom_panel_clip_x4.stl` | Voron-2 `STLs/Panel_Mounting/` | 4 | Black | 3.2 |
| `bottom_panel_hinge_x2.stl` | Voron-2 `STLs/Panel_Mounting/` | 2 | Black | 4.3 |
| `z_belt_cover_a_x2.stl` | Voron-2 `STLs/Panel_Mounting/` | 2 | Black | 6.9 |
| `z_belt_cover_b_x2.stl` | Voron-2 `STLs/Panel_Mounting/` | 2 | Black | 6.9 |
| `exhaust_cover.stl` | LDOVoron2 `STLs/` | 1 | Black | 30.2 |
| `exhaust_filter_grill.stl` | Voron-2 `STLs/Exhaust_Filter/` | 1 | Black | 9.9 |
| `V2_Duo_Plenum.stl` | Nevermore_Micro `V5_Duo/V2/` | 1 | Black | 50.2 |
| `V2_Duo_Plenum_LID.stl` | Nevermore_Micro `V5_Duo/V2/` | 1 | Black | 12.3 |
| `Regular_Cartridge(contributed_by_Bucknova).3mf` | Nevermore_Micro `V5_Duo/V2/` | 1 | Black | 43.0 |
| `Regular_Cartridge_Lid(contributed_by_Bucknova).3mf` | Nevermore_Micro `V5_Duo/V2/` | 1 | Black | 8.4 |
| `spool_holder.stl` | Voron-2 `STLs/Spool_Management/` | 1 | Black | 16.6 |
| `bowden_retainer.stl` | Voron-2 `STLs/Spool_Management/` | 1 | Black | 5.6 |

⚠ **Panel-clip mapping is an inference, not a stated spec.** Back panel: 4 corner + 3 midspan → `_4mm_x8` /
`_4mm_x7`. Top panel: 4 corner + 4 midspan → also drawn from the `_4mm` set per the manual's illustrated
counts. Each side panel: 4 corner + 4 midspan → `_6mm_x8` / `_6mm_x8`. The arithmetic lands exactly, but
**snap one clip of each thickness onto an extrusion with a 3 mm panel offcut and the correct foam tape
before printing all 31.**

You are **not** building the Voron exhaust filter (76 g, 4.5 h saved). Use `exhaust_cover.stl` (LDO) +
`exhaust_filter_grill.stl` (Voron) to seal the back panel. Skip `exhaust_filter_housing`,
`[a]_exhaust_filter_mount_x2`, `[a]_filter_access_cover`, `[a]_exhaust_fan_grill`.

**Nevermore, exactly which files:** the plenum/lid are STLs; the cartridge and its lid are **3MF files** in
the same folder (PrusaSlicer imports them fine). Use the **Regular** cartridge, not XL — XL wants carbon
pellets and a faster/louder fan. 8× 6×3 mm magnets, 6× M3 heat-sets. The cartridge has a **built-in support
you push out**, not cut.

**Hardware:** none.

**Read first**

- Checkpoint after B09: panel clips — snap one onto an extrusion with a 3 mm offcut to confirm 4 mm vs 6 mm
  choice **before** printing all 31. Nevermore: plenum lid must slide in its groove; cartridge must snap
  onto the plenum.
- Most commonly reprinted here: the 6 mm corner clips, if the foam tape choice changes.
- Back and top panels use 1 mm foam tape (3 mm panel + 1 mm tape = 4 mm); side panels use 3 mm foam tape
  (3+3 = 6 mm, "to prevent the gantry from rubbing on the panels").

## Step B09.1 — Filament prep

**Do:** Galaxy Black, confirm ≥297 g remaining across all five plates. Spool #2 is expected to run out
during **B09-P3** (plan §4.3) — stage spool #3.
**Check:** Clean purge.

Source: [print plan §4.3 — spool changes](../../voron-print-plan.md#43-spool-changes) · [00-slicer-setup § Drying](00-slicer-setup.md#drying) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B09.2 — Load plate B09-P1

![Plate B09-P1](../assets/plates/B09-P1.png)

**Do:** Open `slicer/plates/B09-P1.3mf` (**File → Open Project**). The arrangement, the per-object brims and every override are already in the project — what follows is what it contains, so you can confirm it loaded right rather than rebuild it. On the plate: `V2_Duo_Plenum`, `V2_Duo_Plenum_LID`, `Regular_Cartridge_Lid`. Leave `V2_Duo_Plenum`'s
built-in support in place.
**Parts:** the three items above — 4.5 h, 63 g (PrusaSlicer 2.9.6 estimate).
**Check:** Plenum's built-in support visible in preview, not suppressed.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [Nevermore Micro README](https://github.com/nevermore3d/Nevermore_Micro) · [LDO Nevermore V5 Duo guide](https://ldomotion.com/guides/nevermore-v5-duo---v24)

## Step B09.3 — Print plate B09-P1

**Do:** Print with standing overrides.
**Check:** Plenum lid groove prints crisp.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B09.4 — Load plate B09-P2

![Plate B09-P2](../assets/plates/B09-P2.png)

**Do:** Open `slicer/plates/B09-P2.3mf` (**File → Open Project**). The arrangement, the per-object brims and every override are already in the project — what follows is what it contains, so you can confirm it loaded right rather than rebuild it. On the plate: `Regular_Cartridge` (3mf) and `exhaust_cover`. Leave the cartridge's built-in support in
place; 3 mm brim on `exhaust_cover`.
**Parts:** the two items above — 4.9 h, 67 g (PrusaSlicer 2.9.6 estimate).
**Check:** Cartridge support intact in preview; exhaust cover brim applied.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [Nevermore Micro README](https://github.com/nevermore3d/Nevermore_Micro)

## Step B09.5 — Print plate B09-P2

**Do:** Print with standing overrides.
**Check:** Cartridge magnet pockets (8× 6×3 mm) print crisp.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B09.6 — Load plate B09-P3

![Plate B09-P3](../assets/plates/B09-P3.png)

**Do:** Open `slicer/plates/B09-P3.3mf` (**File → Open Project**). The arrangement, the per-object brims and every override are already in the project — what follows is what it contains, so you can confirm it loaded right rather than rebuild it. On the plate: `exhaust_filter_grill`, `spool_holder`, `bowden_retainer`, `z_belt_cover_a` ×2,
`z_belt_cover_b` ×2.
**Parts:** the five files above — 3.9 h, 55 g (PrusaSlicer 2.9.6 estimate).
**Check:** No rotation applied.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [LDO Rev D printed-parts guide](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d)

## Step B09.7 — Print plate B09-P3

**Do:** Print with standing overrides.
**Check:** Clean first layer.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B09.8 — Load plate B09-P4

![Plate B09-P4](../assets/plates/B09-P4.png)

**Do:** Open `slicer/plates/B09-P4.3mf` (**File → Open Project**). The arrangement, the per-object brims and every override are already in the project — what follows is what it contains, so you can confirm it loaded right rather than rebuild it. On the plate: `corner_panel_clip_4mm` ×8, `midspan_panel_clip_4mm` ×7, `bottom_panel_hinge` ×2,
`bottom_panel_clip` ×4.
**Parts:** the four files above (21 pieces) — 4.2 h, 56 g (PrusaSlicer 2.9.6 estimate).
**Check:** Counts match: 8 corner, 7 midspan, 2 hinge, 4 bottom clips.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [print plan §6 — conditional / verify items](../../voron-print-plan.md#6-conditional-verify-items)

## Step B09.9 — Print plate B09-P4

**Do:** Print with standing overrides.
**Check:** Clean first layer.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B09.10 — Load plate B09-P5

![Plate B09-P5](../assets/plates/B09-P5.png)

**Do:** Open `slicer/plates/B09-P5.3mf` (**File → Open Project**). The arrangement, the per-object brims and every override are already in the project — what follows is what it contains, so you can confirm it loaded right rather than rebuild it. On the plate: `corner_panel_clip_6mm` ×8, `midspan_panel_clip_6mm` ×8.
**Parts:** the two files above (16 pieces) — 4.3 h, 56 g (PrusaSlicer 2.9.6 estimate).
**Check:** Counts match: 8 corner, 8 midspan.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [print plan §6 — conditional / verify items](../../voron-print-plan.md#6-conditional-verify-items)

## Step B09.11 — Print plate B09-P5

**Do:** Print with standing overrides.
**Check:** Clean first layer.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B09.12 — Inspect

**Do:** Before binning all 31 panel clips, snap one 4 mm and one 6 mm clip onto a spare extrusion with a
3 mm panel offcut and the corresponding foam tape thickness — confirm the mapping in the Read-first note.
Check the Nevermore plenum lid slides in its groove and the cartridge snaps onto the plenum.
**Check:** Both clip thicknesses confirmed against real panel/tape stock before final use. Plenum lid
slides freely; cartridge seats with a positive snap.

Source: [print plan §5.2 — checkpoint after each batch](../../voron-print-plan.md#52-checkpoint-after-each-batch) · [00-slicer-setup § Calibration sequence](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) · [LDO Nevermore V5 Duo guide](https://ldomotion.com/guides/nevermore-v5-duo---v24)

## Step B09.13 — Label and bin

**Do:** Bin for **Panels** and the Nevermore install. Keep 4 mm and 6 mm clips in clearly separated bags.
**Check:** 31 panel clips counted and separated by thickness; Nevermore assembly (plenum, lid, cartridge,
cartridge lid) bagged together; spool holder and bowden retainer bagged for **Spool Management**.

Source: [print plan §9 — batch summary](../../voron-print-plan.md#9-machine-readable-batch-summary) · [print plan §2 — which parts gate which step](../../voron-print-plan.md#2-which-parts-gate-the-frame-and-z-drive-steps)

---

## Checkpoint B09
- [ ] 4 mm vs 6 mm clip-to-panel mapping confirmed against real panel + foam tape stock
- [ ] Nevermore plenum lid slides freely in its groove
- [ ] Nevermore cartridge snaps positively onto the plenum
- [ ] Cartridge built-in support pushed out clean
- [ ] Exhaust sealed with `exhaust_cover` + `exhaust_filter_grill` only — no Voron exhaust-filter parts printed
- [ ] All 31 panel clips counted and bagged by thickness

## Common mistakes
- Printing all 31 clips before test-fitting the 4 mm/6 mm mapping against real panel stock.
- Confusing the Nevermore Regular and XL cartridge files.
- Cutting instead of pushing out the cartridge's built-in support.

## Next
Assembly: *Panels* (p.240–259) and the Nevermore install. Printing: [B10 — Clicky-Clack door](B10-clicky-clack-door.md).
