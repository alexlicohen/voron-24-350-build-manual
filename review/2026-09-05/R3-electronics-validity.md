# R3 — Validity of chapters 08–14 against the live sources

### F1 · BLOCKER · docs/manual/08-toolhead.md:66 and :987
Claim in doc: "E3D Revo Hotend (HF), Revo Voron form factor | 1 | **40 W**, 300 °C max…" / "A **40 W** 24 V Revo cartridge is roughly **14 Ω**"
Source checked: LDO 350 Rev D BOM ships "E3D Revo Hotend (HF)"; the HF (High Flow) hotside kit is the **LDO Edition 60 W HeaterCore** (west3d/e3d listings); the manual's own 12-software.md:815/830 and 14-calibration.md:55/71 both say **60 W**.
Problem: wrong wattage, and the only pre-power-on heater acceptance value in the manual is derived from it — 24²/60 = **9.6 Ω**, not 14.4 Ω.
Fix: line 66 → "60 W, 300 °C max, Semitec 104NT-4-R025H42G"; line 987 → "A 60 W 24 V Revo HF cartridge is roughly **9.6 Ω**".

### F2 · BLOCKER · docs/manual/08-toolhead.md:610 (Step 08.42)
Claim in doc: "Drop the trimmed blower into the **lower cavity** so its outlet feeds the ducts"
Source checked: Stealthburner Assembly Manual p.56 (PART COOLING FAN) shows the 5015 dropping into the **upper** cavity, above the already-clipped 4010; docs.vorondesign.com/build/startup "Verify fans": "On Stealthburner, this [part cooling] is the **TOP** fan… [hotend fan] this is the **BOTTOM** fan".
Problem: wrong cavity — sends the builder to force the 5015 into the 4010's pocket, and contradicts this manual's own 13-initial-startup.md:162/175.
Fix: "Drop the trimmed blower into the **upper** cavity, above the hotend fan you just clipped in, so its outlet feeds the ducts…"

### F3 · BLOCKER · docs/manual/14-calibration.md:254–259 (Step 14.12)
Claim in doc: "Install the measurement dependencies on the Pi (they are not part of a stock Klipper install): `sudo apt install python3-numpy python3-matplotlib libatlas-base-dev libopenblas-dev` / `~/klippy-env/bin/pip install -v "numpy<1.26"`"
Source checked: MainsailOS `modules/generic/50-klipper` — "libatlas-base-dev was merged into libopenblas-dev in Trixie and is **no longer available**" and "Normally klipper would use `numpy<1.26`, but that version **does not support**…" → it installs plain `numpy`; MainsailOS 3.0.0 (2026-05-06) is Trixie-based and already installs numpy/matplotlib/openblas + numpy in klippy-env.
Problem: on the OS Ch 12.2 mandates the apt line aborts (package removed in Trixie) and the pip line downgrades numpy to a build that does not support Trixie's Python — it can break `klippy-env` and stop Klipper; it is also redundant, and it contradicts 12-software.md:67 ("input-shaper Python dependencies pre-installed").
Fix: replace the block with "MainsailOS already installs these. Verify with `~/klippy-env/bin/python -c 'import numpy, matplotlib; print(numpy.__version__)'`. Only if that fails: `sudo apt install python3-numpy python3-matplotlib libopenblas-dev` — do **not** pin `numpy<1.26` on Trixie."

### F4 · BLOCKER · docs/manual/13-initial-startup.md:64 (Step 13.2)
Claim in doc: "Confirm **all** Leviathan voltage-selection jumpers are back in and set for the parts actually attached."
Source checked: 10-wiring.md:493/495 and Checkpoint 10 — "Exactly two jumpers on the board, both on the 24 V pins, on Fan2 and Fan3… Leave Fan0, Fan1 and Probe bare"; LDO Leviathan V1.3 guide: "Mixing voltage will permanantly damage the controller and attached components"; Leviathan README confirms 4 fan ports + 1 probe port = 5 selectors.
Problem: at the moment of first power-on the manual contradicts its own hardware-destroying-mistake rule and invites five jumpers where only two belong.
Fix: "Confirm exactly **two** voltage-selection jumpers are fitted — Fan2 and Fan3, both at 24 V — and that Probe, Fan0 and Fan1 are still bare (step 10.28)."

### F5 · MAJOR · docs/manual/13-initial-startup.md:196 and :198 (Step 13.11)
Claim in doc: "the Nevermore fan runs (`FAN3/PF9`, `heater_temp: 60`)… the LDO config names `FAN3/PF9` `[heater_fan exhaust_fan]`"
Source checked: 12-software.md:913 replaces that section with `[fan_generic nevermore]` (no `heater`/`heater_temp`), and Checkpoint 12 requires `grep -c '^\[heater_fan exhaust_fan\]'` = 0.
Problem: after the Ch 12 edit the Nevermore fan will **not** start at bed 60 °C, so this verification step fails on a correctly built machine and sends the builder hunting a non-existent wiring fault.
Fix: "Send `SET_FAN_SPEED FAN=nevermore SPEED=1` and confirm the Nevermore fan runs, then `SPEED=0`. (Ch 12 replaced LDO's `[heater_fan exhaust_fan]` with `[fan_generic nevermore]`, so it is no longer slaved to the bed.)"

### F6 · MAJOR · docs/manual/12-software.md:181, :207, :209
Claim in doc: `[src](https://klipperscreen.dev/Installation.html)`, `.../Troubleshooting/Rotation.html`, `.../Troubleshooting/Touch_issues.html`
Source checked: `klipperscreen.dev` returns NXDOMAIN (dead domain); the live docs are at klipperscreen.github.io/KlipperScreen/ — `/Installation/`, `/Troubleshooting/Rotation/`, `/Troubleshooting/Touch_issues/` all HTTP 200. (Content verified: the Rotation page does prescribe `/boot/firmware/cmdline.txt` with `video=DSI-1:800x480@60,rotate=90`, values 0/90/180/270 — so step 12.10's method is right, only the link is dead.)
Problem: three of the manual's citations are unreachable; these are the only three non-200 URLs in chapters 08–14.
Fix: `https://klipperscreen.github.io/KlipperScreen/Installation/`, `.../Troubleshooting/Rotation/`, `.../Troubleshooting/Touch_issues/`

### F7 · MAJOR · docs/manual/10-wiring.md:924 (also 10-wiring.md:1313, 13-initial-startup.md:184, :796)
Claim in doc: "The board-to-board interface … is a **2×10 header** on V2 (V1 used 2×4)"
Source checked: `Nitehawk-SB-V2/Images/nhsbv2_pcb_pinout.jpg` shows the Fan/RGB port as 2 columns × 5 rows (PD1 A1|A2 PD2, PA15 HEF|PCF PD0, PD3 RGB|5V, GND|NC, NC|24V) and `sbv2_fan_adapter_pcb_pinout.jpg` shows P1 as a physical 2×5 header — 10 pins. LDO's doc table wording "2x10 M-Header" means 10 pins, not 20.
Problem: wrong header size, and it contradicts this manual's own 08-toolhead.md:626/939 ("10-pin, 2×5"). "V1 used 2×4" is correct (Rev D wiring guide: "The 2x4 headers on the two PCBs connect to each other").
Fix: everywhere → "a **2×5 (10-pin)** header on V2 (V1 used 2×4)".

### F8 · MAJOR · docs/manual/13-initial-startup.md:104 and :827
Claim in doc: "one `usb-Klipper_stmf446xx_…` (Leviathan)" / "both MCUs are present — `stmf446xx` and `stm32g0b1xx`"
Source checked: LDO Leviathan V1.2 setup guide prints `usb-Klipper_stm32f446xx_<id>` and `ID 1d50:6177 OpenMoko, Inc. stm32f446xx`; 12-software.md:255 already flags this — "the guide writes the mainboard string as `stmf446xx`; the actual Klipper string is `stm32f446xx`".
Problem: Ch 13 propagates the exact typo Ch 12 warns about; a builder grepping `stmf446xx` finds nothing and thinks the mainboard did not enumerate.
Fix: both lines → `stm32f446xx` (or `stm32h743xx` on a V1.3 board).

### F9 · MAJOR · docs/manual/13-initial-startup.md:675–698 (Step 13.38) vs 12-software.md:985–1002
Claim in doc: 13.38 "Confirm the section you added in Ch 12, or add it now:" then `speed: 100 / mesh_min: 35,35 / mesh_max: 315,315 / fade_start: 0.6` — Ch 12.34 gives `speed: 300 / mesh_min: 30,30 / mesh_max: 320,320 / fade_start: 1.0 / fade_target: 0 / adaptive_margin: 5`.
Source checked: docs.vorondesign.com/tuning/secondary_printer_tuning.html sample for a 350: `speed: 300, horizontal_move_z: 10, mesh_min: 40,40, mesh_max: 310,310, zero_reference_position: 175,175, fade_start: 0.6, fade_end: 10.0, probe_count: 5,5, algorithm: bicubic`.
Problem: two different `[bed_mesh]` blocks for the same machine, and "confirm" cannot succeed; both are also wider than Voron's 40/310 inset, pushing probe points 5–10 mm nearer the plate edge and the bed clips.
Fix: make 13.38 a pointer only ("confirm the block from step 12.34; do not retype it") and align 12.34 to Voron's inset — `mesh_min: 40, 40` / `mesh_max: 310, 310`, keeping `probe_count: 7, 7`, `zero_reference_position: 175, 175`.

### F10 · MAJOR · docs/manual/14-calibration.md:173–200 (Step 14.9) vs 12-software.md:1056–1109
Claim in doc: 14.9 "The stock LDO `PRINT_START` is a three-line stub… Replace it." then `{% set CHAMBER = params.CHAMBER|default(50)|float %}` … `G1 X120 E20 F1200 ; purge line`, and a slicer call hardcoding `CHAMBER=50`.
Source checked: 12-software.md:1113 already replaced PRINT_START and warns "**`TEMPERATURE_WAIT` has no timeout**… Keep `CHAMBER=0` (timed soak) until you have measured what your chamber actually reaches"; Klipper G-Codes: `TEMPERATURE_WAIT` blocks indefinitely.
Problem: a second, incompatible PRINT_START that silently reverses Ch 12's safety default (a chamber that never reaches 50 °C hangs the print with no way out but cancel); the purge line also has no `G92 E0`/`M83` before `G1 E20`, so in Klipper's default absolute-E mode it extrudes an arbitrary amount.
Fix: delete the macro from 14.9 and point to step 12.36 ("PRINT_START is owned by Ch 12; here you only add the purge/prime line and set `CHAMBER` once you have measured the soak"), and prefix the purge with `M83` + `G92 E0`.

### F11 · MAJOR · docs/manual/09-electronics-bay.md:54 and :422 (Step 09.25) vs 08-toolhead.md:961 (Step 08.66)
Claim in doc: 09.25 builds the USB-adapter stack with "M2×10 self-tapping **(verify on bench)**"; 08.66 builds the same stack with "M3×10 SHCS ×3" and says "Bag the assembly for Ch 09".
Source checked: LDO Rev D Printed Parts Guide, "Nitehawk Adapter PCB Cover": "Use **3 M3x10 SHCS screws** to attach the base, adapter PCB, and cover together." (The M2×10 self-tappers are for the DIN clips only.)
Problem: the same sub-assembly is built twice with contradictory fasteners, and the published spec is marked "(verify on bench)" as if unknown; M2 self-tappers in an M3 hole will not hold the stack.
Fix: 09.25 → "Parts: … DIN Clip ×1 + M2×10 self-tapping ×2 (clip only), **M3×10 SHCS ×3** (base + PCB + cover)"; and make 09.25 a "confirm the assembly from 08.66" step rather than a rebuild.

### F12 · MAJOR · docs/manual/13-initial-startup.md:130 (Step 13.6)
Claim in doc: "all three are `ATC Semitec 104NT-4-R025H42G` with `pullup_resistor: 2200` in the LDO config"
Source checked: `leviathan-printer-rev-d-sbv2.cfg` — `[extruder]` and `[heater_bed]` carry `pullup_resistor: 2200`, but `[temperature_sensor chamber_temp]` has **no** `pullup_resistor` line (Klipper default 4700); LDO's V2 board doc: "Chamber Thermistor … Uses a **4.7 kΩ** pull up resistor". The manual's own 12-software.md:869 states this correctly.
Problem: a builder chasing a wrong chamber reading will add `pullup_resistor: 2200` to `chamber_temp` and make it much worse.
Fix: "…extruder and bed are `ATC Semitec 104NT-4-R025H42G` with `pullup_resistor: 2200`; the chamber sensor is on the toolboard's CT port, which has a **4.7 kΩ** pull-up, so its section carries no `pullup_resistor` line."

### F13 · MAJOR · docs/manual/11-skirts-panels-door.md:267 (Step 11.8)
Claim in doc: "Screen rotation (`display_lcd_rotate=2` plus the `rpi-ft5406` overlay) is a **Ch 12** software step"
Source checked: 12-software.md:207 — "That is the **legacy fake-KMS path**… on MainsailOS 3.x… `display_lcd_rotate` does nothing. Use the `cmdline.txt` method"; KlipperScreen Troubleshooting/Rotation confirms `display_lcd_rotate=2` is the legacy `vc4-fkms-v3d` path.
Problem: Ch 11 names the exact method Ch 12 rejects, so a builder who reads Ch 11 first edits `/boot/config.txt` on a KMS system and gets nothing.
Fix: "Screen rotation is a **Ch 12** software step (step 12.10 — the `/boot/firmware/cmdline.txt` `video=DSI-1:…rotate=` method, **not** `display_lcd_rotate`)."

### F14 · MINOR · docs/manual/12-software.md:765 (Step 12.29)
Claim in doc: "`##  Connected to Z-PROBE on the Nitehawk-SB V2`"
Source checked: the Nitehawk-SB V2 port is silkscreened **PROBE** (LDO V2 doc port table and `nhsbv2_pcb_pinout.jpg`); `Z-PROBE` is the *Leviathan* header, which 10-wiring.md:771 says must stay empty for the whole build, and 10-wiring.md:773 explicitly calls the stock "Connected to Z-PROBE" comment stale.
Problem: the rewritten block reintroduces the exact wrong port name the manual elsewhere corrects.
Fix: "`##  Connected to PROBE on the Nitehawk-SB V2 (the Leviathan's Z-PROBE header stays empty)`"

### F15 · MINOR · docs/manual/10-wiring.md:974 (Step 10.59)
Claim in doc: "the kit ships **2-hole** chain ends — print `*_2hole` variants, never `*_3hole`. [src](https://docs.ldomotors.com/guides/cable_chain_guide)"
Source checked: that page (fetched in full) covers sizing, latches and end links and says nothing about hole patterns. The claim *is* published, in the Rev D Printed Parts Guide: "Our cable chain ends use the 2 hole configuration… always use the `2hole` version instead of `3hole`".
Problem: correct fact, wrong citation.
Fix: `[src](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d)`

### F16 · MINOR · docs/manual/10-wiring.md:905–909 (Step 10.55, "Rev D wiring guide says" column)
Claim in doc: the Rev D wiring guide says `PROBE` = "JST-XH2.5 3P" and `Endstop` = "JST-XH2.5".
Source checked: the Rev D wiring guide names JST-XH2.5 only for the hotend thermistor ("The connector type to use is JST-XH2.5 two pin"); it specifies nothing for PROBE and nothing for the endstop port (it only says "The endstop port isn't used in a standard Rev D build"). For the SB fans it actually says JST-PH2.0.
Problem: the comparison table attributes two statements to a source that does not make them.
Fix: change those two cells to "not specified" and keep the `TH0` row as the one real conflict.

### F17 · MINOR · docs/manual/10-wiring.md:234 (Step 10.11)
Claim in doc: "Land the free end in a spare port of the brown **L** WAGO. Land the **TO SSR** end on SSR terminal **LOAD 2**."
Source checked: LDO Rev D wiring guide, Connecting 24V: "Connect the **To SSR** end of the SSR to Wago cable to a **brown wago slot** and the other end to **LOAD 2** on the SSR."
Problem: the chapter silently reverses LDO's (self-contradictory) label wording; a builder cross-checking the two will stop and doubt the step.
Fix: keep the chapter's physically sensible instruction but add: "(LDO's text swaps the two labels; go by the connector type — the ferruled end belongs in the SSR screw terminal.)"

### F18 · MINOR · docs/manual/14-calibration.md:143 (Step 14.7)
Claim in doc: "Put a piece of tape on the filament at the **120 mm** mark… Extrude 100 mm. Measure from the extruder entrance to the tape again. Then: `new_rotation_distance = old_rotation_distance × (actual_extruded / 100)`"
Source checked: ellis3dp.com Extruder Calibration — the measured value is the *remaining* distance; `actual_extruded = 120 − remaining`.
Problem: the subtraction is never stated, so `actual_extruded` can be read as the number just measured.
Fix: add "…measure the remaining distance R (should be ≈20 mm). `actual_extruded = 120 − R`."

### F19 · MINOR · docs/manual/13-initial-startup.md, Part D vs the chapter's stated wizard order
Claim in doc: chapter scope line and 12-software.md:1168 both give the order "…XY endstop → homing → bed locating → 0,0 → Z endstop → **probe** → PID…", but the body runs `QUERY_PROBE` at Step 13.21, before homing.
Source checked: `Voron-Documentation/build/startup/buttons.js` — `v2pagename = Start, Information, Verify Temperatures, Verify Heaters, Verify Fans, Motor Checks, XY Endstop Check, Homing Check, Bed Locating, 0 Point, Z Endstop, Probe Check, PID Tuning, Quad Gantry Level, Initial Setup, Finish Line` (16 pages).
Problem: the stated order is right; the body's probe step sits five pages early, so the "in the wizard's own order" claim is not quite true.
Fix: either move 13.21 to sit after 13.26, or note at 13.21 "(brought forward from the wizard's Probe Check page — safe here because the gantry is high and nothing is homed)".

### F20 · MINOR · docs/manual/08-toolhead.md:63 and :204
Claim in doc: "Bondtech **IGDA** gear set"
Source checked: LDO 350 Rev D BOM line reads "Bondtech **IDGA** Gear Set".
Problem: transposed letters against the BOM the builder is ticking off.
Fix: "Bondtech IDGA gear set".

---

## Verified OK

Pin/port/connector claims — all checked against `leviathan-printer-rev-d-sbv2.cfg`, LDO's V2 board doc and LDO's own pinout images; **no wrong pin or port found**:
- Stepper map A→HV-STEPPER-1 (rear right), B→HV-STEPPER-0 (rear left), Z0..Z3→STEPPER-0..3 (FL/RL/RR/FR), STEPPER-4 unused — exact match to the Rev D wiring guide table and the config's own section comments.
- Bed thermistor on `TH1`/`PA2`; bed heater `HEATBED`/`PG11`; nozzle probe on `Z-ENDSTOP`; Leviathan `Z-PROBE` left empty; inductive probe on the toolboard `PROBE` = `nhk:PC15`; chamber on toolboard `CT` = `nhk:PB2`.
- `FAN2`/`PF7` PCB fan, `FAN3`/`PF9` filter fan, `LED-Strip`/`PE6` — exact match to the wiring guide's fan table.
- Toolboard: `HE0`/PA7 + E0508 ferrule, `TH0`/PB12 JST-PH2.0 2P with 2.2 kΩ pull-up, `PROBE` JST-PH2.0 3P GND/SIG/24V, `CT` JST-PH2.0 2P/PB2, XY Endstop JST-PH2.0 4P GND/PB0/PB1/5V, I2C PB3/PB4, USB expansion JST-ZH1.5 5P, `E MOTOR` JST-XH2.5 4P B2 B1 A1 A2 on the reverse side, XT30(2+2) D+/D−/GND/24V, ACT LED PC6.
- Fan-adapter port map P2 = 4010 hotend (`+ / A1 / −`), P3 = neopixel (`5V / GND / RGB`), P4 = 5015 part cooling (`− / A2 / +`) — matches the LDO V2 pinout image silkscreen exactly, including P4's reversed order.
- Step 08.46's documented source conflict is real: `nhsbv2_pcb_pinout.jpg` labels PA15→HEF / PD0→PCF, while the fan-adapter silkscreen (PCF PA15 / HEF PD0), LDO's port table and the config all say the opposite. "Wire by function, fix in software" is the right call.
- Umbilical: Amass XT30(2+2)-F partially-overmolded (the variant LDO ships with Voron kits), Micro-Fit 3.0 at the bay, 28 mm bend radius, 105 °C max, "never plug or unplug when powered", zip-tie both ends of every chain.

Firmware / config:
- Nitehawk V2 menuconfig (STM32G0B1 / 8KiB bootloader / 12 MHz crystal / USB PA11-PA12 / "step on both edges" / `!PC6`) — pixel-exact against `make_menuconfig.png`; Katapult block exact against `katapult_menuconfig.png` (PC6 status LED, 8KiB offset).
- Leviathan F446 row (STM32F446 / 12 MHz / **32 KiB**) exact against ldomotion.com VORON-Leviathan-V12; H743 row (25 MHz / **128 KiB**) exact against the V1.3 guide; `ID 1d50:6177 OpenMoko … stm32f446xx` and the DFU `mass-erase:force` command both verbatim.
- Ch 12.13's "LDO's own documents conflict" framing is current: the Leviathan repo README now reads STM32H743 while the Rev D wiring guide and the kit config header say F446/V1.1.
- `leviathan-printer-rev-d.cfg` really does use `nhk:gpio23` and a `[temperature_sensor nh_temp]` on `nhk:gpio26` — the "grep for `nhk:PB8`" test works.
- Klipper `configfile.py` uses `RawConfigParser(strict=False, …)`, so the duplicate `value:` in LDO's `[output_pin caselight]` is silently accepted and the last (`1`) wins — Ch 12.32's whole rationale is correct.
- `zero_reference_position`, `adaptive_margin`, `fade_target` are all valid `[bed_mesh]` options; `max_extrude_only_distance` default is 50 mm.
- Console-output examples are byte-accurate against current Klipper master: `PROBE_ACCURACY at X:… (samples=… retract=… speed=… lift_speed=…)`, `probe: at X,Y bed will contact at z=…`, `probe accuracy results: maximum … standard deviation …`, `Gantry-relative probe points:` + `Actuator Positions:` + `Average:` + `Making the following Z adjustments:` + `Retries: n/N Probed points range: … tolerance: …`, `Aborting quad_gantry_level required adjustment … greater than max_adjust`, `Z position: ? --> z <-- ?`, `stepper_z: position_endstop: …` + the two SAVE_CONFIG lines, `PID parameters: pid_Kp=… pid_Ki=… pid_Kd=…`, `probe: open`/`TRIGGERED`, `x:open y:open z:open`.
- `STEPPER_BUZZ` described exactly right: no console output, 1 mm forward, 50 ms dwell, 1 mm back, 450 ms dwell, ×10 (`force_move.py`).
- Room-temperature thermistor table (162/140/127/115/100/87/79 kΩ at 15/18/20/22/25/28/30 °C) reproduces Klipper's own `[thermistor ATC Semitec 104NT-4-R025H42G]` curve to ±0.5 % — and `klippy/extras/temperature_sensors.cfg` exists and gives 100 kΩ at 25 °C.
- Bed-heater sanity maths: 750 W @120 V = 19.2 Ω, @230 V = 70.5 Ω.

Hardware / procedure:
- Voron V2 startup-wizard page order (16 pages: temps → heaters → fans → motors → XY endstop → homing → bed locating → 0 point → Z endstop → probe → PID → QGL → initial setup) matches `buttons.js` exactly.
- Belt tension: A/B **110 Hz over a measured 150 mm span**, "≈2 lb… lower end of the range"; Z **140 Hz** over 150 mm from the Z idler centres — verbatim from Secondary Printer Tuning. Chamber 55–60 °C verbatim from materials.html.
- Klipper Z-resonance settings `accel_chip_z`, `max_z_velocity: 20`, `max_z_accel: 1550` verbatim from Measuring_Resonances.md.
- Stealthburner manual cross-checks all pass: p.13 toolhead-PCB inserts, p.14 Igus 2-hole vs generic 3-hole, p.15 flush-not-below on accent parts, **p.21 drive gear 15.6 mm**, p.23 "tighten until the plastic bends and cracks… reprint", p.25 hinge bolt "DON'T TIGHTEN", p.28 M3×30, p.29 M3×8 + washer + access hole, p.30 gear mesh + second bolt, p.31 M3×20, p.32 M3×8, p.38 ADXL-mount inserts to skip, p.40 "You MUST bend the strain relief", p.41 M3×16, **p.43 PTFE 11 mm stickout**, p.46 LED indices logo=1 / right=2 / left=3 with 120 mm + 100 mm 3×0.16 mm² leads and OUT→IN chaining, p.47 opaque mask / translucent diffuser, p.51 wires exit right, p.53 hotend fan wires up + air inwards, p.55 trimming jig in the release, p.56 M3×6 FHCS, p.64 M3×8, p.67 M3×25 + M3×50. `Voron_Design_Cube_v7.stl` measures exactly 30.000 × 30.000 × 30.000 mm.
- Stealthburner printhead README maps "E3D Revo Voron → (E-RV) → 4× M3×8 mm" — confirms both the E-RV code check and the four cartridge studs.
- E3D Revo Voron page: 300 °C max, Semitec 104NT-4-R025H42G, Molex Micro-Fit 3.0 2-pin horizontal for heater and thermistor, "Turn Revo HeaterCore anti-clockwise to orient cables", "Attach the spring to the groove on the bottom of the Heatsink".
- LDO Rev D wiring guide, verbatim: nozzle probe M2×10 self-tappers sideways through the D2F + **M3×25 SHCS** mount + one pulley set screw not overtightened; probe tape front and sides only, never back or bottom; SSR "critical, an incorrect connection can cause catastrophic damage"; SSR SIG red→INPUT 3, black→INPUT 4, other end to HEATBED; Bed N→blue, Bed PE→yellow, Bed L→LOAD 1, Bed TH→TH1; DIN rails run left to right; bottom duct below the hole; splicer PCBs on their printed spacer; Checkpoint #1's four checks in order.
- XY endstop repin map (4→X2, 3→X1, 2→Y1, 1→Y3; X pin3→pin2, Y pin2→pin3) and the XES/YES vs "X Stop / Y Stop" identification — exact.
- FFC orientation: Pi 4B contacts forward / blue tab back; BTT Pi TFT43 contacts up / blue tab back — exact from LDO's touchscreen guide.
- Nevermore V5 Duo: 6 heat-sets (4 fan + 1 plenum + 1 cartridge), snips not a blade, cut the connector off the long-lead fan and keep the pigtail, first fan right / second left, leads trimmed to ~30–40 mm, 4× M3×16 BHCS, red to top pads / black to bottom, "A bad solder will result in permanently damaging the controller board", 6×3 mm magnets marked for polarity, M3 T-nuts into the **inside** of the bed extrusions + 2× M3×12 SHCS, carbon "NOT INCLUDED WITH THE KIT" and acid-free — all verbatim; and the guide's Octopus `PD13` → Leviathan `PF9` correction is right.
- LDO 350 Rev D BOM confirms: E3D Revo Hotend (HF), 2× 60×60×20 24 V fans, 1× 3×2 splicer per pair, 3× WAGO 221-415 + 2× 221-412, 5× VE0508, 2× M5 locking washers, 9× 6 mm slot covers, 2× aluminium handles + 4× M5×14 BHCS, 2× M3×6 captive screws, 32 GB SD, 100 zip ties, drag chains 2× 10×10 R18 + 1× 10×15 R28, deck panel 469×469×**3 mm** vs bottom panel **4 mm** (the manual's flagged deck-thickness conflict with LDO's own build note is real and correctly left to the caliper).
- Omron G3NB-210B-1 really is 24–220 VAC 10 A load / 5–24 VDC input — the manual's markings are right (not the commonly-quoted 240 V).
- Meanwell LRS-200-24 AC terminal order (⏚, N, L with L outermost) and the 115/230 V selector / EU RSP-200-24 exception.
- MainsailOS 3.x really does ship Klipper, Moonraker, Mainsail, Crowsnest, Timelapse and Sonar and **not** KlipperScreen (modules/generic 50–55), so the "MainsailOS + KIAUH for KlipperScreen only" route is correct; and `/boot/firmware/` is right for a Trixie-based 3.0.0 image.
- 164 of the 169 external URLs in these seven chapters return HTTP 200. All GitHub raw image/STL links, all `docs.ldomotors.com` anchors (`#esd-hardening`, `#pinout-fan-adapter-pcb`, `#cable-pinout-adapter-side`, `#umbilical-cable`, `#working-with-cable-chains`, `#printed-parts`, `#features`) and all Ellis/Klipper/Voron links resolve.

## Not checkable
- The **2026-07-10** date attached to LDO's ESD Hardening publication (Ch 08.53, Ch 10.58). The section exists at the cited anchor and its content matches the manual word for word, but docs.ldomotors.com publishes no page date. Related: the Nitehawk-SB-V2 GitHub **README** has no ESD section at all (last commit 2026-07-22, a typo fix); the ESD images were committed 2026-03-12. The prose lives only on docs.ldomotors.com.
- `http://voron.local` (12-software.md) — an example hostname, not a citation; cannot return 200 off-LAN.
- `https://www.raspberrypi.com/software/` returns 403 to curl (bot filter); it loads normally in a browser.
- All `(verify on bench)` fastener counts in Ch 09/10/11 — by design; the underlying LDO pages genuinely print the callout without a quantity. Spot-checked several against the BOM totals and none is short.
- Whether this specific kit's chamber thermistor is a Semitec 104NT or a Generic 3950: LDO's two published configs disagree (`leviathan-printer-rev-d-sbv2.cfg` says ATC Semitec; `Nitehawk-SB-V2/Configs/nitehawk-sbv2.cfg` says `Generic 3950` with a 4.7 kΩ pull-up). Reading the part on the bench is the only way to settle it; the error near room temperature is <1 °C but grows to a few °C at the 50–60 °C chamber band Ch 14.8 gates on.
- Physical fit/rock/clearance items (skirt warp, clip preload, door squareness) — bench-only.
