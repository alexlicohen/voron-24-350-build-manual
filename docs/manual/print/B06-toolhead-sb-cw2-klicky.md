# Batch B06 — Toolhead: Stealthburner, Clockwork 2, Klicky

**Time:** 9.8 h (2 plates).

**Prerequisites:** B00, B02 (SB main body, faceplate, guidler, latch, latch shuttle, pcb spacer), B04.
Also requires `probe_retainer_bracket.stl` from B04.

**Printed parts**

| STL | Repo path | Qty | Colour | g ea |
|---|---|---:|---|---:|
| `stealthburner_printhead_revo_voron_front.stl` | Stealthburner `STLs/Stealthburner/Printheads/revo_voron/` | 1 | Black | 40.6 |
| `stealthburner_printhead_revo_voron_rear_cw2.stl` | Stealthburner `STLs/Stealthburner/Printheads/revo_voron/` | 1 | Black | 15.0 |
| `[o]_stealthburner_LED_carrier.stl` | Stealthburner `STLs/Stealthburner/` | 1 | Black (opaque) | 0.9 |
| `[o]_stealthburner_LED_diffuser_mask.stl` | Stealthburner `STLs/Stealthburner/` | 1 | Black (opaque) | 0.3 |
| `main_body.stl` (Clockwork 2) | Stealthburner `STLs/Clockwork2/Direct_Drive/` | 1 | Black | 23.7 |
| `motor_plate.stl` (Clockwork 2) | Stealthburner `STLs/Clockwork2/Direct_Drive/` | 1 | Black | 14.1 |
| `cw2_captive_pcb_cover.stl` | Nitehawk-SB `STLs/` | 1 | Black | 10.9 |
| `KlickyProbe_v2.stl` | Klicky `Probes/KlickyProbe/STL/` | 2 *(1 + spare, per the mod's own advice)* | Black | 2.5 |
| `Probe_Dock_v2.1.stl` | Klicky `Probes/KlickyProbe/STL/` | 1 | Black | 3.1 |
| `Probe_magnet_holder.stl` | Klicky `Probes/KlickyProbe/STL/` | 1 | Black | 2.3 |
| `Probe_magnet_pressfit_helper.stl` | Klicky `Probes/KlickyProbe/STL/` | 1 | Black | 1.6 |
| `Probe_pressfit_holder.stl` | Klicky `Probes/KlickyProbe/STL/` | 1 | Black | 4.6 |
| `KlickyProbe_AB_mount_v2.stl` | Klicky `Printers/Voron/v1.8_v2.4_Legacy_Trident/v1.8_v2.4_Legacy_Trident_STL/` | 1 | Black | 4.4 |
| `KlickyProbe_AB_mount_v2_holder.stl` | Klicky (same folder) | 1 | Black | 1.6 |
| `Mount_magnet_holder.stl` | Klicky (same folder) | 1 | Black | 2.3 |
| `Mount_magnet_pressfit_helper.stl` | Klicky (same folder) | 1 | Black | 1.6 |
| `Mount_pressfit_holder_v2.stl` | Klicky (same folder) | 1 | Black | 6.6 |
| `Dock_mount_fixed_v2.stl` | Klicky (same folder) | 1 | Black | 22.7 |

**Do not print:** an ADXL mount (Nitehawk-SB has one on board); the CW2 chain anchor (kit supplies "CW2
Chain Anchor Tilted" printed).

**Hardware:** none.

**Read first**
- Checkpoint after B06: Revo Voron hotend must sit flat in the printhead front with 4× M3×8. Klicky:
  magnets pressed **below** the plastic surface, polarity consistent, and the probe must attach/detach
  cleanly from the AB mount.
- Most commonly reprinted here: `KlickyProbe_v2` — that's why two are printed.
- Hotend file choice is settled: E3D Revo Voron → the `revo_voron` folder, `..._rear_cw2` for Clockwork 2.
- `cw2_captive_pcb_cover` is LDO's improved cable door (captive screw + external chamber thermistor); the
  stock alternative is `Clockwork2/cable_door_for_pcb.stl` if you'd rather use it.
- Klicky dock: **fixed** mount chosen for simplicity. If you later add the Decontaminator purge bucket, you
  need `Dock_sidemount_fixed_v2.stl` + `Dock_sidemount_left_v2.stl` instead (~25 g, 1.5 h) — not printed here.
- The `Probe_*_pressfit_helper` / `_holder` parts are jigs for pressing the 6×3 magnets in square. Print
  them — a crooked magnet is a probe that doesn't repeat.

## Step B06.1 — Filament prep

**Do:** Galaxy Black, confirm ≥162 g remaining across both plates.
**Check:** Clean purge.

## Step B06.2 — Load plate B06-P1

**Do:** Slice `stealthburner_printhead_revo_voron_front`, `stealthburner_printhead_revo_voron_rear_cw2`,
`[o]_stealthburner_LED_carrier`, `[o]_stealthburner_LED_diffuser_mask`, `main_body` (CW2), `motor_plate`
(CW2), `cw2_captive_pcb_cover`. Confirm the `revo_voron` printhead folder, not a different hotend variant.
**Parts:** the seven items above — 6.3 h, 106 g.
**Check:** Printhead files confirmed from `revo_voron/`, not `dragon/` or another hotend folder.

## Step B06.3 — Print plate B06-P1

**Do:** Print with standing overrides.
**Check:** LED carrier and diffuser mask pockets print crisp — fine features.

## Step B06.4 — Load plate B06-P2

**Do:** Slice the full Klicky set: `KlickyProbe_v2` ×2, `Probe_Dock_v2.1`, `Probe_magnet_holder`,
`Probe_magnet_pressfit_helper`, `Probe_pressfit_holder`, `KlickyProbe_AB_mount_v2`,
`KlickyProbe_AB_mount_v2_holder`, `Mount_magnet_holder`, `Mount_magnet_pressfit_helper`,
`Mount_pressfit_holder_v2`, `Dock_mount_fixed_v2`.
**Parts:** the twelve pieces above — 3.5 h, 56 g.
**Check:** Confirm the *fixed* dock variant, not the sidemount variant.

## Step B06.5 — Print plate B06-P2

**Do:** Print with standing overrides.
**Check:** Magnet-holder pockets print crisp and centered.

## Step B06.6 — Inspect

**Do:** Dry-fit the Revo Voron hotend into the printhead front — must sit flat, ready for 4× M3×8. Press
the 6×3 mm magnets into the Klicky holders using the pressfit-helper jigs — check they sit **below** the
plastic surface and polarity is consistent across probe and mount magnets. Attach/detach the probe from the
AB mount and dock repeatedly.
**Check:** Hotend sits flat, no rocking. Magnets flush or below surface, consistent polarity. Probe
attaches/detaches cleanly and repeatably.

## Step B06.7 — Label and bin

**Do:** Bin with B02's `[a]_stealthburner_main_body`, `[a]_faceplate`, `[a]_guidler_a/b`, `[a]_latch`,
`[a]_latch_shuttle`, `[a]_pcb_spacer` for **Stealthburner**.
**Check:** All toolhead parts, black and accent, grouped together with the spare `KlickyProbe_v2`
clearly marked "spare."

---

## Checkpoint B06
- [ ] Revo Voron hotend sits flat in the printhead front, ready for 4× M3×8
- [ ] Klicky magnets pressed below the plastic surface using the pressfit-helper jigs
- [ ] Magnet polarity consistent between probe and AB mount
- [ ] Probe attaches and detaches cleanly and repeatably from the dock and AB mount
- [ ] Spare `KlickyProbe_v2` bagged separately and labelled

## Common mistakes
- Slicing the wrong hotend printhead folder (not `revo_voron`).
- Pressing Klicky magnets in with inconsistent polarity — the probe won't attach reliably.
- Skipping the pressfit-helper jigs and pressing magnets in freehand, crooked.

## Next
Assembly: *Stealthburner* (p.146–147, then the separate Stealthburner manual). Printing: [B07 — Electronics bay + lighting](B07-electronics-bay-and-lighting.md).
