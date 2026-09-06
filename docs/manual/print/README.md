# Print batches — overview

27 plates, **157.1 h**, **1813 g Galaxy Black + 279 g Prusa Orange**. Every hour and gram on this page is a
**PrusaSlicer 2.9.6 estimate**, sliced from the committed project for that plate (`slicer/plates/*.3mf`) —
not a throughput model. Method and what these figures replaced:
[print plan §4.1](../../voron-print-plan.md#41-how-these-numbers-were-produced). Per-plate detail with the
previous figure beside each one, and the exact unrounded values, are in `slicer/estimates.csv`;
`python3 slicer/check_docs.py` re-checks every number on this page against it.

**Print order.** Six batches need only **Gate A** (the cube, Step B00.5) and print before the kit arrives:
**B00 → B02 → B07 → (Gen 2 belt upgrade, cube re-passed) → B08 → B09 → B10** — 98.6 h. The five with
bearing seats and shaft bores need **Gate B** (Step B00.7: 625-2RS bore, MGN12 rail, real inserts) and start
the day the kit lands: **B01 → B03 → B04 → B05 → B06** — 58.5 h, printing under Ch 00–05. The "print gate"
column is the *print* prerequisite; which assembly chapter consumes a batch is the "feeds" column, and the
chapter-level prerequisite lists live in [00-index.md](../00-index.md#chapters).

| batch | plates | hours | g black | g orange | feeds (assembly chapter) | print gate |
|---|---:|---:|---:|---:|---|---|
| [B00](B00-calibration-and-jigs.md) | 1 | 4.0 | 52 | 0 | Ch 00 (heat-set coupon, rail guides); Ch 02 / 05 (rail guides); Ch 02 / 04 (`pulley_jig`); B01 (one retainer) | — (it is the gate) |
| [B02](B02-accent-parts-orange.md) | 3 | 21.9 | 0 | 279 | accent for Ch 02, 04, 05, 06, 08, 11; `Handle` for B10 | Gate A |
| [B07](B07-electronics-bay-and-lighting.md) | 3 | 16.0 | 226 | 0 | Ch 09 Electronics bay; Ch 10 Wiring | Gate A |
| [B08](B08-skirts-and-front-modules.md) | 6 | 29.2 | 399 | 0 | Ch 11 Part A Skirts | Gate A, re-passed after the Gen 2 upgrade |
| [B09](B09-panels-filtration-spool.md) | 5 | 21.8 | 297 | 0 | Ch 11 Panels, Nevermore, spool | Gate A (after B08) |
| [B10](B10-clicky-clack-door.md) | 1 | 5.7 | 76 | 0 | Ch 11 Clicky-Clack door | Gate A (after B09) |
| [B01](B01-z-drive-assemblies.md) | 2 | 22.8 | 301 | 0 | Ch 02 Z Drives and Idlers | **Gate B** (kit day) |
| [B03](B03-ab-drive-units-and-front-idlers.md) | 2 | 8.5 | 119 | 0 | Ch 04 A/B Drives and Idlers | Gate B |
| [B04](B04-xy-joints-and-x-carriage.md) | 1 | 8.6 | 117 | 0 | Ch 05 Gantry | Gate B |
| [B05](B05-z-joints-and-z-chain.md) | 1 | 6.4 | 78 | 0 | Ch 06 Z axis; Ch 07 A/B belts | Gate B |
| [B06](B06-toolhead-sb-cw2-klicky.md) | 2 | 12.2 | 148 | 0 | Ch 08 Stealthburner (Klicky set bagged, Ch 08.54) | Gate B |
| **TOTAL** | **27** | **157.1** | **1813** | **279** | | |

**Filament margin:** Black 1813 g needed / 2400 g on hand → **587 g margin (32 %)**. Orange 279 g needed /
800 g on hand → **521 g margin (187 %)**. Setup and the full override table:
[00-slicer-setup.md](00-slicer-setup.md).

## Spool ledger

The margin above is a prediction. This table is where it gets checked. **Weigh the spool before and after
each plate** and write the difference into *actual g*. A plate that misses its slicer figure by more than
about 5 g means the flow is off, not that the estimate is wrong — check extrusion multiplier before the next
plate rather than after five more.

Spool numbering: **#1 · #2 · #3** are the three 800 g Galaxy Black spools, **O1** the single 800 g Prusa
Orange. *Remaining* is what should be left on the active spool once that plate is off the bed, if every
plate lands on its slicer number. Rows are in **print order** — the six pre-kit batches, then the five
kit-day batches.

**When to swap.** Never mid-plate on purpose — but a runout *during* a plate is fine on a part with no
bearing seat: the Core One+ runout sensor pauses, you load the next spool and it resumes. One runout is
predicted, on such a plate:

- **B09-P2** (Nevermore cartridge, exhaust cover) — spool #1 has about 60 g left when it starts.

Two rules that override the ledger:

- **B01-P1 needs ≥ 201 g on the spool at start** (the ledger has it on spool #2 with ~550 g — fine). If a
  reprint or an extra plate has pushed the active spool under ~230 g, start B01-P1 on a fresh one and
  re-derive the ledger from your weighings — a resume seam on a Z-drive body is not worth it.
- **B05-P1 starts spool #3** even though #2 still has ~13 g: a resume seam on a Z joint's shaft bore is not
  worth 13 g. Keep the stub for a clip reprint.
- **B02-P1/P2/P3** run back to back on the one accent spool — two colour changes in the entire build, and
  that is the point ([print plan §4.3](../../voron-print-plan.md#43-spool-changes)).

| plate | slicer g | actual g (weigh) | spool # | remaining |
|---|---:|---:|---|---:|
| B00-P1 | 52 | | #1 | 748 |
| B02-P1 | 90 | | O1 | 710 |
| B02-P2 | 93 | | O1 | 617 |
| B02-P3 | 96 | | O1 | 521 |
| B07-P1 | 67 | | #1 | 681 |
| B07-P2 | 124 | | #1 | 557 |
| B07-P3 | 35 | | #1 | 522 |
| B08-P1 | 99 | | #1 | 423 |
| B08-P2 | 67 | | #1 | 356 |
| B08-P3 | 71 | | #1 | 285 |
| B08-P4 | 66 | | #1 | 219 |
| B08-P5 | 70 | | #1 | 149 |
| B08-P6 | 26 | | #1 | 123 |
| B09-P1 | 63 | | #1 | 60 |
| B09-P2 | 67 | | **#1 → #2 mid-plate** | 793 |
| B09-P3 | 55 | | #2 | 738 |
| B09-P4 | 56 | | #2 | 682 |
| B09-P5 | 56 | | #2 | 626 |
| B10-P1 | 76 | | #2 | 550 |
| *— kit day: Gate B —* | | | | |
| B01-P1 | 201 | | #2 | 349 |
| B01-P2 | 100 | | #2 | 249 |
| B03-P1 | 60 | | #2 | 189 |
| B03-P2 | 59 | | #2 | 130 |
| B04-P1 | 117 | | #2 | 13 |
| B05-P1 | 78 | | **#3 (fresh; #2's 13 g kept)** | 722 |
| B06-P1 | 97 | | #3 | 625 |
| B06-P2 | 51 | | #3 | 574 |
| **TOTAL black** | **1813** | | 3 × 800 g | **587 g margin** (574 on #3 + 13 on #2) |
| **TOTAL orange** | **279** | | 1 × 800 g | **521 g margin** |
