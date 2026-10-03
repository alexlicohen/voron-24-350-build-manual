<!-- Superseded: first draft of Ch 13 Part L (13.44–13.50). The live text is docs/manual/13-initial-startup.md Part L, Steps 13.44–13.54. -->

## Part L — Add-on: nozzle scrubber with sheet stops

This part is optional. It fits jinetix's silicone nozzle scrubber, low variant, on the rear of the bed extrusions: a brush bracket and its magnetic purge bucket on the left, a narrow stop bracket on the right. `PRINT_START` then wipes the nozzle before the Z home that counts.

### Step 13.44 — Measure the probe height and the reach past the plate

(no image — see text)

**What you're looking at:** The brush sits just behind the plate's rear edge, so the nozzle has to travel a few millimetres past that edge. The Omron rides 25 mm behind the nozzle and passes over the bucket. These two numbers decide whether the add-on fits.

**Parts:**

- tool: digital caliper
- tool: steel rule

**Do:**

1. Power on, `M112` ready, `G28`, then `G0 X175 Y175 Z10`. Caliper the Omron face above the plate; minus 10 is d.
2. At `X70`, `G0 Z1`, jog Y back until the tip is over the plate's rear edge. O is `position_max` minus that `M114` Y.

**Check:** d is at least 0.6 mm and O is at least 3.5 mm. Both are written down.

**Helper:** Reads the caliper and the M114 Y value aloud and writes both down.

⚠ If O is under 3.5 mm the nozzle cannot reach the brush, and if d is under 0.6 mm the Omron will strike the sheet stops. Stop here and leave the add-on off `(verify on bench)`.

Tip: The author's macro assumes 6 to 7 mm of reach. The version used here shrinks its scrub circles to whatever O you measured.

Source: [Printables 796563 — jinetix, nozzle scrubber w/ sheet stops](https://www.printables.com/model/796563) · [Voron manual p.161](https://github.com/VoronDesign/Voron-2/blob/de7e89d/Manual/Assembly_Manual_2.4r2.pdf#page=161) · [Klipper docs § probe](https://www.klipper3d.org/Config_Reference.html#probe)

---

### Step 13.45 — Press the magnets and seat the wiper

(no image — see text)

**What you're looking at:** The brush bracket holds the silicone wiper and two magnets. The bucket carries two more and hangs under the bracket on them, so it lifts off for emptying. The wiper is a Bambu A1 bed wiper, a row of silicone bristles.

**Parts:**

- 6×3 mm neodymium magnet ×4
- brush bracket, low, mirrored ×1 — from the scrubber add-on print
- purge bucket, trimmed, mirrored ×1 — from the scrubber add-on print
- Bambu A1 heatbed nozzle wiper ×1 — from Bambu Lab
- consumable: super glue

**Do:**

1. Press two magnets into the bracket's underside pockets, flush.
2. Press the bucket's two in, each one attracting the bracket magnet above it.
3. Press the wiper into its seat, bristles up.

**Check:** The bucket snaps up under the bracket and hangs square. All four magnets sit flush and the wiper lies flat.

**Helper:** Tests each magnet pair and hands them over the right way up.

Tip: The pockets are drawn for ASA shrinkage, so the magnets press in. Any that falls out gets a drop of super glue.

Source: [Printables 796563 — BOM and print settings](https://www.printables.com/model/796563) · [Bambu Lab — Heatbed Nozzle Wiper A1/A2L](https://us.store.bambulab.com/products/heatbed-nozzle-wiper-a1)

---

### Step 13.46 — Bolt both brackets to the bed extrusions

(no image — see text)

**What you're looking at:** Both brackets sit on the bed extrusions just behind the plate, their front faces against its rear edge. The brush bracket goes on the left, away from the nozzle-probe pin. One upright M3×8 in each bracket is a sheet stop.

**Parts:**

- reused: the brush bracket with its bucket
- stop bracket ×1 — from the scrubber add-on print
- M3 roll-in T-nut ×4
- M3×8 SHCS ×6
- tool: 2.5 mm hex key

**Do:**

1. `G0 X175 Y60 Z150`, bed cold. Roll two T-nuts into each bed extrusion's top slot behind the plate.
2. Bolt each bracket with two M3×8, front face on the plate edge, snug.
3. Thread one M3×8 into each upright hole until seated.

**Check:** Both brackets sit flat, front faces on the plate edge. Pushed back, the flex plate stops on both screw heads.

**Helper:** Holds each bracket against the plate edge while the adult tightens it.

⚠ The right bracket sits beside the nozzle-probe collar. If it touches the collar or the probe body, the pin cannot move freely and Z zero drifts. Leave that bracket off `(verify on bench)`.

Source: [Printables 796563 — BOM](https://www.printables.com/model/796563) · [LDO wiring guide § Assembling the nozzle probe](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d#assembling-the-nozzle-probe)

Pause: ~25 min since the last pause — the add-on is measured and bolted on, the bucket hangs on its magnets, and Klipper does not know about it yet. Do not run any scrub command before Step 13.48.

---

### Step 13.47 — Read the brush coordinates off the machine

(no image — see text)

**What you're looking at:** The macros work from numbers read off this machine, never presets: the X of both bristle edges, the plate-edge Y from the first step of this part, and the height of the bristle tops.

**Parts:**

- reused: the fitted scrubber
- tool: a sheet of printer paper

**Do:**

1. `M112` ready, `G28`, nozzle cold. Jog over the brush at `Z5` and read `M114` X at its left and right bristle edges.
2. Lower over the bristles until paper drags. That Z minus 0.5 is `z_scrub`.

**Check:** The two X values are about 35 mm apart and `z_scrub` is close to minus 0.5 mm `(verify on bench)`.

**Helper:** Reads each M114 value aloud and writes it on the record card.

⚠ Below Z1, keep the nozzle over the brush. Over the plate's rear edge it digs into the flex plate.

Source: [Printables 796563 — macro reference point](https://www.printables.com/model/796563) · [Klipper docs § M114](https://www.klipper3d.org/G-Codes.html#g-code-commands)

---

### Step 13.48 — Add the scrubber macros

(no image — see text)

**What you're looking at:** `[gcode_arcs]` lets Klipper run the small G2/G3 circles of the scrub. `_SCRUB` holds your numbers; `NOZZLE_PARK_BUCKET` and `NOZZLE_CLEAN` read them and refuse to run while any is still a placeholder.

**Parts:** none.

**Do:** Paste the block below under `[gcode_macro PRINT_END]`. Replace the four placeholder values with the numbers you wrote down, then **SAVE & RESTART**.

```ini
(paste review/2026-10-03-scrubber/scrubber.cfg here)
```

**Check:** Klipper restarts without an error, and `NOZZLE_PARK_BUCKET` parks the nozzle over the bucket at Z5.

Tip: The macro sizes its scrub circles to fit your reach past the plate, from 2 mm radius down to 0.75 mm.

Source: [Printables 796563 — macros, revision 2025-12-22](https://www.printables.com/model/796563) · [Klipper docs § gcode_arcs](https://www.klipper3d.org/Config_Reference.html#gcode_arcs) · [Klipper docs § Command templates](https://www.klipper3d.org/Command_Templates.html)

---

### Step 13.49 — Dry-run the scrub cold

(no image — see text)

**What you're looking at:** A cold run shows the whole path before anything is hot: five flicks from the bucket into the brush edge, five rows of small circles on the bristles, then a straight lift. The Omron trails behind, over the bucket.

**Parts:** none.

**Do:**

1. `M112` ready, `G28`, then send `NOZZLE_CLEAN`.
2. Watch the nozzle stay on the bristles and the Omron pass over the bucket without touching.

**Check:** Nothing touches except nozzle on silicone, the bucket stays hung, and the run ends at Z5.

**Helper:** Watches the Omron from the side and calls out if it touches anything.

⚠ If the Omron touches the bucket, send `M112` and re-measure d from the first step of this part. The trimmed bucket needs at least 0.6 mm.

Source: [Printables 796563 — macro behaviour](https://www.printables.com/model/796563)

---

### Step 13.50 — Scrub inside `PRINT_START`, then shut down

(no image — see text)

**What you're looking at:** The scrub runs after QGL at the QGL temperature, between a provisional Z home and the one that counts. The nozzle probe measures the real tip, so a clean tip is a true Z zero.

**Parts:** none.

**Do:** In `PRINT_START`, insert the three lines below after `QUAD_GANTRY_LEVEL`, above the existing `G28 Z`. **SAVE & RESTART**, print one small part and watch the scrub, then commit and shut down as before.

```ini
    G28 Z                                  ; provisional Z0 after QGL, tip not yet clean
    NOZZLE_PARK_BUCKET
    NOZZLE_CLEAN
```

**Check:** The tip leaves the brush clean, the string lands in the bucket, and the first layer matches the cube's.

⚠ The nozzle is at 150 °C during the scrub. Keep hands off the toolhead, and empty the bucket only cold, lifting it off its magnets.

Source: [Printables 796563 — macro placement](https://www.printables.com/model/796563) · [Ch 12 Step 12.36](12-software.md#step-1236-replace-print_start-with-a-skeleton-that-waits-on-the-chamber)

Pause: ~30 min since the last pause — the scrubber runs inside `PRINT_START`, the config is committed and copied off the Pi, and the machine is shut down. Ready for Checkpoint 13, then Ch 11 Part B.

---
