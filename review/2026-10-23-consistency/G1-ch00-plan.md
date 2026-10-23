# G1 — Ch 00 / 00a / Tonight / index / print plan / survey / README

**Group:** G1 (triage-deep-reasoner, 2026-10-23). Read-only review of the working tree as is.
**Files covered:** docs/manual/00-before-you-start.md, 00-index.md, 00-tonight.md, 00a-mains-safety.md, docs/voron-print-plan.md, docs/voron-build-instructions-survey.md, README.md.
**Primary sources used:** every chapter's header block (Time / Sessions / Prerequisites / Tools) and `Pause:` lines counted per Part (script); `slicer/bins.py` + `check_docs._batch_bins()` (batch → bin map); `slicer/plates.py`, `slicer/estimates.csv`; `slicer/plates/B08-P1.3mf` mesh extents vs the native STLs; `scripts/data/ldo-350-bom.yml`; Ch 03/09/10/11/12/13/14 mains steps (10.1–10.24, 10.71, 10.73–10.78, 11.67, 12.11, 13.1–13.3, 14.30); `slicer/addons/*/README.md` job grams; PROJECT_MEMORY.md and AGENTS.md for decisions.

Counts: 0 blocker · 7 major · 19 minor · 6 nit.

---

### G1-01 major — Kit ETA is stale everywhere, and the "all 22 plates before kit day" premise now rests on it
- docs/manual/00-index.md:7 "not expected until **late November to late December 2026**, so **all eleven print batches … go down before it arrives**"; :155 "Starting early/mid October puts the last plate off the bed early/mid November, two to six weeks ahead of the kit"; :160 "the kit landing between 2026-11-20 and 2026-12-24".
- docs/manual/00-before-you-start.md:19 "ETA **late November to late December 2026**"; :18 "B00 prints months before the Voron kit lands".
- docs/voron-print-plan.md:243 "not expected before late November 2026"; :859 "realistic delivery is **late November to late December 2026**".
- vs PROJECT_MEMORY.md § Manual › Kit: "ETA early November (Alex 10-22; was Nov 20–Dec 24)".
- Evidence: as of 10-21/10-23 the pre-B00 checks are still pending (PROJECT_MEMORY bring-up list), and the run is 157.0 h ≈ 16 printer-days ≈ 3–4 weeks (index :153). An early-November kit lands mid-run, so index row ordering (rows 14–31 "not one of them waits for a plate"), Ch 00's "every bin already full", Ch 01's "all 22 plates … came off the Prusa before the cartons arrived" and plan §2 no longer follow.
- Fix: needs Alex. Minimum text fix: replace the three ETA strings with "early November 2026 (Alex, 2026-10-22)" and :155/:160's arithmetic; then decide whether the timeline keeps numeric order (build waits on plates) or reorders so Ch 01–Ch 05's batches (B00, B01, B02-P1/P3, B03, B04) print first. Correction #26 (:255) is history and can stay, with a new correction row for the 10-22 date.

### G1-02 major — Ch 00's B00 prerequisite still describes the superseded Gate B (bearings bought, bearing row passed pre-kit)
- docs/manual/00-before-you-start.md:18 "**Gate B** (Step B00.7 — the 625-2RS bearing in the `z_drive_retainer_a` bore and all seven inserts …, **on the bearings and inserts ordered at Step 00.9**) are both long passed by kit day … Steps **00.13**–00.16 *are* Gate B's insert item. **One row of Gate B is left for kit day**: the `MGN12_rail_guide`".
- vs the same file :96 ("the **two kit-day rows of Gate B** … a 625-2RS and an MGN12 rail out of carton 1"), :414 (00.9: "*(nothing to buy for Gate B)* … The 625-2RS bearing and the MGN12 rail are kit parts"), :92/:565 (00.13 is kit day, the LDO tip ships in the kit), Checkpoint :1110; index correction #29 (:258) and row 14 (:78); plan §1.4 :209–210.
- Fix (:18): "**Gate A** (the cube, Step B00.5) and Gate B's caliper and insert rows (Step B00.7 — the `z_drive_retainer_a` pocket calipered against its 16.30 mm STL nominal, and seven KADRICK inserts in the `Heatset_Practice` coupon; nothing bought) are long passed by kit day, and all 22 plates are printed and binned. Steps 00.14–00.16 *are* Gate B's insert row. **Two rows of Gate B are left for kit day**: the 625-2RS thumbed into `z_drive_retainer_a` and the `MGN12_rail_guide` on a real MGN12 rail, both out of carton 1 before the inventory starts."

### G1-03 major — 12.11 and 13.3 ask for "two people" at a power-on that 00a.2 makes one-adult-only
- docs/manual/12-software.md:315 "Printer upright, **two people**, hands out: cord into inlet, then wall."; docs/manual/13-initial-startup.md:135 "**Two people**: one on the switch, one watching with hands out."
- vs docs/manual/00a-mains-safety.md:83 (12.11 through Checkpoint 12 "are adult-only"; she is not in the room), :84 ("She is not beside the machine at any power-on — 10.23, 12.11 and 13.3. One adult … nobody else within reach of the machine"), Checkpoint 00a :377; Ch 10 10.23 (:688 in 10-wiring.md) follows the rule.
- Evidence: the build pair is Alex and his daughter (00a.2, 00.30). 12.11 carries no "Who is in the room" callout, unlike 10.1/10.17/10.23/11.67/14.30.
- Fix: 12.11 step 2 → "Printer upright, one adult at the machine, hands out: cord into inlet, then wall." plus the standard ⚠ Who-is-in-the-room callout. 13.3 step 1 → "One adult on the switch, standing to the side; nobody else within reach of the machine ([00a.2](…))."

### G1-04 major — "Switch off at the wall, not the rocker" (00a.12) contradicts every power-on step
- docs/manual/00a-mains-safety.md:353 "Smoke, a hot smell, buzzing or click-cycling | Switch off at the **wall**, not the rocker, and unplug".
- vs 10-wiring.md 10.23 table "Any buzz, click-cycling or smell → rocker OFF, then pull the plug at the wall"; 13-initial-startup.md:141 "switch off at the inlet immediately"; 00a.11 Ritual 2 (:332) "hand on the rocker … Anything wrong: switch off at once".
- Evidence: every ritual puts the hand on the rocker; the inlet's rocker is double-pole (00a.10 :304), so it is the fastest isolator. A builder at 10.23 gets two different first actions for the same symptom.
- Fix (:353 "Do this first"): "Rocker **off** at once (your hand is already on it), then unplug at the wall."

### G1-05 major — Ch 13's connector swaps at the board say only "power down", against 00a's touch rule
- docs/manual/13-initial-startup.md:54 "means: power down, swap, power up"; :451, :649 ("**power down**, exchange the A and B connectors at the board"), :1717, :1725.
- vs docs/manual/00a-mains-safety.md:334 "To look or touch: power off, unplug, read 0 V held ten seconds, as at 10.73"; 14-calibration.md 14.30 (:1253–1271) opens the same bay after Ch 11 with the full ritual (rocker off, unplug, 0 V for 10 s, helper out of the room).
- Evidence: the Leviathan sits beside the PSU's exposed L/N/⏚ block and the SSR screws (00a.11 :323); by Ch 13 the bottom panel is on, so a swap means opening the bay on a plugged-in machine.
- Fix: define it once in Ch 13 Read first (:54): "…means: rocker off, unplug, meter 0 V across PSU +V/−V for ten seconds as at [11.67](…), swap, close, plug in, power up ([00a.2](…): one adult only)." and point :451/:649/:1717/:1725 at it.

### G1-06 major — Ch 00's tool list misses tools later chapters stop on, despite its "no later chapter stops for a missing tool" promise
- docs/manual/00-before-you-start.md:3 ("so that … no later chapter stops for a missing tool"), Tools :22–35 and 00.8 table :368–387 (no row for any of the below).
- Used but never listed in Ch 00: **PH2 (and PH1) Phillips** — PSU terminal block and SSR terminals (09-electronics-bay.md Tools, 10-wiring.md:26); **hacksaw/fine saw + file** — DIN rails cut to length, no length published (Ch 09 Tools :33, 09.5); **SD card reader** — Ch 12 Tools and 12.1 Parts (PROJECT_MEMORY's pre-kit buy list names "32 GB A1 microSD + reader"); **ABC fire extinguisher** — required at 12.11 Parts, 13.1, 00a.12 ("Buy an ABC extinguisher"); **small hammer** — Clicky-Clack dowels/bushings (Ch 11 Tools); **rubber/nylon mallet** (Ch 01 Tools); **steel tape ≥ 2.2 m** (Ch 01 ≥1 m, Ch 07 ≥2.2 m); **craft knife + plastic scraper** (Ch 03); **label maker** (Ch 10, optional vs kit tags); consumables **solder** (Ch 11 Nevermore bridge PCB) and **super glue** (Ch 11 magnets) are missing from 00.9.
- Fix: add 00.8 rows "PH1 + PH2 Phillips screwdrivers | Buy if not owned | Ch 09 (09.17 SSR, PSU terminals)", "Hacksaw or fine-tooth saw + flat file | Buy if not owned | Ch 09 (09.5 DIN rail length)", "microSD/SD card reader | Buy if not owned | Ch 12 (12.1)", "ABC fire extinguisher | Buy | Ch 12 (12.11) — first power-on of the boards", "Small hammer; rubber or nylon mallet | Buy if not owned | Ch 01 (mallet), Ch 11 (hammer)", "Steel tape ≥ 2.2 m | Buy if not owned | Ch 07 (belt cut)", "Craft knife, plastic scraper | Buy if not owned | Ch 03 (03.9)"; add solder and super glue to 00.9.

### G1-07 major — README tells a reader to run `build_plates.py` bare, which AGENTS.md forbids
- README.md:19 "Rebuild the lot with `python3 slicer/fetch_stls.py && python3 slicer/build_plates.py`".
- vs AGENTS.md › Printing and slicing: "never drop `--from-3mf`: bare, it re-packs every plate and loses the GUI arrangements"; PROJECT_MEMORY § Conventions on record ("`build_plates.py --from-3mf [ids]` only, never bare").
- Fix: "Rebuild the lot with `python3 slicer/fetch_stls.py && python3 slicer/build_plates.py --from-3mf` (re-derives every plate from its committed, GUI-arranged project; never run it bare — that re-packs every plate and discards the arrangements)."

---

### G1-08 minor — 00.6 bins the V2 USB-adapter cover in `09-bay`; it is in `08-CW2`
- docs/manual/00-before-you-start.md:303 "prints the correct **V2** `usb_adapter_mount_partial_cover.stl` into bin `09-bay`".
- vs the same file's Checkpoint :1104 ("found in bin `08-CW2` (B07-P1)"), slicer/bins.py:260, B07 page :25/:129, Ch 09 parts table :50, Ch 10 parts table.
- Fix: "`09-bay`" → "`08-CW2`".

### G1-09 minor — Index "Dependencies inside B02" sends three parts to the wrong chapter
- docs/manual/00-index.md:143 "the Z belt clips and chain retainers gate Ch 06 Part A; and the belt guards, fan grills, keystone blank, **TFT faceplate** and door `Handle` are not needed until Ch 11".
- vs bins.py: `[a]_z_belt_clip_upper_x4` → 05-XY (Ch 05 Steps 05.19–05.23; Ch 05 prereq names "the four upper Z-belt clips"); `[a]_z_chain_retainer_bracket` → 10-chains (fitted at 10.64, only staged in Ch 06); `[a]_faceplate` → 10-tft, needed at 10.50 (index row 25 itself says so); `[a]_cable_cover` (P1) → 07-X is not mentioned.
- Fix: "…the cable bridge, endstop pod and the four upper Z belt clips off P3 go to Ch 05; `[a]_cable_cover` off P1 to Ch 07; the Stealthburner accent parts off P1 and P3 to Ch 08; **B02-P2** gates Ch 04 (A/B tensioners); the four lower Z belt clips gate Ch 06 Part A; the chain retainers and the TFT faceplate are Ch 10 (10.50, 10.64); the belt guards, fan grills, keystone blank and door `Handle` are not needed until Ch 11."

### G1-10 minor — B05's rail stops vanish from the sort lines and from Ch 02's batch list
- docs/manual/00-index.md:58 (row 9) "sort B05 into 06-Z-joints and 10-chains"; :87 (row 17) and :173 (chapter table) Ch 02 needs "B00, B01, B02-P1, B02-P3"; docs/manual/00-tonight.md:79/:178 (from B05.5) "the rail stops stay bagged".
- vs bins.py (`z_rail_stop_x4.stl` → 02-Z0…02-Z3), B05 page sort table :91–94, Ch 02 parts table :58 "batch **B05**, fitted at Step 02.10", Ch 00.11 :491 (B05 → 02-Z0 … 02-Z3).
- Also row 11 (:66) sorts B07 into "08-CW2, 09-bay, 10-lights and 11-finish" — bins.py adds spare-alt (`usb_adapter_mount`), which B07.7 itself names.
- Fix: row 9 "sort B05 into 02-Z0 … 02-Z3 (rail stops), 06-Z-joints and 10-chains"; rows 17 + table "…B02-P3; B05 `z_rail_stop_x4` (optional, Step 02.10)"; B05.5 Pause "…rail stops in the four 02-Z bins"; row 11 "…11-finish and spare-alt".

### G1-11 minor — "eleven bins" for B02 (B02.9 Pause, mirrored in Tonight); it fills 17
- docs/manual/print/B02-accent-parts-orange.md:234 "sorted into their eleven bins"; docs/manual/00-tonight.md:67, :163.
- vs B02.9's own three sort tables (02-Z0–Z3, 07-X, 08-SB, 10-tft, 04-A, 04-B, 11-fans, 11-door, 05-XY, 06-Z-joints, 08-CW2, 10-chains, 11-skirts, spare-alt = 17) and `_batch_bins()["B02"]`; Ch 00.11 :488 lists the same 17.
- Fix: "eleven" → "seventeen" (Tonight regenerates).

### G1-12 minor — Plan §2: the minimum-to-start-building figure is the old model's
- docs/voron-print-plan.md:240 "**B00 + B01 + B02-P1 + B02-P3** ≈ 34 h of printing".
- vs the same plan's sliced figures: 4.0 + 22.8 + 7.0 + 7.6 = **41.4 h** (§3 headers; estimates.csv).
- Fix: "≈ 41 h of printing".

### G1-13 minor — Plan §5.1 names the wrong part as the one rotated on B08-P1 (verified against the 3MF)
- docs/voron-print-plan.md:748 "plate B08-P1 needs it (`side_fan_support` turned 90°)".
- vs index correction #18 (:247: `rear_center_skirt_350` rotated, "as first written this row named the wrong part"); measured: in `slicer/plates/B08-P1.3mf` the rear skirt mesh is 66.8 × 182.0 mm against its STL's native 182.0 × 66.8 (rotated), `side_fan_support` is 72.0 × 180.0 in both (not rotated).
- Fix: "(`rear_center_skirt_350` turned 90° about Z, standing front-to-back beside an unturned `side_fan_support`)".

### G1-14 minor — Plan §9 CSV has B08 at 398 g; every other figure is 399 g
- docs/voron-print-plan.md:942 `B08,…,4,29.2,398,…` vs :927 (table 399), :510 header (399 g), plate rows 99+108+122+70 = 399, TOTAL 1813.
- Fix: 398 → 399.

### G1-15 minor — Plan tells you to test a panel clip before printing B09; the build defers that test to kit day
- docs/voron-print-plan.md:589–590 "snap one clip of each thickness onto an extrusion with a 3 mm panel offcut and the right foam tape **before you commit to printing all 31**"; :789 (§5.2 B09) "**before** printing all 31".
- vs index row 12 (:71) "the panel-clip test (extrusion, panel offcut, foam tape) waits for kit day"; B09.12/B09.13 (Tonight :205–206); B09 prints pre-kit and needs kit extrusion, panel and tape for the test.
- Fix (:589–590): "…snap one clip of each thickness onto an extrusion with a panel offcut and the right foam tape on kit day, before Ch 11 — the clips print before the kit, so a wrong thickness costs a 4 h reprint, not a stall." Same wording at :789.

### G1-16 minor — Plan §5.2 B06 checkpoint presses the Klicky magnets; the build bags Klicky unbuilt
- docs/voron-print-plan.md:786 "Klicky: magnets pressed **below** the plastic surface, polarity consistent, and the probe must attach/detach cleanly from the AB mount."
- vs index row 9 (:59) "**bagged as the alternative probe** (Ch 08.54), no magnets pressed"; Tonight :182–183 (B06.4/B06.5 "No magnets pressed"); PROJECT_MEMORY "Probe stays stock".
- Fix: "Klicky: count the set against the table and bag it as the alternative probe (Ch 08.54); no magnets are pressed in this build."

### G1-17 minor — Plan states Live Adjust Z is not saved; the slicer page and B00 treat it as unverified
- docs/voron-print-plan.md:188 "note the nudge is *not* saved for the next print" (also B00 page :429).
- vs docs/manual/print/00-slicer-setup.md:198 "is kept per sheet `(verify on bench)`" and B00 pre-checks :126 (a check that "settles" it); PROJECT_MEMORY lists "per-sheet Live Z storage" as unverified.
- Fix (:188): "…Live Adjust Z — whether the nudge is kept per sheet is settled by the B00 pre-check (item 3); either way, fix the cause …".

### G1-18 minor — Index row-1 rationale still counts two pre-B00 checks
- docs/manual/00-index.md:141 "Row 1's two checks (belt pluck, hot first layer) confirm the machine …".
- vs row 1 itself (:27), :7, plan §8 :874 ("**Three checks**"), commit e14ef4af (loadcell test added).
- Fix: "Row 1's three checks (belt pluck, loadcell heater noise, hot first layer) confirm …".

### G1-19 minor — Checkpoint 00a is a pre-kit gate in the index, but three of its lines need the kit
- docs/manual/00-index.md:35 (row 3, rows 1–13 are pre-kit) "*Gate:* Checkpoint 00a"; :171 "No kit part, no printed part — doable before the kit".
- vs docs/manual/00a-mains-safety.md:382 ("the M4×6 bed PE screw was confirmed present at Ch 03 Step 03.6"), :384 ("VE0508 ferrules located in the kit"), :309 (00a.10 Check: fuse rating read off the drawer into the log).
- Fix: row 3 Gate → "Checkpoint 00a, except its three kit lines (ferrules, the 03.6 PE screw, the fuse rating), which close on kit day and before Ch 09"; or mark those three Checkpoint lines "(kit day)".

### G1-20 minor — 00a.3 quotes Ch 10 text that does not exist, and its "OL is the pass" clashes with Ch 10's L↔N rule
- docs/manual/00a-mains-safety.md:114 "Ch 10's tool list asks for "at least 2 MΩ", but 10.13 wants to see the bed heater read *"well above 10 MΩ"* … (anything higher shows `OL`, which is the pass)"; :43 "Checkpoint #1 is seven meter measurements".
- vs 10-wiring.md:24 ("a 2 MΩ or 20 MΩ resistance range … The L↔N pass at 10.19 and 10.78 is a number on that range, not `OL`"), 10.13 table ("`OL` on your meter's highest Ω range"; no 10 MΩ figure), :598 (10.19 Check "L↔N reads 100 kΩ or more, **or `OL`**" — itself at odds with :24); 10.17–10.23 is seven steps, of which 10.17 is setup and 10.23 the power-on.
- Fix (:114): "**Resistance range:** Ch 10 asks for a 2 MΩ or 20 MΩ range you can select by hand. 10.13 wants `OL` from the bed heater to earth on the highest range, 10.19 wants L↔N at 100 kΩ or more, and 10.76 reads thermistors up to 162 kΩ. A 20 MΩ meter turns more of those passes into numbers you can log." (:43) "…is five meter checks and one plug-in on an unplugged machine". Ch 10 owner to reconcile :24 vs :598.

### G1-21 minor — 00a's power-on and confirm-dead lists predate the exhaust add-on's 14.30
- docs/manual/00a-mains-safety.md:323 "the only DC-volts readings in the build are the confirm-dead 0 V at 10.24, 10.73 and 11.67"; :83 adult-only list ends at 11.67; Checkpoint :377.
- vs 14-calibration.md 14.30 (:1253–1271: opens the bottom panel, meters DC V, links back to 00a.2 as adult-only).
- Fix: ":323 … at 10.24, 10.73, 11.67 and, for the exhaust add-on, 14.30"; add "and the add-on's shut-down at [14.30](…)" to :83 and Checkpoint :377.

### G1-22 minor — Two chapter headers miss prerequisites the index gives them
- 09-electronics-bay.md:18 Prerequisites: no Ch 00a, while index :108/:181 ("Ch 00a"), 00a title "read before Chapter 09" and Checkpoint 00a :374 ("Do not open Ch 09 until every line is ticked").
- 08-toolhead.md Prerequisites (:20) list B02, B06, B04 only, while index row 23 (:105) needs "B07 `usb_adapter_mount_partial_cover`", fitted at 08.64 (bins.py :352).
- Fix: Ch 09 add "- **Ch 00a — Mains safety**, Checkpoint 00a ticked (who lands the mains, room rule, tested meter)."; Ch 08 add "**B07-P1** (`usb_adapter_mount_partial_cover`, Step 08.64)".

### G1-23 minor — Ch 11 says B08 is 6 plates
- 11-skirts-panels-door.md:21 "**Print batch B08** — skirts and front modules (6 plates, 29.2 h)".
- vs index :209, plan :510 and :927 (4 plates since correction #25).
- Fix: "(4 plates, 29.2 h)".

### G1-24 minor — 00.8 "First needed" and 00.9 notes understate where tools are used
- docs/manual/00-before-you-start.md:380 Multimeter "First needed Ch 10"; vs 00a.3–00a.4 (bought and proved live pre-kit, index row 3) and 08-toolhead.md Tools ("Multimeter (continuity and thermistor resistance)").
- :412 Loctite 243 "Ch 02, Ch 04, Ch 05" vs Ch 08 consumables (Loctite 243) and Ch 11 (thread locker).
- :949/:957 (00.27) require "a plain 2.5 mm" hex driver; 00.8 lists only the ball-end set and the kit L-keys.
- Fix: Multimeter → "Ch 00a (bought and tested before the kit), then Ch 08"; Loctite → "Ch 02, Ch 04, Ch 05, Ch 08"; add "Plain (non-ball) 2.5 mm hex driver | Buy if not owned | Ch 02".

### G1-25 minor — Index lists only 00.23–00.32 as Ch 00's pre-kit steps
- docs/manual/00-index.md:21 "Ch 00's own pre-kit steps (00.23–00.32: …)".
- vs 00-before-you-start.md:92 (00.8–00.11, 00.14–00.16, 00.23–00.32) and Tonight :31/:218 (00.8→00.11 and 00.14→00.16 are `(pre-kit)`).
- Fix: "(00.8–00.11 tools, bench and bins; 00.14–00.16, Gate B's insert row; 00.23–00.32 front matter, log, Discord questions — …)".

### G1-26 minor — README is behind the tree on committed STLs and batch-page count
- README.md:19 "the STLs themselves are not committed (78 MB …)"; :9 "eleven print-batch chapters".
- vs `git ls-files slicer/stl` (41 files: B11's MSS duct STLs, c40f3553, and the add-on Printables pins under `slicer/stl/printables/`); docs/manual/print/ has B00–B11 = twelve batch pages.
- Fix: "the Voron/LDO STLs are not committed (re-fetchable from the pins in `slicer/stl/MANIFEST.sha256`); the B11 duct STLs and the add-ons' upstream files are, because their sources were withdrawn or are pinned for remixing"; "twelve print-batch chapters (B00–B11)".

---

### G1-27 nit — Hands-on total and session total use different bases for Ch 06b
- 00-index.md:152 "59.9 h — the sum of the chapter Time midpoints (Ch 06b's ~1 h … is on top)" = 59.875 without 06b (verified); :158 "≈ 146 sessions" includes 06b's 1 (Ch 06 counted as 9). Tonight :5 repeats 59.9. True hands-on with 06b is 60.9 h. Fix: say "60.9 h with Ch 06b" or exclude 06b's session too.

### G1-28 nit — "24 % filament margin" (index :160) vs the plan's 32 % reprint allowance (plan :709). 24 % is margin over on-hand (587/2400); the reprint allowance the sentence means is 587/1813 = 32 %. Fix: "the plan's 32 % black reprint allowance".

### G1-29 nit — Survey P12 says Fluidd (voron-build-instructions-survey.md:300, CSV :566 name); the build installs Mainsail (Ch 12, index row 15). W1 update (:313) calls 06b.15 a final tension; 06b.15 is "provisional, cold" and final is 14.4.

### G1-30 nit — README CI paragraph (:52) omits two gates check.yml runs: `build_tonight.py --self-test` and `node scripts/check_tonight.mjs`.

### G1-31 nit — 00a.12 (:358) "keep the extinguisher from Step 13.1"; it is first required at 12.11 (Parts: "fire extinguisher, within arm's reach") and in 00a.11 Ritual 2.

### G1-32 nit — Plan B05 "Unlocks … *A/B Belts* (p.124–145)" (:409, §9 :924/:939); Ch 07 needs no B05 part (Ch 07 prereqs B02/B03/B04; index row 22).

Known, still open (not re-reported): 00.11 A5 bag stock tip (:504).

---

## Checked and consistent
- Index timeline vs chapter headers: every row's Time and Sessions match the chapter header and the `Pause:` count per Part (Ch 00 9, 00a 2, 01 4, 02 11, 03 4, 04 7, 05 12, 06 8+1, 07 5, 08 10, 09 8, 10 14, 11 12/5/+3, 12 2+7, 13 11/+4, 14 14/+6); Pause minutes fall inside each Time range.
- Critical path: 146 sessions and 59.9 h recomputed from the headers; 157.0 h / 22 plates / 1813 g + 279 g; 2.7 weeks at 22 h/week.
- Index batch table and rows 2–13 hours/plates vs plan §3/§9 and estimates.csv; B11 rows 32/33 (11.9 h + 13.1 h = 25.0 h, plate split P1–P3 / P4–P5) vs plan §3 B11 and §9 CSV.
- Plan §1.4 "58.4 h and 763 g" (B01 + B03–B06); §4.3 cumulative grams and spool #1/#2/#3 stubs (133 g, 27 g, 454 g, 748 g at B01-P1); index rows 8/11/12 spool staging; B02 "49 accent parts" and P3's "29".
- Plan §4.2 add-on draw (239 g black, 120 g blue) vs the four add-on READMEs (66.0 + 38.5 + 106.7 + 28.7 g black; 34.6 + 84.7 g blue); §6 side spool + camera 6 parts / ~220 g / ~14 h.
- Gates: Gate A releases B02, B07, B08–B10 and Gate B releases B01, B03–B06 consistently across index table, rows 4–13, plan §1.4/§9 and Tonight; Gate B kit-day rows (bearing press, MGN12 rail) consistent in index rows 2/14, Critical path (b), Ch 00 :96/:1110, plan §1.4 (Ch 00 :18 excepted, G1-02).
- Ch 00.11 batch → bin table vs `check_docs._batch_bins()` (all 12 batches) and the add-on bins; 35 bins / 30 A5 / 6 B5 / 2 boxes consistent in index row 2, 00.11 and Checkpoint 00.
- Ch 00.3 counts (283 M3×8, 135 M3 roll-in, 80 M5 roll-in, 75 M3 hammerhead, 46 spacers, 153 inserts, 100 zip ties) and 00.26 (20 F695, 12 625-2RS) vs `ldo-350-bom.yml`.
- Camera cable 3 m in 00.8, index row 25, Ch 10 prereq and 10.81; add-on hours in index rows 28/30/31 vs Ch 11/13/14 headers and plan §6.
- Mains: 00a step references (10.1–10.24, 10.66, 10.69, 10.71, 10.73–10.80, 11.67, 12.11, 13.1, 13.3, 03.6, 09.5, 09.11, 09.17) resolve and match; adult-only callouts at 10.1/10.17/10.23/11.67/14.30; PSU terminal order L, N, ⏚ (10.9); M4×6 bed PE screw (03.6); G3NB-210B-1 10 A (09.17); five VE0508 ferrules (09.35); frame-PE placement vs 10.16; inlet fuse/rocker properties vs 10.5.
- Decisions: PrusaSlicer 2.9.6 only (plan §1.3), Galaxy Black + blue accent with orange spare, B11 layout v3 PETG V0 outside the run, Clicky-Clack, Nevermore + LDO exhaust cover, stock Omron probe with Klicky bagged, add-ons outside the plates and never printed ahead.
