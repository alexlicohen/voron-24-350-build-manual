# Chapter 15 — Troubleshooting index

Every failure this manual already knows about, filed by **symptom** instead of by chapter. Nothing here is new advice: each row points at the step, checkpoint, warning callout or *Common mistakes* bullet that owns the fix, in Chapters 00–14. Use it at the bench when what you have is *"the X carriage binds near one end"* rather than *"Chapter 05"*.

**Time:** none — this is a reference page, not a build chapter.

**Prerequisites:** none. Readable at any point in the build.

**Tools:** whatever the step you land on calls for. The multimeter rows all assume the machine is **unplugged** — see [Ch 00a Step 00a.4](00a-mains-safety.md#step-00a4-test-the-meter-before-you-trust-it-and-again-after).

**Printed parts:** none. **Hardware:** none.

**Read first**

- **Find the symptom, then go to the step. Do not fix it from this page.** The rows are compressed to fit a table; the step has the orientation, the photo and the exact numbers.
- **This index does not invent fixes.** If your symptom is not here, it is not a symptom this manual has an answer for — go to [Not covered here](#not-covered-here-where-to-ask) and ask, with the four pieces of information listed there.
- **Anything smelling, smoking or tripping a breaker is not a troubleshooting problem.** Cut power at the wall and go to [Ch 00a Step 00a.12](00a-mains-safety.md#step-00a12-decide-now-what-you-do-when-it-smokes-trips-or-bites).
- **Ch 13's own [What if](13-initial-startup.md#what-if-first-start-failures-and-what-they-actually-mean) table is the primary source for first-start faults** and is more detailed than the rows here. This page indexes it; it does not replace it.
- Order matters more than any single fix: PID → soak → probe accuracy → QGL → square → Z=0 → mesh. A symptom that appears out of that order is usually the order, not the part ([Ch 13 Common mistakes](13-initial-startup.md#common-mistakes)).

---

## Motion — homing, axes, steppers, endstops

| Symptom | Likely cause | Fix | Owned by |
|---|---|---|---|
| `STEPPER_BUZZ` does nothing on one motor | `enable_pin` / `step_pin`, or no driver power | check the pins, then the HV / 24 V rail | [13.16](13-initial-startup.md#step-1316-correct-any-wrong-motor-or-wrong-direction), [10.25](10-wiring.md#step-1025-psu-leviathan-hv-stepper-supply) |
| `STEPPER_BUZZ` buzzes but does not travel 1 mm | stepper coil pairs transposed in the connector | re-pin so each coil is a pair — power off first | [13.16](13-initial-startup.md#step-1316-correct-any-wrong-motor-or-wrong-direction) |
| A motor runs the wrong way | `dir_pin` polarity | add or remove `!` on that stepper, `RESTART`, re-buzz | [13.16](13-initial-startup.md#step-1316-correct-any-wrong-motor-or-wrong-direction) |
| The wrong motor answers a buzz | motors on the wrong ports | power **off**, move the connector, power on. Never hot-swap a stepper | [13.16](13-initial-startup.md#step-1316-correct-any-wrong-motor-or-wrong-direction), [10.40](10-wiring.md#step-1040-tag-every-stepper-cable-before-you-plug-anything-in) |
| `G28 X` drives the gantry *down* first | Z stepper directions reversed | fix the Z `dir_pin`s before touching A or B | [13.16](13-initial-startup.md#step-1316-correct-any-wrong-motor-or-wrong-direction) |
| X and Y both move but the toolhead travels diagonally | A and B swapped, or one inverted | upper block on the V2 chart → invert a `dir_pin`; lower (orange) block → physically swap A and B | [13.16](13-initial-startup.md#step-1316-correct-any-wrong-motor-or-wrong-direction) |
| Homing overshoots into the frame | `position_endstop` / `position_max` still at the 250 default | prove the 350 edits are live | [13.5](13-initial-startup.md#step-135-prove-the-350-mm-config-edits-are-live), [12.24](12-software.md#step-1224-350-mm-stepper_x-and-stepper_y) |
| An endstop reads `TRIGGERED` untouched | wiring, not polarity — stock Voron endstops are N.C. to ground | fix the wiring; do **not** add a `!` to silence it | [13.17](13-initial-startup.md#step-1317-query_endstops-with-everything-released), [Ch 13 Common mistakes](13-initial-startup.md#common-mistakes) |
| X or Y endstop never triggers, cable is labelled *X Stop / Y Stop* | LDO batch shipped with the wrong labels; needs re-pinning | read the labels, then re-pin | [10.31](10-wiring.md#step-1031-read-the-xy-endstop-cable-labels), [10.32](10-wiring.md#step-1032-repin-the-xy-endstop-cable-only-if-labelled-x-stop-y-stop) |
| The toolhead cannot reach an endstop | rubber rail stopper still on the rail, or the gantry is racked | pull the stoppers, then square the gantry | [13.1](13-initial-startup.md#step-131-clear-the-machine-and-stage-the-bench), [Ch 06b](06-z-axis-and-gantry-squaring.md#step-06b14-de-rack-the-gantry-then-tighten-the-xy-joints) |
| `G28` → `Move out of range: -10.000 -10.000 …` | `[safe_z_home] home_xy_position` still the placeholder | measure the Z endstop coordinate and write it in | [13.26](13-initial-startup.md#step-1326-record-the-z-endstop-coordinate-into-safe_z_home), [12.33](12-software.md#step-1233-z-endstop-leave-safe_z_home-deliberately-unreachable) |
| 0,0 does not land at the front-left corner of the plate | endstop coordinates not defined against the plate | re-run the 0,0 definition | [13.25](13-initial-startup.md#step-1325-define-the-00-point) |

Source: [Ch 13 — What if](13-initial-startup.md#what-if-first-start-failures-and-what-they-actually-mean) · [Ch 13 Common mistakes](13-initial-startup.md#common-mistakes) · [Ch 10 Section 5](10-wiring.md#section-5-leviathan-connections) · [Ch 12 Common mistakes](12-software.md#common-mistakes)

---

## Z, QGL and gantry squaring

| Symptom | Likely cause | Fix | Owned by |
|---|---|---|---|
| **QGL does not converge** — `Probed points range` stalls or grows | gantry racking | square the gantry in Ch 06b, re-tension A/B to 110 Hz, re-QGL | [13.34](13-initial-startup.md#step-1334-hand-off-to-ch-06b-square-the-gantry-then-re-tension-ab), [06b.14](06-z-axis-and-gantry-squaring.md#step-06b14-de-rack-the-gantry-then-tighten-the-xy-joints) |
| QGL: *"Probed points range is increasing. Possibly Z motor numbering is wrong"* | Z motors on the wrong drivers | recheck the map: Z0 front-left → `STEPPER-0`, Z1 rear-left → `-1`, Z2 rear-right → `-2`, Z3 front-right → `-3` | [13.33](13-initial-startup.md#step-1333-quad_gantry_level), [10.43](10-wiring.md#step-1043-z0z3-stepper-0-to-stepper-3) |
| QGL: *"required adjustment … is greater than max_adjust"* | gantry too far out of level to correct in software | `M84`, level by hand against the frame, `G28`, retry | [13.33](13-initial-startup.md#step-1333-quad_gantry_level) |
| QGL "out of bounds" / cannot reach a probe point | gantry far from level, or wrong `gantry_corners` | `FIRMWARE_RESTART`, hand-level, `G28`; confirm the 350 corners `-60,-10 / 410,420` | [13.33](13-initial-startup.md#step-1333-quad_gantry_level), [12.26](12-software.md#step-1226-350-mm-quad_gantry_level) |
| QGL passes but printed parts come out skewed | QGL levels in Z only — it says nothing about the X extrusion being square to Y | de-rack the gantry; QGL cannot detect racking | [Ch 06b Common mistakes](06-z-axis-and-gantry-squaring.md#common-mistakes-06b) |
| `PROBE_ACCURACY` σ high but stable | probe mount, cable strain, or `[probe] speed` too fast | check the retainer bracket is tight; try a lower `speed` | [13.32](13-initial-startup.md#step-1332-probe_accuracy-hot-the-gate-on-everything-downstream), [07.35](07-ab-belts.md#step-0735-fit-the-probe-and-its-retainer-bracket) |
| `PROBE_ACCURACY` values trending one way | frame still expanding, or Z pulley grub screws / uneven Z belts | soak longer; then check all four Z belts and the pulley set screws | [14.3](14-calibration.md#step-143-verify-thermal-stability-then-re-qgl), [14.5](14-calibration.md#step-145-set-the-four-z-belts-to-140-hz-over-150-mm) |
| `Probe samples exceed samples_tolerance` | the same causes — `samples_tolerance: 0.006` is tight by design | fix the cause; do not widen the tolerance | [13.32](13-initial-startup.md#step-1332-probe_accuracy-hot-the-gate-on-everything-downstream) |
| `QUERY_PROBE` stuck `open` or stuck `TRIGGERED` | ground / signal / 24 V, wrong `[probe] pin`, or a voltage-select jumper | check wiring first, then `pin: !nhk:PC15` | [13.21](13-initial-startup.md#step-1321-query_probe-on-the-inductive-probe), [12.29](12-software.md#step-1229-probe-omron-active-klicky-written-but-commented) |
| Probe triggers too early (large gap at trigger) | probe too high in the retainer, or tape on the sensing face | lower it so it triggers ~2 mm above the plate; tape front and sides only | [07.36](07-ab-belts.md#step-0736-set-the-probe-height), [10.30](10-wiring.md#step-1030-insulate-the-inductive-probe) |
| Probe triggers too late, or grazes the plate | probe mounted too low | raise it in the bracket; it must clear the plate and the clips at every mesh point | [07.36](07-ab-belts.md#step-0736-set-the-probe-height) |
| Z drops out of level between prints | Z pulley set screws loose or off the flat | threadlock, one screw on the flat, proper hex driver | [02.20](02-z-drives.md#step-0220-threadlock-the-80t-pulley-set-screws-and-check-your-work), [Ch 02 Common mistakes](02-z-drives.md#common-mistakes) |
| Every Z dimension is silently wrong | a 20T pulley fitted to a Z motor instead of a 16T | count teeth — `gear_ratio: 80:16` is baked into the config | [02.27](02-z-drives.md#step-0227-fit-the-16t-pulley-to-a-z-motor-at-107-mm), [Ch 02 Common mistakes](02-z-drives.md#common-mistakes) |

Source: [Ch 13 — What if](13-initial-startup.md#what-if-first-start-failures-and-what-they-actually-mean) · [Ch 06b Common mistakes](06-z-axis-and-gantry-squaring.md#common-mistakes-06b) · [Ch 02 Common mistakes](02-z-drives.md#common-mistakes) · [Ch 14 Step 14.3](14-calibration.md#step-143-verify-thermal-stability-then-re-qgl)

---

## Extrusion and hotend

| Symptom | Likely cause | Fix | Owned by |
|---|---|---|---|
| Molten plastic leaks at the heatsink on the first hot print | the Revo strain relief was not bent clear, so the nozzle never hand-tightened fully | bend the strain relief, re-seat the nozzle | [08.28](08-toolhead.md#step-0828-bend-the-strain-relief-so-the-nozzle-can-seat-fully), [Ch 08 Common mistakes](08-toolhead.md#common-mistakes) |
| Extruder will not grip or tension filament | the tension arm's M3×25 hinge pin was torqued instead of left as a hinge | back it off — it is a hinge, not a fastener | [08.19](08-toolhead.md#step-0819-hang-the-tension-arm-and-leave-it-loose), [08.21](08-toolhead.md#step-0821-set-the-tension-and-the-anti-squish-stop) |
| CW2 main body cracked while tightening the motor plate | the M3×25 pair over-tightened | the manual's own advice is to bin the part and reprint | [08.17](08-toolhead.md#step-0817-close-the-extruder-with-the-motor-plate), [Ch 08 Common mistakes](08-toolhead.md#common-mistakes) |
| Extruded length does not match the commanded 100 mm | `rotation_distance` not set for this extruder | run the 100 mm extrusion check | [14.7](14-calibration.md#step-147-rotation-distance-check-100-mm-extrusion), [13.40](13-initial-startup.md#step-1340-set-the-extruder-rotation-distance-ch-14-procedure) |
| Hotend heats when you command the bed, or vice versa | thermistor pair or heater pair swapped | swap at the board — power off first | [Ch 13 — What if](13-initial-startup.md#what-if-first-start-failures-and-what-they-actually-mean) |
| Thermistor reads a wild or jumping value | crimp, or a PH2.0 housing half-seated / in the wrong header | re-seat and check continuity — Rev D+ uses **PH2.0**, not the guide's XH2.5 | [10.55](10-wiring.md#step-1055-connector-types-on-the-v2-toolboard), [10.76](10-wiring.md#step-1076-thermistors-at-room-temperature) |
| A temperature climbs with nothing commanded | heater energised through a wiring fault | cut power at the switch and go back to Ch 10 — do not watch it | [Ch 13 — What if](13-initial-startup.md#what-if-first-start-failures-and-what-they-actually-mean), [00a.12](00a-mains-safety.md#step-00a12-decide-now-what-you-do-when-it-smokes-trips-or-bites) |
| Bed does not heat, SSR LED **on** | fault on the mains side of the SSR | check LOAD 1 / LOAD 2 and the bed L and N | [10.14](10-wiring.md#step-1014-bed-live-ssr-load-1), [10.78](10-wiring.md#step-1078-ssr-polarity-and-isolation-one-last-time) |
| Bed does not heat, SSR LED **off** | DC control polarity reversed | Leviathan **+** → SSR `INPUT 3`, **−** → `INPUT 4` | [10.27](10-wiring.md#step-1027-leviathan-heatbed-ssr-input), [13.8](13-initial-startup.md#step-138-short-heat-test-bed-to-50-c-and-watch-the-ssr) |
| PID tune of the hotend trips the temperature limit mid-run | tuning at 260 °C against `max_temp: 270` | tune at 245 °C, or raise `max_temp` to 290 first | [13.30](13-initial-startup.md#step-1330-pid-tune-the-hotend-at-245-c-with-the-part-fan-at-25), [Ch 14 Common mistakes](14-calibration.md#common-mistakes) |
| Bed takes a long time to reach 110 °C | `[heater_bed] max_power` is deliberately limited to protect the 355 mm cast plate | wait — do not raise it | [Ch 14 Common mistakes](14-calibration.md#common-mistakes) |

Source: [Ch 08 Common mistakes](08-toolhead.md#common-mistakes) · [Ch 13 — What if](13-initial-startup.md#what-if-first-start-failures-and-what-they-actually-mean) · [Ch 14 Common mistakes](14-calibration.md#common-mistakes) · [Ch 10 Section 8](10-wiring.md#section-8-pre-power-on-meter-sweep)

---

## Electronics, power and comms

| Symptom | Likely cause | Fix | Owned by |
|---|---|---|---|
| Nothing powers on at all | inlet miswired, or the machine is unplugged as designed | re-run the inlet continuity pattern, then Checkpoint #1 | [10.5](10-wiring.md#step-105-verify-the-pre-wired-inlet-before-you-trust-it), [10.23](10-wiring.md#step-1023-first-power-on-then-off-again) |
| PSU destroyed on first switch-on | 115/230 V selector set for the wrong mains | there is no fix after the fact — the selector is checked twice for this reason | [10.2](10-wiring.md#step-102-set-the-psu-input-voltage-selector), [10.22](10-wiring.md#step-1022-re-check-the-voltage-selector) |
| A 24 V node beeps continuously against its ground | reversed ferrule or a stray strand | find it before power-on; every node must read finite and rising, never 0 Ω | [10.74](10-wiring.md#step-1074-24-v-rails), [10.29](10-wiring.md#step-1029-meter-the-24-v-rail-for-shorts) |
| A PE row fails the bonding sweep | missing PE lead, or anodising under a washer | scrape the anodising; re-land the lead | [10.77](10-wiring.md#step-1077-protective-earth-bonding), [10.16](10-wiring.md#step-1016-frame-pe) |
| SSR reads short LOAD 1 → LOAD 2 with nothing energised | the relay is dead; the bed would be permanently live | replace it — do not power the machine | [10.21](10-wiring.md#step-1021-the-ssr-is-open-when-unpowered), [10.78](10-wiring.md#step-1078-ssr-polarity-and-isolation-one-last-time) |
| Controller or attached components destroyed after power-on | a Leviathan voltage-selection jumper left in, or set to 5 V | exactly two jumpers, Fan2 and Fan3, both at 24 V; Probe/Fan0/Fan1 bare | [09.19](09-electronics-bay.md#step-0919-strip-every-voltage-selection-jumper-off-the-leviathan), [10.28](10-wiring.md#step-1028-set-the-fan2-and-fan3-jumpers-to-24-v) |
| A fan never starts | wrong port, wrong voltage jumper, or the keyed 2×5 toolhead header seated backwards | check the port against the config; the header is keyed — if it will not drop in, it is backwards | [10.56](10-wiring.md#step-1056-the-fan-adapter-header-is-keyed-and-reversed), [13.11](13-initial-startup.md#step-1311-bay-fan-and-filter-fan) |
| Only one MCU enumerates, or none | firmware, serial path, or a USB cable | read both serial IDs and confirm which is which | [12.11](12-software.md#step-1211-gate-power-the-bay-and-confirm-both-mcus-enumerate), [12.20](12-software.md#step-1220-re-read-and-record-both-serial-paths) |
| The toolboard enumerates as `rp2040` | you have a Nitehawk-SB **V1**, not a V2 — or the wrong firmware | Rev D+ must read `stm32g0b1xx`; the Rev D guide's `rp2040` line is wrong for this kit | [00.5](00-before-you-start.md#step-005-verify-you-actually-received-a-rev-d-nitehawk-sb-v2), [12.12](12-software.md#step-1212-read-the-two-serial-ids-and-work-out-which-is-which) |
| A connector destroyed itself going in | a PH2.0 housing forced into the wrong V2 header, or the fan adapter pressed in backwards | if it needs force, it is wrong — read the silkscreen every time | [10.55](10-wiring.md#step-1055-connector-types-on-the-v2-toolboard), [Ch 08 Common mistakes](08-toolhead.md#common-mistakes) |
| A driver dies after a connector change | a stepper or the Micro-Fit umbilical moved with the power on | power down for every connector change — back-EMF kills drivers | [Ch 10 Read first](10-wiring.md), [Ch 13 Common mistakes](13-initial-startup.md#common-mistakes) |
| Umbilical or chain cable fails weeks after the build | cables pulled tight in the drag chains | loose in the chain, zip-tied at both ends of every chain | [10.65](10-wiring.md#step-1065-lay-the-harness-into-the-chains), [10.66](10-wiring.md#step-1066-zip-tie-both-ends-of-every-chain) |
| The ESD ground path is missing or broken | the V1 USB-adapter cover was fitted, hiding the grounding point | fit `usb_adapter_mount_partial_cover` and the supplied grounding cable | [10.57](10-wiring.md#step-1057-the-usb-adapter-cover-is-the-partial-cover), [10.58](10-wiring.md#step-1058-fit-the-esd-grounding-path) |
| A short across the 24 V fan rail takes the controller with it | the Nevermore bridge PCB was not metered before power | meter the bridge PCB; the splicer must sit on its printed spacer | [11.33](11-skirts-panels-door.md#step-1133-solder-the-fans-to-the-bridge-pcb), [Ch 11 Common mistakes](11-skirts-panels-door.md#common-mistakes) |

Source: [Ch 10 Checkpoint 10](10-wiring.md#checkpoint-10) and [Common mistakes](10-wiring.md#common-mistakes) · [Ch 09 Common mistakes](09-electronics-bay.md#common-mistakes) · [Ch 12 Common mistakes](12-software.md#common-mistakes) · [Ch 11 Common mistakes](11-skirts-panels-door.md#common-mistakes)

---

## Print quality

| Symptom | Likely cause | Fix | Owned by |
|---|---|---|---|
| First layer right at the front, wrong at the back | meshed before QGL, or the mesh was taken cold | `G28` → `QUAD_GANTRY_LEVEL` → `G28` → `BED_MESH_CALIBRATE`, hot | [13.39](13-initial-startup.md#step-1339-bed_mesh_calibrate), [Ch 13 Common mistakes](13-initial-startup.md#common-mistakes) |
| First layer featureless and glassy, or gappy and ridged | squish set wrong, or extrusion multiplier moved since it was set | re-run the live-Z procedure and commit with `Z_OFFSET_APPLY_ENDSTOP` | [13.42](13-initial-startup.md#step-1342-print-it-and-set-the-first-layer-squish), [14.21](14-calibration.md#step-1421-re-check-first-layer-squish-because-em-moved) |
| The Z offset reverts after every restart | babystepping was never committed | `Z_OFFSET_APPLY_ENDSTOP` then `SAVE_CONFIG` | [Ch 13 Common mistakes](13-initial-startup.md#common-mistakes) |
| Every first layer slightly under-squished | the extra `TESTZ Z=-0.1` was skipped when calibrating Z=0 hot | redo `Z_ENDSTOP_CALIBRATE` with the correction | [13.36](13-initial-startup.md#step-1336-z_endstop_calibrate-and-the-paper-test) |
| Cube is 0.1–0.3 mm oversize in X and Y | ASA shrinkage and bulging, not an axis error | fix with extrusion multiplier — never with negative XY size compensation | [14.11](14-calibration.md#step-1411-caliper-the-cube-against-the-prusa-printed-one), [14.19](14-calibration.md#step-1419-extrusion-multiplier-flow-the-2-pass) |
| Cube's first layer is wider than its mid-height | elephant-foot compensation wrong | adjust in 0.05 mm steps | [14.11](14-calibration.md#step-1411-caliper-the-cube-against-the-prusa-printed-one) |
| A persistent X − Y size difference on the same cube | gantry-square problem | Ch 06b | [14.11](14-calibration.md#step-1411-caliper-the-cube-against-the-prusa-printed-one), [Ch 06b](06-z-axis-and-gantry-squaring.md#step-06b14-de-rack-the-gantry-then-tighten-the-xy-joints) |
| Cube corner delaminates along a layer line | chamber too cold, or part fan too high | set the chamber target and soak | [14.8](14-calibration.md#step-148-set-the-chamber-target-and-understand-the-soak), [14.11](14-calibration.md#step-1411-caliper-the-cube-against-the-prusa-printed-one) |
| Top surfaces have gaps and valleys, or pellets and ridging | extrusion multiplier low / high | run the 2 % pass, then the 0.5 % refinement | [14.19](14-calibration.md#step-1419-extrusion-multiplier-flow-the-2-pass), [14.20](14-calibration.md#step-1420-the-05-refinement-pass) |
| Ringing / ghosting after corners, even with input shaping saved | `max_accel` left at the stock `10000` — `SAVE_CONFIG` does not touch it | set `max_accel` at or below the lower per-axis suggestion, with margin | [14.15](14-calibration.md#step-1415-save-the-shaper-and-set-the-real-max_accel) |
| Fine vertical ripple 0.5–2 mm apart on flat faces (VFA) | belt-tooth engagement ripple — cosmetic, not ringing | not a tuning fault; input shaping does not fix it | [print/00-slicer-setup.md](print/00-slicer-setup.md#gen-2-belt-upgrade-pause-rule) |
| Mesh and Z offset are wrong for every print | probed on a cold frame — the bed reaches temperature in minutes, the frame takes 30–45 | heat soak before probing | [13.31](13-initial-startup.md#step-1331-heat-soak-bed-100-c-hotend-150-c), [Ch 14 Common mistakes](14-calibration.md#common-mistakes) |
| Shaper graph shows two or more widely separated peaks | usually mechanical — a loose backer, an under-tensioned belt, a rail bolt in an end hole | fix the machine before shaping over it; below 25 Hz on either axis is a build fault | [14.14](14-calibration.md#step-1414-read-the-graphs) |

Source: [Ch 14 Parts D–F](14-calibration.md#part-d-chamber-and-the-first-real-print) and [Common mistakes](14-calibration.md#common-mistakes) · [Ch 13 Common mistakes](13-initial-startup.md#common-mistakes) · [print/00-slicer-setup.md](print/00-slicer-setup.md)

---

## Mechanical — noise, binding, play

| Symptom | Likely cause | Fix | Owned by |
|---|---|---|---|
| A tight spot near one end of X travel | a rail is not centred on its extrusion | re-centre and re-tighten from the middle outward | [05.44](05-gantry.md#step-0544-run-the-x-axis-end-to-end), [05.33](05-gantry.md#step-0533-centre-and-fit-the-mgn12-rail) |
| Stiffness that grows steadily toward one end | the gantry is racked | square it in Ch 06b. Do **not** loosen rails to make it feel better | [05.44](05-gantry.md#step-0544-run-the-x-axis-end-to-end), [06b.14](06-z-axis-and-gantry-squaring.md#step-06b14-de-rack-the-gantry-then-tighten-the-xy-joints) |
| A Z carriage has a tight spot the whole length | rail screws tightened from one end, bowing the rail | back them off and re-tighten centre-outward | [02.07](02-z-drives.md#step-0207-tighten-from-the-centre-outward), [Ch 02 Common mistakes](02-z-drives.md#common-mistakes) |
| A carriage is notchy or gritty and gets worse | the rail was installed dry, or grease was left on the rail surface | flip-and-pack needs the *back* of the rail — it comes off, or it wears out | [00.19](00-before-you-start.md#step-0019-flip-and-pack), [Ch 00 Common mistakes](00-before-you-start.md#common-mistakes) |
| Grease has gone milky and lost film strength | packed before the IPA fully evaporated | strip, dry properly, re-pack | [00.18](00-before-you-start.md#step-0018-degrease-ipa-soak-then-dry-completely), [Ch 00 Common mistakes](00-before-you-start.md#common-mistakes) |
| Belt noise that tension changes do not fix | crushed idler pockets from over-tightened 20T idler bolts | those bolts only locate the idler — they thread into plastic | [Ch 05 Common mistakes](05-gantry.md#common-mistakes) |
| A belt runs clean at one end of travel and rubs at the other | a half-twist somewhere in a long run | sight down each straight run; teeth must face the same way at both ends | [07.29](07-ab-belts.md#step-0729-belt-rub-inspection-at-every-idler-stack), [Ch 07 Common mistakes](07-ab-belts.md#common-mistakes) |
| A belt shreds against a flange | a bearing pair fitted flange-to-flange or flange-in | open the stack; the plain faces must meet | [04.07](04-ab-drives.md#step-047-a-idler-build-the-bearing-stack), [Ch 04 Common mistakes](04-ab-drives.md#common-mistakes) |
| The A and B belts rub against each other | pulleys at the same height, or the B pulley fitted hub-down | A = 16.5 mm hub down, B = 6.5 mm hub up, re-checked with the jig | [04.24](04-ab-drives.md#step-0424-a-drive-set-the-pulley-on-the-a-motor-at-165-mm), [04.33](04-ab-drives.md#step-0433-b-drive-set-the-pulley-on-the-b-motor-at-65-mm-flipped) |
| A and B tension will not converge | unequal belt lengths, unequal tail protrusion, or a belt rubbing | cut both together; equalise the tails; inspect every idler | [07.33](07-ab-belts.md#step-0733-move-the-gantry-return-and-re-check), [07.08](07-ab-belts.md#step-078-cut-both-belts-to-the-same-length) |
| Belt frequency reads far too high and will not come down | you are reading a harmonic, not the fundamental | take the **lowest** peak, three plucks, in a quiet room, over a measured 150 mm span | [07.31](07-ab-belts.md#step-0731-read-both-belts-with-the-phone), [07.30](07-ab-belts.md#step-0730-set-the-150-mm-measuring-span) |
| The plate tacos on the first heat to 110 °C | all four bed bolts were tightened; the plate must float on three | one bolt only — the plate is meant to expand | [03.17](03-build-plate.md#step-0317-tighten-one-bolt-only), [Ch 03 Common mistakes](03-build-plate.md#common-mistakes) |
| A bed bolt strips its T-nut on first tighten | the manual's M3×16 barely engages through a 10 mm plate plus spacer | use the M3×20 | [Ch 03 Common mistakes](03-build-plate.md#common-mistakes) |
| A drive-frame post strips and the frame will not hold | M5×30 BHCS torqued into plastic | stop at closed-and-snug; a stripped post means a reprint | [Ch 04 Common mistakes](04-ab-drives.md#common-mistakes) |
| A skirt or COB mount is bowed and will not sit flat | warped print, caught after assembly instead of at the flat-reference check | check parts against the flat reference as they come off the plate | [print/B07](print/B07-electronics-bay-and-lighting.md), [print/B08](print/B08-skirts-and-front-modules.md) |
| A side panel is scored by the gantry | 1 mm foam tape used on the sides instead of 3 mm | 1 mm on back and top, 3 mm on the sides — the 3 mm is a standoff | [11.56](11-skirts-panels-door.md#step-1156-foam-tape-the-side-panels), [Ch 11 Common mistakes](11-skirts-panels-door.md#common-mistakes) |
| The Clicky-Clack door racks, or the latch will not catch | loose M5×45 dowel fit, or the door is hung wrong at the hinges | re-hang at the hinges — the latch is almost never the problem | [11.62](11-skirts-panels-door.md#step-1162-hang-the-door-hinges), [Ch 11 Common mistakes](11-skirts-panels-door.md#common-mistakes) |

Source: [Ch 05 Step 05.44](05-gantry.md#step-0544-run-the-x-axis-end-to-end) · [Ch 00](00-before-you-start.md#common-mistakes), [Ch 02](02-z-drives.md#common-mistakes), [Ch 03](03-build-plate.md#common-mistakes), [Ch 04](04-ab-drives.md#common-mistakes), [Ch 05](05-gantry.md#common-mistakes), [Ch 07](07-ab-belts.md#common-mistakes), [Ch 11](11-skirts-panels-door.md#common-mistakes) Common mistakes

---

## Software and config

| Symptom | Likely cause | Fix | Owned by |
|---|---|---|---|
| Every `nhk:` pin behaves wrongly at once | `leviathan-printer-rev-d.cfg` loaded instead of the `-sbv2` file | grep for `nhk:PB8` before uploading; Rev D+ needs the `-sbv2` config | [12.21](12-software.md#step-1221-download-the-correct-config-file), [Ch 12 Common mistakes](12-software.md#common-mistakes) |
| `mcu 'nhk': Unable to open serial port` | serial path not pasted, or the board is not flashed | re-read both paths and paste them | [12.23](12-software.md#step-1223-paste-the-two-serial-paths), [13.4](13-initial-startup.md#step-134-connect-klipper-and-confirm-both-mcus) |
| Katapult is gone and the board will not flash | bootloader offset omitted in `make menuconfig` | recover over DFU with the board buttons, then re-flash with the right offset | [12.16](12-software.md#step-1216-recovery-only-reinstall-katapult-on-the-leviathan-over-dfu), [Ch 12 Common mistakes](12-software.md#common-mistakes) |
| `menuconfig` settings do not match the board | following the V1.3 Leviathan guide on a V1.2 board (or the reverse) | read the silkscreen and the serial ID *before* menuconfig | [12.13](12-software.md#step-1213-identify-your-leviathan-revision-before-you-build-anything), [Ch 12 Common mistakes](12-software.md#common-mistakes) |
| Both boards flashed twice, for no reason | MCU firmware built before the Update Manager ran | update the host first, then flash | [Ch 12 Common mistakes](12-software.md#common-mistakes) |
| `Unknown command:"BED_MESH_CLEAR"` at the end of a print | no `[bed_mesh]` section | add it — a warning, not a failure, but you have no mesh | [12.34](12-software.md#step-1234-add-a-bed_mesh-section), [13.38](13-initial-startup.md#step-1338-confirm-the-bed_mesh-section-from-ch-12) |
| The whole mesh is offset by a constant | `[bed_mesh]` added without `zero_reference_position` | the Omron's `z_offset` is 0 by design; pin the reference to bed centre | [12.34](12-software.md#step-1234-add-a-bed_mesh-section), [Ch 12 Common mistakes](12-software.md#common-mistakes) |
| The nozzle drives into the plate on `G28` | `home_xy_position` filled in with a guess | `-10,-10` failing is the interlock working — measure the real coordinate | [12.33](12-software.md#step-1233-z-endstop-leave-safe_z_home-deliberately-unreachable), [13.26](13-initial-startup.md#step-1326-record-the-z-endstop-coordinate-into-safe_z_home) |
| Interface reports X/Y travel of 250, not 350 | the 350 mm config edits are not live | check the running instance, not the file on disk | [13.5](13-initial-startup.md#step-135-prove-the-350-mm-config-edits-are-live) |
| The chamber thermistor reads nothing | plugged into a Leviathan `TH` port | Rev D+ reads it as `nhk:PB2` — it belongs on the toolboard's `CT` port | [10.39](10-wiring.md#step-1039-chamber-thermistor-if-your-batch-includes-one), [Ch 10 Common mistakes](10-wiring.md#common-mistakes) |
| The probe reads nothing on the Leviathan `Z-PROBE` header | on a Nitehawk build the probe lives on the toolboard's `PROBE` port | the stock config's comment says otherwise and the comment is wrong | [Ch 10 Common mistakes](10-wiring.md#common-mistakes), [12.29](12-software.md#step-1229-probe-omron-active-klicky-written-but-commented) |
| The filter fan cannot be commanded from a macro or the slicer | LDO's stock config declares FAN3 as a `[heater_fan]` slaved to the bed | this manual replaces it with `fan_generic` | [12.32](12-software.md#step-1232-fans-and-lighting-nevermore-cob-strips-bay-fans), [11.41](11-skirts-panels-door.md#step-1141-note-the-filter-fan-config-for-ch-12) |
| Homing is lost after every `SAVE_CONFIG` | `SAVE_CONFIG` restarts Klipper | re-`G32` after each one | [Ch 14 Read first](14-calibration.md) |

Source: [Ch 12 Common mistakes](12-software.md#common-mistakes) and [Checkpoint 12](12-software.md#checkpoint-12) · [Ch 13 Step 13.4](13-initial-startup.md#step-134-connect-klipper-and-confirm-both-mcus) · [Ch 10 Common mistakes](10-wiring.md#common-mistakes)

---

## Order-of-operations traps

These have no symptom until they are expensive. They are in the chapters' *Common mistakes* lists because you cannot debug your way out of them — you can only avoid them.

| Trap | What it costs | Owned by |
|---|---|---|
| Fitting a rail before greasing it | the rail comes off again, or runs dry for the life of the machine | [00.19](00-before-you-start.md#step-0019-flip-and-pack), [02.05](02-z-drives.md#step-0205-confirm-the-four-z-rails-are-already-cleaned-and-greased) |
| Missing a heat-set insert before a part is closed | six M3×40 out and the shaft assembly lifted (Z drive); a gantry teardown (XY joint) | [00.16](00-before-you-start.md#step-0016-plan-the-153-inserts), [02.03](02-z-drives.md#step-0203-seat-the-heat-set-inserts-in-the-z-drive-parts), [08.03](08-toolhead.md#step-083-inserts-clockwork-2-main-body) |
| Fitting the titanium backers after the gantry is built | ~3 h teardown — their T-nut slots are capped by the drive and idler frames | [05.16](05-gantry.md#step-0516-unpack-and-identify-the-titanium-backers), [Ch 05 Common mistakes](05-gantry.md#common-mistakes) |
| Using a rail's end hole | the rail comes off and goes back on — the end holes are where the p.89–90 / p.102 T-nuts live | [00.22](00-before-you-start.md#step-0022-understand-the-rail-jigs-before-you-need-them), [05.33](05-gantry.md#step-0533-centre-and-fit-the-mgn12-rail) |
| Skipping the reserved T-nuts at p.90 | Ch 06's Z joints and Ch 10's chain hardware have nowhere to bolt to | [05.13](05-gantry.md#step-0513-second-y-axis-then-load-the-end-m5-t-nuts), [Ch 05 Common mistakes](05-gantry.md#common-mistakes) |
| Skipping the deck supports until Ch 11 | the frame has to come partly apart — the deck cannot be lifted once the gantry and electronics are in | [02.13](02-z-drives.md#step-0213-fit-the-deck-support-clips), [Ch 02 Common mistakes](02-z-drives.md#common-mistakes) |
| Resolving the deck thickness from the documents | LDO's guide says 4 mm and LDO's BOM says 3 mm — only the caliper settles it, and B01 needs the answer | [00.4](00-before-you-start.md#step-004-inventory-carton-2-and-caliper-the-deck-panel), [02.12](02-z-drives.md#step-0212-caliper-the-deck-panel-and-choose-the-support-thickness) |
| Torquing the frame corner by corner as you go | whatever error was there is locked in; the mallet cannot fix it afterwards | [01.12](01-frame.md#step-0112-square-the-bottom-square-and-lock-it), [Ch 01 Common mistakes](01-frame.md#common-mistakes) |
| Treating Ch 07's belt tension as final | Ch 06b releases A/B tension completely as its first move | [07.33](07-ab-belts.md#step-0733-move-the-gantry-return-and-re-check), [06b.6](06-z-axis-and-gantry-squaring.md#step-06b6-release-the-ab-belt-tension-completely) |
| Setting Z offset or bed mesh before squaring the gantry | everything measured before Ch 06b is scrap | [13.34](13-initial-startup.md#step-1334-hand-off-to-ch-06b-square-the-gantry-then-re-tension-ab), [Ch 13 Common mistakes](13-initial-startup.md#common-mistakes) |
| Closing the bay or fitting panels before Checkpoint #1 | an unverified mains bay behind a bottom panel, and an hour to undo | [10.71](10-wiring.md#step-1071-leave-the-duct-covers-off), [Ch 11 Common mistakes](11-skirts-panels-door.md#common-mistakes) |
| Running `SHAPER_CALIBRATE` before the first good print or final belt tension | the result is stale before you use it; the same applies to pressure advance | [14.13](14-calibration.md#step-1413-run-shaper_calibrate), [Ch 14 Common mistakes](14-calibration.md#common-mistakes) |
| Building Klicky because the parts are on the bench | the kit's config, wiring and cable are all for the inductive probe | [08.54](08-toolhead.md#step-0854-confirm-the-probe-decision-and-bag-the-klicky-set), [Ch 08 Common mistakes](08-toolhead.md#common-mistakes) |

Source: the `Common mistakes` sections of [Ch 00](00-before-you-start.md#common-mistakes), [01](01-frame.md#common-mistakes), [02](02-z-drives.md#common-mistakes), [04](04-ab-drives.md#common-mistakes), [05](05-gantry.md#common-mistakes), [07](07-ab-belts.md#common-mistakes), [08](08-toolhead.md#common-mistakes), [11](11-skirts-panels-door.md#common-mistakes), [13](13-initial-startup.md#common-mistakes), [14](14-calibration.md#common-mistakes)

---

## Not covered here — where to ask

If your symptom is not in the tables above, this manual does not have an answer for it and you should ask rather than improvise. The three lifelines were joined in [Step 00.31](00-before-you-start.md#step-0031-join-the-three-lifelines-now); this is what each one is for.

| Where | Use it for | Link |
|---|---|---|
| **Fabreeko Discord** | missing, wrong or damaged parts; anything vendor-specific; your batch sheet | [discord.gg/NV8Y6bcerP](https://discord.gg/NV8Y6bcerP) |
| **Voron Discord**, `#voron_2_questions` | general 2.4 build and tuning questions. The server also runs a general help channel — check its channel list; Step 00.31 names only `#voron_2_questions` | [discord.gg/voron](https://discord.gg/voron) |
| **`#ldo_motors`** (inside the Voron Discord) | anything Rev D / Rev D+ specific, and the channel LDO's Build Notes direct corrections to | [channel link](https://discord.com/channels/460117602945990666/710952853514223617) |
| **Klipper Discourse** | Klipper itself — config, firmware, macros, shutdowns | [community.klipper3d.org](https://community.klipper3d.org) |

**Put all five of these in the question**, or you will spend a day getting asked for them:

1. **Kit identity** — the serial from carton 1, formatted `V2-YYMMDD####`, and that it is an **LDO Voron 2.4 R2 Rev D+, 350 mm** with a **Nitehawk-SB V2** toolboard. Rev D+ is why half the published answers will not apply to you.
2. **Where you are** — the chapter and step number from this manual, plus the corresponding official manual page or LDO guide section from that step's `Source:` line. That turns "it binds" into a place on a drawing.
3. **The config file name you actually loaded** — `leviathan-printer-rev-d-sbv2.cfg`, not `leviathan-printer-rev-d.cfg`. Say which, because it is the single most common wrong assumption in a Rev D+ thread.
4. **`klippy.log`**, complete and unmodified. Klipper's own instruction: *"Do not modify the log file in any way; do not provide a snippet of the log. Only the full unmodified log file provides the necessary information."* It lives at `~/printer_data/logs/klippy.log`; zip it before attaching.
5. **A photo** of the assembly you are asking about — and for anything mechanical, one photo of the *working* side too.

Source: [Ch 00 Step 00.31](00-before-you-start.md#step-0031-join-the-three-lifelines-now) · [Ch 00 Step 00.2](00-before-you-start.md#step-002-find-the-kit-serial-and-open-your-batch-bom-page) · [Klipper — Contact](https://www.klipper3d.org/Contact.html) · [Ch 12 Step 12.21](12-software.md#step-1221-download-the-correct-config-file)

---

## Next

[**Ch 16 — Glossary**](16-glossary.md): every term this manual assumes you already know, with the chapter where each one first matters.
