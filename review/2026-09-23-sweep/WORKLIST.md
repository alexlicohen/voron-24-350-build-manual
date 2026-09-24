# Sweep fix work list (from the 2026-09-23 sweep)

Source: `G1`–`G8` in this folder (each finding has its evidence and a fix); rubric `RUBRIC.md`; report https://claude.ai/artifact/384d2dncFFbqaMYWxE2GDN.
Parsed list of all 243 rows: re-run the parser in the session notes, or just `grep '^| '` the G files.

**Rules for every wave:**
- Check each change against the page image, STL, CAD or LDO photo, never against a finding's text (AGENTS.md standing rule).
- Never split or renumber steps.
- Gate: `python3 scripts/lint_manual.py && python3 slicer/check_docs.py` plus `.venv/bin/mkdocs build --strict`.
- Check at the iPad viewport (1024×768).
- Mains and Ch 10 are the danger zone, so they go to the deep tier.
- Briefs must forbid reverting Alex's uncommitted files (IMG_3298/3299.jpeg, any GUI-saved 3MF).

## Wave 1: blockers and safety (deep tier)
- [x] **Z-belt upper clips** (G3-01, G3-02, G4 B1, B2, M1):
  - fit `[a]_z_belt_clip_upper_x4` in Ch 05 under the idler/drive top M5×16 pair (Voron p.91/93/95);
  - Ch 06: 06.7 stack = lower clip only; 06.17/06.20 clamp the 2nd belt end with the top M5×16;
  - 06b.9/06b.10 and Checkpoint 06b to match p.117/120.
- [x] **Bed WAGO breakout** above the deck on the left bed extrusion (G5-01); fix 09.34, Ch 03, Checkpoint 09 and the 10.12/10.14 wording.
- [x] **Dead-machine step at the top of Ch 11 Part A** (G6-01): off, unplug, cord in view, PSU LED out. Fix the Part A breadcrumb "before first power-up".
- [x] **Chamber Filtration = Adv. Filtration** check in B00.3 and every B01–B10 pre-print step, plus a "set it back" line at the end of B11 (G8-01).
- [x] **Safety majors:**
  - G6-03: the L↔N meter pass criterion;
  - G6-04: safety text collapsed inside "What you're looking at";
  - G1-09: the 00a.11 rituals collapsed;
  - G1-10: the print plan hands the iron to the helper;
  - G7-03: `M84` in Ch 15 with no hold-the-gantry warning;
  - the raven Check badge renders on mains and iron steps (G5 note, systemic: `hooks/callouts.py` / `hooks/mascot.py`).

- Wave 1 done 2026-09-23 (claude, uncommitted): new step 11.67 (dead machine, first in Part A; Checkpoint 12 Next button → 11.67 via `build_steps.py` `## Next` lead link); L↔N pass ≥100 kΩ or OL `(verify on bench)`; badges suppressed via `hooks/mascot.py` NO_MASCOT_STEPS (single classifier, also used by gatecalc); 00a.5/8/9/11 rules visible; Ch 13/15 motor-release rows warn to hold the gantry.
- Wave 1 leftovers for Alex/bench: 09.34 mount reach with the plate fitted (3 mm ball-end from the rear?) and its exact position; 11.67 says "cord out of the room" (worklist said "in view"); blower-audible check in B00.3 not added (start time unverified); 13.22/13.25 Tip/13.26 FIRMWARE_RESTART with the gantry lifted 10 mm (no hands under, left alone).

## Wave 2: regressions from today and stale numbers (builder tier, mechanical)
- [x] 10.80 fin between −V and FG, using the chapter's own terminal numbering (G6-02).
- [x] 09.6 dry-lay the DC loop and VHB it at 09.36 (G5-02).
- [x] 09.16: position from the clearance targets (G5-05).
- [x] B11.9 A/B lead check: move it to after the motors are mounted, or measure a proxy (G8-10).
- [x] B11.11 recipe: rename only the changed piece, round to the 12 mm tine step, flip base-down (G8-09).
- [x] B11.8: 26 pieces (G8-08).
- [x] Hot first-layer check after B00.0, with a project file for the five squares (G8-05).
- [x] v3 images for 10.8–10.16 and the frame PE lug (G6-05, G6-06).
- [x] Cross-page numbers:
  - inserts 146 → 153 (G1-03);
  - bins 25 → 26 (G1-04);
  - the stale 00.6 B07 ⚠ (G1-05);
  - `TESTZ Z=-0.1` removed from Ch 15/16 (G7-01, G7-02);
  - the Heatset_Practice coupon double use (G1-01, G2-04, G8-11);
  - non-HF presets in print plan §1.3 (G8-07);
  - the bare `build_plates.py` line in 00-slicer-setup (G8-06);
  - B01.7 kit-day rows and B01 Next → B02 (G8-03, G8-04);
  - the Gate B table's double header (G8-02).
- [x] Wayfinding:
  - Checkpoint 10 Next → 12.11 (G6-07);
  - Checkpoint 06 → 06b;
  - Home "Build tab in chapter order" (G1-08);
  - the Tonight claim of a progress overlay, which is false (G1-06/07).
- Wave 2 done 2026-09-23 (claude): Heatset_Practice = Gate B insert row only (B00.7, pre-kit, adult, KADRICK M3×H5, stock tip); 00.13 now kit-day LDO-tip fit. Hot first-layer check = `slicer/hot_check.py` → `slicer/checks/hot-first-layer.3mf` (re-run after any start-G-code sync). v3 lead images in `docs/manual/assets/b11/v3-*.jpg` (from `layout-v3/work/leads_v3.py`). Checkpoint pages take their Next button from a `**Next:**` line (build_steps.py); Checkpoint 06 → 07.1, 06b → 13.35, 10 → 12.11, B01 → B02.
- Wave 2 leftovers: 13.34's Next button skips to 13.35 instead of 06b (override works on checkpoints only); B11.10 `sig`/`bedl` rows measure spare on LDO's route before the bed/probe/Nevermore are fitted (same flaw as G8-10); Tonight segment from the 00.16 pre-kit Pause starts at kit-day 00.13 (needs a Pause on 00.13); 02.03 insert temperature with the LDO brass tip `(verify on bench)`; B11 P4/P5 schedule (13.1 h must be off the bed before 09.6; print right after kit day instead? Alex); AGENTS.md `--from-3mf` wording proposal pending approval.

## Wave 3: remaining accuracy majors (deep tier)
- [x] G2-01 Z-idler T-nuts go in the top rail's inner slot; G2-02 tighten the 01.16 M5×16.
- [x] G3-03 the belt-offcut check; G3-04 pulley planes; G3-05 the rail-hole rule; G3-07 the M3×16 count.
- [x] G4 M3 07.7 stop screws in the plain hole; M4 Omron is a rectangular block; M5 don't cut the pre-terminated probe lead; M6 the belt-cut advice; M7 double taping.
- [x] G5-03 probe above the deck; G5-04 Leviathan brackets per p.155.
- [x] G7-04 `SET_IDLE_TIMEOUT` not `RESTART`; G7-05 the MainsailOS numpy/matplotlib check; G7-06 EM vs shrinkage (Ellis).
- [x] G6-08 the DC lid instruction out of the collapsed block; G6-09 11.37 cartridge fill.
- Wave 3 done 2026-09-23 (claude). B11 decision applied: P4/P5 wait only for the kit-day bay measurements (+ coupon for P5); the A/B lead check (B11.9, after Checkpoint 06) only decides whether a longer replacement lead (4-pin JST-XH, `(verify on bench)`) is made before Ch 10. B11.10 `sig`/`bedl` rows now measurable on kit day. 10.30 renamed "Confirm the inductive probe's tape" (old anchor kept): tape goes on once, at 07.34.
- Wave 3 leftovers: bench — 01.19 hex-key reach to the M5×16 (else tighten at 01.16 with the bracket held flush), MGN9H/MGN12H hole counts vs an LDO drawing, probe lead's bag name; wording — 01.16 "other leg down and outward" (CAD: flat on the rail top, pointing outward); 05 "A high, B low" inferred from pulley heights (p.76/80).

## Wave 4: systemic, closer to Prusa (plan first; decide scope with Alex)
- [ ] **Parts lines use `;` separators and totals per segment, and give the bag source,** so the generated Gather block becomes Prusa-style parts preparation (G2-03, G3-06). Fix the generator plus the content.
- [ ] **Step images cropped to the relevant manual panel;** screenshots for the Ch 12–14 software steps (76/104 without an image) and Ch 11 (29/66).
- [ ] **Helper lines** in Ch 06–10 and 12 wherever two hands or a phone are needed (gantry lift, belt readings).
- [ ] **A reward at every Checkpoint:** Revali's `pass` pose, "you built X", and a real treat. Alex to pick the treat.
- [ ] **The Tonight progress overlay** (approved 2026-09-23): read the progress.js tick store, skip finished segments, plans start at the first unfinished step.

## Wave 5: minor and polish (176 items), batched per chapter from the G files


## Decisions (Alex, 2026-09-23)
- Pushed waves 1–2 (283ed5c).
- **B11 P4/P5:** print right after kit day, once the A/B motor-cable lengths are measured; if a cable is short, make a replacement (longer) cable rather than drop layout v3. B11.9 becomes a confirmation. Fold into wave 3 (B11 Read first/B11.9/P4–P5 rule).
- 11.67 keeps "cord out of the room". 10.80 lid order (lids on before the 10.73–10.79 sweep) confirmed.
- Wave 4 approved: Parts lines become **one item per line** (bag source, per-segment totals) feeding Gather; cropped panel images + Ch 11–14 screenshots; helper lines; Checkpoint reward = Revali pass pose + **gummy worms** (bird theme).
- Tonight progress overlay: **build it in wave 4** (read the progress.js tick store, skip finished segments, start the 30/60/90 plans at the first unfinished step; per-device only).

## Gated / needs Alex
- B11 GUI QC (B00.8); the PETG V0 spool; kit-day bench values (every `(verify on bench)`); the Ch 10.80 lid order (lids on before the 10.73–10.79 sweep) was accepted by the orchestrator: confirm.
- Decide whether `build_plates.py --from-3mf` with no ids is safe. AGENTS.md says to run a FULL `--from-3mf` after a GUI re-save; B00.8 says never run it without ids. Read `main()` and make both say the same thing.
