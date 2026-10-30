# G8 — Print batches, slicer profiles, bins, sources

**Group:** G8 (print). **Reviewer:** claude (deep tier), 2026-10-23, read-only; tree reviewed as is (16 uncommitted files included).

**Files covered:** docs/manual/print/ (README, 00-slicer-setup, B00–B11); docs/print/ (bin-labels, checklists, plate-board, plate-plans); slicer/plates.py, bins.py, voron-coreone-asa.ini, voron-accent-blue.ini, bay-ducts-petg.ini, estimates.csv, the 27 plates/*.3mf (metadata read only); sync_start_gcode.py and build_config.py where the pages send the builder; sources.yml; scripts/data/ (ldo-350-bom.yml, hardware-ownership.yml).

**Primary sources used:** the committed 3MFs (`Metadata/Slic3r_PE.config`, `Slic3r_PE_model.config`, `3D/3dmodel.model` object extents), a PrusaSlicer 2.9.6 CLI slice of `B00-P1.3mf` into scratch (first-layer G-code feedrates per `;TYPE:`), the 2.9.6 app bundle's `PrusaResearch.ini` resolved through `slicer/resolve_preset.py`, the STLs under `slicer/stl/` (numpy section probe, `venv-cq/bin/python -I`), `scripts/data/ldo-350-bom.yml`, the chapter Printed-parts tables in docs/manual/0*–1*.md parsed against `plates.PLATES`, and PROJECT_MEMORY.md / AGENTS.md for recorded decisions.

Counts: 0 blocker · 6 major · 12 minor · 3 nit.

---

### G8-01 major — The first layer is not slowed to 25 mm/s: first-layer solid infill prints at 100 mm/s, and the volumetric peak is 10 mm³/s, not 8.8

- docs/manual/print/00-slicer-setup.md:156 — "| First layer speed | 45 | **25** | ASA on smooth PEI is the single biggest failure mode; slow the first layer"
- docs/manual/print/00-slicer-setup.md:58 — "the peak volumetric flow is 110 mm/s solid infill × 0.4 × 0.2 = **8.8 mm³/s**"; :172 "the plates peak at 8.8 mm³/s"
- slicer/voron-coreone-asa.ini:99 `first_layer_infill_speed = 100` (STRUCTURAL default, never overridden; slicer/OVERRIDES.md:49 overrides only `first_layer_speed`). It is the same in every one of the 27 3MFs (`; first_layer_infill_speed = 100`).

Evidence: I sliced `slicer/plates/B00-P1.3mf` with the 2.9.6 CLI into scratch and counted extrusion moves on layer 1: `Solid infill` 1451 moves at F6000 (100 mm/s); `Perimeter` 1328 and `External perimeter` 574 at 25 mm/s. On the first layer, 2.9.6 applies `first_layer_infill_speed` to infill and `first_layer_speed` to everything else. So most of every part's first-layer area goes down at 4× the speed the table promises. The peak flow is 100 × 0.5 (first-layer width) × 0.2 = 10 mm³/s. That is still under 26, so the volumetric conclusion stands, but its number is wrong.

Fix (Alex's call, since it changes every plate's estimate):
(a) add an override row and key: `| First layer infill speed | 100 | **25** | same reason as the row above: PrusaSlicer applies it, not First layer speed, to first-layer infill | judgment |`. Then `build_config.py` → `sync_start_gcode.py --key first_layer_infill_speed` → `build_plates.py --from-3mf` → `check_docs.py`. This is one variable, so it belongs in the first-layer test order.
(b) or keep 100 and reword :156 to say "perimeters and skirt only; first-layer infill stays at the profile's 100 mm/s (first_layer_acceleration 500)", and :58 to "first-layer solid infill 100 mm/s × 0.5 × 0.2 = **10 mm³/s**".

### G8-02 major — The documented start-G-code switch does not work: `sync_start_gcode.py` only re-copies the ini (still the cold start), it skips B11, and it crashes with a traceback

- docs/manual/print/B00-calibration-and-jigs.md:130–131 — "the 22 plates switch to the stock start (`python3 slicer/sync_start_gcode.py`)"
- docs/manual/print/00-slicer-setup.md:418–420 — "the better one goes into all 22 plates with `slicer/sync_start_gcode.py`"; :71 "keeps the inis and the 22 projects in step"
- slicer/sync_start_gcode.py:43–44 `INI = {"black": …, "blue": …}`; :119 `ini_value(INI[PLATES[pid]["colour"]], key)`

Evidence: (1) The script writes the value from the ini. The ini's `start_gcode` comes from `coreone-cold-start.gcode` (build_config.py:28/101). Run as documented, it reports "already current" for all 22 plates and changes nothing. To get the stock or heat-then-off start, `build_config.py`'s source must change first. Neither page says so. (2) `python3 slicer/sync_start_gcode.py --check` prints 22 "already current" lines and then `KeyError: 'petg'` at B11-P1, because the bare run iterates every plate in PLATES. A real run would patch the 22 plates, then die. It would leave the 5 B11 projects (same cold start: `bay-ducts-petg.ini` start_gcode is byte-identical to the ASA ini's) and the bay ini on the old start, with no summary line.

Fix: add `"petg": ROOT / "bay-ducts-petg.ini"` to `INI`. In B00:130–131 and 00-slicer-setup:418–420, state the real procedure: "edit the start-G-code source in `slicer/build_config.py` (or vendor the winning block over `slicer/coreone-cold-start.gcode`), run `python3 slicer/build_config.py`, then `python3 slicer/sync_start_gcode.py` (all 27 plates), `python3 slicer/hot_check.py`, `python3 slicer/build_plates.py --from-3mf`, `python3 slicer/check_docs.py`". Change :71's "the 22 projects" to "the 27 projects (B11's included)".

### G8-03 major — Kit ETA is stale: the pages say late November; the recorded ETA is early November (Alex, 10-22), so "all 157 h before the cartons land" no longer holds as written

- docs/manual/print/README.md:20–22 — "The Voron kit is not expected before **late November 2026**, so the whole run goes down first … all 157.0 h, finished before the cartons land."
- docs/manual/print/00-slicer-setup.md:377–378 — "realistic delivery is **late November to late December 2026**" (dated 2026-09-23 there, but nothing marks it as superseded)
- docs/manual/print/B10-clicky-clack-door.md:146 — "All 22 are done and binned, weeks before the cartons land."; B02:256 "the whole run is finished before the kit lands"
- PROJECT_MEMORY.md § Manual › Kit: "ETA early November (Alex 10-22; was Nov 20–Dec 24); all 22 plates (157.0 h) print before kit day."

Evidence: as of 10-21 the pre-B00 checks were still pending. The README's own schedule is "three to four weeks at two swaps a day" (README:83–84). That puts the last plate in mid-to-late November, after an early-November kit.
Outside G8, the same stale ETA appears in docs/index.md:7, docs/manual/00-index.md:7 and :155, 00-before-you-start.md:19, voron-print-plan.md:243 and :859, voron-build-instructions-survey.md:64, and context/build-facts.md:17.

Fix (README:20–22): "The Voron kit is expected in **early November 2026** (Fabreeko, as of 2026-10-22), so the run goes down in numeric batch order from B00 and may still be printing when the cartons land: Ch 01 needs no printed part, and B00–B05 (≈ 72 h) cover Ch 02–06 first." Also mark 00-slicer-setup:377–378 "(superseded 2026-10-22: early November)", and soften B10:146 and B02:256 to "before or soon after the cartons land".

### G8-04 major — The "did the project load?" test contradicts itself: B00 says all three preset boxes read "(modified)", but 00-slicer-setup says the filament box shows the renamed preset, and the GUI-saved 3MFs show a third form

- docs/manual/print/B00-calibration-and-jigs.md:67 — "**Check:** All three preset boxes read `(modified)`: … `Prusament ASA @COREONE HF0.4 - Voron black`."; :71 — "The project did **not** load if any box lacks `(modified)`"; :409 (Checkpoint B00) — "showed `(modified)` on all three boxes"
- docs/manual/print/00-slicer-setup.md:108–113 — Filament box shows "`Prusament ASA @COREONE HF0.4 - Voron black`" (no "(modified)"); the failure signals are the print box without "(modified)" or a bare `Prusament ASA @COREONE HF0.4`
- docs/manual/print/B02-accent-parts-orange.md:94 — "Confirm: filament box `Prusament ASA @COREONE HF0.4 - Voron blue`"

Evidence: the five plates Alex re-saved from the GUI (B03-P1, B06-P1, B07-P1, B08-P2, B08-P3) carry `filament_settings_id = "B03-P1.3mf (Prusament ASA @COREONE HF0.4 - Voron black)"` (and the same pattern for the others). That is PrusaSlicer's external-preset naming, `<project file> (<preset name>)`, used when a project's preset name is not installed. So on open the filament box most likely reads `B00-P1.3mf (Prusament ASA @COREONE HF0.4 - Voron black)`, without "(modified)". Read literally, B00:71 then says the load failed. I did not check the GUI display itself.

Fix: B00:67 → "**Check:** Printer box `Prusa CORE One HF0.4 nozzle (modified)`, print box `0.20mm STRUCTURAL @COREONE 0.4 (modified)`, and a filament box whose name contains `Prusament ASA @COREONE HF0.4 - Voron black` (PrusaSlicer may prefix it with the project file name)." B00:71 → "…did **not** load if the printer or print box lacks `(modified)`, the filament box reads bare `Prusament ASA @COREONE HF0.4`, …". Change Checkpoint B00:409 to match. In 00-slicer-setup:108 and B02:94, say "contains … - Voron black / - Voron blue". Confirm the exact string in the GUI once (B00.8).

### G8-05 major — The plate-review checklist offers "smooth/satin" for every ASA plate, against the sheet-per-material rule (ASA = smooth PEI only)

- docs/print/checklists.md:475–526 — "- [ ] B00-P1 — ASA, smooth/satin sheet, black · 4.0 h · 52 g" (all 22 ASA rows)
- docs/manual/print/00-slicer-setup.md:192 — "ASA (every Voron plate, the add-on prints) | **smooth PEI**, with the glue film below | … on satin ASA grips less and often needs a brim"; AGENTS.md "Print sheet follows the material: ASA smooth PEI + glue, PLA satin, PETG textured."
- generator: scripts/build_printables.py:943 `sheet = "smooth/satin" if asa else "textured"`

This is the sheet column B00.8 tells the builder to read. Fix: build_printables.py:943 → `sheet = "smooth PEI + glue" if asa else "textured"`, then regenerate.

### G8-06 major — B02-P3 ships the Igus-backer bridge standing 44 mm, so every opening of the committed project tells the builder to re-orient a part on a packed 29-part plate

- docs/manual/print/B02-accent-parts-orange.md:153 — "In preview, if `XY_cable_chain_bridge-Igus-3mm_backer` stands 44 mm tall, lay it flat to match the stock bridge."; :155 "**Check:** Cable-chain bridge sitting flat, not standing, before slicing."
- docs/manual/print/00-slicer-setup.md:309–311 (same exception); B02 page header "Do not rebuild the plate", and 00-slicer-setup:62–66 ("open the plate, don't rebuild it")
- slicer/plates/B02-P3.3mf: from the object extents, the backer is 21.0 × 66.1 × **44.0** mm (standing); the stock `[a]_xy_joint_cable_bridge_2hole` is 41.0 × 66.1 × 21.0 (flat)

Evidence: the condition at :153 is always true. Laying the part flat grows its footprint from 21 to 44 mm, on a plate nest.py packed at 6 mm gaps. That invalidates the plate diagram, the 7.6 h / 96 g check and the sorting legend unless the plate is re-saved and rebuilt, and the step says none of this. 00-slicer-setup:317–325's "Tallest parts, in order" also leaves out this 44.0 mm part (and `cw2_captive_pcb_cover`, 42.2 mm).

Fix: lay it flat once in the GUI, Arrange Current Bed, save over `B02-P3.3mf`, then `build_plates.py --from-3mf B02-P3`, `check_docs.py`, and shift the ledger if the grams move. Then replace B02:153/:155 with "the Igus backer lies flat like the stock bridge (fixed in the project)". Or, if standing is the intended print orientation, delete :153/:155/:249 and 00-slicer-setup exception 1, and add the part to the tallest-parts table.

---

### G8-07 minor — Whether Live Adjust Z is saved is "(verify on bench)" in one place and asserted "not saved" in two others

- B00-calibration-and-jigs.md:294 (Gate A calc, z high) — "because the Core One+ does not save the nudge"; :296 "does not remember a Live Adjust Z nudge"; :429 — "Live Adjust Z is a per-print nudge that is not saved"
- B00:126 — "Kept = Live Adjust Z is stored per sheet; reset to 0 = it is not. This settles § Calibration sequence item 3"; 00-slicer-setup.md:197–198 "Live Adjust Z is kept per sheet `(verify on bench)`", :235
- If the nudge is in fact kept per sheet, a builder who re-nudges every plate (following :294) doubles the offset.

Fix: :294/:296 → "…then fix the cause rather than nudging every plate; whether the nudge carries to the next print is what B00 § Before B00 item 3 settles." :429 → "…Live Adjust Z is a nudge, not a calibration (whether it is kept per sheet: item 3)."

### G8-08 minor — B01-P1 is 4 files, not 5

- B01-z-drive-assemblies.md:80 — "**5 files, 7 objects**"
- slicer/plates.py B01-P1: `z_drive_main_a`, `z_drive_main_b`, `z_drive_retainer_a`, `z_drive_retainer_b` = 4 files; 2+2+1+2 = 7 objects. The 3MF holds the same 7 objects. Every other Load step's count matches plates.py.

Fix: "**4 files, 7 objects**".

### G8-09 minor — B03 says three B02 accent parts are "already in 04-A / 04-B"; two of them are in other bins

- B03-ab-drive-units-and-front-idlers.md:13–15 — "its accent `[a]_cable_cover`, `[a]_z_chain_retainer_bracket` and `[a]_tensioner_left/right` … are already in 04-A / 04-B."
- slicer/bins.py and README § Bins: `[a]_cable_cover` → **07-X**; `[a]_z_chain_retainer_bracket` ×2 → **10-chains**; only the tensioners are in 04-A/04-B.

Fix: "B02 is not a print prerequisite: its `[a]_tensioner_left/right` printed one batch earlier and are already in 04-B / 04-A."

### G8-10 minor — B02 sorts into 17 bins, not "eleven"

- B02-accent-parts-orange.md:234 — "all three plates sorted into their eleven bins"
- B02.9's own tables: 02-Z0, 02-Z1, 02-Z2, 02-Z3, 07-X, 08-SB, 10-tft, 04-A, 04-B, 11-fans, 11-door, 05-XY, 06-Z-joints, 08-CW2, 10-chains, 11-skirts, spare-alt = 17 distinct bins. plate-plans.md:53/61/69 lists the same.

Fix: "into their seventeen bins".

### G8-11 minor — "Every accent part / two colour changes / no more blue prints" no longer holds: the add-ons print blue

- B02-accent-parts-orange.md:3 "Every accent part in the whole build, printed in one continuous session so the accent spool is mounted exactly once"; :5 "Two colour changes in the whole build"; :245 "Blue spool re-sealed/dry-stored — no more blue prints in the build"; README.md:199 "two colour changes in the entire build"
- README.md:306–307, 321–322, 329–330: the exhaust fan grill, access cover and 2 mounts, and the Prusa puck and spindle, print blue with `voron-accent-blue.ini` as separate jobs (Steps 14.26 and 11.69)
- 00-slicer-setup.md:369 "Three non-Voron parts carry no `[a]_` prefix but are printed **Blue**" (the puck and spindle are two more); slicer/voron-accent-blue.ini:76 (from build_config.py) `filament_notes = … accent colour, B02 plates only`

Fix: B02:3 → "Every accent part of the 22-plate run…"; B02:5 and README:199 → "Two colour changes in the run (the optional add-ons add their own blue jobs after kit day)"; B02:245 → "…no more blue in the run; keep it dry for the add-ons' blue jobs (Steps 11.69, 14.26)". In 00-slicer-setup:369, add "(plus the side-spool add-on's Prusa puck and spindle)". In build_config.py, set the blue `filament_notes` to "B02 plates and the add-ons' blue jobs".

### G8-12 minor — "Not yet bought" is stale for the PETG V0 spool (bought 10-13)

- README.md:270 — "348 g needed from one 1 kg spool, **V1**, not yet bought"; :287 — "one 1 kg Prusament PETG V0 Jet Black spool, not yet bought"; B11-bay-ducting.md:12 — "Needs one 1 kg spool of **Prusament PETG V0 Jet Black** (not yet bought)"
- The spool is on hand (purchase details: see context/orders.md, not tracked).

Fix: drop "not yet bought" in all three places ("on the shelf since 2026-10-13"). Known, A5 bags: the README:111 "one more pack of A5 bags … still to buy" is the already-known 00.11 item (it may already be closed: see context/orders.md, not tracked).

### G8-13 minor — The README "feeds" column misses three consuming chapters, and B05's Next names a chapter B05 does not feed

- README.md:37 B05 "Ch 06 Z joints; Ch 10 (chain anchor, guide)". It is missing **Ch 02**: `z_rail_stop` ×4 goes to bins 02-Z0…Z3, fitted at Step 02.10 (02-z-drives.md:58).
- README.md:39 B07 "Ch 09 …; Ch 10 …; Ch 11 (handlebar spacers)". It is missing **Ch 08**: `usb_adapter_mount_partial_cover` → 08-CW2, fitted at 08.64 (09-electronics-bay.md:50).
- README.md:40 B08 "Ch 11 Part A Skirts". It is missing **Ch 10**: `mount.stl` → 10-tft, built at 10.50.
- B05-z-joints-and-z-chain.md:122 — "Assembly: *Z Axis* (p.108–123) and *A/B Belts* (p.124–145)". No B05 part is used in Ch 07; B05 feeds Ch 02 (rail stops), Ch 06 and Ch 10.

Fix: add the missing chapters to the three rows. Change B05:122 to "Assembly: *Z Axis* (Ch 06) for the joints, Ch 02 Step 02.10 for the rail stops, Ch 10 for the chain anchor and guide."

### G8-14 minor — B07 carries a stale throughput-model gram figure and a DIN-clip count that disagrees with Ch 09

- B07-electronics-bay-and-lighting.md:47 — "(127 g on P2 alone)". slicer/estimates.csv B07-P2 = 123.94 g (README:72 and the ledger say 124 g); 127 is plates.py `MODEL_ESTIMATE["B07-P2"]`. check_docs does not see numbers in prose.
- B07:26 — "3 *(spares — the kit supplies the 4 needed)*". 09-electronics-bay.md:83 (hardware table): "DIN Clip | 3 | 2 Leviathan brackets, 1 USB adapter; LDO ships 4, the 4th is a spare" (ldo-350-bom.yml DIN Clip qty 4).

Fix: "(124 g on P2 alone)"; "3 *(spares — the kit supplies 4, of which 3 are used)*".

### G8-15 minor — The bench observation that a 0.1 mm brim gap fuses contradicts "so it snaps off"

- 00-slicer-setup.md:342 — "Brim separation stays at PrusaSlicer's 0.1 mm so it snaps off." (every 3MF: `brim_separation = 0.1`)
- PROJECT_MEMORY.md § Printer › First layer: "Brim gap: Alex uses 0.3 (0.1 fuses); repo stays 0.1 until the first-layer fix proves 0.1 snaps off".

Fix: "Brim separation stays at the profile's 0.1 mm for now `(verify on bench)`: on this printer a 0.1 mm gap has fused; if the first B02-P2 Handle brim will not snap off, the re-slice to 0.3 is Alex's call."

### G8-16 minor — The B11.11 regenerate recipe re-nests B11-P4 after its B00.8 GUI QC and never re-arranges it

- B11-bay-ducting.md:330 — "`python3 slicer/build_plates.py --nest B11-P4`"; :75/:109 require Arrange Current Bed + `--from-3mf` before each first print; B11.12 (:157–165) has no QC line.

Fix: after :330, add "`then open B11-P4.3mf, Arrange Current Bed (6 mm, rotations on), save, python3 slicer/build_plates.py --from-3mf B11-P4 && python3 slicer/check_docs.py`".

### G8-17 minor — Hardware trays: the README names Prusament PLA, but the queue prints them in Elegoo PLA

- README.md:350 — "`0.20mm BALANCED @COREONE HF0.4` with Prusament PLA"; PROJECT_MEMORY § To print › Queue: "hardware trays (plain PLA, Elegoo white/black, satin sheet; 652 g)".

Fix: "with the Prusament PLA preset (printed in Elegoo PLA white/black)".

### G8-18 minor — 00-slicer-setup's STL-source rule ignores the Printables-sourced B11 and add-on files

- 00-slicer-setup.md:447 — "Do not use a re-hosted zip or a Printables mirror." The table at :450–461 lists only the 9 git repos. But B11's `mss/502306/*` (withdrawn, committed) and the add-ons (Printables 1605113, 608769, 488020, 796563) are pinned by Printables file id in plates.py `PRINTABLES` and sources.yml.

Fix: add row "10 | B11 + add-ons | Printables, pinned by file id (`slicer/plates.py` PRINTABLES, sources.yml `printables:`) | `slicer/stl/bayducts/`, `slicer/stl/printables/`, `slicer/addons/`", and change :447 to "…or a Printables *mirror* of a git-hosted part".

---

### G8-19 nit — The ini headers call the bundle's config version the "installed PrusaSlicer" version

- slicer/voron-coreone-asa.ini:4–5 (and the blue and PETG inis, from build_config.py) — "read from the PrusaResearch.ini shipped with the installed PrusaSlicer (2.4.14)". 2.4.14 is the bundle's `config_version` (00-slicer-setup.md:26); the app is 2.9.6. Fix: "…shipped with the installed PrusaSlicer 2.9.6 (bundle config_version 2.4.14)".

### G8-20 nit — The B00 Sessions header and its pauses disagree on setup time

- B00:16 "~15 min one-time slicer and filament setup"; the pauses at B00.0 and B00.1 are "~10 min" + "~10 min" = 20. Fix: "~20 min".

### G8-21 nit — The B11 coupon is 27 min, not 25

- B11:113 "the coupon is printing, 25 min"; estimates.csv B11-P1 = 26 m 44 s (0.4 h). Fix: "~27 min".

---

## Checked and consistent

- Profiles vs 00-slicer-setup override tables: every print and filament row in the ASA ini (perimeters 4, 5/5 solid, 40 % grid, 0.40 widths / 0.50 first, 35/55/100/110/80 mm/s, rear seam, 1-loop skirt 3 mm / 4 mm, Arachne, supports off, XY 0, EFC 0.2, shrinkage 0 %, 265/110 °C, chamber 55/40, fan 20–25 % with the first 4 layers off, 26 mm³/s, retract 0.7 @ 45, z-hop 0.2) matches. The same values sit in all 22 ASA 3MF configs. The STRUCTURAL/SPEED/BALANCED comparison figures match the resolved 2.9.6 bundle.
- Accent ini = ASA ini except colour, notes and preset id. All three B02 3MFs carry `- Voron blue` / `#1F4E9C`; the other 19 ASA plates are black.
- B11 / PETG: bay ini and all 5 B11 3MFs are PETG V0, 230/85–90 °C, 3 perimeters, 4/4, 20 % grid, EM 1.04, `M106 P3 S160` / `M106 P3 R`, chamber 35, cold start identical to ASA, textured sheet. This matches B11:72–74, B11.2 and 00-slicer-setup:194.
- Cold-probe start: all 22 ASA 3MFs match the ini (`sync_start_gcode.py --check`: 22 "already current"; then the G8-02 crash).
- Brims: every object's `brim_width` in all 27 3MFs equals plates.py `brim_for()`. Every Load and Print step's brim statement (B00–B11) and 00-slicer-setup's 5 mm and 3 mm lists match.
- File and object counts in every Load step except B01-P1 (G8-08) match plates.py and the 3MF object lists. The B00-P1 (3 h 58 m / 51.7 g) and B01-P1 (15 h 13 m) GUI times match estimates.csv rounding.
- Plates vs chapters: every STL row in the assembly chapters' Printed-parts tables (Ch 00, 02, 04–06, 08–11) is on a plate with the same quantity and colour, or is marked not-printed, fallback or kit-supplied. Every STL-like name used in a step is on a plate, an add-on, B11 or the fallback set, or is an explicitly skipped alternative (stock doors, mini12864, hall-effect, `mount_thick`, Klicky side docks, `chain_anchor_2hole`). The LDO-supplied printed list (10 items) matches ldo-350-bom.yml.
- Bins: B00–B11 *Sort into bins* tables against bins.py. B11.8 counts (9/6/5/7) and B11.14 counts (6/3/3/6) recomputed. Z-corner hand map. README piece counts 218 + 53 + 14 = 285.
- Spool ledgers: every ASA and B11 "remaining" figure recomputed. Black margin 587 g (32 %), blue 521 g (187 %). The add-on draw is 239 g black / 120 g blue (38 + 66 + 106.7 + 7.6 + 21; 35 + 84.7). The run schedule has 12 overnight and 10 day plates under the 7 h rule.
- Gates: Gate A releases B02, B07–B10; Gate B releases B01, B03–B06 (58.4 h / 763 g recomputed). The Gate A/B calculators' extrusion-multiplier directions agree with the 00-slicer-setup tables. `Heatset_Practice` has exactly 7 Ø4.7 pockets (4 top + 3 side, STL probe). There are 153 kit inserts (BOM).
- Colour scheme: no prose in G8 files still calls the accent orange. The B02 filename is legacy only. B11's "orange endcaps" option uses the recorded spare orange spool. Galaxy Black + blue matches context/build-facts (blue LDO frame, blue Clicky-Clack).
- Clicky-Clack: B10 hinge side and mirror rule, M5×45 pins ×4, 6 split bushings, and the 5 mm brims agree with Ch 11.44–11.50 and 11.62–11.64.
- Add-on pins: plates.py PRINTABLES file ids (1605113, 608769, 488020) match sources.yml `printables:` entries. ADDONS paths match bins.py ADDON_PARTS and README's 4 add-on rows. HappyCam's printer-left cable exit and 3 m cable agree across sources.yml, its README, bins.py and Ch 10.
- Not verified: the F695 and 625-2RS seat diameters (15.00 / 16.30 mm) quoted in B03, B01 and Gate B. My STL section probe closes small bores but not those large stepped pockets, so it gave no reading. The GUI's literal filament-box string (G8-04) is inferred from the saved 3MFs, not seen.
