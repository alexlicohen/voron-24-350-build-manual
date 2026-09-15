# Acronym audit — 2026-09-14

Every token of 2–6 uppercase letters or digits (trailing `s` allowed) in `docs/manual/*.md`, `docs/manual/print/*.md`, `docs/index.md` and `docs/voron-print-plan.md`, counted and classified. Built by script; the table is the whole inventory, not a sample.

**Ask:** *“run a check for excessive acronyms that we have invented and just spell them out instead.”*

## Result

| Class | What it means | Tokens | Decision |
|---|---|---:|---|
| **1** | Community / industry standard — a Voron, Prusa or Klipper reader meets it everywhere | 268 | Keep; glossary row or spelled out at first use |
| **2** | **Invented here** — coined by this manual or an earlier pass over it | 3 | Spell out at every use, or keep only as a row marker whose legend defines it in words |
| **3** | Borderline — community-known but heavy for a first-time builder | 26 | Keep; glossary row required |
| **—** | Not an acronym — G-code, board silkscreen, pin name, part number, batch or plate id, an all-caps word in prose | 253 | Keep verbatim |
| | **Total** | **550** | |

### The whole invented set

| Token | Was | Now |
|---|---|---|
| `EM` | `EM` for extrusion multiplier, 14 uses across Ch 14, `print/00-slicer-setup.md`, `voron-print-plan.md`, the glossary and the generated Tonight view | Spelled out everywhere. Step 14.19's Do reads *“at **92, 94, 96, 98 %** flow”*; Step 14.21's title is *“…because the multiplier moved”*; the glossary row is **Extrusion multiplier / flow**. Ellis' article title *PA / EM Oddities* keeps its own spelling, being a citation |
| `KIT` | Timeline row marker in `00-index.md` | Kept as a marker — it is a column value in a generated structure. The legend at the head of § The timeline already reads **KIT** = needs the Voron kit to have arrived |
| `2P` / `2P lift` | Timeline row marker in `00-index.md` | Kept as a marker, same reason. Legend: **2P** = two people · **2P lift** = the gantry lift, genuinely two people. Ch 10's `JST-PH2.0 2P` is a connector position count, not this marker |

Candidates in the brief that turned out **not** to be ours, checked one by one and kept:

- `TH0` `TH1` `CT` `HE0` `PROBE` `XY ENDSTOP` `FAN0`–`FAN3` `BOOT0` — Nitehawk-SB V2 and Leviathan **silkscreen**, quoted so the reader can find the socket.
- `XES` / `YES` — the label LDO prints on the XY-endstop harness, quoted with the mis-pinned-batch warning.
- `Z0`–`Z3` — Klipper's own stepper names, and the bin ids built from them.
- `FL` / `FR` / `RL` / `RR` — corner codes do not appear anywhere in the manual; the corners are named `Z0`–`Z3` with *front-left* etc. spelled out.
- `AFS` — does not appear; the Advanced Filtration System is only ever written out.
- `USS` (Prusa product), `SP2` (absent), `Gate A` / `Gate B` (named gates, not abbreviations).
- `OL`, `KMS`, `VRN`, `IDGA`, `Q5MC`, `TPW`/`LCH`/`RCH`, `RSP`, `HEF`/`PCF`, `V2TR`, `NH` — all vendor part codes, datasheet labels or file names.

### What was added while auditing

Six class-3 tokens had no glossary row and were never spelled out at first use. Rows added to `docs/manual/16-glossary.md`: **DSI ribbon**, **FFC**, **IPA**, **PTFE**, **VHB**, **XT30**. Corrections-log rows 31 and 32 in `00-index.md` record the spell-out and the plate-mark rule.

---

## Full inventory

Sorted by count. *Files* is how many of the audited files the token appears in.

| Token | Count | Files | Class | Decision | Replacement / note |
|---|---:|---|:---:|---|---|
| `LDO` | 1326 | 35 — 00-before-you-start, 00-index, 00-slicer-setup, … | 1 | KEEP | Vendor name (LDO Motors) |
| `M3` | 647 | 29 — 00-before-you-start, 00-index, 00-slicer-setup, … | — | KEEP | G-code / M-code |
| `M5` | 494 | 18 — 00-before-you-start, 00-tonight, 00a-mains-safety, … | — | KEEP | G-code / M-code |
| `STLs` | 381 | 25 — 00-before-you-start, 00-index, 00-slicer-setup, … | 1 | KEEP | Stereolithography mesh files |
| `SB` | 339 | 19 — 00-before-you-start, 00-index, 00-slicer-setup, … | 3 | KEEP | Glossary § S (Stealthburner) / § N (Nitehawk-SB V2) |
| `V2` | 313 | 21 — 00-before-you-start, 00-index, 00-slicer-setup, … | 1 | KEEP | Board revision 2 |
| `XY` | 312 | 24 — 00-before-you-start, 00-index, 00-slicer-setup, … | 1 | KEEP | The X and Y axes |
| `B00` | 280 | 26 — 00-before-you-start, 00-index, 00-slicer-setup, … | — | KEEP | Print-batch id |
| `SHCS` | 250 | 16 — 00-before-you-start, 00-index, 02-z-drives, … | 3 | KEEP | Glossary § S; taught at 00.25 |
| `B02` | 238 | 27 — 00-before-you-start, 00-index, 00-slicer-setup, … | — | KEEP | Print-batch id |
| `P1` | 219 | 26 — 00-index, 00-slicer-setup, 00-tonight, … | — | KEEP | Plate number / manual page id |
| `USB` | 189 | 15 — 00-before-you-start, 00-index, 00-slicer-setup, … | 1 | KEEP | Universal Serial Bus |
| `PCB` | 184 | 15 — 00-before-you-start, 00-tonight, 03-build-plate, … | 1 | KEEP | Printed Circuit Board |
| `B08` | 178 | 17 — 00-before-you-start, 00-index, 00-slicer-setup, … | — | KEEP | Print-batch id |
| `PSU` | 170 | 14 — 00-before-you-start, 00-index, 00-tonight, … | 1 | KEEP | Power Supply Unit |
| `B09` | 167 | 11 — 00-before-you-start, 00-index, 00-slicer-setup, … | — | KEEP | Print-batch id |
| `ASA` | 164 | 29 — 00-before-you-start, 00-index, 00-slicer-setup, … | 1 | KEEP | Acrylonitrile Styrene Acrylate |
| `BHCS` | 157 | 15 — 00-before-you-start, 00-tonight, 00a-mains-safety, … | 3 | KEEP | Glossary § B; taught at 00.25 |
| `LED` | 155 | 16 — 00-before-you-start, 00-index, 00-slicer-setup, … | 1 | KEEP | Light-Emitting Diode |
| `SSR` | 146 | 10 — 00-index, 00-tonight, 00a-mains-safety, … | 1 | KEEP | Solid-State Relay |
| `B07` | 145 | 16 — 00-before-you-start, 00-index, 00-slicer-setup, … | — | KEEP | Print-batch id |
| `QGL` | 139 | 13 — 00-index, 00-tonight, 03-build-plate, … | 3 | KEEP | Glossary § Q; spelled out at 13.33 |
| `WAGO` | 137 | 12 — 00-before-you-start, 00-index, 00-tonight, … | 1 | KEEP | Vendor name (WAGO lever connectors) |
| `B01` | 134 | 14 — 00-before-you-start, 00-index, 00-slicer-setup, … | — | KEEP | Print-batch id |
| `README` | 126 | 28 — 00-before-you-start, 00-index, 00-slicer-setup, … | 1 | KEEP | Filename |
| `STL` | 123 | 32 — 00-before-you-start, 00-index, 00-slicer-setup, … | 1 | KEEP | Stereolithography mesh file |
| `BOM` | 110 | 18 — 00-before-you-start, 00-index, 02-z-drives, … | 1 | KEEP | Bill of Materials |
| `PE` | 109 | 8 — 00-tonight, 00a-mains-safety, 03-build-plate, … | 1 | KEEP | Protective Earth |
| `DIN` | 105 | 14 — 00-before-you-start, 00-index, 00-tonight, … | 1 | KEEP | Deutsches Institut fur Normung (rail / washer standard) |
| `B06` | 97 | 14 — 00-before-you-start, 00-index, 00-slicer-setup, … | — | KEEP | Print-batch id |
| `Z0` | 97 | 15 — 00-before-you-start, 00-index, 00-tonight, … | — | KEEP | Z corner / Z motor id |
| `B10` | 92 | 15 — 00-before-you-start, 00-index, 00-slicer-setup, … | — | KEEP | Print-batch id |
| `B03` | 89 | 16 — 00-before-you-start, 00-index, 00-slicer-setup, … | — | KEEP | Print-batch id |
| `P2` | 87 | 17 — 00-before-you-start, 00-index, 00-tonight, … | — | KEEP | Plate number / manual page id |
| `CAD` | 86 | 10 — 00-before-you-start, 01-frame, 02-z-drives, … | 1 | KEEP | Computer-Aided Design |
| `V1` | 83 | 11 — 00-before-you-start, 00-index, 08-toolhead, … | 1 | KEEP | Board revision 1 |
| `F695` | 79 | 10 — 00-before-you-start, 00-index, 00-slicer-setup, … | 1 | KEEP | Bearing size |
| `B05` | 76 | 13 — 00-before-you-start, 00-index, 00-slicer-setup, … | — | KEEP | Print-batch id |
| `CW2` | 74 | 13 — 00-before-you-start, 00-index, 00-tonight, … | 3 | KEEP | Glossary § C (Clockwork 2) |
| `20T` | 70 | 10 — 00-before-you-start, 00-index, 00-tonight, … | 1 | KEEP | 20-tooth pulley |
| `B04` | 70 | 14 — 00-before-you-start, 00-index, 00-slicer-setup, … | — | KEEP | Print-batch id |
| `BTT` | 69 | 10 — 00-before-you-start, 00-slicer-setup, 09-electronics-bay, … | 1 | KEEP | Vendor name (BIGTREETECH) |
| `Z3` | 67 | 10 — 00-before-you-start, 00-tonight, 02-z-drives, … | — | KEEP | Z corner / Z motor id |
| `P3` | 66 | 13 — 00-index, 00-tonight, 01-frame, … | — | KEEP | Plate number / manual page id |
| `G28` | 58 | 9 — 00-tonight, 06-z-axis-and-gantry-squaring, 07-ab-belts, … | — | KEEP | G-code / M-code |
| `COB` | 55 | 11 — 00-index, 00-tonight, 09-electronics-bay, … | 1 | KEEP | Chip-on-Board LED strip |
| `MGN12` | 55 | 13 — 00-before-you-start, 00-index, 00-slicer-setup, … | 1 | KEEP | Linear rail size |
| `AC` | 54 | 6 — 00a-mains-safety, 03-build-plate, 09-electronics-bay, … | 1 | KEEP | Alternating current |
| `HF` | 53 | 11 — 00-before-you-start, 00-index, 00-slicer-setup, … | 1 | KEEP | High Flow (nozzle / preset) |
| `PH2` | 53 | 9 — 00-before-you-start, 00-tonight, 08-toolhead, … | 1 | KEEP | JST-PH 2.0 mm connector |
| `2RS` | 51 | 11 — 00-before-you-start, 00-index, 00-slicer-setup, … | 1 | KEEP | Bearing seal type |
| `FHCS` | 50 | 9 — 00-before-you-start, 00-tonight, 05-gantry, … | 3 | KEEP | Glossary § F; taught at 00.25 |
| `JST` | 48 | 8 — 00-before-you-start, 08-toolhead, 09-electronics-bay, … | 1 | KEEP | Vendor name (JST connectors) |
| `Z2` | 47 | 10 — 00-before-you-start, 02-z-drives, 10-wiring, … | — | KEEP | Z corner / Z motor id |
| `FAQ` | 46 | 14 — 05-gantry, 06-z-axis-and-gantry-squaring, 07-ab-belts, … | 1 | KEEP | Frequently Asked Questions |
| `Z1` | 46 | 9 — 00-before-you-start, 02-z-drives, 10-wiring, … | — | KEEP | Z corner / Z motor id |
| `PID` | 43 | 7 — 00-index, 00-tonight, 12-software, … | 3 | KEEP | Glossary § P (PID tune) |
| `LEDs` | 41 | 11 — 00-before-you-start, 00-tonight, 00a-mains-safety, … | 1 | KEEP | Light-Emitting Diodes |
| `ID` | 39 | 10 — 00-before-you-start, 00-index, 00-tonight, … | 1 | KEEP | Identifier / inner diameter |
| `IPA` | 39 | 12 — 00-before-you-start, 00-slicer-setup, 00-tonight, … | 3 | KEEP | Glossary § I — row added |
| `24V` | 37 | 4 — 08-toolhead, 10-wiring, 12-software, … | — | KEEP | Part number, size or voltage |
| `LOAD` | 37 | 7 — 00-tonight, 00a-mains-safety, 09-electronics-bay, … | 1 | KEEP | SSR terminal label |
| `M4` | 36 | 6 — 00-before-you-start, 00a-mains-safety, 02-z-drives, … | — | KEEP | G-code / M-code |
| `P4` | 36 | 9 — 00-tonight, 08-toolhead, 12-software, … | — | KEEP | Plate number / manual page id |
| `GT2` | 35 | 13 — 00-before-you-start, 00-index, 00-slicer-setup, … | 1 | KEEP | Belt profile, 2 mm pitch |
| `PROBE` | 35 | 8 — 00-before-you-start, 08-toolhead, 10-wiring, … | 1 | KEEP | Board port label |
| `KB` | 34 | 14 — 00-slicer-setup, 15-troubleshooting, B00-calibration-and-jigs, … | 1 | KEEP | Prusa Knowledge Base |
| `HV` | 32 | 7 — 00-tonight, 04-ab-drives, 10-wiring, … | 1 | KEEP | High voltage |
| `V5` | 32 | 7 — 00-index, 00-slicer-setup, 11-skirts-panels-door, … | 1 | KEEP | Nevermore Micro revision |
| `16T` | 31 | 6 — 00-before-you-start, 00-tonight, 02-z-drives, … | 1 | KEEP | 16-tooth pulley |
| `CORE` | 31 | 5 — 00-index, 00-slicer-setup, 13-initial-startup, … | 1 | KEEP | Prusa CORE One |
| `C14` | 30 | 5 — 00a-mains-safety, 09-electronics-bay, 10-wiring, … | 1 | KEEP | IEC connector |
| `MCU` | 29 | 7 — 00-before-you-start, 00-index, 10-wiring, … | 1 | KEEP | Microcontroller Unit |
| `TFT` | 29 | 7 — 00-index, 00-slicer-setup, 11-skirts-panels-door, … | 1 | KEEP | Thin-Film Transistor display |
| `2X` | 28 | 6 — 00-slicer-setup, 05-gantry, 11-skirts-panels-door, … | 1 | KEEP | Quantity marker in an LDO/Voron STL name or manual callout |
| `FFC` | 28 | 5 — 00-tonight, 10-wiring, 11-skirts-panels-door, … | 3 | KEEP | Glossary § F — row added |
| `HF0` | 28 | 7 — 00-index, 00-slicer-setup, 13-initial-startup, … | 1 | KEEP | High-flow 0.4 nozzle preset |
| `80T` | 27 | 4 — 00-tonight, 02-z-drives, 16-glossary, … | 1 | KEEP | 80-tooth pulley |
| `ESD` | 27 | 9 — 00-before-you-start, 00-index, 00-tonight, … | 3 | KEEP | Glossary § E |
| `DSI` | 26 | 6 — 00-tonight, 10-wiring, 11-skirts-panels-door, … | 3 | KEEP | Glossary § D — row added |
| `INPUT` | 26 | 6 — 00a-mains-safety, 09-electronics-bay, 10-wiring, … | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `M112` | 26 | 2 — 13-initial-startup, 14-calibration | — | KEEP | G-code / M-code |
| `MCUs` | 26 | 8 — 00-index, 00-tonight, 10-wiring, … | 1 | KEEP | Microcontroller Units |
| `NN` | 26 | 3 — 00-index, 16-glossary, CONVENTIONS | 1 | KEEP | Numeric placeholder |
| `PTFE` | 26 | 6 — 00-tonight, 02-z-drives, 08-toolhead, … | 3 | KEEP | Glossary § P — row added |
| `GT1` | 25 | 9 — 00-index, 00-slicer-setup, 16-glossary, … | 1 | KEEP | Belt profile, 1.5 mm pitch |
| `TFT4` | 25 | 5 — 00-slicer-setup, 11-skirts-panels-door, B02-accent-parts-orange, … | 1 | KEEP | BTT TFT4.3 display |
| `FAN3` | 24 | 6 — 10-wiring, 11-skirts-panels-door, 12-software, … | 1 | KEEP | Fan port |
| `TH0` | 24 | 5 — 00-before-you-start, 08-toolhead, 10-wiring, … | 3 | KEEP | Nitehawk-SB silkscreen; described at 08.36 |
| `MGN9` | 23 | 8 — 00-index, 02-z-drives, 05-gantry, … | 1 | KEEP | Linear rail size |
| `KIT` | 22 | 3 — 00-index, 00-tonight, 11-skirts-panels-door | 2 | KEEP as row marker | legend at the head of 00-index.md § The timeline reads “KIT = needs the Voron kit to have arrived”. The one use outside the index is inside an LDO quote in Ch 11 |
| `VHB` | 22 | 4 — 00-tonight, 09-electronics-bay, 11-skirts-panels-door, … | 3 | KEEP | Glossary § V — row added |
| `XH` | 22 | 5 — 00-before-you-start, 03-build-plate, 09-electronics-bay, … | 1 | KEEP | JST connector series |
| `LRS` | 21 | 5 — 00-before-you-start, 00a-mains-safety, 09-electronics-bay, … | 1 | KEEP | Mean Well PSU series |
| `104NT` | 20 | 6 — 03-build-plate, 08-toolhead, 10-wiring, … | 1 | KEEP | Thermistor part number |
| `E3D` | 20 | 6 — 08-toolhead, 12-software, 14-calibration, … | 1 | KEEP | Vendor name (E3D) |
| `GND` | 20 | 3 — 00a-mains-safety, 08-toolhead, 10-wiring | 1 | KEEP | Ground |
| `OL` | 20 | 3 — 00a-mains-safety, 10-wiring, 16-glossary | 3 | KEEP | Glossary § Symbols |
| `PF9` | 20 | 5 — 00-tonight, 10-wiring, 11-skirts-panels-door, … | — | KEEP | STM32 pin name |
| `SKIP` | 20 | 10 — 03-build-plate, 06-z-axis-and-gantry-squaring, 07-ab-belts, … | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `STEP` | 20 | 7 — 01-frame, 02-z-drives, 03-build-plate, … | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `XH2` | 20 | 6 — 08-toolhead, 10-wiring, 12-software, … | 1 | KEEP | JST-XH 2.5 mm connector |
| `DC` | 19 | 5 — 00-tonight, 00a-mains-safety, 09-electronics-bay, … | 1 | KEEP | Direct current |
| `KB3D` | 19 | 1 — 11-skirts-panels-door | 1 | KEEP | Vendor name (KB-3D) |
| `M2` | 19 | 4 — 08-toolhead, 09-electronics-bay, 10-wiring, … | — | KEEP | G-code / M-code |
| `CT` | 17 | 8 — 00-before-you-start, 08-toolhead, 10-wiring, … | 3 | KEEP | Nitehawk-SB silkscreen; described at 08.44 |
| `FAN` | 17 | 4 — 10-wiring, 11-skirts-panels-door, 12-software, … | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `MGN9H` | 16 | 5 — 00-before-you-start, 02-z-drives, 05-gantry, … | 1 | KEEP | Linear rail carriage |
| `OD` | 16 | 8 — 00-before-you-start, 00-index, 00-slicer-setup, … | 1 | KEEP | Outer diameter |
| `D2F` | 15 | 8 — 05-gantry, 06-z-axis-and-gantry-squaring, 08-toolhead, … | 1 | KEEP | Omron microswitch series |
| `G32` | 15 | 6 — 00-tonight, 12-software, 13-initial-startup, … | — | KEEP | G-code / M-code |
| `G3NB` | 15 | 4 — 00a-mains-safety, 09-electronics-bay, 10-wiring, … | 1 | KEEP | Omron SSR series |
| `C13` | 14 | 7 — 00-before-you-start, 00-tonight, 00a-mains-safety, … | 1 | KEEP | IEC connector |
| `FAN2` | 14 | 4 — 10-wiring, 11-skirts-panels-door, 12-software, … | 1 | KEEP | Fan port |
| `HE0` | 14 | 4 — 08-toolhead, 10-wiring, 12-software, … | 3 | KEEP | Nitehawk-SB silkscreen; described at 08.36 |
| `IEC` | 14 | 6 — 00-tonight, 00a-mains-safety, 09-electronics-bay, … | 1 | KEEP | International Electrotechnical Commission |
| `KIAUH` | 14 | 3 — 00-tonight, 12-software, 16-glossary | 3 | KEEP | Glossary § K |
| `M84` | 14 | 5 — 00-tonight, 10-wiring, 13-initial-startup, … | — | KEEP | G-code / M-code |
| `NOT` | 14 | 7 — 00-before-you-start, 01-frame, 11-skirts-panels-door, … | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `P5` | 14 | 4 — 00-tonight, B09-panels-filtration-spool, README, … | — | KEEP | Plate number / manual page id |
| `RESET` | 14 | 4 — 00a-mains-safety, 08-toolhead, 12-software, … | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `TO` | 14 | 1 — 10-wiring | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `CAT` | 13 | 2 — 00a-mains-safety, 16-glossary | 1 | KEEP | Cable / electrical category |
| `PETG` | 13 | 6 — 00-before-you-start, 00-slicer-setup, 08-toolhead, … | 1 | KEEP | Polyethylene terephthalate glycol |
| `URL` | 13 | 8 — 00-before-you-start, 00-index, 00a-mains-safety, … | 1 | KEEP | Uniform Resource Locator |
| `20TFT4` | 12 | 2 — 11-skirts-panels-door, voron-print-plan | 1 | KEEP | 20T pulley / TFT4.3 in one table cell |
| `MR85` | 12 | 1 — 08-toolhead | 1 | KEEP | Bearing size |
| `R2` | 12 | 8 — 00-index, 00-slicer-setup, 07-ab-belts, … | 1 | KEEP | Voron 2.4 revision 2 |
| `S4` | 12 | 2 — 10-wiring, 11-skirts-panels-door | 1 | KEEP | LDO photo id |
| `DFU` | 11 | 3 — 12-software, 15-troubleshooting, 16-glossary | 3 | KEEP | Glossary § D |
| `FRONT` | 11 | 4 — 00-tonight, 01-frame, 02-z-drives, … | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `HAT` | 11 | 4 — 00-tonight, 09-electronics-bay, 10-wiring, … | 1 | KEEP | Raspberry Pi add-on board |
| `MB` | 11 | 1 — 10-wiring | 1 | KEEP | Megabyte |
| `PEI` | 11 | 6 — 00-slicer-setup, 13-initial-startup, 14-calibration, … | 3 | KEEP | Glossary § P |
| `S6` | 11 | 2 — 10-wiring, 11-skirts-panels-door | 1 | KEEP | LDO photo id |
| `SD` | 11 | 3 — 09-electronics-bay, 12-software, 13-initial-startup | 1 | KEEP | Secure Digital card |
| `SSH` | 11 | 2 — 12-software, 13-initial-startup | 1 | KEEP | Secure Shell |
| `W8` | 11 | 5 — 00-index, 00a-mains-safety, 09-electronics-bay, … | — | KEEP | Wire / warning id |
| `XT30` | 11 | 3 — 08-toolhead, 10-wiring, 16-glossary | 3 | KEEP | Glossary § X — row added |
| `AB` | 10 | 3 — 06-z-axis-and-gantry-squaring, 08-toolhead, voron-print-plan | 1 | KEEP | A/B carriage (Klicky part name) |
| `ATC` | 10 | 5 — 03-build-plate, 10-wiring, 12-software, … | 1 | KEEP | Vendor name (ATC Semitec) |
| `BED` | 10 | 5 — 03-build-plate, 10-wiring, 12-software, … | 1 | KEEP | Board port label |
| `FG` | 10 | 2 — 00a-mains-safety, 10-wiring | 1 | KEEP | Frame Ground |
| `G0` | 10 | 2 — 12-software, 13-initial-startup | — | KEEP | G-code / M-code |
| `GFCI` | 10 | 2 — 00a-mains-safety, 16-glossary | 1 | KEEP | Ground-Fault Circuit Interrupter |
| `LEFT` | 10 | 5 — 00-index, 00-tonight, 04-ab-drives, … | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `PC` | 10 | 3 — 00-before-you-start, 11-skirts-panels-door, voron-print-plan | 1 | KEEP | Polycarbonate |
| `RCD` | 10 | 2 — 00a-mains-safety, 16-glossary | 1 | KEEP | Residual-Current Device |
| `RIGHT` | 10 | 5 — 00-index, 00-tonight, 04-ab-drives, … | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `TESTZ` | 10 | 3 — 13-initial-startup, 15-troubleshooting, 16-glossary | 1 | KEEP | Klipper command |
| `TH1` | 10 | 3 — 00-tonight, 10-wiring, 12-software | 3 | KEEP | Leviathan silkscreen; described at 10.44 |
| `VE0508` | 10 | 4 — 00a-mains-safety, 09-electronics-bay, 10-wiring, … | 1 | KEEP | Ferrule size |
| `VFA` | 10 | 6 — 00-index, 00-slicer-setup, 15-troubleshooting, … | 3 | KEEP | Glossary § V, spelled out in the row |
| `VS8` | 10 | 1 — 10-wiring | 1 | KEEP | LDO photo id |
| `2GT` | 9 | 4 — 02-z-drives, 04-ab-drives, 06-z-axis-and-gantry-squaring, … | 1 | KEEP | Belt profile, 2 mm pitch |
| `4B` | 9 | 2 — 09-electronics-bay, 12-software | 1 | KEEP | Raspberry Pi 4 Model B |
| `A1` | 9 | 2 — 08-toolhead, README | 1 | KEEP | Fan tacho pin / accent spool id |
| `CAT6` | 9 | 4 — 10-wiring, 11-skirts-panels-door, B02-accent-parts-orange, … | 1 | KEEP | Ethernet cable category |
| `MGN12H` | 9 | 5 — 00-before-you-start, 02-z-drives, 05-gantry, … | 1 | KEEP | Linear rail carriage |
| `ON` | 9 | 1 — 10-wiring | 1 | KEEP | Switch position |
| `PC15` | 9 | 5 — 08-toolhead, 10-wiring, 12-software, … | — | KEEP | STM32 pin name |
| `PDF` | 9 | 4 — 00-before-you-start, 00a-mains-safety, 16-glossary, … | 1 | KEEP | Portable Document Format |
| `PF7` | 9 | 4 — 10-wiring, 11-skirts-panels-door, 12-software, … | — | KEEP | STM32 pin name |
| `RP2040` | 9 | 2 — 00-before-you-start, 12-software | 1 | KEEP | Raspberry Pi microcontroller |
| `S1` | 9 | 2 — 10-wiring, 11-skirts-panels-door | 1 | KEEP | LDO photo id |
| `TH` | 9 | 3 — 03-build-plate, 10-wiring, 15-troubleshooting | 1 | KEEP | Thermistor port label |
| `TODO` | 9 | 3 — 00-tonight, 12-software, 14-calibration | 1 | KEEP | Outstanding item |
| `V12` | 9 | 1 — 12-software | 1 | KEEP | Leviathan board revision |
| `VORON` | 9 | 1 — 12-software | 1 | KEEP | Project name |
| `W1` | 9 | 5 — 05-gantry, 06-z-axis-and-gantry-squaring, 07-ab-belts, … | — | KEEP | Wire / warning id |
| `X175` | 9 | 2 — 12-software, 13-initial-startup | — | KEEP | G-code coordinate |
| `2P` | 8 | 2 — 00-index, 10-wiring | 2 | KEEP as row marker | legend reads “2P = two people · 2P lift = the gantry lift, genuinely two people”. `JST-PH2.0 2P` in Ch 10 is the connector position count, an industry token that happens to collide |
| `ABS` | 8 | 6 — 00-before-you-start, 00-index, 00-slicer-setup, … | 1 | KEEP | Acrylonitrile butadiene styrene |
| `ACT` | 8 | 2 — 08-toolhead, 12-software | 1 | KEEP | Activity LED |
| `ADXL` | 8 | 4 — 08-toolhead, 14-calibration, B06-toolhead-sb-cw2-klicky, … | 1 | KEEP | Accelerometer family (ADXL345) |
| `BOOT0` | 8 | 3 — 08-toolhead, 12-software, 16-glossary | 1 | KEEP | Board button label |
| `E0508` | 8 | 3 — 08-toolhead, 10-wiring, 12-software | — | KEEP | G-code extruder parameter |
| `FILTER` | 8 | 3 — 10-wiring, 11-skirts-panels-door, 12-software | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `G1` | 8 | 2 — 13-initial-startup, 14-calibration | — | KEEP | G-code / M-code |
| `GPIO` | 8 | 3 — 09-electronics-bay, 10-wiring, 12-software | 1 | KEEP | General-Purpose Input/Output |
| `MSG` | 8 | 1 — 12-software | 1 | KEEP | G-code parameter |
| `PLA` | 8 | 5 — 00-before-you-start, 00-slicer-setup, 13-initial-startup, … | 1 | KEEP | Polylactic acid |
| `SPEED` | 8 | 4 — 00-slicer-setup, 12-software, 13-initial-startup, … | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `STM32` | 8 | 3 — 00-index, 12-software, 16-glossary | 1 | KEEP | Microcontroller family |
| `SW1` | 8 | 1 — 12-software | 1 | KEEP | Board switch label |
| `VRN` | 8 | 4 — 02-z-drives, 04-ab-drives, 08-toolhead, … | 1 | KEEP | LDO motor part suffix |
| `WAGOs` | 8 | 6 — 00-index, 00a-mains-safety, 03-build-plate, … | 1 | KEEP | WAGO lever connectors |
| `XL` | 8 | 4 — 00-slicer-setup, 11-skirts-panels-door, B09-panels-filtration-spool, … | 1 | KEEP | Prusa XL |
| `Y175` | 8 | 2 — 12-software, 13-initial-startup | — | KEEP | G-code coordinate |
| `5V` | 7 | 2 — 08-toolhead, 09-electronics-bay | — | KEEP | Part number, size or voltage |
| `BMG` | 7 | 2 — 08-toolhead, 16-glossary | 1 | KEEP | Bondtech BMG extruder geometry |
| `ENABLE` | 7 | 4 — 00-tonight, 06-z-axis-and-gantry-squaring, 13-initial-startup, … | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `H5` | 7 | 4 — 00-before-you-start, 00-slicer-setup, B00-calibration-and-jigs, … | 1 | KEEP | Insert length code (M3xH5) |
| `M106` | 7 | 2 — 12-software, 13-initial-startup | — | KEEP | G-code / M-code |
| `M83` | 7 | 3 — 12-software, 13-initial-startup, 14-calibration | — | KEEP | G-code / M-code |
| `OS` | 7 | 2 — 12-software, 14-calibration | 1 | KEEP | Operating system |
| `PA` | 7 | 3 — 00-index, 00-tonight, 14-calibration | 3 | KEEP | Glossary § P (Pressure advance) |
| `RV` | 7 | 3 — 08-toolhead, 16-glossary, voron-print-plan | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `S7` | 7 | 2 — 10-wiring, 12-software | 1 | KEEP | LDO photo id |
| `210B` | 6 | 4 — 00a-mains-safety, 09-electronics-bay, 10-wiring, … | 1 | KEEP | Omron SSR part code |
| `3M` | 6 | 3 — 09-electronics-bay, 11-skirts-panels-door, 16-glossary | — | KEEP | Part number, size or voltage |
| `48V` | 6 | 2 — 10-wiring, 16-glossary | — | KEEP | Part number, size or voltage |
| `API` | 6 | 3 — 12-software, 13-initial-startup, 16-glossary | 1 | KEEP | Application Programming Interface |
| `EMF` | 6 | 5 — 06-z-axis-and-gantry-squaring, 08-toolhead, 10-wiring, … | 1 | KEEP | Electromotive force |
| `GPL` | 6 | 6 — 05-gantry, 06-z-axis-and-gantry-squaring, 07-ab-belts, … | 1 | KEEP | GNU General Public License |
| `GUI` | 6 | 2 — 00-index, 00-slicer-setup | 1 | KEEP | Graphical User Interface |
| `HOME` | 6 | 1 — 00-before-you-start | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `M114` | 6 | 1 — 13-initial-startup | — | KEEP | G-code / M-code |
| `MOTOR` | 6 | 3 — 00-before-you-start, 08-toolhead, 16-glossary | 1 | KEEP | Board port label |
| `OFF` | 6 | 2 — 00a-mains-safety, 10-wiring | 1 | KEEP | Switch position |
| `PA15` | 6 | 3 — 08-toolhead, 12-software, 13-initial-startup | — | KEEP | STM32 pin name |
| `PAGE` | 6 | 5 — 07-ab-belts, 09-electronics-bay, 11-skirts-panels-door, … | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `PB2` | 6 | 5 — 08-toolhead, 10-wiring, 12-software, … | — | KEEP | STM32 pin name |
| `PC6` | 6 | 1 — 12-software | — | KEEP | STM32 pin name |
| `PD0` | 6 | 3 — 08-toolhead, 12-software, 13-initial-startup | — | KEEP | STM32 pin name |
| `PE6` | 6 | 4 — 10-wiring, 11-skirts-panels-door, 12-software, … | — | KEEP | STM32 pin name |
| `REAR` | 6 | 2 — 00-tonight, 04-ab-drives | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `S5` | 6 | 1 — 10-wiring | 1 | KEEP | LDO photo id |
| `STATUS` | 6 | 3 — 12-software, 13-initial-startup, 14-calibration | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `THE` | 6 | 4 — 00a-mains-safety, 09-electronics-bay, 10-wiring, … | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `W3` | 6 | 5 — 00-before-you-start, 02-z-drives, 06-z-axis-and-gantry-squaring, … | — | KEEP | Wire / warning id |
| `XES` | 6 | 4 — 00-before-you-start, 09-electronics-bay, 10-wiring, … | 3 | KEEP | LDO harness label, quoted with the mis-pin warning |
| `YES` | 6 | 4 — 00-before-you-start, 09-electronics-bay, 10-wiring, … | 1 | KEEP | LDO harness label (also the English word) |
| `2004AC` | 5 | 4 — 00-before-you-start, 02-z-drives, 04-ab-drives, … | 1 | KEEP | LDO motor part code |
| `3MF` | 5 | 5 — 00-index, 00-slicer-setup, B09-panels-filtration-spool, … | 1 | KEEP | 3D Manufacturing Format |
| `50T` | 5 | 1 — 08-toolhead | 1 | KEEP | 50-tooth gear |
| `EARTH` | 5 | 3 — 00a-mains-safety, 09-electronics-bay, 10-wiring | 1 | KEEP | Terminal label |
| `F6000` | 5 | 2 — 13-initial-startup, 14-calibration | 1 | KEEP | Bearing size |
| `IDs` | 5 | 4 — 00-tonight, 12-software, 13-initial-startup, … | 1 | KEEP | Identifiers |
| `III` | 5 | 1 — 00a-mains-safety | 1 | KEEP | Roman numeral |
| `IN` | 5 | 2 — 08-toolhead, 10-wiring | 1 | KEEP | Terminal label |
| `NH` | 5 | 3 — 00-before-you-start, 08-toolhead, 09-electronics-bay | 1 | KEEP | Nitehawk (LDO STL name) |
| `NLGI` | 5 | 2 — 00-before-you-start, 02-z-drives | 1 | KEEP | Grease consistency grade |
| `PA11` | 5 | 1 — 12-software | 1 | KEEP | Nylon 11 |
| `PA12` | 5 | 1 — 12-software | 1 | KEEP | Nylon 12 |
| `PB8` | 5 | 3 — 12-software, 13-initial-startup, 15-troubleshooting | — | KEEP | STM32 pin name |
| `PVC` | 5 | 3 — 00-before-you-start, 09-electronics-bay, 16-glossary | 1 | KEEP | Polyvinyl chloride |
| `QR` | 5 | 4 — 00-before-you-start, 00-index, 06-z-axis-and-gantry-squaring, … | 1 | KEEP | Quick Response code |
| `RAIL` | 5 | 3 — 00a-mains-safety, 09-electronics-bay, 10-wiring | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `RJ45` | 5 | 2 — 10-wiring, 11-skirts-panels-door | 1 | KEEP | Ethernet connector |
| `SIG` | 5 | 2 — 08-toolhead, 10-wiring | 1 | KEEP | Signal pin |
| `TOTAL` | 5 | 2 — README, voron-print-plan | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `US` | 5 | 4 — 00-index, 00a-mains-safety, 09-electronics-bay, … | 1 | KEEP | United States |
| `VAC` | 5 | 4 — 00a-mains-safety, 03-build-plate, 10-wiring, … | 1 | KEEP | Volts, alternating current |
| `VS9` | 5 | 2 — 10-wiring, 13-initial-startup | 1 | KEEP | LDO photo id |
| `W2` | 5 | 4 — 00-index, 01-frame, 05-gantry, … | — | KEEP | Wire / warning id |
| `Y1` | 5 | 3 — 00-before-you-start, 00-tonight, 05-gantry | — | KEEP | G-code coordinate |
| `Y2` | 5 | 3 — 00-before-you-start, 00-tonight, 05-gantry | — | KEEP | G-code coordinate |
| `3V3` | 4 | 3 — 08-toolhead, 12-software, 13-initial-startup | — | KEEP | Part number, size or voltage |
| `4P` | 4 | 2 — 08-toolhead, 10-wiring | — | KEEP | Part number, size or voltage |
| `CAN` | 4 | 2 — 10-wiring, 16-glossary | 1 | KEEP | Controller Area Network |
| `CLAUDE` | 4 | 4 — 00-before-you-start, 00-slicer-setup, 01-frame, … | 1 | KEEP | Filename (CLAUDE.md) |
| `DON` | 4 | 2 — 02-z-drives, 03-build-plate | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `E0` | 4 | 2 — 12-software, 14-calibration | 1 | KEEP | Extruder 0 |
| `E100` | 4 | 2 — 13-initial-startup, 14-calibration | — | KEEP | G-code extruder parameter |
| `F3600` | 4 | 2 — 12-software, 13-initial-startup | — | KEEP | G-code feedrate |
| `G90` | 4 | 2 — 12-software, 14-calibration | — | KEEP | G-code / M-code |
| `G92` | 4 | 2 — 12-software, 14-calibration | — | KEEP | G-code / M-code |
| `GATE` | 4 | 2 — 00-tonight, B00-calibration-and-jigs | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `GB` | 4 | 2 — 09-electronics-bay, 12-software | 1 | KEEP | Gigabyte |
| `IDLER` | 4 | 1 — 04-ab-drives | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `INDX` | 4 | 2 — 00-slicer-setup, voron-print-plan | 1 | KEEP | Prusa INDX toolchanger |
| `M107` | 4 | 2 — 12-software, 13-initial-startup | — | KEEP | G-code / M-code |
| `NEMA14` | 4 | 1 — 08-toolhead | 1 | KEEP | Stepper frame size |
| `PILOT` | 4 | 1 — 02-z-drives | 1 | KEEP | Filename (assets/cad/PILOT.md) |
| `QGLs` | 4 | 4 — 00-index, 06-z-axis-and-gantry-squaring, 13-initial-startup, … | 1 | KEEP | Quad Gantry Level runs |
| `R18` | 4 | 1 — 10-wiring | 1 | KEEP | Drag-chain bend radius |
| `RSP` | 4 | 2 — 09-electronics-bay, 10-wiring | 1 | KEEP | Mean Well PSU series |
| `S2` | 4 | 1 — 10-wiring | 1 | KEEP | LDO photo id |
| `SAVE` | 4 | 2 — 00-tonight, 12-software | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `T10` | 4 | 2 — 00-before-you-start, 05-gantry | 1 | KEEP | Torx driver size |
| `TARGET` | 4 | 3 — 12-software, 13-initial-startup, 14-calibration | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `TEST` | 4 | 1 — 00a-mains-safety | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `W9` | 4 | 2 — 00-before-you-start, 02-z-drives | — | KEEP | Wire / warning id |
| `X5` | 4 | 2 — 12-software, 14-calibration | — | KEEP | G-code coordinate |
| `Z10` | 4 | 2 — 12-software, 13-initial-startup | — | KEEP | Part number or board label |
| `Z30` | 4 | 2 — 12-software, 13-initial-startup | — | KEEP | Part number or board label |
| `3D` | 3 | 2 — 00-before-you-start, 12-software | — | KEEP | Part number, size or voltage |
| `400Z0` | 3 | 3 — 00-before-you-start, 02-z-drives, 05-gantry | — | KEEP | Part number, size or voltage |
| `ACCEPT` | 3 | 1 — 13-initial-startup | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `ACTIVE` | 3 | 1 — 12-software | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `ADDED` | 3 | 1 — 12-software | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `CSVs` | 3 | 2 — 00-tonight, 14-calibration | 1 | KEEP | Comma-separated value files |
| `DHCP` | 3 | 1 — 12-software | 1 | KEEP | Dynamic Host Configuration Protocol |
| `EM` | 3 | 2 — 00-index, 14-calibration | 2 | SPELL OUT | extrusion multiplier. The 3 survivors are the citation *PA / EM Oddities* in Ch 14 and corrections-log row 31, which names the old spelling |
| `EU` | 3 | 2 — 09-electronics-bay, 10-wiring | 1 | KEEP | European Union |
| `HEATER` | 3 | 2 — 12-software, 13-initial-startup | 1 | KEEP | Board port label |
| `I2C` | 3 | 1 — 08-toolhead | 1 | KEEP | Inter-Integrated Circuit bus |
| `KMS` | 3 | 2 — 11-skirts-panels-door, 12-software | 1 | KEEP | Kernel Mode Setting (Linux) |
| `L236` | 3 | 3 — 12-software, 13-initial-startup, 14-calibration | — | KEEP | Source line reference |
| `L308` | 3 | 2 — 12-software, 13-initial-startup | — | KEEP | Source line reference |
| `L458` | 3 | 2 — 12-software, 13-initial-startup | — | KEEP | Source line reference |
| `L47` | 3 | 2 — 12-software, 13-initial-startup | — | KEEP | Source line reference |
| `L471` | 3 | 3 — 12-software, 13-initial-startup, 14-calibration | — | KEEP | Source line reference |
| `M190` | 3 | 2 — 12-software, 13-initial-startup | — | KEEP | G-code / M-code |
| `OK` | 3 | 2 — 13-initial-startup, 14-calibration | 1 | KEEP | Confirmation |
| `PA2` | 3 | 3 — 10-wiring, 12-software, 14-calibration | — | KEEP | STM32 pin name |
| `PB12` | 3 | 3 — 08-toolhead, 12-software, 14-calibration | — | KEEP | STM32 pin name |
| `PD1` | 3 | 3 — 08-toolhead, 12-software, 13-initial-startup | — | KEEP | STM32 pin name |
| `PD13` | 3 | 1 — 11-skirts-panels-door | — | KEEP | STM32 pin name |
| `PD2` | 3 | 3 — 08-toolhead, 12-software, 13-initial-startup | — | KEEP | STM32 pin name |
| `PD3` | 3 | 2 — 08-toolhead, 13-initial-startup | — | KEEP | STM32 pin name |
| `PG0` | 3 | 1 — 12-software | — | KEEP | STM32 pin name |
| `PH1` | 3 | 1 — 09-electronics-bay | — | KEEP | STM32 pin name |
| `PNG` | 3 | 2 — 00-slicer-setup, CONVENTIONS | 1 | KEEP | Portable Network Graphics |
| `PRINT` | 3 | 2 — 00-before-you-start, 03-build-plate | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `Q5MC` | 3 | 1 — 07-ab-belts | 1 | KEEP | Omron probe part code |
| `R28` | 3 | 2 — 06-z-axis-and-gantry-squaring, 10-wiring | 1 | KEEP | Drag-chain bend radius |
| `RGB` | 3 | 1 — 08-toolhead | 1 | KEEP | Red-Green-Blue |
| `SERIAL` | 3 | 1 — 12-software | 1 | KEEP | Board port label / kit serial heading |
| `SLR9H` | 3 | 3 — 00-before-you-start, 02-z-drives, 05-gantry | 1 | KEEP | LDO rail part code |
| `STOP` | 3 | 1 — 10-wiring | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `STRIP` | 3 | 2 — 10-wiring, 12-software | 1 | KEEP | LED-strip port label |
| `TL` | 3 | 1 — 07-ab-belts | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `UART` | 3 | 1 — 10-wiring | 1 | KEEP | Universal Asynchronous Receiver/Transmitter |
| `UI` | 3 | 3 — 00-index, 12-software, 14-calibration | 1 | KEEP | User Interface |
| `V2TR` | 3 | 2 — 16-glossary, B04-xy-joints-and-x-carriage | 1 | KEEP | Voron STL variant (2.4 / Trident shared) |
| `W12` | 3 | 2 — 02-z-drives, 06-z-axis-and-gantry-squaring | — | KEEP | Wire / warning id |
| `W4` | 3 | 1 — 02-z-drives | — | KEEP | Wire / warning id |
| `W5` | 3 | 2 — 10-wiring, 11-skirts-panels-door | — | KEEP | Wire / warning id |
| `W6` | 3 | 1 — 03-build-plate | — | KEEP | Wire / warning id |
| `XX` | 3 | 2 — 00-before-you-start, CONVENTIONS | 1 | KEEP | Numeric placeholder |
| `Y5` | 3 | 2 — 12-software, 14-calibration | — | KEEP | G-code coordinate |
| `220B` | 2 | 1 — 00a-mains-safety | 1 | KEEP | Omron SSR part code |
| `230V` | 2 | 2 — 00a-mains-safety, 10-wiring | — | KEEP | Part number, size or voltage |
| `3MFs` | 2 | 1 — 00-slicer-setup | 1 | KEEP | 3D Manufacturing Format files |
| `400Z1` | 2 | 2 — 00-before-you-start, 05-gantry | — | KEEP | Part number, size or voltage |
| `900M` | 2 | 1 — 00-before-you-start | 1 | KEEP | Hakko tip format |
| `A2` | 2 | 1 — 08-toolhead | 1 | KEEP | Fan tacho pin |
| `AWG` | 2 | 1 — 00a-mains-safety | 1 | KEEP | American Wire Gauge |
| `CHECK` | 2 | 2 — 05-gantry, 10-wiring | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `CI` | 2 | 1 — CONVENTIONS | 1 | KEEP | Continuous Integration |
| `CW1` | 2 | 1 — 08-toolhead | — | KEEP | Part number or board label |
| `DO` | 2 | 1 — 00-before-you-start | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `DRIVE` | 2 | 1 — 04-ab-drives | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `E1` | 2 | 1 — 00a-mains-safety | 1 | KEEP | Extruder 1 |
| `E20` | 2 | 1 — 14-calibration | — | KEEP | G-code extruder parameter |
| `ETA` | 2 | 2 — 00-before-you-start, 00-index | 1 | KEEP | Estimated time of arrival |
| `EXP1` | 2 | 1 — 11-skirts-panels-door | 1 | KEEP | Display header |
| `EXP2` | 2 | 1 — 11-skirts-panels-door | 1 | KEEP | Display header |
| `F1200` | 2 | 2 — 13-initial-startup, 14-calibration | — | KEEP | G-code feedrate |
| `F446` | 2 | 1 — 12-software | 1 | KEEP | STM32 part number |
| `F60` | 2 | 2 — 13-initial-startup, 14-calibration | — | KEEP | Part number or board label |
| `FAN0` | 2 | 2 — 10-wiring, 12-software | 1 | KEEP | Fan port |
| `FAN1` | 2 | 2 — 10-wiring, 12-software | 1 | KEEP | Fan port |
| `FFF` | 2 | 2 — 00-slicer-setup, B00-calibration-and-jigs | 1 | KEEP | Fused Filament Fabrication |
| `FRAME` | 2 | 1 — 10-wiring | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `G29` | 2 | 2 — 00-index, 00-slicer-setup | — | KEEP | G-code / M-code |
| `GRBW` | 2 | 2 — 08-toolhead, 13-initial-startup | 1 | KEEP | Green-Red-Blue-White LED order |
| `H743` | 2 | 1 — 12-software | 1 | KEEP | STM32 part number |
| `HEF` | 2 | 2 — 08-toolhead, 13-initial-startup | 1 | KEEP | Hotend fan header |
| `HFSFB5` | 2 | 1 — 11-skirts-panels-door | 1 | KEEP | Misumi extrusion code |
| `IDGA` | 2 | 1 — 08-toolhead | 1 | KEEP | Bondtech gear-set code |
| `IGUS` | 2 | 2 — 05-gantry, 08-toolhead | 1 | KEEP | Vendor name (igus drag chain) |
| `II` | 2 | 1 — 00a-mains-safety | 1 | KEEP | Roman numeral |
| `J164` | 2 | 1 — 00a-mains-safety | 1 | KEEP | Omron datasheet number |
| `JPEG` | 2 | 1 — CONVENTIONS | 1 | KEEP | Image format |
| `L288` | 2 | 2 — 12-software, 13-initial-startup | — | KEEP | Source line reference |
| `L32` | 2 | 1 — 14-calibration | — | KEEP | Source line reference |
| `L327` | 2 | 2 — 12-software, 13-initial-startup | — | KEEP | Source line reference |
| `L441` | 2 | 2 — 12-software, 14-calibration | — | KEEP | Source line reference |
| `L455` | 2 | 2 — 13-initial-startup, 14-calibration | — | KEEP | Source line reference |
| `L621` | 2 | 2 — 12-software, 14-calibration | — | KEEP | Source line reference |
| `L73` | 2 | 1 — 13-initial-startup | — | KEEP | Source line reference |
| `LAN` | 2 | 2 — 00-index, index | 1 | KEEP | Local Area Network |
| `M104` | 2 | 2 — 12-software, 13-initial-startup | — | KEEP | G-code / M-code |
| `M109` | 2 | 2 — 12-software, 13-initial-startup | — | KEEP | G-code / M-code |
| `MOVE` | 2 | 1 — 13-initial-startup | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `NAME` | 2 | 1 — 12-software | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `NC` | 2 | 1 — 08-toolhead | 1 | KEEP | Normally closed |
| `NEMA17` | 2 | 1 — 02-z-drives | 1 | KEEP | Stepper frame size |
| `NNN` | 2 | 1 — CONVENTIONS | 1 | KEEP | Numeric placeholder |
| `NTC` | 2 | 1 — 08-toolhead | 1 | KEEP | Negative Temperature Coefficient thermistor |
| `P01` | 2 | 2 — 01-frame, 04-ab-drives | — | KEEP | Plate number / manual page id |
| `P04` | 2 | 1 — 04-ab-drives | — | KEEP | Plate number / manual page id |
| `P9` | 2 | 2 — 00-index, 00-slicer-setup | — | KEEP | Plate number / manual page id |
| `PA7` | 2 | 2 — 12-software, 13-initial-startup | — | KEEP | STM32 pin name |
| `PB10` | 2 | 2 — 12-software, 14-calibration | — | KEEP | STM32 pin name |
| `PB9` | 2 | 1 — 13-initial-startup | — | KEEP | STM32 pin name |
| `PCF` | 2 | 2 — 08-toolhead, 13-initial-startup | 1 | KEEP | Part-cooling fan header |
| `S255` | 2 | 2 — 12-software, 13-initial-startup | — | KEEP | G-code parameter / LDO photo id |
| `S3` | 2 | 1 — 10-wiring | 1 | KEEP | LDO photo id |
| `SENSOR` | 2 | 1 — 12-software | 1 | KEEP | Board port label |
| `SHA` | 2 | 2 — 12-software, voron-print-plan | 1 | KEEP | Secure Hash Algorithm |
| `SKU` | 2 | 2 — 00-before-you-start, 00-index | 1 | KEEP | Stock-keeping unit |
| `SLR12H` | 2 | 2 — 00-before-you-start, 05-gantry | 1 | KEEP | LDO rail part code |
| `SPEC` | 2 | 1 — 00a-mains-safety | 1 | KEEP | Word in a quoted label |
| `STM` | 2 | 1 — 12-software | 1 | KEEP | STMicroelectronics |
| `SW2` | 2 | 1 — 12-software | 1 | KEEP | Board switch label |
| `TFT43` | 2 | 1 — 11-skirts-panels-door | 1 | KEEP | BTT TFT4.3 display |
| `U6` | 2 | 1 — 00-slicer-setup | 1 | KEEP | Firmware version string |
| `URLs` | 2 | 2 — 08-toolhead, CONVENTIONS | 1 | KEEP | Uniform Resource Locators |
| `USS` | 2 | 2 — 00-slicer-setup, voron-print-plan | 1 | KEEP | Prusa product name (USS Drybox) |
| `VDC` | 2 | 2 — 00a-mains-safety, 16-glossary | 1 | KEEP | Volts, direct current |
| `W11` | 2 | 1 — 11-skirts-panels-door | — | KEEP | Wire / warning id |
| `W13` | 2 | 2 — 00-index, 13-initial-startup | — | KEEP | Wire / warning id |
| `W14` | 2 | 2 — 00-index, 13-initial-startup | — | KEEP | Wire / warning id |
| `WITH` | 2 | 2 — 11-skirts-panels-door, 12-software | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `X0` | 2 | 1 — 13-initial-startup | — | KEEP | G-code coordinate |
| `X120` | 2 | 1 — 14-calibration | — | KEEP | G-code coordinate |
| `Y0` | 2 | 1 — 13-initial-startup | — | KEEP | G-code coordinate |
| `YOUR` | 2 | 2 — 05-gantry, 12-software | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `YYMMDD` | 2 | 2 — 00-before-you-start, 15-troubleshooting | 1 | KEEP | Date placeholder in the kit serial |
| `ZH1` | 2 | 2 — 08-toolhead, 16-glossary | 1 | KEEP | JST-ZH 1.5 mm connector |
| `115V` | 1 | 1 — 10-wiring | — | KEEP | Part number, size or voltage |
| `150C` | 1 | 1 — 12-software | — | KEEP | Part number, size or voltage |
| `240B` | 1 | 1 — 00a-mains-safety | 1 | KEEP | Omron SSR part code |
| `340E` | 1 | 1 — 00-before-you-start | — | KEEP | Part number, size or voltage |
| `3P` | 1 | 1 — 10-wiring | — | KEEP | Part number, size or voltage |
| `430D` | 1 | 1 — 00-before-you-start | — | KEEP | Part number, size or voltage |
| `450C` | 1 | 1 — 00-before-you-start | — | KEEP | Part number, size or voltage |
| `470A` | 1 | 1 — 00-before-you-start | — | KEEP | Part number, size or voltage |
| `4R2` | 1 | 1 — voron-print-plan | — | KEEP | Part number, size or voltage |
| `530B` | 1 | 1 — 00-before-you-start | — | KEEP | Part number, size or voltage |
| `5L` | 1 | 1 — 08-toolhead | — | KEEP | Part number, size or voltage |
| `5P` | 1 | 1 — 08-toolhead | — | KEEP | Part number, size or voltage |
| `60W` | 1 | 1 — 12-software | — | KEEP | Part number, size or voltage |
| `70E` | 1 | 1 — 00a-mains-safety | — | KEEP | Part number, size or voltage |
| `A4` | 1 | 1 — 13-initial-startup | — | KEEP | Part number or board label |
| `ABORT` | 1 | 1 — 13-initial-startup | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `AND` | 1 | 1 — voron-print-plan | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `ANY` | 1 | 1 — 12-software | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `ARE` | 1 | 1 — voron-print-plan | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `AWG26` | 1 | 1 — 08-toolhead | 1 | KEEP | American Wire Gauge 26 |
| `AXIS` | 1 | 1 — 14-calibration | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `B1` | 1 | 1 — 08-toolhead | 1 | KEEP | Stepper coil pin |
| `B2` | 1 | 1 — 08-toolhead | 1 | KEEP | Stepper coil pin |
| `BE` | 1 | 1 — 10-wiring | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `BEFORE` | 1 | 1 — 10-wiring | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `BLDC` | 1 | 1 — 13-initial-startup | 1 | KEEP | Brushless DC motor |
| `BLUE` | 1 | 1 — 13-initial-startup | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `BNN` | 1 | 1 — CONVENTIONS | 1 | KEEP | Batch-number placeholder |
| `BOLT` | 1 | 1 — 05-gantry | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `BOOT` | 1 | 1 — 08-toolhead | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `BY` | 1 | 1 — 10-wiring | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `DAMAGE` | 1 | 1 — 10-wiring | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `DIR` | 1 | 1 — CONVENTIONS | 1 | KEEP | Stepper direction pin |
| `DOORS` | 1 | 1 — 11-skirts-panels-door | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `DOUT` | 1 | 1 — 08-toolhead | 1 | KEEP | LED data-out pad |
| `EP1` | 1 | 1 — 02-z-drives | — | KEEP | Part number or board label |
| `EP2` | 1 | 1 — 02-z-drives | — | KEEP | Part number or board label |
| `EXIF` | 1 | 1 — CONVENTIONS | 1 | KEEP | Image metadata |
| `F4` | 1 | 1 — 00-index | 1 | KEEP | STM32 family |
| `F5` | 1 | 1 — 00-index | 1 | KEEP | Part code |
| `F600` | 1 | 1 — 14-calibration | — | KEEP | G-code feedrate |
| `F7` | 1 | 1 — 00-index | 1 | KEEP | STM32 family |
| `FX888D` | 1 | 1 — 00-before-you-start | 1 | KEEP | Hakko soldering station |
| `G21` | 1 | 1 — 12-software | — | KEEP | G-code / M-code |
| `G3NA` | 1 | 1 — 00a-mains-safety | 1 | KEEP | Omron SSR series |
| `G4` | 1 | 1 — 12-software | — | KEEP | G-code / M-code |
| `GPS` | 1 | 1 — CONVENTIONS | 1 | KEEP | Global Positioning System |
| `GREEN` | 1 | 1 — 13-initial-startup | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `HA2` | 1 | 1 — 09-electronics-bay | — | KEEP | Part number or board label |
| `HEIC` | 1 | 1 — CONVENTIONS | 1 | KEEP | Image format |
| `HTML` | 1 | 1 — 12-software | 1 | KEEP | HyperText Markup Language |
| `HUB` | 1 | 1 — 12-software | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `INFO` | 1 | 1 — CONVENTIONS | 1 | KEEP | Log level |
| `IP` | 1 | 1 — 12-software | 1 | KEEP | Internet Protocol |
| `KLICKY` | 1 | 1 — B06-toolhead-sb-cw2-klicky | 1 | KEEP | Klicky probe |
| `L1` | 1 | 1 — 12-software | — | KEEP | Source line reference |
| `L133` | 1 | 1 — 12-software | — | KEEP | Source line reference |
| `L18` | 1 | 1 — 12-software | — | KEEP | Source line reference |
| `L337` | 1 | 1 — 13-initial-startup | — | KEEP | Source line reference |
| `L348` | 1 | 1 — 13-initial-startup | — | KEEP | Source line reference |
| `L351` | 1 | 1 — 12-software | — | KEEP | Source line reference |
| `L384` | 1 | 1 — 13-initial-startup | — | KEEP | Source line reference |
| `L411` | 1 | 1 — 14-calibration | — | KEEP | Source line reference |
| `L418` | 1 | 1 — 12-software | — | KEEP | Source line reference |
| `L601` | 1 | 1 — 12-software | — | KEEP | Source line reference |
| `L723` | 1 | 1 — 13-initial-startup | — | KEEP | Source line reference |
| `L746` | 1 | 1 — 13-initial-startup | — | KEEP | Source line reference |
| `LCD` | 1 | 1 — 11-skirts-panels-door | 1 | KEEP | Liquid-Crystal Display |
| `LCH` | 1 | 1 — 11-skirts-panels-door | 1 | KEEP | Misumi end-machining code |
| `LEAVE` | 1 | 1 — 05-gantry | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `LOOSE` | 1 | 1 — 05-gantry | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `M105` | 1 | 1 — 14-calibration | — | KEEP | G-code / M-code |
| `M115` | 1 | 1 — 00-slicer-setup | — | KEEP | G-code / M-code |
| `M140` | 1 | 1 — 12-software | — | KEEP | G-code / M-code |
| `M141` | 1 | 1 — 13-initial-startup | — | KEEP | G-code / M-code |
| `M191` | 1 | 1 — 13-initial-startup | — | KEEP | G-code / M-code |
| `MAINS` | 1 | 1 — 09-electronics-bay | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `MAY` | 1 | 1 — CONVENTIONS | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `MGN9s` | 1 | 1 — 02-z-drives | 1 | KEEP | Linear rails |
| `MIC6` | 1 | 1 — 03-build-plate | 1 | KEEP | Cast aluminium plate grade |
| `N35` | 1 | 1 — 08-toolhead | 1 | KEEP | Magnet grade |
| `NFPA` | 1 | 1 — 00a-mains-safety | 1 | KEEP | National Fire Protection Association |
| `ONLY` | 1 | 1 — 05-gantry | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `OPTION` | 1 | 1 — 08-toolhead | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `OUT` | 1 | 1 — 08-toolhead | 1 | KEEP | Terminal label |
| `P00` | 1 | 1 — 00-before-you-start | — | KEEP | Plate number / manual page id |
| `P05` | 1 | 1 — 05-gantry | — | KEEP | Plate number / manual page id |
| `P07` | 1 | 1 — 07-ab-belts | — | KEEP | Plate number / manual page id |
| `P11` | 1 | 1 — 11-skirts-panels-door | — | KEEP | Plate number / manual page id |
| `P12` | 1 | 1 — 12-software | — | KEEP | Plate number / manual page id |
| `P13` | 1 | 1 — 13-initial-startup | — | KEEP | Plate number / manual page id |
| `P1R` | 1 | 1 — README | — | KEEP | Part number or board label |
| `P6` | 1 | 1 — 00-index | — | KEEP | Plate number / manual page id |
| `PA5` | 1 | 1 — 14-calibration | — | KEEP | STM32 pin name |
| `PA6` | 1 | 1 — 14-calibration | — | KEEP | STM32 pin name |
| `PAUSE` | 1 | 1 — 12-software | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `PB0` | 1 | 1 — 08-toolhead | — | KEEP | STM32 pin name |
| `PB1` | 1 | 1 — 08-toolhead | — | KEEP | STM32 pin name |
| `PB11` | 1 | 1 — 12-software | — | KEEP | STM32 pin name |
| `PB3` | 1 | 1 — 08-toolhead | — | KEEP | STM32 pin name |
| `PB4` | 1 | 1 — 08-toolhead | — | KEEP | STM32 pin name |
| `PC1` | 1 | 1 — 12-software | — | KEEP | STM32 pin name |
| `PC14` | 1 | 1 — 13-initial-startup | — | KEEP | STM32 pin name |
| `PCBs` | 1 | 1 — 11-skirts-panels-door | 1 | KEEP | Printed Circuit Boards |
| `PE1` | 1 | 1 — 12-software | — | KEEP | STM32 pin name |
| `PF6` | 1 | 1 — 12-software | — | KEEP | STM32 pin name |
| `PFC` | 1 | 1 — 09-electronics-bay | 1 | KEEP | Power Factor Correction |
| `PG11` | 1 | 1 — 12-software | — | KEEP | STM32 pin name |
| `PH` | 1 | 1 — 00-before-you-start | 1 | KEEP | JST-PH connector series |
| `PI` | 1 | 1 — 09-electronics-bay | 1 | KEEP | Raspberry Pi |
| `PIF` | 1 | 1 — 16-glossary | 3 | KEEP | Glossary § P |
| `PIN` | 1 | 1 — 13-initial-startup | 1 | KEEP | Personal identification number / pin |
| `PNGs` | 1 | 1 — 14-calibration | 1 | KEEP | Portable Network Graphics files |
| `POWER` | 1 | 1 — 10-wiring | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `PWR` | 1 | 1 — 12-software | 1 | KEEP | Power LED |
| `RC` | 1 | 1 — 16-glossary | 1 | KEEP | Resistor-capacitor snubber |
| `RCH` | 1 | 1 — 11-skirts-panels-door | 1 | KEEP | Misumi end-machining code |
| `RED` | 1 | 1 — 13-initial-startup | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `RESUME` | 1 | 1 — 12-software | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `RPM` | 1 | 1 — 08-toolhead | 1 | KEEP | Revolutions per minute |
| `RS` | 1 | 1 — 09-electronics-bay | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `RS25` | 1 | 1 — 09-electronics-bay | 1 | KEEP | Part code |
| `S0` | 1 | 1 — 10-wiring | — | KEEP | G-code parameter / LDO photo id |
| `S150` | 1 | 1 — 12-software | — | KEEP | G-code parameter / LDO photo id |
| `S64` | 1 | 1 — 13-initial-startup | — | KEEP | G-code parameter / LDO photo id |
| `SCL` | 1 | 1 — 08-toolhead | 1 | KEEP | I2C clock line |
| `SDA` | 1 | 1 — 08-toolhead | 1 | KEEP | I2C data line |
| `SHA256` | 1 | 1 — 00-slicer-setup | 1 | KEEP | Secure Hash Algorithm, 256-bit |
| `SOAK` | 1 | 1 — 12-software | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `SPI` | 1 | 1 — 14-calibration | 1 | KEEP | Serial Peripheral Interface |
| `SSID` | 1 | 1 — 12-software | 1 | KEEP | Wi-Fi network name |
| `SWITCH` | 1 | 1 — 10-wiring | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `T1` | 1 | 1 — 14-calibration | 1 | KEEP | Tool 1 |
| `TAP` | 1 | 1 — 08-toolhead | 1 | KEEP | Voron Tap probe |
| `TBD` | 1 | 1 — CONVENTIONS | 1 | KEEP | To be determined |
| `TEMP` | 1 | 1 — 13-initial-startup | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `THIS` | 1 | 1 — CONVENTIONS | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `TPW` | 1 | 1 — 11-skirts-panels-door | 1 | KEEP | Misumi end-machining code |
| `VALUE` | 1 | 1 — 13-initial-startup | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `W7` | 1 | 1 — 08-toolhead | — | KEEP | Wire / warning id |
| `WHITE` | 1 | 1 — 13-initial-startup | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `WORK` | 1 | 1 — 05-gantry | — | KEEP | All-caps word in prose or a quoted UI/silkscreen label, not an acronym |
| `Y10` | 1 | 1 — 13-initial-startup | — | KEEP | G-code coordinate |
| `YAML` | 1 | 1 — 00-slicer-setup | 1 | KEEP | Config format |
| `Z50` | 1 | 1 — 13-initial-startup | — | KEEP | Part number or board label |
| `ZH` | 1 | 1 — 00-before-you-start | 1 | KEEP | JST-ZH connector series |

