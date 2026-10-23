# VERIFY-A — G4-01…G4-06 (Ch 08, Ch 09, B06, B07)

Verdicts: 5 CONFIRMED (G4-01, -02, -03, -04, -06), 1 PARTLY (G4-05). Lint: `lint_manual.py --strict-parts --chapters 08,09` exit 0 (check 6 0, check 7 0); `--budgets-only` has no finding in my files (its one finding is 00.8, another agent's); `slicer/check_docs.py` exit 0.

## G4-01 blocker — 08.7 inserts in `_rear_cw2` · CONFIRMED
- STL, re-probed (numpy slicer, `venv-cq/bin/python -I`, coordinates from the bbox centre): `stealthburner_printhead_revo_voron_front.stl` (71.1×59.1×27.4) has Ø4.6 ×2 at (±13, 23) and Ø4.7 ×2 at (25, 3) / (28, −13), all blind from one face; `…_rear_cw2.stl` (57.7×59.7×26.3) has only Ø3.3–3.4 through holes, no insert bore.
- SB p.37: the thin part with the CW1/CW2 corner is the rear half. SB p.38: the part with 2 top inserts + the circled ADXL pair is the large half. SB p.41: the thin (blue) half goes on last, with the M3×16 driven from its side.
- Changes, `docs/manual/08-toolhead.md`: :61 hardware note "2 printhead front"; :264 title "front printhead half"; :268 WYLA (large half, the one the hotend sits in); :272 Parts `stealthburner_printhead_revo_voron_front` ×1; :275 Do "face the rear half meets"; :277 Check "back face … the thin rear half stay bare". Count unchanged (2, total 18).
- Outside my files (log only): `scripts/data/hardware-ownership.yml:129` evidence string "seated in the rear printhead half" → "seated in the front printhead half" (text only, no count effect).

## G4-02 major — 08.28–08.30 halves swapped · CONFIRMED
- SB p.40 draws the hotend in the half with the two top inserts and the ADXL pair (= front, per G4-01); p.41 closes the thin rear half onto it with two M3×16.
- Changes, `08-toolhead.md`: 08.28 title, WYLA, Parts (`reused: the front printhead half with its inserts`), Do → front; 08.29 Parts + Do 1 → front half; 08.30 WYLA "Rear half on", Parts `stealthburner_printhead_revo_voron_rear_cw2` ×1, Do "Bring the thin rear half onto the front half … drive two M3×16 SHCS through it into the front half's inserts."
- `docs/voron-print-plan.md:786` and B06 (:52, B06.4, :148) already say the hotend seat is in the printhead front: correct, no change for G4-02. (Their "4× M3×8" is G4-21, not assigned here.)

## G4-03 major — 09.18 "rails are earthed" + promised check · CONFIRMED
- 00a.7 (:214–228): the rail bond is incidental through anodised extrusion and steel screws, "not the same thing as a PE conductor". 10-wiring.md:330: "LDO's build does not run a separate PE to the DIN rail". LDO Rev D wiring guide (curl 2026-10-23): the only frame earth is the FRAME PE lead screwed to the frame; no DIN-rail earth anywhere. Ch 10 Checkpoint #1 (10.18–10.21) and 10.77's table have no DIN-rail row, so the promised continuity check does not exist.
- Change, `docs/manual/09-electronics-bay.md` 09.18 ⚠ (:541): no PE conductor to the rail, contact only through screws into anodised extrusion, not a PE bond; do not count it as earthed; decision settled at 00a.7 (link). Source line: LDO § Checkpoint #1 → LDO § Frame PE + Ch 00a Step 00a.7.
- Elsewhere: none required. Optional for the Ch 10 owner: an informational 10.77 row "DIN rail — incidental bond only, not a PE (00a.7); no pass/fail".

## G4-04 major — 09.22 one free Pi USB port · CONFIRMED
- 10.52 (10-wiring.md:1396) plugs the Leviathan into a Pi USB port; 10.53 (:1416) a second Pi USB port for the USB adapter; 11.76 (11-skirts…:2213+) "plug the tagged camera plug into a free Pi USB port" (camera add-on, 10.81). LDO wiring guide § Frame PE: "Connect the usb cable to the Raspberry Pi and the USB Adapter PCB."
- Change, 09.22 (:641–643): Check "Ethernet and two USB-A ports clear of the Leviathan, three with the camera add-on"; ⚠ "Ch 10 needs Ethernet and two USB ports, Leviathan and toolboard USB adapter, plus a third for the camera add-on" (the old "Ch 12 needs a USB port" is gone: Ch 10 makes both links).

## G4-05 major — probe pin gap 1.5 (09.30) vs 2–3 mm (13.24) · PARTLY
- The two Voron primaries disagree. Voron manual p.161 (Z ENDSTOP, "Adjust Z endstop position") dimensions the gap as **1.5** and states the rule "The shaft of the Z Endstop must not touch the print bed". Voron docs startup § Bed locating (raw `VoronDesign/Voron-Documentation/build/startup/startup.md`, fetched 2026-10-23): "a small (2-3mm) gap between the back edge of the bed, and the shaft of the Z endstop". LDO's probe text gives no figure.
- So 09.30 was faithful to p.161, not wrong against its source; the inconsistency is real. 13.24 is where the bed is finally located against the probe and it matches the Voron startup guide, so Ch 13 stays; Ch 09 aligns to it (2–3 mm also satisfies p.161's must-not-touch rule).
- Change, `09-electronics-bay.md` 09.30: WYLA "pin 2–3 mm behind the plate's rear edge, the gap Step 13.24 checks"; Check "A 2 mm hex key slides between pin and plate, a 3 mm does not"; Helper "Tries the 2 mm and 3 mm hex keys … says which one fits"; new Tip "p.161 draws this gap as 1.5 mm; its rule is only that the shaft never touches the plate, and 2–3 mm meets it" [src startup guide]; Source + Voron startup § Bed locating; Checkpoint 09 (:1031) "pin 2–3 mm behind".
- No Ch 13 change. `docs/print/checklists.md:208` still reads 1.5 mm until the build regenerates it.
- The separate "rear cut-out vs LDO photo" location item is untouched (still open).

## G4-06 major — B07 inspects heat-set bosses on the mains WAGO mount · CONFIRMED
- STL probe `slicer/stl/voron2/STLs/Electronics_Bay/wago_221-415_mount_3by5.stl` (126.8×23×12.2): only two Ø5.2 holes at x = ±56 (M5 clearance), no Ø4.7 bore. Ch 09's hardware table (:75) already says "the mains WAGO mount has none, only two M5 holes". The inlet panel's 3 Ø4.7 bores (09.10) are the B07 part that does take inserts. (LDO's bed WAGO mount takes 2, but it is LDO-supplied, not on B07.)
- Changes: `docs/manual/print/B07-electronics-bay-and-lighting.md` :44 Read first → "inlet panel's three insert bores get their inserts on kit day (Ch 09 Step 09.10), not here; the Wago mount takes none"; B07.6 item 2 → "Check the inlet panel's three insert bores are crisp and round", Check "insert bores undamaged"; Checkpoint :154 → "Inlet-panel insert bores crisp (inserts go in at Ch 09 Step 09.10)". `09-electronics-bay.md` 09.13: deleted the second ⚠ ("if your printed mount has insert bosses … (verify on bench)").
- Outside my files (log only): `docs/voron-print-plan.md:787` B07 row "Wago mount heat-sets;" → "Inlet-panel insert bores (3, Ch 09.10; the mains Wago mount takes none);". `docs/print/checklists.md:421` regenerates on build.
- Not touched (G4-07, unassigned): B07 :13–14 and :145 still say the batch's inserts go in "in Ch 09" (COB mounts are 10.35).

## Files changed
- `docs/manual/08-toolhead.md` (G4-01, G4-02)
- `docs/manual/09-electronics-bay.md` (G4-03, -04, -05, -06)
- `docs/manual/print/B07-electronics-bay-and-lighting.md` (G4-06)
- `docs/manual/print/B06-toolhead-sb-cw2-klicky.md`: no change (front-half wording already correct).
