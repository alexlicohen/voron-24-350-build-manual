# R1 — cross-document consistency

Scope: STL↔batch tables, index timeline vs chapter headers, totals, cross-references/anchors,
duplicated procedures, terminology, survey-vs-chapters. All checks re-run programmatically where
possible (scratch scripts in `…/scratchpad/r1/`).

---

### F1 · BLOCKER · docs/manual/09-electronics-bay.md:11, :34 (also 10-wiring.md:13, 11-skirts-panels-door.md:36)
Claim in doc: "**Batch B8, plate B8-P6 — `power_inlet_IECGS_1mm`.** … Print B8-P6 (or at least that one part) before you start, or steps 09.10–09.12 stall." / table row "`Skirts/power_inlet_IECGS_1mm` | 1 (batch B8-P6) | Black"
Source checked: `docs/voron-print-plan.md:485` — "**B8-P6** (1.8 h, 30 g): `mount.stl` — `power_inlet_IECGS_1mm` moved to B7"; `print/B07…md:123` lists it "(moved from B08)"; `00-index.md:185` correction #11 says the same; B08's table does not contain it.
Problem: Three chapters still send the builder to B08/B8-P6 for a part that now prints on **B07-P2**, and B8-P6 is now the BTT TFT mount — following Ch 09 means printing a 6-plate/25.5 h batch out of order and still not having the inlet panel.
Fix: In 09-electronics-bay.md replace the B8-P6 bullet with "**Batch B7 — plate B07-P2** carries `power_inlet_IECGS_1mm` (correction #11); no part of B08 is needed here", change the table cell to `1 (batch B07-P2)`, delete the "B7-P2 … not consumed here" sentence at :10; in 10-wiring.md:13 replace "plate B8-P6 from batch B8" with "B07 (which also carries `power_inlet_IECGS_1mm`)"; in 11-skirts-panels-door.md:36 change the Batch cell from `B8` to `B7`.

### F2 · BLOCKER · docs/manual/print/B01-z-drive-assemblies.md:31, :78, :94–95
Claim in doc: "Checkpoint after B01: **F695 (13 mm OD)** press-fit into each `z_drive_main` and `z_drive_retainer` bearing seat — thumb pressure, no rocking."
Source checked: `voron-print-plan.md:671` — "**625-2RS (16 mm OD)** press-fit into each `z_drive_main` and `z_drive_retainer` bearing seat"; `:182` — "625-2RS; **F695 is the A/B-drive bearing, not the Z drive**"; `02-z-drives.md:67` hardware "625-2RS bearing | 12"; `00-before-you-start.md:442` "**625** bearing (Z drives, 12 in the kit)"; `00-index.md:19` gate "625-2RS bore press-fit".
Problem: B01's bearing-fit gate — the check that decides whether 19.4 h of Z-drive parts are dimensionally good — names a 13 mm bearing for a 16 mm seat; it will always read "loose" and can trigger a needless full reprint or a scale fudge.
Fix: Replace all four `F695 (13 mm OD)` / `F695 bearing` occurrences in B01 with `625-2RS (16 mm OD)`.

### F3 · BLOCKER · docs/manual/print/B03-ab-drive-units-and-front-idlers.md:23 and docs/voron-print-plan.md:673
Claim in doc: "Checkpoint after B03: **625 bearing** seats in the drive frames — the two halves of each drive unit must close flat with no gap."
Source checked: `04-ab-drives.md:47` chapter hardware — "**F695 flanged bearing | 16** | 6 per drive (p.74, p.78) + 2 per front idler (p.65, p.69)"; no 625 appears anywhere in Ch 04; `voron-print-plan.md:182` states the rule explicitly ("F695 is the A/B-drive bearing").
Problem: The B03 fit-check names a bearing that is not used in the A/B drives at all (16 mm OD vs F695's 13 mm) — the mirror image of F2; a builder testing with a 625 will conclude the drive frames printed undersize.
Fix: In both places replace "625 bearing seats in the drive frames" with "**F695** bearing/spacer stacks drop into the drive-frame and front-idler bores without reaming".

### F4 · MAJOR · docs/manual/02-z-drives.md:152–186 (Steps 02.06–02.08) and :80
Claim in doc: Ch 02 Steps 02.06–02.08 run the full rail prep again ("Soak each rail … IPA ≥90 % for about 10 minutes", "flip-and-pack", "wipe"), and :80 adds "do not clean and grease all six unless you intend to install them all now."
Source checked: `00-before-you-start.md:332–375` (Steps 00.18–00.21) already cleans and greases **all seven** rails, Checkpoint 00 :541 requires it; `05-gantry.md:9` prerequisite: "**Ch 00** — all seven rails cleaned and packed with grease"; `00-index.md:22` gate: "all seven rails cleaned and greased"; survey §5.2 W9 guard: "Rail prep is P00, explicitly before P02/P05".
Problem: The same procedure is written twice with contradictory scope; done literally, Ch 02 re-soaks already-packed carriages in IPA and strips the Ch 00 grease, and Ch 02's Time line double-counts 45 min for it.
Fix: Reduce 02.06–02.08 to one verification step — "Rails Z0–Z3 were cleaned and packed in Ch 00 Steps 00.18–00.21. Confirm the labels and that each carriage still runs smooth and silent; if any rail was missed, do Ch 00 Steps 00.18–00.20 now." — and delete the "do not clean and grease all six" sentence at :80.

### F5 · MAJOR · docs/manual/02-z-drives.md:284–294 (Step 02.18) vs docs/manual/09-electronics-bay.md:128–140 (Step 09.5)
Claim in doc: 02.18 "Align the T-nuts and bolt the DIN rails through the deck — **Parts:** DIN rail 35 mm ×2; M5×10 BHCS ×4; the four M5 T-nuts"; 09.5 "Fit the two DIN rails, running left to right — **Parts:** DIN rail ×2, end cap ×4, M5×10 BHCS ×4, M5 T-nut ×4".
Source checked: both cite the same manual page (`manual-p029.png`); Ch 02 hardware :57/:73 counts "M5×10 BHCS | 12 (8 drives + **4 DIN rails**)" and "DIN rail, 35 mm W | 2"; Ch 09 hardware :45 counts "M5×10 BHCS | 8 | **4 DIN rails**, 2 mains WAGO mount, 2 bed WAGO mount"; survey §4.2 p.29 assigns the DIN rails to "`docs/manual/09-electronics-bay.md` step 09.5" only.
Problem: The same two rails and the same four bolts are installed in two chapters and counted in both chapters' Hardware totals (8 M5×10 claimed for 4 fasteners).
Fix: Keep the install in Ch 02 (it is the p.29 page order) and rewrite 09.5 as a check — "The two DIN rails went on in Ch 02 Step 02.18. Confirm they run left-to-right, are parallel, do not overhang the deck, and that all four end caps are fitted." — then drop "DIN rail ×2, M5×10 BHCS ×4, M5 T-nut ×4" from 09.5's Parts and the "4 DIN rails" line from Ch 09's hardware total.

### F6 · MAJOR · docs/manual/07-ab-belts.md:427–470 (Steps 07.34–07.37) vs docs/manual/08-toolhead.md:809–848 (Steps 08.55–08.57)
Claim in doc: 07.35 "Fit the probe and its retainer bracket — **Parts:** `probe_retainer_bracket` ×1; M3×30 SHCS ×2"; 08.56 "Mount the probe on the X carriage and set its height — **Parts:** `probe_retainer_bracket.stl` ×1 (from B4), insulated probe ×1, M3×30 SHCS ×2".
Source checked: Ch 07 hardware :37/:39/:41 counts "M3×30 SHCS | 4 | 2 carriage bolts + **2 probe retainer bracket**", "Inductive probe, Omron TL-Q5MC | 1", "Fibreglass tape … probe insulation"; Ch 08 hardware :54/:74 counts "M3×30 SHCS | 3 | 1 motor, **2 inductive probe**" and "Fibreglass tape, 2×12 cm | 1"; B04 prints exactly **one** `probe_retainer_bracket`. Insulation (07.34 vs 08.55) and the 150 mm lead trim (07.34 vs 08.57) are also duplicated.
Problem: The whole inductive-probe sub-assembly is built twice; one bracket and two M3×30 are counted in two chapter totals; and Ch 08 Step 08.54 "Confirm the probe decision before you drill into it" arrives *after* Ch 07 already fitted the probe.
Fix: Delete 08.55–08.57 and replace with one line in 08.54 — "The Omron probe was insulated, fitted and set to 6 mm in Ch 07 Steps 07.34–07.37; nothing more happens to it here. Bag the Klicky set." — and remove the probe, bracket, 2× M3×30 and fibreglass-tape rows from Ch 08's Hardware total. (Or the reverse; but the probe must live in exactly one chapter, and Ch 05:35 already hedges "fitted in Ch 07/08".)

### F7 · MAJOR · docs/manual/08-toolhead.md:121 (Step 08.3)
Claim in doc: "Set the iron to **~230 °C** with the brass M3 tip and adjust the tongue so it bottoms flush with the insert."
Source checked: `00-before-you-start.md:277` (Step 00.14) — "**LDO publishes no temperature.** Set the iron so the plastic goes *very soft but not runny* … Start low and step up … You have a working temperature written on tape stuck to the iron's base"; `:281` — "Calibrate on this ASA coupon … or the number you find will be wrong for all 150 remaining inserts"; `CONVENTIONS.md:37` — "Never invent a count or a torque. If the source doesn't give it, write `(verify on bench)`".
Problem: Ch 08 is the only place in the manual that states an insert temperature, it is unsourced, and it contradicts the calibrate-your-own procedure Ch 00 mandates — on the Stealthburner main body, the most visible part in the build.
Fix: Replace with "Set the iron to the temperature you found on the Ch 00 practice coupon (Step 00.14) and adjust the tongue so it bottoms flush with the insert."

### F8 · MAJOR · docs/manual/02-z-drives.md:228–238 (Step 02.13) and :45
Claim in doc: Step 02.13 "Optional: fit the LDO rail stops at the top of each Z rail — **Parts:** `z_rail_stop_x4.stl` ×4"; table row "LDO `STLs/z_rail_stop_x4.stl` (optional) | 4 | Black" with no batch id.
Source checked: `print/B05-z-joints-and-z-chain.md:87` is the only batch that prints `z_rail_stop_x4`; `00-index.md:47` places B05 at timeline row 11, five rows after Ch 02 (row 6); Ch 02's Prerequisites (:7–12) name only B0, B1 and B2-P1/P3.
Problem: Ch 02 asks for a printed part that the documented print order does not deliver until after Ch 05, and its Printed-parts table gives no batch id for it — the builder cannot know why it is missing.
Fix: Add the batch to both places and defer: table cell → `4 | Black | **B05** — not available yet at Ch 02`; and in 02.13's Do add "These print in **B05**, which comes after this chapter in the timeline — if B05 is not done, tape or the shipping stoppers from Step 02.11 cover you until Ch 06 Step 06.13, where they are fitted."

### F9 · MAJOR · docs/manual/08-toolhead.md:967 (Step 08.66 callout) and docs/voron-print-plan.md:698
Claim in doc: "⚠ Rev D+ / LDO: **this contradicts the print plan.** `docs/voron-print-plan.md` §0 records Rev D+ as *'electrical only — no printed-part change'*, and batch **B7** lists the V1 `Nitehawk-SB/STLs/usb_adapter_mount.stl`." / plan §6: "Confirm on Fabreeko Discord that D+ is **electrical-only**".
Source checked: `voron-print-plan.md:18` (§0) now reads "**Mostly electrical — one printed-part change:** … `usb_adapter_mount_partial_cover.stl` … — see batch B7"; `print/B07…md:117–118` lists **both** the V1 base file and the V2 partial cover; `00-index.md:175` correction #1 states the same; survey §10 #2 records the correction.
Problem: Ch 08 quotes and attacks a sentence the print plan no longer contains, so the manual advertises an unresolved conflict that was resolved; §6 of the plan still asserts the superseded "electrical-only".
Fix: Replace the Ch 08 callout body with "The Nitehawk-SB-V2 repo's `STLs/` folder contains exactly one file, `usb_adapter_mount_partial_cover.stl`, and it is the cover this kit needs (print plan §0, correction #1). B07 also prints the V1 `usb_adapter_mount.stl` — for a spare **base** only." In plan §6 change the action to "Resolved: D+ changes one printed part (§0); the remaining question for Discord is only whether a D+ printed-parts guide will be published."

### F10 · MAJOR · docs/voron-print-plan.md:734 (§7 Deliberately NOT printed)
Claim in doc: "`deck_support_3mm_x8`, `probe_retainer_bracket_9mm`, `pinda_adapter`, … | **Wrong variant for this kit**"
Source checked: same file §6 :692 — "Print `deck_support_4mm_x8` ×8 now; measure the panel on arrival; **8 g to reprint at 3 mm**"; §3 B1 :262; `print/B01…md:25`; `02-z-drives.md:42` lists `deck_support_3mm_x8` as a chapter part; `00-index.md:181` correction #7; `09-electronics-bay.md:124` tells you to swap to it. (Same problem for `probe_retainer_bracket_9mm`, which §6 :694 and `07-ab-belts.md:449` both tell you to print if the barrel is 9 mm.)
Problem: §7 forbids printing the two parts the rest of the document set names as the documented fallbacks, inside the same file.
Fix: Move both rows out of §7 into §6 (Conditional / verify items), or annotate the row: "`deck_support_3mm_x8`, `probe_retainer_bracket_9mm` — **conditional, not excluded**: print only if the caliper says so (§6)."

### F11 · MAJOR · docs/voron-build-instructions-survey.md:370 (§7.2 Ch 00) and :287 (§5.1 P00)
Claim in doc: "**Printed parts:** the five `STLs/Tools/*` jigs + `Test_Prints/Heatset_Practice` + `Voron_Design_Cube_v7`, **all PLA on the Prusa**." / "*Jigs only, PLA on the Prusa* … ✅ (jigs are PLA, printable day one)"
Source checked: `00-before-you-start.md:25` — "**Printed parts** — batch **B00**, all Galaxy Black **ASA**"; `print/B00…md` table, all Black ASA; `00-index.md:5` — "Every printed part is made here … in Prusament ASA Galaxy Black"; `00-before-you-start.md:553` Common mistakes — "**Practising heat-set inserts on PLA.** ASA softens at a different temperature; the setting you find on a PLA scrap will run too cold or too hot on all 150 remaining inserts"; the B00 gate is an ASA shrinkage/dimensional gate.
Problem: The survey — which CONVENTIONS names as the spine source — specifies PLA for the two coupons whose whole purpose is to calibrate ASA. Not annotated anywhere in the survey.
Fix: Annotate both rows: "**Superseded 2026-09-05:** B00 prints in Prusament ASA Galaxy Black, not PLA — the cube is the ASA dimensional gate and the heat-set coupon must be the build material (see `docs/manual/print/B00-calibration-and-jigs.md`)."

### F12 · MAJOR · docs/voron-build-instructions-survey.md:258 (§4.4 #2) and :311 (§5.2 W1)
Claim in doc: "Gantry racking/squaring must happen after the gantry is in and *before* A/B belts are tensioned." / W1 Guard: "**Gate P07 on P06's squaring sign-off**".
Source checked: `00-index.md:62,98` — Ch 07 (provisional A/B tension) is timeline row 16; Ch 06b (squaring) is row 28, after Ch 13; `06-z-axis…md:622` Step 06b.15 re-tensions afterwards; `07-ab-belts.md:47` explains squaring "needs a running printer … so it happens after Ch 13".
Problem: The manual deliberately inverts the survey's guard (provisional tension → squaring → re-tension), and the survey still states the old rule as a hard gate with no annotation, so the two documents disagree about the single most rework-expensive ordering decision.
Fix: Append to both: "**Revised 2026-09-05:** squaring needs motor control, so it runs out of Ch 13 as Ch 06b. Ch 07 sets *provisional* tension only; final A/B tension is Ch 06b Step 06b.15 / Ch 14 Step 14.4."

### F13 · MAJOR · docs/manual/14-calibration.md:6–12 vs docs/manual/00-index.md:102 and :147
Claim in doc: Ch 14 Prerequisites list Ch 13, the two cubes, Ch 06b, Ch 12 and B00 — no Ch 11 Part B. Index timeline row 30: "needs: Ch 13, Ch 06b, **Ch 11 Part B (the chamber has to close)**". Index Chapters table row 14: "Ch 13, Ch 06b, **Ch 12**".
Source checked: `14-calibration.md:163–165` Step 14.6 requires "panels on and door closed" and a 50–60 °C chamber; `:204` `PRINT_START` waits for chamber > 50 °C; `:512` Checkpoint requires "Chamber reaches the 50–60 °C band with panels and door closed".
Problem: Three statements of Ch 14's prerequisites, none identical; the chapter's own list omits the one prerequisite its checkpoint cannot pass without.
Fix: Make all three read "Ch 13, Ch 06b, Ch 11 Part B (the chamber has to close), Ch 12" — add the Ch 11 Part B bullet to `14-calibration.md` and add Ch 11 Part B to the index Chapters-table cell.

### F14 · MINOR · docs/manual/00-index.md:47 and :35
Claim in doc: Row 11 — "[B05 — Z joints + Z chain] · 5.2 h print · **needs: B00**"; row 7 — "[B03 …] · **needs: B00**".
Source checked: `print/B05…md:5` — "Prerequisites: B00, **B02, B04**"; `print/B03…md:5` — "B00 … ; **B02** printed"; `00-index.md:160` batch table B05 — "B00, B02, B04"; `print/README.md` and plan §9 — `B0;B2;B4` and `B0;B2`.
Problem: The timeline rows under-state two batches' prerequisites and disagree with the index's own batch table three sections lower (execution order happens to satisfy them anyway).
Fix: Row 11 → "needs: B00, B02, B04"; row 7 → "needs: B00, B02".

### F15 · MINOR · docs/manual/11-skirts-panels-door.md:10
Claim in doc: "**Print batch B8** — skirts and front modules (6 plates, **27.6 h**)."
Source checked: `print/B08…md:7` "**Time:** 25.5 h (6 plates)"; `print/README.md`, `00-index.md:71,163`, plan §3/§9 all 25.5 h; B08's six plate times sum to 25.5.
Problem: Single stale figure, 2.1 h high.
Fix: "6 plates, 25.5 h".

### F16 · MINOR · docs/voron-print-plan.md:683
Claim in doc: "Budget your **465 g** of black margin against those."
Source checked: same file §4.2 :609 — "**460 g**"; `print/README.md:18` — "460 g margin (24%)"; 2400 − 1940 = 460.
Fix: "460 g".

### F17 · MINOR · docs/voron-print-plan.md:629 (§4.3) and docs/manual/print/README.md:18
Claim in doc: "With 800 g spools, spool #1 runs out inside **B7**, spool #2 inside **B8/B9**."
Source checked: the cumulative list printed two lines above — B0 57 · B1 381 · B3 511 · B4 633 · B5 716 · B6 878 · B7 1101 · B8 1538 · B9 1860 · B10 1940. 800 g is crossed between B5 (716) and B6 (878); 1600 g between B8 (1538) and B9 (1860).
Problem: Wrong batch named in both files; #1 runs out inside **B6**, #2 inside **B9**.
Fix: "spool #1 runs out inside **B6**, spool #2 inside **B9**" in both places.

### F18 · MINOR · docs/manual/10-wiring.md:34 (table row) and :1034 (Step 10.64)
Claim in doc: "`z_chain_guide` / `z_chain_bottom_anchor` / `[a]_z_chain_retainer_bracket_x2` (**batch B5**)" and "**Parts:** `[a]_z_chain_retainer_bracket` ×1 (**batch B5**)".
Source checked: `print/B02…md:35` prints `[a]_z_chain_retainer_bracket_x2` ×2 in Orange on plate B02-P3; B05's table contains only the four black Z-joint/chain parts; `06-z-axis…md:34` correctly labels it "B2".
Problem: Wrong batch for the orange part — the builder searches the wrong bin. Separately, the quantity does not close: B02 prints 2, Ch 06 Step 06.26 bags 2, Ch 10 Step 10.64 fits 1, and no other step consumes the second.
Fix: Change both `B5` to `B2` for the retainer bracket and split the table row so the black B5 parts and the orange B2 part are not lumped together; and resolve the qty — either 10.64 fits both (one per Z chain end / per drive) or Ch 06 and the tables should say "2 printed, 1 fitted, 1 spare `(verify on bench)`".

### F19 · MINOR · docs/manual/00-index.md:15 (and every assembly chapter)
Claim in doc: "Batches are **B00–B10**; individual plates keep the print plan's shorter form, `B2-P1`."
Source checked: `CONVENTIONS.md:14` says to "name batches by their `batch_id` from the print plan" — the plan's `batch_id` is the *short* form (`B0`…`B10`, §9 CSV). Counts: the short form appears 16× in `00-index.md` itself and is the only form used in Ch 01, 02, 04, 05, 06, 07, 08, 09, 10 and 11 (45× in Ch 11); the long form is the only form in Ch 00, 13, 14 and every `print/` chapter. Plate ids appear in both forms too (`B8-P6` ×7 vs `B08-P6` ×2, `B0-P1` ×6 vs `B00-P1` ×2).
Problem: The index states a naming rule that neither it nor two-thirds of the manual follows, and CONVENTIONS points at the other form; a reader searching "B5" misses the B05 chapter and vice-versa.
Fix: Pick one — recommend `B00`–`B10` for batches and `B00-P1` for plates everywhere (it sorts, and it matches the filenames) — then update `CONVENTIONS.md:14` to say so and normalise the short-form hits.

### F20 · MINOR · docs/manual/00-index.md:107
Claim in doc: "**B2-P1 + B2-P3** gate Ch 02 (Z drive baseplates, belt tensioners, Z tensioners, **cable bridge, endstop pod**) … consumed at **four** different times".
Source checked: `05-gantry.md:10,33,34` — `[a]_xy_joint_cable_bridge_2hole` and `[a]_endstop_pod_D2F_switch` are Ch 05 parts (B2-P3); `08-toolhead.md:10` — the Stealthburner accent parts (`[a]_stealthburner_main_body` on P1; guidler/latch/shuttle/pcb spacer on P3) are a fifth consumption point not listed.
Fix: "…gate Ch 02 (Z drive baseplates, belt tensioners, Z tensioners); the cable bridge and endstop pod off P3 go to Ch 05; the Stealthburner accent parts off P1 and P3 go to Ch 08; …" and change "four" to "five".

### F21 · MINOR · docs/manual/00-index.md:43 and :161
Claim in doc: "`probe_retainer_bracket` off this plate is also **consumed by B06**" / batch table B06 prerequisites "B00, B02, B04 (**consumes `probe_retainer_bracket`**)".
Source checked: `print/B06…md:6` — "Also requires `probe_retainer_bracket.stl` from B04"; but B06 is a print batch and prints none of it; `07-ab-belts.md:443` / `08-toolhead.md:827` are what consume it.
Problem: A print batch is described as consuming a printed part; the real dependency is Ch 07/Ch 08.
Fix: Index → "`probe_retainer_bracket` off this plate is fitted in Ch 07/08, not in a batch"; batch table → drop the parenthetical; `B06…md:6` → "The toolhead chapter also needs `probe_retainer_bracket.stl` from B04 — nothing on this plate depends on it."

### F22 · MINOR · docs/voron-print-plan.md:20 (§0)
Claim in doc: "| Toolhead board | **Nitehawk-SB** (USB toolhead PCB, integrated ADXL) |"
Source checked: same file :18 defines Rev D+ as the V2 board; survey §1.2 — "**Nitehawk-SB V2** (STM32G0B1 …) — **The '+' in D+**"; every manual chapter says Nitehawk-SB V2.
Fix: "**Nitehawk-SB V2** (STM32G0B1, USB toolhead PCB, integrated ADXL)".

### F23 · MINOR · docs/voron-print-plan.md:715 (§7)
Claim in doc: "`usb_adapter_mount` **base** body | Supplied printed (**you print the file anyway for the cover**)"
Source checked: `print/B07…md:117` — "base only — **cover body superseded by the V2 partial cover** below"; `08-toolhead.md:963` — close it with the V2 partial cover, "not the full cover from the V1 `usb_adapter_mount.stl`".
Problem: The stated reason for printing the V1 file is exactly the thing Rev D+ replaced; the actual reason is a spare base.
Fix: "Supplied printed (the file is still printed — for a spare **base**; the V2 partial cover replaces its cover body)".

### F24 · MINOR · docs/manual/14-calibration.md:8
Claim in doc: "**Ch 13 …** All **16** wizard steps passed, including PID, QGL and Z-offset."
Source checked: survey §3.3 :169 lists 13 wizard pages + Finish; `12-software.md:1168` lists the same 13. No 16-item list exists anywhere in the doc set.
Problem: Unsourced count that no other document supports.
Fix: "All wizard steps passed (temperatures → heaters → fans → `STEPPER_BUZZ` → XY endstop → homing → bed locating → 0,0 → Z endstop → probe → PID → QGL → Z-offset), including PID, QGL and Z-offset."

### F25 · MINOR · docs/voron-build-instructions-survey.md:296 (§5.1 P09)
Claim in doc: "**P09 …** Printed parts needed to start: `Electronics_Bay/wago_221-415_mount_3by5` **only (everything else LDO-supplied printed)** … 🟡 one small part"
Source checked: `09-electronics-bay.md:30–35` lists six printed parts for the chapter — `lrs_200_psu_bracket_x2` ×2, the WAGO mount, `pcb_din_clip_x3`, `PSU_stabilizer_50mm`, `usb_adapter_mount_partial_cover`, `power_inlet_IECGS_1mm`; LDO's supplied-printed list (:36) does not include the PSU brackets.
Problem: Unannotated survey statement the chapter contradicts; the PSU brackets in particular are self-printed (B07).
Fix: Annotate: "**Superseded:** Ch 09 consumes six printed parts (B07 + the inlet panel) — see `docs/manual/09-electronics-bay.md`."

### F26 · MINOR · docs/voron-build-instructions-survey.md:287 (§5.1 P00) and :370 (§7.2 Ch 00)
Claim in doc: P00 lists `Tools/bed_hole_marking_template_x1_Rev2` and `Tools/bottom_panel_template` among the parts "needed to start"; §7.2 says "the **five** `STLs/Tools/*` jigs".
Source checked: `print/B00…md` prints **three** Tools files (`MGN12_rail_guide_x2`, `MGN9_rail_guide_x2`, `pulley_jig`); `voron-print-plan.md:615` — "Don't burn black on the optional extras (`bed_hole_marking_template`, `bottom_panel_template`, …) until the machine is standing".
Fix: "the three `STLs/Tools/*` jigs actually printed in B00 (`MGN9_rail_guide_x2`, `MGN12_rail_guide_x2`, `pulley_jig`); the two templates are optional extras deferred per print plan §4.2".

### F27 · MINOR · docs/manual/14-calibration.md:163 vs :165, :512 and docs/manual/00-index.md:101
Claim in doc: "The Voron target to work to is **55–60 °C**" (Step 14.6 Do) vs "settles somewhere in the **50–60 °C** band" (same step's Check), ":512 Chamber reaches the **50–60 °C** band", index gate ":101 Chamber reaches the **50–60 °C** band".
Problem: Two bands one paragraph apart with no statement that 55–60 is the target and 50–60 the accept range.
Fix: In the Check write "settles in the **50–60 °C** accept band (target 55–60 °C)".

### F28 · MINOR · colour naming across chapter Printed-parts tables
Claim in doc: The same filament is written "Black", "Galaxy Black", "Orange", "Prusa Orange", "Prusa Orange (accent)" and "Black (opaque)" in different chapter tables (Ch 02/06/07/08/09/10/11 vs Ch 04 vs the `print/` chapters).
Source checked: `voron-print-plan.md:75–85` §1.2 fixes the colour key — primary = Prusament ASA Galaxy Black, `[a]_` = Prusament ASA Prusa Orange, `[o]_` = Galaxy Black; `CONVENTIONS.md` does not fix the shorthand.
Problem: Harmless in isolation but it defeats a grep/diff over the tables, which is how the STL↔batch reconciliation is done.
Fix: Add one line to `CONVENTIONS.md`: "Colour cells use exactly `Black` or `Orange` (plus `(opaque)` where the STL is `[o]_`); the filament identity lives once, in print plan §1.2."

---

## Verified OK
- All 335 `assets/manual-pages/manual-pNNN.png` image links resolve to files on disk.
- Every relative markdown link and every `#anchor` in `docs/**/*.md` resolves under python-markdown/mkdocs slugification (0 misses, including the `#part-a-…`/`#part-b-…` and `#step-13xx-…` deep links). The only "misses" are the two literal placeholders in `CONVENTIONS.md` (`manual-pXXX.png`, `(url)`), which are examples.
- Every `Step NN.M` / `Step BNN.M` cross-reference in the doc set resolves to an existing heading (0 dangling).
- Every `Checkpoint NN` reference resolves; checkpoints 00–14, 06b and B00–B10 all exist.
- Per-batch gram sums computed from the chapter Printed-parts tables match `print/README.md`, plan §9 and §4.2 to <1 g for all 11 batches; totals 1940 g black / 308 g orange / 2248 g, margins 460 g (24 %) and 492 g (160 %), 26 plates, 134.0 h all reconcile.
- Every per-plate hour/gram figure in the batch chapters (`B00.x`–`B10.x` "Parts:" lines) matches plan §9's plate-level CSV exactly (26 plates).
- Chapter `**Time:**` lines match `00-index.md`'s timeline rows and Chapters table for all 16 chapters; the 60.25 h hands-on total is the exact sum of the midpoints incl. Ch 06b's hour.
- Timeline execution order satisfies every prerequisite it states (topological check over all 30 rows), including Ch 06b and Ch 11 Part B after Ch 13, and Ch 14 last.
- Gen 2 pause placement (index row 17, between B07 and B08) matches print plan §8, including the baseline (before B00), the second-best boundary (before B02) and all five post-upgrade gate items.
- Every STL in an assembly chapter's Printed-parts table exists in exactly one batch table with matching qty, except the two deliberate splits (`z_drive_retainer_a_x2` 1+1 across B00/B01; `Handle` printed in B02, listed again in B10 as a back-reference) — both annotated in-table.
- Belt tension is consistent everywhere: A/B 110 Hz over a measured 150 mm span, Z 140 Hz over 150 mm from the Z idler centres (Ch 06 read-first, 06b.1, 06b.15, Ch 07.32/07.33, Ch 13, Ch 14.4/14.5, survey §4.3) — including the shared rejection of voronldo.com's 80–100/110–130 Hz.
- PID is consistent: bed `TARGET=100`, hotend `TARGET=245` with the part fan at 25 %, PID before QGL, QGL hot (bed 100 / hotend 150); Ch 14 explicitly defers to Ch 13 rather than restating.
- Deck-panel 3 mm/4 mm conflict is stated identically in Ch 00, Ch 02, Ch 09, Ch 11, B01, print plan §3/§6 and index correction #7 (print 4 mm, caliper on arrival, 8 g to reprint) — except plan §7, see F10.
- Probe naming and choice are consistent: Omron inductive on `PROBE` for QGL only, LDO nozzle probe for Z=0, Klicky printed and bagged (Ch 08.54, Ch 09.27/09.30, Ch 12.29, index correction #3, plan §0, survey §4.3).
- DIN rail orientation is left-to-right everywhere (Ch 02.18, Ch 09.5 + Checkpoint 09, index correction #4, survey §4.2 p.29) — the orientation agrees; only the duplication is a problem (F5).
- Fastener naming follows CONVENTIONS: BHCS/SHCS/FHCS used consistently, Ch 00 Steps 00.25–00.26 are the naming contract, no invented torque value anywhere (the only N·m figure is the optional 0.5–3 N·m driver spec).
- "Rev D+ = Rev D + Nitehawk-SB V2, electrical plus one printed part (`usb_adapter_mount_partial_cover`)" agrees between plan §0, survey §1.1/§4.1⑤/§10 #2, index correction #1, Ch 09 and Ch 10 — except the two stale statements in F9.
- Leviathan MCU is treated as contested (F446 V1.1/V1.2 vs H743 V1.3, read the silkscreen) identically in CLAUDE.md, plan §0, survey §1.2, Ch 12 Step 12.13 and index correction #5.
- 350 mm config values agree between survey §4.4 #15 and Ch 12: `position_endstop/position_max: 350` (X,Y), `position_max: 330` (Z), `gantry_corners -60,-10 / 410,420`, `points 50,25 / 50,275 / 300,275 / 300,25`.
- Ch 02's hardware totals (625-2RS ×12, 80T ×4, 20T 9 mm ×4, 16T ×4, 20T idler ×4, 5×60 shafts ×4, closed 2GT 6×188 loops ×4) match survey §7.2 Ch 02 exactly.
- `mkdocs`-visible structure: 16 assembly chapters + 12 print chapters + index, every chapter carrying Time / Prerequisites / Tools / Printed parts / Hardware / Read first / Checkpoint / Common mistakes / Next per CONVENTIONS.

## Not checkable
- Whether the *official* Voron startup wizard really has 16 pages (F24) — needs docs.vorondesign.com; only the survey's 13-item extraction is in-repo.
- Whether `z_rail_stop_x4` is genuinely needed at Ch 02 or only at Ch 06 (F8) — depends on the physical carriage retention, an on-bench call.
- Whether the A/B drive-frame printed bores actually locate a bearing OD at all (F3) — the fix is safe either way because Ch 04 consumes only F695, but the exact seat geometry needs the STL.
- Fastener counts marked `(verify on bench)` throughout — deliberately unresolved by the authors, not checked here.
- Cross-chapter hardware double-counting beyond the three cases found (F5, F6): a full kit-wide fastener reconciliation would need the batch BOM page for the actual kit serial, which does not exist yet.
