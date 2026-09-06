# F8 — Print side, index/Tonight planning, glossary/troubleshooting (Fable read-through)

Scope: `docs/manual/print/*.md`, `00-index.md`, `00-tonight.md`, `15-troubleshooting.md`, `16-glossary.md`, `docs/index.md`.
Evidence checked, not recalled: unzipped `slicer/plates/{B00-P1,B02-P2,B08-P1,B10-P1}.3mf` (Slic3r_PE.config + per-object model config), `slicer/estimates.csv`, `slicer/OVERRIDES.md`, plate PNGs, `scripts/build_tonight.py`, `slicer/plates.py`, Ch 02/08/11 text, Prusa ASA KB + Core One loadcell KB (fetched), `lint_manual.py` (0 findings), `check_docs.py` (OK), and a link+anchor sweep of every internal link in the reviewed files (0 broken of ~400; mkdocs not on PATH so the sweep used python-markdown slug rules).

Counts: BLOCKER 1 · MAJOR 13 · MINOR 12 · IMPROVE 4.

---

### F1 · BLOCKER · print/00-slicer-setup.md:Calibration sequence (items 5–7) + B00.5 + B00 Read first
Persona: first-time
Quote: "Only when all seven pass, start B01." / "nothing proceeds until all seven pass" / index: "all eleven print batches can run before the Voron arrives"
Problem: Three of the seven gate items need the kit — `Heatset_Practice` needs M3×5×4 inserts (Ch 00: "from the 153 supplied"), `MGN12_rail_guide` needs "the real MGN12 rail", `z_drive_retainer_a` needs a 625-2RS. On day 1 with no kit the process deadlocks; the realistic failure is that the builder shrugs, starts B01 on a 4/7 pass, and 22.8 h / 301 g of Z-drive bodies print against an unverified bore fit — exactly the rework the gate exists to prevent.
Fix: Split the table into **Gate A — no kit needed** (cube X/Y, cube Z, first-vs-mid delta, corner snap) and **Gate B — kit needed** (inserts, MGN12 rail, 625-2RS). Rule: "Kit not here? Pass Gate A, then print B02 (orange, no press fits) and B07 (no bearing seats) while you wait. Do **not** start B01, B03–B06 until Gate B passes." Alternative one-liner: "Order 2× 625-2RS + 10× M3×5×4 inserts with the filament (≈$5) so Gate B can run before the kit lands." Apply the same split to B00.5 Check and Checkpoint B00.

### F2 · MAJOR · 00-index.md:The timeline (embedded `assets/diagrams/11-build-timeline.svg`)
Persona: first-time
Quote: SVG text: "B00 — Calibration & jigs · 3.5 h print", "B01 … 19.4 h print", "B08 … 25.5 h print", "134.3 h"; rows directly beneath: "4.0 h", "22.8 h", "29.1 h", "157.1 h"
Problem: The diagram at the top of the planning page still carries the pre-slice throughput-model numbers (every batch 10–15 % low, total 134.3 h). A first-timer sees two figures for the same plate on one screen and does not know which the ledger and Tonight use. `diagrams/MANIFEST.md:241` repeats 134.3 h.
Fix: Regenerate the SVG from `slicer/estimates.csv` (the source of the row numbers) and add the SVG to `slicer/check_docs.py`'s coverage so it cannot drift again; fix MANIFEST.md line 241.

### F3 · MAJOR · 00-tonight.md (generator `scripts/build_tonight.py`) + 00-index.md intro
Persona: first-time
Quote: "**If you have 30 min:** Ch 00 — Step 00.1 → Step 00.6 · ~40 min · leave-state: both cartons inventoried…"
Problem: (a) Day 1, kit not landed: Tonight's only answer is "inventory the cartons" — it has no print-side sessions at all because the print chapters carry no `Pause:`/`Sessions:` lines and the generator only walks `docs/manual/*.md`. The index says "start at print/00-slicer-setup.md if the kit has not landed" and then tells you to keep Tonight open; the two disagree. (b) The 30-min bucket offers a 40-min segment: `_plan_for_budget` always takes the first segment (`if not picked or …`). (c) "By chapter (timeline order)" is filename order — Ch 00a is listed second (index row 20) and Ch 12 after Ch 11 (index rows 22/25). (d) Heading "Chapter 00a-mains-safety — 00a-mains-safety": `_CHAPTER_TITLE_RE` requires `\d+` and misses `00a`.
Fix: Add to every print chapter a `**Sessions:**` line and `Pause:` lines after the Load step ("Pause: ~15 min since the last pause — plate B00-P1 sliced and started, first layer watched; ~4 h to go. Do not open the door mid-print; come back for Step B00.5.") and after Inspect; make `_chapter_files()` include `print/B*.md` and `print/00-slicer-setup.md` (one 30-min segment: wizard + open B00-P1 + slice). Add a "**Kit not here yet**" planner block that draws only from print chapters, 00.7–00.12 (flat reference, tools), Ch 00a and Ch 12 Part 1. Change `_plan_for_budget` to skip a first segment that exceeds the budget (offer the next one that fits, or say "nothing fits in 30 min — next segment is 40"). Fix the title regex to `(\d+[a-z]?)`. Order chapters by the index's row order (read `00-index.md` or a static list), not by filename.

### F4 · MAJOR · print/B02:B02.4, B02 Read first, B07.4, B07.6, B10.2, B10 Read first (vs 00-slicer-setup § Orientation & brim)
Persona: first-time
Quote: "**Add a 5 mm brim to `Handle`** only" / "Apply 5 mm brim to `Hinge-L-sleeve-2X`, `Hinge-L-solid-2X`, and `Latch`" / "**Brim the 100 mm mounts**" — vs — "These brims are **already set per object** inside `slicer/plates/*.3mf` — you do not apply them by hand"
Problem: The 3MFs already carry the brims (verified: `Slic3r_PE_model.config` has `brim_width=5` on Handle in B02-P2, `=3` on both parts of B08-P1, `=5` on the five tall parts of B10-P1; global `brim_width = 0`). A first-timer reading "Add"/"Apply" will hunt for the setting and most plausibly set the *global* brim (Print Settings → Skirt and brim), which brims every flat fan grill on the plate — and then fails B02.4's own Check ("Brim applied only to Handle"). Conversely, B07.2 (wago mount), B09.2 (plenum) and B09.6 (grill) never mention a brim although the projects have one (`estimates.csv brim_mm = 3`), so the preview shows something the text did not predict.
Fix: Replace every imperative with the confirmation form used in B08.2: "5 mm brim on `Handle` — already in the project; check the preview shows the outline on `Handle` only." Add the same one-liner to B07.2, B09.2, B09.6. In 00-slicer-setup § Orientation & brim add: "If you ever need to add one by hand: right-click the object → Add settings → Skirt and brim → Brim width. Never use the global setting."

### F5 · MAJOR · print/00-slicer-setup.md:Calibration sequence item 3 (also B00.4 Check)
Persona: first-time
Quote: "Run Prusa's built-in First Layer Calibration *with ASA loaded and the chamber at 40 °C+*"
Problem: The Core One+ has no first-layer calibration wizard. Prusa KB: the loadcell "will calibrate the first layer automatically… always done automatically during the mesh bed leveling"; the only manual control is Live Adjust Z (long-press the knob during the first layer), and "the Live Adjust Z will not be saved for the next print". A first-timer will search the menus for a step that does not exist.
Fix: Replace item 3 with: "First layer: the Nextruder loadcell sets Z automatically before every print — there is nothing to run. During B00-P1's first layer, judge it by Ellis' smooth-bottom rule (no gaps, no ridging); if it needs a nudge, long-press the knob → Live Adjust Z, and note that the nudge is *not* remembered — if you needed one, the nozzle-height thumb-screw seat or the sheet offset is the thing to fix before B01." Cite [help.prusa3d.com/article/live-adjust-z_112427](https://help.prusa3d.com/article/live-adjust-z_112427).

### F6 · MAJOR · print/00-slicer-setup.md:Committed projects + B00.1 + B00.2
Persona: first-time
Quote: B00.1: "Load it in the Core One+, confirm the `Prusament ASA @COREONE HF0.4` filament profile is selected" / B00.2: "It carries printer `Prusa CORE One HF0.4 nozzle`, print `0.20mm STRUCTURAL @COREONE 0.4` … and filament `Prusament ASA @COREONE HF0.4`"
Problem: (a) The printer's load-filament screen asks for a *type* (ASA); slicer profile names do not exist on the printer — B00.1 sends the reader looking for one. (b) Nothing says to run Configuration Wizard → Prusa Research → CORE One (+) → tick the **0.4 HF** nozzle variant and install Prusament ASA before opening a project. On a fresh 2.9.6 without the HF variant installed, opening the 3MF triggers PrusaSlicer's missing-printer-profile prompt; choosing the wrong option maps the plate onto whatever printer is active (the estimate Check would catch it, but only after 15 minutes of confusion). (c) The names the GUI will actually show differ from the text: the print preset appears as "0.20mm STRUCTURAL @COREONE 0.4 **(modified)**" and the filament preset is stored as `Prusament ASA @COREONE HF0.4 - Voron black` (verified in `Slic3r_PE.config`) — not the bare name B00.2 quotes.
Fix: New step **B00.0 — One-time PrusaSlicer setup**: "Configuration → Configuration Wizard → Prusa FFF → Prusa CORE One & CORE One+ → nozzle **0.4 HF** (tick it even if 0.4 is already ticked) → Filaments: Prusament ASA → Finish. Then File → Open Project → `B00-P1.3mf`. If a dialog offers to install a printer profile, accept. Expect to see `Prusa CORE One HF0.4 nozzle`, `0.20mm STRUCTURAL @COREONE 0.4 (modified)` and `Prusament ASA @COREONE HF0.4 - Voron black` in the three combo boxes — the '(modified)' and the ' - Voron black' suffix are correct." Rewrite B00.1 to: "On the printer: Load Filament → ASA."

### F7 · MAJOR · print/B06:B06.6 Inspect + Checkpoint B06 (vs Ch 08 Step 08.54, 15-troubleshooting order-of-operations trap)
Persona: first-time
Quote: "Press the 6×3 mm magnets into the Klicky holders using the pressfit-helper jigs … Attach/detach the probe from the AB mount and dock repeatedly." / Ch 08.54: "Set the Klicky bag aside; you are not building it" / Ch 15 trap: "Building Klicky because the parts are on the bench"
Problem: B06's inspect step and three of five Checkpoint B06 items *build* Klicky — the exact trap the troubleshooting index lists. 30–45 min of magnet pressing for a probe the manual says never to fit.
Fix: B06.6 → "Dry-fit the Revo hotend in the printhead front (flat, no rock). Klicky parts: count them against the table, bag them, label **KLICKY — alternative only, see Ch 08.54**. Do not press magnets." Drop Checkpoint items 2–4, keep "Klicky set bagged". Second-time (IMPROVE): move B06-P2 (4.2 h, 51 g) out of the critical path to an optional "B11 — alternatives" plate; it also removes the predicted spool-#1 runout from the ledger.

### F8 · MAJOR · print/README.md:batch table "hard prereqs" (vs 00-index timeline rows 3/5, B01 header)
Persona: first-time
Quote: README: "B01 | … | hard prereqs: **B00;B02**" / index row 3: "B01 — Z drive assemblies · needs: B00" / B01: "**Prerequisites:** B00 printed and the seven-item calibration gate passed"
Problem: The README column is the *assembly chapter's* prerequisite list copied from plan §9, but it is labelled as a print prerequisite, so it says the orange day must precede B01 while the timeline prints B01 first. Same for B03 ("B00;B02"). A first-timer cannot tell whether they may start B01-P1 tonight.
Fix: Rename the column "assembly chapter needs" or replace its contents with print-order prerequisites (B01: B00; B03: B00; B04: B00; …) and put the chapter-level list only in the index's Chapters table where it already is.

### F9 · MAJOR · print/README.md:Spool ledger, "Two exceptions"
Persona: first-time
Quote: "Two exceptions, where you start on a fresh spool whatever is left: **B01-P1** — 15.2 h and 201 g of Z-drive bodies."
Problem: The ledger three lines down puts B01-P1 on spool #1 at 748 g → 547 g. Plan §4.3 is conditional ("*if a runout would land inside B01-P1* … start on a fresh spool"); the README made it unconditional. A literal reader opens spool #2 for B01-P1 and every "remaining" and both runout predictions below are wrong from plate two onward.
Fix: "B01-P1 needs ≥ 201 g on the spool at start (the ledger shows 748 g — fine). If a reprint or extra plate has pushed the active spool under ~230 g, start B01-P1 on a fresh one and re-derive the ledger from your weighings."

### F10 · MAJOR · print/B01:B01.8 Label and bin (and Checkpoint B01 last item)
Persona: first-time
Quote: "Group per Z-axis (4 identical sets): `z_drive_main_a` + `z_drive_main_b` + `z_drive_retainer_a` + `z_drive_retainer_b` + `z_motor_mount_a` + `z_motor_mount_b` + …"
Problem: There are two `a` and two `b` of each part; the sets are **mirrored**, not identical, and each corner takes *either* the `a` parts *or* the `b` parts. As written the builder tries to make four bags of eight from two of each and cannot. Ch 02.01 then asks for "two mirrored piles — `*_a` and `*_b`".
Fix: "Bin as **two `a` bags and two `b` bags**: each bag = one `z_drive_main_?` + one `z_drive_retainer_?` + one `z_motor_mount_?` + one `z_tensioner_bracket_?` of the same letter. Write the letter on the inside face of each part now (Ch 02.01 asks for it). The four orange baseplates/tensioners join their letter's bag after B02." Checkpoint: "Two `a` sets and two `b` sets, letters marked."

### F11 · MAJOR · print/B09:⚠ Panel-clip mapping + Read first + B09.12
Persona: first-time
Quote: "snap one clip of each thickness onto an extrusion with a 3 mm panel offcut and the correct foam tape **before printing all 31**."
Problem: There is no plate that prints one clip; B09-P4/P5 print all 31 in two 4.2–4.3 h runs, and B09.12 does the test *after* both. The instruction cannot be followed with the committed projects, and it also needs the kit (extrusion, panel offcut, foam tape).
Fix: Either add `B09-P0` (one `corner_panel_clip_4mm` + one `_6mm`, ~15 min, hand-arranged in 2.9.6 from the STLs in `slicer/stl/`) and make B09-P4/P5 conditional on it, or reword: "The mapping is an inference; the test is at B09.12 after printing. Worst case a wrong guess costs one 4.3 h plate (56 g)." Also list which way the mapping fails (clip too loose → panel rattles; too tight → won't seat).

### F12 · MAJOR · 00-index.md:timeline rows 5, 22, 27
Persona: second-time
Quote: row 5: "*While it prints:* Nothing new — Ch 02 is blocked until B02-P1 and B02-P3 land." / row 27: "Ch 11 Part A … needs: Ch 10 Checkpoint #1; B02, B07, B08, B09"
Problem: (a) The 21.8 h B02 stall is not empty: Ch 00a (needs only Ch 00, no printed part) and Ch 12 Part 1 ("needs: the Pi only") both fit there, and the index parks them at rows 20 and 22 under B08. (b) Ch 11 Part A Steps 11.46–11.50 consume `Hinge-L-solid/sleeve`, `Latch`, `Handle-Hinge_*`, `Panel_Clip` — all B10 parts — but row 27's needs omit B10 and row 26 says B10 prints *during* Part A. The 5.7 h plate will usually finish in time, but the column claims independence it does not have.
Fix: Row 5 "While it prints: Ch 00a (mains-safety reading + meter order) and Ch 12 Part 1 (image the Pi) — both kit-light; if the kit is not here, read Ch 01–02." Row 27 needs: "…B08, B09, **B10 by Step 11.46**".

### F13 · MAJOR · print/B00:B00.3 (and B01.3, B04.3, B10.3)
Persona: first-time
Quote: "Confirm the smooth/satin sheet is installed, clean with IPA."
Problem: Prusa's ASA article (fetched): "Heatbed: Use the smooth or powder-coated PEI sheet **with a glue stick**" — the glue is the separation layer because "ASA sticks very well to our print sheets"; without it the first big flat part (B01's 66 mm Z-drive bodies, later the 182 mm skirt) can pull PEI off the smooth sheet. The manual names two sheets as if interchangeable, omits the glue, and its own override table calls "ASA on smooth PEI" the biggest failure mode.
Fix: Decide once in 00-slicer-setup: "Sheet: **satin** (no glue) — or smooth PEI **with a thin glue-stick layer, re-applied every 2–3 plates**. Clean with IPA (satin) / warm water + dish soap then IPA (smooth). Never acetone on the powder-coated sheet." Then B00.3/B01.3/B04.3/B10.3 just say "sheet per 00-slicer-setup".

### F14 · MAJOR · print/B08:B08.2 (vs plate image and 00-index corrections log #18)
Persona: first-time
Quote: B08.2: "**`rear_center_skirt_350` turned 90° about Z** so its 182 mm axis runs along X" / corrections #18: "B08-P1 cannot be sliced without a 90° Z rotation of `side_fan_support`"
Problem: The preview (`assets/plates/B08-P1.png`) shows the rear skirt's long axis running **along Y** (front-to-back), and the corrections log names the other part. Three statements, no two agree; the reader is told to "confirm the plate matches the image" and cannot.
Fix: Read the rotation out of the committed 3MF (`slicer/geom.py` chooses it) and make one sentence true in both places: "In the project the rear skirt stands front-to-back and `side_fan_support` is turned 90° so both fit; neither rotation changes the face on the bed."

### F15 · MINOR · print/00-slicer-setup.md:Calibration sequence item 1, Gen 2 rule (lines 187, 255, 274)
Persona: first-time
Quote: "~134.3 h of ASA is about to run" / "before printing 437 g of skirts (B08)"
Problem: Stale pre-slice totals; B08 is 399 g, the run is 157.1 h. `check_docs.py` only checks README/plan/chapters' headline figures.
Fix: 157.1 h and "399 g of skirts"; extend `check_docs.py` to grep these two lines.

### F16 · MINOR · 00-index.md:timeline rows 5/19/24 and Print batches table (vs print/README.md)
Persona: first-time
Quote: index "B02 … 21.8 h", "B08 … 29.1 h", "B09 … 21.9 h"; README/chapters "21.9", "29.2", "21.8"
Problem: The chapters sum rounded plate hours; the index sums unrounded ones. Both are "right"; a first-timer sees the discrepancy and distrusts the ledger.
Fix: Pick one rule (sum of rounded plate figures, since that is what the reader can add up from the chapter) and add `00-index.md` to `check_docs.py`.

### F17 · MINOR · 00-index.md:Corrections log rows 10 and 17
Persona: first-time
Quote: #17 "Printer preset is `Prusa CORE One 0.4 nozzle`" / #21 "…use the Core One HF presets — `Prusa CORE One HF0.4 nozzle`" ; #10 "B03's plate captions have the pairing the wrong way round"
Problem: #17 is superseded by #21 with no cross-reference; #10 describes a bug that is already fixed in B03 but reads as current.
Fix: #17: append "— superseded by #21 (HF0.4 variant)". #10: "…had the pairing the wrong way round (fixed 2026-09-05; B03-P1 = A side = `front_idler_right_*`)".

### F18 · MINOR · print/B00:B00.2, print/B01:B01.2, print/B07:table row `usb_adapter_mount`
Persona: first-time
Quote: B01.2 "**Parts:** the six items above" (5 files, 7 pieces) / B00.2 "Confirm all six parts are on the bed" (preview shows 8) / B07: "1 file *(contains base **and** cover; kit supplies the base, so you get a spare; base only — cover body superseded…)*"
Problem: Counts that do not match what the preview lists make the reader doubt the load. The usb_adapter_mount cell is unreadable and effectively says "this file is redundant".
Fix: Use the preview's convention everywhere: "6 files, 8 objects". B07: either drop `usb_adapter_mount` from the plate (kit supplies the base; V2 partial cover replaces the cover) or write "optional spare base — 9 g".

### F19 · MINOR · print/B00:B00.6 + print/README.md "unlocks" column
Persona: first-time
Quote: B00.6: 'labelled "Z-drive tooling — Frame"' / README: "B00 … unlocks: Frame"
Problem: Ch 01 Frame needs no printed part (index table says so). B00's parts are consumed in Ch 00 (`Heatset_Practice`, both rail guides at 00.22), Ch 02 (MGN9 guides), Ch 05 (MGN12 guide) and Ch 04 (`pulley_jig`). The bag label sends the jig to the wrong chapter.
Fix: Two bags: "RAIL GUIDES — Ch 00 / 02 / 05" and "PULLEY JIG — Ch 04". README unlocks: "Ch 00 (heat-set practice, rail guides); Ch 04 (`pulley_jig`)".

### F20 · MINOR · 00-index.md:Critical path "Hands-on time 59.5 h" vs 00-tonight.md "~59.4 h"
Persona: first-time
Quote: "**59.5 h** — the sum of the chapter Time midpoints" / Tonight: "~59.4 h hands-on across 18 chapters"
Problem: The sum of midpoints is 59.375; the two pages round differently, and Tonight counts Ch 15/16 as "chapters".
Fix: Print 59.4 in both (or 59.5 in both); exclude reference chapters from Tonight's count.

### F21 · MINOR · 16-glossary.md:S "Skirt", missing rows; print chapters carry no glossary links
Persona: first-time
Quote: glossary "**Skirt** — The ring of printed segments around the base…" vs 00-slicer-setup "Skirt loops … 1 loop, 3 mm gap" and B00.4 "the abort window the 1-loop skirt buys you"
Problem: "Skirt" has two meanings in this manual and the glossary defines only one; the print chapters use the slicer sense first. Also undefined anywhere: **Arachne**, **seam**, **z-hop**, **volumetric speed (mm³/s)**, **purge**, **runout sensor**, **elephant foot** (defined but first matters at 00-slicer-setup, not 14.11). The eleven print chapters contain zero `16-glossary.md#` links, against the convention every assembly chapter follows.
Fix: Add rows "Skirt (slicer)", "Arachne", "Seam", "Z-hop", "Volumetric flow", "Purge line", "Runout"; point Elephant foot's first-matters at `print/00-slicer-setup.md#overrides`. Link first uses in 00-slicer-setup and B00 (`[brim](../16-glossary.md#b)`, `[extrusion multiplier](../16-glossary.md#e)`, `[625-2RS](../16-glossary.md#f)`, `[heat-set insert](../16-glossary.md#h)`).

### F22 · MINOR · 16-glossary.md:R "Revo HF" vs print/B06 "Revo Voron" vs E "E-RV"
Persona: first-time
Quote: "**Revo HF** — The E3D hotend in this kit" / B06: "Revo Voron hotend must sit flat" / index Ch 08 scope: "Revo HF"
Problem: Two names for one hotend, never reconciled; the printhead folder choice (`revo_voron`) hinges on knowing they are the same heatsink.
Fix: One glossary row: "Revo Voron / Revo HF — the E3D Revo Voron heatsink (printhead code E-RV, STL folder `revo_voron`); 'HF' is the high-flow nozzle fitted to it (verify against the kit's hotend box)".

### F23 · MINOR · print/B10:Read first + B10.2 + Checkpoint B10
Persona: first-time
Quote: "Mirror the two `Hinge-L-*` parts in the slicer if you want the door to swing the other way"
Problem: The default swing is never stated, so "the other way" is undefined; the checkpoint asks for a decision the reader has no basis for.
Fix: "As shipped the hinges are on the **left** and the door opens from the right (`Hinge-L`). Mirror both hinge files only if the printer's left side will be against a wall. Decide from where the machine will live, now."

### F24 · MINOR · 15-troubleshooting.md: no "Printing the parts" section
Persona: first-time
Quote: (absent) — the only print rows are VFA and "A skirt or COB mount is bowed"
Problem: The symptoms the reader actually hits in weeks 1–2 (cube oversize before the Voron exists, corner lift, delamination at the snap test, bearing bore too tight/loose, heat-set boss bulging, first layer glassy vs gappy on the Core One) have owners — the "if out of spec" column in 00-slicer-setup — but no symptom-first entry points to them. The traps table also lacks "Starting B01 before the seven-item gate".
Fix: Add a 6-row "Printing the parts (Core One+)" section pointing at `print/00-slicer-setup.md#calibration-sequence-…` rows and B00/B01 Common mistakes; add the gate trap row.

### F25 · MINOR · print/B00:B00.3 (safety, the daughter)
Persona: first-time
Quote: (absent)
Problem: 157 h of ASA in a home; the only mention of the Advanced Filtration Kit is a "do it first" line with no room rule, and nothing tells a 13-year-old what she may touch on the Core One+ (door stays shut mid-print; bed is 110 °C; nozzle 265 °C).
Fix: One `⚠` in B00.3: "ASA off-gasses styrene. Filtration kit fitted, door shut for the whole print, room ventilated between plates; the bed (110 °C) and nozzle (265 °C) stay hot for ~20 min after the end — the helper handles parts, not the printer."

### F26 · MINOR · print/00-slicer-setup.md:STL source of truth + PrusaSlicer 3.0 preview
Persona: first-time
Quote: "Download these exact trees… **record the commit SHA in a text file next to your STLs**"
Problem: Reads as a to-do, but `fetch_stls.py` + `MANIFEST.sha256` + the committed 3MFs already do it; nobody printing from the projects needs this. The 3.0 section is 25 lines a first-timer must read to learn "use 2.9.6".
Fix: Head both sections with "Reference only — you need this only if you re-derive the plates" and move them below the Gen 2 rule; in the version-posture paragraph say "first build: 2.9.6 for everything."

### F27 · IMPROVE · print/*.md Printed-parts tables
Persona: second-time
Quote: "| `pulley_jig.stl` | Voron-2 `STLs/Tools/` | 1 | Black | 2.8 |"
Problem: The bin step asks the reader to sort 29 small orange parts and 31 clips by filename with no picture; `docs/manual/assets/parts/` already holds 151 renders (`pulley_jig.png`, `Hinge-L-sleeve-2X.png`, …) that Ch 02's table embeds at 96 px.
Fix: Prepend the same `![](../assets/parts/<stem>.png){ width=96 }` column to every print-chapter table (generate it in `build_printables.py`; the bin-labels page can reuse it).

### F28 · IMPROVE · 00-index.md:The timeline — "kit not here" path
Persona: second-time
Quote: "Start at … print/00-slicer-setup.md if it has not — all eleven print batches can run before the Voron arrives."
Problem: The alternating rows are the kit-present schedule; the pre-kit schedule (rows 1, 3, 5, 7, 9, 11, 13, 15, 19, 24, 26 back-to-back, with the F1 gate split) is never written down, nor is its elapsed time (6.5 days floor, ~15 printer-days realistic).
Fix: One line under the markers: "**Kit not here yet:** print rows 1 → 5 → 15 (B02 and B07 have no press fits), then 3, 7, 9, 11, 13, 19, 24, 26 once Gate B passes; ~2–2.5 weeks. Fill the gaps with 00.7–00.12, Ch 00a and Ch 12 Part 1."

### F29 · IMPROVE · print/B07 table (`pcb_din_clip_x3`, `usb_adapter_mount`), print/B02 (`[a]_pcb_spacer`, second `keystone_blank_insert`)
Persona: second-time
Quote: "3 *(one clip per file — `_x3` is the quantity; spares, the kit supplies the 4 needed)*"
Problem: ~30 g / ~1.5 h of declared spares of kit-supplied parts sit on the critical-path plates.
Fix: Move spares to the optional plate proposed in F7; B07-P1 shrinks and the ledger's spool-#1 runout disappears.

### F30 · IMPROVE · print/B00–B10 "Pre-print checks" and "Print" steps
Persona: second-time
Quote: B01.3 "Chamber preheated to ≥40 °C, sheet clean with IPA, spool confirmed dry." / B01.4 "Start overnight or during a full workday"
Problem: Eleven near-identical pre-print/print step pairs; the only content that varies is the watch-for line. The chamber gate is enforced by the profile (`chamber_minimal_temperature = 40`, verified), so "confirm ≥40 °C" is theatre after B00.
Fix: Keep the pair only in B00 (where it teaches the routine); elsewhere fold the watch-for line into the Load step's Check and delete the pair. Saves ~40 steps.

---

## Chapter verdicts

- **print/00-slicer-setup.md** — with fixes (F1, F5, F6, F13). Weakest: Calibration sequence item 3 (no such wizard), items 5–7 (kit-dependent gate), "smooth/satin" sheet line.
- **print/README.md** — with fixes (F8, F9). Weakest: "hard prereqs" column, "two exceptions" spool rule, "unlocks: Frame".
- **print/B00** — with fixes (F1, F6). Weakest: B00.1 (profile "on the printer"), B00.5 (gate needs kit), B00.6 (bag label).
- **print/B01** — with fixes (F10). Weakest: B01.8 grouping, B01.2 "six items", B01.3/B01.4 theatre.
- **print/B02** — with fixes (F4). Weakest: B02.4 "Add a brim", Read-first brim line, B02.9 (long unstructured bin paragraph — a table would do).
- **print/B03** — yes as written. Weakest: B03.5 (build A while B prints assumes kit), B03.7, B03 Checkpoint needs F695s from the kit.
- **print/B04** — yes as written. Weakest: B04.5 (needs carriage + shafts from kit), B04.3, B04.4.
- **print/B05** — yes as written. Weakest: B05.4 (needs shaft + extrusion), B05.3, B05.5.
- **print/B06** — with fixes (F7). Weakest: B06.6, Checkpoint B06, B06.4 ("confirm fixed dock variant" — the project decides it).
- **print/B07** — with fixes (F4, F18). Weakest: table row `usb_adapter_mount`, B07.4 "Brim the 100 mm mounts", B07.1 (runout narrative depends on F9).
- **print/B08** — with fixes (F14, F4). Weakest: B08.2 rotation sentence, intro "6 of the 27 plates … are large flat vertical faces", B08.12 "under the tall/narrow list but fine".
- **print/B09** — with fixes (F11). Weakest: ⚠ clip mapping ("before printing all 31"), B09.2/B09.6 unmentioned brims, B09.12 needs kit stock.
- **print/B10** — with fixes (F4, F23). Weakest: B10.2 "Apply 5 mm brim", Read-first mirror line, Checkpoint "swing direction".
- **00-index.md** — with fixes (F2, F8, F12, F16). Weakest: the SVG, row 5 "Nothing new", row 27 needs.
- **00-tonight.md** — no, for the no-kit case (F3); yes once the kit is here except the 30-min bucket bug.
- **15-troubleshooting.md** — yes as written (every "Owned by" link resolves); weakest: no print-side section (F24).
- **16-glossary.md** — yes as written (all step anchors resolve); weakest: Skirt collision, Revo naming, no print-chapter links (F21, F22).
- **docs/index.md** — yes; one stale claim: "Tonight … 30/60/90-minute session planner" is only true for the build side.

## Praise
- B00.2's Check — "the slicer reads 3 h 58 m / 51.7 g … anything else means the project did not load its own configuration" — is the single best line in the print manual; it turns a 60-key override table into one number a first-timer can verify. Keep it on every plate.
- The seven-item gate table with an "if out of spec" column, and the "never negative XY compensation / fix with EM" rule repeated at B00, Ch 14 and the troubleshooting index, is exactly the kind of cross-referenced correctness that survives a tired evening.
- The committed 3MF story is real: per-object brims, `filament_shrinkage_compensation_xy = 0%`, HF0.4 printer + non-HF STRUCTURAL print preset all verified inside the files, and `OVERRIDES.md` maps every key back to a doc line.
- Spool ledger with weigh-in column and predicted runouts; corrections log with dates and "verified against".
- Every internal link and anchor in the six reviewed reference/planning files resolves; lint and check_docs are clean.
