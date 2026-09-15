# Batch B00 — Calibration & jigs

One plate: the dimensional gate for the whole build, plus the rail-alignment jigs and the pulley jig. The
gate is in two parts — **Gate A** (the cube) releases B02, B07 and the cosmetics B08–B10 the day this plate
comes off; **Gate B** releases B01 and B03–B06 and runs in the same week, on a caliper across the printed
bore and seven M3×H5 inserts out of the KADRICK kit already on the bench `(verify on bench)`. Gate B's
**bearing press** and its **MGN12 rail row** wait for the kit; nothing is bought to bring them forward.

```mascot
pose: gather
caption: Jigs and a gate cube. Nothing else prints until this plate measures right.
```

**Time:** 4.0 h (1 plate) — PrusaSlicer 2.9.6 estimate, sliced from `slicer/plates/B00-P1.3mf`.

**Sessions:** ~15 min one-time slicer and filament setup, then 1 plate start (~5 min hands-on, then 4.0 h unattended) + ~15 min for Gate A + ~10 min sorting + ~15 min for Gate B, of which ~10 min (the bearing press and the rail row) waits for kit day.

**Prerequisites:** the Gen 2 belt upgrade (index row 1) done, or the 2026-10-15 contingency taken — see
**Gen 2 first**, below. Slicer set up per [00-slicer-setup.md](00-slicer-setup.md) (Step B00.0 below walks
the one-time wizard).

**Printed parts**


| STL | Repo path | Qty | Colour | g ea | Bin |
|---|---|---:|---|---:|---|
| `Voron_Design_Cube_v7.stl` | Voron-2 `STLs/Test_Prints/` | 1 | Black | 16.2 | 00-jigs |
| `Heatset_Practice.stl` | Voron-2 `STLs/Test_Prints/` | 1 | Black | 6.5 | 00-jigs |
| `MGN12_rail_guide_x2.stl` | Voron-2 `STLs/Tools/` | 2 | Black | 3.2 | 00-jigs |
| `MGN9_rail_guide_x2.stl` | Voron-2 `STLs/Tools/` | 2 | Black | 2.7 | 00-jigs |
| `pulley_jig.stl` | Voron-2 `STLs/Tools/` | 1 | Black | 2.8 | 00-jigs |
| `z_drive_retainer_a_x2.stl` | Voron-2 `STLs/Z_Drive/` | 1 *(of the 2 needed — this is the bearing-fit coupon and a real part)* | Black | 19.5 | 02-Z0 |

**Hardware:** none printed here. Gate B (Step B00.7) needs seven M3×H5 [heat-set inserts](../16-glossary.md#h)
(the coupon has seven pockets), which come from the KADRICK kit already on the bench (Ch 00 Step 00.9), plus
a [625-2RS](../16-glossary.md#f) bearing and an MGN12 rail, which only the Voron kit supplies. So the insert
row and the caliper row run months before the kit; the bearing press and the rail slide run on kit day, and
the kit's own 153 inserts stay untouched.

**Read first**

- The two-part gate in [00-slicer-setup.md](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade).
  **Gate A** (cube X/Y, Z, first-layer-vs-mid delta, corner snap) is Step B00.5 and releases B02, B07 and
  B08–B10. **Gate B** (`Heatset_Practice` with real inserts and a caliper across `z_drive_retainer_a`'s
  625-2RS pocket now; the bearing press and `MGN12_rail_guide` on a real rail on kit day) is Step B00.7 and
  releases B01 and B03–B06.
- **A failed gate means reprints, and a reprint is marked**: the new plate id with an **R** after it and
  the changed extrusion multiplier, on a hidden face, per [README § Bins](README.md#bins). Gate A and Gate B
  are the two places this build expects to reprint, so it is where the habit starts.
- Most commonly reprinted here: the cube, until the profile is right.
- `z_drive_retainer_a` on this plate is deliberate — it's your bearing-press-fit coupon **and** one of the two
  you need for B01, so nothing is wasted.
- First layer: the Core One+ has no first-layer wizard. The loadcell sets Z before every print; you judge the
  result (Step B00.4) and nudge with Live Adjust Z only if you must.

## Gen 2 first

Before any plate: fit the Gen 1→Gen 2 kit (Prusa order 1787919456) per
[the Prusa guide](https://help.prusa3d.com/manual/prusa-core-one-to-gen-2-upgrade_2435). It changes belts,
pulleys, steps/mm and firmware together, so it is done once, up front, and every one of the 22 plates is
printed on GT1.5. The Voron kit is not what you are waiting for here — the upgrade kit arrives months
earlier.

- [ ] Firmware **≥ 6.8.1** (printer menu → Info)
- [ ] **Settings → Hardware → Edition = Gen 2**
- [ ] GT1.5 belts fitted and tuned (Control → Calibrations & Tests → Belt Tuning)
- [ ] Gantry re-squared
- [ ] Self-test passed
- [ ] Input shaper: the Edition switch loads the Gen 2 defaults; no calibration without the optional accelerometer
- [ ] Printer box reads `Prusa CORE One HF0.4 nozzle (modified)` after opening a plate

Then Step B00.0. If the upgrade kit has still not arrived by **2026-10-15**, take the contingency instead:
start B00 on the Gen 1 belts and take the mid-run pause after B07, per
[00-slicer-setup](00-slicer-setup.md#gen-2-belt-upgrade-the-first-job-contingency-pause-below).

## Steps

## Step B00.0 — One-time PrusaSlicer setup

**Do:**

1. PrusaSlicer 2.9.6, **Configuration → Configuration Wizard**: **Prusa FFF**, **Prusa CORE One & CORE One+**.
2. Tick the **0.4 HF** nozzle even with plain 0.4 ticked; filament **Prusament ASA**; Finish.
3. **File → Open Project**: `slicer/plates/B00-P1.3mf`; accept any profile dialog.

**Check:** All three preset boxes read `(modified)`: `Prusa CORE One HF0.4 nozzle (modified)`, `0.20mm STRUCTURAL @COREONE 0.4 (modified)`, `Prusament ASA @COREONE HF0.4 - Voron black`.

⚠ The printer box's `(modified)` is the **cold-probe start G-code**, baked into all 22 projects. Leave it: never reset that box to its system value, and never pick the `- coldstart` preset first, because the project already carries the identical block.

⚠ The project did **not** load if any box lacks `(modified)`, the filament box reads bare `Prusament ASA @COREONE HF0.4`, the estimate at Step B00.2 is wrong, or the printer box names another printer.

Source: [00-slicer-setup § One-time PrusaSlicer setup](00-slicer-setup.md#one-time-prusaslicer-setup-before-the-first-project) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [PrusaSlicer releases](https://github.com/prusa3d/PrusaSlicer/releases)

## Step B00.1 — Filament prep

**Do:**

1. Mount a fresh or recently-dried spool of Prusament ASA Galaxy Black, ≤2 weeks open.
2. On the printer, **Load Filament → ASA**; it asks for a material type only, and the HF profile lives in the slicer.
**Check:** Purge is clean black, no PLA/PETG streaking from a prior print.

Pause: ~15 min since the last pause — wizard run with the 0.4 HF nozzle, B00-P1 open and showing "(modified)" / " - Voron black", ASA loaded and purged clean. Nothing printing.

Source: [print plan §4.3 — spool changes](../../voron-print-plan.md#43-spool-changes) · [00-slicer-setup § Drying](00-slicer-setup.md#drying) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B00.2 — Load plate B00-P1

![Plate B00-P1 — sorting diagram](../assets/plates/B00-P1.png)

*Sorting diagram, drawn from the committed project: every part numbered and filled in the colour of its bin, bin id on the part; the legend reads # · STL · bin (chapter · steps). Sort at Step B00.6.*

**Do:**

1. **File → Open Project**: `slicer/plates/B00-P1.3mf`. Open it, never rebuild it.
2. Confirm **6 files, 8 objects** on the bed and no [brim](../16-glossary.md#b).
3. Do not change which face a part sits on; rotating about Z is fine.

**Parts:** 6 files, 8 objects — 4.0 h, 52 g (PrusaSlicer 2.9.6 estimate); `Voron_Design_Cube_v7`; `Heatset_Practice`; `MGN12_rail_guide_x2` ×2; `MGN9_rail_guide_x2` ×2; `pulley_jig`; `z_drive_retainer_a_x2` ×1.
**Check:** The slicer reads **3 h 58 m / 51.7 g**, and the filament preset shows shrinkage compensation XY and Z at 0 %.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [Voron materials — shrinkage 100 %](https://docs.vorondesign.com/materials.html)

## Step B00.3 — Pre-print checks

**Do:**

1. Fit [the print sheet](00-slicer-setup.md#print-sheet), cleaned since the last print, with a thin glue-stick film over the printed area.
2. Confirm the chamber reaches 40 °C minimum before the print starts; the ASA profile gates this, do not override.
**Check:** Chamber temp reads ≥40 °C on the display before the nozzle purges.

⚠ ASA off-gasses styrene. Advanced Filtration Kit fitted, door shut for the whole print, room ventilated
between plates. The bed (110 °C) and nozzle (265 °C) stay hot for ~20 min after the print ends — a helper
handles cooled parts, not the printer.

Tip: on the smooth or powder-coated PEI sheet Prusa prints ASA over a glue-stick layer so the part cannot pull the coating off; never acetone on the powder-coated sheet. [help.prusa3d.com/article/asa_1809](https://help.prusa3d.com/article/asa_1809)

Source: [00-slicer-setup § Print sheet](00-slicer-setup.md#print-sheet) · [00-slicer-setup § Calibration sequence](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B00.4 — Print

**Do:**

1. Slice, then Export G-code to the USB stick or Send to printer.
2. Start it, watch the first layer 2 to 3 minutes.
3. Gappy beads: long-press the knob, nudge **Live Adjust Z**, then find the cause before B02.

**Check:** First layer smooth, no gaps between beads, no ridging, and either no Live Adjust Z nudge or its cause written in the log.

Tip: expect 15–25 minutes of chamber heating before the purge (verify on bench). The 4.0 h estimate does not include it.

Source: [00-slicer-setup § Calibration sequence, item 3](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) · [Prusa KB — Live Adjust Z](https://help.prusa3d.com/article/live-adjust-z_112427) · [Ellis — first layer squish](https://ellis3dp.com/Print-Tuning-Guide/articles/first_layer_squish.html) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B00.5 — Inspect: Gate A (the cube, no kit needed)

**Do:**

1. Once cool, remove the plate and run [**Gate A**](00-slicer-setup.md#gate-a-no-kit-needed-the-cube) with calipers at mid-height.
2. Cube X/Y 30.00 mm ±0.15 mm, Z 30.00 mm ±0.10 mm, first-layer-vs-mid-height X delta ≤0.15 mm, corner snap no delamination.
3. Log all four numbers.

**Check:** All four pass; any failure means adjusting [extrusion multiplier](../16-glossary.md#e), never negative XY compensation, then reprinting this plate before B02 or B07.

```gate-calc
id: gate-a
title: Gate A — the 30 mm cube
inputs:
  - key: x
    label: Cube X, at mid height (mm)
    nominal: 30.00
    tol: 0.15
    low: Under. Confirm shrinkage compensation is 0 % and XY compensation is 0, then raise the extrusion multiplier in 1 % steps and reprint the plate. Never dial in positive XY compensation.
    high: Over. Confirm shrinkage compensation is 0 % and XY compensation is 0, then reduce the extrusion multiplier in 1 % steps and reprint the plate. Never dial in negative XY compensation, it wrecks every bearing fit.
    why: Every bearing bore and screw hole in the machine inherits this number, and the only lever that fixes it is extrusion multiplier, because negative XY compensation buys the cube back and wrecks every fit behind it.
  - key: y
    label: Cube Y, at mid height (mm)
    nominal: 30.00
    tol: 0.15
    low: Under, same lever as X. Shrinkage and XY compensation at zero first, then extrusion multiplier up 1 %. A persistent X to Y difference on one cube is a gantry-square problem, not flow.
    high: Over, same lever as X. Shrinkage and XY compensation at zero first, then extrusion multiplier down 1 %. A persistent X to Y difference on one cube is a gantry-square problem, not flow.
    why: Y on its own says little, but Y against X separates a flow error, which moves both, from a squareness error on the Prusa, which moves one.
  - key: z
    label: Cube Z (mm)
    nominal: 30.00
    tol: 0.10
    low: Under means the first layer is over-squished. Nudge Live Adjust Z up on the next print, then fix the cause, a sheet not seated, debris under it, an uneven glue film or a nozzle not fully seated.
    high: Over means the first layer is under-squished. Nudge Live Adjust Z down on the next print, then fix the cause rather than nudging every plate, because the Core One+ does not save the nudge.
    why: Z is the first layer's report card, and the Core One+ has no first-layer wizard and does not remember a Live Adjust Z nudge, so an out-of-range Z is a cause to find before the next plate rather than a number to dial in.
  - key: fl
    label: First layer vs mid height, X difference (mm)
    max: 0.15
    high: Elephant-foot compensation is wrong. Adjust it in 0.05 mm steps and reprint. This is a first-layer artefact, so leave the extrusion multiplier alone.
    why: The first layer is always squashed, so measuring it against mid height is what separates a wrong elephant-foot compensation from a flow error and keeps you from moving the multiplier for something it did not cause.
  - key: snap
    label: Corner snap tears across the layers, not along one
    kind: yesno
    no: Delamination. The chamber is too cold or the part fan is too high. Drop min/max fan to 0/15 %, hold the 40 °C chamber gate, and reprint before any structural plate.
    why: Every Voron part is printed in this same ASA, and a cube that peels along a layer line is a chamber or fan setting that would repeat on every plate after this one.
pass: Gate A passed. B02, B07 and the cosmetics B08 to B10 are released. Write the four numbers in the log, then run Gate B in the same week before B01 and B03 to B06.
```

The 30 mm cube is a ruler for the printer. X and Y say whether walls come out the size the CAD drew, which
every bearing bore in the machine depends on; Z says whether the first layer is squished right; the corner
snap says whether the layers weld. Every later plate inherits these four numbers.

Tip: corner snap means grip a corner in pliers and bend it off. A pass tears across the layers; a peel along one layer line is a fail.

Pause: ~15 min since the last pause — Gate A is measured and written down; B02 and B07 are released. The Gate B coupons (`Heatset_Practice`, one `MGN12_rail_guide`, `z_drive_retainer_a`) are not tested yet — do not bin them with the jigs.

Source: [print plan §5.2 — checkpoint after each batch](../../voron-print-plan.md#52-checkpoint-after-each-batch) · [00-slicer-setup § Gate A](00-slicer-setup.md#gate-a-no-kit-needed-the-cube) · [Ellis' Print Tuning Guide](https://ellis3dp.com/Print-Tuning-Guide/) · [Voron materials — shrinkage 100 %](https://docs.vorondesign.com/materials.html)

## Step B00.6 — Sort into bins

**Do:**

1. Sort every part into its bin off the diagram above.
2. Mark plate id and date on a hidden face.
3. Bag the three **Gate B coupons** at the front of 00-jigs: `GATE B — bore and inserts now, rail on kit day`.

**B00-P1** — bin labels print from the [bin-labels sheet](../../print/bin-labels.md).

| bin | parts off this plate |
|---|---|
| **00-jigs** — Jigs and coupons | `Voron_Design_Cube_v7`, `Heatset_Practice`, `MGN12_rail_guide` ×2, `MGN9_rail_guide` ×2, `pulley_jig` |
| **02-Z0** — Z0 corner (front-left, `_a` hand) | `z_drive_retainer_a` |

**Check:** Bins 00-jigs and 02-Z0 are labelled, every part off this plate is in one of them, and the Gate B bag is closed.

Tip: after Gate B the retainer moves to **02-Z0**; the cube stays as the reference coupon.

Pause: ~10 min since the last pause — plate sorted into 00-jigs and 02-Z0, the GATE B bag closed and marked. Step B00.7 is next, on the caliper and the KADRICK inserts; its bearing and rail rows wait for the kit.

Source: [print plan §9 — batch summary](../../voron-print-plan.md#9-machine-readable-batch-summary) · [print plan §2 — which parts gate which step](../../voron-print-plan.md#2-which-parts-gate-the-frame-and-z-drive-steps) · [print/README § Bins](README.md#bins)

## Step B00.7 — Gate B, bore and inserts now, rail on kit day

**Do:**

1. Open the GATE B bag and run [Gate B](00-slicer-setup.md#gate-b-bore-and-inserts-now-rail-on-kit-day).
2. Caliper the `z_drive_retainer_a` 625-2RS pocket, then set seven KADRICK inserts.
3. Kit day: thumb a real 625-2RS into that pocket, then slide the guide onto a taped carriage.

**Check:** The pocket calipers 16.30 mm ±0.15 and all seven inserts sit flush. Bearing and rail rows sign off on kit day.

| coupon | when | passes when |
|---|---|---|
| `z_drive_retainer_a` 625-2RS pocket, calipered | now | reads **16.30 mm ±0.15** across the pocket |
| heat-set inserts | now, on seven KADRICK M3×H5 | **flush to 0.2 mm proud**, no boss bulge > 0.2 mm |
| insert count | now | the practice seven come out of the KADRICK kit; all **153** kit inserts stay for the build |
| the same pocket, on a real 625-2RS | kit day, out of carton 1 | thumb pressure seats it, **no rocking** |
| `MGN12_rail_guide` | kit day, out of carton 1 | seats with **light finger pressure** |

```gate-calc
id: gate-b
title: Gate B — bore, inserts, and the kit-day rows
inputs:
  - key: bore
    label: 625-2RS pocket across the retainer (mm)
    nominal: 16.30
    tol: 0.15
    low: Under. Confirm shrinkage compensation is 0 % and XY compensation is 0, then reduce the extrusion multiplier 1 %, reprint the retainer and the cube, and re-pass Gate A before B01.
    high: Over. Confirm shrinkage compensation is 0 % and XY compensation is 0, then raise the extrusion multiplier 1 %, reprint the retainer and the cube, and re-pass Gate A before B01. Never fix a bore with XY compensation.
    why: This pocket is the seat every Z drive presses a 625-2RS into, and it is the gate protecting the 22 h of Z-drive bodies that print against the same profile.
  - key: inserts
    label: All seven inserts flush to 0.2 mm proud, no boss bulging over 0.2 mm
    kind: yesno
    no: A bulging boss is technique, not the slicer. The iron is too hot or you are pushing too fast. Practise on the spare pockets until two in a row land flush, and do not re-slice anything.
    why: The kit's 153 inserts go into real parts from Ch 00 onwards, so seven flush, un-bulged ones on a coupon are how you learn the iron before a chapter part sees it.
  - key: bearing
    label: Kit day. A real 625-2RS seats by thumb with no rocking
    kind: yesno
    optional: true
    no: Reprint the retainer and the cube against the corrected multiplier, then re-pass Gate A. This row waits for carton 1, so leave it blank until the kit lands.
    why: This is the press fit the caliper has been standing in for all along, so it either confirms months of printing or sends the retainer and the cube back through Gate A.
  - key: rail
    label: Kit day. MGN12_rail_guide slides on with light finger pressure
    kind: yesno
    optional: true
    no: Very tight means over-extrusion, loose means under-extrusion. This row gates nothing but a 20 minute reprint of the guide, so leave it blank until the kit lands.
    why: The guide is a 3 g jig rather than a machine part, so this row gates nothing but a 20 minute reprint and is the cheapest confirmation the profile is still right on kit day.
pass: Gate B passed on the rows you can run today. B01 and B03 to B06 are released. The two kit-day rows sign off out of carton 1.
```

⚠ A pocket outside 16.30 mm ±0.15 is the profile, not the part. Confirm shrinkage compensation is 0 %, then move extrusion multiplier 1 %, reprint the retainer and the cube, re-pass Gate A, and only then start B01. A bulging boss is technique, so practise rather than re-slice. The six MGN9 rails stay sealed until rail prep.

A 625-2RS is the plain 16 mm bearing in every Z drive, and this pocket is the seat it presses into. The
caliper now is standing in for that press: if the pocket is wrong, 22 h of Z-drive bodies would print wrong
with it. Flush, un-bulged inserts mean the iron is right before any real part sees one.

Pause: ~15 min since the last pause — Gate B's caliper and insert rows are measured and written down; B01 and B03–B06 are released. Put the retainer in bin 02-Z0 and keep the rail guide in 00-jigs for the kit-day rows.

Source: [00-slicer-setup § Gate B](00-slicer-setup.md#gate-b-bore-and-inserts-now-rail-on-kit-day) · [print plan §1.4](../../voron-print-plan.md#14-calibration-sequence-run-this-before-batch-1-and-again-after-the-gen-2-upgrade) · [Voron materials — shrinkage 100 %](https://docs.vorondesign.com/materials.html) · [LDO heat-set insert tool guide](https://docs.ldomotors.com/guides/heatset_insert_tool_guide)

---

## Checkpoint B00

**Gate A — before B02 and B07**

- [ ] Gen 2 belt upgrade done (index row 1), or the 2026-10-15 contingency consciously taken
- [ ] PrusaSlicer wizard run with the 0.4 HF nozzle; B00-P1 opened and showed `(modified)` on all three boxes, ` - Voron black` filament, and 3 h 58 m / 51.7 g
- [ ] Cube X and Y both within 30.00 mm ±0.15 mm
- [ ] Cube Z within 30.00 mm ±0.10 mm
- [ ] First-layer-vs-mid-height X delta ≤0.15 mm
- [ ] Cube corner snap test: no delamination
- [ ] First layer passed without a Live Adjust Z nudge, or the cause of the nudge is fixed
- [ ] Shrinkage compensation XY and Z confirmed at 0 % in the filament preset
- [ ] Bins 00-jigs and 02-Z0 labelled; the three Gate B coupons in a closed bag at the front of 00-jigs

**Gate B — before B01 and B03–B06**

- [ ] `z_drive_retainer_a` 625-2RS pocket calipers 16.30 mm ±0.15
- [ ] `Heatset_Practice`: 7/7 KADRICK M3×H5 inserts flush to ≤0.2 mm proud, no boss bulge >0.2 mm; all 153 kit inserts untouched
- [ ] `z_drive_retainer_a` moved to bin 02-Z0
- [ ] *(kit day)* a real 625-2RS presses into that pocket by thumb, no rocking
- [ ] *(kit day)* `MGN12_rail_guide` fits the real MGN12 rail with light finger pressure

## Common mistakes
- Skipping the chamber-preheat gate — ASA's first layer on a cold bed looks fine and then lifts at hour 2.
- Reaching for negative XY compensation to fix an oversized cube — wrecks bearing fits everywhere else; use extrusion multiplier instead.
- Hunting the printer's menus for a first-layer calibration wizard — the Core One+ has none; the loadcell does it, and Live Adjust Z is a per-print nudge that is not saved.
- Rushing the `Heatset_Practice` coupon — technique (iron temp/speed) matters more than any slicer setting here.
- Starting B01 on Gate A alone "because the cube is fine" — the bore is the gate that protects 22.8 h of Z-drive bodies.
- Resetting the printer preset to its system value to clear the "(modified)" mark — that throws the cold-probe start G-code away and puts a hot nozzle back on the mesh.

## Next
Printing: Gate B (Step B00.7) on the caliper and the KADRICK inserts, then [B01 — Z drive assemblies](B01-z-drive-assemblies.md) and on through B02 → B10 in numeric order, all before the kit. Assembly: Ch 00 needs this plate's `Heatset_Practice` and rail guides on kit day; Ch 01 Frame needs no printed part.
