# Diagram manifest

104 generated SVGs covering the things the official manual states in prose but never draws. Regenerate with `python3 scripts/draw_diagrams.py`; the geometry and every label live in the scripts, not here.

The **Insert at** column names the chapter file and the step whose image block carries the diagram. Diagrams 1 to 18 are drawn in the script itself; the step-column diagrams of Chapters 02 to 14 (numbered by chapter, 201 onwards) live in `scripts/step_diagrams/chNN.py`.

All 104 are 1200 px wide, legible at 800 px, and safe on a dark page — each carries its own light background rect and pins `color` on the `<svg>` root, so `currentColor` text stays dark whether the file is referenced with `<img>` or inlined. Style is uniform: 2 px strokes, orange for `[a]_` accent parts, blue for the frame and extrusions, grey for hardware, teal and violet for the A and B belts.

## Index

| # | Diagram | File | Insert at |
|---|---|---|---|
| 1 | The six A/B bearing stacks | [`01-ab-bearing-stacks.svg`](01-ab-bearing-stacks.svg) | `04-ab-drives.md` — Step 04.7 (+1 more) |
| 2 | A/B handedness and pulley height | [`02-ab-pulley-height-handedness.svg`](02-ab-pulley-height-handedness.svg) | `04-ab-drives.md` — Step 04.2 (+1 more) |
| 3 | CoreXY belt path — A belt and B belt | [`03-corexy-belt-path.svg`](03-corexy-belt-path.svg) | `07-ab-belts.md` — Step 07.3 (+2 more) |
| 4 | Z drive gear train and Z belt loop | [`04-z-drive-gear-train.svg`](04-z-drive-gear-train.svg) | `02-z-drives.md` — Step 02.19 (+2 more) |
| 5 | Mains path and the protective-earth chain | [`05-mains-and-pe-chain.svg`](05-mains-and-pe-chain.svg) | `00a-mains-safety.md` — Step 00a.6 (+1 more) |
| 6 | Harness map — every cable to its port | [`06-harness-map.svg`](06-harness-map.svg) | `10-wiring.md` — Step 10.40 (+2 more) |
| 7 | Leviathan voltage-selection jumper map | [`07-leviathan-jumper-map.svg`](07-leviathan-jumper-map.svg) | `09-electronics-bay.md` — Step 09.19 (+1 more) |
| 8 | Rev D+ vs Rev D — connector differences | [`08-rev-d-plus-connectors.svg`](08-rev-d-plus-connectors.svg) | `10-wiring.md` — Step 10.55 (+3 more) |
| 9 | Racking, and how to measure it | [`09-gantry-racking.svg`](09-gantry-racking.svg) | `06-z-axis-and-gantry-squaring.md` — Step 06b.11 (+1 more) |
| 10 | STEPPER_BUZZ motor-direction cheat sheet | [`10-stepper-buzz-directions.svg`](10-stepper-buzz-directions.svg) | `13-initial-startup.md` — Step 13.13 (+1 more) |
| 11 | Build timeline — print batches against assembly chapters | [`11-build-timeline.svg`](11-build-timeline.svg) | `00-index.md` — The timeline |
| 12 | Titanium backers — which is which | [`12-ti-backers.svg`](12-ti-backers.svg) | `05-gantry.md` — Step 05.16 |
| 13 | Square it by the diagonals | [`13-frame-diagonals.svg`](13-frame-diagonals.svg) | `01-frame.md` — Step 01.12 (+1 more) |
| 14 | Six faces to check | [`14-frame-six-faces.svg`](14-frame-six-faces.svg) | `01-frame.md` — Step 01.14 (+1 more) |
| 15 | The blind joint | [`15-blind-joint.svg`](15-blind-joint.svg) | `01-frame.md` — Step 01.5 (+1 more) |
| 16 | Access holes face out | [`16-corner-access-holes.svg`](16-corner-access-holes.svg) | `01-frame.md` — Step 01.7 (+1 more) |
| 17 | Tightening order | [`17-tightening-order.svg`](17-tightening-order.svg) | `01-frame.md` — Step 01.9 (+1 more) |
| 18 | Bed extrusions | [`18-bed-extrusions.svg`](18-bed-extrusions.svg) | `01-frame.md` — Step 01.19 |
| 201 | The Z drive shaft stack, in order | [`201-z-shaft-stack.svg`](201-z-shaft-stack.svg) | `02-z-drives.md` — Step 02.19 |
| 202 | The first Z rail: holes, key and face | [`202-z-rail-holes-faces.svg`](202-z-rail-holes-faces.svg) | `02-z-drives.md` — Step 02.06 |
| 208 | Which face each Z rail goes on | [`208-z-rail-faces.svg`](208-z-rail-faces.svg) | `02-z-drives.md` — Step 02.09 |
| 203 | The Z0 corner with the printer upside down | [`203-z0-corner-upside-down.svg`](203-z0-corner-upside-down.svg) | `02-z-drives.md` — Step 02.29 |
| 204 | The belt tensioner cam: hand and fit | [`204-belt-tensioner-cam.svg`](204-belt-tensioner-cam.svg) | `02-z-drives.md` — Step 02.33 |
| 209 | Closing the belt tensioner cam | [`209-belt-tensioner-close.svg`](209-belt-tensioner-close.svg) | `02-z-drives.md` — Step 02.34 |
| 205 | Fitting a deck clip: thin edge in, then turn it | [`205-deck-clip-twist.svg`](205-deck-clip-twist.svg) | `02-z-drives.md` — Step 02.14 |
| 206 | Setting the 16T pulley with pulley_jig | [`206-16t-pulley-jig.svg`](206-16t-pulley-jig.svg) | `02-z-drives.md` — Step 02.27 |
| 207 | Insert map: retainer and main body | [`207-z-drive-insert-map.svg`](207-z-drive-insert-map.svg) | `02-z-drives.md` — Step 02.04 |
| 301 | Lay the magnet with a hinge | [`301-magnet-hinge.svg`](301-magnet-hinge.svg) | `03-build-plate.md` — Step 03.9 |
| 302 | Cut the magnet clear of each hole | [`302-trim-counterbore.svg`](302-trim-counterbore.svg) | `03-build-plate.md` — Step 03.10 |
| 303 | What each screw goes through | [`303-plate-stack.svg`](303-plate-stack.svg) | `03-build-plate.md` — Step 03.13 (+1 more) |
| 304 | Measure the gap at each screw | [`304-gap-caliper.svg`](304-gap-caliper.svg) | `03-build-plate.md` — Step 03.18 |
| 305 | Eight T-nuts, from above | [`305-tnut-plan.svg`](305-tnut-plan.svg) | `03-build-plate.md` — Step 03.12 |
| 306 | One screw tight, three loose | [`306-one-screw-tight.svg`](306-one-screw-tight.svg) | `03-build-plate.md` — Step 03.17 |
| 307 | Check the fuse, from below | [`307-fuse-check.svg`](307-fuse-check.svg) | `03-build-plate.md` — Step 03.5 |
| 401 | Near post, far post | [`401-near-far-post.svg`](401-near-far-post.svg) | `04-ab-drives.md` — Step 04.21 (+1 more) |
| 402 | Pulley height with the jig | [`402-pulley-jig.svg`](402-pulley-jig.svg) | `04-ab-drives.md` — Step 04.24 (+1 more) |
| 403 | Belt through the drive | [`403-belt-through-drive.svg`](403-belt-through-drive.svg) | `04-ab-drives.md` — Step 04.28 (+1 more) |
| 404 | Insert into the wide end | [`404-tensioner-insert.svg`](404-tensioner-insert.svg) | `04-ab-drives.md` — Step 04.4 |
| 405 | Screws in, then turn it over | [`405-flip-upper-frame.svg`](405-flip-upper-frame.svg) | `04-ab-drives.md` — Step 04.20 (+1 more) |
| 406 | First set screw on the flat | [`406-set-screw-flat.svg`](406-set-screw-flat.svg) | `04-ab-drives.md` — Step 04.25 |
| 501 | X extrusion: M5 T-nuts | [`501-x-extrusion-m5-tnuts.svg`](501-x-extrusion-m5-tnuts.svg) | `05-gantry.md` — Step 05.36 |
| 502 | Y extrusion end: four T-nuts | [`502-y-extrusion-end-tnuts.svg`](502-y-extrusion-end-tnuts.svg) | `05-gantry.md` — Step 05.14 |
| 503 | Upside down: left and right swap | [`503-gantry-flip.svg`](503-gantry-flip.svg) | `05-gantry.md` — Step 05.41 |
| 504 | Endstop pod: on top, screws down | [`504-endstop-pod-on-joint.svg`](504-endstop-pod-on-joint.svg) | `05-gantry.md` — Step 05.49 |
| 505 | XY joint bearing stack | [`505-xy-joint-bearing-stack.svg`](505-xy-joint-bearing-stack.svg) | `05-gantry.md` — Step 05.26 (+1 more) |
| 506 | Rail one side, backer opposite | [`506-rail-and-backer-faces.svg`](506-rail-and-backer-faces.svg) | `05-gantry.md` — Step 05.17 (+1 more) |
| 601 | A stopper as a shelf | [`601-rubber-stopper-shelf.svg`](601-rubber-stopper-shelf.svg) | `06-z-axis-and-gantry-squaring.md` — Step 06.10 |
| 602 | Fold the tail, tie it to itself | [`602-belt-tail-tie.svg`](602-belt-tail-tie.svg) | `06-z-axis-and-gantry-squaring.md` — Step 06.21 |
| 603 | Set it down on the joints | [`603-set-gantry-down.svg`](603-set-gantry-down.svg) | `06-z-axis-and-gantry-squaring.md` — Step 06.13 |
| 604 | The 150 mm span | [`604-z-belt-span.svg`](604-z-belt-span.svg) | `06-z-axis-and-gantry-squaring.md` — Step 06b.3 |
| 605 | Turn it over, mark the ends | [`605-turn-over-and-mark.svg`](605-turn-over-and-mark.svg) | `06-z-axis-and-gantry-squaring.md` — Step 06.11 |
| 701 | Fold, then cut both at once | [`701-belt-fold-cut.svg`](701-belt-fold-cut.svg) | `07-ab-belts.md` — Step 07.8 |
| 702 | Pluck the 150 mm span | [`702-belt-span-150.svg`](702-belt-span-150.svg) | `07-ab-belts.md` — Step 07.30 |
| 703 | Belt slots: A upper, B lower | [`703-belt-clamp-section.svg`](703-belt-clamp-section.svg) | `07-ab-belts.md` — Step 07.9 (+1 more) |
| 704 | Same length on both tails | [`704-belt-tails-equal.svg`](704-belt-tails-equal.svg) | `07-ab-belts.md` — Step 07.27 |
| 705 | Away, back, measure again | [`705-gantry-away-and-back.svg`](705-gantry-away-and-back.svg) | `07-ab-belts.md` — Step 07.33 |
| 706 | Out to the end, then 4 turns in | [`706-tensioner-four-turns.svg`](706-tensioner-four-turns.svg) | `07-ab-belts.md` — Step 07.5 |
| 707 | Quarter turns, A then B | [`707-quarter-turns.svg`](707-quarter-turns.svg) | `07-ab-belts.md` — Step 07.32 |
| 801 | Fan adapter on the 5015 | [`801-fan-adapter-on-5015.svg`](801-fan-adapter-on-5015.svg) | `08-toolhead.md` — Step 08.44 |
| 802 | Ground wire, motor end | [`802-ground-lug-motor-end.svg`](802-ground-lug-motor-end.svg) | `08-toolhead.md` — Step 08.53 |
| 803 | Cartridge up, leads in | [`803-cartridge-he0-th0.svg`](803-cartridge-he0-th0.svg) | `08-toolhead.md` — Step 08.61 |
| 804 | Cover, header, body | [`804-cover-and-header.svg`](804-cover-and-header.svg) | `08-toolhead.md` — Step 08.62 |
| 805 | Ends for HE0 and TH0 | [`805-revo-lead-ends.svg`](805-revo-lead-ends.svg) | `08-toolhead.md` — Step 08.33 |
| 806 | Toolhead LEDs from the front | [`806-toolhead-led-index.svg`](806-toolhead-led-index.svg) | `08-toolhead.md` — Step 08.37 |
| 901 | Where the PSU stops on the rear rail | [`901-psu-on-rear-rail.svg`](901-psu-on-rear-rail.svg) | `09-electronics-bay.md` — Step 09.16 |
| 902 | Check before the VHB goes down | [`902-vhb-checks.svg`](902-vhb-checks.svg) | `09-electronics-bay.md` — Step 09.36 |
| 903 | SSR the right way round | [`903-ssr-orientation.svg`](903-ssr-orientation.svg) | `09-electronics-bay.md` — Step 09.18 |
| 904 | Probe pin behind the plate | [`904-probe-pin-gap.svg`](904-probe-pin-gap.svg) | `09-electronics-bay.md` — Step 09.30 |
| 905 | Press the inlet in | [`905-inlet-press-in.svg`](905-inlet-press-in.svg) | `09-electronics-bay.md` — Step 09.11 |
| 906 | USB-adapter stack | [`906-usb-adapter-stack.svg`](906-usb-adapter-stack.svg) | `09-electronics-bay.md` — Step 09.25 |
| 1001 | Mains bus: one colour at a time | [`1001-mains-bus-probe-points.svg`](1001-mains-bus-probe-points.svg) | `10-wiring.md` — Step 10.18 |
| 1006 | Between colours: silent | [`1006-mains-isolation-pairs.svg`](1006-mains-isolation-pairs.svg) | `10-wiring.md` — Step 10.19 |
| 1002 | COB mount: inserts, then the lid | [`1002-cob-mount-inserts.svg`](1002-cob-mount-inserts.svg) | `10-wiring.md` — Step 10.35 |
| 1003 | 5 V check on the HAT adapter | [`1003-hat-adapter-5v-pads.svg`](1003-hat-adapter-5v-pads.svg) | `10-wiring.md` — Step 10.75 |
| 1004 | 24 V probe points | [`1004-24v-probe-points.svg`](1004-24v-probe-points.svg) | `10-wiring.md` — Step 10.73 (+1 more) |
| 1005 | Earth: one probe stays on C14 E | [`1005-earth-bonding-points.svg`](1005-earth-bonding-points.svg) | `10-wiring.md` — Step 10.77 |
| 1101 | Door hinges on the left front vertical, pins up | [`1101-door-hinges-pins-up.svg`](1101-door-hinges-pins-up.svg) | `11-skirts-panels-door.md` — Step 11.62 |
| 1102 | Handle and latch on the right side, lined up with a paper shim | [`1102-handle-latch-shim.svg`](1102-handle-latch-shim.svg) | `11-skirts-panels-door.md` — Step 11.64 |
| 1103 | 3 mm foam on the front face of the front opening, corners butted | [`1103-front-opening-foam.svg`](1103-front-opening-foam.svg) | `11-skirts-panels-door.md` — Step 11.51 |
| 1104 | Clicky-Clack door frame: the order | [`1104-door-frame-order.svg`](1104-door-frame-order.svg) | `11-skirts-panels-door.md` — Step 11.44 |
| 1105 | Nevermore plenum between the bed extrusions, T-nuts in the inside faces | [`1105-plenum-on-bed-extrusions.svg`](1105-plenum-on-bed-extrusions.svg) | `11-skirts-panels-door.md` — Step 11.38 |
| 1106 | Side spool frame on the right side | [`1106-side-spool-frame-and-holder.svg`](1106-side-spool-frame-and-holder.svg) | `11-skirts-panels-door.md` — Step 11.71 |
| 1107 | One PTFE from the CW2.5 to the side spool, seen from above | [`1107-side-spool-tube-route.svg`](1107-side-spool-tube-route.svg) | `11-skirts-panels-door.md` — Step 11.72 |
| 1201 | Power on: where to stand and look | [`1201-power-on-stance.svg`](1201-power-on-stance.svg) | `12-software.md` — Step 12.11 |
| 1202 | SW1 and SW2: reach from above | [`1202-leviathan-sw1-sw2.svg`](1202-leviathan-sw1-sw2.svg) | `12-software.md` — Step 12.15 |
| 1203 | Which Leviathan: read the chip | [`1203-leviathan-chip-marking.svg`](1203-leviathan-chip-marking.svg) | `12-software.md` — Step 12.13 |
| 1204 | Which line goes where | [`1204-serial-paths.svg`](1204-serial-paths.svg) | `12-software.md` — Step 12.23 |
| 1205 | Leviathan menuconfig | [`1205-leviathan-menuconfig.svg`](1205-leviathan-menuconfig.svg) | `12-software.md` — Step 12.14 |
| 1206 | Why -10,-10 cannot be reached | [`1206-safe-z-home.svg`](1206-safe-z-home.svg) | `12-software.md` — Step 12.33 |
| 1207 | DFU: both down, SW1 up first | [`1207-leviathan-dfu-press.svg`](1207-leviathan-dfu-press.svg) | `12-software.md` — Step 12.16 |
| 1301 | Hand under the gantry first | [`1301-hand-under-gantry-m84.svg`](1301-hand-under-gantry-m84.svg) | `13-initial-startup.md` — Step 13.17 |
| 1302 | Tape at 120 mm, then read R | [`1302-rotation-distance-tape.svg`](1302-rotation-distance-tape.svg) | `13-initial-startup.md` — Step 13.40 |
| 1303 | Shaft under the nozzle | [`1303-probe-under-nozzle.svg`](1303-probe-under-nozzle.svg) | `13-initial-startup.md` — Step 13.24 |
| 1304 | Paper test: step down to the first drag | [`1304-paper-test-testz.svg`](1304-paper-test-testz.svg) | `13-initial-startup.md` — Step 13.36 |
| 1305 | H at the rear edge, w in the hand | [`1305-scrubber-measurements.svg`](1305-scrubber-measurements.svg) | `13-initial-startup.md` — Step 13.45 |
| 1308 | d, G and O behind the plate | [`1308-omron-height-and-reach.svg`](1308-omron-height-and-reach.svg) | `13-initial-startup.md` — Step 13.46 |
| 1306 | Hand on the rocker, eyes on the bay | [`1306-power-on-hand-on-rocker.svg`](1306-power-on-hand-on-rocker.svg) | `13-initial-startup.md` — Step 13.3 |
| 1307 | First layer, cut across the lines | [`1307-first-layer-squish.svg`](1307-first-layer-squish.svg) | `13-initial-startup.md` — Step 13.42 |
| 1401 | A and B: 110 Hz each | [`1401-ab-belts-110hz.svg`](1401-ab-belts-110hz.svg) | `14-calibration.md` — Step 14.4 |
| 1402 | Lock the Z joints hot | [`1402-z-joints-hot.svg`](1402-z-joints-hot.svg) | `14-calibration.md` — Step 14.6 |
| 1403 | Tape at 120 mm, read R | [`1403-extruder-tape-r.svg`](1403-extruder-tape-r.svg) | `14-calibration.md` — Step 14.7 |
| 1404 | Measure at mid-height | [`1404-cube-mid-height.svg`](1404-cube-mid-height.svg) | `14-calibration.md` — Step 14.11 |
| 1405 | Prove it dead: 0 V | [`1405-psu-prove-dead.svg`](1405-psu-prove-dead.svg) | `14-calibration.md` — Step 14.30 |
| 1406 | Z belts: 140 Hz each | [`1406-z-belt-span-140hz.svg`](1406-z-belt-span-140hz.svg) | `14-calibration.md` — Step 14.5 |

---

## 1. The six A/B bearing stacks

`docs/manual/assets/diagrams/01-ab-bearing-stacks.svg`

**What it shows**

- All six F695 stacks as exploded vertical stacks in build order: A drive near post (2 bearings, 10 mm), A drive far post (4 bearings, 20 mm), B drive far post, B drive near post, A idler (front right), B idler (front left).
- Flange orientation item by item — spacer, flange down, flange up, spacer — and the two spacers that meet in the middle of every 4-bearing stack.
- Which bolt each stack builds on (M5x30 BHCS in the drives, M5x40 SHCS in the idlers) and the handed lower/upper frame heights.

**Insert at**

- `docs/manual/04-ab-drives.md` — **Step 04.7**: after the image line, as the reference for every stack in the chapter.
- `docs/manual/04-ab-drives.md` — **Step 04.22**: again at the four-bearing stack — the most often mis-stacked assembly in the build.

---

## 2. A/B handedness and pulley height

`docs/manual/assets/diagrams/02-ab-pulley-height-handedness.svg`

**What it shows**

- Top view fixing A = rear right and B = rear left, with the idler that belongs to each and the controller port each motor lands on.
- Both motor elevations side by side: A hub-down, teeth up, 16.5 mm; B hub-up, teeth low, 6.5 mm — both measured motor face to the underside of the teeth.
- Motor cable exits pointing inboard, and the 21.6/11.6 mm lower-idler-frame heights that make the 10.0 mm difference between the two belt planes.

**Insert at**

- `docs/manual/04-ab-drives.md` — **Step 04.2**: the handedness half — this is the step that fixes A/B before anything is assembled.
- `docs/manual/04-ab-drives.md` — **Step 04.24**: the pulley-height half, and again at Step 04.33.

---

## 3. CoreXY belt path — A belt and B belt

`docs/manual/assets/diagrams/03-corexy-belt-path.svg`

**What it shows**

- Both belt loops as separate top views, the way the manual splits p.126 and p.127: every 90° turn, the S-wrap at the drive, the 180° U-turn at the front idler, and the return to the carriage.
- The toothed face marked continuously along both belts, so the smooth back on every plain F695 stack, the teeth on the motor pulley, and the teeth-on wrap at each belt's one toothed XY joint (A: the right joint's upper 20T, B: the left joint's lower 20T) are visible at a glance.
- The direction each belt is threaded: both leave the LEFT carriage half heading left (p.131), so the two loops are mirror images traversed in opposite senses — A's first turn is the left joint's plain stack, B's first turn is the left joint's toothed idler.
- The two-runs-on-one-side asymmetry: A has two parallel runs on the right and one on the left; B is the mirror.
- Where the belt ends are clamped in the X carriage halves.

**Insert at**

- `docs/manual/07-ab-belts.md` — **Step 07.3**: the A panel, as the trace reference.
- `docs/manual/07-ab-belts.md` — **Step 07.4**: the B panel.
- `docs/manual/07-ab-belts.md` — **Step 07.23**: whole diagram again, as the pre-close check.

**Drawn schematically / left unlabelled (verify)**

- Which post does what is from the Voron CAD (A/B drive F695 stacks and the A/B belt meshes, 2026-10-30): a belt enters its own drive on the inboard near post (one F695 pair), wraps the pulley, and leaves round the outboard corner post (two pairs); the other belt's 90° turn is on that corner post. All side runs lie inboard of the Y extrusions, and on each side the other belt's single run is stacked on this belt's outer run. Lane spacing and the exact top-view coordinates inside a drive unit are schematic.
- The toothed face is stated by the chapter at four places — the carriage clamp (teeth toward the front, Step 07.9), the drive pulley (teeth seated on the pulley, Step 07.13), the front idler (smooth back on the stack, teeth outward on both runs, Step 07.15) and the toothed XY joint (teeth on its 20T idler — A's return turn at the right joint, Step 07.16; B's first turn at the left joint, Step 07.17). The face drawn at the remaining stations follows from belt geometry: a belt cannot change which face is which along its length. Which joint stack a belt meets (F695 pair or 20T idler) is fixed by the belt's height and needs no decision.
- The diagram does not say which X-carriage slot (upper or lower) each end goes into, because the chapter assigns the slots by belt plane rather than by side.
- Both X runs physically lie in front of the X extrusion (p.131); each panel draws one of them behind it so the two lanes read apart in a top view.

---

## 4. Z drive gear train and Z belt loop

`docs/manual/assets/diagrams/04-z-drive-gear-train.svg`

**What it shows**

- One corner in side elevation: the Z belt down the inside of the upright, around the Z drive's 20T pulley, up the outside, over the Z idler, back down to the Z joint where both ends clamp.
- Inside the drive: the motor's 16T at 10.7 mm, the 188 mm closed loop, the 80T on the 5 x 60 shaft, and the orange cam tensioner that pushes the motor away from the fixed drive body (the body is held by its two M5x40).
- The shaft stack in the order Step 02.19 gives it, with the 33 mm of shaft past the 20T pulley.

**Insert at**

- `docs/manual/02-z-drives.md` — **Step 02.19**: the shaft-stack panel.
- `docs/manual/02-z-drives.md` — **Step 02.21**: the gear-train panel, where the 188 mm loop becomes captive.
- `docs/manual/06-z-axis-and-gantry-squaring.md` — **Step 06.18**: the corner elevation, for the belt wrap direction.

---

## 5. Mains path and the protective-earth chain

`docs/manual/assets/diagrams/05-mains-and-pe-chain.svg`

**What it shows**

- The mains path end to end: wall socket, C13 cord, the combined C14 + rocker + fuse inlet, the three labelled WAGO 221-415 blocks, the Meanwell with its AC screws in datasheet order (1 L, 2 N, 3 FG), the Omron SSR, the bed heater.
- Which pole the fuse is in (Live only), which poles the rocker switches (both), and that the earth spade is neither switched nor fused.
- All four SSR terminals with what lands on each, including the red-to-3 / black-to-4 control pair from the Leviathan's HEATBED terminals.
- The five branches of the protective-earth chain, the bed's M4x6 BHCS + serrated washer, and the thermistor path from the pad to TH1.
- What the SSR's EARTH THE MOUNTING RAIL marking does and does not mean on this build, and what the inlet fuse does not protect.

**Insert at**

- `docs/manual/00a-mains-safety.md` — **Step 00a.6**: the whole diagram — this is the step that teaches the five branches.
- `docs/manual/10-wiring.md` — **Step 10.10**: the SSR panel, before the terminals are wired.

**Drawn schematically / left unlabelled (verify)**

- The inlet fuse rating is left unlabelled: LDO does not publish it, and Ch 00a already asks for it to be read off the part and written in the build log.

---

## 6. Harness map — every cable to its port

`docs/manual/assets/diagrams/06-harness-map.svg`

**What it shows**

- Every LDO harness cable, by the tag printed on it, against the Leviathan port it lands on: both HV-STEPPER ports, STEPPER-0..3 by corner, STEPPER-4 empty, TH1, the three endstop headers, FAN2/FAN3 by role, LED-Strip, the three 24 V feeds, HEATBED, and the data links.
- The ports that stay empty and why — STEPPER-4, TH0, Z-PROBE, FAN0, FAN1.
- The toolhead umbilical (Micro-Fit at the bay, XT30(2+2) at the toolboard) and every Nitehawk-SB V2 port with its connector type and pin.
- The three fan-adapter ports P2/P3/P4 by function.

**Insert at**

- `docs/manual/10-wiring.md` — **Step 10.40**: the Leviathan half, alongside the stepper tag table.
- `docs/manual/10-wiring.md` — **Step 10.54**: the toolhead half.
- `docs/manual/08-toolhead.md` — **Step 08.52**: the toolhead half again, at the account-for-unused-ports step.

---

## 7. Leviathan voltage-selection jumper map

`docs/manual/assets/diagrams/07-leviathan-jumper-map.svg`

**What it shows**

- All five voltage-selection headers by name, which two carry a jumper on this build (Fan2, Fan3, both at 24 V) and which three stay bare (Fan0, Fan1, the Z-probe header).
- The count check — 5 headers, 2 fitted, 3 bare — and why a jumper at 24 V with a 5 V device on the port destroys the device (nothing on the block can bridge 5 V to 24 V).
- The Ch 09 / Ch 10 sequence: strip every jumper on the bench, fit two back only after each device's voltage is verified.

**Insert at**

- `docs/manual/09-electronics-bay.md` — **Step 09.19**: as the picture of what 'all of them' means.
- `docs/manual/10-wiring.md` — **Step 10.28**: as the picture of the end state.

**Drawn schematically / left unlabelled (verify)**

- Header positions on the board outline are schematic, and so is the 5V / 24V pin order inside each header. The chapters name the five headers and say which two are fitted, but never give a physical location or a pin order — LDO's Leviathan V1.3 guide and the S1_mapping photo are the authority. Every header in the drawing is therefore labelled by name only.

---

## 8. Rev D+ vs Rev D — connector differences

`docs/manual/assets/diagrams/08-rev-d-plus-connectors.svg`

**What it shows**

- JST-PH2.0 and JST-XH2.5 drawn to the same scale so the 2.0 mm vs 2.5 mm pitch is visible, with the four ports that are PH2.0 and the one that is not.
- What the Rev D wiring guide says against what the V2 board actually is, port by port.
- The 2 x 5 keyed fan-adapter header with its key and the toolboard-side row order, and why a V1 2 x 4 adapter cannot be reused.
- The V2 partial cover with its deliberately exposed mounting point, and the full ESD ground chain from the extruder motor body to earth.

**Insert at**

- `docs/manual/10-wiring.md` — **Step 10.55**: the pitch panel, at the connector-type table.
- `docs/manual/10-wiring.md` — **Step 10.56**: the keyed-header panel.
- `docs/manual/10-wiring.md` — **Step 10.57**: the partial-cover panel, carrying into Step 10.58.
- `docs/manual/08-toolhead.md` — **Step 08.62**: the keyed-header panel again, where the board-to-board joint is actually mated.

**Drawn schematically / left unlabelled (verify)**

- Connector body proportions other than the pitch (housing height, latch shape) are generic — the chapters give the pitch, pin count and pinout, not a mechanical drawing.

---

## 9. Racking, and how to measure it

`docs/manual/assets/diagrams/09-gantry-racking.svg`

**What it shows**

- Three exaggerated top views: racked (X extrusion skewed between two parallel Y extrusions, the X-to-front-frame gap unequal left and right), yawed (the whole gantry turned in the frame, the four Y-to-upright gaps unequal front to rear) and square.
- The yaw tolerances of Step 06b.11 (same side within 0.5 mm, left vs right within 1 mm, machinist square at each front corner) and the racking check of Step 06b.14 (both X/Y joints touch their drives at once; X to front frame equal).
- Which fasteners come loose and in what order — lower Z joints, X/Y joints, A/B joints and front idlers — and the de-racking move itself.
- The one thing not to over-loosen: the A/B drive and front idler bolts, which also clamp the Z belts (the X/Y joints carry no Z belt clamp).

**Insert at**

- `docs/manual/06-z-axis-and-gantry-squaring.md` — **Step 06b.11**: the measurement half, beside the four-point table.
- `docs/manual/06-z-axis-and-gantry-squaring.md` — **Step 06b.14**: the de-racking half.

**Drawn schematically / left unlabelled (verify)**

- The racked and yawed views are deliberately exaggerated; real racking is a fraction of a millimetre. The skew shown is not a measurement.
- The two drives sit on one rigid E bridge, so racking cannot offset them: the racked view keeps both Y extrusions and drives square and skews only the X extrusion. The Z belt clamps are at the A/B drives and front idlers (p.111, p.117; CAD Z Belt Clamp Upper/Lower), not at the X/Y joints.

---

## 10. STEPPER_BUZZ motor-direction cheat sheet

`docs/manual/assets/diagrams/10-stepper-buzz-directions.svg`

**What it shows**

- A top view naming all four Z corners with the command that must move each one and the port it is on, and the arrow showing which corner rises first.
- That what rises is the gantry corner, not the bed.
- A and B on the rear extrusion with the config sections that drive them — [stepper_x] is motor B, [stepper_y] is motor A.
- Why A/B direction is not judged at the buzz, and the homing directions that do settle it (G28 X to the right, G28 Y to the back).
- The four failure modes and the fix for each.

**Insert at**

- `docs/manual/13-initial-startup.md` — **Step 13.13**: the whole sheet, replacing nothing — it is the picture of the step's table.
- `docs/manual/13-initial-startup.md` — **Step 13.14**: again, for the A/B panel.

---

## 11. Build timeline — print batches against assembly chapters

`docs/manual/assets/diagrams/11-build-timeline.svg`

**What it shows**

- Every row of 00-index.md's timeline in execution order on two lanes — print batches B00–B13 on the Core One+, assembly chapters (including Ch 00a, the two-part Ch 06/06b, Ch 11 A/B and Ch 12 1/2) on the bench — with each row's duration and KIT / 2P marker.
- One orange rail per print batch through the middle channel, forking to every chapter whose `needs:` list names that batch.
- Row 1's pre-B00 checks (belt pluck, hot first layer, on the current Gen 1 belts) as a full-width band before B00. The Gen 2 belt upgrade itself is deferred to the INDX rebuild this winter and no longer has a row.
- The critical-path strip: print hours (per batch and total) from docs/manual/print/README.md, the rest from 00-index.md § Critical path.

**Insert at**

- `docs/manual/00-index.md` — **The timeline**: at the head of the section, above the row list — this is the only diagram that belongs in the index rather than in a chapter step.

**Drawn schematically / left unlabelled (verify)**

- Nothing on this diagram is authored here. The rows, their order, their durations, their markers and their dependency arrows are parsed out of 00-index.md's timeline (via build_tonight.py's own row parser, so the picture and the Tonight planner always walk the same list); the hours come from print/README.md and the footer figures from 00-index.md § Critical path. Edit the index, then re-run this script.
- The vertical axis is execution order, not calendar time. The manual's timeline is dependency-ordered and gives no per-row calendar date, so none is invented here.

---

## 12. Titanium backers — which is which

`docs/manual/assets/diagrams/12-ti-backers.svg`

**What it shows**

- The three titanium backers of the 350 set to scale: the plain Y backer, the Y backer with four cable-chain pilot holes, and the X backer, with every screw hole.
- Where each goes: plain Y on the left Y extrusion's top face, the pilot Y backer on the right Y's top face with the pilot end at the rear, X on the X extrusion's rear face.
- A zoom on the pilot end: four pilots 20–32 mm from the end (Ø2.0 in the DXF), which LDO's set has drilled and tapped M3, where the Y chain's fixed end link sits.

**Insert at**

- `docs/manual/05-gantry.md` — **Step 05.16**: as the sorting picture.

**Drawn schematically / left unlabelled (verify)**

- Hole positions are the tanaes DXFs' (commit 5be0c5b). That Fabreeko's cut matches them, and whether its pilots arrive threaded, is unverified: count the holes on the bench.
- Right Y and rear come from the Voron CAD: the Y chain's fixed-end M3×6 FHCS goes into the right Y extrusion's top face about 54 mm from its rear end, which is where the pilots of a 390 mm backer centred on the 450 mm extrusion fall.

---

## 13. Square it by the diagonals

`docs/manual/assets/diagrams/13-frame-diagonals.svg`

**What it shows**

- Top view of one square of the frame, out of square (an exaggerated parallelogram) beside square: both diagonals measured outside corner to outside corner, the longer one red.
- The fix: tap the corner at one end of the longer diagonal inward along it. Square means both diagonals the same, about 721 mm on a 350.
- Callouts 1 and 2 are the Do numbers of Step 01.12 and of Step 01.13, whose Do 1 and 2 are the same measure and tap.

**Insert at**

- `docs/manual/01-frame.md` — **Step 01.12**: the bottom square.
- `docs/manual/01-frame.md` — **Step 01.13**: again for the top square, the same callouts.

**Drawn schematically / left unlabelled (verify)**

- The skew is exaggerated; 721 mm is the 510 × 510 plan diagonal (Step 01.12).

---

## 14. Six faces to check

`docs/manual/assets/diagrams/14-frame-six-faces.svg`

**What it shows**

- The frame as a wireframe turned 35° and seen from 20° above (off-isometric, so no diagonal lies on a hidden edge): the front face tinted with its two diagonals (about 735 mm, from 510 × 530 outside), the top face's diagonals dashed (about 721 mm), the three hidden edges dashed.
- The rule: six faces, and on each one the two diagonals must match.

**Insert at**

- `docs/manual/01-frame.md` — **Step 01.14**: the four upright faces.
- `docs/manual/01-frame.md` — **Step 01.20**: the final pass over all six.

**Drawn schematically / left unlabelled (verify)**

- Drawn as a plain box of edges; the extrusions' 20 mm section is not to scale.

---

## 15. The blind joint

`docs/manual/assets/diagrams/15-blind-joint.svg`

**What it shows**

- Three sections after p.10, looking down the vertical, titled rather than numbered because two steps with different Do numbers use them: the M5×16 BHCS started in the horizontal's end, head about 2 mm off the end face; the head slid into the vertical's slot; the 3 mm hex key straight through the access hole in the opposite face into the head.

**Insert at**

- `docs/manual/01-frame.md` — **Step 01.5**: the whole sheet.
- `docs/manual/01-frame.md` — **Step 01.4**: the top row, for the 2 mm.

**Drawn schematically / left unlabelled (verify)**

- The three stages are stacked top to bottom, not left to right, so the section stays large enough to label at 480 px.
- The 2020 slot (6.2 mm opening, 1.8 mm lip) and the 5 mm access hole are nominal; the access hole is drawn as one bore through the core.

---

## 16. Access holes face out

`docs/manual/assets/diagrams/16-corner-access-holes.svg`

**What it shows**

- Top view of one corner: the vertical's section, a horizontal on each of its two inner faces, the access holes on the two outer faces and a hex key into each from outside the frame.
- Callouts 1–3 are the Do numbers of Step 01.7. A small second panel shows the vertical turned the wrong way: holes under the horizontals, out of reach.

**Insert at**

- `docs/manual/01-frame.md` — **Step 01.7**: the first corner.
- `docs/manual/01-frame.md` — **Step 01.8**: the same rule at the other three.

**Drawn schematically / left unlabelled (verify)**

- The access holes sit in the side faces, so a top view cannot show them as holes: each is marked by a dot on its face.

---

## 17. Tightening order

`docs/manual/assets/diagrams/17-tightening-order.svg`

**What it shows**

- Top view of a square with its corners numbered 1–4 going round, and the order 1, 3, 2, 4: always across to the opposite corner. The red line says never tighten round the frame in order; fitting the corners in turn (Step 01.8) is not tightening.

**Insert at**

- `docs/manual/01-frame.md` — **Step 01.9**: the bottom square, snug pass.
- `docs/manual/01-frame.md` — **Step 01.12**: the torque pass; Steps 01.11 and 01.13 repeat the order without the picture.

---

## 18. Bed extrusions

`docs/manual/assets/diagrams/18-bed-extrusions.svg`

**What it shows**

- Top view after p.20, FRONT at the bottom: the bed extrusions front to back between the front and rear rails, the centreline 255 mm from the left rail's outer face, each extrusion's inner face 65 mm from it (130 mm clear), and the 90° to the rail. Callouts 1–3 are the Do numbers of Step 01.19; callout 3 sits on the bracket in the side view.
- Side view of the front end after p.18, p.19 and p.21: the bed extrusion's end flush with the rail's inner face and its underside level with the rail's top; the corner bracket's upright leg on the end (M5×16 into the end bore), its flat leg on the rail (M5×10 with the brass spacer under its head, into a T-nut in the rail's top slot).

**Insert at**

- `docs/manual/01-frame.md` — **Step 01.19**: only here: its callouts are this step's Do. Steps 01.16 and 01.18 show the p.18 and p.19 crops instead.

**Drawn schematically / left unlabelled (verify)**

- The bracket's shape, leg thickness and the spacer's thickness are schematic; the chapter gives no dimensions for them.
- Kept within 1200 × 1075 so it fills the iPad's picture column: top view at 0.8 px per mm.

---

## 201. The Z drive shaft stack, in order

`docs/manual/assets/diagrams/201-z-shaft-stack.svg`

**What it shows**

- Side view of one 5x60 shaft, short end left: a 625 against the 20T's collar, the 20T (collar, teeth, flange), two spacers, a 625, two spacers, the 80T with its hub toward the 20T, and the last 625 on the long end (p.33 side view; CAD Z0 shaft assembly). The 33 mm runs from the long end to the 20T's flange (p.32). Callouts 1 to 3 are the Do numbers of Step 02.19.

**Insert at**

- `docs/manual/02-z-drives.md` — **Step 02.19**: the stack in order, first image.

**Drawn schematically / left unlabelled (verify)**

- Part widths along the shaft are from the 250 CAD (625 5 mm, 80T 18 mm incl. hub, 20T 20 mm incl. collar, 1 mm spacers); diameters of the 80T hub and the 20T teeth are estimated from p.32-33. Line weights, fills and the gaps between parts are schematic; every position and number comes from the sources named in the module docstring.

---

## 202. The first Z rail: holes, key and face

`docs/manual/assets/diagrams/202-z-rail-holes-faces.svg`

**What it shows**

- Side view of one MGN9H 400 rail on its vertical: 20 holes numbered from the bottom, screws in 2, 4 ... 18, holes 1, 19 and 20 empty, the carriage taped at mid-rail, the rail standing on the 3 mm hex key above the bottom horizontal (p.25 gap; LDO p.88 end-hole note).
- Plan view from above, front at the bottom: the first rail at Z0 on the vertical's rear-facing side, the rear rails on the rear verticals' front-facing sides (CAD, Step 02.09 render; p.27). Callouts 1 to 3 are the Do numbers of Step 02.06.

**Insert at**

- `docs/manual/02-z-drives.md` — **Step 02.06**: holes, key and face, first image.

**Drawn schematically / left unlabelled (verify)**

- p.25 draws the 250's 15-hole rail with both end holes used; LDO's p.88 note leaves the end holes empty. A 20-hole rail then keeps two empty holes at one end; no source picks the end and it makes no difference, so this manual counts from the bottom. Rail length, widths and the 3 mm gap are drawn schematic (the gap is exaggerated).

---

## 208. Which face each Z rail goes on

`docs/manual/assets/diagrams/208-z-rail-faces.svg`

**What it shows**

- Plan from above, printer upright, front at the bottom: Z0's rail done, the other three to fit; the front rails on the front verticals' rear-facing sides and the rear rails on the rear verticals' front-facing sides, so the two on each side face each other (CAD, Step 02.09 render; p.27). Callouts 1 to 3 are the Do numbers of Step 02.09.

**Insert at**

- `docs/manual/02-z-drives.md` — **Step 02.09**: which face, first image.

**Drawn schematically / left unlabelled (verify)**

- Rail and corner sizes are schematic; only the faces are from the CAD.

---

## 203. The Z0 corner with the printer upside down

`docs/manual/assets/diagrams/203-z0-corner-upside-down.svg`

**What it shows**

- Plan from above with the printer upside down (rolled over sideways, as p.41's inset shows), standing at the FRONT tape: Z0 is on your right. The drive body's counterbored face faces outward over the side extrusion, its retainer face toward the motor; two M5x40 go into the side extrusion, the motor foot's two M5x10 into the front extrusion, 25 mm apart. Positions from the CAD Z0 corner. Callouts 1 and 2 are the Do numbers of Step 02.29.

**Insert at**

- `docs/manual/02-z-drives.md` — **Step 02.29**: the corner, first image.

**Drawn schematically / left unlabelled (verify)**

- Outlines are bounding boxes from the 250 CAD; the baseplate, foot and cam are left off so the faces and screws show. Line weights, fills and the gaps between parts are schematic; every position and number comes from the sources named in the module docstring.

---

## 204. The belt tensioner cam: hand and fit

`docs/manual/assets/diagrams/204-belt-tensioner-cam.svg`

**What it shows**

- Top: the cam flat face down with the lobe on the left (STL outline): the tab is far-right on _a and near-right on _b (the mirror). Bottom: from above, printer upside down, Z0 corner: the cam's lobe under the motor foot's drive end on its loose M5x10, tab sticking straight out (p.43). Callouts 1 to 3 are the Do numbers of Step 02.33.

**Insert at**

- `docs/manual/02-z-drives.md` — **Step 02.33**: hand and where the cam sits, first image.

**Drawn schematically / left unlabelled (verify)**

- The foot's outline and the surface the lobe bears on are schematic; the cam outline is the STL slice.

---

## 209. Closing the belt tensioner cam

`docs/manual/assets/diagrams/209-belt-tensioner-close.svg`

**What it shows**

- From above, printer upside down, Z0 corner: (1) the tab swinging toward the motor, (2) flat along the front extrusion in the notch, the lobe pushing the foot about 2.5 mm away from the drive body, which stays put (p.44; CAD closed position). Callouts 1 and 2 are the Do numbers of Step 02.34.

**Insert at**

- `docs/manual/02-z-drives.md` — **Step 02.34**: the swing, first image.

**Drawn schematically / left unlabelled (verify)**

- The 2.5 mm throw is the lobe's 12.5 mm reach (closed) less its 10 mm reach (open) toward the drive, from the STL; the surface it bears on and the foot's outline are schematic.

---

## 205. Fitting a deck clip: thin edge in, then turn it

`docs/manual/assets/diagrams/205-deck-clip-twist.svg`

**What it shows**

- Section along a bottom frame extrusion, printer upside down, deck panel below. (a) The clip goes in thin edge first, its 5.8 mm thickness through the slot mouth and its 20 mm length along the slot. (b) Turned 90°: the head sits behind the slot's lips and the short end of the body lies over the panel's edge (outline from deck_support_3mm; the short end stops about 0.8 mm off a 3 mm panel). Callout 2 is Do 2 of Step 02.14.

**Insert at**

- `docs/manual/02-z-drives.md` — **Step 02.14**: the twist-in, first image.

**Drawn schematically / left unlabelled (verify)**

- No manual page or CAD shows the clips; the fit is worked out from the STL (key, body and which end is the short one) and the CAD deck position (panel top flush with the extrusion's top). Spacing along the extrusion stays 'verify on bench'.

---

## 206. Setting the 16T pulley with pulley_jig

`docs/manual/assets/diagrams/206-16t-pulley-jig.svg`

**What it shows**

- Side view after p.38: pulley_jig stood on the motor face with its B tab hooked over the motor's edge and its Z tab toward the pulley; the underside of the 16T's teeth level with the Z tab's underside, 10.7 mm above the motor face; collar up. Jig outline from the STL. Callouts 1 to 3 are the Do numbers of Step 02.27.

**Insert at**

- `docs/manual/02-z-drives.md` — **Step 02.27**: the jig in use, first image.

**Drawn schematically / left unlabelled (verify)**

- The 16T's flange, tooth band and collar heights are estimated from p.38; only the 10.7 mm is a given number.

---

## 207. Insert map: retainer and main body

`docs/manual/assets/diagrams/207-z-drive-insert-map.svg`

**What it shows**

- Both flat faces as you look at them (STL slice), with the foot face unfolded below each: the retainer's six inserts in its flat face and one in its foot face; the main body's six counterbores left empty and its two inserts in its foot face. The three foot-face inserts take the baseplate's M3x8 (CAD).

**Insert at**

- `docs/manual/02-z-drives.md` — **Step 02.04**: where the inserts go, first image.

**Drawn schematically / left unlabelled (verify)**

- Drawn from the _a parts; the _b parts are their mirror image. Window and outline shapes are 0.3 mm simplifications of the STL.

---

## 301. Lay the magnet with a hinge

`docs/manual/assets/diagrams/301-magnet-hinge.svg`

**What it shows**

- Three side views, FRONT left, BACK right. (a) The pad, liner side down, flush at the plate's back edge if it is 355 mm, a strip of masking tape over that edge as the hinge (Do 1, 2). (b) The pad folded back over the hinge, its liner now facing the front, a 40 to 50 mm strip of liner cut off at the hinge end (Do 3). (c) The bare strip pressed down at the back, the rest of the pad held up, the liner pulled out to the front and the squeegee sweeping after it toward the front (Do 3).

**Insert at**

- `docs/manual/03-build-plate.md` — **Step 03.9**: the hinge method.

**Drawn schematically / left unlabelled (verify)**

- The pad's size is not known before kit day (Do 1 says verify on bench): the drawing shows it flush at the back, labelled 'if 355 mm', and carries a 'check on the bench' label.
- The fold-back geometry follows the step's own words; the linked lamination video was not watched. Thicknesses of the magnet, liner and tape, and the counterbore's size, are schematic.

---

## 302. Cut the magnet clear of each hole

`docs/manual/assets/diagrams/302-trim-counterbore.svg`

**What it shows**

- Left, from above: the magnet with the counterbore showing through as a dimple and a craft knife two thirds of the way round its edge (Do 1, 2). Right, cut through one hole: the magnet cut back to the counterbore's edge, the M3 head sitting flush with the plate face with no magnet over it, a hex key in its socket, and no burr at the rim (Do 3).

**Insert at**

- `docs/manual/03-build-plate.md` — **Step 03.10**: the cut and the flush head.

**Drawn schematically / left unlabelled (verify)**

- Head flush with the plate face follows p.53 ('flush/below the surface') and the 250 CAD (head top level with the plate top). The counterbore's diameter and depth on LDO's 10 mm plate are not published. Thicknesses of the magnet, liner and tape, and the counterbore's size, are schematic.

---

## 303. What each screw goes through

`docs/manual/assets/diagrams/303-plate-stack.svg`

**What it shows**

- Section across one bed extrusion at a plate screw, to scale from the CAD: magnet, the 10 mm plate with the M3×20 head flush in its counterbore, the M4 thumb nut standing knurled rim down and collar up (p.58), and the roll-in M3 T-nut in the extrusion's top slot, which is the only part the screw threads into. No callouts: it serves two steps with different Do lists.

**Insert at**

- `docs/manual/03-build-plate.md` — **Step 03.13**: the thumb nut's way up.
- `docs/manual/03-build-plate.md` — **Step 03.15**: the screw's path.

**Drawn schematically / left unlabelled (verify)**

- Thumb-nut shape and 8 mm height are the CAD's DIN 466-B; the kit's M4 knurled nut may differ in height (LDO says its spacers are thicker). The screw tip's depth in the T-nut follows from those numbers. Thicknesses of the magnet, liner and tape, and the counterbore's size, are schematic.

---

## 304. Measure the gap at each screw

`docs/manual/assets/diagrams/304-gap-caliper.svg`

**What it shows**

- Side view at a front screw, FRONT left: the caliper's inside jaws in the gap between the bed extrusion's top and the plate's underside, beam upright just in front of the plate's edge (Do 1), and the eye sighting along the plate (Do 2).

**Insert at**

- `docs/manual/03-build-plate.md` — **Step 03.18**: where the caliper goes.

**Drawn schematically / left unlabelled (verify)**

- The caliper is drawn schematically; the jaws sit beside the thumb nut, not through it. Hole 7 mm in from the plate edge is the 250 CAD's.

---

## 305. Eight T-nuts, from above

`docs/manual/assets/diagrams/305-tnut-plan.svg`

**What it shows**

- Top view, FRONT at the bottom: the two bed extrusions with four M3 T-nuts in their top slots under the plate's holes (the front pair 25 mm behind the front extrusion, p.58), and in the rear half of the inner side slots two M3 on the right extrusion and two M5 on the left. Callouts 1 to 3 are the Do numbers of Step 03.12.

**Insert at**

- `docs/manual/03-build-plate.md` — **Step 03.12**: where all eight go.

**Drawn schematically / left unlabelled (verify)**

- Scale is about 1.5 px per mm across and 1.4 front to back. The side-slot T-nuts slide into place in Ch 09: the M3 pair is drawn where the 250 CAD puts the probe's nuts, 87 to 105 mm from the rear extrusion, level with the plate's rear edge; the M5 pair is schematic. The rear holes 7 mm in from the plate's rear edge are the 250 CAD's; the step has the builder measure them.

---

## 306. One screw tight, three loose

`docs/manual/assets/diagrams/306-one-screw-tight.svg`

**What it shows**

- Top view, FRONT at the bottom: the plate on its two bed extrusions with the front-left screw tight and the other three loose, and arrows showing the plate growing away from the fixed screw as it heats. Callouts 1 to 3 are the Do numbers of Step 03.17.

**Insert at**

- `docs/manual/03-build-plate.md` — **Step 03.17**: which screw is tight.

---

## 307. Check the fuse, from below

`docs/manual/assets/diagrams/307-fuse-check.svg`

**What it shows**

- The plate's underside at the back edge, seen from below: the heater pad, the bare aluminium strip along the edge, the plate's three leads leaving in the middle (Do 1), the thermal fuse held flat by one screw and washer (Do 2), and its two legs running down to their heat-shrink joins (Do 3).

**Insert at**

- `docs/manual/03-build-plate.md` — **Step 03.5**: where the fuse sits.

**Drawn schematically / left unlabelled (verify)**

- Traced from LDO's Rev C 300 mm plate photo (build_plate_bottom_view.jpg), the only underside photo LDO publishes; the 350 plate's strip and fuse position are not published, so the drawing carries a check-on-the-bench note. Wire routing below the edge is schematic.

---

## 401. Near post, far post

`docs/manual/assets/diagrams/401-near-far-post.svg`

**What it shows**

- Both upper drive frames from above, flat face down as on the bench, traced from the STLs: the motor bore, the near post about 17 mm from its centre (2 bearings) and the far post about 34 mm away (4 bearings). The far post is on the right for A and on the left for B, as p.74 and p.78 draw them.

**Insert at**

- `docs/manual/04-ab-drives.md` — **Step 04.21**: both posts on A, before the near stack.
- `docs/manual/04-ab-drives.md` — **Step 04.30**: both posts on B, before the far stack.

**Drawn schematically / left unlabelled (verify)**

- Outline is the flat face's outline at 0.5 mm, simplified to 0.25 mm; the walls and pockets above it are left out.
- The stacks are drawn at the F695 flange size (15 mm) from above; the far stack's thicker ring only marks it, both look the same from above.

---

## 402. Pulley height with the jig

`docs/manual/assets/diagrams/402-pulley-jig.svg`

**What it shows**

- A and B motors from the side after p.75 and p.79: the jig standing on its long bottom edge on the motor face beside the pulley, letters upright, its A (or B) tab in the pulley's groove; the tab's underside level with the top of the lower flange (16.5 mm on A hub down, 6.5 mm on B hub up). Callouts 1-3 are the Do numbers of Steps 04.24 and 04.33.
- Two wrong ways, small: the jig on its two feet (every height 3 mm high), and the teeth lined up with the tab's top (about 23 mm on A, 13 mm on B).

**Insert at**

- `docs/manual/04-ab-drives.md` — **Step 04.24**: the A side and both wrong ways.
- `docs/manual/04-ab-drives.md` — **Step 04.33**: the B side.

**Drawn schematically / left unlabelled (verify)**

- The jig outline and tab heights are from pulley_jig.stl; the pulley (hub 16 mm, flanges 15.2 mm, teeth 11.65 mm across, 7 mm groove) is from the CAD and drawn schematically; the motor boss is the nominal NEMA 17 22 mm x 2 mm, not measured on the LDO motor.
- In the 'tab's top' panel the jig is drawn a little away from the pulley so the hub clears the tab.

---

## 403. Belt through the drive

`docs/manual/assets/diagrams/403-belt-through-drive.svg`

**What it shows**

- Each drive from above, right way up, seen standing behind the printer (so its posts mirror diagram 401's upside-down bench view), with the frame shown as a dashed outline so the stacks show: the belt end run over the near stack, teeth round the pulley's front and over the far stack, as the CAD routes the A and B belts. Below a rule, the same drive from behind as p.76 and p.80 draw it, labelled so: the belt's band level across the near pair, the pulley teeth and the far post's upper pair (A) or lower pair (B); the far post's other pair carries the other belt. Callouts 1 and 2 are the Do numbers of Steps 04.28 and 04.37.

**Insert at**

- `docs/manual/04-ab-drives.md` — **Step 04.28**: A on the upper level.
- `docs/manual/04-ab-drives.md` — **Step 04.37**: B on the lower level.

**Drawn schematically / left unlabelled (verify)**

- Frame plates in the side view are schematic slabs (the real frames have walls and pockets); stack, pulley and belt heights are the CAD's.
- The belt's centre line is drawn 7.2 mm from each stack's axis and 7 mm from the pulley's; the wrap angles follow the CAD, the strand lengths are approximate.

---

## 404. Insert into the wide end

`docs/manual/assets/diagrams/404-tensioner-insert.svg`

**What it shows**

- The tension arm cut in half along its one hole: 5 mm at 4.7 mm across at the top, 13 mm at 3.5 mm below it. The insert sits over the 4.7 mm end under the press tip; the 3.5 mm part stays clear for the M3x40. A small panel shows the insert offered to the narrow end, crossed out.

**Insert at**

- `docs/manual/04-ab-drives.md` — **Step 04.4**: the whole sheet.

**Drawn schematically / left unlabelled (verify)**

- The arm's material around the hole is drawn as a 14 mm block; the hole's lengths and diameters are the STL's. Insert 5 x 4 mm and the press tip are schematic.

---

## 405. Screws in, then turn it over

`docs/manual/assets/diagrams/405-flip-upper-frame.svg`

**What it shows**

- The upper drive frame from the side, twice: (1) flat face up, the two M5x30 BHCS dropping in from that face, 37 mm apart; (2) turned over with the heads held, the frame on the bench on the two heads and both threads standing up. Callouts 1 and 2 are the Do numbers of Steps 04.20 and 04.29.

**Insert at**

- `docs/manual/04-ab-drives.md` — **Step 04.20**: the A frame.
- `docs/manual/04-ab-drives.md` — **Step 04.29**: the B frame.

**Drawn schematically / left unlabelled (verify)**

- The frame is a schematic 64 mm slab with three walls; only the post spacing (37 mm), the 6 mm plate and the screw size are real. p.74 shows the upside-down frame resting with the heads under it.

---

## 406. First set screw on the flat

`docs/manual/assets/diagrams/406-set-screw-flat.svg`

**What it shows**

- The pulley hub cut across at its two set screws, 90 degrees apart: the first screw's tip on the flat side of the motor shaft, the second on the round. Callout 2 is the Do number of Step 04.25. A small panel shows the first screw tightened on the round part with the flat under the second, crossed out.

**Insert at**

- `docs/manual/04-ab-drives.md` — **Step 04.25**: which screw goes on the flat.

**Drawn schematically / left unlabelled (verify)**

- Whether the kit's A/B motor shafts have a flat is not known before kit day (the step says 'if it has one'); the flat's depth (0.5 mm) is schematic.
- Set screw angle (90 degrees) is from the CAD pulley; the kit pulley may differ (verify on bench).

---

## 501. X extrusion: M5 T-nuts

`docs/manual/assets/diagrams/501-x-extrusion-m5-tnuts.svg`

**What it shows**

- End view of the D extrusion: the MGN12 rail on the front face, the titanium backer on the rear face, an M5 T-nut in the top slot (callout 1) and one in the bottom slot (callout 2).
- Front view of the whole 430 mm extrusion: two M5 T-nuts in the top slot at each end, one in the bottom slot at each end under the outer top nut, and the 400 mm rail 15 mm short of each end. Callouts 1 and 2 are the Do numbers of Step 05.36.

**Insert at**

- `docs/manual/05-gantry.md` — **Step 05.36**: which slot takes which M5 T-nuts.

**Drawn schematically / left unlabelled (verify)**

- T-nut positions along the extrusion follow the 250-size CAD (2–15 mm and 17–30 mm from each end, the bottom single under the outer top nut); the joint's own holes set the real position.
- Backer thickness (drawn 2.5 mm) is schematic.

---

## 502. Y extrusion end: four T-nuts

`docs/manual/assets/diagrams/502-y-extrusion-end-tnuts.svg`

**What it shows**

- One end of a C extrusion the way it sits in the machine, rail underneath: two M5 T-nuts already in the top slot, and in the rail's slot, in the bare 25 mm beyond the rail end, one M5 outermost and one M3 just inside it (callouts 1 and 2 are the Do numbers of Step 05.14). A small end view names the top slot and the rail slot.

**Insert at**

- `docs/manual/05-gantry.md` — **Step 05.14**: the end as it sits in the machine, not rail-up as on p.90.

**Drawn schematically / left unlabelled (verify)**

- Nut lengths and positions follow the 250-size CAD (M5 2–15 mm, M3 17–29.5 mm from the end); in the CAD the M3 reaches about 4 mm under the rail end.

---

## 503. Upside down: left and right swap

`docs/manual/assets/diagrams/503-gantry-flip.svg`

**What it shows**

- Two top views from the front (idler) end. Before: motors down, rails underneath, B drive and B idler on the left, A on the right, with a dashed front-to-back line down the middle and one arrow rolling the gantry over it, left to right. After the roll: motors up, rails on top, A on the left, and the X axis landed with the right XY joint (the one with the cable bridge) on the A side, your left.

**Insert at**

- `docs/manual/05-gantry.md` — **Step 05.41**: what rolling it over does to left and right, and which end the right XY joint lands on.

**Drawn schematically / left unlabelled (verify)**

- Proportions are schematic. Any way of turning it over gives the same result once the idlers are nearest you; the roll about the front-to-back line is drawn because it keeps them nearest you throughout.

---

## 504. Endstop pod: on top, screws down

`docs/manual/assets/diagrams/504-endstop-pod-on-joint.svg`

**What it shows**

- Front view of the right XY joint with the gantry upside down on the bench: Y extrusion (backer now underneath), rail and carriage on top of it, the joint on the carriage and round the X extrusion's end, the endstop pod on top of the joint, and two M3×30 going down through pod and joint into the carriage (callout 2 is the Do number of Step 05.49).
- From above: the joint's four carriage holes, the M3×16 of Step 05.43 in the pair nearer the drives and the M3×30 in the pair nearer the idlers.

**Insert at**

- `docs/manual/05-gantry.md` — **Step 05.49**: which face the pod goes on and where its screws go.

**Drawn schematically / left unlabelled (verify)**

- Heights and widths come from the 250-size CAD (pod 15.4 mm, joint 14.3 mm over the carriage, M3×30 in the front pair at y 159, M3×16 in the rear pair at y 175); the joint's outline and the pod's shape are schematic, and the endstop board inside the pod is not drawn.

---

## 505. XY joint bearing stack

`docs/manual/assets/diagrams/505-xy-joint-bearing-stack.svg`

**What it shows**

- Side view as p.97 builds it: the thin plate at the bottom, the M5×40 pushed up through it (callout 2), then the stack touching item to item, spacer, F695 flange down, F695 flange up, spacer (callout 3), and the thick body coming down on top. Callouts 2 and 3 are the Do numbers of Steps 05.26 and 05.30. A small red panel shows the wrong way: flanges facing in.

**Insert at**

- `docs/manual/05-gantry.md` — **Step 05.26**: the stack order on the right joint.
- `docs/manual/05-gantry.md` — **Step 05.30**: the same stack on the left joint.

**Drawn schematically / left unlabelled (verify)**

- F695 and spacer sizes are to scale (13/15 mm, 1 mm spacer as in the CAD); the plate, body and screw head are schematic.

---

## 506. Rail one side, backer opposite

`docs/manual/assets/diagrams/506-rail-and-backer-faces.svg`

**What it shows**

- End views as the extrusions sit in the machine. Y extrusion: MGN9 rail and carriage underneath, backer on top. X extrusion: MGN12 rail on the front face, backer on the rear face.

**Insert at**

- `docs/manual/05-gantry.md` — **Step 05.17**: the Y extrusion's faces.
- `docs/manual/05-gantry.md` — **Step 05.34**: the X extrusion's faces.

**Drawn schematically / left unlabelled (verify)**

- Backer thickness (drawn 2.5 mm) is schematic; the 18 mm width is from the tanaes DXFs.

---

## 601. A stopper as a shelf

`docs/manual/assets/diagrams/601-rubber-stopper-shelf.svg`

**What it shows**

- Front view of one Z rail mid-way up its vertical: rail screws in every other hole, the lower Z joint on its carriage, and a rubber stopper in the free hole straight under the carriage, which stops on it when pushed down (callout 1).
- Four rails side by side with the joints at one height on the same hole (2) and the printed `z_rail_stop_x4` on each rail top (3).

**Insert at**

- `docs/manual/06-z-axis-and-gantry-squaring.md` — **Step 06.10**: the shelf and the matched height.

**Drawn schematically / left unlabelled (verify)**

- How the rubber stopper holds in the hole (pressed or screwed) is not in any source: it is drawn as a plug in the hole, and the step text says 'fit'.
- Hole pitch, carriage and joint sizes are schematic; the screwed holes follow Ch 02 (holes 2 to 18).

---

## 602. Fold the tail, tie it to itself

`docs/manual/assets/diagrams/602-belt-tail-tie.svg`

**What it shows**

- Side section of a gantry corner's top clamp, after p.120: the run from the Z idler comes down past the clip's far edge and bends under the upper clip and its two M5×16; the tail leaves the near edge, rises, folds back on itself, and one small zip tie goes round both layers just above the clip (callouts 1-3 = Do of Step 06.21).

**Insert at**

- `docs/manual/06-z-axis-and-gantry-squaring.md` — **Step 06.21**: the fold and the tie.

**Drawn schematically / left unlabelled (verify)**

- The fold's exact path is schematic: p.120 shows the tail folded over and tied to itself above the clip, and whether the tie also catches the running belt is a bench check.

---

## 603. Set it down on the joints

`docs/manual/assets/diagrams/603-set-gantry-down.svg`

**What it shows**

- Left panel: without stoppers, a long zip tie from the gantry corner up over the top frame extrusion before lowering (1), after p.114.
- Front view of one corner: the gantry corner with its lower clip and Z bearing block coming down (2) onto the domed top of the lower joint, parked on its rubber stopper. A corner that does not touch: slide that carriage UP (p.115's arrow). Holes off to one side: nudge the gantry, since the M5×40 is vertical and a carriage slide cannot move a hole sideways.

**Insert at**

- `docs/manual/06-z-axis-and-gantry-squaring.md` — **Step 06.13**: lowering and the fallback.

**Drawn schematically / left unlabelled (verify)**

- Block, joint and clip proportions are schematic; the gap above the joint is exaggerated to show the move.

---

## 604. The 150 mm span

`docs/manual/assets/diagrams/604-z-belt-span.svg`

**What it shows**

- Side view of one Z corner: the Z idler at the top, the run that is fixed to the gantry going down to the top clip, 150 mm from the idler axle to the clip (1), and the pluck point in the middle of that run, about 140 Hz (2). The other run goes on down to the Z drive.
- The tensioner screw up through the moving slider (the blue part that carries the pulley) into the fixed bracket, head down at the slider's underside: clockwise, looking up at it, pulls the idler up and tightens the belt (p.117 section).

**Insert at**

- `docs/manual/06-z-axis-and-gantry-squaring.md` — **Step 06b.3**: the span and the pluck point.

**Drawn schematically / left unlabelled (verify)**

- The span is drawn to scale (3.1 px/mm); the bracket, slider, screw position and the corner are schematic.

---

## 605. Turn it over, mark the ends

`docs/manual/assets/diagrams/605-turn-over-and-mark.svg`

**What it shows**

- The gantry from the left side, front on the left: upside down on the bench with the A/B motors up (as Ch 05 left it), turned over (1) to motors down, Y rails underneath and the X rail facing front, then FRONT and BACK tape on its ends (2) and the same marks on the frame.

**Insert at**

- `docs/manual/06-z-axis-and-gantry-squaring.md` — **Step 06.11**: the turn-over and the marks.

**Drawn schematically / left unlabelled (verify)**

- Which axis the gantry rolls about is not drawn; the front stays on the left in both views and the tape marks settle it. Parts are blocks, not outlines.

---

## 701. Fold, then cut both at once

`docs/manual/assets/diagrams/701-belt-fold-cut.svg`

**What it shows**

- The belt folded back on itself 2000 mm from its free end (callout 1), the cut through the fold and the cut through the reel side level with the free end (callouts 2), and the two equal belts with dots near each end of A (callout 3). Callouts are the Do numbers of Step 07.8.

**Insert at**

- `docs/manual/07-ab-belts.md` — **Step 07.8**: replaces the no-image placeholder.

**Drawn schematically / left unlabelled (verify)**

- Lengths are not to scale; 2000 mm per belt is from the LDO 350 Rev D+ BOM (6.21 m of 6 mm belt) and onetwo3D's 350 BOM (2 x 2000 mm).

---

## 702. Pluck the 150 mm span

`docs/manual/assets/diagrams/702-belt-span-150.svg`

**What it shows**

- Top view of the right front corner of the gantry, FRONT at the bottom: the A belt's inner run between the XY joint's toothed idler and the front idler, 150 mm centre to centre, marked as the run to pluck; the outer run drawn faint.
- The front-idler M3x40 head at the front: turned as seen from the front, clockwise = tighter, anticlockwise = looser (written, since a top view cannot show a rotation). The left side is the mirror, with the B belt.

**Insert at**

- `docs/manual/07-ab-belts.md` — **Step 07.30**: first, before the two CAD renders.

**Drawn schematically / left unlabelled (verify)**

- Positions are from the 2.4r2 CAD (250 build) with the XY joint moved to the 150 mm position; the joint and idler bodies are drawn as dashed outlines.
- Which run is plucked is derived: only the inner run has a free length between those two centres (the outer run passes the joint).

---

## 703. Belt slots: A upper, B lower

`docs/manual/assets/diagrams/703-belt-clamp-section.svg`

**What it shows**

- Section through the X carriage looking along the X extrusion, FRONT to the left: extrusion, rail, rail carriage, the A belt in the upper slot and the B belt in the lower one lying against the rail carriage's face, teeth towards the front, away from the extrusion, and the two M3x8 above and below them.

**Insert at**

- `docs/manual/07-ab-belts.md` — **Step 07.9**: second, after the p.131 crop.
- `docs/manual/07-ab-belts.md` — **Step 07.24**: second, after the p.139 crop.

**Drawn schematically / left unlabelled (verify)**

- Belt heights (A z 80-86, B z 70-76), the rail carriage face and the M3x8 heights are from the CAD; the carriage half is drawn as a plain block, its slot shapes are not.

---

## 704. Same length on both tails

`docs/manual/assets/diagrams/704-belt-tails-equal.svg`

**What it shows**

- Front view of the closed X carriage after p.141: both belts enter the right half from the right at their own heights, turn down in the seam and stick out below; a rule beside them shows both tails ending at the same mark. Callouts are the Do numbers of Step 07.27. A small red case shows unequal tails.

**Insert at**

- `docs/manual/07-ab-belts.md` — **Step 07.27**: first, before the p.141 crop.

**Drawn schematically / left unlabelled (verify)**

- Which tail sits nearer the seam, and the tail lengths, are schematic.

---

## 705. Away, back, measure again

`docs/manual/assets/diagrams/705-gantry-away-and-back.svg`

**What it shows**

- Top view: the X extrusion moved back a few centimetres (dashed) and forward again until the XY joint idler centres are 150 mm from the front idler centres on both sides (callout 1), then both belts read again (callout 2), the Do numbers of Step 07.33.

**Insert at**

- `docs/manual/07-ab-belts.md` — **Step 07.33**: replaces the no-image placeholder.

**Drawn schematically / left unlabelled (verify)**

- Schematic frame; distances are not to scale.

---

## 706. Out to the end, then 4 turns in

`docs/manual/assets/diagrams/706-tensioner-four-turns.svg`

**What it shows**

- A front idler from above, FRONT at the bottom: the M3x40 through the front wall, head on its washer, threaded into the back of the blue tension arm that carries the bearing stack. Callout 1: screw backed out, arm back to the end of its travel (pushed by hand if it does not follow). Callout 2: 4 turns in, arm pulled forward along the screw, so more tip shows behind it. The Do numbers of Step 07.5.

**Insert at**

- `docs/manual/07-ab-belts.md` — **Step 07.5**: first, before the p.128 crop.

**Drawn schematically / left unlabelled (verify)**

- Schematic block and arm shapes; the screw path (front wall, insert at the rear of the arm) is from the CAD and p.128's section.
- Whether the arm follows the screw back on its own with no belt on is not known; Step 07.5 says to push it back by hand if it does not.

---

## 707. Quarter turns, A then B

`docs/manual/assets/diagrams/707-quarter-turns.svg`

**What it shows**

- Both front idlers seen from the front, screw heads towards you: B on the left, A on the right. Callout 1: clockwise tightens, anticlockwise loosens. Callout 2: alternate quarter turns between the two. The Do numbers of Step 07.32.

**Insert at**

- `docs/manual/07-ab-belts.md` — **Step 07.32**: first; replaces 702 there.

**Drawn schematically / left unlabelled (verify)**

- Schematic idler faces. Clockwise = in = tighter follows from the head at the front (p.128 section, CAD) and the M3 right-hand thread.

---

## 801. Fan adapter on the 5015

`docs/manual/assets/diagrams/801-fan-adapter-on-5015.svg`

**What it shows**

- The Stealthburner body from behind with the 5015 in its upper pocket and the triangular SBurnerFanAdapter V2.0 lying flat on the fan's back, its two end holes over the two body holes SB p.64's M3×6 FHCS use, two M3×10 flat-head screws through both.
- P1's pins point back, at the toolboard, on the toolboard side of the body.
- Callouts 1 and 2 are the Do numbers of Step 08.44.

**Insert at**

- `docs/manual/08-toolhead.md` — **Step 08.44**: first image: what the hands do.

**Drawn schematically / left unlabelled (verify)**

- Body, fan and board outlines are schematic. Hole positions follow SB p.64 (the two M3×6 FHCS it replaces) and LDO's wiring guide (two M3×10 FHCS directly on the back of the 5015); that the board's two holes land on those two fan holes, and the board's exact rotation, are drawn from that and the board photo, not from a photo of it mounted (none published).

---

## 802. Ground wire, motor end

`docs/manual/assets/diagrams/802-ground-lug-motor-end.svg`

**What it shows**

- The extruder from behind after LDO's toolboard_ground_routing.jpg: toolboard on the left edge, the ground wire from the lower board screw round the motor can to a ring lug on the motor's lower ear, nearest the chain anchor.
- The lug bent up along the can, clear of the anchor below; a small Wrong panel shows it pointing down into the anchor.
- Callouts 1 and 2 are the Do numbers of Step 08.53.

**Insert at**

- `docs/manual/08-toolhead.md` — **Step 08.53**: first image: what the hands do.

**Drawn schematically / left unlabelled (verify)**

- Schematic proportions. What holds the lug (the supplied short screw, or a nut on the tip of the front M3×8 that shares the lower ear, as LDO's top-down photo may show) is unpublished: drawn generic and tagged for the bench.

---

## 803. Cartridge up, leads in

`docs/manual/assets/diagrams/803-cartridge-he0-th0.svg`

**What it shows**

- Side view from the toolboard side, front on the left: the tool cartridge pushed up under the extruder, held by the cartridge, not the nozzle (the body screws at 08.62 hold it; what holds it before then is tagged for the bench); the heater pair with ferrules into the HE0 screw terminal; the thermistor pair into TH0, the 2-pin socket to the left of HE0 (board pinout).
- Callouts 1 to 3 are the Do numbers of Step 08.61.

**Insert at**

- `docs/manual/08-toolhead.md` — **Step 08.61**: first image: what the hands do.

**Drawn schematically / left unlabelled (verify)**

- Schematic: board, terminal and socket sizes are not to scale. No screw heads or keyholes are drawn: the cartridge's four M3×8 sit in Ø5.8 counterbores in its top (STL) and clamp the Revo heatsink (SB p.50). TH0-left-of-HE0 and the board's front edge forward are from LDO's pinout and ground-routing photo.

---

## 804. Cover, header, body

`docs/manual/assets/diagrams/804-cover-and-header.svg`

**What it shows**

- Top: the extruder from the front with the latch open (closed again after), the M3×16 straight in through the front access hole (SB p.37-38) and the M3×6 BHCS into the cable cover's side wall, low at the front (SB p.38).
- Bottom: side view from the toolboard side, front on the left: the fan adapter's P1 pins pointing back, the toolboard's socket on its front edge, A1/A2 row on top and the 24V row at the bottom, the body pushed straight back; two M3×25 upper and two M3×50 lower from the front.
- Callouts 1 to 3 are the Do numbers of Step 08.62.

**Insert at**

- `docs/manual/08-toolhead.md` — **Step 08.62**: first image: what the hands do.

**Drawn schematically / left unlabelled (verify)**

- Schematic outlines. Reaching the M3×6 BHCS with the toolhead on the carriage is the step's (verify on bench) and is tagged. The socket's key is not drawn: no source shows where it sits. Row order is from LDO's board pinout.

---

## 805. Ends for HE0 and TH0

`docs/manual/assets/diagrams/805-revo-lead-ends.svg`

**What it shows**

- Top: the HeaterCore's heater and thermistor leads, each ending in a Micro-Fit plug (E3D Revo Voron page), marked never cut; the 1 m extension cables beyond them, with the cut line at their board end, only if LDO's cables do not mate.
- Bottom: the heater pair ending in two E0508 ferrules (8 mm tube); the thermistor pair in a 2-pin JST-PH2.0 housing (2.0 mm pitch), with XH2.5 marked as not fitting TH0.
- Callouts 1 and 2 are the Do numbers of Step 08.33.

**Insert at**

- `docs/manual/08-toolhead.md` — **Step 08.33**: first image: what the hands do.

**Drawn schematically / left unlabelled (verify)**

- What LDO packs for the Revo option is the step's (verify on bench); tagged. Ferrule collar and housing colours are not specified by the sources.

---

## 806. Toolhead LEDs from the front

`docs/manual/assets/diagrams/806-toolhead-led-index.svg`

**What it shows**

- The Stealthburner from the front: the two toolhead LEDs in the bottom corners either side of the nozzle, pushed in from the outside; index 2 on your right (SB p.54/p.56 'TOOLHEAD LED RIGHT'), index 3 on your left.
- Callouts 1 and 2 are the Do numbers of Step 08.37.

**Insert at**

- `docs/manual/08-toolhead.md` — **Step 08.37**: first image, before the p.56 crop.

**Drawn schematically / left unlabelled (verify)**

- Body outline schematic. Right = your right is read from the SB manual's own views: p.62 (from behind, upright) draws wires that 'exit on the right side' leaving to the drawing's left, and p.56 draws the body from behind upside down (LED pockets next to the 4010 pocket, the 5015 at the far end), so its RIGHT label sits on your right. No photo of a labelled build was found.

---

## 901. Where the PSU stops on the rear rail

`docs/manual/assets/diagrams/901-psu-on-rear-rail.svg`

**What it shows**

- The bay from the rear, printer on its head, FRONT at the top: the rear DIN rail, the SSR on its left, the PSU on its right with its terminal strip on the left end (AC terminals red), the dry-laid middle run and right narrowed T in front of it, and the SSR run of the AC conduit (red) behind the SSR.
- Callouts 1 and 2 are the Do numbers of Step 09.16: clip on at the right, slide left.
- Two enlargements: the PSU's left end 3 mm or more from the SSR run's open end (check on the bench), and its front-right corner 2 mm from the T's rounded corner.

**Insert at**

- `docs/manual/09-electronics-bay.md` — **Step 09.16**: first image: where the hands stop the PSU.

**Drawn schematically / left unlabelled (verify)**

- Positions are layout v3's apparent mm on LDO's placement photo (±6 % absolute, ±1.5 mm local); the PSU is drawn 215 × 115 at x −29…186. The T's fillet radius and the 2 mm gap in the enlargement are schematic. The 3 mm gap is the step's (verify on bench); tagged.

---

## 902. Check before the VHB goes down

`docs/manual/assets/diagrams/902-vhb-checks.svg`

**What it shows**

- Top: the middle run enlarged between the Leviathan's rear edge and the PSU's front, 1.5 mm or more each side; callout 1 is Do 1 of Step 09.36.
- Bottom: the AC conduit (red, mains) from the rear: the SSR run behind the SSR, the stub up into the port in the wire box's front wall, the box at the mains WAGO blocks, the two R15 curves and the 34 mm run over the round deck hole; callout 2 is Do 2.

**Insert at**

- `docs/manual/09-electronics-bay.md` — **Step 09.36**: first image: the three checks before VHB.

**Drawn schematically / left unlabelled (verify)**

- Bottom panel follows layout-v3.json segment coordinates (apparent mm). The stub's real length is set at B11.10 and is the step's (verify on bench); tagged. The middle-run gaps are drawn enlarged, not to scale.

---

## 903. SSR the right way round

`docs/manual/assets/diagrams/903-ssr-orientation.svg`

**What it shows**

- The SSR on its metal bracket on the rear rail, from the rear with the printer on its head: INPUT pair toward the front, LOAD pair (mains, red) toward the rear, the PSU's left end, terminal strip and all, to its right with about 30 mm of rail between (Do 2).
- Callouts 2 and 3 are the Do numbers of Step 09.18; Do 1 (open the latch) is not drawn.

**Insert at**

- `docs/manual/09-electronics-bay.md` — **Step 09.18**: first image, before p.171.

**Drawn schematically / left unlabelled (verify)**

- Terminal pairs and the LED side follow LDO's placement photo, which shows INPUT toward the front and LOAD toward the rear; terminals are labelled as pairs, not one by one. Which end of the bracket carries the spring latch is not drawn: the photo does not show it clearly.

---

## 904. Probe pin behind the plate

`docs/manual/assets/diagrams/904-probe-pin-gap.svg`

**What it shows**

- From above, rear at the top: the right bed extrusion, the build plate's straight rear edge overhanging the extrusion and running on past the panel edge, the probe body on the extrusion's inner face behind it on two M3×25, and its pin just behind the edge. Callouts 1–3 are the Do numbers of Step 09.30.
- Right: the gauge enlarged, a 2 mm hex key slides between pin and plate, a 3 mm key does not; p.161 draws 1.5 mm.

**Insert at**

- `docs/manual/09-electronics-bay.md` — **Step 09.30**: first image: the gauge.

**Drawn schematically / left unlabelled (verify)**

- Probe body shape and screw positions are schematic. The straight rear edge follows LDO's Rev D heater photo (aluminium edge straight); the recess in LDO's build-plate mapping outline is schematic. 2–3 mm is the Voron startup guide's gap (fetched 2026-11-20).

---

## 905. Press the inlet in

`docs/manual/assets/diagrams/905-inlet-press-in.svg`

**What it shows**

- Left: a cut through the inlet panel, the module (red, mains) pressed in from outside until its sprung tabs snap behind the panel wall; nothing on the spade terminals. Callouts 1 and 2 are the Do numbers of Step 09.11.
- Right: the panel from outside on the bench: the module's switch end toward the panel's curved cut-out, the socket and fuse drawer at the other end.

**Insert at**

- `docs/manual/09-electronics-bay.md` — **Step 09.11**: first image: what the hands do.

**Drawn schematically / left unlabelled (verify)**

- The panel's cut-out takes the module either way round (STL section). Switch end at the curved cut-out follows LDO's fitted photo (iec-inlet-module-fitted.jpg: the factory L-to-fuse bar and the earth spade sit at the end away from the Z motor) and p.167. No earth-pin direction is drawn: no source shows the socket face. The fuse sits in the socket half (LDO inlet_layout.png, rear view); the drawer's exact place on the face, the tab shape and proportions are schematic.

---

## 906. USB-adapter stack

`docs/manual/assets/diagrams/906-usb-adapter-stack.svg`

**What it shows**

- Front, after the Nitehawk-SB V2 grounding photo: the diamond base (labelled), the partial cover cut away at top-right (labelled), three M3×10, the top-right screw left bare with the DC Ground Wire's ring terminal under it, and the M2×10 heads in the base's two wing holes.
- Side: cover, PCB and base in that order, the DIN clip on the base's back on two M2×10 self-tapping screws driven from the front through the wing holes. Callouts 1–3 are the Do numbers of Step 09.25.

**Insert at**

- `docs/manual/09-electronics-bay.md` — **Step 09.25**: first image, before the Nitehawk photo.

**Drawn schematically / left unlabelled (verify)**

- Layer thicknesses are schematic. Screw direction from the STL (usb_adapter_mount_partial_cover: base wing holes Ø2.4 with Ø4 counterbores on the front, 32 mm apart; pcb_din_clip Ø1.9 pilots ~31 mm apart). The M2×10 count and length are the step's (verify on bench); tagged.

---

## 1001. Mains bus: one colour at a time

`docs/manual/assets/diagrams/1001-mains-bus-probe-points.svg`

**What it shows**

- The precondition in the picture: unplugged, cord out of the room.
- The inlet module: its C14 E, L and N pins, the fuse in series with L, the rocker breaking L and N together (drawn ON), E neither fused nor switched; each wire in its colour to its WAGO block and on to every point the 10.18 tables list: PE to PSU 3 FG, the bed plate screw, the frame lug and a far frame corner; L to PSU 1 L and SSR LOAD 2; N to PSU 2 N and the bed N lead. One probe parked on the pin, the other walked along.
- Callouts 1 to 3 are the Do numbers of Step 10.18.

**Insert at**

- `docs/manual/10-wiring.md` — **Step 10.18**: replaces the no-image line.

**Drawn schematically / left unlabelled (verify)**

- A wiring schematic, not a layout: block positions do not match the bay. Fuse and rocker placement inside the module from LDO's inlet_layout.png. The Bed L branch (SSR LOAD 1) stays in the step's table.

---

## 1006. Between colours: silent

`docs/manual/assets/diagrams/1006-mains-isolation-pairs.svg`

**What it shows**

- The precondition in the picture: unplugged, cord out of the room.
- The three pairs L-N, L-PE and N-PE crossed out at the WAGO blocks, drawn in their bench order N, L, PE (Step 10.7; rocker on, then off) and at the PSU screws 1 L, 2 N, 3 FG, with the expected readings: L to N 100 kΩ or more or OL, L or N to PE OL. Callouts 1 and 2 are the Do numbers of Step 10.19.

**Insert at**

- `docs/manual/10-wiring.md` — **Step 10.19**: replaces the no-image line.

---

## 1002. COB mount: inserts, then the lid

`docs/manual/assets/diagrams/1002-cob-mount-inserts.svg`

**What it shows**

- Front view of one COB mount with the lid half lifted: two inserts in the base half's top face, 6 mm from each end; the lid's two countersunk holes over them and two M3×6 FHCS going in; the base half's two counterbored holes, 12.8 mm from each end, left for Step 10.36.
- Below: the 8 mounts (three 100 mm and one 50 mm per strip), the two retainer brackets with one insert each and the TFT mount with two, 20 inserts in one pass. Callouts 1 and 2 are the Do numbers of Step 10.35.

**Insert at**

- `docs/manual/10-wiring.md` — **Step 10.35**: replaces the no-image line.

**Drawn schematically / left unlabelled (verify)**

- Insert and screw positions are from the 100 mm STL (numpy bore probe) and LDO's cob_mount_install.png; the halves' cross-section is not drawn, and the strip is left out because the sources do not show how it sits in the mount.

---

## 1003. 5 V check on the HAT adapter

`docs/manual/assets/diagrams/1003-hat-adapter-5v-pads.svg`

**What it shows**

- Top view of the Pi 4's GPIO edge with the 3/4 HAT adapter over pins 1 to 24 (2 × 12 bare pads on top), pins 25 to 40 bare beside it, the adapter's 6-pin socket and its cable to J9.
- Red probe on the edge-row pad at the microSD end (pin 2, 5 V), black probe on the third pad of that row (pin 6, GND); pin 4 also 5 V. Unplugged, in the picture.

**Insert at**

- `docs/manual/10-wiring.md` — **Step 10.75**: replaces the no-image line.

**Drawn schematically / left unlabelled (verify)**

- Board outline and adapter shape are schematic. Pin positions follow pinout.xyz (pin 1 at the end away from the USB ports, even pins on the board edge) and LDO's rpi4_installed_V1.3.jpg (12 columns of pads on the adapter).

---

## 1004. 24 V probe points

`docs/manual/assets/diagrams/1004-24v-probe-points.svg`

**What it shows**

- The PSU's nine screws in datasheet order, 1 L, 2 N, 3 FG (mains screws, not part of this test; 10.18, 10.19 and 10.77 meter them with the cord out), the fin, then 4 to 6 −V and 7 to 9 +V, with the black probe on −V and the red on +V; first DC V, 0 V for ten seconds (10.73).
- Then on Ω the three 24 V inputs, Leviathan Vin 24V, Vin 24-48V and the USB adapter's 24V IN, + to −: all read the same, never 0 Ω; and the two rows to the C14 earth pin (10.74).

**Insert at**

- `docs/manual/10-wiring.md` — **Step 10.73**: replaces the no-image line.
- `docs/manual/10-wiring.md` — **Step 10.74**: replaces the no-image line.

**Drawn schematically / left unlabelled (verify)**

- Screw order from the Mean Well LRS-200 datasheet; the inputs are drawn as generic two-screw blocks, not their real shapes or positions on the boards.

---

## 1005. Earth: one probe stays on C14 E

`docs/manual/assets/diagrams/1005-earth-bonding-points.svg`

**What it shows**

- The C14 inlet seen from outside with the black probe on its E pin, and the five bonding points from the 10.77 table with their limits: PE WAGO, PSU 3 FG, the frame lug's screw head, the plate's M4×6 screw head (< 1 Ω each) and a far frame corner's screw head or T-nut (< 2–3 Ω).
- Callout 1: probes touched together, the reading to subtract. Callout 2: the probe on the earth pin. A small Wrong panel: a probe on an anodised face reads OL.

**Insert at**

- `docs/manual/10-wiring.md` — **Step 10.77**: first image: what the hands do.

**Drawn schematically / left unlabelled (verify)**

- A checklist picture, not a layout. The extruder, heater and 24 V rows of the 10.77 table stay in the table.

---

## 1101. Door hinges on the left front vertical, pins up

`docs/manual/assets/diagrams/1101-door-hinges-pins-up.svg`

**What it shows**

- The machine's left side, front to the right: the printer's front left vertical and, a labelled foam strip in front of it, the door frame's left vertical, each named with a leader; a band of blue tape across both.
- Two hinges, each a printer half below (pin pointing up) and the door half above it, the top one just under the top corner clip with a small gap, the bottom one just above the bottom corner clip; two screws per half.
- Callouts 1 to 3 are Step 11.62's Do numbers: tape and T-nuts, hinges on loosely pins up, all eight screws tightened once the door hangs parallel.

**Insert at**

- `docs/manual/11-skirts-panels-door.md` — **Step 11.62**: first image: what the hands do.

**Drawn schematically / left unlabelled (verify)**

- Hinge outlines are schematic boxes. The pin axis is drawn on the foam line between the two verticals; its exact front-to-back position is not dimensioned.
- The printer half carries the pin, pointing up, with the door half on top: from the README ('pins should point up', the door 'can be easily removed from the hinges simply by lifting up') and tanaes' hinge cut-away render. KB3D's photos do not show which half is which clearly.
- Heights along the vertical are schematic: KB3D's guide puts the hinges against the top and bottom corner clips with a little gap. Both halves screw into the outer side-face slot of their vertical, as KB3D's photos show.

---

## 1102. Handle and latch on the right side, lined up with a paper shim

`docs/manual/assets/diagrams/1102-handle-latch-shim.svg`

**What it shows**

- The machine's right side, front to the left: the door frame's right vertical, 3 mm of foam, the printer's front right vertical and the side panel's edge.
- The latch on the printer vertical over the panel edge (callout 2: centred and tightened first), the two handle hinges on the door frame (callout 1), the handle between them over the latch, a paper shim at each end of the handle, and the up-and-down slide that lines the handle up (callout 3).
- Callouts 1 to 3 are Step 11.64's Do numbers.

**Insert at**

- `docs/manual/11-skirts-panels-door.md` — **Step 11.64**: first image: what the hands do.

**Drawn schematically / left unlabelled (verify)**

- Outlines are schematic: the handle (60 mm) and latch (58 mm) heights are from their STLs; the handle-hinge widths and the gaps in the stack are not to scale.
- The latch takes the place of the side panel's front-edge midspan clip (11.63), centred on that edge, from the KB3D guide; the side panel edge is drawn 13.5 mm behind the front face (483 mm panel on a 510 mm frame).

---

## 1103. 3 mm foam on the front face of the front opening, corners butted

`docs/manual/assets/diagrams/1103-front-opening-foam.svg`

**What it shows**

- A section from above through the left side of the front opening: the printer's front left vertical, 3 mm foam on its front face along the inner edge, and the door frame with its panel closing onto the foam.
- The opening from the front with a foam strip along the inner edge of all four extrusions, the corners butted; a small overlapped corner marked wrong.

**Insert at**

- `docs/manual/11-skirts-panels-door.md` — **Step 11.51**: first image: what the hands do.

**Drawn schematically / left unlabelled (verify)**

- The foam strip's width (drawn about 9 mm) and its exact place on the face are schematic; the kit's 3 mm tape width is not published.
- The door frame is drawn straight in front of the printer vertical because both frames are 510 mm wide; the opening's proportions in the lower view are schematic.
- KB3D's guide says to put the foam 'on the inner portion of the extrusion' in its door-frame section, so the door frame's back face may be meant; the step marks it '(verify on bench)' and the drawing carries a 'check on the bench' note.

---

## 1104. Clicky-Clack door frame: the order

`docs/manual/assets/diagrams/1104-door-frame-order.svg`

**What it shows**

- Row 1: an M5×16 BHCS started halfway into each tapped end of a 470 mm piece (two such pieces).
- Row 2: both 530 mm pieces fitted to one 470 mm piece, the key going in through the access holes on their outer faces, both corners squared.
- Row 3: the acrylic sliding down into the frame's slots, then the second 470 mm piece closing the fourth side. Callouts 1 to 3 are Step 11.44's Do numbers.

**Insert at**

- `docs/manual/11-skirts-panels-door.md` — **Step 11.44**: first image: what the hands do.

**Drawn schematically / left unlabelled (verify)**

- Bar widths are exaggerated; the 470 and 530 mm lengths are to scale. The panel (480 × 500 mm) is drawn reaching into the slots of the 530 mm sides.
- The access holes are drawn at the ends of the 530 mm pieces on their outer faces, where a blind joint needs them (Ch 01's diagram 15); not dimensioned from the kit.

---

## 1105. Nevermore plenum between the bed extrusions, T-nuts in the inside faces

`docs/manual/assets/diagrams/1105-plenum-on-bed-extrusions.svg`

**What it shows**

- Top view, FRONT at the bottom: the plenum filling the 130 mm gap between the two bed extrusions, just behind the front corner brackets.
- One M3×12 SHCS out through each end wall, near its rear edge, into a T-nut in the inside face of each bed extrusion.
- Below: the inside-face slot end-on with the T-nut and screw, and the top slot marked wrong.

**Insert at**

- `docs/manual/11-skirts-panels-door.md` — **Step 11.38**: first image: what the hands do.

**Drawn schematically / left unlabelled (verify)**

- The plenum's distance behind the front corner brackets is schematic; LDO's CAD image (guide § Installation for Voron V2.4) shows it just behind them.
- From V2_Duo_Plenum.stl: 130.0 mm wide, one Ø3.2 bore along X through each end wall, 6.2 mm from one long edge; that edge is drawn as the rear, as LDO's CAD image shows the screws.

---

## 1106. Side spool frame on the right side

`docs/manual/assets/diagrams/1106-side-spool-frame-and-holder.svg`

**What it shows**

- The right side from outside, FRONT to the left, at 3.3 px per mm from the remix STL: the frame's two feet on the 13.5 mm strip of bare aluminium beside the panel, one on the top extrusion and one on the front vertical, a screw into a T-nut in each outer slot.
- The puck on its boss and the USS Drybox outline (217 × 219 mm, on the puck). Callouts 1 and 2 are Step 11.71's Do numbers.

**Insert at**

- `docs/manual/11-skirts-panels-door.md` — **Step 11.71**: first image: what the hands do.

**Drawn schematically / left unlabelled (verify)**

- The panel edge is drawn 13.5 mm in from the frame edges (483 mm panel on a 510 mm frame); the frame outline, feet and puck axis are from the remix STL.

---

## 1107. One PTFE from the CW2.5 to the side spool, seen from above

`docs/manual/assets/diagrams/1107-side-spool-tube-route.svg`

**What it shows**

- The top of the frame from above, FRONT at the bottom: the tube holder in the top right extrusion's top slot about 22 cm behind the front, the bowden retainer on the top rear extrusion, and the exhaust cover's coupler at the back centre.
- One PTFE from the CW2.5 out through the coupler, through the retainer, forward to the holder and down to the spool outside the right side, cut square there. Callouts 1 to 3 are Step 11.72's Do numbers.

**Insert at**

- `docs/manual/11-skirts-panels-door.md` — **Step 11.72**: first image: what the hands do.

**Drawn schematically / left unlabelled (verify)**

- The 'about 22 cm' is drawn to the holder's front end; the README says about 22 cm without naming the end. The holder clearing the box and the top-panel clips is '(verify on bench)' in the step, so the drawing labels its spot 'check on the bench'.
- The retainer's spot along the rear extrusion follows p.258 (beside the exhaust, toward the right side) but is not dimensioned; the tube's path and the toolhead position are schematic.

---

## 1201. Power on: where to stand and look

`docs/manual/assets/diagrams/1201-power-on-stance.svg`

**What it shows**

- The machine on its side with the bay toward you, the adult standing to the side at the rear (inlet) end with one hand on the rocker and the other down, the cord from the inlet to the wall.
- Mains parts in red (inlet, WAGO blocks, SSR, the PSU's terminal block); where to look: PSU LED, the Pi's red PWR and green ACT, the touchscreen, and the printhead's 3V3 and 24V LEDs.
- Callouts 2 and 3 are the Do numbers of Step 12.11.

**Insert at**

- `docs/manual/12-software.md` — **Step 12.11**: first image: what the hands do.

**Drawn schematically / left unlabelled (verify)**

- Drawn on its right side, as 12.11 Do 2 now says (Alex's ruling 2026-11-20), which puts the rear-left inlet and its rocker uppermost.
- Bay positions are read off LDO's Rev D finished-bay photo (a Rev D bay, PVC ducts; this build uses printed B11 conduits) and turned to that orientation. The person is not to scale.
- The Pi LED position (the Pi's short edge away from its USB ports) is from the Raspberry Pi 4 photo; on the bench the DSI ribbon runs close by.

---

## 1202. SW1 and SW2: reach from above

`docs/manual/assets/diagrams/1202-leviathan-sw1-sw2.svg`

**What it shows**

- Left: the bay in 1201's orientation with the Leviathan outlined, a green reach path from above straight down to SW1, and a red dashed line at the front edge of the PSU and SSR (the middle duct) not to be passed.
- Right: a close-up in the same orientation: heatsink at the rear, J9 with the Pi's power lead, SW1 RESET above SW2 BOOT, the processor on the front side.

**Insert at**

- `docs/manual/12-software.md` — **Step 12.15**: first image: where the hand goes.

**Drawn schematically / left unlabelled (verify)**

- Button order and side follow LDO's frontsw1sw2.jpg (SW2 Boot left of SW1 Reset above the processor) turned 180° as the board sits in LDO's Rev D bay photo, then 90° for the machine on its right side.
- In LDO's rpi4_installed_V1.3 photo the J9 Pi power lead runs over the buttons; in the Rev D bay photo it does not. Where it runs on this build is a bench fact.
- The reach direction assumes the machine lies on its right side, as 12.11 says. The red line is the limit the 12.15 warning names: the arm stays in front of the middle duct.

---

## 1203. Which Leviathan: read the chip

`docs/manual/assets/diagrams/1203-leviathan-chip-marking.svg`

**What it shows**

- The Leviathan as LDO photographs it, stepper sockets along the top: the processor with SW2 and SW1 above it, and the VORON / Leviathan V1.x line at the lower right, under the Pi drawn see-through as mounted in Ch 09.
- A footnote says the drawing keeps LDO's photo orientation and that in the bay the board is turned, so the chip lettering reads sideways.
- STM32F446… = V1.1 or V1.2; STM32H743… = V1.3.

**Insert at**

- `docs/manual/12-software.md` — **Step 12.13**: first image: where to look.

**Drawn schematically / left unlabelled (verify)**

- Chip marking and version text positions from LDO's frontsw1sw2.jpg and frontsw1sw2_V1.3.jpg (STM32F446ZET6, STM32H743ZIT6); the Pi's footprint from rpi4_installed_V1.3.jpg and LDO's Rev D bay photo, both of which hide the version line under the Pi.
- In the bay the board is turned (see 1202); the drawing keeps LDO's photo orientation so the chip text reads the right way up.

---

## 1204. Which line goes where

`docs/manual/assets/diagrams/1204-serial-paths.svg`

**What it shows**

- ls /dev/serial/by-id/ output with two usb-Klipper_ lines, each chip name underlined: the stm32f446xx one (mainboard) arrowed into the [mcu] box on the left, the stm32g0b1xx one (toolboard) into the [mcu nhk] box on the right, boxes in printer.cfg order; landscape, because 12.23 renders stacked with the picture capped at 40vh.

**Insert at**

- `docs/manual/12-software.md` — **Step 12.23**: first image.

**Drawn schematically / left unlabelled (verify)**

- Strings follow the chapter's own code (12.12 table, 12.23 config). ls sorts by name, so f446 lists above g0b1 and an H743 below it; the step says to match by chip family, not order.

---

## 1205. Leviathan menuconfig

`docs/manual/assets/diagrams/1205-leviathan-menuconfig.svg`

**What it shows**

- A settings card in menuconfig's screen order: the low-level tick and Micro-controller Architecture for both versions, then Processor model, Bootloader offset and Clock Reference side by side for F446 (V1.1, V1.2) and H743 (V1.3), then Communication interface, the same on both.

**Insert at**

- `docs/manual/12-software.md` — **Step 12.14**: first image: the settings in the code blocks.

**Drawn schematically / left unlabelled (verify)**

- Values are the step's own code fences, character for character; they match LDO's Leviathan V1.2 and V1.3 guides (fetched 2026-11-20). LDO writes 'Microcontroller Architecture'; Klipper's menu, and the step, write 'Micro-controller'. The screen layout is a card, not a screenshot.

---

## 1206. Why -10,-10 cannot be reached

`docs/manual/assets/diagrams/1206-safe-z-home.svg`

**What it shows**

- Top view, front at the bottom: the travel square 0 to 350 in X and Y, the shipped -10,-10 outside its front-left corner (refused), the nozzle-probe pin near the rear edge right of centre, and, small in red, the bed centre as a guess with no pin under it.

**Insert at**

- `docs/manual/12-software.md` — **Step 12.33**: first image.

**Drawn schematically / left unlabelled (verify)**

- Travel limits are the config's position_min 0 / position_max 350. The pin is placed after Ch 09.30 (right bed extrusion's inner face, just behind the plate's rear edge, extrusions 65 mm either side of centre); its coordinates are measured in Ch 13 and the drawn spot is approximate.

---

## 1207. DFU: both down, SW1 up first

`docs/manual/assets/diagrams/1207-leviathan-dfu-press.svg`

**What it shows**

- Three close-ups of SW1 (above) and SW2 (below) beside the processor, in 1202's orientation: both pressed, SW1 released, then SW2 released; callout 2 is the Do number of Step 12.16; a red caption repeats the 12.15 reach limit.

**Insert at**

- `docs/manual/12-software.md` — **Step 12.16**: first image: the press order.

**Drawn schematically / left unlabelled (verify)**

- Press order from LDO's Leviathan V1.2 and V1.3 guides (fetched 2026-11-20): press both SW2 and SW1 at the same time, release SW1 first, then SW2. Button positions as in 1202. Whether one fingertip covers both buttons is a bench fact.

---

## 1301. Hand under the gantry first

`docs/manual/assets/diagrams/1301-hand-under-gantry-m84.svg`

**What it shows**

- Front view of the machine: a hand flat under each end of the gantry beam, `M84` sent by the second person, and the gantry lowered evenly by hand from high up to a third of its travel, nozzle about 100 mm above the plate (callout 1); the toolhead pushed to the middle (2).

**Insert at**

- `docs/manual/13-initial-startup.md` — **Step 13.17**: a hand under each end of the gantry and the lowered height.

**Drawn schematically / left unlabelled (verify)**

- Frame, gantry, toolhead and hand are schematic; the gantry's starting height is drawn high and dashed because the step does not say where it is.
- 100 mm is the step's figure (a third of the 330 mm Z travel, `[stepper_z] position_max: 330`), drawn to scale against the plate.
- Both hands under the beam because the four Z motors are released at once: lowered by one end, the gantry tilts (review 2026-11-20). Whether and how fast it sinks on its own is for the bench.

---

## 1302. Tape at 120 mm, then read R

`docs/manual/assets/diagrams/1302-rotation-distance-tape.svg`

**What it shows**

- The top of the Clockwork 2.5 with its collet, the PTFE lifted off the filament, and a rule with zero at the collet top: tape at 120 mm before (callout 3), and after `G1 E100 F60` the tape at R, about 20 mm.

**Insert at**

- `docs/manual/13-initial-startup.md` — **Step 13.40**: where the tape goes and where R is read from.

**Drawn schematically / left unlabelled (verify)**

- The Clockwork 2.5 body, collet and tube are schematic; lengths along the rule are to scale (120 mm, 20 mm).
- How far the PTFE has to be lifted to bare 120 mm of filament depends on the tube's slack at the park position: check on the bench.

---

## 1303. Shaft under the nozzle

`docs/manual/assets/diagrams/1303-probe-under-nozzle.svg`

**What it shows**

- From above: the toolhead after `G28 X Y` at the rear-right, jogged left along the rear to the nozzle probe on the right bed extrusion's inner face (callout 1), after LDO's build-plate mapping.
- From the side, rear to the left: the probe body on the extrusion with its two M3×25 screws (2), slid until the shaft is directly under the nozzle, and the 2 to 3 mm gap between the shaft and the plate's rear edge, after Voron manual p.161 and the startup wizard's Bed locating.

**Insert at**

- `docs/manual/13-initial-startup.md` — **Step 13.24**: the nozzle over the shaft, the gap and the two screws.

**Drawn schematically / left unlabelled (verify)**

- The 2 to 3 mm gap is drawn wider than scale so it can be seen; the plate, spacer and probe body are schematic (the LDO body is taller than p.161's).
- Bed-extrusion spacing in the top view is schematic; the probe's side and face follow LDO's build-plate mapping and Ch 09 Step 09.30.
- The side view looks from the middle of the bed at the probe on the right extrusion's inner face, so the rear is on the left; diagrams 1305 and 1308 look from the machine's left and keep the rear on the left too.

---

## 1304. Paper test: step down to the first drag

`docs/manual/assets/diagrams/1304-paper-test-testz.svg`

**What it shows**

- The nozzle over a sheet of paper on the plate (callout 1); `TESTZ Z=-1` until close, `TESTZ Z=-0.1` to the drag, `TESTZ Z=0.1` to back up (2); three feels: slides free (keep going), light drag with the tip resting on the paper (`ACCEPT`, 3), pinned with the tip pressed into it (back up).

**Insert at**

- `docs/manual/13-initial-startup.md` — **Step 13.36**: the step sizes and the feel to accept at.

**Drawn schematically / left unlabelled (verify)**

- Heights are schematic; the step sizes are the wizard's and Klipper's `TESTZ` values as the step sends them.

---

## 1305. H at the rear edge, w in the hand

`docs/manual/assets/diagrams/1305-scrubber-measurements.svg`

**What it shows**

- Side view seen from the machine's left, rear to the left: the caliper standing on its end on the flex plate at the plate's rear edge, its depth rod run down to the left bed extrusion's top, giving H (callout 1); the A1 wiper's height w, base underside to bristle tips, measured in the hand (2).

**Insert at**

- `docs/manual/13-initial-startup.md` — **Step 13.45**: where H and w are measured.

**Drawn schematically / left unlabelled (verify)**

- The caliper, plate stack and wiper are schematic. H is drawn 20 mm to scale (the author's 20.05 mm); the depth rod must run just past the plate edge, which is how the step words it.
- Seen from the machine's left so the rear is on the left, the same way round as diagram 1303's side view.

---

## 1308. d, G and O behind the plate

`docs/manual/assets/diagrams/1308-omron-height-and-reach.svg`

**What it shows**

- Side view seen from the machine's left, rear to the left: the toolhead at full Y with the nozzle tip at the flex plate's level, the Omron 25 mm behind it; d, the Omron face above the nozzle tip (callout 1); G, the Omron face above the left bed extrusion's top (2); O, how far the nozzle reaches past the plate's rear edge (3). Foot note: d and G are read at Z10, less 10.

**Insert at**

- `docs/manual/13-initial-startup.md` — **Step 13.46**: where d, G and O are measured.

**Drawn schematically / left unlabelled (verify)**

- d is drawn as 6 mm so it can be read at 480 px (expected about 0.6 mm); the plate stack and toolhead are schematic. H 20 mm, the Omron's 25 mm `y_offset` and 17 mm body and O 4.5 mm are drawn to scale.
- Split from 1305 (review 2026-11-20) so each step's callouts match its own Do numbers.

---

## 1306. Hand on the rocker, eyes on the bay

`docs/manual/assets/diagrams/1306-power-on-hand-on-rocker.svg`

**What it shows**

- The machine on its right side with the bay toward you, the open bay marked live, eyes only; one adult standing beside the rear end, not in front of the bay (callout 1), hand on the inlet's rocker with the mains lead in red (2), looking into the bay (3).

**Insert at**

- `docs/manual/13-initial-startup.md` — **Step 13.3**: where to stand and where the hand goes.

**Drawn schematically / left unlabelled (verify)**

- The machine lies on its right side (owner's ruling 2026-11-20, now in Step 13.2), which puts the rear end on your left and the inlet, at the rear-left corner (Ch 09 Step 09.2), at the top of that end.
- The person, frame and bay are schematic; the bottom door is left out.

---

## 1307. First layer, cut across the lines

`docs/manual/assets/diagrams/1307-first-layer-squish.svg`

**What it shows**

- Three sections across first-layer lines on the plate: round lines with gaps (too high, `Z_ADJUST=-0.01` brings it closer), flattened lines that touch but each still shows (right), and a ridged, glassy sheet (too low, `Z_ADJUST=0.01`); callout 2, the step's live-adjust Do, beside both `Z_ADJUST` lines.

**Insert at**

- `docs/manual/13-initial-startup.md` — **Step 13.42**: what the right squish looks like.

**Drawn schematically / left unlabelled (verify)**

- Line shapes are schematic, after the step's Check (no gaps, no ridging, each line visible) and Voron's first-print page (which shows no first-layer example).

---

## 1401. A and B: 110 Hz each

`docs/manual/assets/diagrams/1401-ab-belts-110hz.svg`

**What it shows**

- Top view of the gantry's front half, FRONT at the bottom: X and Y motors off while the Z motors hold (1); the X extrusion pushed forward (2) until each XY joint's toothed idler is 150 mm, centre to centre, from its front idler; the A belt's inner run on the right and the B belt's on the left, the runs to pluck (3); the X extrusion moved back a few centimetres and returned before both are plucked again (4); the two front tensioner screws, heads at the front, in = tighter.
- A spectrum strip: read the lowest peak, about 110 Hz, not a louder or higher one (3).

**Insert at**

- `docs/manual/14-calibration.md` — **Step 14.4**: first, before the app screenshot.

**Drawn schematically / left unlabelled (verify)**

- Which run is plucked and the screw head at the front follow diagram 702 (2.4r2 CAD, 250 build); block outlines and the spacing across X are schematic.
- The spectrum is illustrative: peak heights and the harmonics are not a measurement.

---

## 1402. Lock the Z joints hot

`docs/manual/assets/diagrams/1402-z-joints-hot.svg`

**What it shows**

- From above, door open at the front: the four lower Z joints at the corners, the front pair reached straight in and the rear pair along the sides, rear pair first (3); the bed at 110 °C in red, arm off it; a side panel off if a rear joint is out of reach.
- One joint from the side: the M5×40 runs up from below, its head under the lower joint, turned with a ball-end 4 mm key at an angle, the gantry at the height noted at 14.3.

**Insert at**

- `docs/manual/14-calibration.md` — **Step 14.6**: first, before any other image.

**Drawn schematically / left unlabelled (verify)**

- Joint, bed and frame proportions are schematic, and so is the reach path beside the bed; whether an arm reaches the rear pair through the door on this 350 is the step's own fallback (take that side panel off).
- Screw head at the bottom of the lower joint: 2.4r2 CAD (head z 11-16, tip z 56) and Step 06b.13 ('run one M5×40 up into each from below').

---

## 1403. Tape at 120 mm, read R

`docs/manual/assets/diagrams/1403-extruder-tape-r.svg`

**What it shows**

- Before: the hotend at 260 °C (1); the PTFE tube out of the collet, its ring pressed down, and slid about 130 mm up (check on the bench); tape on the bare filament 120 mm above the collet (2), a rule beside it.
- After 100 mm: the tape has moved down to R above the collet, about 20 mm; pushed through = 120 − R.

**Insert at**

- `docs/manual/14-calibration.md` — **Step 14.7**: replaces the no-image placeholder.

**Drawn schematically / left unlabelled (verify)**

- Tube out of the collet so the tape sits on bare filament: Ellis marks where the filament enters the extruder, and the reverse-bowden covers it up to the collet (Ch 08: collet and clip, SB p.21). The ~130 mm of tube slack is the step's bench check.
- Filament, tape and R are to scale (3.3 px/mm); the toolhead is a block.

---

## 1404. Measure at mid-height

`docs/manual/assets/diagrams/1404-cube-mid-height.svg`

**What it shows**

- The 30 mm cube from the front with its first layer bulging (exaggerated): the caliper jaws on the faces at mid-height for X, then Y; Z as the total height; the wider first layer measured only for its own table row.

**Insert at**

- `docs/manual/14-calibration.md` — **Step 14.11**: replaces the no-image placeholder.

**Drawn schematically / left unlabelled (verify)**

- Voron_Design_Cube_v7.stl is 30 × 30 × 30 mm with flat faces at mid-height (0.2 mm chamfer on the bottom edge); the bulge is exaggerated.

---

## 1405. Prove it dead: 0 V

`docs/manual/assets/diagrams/1405-psu-prove-dead.svg`

**What it shows**

- The step's precondition first: the Pi shut down (1); rocker off and the cord out of the wall, the inlet and the room (2); one adult only.
- On its side with the bottom panel open (3): the LRS-200's nine terminals, L, N and FG in red (mains, never probed), three −V and three +V; black probe on −V, red on +V; the LED dark; the meter on DC volts holding 0 V for 10 s.

**Insert at**

- `docs/manual/14-calibration.md` — **Step 14.30**: replaces the no-image placeholder.

**Drawn schematically / left unlabelled (verify)**

- Terminal order from the Mean Well LRS-200 datasheet (pin 1 AC/L, 2 AC/N, 3 FG, 4-6 −V, 7-9 +V); the LED's place beside the +V end follows Step 11.67. Which way up the strip appears with the machine on its side is not drawn.

---

## 1406. Z belts: 140 Hz each

`docs/manual/assets/diagrams/1406-z-belt-span-140hz.svg`

**What it shows**

- One Z corner from the side: the gantry jogged up (1) until its top clip is 150 mm below the Z idler pulley centre; the fixed run between them plucked on its outer side, about 140 Hz (2); the other run, down to the Z drive, not plucked.
- The tensioner from p.117: the M3 head points down inside the blue sliding body above the pulley and threads up into the fixed mount; clockwise, looking up, is tighter. All four corners, then Z down and back up and read again (3).

**Insert at**

- `docs/manual/14-calibration.md` — **Step 14.5**: first, in place of Ch 06's 604.

**Drawn schematically / left unlabelled (verify)**

- Screw head down in the sliding body above the pulley: p.117 section view; the hex key reaches it from below. Proportions are schematic; the span is to scale (2.8 px/mm).
- Fixed run = idler to the gantry's top clip: Voron secondary tuning, Z belts step 1.

---

## Markdown to paste in

Diagrams sit in the step's image block, in the same position a manual page image would take:

```markdown
![The six A/B bearing stacks](assets/diagrams/01-ab-bearing-stacks.svg)
```

From `00-index.md` the path is the same; from a print-batch chapter under `docs/manual/print/` it is `../assets/diagrams/…`.

## Regenerating

```
python3 scripts/draw_diagrams.py            # all 104 + this file
python3 scripts/draw_diagrams.py --only 3 7 # just those two
```

The script has no third-party dependencies — it emits SVG strings directly. To check a render: `rsvg-convert -w 1200 -o /tmp/x.png docs/manual/assets/diagrams/03-corexy-belt-path.svg`.
