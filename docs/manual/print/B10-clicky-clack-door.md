# Batch B10 — Clicky-Clack door

**Time:** 5.7 h (1 plate) — PrusaSlicer 2.9.6 estimate — plus the orange `Handle` printed back in B02.

**Prerequisites:** B00, B02 (the orange `Handle`), B09.

**Printed parts**


| STL | Repo path | Qty | Colour | g ea |
|---|---|---:|---|---:|
| `Handle-Hinge_Bottom.stl` | whopping_Voron_mods `clickyclacky_door/STLs/` | 1 | Black | 17.1 |
| `Handle-Hinge_Top.stl` | whopping_Voron_mods `clickyclacky_door/STLs/` | 1 | Black | 17.1 |
| `Hinge-L-sleeve-2X.stl` | whopping_Voron_mods `clickyclacky_door/STLs/` | 2 | Black | 9.0 |
| `Hinge-L-solid-2X.stl` | whopping_Voron_mods `clickyclacky_door/STLs/` | 2 | Black | 9.2 |
| `Latch.stl` | whopping_Voron_mods `clickyclacky_door/STLs/` | 1 | Black | 8.4 |
| `Panel_Clip.stl` | whopping_Voron_mods `clickyclacky_door/STLs/` | 1 | Black | 0.9 |
| `Handle.stl` | *(printed in B02, orange)* | 1 | Orange | 33.7 |

The "2X" in the filenames means print two copies; each file contains one body. Cross-check against the
mod's BOM: 6 split bushings and 4 M5×45 dowel pins = 2 door hinges + 2 handle hinges.

**Because you're fitting Clicky-Clack, do not print:** `door_hinge_x6`, `handle_a_x2`, `handle_b_x2`,
`latch_x2` (Voron), nor LDO's `LDO Door/` set. That also means losing the LDO kit-number nameplate — if you
want it, print `LDO Door/handle_b_nameplate.stl` and glue it elsewhere.

⚠ **Open question:** the Clicky-Clack kit was ordered in "Blue" — Fabreeko's page doesn't state what the
colour option governs. Almost certainly the anodised door-frame extrusions (visible blue trim around the
front opening, matching the blue LDO frame but sitting next to the orange/black scheme). Confirm with
Fabreeko before it ships **(unverified)**.

**Hardware:** none.

**Read first**

- Checkpoint after B10: sleeve bearings must tap into the hinge sleeves without splitting the part; M5×45
  pin into the "solid" half should be a **very** tight hammer fit with ~20 mm proud.
- Most commonly reprinted here: `Hinge-L-solid-2X` (split risk on the pin press).
- Mirror the two `Hinge-L-*` parts in the slicer if you want the door to swing the other way; handle and
  latch are symmetric. **PrusaSlicer 3.0 preview cannot mirror** — slice this batch in 2.9.6, or mirror the
  STL outside the slicer.
- `Hinge-L-sleeve/solid-2X` are on the tall/narrow brim list (55.0 mm, footprint 20.9×19.5) — **5 mm brim**.
  `Latch.stl` (58.0 mm) also gets a **5 mm brim**.

## Step B10.1 — Filament prep

**Do:** Galaxy Black, confirm ≥76 g remaining. The orange `Handle` from B02 should already be set aside.
**Check:** Clean purge.

Source: [print plan §4.3 — spool changes](../../voron-print-plan.md#43-spool-changes) · [00-slicer-setup § Drying](00-slicer-setup.md#drying) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B10.2 — Load plate B10-P1

![Plate B10-P1](../assets/plates/B10-P1.png)

**Do:** Open `slicer/plates/B10-P1.3mf` (**File → Open Project**). The arrangement, the per-object brims and every override are already in the project — what follows is what it contains, so you can confirm it loaded right rather than rebuild it. On the plate: `Handle-Hinge_Bottom`, `Handle-Hinge_Top`, `Hinge-L-sleeve-2X` ×2, `Hinge-L-solid-2X` ×2,
`Latch`, `Panel_Clip`. Apply 5 mm brim to `Hinge-L-sleeve-2X`, `Hinge-L-solid-2X`, and `Latch`. Mirror the
`Hinge-L-*` parts now if you want the door to swing the opposite way — in **2.9.6**; the 3.0 preview has no
mirror tool.
**Parts:** the six black parts above — 5.7 h, 76 g (PrusaSlicer 2.9.6 estimate).
**Check:** Brim applied to the three tall/narrow parts; mirroring decision made before slicing, not after.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [Clicky-Clack door README](https://github.com/tanaes/whopping_Voron_mods/tree/main/clickyclacky_door)

## Step B10.3 — Pre-print checks

**Do:** Chamber preheated, sheet clean.
**Check:** Chamber ≥40 °C.

Source: [00-slicer-setup § Calibration sequence](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B10.4 — Print

**Do:** Print with standing overrides.
**Check:** The four hinge-sleeve/solid parts print upright and stable through their full 55–58 mm height —
watch the first 10 mm for any brim lift.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B10.5 — Inspect

**Do:** Tap a split bushing into each hinge sleeve — should seat without splitting the part. Test-fit an
M5×45 dowel pin into a `Hinge-L-solid` half — should be a very tight hammer fit with ~20 mm proud.
**Check:** No splitting on the sleeve press; pin fit is tight, not loose, with the correct proud length.

Source: [print plan §5.2 — checkpoint after each batch](../../voron-print-plan.md#52-checkpoint-after-each-batch) · [00-slicer-setup § Calibration sequence](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) · [Clicky-Clack door README](https://github.com/tanaes/whopping_Voron_mods/tree/main/clickyclacky_door)

## Step B10.6 — Label and bin

**Do:** Bring the orange `Handle` (from B02) together with this plate's six black parts for
**Panels (front door)** install, replacing the stock two-door assembly entirely.
**Check:** All seven Clicky-Clack parts (6 black + 1 orange) reunited and labelled together.

Source: [print plan §9 — batch summary](../../voron-print-plan.md#9-machine-readable-batch-summary) · [print plan §2 — which parts gate which step](../../voron-print-plan.md#2-which-parts-gate-the-frame-and-z-drive-steps)

---

## Checkpoint B10
- [ ] Split bushings tap into hinge sleeves without splitting the part
- [ ] M5×45 dowel pin is a tight hammer fit into `Hinge-L-solid`, ~20 mm proud
- [ ] Hinge mirroring decision confirmed against desired door swing direction
- [ ] Orange `Handle` (B02) reunited with the black hardware for assembly
- [ ] Clicky-Clack "Blue" trim question resolved with Fabreeko before/at install

## Common mistakes
- Forgetting to mirror the `Hinge-L-*` parts and getting a door that swings the wrong way.
- Pressing the M5×45 dowel pin in loose instead of a tight hammer fit — the door will rack.
- Printing the stock Voron/LDO door parts alongside Clicky-Clack "just in case."

## Next
Assembly: front door install (*Panels*, front door), replacing the stock two-door assembly. This is the
last print batch — proceed to final assembly and startup once all prior batches' checkpoints are clear.
