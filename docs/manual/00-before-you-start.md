# Chapter 00 — Before you start

Inventories the kit against its own batch BOM, settles the tools and consumables, verifies the flat reference, teaches heat-set inserts, and cleans and greases all seven rails — so that Ch 01 can start the moment the frame extrusions come out of the box and no later chapter stops for a missing tool.

**What you're building in this chapter:** nothing yet — this chapter builds the conditions for everything else. Four things come out of it. **A counted kit**: every box checked against your own batch's bill of materials, so a shortage is a Fabreeko email today rather than a stalled evening in six weeks. **A working bench**: the tools bought, the consumables ordered, and a flat reference surface verified with a straightedge and feeler gauges, because the frame's squareness in Ch 01 can be no better than the surface it is built on. **A heat-set technique**: the brass tip fitted to the soldering iron and an iron temperature found on a scrap coupon, ready for the ~150 brass inserts that give printed parts their metal threads. **Seven prepared linear rails** — the hardened steel bars and ball-bearing carriages that carry the toolhead, the gantry and the gantry's four corners — degreased of their shipping oil, packed with grease, wiped and labelled. Rails can only be greased before they are bolted down, which is why they are done here and not in the chapters that use them.

**Time:** 2.5–4.0 h hands-on, first build (survey §5.1 P00). Rail prep is roughly half of it.

**Sessions:** 7 × ~30 min — the `Pause:` lines below break the chapter into 7 segments; every minute figure is a first-build estimate.

**Prerequisites:**

- **Print batch B00 — Calibration & jigs** (`print/B00-calibration-and-jigs.md`). B00 is printable the day the Core One+ runs, months before the Voron kit lands. Its seven-item gate must pass before B01 starts; this chapter only needs the `Heatset_Practice` coupon and the two rail guides off that plate.
- The kit itself, unopened. Fabreeko order **F6424626**, pre-order, ETA mid/late September 2026.
- Nothing else. This chapter has no assembly prerequisites — it is the first thing you do.

**Tools**

- Digital caliper, 150 mm
- Machinist square, 150 mm, DIN 875/2 or better
- Flat reference surface (the kitchen stone counter, verified in Step 00.10)
- Steel rule / straightedge ≥ 600 mm
- Feeler gauge set
- Temperature-controlled soldering iron that accepts **900M-T** tips (Hakko FX888D-style sleeve with a thumb ring) — the LDO brass insert tip in the kit will not fit anything else. [src](https://docs.ldomotors.com/guides/heatset_insert_tool_guide)
- LDO brass M3 heat-set tip (supplied in the kit)
- Hex drivers 1.5 / 2 / 2.5 / 3 / 4 mm — kit wrenches or the Fabreeko precision set
- Flush cutters
- 10 ml syringe with a blunt tip (grease delivery), or use the grease tube nozzle
- 2 mm drill bit (supplied), 2.5 mm slot screwdriver (supplied)
- Phone or camera on a tripod, for the build log

**Consumables:** IPA ≥ 90% (enough to soak a 400 mm rail — a shallow tray or a length of 40 mm pipe capped at one end works); Super Lube 21030 synthetic grease; nitrile gloves; lint-free cloth; masking tape; permanent marker; a shallow tray for the IPA soak.

**Printed parts** — batch **B00**, all Galaxy Black ASA on the Core One+

| Looks like | STL | Repo path | Qty | Colour |
|---|---|---|---:|---|
| ![](assets/parts/Voron_Design_Cube_v7.png){ width=96 } | `Voron_Design_Cube_v7.stl` | Voron-2 `STLs/Test_Prints/` | 1 | Black |
| ![](assets/parts/Heatset_Practice.png){ width=96 } | `Heatset_Practice.stl` | Voron-2 `STLs/Test_Prints/` | 1 | Black |
| ![](assets/parts/MGN12_rail_guide_x2.png){ width=96 } | `MGN12_rail_guide_x2.stl` | Voron-2 `STLs/Tools/` | 2 | Black |
| ![](assets/parts/MGN9_rail_guide_x2.png){ width=96 } | `MGN9_rail_guide_x2.stl` | Voron-2 `STLs/Tools/` | 2 | Black |
| ![](assets/parts/pulley_jig.png){ width=96 } | `pulley_jig.stl` | Voron-2 `STLs/Tools/` | 1 | Black |
| ![](assets/parts/z_drive_retainer_a_x2.png){ width=96 } | `z_drive_retainer_a_x2.stl` | Voron-2 `STLs/Z_Drive/` | 1 | Black |

`z_drive_retainer_a` is on the jig plate as the bearing press-fit coupon, and it is a real part you will fit in Ch 02 — nothing is wasted.

**Hardware** (chapter totals)

| Fastener / part | Qty | Note |
|---|---|---|
| Heat-set insert, brass, M3×5×4 | 3 | practice coupon only, from the 153 supplied — 150 remain for the build |
| — no other kit hardware is consumed in this chapter — | 0 | every rail, fastener and PCB goes back in its bag |

**Read first**

- **The rails ship dry and must be cleaned and packed before they go on an extrusion.** The flip-and-pack method needs access to the *back* of the rail. Once a rail is bolted to a 2020 you cannot do this (survey §5.2 W9). [src](https://docs.ldomotors.com/guides/rail_grease_guide)
- **A rail carriage will slide off its rail and spill its bearing balls, and dropping one ruins it.** Tape every carriage in place the moment you unbag a rail (manual p.24, p.26).
- **Heat-set inserts go in per print batch, before the part enters any assembly.** One missed insert in an XY joint costs a gantry teardown (survey §5.2 W3).
- **Caliper the deck panel during inventory.** LDO's guides say 4 mm, LDO's own BOM says 3 mm. This decides which `deck_support_*` you print, and it is a Ch 02 step, not a Ch 11 one (survey §4.3).
- **Post the two Discord questions on day one** (Step 00.32). Both have multi-day answer latency and both gate work in Ch 08–Ch 10.

**Sources for this chapter:**

- [LDO batch BOM index](https://docs.ldomotors.com/en/voron/voron2/350_BOM/HOME) — find your batch tile from the kit serial
- [LDO 350 Rev D BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D) — the inventory checklist and every count in this chapter
- [LDO printed parts guide (Rev D)](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d) — which parts LDO supplies printed
- [LDO Nitehawk-SB V2 board doc](https://docs.ldomotors.com/en/Toolboard/nitehawk-sb-v2) — the Rev D+ toolboard identification markers
- [LDO XY endstop cable guide](https://docs.ldomotors.com/en/guides/XY_Endstop_Cable_Reconnecting_Guide) — the mislabelled XY endstop cable batch
- [LDO rail grease guide](https://docs.ldomotors.com/guides/rail_grease_guide) — degrease, flip-and-pack, wipe
- [LDO heat-set insert tool guide](https://docs.ldomotors.com/guides/heatset_insert_tool_guide) — tongue adjustment, temperature technique, the 90 %/10 % trick
- [LDO Klipper config `leviathan-printer-rev-d-sbv2.cfg`](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/667521d/Firmware/leviathan-printer-rev-d-sbv2.cfg) — the `stm32g0b1xx` serial-ID check written into Ch 12
- [Voron 2.4r2 assembly manual (pinned `de7e89d`)](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf) pages 4–11, 24–26, 31 — print spec, filenames, fastener names, drivers, blind joints, exploded-view conventions, rail handling, inserts
- [Voron-2 `STLs/Tools`](https://github.com/VoronDesign/Voron-2/tree/de7e89d/STLs/Tools) and [Voron-2 `STLs/Test_Prints`](https://github.com/VoronDesign/Voron-2/tree/de7e89d/STLs/Test_Prints) — the B00 jigs and the practice coupon
- [survey](../voron-build-instructions-survey.md) §4.1, §4.3, §5.2, §7.4, §7.5 · [print plan](../voron-print-plan.md) §1.2, §1.4
- Mirrored images in this chapter are LDO Motors' (the heat-set and rail-grease guides on docs.ldomotors.com, and the Nitehawk-SB-V2 repo), used with attribution; see `assets/remote/00-before-you-start/SOURCES.txt`. Every step keeps the original URL on its `Source:` line.

---

## Unboxing and inventory

### Step 00.1 — Open the cartons without cutting into them

*(no image — see text)*

**What you're looking at:** Two shipping cartons and a blade. Carton 1 is the mechanical and electrical kit — extrusions, motors, rails, fasteners, boards. Carton 2 is the flat, fragile half: eight acrylic and polycarbonate panels and the 355 × 355 × 10 mm cast aluminium build plate that becomes the printer's heated bed.

**Parts:** the shipping cartons, 2.

**Do:** Photograph all six faces of each carton before you open it — that is your damage evidence if anything inside is bent. Score only the tape, blade set shallow: carton 2 holds the acrylic and polycarbonate panels and the 355×355×10 mm build plate right under the flaps. Lift the build plate out flat, never on edge, so its weight cannot land on one corner and dent the ground face. Leave everything else in its box for now.

**Check:** No crushed corners, no rattle from carton 2, no oil weeping through carton 1. Every panel still has its protective film on both faces — leave it on until Ch 11.

Source: [LDO 350 Rev D BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D) · [survey](../voron-build-instructions-survey.md)

---

### Step 00.2 — Find the kit serial and open your batch BOM page

*(no image — see text)*

**What you're looking at:** The printed label on carton 1. Its serial is the only thing that ties your kit to the right **batch BOM** — LDO's per-batch bill of materials, the inventory checklist you tick in the next two steps ([glossary](16-glossary.md#b)). Quantities and part substitutions change between batches, so the generic page is not a stand-in for yours.

**Parts:** the label on carton 1.

**Do:** Find the serial. It is formatted `V2-YYMMDD####` — for example `V2-2606164523`: `2606` is the production batch (June 2026), then the pack date, then the four-digit kit number. Open [350_BOM/HOME](https://docs.ldomotors.com/en/voron/voron2/350_BOM/HOME), find the batch tile whose `Kit#:` range contains your serial, and open it. That page — not the generic one — is your inventory checklist; it has `Carton`, `Box`, `Item`, `Qty.`, `Check1` and `Check2` columns built for exactly this job. Print it or open it on the iPad.

**Check:** The page you land on is headed *V2.4 350 BOM (Rev. D)*. Every Rev D batch tile from 2406 onward currently resolves to the same [Rev_D page](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D) — that is expected, not an error.

⚠ **Rev D+ / LDO:** the index tops out at batch **2606**. A September/October 2026 kit will be a batch LDO has not listed yet. If your serial is not in any tile, use the Rev_D page above and ask Fabreeko for your batch sheet — do not assume quantities from an older batch. [src](https://docs.ldomotors.com/en/voron/voron2/350_BOM/HOME)

Source: [LDO batch BOM index](https://docs.ldomotors.com/en/voron/voron2/350_BOM/HOME) · [LDO 350 Rev D BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)

---

### Step 00.3 — Inventory carton 1, box by box

*(no image — see text)*

**What you're looking at:** Nine labelled boxes plus loose items — the whole mechanical and electrical half of the printer. The bags you are counting hold the fasteners the rest of the build spends: **SHCS** and **BHCS** screws, **roll-in T-nuts** that drop into an extrusion's slot and rotate to lock, and 153 brass **heat-set inserts** that give printed parts a real metal thread ([glossary](16-glossary.md#s)). The motors and extrusions in here are the frame and the four Z drives.

**Parts:** carton 1 — boxes *Cable Kit 2.4-350*, *Motion*, *Electronics 1*, *Electronics 2*, *Fasteners, Tools & Misc*, *Belts, Chains & Fans*, *Linear Rail Kit*, *Frame Kit 2.4-350*, *Motor Kit*, plus loose *Other* items (C13 cord, PVC wire duct ×5, Revo HF hotend, DIN rails ×2, Leviathan mainboard, Meanwell LRS-200-24 PSU, extrusion slot cover ×9).

**Do:** Work one box at a time against the BOM and tick `Check1`. Do not pour the fastener bags out — count the bag, tick it, close it. The counts that matter most because they are large and easy to be short on: **M3×8 SHCS ×283**, **M3 roll-in T-nut ×135**, **M5 roll-in T-nut ×80**, **M3 hammerhead ×75**, **M5 precision spacer ×46**, **heat-set insert M3×5×4 ×153**, zip ties ×100. Photograph each bag before it goes back in the box.

**Check:** Every BOM line ticked, or written down as short. Frame kit is 18 extrusions: 340E ×1, 430D ×1, 450C ×2, 470A ×10, 530B ×4. Motor kit is 7 motors: 1× 36STH20 (E), 2× 42STH48-2004MAH (A/B, 0.9°), 4× 42STH48-2004AC (Z, 1.8°). [src](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)

⚠ **Rev D+ / LDO:** in the *Cable Kit* box, read the labels on the XY endstop cable now. LDO documents a batch where they read **"X Stop / Y Stop"** instead of **"XES / YES"** and need re-pinning before they will work. Finding this in Ch 10 with the bay half-closed is much worse than finding it now. [src](https://docs.ldomotors.com/en/guides/XY_Endstop_Cable_Reconnecting_Guide)

Source: [LDO 350 Rev D BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D) · [LDO XY endstop cable guide](https://docs.ldomotors.com/en/guides/XY_Endstop_Cable_Reconnecting_Guide)

---

### Step 00.4 — Inventory carton 2 and caliper the deck panel

*(no image — see text)*

**What you're looking at:** The eight flat panels and the plate. The **deck panel** is the acrylic floor of the chamber — it sits on the bed extrusions and separates the printer's electronics bay underneath from the print chamber above ([glossary](16-glossary.md#d)). Its thickness decides which printed support clip you fit in Ch 02, which is why it is the one panel you unwrap far enough to caliper.

**Parts:** deck panel (acrylic, black, 469×469), back panel (acrylic, black, 483×503), bottom panel (acrylic, black, 469×469), door panels (PC clear, 241×503) ×2, side panels (PC clear, 483×503) ×2, top panel (PC clear, 483×483), magnetic pad, spring steel flex plate, build plate.

**Do:** Count the panels against the BOM. Peel back one corner of the **deck** panel's film only, and caliper the panel thickness at three points along one edge. Write the number on the masking-tape label you stick to the film. Re-cover it — the film is the panel's scratch protection until it goes in at Ch 02. Leave every other panel fully filmed.

**Check:** Eight panels present, no cracks, no chips at the corners. You now have one number written down: the deck thickness.

⚠ **Rev D+ / LDO:** LDO's Build Notes (p.29–30) and Printed Parts Guide both say the deck is **4 mm** → print `deck_support_4mm_x8`. LDO's own Rev D BOM lists the deck panel as **3 mm**. Your caliper reading resolves it. Print whichever support matches; both sets together are 16 small parts and minutes of print time, so if you are unsure, print both and fit the one that works. Do not resolve this from the documents. [src](https://docs.ldomotors.com/voron/voron2/build-faq) · survey §4.3

Source: [LDO 350 Rev D BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D) · [LDO Build Notes (Rev D)](https://docs.ldomotors.com/voron/voron2/build-faq) · [LDO printed parts guide (Rev D)](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d)

---

### Step 00.5 — Verify you actually received a Rev D+ (Nitehawk-SB V2)

![LDO Nitehawk-SB V2 — board and connector pinout](assets/remote/00-before-you-start/nhsbv2_pcb_pinout.jpg)

**What you're looking at:** The Nitehawk-SB V2 **toolboard** — the small PCB that rides on the toolhead and drives the hotend, its fans, the LEDs, the probe and the accelerometer over a single cable, so the moving printhead needs one umbilical instead of a dozen wires ([glossary](16-glossary.md#t)). The "+" in Rev D+ *is* this board; the four physical markers below are how you prove you got it, and LDO's own pinout drawing labels three of them — `PROBE` and `XY ENDSTOP` as JST-PH2.0, the `E Motor` port as the coarser JST-XH2.5, and the five-pin JST-ZH1.5 **USB expansion port**. The silkscreen in the drawing reads *LDO NiteHawk-SB V2.0.0*; read yours.

**Parts:** *Electronics 2* box — Nitehawk SB toolhead PCB ×1, Stealthburner fan adapter ×1, USB adapter PCB ×1.

**Do:** Handle the board by its edges on an antistatic bag. Check four physical markers against the V2 board doc: (1) the **PROBE**, **TH0**, **CT** and **Endstop** connectors are JST-**PH 2.0 mm** pitch, visibly finer than the JST-XH 2.5 mm **MOTOR** connector next to them — the pitch difference is the tell; (2) a **secondary USB port** (JST-ZH 1.5 mm, 5-pin, labelled as the USB expansion port) is present; (3) the board-to-board header that mates with the fan adapter is **keyed**; (4) the MCU is marked STM32G0B1, not RP2040. Photograph both faces now — no published guide has these photos.

**Check:** All four markers present → Rev D+, Nitehawk-SB V2. Any one absent → you have a V1 board and a different config, wiring and connector set: stop and ask Fabreeko before you go further. [src](https://docs.ldomotors.com/en/Toolboard/nitehawk-sb-v2)

⚠ **Rev D+ / LDO:** the definitive confirmation is the USB serial ID, and you cannot read it until the Pi is up in Ch 12. There it must contain **`stm32g0b1xx`** (`usb-Klipper_stm32g0b1xx_…`). LDO's Rev D wiring guide says to expect `usb-Klipper_rp2040_…` — that sentence is wrong for this kit. If it reads `rp2040` you have a V1 board and must load `leviathan-printer-rev-d.cfg` instead of `leviathan-printer-rev-d-sbv2.cfg`. Loading the wrong one mis-drives the heater, thermistor, probe, both fans and the accelerometer at once. Write the check into your Ch 12 notes now. [src](https://github.com/MotorDynamicsLab/LDOVoron2/blob/main/Firmware/leviathan-printer-rev-d-sbv2.cfg) · survey §4.1 ①②

Source: [LDO Nitehawk-SB V2 board doc](https://docs.ldomotors.com/en/Toolboard/nitehawk-sb-v2) · [image: Nitehawk-SB-V2 `Images/nhsbv2_pcb_pinout.jpg`](https://raw.githubusercontent.com/MotorDynamicsLab/Nitehawk-SB-V2/42ae497/Images/nhsbv2_pcb_pinout.jpg) · [LDO Klipper config `leviathan-printer-rev-d-sbv2.cfg`](https://raw.githubusercontent.com/MotorDynamicsLab/LDOVoron2/667521d/Firmware/leviathan-printer-rev-d-sbv2.cfg)

---

### Step 00.6 — Set aside the ten LDO-supplied printed parts

*(no image — see text)*

**What you're looking at:** Ten small printed parts LDO makes for you, in one bag. They are the pieces the Voron STL set does not cover or you cannot reproduce — the two Leviathan mainboard brackets, DIN clips, the nozzle-probe body, the bed WAGO mount, and the Stealthburner LED diffuser, which has to be clear so the toolhead logo lights up.

**Parts:** the *LDO Printed Parts* bag — Leviathan Bracket Left ×1, Leviathan Bracket Right ×1, NH Adapter Mount ×1, DIN Clip ×4, CW2 Chain Anchor Tilted ×1, 2×3 Splitter Spacer ×2, LDO Nozzle Probe ×1, Bed WAGO Mount ×1, Stealthburner LED Diffuser ×1 (clear PETG), CW2 PCB Spacer ×1.

**Do:** Count them, photograph them together, and put them in their own labelled bin. These are the parts you must **not** print — the print plan already excludes them. The clear PETG LED diffuser in particular cannot be reproduced; you have no clear filament.

**Check:** Ten part types accounted for, in one bin, labelled "LDO SUPPLIED — DO NOT PRINT".

⚠ **Rev D+ / LDO:** the USB-adapter mount base is supplied printed, but the **cover** changed for the V2 board. The Rev D Printed Parts Guide points at the V1 `usb_adapter_mount.stl` cover; Rev D+ needs [`usb_adapter_mount_partial_cover.stl`](https://github.com/MotorDynamicsLab/Nitehawk-SB-V2/blob/master/STLs/usb_adapter_mount_partial_cover.stl) from the **V2** repo, whose whole purpose is to expose a mounting point as a grounding point. Batch **B07** currently lists the V1 file. Fix the B07 plate before you print it. [src](https://docs.ldomotors.com/en/Toolboard/nitehawk-sb-v2) · survey §4.1 ⑤

Source: [LDO printed parts guide (Rev D)](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d) · [LDO Nitehawk-SB V2 board doc](https://docs.ldomotors.com/en/Toolboard/nitehawk-sb-v2) · [Nitehawk-SB-V2 `STLs/`](https://github.com/MotorDynamicsLab/Nitehawk-SB-V2/tree/master/STLs)

Pause: ~40 min since the last pause — both cartons inventoried and repacked, every fastener bag closed, the deck thickness written on its film and the ten LDO-supplied parts in their own bin. Nothing is open to dust. Do not start unbagging rails before you have the grease and IPA on the bench.

---

## Tools

### Step 00.7 — Lay out what the kit already gives you

![LDO brass M3 heat-set tip — dimensioned drawing](assets/remote/00-before-you-start/heatset_dim.png)

**What you're looking at:** The kit's own tools. Five hex wrenches covering every fastener drive in the machine; a 2.5 mm slot driver; a 2 mm drill bit; a brass brush; and the brass **heat-set insert tip** — a threaded tip that screws into a soldering iron in place of its normal tip, with a thin tongue that carries heat into a brass insert so it melts its way into a printed boss ([glossary](16-glossary.md#h)). The drawing gives the tip's dimensions: the tongue is 2.4 mm across and 5.0 mm long, which is exactly one insert tall.

**Parts:** from *Fasteners, Tools & Misc* — hex wrenches 1.5 / 2 / 2.5 / 3 / 4 mm, 2.5 mm slot-head screwdriver, brass heat-set insert tool (M3), 2 mm drill bit, brass brush, aluminium handles ×2.

**Do:** Put these on the bench, not back in the box. The hex sizes supplied span every fastener drive in the BOM: M3 BHCS/FHCS take 2 mm, M3 SHCS 2.5 mm, M4 BHCS 2.5 mm, M5 BHCS 3 mm, M5 SHCS 4 mm, set screws 1.5–2 mm. Nothing in this kit needs a 5 mm hex.

**Check:** Five wrenches, one slot driver, one brass tip, one drill bit. The brass tip has two knurled adjustment nuts on it — that is the tongue adjuster you will use in Step 00.13.

Tip: `CLAUDE.md` lists "5 mm hex driver for M5 frame bolts" as an open purchase. It is not needed — the M5 BHCS the frame uses is a 3 mm drive.

Source: [LDO 350 Rev D BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D) · [LDO heat-set insert tool guide](https://docs.ldomotors.com/guides/heatset_insert_tool_guide)

---

### Step 00.8 — Settle the tool list: owned vs. buy

*(no image — see text)*

**What you're looking at:** No parts — a purchasing decision. The column that matters is *First needed*: it says which chapter stops dead without that tool, so anything marked Ch 00 or Ch 01 has to be on the bench before the kit lands.

**Parts:** none.

**Do:** Work down this table and buy what is missing. Column *First needed* is the chapter that stops without it.

| Tool | Status | First needed |
|---|---|---|
| Precision hex driver set of 5, ball-end | **Bought** — Fabreeko, in kit order F6424626 | Ch 01 |
| Hex wrenches 1.5–4 mm | **In the kit** | Ch 01 |
| Flat reference surface | **Resolved** — kitchen stone counter, verified in Step 00.10 | Ch 01 |
| Digital caliper, 150 mm | **Buy** | Ch 00 (deck gate, cube gate) |
| Machinist square, 150 mm DIN 875/2 | **Buy** | Ch 01 (frame squaring) |
| Temperature-controlled soldering iron, 900M-T tip fitting | **Buy** | Ch 00 (insert practice) |
| LDO brass M3 heat-set tip | **In the kit** — the $9.99 LDO Heat Insert Tool Kit only buys you spares | Ch 00 |
| Flush cutters | **Buy** | Ch 07 (belts), Ch 10 (zip ties) |
| Torque screwdriver 0.5–3 N·m | **Buy — optional.** No Voron or LDO source publishes a torque figure for any fastener in this build; this manual never invents one. Buy it for repeatability across the 283 M3×8, not to hit a spec | Ch 01 |
| T10 Torx driver | **Buy** | Ch 05 (titanium backer FHCS cam out easily in countersinks) |
| Multimeter | **Buy if not owned** | Ch 10 (mandatory — Checkpoint #1) |
| Dial indicator + magnetic base | Optional, skip for now | — |

**Check:** Every "Buy" row has an order placed or a decision to skip written down.

Source: [LDO 350 Rev D BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D) · [survey](../voron-build-instructions-survey.md)

---

### Step 00.9 — Order the consumables with the longest lead time first

*(no image — see text)*

**What you're looking at:** No parts — the consumables order. Two of these gate work rather than improve it: the synthetic grease and the IPA are what Step 00.18–00.19 consume, and the rails cannot be prepared without both.

**Parts:** none.

**Do:** Order now, before the kit lands: **Super Lube 21030** synthetic grease (3 oz / 85 g tube — far more than seven carriages need; LDO publishes no quantity), IPA ≥ 90% in a volume you can pour into a soak tray, **Loctite 243** blue threadlocker (Ch 02/04/05), nitrile gloves, lint-free cloth, masking tape, permanent marker. Add a 50-pack of spare **M3×5×4 brass heat-set inserts** if you want slack against the 153 supplied.

**Check:** Grease and IPA are on the bench before you touch a rail. Rail prep is the one job in this chapter that cannot start without them.

⚠ **Rev D+ / LDO:** LDO's rail guide recommends an **NLGI 0 or 1** grease and, in the same sentence, names Super Lube 21030 as a community favourite. Super Lube's own product data lists 21030 as **NLGI 2** — one grade stiffer than the stated preference. It is what the Voron community uses and it works; the tube arriving marked "NLGI 2" is not a wrong order. [src](https://docs.ldomotors.com/guides/rail_grease_guide) · [src](https://www.super-lube.com/product-sku/super-lube-multi-purpose-synthetic-grease-nlgi-2-sku-21030-3-oz-tube/)

Source: [LDO rail grease guide](https://docs.ldomotors.com/guides/rail_grease_guide) · [Super Lube 21030 product data](https://www.super-lube.com/product-sku/super-lube-multi-purpose-synthetic-grease-nlgi-2-sku-21030-3-oz-tube/)

---

## Workspace

### Step 00.10 — Verify the flat reference

*(no image — see text)*

**What you're looking at:** The kitchen stone counter, a long straightedge and a set of feeler gauges. This surface is the reference the whole frame is squared against in Ch 01, so its flatness becomes the printer's flatness; the feeler gauges measure the gap under the straightedge and tell you how flat it actually is.

**Parts:** straightedge ≥ 600 mm, feeler gauge set, marker or tape.

**Do:** Clear and clean the stone counter. You need a clear patch of at least **600 × 600 mm** — the 350's frame uses 470 mm and 530 mm extrusions. Stand the straightedge on edge across the patch in five positions: left-to-right, front-to-back, both diagonals, and through the centre. At each position try to slide feeler leaves under the straightedge, starting from the thinnest, and record the largest leaf that goes under anywhere. Mask off the flattest sub-area with tape and use only that for Ch 01 — no published tolerance exists for this surface, and the real acceptance test comes in Ch 01, where the assembled frame must sit on all four points with no rock and both diagonals must match.

**Check:** The straightedge does not rock in any of the five positions, and the worst gap is written down.

Tip: between sessions, lay a clean towel or a sheet of foam over the masked area — grit trapped under an extrusion is the one thing that will make a flat surface lie to you.

Source: [Voron manual p.15](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=15) · [survey](../voron-build-instructions-survey.md)

---

### Step 00.11 — Bin the workspace by chapter

*(no image — see text)*

**What you're looking at:** Empty bins and a marker. Each bin belongs to one chapter; parts land in it as they arrive from the Prusa or out of a kit box, so an assembly session never starts with a hunt.

**Parts:** stackable bins or boxes, one per chapter, plus masking tape and marker.

**Do:** Label a bin per chapter and stage parts into it as they arrive, printed or from the kit, so an assembly session never opens with a hunt through boxes. This is the receiving end of the "label and bin" step at the close of every print batch — a batch is not finished until its parts are in the bin of the chapter that consumes them.

| Print batch | Bins it feeds |
|---|---|
| B00 — Calibration & jigs | Ch 00, Ch 02 |
| B01 — Z drive assemblies | Ch 02 |
| B02 — The orange day (all accent parts) | Ch 02, Ch 04, Ch 05, Ch 08, Ch 11 |
| B03 — A/B drive units + front idlers | Ch 04 |
| B04 — XY joints + X carriage | Ch 05 |
| B05 — Z joints + Z chain | Ch 06, Ch 07 |
| B06 — Toolhead | Ch 08 |
| B07 — Electronics bay + lighting | Ch 09, Ch 10 |
| B08 — Skirts and front modules | Ch 11 |
| B09 — Panels, filtration, spool | Ch 11 |
| B10 — Clicky-Clack door | Ch 11 |

**Check:** Fifteen chapter bins, plus the "LDO SUPPLIED — DO NOT PRINT" bin from Step 00.6, plus one bin for the greased rails from Step 00.21.

Source: [print plan](../voron-print-plan.md) · [survey](../voron-build-instructions-survey.md)

---

### Step 00.12 — Leave the fasteners in their bags

*(no image — see text)*

**What you're looking at:** The *Fasteners, Tools & Misc* box, unopened bags. Every bag is one size of screw or nut; mixing them is easy and un-mixing them is not, because M3×8, M3×12 and M3×16 differ only by a few millimetres of shank.

**Parts:** the *Fasteners, Tools & Misc* box.

**Do:** Do not decant 283 M3×8 SHCS into a compartment tray at the start of the build. M3×8, M3×12 and M3×16 are hard to tell apart by eye once mixed, and re-sorting them costs an hour. Keep each bag closed and labelled; decant into a small tray only the fasteners a single chapter calls for, and tip the remainder back into its bag at the end of the session.

**Check:** Every fastener bag still closed and legible. One small tray, empty, staged for Ch 01.

Source: [LDO 350 Rev D BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)

Pause: ~30 min since the last pause — the tool and consumable decisions are made, the flat reference is verified and masked off, and the bins are labelled. Leave the fastener bags closed; do not decant anything into a tray yet.

---

## Heat-set inserts

### Step 00.13 — Fit the brass tip and set the tongue flush

![LDO brass heat-set tip — the tool's components](assets/remote/00-before-you-start/heatsettoolcomponents.jpg)
![Tongue set flush with the far face of an insert](assets/remote/00-before-you-start/tongueflush.jpg)

**What you're looking at:** The LDO brass tip with its two knurled adjustment nuts, and the same tip set against an insert. The **tongue** is the thin protruding pin that goes inside the insert; the knurled nuts slide the tip in its holder to change how much tongue sticks out. Set correctly, the tongue heats the whole insert and stops flush with its far face instead of poking through into the plastic.

**Parts:** LDO brass M3 heat-set tip (from the kit), soldering iron, one M3×5×4 insert as the gauge.

**Do:** Unscrew the iron's sleeve, remove the stock tip, fit the LDO tip, re-fit the sleeve. Hold an insert alongside the tip and move the two knurled adjustment nuts until the **exposed tongue length equals the insert height** — the tongue should end flush with the far face of the insert. Too short and the heat does not transfer; too long and the tongue touches and melts the printed part.

**Check:** With an insert on the tongue, the tongue tip and the insert's far face are level.

Tip: the adjustment nuts on LDO's own tool are themselves brass inserts. [src](https://docs.ldomotors.com/guides/heatset_insert_tool_guide)

Source: [LDO heat-set insert tool guide](https://docs.ldomotors.com/guides/heatset_insert_tool_guide)

---

### Step 00.14 — Find the iron temperature on the practice coupon

![Voron manual p.31](assets/manual-pages/manual-p031.png)
![LDO — driving an insert into a printed boss](assets/remote/00-before-you-start/insertinstall.jpg)

**What you're looking at:** Manual p.31 shows the general insert operation; the LDO photo shows the tongue driving an insert into a boss. The `Heatset_Practice` coupon is a printed block of seven insert pockets whose only job is to let you find the iron temperature before you spend an insert on a structural part.

**Parts:** `Heatset_Practice` coupon ×1 (batch B00), M3×5×4 inserts ×3.

**Do:** LDO publishes no temperature. Set the iron so the plastic goes *very soft but not runny*: too low and you have to force the insert down, too high and the boss slumps. Start low and step up. Sit the narrow end of the insert in the hole by hand — every Voron boss is drawn for this — then bring the tongue down and push straight until the insert is flush. Do all three on the coupon, and let your daughter do them; this is the part of the build where practice is free.

**Check:** Iron does not linger in any hole longer than it takes to seat the insert. You have a working temperature written on tape stuck to the iron's base.

⚠ **Rev D+ / LDO:** ASA behaves differently from the PLA in most insert tutorials. Calibrate on this ASA coupon, not on a PLA scrap, or the number you find will be wrong for all 150 remaining inserts.

Source: [Voron manual p.31](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=31) · [LDO heat-set insert tool guide](https://docs.ldomotors.com/guides/heatset_insert_tool_guide)

---

### Step 00.15 — Learn what a good insert looks like

*(no image — see text)*

**What you're looking at:** The three inserts you just set, in the practice coupon. A good one is flush with the surface, square to it, and has not made the plastic boss around it swell — a swollen boss means the part grew and will not fit its neighbour.

**Parts:** the practice coupon from Step 00.14.

**Do:** Judge each of your three against the gate from the print plan: the insert sits **flush to at most 0.2 mm proud**, and the boss around it has not bulged by more than **0.2 mm** — measure the boss outside diameter with the caliper before and after if you are unsure. Check squareness by eye from two directions; a tilted insert will not accept its screw straight. If one is tilted, the iron can nudge it — briefly. Use the trick LDO recommends: push the insert 90% of the way in with the iron, then finish the last 10% by pressing with a flat cold tool, which leaves the top face flat and square.

**Check:** Three inserts, flush, square, no bulged boss. A bulged boss is a technique fault (too hot, or pushed too fast), never a slicer fault. [src](https://docs.ldomotors.com/guides/heatset_insert_tool_guide) · print plan §1.4

Source: [LDO heat-set insert tool guide](https://docs.ldomotors.com/guides/heatset_insert_tool_guide) · [print plan](../voron-print-plan.md)

---

### Step 00.16 — Plan the 153 inserts

*(no image — see text)*

**What you're looking at:** No parts — the insert budget. The manual draws every insert with the same blue *Heat Set Insert* pill and no count, so the totals below are the ones this manual could verify; the rest you count off your own printed parts, per batch, before those parts enter an assembly chapter.

**Parts:** none.

**Do:** LDO ships **153** M3×5×4 brass inserts; three are now gone on the coupon. The manual draws inserts in the exploded views with a single blue *Heat Set Insert* pill and no numeral, so a per-chapter total cannot be read off the pages — you count them off each printed part during the insert pass. Do that pass **per print batch, immediately after the batch comes off the plate and before any part enters an assembly chapter**.

| Insert pass belongs to | Manual page carrying the callout | Count |
|---|---|---|
| Ch 02 — Z drive mains, retainers, motor mounts | p.31 | **36** (7 × 4 retainers + 2 × 4 mains — verified against the STLs) |
| Ch 04 — A/B drive frames | p.64 | (verify on bench) |
| Ch 05 — X carriage and XY joints | p.129 | (verify on bench) |
| Ch 08 — Stealthburner and Clockwork 2 | Stealthburner manual | (verify on bench) |
| Ch 10 — power inlet, Z cable chain | p.156, p.201 | (verify on bench) |
| Ch 11 — skirt front cover, screen and fan modules, exhaust cover | p.211, p.212, p.213, p.250 | (verify on bench) |
| **Supplied in the kit** | LDO Rev D 350 BOM | **153** |

**Check:** The insert pass is written into your batch checklist as a gate, not as a reminder. A missed insert in an XY joint means taking the gantry apart (survey §5.2 W3).

⚠ **Rev D+ / LDO:** LDO does not state whether 153 includes spares. Treat every insert after the three practice ones as load-bearing.

Source: [Voron manual p.31](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=31) · [LDO 350 Rev D BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)

Pause: ~30 min since the last pause — the iron is set up with the brass tip, the working temperature is written on tape, and the three practice inserts are done. Unplug the iron and let it cool before you walk away; leave the remaining 150 inserts bagged.

---

## Rail preparation

### Step 00.17 — Unbag the rails and immobilise every carriage

![Voron manual p.26](assets/manual-pages/manual-p026.png)

**What you're looking at:** Manual p.26 shows the linear rails and their carriages. A **linear rail** is a hardened steel bar with ball-bearing grooves down each side; the **carriage** is the block that rides on it on recirculating balls and carries the moving part ([glossary](16-glossary.md#m)). The balls are what fall out and are lost if the carriage runs off the end — hence the tape.

**Parts:** 1× `LDO-SLR12H-400Z1` stainless MGN12H (X axis), 6× `LDO-SLR9H-400Z0` stainless MGN9H (2× Y, 4× Z).

**Do:** Open one rail at a time. Before anything else, tape each carriage to its rail with a strip of masking tape, or refit the plastic end stoppers if your rails shipped with them. The carriage is designed to slide freely, which includes sliding off the end and spilling its ball bearings. Never let a rail hang vertically with an untaped carriage, and never let one fall — a dent or nick anywhere on the raceway makes that rail misbehave for the life of the machine.

**Check:** Seven rails on the bench, seven carriages taped, none dropped. Rails laid flat, not stacked on each other.

Source: [Voron manual p.26](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=26) · [Voron manual p.24](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=24) · [LDO rail grease guide](https://docs.ldomotors.com/guides/rail_grease_guide)

---

### Step 00.18 — Degrease: IPA soak, then dry completely

![LDO — rails soaking in IPA](assets/remote/00-before-you-start/soaking_rails3.jpg)

**What you're looking at:** A rail standing in a tray of IPA. The rails ship coated in a shipping oil that stops corrosion in transit but is not a lubricant; the soak dissolves it out of the ball tracks so the grease you pack in next is not diluted by it.

**Parts:** all 7 rails; IPA ≥ 90%; tray.

**Do:** These ship with a shipping oil, not a lubricant, and it must come out before you pack grease in. Soak each rail in **IPA ≥ 90% for about 10 minutes**, working the carriage back and forth along the rail during the soak to flush debris out of the ball tracks. Then let every rail dry **completely** — the IPA must fully evaporate before grease goes in, or you will emulsify the two.

**Check:** No oil film left on the raceway; the carriage runs dry and slightly notchy (that is correct at this stage — it has no grease yet); no visible wet IPA anywhere. [src](https://docs.ldomotors.com/guides/rail_grease_guide)

Tip: the linked Nero 3D video is the reference demonstration of this whole procedure — manual p.24 QR, [voron.link/agu0nes](https://voron.link/agu0nes).

Source: [LDO rail grease guide](https://docs.ldomotors.com/guides/rail_grease_guide) · [Voron manual p.24](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=24) · [Nero 3D rail prep video](https://voron.link/agu0nes)

Pause: ~30 min since the last pause — all seven rails are soaked, carriages taped, and laid out flat to dry. This is a genuine wait state: the IPA must evaporate completely before grease goes in, so stopping here costs nothing. Do not start packing grease into a rail that is still damp.

---

### Step 00.19 — Flip and pack

![LDO — grease loaded into a syringe](assets/remote/00-before-you-start/grease_prep.jpg)
![LDO — packing the carriage through a rail mounting hole](assets/remote/00-before-you-start/grease_pack.jpg)

**What you're looking at:** Grease being prepared in a syringe, and grease being forced into a carriage through one of the rail's own mounting holes. This is LDO's **flip-and-pack** method: with the rail upside down the mounting hole lines up with the ball tracks, so the grease reaches the bearings without taking the carriage apart ([glossary](16-glossary.md#f)). It only works while the rail's back is accessible — i.e. before the rail is bolted to an extrusion.

**Parts:** dried rail; Super Lube 21030 in a syringe or its own nozzle.

**Do:** This is LDO's flip-and-pack method: it needs no disassembly of the rail, but it needs access to the back of the rail, so it can only be done **before installation**. Flip the rail over so the carriage faces **downwards**. Slide the carriage until it sits over one of the rail's mounting holes, then force grease through that hole into the carriage. Keep going until grease **oozes out past the bearings at the sides of the carriage** — that is the signal the inside of the carriage is full.

**Check:** Grease visible at both ends of the carriage. The carriage now runs smooth and silent along the rail with no notchiness.

Source: [LDO rail grease guide](https://docs.ldomotors.com/guides/rail_grease_guide)

---

### Step 00.20 — Clean the rail surface back to bare steel

*(no image — see text)*

**What you're looking at:** The greased rail and a cloth. Grease belongs inside the carriage; the polished outer faces of the rail are a running surface, and any film left there collects dust and hair and feeds it into the bearings.

**Parts:** greased rail; lint-free cloth.

**Do:** Stroke the carriage the full length of the rail several times to distribute grease inside it, then wipe every trace of grease off the **outside** of the rail. The rule is: grease belongs inside the carriage and nowhere else. Grease left on the raceway collects dust and hair and carries it straight into the bearings.

**Check:** The rail surface is visibly clean and dry; the carriage still slides smoothly and silently.

Source: [LDO rail grease guide](https://docs.ldomotors.com/guides/rail_grease_guide)

---

### Step 00.21 — Label and bag the seven rails by destination

*(no image — see text)*

**What you're looking at:** Seven finished rails, tape and a marker. They are not interchangeable in practice — one is the MGN12H that carries the toolhead on X, and the six MGN9H split into two gantry Y rails and four vertical Z rails — so labelling them now is what stops a mix-up in Ch 02 and Ch 05.

**Parts:** 7 greased rails; masking tape; marker; a bin.

**Do:** Label each rail on its tape: **X** for the single MGN12H, **Y1/Y2** for two MGN9H, **Z0/Z1/Z2/Z3** for the remaining four MGN9H. Re-check the carriage tape, then bag each rail individually and put them all in one bin. They do not come out again until Ch 02 (the four Z rails) and Ch 05 (X and Y).

**Check:** Seven labelled, bagged rails; carriage tape intact on all seven; bin stored flat and away from foot traffic.

Source: [LDO rail grease guide](https://docs.ldomotors.com/guides/rail_grease_guide) · [LDO 350 Rev D BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)

---

### Step 00.22 — Understand the rail jigs before you need them

![Voron manual p.25](assets/manual-pages/manual-p025.png)

**What you're looking at:** Manual p.25 draws the printed rail guides in green, the manual's colour for a jig rather than a machine part. A **rail guide** clips over the extrusion and the rail and holds the rail centred on the 20 mm face while you start the screws; the `pulley_jig` is a printed gauge that sets how far a pulley sits along a motor shaft. Neither ends up in the finished printer.

**Parts:** `MGN9_rail_guide_x2` ×2, `MGN12_rail_guide_x2` ×2, `pulley_jig` ×1 (all batch B00).

**Do:** The rail guides are the green clips drawn on manual p.25. They clip over the extrusion and the rail and hold the rail centred on the 2020 while you start the screws — without them, a 400 mm rail wanders and you find out after it is bolted down. Slide a guide onto the real MGN12 rail now as your dimensional check: it should go on with **light finger pressure**. Very tight means over-extrusion; loose means under-extrusion, and either sends you back to the slicer before batch B01. The `pulley_jig` sets pulley stack height on the Z motors in Ch 02; keep it with the Z-drive bin.

**Check:** Both guide sizes fit their real rails with light finger pressure. This is one of the seven B00 gate items in `print/B00-calibration-and-jigs.md`; none of the other batches start until all seven pass.

⚠ **Rev D+ / LDO:** two rail-mounting rules that override the manual's default and matter from Ch 02 onward — (1) do **not** use the end hole of any rail; use the **second hole in from each end** (LDO Build Notes p.88); (2) tighten the rail screws from the **centre outward** so the rail pulls flush to the extrusion (manual p.24), leaving a ~3 mm gap between the frame and the bottom of the rail (manual p.25). [src](https://docs.ldomotors.com/voron/voron2/build-faq)

Source: [Voron manual p.25](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=25) · [Voron manual p.24](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=24) · [LDO Build Notes (Rev D)](https://docs.ldomotors.com/voron/voron2/build-faq) · [Voron-2 `STLs/Tools`](https://github.com/VoronDesign/Voron-2/tree/de7e89d/STLs/Tools)

Pause: ~40 min since the last pause — all seven rails greased, wiped back to bare steel, labelled X / Y1 / Y2 / Z0–Z3 and bagged, and both jig sizes test-fitted. Rail prep is per-rail work, so if you have to stop earlier, stop after a rail is packed, wiped and bagged — never with a carriage half-packed.

---

## How to read the manual pages

### Step 00.23 — Print guidelines (p.4)

![Voron manual p.4](assets/manual-pages/manual-p004.png)

**What you're looking at:** Manual p.4 — the Voron print specification, not an assembly step. These are the numbers the parts in this build are designed around: ABS or ASA, 0.2 mm layers, 4 perimeters, 5 solid top and bottom layers and 40 % infill, which together make a part stiff enough to hold a bearing and stable in a 60 °C chamber.

**Parts:** none.

**Do:** Read the Voron print spec once so you recognise it when it appears in the slicer chapter: ABS/ASA, 0.2 mm layers, **forced 0.4 mm extrusion width**, **4 perimeters**, **5 solid top and bottom layers**, **40% infill** in grid / gyroid / honeycomb / triangle / cubic. Every one of those numbers is already implemented in the PrusaSlicer profile in `print/00-slicer-setup.md` — this page is where they came from. Ignore the Print It Forward box: the decision on this build is to print everything yourself.

**Check:** Nothing to do on the bench. If your slicer profile disagrees with this page, the profile is wrong.

Source: [Voron manual p.4](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=4) · [slicer setup](print/00-slicer-setup.md)

---

### Step 00.24 — File naming, and where to get help (p.5–6)

![Voron manual p.5](assets/manual-pages/manual-p005.png)
![Voron manual p.6](assets/manual-pages/manual-p006.png)

**What you're looking at:** Manual p.5–6 — the STL filename convention and the two support routes. A prefix in square brackets sets the colour (`[a]_` = accent), and a `_xN` suffix is how many the machine needs ([glossary](16-glossary.md#symbols-prefixes-and-markers)). The print plan and every parts table in this manual are written in that convention.

**Parts:** none.

**Do:** Learn the three-part filename convention, because the print plan is written in it. A bare name (`z_joint_lower_x4.stl`) is **primary colour** — Galaxy Black here. A `[a]_` prefix (`[a]_tensioner_left.stl`) is **accent colour** — Prusa Orange here, which is why every `[a]_` part in the build is collected into the single orange batch B02. A `_x#` suffix is the **quantity the machine needs** — `_x4` means four, regardless of how many bodies are in the file. Bookmark the two help routes on p.5–6: the Voron Discord, and the CAD on GitHub, which is often clearer than a render when a page is ambiguous.

**Check:** You can read `[a]_z_belt_clip_lower_x4.stl` as "accent colour, four required".

Source: [Voron manual p.5](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=5) · [Voron manual p.6](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=6) · [print plan](../voron-print-plan.md)

---

### Step 00.25 — Fastener names, part 1 (p.7)

![Voron manual p.7](assets/manual-pages/manual-p007.png)

**What you're looking at:** Manual p.7 — the first half of the fastener vocabulary, each drawn beside its name. **BHCS** is a domed button head, **SHCS** a plain cylinder, **FHCS** a countersunk cone; a **roll-in T-nut** drops into an extrusion slot and rotates to lock, and a **hammerhead nut** drops in from the face instead ([glossary](16-glossary.md#b)). Every *Parts:* line in this manual uses these names exactly.

**Parts:** none.

**Do:** This page and the next are the naming contract for every *Parts* line in this manual. **BHCS** — domed head, mostly M5. **SHCS** — cylindrical head, the most common fastener in the machine. **FHCS** — countersunk cone head, flat top. **Self-tapping** — screwed straight into plastic. **Hex nut**, M3 and M5. **Heat-set insert** — brass, melted in. **T-nut (roll-in)** — drops into an extrusion slot after assembly, used everywhere. **Hammerhead nut** — used **exclusively for panel mounting**; everything else takes a T-nut. Lay one of each on the bench next to the page.

**Check:** You can pick a BHCS out of a bag by its dome and an SHCS by its straight cylinder without reading a label.

Source: [Voron manual p.7](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=7)

---

### Step 00.26 — Fastener names, part 2, and the spacer substitution (p.8)

![Voron manual p.8](assets/manual-pages/manual-p008.png)

**What you're looking at:** Manual p.8 — the second half: bearings, spacers, pulleys and set screws. **F695** and **625-2RS** are both 5 mm-bore ball bearings but different sizes and different jobs — F695 is flanged and lives in the A/B drives, 625-2RS is plain and lives in the Z drives ([glossary](16-glossary.md#f)). A **set screw** is a headless screw that clamps a pulley to a shaft, and a **shim** is a thin controlled-thickness washer that sets how far apart two things sit.

**Parts:** none.

**Do:** **F695** flanged bearing (5×13×4 mm — A/B drives, front idlers and XY joints, 20 in the kit), **625-2RS** bearing (5×16×5 mm — Z drives only, 12 in the kit), **shim** (DIN 988), **washer** (DIN 125, M3 only), **pulley** and **idler** (GT2), **set screw** (grub screw), **thumb nut** (bed spacer). Note that the manual calls out a *shim* at every M5 location.

**Check:** You can tell an F695 (flanged, 13 mm OD, 4 mm wide) from a 625-2RS (plain, 16 mm OD, 5 mm wide) on sight — both are **5 mm bore**, so sorting by bore does not work.

⚠ **Rev D+ / LDO:** wherever this manual or the official one says **M5 shim**, your kit gives you a **brass M5 1 mm precision spacer** instead — 46 of them, and they replace the shim everywhere unless a step says otherwise. p.104 is the exception: use the black M5 washer there, which is cosmetic. [src](https://docs.ldomotors.com/voron/voron2/build-faq)

Tip: the 16T and 20T GT2 pulleys look nearly identical and are not interchangeable — 16T goes on the Z motors, 20T everywhere else. Separate them into labelled bags during the Ch 02 prep, not while assembling.

Source: [Voron manual p.8](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=8) · [LDO Build Notes (Rev D)](https://docs.ldomotors.com/voron/voron2/build-faq)

---

### Step 00.27 — Drivers (p.9)

![Voron manual p.9](assets/manual-pages/manual-p009.png)

**What you're looking at:** Manual p.9 — the drivers. A **ball-end** driver has a spherical tip that lets it turn a screw at an angle, which is the only way to reach several joints in this frame; a plain hex tip grips more of the socket and is what you use when you need force.

**Parts:** hex drivers.

**Do:** Several joints in this design can only be reached at an angle, so a **ball-end** driver in 2.0, 2.5 and 3.0 mm is not optional. The **2.5 mm** driver does the most work in the entire build — that is the one worth having a good handle on. Your Fabreeko precision set covers this; keep the kit's L-wrenches as the backup for anywhere the driver handle will not fit.

**Check:** 2, 2.5 and 3 mm ball-end drivers on the bench, plus a plain 2.5 mm for anywhere you need to apply real force (ball ends cam out and round the socket under load).

Source: [Voron manual p.9](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=9)

---

### Step 00.28 — Blind joints (p.10)

![Voron manual p.10](assets/manual-pages/manual-p010.png)

**What you're looking at:** Manual p.10 — the **blind joint**, the joint the entire frame is built from. A button-head screw is threaded into the tapped bore in the end of one extrusion, its head captured inside the slot of the mating extrusion, and it is tightened through a small access hole drilled in the side ([glossary](16-glossary.md#b)). Nothing about it is visible once the frame is together, which is why it is worth understanding before Ch 01.

**Parts:** none.

**Do:** This is the joint the whole frame is built from, and it is the one thing worth watching a video about before Ch 01. The BHCS head slides **into the slot of one extrusion**, and its thread is driven into the tapped end of the mating extrusion; you reach the screw through a small access hole drilled in the side of the first extrusion. The consequence for assembly: the screw goes in *before* the two extrusions are brought together, and you tighten it through the access hole afterwards. Watch [voron.link/onjwmcd](https://voron.link/onjwmcd) once.

**Check:** You can point at the access hole on a 2020 extrusion and describe which way the BHCS goes in.

Source: [Voron manual p.10](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=10) · [blind-joint video](https://voron.link/onjwmcd)

---

### Step 00.29 — How to read an exploded view, and the page-number contract (p.11)

![Voron manual p.11](assets/manual-pages/manual-p011.png)

**What you're looking at:** Manual p.11 — how to read the drawings. Blue is what you are adding on this page, grey is what you already built, green is a printed jig, a rounded pill names a part, and the small wireframe cube in the corner tells you which way round the machine is drawn.

**Parts:** none.

**Do:** Learn the manual's five visual conventions, all visible on p.25: **blue** parts are what you are adding at this page; **grey/white** is structure you have already built; a **blue rounded pill** names a part or fastener with a leader line to it; the small wireframe cube in the top-left labelled *Top / Back / Front* tells you which way round the machine you are looking; **green** means a printed jig or tool, not a machine part; and a plain dimension arrow with a bare number is a millimetre gap you must leave. Red headings are section titles and warnings.

Then note the contract that makes this manual possible: the official PDF has not changed since **2023-07-18**, and LDO's Build Notes are a page-indexed diff pinned to that exact commit. Every `p.XX` reference in these chapters points at a page number that will not move. Pages like this one are dividers with no assembly content — they still get a page number, so do not assume a missing step when a page looks empty.

**Check:** Open any page in Ch 02 and identify, without reading the text, which part is new and which way the machine is facing.

Source: [Voron manual p.11](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=11) · [Voron manual p.25](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=25)

Pause: ~25 min since the last pause — you have read the manual's front matter (p.4–11) and can read a filename, a fastener name and an exploded view. Nothing physical is in progress.

---

## Build log and lifelines

### Step 00.30 — Start the build log

*(no image — see text)*

**What you're looking at:** A camera on a tripod and a notebook. The log is the only record of the numbers this build cannot re-derive later — the deck thickness, the frame diagonals, the belt frequency — and the ten listed shots are the ones no published source has for a Rev D+ kit.

**Parts:** phone or camera, tripod, a notebook or a shared album.

**Do:** Set one tripod position per work session and shoot 4:3 with good side light, so consecutive shots overlay and a change between sessions is obvious. Photograph at every chapter Checkpoint, and record the numbers you measure — deck thickness, frame diagonals at Ch 01, belt frequency at Ch 07, probe accuracy sigma at Ch 13. Beyond the checkpoints, shoot these ten because no published source has them for a Rev D+: every LDO deviation next to the part it replaces (precision spacer beside a shim, the second-hole rail mounting, the M3×20 bed screw, the deck support you chose next to the caliper reading); the Nitehawk-SB V2 both faces with PH2.0 connectors seated; the V2 fan-adapter header mated in its keyed orientation; the USB-adapter grounding wire as installed; the titanium backers on both axes before the XY joints are torqued; the electronics bay at each checkpoint; the gantry-squaring setup; the belt-tension measurement with the 150 mm span marked and the phone showing the peak; the good and bad heat-set inserts on the practice coupon; and the finished cable runs before the ducts are covered.

**Check:** The first entry exists before Ch 01 starts: cartons as they arrived, the inventory sheet with `Check1` ticked, and the three practice inserts. Your daughter owns the camera and the measurement log — the diagonals in Ch 01 are hers to read out.

Source: [survey](../voron-build-instructions-survey.md)

---

### Step 00.31 — Join the three lifelines now

*(no image — see text)*

**What you're looking at:** No parts — three chat channels. Fabreeko is the vendor and owns anything missing or wrong in the box; the Voron Discord is the community; `#ldo_motors` inside it is LDO's own channel and the place their Build Notes send Rev D corrections.

**Parts:** none.

**Do:** Join all three before the kit arrives, so you are not waiting on an invite while the frame sits half-built. **Fabreeko Discord** — [discord.gg/NV8Y6bcerP](https://discord.gg/NV8Y6bcerP), linked from the SKU page; the right place for missing or wrong parts and for anything vendor-specific. **Voron Discord** — [discord.gg/voron](https://discord.gg/voron); general build questions in `#voron_2_questions`. **`#ldo_motors`** inside the Voron Discord — [channel link](https://discord.com/channels/460117602945990666/710952853514223617); LDO's own support channel, and the place their Build Notes page explicitly directs Rev D corrections to.

**Check:** All three joined, notifications on for `#ldo_motors`.

Source: [LDO Build Notes (Rev D)](https://docs.ldomotors.com/voron/voron2/build-faq) · [LDO batch BOM index](https://docs.ldomotors.com/en/voron/voron2/350_BOM/HOME)

---

### Step 00.32 — Post the two questions that gate later chapters

*(no image — see text)*

**What you're looking at:** No parts — two questions with slow answers. Both concern gaps in LDO's published documentation for Rev D+ (the toolboard grounding scheme, and whether any STL changed), and both gate printing or wiring work several weeks out.

**Parts:** none.

**Do:** Both of these have days of answer latency and both block work you would otherwise have to redo. Post them today.

1. **In `#ldo_motors` — the Nitehawk-SB V2 grounding scheme.** The V2 repo ships `Images/grounding_scheme.jpg`, `Images/toolboard_ground_routing.jpg` and `Images/usb_adapter_gnd.jpg` with **no accompanying prose in any LDO document**, while the V2 change list claims "vastly improved ESD performance". Ask for the written procedure: what bonds to what, with what wire, and at which mounting point on `usb_adapter_mount_partial_cover`. Treat the grounding as a required build step in Ch 08/Ch 10, not an option. Gate: **Ch 10**.
2. **On the Fabreeko Discord — Rev D+ printed parts.** LDO publishes Printed Parts Guides for Rev A/B, C and D only; `printed_part_guide_rev_d_plus` returns 404. The whole print plan runs on Fabreeko's statement that D+ is an electrical change. Ask them to confirm that **no STL changed between Rev D and Rev D+ apart from the USB-adapter cover**, and ask whether a D+ wiring guide has been posted. Gate: **batches B06 and B07**, which print the toolhead and electronics-bay parts.

**Check:** Both questions posted, with your kit serial quoted. Note the date you asked in the build log; if either is unanswered by the time batch B06 is due, ask again rather than printing on an assumption.

Source: [LDO Nitehawk-SB V2 board doc](https://docs.ldomotors.com/en/Toolboard/nitehawk-sb-v2) · [LDO printed parts guide (Rev D)](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d) · [survey](../voron-build-instructions-survey.md)

Pause: ~20 min since the last pause — build log started, all three Discord channels joined and both gating questions posted with your kit serial. Work through Checkpoint 00 before you open Ch 01.

---

## Checkpoint 00

- [ ] Both cartons inventoried against **your batch's** BOM page; `Check1` ticked on every line; shortages written down and reported to Fabreeko.
- [ ] Deck panel thickness measured and written on its film. `deck_support_3mm_x8` or `_4mm_x8` chosen for batch B01.
- [ ] Nitehawk board confirmed as a **V2**: PH2.0 on PROBE/TH0/CT/Endstop, XH on MOTOR, secondary USB port present, fan-adapter header keyed. Both faces photographed. The `stm32g0b1xx` USB-serial check is written into the Ch 12 notes.
- [ ] XY endstop cable labels read `XES / YES`, or the re-pin guide is bookmarked.
- [ ] Ten LDO-supplied printed parts binned and labelled "DO NOT PRINT". Batch B07 corrected to `usb_adapter_mount_partial_cover.stl`.
- [ ] Every "Buy" row in Step 00.8 ordered or consciously skipped. Grease and IPA on the bench.
- [ ] Flat reference verified in five positions; worst feeler gap recorded; working area masked off and protected.
- [ ] Three practice inserts set: flush to ≤ 0.2 mm proud, square, boss not bulged > 0.2 mm. Working iron temperature written on the iron.
- [ ] All 7 rails: carriages taped, soaked 10 min in IPA ≥ 90%, dried, flip-and-packed until grease oozed past the bearings, rail surfaces wiped clean, labelled X / Y1 / Y2 / Z0–Z3, bagged.
- [ ] Both rail guides fit their real rails with light finger pressure; the full seven-item B00 gate has passed.
- [ ] Chapter bins labelled 00–14 and the batch-to-bin map posted on the wall.
- [ ] Build log started: carton photos, inventory sheet, practice coupon.
- [ ] Fabreeko Discord, Voron Discord and `#ldo_motors` joined; both gating questions posted.

## Common mistakes

- **Installing a rail before greasing it.** Flip-and-pack needs the back of the rail. Once it is on an extrusion your only options are to take it off again or run it dry and wear it out (survey §5.2 W9).
- **Leaving grease on the rail surface.** It looks well-lubricated and it is not — the film collects dust and hair and drags it into the carriage. Grease belongs inside the carriage only.
- **Lubricating before the IPA has fully evaporated.** The residue emulsifies with the grease and you get a milky paste with none of the film strength. Give the rails longer to dry than you think they need.
- **Letting a carriage run off the end of a rail.** The balls fall out and the carriage is scrap. Tape it the moment the bag is open, every time.
- **Practising heat-set inserts on PLA.** ASA softens at a different temperature; the setting you find on a PLA scrap will run too cold or too hot on all 150 remaining inserts.
- **Decanting the fastener bags on day one.** M3×8, M3×12 and M3×16 are indistinguishable in a mixed tray, and there are 283 of the first one.
- **Resolving the deck thickness from the documents.** LDO's guide and LDO's BOM contradict each other. Only the caliper settles it, and it has to be settled before batch B01 prints its deck supports.

## Next

**Ch 01 — Frame**: sort and prepare the 18 extrusions and build the squared frame on the reference surface you just verified.
