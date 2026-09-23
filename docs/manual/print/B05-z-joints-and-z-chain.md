# Batch B05 — Z joints + Z chain

```mascot
pose: print
caption: Z joints and chain links. Small, numerous, identical. Count them now, not halfway through the chain.
```

**Time:** 6.4 h (1 plate) — PrusaSlicer 2.9.6 estimate.

**Sessions:** 1 plate start (~5 min hands-on, 6.4 h unattended) + ~10 min inspect and bin.

**Prerequisites:** **Gate B passed** (Step B00.7 — the printed bores and the insert bosses; the caliper and insert rows run early, on what is already on the bench). B02 and B04 feed
the same assembly chapters; neither is a print prerequisite.

**Printed parts**


| STL | Repo path | Qty | Colour | g ea | Bin |
|---|---|---:|---|---:|---|
| `z_joint_lower_x4.stl` | Voron-2 `STLs/Gantry/Z_Joints/` | 4 | Black | 9.1 | 06-Z-joints |
| `z_joint_upper_x4.stl` | Voron-2 `STLs/Gantry/Z_Joints/` | 4 | Black | 6.6 | 06-Z-joints |
| `z_chain_bottom_anchor.stl` | Voron-2 `STLs/Gantry/` | 1 | Black | 9.1 | 10-chains |
| `z_chain_guide.stl` | Voron-2 `STLs/Gantry/` | 1 | Black | 6.0 | 10-chains |
| `z_rail_stop_x4.stl` | LDOVoron2 `STLs/` | 4 | Black | 1.4 | 06-Z-joints |

Print **4× `z_joint_upper_x4`** and **zero** `z_joint_upper_hall_effect.stl` — that variant exists only for
hall-effect XY endstops, which this kit does not use.

**Hardware:** none.

**Read first**

- Checkpoint after B05: `z_joint_lower`'s four M3 holes caliper 3.40 mm on a 15.0 × 16.0 mm pattern — there
  is no larger bore in this part. `z_joint_upper` must sit square on the extrusion.
- Most commonly reprinted here: `z_joint_lower_x4`.
- The LDO `z_rail_stop` is optional but stops a Z carriage from falling off the top of a rail and spilling its balls.

## Step B05.1 — Filament prep

**Do:** Galaxy Black, still spool #1. The ledger has 211 g on it here and 133 g after, which is the stub B06 leaves behind. Sheet per [00-slicer-setup § Print sheet](00-slicer-setup.md#print-sheet).
**Check:** Clean purge; ≥78 g on the spool.

Source: [print plan §4.3 — spool changes](../../voron-print-plan.md#43-spool-changes) · [00-slicer-setup § Drying](00-slicer-setup.md#drying) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B05.2 — Load plate B05-P1

![Plate B05-P1 — sorting diagram](../assets/plates/B05-P1.png)

*Sorting diagram, drawn from the committed project: every part numbered and filled in the colour of its bin, bin id on the part; the legend reads # · STL · bin (chapter · steps). Sort at Step B05.5.*

**Do:** Open `slicer/plates/B05-P1.3mf` with **File → Open Project**. Arrangement, per-object brims and overrides are already in the project, so confirm it loaded rather than rebuild it. No rotation, no brim. Do **not** include `z_joint_upper_hall_effect.stl`.
**Parts:** the fourteen pieces above — 6.4 h, 78 g (PrusaSlicer 2.9.6 estimate); `z_joint_lower_x4` ×4; `z_joint_upper_x4` ×4; `z_chain_bottom_anchor`; `z_chain_guide`; `z_rail_stop_x4` ×4.
**Check:** File list contains only the D2F-compatible `z_joint_upper_x4`, not the hall-effect variant.

**Helper:** Names the bin colour of each part on the sorting diagram while you open the project.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [LDO Build Notes / FAQ](https://docs.ldomotors.com/voron/voron2/build-faq)

## Step B05.3 — Print

**Do:** Print with standing overrides.
**Check:** First layer clean; no warp on the small joint parts.

Pause: ~5 min since the last pause — plate started; nothing to do until it finishes.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B05.4 — Inspect

**Do:**

1. Now: caliper `z_joint_lower`'s four M3 holes, 3.40 mm on a 15.0 × 16.0 mm pattern.
2. Now: sit each `z_joint_upper` square against a flat reference face.
3. Kit day: fit a lower and an upper onto a real Z carriage.
**Check:** Every M3 hole reads 3.40 mm ±0.10 and no `z_joint_upper` rocks on the flat.

Pause: ~10 min since the last pause — joints calipered and squared on the flat, then set down again; nothing pressed, and the carriage fit is a kit-day row.

Source: [print plan §5.2 — checkpoint after each batch](../../voron-print-plan.md#52-checkpoint-after-each-batch) · [00-slicer-setup § Calibration sequence](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-any-toolchain-change)

## Step B05.5 — Sort into bins

**Do:** Sort off the plate diagram: number to legend, colour to bin, bin id on the part. Mark plate id and date on a hidden face. Labels: [bin-labels sheet](../../print/bin-labels.md). The chain anchor and guide go to **10-chains**, not 06-Z-joints.

**B05-P1**

| bin | parts off this plate |
|---|---|
| **06-Z-joints** — Z joints, belt clips, rail stops | `z_joint_lower` ×4, `z_joint_upper` ×4, `z_rail_stop` ×4 |
| **10-chains** — Z cable chain anchor, guide, retainer | `z_chain_bottom_anchor`, `z_chain_guide` |

**Check:** 4 joint pairs and 4 rail stops in 06-Z-joints with B02's eight belt clips; anchor and guide in 10-chains.

**Helper:** Matches each part's number to the diagram legend and drops it in its bin.


Pause: ~10 min since the last pause — joints in 06-Z-joints, anchor and guide in 10-chains, bin ids written. Nothing is pressed and the rail stops stay bagged.

Source: [print plan §9 — batch summary](../../voron-print-plan.md#9-machine-readable-batch-summary) · [print plan §2 — which parts gate which step](../../voron-print-plan.md#2-which-parts-gate-the-frame-and-z-drive-steps) · [print/README § Bins](README.md#bins)

---

## Checkpoint B05
- [ ] Gate B passed before B05-P1 started
- [ ] Every `z_joint_lower`'s four M3 holes caliper 3.40 mm ±0.10 on a 15.0 × 16.0 mm pattern
- [ ] *(kit day)* lower and upper joints fit a real Z carriage and extrusion end
- [ ] Every `z_joint_upper` sits square on a test extrusion
- [ ] Confirmed zero copies of `z_joint_upper_hall_effect.stl` were printed
- [ ] `z_rail_stop_x4` fitted or bagged for fitting

## Common mistakes
- Accidentally slicing the hall-effect Z-joint variant instead of the D2F one.
- Looking for an 8 mm shaft bore in `z_joint_lower`. There is none: the part's largest hole is 4.0 mm, and the M3 pattern is what a caliper checks.

## Next
Assembly: *Z Axis* (p.108–123) and *A/B Belts* (p.124–145). Printing: [B06 — Toolhead: Stealthburner, Clockwork 2, Klicky](B06-toolhead-sb-cw2-klicky.md).
