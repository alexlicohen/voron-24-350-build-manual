# Batch B01 — Z drive assemblies

Every Z-drive part with a bearing seat, so it waits for Gate B (the 625-2RS bore test) — which now runs
early, on a caliper across the printed pocket, so this batch prints second, straight after B00.

```mascot
pose: print
caption: The first real parts. They hold bearings, so Gate B has opinions and it goes first.
```

**Time:** 22.8 h (2 plates) — PrusaSlicer 2.9.6 estimates.

**Sessions:** 2 plate starts (~5 min hands-on each, 15.2 h and 7.6 h unattended) + ~15 min inspect + ~10 min sort into bins.

**Prerequisites:** **Gate B passed** (Step B00.7 — the 625-2RS pocket calipered and seven real inserts set,
both run early on what is already on the bench; Gate B's bearing press and MGN12 rail row wait for the kit
and gate nothing on this plate). Gate A alone does not release this batch. Note: fully completing the *Z Drives and Idlers*
assembly chapter also needs the accent parts from **B02** (`[a]_z_drive_baseplate_a/b`,
`[a]_belt_tensioner_a/b`, `[a]_z_tensioner_9mm_x4`), printed straight after this batch and long before the
kit — plan §9 lists hard prerequisites `B00;B02` for that chapter.

**Printed parts**


| STL | Repo path | Qty | Colour | g ea | Bin |
|---|---|---:|---|---:|---|
| `z_drive_main_a_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | Black | 39.4 | 02-Z0, 02-Z2 (one each) |
| `z_drive_main_b_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | Black | 39.4 | 02-Z1, 02-Z3 (one each) |
| `z_drive_retainer_a_x2.stl` | Voron-2 `STLs/Z_Drive/` | 1 *(second copy; first was on B00)* | Black | 19.5 | 02-Z2 |
| `z_drive_retainer_b_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | Black | 19.5 | 02-Z1, 02-Z3 (one each) |
| `z_motor_mount_a_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | Black | 11.9 | 02-Z0, 02-Z2 (one each) |
| `z_motor_mount_b_x2.stl` | Voron-2 `STLs/Z_Drive/` | 2 | Black | 11.9 | 02-Z1, 02-Z3 (one each) |
| `z_tensioner_bracket_a_x2.stl` | Voron-2 `STLs/Z_Idlers/` | 2 | Black | 13.0 | 02-Z0, 02-Z2 (one each) |
| `z_tensioner_bracket_b_x2.stl` | Voron-2 `STLs/Z_Idlers/` | 2 | Black | 13.0 | 02-Z1, 02-Z3 (one each) |
| `deck_support_3mm_x8.stl` | Voron-2 `STLs/Panel_Mounting/` | 8 | Black | 1.1 | 02-deck |

⚠ **Deck-support thickness (verify):** LDO's Rev D printed-parts guide says "our kit ships with 4 mm deck
panels, use 4 mm deck support clips," but the Rev D 350 BOM lists the deck panel as **3 mm** acrylic (the
4 mm panel is the *bottom* panel). The size-specific BOM wins: print `deck_support_3mm_x8` ×8 now, and
measure the deck panel at Ch 00 Step 00.4 — if it measures 4 mm, reprint `deck_support_4mm_x8` (8 g, 30 min).
The panel only exists on kit day, months after this plate, so the 3 mm set is printed on the BOM's word and
the reprint is the one plate the build may still owe when the cartons land.

**Hardware:** none.

**Read first**

- The parts come in **mirrored pairs**: every `_a` file has a `_b` twin, and each Z corner takes *either* the
  `a` set *or* the `b` set — two corners of each. They are not interchangeable, so Step B01.8 sorts them into
  the four corner bins 02-Z0–Z3 by hand, not four identical sets.
- Checkpoint after B01: 625-2RS (16 mm OD) press-fit into each `z_drive_main` and `z_drive_retainer` bearing
  seat — thumb pressure, no rocking. M3 heat-set bosses on the motor mounts: no bulge, insert flush. Check
  the 4 mm/3 mm deck-support call above.
- Most commonly reprinted here: `z_drive_main_*` — the largest single parts in the batch, most exposed to
  warp at the corners.
- Plate B01-P1 is the longest single plate in the whole build (15.2 h) — start it in the morning, not at bedtime.

## Step B01.1 — Filament prep

**Do:**

1. Confirm the Galaxy Black spool is loaded and dried within the last 2 weeks, or fresh.
2. Spool #1 came off B00 with 748 g by the ledger. This batch alone is 301 g.
**Check:** B01-P1 needs **≥ 201 g** on the spool at start; the [README ledger](README.md#spool-ledger) has spool #1 at 748 g.

Tip: A kitchen scale, if you own one, turns the ledger into a check. It is optional; the ledger works from the slicer grams.

Source: [print plan §4.3 — spool changes](../../voron-print-plan.md#43-spool-changes) · [00-slicer-setup § Drying](00-slicer-setup.md#drying) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B01.2 — Load plate B01-P1

![Plate B01-P1 — sorting diagram](../assets/plates/B01-P1.png)

*Sorting diagram, drawn from the committed project: every part numbered and filled in the colour of its bin, bin id on the part; the legend reads # · STL · bin (chapter · steps). Sort at Step B01.8.*

**Do:**

1. Open `slicer/plates/B01-P1.3mf` with **File → Open Project**. Do not rebuild the plate.
2. Confirm: profile `0.20mm STRUCTURAL @COREONE 0.4 (modified)`, **5 files, 7 objects**, no brim outline.
3. Do not rotate any part.
**Parts:** `z_drive_main_a` ×2 · `z_drive_main_b` ×2 · `z_drive_retainer_a` ×1 · `z_drive_retainer_b` ×2 — 15.2 h, 201 g (PrusaSlicer 2.9.6 estimate).
**Check:** Estimated plate time is **15 h 13 m**; if far off, re-verify profile/overrides before committing an overnight print.

**Helper:** Reads the sorting diagram legend aloud and counts the parts on it while you load.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim)

## Step B01.3 — Pre-print checks

**Do:** Prepare the sheet per [00-slicer-setup § Print sheet](00-slicer-setup.md#print-sheet) with the glue film renewed, confirm the spool is dry, and start the chamber preheating.
**Check:** Chamber reads ≥40 °C before purge.

Source: [00-slicer-setup § Print sheet](00-slicer-setup.md#print-sheet) · [00-slicer-setup § Calibration sequence](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B01.4 — Print plate B01-P1

**Do:** Start in the morning or at the start of a full workday: this is the 15.2 h plate.
**Check:** First layer clean; no corner lift on the `z_drive_main` bodies partway through.

Tip: look at the first layer, the corners after an hour, and again at bedtime. A lifted corner is a stop, not a wait.

Pause: ~5 min since the last pause — B01-P1 running, 15.2 h unattended, door shut. Meanwhile: read Ch 02, sort the last plate, label bins.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B01.5 — Load plate B01-P2

![Plate B01-P2 — sorting diagram](../assets/plates/B01-P2.png)

*Sorting diagram, drawn from the committed project: every part numbered and filled in the colour of its bin, bin id on the part; the legend reads # · STL · bin (chapter · steps). Sort at Step B01.8.*

**Do:**

1. Open `slicer/plates/B01-P2.3mf` with **File → Open Project**. Do not rebuild the plate.
2. Confirm: **5 files, 16 objects**, no brim.
**Parts:** `z_motor_mount_a` ×2 · `z_motor_mount_b` ×2 · `z_tensioner_bracket_a` ×2 · `z_tensioner_bracket_b` ×2 · `deck_support_3mm` ×8 — 7.6 h, 100 g (PrusaSlicer 2.9.6 estimate).
**Check:** All 8 clips on the plate, 3 mm per the BOM; the kit-day caliper decides a 4 mm reprint.

**Helper:** Counts the parts on the sorting diagram and checks the total against the object count.

⚠ `z_motor_mount_a/b` are 42.0 mm tall, borderline aspect. **Only if a motor mount lifts on this print**, add a 5 mm brim to those four objects by hand for the reprint: right-click the object → Add settings → Skirt and brim → Brim width. Never the global setting, per [00-slicer-setup](00-slicer-setup.md#orientation-brim).

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [LDO Rev D printed-parts guide](https://docs.ldomotors.com/en/voron/voron2/printed_part_guide_rev_d) · [LDO Rev D 350 BOM](https://docs.ldomotors.com/en/voron/voron2/350_BOM/Rev_D)

## Step B01.6 — Print plate B01-P2

**Do:** Start after P1 is pulled and inspected.
**Check:** No warp at the corners of the motor mounts.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B01.7 — Inspect

**Do:**

1. Press a 625-2RS bearing, 16 mm OD, into every `z_drive_main` and `z_drive_retainer` bearing seat by thumb: it should seat with no rocking.
2. Check the M3 heat-set bosses on the motor mounts sit flush with no bulge.
**Check:** All bearing seats pass; any that don't → reprint that part, don't proceed with a known-bad Z drive.

Pause: ~15 min since the last pause — every bearing seat tested and the bearings pulled back out; nothing pressed for keeps yet. Do not seat inserts — Ch 02 Step 02.04 does that with the parts sorted.

Source: [print plan §5.2 — checkpoint after each batch](../../voron-print-plan.md#52-checkpoint-after-each-batch) · [00-slicer-setup § Gate B](00-slicer-setup.md#gate-b-bore-and-inserts-now-rail-on-kit-day) · [Voron materials — shrinkage 100 %](https://docs.vorondesign.com/materials.html)

## Step B01.8 — Sort into bins

**Do:**

1. Sort each plate off its diagram: the number on a part is its legend number, the colour its bin.
2. Write bin id, plate id and date on the inside face of every `_a` / `_b` part.

**B01-P1**

| bin | parts off this plate |
|---|---|
| **02-Z0** — Z0 corner (front-left, `_a` hand) | `z_drive_main_a` |
| **02-Z1** — Z1 corner (rear-left, `_b` hand) | `z_drive_main_b`, `z_drive_retainer_b` |
| **02-Z2** — Z2 corner (rear-right, `_a` hand) | `z_drive_main_a`, `z_drive_retainer_a` |
| **02-Z3** — Z3 corner (front-right, `_b` hand) | `z_drive_main_b`, `z_drive_retainer_b` |

**B01-P2**

| bin | parts off this plate |
|---|---|
| **02-Z0** — Z0 corner (front-left, `_a` hand) | `z_motor_mount_a`, `z_tensioner_bracket_a` |
| **02-Z1** — Z1 corner (rear-left, `_b` hand) | `z_motor_mount_b`, `z_tensioner_bracket_b` |
| **02-Z2** — Z2 corner (rear-right, `_a` hand) | `z_motor_mount_a`, `z_tensioner_bracket_a` |
| **02-Z3** — Z3 corner (front-right, `_b` hand) | `z_motor_mount_b`, `z_tensioner_bracket_b` |
| **02-deck** — Deck panel clips | `deck_support_3mm` ×8 |

**Check:** 02-Z0 to 02-Z3 each hold one `z_drive_main`, one `z_drive_retainer`, one `z_motor_mount` and one `z_tensioner_bracket` of the right hand, ids written on the parts; 02-deck holds 8 clips.

**Helper:** Reads each bin label aloud and checks the count against the diagram.

⚠ 02-Z0's `z_drive_retainer_a` is the Gate B coupon printed on B00, so it is not on these plates. B02's blue baseplates and tensioners join these bins next batch.

Tip: Print the bin labels from the [bin-labels sheet](../../print/bin-labels.md). Mark the 02-deck bin "3 mm clips, confirm against the calipered panel".

Pause: ~10 min since the last pause — both plates sorted into 02-Z0 … 02-Z3 and 02-deck, bin ids written on the inside face of every part. Nothing is pressed or inserted; Ch 02 does that from the bins.

Source: [print plan §9 — batch summary](../../voron-print-plan.md#9-machine-readable-batch-summary) · [print plan §2 — which parts gate which step](../../voron-print-plan.md#2-which-parts-gate-the-frame-and-z-drive-steps) · [print/README § Bins](README.md#bins)

---

## While a long plate runs

Four plates in this build run past eight hours and one runs past fifteen. None of them wants watching, but
all of them want three looks: the **first layer**, the **corners after an hour**, and once more **at
bedtime**. A lifted corner is a stop, not a wait — abort, clear the sheet, renew the glue film and restart,
rather than letting the plate print another six hours on top of it.

```mascot
pose: pause
caption: Fifteen hours. Watch the first layer, then walk away. A champion can supervise from a spool.
```

The rest of the time the printer is working for you and the bench is free. In order of value: read the
assembly chapter the running batch feeds, sort and label the *previous* plate into its bins, and print or
write the bin labels you are still missing.

## Checkpoint B01
- [ ] Gate B passed before B01-P1 started (Step B00.7)
- [ ] 625-2RS bearing press-fit into all `z_drive_main_a/b` seats — thumb pressure, no rocking
- [ ] 625-2RS bearing press-fit into all `z_drive_retainer_a/b` seats — thumb pressure, no rocking
- [ ] M3 heat-set bosses on motor mounts: flush, no bulge
- [ ] *(kit day)* Deck panel measured; correct deck-support thickness confirmed or `deck_support_4mm_x8` reprinted
- [ ] No corner lift or delamination on any `z_drive_main` body
- [ ] Bins 02-Z0–Z3 each hold one matched set of the right hand, bin id written on every part; 8 clips in 02-deck

## Common mistakes
- Starting the 15.2 h P1 plate late in the day and having it finish unattended overnight with no chance to
  abort a bad first layer.
- Starting B01 on Gate A alone — the bore fit on the real bearing is what protects these 22.8 h.
- Trying to make four identical sets from two `a` and two `b` of each part — the sets are mirrored; the corner bins are not interchangeable.
- Assuming the deck-support thickness without measuring the actual panel.
- Forcing a tight bearing seat with a press instead of reducing extrusion multiplier for the reprint.

## Next
Assembly: *Z Drives and Idlers* (Ch 02), with B02's accent parts already on the shelf. Printing: [B03 — A/B drive units + front idlers](B03-ab-drive-units-and-front-idlers.md).
