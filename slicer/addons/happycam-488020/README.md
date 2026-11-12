# HappyCam camera mount (Ch 10 Step 10.81, Ch 11 Part C, batch B12)

Part of the build since 2026-11-12 (Alex): the body and light cover print in the ASA run on plate B12-P2,
right after B10. The camera's USB cable goes into the frame at **Ch 10 Step 10.81**, before the LED lead's
slot covers; the mount is fitted at Ch 11 Step 11.74, after Step 11.68 has checked the camera board against it.

## Licence and credit

**CC BY-NC.** **Voxel3D_NL**, *HappyCam, Voron 2.4 OV5640 camera mount*,
<https://www.printables.com/model/488020>. `HappyCam_main-350.stl` and `Cameradoor_120.stl`, unchanged,
fetched to `slicer/stl/printables/488020/` by `python3 slicer/fetch_stls.py`: the closed-door fallback.

**Printed pair (Alex 2026-11-12): CC BY-NC-SA.** **Zemistr**, *HappyCam OV5640 - camera width light cover*,
<https://www.printables.com/model/527904>, a remix of 488020: `HappyCam_cover_with_light.stl` (a flat
1.5 mm cover with a window over the lens and one over the board's LED) and the `HappyCam_main-350.stl` it
was drawn against, unchanged, fetched to `slicer/stl/printables/527904/`. That body shares 4687 of the
original's 4845 vertices: the two ends are re-cut 0.68 mm and the pegs and mount holes are identical, so
every number below holds. The cover on the 488020 body is untested, so the pair prints together. Nothing
is remixed here, so nothing is committed here. The page's STEP file is empty (4 kB, its comments say so too), so the STLs are
the only geometry.

## Fit, read from the STLs

- The body bolts to the **inner face of the top front extrusion**, centred, with 2 × M3×20 SHCS into roll-in
  T-nuts: 14.96 mm of plastic sits under the head, so the page's M3×16 or M3×18 ends 1–3 mm past the face,
  short of or barely into the nut. The door closes the board pocket with 1 × M3×8 SHCS.
- Board pocket: **three** Ø1.7 mm locating pegs, two 4.0 mm apart across the closed end and the third
  **50.0 mm** along (the author's page: "3 little pegs"); pocket about 75 mm long, open at the cable end.
  That is a bar-shaped OV5640 USB board; check a seller's drawing has a hole over every peg. Step 11.68's
  calculator checks a bought board against these numbers before anything is printed.
- The cable leaves the body at its **printer-left end** (the pocket's open end wall; the door screw is at the
  right). Step 10.81 leaves the tail 5 cm left of centre, then runs right along the top front and top right
  extrusions and down the rear-right vertical; the route is about 2 m, hence a 3 m cable.
- Lens: builders on 350 frames report a ~68–72° lens shows the whole bed; 95° and wider look too far
  away from this height (page comments, 2024–2026).

## Print (plate B12-P2)

With the side spool's tube holder, Galaxy Black ASA, `slicer/voron-coreone-asa.ini`, satin sheet, no glue. The
files are drawn as installed: `slicer/plates.py` `ORIENT` turns the 527904 body 180° about X onto its top face
(keyed by path: this folder's fallback body shares the file name); the light cover is drawn flat, outer face
down. Build-plate-only supports on the body alone, for the cable exit (`slicer/plates.py` `OBJECT_SETTINGS`).
Plate estimate: 28 g, 1.8 h (PrusaSlicer 2.9.7, 3 mm brims); sliced alone, the body is 18.6 g with its
supports and the cover 1.5 g. Bin `11-camera`, with the bought board.

## Software

MainsailOS ships crowsnest. The camera is one `[cam]` section with `mode: ustreamer` on port 8080, which
MainsailOS serves at `/webcam/`. In Mainsail add it as **Adaptive MJPEG-Streamer**: plain MJPEG-Streamer
does not play on iOS, and the bench reader is an iPad. Step 11.76 has the section.
