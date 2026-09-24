# Hardware ownership: where each kit unit is consumed

Wave 4 phase 3b (claude, 2026-09-24). Input for the content packets P1–P9 (WAVE4-PLAN § 6).
Machine-readable map: `scripts/data/hardware-ownership.yml`. Code: `scripts/parts.py` (check 7, `--ledger`), `scripts/lint_manual.py` (`--strict-parts`).
Evidence is the Voron manual page image (`docs/manual/assets/manual-pages/manual-pNNN.png`), the LDO 350 Rev D BOM (`scripts/data/ldo-350-bom.yml`), the LDO wiring guide, or the Clicky-Clack sources named per row. Never a reviewer's summary.

## The rule

1. A kit unit is consumed once: at the step that first mounts, fastens, presses, glues, solders or plugs it into the machine or a sub-assembly. That step lists it as a counted part.
2. Earlier steps (unpack, inspect, set a switch, strip jumpers, trim, tape, bag) list it `staged:`. Later steps (adjust, remove and refit, route, verify) list it `reused:`. Neither is summed.
3. A chapter's Hardware table counts that chapter's consumption. It may also carry a quantity bagged here for a later chapter, but only as a `carries:` entry in the map. The consuming chapter then writes `0: bagged at Step …` or leaves the row out.
4. `reused:` needs an earlier consumption of at least that count. `staged:` needs a later one. Ch 00 is inventory: none of its kit mentions are consumption.
5. Stock drawn on demand, cut stock, tools and conditional rows (`unreconciled:` in the map) are `consumable:` or `tool:` and never reconciled. Bag rows (one BOM line, several parts) are reconciled per chapter, but not against the BOM quantity.

## What the checks do now

**Per chapter (check 7).** Table total = the chapter's counted consumption, plus carries staged here, minus carries consumed here. Not summed:

- `staged:`, `reused:`, `tool:` and `consumable:` lines, and `— from` items.
- Inventory chapters.
- Unreconciled rows. Their table rows are skipped too.

**Across the manual (check 7, new kinds).**

- `double-count`: an owned row listed as fitted at a step the map does not name. The message says whether it should be `staged:` or `reused:`.
- `owner-missing`: a map step that does not list its quantity as fitted.
- `carry-unstaged` / `carry-unfitted`: a carry's staging or consuming step is wrong.
- `fake-reuse`: `reused:` with fewer units fitted before it.
- `staged-unfitted`: `staged:` with nothing fitted later.
- `over-bom`: running consumption of an unowned row passes the BOM quantity.
- `map-error`: the map names an unknown item or step.

**Check 6** adds `unreconciled-row` (write `consumable:`/`tool:`) and `staged-xref`.

**Commands.**

- Packet gate: `python3 scripts/lint_manual.py --strict-parts --chapters 05,06`. It exits 1 on any check 6/7 finding in those chapters only; the cross-chapter findings are filed under the chapter that holds the step. The default gate keeps 6/7 as WARN.
- Per-step evidence: `python3 scripts/parts.py --ledger 'Wago 221-415'`. It prints every mention of a BOM row in manual order, with its role, its count and the step's Source line, so equal totals cannot hide a wrong step.

## Cross-chapter ownership (the map, readable)

"Inv" = Ch 00 inventory step. Listed = Hardware tables that name it today.

| Item | Listed | Staged | Consumed at | Reused at | Evidence |
|---|---|---|---|---|---|
| MGN9H rail ×6 | 02 (4), 05 (2) | Inv 00.17; 02.05 | 02.06 ×1, 02.09 ×3, 05.11 ×1, 05.13 ×1 | — | Voron p.24–27, p.88 |
| MGN12H rail ×1 | 05 | Inv 00.17 | 05.33 | — | Voron p.101 |
| Nitehawk SB PCB | 08 | Inv 00.5 | 08.43 | — | Ch 08 table |
| SB fan adapter PCB | 08 | Inv 00.5 | 08.44 | 08.45 | Ch 08 table |
| USB adapter PCB | **09** | Inv 00.5 | **08.64** | 09.25 | Ch 09's own note: stack fitted at 08.64 |
| Leviathan brackets L/R | — | Inv 00.6 | 09.20 | 09.21 | LDO wiring guide |
| NH Adapter Mount | — | Inv 00.6 | 08.64 | 09.25 | Ch 08.64 |
| DIN clip ×4 | — | Inv 00.6 | 09.20 ×2, 09.25 ×1 | — | Ch 09 M2×10 row; 4th = spare (open) |
| CW2 chain anchor | — | Inv 00.6; 08.6 | 08.25 | 10.59 | Ch 08.25 |
| 2×3 splitter spacer ×2 | — | Inv 00.6 | 10.37, 10.47 | 11.18 | LDO wiring guide ("mount 3x2 splicing PCBs using the printed part") |
| LDO nozzle probe | — | Inv 00.6 | 09.27 | 09.30 | LDO build FAQ |
| Bed WAGO mount | — | Inv 00.6 | 09.34 | — | LDO wiring guide § bed WAGO mount |
| CW2 PCB spacer | — | Inv 00.6 | 08.43 | — | Ch 08.43 |
| Aluminium handle ×2 | 11 | Inv 00.7 | 11.60 | — | LDO extra |
| Revo HF hotend | 08 | Inv 00.3; 08.27 | 08.28 | 08.29 | Ch 08.28 (seated in the printhead) |
| DIN rails ×2 | 09 | Inv 00.3 | 09.5 | — | Voron p.29 |
| Leviathan | 09 | Inv 00.3; 09.19 | 09.21 | 10.3 | 09.19 strips jumpers on the loose board |
| PSU | 09, **10** | Inv 00.3; 09.14 | 09.15 | 09.16, 10.2 | 09.15 fits its DIN brackets |
| C13 cord | — | Inv 00.3; 09.35 | 10.23 | 12.11 | first plugged in at 10.23 |
| Deck panel | 02 | Inv 00.4; 02.12 | 02.13 | 09.4 | Voron p.28–29 |
| Bottom / back / side ×2 / top panels | — | Inv 00.4; 11.52, 11.56 | 11.21 / 11.55 / 11.57, 11.58 / 11.59 | — | Voron p.232–243 |
| PC door panels ×2 | — | Inv 00.4 | not used | — | Clicky-Clack replaces the doors (11.61) |
| Magnetic pad | 03 | Inv 00.4; 03.1 | 03.9 | 03.10 | Voron p.58 |
| Build plate | 03 | Inv 00.4; 03.1–03.8 | 03.14 | 03.15–03.18 | Voron p.60–61 |
| Flex plate | 03 | Inv 00.4; 03.1 | 03.20 | 13.42 | Ch 03.20 |
| AC inlet | 09, **10** | — | 09.11 | 10.5 | LDO wiring guide: Ch 10 is wiring only |
| WAGO 221-415 ×3 | 09, **10** | — | 09.13 | 10.7 | 10.7 itself: "populated and mounted at Step 09.13" |
| WAGO 221-412 ×2 | 09, **10** | — | 09.34 | — | LDO: "two WAGO terminals are snapped into the printed part" |
| 2×2 XH splicer | 09, **10** | — | 09.34 | 10.12 | LDO: "2x2 XH Splicer PCB is fastened using two M3x6 BHCS" |
| SSR + DIN bracket | 09, **10** | — | 09.17 | 09.18, 10.10 | Ch 09.17 |
| XY / Z endstop PCB | 09 | — | 09.32 / 09.28 | 10.33 / — | Voron p.164; Ch 09.28 |
| Pi 4B + heatsink | 09 | — | 09.22 | — | Ch 09.22 |
| 3×2 XH splicer ×2 | 10, **11** | — | 10.37 (LED), 10.47 (fans) | 11.18 | LDO: "two 6020 fans are joined using the 3x2 splicing PCB" |
| 60×60×20 fan ×2 | **11** | — | 10.47 (plugged) | 11.3, 11.11 | rule 1: first connected at 10.47. Open question 1 |
| Keystone CAT6 insert | **11** | — | 10.51 (plugged) | 11.10 | Ch 10.51 |
| 4.3" DSI display | — | 10.50 | 11.6 (run from 10.50) | 12.10 | 10.50 builds the module by running 11.5–11.6 |
| 5015 blower (toolhead) | 08 | 08.34 | 08.42 | — | Ch 08.42 |
| Drag chains 10×10 ×2 / 10×15 | 10 | — | 10.59, 10.60 / 10.62 | — | Voron p.197–203 |
| **Carry:** M3×30 SHCS ×2 | 05, **09** | 05.46 (bagged with the pod) | 09.33 | — | Voron p.164, checked on the page: 2× M3×30 through the pod |

Other cross-chapter fastener stacks, checked on the pages. None needs a map entry, only `reused:`.

- **p.29.** The four deck M5 T-nuts are consumed at 02.11, and 09.5 reuses them. Ch 09's table already says "0 new here".
- **p.90 + p.111.** The four M3 and four M5 rail-slot T-nuts are consumed at 05.14. At 06.7/06.8, the M3×30 and M5×30 (4 each on p.111) thread into them.
- **p.115.** Four M5×40 SHCS at 06.14/06.15. 06b.8 removes them and 06b.13 refits the same four, so 06b.13 is `reused:`.
- **p.67/p.71.** The front-idler M3×40 SHCS and M3 washers are consumed in Ch 04 (04.11, 04.18). Ch 07 only adjusts them (07.5).
- **p.91/93/95.** The upper-Z-clip M5×16 BHCS are consumed in Ch 05. 06.20 is `reused:`.

## Corrections for the content packets

Format: `step or table row: current → correct (evidence)`. Scope: ownership and table corrections.
The within-chapter count errors (per-unit counts in build-all-four steps, uncounted items, multi-item bullets) are listed by `--parts-report <ch>`. Fix them against the page images and use `--ledger` to check.

### P1: Ch 00, 00a, 01 (5)

1. 00.14: `KADRICK M3×H5 inserts ×7, one per pocket` → `M3×H5 heat-set insert ×7 — from KADRICK kit` (AGENTS.md ruling 2026-09-14; not kit stock).
2. 01.3: `1× M5 roll-in T-nut and 1× M3 roll-in T-nut (for the fit test — both go back in their bags)` → `tool: M5 roll-in T-nut, fit test, back in its bag` and `tool: M3 roll-in T-nut, fit test, back in its bag` (the step's own text).
3. Ch 01 table: `M3 T-nut, roll-in | 1` → delete. The only M3 T-nut in the chapter is 01.3's, and it goes back in the bag.
4. 01.6: `4× A extrusion (prepared, from Step 01.4)` → `reused: the four prepared A extrusions`. Today it is an over-BOM of 12 > 10. Sweep every A/B mention with `--ledger 470A` and `--ledger 530B`: count each extrusion once, at its first fastening, and make the rest `reused:`.
5. Ch 01 table: `Corner bracket | 4` is not an LDO 350 BOM row. Name the source (`— from …`) or the BOM item (open question 7).

### P2: Ch 02 (3, plus the per-unit counts)

1. 02.05: `MGN9H 400 mm rails ×4 (…)` → `staged: MGN9H 400 mm rail ×4` (owners 02.06/02.09).
2. 02.12: `deck panel` → `staged: deck panel`.
3. 02.15: `the four M5 T-nuts already in the bed extrusions. **No bolts and no DIN rails yet.**` → `reused: the four deck T-nuts`. The sentence moves to Do.
4. Twenty per-unit mismatches (build-all-four steps, G2-03) → step totals against p.30–47. This is within the chapter, so no map entry.

### P3: Ch 03, 04 (7)

1. 03.1: all three → `staged:` (build plate, magnetic pad, flex plate).
2. 03.2, 03.3, 03.7, 03.8: `build plate…` → `staged: build plate`. 03.14: `build plate assembly` → counted `build plate, magnet applied ×1` (owner 03.14; p.60–61).
3. 03.10: `Magnetic pad (applied), sharp craft knife` → `reused: the applied magnetic pad` and `tool: sharp craft knife`.
4. Ch 03 table: `M4×6 BHCS (bed PE) | 1` → `0: pre-fitted to the plate` (03.6 ⚠; 10.x only backs it out).
5. Ch 03 table: `M3×12 SHCS + M3 washer (thermal fuse) | 0` → delete. The fuse is pre-applied (03.5).
6. Ch 03 table: the build-plate name contains " + " (table-multi) → `Build plate, cast 5083, heatpad and 125 °C fuse pre-applied`.
7. 04.28: `a 6 mm belt offcut or a thin steel rule` → `tool: a 6 mm belt offcut or a thin steel rule`.

### P4: Ch 05 (8)

1. 05.1: `C extrusion ×2, D extrusion ×1, E extrusion ×1` → three `staged:` bullets. Today it is an over-BOM, E 2 > 1; they are fitted at 05.5 (E), 05.11/05.13 (C) and the D step.
2. 05.4: `M5 roll-in T-nut ×26, M3 roll-in T-nut ×≈32 (+ ~30 for the backers)` → `staged: M5 roll-in T-nut ×26` and `staged: M3 roll-in T-nut ×N` (exact). Today M5 counts 52 against a table of 26: the consuming steps are 05.5, 05.13, 05.14 and 05.36.
3. 05.12: `the ~10 M3×8 SHCS already started` → `reused:`.
4. 05.13: split into `C extrusion ×1`, `MGN9H 400 mm rail ×1` (owner), `M3 roll-in T-nut ×N` and `M3×8 SHCS ×N`.
5. 05.46: split into `staged: M3×30 SHCS ×2` (carry to 09.33, p.164), `staged: [a]_endstop_pod_D2F_switch ×1` and `staged: [a]_cable_cover ×1`.
6. Ch 05 table: `MGN9H rail + carriage` → `MGN9H 400 mm rail | 2`; `MGN12H rail + carriage` → `MGN12H 400 mm rail | 1` (table-multi).
7. Ch 05 table: `M3×30 SHCS | 2` → Qty `2: bagged with the endstop pod at 05.46, fitted at 09.33 (p.164)`.
8. Ch 05 table: `Titanium backer, Y/X` and `M3×8 FHCS (backers, Y)` → `— from Ti backer set`. The West3D set ships 22× M3×8 FHCS and 10× M3×6 FHCS, per the note under the table. `M3×6 FHCS (backers, X) | ~8` → `— from Ti backer set` too, or it double-counts against the kit's M3×6 FHCS. The `≈`/`~` quantities need numbers: count the rail holes (p.88, p.101).

### P5: Ch 06, 07 (7)

1. 06.8: `the remaining 3× belt, 3× lower clip, 3× block, 3× M3×30 SHCS, 3× M5×30 BHCS` → counted bullets, so that 06.7 + 06.8 = 4 M3×30 and 4 M5×30 (p.111).
2. 06.20: `the two M5×16 BHCS on top of this corner (already in place)` → `reused:` (Ch 05, p.91/93/95).
3. 06b.8: `the four M5×40 SHCS from step 06.14` → `reused: the four Z-joint M5×40 SHCS` (no step ref).
4. 06b.13: `M5×40 SHCS ×4` → `reused: the four Z-joint M5×40 SHCS`. These are the same bolts (p.115: 4 total, table 4).
5. Ch 06 table: `Rubber rail stopper | 4` → `— from the Z rails` (not a BOM row; they ship on the rails).
6. 07.5: `the two M3×40 SHCS + M3 washers already in the front idlers (Ch 04, p.67 and p.71)` → `reused: the two front-idler M3×40 SHCS and M3 washers`.
7. Ch 07 table: `M3×40 SHCS + M3 washer | 2 + 2` → delete. They are consumed and listed in Ch 04 (p.67, p.71).

### P6: Ch 08 (12)

1. 08.27: the Revo parts → `staged:` (it assembles the loose hotend). 08.28: `Revo assembly` → counted `E3D Revo HF hotend, assembled ×1` (owner).
2. 08.29: hotend mentions → `reused:`.
3. 08.34: `50×50×15 centrifugal fan (24 V) ×1, flush cutters, small flat file` → `staged: 5015 blower ×1`, `tool: flush cutters` and `tool: small flat file`. 08.42: add counted `50×50×15 centrifugal fan ×1` (owner).
4. 08.41: `hotend fan wires` → `reused: the hotend fan's leads` (fitted at 08.40).
5. 08.43: split into `Nitehawk-SB V2 toolboard ×1`, `CW2 PCB Spacer ×1` and `M3×8 SHCS ×2` (owner for both boards).
6. 08.6: the anchor → `staged:`. 08.25: split into `CW2 Chain Anchor Tilted ×1` (owner) and `M3×20 SHCS ×1`.
7. 08.45: `fan adapter PCB, magnifier` → `reused: the fan adapter PCB` and `tool: magnifier`.
8. 08.50, 08.63: the toolhead cable and probe lead → `reused:`. 08.60 is the counted plug-in. Ch 08 table: rename `Toolhead cable (combined USB + 24 V), XT30(2+2)` → `Toolhead cable, USB and 24 V, XT30(2+2)` (table-multi).
9. 08.33: `E0508 ferrules ×2` → `consumable: E0508 ferrule ×2, only if re-terminating`. VE0508 is spare stock: the LDO wiring guide uses E0508 only for an integrated-heater hotend. Ch 08 table: `Ferrule, E0508 | 2` → delete or a `consumable` note.
10. Ch 08 table: `PTFE 4 mm OD / 2 mm ID, 10 cm` → `PTFE tube, 4 mm OD, 2 mm ID, 10 cm` (the `/` trips table-multi).
11. Ch 08 table: add `USB Adapter PCB | 1` and `NH Adapter Mount | 1` (fitted at 08.64). `M3×10 SHCS | 3` and `Ring-lug ground wire…` are not LDO BOM rows: name the source or fix the size (open question 6).
12. Steps that fit table rows but do not count them:
    - MR85 ×2: 08.12, 08.14.
    - IDGA gear set.
    - M3×50 ×2: 08.62, a multi-item bullet.
    - Captive M3×6: 08.51.
    - 16 inserts: 08.3, 08.4, 08.6 … now parse as ×4/×4/×3 after the count fix.

    Count them in their steps.

### P7: Ch 09, 10 (21)

1. 09.4: `deck panel ×1 (already fitted in Ch 02)` → `reused: the deck panel`.
2. 09.5: split into `DIN rail ×2` (owner), `DIN rail plastic end cap ×4`, `M5×10 BHCS ×4` and `reused: the four deck T-nuts` (p.29).
3. 09.14: `Meanwell LRS-200-24 ×1` → `staged:`. 09.15: add counted `Meanwell LRS-200-24 PSU ×1` (owner). 09.16: → `reused:`.
4. 09.19: → `staged: LDO Leviathan mainboard ×1` and `tool: a small pot or bag for the jumpers`. 09.21: split into `LDO Leviathan mainboard ×1` (owner), `reused: the two bracket assemblies` and `M3×8 SHCS ×4`.
5. 09.22: split into `Raspberry Pi 4B ×1`, `Raspberry Pi heatsink ×1` and standoffs `— from …` (verify).
6. 09.23: `Raspberry Pi 3/4 HAT power adapter ×1` → add `— from <its box>` (open question 5). It has no BOM row and falsely matches the Pi.
7. 09.33: keep `M3×30 SHCS ×2` counted (the carry's consumption). The "bagged by Ch 05" prose moves to Do.
8. 09.35: → `consumable: VE0508 ferrule ×5`, `staged: C13 power cord ×1` and `tool: cable tags`. The ring terminal needs a source.
9. 09.36, 10.80: `VHB tape`/`VHB pad` → `consumable:`.
10. Ch 09 table: `M3×30 SHCS | 2` → `0: bagged with the pod at Step 05.46` (carry).
11. Ch 09 table: `Ferrule, VE0508 | 5 | fitted in Ch 10…` → delete. They are spares; Ch 10's own row says so.
12. Ch 09 table: the `SSR + bracket | 1 + 1`, `Pi 4B + heatsink + standoffs + HAT | 1 set`, `XY / Z / USB adapter / 2×2 splicer | 1 each` and `GT2 pulley + shaft + set screw | 1 each` rows → one row each.
    - USB adapter PCB moves to Ch 08.
    - The nozzle-probe row becomes `LDO Nozzle Probe, collar and shaft pre-fitted | 1` (BOM: `Shaft, for Nozzle Probe`), plus the set screw if it is bagged.
13. Ch 09 table: add `Leviathan Bracket Left | 1`, `Leviathan Bracket Right | 1`, `DIN Clip | 3`, `LDO Nozzle Probe | 1` and `Bed WAGO Mount | 1`. `M3×5×4 heat-set insert | 2+` → an exact total.
14. 10.2, 10.3, 10.5, 10.10, 10.12: → `reused:` (the PSU, the Leviathan, the inlet, the SSR and the bed breakout, all fitted in Ch 09).
15. 10.7: → `reused: the three WAGO 221-415 blocks`.
16. 10.33: split into `XY endstop cable ×1` and `reused: the XY endstop PCB`.
17. 10.50: the display and the module parts → `staged:` (fitted at 11.5–11.6, which run from here). The FFC ribbon needs a source (the display box).
18. 10.54, 10.65, 10.67: the umbilical → `reused:` (plugged in at 08.60).
19. 10.23: `C13 power cord ×1. No meter` → `C13 power cord ×1` (owner). "No meter" moves to Do.
20. 10.59, 10.60, 10.62: split so that each chain is a counted bullet (owners).
21. Ch 10 table:
    - **Delete**, fitted in Ch 09: the `AC inlet`, `Meanwell PSU`, `SSR + DIN bracket`, `WAGO 221-415`, `WAGO 221-412` and `2×2 XH splicer` rows. Or write `0: fitted Ch 09`.
    - **Delete**: `VE0508 ferrule | 5` (spares).
    - **Add**: `60×60×20 fan | 2`, `Keystone CAT6 insert | 1`, `C13 power cord | 1` and `2×3 Splitter Spacer | 2`.
    - **Split**: `M5×10 BHCS + M5 roll-in T-nut | 2 + 2` and its frame-PE row → `M5×10 BHCS | 3` and `M5 roll-in T-nut | 3`.
    - **Number**: `M3×6 FHCS (chain ends) | (verify on bench)` needs a quantity.
    - **Count in steps**: the 20 inserts (10.35 is a multi-item bullet).

### P8: Ch 11 (11)

1. 11.3, 11.11: `60×60×20 mm 24 V fan ×2` → `reused: the two bay fans` (plugged in at 10.47; open question 1).
2. 11.10: `Keystone CAT6 insert ×1 (supplied)` → `reused:`. 11.18: `3×2 XH splicer PCB ×1, its printed spacer` → `reused:`.
3. 11.6: the display counts here (owner). `M2.5×6 screws ×4` → `— from BTT screen packaging`; the table row gets the same.
4. 11.21: split out `bottom panel ×1` (owner).
5. 11.52 and 11.56: the panels → `staged:`. 11.55: `back panel assembly from 11.52–11.54` → counted `back panel ×1`. 11.57, 11.58: add `side panel, PC clear 483×503 ×1` each. 11.59: split out `top panel ×1`.
6. 11.27: `5015 fan ×2` → `staged:`. 11.32 counts the two Nevermore 5015s. 11.29, 11.31 → `reused:`; they also alias to the toolhead 5015 row, see the resolver list.
7. 11.34, 11.36: `6×3 mm neodymium magnets` → a count (the table claims 8; the LDO guide gives none: verify on bench).
8. 11.48: `6×3 mm magnets ×12` → `6×3 mm magnet ×12 — from Clicky-Clack door kit`. KB3D: *"the magnets that were provided in the hardware kit for the Door Kit"*. The mod BOM says 12, but 11.48's own Do places 4 + 4 + 1 + 1 = 10 (open question 3).
9. 11.44, 11.50, 11.62, 11.64 and the latch steps: the door-kit hardware → `— from Clicky-Clack door kit` (tanaes mod BOM: M5×16 BHCS ×4, M5×45 dowel ×4, M5×7×8 bushing ×6, M3×20 SHCS ×4, M3×8 SHCS ×12, M3×8 BHCS ×1, M3×5×4 insert ×1). The M3 roll-in T-nuts stay kit (KB3D). `the 480 × 500 × 3 mm clear acrylic door panel` → `Clicky-Clack door panel ×1 — from Clicky-Clack acrylic panel` (Fabreeko line item; not the kit's PC doors).
10. Ch 11 table:
    - **Delete**: the `60×60×20 fan`, `3×2 XH splicer PCB` and `Keystone CAT6 insert` rows (Ch 10 owns them).
    - **Magnets**: split into `6×3 mm magnet | N` (Nevermore, kit) and `6×3 mm magnet — from Clicky-Clack door kit | 12`. Today they total 20 against a BOM of 16.
    - **Door-kit rows**: the dowel, bushing, M3×20 ×4, M3×8 ×12, M3×8 BHCS, Clicky M5×16 ×4 and latch insert ×1 rows → `— from Clicky-Clack door kit`.
    - **Not BOM rows**: `M3×16 BHCS | 4` (Nevermore) → `— from Nevermore Micro V5 Parts bag` (verify).
11. Ch 11 table quantities:
    - `M3 hammerhead T-nut | 7 + 8 + 16 + 4` → `35: 7 back + 8 top + 16 side + 4 Z covers`.
    - `M3×8 SHCS | belt guards…` and `M3 heat-set insert | skirt segments` → numbers.

### P9: Ch 12, 13, 14 (5)

1. 12.10: → `**Parts:** none.` The prose moves to Do.
2. 12.11: `C13 power cord ×1` → `reused: the C13 cord`.
3. 13.42: `clean flex plate` → `reused: the flex plate`.
4. 14.24: `M3×8 SHCS ×2, M3 roll-in T-nut ×2` (nameplate) → counted. Add them to Ch 14's table, which says "none" today.
5. 14.6: `the four M5×40 Z joint SHCS (already fitted, light)` → `reused:`.

### Not content: resolver aliases (`scripts/kit_bom.py` ALIASES + the vendored YAML; owner 1A)

These produce false double counts that no content edit can clear:

- SSR `\bssr\b(?!.*\bbracket\b)` matches "SSR to Wago cable" and "SSR to MB cable" (10.11, 10.27). Proposed: `(?!.*\b(?:bracket|cable)\b)`.
- Pi `\braspberry pi\b…` matches "Raspberry Pi 3/4 HAT power adapter" (09.23). Proposed: exclude `\bhat\b`.
- 5015 `\b5015\b(?!.*nevermore)` matches Nevermore fans on lines without the word (11.29, 11.31).

## Open questions

1. Bay fans: rule 1 puts consumption at 10.47 (first plugged in), so Ch 10's table owns them. If Alex prefers "physically mounted", flip the owner to 11.11 and move the table row back to Ch 11. It is a one-line map change.
2. The 4th DIN clip: a spare, or does a step use it?
3. Clicky-Clack magnets: 12 (mod BOM) against 10 (11.48's Do). Does LDO's door hardware kit also carry the M5×16, M3×20 and M3×8 screws? KB3D states only the magnets explicitly. (verify on bench)
4. Nevermore magnet count (8 in the table) is unverified.
5. Sources of the Pi HAT power adapter, the Leviathan standoffs and the FFC ribbon.
6. `M3×10 SHCS` (Ch 08, USB adapter stack), `M3×16 BHCS` (Nevermore) and the Ch 08 ring-lug wire are not LDO 350 BOM rows.
7. Ch 01 `Corner bracket` is not an LDO 350 BOM row.
8. Phase 3a converted `**Parts:** none — reason` into a `- none — reason` bullet (00a.8, 13.1, 13.2, 13.24, 13.34 …). Check 6 flags each one twice. They should go back to `**Parts:** none.`, with the reason in Do.
