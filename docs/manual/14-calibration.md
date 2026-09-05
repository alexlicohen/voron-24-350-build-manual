# Chapter 14 — Calibration and tuning

Takes a machine that homes, probes, levels and has printed its first cube (Ch 13) and turns it into a machine that prints Voron-quality ASA: belts at final tension, extruder measured, input shaper set, pressure advance and flow dialled in, and that cube calipered against the Prusa-printed reference.

**Time:** 2.5–4.0 h hands-on (survey §7.2), spread over ~6–8 h wall-clock. Most of the wall-clock is heat soaks (~30 min each) and four test prints.

**Prerequisites:**
- **Ch 13 — First power-up and initial startup.** All wizard steps passed (temperatures → heaters → fans → `STEPPER_BUZZ` → XY endstop → homing → bed locating → 0,0 → Z endstop → probe → PID → QGL → Z-offset).
- **The Voron-printed `Voron_Design_Cube_v7`** from [Ch 13 Steps 13.41–13.42](13-initial-startup.md#step-1341-slice-the-voron-cube), kept. Ch 13 prints the cube and commits the first-layer squish; this chapter measures it, at step 14.11.
- **Ch 06b — Squaring the gantry.** Run immediately after Ch 13, followed by a QGL re-run. **This chapter's belt-tension steps must come after 06b** — the squaring procedure starts by fully releasing A/B tension, so anything you set before it is gone (survey §4.4 #2, §5.2 W1).
- **Ch 11 Part B — Panels and the Clicky-Clack door.** The chamber has to close: Step 14.8 and Checkpoint 14 both gate on a 50–60 °C chamber with panels on and the door shut.
- **Ch 12 — Software.** `[bed_mesh]` added at Step 12.34, `PRINT_START` replaced at Step 12.36 (survey §4.4 #15).
- **Batch B00.** The Prusa-printed `Voron_Design_Cube_v7` in Prusament ASA Galaxy Black, kept as the reference coupon ([B00 step B00.6](print/B00-calibration-and-jigs.md)). You need it in hand at step 14.11.
- **Printed parts: none.** Everything this chapter prints, it prints on the Voron.
- A spool of Prusament ASA in the dryer, warm and loaded (survey §7.3).

**Tools**
- Digital caliper, 150 mm
- Steel rule, 150 mm minimum (belt spans and the e-step mark)
- Masking tape and a fine marker (e-step mark; Ellis prefers tape to a marker line)
- Phone with a spectrum analyser: **Sound Spectrum Analysis** (iOS), **Spectroid** (Android), or **Gates Carbon Drive** (both — use the "motorcycle" option) [src](https://docs.vorondesign.com/tuning/secondary_printer_tuning.html)
- Hex 2 mm and 2.5 mm (belt tensioners)
- Laptop or tablet on the Fluidd/Mainsail console

**Printed parts**

| STL | Qty | Colour |
|---|---|---|
| — none — | 0 | — |

**Hardware** (chapter totals)

| Fastener / part | Qty | Note |
|---|---|---|
| — none — | 0 | No fasteners are added or removed in this chapter. The only things you turn are the two A/B belt tensioner screws and, if needed, the four Z belt clamps. |

**Consumables:** Prusament ASA Galaxy Black (~150 g across all test prints), IPA for the flex plate.

**Read first**
- **Order is not intuitive and is enforced.** PID before QGL (a thermally unstable machine will not QGL repeatably); e-steps before the first print; **input shaper and pressure advance only *after* a successful first print** (survey §3.3). Pressure advance changes when input shaping is enabled, so shaper comes first of the two. [src](https://ellis3dp.com/Print-Tuning-Guide/articles/pressure_linear_advance/introduction.html)
- **`SAVE_CONFIG` restarts Klipper.** Every `SAVE_CONFIG` in this chapter loses your homing. Re-`G32` after each one. Saved values land in the auto-generated block at the *bottom* of `printer.cfg` and override anything you typed above.
- **Change one thing at a time and write it down.** The [tuning log](#tuning-log) at the end of this chapter is the deliverable. If two things change between prints you cannot attribute the result.
- **Do not chase dimensional error with `rotation_distance` or XY compensation.** Ellis: deviations are material shrinkage and bulging, not axis errors; 100–101 % X/Y scaling "is about the range you would expect with ABS". [src](https://ellis3dp.com/Print-Tuning-Guide/articles/extrusion_multiplier.html)
- **Shaper auto-calibration is destructive if abused.** Klipper: "It is not advisable to run the shaper auto-calibration very frequently… There is also an increased risk of some parts unscrewing or becoming loose. Always check that all parts of the printer are securely fixed in place after each auto-tuning." [src](https://www.klipper3d.org/Measuring_Resonances.html)

---

## Part A — Heaters

### Step 14.1 — Pre-flight the config before you tune anything

(no image — see text)

**Parts:** none — console only.

**Do:** Open `printer.cfg` and confirm four things, because every number in this chapter is written into these sections: `[extruder]` has `sensor_type: ATC Semitec 104NT-4-R025H42G`, `pullup_resistor: 2200`, `max_temp: 270`, `rotation_distance: 22.6789511`, `gear_ratio: 50:10`; `[heater_bed]` has `max_power: 0.6` and `control: pid`; `[resonance_tester]` exists with `accel_chip: adxl345`; there is **no** `[input_shaper]` section yet. Confirm the toolhead thermistor and the Revo HF agree: E3D's 60 W HeaterCore uses the Semitec 104NT-4-R025H42G and is rated to **300 °C**, so the config's `max_temp: 270` is a deliberate ceiling below the hardware limit, not the hotend's limit.

**Check:** `STATUS` is clean, both MCUs connected, chamber sensor reading room temperature, hotend and bed both within a couple of degrees of each other and of the room. A hotend reading 20 °C off the bed at rest means a wrong `sensor_type`, and every PID number you are about to generate will be wrong.

⚠ Rev D+ / LDO: These values come from `leviathan-printer-rev-d-**sbv2**.cfg`, not `leviathan-printer-rev-d.cfg`. If `[extruder] sensor_pin` reads `nhk:gpio29` instead of `nhk:PB12` you are on the V1 config and must go back to Ch 12 before doing anything thermal. [src](https://github.com/MotorDynamicsLab/LDOVoron2/blob/main/Firmware/leviathan-printer-rev-d-sbv2.cfg)

### Step 14.2 — Confirm the heaters are already PID-tuned

(no image — see text)

**Parts:** none.

**Do:** Both heaters were tuned and `SAVE_CONFIG`-ed in Ch 13 — [Step 13.29, bed at 100 °C](13-initial-startup.md#step-1329-pid-tune-the-bed-at-100-c) and [Step 13.30, hotend at 245 °C with the part fan at 25 %](13-initial-startup.md#step-1330-pid-tune-the-hotend-at-245-c-with-the-part-fan-at-25). Ch 13 is authoritative for that procedure; do not repeat it here. Open `printer.cfg` and confirm both PID stanzas are in the auto-generated block at the bottom. Re-run Ch 13's procedure only if you have since moved a target — for example if you settle on a **110 °C** bed for ASA (the Prusa filament profile's value, see [print/00-slicer-setup.md](print/00-slicer-setup.md)), re-tune the bed at `TARGET=110`, because PID is most accurate near the temperature it was tuned at.

**Check:** Both stanzas hold *your* numbers, not the LDO config's generic starting values (`58.437 / 2.347 / 363.769` for the bed, `26.213 / 1.304 / 131.721` for the hotend). Do **not** add `pwm_cycle_time`; Klipper's 0.100 s default is correct here and the docs say not to set it "unless there is an electrical requirement to switch the heater faster than 10 times a second".

⚠ Do not simply re-run the hotend tune at 260 °C (the ASA print temperature) with the stock config. `PID_CALIBRATE` deliberately overshoots the target during the relay test, and `[extruder] max_temp` is **270**. A 60 W Revo HF will trip `max_temp` and shut Klipper down mid-tune. If you want a tune at the print temperature, raise `max_temp` to 290 first — safely under the Revo HF's rated 300 °C — then set it back. Tuning at 245 and printing at 260 is perfectly serviceable; this is optional refinement. [src](https://e3d-online.com/pages/revo-support-60w-104nt-heatercore)

### Step 14.3 — Verify thermal stability, then re-QGL

(no image — see text)

**Parts:** none.

**Do:** Heat bed to 100 °C and hotend to 150 °C and let the machine sit for 10–20 minutes from cold. Watch the temperature graph. Then `G32` and run `PROBE_ACCURACY` at bed centre.

**Check:** Both heaters hold within ±0.5 °C of setpoint with no slow oscillation. `PROBE_ACCURACY` reports **σ (standard deviation) < 0.003 mm with no trend** across the samples. A drifting series (each probe lower than the last) means the frame is still expanding — wait longer. If σ stays high after soak, suspect uneven Z belts, which step 14.5 fixes. [src](https://docs.vorondesign.com/build/startup/)

---

## Part B — Belts, final tension

These three steps only run **after Ch 06b squaring and its QGL re-run.** Squaring releases A/B tension by design.

### Step 14.4 — Set A/B belt tension to 110 Hz over a 150 mm span

![Sound Spectrum Analysis reading a belt](https://raw.githubusercontent.com/VoronDesign/Voron-Documentation/master/tuning/images/sound-spectrum-belt.jpg)

**Parts:** 2 mm hex (tensioner screws), steel rule, phone spectrum analyser.

**Do:** Move the X extrusion forward until the **X/Y idler centres are 150 mm from the front idler centres** — measure it, don't estimate; a frequency without a stated span is meaningless. Pluck the 150 mm section of the A belt and read the **lowest** frequency peak in the plot. Adjust the tensioner until it reads approximately **110 Hz**. Repeat on B. The two tensions affect each other — tightening one tightens the other — so go back and forth until both are equal. Then move the X extrusion back at least a few centimetres and forward again, and re-check both.

**Check:** A and B both read within a few Hz of each other at ~110 Hz *after* moving the gantry and returning. If one reads 110 and the other 95, the gantry is not square — go back to Ch 06b, do not compensate with tension.

**The disagreement, resolved:**

| Source | A/B target | Z target |
|---|---|---|
| Official assembly manual p.125 | **no number** — "cut both belts to the same length" | no number |
| [docs.vorondesign.com — Secondary Printer Tuning](https://docs.vorondesign.com/tuning/secondary_printer_tuning.html) | **110 Hz over a 150 mm span** (≈ 2 lb, "on the lower end of the range") | **140 Hz** over 150 mm |
| voronldo.com belt tension guide | 80–100 Hz for a 350 | "same as X/Y, 110–130 Hz" |

**Use 110 Hz / 150 mm.** It is the only sourced official figure, and it is the only one that names the span, which is what makes a frequency mean anything — the same belt at a 200 mm span reads far lower. The Voron docs also explain *why* 110: it corresponds to roughly 2 lb of tension and is deliberately at the low end, so you get a good starting point without stretching the belts. The survey rejects voronldo.com as unaffiliated, uncited and internally inconsistent (survey §4.3, §9 Rejected sources) — ignore the 80–100 Hz figure entirely.

### Step 14.5 — Set the four Z belts to 140 Hz over 150 mm

(no image — see text)

**Parts:** 2.5 mm hex (Z belt clamps), steel rule, phone.

**Do:** Move the gantry up until the **fixed side of the belt is 150 mm from the Z idler centres**. Pluck, measure, adjust — same method as A/B. Do all four. Move the gantry down at least a few centimetres and back up, then re-check all four.

**Check:** All four Z belts within a few Hz of each other at ~140 Hz. Evenness across the four matters more than hitting 140 exactly — the Voron QGL troubleshooting text points at uneven Z belts when `PROBE_ACCURACY` σ is high (survey §4.3). [src](https://docs.vorondesign.com/tuning/secondary_printer_tuning.html)

### Step 14.6 — Re-home, re-QGL, re-verify probe accuracy

(no image — see text)

**Parts:** none.

**Do:** With the machine hot (bed 100 °C, hotend 150 °C, soaked), run `G32` then `PROBE_ACCURACY` again. `QUAD_GANTRY_LEVEL` should converge within its configured `retry_tolerance: 0.0075` inside `retries: 5`.

**Check:** QGL converges in ≤3 retries and σ is still < 0.003 mm. If QGL now needs all 5 retries when it converged in 2 before belt tensioning, one belt is off — go back to 14.4/14.5 rather than raising the tolerance.

---

## Part C — Extruder

### Step 14.7 — Rotation-distance check (100 mm extrusion)

(no image — see text)

**Parts:** masking tape, steel rule, caliper, loaded ASA.

**Do:** Heat the hotend to the ASA print temperature (260 °C) and make sure filament is loaded and the extruder is engaged. Klipper's `[extruder] max_extrude_only_distance` defaults to **50 mm**, so a single `G1 E100` errors out with "Extrude only move too long". Pick one:
- **Voron guide way:** extrude 50 mm twice.
- **Ellis way (preferred, slower and more accurate):** add `max_extrude_only_distance: 150` to `[extruder]`, `RESTART`, then extrude once at 1 mm/s: `G1 E100 F60`. Extruding slowly removes the pressure-related error that a fast extrude introduces.

Put a piece of tape on the filament at the **120 mm** mark measured from where the filament enters the extruder. Extrude 100 mm. Measure from the extruder entrance to the tape again — this is the **remaining** distance R, and it should be ≈20 mm. Then:

```
actual_extruded      = 120 − R
new_rotation_distance = old_rotation_distance × (actual_extruded / 100)
```

R is what the rule reads, not the amount extruded — forgetting the subtraction is the classic way to land a rotation distance five times too small.

Iterate without restarting using `SET_EXTRUDER_ROTATION_DISTANCE EXTRUDER=extruder DISTANCE=<value>`, then write the final number into `[extruder] rotation_distance` and `RESTART`. Remember: **a higher value means less filament comes out.** Always use your *current* value in the formula, not the original.

**Check:** Actual extruded amount is within **0.5 %** of target — 99.5 to 100.5 mm for a 100 mm request. Starting value for Clockwork 2 is `rotation_distance: 22.6789511` with `gear_ratio: 50:10`; expect to land within about ±2 % of that. If you are 5 %+ off, you have the wrong `gear_ratio` (50:17 is Clockwork **1**), not a calibration problem. [src](https://docs.vorondesign.com/build/startup/) · [src](https://ellis3dp.com/Print-Tuning-Guide/articles/extruder_calibration.html)

---

## Part D — Chamber and the first real print

### Step 14.8 — Set the chamber target and understand the soak

(no image — see text)

**Parts:** none.

**Do:** There is no chamber heater on this machine — the chamber is heated by the bed and the enclosure. The Voron target to work to is **55–60 °C**, which is the band the printed parts were designed for: "It is common for the chamber temperatures inside an enclosed Voron printer to reach 55–60 ºC." A 350 with a 100–110 °C bed, panels on and the Clicky-Clack door shut will get there passively. Read it off `[temperature_sensor chamber_temp]` in the web UI — that sensor is already wired to the Nitehawk (`nhk:PB2`, T1). Expect **30–45 minutes** from cold to a stable chamber; that is the soak, and it is also what makes `PROBE_ACCURACY` repeatable.

**Check:** With bed at 110 °C, panels on and door closed, `chamber_th` climbs past 45 °C within ~20 minutes and settles in the **50–60 °C accept band** (target 55–60 °C). If it stalls below 45 °C, look for a missing panel, an open keystone blank, or the exhaust left open. [src](https://docs.vorondesign.com/materials.html)

### Step 14.9 — Close Ch 12's `PRINT_START` TODO with the purge line

(no image — see text)

**Parts:** none.

**Do:** `PRINT_START` is owned by **[Ch 12 Step 12.36](12-software.md)** — do not write a second one here. That macro already homes, soaks (chamber sensor or timed), QGLs hot, meshes adaptively and brings the nozzle up, and it ends with a `##  TODO Ch 14: purge / prime line goes here` marker. Now that the extruder is calibrated, replace that marker with:

```ini
    G90
    G1 X5 Y5 Z0.3 F6000                    ; <-- 350 only
    M83                                    ; relative extrusion for the purge
    G92 E0
    G1 X120 E20 F1200                      ; purge line
    G1 Z2 F600
```

`M83` and `G92 E0` are not optional. Klipper starts in **absolute** extrusion mode, and Ch 12's macro does not set `M83`/`G92 E0` until *after* this point — a bare `G1 E20` here would extrude to an arbitrary absolute position instead of 20 mm.

Then set the slicer's start G-code (PrusaSlicer → **Printer Settings → Custom G-code → Start G-code**):

```
PRINT_START BED=[first_layer_bed_temperature] EXTRUDER=[first_layer_temperature] CHAMBER=0
```

**Check:** Run `PRINT_START CHAMBER=0` by hand from the console with the machine cold. It heats the bed, does the timed soak, homes, QGLs, meshes, heats the nozzle, and lays a purge line at X5 → X120 that is continuous and sticks. Nothing in Ch 12's macro has been duplicated or re-declared — `grep -c '^\[gcode_macro PRINT_START\]' printer.cfg` returns **1**.

⚠ **Keep `CHAMBER=0` until Step 14.8 has told you what your chamber actually reaches.** `TEMPERATURE_WAIT` has **no timeout** (Ch 12 Step 12.36): a `CHAMBER=50` the machine never reaches blocks the print forever, and the only way out is cancelling. Once 14.8 gives you a repeatable settled value, set `CHAMBER` a few degrees **below** it — never at or above it. [src](https://www.klipper3d.org/G-Codes.html#temperature_wait)

### Step 14.10 — Fetch the cube you already printed in Ch 13

(no image — see text)

**Parts:** the Voron-printed cube; the Prusa-printed B00 reference cube.

**Do:** The cube is printed **once**, in Ch 13, and Ch 13 is authoritative for it. [Step 13.41](13-initial-startup.md#step-1341-slice-the-voron-cube) slices `Voron_Design_Cube_v7.stl` at 260 °C / 110 °C / chamber 50 °C with XY size compensation and shrinkage compensation both at zero — the same overrides the Prusa profile used, which is what makes the two cubes comparable ([print/00-slicer-setup.md](print/00-slicer-setup.md)). [Step 13.42](13-initial-startup.md#step-1342-print-it-and-set-the-first-layer-squish) prints it, live-adjusts the first layer and commits the squish with `Z_OFFSET_APPLY_ENDSTOP`. Put both cubes on the bench. Re-print only if you have changed a slicer setting since — and then re-run 13.41–13.42 as written, not a variation of them.

**Check:** Two cubes in front of you, both `Voron_Design_Cube_v7`, both in Prusament ASA Galaxy Black. The purge line you just added to `PRINT_START` governs the *next* print — it does not invalidate this cube.

### Step 14.11 — Caliper the cube against the Prusa-printed one

(no image — see text)

**Parts:** both cubes, digital caliper.

**Do:** Measure both cubes at **mid-height** (not across the first layer), X and Y and Z, and record everything in the table below. Same STL, same filament, same nominal settings — the only variables are the two machines.

| Measurement | Nominal | Prusa Core One+ (B00 reference) | Voron 2.4 350 (this print) | Accept | If out |
|---|---|---|---|---|---|
| X, mid-height | 30.00 mm | ______ | ______ | ±0.15 mm | see below |
| Y, mid-height | 30.00 mm | ______ | ______ | ±0.15 mm | see below |
| Z (total height) | 30.00 mm | ______ | ______ | ±0.10 mm | over → first layer under-squished; under → over-squished |
| X at first layer | — | ______ | ______ | within 0.15 mm of mid-height X | elephant-foot compensation wrong; adjust in 0.05 mm steps |
| X − Y (squareness proxy) | 0.00 mm | ______ | ______ | ≤0.10 mm | a persistent X−Y difference on the Voron is a gantry-square problem → Ch 06b |
| Corner snap test | — | pass/fail | pass/fail | must not delaminate along a layer line | chamber too cold or fan too high |

Two honest expectations before you start chasing numbers:

- **Oversize is normal and is not an axis error.** Ellis: 100–101 % X/Y scaling "is about the range you would expect with ABS", and *"don't mess with your `steps_per_mm`/`rotation_distance`. Deviations are almost always from material shrinkage, bulging, layer inconsistencies, etc, NOT issues with your axes."* Fix it with extrusion multiplier at step 14.19, never with XY compensation — negative XY compensation wrecks every bearing fit in the machine. [src](https://ellis3dp.com/Print-Tuning-Guide/articles/extrusion_multiplier.html)
- **A Voron-vs-Prusa difference of ~0.1 mm is chamber, not calibration.** The Voron runs a hotter, more uniform chamber than the Core One+, so its parts shrink slightly differently. Both being *in* tolerance matters more than them matching each other.

**Check:** Both cubes inside tolerance — X and Y within ±0.15 mm and Z within ±0.10 mm of 30.00 mm — and within 0.15 mm of *each other*.

---

## Part E — Input shaper

Now, and not before — the machine has printed successfully, the belts are at final tension, and the frame has been hot.

### Step 14.12 — Bring up the on-board accelerometer

(no image — see text)

**Parts:** none.

**Do:** MainsailOS pre-installs the resonance dependencies (Ch 12 Step 12.2), so there is nothing to install. Verify:

```
~/klippy-env/bin/python -c 'import numpy, matplotlib; print(numpy.__version__)'
```

Only if that fails — i.e. you are on a plain Raspberry Pi OS image rather than MainsailOS — follow Klipper's own installation instructions. Do **not** pin `numpy<1.26`, and do not ask for `libatlas-base-dev`: that package was merged into `libopenblas-dev` in Trixie and no longer exists, and the pinned numpy does not support Trixie's Python — either one can break `klippy-env` and stop Klipper. [src](https://www.klipper3d.org/Measuring_Resonances.html)

Then uncomment the **350 mm** probe point in `[resonance_tester]` — the stock config ships all three build sizes commented out:

```ini
[adxl345]
cs_pin: nhk:PB10
spi_software_sclk_pin: nhk:PA5
spi_software_mosi_pin: nhk:PA2
spi_software_miso_pin: nhk:PA6

[resonance_tester]
accel_chip: adxl345
accel_per_hz: 100
sweeping_accel: 400
sweeping_period: 0
probe_points:
    175, 175, 20
```

`RESTART`, then `ACCELEROMETER_QUERY` and `MEASURE_AXES_NOISE`.

**Check:** `ACCELEROMETER_QUERY` returns three axis values with roughly 9800 (free-fall, mm/s²) on one of them. `MEASURE_AXES_NOISE` returns noise figures **in the ~1–100 range**; 1000 or more means a sensor, power or wiring problem, or a badly imbalanced fan. If you get `Invalid adxl345 id (got xx vs e5)`, run it again immediately — SPI init is flaky on the first attempt; a repeated failure is a real wiring fault. [src](https://www.klipper3d.org/Measuring_Resonances.html)

⚠ Rev D+ / LDO: The accelerometer is **on the Nitehawk-SB V2 board itself**. There is no separate ADXL345 breakout and no printed ADXL mount to fit — the V1 documentation's ADXL mount does not apply to this kit (survey §4.1). The `[adxl345]` pins above are already correct in `leviathan-printer-rev-d-sbv2.cfg`; if yours read `nhk:gpio21/18/20/19` you are on the V1 config.

### Step 14.13 — Run `SHAPER_CALIBRATE`

(no image — see text)

**Parts:** none.

**Do:** `G28` first. Make sure nothing is resting on the gantry and the panels are on. Then:

```
SHAPER_CALIBRATE
```

Both axes run in one pass (the accelerometer is on the toolhead, so this is not a bed-slinger — no re-mounting between axes). It takes a few minutes and is loud. **Do not** `SAVE_CONFIG` yet.

Klipper's own worked example of the output block you should see, one per axis:

```
Fitted shaper 'mzv' frequency = 36.8 Hz (vibrations = 1.7%, smoothing ~= 0.150)
To avoid too much smoothing with 'mzv', suggested max_accel <= 4000 mm/sec^2
...
Recommended shaper_type_y = mzv, shaper_freq_y = 36.8 Hz
```

**Check:** A block per axis, giving fitted frequency, residual vibration %, smoothing and a suggested `max_accel` for each of the five shaper types, ending in a `Recommended shaper_type_x = …, shaper_freq_x = … Hz` line. [src](https://www.klipper3d.org/Measuring_Resonances.html)

### Step 14.14 — Read the graphs

![Klipper shaper calibration chart, X axis](https://raw.githubusercontent.com/Klipper3d/klipper/master/docs/img/calibrate-x.png)

**Parts:** none.

**Do:** Generate the PNGs from the CSVs the run left in `/tmp`:

```
~/klipper/scripts/calibrate_shaper.py /tmp/calibration_data_x_*.csv -o /tmp/shaper_x.png
~/klipper/scripts/calibrate_shaper.py /tmp/calibration_data_y_*.csv -o /tmp/shaper_y.png
```

Read them in this order:
1. **Where is the tallest peak?** That is the dominant resonance and it is what sets `shaper_freq`.
2. **How many big peaks are there, and how far apart?** One clean peak → `mzv` or `zv` and a high `max_accel`. Two or more widely separated peaks → the script will push you to `2hump_ei`/`3hump_ei`, which cost acceleration. Widely separated peaks are usually a *mechanical* message: a loose backer, an under-tensioned belt, a rail bolt in the end hole.
3. **`vibrations = X %`** — residual ringing after shaping. Lower is better; single digits is good.
4. **`smoothing ~= Y`** — how much the shaper blurs fine detail. Higher smoothing forces a lower `max_accel`. The two trade against each other; the script's `max_accel` line is that trade expressed as a number.
5. **Is the plot noise with no peak?** Then you measured nothing — go back to `MEASURE_AXES_NOISE`.

**Check:** What to expect on a 350 2.4 — no official per-model figure exists; what is sourced is the *floor*. Klipper: **"If the measured ringing frequency is very low (below approx 20-25 Hz), it might be a good idea to invest into stiffening the printer or decreasing the moving mass… before proceeding with further input shaping tuning."** In practice a well-built 350 with backers fitted lands both axes in roughly the **35–60 Hz** band, X usually the higher of the two (the toolhead alone is lighter than the whole gantry that Y has to move) — treat that band as community-observed, not a spec. Anything **below 25 Hz on either axis is a build fault, not a tuning result**: stop, and go re-check belt tension, the titanium backers, the XY joints and the frame bolts before you shape over it. [src](https://www.klipper3d.org/Resonance_Compensation.html)

### Step 14.15 — Save the shaper and set the real `max_accel`

(no image — see text)

**Parts:** none.

**Do:** If the recommendations look sane, `SAVE_CONFIG`. That writes `[input_shaper]` with `shaper_type_x/y` and `shaper_freq_x/y`. It does **not** touch `max_accel` — Klipper says so explicitly, and this is the step everyone skips. The LDO config ships:

```ini
[printer]
max_velocity: 300
max_accel: 10000          # placeholder — must come down
max_z_velocity: 15
max_z_accel: 350
square_corner_velocity: 5.0
```

Set `max_accel` to **at or below the lower of the two per-axis suggested values, with margin** — if the run suggested ≤4000 for X and ≤3500 for Y, use 3000–3500. Klipper is blunt that the suggested figure "is by no means a recommendation to set this acceleration for printing"; it is only the ceiling at which that shaper stops smoothing badly, and your real ceiling is also limited by motor torque. Leave `square_corner_velocity` at **5.0** — the calibration script assumed it, and changing it invalidates the `max_accel` numbers.

**Check:** `printer.cfg` bottom block has `[input_shaper]` with four values; `[printer] max_accel` is no longer 10000. Re-print the Voron cube and compare the corners to the first one — that is your before/after. Then walk the machine and check nothing has unscrewed itself: Klipper warns that resonance testing loosens fasteners. [src](https://www.klipper3d.org/Measuring_Resonances.html)

### Step 14.16 — Z-axis shaping and Z limits (optional)

(no image — see text)

**Parts:** none.

**Do:** On a 2.4 the gantry moves in Z, so the toolhead accelerometer can measure Z too — unusual and worth doing if you see Z-direction artefacts. It needs two temporary changes, because the stock Z limits are far below what the test needs:

```ini
[resonance_tester]
accel_chip_z: adxl345

[printer]
max_z_velocity: 20        # temporarily, up from 15
max_z_accel: 1550         # temporarily, up from 350
```

`RESTART`, run `SHAPER_CALIBRATE AXIS=Z`, `SAVE_CONFIG` if you like the result (it writes `shaper_type_z` / `shaper_freq_z`), then **put `max_z_velocity` and `max_z_accel` back to 15 and 350.**

**Check:** The two Z limits read 15 and 350 again after you are done. These are belt-and-driver limits for a four-motor belted Z, not resonance limits — leaving them at 20/1550 for normal printing is not a tuning gain, it is a way to skip Z steps. Klipper's own instruction is "only for the duration of the test". If you skip this whole step, nothing downstream breaks. [src](https://www.klipper3d.org/Measuring_Resonances.html)

---

## Part F — Pressure advance and flow

### Step 14.17 — Generate and print the Ellis PA pattern

(no image — the pattern and an annotated example are on [Ellis' Pattern Method page](https://ellis3dp.com/Print-Tuning-Guide/articles/pressure_linear_advance/pattern_method.html))

**Parts:** ASA, ~15 g.

**Do:** Open **[ellis3dp.com/Pressure_Linear_Advance_Tool/](https://ellis3dp.com/Pressure_Linear_Advance_Tool/)** and fill it in like a slicer: nozzle 0.4, layer 0.2, ASA temps 260/110, and — critically — **enable the acceleration-control option and set it to your external-perimeter acceleration**, not your new `max_accel`. If you leave it at the machine maximum the pattern will ring and the result is worthless. Sweep **PA 0 to 0.10 in 0.005 steps** as a first pass. Print the generated G-code.

**Check:** Pattern prints cleanly with visible, distinct corner tests across the full sweep. If the extremes of your sweep both look equally bad, widen the range and re-run rather than guessing. [src](https://ellis3dp.com/Print-Tuning-Guide/articles/pressure_linear_advance/pattern_method.html)

### Step 14.18 — Read the pattern and save the value

(no image — see text)

**Parts:** caliper not needed; good light and, ideally, a loupe.

**Do:** Look for the **sharpest corner with the fewest artefacts** — no gaps, no bulges, no divots. Imagine holding a machinist's square over each corner. There is rarely a perfect value; get as close as you can. Ellis leans **higher**: if the sharpest corner has a tiny bit of gapping, still take it. Once you have a range, re-run at 0.001–0.002 intervals to refine (direct drive is that sensitive). Save it per-filament rather than globally, since PA changes with material and brand — put this in the PrusaSlicer **filament** custom G-code for ASA:

```
SET_PRESSURE_ADVANCE ADVANCE=<your value>
```

Or set `[extruder] pressure_advance:` if you only ever print ASA on this machine.

**Check:** Where you should land — the LDO config's own commented starting point is `#pressure_advance: 0.05`, and Klipper documents typical values as "between 0.050 and 1.000 (the high end usually only with bowden extruders)". For a **direct-drive Clockwork 2 with a Revo HF and a 0.4 nozzle in ASA, expect the bottom of that band — roughly 0.02 to 0.05.** No vendor publishes a Revo-HF-specific number; treat 0.04 as the place to start looking and let the pattern decide. If you cannot get a clean corner at *any* value, or you see gapping and bulging simultaneously, stop tuning — Ellis: *"you likely have extruder issues."* Check the CW2 for backlash: with the toolhead cold, reverse the extruder gear direction by hand and feel for a dead zone. [src](https://ellis3dp.com/Print-Tuning-Guide/articles/pressure_linear_advance/saving.html) · [src](https://www.klipper3d.org/Pressure_Advance.html)

### Step 14.19 — Extrusion multiplier / flow: the 2 % pass

(no image — see text)

**Parts:** ASA, ~25 g.

**Do:** Print Ellis' **30 × 30 × 3 mm** test cubes (in his [`test_prints`](https://github.com/AndrewEllis93/Print-Tuning-Guide/tree/main/test_prints) folder) in a row, each at a different EM: **92, 94, 96, 98 %**. Slice with top-layer line width 100 %, infill 30 %+, top solid infill speed moderate (~60 mm/s), and your normal fan setting. In PrusaSlicer, right-click each object → add settings → **Extrusion multiplier** to vary them on one plate.

**Check:** Judge the **centre** of each top surface, not the edges — edges always look over-extruded. Too low: visible gaps/valleys between the top lines when held toward a light. Too high: pellets, ridging, a rough raised surface. Most filaments land in the 92–98 % window; Prusament ASA is not exotic and should. [src](https://ellis3dp.com/Print-Tuning-Guide/articles/extrusion_multiplier.html)

### Step 14.20 — The 0.5 % refinement pass

(no image — see text)

**Parts:** ASA, ~25 g.

**Do:** Take the winner from 14.19 and print four more cubes at ±0.5 % and ±1.0 % around it. Pick the smoothest centre. Write that number into the **filament** profile's extrusion multiplier, not the print profile — it is a material property.

**Check:** Chosen cube has a uniformly smooth top with no gaps and no ridging. Then re-caliper it: this is also the lever that fixes an oversize Voron cube from step 14.11 — 1 % of EM is worth roughly 0.1 mm on a 30 mm face. If the cube is now in tolerance, you fixed it the right way.

### Step 14.21 — Re-check first-layer squish, because EM moved

(no image — see text)

**Parts:** none.

**Do:** Extrusion multiplier changes how much plastic the first layer puts down, so the squish you set at [Ch 13 Step 13.42](13-initial-startup.md#step-1342-print-it-and-set-the-first-layer-squish) is now slightly wrong. Print one more cube (or any wide flat part) and repeat that live-Z procedure. Save with `Z_OFFSET_APPLY_ENDSTOP` + `SAVE_CONFIG`.

**Check:** Bottom surface is smooth, lines still individually visible, no gaps. This is the last step of the "essentials" loop — Ellis' order is extruder → surface prep → first layer → PA → EM, and EM feeding back into first layer is expected, not a mistake.

---

## Part G — Ongoing

### Step 14.22 — Bed mesh variance, and a backup

(no image — [heightmap example](https://raw.githubusercontent.com/VoronDesign/Voron-Documentation/master/tuning/images/heightmap_variance.png))

**Parts:** none.

**Do:** With the machine fully heat-soaked and QGL'd, run `BED_MESH_CALIBRATE` and open the Heightmap (Mainsail) / Tuning (Fluidd) tab. Read the **Variance** number, not the colours — the preview exaggerates deviation wildly. Under ~0.05 mm total variance and a mesh is optional; keep generating one per print anyway (it is already in your `PRINT_START`) because the variance changes with chamber temperature as the gantry extrusions bend. Confirm `zero_reference_position: 175,175` is set — a V2 on the stock Z endstop **must** have it, or the mesh floats away from Z0.

Then back up. Copy `printer.cfg`, `moonraker.conf` and the `printer.cfg` auto-save block off the Pi — everything you have generated in this chapter lives in that one file.

**Check:** Heightmap sits centred around Z0 (not offset up or down as a whole), variance recorded in the tuning log, config copied somewhere that is not the Pi's SD card. [src](https://docs.vorondesign.com/tuning/secondary_printer_tuning.html)

### Step 14.23 — Hand off to Ellis for everything after this

(no image — see text)

**Parts:** none.

**Do:** [**Ellis' Print Tuning Guide**](https://ellis3dp.com/Print-Tuning-Guide/) is the ongoing reference from here. Work his **Tuning** section in his order — the numbering is his, and each step assumes the ones above it:

| # | Section | Status after this chapter |
|---|---|---|
| 1 | [Extruder Calibration](https://ellis3dp.com/Print-Tuning-Guide/articles/extruder_calibration.html) | done — step 14.7 |
| 2 | [Build Surface Preparation & Handling](https://ellis3dp.com/Print-Tuning-Guide/articles/build_surface_prep_handling.html) | read it — smooth PEI + ASA needs no glue, but it needs to be clean |
| 3 | [First Layer Squish](https://ellis3dp.com/Print-Tuning-Guide/articles/first_layer_squish.html) | done — Ch 13 step 13.42, then step 14.21 |
| 4 | [Pressure Advance / Linear Advance](https://ellis3dp.com/Print-Tuning-Guide/articles/index_pressure_advance.html) | done — steps 14.17, 14.18 |
| 5 | [Extrusion Multiplier](https://ellis3dp.com/Print-Tuning-Guide/articles/extrusion_multiplier.html) | done — steps 14.19, 14.20 |
| 6 | [PA / EM Oddities](https://ellis3dp.com/Print-Tuning-Guide/articles/pa_em_oddities.html) | read when a result won't converge |
| 7 | [Cooling and Layer Times](https://ellis3dp.com/Print-Tuning-Guide/articles/cooling_and_layer_times.html) | **next** — the ASA-specific one; minimum layer times matter more than fan % in a hot chamber |
| 8 | [Retraction](https://ellis3dp.com/Print-Tuning-Guide/articles/retraction.html) | **next** — CW2 is direct drive, expect a small value |
| 9 | [Infill/Perimeter Overlap](https://ellis3dp.com/Print-Tuning-Guide/articles/infill_perimeter_overlap.html) | later |
| 10 | [Stepover](https://ellis3dp.com/Print-Tuning-Guide/articles/stepover.html) | later |

Beyond that, his **Advanced Tuning** section covers [Maximum Volumetric Flow Rate](https://ellis3dp.com/Print-Tuning-Guide/articles/determining_max_volumetric_flow_rate.html) (worth doing — the Revo HF's whole point is flow) and [Maximum Speeds and Accelerations](https://ellis3dp.com/Print-Tuning-Guide/articles/determining_max_speeds_accels.html), and his [Troubleshooting](https://ellis3dp.com/Print-Tuning-Guide/articles/index_troubleshooting.html) index is the fastest way to name a defect you are looking at.

**Check:** Cooling/layer times and retraction are on the list for the next session, with the tuning log ready to record them.

---

## Tuning log

Fill this in as you go — one row per change, both of you initialling. This is the record that makes the next tuning session cheap, and the thing you check first when a print goes wrong three months from now.

| Date | What | Value set | How measured | Result / notes | By |
|---|---|---|---|---|---|
| | Bed PID @ 100 °C | Kp ___ Ki ___ Kd ___ | `PID_CALIBRATE` + `SAVE_CONFIG` | holds ±___ °C | |
| | Hotend PID @ 245 °C | Kp ___ Ki ___ Kd ___ | `PID_CALIBRATE`, fans 25 % | holds ±___ °C | |
| | A belt tension | ___ Hz | 150 mm span, ___ app | | |
| | B belt tension | ___ Hz | 150 mm span, ___ app | | |
| | Z belts (4) | ___ / ___ / ___ / ___ Hz | 150 mm from Z idler centres | | |
| | `PROBE_ACCURACY` σ | ___ mm | hot, soaked ___ min | target < 0.003 | |
| | `rotation_distance` | ______ | 100 mm extrude, actual ___ mm | within 0.5 %? | |
| | Chamber soak | ___ °C in ___ min | `chamber_th`, panels + door on | | |
| | Cube X / Y / Z (Voron) | ___ / ___ / ___ mm | caliper, mid-height | vs Prusa: ___ / ___ / ___ | |
| | `shaper_type_x` / freq | ______ / ___ Hz | `SHAPER_CALIBRATE` | vibrations ___ %, smoothing ___ | |
| | `shaper_type_y` / freq | ______ / ___ Hz | `SHAPER_CALIBRATE` | vibrations ___ %, smoothing ___ | |
| | `max_accel` | ______ mm/s² | lower of the two suggestions, minus margin | | |
| | Pressure advance (ASA) | ______ | Ellis pattern, ___ to ___ step ___ | | |
| | Extrusion multiplier (ASA) | ___ % | Ellis 30×30×3 cubes | cube X now ___ mm | |
| | Z offset (final) | `position_endstop` ______ | `Z_OFFSET_APPLY_ENDSTOP` | | |
| | Bed mesh variance | ___ mm | `BED_MESH_CALIBRATE`, hot | | |
| | | | | | |

---

## Checkpoint 14

- [ ] Bed and hotend PID tuned in Ch 13 and `SAVE_CONFIG`'d; both hold within ±0.5 °C at setpoint
- [ ] A and B belts both at ~110 Hz over a measured 150 mm span, equal to each other after moving the gantry and returning
- [ ] All four Z belts at ~140 Hz over a measured 150 mm span, even with each other
- [ ] `QUAD_GANTRY_LEVEL` converges in ≤3 retries hot; `PROBE_ACCURACY` σ < 0.003 mm with no trend
- [ ] `rotation_distance` verified: 100 mm requested measures 99.5–100.5 mm
- [ ] `PRINT_START` (Ch 12 Step 12.36, with Step 14.9's purge line) heats, soaks, homes, QGLs, meshes and purges — tested standalone from the console with `CHAMBER=0`
- [ ] Chamber reaches the 50–60 °C band with panels and door closed
- [ ] Voron cube (printed in Ch 13) calipered; X, Y within ±0.15 mm and Z within ±0.10 mm of 30.00 mm
- [ ] Both cubes (Prusa and Voron) measured into the comparison table
- [ ] `MEASURE_AXES_NOISE` in the 1–100 range; `[resonance_tester] probe_points: 175, 175, 20` uncommented
- [ ] `[input_shaper]` saved for X and Y; neither axis below 25 Hz
- [ ] `[printer] max_accel` reduced from the stock 10000 to at or below the calibration's suggestion, with margin
- [ ] `max_z_velocity: 15` / `max_z_accel: 350` restored if Z shaping was attempted
- [ ] Pressure advance set per-filament for ASA and recorded
- [ ] Extrusion multiplier set in the ASA filament profile and recorded
- [ ] First-layer squish re-checked *after* the EM change and saved with `Z_OFFSET_APPLY_ENDSTOP`
- [ ] Every fastener the shaper run could have loosened re-checked
- [ ] `printer.cfg` backed up off the Pi
- [ ] Tuning log filled in, with initials

## Common mistakes

- **Tensioning belts before Ch 06b squaring.** The squaring procedure begins by fully releasing A/B tension; anything set before it is thrown away, and you will have done the work twice (survey §5.2 W1).
- **Reading a belt frequency without measuring the span.** 110 Hz is only meaningful at 150 mm. Eyeballing the span is the single most common way people end up with belts 30 % out and blame the printer.
- **Running `SHAPER_CALIBRATE` before the first successful print, or before final belt tension.** Both change the resonances you just measured, so the result is stale before you use it. Same for pressure advance, which also shifts when input shaping is switched on.
- **`SAVE_CONFIG` after the shaper run and stopping there.** It writes `[input_shaper]` but explicitly does *not* touch `max_accel`. Leaving the stock `max_accel: 10000` means you shaped the ringing and then printed at an acceleration that reintroduces it.
- **Fixing an oversize cube with negative XY size compensation.** It makes every bearing bore and screw hole in the machine oversize. Use extrusion multiplier (step 14.19), which is what actually changed.
- **PID-tuning the hotend at 260 °C with `max_temp: 270`.** The calibration overshoots and trips the limit mid-run. Tune at 245, or raise `max_temp` to 290 first.
- **Raising `[heater_bed] max_power` above 0.6 to speed up warm-up.** LDO set it to protect a 355 mm cast plate from warping. Wait the extra five minutes.
- **Skipping the heat soak because the bed says 110 °C.** The bed reaches temperature in minutes; the *frame* takes 30–45. Probing a cold frame gives a mesh and a Z offset that are wrong for every print you then run.

## Next

The machine is tuned. Print something for the machine itself — a nozzle brush, a spool holder, the Clicky-Clack spares — and then work Ellis' sections 7 and 8 (cooling/layer times, retraction) as your first real tuning session on ASA.
