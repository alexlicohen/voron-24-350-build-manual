# Chapter 05 — Gantry: X and Y axes, XY joints, X carriage, titanium backers

Builds the complete gantry on the bench — XY bridge, both Y axes with their MGN9 rails, both XY joints, the X extrusion with its MGN12 rail, and the titanium extrusion backers — and ends with the X axis riding on the Y carriages. Unlocks Ch 06 (gantry install, Z belts, squaring).

**What you're building in this chapter.** The gantry is the entire moving upper half of the printer — a rectangle of aluminium extrusion that later hangs on four belts and slides up and down, with the toolhead riding inside it. Its back edge is the **XY bridge**, the cross-beam that carries the A and B motors you built in Ch 04. Two side extrusions, the **Y axes**, run forward from that bridge; each has a linear rail along one face and a **front idler** block at its front end that turns its belt back. Spanning the two sides is the **X beam**, capped at each end by an **XY joint** — the printed blocks that ride on the Y carriages and turn each belt around from its Y run to its X run. Bolted to the face opposite every rail are the **titanium backers**, flat strips that stop a steel rail bowing its aluminium extrusion as the chamber heats. Nothing in this chapter gets belts or squaring: both belong to Ch 06/07, and both would undo work done here.

**Time:** 5.0–7.0 h hands-on, first build, two people ([survey §5.1 P05 / §7.2](../voron-build-instructions-survey.md)).

**Sessions:** 12 × ~30 min (first-build estimate; each `Pause:` line carries its own segment minutes).

**Prerequisites:**

- **Ch 04** — A drive, B drive and both front idler assemblies built and checked (manual p.62–81). This chapter consumes them whole.
- **Ch 00** — all seven rails cleaned and packed with grease *before* they go on an extrusion ([LDO rail grease guide](https://docs.ldomotors.com/guides/rail_grease_guide)); jigs `Tools/MGN9_rail_guide_x2.stl` and `Tools/MGN12_rail_guide_x2.stl` printed (batch **B00**).
- **Print batches: B04** (XY joints + X carriage, plate B04-P1, 7.3 h, black) and **B02-P3** (the orange accent plate — cable bridge and endstop pod) ([print plan §B04](../voron-print-plan.md)). B04 is itself gated on B00 + B02 + B03.
- **Titanium backer set** (Fabreeko/LDO, 350 size) unpacked and counted.
- Ch 01's bagged **C ×2, D ×1, E ×1** extrusions.

**Tools**

- Hex drivers 2 / 2.5 / 3 / 4 mm; a **ball-end 2.5 mm** helps at the XY joints
- **T10 Torx driver** — strongly preferred for the backer M3 FHCS; hex cams out of a countersink easily ([backers README](https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers))
- Printed rail-centring jigs `MGN9_rail_guide_x2`, `MGN12_rail_guide_x2`
- Steel rule 300 mm and a caliper — to equalise the rail overhang at both ends
- Masking tape (carriage retention) and the kit's rubber rail stoppers
- 2.5 mm flat screwdriver (cable-chain latches, if you dry-fit the chain end)
- Camera for the build log

**Printed parts**

| Looks like | STL | Qty | Colour |
|---|---|---|---|
| ![](assets/parts/xy_joint_left_lower_MGN12.png){ width=96 } | `xy_joint_left_lower_MGN12.stl` | 1 | Black |
| ![](assets/parts/xy_joint_left_upper_MGN12.png){ width=96 } | `xy_joint_left_upper_MGN12.stl` | 1 | Black |
| ![](assets/parts/xy_joint_right_lower_MGN12.png){ width=96 } | `xy_joint_right_lower_MGN12.stl` | 1 | Black |
| ![](assets/parts/xy_joint_right_upper_MGN12.png){ width=96 } | `xy_joint_right_upper_MGN12.stl` | 1 | Black |
| ![](assets/parts/%5Ba%5D_xy_joint_cable_bridge_2hole.png){ width=96 } | `[a]_xy_joint_cable_bridge_2hole.stl` | 1 | Orange |
| ![](assets/parts/XY_cable_chain_bridge-Igus-3mm_backer.png){ width=96 } | `XY_cable_chain_bridge-Igus-3mm_backer.stl` | 1 (alternate — fit whichever clears the backer) | Orange |
| ![](assets/parts/x_frame_V2TR_MGN12_left.png){ width=96 } | `x_frame_V2TR_MGN12_left.stl` | 1 | Black — *staged here, fitted in Ch 07* |
| ![](assets/parts/x_frame_V2TR_MGN12_right.png){ width=96 } | `x_frame_V2TR_MGN12_right.stl` | 1 | Black — *staged here, fitted in Ch 07* |
| ![](assets/parts/probe_retainer_bracket.png){ width=96 } | `probe_retainer_bracket.stl` | 1 | Black — *staged here, fitted in Ch 07/08* |
| ![](assets/parts/%5Ba%5D_endstop_pod_D2F_switch.png){ width=96 } | `[a]_endstop_pod_D2F_switch.stl` | 1 | Orange — *staged here, fitted at endstop wiring* |

Do **not** print `[a]_endstop_pod_hall_effect.stl`, `[a]_xy_joint_cable_bridge_3hole.stl`, or any `xy_joint_*_MGN9` — wrong variants for this kit ([print plan §7](../voron-print-plan.md)).

**Hardware** (chapter totals)

| Fastener / part | Qty | Where |
|---|---|---|
| E extrusion (XY bridge) | 1 | p.85 |
| C extrusion (Y axis) | 2 | p.88 |
| D extrusion (X axis) | 1 | p.101 |
| MGN9H rail + carriage | 2 | Y axes, p.88 |
| MGN12H rail + carriage | 1 | X axis, p.101 |
| M5 roll-in T-nut | 26 | 8 in E (p.85), 12 in the C pair (p.89, p.90), 6 in D (p.102) |
| M3 roll-in T-nut | ≈32 | ≈20 Y rails (p.88 — ~10 per 400 mm MGN9), 4 in the C pair (p.90), ≈8 X rail (p.101) |
| M3 roll-in T-nut, backers | ~30 | not supplied with the backers — order separately |
| M5×10 BHCS | 10 | 8 bridge-to-drive (p.86–87), 2 left XY joint (p.104) |
| M5×16 BHCS | 10 | 4 front idlers (p.91, p.93), 4 rear drive joints (p.95), 2 right XY joint + cable bridge (p.104) |
| M5×30 BHCS | 2 | XY joints from below (p.104) |
| M5×40 SHCS | 8 | 4 per XY joint (p.97–100) |
| M3×8 SHCS | ≈28 | ≈20 Y rails (~10 each), ≈8 X rail — count the holes on your own rails |
| M3×16 SHCS | 8 (6 fitted + 2 reserved) | XY joints to the Y carriages (p.106); 2 held back for the endstop pod |
| M5 nut | 6 | 3 per XY joint (p.96) |
| **M5 precision spacer, brass** | 2 | XY joint bearing stacks (p.97, p.99) — replaces the manual's "M5 shim" |
| **M5 washer, black** | 2 | under the M5×30 heads (p.104) — replaces the manual's "M5 shim" |
| F695 bearing | 4 | 2 per XY joint |
| GT2 20-tooth idler | 2 | 1 per XY joint |
| Titanium backer, Y | 2 | one per C extrusion |
| Titanium backer, X | 1 | D extrusion, rear face |
| M3×8 FHCS (backers, Y) | ~20 | count the holes in your backers *(verify on bench)* |
| M3×6 FHCS (backers, X) | ~8 | count the holes in your backer *(verify on bench)* |

The West3D/Fabreeko titanium set ships **22× M3×8 FHCS and 10× M3×6 FHCS** with a few spares, and **no T-nuts** ([West3D](https://west3d.com/products/titanium-backers-for-voron-2-4-trident-3-pack)).

**Read first**

- **The titanium backers go on during this chapter, not after it.** Fitting them once the gantry is assembled or installed means a teardown (survey §5.2 W2). They mount on the face **opposite the rail** — top of the Y extrusions, rear of the X extrusion. *"If you have a single MGN12 but decide to put a backer on top, you will be actively contributing to the problem of bimetallic expansion!"* [src](https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers)
- **Do not tension the A/B belts and do not square the gantry here.** Both are Ch 06/07, and the official squaring procedure begins by *releasing* A/B tension — tension it now and you undo it (survey §4.4 #2, §5.2 W1). Several joints in this chapter are deliberately left "slightly loose".
- **Every T-nut this chapter needs must go in before the drive and idler frames cap the extrusion ends.** LDO: *"Due to the tight tolerances of the extrusions and roll-in t-nuts it is advisable to either test fit before assembly … or to pre-load the t-nuts into the extrusions."* [src](https://docs.ldomotors.com/en/voron/voron2/build-faq)
- **Rails ship dry.** If Ch 00's clean-and-pack pass has not been done, stop and do it — the flip-and-pack method needs access to the back of the rail (survey §4.4 #5).
- **Carriages slide off rails and are ruined by a drop** (manual p.88, p.101). Tape or stopper every carriage the moment its rail is on an extrusion.
- The gantry is assembled **upside down** through p.105 — that is a continuation of Ch 04's "UPSIDE DOWN ASSEMBLY" (manual p.74, p.78) — and is flipped at p.106.

**Sources for this chapter:**

- [Voron 2.4r2 assembly manual, p.82–107](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=82) — the page sequence this chapter transcribes, pinned at commit `de7e89d`
- [LDO Build Notes § Voron 2.4 build FAQ](https://docs.ldomotors.com/en/voron/voron2/build-faq) — Rev D kit deviations, T-nut pre-loading, rail stoppers
- [LDO printed-parts guide (Rev D)](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d) — 2-hole cable bridge, D2F endstop pod
- [LDO rail-grease guide](https://docs.ldomotors.com/guides/rail_grease_guide) — rail clean-and-pack, done in Ch 00
- [LDO cable-chain guide](https://docs.ldomotors.com/guides/cable_chain_guide) — chain-end clearance over the backers
- [Ti extrusion-backers README (tanaes)](https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers) — which face the backers go on, and why; source of the two backer images (GPL-3.0)
- [Fabreeko](https://www.fabreeko.com/products/v2-4-trident-titanium-extrusion-backers) and [West3D](https://west3d.com/products/titanium-backers-for-voron-2-4-trident-3-pack) backer sets — supplied screw counts
- [Voron docs § V2 Gantry Squaring](https://docs.vorondesign.com/build/mechanical/v2_gantry_squaring.html) — why nothing is squared or tensioned in this chapter

**Video coverage (Steve Builds, pre-release LDO kit — differs from Rev D+):** [Part 3 @0:56:34](https://www.youtube.com/watch?v=ii14-2COjuA&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=3394s) (+2m), [Part 3 @1:19:23](https://www.youtube.com/watch?v=ii14-2COjuA&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=4763s) (+16m), [Part 3 @1:34:36](https://www.youtube.com/watch?v=ii14-2COjuA&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=5676s) (+9m), [Part 3 @1:43:29](https://www.youtube.com/watch?v=ii14-2COjuA&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=6209s) (+5m), [Part 4 @0:06:16](https://www.youtube.com/watch?v=ViB5Ulc9zDI&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=376s) (+7m), [Part 4 @0:34:10](https://www.youtube.com/watch?v=ViB5Ulc9zDI&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=2050s) (+9m), [Part 5 @1:05:40](https://www.youtube.com/watch?v=hTKCBrk36R0&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=3940s) (+1m), [Part 5 @1:20:27](https://www.youtube.com/watch?v=hTKCBrk36R0&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=4827s) (+13m)

---

### Step 05.1 — Clear the bench and confirm the sub-assemblies

![Voron manual p.82](assets/manual-pages/manual-p082.png)

**What you're looking at:** The [gantry](16-glossary.md#g) is the moving frame above the bed that carries the toolhead — a rectangle of extrusions in which the X beam slides forward and back along two side rails. This page shows it finished, so you can see where the four Ch 04 sub-assemblies land: the A and B drives (motor, 20 T pulley and the bearing posts that turn the belt) at the two rear corners, the two front idler blocks at the front corners.

**Parts:** A drive, B drive, front idler left, front idler right (all from Ch 04); C extrusion ×2, D extrusion ×1, E extrusion ×1.

**Do:** Clear a bench at least 700 × 700 mm — the finished gantry is a 350's full footprint and you will rotate it repeatedly. Lay the four Ch 04 sub-assemblies out, drives at the top, idlers at the bottom, so left and right never get confused. Keep the A drive on the **right** and the B drive on the **left** as the overview draws them.

**Check:** Four Ch 04 assemblies present, pulleys and bearing stacks matching the p.80 "CHECK YOUR WORK" graphic, all four spinning freely.

Source: [Voron manual p.82](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=82) · [Video: Part 4 @0:06:30](https://www.youtube.com/watch?v=ViB5Ulc9zDI&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=390s)

---

### Step 05.2 — Name the six gantry parts

![Voron manual p.83](assets/manual-pages/manual-p083.png)

**What you're looking at:** The same rectangle, now labelled. **A** and **B** are the two [CoreXY](16-glossary.md#c) motors: run together they move the toolhead in X, run against each other they move it in Y, so neither motor "is" an axis. The **XY bridge** is the rear cross-beam that holds the two drives apart; the **XY joints** are the printed blocks at the ends of the X beam that ride on the Y carriages; the two **[idlers](16-glossary.md#i)** at the front are the bearing blocks that turn each belt back on itself.

**Parts:** none.

**Do:** Read the overview and fix the vocabulary — B Drive (rear left), A Drive (rear right), XY Bridge (the E extrusion joining them), Left XY Joint, Right XY Joint, X Linear Rail, B Idler (front left), A Idler (front right). Write "A" and "B" on masking tape on the two drive units now; from here to Ch 10 the wiring, the belt paths and the Klipper config all use those letters.

**Check:** You can point at the A drive, the B idler and the right XY joint without hesitating.

Source: [Voron manual p.83](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=83)

---

### Step 05.3 — Pick the cable-chain bridge

![Voron manual p.84](assets/manual-pages/manual-p084.png)

**What you're looking at:** The cable bridge is the small orange arch that bolts on top of the right XY joint and lifts the toolhead's [drag chain](16-glossary.md#d) clear of the joint and of the moving belts. The two versions differ only in the hole pattern where the chain's end link screws on — three holes for generic chains, two for the IGUS pattern this kit ships.

**Parts:** `[a]_xy_joint_cable_bridge_2hole.stl` ×1 (orange).

**Do:** The manual offers a 3-hole bridge (generic chains) and a 2-hole bridge (IGUS-pattern chains). Take the **2-hole** part and put the 3-hole one away.

⚠ **Rev D+ / LDO:** *"Our cable chain ends use the 2 hole configuration. When printing parts that interface with cable chains, always use the 2hole version instead of 3hole (e.g. xy_joint_cable_bridge_2hole instead of xy_joint_cable_bridge_3hole)."* [src](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d)

Tip: keep `XY_cable_chain_bridge-Igus-3mm_backer.stl` (also on plate B02-P3) beside it. It is the same 2-hole pattern raised for a ~3 mm backer. The titanium backers carry **pilot** holes for the chain end link, not tapped ones — drill 2.5 mm and tap M3 if you want to use them. Fit whichever bridge clears once the backers are on. [src](https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers)

**Check:** One 2-hole bridge on the bench, one alternate beside it, the 3-hole variant binned.

Source: [Voron manual p.84](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=84) · [LDO printed-parts guide (Rev D)](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d) · [Ti extrusion-backers README (tanaes)](https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers) · [Video: Part 3 @1:43:24](https://www.youtube.com/watch?v=ii14-2COjuA&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=6204s)

---

### Step 05.4 — Test-fit T-nuts and stage the fasteners

![CAD render — every T-nut this chapter will ever load](assets/cad/05-04-a.png)
![CAD render — every T-nut this chapter will ever load, in place](assets/cad/05-04-b.png)

**What you're looking at:** No picture — this is a dry run with the fasteners. A [roll-in T-nut](16-glossary.md#r) drops into an extrusion slot and rotates a quarter turn to lock, and almost every bolt in this chapter pulls against one. They can only be fed in through an open slot, and the drive and idler blocks cap those slots later in this chapter, so every nut goes in now or not at all. The four gantry extrusions — E across the back, the two C side beams and the D cross beam — with every T-nut this chapter needs already in its slot, because the printed blocks cap those slots later on.

**Parts:** M5 roll-in T-nut ×26, M3 roll-in T-nut ×27 (+ ~30 for the backers).

**Do:** Take one M5 and one M3 T-nut and roll them through each face of each of the four extrusions. Note which faces run freely and which bind, and mark the tight faces with tape. Count the fasteners out into labelled trays per the hardware table above — this chapter loads T-nuts on six different faces and there is no way to add one later.

**Check:** Every T-nut you will use rolls in without force. A forced roll-in nut galls the channel and the next one will not go in at all.

Tip: The CAD extrusions are the 250 lengths (E 240, C 350, D 330 mm); yours are the 350 set. Which faces carry nuts, and how many, is what transfers.

Source: [LDO Build Notes § Voron 2.4 build FAQ](https://docs.ldomotors.com/en/voron/voron2/build-faq) · [Voron manual p.85](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=85) · [Video: Part 4 @0:36:43](https://www.youtube.com/watch?v=ViB5Ulc9zDI&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=2203s) · CAD: Voron 2.4r2 STEP @ de7e89d

Pause: ~25 min since the last pause — bench cleared, sub-assemblies laid out left/right, T-nuts test-rolled and counted into trays. Nothing is assembled; leave the trays covered so nothing gets swept off.

---

### Step 05.5 — Load the E extrusion (XY bridge)

![Voron manual p.85](assets/manual-pages/manual-p085.png)

**What you're looking at:** The E extrusion is the **XY bridge** — the beam across the back of the gantry that holds the two drive blocks a fixed distance apart and so sets the gantry's width. The eight M5 T-nuts you slide in are what those drive blocks bolt down onto.

**Parts:** E extrusion ×1, M5 T-nut ×8.

**Do:** Slide **eight** M5 T-nuts into the E extrusion — four at each end, two per slot, in the two slots the highlight shows. Push them 10–15 mm in from the ends so they are clear of the drive frame's tongue but still under its bolt holes.

**Check:** 4 nuts at each end, threaded holes facing outward, none of them jammed.

Source: [Voron manual p.85](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=85)

---

### Step 05.6 — Slide the A drive onto the E extrusion

![Voron manual p.85](assets/manual-pages/manual-p085.png)

**What you're looking at:** The A drive is the right-hand assembly from Ch 04: a stepper motor with its 20 T pulley, wrapped in a printed frame that carries the belt bearing posts. It slides over the end of the bridge extrusion like a sleeve. The whole gantry is built motors-down and stays that way until the flip at Step 05.41.

**Parts:** A drive assembly ×1, E extrusion ×1.

**Do:** Push the A drive unit onto one end of the E extrusion, motor pointing **down** (the assembly stays upside down until p.106). Seat it until the printed part is flush with the extrusion end.

**Check:** Plastic flush to the aluminium end face, and the four M5 T-nuts visible through the drive frame's bolt holes.

Source: [Voron manual p.85](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=85)

---

### Step 05.7 — Bolt the A drive to the bridge

![Voron manual p.86](assets/manual-pages/manual-p086.png)

**What you're looking at:** Four M5×10 BHCS pass through the drive frame's flange into the T-nuts underneath. This is what turns the drive block and the bridge into one rigid rear corner; a bolt that spins freely means its T-nut never rolled and the corner is holding on three.

**Parts:** M5×10 BHCS ×4.

**Do:** Drive four M5×10 BHCS — two into the upper slot, two into the lower — and take them to snug, not torqued. If a bolt spins without pulling, the T-nut has not rolled; back it out and reseat the nut rather than forcing it.

**Check:** All four bolts bite. The drive frame does not rock on the extrusion.

Source: [Voron manual p.86](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=86)

---

### Step 05.8 — Slide the B drive onto the other end

![Voron manual p.86](assets/manual-pages/manual-p086.png)

**What you're looking at:** The B drive is the left-hand counterpart. It is not an identical copy: its motor pulley sits at 6.5 mm where the A drive's sits at 16.5 mm (set in Ch 04), which is what puts the two belts in two separate planes so they can cross without touching. Cable exits facing each other is the fast check that neither drive is on backwards.

**Parts:** B drive assembly ×1.

**Do:** Push the B drive onto the free end of the E extrusion, motor down, flush to the end face. The two drives are mirror images — the motor cable exits must point **towards each other** (manual p.75, MOTOR ORIENTATION). If they point apart, you have the drives swapped end for end.

**Check:** Both motor cable exits face inboard, both printed parts flush.

Source: [Voron manual p.86](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=86)

---

### Step 05.9 — Bolt the B drive and check the bridge

![Voron manual p.87](assets/manual-pages/manual-p087.png)

**What you're looking at:** With both drives bolted on, bridge plus drives is a single rear beam — the fixed back edge of the gantry, and the reference everything else is built to. The plan view is the alignment check: the two drive frames parallel, the two pulley stacks lined up across the bridge.

**Parts:** M5×10 BHCS ×4.

**Do:** Fit the last four M5×10 BHCS, snug. Then sight down the plan view: the two drive frames must be parallel and the two pulley stacks must line up across the bridge, exactly as the lower graphic shows.

**Check:** Drives parallel, no twist along the bridge, all eight M5×10 in and snug. Nothing here is torqued yet.

Source: [Voron manual p.87](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=87)

Pause: ~30 min since the last pause — XY bridge bolted to both drive units, bridge bolts tight. Lay the assembly flat, still upside down. Do not start a Y rail: a rail must be centred and screwed down in one sitting.

---

### Step 05.10 — Load M3 T-nuts for the first Y rail

![Voron manual p.88](assets/manual-pages/manual-p088.png)

**What you're looking at:** The two C extrusions are the **Y axes** — the side rails the X beam slides along. Each carries an [MGN9](16-glossary.md#m) linear rail on one face. The M3 T-nuts you load now are the anchor for every rail screw; once the rail is down, there is no way to add one.

**Parts:** C extrusion ×1, M3 T-nut ×~10.

**Do:** This kit's Y rails are **400 mm** MGN9H (`LDO-SLR9H-400Z0`), not the 250-spec rails the manual's drawings are dimensioned from. A 400 mm MGN9 has 20 holes at 20 mm pitch and the pattern uses **every other hole**, so you need about **10** T-nuts per rail. Count the holes on your own rail and mark the ones you will use before loading any nuts. Slide them into the slot that will carry the rail, spread along its length, orientation as the highlight shows. Leave roughly 25 mm of free slot at each end — the rail does not reach the extrusion ends and later steps need that space.

**Check:** ~10 nuts, one per marked hole, evenly spread, all rolled flat in the channel, ~25 mm clear at both ends.

Source: [Voron manual p.88](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=88) · [LDO Build Notes § Voron 2.4 build FAQ](https://docs.ldomotors.com/en/voron/voron2/build-faq)

---

### Step 05.11 — Centre and start the first MGN9 rail

![Voron manual p.88](assets/manual-pages/manual-p088.png)

**What you're looking at:** An MGN9 rail is a hardened steel guide with a recirculating-ball carriage riding on it; that carriage is what an XY joint bolts to at Step 05.43. The two printed guides are U-shaped clips that straddle rail and extrusion and hold the rail dead-centred while you start the screws, so the rail's position is set by the jig rather than by eye.

**Parts:** MGN9H 400 mm rail ×1, `MGN9_rail_guide_x2` jig ×2, M3×8 SHCS ×~10 (one per marked hole).

**Do:** Tape the carriage to the middle of the rail before you pick it up. Sit the rail on the extrusion, slide a printed MGN9 guide onto each end and let them centre it side to side. Start the first screw in the **second hole from the end**, not the end hole, and work along.

⚠ **Rev D+ / LDO:** *"Do not use the holes on the ends of the rails, use the second ones from the ends."* [src](https://docs.ldomotors.com/en/voron/voron2/build-faq) — the manual only requires this on 300 mm builds; LDO requires it on every build, because the end holes sit over the T-nuts you load at Step 05.13/05.14.

**Check:** Rail centred on the extrusion by both jigs. The p.88 detail dimensions **25 mm** from the extrusion end to the rail end — measure both ends and make them equal.

Source: [Voron manual p.88](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=88) · [LDO Build Notes § Voron 2.4 build FAQ](https://docs.ldomotors.com/en/voron/voron2/build-faq) · [LDO rail-grease guide](https://docs.ldomotors.com/guides/rail_grease_guide) · [Video: Part 3 @1:34:58](https://www.youtube.com/watch?v=ii14-2COjuA&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=5698s)

---

### Step 05.12 — Tighten the first Y rail

![Voron manual p.88](assets/manual-pages/manual-p088.png)

**What you're looking at:** The same rail, now being pulled flat onto the extrusion. Tightening from the centre outwards pushes any bow out towards the free ends instead of trapping it in the middle — a rail screwed down bowed is a tight spot the carriage will hit on every single pass for the life of the machine.

**Parts:** the ~10 M3×8 SHCS already started.

**Do:** Run every screw down finger-tight first, re-check the jigs at both ends and the middle, then tighten from the centre outwards in two passes. The manual gives no torque figure — take them to firm and even, not maximum. Re-fit a jig after the last pass to confirm nothing walked.

**Check:** Rail sits flat with no visible gap under it anywhere; the guide jig still slides on at both ends and the middle; the carriage runs the full length with no notch or tight spot.

Source: [Voron manual p.88](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=88) · [LDO rail-grease guide](https://docs.ldomotors.com/guides/rail_grease_guide)

Pause: ~30 min since the last pause — first Y rail centred, all its M3×8 screwed down, carriage still on. Tape or stopper the carriage before you walk away.

---

### Step 05.13 — Second Y axis, then load the end M5 T-nuts

![Voron manual p.89](assets/manual-pages/manual-p089.png)

**What you're looking at:** The second Y axis is a mirror of the first, not a copy: built side by side, both rails must end up facing the same way when the pair is stood as the left and right sides of the machine. The M5 T-nuts going into the four extrusion ends are for the front idler blocks and the drive frames, which seal those slots the moment they are fitted.

**Parts:** C extrusion ×1, MGN9H rail ×1, M3 T-nut ×8, M3×8 SHCS ×8; then M5 T-nut ×8.

**Do:** Repeat Steps 05.10–05.12 on the second C extrusion — it is a mirror, not a copy, so build it lying next to the first with both rails facing the same way. Then slide **two M5 T-nuts into each end of each C extrusion** (eight in total), in the slot and orientation the highlight shows. These are the nuts the front idler and the A/B drive frames bolt into.

**Check:** Two rails installed and equally centred. 2 M5 T-nuts sitting at each of the four extrusion ends.

Source: [Voron manual p.89](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=89)

---

### Step 05.14 — Load the reserved M5 + M3 pair at each end

![Voron manual p.90](assets/manual-pages/manual-p090.png)

**What you're looking at:** One more M5 and one more M3 nut at each end, for hardware that belongs to later chapters — the Ch 06 [Z joints](16-glossary.md#z), and the chain and endstop mounts in Ch 10. Nothing in this chapter uses them; they are loaded now purely because the idler and drive frames are about to close these slots permanently.

**Parts:** M5 T-nut ×4, M3 T-nut ×4.

**Do:** At each end of each C extrusion add **one M5 T-nut and one M3 T-nut** in the slot the blow-ups show — M5 outermost, M3 just inboard of it, both in the free slot beyond the rail end. Nothing in this chapter uses them; they are for the Z joints, chain retainers and endstop hardware in Ch 06 and Ch 10, and once the idler and drive frames are on you cannot get another nut into these slots.

**Check:** Four ends, each with one M5 and one M3 T-nut in addition to the pair from Step 05.13 — three M5 and one M3 per end. Count them before you go on.

Source: [Voron manual p.90](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=90)

---

### Step 05.15 — Stop the carriages running off

![CAD render — keep both Y carriages captive](assets/cad/05-15-a.png)
![CAD render — keep both Y carriages captive, in place](assets/cad/05-15-b.png)

**What you're looking at:** A linear-rail carriage keeps its ball bearings only while it is on the rail — run it off the end and they scatter, and the manual is blunt that a dropped carriage is likely ruined. A rubber stopper or a doubled tape flag near each end makes that impossible rather than merely unlikely. The two Y rails on the undersides of the C extrusions, each carrying one carriage — the stoppers near the ends are what stop a carriage sliding off and scattering its ball bearings.

**Parts:** rubber rail stoppers (LDO-supplied) or masking tape.

**Do:** Fit a rubber rail stopper — or a doubled tape flag — near each end of both Y rails so a carriage cannot run off. Keep the stoppers: LDO reuses them under the Z joints at manual p.114–116 to rest the gantry during install. [src](https://docs.ldomotors.com/en/voron/voron2/build-faq)

**Check:** Each Y carriage is captive. *"Dropping the carriage likely irreparably damages it"* (manual p.88).

Tip: The CAD Y rails are MGN9 300 mm; yours are 400 mm (Step 05.10). The stoppers go near the ends wherever those ends are.

Source: [Voron manual p.88](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=88) · [LDO Build Notes § Voron 2.4 build FAQ](https://docs.ldomotors.com/en/voron/voron2/build-faq) · CAD: Voron 2.4r2 STEP @ de7e89d

Pause: ~30 min since the last pause — both Y rails down and tightened, end M5/M3 T-nuts loaded, both carriages captive. Do not fit a backer now: start one only when you can finish it.

---

### Step 05.16 — Unpack and identify the titanium backers

![CAD render — which backer is which, and which face it goes on](assets/cad/05-16-a.png)

**What you're looking at:** The titanium [backers](16-glossary.md#b) are three flat drilled strips that bolt to the extrusion face **opposite** a linear rail. A steel rail screwed to an aluminium extrusion makes a bimetallic strip that bows as the chamber heats; a titanium strip on the far face pulls the other way and cancels most of that bow. Two matching long ones are the Y backers, the odd shorter one is the X backer. The three backers laid on the extrusions they belong to — the two matching long ones on top of the Y (C) beams, the odd shorter one on the back of the X (D) beam, always on the face opposite that beam's rail.

**Parts:** titanium backer set ×3 (2 long "Y", 1 shorter "X"), M3×8 FHCS ×~20, M3×6 FHCS ×~8, M3 roll-in T-nut ×~30.

**Do:** Lay the three backers out. The two matching long pieces are the **Y** backers, the odd shorter one is the **X** backer. Check they are drilled and countersunk — the vendor sets ship *"pre drilled and ready for install"* ([Fabreeko](https://www.fabreeko.com/products/v2-4-trident-titanium-extrusion-backers)) — and count the holes so you know how many screws and T-nuts each one needs. A backer that is slightly bowed along its length is fine: *"During installation, they'll clamp down to the extrusion and straighten right out."*

**Check:** 2 Y + 1 X backer, hole counts written down, and you have at least that many M3 T-nuts. The set does not include T-nuts.

Tip: Backer lengths in the picture follow the 250 CAD's extrusions. Sort your set by matched pair versus odd one, not by the lengths drawn here.

Source: [Ti extrusion-backers README (tanaes)](https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers) · [Fabreeko backer set](https://www.fabreeko.com/products/v2-4-trident-titanium-extrusion-backers) · [West3D backer set](https://west3d.com/products/titanium-backers-for-voron-2-4-trident-3-pack) · CAD: Voron 2.4r2 STEP @ de7e89d

---

### Step 05.17 — Fit the first Y backer

![Backer faces for a 1×MGN12 gantry — backers (magenta) on the top of both Y extrusions and the rear of the X extrusion](assets/remote/05-gantry/ti-backer-face-layout.jpeg)

**What you're looking at:** You are working on the bare back of the first Y extrusion — the face with no rail on it, which becomes the top of the Y axis in the finished machine. FHCS are countersunk screws whose heads sink flush into the backer's chamfered holes; that large cone of contact is exactly why a hex key cams out of them and why the T10 Torx is worth finding.

**Parts:** Y backer ×1, M3×8 FHCS ×~10, M3 T-nut ×~10, T10 Torx driver.

**Do:** Turn the first C extrusion so the MGN9 rail faces away from you and work on the **opposite face** — in the finished machine that is the top of the Y extrusion. Roll the T-nuts into that face's slot, lay the backer on, and start every screw before tightening any. Use **M3×8 FHCS for Y**, driven with Torx if you have it: *"the added contact surface area with the countersinks makes the M3 FHCS susceptible to camming out."* Tighten from the centre outwards so the backer flattens onto the extrusion rather than bowing between fixings.

⚠ **Never on the rail face:** the whole point is to put steel on the face *opposite* the rail and cancel the bending couple. Doubling up on the rail side makes the bow worse. [src](https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers)

**Check:** Backer flat along its whole length, no rocking, every screw seated in its countersink and none of them cammed out. Both ends clear of where the idler and drive frames will land.

Source: [Ti extrusion-backers README (tanaes)](https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers) (image [`x_axis.jpeg`](https://raw.githubusercontent.com/tanaes/whopping_Voron_mods/main/extrusion_backers/images/x_axis.jpeg))

---

### Step 05.18 — Fit the second Y backer

![CAD render — the backer goes on the face opposite the rail](assets/cad/05-18-a.png)
![CAD render — both Y backers, mirrored, on the top faces](assets/cad/05-18-b.png)

**What you're looking at:** The second Y extrusion, same treatment on its rail-opposite face. The check that matters is that the two finished assemblies read as mirrors — rails on the same side as each other, backers on the same side as each other, when the pair is stood up as the left and right of the machine. One Y extrusion seen from underneath, so the rail face and the backer face are both in frame — the backer always goes on the face directly opposite the rail. Both Y beams in place, mirrored about the machine's centreline — rails underneath on both, backers on top on both.

**Parts:** Y backer ×1, M3×8 FHCS ×~10, M3 T-nut ×~10.

**Do:** Repeat on the second C extrusion, again on the face opposite its rail. Lay the two finished Y assemblies side by side and confirm they are mirrored — rails facing the same way, backers facing the same way.

**Check:** Both backers on the rail-opposite face, both flat. Their cable-chain pilot holes end up on the same side of the machine.

Tip: The CAD C extrusion is 350 mm with a 300 mm rail (250 machine); yours is the 350-kit C with a 400 mm rail.

Source: [Ti extrusion-backers README (tanaes)](https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers) · CAD: Voron 2.4r2 STEP @ de7e89d

Pause: ~35 min since the last pause — both titanium Y backers screwed down flat on the rail-opposite face. Check nothing is cammed out before you stop.

---

### Step 05.19 — Fit the front idler to the first Y axis

![Voron manual p.91](assets/manual-pages/manual-p091.png)

**What you're looking at:** The front idler block is the Ch 04 assembly that turns its belt around at the front corner: a printed frame around a stack of bearings, with a belt-clamp notch moulded into the outside. It slides onto the front end of a Y extrusion and bolts down into the M5 T-nuts you loaded at Step 05.13.

**Parts:** front idler assembly ×1, M5×16 BHCS ×2.

**Do:** Slide the idler onto the **front** end of the first C extrusion. Use the idler that has **two M5 holes in the top** when it is oriented as the page draws it — that is what tells the left idler from the right. Push it home, then drive two M5×16 BHCS down through its top flange into the M5 T-nuts from Step 05.13.

**Check:** Two M5 holes on top, both bolts biting into T-nuts, idler pulled up tight against the extrusion.

Source: [Voron manual p.91](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=91) · [Video: Part 4 @0:06:41](https://www.youtube.com/watch?v=ViB5Ulc9zDI&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=401s)

---

### Step 05.20 — Check flush and notch orientation

![Voron manual p.92](assets/manual-pages/manual-p092.png)

**What you're looking at:** The two front idlers are handed — genuinely different parts, not mirrored copies (their lower frames differ by 10 mm in height to match the two belt planes). Plastic sitting flush against the aluminium end face is the tell that you picked the right hand; the belt-clamp notch pointing outboard is the tell that it is the right way up.

**Parts:** none.

**Do:** Look at the joint from the end: the printed part must sit flush with the aluminium end face. If it does not, you have the wrong-hand idler — take it off rather than pulling it down with the bolts. Then check the belt-clamp indentation: the notch points **away from the idler assembly**.

**Check:** Plastic flush to the extrusion end, notch pointing outboard.

Source: [Voron manual p.92](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=92) · [Video: Part 4 @0:08:32](https://www.youtube.com/watch?v=ViB5Ulc9zDI&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=512s)

---

### Step 05.21 — Fit the second front idler

![Voron manual p.93](assets/manual-pages/manual-p093.png)

**What you're looking at:** The other front corner, with the opposite-hand idler. After this the two Y assemblies are complete as sides of the machine: rail, backer and idler on each.

**Parts:** front idler assembly ×1, M5×16 BHCS ×2.

**Do:** Same on the second Y assembly with the opposite-hand idler. Push flush, two M5×16 BHCS into the top-slot T-nuts, snug.

**Check:** Both Y assemblies now have an idler at the front, both flush, both notches pointing away from the idler body.

Source: [Voron manual p.93](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=93)

---

### Step 05.22 — Offer both Y axes to the drive units

![Voron manual p.94](assets/manual-pages/manual-p094.png)

**What you're looking at:** Now the two sides meet the rear beam. The A drive takes the right-hand side and the B drive the left, so the belt planes you set in Ch 04 line up with the corners those belts actually run to. What you end up with is a U — open at the front until the X beam goes in at Step 05.42.

**Parts:** the two Y assemblies, the bridge + drives assembly.

**Do:** Bring the rear end of each C extrusion into its drive frame — the assembly with the A drive takes the right-hand Y axis, the B drive the left. Push each in until the printed frame is flush with the extrusion end. Work on a flat bench so the four corners stay in one plane.

**Check:** A U-shaped gantry: bridge across the back, two Y axes running forward, idlers at the front. Both rails face the same way; both backers face the same way.

Source: [Voron manual p.94](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=94) · [Video: Part 4 @0:34:56](https://www.youtube.com/watch?v=ViB5Ulc9zDI&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=2096s)

---

### Step 05.23 — Bolt the Y axes to the drives

![Voron manual p.95](assets/manual-pages/manual-p095.png)

**What you're looking at:** Two M5×16 per side, down through each drive frame's flange into the rear-end T-nuts, closing the two rear corners. The two checks repeat the idler checks because the failure repeats too: a block not pushed fully home leaves that corner short, and a short corner is a gantry that cannot be squared.

**Parts:** M5×16 BHCS ×4.

**Do:** Two M5×16 BHCS per side, down through the drive frame's top flange into the M5 T-nuts at the rear of each C extrusion. Snug only. Check the same two things as at the idlers: plastic flush with the extrusion end, and the belt-clamp notch pointing **away from the drive assembly**.

**Check:** Four bolts in, both rear joints flush, both notches outboard.

Source: [Voron manual p.95](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=95)

---

### Step 05.24 — Sanity-check the gantry frame, then leave it alone

![Voron manual p.95](assets/manual-pages/manual-p095.png)

**What you're looking at:** Four corners, all snug, none torqued. Measuring inside face to inside face at both ends tells you the two Y axes are parallel; pushing the frame diagonally shows it can still [rack](16-glossary.md#r) — the rectangle deforming into a parallelogram. That freedom is deliberate: squaring happens with the gantry in the frame in Ch 06, and needs these joints loose.

**Parts:** none.

**Do:** Lay the U-frame flat and measure from the inside face of one Y extrusion to the other, at the bridge and again at the idlers. They should match within about a millimetre. Push the gantry gently diagonally — it will rack, and that is expected at this stage.

**Check:** Front and rear spacing equal within ~1 mm. **Do not try to square or lock the gantry now** — squaring happens with the gantry in the frame, belts slack, in Ch 06 (survey §4.4 #2).

Source: [Voron manual p.95](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=95)

Pause: ~40 min since the last pause — front idlers and both Y axes bolted to the drives, gantry frame sanity-checked and deliberately left slightly loose. Do not tighten anything further; do not start an XY joint (each joint is a bearing stack you must finish in one go).

---

### Step 05.25 — Seat the M5 nuts in both XY joints

![Voron manual p.96](assets/manual-pages/manual-p096.png)
![Lower XY joint bodies — left and right; the right-hand body carries the endstop wire channel](assets/parts/pair-xy_joint_lower_MGN12.png)

**What you're looking at:** The [XY joints](16-glossary.md#x) are the two printed blocks that cap the ends of the X beam and ride on the Y carriages. Each is a pair of parts: a thick **lower** body (~34 mm tall, about three times the plastic) that the extrusion end plugs into, and a thin **upper** plate (~16 mm) that caps it. These are the two lower bodies — and the way to tell left from right is the moulded wire channel: the **right** body has one (it carries the XY endstop wires), the **left** is plain.

**Parts:** `xy_joint_left_lower_MGN12` ×1, `xy_joint_right_lower_MGN12` ×1, M5 nut ×6.

**Do:** Drop **three M5 nuts** into the hex pockets of each XY joint body, flats aligned to the pocket. Push each one fully home with a spare M5 bolt; a nut sitting proud will stop the joint closing later and will crack the pocket if you bolt through it.

**Check:** Three nuts per joint, all flush in their pockets, none rotated out of the hex.

Source: [Voron manual p.96](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=96) · [Video: Part 5 @1:18:07](https://www.youtube.com/watch?v=hTKCBrk36R0&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=4687s) (differs: substitutes Trident-repo parts still in beta at the time)

---

### Step 05.26 — Start the right XY joint bearing stack

![Voron manual p.97](assets/manual-pages/manual-p097.png)
![Upper XY joint plates — left and right; the right-hand plate carries the endstop wire channel](assets/parts/pair-xy_joint_upper_MGN12.png)

**What you're looking at:** The two upper plates, left and right — same tell as the lower bodies: the right-hand plate has the endstop wire channel, the left does not. The stack you build on the M5×40 is the belt corner: two F695 flanged bearings with a brass [precision spacer](16-glossary.md#p) setting their height, which together with the 20 T idler added at Step 05.29 turns each belt around from its run along Y to its run along X.

**Parts:** `xy_joint_right_upper_MGN12` ×1, M5×40 SHCS ×1, F695 bearing ×2, M5 precision spacer ×1.

**Do:** Note the small channel moulded into the right-hand joint parts — that is the **cable path** for the endstop wires; keep it clear and pointing the way the page shows. Push an M5×40 SHCS up through the joint's upper plate, then stack onto it, in order: F695 bearing, F695 bearing, spacer.

⚠ **Rev D+ / LDO:** the manual's "M5 Shim" is the brass **M5 precision spacer** in this kit, here and everywhere else unless a page is explicitly noted otherwise. [src](https://docs.ldomotors.com/en/voron/voron2/build-faq)

**Check:** Two bearings and one spacer on the bolt, in that order, bearings spinning freely, cable channel unobstructed.

Source: [Voron manual p.97](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=97) · [LDO Build Notes § Voron 2.4 build FAQ](https://docs.ldomotors.com/en/voron/voron2/build-faq) · [Video: Part 3 @1:27:47](https://www.youtube.com/watch?v=ii14-2COjuA&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=5267s) (differs: pre-release kit had no titanium rail backers)

---

### Step 05.27 — Close the right XY joint

![Voron manual p.97](assets/manual-pages/manual-p097.png)

**What you're looking at:** The lower body comes down over the bearing stack and the M5×40's thread picks up one of the nuts you seated at Step 05.25. The two halves must close plastic-to-plastic with no gap — a bearing pinched between them drags on the belt, and you will not find it again until Ch 07.

**Parts:** `xy_joint_right_lower_MGN12` ×1 (with its three M5 nuts).

**Do:** Bring the joint body down over the bearing stack so the M5×40's thread enters the nut pocket you loaded at Step 05.25. The two halves must meet with no gap and no bearing pinched between them.

**Check:** Halves closed flat, bolt engaged in its nut, bearing stack still turning by finger.

Source: [Voron manual p.97](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=97) · [Video: Part 3 @1:28:26](https://www.youtube.com/watch?v=ii14-2COjuA&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=5306s) (differs: pre-release kit had no titanium rail backers)

---

### Step 05.28 — Bolt the right XY joint together

![Voron manual p.98](assets/manual-pages/manual-p098.png)

**What you're looking at:** The other two M5×40 bolts. Three bolts into three captive nuts turn the two printed halves into a single rigid block, which it has to be: belt tension in Ch 07 pulls hard on this corner and tries to prise it open.

**Parts:** M5×40 SHCS ×2.

**Do:** Add the two remaining M5×40 SHCS from the top into the other two M5 nuts and tighten all three evenly. These clamp the joint into a single rigid part.

**Check:** No light between the halves anywhere. The bearing stack still spins.

Source: [Voron manual p.98](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=98) · [Video: Part 3 @1:21:27](https://www.youtube.com/watch?v=ii14-2COjuA&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=4887s) (differs: pre-release kit had no titanium rail backers)

---

### Step 05.29 — Fit the right joint's 20-tooth idler

![Voron manual p.98](assets/manual-pages/manual-p098.png)

**What you're looking at:** The 20 T idler is a small toothed pulley running on its own bearing — the toothed side of the belt wraps it. Its M5×40 threads straight into plastic and does nothing but hold the idler in place, so it carries no clamping load and stops the instant the head seats.

**Parts:** GT2 20-tooth idler ×1, M5×40 SHCS ×1.

**Do:** Drop the 20T idler into its pocket and run an M5×40 SHCS down through it. This bolt threads **directly into plastic** and only positions the idler.

⚠ Do not over-tighten. Stop the moment the head seats and the idler still spins freely; a crushed pocket here shows up as belt noise and premature wear in Ch 07.

**Check:** Idler spins under a fingernail flick with no drag and no wobble.

Source: [Voron manual p.98](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=98) · [Video: Part 3 @1:25:58](https://www.youtube.com/watch?v=ii14-2COjuA&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=5158s) (differs: pre-release kit had no titanium rail backers)

Pause: ~25 min since the last pause — right XY joint fully built, bolted and its 20T idler fitted and spinning. Leave the left joint's parts bagged; do not part-build it.

---

### Step 05.30 — Build the left XY joint

![Voron manual p.99](assets/manual-pages/manual-p099.png)

**What you're looking at:** The left joint, built exactly as the right was. The tell is the wire channel: only the right-hand pair has one. If the parts in your hand have a channel, put them down — you are holding the right joint's.

**Parts:** `xy_joint_left_upper_MGN12` ×1, `xy_joint_left_lower_MGN12` ×1, M5×40 SHCS ×1, F695 bearing ×2, M5 precision spacer ×1.

**Do:** Mirror of Steps 05.26–05.27 — M5×40 up through the upper plate, F695, F695, precision spacer, then close the joint body over it into its M5 nut. The left joint has no endstop cable channel; if the part you are holding has one, you have the right-hand pair.

**Check:** Left and right joints sit as mirror images on the bench, not as two of the same hand.

Source: [Voron manual p.99](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=99)

---

### Step 05.31 — Bolt the left joint and fit its idler

![Voron manual p.100](assets/manual-pages/manual-p100.png)

**What you're looking at:** Both joints finished and identical in content: 4× M5×40, 2× F695, one precision spacer and one 20 T idler each. Everything that is meant to spin must still spin freely — drag here becomes belt drag and belt noise once the belts go on.

**Parts:** M5×40 SHCS ×3, GT2 20-tooth idler ×1.

**Do:** Two M5×40 SHCS from the top into the remaining M5 nuts, tightened evenly; then the 20T idler and its own M5×40 into plastic — snug only, must spin.

**Check:** Both joints complete: 4× M5×40 each, 2× F695 each, one spacer each, one 20T idler each, all four bearing stacks and both idlers free.

Source: [Voron manual p.100](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=100) · [Video: Part 3 @1:31:05](https://www.youtube.com/watch?v=ii14-2COjuA&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=5465s) (differs: pre-release kit had no titanium rail backers)

Pause: ~20 min since the last pause — both XY joints built, bolted and idler-fitted, sitting loose on the bench. Do not slide them onto the X extrusion yet.

---

### Step 05.32 — Load M3 T-nuts for the X rail

![Voron manual p.101](assets/manual-pages/manual-p101.png)

**What you're looking at:** The D extrusion is the **X beam** — the one the toolhead runs along. It carries an [MGN12](16-glossary.md#m) rail, wider and stiffer than the Y rails because it holds the whole toolhead cantilevered off one carriage. Same T-nut rule as the Y axes: load them now, before the XY joints cap the ends.

**Parts:** D extrusion ×1, M3 T-nut ×~8.

**Do:** The X rail is a **400 mm** MGN12H (`LDO-SLR12H-400Z1`): ~16 holes at 25 mm pitch, every other hole, so about **8** T-nuts. Count the holes and mark the ones you will use, then slide the nuts into the D extrusion's rail slot, spread along it, orientation per the highlight. Leave about 15 mm of clear slot at each end.

**Check:** ~8 nuts in, one per marked hole, flat, with clear slot at both ends.

Source: [Voron manual p.101](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=101)

---

### Step 05.33 — Centre and fit the MGN12 rail

![Voron manual p.101](assets/manual-pages/manual-p101.png)

**What you're looking at:** Same centre-and-tighten procedure as the Y rails, with the larger MGN12 guides. This is the rail that decides print quality across X, so the two things to get right are that it sits centred along its whole length and that it pulls down flat with no gap anywhere underneath.

**Parts:** MGN12H 400 mm rail ×1, `MGN12_rail_guide_x2` jig ×2, M3×8 SHCS ×~8 (one per marked hole).

**Do:** *"Temporarily secure the carriage with a piece of sticky tape to prevent it from sliding off the rail"* before you handle it. Sit the rail on the D extrusion, centre it with an MGN12 guide at each end, and start the first screw in the **second hole from the end**. Run them all down finger-tight, re-check the jigs, then tighten centre-outwards in two passes.

⚠ **Rev D+ / LDO:** second hole in from each end here too, not the end hole. [src](https://docs.ldomotors.com/en/voron/voron2/build-faq)

**Check:** The p.101 detail dimensions **15 mm** of bare extrusion beyond the rail end — measure both ends and make them equal. Carriage runs the full rail with no tight spot; rail flat with no gap under it.

Source: [Voron manual p.101](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=101) · [LDO Build Notes § Voron 2.4 build FAQ](https://docs.ldomotors.com/en/voron/voron2/build-faq) · [LDO rail-grease guide](https://docs.ldomotors.com/guides/rail_grease_guide) · [Video: Part 3 @1:34:46](https://www.youtube.com/watch?v=ii14-2COjuA&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=5686s)

---

### Step 05.34 — Fit the X backer to the rear face

![Titanium X backer on the rear face of the X extrusion, with the cable-chain pilot holes](assets/remote/05-gantry/ti-backer-x-rear-face.png)

**What you're looking at:** The X backer goes on the rear face — the one directly opposite the rail — for the same reason as on the Y axes: steel on one face, titanium on the other, the two bows cancelling. The top face of the X beam stays bare because the XY joints and the cable bridge bolt into it.

**Parts:** X backer ×1, M3×6 FHCS ×~8, M3 T-nut ×~8.

**Do:** Turn the D extrusion so the MGN12 rail faces you. The backer goes on the **rear face — the one directly opposite the rail**, not on top. Roll the T-nuts in, start every screw, then tighten centre-outwards. Use **M3×6 FHCS for X** — the 8 mm screws are for Y and will bottom out.

⚠ *"For X axes, in most cases you'll want to install them on the rear of the X extrusion, opposite the MGN12 rail… If you have a single MGN12 but decide to put a backer on top, you will be actively contributing to the problem of bimetallic expansion!"* [src](https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers)

**Check:** Backer on the face opposite the MGN12, flat, all screws seated. Nothing added to the top face of the D extrusion — the XY joints and the cable bridge need that face clear.

Source: [Ti extrusion-backers README (tanaes)](https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers) (image [`fusion_x_chainmount.png`](https://raw.githubusercontent.com/tanaes/whopping_Voron_mods/main/extrusion_backers/images/fusion_x_chainmount.png))

---

### Step 05.35 — Check backer clearance for the cable chain

![CAD render — the chain's fixed end lands on the backer's face](assets/cad/05-35-a.png)
![CAD render — which bridge, and the run it has to serve](assets/cad/05-35-b.png)

**What you're looking at:** A dry fit; nothing gets fixed here. The backers carry pilot holes for the cable chain's end link, and the printed bridge has a flat foot that a 3 mm titanium strip may now hold off the extrusion. This is where you decide which of the two bridges from Step 05.3 you keep. The fixed end of the Y cable chain, lifted off the beam it bolts to — that bolt goes down through the top face of the Y extrusion, which is the face the titanium backer covers, so the link may now sit 3 mm proud. The cable chain's full run along the right Y beam, from its fixed end at the back to the printed bridge on the XY joint at the front — and both bridge variants, of which this kit uses the 2-hole one.

**Parts:** cable-chain end link (dry fit only).

**Do:** The backers carry **pilot holes for the cable-chain end link**. Offer the chain's end link up to the X backer and to the Y backers and see whether the holes line up and whether the stock printed bridge still sits flat. Do not fit the chain — that is Ch 10 — you are only deciding which bridge to keep.

**Check:** You know whether you will use `[a]_xy_joint_cable_bridge_2hole` or the raised `XY_cable_chain_bridge-Igus-3mm_backer`. "Igus" = the 2-hole pattern LDO ships. [src](https://docs.ldomotors.com/guides/cable_chain_guide)

Tip: The CAD chain and extrusion are the 250 machine's; a 350 chain run is longer. What transfers is which face the end link lands on. The raised bridge variant the parts list names is a mod part and is not in the Voron CAD — only the stock 2-hole and 3-hole bridges are.

Source: [Ti extrusion-backers README (tanaes)](https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers) · [LDO cable-chain guide](https://docs.ldomotors.com/guides/cable_chain_guide) · CAD: Voron 2.4r2 STEP @ de7e89d

Pause: ~35 min since the last pause — MGN12 rail centred and screwed down on the X extrusion, titanium X backer on the rear face, cable-chain clearance checked. Carriage taped captive.

---

### Step 05.36 — Load the D extrusion's M5 T-nuts

![Voron manual p.102](assets/manual-pages/manual-p102.png)

**What you're looking at:** Six M5 T-nuts in two different slots of the X beam: four in the face the XY joints bolt down onto, two in the opposite face for the long bolts that come up from underneath at Step 05.39. Between them they clamp each joint to the beam from both sides so it cannot rock.

**Parts:** M5 T-nut ×6.

**Do:** Two slots are used here. In the slot on the face **adjacent to the rail** (the joints' bolting face) put **two M5 T-nuts at each end** — four in total. In the slot on the **opposite** face put **one M5 T-nut at each end** — two in total. Both blow-ups on the page show the orientation.

**Check:** 4 + 2 = six M5 T-nuts. The two singles line up with the through-holes the M5×30 bolts will use from underneath.

Source: [Voron manual p.102](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=102)

---

### Step 05.37 — Slide both XY joints onto the X extrusion

![Voron manual p.103](assets/manual-pages/manual-p103.png)

**What you're looking at:** Each joint's pocket slides over an end of the X beam. This is the first time the X axis exists as one object — beam, rail, backer and both belt corners.

**Parts:** left XY joint ×1, right XY joint ×1.

**Do:** Push a joint onto each end of the D extrusion, left joint to the left end, right joint (the one with the endstop cable channel) to the right. Seat each until the extrusion bottoms out in the joint's pocket.

**Check:** Both joints fully home; the two 20T idlers and the two bearing stacks all face the same way along the extrusion.

Source: [Voron manual p.103](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=103)

---

### Step 05.38 — Bolt the joints from above, with the cable bridge

![Voron manual p.104](assets/manual-pages/manual-p104.png)

**What you're looking at:** Bolts down through the top of each joint into the beam's top-slot T-nuts. On the right, the orange cable bridge's foot is sandwiched under the two heads, which is why that side needs the longer M5×16. They are left slightly loose on purpose: Ch 06 squares the gantry by nudging these joints along the beam, which it cannot do if they are locked down.

**Parts:** M5×10 BHCS ×2, `[a]_xy_joint_cable_bridge_2hole` ×1, M5×16 BHCS ×2.

**Do:** On the **left** joint, two M5×10 BHCS straight down into the extrusion's top-slot T-nuts. On the **right** joint, lay the cable bridge's foot over the same two holes and use the longer **M5×16 BHCS** to bolt through bridge and joint into the extrusion. *"LEAVE SLIGHTLY LOOSE — lightly tighten the bolts."* These joints are re-seated when the gantry is squared in Ch 06.

**Check:** Bridge foot flat with its arm standing up on the right-hand side; four bolts started and lightly tightened, none torqued.

Source: [Voron manual p.104](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=104)

---

### Step 05.39 — Bolt the joints from below

![Voron manual p.104](assets/manual-pages/manual-p104.png)

**What you're looking at:** Two more bolts, this time up into the joints from underneath the beam, each with a black washer to spread the load across the plastic. Pulled from both faces the joint cannot rock — but still only lightly tightened, until squaring.

**Parts:** M5×30 BHCS ×2, black M5 washer ×2.

**Do:** Turn the X assembly over and run an M5×30 BHCS with a washer under its head up into each of the single M5 T-nuts from Step 05.36. Light tightening again — the whole joint stays slightly loose until Ch 06.

⚠ **Rev D+ / LDO (p.104):** *"Use the black M5 Washer instead of the M5 Shim cause it looks nicer."* This page is the documented exception to the precision-spacer substitution. [src](https://docs.ldomotors.com/en/voron/voron2/build-faq)

**Check:** Two M5×30 in with black washers under the heads, both lightly tightened.

Source: [Voron manual p.104](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=104) · [LDO Build Notes § Voron 2.4 build FAQ](https://docs.ldomotors.com/en/voron/voron2/build-faq)

---

### Step 05.40 — Check the X axis assembly

![Voron manual p.105](assets/manual-pages/manual-p105.png)

**What you're looking at:** The finished X axis, checked against the drawing. What you are sighting for is that both belt corners sit at the same height: a 20 T idler or an F695 stack a millimetre out of plane feeds the belt into the drive pulley at an angle and chews its edge.

**Parts:** none.

**Do:** Compare your X assembly with the page. Sight along the extrusion at each end: the 20T idler and the F695 stack must be in the same plane as their opposite numbers, so a belt can run straight between them. Spin all four.

**Check:** Idler and bearing-stack heights match end to end; nothing binds; the MGN12 carriage still slides freely and is still taped.

Source: [Voron manual p.105](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=105)

Pause: ~35 min since the last pause — both XY joints bolted to the X extrusion top and bottom, cable bridge on, assembly checked against p.105. Still upside down; leave it that way and do not attempt the flip alone.

---

### Step 05.41 — Flip the gantry

![Voron manual p.106](assets/manual-pages/manual-p106.png)

**What you're looking at:** Everything since the bridge was built inverted, so gravity held the bearing stacks in place while you closed the joints. Turning it over puts the motors on top and the two Y carriages where you can reach them, which is the orientation the machine actually runs in.

**Parts:** none.

**Do:** Turn the U-frame gantry over so the A/B motors point up and both MGN9 carriages face you. Everything from p.85 on was built inverted; this is the orientation the machine actually uses. Get a second pair of hands — it is large, unbraced, and the drives are heavy.

**Check:** Motors up, both Y carriages accessible from above, nothing dropped on a bearing stack.

Source: [Voron manual p.106](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=106)

---

### Step 05.42 — Insert the X axis at an angle

![Voron manual p.106](assets/manual-pages/manual-p106.png)

**What you're looking at:** The X axis drops onto the two Y carriages — the sliding blocks on the Y rails. Tilting it lets you land one joint at a time; lowering it flat means fighting both carriages at once, and a carriage shoved sideways off its rail is a ruined carriage.

**Parts:** the X axis assembly.

**Do:** *"Tilt the X axis to install it onto the gantry."* Bring one XY joint down onto its Y carriage first, then swing the other end across and drop it onto the second carriage. The left joint goes to the left Y rail, the right joint (cable bridge, endstop channel) to the right.

**Check:** Both joints sitting squarely on their carriages, bolt holes lined up, no bearing or idler fouling the Y extrusion.

Source: [Voron manual p.106](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=106)

---

### Step 05.43 — Bolt the XY joints to the Y carriages

![Voron manual p.106](assets/manual-pages/manual-p106.png)

**What you're looking at:** M3×16 down through each XY joint into the threaded holes in the Y carriage below it. The right joint deliberately gets only two: the XY endstop pod fitted at wiring shares its other two holes, and the two bolts you set aside now are the ones it will need.

**Parts:** M3×16 SHCS ×6.

**Do:** The **left** joint takes all four M3×16 SHCS. The **right** joint — the one with the cable bridge, whose remaining two holes the endstop pod will share — takes **two only**. *"2X BOLT ONLY: the remaining bolts will be installed during the end-stop installation."* Take all six to snug.

**Check:** 4 bolts on one joint, 2 on the other, 2 M3×16 left over and bagged with `[a]_endstop_pod_D2F_switch`. Count them; the pod cannot go on later without them.

Source: [Voron manual p.106](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=106)

---

### Step 05.44 — Run the X axis end to end

![Voron manual p.106](assets/manual-pages/manual-p106.png)

**What you're looking at:** The first real function test of the gantry as a mechanism. Even, light resistance the whole way means both rails are centred and both carriages sit square on them. Resistance that grows steadily towards one end is [racking](16-glossary.md#r) — the rectangle sitting as a parallelogram — and it is a Ch 06 problem, not a rail problem.

**Parts:** none.

**Do:** Push the X axis slowly from one end of the Y travel to the other, several times, with a hand on each XY joint. It should move with even, light resistance the whole way. A tight spot near one end usually means a rail is not centred; a general stiffness that grows towards one end usually means the gantry is racked — do **not** fix that by loosening rails.

**Check:** Full travel both directions, no notch, no rising resistance, both Y carriages moving together. Racking is normal and is corrected in Ch 06.

Source: [Voron manual p.106](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=106)

Pause: ~30 min since the last pause — gantry flipped, X axis in and bolted to both Y carriages, running end to end without binding. Belts still bagged, XY joint bolts still only lightly tightened — leave both alone.

---

### Step 05.45 — Stage the X-carriage frame halves

![X carriage frame halves — left and right](assets/parts/pair-x_frame_V2TR_MGN12.png)
![CAD render — stage the X-carriage frame halves](assets/cad/05-45-a.png)
![CAD render — stage the X-carriage frame halves, in place](assets/cad/05-45-b.png)

**What you're looking at:** The [X carriage](16-glossary.md#x) is the two-part printed frame that clamps onto the MGN12 carriage and becomes the mounting plate for the entire toolhead — extruder, hotend and toolboard all hang off it. These are the Clockwork-2 (R2) halves shown left and right in the render; older X-carriage parts look almost the same and will not fit. The two halves of the X carriage — handed, so they only nest one way — together with the probe retainer and the MGN12 carriage block whose bolt pattern they must match.

**Parts:** `x_frame_V2TR_MGN12_left` ×1, `x_frame_V2TR_MGN12_right` ×1, `probe_retainer_bracket` ×1.

**Do:** Offer the two carriage halves to the MGN12 carriage and confirm the bolt pattern matches before you commit any heat-set inserts to them. These are the R2 / Clockwork-2 halves and they are **not** interchangeable with older X-carriage parts. Then bag them, labelled, with the probe retainer.

⚠ **Rev D+ / LDO (p.129–130):** *"If you are building Clockwork 2 double-check that you have the correct X-Carriage and follow the instructions in the Stealthburner manual."* [src](https://docs.ldomotors.com/en/voron/voron2/build-faq) The carriage goes on with the belts in Ch 07; the toolhead itself is Ch 08.

**Check:** Bolt pattern matches the MGN12 carriage; both halves and the probe retainer bagged and labelled for Ch 07.

Source: [Voron manual p.129](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=129) · [LDO Build Notes § Voron 2.4 build FAQ](https://docs.ldomotors.com/en/voron/voron2/build-faq) · [Video: Part 5 @1:05:47](https://www.youtube.com/watch?v=hTKCBrk36R0&list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY&t=3947s) (differs: substitutes Trident-repo parts still in beta at the time · MGN12 X was a mod then; it is stock on this kit) · CAD: Voron 2.4r2 STEP @ de7e89d

---

### Step 05.46 — Bag what belongs to later chapters

![CAD render — the two Rev D+ variant choices, pulled apart](assets/cad/05-46-a.png)
![CAD render — where the two parts you keep end up](assets/cad/05-46-b.png)

**What you're looking at:** Housekeeping for later chapters. The [XY endstop pod](16-glossary.md#x) is the small orange box that carries the X and Y limit switches on the right XY joint; the tensioners are the sprung blocks that pull the A/B belts tight at the front idlers in Ch 07. None of it fits yet and all of it is easy to lose. The two either/or choices on the right XY joint, pulled apart so you can see both at once — print the D2F endstop pod and keep the 2-hole cable bridge; the hall-effect pod and the 3-hole bridge are not used in this kit. Where the endstop pod and the cable bridge you kept eventually live — both on the right-hand XY joint, fitted in later chapters.

**Parts:** `[a]_endstop_pod_D2F_switch` ×1, M3×16 SHCS ×2, `[a]_tensioner_left/right`, `[a]_cable_cover`, the unused cable bridge variant.

**Do:** Put the endstop pod and its two reserved M3×16 SHCS in one labelled bag, the Ch 07 tensioners and cable cover in another. Print the D2F pod only — this kit has no hall-effect endstops anywhere.

⚠ **Rev D+ / LDO:** *"Our kit includes the XY microswitch PCB, print [a]_endstop_pod_D2F_switch instead of [a]_endstop_pod_hall_effect."* [src](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d)

**Check:** Two labelled bags; nothing loose on the bench that Ch 06 or Ch 07 will need.

Source: [LDO printed-parts guide (Rev D)](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d) · CAD: Voron 2.4r2 STEP @ de7e89d

---

### Step 05.47 — Stop here: no belts, no squaring

![Voron manual p.107](assets/manual-pages/manual-p107.png)

**What you're looking at:** The gantry is complete as a mechanism and deliberately unfinished as a machine. Belts and squaring are held back because the official squaring procedure *begins* by releasing A/B belt tension — tension it now and Ch 06 simply undoes it.

**Parts:** none.

**Do:** The gantry is complete as a mechanism and deliberately unfinished as a machine. Do not cut, route or tension the A/B belts, do not tighten the XY joints "properly", and do not try to square the gantry on the bench. The official procedure squares it **in the frame, with A/B tension released and the lower Z joints dropped** — doing it now guarantees doing it twice. [src](https://docs.vorondesign.com/build/mechanical/v2_gantry_squaring.html)

**Check:** A/B belts still in their bag. XY joint bolts still only lightly tightened.

Source: [Voron manual p.107](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=107) · [Voron docs § V2 Gantry Squaring](https://docs.vorondesign.com/build/mechanical/v2_gantry_squaring.html)

---

### Step 05.48 — Log it and photograph it

(no image — see text)

**What you're looking at:** The paperwork you will want in Ch 06. The rail overhangs are the evidence that each rail is centred; the two Y-to-Y spacings are the baseline you measure against once the gantry has been squared in the frame.

**Parts:** camera.

**Do:** Photograph the assembled gantry from above and from each end, plus a close-up of each backer showing which face it is on, and one of the right XY joint with the cable bridge. Record the rail overhangs you measured (Y and X, both ends) and note anything you left deliberately loose.

| Measurement | Target | Yours | Notes |
|---|---:|---|---|
| Y rail overhang, extrusion 1 — end A / end B | 25 / 25 mm | | |
| Y rail overhang, extrusion 2 — end A / end B | 25 / 25 mm | | |
| X rail overhang — end A / end B | 15 / 15 mm | | |
| Inside Y-to-Y spacing at the bridge | — | | |
| Inside Y-to-Y spacing at the idlers | = at bridge | | |
| M3×16 SHCS remaining for the endstop pod | 2 | | |

**Check:** Numbers written down, not "looked fine". You will want the Y-to-Y spacings when the gantry is squared in Ch 06.

---

## Checkpoint 05

- [ ] E extrusion joined to both drive units with 8× M5×10 BHCS; drives parallel, no twist
- [ ] Both MGN9 rails centred and tightened, first screw in the **second hole** from each end, overhang equal at both ends
- [ ] MGN12 rail centred and tightened, second hole in, overhang equal at both ends
- [ ] Every carriage retained by a stopper or tape; none dropped
- [ ] Three M5 and one M3 T-nut pre-loaded at each of the four C-extrusion ends
- [ ] **Titanium backers on the face opposite the rail** — top of both Y extrusions, rear of the X extrusion — flat, all screws seated, none cammed out
- [ ] Both front idlers and both rear drive joints flush with the extrusion ends, notches pointing away from the assembly
- [ ] Both XY joints: 3 M5 nuts, 4 M5×40 SHCS, 2 F695, 1 precision spacer, 1 free-spinning 20T idler
- [ ] Cable bridge fitted to the **right** XY joint with M5×16 BHCS; left joint on M5×10
- [ ] M5×30 BHCS with **black M5 washers** underneath, both lightly tightened
- [ ] XY joints bolted to the Y carriages: 4 bolts one side, 2 the other, **2× M3×16 SHCS bagged** with the endstop pod
- [ ] X axis runs the full Y travel with no tight spot
- [ ] A/B belts still unopened; nothing squared, nothing torqued down

## Common mistakes

- **Fitting the backers after the gantry is built.** Their T-nut slots are capped by the idler and drive frames, and the backer face is buried once the gantry is in the frame. It is a ~3 h teardown to fix (survey §5.2 W2).
- **Putting the X backer on top of the X extrusion.** With a single MGN12 on the front face, a top backer adds to the bimetallic bow instead of cancelling it, and it blocks the top slot the XY joints and cable bridge bolt into.
- **Using the rails' end holes.** The manual only forbids it on 300 mm builds; LDO forbids it on all of them, because the end holes sit exactly where the M5/M3 T-nuts of p.89–90 and p.102 have to live. Caught late, the rail comes off and goes back on.
- **Forgetting the reserved T-nuts at p.90.** Nothing in this chapter uses them, so they are easy to skip — and Ch 06's Z joints and Ch 10's chain hardware then have nowhere to bolt to. Count three M5 + one M3 per end before the idlers go on.
- **Torquing the XY joints and "squaring" on the bench.** The joints are meant to stay slightly loose and the gantry is squared in the frame with the belts slack. Tightening now, or tensioning belts now, costs a full de-tension in Ch 07 (survey §5.2 W1).
- **Over-tightening the 20T idler bolts.** They thread straight into plastic and only locate the idler. Crushed pockets show up later as belt noise you will blame on tension.

## Next

Ch 06 — Z axis: gantry install, Z belts and gantry squaring (manual p.108–123, plus the official 16-step squaring procedure); gated on batch **B05** (Z joints + Z chain, 1 plate, 5.2 h) — start it now if it is not already printed. Keep the rubber rail stoppers: LDO uses them under the Z joints to rest the gantry during install.

Source: [survey §7.5](../voron-build-instructions-survey.md) · [Voron manual p.107](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=107)

Pause: ~25 min since the last pause — gantry complete, measurements written down, photographs taken, Ch 06/07 parts bagged and labelled. Do not tension belts and do not square the gantry: both are Ch 06/07 and both would be undone.
