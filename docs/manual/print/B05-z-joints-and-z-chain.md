# Batch B05 — Z joints + Z chain

**Time:** 5.2 h (1 plate).

**Prerequisites:** B00, B02, B04.

**Printed parts**

| STL | Repo path | Qty | Colour | g ea |
|---|---|---:|---|---:|
| `z_joint_lower_x4.stl` | Voron-2 `STLs/Gantry/Z_Joints/` | 4 | Black | 9.1 |
| `z_joint_upper_x4.stl` | Voron-2 `STLs/Gantry/Z_Joints/` | 4 | Black | 6.6 |
| `z_chain_bottom_anchor.stl` | Voron-2 `STLs/Gantry/` | 1 | Black | 9.1 |
| `z_chain_guide.stl` | Voron-2 `STLs/Gantry/` | 1 | Black | 6.0 |
| `z_rail_stop_x4.stl` | LDOVoron2 `STLs/` | 4 | Black | 1.4 |

Print **4× `z_joint_upper_x4`** and **zero** `z_joint_upper_hall_effect.stl` — that variant exists only for
hall-effect XY endstops, which this kit does not use.

**Hardware:** none.

**Read first**
- Checkpoint after B05: Z joints — the 8 mm shaft should slide, not press. `z_joint_upper` must sit square
  on the extrusion.
- Most commonly reprinted here: `z_joint_lower_x4`.
- The LDO `z_rail_stop` is optional but stops a Z carriage from falling off the top of a rail and spilling its balls.

## Step B05.1 — Filament prep

**Do:** Galaxy Black, confirm ≥83 g remaining.
**Check:** Clean purge.

## Step B05.2 — Load plate B05-P1

**Do:** Slice all fourteen parts: `z_joint_lower_x4` ×4, `z_joint_upper_x4` ×4, `z_chain_bottom_anchor`,
`z_chain_guide`, `z_rail_stop_x4` ×4. No rotation, no brim. Confirm you are **not** including
`z_joint_upper_hall_effect.stl`.
**Parts:** the fourteen pieces above — 5.2 h, 83 g.
**Check:** File list contains only the D2F-compatible `z_joint_upper_x4`, not the hall-effect variant.

## Step B05.3 — Print

**Do:** Print with standing overrides.
**Check:** First layer clean; no warp on the small joint parts.

## Step B05.4 — Inspect

**Do:** With calipers, confirm the 8 mm Z shaft slides (not presses) through each `z_joint_lower`. Check
each `z_joint_upper` sits square against a test extrusion face.
**Check:** Shaft slides freely; joint sits flush and square.

## Step B05.5 — Label and bin

**Do:** Bin for **Z Axis** and **A/B Belts** chapters. Group all four joint pairs together, plus the chain
anchor/guide, plus the four rail stops.
**Check:** 4 complete joint pairs, chain anchor, chain guide, 4 rail stops accounted for.

---

## Checkpoint B05
- [ ] 8 mm Z shaft slides freely through every `z_joint_lower` — no press-fit
- [ ] Every `z_joint_upper` sits square on a test extrusion
- [ ] Confirmed zero copies of `z_joint_upper_hall_effect.stl` were printed
- [ ] `z_rail_stop_x4` fitted or bagged for fitting

## Common mistakes
- Accidentally slicing the hall-effect Z-joint variant instead of the D2F one.
- Treating a tight Z shaft fit as acceptable "because it'll wear in" — it should slide from day one.

## Next
Assembly: *Z Axis* (p.108–123) and *A/B Belts* (p.124–145). Printing: [B06 — Toolhead: Stealthburner, Clockwork 2, Klicky](B06-toolhead-sb-cw2-klicky.md).
