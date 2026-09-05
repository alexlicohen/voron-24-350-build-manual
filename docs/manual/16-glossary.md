# Chapter 16 — Glossary

Every term this manual uses without stopping to explain it, with the chapter or step where it first matters. Ch 00 Steps [00.23](00-before-you-start.md#step-0023-print-guidelines-p4)–[00.29](00-before-you-start.md#step-0029-how-to-read-an-exploded-view-and-the-page-number-contract-p11) teach the fastener and drawing vocabulary once and then rely on it for ~600 steps; this page makes that reliance recoverable instead of assumed.

**Time:** none — reference page.

**Prerequisites:** none. **Tools:** none. **Printed parts:** none. **Hardware:** none.

**Read first**

- **One line each, and the link is the real answer.** Where a definition and a step disagree, the step wins.
- **Symbols first, then A–Z.** Document names are folded into the alphabet under their own initial (LDO Build Notes under **L**, Voron Assembly Manual under **V**).
- **"First matters at"** is the earliest place in *this* manual where you must already understand the term — not necessarily where the word first appears.

---

## Symbols, prefixes and markers

| Term | What it means | First matters at |
|---|---|---|
| `[a]_` | STL filename prefix: print in the **accent** colour — Prusa Orange on this build. Every `[a]_` part is collected into batch B02 | [00.24](00-before-you-start.md#step-0024-file-naming-and-where-to-get-help-p56) |
| `[o]_` | Prefix: **opaque** — the part must block light. Galaxy Black satisfies it | [print/00-slicer-setup — Colour key](print/00-slicer-setup.md#colour-key) |
| `[c]_` | Prefix: **clear / translucent**. Do not print — LDO supplies the one such part (the SB LED diffuser) in clear PETG | [00.6](00-before-you-start.md#step-006-set-aside-the-ten-ldo-supplied-printed-parts) |
| `_xN` | Filename suffix: the **quantity the machine needs**, regardless of how many bodies are in the file. `_x4` means four | [00.24](00-before-you-start.md#step-0024-file-naming-and-where-to-get-help-p56) |
| `B00`–`B10` | Print-batch ids, always two digits. A plate inside a batch is `B07-P3` — two-digit batch, unpadded plate number | [00.11](00-before-you-start.md#step-0011-bin-the-workspace-by-chapter) |
| `p.NN` | A page in the official Voron 2.4r2 Assembly Manual PDF, which has not changed since 2023-07-18 — the page numbers do not move | [00.29](00-before-you-start.md#step-0029-how-to-read-an-exploded-view-and-the-page-number-contract-p11) |
| `nhk:` | Klipper pin prefix for the **toolboard** MCU (`[mcu nhk]`). A `nhk:` pin is on the Nitehawk, not the Leviathan | [12.21](12-software.md#step-1221-download-the-correct-config-file) |
| `!` (leading, on a pin) | Klipper's invert marker. On an endstop it is almost always the wrong fix — stock Voron endstops are normally-closed to ground | [13.17](13-initial-startup.md#step-1317-query_endstops-with-everything-released) |
| `OL` | Multimeter display for **open / over-range** — no measurable path. The expected reading for L-to-PE, bed-to-plate and any 24 V node to earth | [10.13](10-wiring.md#step-1013-measure-the-bed-heater-before-you-connect-it) |
| `(verify on bench)` | This manual's marker for a count, torque or dimension **no source publishes**. Measure it yourself; never invent it | [CONVENTIONS](CONVENTIONS.md) |
| `Source:` | The line closing every step, linking the exact page or guide section that step was transcribed from | [CONVENTIONS](CONVENTIONS.md) |
| `Pause:` | A safe stopping point, with the minutes since the last one and the state you leave the machine in | [CONVENTIONS](CONVENTIONS.md) |

Source: [Ch 00 Step 00.24](00-before-you-start.md#step-0024-file-naming-and-where-to-get-help-p56) · [print/00-slicer-setup — Colour key](print/00-slicer-setup.md#colour-key) · [docs/manual/CONVENTIONS.md](CONVENTIONS.md)

---

## A

| Term | What it is | First matters at |
|---|---|---|
| **A and B** | The two CoreXY motors and their belts. A is the right-hand drive, B the left; moving both together moves X, moving them oppositely moves Y | [04 — A/B drives](04-ab-drives.md) |
| **ADXL345** | The accelerometer built into the Nitehawk-SB V2, used by `SHAPER_CALIBRATE` to measure resonance | [14.12](14-calibration.md#step-1412-bring-up-the-on-board-accelerometer) |
| **Anodising** | The hard oxide layer on the extrusions. It is an electrical **insulator**, which is why it gets scraped under the frame PE washer | [10.16](10-wiring.md#step-1016-frame-pe) |
| **ASA** | The material this whole build is printed in — Voron spec for an enclosed printer, 4 perimeters, 5 top/bottom, 40 % infill, 0.2 mm layers | [00.23](00-before-you-start.md#step-0023-print-guidelines-p4) |

Source: [Ch 04](04-ab-drives.md) · [Ch 14 Step 14.12](14-calibration.md#step-1412-bring-up-the-on-board-accelerometer) · [Ch 00 Step 00.23](00-before-you-start.md#step-0023-print-guidelines-p4)

---

## B

| Term | What it is | First matters at |
|---|---|---|
| **Backer** (titanium extrusion backer) | A titanium strip bolted to the face **opposite** a linear rail, to cancel the bimetallic bow a steel rail induces in an aluminium extrusion | [05.16](05-gantry.md#step-0516-unpack-and-identify-the-titanium-backers) |
| **Batch BOM** | *Your kit's* bill of materials page on LDO's site, keyed to the serial on carton 1 — not the generic page | [00.2](00-before-you-start.md#step-002-find-the-kit-serial-and-open-your-batch-bom-page) |
| **Bed mesh** | A grid of probed heights that Klipper applies as a Z correction during a print. Taken **hot and after QGL**, never before | [12.34](12-software.md#step-1234-add-a-bed_mesh-section) |
| **BHCS** | Button Head Cap Screw — domed head, mostly M5 in this build | [00.25](00-before-you-start.md#step-0025-fastener-names-part-1-p7) |
| **Blind joint** | The frame joint: a BHCS head slides into one extrusion's slot and threads into the tapped end of the mating extrusion, tightened through an access hole | [00.28](00-before-you-start.md#step-0028-blind-joints-p10) |
| **BMG** | The dual-geared filament drive inside Clockwork 2 — the idler assembly you grease and the tension arm that loads it | [08.9](08-toolhead.md#step-089-build-the-bmg-idler-assembly-and-grease-it) |
| **Brim** | A single-layer skirt fused to the part, added only where a plate needs adhesion help. Most Voron plates do not | [print/00-slicer-setup — Orientation & brim](print/00-slicer-setup.md#orientation-brim) |

Source: [Ch 05 Step 05.16](05-gantry.md#step-0516-unpack-and-identify-the-titanium-backers) · [Ch 00 Steps 00.2](00-before-you-start.md#step-002-find-the-kit-serial-and-open-your-batch-bom-page), [00.25](00-before-you-start.md#step-0025-fastener-names-part-1-p7), [00.28](00-before-you-start.md#step-0028-blind-joints-p10) · [Ch 08 Step 08.9](08-toolhead.md#step-089-build-the-bmg-idler-assembly-and-grease-it)

---

## C

| Term | What it is | First matters at |
|---|---|---|
| **CAN toolboard** | A toolboard that talks to the host over CAN bus on a two-wire umbilical. **This build has none** — the Nitehawk-SB V2 is a **USB** toolboard, so it appears as a second Klipper MCU on `/dev/serial/by-id` | [10.54](10-wiring.md#step-1054-identify-your-umbilical-and-its-two-connectors) |
| **CAT rating** | A multimeter's IEC 61010 measurement category — how big a transient it can survive where you use it, not what voltage it can display | [00a.3](00a-mains-safety.md#step-00a3-buy-a-meter-that-is-rated-for-the-job) |
| **Checkpoint #1** | LDO's mains gate: seven meter measurements on an unplugged machine, then one deliberate power-on. The bay does not close until it passes | [Ch 10 Section 2](10-wiring.md#section-2-checkpoint-1-exactly-as-ldo-writes-it) |
| **Clicky-Clack** | The magnetic-latch front door kit (LDO, blue frame) fitted instead of the stock Voron doors | [11.44](11-skirts-panels-door.md#step-1144-assemble-the-clicky-clack-door-frame) |
| **Clockwork 2 (CW2)** | The Voron extruder that mounts to the Stealthburner — BMG drive, printed body, its own insert pass | [08.3](08-toolhead.md#step-083-inserts-clockwork-2-main-body) |
| **COB light strip** | The chamber lighting: two strips on printed mounts, joined by a splitter PCB, on the Leviathan's `LED-Strip` port | [12.32](12-software.md#step-1232-fans-and-lighting-nevermore-cob-strips-bay-fans) |
| **CoreXY** | The motion system: two fixed motors drive two crossed belts; neither motor moves the bed or itself. Diagonal motion means A and B are wrong | [04 — A/B drives](04-ab-drives.md) |

Source: [Ch 10 Step 10.54](10-wiring.md#step-1054-identify-your-umbilical-and-its-two-connectors) · [Ch 00a Step 00a.3](00a-mains-safety.md#step-00a3-buy-a-meter-that-is-rated-for-the-job) · [Ch 08 Step 08.3](08-toolhead.md#step-083-inserts-clockwork-2-main-body) · [Ch 11 Step 11.44](11-skirts-panels-door.md#step-1144-assemble-the-clicky-clack-door-frame)

---

## D

| Term | What it is | First matters at |
|---|---|---|
| **Deck panel** | The acrylic floor of the chamber, above the electronics bay. Its thickness (3 or 4 mm) is disputed between LDO's own documents — caliper it | [02.12](02-z-drives.md#step-0212-caliper-the-deck-panel-and-choose-the-support-thickness) |
| **DFU** | STM32's built-in USB bootloader mode, entered with the RESET/BOOT0 buttons. The recovery route when Katapult has been overwritten | [12.16](12-software.md#step-1216-recovery-only-reinstall-katapult-on-the-leviathan-over-dfu) |
| **DIN rail** | The standard 35 mm steel mounting rail. This bay has two, running **left to right** per LDO — not front-to-back as the manual draws | [09.5](09-electronics-bay.md#step-095-fit-the-two-din-rails-running-left-to-right) |
| **Drag chain** | The articulated plastic chain carrying cables to a moving part. Three here: X, Y and Z. Cables inside must stay **loose** | [10.59](10-wiring.md#step-1059-fit-the-x-drag-chain) |
| **Drying** | Heating filament to drive out absorbed moisture. ASA needs it only if the spool has been open a while or shows bubbling | [print/00-slicer-setup — Drying](print/00-slicer-setup.md#drying) |

Source: [Ch 02 Step 02.12](02-z-drives.md#step-0212-caliper-the-deck-panel-and-choose-the-support-thickness) · [Ch 12 Step 12.16](12-software.md#step-1216-recovery-only-reinstall-katapult-on-the-leviathan-over-dfu) · [Ch 09 Step 09.5](09-electronics-bay.md#step-095-fit-the-two-din-rails-running-left-to-right) · [Ch 10 Step 10.59](10-wiring.md#step-1059-fit-the-x-drag-chain)

---

## E

| Term | What it is | First matters at |
|---|---|---|
| **Elephant foot** | The first layer coming out wider than the rest, from squish plus heat. Corrected with the slicer's compensation, in 0.05 mm steps | [14.11](14-calibration.md#step-1411-caliper-the-cube-against-the-prusa-printed-one) |
| **E-RV** | The hotend code embossed on both Stealthburner printhead halves for **E3D Revo Voron**. Read it before you build — it decides which printhead folder you slice | [08.1](08-toolhead.md#step-081-sort-the-printed-parts-and-confirm-the-hotend-code) |
| **ESD ground** | The Rev D+ bonding path from the extruder motor body to the toolboard, exposed by the V2 partial USB-adapter cover | [10.58](10-wiring.md#step-1058-fit-the-esd-grounding-path) |
| **Extrusion multiplier (EM) / flow** | The slicer's scaling of how much plastic is extruded. The correct lever for an oversize part — **not** XY size compensation | [14.19](14-calibration.md#step-1419-extrusion-multiplier-flow-the-2-pass) |

Source: [Ch 14 Steps 14.11](14-calibration.md#step-1411-caliper-the-cube-against-the-prusa-printed-one), [14.19](14-calibration.md#step-1419-extrusion-multiplier-flow-the-2-pass) · [Ch 08 Step 08.1](08-toolhead.md#step-081-sort-the-printed-parts-and-confirm-the-hotend-code) · [Ch 10 Step 10.58](10-wiring.md#step-1058-fit-the-esd-grounding-path)

---

## F

| Term | What it is | First matters at |
|---|---|---|
| **F695** | Flanged bearing, 5 × 13 × 4 mm — A/B drives, front idlers, XY joints. Twenty in the kit | [00.26](00-before-you-start.md#step-0026-fastener-names-part-2-and-the-spacer-substitution-p8) |
| **625-2RS** | Plain bearing, 5 × 16 × 5 mm — **Z drives only**. Same 5 mm bore as an F695, so sorting by bore does not work | [00.26](00-before-you-start.md#step-0026-fastener-names-part-2-and-the-spacer-substitution-p8) |
| **Ferrule** | A crimped metal sleeve on a stranded wire end so a **screw** terminal clamps a solid tube instead of loose strands. The kit ships VE0508 | [00a.8](00a-mains-safety.md#step-00a8-ferrules-and-the-no-whisker-rule) |
| **FHCS** | Flat Head Cap Screw — countersunk cone head, flat top. The titanium backers use them, and they cam out easily in a countersink | [00.25](00-before-you-start.md#step-0025-fastener-names-part-1-p7) |
| **Flex plate** | The removable spring-steel print surface that sits on the magnetic pad. Smooth/satin side for ASA on this build | [03.20](03-build-plate.md#step-0320-fit-the-flex-plate-then-cover-the-bed) |
| **Flip-and-pack** | LDO's rail-greasing method: carriage down, grease forced through a mounting hole until it oozes past the bearings. Needs the **back** of the rail, so it only works before installation | [00.19](00-before-you-start.md#step-0019-flip-and-pack) |

Source: [Ch 00 Steps 00.19](00-before-you-start.md#step-0019-flip-and-pack), [00.25](00-before-you-start.md#step-0025-fastener-names-part-1-p7), [00.26](00-before-you-start.md#step-0026-fastener-names-part-2-and-the-spacer-substitution-p8) · [Ch 00a Step 00a.8](00a-mains-safety.md#step-00a8-ferrules-and-the-no-whisker-rule)

---

## G

| Term | What it is | First matters at |
|---|---|---|
| **G28** | Klipper's home-all command. On this machine it needs a reachable `safe_z_home` position, which is deliberately left invalid until you measure it | [13.27](13-initial-startup.md#step-1327-full-g28) |
| **G32** | The Voron macro that homes, runs QGL and re-homes. Re-run it after every `SAVE_CONFIG`, which restarts Klipper and loses homing | [12.27](12-software.md#step-1227-350-mm-resonance-probe-point-and-the-g32-homing-end-position) |
| **Gantry** | The X extrusion, its two XY joints and the X carriage, carried on the two Y axes. Everything above the deck that moves in XY | [05 — Gantry](05-gantry.md) |
| **GFCI / RCD** | Residual-current device — cuts the supply when live and neutral currents differ, which is what happens when current leaves through a person | [00a.5](00a-mains-safety.md#step-00a5-put-the-printer-on-an-rcdgfci-outlet-you-can-reach) |

Source: [Ch 13 Step 13.27](13-initial-startup.md#step-1327-full-g28) · [Ch 12 Step 12.27](12-software.md#step-1227-350-mm-resonance-probe-point-and-the-g32-homing-end-position) · [Ch 00a Step 00a.5](00a-mains-safety.md#step-00a5-put-the-printer-on-an-rcdgfci-outlet-you-can-reach)

---

## H

| Term | What it is | First matters at |
|---|---|---|
| **Hammerhead nut** | A T-nut that drops in from the face of the slot rather than rolling in. Used **exclusively for panel mounting** in this build | [00.25](00-before-you-start.md#step-0025-fastener-names-part-1-p7) |
| **Heat-set insert** | A brass M3×5×4 sleeve melted into a printed boss to give it a real thread. 153 in the kit; a missed one can cost a gantry teardown | [00.13](00-before-you-start.md#step-0013-fit-the-brass-tip-and-set-the-tongue-flush) |
| **Heat soak** | Holding the machine at temperature until the **frame**, not just the bed, has expanded. Bed: minutes. Frame: 30–45 minutes | [13.31](13-initial-startup.md#step-1331-heat-soak-bed-100-c-hotend-150-c) |
| **HV stepper** | The Leviathan's high-voltage stepper ports (`Vin 24-48V` supply). The A and B motors live here; Z motors are on the standard ports | [10.25](10-wiring.md#step-1025-psu-leviathan-hv-stepper-supply) |

Source: [Ch 00 Steps 00.13](00-before-you-start.md#step-0013-fit-the-brass-tip-and-set-the-tongue-flush), [00.25](00-before-you-start.md#step-0025-fastener-names-part-1-p7) · [Ch 13 Step 13.31](13-initial-startup.md#step-1331-heat-soak-bed-100-c-hotend-150-c) · [Ch 10 Step 10.25](10-wiring.md#step-1025-psu-leviathan-hv-stepper-supply)

---

## I

| Term | What it is | First matters at |
|---|---|---|
| **IEC C13 / C14** | The kettle-lead connector pair — C14 is the male inlet on the machine, C13 the socket on the cord. Ch 10 keeps the cord in another room between rituals | [09.11](09-electronics-bay.md#step-0911-fit-the-combined-iec-inlet-module) |
| **Idler** | A toothed or plain pulley that redirects a belt without driving it. F695 stacks in the A/B path, 20T idlers at the XY joints, extendable idlers on Z | [04.7](04-ab-drives.md#step-047-a-idler-build-the-bearing-stack) |
| **Inductive probe** | The Omron sensor that detects the metal bed for QGL only. It never sets Z=0 — the nozzle probe does | [07.35](07-ab-belts.md#step-0735-fit-the-probe-and-its-retainer-bracket) |
| **Input shaper** | Klipper's anti-ringing filter, fitted to the machine's measured resonance. Saving it does **not** set `max_accel`; that is a separate, mandatory edit | [14.13](14-calibration.md#step-1413-run-shaper_calibrate) |

Source: [Ch 09 Step 09.11](09-electronics-bay.md#step-0911-fit-the-combined-iec-inlet-module) · [Ch 07 Step 07.35](07-ab-belts.md#step-0735-fit-the-probe-and-its-retainer-bracket) · [Ch 14 Steps 14.13](14-calibration.md#step-1413-run-shaper_calibrate), [14.15](14-calibration.md#step-1415-save-the-shaper-and-set-the-real-max_accel)

---

## J

| Term | What it is | First matters at |
|---|---|---|
| **JST-PH2.0** | 2.0 mm-pitch connector. On the Nitehawk-SB **V2** this is `PROBE`, `TH0`, `CT` and `XY ENDSTOP` — the Rev D guide's XH2.5 text is wrong for this board | [10.55](10-wiring.md#step-1055-connector-types-on-the-v2-toolboard) |
| **JST-XH2.5** | 2.5 mm-pitch connector — visibly coarser. On the V2 it is the `MOTOR` port. The pitch difference is how you identify a V2 board | [00.5](00-before-you-start.md#step-005-verify-you-actually-received-a-rev-d-nitehawk-sb-v2) |
| **JST-ZH1.5** | 1.5 mm-pitch, 5-pin — the V2's **secondary USB port**, the physical marker that the board is a V2 and the reason to leave umbilical slack | [00.5](00-before-you-start.md#step-005-verify-you-actually-received-a-rev-d-nitehawk-sb-v2) |

Source: [Ch 10 Step 10.55](10-wiring.md#step-1055-connector-types-on-the-v2-toolboard) · [Ch 00 Step 00.5](00-before-you-start.md#step-005-verify-you-actually-received-a-rev-d-nitehawk-sb-v2)

---

## K

| Term | What it is | First matters at |
|---|---|---|
| **Katapult** | The CAN/USB bootloader on both MCUs, letting you reflash without touching the boards. Building Klipper with the wrong bootloader **offset** erases it | [12.15](12-software.md#step-1215-flash-the-leviathan-through-katapult) |
| **KIAUH** | Klipper Installation And Update Helper — the script that installs Klipper, Moonraker, Mainsail and KlipperScreen on the Pi | [12.8](12-software.md#step-128-install-kiauh) |
| **Klicky** | A dockable microswitch probe. Its parts are printed and bagged on this build but **not fitted** — the kit's config, wiring and cable are for the inductive probe | [08.54](08-toolhead.md#step-0854-confirm-the-probe-decision-and-bag-the-klicky-set) |
| **Klipper** | The firmware: a host process on the Raspberry Pi plus thin firmware on each MCU. Configuration lives in `printer.cfg` on the Pi, not on the boards | [12 — Software](12-software.md) |
| **klippy.log** | Klipper's full log, at `~/printer_data/logs/klippy.log`. Attach it complete and unmodified to any question — a snippet is not useful | [15 — Where to ask](15-troubleshooting.md#not-covered-here-where-to-ask) |

Source: [Ch 12 Steps 12.8](12-software.md#step-128-install-kiauh), [12.15](12-software.md#step-1215-flash-the-leviathan-through-katapult) · [Ch 08 Step 08.54](08-toolhead.md#step-0854-confirm-the-probe-decision-and-bag-the-klicky-set) · [Klipper — Contact](https://www.klipper3d.org/Contact.html)

---

## L

| Term | What it is | First matters at |
|---|---|---|
| **LDO** | Motor Dynamics Lab — the kit vendor whose Build Notes, Wiring Guide, Printed Parts Guide and BOM overlay the official Voron manual everywhere they differ | [00.2](00-before-you-start.md#step-002-find-the-kit-serial-and-open-your-batch-bom-page) |
| **LDO Build Notes / Build FAQ** | LDO's page-indexed diff against the official manual — which pages to skip, which parts differ. The source of most `Rev D+ / LDO` callouts | [Build FAQ](https://docs.ldomotors.com/voron/voron2/build-faq) |
| **LDO Wiring Guide (Rev D)** | LDO's own electrical walkthrough, and the source of Checkpoint #1. Written for a V1 toolboard, so its `rp2040` and XH2.5 statements are wrong for a Rev D+ | [Wiring guide](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d) |
| **Leviathan** | LDO's mainboard, replacing the manual's BTT Octopus. Carries the Pi on standoffs and supplies its 5 V — there is **no 5 V PSU** in this kit | [09.24](09-electronics-bay.md#step-0924-clip-the-leviathan-and-pi-onto-the-front-rail) |
| **Live–dead–live** | Prove the meter on a known-live source, take the reading, prove the meter again. The defence against a dead meter reading "no voltage" | [00a.4](00a-mains-safety.md#step-00a4-test-the-meter-before-you-trust-it-and-again-after) |
| **Loctite 243** | Medium-strength threadlocker, used on every pulley set screw and the Z drive fasteners | [00.9](00-before-you-start.md#step-009-order-the-consumables-with-the-longest-lead-time-first) |

Source: [Ch 00 Step 00.2](00-before-you-start.md#step-002-find-the-kit-serial-and-open-your-batch-bom-page) · [Ch 09 Step 09.24](09-electronics-bay.md#step-0924-clip-the-leviathan-and-pi-onto-the-front-rail) · [LDO Build FAQ](https://docs.ldomotors.com/voron/voron2/build-faq) · [LDO wiring guide](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d)

---

## M

| Term | What it is | First matters at |
|---|---|---|
| **Mainsail** | The web interface for Klipper (with Moonraker as its API layer). Every g-code command in Ch 13–14 is typed in its Console tab | [12.5](12-software.md#step-125-reach-mainsail-and-open-an-ssh-session) |
| **`max_accel`** | The printer's acceleration ceiling. The LDO config ships a placeholder `10000`; input shaping tells you the real number and `SAVE_CONFIG` will not write it for you | [14.15](14-calibration.md#step-1415-save-the-shaper-and-set-the-real-max_accel) |
| **Meanwell LRS-200-24** | The 24 V 8.8 A PSU. Its **115/230 V selector** is set once in Ch 09 and re-checked at Checkpoint #1; getting it wrong destroys the unit on first switch-on | [09.14](09-electronics-bay.md#step-0914-set-the-psu-voltage-selector-to-115-v) |
| **MGN9 / MGN12** | Linear rail sizes. This build has one MGN12H (X) and six MGN9H (2 × Y, 4 × Z), all shipped dry and all greased in Ch 00 | [00.17](00-before-you-start.md#step-0017-unbag-the-rails-and-immobilise-every-carriage) |

Source: [Ch 12 Step 12.5](12-software.md#step-125-reach-mainsail-and-open-an-ssh-session) · [Ch 14 Step 14.15](14-calibration.md#step-1415-save-the-shaper-and-set-the-real-max_accel) · [Ch 09 Step 09.14](09-electronics-bay.md#step-0914-set-the-psu-voltage-selector-to-115-v) · [Ch 00 Step 00.17](00-before-you-start.md#step-0017-unbag-the-rails-and-immobilise-every-carriage)

---

## N

| Term | What it is | First matters at |
|---|---|---|
| **Nevermore** | A recirculating activated-carbon filter inside the chamber — the Micro V5 Duo here, on the Leviathan's FAN3, declared as `fan_generic` so a macro can run it | [11.26](11-skirts-panels-door.md#step-1126-break-out-the-nevermore-printed-supports) |
| **Nitehawk-SB V2** | The Rev D+ toolboard: STM32G0B1, integrated ADXL345, PH2.0 connectors, keyed fan-adapter header, secondary USB port. The "+" in Rev D+ | [00.5](00-before-you-start.md#step-005-verify-you-actually-received-a-rev-d-nitehawk-sb-v2) |
| **Nozzle probe** | LDO's mechanical Z endstop — a pin the nozzle presses. This, not the inductive probe, sets Z=0 | [08.56](08-toolhead.md#step-0856-assemble-the-ldo-nozzle-probe-z-endstop) |

Source: [Ch 11 Step 11.26](11-skirts-panels-door.md#step-1126-break-out-the-nevermore-printed-supports) · [Ch 00 Step 00.5](00-before-you-start.md#step-005-verify-you-actually-received-a-rev-d-nitehawk-sb-v2) · [Ch 08 Step 08.56](08-toolhead.md#step-0856-assemble-the-ldo-nozzle-probe-z-endstop)

---

## O

| Term | What it is | First matters at |
|---|---|---|
| **Omron G3NB-210B-1** | The solid-state relay switching mains to the bed heater: `1 / 2` = LOAD (24–220 VAC 10 A), `3 + / 4 −` = INPUT (5–24 VDC). LDO calls this connection *critical* | [09.17](09-electronics-bay.md#step-0917-fit-the-ssr-to-its-metal-din-bracket) |

Source: [Ch 09 Step 09.17](09-electronics-bay.md#step-0917-fit-the-ssr-to-its-metal-din-bracket) · [Ch 10 Step 10.10](10-wiring.md#step-1010-read-the-ssr-terminal-numbers-before-you-wire-it) · [Ch 00a Step 00a.7](00a-mains-safety.md#step-00a7-the-ssr-is-marked-earth-the-mounting-rail-and-this-build-does-not)

---

## P

| Term | What it is | First matters at |
|---|---|---|
| **PE (protective earth)** | The green/yellow conductor that makes the machine safe to **touch**. Five branches here: supply, WAGO bus, PSU, frame, bed | [00a.6](00a-mains-safety.md#step-00a6-learn-the-protective-earth-chain-in-this-build) |
| **PEI sheet** | The coated spring-steel print surface. Smooth/satin for ASA on this build; a good first layer still shows individual lines, not a featureless gloss | [13.42](13-initial-startup.md#step-1342-print-it-and-set-the-first-layer-squish) |
| **PID tune** | Klipper's automatic heater-control calibration. Run **before** QGL, because a drifting probe gives a QGL that reports success and is wrong | [13.29](13-initial-startup.md#step-1329-pid-tune-the-bed-at-100-c) |
| **PIF (Print It Forward)** | The Voron programme that sells printed part sets. Explicitly **not** used on this build — every part is printed here | [00.23](00-before-you-start.md#step-0023-print-guidelines-p4) |
| **Precision spacer** | The brass M5 1 mm spacer the kit supplies wherever the manual says *M5 shim*. A controlled thickness, not a washer — 46 in the kit | [00.26](00-before-you-start.md#step-0026-fastener-names-part-2-and-the-spacer-substitution-p8) |
| **Pressure advance** | Klipper's compensation for filament pressure lag in the nozzle, tuned from a printed pattern. Shifts when input shaping is switched on, so it comes after | [14.17](14-calibration.md#step-1417-generate-and-print-the-ellis-pa-pattern) |
| **`PROBE_ACCURACY`** | Klipper's repeatability test for the probe. σ < 0.003 mm hot, with no trend, is the gate on QGL and everything downstream | [13.32](13-initial-startup.md#step-1332-probe_accuracy-hot-the-gate-on-everything-downstream) |
| **Pulley (16T / 20T / 80T)** | GT2 toothed pulleys. 16T on the Z motors, 20T everywhere else, 80T on the Z drive shafts — 16T and 20T look nearly identical and are not interchangeable | [00.26](00-before-you-start.md#step-0026-fastener-names-part-2-and-the-spacer-substitution-p8) |

Source: [Ch 00a Step 00a.6](00a-mains-safety.md#step-00a6-learn-the-protective-earth-chain-in-this-build) · [Ch 00 Steps 00.23](00-before-you-start.md#step-0023-print-guidelines-p4), [00.26](00-before-you-start.md#step-0026-fastener-names-part-2-and-the-spacer-substitution-p8) · [Ch 13 Steps 13.29](13-initial-startup.md#step-1329-pid-tune-the-bed-at-100-c), [13.32](13-initial-startup.md#step-1332-probe_accuracy-hot-the-gate-on-everything-downstream) · [Ch 14 Step 14.17](14-calibration.md#step-1417-generate-and-print-the-ellis-pa-pattern)

---

## Q

| Term | What it is | First matters at |
|---|---|---|
| **QGL (quad gantry level)** | The routine that probes four points and drives the four Z motors independently until the gantry is parallel to the bed. It levels in **Z only** — it cannot see racking | [13.33](13-initial-startup.md#step-1333-quad_gantry_level) |
| **`QUERY_ENDSTOPS` / `QUERY_PROBE`** | Klipper commands that report each switch's current state. The first thing to run when homing misbehaves | [13.17](13-initial-startup.md#step-1317-query_endstops-with-everything-released) |

Source: [Ch 13 Steps 13.17](13-initial-startup.md#step-1317-query_endstops-with-everything-released), [13.33](13-initial-startup.md#step-1333-quad_gantry_level) · [Ch 12 Step 12.26](12-software.md#step-1226-350-mm-quad_gantry_level)

---

## R

| Term | What it is | First matters at |
|---|---|---|
| **Racking** | The gantry's X extrusion sitting out of square to the Y axes — a parallelogram instead of a rectangle. QGL passes happily on a racked gantry and the parts print skewed | [05.44](05-gantry.md#step-0544-run-the-x-axis-end-to-end) |
| **Rev D+** | This kit: LDO Rev D **plus** the Nitehawk-SB V2. An electrical change plus exactly one STL (`usb_adapter_mount_partial_cover`) — LDO publishes no Rev D+ guide | [00.5](00-before-you-start.md#step-005-verify-you-actually-received-a-rev-d-nitehawk-sb-v2) |
| **Revo HF** | The E3D hotend in this kit — quick-change nozzle, screwed in by hand, which is why the strain relief has to be bent clear first | [08.27](08-toolhead.md#step-0827-assemble-the-revo-hf-hotend) |
| **Roll-in T-nut** | A nut that drops into an extrusion slot and rotates to lock, so it can be added after assembly. Used everywhere except panel mounting | [00.25](00-before-you-start.md#step-0025-fastener-names-part-1-p7) |
| **Rotation distance** | The millimetres of filament (or belt) per motor revolution. Checked by extruding a measured 100 mm — **not** the lever for an oversize printed part | [14.7](14-calibration.md#step-147-rotation-distance-check-100-mm-extrusion) |

Source: [Ch 05 Step 05.44](05-gantry.md#step-0544-run-the-x-axis-end-to-end) · [Ch 00 Steps 00.5](00-before-you-start.md#step-005-verify-you-actually-received-a-rev-d-nitehawk-sb-v2), [00.25](00-before-you-start.md#step-0025-fastener-names-part-1-p7) · [Ch 08 Step 08.27](08-toolhead.md#step-0827-assemble-the-revo-hf-hotend) · [Ch 14 Step 14.7](14-calibration.md#step-147-rotation-distance-check-100-mm-extrusion)

---

## S

| Term | What it is | First matters at |
|---|---|---|
| **`SAVE_CONFIG`** | Klipper's command to write calibrated values into an auto-generated block at the end of `printer.cfg`. It **restarts Klipper**, so homing is lost each time | [13.29](13-initial-startup.md#step-1329-pid-tune-the-bed-at-100-c) |
| **"Second hole in"** | LDO's rail rule that overrides the manual: never use a rail's **end** hole — use the second hole from each end, because the end holes are where later T-nuts must live | [00.22](00-before-you-start.md#step-0022-understand-the-rail-jigs-before-you-need-them) |
| **Set screw (grub screw)** | A headless screw that clamps a pulley to a shaft. One of the pair goes on the shaft's machined **flat**, and both get threadlocker | [00.26](00-before-you-start.md#step-0026-fastener-names-part-2-and-the-spacer-substitution-p8) |
| **SHCS** | Socket Head Cap Screw — straight cylindrical head. The most common fastener in the machine: 283 M3×8 alone | [00.25](00-before-you-start.md#step-0025-fastener-names-part-1-p7) |
| **Shim** | A thin DIN 988 spacer the official manual calls for at M5 locations. Your kit replaces every one with a brass precision spacer | [00.26](00-before-you-start.md#step-0026-fastener-names-part-2-and-the-spacer-substitution-p8) |
| **Skirt** | The ring of printed segments around the base that hides and closes the electronics bay, and carries the touchscreen and bay-fan modules | [11.1](11-skirts-panels-door.md#step-111-dry-fit-the-whole-skirt-ring) |
| **Snubber** | The RC network inside the SSR. It leaks a small current **even with no input**, which is why the SSR is only ever wired dead | [00a.7](00a-mains-safety.md#step-00a7-the-ssr-is-marked-earth-the-mounting-rail-and-this-build-does-not) |
| **Squish** | How hard the first layer is pressed into the sheet, set live during a print and committed with `Z_OFFSET_APPLY_ENDSTOP`. Moves again when extrusion multiplier changes | [13.42](13-initial-startup.md#step-1342-print-it-and-set-the-first-layer-squish) |
| **SSR (solid-state relay)** | A semiconductor switch with no moving contacts, used here to switch mains to the bed. One that reads short when unpowered is dead and the bed would be permanently live | [09.17](09-electronics-bay.md#step-0917-fit-the-ssr-to-its-metal-din-bracket) |
| **Stealthburner** | The Voron toolhead body — printhead halves, fan ducts, LED logo, and the accent-coloured main body from batch B02 | [08.62](08-toolhead.md#step-0862-fit-the-stealthburner-body-and-mate-the-board-to-board-header) |
| **`STEPPER_BUZZ`** | Klipper's per-motor test: 1 mm forward and back. Proves the right motor is on the right port and turning the right way, before anything homes | [13.13](13-initial-startup.md#step-1313-stepper_buzz-the-four-z-motors) |

Source: [Ch 00 Steps 00.22](00-before-you-start.md#step-0022-understand-the-rail-jigs-before-you-need-them), [00.25](00-before-you-start.md#step-0025-fastener-names-part-1-p7), [00.26](00-before-you-start.md#step-0026-fastener-names-part-2-and-the-spacer-substitution-p8) · [Ch 08 Step 08.62](08-toolhead.md#step-0862-fit-the-stealthburner-body-and-mate-the-board-to-board-header) · [Ch 13 Steps 13.13](13-initial-startup.md#step-1313-stepper_buzz-the-four-z-motors), [13.42](13-initial-startup.md#step-1342-print-it-and-set-the-first-layer-squish)

---

## T

| Term | What it is | First matters at |
|---|---|---|
| **Thermal fuse** | The 125 °C one-shot cut-out already bonded to the bed heater pad. Verify it, photograph it, never try to re-seat it | [03.5](03-build-plate.md#step-035-verify-the-thermal-fuse-do-not-fit-one) |
| **Thumb nut** | The knurled nut used as a **bed spacer** under the build plate, letting it float and expand | [03.13](03-build-plate.md#step-0313-fit-the-four-thumb-nuts-as-spacers) |
| **Toolboard** | The PCB on the toolhead that drives the hotend, fans, LEDs, probe and accelerometer over one umbilical. Here: Nitehawk-SB V2, over USB | [00.5](00-before-you-start.md#step-005-verify-you-actually-received-a-rev-d-nitehawk-sb-v2) |
| **"Snug, not torqued"** | This manual's instruction to close a joint without setting it, so a later squaring pass can still move it. No Voron or LDO source publishes a torque figure for any fastener in this build | [00.8](00-before-you-start.md#step-008-settle-the-tool-list-owned-vs-buy) |

Source: [Ch 03 Steps 03.5](03-build-plate.md#step-035-verify-the-thermal-fuse-do-not-fit-one), [03.13](03-build-plate.md#step-0313-fit-the-four-thumb-nuts-as-spacers) · [Ch 00 Steps 00.5](00-before-you-start.md#step-005-verify-you-actually-received-a-rev-d-nitehawk-sb-v2), [00.8](00-before-you-start.md#step-008-settle-the-tool-list-owned-vs-buy)

---

## U

| Term | What it is | First matters at |
|---|---|---|
| **Umbilical** | The single bundled cable from the electronics bay to the toolhead, carrying 24 V and USB. Never plug or unplug it with the power on | [10.54](10-wiring.md#step-1054-identify-your-umbilical-and-its-two-connectors) |
| **USB adapter PCB** | The bay-side end of the umbilical, on its own DIN clip. Its **partial** cover is the one Rev D+ STL change, and it exists to expose a grounding point | [09.25](09-electronics-bay.md#step-0925-confirm-the-usb-adapter-stack-and-clip-it) |

Source: [Ch 10 Step 10.54](10-wiring.md#step-1054-identify-your-umbilical-and-its-two-connectors) · [Ch 09 Step 09.25](09-electronics-bay.md#step-0925-confirm-the-usb-adapter-stack-and-clip-it) · [Ch 10 Step 10.57](10-wiring.md#step-1057-the-usb-adapter-cover-is-the-partial-cover)

---

## V

| Term | What it is | First matters at |
|---|---|---|
| **VE0508** | The ferrule size the kit supplies for its mains screw terminals — 0.5 mm², 8 mm barrel | [00a.8](00a-mains-safety.md#step-00a8-ferrules-and-the-no-whisker-rule) |
| **VFA (vertical fine artifacts)** | Fine periodic vertical ripple, 0.5–2 mm apart, from belt-tooth engagement. Cosmetic only, and **not** the same thing as ringing | [print/00-slicer-setup — Gen 2 pause rule](print/00-slicer-setup.md#gen-2-belt-upgrade-pause-rule) |
| **Voron 2.4r2 Assembly Manual** | The official PDF this manual transcribes, unchanged since 2023-07-18. Cited throughout as `p.NN` | [00.29](00-before-you-start.md#step-0029-how-to-read-an-exploded-view-and-the-page-number-contract-p11) |
| **Voron Stealthburner manual** | The separate official PDF for the toolhead, referenced by page through Ch 08 | [08 — Toolhead](08-toolhead.md) |

Source: [Ch 00a Step 00a.8](00a-mains-safety.md#step-00a8-ferrules-and-the-no-whisker-rule) · [print/00-slicer-setup.md](print/00-slicer-setup.md#gen-2-belt-upgrade-pause-rule) · [Ch 00 Step 00.29](00-before-you-start.md#step-0029-how-to-read-an-exploded-view-and-the-page-number-contract-p11)

---

## W

| Term | What it is | First matters at |
|---|---|---|
| **WAGO 221** | Lever-clamp connector blocks. Three 5-way ones form the mains N / L / PE bus; two 2-way ones break out the bed's L and N | [10.7](10-wiring.md#step-107-populate-and-label-the-wago-bus) |
| **Washer (DIN 125)** | A plain flat washer. In this build it appears at M3 locations only — every M5 "washer" in the official manual is really the brass precision spacer | [00.26](00-before-you-start.md#step-0026-fastener-names-part-2-and-the-spacer-substitution-p8) |
| **Wire duct** | The slotted PVC channel the below-deck runs sit inside. Mains never crosses open deck, and the covers stay **off** until Checkpoint #1 has passed | [09.6](09-electronics-bay.md#step-096-cut-and-stick-the-five-wire-ducts) |

Source: [Ch 10 Steps 10.7](10-wiring.md#step-107-populate-and-label-the-wago-bus), [10.71](10-wiring.md#step-1071-leave-the-duct-covers-off) · [Ch 00 Step 00.26](00-before-you-start.md#step-0026-fastener-names-part-2-and-the-spacer-substitution-p8) · [Ch 09 Step 09.6](09-electronics-bay.md#step-096-cut-and-stick-the-five-wire-ducts)

---

## X

| Term | What it is | First matters at |
|---|---|---|
| **X carriage** | The printed halves that clamp the MGN12 carriage, capture both belt ends, and carry the toolhead. The `V2TR` file is the correct one — it is shared with the Trident | [05.45](05-gantry.md#step-0545-stage-the-x-carriage-frame-halves) |
| **XY endstop pod** | The small PCB carrying the X and Y switches, mounted on the gantry. Some LDO batches ship its cable mislabelled *X Stop / Y Stop* and it needs re-pinning | [10.31](10-wiring.md#step-1031-read-the-xy-endstop-cable-labels) |
| **XY joint** | The printed block at each end of the X extrusion that ties it to a Y carriage and turns both belts. Left deliberately loose until the gantry is squared | [05.25](05-gantry.md#step-0525-seat-the-m5-nuts-in-both-xy-joints) |

Source: [Ch 05 Steps 05.25](05-gantry.md#step-0525-seat-the-m5-nuts-in-both-xy-joints), [05.45](05-gantry.md#step-0545-stage-the-x-carriage-frame-halves) · [Ch 10 Step 10.31](10-wiring.md#step-1031-read-the-xy-endstop-cable-labels)

---

## Z

| Term | What it is | First matters at |
|---|---|---|
| **Z=0 / `Z_ENDSTOP_CALIBRATE`** | Setting the nozzle-to-bed zero with the paper test, done **hot**, with an extra `TESTZ Z=-0.1` because Klipper's test assumes a cold machine | [13.36](13-initial-startup.md#step-1336-z_endstop_calibrate-and-the-paper-test) |
| **Z joint** | The printed block joining each corner of the gantry to a Z carriage. Kept light through squaring and tightened **hot**, at the end | [06.14](06-z-axis-and-gantry-squaring.md#step-0614-bolt-the-first-z-joint-together) |
| **`Z_OFFSET_APPLY_ENDSTOP`** | The command that commits a live babystepping adjustment. Without it — followed by `SAVE_CONFIG` — the slider is discarded on restart | [13.42](13-initial-startup.md#step-1342-print-it-and-set-the-first-layer-squish) |
| **Z0–Z3** | The four Z drive positions: Z0 front-left, Z1 rear-left, Z2 rear-right, Z3 front-right, mapped to `STEPPER-0` … `-3`. QGL fails loudly if this map is wrong | [02.2](02-z-drives.md#step-0202-learn-the-four-z-positions-before-you-build-anything) |

Source: [Ch 13 Steps 13.36](13-initial-startup.md#step-1336-z_endstop_calibrate-and-the-paper-test), [13.42](13-initial-startup.md#step-1342-print-it-and-set-the-first-layer-squish) · [Ch 06 Step 06.14](06-z-axis-and-gantry-squaring.md#step-0614-bolt-the-first-z-joint-together) · [Ch 02 Step 02.02](02-z-drives.md#step-0202-learn-the-four-z-positions-before-you-build-anything)

---

## Next

Back to [**Ch 15 — Troubleshooting index**](15-troubleshooting.md) if you arrived here from a symptom, or to the [**timeline in 00-index.md**](00-index.md#the-timeline) if you are planning the next session.
