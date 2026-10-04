#!/usr/bin/env python3
"""Bin scheme: which sorting bin every printed part goes into once it is off the plate.

One bin per consuming assembly chapter, sub-bins where a chapter is part-heavy
(the four Z corners, the A/B drive sides, the 4 mm / 6 mm panel clips ...).
This is the single source for:

  * scripts/render_plate_bins.py  - the per-plate sorting diagrams (colour + bin id on every part)
  * scripts/build_printables.py   - the printable bin labels and the bin map
  * docs/manual/assets/parts/MANIFEST.csv `bin` column (written by render_plate_bins.py --write-manifest)
  * docs/manual/print/README.md § Bins (hand-maintained; slicer/check_docs.py cross-checks it,
    the `bag` column included)

Two bins hold add-on parts that are on no plate (13-scrubber, 14-exhaust): ADDON_PARTS lists them,
so they reach the labels and the bag sizing but never a plate, a diagram, an estimate or a total.
FALLBACK_PARTS (B11's stock middle joints, printed only instead of B11-P5) and BOUGHT_PARTS (the
add-ons' bought fan, lead, mat and wipers) reach the labels and the bag sizing the same way and count
toward no piece total.

A bin is keyed to the step that opens it: one bin holds the parts first needed at one point in the
build, a step or one run of steps in a chapter (or in a chapter part that other work separates
from the rest, as Ch 13 separates Ch 11 Part A from Part B). Parts staged early and carried along
(05.45, 05.46, 06.26) and jigs that are taken out and returned (00-jigs) do not open a bin twice.

Every bin also names the bag (or box) its parts travel in: `bag`, decided from the STL geometry by
slicer/bin_bags.py (`--check` re-derives it and fails on drift). BAGS is the stock of mesh zip bags.

Consumers were derived from the assembly chapters' Printed-parts tables and the steps that name each
STL (docs/manual/NN-*.md). Corner map for the Z parts is Ch 02 Step 02.02: `_a` parts build Z0
(front-left) and Z2 (rear-right), `_b` parts build Z1 (rear-left) and Z3 (front-right).
"""
from __future__ import annotations

import re

# ------------------------------------------------------------------ the bags
# Mesh zip bags in the bag stock. `owned`: 24 A5 and 12 B5 on hand 2026-10-04, plus one more pack of
# 24 A5 to buy for the bins split by opening step (Ch 00 Step 00.11 says so); the bags come in packs
# of 24 A5 and 12 B5. `flat` is the usable flat inside, taken as the paper size the bag is sold for; BAG_THICK is the usable thickness at that flat size (an assumption:
# a filled mesh pouch is about an inch deep before it starts to steal width). slicer/bin_bags.py
# owns the fit rule; a bin's `bag` is "A5", "B5", "A5 ×2" ... or "box".
BAGS: dict[str, dict] = {
    "A5": dict(flat=(148.0, 210.0), owned=48, on_hand=24),
    "B5": dict(flat=(176.0, 250.0), owned=12, on_hand=12),
}
BAG_THICK = 25.0

# ------------------------------------------------------------------ the bins
# id -> (label, chapter, steps, colour)
#   label   : what to write on the bin
#   chapter : "Ch NN" the bin is opened for (the chapter whose steps fit the parts)
#   steps   : step range(s) in that chapter; secondary uses in parentheses
#   colour  : fill on the plate diagrams and labels (hex); consistent across every plate
#   bag     : added from BAG below (the mesh bag or box the bin travels in)
BINS: dict[str, dict[str, str]] = {
    "00-jigs": dict(
        label="Jigs and coupons",
        chapter="Ch 00", steps="00.14–00.22 (rail guides again at 02.06, 05.11, 05.33; pulley jig at 02.18, 04.24, 04.33; cube at 14.11)",
        colour="#8a8f98"),
    "02-Z0": dict(label="Z0 corner (front-left, `_a` hand)", chapter="Ch 02", steps="02.01–02.44 (drive 02.17–02.38, idler 02.39–02.43)", colour="#2457c5"),
    "02-Z1": dict(label="Z1 corner (rear-left, `_b` hand)", chapter="Ch 02", steps="02.01–02.44 (drive 02.17–02.38, idler 02.39–02.43)", colour="#1a9c8c"),
    "02-Z2": dict(label="Z2 corner (rear-right, `_a` hand)", chapter="Ch 02", steps="02.01–02.44 (drive 02.17–02.38, idler 02.39–02.43)", colour="#7b4fc4"),
    "02-Z3": dict(label="Z3 corner (front-right, `_b` hand)", chapter="Ch 02", steps="02.01–02.44 (drive 02.17–02.38, idler 02.39–02.43)", colour="#3fa9e0"),
    "02-deck": dict(label="Deck panel clips", chapter="Ch 02", steps="02.11–02.15 (confirm thickness at 02.12)", colour="#7f95c9"),
    "04-A": dict(label="A drive unit + A (right) front idler", chapter="Ch 04", steps="04.1–04.24 (A idler 04.6–04.9, A drive 04.20–04.24)", colour="#2e8b57"),
    "04-B": dict(label="B drive unit + B (left) front idler", chapter="Ch 04", steps="04.1–04.33 (B idler 04.13–04.16, B drive 04.29–04.33)", colour="#8fbc4a"),
    "05-XY": dict(label="XY joints, endstop pod, upper Z belt clips", chapter="Ch 05",
                  steps="05.3–05.38 (upper Z belt clips 05.19–05.23; endstop pod bagged at 05.46, fitted at 09.32–09.33)",
                  colour="#c2185b"),
    "06-Z-joints": dict(label="Z joints and lower Z belt clips", chapter="Ch 06", steps="06.3–06.9", colour="#a0522d"),
    "07-X": dict(label="X carriage halves, probe bracket, cable cover", chapter="Ch 07", steps="07.6–07.39 (staged at 05.45; probe 07.35; cover 07.39)", colour="#cd853f"),
    "08-SB": dict(label="Stealthburner body, printhead, LEDs", chapter="Ch 08", steps="08.2–08.62 (printhead 08.28–08.30, LEDs 08.35–08.37, body 08.62)", colour="#d62839"),
    "08-CW2": dict(label="Clockwork 2 extruder, toolboard + USB covers", chapter="Ch 08",
                   steps="08.3–08.20 (toolboard cover 08.51, USB adapter cover 08.64)", colour="#f28482"),
    "09-bay": dict(label="Electronics bay: inlet, WAGO, PSU, DIN clips", chapter="Ch 09", steps="09.7–09.16 (inlet 09.10–09.12, WAGO 09.13, PSU 09.15–09.16)", colour="#e0a100"),
    # B11 bay ducting: one bin per step that opens it. Bodies are laid in Ch 09, lids closed later.
    "09-ducts-DC": dict(label="DC conduit + coupon, B11", chapter="Ch 09",
                        steps="09.6 (dry-laid at B11.10, stuck down at 09.36; coupon tested at B11.4 and B11.10)",
                        colour="#9c6a12"),
    "09-ducts-AC": dict(label="AC conduit, B11", chapter="Ch 09",
                        steps="09.36 (dry-laid at B11.10)", colour="#b4501a"),
    "10-chains": dict(label="Z cable chain anchor, guide, retainer", chapter="Ch 10", steps="10.35, 10.62–10.64 (bagged with the chain at 06.26; inserts 10.35)", colour="#6b8e23"),
    "10-lights": dict(label="COB light-strip mounts", chapter="Ch 10", steps="10.35–10.36", colour="#b8b62c"),
    "10-tft": dict(label="Touchscreen faceplate + mount", chapter="Ch 10", steps="10.50 (builds the module: Ch 11 Steps 11.5–11.6)", colour="#4f6d7a"),
    "10-lids-AC": dict(label="AC lids + strip fin, B11", chapter="Ch 10", steps="10.80", colour="#3d5a80"),
    "11-skirts": dict(label="Skirt ring, keystone panel and inserts", chapter="Ch 11", steps="11.1–11.19 (keystone 11.10, bestagon 11.19)", colour="#5c6b73"),
    "11-fans": dict(label="Fan grills, retainers, belt guards", chapter="Ch 11", steps="11.3, 11.9, 11.11, 11.16", colour="#9aa5ad"),
    "11-panels": dict(label="Bottom-panel clips/hinges, Z belt covers", chapter="Ch 11", steps="11.20–11.25", colour="#8d6e63"),
    "11-lids-DC": dict(label="DC lids, B11", chapter="Ch 11", steps="11.52", colour="#d4a373"),
    "11-clips-4mm": dict(label="Panel clips, 4 mm (back + top panels)", chapter="Ch 11", steps="11.53, 11.59", colour="#a1887f"),
    "11-finish": dict(label="Exhaust cover + grill, handlebar spacers", chapter="Ch 11", steps="11.54, 11.60", colour="#7a6a53"),
    "11-clips-6mm": dict(label="Panel clips, 6 mm (side panels)", chapter="Ch 11", steps="11.57–11.58", colour="#6d4c41"),
    "11-nevermore": dict(label="Nevermore plenum + cartridge", chapter="Ch 11", steps="11.26–11.40", colour="#00695c"),
    "11-spool": dict(label="Spool holder + bowden retainer", chapter="Ch 11", steps="11.42–11.43", colour="#78909c"),
    "11-door": dict(label="Clicky-Clack door", chapter="Ch 11", steps="11.44–11.50, 11.62–11.64", colour="#ff7043"),
    # Add-on bins: their parts are on no plate (ADDON_PARTS below), printed after kit day.
    "13-scrubber": dict(label="Nozzle scrubber add-on: brackets + bucket", chapter="Ch 13",
                        steps="13.44–13.54, Part L (printed 13.48, fitted 13.49–13.50)", colour="#b5838d"),
    "14-exhaust": dict(label="Chamber exhaust add-on: housing, grill, cover, mounts", chapter="Ch 14",
                       steps="14.25–14.36, Part H (printed 14.26, built 14.27–14.29)", colour="#264653"),
    "spare-alt": dict(label="Spares / alternates (not fitted)", chapter="—", steps="not fitted (Klicky set bagged at 08.54)", colour="#bdbdbd"),
}

# Bag per bin, from `python3 slicer/bin_bags.py` (the why is in its table and in print/README § Bins).
BAG: dict[str, str] = {
    "00-jigs": "A5", "02-Z0": "A5", "02-Z1": "A5", "02-Z2": "A5", "02-Z3": "A5",
    "02-deck": "A5", "04-A": "A5", "04-B": "A5", "05-XY": "B5", "06-Z-joints": "A5",
    "07-X": "A5", "08-SB": "B5", "08-CW2": "A5", "10-tft": "B5", "11-finish": "A5", "09-bay": "A5", "09-ducts-DC": "A5 ×3",
    "09-ducts-AC": "A5", "10-chains": "A5", "10-lights": "A5", "10-lids-AC": "A5", "11-skirts": "box",
    "11-fans": "A5", "11-panels": "A5", "11-lids-DC": "A5", "11-clips-4mm": "A5", "11-clips-6mm": "A5",
    "11-nevermore": "B5", "11-spool": "A5", "11-door": "A5", "13-scrubber": "A5",
    "14-exhaust": "B5 ×2", "spare-alt": "A5",
}
for _b, _meta in BINS.items():
    _meta["bag"] = BAG[_b]


def bag_parse(bag: str) -> tuple[str, int]:
    """"A5" -> ("A5", 1); "B5 ×2" -> ("B5", 2); "box" -> ("box", 1)."""
    m = re.fullmatch(r"(A5|B5|box)(?: ×(\d+))?", bag)
    if not m:
        raise ValueError(f"bad bag {bag!r}: want A5, B5, box, optionally ' ×N'")
    return m.group(1), int(m.group(2) or 1)


def bag_counts() -> dict[str, int]:
    """{"A5": n, "B5": n, "box": n} over every bin."""
    out = {"A5": 0, "B5": 0, "box": 0}
    for meta in BINS.values():
        kind, n = bag_parse(meta["bag"])
        out[kind] += n
    return out


def bag_text(bag: str) -> str:
    """Display form: "A5 mesh bag", "2 × B5 mesh bags", "box (too big for a bag)"."""
    kind, n = bag_parse(bag)
    if kind == "box":
        return "box, too big for a bag"
    return f"{kind} mesh bag" if n == 1 else f"{n} × {kind} mesh bags"


def bag_summary() -> str:
    """The phrase every page quotes, e.g. "24 of 24 A5 and 7 of 12 B5 mesh bags, plus 1 box"
    (no parentheses: Ch 00 puts it in a Do line). slicer/check_docs.py requires it in print/README
    and Ch 00 and fails on any other A5/B5/box count in the pages that state one."""
    c = bag_counts()
    return (f"{c['A5']} of {BAGS['A5']['owned']} A5 and {c['B5']} of {BAGS['B5']['owned']} B5 "
            f"mesh bags, plus {c['box']} box{'es' if c['box'] != 1 else ''}")


# ------------------------------------------------------ STL -> bin assignment
# One entry per STL in slicer/plates.py. A list means one bin per printed copy, in the
# order the copies appear on the plate (object name suffix #1, #2 ...); a copy beyond the
# list length cycles. PLATE_ASSIGN overrides per plate for an STL split across plates.
_A = ["02-Z0", "02-Z2"]     # `_a` hand: one copy to each `_a` corner
_B = ["02-Z1", "02-Z3"]     # `_b` hand
_ALL_Z = ["02-Z0", "02-Z1", "02-Z2", "02-Z3"]

ASSIGN: dict[str, str | list[str]] = {
    # B00
    "Voron_Design_Cube_v7.stl": "00-jigs",
    "Heatset_Practice.stl": "00-jigs",
    "MGN12_rail_guide_x2.stl": "00-jigs",
    "MGN9_rail_guide_x2.stl": "00-jigs",
    "pulley_jig.stl": "00-jigs",
    "z_drive_retainer_a_x2.stl": _A,          # B00 copy -> Z0, B01 copy -> Z2 (PLATE_ASSIGN)
    # B01
    "z_drive_main_a_x2.stl": _A,
    "z_drive_main_b_x2.stl": _B,
    "z_drive_retainer_b_x2.stl": _B,
    "z_motor_mount_a_x2.stl": _A,
    "z_motor_mount_b_x2.stl": _B,
    "z_tensioner_bracket_a_x2.stl": _A,
    "z_tensioner_bracket_b_x2.stl": _B,
    "deck_support_3mm_x8.stl": "02-deck",
    # B02 (accent)
    "[a]_stealthburner_main_body.stl": "08-SB",
    "[a]_faceplate.stl": "10-tft",
    "[a]_cable_cover.stl": "07-X",
    "[a]_z_drive_baseplate_a_x2.stl": _A,
    "[a]_z_drive_baseplate_b_x2.stl": _B,
    "Handle.stl": "11-door",
    "[a]_fan_grill_a_x2.stl": "11-fans",
    "[a]_fan_grill_b_x2.stl": "11-fans",
    "[a]_fan_grill_retainer_x2.stl": "11-fans",
    "[a]_belt_guard_a_x2.stl": "11-fans",
    "[a]_belt_guard_b_x2.stl": "11-fans",
    "[a]_tensioner_left.stl": "04-B",
    "[a]_tensioner_right.stl": "04-A",
    "[a]_belt_tensioner_a_x2.stl": _A,
    "[a]_belt_tensioner_b_x2.stl": _B,
    "[a]_z_tensioner_9mm_x4.stl": _ALL_Z,
    "[a]_z_chain_retainer_bracket_x2.stl": "10-chains",
    "[a]_endstop_pod_D2F_switch.stl": "05-XY",
    "[a]_xy_joint_cable_bridge_2hole.stl": "05-XY",
    "XY_cable_chain_bridge-Igus-3mm_backer.stl": "05-XY",
    "[a]_z_belt_clip_lower_x4.stl": "06-Z-joints",
    "[a]_z_belt_clip_upper_x4.stl": "05-XY",
    "[a]_guidler_a.stl": "08-CW2",
    "[a]_guidler_b.stl": "08-CW2",
    "[a]_latch.stl": "08-CW2",
    "[a]_latch_shuttle.stl": "08-CW2",
    "[a]_pcb_spacer.stl": "spare-alt",
    "[a]_keystone_blank_insert.stl": "11-skirts",
    "ldo_bestagon_insert.stl": "11-skirts",
    # B03
    "a_drive_frame_lower.stl": "04-A",
    "a_drive_frame_upper.stl": "04-A",
    "front_idler_right_lower.stl": "04-A",
    "front_idler_right_upper.stl": "04-A",
    "b_drive_frame_lower.stl": "04-B",
    "b_drive_frame_upper.stl": "04-B",
    "front_idler_left_lower.stl": "04-B",
    "front_idler_left_upper.stl": "04-B",
    # B04
    "xy_joint_left_lower_MGN12.stl": "05-XY",
    "xy_joint_left_upper_MGN12.stl": "05-XY",
    "xy_joint_right_lower_MGN12.stl": "05-XY",
    "xy_joint_right_upper_MGN12.stl": "05-XY",
    "x_frame_V2TR_MGN12_left.stl": "07-X",
    "x_frame_V2TR_MGN12_right.stl": "07-X",
    "probe_retainer_bracket.stl": "07-X",
    # B05
    "z_joint_lower_x4.stl": "06-Z-joints",
    "z_joint_upper_x4.stl": "06-Z-joints",
    "z_chain_bottom_anchor.stl": "10-chains",
    "z_chain_guide.stl": "10-chains",
    "z_rail_stop_x4.stl": _ALL_Z,
    # B06
    "stealthburner_printhead_revo_voron_front.stl": "08-SB",
    "stealthburner_printhead_revo_voron_rear_cw2.stl": "08-SB",
    "[o]_stealthburner_LED_carrier.stl": "08-SB",
    "[o]_stealthburner_LED_diffuser_mask.stl": "08-SB",
    "main_body.stl": "08-CW2",
    "motor_plate.stl": "08-CW2",
    "cw2_captive_pcb_cover.stl": "08-CW2",
    "KlickyProbe_v2.stl": "spare-alt",
    "Probe_Dock_v2.1.stl": "spare-alt",
    "Probe_magnet_holder.stl": "spare-alt",
    "Probe_magnet_pressfit_helper.stl": "spare-alt",
    "Probe_pressfit_holder.stl": "spare-alt",
    "KlickyProbe_AB_mount_v2.stl": "spare-alt",
    "KlickyProbe_AB_mount_v2_holder.stl": "spare-alt",
    "Mount_magnet_holder.stl": "spare-alt",
    "Mount_magnet_pressfit_helper.stl": "spare-alt",
    "Mount_pressfit_holder_v2.stl": "spare-alt",
    "Dock_mount_fixed_v2.stl": "spare-alt",
    # B07
    "wago_221-415_mount_3by5.stl": "09-bay",
    "lrs_200_psu_bracket_x2.stl": "09-bay",
    "PSU_stabilizer_50mm.stl": "09-bay",
    "usb_adapter_mount.stl": "spare-alt",
    "usb_adapter_mount_partial_cover.stl": "08-CW2",
    "pcb_din_clip_x3.stl": "09-bay",
    "handlebar_spacer_x4.stl": "11-finish",
    "cob_light_strip_mount_100mm.stl": "10-lights",
    "cob_light_strip_mount_50mm.stl": "10-lights",
    "power_inlet_IECGS_1mm.stl": "09-bay",
    # B08
    "rear_center_skirt_350.stl": "11-skirts",
    "side_fan_support_x2.STL": "11-skirts",
    "front_skirt_a_350.stl": "11-skirts",
    "front_skirt_b_350.stl": "11-skirts",
    "side_skirt_a_350_x2.stl": "11-skirts",
    "side_skirt_b_350_x2.stl": "11-skirts",
    "keystone_panel.stl": "11-skirts",
    "mount.stl": "10-tft",
    # B09
    "V2_Duo_Plenum.stl": "11-nevermore",
    "V2_Duo_Plenum_LID.stl": "11-nevermore",
    "Regular_Cartridge_Lid(contributed_by_Bucknova).3mf": "11-nevermore",
    "Regular_Cartridge(contributed_by_Bucknova).3mf": "11-nevermore",
    "exhaust_cover.stl": "11-finish",
    "exhaust_filter_grill.stl": "11-finish",
    "spool_holder.stl": "11-spool",
    "bowden_retainer.stl": "11-spool",
    "z_belt_cover_a_x2.stl": "11-panels",
    "z_belt_cover_b_x2.stl": "11-panels",
    "corner_panel_clip_4mm_x8.stl": "11-clips-4mm",
    "midspan_panel_clip_4mm_x7.stl": "11-clips-4mm",
    "bottom_panel_hinge_x2.stl": "11-panels",
    "bottom_panel_clip_x4.stl": "11-panels",
    "corner_panel_clip_6mm_x8.stl": "11-clips-6mm",
    "midspan_panel_clip_6mm_x8.stl": "11-clips-6mm",
    # B10
    "Handle-Hinge_Bottom.stl": "11-door",
    "Handle-Hinge_Top.stl": "11-door",
    "Hinge-L-sleeve-2X.stl": "11-door",
    "Hinge-L-solid-2X.stl": "11-door",
    "Latch.stl": "11-door",
    "Panel_Clip.stl": "11-door",
    # B11 (bay ducting, PETG V0): bodies by conduit (laid at 09.6 / 09.36), lids by the step that
    # closes them (AC 10.80 with the strip fin, DC 11.52). The 10 mm straight and its cover serve
    # both conduits: copy 1 is the DC rear-upper run, copies 2-3 the SSR run's right end and the
    # box-port stub. A B11.11 regeneration that drops a copy keeps copy 1 DC.
    "V3L_COUPON_22N_DUCT.stl": "09-ducts-DC",
    "V3L_COUPON_22N_DUCT_COVER.stl": "09-ducts-DC",
    "CMD_V3_1H_154mm_DUCT.stl": "09-ducts-DC",
    "CMD_V2_6B_154mm_DUCT_COVER.stl": "11-lids-DC",
    "CMD_V3_1H_90DEG.stl": "09-ducts-DC",
    "CMD_V2_6B_90DEG_COVER.stl": "11-lids-DC",
    "V2L_90DEG_MIRROR.stl": "09-ducts-DC",
    "V2L_90DEG_COVER_MIRROR.stl": "11-lids-DC",
    "CMD_Remix-V3_DUCT-2B_45deg.stl": "09-ducts-DC",
    "CMD_Remix-V3_DUCT-2B_45deg_LID.stl": "11-lids-DC",
    "V3L_WIRE_BOX_PORT.stl": "09-ducts-AC",
    "CMD_V2_6B_WIRE_BOX_COVER.stl": "10-lids-AC",
    "V3L_90DEG_R15.stl": "09-ducts-AC",
    "V3L_90DEG_R15_COVER.stl": "10-lids-AC",
    "CMD_V3_1H_T_SHORT.stl": "09-ducts-AC",
    "CMD_V2_6B_T_SHORT_COVER.stl": "10-lids-AC",
    "CMD_Remix-V3_DUCT-1M_ENDCAP.stl": "09-ducts-AC",
    "V2L_STRIP_FIN.stl": "10-lids-AC",
    "V2L_58mm_DUCT.stl": "09-ducts-DC",
    "V2L_58mm_DUCT_COVER.stl": "11-lids-DC",
    "V2L_130mm_DUCT.stl": "09-ducts-DC",
    "V2L_130mm_DUCT_COVER.stl": "11-lids-DC",
    "V2L_70mm_DUCT.stl": "09-ducts-DC",
    "V2L_70mm_DUCT_COVER.stl": "11-lids-DC",
    "V3L_10mm_DUCT.stl": ["09-ducts-DC", "09-ducts-AC", "09-ducts-AC"],
    "V3L_10mm_DUCT_COVER.stl": ["11-lids-DC", "10-lids-AC", "10-lids-AC"],
    "V3L_34mm_DUCT_HOLE.stl": "09-ducts-AC",
    "V3L_34mm_DUCT_COVER.stl": "10-lids-AC",
    "V3L_154N_DUCT.stl": "09-ducts-DC",
    "V3L_154N_DUCT_COVER.stl": "11-lids-DC",
    "V3L_T_REG_N.stl": "09-ducts-DC",
    "V3L_T_REG_N_COVER.stl": "11-lids-DC",
}

PLATE_ASSIGN: dict[tuple[str, str], list[str]] = {
    ("B00-P1", "z_drive_retainer_a_x2.stl"): ["02-Z0"],
    ("B01-P1", "z_drive_retainer_a_x2.stl"): ["02-Z2"],
}

# Per-part notes that belong on the label / sort table (not on the diagram).
NOTES: dict[str, str] = {
    "Voron_Design_Cube_v7.stl": "reference coupon — keep for re-passing Gate A at the INDX + Gen 2 rebuild and 14.11",
    "Heatset_Practice.stl": "Gate B coupon (7 inserts, Step B00.7)",
    "MGN12_rail_guide_x2.stl": "one is the Gate B coupon (Step B00.7)",
    "z_drive_retainer_a_x2.stl": "B00 copy is the Gate B bore coupon",
    "deck_support_3mm_x8.stl": "reprint `deck_support_4mm_x8` if the deck panel calipers 4 mm (02.12)",
    "XY_cable_chain_bridge-Igus-3mm_backer.stl": "alternate to `[a]_xy_joint_cable_bridge_2hole` — fit whichever clears the backer (05.3)",
    "[a]_endstop_pod_D2F_switch.stl": "bagged with its screws at 05.46, fitted at 09.32–09.33",
    "[a]_z_belt_clip_upper_x4.stl": "fitted at 05.19–05.23 under the idler and drive tops",
    "usb_adapter_mount_partial_cover.stl": "closes the USB adapter stack at 08.64, bagged for Ch 09",
    "mount.stl": "TFT module built at 10.50 (Ch 11 Steps 11.5–11.6)",
    "[a]_z_chain_retainer_bracket_x2.stl": "1 fitted, 1 spare (verify on bench)",
    "[a]_keystone_blank_insert.stl": "1 used, 1 spare",
    "ldo_bestagon_insert.stl": "optional trim (11.19)",
    "[a]_pcb_spacer.stl": "kit supplies one printed — this is the spare",
    "usb_adapter_mount.stl": "LDO supplies one printed — this is the spare (08.64)",
    "pcb_din_clip_x3.stl": "kit supplies 4 — one is the 09.7 practice clip, rest spares",
    "PSU_stabilizer_50mm.stl": "fit only if needed (09.16)",
    "power_inlet_IECGS_1mm.stl": "ring segment: dry-fitted with the skirts at 11.1, mounted at 09.12",
    "z_rail_stop_x4.stl": "optional (02.10 / 06.10)",
    "KlickyProbe_v2.stl": "Klicky — alternative probe only, bag closed (08.54)",
    "cw2_captive_pcb_cover.stl": "replaces the stock `cable_door` (08.51)",
    "handlebar_spacer_x4.stl": "handlebars go on last (11.60)",
    "Handle.stl": "blue — joins the black door parts from B10",
    "V3L_COUPON_22N_DUCT.stl": "lid-snap coupon: tested at B11.4, bundle-fill test at B11.10, then kept here",
    "CMD_V2_6B_WIRE_BOX_COVER.stl": "plain lid; the WARNING lid waits for INDX",
    "CMD_Remix-V3_DUCT-1M_ENDCAP.stl": "Jet Black; orange ASA is an option with no plate",
    "V3L_10mm_DUCT.stl": "1 in 09-ducts-DC (rear-upper run), 2 in 09-ducts-AC (SSR run right end, box-port stub)",
    "V3L_154N_DUCT.stl": "fitted only if the Leviathan-to-PSU gap measured ≥ 25 mm",
    "V3L_T_REG_N.stl": "fitted only if the Leviathan-to-PSU gap measured ≥ 25 mm",
    "V2L_STRIP_FIN.stl": "divider between PSU −V and FG, fitted as Ch 10 closes the AC lids",
}

# ------------------------------------------------------------- add-on parts
# On no plate (slicer/plates.py ADDONS pins the files): printed after kit day inside their own
# chapter part. `name` is what the label says; `geom` is the file bin_bags.py measures (for the
# scrubber, the committed default set: the real files come out of `measured/` at Step 13.47 and
# differ by at most a few mm in height); `made` is where the part comes from instead of a plate id.
ADDON_PARTS: dict[str, list[dict]] = {
    "13-scrubber": [
        dict(name="brush bracket, mirrored", qty=1,
             geom=("addons", "scrubber-796563/brush_bracket_L1.5_MIRROR.stl"),
             made="add-on print, Step 13.48", note="file name from `measured/` (Step 13.47)"),
        dict(name="stop bracket", qty=1,
             geom=("addons", "scrubber-796563/stop_bracket.stl"),
             made="add-on print, Step 13.48", note="only if Step 13.47 fits the sheet stops"),
        dict(name="purge bucket, 350 mm, mirrored", qty=1,
             geom=("addons", "scrubber-796563/bucket350_T1.5_MIRROR.stl"),
             made="add-on print, Step 13.48", note="file name from `measured/` (Step 13.47)"),
    ],
    "14-exhaust": [
        dict(name="`exhaust_filter_housing`", qty=1,
             geom=("voron2", "STLs/Exhaust_Filter/exhaust_filter_housing.stl"),
             made="add-on print, Step 14.26 job 1", note="black"),
        dict(name="`[a]_exhaust_fan_grill`", qty=1,
             geom=("voron2", "STLs/Exhaust_Filter/[a]_exhaust_fan_grill.stl"),
             made="add-on print, Step 14.26 job 2", note="blue"),
        dict(name="`[a]_filter_access_cover`", qty=1,
             geom=("voron2", "STLs/Exhaust_Filter/[a]_filter_access_cover.stl"),
             made="add-on print, Step 14.26 job 2", note="blue"),
        dict(name="`[a]_exhaust_filter_mount`", qty=2,
             geom=("voron2", "STLs/Exhaust_Filter/[a]_exhaust_filter_mount_x2.stl"),
             made="add-on print, Step 14.26 job 2", note="blue"),
    ],
}


# --------------------------------------------------------- fallback parts
# On no plate, printed only in place of a plate: if Step B11.10 measures the Leviathan-to-PSU gap
# under 25 mm, B11-P5 is skipped and these stock MSS pieces print instead (B11.13, Options). They
# are pinned in slicer/plates.py PRINTABLES. They count toward no piece total, plate or estimate;
# they reach the labels, the index and the bag sizing, which takes the worse of the two cases
# (P5's parts, or these in their place: scenarios() below).
FALLBACK_WHEN = "only if the Leviathan-to-PSU gap is < 25 mm (Step B11.10)"
FALLBACK_SHORT = "if gap < 25 mm"
FALLBACK_PLATE = "B11-P5"
FALLBACK_MADE = "fallback, Step B11.13"
FALLBACK_PARTS: dict[str, list[dict]] = {
    "09-ducts-DC": [
        dict(qty=2, geom=("bayducts", "mss/502306/CMD_V3_1H_T_REG.stl"), instead="`V3L_T_REG_N` ×2"),
        dict(qty=1, geom=("bayducts", "mss/502306/CMD_V3_1H_82mm_DUCT.stl"), instead="`V3L_154N_DUCT` ×2"),
    ],
    "11-lids-DC": [
        dict(qty=2, geom=("bayducts", "mss/502306/CMD_V2_6B_T_REG_COVER.stl"),
             instead="`V3L_T_REG_N_COVER` ×2"),
        dict(qty=1, geom=("bayducts", "mss/502306/CMD_V2_6B_82mm_DUCT_COVER.stl"),
             instead="`V3L_154N_DUCT_COVER` ×2"),
    ],
}

# ---------------------------------------------------------- bought parts
# Bought, not printed, but bagged with the add-on they serve so the step that opens the bin finds
# them (Ch 00 Step 00.8's buy table). No picture, no piece count. `size` is a nominal box in mm
# that slicer/bin_bags.py packs like a printed piece; `made` places it in a split bin's bag.
BOUGHT_MADE = "bought, Step 00.8"
BOUGHT_PARTS: dict[str, list[dict]] = {
    "13-scrubber": [
        # Three wipers, one fitted (13.49); the Ch 13 Part L buy row is the 3-pack.
        dict(name="Bambu A1 nozzle wiper", short="A1 wiper", qty=3, size=(37.0, 8.0, 4.0),
             note="3-pack; one fitted at 13.49"),
    ],
    "14-exhaust": [
        dict(name="24 V 6020 fan", short="fan", qty=1, size=(60.0, 60.0, 20.0)),
        dict(name="1 m JST-XH 2-pin extension lead", short="lead", qty=1, size=(60.0, 60.0, 15.0), note="coiled"),
        # Bagged as two pieces cut to about the access cover's 73 x 135 mm (the filter bay it closes),
        # ~6 mm each; 14.28 trims them to the bay.
        dict(name="carbon-mat piece", short="carbon mat", qty=2, size=(130.0, 70.0, 6.0),
             note="about 70 × 130 mm, trimmed to the bay at 14.28"),
    ],
}


def contents() -> dict[str, dict[str, dict]]:
    """bin id -> part key -> {"name", "n", "made": [plate ids or add-on step], "note", "geom",
    "cond", "bought", "size"}.

    Plate parts come from slicer/plates.py through copies_bins (key = STL file name, `name` its
    short form in backticks); add-on parts from ADDON_PARTS. FALLBACK_PARTS come in with `cond` set
    (the condition text) and BOUGHT_PARTS with `bought` True, `geom` None and a nominal `size`;
    neither counts as a printed piece (pieces()). The labels, the index and slicer/bin_bags.py all
    read this one function."""
    from plates import PLATES   # slicer/plates.py; imported here so bins.py stays importable alone
    out: dict[str, dict[str, dict]] = {}

    def entry(**kw):
        return dict(dict(note=None, cond=None, bought=False, size=None, instead=None, short=None), **kw)

    for pid, spec in PLATES.items():
        for repo, path, qty in spec["parts"]:
            stl = path.rsplit("/", 1)[-1]
            for b in copies_bins(pid, stl, qty):
                e = out.setdefault(b, {}).setdefault(stl, entry(
                    name=f"`{short_name(stl)}`", n=0, made=[], note=NOTES.get(stl), geom=(repo, path)))
                e["n"] += 1
                if pid not in e["made"]:
                    e["made"].append(pid)
    for b, parts in ADDON_PARTS.items():
        for p in parts:
            out.setdefault(b, {})[p["geom"][1]] = entry(
                name=p["name"], n=p["qty"], made=[p["made"]], note=p.get("note"), geom=p["geom"])
    for b, parts in FALLBACK_PARTS.items():
        for p in parts:
            stl = p["geom"][1].rsplit("/", 1)[-1]
            out.setdefault(b, {})[stl] = entry(
                name=f"`{short_name(stl)}`", n=p["qty"], made=[FALLBACK_MADE], geom=p["geom"],
                cond=FALLBACK_WHEN, instead=p["instead"])
    for b, parts in BOUGHT_PARTS.items():
        for p in parts:
            out.setdefault(b, {})[f"bought:{p['name']}"] = entry(
                name=p["name"], n=p["qty"], made=[BOUGHT_MADE], note=p.get("note"), geom=None,
                bought=True, size=p["size"], short=p["short"])
    return out


def pieces(parts: dict[str, dict]) -> int:
    """Printed pieces in a contents() mapping: fallback and bought entries do not count."""
    return sum(e["n"] for e in parts.values() if not e["cond"] and not e["bought"])


def scenarios(parts: dict[str, dict]) -> list[dict[str, dict]]:
    """The sets of entries a bag may have to hold at once: everything but the fallback parts, and,
    when any are present, the case where they replace FALLBACK_PLATE's parts. Bought entries are in
    both. slicer/bin_bags.py sizes a bag for the worse of the two."""
    base = {k: e for k, e in parts.items() if not e["cond"]}
    if not any(e["cond"] for e in parts.values()):
        return [base]
    alt = {k: e for k, e in parts.items()
           if e["cond"] or (not e["cond"] and FALLBACK_PLATE not in e["made"])}
    return [base, alt]


# A bin that travels in more than one bag: which parts go in which bag. One set per bag, bag 1
# first; a set holds part keys (STL file names) and/or `made` values (plate id, add-on print step,
# FALLBACK_MADE, BOUGHT_MADE): a part goes to the bag that names its key, else to the bag whose set
# holds all its `made` values. Every bag of a bin is opened at the same step (BINS steps): a split
# is only about fitting, never about when.
# 09-ducts-DC is split by volume, since 1121 cm³ needs three A5 and no plate-aligned split fits:
# bag 1 the front run and right side, bag 2 the left side, the rear runs and the S-jog, bag 3 the
# narrowed middle run (P5) or the fallback that replaces it (the fallback is the smaller case).
# 14-exhaust splits by print job, which is by size: the housing (the one big piece) in bag 1, the
# rest and the bought fan, lead and mat in bag 2.
BAG_SPLIT: dict[str, list[set[str]]] = {
    "09-ducts-DC": [
        {"V3L_COUPON_22N_DUCT.stl", "V3L_COUPON_22N_DUCT_COVER.stl", "CMD_V3_1H_154mm_DUCT.stl",
         "CMD_V3_1H_90DEG.stl", "V2L_70mm_DUCT.stl"},
        {"V2L_90DEG_MIRROR.stl", "CMD_Remix-V3_DUCT-2B_45deg.stl", "V2L_58mm_DUCT.stl",
         "V2L_130mm_DUCT.stl", "V3L_10mm_DUCT.stl"},
        {"B11-P5", FALLBACK_MADE},
    ],
    "14-exhaust": [{"add-on print, Step 14.26 job 1"}, {"add-on print, Step 14.26 job 2", BOUGHT_MADE}],
}

BAG_SPLIT_WHY: dict[str, str] = {
    "09-ducts-DC": "splits by volume, the middle run or its fallback in bag 3",
    "14-exhaust": "splits by size, the housing alone in bag 1",
}


def containers() -> list[dict]:
    """One dict per physical container (a bag or a box), in BINS order, bag 1 of a split bin first:
    {bin, kind ("A5"|"B5"|"box"), k (1-based bag number), of (bags in the bin), parts (part key ->
    contents() entry), n (printed pieces, pieces())}. Raises if a split leaves a part unplaced or placed twice."""
    cont = contents()
    out = []
    for b, meta in BINS.items():
        kind, nbags = bag_parse(meta["bag"])
        parts = cont.get(b, {})
        if nbags == 1:
            groups = [dict(parts)]
        else:
            split = BAG_SPLIT.get(b)
            if not split or len(split) != nbags:
                raise ValueError(f"{b}: {nbags} bags but BAG_SPLIT has "
                                 f"{len(split) if split else 0} groups")
            keyed = {k for g in split for k in g if k in parts}
            groups = [{k: e for k, e in parts.items()
                       if k in g or (k not in keyed and set(e["made"]) <= g)} for g in split]
            placed = sum(len(g) for g in groups)
            if placed != len(parts) or len({k for g in groups for k in g}) != len(parts):
                raise ValueError(f"{b}: BAG_SPLIT places {placed} of {len(parts)} parts exactly once")
        for k, g in enumerate(groups, 1):
            out.append(dict(bin=b, kind=kind, k=k, of=nbags, parts=g, n=pieces(g)))
    return out


def stock_note() -> str:
    """The index header's stock sentence: what is still to buy, then the spares once it is bought.
    `owned` is the planned stock; `on_hand` is what is already on the bench."""
    sp = spares()
    buy = [f"{BAGS[k]['owned'] - BAGS[k]['on_hand']} {k}" for k in BAGS
           if BAGS[k]["owned"] > BAGS[k]["on_hand"]]
    have = ", ".join(f"{BAGS[k]['on_hand']} {k}" for k in BAGS)
    spare = f"{sp['A5']} A5, {sp['B5']} B5"
    if buy:
        return f"On hand: {have}. To buy: {', '.join(buy)}. Spares once bought: {spare}."
    return f"Spares: {spare}."


def spares() -> dict[str, int]:
    """{"A5": owned - used, "B5": ...}: mesh bags left over."""
    c = bag_counts()
    return {k: BAGS[k]["owned"] - c[k] for k in BAGS}


def copies_bins(plate_id: str, stl: str, n_copies: int) -> list[str]:
    """Bin id for each printed copy of `stl` on `plate_id`, in copy order."""
    spec = PLATE_ASSIGN.get((plate_id, stl)) or ASSIGN[stl]
    if isinstance(spec, str):
        return [spec] * n_copies
    return [spec[i % len(spec)] for i in range(n_copies)]


def manifest_value(stl: str) -> str:
    """The `bin` cell for MANIFEST.csv: one id, or `;`-joined ids, one per copy in plate order."""
    spec = ASSIGN[stl]
    return spec if isinstance(spec, str) else ";".join(spec)


def short_name(stl: str) -> str:
    """`z_drive_main_a_x2.stl` -> `z_drive_main_a`; the manual's short form."""
    name = re.sub(r"\.(stl|3mf)$", "", stl, flags=re.I)
    return re.sub(r"_x\d+$", "", name)


def text_colour(hex_colour: str) -> str:
    """White or near-black, whichever reads on this fill."""
    r, g, b = (int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5))
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return "#ffffff" if lum < 0.5 else "#1a1a1e"


def check(plate_sources: list[str], addon_sources: list[tuple[str, str]] | None = None) -> list[str]:
    """Every STL in the plan has exactly one assignment; every assignment names a real bin
    and a real STL. `plate_sources` are basenames from slicer/plates.py; `addon_sources` its
    ADDONS (repo, path) pairs, which every ADDON_PARTS file must be one of. Every bin names a
    valid bag, and the add-on bins hold nothing a plate feeds."""
    bad = []
    for b, meta in BINS.items():
        try:
            bag_parse(meta.get("bag", ""))
        except ValueError as e:
            bad.append(f"{b}: {e}")
    plate_bins = {x for spec in ASSIGN.values() for x in ([spec] if isinstance(spec, str) else spec)}
    for b, parts in ADDON_PARTS.items():
        if b not in BINS:
            bad.append(f"ADDON_PARTS: unknown bin {b}")
        if b in plate_bins:
            bad.append(f"ADDON_PARTS: bin {b} also takes plate parts; an add-on bin must not")
        for p in parts:
            if addon_sources is not None and tuple(p["geom"]) not in set(addon_sources):
                bad.append(f"ADDON_PARTS {b}: {p['geom'][1]} is not in slicer/plates.py ADDONS")
    from plates import PRINTABLES   # slicer/plates.py: the fallback files must be pinned there
    for b, parts in FALLBACK_PARTS.items():
        if b not in BINS:
            bad.append(f"FALLBACK_PARTS: unknown bin {b}")
        for p in parts:
            if tuple(p["geom"]) not in PRINTABLES:
                bad.append(f"FALLBACK_PARTS {b}: {p['geom'][1]} is not pinned in slicer/plates.py PRINTABLES")
    for b in list(BOUGHT_PARTS) + list(BAG_SPLIT):
        if b not in BINS:
            bad.append(f"BOUGHT_PARTS/BAG_SPLIT: unknown bin {b}")
    wanted = set(plate_sources)
    for stl in sorted(wanted - set(ASSIGN)):
        bad.append(f"no bin for {stl}")
    for stl in sorted(set(ASSIGN) - wanted):
        bad.append(f"bin assigned to {stl}, which is on no plate")
    for stl, spec in ASSIGN.items():
        for b in ([spec] if isinstance(spec, str) else spec):
            if b not in BINS:
                bad.append(f"{stl}: unknown bin {b}")
    for (pid, stl), spec in PLATE_ASSIGN.items():
        if stl not in ASSIGN:
            bad.append(f"PLATE_ASSIGN {pid}/{stl}: STL not in ASSIGN")
        for b in spec:
            if b not in BINS:
                bad.append(f"PLATE_ASSIGN {pid}/{stl}: unknown bin {b}")
    return bad


if __name__ == "__main__":
    from plates import ADDONS, PLATES
    names = [p.rsplit("/", 1)[-1] for pl in PLATES.values() for _r, p, _q in pl["parts"]]
    problems = check(names, list(ADDONS))
    for p in problems:
        print(p)
    print(f"{len(BINS)} bins, {len(ASSIGN)} STLs, {len(problems)} problem(s)")
    raise SystemExit(1 if problems else 0)
