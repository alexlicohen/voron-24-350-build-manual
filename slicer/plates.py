#!/usr/bin/env python3
"""Single source of truth for what goes on each plate: the 22 plates of the ASA run
(B00-B10) and the separate PETG V0 bay-ducting batch B11.

Mirrors `docs/voron-print-plan.md` §3 (per-batch parts tables and the plate
packing lists) and §5.1 (orientation and brim). Every path here was verified to
exist in the pinned repo tree — see `slicer/stl/MANIFEST.sha256`.

A plate's `run` is "asa" unless it says otherwise. Every total the manual prints
for "the run" (22 plates, 157.0 h) is over the "asa" plates only; B11 ("bay") is
added up on its own (slicer/check_docs.py § B11).
"""
from __future__ import annotations

# repo key -> (owner/name, branch, pinned commit resolved 2026-09-05)
REPOS: dict[str, tuple[str, str, str]] = {
    "voron2": ("VoronDesign/Voron-2", "Voron2.4", "a192410e27ea345644ae5c4b29b4c9c40cbe1a73"),
    "sb": ("VoronDesign/Voron-Stealthburner", "main", "8bcb9c246fac19d8ac03931ef97fa07c5e5f0f2b"),
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
}
# Committed sources: (repo, path prefix). fetch_stls.py hashes them and never downloads.
TRACKED: tuple[tuple[str, str], ...] = (("bayducts", "remix/"),)

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


def brim_for(path: str) -> float:
    """Brim width in mm for one STL, by filename."""
    name = path.rsplit("/", 1)[-1]
    if name in BRIM_5MM:
        return 5.0
    if name in BRIM_3MM:
        return 3.0
    return 0.0


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
        ]),
    "B02-P1": dict(
        batch="B02", colour="blue",
        note="SB main body has built-in supports - snap them out, do not cut.",
        parts=[
            ("sb", "STLs/Stealthburner/[a]_stealthburner_main_body.stl", 1),
            ("ldotri", "STLs/BTT Pi TFT4.3 Mount/[a]_faceplate.stl", 1),
            ("voron2", "STLs/Gantry/AB_Drive_Units/[a]_cable_cover.stl", 1),
            ("voron2", "STLs/Z_Drive/[a]_z_drive_baseplate_a_x2.stl", 2),
            ("voron2", "STLs/Z_Drive/[a]_z_drive_baseplate_b_x2.stl", 2),
        ]),
    "B02-P2": dict(
        batch="B02", colour="blue",
        note="Handle is 60 mm tall on a 68x19 footprint - 5 mm brim.",
        parts=[
            ("whopping", "clickyclacky_door/STLs/Handle.stl", 1),
            ("voron2", "STLs/Skirts/[a]_fan_grill_a_x2.stl", 2),
            ("voron2", "STLs/Skirts/[a]_fan_grill_b_x2.stl", 2),
            ("voron2", "STLs/Skirts/[a]_fan_grill_retainer_x2.stl", 2),
            ("voron2", "STLs/Skirts/[a]_belt_guard_a_x2.stl", 2),
            ("voron2", "STLs/Skirts/[a]_belt_guard_b_x2.stl", 2),
            ("voron2", "STLs/Gantry/Front_Idlers/[a]_tensioner_left.stl", 1),
            ("voron2", "STLs/Gantry/Front_Idlers/[a]_tensioner_right.stl", 1),
        ]),
    "B02-P3": dict(
        batch="B02", colour="blue",
        note="The 29 small accent parts.",
        parts=[
            ("voron2", "STLs/Z_Drive/[a]_belt_tensioner_a_x2.stl", 2),
            ("voron2", "STLs/Z_Drive/[a]_belt_tensioner_b_x2.stl", 2),
            ("voron2", "STLs/Z_Idlers/[a]_z_tensioner_9mm_x4.stl", 4),
            ("voron2", "STLs/Gantry/AB_Drive_Units/[a]_z_chain_retainer_bracket_x2.stl", 2),
            ("voron2", "STLs/Gantry/X_Axis/XY_Joints/[a]_endstop_pod_D2F_switch.stl", 1),
            ("voron2", "STLs/Gantry/X_Axis/XY_Joints/[a]_xy_joint_cable_bridge_2hole.stl", 1),
            ("whopping", "extrusion_backers/STLs/XY_cable_chain_bridge-Igus-3mm_backer.stl", 1),
            ("voron2", "STLs/Gantry/[a]_z_belt_clip_lower_x4.stl", 4),
            ("voron2", "STLs/Gantry/[a]_z_belt_clip_upper_x4.stl", 4),
            ("sb", "STLs/Clockwork2/Direct_Drive/[a]_guidler_a.stl", 1),
            ("sb", "STLs/Clockwork2/Direct_Drive/[a]_guidler_b.stl", 1),
            ("sb", "STLs/Clockwork2/Direct_Drive/[a]_latch.stl", 1),
            ("sb", "STLs/Clockwork2/Direct_Drive/[a]_latch_shuttle.stl", 1),
            ("sb", "STLs/Clockwork2/[a]_pcb_spacer.stl", 1),
            ("voron2", "STLs/Skirts/[a]_keystone_blank_insert.stl", 2),
            ("ldov2", "STLs/ldo_bestagon_insert.stl", 1),
        ]),
    "B03-P1": dict(
        batch="B03", colour="black",
        note="Both sides on one plate: A parts left of the legend numbers, B parts right.",
        parts=[
            ("voron2", "STLs/Gantry/AB_Drive_Units/a_drive_frame_lower.stl", 1),
            ("voron2", "STLs/Gantry/AB_Drive_Units/a_drive_frame_upper.stl", 1),
            ("voron2", "STLs/Gantry/Front_Idlers/front_idler_right_lower.stl", 1),
            ("voron2", "STLs/Gantry/Front_Idlers/front_idler_right_upper.stl", 1),
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
        note="Stealthburner + Clockwork 2 black parts and the whole Klicky set on one plate.",
        parts=[
            ("sb", "STLs/Stealthburner/Printheads/revo_voron/stealthburner_printhead_revo_voron_front.stl", 1),
            ("sb", "STLs/Stealthburner/Printheads/revo_voron/stealthburner_printhead_revo_voron_rear_cw2.stl", 1),
            ("sb", "STLs/Stealthburner/[o]_stealthburner_LED_carrier.stl", 1),
            ("sb", "STLs/Stealthburner/[o]_stealthburner_LED_diffuser_mask.stl", 1),
            ("sb", "STLs/Clockwork2/Direct_Drive/main_body.stl", 1),
            ("sb", "STLs/Clockwork2/Direct_Drive/motor_plate.stl", 1),
            ("nitehawk", "STLs/cw2_captive_pcb_cover.stl", 1),
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
        note="Bay hardware plus power_inlet_IECGS_1mm, 3 mm brim on the inlet and the WAGO mount.",
        parts=[
            ("voron2", "STLs/Electronics_Bay/wago_221-415_mount_3by5.stl", 1),
            ("voron2", "STLs/Electronics_Bay/lrs_200_psu_bracket_x2.stl", 2),
            ("voron2", "STLs/Electronics_Bay/PSU_stabilizer_50mm.stl", 1),
            ("nitehawk", "STLs/usb_adapter_mount.stl", 1),
            ("nitehawk2", "STLs/usb_adapter_mount_partial_cover.stl", 1),
            ("voron2", "STLs/Electronics_Bay/pcb_din_clip_x3.stl", 3),
            ("ldov2", "STLs/handlebar_spacer_x4.stl", 4),
            ("voron2", "STLs/Skirts/power_inlet_IECGS_1mm.stl", 1),
        ]),
    "B07-P2": dict(
        batch="B07", colour="black", note="The eight COB light-strip mounts, brimmed.",
        parts=[
            ("ldov2", "STLs/COB Light Strip/cob_light_strip_mount_100mm.stl", 6),
            ("ldov2", "STLs/COB Light Strip/cob_light_strip_mount_50mm.stl", 2),
        ]),
    "B08-P1": dict(
        batch="B08", colour="black", note="",
        parts=[
            ("voron2", "STLs/Skirts/350/rear_center_skirt_350.stl", 1),
            ("voron2", "STLs/Skirts/side_fan_support_x2.STL", 1),
        ]),
    "B08-P2": dict(
        batch="B08", colour="black", note="The whole front of the ring plus one side skirt.",
        parts=[
            ("voron2", "STLs/Skirts/350/front_skirt_a_350.stl", 1),
            ("voron2", "STLs/Skirts/350/front_skirt_b_350.stl", 1),
            ("voron2", "STLs/Skirts/350/side_skirt_a_350_x2.stl", 1),
        ]),
    "B08-P3": dict(
        batch="B08", colour="black",
        note="The TFT mount rides with the second fan support and two side skirts.",
        parts=[
            ("voron2", "STLs/Skirts/side_fan_support_x2.STL", 1),
            ("voron2", "STLs/Skirts/350/side_skirt_a_350_x2.stl", 1),
            ("voron2", "STLs/Skirts/350/side_skirt_b_350_x2.stl", 1),
            ("ldotri", "STLs/BTT Pi TFT4.3 Mount/mount.stl", 1),
        ]),
    "B08-P4": dict(
        batch="B08", colour="black", note="",
        parts=[
            ("voron2", "STLs/Skirts/350/side_skirt_b_350_x2.stl", 1),
            ("voron2", "STLs/Skirts/keystone_panel.stl", 1),
        ]),
    "B09-P1": dict(
        batch="B09", colour="black", note="V2_Duo_Plenum has a built-in support to push out.",
        parts=[
            ("nevermore", "V5_Duo/V2/V2_Duo_Plenum.stl", 1),
            ("nevermore", "V5_Duo/V2/V2_Duo_Plenum_LID.stl", 1),
            ("nevermore", "V5_Duo/V2/Regular_Cartridge_Lid(contributed_by_Bucknova).3mf", 1),
        ]),
    "B09-P2": dict(
        batch="B09", colour="black", note="Regular_Cartridge has a built-in support to push out.",
        parts=[
            ("nevermore", "V5_Duo/V2/Regular_Cartridge(contributed_by_Bucknova).3mf", 1),
            ("ldov2", "STLs/exhaust_cover.stl", 1),
        ]),
    "B09-P3": dict(
        batch="B09", colour="black", note="",
        parts=[
            ("voron2", "STLs/Exhaust_Filter/exhaust_filter_grill.stl", 1),
            ("voron2", "STLs/Spool_Management/spool_holder.stl", 1),
            ("voron2", "STLs/Spool_Management/bowden_retainer.stl", 1),
            ("voron2", "STLs/Panel_Mounting/z_belt_cover_a_x2.stl", 2),
            ("voron2", "STLs/Panel_Mounting/z_belt_cover_b_x2.stl", 2),
        ]),
    "B09-P4": dict(
        batch="B09", colour="black", note="4 mm panel clips.",
        parts=[
            ("voron2", "STLs/Panel_Mounting/corner_panel_clip_4mm_x8.stl", 8),
            ("voron2", "STLs/Panel_Mounting/midspan_panel_clip_4mm_x7.stl", 7),
            ("voron2", "STLs/Panel_Mounting/bottom_panel_hinge_x2.stl", 2),
            ("voron2", "STLs/Panel_Mounting/bottom_panel_clip_x4.stl", 4),
        ]),
    "B09-P5": dict(
        batch="B09", colour="black", note="6 mm panel clips.",
        parts=[
            ("voron2", "STLs/Panel_Mounting/corner_panel_clip_6mm_x8.stl", 8),
            ("voron2", "STLs/Panel_Mounting/midspan_panel_clip_6mm_x8.stl", 8),
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
    # qc="pending": packed by nest.py, not yet opened, arranged and re-saved in the GUI.
    # Once Alex has done that, delete the key and run build_plates.py --from-3mf B11-Pn.
    "B11-P1": dict(
        batch="B11", colour="petg", run="bay", group="before-kit", qc="pending",
        note="Test coupon: prints first, alone. The lid must snap and hold before P5 is printed.",
        parts=[
            ("bayducts", "remix/V3L_COUPON_22N_DUCT.stl", 1),
            ("bayducts", "remix/V3L_COUPON_22N_DUCT_COVER.stl", 1),
        ]),
    "B11-P2": dict(
        batch="B11", colour="petg", run="bay", group="before-kit", qc="pending",
        note="DC conduit: the two stock 154s and the three 90 deg corners.",
        parts=[
            ("bayducts", "mss/502306/CMD_V3_1H_154mm_DUCT.stl", 2),
            ("bayducts", "mss/502306/CMD_V2_6B_154mm_DUCT_COVER.stl", 2),
            ("bayducts", "mss/502306/CMD_V3_1H_90DEG.stl", 2),
            ("bayducts", "mss/502306/CMD_V2_6B_90DEG_COVER.stl", 2),
            ("bayducts", "remix/V2L_90DEG_MIRROR.stl", 1),
            ("bayducts", "remix/V2L_90DEG_COVER_MIRROR.stl", 1),
        ]),
    "B11-P3": dict(
        batch="B11", colour="petg", run="bay", group="before-kit", qc="pending",
        note="AC conduit (wire box, R15 curves, SSR T, endcaps, strip fin) plus the DC S-jog.",
        parts=[
            ("bayducts", "remix/V3L_WIRE_BOX_PORT.stl", 1),
            ("bayducts", "mss/502306/CMD_V2_6B_WIRE_BOX_COVER.stl", 1),
            ("bayducts", "remix/V3L_90DEG_R15.stl", 2),
            ("bayducts", "remix/V3L_90DEG_R15_COVER.stl", 2),
            ("bayducts", "mss/502306/CMD_V3_1H_T_SHORT.stl", 1),
            ("bayducts", "mss/502306/CMD_V2_6B_T_SHORT_COVER.stl", 1),
            ("bayducts", "mss/502306/CMD_Remix-V3_DUCT-1M_ENDCAP.stl", 2),
            ("bayducts", "remix/V2L_STRIP_FIN.stl", 1),
            ("bayducts", "mss/502306/CMD_Remix-V3_DUCT-2B_45deg.stl", 2),
            ("bayducts", "mss/502306/CMD_Remix-V3_DUCT-2B_45deg_LID.stl", 2),
        ]),
    "B11-P4": dict(
        batch="B11", colour="petg", run="bay", group="after-kit", qc="pending",
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
        batch="B11", colour="petg", run="bay", group="after-kit", qc="pending",
        note="Narrowed middle run: only if the Leviathan-to-PSU gap is 25 mm or more.",
        parts=[
            ("bayducts", "remix/V3L_154N_DUCT.stl", 2),
            ("bayducts", "remix/V3L_154N_DUCT_COVER.stl", 2),
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
    "B09-P1": (4.1, 71), "B09-P2": (4.3, 73), "B09-P3": (3.5, 60),
    "B09-P4": (3.6, 59), "B09-P5": (3.6, 59), "B10-P1": (5.1, 80),
}


def all_sources() -> list[tuple[str, str]]:
    """Every (repo_key, path) referenced by any plate, plus the Printables files kept
    for B11's fallback and regeneration path, deduplicated."""
    seen: dict[tuple[str, str], None] = {}
    for plate in PLATES.values():
        for repo, path, _qty in plate["parts"]:
            seen[(repo, path)] = None
    for key in PRINTABLES:
        seen[key] = None
    return sorted(seen)


def run_of(plate_id: str) -> str:
    """"asa" for the 22-plate run, "bay" for B11."""
    return PLATES[plate_id].get("run", "asa")


def local_path(repo: str, path: str) -> str:
    """Where fetch_stls.py puts one source file, relative to slicer/stl/."""
    return f"{repo}/{path}"
