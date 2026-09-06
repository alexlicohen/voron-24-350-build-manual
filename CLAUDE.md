# 3D Printing — Prusa Core One+ / Voron 2.4 350

## Goal (stated 2026-09-05)
Most efficient AND most effective print/build order for the Voron 2.4 350 once the Core One+ is running: one interleaved timeline of Prusa print batches and Voron assembly phases, dependency-ordered, so the printer is never idle and no assembly step waits on a part. Deliverables: docs/voron-print-plan.md (what to print, batch order), docs/voron-build-instructions-survey.md (which instructions to follow, Prusa-manual-style consolidation), and docs/manual/ — the actual consolidated build manual: Prusa-style numbered steps with fasteners, checks, and print batches interleaved as chapters (Alex: "not just an order, a detailed set of instructions"). Printing guidance is Prusa/PrusaSlicer-specific and quality-first: "speed is not the priority, quality is." Alex will probably use the PrusaSlicer 3.0.0-preview (2026-09-01: yaml profiles, multi-bed projects, per-tool profiles; not feature-complete vs 2.9.6) — the slicer chapter targets 2.9.6 and must carry a 3.0 mapping/posture section. Delivery: MkDocs Material site from docs/ (`scripts/serve.sh` → LAN URL), read on an iPad at the bench; markdown is the single source, PDFs only as exported snapshots. Presentation (Alex 2026-09-06): one page per step like Prusa's help site (generated at build from the chapter markdown; chapter overview pages list steps with thumbnails), NOT long scrolling chapters. No bench photos: the manual is to build from, not a record — the photo ingest script is optional tooling only.


**Status 2026-09-06 (evening):** backlog items 1–4 and 6 shipped, 5 in flight. Site nav is five tabs (Home · Build · Print · Plan · Reference; `docs/.nav.yml` owns the nav). Step pages are action-first (Do → Parts with thumbnails → Check → collapsed "What you're looking at" → ⚠/Tip → Pause → Source) and every step passes lint check 5 word budgets (Do ≤40, Check ≤25, description ≤45, Tip ≤30, ⚠ ≤60; no em-dash/parenthetical in Do/Check/description; ≤1 cross-ref) — see docs/manual/CONVENTIONS.md § Action-first; **never split or renumber steps** (ids are keys everywhere). Plates: **22** (was 27; same-batch merges, 157.1 h unchanged) packed by `slicer/nest.py` (outline packer; the 2.9.6 CLI cannot arrange). **Pending: Alex's GUI QC** of the six changed plates (B03-P1, B06-P1, B07-P1, B08-P2, B08-P3, B08-P4): right-click Arrange → 6 mm, rotations on; save in place; then a FULL `python3 slicer/build_plates.py --from-3mf` re-derives estimates/diagrams; `python3 slicer/check_docs.py` (now also checks plate ids in prose) gates the numbers. Plate plans page: docs/print/plate-plans.md (generated). Item 5 = cumulative end-of-chapter CAD renders on overview/Checkpoint pages (cache: `~/.cache/voron-cad/cache`, venv `venv-cq/`, both uncommitted; rebuild per docs/manual/assets/cad/PILOT.md). Guard rails: scripts/lint_manual.py (5 checks), slicer/check_docs.py (7 sections), CI build+deploy, weekly drift job. Deferred until the printer runs: maintenance + first-prints chapters. Bench-verify items are marked `(verify on bench)` in-chapter. Subagent rule: the working tree may hold Alex's GUI-saved 3MFs — briefs must forbid reverting them.

## Hardware

- **Prusa Core One+** — building with daughter, currently in-progress (as of 2026-09-05 was at Ch.6/step 33 of 58, ~55% through by time). Original kit purchased 2026-05-17 (Prusa order **1779051361**, $1,384.86: "CORE One+ kit Advanced Filtration + Camera BUNDLE" $1,109.00 + Prusament PLA Pearl Mouse 1kg clearance $24.99 + FedEx economy $179.99 + duties/tax; shipped 2026-05-18, FedEx). Nozzle: the stock HF (high-flow) 0.4 Nextruder nozzle (Alex, 2026-09-05) — use PrusaSlicer's HF Core One presets; no hardened nozzle needed for Prusament ASA; buy one identical spare for the ~134 h run. Frame is Gen 1; ordered the Gen 1→Gen 2 upgrade kit (order 1787919456, Aug 28, $212.43): GT1.5 belts/pulleys, Gen 2 heatbed expansion joints, nozzle wiper, spare nylon rivets; Gen 2 quick-release top cover sold separately, not included.
- **INDX 8-Tool Conversion Kit** for Core One+ (Gen 2) — ordered Aug 21 (order 1787331673, $1,083.43, pre-order, $999). Supports PLA/PETG/ASA/ABS/PC/PCCF/PA/TPU/PVA/BVOH, any 1.75mm up to 300°C; nitrocarburized steel nozzles (~10kg PETG-CF / 5kg PC-CF before wear); optional 400°C HT hotend opens PEKK-CF/PPS-CF/PSU/PPA. "No build-volume compromise" claim is from a reseller, not Prusa's spec page — unverified.
- **Advanced Filtration Kit** — corrected provenance: not a separate purchase. Bundled into the original kit order (Prusa order 1779051361, 2026-05-17, "CORE One+ kit Advanced Filtration + Camera BUNDLE") — already owned since the kit arrived, not yet installed. Install before Voron ASA batches begin, during Ch.7 (back panel/PSU cover off) rather than reopening later. Rear-exhaust HEPA+carbon backpack, ~600 print-hrs per cartridge (~6 Voron print sets). Stock reasoning: buy one spare cartridge now (1-2wk Prusa lead time).
- **Sequencing decision**: finish Core One+ kit build through Ch.9 (selftest + first print) BEFORE applying the Gen 2 upgrade — isolates kit-assembly faults from upgrade faults, and belt swap is a from-the-top job. Then re-run belt tensioning/squaring, then start Voron ASA print batches on Gen 2 hardware.
- Core One+ specs (per Prusa/INDX materials, largely unverified beyond memory-level): build volume 250×220×270mm; chamber via bed+fans to 55°C, no dedicated heater (adequate ASA/ABS, marginal PC/PA at scale). Stock Core One+ has NO built-in filter (chamber vents unfiltered) — correction made mid-chat to an earlier wrong claim.
- Order history: context/orders.md

## Voron 2.4 350 plan

- **Kit ordered**: LDO Voron 2.4 R2 Rev D+, 350mm, blue frame, Revo HF hotend, touchscreen, Pi 4B — Fabreeko order **F6424626**, 2026-09-04 (today at time of order), $1,563.21, free shipping, pre-order (ETA mid-September). Line items: kit $1,399.99; titanium extrusion backers 350 $56.25 (25% bundle discount); Clicky-Clack door kit by LDO, 350/Blue, $49.99; acrylic panel for Clicky-Clack, 350, $23.99; precision hex driver set of 5, $32.99.
- **Decision: print ALL functional + cosmetic parts self** (no PIF / Print-It-Forward purchase) — "for the fun of it." PIF was considered (functional set $149.99, cosmetic add-on $134.99 via Fabreeko-PIF collab) but rejected; savings from self-print ≈$190-200 (~$2/hr of Prusa time) were secondary to the stated goal of printing everything themselves.
- **Trident rejected** as the platform (was the initial top recommendation) in favor of 2.4 350 once complexity was deprioritized and volume became a driver — Trident 300 would save ~10-15h build time at same quality but gives up 50mm and the fixed-bed advantage on tall prints.
- **StealthChanger (toolchanger)**: available now via LDO's DraftShift kit (Base + Tool&Dock + Top Hat sub-kits; 350 supports up to 6 tools, 300 up to 5). Decision: build stock single-tool first, upgrade later — need a tuned baseline before adding toolchanger calibration complexity, and INDX already covers multi-material needs.
- **Beacon (eddy-current probe) and Nevermore StealthMax**: deferred, not part of current build — explicitly excluded ("not doing the beacon or the nevermore stealthmax right now"). Probe: kit ships BOTH the Omron inductive probe (QGL-only, wired to PROBE, primary per LDO config) and a Klicky kit (alternative, hand-made cable), plus the LDO nozzle-probe PCB for Z=0. Also in the kit: Nevermore Micro V5 Duo parts, Nitehawk-SB V2 toolboard (the "+" = Nitehawk-SB V2; verified in docs/voron-build-instructions-survey.md).
- **Leviathan MCU (contested):** F446 per the Rev D wiring guide/kit Klipper config; LDO's Leviathan README changed to STM32H743 on 2025-10-30. Read the silkscreen — don't assume from paperwork (manual Ch 12 step 12.13).
- **Bed magnet sheet is user-applied, not pre-laminated** — a separate BOM line (`Magnetic Pad 2.4-350`), fitted during the build (docs/manual/03-build-plate.md), unlike the heater/thermal fuse which are pre-applied.
- **Rev D+ = Rev D + Nitehawk-SB V2** (electrical + one STL: `usb_adapter_mount_partial_cover`) — confirmed, not electrical-only; LDO documented the V2 ESD/grounding scheme 2026-07-10 (manual Ch 10 step 10.58).
- **1 tool to start** on the 350 (not the 300) — locked in.
- **Print order** (batches, all fit a 250×220 plate): 1) Z-drive assemblies (4× housings+tensioners) — gates Z; 2) (no printed parts needed for the build plate — 2.4r2 has no printed feet/bed mounts); 3) A/B drive units, front/rear idlers, XY joints — gates gantry; 4) DIN-rail mounts, electronics-bay parts — gates wiring; 5) Stealthburner + Clockwork 2 (no Beacon mount now) — toolhead, last mechanical step; 6) skirts, panel clips, Clicky-Clack door, Nevermore, spool holder — cosmetic, print while wiring. Batches 1-3 ≈ first 35 print-hours. Print a Voron test cube first, caliper it, before committing to the Z-drive batch — XY dimensional check gates everything downstream.
- Only ~18–19% of the build (by time; per docs/voron-build-instructions-survey.md, corrected from the chat's 15%) is possible before any printed parts exist: frame squaring/assembly, Z linear rails on vertical extrusions, firmware flashing (Klipper on Pi/Leviathan/Nitehawk), harness inventory/DIN rail install.
- **Chamber/material spec**: Voron spec ABS/ASA only, 4 perimeters, 5 top/bottom, 40% grid/cubic infill, 0.2mm layers, 0.4 nozzle, no supports, seam aligned rear, smooth/satin sheet (not textured — ASA adheres poorly on textured, no glue needed on smooth). Stock chamber ~50-60°C passive; heater retrofit to 65-70°C possible later but not planned now.
- **Vendor**: Fabreeko chosen over MatterHackers/Levendigs (same LDO kit), Fysetc (cheaper, worse QC/support), Formbot/Siboor (skip) — reference reseller for the Voron community, best component QC (LDO motors/rails, pre-crimped harness).
- **Assembly docs** (layered, not a single manual): Voron 2.4r2 official Assembly Manual (vorondesign.com) + Stealthburner manual as primary; LDO supplements at docs.ldomotors.com/en/voron/voron2 (Build Notes/FAQ, Printed Parts Guide, Wiring Guide, Klipper config) as deviations/overlay. LDO docs currently only cover Rev D, not D+ — Rev D+ = Rev D + Nitehawk-SB V2 (electrical + one STL: `usb_adapter_mount_partial_cover`), not electrical-only.

## Materials & filament

- **Prusa order 1788547486** (today, $291.66, incl. $57.99 FedEx Economy): Prusament ASA Galaxy Black 800g ×3, Prusament ASA Prusa Orange 800g ×1, Prusament PVB Natural 500g, Prusa USS Drybox ×2. ASA came in at $26.99/spool (well under earlier ~$35-49.99 estimates from web searches).
- **Color scheme**: Galaxy Black primary (metallic fleck hides layer lines/artifacts on skirts) + **Prusa Orange accent** — chosen *intentionally* to contrast against the blue LDO frame ("orange was intentional to contrast blue+orange over the black base material"). Note this reverses earlier chat recommendations (which proposed a blue accent to match the frame, or red rejected as fighting the blue) — final decision is orange, confirmed directly by Alex.
- **Spool count — evolved across the chat, final = 3 black + 1 accent (orange), 800g each.** History: first estimate was 5 spools (4 black + 1 accent) assuming Beacon mount + Nevermore StealthMax included; once those were dropped, revised black need ≈2.0kg (incl. ~0.3kg reprint allowance) → 3 spools (2.4kg) is sufficient with margin. Confirmed by the actual order (3 black + 1 orange). Estimated need breakdown at the 5-spool stage: functional set ~1.0kg, cosmetic set ~0.9kg, mods (Beacon mount/Clicky-Clack/Nevermore) ~0.35kg, reprints ~15%/~0.35kg.
- **Build sheet**: use the **smooth/satin sheet** (ships with kit) for all Voron ASA parts — textured sheet is for PLA/PETG and was separately purchased for that use (confirmed, not a mix-up).
- **Drybox/drying conclusions per material**: PLA — no drybox needed, dry only if open for months/stringing. PETG — not required, helps in humid Boston summer if mounted for weeks. ASA — not required if spool fresh/used within 1-2 weeks; dry at 80°C/4h if open longer or bubbling/matte striping appears (Voron parts are structural, so this is the material to watch). PVB — yes, needs drybox, absorbs moisture quickly, ruins clarity. Rule of thumb: printer-mounted drybox earns its place for PVB/TPU/PC Blend/nylon; PLA/PETG/ASA just need a heat-dry before use + sealed bag after. Practical setup: one USS Drybox on the active ASA spool during the ~2-week continuous Voron print run, not eight boxes.
- **Materials-of-interest ranking for Core One+** (beyond PLA/PETG already owned), from Prusament's lineup: 1) PVB — translucent, vapor-smoothable, best "wow" for daughter, ~$30. 2) PC Blend — real engineering plastic (~110°C HDT), ~$60. 3) PA11 (Natural) — bio-based nylon, low-warp, needs dry box, ~$50. 4) TPU — flexible, showcases INDX multi-material later, ~$40. 5) PC Blend CF / PA11 CF — stiff/matte, needs hardened nozzle (wait for INDX), $72-100. 6) PETG Tungsten — niche radiation-shielding novelty, ~$100+. 7) PP — skip, hard to bed-adhere. 8) PEI — skip, needs 400°C HT hotend + hotter chamber than Core One+ supports. Practical first order alongside ASA: one PVB, one PC Blend, one TPU.

## Tools & metrology

Ranked by effect on finished build quality (not assembly speed):
1. Flat reference surface (granite plate or float glass) — squareness is set here.
2. Machinist square (150mm, DIN 875/2+) + steel rule.
3. Digital caliper, 150mm.
4. Hex drivers, ball-end 1.5/2/2.5/3/4/5mm.
5. Torque screwdriver, 0.5-3 Nm adjustable.
6. Temp-controlled soldering iron for heat-set inserts (~150 inserts in the build).
7. Insert-setting press/jig.
8. Rail alignment jig for MGN12 on 2020 (printed, free).
9. Dial indicator + magnetic base (optional; Beacon would replace this for bed, but Beacon deferred).
10. Loctite 243, Super Lube 21030, isopropyl, flush cutters, JST crimper (mods only).

**Bought**: Fabreeko precision hex driver set of 5 (in kit order F6424626, $32.99).
**Still needed**: flat reference surface, machinist square, digital caliper, torque screwdriver, soldering iron/insert tips, rail alignment jig, dial indicator (optional).
**Flat-reference decision**: use the kitchen stone counter (granite/quartz) for the frame-squaring step — verified flat with a straightedge/feeler-gauge test across the working area in both directions and diagonals — rather than buying float glass or a granite tile/plate specifically for this. (Prior candidates considered and priced: Grizzly G9650 12×18×3in granite ~$80-110/~60lb; ½in annealed float glass 18×24 ~$40-70/~19lb — both superseded by the counter-top solution once confirmed usable.) A dedicated 12×18 granite plate may still be worth buying later for precise caliper/insert work, per the tool list above, but no purchase confirmed.

## Open items / to-buy

- Super Lube 21030 synthetic grease (LDO rails ship dry; documented requirement) — not yet ordered. Note: 21030 is NLGI 2 — LDO's guide asks for 0/1 but names 21030 by part number; buy 21030.
- Filament dryer (e.g. Sunlu S4, ~$100, 4-spool) — not yet ordered; needed since drybox alone doesn't dry filament.
- Spare Advanced Filtration cartridge (1-2wk Prusa lead time; don't want printer idle mid-Voron-batch).
- Clicky-Clack "Blue" option = the door's aluminium extrusion frame color, matching the blue printer frame; visible trim, intentional, RESOLVED (survey).
- Digital caliper, machinist square, torque screwdriver, soldering iron/insert-tool kit (LDO Heat Insert Tool Kit, $9.99, sold by Fabreeko), rail alignment jig — none confirmed purchased.
- Soldering iron must accept Hakko-style 900M-T tips — the kit already includes LDO's brass heat-set tip in that format; a Pinecil won't fit it.
- 5 mm hex driver — not needed — every BOM fastener is 3 or 4 mm drive.
- Nevermore carbon/Boost filter media — deferred along with StealthMax; will be needed once Nevermore is built.
- LDO documented the V2 ESD/grounding scheme 2026-07-10 (manual Ch 10 step 10.58).

## Key facts & numbers

| Item | Value |
|---|---|
| Core One+ kit assembly time | ~9-11h total; ~4.5-6h hands-on remained at Ch.6 step 33/58 |
| Voron 2.4 350 build time | ~40-60h hands-on + ~100h unattended printing (first build); experienced builders ~20h |
| Voron self-print filament cost | ~$70-90 (vs. $284.98 buying PIF functional+cosmetic sets) |
| Prusa vs. LDO kit price delta (300 vs 350) | ~$100-150 originally estimated; actual Fabreeko listing had 300/350 at same price |
| VFA (vertical fine artifacts) | Fine periodic vertical ripple (0.5-2mm spacing) from belt-tooth engagement ripple on pulleys; cosmetic only, no strength/dimensional effect. Distinct from ringing (frame/toolhead resonance, fixed by input shaping). |
| GT1.5 belt fix (Gen 2) | Replaces Core One's GT2 (2mm pitch) belts/pulleys with GT1.5 (1.5mm pitch); raises ripple frequency ~1/3 and reduces amplitude, reducing VFA — a productized community fix. Pulleys, steps/mm, and firmware all change together; must re-tension/re-square after. |
| Fabreeko order | F6424626 — 2026-09-04, $1,563.21 |
| Prusa filament/drybox order | 1788547486 — 2026-09-04, $291.66 |
| Prusa Gen 1→Gen 2 upgrade order | 1787919456 — 2026-08-28, $212.43 |
| Prusa INDX order | 1787331673 — 2026-08-21, $1,083.43 |
| Gen 2 upgrade KB guide | help.prusa3d.com/manual/prusa-core-one-to-gen-2-upgrade_2435 |
| Prusa Core One+ original kit order | 1779051361 — 2026-05-17, $1,384.86, shipped 2026-05-18 |

## Source

Raw record: `context/chat-transcript.md` (51-turn claude.ai chat, exported 2026-09-05, covering 2026-09-03 through 2026-09-05).
