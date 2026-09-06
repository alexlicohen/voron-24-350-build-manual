# Batch B10 — Clicky-Clack door

**Time:** 5.7 h (1 plate) — PrusaSlicer 2.9.6 estimate — plus the orange `Handle` printed back in B02.

**Sessions:** 1 plate start (~5 min hands-on, 5.7 h unattended) + ~10 min inspect and bin, plus the bushing and
pin test on kit day.

**Prerequisites:** **Gate A** (re-passed after the Gen 2 upgrade, as for B08) and B09 — the last pre-kit
batch. B02's orange `Handle` joins these parts at B10.6. No bearing seat here, so Gate B is not needed.

**Printed parts**


| STL | Repo path | Qty | Colour | g ea | Bin |
|---|---|---:|---|---:|---|
| `Handle-Hinge_Bottom.stl` | whopping_Voron_mods `clickyclacky_door/STLs/` | 1 | Black | 17.1 | 11-door |
| `Handle-Hinge_Top.stl` | whopping_Voron_mods `clickyclacky_door/STLs/` | 1 | Black | 17.1 | 11-door |
| `Hinge-L-sleeve-2X.stl` | whopping_Voron_mods `clickyclacky_door/STLs/` | 2 | Black | 9.0 | 11-door |
| `Hinge-L-solid-2X.stl` | whopping_Voron_mods `clickyclacky_door/STLs/` | 2 | Black | 9.2 | 11-door |
| `Latch.stl` | whopping_Voron_mods `clickyclacky_door/STLs/` | 1 | Black | 8.4 | 11-door |
| `Panel_Clip.stl` | whopping_Voron_mods `clickyclacky_door/STLs/` | 1 | Black | 0.9 | 11-door |
| `Handle.stl` | *(printed in B02, orange)* | 1 | Orange | 33.7 |  |

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
  pin into the "solid" half should be a **very** tight hammer fit with ~20 mm proud. Both need the
  Clicky-Clack kit's hardware, so the test is on kit day.
- Most commonly reprinted here: `Hinge-L-solid-2X` (split risk on the pin press).
- **Door swing — decide now, from where the machine will live.** As designed the hinges are on the **left**
  and the door opens from the right (`Hinge-L`). Mirror both `Hinge-L-*` files only if the printer's left
  side will be against a wall; handle and latch are symmetric. **PrusaSlicer 3.0 preview cannot mirror** —
  slice this batch in 2.9.6, or mirror the STL outside the slicer.
  [src](https://github.com/tanaes/whopping_Voron_mods/tree/main/clickyclacky_door)
- `Hinge-L-sleeve/solid-2X` (55.0 mm on a 20.9×19.5 footprint) and `Latch.stl` (58.0 mm) carry a **5 mm brim
  already in the project**; `Handle-Hinge_*` and `Panel_Clip` have none. Verify in the preview, never add.

## Step B10.1 — Filament prep

**Do:** Galaxy Black, confirm ≥76 g remaining; the ledger has this plate on spool #2 after B09. The orange
`Handle` from B02 should already be set aside. Sheet per [00-slicer-setup § Print sheet](00-slicer-setup.md#print-sheet).
**Check:** Clean purge.

Source: [print plan §4.3 — spool changes](../../voron-print-plan.md#43-spool-changes) · [00-slicer-setup § Drying](00-slicer-setup.md#drying) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B10.2 — Load plate B10-P1

![Plate B10-P1 — sorting diagram](../assets/plates/B10-P1.png)

*Sorting diagram, drawn from the committed project: every part numbered and filled in the colour of its bin, bin id on the part; the legend reads # · STL · bin (chapter · steps). Sort at Step B10.6.*

**Do:** Open `slicer/plates/B10-P1.3mf` with **File → Open Project**; the arrangement, brims and overrides are already in it. Mirror the four `Hinge-L-*` objects in **2.9.6** only if the door must open the other way; the 3.0 preview has no mirror tool.
**Parts:** `Handle-Hinge_Bottom`, no brim · `Handle-Hinge_Top`, no brim · `Hinge-L-sleeve-2X` ×2, **5 mm brim already in the project** · `Hinge-L-solid-2X` ×2, **5 mm brim** · `Latch`, **5 mm brim** · `Panel_Clip`, no brim · 6 files, 8 objects — 5.7 h, 76 g (PrusaSlicer 2.9.6 estimate).
**Check:** The preview shows the brim outline on the four hinge parts and `Latch`, and on nothing else;
swing decision made before slicing, not after.

Source: [print plan §3 — the batches](../../voron-print-plan.md#3-the-batches) · [00-slicer-setup § Committed projects](00-slicer-setup.md#committed-projects-open-the-plate-dont-rebuild-it) · [00-slicer-setup § Orientation & brim](00-slicer-setup.md#orientation-brim) · [Clicky-Clack door README](https://github.com/tanaes/whopping_Voron_mods/tree/main/clickyclacky_door)

## Step B10.3 — Pre-print checks

**Do:** Sheet per [00-slicer-setup § Print sheet](00-slicer-setup.md#print-sheet), chamber preheating.
**Check:** Chamber ≥40 °C.

Source: [00-slicer-setup § Print sheet](00-slicer-setup.md#print-sheet) · [00-slicer-setup § Calibration sequence](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) · [Prusa KB — ASA](https://help.prusa3d.com/article/asa_1809)

## Step B10.4 — Print

**Do:** Print with standing overrides.
**Check:** The four hinge-sleeve/solid parts print upright and stable through their full 55–58 mm height;
watch the first 10 mm for any brim lift.

Pause: ~5 min since the last pause — plate started; nothing to do until it finishes.

Source: [00-slicer-setup § Overrides](00-slicer-setup.md#overrides) · [print plan §4.1 — how these numbers were produced](../../voron-print-plan.md#41-how-these-numbers-were-produced)

## Step B10.5 — Inspect

**Do:**

1. Snap the five brims off; check the bases for scarring.
2. On kit day, tap a split bushing into each hinge sleeve.
3. Test-fit an M5×45 dowel pin into a `Hinge-L-solid` half: very tight hammer fit, ~20 mm proud.
**Check:** Brims off clean. Kit day: no splitting on the sleeve press; pin fit is tight, not loose, with the
correct proud length.

Pause: ~10 min since the last pause — brims off, parts bagged; the bushing and pin tests wait for the kit.

Source: [print plan §5.2 — checkpoint after each batch](../../voron-print-plan.md#52-checkpoint-after-each-batch) · [00-slicer-setup § Calibration sequence](00-slicer-setup.md#calibration-sequence-run-before-b00-and-again-after-the-gen-2-upgrade) · [Clicky-Clack door README](https://github.com/tanaes/whopping_Voron_mods/tree/main/clickyclacky_door)

## Step B10.6 — Sort into bins

**Do:** Sort off the plate diagram: part number, fill colour and printed bin id all name the bin. Print labels from the [bin-labels sheet](../../print/bin-labels.md); bins listed in [README § Bins](README.md#bins). The six black parts join the orange `Handle` in **11-door**.

**B10-P1**

| bin | parts off this plate |
|---|---|
| **11-door** — Clicky-Clack door | `Handle-Hinge_Bottom`, `Handle-Hinge_Top`, `Hinge-L-sleeve-2X` ×2, `Hinge-L-solid-2X` ×2, `Latch`, `Panel_Clip` |

**Check:** All seven Clicky-Clack parts in **11-door**: 6 black plus the orange `Handle` from B02.

Source: [print plan §9 — batch summary](../../voron-print-plan.md#9-machine-readable-batch-summary) · [print plan §2 — which parts gate which step](../../voron-print-plan.md#2-which-parts-gate-the-frame-and-z-drive-steps) · [print/README § Bins](README.md#bins)

---

## Checkpoint B10
- [ ] Split bushings tap into hinge sleeves without splitting the part
- [ ] M5×45 dowel pin is a tight hammer fit into `Hinge-L-solid`, ~20 mm proud
- [ ] Door swing decided from where the machine will live (as designed: hinges left, opens from the right); hinge files mirrored only if it must open the other way
- [ ] Orange `Handle` (B02) reunited with the black hardware for assembly
- [ ] Clicky-Clack "Blue" trim question resolved with Fabreeko before/at install

## Common mistakes
- Mirroring the `Hinge-L-*` parts "to be safe" — as designed the hinges are on the left; mirror only if the machine's left side will be against a wall.
- Pressing the M5×45 dowel pin in loose instead of a tight hammer fit — the door will rack.
- Printing the stock Voron/LDO door parts alongside Clicky-Clack "just in case."

## Next
Assembly: door hinges and handle in Ch 11 Part A (Steps 11.46–11.50), the door hung in Part B. Printing:
this is the last pre-kit batch — on kit day run Gate B (Step B00.7), then [B01](B01-z-drive-assemblies.md)
and B03–B06. If those already printed, all 22 plates are done.
