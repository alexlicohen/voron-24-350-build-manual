# Batch B03 — A/B drive units + front idlers

```mascot
pose: print
caption: The corners the belts turn on. Flange seats again, so Gate B comes first.
```

**Time:** 8.5 h (1 plate) — PrusaSlicer 2.9.6 estimates.

**Sessions:** 1 plate start (~5 min hands-on, 8.5 h unattended) + ~15 min inspect and bin.

**Prerequisites:** **Gate B passed** (Step B00.7 — these are F695 flange seats; the caliper and insert rows
run early, on what is already on the bench). B02 is not a print prerequisite: its accent `[a]_cable_cover`,
`[a]_z_chain_retainer_bracket` and `[a]_tensioner_left/right` printed one batch earlier, at B02, and are
already in 04-A / 04-B.

**Printed parts**


| STL | Repo path | Qty | Colour | g ea | Bin |
|---|---|---:|---|---:|---|
| `a_drive_frame_lower.stl` | Voron-2 `STLs/Gantry/AB_Drive_Units/` | 1 | Black | 22.4 | 04-A |
| `a_drive_frame_upper.stl` | Voron-2 `STLs/Gantry/AB_Drive_Units/` | 1 | Black | 21.8 | 04-A |
| `b_drive_frame_lower.stl` | Voron-2 `STLs/Gantry/AB_Drive_Units/` | 1 | Black | 20.5 | 04-B |
| `b_drive_frame_upper.stl` | Voron-2 `STLs/Gantry/AB_Drive_Units/` | 1 | Black | 21.3 | 04-B |
| `front_idler_left_lower.stl` | Voron-2 `STLs/Gantry/Front_Idlers/` | 1 | Black | 7.7 | 04-B |
| `front_idler_left_upper.stl` | Voron-2 `STLs/Gantry/Front_Idlers/` | 1 | Black | 14.1 | 04-B |
| `front_idler_right_lower.stl` | Voron-2 `STLs/Gantry/Front_Idlers/` | 1 | Black | 13.8 | 04-A |
| `front_idler_right_upper.stl` | Voron-2 `STLs/Gantry/Front_Idlers/` | 1 | Black | 7.9 | 04-A |

**Hardware:** none.

**Read first**

- Checkpoint after B03: the **F695 flange seats** caliper 15.00 mm now, and the two halves of each drive
  unit must close flat with no gap. On kit day the real **F695-2RS** (13 mm OD, flanged) bearing/spacer
  stacks must drop into those seats without reaming. (625-2RS is the *Z-drive* bearing, B01 — not this batch.)
- Most commonly reprinted here: `a/b_drive_frame_lower` — the bearing seats are the tightest fit in the machine.
- A and B share one plate (merged 2026-09-06, one swap instead of two), so a failed plate costs both drive
  units. Watch the first layer before you walk away from an 8.5 h print.

## Step B03.1 — Filament prep

**Do:** Swap the accent spool for Galaxy Black: Unload, Load Filament → ASA, purge until no blue shows.
The ledger has B03 on spool #1 with 447 g, leaving 328 g after. Sheet per [00-slicer-setup § Print sheet](00-slicer-setup.md#print-sheet).
**Check:** Purge clean black, no blue streak.

Source: [print plan §4.3 — spool changes](../../voron-print-plan.md#43-spool-changes) · [00-slicer-setup § Drying](00-slicer-setup.md#drying) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B03.2 — Load plate B03-P1 (both sides)

![Plate B03-P1 — sorting diagram](../assets/plates/B03-P1.png)

*Sorting diagram, drawn from the committed project: every part numbered and filled in the colour of its bin, bin id on the part; the legend reads # · STL · bin (chapter · steps). Sort at Step B03.5.*

**Do:** Open `slicer/plates/B03-P1.3mf` with **File → Open Project**. Arrangement, per-object brims and overrides ship in the project; confirm what loaded, don't rebuild it. No rotation, no brim in the project.
**Parts:** 8 objects — 8.5 h, 119 g (PrusaSlicer 2.9.6 estimate); `a_drive_frame_lower`; `a_drive_frame_upper`; `front_idler_right_lower`; `front_idler_right_upper`; `b_drive_frame_lower`; `b_drive_frame_upper`; `front_idler_left_lower`; `front_idler_left_upper`.
**Check:** Parts sit flat as shipped; no brim outline in the preview.

**Helper:** Reads the sorting diagram legend aloud and counts the parts on it while you load.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim)

## Step B03.3 — Print plate B03-P1

**Do:** Print with standing overrides.
**Check:** No warp at drive-frame corners.

Pause: ~5 min since the last pause — plate started; nothing to do until it finishes.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B03.4 — Inspect

**Do:**

1. Now: caliper each drive frame half's F695 flange seat, a 15.00 mm pocket 4.00 mm deep.
2. Now: dry-fit each drive unit's two halves, which must close flat.
3. Kit day: drop a real F695-2RS in, no rocking.
**Check:** Every seat reads 15.00 mm ±0.15 and both halves close with no visible gap.

Pause: ~10 min since the last pause — seats calipered, halves dry-fitted and separated again. Nothing pressed for keeps; the bearings themselves are a kit-day row.

Source: [print plan §5.2 — checkpoint after each batch](../../voron-print-plan.md#52-checkpoint-after-each-batch) · [00-slicer-setup § Gate B](00-slicer-setup.md#gate-b-bore-and-inserts-now-rail-on-kit-day) · [LDO Build Notes / FAQ](https://docs.ldomotors.com/voron/voron2/build-faq)

## Step B03.5 — Sort into bins

**Do:**

1. Sort the plate off its diagram: number to legend, colour to bin, bin id on the part.
2. Mark plate id and date on a hidden face.
3. A is the right-hand side, B the left.

**B03-P1**

| bin | parts off this plate |
|---|---|
| **04-A** — A drive unit + A (right) front idler | `a_drive_frame_lower`, `a_drive_frame_upper`, `front_idler_right_lower`, `front_idler_right_upper` |
| **04-B** — B drive unit + B (left) front idler | `b_drive_frame_lower`, `b_drive_frame_upper`, `front_idler_left_lower`, `front_idler_left_upper` |

**Check:** 04-A and 04-B each hold one drive-frame pair, one idler pair and one blue tensioner.

**Helper:** Writes the bin id and the date on the inside face of each part.

Tip: the blue `[a]_tensioner_right` and `[a]_tensioner_left` from B02 are already in these two bins. Print bin labels from the [bin-labels sheet](../../print/bin-labels.md).

Pause: ~10 min since the last pause — both bins sorted and labelled, A-side and B-side parts kept apart. Nothing is pressed or bolted; Ch 04 builds from the bins.

Source: [print plan §9 — batch summary](../../voron-print-plan.md#9-machine-readable-batch-summary) · [print plan §2 — which parts gate which step](../../voron-print-plan.md#2-which-parts-gate-the-frame-and-z-drive-steps) · [print/README § Bins](README.md#bins)

---

## Checkpoint B03
- [ ] Gate B passed before B03-P1 started
- [ ] F695 flange seats in `a/b_drive_frame_lower/upper` caliper 15.00 mm ±0.15
- [ ] *(kit day)* a real F695-2RS sits in each seat with no rocking
- [ ] Drive unit halves (upper+lower) close flat with no visible gap, both A and B
- [ ] No corner warp on any of the eight parts
- [ ] A-side parts in 04-A, B-side parts in 04-B

## Common mistakes
- Mixing A-side and B-side parts in one bag — they are not interchangeable.
- Force-closing a warped drive-frame half instead of reprinting it.
- Skipping the dry-fit and only discovering the bearing-seat gap during final assembly.

## Next
Assembly: *A/B Drives and Idlers* (p.62–81). Printing: [B04 — XY joints + X carriage](B04-xy-joints-and-x-carriage.md).
