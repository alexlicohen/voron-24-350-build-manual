# Batch B04 — XY joints + X carriage

**Time:** 7.3 h (1 plate).

**Prerequisites:** B00, B02 (accent `[a]_endstop_pod_D2F_switch`, cable bridge), B03.

**Printed parts**

| STL | Repo path | Qty | Colour | g ea |
|---|---|---:|---|---:|
| `xy_joint_left_lower_MGN12.stl` | Voron-2 `STLs/Gantry/X_Axis/XY_Joints/` | 1 | Black | 32.0 |
| `xy_joint_left_upper_MGN12.stl` | Voron-2 `STLs/Gantry/X_Axis/XY_Joints/` | 1 | Black | 11.7 |
| `xy_joint_right_lower_MGN12.stl` | Voron-2 `STLs/Gantry/X_Axis/XY_Joints/` | 1 | Black | 32.7 |
| `xy_joint_right_upper_MGN12.stl` | Voron-2 `STLs/Gantry/X_Axis/XY_Joints/` | 1 | Black | 11.1 |
| `x_frame_V2TR_MGN12_left.stl` | Voron-2 `STLs/Gantry/X_Axis/X_Carriage/` | 1 | Black | 17.1 |
| `x_frame_V2TR_MGN12_right.stl` | Voron-2 `STLs/Gantry/X_Axis/X_Carriage/` | 1 | Black | 17.2 |
| `probe_retainer_bracket.stl` | Voron-2 `STLs/Gantry/X_Axis/X_Carriage/` | 1 | Black | 0.5 |

⚠ **Probe retainer bracket, conditional:** only used with the Omron inductive probe. Costs 0.5 g — print
it, decide later. If the probe barrel measures 9 mm rather than 8 mm on arrival, print
`probe_retainer_bracket_9mm.stl` instead **(verify on arrival)**.

**Hardware:** none.

**Read first**
- Checkpoint after B04: test the MGN12 carriage screw pattern against `x_frame_V2TR_MGN12_*` before
  committing heat-sets. XY joint bores must accept the shafts without reaming.
- Most commonly reprinted here: `xy_joint_*_lower_MGN12`.
- `x_frame_V2TR_MGN12_*` are the R2/Clockwork-2 carriage halves — LDO Build Notes p.129-130 warn
  specifically about using the wrong X-carriage variant here.

## Step B04.1 — Filament prep

**Do:** Galaxy Black, confirm ≥122 g remaining.
**Check:** No colour cross-contamination from B03.

## Step B04.2 — Load plate B04-P1

**Do:** Slice all seven parts together: `xy_joint_left_lower_MGN12`, `xy_joint_left_upper_MGN12`,
`xy_joint_right_lower_MGN12`, `xy_joint_right_upper_MGN12`, `x_frame_V2TR_MGN12_left`,
`x_frame_V2TR_MGN12_right`, `probe_retainer_bracket`. No rotation, no brim.
**Parts:** all seven — 7.3 h, 122 g.
**Check:** Confirm the files are `x_frame_V2TR_MGN12_left/right` (V2TR = the shared V2/Trident R2 carriage,
so `TR` in the name is correct) — **not** the superseded `Superceded_Parts/MGN9_X/x_carriage_frame_*_MGN9` files.

## Step B04.3 — Pre-print checks

**Do:** Chamber preheated, sheet clean.
**Check:** Chamber ≥40 °C.

## Step B04.4 — Print

**Do:** Print with standing overrides.
**Check:** First layer clean on both XY joint lowers — these are the largest parts on the plate.

## Step B04.5 — Inspect

**Do:** With calipers, dry-fit the MGN12 carriage screw pattern against `x_frame_V2TR_MGN12_left/right`
before committing any heat-set inserts. Check XY joint bores accept the X-axis shafts without reaming.
**Check:** Screw pattern lines up; shafts slide into the joint bores without forcing.

## Step B04.6 — Label and bin

**Do:** Bin with B02's `[a]_endstop_pod_D2F_switch` and cable bridge for **Gantry**. Keep
`probe_retainer_bracket` loose until the probe decision (Omron barrel diameter) is confirmed.
**Check:** All Gantry-destined parts, black and accent, grouped together.

---

## Checkpoint B04
- [ ] MGN12 carriage screw pattern confirmed against `x_frame_V2TR_MGN12_left/right` before heat-sets
- [ ] XY joint bores accept shafts without reaming
- [ ] Omron probe barrel measured (8 mm vs 9 mm) — correct `probe_retainer_bracket` variant confirmed
- [ ] Confirmed X-carriage is `x_frame_V2TR_MGN12_left/right` (V2TR/Clockwork-2), not the superseded MGN9 carriage

## Common mistakes
- Grabbing a superseded MGN9 X-carriage file by mistake — LDO Build Notes flag this explicitly. `V2TR` is the
  right file: it is the carriage shared by the V2 and the Trident.
- Committing heat-set inserts into the carriage before dry-fitting the screw pattern.
- Reaming an XY joint bore instead of checking the shaft or reprinting.

## Next
Assembly: *Gantry* (p.82–107). Printing: [B05 — Z joints + Z chain](B05-z-joints-and-z-chain.md).
