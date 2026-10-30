# G4b — Ch 08 / Ch 09 / B06 / B07 / B11 images (goal 2 only, finishing G4)

**Group:** G4b. Scope = the images G4's header lists as unchecked; G4's findings (G4-05, -06, -11 etc.) are not repeated.

**Files covered:** `docs/manual/08-toolhead.md` (08.13, 08.23, 08.24, 08.27, 08.29, 08.32, 08.34–08.36, 08.39–08.41,
08.43, 08.52, 08.53, 08.56, 08.57, 08.59, 08.60, 08.63, 08.65), `docs/manual/09-electronics-bay.md` (09.1, 09.2, 09.4,
09.6–09.21, 09.23, 09.24, 09.27, 09.29, 09.31–09.33, 09.36), `docs/manual/print/B06-*.md`, `B07-*.md`, `B11-*.md`.
Images were read from the fresh `site/` build, so each is the file the step page actually shows: the crop PNG, and
where it ends up on the page.

**Primary sources used:** SB manual crops/pages (`sb-pages/`), Voron manual pages p.028, 146–172 (`manual-pages/`);
LDO mirrors under `assets/remote/` (Nitehawk-SB V2, Leviathan V1.3, LDOVoron2 RevD) and the pinned LDO copies
under `assets/ldo/` (pixel-compared); LDO build-FAQ page notes (saved `voron2_build-faq.html`: p.149, 156, 169,
170–171); committed plate projects `slicer/plates/{B06-P1,B07-P1,B07-P2,B11-P1..P5}.3mf` (`Slic3r_PE_model.config`
names plus `3D/3dmodel.model` build transforms → per-object XY bounding boxes); `slicer/bins.py`; plate SVG text and
outline paths; `assets/parts/power_inlet_IECGS_1mm.png`.

**Images opened:** 68 in 17 contact-sheet reads plus 5 zooms. Ch 08: 23. Ch 09: 34, including the full p.158 page
(it renders uncropped, see G4b-01). Batch pages: 8 plate PNGs, the coupon render and the layout-v3 overlay. Also
the full p.146 page and the IECGS part render, for comparison. No request-limit errors.
Not re-opened: `06-harness-map.svg` (08.52) and `07-leviathan-jumper-map.svg` (09.19); G4 already rendered both.

**Plate diagrams (all 8), checked by script:** each 3MF object is matched to its diagram outline by name and by
position. The 3MF bounding box (build transform applied to the mesh) is compared with the SVG outline (3.6 px/mm,
origin at the front-left corner). All 83 objects match, every one within 1 mm summed over the four bbox edges.
Object counts: B06-P1 19, B07-P1 11, B07-P2 11, B11-P1 2, P2 10, P3 15, P4 18, P5 8. Each legend bin equals
`slicer/bins.py`. The 10 mm pieces split as the steps say: B11-P4 `V3L_10mm_DUCT` has 1 in 09-ducts-DC (09.6) and
2 in 09-ducts-AC (09.36). Lids sit in 10-lids-AC / 11-lids-DC, and `V2L_STRIP_FIN` is in 10-lids-AC (10.80). The
PNGs match their SVGs visually.

Counts: **0 blocker, 0 major, 5 minor, 4 nit** (all goal 2; G4b-03 is goal 1/2).

---

### G4b-01 minor goal 2 — 09.27, 09.28 and 09.30: a trailing " ·" demotes the Voron page out of the figure; it renders uncropped inside the collapsed "What you're looking at"

- `09-electronics-bay.md:748` `![Voron manual p.158](assets/manual-pages/manual-p158.png){ crop="0.36 0.24 0.56 0.72" } ·`.
  Same at `:771` (p.160, 09.28) and `:822` (p.161, 09.30). These are the only three image lines in the manual with
  trailing text.
- Built pages `site/manual/steps/09-electronics-bay/09-27/`, `09-28/` and `09-30/`. The step figure holds only the
  LDO photo(s). The Voron page sits inside `<details class="note"><summary>What you're looking at</summary>`, which
  is closed by default. It renders as `<img … crop="0.36 0.24 0.56 0.72" src="…manual-p158.png">`: the crop is
  passed through as an inert HTML attribute, so the full uncropped page shows, followed by a stray "·".
- Effect: at 09.30 the builder never sees p.161, the only drawing of the probe *mounted*. LDO's
  `nozzle-probe-installed.jpg` is the bench-finished probe, and its own alt says "mounting is p.161". At 09.28 the
  ⚠ explains "two screws, not the four the manual's render shows", but that render is hidden.
- Fix: delete the trailing ` ·` on lines 748, 771 and 822, then rebuild. Each page then leads with the cropped
  Voron page and the LDO photos.

### G4b-02 minor goal 2 — 09.10's image is the manual's `power_inlet_filtered` with five inserts; the step (correctly) presses three

- `09-electronics-bay.md:337` p.156 crop `p156-e9b0ffea.png`. It shows a two-window panel (filtered inlet plus a
  separate rocker) with **five** heat-set inserts: one on the top rail, one on the right side, one between the
  windows and two in the curved cut-out.
- vs `:344` "M3×5×4 heat-set insert ×3" and `:346` "one in the rail, two in the curved cut-out". Three is right for
  `power_inlet_IECGS_1mm` (STL bore count 3, 10-23 G4). LDO build FAQ: "PAGE 156 Use the 1.0mm AC inlets with
  integrated switches plug panel." The ⚠ names the different file but never says the drawing has two more inserts
  than your part, and alt text is not rendered.
- Fix: in the Do, after "press one insert into each of the three bores", add "p.156 draws the manual's two-window
  panel with five; yours has three bores, so ignore the other two." Optionally put
  `![power_inlet_IECGS_1mm — your panel](assets/parts/power_inlet_IECGS_1mm.png)` first.

### G4b-03 minor goal 1/2 — 09.6's Check asks for "One closed loop"; the overlay draws the DC conduit open at both rear ends

- `09-electronics-bay.md:261` "**Check:** One closed loop, joints marked, …"; `print/B11-bay-ducting.md:14` "The
  **DC conduit** is one loop".
- `assets/b11/layout-v3-overlay.jpg` (09.6, 09.36, B11), zoomed on the rear-left. The left run (58c → T(N) → 130c)
  ends at the rear-left Z motor, with nothing joining it. The rear run (RR 90 → 58c → 45 → 45 → 10c) ends at the
  Z-chain notch. The AC wire box fills the space between them. The DC conduit is a C, open at both rear ends. The
  piece list agrees: one 130, and no rear-left corner in the DC Parts or on B11-P2/P4.
- Effect: a builder checking for a closed loop looks for a missing rear-left corner piece, or butts the 130 into
  the AC wire box. The latter is a DC-to-AC contact the layout keeps 12 mm apart.
- Fix: `:261` "**Check:** One continuous run from the rear-left Z motor, round the front, to the notch; every joint
  pushed closed and marked, …". Also say "one continuous run" at `:239` ("The DC loop …") and B11:14. Confidence:
  high on the drawing. The overlay is approximate (±6 %), but the gap is a whole component width.

### G4b-04 minor goal 2 — 09.2 "Read the placement you are actually building" shows only the manual's wrong layout, and sends the builder to GitHub for the photo the repo already mirrors

- `09-electronics-bay.md:141`: the p.149 crop draws Pi on its bracket, "Controller Board" and "5V PSU" on the
  manual's layout. `:147` "Match the bay against LDO's placement photo [`S0General_Placement.jpg`](https://raw.githubusercontent…)";
  `:149` "You have that photo open on a phone or second screen." `:1016` (09.36) links the same raw URL again.
- `assets/remote/09-electronics-bay/bay-general-placement.jpg` is that exact LDO photo: SOURCES.txt cites that URL,
  the mean pixel diff against `assets/ldo/…/RevD/S0General_Placement.jpg` is 2.5/255, and it is resized only. It is
  already embedded at 09.22 (`:625`). On the iPad, a phone or second screen is an extra device for no reason.
- Fix: at 09.2 put
  `![LDO Rev D general placement: Leviathan + Pi and the USB adapter on the front rail, SSR and PSU on the rear, inlet and WAGO bus at the rear-left (© LDO Motors)](assets/remote/09-electronics-bay/bay-general-placement.jpg)`
  first, and keep p.149 second. Change the Check to "You can find each item of the photo above on your bench."
  At 09.36 (`:1016`), point to the local image instead of the raw URL.

### G4b-05 minor goal 2 — 08.43 says "the photo … is the source" for the ground-lug position, but its photo is the bare product shot

- `08-toolhead.md:1021` `nitehawk-sb_title_img.jpg` shows both boards loose on white, with no CW2, no screws and
  no lug. `:1034` "Trap the supplied ground cable's ring lug under the lower M3×8 head … `(verify on bench — the
  photo, not LDO's prose, is the source)`".
- The photo that shows it is `toolboard_ground_routing.jpg`, left panel. It has the board on the CW2 and the ring
  lug under the lower-left board screw, tail running down past the gear. It is embedded only at 08.53 (`:1252`).
- Fix: add `![Nitehawk-SB V2 on the Clockwork 2, ground lug under the lower board screw (© LDO Motors)](assets/remote/08-toolhead/toolboard_ground_routing.jpg)`
  to 08.43 after the title image. Alternatively, change `:1034` to "(… LDO's `toolboard_ground_routing` photo at
  08.53 is the source)".

### G4b-06 nit goal 2 — 09.1: "three of the four components pictured are wrong"; p.148 pictures five

- `09-electronics-bay.md:131`. The p.148 crop shows the Pi on its bracket, the controller, the 5 V PSU, the SSR and
  the 24 V PSU. The Check at `:133` names three wrong ones, which leaves two right.
- Fix: "three of the five components pictured are wrong".

### G4b-07 nit goal 2 — 08.57 calls its image "the hand-off page"; the p.146 crop is the Stealthburner title render, and the pointer text is on p.147

- `08-toolhead.md:1365` crop of p.146 is a red SB render only; the full page has nothing else but "STEALTHBURNER".
  `:1367` "The hand-off page … p.146 points you there". The text "Follow the StealthBurner assembly manual … and
  return here to proceed" is on p.147, which 08.65 uses.
- Fix: `:1367` "p.146 is the Stealthburner title page; p.147's one-line pointer (Step 08.65) sends you to the SB
  manual and back."

### G4b-08 nit goal 2 — 09.36's AC-conduit render is orange; "B11 prints every part black" lives only in the unrendered alt

- `09-electronics-bay.md:987`, `assets/b11/ac-conduit-assembled.jpg`: orange bodies with black lids. Alt text is
  never shown on step pages (no figure caption). B11 prints the conduit in Jet Black PETG V0.
- Fix: add to the What-you're-looking-at at `:989`: "The render colours the bodies orange to tell them from the
  lids; yours are all black."

### G4b-09 nit goal 2 — 08.63's photo is LDO's finished Ch 10 chain tie-down, not the loose parking this step does

- `08-toolhead.md:1484` `cable_chain_ties.jpg`: four panels of the umbilical zip-tied along the drag chain with a
  service loop. Step 08.63 puts one loose tie through the anchor tab, and says "chain ties are Ch 10" in its title.
- Fix: begin the What-you're-looking-at with "LDO's photo shows the Ch 10 end state; today only the loop at the
  anchor applies."

---

## Checked and consistent

- 08.13 (SB p.19 bearing slide fit, MR85 ×2 drawn), 08.23 (p.29 M3×8 plus washer through the front access hole),
  08.24 (p.30 mesh/backlash), 08.27 (p.39 heatsink/spring/HeaterCore/nozzle), 08.29 (p.40 wire route plus strain
  relief), 08.32 (p.43 11 mm stickout), 08.34 (p.55 ears off, front cover off), 08.35 (p.47 mask/diffuser/carrier
  order, LED wires up), 08.36 (p.46 120/100/100 mm, index 1/2/3 = logo/right/left), 08.39 and 08.41 (p.51/p.54
  exits "right side", same wording as SB), 08.40 (p.53 wires top, air inwards), 08.59 (p.65 M3×8 through the
  front access hole), 08.65 (p.147 "return here").
- 08.52 `reset_boot_buttons.jpg`: RESET, BOOT0 and ACT beside the 5-pin ZH USB header, as the port table says.
  08.53 `grounding_scheme.jpg`: motor → toolboard → cable → USB adapter → extrusion, matching the What-you're-
  looking-at chain. 08.56: the parts photo, and the `z_stop_install_1.jpg` alt ("collar and shaft already in the
  body, PCB and screws loose", HA2×10 bag, hex key) is true. 08.60 pinout: XT30(2+2) D+/D−/GND/24V as the Do says.
- 09.4 (p.28 notch to the back), 09.7 (p.168 hook/rotate/snap), 09.8 (p.150–151 Pi bracket, skipped), 09.9
  (p.152/172 RS25-5, skipped), 09.12 (p.167 2× M3×8 against the Z mount), 09.13 (p.165 3× 221-415, 2× M5 T-nut,
  M5×10), 09.14 (selector photo at 230 V, alt says so), 09.15 (p.153 2 brackets, M4×6), 09.16 (p.169 top half only;
  the inset puts the PSU at the right of the rear rail), 09.17 (p.157 bracket plus 2× M4×6), 09.18 (p.171 SSR left
  of the PSU, latch), 09.20 (p.154 2× M2×10 per bracket), 09.21 (p.155 M3×6 BHCS drawn, the ⚠ covers M3×8), 09.23
  (Pi 4B on Leviathan V1.3, 3/4 adapter on the GPIO, 6-wire lead to the Leviathan), 09.24 (p.170 Octopus, ⚠
  covers it), 09.27 (LDO parts photo: collar, shaft, 2 screws, PCB), 09.29 (p.159 notch plus set screw), 09.31
  (p.162 soldered switches, skipped), 09.32 (p.163 XY endstop board, 2× M3×8), 09.33 (p.164 2× M3×30).
- 09.11 photos: inlet module fitted (wired, alt says so), and the inlet layout L/N/GND.
- Layout-v3 overlay vs the piece lists. DC: 154 ×2, FL 90 mirror, FR/RR 90 ×2, 58c ×3, 130c, 70c, T(N) ×2, 154N ×2,
  45 ×2, 10c ×1 = 09.6 Parts. AC: wire box, R15 ×2, 34c over the round hole, T_SHORT, 10c ×2, cap ×2 = 09.36 Parts;
  the fin is 10.80. Hatched = remix pieces. Components: Leviathan+Pi front-left, USB adapter front-right, SSR
  rear-left, PSU rear-right, inlet plus WAGO at the rear-left, so "rear at the bottom, x right = printer right" is
  a correct bottom-up view. `din-rails-and-wire-ducts.jpg`: 3 left-right plus 2 front-back PVC ducts, as the LDO ⚠
  says.
- Cosmetic, no action: the 08.24 crop includes SB p.30's QR code, and the 09.21 crop has a clipped text fragment
  at the top-left ("…on will have a fully"). Neither can be cropped out with a rectangle without cutting a drawing.
- B11-P1 coupon render: stock 22 mm beside 22N, lid off/on, as its alt says. All 8 plate diagrams vs 3MF names,
  counts, positions and bins: see the header.
