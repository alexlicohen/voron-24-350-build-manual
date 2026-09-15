# Batch B04 — XY joints + X carriage

**Time:** 8.6 h (1 plate) — PrusaSlicer 2.9.6 estimate.

**Sessions:** 1 plate start (~5 min hands-on, 8.6 h unattended) + ~15 min inspect and bin.

**Prerequisites:** **Gate B passed** (Step B00.7 — the printed bores and the insert bosses; the caliper and
insert rows run early, on what is already on the bench). B02 (accent `[a]_endstop_pod_D2F_switch`, cable bridge)
feeds the same assembly chapter and printed two batches ago. B03 is not a print prerequisite — the two
batches only meet at Ch 04/05.

**Printed parts**


| STL | Repo path | Qty | Colour | g ea | Bin |
|---|---|---:|---|---:|---|
| `xy_joint_left_lower_MGN12.stl` | Voron-2 `STLs/Gantry/X_Axis/XY_Joints/` | 1 | Black | 32.0 | 05-XY |
| `xy_joint_left_upper_MGN12.stl` | Voron-2 `STLs/Gantry/X_Axis/XY_Joints/` | 1 | Black | 11.7 | 05-XY |
| `xy_joint_right_lower_MGN12.stl` | Voron-2 `STLs/Gantry/X_Axis/XY_Joints/` | 1 | Black | 32.7 | 05-XY |
| `xy_joint_right_upper_MGN12.stl` | Voron-2 `STLs/Gantry/X_Axis/XY_Joints/` | 1 | Black | 11.1 | 05-XY |
| `x_frame_V2TR_MGN12_left.stl` | Voron-2 `STLs/Gantry/X_Axis/X_Carriage/` | 1 | Black | 17.1 | 07-X |
| `x_frame_V2TR_MGN12_right.stl` | Voron-2 `STLs/Gantry/X_Axis/X_Carriage/` | 1 | Black | 17.2 | 07-X |
| `probe_retainer_bracket.stl` | Voron-2 `STLs/Gantry/X_Axis/X_Carriage/` | 1 | Black | 0.5 | 07-X |

⚠ **Probe retainer bracket, conditional:** only used with the Omron inductive probe. Costs 0.5 g — print
it, decide later. If the probe barrel measures 9 mm rather than 8 mm on arrival, print
`probe_retainer_bracket_9mm.stl` instead **(verify on arrival)**.

**Hardware:** none.

**Read first**

- Checkpoint after B04: caliper the printed M3 holes now; the real MGN12 carriage screw pattern is tested
  against `x_frame_V2TR_MGN12_*` on kit day, before any heat-set goes in.
- Most commonly reprinted here: `xy_joint_*_lower_MGN12`.
- `x_frame_V2TR_MGN12_*` are the R2/Clockwork-2 carriage halves — LDO Build Notes p.129-130 warn
  specifically about using the wrong X-carriage variant here.

## Step B04.1 — Filament prep

**Do:** Galaxy Black, spool #1 after B03. The ledger has 328 g on it at the start of this plate and 211 g after, so no spool change here.
**Check:** Clean purge; ≥117 g on the spool.

Source: [print plan §4.3 — spool changes](../../voron-print-plan.md#43-spool-changes) · [00-slicer-setup § Drying](00-slicer-setup.md#drying) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B04.2 — Load plate B04-P1

![Plate B04-P1 — sorting diagram](../assets/plates/B04-P1.png)

*Sorting diagram, drawn from the committed project: every part numbered and filled in the colour of its bin, bin id on the part; the legend reads # · STL · bin (chapter · steps). Sort at Step B04.6.*

**Do:** Open `slicer/plates/B04-P1.3mf` with **File → Open Project**. Arrangement, per-object brims and overrides are already in the project, so confirm it loaded rather than rebuild it. No rotation, no brim: the preview shows no brim outline.
**Parts:** all seven — 8.6 h, 117 g (PrusaSlicer 2.9.6 estimate); `xy_joint_left_lower_MGN12`; `xy_joint_left_upper_MGN12`; `xy_joint_right_lower_MGN12`; `xy_joint_right_upper_MGN12`; `x_frame_V2TR_MGN12_left`; `x_frame_V2TR_MGN12_right`; `probe_retainer_bracket`.
**Check:** The plate holds `x_frame_V2TR_MGN12_left/right`, not the superseded `Superceded_Parts/MGN9_X/x_carriage_frame_*_MGN9` files.

**Helper:** Counts the parts on the sorting diagram and checks the total against the object count.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [print plan §6 — conditional / verify items](../../voron-print-plan.md#6-conditional-verify-items)

## Step B04.3 — Pre-print checks

**Do:** Sheet per [00-slicer-setup § Print sheet](00-slicer-setup.md#print-sheet), chamber preheating.
**Check:** Chamber ≥40 °C.

Source: [00-slicer-setup § Print sheet](00-slicer-setup.md#print-sheet) · [00-slicer-setup § Calibration sequence](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B04.4 — Print

**Do:** Print with standing overrides.
**Check:** First layer clean on both XY joint lowers, the largest parts on the plate.

Pause: ~5 min since the last pause — plate started; nothing to do until it finishes.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B04.5 — Inspect

**Do:**

1. Now: caliper each `xy_joint_*_MGN12` half's four M3 holes, 3.40 mm, 15.0 × 16.0 mm apart.
2. Now: caliper the carriage halves' M3 holes, 3.40 mm.
3. Kit day: offer the real MGN12 carriage up before any heat-set.
**Check:** Every M3 hole reads 3.40 mm ±0.10 and the two carriage halves close with no gap.

Pause: ~10 min since the last pause — holes calipered and the halves separated again; no inserts set, and the real carriage is a kit-day row (Ch 05 sets the inserts).

Source: [print plan §5.2 — checkpoint after each batch](../../voron-print-plan.md#52-checkpoint-after-each-batch) · [00-slicer-setup § Calibration sequence](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) · [LDO Build Notes / FAQ](https://docs.ldomotors.com/voron/voron2/build-faq)

## Step B04.6 — Sort into bins

**Do:** Sort off the plate diagram: number to legend, colour to bin, bin id on the part. Mark plate id and date on a hidden face. Labels: [bin-labels sheet](../../print/bin-labels.md). Keep `probe_retainer_bracket` loose until the Omron barrel diameter is confirmed.

**B04-P1**

| bin | parts off this plate |
|---|---|
| **05-XY** — XY joints, cable bridge, endstop pod | `xy_joint_left_lower_MGN12`, `xy_joint_left_upper_MGN12`, `xy_joint_right_lower_MGN12`, `xy_joint_right_upper_MGN12` |
| **07-X** — X carriage halves, probe bracket, cable cover | `x_frame_V2TR_MGN12_left`, `x_frame_V2TR_MGN12_right`, `probe_retainer_bracket` |

**Check:** 05-XY: four joint halves plus the pod and bridges; 07-X: two frame halves and the bracket.

**Helper:** Reads each bin label aloud and checks the count against the diagram.


Pause: ~10 min since the last pause — the plate sorted into 05-XY and 07-X, bin ids on the parts. `probe_retainer_bracket` stays loose until the Omron barrel is measured; no inserts set.

Source: [print plan §9 — batch summary](../../voron-print-plan.md#9-machine-readable-batch-summary) · [print plan §2 — which parts gate which step](../../voron-print-plan.md#2-which-parts-gate-the-frame-and-z-drive-steps) · [print/README § Bins](README.md#bins)

---

## Checkpoint B04
- [ ] Gate B passed before B04-P1 started
- [ ] Printed M3 holes in both XY joints and both carriage halves caliper 3.40 mm ±0.10
- [ ] *(kit day)* MGN12 carriage screw pattern confirmed against `x_frame_V2TR_MGN12_left/right` before heat-sets
- [ ] *(kit day)* Omron probe barrel measured (8 mm vs 9 mm) — correct `probe_retainer_bracket` variant confirmed
- [ ] Confirmed X-carriage is `x_frame_V2TR_MGN12_left/right` (V2TR/Clockwork-2), not the superseded MGN9 carriage

## Common mistakes
- Grabbing a superseded MGN9 X-carriage file by mistake — LDO Build Notes flag this explicitly. `V2TR` is the
  right file: it is the carriage shared by the V2 and the Trident.
- Committing heat-set inserts into the carriage before the real carriage has been offered up on kit day.
- Reaming a printed hole instead of calipering it and fixing the profile.

## Next
Assembly: *Gantry* (p.82–107). Printing: [B05 — Z joints + Z chain](B05-z-joints-and-z-chain.md).
