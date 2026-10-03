# Chamber exhaust housing — add-on (Ch 14 Part H)

Optional. On no plate, in no batch (B00–B11), in no run total. **Printed only after Ch 14 Step 14.25 has
checked the back of the real machine** (stock notch, free depth behind it, extrusion slot, lead route,
spare jumper); never ahead of kit day.

## Licence and credit

**GPL-3.0** (<https://github.com/VoronDesign/Voron-2/blob/a192410/LICENSE>). The parts are the Voron Design
team's stock Voron 2.4r2 exhaust filter, *unchanged*: `VoronDesign/Voron-2` at
`a192410e27ea345644ae5c4b29b4c9c40cbe1a73` (branch `Voron2.4`), folder `STLs/Exhaust_Filter/`. Nothing is
remixed, so nothing is committed here; the files are fetched like every other stock part.

## Files

`python3 slicer/fetch_stls.py` downloads them to `slicer/stl/voron2/STLs/Exhaust_Filter/` (gitignored).
`slicer/plates.py` `ADDONS` lists them and `slicer/stl/MANIFEST.sha256` pins their hashes, so
`python3 slicer/fetch_stls.py --verify` fails if one changes. `sources.yml` pins the Voron-2 repo commit;
`python3 scripts/sources_verify.py --git-only` reports when it moves.

| File | Qty | Colour | Job |
|---|---:|---|---|
| `exhaust_filter_housing.stl` | 1 | Black | 1 |
| `[a]_exhaust_fan_grill.stl` | 1 | Blue | 2 |
| `[a]_filter_access_cover.stl` | 1 | Blue | 2 |
| `[a]_exhaust_filter_mount_x2.stl` | 2 | Blue | 2 |
| `exhaust_filter_grill.stl` | — | — | already printed in B09-P3 and fitted at Ch 11 Step 11.54; Part H reuses it |

## Print

Two jobs on the Core One+, smooth sheet, as oriented, **no supports**, Voron spec (4 walls, 5 top/bottom,
40 % grid, 0.2 mm):

| Job | Profile | PrusaSlicer 2.9.6 CLI estimate |
|---|---|---|
| 1 — housing | `slicer/voron-coreone-asa.ini`, Galaxy Black ASA | 66.0 g, 5 h 03 m |
| 2 — fan grill, access cover, 2 mounts | `slicer/voron-accent-blue.ini`, blue accent ASA | 34.6 g, 2 h 04 m |

Estimates were sliced with the parts laid side by side, not GUI-arranged (2026-10-03). Bin with Ch 14.

## Hardware (all kit spares except the purchase)

8 × M3×5×4 heat-set insert, 4 × M3×30 SHCS (fan and grill), 2 × M3×8 SHCS (access cover), 2 × M5 roll-in
T-nut and 2 × M5×10 BHCS (mounts), VHB tape; the two M3×12 SHCS come off the exhaust cover. Bought (Ch 00
Step 00.8): a 60×60×20 mm 24 V fan, a 1 m JST-XH 2-pin extension, carbon filter mat. Counts from the Voron
2.4r2 assembly CAD and manual p.250–256; design record `review/2026-10-03-exhaust/DESIGN.md`.

## Upstream changes

A `CHANGED VoronDesign/Voron-2` line from `sources_verify.py` means: compare `STLs/Exhaust_Filter/` across
the two commits, and re-fetch and re-slice before printing if any of these files moved.
