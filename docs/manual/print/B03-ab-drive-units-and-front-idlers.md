# Batch B03 — A/B drive units + front idlers

**Time:** 7.7 h (2 plates).

**Prerequisites:** B00 printed and gate passed; B02 printed (accent `[a]_cable_cover`,
`[a]_z_chain_retainer_bracket`, `[a]_tensioner_left/right` feed this same assembly chapter).

**Printed parts**

| STL | Repo path | Qty | Colour | g ea |
|---|---|---:|---|---:|
| `a_drive_frame_lower.stl` | Voron-2 `STLs/Gantry/AB_Drive_Units/` | 1 | Black | 22.4 |
| `a_drive_frame_upper.stl` | Voron-2 `STLs/Gantry/AB_Drive_Units/` | 1 | Black | 21.8 |
| `b_drive_frame_lower.stl` | Voron-2 `STLs/Gantry/AB_Drive_Units/` | 1 | Black | 20.5 |
| `b_drive_frame_upper.stl` | Voron-2 `STLs/Gantry/AB_Drive_Units/` | 1 | Black | 21.3 |
| `front_idler_left_lower.stl` | Voron-2 `STLs/Gantry/Front_Idlers/` | 1 | Black | 7.7 |
| `front_idler_left_upper.stl` | Voron-2 `STLs/Gantry/Front_Idlers/` | 1 | Black | 14.1 |
| `front_idler_right_lower.stl` | Voron-2 `STLs/Gantry/Front_Idlers/` | 1 | Black | 13.8 |
| `front_idler_right_upper.stl` | Voron-2 `STLs/Gantry/Front_Idlers/` | 1 | Black | 7.9 |

**Hardware:** none.

**Read first**
- Checkpoint after B03: **F695-2RS (13 mm OD, flanged)** bearing/spacer stacks drop into the drive-frame and
  front-idler bores without reaming — and the two halves of each drive unit must close flat with no gap.
  (625-2RS is the *Z-drive* bearing, B01 — not this batch.)
- Most commonly reprinted here: `a/b_drive_frame_lower` — the bearing seats are the tightest fit in the machine.
- Splitting A and B onto separate plates isn't just packing — a failed plate costs one drive unit, not
  both, and you can build the A side while the B side prints.

## Step B03.1 — Filament prep

**Do:** Back to Galaxy Black. Confirm spool remaining ≥130 g for both plates.
**Check:** Purge clean black, no orange streaking from B02.

## Step B03.2 — Load plate B03-P1 (the A side)

**Do:** Slice `a_drive_frame_lower`, `a_drive_frame_upper`, `front_idler_right_lower`, `front_idler_right_upper`.
No rotation, no brim.
**Parts:** the four items above — 3.9 h, 66 g.
**Check:** Parts sit flat as shipped.

## Step B03.3 — Print plate B03-P1

**Do:** Print with standing overrides.
**Check:** No warp at drive-frame corners.

## Step B03.4 — Load plate B03-P2 (the B side)

**Do:** Slice `b_drive_frame_lower`, `b_drive_frame_upper`, `front_idler_left_lower`, `front_idler_left_upper`.
**Parts:** the four items above — 3.8 h, 64 g.
**Check:** Parts sit flat as shipped.

## Step B03.5 — Print plate B03-P2

**Do:** Can run while the A side is being built up, since the two are independent.
**Check:** No warp at drive-frame corners.

## Step B03.6 — Inspect

**Do:** With calipers, check the F695 bearing seat diameter (13 mm OD, flanged) in each drive frame half. Dry-fit the lower and
upper halves of each drive unit together — they must close flat with no gap.
**Check:** No gap when the two halves are clamped together; bearing seats accept an F695-2RS bearing snugly, no rocking.

## Step B03.7 — Label and bin

**Do:** Bin by consuming assembly chapter: everything here plus B02's `[a]_cable_cover`,
`[a]_z_chain_retainer_bracket`, `[a]_tensioner_left/right`, `[a]_endstop_pod_D2F_switch`, and the cable
bridge feed **A/B Drives and Idlers**. Keep A-side and B-side parts in separate labelled bags.
**Check:** Two complete, correctly-sided part sets (A and B) ready for assembly.

---

## Checkpoint B03
- [ ] F695-2RS (13 mm OD) bearing seats in `a/b_drive_frame_lower/upper` accept the bearing with no rocking
- [ ] Drive unit halves (upper+lower) close flat with no visible gap, both A and B
- [ ] No corner warp on any of the eight parts
- [ ] A-side and B-side parts bagged separately and labelled

## Common mistakes
- Mixing A-side and B-side parts in one bag — they are not interchangeable.
- Force-closing a warped drive-frame half instead of reprinting it.
- Skipping the dry-fit and only discovering the bearing-seat gap during final assembly.

## Next
Assembly: *A/B Drives and Idlers* (p.62–81). Printing: [B04 — XY joints + X carriage](B04-xy-joints-and-x-carriage.md).
