# G8 — Print side, index/Tonight planning, bins, glossary/troubleshooting (Fable re-read after the fix wave)

Scope: `docs/manual/print/*.md`, `00-index.md`, `00-tonight.md`, `docs/print/checklists.md`, `docs/print/bin-labels.md`, `15-troubleshooting.md`, `16-glossary.md`, `docs/index.md`, plan §1.4/§2/§8, `slicer/bins.py`, plate diagrams, the F8 findings.
Evidence, not recall: `Slic3r_PE.config` + `Slic3r_PE_model.config` of B00-P1/B02-P1/B08-P1; `slicer/estimates.csv`; `python3 slicer/check_docs.py` (OK), `python3 slicer/bins.py` (25 bins, 121 STLs, 0 problems), `python3 scripts/lint_manual.py` (0); a link+anchor sweep of the in-scope files (1002 links, 0 broken, python-markdown slug rule); the installed PrusaSlicer (2.9.6; app bundle `config_version 2.4.14`, live vendor bundle in Application Support `2.5.8`) diffed against the project's printer config; `11-build-timeline.svg` rendered (rsvg) and read; plate PNGs B01-P1, B07-P2, B08-P1, B02-P3 read; every chapter's Prerequisites block; `build_tonight.py`, `build_printables.py`, `draw_diagrams.py` read.
Prior-review ids are cited as **F8/F<n>**; this file's own findings are F1–F16.

Counts: BLOCKER 0 · MAJOR 5 · MINOR 9 · IMPROVE 2.

---

### F1 · MAJOR · 00-index.md:The timeline (embedded `assets/diagrams/11-build-timeline.svg`; generator `scripts/draw_diagrams.py` `TIMELINE`)
Quote: index, directly under the image: "Rows are in execution order." SVG rows: 1 B00, 2 Ch 00, 3 B01, 4 Ch 01, 5 B02 … 17 Gen 2 pause … 30 Ch 14; facts strip "59.5 h hands-on", "~15 printer-days printing, elapsed"; footer "Row 17 is the contingency pause".
Problem: The hours were regenerated (F8/F2 numbers are right) but the diagram still draws the pre-split interleaved order from a hard-coded list (`draw_diagrams.py:1679–1713`, 30 rows): no Ch 00a row, B01 at row 3, the Gen 2 pause at row 17, Ch 00 before B02. The index list beneath it now has 31 rows in the new order (B00 → B02 → Ch 00a → B07 → Gen 2 → B08 → B09 → B10 → Ch 00 → B01 …, pause at row 5) and says 59.4 h / ~10 + ~6 printer-days. Two execution orders on one screen, and the row numbers in Tonight ("### 9 · Build — Ch 00") match the list, not the picture.
Fix: Make `d11_timeline()` read the rows from `00-index.md` the way `build_tonight._timeline_rows()` does (same `_ROW_RE`), or rewrite `TIMELINE` to the 31-row order with `needs` from the "needs:" text; facts strip 59.4 h, "~10 printer-days pre-kit + ~6 kit"; footer "Row 5"; `diagrams/MANIFEST.md` entry 11 ("All 30 timeline rows", "59.5 h hands-on") with it. Add the SVG's numbers to `check_docs.py` (F8/F2 asked for this; not done).

### F2 · MAJOR · docs/print/checklists.md (generator `scripts/build_printables.py`)
Quote: docs/index.md: "The print section … has print-ready Checkpoint checklists"; the page's `##` headings: Ch 00, 01, 02, 03, 04, 05, 06, 07, 09, 10, 11, 12, 13, 14.
Problem: The garage-bench sheet has no Checkpoint B00–B10 (Gate A / Gate B are exactly what a first-timer needs on paper on day 1 and kit day), and silently drops Ch 00a, Ch 06b and Ch 08. Causes, all in the generator: `_chapter_files()` globs `manual/*.md` only (no `print/B*.md`); `_CHAPTER_TITLE_RE` needs `Chapter\s+(\d+)` (rejects "00a" and every "Batch BNN"); `_CHECKPOINT_RE` needs the heading to end after one token (rejects "Checkpoint 08 — bench test before anything is powered"); `_checkpoint_items` uses `.search` (first checkpoint only, so 06b is lost).
Fix: Title regex `(?:Chapter|Batch)\s+([A-Za-z]?\d+[a-z]?)`, checkpoint regex `^##\s*Checkpoint\b[^\n]*$`, iterate `finditer`, include `PRINT/B*.md` (print pages titled "Batch BNN — …"), keep print batches in print order after the chapters or in their own section.

### F3 · MAJOR · print/B00:B00.0 Check + 00-slicer-setup.md § One-time PrusaSlicer setup, table row "Printer"
Quote: "Printer | `Prusa CORE One HF0.4 nozzle` | system preset" / B00.0: "Anything else means the project's configuration did not load; reopen it before slicing."
Problem: The project's printer section is not identical to the system preset, so PrusaSlicer will show the printer box as `Prusa CORE One HF0.4 nozzle (modified)` too. Verified by diffing `Slic3r_PE.config` against the resolved `[printer:Prusa CORE One HF0.4 nozzle]`: (a) `thumbnails` carries an extra `640x480/PNG` that `slicer/build_config.py:81` adds on purpose — differs even against the app-bundle 2.4.14; (b) on this Mac the live vendor bundle has auto-updated to `config_version 2.5.8`, whose `start_gcode` differs (`M115 U6.5.3` → `U6.8.1`), so it differs on two keys. A literal first-timer reopens the project, sees the same "(modified)", and is stuck at the first instruction of day 1. (Also: 00-slicer-setup says the installed bundle is 2.4.14 — that is the copy inside the .app; `resolve_preset.py` reads that copy, not the one the GUI uses.)
Fix: Change the table row and B00.0 Check to: "Printer: `Prusa CORE One HF0.4 nozzle` — usually with "(modified)", because the project adds a 640×480 thumbnail; fine." Make the only two 'did not load' signals the bare filament name and the B00.2 estimate. Note the live-bundle version (`~/Library/Application Support/PrusaSlicer/vendor/PrusaResearch.ini`, 2.5.8 today) and that a re-derive should resolve against it. Confirm once in the GUI before B00.

### F4 · MAJOR · 00-tonight.md (generator `scripts/build_tonight.py`) + print/B00:B00.0–B00.2
Quote: Kit not here yet → "If you have 30 min: B00 — Calibration & jigs — Start plate B00-P1 (Step B00.2) · ~5 min hands-on"
Problem: The first executable link a first-timer follows lands on B00.2 (open the 3MF). B00.0 (wizard, HF nozzle, filament install) and B00.1 (Load Filament → ASA, purge) are invisible to the planner because print chapters only emit segments for Load steps and `Pause:` lines, and B00 has no Pause before B00.2. Day 1 is ~20 min hands-on, not 5, and the wizard is the one step that decides whether the project loads its presets (F3).
Fix: Add after B00.1: `Pause: ~15 min since the last pause — wizard run with the 0.4 HF nozzle, B00-P1 open and showing "(modified)" / " - Voron black", ASA loaded and purged clean. Nothing printing.` — `_parse_chapter` will then emit "Step B00.0 → Step B00.1 · ~15 min" ahead of the plate start (boundary logic already handles it; sorted by position). Optionally make `PLATE_START_MIN` a per-batch override so B00's Sessions line and Tonight agree.

### F5 · MAJOR · 00-before-you-start.md:Step 00.11 + Checkpoint 00 (assembly side — read-only here; route to the Ch 00 agent) · also 00-index.md row 8
Quote: 00.11: "Label a bin per chapter … | Print batch | Bins it feeds | … B02 → Ch 02, Ch 04, Ch 05, Ch 08, Ch 11" / Check: "Fifteen chapter bins" / Checkpoint 00: "Chapter bins labelled 00–14 and the batch-to-bin map posted on the wall" / index row 8: "Bag every pre-kit batch by chapter — the bin labels page".
Problem: The print side (README § Bins, every Sort step, the labels, the diagrams) now sorts into 25 named bins (02-Z0 … spare-alt); the receiving end still tells the builder to label fifteen chapter bins and lists bins by chapter number. Same Ch 00 file already carries the new Bin column in its parts table, so the chapter contradicts itself.
Fix: 00.11 → "Label the 25 bins from `print/README.md#bins` (print the bin-labels sheet); the table is the batch → bin map" with the batch-to-bin rows taken from README's "from batches" column; Checkpoint 00 line → "25 bins labelled from the bin-labels sheet, bin map posted"; index row 8 "by chapter" → "into their bins".

### F6 · MINOR · 00-tonight.md:B00 row + every batch's Sort step (print/B00:B00.6, B02:B02.9 … B10:B10.6)
Quote: "Step B00.6 → Step B00.7 · ~15 min · leave-state: Gate B is measured …"
Problem: B00.6 (day-1 sorting) and B00.7 (kit-day Gate B) are one segment because only B00.7 has a Pause. Every other batch's Sort step has no Pause either, so binning (29 accent parts, 31 clips) never appears in the planner at all; the Sessions lines count it ("+ ~20 min inspect and bin") but Tonight does not.
Fix: Pause after each Sort step (B00.6 ~10 min "plate sorted, GATE B bag closed — B00.7 waits for the kit"; B02.9 ~15 min; others ~5–10 min), or fold "sorted into bins" into each Inspect Pause and rename those segments.

### F7 · MINOR · slicer/bins.py:`00-jigs` steps / print/README.md § Bins / docs/print/bin-labels.md (vs print/B00:B00.6 and Ch 14 Prerequisites)
Quote: bins.py: "cube at 14.10" / B00.6: "reference coupon for later re-checks (after the Gen 2 upgrade, and Ch 14 Step 14.11)" / Ch 14 Prerequisites: "You need it in hand at step 14.11".
Problem: 14.10 is "Fetch the cube you already printed in Ch 13"; the Prusa cube is used at 14.11. Label, README and bin map inherit the wrong step.
Fix: bins.py `00-jigs` steps "cube at 14.11"; regenerate labels; update the README row.

### F8 · MINOR · print/README.md:batch table "feeds" column (B02, B05, B07) + 00-index.md rows 22/Chapters Ch 07
Quote: "B05 | … | Ch 06 Z axis; Ch 07 A/B belts" / Ch 07 Prerequisites: "B05 (gates *A/B Belts* in the print plan)".
Problem: B05's parts bin to 06-Z-joints and 10-chains — Ch 06 and Ch 10; Ch 07's own parts table has no B05 part. Likewise B02 feeds omit Ch 07 (`[a]_cable_cover` → 07-X) and Ch 10 (`[a]_z_chain_retainer_bracket` → 10-chains); B07 omits Ch 11 (`handlebar_spacer` → 11-panels). The bins table three sections down is right; the batch table disagrees with it.
Fix: Derive the "feeds" cell from `bins.py` (chapters of the bins each batch fills) or hand-fix: B05 "Ch 06 Z joints; Ch 10 (chain anchor, guide)"; B02 add "Ch 07, Ch 10"; B07 add "Ch 11 (handlebar spacers)". Drop B05 from Ch 07's needs (index row 22, Chapters table, Ch 07 Prerequisites — assembly side).

### F9 · MINOR · 00-index.md:row 27 "needs" + Chapters table row Ch 10
Quote: row 27: "needs: Ch 10 Checkpoint #1; B02, B07, B08, B09, B10 by Step 11.46" / Chapters table Ch 10: "Ch 03, Ch 06, Ch 07, Ch 08, Ch 09; B05, B07".
Problem: Ch 11's own Prerequisites make Ch 12 Part 2 a hard gate ("the bay powered once, both MCUs flashed … before this part closes it"); row 27 omits it (order implies it, the "needs" contract says list it). Row 25 and Ch 10 itself also need B08 `mount.stl` + B02 `[a]_faceplate` at 10.50; the Chapters table omits them.
Fix: row 27 needs "Ch 10 Checkpoint #1, Ch 12 Part 2; …"; Chapters table Ch 10 "… B05, B07, B08 (`mount.stl`), B02 (`[a]_faceplate`)".

### F10 · MINOR · 05-gantry.md:Prerequisites (line 15) and Next (line 973); 06-z-axis-and-gantry-squaring.md:Prerequisites (line 15) — assembly side, read-only; route
Quote: "B04 (XY joints + X carriage, plate B04-P1, 7.3 h, black) … B04 is itself gated on B00 + B02 + B03" / "B05 … 1 plate, 5.2 h" (twice).
Problem: Pre-slice hours (B04-P1 is 8.6 h, B05-P1 6.4 h) and a pre-split print gate (B04 is gated on Gate B only; B04's own header says "B03 is not a print prerequisite"). `check_docs.py` does not scan chapter prose.
Fix: 8.6 h / 6.4 h; "B04 needs Gate B (Step B00.7)". Consider a `check_docs.py` sweep for `B\d\d-P\d, [\d.]+ h` in `docs/manual/*.md`.

### F11 · MINOR · 00-before-you-start.md:Printed-parts table row `z_drive_retainer_a_x2.stl` (concurrent Bin column) + print/B10:table row `Handle.stl`
Quote: Ch 00: "`z_drive_retainer_a_x2.stl` | 02-Z0 · 02-Z2 | … | 1" / B10: "`Handle.stl` | *(printed in B02, orange)* | 1 | Orange | 33.7 |  |" (empty Bin).
Problem: Ch 00 receives only the B00 copy, which `PLATE_ASSIGN` sends to 02-Z0; the cell shows the manifest's both-copies value. B10's Handle row has no bin though B10.6 and the label put it in 11-door.
Fix: Ch 00 cell "02-Z0"; B10 cell "11-door (already there from B02)".

### F12 · MINOR · docs/manual/assets/plates/B08-P1.png (renderer `scripts/render_plate_bins.py`, rotated labels)
Quote: caption: "every part numbered and filled in the colour of its bin, bin id on the part".
Problem: Part 1 (`rear_center_skirt_350`, turned 90° in the project) gets its label background drawn as three diagonal white bars instead of one rounded box (cropped at 3×: the "1 / 11-skirts" text is readable but sits on stripes); part 2's rotated label on the same plate renders correctly. Cosmetic; the other three diagrams read cleanly (B01-P1 corner ids, B07-P2 brim rings on the six 100 mm mounts only, B02-P3 all 29 parts with outside callouts).
Fix: In the rotated-text path, draw the label box after rotation (or rotate the box with the text); regenerate with `build_plates.py --from-3mf`.

### F13 · MINOR · docs/manual/assets/diagrams/MANIFEST.md:entry 11
Quote: "All 30 timeline rows in execution order …", "59.5 h hands-on … are 00-index.md's own figures".
Problem: Stale with F1 (31 rows, 59.4 h; the pause is at row 5, not 17).
Fix: With F1.

### F14 · MINOR · print/B07:Printed-parts table rows `usb_adapter_mount`, `usb_adapter_mount_partial_cover`
Quote: "5.0 (verify; 0.30 h est.)" / "1 file, 2 bodies *(optional spare: the kit supplies the base printed, and the V2 partial cover below replaces the cover — 9 g, on the plate as shipped)*".
Problem: The grams come from the sliced project now — "(verify; 0.30 h est.)" is pre-slice residue; the spare row is still a paragraph in a Qty cell (F8/F18 half-applied).
Fix: "5.0" plain; Qty "1 *(spare — kit supplies one; → spare-alt)*".

### F15 · IMPROVE · slicer/check_docs.py (F8/F15, F8/F16, F8/F2 asked; not done)
Quote: check_docs output: "consistent across the chapters, the plan (§3/§4/§9), print/README.md and README.md; 25 bins consistent …".
Problem: The numbers it does not guard are the ones that drifted this round: the SVG facts and row order (F1), `00-index.md` hours (now right), the "~157 h" / "399 g" lines in 00-slicer-setup, and chapter-prose plate hours (F10).
Fix: Add `00-index.md` batch rows, the two 00-slicer-setup lines, `MANIFEST.md` entry 11 and the SVG's "h print" texts to the check.

### F16 · IMPROVE · 00-tonight.md "Kit not here yet" + 00-index.md row 9
Quote: pre-kit 30 min: only "Start plate B00-P1 · ~5 min"; 90 min: "~60 min hands-on planned".
Problem: Ch 00's own pre-kit steps (00.8–00.11 tools/flat reference/bins, 00.23–00.32 reading, log, Discord) are real bench work the index says to do "the week batch B00 prints", but row 9 is one **KIT** row so the pre-kit planner never offers them; the pre-kit buckets are B00 + Ch 00a and nothing else. (F8/F3's "00.7–00.12" ask; Ch 12 Part 1 is correctly KIT — the Pi ships in carton 2.)
Fix: Either a second index row for Ch 00 anchored at "Before the kit ships" without KIT (needs the pre-kit steps to be contiguous, which they are not), or a `pre-kit` marker on individual Pause segments that the planner honours.

---

## Applied-and-correct (F8 findings verified in the files)
F8/F1 (Gate A/B split: 00-slicer-setup tables, B00.5/B00.7, Checkpoint B00, README order column, index row 1/9, plan §1.4/§2, corrections #22, glossary "Gate A / Gate B") · F8/F2 numbers only (SVG hours 4.0/22.8/…/157.1 — order not, see F1) · F8/F3 a–d (print chapters in the generator, 30-min bucket honest, index-row order, "Ch 00a" title; Ch 00 pre-kit not, see F16) · F8/F4 (every brim line is the confirmation form; B07.2/B09.2/B09.6 name their brims; "never the global setting" in 00-slicer-setup; verified per-object brims in the 3MFs: B08-P1 3 mm ×2, B00-P1/B02-P1 none) · F8/F5 (item 3, B00.4, B00 Common mistakes, Ch 15 rows) · F8/F6 (B00.0; B00.1 "Load Filament → ASA"; preset names match `Slic3r_PE.config`: printer `Prusa CORE One HF0.4 nozzle`, print `0.20mm STRUCTURAL @COREONE 0.4`, filament `Prusament ASA @COREONE HF0.4 - Voron black` / `- Voron orange` on B02 — see F3 for the printer-box caveat) · F8/F7 (B06.6, Checkpoint B06, index row 19) · F8/F8 (README "feeds" / "print gate" columns) · F8/F9 (ledger rule; ledger arithmetic re-checked: #1 748→60, runout in B09-P2, #2 793→13, #3 722→574, margins 587/521 ✓; every B0x.1 spool remark matches the ledger) · F8/F10 (B01.8 two-hand sorting, corner map matches bins.py and Ch 02.02) · F8/F11 (B09 ⚠ reworded, test at B09.12 on kit day) · F8/F12 (row 2 "While it prints: Ch 00a"; row 27 "B10 by Step 11.46"; Ch 12 Part 1 correctly KIT) · F8/F13 (§ Print sheet: glue on either sheet, acetone warning; B00.3/B01.3/B04.3/B10.3 "sheet per …") · F8/F14 (B08.2, 00-slicer-setup example, corrections #18 agree with the diagram: rear skirt along Y) · F8/F15, F8/F16 numbers (157 h, 399 g; index 21.9/29.2/21.8; not the check — F15) · F8/F17 (#17 superseded, #10 past tense) · F8/F18 (6 files/8 objects, 5/7 — all 27 plate counts re-added: 218 objects ✓; usb row see F14) · F8/F19 (B00.6 bags, README feeds) · F8/F20 (59.4 both; 141 sessions re-summed ✓) · F8/F21 (Skirt (slicer), Arachne, Seam, Z-hop, Volumetric flow, Purge line, Runout; glossary links in 00-slicer-setup/B00/B07) · F8/F22 (one Revo row) · F8/F23 (B10 swing default) · F8/F24 (Ch 15 "Printing the parts" + two trap rows; anchors resolve) · F8/F25 (B00.3 ⚠) · F8/F26 (reference-only sections moved) · F8/F28 (index "Kit not here yet" line, critical path split). Not applied, IMPROVE only: F8/F27, F8/F29, F8/F30 (B02/B03/B05–B09 dropped the pre-print pair; B00/B01/B04/B10 keep it — fine).

Bins work: README § Bins table = `bins.py` (25 bins, 218 pieces re-summed); every Sort-into-bins table in B00–B10 matches `ASSIGN`/`PLATE_ASSIGN` and the diagrams; bin labels list the right parts per plate (spot-checked all 25; 11-skirts ×2 plates, 02-Z2 retainer from B01-P1, spare-alt 14); QR targets encode `…/manual/steps/<chapter-slug>/` per `_chapter_overview_url`, and `…/manual/print/#bins` for spare-alt (segno, not decoded here — no zbar on this machine); all bins.py step ids resolve to real step headings except the cube's (F7); the concurrent Bin columns in Ch 00/02/04–11 agree with bins.py except the two cells in F11.

Day-1 walk (no kit): Tonight → Kit not here → B00 (lands on B00.2, F4) → B00.0 wizard (Prusa FFF → CORE One & CORE One+ → 0.4 HF → Prusament ASA) → open B00-P1.3mf (printer box likely "(modified)", F3) → B00.2 estimate 3 h 58 m / 51.7 g (= estimates.csv 3h 57m 38s / 51.66 g) → B00.3/B00.4 → Gate A (cube only) → B02. Executable with 2.9.6 and the committed 3MFs once F3/F4 are worded. Kit day: B00.7 → B01.1/B01.2, Ch 00 kit-day order (00.1 → Gate B → B01-P1 on → 00.2 …) consistent across Ch 00, B00, B01, index row 9, Checkpoint 00. Index order 10 → 12 Part 2 → 11 Part A → 13 → 06b → 11 Part B → 14 = rows 25–31, and every chapter's Prerequisites block agrees with it (Ch 11 Part B: Ch 13 + 06b; Ch 14: Ch 13, 06b, 11 Part B, 12; Ch 13: 11 Part A, 12; 06b: 13.34) — the only gaps are the omitted "needs" entries in F9.

## Chapter verdicts
- **print/00-slicer-setup.md** — with fix (F3). Weakest: the printer-box row; "config_version 2.4.14" is the .app copy, not the live bundle.
- **print/README.md** — with fixes (F8, F7). Weakest: "feeds" cells vs the bins table on the same page.
- **print/B00** — with fixes (F3, F4, F6). Weakest: B00.0 Check, no Pause before B00.2, B00.6/B00.7 as one segment.
- **print/B01** — yes as written. Weakest: none material.
- **print/B02** — yes as written (F6 applies to B02.9).
- **print/B03, B04, B05** — yes as written.
- **print/B06** — yes as written.
- **print/B07** — yes; F14 cosmetic.
- **print/B08** — yes as written; diagram F12 cosmetic.
- **print/B09** — yes as written.
- **print/B10** — yes; F11 empty Bin cell.
- **00-index.md** — with fix (F1, F9). Weakest: the SVG contradicts the list under it.
- **00-tonight.md** — with fix (F4; F6/F16 minor). Yes once the kit is here.
- **docs/print/checklists.md** — no, as generated (F2): no print-batch or Ch 00a/06b/08 checklists.
- **docs/print/bin-labels.md** — yes (F7 step id).
- **15-troubleshooting.md** — yes as written; every "Owned by" link resolves.
- **16-glossary.md** — yes as written; all anchors resolve.
- **docs/index.md** — yes; its "print-ready Checkpoint checklists" claim is true only after F2.
- **slicer/bins.py + plate diagrams** — yes (F7, F12).
