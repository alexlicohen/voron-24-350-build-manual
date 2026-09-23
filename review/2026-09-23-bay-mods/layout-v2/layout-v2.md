# Layout v2: printed conduits for the LDO Rev D+ bay (2026-09-23)

Analysis and geometry only. Frame and method are v1's (`../fit-report.md`): apparent mm on LDO's `S0General_Placement.jpg`, origin at the frame centre, +y toward the rear. **Every position is unverified: ±6 % absolute, ±1.5 mm on local gaps.** Figure: `overlay-v2.jpg`. To re-run `work/` (e.g. to regenerate the hub for a measured SSR→WAGO gap), re-download the MSS files per PROJECT_MEMORY (Printables technique) into `$BAY_MODS_SCRATCH/mods/502306-cable-duct/` and `…/505838-ac-covers/`, then set `BAY_MODS_SCRATCH`. Diagram data: `layout-v2.json`. Scripts are in `work/`: `remix.py`, `layout.py` (places the real meshes and checks clearances), `outputs.py`, `slice_v2.py`.

**One correction to the brief.** LDO's S5/S6/S7 mapping photos show the bed L/N/PE/TH, the nozzle-probe lead and the filter-fan lead rising through the **round deck hole at (+15, +146)**, about 50 mm in front of the notch. The rear notch (x 0…+12) carries the Z-chain bundle (umbilical, XY endstop, A, B) and the LED lead. So the AC/DC meeting point is the hole, not the notch.

> **Revision 2026-09-23 (orchestrator):** the front-rail move is NOT possible as assumed. Its M5 screws pass through fixed holes in the acrylic deck panel (Voron manual p.29: "Position the 4 T-nuts so they are directly below the 4 holes in the deck panel"); the rail's slots run lengthwise only. Default is now LDO's PVC middle duct butted against the two T_REG stems. Optional upgrade: a remixed ~22 mm-wide middle duct (test print first). Bench check 3 becomes "≥ 25 mm, only for the optional narrow duct". The 4 mm PSU shift is along the rail and stands. Totals without the printed middle run: ~26 h, 286 g ASA / ~340 g PETG.

## Bill of pieces
| File | Qty | Colour / role | Stock or custom |
|---|---|---|---|
| `CMD_V3_1H_90DEG` + `CMD_V2_6B_90DEG_COVER` | 2+2 | black, FR and RR corners | stock |
| `V2L_90DEG_MIRROR` + `V2L_90DEG_COVER_MIRROR` | 1+1 | black, FL corner | remix: mirror image. The corner's arms are unequal (38.8 / 42.0 mm from the corner point), and FL needs the other hand |
| `CMD_V3_1H_T_REG` + `CMD_V2_6B_T_REG_COVER` | 2+2 | black, side-run junctions for the middle run | stock |
| `CMD_V3_1H_154mm_DUCT` + cover | 2+2 | black, front run | stock |
| `CMD_V3_1H_154mm_DUCT` + cover | 2+2 | black, middle run (conditional) | stock |
| `CMD_Remix-V3_DUCT-2B_45deg` + `_45deg_LID` | 2+2 | black, S-jog in the rear run (one rotated 180°) | stock |
| `V2L_58mm_DUCT` + cover | 3+3 | black: L1, R1, rear-lower | custom: 154 cut at a tine boundary (12n+10) |
| `V2L_130mm_DUCT` / `V2L_70mm_DUCT` / `V2L_22mm_DUCT` + covers | 1+1 each | black: L2, R2, rear-upper | custom: cut from 142 / 82 / 82 |
| `V2L_AC_HUB` + `V2L_AC_HUB_COVER` | 1+1 | **orange**, the AC collector | remix of `CMD_V3_1H_WIRE_BOX` / `_COVER` (details below) |
| `V2L_58mm_DUCT_HOLE` + `V2L_58mm_DUCT_COVER` | 1+1 | **orange**, run over the bed-lead hole | custom 58 with a 17 × 16 mm opening in the base |
| `CMD_Remix-V3_DUCT-1M_ENDCAP` | 1 | **orange**, closes the hole run | stock |
| `V2L_STRIP_FIN` | 1 | **orange**, divider at the PSU terminal strip | new part: 25 × 55 × 2.4 plate, foot and rib |

- **No stock straight fits:**
  - the side runs need 58 mm between the corner arm and the T bar;
  - L2 has to stop 6 mm short of the rear-left Z motor;
  - the right run has to put the RR corner in front of the RR motor;
  - the rear run is the S-jog's remainder.
- **Seams:** every cut is on a plane whose section repeats for all k × 12 mm (checked). Custom STLs are watertight.
- **Frames:** remix STLs keep their parent's frame, so print them as v1 did. Ducts and hub: flip base-down. Covers: as-is. Fin: on its side.
- **Why the hub is a remix:**
  - the hole line (y 146) and the WAGO face (y 202) are only 43 mm apart;
  - any stock T or corner pair needs 57–69 mm between centrelines;
  - so no stock chain links the WAGO to the hole run, the SSR and the PSU.
- **Hub construction:**
  - the wire box is stretched by vertex moves in bands that have no vertices, so its topology is untouched;
  - +48.8 mm deep; +18 mm long, which widens one wall slot to 22 mm, in front of SSR LOAD 1/2 and behind the WAGO L block;
  - its end notch faces the PSU and the hole run, open y 117…160; a 2.4 mm filler wall closes y 160…190;
  - result: 95.4 × 97.2 × 25 mm.
- **Hub mesh:** it inherits the parent's four non-manifold edges. PrusaSlicer 2.9.6 slices it (checked).
- **Printability:**
  - hub, covers and straights: the parent's supports-free geometry;
  - the widened slot is a 22 mm bridge at the lid rail, which the lid spans;
  - the hub lid is 99.4 × 96.1, which fits the Core One.
- **Credit:** MyStoopidStuff (Printables 502306) and RyanDam's Cable Management Duct. The GPL-3.0 licence is carried over as the brief states it; not checked against the Printables page.

## How each requirement is met
1. **Curved 90° corners, one DC loop.** The DC conduit is one piece chain, open only where leads enter: Z1 at L2's rear end, and the notch at the rear-upper run.
   - Path: L2 → T → L1 → FL 90° → front 2 × 154 → FR 90° → R1 → T → R2 → RR 90° → rear-lower → two 45° (S-jog, +36.6 mm) → rear-upper at the notch.
   - The jog is needed because the RR corner must sit in front of the RR motor and the Z2 plug (y ≤ 158), while the notch run must pass behind the AC hole run (y ≥ 170).
   - A 45°-chamfer `45deg_CORNER` at RR hits the Z2 plug (checked).
2. **Complete AC/DC separation.** Every mains lead lies in the orange hub or the hole run; no DC lead enters either. No conduit crosses another.
   - **Deck hole:** made AC-only. Bed TH, the nozzle-probe lead and the filter-fan lead leave the bed area above the deck and drop through the Z-chain notch instead. The hole run's base opening sits over the hole, so bed L/N/PE go straight from the deck into AC.
   - **PSU terminal strip, front to rear:** +V +V +V −V −V −V FG N L, at y 38.7…114.7 with 9.5 mm pitch.
     - The fin stands on the deck in plane y ≈ 91.2, between terminal 6 (−V) and terminal 7 (FG), from x −50 to 1.5 mm short of the block face, up to 55 mm high, which is above the PSU top at 52.5.
     - DC leads leave forward, toward the middle run.
     - L/N/FG turn rear into the hub's open end or its last front slot.
     - The terminal screws themselves stay as Meanwell built them.
   - **SSR:** INPUT 3/4 (DC) is at its front end and LOAD 1/2 (AC) at its rear. The SSR body is the barrier; the hub wall is 2 mm behind it.
   - **Frame PE:** moves from LDO's x ≈ +105, which would cross the notch zone, to the rear extrusion at x ≈ −20, behind the hub.
   - **Closest AC–DC neighbours:**
     - hole-run cap ↔ S-jog: 9.9 mm;
     - hole run ↔ rear-upper run: 11 mm;
     - hub ↔ DC open end: 18 mm.
   - **Honest limit:** the WAGO blocks and the inlet→WAGO leads stay as LDO builds them. The hub's rear wall sits 0.8 mm off the port faces, so every lead from a port goes straight into the hub.
3. **Fewer runs.**
   - **LDO:** five loose PVC runs, mains mixed into the rear one.
   - **MSS, stock bay:** one DC perimeter loop plus a T-spine, and an AC box with three branches.
   - **v2:** two conduits, one DC and one AC, with 3 corners and 2 T junctions. The middle run is the only conditional part.

## Component shifts and the leads they lengthen (lengths unknown: each is a bench check)
- **Front DIN rail, with the Leviathan + Pi and the USB adapter clipped on it: 7 mm toward the door.** Opens the middle gap to ~33 mm.
  - Lengthens by ≤ 7 mm: HV, 24V PSU→MB, 24V→USB adapter, SSR SIG, and the six stepper leads at the rear-edge headers.
- **PSU: 4 mm left on its DIN clips.** Clears the right run's lid and the right T_REG fillet. Only 1.1 mm clearance otherwise, at apparent scale.
  - Lengthens by ~4 mm: 24V PSU→MB, 24V→USB adapter.
- **Routing changes (no DIN shift):**
  - A and B go notch → right run → middle run: **+195 / +129 mm** estimated;
  - bed TH, nozzle probe and filter fan go through the notch: **~+44 mm** (±25);
  - bed L: +11 mm;
  - Z0–Z3: +11…+37 mm, worst Z2;
  - frame PE lug: shorter;
  - umbilical: −12 mm.

## Bench checks (numbered; thresholds)
1. **A and B spare length** at HV-STEPPER-0/1 on LDO's route: **≥ 215 mm (A)** and **≥ 150 mm (B)**.
   - Short → two 4-pin JST-XH extensions, a purchase and Alex's call. The only other route crosses the AC zone.
2. **TH, probe and filter-fan leads** each reach source → notch → header with **≥ 65 mm** spare on LDO's route. The notch passes three extra cables beside the Z-chain bundle without pinching.
   - Short → fallback: seat the hole-run endcap over the hole's right third, and run those three DC leads 10 mm across open deck to the rear-upper run.
3. **Middle run** after the 7 mm rail move: Leviathan PCB rear edge → PSU front edge **≥ 32 mm**, and the rail T-nuts slide 7 mm.
   - Short → middle run off: replace each T_REG with an 82 straight and keep LDO's PVC middle duct.
4. **Front run** inner wall → Leviathan front header row **≥ 15 mm** (est. 19.8).
5. **After the 4 mm PSU move:** PSU → right-run lid **≥ 2 mm**, and PSU front-right corner → right T_REG rear fillet **≥ 2 mm** (est. 1.1 apparent, ~3.6 after the PSU's known ~1.4 % photo magnification).
6. **PSU left end → hub right wall ≥ 3 mm** (est. 3.0 including the lid overhang).
7. **SSR rear edge (with its DIN tab) → WAGO port face: 100 ± 1 mm.** Other → regenerate the hub with `HY = gap − 51.2` (`work/remix.py`).
8. **Deck-hole centre** 19 ± 1.5 mm behind the PSU rear edge. Hole edges **≥ 1 mm** inside the hole run's inner walls (est. 1.5). The run can slide ±3 mm in y.
9. **Notch front edge ≥ 1 mm** behind the rear-upper run's rear wall (est. 0–1).
10. **Z1 plug tip → hub left wall ≥ 6 mm.** L2 end → RL motor ≥ 3 mm (est. 4.6). Z2 plug → RR corner ≥ 10 mm.
11. **Right-run outer wall → bay-fan splicer and frame ≥ 3 mm** (est. 3.1; splicer position unverified).
12. **Frame PE:** a free, bare-metal slot on the rear extrusion at x ≈ −20, between the WAGO-mount screw (~−31) and the notch. Then C14 earth → far corner **< 2–3 Ω** (10.16).
13. **Fin:** ≥ 2 mm to the terminal 6 and 7 screws (nominal 3.5 each side), and top ≥ the PSU top.
14. **PSU silkscreen** reads +V ×3, −V ×3, FG, N, L front to rear. The fin's position depends on it.
15. **Spare length:** Z2 ≥ 40 mm; HV, 24V PSU→MB, 24V→USB adapter and SSR SIG ≥ 12 mm; bed L ≥ 15 mm.

## Ch 09 / 10 steps needing an amended variant (ids only, no renumbering)
- **Amend:**
  - 09.5 (front rail 7 mm forward), 09.6 (printed conduits replace the five PVC ducts), 09.16 (PSU 4 mm left), 09.36;
  - 10.8, 10.9, 10.11, 10.12 (TH to the notch), 10.14, 10.15, 10.16 (PE lug position), 10.34 (probe via the notch), 10.41, 10.42 (A/B route), 10.44, 10.48 (filter fan via the notch), 10.51, 10.68, 10.69 (two openings: hole = AC, notch = DC), 10.71 (lids), 10.72 (differences from LDO's photo).
- **Append:** 10.80, "Fit the strip fin and close the AC hub lid", after the DC feeds and before 10.73.

## Material (PrusaSlicer 2.9.6 CLI, `slicer/voron-coreone-asa.ini`, Voron spec; PETG = ASA-slice cm³ × 1.27 g/cm³, density swap, no PETG slice)
| Set | Plates | Time (ASA profile) | ASA g | PETG g |
|---|---|---|---|---|
| Black DC loop (without the middle run) | 4 | 22 h 06 m | 231.7 | 274.9 |
| Black middle run (conditional) | 1 | 4 h 26 m | 46.6 | 55.3 |
| Orange AC | 1 | 3 h 55 m | 54.7 | 64.9 |
| **Total** | 6 | **30 h 27 m** | **333.0** | **395.1** |

- v1's full set was 266.7 g ASA / 316.5 g PETG.
- Black plate 4 holds a single 130 cover; merge it into any other plate.
- G-code and `results.json` are in `slice/`.
