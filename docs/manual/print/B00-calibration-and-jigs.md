# Batch B00 — Calibration & jigs

One plate: the dimensional gate for the whole build, plus two rail-alignment jigs. Nothing else prints
until this plate passes.

**Time:** 4.0 h (1 plate) — PrusaSlicer 2.9.6 estimate, sliced from `slicer/plates/B00-P1.3mf`.

**Prerequisites:** none — this is the first batch. Slicer set up per [00-slicer-setup.md](00-slicer-setup.md).

**Printed parts**


| STL | Repo path | Qty | Colour | g ea |
|---|---|---:|---|---:|
| `Voron_Design_Cube_v7.stl` | Voron-2 `STLs/Test_Prints/` | 1 | Black | 16.2 |
| `Heatset_Practice.stl` | Voron-2 `STLs/Test_Prints/` | 1 | Black | 6.5 |
| `MGN12_rail_guide_x2.stl` | Voron-2 `STLs/Tools/` | 2 | Black | 3.2 |
| `MGN9_rail_guide_x2.stl` | Voron-2 `STLs/Tools/` | 2 | Black | 2.7 |
| `pulley_jig.stl` | Voron-2 `STLs/Tools/` | 1 | Black | 2.8 |
| `z_drive_retainer_a_x2.stl` | Voron-2 `STLs/Z_Drive/` | 1 *(of the 2 needed — this is the bearing-fit coupon and a real part)* | Black | 19.5 |

**Hardware:** none.

**Read first**

- The seven-item gate in [00-slicer-setup.md](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) — nothing proceeds until all seven pass.
- Most commonly reprinted here: the cube, until the profile is right.
- `z_drive_retainer_a` on this plate is deliberate — it's your bearing-press-fit coupon **and** one of the two you need for B01, so nothing is wasted.

## Step B00.1 — Filament prep

**Do:** Mount a fresh or recently-dried (≤2 weeks open) spool of Prusament ASA Galaxy Black. Load it in the
Core One+, confirm the `Prusament ASA @COREONE HF0.4` filament profile is selected (HF — the machine has the
high-flow nozzle).
**Check:** Purge is clean black, no PLA/PETG streaking from a prior print.

Source: [print plan §4.3 — spool changes](../../voron-print-plan.md#43-spool-changes) · [00-slicer-setup § Drying](00-slicer-setup.md#drying) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B00.2 — Load plate B00-P1

![Plate B00-P1](../assets/plates/B00-P1.png)

**Do:** Open `slicer/plates/B00-P1.3mf` (**File → Open Project**). The arrangement, the per-object brims and every override are already in the project — what follows is what it contains, so you can confirm it loaded right rather than rebuild it. It carries printer `Prusa CORE One HF0.4 nozzle`, print
`0.20mm STRUCTURAL @COREONE 0.4` with the overrides from [00-slicer-setup.md](00-slicer-setup.md), and filament
`Prusament ASA @COREONE HF0.4` with shrinkage compensation XY/Z zeroed. Confirm all six parts are on the bed: `Voron_Design_Cube_v7`, `Heatset_Practice`,
`MGN12_rail_guide_x2` ×2, `MGN9_rail_guide_x2` ×2, `pulley_jig`, `z_drive_retainer_a_x2` ×1. Do not change which face any part sits on — all ship pre-oriented (rotating about Z to fit the plate is
fine).
**Parts:** all six items above — 4.0 h, 52 g (PrusaSlicer 2.9.6 estimate).
**Check:** The slicer reads **3 h 58 m / 51.7 g**. It is the same file these numbers came from, so anything
else means the project did not load its own configuration — stop and check before printing.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [Voron materials — shrinkage 100 %](https://docs.vorondesign.com/materials.html)

## Step B00.3 — Pre-print checks

**Do:** Confirm chamber has reached 40 °C minimum before the print starts (this is the slicer's built-in
gate on the ASA filament profile — don't override it). Confirm the smooth/satin sheet is installed, clean
with IPA.
**Check:** Chamber temp reads ≥40 °C on the display before the nozzle purges.

Source: [00-slicer-setup § Calibration sequence](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B00.4 — Print

**Do:** Start the plate. Watch the first layer for at least the first 2–3 minutes — this is the abort
window the 1-loop skirt buys you.
**Check:** First layer is smooth, no gaps between beads, no ridging (Ellis' smooth-bottom method).

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B00.5 — Inspect

**Do:** Once cool, remove the plate and run the full seven-item gate from
[00-slicer-setup.md](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade):
cube X/Y (30.00 mm ±0.15 mm), cube Z (30.00 mm ±0.10 mm), first-layer-vs-mid-height X delta (≤0.15 mm),
cube corner snap (no delamination), `Heatset_Practice` insert flush ±0.2 mm proud with no boss bulge >0.2 mm,
`MGN12_rail_guide` slides onto the real MGN12 rail with light finger pressure, `z_drive_retainer_a`'s
625-2RS bore (16 mm OD) takes the bearing with thumb pressure and no rocking.
**Check:** All seven pass. Any failure → adjust per the "if out of spec" column in
[00-slicer-setup.md](00-slicer-setup.md), reprint this plate, do not proceed to B01.

Source: [print plan §5.2 — checkpoint after each batch](../../voron-print-plan.md#52-checkpoint-after-each-batch) · [00-slicer-setup § Calibration sequence](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) · [Ellis' Print Tuning Guide](https://ellis3dp.com/Print-Tuning-Guide/) · [Voron materials — shrinkage 100 %](https://docs.vorondesign.com/materials.html)

## Step B00.6 — Label and bin

**Do:** Bin the two rail guides and the pulley jig together, labelled "Z-drive tooling — Frame". Set the
`z_drive_retainer_a` aside with the B01 parts (it's the coupon *and* the first of the two needed). The cube
and `Heatset_Practice` are consumables — keep the cube as the reference coupon for later re-checks (e.g.
after the Gen 2 upgrade).
**Check:** Nothing from this plate is wasted — even the test coupons are either reused (rail guides,
retainer) or kept as reference (cube).

Source: [print plan §9 — batch summary](../../voron-print-plan.md#9-machine-readable-batch-summary) · [print plan §2 — which parts gate which step](../../voron-print-plan.md#2-which-parts-gate-the-frame-and-z-drive-steps)

---

## Checkpoint B00
- [ ] Cube X and Y both within 30.00 mm ±0.15 mm
- [ ] Cube Z within 30.00 mm ±0.10 mm
- [ ] First-layer-vs-mid-height X delta ≤0.15 mm
- [ ] Cube corner snap test: no delamination
- [ ] `Heatset_Practice`: 3/3 inserts flush to ≤0.2 mm proud, no boss bulge >0.2 mm
- [ ] `MGN12_rail_guide` fits the real MGN12 rail with light finger pressure
- [ ] `z_drive_retainer_a` 625-2RS bore: bearing presses in by thumb, no rocking
- [ ] Shrinkage compensation XY and Z confirmed at 0 % in the filament profile
- [ ] `z_drive_retainer_a` set aside for B01

## Common mistakes
- Skipping the chamber-preheat gate — ASA's first layer on a cold bed looks fine and then lifts at hour 2.
- Reaching for negative XY compensation to fix an oversized cube — wrecks bearing fits everywhere else; use extrusion multiplier instead.
- Rushing the `Heatset_Practice` coupon — technique (iron temp/speed) matters more than any slicer setting here.
- Printing B01 before all seven checks pass "because it's close enough."

## Next
Assembly: begin *Frame* squaring (no printed parts required — can start day the kit lands). Printing: [B01 — Z drive assemblies](B01-z-drive-assemblies.md).
