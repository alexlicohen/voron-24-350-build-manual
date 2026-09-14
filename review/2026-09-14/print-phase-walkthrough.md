# Print-phase walkthrough — Home → "all 22 plates in bins" (persona read, 2026-09-14)

Reader order, generated step pages; fixes cite chapter file + step id. Checked on disk: all 22 `slicer/plates/*.3mf` configs, the user's PrusaSlicer printer presets, the two generators, timeline SVG, survey, glossary, review/2026-09-05–06.

## A. Verdict

No — he stalls on the first job: Home and Tonight send him to B00.0, but timeline row 1 (the Gen 2 belt upgrade) has no page, and its only paragraph says "apply the upgrade as soon as the kit lands", which he reads as the Voron kit. Past that, every plate he opens replaces his `- coldstart` printer preset with the 3MF's stock start G-code (all 22 carry it), undoing the 09-13 "bed not aligned" fix on plate 1. From B03 on, the filament-prep steps still name the pre-09-14 spool order.

## B. Findings (ranked by stall likelihood)

`[F1]` 00-index row 1 · 00-slicer-setup § Gen 2 belt-upgrade pause rule · 00-tonight — "My first job has no page, Tonight skips it, and the text says 'as soon as the kit lands'." — Heading → "Gen 2 belt upgrade — the first job (contingency pause below)". Sentence → "Apply it the day the Gen 1→Gen 2 kit (order 1787919456) arrives: firmware ≥ 6.8.1, Settings → Hardware → Edition → Gen 2, belts per the Prusa guide, re-tension, re-square, self-test, input shaper — then B00, whose cube is Gate A." Add a `## Gen 2 first` section (its own page) atop B00-calibration-and-jigs.md with that list as tick boxes; link from row 1. B07 Read-first "Gen 2 upgrade pause point": prefix "Contingency only:". — M

`[F2]` 00-slicer-setup § Committed projects · B00.0 Check · every Load step — "The Printer box reads `(modified)`; nothing says pick my `- coldstart` preset." Every 3MF `start_gcode` is stock (`M115 U6.5.3`, hot M109 waits). — B00.0 Do 4: "Set the Printer box to `Prusa CORE One HF0.4 nozzle - coldstart`; the project's printer section is stock and only a thumbnail is lost." Same standing rule in § Committed projects — or rebuild the 3MFs with the coldstart G-code in `slicer/build_config.py`. — S text / M rebuild

`[F3]` B03.1–B10.1 (Filament prep) vs README § Spool ledger — "B03.1 says spool #2, the ledger #1; B07.1 unloads orange I removed four batches ago; B09.1 puts the runout in P2, the ledger in P1." — Rewrite from the ledger: B03/B04/B05 on #1 (328/211/133 g after); B06 fresh #2, keep #1's 133 g; B07 #2 (550/426); B08 #2 (327→27); B09-P1 is the #2→#3 runout (~27 g on #2); B09-P2–P5, B10 on #3. Move the orange→black unload-and-purge sentence from B07.1 to B03.1. — S

`[F4]` B03.4, B04.5, B05.4, B06.4 + Checkpoints B03–B06 — "Press an F695, slide the 8 mm Z shaft, dry-fit the MGN12 carriage and the Revo heatsink — all kit parts." — Step 00.9 required row: add "two F695-2RS bearings and 100 mm of 8 mm ground rod" so B03.4/B05.4 run now. B04.5, B06.4 become two rows like B09.12: "Now: caliper the seats (F695 13.0 mm, shaft bore 8.0 mm, carriage holes 20 mm apart). Kit day: carriage pattern, heatsink." Prefix those checkpoint lines "(kit day)". — M

`[F5]` 00-tonight § Tonight's planner — "The 90-minute plan ends with Ch 10 Step 10.1, mains wiring; the 30-minute plan starts B00 before the upgrade." — `build_tonight.py`: render "Before the kit" first until kit day; never fill a bucket past the first unticked KIT row. — M

`[F6]` 00-before-you-start.md Pauses at 00.12, 00.16 — "The note calls tools, flat reference, bins and heat-set practice pre-kit, but *Before the kit* never offers them" (only 00.29/00.32 carry `(pre-kit)`). — Add `(pre-kit)` to both; 00.12 gains "Step 00.7 waits for the kit." — S

`[F7]` 00-slicer-setup § Print sheet · B00.3 — "'Decide this once' — I own the kit's sheet and two textured ones; CLAUDE.md already decided." — "Which sheet: the smooth/satin PEI sheet that shipped with the Core One+; the textured sheets are for PLA/PETG." B00.3 Do 1: "Fit the smooth/satin sheet …". — S

`[F8]` 00-slicer-setup § Gate A · B00.5 · B00.2 Check — "I cannot 'corner snap', and where do extrusion multiplier and shrinkage live, and how does a change reach the other 21 plates?" — Row: "Corner snap: grip one corner in pliers and bend it off; the break tears across layers, never peels along one (verify on bench)." After the table: "Extrusion multiplier: Filament Settings → Filament; shrinkage: Filament Settings → Advanced. A changed multiplier is re-entered in every later project (each carries its own filament config); write it on the sheet-edge tape." — S

`[F9]` 00-slicer-setup § Gate B · B00.7 ⚠ — "Shrinkage is 0 % and the bearing is still loose; the table stops there." — "Loose with shrinkage at 0 % → raise extrusion multiplier 1 %, reprint retainer and cube, re-pass Gate A." — S

`[F10]` B00 start Prerequisites — "'none — this is the first batch', but the timeline says row 1 first." — "**Prerequisites:** the Gen 2 belt upgrade (index row 1) done, or the 2026-10-15 contingency taken." — S

`[F11]` B01.1 · README § Spool ledger — "'Weigh the spool' — no scale in any tool list; the ledger's grams are filament, not a scale reading." — Add "kitchen scale, 1 g" to B00/B01 Tools; ledger intro: "Write each new spool's scale reading on its flange; remaining = reading − (new reading − 800)." — S

`[F12]` B01.5 Check · Checkpoint B01 · Checkpoint 00 bullet 2 · 00.30 table — "B01.5 says the deck panel 'is already calipered'; it arrives in December." — B01.5 Check: "All 8 clips on the plate, 3 mm per the BOM; the kit-day caliper decides a 4 mm reprint." Checkpoint 00: "Deck panel calipered on kit day; if 4 mm, `deck_support_4mm_x8` reprinted (8 g, 30 min)." Checkpoint B01 line prefixed "(kit day)". — S

`[F13]` Checkpoint 00 bullet 10 · 00-index § Chapters row Ch 00 — "'B01 is on the Prusa' / 'Gate B runs the same morning', but Kit day says nothing prints." — "Gate B's bore and insert rows passed months ago (B00.7); its rail row is done out of carton 1, then both guides fitted rail-plus-extrusion (00.20)." Chapters row: "Gate B's rail row on kit day". — S

`[F14]` 00-slicer-setup § Gate B row `Heatset_Practice` · Ch 00 Hardware · 00.16 Pause — "'from the kit's 153 (146 remain)' vs B00.7 'leaves all 153'." — "seven of the ten ordered inserts; all 153 kit inserts stay for the build", everywhere. — S

`[F15]` 00-slicer-setup § Calibration sequence · README § Print order — "'reprint of the PLA rail-guide jig' — B00 is all ASA." — "the ASA `MGN12_rail_guide` (3 g, 20 min)". — S

`[F16]` B01.8 ⚠ · B03 start Prerequisites — "'The orange baseplates from B02 are already in these bins' — B02 hasn't printed; B03 says B02 'prints next'." — B01.8: "B02's orange baseplates and tensioners join these bins next batch." B03: "printed one batch earlier, at B02, already in 04-A / 04-B." — S

`[F17]` docs/print/plate-plans.md header · docs/print/checklists.md line 5 — "Plate plans says B00 → B02 → B07 …; everything else says numeric." — `_BATCH_PRINT_ORDER` in scripts/build_printables.py:49 → B00…B10; checklists intro "day-1 and kit-day gates" → "same-week gates (rail row on kit day)". — S

`[F18]` B08 start · 00-index rows 1/14 — "GT1.5 and VFA appear undefined; GT1.5 is not in the glossary." — Glossary row: "**GT1.5 / GT2** — belt tooth pitch in mm; Gen 2 swaps the Core One's 2 mm belts for 1.5 mm, which is what shrinks VFA." Link both at B08 start. — S

`[F19]` B00.4 Do — "4.0 h estimate; nothing says the printer heats 15–25 min first, or how the G-code reaches it." — Do 1: "Slice; Export G-code to the USB stick or Send to printer via Prusa Connect. Expect 15–25 min of chamber heating before the purge (verify on bench); the 4.0 h excludes it. Then watch the first layer 2–3 min." — S

`[F20]` B10 start ⚠ · Checkpoint B10 — "'Open question … (unverified)' on Blue; the survey resolved it 09-05 (line 453)." — "The Clicky-Clack 'Blue' option is the door's aluminium frame colour, matching the blue LDO frame (survey)."; drop the checkpoint line. — S

`[F21]` docs/index.md — "The first page describes tabs; nothing says where to begin." — First line: "**Start here (Sept 2026):** the kit lands late Nov–Dec. Do the Gen 2 belt upgrade, then [slicer setup] and [B00]; plan sessions from [Tonight → Before the kit]." Also "picture, what you're looking at, Parts, Do, Check" → "Do, Parts, Check, then what you're looking at". — S

## C. Expansions

1. **New `## Gen 2 first` page in B00-calibration-and-jigs.md (F1)** — "Before any plate: fit the Gen 1→Gen 2 kit per the Prusa guide. Tick: firmware ≥ 6.8.1 (Info); Settings → Hardware → Edition = Gen 2; belts tuned (Control → Calibrations & Tests → Belt Tuning); gantry squared; self-test and input shaper passed; `- coldstart` preset still selected. Then Step B00.0."
2. **B00.5 collapsed block** — "The 30 mm cube is a ruler for the printer: X/Y say whether walls come out the size the CAD drew (every bearing bore depends on this), Z whether the first layer is squished right, the corner whether layers weld. Every later plate inherits these numbers."
3. **B00.7 collapsed block** — "A 625-2RS is the plain 16 mm bearing in every Z drive. Thumb-pressing one into this retainer is the fit the four Z drives need; if it rocks or needs a press, 22 h of Z-drive bodies would print wrong. Flush, un-bulged inserts mean the iron is right."
4. **Note page "While a long plate runs" (from B01.4, B08.3)** — "Look at the first layer, the corners after an hour, and at bedtime; a lifted corner is a stop, not a wait. Meanwhile: read the chapter the batch feeds, sort the previous plate, label bins."

## D. Contradictions

Each is a finding above with its correct value: print order (F17), spool numbers (F3), Gen 2 timing / B00 prerequisites (F1, F10), start G-code vs `- coldstart` (F2), inserts 153/146 (F14), PLA vs ASA jig (F15), Gate B timing (F13), deck-support timing (F12), orange parts "already binned" (F16), Clicky-Clack Blue (F20), Home's step-page order (F21).

## E. Still open from earlier reviews

- G8 F16 (Ch 00 pre-kit segments absent from the planner): partial — markers on 00.29/00.32 only (F6).
- G8 F6 (Sort steps without a Pause): B00.6, B01.8 fixed; B02.9 and B03.5–B10.6 still none.
- G8 F11 second half: B10 `Handle.stl` row still has an empty Bin cell ("11-door, from B02").
- R5 F6 (five-column override tables on iPad): unchanged; not re-verified on device.
- Verified applied: G8 F1, F2, F3/F4, F5, F7, F8, F9, F14; G1 F2, F5, F12.
