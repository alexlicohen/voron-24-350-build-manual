# VERIFY-D — Ch 00, README, glossary, slicer setup, B00, two scripts (2026-10-23)

Gates: `.venv/bin/python scripts/lint_manual.py --strict-parts --chapters 00,16` exit 0 (check 6: 0, check 7: 0);
`--budgets-only` reports nothing in my files; `.venv/bin/python slicer/check_docs.py` exit 0 (22 plates, 157.0 h, B11 consistent).
Script checks: `python3 slicer/sync_start_gcode.py --check` (27 plates, "would change 0 of 27"); `build_plate_review_markdown()` rendered in memory (27 rows: 22 "smooth PEI sheet + glue", 5 "textured sheet"). No 3MF, ini or generated file written.

## G1-02 — CONFIRMED
- Source: same file :92 (00.14–00.16 = Gate B insert row, KADRICK, nothing from the kit), :96 (two kit-day rows: 625-2RS + MGN12), :414 (nothing to buy for Gate B); B00.7 (B00:342–356): pocket calipered 16.30 ±0.15 now, bearing + rail rows on kit day. Line 18 also said 00.13–00.16; 00.13 is kit day (:92, :565).
- Change: 00-before-you-start.md:18 now names Gate B's caliper and insert rows (passed, nothing bought), Steps 00.14–00.16, and **two** kit-day rows (625-2RS thumbed into `z_drive_retainer_a`, `MGN12_rail_guide` on a real rail).

## G1-06 — PARTLY (9 of 11 reviewer items confirmed, plus 1 not on the list)
Grep of every chapter's Tools/Parts against 00.8/00.9 and the LDO BOM (`scripts/data/ldo-350-bom.yml`: hex wrenches, 2.5 mm slot driver, drill bit, brass brush, insert tip, 32 GB SD card; no Phillips, saw, pliers, solder or glue):
- Confirmed, added as 00.8 rows (00-before-you-start.md:382–390): mallet (Ch 01 Tools, 01 Do "Tap … with the mallet"); steel tape ≥ 2.2 m (Ch 01 ≥1 m diagonals; 07.8 Do "Measure 2000 mm"); craft knife + scraper/card (Ch 03 Tools, 03.9 Parts); hacksaw/fine saw + small flat file (09.5 ⚠ no DIN length published, shorten the rail; Ch 08 Tools file for 5015 ears); PH1 + PH2 (Ch 09 Tools, 09 Do "with a PH1", Ch 10 Parts "tool: PH2 screwdriver"); small hammer (11.47 Parts); SD card reader (12.2 Parts "tool: SD card reader"; the kit ships the card only); fire extinguisher (12.11 Parts, 13.1 Do, 00a.12 "keep the extinguisher … permanently by the machine").
- Not on the reviewer list but confirmed: needle-nose pliers + tweezers (Ch 06 Tools p.118, Ch 07 Tools p.132, Ch 08/10). Added.
- Confirmed, added to 00.9 (:423–424): solder (11.33 Parts), super glue (11.34, 11.36, 11.48 Parts; Ch 11 Consumables).
- REFUTED: label maker (Ch 10 Tools: "Label maker, or the cable tags supplied in the kit" = optional). The reviewer's "00a.12 Buy an ABC extinguisher" quote does not exist; no page names a class. Row says "ABC dry chemical (rated for electrical fires)" as a buying spec, not a source claim.
- First lint pass flagged 00.8 at 2 prose Step refs (my "Step 00a.12"); reworded to "Ch 00a", budgets clean.

## G1-07 — CONFIRMED
- Source: slicer/build_plates.py docstring :14–27 and main() :464–468: bare = pack every plate from plates.py and rewrite the 3MFs ("loses any hand arrangement"); `--from-3mf` re-slices the committed 3MF, refreshes estimates.csv and diagrams; build_from_3mf() needs no STLs (reads the 3MF).
- Change: README.md:19 → `python3 slicer/build_plates.py --from-3mf`, never bare; packing only for a plate with no project, after `fetch_stls.py`.

## G7-M1 — CONFIRMED
- Source: 00-slicer-setup.md:246 Gate A row links `../16-glossary.md#e` and says reduce EM in 1 % steps; B00.7 gate-calc low/high rows move EM ±1 %; Ch 15 :37/:50/:506/:512 the same. Glossary :109 forbade it globally.
- Change: 16-glossary.md:109 scoped to the Voron (Ch 14, Ellis); names the Core One+ Gate A cube / Gate B pocket (shrinkage 0 %, XY comp 0) as the one exception; keeps "never negative XY". Added a Gate A link in "First matters at".

## G8-01 — CONFIRMED
- Source: slicer/voron-coreone-asa.ini :94 `first_layer_acceleration = 500`, :97 `first_layer_extrusion_width = 0.5`, :99 `first_layer_infill_speed = 100`, :100 `first_layer_speed = 25` (same in voron-accent-blue.ini). CLI slice of `slicer/plates/B00-P1.3mf` (PrusaSlicer 2.9.6, `--dont-arrange --binary-gcode=0`, output in my scratchpad), layer-1 extrusion moves: Solid infill 1451 @ F6000 (100 mm/s); Perimeter 1328, External perimeter 574, Skirt/Brim 18 @ F1500 (25 mm/s). Peak = 100 × 0.5 × 0.2 = 10 mm³/s.
- Change (option b, no ini change): 00-slicer-setup.md:58–59 peak 10 mm³/s on first-layer solid infill (8.8 above layer 1); :157 First layer speed row says it covers perimeters, skirt and brim only, infill stays at `first_layer_infill_speed` 100 with acceleration 500; new line :162 naming `first_layer_infill_speed = 25` as the override, unset, a one-variable test first; :175 Max volumetric row → 10 mm³/s. Override table rows not added or moved (build_config.py cites them by row number).
- **Outside my files (proposal):** docs/voron-print-plan.md:166 "(peak ≈8.8 mm³/s)" → "(peak ≈10 mm³/s, first-layer solid infill)"; :150 First layer speed row → append "; perimeters, skirt and brim only, first-layer infill stays at 100 mm/s".
- **For Alex:** whether first-layer infill goes to 25 too (changes every estimate; one-variable rule).

## G8-02 — CONFIRMED
- Source: sync_start_gcode.py `INI` had only black/blue; `value = ini_value(INI[colour], key)`. `python3 slicer/sync_start_gcode.py --check` before the fix: 22 × "already current", then `KeyError: 'petg'` at B11-P1. build_config.py:28/101/210: every ini's `start_gcode` = `coreone-cold-start.gcode`, so the documented command changes nothing.
- Change, script: `"petg": ROOT / "bay-ducts-petg.ini"` (B11 plates have `colour="petg"`, plates.py:384–432; same key build_plates.py:60 uses); a clean SystemExit for an unknown colour instead of a traceback; docstring says it runs over all 27 plates, never changes an ini, and that a start switch means changing `COLD_START` in build_config.py + `python3 slicer/build_config.py` first. After: `--check` → 27 × "already current", "would change 0 of 27". `--check --value test B11-P1 B00-P1` reports "differs" and leaves the 3MF md5 unchanged. Not run in write mode.
- Change, docs: 00-slicer-setup.md:72 (build_config writes the start into the inis; sync copies it into all 27 projects); :422–430 the full working procedure (point `COLD_START` at the winning block, a stock start vendored to its own file first, `build_config.py`, `sync_start_gcode.py`, `build_plates.py --from-3mf`, `check_docs.py`), plus: do not rebuild the check projects after the switch (hot_check.py:124 would fail the cold project, which then carries `G29 P9`). B00-calibration-and-jigs.md:127 "every plate, the 22 and B11's five"; :129–141 the same short procedure with a link to 00-slicer-setup § Gen 2.
- **Outside my files (proposal):** slicer/hot_check.py docstring :34–35 "after `sync_start_gcode.py` changes the start G-code in the inis: that script patches the 22 plates only" is false both ways → "after `build_config.py` changes the start G-code in the inis (sync_start_gcode.py then patches every plate)". build_config.py:450 "22 committed plates" → "27". hot_check.py has no stock-start project (known gap, B00:129).

## G8-05 — CONFIRMED
- Source: AGENTS.md "ASA smooth PEI + glue"; 00-slicer-setup.md:195 "ASA … **smooth PEI**, with the glue film below … on satin ASA grips less". Generator: scripts/build_printables.py:943 `"smooth/satin"`.
- Change: build_printables.py:943–949 → `"smooth PEI sheet + glue"` / `"textured sheet"` (the f-string no longer appends " sheet"). docs/print/checklists.md is regenerated by the orchestrator's `make verify`; I did not write it.
