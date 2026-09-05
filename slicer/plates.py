#!/usr/bin/env python3
"""Single source of truth for what goes on each of the 27 plates.

Mirrors `docs/voron-print-plan.md` §3 (per-batch parts tables and the plate
packing lists) and §5.1 (orientation and brim). Every path here was verified to
exist in the pinned repo tree — see `slicer/stl/MANIFEST.sha256`.
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
        batch="B02", colour="orange",
        note="SB main body has built-in supports - snap them out, do not cut.",
        parts=[
            ("sb", "STLs/Stealthburner/[a]_stealthburner_main_body.stl", 1),
            ("ldotri", "STLs/BTT Pi TFT4.3 Mount/[a]_faceplate.stl", 1),
            ("voron2", "STLs/Gantry/AB_Drive_Units/[a]_cable_cover.stl", 1),
            ("voron2", "STLs/Z_Drive/[a]_z_drive_baseplate_a_x2.stl", 2),
            ("voron2", "STLs/Z_Drive/[a]_z_drive_baseplate_b_x2.stl", 2),
        ]),
    "B02-P2": dict(
        batch="B02", colour="orange",
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
        batch="B02", colour="orange",
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
        batch="B03", colour="black", note="The A side.",
        parts=[
            ("voron2", "STLs/Gantry/AB_Drive_Units/a_drive_frame_lower.stl", 1),
            ("voron2", "STLs/Gantry/AB_Drive_Units/a_drive_frame_upper.stl", 1),
            ("voron2", "STLs/Gantry/Front_Idlers/front_idler_right_lower.stl", 1),
            ("voron2", "STLs/Gantry/Front_Idlers/front_idler_right_upper.stl", 1),
        ]),
    "B03-P2": dict(
        batch="B03", colour="black", note="The B side.",
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
        batch="B06", colour="black", note="Stealthburner + Clockwork 2 black parts.",
        parts=[
            ("sb", "STLs/Stealthburner/Printheads/revo_voron/stealthburner_printhead_revo_voron_front.stl", 1),
            ("sb", "STLs/Stealthburner/Printheads/revo_voron/stealthburner_printhead_revo_voron_rear_cw2.stl", 1),
            ("sb", "STLs/Stealthburner/[o]_stealthburner_LED_carrier.stl", 1),
            ("sb", "STLs/Stealthburner/[o]_stealthburner_LED_diffuser_mask.stl", 1),
            ("sb", "STLs/Clockwork2/Direct_Drive/main_body.stl", 1),
            ("sb", "STLs/Clockwork2/Direct_Drive/motor_plate.stl", 1),
            ("nitehawk", "STLs/cw2_captive_pcb_cover.stl", 1),
        ]),
    "B06-P2": dict(
        batch="B06", colour="black", note="The whole Klicky set.",
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
        batch="B07", colour="black", note="",
        parts=[
            ("voron2", "STLs/Electronics_Bay/wago_221-415_mount_3by5.stl", 1),
            ("voron2", "STLs/Electronics_Bay/lrs_200_psu_bracket_x2.stl", 2),
            ("voron2", "STLs/Electronics_Bay/PSU_stabilizer_50mm.stl", 1),
            ("nitehawk", "STLs/usb_adapter_mount.stl", 1),
            ("nitehawk2", "STLs/usb_adapter_mount_partial_cover.stl", 1),
            ("voron2", "STLs/Electronics_Bay/pcb_din_clip_x3.stl", 3),
            ("ldov2", "STLs/handlebar_spacer_x4.stl", 4),
        ]),
    "B07-P2": dict(
        batch="B07", colour="black", note="The eight COB light-strip mounts, brimmed.",
        parts=[
            ("ldov2", "STLs/COB Light Strip/cob_light_strip_mount_100mm.stl", 6),
            ("ldov2", "STLs/COB Light Strip/cob_light_strip_mount_50mm.stl", 2),
        ]),
    "B07-P3": dict(
        batch="B07", colour="black", note="power_inlet_IECGS_1mm alone, 3 mm brim.",
        parts=[
            ("voron2", "STLs/Skirts/power_inlet_IECGS_1mm.stl", 1),
        ]),
    "B08-P1": dict(
        batch="B08", colour="black", note="",
        parts=[
            ("voron2", "STLs/Skirts/350/rear_center_skirt_350.stl", 1),
            ("voron2", "STLs/Skirts/side_fan_support_x2.STL", 1),
        ]),
    "B08-P2": dict(
        batch="B08", colour="black", note="",
        parts=[
            ("voron2", "STLs/Skirts/side_fan_support_x2.STL", 1),
            ("voron2", "STLs/Skirts/350/front_skirt_a_350.stl", 1),
        ]),
    "B08-P3": dict(
        batch="B08", colour="black", note="",
        parts=[
            ("voron2", "STLs/Skirts/350/front_skirt_b_350.stl", 1),
            ("voron2", "STLs/Skirts/350/side_skirt_a_350_x2.stl", 1),
        ]),
    "B08-P4": dict(
        batch="B08", colour="black", note="",
        parts=[
            ("voron2", "STLs/Skirts/350/side_skirt_a_350_x2.stl", 1),
            ("voron2", "STLs/Skirts/350/side_skirt_b_350_x2.stl", 1),
        ]),
    "B08-P5": dict(
        batch="B08", colour="black", note="",
        parts=[
            ("voron2", "STLs/Skirts/350/side_skirt_b_350_x2.stl", 1),
            ("voron2", "STLs/Skirts/keystone_panel.stl", 1),
        ]),
    "B08-P6": dict(
        batch="B08", colour="black", note="TFT mount; power inlet moved to B07-P3.",
        parts=[
            ("ldotri", "STLs/BTT Pi TFT4.3 Mount/mount.stl", 1),
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
}

# Previous throughput-model estimates from docs/voron-print-plan.md §9, kept so
# estimates.csv can show the delta against the numbers they replace.
MODEL_ESTIMATE: dict[str, tuple[float, int]] = {
    "B00-P1": (3.5, 57), "B01-P1": (12.7, 216), "B01-P2": (6.7, 108),
    "B02-P1": (5.9, 100), "B02-P2": (6.1, 102), "B02-P3": (6.5, 106),
    "B03-P1": (3.9, 66), "B03-P2": (3.8, 64), "B04-P1": (7.3, 122),
    "B05-P1": (5.2, 83), "B06-P1": (6.3, 106), "B06-P2": (3.5, 56),
    "B07-P1": (3.6, 60), "B07-P2": (7.5, 127), "B07-P3": (2.1, 36),
    "B08-P1": (6.1, 105), "B08-P2": (4.3, 74), "B08-P3": (4.6, 78),
    "B08-P4": (4.3, 74), "B08-P5": (4.4, 76), "B08-P6": (1.8, 30),
    "B09-P1": (4.1, 71), "B09-P2": (4.3, 73), "B09-P3": (3.5, 60),
    "B09-P4": (3.6, 59), "B09-P5": (3.6, 59), "B10-P1": (5.1, 80),
}


def all_sources() -> list[tuple[str, str]]:
    """Every (repo_key, path) referenced by any plate, deduplicated."""
    seen: dict[tuple[str, str], None] = {}
    for plate in PLATES.values():
        for repo, path, _qty in plate["parts"]:
            seen[(repo, path)] = None
    return sorted(seen)


def local_path(repo: str, path: str) -> str:
    """Where fetch_stls.py puts one source file, relative to slicer/stl/."""
    return f"{repo}/{path}"
