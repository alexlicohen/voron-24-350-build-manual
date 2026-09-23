# bayducts — STLs for batch B11 (bay ducting, layout v3)

Print page: `docs/manual/print/B11-bay-ducting.md`. Plates: `slicer/plates.py` (B11-P1…P5).

## Licence and credit

GPL-3.0. Every file here is, or is derived from:

- **MyStoopidStuff**, *Remix of RyanDam's Cable Management Duct for Voron Printers, Version 3.2*,
  <https://www.printables.com/model/502306> (GPL 3.0), itself a remix of
- **RyanDam**, *Cable Management Duct* for Voron printers.

The files under `remix/` are **remixed for the LDO Rev D+ bay** (Voron 2.4 R2 350) in this repo,
2026-09-23, and are distributed under the same GPL-3.0 terms. The scripts that made them are in
`review/2026-09-23-bay-mods/layout-v2/work/remix.py` and `layout-v3/work/remix_v3.py`; the GPL
text is at <https://www.gnu.org/licenses/gpl-3.0.html>.

## Layout

| Folder | What | In git? | How it gets here |
|---|---|---|---|
| `mss/502306/` | MSS stock pieces, byte-for-byte | no (gitignored) | `python3 slicer/fetch_stls.py`, by Printables file id (`slicer/plates.py` `PRINTABLES`) |
| `remix/` | the V2L_* / V3L_* remixes | yes | committed; `fetch_stls.py` only hashes them |

`slicer/stl/MANIFEST.sha256` pins both. `python3 slicer/fetch_stls.py --verify` fails if a file here
differs from it.

Four `mss/502306/` files are on no plate: `CMD_V3_1H_T_REG` and `CMD_V3_1H_82mm_DUCT` (+ covers) are
the fallback middle joints if the Leviathan-to-PSU gap measures under 25 mm; `CMD_V3_1H_142mm_DUCT`
(+ cover) and `CMD_V3_1H_WIRE_BOX` are parents the remix scripts cut custom lengths from.

## What each remix is

| File | From | Change |
|---|---|---|
| `V3L_COUPON_22N_DUCT` + `_COVER` | v2's 22 mm straight | narrowed 2.4 mm like the 154N; lid-snap test coupon |
| `V3L_154N_DUCT` + `_COVER` | `CMD_V3_1H_154mm_DUCT` | slice-and-shift Δ2.4 mm: 22.0 mm outer, walls/tines/snap unchanged |
| `V3L_T_REG_N` + `_COVER` | `CMD_V3_1H_T_REG` | stem narrowed by the same cut; bar 81.6 mm |
| `V3L_10mm_DUCT` + `_COVER` | `CMD_V3_1H_82mm_DUCT` | shortened to 10 mm |
| `V3L_34mm_DUCT_HOLE`, `V3L_34mm_DUCT_COVER` | `CMD_V3_1H_82mm_DUCT` | 34 mm, 17 × 16 mm floor opening over the bed-lead hole |
| `V3L_90DEG_R15` + `_COVER` | `CMD_V3_1H_90DEG` | arc only, re-radiused R22 → R15.5 |
| `V3L_WIRE_BOX_PORT` | `CMD_V3_1H_WIRE_BOX` | original size, 4 pinched edges repaired, one 18 mm port in the front wall |
| `V2L_90DEG_MIRROR`, `V2L_90DEG_COVER_MIRROR` | `CMD_V3_1H_90DEG` + cover | mirrored |
| `V2L_58mm_DUCT`, `V2L_130mm_DUCT`, `V2L_70mm_DUCT` (+ covers) | 154 / 142 / 82 mm ducts | shortened |
| `V2L_STRIP_FIN` | new | divider fin between PSU −V and FG |
