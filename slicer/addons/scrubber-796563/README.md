# Nozzle scrubber with sheet stops — add-on (Ch 13 Part L)

Optional. On no plate, in no batch (B00–B11), in no run total. **Printed only after Ch 13 Step 13.47 has
decided the parts from this machine's measurements — never ahead of kit day, never from the files below
without that decision.**

## Licence and credit

**CC BY-NC-SA 4.0** (<https://creativecommons.org/licenses/by-nc-sa/4.0/>). Derived from **jinetix**,
*Voron 2.4 Silicone Nozzle Scrubber w/ Sheet Stops (Beacon / Carto Compatible)*,
<https://www.printables.com/model/796563> (CC BY-NC-SA). `source/10mm Bed.stp` is the author's file,
unchanged (Printables file id 5160571, 308 070 bytes, sha256
`64c88c0a3bc9dda1bc6bcfc9f958f10b1b4e32f413ab20ecb1c58e22a790fb9c`). The macros in Ch 13 Step 13.52 are
adapted from the same page (macro revision 2025-12-22). Every file `remix.py` writes is a derivative under
the same licence.

## How the parts are made

`remix.py` is the only generator. It reads `source/10mm Bed.stp`, mirrors the parts for the left bed
extrusion, lowers the A1-wiper seat by **L** and trims the 350 mm bucket by **T**:

| Step | What | Where |
|---|---|---|
| 13.44 | plate rear edge straight at the brush; bare top on both bed extrusions (≥ 39 mm); probe collar clear of the right one | steel rule, machine off |
| 13.45 | **H** flex-plate top above the bed-extrusion top; **w** wiper height | caliper, machine off |
| 13.46 | **d** Omron face above the nozzle tip; **G** Omron face above the extrusion top at Z0; **O** reach past the plate edge | caliper + homed machine |
| 13.47 | calculator (layout rows), then `venv-cq/bin/python slicer/addons/scrubber-796563/remix.py --H … --w … --d … --G … --O …` | laptop |
| 13.48 | print what it wrote to `measured/` (gitignored) | Core One+ |

Decision (heights above the bed-extrusion top; 0.3 mm margin; first layer at Z 0.2; scrub 0.5 mm into
the bristles; S 17.77 seat floor, F 18.85 bracket top, K 20.47 sheet-stop head top, B 21.39 bucket wall,
all read from the STEP and asserted by `remix.py`):

| Quantity | Rule | Why |
|---|---|---|
| L | ≥ S + w + 0.1 − G | the Omron clears the wiper while the plate's rear rows print |
| L | ≤ w − 1.88 | the nozzle at scrub height clears the bracket top on the flick path |
| T | ≥ B + 0.1 − G | the Omron clears the bucket walls while the rear rows print |
| T | ≥ B − S + 0.8 + L − w − d | the Omron clears the bucket walls while the nozzle scrubs |
| sheet-stop screws | fit only if G ≥ K + 0.1 and H ≤ 21.0 | Omron clears the heads; the heads reach the flex plate's edge |
| no-go | O < 3.5, G < 19.75, \|G − (H + d)\| > 0.3 | no reach; no L satisfies both L rows; inconsistent measurements |

L and T round up to 0.5 mm (0 = stock). The printout also gives the two inspection readings for Step
13.49 (bracket base to bristle tips, bucket height) and the expected `z_scrub` for Step 13.51.

## Files here

The committed STLs are the generator's **default**, `remix.py --defaults`, for the expected numbers
(H 20.05 from the author's LDO 10 mm assembly, official wiper w 3.85, d 0.6, O 4.5): L 1.5, T 1.5, sheet
stops fitted. They exist so the pipeline and the print estimate can be checked; print them only if the
Step 13.47 printout names exactly these files.

| File | Change from the author's part | Qty |
|---|---|---:|
| `brush_bracket_L1.5_MIRROR.stl` | mirrored; wiper seat and its posts lowered 1.5 mm | 1 |
| `bucket350_T1.5_MIRROR.stl` | mirrored; top trimmed 1.5 mm | 1 |
| `stop_bracket.stl` | none (symmetric) | 1 |

## Print

One job on the Core One+, smooth sheet, `slicer/voron-coreone-asa.ini` (Voron spec: 4 walls, 5 top/bottom,
40 % grid, 0.2 mm), Galaxy Black ASA, as oriented, **no supports**. Default set, PrusaSlicer 2.9.6 CLI
estimate: **38.5 g, 2 h 30 m**. Bin with Ch 13.

## Upstream changes

`sources.yml` pins the Printables page (`printables-796563-nozzle-scrubber`): file ids and sizes, and a
hash of the macro text. A `CHANGED` line from `python3 scripts/sources_verify.py` means: download the new
`10mm Bed.stp`, diff it against `source/`, re-run `remix.py --defaults` and the measured set, and re-diff
the page's macros against Ch 13 Step 13.52's block before printing anything.
