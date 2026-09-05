# Chapter 04 — A/B drive units and front idlers

Builds the four CoreXY sub-assemblies that carry the A and B belts — two motor-carrying drive units and two front idlers with their tension arms. Unlocks Ch 05 (gantry), which bolts all four onto the Y extrusions.

**Time:** 3.5–5.0 h hands-on, first build ([survey §5.1 P04](../voron-build-instructions-survey.md)).

**Prerequisites:**
- **Ch 01 — Frame.** Nothing from Ch 02 or Ch 03 is needed; this is bench work and can run in parallel with them (survey §5.1: P04 ← P01).
- **Print batch B03** — *A/B drive units + front idlers*, 2 plates, 7.7 h, 130 g black ([print plan](../voron-print-plan.md)). B03's plate captions were corrected 2026-09-05 to pair `front_idler_right_*` with the A drive and `front_idler_left_*` with B — see Step 04.2. Both plates print all eight frames either way.
- **Print batch B02** — *the orange day*, plate **B02-P2**, for `[a]_tensioner_left` and `[a]_tensioner_right`.
- **Print batch B00** — for `pulley_jig.stl`. Without it you are setting two different pulley heights with calipers.

**Tools**
- Hex drivers 2 mm, 2.5 mm, 3 mm, 4 mm — a 2.5 mm ball-end helps at the M3×40 and the set screws
- Temperature-controlled soldering iron + LDO brass M3 insert tip (4 heat-set inserts, Steps 04.3–04.4)
- Printed `pulley_jig.stl` (Voron-2 `STLs/Tools/`)
- Digital caliper — pulley height fallback, and to confirm both drives match
- A 60 mm offcut of 6 mm 2GT belt, or a thin steel rule — the belt-path straightness check
- Tweezers or a small screwdriver to place spacers into the stacks without dropping them
- Masking tape + marker — label every assembly **A** or **B** as it is finished

**Consumables:** Loctite 243 (blue), for the pulley set screws if they are not already pre-applied.

**Printed parts**

| STL | Qty | Colour |
|---|---|---|
| `a_drive_frame_upper.stl` | 1 | Black |
| `a_drive_frame_lower.stl` | 1 | Black |
| `b_drive_frame_upper.stl` | 1 | Black |
| `b_drive_frame_lower.stl` | 1 | Black |
| `front_idler_right_lower.stl` | 1 | Black |
| `front_idler_right_upper.stl` | 1 | Black |
| `front_idler_left_lower.stl` | 1 | Black |
| `front_idler_left_upper.stl` | 1 | Black |
| `[a]_tensioner_right.stl` | 1 | Orange |
| `[a]_tensioner_left.stl` | 1 | Orange |

All ten are in Voron-2 `STLs/Gantry/AB_Drive_Units/` and `STLs/Gantry/Front_Idlers/`. Two more parts sit in those same folders and are **not** used here: `[a]_cable_cover` (Ch 07) and `[a]_z_chain_retainer_bracket_x2` (Ch 06). Keep them bagged.

**Hardware** (chapter totals)

| Fastener / part | Qty | Where |
|---|---|---|
| Stepper motor, **0.9°**, `LDO-42STH48-2004MAH(VRN)` | 2 | one per drive (p.75, p.79) |
| GT2 pulley, 20 T, 5 mm bore, **6 mm wide** (`Pulley, 2GT, 20T, 5mm ID 6mm W`) | 2 | one per motor shaft (p.75, p.79). The kit has exactly two; the four **9 mm** 20T pulleys are the Z-drive pulleys used in Ch 02 |
| F695 flanged bearing (5×13×4 mm) | 16 | 6 per drive (p.74, p.78) + 2 per front idler (p.65, p.69). The A/B side uses **F695 only** — 625-2RS is the Z-drive bearing (Ch 02) |
| **M5 precision spacer, brass** — the manual's "M5 shim" | 16 | one above and one below every bearing pair |
| M5×30 BHCS | 4 | 2 per drive, upper frame → lower frame (p.73, p.77) |
| M5×40 SHCS | 2 | 1 per front idler — first as the assembly aid, then fitted from the top (p.65–66, p.69–70) |
| M3×30 SHCS | 6 | 3 per motor (p.76, p.80) |
| M3×40 SHCS | 2 | 1 per front idler tension arm (p.67, p.71) |
| M3 washer | 2 | under each M3×40 head (p.67, p.71) |
| Heat-set insert, brass, M3×5×4 | 4 | 2 in `a_drive_frame_upper`, 1 in each tension arm (p.64) |
| M5 hex nut | 2 | 1 in each tension arm foot (p.64) |

**Read first**
- **A and B parts are mirrored and swap silently.** The A drive's printed frames carry a **cutout** the B frames do not have (p.73, circled). Only `a_drive_frame_upper` has the two heat-set insert bosses — `b_drive_frame_upper` has none. Build one complete assembly at a time; never have both sets of frames loose on the bench together.
- **Where each assembly ends up, standing in front of the printer: A = rear right, B = rear left.** The official manual never says this; the LDO wiring guide does, and the LDO Klipper config repeats it (`## B Stepper - Left`, `## A Stepper - Right`). It follows that the A idler is the **front right** pair and the B idler the **front left** pair. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d)
- **The bearing stacks are the mistake everyone makes.** Every F695 pair goes **flange-out** — the two plain faces touch, the two flanges face away from each other — with one spacer above the pair and one below. The drive's far post takes **two** such pairs (4 bearings, 4 spacers); the near post and each front idler take **one** (2 bearings, 2 spacers).
- **The A and B pulleys sit at different heights and face opposite ways**: A is hub-down at 16.5 mm (p.75), B is hub-up at 6.5 mm (p.79). That difference is what stacks the two belt planes. No amount of belt tension in Ch 07 will fix it if you set them the same.
- **LDO's Build Notes have no entry for p.62–81.** The only kit deviation in this whole chapter is the standing substitution from their p.19 note: brass M5 precision spacer everywhere the manual writes "M5 shim". [src](https://docs.ldomotors.com/en/voron/voron2/build-faq)

---

### Step 04.1 — Lay the chapter out as four separate kits

![Voron manual p.62](assets/manual-pages/manual-p062.png)

**Parts:** all ten printed parts; four trays or bags.

**Do:** Split the bench into four labelled areas: **A DRIVE**, **B DRIVE**, **A IDLER**, **B IDLER**. Put `a_drive_frame_upper` + `a_drive_frame_lower` in the first, `b_drive_frame_*` in the second, `front_idler_right_*` + `[a]_tensioner_right` in the third, `front_idler_left_*` + `[a]_tensioner_left` in the fourth. Only open one area at a time.

**Check:** Ten printed parts placed, none left over. If you have an eleventh, it is `[a]_cable_cover` or a `[a]_z_chain_retainer_bracket` — bag those for Ch 07 and Ch 06.

---

### Step 04.2 — Fix which assembly is A and which is B

![Voron manual p.63](assets/manual-pages/manual-p063.png)

**Parts:** masking tape, marker.

**Do:** Write the destination on every part now, before anything is assembled: `a_drive_*` → **rear right**; `b_drive_*` → **rear left**; `front_idler_right_*` + `[a]_tensioner_right` → **front right**; `front_idler_left_*` + `[a]_tensioner_left` → **front left**. All four positions are as seen standing in front of an upright printer.

**Check:** Confirm the idler pairing by height — the two idler assemblies are not mirror images, they are handed by belt plane. `front_idler_right_lower` is **21.6 mm** tall and `front_idler_right_upper` 12.0 mm; `front_idler_left_lower` is **11.6 mm** and `front_idler_left_upper` 21.6 mm. The 10.0 mm difference between the two lower frames is exactly the 10 mm between the A and B pulley heights (16.5 mm vs 6.5 mm, p.75/p.79) — the A belt runs in the upper plane, so the **right** (A) idler carries its bearings high and the **left** (B) idler low. Caliper the two lower frames: the tall one is the A idler's, and it goes to the front right.

⚠ Rev D+ / LDO: the motor identity comes from the wiring guide, not the manual: **A = rear right → HV-STEPPER-1**, **B = rear left → HV-STEPPER-0**. Get this backwards and the machine moves diagonally on a straight-line jog. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d)

---

### Step 04.3 — Heat-set the two inserts in `a_drive_frame_upper`

![Voron manual p.64](assets/manual-pages/manual-p064.png)

**Parts:** 2× M3×5×4 brass heat-set insert; `a_drive_frame_upper`.

**Do:** Find the two blind 4.7 mm bosses on the flat face of `a_drive_frame_upper`, one either side of the motor bore, ~56 mm apart. Set the iron to your ABS insert temperature, hold the part flat, and press each insert straight down until its top is flush with the surface. Let the plastic cool before touching the part.

**Check:** Both inserts flush and square — a tilted insert will not accept the screw in Ch 07. `b_drive_frame_upper` takes **no** inserts; if you find bosses on it you have picked up the A frame.

Tip: if your print batch already ran its insert pass ([survey §4.4 #4](../voron-build-instructions-survey.md)), just confirm the two are present and skip ahead.

---

### Step 04.4 — Heat-set one insert into each tension arm

![Voron manual p.64](assets/manual-pages/manual-p064.png)

**Parts:** 2× M3×5×4 brass heat-set insert; `[a]_tensioner_left`, `[a]_tensioner_right`.

**Do:** Each tension arm has one through-bore that steps from 3.5 mm to 4.7 mm. Press the insert into the **4.7 mm end** — the wider opening. The 3.5 mm section is the M3×40's clearance and must stay clear.

**Check:** Push an M3×40 SHCS through the small end by hand — it should pass freely down the 3.5 mm bore and pick up thread only when it reaches the insert. If it binds early, the insert went in the wrong end or sits crooked.

---

### Step 04.5 — Press an M5 nut into each tension arm foot

![Voron manual p.64](assets/manual-pages/manual-p064.png)

**Parts:** 2× M5 hex nut; both tension arms.

**Do:** Drop an M5 nut into the hex pocket in the underside of each arm's foot. Seat it fully with a flat driver — the nut must sit below the face, not proud of it.

**Check:** The nut does not rock in its pocket and does not stand above the foot. Nothing holds it in yet; keep the arms flat until Step 04.9.

---

### Step 04.6 — A idler: stand the assembly-aid bolt in the lower frame

![Voron manual p.65](assets/manual-pages/manual-p065.png)

**Parts:** `front_idler_right_lower`; 1× M5×40 SHCS.

**Do:** Lay `front_idler_right_lower` flat with its idler boss facing up. Push the M5×40 SHCS up through the boss from underneath so the thread stands vertically. This bolt is only a stack alignment aid at this stage and comes out again at Step 04.9.

**Check:** The bolt stands square to the frame and the head sits fully home underneath. If it leans, the stack will not seat.

---

### Step 04.7 — A idler: build the bearing stack

![Voron manual p.65](assets/manual-pages/manual-p065.png)

**Parts:** 2× M5 precision spacer; 2× F695 bearing.

**Do:** Thread onto the standing bolt, **bottom to top**: (1) M5 precision spacer; (2) F695 bearing, **flange down**; (3) F695 bearing, **flange up**; (4) M5 precision spacer. The two bearings meet plain face to plain face, so their flanges point away from each other and form the belt channel.

**Check:** Sight the stack from the side — you see spacer, flange, plain, plain, flange, spacer. If you can see a flange in the middle of the stack, one bearing is reversed; strip it and rebuild. Spin the pair: both bearings must turn freely and independently.

⚠ Rev D+ / LDO: the manual's "M5 Shim" is the brass **M5 precision spacer** in this kit — one per callout, never two stacked to make up height. [src](https://docs.ldomotors.com/en/voron/voron2/build-faq)

---

### Step 04.8 — A idler: cap the stack with the upper frame

![Voron manual p.65](assets/manual-pages/manual-p065.png)

**Parts:** `front_idler_right_upper` (the 12.0 mm-tall one).

**Do:** Lower `front_idler_right_upper` over the stack so its nose captures the top spacer and the two frames meet along their mating faces.

**Check:** The two frames sit tight together with no gap and no rock. A visible gap means a spacer is out of place or a bearing is not centred on the bolt.

---

### Step 04.9 — A idler: pull the aid bolt and slide in the tension arm

![Voron manual p.66](assets/manual-pages/manual-p066.png)

**Parts:** `[a]_tensioner_right` (with its insert and M5 nut already fitted).

**Do:** Hold the two frames together, withdraw the M5×40 SHCS downwards, and slide `[a]_tensioner_right` into the channel between the frames until its top boss lines up with the hole in the upper frame. Keep the assembly pinched together while you do it — the bearing stack is unsupported for these few seconds.

**Check:** The arm sits flat in the channel and its top boss is concentric with the frame's top hole. The wrong-hand arm will not sit flat — if it fights you, you have `[a]_tensioner_left`.

---

### Step 04.10 — A idler: refit the M5×40 SHCS from the top

![Voron manual p.66](assets/manual-pages/manual-p066.png)

**Parts:** the same 1× M5×40 SHCS.

**Do:** Drop the M5×40 SHCS in from the **top** of the assembly and run it down by hand until it just picks up the M5 nut in the tension arm's foot. Stop there.

**Check:** The bolt starts by hand for its full travel — no forcing. Leave it barely engaged: this is the belt tensioner and it is set with the belt on in Ch 07 (p.124–145). Preloading it now only makes Ch 07 harder.

---

### Step 04.11 — A idler: fit the M3 washer and M3×40 SHCS

![Voron manual p.67](assets/manual-pages/manual-p067.png)

**Parts:** 1× M3 washer; 1× M3×40 SHCS.

**Do:** Put the M3 washer under the head of the M3×40 SHCS, enter it horizontally through the side of the idler frame, and run it in until snug.

**Check:** Snug, not torqued (the manual specifies no value). The washer is captive under the head and the head sits flat on the frame's side face.

---

### Step 04.12 — A idler: check your work

![Voron manual p.68](assets/manual-pages/manual-p068.png)

**Parts:** none.

**Do:** Compare your assembly against the four circled features on p.68: the M5×40 head recessed in the top boss; the ribbed face of the upper frame; the exposed bearing pair with a flange top and bottom; the M3×40 head with its washer in the side of the arm. Then set it in the **A IDLER** tray.

**Check:** All four features match the page. Spin the bearing pair once more with a fingertip — it must run free with the frames closed.

---

### Step 04.13 — B idler: stand the assembly-aid bolt in the lower frame

![Voron manual p.69](assets/manual-pages/manual-p069.png)

**Parts:** `front_idler_left_lower` (the 11.6 mm-tall one); 1× M5×40 SHCS.

**Do:** Lay `front_idler_left_lower` flat with its idler boss up and push the M5×40 SHCS up through it from underneath. The B idler's boss is lower than the A idler's — that is correct, it carries the lower belt plane.

**Check:** Bolt vertical, head home. If the boss looks tall like the last one, you have the A idler's lower frame.

---

### Step 04.14 — B idler: build the bearing stack

![Voron manual p.69](assets/manual-pages/manual-p069.png)

**Parts:** 2× M5 precision spacer; 2× F695 bearing.

**Do:** Bottom to top: M5 precision spacer, F695 **flange down**, F695 **flange up**, M5 precision spacer. Identical to the A idler.

**Check:** No flange visible in the middle of the stack; both bearings spin free.

⚠ Rev D+ / LDO: brass **M5 precision spacer** in place of the manual's "M5 shim". [src](https://docs.ldomotors.com/en/voron/voron2/build-faq)

---

### Step 04.15 — B idler: cap the stack with the upper frame

![Voron manual p.69](assets/manual-pages/manual-p069.png)

**Parts:** `front_idler_left_upper` (the tall 21.6 mm one).

**Do:** Lower `front_idler_left_upper` over the stack until the two frames meet.

**Check:** Frames flush, no gap, no rock.

---

### Step 04.16 — B idler: pull the aid bolt and slide in the tension arm

![Voron manual p.70](assets/manual-pages/manual-p070.png)

**Parts:** `[a]_tensioner_left`.

**Do:** Pinch the frames together, withdraw the M5×40 SHCS downwards, and slide `[a]_tensioner_left` into the channel until its top boss lines up with the frame's top hole.

**Check:** The arm lies flat in the channel; its boss is concentric with the hole above it.

---

### Step 04.17 — B idler: refit the M5×40 SHCS from the top

![Voron manual p.70](assets/manual-pages/manual-p070.png)

**Parts:** the same 1× M5×40 SHCS.

**Do:** Drop it in from the top and run it down by hand until it just engages the M5 nut in the arm's foot.

**Check:** Hand-tight only. Tensioning happens in Ch 07.

---

### Step 04.18 — B idler: fit the M3 washer and M3×40 SHCS

![Voron manual p.71](assets/manual-pages/manual-p071.png)

**Parts:** 1× M3 washer; 1× M3×40 SHCS.

**Do:** Washer under the head, in through the side of the frame, snug.

**Check:** Snug, not torqued (not specified — snug). Head flat, washer captive.

---

### Step 04.19 — B idler: check your work

![Voron manual p.72](assets/manual-pages/manual-p072.png)

**Parts:** none.

**Do:** Match the five circled features on p.72 — ribbed face, M5×40 head in the top boss, exposed bearing pair, M3×40 head with washer, and the slot in the lower frame. Set it in the **B IDLER** tray.

**Check:** All five match, bearings free. Hold the two idlers side by side: their bearing pairs must sit at visibly different heights. If they look the same, you built two of the same hand.

---

### Step 04.20 — A drive: upper frame face down, two M5×30 BHCS

![Voron manual p.73](assets/manual-pages/manual-p073.png)

**Parts:** `a_drive_frame_upper`; 2× M5×30 BHCS.

**Do:** The manual builds both drives **upside down**: lay `a_drive_frame_upper` on the bench with its heat-set inserts facing **down** against the bench, so the two bearing posts point up at you. Drop an M5×30 BHCS through each of the two 5.4 mm holes (37 mm apart, either side of the motor bore) so the threads stand vertically.

**Check:** This is an A part — it has the **cutout** circled on p.73 and the two heat-set inserts fitted at Step 04.3. Both bolts stand square, heads fully home in the plate.

---

### Step 04.21 — A drive: two-bearing stack on the near post

![Voron manual p.74](assets/manual-pages/manual-p074.png)

**Parts:** 2× M5 precision spacer; 2× F695 bearing.

**Do:** Work on the post **nearer the motor bore** (drawn on the left on p.74). Bottom to top: M5 precision spacer, F695 **flange down**, F695 **flange up**, M5 precision spacer.

**Check:** One pair, flanges out, one spacer each end — four items, 10 mm of stack. If you have loaded four bearings here, you are on the wrong post.

⚠ Rev D+ / LDO: brass **M5 precision spacer** in place of the manual's "M5 shim". [src](https://docs.ldomotors.com/en/voron/voron2/build-faq)

---

### Step 04.22 — A drive: four-bearing stack on the far post

![Voron manual p.74](assets/manual-pages/manual-p074.png)

**Parts:** 4× M5 precision spacer; 4× F695 bearing.

**Do:** Work on the post **farther from the motor bore** (drawn on the right on p.74). Load two complete pairs, bottom to top: spacer, F695 **flange down**, F695 **flange up**, spacer, spacer, F695 **flange down**, F695 **flange up**, spacer. Note the two spacers that meet in the middle — one closes the lower pair, one opens the upper pair.

**Check:** Eight items, 20 mm of stack, and exactly **two** spacers touching in the middle. Read the stack from the side: spacer, flange, plain, plain, flange, spacer, spacer, flange, plain, plain, flange, spacer. This post carries both belt planes and is the single most-often mis-stacked assembly in the build.

⚠ Rev D+ / LDO: all four "M5 shims" here are brass **M5 precision spacers**. [src](https://docs.ldomotors.com/en/voron/voron2/build-faq)

---

### Step 04.23 — A drive: close it with `a_drive_frame_lower`

![Voron manual p.74](assets/manual-pages/manual-p074.png)

**Parts:** `a_drive_frame_lower`.

**Do:** Lower `a_drive_frame_lower` onto both stacks, aligning the two M5×30 threads with their blind holes, and run both bolts down alternately a couple of turns at a time until the frames meet.

**Check:** **Do not over-tighten — the M5 bolts thread directly into plastic** (p.74). Stop the moment the frames are closed and the bolt stops turning easily. Both bearing pairs must still spin free with the frames closed; if either is pinched, back the bolts off and check the stack order.

---

### Step 04.24 — A drive: set the pulley on the A motor at 16.5 mm

![Voron manual p.75](assets/manual-pages/manual-p075.png)

**Parts:** 1× stepper motor (0.9° A/B motor); 1× GT2 20 T **6 mm** pulley; printed `pulley_jig.stl`.

**Do:** Slide the pulley onto the shaft **hub first — teeth up**. Sit the pulley jig flat on the motor's front face and rest the underside of the pulley's toothed section on the jig step marked **A**. That sets 16.5 mm from the motor face to the underside of the teeth (p.75). Without the jig, set 16.5 mm with a caliper.

**Check:** 16.5 mm, teeth up, hub down against the shaft. Compare against p.75's elevation before you lock anything.

⚠ Rev D+ / LDO: the two A/B motors are **0.9°** (`LDO-42STH48-2004MAH(VRN)`); the four Z motors are 1.8° and look identical. Take an A/B motor, not a spare Z motor. This is why the LDO config carries `full_steps_per_rotation: 400` in `[stepper_x]` and `[stepper_y]` — you will set it in Ch 12, and it is the only place in the build the difference shows up. [src](https://github.com/MotorDynamicsLab/LDOVoron2/blob/main/Firmware/leviathan-printer-rev-d-sbv2.cfg)

---

### Step 04.25 — A drive: threadlock and lock the pulley set screws

![Voron manual p.75](assets/manual-pages/manual-p075.png)

**Parts:** 2× set screw (in the pulley); Loctite 243.

**Do:** Back both set screws out, put a drop of Loctite 243 on each, and refit. Rotate the shaft so the first set screw lands on the machined flat, if the shaft has one; tighten that one first, then the second. Recheck the height with the jig — set screws pull a pulley sideways as they bite.

**Check:** The pulley will not twist or slide on the shaft under firm hand pressure, and it still reads 16.5 mm. If the set screws already carry a dry blue patch, that is pre-applied threadlocker — do not add more.

---

### Step 04.26 — A drive: offer the motor up with the cable exit inboard

![Voron manual p.75](assets/manual-pages/manual-p075.png)

**Parts:** the A motor with its pulley.

**Do:** Turn the drive assembly the right way up (motor below the frames) and offer the motor up into the frame with the **cable exit facing inboard** — toward where the B drive will sit, i.e. toward the middle of the rear extrusion. The manual's rule: *"the wires from the motors will be pointing towards each other once fully assembled"* (p.75).

**Check:** With A at the rear right, the A motor's cable exits toward the machine's centreline, not out toward the right skirt. Getting this wrong is a full teardown of the drive once the gantry is in.

---

### Step 04.27 — A drive: three M3×30 SHCS through the frames into the motor

![Voron manual p.76](assets/manual-pages/manual-p076.png)

**Parts:** 3× M3×30 SHCS.

**Do:** Line the motor's mounting holes up with the three clearance holes around the bore and run all three M3×30 SHCS down through both frames into the motor. Start all three by hand before tightening any, then tighten evenly.

**Check:** Three bolts, not four — the fourth motor hole is not used (p.76). All three pulled down evenly with the motor face flat against the frame.

---

### Step 04.28 — A drive: check your work and the belt path

![Voron manual p.76](assets/manual-pages/manual-p076.png)

**Parts:** a 6 mm belt offcut or a thin steel rule.

**Do:** Compare against p.76's elevation — the manual asks you to *"pay attention to the pulley orientation and alignment with the bearing stack ups"*. Lay the belt offcut flat across the pulley teeth and then across each bearing pair in turn, following the path the belt will take.

**Check:** **The belt path must be straight.** The offcut lies flat on the pulley and in each bearing groove without tilting, riding up a flange, or needing to twist. Any step in height here becomes belt whine and edge wear that Ch 07 tension cannot cure. Then label the assembly **A — REAR RIGHT** and set it aside.

---

### Step 04.29 — B drive: upper frame face down, two M5×30 BHCS

![Voron manual p.77](assets/manual-pages/manual-p077.png)

**Parts:** `b_drive_frame_upper`; 2× M5×30 BHCS.

**Do:** Lay `b_drive_frame_upper` on the bench, the same upside-down way as the A drive, so the two bearing posts point up. Drop an M5×30 BHCS through each of the two 5.4 mm holes.

**Check:** This is a B part — **no cutout** and **no heat-set inserts**. If you can see either, you have picked up the A frame.

---

### Step 04.30 — B drive: four-bearing stack on the far post

![Voron manual p.78](assets/manual-pages/manual-p078.png)

**Parts:** 4× M5 precision spacer; 4× F695 bearing.

**Do:** Work on the post **farther from the motor bore** — because the B frame is the mirror of the A frame, p.78 draws it on the **left**, where p.74 drew it on the right. Load two pairs: spacer, F695 **flange down**, F695 **flange up**, spacer, spacer, F695 **flange down**, F695 **flange up**, spacer.

**Check:** Eight items, two spacers meeting in the middle, no flange face-to-face anywhere. Same 20 mm stack as the A drive.

⚠ Rev D+ / LDO: brass **M5 precision spacers**, not shims. [src](https://docs.ldomotors.com/en/voron/voron2/build-faq)

---

### Step 04.31 — B drive: two-bearing stack on the near post

![Voron manual p.78](assets/manual-pages/manual-p078.png)

**Parts:** 2× M5 precision spacer; 2× F695 bearing.

**Do:** On the post nearer the motor bore (drawn on the right on p.78): spacer, F695 **flange down**, F695 **flange up**, spacer.

**Check:** Four items, 10 mm. Both drives now hold six bearings and six spacers each — count them before closing.

⚠ Rev D+ / LDO: brass **M5 precision spacers**, not shims — the last two of the sixteen this chapter uses. [src](https://docs.ldomotors.com/en/voron/voron2/build-faq)

---

### Step 04.32 — B drive: close it with `b_drive_frame_lower`

![Voron manual p.78](assets/manual-pages/manual-p078.png)

**Parts:** `b_drive_frame_lower`.

**Do:** Lower `b_drive_frame_lower` onto both stacks and run the two M5×30 BHCS down alternately until the frames meet.

**Check:** **Do not over-tighten — these bolts thread straight into plastic** (p.78). Both bearing pairs spin free with the frames closed.

---

### Step 04.33 — B drive: set the pulley on the B motor at 6.5 mm — flipped

![Voron manual p.79](assets/manual-pages/manual-p079.png)

**Parts:** 1× stepper motor (0.9° A/B motor); 1× GT2 20 T **6 mm** pulley; `pulley_jig.stl`.

**Do:** Slide the pulley onto the shaft **the other way up from the A drive — teeth first, hub up**, so the shaft end pokes through the top of the hub. Sit the jig on the motor face and rest the pulley's lower flange on the step marked **B**: 6.5 mm from the motor face to the underside of the teeth (p.79).

**Check:** 6.5 mm and hub **up**. Stand the two motors side by side — the A pulley sits high with its teeth on top, the B pulley sits low with its hub on top. If both look the same, one is wrong.

---

### Step 04.34 — B drive: threadlock and lock the pulley set screws

![Voron manual p.79](assets/manual-pages/manual-p079.png)

**Parts:** 2× set screw (in the pulley); Loctite 243.

**Do:** Loctite 243 on both set screws, first one onto the shaft flat if there is one, then the second. Re-measure with the jig after tightening.

**Check:** No slip under hand pressure; still 6.5 mm.

---

### Step 04.35 — B drive: offer the motor up with the cable exit inboard

![Voron manual p.79](assets/manual-pages/manual-p079.png)

**Parts:** the B motor with its pulley.

**Do:** Turn the assembly the right way up and fit the motor with the **cable exit facing inboard** (p.79, circled) — mirrored from the A drive, so with B at the rear left its cable also runs toward the machine's centreline.

**Check:** Hold both drives in their build positions: the two cable exits face each other. That is the manual's own test (p.75).

---

### Step 04.36 — B drive: three M3×30 SHCS through the frames into the motor

![Voron manual p.80](assets/manual-pages/manual-p080.png)

**Parts:** 3× M3×30 SHCS.

**Do:** Start all three by hand through both frames into the motor, then tighten evenly.

**Check:** Three bolts, motor face flat against the frame, nothing cross-threaded.

---

### Step 04.37 — B drive: check your work and the belt path

![Voron manual p.80](assets/manual-pages/manual-p080.png)

**Parts:** the belt offcut or steel rule.

**Do:** Compare against p.80's elevation and run the offcut across the pulley and each bearing pair as you did for the A drive.

**Check:** **The belt path must be straight** — offcut flat on the pulley and in both grooves, no tilt, no flange contact. Label the assembly **B — REAR LEFT**.

---

### Step 04.38 — Bag, label and hand off to Ch 05

![Voron manual p.81](assets/manual-pages/manual-p081.png)

**Parts:** four finished assemblies; four bags; marker.

**Do:** Bag each assembly separately with its destination written on the bag: **A drive — rear right**, **B drive — rear left**, **A idler — front right**, **B idler — front left**. Photograph all four together for the build log. Manual p.81 is a filler page and carries no assembly step.

**Check:** Four bags, four labels, no loose bearings or spacers left on the bench. Leftover F695s or spacers mean a stack is short — find it now, not after the gantry is bolted up.

---

## Checkpoint 04

- [ ] Two drive units and two front idlers built, each labelled with its position on the machine.
- [ ] Every F695 pair is flange-out — plain faces touching — with one brass M5 precision spacer above and below each pair.
- [ ] Drive far posts: 4 bearings + 4 spacers, with two spacers meeting mid-stack. Drive near posts and both idlers: 2 bearings + 2 spacers.
- [ ] All six bearing groups spin free with the frames closed and bolted.
- [ ] `a_drive_frame_upper` has its two heat-set inserts; `b_drive_frame_upper` has none.
- [ ] Both motor pulleys are the **6 mm-wide** 20T (`5mm ID 6mm W`), not one of the four 9 mm Z-drive pulleys.
- [ ] A pulley: hub down, 16.5 mm. B pulley: hub up, 6.5 mm. The two are visibly different.
- [ ] Both pulleys are threadlocked and will not slip under hand pressure.
- [ ] The belt offcut lies flat across pulley and bearing grooves on both drives — no tilt, no flange contact.
- [ ] Both motor cable exits point inboard; held in their build positions, they face each other.
- [ ] Every M5×30 BHCS is snug only — none was torqued down into the plastic thread.
- [ ] Zero bearings, spacers or fasteners left over.
- [ ] Photos taken of all four assemblies before bagging.

## Common mistakes

- **A bearing pair fitted flange-to-flange (or flange-in).** The belt then rides on a flange edge instead of the bearing races and shreds. Fix: open the stack, turn the two bearings so their plain faces meet. Check by sighting the stack edge-on — a flange in the middle is always wrong.
- **Four bearings on the near post, two on the far post.** The frames will not close square, or they close and pinch a bearing. Fix: the four-bearing stack always goes on the post farther from the motor bore — right on p.74, left on p.78.
- **Fitting a 9 mm 20T pulley on an A/B motor.** It looks like the right pulley but it is a Z-drive part, and it will not sit in the 6 mm belt plane that a flange-out F695 pair forms. The kit ships exactly two 6 mm 20T pulleys and four 9 mm ones — count them before you start, and keep the 9 mm four with the Ch 02 Z bin.
- **Both pulleys set to the same height, or the B pulley fitted hub-down.** The A and B belts then try to share one plane and rub. This is not fixable at belting time. Fix: A = 16.5 mm hub down, B = 6.5 mm hub up, both re-checked with the jig after the set screws are tight.
- **Motor cable exits pointing outboard.** The cables will not reach the drag chain and the drive has to come apart with the gantry in the machine. Fix: check before the three M3×30 go in — the exits face each other.
- **M5×30 BHCS torqued down.** They thread into plastic (p.74, p.78) and strip permanently; a stripped post means reprinting a drive frame. Fix: stop at closed-and-snug.
- **A parts and B parts swapped.** The A frames have a cutout and `a_drive_frame_upper` has two heat-set inserts; the B frames have neither. On the idlers, the tall lower frame is the A (right) idler.

## Next

**Ch 05 — Gantry: X and Y axes, XY joints, X carriage, titanium backers.** The four assemblies you just built bolt onto the Y extrusions there (manual p.82–107); print batch **B04** must be done before you start it.
