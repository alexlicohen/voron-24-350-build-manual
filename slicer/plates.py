#!/usr/bin/env python3
"""Single source of truth for what goes on each plate: the 20 plates of the ASA run
(B00-B10) and the separate PETG V0 bay-ducting batch B11.

Mirrors `docs/voron-print-plan.md` §3 (per-batch parts tables and the plate
packing lists) and §5.1 (orientation and brim). Every path here was verified to
exist in the pinned repo tree — see `slicer/stl/MANIFEST.sha256`.

A plate's `run` is "asa" unless it says otherwise. Every total the manual prints
for "the run" (20 plates, 157.0 h) is over the "asa" plates only; B11 ("bay") is
added up on its own (slicer/check_docs.py § B11).
"""
from __future__ import annotations

# repo key -> (owner/name, branch, pinned commit resolved 2026-09-05)
REPOS: dict[str, tuple[str, str, str]] = {
    "voron2": ("VoronDesign/Voron-2", "Voron2.4", "a192410e27ea345644ae5c4b29b4c9c40cbe1a73"),
    # Stealthburner r2 / Clockwork 2.5 (released 2026-11-07, pin = PR #154's STL fixes). Alex
    # 2026-11-10: build to 2.5. B06-P1 and B02-P5 print from this pin.
    "sb": ("VoronDesign/Voron-Stealthburner", "main", "1572a42e6df5d2f0ddf04a2145be4dc9c3693723"),
    # The Clockwork 2 pin the B02 plates were printed from before the switch. Only those
    # plates' toolhead parts read it, so their 3MFs and the manifest stay the record of what
    # was printed. bins.PLATE_ASSIGN sends the four superseded parts to 08-superseded.
    "sb_cw2": ("VoronDesign/Voron-Stealthburner", "main", "8bcb9c246fac19d8ac03931ef97fa07c5e5f0f2b"),
    "ldov2": ("MotorDynamicsLab/LDOVoron2", "main", "8270e8cf6c7ba29a7fd11d143c287bd3af576934"),
    "ldotri": ("MotorDynamicsLab/LDOVoronTrident", "master", "5b0496a5ae8d0d6a3f782dfa7e06eb9e1c102ba5"),
    "nitehawk": ("MotorDynamicsLab/Nitehawk-SB", "master", "be93526b948d3339c755cb32116baef221ce1a8d"),
    "nitehawk2": ("MotorDynamicsLab/Nitehawk-SB-V2", "master", "42ae497cfd627acde0f6ad81c8dd26f51efcbb48"),
    "klicky": ("jlas1/Klicky-Probe", "main", "ab86f91d47ac7353a0a7c7e0de26542dca00f63e"),
    "nevermore": ("nevermore3d/Nevermore_Micro", "master", "8740b34fcc88e64afff74115f2c7c7002059f229"),
    "whopping": ("tanaes/whopping_Voron_mods", "main", "62268ed817878e54d6a1186882060aa8368d4f0f"),
}

# B11 bay ducting (layout v3, adopted 2026-09-23). One source folder, slicer/stl/bayducts/,
# holding two kinds of file (slicer/stl/bayducts/README.md has the licence and credit):
#   mss/502306/<file>  MyStoopidStuff's stock pieces, downloaded from Printables by file id
#                      (fetch_stls.py). A re-upload gets a new file id, so the id is the pin
#                      and MANIFEST.sha256 the proof. Gitignored like every other fetched STL.
#   remix/<file>       the layout-v2/v3 remixes for the Rev D+ bay. Nobody else hosts them,
#                      so they are committed; fetch_stls.py only hashes them.
# (repo, path) -> (Printables print id, file id)
PRINTABLES: dict[tuple[str, str], tuple[str, str]] = {
    ("bayducts", "mss/502306/CMD_V3_1H_154mm_DUCT.stl"): ("502306", "5252452"),
    ("bayducts", "mss/502306/CMD_V2_6B_154mm_DUCT_COVER.stl"): ("502306", "4285489"),
    ("bayducts", "mss/502306/CMD_V3_1H_90DEG.stl"): ("502306", "5252443"),
    ("bayducts", "mss/502306/CMD_V2_6B_90DEG_COVER.stl"): ("502306", "4285520"),
    ("bayducts", "mss/502306/CMD_Remix-V3_DUCT-2B_45deg.stl"): ("502306", "5570632"),
    ("bayducts", "mss/502306/CMD_Remix-V3_DUCT-2B_45deg_LID.stl"): ("502306", "5570629"),
    ("bayducts", "mss/502306/CMD_V2_6B_WIRE_BOX_COVER.stl"): ("502306", "4285499"),
    ("bayducts", "mss/502306/CMD_V3_1H_T_SHORT.stl"): ("502306", "5252445"),
    ("bayducts", "mss/502306/CMD_V2_6B_T_SHORT_COVER.stl"): ("502306", "4285575"),
    ("bayducts", "mss/502306/CMD_Remix-V3_DUCT-1M_ENDCAP.stl"): ("502306", "5290452"),
    # Not on a plate: the fallback middle joints (Leviathan->PSU gap < 25 mm) and the
    # parents review/2026-09-23-bay-mods/layout-v3/work/remix_v3.py cuts custom lengths from.
    ("bayducts", "mss/502306/CMD_V3_1H_T_REG.stl"): ("502306", "5252450"),
    ("bayducts", "mss/502306/CMD_V2_6B_T_REG_COVER.stl"): ("502306", "4285522"),
    ("bayducts", "mss/502306/CMD_V3_1H_82mm_DUCT.stl"): ("502306", "5252446"),
    ("bayducts", "mss/502306/CMD_V2_6B_82mm_DUCT_COVER.stl"): ("502306", "4285519"),
    ("bayducts", "mss/502306/CMD_V3_1H_142mm_DUCT.stl"): ("502306", "5252451"),
    ("bayducts", "mss/502306/CMD_V2_6B_142mm_DUCT_COVER.stl"): ("502306", "4285495"),
    ("bayducts", "mss/502306/CMD_V3_1H_WIRE_BOX.stl"): ("502306", "5252449"),
    # Ch 11 Part C add-ons, unchanged authors' files, fetched to slicer/stl/printables/<print id>/:
    # Prusa's Universal Puck and 1 kg spindle (OCL v1), the side mount's tube holder (Maltasrc,
    # CC BY-NC-SA) and HappyCam's 350 body and door (Voxel3D_NL, CC BY-NC).
    ("printables", "1605113/Universal-puck-R1.stl"): ("1605113", "6754814"),
    ("printables", "1605113/Universal-spoolholder-1kg-R1.stl"): ("1605113", "6754815"),
    ("printables", "608769/Bowden Tube Holder_Long.stl"): ("608769", "2569104"),
    ("printables", "488020/HappyCam_main-350.stl"): ("488020", "2101024"),
    ("printables", "488020/Cameradoor_120.stl"): ("488020", "2101022"),
}
# Committed sources: (repo, path prefix). fetch_stls.py hashes them and never downloads.
TRACKED: tuple[tuple[str, str], ...] = (("bayducts", "remix/"), ("addons", "scrubber-796563/"),
                                         ("addons", "side-spool-608769/"))

# Committed files that live outside slicer/stl/: repo key -> folder relative to slicer/stl/.
ROOTS: dict[str, str] = {"addons": "../addons"}

# Pinned but on no plate: the nozzle-scrubber add-on (Ch 13 Part L), printed only after its
# decision step, and the chamber-exhaust add-on (Ch 14 Part H, slicer/addons/exhaust-voron2/),
# the stock Voron housing set at the pinned Voron-2 commit, printed only after Step 14.25, and Ch 11
# Part C's side spool holder (the committed remix in slicer/addons/side-spool-608769/ plus the
# Printables files above) and camera mount, printed after Step 11.68 has measured.
# Listed here so MANIFEST.sha256 pins them. They are not in PLATES, so no plate, estimate or total;
# slicer/bins.py ADDON_PARTS gives them their own bins (11-side-spool, 11-camera, 13-scrubber,
# 14-exhaust) and checks every file it names is in this list. exhaust_filter_grill.stl is already
# pinned through B09-P3.
ADDONS: tuple[tuple[str, str], ...] = (
    ("addons", "scrubber-796563/source/10mm Bed.stp"),
    ("addons", "scrubber-796563/brush_bracket_L1.5_MIRROR.stl"),
    ("addons", "scrubber-796563/bucket350_T1.5_MIRROR.stl"),
    ("addons", "scrubber-796563/stop_bracket.stl"),
    ("voron2", "STLs/Exhaust_Filter/exhaust_filter_housing.stl"),
    ("voron2", "STLs/Exhaust_Filter/[a]_exhaust_fan_grill.stl"),
    ("voron2", "STLs/Exhaust_Filter/[a]_exhaust_filter_mount_x2.stl"),
    ("voron2", "STLs/Exhaust_Filter/[a]_filter_access_cover.stl"),
    ("addons", "side-spool-608769/source/Reel Mount 2_Frame v1.stl"),
    ("addons", "side-spool-608769/side_spool_frame_puck.stl"),
    ("printables", "1605113/Universal-puck-R1.stl"),
    ("printables", "1605113/Universal-spoolholder-1kg-R1.stl"),
    ("printables", "608769/Bowden Tube Holder_Long.stl"),
    ("printables", "488020/HappyCam_main-350.stl"),
    ("printables", "488020/Cameradoor_120.stl"),
)

# Print orientation for files that are not drawn print-ready (MSS keeps the parent's
# frame: duct, box and curve bodies sit base-UP, lids base-down). build_plates.source_stl
# writes a rotated copy under slicer/stl/.oriented/ and packs that; the vendored file stays
# byte-identical to its source. flip = 180 deg about X and ec = +90 deg about Y are the modes
# review/.../layout-v3/work/slice_v3.py sliced with; side = -90 deg about X puts the fin's
# plate face down (1375 mm2 on the bed; slice_v3's +90 stood it on a 95 mm2 edge).
ORIENT: dict[str, str] = {
    **{n: "flip" for n in (
        "CMD_V3_1H_154mm_DUCT.stl", "CMD_V3_1H_90DEG.stl", "CMD_V3_1H_T_SHORT.stl",
        "CMD_V3_1H_T_REG.stl", "CMD_V3_1H_82mm_DUCT.stl", "CMD_V3_1H_142mm_DUCT.stl",
        "V2L_90DEG_MIRROR.stl", "V2L_58mm_DUCT.stl", "V2L_130mm_DUCT.stl",
        "V2L_70mm_DUCT.stl", "V3L_154N_DUCT.stl", "V3L_T_REG_N.stl",
        "V3L_COUPON_22N_DUCT.stl", "V3L_10mm_DUCT.stl", "V3L_34mm_DUCT_HOLE.stl",
        "V3L_90DEG_R15.stl", "V3L_WIRE_BOX_PORT.stl")},
    "CMD_Remix-V3_DUCT-1M_ENDCAP.stl": "ec",
    "V2L_STRIP_FIN.stl": "side",
    # Alex 2026-11-08: drawn standing up; B02-P4's print came out with poor overhangs. ec lays
    # its 731 mm2 flat face down: 21 mm tall, overhang >45 deg 581 -> 237 mm2.
    "XY_cable_chain_bridge-Igus-3mm_backer.stl": "ec",
    # Drawn rim-and-ribs down, so the 1.2 mm panel bridged ~3900 mm2; flip puts the solid face down.
    "Regular_Cartridge_Lid(contributed_by_Bucknova).3mf": "flip",
}

# Per-part brim, from 00-slicer-setup.md § "Orientation & brim".
# 5 mm: tall and narrow.  3 mm: 150-182 mm of flat ASA that lifts at the ends.
BRIM_5MM = {
    "Handle.stl",
    "Latch.stl",
    "Hinge-L-sleeve-2X.stl",
    "Hinge-L-solid-2X.stl",
}
BRIM_3MM = {
    "rear_center_skirt_350.stl",
    "front_skirt_a_350.stl",
    "front_skirt_b_350.stl",
    "side_skirt_a_350_x2.stl",
    "side_skirt_b_350_x2.stl",
    "side_fan_support_x2.STL",
    "keystone_panel.stl",
    "power_inlet_IECGS_1mm.stl",
    "exhaust_cover.stl",
    "V2_Duo_Plenum.stl",
    "Regular_Cartridge(contributed_by_Bucknova).3mf",
    "wago_221-415_mount_3by5.stl",
    "exhaust_filter_grill.stl",
    "cob_light_strip_mount_100mm.stl",
}


BIG_PART_BRIM = 3.0  # every part of BRIM_MIN_MM or more gets at least this (Alex 2026-11-05)
# Alex 2026-11-07: 30 mm (was geom.BIG_PART_MM, 50). On B02-P3, the unbrimmed z_tensioner_9mm
# (36 mm, arms lifted) and z_drive_baseplate_a (44 mm) lifted 37-45 mm from the edges.
BRIM_MIN_MM = 30.0


def brim_for(path: str, footprint: float = 0.0, colour: str = "") -> float:
    """Brim width in mm for one STL: by filename, and at least BIG_PART_BRIM when the
    footprint's longest side (`footprint`, mm) is BRIM_MIN_MM or more. Lift-map 2: unbrimmed
    bars lifted at the corners even 20 mm in; brimmed ones stayed flat. ASA only: the
    "petg" plates (B11) print brimless, as reviewed, since bay-ducts-petg.ini's 0.1 mm
    brim gap fuses PETG (a 0.3 gap already fused on the storage prints)."""
    if colour == "petg":
        return 0.0
    name = path.rsplit("/", 1)[-1]
    if name in BRIM_5MM:
        return 5.0
    if name in BRIM_3MM or footprint >= BRIM_MIN_MM:
        return BIG_PART_BRIM
    return 0.0


def footprint_of(bb) -> float:
    """Longest XY side of a geom.bbox (x0, y0, z0, x1, y1, z1)."""
    return max(bb[3] - bb[0], bb[4] - bb[1])


# Plates already printed from the committed 3MF, before the 25 mm edge rule (2026-11-06) and
# the 30 mm brim rule (2026-11-07). Their 3MFs are the record of what was printed, so
# build_plates.py refuses to re-pack them and audit_plates.py lists their rule breaks
# without failing. Re-slicing them (--from-3mf) stays allowed. A reprint of one of their
# parts goes on its own project, not through here.
AS_PRINTED = frozenset({"B00-P1", "B01-P1", "B02-P1", "B02-P2", "B02-P3"})


# plate_id -> dict(batch, colour, parts=[(repo, path, qty)], note)
PLATES: dict[str, dict] = {
    "B00-P1": dict(
        batch="B00", colour="black",
        note="Calibration gate plate. The z_drive_retainer_a is the 625-2RS press-fit coupon.",
        parts=[
            ("voron2", "STLs/Test_Prints/Voron_Design_Cube_v7.stl", 1),
            ("voron2", "STLs/Test_Prints/Heatset_Practice.stl", 1),
            ("voron2", "STLs/Tools/MGN12_rail_guide_x2.stl", 2),
            ("voron2", "STLs/Tools/MGN9_rail_guide_x2.stl", 2),
            ("voron2", "STLs/Tools/pulley_jig.stl", 1),
            ("voron2", "STLs/Z_Drive/z_drive_retainer_a_x2.stl", 1),
        ]),
    "B01-P1": dict(
        batch="B01", colour="black",
        note="Longest plate in the build - start it in the morning.",
        parts=[
            ("voron2", "STLs/Z_Drive/z_drive_main_a_x2.stl", 2),
            ("voron2", "STLs/Z_Drive/z_drive_main_b_x2.stl", 2),
            ("voron2", "STLs/Z_Drive/z_drive_retainer_a_x2.stl", 1),
            ("voron2", "STLs/Z_Drive/z_drive_retainer_b_x2.stl", 2),
        ]),
    "B01-P2": dict(
        batch="B01", colour="black", note="",
        parts=[
            ("voron2", "STLs/Z_Drive/z_motor_mount_a_x2.stl", 2),
            ("voron2", "STLs/Z_Drive/z_motor_mount_b_x2.stl", 2),
            ("voron2", "STLs/Z_Idlers/z_tensioner_bracket_a_x2.stl", 2),
            ("voron2", "STLs/Z_Idlers/z_tensioner_bracket_b_x2.stl", 2),
            ("voron2", "STLs/Panel_Mounting/deck_support_3mm_x8.stl", 8),
            # Both deck-support sets print (Alex 2026-10-30): the kit-day caliper (00.4) picks one.
            ("voron2", "STLs/Panel_Mounting/deck_support_4mm_x8.stl", 8),
        ]),
    "B02-P1": dict(
        batch="B02", colour="blue",
        note="Faceplate centred, with the door Handle (60 mm tall on a 68x19 footprint - 5 mm brim) and accent parts.",
        parts=[
            ("ldotri", "STLs/BTT Pi TFT4.3 Mount/[a]_faceplate.stl", 1),
            ("voron2", "STLs/Skirts/[a]_fan_grill_b_x2.stl", 1),
            ("whopping", "clickyclacky_door/STLs/Handle.stl", 1),
            ("voron2", "STLs/Z_Drive/[a]_z_drive_baseplate_b_x2.stl", 1),
            ("voron2", "STLs/Skirts/[a]_belt_guard_a_x2.stl", 1),
            ("voron2", "STLs/Skirts/[a]_belt_guard_b_x2.stl", 1),
            ("voron2", "STLs/Gantry/X_Axis/XY_Joints/[a]_endstop_pod_D2F_switch.stl", 1),
            ("voron2", "STLs/Z_Idlers/[a]_z_tensioner_9mm_x4.stl", 2),
            ("voron2", "STLs/Gantry/[a]_z_belt_clip_upper_x4.stl", 1),
            ("voron2", "STLs/Z_Drive/[a]_belt_tensioner_a_x2.stl", 1),
            ("voron2", "STLs/Z_Drive/[a]_belt_tensioner_b_x2.stl", 1),
            ("voron2", "STLs/Gantry/[a]_z_belt_clip_lower_x4.stl", 1),
            ("sb_cw2", "STLs/Clockwork2/Direct_Drive/[a]_guidler_b.stl", 1),
            ("voron2", "STLs/Skirts/[a]_keystone_blank_insert.stl", 1),
            ("voron2", "STLs/Gantry/AB_Drive_Units/[a]_z_chain_retainer_bracket_x2.stl", 1),
        ]),
    "B02-P2": dict(
        batch="B02", colour="blue",
        note="SB main body centred - it has built-in supports, snap them out, do not cut.",
        parts=[
            ("sb_cw2", "STLs/Stealthburner/[a]_stealthburner_main_body.stl", 1),
            ("voron2", "STLs/Skirts/[a]_fan_grill_a_x2.stl", 2),
            ("voron2", "STLs/Z_Drive/[a]_z_drive_baseplate_a_x2.stl", 1),
            ("voron2", "STLs/Z_Drive/[a]_z_drive_baseplate_b_x2.stl", 1),
            ("voron2", "STLs/Skirts/[a]_belt_guard_b_x2.stl", 1),
            ("voron2", "STLs/Gantry/X_Axis/XY_Joints/[a]_xy_joint_cable_bridge_2hole.stl", 1),
            ("voron2", "STLs/Gantry/Front_Idlers/[a]_tensioner_left.stl", 1),
            ("voron2", "STLs/Z_Idlers/[a]_z_tensioner_9mm_x4.stl", 1),
            ("voron2", "STLs/Gantry/[a]_z_belt_clip_upper_x4.stl", 1),
            ("sb_cw2", "STLs/Clockwork2/Direct_Drive/[a]_guidler_a.stl", 1),
            ("voron2", "STLs/Z_Drive/[a]_belt_tensioner_b_x2.stl", 1),
            ("voron2", "STLs/Gantry/[a]_z_belt_clip_lower_x4.stl", 1),
            ("ldov2", "STLs/ldo_bestagon_insert.stl", 1),
            ("sb_cw2", "STLs/Clockwork2/[a]_pcb_spacer.stl", 1),
            ("voron2", "STLs/Gantry/AB_Drive_Units/[a]_z_chain_retainer_bracket_x2.stl", 1),
        ]),
    "B02-P3": dict(
        batch="B02", colour="blue",
        note="Skirt and Z-drive accents: fan grill retainers, a fan grill, a belt guard, a Z drive baseplate, a Z tensioner and a belt tensioner.",
        parts=[
            ("voron2", "STLs/Skirts/[a]_fan_grill_retainer_x2.stl", 2),
            ("voron2", "STLs/Skirts/[a]_fan_grill_b_x2.stl", 1),
            ("voron2", "STLs/Z_Drive/[a]_z_drive_baseplate_a_x2.stl", 1),
            ("voron2", "STLs/Skirts/[a]_belt_guard_a_x2.stl", 1),
            ("voron2", "STLs/Z_Idlers/[a]_z_tensioner_9mm_x4.stl", 1),
            ("voron2", "STLs/Z_Drive/[a]_belt_tensioner_a_x2.stl", 1),
        ]),


    # B02-P4 added 2026-11-06 (Alex): every part 25 mm from every edge no longer fits B02-P3.
    "B02-P4": dict(
        batch="B02", colour="blue",
        note="Gantry and toolhead accents: cable cover, chain-bridge backer, right tensioner, Z belt clips, keystone blank, and the latch with its shuttle.",
        parts=[
            ("voron2", "STLs/Gantry/AB_Drive_Units/[a]_cable_cover.stl", 1),
            ("whopping", "extrusion_backers/STLs/XY_cable_chain_bridge-Igus-3mm_backer.stl", 1),
            ("voron2", "STLs/Gantry/Front_Idlers/[a]_tensioner_right.stl", 1),
            ("sb_cw2", "STLs/Clockwork2/Direct_Drive/[a]_latch.stl", 1),
            ("voron2", "STLs/Gantry/[a]_z_belt_clip_upper_x4.stl", 2),
            ("voron2", "STLs/Gantry/[a]_z_belt_clip_lower_x4.stl", 2),
            ("voron2", "STLs/Skirts/[a]_keystone_blank_insert.stl", 1),
            ("sb_cw2", "STLs/Clockwork2/Direct_Drive/[a]_latch_shuttle.stl", 1),
        ]),
    # B02-P5 added 2026-11-10 (Alex): catch-up plate for the Clockwork 2.5 / Stealthburner r2
    # switch. These four replace the Clockwork 2 copies already printed on B02-P1, P2 and P4
    # (bin 08-superseded). The latch shuttle and PCB spacer did not change shape and are kept.
    "B02-P5": dict(
        batch="B02", colour="blue",
        note="Clockwork 2.5 catch-up: the r2 Stealthburner body centred, both guidler halves and the latch.",
        parts=[
            ("sb", "STLs/Stealthburner/[a]_stealthburner_main_body.stl", 1),
            ("sb", "STLs/Clockwork2.5/Direct_Drive/[a]_guidler_a.stl", 1),
            ("sb", "STLs/Clockwork2.5/Direct_Drive/[a]_guidler_b.stl", 1),
            ("sb", "STLs/Clockwork2.5/Direct_Drive/[a]_latch.stl", 1),
        ]),
    "B03-P1": dict(
        batch="B03", colour="black",
        note="The A side: the A drive frame and the right front idler, upper and lower.",
        parts=[
            ("voron2", "STLs/Gantry/AB_Drive_Units/a_drive_frame_lower.stl", 1),
            ("voron2", "STLs/Gantry/AB_Drive_Units/a_drive_frame_upper.stl", 1),
            ("voron2", "STLs/Gantry/Front_Idlers/front_idler_right_lower.stl", 1),
            ("voron2", "STLs/Gantry/Front_Idlers/front_idler_right_upper.stl", 1),
        ]),
    # B03-P2 added 2026-11-05 (Alex): with a brim on every big part, both sides no longer fit one plate.
    "B03-P2": dict(
        batch="B03", colour="black",
        note="The B side: the B drive frame and the left front idler, upper and lower.",
        parts=[
            ("voron2", "STLs/Gantry/AB_Drive_Units/b_drive_frame_lower.stl", 1),
            ("voron2", "STLs/Gantry/AB_Drive_Units/b_drive_frame_upper.stl", 1),
            ("voron2", "STLs/Gantry/Front_Idlers/front_idler_left_lower.stl", 1),
            ("voron2", "STLs/Gantry/Front_Idlers/front_idler_left_upper.stl", 1),
        ]),
    "B04-P1": dict(
        batch="B04", colour="black", note="",
        parts=[
            ("voron2", "STLs/Gantry/X_Axis/XY_Joints/xy_joint_left_lower_MGN12.stl", 1),
            ("voron2", "STLs/Gantry/X_Axis/XY_Joints/xy_joint_left_upper_MGN12.stl", 1),
            ("voron2", "STLs/Gantry/X_Axis/XY_Joints/xy_joint_right_lower_MGN12.stl", 1),
            ("voron2", "STLs/Gantry/X_Axis/XY_Joints/xy_joint_right_upper_MGN12.stl", 1),
            ("voron2", "STLs/Gantry/X_Axis/X_Carriage/x_frame_V2TR_MGN12_left.stl", 1),
            ("voron2", "STLs/Gantry/X_Axis/X_Carriage/x_frame_V2TR_MGN12_right.stl", 1),
            ("voron2", "STLs/Gantry/X_Axis/X_Carriage/probe_retainer_bracket.stl", 1),
        ]),
    "B05-P1": dict(
        batch="B05", colour="black", note="",
        parts=[
            ("voron2", "STLs/Gantry/Z_Joints/z_joint_lower_x4.stl", 4),
            ("voron2", "STLs/Gantry/Z_Joints/z_joint_upper_x4.stl", 4),
            ("voron2", "STLs/Gantry/z_chain_bottom_anchor.stl", 1),
            ("voron2", "STLs/Gantry/z_chain_guide.stl", 1),
            ("ldov2", "STLs/z_rail_stop_x4.stl", 4),
        ]),
    "B06-P1": dict(
        batch="B06", colour="black",
        note="Stealthburner r2 and Clockwork 2.5 black parts. The stock cable_cover fits the Nitehawk-SB V2.",
        parts=[
            ("sb", "STLs/Stealthburner/Printheads/revo_voron/stealthburner_printhead_revo_voron_front.stl", 1),
            ("sb", "STLs/Stealthburner/Printheads/revo_voron/stealthburner_printhead_revo_voron_rear_cw2.stl", 1),
            ("sb", "STLs/Stealthburner/[o]_stealthburner_LED_carrier.stl", 1),
            ("sb", "STLs/Stealthburner/[o]_stealthburner_LED_diffuser_mask.stl", 1),
            ("sb", "STLs/Clockwork2.5/Direct_Drive/main_body_collet.stl", 1),
            ("sb", "STLs/Clockwork2.5/Direct_Drive/motor_plate.stl", 1),
            ("sb", "STLs/Clockwork2.5/cable_cover.stl", 1),
        ]),


    # B06-P2 added 2026-11-06 (Alex): every part 25 mm from every edge no longer fits B06-P1.
    "B06-P2": dict(
        batch="B06", colour="black",
        note="The whole Klicky set: probes, dock, mounts and press-fit helpers.",
        parts=[
            ("klicky", "Probes/KlickyProbe/STL/KlickyProbe_v2.stl", 2),
            ("klicky", "Probes/KlickyProbe/STL/Probe_Dock_v2.1.stl", 1),
            ("klicky", "Probes/KlickyProbe/STL/Probe_magnet_holder.stl", 1),
            ("klicky", "Probes/KlickyProbe/STL/Probe_magnet_pressfit_helper.stl", 1),
            ("klicky", "Probes/KlickyProbe/STL/Probe_pressfit_holder.stl", 1),
            ("klicky", "Printers/Voron/v1.8_v2.4_Legacy_Trident/v1.8_v2.4_Legacy_Trident_STL/KlickyProbe_AB_mount_v2.stl", 1),
            ("klicky", "Printers/Voron/v1.8_v2.4_Legacy_Trident/v1.8_v2.4_Legacy_Trident_STL/KlickyProbe_AB_mount_v2_holder.stl", 1),
            ("klicky", "Printers/Voron/v1.8_v2.4_Legacy_Trident/v1.8_v2.4_Legacy_Trident_STL/Mount_magnet_holder.stl", 1),
            ("klicky", "Printers/Voron/v1.8_v2.4_Legacy_Trident/v1.8_v2.4_Legacy_Trident_STL/Mount_magnet_pressfit_helper.stl", 1),
            ("klicky", "Printers/Voron/v1.8_v2.4_Legacy_Trident/v1.8_v2.4_Legacy_Trident_STL/Mount_pressfit_holder_v2.stl", 1),
            ("klicky", "Printers/Voron/v1.8_v2.4_Legacy_Trident/v1.8_v2.4_Legacy_Trident_STL/Dock_mount_fixed_v2.stl", 1),
        ]),
    "B07-P1": dict(
        batch="B07", colour="black",
        note="Power inlet and WAGO mount (3 mm brims), two 100 mm COB light-strip mounts, bay hardware.",
        parts=[
            ("voron2", "STLs/Skirts/power_inlet_IECGS_1mm.stl", 1),
            ("ldov2", "STLs/COB Light Strip/cob_light_strip_mount_100mm.stl", 2),
            ("voron2", "STLs/Electronics_Bay/wago_221-415_mount_3by5.stl", 1),
            ("voron2", "STLs/Electronics_Bay/pcb_din_clip_x3.stl", 1),
            ("ldov2", "STLs/handlebar_spacer_x4.stl", 2),
        ]),
    "B07-P2": dict(
        batch="B07", colour="black",
        note="Four 100 mm COB light-strip mounts, brimmed, with a DIN clip and two handlebar spacers.",
        parts=[
            ("ldov2", "STLs/COB Light Strip/cob_light_strip_mount_100mm.stl", 4),
            ("voron2", "STLs/Electronics_Bay/pcb_din_clip_x3.stl", 1),
            ("ldov2", "STLs/handlebar_spacer_x4.stl", 2),
        ]),
    # B07-P3 added 2026-11-03 (Alex): big parts 20 mm from every edge no longer fit B07 on two plates.
    "B07-P3": dict(
        batch="B07", colour="black",
        note="The USB adapter mount and its cover, the LRS-200 PSU brackets, the PSU stabiliser, both 50 mm COB mounts and a DIN clip.",
        parts=[
            ("nitehawk", "STLs/usb_adapter_mount.stl", 1),
            ("nitehawk2", "STLs/usb_adapter_mount_partial_cover.stl", 1),
            ("ldov2", "STLs/COB Light Strip/cob_light_strip_mount_50mm.stl", 2),
            ("voron2", "STLs/Electronics_Bay/PSU_stabilizer_50mm.stl", 1),
            ("voron2", "STLs/Electronics_Bay/lrs_200_psu_bracket_x2.stl", 2),
            ("voron2", "STLs/Electronics_Bay/pcb_din_clip_x3.stl", 1),
        ]),
    "B08-P1": dict(
        batch="B08", colour="black",
        note="",
        parts=[
            ("voron2", "STLs/Skirts/350/rear_center_skirt_350.stl", 1),
            ("voron2", "STLs/Skirts/350/side_skirt_a_350_x2.stl", 1),
        ]),
    "B08-P2": dict(
        batch="B08", colour="black",
        note="A side fan support and one side_skirt_b.",
        parts=[
            ("voron2", "STLs/Skirts/side_fan_support_x2.STL", 1),
            ("voron2", "STLs/Skirts/350/side_skirt_b_350_x2.stl", 1),
        ]),
    "B08-P3": dict(
        batch="B08", colour="black",
        note="A side fan support and a side_skirt_a.",
        parts=[
            ("voron2", "STLs/Skirts/side_fan_support_x2.STL", 1),
            ("voron2", "STLs/Skirts/350/side_skirt_a_350_x2.stl", 1),
        ]),
    "B08-P4": dict(
        batch="B08", colour="black",
        note="The whole front of the ring: both front skirts.",
        parts=[
            ("voron2", "STLs/Skirts/350/front_skirt_b_350.stl", 1),
            ("voron2", "STLs/Skirts/350/front_skirt_a_350.stl", 1),
        ]),
    # B08-P5 added 2026-11-03 (Alex): big parts 20 mm from every edge no longer fit B08 on four plates.
    "B08-P5": dict(
        batch="B08", colour="black",
        note="The second side_skirt_b, the keystone panel and the TFT mount.",
        parts=[
            ("voron2", "STLs/Skirts/350/side_skirt_b_350_x2.stl", 1),
            ("voron2", "STLs/Skirts/keystone_panel.stl", 1),
            ("ldotri", "STLs/BTT Pi TFT4.3 Mount/mount.stl", 1),
        ]),
    # B09 was five plates until 2026-10-23, then merged into three (each bin whole on one plate,
    # hours balanced) from the committed projects with platearrange.merge_3mf, arranged at 6 mm.
    "B09-P1": dict(
        batch="B09", colour="black",
        note="Exhaust cover centred, with panel clips and a bottom-panel hinge.",
        parts=[
            ("ldov2", "STLs/exhaust_cover.stl", 1),
            ("voron2", "STLs/Panel_Mounting/bottom_panel_hinge_x2.stl", 1),
            # 2 since 2026-11-07: one moved from B09-P3, which no longer fits with 30 mm-rule brims
            ("voron2", "STLs/Panel_Mounting/bottom_panel_clip_x4.stl", 2),
            ("voron2", "STLs/Panel_Mounting/corner_panel_clip_4mm_x8.stl", 2),
            ("voron2", "STLs/Panel_Mounting/corner_panel_clip_6mm_x8.stl", 2),
            ("voron2", "STLs/Panel_Mounting/midspan_panel_clip_4mm_x7.stl", 2),
            ("voron2", "STLs/Panel_Mounting/midspan_panel_clip_6mm_x8.stl", 2),
        ]),
    "B09-P2": dict(
        batch="B09", colour="black",
        note="Nevermore Regular_Cartridge centred (built-in support to push out) and panel clips.",
        parts=[
            ("nevermore", "V5_Duo/V2/Regular_Cartridge(contributed_by_Bucknova).3mf", 1),
            ("voron2", "STLs/Panel_Mounting/bottom_panel_clip_x4.stl", 1),
            ("voron2", "STLs/Panel_Mounting/corner_panel_clip_4mm_x8.stl", 2),
            ("voron2", "STLs/Panel_Mounting/corner_panel_clip_6mm_x8.stl", 2),
            ("voron2", "STLs/Panel_Mounting/midspan_panel_clip_4mm_x7.stl", 2),
            ("voron2", "STLs/Panel_Mounting/midspan_panel_clip_6mm_x8.stl", 2),
        ]),
    "B09-P3": dict(
        batch="B09", colour="black",
        note="Nevermore V2_Duo_Plenum centred (built-in support to push out), cartridge lid, a bottom-panel hinge and 4 mm panel clips.",
        parts=[
            ("nevermore", "V5_Duo/V2/V2_Duo_Plenum.stl", 1),
            ("nevermore", "V5_Duo/V2/Regular_Cartridge_Lid(contributed_by_Bucknova).3mf", 1),
            ("voron2", "STLs/Panel_Mounting/bottom_panel_hinge_x2.stl", 1),
            ("voron2", "STLs/Panel_Mounting/corner_panel_clip_4mm_x8.stl", 2),
            ("voron2", "STLs/Panel_Mounting/midspan_panel_clip_4mm_x7.stl", 2),
        ]),
    "B09-P4": dict(
        batch="B09", colour="black",
        note="Nevermore plenum lid centred, exhaust grill and panel clips.",
        parts=[
            ("nevermore", "V5_Duo/V2/V2_Duo_Plenum_LID.stl", 1),
            ("voron2", "STLs/Exhaust_Filter/exhaust_filter_grill.stl", 1),
            ("voron2", "STLs/Panel_Mounting/bottom_panel_clip_x4.stl", 1),
            ("voron2", "STLs/Panel_Mounting/corner_panel_clip_4mm_x8.stl", 2),
            ("voron2", "STLs/Panel_Mounting/corner_panel_clip_6mm_x8.stl", 2),
            ("voron2", "STLs/Panel_Mounting/midspan_panel_clip_4mm_x7.stl", 1),
            ("voron2", "STLs/Panel_Mounting/midspan_panel_clip_6mm_x8.stl", 2),
        ]),


    # B09-P5 added 2026-11-06 (Alex): every part 25 mm from every edge no longer fits B09 on four plates.
    "B09-P5": dict(
        batch="B09", colour="black",
        note="All four Z belt covers, spool holder, bowden retainer and 6 mm panel clips.",
        parts=[
            ("voron2", "STLs/Panel_Mounting/z_belt_cover_a_x2.stl", 2),
            ("voron2", "STLs/Spool_Management/spool_holder.stl", 1),
            ("voron2", "STLs/Panel_Mounting/z_belt_cover_b_x2.stl", 2),
            ("voron2", "STLs/Spool_Management/bowden_retainer.stl", 1),
            ("voron2", "STLs/Panel_Mounting/corner_panel_clip_6mm_x8.stl", 2),
            ("voron2", "STLs/Panel_Mounting/midspan_panel_clip_6mm_x8.stl", 2),
        ]),
    "B10-P1": dict(
        batch="B10", colour="black",
        note="Hinge-L parts are mirrored in the slicer if you want the door to swing the other way.",
        parts=[
            ("whopping", "clickyclacky_door/STLs/Handle-Hinge_Bottom.stl", 1),
            ("whopping", "clickyclacky_door/STLs/Handle-Hinge_Top.stl", 1),
            ("whopping", "clickyclacky_door/STLs/Hinge-L-sleeve-2X.stl", 2),
            ("whopping", "clickyclacky_door/STLs/Hinge-L-solid-2X.stl", 2),
            ("whopping", "clickyclacky_door/STLs/Latch.stl", 1),
            ("whopping", "clickyclacky_door/STLs/Panel_Clip.stl", 1),
        ]),
    # ---- B11: bay ducting, layout v3 (PETG V0, outside the ASA run) ----------------------
    # group "before-kit": needs no bench measurement. group "after-kit": custom lengths and
    # the narrowed middle run, printed once the kit-day measurements are in (B11 page).
    # Packed by nest.py; Alex passed the arrangements as packed at the Step B00.8 review (2026-11-02).
    # qc="pending" marks a plate whose arrangement has not been reviewed (none now). The ten re-packed
    # 2026-11-03 for the big-part 20 mm edge rule passed Alex's GUI review as packed the same day.
    # 2026-11-06: P2, P3, P5 re-packed and P6, P7 added for the 25 mm rule; P1 and P4 already met it.
    "B11-P1": dict(
        batch="B11", colour="petg", run="bay", group="before-kit",
        note="Test coupon: prints first, alone. The lid must snap and hold before P5 is printed.",
        parts=[
            ("bayducts", "remix/V3L_COUPON_22N_DUCT.stl", 1),
            ("bayducts", "remix/V3L_COUPON_22N_DUCT_COVER.stl", 1),
        ]),
    "B11-P2": dict(
        batch="B11", colour="petg", run="bay", group="before-kit",
        note="DC conduit's front run: the two stock 154s.",
        parts=[
            ("bayducts", "mss/502306/CMD_V3_1H_154mm_DUCT.stl", 2),
            ("bayducts", "mss/502306/CMD_V2_6B_154mm_DUCT_COVER.stl", 2),
        ]),
    "B11-P3": dict(
        batch="B11", colour="petg", run="bay", group="before-kit",
        note="AC conduit: wire box, R15 curves, SSR T, endcaps, strip fin.",
        parts=[
            ("bayducts", "remix/V3L_WIRE_BOX_PORT.stl", 1),
            ("bayducts", "mss/502306/CMD_V2_6B_WIRE_BOX_COVER.stl", 1),
            ("bayducts", "remix/V3L_90DEG_R15.stl", 2),
            ("bayducts", "remix/V3L_90DEG_R15_COVER.stl", 2),
            ("bayducts", "mss/502306/CMD_V3_1H_T_SHORT.stl", 1),
            ("bayducts", "mss/502306/CMD_V2_6B_T_SHORT_COVER.stl", 1),
            ("bayducts", "mss/502306/CMD_Remix-V3_DUCT-1M_ENDCAP.stl", 2),
            ("bayducts", "remix/V2L_STRIP_FIN.stl", 1),
        ]),
    "B11-P4": dict(
        batch="B11", colour="petg", run="bay", group="after-kit",
        note="Custom lengths: regenerate any piece whose bench gap differs before slicing.",
        parts=[
            ("bayducts", "remix/V2L_58mm_DUCT.stl", 3),
            ("bayducts", "remix/V2L_58mm_DUCT_COVER.stl", 3),
            ("bayducts", "remix/V2L_130mm_DUCT.stl", 1),
            ("bayducts", "remix/V2L_130mm_DUCT_COVER.stl", 1),
            ("bayducts", "remix/V2L_70mm_DUCT.stl", 1),
            ("bayducts", "remix/V2L_70mm_DUCT_COVER.stl", 1),
            ("bayducts", "remix/V3L_10mm_DUCT.stl", 3),
            ("bayducts", "remix/V3L_10mm_DUCT_COVER.stl", 3),
            ("bayducts", "remix/V3L_34mm_DUCT_HOLE.stl", 1),
            ("bayducts", "remix/V3L_34mm_DUCT_COVER.stl", 1),
        ]),
    "B11-P5": dict(
        batch="B11", colour="petg", run="bay", group="after-kit",
        note="Narrowed middle run, straights: only if the Leviathan-to-PSU gap is 25 mm or more.",
        parts=[
            ("bayducts", "remix/V3L_154N_DUCT.stl", 2),
            ("bayducts", "remix/V3L_154N_DUCT_COVER.stl", 2),
        ]),
    # B11-P6 and P7 added 2026-11-06 (Alex): every part 25 mm from every edge no longer fits.
    # P6 takes P2's corners and P3's DC S-jog; P7 takes P5's narrowed Ts.
    "B11-P6": dict(
        batch="B11", colour="petg", run="bay", group="before-kit",
        note="DC conduit: the three 90 deg corners and the 45 deg S-jog.",
        parts=[
            ("bayducts", "mss/502306/CMD_V3_1H_90DEG.stl", 2),
            ("bayducts", "mss/502306/CMD_V2_6B_90DEG_COVER.stl", 2),
            ("bayducts", "remix/V2L_90DEG_MIRROR.stl", 1),
            ("bayducts", "remix/V2L_90DEG_COVER_MIRROR.stl", 1),
            ("bayducts", "mss/502306/CMD_Remix-V3_DUCT-2B_45deg.stl", 2),
            ("bayducts", "mss/502306/CMD_Remix-V3_DUCT-2B_45deg_LID.stl", 2),
        ]),
    "B11-P7": dict(
        batch="B11", colour="petg", run="bay", group="after-kit",
        note="Narrowed middle run, Ts: only if the Leviathan-to-PSU gap is 25 mm or more.",
        parts=[
            ("bayducts", "remix/V3L_T_REG_N.stl", 2),
            ("bayducts", "remix/V3L_T_REG_N_COVER.stl", 2),
        ]),
}

# Previous throughput-model estimates from docs/voron-print-plan.md §9, kept so
# estimates.csv can show the delta against the numbers they replace.
MODEL_ESTIMATE: dict[str, tuple[float, int]] = {
    "B00-P1": (3.5, 57), "B01-P1": (12.7, 216), "B01-P2": (6.7, 108),
    "B02-P1": (5.9, 100), "B02-P2": (6.1, 102), "B02-P3": (6.5, 106),
    "B03-P1": (7.7, 130), "B04-P1": (7.3, 122),
    "B05-P1": (5.2, 83), "B06-P1": (9.8, 162),
    "B07-P1": (5.7, 96), "B07-P2": (7.5, 127),
    "B08-P1": (6.1, 105), "B08-P2": (7.0, 120), "B08-P3": (8.0, 136),
    "B08-P4": (4.4, 76),
    "B10-P1": (5.1, 80),
    # B09: the model sized five plates (19.1 h, 322 g); none of them survives the 2026-10-23
    # merge, so the three B09 plates have no model figure and the TOTAL row no model delta.
}


def all_sources() -> list[tuple[str, str]]:
    """Every (repo_key, path) referenced by any plate, plus the Printables files kept
    for B11's fallback and regeneration path and the add-on files in ADDONS, deduplicated.
    Only fetch_stls.py reads this; plate, bin and total code reads PLATES."""
    seen: dict[tuple[str, str], None] = {}
    for plate in PLATES.values():
        for repo, path, _qty in plate["parts"]:
            seen[(repo, path)] = None
    for key in PRINTABLES:
        seen[key] = None
    for key in ADDONS:
        seen[key] = None
    return sorted(seen)


def run_of(plate_id: str) -> str:
    """"asa" for the 20-plate run, "bay" for B11."""
    return PLATES[plate_id].get("run", "asa")


def local_path(repo: str, path: str) -> str:
    """Where fetch_stls.py finds or puts one source file, relative to slicer/stl/."""
    return f"{ROOTS.get(repo, repo)}/{path}"
