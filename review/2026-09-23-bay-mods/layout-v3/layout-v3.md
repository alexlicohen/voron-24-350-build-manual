# Layout v3: changes against v2 (2026-09-23)

The frame and method are unchanged: apparent mm, **±6 % absolute and ±1.5 mm on local gaps; every position is unverified.** Files: `overlay-v3.png`, `layout-v3.json`, `remix/` (14 STLs), `renders/`, `slice/`. Scripts are in `work/`: `remix_v3.py`, `layout_v3.py`, `outputs_v3.py`, `render.py`, `slice_v3.py`. v2 is untouched.

## What changed
- **Front DIN rail stays where LDO puts it.** Its screws go through fixed deck holes. The Leviathan-edge → PSU gap stays at ~26.3 mm apparent.
  - Middle run re-centred at y −2.2 and narrowed; side runs follow (front run y −143, RR corner y 147.4).
- **PSU moves 6 mm left, not 4.** At 4 mm the narrowed right T's rear fillet touches it.
- **AC:** the 95 × 97 hub is gone. It is replaced by MSS's AC look: the original-size wire box, the curve that leaves its open end, and small T and straight pieces.

## Middle run, printed (`V3L_154N_DUCT` + cover, ×2)
- **Method:** slice-and-shift along the long mid-plane (author y 207.18, which gives the least seam mismatch).
  - **Δ = 2.4 mm.** Outer width at the tine bulge 24.4 → **22.0**; lid 24.1 → 21.7.
  - Clear channel 17.9 → **15.5 mm** at mid-height, and 16.2 → 13.8 at the lid rail.
  - Walls, tines (12 mm pitch, 4 mm slots), lid rail and snap keep their exact geometry. Only the floor and lid are narrower.
  - The small floor zip-tie bar at the centre loses 2.4 mm of width. See `renders/00_profile…` and `01_…`.
  - Estimated fill for 6 steppers + HV + 2 × 24 V + SSR SIG: ~150 of ~290 mm² (unverified OD).
- **Clearance (apparent, lid included):** 1.6 mm to the Leviathan PCB edge, 1.7 mm to the PSU front. Target is ≥ 1.5.
- **Joints: `V3L_T_REG_N` + cover (×2), the same cut through the T's stem centre at author x −52.34.**
  - The stem becomes 22.0 wide, so the stem-to-duct joint is profile-identical.
  - The bar shortens 84 → 81.6 but keeps its 24.4 width, so the side runs are unchanged.
  - I chose this over a tapered adapter: there is no extra joint and no skewed tines (`02_…`).
- **Coupon:** `V3L_COUPON_22N_DUCT` + cover (22 mm), to test the snap and the fill before printing the 154s (`03_…`).

## AC conduit in MSS's look
- **Identifying the curved piece.** In 505838's photos, the curve leaving the box's open end is 502306's **`CMD_V3_1H_90DEG` + `_90DEG_COVER`**:
  its outer radius matches 34.2 mm against the 77.4 mm box; MSS's render 03 shows the same box → 90DEG → hazard half-bridge chain; the 505838 3MF holds only the box, WARNING lid, half-bridge and hazard cover.
- **What the original proportions can't reach.** The SSR rear edge is ~100 mm from the WAGO port face, and the bed-lead hole line is only 43 mm from the WAGO run's centreline. A 48.4 mm box at the WAGO therefore can't reach the SSR, and a stock R22 curve can't drop to the hole line. The only other hole approach runs over the Z-chain notch, which breaks DC separation.
- **Closest faithful option, chosen:**
  1. **`V3L_WIRE_BOX_PORT`:** the MSS box at original size (77.4 × 48.4) against the WAGO bus at x −115.8…−38.4.
     - Change: one 18 mm port through the front tined wall at x −72. The parent's 4 pinched edges are repaired.
     - Lid options: `…1V_WIRE_BOX_LID_WARNING` + INLAY (two colours, INDX), or plain `CMD_V2_6B_WIRE_BOX_COVER`. Both are unchanged (`05_…`).
  2. **`V3L_90DEG_R15` ×2** leave the box's open end and drop to the hole line.
     - Re-radiused: the arc of `CMD_V3_1H_90DEG` alone, every vertex moved 6.5 mm toward the arc centre.
     - Centreline R 22 → 15.5, arms 15.5 each; wall, floor and lid sections unchanged. The cover gets the same treatment (`04_…`).
     - The two curves meet exactly: 15.5 + 15.5 = 177 − 146.
  3. **`V3L_34mm_DUCT_HOLE`** (base opening over the hole) + endcap, then the fin at the PSU as in v2.
  4. **SSR run behind the SSR:** stock `CMD_V3_1H_T_SHORT` + cover at x −72, y 116; `V3L_10mm` to the right (open end 6 mm from the strip face, where L/N/FG enter); endcap on the left; a `V3L_10mm` stub up into the box's port.
- **Enclosure.** WAGO ports go straight into the box's rear tines; SSR LOAD1/2 into the T's front tines; PSU L/N/FG into the SSR run's open end; bed L/N/PE from the hole through the curves into the box.
- **Separation.** Minimum AC↔DC distance is **12.0 mm** (endcap ↔ S-jog). The lower curve ↔ rear-upper DC run is 13.7 mm. The rear-upper DC run is shortened to `V3L_10mm`.
- Assembled view: `renders/06_AC_conduit_assembled.png`.

## Clearance and bench checks that changed (renumbered from v2's list)
3. **Leviathan PCB rear edge → PSU front: ≥ 25.0 mm** (21.7 lid + 2 × 1.5). This replaces v2's ≥ 32 after the rail move.
   - Below 25 → keep LDO's PVC middle duct, and use stock T_REG with an 82 straight.
5. **PSU moved 6 mm left.** Its front-right corner → the right T's rear fillet must be **≥ 2 mm**. Estimate: 0.8 apparent, ~3.3 after the PSU's ~1.4 % photo magnification.
   - Short → move the PSU 8 mm left and drop the `V3L_10mm` at the SSR run's right end.
6. **PSU left end → SSR run's open end ≥ 3 mm** (est. 3.0).
7. **SSR rear edge → WAGO port face = 100 ± 1 mm.** Otherwise re-cut the stub to `gap − 90` mm. The box is fixed at the WAGO; the stub takes up the difference.
9. **DC rear-upper run** now overlaps the assumed notch front by ≤ 1.2 mm (y 196.2). Harmless because it's DC; confirm the harness still drops in.
15. **Spare length:**
    - bed L ≥ 70 mm: the route is longer via the box and curves, est. +47 mm against LDO's;
    - 24V PSU→MB and 24V→USB adapter ≥ 8 mm for the 6 mm PSU move;
    - the rail-shift items are dropped.
16. **New, coupon:** the lid snaps and holds, and the full middle bundle lies below the lid rail, 13.8 mm clear.
17. **New, port:** the stub lands on the box port within ±2 mm in x.

Unchanged from v2: 1 (A/B +195/+129 mm), 2 (TH/probe/fan via the notch), 4, 8, 10–14.

## Ch 09/10 steps (ids only)
- **Dropped:** 09.5 (no rail change now).
- **Amend:** 09.6, 09.16 (PSU 6 mm left), 09.36, and the same Ch 10 list as v2.
- **Append:** 10.80 becomes "Fit the strip fin and close the AC lids (WARNING lid on the box)".

## PrusaSlicer 2.9.6 CLI check and material (`voron-coreone-asa.ini`; PETG = cm³ × 1.27)
All 14 new STLs slice on their own: OK (`slice_v3.py` output).

| Set | Time | ASA g | PETG g |
|---|---|---|---|
| Black DC loop (T_REG_N, 10c rear-upper) | 17 h 25 m | 182.2 | 216.3 |
| Black middle run 2×154N + coupon | 4 h 41 m | 47.7 | 56.6 |
| Orange AC (box, plain lid, 2 curves, T_SHORT, 34c, 2×10c, 2 caps, fin) | 4 h 28 m | 51.5 | 61.2 |
| WARNING lid, black part (replaces the plain lid) | 25 m | 5.7 | 6.8 |
| **Total with the plain lid** | **26 h 34 m** | **281.4** | **334.1** |

- **Correction to v2:** its black-DC plate double-counted the two middle 154s. Corrected v2 total: **286.4 g ASA / 339.8 g PETG**, not 333.0 / 395.1.
- **Credit:** MyStoopidStuff (502306, 505838) and RyanDam's Cable Management Duct. GPL-3.0 per the brief; I did not check it against the Printables pages.
