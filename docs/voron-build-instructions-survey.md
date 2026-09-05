# Voron 2.4 R2 Rev D+ (LDO/Fabreeko, 350mm) — build-instruction source survey and consolidation spec

Compiled 2026-09-05. Every claim below was checked against the live source on that date; dates/versions are quoted from the source itself (HTTP metadata, PDF `ModDate`, wiki `updated-at`, GitHub commit dates), not from recall.

---

## 0. Verdict up front

- **Spine = the official Voron 2.4r2 Assembly Manual PDF** (263 pages, `ModDate` 2023-07-18), read *only* through **LDO's Build Notes/FAQ**, which is a page-indexed diff against that exact PDF commit.
- **Electronics/wiring/software spine = LDO Wiring Guide Rev D** (updated 2026-07-14), not the manual — the manual's Electronics/Controller/Wiring chapters (p.148–211) are almost entirely superseded.
- **"Rev D+" is a one-line hardware delta**: Rev D with the **Nitehawk-SB V2** toolboard. Everything else in the kit is Rev D. But that one delta invalidates a surprising amount of LDO's own Rev D toolhead text (MCU family, USB serial ID pattern, connector types, header keying, Klipper config file).
- **LDO publishes no Rev D+ document.** Verified by enumerating every link on `docs.ldomotors.com/en/voron/voron2`: guides exist for Rev A/B, Rev C, Rev D only. The Rev D+ specifics live in three other places (the `-sbv2` Klipper config, the Nitehawk-SB-V2 board doc, the Nitehawk-SB-V2 repo).
- **No video series exists for this kit revision at build-along granularity.** The only Rev D video content is a 4-part ~45-minute overview (123-3D, Oct–Nov 2024) and one 10-hour unedited livestream (Nathan Builds Robots, Feb 2025). Every step-by-step series is Rev A/B/C or a FormBot/Blurolls kit.

---

## 1. Kit facts (verified)

### 1.1 What "Rev D+" means

Fabreeko's product page for the exact SKU states, verbatim:

> **Rev D+ Changes for March 2026** — Nitehawk SB update with USB passthrough for USB based eddy current probes

— [fabreeko.com/products/ldo-voron-v2-4-kit](https://www.fabreeko.com/products/ldo-voron-v2-4-kit)

That is the *only* listed change vs. Rev D. Cross-checked against LDO's own board documentation, "USB passthrough" = the **Nitehawk-SB V2**:

> Added USB hub and secondary USB port as in Nitehawk-36 … Onboard microcontroller changed from RP2040 to **STM32G0B1** … Probe, TH0, XY Endstop ports changed from JST-XH2.5 to **JST-PH2.0** … Reversed connector gender between main toolboard and fan adapter PCB. The headers are also now keyed … Vastly Improved ESD performance.

— [docs.ldomotors.com/en/Toolboard/nitehawk-sb-v2](https://docs.ldomotors.com/en/Toolboard/nitehawk-sb-v2) (page created 2025-12-22, updated 2026-07-10) and [github.com/MotorDynamicsLab/Nitehawk-SB-V2](https://github.com/MotorDynamicsLab/Nitehawk-SB-V2) (README, repo pushed 2026-07-22)

Corroborating: LDO added `Firmware/leviathan-printer-rev-d-sbv2.cfg` to the kit repo on **2026-07-21** with the commit message *"feat(leviathan-rev-d): add Nitehawk-SB toolboard config"*, and its `Firmware/README.md` says *"This contains mainboard configs for LDO V2.4 kits Rev.D with the **Nitehawk-SB V2** toolboard."* — [github.com/MotorDynamicsLab/LDOVoron2](https://github.com/MotorDynamicsLab/LDOVoron2)

### 1.2 Rev D+ contents (electronics, probe, motion)

Sourced from the [Fabreeko SKU page](https://www.fabreeko.com/products/ldo-voron-v2-4-kit), the [LDO kit index](https://docs.ldomotors.com/en/voron/voron2), and the per-batch [LDO V2.4-350 Rev D BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D) (BOM page updated 2026-02-05).

| Subsystem | Rev D+ content | Note |
|---|---|---|
| Mainboard | **LDO Leviathan** (STM32F446 **(contested: F446 per wiring guide/config, H743 per LDO README since 2025-10-30 — read the silkscreen; see manual Ch 12 step 12.13)**), 5× TMC2209 + 2× TMC5160 HV for A/B, separate HV rail 24/48 V, on-board Pi mount + Pi HAT power adapter | Replaces BTT Octopus of Rev A–C |
| Toolboard | **Nitehawk-SB V2** (STM32G0B1, TMC2209, ADXL345, USB hub, secondary USB port, I²C port) + Fan Adapter PCB + USB Adapter PCB + flat umbilical | **The "+" in D+** |
| Toolhead | Stealthburner + **Clockwork 2**, Bondtech IGDA gear set, **E3D Revo HF** with 60 W heater (Rapido HF is a $9.99 swap) | ADXL mount not needed — accelerometer is on-board |
| Z probe | **Omron inductive probe** (QGL only) + fibreglass insulation tape. **Klicky Probe Kit** included as the optional alternative | **Not** Tap. **Not** Cartographer/Beacon. |
| Z endstop | LDO **nozzle probe** PCB (D2F microswitch + 5 mm shaft) + LDO printed part | Replaces the manual's `nozzle_probe.stl` and hall-effect endstops |
| XY endstop | LDO **XY microswitch PCB** (single 4-pin, breaks out to X Stop / Y Stop) | Manual's hall-effect pods not used |
| A/B motors | 2× `LDO-42STH48-2004MAH(VRN)` — **0.9°** (config uses `full_steps_per_rotation: 400`) | |
| Z motors | 4× `LDO-42STH48-2004AC(VRN)`, 1.8°, `gear_ratio: 80:16` | |
| Extruder motor | 1× `LDO-36STH20-1004AHG(VRN)` | |
| Rails | 1× `LDO-SLR12H-400Z1` stainless **MGN12H** (X); 6× `LDO-SLR9H-400Z0` stainless **MGN9H** (Y×2, Z×4). Ship **dry** | Grease before install |
| Bed | Cast 5083 Al, Blanchard-ground, 355×355×10 mm, LDO AC heatpad + 125 °C thermal fuse **pre-applied**, magnetic pad **NOT pre-applied** — separate BOM line `Magnetic Pad 2.4-350`, applied during the build (`docs/manual/03-build-plate.md`), spring-steel flex plate | Manual p.55/56 become no-ops (magnet still applied per manual) |
| Power | Meanwell **LRS-200-24** (US 110 V build; EU may get RSP-200-24), Omron SSR + DIN bracket, AC inlet with integrated switch + fuse | 115/230 V selector switch on the PSU |
| Screen | 4.3" capacitive DSI touchscreen + Pi ribbon cable | Mount STL lives in the **Trident** repo, not the V2 repo |
| Host | Raspberry Pi 4B + heatsink + 32 GB SD (BOM marks the Pi "OPTIONAL — check with your reseller"; the Fabreeko SKU includes it) | |
| Lighting | 2× **COB** LED strip + 2× splitter PCB (LDO ships the splitter spacers printed) | Rev D upgraded from discrete LEDs to COB |
| Filtration | **Nevermore Micro V5 Duo** parts, no carbon (shipping restriction) | Stock exhaust filter parts are optional and the fan is not included |
| Panels | Acrylic deck/back/bottom (black); PC clear doors/sides/top | See §4.3 — deck thickness is contested |
| Belts | Gates 2GT 9 mm × 6 m (Z), 2GT 6 mm × 6.21 m (A/B), 4× closed 2GT 6×188 mm loops (Z drive) | |
| Drag chain | 10×10 R18 × 2, 10×15 R28 × 1, **2-hole** chain ends | Print `*_2hole` parts, never `*_3hole` |
| Printed parts **included** by LDO | Leviathan Bracket L/R, NH Adapter Mount, DIN Clip ×4, CW2 Chain Anchor Tilted, 2×3 Splitter Spacer ×2, LDO Nozzle Probe, Bed WAGO Mount, Stealthburner LED Diffuser (clear PETG), CW2 PCB Spacer | Do **not** re-print these |

Bulk consumables that drive the build plan (Rev D 350 BOM): **153×** M3×5×4 brass heat-set inserts, **283×** M3×8 SHCS, 135× M3 roll-in T-nut, 80× M5 roll-in T-nut, 75× M3 hammerhead, 16× M5 hammerhead, 46× M5 1 mm precision spacer (used *instead of* every M5 shim in the manual), 44× M3×30, 43× M3×16-equivalent… plus 100 zip ties, 16× 6×3 mm magnets, VE0508 ferrules ×5, brass heat-set tip, 2 mm drill bit, 5 hex wrenches, 2.5 mm flat screwdriver, brass brush, 1 mm + 3 mm foam tape, 3M VHB.

**Batch-specific BOM.** LDO publishes a *separate BOM page per production batch*, indexed by kit serial (`V2-YYMM…`). The index at [350_BOM/HOME](https://docs.ldomotors.com/en/voron/voron2/350_BOM/HOME) (updated 2026-06-26) currently tops out at batch **2606**. Order F6424626 (2026-09-04, ETA mid/late September) will be a later batch. **Action on arrival:** find the kit serial on the carton, open its batch BOM, and use *that* page as the inventory checklist — it has `Check1`/`Check2` columns designed for exactly this.

### 1.3 Documentation LDO actually publishes for this SKU

| Doc | URL | Created | Last updated | Images |
|---|---|---|---|---|
| Kit index / features | [docs.ldomotors.com/en/voron/voron2](https://docs.ldomotors.com/en/voron/voron2) | — | — | — |
| **Build Notes / FAQ** (page-indexed diff vs official manual) | [/voron/voron2/build-faq](https://docs.ldomotors.com/voron/voron2/build-faq) | 2022-09-12 | **2026-02-10** | few |
| **Wiring Guide Rev D** (incl. full software setup) | [/en/voron/voron2/wiring_guide_rev_d](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d) | 2024-06-17 | **2026-07-14** | 39 |
| **Printed Parts Guide Rev D** | [/en/voron/voron2/printed_part_guide_rev_d](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d) | 2024-07-22 | 2025-07-14 | 20 |
| 350 BOM index (per batch) | [/en/voron/voron2/350_BOM/HOME](https://docs.ldomotors.com/en/voron/voron2/350_BOM/HOME) | 2022-06-22 | 2026-06-26 | — |
| 350 Rev D BOM | [/en/voron/voron2/350_BOM/Rev_D](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D) | 2024-07-05 | 2026-02-05 | — |
| **Nitehawk-SB V2 board doc** (pinout, changes) | [/en/Toolboard/nitehawk-sb-v2](https://docs.ldomotors.com/en/Toolboard/nitehawk-sb-v2) | 2025-12-22 | 2026-07-10 | yes |
| Nitehawk-SB **V1** board doc (do not use for D+) | [/en/Toolboard/nitehawk-sb](https://docs.ldomotors.com/en/Toolboard/nitehawk-sb) | — | — | yes |
| Rail grease guide | [/guides/rail_grease_guide](https://docs.ldomotors.com/guides/rail_grease_guide) | 2022-01-31 | 2023-09-16 | 3 |
| Heat-set insert tool guide | [/guides/heatset_insert_tool_guide](https://docs.ldomotors.com/guides/heatset_insert_tool_guide) | 2021-05-19 | 2022-07-29 | 4 |
| Cable chain guide | [/guides/cable_chain_guide](https://docs.ldomotors.com/guides/cable_chain_guide) | 2021-09-25 | 2022-07-29 | 7 |
| **Leviathan V1.3 firmware guide** (numbered steps + step photos) | [ldomotion.com/guides/voron-leviathan-v1-3](https://ldomotion.com/guides/voron-leviathan-v1-3) | — | — | 30 |
| **Nevermore V5 Duo — V2.4** (numbered steps + step photos) | [ldomotion.com/guides/nevermore-v5-duo---v24](https://ldomotion.com/guides/nevermore-v5-duo---v24) | — | — | 37 |
| Klipper config (Rev D, Nitehawk V1) | [`Firmware/leviathan-printer-rev-d.cfg`](https://github.com/MotorDynamicsLab/LDOVoron2/blob/main/Firmware/leviathan-printer-rev-d.cfg) | — | 2026-07-21 | — |
| **Klipper config (Rev D+, Nitehawk V2)** | [`Firmware/leviathan-printer-rev-d-sbv2.cfg`](https://github.com/MotorDynamicsLab/LDOVoron2/blob/main/Firmware/leviathan-printer-rev-d-sbv2.cfg) | 2026-07-21 | 2026-07-21 | — |
| Hi-res Rev D wiring photos (GPL-3.0) | [`Images/WiringGuide/RevD/`](https://github.com/MotorDynamicsLab/LDOVoron2/tree/main/Images/WiringGuide/RevD) | — | — | 19 build + 6 UI |

Note: **ldomotion.com** (LDO's newer guide platform) hosts step-numbered, photo-per-step guides — literally the Prusa format ("Step 3 of 7 in this section", "Step Images"). Only two are relevant here (Leviathan, Nevermore); there is no Voron 2.4 *assembly* guide on it. This is the strongest existing evidence that the target format is achievable and that LDO would have done it if they had the budget.

---

## 2. Source survey

Legend for **Fit**: 🟢 use as-is · 🟡 use with documented overlay · 🔴 do not follow for this kit.

| # | Source | Covers | Kit rev / date | Format & strengths | Gaps / conflicts with Rev D+ | Fit |
|---|---|---|---|---|---|---|
| 1 | **Official Voron 2.4r2 Assembly Manual** — [`Voron-2/Manual/Assembly_Manual_2.4r2.pdf`](https://github.com/VoronDesign/Voron-2/blob/Voron2.4/Manual/Assembly_Manual_2.4r2.pdf) | Whole machine, Frame→Panels | Generic 2.4r2. Title page "VERSION 2023-07-04"; PDF `ModDate` **2023-07-18**; last commit touching `Manual/` 2023-07-18 ("stealthburner integration"). Release tag `V2.4r2` is 2022-02-23 | 263-page A4-landscape PDF, CAD exploded views, one action per page, fastener callouts drawn in place | No step numbers, no photos, no "what you should see" checks, no time estimates, no per-step BOM totals. Ch. Electronics/Controller/Wiring (p.148–211) is Octopus + 5 V PSU + mini12864 — **wrong board, wrong PSU topology, wrong screen** for this kit | 🟡 spine for mechanical (p.12–147); 🔴 for p.148–211 |
| 2 | **LDO Build Notes / FAQ** — [build-faq](https://docs.ldomotors.com/voron/voron2/build-faq) | Page-by-page deltas vs. #1 | Rev A→D. Page updated **2026-02-10**; explicitly pinned to manual commit `de7e89d`, "as of July 18, 2023" | Wiki text, ~35 numbered page callouts | Silent on everything Rev D+ (toolboard). Contains an internal contradiction on deck thickness (§4.3). Some notes still reference Rev A/C parts | 🟢 mandatory overlay on #1 |
| 3 | **LDO Wiring Guide Rev D** — [wiring_guide_rev_d](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d) | Above-deck + below-deck wiring, mains, Checkpoint #1, Pi OS, KIAUH, KlipperScreen, firmware, USB IDs, printer.cfg | Rev D; updated **2026-07-14**; 39 images | The only end-to-end electrical doc for this machine. Has a real safety checkpoint with multimeter procedure. Sourced hi-res images on GitHub under GPL-3.0 | **Toolhead section is Nitehawk V1**: says JST-XH2.5 connectors, says the toolboard is RP2040, links the V1 `leviathan-printer-rev-d.cfg`. All three are wrong for Rev D+ | 🟢 spine for electrical, with §4.1 patch |
| 4 | **LDO Printed Parts Guide Rev D** — [printed_part_guide_rev_d](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d) | Which STLs to print/skip/substitute | Rev D; updated 2025-07-14; 20 images | Colour-coded (must / optional / already-in-kit). Names the 2-hole chain parts, D2F endstop pod, `power_inlet_IECGS_1mm`, 4 mm deck supports, COB light-bar clips | Points at the **V1** Nitehawk USB-adapter cover; V2 uses `usb_adapter_mount_partial_cover.stl` from the V2 repo | 🟢 with one substitution |
| 5 | **LDO Nitehawk-SB V2 doc + repo** — [board doc](https://docs.ldomotors.com/en/Toolboard/nitehawk-sb-v2) · [repo](https://github.com/MotorDynamicsLab/Nitehawk-SB-V2) | Pinout, connectors, change list, grounding images, `Configs/nitehawk-sbv2.cfg` | Rev D+ era; doc updated 2026-07-10, repo pushed 2026-07-22 | The authoritative Rev D+ delta. Full port/pin table. `ibom.html` interactive BOM, schematic PDF | Thin: no assembly text, no license file on the repo, grounding images (`grounding_scheme.jpg`, `toolboard_ground_routing.jpg`, `usb_adapter_gnd.jpg`) have **no prose anywhere** | 🟢 mandatory for Ch. toolhead + wiring |
| 6 | **Voron Stealthburner Assembly Manual** — [`Assembly_Manual_SB.pdf`](https://github.com/VoronDesign/Voron-Stealthburner/blob/main/Manual/Assembly_Manual_SB.pdf) | SB body, CW2 extruder, LEDs | 73 pages, "VERSION 2023-07-07", `ModDate` 2023-07-07; last `Manual/` commit 2023-07-13. High-contrast variant also present | Same CAD-exploded style; covers CW2 and the LED chain properly | Generic — assumes hartk 2-piece PCB, not Nitehawk V2. Fan/neopixel connector routing differs | 🟡 spine for Ch. toolhead with #3/#5 overlay |
| 7 | **Voron Documentation site** — [docs.vorondesign.com](https://docs.vorondesign.com) ([repo](https://github.com/VoronDesign/Voron-Documentation), pushed 2026-08-29) | Sourcing, **V2 gantry squaring**, software, **Initial Startup wizard**, tuning (belt tension, bed mesh), maintenance, community how-tos | Actively maintained; generic 2.4 | The Startup guide is a *stepped wizard with a progress bar* that branches on probe type and web UI — closest existing thing to the target format. Authoritative belt-tension numbers | Generic: nothing kit-specific. `build/electrical/v2_octopus_wiring.md` is the wrong board | 🟢 spine for Ch. squaring, startup, tuning |
| 8 | **Ellis' Print Tuning Guide** — [ellis3dp.com](https://ellis3dp.com/Print-Tuning-Guide/) · [repo](https://github.com/AndrewEllis93/Print-Tuning-Guide) (2.1k★, last push **2025-03-14**) | First-layer squish, pressure advance, extrusion multiplier, flow, max accel, VFA troubleshooting, macros | Printer-agnostic; also carries the original V2 gantry-squaring procedure | The de-facto community standard; LDO and Fabreeko both link it. Concrete, image-heavy, decision-tree structured | Not a build guide. Slicer examples are SuperSlicer-centric; needs translation to PrusaSlicer/Orca. No commits in ~18 months | 🟢 spine for Ch. tuning |
| 9 | **Klicky Probe** — [github.com/jlas1/Klicky-Probe](https://github.com/jlas1/Klicky-Probe) (1.4k★, pushed 2026-05-09) | Dockable microswitch probe, macros, `[gcode_macro]` set | Active | Only needed if he abandons the Omron. Kit ships the parts | Adds a whole macro layer and dock calibration; conflicts with the stock LDO config | 🔴 for the first build (defer) |
| 10 | **Nevermore Micro V5** — [github.com/nevermore3d/Nevermore_Micro](https://github.com/nevermore3d/Nevermore_Micro) (1.6k★, pushed 2025-01-01) + [LDO's V5-Duo–V2.4 guide](https://ldomotion.com/guides/nevermore-v5-duo---v24) | Filter build + mount | Current | LDO's version is **step-numbered with 37 step images** — already Prusa-format | Print the 3×6-magnet variant. Carbon media not supplied | 🟢 for Ch. filter/panels |
| 11 | **Extrusion backers + Clicky-Clack** — [github.com/tanaes/whopping_Voron_mods](https://github.com/tanaes/whopping_Voron_mods) | Ti backers; Clicky-Clack fridge door | Current, widely deployed | Backers README is explicit on **placement** (opposite the rail) and fasteners (M3×8 FHCS for Y, M3×6 FHCS for X, ~30 T-nuts) | Clicky-Clack README has **no print settings and no install steps** — see #12 | 🟢 backers · 🟡 door |
| 12 | **KB3D wiki — LDO Clicky-Clacky Door Mod** — [wiki.kb-3d.com](https://wiki.kb-3d.com/en/home/LDO/LDO_Clicky_Clacky_Door_Mod) | Hinge/handle/latch assembly and mounting | Created 2024-10-27, updated **2025-09-15**; demonstrated on a 300 V2.4; **34 images** | The only photo-illustrated Clicky-Clack install guide. Lists the exact STL set and print settings | Reseller wiki (KB3D, not Fabreeko/LDO). Demo uses NanoNest panels, not the plain acrylic panel he ordered | 🟢 for Ch. door, with panel-mount substitution |
| 13 | **Voron community how-tos** — [`community/howto/simonthecat/I_wish_I_had_known.md`](https://github.com/VoronDesign/Voron-Documentation/blob/main/community/howto/simonthecat/I_wish_I_had_known.md) et al. | Accumulated first-build gotchas | Live in the docs repo | Genuinely non-obvious items: bed tacos from cold-tightening, 16T vs 20T Z pulleys look alike, never unplug a stepper with power on, don't hand-spin connected steppers | Unstructured, partly stale (Afterburner-era) | 🟢 mine for check-text, don't follow as a track |
| 14 | **Voron Discord** (`#voron_2_questions`, `#ldo_motors`) — [discord.gg/voron](https://discord.gg/voron) | Live Q&A, LDO's own support channel | Live | LDO's build-notes page explicitly directs Rev D corrections to `#ldo_motors`. Fastest path for a Rev D+ ambiguity | Not citable, not searchable offline, no version pinning | 🟢 as escalation only |
| 15 | **Fabreeko Discord** — [discord.gg/NV8Y6bcerP](https://discord.gg/NV8Y6bcerP) (linked from the SKU page) | Vendor support, missing/wrong parts | Live | Right channel for the *"is my batch Nitehawk V1 or V2"* question and for the XY-endstop-cable mis-label issue | Vendor-scoped | 🟢 as escalation only |
| 16 | **Voron forum** — [forum.vorondesign.com](https://forum.vorondesign.com) | Threads incl. the [Rev D launch thread (2024-06-12)](https://forum.vorondesign.com/threads/ldo-voron-rev-d-kits-are-now-live-at-fabreeko.1802/) | Live but Cloudflare-gated to scripted access | Useful archive of Rev D discussion | Thin traffic; no Rev D+ discussion found | 🟡 background only |
| 17 | **Steve Builds — "LDO Voron 2.4 Kit Hangout and Build"** ([playlist](https://www.youtube.com/playlist?list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY)) | 11 parts, full build | **Dec 2021 – Jan 2022 → Rev A/B** | Livestream video · Linked from LDO's own docs; Steve is on the Voron team | Octopus board, Afterburner toolhead, mini12864, 5 V PSU, discrete LEDs. **Nothing about the electronics half transfers** | 🔴 electrical · 🟡 mechanical only |
| 18 | **Nero3D / Canuck Creator — "Voron V2.4r2 LDOmotors kit Livestream build"** ([Part 1](https://www.youtube.com/watch?v=ZHO-kFlY91c), 3 h 49 m, 2022-02-15) | Full build, LDO kit | **Feb 2022 → Rev A/B** | Livestream · Nero is a Voron team member; the reference "why" commentary (t-nuts, rail grease NLGI 0/1, gantry racking) | Same revision problem as #17 | 🟡 mechanical rationale only |
| 19 | **Minimal 3DP — "Voron 2.4 R2 Build Guide"** ([playlist](https://www.youtube.com/playlist?list=PLXcVv43EZh9DzcPPF0IUVnpVdxQTQX8nE)) | 15 parts, Apr–Oct 2024, unboxing→wiring | **FormBot kit**, explicitly ("VORON 2.4 R2 Build Guide for the **FormBot** Kit") | Edited tutorial, 15–40 min/part · The best-structured recent mechanical series; chapter boundaries match the manual | Not the LDO kit. Different harness, board, bed, endstops. Rails/bed/probe differ | 🟡 mechanical only |
| 20 | **Build It Basement — "ULTIMATE Voron 2.4R2 Build"** ([playlist](https://www.youtube.com/playlist?list=PLjlotZjUVD32oT7YpPE89dqFwjCkVNKQ9)) | 15+ parts, Dec 2022 – Feb 2023 | 2.4r2, non-LDO; **includes Ti backers (Part 7.5) and Tap (Part 9.5)** | Edited tutorial · The only series with a dedicated **titanium-backers** episode and a gantry square-check episode (Part 8.5) | Uses Tap, not the LDO probe stack. Pre-Rev-D | 🟡 backers + gantry-square episodes only |
| 21 | **123-3D — "Building The Voron 2.4 Rev D LDO Motors Kit"** ([Part 1](https://www.youtube.com/watch?v=IushU1_ikKw) 2024-10-04 · [Part 2](https://www.youtube.com/watch?v=vpIDagUumgI) · [Part 3](https://www.youtube.com/watch?v=0cuV6iROV1k) · [Part 4](https://www.youtube.com/watch?v=QA0eMNXqI-E) 2024-11-08) | Unbox → frame/motion → electrics/gantry → first print | **Rev D**, Oct–Nov 2024 | 4 videos, ~10–15 min each (~45 min total) · **The only Rev D-specific series.** Shows the real Leviathan/Nitehawk bay layout | Far too coarse to build from — 45 minutes for a 50-hour build. Rev D, not D+ | 🟡 reference imagery only |
| 22 | **Nathan Builds Robots — "Help me build this printer! LDO Voron 2.4 Rev D Kit"** ([video](https://www.youtube.com/watch?v=hJPDsoD43dA), 2025-02-15, **10 h 13 m**) | One-sitting Rev D build | **Rev D**, Feb 2025 | Unedited livestream · Longest Rev D-specific footage in existence; good for "what does this actually look like" on the Leviathan bay | Unindexed, no chapters, real-time. Rev D, not D+ | 🟡 spot-reference (scrub to timestamp) |
| 23 | **Esoterical CAN-bus guide** — [canbus.esoterical.online](https://canbus.esoterical.online) / [repo](https://github.com/Esoterical/voron_canbus) (pushed 2026-04-23) | CAN toolhead bring-up, Katapult flashing | Current | The community standard for CAN builds | **Not applicable.** Nitehawk-SB V2 is USB; the kit ships no CAN hardware. Following it would add complexity for zero benefit | 🔴 |
| 24 | **voronldo.com "Voron Belt Tension Guide"** — [voronldo.com/guides/voron-belt-tension](https://voronldo.com/guides/voron-belt-tension/) | Belt tension numbers | "Last updated May 2025"; self-described *"independent resource site. Not affiliated with the Voron project"* | — | Publishes 350 mm targets (X 80–100 Hz, Y 75–90 Hz) that **contradict the official 110 Hz**, cites nothing, and is internally inconsistent (says Z "same as X/Y" then gives 110–130 Hz). Domain-for-sale notice on the page. Reads as SEO content | 🔴 **do not use** |
| 25 | **voron.dozuki.com** | Old wiki, step-format guides | Last revision **2019-12-09**; Voron 1.6/2.2/Afterburner | Dozuki step format | Format is right, content is 6 years obsolete | 🔴 |
| 26 | **CNC Kitchen — "Should you build a VORON 2.4 in 2023? (LDO Kit Review)"** ([video](https://youtu.be/nik-HCeOSB8), 2022-09-24) + [blog](https://www.cnckitchen.com/blog/building-a-voron-24-r2-in-2022-ldo-kit) | Review / expectation-setting | Rev A/B era | 23 min | Good expectation-setting for a first-timer; not instructional | 🟡 morale only |

---

## 3. Verdict — the single track and the per-phase overlay map

### 3.1 The spine

**Primary spine: the official Voron 2.4r2 manual PDF, pages 12–147, read through LDO's Build Notes.**
Reasons, in order of weight:

1. It is the only source that covers the whole mechanical machine at one action per illustration, with fastener callouts in place. Nothing else is even close on completeness.
2. LDO's Build Notes are a *page-indexed diff against that exact PDF*, pinned to commit `de7e89d`. That makes the two documents mechanically composable — every LDO deviation maps to a manual page number. No other kit vendor publishes this.
3. The PDF has not changed since 2023-07-18, so page numbers are stable and will stay stable. LDO's pinned link removes even that risk.
4. Everything else (videos, third-party guides) is either the wrong kit revision or the wrong vendor.

**Secondary spine: the LDO Wiring Guide Rev D, for everything from the electronics bay onward.** The manual's p.148–211 describe a machine this kit is not.

**Tertiary spine: docs.vorondesign.com Initial Startup wizard (V2 path) for bring-up, then Ellis for print tuning.**

### 3.2 Per-phase overlay map

| Phase | Follow | Overlay from | Ignore |
|---|---|---|---|
| **Prep / inventory** | LDO batch BOM for your kit serial | LDO rail grease guide; heat-set tool guide; Voron `STLs/Tools/*` jigs | — |
| **Frame** | Manual p.12–21 | LDO note p.19 (M5 precision spacer replaces every M5 shim); docs.vorondesign flat-surface guidance | — |
| **Z drives & idlers** | Manual p.22–51 | LDO notes p.29–30 (deck supports now, 4 mm — but measure), p.39 (stepper wiring per wiring guide) | — |
| **Build plate / bed** | Manual p.52–61 | LDO notes p.54 (remove film, trim magnet holes), p.55/56 **SKIP** (heatpad + fuse pre-applied), p.57 (M4×6 BHCS already fitted), p.59 (M3×**20**, not M3×16) | Manual p.55–56 entirely |
| **A/B drives & idlers** | Manual p.62–81 | LDO note p.88 (rails: use the *second* hole from each end, not the end holes) | — |
| **Gantry (X/Y, XY joints)** | Manual p.82–107 | Ti backers README (placement + M3×8 FHCS Y / M3×6 FHCS X, ~30 T-nuts); LDO printed-parts guide (`endstop_pod_D2F_switch`, `xy_joint_cable_bridge_2hole`); Build It Basement Part 7.5 for backer technique | Hall-effect endstop pods |
| **Z axis / gantry install** | Manual p.108–123 | LDO note p.114–116 (do p.115–116 first, then rest the gantry on rubber rail stoppers under the Z joints — avoids the long-zip-tie dance) | — |
| **Gantry squaring** | [docs.vorondesign.com/build/mechanical/v2_gantry_squaring.html](https://docs.vorondesign.com/build/mechanical/v2_gantry_squaring.html) (16 numbered steps, image per step) | Ellis' identical section; Build It Basement Part 8.5 | Manual's brief "SQUARING THE GANTRY" page |
| **A/B belts + tension** | Manual p.124–145 | Official tension target: **110 Hz over a 150 mm span** ([secondary_printer_tuning](https://docs.vorondesign.com/tuning/secondary_printer_tuning.html)). Z belts: **140 Hz over 150 mm** | voronldo.com numbers |
| **Toolhead** | Stealthburner manual (73 pp) + LDO note p.129–130, p.146–147 | **LDO Wiring Guide "Wiring the Toolhead PCB"** + **Nitehawk-SB V2 pinout** (§4.1 patch: PH2.0 connectors, keyed reversed fan header, no ADXL mount, `usb_adapter_mount_partial_cover.stl`) | Manual p.196 (toolhead wiring); ADXL mount |
| **Electronics bay** | **LDO Wiring Guide "Below Deck Wiring"** | Leviathan V1.3 guide (jumper removal, Pi HAT adapter, standoffs); LDO notes p.150/152/156/158–163/169–172 | Manual p.148–179 wholesale |
| **Wiring / mains** | **LDO Wiring Guide**, in order, including **Checkpoint #1** | Manual p.194–195 (cable-chain slack) + LDO cable-chain guide; LDO XY-endstop-cable repin guide if the labels read "X Stop/Y Stop" instead of "XES/YES" | Manual p.180–211 |
| **Skirts / panels** | Manual p.212–259 | LDO notes p.214–216 & 220–221 (BTT 4.3" screen — mount STL is in the **Trident** repo), p.234 (alt Z-belt cover if LEDs routed through the Z-motor opening), `power_inlet_IECGS_1mm` | mini12864 case parts |
| **Door (Clicky-Clack)** | KB3D wiki install guide | tanaes STL set; the plain acrylic panel instead of NanoNest | Stock Voron door parts (`Front_Doors/*`) |
| **Filter (Nevermore)** | [LDO Nevermore V5 Duo — V2.4 guide](https://ldomotion.com/guides/nevermore-v5-duo---v24) (step-numbered) | LDO note p.250–253 & 256 **SKIP**; print the 3×6-magnet variant + exhaust cover | Manual's exhaust filter section |
| **Firmware / Klipper** | **LDO Wiring Guide "Software Setup"** + Leviathan V1.3 guide | §4.1: use `leviathan-printer-rev-d-**sbv2**.cfg`; expect `stm32g0b1xx` in the toolboard USB ID | The wiring guide's RP2040 sentence and its config link |
| **Initial startup** | [docs.vorondesign.com Startup wizard, V2 path](https://docs.vorondesign.com/build/startup/) — 16 gated steps | Probe selection = "Stock Inductive probe" | Dockable/Tap branches |
| **Calibration / tuning** | Voron startup order, then Ellis | Voron: PID bed @100 °C, PID hotend @245 °C with fans 25%; QGL hot (bed 100 °C, hotend 150 °C) with `PROBE_ACCURACY` σ < 0.003 mm before trusting it | — |

### 3.3 Correct order of operations for the software/calibration tail

The Voron V2 wizard's own page order (extracted from `build/startup/buttons.js`) is authoritative and is **not** the order people intuit:

`Verify temperatures → Verify heaters → Verify fans → Motor checks (STEPPER_BUZZ) → XY endstop check → Homing check → Bed locating → 0,0 point → Z endstop → Probe check → **PID tuning** → **Quad Gantry Level** → Z-offset → Finish`
then, after the wizard: **extruder e-steps** → first print → **input shaper** → **pressure advance** → extrusion multiplier.

Two things people get wrong: PID tuning comes *before* QGL (a thermally unstable machine will not QGL repeatably), and input shaper/pressure advance come *after* a first successful print, not before.

---

## 4. Rev D+ deviations and first-build pitfalls

### 4.1 Rev D+ deviations from LDO's own Rev D documentation — the five that will bite

**① Wrong Klipper config file.** The Rev D wiring guide's "pre-made configuration file" link points at [`leviathan-printer-rev-d.cfg`](https://github.com/MotorDynamicsLab/LDOVoron2/blob/main/Firmware/leviathan-printer-rev-d.cfg). For Rev D+ you need [`leviathan-printer-rev-d-sbv2.cfg`](https://github.com/MotorDynamicsLab/LDOVoron2/blob/main/Firmware/leviathan-printer-rev-d-sbv2.cfg). *Every* `nhk:` pin differs, because the MCU changed family. Verified by diffing the two files:

| Function | Rev D (`nhk:` RP2040) | **Rev D+ (`nhk:` STM32G0B1)** |
|---|---|---|
| extruder step/dir/enable | `gpio23 / gpio24 / !gpio25` | `PB8 / PB9 / !PC14` |
| hotend heater | `gpio9` | `PA7` |
| hotend thermistor | `gpio29` | `PB12` |
| extruder TMC uart/tx | `gpio0 / gpio1` | `PB7 / PB6` |
| probe | `gpio10` | `PC15` |
| part fan / tacho | `gpio6 / gpio17` | `PA15 / PD2` |
| hotend fan / tacho | `gpio5 / gpio16` | `PD0 / PD1` |
| PCB LED | `!gpio8` | `!PC6` |
| neopixel | `gpio7` | `PD3` |
| ADXL cs/sclk/mosi/miso | `gpio21/18/20/19` | `PB10/PA5/PA2/PA6` |
| chamber thermistor | `gpio28` | `PB2` |
| on-board PCB temp sensor | `[temperature_sensor nh_temp]` on `gpio26` with a custom `[thermistor CMFB103F3950FANT]` | **removed — does not exist on V2** |

Loading the V1 config on a V2 board mis-drives the heater, thermistor, probe, both fans and the accelerometer simultaneously.

**② Wrong USB serial-ID pattern.** The wiring guide says: *"The Nitehawk uses an RP2040 MCU, therefore its ID will be in a format similar to `usb-Klipper_rp2040_…`"*. On Rev D+ it will be an **STM32G0B1** ID (`usb-Klipper_stm32g0b1xx_…`). If you match by the documented pattern you will assign the *mainboard's* ID to `[mcu nhk]` or fail to find the board at all. (Mainboard is unchanged: STM32F446, `usb-Klipper_stmf446xx_…`.)

**③ Connectors changed from JST-XH2.5 to JST-PH2.0** on **PROBE, TH0 and XY-Endstop**. The wiring guide still says *"The connector type to use is JST-XH2.5 two pin"* for the hotend thermistor. Consequence: any aftermarket or spare thermistor/probe pigtail crimped to the documented XH2.5 will not fit, and the smaller PH2.0 housings are easy to force into the wrong header. The heater screw terminal and E0508 ferrule spec are unchanged.

**④ Fan-adapter PCB header gender reversed and now keyed.** The 2×10 board-to-board interface between the Stealthburner fan adapter and the main toolboard is physically different from every Rev D photo. The keying is the check — if it does not drop in, you have it backwards; do not press harder.

**⑤ USB-adapter mount cover changed, and there is an undocumented grounding scheme.** The printed-parts guide points at the V1 `cw2_captive_pcb_cover.stl`/`usb_adapter_mount.stl` cover; Rev D+ uses [`usb_adapter_mount_partial_cover.stl`](https://github.com/MotorDynamicsLab/Nitehawk-SB-V2/blob/master/STLs/usb_adapter_mount_partial_cover.stl), whose whole purpose per the board doc is *"a newly designed cover exposes one of the mounting points to connect a grounding point."* The V2 repo ships `Images/grounding_scheme.jpg`, `Images/toolboard_ground_routing.jpg` and `Images/usb_adapter_gnd.jpg` with **no accompanying prose in any LDO document**. Given the change list also claims *"Vastly Improved ESD performance"*, treat the grounding images as a required build step and ask in `#ldo_motors` before wiring the bay.

**Update 2026-09-05:** LDO gained an "ESD Hardening" section on 2026-07-10 at [docs.ldomotors.com/en/Toolboard/nitehawk-sb-v2#esd-hardening](https://docs.ldomotors.com/en/Toolboard/nitehawk-sb-v2#esd-hardening), which now documents the discharge path (extruder motor body → toolboard ground → umbilical → USB adapter → frame → earth) with supplied grounding cables. See `docs/manual/10-wiring.md` step 10.58 for the transcribed wording. `#ldo_motors` is now only the fallback for a kit missing the grounding cables.

**Sixth, benign:** the secondary USB port on the toolhead is the actual "+" feature. Nothing to do now (Beacon/Cartographer deferred), but leave enough umbilical slack that the port stays reachable without pulling the toolhead.

### 4.2 Rev D deviations from the official manual (all from LDO Build Notes, page-indexed)

Pre-load or test-fit roll-in T-nuts — LDO warns extrusion/T-nut tolerances are tight.

| Manual page | Deviation |
|---|---|
| 19 | Brass **M5 precision spacer** replaces the M5 shim — everywhere in the manual unless noted |
| 29–30 | Install deck supports now; use `deck_support_4mm_x8` (but see §4.3) |
| 29 | DIN rails run **left to right** (LDO), not front-to-back as manual p.29 draws — *"These DIN rails run from left to right"* (`S0_Din_Raill.jpg`). Every LDO component position in the bay depends on this orientation. See `docs/manual/09-electronics-bay.md` step 09.5 |
| 39 | Stepper wiring per the LDO wiring guide, not the manual |
| 54 | Remove bed protective film; after applying the magnet sheet, trim the bolt holes |
| 55, 56 | **SKIP** — heatpad and thermal fuse pre-applied |
| 57 | Use the M4×6 BHCS already fitted to the bed |
| 59 | M3×**20** SHCS, not M3×16 (thicker bed + spacers) |
| 88 | Do not use the end holes of the rails; use the second holes in |
| 104 | Black M5 washer instead of the M5 shim (cosmetic) |
| 114–116 | Do 115–116 first, then rest the gantry on rubber rail stoppers under the Z joints |
| 129–130 | Verify the correct X-carriage for Clockwork 2; follow the Stealthburner manual |
| 143 | Insulate the inductive probe with the supplied fibreglass tape (front + sides only; **not** the back or bottom) |
| 145 | **SKIP** — no hall-effect endstops |
| 146–147 | Stealthburner + CW2 per the SB manual |
| 149 | Kit wiring differs; **no 5 V PSU** |
| 150 | **SKIP** the manual's Pi bracket; the Beefy Pi Mount explicitly *does not apply to Rev D* — the Pi mounts to the Leviathan on standoffs with the Pi 3/4 HAT power adapter |
| 152, 172, 190 | **SKIP** — no 5 V PSU; the Leviathan supplies the Pi 5 V |
| 156 | Use `power_inlet_IECGS_1mm` (1.0 mm AC inlet with integrated switch) |
| 158–160, 163 | LDO Z-endstop printed part + PCB; LDO XY endstop PCB |
| 162, 169 | **SKIP** — XY endstop board; no support bracket |
| 170–171, 182–189, 192–193, 205–209 | **SKIP** — see wiring guide |
| 194–195 | Keep drag-chain wiring **loose** — taut wires fatigue and break |
| 196 | **SKIP** — toolhead PCB |
| 214–216, 220–221 | BTT 4.3" touchscreen; mount STL in the **Trident** repo; wiring/rotation per LDO's `btt_43_rotate_guide` |
| 234 | Alternate Z-belt cover if LEDs are routed through the Z-motor opening |
| 250–253, 256 | **SKIP** — follow LDO's Nevermore guide instead |

### 4.3 Conflicts between sources, and what to do

| Conflict | Positions | Recommendation |
|---|---|---|
| **Deck panel thickness** | LDO Build Notes p.29–30 and the Printed Parts Guide both say the deck is **4 mm** → print `deck_support_4mm_x8`. The Rev D 350 BOM lists "Deck Panel, Acrylic, Black, 469×469×**3** mm" (and Bottom Panel at 4 mm) | **Caliper the actual deck panel on arrival.** Print *both* `deck_support_3mm_x8` and `deck_support_4mm_x8` (16 small parts, minutes of print time) and fit whichever matches. Do not resolve this from documents |
| **A/B belt tension** | Official manual: no number at all — "cut both belts to the same length" (p.125). Voron docs: **110 Hz over a 150 mm span**, ≈2 lb, deliberately at the low end. voronldo.com: 80–100 Hz for a 350 | **Use 110 Hz / 150 mm span from docs.vorondesign.com.** It is the only sourced, official number and it names the span, which is what makes a frequency meaningful. Discard voronldo.com |
| **Z belt tension** | Voron docs: **140 Hz** with the fixed side 150 mm from the Z idler centres. voronldo.com: "same as X/Y, 110–130 Hz" | 140 Hz / 150 mm, official. Also the QGL troubleshooting text points at uneven Z belts when σ is high — tension all four, evenly |
| **Klicky vs. Omron** | Kit ships both. LDO config and wiring guide assume the Omron inductive probe (QGL only) with the LDO nozzle probe as the Z endstop. `CLAUDE.md` currently records "Stock kit ships Klicky … instead" | **Build stock: Omron inductive + LDO nozzle probe.** Klicky is an optional mod that adds a dock, macros and a calibration procedure. Keep the Klicky parts bagged for later. *This is a correction to `CLAUDE.md`* |
| **Pi OS version** | LDO wiring guide: "Raspberry Pi OS Lite (32-bit)". Leviathan V1.3 guide: "we recommend Raspberry Pi OS lite (Legacy) Bullseye", and carries a Bullseye-specific `udev` bug fix for a broken `/dev/serial/by-id/` | On a Pi 4B, take the wiring guide's path (current Pi OS Lite) but **know the Bullseye `/dev/serial/by-id` bug and its fix** — if `ls /dev/serial/by-id/*` comes up empty, that's the first thing to check |
| **`nh_temp` sensor** | V1 config exposes a Nitehawk PCB temperature sensor; the V2 config removes it | Do not add it back. It does not exist on the V2 board |

### 4.4 First-build pitfalls, ranked

1. **Frame squaring is the one irreversible quality decision.** Build on the verified-flat stone counter, check both diagonals and both faces, and re-check after every bolt-tightening pass (manual p.16–17: "BUILD ON A FLAT SURFACE", "CHECK FOR SQUARENESS"). Everything downstream inherits this.
2. **Gantry racking/squaring must happen after the gantry is in and *before* A/B belts are tensioned.** The official procedure ([v2_gantry_squaring](https://docs.vorondesign.com/build/mechanical/v2_gantry_squaring.html)) starts by *fully releasing A/B belt tension* and *dropping the lower Z joints*. Tension the A/B belts first and you will undo them.
   - **Update 2026-09-05:** the manual deliberately inverts this. Squaring needs motor control (`G28`, `QUAD_GANTRY_LEVEL`, `SET_STEPPER_ENABLE`), so it runs out of Ch 13 as **Ch 06b**. Ch 07 sets *provisional* tension only; final A/B tension is Ch 06b Step 06b.15 / Ch 14 Step 14.4.
3. **Titanium backers go on during gantry assembly, on the face opposite the rail.** Y-axis backers on **top** of the Y extrusions; X-axis backer on the **rear** of the X extrusion, opposite the MGN12. The README is blunt: *"If you have a single MGN12 but decide to put a backer on top, you will be actively contributing to the problem of bimetallic expansion!"* Fasteners: M3×8 FHCS (Y), M3×6 FHCS (X), ~30 T-nuts, Torx preferred (M3 FHCS cams out easily in countersinks).
4. **Heat-set inserts (153 of them) go in before assembly, not during.** A missed insert in an XY joint means a gantry teardown. Batch them per printed-part group, use the supplied brass tip with the tongue adjusted flush to the insert height, and practise on `STLs/Test_Prints/Heatset_Practice.stl` first.
5. **Rails ship dry and must be cleaned and packed before installation** — the flip-and-pack method requires access to the back of the rail, i.e. *before* it goes on an extrusion. IPA soak 10 min, dry fully, pack NLGI 0/1 grease (Super Lube 21030) through a mounting hole until it oozes past the bearings, wipe the rail surface clean. Rail carriages slide off the ends easily and are ruined by a drop.
6. **Use the second mounting hole from each end of every rail, never the end hole** (LDO note p.88). Also use the printed `MGN9_rail_guide_x2` / `MGN12_rail_guide_x2` jigs to centre rails on the extrusion.
7. **Z pulleys: 16T on the Z motors, 20T elsewhere — they look nearly identical.** Threadlocker is pre-applied to the set screws; get orientation and stack height right the first time (`pulley_jig.stl`).
8. **Mains wiring is the one step that can kill you.** Do LDO's *Checkpoint #1* with a multimeter, unplugged: continuity within each colour group, no continuity between L/N/PE, and confirm the PSU's 115/230 V selector **before** the first power-on. The SSR wiring is called out as *"critical — an incorrect connection can cause catastrophic damage"*; watch the numbered terminals and the yellow LED position.
9. **Leviathan voltage-selection jumpers must be removed before installation** and only re-inserted after each attached component's voltage is verified. Mixing voltages on a shared 24 V supply "will permanently damage the controller and attached components."
10. **Never unplug or re-plug a stepper with power on, and never hand-spin a connected stepper fast** — back-EMF kills drivers.
11. **Bed tacos come from tightening the bed cold and heating fast.** Community guidance: one screw tight, two firm, one loose or absent.
12. **Stealthburner LEDs:** the kit's diffuser is clear PETG (supplied printed). `chain_count: 3`, `color_order: GRBW` in the LDO config — a mismatch here shows up as wrong colours, not as a failure.
13. **Drag chains: keep the wires loose inside the chain.** Taut wires fatigue and break — this is the single most-repeated LDO warning.
14. **XY endstop cable mis-labelling.** LDO documents a known batch where the cables are labelled "X Stop / Y Stop" instead of "XES / YES" and need re-pinning ([XY_Endstop_Cable_Reconnecting_Guide](https://docs.ldomotors.com/en/guides/XY_Endstop_Cable_Reconnecting_Guide)). Check labels before wiring.
15. **The stock config ships with every build-size option commented out.** For a 350 you must uncomment: `position_endstop: 350` and `position_max: 350` in `[stepper_x]` **and** `[stepper_y]`; `position_max: 330` in `[stepper_z]`; and the 350 `gantry_corners` (`-60,-10` / `410,420`) plus `points` (`50,25 / 50,275 / 300,275 / 300,25`) in `[quad_gantry_level]`. There is **no `[bed_mesh]` section at all** in the LDO config — add one (a 350 with a heated chamber will want a per-print mesh).
16. **Calibration order:** PID before QGL; QGL hot (bed 100 °C, hotend 150 °C) and only once `PROBE_ACCURACY` shows σ < 0.003 mm with no trend — a cold printer takes 10–20 minutes to stabilise. E-steps before the first print (`rotation_distance: 22.6789511`, `gear_ratio: 50:10` for CW2). Input shaper and pressure advance *after* a successful first print.

---

## 5. Build-phase plan (print/assemble interleave)

### 5.1 Phase table

Hours are **first-build, hands-on**, for two people (one adult, one 13-year-old) working carefully with a written procedure. Basis: apportioned across the community-standard 40–60 h first-build envelope (LDO/Voron community; also recorded in `CLAUDE.md`) weighted by official-manual page count per chapter (Frame 10 pp, Z Drives 30, Build Plate 10, A/B Drives 20, Gantry 26, Z Axis 16, A/B Belts 22, Electronics 26, Wiring 32, Skirts 28, Panels 20) plus the Stealthburner manual's 73 pp, with an explicit uplift for the 153 heat-set inserts and for teaching-as-you-go. Ranges, not points — treat the low end as "everything fits first time".

Printed-part groups map to the Voron STL tree (`github.com/VoronDesign/Voron-2/tree/Voron2.4/STLs`), which is organised by build phase. Parts LDO ships **already printed** are excluded (Leviathan brackets, DIN clips, NH adapter mount, CW2 chain anchor, splitter spacers, LDO nozzle probe, bed WAGO mount, SB LED diffuser, CW2 PCB spacer).

| Phase | Hands-on (h) | Printed parts needed to start | Prereq phases | Runnable with **no** self-printed parts? |
|---|---|---|---|---|
| **P00 Prep, inventory, rail prep, jigs** | 2.5–4.0 | *Jigs and coupons:* `Tools/MGN9_rail_guide_x2`, `Tools/MGN12_rail_guide_x2`, `Tools/pulley_jig`, `Tools/bed_hole_marking_template_x1_Rev2`, `Tools/bottom_panel_template`, `Test_Prints/Heatset_Practice`, `Test_Prints/Voron_Design_Cube_v7` — **Update 2026-09-05:** these print in **Prusament ASA Galaxy Black** as batch **B00**, not PLA: the cube is the ASA dimensional gate and the heat-set coupon has to be in the build material or the iron temperature you find is wrong for all 150 remaining inserts. Only **three** Tools jigs are actually printed in B00 (`MGN9_rail_guide_x2`, `MGN12_rail_guide_x2`, `pulley_jig`); the two templates are optional extras deferred per print plan §4.2. See `docs/manual/print/B00-calibration-and-jigs.md`. | — | ✅ (printable day one, months before the kit lands) |
| **P01 Frame assembly + squaring** | 2.5–4.0 | **none** | P00 | ✅ |
| **P02 Z drives, Z idlers, Z rails, deck** | 5.0–7.0 | `Z_Drive/*` (10 files), `Z_Idlers/*` (3), `Panel_Mounting/deck_support_{3,4}mm_x8` | P01 | ❌ |
| **P03 Build plate / bed** | 1.5–2.5 | **none** (verified: no printed parts in `STLs/` for the Build Plate chapter; feet are rubber, supplied; there is no printed bed mount) | P01 | ✅ |
| **P04 A/B drives + idlers** | 3.5–5.0 | `Gantry/AB_Drive_Units/*` (6), `Gantry/Front_Idlers/*` (6) | P01 | ❌ |
| **P05 Gantry: X/Y axes, XY joints, X carriage, Ti backers** | 5.0–7.0 | `Gantry/X_Axis/XY_Joints/*` (MGN12 set + `[a]_endstop_pod_D2F_switch` + `[a]_xy_joint_cable_bridge_2hole`), `Gantry/X_Axis/X_Carriage/x_frame_V2TR_MGN12_{left,right}`, `probe_retainer_bracket` | P04 | ❌ |
| **P06 Z axis: gantry install, Z belts, gantry squaring** | 3.5–5.0 | `Gantry/Z_Joints/{z_joint_lower_x4, z_joint_upper_x4}`, `Gantry/[a]_z_belt_clip_{lower,upper}_x4`, `Gantry/z_chain_{bottom_anchor,guide}`, `Gantry/AB_Drive_Units/[a]_z_chain_retainer_bracket_x2` | P02, P05 | ❌ |
| **P07 A/B belts + tension** | 2.5–4.0 | `Gantry/Front_Idlers/[a]_tensioner_{left,right}` (from P04), `Gantry/AB_Drive_Units/[a]_cable_cover` | P06 | ❌ |
| **P08 Toolhead: Stealthburner + CW2 + Nitehawk V2** | 3.0–4.5 | Stealthburner + Clockwork 2 sets ([Voron-Stealthburner repo](https://github.com/VoronDesign/Voron-Stealthburner)), plus `Nitehawk-SB/STLs/cw2_captive_pcb_cover` (LDO's variant with chamber-thermistor anchor) and **`Nitehawk-SB-V2/STLs/usb_adapter_mount_partial_cover`** | P05 | ❌ |
| **P09 Electronics bay: DIN rails, ducts, board mounting, endstops, Pi** | 2.5–4.0 | `Electronics_Bay/wago_221-415_mount_3by5` only (everything else LDO-supplied printed) — **Update 2026-09-05:** superseded. Ch 09 consumes **six** printed parts: `lrs_200_psu_bracket_x2` ×2, the WAGO mount, `pcb_din_clip_x3`, `PSU_stabilizer_50mm`, `usb_adapter_mount_partial_cover` (all batch B07) and `power_inlet_IECGS_1mm` (plate B07-P3). The PSU brackets in particular are self-printed. See `docs/manual/09-electronics-bay.md`. | P02 | ❌ |
| **P10 Wiring: above-deck, below-deck, mains, Checkpoint #1** | 5.0–7.0 | `Skirts/power_inlet_IECGS_1mm`, COB light-strip mounts ([`LDOVoron2/STLs` COB Light Strip Mount](https://github.com/MotorDynamicsLab/LDOVoron2/tree/main/STLs)) | P06, P08, P09 | 🟡 two small parts |
| **P11 Skirts, panels, doors (Clicky-Clack), Nevermore, spool holder** | 4.0–6.0 | `Skirts/350/*` (5), `Skirts/[a]_*` grills/guards/keystone, `Panel_Mounting/*` clips + `z_belt_cover_{a,b}`, Clicky-Clack set (tanaes), Nevermore Micro V5 Duo 3×6-magnet set, `Spool_Management/*` | P10 | ❌ |
| **P12 Software: Pi image, Klipper/Moonraker/Fluidd/KlipperScreen, firmware, printer.cfg** | 2.0–3.0 | **none** | (hardware from P09/P10 for final wiring, but the whole flash+install can be bench-done on day one) | ✅ |
| **P13 Initial startup: verify temps/heaters/fans/motors/endstops, bed locating, 0,0, Z endstop, probe check, PID, QGL, Z offset** | 2.5–4.0 | **none** | P10, P12 | ❌ (needs the machine) |
| **P14 Tuning: e-steps, first print, input shaper, pressure advance, EM, first-layer** | 2.5–4.0 | **none** | P13 | ❌ |
| **Totals** | **47.5–71.0** (mid ≈ 59) | | | |

Reality check on the total: the low end (47.5 h) sits inside the community 40–60 h first-build envelope; the mid-point (≈59 h) sits at its top edge and the high end runs past it. That is the honest expectation for a first Voron built alongside a 13-year-old from a written procedure — the second pair of hands genuinely helps at gantry install and belt routing, but explaining every step costs more than it saves. Unattended print time is separate (~100 h).

**Correction to `CLAUDE.md`:** it records "only ~15% of the build (by time) is possible before any printed parts exist" and lists "feet + bed mounts" as a print batch gating the bed. Both are wrong. P00+P01+P03+P12 = **8.5–13.5 h** out of 47.5–71.0 h, i.e. **~18–19%** of the build with zero self-printed ASA parts. And the Build Plate chapter needs **no printed parts at all** — the 2.4r2 STL tree contains no bed mount and no feet (feet are supplied rubber).

### 5.2 Wrong-order pitfalls that cost rework

| # | Pitfall | Cost if missed | Guard |
|---|---|---|---|
| W1 | A/B belts tensioned before gantry squaring | Full de-tension + belt-clamp release; ~1.5 h | Gate P07 on P06's squaring sign-off. **Update 2026-09-05:** revised — squaring needs motor control, so it runs out of Ch 13 as Ch 06b. Ch 07 sets *provisional* tension only; final tension is Ch 06b Step 06b.15 / Ch 14 Step 14.4. |
| W2 | Ti backers fitted after the gantry is assembled/installed | Gantry teardown; ~3 h | Backers are a numbered step *inside* P05, before XY joints are torqued |
| W3 | Heat-set inserts missed in a printed part | Disassemble whatever the part is in; 0.5–3 h | Insert pass is a gated checklist per print batch, before the part enters any phase |
| W4 | Deck supports not fitted at manual p.29–30 | Deck out, frame partly apart; ~1 h | LDO note is a step inside P02, not P11 |
| W5 | LED strips + extrusion covers routed after the top frame is closed / panels on | Top panel and covers off again; ~0.5 h | LED routing is a numbered step in P10 that runs *before* P11 |
| W6 | Bed magnet applied without trimming the bolt holes (manual p.54 vs p.59) | Peel and re-apply magnet, or drill through the magnet; risk of ruining it | Trim step immediately after magnet application in P03 |
| W7 | Toolhead umbilical not threaded through the drag chain before the chain ends are mounted | Chain disassembly; 0.5 h | P08→P10 handoff step: "pull cable, then mount chain ends" |
| W8 | Electronics bay closed (skirts + bottom panel on) before Checkpoint #1 | Full re-open; 1 h + the safety risk of skipping it | Checkpoint #1 is a hard gate at the end of P10; P11 cannot start until it passes |
| W9 | Rails installed before cleaning/greasing | Rails off again, or run them dry and wear them out | Rail prep is P00, explicitly before P02/P05 |
| W10 | Rails mounted using the end holes (manual default) instead of the second holes | Rail off, re-position, re-align | LDO p.88 note is inlined at the step, not in an appendix |
| W11 | Nevermore vs. stock exhaust decided after the back panel is sealed | Back panel off, different exhaust cover printed; 1 h + a reprint | Decide in P00 (it's Nevermore — the kit has no exhaust fan); print the matching exhaust cover in the same batch as the skirts |
| W12 | Z-motor pulley set screws not threadlocked/seated before Z belting | Belt slip under load, re-belt all four; 1.5 h | Set-screw + `pulley_jig` verification step inside P02 |
| W13 | Wrong Klipper config loaded (Rev D vs Rev D+) at P12 | Mis-driven heater/probe/fans at P13; potentially a damaged component | P12 step 1: confirm the toolboard ID reads `stm32g0b1xx`; if it reads `rp2040` you have a V1 board and the *other* config |
| W14 | `position_max` / QGL points left commented out for the 350 | Homing crashes into the frame at P13 | P12 config-edit checklist with the exact 350 values |

---

## 6. Gap analysis vs. a Prusa-style manual

Baseline: the Prusa Core One+ kit manual — numbered steps, one photo per step, a per-step parts strip showing exact fasteners and counts, bold "what you should see" checks, chapter structure with time estimates, and everything he needs on one page.

| Prusa property | Best existing Voron/LDO equivalent | Gap |
|---|---|---|
| **Numbered steps** | ldomotion.com guides ("Step 3 of 7 in this section"); the Voron startup wizard (progress bar, gated Next). Neither covers assembly | **Missing for the entire mechanical build.** The 2.4r2 manual has page numbers, not step numbers |
| **One photo per step** | LDO wiring guide: 39 images across ~16 sections; hi-res originals in `LDOVoron2/Images/WiringGuide/RevD` (19 build shots). LDO printed-parts guide: 20. KB3D Clicky-Clack: 34. LDO Nevermore: 37 | **Partly solved for electrical/filter/door; absent for mechanical.** The manual's images are CAD renders, not photos — but they are actually *better* than photos for exploded fastener geometry. One render per manual page already exists |
| **Per-step fastener list with counts** | Manual draws callouts in the image (e.g. "M5×16 BHCS", "M3 T-Nut") but never tabulates them. LDO BOM gives whole-kit totals only | **Missing.** Derivable: per-chapter fastener sets are extractable from the PDF text layer (already done, §5.4); per-*step* counts require reading the renders |
| **"What you should see" checks** | Manual has a few: "CHECK FOR SQUARENESS", "CHECK YOUR WORK", "CHECK SHAFT POSITION", "CHECK FOR BELT", "VERIFY PLATE PLACEMENT", "CHECK POSITION". LDO has exactly one real one ("Checkpoint #1"). Voron startup wizard is entirely built from checks | **Mostly missing.** ~8 checks across 263 pages vs. Prusa's per-step cadence |
| **Time estimates** | None anywhere | **Missing.** §5.1 supplies them |
| **Single document, no cross-referencing** | It currently takes 4 documents open at once (manual PDF + build-notes wiki + wiring wiki + printed-parts wiki), plus a fifth for Rev D+ | **The core problem.** This is exactly what the consolidation solves |
| **Tools/consumables per chapter** | Wiring guide has a 3-item tool list; nothing else | **Missing.** §7.3 supplies them |
| **Warnings/safety inline** | Manual has a good intro warning; LDO has the mains warning and Checkpoint #1 | Adequate, needs re-siting inline |
| **Print-batch interleave** | Nothing. Every source assumes parts already exist | **Entirely missing** — and it is the single biggest difference between a kit build and this build |

**What already exists and must not be re-created:** 263 exploded CAD renders (one per action) at print quality; 19 hi-res GPL-licensed Rev D wiring photos; a complete, current, page-indexed deviation list; a complete per-batch BOM with check columns; a gated startup wizard; a mature tuning guide; step-numbered photo guides for Leviathan firmware, Nevermore and the Clicky-Clack door. The gap is **assembly, indexing, per-step fastener tables, checks and Rev D+ patching** — not content creation.

---

## 7. Proposal — the consolidated instruction set

### 7.1 Recommended shape and the deciding criterion

**Two production modes, chosen per chapter by whether a good visual already exists:**

- **Mode A — "index and embed" (mechanical chapters, P01–P07):** do **not** re-draw or re-photograph. Render each manual page to PNG (`pdftoppm -r 200 -png -f N -l N`, verified working — 263 pages ≈ 60 MB), then write numbered steps *around* the render, adding the fastener table, the check, and the inline LDO deviation. Roughly 1.5–2.5 steps per manual page. This is ~4× faster than transcription and loses nothing, because the render *is* the best available illustration.
- **Mode B — "write it properly" (P00, P08–P14):** these chapters have no single good source, or the good source is wrong for Rev D+. Write full steps, embed LDO's GPL images by raw URL, and photograph the gaps during the build.

Deciding criterion: *does one existing image already show the exact action?* If yes → Mode A. If no, or if the image shows the wrong revision → Mode B.

**Format: a static site generated from Markdown, plus a print-to-PDF path.** Markdown because the content is 90% text + image reference and must be diffable and patchable when LDO updates a guide; a static site because the build happens at a bench with a tablet and a 350 MB PDF is miserable there; a PDF export because the shop tablet may not have Wi-Fi in the basement. Concretely: one `.md` per chapter, images in a sibling directory, built with any Markdown→HTML static generator, plus `weasyprint`/`prince`/browser-print for PDF. Not a wiki (no offline), not a bare PDF (no incremental patching).

### 7.2 Chapter outline — writing spec

Each row is a chapter file. **Source** = what the writer transcribes from, with exact page ranges / section anchors / URLs. **Steps** = expected numbered-step count. **Mode** per §7.1.

---

**Ch 00 — Before you start: inventory, tools, jigs, rail prep** · Mode B · ~25 steps · 2.5–4.0 h
- **Sources:** LDO batch BOM for the kit serial ([350_BOM/HOME](https://docs.ldomotors.com/en/voron/voron2/350_BOM/HOME) → the batch page); manual p.4–11 (Part Printing Guidelines, File Naming, Hardware Reference, Blind Joint Basics, Ball-End Driver); [LDO rail grease guide](https://docs.ldomotors.com/guides/rail_grease_guide); [LDO heat-set insert tool guide](https://docs.ldomotors.com/guides/heatset_insert_tool_guide); [LDO cable chain guide](https://docs.ldomotors.com/guides/cable_chain_guide); [Printed Parts Guide Rev D](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d).
- **Printed parts:** the five `STLs/Tools/*` jigs + `Test_Prints/Heatset_Practice` + `Voron_Design_Cube_v7`, all PLA on the Prusa.
  - **Update 2026-09-05:** superseded. Batch **B00** prints in **Prusament ASA Galaxy Black**, not PLA — the cube is the ASA dimensional gate and the heat-set coupon must be the build material. And only the **three** jigs actually used are printed (`MGN9_rail_guide_x2`, `MGN12_rail_guide_x2`, `pulley_jig`); `bed_hole_marking_template_x1_Rev2` and `bottom_panel_template` are optional extras deferred per print plan §4.2. See `docs/manual/print/B00-calibration-and-jigs.md`.
- **Hardware consumed:** none. Consumes IPA, grease, soldering iron + brass tip.
- **Rev D+ deviations to apply:** substitute `usb_adapter_mount_partial_cover.stl` (V2 repo) for the V1 cover in the print list; add the Nitehawk-SB-V2 grounding images to the "questions to ask in `#ldo_motors`" box.
- **Also:** the print-batch plan and a "verify with the Voron cube before committing to batch 1" gate.

**Ch 01 — Frame** · Mode A · ~22 steps · 2.5–4.0 h
- **Sources:** manual **p.12–21** (SORT EXTRUSIONS, PREPARE 8 EXTRUSIONS, EXTRUSION REFERENCE, FRAME ASSEMBLY, BUILD ON A FLAT SURFACE, CHECK FOR SQUARENESS, POSITION BED EXTRUSIONS); LDO note **p.19**.
- **Printed parts:** none.
- **Hardware:** M5×16 BHCS, M5×10 BHCS, M5 roll-in T-nut, **M5 precision spacer** (not shim).
- **Rev D+ deviations:** none. (Rev D deviation: precision spacer substitution, everywhere from here on.)
- **Checks to author:** diagonal equality both faces; extrusion faces flush at every corner; frame sits on all four points on the reference surface with no rock.

**Ch 02 — Z drives, Z idlers, Z rails, deck** · Mode A · ~60 steps · 5.0–7.0 h
- **Sources:** manual **p.22–51** (LINEAR RAIL BASICS, RAIL SAFETY, CENTRED RAIL INSTALLATION GUIDE, Z RAILS, Z DRIVE ×4, Z IDLER ×4, HEAT SET INSERTS, APPLY THREAD LOCKER, SET SCREWS, CLOSE THE BELT TENSIONER, DECK PANEL, DIN RAIL SLOTS); LDO notes **p.29–30**, **p.39**.
- **Printed parts:** `Z_Drive/*` ×10, `Z_Idlers/*` ×3, `Panel_Mounting/deck_support_{3,4}mm_x8`.
- **Hardware:** M3×8/×16/×40 SHCS, M3 nut, M3 T-nut, M5×10/×16/×30 BHCS, M5×40 SHCS, M5 nut, M5 precision spacer, M5 T-nut, 625 bearings ×12, 16T pulleys ×4, 80T pulleys ×4, 20T 9 mm idlers ×4, 5×60 mm shafts ×4, closed 2GT 6×188 loops ×4, M4×4 set screws (pre-threadlocked).
- **Rev D+ deviations:** none. **Deck thickness gate** (§4.3) — measure, then choose the support.

**Ch 03 — Build plate** · Mode A · ~20 steps · 1.5–2.5 h
- **Sources:** manual **p.52–61** (HEATED BED, MAGNET APPLICATION, HEATER APPLICATION, THERMAL FUSE, HEATER/THERMISTOR WIRES, BED AND SPACER THICKNESS, VERIFY PLATE PLACEMENT, WIRE PASSTHROUGH); LDO notes **p.54, 55 (SKIP), 56 (SKIP), 57, 59**; wiring guide [§ Wiring the Bed Heater](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#wiring-the-bed-heater) for the bed harness breakout.
- **Printed parts:** none (bed WAGO mount is LDO-supplied printed).
- **Hardware:** M3×20 SHCS ×4 (**not** M3×16), M3 washers, thumb nuts, M4×6 BHCS (pre-fitted), M4 + serrated washer for bed PE.
- **Rev D+ deviations:** none.
- **Checks:** magnet fully rolled with no bubbles; bolt holes trimmed *before* bolting; bed sits with even gap on all four thumb nuts.

**Ch 04 — A/B drives and idlers** · Mode A · ~40 steps · 3.5–5.0 h
- **Sources:** manual **p.62–81** (OVERVIEW, PREPARATION, A DRIVE, B DRIVE, A IDLER, B IDLER, ASSEMBLY AID, MOTOR ORIENTATION, APPLY THREAD LOCKER, UPSIDE DOWN ASSEMBLY, CHECK YOUR WORK).
- **Printed parts:** `Gantry/AB_Drive_Units/{a,b}_drive_frame_{lower,upper}`, `Gantry/Front_Idlers/front_idler_{left,right}_{lower,upper}`.
- **Hardware:** M3×30/×40 SHCS, M3 washer, M5×30 BHCS, M5×40 SHCS, M5 nut, M5 precision spacer, F695 bearings, 20T 9 mm pulleys ×4.
- **Rev D+ deviations:** none.

**Ch 05 — Gantry: X and Y axes, XY joints, X carriage, titanium backers** · Mode A + inserted Mode B · ~55 steps · 5.0–7.0 h
- **Sources:** manual **p.82–107** (PREPARATION, Y AXIS, T-NUT ORIENTATION, X AXIS, XY JOINTS left/right, CENTRED RAIL INSTALLATION GUIDE, X CARRIAGE prep, CABLE PATH, FLIP GANTRY, CHECK YOUR WORK); LDO note **p.88**; printed-parts guide (`[a]_endstop_pod_D2F_switch`, `[a]_xy_joint_cable_bridge_2hole`); **Mode B insert:** [extrusion_backers README](https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers) + [Build It Basement Part 7.5](https://youtu.be/BHUxiEEnyGg) for backer technique.
- **Printed parts:** `X_Axis/XY_Joints/xy_joint_{left,right}_{lower,upper}_MGN12`, `[a]_endstop_pod_D2F_switch`, `[a]_xy_joint_cable_bridge_2hole`, `X_Carriage/x_frame_V2TR_MGN12_{left,right}`, `probe_retainer_bracket`.
- **Hardware:** M3×8/×16 SHCS, M3 T-nut, M5×10/×16/×30 BHCS, M5×40 SHCS, M5 nut/precision spacer/T-nut; **backers:** M3×8 FHCS (Y), M3×6 FHCS (X), ~30 T-nuts.
- **Rev D+ deviations:** none (D2F endstop pod is a Rev C+ deviation).
- **Checks:** backer on the face *opposite* the rail; XY joints not rotated; X carriage runs the full X travel with no bind.

**Ch 06 — Z axis: gantry install, Z belts, and squaring the gantry** · Mode A + Mode B tail · ~38 steps · 3.5–5.0 h
- **Sources:** manual **p.108–123** (Z JOINTS, INSTALL REMAINING JOINTS, GANTRY INSTALL, A HELPING HAND, GANTRY ALIGNMENT, Z BEARING BLOCKS, Z BELT ROUTING, LOOSEN TOP BELT CLAMPS, PULL TIGHT AND SECURE BELT CLAMP, EXCESS BELT, REPEAT ×4, SQUARING THE GANTRY); LDO note **p.114–116** (rubber rail stoppers trick); **Mode B tail:** the full 16-step [V2 Gantry Squaring](https://docs.vorondesign.com/build/mechanical/v2_gantry_squaring.html) procedure with its 10 images — **note this procedure needs a working printer** (`SET_IDLE_TIMEOUT`, `G28`, `QUAD_GANTRY_LEVEL`, `SET_STEPPER_ENABLE`), so the chapter ends with a "return here after Ch 13" pointer.
- **Printed parts:** `Gantry/Z_Joints/z_joint_{lower,upper}_x4`, `[a]_z_belt_clip_{lower,upper}_x4`, `z_chain_{bottom_anchor,guide}`, `[a]_z_chain_retainer_bracket_x2`.
- **Hardware:** M3×20/×30 SHCS, M5×30 BHCS, M5×40 SHCS, M5 nut; Gates 2GT 9 mm belt.
- **Rev D+ deviations:** none.
- **Structural note for the writer:** this is the one place where a purely linear manual breaks. Split into **Ch 06a** (install + belt, mechanical) and **Ch 06b** (squaring, requires firmware) and put 06b immediately after Ch 13.

**Ch 07 — A/B belts and tensioning** · Mode A · ~40 steps · 2.5–4.0 h
- **Sources:** manual **p.124–145** (THE VORON BELT PATH, OVERVIEW A BELT / B BELT, BELTING IDLERS, EXTEND IDLER, CLAMP BELTS, PULL TIGHT, LEAVE LOOSE, PROBE WIRES, X CARRIAGE, CHECK YOUR WORK); **tension target from** [secondary_printer_tuning § Belt Tension](https://docs.vorondesign.com/tuning/secondary_printer_tuning.html) — 110 Hz over a 150 mm span, method and app list included.
- **Printed parts:** `[a]_tensioner_{left,right}` (printed in Ch 04's batch), `[a]_cable_cover`.
- **Hardware:** M3×8/×12/×30/×40 SHCS, M3 nut; Gates 2GT 6 mm belt (cut both to the same length by running one and matching).
- **Rev D+ deviations:** none.
- **Check:** both belts read within a few Hz of each other at 110 Hz after moving the gantry and returning.

**Ch 08 — Toolhead: Stealthburner, Clockwork 2, Nitehawk-SB V2** · Mode B · ~70 steps · 3.0–4.5 h
- **Sources:** [Stealthburner Assembly Manual](https://github.com/VoronDesign/Voron-Stealthburner/blob/main/Manual/Assembly_Manual_SB.pdf) (73 pp; Mode A embedding for the mechanical pages) + manual p.146–147; LDO notes **p.129–130, 146–147**; **[LDO Wiring Guide § Wiring the Toolhead PCB](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#wiring-the-toolhead-pcb)** (for the port assignments); **[Nitehawk-SB V2 doc](https://docs.ldomotors.com/en/Toolboard/nitehawk-sb-v2)** port/pin table and change list; [Nitehawk-SB-V2 repo images](https://github.com/MotorDynamicsLab/Nitehawk-SB-V2/tree/master/Images) (`nhsbv2_pcb_pinout.jpg`, `sbv2_fan_adapter_pcb_pinout.jpg`, `grounding_scheme.jpg`, `toolboard_ground_routing.jpg`).
- **Printed parts:** Stealthburner + Clockwork 2 sets; `cw2_captive_pcb_cover` (LDO chamber-thermistor variant); `usb_adapter_mount_partial_cover` (**V2**). LED diffuser and CW2 PCB spacer are supplied.
- **Hardware:** M3×8 SHCS ×2 (toolboard to CW2), M3×10 FHCS ×2 (fan adapter), M3×6 captive screw (cable door), M3×10 SHCS ×3 (USB adapter stack), E0508 ferrules if fitting a Rapido.
- **Rev D+ deviations — all five of §4.1 land in this chapter:** PH2.0 not XH2.5 on PROBE/TH0/Endstop; keyed reversed 2×10 header; no ADXL mount; V2 USB-adapter cover; grounding wire per the V2 images. Also: the endstop port is unused in a standard build; the probe port is 24 V only.
- **Checks:** thermistor reads room temperature before the toolhead goes on; the 2×10 headers seat with the SB front snapped on and no gap.

**Ch 09 — Electronics bay: DIN rails, wire ducts, board placement, endstops, Pi** · Mode B · ~30 steps · 2.5–4.0 h
- **Sources:** [LDO Wiring Guide](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d) §§ *Assembling the Nozzle Probe*, *Preparing the Inlet*, *Preparing the Power Supply Unit*, *Preparing the Mainboard*, *Installing the DIN Rails and Wire Ducts*, *General Placement*; [Leviathan V1.3 guide](https://ldomotion.com/guides/voron-leviathan-v1-3) § *Overview and Preparation* steps 1–4 (wiring diagram, pin assignment, **voltage-selection jumper removal**, Raspberry Pi mounting + HAT adapter); LDO notes **p.150, 152, 156, 158–163, 169–172**; manual p.148–173 for the DIN-rail *technique* pages only (DIN RAIL MOUNTS — HOW TO, HOOK FIXED SIDE, PRESS FIT).
- **Images to embed:** `Images/WiringGuide/RevD/S0_Din_Raill.jpg`, `S0General_Placement.jpg`, plus `Images/WiringGuide/z_stop_parts.jpg`, `z_stop_install_{1,2,3}.jpg`, `z_stop_final.jpg`.
- **Printed parts:** `Electronics_Bay/wago_221-415_mount_3by5`. (Leviathan brackets, DIN clips, NH adapter mount, bed WAGO mount all LDO-supplied.)
- **Hardware:** M2×10 self-tapping (DIN clips to brackets, nozzle probe), M3×8 SHCS (brackets to PCB), M3×25 SHCS ×2 (nozzle probe mount), M5×10 BHCS (bed WAGO mount), DIN end caps ×4, VHB tape.
- **Rev D+ deviations:** the USB adapter PCB now has a grounding point exposed by the new cover — mount and ground it here.
- **Hard rule to author:** remove **all** Leviathan voltage-selection jumpers before installing the board.

**Ch 10 — Wiring: above-deck, below-deck, mains, Checkpoint #1** · Mode B · ~75 steps · 5.0–7.0 h
- **Sources:** the whole [LDO Wiring Guide](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d) in its own order — *Insulating the Z Probe* → *Wiring the XY endstop* → *Routing the LED strips* → *Connecting Steppers* → *Connecting Inlet and WAGO* → *Connecting Wago and PSU* → **Checkpoint #1** → *Connecting 24V* → *Connecting Build Plate* → *Connecting the Gantry Cables* → *Connecting the Fans and the LED Strip* → *FFC/Ethernet/USB/Frame PE* → *Finish Line*; plus manual **p.194–195** (drag-chain slack) and the [LDO cable chain guide](https://docs.ldomotors.com/guides/cable_chain_guide); [XY endstop repin guide](https://docs.ldomotors.com/en/guides/XY_Endstop_Cable_Reconnecting_Guide) if labels read "X Stop/Y Stop".
- **Images to embed (raw GitHub, GPL-3.0):** `RevD/S1_mapping.jpg`, `S1_steppers.jpg`, `S2_inlet.jpg`, `S2_mapping.jpg`, `S3_mapping.jpg`, `S3_wago_PSU.jpg`, `S4_MB_PSU.jpg`, `S4_mapping.jpg`, `S5_bed.jpg`, `S5_mapping.jpg`, `S6_Endstop.jpg`, `S6_mapping.jpg`, `S7_fan.jpg`, `S7_mapping.jpg`, `VS8_Misc.jpg`, `VS8_mapping.jpg`, `VS9_Final.jpg`; plus `WiringGuide/led_route.svg`, `led_splitter_placement.jpg`, `led_extrusion_cover.jpg`, `psu_switch.jpg`, `z_motor_orientation{,2}.jpg`.
- **Printed parts:** `Skirts/power_inlet_IECGS_1mm`, COB light-strip mounts.
- **Hardware:** M3×8 SHCS + M3 hammerhead T-nuts (LED bars, splitter spacers), M5×10 BHCS, VE0508 ferrules, 100 zip ties, cable tags.
- **Stepper map to transcribe verbatim:** A = rear **right** → `HV-STEPPER-1`; B = rear **left** → `HV-STEPPER-0`; Z0 front-left → `STEPPER-0`; Z1 rear-left → `STEPPER-1`; Z2 rear-right → `STEPPER-2`; Z3 front-right → `STEPPER-3`; `STEPPER-4` unused. Fans: PCB fan → `FAN2/PF7`, LED strip → `LED-Strip/PE6`, filter fan → `FAN3/PF9`.
- **Rev D+ deviations:** the toolhead-side connector types (§4.1 ③); the umbilical must leave the secondary USB port accessible.
- **Hard gate:** Checkpoint #1 (multimeter, unplugged) before any power-on, and before Ch 11 starts.

**Ch 11 — Skirts, panels, Clicky-Clack door, Nevermore, spool holder** · Mode A + two Mode B inserts · ~70 steps · 4.0–6.0 h
- **Sources:** manual **p.212–239** (Skirts: APPLY FOAM TAPE, APPLY VHB TAPE, Z BELT COVERS, ELECTRONICS COOLING FAN, LCD HOOKUP, BOTTOM PANEL, BACK PANEL) and **p.240–259** (Panels: SIDE PANELS, TOP PANEL, MIND THE MAGNET POLARITY, APPLY 3MM FOAM TAPE, SPOOL HOLDER, EXHAUST); LDO notes **p.214–216 & 220–221** (BTT 4.3" screen; mount STL in [`LDOVoronTrident/STLs/BTT Pi TFT4.3 Mount`](https://github.com/MotorDynamicsLab/LDOVoronTrident/tree/master/STLs/BTT%20Pi%20TFT4.3%20Mount)), **p.234** (alt Z-belt cover), **p.250–253 & 256 SKIP**; **Mode B insert 1:** [KB3D Clicky-Clacky Door guide](https://wiki.kb-3d.com/en/home/LDO/LDO_Clicky_Clacky_Door_Mod) (34 images) with the plain acrylic panel instead of NanoNest; **Mode B insert 2:** [LDO Nevermore V5 Duo — V2.4](https://ldomotion.com/guides/nevermore-v5-duo---v24) (37 step images).
- **Printed parts:** `Skirts/350/*` ×5, `Skirts/[a]_{belt_guard,fan_grill,fan_grill_retainer,keystone_blank}_*`, `keystone_panel`, `side_fan_support_x2`, `Panel_Mounting/{corner,midspan}_panel_clip_*`, `bottom_panel_{clip,hinge}`, `z_belt_cover_{a,b}` (or the LED-routing variant), Clicky-Clack set (`Handle`, `Handle-Hinge_{Top,Bottom}`, `Hinge-L-{Sleeve,Solid}` ×2 each, `Latch`, `Panel_Clip`), Nevermore Micro V5 Duo (3×6-magnet variant) + exhaust cover + stock exhaust grill, `Spool_Management/*`, optional `LDO Insert`, handlebar spacers, Z stoppers.
- **Hardware:** M3×8/×12/×30/×40 SHCS, M3×6 BHCS, M3 T-nut, M5×10/×16 BHCS, M5 T-nut, M5×14 + M5 hammerhead (handlebars), 6×3 magnets ×16, 1 mm and 3 mm foam tape, VHB, super glue (door magnets), 5 mm dowels + split bushings (door hinges), heat-set insert (door latch).
- **Rev D+ deviations:** none.
- **Colour note:** the Clicky-Clack "Blue" option selects the **door's aluminium extrusion frame** colour (per the vendor page and a customer review) — i.e. it is visible trim, and blue matches the printer's blue frame rather than the orange/black printed-part accent. That resolves the open question in `CLAUDE.md`; no change needed unless he wants the door frame to read as accent rather than frame.

**Ch 12 — Software: Pi, Klipper, firmware, printer.cfg** · Mode B · ~30 steps · 2.0–3.0 h
- **Sources:** [LDO Wiring Guide § Software Setup](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#software-setup) (Pi OS imaging, SSH, KIAUH order: Klipper → Moonraker → Fluidd/Mainsail → KlipperScreen, touchscreen rotation via [`btt_43_rotate_guide`](https://docs.ldomotors.com/en/guides/btt_43_rotate_guide), firmware, USB IDs via [`klipper_id`](https://docs.ldomotors.com/guides/klipper_id)); [Leviathan V1.3 guide](https://ldomotion.com/guides/voron-leviathan-v1-3) §§ Katapult Bootloader, Klipper Firmware Installation, Firmware Testing; [docs.vorondesign.com/build/software](https://docs.vorondesign.com/build/software/).
- **Config file:** **[`leviathan-printer-rev-d-sbv2.cfg`](https://github.com/MotorDynamicsLab/LDOVoron2/blob/main/Firmware/leviathan-printer-rev-d-sbv2.cfg)**.
- **Printed parts / hardware:** none.
- **Rev D+ deviations — this chapter is where they concentrate:** ① the config file; ② `stm32g0b1xx` not `rp2040` in the toolboard ID. Plus the 350 mm uncommenting checklist (§4.4 #15) and adding a `[bed_mesh]` section.
- **Checks:** `ls /dev/serial/by-id/*` shows exactly two Klipper devices, one `stmf446xx` (Leviathan) and one `stm32g0b1xx` (Nitehawk V2); `STATUS` clean after `RESTART`.

**Ch 13 — First power-up and initial startup** · Mode B, transcribed from the wizard · ~35 steps · 2.5–4.0 h
- **Source:** [docs.vorondesign.com/build/startup](https://docs.vorondesign.com/build/startup/), **V2 path, probe = "Stock Inductive probe"**, in the wizard's own page order: Verify Temperatures → Verify Heaters → Verify Fans → Motor Checks (`STEPPER_BUZZ` per motor) → XY Endstop Check → Homing Check → Bed Locating → 0,0 Point → Z Endstop → Probe Check (`PROBE_ACCURACY`) → PID Tuning → Quad Gantry Level → Z-offset → Finish. Each wizard page already carries a `<details>` troubleshooting block — transcribe those as the "if this happens" boxes.
- **Numbers to transcribe verbatim:** `PID_CALIBRATE HEATER=heater_bed TARGET=100` (~10 min); `M106 S64` then `PID_CALIBRATE HEATER=extruder TARGET=245` (~5 min); QGL hot at bed 100 °C / hotend 150 °C, `PROBE_ACCURACY` σ < 0.003 mm with no trend, 10–20 min to stabilise from cold; QGL `retry_tolerance: 0.0075`, `retries: 5`.
- **Rev D+ deviations:** none beyond Ch 12's config.
- **Then:** Ch 06b (gantry squaring) runs here, followed by a QGL re-run.

**Ch 14 — Calibration and first prints** · Mode B · ~25 steps · 2.5–4.0 h
- **Sources:** startup guide "Finish Line" (e-steps: mark 120–150 mm, extrude 2×50 mm, `rotation_distance = old × actual/target`, target within 0.5%; CW2 = `gear_ratio 50:10`, `rotation_distance 22.6789511`); [docs.vorondesign.com/build/slicer/first_print.html](https://docs.vorondesign.com/build/slicer/first_print.html); [Ellis' Print Tuning Guide](https://ellis3dp.com/Print-Tuning-Guide/) — First Layer Squish → Pressure Advance (Pattern Method) → Extrusion Multiplier → Cooling/Layer Times → Retraction; Klipper input shaper (ADXL is on the toolboard, `[resonance_tester]` already configured, `accel_per_hz: 100`).
- **Order to enforce:** e-steps → first print (Voron cube) → input shaper → pressure advance → extrusion multiplier → first-layer squish refinement.
- **Rev D+ deviations:** none.

---

### 7.3 Tools and consumables checklist, per chapter

| Chapter | Tools | Consumables |
|---|---|---|
| 00 | Digital caliper 150 mm; machinist square 150 mm DIN 875/2; flat reference (the stone counter, verified); temperature-controlled soldering iron + LDO brass M3 tip; flush cutters; 2 mm drill bit (supplied) | IPA ≥90%; Super Lube 21030 (NLGI 0/1); nitrile gloves; lint-free cloth; masking tape + marker for labelling |
| 01 | Ball-end hex 4 mm; machinist square; steel rule; flat reference; torque driver 0.5–3 N·m (optional) | — |
| 02 | Hex 1.5/2/2.5/3/4 mm; soldering iron + insert tip; caliper (deck thickness gate); printed `MGN9_rail_guide`, `pulley_jig` | Loctite 243 (blue) for non-pre-applied set screws; grease |
| 03 | Hex 2.5/3 mm; PH2 screwdriver; plastic scraper or card (magnet application); sharp knife (trim magnet holes) | IPA; the bed's protective film goes in the bin |
| 04 | Hex 2/2.5/3/4 mm; printed assembly aid (from the manual); pulley jig | Loctite 243 |
| 05 | Hex 2/2.5/3/4 mm; **T10 Torx** driver for backer FHCS (strongly preferred); rail guides; soldering iron (inserts) | Loctite 243 |
| 06 | Hex 2.5/3/4 mm; two people for gantry install; rubber rail stoppers (LDO trick); long zip ties as backup | — |
| 07 | Hex 2/2.5 mm; flush cutters; phone with Spectroid (Android) / Sound Spectrum Analysis (iOS) / Gates Carbon Drive; 150 mm rule to set the span | — |
| 08 | Hex 1.5/2/2.5 mm; JST-PH crimp tool **only if** modifying pigtails; multimeter; soldering iron (fan voltage trace cut/bridge, if ever needed) | Fibreglass tape (supplied, for the probe); E0508 ferrules if fitting a Rapido |
| 09 | 2.5 mm flat screwdriver (supplied); PH2; hex 2/2.5/3 mm; multimeter | VHB tape (supplied); DIN end caps |
| 10 | Multimeter (**mandatory**); 2.5 mm flat screwdriver; PH2 (PSU + SSR); flush cutters; small pliers; label maker or the supplied cable tags | Zip ties ×100; VE0508 ferrules; wire duct offcuts |
| 11 | Hex 2/2.5/3/4 mm; small hammer (door hinge dowels + bushings); side cutters; soldering iron (door latch insert); scissors for foam tape | 1 mm and 3 mm foam tape; VHB; super glue (door magnets); 6×3 magnets ×16 |
| 12 | Laptop; SD card reader; USB-A→USB-C/micro cable for board flashing; network cable | 32 GB SD (supplied) |
| 13 | — | A spool of ASA in the dryer, warmed up |
| 14 | Caliper; ruler; marker (e-steps) | Test filament; Voron cube; Ellis' PA pattern |

### 7.4 Image and asset sourcing, with licensing

| Asset | Location | How to get one image per step | Licence |
|---|---|---|---|
| Official manual page renders | `github.com/VoronDesign/Voron-2` branch `Voron2.4`, path `Manual/Assembly_Manual_2.4r2.pdf` (74,568,690 bytes, 263 pp, A4 landscape 841.89×595.276 pt, PDF 1.6, `ModDate` 2023-07-18). **Pin to commit `de7e89de1908e525d6d10eda453298bd9cc83d3b`** — the same commit LDO's build notes reference | `pdftoppm -r 200 -png -f N -l N Assembly_Manual_2.4r2.pdf out/page` (verified working; ~240 KB/page at 150 dpi). For vector: `pdftocairo -svg -f N -l N` | **GPL-3.0** (`VoronDesign/Voron-2/LICENSE`) — derivative docs must also be GPL-3.0 |
| Stealthburner manual renders | `VoronDesign/Voron-Stealthburner/Manual/Assembly_Manual_SB.pdf` (7,245,278 bytes, 73 pp, `ModDate` 2023-07-07). A high-contrast variant `Assembly_Manual_SB_High_Contrast_7-7-23.pdf` also exists | same | **GPL-3.0** |
| LDO Rev D wiring photos (hi-res) | `raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/main/Images/WiringGuide/RevD/<name>.jpg` — verified HTTP 200. 19 build images (`S0…VS9`) at ~600–880 KB each + 6 UI screenshots | Direct download; the wiring guide itself points here for hi-res | **GPL-3.0** (`MotorDynamicsLab/LDOVoron2/LICENSE`) |
| LDO wiring/printed-parts wiki images (lower-res) | `https://docs.ldomotors.com/<path>` (e.g. `/vs1_steppers.jpg`, `/v2_wire_guide/bed_wago_mount.jpg`) | Only for images with no GitHub original | Wiki content licence "alr" (all rights reserved) per `siteConfig` — **link, do not copy** |
| Nitehawk-SB V2 pinouts + grounding | `github.com/MotorDynamicsLab/Nitehawk-SB-V2/Images/` (`nhsbv2_pcb_pinout.jpg`, `sbv2_fan_adapter_pcb_pinout.jpg`, `grounding_scheme.jpg`, `toolboard_ground_routing.jpg`, `usb_adapter_gnd.jpg`, `reset_boot_buttons.jpg`) + `Hardware/Nitehawk-SB_V2.0.0/` schematic PDF and interactive `ibom.html` | Direct download | **No LICENSE file in the repo** — link, do not redistribute; ask LDO in `#ldo_motors` if embedding matters |
| Voron gantry-squaring images | `VoronDesign/Voron-Documentation/build/mechanical/images/v2_gantry_squaring/*.png` (10 images) | Direct | **GPL-3.0** |
| Voron startup wizard images/GIFs | `VoronDesign/Voron-Documentation/build/startup/images/*` | Direct | **GPL-3.0** |
| KB3D Clicky-Clack images (34) | `wiki.kb-3d.com` | **Link only** | Reseller wiki, no stated licence |
| ldomotion.com step images | `ldomotion.com/guides/{voron-leviathan-v1-3, nevermore-v5-duo---v24}` | **Link only** | No stated licence |
| His own build photos | — | Shoot per §7.5 | His |

**Licensing conclusion:** because the manual, the Stealthburner manual, the Voron docs and the LDO kit repo are **all GPL-3.0**, a consolidated manual that embeds their images is a derivative work and must itself be GPL-3.0 with attribution — which is fine, and means it can be published back to the community. Assets from the LDO wiki, KB3D and ldomotion.com must be **linked, not embedded**.

### 7.5 What to photograph during his own build

Shoot these because no source has them for Rev D+ or for his exact configuration. One tripod position per phase, phone on a timer, 4:3, good side light.

1. **Every LDO deviation.** The precision spacer next to a shim; the second-hole rail mounting; the M3×20 bed screw; the deck-support thickness he actually used, next to the caliper reading.
2. **The Nitehawk-SB V2 board, both faces**, with the PH2.0 connectors seated — this literally does not exist in any guide.
3. **The V2 fan-adapter header mating** in the correct (keyed) orientation.
4. **The USB-adapter grounding wire** as installed, matching the V2 repo's `usb_adapter_gnd.jpg`.
5. **The Ti backers on both axes** before the XY joints are torqued, showing the face they are on relative to the rail.
6. **The electronics bay at each Checkpoint** — LDO's `mapping` images are diagrams; a real photo of *his* bay at each stage is worth more.
7. **The gantry-squaring setup**: dropped Z joints, released tensioners, the flush/hole checks from the Voron procedure.
8. **Belt tension measurement**: the 150 mm span marked, and the phone showing the peak at 110 Hz.
9. **Heat-set insert results**, good and bad, on the practice part — the best possible teaching image for a 13-year-old.
10. **The finished cable runs** before the ducts are covered (LDO's `VS9_Final.jpg` equivalent, but his).

### 7.6 Effort estimate for producing the manual

| Work | Hours | Notes |
|---|---|---|
| Tooling: page-render script, image fetch/cache, chapter scaffold, static-site + PDF build | 4–6 | One-off; scripted |
| Ch 01–07 in Mode A (~275 steps over 156 manual pages) | 14–18 | ~18 steps/h: write the step text + fastener row + check around an existing render |
| Ch 08–11 in Mode B (~245 steps) | 16–22 | Slower — reconciling three sources per step, and Ch 08/10 carry all the Rev D+ patching |
| Ch 00, 12, 13, 14 (~115 steps) | 8–11 | Ch 13 is mostly faithful transcription of the wizard |
| Rev D+ deviation audit + cross-check pass (verify each patch against the board doc, the `-sbv2` config and the V2 repo) | 4–6 | Do this **once at the end**, as a single pass, against the config diff table in §4.1 |
| Photo capture during the build (his time) | 6–9 | ≈ +12–15% on build hours |
| Photo selection, crop, caption, placement | 4–6 | |
| **Total** | **56–78 h** | ≈ 640 steps |

That is more than the build itself, which is the honest headline. Three ways to make it tractable, in order of recommendation:

1. **Write one chapter ahead of the bench.** Ch 00–02 before the kit lands (they need nothing but the PDF and the wiki), then stay one phase ahead. Spreads the load and means the manual is written by someone who has just done the previous step.
2. **Cut Mode A to a thin overlay for Ch 01, 03, 04.** These three are the least error-prone chapters and the manual renders are unambiguous. A "page N + fastener row + check" line per page instead of full step prose drops ~8 h.
3. **Do not write Ch 14.** Ellis' guide is better than anything we would produce and is already the community standard; link it with an ordering wrapper. Saves ~3 h.

Trimmed scope: **~42–55 h**, still producing a genuinely single-track, Prusa-shaped manual for the ~70% of the build where the existing sources actively fight each other.

---

## 8. Machine-readable phase summary

```csv
phase_id,name,hours_handson_low,hours_handson_high,needs_part_groups,prereq_phases,no_parts_ok
P00,Prep inventory rail-prep jigs,2.5,4.0,"Tools/MGN9_rail_guide;Tools/MGN12_rail_guide;Tools/pulley_jig;Tools/bed_hole_marking_template;Tools/bottom_panel_template;Test_Prints/Heatset_Practice;Test_Prints/Voron_Design_Cube_v7",,yes
P01,Frame assembly and squaring,2.5,4.0,,P00,yes
P02,Z drives Z idlers Z rails deck,5.0,7.0,"Z_Drive;Z_Idlers;Panel_Mounting/deck_support",P01,no
P03,Build plate and bed,1.5,2.5,,P01,yes
P04,A/B drives and idlers,3.5,5.0,"Gantry/AB_Drive_Units;Gantry/Front_Idlers",P01,no
P05,Gantry X/Y XY-joints X-carriage Ti-backers,5.0,7.0,"Gantry/X_Axis/XY_Joints;Gantry/X_Axis/X_Carriage",P04,no
P06,Z axis gantry-install Z-belts gantry-squaring,3.5,5.0,"Gantry/Z_Joints;Gantry/z_belt_clips;Gantry/z_chain",P02;P05,no
P07,A/B belts and tensioning,2.5,4.0,"Gantry/Front_Idlers/tensioners;Gantry/AB_Drive_Units/cable_cover",P06,no
P08,Toolhead Stealthburner CW2 Nitehawk-SB-V2,3.0,4.5,"Voron-Stealthburner/StealthBurner;Voron-Stealthburner/Clockwork2;Nitehawk-SB/cw2_captive_pcb_cover;Nitehawk-SB-V2/usb_adapter_mount_partial_cover",P05,no
P09,Electronics bay DIN ducts boards endstops Pi,2.5,4.0,"Electronics_Bay/wago_221-415_mount_3by5",P02,partial
P10,Wiring above-deck below-deck mains Checkpoint-1,5.0,7.0,"Skirts/power_inlet_IECGS_1mm;LDOVoron2/COB_light_strip_mount",P06;P08;P09,partial
P11,Skirts panels ClickyClack-door Nevermore spool,4.0,6.0,"Skirts/350;Skirts/accents;Panel_Mounting;ClickyClack;Nevermore_V5_Duo;Spool_Management",P10,no
P12,Software Pi Klipper firmware printer.cfg,2.0,3.0,,,yes
P13,Initial startup checks PID QGL Z-offset,2.5,4.0,,P10;P12,no
P14,Calibration e-steps input-shaper PA first-print,2.5,4.0,,P13,no
```

Totals: **47.5–71.0 h** hands-on, midpoint ≈ 59 h. Zero-printed-part work (`no_parts_ok = yes`): P00 + P01 + P03 + P12 = **8.5–13.5 h ≈ 18–19%** of the build. (Verified: the CSV sums match the §5.1 table.)

---

## 9. Sources

**Official Voron**
- [github.com/VoronDesign/Voron-2 — `Manual/Assembly_Manual_2.4r2.pdf`](https://github.com/VoronDesign/Voron-2/blob/Voron2.4/Manual/Assembly_Manual_2.4r2.pdf) · 263 pp, `ModDate` 2023-07-18, GPL-3.0 · pinned commit [`de7e89d`](https://github.com/VoronDesign/Voron-2/blob/de7e89de1908e525d6d10eda453298bd9cc83d3b/Manual/Assembly_Manual_2.4r2.pdf)
- [github.com/VoronDesign/Voron-2 — `STLs/`](https://github.com/VoronDesign/Voron-2/tree/Voron2.4/STLs) · 155 STLs, phase-organised
- [github.com/VoronDesign/Voron-Stealthburner — `Manual/Assembly_Manual_SB.pdf`](https://github.com/VoronDesign/Voron-Stealthburner/blob/main/Manual/Assembly_Manual_SB.pdf) · 73 pp, `ModDate` 2023-07-07
- [docs.vorondesign.com](https://docs.vorondesign.com) · [V2 Gantry Squaring](https://docs.vorondesign.com/build/mechanical/v2_gantry_squaring.html) · [Initial Startup](https://docs.vorondesign.com/build/startup/) · [Secondary Printer Tuning (belt tension, bed mesh)](https://docs.vorondesign.com/tuning/secondary_printer_tuning.html) · [Software](https://docs.vorondesign.com/build/software/) · [First Print](https://docs.vorondesign.com/build/slicer/first_print.html) · repo [VoronDesign/Voron-Documentation](https://github.com/VoronDesign/Voron-Documentation) pushed 2026-08-29
- [community/howto/simonthecat/I_wish_I_had_known.md](https://github.com/VoronDesign/Voron-Documentation/blob/main/community/howto/simonthecat/I_wish_I_had_known.md)
- [Voron Discord](https://discord.gg/voron) · [`#ldo_motors` channel](https://discord.com/channels/460117602945990666/710952853514223617) · [forum.vorondesign.com](https://forum.vorondesign.com) · [Rev D launch thread, 2024-06-12](https://forum.vorondesign.com/threads/ldo-voron-rev-d-kits-are-now-live-at-fabreeko.1802/)

**LDO**
- [Kit index](https://docs.ldomotors.com/en/voron/voron2) · [Build Notes/FAQ (upd. 2026-02-10)](https://docs.ldomotors.com/voron/voron2/build-faq) · [Wiring Guide Rev D (upd. 2026-07-14)](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d) · [Printed Parts Guide Rev D (upd. 2025-07-14)](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d) · [Printed Parts Rev C](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_c) · [Wiring Rev C](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_c)
- [350 BOM index (upd. 2026-06-26)](https://docs.ldomotors.com/en/voron/voron2/350_BOM/HOME) · [350 Rev D BOM (upd. 2026-02-05)](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D) · [300 BOM](https://docs.ldomotors.com/en/voron/voron2/300_BOM/HOME)
- [Nitehawk-SB V2 board doc (upd. 2026-07-10)](https://docs.ldomotors.com/en/Toolboard/nitehawk-sb-v2) · [Nitehawk-SB V1 board doc](https://docs.ldomotors.com/en/Toolboard/nitehawk-sb)
- [Rail grease guide](https://docs.ldomotors.com/guides/rail_grease_guide) · [Heat-set insert tool guide](https://docs.ldomotors.com/guides/heatset_insert_tool_guide) · [Cable chain guide](https://docs.ldomotors.com/guides/cable_chain_guide) · [Klipper USB ID guide](https://docs.ldomotors.com/guides/klipper_id) · [BTT 4.3 rotate guide](https://docs.ldomotors.com/en/guides/btt_43_rotate_guide) · [XY endstop cable repin guide](https://docs.ldomotors.com/en/guides/XY_Endstop_Cable_Reconnecting_Guide)
- [ldomotion.com — VORON Leviathan V1.3 guide](https://ldomotion.com/guides/voron-leviathan-v1-3) · [Nevermore V5 Duo — V2.4](https://ldomotion.com/guides/nevermore-v5-duo---v24) · [guides index](https://ldomotion.com/guides)
- [github.com/MotorDynamicsLab/LDOVoron2](https://github.com/MotorDynamicsLab/LDOVoron2) (GPL-3.0) — [`leviathan-printer-rev-d.cfg`](https://github.com/MotorDynamicsLab/LDOVoron2/blob/main/Firmware/leviathan-printer-rev-d.cfg) · [**`leviathan-printer-rev-d-sbv2.cfg`**](https://github.com/MotorDynamicsLab/LDOVoron2/blob/main/Firmware/leviathan-printer-rev-d-sbv2.cfg) · [`Images/WiringGuide/RevD/`](https://github.com/MotorDynamicsLab/LDOVoron2/tree/main/Images/WiringGuide/RevD)
- [github.com/MotorDynamicsLab/Nitehawk-SB-V2](https://github.com/MotorDynamicsLab/Nitehawk-SB-V2) (no LICENSE) · [github.com/MotorDynamicsLab/Nitehawk-SB](https://github.com/MotorDynamicsLab/Nitehawk-SB) · [github.com/MotorDynamicsLab/Leviathan](https://github.com/MotorDynamicsLab/Leviathan) (GPL-3.0) · [github.com/MotorDynamicsLab/LDOVoronTrident — BTT TFT4.3 mount](https://github.com/MotorDynamicsLab/LDOVoronTrident/tree/master/STLs/BTT%20Pi%20TFT4.3%20Mount)

**Vendor**
- [Fabreeko — Voron 2.4 R2 (Rev D+) Kit by LDO](https://www.fabreeko.com/products/ldo-voron-v2-4-kit) · [Fabreeko blog — Exciting Changes in the New LDO Voron Kits Rev D](https://www.fabreeko.com/blogs/news/exciting-changes-in-the-new-ldo-voron-kits-rev-d) · [Clicky-Clack Door Kit by LDO](https://www.fabreeko.com/products/clickyclackydoor-kit-by-ldo) · [Acrylic panel for Clicky-Clack](https://www.fabreeko.com/products/acrylic-pannel-for-clicky-clacky-door) · [Ti extrusion backers](https://www.fabreeko.com/products/v2-4-trident-titanium-extrusion-backers) · [Fabreeko Discord](https://discord.gg/NV8Y6bcerP)

**Community guides and mods**
- [Ellis' Print Tuning Guide](https://ellis3dp.com/Print-Tuning-Guide/) · [repo](https://github.com/AndrewEllis93/Print-Tuning-Guide) (last push 2025-03-14)
- [github.com/tanaes/whopping_Voron_mods — extrusion_backers](https://github.com/tanaes/whopping_Voron_mods/tree/main/extrusion_backers) · [clickyclacky_door](https://github.com/tanaes/whopping_Voron_mods/tree/main/clickyclacky_door)
- [KB3D wiki — LDO Clicky-Clacky Door Mod (upd. 2025-09-15)](https://wiki.kb-3d.com/en/home/LDO/LDO_Clicky_Clacky_Door_Mod)
- [github.com/nevermore3d/Nevermore_Micro](https://github.com/nevermore3d/Nevermore_Micro) · [github.com/jlas1/Klicky-Probe](https://github.com/jlas1/Klicky-Probe)
- [github.com/th33xitus/kiauh](https://github.com/th33xitus/kiauh) · [Mainsail docs](https://docs-os.mainsail.xyz/) · [Fluidd docs](https://docs.fluidd.xyz/)
- [mods.vorondesign.com — Extrusion Backers](https://mods.vorondesign.com/details/ewDI1Cntz7urtuq3Cm9wGQ)

**Video (with the revision each one actually built)**
- Steve Builds — [LDO Voron 2.4 Kit Build](https://www.youtube.com/playlist?list=PL0fUJbigELQPqpeGOgHYisG4KaSXVtnNY), 11 parts, **Dec 2021–Jan 2022, Rev A/B**
- Nero3D / Canuck Creator — [Voron V2.4r2 LDOmotors kit Livestream build Part 1](https://www.youtube.com/watch?v=ZHO-kFlY91c), 3 h 49 m, **2022-02-15, Rev A/B**; also [Voron V2.4 Build Livestream playlist](https://www.youtube.com/playlist?list=PL7zrGeKp_8CRMm8sMrxQ02QfZYhP7f0cQ), **2020, pre-r2**
- Minimal 3DP — [Voron 2.4 R2 Build Guide](https://www.youtube.com/playlist?list=PLXcVv43EZh9DzcPPF0IUVnpVdxQTQX8nE), 15 parts, **Apr–Oct 2024, FormBot kit**
- Build It Basement — [ULTIMATE Voron 2.4R2 Build](https://www.youtube.com/playlist?list=PLjlotZjUVD32oT7YpPE89dqFwjCkVNKQ9), **Dec 2022–Feb 2023**, incl. [Part 7.5 Titanium Backers](https://youtu.be/BHUxiEEnyGg) and [Part 8.5 Gantry Check and Square](https://youtu.be/eaWr10UDIC0)
- 123-3D — [Rev D Part 1](https://www.youtube.com/watch?v=IushU1_ikKw) (2024-10-04) · [Part 2](https://www.youtube.com/watch?v=vpIDagUumgI) · [Part 3](https://www.youtube.com/watch?v=0cuV6iROV1k) · [Part 4](https://www.youtube.com/watch?v=QA0eMNXqI-E) (2024-11-08) · [Rev D kit review](https://www.youtube.com/watch?v=sNCyXx_2Um0) (2025-02-21) — **the only Rev D series**
- Nathan Builds Robots — [Help me build this printer! LDO Voron 2.4 Rev D Kit](https://www.youtube.com/watch?v=hJPDsoD43dA), **10 h 13 m, 2025-02-15, Rev D**
- Greg's Maker Corner — [Voron 2.4 Build Series](https://www.youtube.com/playlist?list=PLpQnpsv1trbQxzX1zIVISOJtE6Pnb-si6), **2022, incl. titanium backers episode**
- Kapman's Basement Workshop — [Voron 2.4 Build](https://www.youtube.com/playlist?list=PL16WZCqkIMPh415mwyKJNhOl5i7Qo8pip), 15 parts, **2021, Blurolls kit**
- Maple Leaf Makers — [Voron LDO 2.4r2 Complete Build Guide Part 2](https://www.youtube.com/watch?v=4DbeedEe8nM), **2022, LDO Rev A/B**
- ModBotArmy — [LDO Voron 2.4 Rev C Build Part 1: Frame](https://www.youtube.com/watch?v=-mHLoGsHp1E), **2023, Rev C**
- CNC Kitchen — [Should you build a VORON 2.4 in 2023? (LDO Kit Review)](https://youtu.be/nik-HCeOSB8), **2022-09-24**

**Rejected sources (documented so they are not re-evaluated)**
- [voronldo.com belt tension guide](https://voronldo.com/guides/voron-belt-tension/) — unaffiliated, uncited, internally inconsistent, contradicts official numbers, domain-for-sale notice. **Do not use.**
- [voron.dozuki.com](https://voron.dozuki.com/) — last revision 2019-12-09, covers Voron 1.6/2.2/Afterburner. Obsolete.
- [canbus.esoterical.online](https://canbus.esoterical.online) / [Esoterical/voron_canbus](https://github.com/Esoterical/voron_canbus) — excellent, but CAN-only; this kit is USB end-to-end. Not applicable.

---

## 10. Corrections to `CLAUDE.md` surfaced by this survey

Listed, not applied — `CLAUDE.md` is outside this task's scope.

1. *"Stock kit ships Klicky + Nevermore Micro V5 Duo parts instead"* — the kit ships an **Omron inductive probe** as the default (QGL only) plus an **LDO nozzle-probe PCB** for Z=0; Klicky parts are the *optional alternative*. The stock LDO config assumes the inductive probe.
2. *"LDO docs currently only cover Rev D, not D+ (electrical-only diff)"* — correct that no doc is labelled D+, but the diff is **not** purely electrical: it changes a printed part (`usb_adapter_mount_partial_cover`), the connector types on three toolhead ports, the fan-adapter header orientation, and the Klipper config file.
3. *"only ~15% of the build (by time) is possible before any printed parts exist"* — measured at **18–19%** (P00, P01, P03, P12).
4. Print batch 2, *"feet + bed mounts — gates bed install"* — there are **no printed feet and no printed bed mounts** in the 2.4r2 STL set; feet are supplied rubber. The Build Plate phase needs zero printed parts and can run right after the frame.
5. *"Assembly docs … LDO supplements at docs.ldomotors.com … Klipper config"* — the config to use is `leviathan-printer-rev-d-**sbv2**.cfg`, which the LDO wiring guide does **not** link.
6. Open item *"Clicky-Clack accent color — unresolved whether 'Blue' governs visible trim"* — **it does**: the colour option selects the door's aluminium extrusion frame, which is visible and matches the printer's blue frame.
7. Open item *"5mm hex driver for M5 frame bolts"* — the frame fasteners are M5×16 / M5×10 **BHCS**, which take a **3 mm** hex; the largest fastener in the build is M5×40 SHCS at **4 mm**. The manual's own tools page (p.9) recommends only ball-end **2.0 / 2.5 / 3.0 mm** and notes 2.5 mm gets the most use; the kit supplies 1.5/2/2.5/3/4 mm. **A 5 mm driver is not needed anywhere in this build.** Spend the money on a good ball-end 2.5 mm instead. Verify against the actual kit on arrival.
