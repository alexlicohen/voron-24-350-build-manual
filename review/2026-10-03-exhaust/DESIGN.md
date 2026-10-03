# Chamber exhaust fan — design record (2026-10-03)

Alex's decision (2026-10-03): one chamber exhaust fan, driven by the chamber thermistor through Klipper, so PLA
(~35 °C) and PETG (~40 °C) print in a cool, steady chamber; every other cooling or venting mod is deferred. After the
build he prints mostly PLA/PETG, ASA only occasionally.

**Decision in one line:** the stock Voron 2.4r2 exhaust housing over the stock back-panel notch (no cutting), a 24 V
6020 on Leviathan FAN0 (`PB7`) with a third 24 V jumper, `[temperature_fan exhaust_fan]` reading the existing
`chamber_temp` through a `temperature_combined` sensor, `watermark` control, ceiling per filament from PrusaSlicer's
native *Chamber temperature* fields via `PRINT_START`, ASA never vented. Ch 14 Part H, Steps 14.25–14.36.

## Folder

| File | What |
|---|---|
| `exhaust.cfg` | the Klipper block, byte-identical to Ch 14 Step 14.33's (the test asserts it) |
| `test_macros.py` | `.venv/bin/python review/2026-10-03-exhaust/test_macros.py` — macros rendered with Klipper's Jinja delimiters; `PRINT_START` (Ch 12 12.36 block) and LDO's `PRINT_END` with the inserted lines; Klipper's own `temperature_fan.py` + `temperature_combined.py` at `f0892d8` driven by a mock `chamber_temp`; since the 2026-10-03 follow-up also the Nevermore gating (`FILAMENT=`), `_EXHAUST FILTER=` and `_NEVERMORE_SCRUB`. PASS 2026-10-03, 35 checks |

## 1. Physical exhaust

**Stock housing exists and fits without cutting** (verified):
- Voron-2 `STLs/Exhaust_Filter/` at the pinned `a192410`: `exhaust_filter_housing`, `[a]_exhaust_filter_mount_x2`,
  `[a]_filter_access_cover`, `[a]_exhaust_fan_grill`, `exhaust_filter_grill`. Manual p.250–256.
- Stock `Drawing_DXFs/Panels/350_Back_Panel.DXF` = 483 × 503 mm with a centred notch in the top edge, 147 mm wide ×
  42.5 mm deep. The LDO back panel is 483 × 503 × 3 mm (Ch 11 11.55), and LDO ships `exhaust_cover.stl` "with the
  stock exhaust grill to seal the back panel" (print plan l.598): the LDO panel carries the stock notch. Bench
  confirmation is gate row 1 of Step 14.25.
- The kit's printed set already has `exhaust_filter_grill` (B09-P3, fitted at 11.54); the other four were listed as
  skipped (print plan l.600, l.837). They are now an add-on print outside the plates, like the scrubber.
- Geometry from the cached 2.4r2 assembly CAD (`~/.cache/voron-cad/cache/index.json`): grill in the notch plane, flush
  with the panel's outer face; two mounts on M5 drop-in T-nuts in the top rear extrusion's back slot; housing taped
  (VHB) to the panel's outside, projecting ~48 mm, fan grill to ~62 mm. M3×12 ×2 through the grill into the housing
  from inside. Hardware in the CAD: 8 M3 inserts, 4 M3×30, 2 M3×12, 2 M3×8, 2 M5×10 BHCS (+2 M5 T-nuts per p.254).
  All kit spares (`parts.py --ledger`: inserts 153/122, M3×30 44/17, M3×12 50/32 — the two come off the cover, M3×8
  283/207, M5×10 BHCS 54/35, M5 roll-in T-nut 80/68).
- **Fan: 60×60×20, 24 V.** CAD solid "6020 Fan"; the screw stack confirms it (M3×30 = 3.2 grill + 20 fan + ~6.8 in
  the insert; a 6025 would leave 1.8 mm). The kit's two 6020s are the bay pair (BOM qty 2, both fitted at 10.47), so
  one is bought. Leviathan fan channels are 0.5 A each (README); a 6020 draws ~0.1 A.
- **Connector:** Leviathan V1.3 `FAN_0` = J22, `JST_XH_B3B-XH-A` (3-pin XH 2.5, power/GND/tach) per the KiCad
  schematic @878c3c4; LDO's `voron2_leviathan.cfg` @878c3c4: FAN0 `PB7`, tach `PB8`; FAN1 `PB3`. A 2-wire fan's 2-pin
  XH plug sits on the power pins; Step 14.31 copies FAN2's red-wire position (no crimper owned). Buy a 1 m XH 2-pin
  extension; Step 14.25 measures the route (gate ≤ 1250 mm).
- **Cable route (bench item):** the fan is outside the chamber; its lead is fed inside the housing on the intake
  side, out through a grill opening, down the back panel's inner face on VHB tie points, into the bay through the
  Z-chain notch beside the FILTER FAN lead (layout v3 keeps DC out of the round hole). Nothing in the Part cuts or
  drills to make a route; the gate stops the add-on if none exists. Not found in any source: how stock 2.4 builds
  route this lead (Voron's gantry-wire table explicitly excludes the exhaust fan).
- **PTFE:** the LDO cover's centre hole is threaded (Ø ~8.9–9.6 modelled, i.e. a 1/8 BSPP-class coupler) and the
  stock housing's top boss is the same class (Ø ~9.1–9.9) with a Ø ~4.4 PTFE channel. The manual never fits the kit's
  "4mm Bowden Coupler"; if the PTFE runs through the cover, the coupler moves to the housing boss `(verify on bench)`.
- **Clearance:** gate row 2 wants ≥ 100 mm free behind the notch (62 mm housing + outlet room).

**Fumes.** The stock filter bay holds a stack of mat (six 7 mm layers in the CAD, 130 × 65 mm). Part H fits two
layers of cuttable activated-carbon cooker-hood mat: some odour capture, little flow loss. Rationale: ASA is never
vented (its fumes stay with the Nevermore, as designed); PLA/PETG venting through a thin mat matches how Alex already
runs the Core One+ (AFS bypass flaps vent PLA/PETG unfiltered, Filter All Materials off). Step 14.36's fallback order
if the ceiling cannot be held: one layer out → door ajar. Voron's own note (Voron-Documentation
`tuning/filament_tuning.md` @b8c014f): "with enclosures, some filaments such as PLA may need to have the doors opened
and the exhaust fan running (and even the sides removed)". Expect a ceiling, not air conditioning.

**Not a STOP.** No panel cutting, drilling or remix; the cover swap is reversible (keep the cover). The only open
choices left to Alex are in § 6.

## 2. Klipper

```ini
[temperature_fan exhaust_fan]   # full block: exhaust.cfg / Step 14.33
pin: PB7
sensor_type: temperature_combined
sensor_list: temperature_sensor chamber_temp
combination_method: max
maximum_deviation: 999.9
control: watermark
max_delta: 2.0
target_temp: 0
min_speed: 0.0
max_speed: 1.0
shutdown_speed: 0.0
kick_start_time: 0.5
min_temp: 0
max_temp: 100
```

- **Sensor: `temperature_combined`, not a converted sensor or `duplicate_pin_override`.** Klipper refuses a pin
  declared twice; `[duplicate_pin_override]` is documented as "for diagnostic and debugging purposes … may cause
  confusing and unexpected results". Converting `chamber_temp` into the fan renames the object, which breaks Ch 12
  12.36's `TEMPERATURE_WAIT SENSOR="temperature_sensor chamber_temp"`, Ch 14 14.8's reading, Ch 13's checks and the
  Checkpoint lines. A combined sensor with one member reads `chamber_temp`'s value every 0.3 s, so nothing existing
  changes: Mainsail keeps `chamber_temp` and adds `exhaust_fan` (temperature + target + speed), `M105` keeps
  `chamber_th`, no macro edits. Source-verified at `f0892d8` (= master 461c4e3, identical blobs): `temperature_fan`
  calls `heaters.setup_sensor()`, `temperature_combined` is auto-loaded from `temperature_sensors.cfg` and implements
  `setup_minmax`/`setup_callback`/`get_report_time_delta`. Klipper's docs list extruders/heater_generic/heater_bed as
  users; `temperature_fan` is not named but uses the same factory. `test_macros.py` instantiates the real classes.
- **`min_temp: 0` is required**, not cosmetic: the combined sensor starts at 0.0 and its timer compares against
  `min_temp` before `chamber_temp` has reported; `min_temp: 5` shuts Klipper down at boot (test shows it).
- **No `gcode_id`:** `chamber_th` already reports the same reading in `M105`; a second id adds nothing (Mainsail reads
  objects, not M105).
- **`watermark`, not `pid`:** Klipper has no `PID_CALIBRATE` for a temperature_fan, so gains would be guesses; the
  plant is slow (minutes) and the sensor moves with the toolhead, so a PID would chase position; Klipper's PID path
  floors the fan at `min_speed` whenever a target is set (`max(min_speed, max_speed − co)`), which is the opposite of
  "off when cool". Watermark: off below ceiling − 2, flat out above ceiling + 2; the 4 °C band is irrelevant to
  PLA/PETG. Same choice as the Voron community page.
- **`target_temp: 0`**: `set_tf_speed` forces 0 whenever the target is ≤ 0, so 0 = off regardless of temperature;
  the fan does nothing until a print sets a ceiling, and every `RESTART` returns it there.
- **`shutdown_speed: 0.0`** (temperature_fan's default is full on): matches LDO's stock `[heater_fan exhaust_fan]` and
  `[fan_generic nevermore]`; a fault cuts the heaters anyway.
- **Macros:** `_EXHAUST CHAMBER= TARGET=` (called first thing in `PRINT_START`, after `SET_GCODE_OFFSET Z=0`): any
  print that waits for chamber heat (`CHAMBER > 0`) or asks a ceiling above `hot_above` = 45 °C is a hot-chamber
  material → ceiling 0; it also cancels a pending purge timer, so a print started within 10 min of the last one keeps
  its ceiling. `_EXHAUST_PURGE` (in `PRINT_END` after `TURN_OFF_HEATERS`): after a vented print, ceiling 1 °C = flat
  out for `purge_min` = 10 min, then `[delayed_gcode _EXHAUST_OFF]` sets 0; after an unvented (ASA) print, 0 at once
  and the Nevermore keeps running as before. No `M141` macro: one owner (`PRINT_START`), and PrusaSlicer emits
  `M141` only with automatic temperature commands on, which Ch 13 13.41 turns off for good reason.

Chamber thermistor placement (LDO `cw2_captive_pcb_cover`, CT = `nhk:PB2`, Ch 08 08.51): good enough to control a
ceiling. Bias: it rides on the toolhead, in the bed's plume at low Z and near the hotend and its fan exhaust, so
during a print it reads warm against mid-chamber air (magnitude not measured; Step 14.36 Tip suggests a reference
thermometer). For a ceiling that errs safe: the fan runs a little more, the real chamber sits a little under the
setting. It also wanders with toolhead position; `max_delta` 2 absorbs that. For ASA the fan is off, so the bias does
not matter. A fixed mid-chamber thermistor on a spare Leviathan `TH` port would be the upgrade if the log shows a
problem (not proposed now: it is a purchase and a wire).

## 3. PrusaSlicer 2.9.6

Printer preset `Voron 2.4 350`, start G-code (one line, replaces Ch 13 13.41's):

```
PRINT_START BED=[first_layer_bed_temperature] EXTRUDER=[first_layer_temperature] CHAMBER={chamber_minimal_temperature[initial_tool]} EXHAUST={chamber_temperature[initial_tool]}
```

End G-code stays `PRINT_END`. **No filament start/end G-code lines.** Per filament, Filament Settings → Chamber
temperature (Expert mode; `comExpert` in PrintConfig.cpp) — Nominal / Minimal:

| Preset (the ones printed on the Voron) | Nominal → ceiling | Minimal → `CHAMBER` wait | Prusa vendor values (2.5.11) |
|---|---|---|---|
| PLA | 35 | 0 | 20 / 0 |
| PETG | 40 | 0 | 35 / 0 |
| ASA | ignored (fan off) | Ch 14 14.8 settled − a few °C | 55 / 40 |

Why native fields, not filament G-code or an `M141` macro: (1) filament start G-code runs after `PRINT_START`, too
late for the soak; (2) Prusa uses the same two fields with the same meaning on the Core One (fans hold the chamber at
or below Nominal; the printer waits for Minimal), so the value sits where PrusaSlicer users look; (3) it also fixes a
latent hang: `CHAMBER` was one printer-level number, so raising it for ASA after 14.8 would make every PLA print
`TEMPERATURE_WAIT` forever (no timeout). Minimal 0 = no wait.

Verified with the 2.9.6 CLI (`voron-coreone-asa.ini` + Klipper flavour, automatic temperature commands off, these
two fields): PLA → `PRINT_START BED=60 EXTRUDER=215 CHAMBER=0 EXHAUST=35`, PETG → `… CHAMBER=0 EXHAUST=40`, ASA →
`… CHAMBER=40 EXHAUST=55`; no `M141`/`M191`/`M190`/`M109` emitted. Source: `GCode.cpp` @version_2.9.6
l.1981–2001 writes chamber commands only when `autoemit_temperature_commands` is on. With vendor values untouched,
PLA's 20 still works (fan runs more) and ASA stays off via `hot_above`.

Where the manual says it: a step (14.35), because it is an action in the add-on; no frozen step edited.

## 4. Manual placement

Ch 14, new **Part H** after 14.24, before the Tuning log and Checkpoint 14 (Ch 14 has no What-if section). Why not
Ch 13 like the scrubber: the housing needs the back panel on (Ch 11 Part B, after Ch 13), and the test needs Ch 14
14.8's settled ASA number to prove the closed housing does not leak the 50–60 °C band. The intro says Ch 10's "exactly
two jumpers" / "FAN0 empty" checks describe the machine before the add-on; 14.31's ⚠ and Check state the new count.

| Step | Title | Kind | Helper |
|---|---|---|---|
| 14.25 | Inspect the back of the machine before anything is bought (gate-calc `exhaust-fit`) | off | yes |
| 14.26 | Print the exhaust parts on the Core One+ | bench | yes |
| 14.27 | Set the eight heat-set inserts in the housing | **iron** | – |
| 14.28 | Build the fan and the filter into the housing | **blade** (scissors) | – |
| 14.29 | Swap the exhaust cover for the housing | off | yes |
| 14.30 | Shut down, unplug and prove it dead | **mains** | – |
| 14.31 | Plug the lead into FAN0 and jumper it for 24 V | **mains** (bay open) | – |
| 14.32 | Close the bay and power on, hand on the switch | **mains** | – |
| 14.33 | Add the exhaust fan to `printer.cfg` | on | yes |
| 14.34 | Test the fan by target, then on a hot chamber (gate-calc `exhaust-test`) | **hot** | – |
| 14.35 | Give PrusaSlicer the exhaust ceiling | laptop | yes |
| 14.36 | Print PLA under a 35 °C ceiling, log it, shut down | **hot** | – |

`hooks/mascot.py` `NO_MASCOT_STEPS`: mains 14.30–14.32, iron 14.27, blade 14.28, hot 14.34 14.36. Six Pause
segments (Sessions 14 → 20 with Part H). Header, Hardware table, tuning-log rows, Checkpoint 14 optional line, 00-index
row 31 + chapter table, Ch 00 00.8 buy row, print README add-on row, print plan l.600/l.837 notes, and Ch 15's
two "exactly two jumpers" lines (tap-tree leaf + table) now add "three with Part H".

## 5. Purchases

| Item | Rough price | Source |
|---|---|---|
| 60×60×20 mm 24 V fan, 2-wire, ball bearing (XH 2.54/2.5 plug if offered) | ~$10 | Amazon / any electronics shop (e.g. GDStime, Winsinn 6020 24 V) |
| JST-XH 2-pin extension lead, 1 m (1.5 m if 14.25's string > 1250 mm) | ~$7 (multi-pack) | Amazon |
| Activated-carbon cooker-hood filter mat, cuttable | ~$10 | Amazon / hardware store |

Not bought (kit spares): screws, inserts, T-nuts, VHB, zip ties, the third jumper (Ch 09 bag holds five, Ch 10 uses
two). Not bought: a JST crimper (the plug and FAN2's pattern avoid crimping).

## 6. Open — Alex / bench

1. **Bench:** the LDO back panel has the stock notch, free depth ≥ 100 mm, the extrusion's back slot reachable, a lead
   route without cutting, route length (14.25). If no route: STOP — any hole is Alex's call, outside Part H.
2. **Bench:** the kit coupler threads into the housing boss, if the PTFE ran through the cover (14.29).
3. **Bench:** FAN0 polarity by FAN2's plug; a 2-pin XH plug seats on the 3-pin header's power pins (14.31).
4. **Bench:** the closed housing still lets ASA settle at 50–60 °C (14.34); the 35 °C ceiling holds with the door shut
   (14.36). Unknown until measured: whether a 6020 through two mat layers is enough (Voron's own note says maybe not).
5. **Alex (optional):** filter choice — two carbon layers (default), none (max flow, consistent with the Core One+
   PLA/PETG practice), or the full stack.
6. Not verified on real Klipper/Mainsail: the macros and the combined-sensor path ran only offline (test_macros.py,
   real Klipper classes with mocks). Mainsail's display of a `temperature_fan` (target box, speed) is expected, not seen.

## Side findings (outside this task, not acted on)

Follow-up 2026-10-03 (same day): the first, third and fourth findings below are fixed in the manual (13.41 machine
limits and binary G-code; 11.42/11.54/11.55 grill inside, cover outside with two inserts, two M5 tabs and the
PTFE coupler, 14.29 reusing them; 12.36 `FILAMENT=` gating with `_NEVERMORE_SCRUB`, and `_EXHAUST FILTER=`
so a filtered material is never vented). The 13.41 claim was confirmed with the 2.9.6 CLI; the GUI switches
*How to apply limits* to *Use for time estimate* itself when the flavour changes (`Tab.cpp` @version_2.9.6).

- Ch 13 13.41 switches the copied Core One printer preset to Klipper flavour but does not change *Machine limits*;
  the 2.9.6 CLI refuses to export ("Machine limits cannot be emitted to G-Code when Klipper firmware flavor is used")
  until `machine_limits_usage` is `time_estimate_only` or `ignore`. The GUI likely says the same at export. Worth a
  line in 13.41.
- The copied Core One filament presets emit `M572 S…` (Prusa pressure advance) from their filament start G-code;
  Klipper answers "Unknown command" (harmless). PA lives in Klipper per Ch 14.
- Ch 11 11.54 says "cover on the inside face, grill on the outside"; the stock CAD puts the grill in the notch plane
  with the housing outside, and LDO's cover has two top tabs that look like the stock mounts' M5 holes. 11.54 is
  already `(verify on bench)`. The manual never fits the kit's `4mm Bowden Coupler` nor says where the PTFE crosses the
  back panel (probably the cover's threaded centre hole).
- `PRINT_START` turns the Nevermore on for every print, PLA included, spending carbon on materials that do not need
  it.
