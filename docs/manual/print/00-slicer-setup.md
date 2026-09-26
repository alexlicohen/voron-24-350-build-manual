# Slicer setup — PrusaSlicer profile and Voron overrides

One-time setup for every print batch (`B00`–`B10`). Read this chapter before B00; batch chapters link
back here and list only their own deviations (brim, orientation, accent colour). B11, the PETG V0 bay
ducting, uses its own bundle, `slicer/bay-ducts-petg.ini`, and the textured sheet: see [its page](B11-bay-ducting.md).

```mascot
pose: check
caption: Set the profile once, carefully. Twenty two plates inherit these numbers and none of them ask twice.
```

**Slicer:** PrusaSlicer **2.9.6** (current stable, released 2026-06-25). PrusaSlicer **3.0.0-alpha11**
(published 2026-09-01) is an early preview.
([releases](https://github.com/prusa3d/PrusaSlicer/releases))

**Version posture.** First build: **2.9.6 for every batch, B11 included** (decision 2026-09-26). The 3.0
preview is not used for this build; *PrusaSlicer 3.0 preview* at the end is reference only, for when it goes
stable.
Changing slicer version is a toolchain change: re-run Gate A — and Gate B once the kit is here — before the
next plate.

**Base profiles** (read out of a `PrusaResearch.ini` with `inherits` resolved). Two copies of that
file exist and they are not the same file:

- `/Applications/PrusaSlicer.app/Contents/Resources/profiles/PrusaResearch.ini` — the copy shipped
  inside the 2.9.6 app bundle, `config_version = 2.4.14`. This is what `slicer/resolve_preset.py`
  reads, so it is the base the committed `.ini` and the plate 3MFs were derived from.
- `~/Library/Application Support/PrusaSlicer/vendor/PrusaResearch.ini` — the vendor bundle the GUI
  actually resolves presets against, auto-updated in place. It is at `config_version = 2.5.9` today (2.5.9, 2026-09-08, only added INDX/XL filament profiles; nothing for the CORE One HF0.4 or Prusament ASA changed).

They differ on one key that reaches these plates: 2.5.8+'s CORE One `start_gcode` bumps the firmware
check from `M115 U6.5.3+12780` to `U6.8.1+16182`. Nothing mechanical differs; a re-derive should be
resolved against the live bundle. Our plates carry neither version verbatim — every one of them ships the
**cold-probe start G-code** instead (below), and that is what makes the Plater's **printer** box read
"(modified)".

The machine has the **high-flow 0.4 nozzle**, so the HF variants are the base wherever one exists:

- Printer: **`Prusa CORE One HF0.4 nozzle`** (printer model `Prusa CORE One & CORE One+`) — bed 250×220,
  max height 270, retract 0.7 mm @ 45 mm/s, [z-hop](../16-glossary.md#z) 0.2 mm, wipe off. The non-HF
  `Prusa CORE One 0.4 nozzle` preset *inherits from this one* and only sets `nozzle_high_flow = 0`;
  every mechanical value is identical.
- Filament: **`Prusament ASA @COREONE HF0.4`** — nozzle **265 °C**, bed 110 °C, chamber 55 °C
  (minimum 40 °C), fan 20–25 %, first 4 layers fan off, density 1.07 g/cm³, max
  [volumetric flow](../16-glossary.md#v) **26 mm³/s**. (The non-HF `Prusament ASA @COREONE` is 260 °C / 15 mm³/s.)
- Print: **`0.20mm STRUCTURAL @COREONE 0.4`** — *not* SPEED. STRUCTURAL is already the quality-biased
  profile (perimeters 70 mm/s vs SPEED's 170; external 50 vs 170; infill 120 vs 200).

⚠ **There is no `0.20mm STRUCTURAL @COREONE HF0.4`.** At 0.20 mm the bundle ships STRUCTURAL only in
the non-HF variant; the HF entries at this layer height are SPEED and BALANCED. That is not a problem:
`0.20mm STRUCTURAL @COREONE 0.4`'s compatibility rule is `printer_model=~/(COREONE|…)/ and
nozzle_diameter[0]==0.4` with **no** `nozzle_high_flow` clause, so PrusaSlicer offers it on the HF
printer. Do not "upgrade" to `0.20mm BALANCED @COREONE HF0.4` — it inherits from the STRUCTURAL preset
and then raises perimeter 70→150, external 50→200 and small-perimeter 50→170 mm/s, and drops bottom
solid layers to 3.

**High flow raises the ceiling, not the speeds.** Every speed below stays exactly as the table says.
At those speeds the peak volumetric flow is 110 mm/s solid infill × 0.4 × 0.2 = **8.8 mm³/s**, well under the
15 mm³/s the non-HF profile allows, let alone 26 — so the HF base changes the melt temperature and the
start G-code and nothing else about these plates.

## Committed projects — open the plate, don't rebuild it

You do **not** re-enter any of this by hand. Every plate is committed as a PrusaSlicer 2.9.6 project
with the arrangement, the per-object brims and the full configuration already inside it:

| What | Where |
|---|---|
| One project per plate, 22 of them | `slicer/plates/B01-P1.3mf` … |
| Config bundle for `--load` (black / accent) | `slicer/voron-coreone-asa.ini`, `slicer/voron-accent-blue.ini` |
| The cold-probe start G-code, vendored | `slicer/coreone-cold-start.gcode` (`slicer/sync_start_gcode.py` keeps the inis and the 22 projects in step) |
| Every override below → ini key → value → the line it came from | `slicer/OVERRIDES.md` |
| SHA256 + pinned commit of every STL | `slicer/stl/MANIFEST.sha256` |
| Sliced time and grams per plate, vs the old model | `slicer/estimates.csv` |
| The pre-B00 hot first-layer check (five squares, not a plate of the run, outside every total) | `slicer/checks/hot-first-layer.3mf` (`slicer/hot_check.py` rebuilds and checks it) |

Open `slicer/plates/<plate>.3mf` in PrusaSlicer (**File → Open Project**) and slice. The project
carries its own print/filament/printer configuration, so it does not matter which presets you had
selected. After a plate is re-saved from the GUI, refresh its numbers with
`python3 slicer/build_plates.py --from-3mf <plate id> [<plate id> ...]`: it re-slices those committed 3MFs
as they are, replaces their rows in `slicer/estimates.csv` (and their run's total) and redraws their
diagrams. `--from-3mf` with no ids does the same for all 27 plates, which is safe but slow. **Never drop
`--from-3mf`:** without it the script re-packs the plates from `slicer/plates.py` and rewrites their 3MFs,
all 27 when no ids are given, and every hand arrangement in them is lost. `python3 slicer/fetch_stls.py`
re-downloads the pinned STLs if `slicer/stl/` is empty.

⚠ **The plates carry the cold-probe start G-code — leave it alone.** All 22 projects and both `.ini`
bundles ship the same block as the GUI preset `Prusa CORE One HF0.4 nozzle - coldstart`: the nozzle stays
at 0 °C through homing and the whole mesh, and the `G29 P9` nozzle wipe is removed because a cold tip
cannot be wiped. Clean the tip by hand while it is hot, after each print. Opening a project therefore shows
the Printer box as `Prusa CORE One HF0.4 nozzle (modified)` — that modification *is* the cold start.

### One-time PrusaSlicer setup — before the first project

1. **Configuration → Configuration Wizard → Prusa FFF → Prusa CORE One & CORE One+** → tick the
   **0.4 HF** nozzle (tick it even if plain 0.4 is already ticked) → Filaments: **Prusament ASA** → Finish.
   A fresh install without the HF variant makes PrusaSlicer ask what to do about the project's missing
   printer profile when you open a plate, and the wrong answer maps the plate onto whatever printer is
   active. The estimate check in every Load step would catch that, but only after a wasted quarter hour.
2. **File → Open Project → `slicer/plates/B00-P1.3mf`.** If a dialog offers to install a printer
   profile, accept.
3. **Read the three preset boxes on the Plater tab.** They will *not* show the bare names above:

   | Box | What it shows | Why |
   |---|---|---|
   | Printer | `Prusa CORE One HF0.4 nozzle` — **always with (modified)** | the project replaces `start_gcode` with the cold-probe block and adds one printer key, `thumbnails` (`slicer/build_config.py`, a 640×480 PNG so a GUI G-code export carries a doc-sized preview). Both are expected; the "(modified)" is the cold start and must stay |
   | Print | `0.20mm STRUCTURAL @COREONE 0.4 (modified)` | the project's overrides sit on the system preset |
   | Filament | `Prusament ASA @COREONE HF0.4 - Voron black` (` - Voron blue` on the three B02 plates) | the project's renamed filament preset, shrinkage zeroed |

   "(modified)" on the printer box is **not** a fault and is not the signal to look for — it is the
   cold-probe start G-code, and a printer box *without* it means the project did not load. The other two
   signals that it did not load are a **print** box without "(modified)" and a **filament**
   box reading the bare `Prusament ASA @COREONE HF0.4` — any of those, or an estimate that does not
   match the Load step's numbers, means do not slice; reopen the project. A printer box naming a
   different printer entirely (not just "(modified)") is the wizard problem in step 1.

   You do not need to select the GUI preset `Prusa CORE One HF0.4 nozzle - coldstart` before opening a
   plate: the preset and the project hold the identical block, and the project's own copy wins. Selecting
   it changes nothing, and never "reset to system value" on the printer box — that throws the cold start
   away.

The times and weights in every batch chapter are **PrusaSlicer 2.9.6 estimates** from these
projects, not a throughput model. Treat the first plate as the calibration of the *printer*, not of
the estimate: if B00-P1 comes off within a few minutes of 4.0 h, the whole table is trustworthy.

## Overrides

"Source" = where the number comes from. A source of **judgment** means it is a call made for this build,
not a cited spec — treat it as adjustable if the calibration cube (below) says otherwise.

### Print settings

| Setting | STRUCTURAL default | Set to | Why | Source |
|---|---|---|---|---|
| Layer height / first layer | 0.20 / 0.20 | **keep** | Voron spec | Manual p.4 |
| Perimeters | 2 | **4** | Voron spec; wall count carries load in these parts | Manual p.4 |
| Top solid layers | 5 | **keep 5** | Voron spec | Manual p.4 |
| Bottom solid layers | 4 | **5** | Voron spec says 5 top **and** bottom | Manual p.4 |
| Fill density | 15 % | **40 %** | Voron spec | Manual p.4 |
| Fill pattern | Grid | **keep Grid** | Voron allows grid/gyroid/honeycomb/triangle/cubic | Manual p.4 |
| Extrusion width (default, perimeter, external, infill, solid) | 0.45 | **0.40** | Voron: "Extrusion width — Recommended: Forced 0.4 mm". Ribs, bosses and bearing seats were drawn around a 0.4 bead. | Manual p.4 |
| First layer extrusion width | 0.50 | **keep 0.50** | wider first bead = better ASA adhesion | judgment |
| Top infill extrusion width | 0.42 | **0.40** | consistency | judgment |
| Perimeter generator | [Arachne](../16-glossary.md#a) | **keep Arachne** | Voron's "forced 0.4" predates Arachne. Arachne varies bead width on purpose and handles Voron's thin ribs better than Classic. Setting nominal width to 0.4 gives Arachne the right target. | judgment |
| Supports | on (auto off) | **None** | every Voron/LDO/Nevermore STL is pre-oriented with built-in break-away supports where needed | Manual; Nevermore README; Klicky STL README |
| [Seam](../16-glossary.md#s) position | Aligned | **Rear** | keeps the seam off the visible outward faces of skirts and the toolhead | build spec |
| [Skirt](../16-glossary.md#s) loops | 0 | **1 loop, 3 mm gap, min length 4 mm** | primes after the long ASA purge; lets you abort in the first 60 s if the first layer is wrong | judgment |
| [Brim](../16-glossary.md#b) | off | **off globally; 5 mm on the tall/narrow parts, 3 mm on the 150–182 mm skirts** — already applied per object in the committed 3MFs, see §Orientation & brim below | ASA corner lift on long flat parts and tippy tall parts | Prusa warping KB; judgment |
| **XY size compensation** | 0 | **keep 0** | Voron: "The parts have been designed with ABS/ASA shrinkage in mind… shrinkage should be set to 100 %. Compensating for this is likely to make bearing fits and screw holes too large." | docs.vorondesign.com/materials.html |
| [Elephant-foot](../16-glossary.md#e) compensation | 0.20 | **keep 0.20 for now, verify on the cube** | shrinks only the first layer; several Voron parts have a bearing bore starting at the bed — measure before changing | judgment |
| External perimeter speed | 50 | **35** | surface finish and corner accuracy on the visible skirts; speed is not a goal here | judgment |
| Perimeter speed | 70 | **55** | more time at temperature per bead = better interlayer bond at 4 walls | judgment |
| Infill speed | 120 | **100** | interior quality and less pressure variation into the perimeters | judgment |
| Solid infill speed | 140 | **110** | flatter top/bottom faces on the skirts | judgment |
| Top solid infill | 80 | **keep 80** | already conservative | — |
| First layer speed | 45 | **25** | ASA on smooth PEI is the single biggest failure mode; slow the first layer (and see §Print sheet) | Prusa ASA KB; judgment |
| External perimeters first | off | **keep off** | inside-out gives better dimensional accuracy on holes; only flip it if you see external-perimeter bulging | judgment |
| Dynamic overhang speeds | on (15/25/45/90 %) | **keep on** | Prusa tuned these for the Core One's part fan | — |
| Ironing | off | **keep off** | — | — |

### Filament settings (Prusament ASA @COREONE HF0.4)

| Setting | Profile default | Set to | Why | Source |
|---|---|---|---|---|
| **Shrinkage compensation XY** | **0.22 %** | **0 %** | Same rule as XY size compensation — PrusaSlicer 2.9 scales ASA parts up 0.22 %; that is +0.15 mm on a 66.7 mm Z-drive body and +0.035 mm on every 16 mm bearing bore, compounding with any flow error. **This is the single most important override in this document.** | docs.vorondesign.com/materials.html + profile value |
| Shrinkage compensation Z | 0.22 % | **0 %** | same reason | as above |
| Nozzle / first-layer nozzle | 265 / 265 °C | **keep** | Prusa's own Prusament ASA values for this machine *and this nozzle* — the HF0.4 profile runs 5 °C hotter than the non-HF one | profile (`Prusament ASA @COREONE HF0.4`) |
| Bed / first-layer bed | 110 / 110 °C | **keep** | Prusa ASA guidance is ≥100 °C bed | profile; Prusa ASA KB |
| Chamber temperature | 55 °C | **keep 55** | matches the 55–60 °C a real Voron sees; the Voron parts are designed for it | profile; docs.vorondesign.com/materials.html |
| Chamber minimal temperature | 40 °C | **keep 40** | printer will not start until the chamber reaches 40 °C — this *is* the preheat gate | profile |
| Min / max fan | 20 / 25 % | **keep for B00–B02, then decide** | Prusa tuned this for the Core One chamber. If perimeter separation shows on the Z-drive bodies, drop to 0 / 15 % and keep bridge fan at 25 %. | profile; Ellis — Perimeter Separation |
| Max volumetric speed | 26 mm³/s | **keep** | not a limit at these speeds — the plates peak at 8.8 mm³/s | profile (HF0.4) |
| Retraction / z-hop | 0.7 mm / 0.2 mm | **keep** | Nextruder-specific; do not touch | printer profile |

### Drying

ASA is mildly hygroscopic. A fresh, sealed Prusament spool used within ~2 weeks needs nothing. Dry at
**80 °C for 4 h** (Prusa KB) if a spool has been open longer, or the moment you see stringing, matte striping, or
popping. The Sunlu SP2 on the bench tops out at 70 °C, so there it is **70 °C for 6 h**, with the port plugs out. Keep the active spool in one USS Drybox during the run. Voron parts are structural — this is the
material where wet filament actually costs strength. ([Prusa ASA KB](https://help.prusa3d.com/article/asa_1809).)

## Print sheet

Decided, and written on the sheet's edge tape; every batch's pre-print step then says "sheet per
00-slicer-setup" and nothing more.

- **Which sheet:** the smooth/satin PEI sheet that shipped with the Core One+. The textured sheets are for
  PLA/PETG and were bought for that; ASA adheres poorly to textured and the smooth sheet needs no glue to
  hold it — the glue below is a release layer, not an adhesion aid.
- **Glue stick on either.** ASA bonds to PEI hard enough that a big flat part (the 66 mm Z-drive bodies,
  the 182 mm rear skirt) can pull the coating off a smooth sheet; the glue is a *separation* layer, not an
  adhesion aid. Thin, even film over the printed area, re-applied every 2–3 plates.
- **Cleaning:** wash the old glue off with warm water and dish soap, then IPA on the smooth sheet. **Never
  acetone or ASA juice on a powder-coated sheet** — it strips the coating.

Tip: Prusa's own ASA article is the source for the sheet, the glue stick and the acetone warning — *"use the smooth or powder-coated PEI sheet with a glue stick"*, *"ASA sticks very well to our print sheets"*. [help.prusa3d.com/article/asa_1809](https://help.prusa3d.com/article/asa_1809)

## Calibration sequence — run before B00, and again after any toolchain change

The dimensional gate is in **two parts**. **Gate A** needs only the cube. **Gate B** tests the fits, and
the parts it would fit against — the [625-2RS](../16-glossary.md#f) bearing and the MGN12 rail — come in
the Voron kit. Nothing is bought to bring them forward: what runs early is the *dimensional* half of Gate
B, a caliper on the printed bores and seven real inserts out of the KADRICK kit already on the bench. The
bearing press and the rail slide are signed off on kit day, and the rail row gates nothing but a 20-minute
reprint of the ASA `MGN12_rail_guide` (3 g). Each gate releases its own set of batches (table below).

**Printer status, 2026-09-23.** Bed flatness is closed — flat to ±0.1 mm on printed Z-stop correction caps,
verified at 60 °C. Belt tuning was never formally closed; the Gen 2 belt upgrade that would redo it is now
**deferred to the INDX rebuild this winter** (Prusa documents the combined install), so the whole 157.0 h
run stays on the current **Gen 1 GT2** belts. Run this sequence after two pre-B00 checks instead — see
[B00 § Before B00 checks](B00-calibration-and-jigs.md#before-b00-belt-and-hot-bed-checks): a belt pluck check (belt tuning is still
open) and a hot first-layer check at ASA bed temperature (the bed has only been verified at 60 °C), run on
its committed project right after Step B00.0 installs the presets. Either
check failing means doing the Gen 2 upgrade now, before B00, after all.

1. **Advanced Filtration Kit — already fitted** (2026-09-12), so nothing to install here. ~157 h of ASA is
   about to run in an enclosure: confirm on the first ASA plate that the blower runs and the bypass flaps
   seal. One spare cartridge is still to buy (~600 print-h each, 1–2 wk Prusa lead time).
2. **Firmware ≥ 6.8.1** on the Core One+ — the current non-INDX build, required either way. It already
   carries the Settings → Hardware → Edition selector the Gen 2 + INDX rebuild will use later.
3. **First layer: there is nothing to run.** The Core One+ has no first-layer calibration wizard — the
   Nextruder loadcell sets Z automatically before every print, as part of mesh bed levelling. Judge
   B00-P1's first layer by Ellis' smooth-bottom rule: no gaps between beads, no ridging. If it needs a
   nudge, long-press the knob during the first layer → **Live Adjust Z**. That nudge is **not remembered**
   for the next print, so if you needed one, fix the cause (sheet not seated, debris under it, nozzle not
   fully seated, glue film uneven) before the next plate rather than nudging every plate.
   ([Prusa KB — Live Adjust Z](https://help.prusa3d.com/article/live-adjust-z_112427) ·
   [Ellis — first layer squish](https://ellis3dp.com/Print-Tuning-Guide/articles/first_layer_squish.html))
4. **Print plate B00-P1.** It carries the coupons for both gates.
5. **Measure with calipers, at mid-height (not across the first layer).**

### Gate A — no kit needed (the cube)

| Coupon | Nominal | Accept | If out of spec |
|---|---|---|---|
| `Voron_Design_Cube_v7` X and Y | 30.00 mm | **±0.15 mm** | >+0.15: confirm shrinkage compensation is 0 % and XY compensation is 0. Still over → reduce [extrusion multiplier](../16-glossary.md#e) in 1 % steps. Do **not** dial in negative XY compensation — it wrecks the bearing fits. |
| `Voron_Design_Cube_v7` Z | 30.00 mm | **±0.10 mm** | over → first layer under-squished; under → over-squished (Live Adjust Z, then fix the cause — item 3) |
| Cube first layer vs mid-height X | — | difference **≤ 0.15 mm** | bigger → elephant-foot compensation is wrong; adjust in 0.05 mm steps |
| Cube corner snap test | — | must **not** delaminate along a layer line | delamination → chamber too cold or fan too high → drop min/max fan to 0/15 % |

The four rows are also a calculator at [Step B00.5](B00-calibration-and-jigs.md#step-b005-inspect-gate-a-the-cube-no-kit-needed): type the measurements in, press Check, and it keeps the verdict and shows the advice from this table for whichever row failed.

**Corner snap:** grip one corner in pliers and bend it off. A pass tears *across* the layers and leaves a
rough, fibrous face; a fail peels cleanly *along* one layer line and leaves a flat shiny face `(verify on
bench)`.

**Where the two numbers live.** Extrusion multiplier: **Filament Settings → Filament**. Shrinkage
compensation: **Filament Settings → Advanced**. Both belong to the filament preset *inside each project*,
so a change made here does not travel: re-enter it in every later project as you open it, and write the
value on the sheet-edge tape so you know what it should be.

**Gate A passed →** every batch with no press fit is released: **B02**, **B07**, and the cosmetics
**B08 → B09 → B10**. Do **not** start B01 or B03–B06 on Gate A alone: that is 58.4 h and 763 g of
bearing-seat and shaft-bore parts printed against an unverified fit — run Gate B first, the same week.

### Gate B — bore and inserts now, rail on kit day

| When | Coupon | Nominal | Accept | If out of spec |
|---|---|---|---|---|
| **now** | `Heatset_Practice` | 7 × M3×H5 inserts from the KADRICK kit — all seven pockets. Shank must caliper ~4 mm `(verify on bench)` | insert sits flush to 0.2 mm proud, boss does not bulge > 0.2 mm | bulging → iron too hot or pushed too fast — a technique problem, not a slicer one. Do all seven before touching a real part. Ch 00 Steps 00.14–00.15 are this row, same coupon, same session: the coupon's one use. |
| **now** | `z_drive_retainer_a` 625-2RS pocket (same plate) | **16.30 mm**, measured off the STL; the concentric lip below it is 14.30 mm | caliper across the pocket reads 16.30 mm ±0.15 | over → confirm shrinkage compensation is 0 % and XY compensation is 0, then raise [extrusion multiplier](../16-glossary.md#e) 1 %. Under → reduce it 1 %. Never fix it with XY compensation. |
| **kit day** | the same pocket, on a real 625-2RS (16 mm OD) | — | bearing presses in with thumb pressure, no rocking | this is the press fit the caliper is standing in for; a fail here reprints the retainer and the cube, and re-passes Gate A |
| **kit day** | `MGN12_rail_guide` on the real MGN12 rail | — | slides on with light finger pressure | very tight → over-extrusion; loose → under-extrusion |

The inserts are set by the adult with the **X-Tronic iron's stock conical tip**; the helper never handles
the iron. The LDO brass M3 tip lands with the kit: it is fitted at Ch 00 Step 00.13 and re-checked on the
first real insert at Step 02.03. Seven of the KADRICK kit's inserts are consumed here; **all 153 kit
inserts stay for the build**.

The same calculator covers Gate B at [Step B00.7](B00-calibration-and-jigs.md#step-b007-gate-b-bore-and-inserts-now-rail-on-kit-day), with the two kit-day rows marked optional so they can stay blank until carton 1 is open.

**Gate B passed →** start **B01**, then **B03–B06**. Gate B is Step B00.7; its two early rows take about
15 minutes and unblock 58.4 h of printing, so run them in the same week as Gate A. If Gate B moves the
extrusion multiplier, re-print the cube and re-pass Gate A before B01.

If the bore is still loose with shrinkage compensation already at 0 % and XY compensation at 0, **raise the
extrusion multiplier 1 %, reprint the retainer and the cube, and re-pass Gate A** before B01 starts. There
is no other lever: negative XY compensation buys this one bore at the cost of every other fit in the
machine.

6. **Which gate releases which batch:**

| Batch | Gate | Why |
|---|---|---|
| B02, B07 | **A** | no bearing seats, no rail fit; their heat-set bosses get inserts on kit day |
| B08, B09, B10 | **A** | cosmetic; the skirts are where VFA shows most, but they print on the same GT2 belts as the rest of the run — Galaxy Black's fleck hides the ripple, and GT1.5 lands with the INDX + Gen 2 rebuild |
| B01, B03, B04, B05, B06 | **B** (bore + inserts, run early) | 625-2RS pockets, F695 flange seats, MGN12 carriage pattern, Z-joint bolt pattern |

**Quality gate before every later batch:** look at the *last* plate pulled off. If any part shows
(a) a lifted corner, (b) a delaminated layer, or (c) a bore/boss that failed a test fit — fix that before
starting the next plate. Don't print 100 g on top of a known problem.

## Orientation & brim

**Do not change which face sits on the bed.** Every Voron, LDO, Klicky, Nevermore and Clicky-Clack STL ships
pre-oriented for support-free printing. Rotating a part **about Z** (in the plane of the bed) to make it fit
is fine — it does not change the layer orientation. Two exceptions to the face rule:

1. `XY_cable_chain_bridge-Igus-3mm_backer.stl` is a community remix and arrives standing 44 mm tall on a
   21 mm-wide footprint, unlike the stock part which lies flat. Check it in the preview before slicing — if
   it isn't sitting on a flat face, lay it down to match the stock `[a]_xy_joint_cable_bridge_2hole`.
2. The two Clicky-Clack `Hinge-L-*` parts. As designed the hinges are on the **left** and the door opens from
   the right; mirror both hinge files (2.9.6 only — the 3.0 preview has no mirror tool) if the printer's
   left side will be against a wall. The handle and latch are symmetric.
   [src](https://github.com/tanaes/whopping_Voron_mods/tree/main/clickyclacky_door)

No part in this build exceeds 150 mm in Z. Tallest parts, in order:

| Part | Height | Footprint | Aspect | Brim in the project |
|---|---:|---|---|---|
| `Handle.stl` (Clicky-Clack) | 60.0 mm | 67.9 × 18.6 | tall & narrow | **5 mm** |
| `Latch.stl` (Clicky-Clack) | 58.0 mm | 25.9 × 14.6 | very tall & narrow | **5 mm** |
| `Hinge-L-sleeve/solid-2X` ×4 | 55.0 mm | 20.9 × 19.5 | very tall & narrow | **5 mm** |
| `mount.stl` (TFT) | 44.8 mm | 117 × 67 | fine | none |
| `z_motor_mount_a/b` ×4 | 42.0 mm | 51 × 30.7 | borderline | none — add one by hand only if a print shows lift |

The committed projects turn parts about Z wherever it packs the bed better — `slicer/geom.py` picks the
orientation, and the plate diagram in each chapter shows the result (drawn from the committed project itself, so a plate you re-arrange in the GUI and save is redrawn by `python3 slicer/build_plates.py --from-3mf`). That is the allowed kind of rotation:
it never changes which face is on the bed. Example: B08-P1 stands the 182 mm `rear_center_skirt_350`
front-to-back (turned 90° from the STL) beside an unturned `side_fan_support`, because side by side as
shipped the pair needs 254 mm of X on a 250 mm bed.

These brims are **already set per object** inside `slicer/plates/*.3mf` — you do not apply them by
hand, and a part that is not on one of these two lists gets no brim even when it shares a plate with
one that does. The plate diagram at the top of each Load step draws the brim ring, so the check at every
plate is the same: *the outline shows on the parts the chapter names, and on nothing else.*

Separately, the projects **brim the long flat parts** — not because they're tall, but because 150–182 mm of ASA
on a plate lifts at the ends — and a few smaller flat ones with them: **3 mm brim** on `rear_center_skirt_350`, `front_skirt_a/b_350`, `side_skirt_a/b_350`,
`side_fan_support_x2`, `keystone_panel`, `power_inlet_IECGS_1mm`, `exhaust_cover`, `V2_Duo_Plenum`,
`Regular_Cartridge`, `wago_221-415_mount_3by5`, `exhaust_filter_grill`, `cob_light_strip_mount_100mm`. Brim
separation stays at PrusaSlicer's 0.1 mm so it snaps off.

**If you ever need to add a brim by hand** (a reprint that lifted): right-click the object in the object
list → **Add settings → Skirt and brim → Brim width**, and set it on that object only. **Never use the
global brim setting** (Print Settings → Skirt and brim) — it brims every flat part on the plate, including
the skirt fan grills (`[a]_fan_grill_*`) and clips that must not have one.

Parts with **built-in supports to break out, not cut**: `[a]_stealthburner_main_body`, `Regular_Cartridge`
(Nevermore), `V2_Duo_Plenum`. The skirts are single-shell parts — they have no break-away body.

## Colour key

| Prefix | Meaning | Our filament |
|---|---|---|
| *(none)* | Primary colour | **Prusament ASA Galaxy Black** |
| `[a]_` | Accent colour | **Prusament ASA Blue** |
| `[o]_` | Opaque — must block light | Galaxy Black (perfect) |
| `[c]_` | Clear / translucent | **Do not print** — LDO supplies the SB LED diffuser in clear PETG |
| `_x#` suffix | **Quantity required to build the machine** | e.g. `z_joint_lower_x4.stl` → print 4 copies of the file |

The `_x#` number is a *quantity*, not a hint that the file contains that many bodies. Files confirmed to
contain more than one body: `[a]_stealthburner_main_body` (7 — built-in supports), `cw2_captive_pcb_cover` (2),
`usb_adapter_mount` (2 — mount base + cover), `Leviathan_bracket_set` (2 — L+R), `bottom_panel_hinge_x2` (2),
`cob_light_strip_mount_*` (2 — the mount is a 2-piece assembly), `V2_Duo_Plenum` (2 — built-in support),
`usb_adapter_mount_partial_cover` (2 — Nitehawk-SB V2).
Clicky-Clack's `Hinge-L-sleeve-2X` / `-solid-2X` contain **one** body each — "2X" means print two.

Three non-Voron parts carry no `[a]_` prefix but are printed **Blue** by choice: `Handle.stl`
(Clicky-Clack), `ldo_bestagon_insert.stl`, and `XY_cable_chain_bridge-Igus-3mm_backer.stl` (a remix of the
accent `[a]_xy_joint_cable_bridge_2hole`).

## Gen 2 belt upgrade — deferred to the INDX rebuild

**Where things stand (2026-09-23).** The Core One+ is built and commissioned — commissioning closed
2026-09-13 on **Gen 1 (GT2) belts**, bed flat to ±0.1 mm on printed Z-stop correction caps. The Gen 1→Gen 2
upgrade kit (Prusa order 1787919456) has shipped. The LDO Voron kit has not: Fabreeko's tracking page still
shows the V2.4/Trident batch in manufacture, so realistic delivery is **late November to late December 2026**.

**Decision (2026-09-23): the Gen 2 upgrade is deferred to the INDX 8-tool conversion this winter,** not done
before B00. Prusa documents the combined install:
<https://help.prusa3d.com/article/assemblling-the-prusa-indx-core-one-with-the-gen-2-upgrade_1147602>. The
whole 157.0 h / 22-plate run — B00 → B10, numeric order — prints on the current Gen 1 GT2 belts. This
supersedes the earlier "Gen 2 before B00" baseline and its 2026-10-15 contingency; there is no mid-run pause,
because nothing changes the machine under the parts.

**Why.** The printer is commissioned and printing well; the upgrade fixes neither open issue on the bench
(loadcell/heater noise, PETG infill strands); a heatbed swap now would put the closed bed calibration
(±0.1 mm on the +2.8 front-left Z-stop correction cap) at risk and force a belt retune, an XY-homing recal
and a start-G-code re-sync of all 22 committed `.3mf` projects; GT1.5's benefit is cosmetic (less VFA) and
Galaxy Black's metallic fleck already hides it; and one teardown (with INDX) beats two.

**Two checks replace it, before B00** — see [B00 § Before B00 checks](B00-calibration-and-jigs.md#before-b00-belt-and-hot-bed-checks) for
the full tick list `(verify on bench)`:

1. **Belt pluck check.** Belt tuning was never formally closed. Pluck mid-belt (motors disabled, head front,
   X centred) via belt.connect.prusa3d.com or the Prusa app; targets upper ≈96 Hz, lower ≈92 Hz, ≤8 Hz apart.
   Out of range → Control → Calibrations & Tests → Belt Tuning, tensioner screws half a turn, evenly and
   alternately.
2. **Hot first-layer check, at ASA bed temperature.** The bed has only been verified flat at 60 °C, not at
   the Voron ASA batches' 50–60 °C chamber / hotter bed. Its project is committed:
   `slicer/checks/hot-first-layer.3mf`, five 30×30×0.2 mm squares (four corners + centre, one layer) in
   Galaxy Black ASA on B00-P1's presets, 110 °C bed, cold start G-code. It runs after Step B00.0, whose wizard
   installs those presets. Pass: no "bed not aligned" prompt, every square 0.17–0.23 mm, spread ≤0.05 mm.

Either check failing means doing the Gen 2 upgrade now, before B00, after all — then re-running both checks.

**After the eventual INDX + Gen 2 rebuild, before restarting prints:**

1. Firmware ≥ 6.8.1 (carries GT1.5 belt support and the Gen 2 expansion joints; the combined INDX + Gen 2
   guide supersedes the standalone Gen 2 KB article once both go in together).
2. Re-tension both belts and re-square the gantry.
3. Re-run the self-test and input shaper calibration.
4. **Re-print `Voron_Design_Cube_v7` and re-pass Gate A** — steps/mm changes with the pulleys, so the
   dimensional gate must be re-passed before you print 399 g of skirts (B08) or anything else on the rebuilt
   machine. Judge the cube's first layer as
   in item 3 of the calibration sequence — the loadcell re-zeroes on its own; there is no wizard to redo.

**The same rule generalises:** *any* toolchain change — slicer version (2.9.6 → 3.0), profile bundle, belts,
pulleys or nozzle — re-runs Gate A (and Gate B, if run before the kit's fits are all confirmed) before the
next plate. For this build that next applies at the INDX + Gen 2 rebuild, not mid-run.

Do **not** try to interleave a belt/tool upgrade with a running plate — the Nextruder and bed have to come apart.

## STL source of truth

*Reference only — you need this only if you re-derive the plates. `slicer/fetch_stls.py` fetches these
exact trees and `slicer/stl/MANIFEST.sha256` pins every file to a commit; printing from the committed
projects needs none of it.*

Do not use a re-hosted zip or a Printables mirror. The Voron repos have no release tags — the manifest
records the branch head so a mid-build reprint is identical to the first print.

| # | What | Repo / branch | Path |
|---|---|---|---|
| 1 | Voron 2.4 R2 core | `VoronDesign/Voron-2` branch `Voron2.4` | `/STLs` |
| 2 | Stealthburner + Clockwork 2 | `VoronDesign/Voron-Stealthburner` branch `main` | `/STLs` |
| 3 | LDO kit-specific | `MotorDynamicsLab/LDOVoron2` branch `main` | `/STLs` |
| 4 | LDO touchscreen mount | `MotorDynamicsLab/LDOVoronTrident` branch `master` | `/STLs/BTT Pi TFT4.3 Mount` |
| 5 | Nitehawk-SB | `MotorDynamicsLab/Nitehawk-SB` branch `master` | `/STLs` |
| 5b | Nitehawk-SB V2 (Rev D+ USB cover) | `MotorDynamicsLab/Nitehawk-SB-V2` branch `master` | `/STLs` |
| 6 | Klicky probe | `jlas1/Klicky-Probe` branch `main` | `/Probes/KlickyProbe/STL` + `/Printers/Voron/v1.8_v2.4_Legacy_Trident/v1.8_v2.4_Legacy_Trident_STL` |
| 7 | Nevermore Micro V5 Duo | `nevermore3d/Nevermore_Micro` branch `master` | `/V5_Duo/V2` |
| 8 | Clicky-Clack door | `tanaes/whopping_Voron_mods` branch `main` | `/clickyclacky_door/STLs` |
| 9 | Backer-aware cable bridge (conditional) | `tanaes/whopping_Voron_mods` branch `main` | `/extrusion_backers/STLs` |

## PrusaSlicer 3.0 preview

*Reference only — first build: 2.9.6 for everything.*

3.0.0-alpha11 (2026-09-01) is usable for the cosmetic batches but changes enough that it is not a drop-in.
Verified against the 3.0 branch, not recalled:

- **Profiles moved** from the single `PrusaResearch.ini` to per-preset YAML under
  `resources/presets/prusa-research-fff/PrusaResearch/`.
- **ASA shrinkage is still 0.22 %** on CORE One (`preset-filament-common.yaml`, id `*shrinkage_ASA*`,
  `condition: printer.base_model=~/(COREONE|COREONE_INDX)/`) — so the zeroing override in the Filament
  table above is unchanged and just as important.
- **`0.20mm STRUCTURAL @COREONE 0.4` exists under the same name.** Its `bottom_solid_layers` default is
  **3** in 3.0, not 4 — the action is unchanged: set it to **5**.
- **`support_material` is now one enum** (CORE One base value `enforcers_only`) replacing the 2.x
  `support_material` + `support_material_auto` pair. Set it to `none`.
- **The printer is picked as the model** "Prusa CORE One & CORE One+" with the nozzle chosen per-tool, not
  as a `…0.4 nozzle` preset.
- **Extrusion-width auto/percent values now resolve against nozzle diameter** instead of layer height.
  Harmless here — every width in the override table is an explicit mm value.
- **No `.ini` import.** 3.0 has no Import Config / Import Config Bundle / Export Config, so
  `slicer/voron-coreone-asa.ini` does not cross the boundary. What does cross is the plate projects:
  3.0 imports a 2.x **3MF project** config and maps it to system presets, so open
  `slicer/plates/<plate>.3mf` and check every override by hand against the tables above. A 3.0 project
  opened in 2.9.6 loads geometry only — the configuration is discarded (2.9.1+ warns).
- **No mirroring.** Mirroring is still on the 3.0 queue, so the B10 `Hinge-L-*` mirror cannot be done in the
  preview: slice B10 in 2.9.6, or mirror the STL outside the slicer.
