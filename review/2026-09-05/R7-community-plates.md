# R7 — Community plate cross-check vs docs/voron-print-plan.md §3/§9

Sources fetched: gist thalbr/886aaea (raw, full text, 2.4r2 assembly order) — OK.
Printables 1012764 and 1002744: **HTTP 403 to fetch tools (login wall)**; worked from
description snippets via search only, per task instructions. Bed size, per-size 3MF file
lists, and exact slicer settings on those two pages could not be confirmed — flag as
unverified, not as agreement or conflict.

## (a) Parts in either source, absent from our plan

### F1 · medium · docs/voron-print-plan.md §3 (all batches)
- **Claim:** Our plan has no batch entry for `[a]_z_belt_clip_upper_x4` / `[a]_z_belt_clip_lower_x4`.
- **Source:** gist, "Gantry" section (pages 82, 108) — lists these alongside `z_joint_upper/lower_x4`,
  which we do print (B05).
- **Problem:** Not in any batch table and not in §7 "Deliberately NOT printed" either — looks like a
  gap rather than a deliberate exclusion, unlike every other omission in the plan which is logged in §7.
- **Fix:** Check the current `Voron-2` STL repo (`STLs/Gantry/`) for these two files; if they're current
  (not superseded by a Rev naming change), add to B04/B05 and note the ~1 g/part cost. If superseded,
  add a line to §7.

### Not applicable (different hardware, correctly excluded already)
- Klicky/CW1 legacy: `[a]_belt_tensioner_a/b_x2`, `[a]_z_drive_baseplate_a/b_x2` (gist Z_Drive) — look
  like older names for what we print as `z_tensioner_bracket_a/b_x2`; naming drift across manual
  revisions, not a missing part. Low confidence without diffing the STL repo directly.
- `[a]_tensioner_left/right` (gist Front_Idlers) — not in our plan; likely superseded by the
  `front_idler_left/right_lower/upper` set we already print. Verify only if front idler feels loose.
- CW1-only, mini12864, Octopus, hall-effect, MGN9, breakout-PCB, endstop-pod-switch, exhaust-housing,
  stock-door, Bowden parts from the gist — all already correctly covered by our §7 exclusion table
  (wrong extruder gen / wrong board / wrong probe / wrong screen / Nevermore / Clicky-Clack / MGN12).
- `SB_5015_Cutting_Tool_A/B` (gist) — a fan-shroud cutting jig, not a machine part; optional, skip.
- JackHammer 1012764/1002744: no confirmed part beyond ours — page text only says 3MFs are
  organized by bed size (250/300/350) with example hotend/mainboard mounts *only in the 3MF*, not the
  STLs; can't diff names without the file list (login-gated).

## (b) Parts in our plan absent from both sources — sanity check
`Leviathan_bracket_set`, LDO `nozzle_probe_ldo`, Nitehawk-SB V2 `usb_adapter_mount_partial_cover`,
Clicky-Clack (`Handle`, `Hinge-L-*`, `Latch`), Ti-backer `XY_cable_chain_bridge-Igus-3mm_backer` —
all kit/mod-specific, correctly absent from the stock-manual gist and from JackHammer's generic
LDO-oriented plates. No sanity-check failures.

## (c) Ordering insight from the gist
Gist order matches our batch order closely: Z rails → deck panel → Z drive → AB drives/idlers →
gantry/XY joints → Z axis/joints → X carriage → toolhead → electronics → skirts/panels → spool →
exhaust. Our B00→B10 sequence tracks this 1:1 except we front-load **B02 (all orange accents)** as
its own batch rather than interleaving accent parts per-assembly-stage — a deliberate batching choice
(§3 batch header), not a conflict with the gist's assembly-order framing.

## (d) Print-setting differences vs docs/manual/print/00-slicer-setup.md
No specific perimeter/infill/width/brim numbers were retrievable from either Printables page
(login wall). One qualitative point did surface: search results describe JackHammer's OrcaSlicer
profile as having print speeds "set very high for a Klipper printer, may need to adjust down."
Our profile is already the opposite (STRUCTURAL preset speeds cut further: external perimeter
50→35 mm/s, perimeter 70→55, infill 120→100) — no conflict, ours is already conservative relative
to that community profile's stated risk.

## (e) Verdict
Only one actionable item: **F1** — confirm whether `z_belt_clip_upper/lower_x4` are current parts
missing from B04/B05, or superseded. Everything else in our plan checks out as kit-specific and
correctly scoped; nothing from the community sources indicates a setting or part we should change
otherwise. Printables 1012764/1002744 need a logged-in fetch (or a browser session) for a real
file-list diff — current comparison is description-level only.

**Orchestrator note (2026-09-05):** F1 is not a gap. The clips are accent parts, `[a]_z_belt_clip_lower_x4.stl` / `[a]_z_belt_clip_upper_x4.stl` (Voron-2 `STLs/Gantry/`), printed on batch **B02** (print plan §3 lines 300–301) and consumed in Ch 06 Steps 06.6–06.7. The gist lists them without the `[a]_` prefix. No change needed.
