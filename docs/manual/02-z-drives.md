# Chapter 02 — Z drives, Z idlers, Z rails, deck panel

Builds the four Z drive units, the four Z idlers, the four Z linear rails and the deck panel. When this chapter closes, the frame has a floor, feet, and every part of the Z motion system except the belts and the Z joints — the gantry has somewhere to hang from.

**Time:** 5.0–7.0 h hands-on, first build (survey §7.2). Rail cleaning and greasing is ~45 min of that and is mostly waiting.

**Prerequisites:**
- Chapter 01 complete: frame assembled, squared, bed extrusions positioned at 255 mm from the centreline (350 spec), and the squareness re-checked after the final torque pass.
- Print batch **B0** (Calibration & jigs) — `MGN9_rail_guide_x2`, `pulley_jig`.
- Print batch **B1** (Z drive assemblies) — drive bodies, retainers, motor mounts, Z-tensioner brackets, deck supports.
- Print batch **B2** (Accent parts, orange) plates P1 and P3 — the five `[a]_` parts below.
- Kit boxes open: Motion, Linear Rail Kit, Motor Kit, the M3/M5 fastener bags.

**Tools**
- Hex drivers 1.5 / 2 / 2.5 / 3 / 4 mm — good quality, *not* ball-end for set screws (p.32).
- Temperature-controlled soldering iron + the LDO brass M3 heat-set tip.
- Digital caliper (deck-panel thickness gate; 33 mm and 10.7 mm pulley dimensions).
- Printed jigs: `MGN9_rail_guide_x2` ×2, `pulley_jig` ×1.
- Shallow tray or pipe long enough to soak a 400 mm rail; grease syringe; lint-free cloth; nitrile gloves.
- Masking tape (carriage retention + rail hole marking) and a marker.

**Consumables:** IPA ≥90%; NLGI 0/1 grease (Super Lube 21030, Mobilux EP1/EP2, or white lithium); Loctite 243 for any set screw that did *not* arrive with threadlocker pre-applied.

**Printed parts** — all ASA. Black = main colour, Orange = accent (`[a]_` prefix).

| STL (Voron-2 `STLs/`, branch `Voron2.4`) | Qty | Colour |
|---|---:|---|
| `Z_Drive/z_drive_main_a_x2.stl` | 2 | Black |
| `Z_Drive/z_drive_main_b_x2.stl` | 2 | Black |
| `Z_Drive/z_drive_retainer_a_x2.stl` | 2 | Black |
| `Z_Drive/z_drive_retainer_b_x2.stl` | 2 | Black |
| `Z_Drive/z_motor_mount_a_x2.stl` | 2 | Black |
| `Z_Drive/z_motor_mount_b_x2.stl` | 2 | Black |
| `Z_Drive/[a]_z_drive_baseplate_a_x2.stl` | 2 | Orange |
| `Z_Drive/[a]_z_drive_baseplate_b_x2.stl` | 2 | Orange |
| `Z_Drive/[a]_belt_tensioner_a_x2.stl` | 2 | Orange |
| `Z_Drive/[a]_belt_tensioner_b_x2.stl` | 2 | Orange |
| `Z_Idlers/z_tensioner_bracket_a_x2.stl` | 2 | Black |
| `Z_Idlers/z_tensioner_bracket_b_x2.stl` | 2 | Black |
| `Z_Idlers/[a]_z_tensioner_9mm_x4.stl` | 4 | Orange |
| `Panel_Mounting/deck_support_4mm_x8.stl` | 8 | Black |
| `Panel_Mounting/deck_support_3mm_x8.stl` | 8 | Black — fallback, see Step 02.15 |
| `Tools/MGN9_rail_guide_x2.stl` (jig, not consumed) | 2 | Black |
| `Tools/pulley_jig.stl` (jig, not consumed) | 1 | Black |
| LDO `STLs/z_rail_stop_x4.stl` (optional) | 4 | Black |

The `_xN` suffix is the quantity you need, not the number of copies in the file — each STL contains one part. `_a` and `_b` are mirrored: two drives use the `a` set, two use the `b` set.

**Hardware** — chapter totals.

| Fastener / part | Qty |
|---|---:|
| M3×8 SHCS | 24 (drives) + ~40 (Z rails, Step 02.09) |
| M3×16 SHCS | 4 |
| M3×40 SHCS | 24 |
| M3 hexnut | 4 |
| M3 roll-in T-nut, 2020 | ~40 (one per Z-rail screw) |
| M3×5×4 brass heat-set insert | 36 (Step 02.03) |
| M5×10 BHCS | 12 (8 drives + 4 DIN rails) |
| M5×16 BHCS | 4 |
| M5×30 BHCS | 12 (idlers: 2 mounting + 1 axle each) |
| M5×40 SHCS | 8 |
| M5 hexnut | 4 |
| M5 roll-in T-nut, 2020 | 20 (16 drives + 4 deck) |
| M5 precision spacer, 1 mm (kit substitute for "M5 Shim") | 16 |
| M4×4 set screw, pre-applied threadlocker | 24 (2 each on 4× 20T, 4× 80T, 4× 16T) |
| 625-2RS bearing | 12 |
| GT2 80T pulley, 5 mm ID | 4 |
| GT2 20T 9 mm pulley, 5 mm ID | 4 |
| GT2 16T pulley, 5 mm ID 6 mm W | 4 |
| GT2 20T 9 mm idler, 5 mm ID | 4 |
| 5×60 mm shaft | 4 |
| Gates 2GT closed loop, 6 mm × 188 mm | 4 |
| NEMA17 Z motor, `LDO-42STH48-2004AC(VRN)` | 4 |
| MGN9H 400 mm rail, `LDO-SLR9H-400Z0` | 4 |
| Rubber foot, 38×19 mm | 4 |
| DIN rail, 35 mm W | 2 |
| Deck panel, acrylic black 469×469 | 1 |

Quantities cross-checked against the LDO Rev D 350 BOM ([350_BOM/Rev_D](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)); the LDO kit ships 6× MGN9H-400 and 1× MGN12H-400 — four of the MGN9s are yours here, the other two are the gantry Y rails in Chapter 05, so do not clean and grease all six unless you intend to install them all now.

**Read first**
- **Rails ship dry, and they must be cleaned and packed with grease *before* they go on the frame.** LDO's flip-and-pack method needs access to the back of the rail, which you lose the moment it is bolted to an extrusion ([rail grease guide](https://docs.ldomotors.com/guides/rail_grease_guide); survey §4.4 #5, §5.2 W9).
- **The Z motors are the only place in the whole printer that uses 16T pulleys.** They look almost identical to the 20T. Get them off the bench when this chapter is done (p.38; survey §4.4 #7).
- **Every set screw gets threadlocker and must land on the flat/D-cut of the shaft.** Loose set screws are the single most reported failure on this machine (p.32; §5.2 W12).
- **Heat-set inserts go into the drive parts before the drive is assembled.** A missed insert means taking a finished drive back apart (§4.4 #4, §5.2 W3).
- **The deck panel and its supports go in now, at p.28–30 — not later with the panels.** Retro-fitting the deck means pulling the frame apart (LDO note p.29–30; §5.2 W4).
- Nothing in this chapter touches a probe or an endstop. The Rev D+ nozzle probe and the Omron inductive probe belong to Chapters 08–09; leave both bagged.

---

## Steps

### Step 02.01 — Lay out and label the chapter's printed parts

![Voron manual p.22](assets/manual-pages/manual-p022.png)

**Parts:** all Chapter 02 printed parts from batches B0, B1 and B2.

**Do:** Sort the drive parts into two mirrored piles — `*_a` and `*_b`, two drives each. Write `a` or `b` on the inside face of every part with a marker. Set the four orange `[a]_z_tensioner_9mm` and the two mirrored `z_tensioner_bracket` pairs aside as the idler pile. Check every part for a corner that lifted off the plate or a delaminated layer at a bolt boss before you put any hardware into it.

**Check:** Ten drive parts (4 main, 4 retainer, 4 motor mount — 12 counting mirrors), 8 orange drive accents, 4 idler brackets, 4 orange idler tensioners, 8 deck supports. Nothing warped at a bearing seat or a bolt boss.

Tip: reprint rather than force a warped `z_drive_main` — it holds the shaft alignment for the whole Z axis. [src](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d)

### Step 02.02 — Learn the four Z positions before you build anything

![Voron manual p.23](assets/manual-pages/manual-p023.png)

**Parts:** none.

**Do:** Memorise the naming from the overview: **Z0 front-left, Z1 rear-left, Z2 rear-right, Z3 front-right**, viewed from the front of an upright printer. The Z idlers ("Z Eyedlers" in the manual's typo) sit directly above their drives at the top corners; the Z linear rails run up the four vertical extrusions; the deck panel goes on the bed extrusions.

**Check:** You can point at each of the four corners and say its Z number without looking.

⚠ **Rev D+ / LDO:** this naming is what the kit's wiring and Klipper config assume — Z0→`STEPPER-0`, Z1→`STEPPER-1`, Z2→`STEPPER-2`, Z3→`STEPPER-3` on the Leviathan. Label each motor's cable with a kit cable tag as you fit it in this chapter and you save an hour in Chapter 10. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#connecting-steppers)

### Step 02.03 — Seat the heat-set inserts in the Z drive parts

![Voron manual p.31](assets/manual-pages/manual-p031.png)

**Parts:** M3×5×4 brass heat-set inserts ×36; `z_drive_retainer_a/b` ×4; `z_drive_main_a/b` ×4.

**Do:** Fit the brass M3 tip to the iron and set the tongue length flush with the height of an insert — long enough to transfer heat, short enough that the tongue never touches the plastic. Insert counts, measured off the STL geometry: **7 per `z_drive_retainer`** (6 in the bolt-circle face plus 1 in a side face) and **2 per `z_drive_main`** (one face). Identify a pocket by diameter: an insert pocket is **Ø4.7 mm × 5 mm deep**; a plain M3 screw clearance hole is Ø3.4 mm and goes straight through. Push each insert down with steady pressure until it is flush, then let the part cool before touching it.

**Check:** 36 inserts in, every one flush or a hair below the surface, no melted bulge around the rim, no insert cocked in its pocket. Count the Ø4.7 pockets on your own parts before you start — if a part shows a different number, trust the part.

Tip: practise on `STLs/Test_Prints/Heatset_Practice.stl` (7 pockets, same Ø4.7×5 geometry) until two in a row go in square. [src](https://docs.ldomotors.com/guides/heatset_insert_tool_guide)

### Step 02.04 — Dial in the iron before you touch a structural part

![Voron manual p.31](assets/manual-pages/manual-p031.png)

**Parts:** the practice coupon from Step 02.03.

**Do:** Set the iron so the plastic goes *soft, not runny*. Too cold and you push hard and cock the insert; too hot and the boss slumps and the insert sinks. LDO's trick: drive the insert ~90 % of the way with the iron, then press the last fraction home with a flat steel block so the top face ends up parallel to the part. Do not leave the iron sitting in a part, and do not leave it powered longer than needed — the brass tip oxidises.

**Check:** On the coupon, an insert goes in square in under 5 seconds with no visible bulge.

⚠ **Rev D+ / LDO:** the kit supplies the brass tip (`Brass Heatset Insert tool (for M3 Brass Inserts)`, 1 off) and 153 inserts for the whole build. 36 of them are spent here. [src](https://docs.ldomotors.com/guides/heatset_insert_tool_guide)

### Step 02.05 — Rail handling rules

![Voron manual p.24](assets/manual-pages/manual-p024.png)

**Parts:** MGN9H 400 mm rails ×4.

**Do:** Read the safety block before you unwrap anything. The carriage slides off the end of the rail if you tip it, and a dropped carriage spills its ball bearings and is scrap. Work over the bench, never over the floor. Keep the shipping stoppers on until the moment you need the carriage off, and put them straight back. Any nick, dent or burr on the rail surface will be felt for the life of the machine.

**Check:** All four rails on the bench, stoppers or tape in place, none of them resting where they can roll off.

### Step 02.06 — Degrease: 10-minute IPA soak

![Voron manual p.24](assets/manual-pages/manual-p024.png)

**Parts:** MGN9H 400 mm rails ×4; IPA ≥90 %.

**Do:** Soak each rail — carriage included — in IPA ≥90 % for about 10 minutes, working the carriage back and forth along the rail to flush the shipping oil and any swarf out from between the ball tracks. Then let the rails dry **completely**; residual IPA thins the grease you are about to pack in.

**Check:** No oil film, no gritty feel when the carriage is run by hand, and the rail is bone dry before the next step.

Tip: a 500 mm length of 40 mm waste pipe with an end cap makes a cheap soak tube and uses a fraction of the IPA a tray does. [src](https://docs.ldomotors.com/guides/rail_grease_guide)

### Step 02.07 — Pack the carriages: LDO's flip-and-pack method

(no image — see text; LDO [rail grease guide](https://docs.ldomotors.com/guides/rail_grease_guide))

**Parts:** MGN9H 400 mm rails ×4; NLGI 0/1 grease in a syringe.

**Do:** Flip the rail so the carriage faces **downwards**. Pick a mounting hole in the rail that is currently underneath the carriage and force grease through it with the syringe. Keep going until you see grease ooze out past the bearings at the sides of the carriage — that is the signal the inside of the carriage is full. Repeat for all four rails. This does not require disassembling the rail, and it is only possible while the back of the rail is accessible, which is why it happens now.

**Check:** Grease visible at both ends of each carriage's seals; the carriage now moves with a smooth, slightly damped feel instead of a dry rattle.

⚠ **Rev D+ / LDO:** the kit does **not** include grease. Use NLGI 0 or NLGI 1 — Super Lube 21030, Mobilux EP1/EP2, or white lithium. Do not use a thin oil or a PTFE dry lube. [src](https://docs.ldomotors.com/guides/rail_grease_guide)

### Step 02.08 — Wipe the rail surfaces clean

(no image — see text; LDO [rail grease guide](https://docs.ldomotors.com/guides/rail_grease_guide))

**Parts:** the four packed rails; lint-free cloth.

**Do:** Run each carriage the full length of the rail, then wipe every trace of grease off the *outside* of the rail. The only grease that should remain is inside the carriage. Grease left on the rail surface collects dust and hair and eventually drags it into the ball tracks.

**Check:** Rail surfaces visibly dry and clean; carriage still runs smoothly end to end with no notch or grinding anywhere in the travel.

### Step 02.09 — Fit the first Z rail, centred, with the MGN9 guides

![Voron manual p.25](assets/manual-pages/manual-p025.png)

**Parts:** MGN9H 400 mm rail ×1; M3×8 SHCS ×~10; M3 roll-in T-nut ×~10; `MGN9_rail_guide_x2` jigs ×2.

**Do:** Pre-load the M3 T-nuts into the inward-facing slot of one vertical extrusion — LDO warns that extrusion/T-nut tolerances are tight, so test-fit and pick the face that runs freely. Slip a printed `MGN9_rail_guide` over the rail at each end; the guides centre the rail on the 20 mm face for you. Set the rail so there is a **~3 mm gap between the bottom of the rail and the printer frame** and start every screw finger-tight before tightening any of them. The manual's pattern deliberately **skips every other mounting hole** — a 400 mm MGN9 has 20 holes at 20 mm pitch, so you use ~10 screws per rail. Count the holes on your own rail and mark the ones you will use with tape before you start, so the pattern comes out symmetric.

**Check:** Rail centred on the extrusion along its whole length (slide a guide up and down to confirm), ~3 mm gap at the bottom, all screws started, none tight yet.

⚠ **Rev D+ / LDO:** LDO's build note "do not use the holes on the ends of the rails, use the second ones from the ends" is written against manual p.88 (the gantry rails). The survey generalises it to every rail in the build (§4.4 #6) — start from the second hole in at each end and alternate from there. It is your call whether to apply it to the Z rails; if you do, apply it to all four identically. [src](https://docs.ldomotors.com/voron/voron2/build-faq)

### Step 02.10 — Tighten from the centre outward

![Voron manual p.25](assets/manual-pages/manual-p025.png)

**Parts:** the rail from Step 02.09.

**Do:** Tighten the screws starting at the middle of the rail and working outward, alternating up and down. This is what pulls the rail flush against the extrusion instead of trapping a bow in it. Snug, not gorilla-tight — an M3 into a T-nut will strip.

**Check:** Run the carriage the full length of the rail with the guides removed. It must feel identical at every point. Any tight spot means the rail is not flush — back the screws off and re-tighten from the centre.

### Step 02.11 — Secure the carriage before the printer is turned over

![Voron manual p.26](assets/manual-pages/manual-p026.png)

**Parts:** masking tape, or the rail's plastic shipping stoppers, or optional `z_rail_stop_x4`.

**Do:** Tape the carriage to the rail, or refit the plastic shipping stopper. The printer goes upside down at Step 02.14 and an untethered carriage will slide straight off the bottom end and spill its bearing balls.

**Check:** The carriage cannot move to the end of the rail under its own weight.

### Step 02.12 — Install the remaining three Z rails

![Voron manual p.27](assets/manual-pages/manual-p027.png)

**Parts:** MGN9H 400 mm rails ×3; M3×8 SHCS ×~30; M3 roll-in T-nut ×~30.

**Do:** Repeat Steps 02.09–02.11 on the other three vertical extrusions. **The rails must face each other** — front-left faces front-right, rear-left faces rear-right, as in the graphic. Keep the same 3 mm bottom gap and the same hole pattern on all four.

**Check:** Four rails installed, all facing inward at each other, all four bottom gaps equal, every carriage taped or stoppered, every carriage running smoothly over full travel.

### Step 02.13 — Optional: fit the LDO rail stops at the top of each Z rail

(no image — see text; LDO [printed parts guide Rev D](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d))

**Parts:** `z_rail_stop_x4.stl` ×4 (LDO repo, print in black).

**Do:** LDO publishes an optional printed stop that clips to the top of each Z rail so a carriage cannot run off the top end during the gantry install in Chapter 06. If you printed them, fit them now while the rails are still open and accessible.

**Check:** A stop at the top of each of the four rails, or a conscious decision to skip them.

Tip: LDO also uses a rubber rail stopper under the Z joints as a gantry rest at manual p.114–116. That is Chapter 06 — do not confuse the two. [src](https://docs.ldomotors.com/voron/voron2/build-faq)

### Step 02.14 — Turn the printer upside down and pre-load the deck T-nuts

![Voron manual p.28](assets/manual-pages/manual-p028.png)

**Parts:** M5 roll-in T-nut ×4.

**Do:** Confirm every carriage is taped, then turn the frame upside down onto the flat reference surface. Slide **four M5 T-nuts** into the upward-facing slots of the two bed extrusions — two per extrusion, roughly where the deck panel's four holes will land.

**Check:** Frame sits flat and does not rock in this orientation; four T-nuts in, free to slide, none dropped inside an extrusion.

### Step 02.15 — Caliper the deck panel and choose the support thickness

![Voron manual p.29](assets/manual-pages/manual-p029.png)

**Parts:** deck panel; caliper; `deck_support_4mm_x8` ×8 and `deck_support_3mm_x8` ×8.

**Do:** Measure the actual thickness of your deck panel with the caliper, in three places. **Do not resolve this from documents.** Fit the deck support clips that match what you measured.

**Check:** Three readings agree to within 0.1 mm, and the number is written in your build log. You have eight clips of the matching thickness on the bench.

⚠ **Rev D+ / LDO:** LDO's build note for p.29–30 says the LDO deck panel is **4 mm nominal — use `deck_support_4mm`**, but the Rev D 350 BOM lists the deck panel as *469×469×**3 mm***. The two LDO documents disagree (survey §4.3). Both support variants are 1.1 g and minutes of print time; print both, measure, fit whichever matches, and write the measured number in your build log. [src](https://docs.ldomotors.com/voron/voron2/build-faq) · [BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)

### Step 02.16 — Fit the deck support clips

![Voron manual p.29](assets/manual-pages/manual-p029.png)

**Parts:** deck support clips ×8 (the thickness you chose in Step 02.15).

**Do:** Slide the eight clips into the extrusion slots that the deck panel will rest on, spaced evenly along the unsupported spans. They carry the middle of the panel so it does not sag under the weight of the electronics.

**Check:** Eight clips fitted, all the same thickness variant, all sitting square in the slot with their support face level with the extrusion face the panel will sit on.

⚠ **Rev D+ / LDO:** this step is not in the official manual at all. LDO adds it here: *"This is a good time to install the deck supports."* Doing it later means the deck comes out and the frame comes partly apart (§5.2 W4). [src](https://docs.ldomotors.com/voron/voron2/build-faq)

### Step 02.17 — Drop the deck panel in, notch to the back

![Voron manual p.28](assets/manual-pages/manual-p028.png)

**Parts:** deck panel ×1.

**Do:** Peel any protective film. Lay the panel on the bed extrusions with the **cut-out notch toward the back** of the printer — the notch is the wire pass-through and it is wrong in every other orientation. Line the four bolt holes up over the four T-nuts.

**Check:** Notch at the back. Panel sits flat on the extrusions and the support clips with no rock and no gap at a corner.

### Step 02.18 — Align the T-nuts and bolt the DIN rails through the deck

![Voron manual p.29](assets/manual-pages/manual-p029.png)

**Parts:** DIN rail 35 mm ×2; M5×10 BHCS ×4; the four M5 T-nuts from Step 02.14.

**Do:** Slide each T-nut until it sits directly under one of the four holes in the deck panel. Lay the two DIN rails across the panel, left-to-right, and drive **two M5×10 BHCS through each rail**, through the deck panel, into the T-nuts. If a DIN rail's own slots will not line up with a T-nut, shorten the DIN rail by a few millimetres rather than moving the panel.

**Check:** Four bolts in, deck clamped but not dished — acrylic cracks if you over-torque it. Both DIN rails parallel and running left-to-right.

Tip: the kit includes four DIN rail plastic end caps. LDO fits them during wiring; fitting them now is easier and costs nothing. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#installing-the-din-rails-and-wire-ducts)

### Step 02.19 — Fix the printer's orientation in your head

![Voron manual p.30](assets/manual-pages/manual-p030.png)

**Parts:** none.

**Do:** The manual now labels Top / Front / Back on every graphic, and the printer spends the next fifteen pages upside down. Put a strip of masking tape on the **front** bed extrusion and write "FRONT" on it. Every "which corner is this?" callout for the rest of the chapter is read relative to that tape.

**Check:** Front face marked, and you can restate the Z0–Z3 map from Step 02.02 with the printer inverted.

### Step 02.20 — Fit the 20T pulley to the 5×60 shaft, 33 mm out

![Voron manual p.32](assets/manual-pages/manual-p032.png)

**Parts:** 5×60 mm shaft ×1; GT2 20T 9 mm pulley ×1; M4×4 set screws ×2 (pre-threadlocked).

**Do:** Slide the 20T 9 mm pulley onto the shaft so **33 mm of shaft protrudes past the pulley** on the long side (the dimension on the page). Rotate the pulley so that **one set screw lands on the D-cut flat** of the shaft. Fit both set screws and tighten with a proper hex driver — **not** a ball-end driver, which cams out and rounds the socket.

**Check:** 33 mm on the caliper. One set screw provably on the flat (the shaft will not rotate in the pulley when you twist it hard by hand).

⚠ **Rev D+ / LDO:** the kit's M4×4 set screws arrive with threadlocker pre-applied — do not add more. If a screw has clearly been used before or has no visible compound, add Loctite 243 and keep it off the printed parts. [src](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)

### Step 02.21 — Verify the pulley with the jig, then repeat ×4

![Voron manual p.32](assets/manual-pages/manual-p032.png)

**Parts:** `pulley_jig.stl`; the remaining three shafts and 20T pulleys; M4×4 set screws ×6.

**Do:** Check the pulley position against the printed `pulley_jig` — it gives you a repeatable stack height without re-measuring. Build the other three shaft/pulley pairs the same way.

**Check:** Four shafts, four 20T pulleys, all at the same protrusion, all with a set screw on the flat, all eight set screws tight.

### Step 02.22 — Build the bearing/pulley stack on each shaft

![Voron manual p.33](assets/manual-pages/manual-p033.png)

**Parts:** per drive — 625-2RS bearings ×3; GT2 80T pulley ×1; M5 precision spacer 1 mm ×4; the shaft from Step 02.20.

**Do:** Working outward from the 20T pulley along the shaft, the order in the exploded view is: **625 bearing** (outboard of the 20T pulley's set-screw collar), then on the other side of the 20T pulley — **two M5 precision spacers, a 625 bearing, two more M5 precision spacers, the 80T pulley, and the last 625 bearing on the very end of the shaft.** Push the bearings on square by hand; if one needs a press, press on the *inner* race only.

**Check:** Compare your stack side by side with the p.33 graphic before you go any further. Both outer bearings free to spin, no spacer trapped crooked, the 80T pulley running true (spin the shaft and watch the pulley rim for wobble).

⚠ **Rev D+ / LDO:** the manual says "M5 Shim". **The kit supplies brass M5 precision spacers instead — use those, everywhere in the manual from p.19 onward unless a note says otherwise.** Four per drive, 16 for this chapter. [src](https://docs.ldomotors.com/voron/voron2/build-faq)

### Step 02.23 — Threadlock the 80T pulley set screws and check your work

![Voron manual p.33](assets/manual-pages/manual-p033.png)

**Parts:** M4×4 set screws ×2 per 80T pulley.

**Do:** Set the 80T pulley so a set screw meets the flat of the shaft, fit both set screws with threadlocker, and tighten. The manual is blunt about this: loose set screws account for the majority of user problems on this machine. Build all four stacks.

**Check:** Four complete shaft assemblies, all matching the graphic, none able to slip when you twist the 80T pulley against the shaft by hand.

### Step 02.24 — Fit the 188 mm closed belt loop over the 80T pulley

![Voron manual p.34](assets/manual-pages/manual-p034.png)

**Parts:** Gates 2GT closed loop 6 mm × 188 mm ×1 per drive.

**Do:** Drop the closed belt loop over the 80T pulley, teeth inward, before the shaft goes into the housing. This loop is captive once the drive is closed — there is no way to add it later without dismantling the drive.

**Check:** Loop seated in the 80T pulley's teeth, hanging free, not twisted.

⚠ **Rev D+ / LDO:** LDO publishes **no** deviation for the Z belt loop, the 16T/80T pulleys or the Z gear ratio — the Build Notes for p.22–51 cover only p.29–30 (deck supports) and p.39 (stepper wiring). The kit's Klipper config confirms the stock arrangement: `[stepper_z] rotation_distance: 40`, `gear_ratio: 80:16`. Use the 188 mm loops as supplied. [src](https://github.com/MotorDynamicsLab/LDOVoron2/blob/main/Firmware/leviathan-printer-rev-d-sbv2.cfg)

### Step 02.25 — Seat the shaft assembly into `z_drive_main`

![Voron manual p.35](assets/manual-pages/manual-p035.png)

**Parts:** `z_drive_main_a` or `_b` ×1; the belted shaft assembly from Step 02.24.

**Do:** Lower the whole shaft assembly into the printed housing so each 625 bearing drops into its seat and the belt loop lies inside the body. The bearings should go in with firm thumb pressure. **If one needs real force, do not drive it.** Warm the part to roughly 50 °C first (a few minutes on a warm bed or under a hair dryer), then press the bearing square using a flat block on the outer race — never a hammer, never a screwdriver against the seal, and never at an angle. ASA at room temperature cracks along the layer lines when a bearing is driven into a seat that shrank slightly on cooling.

**Check:** All three bearings fully home, the shaft parallel to the housing's mating face, and the belt loop entirely inside the body.

### Step 02.26 — Check the shaft position against the section view

![Voron manual p.35](assets/manual-pages/manual-p035.png)

**Parts:** none.

**Do:** Hold your part next to the two isometric views and the section view on the page. Confirm the 20T pulley is on the same side as in the drawing, that the spacer stack sits between the same two bearings, and that the shaft ends are flush the same way.

**Check:** Your assembly and the drawing are indistinguishable. Fix it now — after the retainer goes on, six M3×40 have to come back out.

### Step 02.27 — Close the drive with `z_drive_retainer` and six M3×40

![Voron manual p.36](assets/manual-pages/manual-p036.png)

**Parts:** `z_drive_retainer_a` or `_b` ×1 (inserts already fitted, Step 02.03); M3×40 SHCS ×6.

**Do:** Lay the retainer over the drive body so the bearing cradles line up, press it down until the two mating faces meet with no gap, and drive the six M3×40 SHCS through the stack into the heat-set inserts. Tighten in a criss-cross pattern, a little at a time, so the retainer pulls down evenly. Snug, then stop — the thread is a brass insert in ASA.

**Check:** No gap anywhere along the joint line. The shaft still spins freely by hand with the belt on. If it binds, the retainer has trapped a bearing crooked — back the screws off and reseat.

### Step 02.28 — Fit the orange baseplate and its captive M5 nut

![Voron manual p.37](assets/manual-pages/manual-p037.png)

**Parts:** `[a]_z_drive_baseplate_a` or `_b` ×1 (orange); M5 hexnut ×1; M3×8 SHCS ×3.

**Do:** Drop the M5 hexnut into its pocket in the orange baseplate — the Voron heart on the part is the manual's accent-part marker, so this is the piece that ends up in your accent colour. Fit the baseplate to the drive and secure it with three M3×8 SHCS.

**Check:** M5 nut fully seated in its pocket and not able to spin. Three M3×8 in, plate flat against the drive body with no rock.

### Step 02.29 — Confirm the belt loop is captured

![Voron manual p.37](assets/manual-pages/manual-p037.png)

**Parts:** none.

**Do:** Look into the drive through the openings. The closed 188 mm loop must be inside the part, around the 80T pulley, with enough slack hanging to reach the motor pulley.

**Check:** Belt visible inside the drive and free to move. Repeat Steps 02.25–02.29 for the other three drives before moving on — two `a` and two `b`.

### Step 02.30 — Fit the 16T pulley to a Z motor at 10.7 mm

![Voron manual p.38](assets/manual-pages/manual-p038.png)

**Parts:** NEMA17 Z motor `LDO-42STH48-2004AC` ×1; GT2 **16T** pulley ×1; M4×4 set screws ×2.

**Do:** **These are the only 16T pulleys in the printer** — check the tooth count on the pulley itself, not the bag it came out of. Slide it onto the motor shaft so the gap from the motor's front face to the underside of the pulley is **10.7 mm**. Rotate so at least one set screw contacts the flat of the motor shaft, then fit and tighten both with threadlocker. Depending on the motor, the pulley may sit better flipped; what matters is where the *teeth* end up, not which way the boss faces.

**Check:** 10.7 mm on the caliper. Tooth band at the same height as the 20T band it will drive. Pulley will not slip on the shaft under hand force.

Tip: when all four are done, physically remove every remaining 16T pulley from the bench so one cannot end up on an A/B motor in Chapter 04. [src](https://docs.ldomotors.com/voron/voron2/build-faq)

### Step 02.31 — Bolt the motor to `z_motor_mount`, watching the cable exit

![Voron manual p.39](assets/manual-pages/manual-p039.png)

**Parts:** `z_motor_mount_a` or `_b` ×1; M3×8 SHCS ×3.

**Do:** Set the motor against the printed L-bracket with the shaft through the opening and the **cable exit oriented as in the graphic** (the circled feature on the page). Fit three M3×8 SHCS through the mount's plate into the motor. Build all four; two mounts are `a`, two are `b`.

**Check:** All four cable exits point the same way relative to their mount, the 16T pulley clears the mount, and the two large M5 clearance holes in the mount's foot are unobstructed.

⚠ **Rev D+ / LDO:** the manual's own stepper wiring instructions for this page do **not** apply to this kit. Wire the Z steppers per the LDO Rev D wiring guide (Z0 front-left→`STEPPER-0`, Z1 rear-left→`STEPPER-1`, Z2 rear-right→`STEPPER-2`, Z3 front-right→`STEPPER-3`). Label each motor cable with a kit cable tag now — in Chapter 10 the four cables are indistinguishable. [src](https://docs.ldomotors.com/voron/voron2/build-faq) · [wiring guide](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#connecting-steppers)

### Step 02.32 — Identify Z0 and start there

![Voron manual p.40](assets/manual-pages/manual-p040.png)

**Parts:** one complete drive + one motor/mount assembly.

**Do:** Z0 is the first drive to go on the printer. With the printer upside down, find the corner the graphic highlights and lay the matching drive and motor assembly beside it. Match the mirror hand (`a` vs `b`) to the corner before you fit anything.

**Check:** The drive body's belt tensioner cut-out and the motor's cable exit both face the way the graphic shows for this corner.

### Step 02.33 — Pre-load four M5 T-nuts at the Z0 corner

![Voron manual p.41](assets/manual-pages/manual-p041.png)

**Parts:** M5 roll-in T-nut ×4.

**Do:** Slide **four M5 T-nuts** into the two bottom extrusions meeting at this corner, two in each, positioned roughly where the four M5 bolts will land — two for the motor mount (M5×40), one for the drive body (M5×10, Step 02.35), one for the belt tensioner (M5×10, Step 02.36). Test-fit them first: LDO warns the extrusion and roll-in T-nut tolerances are tight and vary by extrusion face.

**Check:** Four T-nuts in, all free to slide, none jammed or dropped inside the extrusion.

### Step 02.34 — Bolt the motor mount down with two M5×40

![Voron manual p.41](assets/manual-pages/manual-p041.png)

**Parts:** M5×40 SHCS ×2; the motor/mount assembly.

**Do:** Set the motor assembly at the corner and drive two M5×40 SHCS down through the counterbored holes in the mount's foot into two of the pre-loaded T-nuts. Do not fully tighten yet — the belt tensioner still has to pull the drive body into position.

**Check:** Both bolts engaged in T-nuts, motor mount sitting flat on the extrusion, motor free to be nudged a millimetre or two.

### Step 02.35 — Slide the drive body in at an angle

![Voron manual p.42](assets/manual-pages/manual-p042.png)

**Parts:** M5×10 BHCS ×1; the completed Z drive.

**Do:** Insert the drive body at an angle and slide it into place against the corner, feeding the belt loop over the 16T motor pulley as it goes. Fit one M5×10 BHCS through the drive body's foot into a T-nut. **Leave it loose** — the manual says so explicitly, and the tensioner in the next step needs the drive free to move.

**Check:** Belt loop engaged on both the 16T motor pulley and the 80T drive pulley, sitting squarely in both tooth bands. Bolt started but loose.

### Step 02.36 — Fit the orange belt tensioner, still loose

![Voron manual p.43](assets/manual-pages/manual-p043.png)

**Parts:** `[a]_belt_tensioner_a` or `_b` ×1 (orange); M5×10 BHCS ×1.

**Do:** Lay the orange tensioner cam on the extrusion in front of the drive, in the open position shown, and fit one M5×10 BHCS through its pivot hole into the last T-nut. **Leave this bolt loose too** — it is a pivot at this point, not a fastener.

**Check:** Cam free to rotate about the bolt; drive body still free to slide.

### Step 02.37 — Flip the tensioner latch closed

![Voron manual p.44](assets/manual-pages/manual-p044.png)

**Parts:** none.

**Do:** Rotate the tensioner cam closed, in the direction of the arrow. Closing it drives the Z drive body away from the motor and tensions the 188 mm belt loop.

**Check:** Cam fully closed and sitting flat against the extrusion. Belt loop now taut — you should be able to spin the 80T pulley by turning the motor shaft by hand, with no slip and no belt skip.

### Step 02.38 — Tighten the M5 bolts

![Voron manual p.45](assets/manual-pages/manual-p045.png)

**Parts:** none — the four M5 bolts already fitted.

**Do:** Only now, with the tensioner closed, tighten the two M5×40 and both M5×10 bolts properly.

**Check:** All four bolts tight. Nothing has moved. The belt is still correctly seated in both pulleys.

### Step 02.39 — Fit the rubber foot

![Voron manual p.45](assets/manual-pages/manual-p045.png)

**Parts:** Rubber foot 38×19 mm ×1; M5×16 BHCS ×1.

**Do:** With the printer still upside down, fit a rubber foot at this corner and fix it with one M5×16 BHCS.

**Check:** Foot square to the corner and firmly attached.

### Step 02.40 — Check the drive did not shift when the tensioner closed

![Voron manual p.46](assets/manual-pages/manual-p046.png)

**Parts:** none.

**Do:** Sight down the section view on the page and compare. The drive body must still sit hard against the corner and square to both extrusions.

**Check:** No skew, no gap at the corner, belt still fully on both pulleys. **If the drive moved when the tensioner closed, undo the bolts, realign, and redo Steps 02.37–02.38** — the manual calls this out specifically.

### Step 02.41 — Build and fit the other three Z drives

![Voron manual p.47](assets/manual-pages/manual-p047.png)

**Parts:** the remaining three drives, motors, mounts, tensioners, feet and their hardware.

**Do:** Repeat Steps 02.32–02.40 at the opposing corner with the same hand of parts, then at the two remaining corners with the **mirrored** printed parts (`_b` where you used `_a`, and vice versa). Label each motor's cable Z0/Z1/Z2/Z3 by its physical corner as you go.

**Check:** Four drives on, four feet on, four belts tensioned, four tensioners closed, four cables labelled. The frame now stands on its rubber feet — turn it back upright and confirm it does not rock.

### Step 02.42 — Assemble a Z idler cage

![Voron manual p.48](assets/manual-pages/manual-p048.png)

**Parts:** `z_tensioner_bracket_a` or `_b` ×1; `[a]_z_tensioner_9mm` ×1 (orange); M3×16 SHCS ×1; M3 hexnut ×1.

**Do:** Drop the M3 hexnut into the pocket in the top of the bracket. Slide the orange tensioner into the bracket and run the M3×16 SHCS up through the tensioner into the nut. Leave it a couple of turns short of tight so the tensioner can still slide — this screw is the Z belt tension adjuster later.

**Check:** Nut captive, screw engaged, tensioner sliding smoothly in the bracket with no side play.

### Step 02.43 — Fit the 20T idler on its M5×30 axle

![Voron manual p.48](assets/manual-pages/manual-p048.png)

**Parts:** GT2 20T 9 mm idler ×1; M5×30 BHCS ×1.

**Do:** Slot the 20T 9 mm idler into the fork of the orange tensioner and push the M5×30 BHCS through as the axle. Build all four idlers — two `a` brackets, two `b`.

**Check:** Idler spins freely on the axle with no axial slop, and its tooth band sits centred in the fork. Four idlers built.

### Step 02.44 — Pre-load two M5 T-nuts at a top corner

![Voron manual p.49](assets/manual-pages/manual-p049.png)

**Parts:** M5 roll-in T-nut ×2.

**Do:** Slide two M5 T-nuts into the vertical extrusion at the top corner directly above a Z drive, positioned where the idler bracket's two mounting holes will land.

**Check:** Two T-nuts in the correct extrusion face, free to slide.

### Step 02.45 — Mount the idler, matching the drive below it

![Voron manual p.49](assets/manual-pages/manual-p049.png)

**Parts:** M5×30 BHCS ×2; the idler from Step 02.43.

**Do:** Offer the idler up to the corner. **Its pulley must face the same way as the pulley in the drive directly below it** — this is what keeps the Z belt running in a single plane. Press the bracket **firmly into the corner** before you tighten anything, then fit two M5×30 BHCS into the T-nuts and tighten.

**Check:** Idler pulley and the drive's 20T pulley below it lie in the same vertical plane — sight down them, or hang a length of the 2GT belt between them and look for twist. Bracket hard against both faces of the corner.

### Step 02.46 — Fit the remaining three Z idlers

![Voron manual p.50](assets/manual-pages/manual-p050.png)

**Parts:** the remaining three idlers; M5×30 BHCS ×6; M5 roll-in T-nut ×6.

**Do:** Repeat Steps 02.44–02.45 at the opposing corner, then at the two mirrored corners with the `b`-hand brackets.

**Check:** Four idlers fitted, each one aligned with the drive beneath it, all pressed into their corners, all eight M5×30 tight.

### Step 02.47 — Close the chapter

![Voron manual p.51](assets/manual-pages/manual-p051.png)

**Parts:** none — p.51 is a filler page in the manual and carries no assembly step.

**Do:** Use it as the marker that the Z chapter is done. Turn the printer upright, work through Checkpoint 02, and photograph the deck-support thickness next to the caliper reading and one complete Z drive corner before the gantry starts hiding them.

**Check:** Checkpoint 02 fully ticked.

---

## Checkpoint 02

- [ ] All four Z rails run their full travel with no notch, tight spot or grinding; every carriage is taped or stoppered.
- [ ] Rail surfaces are clean and dry; grease is inside the carriages only; you saw grease ooze past the bearings on each of the four.
- [ ] All four rails are centred on their extrusions, face each other, and share the same ~3 mm bottom gap and the same hole pattern.
- [ ] Deck panel notch is at the **back**; panel sits flat with no rock; four M5×10 into T-nuts through both DIN rails; nothing over-torqued into the acrylic.
- [ ] Measured deck-panel thickness is written down and the fitted deck supports (8 off) match it.
- [ ] Every 20T drive pulley sits 33 mm along its shaft; every 16T motor pulley sits 10.7 mm off the motor face.
- [ ] All 24 M4×4 set screws are tight, threadlocked, and at least one per pulley lands on the shaft flat.
- [ ] Four M5 precision spacers per drive (16 total) — **spacers, not shims**.
- [ ] Each Z drive shaft turns freely by hand through the belt, with no belt skip and no bearing rumble.
- [ ] All four tensioner cams are closed and no drive shifted when its cam closed (p.46 check).
- [ ] Four rubber feet fitted; the printer stands on all four without rocking on the reference surface.
- [ ] Each Z idler faces the same way as the pulley in the drive below it and is pressed hard into its corner.
- [ ] Four motor cables labelled Z0 / Z1 / Z2 / Z3 by physical corner.
- [ ] Photos taken: deck thickness + caliper, one complete drive corner, one greased carriage.

## Common mistakes

- **Bolting the rails on dry.** Once a rail is on an extrusion you cannot use the flip-and-pack method, and a dry MGN9 wears out. Rails off again, or a compromised axis — clean and pack them first (§5.2 W9).
- **Missing a heat-set insert before the drive is closed.** Six M3×40 have to come out and the shaft assembly has to be lifted to reach it. Do the insert pass as a batch, count the pockets, and only then start assembling (§5.2 W3).
- **A 20T pulley on a Z motor.** The 16T and 20T look nearly identical. The machine will home and move and be silently wrong on every Z dimension, because `gear_ratio: 80:16` is baked into the config. Count teeth, then clear the 16T pulleys off the bench (p.38).
- **Skipping the deck supports "until the panels chapter".** The deck cannot be lifted once the gantry and electronics are in — the frame has to come partly apart. LDO puts this at p.29–30 for a reason (§5.2 W4).
- **Tightening rail screws from one end.** The rail bows and the carriage develops a tight spot that no amount of greasing fixes. Always centre-outward (p.24).
- **Set screws finger-tight or off the flat.** They loosen under Z load, the belt slips, and the gantry drops out of level. Threadlocker on all of them, one on the flat, tightened with a proper hex driver (p.32, §5.2 W12).
- **Over-torquing an M5×10 into the acrylic deck.** Acrylic crazes and cracks around the bolt. Snug is enough; the DIN rails spread the load.

## Next

Chapter 03 — Build plate: bed, magnet sheet, spacers and the M3×20 mounting screws (manual p.52–61, with LDO's p.55/56 skips).
