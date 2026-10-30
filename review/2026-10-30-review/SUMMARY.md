# Review 2026-10-30: merged summary

Nine read-only deep reviewers (brief: `BRIEF.md`) over the tree with the uncommitted Rev D+ re-pin, three
goals: (1) accuracy against primary sources, (2) diagrams and photos, (3) build order and flow. G9 reviewed
the Rev D+ diff itself. G4 hit the image viewer's limit at 56 of 132 images; **G4b** checked the rest
(top items: 09.27/09.28/09.30 page images dropped by a trailing " ·"; 09.2 should embed LDO's bay photo;
08.43 lacks the ground-lug photo). Detail, quotes, sources and replacement text live in the group files.

| Group | Scope | Blocker | Major | Minor | Nit |
|---|---|---:|---:|---:|---:|
| G1 | Ch 00, 00a, index, Ch 01 | 0 | 4 | 17 | 6 |
| G2 | Ch 02–04, B01, B03 | 1 | 1 | 9 | 4 |
| G3 | Ch 05–07, B04, B05 | 1 | 3 | 7 | 3 |
| G4 | Ch 08–09, B06, B07, B11 | 0 | 1 | 7 | 8 |
| G5 | Ch 10–11, B08–B10 | 1 | 4 | 8 | 3 |
| G6 | Ch 12–13 | 0 | 5 | 8 | 6 |
| G7 | Ch 14–16 | 0 | 7 | 6 | 3 |
| G8 | build order and flow | 0 | 5 | 14 | 3 |
| G9 | the Rev D+ diff | 0 | 2 | 6 | 2 |
| G4b | Ch 08–09 images G4 could not open (68) | 0 | 0 | 5 | 4 |
| **Total** | | **3 (2 unique)** | **32 (≈28 unique)** | **87** | **42** |

Orchestrator re-checks: G2-01/G3-30-01 confirmed in `scripts/draw_diagrams.py:394–415` (top-down draw of a
bottom-up list) and manual p.68 (flanges outside the pair). G5-01 confirmed by the step's own logic (the
marked face is the one that faced away from the plenum magnet). G9-01 confirmed on LDO's seal drawings
(West3D images 2–3: the seal sits in the vertical's slot, against the horizontal). G7-01 confirmed in
PrusaSlicer 2.9.6 `--help-fff` ("If expressed as percentage … computed over layer height"). Brims: the 21
ASA plates set `brim_width = 0` and add per-object brims only to large parts; B00, B01, B03–B06 and
B02-P2/P3 have none (G2 note, G7-07).

## Needs Alex's decision
1. **Brims on small ASA parts.** AGENTS.md says "ASA satin + brim"; the 10-28 test lifted at brim-free
   corners; B00–B06 plates have no brims. Same question for the Part H exhaust housing (G7-07, 155 mm).
2. **Voron final location and when it moves** (G8-02): 00a.5 outlet, Ch 13–14 and the 14.25 depth check
   depend on it. Proposed: a pre-kit decision step and "move before Ch 13".
3. **B11 print order** (G8-01): P1–P3 after B07, P4/P5 after the kit-day bay measurements (saves 1–5 days
   if the kit lands by ~Nov 4, nothing later).
4. **Ch 12 config editing on the bench Pi** (G6-04): ~1.5 h out of the live open-bay window. G6 also
   floats moving the heater/SSR-LED checks (13.6–13.8) to the end of Ch 12, which would change the 10-23
   eyes-only ruling.
5. **Part H earlier** (G7-06): 14.25's go/no-go look before Parts A–G so the fan order and ~7 h of printing
   overlap; whether the add-on may go in before Part B.

## Blockers
- **G2-01 = G3-30-01** diagram 01 (A/B bearing stacks, used at 04.7, 04.21, 05.26) draws every F695 pair
  flange-IN. Fix the draw order, regenerate `--only 01`.
- **G5-01** 11.36 glues the Nevermore cartridge magnets "marked face out": all four repel the plenum. Marked
  face goes down into the pocket.

## Majors (unique)
Rev D+ diff:
- **G9-01** (supersedes G1-01; affects G5-04) 01.23 puts the seals in the horizontal's slot; LDO's drawing
  puts them in the **vertical's** slot, against the horizontal. Rewrite 01.23 (+ :50, :59, Checkpoint,
  checklists) and embed LDO's drawing. Position before Checkpoint 01 is right (the Z rails cover four of
  those slots from Step 02.06). Then re-check G5-04: which corner slots the LED lead (10.38) and camera
  cable (10.81) pass through.
- **G9-02** 00.2 Do/Check and Checkpoint 00 still inventory against the batch tile (= Rev D page).
Build:
- **G3-30-02** only one long Ti backer has the chain pilot holes: right (A-side) Y, holes at the rear,
  drill 2.5 / tap M3; Ch 05 calls the pair matched and 10.60 puts a T-nut under it. "Pre-tapped" unverified.
- **G3-30-03** `[a]_cable_cover` is the p.204 arch, 2× M3×12 into the A drive's inserts, over the Z-chain
  bundle in Ch 10, not clipped on at 07.39; 10.64 mislabels it.
- **G5-03** 10.37 puts the LED junction PCB on the top rear extrusion; LDO's photo and route: inner face of
  the rear-right vertical, below the corner.
- **G2-02** B03 calipers F695 "flange seats, 15.00 mm × 4 mm" that do not exist (also plan:790,
  checklists:380, slicer-setup:304, index:47).
- **G6-01** every `SAVE_CONFIG`/`RESTART`/`FIRMWARE_RESTART` releases the motors; Ch 13's "M84 only in three
  places" rule fails ten times, once (13.36) with a 150 °C nozzle ~0.25 mm over the PEI.
Images:
- **G3-30-04** diagram 09 (racking) draws equal gaps under a caption saying they differ; 06b checks measure
  yaw, not racking; Z belt clamps drawn on the XY joints.
- **G6-02** 12.12 screenshot shows the V1 toolboard ID the step says you won't see.
- **G6-03** 12.9 KIAUH screenshot: KlipperScreen is option 7 now, not 5.
Print side:
- **G7-01** 14.19 "top-layer line width 100 %" = 0.2 mm in PrusaSlicer; use 0.45 mm.
- **G7-02** per-object extrusion multiplier is impossible in PrusaSlicer; eight separate prints unbudgeted.
- **G8-04 ⊃ G4-01** "smooth sheet" for ASA in B11 (×7), README, Tonight, checklists, B00: now satin.
- **G8-05** the planned B09-P1 runout waits for a person mid-day; start it on a fresh spool.
- **G7-07** see decision 1.
Safety:
- **G5-02** 11.76 opens the bay of a live machine to plug the camera in; do it at 11.52, dead.
- **G7-04** Ch 15 tap-tree SSR rows lack the unplug + 0 V step the tables got on 10-23.
Docs:
- **G1-04 = G8-03** index row 1, Tonight, diagram 11 still say Gen 2 joints and wiper first (10-28 ruling).
- **G1-02** Ch 01/02 say Ch 02 needs B02-P1/P3; P2 holds half the Z1/Z2 corner parts.
- **G7-03** Ch 15's probe "too early/too late" rows still inverted (Ch 13's were fixed).
Flow (goal 3):
- **G1-03** kit day: start the rail soak right after 00.6; trays/tip/Ch 12 Part 1 during the dry (≥45 min).
- **G5-05** Ch 10: say which way up after 10.23; move Sections 4 and 6 to save two flips.
- **G6-05** 13.36→13.39: one hot pass, one `SAVE_CONFIG` (~30 min).
- **G7-05** Ch 14: one 1½–2 h soak instead of four heats (>30 min).
- **G6-04, G7-06, G8-01, G8-02** see decisions.

## Minors and nits
In the group files. Recurring themes: stale hours and plate counts after the 10-24 re-split (Ch 01/02/05
prerequisites, B10 "22 plates", B11 "156.9 h", plate-board 157.0 h, slicer-setup 58.4 h); "months before the
kit" wording against an early-November kit; Rev D+ loose ends (G9-03 "both questions" ×2, G9-04 cable names
in 08.43/10.58 and four callouts, G9-06 survey/plan labels, G9-07 the daylight check, G9-08 magnet sheet
"not laminated" vs Fabreeko's "pre-installed"); stretched part renders and two orange pair renders (G2);
p.31 anchor image shows the 3-hole anchor 08.25 forbids (G4-05); front-load ideas (image the microSD and
draft printer.cfg pre-kit, ~1.5 h).

## Already known and still open
Each group file ends with a "known, still open" line for the 10-23 items in its scope (G1 8, G2/G3 8 + 13,
G4 15, G5 ~12, G6 2, G7 16, G8 2). Closed since 10-23: nozzle-probe gap (09.30 = 13.24), 13.39 re-heat.

## Alex's answers (2026-10-30) and fix status
1. Brims stay off small parts for now (re-assess after the first plates); large add-on parts get one.
2. Location: no step needed, moved as needed. 3–5: approved.
Fixed by the orchestrator: G2-01/G3-30-01 (diagram 01), G5-01 (magnets), G9-01 (01.23 rewritten to LDO's
placement, LDO drawings mirrored), G9-02, G9-03, G9-04, G9-05. Delegated: G8-01 + satin (G8-04/G4-01), G6-04
(+ G6-02/03), G7-05/06/07. Not yet approved: the remaining majors and all minors.
