# Chapter 09 — Electronics bay

Fits out the space under the deck panel: two DIN rails and five wire ducts, the Meanwell 24 V PSU, the Omron SSR, the Leviathan mainboard carrying the Raspberry Pi 4B, the Nitehawk USB adapter, the mains inlet and WAGO blocks, and both endstops. Everything is mounted and nothing is wired — that unlocks Ch 10, which is one continuous harness job ending at Checkpoint #1.

**Time:** 2.5–4.0 h hands-on, first build (survey §7.2).

**Prerequisites:**
- **Ch 01–03.** Frame squared, deck panel and deck supports in (manual p.28–30), build plate on with its three cables hanging free below the deck.
- **Ch 06.** Gantry installed — step 09.33 mounts the XY endstop pod to it.
- **Batch B7 — Electronics bay + lighting.** The COB light-strip mounts on plate B7-P2 are *not* consumed here; they are Ch 10.
- **Batch B8, plate B8-P6 — `power_inlet_IECGS_1mm`.** The print plan groups the inlet panel with the skirts (B8), but the manual fits it at p.156/167, i.e. in this chapter. Print B8-P6 (or at least that one part) before you start, or steps 09.10–09.12 stall.
- **Batch B0 heat-set pass.** The inlet panel and the bed WAGO mount both need inserts before assembly (survey §5.2 W3).

**Tools**
- 2.5 mm flat-blade screwdriver (supplied — this is the tool for every plug-type terminal in the bay)
- PH1 (M2 self-tapping) and PH2 (PSU and SSR terminals) screwdrivers
- Hex 2 / 2.5 / 3 mm
- Soldering iron + brass M3 heat-set tip
- Hacksaw or fine-tooth saw + file (DIN rail), side cutters or a fine saw (wire duct)
- Steel rule ≥300 mm, marker, digital caliper
- Multimeter (used properly in Ch 10; keep it on the bench from now on)

**Consumables:** 3M VHB tape (supplied, for the wire ducts), IPA + lint-free cloth, masking tape and marker for labelling.

**Printed parts**

| STL | Qty | Colour |
|---|---|---|
| `Electronics_Bay/lrs_200_psu_bracket_x2` | 2 | Black |
| `Electronics_Bay/wago_221-415_mount_3by5` | 1 | Black |
| `Electronics_Bay/pcb_din_clip_x3` | 1 file = 3 clips (spares — kit supplies 4) | Black |
| `Electronics_Bay/PSU_stabilizer_50mm` | 1 — **fit only if needed**, see 09.16 | Black |
| `Nitehawk-SB-V2/usb_adapter_mount_partial_cover` | 1 | Black |
| `Skirts/power_inlet_IECGS_1mm` | 1 (batch B8-P6) | Black |

**Supplied printed by LDO — do not print these:** Leviathan Bracket Left ×1, Leviathan Bracket Right ×1, NH Adapter Mount ×1, DIN Clip ×4, LDO Nozzle Probe ×1, Bed WAGO Mount ×1. [src](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)

**Hardware** (chapter totals)

| Fastener / part | Qty | Note |
|---|---|---|
| DIN rail, 35 mm W, slotted | 2 | length not stated by the manual or LDO — **(verify on bench)** |
| DIN rail plastic end cap | 4 | 2 per rail |
| PVC wire duct, 20 W × 25 H | 5 | 3 across, 2 front-to-back; cut lengths **(verify on bench)** |
| M5×10 BHCS | 8 | 4 DIN rails, 2 mains WAGO mount, 2 bed WAGO mount |
| M5 T-nut | 8 | same three groups **(verify on bench for the bed WAGO mount)** |
| M4×6 BHCS | 6 | 4 PSU brackets **(verify)**, 2 SSR to its metal bracket |
| M3×8 SHCS | 8 | 4 Leviathan to brackets **(verify)**, 2 inlet panel, 2 XY endstop PCB |
| M3×6 BHCS | 2 | 2×2 XH splicer PCB to the bed WAGO mount |
| M3×10 FHCS | 2 | IEC inlet module into the printed panel **(verify on bench)** |
| M3×25 SHCS | 2 | nozzle probe to the bed extrusion — **not** the manual's M3×20 |
| M3×30 SHCS | 2 | XY endstop pod to the gantry |
| M3 T-nut | 4 | 2 inlet panel, 2 nozzle probe |
| M2×10 self-tapping | 6+ | 4 DIN clips to Leviathan brackets, 2 Z endstop PCB; USB adapter mount **(verify on bench)** |
| M3×5×4 heat-set insert | 2+ | 2 bed WAGO mount; inlet panel and mains WAGO mount **(verify on bench)** |
| Meanwell LRS-200-24 PSU | 1 | 115/230 V selector switch on the side |
| Omron G3NB-210B-1 SSR + metal DIN mount bracket | 1 + 1 | bracket is off-the-shelf metal; there is no printed SSR mount |
| AC inlet, integrated switch & fuse | 1 | one module — not the manual's separate inlet + rocker |
| WAGO 221-415 (5-way) | 3 | mains distribution, L / N / PE |
| WAGO 221-412 (2-way) | 2 | bed WAGO mount |
| Ferrule, VE0508 | 5 | fitted in Ch 10, counted here so you can find them |
| LDO Leviathan mainboard | 1 | |
| Raspberry Pi 4B + heatsink + standoffs + 3/4 HAT power adapter | 1 set | Pi is a reseller-optional line item |
| XY endstop PCB / Z endstop PCB / USB adapter PCB / 2×2 XH splicer PCB | 1 each | |
| GT2 20-tooth pulley + 5 mm shaft + M3 set screw | 1 each | nozzle probe |

**Read first**
- **Remove *every* voltage-selection jumper from the Leviathan before it goes anywhere near the rail** (step 09.19). Mixing voltages on the shared 24 V supply permanently destroys the controller and whatever is plugged into it. Jumpers go back in Ch 10, one at a time, after each component's voltage is confirmed. [src](https://ldomotion.com/guides/voron-leviathan-v1-3)
- **Nothing is wired in this chapter.** Mains wiring is the one step in this build that can kill you, and it is done as one deliberate sequence in Ch 10 that ends at LDO's **Checkpoint #1** — continuity within each colour group, no continuity between L, N and PE, PSU selector confirmed, all with the cord unplugged. Leave the C13 cord in its bag. (survey §4.4 #8)
- **The manual pages p.148–172 describe a different machine** — a BTT Octopus, a mini12864, a 5 V PSU and a separate Pi bracket. Use them for the DIN-rail technique and the mounting geometry only; every part that differs carries a ⚠ callout at its step. [src](https://docs.ldomotors.com/voron/voron2/build-faq)
- **Do not close the bay.** Skirts and the bottom panel go on in Ch 11, only after Checkpoint #1 passes. Fitting them now costs an hour of re-opening plus the safety check you skipped (survey §5.2 W8).
- **Test-fit every roll-in T-nut.** Extrusion and T-nut tolerances on this kit are tight; a forced nut galls the slot. [src](https://docs.ldomotors.com/voron/voron2/build-faq)

---

### Step 09.1 — Read the end state

![Voron manual p.148](assets/manual-pages/manual-p148.png)

**Parts:** none.

**Do:** Look at the render. Two DIN rails run across the bay; boards clip onto one, power onto the other. That geometry is correct for your kit even though three of the four components pictured are wrong. Nothing here is fastened to the acrylic itself except the wire ducts.

**Check:** You can name the two rails and say which components go on each before you start cutting.

---

### Step 09.2 — Read the placement you are actually building

![Voron manual p.149](assets/manual-pages/manual-p149.png)

**Parts:** none.

**Do:** Compare the manual's overview against LDO's Rev D placement photo, [`S0General_Placement.jpg`](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/RevD/S0General_Placement.jpg). Front rail: Leviathan with the Pi mounted on it, plus the USB adapter at the right-hand end. Rear rail: Omron SSR at the left, Meanwell LRS-200-24 to its right with its terminal block facing the SSR. Rear-left corner of the frame: mains WAGO block. Rear centre: the IEC inlet.

**Check:** You have that photo open on a phone or second screen. You will check the finished bay against it at 09.36.

⚠ **Rev D+ / LDO:** the manual shows a **Raspberry Pi on its own bracket**, a **BTT Octopus**, and a **5 V PSU**. Your kit has none of those: the Pi mounts *on* the Leviathan, the Leviathan replaces the Octopus, and there is no 5 V PSU at all — the Leviathan supplies the Pi's 5 V. [src](https://docs.ldomotors.com/voron/voron2/build-faq) · [wiring guide § General Placement](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#general-placement)

---

### Step 09.3 — Turn the printer over and pre-load the rear T-nuts

![Voron manual p.166](assets/manual-pages/manual-p166.png)

**Parts:** M3 T-nut ×2.

**Do:** Take the flex plate off and put it away, lay a folded blanket on the bench, and turn the printer onto its top with two people — a 350 with a gantry and a 10 mm plate in it is heavy and top-corner-fragile. Support the gantry so it cannot slam down its Z travel. With the bay now facing up, drop two M3 roll-in T-nuts into the inner slot of the **rear lower extrusion**, roughly where the inlet panel will sit (rear centre-left), and leave them loose.

**Check:** Printer sits stable and level on its top; no load on the gantry, motors or belts. Two M3 T-nuts free to slide in the rear extrusion slot.

---

### Step 09.4 — Verify the deck panel before you drill anything into the layout

![Voron manual p.28](assets/manual-pages/manual-p028.png)

**Parts:** deck panel ×1 (already fitted in Ch 02).

**Do:** Confirm the panel's **notch faces the back** and that the round wire opening near the rear centre is clear. Caliper the panel edge and write the number down — the Rev D 350 BOM lists 469 × 469 × **3 mm** while LDO's own guide assumes a 4 mm deck, and the deck supports must match what you measured (survey §4.3).

**Check:** Notch to the back. Wire opening unobstructed. Deck thickness recorded, and the deck supports fitted in Ch 02 are the matching variant.

⚠ **Rev D+ / LDO:** if Ch 02 fitted `deck_support_4mm_x8` and your panel calipers at 3 mm, swap them for `deck_support_3mm_x8` now — the deck is about to carry the DIN rails and everything on them. [src](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)

---

### Step 09.5 — Fit the two DIN rails, running left to right

![Voron manual p.29](assets/manual-pages/manual-p029.png)

**Parts:** DIN rail ×2, DIN rail plastic end cap ×4, M5×10 BHCS ×4, M5 T-nut ×4.

**Do:** Slide the four M5 T-nuts along the two bed extrusions so that each rail crosses **both** extrusions and picks up one T-nut in each. Position one rail toward the front of the bay and one toward the rear, leaving room between them for a wire duct. Bolt through the rail slot and the deck panel into the T-nut with M5×10 BHCS, snug only. Push a plastic end cap onto each of the four rail ends.

**Check:** Both rails parallel, running left–right, each held by two screws. Rails do not overhang the deck panel or foul the Z belts or the gantry's lowest travel. All four end caps on.

⚠ **Rev D+ / LDO:** the manual runs the rails **front-to-back**, each rail bolted twice into the same extrusion. LDO runs them **left-to-right**: *"These DIN rails run from left to right."* Follow LDO — the Leviathan, the PSU and the SSR are all laid out for that orientation. Same four screws and T-nuts either way; just slide the T-nuts to suit. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#installing-the-din-rails-and-wire-ducts)

⚠ **Rev D+ / LDO:** neither the manual nor LDO publishes a **cut length** for a 350's rails — **(verify on bench)**. Cut both to the same length, keep them inside the deck panel, and use the manual's own escape hatch at p.29: if a rail slot does not land on a T-nut, shorten the rail by a few mm rather than moving the nut off the extrusion.

---

### Step 09.6 — Cut and stick the five wire ducts

![LDO Rev D — DIN rails and wire ducts](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/RevD/S0_Din_Raill.jpg)

**Parts:** PVC wire duct 20 W × 25 H ×5, VHB tape.

**Do:** Cut three ducts to run left–right — one in front of the front rail, one between the two rails, one behind the rear rail — and two to run front-to-back down the left and right sides of the bay, joining the three. Dry-lay all five first. Wipe the deck with IPA, then VHB the ducts down. Put the rear duct **below the deck's wire opening**, not across it.

**Check:** Five ducts, no duct crossing the wire opening, none fouling a DIN rail or the components you are about to clip on. Every duct still has its snap-on lid (they go on in Ch 10, after wiring).

⚠ **Rev D+ / LDO:** duct lengths are not published — **(verify on bench)**. Cut to fit between the side runs and the frame, and leave the offcuts: Ch 10 uses short pieces to bridge gaps. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#installing-the-din-rails-and-wire-ducts)

---

### Step 09.7 — Learn the DIN clip motion once

![Voron manual p.168](assets/manual-pages/manual-p168.png)

**Parts:** one spare printed `pcb_din_clip` ×1.

**Do:** Practise on a spare clip. Hook the **fixed** side of the clip over one edge of the rail, rotate the part down flat while keeping that hook engaged, then press until the sprung side snaps over the other edge. Every clipped component in this chapter goes on this way.

**Check:** The clip sits square on the rail, does not rock, and slides along the rail with firm thumb pressure but not under its own weight.

---

### Step 09.8 — Do not build the Pi bracket

![Voron manual p.150](assets/manual-pages/manual-p150.png)
![Voron manual p.151](assets/manual-pages/manual-p151.png)

**Parts:** none.

**Do:** Skip both pages. Put the Pi aside for step 09.22.

**Check:** No `raspberrypi_bracket` or `beefy_raspberry_bracket` in your printed-parts bin — the print plan deliberately never printed them.

⚠ **Rev D+ / LDO:** **SKIP manual p.150–151.** LDO's note on p.150 points at the Beefy Raspberry Pi Mount and then says *"it does not apply for rev D kits"* — the Leviathan has a dedicated Pi mounting area with its own standoffs. [src](https://docs.ldomotors.com/voron/voron2/build-faq)

---

### Step 09.9 — Do not fit a 5 V PSU

![Voron manual p.152](assets/manual-pages/manual-p152.png)
![Voron manual p.172](assets/manual-pages/manual-p172.png)

**Parts:** none.

**Do:** Skip both pages. There is no RS25-5 in the kit and no space allocated for one.

**Check:** Your bay plan has exactly one power supply in it.

⚠ **Rev D+ / LDO:** **SKIP manual p.152 and p.172** — *"The kit does not use a 5V PSU."* The Leviathan supplies the Pi's 5 V through the GPIO power adapter fitted at 09.23. This also removes manual p.190 later in the build. [src](https://docs.ldomotors.com/voron/voron2/build-faq)

---

### Step 09.10 — Heat-set the power inlet panel

![Voron manual p.156](assets/manual-pages/manual-p156.png)

**Parts:** `power_inlet_IECGS_1mm` ×1, M3×5×4 heat-set inserts **(verify on bench — count the bosses on your printed part)**.

**Do:** Set the iron to your ASA insert temperature and press one insert into each boss on the back of the panel, square and flush with the surface. Let it cool completely before you touch anything to it.

**Check:** Every insert flush or a hair below, none tilted, no bulged plastic around a boss.

⚠ **Rev D+ / LDO:** the manual's part is `power_inlet_filtered`. Yours is **`power_inlet_IECGS_1mm`** — LDO ships the **1.0 mm AC inlet with an integrated switch**, so the printed panel is a different file with a different cut-out. [src](https://docs.ldomotors.com/voron/voron2/build-faq) · [Rev D printed parts guide](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d)

---

### Step 09.11 — Fit the combined IEC inlet module

![LDO Rev D — inlet fitted](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/RevD/S2_inlet.jpg)

**Parts:** AC inlet with integrated switch & fuse ×1, M3×10 FHCS ×2 **(verify on bench)**.

**Do:** Press the inlet module into the panel from the outside so the earth pin is at the top when the printer is upright and the switch faces out. Fasten with M3×10 FHCS into the inserts. Do not connect anything to its spade terminals — the pre-wired inlet cable lands in Ch 10.

**Check:** Module square in the panel, no rocking, fuse drawer accessible, switch rocks freely. Nothing wired.

⚠ **Rev D+ / LDO:** the manual fits **two** parts here — a filtered inlet *and* a separate rocker switch. Your kit is **one module** containing inlet, switch and fuse. Ignore the manual's switch. Confirm the module's factory wiring against LDO's [inlet layout diagram](https://docs.ldomotors.com/v01_wire_guide/inlet_layout.png): wired correctly, the live conductor is fused and the switch lights when on. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#preparing-the-inlet)

---

### Step 09.12 — Mount the inlet panel to the rear extrusion

![Voron manual p.167](assets/manual-pages/manual-p167.png)

**Parts:** M3×8 SHCS ×2, the two M3 T-nuts pre-loaded at 09.3.

**Do:** Slide the panel over the rear extrusion so its lip hooks the slot, line the two holes up with the T-nuts and drive M3×8 SHCS in. Position it rear-centre-left, clear of the Z motor mount, and leave enough room to the left for the WAGO block.

**Check:** Panel flat against the extrusion, no gap at the lip. Panel does not overhang where the rear skirt will land in Ch 11. Inlet reachable from outside.

---

### Step 09.13 — Build and mount the mains WAGO block

![Voron manual p.165](assets/manual-pages/manual-p165.png)

**Parts:** `wago_221-415_mount_3by5` ×1, WAGO 221-415 (5-way) ×3, M5×10 BHCS ×2, M5 T-nut ×2.

**Do:** Snap the three 5-way WAGO 221-415 clamps into the printed mount, levers facing outward so you can reach them with the bay open. Slide two M5 T-nuts into the rear extrusion just left of the inlet panel, hook the mount over the slot and fasten with M5×10 BHCS.

**Check:** All three clamps fully seated (no visible step between clamp and mount), every lever free to lift, mount solid on the extrusion and within reach of the inlet's flying leads.

⚠ **Rev D+ / LDO:** the manual titles p.165 *"ALTERNATE MAINS DISTRIBUTION — WAGO"*. For this kit it is not an alternate — it is the only path. The BOM ships three 221-415 clamps, and Ch 10 uses them as the L / N / PE distribution nodes. [src](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)

⚠ **Rev D+ / LDO:** if your printed mount has insert bosses, heat-set them in the same pass as 09.10 — **(verify on bench)**; the stock Voron part is snap-fit only.

---

### Step 09.14 — Set the PSU voltage selector to 115 V

![LDO — PSU voltage selector switch](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/psu_switch.jpg)

**Parts:** Meanwell LRS-200-24 ×1.

**Do:** Find the small recessed slide switch on the side of the PSU next to the yellow warning label. Push it to **115 V** for US mains with the 2.5 mm flat screwdriver. Photograph the switch position now, while it is still easy to see — once the PSU is on the rail with a duct in front of it, it is not.

**Check:** Selector reads 115 V (some units print 115, some 120 — either marking is the low-voltage position). Yellow label on the PSU says *"AC INPUT VOLTAGE CAN BE SELECTED BY SWITCH, CHECK INPUT VOLTAGE AVOIDING DAMAGE BEFORE POWER ON"* — you have just done that.

⚠ **Rev D+ / LDO:** LDO calls this out twice, in *Preparing the Power Supply Unit* and again in Checkpoint #1: *"Flick the switch to the correct value before powering it on! Failing to do so can destroy the power supply!"* Ch 10 re-checks it before the first power-on. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#preparing-the-power-supply-unit)

Tip: EU builds may get a Meanwell RSP-200-24 instead, which has PFC and a universal input and no switch at all. If yours has no selector, you have that unit — nothing to set. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#preparing-the-power-supply-unit)

---

### Step 09.15 — Fit the printed DIN brackets to the PSU

![Voron manual p.153](assets/manual-pages/manual-p153.png)

**Parts:** `lrs_200_psu_bracket_x2` ×2, M4×6 BHCS ×4 **(verify on bench)**.

**Do:** Sit the two printed brackets on the PSU's long face — the one *without* the vents — using the factory M4 threaded holes, and drive M4×6 BHCS. Both brackets must face the same way so their DIN hooks line up. Do not use longer screws: an M4 that reaches inside a 200 W PSU is a short circuit.

**Check:** Both DIN hooks parallel and coplanar; the PSU's screw terminal block is on the edge that will face the SSR, i.e. to the left. Rest the PSU on a spare rail offcut and confirm both hooks engage at once.

⚠ **Rev D+ / LDO:** the manual's "24 V PSU" here is a generic block. Yours is the **Meanwell LRS-200-24** and these two printed brackets are the *whole* mounting system for it. [src](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)

---

### Step 09.16 — Clip the PSU onto the rear rail

![Voron manual p.169](assets/manual-pages/manual-p169.png)

**Parts:** PSU assembly from 09.15.

**Do:** Hook, rotate and snap the PSU onto the **rear** DIN rail (top-left render on p.169), positioned toward the right of the bay with its terminal block facing left. Slide it until the terminal block is clear of the right-hand vertical wire duct and you can get a PH2 driver squarely onto every terminal screw.

**Check:** PSU sits square with both brackets latched; it does not rock when you push a screwdriver against a terminal. Vented face clear of ducts and the deck. Terminal block accessible without removing anything.

⚠ **Rev D+ / LDO:** **SKIP the bottom half of p.169** — the L-shaped support bracket with its M5 T-nut, M5×10 BHCS and M4×6 BHCS. LDO: *"PAGE 169 SKIP. The kit does not use a support bracket."* The two printed DIN brackets carry the PSU on their own. [src](https://docs.ldomotors.com/voron/voron2/build-faq)

⚠ **Rev D+ / LDO:** the print plan prints `PSU_stabilizer_50mm` anyway as a 4 g insurance part. Fit it **only** if the PSU visibly sags or rocks on the rail; otherwise it stays in the spares bin. [src](../voron-print-plan.md) §6

---

### Step 09.17 — Fit the SSR to its metal DIN bracket

![Voron manual p.157](assets/manual-pages/manual-p157.png)

**Parts:** Omron G3NB-210B-1 SSR ×1, metal DIN rail mount bracket ×1, M4×6 BHCS ×2.

**Do:** Find the stamped metal bracket in the hardware bags — there is no printed SSR mount anywhere in this build. Lay the SSR on it and drive the two M4×6 BHCS through the SSR's mounting ears into the bracket. Before you tighten, read the SSR's own label and note which pair of terminals is which: **1 / 2 = LOAD, 24–220 VAC 10 A**; **3 + / 4 − = INPUT, 5–24 VDC**, with the indicator LED next to terminal 3.

**Check:** SSR square on the bracket, both screws tight, spring latch on the back of the bracket free to move. You can state from memory which pair is load and which is control.

---

### Step 09.18 — Clip the SSR onto the rear rail

![Voron manual p.171](assets/manual-pages/manual-p171.png)

**Parts:** SSR assembly from 09.17.

**Do:** Use the 2.5 mm flat screwdriver to pull the bracket's spring latch open — it locks in the open position. Hook the bracket over the rear rail to the **left of the PSU**, then release the latch. Mind your fingers: it snaps back hard. Orient the SSR so the **INPUT (3 + / 4 −)** terminals face the front rail, where the Leviathan's DC control wire comes from, and the **LOAD (1 / 2)** terminals face the rear, toward the inlet and WAGO block.

**Check:** SSR latched, square, no rocking. Both terminal pairs reachable with a PH2 driver. Roughly 30 mm of clear rail between the SSR and the PSU so both sets of screws can be driven.

⚠ **Rev D+ / LDO:** the SSR body is stamped **"EARTH THE MOUNTING RAIL"**. Your DIN rails bolt through the deck panel into the aluminium bed extrusions (09.5), so they are earthed once the frame PE lands in Ch 10. Verify rail-to-frame continuity with the multimeter at Checkpoint #1 — do not assume it. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#checkpoint-1)

Tip: the SSR wiring is the one connection LDO flags as *"critical — an incorrect connection can cause catastrophic damage"*. Getting the orientation right now is what makes Ch 10 unambiguous (survey §4.4 #8).

---

### Step 09.19 — Strip every voltage-selection jumper off the Leviathan

(no image — the LDO step images are link-only: [Leviathan V1.3 § Voltage Selection](https://ldomotion.com/guides/voron-leviathan-v1-3))

**Parts:** LDO Leviathan mainboard ×1, a small pot or bag for the jumpers.

**Do:** On the bench, on an anti-static surface, pull **all** of the voltage-selection jumpers — the four fan headers and the Z-probe voltage header — and put them in a labelled bag taped to the bay wall. Do this before the board goes on the rail, not after.

**Check:** Zero jumpers left in any voltage-selection header. Bag labelled and stored where Ch 10 will find it.

⚠ **Rev D+ / LDO:** LDO's rule, verbatim: *"Remove all of the jumpers used for voltage selection prior to installation."* and *"Mixing voltage will permanantly damage the controller and attached components."* Jumpers go back only in Ch 10, one component at a time, after each attached device's voltage is verified. [src](https://ldomotion.com/guides/voron-leviathan-v1-3)

⚠ **Rev D+ / LDO:** ignore manual p.174–178 entirely when you get there — that is Octopus jumper configuration. LDO: *"Follow the instruction in the LDO guide for configuring the Leviathan controller board."* [src](https://docs.ldomotors.com/voron/voron2/build-faq)

---

### Step 09.20 — Fit DIN clips to the two Leviathan brackets

![Voron manual p.154](assets/manual-pages/manual-p154.png)

**Parts:** Leviathan Bracket Left ×1, Leviathan Bracket Right ×1 (both LDO-supplied printed), DIN Clip ×2, M2×10 self-tapping ×4.

**Do:** Sit a DIN clip on each bracket and drive two M2×10 self-tapping screws through the clip into the bracket with a PH1. Self-tappers cut their own thread in ASA — go slowly, stop the moment the head seats, and do not run them in and out repeatedly.

**Check:** Two bracket-and-clip assemblies, mirror images of each other, clips square and both hooks facing the same direction.

⚠ **Rev D+ / LDO:** p.154 shows the **Octopus** bracket set and its siblings. You use `Leviathan_bracket_set` — supplied printed by LDO, do not print it — with **two** DIN clips. The assembly method on this page is the same; only the parts differ. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#preparing-the-mainboard-ldo-voron-leviathan-board)

---

### Step 09.21 — Bolt the Leviathan to its brackets

![Voron manual p.155](assets/manual-pages/manual-p155.png)

**Parts:** Leviathan ×1, the two bracket assemblies from 09.20, M3×8 SHCS ×4 **(verify on bench)**.

**Do:** Lay the Leviathan face down on a clean anti-static surface. Set a bracket under each short end, line up the PCB's corner mounting holes and drive M3×8 SHCS — finger-tight plus a nudge. Over-torquing an M3 into a PCB corner cracks the board.

**Check:** Board flat on both brackets with no twist; the two DIN hooks are coplanar. Rest the assembly on a rail offcut — both clips must engage together.

⚠ **Rev D+ / LDO:** the manual's board is a dummy Octopus fastened with **M3×6 BHCS**. The Leviathan takes **M3×8 SHCS** through the LDO brackets. Confirm the screw seats without bottoming out before you drive all four. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#preparing-the-mainboard-ldo-voron-leviathan-board)

---

### Step 09.22 — Heatsink and mount the Raspberry Pi 4B on the Leviathan

![LDO Rev D — general placement](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/RevD/S0General_Placement.jpg)

**Parts:** Raspberry Pi 4B ×1, Pi heatsink ×1, Leviathan standoffs (supplied with the board) **(verify on bench — typically 4)**, 32 GB SD card ×1.

**Do:** Stick the heatsink on the Pi's SoC first — you cannot get at it once the Pi is on the board. Screw the standoffs into the Leviathan's dedicated Pi mounting area, then sit the Pi on them with its USB and Ethernet ports facing **outward, away from the Leviathan's connector banks**, and fasten. Slide the SD card in now; it is far easier here than on the rail.

**Check:** Pi flat on all standoffs, no flex. Ethernet and at least one USB-A port clear of the Leviathan's headers. SD card seated. Nothing shorting between the Pi's underside and the Leviathan.

⚠ **Rev D+ / LDO:** *"Some ports of the Raspberry Pi may not be usable due to interference with the Leviathan ports."* Check which ones you lose **now**, while you can still rotate the Pi, because Ch 10 needs the Ethernet port and Ch 12 needs a USB port for the toolboard. [src](https://ldomotion.com/guides/voron-leviathan-v1-3)

---

### Step 09.23 — Fit the Raspberry Pi 3/4 HAT power adapter

(no image — LDO's adapter photos are link-only: [Leviathan V1.3 § Raspberry Pi Mounting](https://ldomotion.com/guides/voron-leviathan-v1-3))

**Parts:** Raspberry Pi **3/4** HAT power adapter ×1.

**Do:** Seat the 3/4-version adapter onto the Pi's GPIO header in the orientation LDO's image shows, and connect its lead to the Leviathan's dedicated Raspberry Pi supply port. This is how the Pi gets its 5 V — there is no USB-C brick and no 5 V PSU in this machine.

**Check:** Adapter fully seated on the GPIO pins with no row offset. Lead reaches the Leviathan's Pi power port without tension.

⚠ **Rev D+ / LDO:** the kit ships adapters for both **Pi 5** and **Pi 3/4**, and *"the orientation differs"* between them. You have a Pi 4B — use the 3/4 adapter. Fitting the Pi 5 adapter to a Pi 4 puts supply on the wrong pins. [src](https://ldomotion.com/guides/voron-leviathan-v1-3)

⚠ **Rev D+ / LDO:** this replaces manual p.190 as well (*"the kit uses the Leviathan to supply the 5v power for the Raspberry PI"*). [src](https://docs.ldomotors.com/voron/voron2/build-faq)

---

### Step 09.24 — Clip the Leviathan and Pi onto the front rail

![Voron manual p.170](assets/manual-pages/manual-p170.png)

**Parts:** Leviathan + Pi assembly.

**Do:** Hook, rotate and snap the assembly onto the **front** DIN rail, roughly centred left-to-right but biased left so the right-hand end of the rail is free for the USB adapter. Keep the Leviathan's high-current terminal block on the side facing the PSU.

**Check:** Both clips latched, board square, and no part of the Pi or the Leviathan touching a wire duct, the deck panel or the frame. You can reach every connector bank with the bay open.

⚠ **Rev D+ / LDO:** **SKIP the manual's arrangement on p.170–171.** LDO: *"Refer to the wiring guide for Leviathan and electronics general placement."* The manual puts a Pi and an Octopus on the same rail as separate items; you have one clipped assembly. [src](https://docs.ldomotors.com/voron/voron2/build-faq)

---

### Step 09.25 — Build the USB adapter mount

(no image — the Nitehawk-SB V2 repo has no licence file, so link only: [`usb_adapter_gnd.jpg`](https://raw.githubusercontent.com/MotorDynamicsLab/Nitehawk-SB-V2/master/Images/usb_adapter_gnd.jpg))

**Parts:** NH Adapter Mount ×1 (LDO-supplied printed), USB adapter PCB ×1, `usb_adapter_mount_partial_cover` ×1 (you printed it), DIN Clip ×1, M2×10 self-tapping **(verify on bench)**.

**Do:** Sit the USB adapter PCB in the LDO-supplied mount base, fit a DIN clip to the back of the base, then fit the **partial** cover — the one whose cut-out deliberately leaves a mounting point exposed. Attach the supplied grounding cable's ring terminal to that exposed point. Leave the free end of the ground lead loose.

**Check:** PCB captive, Micro-Fit 3.0 socket and USB connector both accessible, cover on, and one mounting point still bare with the ground ring terminal on it.

⚠ **Rev D+ / LDO:** print-plan batch B7 lists the **V1** `usb_adapter_mount.stl`. Rev D+ needs [`usb_adapter_mount_partial_cover.stl`](https://raw.githubusercontent.com/MotorDynamicsLab/Nitehawk-SB-V2/master/STLs/usb_adapter_mount_partial_cover.stl) from the Nitehawk-SB-V2 repo — *"a newly designed cover exposes one of the mounting points to connect a grounding point."* If you printed the V1 cover, reprint the partial cover (a few minutes) rather than omitting the ground. (survey §4.1 ⑤)

⚠ **Rev D+ / LDO:** use the **supplied** grounding cable. LDO: *"Be sure to use the supplied grounding cable since using larger O ring connectors may cause inadvertent shorting of the PCB boards."*

---

### Step 09.26 — Clip the USB adapter to the front rail

(no image — see text; position matches the right-hand end of the front rail in [`S0General_Placement.jpg`](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/RevD/S0General_Placement.jpg))

**Parts:** USB adapter assembly from 09.25.

**Do:** Clip it onto the **right-hand end of the front DIN rail**, beside the Leviathan, with the umbilical connector facing where the cable chain drops into the bay. Route the ground lead toward the nearest frame extrusion and leave it hanging — it terminates on the frame during Ch 10's PE step.

**Check:** Adapter latched and square. Umbilical socket points at the chain entry, not at a wire duct. Ground lead reaches a frame extrusion with slack.

⚠ **Rev D+ / LDO:** this is the Rev D+ ESD path: extruder motor body → toolboard → umbilical → USB adapter → **frame/earth**. Skipping the frame end leaves the chain broken, and LDO ships this hardware with no written procedure — treat the repo images as the spec and ask in `#ldo_motors` if anything is ambiguous. (survey §4.1 ⑤)

---

### Step 09.27 — Press the 20-tooth pulley into the LDO nozzle probe

![Voron manual p.158](assets/manual-pages/manual-p158.png) ·
![LDO — Z endstop parts](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/z_stop_parts.jpg)

**Parts:** LDO Nozzle Probe printed part ×1 (LDO-supplied), GT2 20-tooth pulley ×1.

**Do:** Press the pulley fully into its seat in the printed body — it is an interference fit, so use steady thumb or vice pressure, not a hammer. It must bottom out.

**Check:** Pulley flush and square in the body, no gap under the flange, printed part not split.

⚠ **Rev D+ / LDO:** use LDO's own printed part, not the Voron `nozzle_probe.stl` — it is supplied printed in the kit and the print plan deliberately never printed either version. Ignore the manual's "remove flange & set screws" and lever-removal instructions: those are for a bare microswitch build. [src](https://docs.ldomotors.com/voron/voron2/build-faq)

---

### Step 09.28 — Fit the Z endstop PCB

![Voron manual p.160](assets/manual-pages/manual-p160.png) ·
![LDO — Z endstop assembled](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/z_stop_install_1.jpg)

**Parts:** Z endstop PCB (D2F switch board) ×1, M2×10 self-tapping ×2.

**Do:** Sit the PCB against the printed body so the D2F switch's plunger is under the pulley bore. Drive two M2×10 self-tapping screws **sideways** through the two holes in the D2F switch and into the printed part. PH1, slow, stop when seated.

**Check:** PCB solid, switch square under the bore, plunger free. Pressing the plunger gives a clean audible click and it returns fully.

⚠ **Rev D+ / LDO:** p.160 is titled *"ALTERNATE Z ENDSTOP"* in the manual — for this kit it is the only path. LDO: *"Use the LDO Z endstop printed part and PCB."* Note it is **two** screws through the switch, not the four the manual's render shows. There is nothing to solder — the PCB carries a connector. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#assembling-the-nozzle-probe)

---

### Step 09.29 — Fit the 5 mm shaft and its retaining set screw

![Voron manual p.159](assets/manual-pages/manual-p159.png)

**Parts:** 5 mm shaft ×1, M3 set screw ×1.

**Do:** Drop the 5 mm shaft down through the pulley bore so it rests on the switch plunger. Thread one set screw into the pulley's grub-screw hole until it just enters the shaft's notch — enough that the shaft cannot fall out, loose enough that it still slides up and down under its own weight.

**Check:** Lift the shaft and let go: it drops freely and clicks the switch. Turn the assembly upside down: the shaft does not fall out.

⚠ **Rev D+ / LDO:** LDO: *"Remember to install one set screw into the pulley, but do not overtighten it… it should not be so tight as to impede the shaft from freely moving up and down."* Follow **only** the 5 mm shaft part of p.159 — the soldered-connector half of the page does not apply to the PCB version. [src](https://docs.ldomotors.com/voron/voron2/build-faq)

---

### Step 09.30 — Turn the printer upright and mount the nozzle probe

![Voron manual p.161](assets/manual-pages/manual-p161.png) ·
![LDO — Z endstop installed](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/z_stop_final.jpg)

**Parts:** nozzle probe assembly, M3×25 SHCS ×2, M3 T-nut ×2.

**Do:** Before you flip: check that nothing in the bay is loose, no tool is lying on the deck, and the boards are latched. Turn the printer back onto its feet with two people. Slide two M3 T-nuts into the **rear bed extrusion**, hang the probe body under it and fasten with M3×25 SHCS. Slide it left/right so the shaft clears the build plate edge and sits under the gantry's path — roughly 1.5 mm of clearance to the bed, per the p.161 detail.

**Check:** Shaft does not touch the build plate anywhere in Y. Shaft still drops freely and clicks. Probe body square, screws snug, nothing fouling the bed's underside or its cables.

⚠ **Rev D+ / LDO:** the manual calls for **M3×20 SHCS**. LDO's nozzle probe needs **M3×25 SHCS ×2** — the printed body is thicker. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#assembling-the-nozzle-probe)

---

### Step 09.31 — Do not build the soldered X/Y microswitches

![Voron manual p.162](assets/manual-pages/manual-p162.png)

**Parts:** none.

**Do:** Skip the page. No wire is cut, stripped or soldered here.

**Check:** Your XY endstop is one PCB with one 4-pin JST-XH connector, not two loose microswitches with flying leads.

⚠ **Rev D+ / LDO:** **SKIP manual p.162** — *"The kit uses the X/Y Endstop PCB board."* Also skip the hall-effect option on p.163: this kit has no hall-effect endstops anywhere (LDO note on p.145). [src](https://docs.ldomotors.com/voron/voron2/build-faq)

---

### Step 09.32 — Fit the XY endstop PCB to the pod

![Voron manual p.163](assets/manual-pages/manual-p163.png)

**Parts:** `[a]_endstop_pod_D2F_switch` ×1 (orange, batch B2; fitted to the gantry in Ch 05), XY endstop PCB ×1, M3×8 SHCS ×2.

**Do:** Follow the **left-hand** option only. Seat the XY endstop board on the pod so both switches face the directions the toolhead and the frame will hit them, and fasten with two M3×8 SHCS.

**Check:** Board flat on the pod, both switches proud and clicking cleanly, connector accessible from below.

⚠ **Rev D+ / LDO:** LDO: *"Follow only the step for the XY Endstop board."* Ignore the hall-effect half of the page. [src](https://docs.ldomotors.com/voron/voron2/build-faq)

⚠ **Rev D+ / LDO:** check the cable labels before Ch 10. LDO documents a batch whose XY endstop cable is labelled *"X Stop / Y Stop"* instead of *"XES / YES"* and needs re-pinning. [XY endstop repin guide](https://docs.ldomotors.com/en/guides/XY_Endstop_Cable_Reconnecting_Guide)

---

### Step 09.33 — Mount the endstop pod to the gantry

![Voron manual p.164](assets/manual-pages/manual-p164.png)

**Parts:** pod assembly, M3×30 SHCS ×2.

**Do:** Hold the pod under the **right-hand XY joint** and drive two M3×30 SHCS up through it into the joint. If Ch 05 already fitted the pod, this step is: drop the two screws, fit the PCB from 09.32, and put the screws back.

**Check:** Pod solid with no rotation. Run the gantry through its full X and Y travel by hand — the pod must not foul the frame, a Z rail, the drag chain or the toolhead anywhere except where it is meant to be triggered.

---

### Step 09.34 — Build and mount the bed WAGO breakout

(image is on LDO's wiki and is link-only: [bed WAGO mount](https://docs.ldomotors.com/v2_wire_guide/bed_wago_mount.jpg))

**Parts:** Bed WAGO Mount ×1 (LDO-supplied printed), M3×5×4 heat-set inserts ×2, 2×2 XH splicer PCB ×1, M3×6 BHCS ×2, WAGO 221-412 (2-way) ×2, M5×10 BHCS ×2, M5 T-nut ×2 **(verify on bench)**.

**Do:** Heat-set two inserts into the **front** face of the printed mount and let them cool. Fasten the 2×2 XH splicer PCB to them with M3×6 BHCS. Snap the two 2-way WAGO 221-412 clamps directly into their slots. Mount the finished assembly under the deck near the bed cable drop with two M5×10 BHCS.

**Check:** Inserts flush, splicer PCB solid, both WAGO levers free. The three bed cables from Ch 03 — Bed L, N and BED TH — reach the mount with slack, and the plate can still be lifted off the deck from above without disturbing it.

⚠ **Rev D+ / LDO:** this whole sub-assembly is a Rev C+ addition with no page in the manual. Its point is that the build plate detaches from the top of the deck panel without unpicking the harness. Two 2-way WAGOs break out the bed power lines; the splicer PCB breaks out the bed thermistor. Terminating any of it is Ch 10. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#wiring-the-bed-heater)

---

### Step 09.35 — Stage the mains-safety hardware, then stop

(no image — see text)

**Parts:** VE0508 ferrules ×5, C13 power cord ×1 (stays bagged), ring terminal for the frame PE, cable tags.

**Do:** Lay out what Ch 10 needs and check you have it, then do nothing else. Every stranded conductor that enters a screw terminal in this machine gets a **VE0508 ferrule** crimped on first — bare strands in a PSU or SSR terminal work loose and arc. Identify the frame's PE point and confirm the paint or anodising is clear under it. Identify where the mains cable will be strain-relieved at the inlet so no conductor takes load from the cord. Confirm the C13 cord is still in its bag.

**Check:** Five ferrules present and the crimp tool to hand. A clean metal-to-metal frame PE point identified. Cord bagged and the inlet switch off.

⚠ **Rev D+ / LDO:** **no wiring happens in this chapter and no plug goes in a socket.** LDO's own warning: *"Mains wiring should only be performed by certified personnel trained in local regulations and safety standards."* Ch 10 runs the full harness in LDO's order and gates on **Checkpoint #1** — with the cord unplugged, continuity within each colour group, **no** continuity between L, N and PE, and the PSU selector re-confirmed at 115 V — before anything is ever switched on. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#checkpoint-1)

---

### Step 09.36 — Photograph the bay and hand it to Ch 10

(no image — see text)

**Parts:** none.

**Do:** Turn the printer back onto its top, light the bay from the side, and shoot it square-on. Compare your photo against LDO's [`S0General_Placement.jpg`](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/RevD/S0General_Placement.jpg) component by component. Tag the boards and the WAGO blocks with the supplied cable tags now, while there is nothing in the way.

**Check:** Your bay matches LDO's layout in kind and roughly in position. Every component is latched or bolted, nothing is wired, no duct lids are on, and the deck's wire opening is clear.

Tip: this photo is worth taking — LDO's placement images are the Rev D reference, but nothing exists for a Rev D+ bay with your exact parts (survey §7.5 #6).

---

## Checkpoint 09

- [ ] Two DIN rails run **left-to-right**, each bolted with one M5×10 BHCS into each bed extrusion, all four plastic end caps fitted.
- [ ] Five wire ducts VHB'd down; the rear duct is below the deck's wire opening, and the opening is clear.
- [ ] Meanwell LRS-200-24 selector set to **115 V**, photographed, on the rear rail via its two printed brackets — and **no** support bracket fitted.
- [ ] Omron SSR on its metal bracket, latched to the rear rail left of the PSU, LOAD (1/2) and INPUT (3+/4−) identified and reachable.
- [ ] **Every** Leviathan voltage-selection jumper removed and bagged.
- [ ] Leviathan on the front rail with the Pi 4B mounted on it, heatsink fitted, SD card in, and the **3/4** HAT power adapter seated.
- [ ] USB adapter on the front rail with the partial cover and the supplied grounding cable attached to its exposed point; frame end left loose for Ch 10.
- [ ] IEC inlet module (one part, not two) in `power_inlet_IECGS_1mm`, panel bolted to the rear extrusion; three WAGO 221-415 clamps in the mains WAGO mount beside it.
- [ ] Nozzle probe assembled — pulley pressed home, PCB on two M2×10, shaft free but captive — and mounted on **M3×25 SHCS**, clear of the plate.
- [ ] XY endstop PCB on the pod, pod on the gantry, full X and Y travel with no fouling.
- [ ] Bed WAGO breakout built and mounted; the plate still lifts off the deck from above.
- [ ] Nothing wired. Nothing plugged in. Duct lids off, skirts and bottom panel off. Multimeter on the bench.

## Common mistakes

- **Running the DIN rails front-to-back because that is what p.29 draws.** Every LDO component position in this bay assumes left-to-right rails. Fixing it later means unbolting rails with the PSU and boards on them.
- **Fitting the p.169 support bracket "because it's in the manual".** LDO explicitly skips it; the two printed brackets are the mount. Bolting an unneeded L-bracket to the frame just puts a screw where a cable wants to go.
- **Leaving the Leviathan's voltage jumpers in.** The one mistake in this chapter that destroys hardware. They come out before the board is installed, not before it is wired.
- **Setting the PSU selector after the bay is full.** Once the PSU is on the rail behind a wire duct the switch is nearly invisible. Set it and photograph it at 09.14.
- **Fitting the V1 USB adapter cover.** It hides the grounding point that Rev D+ exists to expose, and the ESD path silently ends up broken.
- **Closing the bay, or plugging the cord in "just to see the PSU light".** Both belong after Checkpoint #1 in Ch 10 (survey §5.2 W8).
- **Over-driving M2 self-tapping screws into ASA.** Two turns too far strips the boss and the DIN clip or the Z endstop PCB never sits solid again.

## Next

Ch 10 — Wiring: above-deck, below-deck, mains and **Checkpoint #1** (LDO wiring guide, in its own order, plus manual p.194–195 for drag-chain slack). Nothing in this bay gets energised until that checkpoint passes.
