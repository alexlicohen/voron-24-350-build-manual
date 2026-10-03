# Nozzle scrubber with sheet stops — add-on print (Ch 13 Part L)

Fitted at Ch 13 Steps 13.44–13.50. Not on any plate, not in B00–B11, not in any run total.

## Licence and credit

**CC BY-NC-SA 4.0** (<https://creativecommons.org/licenses/by-nc-sa/4.0/>). Derived from
**jinetix**, *Voron 2.4 Silicone Nozzle Scrubber w/ Sheet Stops (Beacon / Carto Compatible)*,
<https://www.printables.com/model/796563> (CC BY-NC-SA), objects of its `10mm Bed Setup.3mf`.
The macros in Ch 13 Step 13.48 are adapted from the same page (revision 2025-12-22).
Changes made in this repo, 2026-10-03, are listed below; they are shared under the same licence.

## Files

| File | From | Change | Qty |
|---|---|---|---:|
| `brush_bracket_low1.5_MIRROR.stl` | brush bracket ("Decontaminator") | mirrored for the left bed extrusion; wiper seat and its posts lowered 1.5 mm | 1 |
| `350mm_bucket_trim2_MIRROR.stl` | 350 mm bucket | mirrored; top trimmed 2.0 mm | 1 |
| `jinetix_10mm_stop_bracket.stl` | stop bracket | none (symmetric), print-oriented | 1 |

Why lower: this build's Omron rides closer to the plate than the eddy probes the design targets, so
the stock wiper top (+1.55 mm above the sheet) would need ≥ 1.65 mm of Omron clearance; the low set
needs ≥ 0.52 mm. Remix script and design record: `review/2026-10-03-scrubber/` (`remix_low.py`,
`DESIGN.md`).

## Print

One plate on the Core One+, smooth sheet, `slicer/voron-coreone-asa.ini` (Voron spec: 4 walls,
5 top/bottom, 40 % grid, 0.2 mm), Galaxy Black ASA, as oriented (flat base down), **no supports**.
PrusaSlicer 2.9.6 CLI estimate: **38.3 g, 2 h 30 m**. Any time after B10; bin with Ch 13.
