# Chapter 13 — Initial startup

Turns the wired machine on for the first time and proves every subsystem in the order the Voron startup wizard prescribes — temperatures, heaters, fans, motors, endstops, homing, probe, PID, QGL, Z=0, bed mesh — then hands off to gantry squaring and comes back for the first print.

**Time:** 2.5–4.0 h hands-on, first build (survey §5.1 P13 / §7.2). Add ~30 min of unattended PID runs and 10–20 min of heat-soak wall clock, plus ~1 h for the cube print at the end.

**Prerequisites:**
- **Ch 10 — Wiring.** **Checkpoint #1 passed** with a multimeter, machine unplugged. This is a hard gate: if you have not done it, stop and do it. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d)
- **Ch 12 — Software.** Klipper, Moonraker and Fluidd/Mainsail installed; `leviathan-printer-rev-d-sbv2.cfg` uploaded as `printer.cfg`; both MCU serial IDs filled in; the 350 mm options uncommented.
- **[Ch 06 Part A — Z axis](06-z-axis-and-gantry-squaring.md)** (gantry installed, Z belts on) and **[Ch 07 — A/B belts](07-ab-belts.md)** at provisional tension. The gantry is *not* squared yet — that is Ch 06 Part B (06b), which runs out of the middle of this chapter at Step 13.34.
- **Ch 11 — Skirts and panels:** bottom panel and skirts on (Ch 11 Part A). **Back, side and top panels off** and left off (Ch 11 Part B comes after this chapter) — you need access to the gantry for Ch 06b, and you want to see and smell everything on first power-up.
- **Print batches:** none. You will *print* `Voron_Design_Cube_v7` at the end of this chapter, on the new machine.

**Tools**
- Laptop or tablet on the same network, with the Fluidd/Mainsail console open, and a second window with `RESTART` already typed and unsent (your software E-stop)
- A sheet of ordinary printer paper (~0.1 mm) for the Z=0 paper test
- Digital caliper and a marker (e-steps)
- 2 mm and 2.5 mm hex keys (Z endstop position, probe height)
- Phone (video of the first homing move; belt-tension app for the Ch 06b return leg)

**Consumables:** a spool of ASA, dried and warm from the dryer (survey §7.3). Nothing else is consumed.

**Printed parts**

| STL | Qty | Colour |
|---|---|---|
| — none — | 0 | — |

**Hardware** (chapter totals)

| Fastener / part | Qty | Note |
|---|---|---|
| — none — | 0 | Nothing is fastened in this chapter except re-positioning the Z endstop and the probe, both already installed in Ch 09/Ch 10 |

**Read first**
- **PID tuning comes before QGL, and QGL is run hot.** A thermally unstable machine will not QGL repeatably. Do not reorder this. (survey §3.3, §4.4 #16)
- **Do not trust a QGL until `PROBE_ACCURACY` shows σ < 0.003 mm with no trend across the 10 samples.** From cold, that takes 10–20 minutes of soak at temperature. (survey §4.4 #16)
- **Never unplug or re-plug a stepper with the power on.** Every "swap the A and B connectors" instruction in this chapter means: power down, swap, power up. (survey §4.4 #10)
- **The stock LDO config ships every build-size option commented out and `[safe_z_home] home_xy_position` set to the placeholder `-10,-10`.** A full `G28` will refuse to run until you replace it with a real coordinate — that is Step 13.26, not a fault. (survey §4.4 #15)
- **If Ch 12 loaded `leviathan-printer-rev-d.cfg` instead of `leviathan-printer-rev-d-sbv2.cfg`, stop now.** Every `nhk:` pin differs; you would be mis-driving the heater, thermistor, probe, both toolhead fans and the accelerometer at once. Check `[mcu nhk]` resolves to a `stm32g0b1xx` serial ID before you heat anything. (survey §4.1 ①, §5.2 W13)

---

## Part A — First power-on

### Step 13.1 — Clear the machine and stage the bench

![Voron 2.4 reference render](https://raw.githubusercontent.com/VoronDesign/Voron-Documentation/master/build/startup/images/v2render.png)

**Parts:** none — preparation.

**Do:** Take everything out of the chamber: tools, offcuts, zip-tie tails, the bag of spare fasteners, the filament spool. Check the gantry and bed for anything resting on them and pull off any rubber rail stoppers still on the rails. Put a fire extinguisher within arm's reach and clear the bench of paper and IPA. Confirm the side and top panels are off.

**Check:** You can see the toolhead, all four Z drives, the electronics bay and the PSU without moving anything.

---

### Step 13.2 — Re-confirm the Checkpoint #1 result and the PSU voltage selector

![LDO Rev D bay, wiring complete](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/RevD/VS9_Final.jpg)

**Parts:** none — verification.

**Do:** With the power cable **still unplugged**, look once more at the PSU's 115/230 V selector and confirm it matches your mains. Confirm the SSR wiring against the numbered terminals: control on INPUT 3 (red, +) and INPUT 4 (black, −), bed live on LOAD 1, mains brown on LOAD 2. Confirm **exactly two** Leviathan voltage-selection jumpers are fitted — **Fan2 and Fan3, both on the 24 V pins** — and that **Probe, Fan0 and Fan1 are still bare** (Step 10.28, Checkpoint 10). LDO: *"Mixing voltage will permanantly damage the controller and attached components."*

**Check:** Selector correct. No bare copper anywhere. Every wire duct still open so you can watch the bay. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d)

⚠ Rev D+ / LDO: there is **no 5 V PSU** in this kit — the Leviathan supplies the Pi's 5 V through the Pi HAT adapter. If you are looking for a second supply, you have the wrong manual pages (manual p.152, p.172, p.190 are all SKIP). (survey §4.2)

---

### Step 13.3 — First power-on, hand on the switch

![LDO PSU switch](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/psu_switch.jpg)

**Parts:** none.

**Do:** Plug the mains lead in. Stand to the side of the machine, put your hand on the IEC inlet's rocker switch, and switch on. Keep your hand there for a full ten seconds. Listen and smell.

**Check:** The PSU's green LED lights. The Pi's power LED lights and its activity LED flickers. Nothing clicks repeatedly, nothing buzzes, nothing smells hot, no stepper is humming or holding hard. If anything on that list is wrong, switch off immediately and go back to Ch 10.

Tip: a stepper that is warm to the touch after a minute of idling is normal (they hold at `run_current`); a stepper that is *hot* in a minute is not.

---

### Step 13.4 — Connect Klipper and confirm both MCUs

![Fluidd/Mainsail console](https://raw.githubusercontent.com/VoronDesign/Voron-Documentation/master/build/startup/images/mainsail_terminal.png)

**Parts:** none.

**Do:** Open the web interface at the Pi's address. Go to the **Console** tab — every command in this chapter is typed there. Send `FIRMWARE_RESTART`, then `STATUS`.

```
Send: FIRMWARE_RESTART
Recv: // Klipper state: Shutdown
Recv: // Klipper state: Ready
Send: STATUS
Recv: // Klipper state: Ready
```

**Check:** `Ready`, with no `mcu 'nhk': Unable to open serial port` and no `Option 'serial' in section 'mcu' must be specified`. Any error here is a Ch 12 problem, not a Ch 13 problem.

⚠ Rev D+ / LDO: `ls /dev/serial/by-id/*` over SSH must show exactly two Klipper devices — one `usb-Klipper_**stm32f446xx**_…` (Leviathan; `stm32h743xx` on a V1.3 board — the LDO guide's `stmf446xx` is a typo, Ch 12 Step 12.13) and one `usb-Klipper_**stm32g0b1xx**_…` (Nitehawk-SB **V2**). The Rev D wiring guide tells you to look for `rp2040`; that is the V1 board and it is not what you have. (survey §4.1 ②)

---

### Step 13.5 — Prove the 350 mm config edits are live

(no image — see text)

**Parts:** none.

**Do:** Do not trust the file on disk; ask the running instance. Send `GET_POSITION` and check the reported axis maximums in the interface's status panel, then confirm in the config editor that these are uncommented: `[stepper_x] position_endstop: 350` and `position_max: 350`; `[stepper_y]` the same; `[stepper_z] position_max: 330`; `[quad_gantry_level] gantry_corners: -60,-10 / 410,420` and `points: 50,25 / 50,275 / 300,275 / 300,25`; `[gcode_macro G32]` park line `G0 X175 Y175 Z30 F3600`; `[resonance_tester] probe_points: 175, 175, 20`.

**Check:** The interface's X and Y travel limits read 350, Z reads 330. If X/Y read 250 you are still on the default and homing will crash the toolhead into the frame. (survey §5.2 W14)

---

## Part B — Temperatures, heaters, fans, lights

### Step 13.6 — Verify the four temperature readings at room temperature

![Mainsail temperature graph](https://raw.githubusercontent.com/VoronDesign/Voron-Documentation/master/build/startup/images/mainsail_temp_graph.png)

**Parts:** none.

**Do:** Look at the temperature panel. You should have four sensors: `extruder`, `heater_bed`, `chamber_temp` and the Pi's `temperature_host`. Read them and do nothing else for thirty seconds.

**Check:** Extruder, bed and chamber all read within a couple of degrees of the actual room temperature, and **none of them is climbing**. If a temperature is rising with nothing commanded, cut power at the switch — a heater is energised through a wiring fault. If a reading is wildly wrong or jittering, check the crimps and the `sensor_type` / `sensor_pin` entries; extruder and bed are `ATC Semitec 104NT-4-R025H42G` with `pullup_resistor: 2200` in the LDO config; the chamber sensor is on the toolboard's `CT` port, which has a **4.7 kΩ** pull-up, so `[temperature_sensor chamber_temp]` carries **no** `pullup_resistor` line and must not be given one (Klipper's default is 4700). [src](https://docs.vorondesign.com/build/startup/)

⚠ Rev D+ / LDO: the hotend and chamber thermistors land on the **Nitehawk V2** through **JST-PH2.0** connectors, not the XH2.5 the Rev D wiring guide names. A spare pigtail crimped to XH2.5 will not fit, and a PH2.0 housing can be forced into the wrong header. (survey §4.1 ③)

---

### Step 13.7 — Short heat test: hotend to 50 °C

![Heater verification](https://raw.githubusercontent.com/VoronDesign/Voron-Documentation/master/build/startup/images/heaters.gif)

**Parts:** none.

**Do:** Hand back on the power switch. Set the **Tool** target to 50 and press enter. Watch the graph.

**Check:** The extruder temperature starts climbing within about 10 s. Set the target back to **Off** and confirm it decays toward room temperature over the next few minutes. If a *different* sensor heats, your thermistor or heater connections are swapped. If nothing heats, check `[extruder] heater_pin: nhk:PA7`. [src](https://docs.vorondesign.com/build/startup/)

---

### Step 13.8 — Short heat test: bed to 50 °C, and watch the SSR

(no image — see text)

**Parts:** none.

**Do:** Hand back on the switch. Set the **Bed** target to 50. Watch the SSR's indicator LED in the electronics bay as well as the graph.

**Check:** The SSR LED comes on, and the bed temperature climbs. Set the target to **Off**. If the SSR LED lights but the bed does not heat, the fault is on the mains side of the SSR. If the SSR LED never lights, the fault is on the control side — the commonest cause is the control pair reversed (Leviathan **+** must go to SSR INPUT **3**). [src](https://docs.vorondesign.com/build/startup/)

Tip: `[heater_bed] max_power: 0.6` in the LDO config is deliberate — it limits warp on a 350 plate. Do not raise it because 100 °C feels slow.

---

### Step 13.9 — Hotend fan (Stealthburner **bottom** fan)

(no image — see text)

**Parts:** none.

**Do:** Set the Tool target to 50 again and leave it there for this step and the next.

**Check:** The **bottom** fan of the Stealthburner spins up as soon as the hotend is active, and stays on above 50 °C. This is `[heater_fan hotend_fan]` on `nhk:PD0` with `heater_temp: 50.0`. A hotend fan that does not run will clog the hotend on your first print. [src](https://docs.vorondesign.com/build/startup/)

---

### Step 13.10 — Part cooling fan (Stealthburner **top** fan)

(no image — see text)

**Parts:** none.

**Do:** Send `M106 S255`, then `M107`.

**Check:** The **top** fan spins to full and you feel air under the nozzle; `M107` stops it. This is `[fan]` on `nhk:PA15`. Note that `off_below: 0.10` means anything under 10 % commands zero — that is expected, not a fault.

⚠ Rev D+ / LDO: the 2×5 (10-pin) board-to-board header between the Stealthburner fan adapter and the toolboard has **reversed gender and is keyed** on Rev D+. If a toolhead fan does nothing at all, do not press the connector harder — check that it seated with the key, not against it. (survey §4.1 ④)

---

### Step 13.11 — Bay fan and filter fan

(no image — see text)

**Parts:** none.

**Do:** Set the **Bed** target to 60 and wait for it to pass 60 °C, then send `SET_FAN_SPEED FAN=nevermore SPEED=1` and, after confirming it, `SET_FAN_SPEED FAN=nevermore SPEED=0`.

**Check:** The electronics-bay PCB fan runs on its own as the bed passes 60 °C (`[controller_fan controller_fan]`, `FAN2/PF7`, keyed off `heater_bed`) and keeps running for a while after you set the bed to Off — that is the idle behaviour, not a fault. The Nevermore fan (`FAN3/PF9`) runs **only** while you command it: it is **not** slaved to the bed.

⚠ Rev D+ / LDO: the LDO config names `FAN3/PF9` `[heater_fan exhaust_fan]`, but on this build that port drives the **Nevermore filter fan** — the kit has no exhaust fan. Ch 12 Step 12.32 replaced that section with `[fan_generic nevermore]` so `PRINT_START` can run the filter for the whole print, so there is no `heater_temp: 60` trigger any more and nothing happens at bed 60 °C. Do not go looking for a second fan or a wiring fault. (survey §3.2, §4.2 p.250–253)

---

### Step 13.12 — Lights

(no image — see text)

**Parts:** none.

**Do:** Send `SET_PIN PIN=caselight VALUE=1`, then `SET_LED LED=rgb_light RED=1 GREEN=1 BLUE=1 WHITE=1`.

**Check:** The chamber COB strips come on (`[output_pin caselight]`, `PE6`). All three Stealthburner LEDs light. If the colours come out wrong rather than absent, the LEDs work and only `color_order` is off — the LDO config sets `chain_count: 3`, `color_order: GRBW`, which is correct for the supplied diffuser and LEDs. (survey §4.4 #12)

---

## Part C — Motors

### Step 13.13 — `STEPPER_BUZZ` the four Z motors

![Voron V2 stepper locations and configuration guide](https://raw.githubusercontent.com/VoronDesign/Voron-Documentation/master/build/startup/images/V2-motor-configuration-guide.png)

**Parts:** none.

**Do:** Run the four Z commands one at a time, watching the machine — not the console. `STEPPER_BUZZ` prints nothing; it moves the named stepper 1 mm positive, pauses, returns, and repeats ten times.

```
Send: STEPPER_BUZZ STEPPER=stepper_z
Send: STEPPER_BUZZ STEPPER=stepper_z1
Send: STEPPER_BUZZ STEPPER=stepper_z2
Send: STEPPER_BUZZ STEPPER=stepper_z3
```

**Check:** Exactly one motor responds per command, it moves cleanly (forward, pause, back, pause), and it lifts the corner named below **first**, before returning.

| Command | Motor | Corner that must rise first |
|---|---|---|
| `STEPPER_BUZZ STEPPER=stepper_z` | Z0, `STEPPER-0` | front **left** |
| `STEPPER_BUZZ STEPPER=stepper_z1` | Z1, `STEPPER-1` | rear **left** |
| `STEPPER_BUZZ STEPPER=stepper_z2` | Z2, `STEPPER-2` | rear **right** |
| `STEPPER_BUZZ STEPPER=stepper_z3` | Z3, `STEPPER-3` | front **right** |

[src](https://docs.vorondesign.com/build/startup/)

Note: the wizard's V2 table words this as "the corner of the **bed** moves up". On a 2.4 the bed is bolted to the frame and does not move — what rises 1 mm is the corresponding corner of the **gantry**. Sight along the top of the X extrusion against the frame to see it.

---

### Step 13.14 — `STEPPER_BUZZ` the A and B motors

![Stepper buzz](https://raw.githubusercontent.com/VoronDesign/Voron-Documentation/master/build/startup/images/verifysteppers.gif)

**Parts:** none.

**Do:** Run the two gantry commands.

```
Send: STEPPER_BUZZ STEPPER=stepper_x
Send: STEPPER_BUZZ STEPPER=stepper_y
```

**Check:** `stepper_x` moves the **rear-left** motor (B, `HV-STEPPER-0`); `stepper_y` moves the **rear-right** motor (A, `HV-STEPPER-1`). Both must move cleanly with no grinding or vibrating in place. The wizard's expectation is "rotate clockwise first, then back counterclockwise", but do not spend time on that here: on CoreXY a single motor's rotation direction is not a meaningful check by eye. **A/B direction is settled at the homing check in Step 13.22–13.23**, against the chart above. What matters right now is that the right motor answers and that it moves cleanly. [src](https://docs.vorondesign.com/build/startup/)

---

### Step 13.15 — `STEPPER_BUZZ` the extruder

(no image — see text)

**Parts:** none.

**Do:** Send `STEPPER_BUZZ STEPPER=extruder` with no filament loaded.

**Check:** The Clockwork 2 gears turn back and forth. Direction is not tested here — it is tested when you first extrude, in Step 13.40. If nothing moves, check `[extruder] step_pin: nhk:PB8 / dir_pin: nhk:PB9 / enable_pin: !nhk:PC14` — these are the **V2** pins; the V1 config's `gpio23/24/25` will silently do nothing on this board.

---

### Step 13.16 — Correct any wrong motor or wrong direction

(no image — see text)

**Parts:** none.

**Do:** Fix what Steps 13.13–13.15 found, one cause at a time.
- **Nothing moved:** check `enable_pin` and `step_pin`, and that the driver has power.
- **Buzzed but did not travel 1 mm cleanly:** stepper phase wiring — the two coil pairs are transposed in the connector.
- **The wrong motor answered:** the motors are in the wrong ports. **Power the machine down** before moving any stepper connector.
- **It moved the wrong way:** invert that stepper's `dir_pin` — add a `!` (`dir_pin: PD3` → `dir_pin: !PD3`), or remove the `!` if one is already there. `RESTART` and re-run the buzz.

**Check:** Every motor in Steps 13.13–13.15 now passes all three tests — right motor, clean motion, right direction. Do not proceed with a known-bad axis. [src](https://docs.vorondesign.com/build/startup/)

---

## Part D — Endstops and probe

### Step 13.17 — `QUERY_ENDSTOPS` with everything released

(no image — see text)

**Parts:** none.

**Do:** Send `M84` to de-energise the motors, push the toolhead to the middle of the build volume by hand, and send `QUERY_ENDSTOPS`.

```
Send: QUERY_ENDSTOPS
Recv: // x:open y:open z:open
```

**Check:** All three read `open`. If one reads `TRIGGERED` with nothing pressing it, do **not** just add a `!` — all stock Voron endstops are normally-closed switches to ground, so an inverted reading almost always means a wiring fault. [src](https://docs.vorondesign.com/build/startup/)

⚠ Rev D+ / LDO: if your XY endstop cables are labelled **"X Stop / Y Stop"** instead of **"XES / YES"**, you have the mis-pinned batch and both X and Y will misbehave here. Re-pin per LDO's guide before going further. [src](https://docs.ldomotors.com/en/guides/XY_Endstop_Cable_Reconnecting_Guide) (survey §4.4 #14)

---

### Step 13.18 — X endstop by hand

(no image — see text)

**Parts:** none.

**Do:** Push the toolhead all the way to the **right** until you hear the endstop pod click, hold it there, and send `QUERY_ENDSTOPS`.

```
Send: QUERY_ENDSTOPS
Recv: // x:TRIGGERED y:open z:open
```

**Check:** Only `x` changes. Push the toolhead back to the middle and confirm it returns to `open`. If the toolhead cannot reach the switch, look for a rubber rail stopper still on the rail, then for a racked gantry.

---

### Step 13.19 — Y endstop by hand

(no image — see text)

**Parts:** none.

**Do:** Push the gantry all the way to the **back** until the endstop clicks, hold, and send `QUERY_ENDSTOPS`.

```
Send: QUERY_ENDSTOPS
Recv: // x:open y:TRIGGERED z:open
```

**Check:** Only `y` changes, and it releases when you move the gantry forward again.

---

### Step 13.20 — Z endstop (the LDO nozzle probe) by hand

![LDO nozzle probe installed](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/z_stop_final.jpg)

**Parts:** none.

**Do:** Press the nozzle probe's sliding shaft down with a finger until the D2F switch clicks, hold, and send `QUERY_ENDSTOPS`.

```
Send: QUERY_ENDSTOPS
Recv: // x:open y:open z:TRIGGERED
```

**Check:** Only `z` changes. Release the shaft: it must spring back up **freely** and read `open` again. If it is sticky, back off the pulley set screw — its job is only to stop the shaft falling out, not to grip it. This is the part that defines Z=0 for every print you will ever make on this machine. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d)

---

### Step 13.21 — `QUERY_PROBE` on the inductive probe

(no image — see text)

**Parts:** none.

**Do:** *(Brought forward from the wizard's Probe Check page, which sits five pages later — safe here because the gantry is high and nothing is homed.)* With the gantry still high and well clear of the bed, send `QUERY_PROBE`. Then hold a steel offcut (or the flex plate) up under the probe face and send it again.

```
Send: QUERY_PROBE
Recv: // probe: open

  (metal close to the probe)

Send: QUERY_PROBE
Recv: // probe: TRIGGERED
```

**Check:** `open` when far, `TRIGGERED` when metal is close. If it is stuck one way, check ground/signal/24 V at the probe and that `[probe] pin: nhk:PC15` matches where it is actually plugged. If the sense is inverted, add a `!` (`pin: !nhk:PC15`). [src](https://docs.vorondesign.com/build/startup/)

⚠ Rev D+ / LDO: the PROBE port is **JST-PH2.0** on Rev D+ and is **24 V only**. Also confirm the probe body still carries the supplied fibreglass tape on the **front and sides only — not the back and not the bottom** (manual p.143 / LDO note); tape on the sensing face changes the trigger height. (survey §4.1 ③, §4.2 p.143)

---

## Part E — Homing and machine coordinates

### Step 13.22 — Home X, with an abort ready

![Mainsail control panel](https://raw.githubusercontent.com/VoronDesign/Voron-Documentation/master/build/startup/images/mainsail_controls.png)

**Parts:** none.

**Do:** First *test* your stop: press the E-stop on the touchscreen and confirm Klipper shuts down, then `FIRMWARE_RESTART` to bring it back. Now have `RESTART` typed and unsent in the console. Send `G28 X`.

**Check:** The toolhead lifts slightly (that is `[safe_z_home] z_hop: 10`), then travels to the **right** until it hits the X endstop, backs off 5 mm and re-touches. Any other direction: send the abort, note what happened, and still go on to test Y before changing anything — you need both results to read the chart. [src](https://docs.vorondesign.com/build/startup/)

---

### Step 13.23 — Home Y, then read the chart

![Voron V2 stepper locations and configuration guide](https://raw.githubusercontent.com/VoronDesign/Voron-Documentation/master/build/startup/images/V2-motor-configuration-guide.png)

**Parts:** none.

**Do:** Send `G28 Y`. Then compare what X and Y actually did against the chart.

**Check:** The toolhead travels to the **back** until it hits the Y endstop. To correct:
- Match your observed X/Y arrow pair to a column in the **upper** block of the chart, then invert `dir_pin` on the stepper(s) that column marks *Inverted* — `[stepper_x]` is motor **B**, `[stepper_y]` is motor **A**.
- If your observation matches the **lower (orange)** block, the motors themselves are swapped: **power down**, physically exchange the A and B connectors at the board, power up, and re-test.
- If the gantry moves *downward* first instead of sideways, your Z stepper directions are reversed — go back to Step 13.16.

[src](https://docs.vorondesign.com/build/startup/)

---

### Step 13.24 — Bed locating: line up the Z endstop and set the bed gap

![LDO nozzle probe, installation](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/z_stop_install_3.jpg)

**Parts:** none — repositioning parts already fitted in Ch 09.

**Do:** `G28 X Y`, then jog the toolhead left along the rear of the machine until the nozzle is in line with the nozzle probe. Loosen the probe's two M3×25 SHCS and slide the whole probe along the extrusion until the shaft is centred **directly under the nozzle**. Re-tighten. Then check the bed: there must be a 2–3 mm gap between the back edge of the build plate and the probe shaft.

**Check:** Looking straight down, the nozzle tip is over the middle of the probe shaft, and the plate does not touch the shaft anywhere across its travel. If the bed fouls the shaft, loosen the bed and shift it forward — this is your last chance to do it easily. [src](https://docs.vorondesign.com/build/startup/)

---

### Step 13.25 — Define the 0,0 point

(no image — see text)

**Parts:** none.

**Do:** Send `M84`, then push the toolhead by hand to the front-left corner. If it binds before the nozzle gets near the corner, stop — that is racking or a mechanical fault, not a config problem. Then `G28 X Y` and jog to X0 Y0 using the interface, watching for skipping as it approaches the corner.

**Check:** The nozzle sits over the plate, within about 5 mm of the front-left corner, with no skipping on the way. To correct, change `position_endstop` **and** `position_max` together, on the affected axis only:
- nozzle too far **into** the bed → **increase** both (e.g. +2 mm on `[stepper_x]` moves 0,0 2 mm left)
- nozzle **beyond** the bed edge → **decrease** both

`FIRMWARE_RESTART` after any edit and re-check. [src](https://docs.vorondesign.com/build/startup/)

---

### Step 13.26 — Record the Z endstop coordinate into `[safe_z_home]`

(no image — see text)

**Parts:** none.

**Do:** `G28 X Y`, jog the nozzle back to directly over the probe shaft from Step 13.24, and send `M114`.

```
Send: M114
Recv: X:163.500 Y:350.000 Z:10.000 E:0.000
```

Copy the X and Y values into `[safe_z_home] home_xy_position:` replacing the placeholder `-10,-10`. `FIRMWARE_RESTART`.

**Check:** The values are yours, not the example above `(verify on bench)`. Until you do this, a full `G28` fails with `Move out of range: -10.000 -10.000 …` because the placeholder is outside `position_min: 0`. If you later re-calibrate the X or Y endstop, come back and re-set these. [src](https://docs.vorondesign.com/build/startup/)

---

### Step 13.27 — Full `G28`

(no image — see text)

**Parts:** none.

**Do:** Send `G28` and watch the whole sequence: X to the right, Y to the back, then a move to the `[safe_z_home]` coordinate and a slow descent onto the nozzle probe.

**Check:** Z homes on the probe with a first touch at `homing_speed: 8`, a 3 mm retract and a second touch at 3 mm/s. The nozzle presses the shaft, not the printed body. After homing, `[stepper_z] position_endstop: -0.5` (the stock value) leaves the nozzle deliberately *high* — a safe placeholder that Step 13.35 will replace. Do not send the nozzle to Z0 yet.

---

## Part F — Probe accuracy, cold

### Step 13.28 — `PROBE_ACCURACY` at the bed centre, cold

(no image — see text)

**Parts:** none.

**Do:** `G28`, then `G0 X175 Y175 Z10 F6000`, then `PROBE_ACCURACY`.

```
Send: PROBE_ACCURACY
Recv: // PROBE_ACCURACY at X:175.000 Y:175.000 Z:10.000 (samples=10 retract=3.000 speed=10.0 lift_speed=10.0)
Recv: // probe: at 175.000,200.000 bed will contact at z=2.077500
      ... (8 more)
Recv: // probe: at 175.000,200.000 bed will contact at z=2.075000
Recv: // probe accuracy results: maximum 2.080000, minimum 2.075000, range 0.005000,
      average 2.077250, median 2.077500, standard deviation 0.001803
```

**Check:** Standard deviation **< 0.003 mm** and the ten values are not marching steadily one way. A cold machine can pass this; the same test hot is the one that gates QGL (Step 13.32). Values that trend are mechanical, not electrical: check the Z drive pulley grub screws and the four Z belt tensions. Values that scatter randomly are usually probe mounting or cable. [src](https://docs.vorondesign.com/build/startup/)

Note: `[probe] y_offset: 25.0`, so the probe sits 25 mm behind the nozzle — that is why the reported probe Y is 200 when the nozzle is at 175. Older Klipper prints these lines as `probe at 175.000,200.000 is z=2.077500`; same thing.

---

## Part G — PID, before QGL

### Step 13.29 — PID tune the bed at 100 °C

(no image — see text)

**Parts:** none.

**Do:** Move the nozzle to the bed centre, 5–10 mm above the surface, then run the calibration. It takes about 10 minutes; leave it alone.

```
Send: G0 X175 Y175 Z10 F6000
Send: PID_CALIBRATE HEATER=heater_bed TARGET=100
      ... ~10 min ...
Recv: // PID parameters: pid_Kp=58.437 pid_Ki=2.347 pid_Kd=363.769
Recv: // The SAVE_CONFIG command will update the printer config file
Recv: // with these parameters and restart the printer.
Send: SAVE_CONFIG
```

**Check:** `SAVE_CONFIG` restarts Klipper and the new `pid_Kp/Ki/Kd` appear in the auto-generated block at the bottom of `printer.cfg`. Your numbers will differ from the example. [src](https://docs.vorondesign.com/build/startup/)

---

### Step 13.30 — PID tune the hotend at 245 °C with the part fan at 25 %

(no image — see text)

**Parts:** none.

**Do:** `G28` first — `SAVE_CONFIG` restarted the printer. Then set the part fan to 25 % and run the hotend calibration; about 5 minutes.

```
Send: G28
Send: M106 S64
Send: PID_CALIBRATE HEATER=extruder TARGET=245
      ... ~5 min ...
Recv: // PID parameters: pid_Kp=26.213 pid_Ki=1.304 pid_Kd=131.721
Send: SAVE_CONFIG
Send: M107
```

**Check:** Saved and restarted. Running the hotend PID *with* the part fan at 25 % is deliberate — it tunes for the disturbance the fan actually causes in a print. [src](https://docs.vorondesign.com/build/startup/)

---

## Part H — Quad gantry level

### Step 13.31 — Heat soak: bed 100 °C, hotend 150 °C

(no image — see text)

**Parts:** none.

**Do:** `G28`. Set the bed to 100 °C and the hotend to 150 °C. Put the side and top panels loosely in place so the chamber comes up to temperature (you will take them off again for Ch 06b). Wait 10–20 minutes from cold.

**Check:** `chamber_temp` has stopped climbing and the bed is holding 100 °C without hunting. 150 °C on the hotend is below `min_extrude_temp: 170` on purpose — hot enough to expand the toolhead realistically, cold enough that nothing oozes onto the plate. [src](https://docs.vorondesign.com/build/startup/)

---

### Step 13.32 — `PROBE_ACCURACY` hot — the gate on everything downstream

(no image — see text)

**Parts:** none.

**Do:** With the printer at temperature, `G0 X175 Y175 Z10 F6000` and run `PROBE_ACCURACY` again.

**Check:** σ **< 0.003 mm** *and* no trend across the ten samples. If the values are still drifting, wait another 5 minutes and repeat. Write down how long it took to stabilise — that number is your print-start soak time forever after. **Do not run QGL until this passes.** A drifting probe produces a QGL that looks like it converged and is not level. [src](https://docs.vorondesign.com/build/startup/) (survey §4.4 #16)

---

### Step 13.33 — `QUAD_GANTRY_LEVEL`

(no image — see text)

**Parts:** none.

**Do:** Send `QUAD_GANTRY_LEVEL`. It probes the four points (`50,25 / 50,275 / 300,275 / 300,25`), computes each Z actuator's height against the gantry corners, adjusts, and repeats until the probed range is inside `retry_tolerance: 0.0075` or it runs out of `retries: 5`.

```
Send: QUAD_GANTRY_LEVEL
Recv: // Gantry-relative probe points:
Recv: // 0: 0.052500 1: 0.031250 2: -0.018750 3: 0.005000
Recv: // Actuator Positions:
Recv: // z: 0.061250 z1: 0.030000 z2: -0.022500 z3: 0.008750
Recv: // Average: 0.019375
Recv: // Making the following Z adjustments:
Recv: // stepper_z = -0.041875
Recv: // stepper_z1 = -0.010625
Recv: // stepper_z2 = 0.041875
Recv: // stepper_z3 = 0.010625
Recv: // Retries: 0/5 Probed points range: 0.071250 tolerance: 0.007500
      ... repeats ...
Recv: // Retries: 2/5 Probed points range: 0.005250 tolerance: 0.007500
```

**Check:** `Probed points range` **shrinks** on every pass and ends below 0.007500. Watch that number, not the individual adjustments. If it grows, or if it stalls well above tolerance, the gantry is racked — go to Step 13.34 now rather than retrying. [src](https://docs.vorondesign.com/build/startup/)

---

### Step 13.34 — Hand off to Ch 06b: square the gantry, then re-tension A/B

![Fully release A/B tension before squaring](https://raw.githubusercontent.com/VoronDesign/Voron-Documentation/master/build/mechanical/images/v2_gantry_squaring/Gantry-ABTension.png)

**Parts:** none — Ch 06b and Ch 07 hardware only.

**Do:** Leave this chapter here and run [**Ch 06b — Gantry squaring**](06-z-axis-and-gantry-squaring.md), which needs exactly what you now have: a printer that homes and QGLs. It starts by raising the idle timeout (`SET_IDLE_TIMEOUT TIMEOUT=99999`), homing, QGL-ing, disabling *only* the A/B motors (`SET_STEPPER_ENABLE STEPPER=stepper_x ENABLE=0`, same for `stepper_y`), **fully releasing A/B belt tension**, taking the side panels off and dropping the lower Z joints. When squaring is done, re-tension both A/B belts at Ch 06b step 06b.15 — the target, the method and the verification live in [**Ch 14 Step 14.4**](14-calibration.md#step-144-set-ab-belt-tension-to-110-hz-over-a-150-mm-span), which is authoritative for final belt tension.

**Check:** Do not skip this even if Step 13.33 converged — a QGL that converges on a racked gantry is a levelled parallelogram. Squaring undoes belt tension by design, which is why Ch 07's tensioning is only *provisional* until now (survey §5.2 W1). Come back here when the belts are at final tension. [src](https://docs.vorondesign.com/build/mechanical/v2_gantry_squaring.html)

---

### Step 13.35 — Re-heat and re-QGL after squaring

(no image — see text)

**Parts:** none.

**Do:** Panels back on, bed to 100 °C, hotend to 150 °C, soak for the time you recorded in Step 13.32. Then `G28`, `PROBE_ACCURACY` (σ < 0.003 mm), `QUAD_GANTRY_LEVEL`.

**Check:** QGL now converges in fewer passes and with a smaller starting range than it did in Step 13.33. If it does not, the squaring did not take — go back to Ch 06b. Only when this passes is the machine's geometry final, and only then are the Z offset and the bed mesh worth measuring.

---

## Part I — Z offset (Z=0)

### Step 13.36 — `Z_ENDSTOP_CALIBRATE` and the paper test

![Mainsail manual probe dialog](https://raw.githubusercontent.com/VoronDesign/Voron-Documentation/master/build/startup/images/mainsail_manual_probe.png)

**Parts:** one sheet of printer paper.

**Do:** With the machine still hot and levelled, `G28`, move the nozzle to the bed centre, wipe any ooze off the nozzle, put the paper under it and run `Z_ENDSTOP_CALIBRATE`. Step down with `TESTZ Z=-1` until you are close, then `TESTZ Z=-0.1`; `TESTZ Z=0.1` backs off if you overshoot.

```
Send: Z_ENDSTOP_CALIBRATE
Recv: // Starting manual Z probe. Use TESTZ to adjust position.
Recv: // Finish with ACCEPT or ABORT command.
Recv: // Z position: ?????? --> 9.800 <-- ??????
Send: TESTZ Z=-1
Recv: // Z position: ?????? --> 8.800 <-- 9.800
      ... down to ...
Send: TESTZ Z=-0.1
Recv: // Z position: 0.150 --> 0.250 <-- 0.350
Send: ACCEPT
Recv: // stepper_z: position_endstop: -0.310
Recv: // The SAVE_CONFIG command will update the printer config file
Recv: // with the above and restart the printer.
Send: SAVE_CONFIG
```

**Check:** Stop when you feel light drag on the paper — the paper still slides, but with resistance. **You are doing this hot, and Klipper assumes cold: send one extra `TESTZ Z=-0.1` before `ACCEPT`.** The small back-and-forth Klipper does on tiny moves is deliberate backlash compensation; the final position is the one you asked for. [src](https://docs.vorondesign.com/build/startup/)

Note: this sets Z=0 from the **nozzle probe**, not the inductive probe. `[probe] z_offset: 0` stays uncalibrated on purpose — that probe is used only for QGL and mesh shape.

---

### Step 13.37 — Sanity-check Z=0

(no image — see text)

**Parts:** paper.

**Do:** `G28`, then `G0 X175 Y175 Z0 F1200`. Slide the paper under the nozzle.

**Check:** The paper drags but is not pinned or torn, and the nozzle has not touched the PEI. If it is wrong, re-run Step 13.36 — do not hand-edit `position_endstop` yet. Remember the sign: **increasing `[stepper_z] position_endstop` brings the nozzle closer to the bed.**

---

## Part J — Bed mesh

### Step 13.38 — Confirm the `[bed_mesh]` section from Ch 12

(no image — see text)

**Parts:** none.

**Do:** The LDO config ships **no `[bed_mesh]` section at all** — but `PRINT_END` calls `BED_MESH_CLEAR`, which will print `Unknown command:"BED_MESH_CLEAR"` at the end of every print until one exists. **Ch 12 Step 12.34 owns that block.** Do not retype it here: open `printer.cfg`, confirm the section is present and unchanged, then `FIRMWARE_RESTART`.

**Check:** `grep -A4 '^\[bed_mesh\]' ~/printer_data/config/printer.cfg` returns the Step 12.34 block, Klipper comes back `Ready` with no `[bed_mesh]` error, and `BED_MESH_CLEAR` is accepted at the console. If Klipper rejects the section, the cause is a range error — `mesh_min`/`mesh_max` are **probe** coordinates and `[probe] y_offset: 25.0` puts the nozzle 25 mm in front of the probe. Fix it in Step 12.34, not here, so the two chapters cannot drift apart again. (survey §4.4 #15)

---

### Step 13.39 — `BED_MESH_CALIBRATE`

(no image — see text)

**Parts:** none.

**Do:** Still hot and still levelled: `G28`, `QUAD_GANTRY_LEVEL`, `G28`, then `BED_MESH_CALIBRATE`. 49 probe points takes a few minutes.

```
Send: BED_MESH_CALIBRATE
      ... 49 probes ...
Recv: // Mesh Bed Leveling Complete
Recv: // Bed Mesh state has been saved to profile [default]
Recv: // for the current session.  The SAVE_CONFIG command will
Recv: // update the printer config file and restart the printer.
Send: SAVE_CONFIG
```

**Check:** Send `BED_MESH_OUTPUT` and look at the spread. A cast-and-ground 350 plate at 100 °C should land inside roughly ±0.10 mm; a corner that is 0.3 mm out of family points at a bed screw torqued cold (Ch 03) rather than at a bad plate. Mesh **after** QGL, always, and re-mesh whenever you change the bed or the plate.

Tip: this mesh is a hot mesh at 100 °C. It is not valid for a 60 °C PLA bed — take a second profile later if you print cold materials.

---

## Part K — First print

The first print is the last check in this chapter, not the start of tuning. The cube is printed **once**, here. `rotation_distance` is Ch 14's topic and Step 13.40 only borrows it, because the cube cannot be judged without it; the cube's *measurement* is Ch 14's and stays there. Keep the cube.

### Step 13.40 — Set the extruder rotation distance (Ch 14 procedure)

(no image — see text)

**Parts:** ASA filament; caliper or steel rule; masking tape.

**Do:** Go and run [**Ch 14 Step 14.7 — Rotation-distance check**](14-calibration.md#step-147-rotation-distance-check-100-mm-extrusion) now, then come back here. Ch 14 owns `rotation_distance` — the formula, the Clockwork 2 starting values and the two ways of extruding 100 mm are all there, and are not repeated here.

**Check:** 100 mm requested measures 99.5–100.5 mm. This has to be right **before** the first print: extrusion error left in place looks exactly like flow and first-layer problems for the rest of the build. [src](https://docs.vorondesign.com/build/startup/)

---

### Step 13.41 — Slice the Voron cube

(no image — see text)

**Parts:** `Voron_Design_Cube_v7.stl`; ASA.

**Do:** Load [`Voron_Design_Cube_v7.stl`](https://github.com/VoronDesign/Voron-2/tree/Voron2.4/STLs/Test_Prints) — the same file batch B00 printed on the Prusa. It is exactly **30.000 × 30.000 × 30.000 mm**. Slice it at **hotend 260 °C, bed 110 °C, chamber 50 °C, no XY size compensation, shrinkage compensation 0 %** — the same overrides the Prusa profile uses, so the two cubes are comparable ([print/00-slicer-setup.md](print/00-slicer-setup.md)). No supports, seam to the rear.

**Check:** The sliced preview shows no supports and the seam at the rear.

Tip: the Voron slicer guide's own starting point is 240 °C / 100 °C / 92 % flow for ABS. Use 260/110 here anyway — it is the Prusament ASA figure, and it is what makes this cube comparable with the B00 reference you caliper it against at [Ch 14 Step 14.11](14-calibration.md#step-1411-caliper-the-cube-against-the-prusa-printed-one). [src](https://docs.vorondesign.com/build/slicer/first_print.html)

---

### Step 13.42 — Print it, and set the first-layer squish

![Voron cereal](https://raw.githubusercontent.com/VoronDesign/Voron-Documentation/master/build/slicer/images/voron_cereal.png)

**Parts:** the sliced cube; clean flex plate; IPA.

**Do:** Upload, start it, and **watch the whole first layer**. Live-adjust Z in 0.01 mm steps while it lays down — the "Z Offset" babystep control in Fluidd/Mainsail does the same thing:

```
SET_GCODE_OFFSET Z_ADJUST=-0.01 MOVE=1     ; closer to the bed
SET_GCODE_OFFSET Z_ADJUST=0.01 MOVE=1      ; further away
```

Once the squish is right, make it permanent with `Z_OFFSET_APPLY_ENDSTOP` then `SAVE_CONFIG`. Keep the cube.

**Check:** On smooth PEI the bottom has **no gaps between the beads and no ridging**, and you can still see the individual lines; completely featureless and glassy is too much squish. `stepper_z: position_endstop` in the saved block has moved by the amount you babystepped — babystepping alone is discarded on restart. Do **not** use `Z_OFFSET_APPLY_PROBE`: this machine's Z reference is the LDO nozzle probe, not the inductive probe. Do not touch input shaper or pressure advance until this print has finished successfully. [src](https://ellis3dp.com/Print-Tuning-Guide/articles/first_layer_squish.html) (survey §3.3)

---

### Step 13.43 — Shut down properly

(no image — see text)

**Parts:** none.

**Do:** Use the web interface's **Shutdown** (host shutdown), wait for the Pi's activity LED to go dark, and only then switch the machine off at the inlet. Take a copy of `printer.cfg` off the Pi.

**Check:** You have a backup of the config with all four `SAVE_CONFIG` blocks (bed PID, hotend PID, `position_endstop`, bed mesh) in it. Pulling power on a running Pi corrupts the SD card and costs you Ch 12 all over again. [src](https://docs.vorondesign.com/build/startup/)

---

## What if — first-start failures and what they actually mean

| Symptom | Most likely cause | Fix |
|---|---|---|
| A temperature climbs with nothing commanded | Heater energised through a wiring fault | Cut power at the switch. Back to Ch 10 — do not "just watch it" |
| Thermistor reads a wild or jumping value | Crimp, or a PH2.0 housing half-seated / in the wrong header | Re-seat, check continuity. Rev D+: uses **PH2.0**, not the guide's XH2.5 |
| Hotend heats when you command the bed (or vice versa) | Thermistor pair or heater pair swapped | Swap at the board, power off first |
| Bed does not heat, SSR LED **on** | Fault on the mains side of the SSR | Check LOAD 1 / LOAD 2 and the bed L/N |
| Bed does not heat, SSR LED **off** | Control polarity reversed | Leviathan **+** → SSR **INPUT 3**, **−** → INPUT 4 |
| A fan never starts | Wrong port, wrong voltage jumper, or the keyed 2×5 (10-pin) toolhead header seated backwards | Check the port against the config; Rev D+: header is keyed — if it will not drop in, it is backwards. BLDC fans do not spin backwards on reversed polarity, they do nothing or burn out |
| `STEPPER_BUZZ` moves nothing | `enable_pin`/`step_pin`, or no driver power | Check the pins; check the HV/24 V rail |
| `STEPPER_BUZZ` buzzes without travelling 1 mm | Stepper coil pairs transposed in the connector | Re-pin the connector so each coil is a pair. Power off first |
| **A motor moves the wrong way** | `dir_pin` polarity | Add or remove `!` on that stepper's `dir_pin`, `RESTART`, re-buzz |
| The wrong motor answers | Motors in the wrong ports | Power **off**, move the connector, power on. Never hot-swap a stepper |
| `G28 X` sends the gantry *down* first | Z stepper directions reversed | Fix Z `dir_pin`s before touching A/B |
| X and Y both move, but the toolhead goes diagonally / the wrong axis | A and B swapped, or one inverted | Read the V2 configuration chart; upper block → invert a `dir_pin`; lower (orange) block → physically swap A and B |
| An endstop reads `TRIGGERED` untouched | Wiring, not polarity | Stock Voron endstops are N.C. to ground — a needed `!` usually means a wiring fault. Fix the wiring |
| Endstop unreachable by the toolhead | Rubber rail stopper still on the rail, or racked gantry | Remove stoppers; then Ch 06b |
| `G28` → `Move out of range: -10.000 -10.000 …` | `[safe_z_home] home_xy_position` still the `-10,-10` placeholder | Step 13.26 |
| Homing overshoots into the frame | `position_endstop`/`position_max` still at the 250 default | Step 13.5 |
| `QUERY_PROBE` stuck `open` or stuck `TRIGGERED` | Ground/signal/24 V, wrong `[probe] pin`, or a voltage-select jumper | Check wiring first, then `pin: !nhk:PC15` |
| **Probe triggers too early** (large gap at trigger) | Probe mounted too high in the retainer bracket, or fibreglass tape on the sensing face | Lower the probe in the bracket so it triggers ~2 mm above the plate; strip tape from the **back and bottom** — front and sides only |
| **Probe triggers too late** (nozzle nearly touching, or the probe grazes the plate) | Probe mounted too low | Raise it in the bracket. It must clear the plate and any clips at every mesh point |
| `PROBE_ACCURACY` σ high but stable | Probe mount, cable strain, or `[probe] speed` too fast | Check the bracket is tight; try a lower `speed` |
| `PROBE_ACCURACY` values trending one way | Thermal, or mechanical: Z pulley grub screws, uneven Z belts | Soak longer; then check all four Z belts and the pulley set screws |
| `Probe samples exceed samples_tolerance` | Same causes; `samples_tolerance: 0.006` is tight by design | Fix the cause, do not widen the tolerance |
| **QGL does not converge** — `Probed points range` stalls or grows | **Gantry racking** | Step 13.34 → Ch 06b, then re-tension A/B to 110 Hz and re-QGL |
| QGL: `Retries aborting: Probed points range is increasing. Possibly Z motor numbering is wrong` | Z motors on the wrong drivers | Recheck the Z map: Z0 front-left → `STEPPER-0`, Z1 rear-left → `-1`, Z2 rear-right → `-2`, Z3 front-right → `-3` |
| QGL: `Aborting quad_gantry_level required adjustment … is greater than max_adjust` | Gantry too far out of level to correct in software | `M84`, level the gantry by hand against the frame, `G28`, retry |
| QGL "out of bounds" / cannot reach the probe point | Gantry far from level, or wrong `gantry_corners` | `FIRMWARE_RESTART`, hand-level, `G28`, retry; confirm the 350 corners `-60,-10 / 410,420` |
| `Unknown command:"BED_MESH_CLEAR"` at the end of a print | No `[bed_mesh]` section | Step 13.38. It is a warning, not a failure — but you have no mesh |
| First layer is right at the front and wrong at the back (or similar) | Meshed before QGL, or mesh taken cold | Re-run: `G28` → `QUAD_GANTRY_LEVEL` → `G28` → `BED_MESH_CALIBRATE`, hot |

---

## Checkpoint 13

Tick every line before you start Ch 14.

- [ ] Checkpoint #1 (Ch 10) was passed before this chapter began, with a multimeter, unplugged.
- [ ] `STATUS` returns `Klipper state: Ready`, and both MCUs are present — `stm32f446xx` (or `stm32h743xx` on a V1.3 board) and `stm32g0b1xx`.
- [ ] Extruder, bed and chamber all report room temperature at rest and none of them drifts upward untouched.
- [ ] Both heaters heat and cool on command; the SSR LED tracks the bed.
- [ ] All five fans verified: hotend (SB bottom), part cooling (SB top), bay PCB fan, Nevermore filter fan, and the chamber LEDs plus all three Stealthburner LEDs.
- [ ] All seven motors pass `STEPPER_BUZZ` — correct motor, clean motion, correct direction.
- [ ] `QUERY_ENDSTOPS` reads `x:open y:open z:open` at rest and each endstop triggers alone; the nozzle probe shaft springs back freely.
- [ ] `QUERY_PROBE` toggles `open` / `TRIGGERED` with metal, and the probe's fibreglass tape is front-and-sides only.
- [ ] `G28` completes on all three axes; 0,0 lands within 5 mm of the front-left corner of the plate with no skipping.
- [ ] `[safe_z_home] home_xy_position` holds your measured Z-endstop coordinate, not `-10,-10`.
- [ ] Bed and hotend PID tuned and `SAVE_CONFIG`-ed; `PROBE_ACCURACY` hot shows σ < 0.003 mm with no trend, and you wrote down the soak time.
- [ ] Ch 06b gantry squaring done, A/B belts re-tensioned to 110 Hz / 150 mm span and matched, and QGL re-run and converged afterwards.
- [ ] `Z_ENDSTOP_CALIBRATE` done hot with the extra `TESTZ Z=-0.1`, and saved; bed mesh taken hot **after** QGL and saved.
- [ ] `rotation_distance` set (Ch 14 Step 14.7), and the Voron cube printed here, first-layer squish committed with `Z_OFFSET_APPLY_ENDSTOP`, cube kept for Ch 14's measurement.
- [ ] `printer.cfg` backed up off the Pi, with all four `SAVE_CONFIG` blocks in it.

---

## Common mistakes

- **Running QGL before PID, or cold.** A drifting probe gives a QGL that reports success and leaves the gantry unlevel; you then chase it through first-layer tuning for a week. PID first, soak to temperature, and gate on `PROBE_ACCURACY` σ < 0.003 mm. (survey §3.3, §4.4 #16)
- **Setting the Z offset and the bed mesh before squaring the gantry.** Ch 06b fully releases A/B tension and drops the Z joints — everything measured before it is scrap. Square first, re-tension, re-QGL, *then* Z=0 and mesh.
- **Adding a `!` to an endstop pin to make a `TRIGGERED` reading go away.** Every stock Voron endstop is normally-closed to ground. If it needs inverting, you almost certainly have a wiring fault that will fail intermittently later.
- **Moving a stepper connector with the power on.** Back-EMF from a spinning or hot-swapped motor kills drivers, and you will not find out until the next homing move. Power down for every connector change. (survey §4.4 #10)
- **Forgetting the extra `TESTZ Z=-0.1` when calibrating Z=0 hot.** Klipper's paper test assumes a cold machine; skip the correction and every first layer will be slightly under-squished.
- **Trusting babystepping.** The Z Offset slider is discarded on restart unless you commit it with `Z_OFFSET_APPLY_ENDSTOP` followed by `SAVE_CONFIG`.

---

## Next

[**Ch 14 — Calibration and tuning**](14-calibration.md): caliper the cube against the Prusa-printed reference, then input shaper → pressure advance → extrusion multiplier → first-layer squish, in that order, and only now that a cube has printed.
