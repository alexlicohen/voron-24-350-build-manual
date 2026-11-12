# Side spool holder with a Prusa spindle (Ch 11 Part C, batch B12)

Part of the build since 2026-11-12 (Alex): printed in the ASA run as batch B12, right after B10, on plates
B12-P1 (the frame) to B12-P3 (puck and spindle); fitted after Part B, once the side panels are on. Ch 11
Step 11.68 calipers the right side panel's stack; only a stack over 6.2 mm reprints the frame (Step 11.69).

A diagonal frame on the right side panel's extrusions carries Prusa's Universal Puck, so the right side
takes either a bare spool on Prusa's 1 kg spindle or a Prusa USS Drybox hung straight on the puck. The
filament leaves over the top: through the tube holder on the top right extrusion, to the stock bowden
retainer at the rear, in through the exhaust cover's coupler. The stock rear spool arm stays fitted as a
second spool position.

Fit, modelled 2026-10-23 with a 3D scan of the USS Drybox (Scott, Printables 1783654, CC BY: 217 × 219 × 91 mm, centre hole on the puck axis): the box's front edge sits 2 mm behind the frame's front face and its top 1 mm under the top extrusion, so the touchscreen is clear (the door handle is checked on the machine at Step 11.71); it stands about 120 mm out from the right side's extrusion face, a bare 1 kg spool about the same. The tube holder hangs 5 mm into the box's space, so it goes in the top slot about 22 cm behind the front face, behind the box.

## Licence and credit

- **Frame:** CC BY-NC-SA 4.0. Derived from **Maltasrc**, *Voron 2.4 (350 bed) Side mounted spool*,
  <https://www.printables.com/model/608769> (CC BY-NC-SA). `source/Reel Mount 2_Frame v1.stl` is the
  author's file, unchanged (Printables file id 2569106, 112 084 bytes, sha256
  `7efa10b2f3c8e64270d50200bfd364f7ccd8d14f698eee699044bf99b766da4f`). `remix.scad` and the STL it writes
  are derivatives under the same licence.
- **Tube holder:** the same author and page, file `Bowden Tube Holder_Long.stl` unchanged, fetched (not
  committed).
- **Puck and spindle:** Prusa Research, *Prusa USS Drybox printable accessories*,
  <https://www.printables.com/model/1605113> (Open Community License v1), files `Universal-puck-R1.stl`
  and `Universal-spoolholder-1kg-R1.stl` unchanged, fetched (not committed). The frame only matches the
  puck's screw pattern; no Prusa geometry is copied into it.

## How the frame is made

`remix.scad` is the only generator; from this folder,
`openscad -q --export-format binstl -o side_spool_frame_puck.stl remix.scad` rewrites the committed file
byte for byte. Changes from the author's frame, all asserted in the script:

| Change | Why |
|---|---|
| feet 3.5 → **6.5 mm** (`stack`) | LDO's side panel is 3 mm PC on 3 mm foam tape; the author's feet clear a ~3 mm stack, so the body would sit on the panel (a Formbot builder hit the same thing in the model's comments) |
| peg hub → a solid Ø63 mm boss with four M3 holes on a 26 mm square, counterbored 3.5 mm from the panel side | Prusa's Universal Puck screws on there with four M3×20 SHCS into its pilot holes (8.5 mm of thread) |
| extrusion-screw counterbores deepened to a seat 8.5 mm above the back face | an M3×20 SHCS ends 5 mm below the extrusion face, in a roll-in T-nut, short of the extrusion core |
| output turned to print orientation, front face on the bed | 212 × 212 mm footprint, 21.5 mm tall, no supports |

Re-run with `-D stack=<reading + 0.3>` if Step 11.68 measures the stack over 6.2 mm; the seat moves with
it, so the M3×20 still lands in the nut.

## Print (batch B12)

Core One+, satin sheet, no glue, Voron spec (4 walls, 5 top/bottom, 40 % gyroid, 0.2 mm), 3 mm brims, no skirt.
The committed projects `slicer/plates/B12-P*.3mf` are the jobs laid out by hand and sliced on 2026-11-12;
PrusaSlicer 2.9.7 estimates from `python3 slicer/build_plates.py --from-3mf B12-P1 B12-P2 B12-P3`:

| Plate | Parts | Profile | Estimate |
|---|---|---|---|
| B12-P1 | the frame alone, as oriented, centred | `slicer/voron-coreone-asa.ini`, Galaxy Black ASA | 105 g, 6.9 h |
| B12-P2 | tube holder, flat face down (`plates.ORIENT`), and the camera's two parts (`../happycam-488020/`) | `slicer/voron-coreone-asa.ini`, Galaxy Black ASA | 28 g, 1.8 h |
| B12-P3 | puck and spindle, as oriented | `slicer/voron-accent-blue.ini`, blue accent ASA | 83 g, 5.7 h |

The 212 × 212 mm frame cannot sit 25 mm from every bed edge, so B12-P1 is the one plate exempt from that
rule (`slicer/plates.py` `EDGE_EXEMPT`; `slicer/audit_plates.py` lists the break with its reason). Prusa
prints the puck and spindle in PETG or PC; ASA at the Voron spec is stronger than that and keeps the machine
in two colours. The grams are in the run's spool ledger (`docs/manual/print/README.md`). Everything goes in
bin `11-side-spool`, a box: the frame fits no mesh bag.

**A frame reprint for a thick stack:** write the regenerated STL to a new file, open `B12-P1.3mf`, right-click
the frame, **Replace with STL**, and print it alone (Step 11.69).

## Hardware (kit spares except where named)

6 × M3×20 SHCS (4 puck, 2 frame), 1 × M3×8 SHCS (tube holder: its pegs key into the slot), 2 × M3 roll-in T-nut (frame), 1 × M3 hammerhead
T-nut (tube holder: its pegs leave 12 mm, too short for a roll-in), the spindle's rubber
O-ring (one ships with every USS Drybox), and one new 2 m length of 4 mm OD × 3 mm ID PTFE, bought (Ch 00
Step 00.8), replacing the kit's reverse-bowden run.

## Files

`slicer/plates.py` `PLATES` (B12) lists the remix and the three fetched files, `ADDONS` the unchanged source;
`slicer/stl/MANIFEST.sha256` pins them, so `python3 slicer/fetch_stls.py --verify` fails if any changes.
`sources.yml` pins both Printables pages (`printables-608769-voron-side-spool`,
`printables-1605113-prusa-uss-drybox-accessories`); a `CHANGED` line from `scripts/sources_verify.py`
carries what to re-check.
