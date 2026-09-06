#!/usr/bin/env python3
"""Bin scheme: which sorting bin every printed part goes into once it is off the plate.

One bin per consuming assembly chapter, sub-bins where a chapter is part-heavy
(the four Z corners, the A/B drive sides, the 4 mm / 6 mm panel clips ...).
This is the single source for:

  * scripts/render_plate_bins.py  - the per-plate sorting diagrams (colour + bin id on every part)
  * scripts/build_printables.py   - the printable bin labels and the bin map
  * docs/manual/assets/parts/MANIFEST.csv `bin` column (written by render_plate_bins.py --write-manifest)
  * docs/manual/print/README.md § Bins (hand-maintained; slicer/check_docs.py cross-checks it)

Consumers were derived from the assembly chapters' Printed-parts tables and the steps that name each
STL (docs/manual/NN-*.md). Corner map for the Z parts is Ch 02 Step 02.02: `_a` parts build Z0
(front-left) and Z2 (rear-right), `_b` parts build Z1 (rear-left) and Z3 (front-right).
"""
from __future__ import annotations

import re

# ------------------------------------------------------------------ the bins
# id -> (label, chapter, steps, colour)
#   label   : what to write on the bin
#   chapter : "Ch NN" the bin is opened for (the chapter whose steps fit the parts)
#   steps   : step range(s) in that chapter; secondary uses in parentheses
#   colour  : fill on the plate diagrams and labels (hex); consistent across every plate
BINS: dict[str, dict[str, str]] = {
    "00-jigs": dict(
        label="Jigs and coupons",
        chapter="Ch 00", steps="00.14–00.22 (rail guides again at 02.06, 05.11, 05.33; pulley jig at 02.18, 04.24, 04.33; cube at 14.10)",
        colour="#8a8f98"),
    "02-Z0": dict(label="Z0 corner (front-left, `_a` hand)", chapter="Ch 02", steps="02.01–02.44 (drive 02.17–02.36, idler 02.37–02.43)", colour="#2457c5"),
    "02-Z1": dict(label="Z1 corner (rear-left, `_b` hand)", chapter="Ch 02", steps="02.01–02.44 (drive 02.17–02.36, idler 02.37–02.43)", colour="#1a9c8c"),
    "02-Z2": dict(label="Z2 corner (rear-right, `_a` hand)", chapter="Ch 02", steps="02.01–02.44 (drive 02.17–02.36, idler 02.37–02.43)", colour="#7b4fc4"),
    "02-Z3": dict(label="Z3 corner (front-right, `_b` hand)", chapter="Ch 02", steps="02.01–02.44 (drive 02.17–02.36, idler 02.37–02.43)", colour="#3fa9e0"),
    "02-deck": dict(label="Deck panel clips", chapter="Ch 02", steps="02.11–02.15 (confirm thickness at 02.12)", colour="#7f95c9"),
    "04-A": dict(label="A drive unit + A (right) front idler", chapter="Ch 04", steps="04.1–04.24 (A idler 04.6–04.9, A drive 04.20–04.24)", colour="#2e8b57"),
    "04-B": dict(label="B drive unit + B (left) front idler", chapter="Ch 04", steps="04.1–04.33 (B idler 04.13–04.16, B drive 04.29–04.33)", colour="#8fbc4a"),
    "05-XY": dict(label="XY joints, cable bridge, endstop pod", chapter="Ch 05", steps="05.3, 05.25–05.38 (endstop pod fitted at 09.32–09.33)", colour="#c2185b"),
    "06-Z-joints": dict(label="Z joints, belt clips, rail stops", chapter="Ch 06", steps="06.3–06.10, 06.26 (rail stops optional at 02.10)", colour="#a0522d"),
    "07-X": dict(label="X carriage halves, probe bracket, cable cover", chapter="Ch 07", steps="07.6–07.39 (staged at 05.45; probe 07.35; cover 07.39)", colour="#cd853f"),
    "08-SB": dict(label="Stealthburner body, printhead, LEDs", chapter="Ch 08", steps="08.2–08.62 (printhead 08.28–08.30, LEDs 08.35–08.37, body 08.62)", colour="#d62839"),
    "08-CW2": dict(label="Clockwork 2 extruder + toolboard cover", chapter="Ch 08", steps="08.3–08.20 (cover 08.51)", colour="#f28482"),
    "09-bay": dict(label="Electronics bay: inlet, WAGO, PSU, USB, DIN clips", chapter="Ch 09", steps="09.7–09.25 (inlet 09.10–09.12, WAGO 09.13, PSU 09.15–09.16, USB 09.25)", colour="#e0a100"),
    "10-chains": dict(label="Z cable chain anchor, guide, retainer", chapter="Ch 10", steps="10.62–10.64 (inserts at 10.35)", colour="#6b8e23"),
    "10-lights": dict(label="COB light-strip mounts", chapter="Ch 10", steps="10.35–10.36", colour="#b8b62c"),
    "11-skirts": dict(label="Skirt ring, keystone panel, TFT mount", chapter="Ch 11", steps="11.1–11.17 (TFT 11.5–11.7, keystone 11.10, bestagon 11.19)", colour="#5c6b73"),
    "11-fans": dict(label="Fan grills, retainers, belt guards", chapter="Ch 11", steps="11.3, 11.9, 11.11, 11.16", colour="#9aa5ad"),
    "11-panels": dict(label="Bottom-panel clips/hinges, Z belt covers, handlebar spacers", chapter="Ch 11", steps="11.20–11.25, 11.60", colour="#8d6e63"),
    "11-clips-4mm": dict(label="Panel clips, 4 mm (back + top panels)", chapter="Ch 11", steps="11.53, 11.59", colour="#a1887f"),
    "11-clips-6mm": dict(label="Panel clips, 6 mm (side panels)", chapter="Ch 11", steps="11.57–11.58", colour="#6d4c41"),
    "11-nevermore": dict(label="Nevermore plenum + cartridge, exhaust cover + grill", chapter="Ch 11", steps="11.26–11.40, 11.54", colour="#00695c"),
    "11-spool": dict(label="Spool holder + bowden retainer", chapter="Ch 11", steps="11.42–11.43", colour="#78909c"),
    "11-door": dict(label="Clicky-Clack door", chapter="Ch 11", steps="11.44–11.50, 11.62–11.64", colour="#ff7043"),
    "spare-alt": dict(label="Spares / alternates (not fitted)", chapter="—", steps="Klicky set bagged at 08.54; USB base and PCB spacer are kit-supplied", colour="#bdbdbd"),
}

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
    "[a]_faceplate.stl": "11-skirts",
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
    "[a]_z_belt_clip_upper_x4.stl": "06-Z-joints",
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
    "z_rail_stop_x4.stl": "06-Z-joints",
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
    "usb_adapter_mount_partial_cover.stl": "09-bay",
    "pcb_din_clip_x3.stl": "09-bay",
    "handlebar_spacer_x4.stl": "11-panels",
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
    "mount.stl": "11-skirts",
    # B09
    "V2_Duo_Plenum.stl": "11-nevermore",
    "V2_Duo_Plenum_LID.stl": "11-nevermore",
    "Regular_Cartridge_Lid(contributed_by_Bucknova).3mf": "11-nevermore",
    "Regular_Cartridge(contributed_by_Bucknova).3mf": "11-nevermore",
    "exhaust_cover.stl": "11-nevermore",
    "exhaust_filter_grill.stl": "11-nevermore",
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
}

PLATE_ASSIGN: dict[tuple[str, str], list[str]] = {
    ("B00-P1", "z_drive_retainer_a_x2.stl"): ["02-Z0"],
    ("B01-P1", "z_drive_retainer_a_x2.stl"): ["02-Z2"],
}

# Per-part notes that belong on the label / sort table (not on the diagram).
NOTES: dict[str, str] = {
    "Voron_Design_Cube_v7.stl": "reference coupon — keep for the Gen 2 re-check and 14.10",
    "Heatset_Practice.stl": "Gate B coupon (7 inserts, Step B00.7)",
    "MGN12_rail_guide_x2.stl": "one is the Gate B coupon (Step B00.7)",
    "z_drive_retainer_a_x2.stl": "B00 copy is the Gate B bore coupon",
    "deck_support_3mm_x8.stl": "reprint `deck_support_4mm_x8` if the deck panel calipers 4 mm (02.12)",
    "XY_cable_chain_bridge-Igus-3mm_backer.stl": "alternate to `[a]_xy_joint_cable_bridge_2hole` — fit whichever clears the backer (05.3)",
    "[a]_endstop_pod_D2F_switch.stl": "staged at 05.46, fitted at 09.32–09.33",
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
    "Handle.stl": "orange — joins the black door parts from B10",
}


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


def check(plate_sources: list[str]) -> list[str]:
    """Every STL in the plan has exactly one assignment; every assignment names a real bin
    and a real STL. `plate_sources` are basenames from slicer/plates.py."""
    bad = []
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
    from plates import PLATES
    names = [p.rsplit("/", 1)[-1] for pl in PLATES.values() for _r, p, _q in pl["parts"]]
    problems = check(names)
    for p in problems:
        print(p)
    print(f"{len(BINS)} bins, {len(ASSIGN)} STLs, {len(problems)} problem(s)")
    raise SystemExit(1 if problems else 0)
