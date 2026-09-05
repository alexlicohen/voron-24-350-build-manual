# R2 — Validity of assembly chapters 00–07 against live sources

Sources used: `docs/manual/assets/Voron2.4r2-manual.pdf` (text via `pdftotext -layout`, page N == manual p.N; PNG page renders for all dimensioned/counted claims), LDO Build Notes/FAQ, LDO Rev D 350 BOM, LDO Printed Parts Guide Rev D, LDO `leviathan-printer-rev-d-sbv2.cfg`, LDO Nitehawk-SB v2 page, docs.vorondesign.com `v2_gantry_squaring.md` + `secondary_printer_tuning.md` (raw markdown), tanaes `extrusion_backers/README.md`, West3D + Fabreeko backer listings, onetwo3d 2.4-350 BOM, Voron-2 `Voron2.4` STL tree (filenames + geometry of 8 STLs).

---

### F1 · BLOCKER · docs/manual/04-ab-drives.md:46 (Hardware table), and Steps 04.24, 04.33, Checkpoint 04
Claim in doc: "GT2 pulley, 20 T, 5 mm bore, **9 mm wide** | 2 | one per motor shaft (p.75, p.79)"; Step 04.24 "1× GT2 20 T 9 mm pulley".
Source checked: LDO Rev D 350 BOM — "Pulley, 2GT, 20T, (5mm ID **6mm** W) 2" and "(5mm ID **9mm** W) 4"; manual p.32 labels the Z pulley "GT2 20T **9mm wide** Pulley" but p.75/p.79 label the A/B pulley only "GT2 20 Tooth Pulley"; p.131 "GT2 Belt **6mm** wide"; onetwo3d 2.4-350 BOM "GT2 20T Pulley (5mm ID 6mm W)".
Problem: the A/B motor pulley is the 6 mm variant — all four 9 mm 20T pulleys are consumed by the Z drive shafts in Ch 02 (Step 02.20), so following Ch 04 steals two Z pulleys and puts a 9 mm pulley in a 6 mm belt plane whose F695 pairs form only an 8 mm channel.
Fix: in the table and Steps 04.24/04.33/Checkpoint, change to "GT2 pulley, 20 T, 5 mm bore, **6 mm wide** (`Pulley, 2GT, 20T, 5mm ID 6mm W` — the kit has exactly 2; the four 9 mm ones are the Z drive pulleys from Ch 02)".

---

### F2 · BLOCKER · docs/manual/03-build-plate.md:192-194 (Step 03.11)
Claim in doc: "measure the two bed extrusions: 130 mm apart… **Check:** 130 mm centre-to-centre; 65 mm each side of centre".
Source checked: manual p.20 — measured on the page render, an extrusion is drawn 26 px = 20 mm (1.30 px/mm); the "65" dimension spans 84 px (64.6 mm) from the centreline to the **inner face** of each bed extrusion, and the "130" spans inner face to inner face (478→647 px).
Problem: 130 mm is the clear gap between the facing inner faces (centres 150 mm apart) — exactly what Ch 01 Step 01.19 says — so Ch 03's "centre-to-centre" check fails on a correctly built frame and sends the builder to move each extrusion 10 mm inboard, after which the plate's corner holes no longer land on the T-nuts.
Fix: replace the Check with "130 mm clear gap between the facing inner faces (= 150 mm centre-to-centre); 65 mm from the centreline to each **inner face**", and change the Do line and the Prerequisites line (03-build-plate.md:8) to match Ch 01 Step 01.19.

---

### F3 · MAJOR · docs/manual/05-gantry.md:49-56 (Hardware table) and Steps 05.10, 05.11, 05.13, 05.32, 05.33
Claim in doc: "Slide **eight** M3 T-nuts…" / "M3×8 SHCS | 23 | 16 Y rails, 7 X rail" / "Slide **seven** M3 T-nuts into the D extrusion's rail slot".
Source checked: p.20 proves the manual's CAD is drawn at the **250 spec** (½ printer width scales to 204 mm ≈ 205); this kit's rails are 400 mm (LDO BOM `LDO-SLR9H-400Z0` ×6, `LDO-SLR12H-400Z1` ×1; onetwo3d 350 BOM "MGN9H 400 mm ×6, MGN12H 400 mm"). MGN9 hole pitch 20 mm → ~20 holes → ~10 screws alternating; MGN12 pitch 25 mm → ~16 holes → ~8.
Problem: the fixed counts are the 250-spec counts read off the drawings; Ch 02 Step 02.09 derives ~10 screws for the *same* 400 mm MGN9, so the two chapters contradict each other and Ch 05's chapter totals are ~4 M3×8 and ~5 M3 T-nuts short.
Fix: mirror Ch 02's wording — "a 400 mm MGN9 has 20 holes at 20 mm pitch, so ~10 screws per Y rail; a 400 mm MGN12 has ~16 at 25 mm pitch, so ~8. Count the holes on your own rail and mark the ones you will use before loading T-nuts." Raise the table to M3×8 SHCS ≈28, M3 T-nut ≈32.

---

### F4 · MAJOR · docs/manual/02-z-drives.md:8 (Prerequisites)
Claim in doc: "Chapter 01 complete: frame assembled, squared, bed extrusions positioned at **255 mm from the centreline** (350 spec)".
Source checked: manual p.20 — "1/2 printer width for standard sizes: … 350 spec 255mm"; the bed-extrusion dimensions on the same page are 65 / 65 / 130.
Problem: 255 mm is the half-width from the frame's outer side face to the centreline, not a bed-extrusion position; as written it is an unbuildable instruction on a 510 mm-wide frame.
Fix: "…bed extrusions positioned 65 mm each side of the printer centreline (130 mm clear gap), per Ch 01 Step 01.19".

---

### F5 · MINOR · docs/manual/05-gantry.md:114 (Step 05.3, Tip)
Claim in doc: "the titanium backers are **pre-tapped** for the chain end link".
Source checked: tanaes `extrusion_backers/README.md` L124 — "They also have pilot holes for the cable chain end link to attach. They are sized to be **drilled out with a 2.5 mm bit and then M3 tapped**."
Problem: the holes are undersized pilots that the builder must drill and tap; Step 05.35 in the same chapter correctly calls them "pilot holes".
Fix: "…the backers carry pilot holes for the chain end link (drill 2.5 mm, tap M3 if you use them) — fit whichever bridge clears once the backers are on."

---

### F6 · MINOR · docs/manual/00-before-you-start.md:444 (Step 00.26)
Claim in doc: "You can tell an F695 (flanged) from a 625 (plain, **larger bore**) on sight."
Source checked: manual p.8 hardware reference (F695 = flanged gantry bearing, 625 = Z-drive bearing); F695 is 5×13×4 mm, 625 is 5×16×5 mm.
Problem: both have a 5 mm bore — the difference is outside diameter and width (plus the flange), so sorting by bore fails.
Fix: "…from a 625 (plain, **larger outside diameter and wider**) on sight — both are 5 mm bore."

---

### F7 · MINOR · docs/manual/06-z-axis-and-gantry-squaring.md:114 (Step 06.4) and Common mistakes
Claim in doc: "cut four at ~1500 mm and trim the tails at the end"; "Cut ~1500 mm; the kit's 6 m of 9 mm belt allows it."
Source checked: LDO Rev D 350 BOM — "Gates Open Belt, 2GT, 9mm (by metre) **6**"; manual p.111 "350 spec 1200mm" minimum.
Problem: 4 × 1500 mm is exactly 6.00 m — zero margin for the squaring cut, a mis-cut or a re-clamp.
Fix: "cut four at ~1400 mm (the manual's 350 minimum is 1200 mm; the kit's 6 m of 9 mm belt then leaves ~400 mm spare)".

---

### F8 · MINOR · docs/manual/00-before-you-start.md:304 vs docs/manual/02-z-drives.md:124
Claim in doc: Ch 00's insert table gives Ch 02 (p.31) as "(verify on bench)"; Ch 02 Step 02.03 states 36 (7 per `z_drive_retainer`, 2 per `z_drive_main`).
Source checked: I measured the released STLs — `z_drive_retainer_a_x2.stl` has six Ø4.70 × 5 mm blind pockets on the bolt-circle face plus one Ø4.70 pocket in a side face (7); `z_drive_main_a_x2.stl` has two Ø4.70 pockets in one face and six Ø3.40 through-holes. Ch 02's counts and its "Ø4.7 × 5 mm pocket vs Ø3.4 through-hole" discriminator are exactly right.
Problem: Ch 00's table is stale relative to the verified number in Ch 02.
Fix: in Ch 00 Step 00.16, change the Ch 02 row's Count cell from "(verify on bench)" to "36 (7 × 4 retainers + 2 × 4 mains — verified against the STLs)".

---

### F9 · MINOR · docs/manual/05-gantry.md:57 (Hardware table row "M3×16 SHCS")
Claim in doc: "M3×16 SHCS | **6** | XY joints to the Y carriages (p.106); 2 more held back for the endstop pod".
Source checked: manual p.106 (4 bolts on one joint, 2 on the other) plus Step 05.43's Check "2 M3×16 left over and bagged".
Problem: the chapter needs 8 counted out of the bag; the Qty cell says 6, so the two reserved screws are not in the chapter total.
Fix: change Qty to "8 (6 fitted + 2 reserved for the endstop pod)".

---

## Verified OK

- Ch 01: p.14 M5×16 in each end of 8 A extrusions (16); p.18 corner brackets + M5×16 ×4; p.19 4× M5 T-nut, 4× M5×10 BHCS, 4× "M5 Shim"; p.15 "BUILD ON A FLAT SURFACE"; p.21 "CHECK FOR SQUARENESS"; blind-joint description matches p.10; access-holes-outward rule follows from p.10; 350 half-width 255 mm (p.20).
- Ch 01 Step 01.19's 65 / 130 / 150 reading of p.20 — confirmed by pixel measurement of the dimension arrows (the authoritative version of the pair contradicted in F2).
- Ch 02: p.24 skip-every-other-hole + centre-outward tightening; p.25 ~3 mm bottom gap, MGN9 guides; p.27 rails face each other; p.28 notch to the back; p.29 align T-nuts / shorten DIN rails; p.32 "GT2 20T 9mm wide Pulley", 5×60 shaft, D-cut, no ball-end drivers, 33 mm = shaft protrusion past the pulley; p.33 stack order (625 · 80T · 2 shims · 625 · 2 shims · 20T · 625) and 3× 625 + 4 shims per drive; p.34 "GT2 188mm Belt Loop"; p.36 exactly 6× M3×40; p.37 M3×8 + M5 nut + accent heart; p.38 16T-only warning, 10.7 mm to the underside of the teeth, "pulley may sit better in the opposite orientation"; p.41 4× M5 T-nut + 2× M5×40; p.42–46 loose/close-tensioner/tighten/check sequence; p.48 "GT2 20 Tooth Idler 9mm wide", M3 nut, M3×16, M5×30; p.49 idler faces the pulley below + seat in corner; p.51 filler.
- Ch 02 insert counts (36 = 7 retainer + 2 main) and the Ø4.7×5 vs Ø3.4 discriminator — verified against the released STL geometry.
- Ch 02/04 Klipper claims — `leviathan-printer-rev-d-sbv2.cfg`: `[stepper_z] rotation_distance: 40`, `gear_ratio: 80:16`; Z0 Front Left→STEPPER 0 … Z3 Front Right→STEPPER 3; `## B Stepper - Left`/HV STEPPER 0 and `## A Stepper - Right`/HV STEPPER 1; `full_steps_per_rotation:400` on X and Y (⇒ 0.9° A/B motors).
- Ch 03: p.53 counterbored top face; p.54 magnet + `voron.link/rm6tpld`; p.55/56 skips; p.57 manual's M3×6 BHCS vs LDO's pre-fitted M4×6; p.58 M4 thumb nuts as spacers + the two 25 mm dimensions; p.59 M3×16 → LDO M3×20 + "only tighten one bolt fully"; p.60 38 mm front offset + wire passthrough; p.61 filler. BOM: build plate 355×355×10, magnetic pad and flex plate as separate line items, `Knurled Nut, M4` ×4.
- Ch 04: p.73 A-frame cutout; p.74/78 stacks — near post 2 bearings + 2 shims, far post 4 + 4 with two shims meeting mid-stack, drawn right on p.74 and left on p.78; flange-out orientation; p.65/69 idler stack shim·F695·F695·shim and the M5×40 assembly aid; p.67/71 M3 washer + M3×40; p.75 16.5 mm hub-down, p.79 6.5 mm hub-up, "wires… pointing towards each other"; p.76/80 3× M3×30; p.81 filler; "LDO has no note for p.62–81" — correct.
- Ch 04 geometry verified against STLs: `front_idler_right_lower` 21.6 mm, `right_upper` 12.0, `left_lower` 11.6, `left_upper` 21.61 (10.00 mm difference = 16.5 − 6.5); `a_drive_frame_upper` has exactly two Ø4.7 insert pockets 56.2 mm apart and two Ø5.4 holes 37.0 mm apart; `b_drive_frame_upper` has **no** Ø4.7 pockets.
- Ch 05: p.84 3-hole vs IGUS 2-hole; p.85 8 M5 T-nuts (4 per end, 2 per slot); p.88 25 mm rail overhang + the "300 mm builds only" end-hole rule (correctly generalised via LDO); p.90 one M5 + one M3 per end; p.91 "5MM HOLES ON TOP"; p.92/93/95 flush install + notch away from the assembly; p.96 three M5 nuts per joint; p.97/99 M5 shim + 2× F695 + M5×40, right joint has the endstop cable channel; p.98/100 2× M5×40 + 20T idler "screwed directly into plastic… must spin"; p.101 15 mm overhang; p.102 4 + 2 M5 T-nuts; p.104 M5×16 (bridge) / M5×10 / M5×30 + shim, "LEAVE SLIGHTLY LOOSE"; p.106 flip, tilt, "2X BOLT ONLY", M3×16.
- Ch 05 backers: tanaes README verbatim on "opposite a linear rail", the single-MGN12 warning, M3×8 for Y / M3×6 for X, Torx/cam-out, and the bowing-straightens-out line; West3D "22 M3x8 FHCS and 10 M3x6 FHCS… about 30 TNuts"; Fabreeko "pre drilled and ready for install".
- Ch 06: p.110 M5 nut + 6×3 magnet (hall-effect only); p.111 GT2 9 mm belt, teeth down, 1× M3×30 + 1× M5×30 per corner, 350 minimum 1200 mm; p.112 "The cutout goes towards the outside"; p.113 belts not drawn; p.114 tilt + extra pair of hands; p.115 4× M3×20 per lower joint + M5×40 up into the block; p.117 "extend… tighten 4 turns" + loosen top clamps; p.118–121 routing/clamp/ziptie; p.122 squaring text + `voron.link/cekh81l`; p.123 filler. LDO p.114–116 re-ordering applied correctly.
- Ch 06b: the Voron page has exactly 17 steps and every 06b.N → Voron-step mapping is right; all verbatim quotes match; A/B 110 Hz over a 150 mm span ("roughly 2lb… lower end of the range") and Z 140 Hz over 150 mm from the Z idler centres; app list matches.
- Ch 07: p.125 equal-length rule; p.126 five insets and two runs on the right / one on the left; p.128 "tighten 4 turns"; p.129 1 + 1 inserts in the carriage halves, 2 in the probe retainer, 2 M3 nuts in the right half; p.130 M3×12 at 3 mm proud; p.131 6 mm belt, teeth away from the extrusion; p.134/136 pull the M3×40 for access; p.139–142 capture/lightly tighten/pull tight/equal protrusion/no plastic rub; p.143 150 mm probe leads + Omron TL-Q5MC; p.144 6 mm below the plastic; p.145 3×6 magnet skipped. onetwo3d's "LL-2GT-6 (6 mm) 2000 mm ×2" quoted correctly.
- LDO Build Notes coverage for p.4–145 is complete and correctly placed: p.19 spacer (Ch 01.18), p.29–30 deck supports (Ch 02.16), p.39 steppers (Ch 02.31), p.54/55/56/57/59 (Ch 03.3/03.4/03.5/03.6/03.15), p.88 (Ch 02.09 + 05.11), p.104 (Ch 05.39), p.114–116 (Ch 06.9), p.129–130 (Ch 05.45 + 07.6), p.143 (Ch 07.34), p.145 (Ch 06 read-first + 07.38). No note in that page range is missing from a chapter, and no ⚠ callout quotes a note that does not exist.
- BOM cross-checks in Ch 00/02/04: F695 ×20, 625 ×12, precision spacer ×46, heat-set insert ×153, M3×8 ×283, M3 T-nut ×135, M5 T-nut ×80, M3 hammerhead ×75, zip ties ×100, 18 extrusions (340E/430D/450C×2/470A×10/530B×4), 7 motors, 8 panels, 10 LDO printed part types, 6× MGN9H-400 + 1× MGN12H-400. Deck-panel 4 mm (Build Notes + Printed Parts Guide) vs 3 mm (Rev D BOM) contradiction is real and correctly flagged in Ch 00.4 / 02.15.
- Every STL filename and repo path in Ch 00/02/04/05/06/07 resolves in `VoronDesign/Voron-2@Voron2.4`, `MotorDynamicsLab/LDOVoron2` (`z_rail_stop_x4.stl`) and `tanaes/whopping_Voron_mods` (`XY_cable_chain_bridge-Igus-3mm_backer.stl`).
- All external URLs return 200 (42 checked, including the 16 Voron-doc raw image links in Ch 06b), except the one noted below.
- Ch 00.5's Nitehawk-SB V2 markers confirmed by LDO's V2 page: RP2040→STM32G0B1, secondary USB port added, keyed fan-adapter headers, Probe/TH0/XY-Endstop moved from JST-XH2.5 to JST-PH2.0.

## Not checkable

- `super-lube.com` NLGI-2 product page returns 403 to curl (bot filter). The NLGI 0/1-vs-2 claim itself is consistent with LDO's rail grease guide; the link is very likely fine in a browser but I could not fetch it.
- The p.111/p.112 point at which `[a]_z_belt_clip_upper_x4` is fitted is not explicit in the manual (p.117 only presumes the top clamps exist). Ch 06 Step 06.7's placement is a defensible reading, not a verifiable one.
- Ch 03.6's identification of the bed thermistor as an ATC Semitec 104NT — not stated in the Rev D BOM, the manual, or the wiring guide section I could reach.
- Whether the supplied titanium backers are 3 mm or 6.5 mm thick (determines which `XY_cable_chain_bridge-*_backer.stl` variant is needed). Ch 05 stages only the 3 mm variant but hedges with a dry-fit at Step 05.35.
- Ch 02.03's per-part insert counts were verified for the `_a` hand only (`_b` mirrors assumed identical).
- Exact screw counts drawn on p.88/p.101 could not be counted unambiguously (carriage occludes one or two); the finding in F3 rests on the rail length and hole pitch, not on the drawing.
