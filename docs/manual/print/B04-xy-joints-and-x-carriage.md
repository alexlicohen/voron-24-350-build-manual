# Batch B04 — XY joints + X carriage

**Time:** 8.6 h (1 plate) — PrusaSlicer 2.9.6 estimate.

**Sessions:** 1 plate start (~5 min hands-on, 8.6 h unattended) + ~15 min inspect and bin.

**Prerequisites:** **Gate B passed** (Step B00.7, kit day — XY joint bores and the MGN12 carriage pattern).
B02 (accent `[a]_endstop_pod_D2F_switch`, cable bridge) feeds the same assembly chapter and is already printed
in the pre-kit order. B03 is not a print prerequisite — the two batches only meet at Ch 04/05.

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

- Checkpoint after B04: test the MGN12 carriage screw pattern against `x_frame_V2TR_MGN12_*` before
  committing heat-sets. XY joint bores must accept the shafts without reaming.
- Most commonly reprinted here: `xy_joint_*_lower_MGN12`.
- `x_frame_V2TR_MGN12_*` are the R2/Clockwork-2 carriage halves — LDO Build Notes p.129-130 warn
  specifically about using the wrong X-carriage variant here.

## Step B04.1 — Filament prep

**Do:** Galaxy Black, confirm ≥117 g remaining (the ledger has B04-P1 ending spool #2 at ~13 g — stage spool #3).
**Check:** Clean purge.

Source: [print plan §4.3 — spool changes](../../voron-print-plan.md#43-spool-changes) · [00-slicer-setup § Drying](00-slicer-setup.md#drying) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B04.2 — Load plate B04-P1

![Plate B04-P1 — sorting diagram](../assets/plates/B04-P1.png)

*Sorting diagram, drawn from the committed project: every part numbered and filled in the colour of its bin, bin id on the part; the legend reads # · STL · bin (chapter · steps). Sort at Step B04.6.*

**Do:** Open `slicer/plates/B04-P1.3mf` (**File → Open Project**). The arrangement, the per-object brims and every override are already in the project — what follows is what it contains, so you can confirm it loaded right rather than rebuild it. On the plate: all seven parts together: `xy_joint_left_lower_MGN12`, `xy_joint_left_upper_MGN12`,
`xy_joint_right_lower_MGN12`, `xy_joint_right_upper_MGN12`, `x_frame_V2TR_MGN12_left`,
`x_frame_V2TR_MGN12_right`, `probe_retainer_bracket`. No rotation, no brim in the project — the preview shows no
brim outline.
**Parts:** all seven — 8.6 h, 117 g (PrusaSlicer 2.9.6 estimate).
**Check:** Confirm the files are `x_frame_V2TR_MGN12_left/right` (V2TR = the shared V2/Trident R2 carriage,
so `TR` in the name is correct) — **not** the superseded `Superceded_Parts/MGN9_X/x_carriage_frame_*_MGN9` files.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [print plan §6 — conditional / verify items](../../voron-print-plan.md#6-conditional-verify-items)

## Step B04.3 — Pre-print checks

**Do:** Sheet per [00-slicer-setup § Print sheet](00-slicer-setup.md#print-sheet), chamber preheating.
**Check:** Chamber ≥40 °C.

Source: [00-slicer-setup § Print sheet](00-slicer-setup.md#print-sheet) · [00-slicer-setup § Calibration sequence](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B04.4 — Print

**Do:** Print with standing overrides.
**Check:** First layer clean on both XY joint lowers — these are the largest parts on the plate.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B04.5 — Inspect

**Do:** With calipers, dry-fit the MGN12 carriage screw pattern against `x_frame_V2TR_MGN12_left/right`
before committing any heat-set inserts. Check XY joint bores accept the X-axis shafts without reaming.
**Check:** Screw pattern lines up; shafts slide into the joint bores without forcing.

Pause: ~10 min since the last pause — carriage pattern and shaft bores dry-fitted and taken apart again; no inserts set (Ch 05 does that).

Source: [print plan §5.2 — checkpoint after each batch](../../voron-print-plan.md#52-checkpoint-after-each-batch) · [00-slicer-setup § Calibration sequence](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) · [LDO Build Notes / FAQ](https://docs.ldomotors.com/voron/voron2/build-faq)

## Step B04.6 — Sort into bins

**Do:** Sort each plate straight off its diagram (the image at the top of its Load step): the number on a part is the number in the legend, the fill colour is its bin, and the bin id is printed on the part. Bins are listed in [README § Bins](README.md#bins); print their labels from the [bin-labels sheet](../../print/bin-labels.md). **05-XY** also holds B02's `[a]_endstop_pod_D2F_switch` and both cable bridges. **07-X** (the X-carriage halves and probe bracket) is staged at Ch 05 Step 05.45 and fitted in Ch 07 — keep `probe_retainer_bracket` loose in it until the probe decision (Omron barrel diameter) is confirmed.

**B04-P1**

| bin | parts off this plate |
|---|---|
| **05-XY** — XY joints, cable bridge, endstop pod | `xy_joint_left_lower_MGN12`, `xy_joint_left_upper_MGN12`, `xy_joint_right_lower_MGN12`, `xy_joint_right_upper_MGN12` |
| **07-X** — X carriage halves, probe bracket, cable cover | `x_frame_V2TR_MGN12_left`, `x_frame_V2TR_MGN12_right`, `probe_retainer_bracket` |

**Check:** 05-XY: four joint halves plus the pod and bridges; 07-X: two frame halves and the bracket.

Source: [print plan §9 — batch summary](../../voron-print-plan.md#9-machine-readable-batch-summary) · [print plan §2 — which parts gate which step](../../voron-print-plan.md#2-which-parts-gate-the-frame-and-z-drive-steps) · [print/README § Bins](README.md#bins)

---

## Checkpoint B04
- [ ] Gate B passed before B04-P1 started
- [ ] MGN12 carriage screw pattern confirmed against `x_frame_V2TR_MGN12_left/right` before heat-sets
- [ ] XY joint bores accept shafts without reaming
- [ ] Omron probe barrel measured (8 mm vs 9 mm) — correct `probe_retainer_bracket` variant confirmed
- [ ] Confirmed X-carriage is `x_frame_V2TR_MGN12_left/right` (V2TR/Clockwork-2), not the superseded MGN9 carriage

## Common mistakes
- Grabbing a superseded MGN9 X-carriage file by mistake — LDO Build Notes flag this explicitly. `V2TR` is the
  right file: it is the carriage shared by the V2 and the Trident.
- Committing heat-set inserts into the carriage before dry-fitting the screw pattern.
- Reaming an XY joint bore instead of checking the shaft or reprinting.

## Next
Assembly: *Gantry* (p.82–107). Printing: [B05 — Z joints + Z chain](B05-z-joints-and-z-chain.md).
