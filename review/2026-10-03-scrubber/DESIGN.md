# Nozzle scrubber with sheet stops — design record (2026-10-03)

> **Superseded in part, 2026-10-03 (follow-up).** Nothing is printed ahead any more: Ch 13 Part L is now Steps 13.44–13.54 (inspect → measure → decide → print → fit), and `slicer/addons/scrubber-796563/remix.py` (reading the tracked `source/10mm Bed.stp`) is the only generator, deriving L and T from the measured H, w, d, G and O (rules in that folder's README). `remix_low.py` below was its prototype and is removed; `ch13-append.md` is the first draft of Part L. Geometry, sources and § 3/§ 4 analysis here still stand.

Add-on for the end of Ch 13: jinetix's "Voron 2.4 Silicone Nozzle Scrubber w/ Sheet Stops (Beacon / Carto
Compatible)", Printables 796563. Research only; no existing file was edited.

**Decision in one line:** print the 10 mm-bed set as a **low-profile remix** (wiper seat −1.5 mm, bucket
−2.0 mm), mirrored to the **left** bed extrusion, as an **add-on print outside the plate system** (38.3 g
black ASA, 2 h 30 m); hardware all from kit spares; buy only the Bambu A1 wiper (3-pack, $2.99). Fit as
Steps 13.44–13.50 in a new Part L; the macro clamps its circles to this build's ~4–5.5 mm reach past the plate.

## Folder

| File | What |
|---|---|
| `src/description.txt`, `src/print.json`, `src/comments.txt` | Printables page text (BOM, macros), metadata, all 100 comment lines (2026-10-03) |
| `src/10mm Bed Setup.3mf`, `src/10mm Bed.stp`, `src/8mm Bed Setup.3mf` | author's files (no STLs exist on the page) |
| `src/Voron 2.4 Decontaminator.stp` (25 MB), `src/MRW Kit*`, `src/img/*.jpeg` | full assembly incl. 10 mm LDO bed, MRW kinematic-bed variant, photos — gitignored (`.gitignore` here) |
| `src/leviathan-printer-rev-d-sbv2.cfg` | LDO config @667521d, for the section placement |
| `stl/jinetix_10mm_*.stl` | the 5 objects of `10mm Bed Setup.3mf`, print-oriented; `_MIRROR` = left-side copies |
| `stl/low/*.stl` | low-profile remix (recommended), from `remix_low.py --lower 1.5 --trim 2.0` |
| `remix_low.py` | cadquery remix from `src/10mm Bed.stp` (`venv-cq/bin/python remix_low.py --lower L --trim T`) |
| `scrubber.cfg` | Klipper block to paste (§ 4) |
| `test_macros.py` | renders the macros with Klipper's Jinja delimiters and a mock printer; asserts the G-code (PASS, below) |
| `ch13-append.md` | Steps 13.44–13.50 exactly as they would be appended (§ 6) |

Re-fetch: Printables GraphQL `getDownloadLink(id, printId:"796563", fileType:stl)`; file ids: `10mm Bed Setup.3mf`
5160570, `10mm Bed.stp` 5160571, `8mm Bed Setup.3mf` 5160556, assembly STEP 5159481, MRW 10 mm 6276608/6276609.
3MF/STEP files are listed under `stls`, so `fileType:stl` works for them. Comments: `comments(targetObjectId:796563,
targetType: print){ text created author{publicUsername} replies{...} }` (field is `text`).

## 0. Earlier-session facts, re-verified

| Claim | Verdict | Evidence |
|---|---|---|
| Printables 796563 by jinetix, CC BY-NC-SA | ✓ | `print.json`: user `jinetix`, licence "Attribution — Noncommercial — Share Alike"; published 2026-01-16; 331 likes, 18 makes |
| has 10 mm-bed and 350 files | ✓, as **one 3MF** | `10mm Bed Setup.3mf` holds 5 objects: 300/350/centre buckets, brush bracket ("Decontaminator"), stop bracket. Names from `10mm Bed.stp`, matched by volume |
| Bambu A1 wiper pad | ✓ | description l.12–18: official 8×37×3.85 mm, clone 8×37×4 mm (bristles ~0.2 mm taller) |
| 4× 6×3 mm magnets | ✓ | description BOM; STEP: 2 Ø6.2 pockets in the bracket (open downward, 3.16 deep) + 2 in the bucket (open upward, 2.64 deep), facing through ~1.1 mm of plastic |
| needs `[gcode_arcs]` | ✓ | description l.29–30 (`resolution: 0.1`) |
| ≥ 6–7 mm Y travel past the plate | ✓ as stated; **this build has ~4–5.5 mm** | description l.2, l.24 ("typical 10mm extra Y overtravel"); § 3a |
| kit brass brush used by 796563 | ✗ | 796563 uses only the silicone A1 wiper. The kit's `Brass Brush` is a hand tool (`hardware-ownership.yml` `unreconciled: tool`; `00-before-you-start.md` l.317, l.329) |
| MRW files | not for us | "MRW Kit" = parts for the MRW kinematic bed mount (assembly solids `MRW Kinematic Ball`, `MRW Wings`), ~16 mm taller |

Author's own text calls the macros `CLEAN_NOZZLE_PARK`/`CLEAN_NOZZLE` in "Macro Placement"; the cfg names are
`NOZZLE_PARK_BUCKET`/`NOZZLE_CLEAN` (description l.26 vs l.32, l.75).

## 1. Printed parts

LDO plate is **355×355×10 mm** (`ldo-350-bom.yml` l.793; Ch 03 l.3) → the **10 mm** set. Bed extrusions are
150 mm c-c (Ch 03 l.18), as in the author's CAD (±75 mm). Kit uses **no printed sheet stops**: the print plan lists
`Purge Bucket/brush_holder_sheet_stop` + `individual_sheet_stop` only as optional, unprinted (plan l.809–813);
`slicer/plates.py` has no sheet_stop/brush_holder entry. Nothing is replaced.

| Part (source object) | Qty | Recommended file | Size, mm | ASA spec mass / time |
|---|---|---|---|---|
| brush bracket ("Decontaminator") | 1 | `stl/low/brush_bracket_low1.5_MIRROR.stl` | 61.3×38.0×18.9 | 9.4 g / 40 m |
| stop bracket | 1 | `stl/jinetix_10mm_stop_bracket.stl` (symmetric, no mirror) | 20.0×38.0×17.5 | 4.6 g / 24 m |
| 350 mm bucket | 1 | `stl/low/350mm_bucket_trim2_MIRROR.stl` | 93.0×38.0×24.9 | 24.3 g / 1 h 31 m |
| **plate (3 parts)** | | | | **38.3 g / 2 h 30 m** |

Stock (un-remixed) set for comparison: 9.7 + 4.6 + 24.8 = 39.1 g, 2 h 34 m. Estimates: PrusaSlicer 2.9.6 CLI,
`slicer/voron-coreone-asa.ini` (4 perimeters, 40 % grid, 5/5, 0.2 mm, shrinkage comp 0 %, no support), parts
merged on one bed, not GUI-arranged. Orientation: as drawn, flat base down; **no supports** (author's 3MF:
`enable_support 0`, 4 walls, 40 %, 5/5, 0.2; author: "turn off shrinkage compensation"). Colour: Galaxy Black.
A blue-accent bucket would need its own plate; not worth it.

Remix (`remix_low.py`): bracket wiper seat floor 37.77 → 36.27 (posts moved down with it; seat-centre ray cast
17.77 → 16.27 in print frame); bucket top 41.39 → 39.39. Both re-slice clean. Licence: a CC BY-NC-SA derivative —
if committed to the public repo, ship with attribution + same licence (B11 precedent: `slicer/stl/bayducts/README.md`).

## 2. Hardware and purchases

| Item | Qty | Use | Source |
|---|---|---|---|
| M3×8 SHCS | 6 | 2 bolts per bracket (Ø3.2 through, Ø5.7 counterbore, 2.93 mm floor) + 1 upright sheet stop per bracket, self-tapped into a Ø3.0 bore | kit: ledger 207/283 after this |
| M3 roll-in T-nut | 4 | top slot of each bed extrusion behind the plate (holes on the slot centreline) | kit: 128/135 |
| 6×3 mm neodymium magnet | 4 | 2 bracket, 2 bucket | kit: 12/16 (Nevermore uses 8) |
| super glue | – | only if a magnet is loose | consumable (11.34 precedent) |
| **Heatbed Nozzle Wiper – A1/A2L** | 1 (3 in the box) | the brush | **buy**: Bambu Lab US store, $2.99, in stock 2026-10-03, "In the Box … ×3"; free shipping only over $59 |

Ledger numbers: `python3 scripts/parts.py --ledger` on a scratch copy with the draft spliced in. Sheet-stop length:
assembly SHCS solids are 11.0 mm overall (3 head + 8); the stop bracket's blind bore is ~11.4 mm deep, so M3×12
would bottom out. Author's BOM names no T-nuts; the brackets need them.

## 3. Mounting position and geometry

Frame: y0 = plate rear edge. Author's assembly: brackets' front faces butt the plate's rear edge; the wiper spans
y0 … y0+8 (bristle field ≈ y0+0.5 … y0+7.5); the bracket footprint runs y0 … y0+38.25 on the extrusion top.

**Side: left bed extrusion, mirrored** (brush and bucket outboard-left), stop bracket on the right extrusion. The LDO
nozzle probe is on the **right** extrusion's inner face (Step 09.30; LDO build-plate mapping); flicked ooze then lands
far from the pin. Machine-X estimate if the plate is centred on X175: left extrusion X 90–110; bristles ≈ X 51–87;
bucket X ≈ −3…90; bucket park X ≈ 41 `(verify on bench)`. Room behind the plate: frame 470, plate front 38 mm behind
the frame front (Ch 03 03.16) → rear edge at 393, rear rail inner face at 450 → 57 mm free vs 38.25 needed.

**(a) Y travel past the plate (O).** The nozzle reaches Y_max only where the nozzle-probe pin is: Step 13.24 slides the
probe until the Ø5 shaft is under the nozzle at the rear limit with a 2–3 mm gap to the plate (Voron p.161: 1.5 mm).
So O ≈ gap + 2.5 = **4.0–5.5 mm** (inference; stock configs in both LDO and Voron files are Y 350/350). The author's
default macro scrubs up to y0+6 and wants O ≥ 6–7. Users on 350 machines with reduced travel cut `brush_depth` to 2
or moved the plate forward 3–5 mm (comments: Mazvydas, dobromyslov). Our macro clamps: circle Y from y0+1.5 to
Y_max−0.5, radius = min(2, (O−2)/2); O 4.0 → r 1.0, 5.5 → r 1.75, < 3.5 → refuses. Optional upstream tweak: Step 13.24
could ask for the 3 mm end of its gap (O ≈ 5.5) when the add-on will be fitted.
Plate rear edge: the manual says the pin "stands in the plate's rear cut-out" (09.30). LDO's Rev C plate photo
(`03-build-plate/build_plate_bottom_view.jpg`) shows a straight cable edge; the "cut-out" seems to come from the
stepped outline of the schematic `ldo-build-plate-mapping.png`. If the 350 plate really is notched at the pin, O at
the brush X could be ≤ 0 and the add-on cannot work: Step 13.44 measures O at the brush X first.

**(b) Brush height vs the Omron.** Heights above the build surface, author's 10 mm assembly (extrusion top z 20,
plate on 7.8 mm thumb nuts, 1.5 mm magnet sheet, 0.75 mm flex plate → sheet top z 40.05, i.e. 20.05 mm above the
extrusion):

| Feature | Stock | Low remix |
|---|---|---|
| wiper top (official / clone) | +1.55 / +1.75 | +0.05 / +0.25 |
| bucket rear and end walls | +1.34 | −0.66 |
| bucket front lip, bracket top | −1.1…−1.3, −1.20 | same |
| sheet-stop heads | +0.42 | +0.42 |

Omron TL-Q5MC2: footprint 17×17 mm (CAD index), centre 25 mm behind the nozzle (`[probe] y_offset: 25.0`, Ch 12
12.29). Let d = Omron face height above the nozzle tip (`z_offset: 0`; Ch 12/13 give no value, Voron docs give no
target — **measure it**, Step 13.44). Requirements with 0.3 mm margin, first layer at Z 0.2, scrub 0.5 mm into the
bristles, no flick dip:

| Situation | Stock needs | Low needs |
|---|---|---|
| printing in the rear 33.5 mm of the plate within ±8.5 mm of the brush X: Omron over the wiper | d ≥ 1.65 (1.85 clone) | d ≥ 0.15 |
| printing near the rear at either extrusion X: Omron over a sheet-stop head | d ≥ 0.52 | d ≥ 0.52 |
| scrubbing (Z = wiper top − 0.5): Omron over the bucket rear wall | d ≥ 0.59 | d ≥ 0.09 |
| **governing** | **d ≥ 1.65** | **d ≥ 0.52** |

Every row shifts by −Δ, Δ = (our extrusion-top-to-sheet-top) − 20.05; Steps 13.44/13.47 measure the real heights
directly, so Δ is never needed as a number. The low remix scrubs at Z ≈ −0.45 behind the plate (Klipper
`[stepper_z] position_min: -5`, Ch 12 12.25), so the macro keeps the circle's front ≥ y0+1.5 and drops Z only over
the bucket. Flick path over the bracket/bucket lip: Z −0.45 vs −1.1…−1.3 → ≥ 0.65 mm.

**(c) Collisions at the bed rear.**
- Nozzle-probe body/collar (right extrusion inner face): Voron CAD puts the Ø16 collar 1.5 mm inboard of the inner
  face and ~5 mm above the extrusion top; the stop bracket overhangs the inner face by 0.23 mm, its Y range covers
  the collar. ~1.3 mm clearance in the Voron geometry; LDO's thicker body unknown → bench check, fallback: no stop
  bracket.
- Sheet-stop heads: centre y0+2.3, Ø5.5 → head front 0.45 mm over the plate edge line, head underside 0.33 mm below
  the plate top in the author's CAD; the head bears on the plate's rear arris/magnet-pad edge. Bench check; if it
  fouls, set the bracket 0.5 mm back.
- Bed WAGO mount: left extrusion **inner side** slot under the plate (Step 09.34), not on the top behind it. Bed leads
  exit the rear edge centre-left: keep them dressed inboard of the left extrusion.
- Nevermore plenum: inner faces between the extrusions (11.38); brackets use the top slot. No conflict.
- Rear frame / Z rails: bucket ends ~19 mm in front of the rear rail; Z rails sit on the rear vertical extrusions.

## 4. Klipper

Author's macros verbatim: `src/description.txt` l.29–30 (`[gcode_arcs]`), l.32–72 (`NOZZLE_PARK_BUCKET`),
l.75–175 (`NOZZLE_CLEAN`; l.175 runs into the closing prose, an HTML-strip artefact), revision 2025-12-22. Adapted block: **`scrubber.cfg`** (paste whole). Changes: one
`_SCRUB` variable block (the author duplicates the brush reference in both macros); bucket side left; Y clamp to
`printer.toolhead.axis_maximum.y` (§ 3a); lift → XY → drop over the bucket (the author's Z-then-XY order drags at
scrub height; comment by Locki 2026-04-06); no flick Z-dip; raises an error until measured or if not homed.

Variables to fill, all `(verify on bench)`, measured at Steps 13.44/13.47: `brush_x_min`, `brush_x_max` (bristle
edges, nozzle X), `edge_y` (nozzle tip over the plate's rear edge, at the brush X), `z_scrub` (Z where paper drags on
the bristle tops, minus 0.5). Nothing else is machine-specific.

Where in printer.cfg: after `[gcode_macro PRINT_END]` (LDO cfg l.629), before `[gcode_macro CHOME]`; above the
`SAVE_CONFIG` block in any case. The manual instruction lives in Ch 13 (Step 13.48), not Ch 12: Ch 12 runs before the
parts exist. Ch 12 Step 12.36 can carry a one-line forward note (non-step text).

PRINT_START (Ch 12 12.36 skeleton) insert after `QUAD_GANTRY_LEVEL`, above the existing `G28 Z`:

```ini
    G28 Z                                  ; provisional Z0 after QGL, tip not yet clean
    NOZZLE_PARK_BUCKET
    NOZZLE_CLEAN
```

Why two Z homes: after QGL the Z coordinate is off by the gantry correction until re-homed, so scrubbing at Z −0.45
needs a provisional home; the final `G28 Z` then touches the nozzle-probe pin with a clean tip (the point of the
add-on on a nozzle-probe Z0). The scrub runs at the QGL temperature (150 °C, `M104 S150` before QGL). ~+1 min.

Test (`../../.venv/bin/python test_macros.py`, exit 0): placeholders refused; unhomed refused; for O = 6.5/5.5/4.5/
4.0/3.5 the circles stay in y0+1.5 … Y_max−0.5 (r 2.00/1.75/1.25/1.00/0.75) and inside the bristle X span; Z drops
on its own line; ends at Z5; O = 2.8 refused; the park macro lifts before moving. Not run on real Klipper; the
`G2/G3` full circle (end = start, `I` only) is the author's own construct.

## 5. Which plate/batch

**Recommended: an add-on print outside the plate system.** Commit the three STLs (+ README with attribution and
CC BY-NC-SA) under e.g. `slicer/stl/addons/scrubber-796563/`; print them in one go on the Core One+ with
`slicer/voron-coreone-asa.ini` on the smooth sheet, any time after B10 (or after kit day; the parts are not on
anyone's critical path). The 22 plates, B11, every run total and `check_docs.py` stay untouched. Ch 13 lists them
as `… ×1 — from the scrubber add-on print` (parts grammar `— from`); no backticked STL names, so lint check 3
(STL in no batch) does not apply. Black spare is ~587 g (plan); 38 g fits.

**B12 (B11 precedent) costs too much for 38 g.** B11 (061dfd5, 100+ files) hard-codes itself in: `slicer/plates.py`
(`run=`, entries), `build_plates.py` (`TOTAL_LABEL`, ini map), `estimates.csv` (`TOTAL B11` row), `check_docs.py`
§ 8 (page, README, plan §3/§9, 00-index regexes, diagram 11), `build_printables.py` (`_BATCH_PRINT_ORDER`, schedules,
ledgers), `build_tonight.py` (`whole("B11")`), `docs/javascripts/boards.js`, `draw_diagrams.py`, `bins.py` (new bin),
part thumbnails + `MANIFEST.csv`, plate 3MF/PNG/SVG, a print page, README tables, nav. A B12 needs each generalised to
"batches outside the run" first. Only worth it if Alex wants the scrubber on the plate board / Tonight.

## 6. Ch 13 steps

Full text: **`ch13-append.md`** (Part L, Steps 13.44–13.50). Verified on a scratch copy of the repo with the text
spliced in after 13.43 and the Hardware rows below: `lint_manual.py --budgets` 0 findings (raw-callout check
skipped, no mkdocs build per brief), `--strict-parts --chapters 13` 0/0, `hooks/mascot.py --self-test` passed,
`build_tonight.py --self-test` OK.

| Step | Title | Power / heat | Helper |
|---|---|---|---|
| 13.44 | Measure the probe height and the reach past the plate (gate: d ≥ 0.6, O ≥ 3.5) | on, cold | yes |
| 13.45 | Press the magnets and seat the wiper | bench | yes |
| 13.46 | Bolt both brackets to the bed extrusions (+ Pause ~25 min) | on, cold, toolhead parked | yes |
| 13.47 | Read the brush coordinates off the machine | on, cold | yes |
| 13.48 | Add the scrubber macros | on | – |
| 13.49 | Dry-run the scrub cold | on, cold | yes |
| 13.50 | Scrub inside `PRINT_START`, then shut down (+ Pause ~30 min) | **hot** → add `13.50` to `NO_MASCOT_STEPS["hot"]`; no Helper | – |

Placement: after Step 13.43's `---`, before `## What if`; Checkpoint 13, Common mistakes and `## Next` stay below.
Step 13.43 shuts the machine down, so 13.44 powers it on again; 13.50 ends with the commit + shutdown.

Other edits the orchestrator owns (non-step text): Ch 13 header — Time +~1 h, Sessions 11 → 13, Printed parts table
gets a non-backticked add-on row, Hardware table replaces "— none —" with `M3×8 SHCS | 6`, `M3 roll-in T-nut | 4`,
`6×3 mm neodymium magnet | 4`; optional Checkpoint 13 line "scrubber fitted, dry-run clean (if fitted)"; 00-index
Ch 13 hours → re-run `python3 scripts/draw_diagrams.py --only 11`; the chapter scope/intro sentence; the
`00-tonight.md` regeneration that the build does.

## 7. Open risks / bench items

1. **O at the brush X** (13.44): 4.0–5.5 mm expected, ≥ 3.5 required; a notched LDO plate edge would end the add-on.
2. **d, Omron face above the nozzle tip** (13.44): ≥ 0.6 mm for the low set; the stock set needs ≥ 1.7 mm.
3. Right bracket vs the LDO nozzle-probe collar/body (13.46); fallback: run without the stop bracket.
4. Sheet-stop heads vs the plate's rear arris and the magnet pad edge (0.45 mm overlap in the author's CAD).
5. Magnet press fit in Ø6.2 pockets (author's own profile carries `filament_shrink 99.3%` despite telling users to
   turn compensation off; one maker opened the holes 0.05 mm). Glue fallback.
6. Scrub quality at 150 °C on ASA; if strings survive, scrub at 170–180 °C then wait back to 150 before `G28 Z`
   (dobromyslov's two-temperature sequence).
7. Kit magnet count: 16 shipped, 8 Nevermore + 4 here = 12; a later Klicky build would need its own.
8. Bed leads and WAGO mount clear of the left extrusion top behind the plate.
9. Clone wiper is ~0.2 mm taller; 13.47 measures the real top, so only the d margin moves.
10. A loaded bed mesh extrapolates its edge value behind the plate if `NOZZLE_CLEAN` is run by hand mid-session
    (PRINT_START clears the mesh first).

## Side findings (outside this task, not acted on)

- Ch 13 What-if rows "Probe triggers too early … Probe mounted too high … Lower the probe" and "too late … too low …
  Raise it" look inverted: a lower Omron face triggers earlier (larger gap). Check before Ch 13 is used.
- Step 09.30 / 09 Checkpoint "pin in the plate's rear cut-out": no cut-out is visible on LDO's plate photo (§ 3a).
