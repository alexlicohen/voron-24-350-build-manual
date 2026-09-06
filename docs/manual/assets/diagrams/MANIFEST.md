# Diagram manifest

Eleven generated SVGs covering the things the official manual states in prose but never draws. Regenerate with `python3 scripts/draw_diagrams.py`; the geometry and every label live in that script, not here.

No chapter has been edited. The **Insert at** column is the proposal: the chapter file and the step whose image block the diagram belongs in.

All eleven are 1200 px wide, legible at 800 px, and safe on a dark page — each carries its own light background rect and pins `color` on the `<svg>` root, so `currentColor` text stays dark whether the file is referenced with `<img>` or inlined. Style is uniform: 2 px strokes, orange for `[a]_` accent parts, blue for the frame and extrusions, grey for hardware, teal and violet for the A and B belts.

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

- Lane spacing and the position of the two bearing stacks and the motor pulley *within* each drive unit are schematic. The chapters fix the order of the wraps (stack, pulley, stack) and which stack the other belt turns on, not their top-view coordinates.
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

- A racked gantry against a square one in exaggerated top view, with the four measurement points (front-left, rear-left, front-right, rear-right) marked on both.
- The two tolerances: front and rear on the same side within 0.5 mm, left and right within 1 mm, plus the machinist-square check at each front corner.
- Which fasteners come loose and in what order — lower Z joints, X/Y joints, A/B joints and front idlers — and the de-racking move itself.
- The one thing not to over-loosen: an X/Y joint that also carries a Z belt clamp.

**Insert at**

- `docs/manual/06-z-axis-and-gantry-squaring.md` — **Step 06b.11**: the measurement half, beside the four-point table.
- `docs/manual/06-z-axis-and-gantry-squaring.md` — **Step 06b.14**: the de-racking half.

**Drawn schematically / left unlabelled (verify)**

- The racked view is deliberately exaggerated; real racking is a fraction of a millimetre. The skew shown is not a measurement.

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

- Every row of 00-index.md's timeline in execution order on two lanes — print batches B00–B10 on the Core One+, assembly chapters (including Ch 00a, the two-part Ch 06/06b, Ch 11 A/B and Ch 12 1/2) on the bench — with each row's duration and KIT / 2P marker.
- One orange rail per print batch through the middle channel, forking to every chapter whose `needs:` list names that batch.
- The Gen 2 belt-upgrade pause as a full-width band at its contingency position in the pre-kit block, between B07 and B08.
- The critical-path strip: print hours (per batch and total) from docs/manual/print/README.md, the rest from 00-index.md § Critical path.

**Insert at**

- `docs/manual/00-index.md` — **The timeline**: at the head of the section, above the row list — this is the only diagram that belongs in the index rather than in a chapter step.

**Drawn schematically / left unlabelled (verify)**

- Nothing on this diagram is authored here. The rows, their order, their durations, their markers and their dependency arrows are parsed out of 00-index.md's timeline (via build_tonight.py's own row parser, so the picture and the Tonight planner always walk the same list); the hours come from print/README.md and the footer figures from 00-index.md § Critical path. Edit the index, then re-run this script.
- The vertical axis is execution order, not calendar time. The manual's timeline is dependency-ordered and gives no per-row calendar date, so none is invented here.

---

## Markdown to paste in

Diagrams sit in the step's image block, in the same position a manual page image would take:

```markdown
![The six A/B bearing stacks](assets/diagrams/01-ab-bearing-stacks.svg)
```

From `00-index.md` the path is the same; from a print-batch chapter under `docs/manual/print/` it is `../assets/diagrams/…`.

## Regenerating

```
python3 scripts/draw_diagrams.py            # all eleven + this file
python3 scripts/draw_diagrams.py --only 3 7 # just those two
```

The script has no third-party dependencies — it emits SVG strings directly. To check a render: `rsvg-convert -w 1200 -o /tmp/x.png docs/manual/assets/diagrams/03-corexy-belt-path.svg`.
