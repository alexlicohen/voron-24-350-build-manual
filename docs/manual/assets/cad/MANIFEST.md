# CAD render manifest

15 manual steps illustrated from the official Voron 2.4r2 STEP
(18 manifest entries, 28 PNGs).
Generated from `steps.yml` by `scripts/cad_render/render_steps.py --manifest` —
edit that file, not this one.

Two standing caveats apply to every image and are printed in every footer:

1. **The published CAD is the 250 machine.** Part identity, handedness, mounting
   faces and assembly relationships transfer to this 350 build; extrusion, rail
   and belt **lengths do not**. Per-image detail is in the *350 caveat* line below.
2. Anything labelled **(schematic)** is a box drawn by the renderer, not Voron
   geometry — the LDO Rev D+ and mod hardware (rail stops, titanium backers,
   the USB/ESD adapter) is absent from the Voron CAD.

## For the pass that inserts these

- `a` = the selected parts alone; `b` = the same parts in place with the rest of
  the machine ghosted. Where only one is listed, the other was judged to add
  nothing.
- Put the image line(s) directly under the `### Step` heading, replacing
  `(no image — see text)` where that is what the step still shows. Where the
  step already carries a manual page, a parts render or a bench photo, **add**
  these after it — do not replace the existing image.
- Every one of these steps already has a `**What you're looking at:**` line
  written by the chapter author. Fold the sentence below into it; do not add a
  second one.
- The *currently shows* column and the *already in the chapter* lines record the
  chapters as they stood when this file was generated, while they were still
  being written. Re-run `--manifest` and re-check before inserting.

## Index

| Step | Chapter | Images | Currently shows | Ready |
|---|---|---|---|---|
| 01.15 | `01-frame.md` | 01-15-a.png | assets/cad/01-15-a.png | yes |
| 02.09 | `02-z-drives.md` | 02-09-a.png, 02-09-b.png | assets/manual-pages/manual-p027.png + assets/cad/02-09-a.png + assets/cad/02-09-b.png | **no** |
| 02.10 | `02-z-drives.md` | 02-10-a.png, 02-10-b.png | assets/parts/z_rail_stop_x4.png + assets/cad/02-10-b.png | yes |
| 03.18 | `03-build-plate.md` | 03-18-a.png, 03-18-b.png | assets/cad/03-18-a.png + assets/cad/03-18-b.png | yes |
| 05.4 | `05-gantry.md` | 05-04-a.png, 05-04-b.png | assets/cad/05-04-a.png + assets/cad/05-04-b.png | yes |
| 05.15 | `05-gantry.md` | 05-15-a.png, 05-15-b.png | assets/cad/05-15-a.png + assets/cad/05-15-b.png | yes |
| 05.18 | `05-gantry.md` | 05-18-a.png, 05-18-b.png | assets/cad/05-18-a.png + assets/cad/05-18-b.png | yes |
| 05.45 | `05-gantry.md` | 05-45-a.png, 05-45-b.png | assets/parts/pair-x_frame_V2TR_MGN12.png + assets/cad/05-45-a.png + assets/cad/05-45-b.png | yes |
| 05.46 | `05-gantry.md` | 05-46-a.png, 05-46-b.png | assets/cad/05-46-a.png + assets/cad/05-46-b.png | yes |
| 06.23 | `06-z-axis-and-gantry-squaring.md` | 06-23-a.png, 06-23-b.png | assets/cad/06-23-a.png + assets/cad/06-23-b.png | yes |
| 06b.7 | `06-z-axis-and-gantry-squaring.md` | 06b-07-b.png | assets/cad/06b-07-b.png | yes |
| 06b.13 | `06-z-axis-and-gantry-squaring.md` | 06b-13-a.png, 06b-13-b.png | assets/cad/06b-13-a.png + assets/cad/06b-13-b.png | yes |
| 06b.14 | `06-z-axis-and-gantry-squaring.md` | 06b-14-a.png, 06b-14-b.png | assets/diagrams/09-gantry-racking.svg + assets/cad/06b-14-a.png + assets/cad/06b-14-b.png | yes |
| 07.30 | `07-ab-belts.md` | 07-30-a.png, 07-30-b.png | assets/cad/07-30-a.png + assets/cad/07-30-b.png | yes |
| 09.26 | `09-electronics-bay.md` | 09-26-a.png, 09-26-b.png | assets/cad/09-26-a.png + assets/cad/09-26-b.png | yes |

## Per-step detail

### 01.15 — Check the frame sits without rock

Chapter `01-frame.md` · currently shows: assets/cad/01-15-a.png

**`01-15-a.png`** (parts alone) — The squared frame on its reference surface: the four bottom corners that must all touch, and the four top corners you press.

**350 caveat:** CAD frame is the 250: 370 mm horizontals on 430 mm verticals. Yours is the 350 set. The contact geometry is the same.

Already in the chapter, do not add again: `01-15-a.png`

**What you're looking at:** The finished frame standing on the stone - the four bottom corners are the only things that should touch it, and the four top corners are where you press to find a rock.

### 02.09 — Install the remaining three Z rails

Chapter `02-z-drives.md` · currently shows: assets/manual-pages/manual-p027.png + assets/cad/02-09-a.png + assets/cad/02-09-b.png

**`02-09-a.png`** (parts alone) and **`02-09-b.png`** (in place, rest of the machine ghosted) — Plan view of the four Z rails. Rear rails occupy y 345.5-352 on verticals at y 352-372 (facing forward); front rails occupy y -18 to -11.5 on verticals at y -38 to -18 (facing rearward). All four normals are +/-Y.

**350 caveat:** CAD rails are MGN9 300 mm on 430 mm verticals (250). Yours are MGN9H 400 mm on the 350 verticals. Which face the rail is on does not change with size.

Already in the chapter, do not add again: `02-09-a.png`, `02-09-b.png`

**What you're looking at:** The four Z rails seen from above. Each rail sits on a face whose normal points along Y, so the left pair faces each other front-to-back and the right pair does the same - the two front rails are parallel, not opposed.

> EVIDENCE FOR PILOT.md §8 - do NOT insert until Step 02.09's text is fixed. The step currently says "front-left faces front-right, rear-left faces rear-right"; the CAD says front-left faces rear-left. Insert once the chapter owner has corrected the pairing claim.

### 02.10 — Optional: fit the LDO rail stops at the top of each Z rail

Chapter `02-z-drives.md` · currently shows: assets/parts/z_rail_stop_x4.png + assets/cad/02-10-b.png

**`02-10-a.png`** (parts alone) and **`02-10-b.png`** (in place, rest of the machine ghosted) — The free top end of one Z rail and the carriage that must not run off it; the LDO printed stop clips over that end (drawn schematically).

**350 caveat:** CAD rail is MGN9 300 mm on a 430 mm vertical (250), leaving ~107 mm of bare extrusion above the rail. Your 400 mm rail on the 350 vertical leaves a different length. The stop clips to the rail end, not to a dimension.

Already in the chapter, do not add again: `02-10-b.png`

Image line(s) to add, immediately after the step heading:

```markdown
![CAD render — LDO rail stop at the top of a Z rail](assets/cad/02-10-a.png)
```

**What you're looking at:** The top of one Z rail where it stops short of the vertical extrusion's end - that free length is where the printed stop clips on, and the carriage below it is the thing the stop keeps captive.

### 03.18 — Verify the plate floats level

Chapter `03-build-plate.md` · currently shows: assets/cad/03-18-a.png + assets/cad/03-18-b.png

**`03-18-a.png`** (parts alone) and **`03-18-b.png`** (in place, rest of the machine ghosted) — The plate floating on its four bolts above the two bed extrusions: four gaps, all equal to the thumb-nut height.

**350 caveat:** CAD bed is the 10 in (254 mm) MIC6 plate on 370 mm bed extrusions (250). Yours is the 350 plate on the 350 frame - still four bolts, four gaps.

Already in the chapter, do not add again: `03-18-a.png`, `03-18-b.png`

**What you're looking at:** The build plate riding on four bolts above the two bed extrusions that span the frame - the gap under each bolt is what you measure, and all four should be the same.

### 05.4 — Test-fit T-nuts and stage the fasteners

Chapter `05-gantry.md` · currently shows: assets/cad/05-04-a.png + assets/cad/05-04-b.png

**`05-04-a.png`** (parts alone) and **`05-04-b.png`** (in place, rest of the machine ghosted) — The four gantry extrusions with every T-nut the chapter uses, shown on the faces they go into.

**350 caveat:** CAD extrusions are the 250 lengths (E 240, C 350, D 330 mm); yours are the 350 set. Which faces carry nuts, and how many, is what transfers.

Already in the chapter, do not add again: `05-04-a.png`, `05-04-b.png`

**What you're looking at:** The four gantry extrusions - E across the back, the two C side beams and the D cross beam - with every T-nut this chapter needs already in its slot, because the printed blocks cap those slots later on.

### 05.15 — Stop the carriages running off

Chapter `05-gantry.md` · currently shows: assets/cad/05-15-a.png + assets/cad/05-15-b.png

**`05-15-a.png`** (parts alone) and **`05-15-b.png`** (in place, rest of the machine ghosted) — Both Y rails with their carriages and a schematic stopper near each of the four rail ends.

**350 caveat:** CAD Y rails are MGN9 300 mm; yours are 400 mm (Step 05.10). The stoppers go near the ends wherever those ends are.

Already in the chapter, do not add again: `05-15-a.png`, `05-15-b.png`

**What you're looking at:** The two Y rails on the undersides of the C extrusions, each carrying one carriage - the stoppers near the ends are what stop a carriage sliding off and scattering its ball bearings.

### 05.18 — Fit the second Y backer

Chapter `05-gantry.md` · currently shows: assets/cad/05-18-a.png + assets/cad/05-18-b.png

**`05-18-a.png`** (parts alone) — One Y beam from below: the rail face and, opposite it, the face the titanium backer goes on.

**`05-18-b.png`** (in place, rest of the machine ghosted) — Both finished Y assemblies in the gantry, mirrored: rails underneath, backers on the two top faces.

**350 caveat:** CAD C extrusion is 350 mm with a 300 mm rail (250 machine); yours is the 350-kit C with a 400 mm rail.

Already in the chapter, do not add again: `05-18-a.png`, `05-18-b.png`

**What you're looking at:** One Y extrusion seen from underneath, so the rail face and the backer face are both in frame - the backer always goes on the face directly opposite the rail. Both Y beams in place, mirrored about the machine's centreline - rails underneath on both, backers on top on both.

### 05.45 — Stage the X-carriage frame halves

Chapter `05-gantry.md` · currently shows: assets/parts/pair-x_frame_V2TR_MGN12.png + assets/cad/05-45-a.png + assets/cad/05-45-b.png

**`05-45-a.png`** (parts alone) and **`05-45-b.png`** (in place, rest of the machine ghosted) — The two handed X-carriage halves, the probe retainer and the MGN12H carriage whose bolt pattern they have to match.

**350 caveat:** none - nothing in this image is size-dependent.

Already in the chapter, do not add again: `05-45-a.png`, `05-45-b.png`

**What you're looking at:** The two halves of the X carriage - handed, so they only nest one way - together with the probe retainer and the MGN12 carriage block whose bolt pattern they must match.

> Step 05.45 already carries assets/parts/pair-x_frame_V2TR_MGN12.png from an earlier pass. Add these as additional images, do not replace that one.

### 05.46 — Bag what belongs to later chapters

Chapter `05-gantry.md` · currently shows: assets/cad/05-46-a.png + assets/cad/05-46-b.png

**`05-46-a.png`** (parts alone) — Both Rev D+ alternates pulled apart along Z and labelled: the D2F pod you print, the hall-effect pod you skip, the 2-hole bridge you keep, the 3-hole one you do not.

**`05-46-b.png`** (in place, rest of the machine ghosted) — The two parts you keep, shown where they will eventually sit on the right XY joint.

**350 caveat:** none - nothing in this image is size-dependent.

Already in the chapter, do not add again: `05-46-a.png`, `05-46-b.png`

**What you're looking at:** The two either/or choices on the right XY joint, pulled apart so you can see both at once - print the D2F endstop pod and keep the 2-hole cable bridge; the hall-effect pod and the 3-hole bridge are not used in this kit. Where the endstop pod and the cable bridge you kept eventually live - both on the right-hand XY joint, fitted in later chapters.

### 06.23 — Even the four belts by hand

Chapter `06-z-axis-and-gantry-squaring.md` · currently shows: assets/cad/06-23-a.png + assets/cad/06-23-b.png

**`06-23-a.png`** (parts alone) — One Z idler mount seen from below, with the M3x16 tensioner bolt that adjusts that corner's belt.

**`06-23-b.png`** (in place, rest of the machine ghosted) — All four Z belt runs, from the drives at the bottom of each upright up to the idlers at the top.

**350 caveat:** Idler height is the 250 machine's. There is one of these at each of the four corners either way.

Already in the chapter, do not add again: `06-23-a.png`, `06-23-b.png`

**What you're looking at:** The Z idler at the top of one upright, seen from underneath - the small bolt standing proud below it is the tensioner, and turning it changes that corner's belt tension. The four Z belts that hang the gantry, one down each upright - each runs from its drive at the bottom, up over the idler at the top, and back to the gantry corner.

### 06b.7 — Confirm access to the Z and XY joints (the side panels are not on yet)

Chapter `06-z-axis-and-gantry-squaring.md` · currently shows: assets/cad/06b-07-b.png

**`06b-07-b.png`** (in place, rest of the machine ghosted) — The two side panels, and the four Z joints and two XY joints that come within reach once they are off.

**350 caveat:** none - nothing in this image is size-dependent.

Already in the chapter, do not add again: `06b-07-b.png`

**What you're looking at:** The two side panels of the enclosure, and behind them the four Z joints in the corners and the two XY joints on the gantry - the parts every step in Part B has to reach.

### 06b.13 — Reinstall the lower Z joints, lightly

Chapter `06-z-axis-and-gantry-squaring.md` · currently shows: assets/cad/06b-13-a.png + assets/cad/06b-13-b.png

**`06b-13-a.png`** (parts alone) and **`06b-13-b.png`** (in place, rest of the machine ghosted) — One Z joint in section: the lower half on its rail carriage, the upper half under the gantry, and the single M5x40 that joins them.

**350 caveat:** none - nothing in this image is size-dependent.

Already in the chapter, do not add again: `06b-13-a.png`, `06b-13-b.png`

**What you're looking at:** A Z joint at one corner - the lower block rides the Z rail carriage, the upper block sits under the gantry corner, and one M5x40 joins the two; left light, the pair can still pivot.

### 06b.14 — De-rack the gantry, then tighten the X/Y joints

Chapter `06-z-axis-and-gantry-squaring.md` · currently shows: assets/diagrams/09-gantry-racking.svg + assets/cad/06b-14-a.png + assets/cad/06b-14-b.png

**`06b-14-a.png`** (parts alone) and **`06b-14-b.png`** (in place, rest of the machine ghosted) — The six bolts that hold each XY joint to the X beam - two from the top per side, one from below per side - and the drive units the beam is pushed back against.

**350 caveat:** none - nothing in this image is size-dependent.

Already in the chapter, do not add again: `06b-14-a.png`, `06b-14-b.png`

**What you're looking at:** The XY joint clamped to the end of the X beam: two bolts come down from the top of the beam and one comes up from underneath, and those are the ones you tighten while the beam is held hard back against both drive units.

> The same image serves Step 06b.12 ("retighten everything except the X/Y joints") - it identifies exactly the bolts that step tells you to leave.

### 07.30 — Set the 150 mm measuring span

Chapter `07-ab-belts.md` · currently shows: assets/cad/07-30-a.png + assets/cad/07-30-b.png

**`07-30-a.png`** (parts alone) and **`07-30-b.png`** (in place, rest of the machine ghosted) — The XY joint idler and the front idler on each side, and the belt span between them that the 150 mm figure refers to.

**350 caveat:** The 150 mm is set by moving the gantry, and the CAD shows a parked 250 machine, not the measuring pose. Take which two centres from the picture, take the number from the rule.

Already in the chapter, do not add again: `07-30-a.png`, `07-30-b.png`

**What you're looking at:** The two idlers a belt runs between on each side - one in the XY joint at the back of the Y beam, one in the front idler block - and the free length of belt between them that you pluck.

### 09.26 — Clip the USB adapter to the front rail

Chapter `09-electronics-bay.md` · currently shows: assets/cad/09-26-a.png + assets/cad/09-26-b.png

**`09-26-a.png`** (parts alone) and **`09-26-b.png`** (in place, rest of the machine ghosted) — The two bay DIN rails, which one is the front, and where along it the USB/ESD adapter clips.

**350 caveat:** Bay layout is the 250 machine's; the rails are shorter than yours, but front/rear and left/right are the same.

Already in the chapter, do not add again: `09-26-a.png`, `09-26-b.png`

**What you're looking at:** The two DIN rails that run across the electronics bay - the front one is the one nearer the door, and the adapter clips onto its right-hand end.
