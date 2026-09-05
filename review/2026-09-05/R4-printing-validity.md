# R4 — Printing chapters & print plan vs live STL repos + PrusaSlicer

### F1 · BLOCKER · docs/manual/print/00-slicer-setup.md:124 (also B00:64, B00:87, B01:31, B01:78, B01:94, B01:95)
Claim in doc: "`z_drive_retainer_a` F695 bore (same plate) | 13.00 mm bearing | bearing presses in with thumb pressure… **The real press-fit gate.**"
Source checked: Assembly_Manual_2.4r2.pdf p.8 "625 BEARING — A ball bearing used on the Voron Z drives"; p.32–33 BELT DRIVE ASSEMBLY shows 3× 625 Bearing; F695 appears only on p.65/69/74/78/97/99 (A/B idler, A/B drive, XY joints). LDO Rev D 350 BOM: 625-2RS ×12 = exactly 4 Z drives × 3.
Problem: The whole dimensional gate — and the B01 bearing-seat check — names the wrong bearing (F695, 13 mm OD) for a seat that takes a 625-2RS (16 mm OD), so the builder tests a 16 mm bore with a 13 mm bearing, sees it rattle, and "fixes" the profile (extrusion multiplier / compensation) before any real part is printed.
Fix: Replace every "F695"/"13 mm"/"13.00 mm" in 00-slicer-setup.md:124, B00:64,87 and B01:31,78,94,95 with "625-2RS (16 mm OD)". The print plan already has this right at docs/voron-print-plan.md:182 and :671 — copy that wording verbatim.

### F2 · MAJOR · docs/manual/print/B03-ab-drive-units-and-front-idlers.md:24,60,62,74 (also docs/voron-print-plan.md:673)
Claim in doc: "Checkpoint after B03: **625 bearing seats** in the drive frames"; "check the 625 bearing seat diameter in each drive frame half".
Source checked: Assembly_Manual_2.4r2.pdf p.74 "A DRIVE — M5 Shim, **F695 Bearing**", p.78 "B DRIVE — F695 Bearing", p.65/69 A/B IDLER — F695. No page in the A/B chapter mentions a 625.
Problem: The A/B drive-frame bearing is F695 (13 mm OD, flanged), not 625 — F1 and F2 are the same two bearings swapped, so a builder following both chapters will test both seats with the wrong bearing.
Fix: In B03:24,60,62,74 and voron-print-plan.md:673 replace "625 bearing" with "F695-2RS (13 mm OD, flanged)".

### F3 · MAJOR · docs/manual/print/B07-electronics-bay-and-lighting.md:64–69 (Step B07.4) / docs/voron-print-plan.md:444
Claim in doc: "Slice `cob_light_strip_mount_100mm` ×6 and `cob_light_strip_mount_50mm` ×2 … plus `power_inlet_IECGS_1mm` … **Brim the 100 mm mounts and the power inlet**. Parts: … 9.6 h, 163 g."
Source checked: Mesh bboxes from the live STLs — cob_100mm 45.43×100.0, cob_50mm 45.43×50.0, power_inlet_IECGS_1mm 118.0×66.8. Bed = 250×220 (PrusaResearch.ini v2.9.6, `printer:Prusa CORE One 0.4 nozzle`, `bed_shape = 0x0,250x0,250x220,0x220`). MaxRects packing (rotation allowed, 0 mm gap): with the mandated 3 mm brims the set is 46 280 mm² = 84 % of the bed and **cannot be placed**; without brims it fits, but the best packing at a 3 mm gap uses 219.7 × 217.9 mm — 2.1 mm of spare Y.
Problem: As specified (six 100 mm mounts + two 50 mm + power inlet, all brimmed) B07-P2 does not fit a 250×220 plate, so the plate count (26), the 9.6 h figure and the schedule are wrong.
Fix: Split B07-P2: keep the eight COB mounts on B07-P2 (brimmed; fits) and move `power_inlet_IECGS_1mm` to its own plate B07-P3 (~2.1 h, 36 g). Update B07 to 3 plates and the totals to 27 plates. Delete the "add wherever it fits on the plate, verify in slicer" hedge.

### F4 · MAJOR · docs/manual/print/B08-skirts-and-front-modules.md:60,62 (Step B08.2) / docs/voron-print-plan.md:480
Claim in doc: "Slice `rear_center_skirt_350`, `side_fan_support` ×1. Apply 3 mm brim to both. **Check:** Brim applied; **parts not rotated**." (00-slicer-setup.md:134 "Do not rotate anything.")
Source checked: Mesh bboxes — rear_center_skirt_350 = 182.00 × 66.80; side_fan_support_x2.STL = 72.00 × **180.02**. Side by side needs 254 mm of X (>250); stacked needs 246.8 mm of Y (>220). MaxRects: no fit at any brim/gap setting without an in-plane 90° rotation; with one part rotated it fits at 156.8 × 191 mm even with 3 mm brims.
Problem: B08-P1 is impossible in the as-shipped in-plane orientations, and the chapter explicitly forbids rotating, so the builder hits "outside print area" with no sanctioned fix.
Fix: In 00-slicer-setup.md:134 change "Do not rotate anything" to "Do not change which face sits on the bed. Rotating about Z to fit the plate is fine." In B08.2 add: "Rotate `side_fan_support` 90° about Z (180 mm along X) — it will not fit beside the rear skirt otherwise", and drop "parts not rotated" from the Check.

### F5 · MAJOR · docs/manual/print/00-slicer-setup.md:11 (also B00:29, docs/voron-print-plan.md:103)
Claim in doc: "Printer: **`Original Prusa CORE One 0.4 nozzle`** — bed 250×220, max height 270 … (verified against `PrusaResearch.ini` @ `version_2.9.6`)"
Source checked: github.com/prusa3d/PrusaSlicer @ version_2.9.6 `resources/profiles/PrusaResearch.ini` — the section is `[printer:Prusa CORE One 0.4 nozzle]`; the string "Original Prusa CORE" occurs **0 times** in the file (also 0 in the current live bundle PrusaResearch/2.5.8.ini). `[printer_model:COREONE] name = Prusa CORE One && CORE One+`.
Problem: The printer preset name in the doc does not exist — the CORE One family dropped the "Original" prefix — so the builder searches a dropdown for a profile that isn't there.
Fix: Replace all three occurrences of "Original Prusa CORE One 0.4 nozzle" with "Prusa CORE One 0.4 nozzle" (model shown as "Prusa CORE One & CORE One+"). Every other value on that line (250×220, 270, retract 0.7 @ 45, z-hop 0.2, wipe off) is correct.

### F6 · MAJOR · docs/manual/print/00-slicer-setup.md:93–103 (STL source of truth) / docs/voron-print-plan.md:60–70
Claim in doc: Nine-row "Download these exact trees" table, row 5 "Nitehawk-SB | `MotorDynamicsLab/Nitehawk-SB` branch `master` | `/STLs`" — no Nitehawk-SB-V2 row.
Source checked: B07 line 18 requires `usb_adapter_mount_partial_cover.stl` from "Nitehawk-SB-V2 `STLs/`". That file exists only at github.com/MotorDynamicsLab/Nitehawk-SB-V2 @ `master` → `STLs/usb_adapter_mount_partial_cover.stl` (verified via the git trees API; the repo's whole STLs dir is that one file).
Problem: A required B07 part lives in a repo the "download these exact trees" table never lists, so a builder who follows the setup chapter literally will not have the file.
Fix: Add a row: "5b | Nitehawk-SB V2 (Rev D+ USB cover) | `MotorDynamicsLab/Nitehawk-SB-V2` branch `master` | `/STLs`" to both tables.

### F7 · MAJOR · docs/manual/print/00-slicer-setup.md:6 (whole chapter)
Claim in doc: "**Slicer:** PrusaSlicer **2.9.6** (current stable, released 2026-06-25). 3.0.0 is alpha — do not use it." — and nothing else about 3.0.
Source checked: PrusaSlicer releases API — `version_3.0.0-alpha11` published 2026-09-01 (prerelease), `version_2.9.6` 2026-06-25 (stable) — both statements true. But CLAUDE.md (2026-09-05) now says Alex will probably use the 3.0.0-preview and "the slicer chapter targets 2.9.6 and **must carry a 3.0 mapping/posture section**".
Problem: The chapter has no 3.0 section, so the concrete 2.9.6→3.0 deltas are undocumented (see Fix for the verified list).
Fix: Add a "PrusaSlicer 3.0 preview" section stating: profiles moved from one `PrusaResearch.ini` to per-preset YAML under `resources/presets/prusa-research-fff/PrusaResearch/`; **`filament_shrinkage_compensation_xy/z` for ASA on CORE One is still 0.22 %** (`preset-filament-common.yaml` id `*shrinkage_ASA*`, `condition: printer.base_model=~/(COREONE|COREONE_INDX)/`) — the zeroing override is unchanged; `0.20mm STRUCTURAL @COREONE 0.4` exists under the same name; in 3.0 its `bottom_solid_layers` default is **3**, not 4 (the "set to 5" action is unchanged); `support_material` is now one enum (CORE One base value `enforcers_only`) replacing the 2.x `support_material` + `support_material_auto` pair — set it to `none`; the printer is picked as the model "Prusa CORE One & CORE One+" with the nozzle chosen per-tool, not as a "…0.4 nozzle" preset; extrusion-width auto/percent values now resolve against nozzle diameter instead of layer height (harmless here — every width in the table is an explicit mm value).

### F8 · MAJOR · docs/manual/print/B10-clicky-clack-door.md:37,50 (also 00-slicer-setup.md:140, B02 common-mistakes)
Claim in doc: "**Mirror the two `Hinge-L-*` parts in the slicer** if you want the door to swing the other way." / "Mirror the `Hinge-L-*` parts now if you want the door to swing the opposite way."
Source checked: PrusaSlicer 3.0.0-alpha11 release notes, "What is in the queue?" → 🚧 Others: "Post processing scripts, Custom G-code editor, Sequential arrange, 3Dconnexion mouse support, **Mirroring**, Accessibility…" — mirroring is not implemented in the 3.0 preview. Separately, `resources/localization/PrusaSlicer.pot` @ 3.0.0-alpha11 contains **no** "Import Config"/"Import Config Bundle"/"Export Config" strings (2.9.6's .pot has all of them); only "Configuration Wizard", "Check for Config Updates", "Show Configuration Folder", "Save preset".
Problem: On 3.0 the mirror step cannot be performed at all, and a 2.9.6 `.ini` config/bundle carrying the Voron overrides cannot be imported into 3.0 — both are silent workflow breaks for the version Alex plans to use.
Fix: In the new 3.0 section: "3.0 preview cannot mirror — if you want the reversed door swing, slice B10 in 2.9.6, or mirror the STL outside the slicer. 3.0 has no Import Config / Config Bundle: carry settings over by saving a 2.x **3MF project** (3.0 imports 2.x project configs and maps them to system presets) and re-enter the overrides once in 3.0. A 3.0 project opened in 2.9.6 loads geometry only — the configuration is discarded (2.9.1+ warns)."

### F9 · MINOR · docs/manual/print/B01-z-drive-assemblies.md:69 (Step B01.5 Check)
Claim in doc: "**Check:** All **12** deck-support clips accounted for on the plate."
Source checked: Same chapter, table line 21 and step line 66: `deck_support_4mm_x8.stl`, qty **8**, "deck_support_4mm ×8"; docs/voron-print-plan.md:254 also 8.
Problem: The check asks for 12 of a part the same chapter says to print 8 of.
Fix: "All 8 deck-support clips accounted for on the plate."

### F10 · MINOR · docs/manual/print/B02-accent-parts-orange.md:101,132 (also docs/voron-print-plan.md:310)
Claim in doc: "Parts: the 16 files above (**25 small accent parts**) — 6.5 h, 106 g" / "All 25 small accent parts present and sorted".
Source checked: Counting the 16 files listed in Step B02.6 with their table quantities: 2+2+4+2+1+1+1+4+4+1+1+1+1+1+2+1 = **29** pieces (49 accent parts total − 7 on P1 − 13 on P2 = 29).
Problem: The piece count is 29, not 25; the "16 files" and the 6.5 h / 106 g figures are correct.
Fix: Replace "25 small accent parts" with "29 small accent parts" in B02:101, B02:132 and voron-print-plan.md:310.

### F11 · MINOR · docs/manual/print/00-slicer-setup.md:184 (also docs/voron-print-plan.md:764)
Claim in doc: "the dimensional gate must be re-passed before printing **473 g** of skirts (B08)."
Source checked: Same repo — B08 totals are 437 g (README.md:11, voron-print-plan.md:461 and :786, and the per-plate sum 105+74+78+74+76+30 = 437).
Problem: Digit transposition — 473 vs 437.
Fix: "…before printing 437 g of skirts (B08)." in both files.

### F12 · MINOR · docs/voron-print-plan.md:683
Claim in doc: "Budget your **465 g** of black margin against those."
Source checked: Same document, §4.2 line 609 and line 613, and README.md:18 — margin is 2400 − 1940 = **460 g**.
Problem: Inconsistent margin figure inside the same document.
Fix: "Budget your 460 g of black margin against those."

### F13 · MINOR · docs/voron-print-plan.md:628 (also docs/manual/print/B07-…:44, README.md:18)
Claim in doc: "With 800 g spools, **spool #1 runs out inside B7**, spool #2 inside B8/B9."
Source checked: The document's own cumulative list (line 625–626): B5 **716** g, B6 **878** g — 800 g is crossed during **B6**, not B7. (Spool #2: B8 1538 → B9 1860 crosses 1600 in B9, so "B8/B9" is fine.)
Problem: Sends the builder to stage a fresh spool one batch late; B07.1 repeats it as an instruction.
Fix: "spool #1 runs out inside B6, spool #2 inside B9" in voron-print-plan.md:628, README.md:18, and B07-electronics-bay-and-lighting.md:44.

### F14 · MINOR · docs/manual/print/B07-electronics-bay-and-lighting.md:19 (also docs/voron-print-plan.md:437)
Claim in doc: "`pcb_din_clip_x3.stl` | Voron-2 `STLs/Electronics_Bay/` | **1 file = 3 clips** *(spares; kit supplies 4)*"
Source checked: Mesh of the live file — a **single connected shell**, 17.60 × 62.00 × 10.00 (union-find over shared vertices, 1308 tris → 1 component). LDO Rev D printed-parts guide: "Four `pcb_din_clips` are provided in the kits. One is used to work with Nitehawk adapter PCB mount. Two are used to install the Leviathan board." → 3 needed, matching the `_x3` = print-3 convention the same doc states at 00-slicer-setup.md:79.
Problem: The file is one clip, not three; printing "1 file" yields 1 spare, and the row contradicts the chapter's own `_x#` rule.
Fix: "`pcb_din_clip_x3.stl` | Voron-2 `STLs/Electronics_Bay/` | 3 *(spares; kit supplies the 4 needed)* | Black | 5.9 g ea" — or drop it, since the kit already covers all four.

### F15 · MINOR · docs/manual/print/00-slicer-setup.md:81–85 (multi-body list)
Claim in doc: "Files confirmed to contain more than one body: `[a]_stealthburner_main_body` (7), `cw2_captive_pcb_cover` (2), `usb_adapter_mount` (2), `Leviathan_bracket_set` (2), `bottom_panel_hinge_x2` (2), `cob_light_strip_mount_*` (2), `V2_Duo_Plenum` (2)."
Source checked: Shell counts recomputed from the live meshes for all 66 downloaded parts — all seven listed counts confirmed exactly, **plus** `usb_adapter_mount_partial_cover.stl` (Nitehawk-SB-V2) = **2** bodies, which is printed in B07 but is missing from the list.
Problem: An omission in an otherwise-correct list, and `Leviathan_bracket_set` is listed although it is not in `MotorDynamicsLab/LDOVoron2` at all (it is supplied printed, so nothing to check).
Fix: Add "`usb_adapter_mount_partial_cover` (2)" to the list.

### F16 · MINOR · docs/manual/print/00-slicer-setup.md:158–159 (also B08:78, voron-print-plan.md:663)
Claim in doc: "Parts with **built-in supports to break out, not cut**: `[a]_stealthburner_main_body`, **the skirt front covers**, `Regular_Cartridge` (Nevermore), `V2_Duo_Plenum`." / B08.5 Check: "Front skirt's built-in support intact, not suppressed in slicer."
Source checked: `[a]_stealthburner_main_body` = 7 shells ✓, `V2_Duo_Plenum` = 2 shells ✓. `front_skirt_a_350`, `front_skirt_b_350`, `rear_center_skirt_350`, `side_skirt_a/b_350_x2`, `side_fan_support_x2` are all **single-shell** meshes, and no file in this build is named "skirt front cover".
Problem: The builder is told to look for and preserve a separate break-away body on the front skirts that does not exist as one.
Fix: Drop "the skirt front covers" from the list and replace B08.5's Check with "Front skirt's first layer clean across the full 150 mm; no corner lift."

### F17 · MINOR · docs/manual/print/B02-accent-parts-orange.md:26,42,43 (colour key at 00-slicer-setup.md:73–79)
Claim in doc: Colour key — "`[a]_` | Accent colour | Prusament ASA Prusa Orange" — with no stated exceptions; B02 then lists `XY_cable_chain_bridge-Igus-3mm_backer.stl`, `ldo_bestagon_insert.stl` and `Handle.stl` (no `[a]_` prefix) as Orange.
Source checked: Assembly_Manual_2.4r2.pdf p.5 and docs.vorondesign.com/sourcing.html — "[a]" marks accent parts; the three files above come from third-party repos that don't use the convention. A full audit of every batch table found no `[a]_` part printed black and no `[o]_` part printed orange.
Problem: Three deliberate accent-colour exceptions are never declared, so the colour rule and the tables appear to disagree.
Fix: Append to the colour key: "Three non-Voron parts are also printed orange by choice: `Handle.stl` (Clicky-Clack), `ldo_bestagon_insert.stl`, and `XY_cable_chain_bridge-Igus-3mm_backer.stl` (a remix of the accent `[a]_xy_joint_cable_bridge_2hole`)."

### F18 · MINOR · docs/manual/print/B08-skirts-and-front-modules.md:12,138,143 (also docs/voron-print-plan.md:464,489)
Claim in doc: "nine segments plus three 'module' segments sharing the same **67×20 mm cross-section**"; "All **nine** structural segments plus TFT mount labelled by ring position"; "every one is 118–182 mm on its long axis and **67 mm deep**."
Source checked: Mesh bboxes — `side_fan_support_x2.STL` is 72.00 × 180.02 × 20.00, i.e. **72 mm** deep, not 67. B08 prints 10 structural segments (rear ×1, front ×2, side_skirt_a ×2, side_skirt_b ×2, side_fan_support ×2, keystone_panel ×1), not nine.
Problem: Two small counting/dimension errors in the ring description and the binning checklist.
Fix: "…sharing a 67–72 × 20 mm cross-section"; "All **ten** structural segments plus TFT mount"; "118–182 mm on its long axis and 67–72 mm deep."

### F19 · MINOR · docs/voron-print-plan.md:698 and :48–50
Claim in doc: "Rev D+ printed-parts guide | Doesn't exist… | **Confirm on Fabreeko Discord that D+ is electrical-only**" / "**Not verified:** … The Rev D guide is being used on the strength of Fabreeko's statement that D+ is a Nitehawk firmware/USB change."
Source checked: Project CLAUDE.md (updated 2026-09-05): "**Rev D+ = Rev D + Nitehawk-SB V2** (electrical + one STL: `usb_adapter_mount_partial_cover`) — **confirmed, not electrical-only**; LDO documented the V2 ESD/grounding scheme 2026-07-10 (manual Ch 10 step 10.58)."
Problem: A resolved open item is still listed as unverified, and "electrical-only" is now the wrong framing (there is a printed-part change, which the plan itself already handles in B07).
Fix: Replace both notes with: "Resolved — Rev D+ = Rev D + Nitehawk-SB V2: electrical plus one printed part (`usb_adapter_mount_partial_cover`, B07). The Rev D printed-parts guide applies for everything else."

### F20 · MINOR · docs/manual/print/B01-z-drive-assemblies.md:23–26 / docs/voron-print-plan.md:260–264, 692
Claim in doc: "Print `deck_support_4mm_x8` now; measure the deck panel on arrival — if it's 3 mm, print `deck_support_3mm_x8` instead."
Source checked: LDO Rev D printed-parts guide: "Our kit ships with **4mm** deck panels, using 4mm deck support clips will help prevent the deck from potential sagging." LDO Rev D **350** BOM: "Deck Panel, Acrylic, Black, 469x469x**3**mm" (the 4 mm panel is the bottom panel — the BOM's Bottom Panel line is 469x469x4mm). The plan's own §0 panel row already states "Deck 3 mm acrylic" from that BOM.
Problem: The conflict is reported accurately, but the default chosen (4 mm) follows the size-generic guide over the size-specific BOM that the same document cites for 3 mm.
Fix: Flip the default: "Print `deck_support_3mm_x8` ×8 (the Rev D **350** BOM lists a 3 mm deck panel); if the panel measures 4 mm on arrival, reprint `deck_support_4mm_x8` — 8 g, 30 min."

### F21 · MINOR · docs/voron-print-plan.md:620–621
Claim in doc: "the cheapest place to substitute is the **panel clips and deck supports** — those see no heat and no load, and the Voron docs explicitly permit PLA/PETG there."
Source checked: docs.vorondesign.com/materials.html — "PLA is entirely acceptable for **skirts and panel clips**"; "PETG is acceptable for **skirts and panel clips**." Deck supports are not named.
Problem: The permission is extended to a part class Voron does not name (and the parts Voron *does* name — the 437 g of skirts — are excluded by the sentence).
Fix: "…the cheapest place to substitute is the **skirts and panel clips** — the Voron docs explicitly permit PLA/PETG there."

### F22 · MINOR · docs/manual/print/B07-electronics-bay-and-lighting.md:18,54
Claim in doc: `usb_adapter_mount_partial_cover.stl` "| 5.0 ⚠ *(est.)*" and Step B07.2 "the seven files above — **3.3 h**, 60 g".
Source checked: docs/voron-print-plan.md:436 gives it "5.0 (est.)" grams and "—" hours; the 3.3 h plate total is the sum of the other six files only (0.63 + 2×0.49 + 0.26 + 0.55 + 0.35 + 4×0.13 = 3.29 h), while its 5.0 g **is** included in the 60 g.
Problem: The plate's gram total counts the part and the hour total doesn't — B07-P1 is ~0.3 h under-stated and the two figures are derived inconsistently.
Fix: Give the part an estimated 0.30 h and restate B07-P1 as "3.6 h, 60 g" (B07 total 13.2 h; grand total 134.3 h), or mark both the grams and the hours as estimates.

### F23 · MINOR · docs/manual/print/B04-xy-joints-and-x-carriage.md:43,73,76
Claim in doc: "Confirm `x_frame_V2TR_MGN12_*` files, **not a Trident** or MGN9 variant" / "Confirmed X-carriage is the V2TR/Clockwork-2 variant, **not a Trident** or legacy carriage".
Source checked: github.com/VoronDesign/Voron-2 @ `Voron2.4` → `STLs/Gantry/X_Axis/X_Carriage/x_frame_V2TR_MGN12_left.stl` / `_right.stl` — "V2TR" is the shared **V2 + Trident** carriage; it is the correct and only MGN12 R2 carriage in this repo.
Problem: Telling the builder the file must not be "a Trident variant" while the correct filename literally contains `TR` invites them to reject the right file.
Fix: "Confirm the files are `x_frame_V2TR_MGN12_left/right` (V2TR = the shared V2/Trident R2 carriage) — not the superseded `Superceded_Parts/MGN9_X/x_carriage_frame_*_MGN9` files."

## Verified OK
- Every STL/3MF path in the plan and in B00–B10 exists at the stated repo+branch (git trees API, 2026-09-05): Voron-2@`Voron2.4` (202 blobs), Voron-Stealthburner@`main`, LDOVoron2@`main`, LDOVoronTrident@`master`, Nitehawk-SB@`master`, Nitehawk-SB-V2@`master`, Klicky-Probe@`main`, Nevermore_Micro@`master`, whopping_Voron_mods@`main`. **Zero missing or renamed files.** Case-sensitive `side_fan_support_x2.STL` is correct.
- 350-size variants correct everywhere a size variant exists: `rear_center_skirt_350`, `front_skirt_a/b_350`, `side_skirt_a/b_350_x2` (250/300 correctly unused). COB counts 6×100 mm + 2×50 mm match LDO's own README ("Voron 2.4-350 Kit: Print 6x …100mm + 2x …50mm").
- `[a]_z_tensioner_9mm_x4` correct: LDO Rev D 350 BOM lists "Idler, 2GT, 20T, (5mm ID **9mm** W) ×4"; the 6 mm variant is superseded.
- Rails: BOM "LDO-SLR12H-400Z1 ×1" + "LDO-SLR9H-400Z0 ×6" — both rail guides correctly printed.
- 2-hole cable-chain parts, `power_inlet_IECGS_1mm`, `[a]_endstop_pod_D2F_switch`, BTT TFT4.3 mount over mini12864, no ADXL mount, exhaust_cover + stock grill for Nevermore — all match the LDO Rev D printed-parts guide verbatim.
- The ten "supplied printed" LDO parts in §7 match the BOM's "LDO Printed Parts" bag exactly (Leviathan bracket L/R, NH Adapter Mount, DIN Clip ×4, CW2 Chain Anchor Tilted, 2x3 Splitter Spacer ×2, LDO Nozzle Probe, Bed WAGO Mount, SB LED Diffuser, CW2 PCB Spacer).
- Panel spec matches the BOM line for line: deck 3 mm acrylic, back 3 mm acrylic, bottom 4 mm acrylic, doors/sides/top 3 mm PC, foam tape 1 mm and 3 mm. Keystone CAT6 Insert ×1 → 1 blank used + 1 spare is right (2 slots).
- Magnets close exactly: LDO ships 16× 6×3 mm; Klicky needs 8 (4 probe + 3 mount + 1 dock, per the mod BOM) and Nevermore V5 Duo needs 8.
- Klicky B06 list matches the mod's own "What to print" (2× `KlickyProbe_v2`, the three probe jigs, AB mount + three mount jigs, `Probe_Dock_v2.1`, `Dock_mount_fixed_v2`); the plan correctly uses the current `_v2`/`v2.1` filenames where the README is stale.
- Clicky-Clack: "2X" files are **one body each** (shell count = 1) — print two, as the doc says. 6 split bushings + 4 M5×45 pins + ~20 mm proud match the mod README (its `fasteners.csv` says M5x50; README line 30 allows 40–50 mm).
- E3D Revo Voron → `revo_voron/` + `_rear_cw2`, 4× M3×8 — matches the Stealthburner printhead README (E-RV). `[o]` = opaque, `[c]` = clear per the SB STL README.
- Voron print settings quoted correctly: Manual p.4 and docs.vorondesign.com/sourcing.html — layer 0.2 mm, extrusion width "forced 0.4 mm", infill 40 %, grid/gyroid/honeycomb/triangle/cubic, wall count 4, solid top/bottom 5, supports NONE. materials.html shrinkage quote is verbatim, including "55–60 ºC" chamber.
- PrusaResearch.ini @ `version_2.9.6` (and current live bundle 2.5.8, identical): `Prusament ASA @COREONE` — shrinkage XY **0.22 %**, Z 0.22 %, 260/260 °C, bed 110/110, chamber 55, chamber min 40, fan 20/25 %, bridge fan 25, `disable_fan_first_layers = 4`, density 1.07, max volumetric 15. All correct.
- `0.20mm STRUCTURAL @COREONE 0.4` — every "default" in the override table verified: perimeters 2, top 5, bottom 4, fill 15 % grid, widths 0.45 / first 0.50 / top-infill 0.42, arachne, support_material 1 + auto 0, seam aligned, skirts 0, min_skirt_length 4, brim_separation 0.1, elefant foot 0.20, speeds 50/70/120/140/80/45, external-perimeters-first off, dynamic overhang 15/25/45/90 %. SPEED comparison (170/170/200) also correct.
- Printer profile values all correct: bed 250×220, height 270, retract 0.7 @ 45, z-hop 0.2, wipe off. PrusaSlicer 2.9.6 stable 2026-06-25 and 3.0.0-alpha11 2026-09-01 both confirmed; Buddy firmware 6.9.0 exists (2026-08-20).
- Calibration gate internally consistent: cube mesh is exactly 30.00×30.00×30.00; seven checks = seven rows; "0.22 % on a 66.7 mm Z-drive body = +0.15 mm" checks out — `z_drive_main_a_x2` measures 66.70 mm.
- Arithmetic clean throughout: every plate's grams and hours equal the sum of its parts (±0.1 rounding); batch totals 57/324/308/130/122/83/162/223/437/322/80 → 1940 g black + 308 g orange; hours sum to 134.0; plates sum to 26; the §4.3 cumulative series is exact; margins 460 g (24 %) and 492 g (160 %) correct.
- Tallest-parts table verified against the meshes: Handle 60.00 / 67.86×18.62, Latch 58.00 / 25.90×14.61, Hinge-L 55.00 / 20.89×19.50, TFT mount 44.84 / 117×67 (thick 67.84), z_motor_mount 42.00 / 51×30.70. "No part exceeds 150 mm in Z" holds. The Igus backer bridge really does arrive 21.00 × 66.15 × **44.00** standing, as §5.1 warns.
- Multi-body claims verified by shell count: SB main body 7, cw2_captive_pcb_cover 2, usb_adapter_mount 2, bottom_panel_hinge_x2 2, cob mounts 2, V2_Duo_Plenum 2.
- Nevermore `Regular_Cartridge*.3mf` are plain model 3MFs (no `Metadata/Slic3r_PE.config`) — importing them cannot silently overwrite the shrinkage override, so "PrusaSlicer imports them fine" is safe.
- Plate packing checked by MaxRects against the real bboxes: B01-P1, B02-P1, B07-P1, B08-P2/P3/P4/P5/P6 and B09-P1/P2/P3 all fit 250×220 with 3 mm brims and a 3 mm gap. Only B07-P2 and B08-P1 fail (F3, F4).
- Accent-part completeness: all 49 orange pieces account for every `[a]_` file in Voron-2 and Stealthburner that this kit uses; every `[a]_` file left unprinted is explicitly justified (hall-effect, 3-hole, mini12864, exhaust filter, MGN9/6 mm superseded). The 52 Voron-2 STLs never mentioned anywhere are all legitimately out of scope.

## Not checkable
- Whether the V1 `cw2_captive_pcb_cover.stl` physically fits the Nitehawk-SB **V2** board. The V2 repo ships no CW2 cover and its README says the form factor is still "based on hartk's two-piece Stealthburner toolhead PCB", which supports the plan's choice, but LDO publishes no explicit statement. Bench-verify at B06.
- The gram/hour model itself (docs/voron-print-plan.md §4.1). I verified the arithmetic is self-consistent and that the totals are plausible (Voron's sourcing page quotes ~1.5 kg primary + 0.3 kg accent for a typical build; 1.5 kg + Klicky 53 g + COB 127 g + Nevermore 114 g + Clicky-Clack 80 g ≈ 1.87 kg vs the plan's 1.94 kg, and orange 308 g vs Voron's 300 g). I did not slice anything, so the ±30 % hour caveat stands as written.
- `PSU_stabilizer_50mm` "(verify)" — the LDO Build Notes "PAGE 169 SKIP" text is not in the captured Rev D pages I could read; the plan's 4 g print-and-decide hedge is reasonable either way. (The PSU itself is confirmed: BOM says Meanwell **LRS-200**-24, so `lrs_200_psu_bracket_x2` is right.)
- Whether PrusaSlicer refuses to slice, or silently clips, a brim that extends past the bed edge. F3 is stated as a geometric fact (84 % bed fill, no valid MaxRects placement); the exact failure mode in the UI is unverified.
- Clicky-Clack "Blue" colour option (plan §6) — still an open question with Fabreeko; nothing printable depends on it.
