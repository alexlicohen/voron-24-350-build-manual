# Print batches — overview

27 plates, **157.1 h**, **1813 g Galaxy Black + 279 g Prusa Orange**. Every hour and gram on this page is a
**PrusaSlicer 2.9.6 estimate**, sliced from the committed project for that plate (`slicer/plates/*.3mf`) —
not a throughput model. Method and what these figures replaced:
[print plan §4.1](../../voron-print-plan.md#41-how-these-numbers-were-produced). Per-plate detail with the
previous figure beside each one, and the exact unrounded values, are in `slicer/estimates.csv`;
`python3 slicer/check_docs.py` re-checks every number on this page against it.

| batch | plates | hours | g black | g orange | unlocks | hard prereqs |
|---|---:|---:|---:|---:|---|---|
| [B00](B00-calibration-and-jigs.md) | 1 | 4.0 | 52 | 0 | Frame | — |
| [B01](B01-z-drive-assemblies.md) | 2 | 22.8 | 301 | 0 | Z Drives and Idlers | B00;B02 |
| [B02](B02-accent-parts-orange.md) | 3 | 21.9 | 0 | 279 | accent for Z Drives/Idlers, A/B Drives/Idlers, Gantry, Stealthburner, Skirts | B00 |
| [B03](B03-ab-drive-units-and-front-idlers.md) | 2 | 8.5 | 119 | 0 | A/B Drives and Idlers | B00;B02 |
| [B04](B04-xy-joints-and-x-carriage.md) | 1 | 8.6 | 117 | 0 | Gantry | B00;B02;B03 |
| [B05](B05-z-joints-and-z-chain.md) | 1 | 6.4 | 78 | 0 | Z Axis; A/B Belts | B00;B02;B04 |
| [B06](B06-toolhead-sb-cw2-klicky.md) | 2 | 12.2 | 148 | 0 | Stealthburner | B00;B02;B04 |
| [B07](B07-electronics-bay-and-lighting.md) | 3 | 16.0 | 226 | 0 | Electronics; Controller; Wiring | B00 |
| [B08](B08-skirts-and-front-modules.md) | 6 | 29.2 | 399 | 0 | Skirts | B00;B02;B07 |
| [B09](B09-panels-filtration-spool.md) | 5 | 21.8 | 297 | 0 | Panels | B00;B08 |
| [B10](B10-clicky-clack-door.md) | 1 | 5.7 | 76 | 0 | Panels (front door) | B00;B02;B09 |
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
plate lands on its slicer number.

**When to swap.** Never mid-plate on purpose — but a runout *during* a plate is fine and expected: the
Core One+ runout sensor pauses, you load the next spool and it resumes. Two runouts are predicted, both on
plates where a resume seam does not matter:

- **B06-P2** (the Klicky set) — spool #1 has about 36 g left when it starts.
- **B09-P3** (exhaust grill, spool holder, Z belt covers) — spool #2 has about 30 g left when it starts.

Two exceptions, where you start on a fresh spool whatever is left:

- **B01-P1** — 15.2 h and 201 g of Z-drive bodies. A resume seam on a bearing-seat part is not worth it.
- **B02-P1/P2/P3** — the whole orange session runs on the one accent spool; two colour changes in the entire
  build, and that is the point ([print plan §4.3](../../voron-print-plan.md#43-spool-changes)).

| plate | slicer g | actual g (weigh) | spool # | remaining |
|---|---:|---:|---|---:|
| B00-P1 | 52 | | #1 | 748 |
| B01-P1 | 201 | | #1 | 547 |
| B01-P2 | 100 | | #1 | 447 |
| B02-P1 | 90 | | O1 | 710 |
| B02-P2 | 93 | | O1 | 617 |
| B02-P3 | 96 | | O1 | 521 |
| B03-P1 | 60 | | #1 | 387 |
| B03-P2 | 59 | | #1 | 328 |
| B04-P1 | 117 | | #1 | 211 |
| B05-P1 | 78 | | #1 | 133 |
| B06-P1 | 97 | | #1 | 36 |
| B06-P2 | 51 | | **#1 → #2 mid-plate** | 785 |
| B07-P1 | 67 | | #2 | 718 |
| B07-P2 | 124 | | #2 | 594 |
| B07-P3 | 35 | | #2 | 559 |
| B08-P1 | 99 | | #2 | 460 |
| B08-P2 | 67 | | #2 | 393 |
| B08-P3 | 71 | | #2 | 322 |
| B08-P4 | 66 | | #2 | 256 |
| B08-P5 | 70 | | #2 | 186 |
| B08-P6 | 26 | | #2 | 160 |
| B09-P1 | 63 | | #2 | 97 |
| B09-P2 | 67 | | #2 | 30 |
| B09-P3 | 55 | | **#2 → #3 mid-plate** | 775 |
| B09-P4 | 56 | | #3 | 719 |
| B09-P5 | 56 | | #3 | 663 |
| B10-P1 | 76 | | #3 | 587 |
| **TOTAL black** | **1813** | | 3 × 800 g | **587 g margin** |
| **TOTAL orange** | **279** | | 1 × 800 g | **521 g margin** |
