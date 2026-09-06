# Batch B08 — Skirts and front modules

**These are the parts people see.** Print them after the Gen 2 belt upgrade (see
[00-slicer-setup.md](00-slicer-setup.md#gen-2-belt-upgrade-pause-rule)) — the four plates in this batch carry
the 150–182 mm skirt segments, large flat vertical faces, exactly where GT1.5's reduced VFA shows.

**Time:** 29.2 h (4 plates) — PrusaSlicer 2.9.6 estimates.

**Sessions:** 4 plate starts (~5 min hands-on each, 5.0–9.5 h unattended) + ~20 min inspect and bin.

**Prerequisites:** **Gate A re-passed on a fresh cube after the Gen 2 belt upgrade** (Step B00.5; no bearing
seat here, so Gate B is not needed — this prints before the kit). B02 (accent belt guards, fan grills,
faceplate) and B07 (`power_inlet_IECGS_1mm`) feed the same skirt ring and are already printed in the pre-kit
order; the dry-fit at B08.10 wants the inlet to hand.

The skirt ring is made of ten structural segments plus two "module" pieces — the TFT mount and the power
inlet — sharing a 67–72 × 20 mm cross-section. On the 350: front = `front_skirt_a` + TFT mount + `front_skirt_b`; rear = `rear_center_skirt`
+ `power_inlet` + `keystone_panel`; each side = `side_skirt_a` + `side_fan_support` + `side_skirt_b`.

**Printed parts**


| STL | Repo path | Qty | Colour | g ea | Bin |
|---|---|---:|---|---:|---|
| `rear_center_skirt_350.stl` | Voron-2 `STLs/Skirts/350/` | 1 | Black | 71.9 | 11-skirts |
| `front_skirt_a_350.stl` | Voron-2 `STLs/Skirts/350/` | 1 | Black | 41.4 | 11-skirts |
| `front_skirt_b_350.stl` | Voron-2 `STLs/Skirts/350/` | 1 | Black | 41.4 | 11-skirts |
| `side_skirt_a_350_x2.stl` | Voron-2 `STLs/Skirts/350/` | 2 | Black | 36.9 | 11-skirts |
| `side_skirt_b_350_x2.stl` | Voron-2 `STLs/Skirts/350/` | 2 | Black | 36.9 | 11-skirts |
| `side_fan_support_x2.STL` | Voron-2 `STLs/Skirts/` | 2 | Black | 33.0 | 11-skirts |
| `keystone_panel.stl` | Voron-2 `STLs/Skirts/` | 1 | Black | 38.6 | 11-skirts |
| `mount.stl` (BTT Pi TFT4.3) | LDOVoronTrident `STLs/BTT Pi TFT4.3 Mount/` | 1 | Black | 30.1 | 11-skirts |

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
- Two to four of these long parts fit per plate — every one is 117–182 mm on its long axis and 67–72 mm deep,
  and the outline packer interleaves the C-shaped segments at a 6 mm gap on the 250×220 bed.
- **3 mm brim, already in every project,** on `rear_center_skirt_350`, `front_skirt_a/b_350`, `side_skirt_a/b_350`,
  `side_fan_support`, `keystone_panel` (per [00-slicer-setup.md](00-slicer-setup.md#orientation-brim)); `mount.stl`
  on P3 has none. At each plate you verify the outline in the preview — you never add one.
- Optional, not printed here: `[a]_fan_grill_open_optional_x2` (more airflow, less filtering) instead of
  `[a]_fan_grill_a/b`; extra `ldo_bestagon_insert`s.

## Step B08.1 — Filament prep

**Do:** Galaxy Black, spool #1 after B07: ~522 g at the start, ~124 g at the end, so no runout here. The
first predicted runout is B09-P2. Sheet per [00-slicer-setup § Print sheet](00-slicer-setup.md#print-sheet),
renewing the glue film.
**Check:** Spool weighed and written in the ledger before starting the 6.3 h P1 plate.

Source: [print plan §4.3 — spool changes](../../voron-print-plan.md#43-spool-changes) · [00-slicer-setup § Drying](00-slicer-setup.md#drying) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B08.2 — Load plate B08-P1

![Plate B08-P1 — sorting diagram](../assets/plates/B08-P1.png)

*Sorting diagram, drawn from the committed project: every part numbered and filled in the colour of its bin, bin id on the part; the legend reads # · STL · bin (chapter · steps). Sort at Step B08.11.*

**Do:** Open `slicer/plates/B08-P1.3mf` with **File → Open Project**. The arrangement, brims and overrides
are already in it. Confirm the rear skirt is turned 90° about Z, its 182 mm axis running front-to-back along
Y, beside an unturned `side_fan_support`.
**Parts:** `rear_center_skirt_350` · `side_fan_support` ×1 — 6.3 h, 99 g (PrusaSlicer 2.9.6 estimate) · 3 mm brim on both, already in the project.
**Check:** Both parts flat on their shipped faces, long axes front-to-back, brim outline on both in the
preview, plate matching the image above.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [print plan §5.1 — orientation and brim](../../voron-print-plan.md#51-orientation-and-brim)

## Step B08.3 — Print plate B08-P1

**Do:** Print with standing overrides.
**Check:** Watch the ends of `rear_center_skirt_350` for the first hour: 182 mm is the worst warp candidate in the set.

Pause: ~5 min since the last pause — plate started; nothing to do until it finishes.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B08.4 — Load plate B08-P2

![Plate B08-P2 — sorting diagram](../assets/plates/B08-P2.png)

*Sorting diagram, drawn from the committed project: every part numbered and filled in the colour of its bin, bin id on the part; the legend reads # · STL · bin (chapter · steps). Sort at Step B08.11.*

**Do:** Open `slicer/plates/B08-P2.3mf` with **File → Open Project**. The arrangement, brims and overrides are
already in it. Confirm it loaded as described rather than rebuilding it.
**Parts:** `front_skirt_a_350` · `front_skirt_b_350` · `side_skirt_a_350` ×1 — 8.4 h, 108 g (PrusaSlicer 2.9.6 estimate) · 3 mm brim on all three, already in the project.
**Check:** Brim outline shows on all three in the preview.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim)

## Step B08.5 — Print plate B08-P2

**Do:** Print with standing overrides.
**Check:** Both front skirts lay down a clean first layer across the full 150 mm; no corner lift.

Pause: ~5 min since the last pause — plate started; nothing to do until it finishes.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B08.6 — Load plate B08-P3

![Plate B08-P3 — sorting diagram](../assets/plates/B08-P3.png)

*Sorting diagram, drawn from the committed project: every part numbered and filled in the colour of its bin, bin id on the part; the legend reads # · STL · bin (chapter · steps). Sort at Step B08.11.*

**Do:** Open `slicer/plates/B08-P3.3mf` with **File → Open Project**. The arrangement, brims and overrides are
already in it. Confirm it loaded as described rather than rebuilding it.
**Parts:** `side_fan_support` ×1 · `side_skirt_a_350` ×1 · `side_skirt_b_350` ×1 · `mount.stl` — 9.5 h, 121 g (PrusaSlicer 2.9.6 estimate) · 3 mm brim on the three skirt parts, none on the TFT mount, all as shipped in the project.
**Check:** Brim outline on the three skirt parts, none on the mount; confirm `mount.stl`, not `mount_thick.stl`.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [LDO Rev D printed-parts guide](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d)

## Step B08.7 — Print plate B08-P3

**Do:** Print with standing overrides.
**Check:** No corner lift on the skirts, no warp on the tall narrow TFT mount.

Pause: ~5 min since the last pause — plate started; nothing to do until it finishes.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B08.8 — Load plate B08-P4

![Plate B08-P4 — sorting diagram](../assets/plates/B08-P4.png)

*Sorting diagram, drawn from the committed project: every part numbered and filled in the colour of its bin, bin id on the part; the legend reads # · STL · bin (chapter · steps). Sort at Step B08.11.*

**Do:** Open `slicer/plates/B08-P4.3mf` with **File → Open Project**. The arrangement, brims and overrides are
already in it. Confirm it loaded as described rather than rebuilding it.
**Parts:** `side_skirt_b_350` ×1 · `keystone_panel` — 5.0 h, 70 g (PrusaSlicer 2.9.6 estimate) · 3 mm brim on both, already in the project.
**Check:** Brim outline shows on both in the preview.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim)

## Step B08.9 — Print plate B08-P4

**Do:** Print with standing overrides.
**Check:** Keystone panel's two cutout slots print crisp and undistorted.

Pause: ~5 min since the last pause — plate started; nothing to do until it finishes.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B08.10 — Inspect

**Do:** Lay every skirt segment from all four plates on the flat granite reference; check each for rocking.
Dry-fit the full ring: front `front_skirt_a` + TFT `mount` + `front_skirt_b`; rear `rear_center_skirt` +
`power_inlet` from B07 + `keystone_panel`; each side `side_skirt_a` + `side_fan_support` + `side_skirt_b`.
**Check:** No rocking on any segment. Ring dry-fits with consistent gaps at every joint.

Pause: ~20 min since the last pause — every segment checked flat, brims off, ring dry-fitted and taken apart again. Nothing bolted.

Source: [print plan §5.2 — checkpoint after each batch](../../voron-print-plan.md#52-checkpoint-after-each-batch) · [00-slicer-setup § Calibration sequence](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) · [Prusa KB — Warping](https://help.prusa3d.com/article/warping_2011)

## Step B08.11 — Sort into bins

**Do:** Sort off each plate diagram; the bin id is printed on every part. Labels: [bin-labels sheet](../../print/bin-labels.md). Bins: [README § Bins](README.md#bins). Every plate here feeds **11-skirts**, joining B02's `[a]_faceplate` and inserts. Stack by ring position: front, rear, left, right.

**B08-P1**

| bin | parts off this plate |
|---|---|
| **11-skirts** — Skirt ring, keystone panel, TFT mount | `rear_center_skirt_350`, `side_fan_support` |

**B08-P2**

| bin | parts off this plate |
|---|---|
| **11-skirts** — Skirt ring, keystone panel, TFT mount | `front_skirt_a_350`, `front_skirt_b_350`, `side_skirt_a_350` |

**B08-P3**

| bin | parts off this plate |
|---|---|
| **11-skirts** — Skirt ring, keystone panel, TFT mount | `side_fan_support`, `side_skirt_a_350`, `side_skirt_b_350`, `mount` |

**B08-P4**

| bin | parts off this plate |
|---|---|
| **11-skirts** — Skirt ring, keystone panel, TFT mount | `side_skirt_b_350`, `keystone_panel` |

**Check:** All ten structural segments plus the TFT mount in 11-skirts, stacked by ring position; B02's grills, retainers and belt guards wait in 11-fans.

Source: [print plan §9 — batch summary](../../voron-print-plan.md#9-machine-readable-batch-summary) · [print plan §2 — which parts gate which step](../../voron-print-plan.md#2-which-parts-gate-the-frame-and-z-drive-steps) · [print/README § Bins](README.md#bins)

---

## Checkpoint B08
- [ ] All ten skirt segments plus TFT mount pass the flat-reference rocking test
- [ ] Full ring dry-fits: front, rear, and both sides, with consistent joint gaps (power inlet from B07)
- [ ] `mount.stl` vs `mount_thick.stl` choice confirmed and matches what was printed
- [ ] 3 mm brims removed cleanly from all long-flat parts

## Common mistakes
- Skipping the flat-reference check and only noticing a bowed skirt after the panels are mounted.
- Slicing `mount_thick.stl` by accident when the plan calls for `mount.stl`.

## Next
Assembly: *Skirts* (Ch 11 Part A, p.212–239). Printing: [B09 — Panels, filtration, spool](B09-panels-filtration-spool.md).
