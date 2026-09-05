# Batch B08 — Skirts and front modules

**These are the parts people see.** Print them after the Gen 2 belt upgrade if it's in hand (see
[00-slicer-setup.md](00-slicer-setup.md#gen-2-belt-upgrade-pause-rule)) — 6 of the 26 plates in this batch
are large flat vertical faces, exactly where GT1.5's reduced VFA shows.

**Time:** 25.5 h (6 plates).

**Prerequisites:** B00, B02 (accent belt guards, fan grills, faceplate feed the same visible assembly), B07,
and **the Gen 2 belt-upgrade pause point** if the kit is on hand — re-run the calibration-cube gate first.

The skirt ring is made of nine segments plus three "module" segments sharing the same 67×20 mm
cross-section. On the 350: front = `front_skirt_a` + TFT mount + `front_skirt_b`; rear = `rear_center_skirt`
+ `power_inlet` + `keystone_panel`; each side = `side_skirt_a` + `side_fan_support` + `side_skirt_b`.

**Printed parts**

| STL | Repo path | Qty | Colour | g ea |
|---|---|---:|---|---:|
| `rear_center_skirt_350.stl` | Voron-2 `STLs/Skirts/350/` | 1 | Black | 71.9 |
| `front_skirt_a_350.stl` | Voron-2 `STLs/Skirts/350/` | 1 | Black | 41.4 |
| `front_skirt_b_350.stl` | Voron-2 `STLs/Skirts/350/` | 1 | Black | 41.4 |
| `side_skirt_a_350_x2.stl` | Voron-2 `STLs/Skirts/350/` | 2 | Black | 36.9 |
| `side_skirt_b_350_x2.stl` | Voron-2 `STLs/Skirts/350/` | 2 | Black | 36.9 |
| `side_fan_support_x2.STL` | Voron-2 `STLs/Skirts/` | 2 | Black | 33.0 |
| `keystone_panel.stl` | Voron-2 `STLs/Skirts/` | 1 | Black | 38.6 |
| `mount.stl` (BTT Pi TFT4.3) | LDOVoronTrident `STLs/BTT Pi TFT4.3 Mount/` | 1 | Black | 30.1 |

`power_inlet_IECGS_1mm` moved to [B07](B07-electronics-bay-and-lighting.md) — it's consumed in Ch 09, not the skirts chapter.

⚠ **`mount.stl` vs `mount_thick.stl`:** `mount.stl` is 30 g / 44.8 mm tall; `mount_thick.stl` is 74 g /
67.8 mm and gives access to the screen's brightness buttons with a pointy tool. `mount.stl` is the
recommendation — swap if you find you want the buttons **(judgment; LDO links the folder, not a specific file)**.

**Do not print:** `mini12864_case_front/rear`, `[a]_mini12864_case_hinge`, `[a]_mini12864_case_front_insert`,
`[a]_btt_knob_light_shield` — the touchscreen mount replaces that whole front module.

**Hardware:** none.

**Read first**
- Checkpoint after B08: lay every skirt segment on a flat reference (granite counter) and check for
  rocking. A bowed skirt is the most visible defect on a finished Voron. Dry-fit the ring: front + TFT
  mount + front, rear + inlet + keystone, sides + fan supports.
- Most commonly reprinted here: `rear_center_skirt_350` (182 mm — the worst warp candidate in the set).
- Only two of these long parts fit per plate — every one is 118–182 mm on its long axis and 67 mm deep, so
  a 250×220 bed takes two per plate with a workable gap.
- **3 mm brim** required on: `rear_center_skirt_350`, `front_skirt_a/b_350`, `side_skirt_a/b_350`,
  `side_fan_support`, `keystone_panel` (per [00-slicer-setup.md](00-slicer-setup.md#orientation-brim)).
- Optional, not printed here: `[a]_fan_grill_open_optional_x2` (more airflow, less filtering) instead of
  `[a]_fan_grill_a/b`; extra `ldo_bestagon_insert`s.

## Step B08.1 — Filament prep

**Do:** Galaxy Black. Spool #2 is expected to run out inside this batch or B09 (per plan §4.3) — stage a
fresh spool.
**Check:** Confirm spool weight before starting the 6.1 h P1 plate.

## Step B08.2 — Load plate B08-P1

**Do:** Slice `rear_center_skirt_350`, `side_fan_support` ×1. Apply 3 mm brim to both.
**Parts:** the two items above — 6.1 h, 105 g.
**Check:** Brim applied; parts not rotated.

## Step B08.3 — Print plate B08-P1

**Do:** Print with standing overrides.
**Check:** Watch the ends of `rear_center_skirt_350` for the first hour — 182 mm is the worst warp candidate in the set.

## Step B08.4 — Load plate B08-P2

**Do:** Slice `side_fan_support` ×1, `front_skirt_a_350`. 3 mm brim on both.
**Parts:** the two items above — 4.3 h, 74 g.
**Check:** Brim applied.

## Step B08.5 — Print plate B08-P2

**Do:** Print with standing overrides.
**Check:** Front skirt's built-in support intact, not suppressed in slicer.

## Step B08.6 — Load plate B08-P3

**Do:** Slice `front_skirt_b_350`, `side_skirt_a_350` ×1. 3 mm brim on both.
**Parts:** the two items above — 4.6 h, 78 g.
**Check:** Brim applied.

## Step B08.7 — Print plate B08-P3

**Do:** Print with standing overrides.
**Check:** No corner lift.

## Step B08.8 — Load plate B08-P4

**Do:** Slice `side_skirt_a_350` ×1, `side_skirt_b_350` ×1. 3 mm brim on both.
**Parts:** the two items above — 4.3 h, 74 g.
**Check:** Brim applied.

## Step B08.9 — Print plate B08-P4

**Do:** Print with standing overrides.
**Check:** No corner lift.

## Step B08.10 — Load plate B08-P5

**Do:** Slice `side_skirt_b_350` ×1, `keystone_panel`. 3 mm brim on both.
**Parts:** the two items above — 4.4 h, 76 g.
**Check:** Brim applied.

## Step B08.11 — Print plate B08-P5

**Do:** Print with standing overrides.
**Check:** Keystone panel's two cutout slots print crisp and undistorted.

## Step B08.12 — Load plate B08-P6

**Do:** Slice `mount.stl` (no brim — under the tall/narrow list but fine per the orientation table).
`power_inlet_IECGS_1mm` moved to B07 (Ch 09, not the skirts chapter) — see B07.4.
**Parts:** `mount.stl` — 1.8 h, 30 g.
**Check:** Confirm `mount.stl`, not `mount_thick.stl`, unless the button-access swap was chosen.

## Step B08.13 — Print plate B08-P6

**Do:** Print with standing overrides.
**Check:** Clean first layer, no warp on the tall/narrow mount.

## Step B08.14 — Inspect

**Do:** Lay every skirt segment from all six plates on the flat granite reference; check each for rocking.
Dry-fit the full ring: front `front_skirt_a` + TFT `mount` + `front_skirt_b`; rear `rear_center_skirt` +
`power_inlet` (from B07) + `keystone_panel`; each side `side_skirt_a` + `side_fan_support` + `side_skirt_b`.
**Check:** No rocking on any segment. Ring dry-fits with consistent gaps at every joint.

## Step B08.15 — Label and bin

**Do:** Bin by consuming assembly chapter — everything here plus B02's accent belt guards, fan grills/retainers,
keystone insert(s), faceplate, and bestagon insert go to **Skirts**. `power_inlet_IECGS_1mm` (printed in B07)
also belongs in this ring — bin it here for the dry-fit. Keep front/rear/side groupings labelled so the ring
assembles in the right order.
**Check:** All nine structural segments plus TFT mount labelled by ring position; power inlet (from B07) on hand.

---

## Checkpoint B08
- [ ] All nine skirt segments plus TFT mount pass the flat-reference rocking test
- [ ] Full ring dry-fits: front, rear, and both sides, with consistent joint gaps (power inlet from B07)
- [ ] `mount.stl` vs `mount_thick.stl` choice confirmed and matches what was printed
- [ ] 3 mm brims removed cleanly from all long-flat parts

## Common mistakes
- Skipping the flat-reference check and only noticing a bowed skirt after the panels are mounted.
- Slicing `mount_thick.stl` by accident when the plan calls for `mount.stl`.

## Next
Assembly: *Skirts* (p.212–239). Printing: [B09 — Panels, filtration, spool](B09-panels-filtration-spool.md).
