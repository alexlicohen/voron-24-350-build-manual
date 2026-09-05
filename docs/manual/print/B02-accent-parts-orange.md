# Batch B02 — Accent parts (orange), "the orange day"

Every accent part in the whole build, printed in one continuous orange session so the accent spool is
mounted exactly once. **Two colour changes in the whole build: black → orange here, orange → black after.**
Everything here is printed before the kit arrives anyway, so nothing waits on this.

**Time:** 18.5 h (3 plates).

**Prerequisites:** B00 printed and gate passed (colour change doesn't skip the calibration requirement).

**Printed parts**

| STL | Repo path | Qty | Colour | g ea |
|---|---|---:|---|---:|
| `[a]_z_drive_baseplate_a_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | Orange | 9.7 |
| `[a]_z_drive_baseplate_b_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | Orange | 9.7 |
| `[a]_belt_tensioner_a_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | Orange | 1.9 |
| `[a]_belt_tensioner_b_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | Orange | 1.9 |
| `[a]_z_tensioner_9mm_x4.stl` | Voron-2 `STLs/Z_Idlers/` | 4 | Orange | 8.1 |
| `[a]_tensioner_left.stl` | Voron-2 `STLs/Gantry/Front_Idlers/` | 1 | Orange | 7.4 |
| `[a]_tensioner_right.stl` | Voron-2 `STLs/Gantry/Front_Idlers/` | 1 | Orange | 7.4 |
| `[a]_cable_cover.stl` | Voron-2 `STLs/Gantry/AB_Drive_Units/` | 1 | Orange | 8.0 |
| `[a]_z_chain_retainer_bracket_x2.stl` | Voron-2 `STLs/Gantry/AB_Drive_Units/` | 2 | Orange | 0.6 |
| `[a]_endstop_pod_D2F_switch.stl` | Voron-2 `STLs/Gantry/X_Axis/XY_Joints/` | 1 | Orange | 8.1 |
| `[a]_xy_joint_cable_bridge_2hole.stl` | Voron-2 `STLs/Gantry/X_Axis/XY_Joints/` | 1 | Orange | 9.2 |
| `XY_cable_chain_bridge-Igus-3mm_backer.stl` | whopping_Voron_mods `extrusion_backers/STLs/` | 1 Note: alternate to the above — fit whichever clears the Ti backers, see §Read first | Orange | 9.1 |
| `[a]_z_belt_clip_lower_x4.stl` | Voron-2 `STLs/Gantry/` | 4 | Orange | 2.3 |
| `[a]_z_belt_clip_upper_x4.stl` | Voron-2 `STLs/Gantry/` | 4 | Orange | 2.4 |
| `[a]_stealthburner_main_body.stl` | Stealthburner `STLs/Stealthburner/` | 1 | Orange | 46.5 |
| `[a]_guidler_a.stl` | Stealthburner `STLs/Clockwork2/Direct_Drive/` | 1 | Orange | 3.7 |
| `[a]_guidler_b.stl` | Stealthburner `STLs/Clockwork2/Direct_Drive/` | 1 | Orange | 2.1 |
| `[a]_latch.stl` | Stealthburner `STLs/Clockwork2/Direct_Drive/` | 1 | Orange | 3.5 |
| `[a]_latch_shuttle.stl` | Stealthburner `STLs/Clockwork2/Direct_Drive/` | 1 | Orange | 1.7 |
| `[a]_pcb_spacer.stl` | Stealthburner `STLs/Clockwork2/` | 1 *(spare — kit supplies one)* | Orange | 0.3 |
| `[a]_belt_guard_a_x2.stl` | Voron-2 `STLs/Skirts/` | 2 | Orange | 5.4 |
| `[a]_belt_guard_b_x2.stl` | Voron-2 `STLs/Skirts/` | 2 | Orange | 5.4 |
| `[a]_fan_grill_a_x2.stl` | Voron-2 `STLs/Skirts/` | 2 | Orange | 5.9 |
| `[a]_fan_grill_b_x2.stl` | Voron-2 `STLs/Skirts/` | 2 | Orange | 5.9 |
| `[a]_fan_grill_retainer_x2.stl` | Voron-2 `STLs/Skirts/` | 2 | Orange | 4.2 |
| `[a]_keystone_blank_insert.stl` | Voron-2 `STLs/Skirts/` | 2 *(1 used + 1 spare; LDO ships one CAT6 keystone)* | Orange | 2.5 |
| `[a]_faceplate.stl` | LDOVoronTrident `STLs/BTT Pi TFT4.3 Mount/` | 1 | Orange | 6.6 |
| `ldo_bestagon_insert.stl` | LDOVoron2 `STLs/` | 1 | Orange | 3.0 |
| `Handle.stl` | whopping_Voron_mods `clickyclacky_door/STLs/` | 1 | Orange | 33.7 |

⚠ **Cable-chain bridge, conditional:** Fabreeko's titanium extrusion backers ship pre-tapped for the cable
chain, which may make the printed bridge unnecessary. Print **both** `[a]_xy_joint_cable_bridge_2hole` and
`XY_cable_chain_bridge-Igus-3mm_backer` (18 g total) and fit whichever clears at assembly. "Igus" = the
2-hole chain pattern, which is what LDO ships.

**Hardware:** none.

**Read first**
- Checkpoint after B02: guidler and latch must move freely against the CW2 body once it exists (B06) —
  test-fit then, not now. Check the SB main body's built-in supports came out clean and the LED pockets are crisp.
- Most commonly reprinted here: `[a]_stealthburner_main_body` — the most-photographed part in the build.
- `[a]_stealthburner_main_body` has **built-in supports** — snap them out, don't cut.
- `Handle.stl` is 60 mm tall on a 68×19 footprint — give it a 5 mm brim (per [00-slicer-setup.md](00-slicer-setup.md#orientation-brim)).
- `[a]_keystone_blank_insert` ×2 covers a panel with 2 slots against 1 LDO-supplied CAT6 keystone — 1 used, 1 spare.

## Step B02.1 — Filament prep

**Do:** Change spool to Prusament ASA Prusa Orange. Purge fully — this is the one accent session in the
whole build, so a clean colour change matters more here than anywhere else.
**Check:** Purge line is clean orange with no black streaking.

## Step B02.2 — Load plate B02-P1

**Do:** Slice `[a]_stealthburner_main_body`, `[a]_faceplate`, `[a]_cable_cover`, `[a]_z_drive_baseplate_a` ×2,
`[a]_z_drive_baseplate_b` ×2. No rotation. Leave the SB main body's built-in supports in place — do not
suppress them in slicer.
**Parts:** the five items above — 5.9 h, 100 g.
**Check:** SB main body oriented as shipped (supports visible in preview).

## Step B02.3 — Print plate B02-P1

**Do:** Print with standing overrides, no brim on this plate's parts.
**Check:** First layer clean; SB body prints without support failure.

## Step B02.4 — Load plate B02-P2

**Do:** Slice `Handle`, `[a]_fan_grill_a` ×2, `[a]_fan_grill_b` ×2, `[a]_fan_grill_retainer` ×2,
`[a]_belt_guard_a` ×2, `[a]_belt_guard_b` ×2, `[a]_tensioner_left`, `[a]_tensioner_right`. **Add a 5 mm
brim to `Handle`** only (60 mm tall, tippy).
**Parts:** the eight items above — 6.1 h, 102 g.
**Check:** Brim applied only to `Handle`, not the flat fan grills/belt guards.

## Step B02.5 — Print plate B02-P2

**Do:** Print with standing overrides.
**Check:** `Handle` stands through the full print with no lean; brim shows no lift.

## Step B02.6 — Load plate B02-P3

**Do:** Slice the remaining accent parts: `[a]_belt_tensioner_a` ×2, `[a]_belt_tensioner_b` ×2,
`[a]_z_tensioner_9mm` ×4, `[a]_z_chain_retainer_bracket` ×2, `[a]_endstop_pod_D2F_switch`,
`[a]_xy_joint_cable_bridge_2hole`, `XY_cable_chain_bridge-Igus-3mm_backer`, `[a]_z_belt_clip_lower` ×4,
`[a]_z_belt_clip_upper` ×4, `[a]_guidler_a`, `[a]_guidler_b`, `[a]_latch`, `[a]_latch_shuttle`,
`[a]_pcb_spacer`, `[a]_keystone_blank_insert` ×2, `ldo_bestagon_insert`. **Check `XY_cable_chain_bridge-Igus-3mm_backer`
in preview** — it's a community remix that may arrive standing 44 mm tall; lay it flat to match the stock
bridge if so.
**Parts:** the 16 files above (29 small accent parts) — 6.5 h, 106 g.
**Check:** Cable-chain bridge sitting flat, not standing, before slicing.

## Step B02.7 — Print plate B02-P3

**Do:** Print with standing overrides.
**Check:** No warp on the small parts; SB accent pieces (guidler, latch, latch shuttle) print crisp — these
have fine features that go under close fitment tolerances later.

## Step B02.8 — Inspect

**Do:** Check the SB main body's built-in supports snapped out clean and the LED pockets are crisp (final
guidler/latch fit test happens at B06, not now).
**Check:** No support remnants inside the SB body's cable channels or LED pockets.

## Step B02.9 — Label and bin

**Do:** Bin by consuming assembly chapter. The Z-drive baseplates/tensioners/9mm tensioners go with the
**Z Drives and Idlers** bin from B01. `[a]_cable_cover`, `[a]_z_chain_retainer_bracket`, `[a]_endstop_pod_D2F_switch`,
the cable bridges, and `[a]_tensioner_left/right` go with **A/B Drives and Idlers** / **Gantry**.
`[a]_z_belt_clip_lower/upper` go with **Gantry**. SB body, faceplate, guidler, latch, latch shuttle, pcb
spacer go with **Stealthburner**. Belt guards, fan grills/retainers, keystone inserts, bestagon insert go
with **Skirts**. `Handle` goes with **B10 — Clicky-Clack door** (keep it separate, orange, until then).
**Check:** Every accent part labelled with its destination chapter; `Handle` set aside specifically for B10.

---

## Checkpoint B02
- [ ] SB main body built-in supports removed clean; LED pockets crisp
- [ ] Cable-chain bridge fit decision made (stock 2-hole vs Ti-backer remix) once Ti backers are in hand
- [ ] `Handle` brim removed cleanly, no visible scarring
- [ ] All 29 small accent parts present and sorted by destination chapter
- [ ] Orange spool re-sealed/dry-stored — no more orange prints until B10 label check

## Common mistakes
- Suppressing the SB main body's built-in supports in slicer instead of leaving them as designed.
- Slicing the Ti-backer cable bridge standing up because it didn't auto-lay-flat.
- Mixing up which fan grill/belt guard pair (`a` vs `b`) goes to which side — label immediately after print.
- Skipping the full purge on the orange colour change and getting black-streaked accent parts.

## Next
Assembly: accent half of *Z Drives and Idlers*, *A/B Drives and Idlers*, *Gantry*, *Stealthburner*, *Skirts*
and the Clicky-Clack door — as their black counterparts complete. Printing: [B03 — A/B drive units + front idlers](B03-ab-drive-units-and-front-idlers.md).
