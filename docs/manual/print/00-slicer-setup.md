# Slicer setup — PrusaSlicer profile and Voron overrides

One-time setup for every print batch (`B00`–`B10`). Read this chapter before B00; batch chapters link
back here and list only their own deviations (brim, orientation, accent colour).

**Slicer:** PrusaSlicer **2.9.6** (current stable, released 2026-06-25). PrusaSlicer **3.0.0-alpha11**
(published 2026-09-01) is an early preview.
([releases](https://github.com/prusa3d/PrusaSlicer/releases))

**Version posture.** First build: **2.9.6 for everything.** The dimension-critical batches — the **B00
gates**, **B01**, and **B03–B06** — are 2.9.6 only. 3.0 is acceptable for **B08–B10** provided you re-enter
every override in this document by hand (see *PrusaSlicer 3.0 preview*, reference-only, at the end).
Changing slicer version is a toolchain change: re-run Gate A — and Gate B once the kit is here — before the
next plate.

**Base profiles** (read out of the `PrusaResearch.ini` that ships with the installed 2.9.6 —
`config_version = 2.4.14` — with `inherits` resolved). The machine has the **high-flow 0.4 nozzle**,
so the HF variants are the base wherever one exists:

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
At those speeds the peak volumetric flow is 100 mm/s × 0.4 × 0.2 = **8.0 mm³/s**, well under the
15 mm³/s the non-HF profile allows, let alone 26 — so the HF base changes the melt temperature and the
start G-code and nothing else about these plates.

## Committed projects — open the plate, don't rebuild it

You do **not** re-enter any of this by hand. Every plate is committed as a PrusaSlicer 2.9.6 project
with the arrangement, the per-object brims and the full configuration already inside it:

| What | Where |
|---|---|
| One project per plate, 27 of them | `slicer/plates/B01-P1.3mf` … |
| Config bundle for `--load` (black / accent) | `slicer/voron-coreone-asa.ini`, `slicer/voron-accent-orange.ini` |
| Every override below → ini key → value → the line it came from | `slicer/OVERRIDES.md` |
| SHA256 + pinned commit of every STL | `slicer/stl/MANIFEST.sha256` |
| Sliced time and grams per plate, vs the old model | `slicer/estimates.csv` |

Open `slicer/plates/<plate>.3mf` in PrusaSlicer (**File → Open Project**) and slice. The project
carries its own print/filament/printer configuration, so it does not matter which presets you had
selected. Re-derive everything with `python3 slicer/fetch_stls.py && python3 slicer/build_plates.py`.

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
   | Printer | `Prusa CORE One HF0.4 nozzle` | system preset |
   | Print | `0.20mm STRUCTURAL @COREONE 0.4 (modified)` | the project's overrides sit on the system preset |
   | Filament | `Prusament ASA @COREONE HF0.4 - Voron black` (` - Voron orange` on the three B02 plates) | the project's renamed filament preset, shrinkage zeroed |

   A print box **without** "(modified)", or a filament box reading the bare `Prusament ASA @COREONE HF0.4`,
   means the project's configuration did not load — do not slice; reopen the project.

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
| **Shrinkage compensation XY** | **0.22 %** | **0 %** | Same rule as XY size compensation — PrusaSlicer 2.9 scales ASA parts up 0.22 %; on a 66.7 mm Z-drive body that is +0.15 mm and it lands straight in the bearing bores. **This is the single most important override in this document.** | docs.vorondesign.com/materials.html + profile value |
| Shrinkage compensation Z | 0.22 % | **0 %** | same reason | as above |
| Nozzle / first-layer nozzle | 265 / 265 °C | **keep** | Prusa's own Prusament ASA values for this machine *and this nozzle* — the HF0.4 profile runs 5 °C hotter than the non-HF one | profile (`Prusament ASA @COREONE HF0.4`) |
| Bed / first-layer bed | 110 / 110 °C | **keep** | Prusa ASA guidance is ≥100 °C bed | profile; Prusa ASA KB |
| Chamber temperature | 55 °C | **keep 55** | matches the 55–60 °C a real Voron sees; the Voron parts are designed for it | profile; docs.vorondesign.com/materials.html |
| Chamber minimal temperature | 40 °C | **keep 40** | printer will not start until the chamber reaches 40 °C — this *is* the preheat gate | profile |
| Min / max fan | 20 / 25 % | **keep for B00–B02, then decide** | Prusa tuned this for the Core One chamber. If perimeter separation shows on the Z-drive bodies, drop to 0 / 15 % and keep bridge fan at 25 %. | profile; Ellis — Perimeter Separation |
| Max volumetric speed | 26 mm³/s | **keep** | not a limit at these speeds — the plates peak at 8.0 mm³/s | profile (HF0.4) |
| Retraction / z-hop | 0.7 mm / 0.2 mm | **keep** | Nextruder-specific; do not touch | printer profile |

### Drying

ASA is mildly hygroscopic. A fresh, sealed Prusament spool used within ~2 weeks needs nothing. Dry at
**80 °C for 4 h** if a spool has been open longer, or the moment you see stringing, matte striping, or
popping. Keep the active spool in one USS Drybox during the run. Voron parts are structural — this is the
material where wet filament actually costs strength. (Prusa ASA KB; drying decision in project `CLAUDE.md`.)

## Print sheet

Decide this once, before B00-P1, and write the decision on the sheet's edge tape; every batch's pre-print
step then says "sheet per 00-slicer-setup" and nothing more.

- **Which sheet:** the smooth PEI sheet or the satin/textured (powder-coated) PEI sheet — both work for ASA.
- **Glue stick on either.** ASA bonds to PEI hard enough that a big flat part (the 66 mm Z-drive bodies,
  the 182 mm rear skirt) can pull the coating off a smooth sheet; the glue is a *separation* layer, not an
  adhesion aid. Thin, even film over the printed area, re-applied every 2–3 plates.
- **Cleaning:** wash the old glue off with warm water and dish soap, then IPA on the smooth sheet. **Never
  acetone or ASA juice on a powder-coated sheet** — it strips the coating.

Tip: Prusa's own ASA article is the source for the sheet, the glue stick and the acetone warning — *"use the smooth or powder-coated PEI sheet with a glue stick"*, *"ASA sticks very well to our print sheets"*. [help.prusa3d.com/article/asa_1809](https://help.prusa3d.com/article/asa_1809)

## Calibration sequence — run before B00, and again after the Gen 2 upgrade

The dimensional gate is in **two parts**, because three of its coupons need parts that only arrive with
the Voron kit: the [625-2RS](../16-glossary.md#f) bearing, the MGN12 rail and the M3×5×4
[heat-set inserts](../16-glossary.md#h). **Gate A** needs only the cube and runs the day the plate comes
off; **Gate B** runs the morning the kit lands. Each gate releases its own set of batches (table below).

1. **Install the Advanced Filtration Kit first.** ~157 h of ASA is about to run in an enclosure. Do it
   while the back panel is already off (Core One+ Ch.7), not later.
2. **Firmware ≥ 6.9.0** on the Core One+ (needed for GT1.5 belts later; harmless now).
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

**Gate A passed →** print **B02** (orange — no press fits) and **B07** (bay parts — no bearing seats)
now, then, once the Gen 2 belt upgrade is done and the cube re-passes Gate A, the cosmetics
**B08 → B09 → B10**. Do **not** start B01 or B03–B06 on Gate A alone: that is 58.5 h and 763 g of
bearing-seat and shaft-bore parts printed against an unverified fit.

### Gate B — kit day (bore, rail, inserts)

| Coupon | Nominal | Accept | If out of spec |
|---|---|---|---|
| `Heatset_Practice` | 7 × M3×5×4 inserts — all seven pockets, from the kit's 153 (146 remain for the build) | insert sits flush to 0.2 mm proud, boss does not bulge > 0.2 mm | bulging → iron too hot or pushed too fast — a technique problem, not a slicer one. Do all seven before touching a real part; Ch 00 Steps 00.13–00.16 use this same coupon. |
| `MGN12_rail_guide` on the real MGN12 rail | — | slides on with light finger pressure | very tight → over-extrusion; loose → under-extrusion |
| `z_drive_retainer_a` 625-2RS bore (same plate) | 625-2RS bearing, 16 mm OD | bearing presses in with thumb pressure, no rocking | **The real press-fit gate.** Loose → check shrinkage compensation is 0 %. Tight → reduce EM 1 %, do not enlarge with compensation. |

**Gate B passed →** start **B01**, then **B03–B06**. Gate B is Step B00.7; it takes about 15 minutes
and unblocks 22.8 h of printing, so run it before Ch 00's inventory, not after. If Gate B moves the
extrusion multiplier, re-print the cube and re-pass Gate A before B01.

Two 625-2RS bearings and ten M3×5×4 inserts (seven for the coupon) cost a few dollars: order them with the filament and Gate B
can run in the same week as Gate A, with the parts otherwise sitting idle until the kit lands.

6. **Which gate releases which batch:**

| Batch | Gate | Why |
|---|---|---|
| B02, B07 | **A** | no bearing seats, no rail fit; their heat-set bosses get inserts on kit day |
| B08, B09, B10 | **A**, re-passed on a fresh cube after the Gen 2 belt upgrade | cosmetic; the skirts are where GT1.5's reduced VFA shows |
| B01, B03, B04, B05, B06 | **B** | 625-2RS / F695 seats, MGN12 carriage pattern, 8 mm shaft bores |

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
on a plate lifts at the ends: **3 mm brim** on `rear_center_skirt_350`, `front_skirt_a/b_350`, `side_skirt_a/b_350`,
`side_fan_support_x2`, `keystone_panel`, `power_inlet_IECGS_1mm`, `exhaust_cover`, `V2_Duo_Plenum`,
`Regular_Cartridge`, `wago_221-415_mount_3by5`, `exhaust_filter_grill`, `cob_light_strip_mount_100mm`. Brim
separation stays at PrusaSlicer's 0.1 mm so it snaps off.

**If you ever need to add a brim by hand** (a reprint that lifted): right-click the object in the object
list → **Add settings → Skirt and brim → Brim width**, and set it on that object only. **Never use the
global brim setting** (Print Settings → Skirt and brim) — it brims every flat part on the plate, including
fan grills and clips that must not have one.

Parts with **built-in supports to break out, not cut**: `[a]_stealthburner_main_body`, `Regular_Cartridge`
(Nevermore), `V2_Duo_Plenum`. The skirts are single-shell parts — they have no break-away body.

## Colour key

| Prefix | Meaning | Our filament |
|---|---|---|
| *(none)* | Primary colour | **Prusament ASA Galaxy Black** |
| `[a]_` | Accent colour | **Prusament ASA Prusa Orange** |
| `[o]_` | Opaque — must block light | Galaxy Black (perfect) |
| `[c]_` | Clear / translucent | **Do not print** — LDO supplies the SB LED diffuser in clear PETG |
| `_x#` suffix | **Quantity required to build the machine** | e.g. `z_joint_lower_x4.stl` → print 4 copies of the file |

The `_x#` number is a *quantity*, not a hint that the file contains that many bodies. Files confirmed to
contain more than one body: `[a]_stealthburner_main_body` (7 — built-in supports), `cw2_captive_pcb_cover` (2),
`usb_adapter_mount` (2 — mount base + cover), `Leviathan_bracket_set` (2 — L+R), `bottom_panel_hinge_x2` (2),
`cob_light_strip_mount_*` (2 — the mount is a 2-piece assembly), `V2_Duo_Plenum` (2 — built-in support),
`usb_adapter_mount_partial_cover` (2 — Nitehawk-SB V2).
Clicky-Clack's `Hinge-L-sleeve-2X` / `-solid-2X` contain **one** body each — "2X" means print two.

Three non-Voron parts carry no `[a]_` prefix but are printed **Orange** by choice: `Handle.stl`
(Clicky-Clack), `ldo_bestagon_insert.stl`, and `XY_cable_chain_bridge-Igus-3mm_backer.stl` (a remix of the
accent `[a]_xy_joint_cable_bridge_2hole`).

## Gen 2 belt-upgrade pause rule

**Baseline plan:** finish the Core One+ kit through Ch.9 (self-test + first print), apply the Gen 1→Gen 2
upgrade, re-tension and re-square, *then* start B00. The GT1.5 conversion changes belts, pulleys, steps/mm
and firmware together — get it done and settled before 157.1 h of ASA.

**If the upgrade kit arrives mid-run, pause at the end of Batch B07, before Batch B08.**

1. B08 + B09 + B10 are 12 of the 27 plates and contain every surface anyone will ever look at — the
   150–182 mm skirts are large flat vertical faces, exactly where GT1.5's reduced VFA shows.
2. B00–B07 are structural parts inside the machine; VFA there is cosmetically irrelevant.
3. Clean boundary — no half-finished sub-assembly waits on it, and in the pre-kit order (B00 → B02 → B07 →
   B08) it is exactly where the cosmetic run begins.

**Second-best boundary:** if the kit arrives before B02 starts, do it then — the Stealthburner main body is
the single most-looked-at printed part on the machine and it's on B02-P1.

**After the upgrade, before restarting prints:**

1. Firmware ≥ 6.9.0 (adds GT1.5 belt support and Gen 2 expansion joints).
2. Re-tension both belts and re-square the gantry, per [help.prusa3d.com/manual/prusa-core-one-to-gen-2-upgrade_2435](https://help.prusa3d.com/manual/prusa-core-one-to-gen-2-upgrade_2435).
3. Re-run the self-test and input shaper calibration.
4. **Re-print `Voron_Design_Cube_v7` and re-pass Gate A** — steps/mm changed with the pulleys; the
   dimensional gate must be re-passed before printing 399 g of skirts (B08). Judge the cube's first layer as
   in item 3 of the calibration sequence — the loadcell re-zeroes on its own; there is no wizard to redo.

**The same rule generalises:** *any* toolchain change — slicer version (2.9.6 → 3.0), profile bundle, belts,
pulleys or nozzle — re-runs Gate A (and Gate B, once the kit is here) before the next plate.

Do **not** try to interleave the upgrade with a running plate — the Nextruder and bed have to come apart.

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
