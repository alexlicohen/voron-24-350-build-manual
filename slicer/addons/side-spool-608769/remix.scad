// Side spool frame for the LDO Voron 2.4 350, remixed to carry a Prusa Universal Puck
// (Ch 11 Part C). The one generator of side_spool_frame_puck.stl:
//
//     cd slicer/addons/side-spool-608769 && openscad -q --export-format binstl \
//         -o side_spool_frame_puck.stl remix.scad
//     ... -D stack=6.8 ...      only if Step 11.68 measured the panel stack over 6.3 mm
//
// Source: Maltasrc, "Voron 2.4 (350 bed) Side mounted spool", Printables 608769,
// source/"Reel Mount 2_Frame v1.stl" unchanged (CC BY-NC-SA 4.0; this file and its output are
// derivatives under the same licence).
//
// The source is drawn installed on the RIGHT side panel: x out of the panel (body x 0..15, feet
// x -3.5..0 on the extrusion faces), y front -> rear (front vertical extrusion slot at y -80),
// z up (top side extrusion top at z 90, its slot at z 80). Changes:
//   1. feet 3.5 -> `stack` tall, for LDO's 3 mm PC side panel on 3 mm foam tape;
//   2. the peg hub (three M3 into a printed peg) -> a solid boss for Prusa's Universal Puck,
//      four M3x20 SHCS from the panel side into the puck's pilot holes;
//   3. the two extrusion-screw counterbores deepened so an M3x20 SHCS reaches a roll-in T-nut;
//   4. output turned to its print orientation, the front face (x 15) on the bed.

stack     = 6.5;              // foot height: 3 mm PC + 3 mm foam + 0.5 clearance
foot0     = 3.5;              // the source's foot height
body_t    = 15;               // body, x 0..15
hole      = 3.4;              // M3 clearance (the source's)
cb_d      = 6.5;              // counterbore diameter (the source's)
screw     = 20;               // M3x20 SHCS everywhere
tip_depth = 5;                // extrusion screws: tip this far below the extrusion face
mounts    = [[89.97, 80.0], [-80.03, -90.0]];   // (y, z) of the two extrusion screws
hub       = [20.4, -20.36];   // (y, z) of the source peg axis: centre of its three screws
boss_r    = 31.5;             // the puck's flange is 60.2 mm across
puck_sq   = 13.0;             // puck pilot holes at (+-13, +-13) about its axis (Universal-puck-R1)
puck_cb   = 3.5;              // SHCS head (3.0) sunk 0.5 below the back face
view      = "print";          // "print" | "installed"
$fn = 96;

seat = screw - stack - tip_depth;               // x of the extrusion-screw head seat
assert(seat > 3 && seat < body_t - 1, "stack out of range for an M3x20");
// puck screws: head seat at x puck_cb, tip inside the puck by screw - (body_t - puck_cb)
assert(screw - (body_t - puck_cb) >= 8, "puck screws engage under 8 mm");

module src() { import("source/Reel Mount 2_Frame v1.stl", convexity = 10); }

// The source feet, copied out by (stack - foot0). The box stops 0.5 short of x 0 so the
// body's back face is not dragged along as a zero-thickness sheet.
module feet_extension() {
  translate([-(stack - foot0), 0, 0])
    intersection() { src(); translate([-foot0 - 1, -200, -200]) cube([foot0 + 0.5, 400, 400]); }
}

module boss() {
  translate([0, hub[0], hub[1]]) rotate([0, 90, 0]) cylinder(r = boss_r, h = body_t);
}

module frame() {
  difference() {
    union() { src(); feet_extension(); boss(); }
    for (dy = [-puck_sq, puck_sq], dz = [-puck_sq, puck_sq])
      translate([0, hub[0] + dy, hub[1] + dz]) rotate([0, 90, 0]) {
        translate([0, 0, -1]) cylinder(d = hole, h = body_t + 2);
        translate([0, 0, -1]) cylinder(d = cb_d, h = puck_cb + 1);
      }
    for (m = mounts) translate([0, m[0], m[1]]) rotate([0, 90, 0]) {
      translate([0, 0, -stack - 1]) cylinder(d = hole, h = stack + body_t + 2);
      translate([0, 0, seat]) cylinder(d = cb_d, h = body_t - seat + 1);
    }
  }
}

if (view == "installed") frame();
else multmatrix([[0, 1, 0, 0], [0, 0, -1, 0], [-1, 0, 0, body_t], [0, 0, 0, 1]]) frame();
