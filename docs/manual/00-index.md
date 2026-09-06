# Voron 2.4 350 — build manual

This is the single track for building an **LDO Voron 2.4 R2 Rev D+, 350 mm, blue** (Fabreeko F6424626) — the official Voron and Stealthburner manuals, the LDO Rev D guides and the Rev D+ corrections consolidated into one Prusa-style set of numbered steps.

Every printed part is made here, on a **Prusa Core One+** (Gen 2 belts), in Prusament ASA Galaxy Black with a Prusa Orange accent: 27 plates, 157.1 h, 1813 g black + 279 g orange — see [Plate plans](../print/plate-plans.md) for every diagram at a glance.

Start at [**Ch 00 — Before you start**](00-before-you-start.md) if the kit has landed, and at [**print/00-slicer-setup.md**](print/00-slicer-setup.md) if it has not — **six of the eleven print batches (B00, B02, B07, B08, B09, B10 — 98.6 h of the 157.1) run before the Voron arrives**; the five with bearing seats and shaft bores (B01, B03–B06 — 58.5 h) wait for Gate B on kit day.

Keep two pages open at the bench: [**Tonight**](00-tonight.md), a fresh 30/60/90-minute session planner built from every chapter's `Time:` and `Pause:` lines and every plate's print time, for deciding what fits in the time you have — including "start plate X, then …" when the printer is free; and the print pages — [checklists](../print/checklists.md) and [bin labels with QR codes](../print/bin-labels.md) — for the garage bench where a tablet doesn't survive.

---

## The timeline

![Build timeline — print batches against assembly chapters](assets/diagrams/11-build-timeline.svg)

Rows are in execution order. Do a row only when its **needs** are satisfied; do the *While it prints* work in the same sitting so the Core One+ is never idle and no chapter waits on a part.

Markers: **KIT** = needs the Voron kit to have arrived · **2P** = two people · **2P lift** = the gantry lift, genuinely two people. Batches are B00–B10; plates are `B00-P1` too (two-digit batch, plate number unpadded).

**Kit not here yet:** rows 1–8 are the pre-kit run — B00 → B02 → B07 → (Gen 2 upgrade) → B08 → B09 → B10, 98.6 h ≈ 10 printer-days ≈ 1.5–2 weeks at two plate swaps a day, with Ch 00a and Ch 00's own pre-kit steps (00.23–00.32: the manual's front matter, the measurement log, the Discord questions — marked `(pre-kit)` so [Tonight](00-tonight.md) offers them) as the bench work. Rows 9 onward start the day the kit lands: **Gate B** first (Step B00.7, 15 min), then B01 and B03–B06 (58.5 h) print under Ch 00–05.

- **1 · Print** — [B00 — Calibration & jigs](print/B00-calibration-and-jigs.md) · 4.0 h print · needs: the Core One+ running, Gen 2 upgrade done (baseline)
    - *While it prints:* Dry a spool, read [00-slicer-setup](print/00-slicer-setup.md), decide the sheet and glue
    - *Gate:* **Gate A** (Step B00.5, cube only): X/Y ±0.15 mm, Z ±0.10 mm, first-layer-vs-mid delta ≤ 0.15 mm, corner snap. Gate B (625-2RS bore, MGN12 rail, real inserts) waits for the kit
    - *Sessions:* 1 plate start
- **2 · Print** — [B02 — Accent parts, the orange day](print/B02-accent-parts-orange.md) · 21.9 h print · needs: Gate A
    - *While it prints:* [Ch 00a](00a-mains-safety.md) (row 3); read Ch 01–02
    - *Gate:* SB main body supports out clean, LED pockets crisp; `Handle` set aside for B10; orange spool re-sealed
    - *Sessions:* 3 plate starts
- **3 · Build** — [Ch 00a — Mains safety](00a-mains-safety.md) · 0.75–1.0 · needs: Ch 00 Steps 00.8 and 00.30 as reading (the tool table and the log) — no kit part is touched
    - *While it prints:* B02
    - *Gate:* Checkpoint 00a: mains-work owner and room rule written down, meter tested live and dead, "what to do when it smokes/trips/bites" decided
    - *Sessions:* 2 × ~30 min
- **4 · Print** — [B07 — Electronics bay + lighting](print/B07-electronics-bay-and-lighting.md) · 16.0 h print · needs: Gate A
    - *While it prints:* Read Ch 09–10; if the Gen 2 upgrade kit is on hand, stage it for row 5
    - *Gate:* COB mounts flat on the reference; this batch carries `power_inlet_IECGS_1mm` and the **V2** `usb_adapter_mount_partial_cover`. Its heat-set bosses get inserts on kit day (Ch 09)
    - *Sessions:* 3 plate starts
- **5 · Both** — **Gen 2 belt-upgrade pause** on the Core One+ · ~1 day wall clock · needs: B07 finished, B08 not started — the contingency row; the baseline is the upgrade before B00
    - *While it prints:* Nothing prints — the Prusa is apart
    - *Gate:* Firmware ≥ 6.9.0, re-tension and re-square, self-test + input shaper, then **re-print `Voron_Design_Cube_v7` and re-pass Gate A** before B08
    - *Sessions:* —
- **6 · Print** — [B08 — Skirts and front modules](print/B08-skirts-and-front-modules.md) · 29.2 h print · needs: Gate A re-passed after the Gen 2 upgrade; B02 and B07 to hand for the ring dry-fit
    - *While it prints:* Nothing on the bench needs the kit — read Ch 03–05
    - *Gate:* Skirt faces flat with no lift; the ring dry-fits (power inlet from B07)
    - *Sessions:* 6 plate starts
- **7 · Print** — [B09 — Panels, filtration, spool](print/B09-panels-filtration-spool.md) · 21.8 h print · needs: B08
    - *While it prints:* Read Ch 11; the first spool runout is predicted inside B09-P2 — stage spool #2
    - *Gate:* Nevermore lid slides, cartridge snaps; the panel-clip test (extrusion, panel offcut, foam tape) waits for kit day
    - *Sessions:* 5 plate starts
- **8 · Print** — [B10 — Clicky-Clack door](print/B10-clicky-clack-door.md) · 5.7 h print · needs: B02 (`Handle`), B09; door swing decided
    - *While it prints:* Sort every pre-kit batch into its bins — print the [bin labels](../print/bin-labels.md) (25 bins, [scheme](print/README.md#bins)) and label ~25 containers or bags
    - *Gate:* Brims off clean; the bushing and dowel tests wait for the Clicky-Clack hardware
    - *Sessions:* 1 plate start
- **9 · Build** — [Ch 00 — Before you start](00-before-you-start.md) **KIT** · 2.5–4.0 · needs: the kit; B00 (`Heatset_Practice`, both rail guides)
    - *While it prints:* **Gate B first** (Step B00.7, 15 min: 625-2RS bore, MGN12 rail, seven inserts in the coupon), then B01-P1 on the Prusa before the inventory starts
    - *Gate:* Checkpoint 00: deck panel calipered, all seven rails cleaned and greased, both Discord questions posted
    - *Sessions:* 7 × ~30 min
- **10 · Print** — [B01 — Z drive assemblies](print/B01-z-drive-assemblies.md) · 22.8 h print · needs: **Gate B**
    - *While it prints:* Ch 00 finishes, then Ch 12 Part 1 and Ch 01
    - *Gate:* Batch gate (bearing seats), then the heat-set pass on every drive part in Ch 02
    - *Sessions:* 2 plate starts
- **11 · Build** — [Ch 12 Part 1 — image the Pi, install Klipper/Moonraker/Mainsail](12-software.md) **KIT** · ~1.0 of Ch 12's 2.0–3.0 · needs: the Pi from carton 2 only — no hardware gate
    - *While it prints:* B01
    - *Gate:* Pi on the network, web UI up, bench-powered from USB-C
    - *Sessions:* 2 × ~30 min
- **12 · Build** — [Ch 01 — Frame](01-frame.md) **KIT 2P** · 2.5–4.0 · needs: Ch 00
    - *While it prints:* B01 continues
    - *Gate:* Checkpoint 01: diagonals equal, frame square on the verified-flat counter
    - *Sessions:* 4 × ~30 min
- **13 · Print** — [B03 — A/B drive units + front idlers](print/B03-ab-drive-units-and-front-idlers.md) · 8.5 h print · needs: Gate B
    - *While it prints:* Ch 02 Z drives
    - *Gate:* Bearing-seat test on a drive frame (F695)
    - *Sessions:* 2 plate starts
- **14 · Build** — [Ch 02 — Z drives, Z idlers, Z rails, deck](02-z-drives.md) **KIT** · 4.25–6.25 · needs: Ch 01; B00, B01, **B02-P1**, **B02-P3**
    - *While it prints:* B03, then B04
    - *Gate:* Checkpoint 02: four Z carriages move freely, deck in, every set screw threadlocked on the flat
    - *Sessions:* 11 × ~30 min
- **15 · Print** — [B04 — XY joints + X carriage](print/B04-xy-joints-and-x-carriage.md) · 8.6 h print · needs: Gate B
    - *While it prints:* Ch 03 Build plate
    - *Gate:* Carriage pattern and shaft bores dry-fitted. `probe_retainer_bracket` off this plate is fitted in Ch 07/08, not in a batch
    - *Sessions:* 1 plate start
- **16 · Build** — [Ch 03 — Build plate](03-build-plate.md) **KIT** · 1.5–2.5 · needs: Ch 01, Ch 02
    - *While it prints:* B04, then B05
    - *Gate:* Checkpoint 03: magnet applied **and** its bolt holes trimmed straight after, plate bolted, three cables hanging below deck
    - *Sessions:* 4 × ~30 min
- **17 · Print** — [B05 — Z joints + Z chain](print/B05-z-joints-and-z-chain.md) · 6.4 h print · needs: Gate B; starts spool #3
    - *While it prints:* Ch 04
    - *Gate:* 8 mm shaft slides through every Z joint
    - *Sessions:* 1 plate start
- **18 · Build** — [Ch 04 — A/B drives and front idlers](04-ab-drives.md) **KIT** · 3.5–5.0 · needs: Ch 01; B00 (`pulley_jig`), **B02-P2**, B03
    - *While it prints:* B05, then B06
    - *Gate:* Checkpoint 04: A = rear right, B = rear left; both pulley heights set with `pulley_jig`
    - *Sessions:* 6 × ~30 min
- **19 · Print** — [B06 — Toolhead: SB, CW2, Klicky](print/B06-toolhead-sb-cw2-klicky.md) · 12.2 h print · needs: Gate B
    - *While it prints:* Ch 05 Gantry
    - *Gate:* Hotend seat flat; the Klicky set counted and **bagged as the alternative probe** (Ch 08.54), no magnets pressed
    - *Sessions:* 2 plate starts
- **20 · Build** — [Ch 05 — Gantry](05-gantry.md) **KIT 2P** · 5.0–7.0 · needs: Ch 00 rails, Ch 04; **B02-P3**, B04
    - *While it prints:* B06 — the last plate. If the kit landed before B08–B10 printed, those three batches run from here under Ch 06–12 instead, after the Gen 2 upgrade
    - *Gate:* Checkpoint 05: titanium backers fitted **before** the XY joints are torqued (survey W2); X carriage runs full travel
    - *Sessions:* 12 × ~30 min
- **21 · Build** — [Ch 06 Part A — Z axis: hang the gantry, Z belts](06-z-axis-and-gantry-squaring.md#part-a-chapter-06-z-axis-mechanical) **KIT 2P lift** · 3.5–5.0 · needs: Ch 02, Ch 05; B02, B05
    - *While it prints:* Printer idle — all 27 plates are done
    - *Gate:* Checkpoint 06: gantry travels its full Z range by hand, four Z belts even by ear
    - *Sessions:* 8 × ~30 min
- **22 · Build** — [Ch 07 — A/B belts, provisional tension](07-ab-belts.md) **KIT** · 2.5–4.0 · needs: Ch 04, Ch 05, Ch 06 Part A; B02, B03, B04, B05
    - *Gate:* Checkpoint 07: both belts ~110 Hz and equal after moving the gantry — **provisional**, Ch 06b releases it again
    - *Sessions:* 5 × ~30 min
- **23 · Build** — [Ch 08 — Toolhead](08-toolhead.md) **KIT** · 3.0–4.5 · needs: Ch 05, Ch 07; B02, B04, B06
    - *Gate:* Checkpoint 08: inductive probe built and Klicky bagged, every toolhead connector seated, ESD ground lead on
    - *Sessions:* 10 × ~30 min
- **24 · Build** — [Ch 09 — Electronics bay](09-electronics-bay.md) **KIT** · 2.5–4.0 · needs: Ch 01–03, Ch 06, Ch 00a; B07
    - *Gate:* Checkpoint 09: DIN rails **left-to-right**, everything mounted, nothing wired yet
    - *Sessions:* 7 × ~30 min
- **25 · Build** — [Ch 10 — Wiring](10-wiring.md) **KIT** · 5.0–7.0 · needs: Ch 03, Ch 06, Ch 07, Ch 08, Ch 09; B05, B07, B08 (`mount.stl`), B02 (`[a]_faceplate`) — the TFT module is built at 10.50
    - *Gate:* **LDO Checkpoint #1** — multimeter, machine unplugged. Hard gate: the bay does not close until it passes (survey W8)
    - *Sessions:* 14 × ~30 min
- **26 · Build** — [Ch 12 Part 2 — flash both MCUs, `printer.cfg` for a 350 Rev D+](12-software.md#step-1211-gate-power-the-bay-and-confirm-both-mcus-enumerate) **KIT** · the rest of 2.0–3.0 · needs: Ch 10
    - *Gate:* Checkpoint 12: toolboard ID reads `stm32g0b1xx` (survey W13); every 350 mm value uncommented (survey W14)
    - *Sessions:* 7 × ~30 min
- **27 · Build** — [Ch 11 Part A — skirts, bay fans, bottom panel, Z belt covers, Nevermore, spool, door hinges](11-skirts-panels-door.md#part-a-before-first-power-up) **KIT** · 3.0–4.0 · needs: Ch 10 Checkpoint #1, Ch 12 Part 2; B02, B07, B08, B09, **B10 by Step 11.46** (hinges, latch, handle)
    - *Gate:* Bay closed. **Back, side and top panels and the door stay off** — Ch 13 and Ch 06b need to reach the gantry
    - *Sessions:* 12 × ~30 min
- **28 · Build** — [Ch 13 — Initial startup](13-initial-startup.md) **KIT** · 2.5–4.0 plus ~1 h cube print · needs: Ch 06 Part A, Ch 07, Ch 10, Ch 11 Part A, Ch 12
    - *Gate:* Checkpoint 13: `PROBE_ACCURACY` σ < 0.003 mm, QGL converged, Z=0 set, cube printed and kept
    - *Sessions:* 11 × ~30 min
- **29 · Build** — [Ch 06b — Gantry squaring, cold, and provisional tension](06-z-axis-and-gantry-squaring.md#part-b-chapter-06b-gantry-squaring) **KIT 2P** · ~1.0 · needs: Ch 13 Step 13.34
    - *Gate:* Checkpoint 06b: gantry de-racked and the XY joints tightened **cold**; Z joints seated; A/B back to ~110 Hz provisional; Ch 13 Step 13.35 re-QGLs. No heat soak here — the chamber cannot close yet
    - *Sessions:* 1 × ~30 min
- **30 · Build** — [Ch 11 Part B — back, side and top panels, Clicky-Clack door](11-skirts-panels-door.md#part-b-after-ch-13) **KIT** · 1.0–2.0 · needs: Ch 13, Ch 06b; B02 `Handle`, B09, B10
    - *Gate:* Chamber reaches the 50–60 °C band with the door shut
    - *Sessions:* 5 × ~30 min
- **31 · Build** — [Ch 14 — Calibration and tuning: hot soak, final tension, re-check, then tune](14-calibration.md) **KIT** · 2.5–4.0 over 6–8 h · needs: Ch 13, Ch 06b, Ch 11 Part B (the chamber has to close for the soak)
    - *Gate:* The 1½–2 h heat soak with the panels on, Z joints tightened hot, A/B and Z belts at final tension, QGL and probe accuracy re-checked — then Checkpoint 14 and the tuning log filled in
    - *Sessions:* 13 × ~30 min

**Baseline vs. row 5.** The plan is to do the Gen 1 → Gen 2 belt upgrade *before* B00, so the whole Voron run prints on GT1.5. Row 5 is the contingency for an upgrade kit that turns up mid-run: pause at the end of B07, because B08–B10 are 12 of the 27 plates and hold every surface anyone will ever look at ([print plan §8](../voron-print-plan.md#8-where-to-do-the-core-one-gen-2-belt-upgrade)). Second-best boundary is before B02, whose plate P1 carries the Stealthburner body.

**Dependencies inside B02.** The orange day prints once, but its plates are consumed at five different times: **B02-P1 + B02-P3** gate Ch 02 (Z drive baseplates, belt tensioners, Z tensioners); the cable bridge and endstop pod off P3 go to Ch 05; the Stealthburner accent parts off P1 and P3 go to Ch 08; **B02-P2** gates Ch 04 (A/B tensioners); the Z belt clips and chain retainers gate Ch 06 Part A; and the belt guards, fan grills, keystone blank, TFT faceplate and door `Handle` are not needed until Ch 11.

---

## Critical path

| | |
|---|---|
| Print time | **157.1 h** across 27 plates in 11 batches (1813 g black, 279 g orange) — **98.6 h in the six pre-kit batches**, **58.5 h in the five kit-day batches** |
| Hands-on time | **59.4 h** — the sum of the chapter Time midpoints (Ch 06b's ~1 h cold squaring pass is on top of Ch 06's figure) |
| Printing, elapsed | Pre-kit: **~10 printer-days ≈ 1.5–2 weeks** (swap-limited, ~10 print-hours/day; the floor is ~4 days if you change plates the minute each one ends). Kit day onward: ~6 printer-days, all under Ch 00–05 |
| Building, elapsed | **~2.7 weeks ≈ 3 weeks** at 22 h/week |
| **(a) After the Prusa is running** | **≈ 4.5–5 calendar weeks** — ~1.5–2 weeks printing the pre-kit batches while the kit ships, then ~3 weeks of build with B01 and B03–B06 printing underneath |
| **(b) After the kit arrives** | **≈ 3 calendar weeks** — Gate B and B01 (22.8 h) run under Ch 00–01 (5–8 h hands-on ≈ 2–3 days at 22 h/week), so Ch 02 waits on B01-P2 for half a day at most; B03–B06 print under Ch 02–05 and nothing after Ch 05 waits on plastic |

**≈ 141 sessions of ~30 min** — the sum of every assembly chapter's `Sessions:` line (Ch 00, 00a–14, 06b and both parts of 11 and 12 counted once each) — plus 27 plate starts of ~5 min each and the inspect passes after each batch.

Assumptions: 22 h/week of hands-on (2 h on each of five weekdays, 6 h on each of two weekend days), the Core One+ printing unattended overnight with about two plate swaps a day, no reprints beyond the plan's 24 % filament margin, the Gen 2 upgrade done before B00, and the kit landing after the pre-kit run ends.

---

## Chapters

### Assembly

| Chapter | Scope | Time (h) | Sessions | Prerequisites |
|---|---|---|---|---|
| [00 — Before you start](00-before-you-start.md) | Inventory against the BOM, tools, flat reference, heat-set practice, clean and grease all seven rails | 2.5–4.0 | 7 × ~30 min | The kit; B00 (`Heatset_Practice`, both rail guides). Gate B (Step B00.7) runs the same morning |
| [00a — Mains safety](00a-mains-safety.md) | Decide who does the mains work, buy and test the meter, agree the who's-in-the-room and smoke/trip/bite rules — read before Ch 09 | 0.75–1.0 | 2 × ~30 min | Ch 00 Steps 00.8 and 00.30 as reading. No kit part, no printed part — doable before the kit |
| [01 — Frame](01-frame.md) | 2020 frame and the two bed extrusions, squared on a verified-flat surface | 2.5–4.0 | 4 × ~30 min | Ch 00. No printed part required |
| [02 — Z drives, Z idlers, Z rails, deck](02-z-drives.md) | Four Z drives, four Z idlers, four Z rails, deck panel and supports | 4.25–6.25 | 11 × ~30 min | Ch 01; B00, B01, B02-P1, B02-P3 |
| [03 — Build plate](03-build-plate.md) | 355×355×10 mm plate, magnet sheet, bed harness dressed below deck | 1.5–2.5 | 4 × ~30 min | Ch 01, Ch 02. No printed part required |
| [04 — A/B drives and front idlers](04-ab-drives.md) | The four CoreXY sub-assemblies that carry the A and B belts | 3.5–5.0 | 6 × ~30 min | Ch 01; B00 (`pulley_jig`), B02-P2, B03 |
| [05 — Gantry](05-gantry.md) | X and Y axes, both XY joints, X carriage, titanium backers | 5.0–7.0 | 12 × ~30 min | Ch 00 rails, Ch 04; B02-P3, B04 |
| [06 Part A — Z axis](06-z-axis-and-gantry-squaring.md#part-a-chapter-06-z-axis-mechanical) | Hang the gantry on the Z joints, belt all four Z corners | 3.5–5.0 | 8 × ~30 min | Ch 02, Ch 05; B02, B05 |
| [06b — Gantry squaring](06-z-axis-and-gantry-squaring.md#part-b-chapter-06b-gantry-squaring) | The real squaring pass, **cold** — needs motor control, so it runs out of Ch 13; ends at provisional A/B tension. The hot soak and final tension are Ch 14 | ~1.0 | 1 × ~30 min | Ch 13 Step 13.34 |
| [07 — A/B belts](07-ab-belts.md) | Cut, route and clamp both CoreXY belts; provisional tension; inductive probe on the carriage | 2.5–4.0 | 5 × ~30 min | Ch 04, Ch 05, Ch 06 Part A; B02, B03, B04, B05 |
| [08 — Toolhead](08-toolhead.md) | Stealthburner, Clockwork 2, Revo Voron (HF nozzle), Nitehawk-SB V2, hung on the carriage; Klicky bagged | 3.0–4.5 | 10 × ~30 min | Ch 05, Ch 07; B02, B04, B06 |
| [09 — Electronics bay](09-electronics-bay.md) | DIN rails, ducts, PSU, SSR, Leviathan and Pi, mains inlet, WAGOs, both endstops — mounted, not wired | 2.5–4.0 | 7 × ~30 min | Ch 01–03, Ch 06, Ch 00a; B07 |
| [10 — Wiring](10-wiring.md) | Every harness, ending at LDO Checkpoint #1 | 5.0–7.0 | 14 × ~30 min | Ch 03, Ch 06, Ch 07, Ch 08, Ch 09; B05, B07, B08 (`mount.stl`), B02 (`[a]_faceplate`) — both at Step 10.50 |
| [11 — Skirts, panels, door, filtration](11-skirts-panels-door.md) | Part A closes the bay and builds the door hinges and handle; Part B fits the back, side and top panels and hangs the Clicky-Clack door after Ch 06b | 3.0–4.0 + 1.0–2.0 | 12 + 5 × ~30 min | Part A: Ch 10 + Checkpoint #1; B02, B07, B08, B09, B10 (by Step 11.46). Part B also Ch 13, Ch 06b; B09, B10, B02 `Handle` |
| [12 — Software](12-software.md) | Pi image, Klipper/Moonraker/Mainsail, both MCUs flashed, `printer.cfg` for a 350 Rev D+ | 2.0–3.0 | 9 × ~30 min | Part 1: the Pi only. Part 2: Ch 10 + Checkpoint #1. No printed part required |
| [13 — Initial startup](13-initial-startup.md) | First power-on through temps, fans, motors, endstops, homing, PID, QGL, Z=0, bed mesh and the first cube | 2.5–4.0 | 11 × ~30 min | Ch 06 Part A, Ch 07, Ch 10, Ch 11 Part A, Ch 12. No printed part required |
| [14 — Calibration and tuning](14-calibration.md) | Hot soak with the chamber closed, Z joints tightened hot, final belt tension, squaring and QGL re-check; then rotation distance, chamber and `PRINT_START`, cube measurement, input shaper, PA, flow | 2.5–4.0 | 13 × ~30 min | Ch 13, Ch 06b, Ch 11 Part B, Ch 12; the B00 reference cube and Ch 13's cube |

### Reference

| Chapter | Scope |
|---|---|
| [15 — Troubleshooting index](15-troubleshooting.md) | Symptom-first lookup into the fix already owned by a step, checkpoint or callout in Ch 00–14 and the print chapters |
| [16 — Glossary](16-glossary.md) | Every term the manual uses without stopping to define it, with the chapter or step it first matters at |

### Print batches

Full table with grams and plate counts: [print/README.md](print/README.md). Profile, overrides and the two-part calibration gate: [print/00-slicer-setup.md](print/00-slicer-setup.md). Print order is the timeline above — the six Gate A batches before the kit, the five Gate B batches from kit day.

| Batch | Scope | Plates · hours | Print gate |
|---|---|---|---|
| [B00 — Calibration & jigs](print/B00-calibration-and-jigs.md) | Test cube, heat-set coupon, rail guides, pulley jig, one Z-drive retainer as the bore coupon | 1 · 4.0 | None — it *is* the gate: Gate A on the day, Gate B on kit day |
| [B02 — Accent parts, orange](print/B02-accent-parts-orange.md) | Every orange part in the build, in one session | 3 · 21.9 | Gate A |
| [B07 — Electronics bay + lighting](print/B07-electronics-bay-and-lighting.md) | WAGO and PSU mounts, DIN clips, eight COB mounts, `power_inlet_IECGS_1mm`, `usb_adapter_mount_partial_cover` | 3 · 16.0 | Gate A |
| [B08 — Skirts and front modules](print/B08-skirts-and-front-modules.md) | The 350 skirt set, front touchscreen module, grills and guards | 6 · 29.2 | Gate A, re-passed after the Gen 2 upgrade |
| [B09 — Panels, filtration, spool](print/B09-panels-filtration-spool.md) | Panel clips, Z belt covers, Nevermore Micro V5 Duo, spool holder | 5 · 21.8 | Gate A (after B08) |
| [B10 — Clicky-Clack door](print/B10-clicky-clack-door.md) | The door set, plus the orange `Handle` from B02 | 1 · 5.7 | Gate A (after B09) |
| [B01 — Z drive assemblies](print/B01-z-drive-assemblies.md) | Z drive bodies, retainers, motor mounts, Z tensioner brackets, deck supports | 2 · 22.8 | **Gate B** (kit day) |
| [B03 — A/B drive units + front idlers](print/B03-ab-drive-units-and-front-idlers.md) | A and B drive frames, both front idler pairs | 2 · 8.5 | Gate B |
| [B04 — XY joints + X carriage](print/B04-xy-joints-and-x-carriage.md) | MGN12 XY joint set, X carriage halves, `probe_retainer_bracket` | 1 · 8.6 | Gate B |
| [B05 — Z joints + Z chain](print/B05-z-joints-and-z-chain.md) | Upper and lower Z joints, Z chain anchor and guide | 1 · 6.4 | Gate B |
| [B06 — Toolhead](print/B06-toolhead-sb-cw2-klicky.md) | Stealthburner, Clockwork 2, `cw2_captive_pcb_cover`; the Klicky set, bagged as the alternative probe | 2 · 12.2 | Gate B |

---

## Every step links to its source

Every step ends with a `Source:` line naming the exact manual page, LDO doc or print-plan section it was transcribed from, pinned to a specific commit for GitHub-hosted files so the link doesn't drift under you. If a step's text and its Source line disagree, or the source itself looks wrong, file a correction with the [correction issue template](https://github.com/alexlicohen/voron-24-350-build-manual/issues/new/choose) rather than editing the step from memory.

---

## Corrections log

What the kit actually is, where it differs from the published documents, and which chapter holds the detail. This is the list to re-check whenever LDO updates its docs.

To add a row: append it with the next `#`, today's date, and fill "Source that was wrong" / "Verified against" only when the correction actually names them — otherwise leave `—` rather than guessing.

| # | Date | Correction | Source that was wrong | Detail lives in | Verified against |
|---|---|---|---|---|---|
| 1 | 2026-09-05 | **Rev D+ = Nitehawk-SB V2.** The difference is electrical apart from one printed part: the V2 repo's `usb_adapter_mount_partial_cover.stl` (it exposes a mounting point for the ground lug), not the V1 `usb_adapter_mount.stl` | — | [Ch 09 Step 09.25](09-electronics-bay.md); flagged in Ch 00; printed in [B07](print/B07-electronics-bay-and-lighting.md) | — |
| 2 | 2026-09-05 | **The magnet sheet is user-applied**, and its bolt holes are trimmed immediately after — not later | — | [Ch 03 Step 03.9](03-build-plate.md) | — |
| 3 | 2026-09-05 | **Both probes ship. Build the inductive one.** Omron inductive for QGL, LDO nozzle probe for Z=0; the Klicky parts get printed (B06-P2) and bagged | — | [Ch 08 Step 08.54](08-toolhead.md); config in [Ch 12](12-software.md); printed in [B06](print/B06-toolhead-sb-cw2-klicky.md) | — |
| 4 | 2026-09-05 | **RETRACTED 2026-09-06.** Originally: "DIN rails run left-to-right, per LDO — the official manual runs them front-to-back." The manual's own p.28–29 already show the rails left-to-right; manual and LDO agree, so there is no deviation (Ch 09 fix, review F5) | This log (row 4 as first written) | [Ch 09 Step 09.5](09-electronics-bay.md) | manual p.28–29 page images |
| 5 | 2026-09-05 | **Which Leviathan you have is contested**: STM32F446 (V1.1/V1.2) or STM32H743 (V1.3). Processor, clock and bootloader offset all differ; settle it from the board, not from a document | — | [Ch 12 Step 12.13](12-software.md) | The physical board (STM32 marking), not a document |
| 6 | 2026-09-05 | **The Nitehawk-SB V2 ESD grounding scheme** shipped as three images with no prose until LDO's board doc was updated **2026-07-10**. Treat grounding as a required build step | LDO Nitehawk-SB V2 board doc (pre-2026-07-10, images only, no prose) | [Ch 10 Step 10.58](10-wiring.md); also Ch 08 | LDO board doc, updated 2026-07-10 |
| 7 | 2026-09-05 | **Deck panel: 3 mm or 4 mm.** LDO's guides say 4 mm, LDO's own BOM says 3 mm. Your caliper decides which `deck_support_*` you print | LDO guides (4 mm) vs. LDO's own BOM (3 mm) — internally inconsistent | [Ch 02 Step 02.12](02-z-drives.md); measured at Ch 00 | Caliper measurement of your kit's deck panel |
| 8 | 2026-09-05 | **PrusaSlicer shrinkage compensation and XY size compensation must both be zero.** Voron parts are already drawn for ABS/ASA shrinkage; compensating again ruins every bearing fit | — | [print/00-slicer-setup.md](print/00-slicer-setup.md) | — |
| 9 | 2026-09-05 | **Four GT2 20T 9 mm idlers are consumed in Ch 02** on the Z tensioners; the two XY joints need two more. Do not raid the bag early | — | [Ch 02 Step 02.40](02-z-drives.md); consumed again in [Ch 05](05-gantry.md) | — |
| 10 | 2026-09-05 | **A = rear right, B = rear left**, so the A idler is the front-right pair and the B idler the front-left pair. B03's plate captions *had* the pairing the wrong way round (fixed 2026-09-05; B03-P1 = A side = `front_idler_right_*`) | B03 plate captions (this manual, pre-fix) | [Ch 04 Step 04.2](04-ab-drives.md); belt paths in [Ch 07](07-ab-belts.md) | Ch 04 Step 04.2 A/B convention |
| 11 | 2026-09-05 | **`power_inlet_IECGS_1mm` prints in B07, not B08** — it is fitted in the electronics bay at manual p.156/167, not with the skirts. It needs its **own plate B07-P3**: with 3 mm brims it will not fit beside the eight COB mounts (84 % bed fill). B07 is 3 plates, and the build is **27 plates / 134.3 h at the time (re-estimated by slicing to 157.1 h, row 20)** | — | [Ch 09](09-electronics-bay.md); [B07](print/B07-electronics-bay-and-lighting.md) | — |
| 12 | 2026-09-05 | **625-2RS is the Z-drive bearing (16 mm OD); F695 is the A/B-drive, front-idler and XY-joint bearing (13 mm OD).** Both are 5 mm bore, so you cannot sort them by bore. The B00 press-fit gate tests a **625-2RS** seat | — | [print/00-slicer-setup.md](print/00-slicer-setup.md); [B01](print/B01-z-drive-assemblies.md), [B03](print/B03-ab-drive-units-and-front-idlers.md), [Ch 00](00-before-you-start.md), [Ch 02](02-z-drives.md), [Ch 04](04-ab-drives.md) | — |
| 13 | 2026-09-05 | **A/B motor pulleys are GT2 20T ×2 in the 6 mm width.** The kit's four 9 mm 20T pulleys are all Z-drive parts — using one on an A/B motor steals a Z pulley and puts a 9 mm pulley in the 6 mm belt plane an F695 pair forms | — | [Ch 04 Step 04.24](04-ab-drives.md); Z pulleys at [Ch 02](02-z-drives.md) | — |
| 14 | 2026-09-05 | **Bed extrusions: 130 mm is the clear gap between inner faces**, i.e. 65 mm each side of the centreline and **150 mm centre-to-centre**. Manual p.20's dimension lines land on the inner faces | — | [Ch 01 Step 01.19](01-frame.md); checked at [Ch 03 Step 03.11](03-build-plate.md) | Ch 03 Step 03.11 build-plate fit check |
| 15 | 2026-09-05 | **The rails are 400 mm, not the manual's 250-spec length.** ~10 M3×8 + T-nuts per MGN9 Y rail, ~8 for the MGN12 X rail — count the holes; every other hole | Official Voron 2.4r2 assembly manual (specifies 250 mm rails) | [Ch 05 Steps 05.10–05.12, 05.32–05.33](05-gantry.md); same rule at [Ch 02](02-z-drives.md) | Hole count on the 400 mm rails as received |
| 16 | 2026-09-05 | **Rails are cleaned and greased once, in Ch 00.** Ch 02 only verifies; the DIN rails are installed once, in Ch 09 Step 09.5, and Ch 02 only stages their T-nuts | — | [Ch 00 Steps 00.18–00.21](00-before-you-start.md), [Ch 02 Steps 02.05 / 02.15](02-z-drives.md), [Ch 09 Step 09.5](09-electronics-bay.md) | — |
| 17 | 2026-09-05 | **Printer preset is `Prusa CORE One 0.4 nozzle`** — the CORE One family dropped the "Original" prefix, so a search for "Original Prusa CORE One" finds nothing. *Superseded by #21: the HF0.4 variant is the preset in use* | — | [print/00-slicer-setup.md](print/00-slicer-setup.md) | — |
| 18 | 2026-09-05 | **Rotating a part about Z to fit the plate is allowed**; changing which face sits on the bed is not. B08-P1 cannot be sliced without a 90° Z rotation of **`rear_center_skirt_350`** (it stands front-to-back beside an unturned `side_fan_support`; as first written this row named the wrong part — corrected 2026-09-06 against the committed 3MF) | This log (row 18 as first written) | [print/00-slicer-setup.md](print/00-slicer-setup.md); [B08 Step B08.2](print/B08-skirts-and-front-modules.md) | `slicer/plates/B08-P1.3mf` mesh extents |
| 19 | 2026-09-05 | **PrusaSlicer version posture:** 2.9.6 for the dimension-critical batches (B00 gate, B01, B03–B06); the 3.0 preview is acceptable for B08–B10 with overrides re-entered by hand. Any toolchain change re-runs the B00 gate | — | [print/00-slicer-setup.md](print/00-slicer-setup.md#prusaslicer-30-preview) | — |
| 20 | 2026-09-05 | **Print estimates now from PrusaSlicer 2.9.6 slices (were a throughput model).** Totals moved to 27 plates, 157.1 h, 1813 g black + 279 g orange | Throughput-model estimate (this manual, pre-fix) | `print/README.md` | Sliced `.3mf` project per plate (`slicer/estimates.csv`) |
| 21 | 2026-09-05 | **HF 0.4 nozzle: slicer profiles use the Core One HF presets** — `Prusa CORE One HF0.4 nozzle` printer preset and `Prusament ASA @COREONE HF0.4` filament preset, both hotter and faster than their non-HF equivalents. In the GUI the project shows them as `0.20mm STRUCTURAL @COREONE 0.4 (modified)` and `Prusament ASA @COREONE HF0.4 - Voron black` | — | [print/00-slicer-setup.md](print/00-slicer-setup.md) | `Slic3r_PE.config` inside every committed `.3mf` |
| 22 | 2026-09-06 | **The B00 calibration gate is split.** Three of its seven coupons (heat-set inserts, the MGN12 rail, the 625-2RS bearing) only arrive with the kit, so a pre-kit builder could never pass "all seven". **Gate A** (the cube) releases B02, B07 and — after the Gen 2 upgrade — B08–B10; **Gate B** (kit day) releases B01 and B03–B06. Pre-kit print order is B00 → B02 → B07 → (Gen 2) → B08 → B09 → B10 | This manual and print plan §1.4, pre-fix ("only when all seven pass, start B01") | [print/00-slicer-setup.md](print/00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade); [B00 Steps B00.5 / B00.7](print/B00-calibration-and-jigs.md); [print/README.md](print/README.md); this timeline | Ch 00's insert count (kit-supplied, 153) and the B00 plate contents |
| 23 | 2026-09-06 | **Ch 06b is cold; the hot soak moved to Ch 14.** Timeline order is Ch 13 → Ch 06b (cold squaring, provisional tension) → Ch 11 Part B (panels) → Ch 14 (hot soak with the chamber closed, Z joints tightened hot, final tension, re-check). As first written 06b soaked a machine with no back, top or side panels | This manual's timeline and Ch 06b Steps 06b.16–06b.18, pre-fix | [Ch 06b](06-z-axis-and-gantry-squaring.md#part-b-chapter-06b-gantry-squaring); [Ch 14 Parts A–B](14-calibration.md); this timeline | Voron gantry-squaring procedure (assumes a panelled machine, sides off) — review F7 |
| 24 | 2026-09-06 | **Each A/B belt is teeth-on at exactly one XY joint: A at the RIGHT joint's upper 20T, B at the LEFT joint's lower 20T; smooth-back on the other joint's F695 stack.** A leaves the X carriage westward, rounds the LEFT joint's plain F695 stack smooth-back, wraps its own drive and front idler, and returns through the RIGHT joint on its upper 20T teeth-on; B mirrors it: first turn teeth-on the LEFT joint's lower 20T, return smooth-back on the RIGHT joint's lower F695 (manual p.105, p.131, p.135–138; Ch 07 Steps 07.16 / 07.17 / 07.23). | Ch 07 intro and Step 07.23 Check, pre-fix ("smooth back on every plain stack") | [Ch 07 Steps 07.16 / 07.17 / 07.23 / 07.23](07-ab-belts.md); [Ch 05 Step 05.29](05-gantry.md) | Manual p.135 and p.138; Ch 05.29 — review F4 |

---

## How to update this manual

1. Everything is markdown under `docs/`; one chapter per file, `docs/manual/NN-slug.md`, print batches in `docs/manual/print/`.
2. Serve it to the iPad with `./scripts/serve.sh` and read it at the bench on the LAN URL.
3. Chapter format — header block, `### Step NN.M`, Parts / Do / Check, `⚠ Rev D+ / LDO:` callouts, Checkpoint, Common mistakes — is fixed by [CONVENTIONS.md](CONVENTIONS.md). Follow it exactly.
4. A new correction goes in **two** places: the log above (one row, with the chapter link) and inline at the step it affects, as a `⚠ Rev D+ / LDO:` callout. Never only in a preamble.
5. [`docs/voron-print-plan.md`](../voron-print-plan.md) and [`docs/voron-build-instructions-survey.md`](../voron-build-instructions-survey.md) are the sources these chapters were written from — change them first when a fact moves, then the chapters, then this page.
