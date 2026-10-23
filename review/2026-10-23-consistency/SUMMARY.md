# Consistency review 2026-10-23: merged summary

Eight read-only deep reviewers (brief: `BRIEF.md`), one report per group (`G1`–`G8`). Detail, quotes,
sources and replacement text live in the group files; this page ranks and de-duplicates.

| Group | Scope | Blocker | Major | Minor | Nit |
|---|---|---:|---:|---:|---:|
| G1 | Ch 00, 00a, index, plan, survey, README | 0 | 7 | 19 | 6 |
| G2 | Ch 01–03, B01 | 0 | 0 | 10 | 6 |
| G3 | Ch 04–07, B03–B05 | 0 | 0 | 11 | 8 |
| G4 | Ch 08–09, B06, B07, B11 | 1 | 5 | 10 | 6 |
| G5 | Ch 10 + Ch 12 | 0 | 6 | 7 | 4 |
| G6 | Ch 11 A/B + Ch 13, B08–B10 | 0 | 4 | 5 | 5 |
| G7 | Ch 14–16 | 0 | 1 | 8 | 8 |
| G8 | print/, slicer/, sources | 0 | 6 | 12 | 3 |
| **Total** | | **1** | **29 (25 unique)** | **82** | **46** |

Orchestrator re-checks: G4-01 and G4-02 confirmed from the STLs (front half: Ø4.6 ×2 + Ø4.7 ADXL pair;
rear_cw2: Ø3.3–3.5 clearance only) and SB p.40/p.41. G8-01 confirmed in the three inis
(`first_layer_infill_speed = 100`). G8-02 confirmed in `sync_start_gcode.py` (`INI` has black/blue only).

## Needs Alex's decision
1. **Kit ETA early November vs "late Nov–Dec" everywhere** (G1-01, G8-03, G2 note): pages to update, and
   whether the remaining 157 h keeps numeric batch order or front-loads what Ch 01–08 need.
2. **Ch 13 checks that look into a closed bay while live** (G6-01 = G5-5: 13.1–13.3, 13.8 SSR LED,
   What-if rows, Checkpoint 13): recommended, keep the bay closed live and replace those checks.
3. **Leviathan flash by SW1/SW2 on a live board in the open bay** (G5-2): recommended, no-button flash,
   buttons as a named recovery exception.
4. **B02-P3 Igus-backer bridge stands upright in the committed 3MF** (G8-06): fix in the GUI + `--from-3mf B02-P3`.
5. **Preset "(modified)" wording** (G8-04): B00 vs 00-slicer-setup disagree; settle by looking at the GUI.

## Blocker
- **G4-01** 08.7 puts the inserts in `printhead_revo_voron_rear_cw2`; they belong in `_front` (ruins the rear half).

## Majors (unique)
Build:
- G4-02 08.28–08.30 halves swapped (hotend seats in the front half; rear closes onto it, p.40–41).
- G4-05 = G6-04 nozzle-probe pin gap: 09.30 sets 1.5 mm, 13.24 checks 2–3 mm.
- G4-04 09.22 keeps one Pi USB-A port clear; Ch 10 needs two (three with the camera).
- G4-06 B07 inspects heat-set bosses the mains WAGO mount does not have.
- G6-03 13.39 meshes "still hot" after 13.36's SAVE_CONFIG turned the heaters off.
Mains safety:
- G1-03 = G5-1 power-on steps say "two people" / carry Helper lines; 00a.2 says one adult.
- G1-04 00a says wall-first switch-off; the steps say rocker first.
- G1-05 + G6-02 connector swaps (Ch 13) and opening the bay at 11.52 lack unplug + 0 V proof.
- G5-3 12.1 option 2 powers the bay before 12.11, the first sanctioned power-on.
- G5-4 00a.6 says +24 V to earth reads OL; Ch 10 (correct) says about the +V→−V value.
- G5-6 10.75 meters 5 V on Pi pins the HAT power adapter covers.
- G4-03 09.18 says the DIN rails are earthed and promises a continuity check that does not exist.
Print side:
- G8-01 first-layer solid infill runs at 100 mm/s, not 25 (peak flow 10, not 8.8 mm³/s).
- G8-02 the documented start-G-code switch is a no-op and crashes on PETG (B11).
- G8-05 plate-review checklist says "smooth/satin" for ASA (`build_printables.py:943`).
- G1-07 README tells readers to run `build_plates.py` without `--from-3mf`.
Docs:
- G1-02 Ch 00 line 18 describes Gate B the old way, contradicting the rest of Ch 00 and the plan.
- G1-06 Ch 00 tool list misses ~8 tools later chapters use.
- G7-M1 glossary "never from caliper readings" contradicts the Core One+ gates that link to it.

## Minors and nits
82 minors + 46 nits in the group files: mostly stale step/chapter/bin cross-references (e.g. G3 set),
counts (B08 4 plates not 6; B02 17 bins not eleven; B01 4 files), stale purchase states (PETG V0
bought 10-13), and add-on blue jobs ignored by "no more blue" lines.
