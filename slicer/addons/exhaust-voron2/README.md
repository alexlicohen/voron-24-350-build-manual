# Chamber exhaust housing — add-on (Ch 14 Part H)

Optional. On no plate, in no batch (B00–B11), in no run total. **Printed only after Ch 14 Step 14.25 has
checked the back of the real machine** (stock notch, free depth behind it, extrusion slot, lead route,
spare jumper); never ahead of kit day. Step 14.25 opens Ch 14, so both jobs print while the Voron runs Parts A–G.

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

Two jobs on the Core One+, satin sheet, no glue, as oriented, **no supports**, the inis' Voron settings (4 walls,
5 top/bottom, 40 % gyroid, 0.2 mm). **3 mm brim on the two large flat parts**, the housing (143.7 × 154.8 mm
footprint) and the access cover (73.2 × 134.8 mm), set per object (right-click → Add settings → Skirt and brim →
Brim width), as `docs/manual/print/00-slicer-setup.md` § Orientation & brim does for the 155 mm grill. The inis
keep the global brim at 0 and `brim_separation` at 0.15; the fan grill and the two mounts print without one.

| Job | Profile | PrusaSlicer 2.9.6 CLI estimate |
|---|---|---|
| 1 — housing, 3 mm brim | `slicer/voron-coreone-asa.ini`, Galaxy Black ASA | 66.1 g, 4 h 31 m |
| 2 — fan grill, access cover with a 3 mm brim, 2 mounts | `slicer/voron-accent-blue.ini`, blue accent ASA | 34.8 g, 1 h 54 m |

Estimates are normal-mode, re-sliced 2026-10-30 with the current inis (Z +0.08, 95 % first-layer flow, the
10-29 speeds), the parts laid side by side, not GUI-arranged. The CLI sets a brim per job, so job 2 is the
three parts sliced bare (34.5 g, 1 h 52 m) plus the cover's brim from its own slice (+0.24 g, +1.6 min); the
housing's brim costs 0.27 g and 2 min. All five
pieces go in bin `14-exhaust` (`slicer/bins.py` `ADDON_PARTS`); `exhaust_filter_grill` stays in `11-finish`,
where B09 sorted it, since it is fitted at Step 11.54 and reused in place at Step 14.29.

## Hardware (all kit spares except the purchase)

8 × M3×5×4 heat-set insert, 4 × M3×30 SHCS (fan and grill), 2 × M3×8 SHCS (access cover), VHB tape; the
mounts reuse the exhaust cover's 2 × M5 roll-in T-nut and 2 × M5×10 BHCS (Ch 11 Step 11.55), and the two
M3×12 SHCS and the PTFE coupler come off the cover too. Bought (Ch 00
Step 00.8): a 60×60×20 mm 24 V fan, a 1 m JST-XH 2-pin extension, carbon filter mat. Counts from the Voron
2.4r2 assembly CAD and manual p.250–256; design record `review/2026-10-03-exhaust/DESIGN.md`.

## Upstream changes

A `CHANGED VoronDesign/Voron-2` line from `sources_verify.py` means: compare `STLs/Exhaust_Filter/` across
the two commits, and re-fetch and re-slice before printing if any of these files moved.
