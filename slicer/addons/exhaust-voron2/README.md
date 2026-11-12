# Chamber exhaust housing — batch B13 (Ch 14 Part H)

On plates **B13-P1 and B13-P2**, the last batch of the ASA run (Alex 2026-11-12: part of the build; an add-on
printed after Step 14.25 until then), and in the run's totals. **Fitted only after Ch 14 Step 14.25 has checked
the back of the real machine** (stock notch, free depth behind it, extrusion slot, lead route, spare jumper); if a
row there fails, the printed parts stay in bin `14-exhaust` unused and nothing is bought.

## Licence and credit

**GPL-3.0** (<https://github.com/VoronDesign/Voron-2/blob/a192410/LICENSE>). The parts are the Voron Design
team's stock Voron 2.4r2 exhaust filter, *unchanged*: `VoronDesign/Voron-2` at
`a192410e27ea345644ae5c4b29b4c9c40cbe1a73` (branch `Voron2.4`), folder `STLs/Exhaust_Filter/`. Nothing is
remixed, so nothing is committed here; the files are fetched like every other stock part.

## Files

`python3 slicer/fetch_stls.py` downloads them to `slicer/stl/voron2/STLs/Exhaust_Filter/` (gitignored).
`slicer/plates.py` `PLATES` (B13-P1, B13-P2) lists them and `slicer/stl/MANIFEST.sha256` pins their hashes, so
`python3 slicer/fetch_stls.py --verify` fails if one changes. `sources.yml` pins the Voron-2 repo commit;
`python3 scripts/sources_verify.py --git-only` reports when it moves.

| File | Qty | Colour | Plate |
|---|---:|---|---|
| `exhaust_filter_housing.stl` | 1 | Black | B13-P1 |
| `[a]_exhaust_fan_grill.stl` | 1 | Blue | B13-P2 |
| `[a]_filter_access_cover.stl` | 1 | Blue | B13-P2 |
| `[a]_exhaust_filter_mount_x2.stl` | 2 | Blue | B13-P2 |
| `exhaust_filter_grill.stl` | — | — | already printed in B09-P4 and fitted at Ch 11 Step 11.54; Part H reuses it |

## Print

Two plates of the ASA run on the Core One+, satin sheet, no glue, as oriented, **no supports**, the inis' Voron
settings (4 walls, 5 top/bottom, 40 % gyroid, 0.2 mm), packed by `python3 slicer/build_plates.py --repack B13-P1
B13-P2 --packer=platearrange` and committed as `slicer/plates/B13-P1.3mf` and `B13-P2.3mf`. Every part is 30 mm or
longer, so each carries the run's 3 mm per-object brim (`plates.brim_for`); both plates meet the 25 mm edge and
6 mm gap rules with no exemption. Page: `docs/manual/print/B13-exhaust-housing.md`.

| Plate | Profile | PrusaSlicer 2.9.7 estimate |
|---|---|---|
| B13-P1 — housing | `slicer/voron-coreone-asa.ini`, Galaxy Black ASA | 66.1 g, 4 h 31 m |
| B13-P2 — fan grill, access cover, 2 mounts | `slicer/voron-accent-blue.ini`, blue accent ASA | 35.1 g, 1 h 56 m |

All five pieces go in bin `14-exhaust` (`slicer/bins.py` `ASSIGN`), the housing in bag 1 and B13-P2's parts in
bag 2 with the bought fan, lead and mat; `exhaust_filter_grill` stays in `11-finish`, where B09 sorted it, since
it is fitted at Step 11.54 and reused in place at Step 14.29.

## Hardware (all kit spares except the purchase)

8 × M3×5×4 heat-set insert, 4 × M3×30 SHCS (fan and grill), 2 × M3×8 SHCS (access cover), VHB tape; the
mounts reuse the exhaust cover's 2 × M5 roll-in T-nut and 2 × M5×10 BHCS (Ch 11 Step 11.55), and the two
M3×12 SHCS and the PTFE coupler come off the cover too. Bought (Ch 00
Step 00.8): a 60×60×20 mm 24 V fan, a 1 m JST-XH 2-pin extension, carbon filter mat. Counts from the Voron
2.4r2 assembly CAD and manual p.250–256; design record `review/2026-10-03-exhaust/DESIGN.md`.

## Upstream changes

A `CHANGED VoronDesign/Voron-2` line from `sources_verify.py` means: compare `STLs/Exhaust_Filter/` across
the two commits, and re-fetch and rebuild B13-P1 and B13-P2 before printing if any of these files moved.
