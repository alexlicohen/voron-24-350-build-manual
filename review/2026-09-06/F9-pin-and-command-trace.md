# F9 — Electrical + software end-to-end trace (adversarial)

Scope: Ch 00a, 08 (connectors), 09, 10, 12, 13, 14; diagrams 05/06/07/08/10; `leviathan-printer-rev-d-sbv2.cfg` @ `667521d` (byte-identical to `main`); Nitehawk-SB-V2 README + `Configs/nitehawk-sbv2.cfg` @ `42ae497`; LDO V2 board doc; Klipper @ `f0892d8` (`safe_z_home.py`, `controller_fan.py`, `probe.py`, `manual_probe.py`, `force_move.py`, `resonance_tester.py`, `display_status.py`, `configfile.py`); `mainsail-config/client.cfg`; Meanwell LRS-200 spec. R3's fixes (13.2 jumpers, 13.11 nevermore, 13.38 pointer, stm32f446xx, chamber pull-up, 12.29 PROBE) are already applied and are not repeated here.

### F1 · MAJOR · 10-wiring.md:10.33 and 10.60
Persona: first-time
Quote: "XY endstop PCB (on the **left** XY joint, fitted in Ch 05) … Dress the cable along the Y extrusion toward the rear-left" / "T-nut into the **left** Y extrusion, chain fixed end onto it, moving end onto the XY joint's cable bridge."
Problem: Every other document puts the pod and the chain on the RIGHT: Ch 05 Step 05.834/05.885 ("cable bridge … on the **right** XY joint", "endstop pod … on the right XY joint"), 09.33 ("under the **right-hand** XY joint"), 10.64/manual p.204 (Z chain retainer on the **A drive = rear right**), 10.42 (LDO's "B motor cable too short" only makes sense if the Z chain is on the A side), and X homes to +350 (right) so the X switch must be on the right joint. A builder following 10.60 mounts the Y chain on the side that has no cable bridge, then re-does it.
Fix: 10.33 → "on the **right** XY joint … Dress the cable along the **right** Y extrusion toward the **rear-right**, ready to enter the Y chain." 10.60 → "T-nut into the **right** Y extrusion … moving end onto the **right** XY joint's cable bridge (Ch 05 Step 05.750) … carries the umbilical and endstop cable rearward to the Z chain on the A drive."

### F2 · MAJOR · 10-wiring.md:10.74 and 10.77
Persona: first-time
Quote: "| Any 24 V node → **PE** | `OL` |" (10.74) / "| Any 24 V node | `OL` |" (10.77)
Problem: By Section 8 the ESD bond from 10.58 is fitted — LDO: "connecting … the USB adapter **ground** to the printer frame" — so the 24 V **negative** rail (PSU −V = USB-adapter GND = toolboard GND) is deliberately bonded to frame → PE. Measured −V→PE reads a few ohms, not `OL`. The same 10.77 table proves it: "Extruder motor body (via the ESD ground) → a few Ω" only exists *because* DC GND is bonded. A builder reads the −V row as a short, hunts a reversed ferrule, and the worst outcome is pulling the prescribed ground cable.
Fix: split the row in both tables: "PSU **+V** (or any Vin **+**) → PE: `OL`" and "PSU **−V** / any GND → PE: **a few Ω — expected**, this is the ESD bond from 10.58; it only reads `OL` if that cable is missing." Keep 10.29 as-is (it runs before 10.58).

### F3 · MAJOR · 12-software.md:12.11 vs 10-wiring.md:10.79 (pause) vs 13-initial-startup.md:13.2–13.3 vs 00a-mains-safety.md:00a.11
Persona: first-time
Quote: "Do not plug the cord in again until Ch 13." (10.79 pause) / "switch the inlet on. The PSU LED lights. Then, over SSH: lsusb" (12.11) / "Step 13.3 — First power-on, hand on the switch … With the power cable still unplugged … The cord is still out of the room" (13.2–13.3)
Problem: The Leviathan, Pi and Nitehawk are energised for the first time at 12.11, with no hand-on-switch/ten-second/smell ritual, and the machine then stays powered through flashing and 12.37. Ch 10 forbids exactly that plug-in, Ch 13 then stages a "first" power-on that has already happened many times, and 00a.11 lists 12.11 as the "third powered moment" although it is chronologically the second. The ritual is attached to the wrong step; the daughter-persona rule "when is it allowed to be live" is contradicted by the sequence itself.
Fix: (a) 10.79 pause and Checkpoint 10 → "Do not plug the cord in again until **Ch 12 Step 12.11**." (b) Move the 13.3 ritual into 12.11: "Stand to the side, hand on the rocker, switch on, ten seconds: PSU LED green, Pi PWR + ACT, toolboard **3V3** and **24V** LEDs lit, no click-cycling, buzz or smell, no stepper hot after a minute; then `lsusb`." (c) Retitle 13.3 "Power on again, hand on the switch" and delete "the cord is still out of the room" from 13.2. (d) 00a.11: order the three moments chronologically (10.23 → 12.11 → 13.3) and say the ritual applies at 12.11.

### F4 · MAJOR · 13-initial-startup.md:13.9, 13.10 and the What-if table
Persona: first-time
Quote: "The **bottom** fan of the Stealthburner spins up as soon as the hotend is active" (13.9) / "The **top** fan spins to full … `M107` stops it" (13.10)
Problem: The HEF/PCF pin conflict (LDO's `nhsbv2_pcb_pinout.jpg` says PA15→HEF, PD0→PCF; the adapter silk, board doc and config say the opposite) is documented and its remedy given only in 08.46 ("swap the `pin:` values … do not re-crimp"). Ch 13 is where the symptom appears (top fan answers the heater, bottom fan answers `M106`) and it offers no branch for it; the What-if row "A fan never starts" does not cover "the wrong fan starts". A hotend fan silently on `[fan]` is a heat-creep jam on the first print.
Fix: add to 13.9 Check: "If the **top** (5015) fan is what answers the hotend, and at 13.10 the **bottom** fan answers `M106`, the adapter's HEF/PCF assignment is the reverse of the config: exchange `pin: nhk:PD0` and `pin: nhk:PA15` between `[heater_fan hotend_fan]` and `[fan]` (and the commented tacho pins PD1/PD2), `RESTART`, re-run 13.9–13.10. Do **not** re-plug P2/P4 (08.46)." Add the same as a What-if row "The wrong toolhead fan answers".

### F5 · MAJOR · 00a-mains-safety.md:00a.6 (PE table, PSU row)
Persona: first-time
Quote: "PE WAGO → the Meanwell's **⏚** terminal, the outermost of its three AC screws (⏚, N, L)"
Problem: Meanwell LRS-200 spec, Terminal Pin No. Assignment: **1 AC/L, 2 AC/N, 3 FG**, 4–6 −V, 7–9 +V — L is the outermost, FG is innermost next to the DC block. 10.9 and the 05 diagram embedded on this very page say "L is the outermost". The safety chapter's own earth-chain table names the wrong screw for earth.
Fix: "PE WAGO → the Meanwell's **⏚** terminal — the **innermost** of its three AC screws, next to −V; order from the outer end is L, N, ⏚ (10.9)."

### F6 · MINOR · assets/diagrams/06-harness-map.svg (POWER — 24 V, row 1) vs 10-wiring.md:10.24
Persona: first-time
Quote: diagram: "24V PSU to MB (TO MB end) → Vin 24V / Board · other end on the PSU +V / −V"; 10.24: "Land the **TO MB** end on the PSU's +V and −V terminals. Land the **24V** end on the Leviathan … Vin 24V / Board."
Problem: Diagram and chapter disagree on which tagged end goes where. LDO's guide (Connecting 24V) is with the chapter: "Connect the **24V** end … to the Board terminals on the controller and the **TO MB** end to the PSU." The HV, SSR and toolhead rows of the same diagram follow LDO; only this row was "corrected" to the intuitive reading.
Fix: diagram row → "24V PSU to MB (**24V** end) → Vin 24V / Board · **TO MB** end on the PSU +V / −V".

### F7 · MINOR · 10-wiring.md:10.11 (and 10.24–10.27 Parts lines)
Persona: first-time
Quote: "(LDO's text swaps the two labels — *Connect the To SSR end … to a brown wago slot* … so go by the connector type: the ferruled end belongs in the SSR screw terminal.)"
Problem: LDO's tags are not swapped; they follow one convention on all five cables — the tag names the cable's **destination**, not the end you hold: TO MB HV and TO TOOLHEAD sit on the PSU ends, To SSR on the WAGO end, SSR SIG on the SSR end. Read that way, LDO's sentence is right and 10.11's "Land the **TO SSR** end on SSR terminal LOAD 2" is the one that puts the bare stripped end under a screw. The parenthetical rescues the builder but teaches them the wrong rule.
Fix: state the convention once at 10.10 ("LDO's cable tags name where the *other* end goes") and reword 10.11: "The end tagged **TO SSR** is the bare, stripped end — it goes into a spare port of the brown **L** WAGO. The ferruled end goes on SSR **LOAD 2**."

### F8 · MINOR · 13-initial-startup.md:13.6
Persona: first-time
Quote: "You should have four sensors: `extruder`, `heater_bed`, `chamber_temp` and the Pi's `temperature_host`."
Problem: Neither the `-sbv2` config nor `mainsail.cfg` (`client.cfg`: virtual_sdcard, pause_resume, display_status, respond, macros only) defines a host sensor; 12.37 and Checkpoint 13 correctly say three. A builder looks for a fourth trace that cannot exist.
Fix: "three sensors: `extruder`, `heater_bed`, `chamber_temp`" — or add `[temperature_sensor raspberry_pi]\nsensor_type: temperature_host` at 12.35 and keep "four".

### F9 · MINOR · 13-initial-startup.md:13.11
Persona: first-time
Quote: "Set the **Bed** target to 60 and wait for it to pass 60 °C … The electronics-bay PCB fan runs on its own as the bed passes 60 °C"
Problem: `controller_fan.py` sets `active` when `heater.get_temp()` returns a non-zero **target** or any stepper is enabled — the bay fan starts the instant a bed target is set (it was already running at 13.8) and stops 30 s (`idle_timeout`) after target and steppers go idle. The ten-minute wait for 60 °C proves nothing and the stated trigger is wrong.
Fix: "Set the Bed target to 60. The bay fan pair starts **immediately** — `[controller_fan]` keys on the bed being *commanded* (and on any enabled stepper), not on its temperature — and keeps running ~30 s after you set the bed Off. No need to wait for a temperature; send `SET_FAN_SPEED FAN=nevermore SPEED=1` now."

### F10 · MINOR · 14-calibration.md:14.1 and 14.12 vs 12-software.md:12.35, 12.27, Checkpoint 12
Persona: first-time
Quote: "there is **no** `[input_shaper]` section yet" (14.1) / "Then uncomment the **350 mm** probe point in `[resonance_tester]`" (14.12)
Problem: 12.35 adds an `[input_shaper]` placeholder and Checkpoint 12 requires it; 12.27 already uncommented `probe_points: 175, 175, 20` and Checkpoint 12 requires that too. A literal reader of 14.1 deletes the placeholder; 14.12 re-instructs a done edit. (`configfile._strip_duplicates` means the empty placeholder is harmless to SAVE_CONFIG — no functional bug.)
Fix: 14.1 → "the `[input_shaper]` placeholder from 12.35 is present with both `shaper_freq` lines still commented"; 14.12 → "confirm `probe_points: 175, 175, 20` is live (12.27) — do not edit".

### F11 · MINOR · 12-software.md:12.17 (ACT LED claim) and the untouched `[output_pin pcb_led]` stanza
Persona: first-time
Quote: "`!PC6` lights the ACT LED at startup, which is your at-a-glance 'Klipper is running' indicator on the toolhead."
Problem: LDO's board doc: ACT is "Active low"; the firmware's `!PC6` drives it low → ON at MCU boot. The kit config keeps `[output_pin pcb_led] pin: !nhk:PC6` with default `value: 0` → Klipper drives PC6 **high** the moment the host connects → LED **off**. LDO's own `nitehawk-sbv2.cfg` uses the non-inverted `pin: nhk:PC6` (LED on while connected). As shipped, the "Klipper is running" light goes dark exactly when Klipper connects, which is the opposite of what 12.17 and 12.19 lead the builder to expect at 13.4. (Inferred from the two LDO files + `output_pin.py`; verify on bench.)
Fix: in 12.32 add "`[output_pin pcb_led]`: change `pin: !nhk:PC6` → `pin: nhk:PC6` (LDO's board-level config form) so the ACT LED stays lit while Klipper is connected; if it goes dark at `Ready`, the `!` is still there." Add "toolboard ACT LED lit" to the 13.4 Check.

### F12 · MINOR · 13-initial-startup.md:13.5
Persona: first-time
Quote: "Send `GET_POSITION` and check the reported axis maximums in the interface's status panel … If X/Y read 250 you are still on the default"
Problem: `GET_POSITION` prints stepper/kinematic/toolhead positions, never limits, and Mainsail shows no `axis_maximum`; the check cannot be performed as written. There is also no 250 default — with every size commented Klipper refuses to start ("Option 'position_endstop' in section 'stepper_x' must be specified"), so the only way to be "on 250" is to have uncommented the wrong pair.
Fix: "Open `printer.cfg` in the editor and confirm the six 350 sites (list). The running instance is proved at 13.22/13.23: after `G28 X` then `G28 Y`, `M114` must read `X:350.000 Y:350.000`; anything else means the wrong size pair is live."

### F13 · MINOR · 13-initial-startup.md:13.36 (example transcript)
Persona: first-time
Quote: "Recv: // Z position: 0.150 --> 0.250 <-- 0.350 / Send: ACCEPT / Recv: // stepper_z: position_endstop: -0.310"
Problem: `manual_probe.py`: `z_pos = position_endstop − bed_z` → with the stock −0.5 and ACCEPT at 0.250 the printed value is **−0.750**. The example's numbers do not produce its own answer, and 13.37 then tells the builder the sign convention matters.
Fix: change the last line to `stepper_z: position_endstop: -0.750` (and say "= −0.5 − 0.250").

### F14 · MINOR · 13-initial-startup.md:13.22 (and 13.17)
Persona: first-time
Quote: "The toolhead lifts slightly (that is `[safe_z_home] z_hop: 10`), then travels to the right"
Problem: `safe_z_home.py`: when Z is unhomed, `G28 X` sets the current Z to 0 and lifts 10 mm from **wherever the gantry is**. 13.17 positions XY only; a gantry parked against its top stop (where Ch 06/13.21 leave it "high") stalls the four Z motors into the frame on the very first move. If a Z `dir_pin` is still wrong, it drops 10 mm instead — into the bed if the nozzle was low.
Fix: at 13.17 add "and set the gantry roughly mid-travel by hand — at least 20 mm below its top stop and well above the bed: the first `G28 X` lifts it 10 mm before anything else."

### F15 · MINOR · 10-wiring.md:10.41 vs 13-initial-startup.md:13.17–13.19, 13.25, Ch 06b
Persona: first-time
Quote: "never spin a connected motor by hand. Back-EMF kills drivers."
Problem: Ch 13 then instructs four hand moves of the toolhead/gantry (after `M84`) and Ch 06b squaring moves the gantry by hand with A/B disabled. The absolute rule freezes the first-timer at 13.17 or makes them ignore 10.41 altogether.
Fix: 10.41 → "never spin a connected motor **fast** by hand or shove the gantry — a fast move generates back-EMF the driver has to absorb. The slow, driver-disabled (`M84`) hand moves Ch 13 and Ch 06b ask for are fine."

### F16 · MINOR · 12-software.md:12.10 and the chapter Hardware table
Persona: first-time
Quote: "Pi FFC ribbon ×1 — both already fitted in Ch 11" / "The DSI ribbon and the Pi were fitted in Ch 09/Ch 11"
Problem: The ribbon is latched at both ends at **10.50**; Ch 11 only mounts the screen with the front skirt. Wrong pointer for a builder checking the FFC orientation warning.
Fix: "ribbon fitted at 10.50, screen mounted in Ch 11".

### F17 · MINOR · 12-software.md:12.16
Persona: first-time
Quote: "sudo dfu-util -d 0483:df11 -a 0 -s 0x08000000:mass-erase:force -D out/katapult.bin"
Problem: `dfu-util` is not installed on MainsailOS; the install line appears only in 12.19, three steps later. The recovery path fails with "command not found" at the worst moment.
Fix: prefix the block with `sudo apt install dfu-util` as 12.19 does.

### F18 · MINOR · 12-software.md:12.11
Persona: first-time
Quote: "`lsusb` lists two devices whose descriptors mention Klipper"
Problem: `lsusb` prints `ID 1d50:614e OpenMoko, Inc. stm32f446xx` / `… stm32g0b1xx`; "Klipper" is the manufacturer string, shown only with `-v`. The builder sees no "Klipper" and doubts the boards.
Fix: "two `1d50:614e OpenMoko, Inc.` entries whose product names are the MCUs — `stm32f446xx` (or `stm32h743xx`) and `stm32g0b1xx` — plus the Nitehawk's hub".

### F19 · IMPROVE · 10-wiring.md:10.29 vs 10.74; 10.44 vs 10.76
Persona: second-time
Quote: "measure across the PSU's +V → −V … Vin 24V … Vin 24-48V … USB adapter's 24 V input" (10.29, repeated verbatim as 10.74) / "Before plugging it in, measure it — see the table in step 10.76" (10.44) then "Unplug the bed thermistor from TH1 and measure" (10.76)
Problem: The same four resistance readings are taken twice, and the bed thermistor is measured, plugged, unplugged and measured again.
Fix: keep 10.29 only as "cap-charging sanity after wiring", and make 10.74 the single authoritative table (with the F2 split); in 10.76 say "bed thermistor was measured at 10.44 — measure only the toolboard TH0 and CT here if the toolhead is still open".

### F20 · IMPROVE · 13-initial-startup.md:13.7 and 13.3/12.11
Persona: second-time
Quote: "If nothing heats, check `[extruder] heater_pin: nhk:PA7`."
Problem: The Nitehawk has five status LEDs (3V3, 24V, HE0, ACT, HUB — named at 12.19) and 13.8 already uses the SSR LED to split a bed fault into halves; the hotend test ignores the equivalent HE0 LED, and the power-on checks ignore 3V3/24V.
Fix: 13.7 Check → "the toolboard **HE0** LED lights while the target is set; LED on + no climb = heater/ferrule side, LED off = pin/config side." Add "toolboard 3V3 and 24V LEDs lit" to the 12.11/13.3 checks (see F3).

### F21 · IMPROVE · 14-calibration.md:14.4–14.6 vs 13-initial-startup.md:13.34–13.39 and Ch 06b.15
Persona: second-time
Quote: "Set A/B belt tension to 110 Hz over a 150 mm span" (14.4, "for the last time") after Ch 13 has already re-tensioned at 06b.15 "to 110 Hz / 150 mm span and matched" (Checkpoint 13) and then measured Z0 and the mesh.
Problem: Belts are set twice with the same method, and the Z belts (140 Hz) are set only in Ch 14 — after the Ch 13 mesh/Z0 that 14.6 admits belt tension shifts. Either Ch 13's Z0/mesh are taken on belts that will change, or 14.4/14.5 are theatre.
Fix: move the Z-belt 140 Hz set into 06b (with the A/B re-tension), make 14.4/14.5 a "re-verify only" step, and keep 14.6 as the post-check.

## Trace — verified consistent (no finding)
- Motors: A rear-right → HV-STEPPER-1 → `[stepper_y]`; B rear-left → HV-STEPPER-0 → `[stepper_x]`; Z0 FL→STEPPER-0/`stepper_z`, Z1 RL→1/`z1`, Z2 RR→2/`z2`, Z3 FR→3/`z3`; STEPPER-4 empty; config comments, LDO table, diagrams 03/06/10, Ch 04/05/07 side naming all agree. `STEPPER_BUZZ` = +1 mm, 50 ms, −1 mm, 450 ms ×10 (`force_move.py`) → "corner rises first" is right given a correct `dir_pin`; QGL points order FL/RL/RR/FR matches Z0–Z3.
- Thermistors/heaters: bed TH1/PA2 + PG11/HEATBED, 2k2; hotend TH0/PB12 + HE0/PA7, 2k2; chamber CT/PB2, 4k7 (no line); 10.76 table ≈ Klipper 104NT curve; 13.6 "couple of degrees" consistent.
- Probe: PROBE port → `nhk:PC15`, `y_offset 25` → QGL nozzle points 50,25…300,275 put the probe at 50,50…300,300; `bed_mesh` 40/310 probe coords → nozzle Y 15…285 legal; `PROBE_ACCURACY` "probe: at 175,200" is correct (`create_probe_result` adds the offset). Z-ENDSTOP/PC3 for the nozzle probe; Z-PROBE empty everywhere.
- Endstops: X-ENDSTOP/PC1, Y-ENDSTOP/PC2, `homing_positive_dir` + `position_endstop 350` → right/back; NC-to-ground reading (`open` at rest, `TRIGGERED` on break) matches no-`!` pins.
- Fans: FAN2/PF7 `[controller_fan]` 24 V jumper; FAN3/PF9 `[fan_generic nevermore]` 24 V jumper; FAN0/FAN1/Z-PROBE bare; toolhead P2 4010→HEF/PD0 `[heater_fan]`, P4 5015→PCF/PA15 `[fan]`, P3→PD3 neopixel GRBW ×3; 08.45 solder selectors 24 V. `SET_DISPLAY_TEXT` exists (`display_status.py`), Z-axis `SHAPER_CALIBRATE`/`accel_chip_z`/20/1550 exist (`resonance_tester.py`, Measuring_Resonances.md).
- Mains/PE: inlet (fuse in L only, rocker breaks L+N, E straight through) → WAGO N/L/PE → PSU (L,N,⏚ per LRS-200 spec) and L→SSR LOAD 2 → LOAD 1→bed L; INPUT 3 red/+, 4 black/−; bed N/PE to bus; frame PE on scraped metal; five PE branches identical in 00a.6, 05 diagram, 10.5–10.16, 10.77 (except F5 and F2).
- Software order: update → record version → flash Leviathan (Katapult, 32/128 KiB) → flash Nitehawk (8 KiB, `make flash`) → serial IDs → config edits → 12.37 restart (no motion) → 13 in wizard order; `safe_z_home` −10,−10 interlock; `homing_retract_dist`/`second_homing_speed` numbers match config; SAVE_CONFIG/`_strip_duplicates` behaviour as described.

## Chapter verdicts
- 00a — buildable by a first-timer as written: with fixes — weakest: 00a.6 (F5 wrong PSU screw), 00a.11 (F3 ritual order), 00a.7 (fine, but repeats 10.10).
- 08 (electrical steps 08.45–08.62) — yes — weakest: 08.46 (remedy not echoed in Ch 13, F4), 08.52 (ACT LED role, F11), 08.60 (no mention that the umbilical must stay unplugged at the bay until 10.67 — it does say so; fine).
- 09 — yes — weakest: 09.33/09.19 fine; only cross-reference victims of F1.
- 10 — with fixes — weakest: 10.33/10.60 (F1), 10.74/10.77 (F2), 10.11 (F7); 10.79 pause (F3).
- 12 — with fixes — weakest: 12.11 (F3, F18), 12.17/12.32 (F11), 12.16 (F17).
- 13 — with fixes — weakest: 13.9–13.10 (F4), 13.5 (F12), 13.11 (F9); 13.22 (F14).
- 14 — yes — weakest: 14.1/14.12 (F10), 14.4–14.5 (F21), 14.16 (valid but optional).
- Diagrams — 06 harness map needs the F6 row fixed; 05/07/08/10 consistent with the chapters and config.

## Praise
- The pin/port trace is otherwise exact end to end: config, LDO table, three diagrams and Ch 10/13 never disagree on a single stepper, thermistor, endstop, fan or probe pin — rare for a Rev D+ document set.
- 12.33's "leave `safe_z_home` broken on purpose" interlock and 12.34's `zero_reference_position` reasoning are the two best-explained config decisions in the manual; keep them verbatim.
- 13.8's SSR-LED fault split and 13.23's "test both axes before changing anything" are exactly how an experienced builder diagnoses; extend the pattern (F4, F20) rather than rewrite it.
- 10.13/10.19/10.21/10.78 turn LDO's four-line Checkpoint #1 into a real meter procedure with expected values — the strongest safety section in the manual.
