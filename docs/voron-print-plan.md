# Voron 2.4 R2 (LDO Rev D+, 350) — Printed Parts Plan

Print every part on the **Prusa Core One+**, Prusament ASA, plate by plate, in build order.
Written to be followed with a 13-year-old: one plate = one job.

**Totals at a glance:** 27 plates · **156.9 h** print time · **1811 g Galaxy Black + 279 g Prusa Orange** ·
against 2400 g black + 800 g orange on hand. PrusaSlicer 2.9.6 estimates, sliced from the committed
projects in `slicer/plates/` (§4.1); they replace a throughput model that read 134.3 h / 2248 g.

---

## 0. What kit you actually have (established facts, with sources)

Everything below is from LDO's or Fabreeko's own pages, not from blogs.

| Fact | Value | Source |
|---|---|---|
| Kit | LDO Voron 2.4 R2 **Rev D+**, 350 mm | [Fabreeko product page](https://www.fabreeko.com/products/ldo-voron-v2-4-kit) |
| What "Rev D+" changes vs Rev D | "Nitehawk SB update with USB passthrough for USB based eddy current probes" (Mar 2026). **Mostly electrical — one printed-part change:** the V2 board's USB-adapter cover is `MotorDynamicsLab/Nitehawk-SB-V2/STLs/usb_adapter_mount_partial_cover.stl` (ground-lug mount), not the V1 `usb_adapter_mount.stl` cover — see batch B07. | [Fabreeko](https://www.fabreeko.com/products/ldo-voron-v2-4-kit) |
| Mainboard | **LDO Leviathan** (5× TMC2209 + 2× TMC5160HV for A/B, 48 V capable, integrated Raspberry Pi mount) | [Fabreeko](https://www.fabreeko.com/products/ldo-voron-v2-4-kit); [LDO wiring guide Rev D](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d) |
| Toolhead board | **Nitehawk-SB V2** (STM32G0B1; USB toolhead PCB, **integrated ADXL**) — the "+" in Rev D+ | [LDO Voron 2.4 kit page](https://docs.ldomotors.com/en/voron/voron2) |
| Bed probe | **Omron inductive probe included AND a Klicky Probe Kit included** — you pick one. LDO: *"Instead of the included Omron inductive probe, we also provide the parts to build your machine using the optional Klicky mod by jlas1."* Wiring guide: *"Connect the inductive probe or Klicky cable to the PROBE port."* | [LDO kit page](https://docs.ldomotors.com/en/voron/voron2); [Rev D wiring guide](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d); [Rev D 350 BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D) lists "Klicky Probe Kit ×1" |
| Z endstop | LDO **nozzle-probe PCB**; the printed part `nozzle_probe_ldo.stl` **is supplied printed in the kit** | [Rev D printed parts guide](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d) |
| XY endstop | **D2F microswitch PCB** — print `[a]_endstop_pod_D2F_switch`, *not* the hall-effect pod. No hall effect anywhere in this kit. | [Rev D printed parts guide](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d); [Build Notes p.145](https://docs.ldomotors.com/voron/voron2/build-faq) |
| Screen | **BigTreeTech Pi TFT4.3** (4.3" capacitive DSI). Print the LDO **BTT Pi TFT4.3 Mount**; **do not print the mini12864 parts.** | [Rev D printed parts guide](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d); [Rev D 350 BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D) |
| Filtration | **Nevermore Micro V5 Duo** (6×3 mm magnets), *instead of* the stock Voron exhaust filter. Stock exhaust housing is NOT built; the back panel is sealed with LDO's `exhaust_cover` + the stock `exhaust_filter_grill`. Carbon not included. | [LDO kit page](https://docs.ldomotors.com/en/voron/voron2); [Rev D printed parts guide](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d); [LDO Nevermore guide](https://ldomotion.com/guides/nevermore-v5-duo---v24) |
| Hotend | E3D **Revo High-Flow (Revo Voron form factor)** → Stealthburner printhead files `revo_voron/*` | [Fabreeko](https://www.fabreeko.com/products/ldo-voron-v2-4-kit); [SB printhead compatibility table](https://github.com/VoronDesign/Voron-Stealthburner/blob/main/STLs/Stealthburner/Printheads/README.md) ("E3D Revo Voron → E-RV") |
| Cable chains | **2-hole** ends → always take the `_2hole` variants, never `_3hole` | [Rev D printed parts guide](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d) |
| Power inlet | 1.0 mm AC inlet with integrated switch → `power_inlet_IECGS_1mm.stl` | [Rev D printed parts guide](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d) |
| Panels | Deck 3 mm acrylic, back 3 mm acrylic, bottom 4 mm acrylic, doors/sides/top 3 mm PC. Foam tape 1 mm and 3 mm both supplied. | [Rev D 350 BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D) |
| Rails | 1× stainless MGN12H 400 (X) + 6× stainless MGN9H 400 (2× Y, 4× Z) → print **both** rail guides | [Rev D 350 BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D) |
| Printed parts included | **NOT** included with the kit — except the ten LDO parts listed in §7 | [Fabreeko](https://www.fabreeko.com/products/ldo-voron-v2-4-kit) |
| Clicky-Clack door kit | Hardware + extrusions only. **STLs come from GitHub**, panel bought separately (you did). | [Fabreeko Clicky-Clack page](https://www.fabreeko.com/products/clickyclackydoor-kit-by-ldo) |
| Titanium backers | Gantry X/Y extrusion stiffeners; **no stock STL changes**. Fabreeko's set ships pre-tapped for the cable chain. See §6 note. | [Fabreeko backers](https://www.fabreeko.com/products/v2-4-trident-titanium-extrusion-backers); [whoppingpochard backer README](https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers) |

**Parts where the kit revision changes the STL** — all three already resolved above, but flag them if the kit
that arrives is not Rev D/D+:

1. **Mainboard bracket.** Rev C and earlier shipped a BTT Octopus → `Octopus_bracket_set.stl`.
   Rev D ships Leviathan → `Leviathan_bracket_set.stl` (supplied printed). If a Rev C kit arrives, print the Octopus set.
2. **Raspberry Pi mount.** Rev C needed `beefy_raspberry_bracket.stl`; LDO Build Notes p.150 explicitly say
   *"it does not apply for rev D kits"* — Leviathan carries the Pi. Print nothing.
3. **XY endstop pod.** Rev A/B kits used a hall-effect endstop → `[a]_endstop_pod_hall_effect.stl` +
   `z_joint_upper_hall_effect.stl`. Rev C/D use the D2F PCB → `[a]_endstop_pod_D2F_switch.stl` + 4× plain `z_joint_upper_x4`.
4. **Display.** Rev A used the mini12864 skirt module; Rev C/D use the BTT touchscreen mount. Different front-skirt module entirely.
5. **Plug panel.** `power_inlet_IECGS_1mm` (Rev C/D, 1.0 mm inlet) vs `_1.2mm` vs `power_inlet_filtered`. LDO's own
   `plug_panel_1.2mm.stl` is marked deprecated for 2.4R2.

**Resolved 2026-09-05:** Rev D+ = Rev D + **Nitehawk-SB V2** — electrical plus one printed part
(`usb_adapter_mount_partial_cover`, batch B07). The Rev D printed-parts guide applies for everything else.
LDO still publishes no "Rev D+" printed-parts page (`printed_part_guide_rev_d_plus` returns 404); the only
open question for the Fabreeko Discord is whether one will ever be published.

---

## 1. Before the first plate

### 1.1 STL source of truth

Download these exact trees. Do not use a re-hosted zip or a Printables mirror.

| # | What | Repo / branch | Path |
|---|---|---|---|
| 1 | Voron 2.4 R2 core | `VoronDesign/Voron-2` branch **`Voron2.4`** | [`/STLs`](https://github.com/VoronDesign/Voron-2/tree/Voron2.4/STLs) |
| 2 | Stealthburner + Clockwork 2 | `VoronDesign/Voron-Stealthburner` branch **`main`** | [`/STLs`](https://github.com/VoronDesign/Voron-Stealthburner/tree/main/STLs) |
| 3 | LDO kit-specific | `MotorDynamicsLab/LDOVoron2` branch **`main`** | [`/STLs`](https://github.com/MotorDynamicsLab/LDOVoron2/tree/main/STLs) |
| 4 | LDO touchscreen mount | `MotorDynamicsLab/LDOVoronTrident` branch **`master`** | [`/STLs/BTT Pi TFT4.3 Mount`](https://github.com/MotorDynamicsLab/LDOVoronTrident/tree/master/STLs/BTT%20Pi%20TFT4.3%20Mount) |
| 5 | Nitehawk-SB | `MotorDynamicsLab/Nitehawk-SB` branch **`master`** | [`/STLs`](https://github.com/MotorDynamicsLab/Nitehawk-SB/tree/master/STLs) |
| 5b | Nitehawk-SB V2 (Rev D+ USB cover) | `MotorDynamicsLab/Nitehawk-SB-V2` branch **`master`** | [`/STLs`](https://github.com/MotorDynamicsLab/Nitehawk-SB-V2/tree/master/STLs) |
| 6 | Klicky probe | `jlas1/Klicky-Probe` branch **`main`** | [`/Probes/KlickyProbe/STL`](https://github.com/jlas1/Klicky-Probe/tree/main/Probes/KlickyProbe/STL) + [`/Printers/Voron/v1.8_v2.4_Legacy_Trident/v1.8_v2.4_Legacy_Trident_STL`](https://github.com/jlas1/Klicky-Probe/tree/main/Printers/Voron/v1.8_v2.4_Legacy_Trident/v1.8_v2.4_Legacy_Trident_STL) |
| 7 | Nevermore Micro V5 Duo | `nevermore3d/Nevermore_Micro` branch **`master`** | [`/V5_Duo/V2`](https://github.com/nevermore3d/Nevermore_Micro/tree/master/V5_Duo/V2) |
| 8 | Clicky-Clack door | `tanaes/whopping_Voron_mods` branch **`main`** | [`/clickyclacky_door/STLs`](https://github.com/tanaes/whopping_Voron_mods/tree/main/clickyclacky_door/STLs) |
| 9 | Backer-aware cable bridge (conditional) | `tanaes/whopping_Voron_mods` branch **`main`** | [`/extrusion_backers/STLs`](https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers/STLs) |

The Voron repos have no release tags; take the branch head and **record the commit SHA in a text file next to
your STLs** so a mid-build reprint is identical to the first print.

### 1.2 Colour key (Voron's own naming convention)

From the [2.4r2 Assembly Manual p.4–5](https://github.com/VoronDesign/Voron-2/blob/Voron2.4/Manual/Assembly_Manual_2.4r2.pdf)
and the [Stealthburner STL README](https://github.com/VoronDesign/Voron-Stealthburner/blob/main/STLs/README.md):

| Prefix | Meaning | Our filament |
|---|---|---|
| *(none)* | Primary colour | **Prusament ASA Galaxy Black** |
| `[a]_` | Accent colour | **Prusament ASA Prusa Orange** |
| `[o]_` | Opaque — must block light | Galaxy Black (perfect) |
| `[c]_` | Clear / translucent | **Do not print** — LDO supplies the SB LED diffuser in clear PETG |
| `_x#` suffix | **Quantity required to build the machine** | e.g. `z_joint_lower_x4.stl` → print 4 copies of the file |

The `_x#` number is a *quantity*, not a hint that the file contains that many bodies. I checked every file:
only these contain more than one body — `[a]_stealthburner_main_body` (7 — built-in supports),
`cw2_captive_pcb_cover` (2), `usb_adapter_mount` (2 — mount base + cover), `Leviathan_bracket_set` (2 — L+R),
`bottom_panel_hinge_x2` (2), `cob_light_strip_mount_*` (2 — the mount is a 2-piece assembly),
`V2_Duo_Plenum` (2 — built-in support).
Clicky-Clack's `Hinge-L-sleeve-2X` / `-solid-2X` contain **one** body each — "2X" means print two.

### 1.3 Slicer: PrusaSlicer profile and the Voron overrides

**Slicer:** PrusaSlicer **2.9.6** (current stable, released 2026-06-25 —
[GitHub releases](https://github.com/prusa3d/PrusaSlicer/releases)). 3.0.0-alpha11 shipped 2026-09-01 as an
early preview. **Version posture:** the dimension-critical batches — the B00 gate, B01, and B03–B06 — are sliced on
2.9.6; 3.0 is acceptable for B08–B10 with every override re-entered by hand. Any toolchain change re-runs the
B00 seven-item gate. Deltas and the migration route are in
[`docs/manual/print/00-slicer-setup.md`](manual/print/00-slicer-setup.md#prusaslicer-30-preview).

**Base profiles to select (verified against
[`PrusaResearch.ini` @ version_2.9.6](https://github.com/prusa3d/PrusaSlicer/blob/version_2.9.6/resources/profiles/PrusaResearch.ini)):**

- Printer: **`Prusa CORE One 0.4 nozzle`** (printer model `Prusa CORE One & CORE One+`) — bed `250×220`, max height `270`, retract 0.7 mm @ 45 mm/s, z-hop 0.2 mm, wipe off.
- Filament: **`Prusament ASA @COREONE`** — nozzle 260 °C, bed 110 °C, **chamber 55 °C** (minimum 40 °C), fan 20–25 %, first 4 layers fan off, density 1.07 g/cm³, max volumetric 15 mm³/s.
- Print: **`0.20mm STRUCTURAL @COREONE 0.4`** — *not* SPEED. STRUCTURAL is already the quality-biased profile
  (perimeters 70 mm/s vs SPEED's 170; external 50 vs 170; infill 120 vs 200).

**Overrides.** Column "source" = where the number comes from; **judgment** = my call, not a cited spec.

#### Print settings

| Setting | Prusa STRUCTURAL default | Set to | Why | Source |
|---|---|---|---|---|
| Layer height / first layer | 0.20 / 0.20 | **keep** | Voron spec | [Manual p.4](https://github.com/VoronDesign/Voron-2/blob/Voron2.4/Manual/Assembly_Manual_2.4r2.pdf) |
| Perimeters | 2 | **4** | Voron spec; wall count is what carries load in these parts | Manual p.4 |
| Top solid layers | 5 | **keep 5** | Voron spec | Manual p.4 |
| Bottom solid layers | 4 | **5** | Voron spec says 5 top **and** bottom | Manual p.4 |
| Fill density | 15 % | **40 %** | Voron spec | Manual p.4 |
| Fill pattern | Grid | **keep Grid** | Voron allows grid/gyroid/honeycomb/triangle/cubic | Manual p.4 |
| Extrusion width (default, perimeter, external, infill, solid) | 0.45 | **0.40** | Voron: *"Extrusion width — Recommended: Forced 0.4 mm"*. Ribs, bosses and bearing seats were drawn around a 0.4 bead. | Manual p.4 |
| First layer extrusion width | 0.50 | **keep 0.50** | wider first bead = better ASA adhesion | judgment |
| Top infill extrusion width | 0.42 | **0.40** | consistency | judgment |
| Perimeter generator | Arachne | **keep Arachne** | Voron's "forced 0.4" predates Arachne. Arachne varies bead width *on purpose* and handles Voron's thin ribs better than Classic. Setting nominal width to 0.4 gives Arachne the right target. | judgment |
| Supports | on (auto **off**) | **None** | Every Voron/LDO/Nevermore STL is pre-oriented with built-in break-away supports where needed | Manual; [Nevermore README](https://github.com/nevermore3d/Nevermore_Micro#assembly); [Klicky STL README](https://github.com/jlas1/Klicky-Probe/blob/main/Probes/KlickyProbe/STL/README.md) |
| Seam position | Aligned | **Rear** | keeps the seam off the visible outward faces of skirts and the toolhead | your build spec |
| Skirt loops | 0 | **1 loop, 3 mm gap, min length 4 mm** | primes after the long ASA purge; lets you abort in the first 60 s if the first layer is wrong | judgment |
| Brim | off | **off by default; 5 mm on the tall/narrow parts, 3 mm on the 150–182 mm skirts** — list in §5 | ASA corner lift on long flat parts and tippy tall parts | [Prusa warping KB](https://help.prusa3d.com/article/warping_2011); judgment |
| **XY size compensation** | 0 | **keep 0** | Voron: *"The parts have been designed with ABS/ASA shrinkage in mind… shrinkage should be set to 100 %. Compensating for this is likely to make bearing fits and screw holes too large."* | [docs.vorondesign.com/materials.html](https://docs.vorondesign.com/materials.html) |
| Elephant-foot compensation | 0.20 | **keep 0.20 for now, verify on the cube** | it shrinks only the *first* layer; several Voron parts have a bearing bore starting at the bed. Measure before changing. | judgment |
| External perimeter speed | 50 | **35** | surface finish and corner accuracy on the visible skirts; speed is not a goal here | judgment |
| Perimeter speed | 70 | **55** | more time at temperature per bead = better interlayer bond at 4 walls | judgment |
| Infill speed | 120 | **100** | interior quality and less pressure variation into the perimeters | judgment |
| Solid infill speed | 140 | **110** | flatter top/bottom faces on the skirts | judgment |
| Top solid infill | 80 | **keep 80** | already conservative | — |
| First layer speed | 45 | **25** | ASA on smooth PEI is the single biggest failure mode; slow the first layer | [Prusa ASA KB](https://help.prusa3d.com/article/asa_1809); judgment |
| External perimeters first | off | **keep off** | inside-out gives better dimensional accuracy on holes; only flip it if you see external-perimeter bulging | judgment |
| Dynamic overhang speeds | on (15/25/45/90 %) | **keep on** | Prusa tuned these for the Core One's part fan | — |
| Ironing | off | **keep off** | — | — |

#### Filament settings (Prusament ASA @COREONE)

| Setting | Profile default | Set to | Why | Source |
|---|---|---|---|---|
| **Shrinkage compensation XY** | **0.22 %** | **0 %** | Same rule as XY size compensation — PrusaSlicer 2.9 scales ASA parts up 0.22 %; on a 66.7 mm Z-drive body that is +0.15 mm and it lands straight in the bearing bores. **This is the single most important override in this document.** | [docs.vorondesign.com/materials.html](https://docs.vorondesign.com/materials.html) + profile value |
| Shrinkage compensation Z | 0.22 % | **0 %** | same reason | as above |
| Nozzle / first-layer nozzle | 260 / 260 °C | **keep** | Prusa's own Prusament ASA values for this machine | profile |
| Bed / first-layer bed | 110 / 110 °C | **keep** | Prusa ASA guidance is ≥100 °C bed | profile; [Prusa ASA KB](https://help.prusa3d.com/article/asa_1809) |
| Chamber temperature | 55 °C | **keep 55** | matches the 55–60 °C a real Voron sees; the Voron parts are designed for it | profile; [docs.vorondesign.com/materials.html](https://docs.vorondesign.com/materials.html) |
| Chamber minimal temperature | 40 °C | **keep 40** | printer will not start until the chamber reaches 40 °C — this *is* your preheat gate | profile |
| Min / max fan | 20 / 25 % | **keep for batch 0–1, then decide** | Prusa tuned this for the Core One chamber. If you see perimeter separation on the Z-drive bodies, drop to **0 / 15 %** and keep bridge fan at 25 %. | profile; [Ellis — Perimeter Separation](https://ellis3dp.com/Print-Tuning-Guide/articles/troubleshooting/perimeter_separation.html) |
| Max volumetric speed | 15 mm³/s | **keep** | not a limit at these speeds | profile |
| Retraction / z-hop | 0.7 mm / 0.2 mm | **keep** | Nextruder-specific; do not touch | printer profile |

#### Drying

ASA is mildly hygroscopic. A fresh, sealed Prusament spool used within ~2 weeks needs nothing.
Dry at **80 °C for 4 h** if a spool has been open longer, or the moment you see stringing, matte striping, or
popping. Keep the active spool in one USS Drybox during the run. Voron parts are structural — this is the
material where wet filament actually costs you strength.
(Sources: [Prusa ASA KB](https://help.prusa3d.com/article/asa_1809); your own drying decision in `CLAUDE.md`.)

### 1.4 Calibration sequence — run this before Batch 1, and again after the Gen 2 upgrade

1. **Install the Advanced Filtration Kit first.** You're about to run ~157 h of ASA in an enclosure.
   Do it while the back panel is already off (Ch. 7 of the Core One build), not later.
2. **Firmware ≥ 6.9.0** on the Core One+ (needed for GT1.5 belts later; harmless now).
3. **First-layer Z.** Run Prusa's built-in First Layer Calibration *with ASA loaded and the chamber at 40 °C+* —
   ASA's first layer behaves differently from PLA's. Then fine-tune squish by
   [Ellis' smooth-bottom method](https://ellis3dp.com/Print-Tuning-Guide/articles/first_layer_squish.html):
   the bottom should be smooth with no visible gaps between beads and no ridging.
4. **Print plate B00-P1** (§3). It contains the gate parts.
5. **Measure with the calipers, at mid-height (not across the first layer):**

   | Coupon | Nominal | Accept | If out of spec |
   |---|---|---|---|
   | `Voron_Design_Cube_v7` X and Y | 30.00 mm | **±0.15 mm** | >+0.15: confirm shrinkage compensation is 0 % and XY compensation is 0. Still over → reduce extrusion multiplier in 1 % steps ([Ellis — Extrusion Multiplier](https://ellis3dp.com/Print-Tuning-Guide/articles/extrusion_multiplier.html)). Do **not** dial in negative XY compensation; you will wreck the bearing fits. |
   | `Voron_Design_Cube_v7` Z | 30.00 mm | **±0.10 mm** | over → first layer under-squished; under → over-squished |
   | Cube first layer vs mid-height X | — | difference **≤ 0.15 mm** | bigger → elephant-foot compensation is wrong; adjust in 0.05 mm steps |
   | Cube corner snap test | — | must **not** delaminate along a layer line | delamination → chamber too cold or fan too high → drop min/max fan to 0/15 % |
   | `Heatset_Practice` | 3 × M3×5×4 inserts | insert sits flush to 0.2 mm proud, boss does not bulge > 0.2 mm | bulging → iron too hot or pushed too fast; this is a technique problem, not a slicer one. This coupon is the daughter's practice part — do all three before touching a real part. |
   | `MGN12_rail_guide` on the real MGN12 rail | — | slides on with light finger pressure | very tight → over-extrusion; loose → under-extrusion |
   | `z_drive_retainer_a` 625-2RS bore (on the same plate) | 16.00 mm bearing (625-2RS; F695 is the A/B-drive bearing, not the Z drive) | bearing presses in with thumb pressure, no rocking | **This is the real press-fit gate.** Loose → check shrinkage compensation is 0 %. Tight → reduce EM 1 %, do not enlarge with compensation. |

6. Only when all seven pass, start Batch 1.

**Quality gate before every later batch:** look at the *last* plate you pulled off. If any part shows
(a) a lifted corner, (b) a delaminated layer, or (c) a bore/boss that failed a test fit — fix that before
starting the next plate, don't print 100 g on top of a known problem.

---

## 2. Which parts gate the frame and Z-drive steps

**Frame** (Assembly Manual ch. *Frame*, p.12–21): **no printed part is required.** The frame is extrusion,
corner brackets and hardware. You can square the frame the day the kit lands.

**Z rails** (p.24–27, inside ch. *Z Drives and Idlers*): the only printed items are the optional-but-worth-it
alignment jigs — `MGN12_rail_guide_x2` ×2 and `MGN9_rail_guide_x2` ×2. Both are on plate **B00-P1**.

**Z Drives and Idlers** (p.22–51) — the first step that genuinely stops without plastic. It needs:

- all of **Batch 1** (Z-drive bodies, retainers, motor mounts, Z-tensioner brackets, deck supports), **and**
- these accent parts from **Batch 2**: `[a]_z_drive_baseplate_a/b` ×2 each, `[a]_belt_tensioner_a/b` ×2 each,
  `[a]_z_tensioner_9mm_x4` ×4.

So the minimum to start building is **B00 + B01 + B02-P1 + B02-P3** ≈ 34 h of printing.
Everything else can be printed while you build.

**Tall parts (> 150 mm in Z): none.** The tallest part in the whole set is the Clicky-Clack `Handle` at
**60.0 mm**. Orientation rules that do matter are in §5.

---

## 3. The batches

Format for each: what it unlocks (manual chapter name), plates, hours, grams, then the parts table
(exact filenames, repo path, qty, colour, grams and hours per copy).

**Batch headers and plate lines are PrusaSlicer 2.9.6 estimates** — sliced from the committed projects in
`slicer/plates/`, with this build's overrides, the real arrangement and the real brims (§4.1). The per-copy
`g ea` / `h ea` columns inside the parts tables are still the older geometry model, kept for relative sizing
only; they do not sum to the plate line, which also carries skirt, brim and travel.

---

### Batch B00 — Calibration & jigs · **1 plate · 4.0 h · 52 g black**
**Unlocks:** *Frame* (rail installation aids) — and gates every batch after it.

| STL | Repo path | Qty | Colour | g ea | h ea |
|---|---|---:|---|---:|---:|
| `Voron_Design_Cube_v7.stl` | Voron-2 `STLs/Test_Prints/` | 1 | Black | 16.2 | 0.98 |
| `Heatset_Practice.stl` | Voron-2 `STLs/Test_Prints/` | 1 | Black | 6.5 | 0.39 |
| `MGN12_rail_guide_x2.stl` | Voron-2 `STLs/Tools/` | 2 | Black | 3.2 | 0.20 |
| `MGN9_rail_guide_x2.stl` | Voron-2 `STLs/Tools/` | 2 | Black | 2.7 | 0.17 |
| `pulley_jig.stl` | Voron-2 `STLs/Tools/` | 1 | Black | 2.8 | 0.17 |
| `z_drive_retainer_a_x2.stl` | Voron-2 `STLs/Z_Drive/` | 1 *(of the 2 needed)* | Black | 19.5 | 1.15 |

**Plate B00-P1** — all of the above. 4.0 h, 52 g.
The `z_drive_retainer_a` here is deliberate: it is your bearing-press-fit coupon, and it is a real part you
will use, so nothing is wasted.

---

### Batch B01 — Z drive assemblies · **2 plates · 22.8 h · 301 g black**
**Unlocks:** *Z Drives and Idlers* (p.22–51) and the deck-panel step (p.28–30).

| STL | Repo path | Qty | Colour | g ea | h ea |
|---|---|---:|---|---:|---:|
| `z_drive_main_a_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | Black | 39.4 | 2.31 |
| `z_drive_main_b_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | Black | 39.4 | 2.31 |
| `z_drive_retainer_a_x2.stl` | Voron-2 `STLs/Z_Drive/` | 1 *(second copy; first was on B00)* | Black | 19.5 | 1.15 |
| `z_drive_retainer_b_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | Black | 19.5 | 1.15 |
| `z_motor_mount_a_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | Black | 11.9 | 0.75 |
| `z_motor_mount_b_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | Black | 11.9 | 0.75 |
| `z_tensioner_bracket_a_x2.stl` | Voron-2 `STLs/Z_Idlers/` | 2 | Black | 13.0 | 0.79 |
| `z_tensioner_bracket_b_x2.stl` | Voron-2 `STLs/Z_Idlers/` | 2 | Black | 13.0 | 0.79 |
| `deck_support_3mm_x8.stl` | Voron-2 `STLs/Panel_Mounting/` | 8 | Black | 1.1 | 0.07 |

- **Plate B01-P1** (15.2 h, 201 g): `z_drive_main_a` ×2, `z_drive_main_b` ×2, `z_drive_retainer_a` ×1, `z_drive_retainer_b` ×2.
  Longest plate in the build — start it in the morning, not at bedtime.
- **Plate B01-P2** (7.6 h, 100 g): `z_motor_mount_a` ×2, `z_motor_mount_b` ×2, `z_tensioner_bracket_a` ×2, `z_tensioner_bracket_b` ×2, `deck_support_3mm` ×8.

**Deck supports (verify):** LDO's Rev D printed-parts guide says *"Our kit ships with 4 mm deck panels, use 4 mm
deck support clips"*, but the Rev D 350 BOM lists the deck panel as **3 mm** acrylic (the 4 mm panel is the
*bottom* panel). The size-specific 350 BOM wins: print `deck_support_3mm_x8` ×8, and if the deck panel
measures 4 mm when it arrives, reprint `deck_support_4mm_x8` — 8 g, 30 minutes.
([guide](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d), [BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D), [Build Notes p.29-30](https://docs.ldomotors.com/voron/voron2/build-faq))

---

### Batch B02 — **The orange day** (every accent part in the build) · **3 plates · 21.8 h · 279 g orange**
**Unlocks:** the accent half of *Z Drives and Idlers*, *A/B Drives and Idlers*, *Gantry*, *Stealthburner*,
*Skirts* and the Clicky-Clack door.

All 49 accent parts are printed in one continuous orange session so the accent spool is mounted exactly
once. **Two colour changes in the whole build: black → orange here, orange → black after.**
Everything is printed before the kit arrives anyway, so nothing waits on this.

| STL | Repo path | Qty | g ea | h ea |
|---|---|---:|---:|---:|
| `[a]_z_drive_baseplate_a_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | 9.7 | 0.57 |
| `[a]_z_drive_baseplate_b_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | 9.7 | 0.57 |
| `[a]_belt_tensioner_a_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | 1.9 | 0.12 |
| `[a]_belt_tensioner_b_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | 1.9 | 0.12 |
| `[a]_z_tensioner_9mm_x4.stl` | Voron-2 `STLs/Z_Idlers/` | 4 | 8.1 | 0.49 |
| `[a]_tensioner_left.stl` | Voron-2 `STLs/Gantry/Front_Idlers/` | 1 | 7.4 | 0.45 |
| `[a]_tensioner_right.stl` | Voron-2 `STLs/Gantry/Front_Idlers/` | 1 | 7.4 | 0.45 |
| `[a]_cable_cover.stl` | Voron-2 `STLs/Gantry/AB_Drive_Units/` | 1 | 8.0 | 0.51 |
| `[a]_z_chain_retainer_bracket_x2.stl` | Voron-2 `STLs/Gantry/AB_Drive_Units/` | 2 | 0.6 | 0.04 |
| `[a]_endstop_pod_D2F_switch.stl` | Voron-2 `STLs/Gantry/X_Axis/XY_Joints/` | 1 | 8.1 | 0.49 |
| `[a]_xy_joint_cable_bridge_2hole.stl` | Voron-2 `STLs/Gantry/X_Axis/XY_Joints/` | 1 | 9.2 | 0.56 |
| `XY_cable_chain_bridge-Igus-3mm_backer.stl` | whopping\_Voron\_mods `extrusion_backers/STLs/` | 1 *(alternate — see §6)* | 9.1 | 0.58 |
| `[a]_z_belt_clip_lower_x4.stl` | Voron-2 `STLs/Gantry/` | 4 | 2.3 | 0.14 |
| `[a]_z_belt_clip_upper_x4.stl` | Voron-2 `STLs/Gantry/` | 4 | 2.4 | 0.14 |
| `[a]_stealthburner_main_body.stl` | Stealthburner `STLs/Stealthburner/` | 1 | 46.5 | 2.73 |
| `[a]_guidler_a.stl` | Stealthburner `STLs/Clockwork2/Direct_Drive/` | 1 | 3.7 | 0.24 |
| `[a]_guidler_b.stl` | Stealthburner `STLs/Clockwork2/Direct_Drive/` | 1 | 2.1 | 0.14 |
| `[a]_latch.stl` | Stealthburner `STLs/Clockwork2/Direct_Drive/` | 1 | 3.5 | 0.22 |
| `[a]_latch_shuttle.stl` | Stealthburner `STLs/Clockwork2/Direct_Drive/` | 1 | 1.7 | 0.11 |
| `[a]_pcb_spacer.stl` | Stealthburner `STLs/Clockwork2/` | 1 *(spare — kit supplies one)* | 0.3 | 0.02 |
| `[a]_belt_guard_a_x2.stl` | Voron-2 `STLs/Skirts/` | 2 | 5.4 | 0.33 |
| `[a]_belt_guard_b_x2.stl` | Voron-2 `STLs/Skirts/` | 2 | 5.4 | 0.33 |
| `[a]_fan_grill_a_x2.stl` | Voron-2 `STLs/Skirts/` | 2 | 5.9 | 0.34 |
| `[a]_fan_grill_b_x2.stl` | Voron-2 `STLs/Skirts/` | 2 | 5.9 | 0.34 |
| `[a]_fan_grill_retainer_x2.stl` | Voron-2 `STLs/Skirts/` | 2 | 4.2 | 0.25 |
| `[a]_keystone_blank_insert.stl` | Voron-2 `STLs/Skirts/` | 2 *(1 used + 1 spare; LDO ships one CAT6 keystone)* | 2.5 | 0.16 |
| `[a]_faceplate.stl` | LDOVoronTrident `STLs/BTT Pi TFT4.3 Mount/` | 1 | 6.6 | 0.41 |
| `ldo_bestagon_insert.stl` | LDOVoron2 `STLs/` | 1 | 3.0 | 0.18 |
| `Handle.stl` | whopping\_Voron\_mods `clickyclacky_door/STLs/` | 1 | 33.7 | 2.03 |

- **Plate B02-P1** (7.0 h, 90 g): `[a]_stealthburner_main_body`, `[a]_faceplate`, `[a]_cable_cover`, `[a]_z_drive_baseplate_a` ×2, `[a]_z_drive_baseplate_b` ×2.
- **Plate B02-P2** (7.3 h, 93 g): `Handle`, `[a]_fan_grill_a` ×2, `[a]_fan_grill_b` ×2, `[a]_fan_grill_retainer` ×2, `[a]_belt_guard_a` ×2, `[a]_belt_guard_b` ×2, `[a]_tensioner_left`, `[a]_tensioner_right`.
- **Plate B02-P3** (7.6 h, 96 g): everything else — the 29 small accent parts.

Notes: the SB main body has **built-in supports** — snap them out, don't cut
([SB manual, "Remove built-in supports"](https://github.com/VoronDesign/Voron-Stealthburner/blob/main/Manual/Assembly_Manual_SB.pdf)).
`Handle.stl` is 60 mm tall on a 68×19 footprint — give it a 5 mm brim (§5).

---

### Batch B03 — A/B drive units + front idlers · **2 plates · 8.5 h · 119 g black**
**Unlocks:** *A/B Drives and Idlers* (p.62–81).

| STL | Repo path | Qty | Colour | g ea | h ea |
|---|---|---:|---|---:|---:|
| `a_drive_frame_lower.stl` | Voron-2 `STLs/Gantry/AB_Drive_Units/` | 1 | Black | 22.4 | 1.32 |
| `a_drive_frame_upper.stl` | Voron-2 `STLs/Gantry/AB_Drive_Units/` | 1 | Black | 21.8 | 1.28 |
| `b_drive_frame_lower.stl` | Voron-2 `STLs/Gantry/AB_Drive_Units/` | 1 | Black | 20.5 | 1.21 |
| `b_drive_frame_upper.stl` | Voron-2 `STLs/Gantry/AB_Drive_Units/` | 1 | Black | 21.3 | 1.25 |
| `front_idler_left_lower.stl` | Voron-2 `STLs/Gantry/Front_Idlers/` | 1 | Black | 7.7 | 0.46 |
| `front_idler_left_upper.stl` | Voron-2 `STLs/Gantry/Front_Idlers/` | 1 | Black | 14.1 | 0.84 |
| `front_idler_right_lower.stl` | Voron-2 `STLs/Gantry/Front_Idlers/` | 1 | Black | 13.8 | 0.83 |
| `front_idler_right_upper.stl` | Voron-2 `STLs/Gantry/Front_Idlers/` | 1 | Black | 7.9 | 0.47 |

- **Plate B03-P1** (4.4 h, 61 g): the **A** side — `a_drive_frame_lower`, `a_drive_frame_upper`, `front_idler_right_lower`, `front_idler_right_upper`.
- **Plate B03-P2** (4.1 h, 59 g): the **B** side — `b_drive_frame_lower`, `b_drive_frame_upper`, `front_idler_left_lower`, `front_idler_left_upper`.

Splitting A and B onto separate plates is not just packing — it means a failed plate costs you one drive unit,
not both, and you can build the A side while the B side prints.

---

### Batch B04 — XY joints + X carriage · **1 plate · 8.6 h · 117 g black**
**Unlocks:** *Gantry* (p.82–107).

| STL | Repo path | Qty | Colour | g ea | h ea |
|---|---|---:|---|---:|---:|
| `xy_joint_left_lower_MGN12.stl` | Voron-2 `STLs/Gantry/X_Axis/XY_Joints/` | 1 | Black | 32.0 | 1.90 |
| `xy_joint_left_upper_MGN12.stl` | Voron-2 `STLs/Gantry/X_Axis/XY_Joints/` | 1 | Black | 11.7 | 0.70 |
| `xy_joint_right_lower_MGN12.stl` | Voron-2 `STLs/Gantry/X_Axis/XY_Joints/` | 1 | Black | 32.7 | 1.94 |
| `xy_joint_right_upper_MGN12.stl` | Voron-2 `STLs/Gantry/X_Axis/XY_Joints/` | 1 | Black | 11.1 | 0.67 |
| `x_frame_V2TR_MGN12_left.stl` | Voron-2 `STLs/Gantry/X_Axis/X_Carriage/` | 1 | Black | 17.1 | 1.02 |
| `x_frame_V2TR_MGN12_right.stl` | Voron-2 `STLs/Gantry/X_Axis/X_Carriage/` | 1 | Black | 17.2 | 1.03 |
| `probe_retainer_bracket.stl` | Voron-2 `STLs/Gantry/X_Axis/X_Carriage/` | 1 | Black | 0.5 | 0.03 |

**Plate B04-P1** — all seven. 8.6 h, 117 g.

`probe_retainer_bracket` is only used if you run the Omron inductive probe. It costs 0.5 g — print it, decide later.
If the probe barrel measures 9 mm rather than 8 mm, print `probe_retainer_bracket_9mm.stl` instead **(verify on arrival)**.
`x_frame_V2TR_MGN12_*` are the R2 / Clockwork-2 carriage halves — LDO Build Notes p.129-130 warn specifically about
using the wrong X-carriage here.

---

### Batch B05 — Z joints + Z chain · **1 plate · 6.4 h · 78 g black**
**Unlocks:** *Z Axis* (p.108–123) and *A/B Belts* (p.124–145).

| STL | Repo path | Qty | Colour | g ea | h ea |
|---|---|---:|---|---:|---:|
| `z_joint_lower_x4.stl` | Voron-2 `STLs/Gantry/Z_Joints/` | 4 | Black | 9.1 | 0.56 |
| `z_joint_upper_x4.stl` | Voron-2 `STLs/Gantry/Z_Joints/` | 4 | Black | 6.6 | 0.41 |
| `z_chain_bottom_anchor.stl` | Voron-2 `STLs/Gantry/` | 1 | Black | 9.1 | 0.55 |
| `z_chain_guide.stl` | Voron-2 `STLs/Gantry/` | 1 | Black | 6.0 | 0.37 |
| `z_rail_stop_x4.stl` | LDOVoron2 `STLs/` | 4 | Black | 1.4 | 0.11 |

**Plate B05-P1** — all fourteen. 6.4 h, 78 g.

Print **4× `z_joint_upper_x4`** and **zero** `z_joint_upper_hall_effect.stl` — that variant exists only for
hall-effect XY endstops, which this kit does not use
([LDO Build Notes p.145](https://docs.ldomotors.com/voron/voron2/build-faq)).
The LDO `z_rail_stop` is optional but stops a Z carriage from falling off the top of a rail and spilling its balls.

---

### Batch B06 — Toolhead: Stealthburner, Clockwork 2, Klicky · **2 plates · 12.2 h · 148 g black**
**Unlocks:** *Stealthburner* (p.146–147, then the separate Stealthburner manual). Also requires
`probe_retainer_bracket.stl` from B04.

| STL | Repo path | Qty | Colour | g ea | h ea |
|---|---|---:|---|---:|---:|
| `stealthburner_printhead_revo_voron_front.stl` | Stealthburner `STLs/Stealthburner/Printheads/revo_voron/` | 1 | Black | 40.6 | 2.38 |
| `stealthburner_printhead_revo_voron_rear_cw2.stl` | Stealthburner `STLs/Stealthburner/Printheads/revo_voron/` | 1 | Black | 15.0 | 0.90 |
| `[o]_stealthburner_LED_carrier.stl` | Stealthburner `STLs/Stealthburner/` | 1 | Black (opaque) | 0.9 | 0.06 |
| `[o]_stealthburner_LED_diffuser_mask.stl` | Stealthburner `STLs/Stealthburner/` | 1 | Black (opaque) | 0.3 | 0.03 |
| `main_body.stl` (Clockwork 2) | Stealthburner `STLs/Clockwork2/Direct_Drive/` | 1 | Black | 23.7 | 1.40 |
| `motor_plate.stl` (Clockwork 2) | Stealthburner `STLs/Clockwork2/Direct_Drive/` | 1 | Black | 14.1 | 0.83 |
| `cw2_captive_pcb_cover.stl` | Nitehawk-SB `STLs/` | 1 | Black | 10.9 | 0.69 |
| `KlickyProbe_v2.stl` | Klicky `Probes/KlickyProbe/STL/` | 2 *(1 + spare, per the mod's own advice)* | Black | 2.5 | 0.16 |
| `Probe_Dock_v2.1.stl` | Klicky `Probes/KlickyProbe/STL/` | 1 | Black | 3.1 | 0.19 |
| `Probe_magnet_holder.stl` | Klicky `Probes/KlickyProbe/STL/` | 1 | Black | 2.3 | 0.14 |
| `Probe_magnet_pressfit_helper.stl` | Klicky `Probes/KlickyProbe/STL/` | 1 | Black | 1.6 | 0.10 |
| `Probe_pressfit_holder.stl` | Klicky `Probes/KlickyProbe/STL/` | 1 | Black | 4.6 | 0.29 |
| `KlickyProbe_AB_mount_v2.stl` | Klicky `Printers/Voron/v1.8_v2.4_Legacy_Trident/v1.8_v2.4_Legacy_Trident_STL/` | 1 | Black | 4.4 | 0.29 |
| `KlickyProbe_AB_mount_v2_holder.stl` | Klicky (same folder) | 1 | Black | 1.6 | 0.10 |
| `Mount_magnet_holder.stl` | Klicky (same folder) | 1 | Black | 2.3 | 0.14 |
| `Mount_magnet_pressfit_helper.stl` | Klicky (same folder) | 1 | Black | 1.6 | 0.10 |
| `Mount_pressfit_holder_v2.stl` | Klicky (same folder) | 1 | Black | 6.6 | 0.42 |
| `Dock_mount_fixed_v2.stl` | Klicky (same folder) | 1 | Black | 22.7 | 1.36 |

- **Plate B06-P1** (8.0 h, 97 g): the Stealthburner + Clockwork 2 black parts.
- **Plate B06-P2** (4.2 h, 51 g): the whole Klicky set.

Notes:
- **Hotend file choice is settled:** E3D Revo Voron → the `revo_voron` folder, `..._rear_cw2` for Clockwork 2
  ([SB printhead README](https://github.com/VoronDesign/Voron-Stealthburner/blob/main/STLs/Stealthburner/Printheads/README.md)).
- **Do not print an ADXL mount** — the Nitehawk-SB has one on board
  ([LDO Rev D guide](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d)).
- **Do not print the CW2 chain anchor** — the kit supplies "CW2 Chain Anchor Tilted" printed
  ([Rev D 350 BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)).
- `cw2_captive_pcb_cover` is LDO's improved cable door (captive screw + external chamber thermistor); the stock
  alternative is `Clockwork2/cable_door_for_pcb.stl` if you'd rather.
- Klicky dock: **fixed** mount chosen for simplicity. If you later add the Decontaminator purge bucket, you need
  `Dock_sidemount_fixed_v2.stl` + `Dock_sidemount_left_v2.stl` instead (~25 g, 1.5 h).
- The `Probe_*_pressfit_helper` / `_holder` parts are jigs for pressing the 6×3 magnets in square. Print them —
  a crooked magnet is a probe that doesn't repeat.
  ([Klicky "What to print"](https://github.com/jlas1/Klicky-Probe/tree/main/Printers/Voron/v1.8_v2.4_Legacy_Trident))

---

### Batch B07 — Electronics bay + lighting · **3 plates · 16.0 h · 226 g black**
**Unlocks:** *Electronics* (p.148–173), *Controller* (p.174–179), *Wiring* (p.180–211).

| STL | Repo path | Qty | Colour | g ea | h ea |
|---|---|---:|---|---:|---:|
| `wago_221-415_mount_3by5.stl` | Voron-2 `STLs/Electronics_Bay/` | 1 | Black | 10.6 | 0.63 |
| `lrs_200_psu_bracket_x2.stl` | Voron-2 `STLs/Electronics_Bay/` | 2 | Black | 8.2 | 0.49 |
| `PSU_stabilizer_50mm.stl` | Voron-2 `STLs/Electronics_Bay/` | 1 **(verify)** | Black | 4.1 | 0.26 |
| `usb_adapter_mount.stl` | Nitehawk-SB `STLs/` | 1 file *(contains base **and** cover; kit supplies the base, so you get a spare; base only — cover body superseded by the V2 partial cover below)* | Black | 9.4 | 0.55 |
| `usb_adapter_mount_partial_cover.stl` | Nitehawk-SB-V2 `STLs/` | 1 | Black | 5.0 (est.) | 0.30 (est.) |
| `pcb_din_clip_x3.stl` | Voron-2 `STLs/Electronics_Bay/` | 3 *(one clip per file; spares — the kit supplies the 4 needed)* | Black | 5.9 | 0.35 |
| `handlebar_spacer_x4.stl` | LDOVoron2 `STLs/` | 4 | Black | 2.1 | 0.13 |
| `cob_light_strip_mount_100mm.stl` | LDOVoron2 `STLs/COB Light Strip/` | 6 | Black | 18.1 | 1.06 |
| `cob_light_strip_mount_50mm.stl` | LDOVoron2 `STLs/COB Light Strip/` | 2 | Black | 9.3 | 0.55 |
| `power_inlet_IECGS_1mm.stl` | Voron-2 `STLs/Skirts/` | 1 *(moved from B08 — consumed in Ch 09, p.156/167, not the skirts chapter; own plate B07-P3)* | Black | 36.2 | 2.11 |

- **Plate B07-P1** (5.6 h, 67 g): wago mount, PSU brackets ×2, PSU stabilizer, USB adapter mount, `usb_adapter_mount_partial_cover` (ground-lug mount, est.), DIN clips, handlebar spacers ×4.
- **Plate B07-P2** (8.2 h, 124 g): the eight COB light-strip mounts, brimmed. Nothing else fits.
- **Plate B07-P3** (2.3 h, 35 g): `power_inlet_IECGS_1mm` alone, 3 mm brim.

Notes:
- COB counts are LDO's own for a 2.4-350: **6× 100 mm + 2× 50 mm**
  ([COB README](https://github.com/MotorDynamicsLab/LDOVoron2/tree/main/STLs/COB%20Light%20Strip)).
  Each STL contains a 2-piece assembly joined with 2× M3 heat-sets + 2× M3×6 FHCS. This is the heaviest
  single group of "small" parts in the build — 127 g.
- `PSU_stabilizer_50mm` is marked **(verify)**: LDO Build Notes say *"PAGE 169 SKIP — the kit does not use a
  support bracket"*, which most likely refers to this part. It is 4 g; print it and only fit it if it's needed.
- **Do not print** `raspberrypi_bracket.stl`, `beefy_raspberry_bracket.stl` or `rs25_psu_bracket.stl` — Leviathan
  carries the Pi and there is no 5 V PSU in this kit
  ([Build Notes p.150, p.152](https://docs.ldomotors.com/voron/voron2/build-faq)).
- **Do not print** the Leviathan bracket set or the bed WAGO mount — both supplied printed.
- `power_inlet_IECGS_1mm` lives here, not in B08, because it's fitted in Ch 09 (p.156/167) — see `docs/manual/09-electronics-bay.md`.
- It needs its **own plate (B07-P3)**: with the mandated 3 mm brims the eight COB mounts plus the 118 × 66.8 mm
  inlet come to 46 280 mm², 84 % of the 250 × 220 bed, and no placement exists.

---

### Batch B08 — Skirts and front modules · **6 plates · 29.1 h · 399 g black**
**Unlocks:** *Skirts* (p.212–239).

The skirt ring is made of ten structural segments plus two "module" pieces — the TFT mount and the power
inlet — that all share a 67–72 × 20 mm cross-section. On the 350 the ring works out as:
front = `front_skirt_a` + **TFT mount** + `front_skirt_b`; rear = `rear_center_skirt` + `power_inlet` + `keystone_panel`;
each side = `side_skirt_a` + `side_fan_support` + `side_skirt_b`.

| STL | Repo path | Qty | Colour | g ea | h ea |
|---|---|---:|---|---:|---:|
| `rear_center_skirt_350.stl` | Voron-2 `STLs/Skirts/350/` | 1 | Black | 71.9 | 4.18 |
| `front_skirt_a_350.stl` | Voron-2 `STLs/Skirts/350/` | 1 | Black | 41.4 | 2.42 |
| `front_skirt_b_350.stl` | Voron-2 `STLs/Skirts/350/` | 1 | Black | 41.4 | 2.42 |
| `side_skirt_a_350_x2.stl` | Voron-2 `STLs/Skirts/350/` | 2 | Black | 36.9 | 2.16 |
| `side_skirt_b_350_x2.stl` | Voron-2 `STLs/Skirts/350/` | 2 | Black | 36.9 | 2.16 |
| `side_fan_support_x2.STL` | Voron-2 `STLs/Skirts/` | 2 | Black | 33.0 | 1.93 |
| `keystone_panel.stl` | Voron-2 `STLs/Skirts/` | 1 | Black | 38.6 | 2.26 |
| `mount.stl` (BTT Pi TFT4.3) | LDOVoronTrident `STLs/BTT Pi TFT4.3 Mount/` | 1 | Black | 30.1 | 1.80 |

- **B08-P1** (6.3 h, 99 g): `rear_center_skirt_350`, `side_fan_support` ×1
- **B08-P2** (5.0 h, 67 g): `side_fan_support` ×1, `front_skirt_a_350`
- **B08-P3** (5.5 h, 71 g): `front_skirt_b_350`, `side_skirt_a_350` ×1
- **B08-P4** (5.1 h, 66 g): `side_skirt_a_350` ×1, `side_skirt_b_350` ×1
- **B08-P5** (5.0 h, 70 g): `side_skirt_b_350` ×1, `keystone_panel`
- **B08-P6** (2.3 h, 26 g): `mount.stl` — `power_inlet_IECGS_1mm` moved to B07 (Ch 09, not the skirts chapter)

Only two of these long parts fit per plate — every one is 118–182 mm on its long axis and 67–72 mm deep, so a
250 × 220 bed takes two per plate with a workable gap. **These are the parts people see.** Print them after the
Gen 2 belt upgrade if you have it (§8).

Notes:
- `mount.stl` vs `mount_thick.stl`: `mount.stl` is 30 g / 44.8 mm tall; `mount_thick.stl` is 74 g / 67.8 mm and
  gives access to the screen's brightness buttons with a pointy tool. `mount.stl` is the recommendation —
  swap if you find you want the buttons **(judgment; LDO links the folder, not a specific file)**
  ([mount README](https://github.com/MotorDynamicsLab/LDOVoronTrident/tree/master/STLs/BTT%20Pi%20TFT4.3%20Mount)).
- **Do not print** `mini12864_case_front/rear`, `[a]_mini12864_case_hinge`, `[a]_mini12864_case_front_insert`,
  `[a]_btt_knob_light_shield` — the touchscreen mount replaces that whole front module
  ([LDO Rev D guide](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d)).
- Optional: `[a]_fan_grill_open_optional_x2` (more airflow, less filtering) instead of `[a]_fan_grill_a/b`;
  `ldo_bestagon_insert` (in B02) snaps into the skirt hexagons — print more copies if you like the look.

---

### Batch B09 — Panels, filtration, spool · **5 plates · 21.9 h · 296 g black**
**Unlocks:** *Panels* (p.240–259) and the Nevermore install.

| STL | Repo path | Qty | Colour | g ea | h ea |
|---|---|---:|---|---:|---:|
| `corner_panel_clip_4mm_x8.stl` | Voron-2 `STLs/Panel_Mounting/` | 8 | Black | 3.0 | 0.18 |
| `midspan_panel_clip_4mm_x7.stl` | Voron-2 `STLs/Panel_Mounting/` | 7 | Black | 2.0 | 0.12 |
| `corner_panel_clip_6mm_x8.stl` | Voron-2 `STLs/Panel_Mounting/` | 8 | Black | 4.5 | 0.27 |
| `midspan_panel_clip_6mm_x8.stl` | Voron-2 `STLs/Panel_Mounting/` | 8 | Black | 2.9 | 0.18 |
| `bottom_panel_clip_x4.stl` | Voron-2 `STLs/Panel_Mounting/` | 4 | Black | 3.2 | 0.19 |
| `bottom_panel_hinge_x2.stl` | Voron-2 `STLs/Panel_Mounting/` | 2 | Black | 4.3 | 0.26 |
| `z_belt_cover_a_x2.stl` | Voron-2 `STLs/Panel_Mounting/` | 2 | Black | 6.9 | 0.40 |
| `z_belt_cover_b_x2.stl` | Voron-2 `STLs/Panel_Mounting/` | 2 | Black | 6.9 | 0.40 |
| `exhaust_cover.stl` | LDOVoron2 `STLs/` | 1 | Black | 30.2 | 1.76 |
| `exhaust_filter_grill.stl` | Voron-2 `STLs/Exhaust_Filter/` | 1 | Black | 9.9 | 0.58 |
| `V2_Duo_Plenum.stl` | Nevermore\_Micro `V5_Duo/V2/` | 1 | Black | 50.2 | 2.93 |
| `V2_Duo_Plenum_LID.stl` | Nevermore\_Micro `V5_Duo/V2/` | 1 | Black | 12.3 | 0.71 |
| `Regular_Cartridge(contributed_by_Bucknova).3mf` | Nevermore\_Micro `V5_Duo/V2/` | 1 | Black | 43.0 | 2.51 |
| `Regular_Cartridge_Lid(contributed_by_Bucknova).3mf` | Nevermore\_Micro `V5_Duo/V2/` | 1 | Black | 8.4 | 0.49 |
| `spool_holder.stl` | Voron-2 `STLs/Spool_Management/` | 1 | Black | 16.6 | 0.98 |
| `bowden_retainer.stl` | Voron-2 `STLs/Spool_Management/` | 1 | Black | 5.6 | 0.33 |

- **B09-P1** (4.6 h, 63 g): `V2_Duo_Plenum`, `V2_Duo_Plenum_LID`, `Regular_Cartridge_Lid`
- **B09-P2** (4.9 h, 67 g): `Regular_Cartridge`, `exhaust_cover`
- **B09-P3** (3.9 h, 55 g): `exhaust_filter_grill`, `spool_holder`, `bowden_retainer`, `z_belt_cover_a` ×2, `z_belt_cover_b` ×2
- **B09-P4** (4.2 h, 56 g): `corner_panel_clip_4mm` ×8, `midspan_panel_clip_4mm` ×7, `bottom_panel_hinge` ×2, `bottom_panel_clip` ×4
- **B09-P5** (4.3 h, 56 g): `corner_panel_clip_6mm` ×8, `midspan_panel_clip_6mm` ×8

**Why both 4 mm and 6 mm panel clips.** The manual mounts back and top panels with **1 mm foam tape**
(3 mm panel + 1 mm tape = 4 mm) and side panels with **3 mm foam tape** (3 + 3 = 6 mm, *"to prevent the gantry
from rubbing on the panels"*). Counting the clips in the manual's own illustrations: back panel 4 corner + 3
midspan, top panel 4 corner + 4 midspan → exactly the `_4mm_x8` / `_4mm_x7` quantities; each side panel 4 corner
+ 4 midspan → exactly the `_6mm_x8` / `_6mm_x8` quantities. (Manual p.239–244; the `_x#` filename suffix is the
authoritative count.)
**This mapping is an inference** — neither Voron nor LDO states which clip goes on which panel. The arithmetic
lands exactly, so I'm confident, but snap one clip of each thickness onto an extrusion with a 3 mm panel offcut
and the right foam tape before you commit to printing all 31.

**Nevermore V5 Duo, exactly which files.** The Voron-2 plenum/lid are STLs; the **cartridge and its lid are
3MF files** in the same folder (PrusaSlicer imports them fine). Use the **Regular** cartridge, not XL — XL wants
carbon pellets and a faster/louder fan. 8× 6×3 mm magnets, 6× M3 heat-sets. The cartridge has a **built-in
support you push out**. ([Nevermore README](https://github.com/nevermore3d/Nevermore_Micro),
[LDO Nevermore guide](https://ldomotion.com/guides/nevermore-v5-duo---v24))

**Exhaust:** you are *not* building the Voron exhaust filter (76 g, 4.5 h saved). LDO: *"print this exhaust cover
with the stock exhaust grill to seal the back panel"* — that is `exhaust_cover.stl` (LDO) + `exhaust_filter_grill.stl`
(Voron). Skip `exhaust_filter_housing`, `[a]_exhaust_filter_mount_x2`, `[a]_filter_access_cover`, `[a]_exhaust_fan_grill`.

---

### Batch B10 — Clicky-Clack door · **1 plate · 5.7 h · 76 g black** (+ the orange `Handle` from B02)
**Unlocks:** front door install, replacing the stock two-door assembly entirely.

| STL | Repo path | Qty | Colour | g ea | h ea |
|---|---|---:|---|---:|---:|
| `Handle-Hinge_Bottom.stl` | whopping\_Voron\_mods `clickyclacky_door/STLs/` | 1 | Black | 17.1 | 1.03 |
| `Handle-Hinge_Top.stl` | whopping\_Voron\_mods `clickyclacky_door/STLs/` | 1 | Black | 17.1 | 1.03 |
| `Hinge-L-sleeve-2X.stl` | whopping\_Voron\_mods `clickyclacky_door/STLs/` | **2** | Black | 9.0 | 0.60 |
| `Hinge-L-solid-2X.stl` | whopping\_Voron\_mods `clickyclacky_door/STLs/` | **2** | Black | 9.2 | 0.61 |
| `Latch.stl` | whopping\_Voron\_mods `clickyclacky_door/STLs/` | 1 | Black | 8.4 | 0.57 |
| `Panel_Clip.stl` | whopping\_Voron\_mods `clickyclacky_door/STLs/` | 1 | Black | 0.9 | 0.06 |
| `Handle.stl` | *(printed in B02, orange)* | 1 | Orange | 33.7 | 2.03 |

**Plate B10-P1** — all six black parts. 5.7 h, 76 g.

Notes:
- The "2X" in the filenames means **print two copies**; each file contains one body. Cross-check against the
  mod's BOM: 6 split bushings and 4 M5×45 dowel pins = 2 door hinges + 2 handle hinges.
- Hinge on the right / handle on the left? Mirror the two `Hinge-L-*` parts in the slicer; handle and latch are
  symmetric. ([Clicky-Clack README](https://github.com/tanaes/whopping_Voron_mods/tree/main/clickyclacky_door))
- **Because you're fitting Clicky-Clack, do not print** `door_hinge_x6`, `handle_a_x2`, `handle_b_x2`, `latch_x2`
  (Voron), nor LDO's `LDO Door/` set. That also means you lose the LDO kit-number nameplate — if you want it,
  print `LDO Door/handle_b_nameplate.stl` and glue it somewhere else.
- **Open question from your notes:** the Clicky-Clack kit was ordered in "Blue". Fabreeko's page doesn't say what
  the colour option governs; it is almost certainly the anodised door-frame extrusions, i.e. **visible blue trim
  around the front opening** — which matches the blue LDO frame but sits next to an orange/black scheme.
  Worth one message to Fabreeko before it ships. **(unverified)**

---

## 4. Totals, margin, spool changes

### 4.1 How these numbers were produced

Every plate hour and gram in this document is a **PrusaSlicer 2.9.6 estimate**, produced by actually slicing
the plate — not modelled. `slicer/build_plates.py` arranges each plate's real STLs on the 250 × 220 bed,
applies the per-object brims, writes `slicer/plates/<plate>.3mf`, slices it and reads
`; estimated printing time (normal mode)` and `; total filament used [g]` from the G-code footer.
`slicer/estimates.csv` lists every plate beside the figure it replaced.

The configuration is the one in [`manual/print/00-slicer-setup.md`](manual/print/00-slicer-setup.md): system
presets `0.20mm STRUCTURAL @COREONE 0.4` / `Prusament ASA @COREONE HF0.4` / `Prusa CORE One HF0.4 nozzle`,
plus every override in that document — 4 perimeters, 5 solid top and bottom, 40 % grid, forced 0.4 mm
extrusion width, shrinkage compensation zeroed, and the reduced speeds. Grams use the profile's own
1.07 g/cm³ ASA density.

**What replaced what.** The previous figures (134.3 h / 2248 g) came from a geometry-plus-throughput model:
wall-and-skin volume × 1.03 overhead, time = volume ÷ 4.5 mm³/s. Sliced, the build is **156.9 h / 2090 g** —
**+17 % time, −7 % filament**. Both errors have the same root: the model assumed a flat 4.5 mm³/s, but the
override table deliberately trades throughput for quality (perimeters 70 → 55 mm/s, external 50 → 35, first
layer 45 → 25), and it over-counted material by treating 4 perimeters as a solid 1.6 mm wall where Arachne
varies the beads. Every plate moved the same direction — the largest single change is B07-P1 at +2.0 h — so
the *shape* of the plan (which plates are long, which are short, what to start in the morning) is unchanged.

**Still calibrate on the first plate.** These are estimates from a slicer, not measurements from a printer.
Slicing `slicer/plates/B00-P1.3mf` yourself will return 3 h 58 m and 51.7 g to the minute, because it is the
same file. What is worth measuring is the *printer*: record B00-P1's wall-clock time and the weight of what
comes off the bed, and carry that ratio forward.

**Cross-check against the community numbers:** stripping the mods (Klicky 51 g, COB mounts 124 g, LDO extras)
gives ≈ **0.95 kg functional** and ≈ **0.90 kg cosmetic**, against the widely-quoted ~1.0 kg / ~0.9 kg for a
Voron 2.4 350 set. Total print time 156.9 h sits at the top of the commonly reported 120–160 h band — which is
what a quality-biased profile is supposed to do.

### 4.2 Filament budget

PrusaSlicer 2.9.6 estimates. The old model said 1940 g black / 308 g orange; slicing gives 129 g and 29 g
less — margin you gain, not a budget to spend.

| | Needed | On hand | Margin | Reprint allowance |
|---|---:|---:|---:|---:|
| **Galaxy Black** | **1811 g** | 2400 g (3 × 800 g) | **589 g** | **33 %** |
| **Prusa Orange** | **279 g** | 800 g (1 × 800 g) | **521 g** | **187 %** |
| Total | 2090 g | 3200 g | 1110 g | — |

**Black margin is comfortable, but not unlimited.** 589 g is about three of the largest plates. Typical
first-build reprint rate is 10–15 %, so you should land fine — but:

- Don't burn black on the optional extras (`bed_hole_marking_template`, `bottom_panel_template`, purge-bucket
  sheet stops, extra bestagon inserts) until the machine is standing.
- If any single plate fails twice, order a fourth black spool that day rather than mid-B08.
- If you do run short, the cheapest place to substitute is the **skirts and panel clips** — those see no heat
  and no load, and the Voron docs explicitly permit PLA/PETG there
  ([materials page](https://docs.vorondesign.com/materials.html)). Don't substitute anywhere else.

### 4.3 Spool changes

Cumulative black consumed after each batch: B00 **52** · B01 **353** · B03 **472** · B04 **588** · B05 **666** ·
B06 **814** · B07 **1040** · B08 **1439** · B09 **1735** · B10 **1811 g**.

With 800 g spools, spool #1 runs out inside **B06** — during **B06-P2**, which starts with only ~37 g left on
the spool — and spool #2 inside **B09**, during **B09-P3** (~31 g left at its start). The Core One+ runout
sensor pauses and resumes, so let it happen mid-plate; neither of those two plates is dimension-critical. But
if a runout would land inside B01-P1 (the 15.2 h, 201 g plate), start that plate on a fresh spool anyway — a
resume seam on a Z-drive body is not worth the risk. Record what is *actually* consumed in the spool ledger in
[`manual/print/README.md`](manual/print/README.md#spool-ledger); the prediction above is only as good as the
first few weighings.

---

## 5. Orientation, brim, and per-batch checkpoints

### 5.1 Orientation and brim

**Do not change which face sits on the bed.** Every Voron, LDO, Klicky, Nevermore and Clicky-Clack STL ships
pre-oriented for support-free printing. Rotating a part **about Z** (in the plane of the bed) to make it fit is
fine — it does not change the layer orientation, and plate B08-P1 needs it (`side_fan_support` turned 90°).
Two exceptions to the face rule:

1. `XY_cable_chain_bridge-Igus-3mm_backer.stl` is a community remix and arrives standing 44 mm tall on a
   21 mm-wide footprint, unlike the stock part which lies flat. **Check it in the preview before slicing** — if
   it isn't sitting on a flat face, lay it down to match the stock `[a]_xy_joint_cable_bridge_2hole`.
2. Mirror the two Clicky-Clack `Hinge-L-*` parts if you want the door to swing the other way.

**No part in this build exceeds 150 mm in Z.** The tallest are, in order:

| Part | Height | Footprint | Aspect | Action |
|---|---:|---|---|---|
| `Handle.stl` (Clicky-Clack) | 60.0 mm | 67.9 × 18.6 | tall & narrow | **5 mm brim** |
| `Latch.stl` (Clicky-Clack) | 58.0 mm | 25.9 × 14.6 | very tall & narrow | **5 mm brim** |
| `Hinge-L-sleeve/solid-2X` ×4 | 55.0 mm | 20.9 × 19.5 | very tall & narrow | **5 mm brim** |
| `mount.stl` (TFT) | 44.8 mm | 117 × 67 | fine | none |
| `z_motor_mount_a/b` ×4 | 42.0 mm | 51 × 30.7 | borderline | brim if you see any lift |

Separately, **brim the long flat parts** — not because they're tall but because 150–182 mm of ASA on a plate lifts
at the ends: **3 mm brim** on `rear_center_skirt_350`, `front_skirt_a/b_350`, `side_skirt_a/b_350`,
`side_fan_support_x2`, `keystone_panel`, `power_inlet_IECGS_1mm`, `exhaust_cover`, `V2_Duo_Plenum`,
`Regular_Cartridge`, `wago_221-415_mount_3by5`, `exhaust_filter_grill`, `cob_light_strip_mount_100mm`.
Brim separation stays at PrusaSlicer's 0.1 mm so it snaps off.
([Prusa warping KB](https://help.prusa3d.com/article/warping_2011))

Parts with **built-in supports to break out, not cut**: `[a]_stealthburner_main_body`, `Regular_Cartridge`
(Nevermore), `V2_Duo_Plenum`. The skirts are single-shell parts — they have no break-away body.

### 5.2 Checkpoint after each batch

| After | Inspect | Most commonly reprinted here |
|---|---|---|
| **B00** | The seven-item gate in §1.4. Nothing proceeds until all pass. | the cube, until the profile is right |
| **B01** | 625-2RS (16 mm OD) press-fit into each `z_drive_main` and `z_drive_retainer` bearing seat — thumb pressure, no rocking. M3 heat-set bosses on the motor mounts: no bulge, insert flush. Check the 4 mm/3 mm deck-support call. | `z_drive_main_*` — largest single parts, most exposed to warp at the corners |
| **B02** | Guidler and latch must move freely against the CW2 body once it exists (B06) — test-fit then, not now. Check the SB main body's built-in supports came out clean and the LED pockets are crisp. | `[a]_stealthburner_main_body` (most-photographed part in the build) |
| **B03** | **F695-2RS (13 mm OD, flanged)** bearing/spacer stacks must drop into the drive-frame and front-idler bores without reaming, and the two halves of each drive unit must close flat with no gap. (625-2RS is the Z-drive bearing — B01, not this batch.) | `a/b_drive_frame_lower` — the bearing seats are the tightest fit in the machine |
| **B04** | Test the MGN12 carriage screw pattern against `x_frame_V2TR_MGN12_*` before you commit heat-sets. XY joint bores must accept the shafts without reaming. | `xy_joint_*_lower_MGN12` |
| **B05** | Z joints: the 8 mm shaft should slide, not press. `z_joint_upper` must sit square on the extrusion. | `z_joint_lower_x4` |
| **B06** | Revo Voron hotend must sit flat in the printhead front with 4× M3×8. Klicky: magnets pressed **below** the plastic surface, polarity consistent, and the probe must attach/detach cleanly from the AB mount. | `KlickyProbe_v2` (that's why you print two) |
| **B07** | Wago mount heat-sets; COB mount halves must close flush on their 2× M3×6 FHCS. | `cob_light_strip_mount_100mm` (warps at the ends — check flatness on glass) |
| **B08** | **Lay every skirt segment on a flat reference (your granite counter) and check for rocking.** A bowed skirt is the most visible defect on a finished Voron. Also dry-fit the ring: front + TFT mount + front, rear + inlet + keystone, sides + fan supports. | `rear_center_skirt_350` (182 mm — the worst warp candidate in the set) |
| **B09** | Panel clips: snap one onto an extrusion with a 3 mm offcut to confirm 4 mm vs 6 mm choice **before** printing all 31. Nevermore: plenum lid must slide in its groove; cartridge must snap onto the plenum. | the 6 mm corner clips, if the foam tape choice changes |
| **B10** | Sleeve bearings must tap into the hinge sleeves without splitting the part; M5×45 pin into the "solid" half should be a **very** tight hammer fit with ~20 mm proud. | `Hinge-L-solid-2X` (split risk on the pin press) |

Across the whole build, the three parts most often reprinted by Voron builders are the **A/B drive frames**
(bearing fit), the **long skirts** (warp), and the **Stealthburner main body** (cosmetics). Budget your 589 g of
black margin against those.

---

## 6. Conditional / verify items

| Item | Status | What to do |
|---|---|---|
| Deck support thickness | LDO's guide says 4 mm, LDO's **350** BOM says the deck panel is 3 mm | Print `deck_support_3mm_x8` ×8 now (the size-specific BOM wins); measure the panel on arrival; 8 g to reprint at 4 mm |
| `PSU_stabilizer_50mm` | LDO says "SKIP p.169 — no support bracket" | Print it (4 g), fit only if the PSU needs it |
| Probe retainer bracket | 8 mm vs 9 mm probe barrel | Measure the Omron on arrival; the `_9mm` variant is 0.5 g |
| Cable-chain bridge with Ti backers | Fabreeko's backers ship pre-drilled with **pilot** holes for the cable-chain end link (drill 2.5 mm, tap M3 to use them), which may make the printed bridge unnecessary; the backer-aware remix exists in 3 mm and 6.5 mm | Both the stock `[a]_xy_joint_cable_bridge_2hole` and `XY_cable_chain_bridge-Igus-3mm_backer` are on plate B02-P3 (18 g total). Fit whichever clears. "Igus" = the **2-hole** chain pattern, which is what LDO ships. |
| Keystone blanks | Panel has **2** slots; LDO supplies 1 CAT6 keystone | 1 blank used, 1 spare — both on B02-P3 |
| Clicky-Clack "Blue" | Fabreeko doesn't state what the colour governs | Ask before it ships |
| Rev D+ printed-parts guide | Doesn't exist; only Rev A/B, C, D | **Resolved:** D+ changes one printed part (§0). The remaining Discord question is only whether a D+ guide will be published. |
| `mount.stl` vs `mount_thick.stl` | LDO links the folder, not a file | `mount.stl` chosen (30 g vs 74 g); swap if you want brightness-button access |

**Optional, not in any batch** (print later if you want them): `bed_hole_marking_template_x1_Rev2` (LDO's bed is
pre-drilled), `bottom_panel_template`, `Purge Bucket/brush_holder_sheet_stop` + `individual_sheet_stop`
(the kit does include a brass brush, so the Decontaminator nozzle-scrubber mod is on the table —
add ~9 g plus the mod's own STLs from
[VoronUsers](https://github.com/VoronDesign/VoronUsers/tree/main/orphaned_mods/edwardyeeks/Decontaminator_Purge_Bucket_%26_Nozzle_Scrubber)),
`[a]_fan_grill_open_optional_x2`, `z_belt_cover_a_led` (LDO variant if you route the LED strip through the
Z-belt opening), extra `ldo_bestagon_insert`s.

---

## 7. Deliberately NOT printed

| File | Why |
|---|---|
| `nozzle_probe.stl` (Voron) and `nozzle_probe_ldo.stl` (LDO) | LDO supplies the nozzle probe printed |
| `Leviathan_bracket_set.stl` | Supplied printed (L + R) |
| `usb_adapter_mount` **base** body | Supplied printed (the file is still printed — for a spare **base**; the Nitehawk-SB V2 partial cover replaces its cover body) |
| `bed_wago_mount.stl` | Supplied printed |
| `led_fan_pcb_spacer_x2.stl` | Supplied printed (×2) |
| `[a]_pcb_spacer.stl` (CW2) | Supplied printed — printing a spare anyway, 0.3 g |
| `cw2_chain_anchor_tilted.stl` | Supplied printed |
| `[c]_stealthburner_LED_diffuser.stl` | Supplied printed in **clear PETG**; you have no clear filament |
| `[a]_endstop_pod_hall_effect.stl`, `z_joint_upper_hall_effect.stl` | No hall-effect endstops in this kit |
| `Octopus_bracket_set.stl` and all other `Controller_Mounts/*` | Leviathan, not Octopus |
| `raspberrypi_bracket.stl`, `beefy_raspberry_bracket.stl` | Leviathan has an integrated Pi mount (Rev D) |
| `rs25_psu_bracket.stl` | No 5 V PSU in this kit |
| `mini12864_case_front/rear`, `[a]_mini12864_case_hinge`, `[a]_mini12864_case_front_insert`, `[a]_btt_knob_light_shield` | BTT touchscreen replaces the mini12864 module |
| `exhaust_filter_housing`, `[a]_exhaust_filter_mount_x2`, `[a]_filter_access_cover`, `[a]_exhaust_fan_grill` | Nevermore replaces the stock exhaust filter; kit has no fan for it |
| `door_hinge_x6`, `handle_a_x2`, `handle_b_x2`, `latch_x2`, LDO `LDO Door/*` | Clicky-Clack replaces the stock doors |
| `power_inlet_IECGS_1.2mm`, `power_inlet_filtered`, `plug_panel_1.2mm` | Kit ships the 1.0 mm inlet |
| `xy_joint_*_MGN9`, `x_carriage_*_MGN9`, `[a]_belt_clamp_MGN9_x2` (Superceded) | X axis is MGN12 |
| `zipchain2_*` (Superceded) | Kit ships real drag chain |
| `[a]_z_tensioner_x4_6mm` (Superceded) | Kit ships 9 mm-wide Z idlers |
| `pinda_adapter`, `chain_anchor_3hole*`, `cable_door.stl`, `Bowden/*`, `ADXL345_Mounts/*` | Wrong variant for this kit |
| `deck_support_4mm_x8`, `probe_retainer_bracket_9mm` | **Conditional, not excluded** — the caliper decides (§6). `deck_support_3mm_x8` is the printed default (Rev D 350 BOM); the 4 mm set is the reprint if the panel measures 4 mm. |
| `spool_holder`/`bowden_retainer` — *these ARE printed* (B09) | listed here only to avoid confusion with Spool_Management's other files |
| Beacon, Nevermore StealthMax, StealthChanger parts | Explicitly out of scope for this build |

---

## 8. Where to do the Core One+ Gen 2 belt upgrade

**Baseline plan (unchanged):** finish the Core One+ kit through Ch. 9 (self-test + first print), then apply the
Gen 1 → Gen 2 upgrade, re-tension and re-square, *then* start batch B00. The GT1.5 conversion changes belts,
pulleys, steps/mm and firmware together — you want it done and settled before 157 h of ASA.

**If the upgrade kit arrives mid-run, pause at the end of Batch B07, before Batch B08.** Reasons:

1. B08 + B09 + B10 are 12 of the 27 plates and contain **every surface anyone will ever look at** — the 150–182 mm
   skirts are large flat vertical faces, which is exactly where GT1.5's reduced VFA shows.
2. B00–B07 are structural parts inside the machine; VFA there is cosmetically irrelevant.
3. It's a clean boundary — no half-finished sub-assembly waits on it.

**Second-best boundary:** if the kit arrives *before* B02 starts, do it then — the Stealthburner main body is the
single most-looked-at printed part on the machine and it's on B02-P1.

**After the upgrade, before restarting prints:**

1. Firmware **≥ 6.9.0** (adds GT1.5 belt support and Gen 2 expansion joints).
2. Re-tension both belts and re-square the gantry, per
   [help.prusa3d.com/manual/prusa-core-one-to-gen-2-upgrade_2435](https://help.prusa3d.com/manual/prusa-core-one-to-gen-2-upgrade_2435).
3. Re-run the self-test and input shaper calibration.
4. Redo first-layer calibration (§1.4 step 3).
5. **Re-print `Voron_Design_Cube_v7` and re-measure** — steps/mm changed with the pulleys, so the dimensional gate
   has to be re-passed before you print 437 g of skirts.

Do **not** try to interleave the upgrade with a running plate; the Nextruder and bed have to come apart.

---

## 9. Machine-readable batch summary

Hours and grams are **PrusaSlicer 2.9.6 estimates** sliced from `slicer/plates/*.3mf` (§4.1); per-plate
detail with the previous model figure beside each one is in `slicer/estimates.csv`.

`hard_prereq_batches` = batches that must be **printed** before the assembly chapter in `unlocks_chapter` can
actually be completed (B00 is the calibration gate for everything; B02 carries the accent parts that most
mechanical chapters need).

| batch_id | name | plates | hours | g_black | g_orange | unlocks_chapter | hard_prereq_batches |
|---|---|---:|---:|---:|---:|---|---|
| B00 | Calibration & jigs | 1 | 4.0 | 52 | 0 | Frame | — |
| B01 | Z drive assemblies | 2 | 22.8 | 301 | 0 | Z Drives and Idlers | B00;B02 |
| B02 | Accent parts (orange) | 3 | 21.8 | 0 | 279 | *(accent for Z Drives and Idlers, A/B Drives and Idlers, Gantry, Stealthburner, Skirts)* | B00 |
| B03 | A/B drive units + front idlers | 2 | 8.5 | 119 | 0 | A/B Drives and Idlers | B00;B02 |
| B04 | XY joints + X carriage | 1 | 8.6 | 117 | 0 | Gantry | B00;B02;B03 |
| B05 | Z joints + Z chain | 1 | 6.4 | 78 | 0 | Z Axis; A/B Belts | B00;B02;B04 |
| B06 | Toolhead (SB + CW2 + Klicky) | 2 | 12.2 | 148 | 0 | Stealthburner | B00;B02;B04 |
| B07 | Electronics bay + lighting | 3 | 16.0 | 226 | 0 | Electronics; Controller; Wiring | B00 |
| B08 | Skirts + front modules | 6 | 29.1 | 399 | 0 | Skirts | B00;B02;B07 |
| B09 | Panels, filtration, spool | 5 | 21.9 | 296 | 0 | Panels | B00;B08 |
| B10 | Clicky-Clack door | 1 | 5.7 | 76 | 0 | Panels (front door) | B00;B02;B09 |
| **TOTAL** | | **27** | **156.9** | **1811** | **279** | | |

```csv
batch_id,name,plates,hours,g_black,g_orange,unlocks_chapter,hard_prereq_batches
B00,Calibration & jigs,1,4.0,52,0,Frame,
B01,Z drive assemblies,2,22.8,301,0,Z Drives and Idlers,B00;B02
B02,Accent parts (orange),3,21.8,0,279,Multiple (accent),B00
B03,A/B drive units + front idlers,2,8.5,119,0,A/B Drives and Idlers,B00;B02
B04,XY joints + X carriage,1,8.6,117,0,Gantry,B00;B02;B03
B05,Z joints + Z chain,1,6.4,78,0,Z Axis;A/B Belts,B00;B02;B04
B06,Toolhead (SB + CW2 + Klicky),2,12.2,148,0,Stealthburner,B00;B02;B04
B07,Electronics bay + lighting,3,16.0,226,0,Electronics;Controller;Wiring,B00
B08,Skirts + front modules,6,29.1,399,0,Skirts,B00;B02;B07
B09,"Panels, filtration, spool",5,21.9,296,0,Panels,B00;B08
B10,Clicky-Clack door,1,5.7,76,0,Panels (front door),B00;B02;B09
TOTAL,,27,156.9,1811,279,,
```

Plate-level detail (batch, plate, hours, grams) for scheduling:

```csv
plate_id,batch_id,hours,grams,colour
B00-P1,B00,4.0,52,black
B01-P1,B01,15.2,201,black
B01-P2,B01,7.6,100,black
B02-P1,B02,7.0,90,orange
B02-P2,B02,7.2,93,orange
B02-P3,B02,7.6,96,orange
B03-P1,B03,4.4,60,black
B03-P2,B03,4.1,58,black
B04-P1,B04,8.6,117,black
B05-P1,B05,6.4,78,black
B06-P1,B06,8.0,97,black
B06-P2,B06,4.2,51,black
B07-P1,B07,5.6,67,black
B07-P2,B07,8.2,124,black
B07-P3,B07,2.3,34,black
B08-P1,B08,6.3,99,black
B08-P2,B08,5.0,67,black
B08-P3,B08,5.5,71,black
B08-P4,B08,5.1,66,black
B08-P5,B08,5.0,70,black
B08-P6,B08,2.3,26,black
B09-P1,B09,4.5,63,black
B09-P2,B09,4.9,67,black
B09-P3,B09,3.9,55,black
B09-P4,B09,4.2,56,black
B09-P5,B09,4.3,56,black
B10-P1,B10,5.7,76,black
```

---

## 10. Sources

**Voron official**
- Voron-2 repo, branch `Voron2.4` — <https://github.com/VoronDesign/Voron-2/tree/Voron2.4>
- Voron 2.4r2 Assembly Manual (2023-07-04) — <https://github.com/VoronDesign/Voron-2/blob/Voron2.4/Manual/Assembly_Manual_2.4r2.pdf>
  (print settings p.4; file naming p.5; deck panel p.28–30; skirts p.211–221; bottom panel p.232–233; Z belt covers p.234–236; panels p.239–244; exhaust p.250–256; spool holder p.257–259)
- Voron STL folder — <https://github.com/VoronDesign/Voron-2/tree/Voron2.4/STLs>
- Stealthburner repo — <https://github.com/VoronDesign/Voron-Stealthburner/tree/main/STLs>
- Stealthburner filename nomenclature — <https://github.com/VoronDesign/Voron-Stealthburner/blob/main/STLs/README.md>
- Stealthburner printhead compatibility — <https://github.com/VoronDesign/Voron-Stealthburner/blob/main/STLs/Stealthburner/Printheads/README.md>
- Stealthburner Assembly Manual — <https://github.com/VoronDesign/Voron-Stealthburner/blob/main/Manual/Assembly_Manual_SB.pdf>
- Voron materials selection (shrinkage = 100 %) — <https://docs.vorondesign.com/materials.html>
- Voron secondary printer tuning (belt tensions) — <https://docs.vorondesign.com/tuning/secondary_printer_tuning.html>

**LDO**
- LDO Voron 2.4 kit landing page — <https://docs.ldomotors.com/en/voron/voron2>
- Rev D printed parts guide — <https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d>
- Rev D wiring guide — <https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d>
- Build Notes / FAQ (manual deviations by page) — <https://docs.ldomotors.com/voron/voron2/build-faq>
- Rev D 350 BOM — <https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D>
- LDO Nevermore V5 Duo assembly guide — <https://ldomotion.com/guides/nevermore-v5-duo---v24>
- LDOVoron2 STLs — <https://github.com/MotorDynamicsLab/LDOVoron2/tree/main/STLs>
- COB light strip mount counts — <https://github.com/MotorDynamicsLab/LDOVoron2/tree/main/STLs/COB%20Light%20Strip>
- BTT Pi TFT4.3 mount — <https://github.com/MotorDynamicsLab/LDOVoronTrident/tree/master/STLs/BTT%20Pi%20TFT4.3%20Mount>
- Nitehawk-SB STLs — <https://github.com/MotorDynamicsLab/Nitehawk-SB/tree/master/STLs>
- Nitehawk-SB V2 STLs (`usb_adapter_mount_partial_cover`) — <https://github.com/MotorDynamicsLab/Nitehawk-SB-V2/tree/master/STLs>
- Leviathan STLs — <https://github.com/MotorDynamicsLab/Leviathan/tree/master/STLs>

**Vendor**
- Fabreeko — LDO Voron 2.4 R2 (Rev D+) kit — <https://www.fabreeko.com/products/ldo-voron-v2-4-kit>
- Fabreeko — Clicky-Clack Door Kit by LDO — <https://www.fabreeko.com/products/clickyclackydoor-kit-by-ldo>
- Fabreeko — V2.4/Trident titanium extrusion backers — <https://www.fabreeko.com/products/v2-4-trident-titanium-extrusion-backers>

**Mods**
- Klicky Probe — <https://github.com/jlas1/Klicky-Probe> (what-to-print + BOM: <https://github.com/jlas1/Klicky-Probe/tree/main/Printers/Voron/v1.8_v2.4_Legacy_Trident>)
- Nevermore Micro (V5 Duo) — <https://github.com/nevermore3d/Nevermore_Micro>
- Clicky-Clack Fridge Door (whoppingpochard / tanaes) — <https://github.com/tanaes/whopping_Voron_mods/tree/main/clickyclacky_door>
- Extrusion backers — <https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers>

**Prusa / slicer**
- PrusaSlicer releases (2.9.6 stable, 2026-06-25) — <https://github.com/prusa3d/PrusaSlicer/releases>
- PrusaResearch.ini @ version_2.9.6 (source of every quoted default) — <https://github.com/prusa3d/PrusaSlicer/blob/version_2.9.6/resources/profiles/PrusaResearch.ini>
- Prusa KB — ASA — <https://help.prusa3d.com/article/asa_1809>
- Prusa KB — Warping — <https://help.prusa3d.com/article/warping_2011>
- Prusa KB — CORE One to Gen 2 upgrade — <https://help.prusa3d.com/manual/prusa-core-one-to-gen-2-upgrade_2435>
- Prusa KB — CORE One downloads / firmware — <https://help.prusa3d.com/downloads/core-one>

**Community**
- Ellis' Print Tuning Guide — <https://ellis3dp.com/Print-Tuning-Guide/> (first-layer squish, extrusion multiplier, perimeter separation)
- Voron Print It Forward (the option not taken) — <https://pif.voron.dev/>
