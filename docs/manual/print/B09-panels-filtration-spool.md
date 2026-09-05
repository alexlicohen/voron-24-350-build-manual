# Batch B09 — Panels, filtration, spool

**Time:** 19.1 h (5 plates).

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

**Do:** Galaxy Black, confirm ≥322 g remaining across all five plates.
**Check:** Clean purge.

## Step B09.2 — Load plate B09-P1

**Do:** Slice `V2_Duo_Plenum`, `V2_Duo_Plenum_LID`, `Regular_Cartridge_Lid`. Leave `V2_Duo_Plenum`'s
built-in support in place.
**Parts:** the three items above — 4.1 h, 71 g.
**Check:** Plenum's built-in support visible in preview, not suppressed.

## Step B09.3 — Print plate B09-P1

**Do:** Print with standing overrides.
**Check:** Plenum lid groove prints crisp.

## Step B09.4 — Load plate B09-P2

**Do:** Slice `Regular_Cartridge` (3mf) and `exhaust_cover`. Leave the cartridge's built-in support in
place; 3 mm brim on `exhaust_cover`.
**Parts:** the two items above — 4.3 h, 73 g.
**Check:** Cartridge support intact in preview; exhaust cover brim applied.

## Step B09.5 — Print plate B09-P2

**Do:** Print with standing overrides.
**Check:** Cartridge magnet pockets (8× 6×3 mm) print crisp.

## Step B09.6 — Load plate B09-P3

**Do:** Slice `exhaust_filter_grill`, `spool_holder`, `bowden_retainer`, `z_belt_cover_a` ×2,
`z_belt_cover_b` ×2.
**Parts:** the five files above — 3.5 h, 60 g.
**Check:** No rotation applied.

## Step B09.7 — Print plate B09-P3

**Do:** Print with standing overrides.
**Check:** Clean first layer.

## Step B09.8 — Load plate B09-P4

**Do:** Slice `corner_panel_clip_4mm` ×8, `midspan_panel_clip_4mm` ×7, `bottom_panel_hinge` ×2,
`bottom_panel_clip` ×4.
**Parts:** the four files above (21 pieces) — 3.6 h, 59 g.
**Check:** Counts match: 8 corner, 7 midspan, 2 hinge, 4 bottom clips.

## Step B09.9 — Print plate B09-P4

**Do:** Print with standing overrides.
**Check:** Clean first layer.

## Step B09.10 — Load plate B09-P5

**Do:** Slice `corner_panel_clip_6mm` ×8, `midspan_panel_clip_6mm` ×8.
**Parts:** the two files above (16 pieces) — 3.6 h, 59 g.
**Check:** Counts match: 8 corner, 8 midspan.

## Step B09.11 — Print plate B09-P5

**Do:** Print with standing overrides.
**Check:** Clean first layer.

## Step B09.12 — Inspect

**Do:** Before binning all 31 panel clips, snap one 4 mm and one 6 mm clip onto a spare extrusion with a
3 mm panel offcut and the corresponding foam tape thickness — confirm the mapping in the Read-first note.
Check the Nevermore plenum lid slides in its groove and the cartridge snaps onto the plenum.
**Check:** Both clip thicknesses confirmed against real panel/tape stock before final use. Plenum lid
slides freely; cartridge seats with a positive snap.

## Step B09.13 — Label and bin

**Do:** Bin for **Panels** and the Nevermore install. Keep 4 mm and 6 mm clips in clearly separated bags.
**Check:** 31 panel clips counted and separated by thickness; Nevermore assembly (plenum, lid, cartridge,
cartridge lid) bagged together; spool holder and bowden retainer bagged for **Spool Management**.

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
