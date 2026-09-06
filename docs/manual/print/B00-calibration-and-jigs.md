# Batch B00 — Calibration & jigs

One plate: the dimensional gate for the whole build, plus the rail-alignment jigs and the pulley jig. The
gate is in two parts — **Gate A** (the cube, no kit needed) releases B02 and B07 the day this plate comes
off, and the cosmetics B08–B10 once the Gen 2 belt upgrade is done; **Gate B** (bearing bore, rail fit,
real inserts) runs the morning the kit lands and releases B01 and B03–B06.

**Time:** 4.0 h (1 plate) — PrusaSlicer 2.9.6 estimate, sliced from `slicer/plates/B00-P1.3mf`.

**Sessions:** ~15 min one-time slicer and filament setup, then 1 plate start (~5 min hands-on, then 4.0 h unattended) + ~15 min for Gate A + ~10 min sorting + ~15 min for Gate B on kit day.

**Prerequisites:** none — this is the first batch. Slicer set up per [00-slicer-setup.md](00-slicer-setup.md)
(Step B00.0 below walks the one-time wizard).

**Printed parts**


| STL | Repo path | Qty | Colour | g ea | Bin |
|---|---|---:|---|---:|---|
| `Voron_Design_Cube_v7.stl` | Voron-2 `STLs/Test_Prints/` | 1 | Black | 16.2 | 00-jigs |
| `Heatset_Practice.stl` | Voron-2 `STLs/Test_Prints/` | 1 | Black | 6.5 | 00-jigs |
| `MGN12_rail_guide_x2.stl` | Voron-2 `STLs/Tools/` | 2 | Black | 3.2 | 00-jigs |
| `MGN9_rail_guide_x2.stl` | Voron-2 `STLs/Tools/` | 2 | Black | 2.7 | 00-jigs |
| `pulley_jig.stl` | Voron-2 `STLs/Tools/` | 1 | Black | 2.8 | 00-jigs |
| `z_drive_retainer_a_x2.stl` | Voron-2 `STLs/Z_Drive/` | 1 *(of the 2 needed — this is the bearing-fit coupon and a real part)* | Black | 19.5 | 02-Z0 |

**Hardware:** none printed here. Gate B (Step B00.7) needs seven M3×5×4 [heat-set inserts](../16-glossary.md#h) (the coupon has seven pockets; 146 of the kit's 153 remain for the build),
one [625-2RS](../16-glossary.md#f) bearing and the MGN12 rail — all from the Voron kit, unless you order
2× 625-2RS and 10× inserts with the filament so Gate B can run early.

**Read first**

- The two-part gate in [00-slicer-setup.md](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade).
  **Gate A** (cube X/Y, Z, first-layer-vs-mid delta, corner snap) is Step B00.5 and releases B02, B07 and —
  after the Gen 2 upgrade — B08–B10. **Gate B** (`Heatset_Practice` with real inserts, `MGN12_rail_guide` on
  the real rail, `z_drive_retainer_a`'s 625-2RS bore) is Step B00.7, on kit day, and releases B01 and B03–B06.
- Most commonly reprinted here: the cube, until the profile is right.
- `z_drive_retainer_a` on this plate is deliberate — it's your bearing-press-fit coupon **and** one of the two
  you need for B01, so nothing is wasted.
- First layer: the Core One+ has no first-layer wizard. The loadcell sets Z before every print; you judge the
  result (Step B00.4) and nudge with Live Adjust Z only if you must.

## Step B00.0 — One-time PrusaSlicer setup

**Do:**

1. PrusaSlicer 2.9.6, **Configuration → Configuration Wizard**: **Prusa FFF**, **Prusa CORE One & CORE One+**.
2. Tick the **0.4 HF** nozzle even with plain 0.4 ticked; filament **Prusament ASA**; Finish.
3. **File → Open Project**: `slicer/plates/B00-P1.3mf`; accept any profile dialog.

**Check:** The Plater's three preset boxes read `Prusa CORE One HF0.4 nozzle`, `0.20mm STRUCTURAL @COREONE 0.4 (modified)` and `Prusament ASA @COREONE HF0.4 - Voron black`.

⚠ The `(modified)` marks and the ` - Voron black` suffix are correct: they are the project's own overrides, and the printer box also counts a 640×480 thumbnail and a self-updating vendor bundle. The project did **not** load if the print box lacks `(modified)`, the filament box reads bare `Prusament ASA @COREONE HF0.4`, the estimate at Step B00.2 is wrong, or the printer box names another printer.

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

1. Start the plate; watch the first layer 2–3 minutes.
2. Gappy or ridged beads: long-press the knob → **Live Adjust Z** and nudge.
3. If you nudged, find the cause before B02: sheet seating, glue film, nozzle seating.

**Check:** First layer smooth, no gaps between beads, no ridging, and either no Live Adjust Z nudge or its cause written in the log.

Source: [00-slicer-setup § Calibration sequence, item 3](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) · [Prusa KB — Live Adjust Z](https://help.prusa3d.com/article/live-adjust-z_112427) · [Ellis — first layer squish](https://ellis3dp.com/Print-Tuning-Guide/articles/first_layer_squish.html) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B00.5 — Inspect: Gate A (the cube, no kit needed)

**Do:**

1. Once cool, remove the plate and run [**Gate A**](00-slicer-setup.md#gate-a-no-kit-needed-the-cube) with calipers at mid-height.
2. Cube X/Y 30.00 mm ±0.15 mm, Z 30.00 mm ±0.10 mm, first-layer-vs-mid-height X delta ≤0.15 mm, corner snap no delamination.
3. Log all four numbers.

**Check:** All four pass; any failure means adjusting [extrusion multiplier](../16-glossary.md#e), never negative XY compensation, then reprinting this plate before B02 or B07.

Pause: ~15 min since the last pause — Gate A is measured and written down; B02 and B07 are released. The Gate B coupons (`Heatset_Practice`, one `MGN12_rail_guide`, `z_drive_retainer_a`) are not tested yet — do not bin them with the jigs.

Source: [print plan §5.2 — checkpoint after each batch](../../voron-print-plan.md#52-checkpoint-after-each-batch) · [00-slicer-setup § Gate A](00-slicer-setup.md#gate-a-no-kit-needed-the-cube) · [Ellis' Print Tuning Guide](https://ellis3dp.com/Print-Tuning-Guide/) · [Voron materials — shrinkage 100 %](https://docs.vorondesign.com/materials.html)

## Step B00.6 — Sort into bins

**Do:**

1. Sort every part into its bin off the diagram above.
2. Bag the three **Gate B coupons** at the front of 00-jigs: `GATE B — open on kit day`.
3. After Gate B the retainer moves to **02-Z0**; the cube stays as the reference coupon.

**B00-P1** — bin labels print from the [bin-labels sheet](../../print/bin-labels.md).

| bin | parts off this plate |
|---|---|
| **00-jigs** — Jigs and coupons | `Voron_Design_Cube_v7`, `Heatset_Practice`, `MGN12_rail_guide` ×2, `MGN9_rail_guide` ×2, `pulley_jig` |
| **02-Z0** — Z0 corner (front-left, `_a` hand) | `z_drive_retainer_a` |

**Check:** Bins 00-jigs and 02-Z0 are labelled, every part off this plate is in one of them, and the Gate B bag is closed.

Pause: ~10 min since the last pause — plate sorted into 00-jigs and 02-Z0, the GATE B bag closed and marked. Step B00.7 waits for the kit, so this is the end of B00 until kit day.

Source: [print plan §9 — batch summary](../../voron-print-plan.md#9-machine-readable-batch-summary) · [print plan §2 — which parts gate which step](../../voron-print-plan.md#2-which-parts-gate-the-frame-and-z-drive-steps) · [print/README § Bins](README.md#bins)

## Step B00.7 — Gate B, on kit day (bore, rail, inserts)

**Do:**

1. Open the GATE B bag and run [Gate B](00-slicer-setup.md#gate-b-kit-day-bore-rail-inserts).
2. Thumb a 625-2RS into the `z_drive_retainer_a` bore and set seven M3×5×4 inserts in `Heatset_Practice`.
3. Unbag one MGN12 rail, tape the carriage, band the ends 15 mm in, slide `MGN12_rail_guide` on.

**Check:** All three pass, so B01 starts now at Step B01.1 and B03–B06 follow.

⚠ A tight or loose bore is the profile: adjust extrusion multiplier per the Gate B table, re-run Gate A on a fresh cube, and re-print this retainer before B01. A bulging boss is technique, so practise rather than re-slice. The six MGN9 rails stay sealed until rail prep.

Pause: ~15 min since the last pause — Gate B is measured and written down; B01 and B03–B06 are released. Put the retainer in bin 02-Z0 and the rail guide back in 00-jigs before the inventory starts.

Source: [00-slicer-setup § Gate B](00-slicer-setup.md#gate-b-kit-day-bore-rail-inserts) · [print plan §1.4](../../voron-print-plan.md#14-calibration-sequence-run-this-before-batch-1-and-again-after-the-gen-2-upgrade) · [Voron materials — shrinkage 100 %](https://docs.vorondesign.com/materials.html) · [LDO heat-set insert tool guide](https://docs.ldomotors.com/guides/heatset_insert_tool_guide)

---

## Checkpoint B00

**Gate A — before B02 and B07**

- [ ] PrusaSlicer wizard run with the 0.4 HF nozzle; B00-P1 opened and showed `(modified)` / ` - Voron black` presets and 3 h 58 m / 51.7 g
- [ ] Cube X and Y both within 30.00 mm ±0.15 mm
- [ ] Cube Z within 30.00 mm ±0.10 mm
- [ ] First-layer-vs-mid-height X delta ≤0.15 mm
- [ ] Cube corner snap test: no delamination
- [ ] First layer passed without a Live Adjust Z nudge, or the cause of the nudge is fixed
- [ ] Shrinkage compensation XY and Z confirmed at 0 % in the filament preset
- [ ] Bins 00-jigs and 02-Z0 labelled; the three Gate B coupons in a closed bag at the front of 00-jigs

**Gate B — kit day, before B01 and B03–B06**

- [ ] `z_drive_retainer_a` 625-2RS bore: bearing presses in by thumb, no rocking
- [ ] `MGN12_rail_guide` fits the real MGN12 rail with light finger pressure
- [ ] `Heatset_Practice`: 7/7 inserts flush to ≤0.2 mm proud, no boss bulge >0.2 mm
- [ ] `z_drive_retainer_a` moved to bin 02-Z0

## Common mistakes
- Skipping the chamber-preheat gate — ASA's first layer on a cold bed looks fine and then lifts at hour 2.
- Reaching for negative XY compensation to fix an oversized cube — wrecks bearing fits everywhere else; use extrusion multiplier instead.
- Hunting the printer's menus for a first-layer calibration wizard — the Core One+ has none; the loadcell does it, and Live Adjust Z is a per-print nudge that is not saved.
- Rushing the `Heatset_Practice` coupon — technique (iron temp/speed) matters more than any slicer setting here.
- Starting B01 on Gate A alone "because the cube is fine" — the bore fit is the gate that protects 22.8 h of Z-drive bodies, and it needs the real bearing.

## Next
Printing, kit not here: [B02 — Accent parts (orange)](B02-accent-parts-orange.md), then B07, then (after the Gen 2 upgrade) B08–B10. Printing, kit day: Gate B (Step B00.7), then [B01 — Z drive assemblies](B01-z-drive-assemblies.md). Assembly: Ch 00 needs this plate's `Heatset_Practice` and rail guides; Ch 01 Frame needs no printed part.
