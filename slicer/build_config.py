#!/usr/bin/env python3
"""Generate the PrusaSlicer `--load` config bundles and OVERRIDES.md.

Base values come from the PrusaResearch.ini that ships with the installed
PrusaSlicer 2.9.6, with `inherits` resolved (see resolve_preset.py), so the
committed .ini is provably the system preset plus this build's overrides and
nothing else.

    python3 slicer/build_config.py

Three bundles: voron-coreone-asa.ini and voron-accent-blue.ini (the 22-plate ASA run)
and bay-ducts-petg.ini (batch B11, the PETG V0 bay ducts; its own base filament and
print overrides, the same printer settings and cold start).
"""
from __future__ import annotations

from pathlib import Path

from resolve_preset import load_bundle, resolve

ROOT = Path(__file__).resolve().parent
DOC = "docs/manual/print/00-slicer-setup.md"

# Alex's cold-probe start G-code, vendored from
# ~/projects/core-one-mods/reference/coreone-cold-start.gcode (verified 2026-09-14) so
# this repo builds without that one. Single-line `\n` escaping is what `--load` reads
# and what PrusaSlicer itself writes.
COLD_START = ROOT / "coreone-cold-start.gcode"


def cold_start_gcode() -> str:
    return COLD_START.read_text().rstrip("\n").replace("\n", "\\n")

BASE_PRINT = "0.20mm STRUCTURAL @COREONE 0.4"
BASE_FILAMENT = "Prusament ASA @COREONE HF0.4"
BASE_PRINTER = "Prusa CORE One HF0.4 nozzle"

# (key, value, section, why, doc reference)
# `section` is only used to group OVERRIDES.md; the emitted .ini is flat, which
# is the format `--load` reads.
OVERRIDES: list[tuple[str, str, str, str, str]] = [
    # --- Print settings (00-slicer-setup.md § Overrides > Print settings) ---
    ("perimeters", "4", "print",
     "Voron spec; wall count carries load in these parts", "Print row 2 (Manual p.4)"),
    ("bottom_solid_layers", "5", "print",
     "Voron spec says 5 top and bottom", "Print row 4 (Manual p.4)"),
    ("fill_density", "40%", "print", "Voron spec", "Print row 5 (Manual p.4)"),
    ("extrusion_width", "0.4", "print",
     'Voron: "Extrusion width - Recommended: Forced 0.4 mm"', "Print row 7 (Manual p.4)"),
    ("perimeter_extrusion_width", "0.4", "print", "same forced-0.4 rule", "Print row 7"),
    ("external_perimeter_extrusion_width", "0.4", "print", "same forced-0.4 rule", "Print row 7"),
    ("infill_extrusion_width", "0.4", "print", "same forced-0.4 rule", "Print row 7"),
    ("solid_infill_extrusion_width", "0.4", "print", "same forced-0.4 rule", "Print row 7"),
    ("top_infill_extrusion_width", "0.4", "print", "consistency (judgment)", "Print row 9"),
    ("support_material", "0", "print",
     "every Voron/LDO/Nevermore STL is pre-oriented with built-in break-away supports",
     "Print row 11"),
    ("support_material_auto", "0", "print", "same", "Print row 11"),
    ("seam_position", "rear", "print",
     "keeps the seam off the visible outward faces of skirts and toolhead", "Print row 12"),
    ("skirts", "1", "print",
     "primes after the long ASA purge; lets you abort in the first 60 s", "Print row 13"),
    ("skirt_distance", "3", "print", "3 mm gap", "Print row 13"),
    ("skirt_height", "1", "print", "one loop, first layer only", "Print row 13"),
    ("min_skirt_length", "4", "print", "min length 4 mm (already the base value)", "Print row 13"),
    ("brim_type", "outer_only", "print",
     "outer_only keeps the brim off internal holes", "Print row 14"),
    ("brim_width", "0", "print",
     "off globally; build_plates.py writes 3 mm / 5 mm as per-object metadata into each "
     "plate 3MF for exactly the parts the doc names",
     "Print row 14 + section Orientation & brim"),
    ("brim_separation", "0.1", "print",
     "PrusaSlicer default, kept so the brim snaps off", "section Orientation & brim"),
    ("xy_size_compensation", "0", "print",
     'Voron: parts are drawn for ASA shrinkage; compensating "is likely to make bearing '
     'fits and screw holes too large"', "Print row 15 (docs.vorondesign.com/materials.html)"),
    ("elefant_foot_compensation", "0.2", "print",
     "kept at the profile value for now, verify on the cube", "Print row 16"),
    ("external_perimeter_speed", "35", "print",
     "surface finish and corner accuracy on the visible skirts", "Print row 17"),
    ("perimeter_speed", "55", "print",
     "more time at temperature per bead = better interlayer bond at 4 walls", "Print row 18"),
    ("infill_speed", "100", "print",
     "interior quality and less pressure variation into the perimeters", "Print row 19"),
    ("solid_infill_speed", "110", "print", "flatter top/bottom faces on the skirts", "Print row 20"),
    ("first_layer_speed", "25", "print",
     "ASA on smooth PEI is the biggest failure mode; slow the first layer", "Print row 22"),
    ("ironing", "0", "print", "kept off", "Print row 25"),
    # --- Filament settings (§ Overrides > Filament settings) ---
    ("filament_shrinkage_compensation_xy", "0%", "filament",
     "THE critical override: the profile scales ASA up 0.22 %, which lands in the bearing bores",
     "Filament row 1"),
    ("filament_shrinkage_compensation_z", "0%", "filament", "same reason", "Filament row 2"),
    # --- Thumbnails (needed for the plate previews in docs/manual/assets/plates/) ---
    ("thumbnails", "16x16/QOI, 313x173/QOI, 480x240/QOI, 380x285/PNG, 640x480/PNG", "printer",
     "stock CORE One list plus a 640x480 PNG, so a G-code export from the GUI carries a "
     "doc-sized preview. The CLI writes no thumbnail data at all (see the last section), so "
     "the committed plate previews are drawn by slicer/render_plate.py instead.",
     "added for R6 P4"),
    # --- Start G-code (cold-probe / loadcell workaround, 2026-09-14) ---
    ("start_gcode", cold_start_gcode(), "printer",
     "the stock CORE One start heats the nozzle to 170 C for homing and MBL and runs "
     "`G29 P9` to wipe it; on this machine that loads the loadcell with a hot, oozing tip "
     "and raises 'bed not aligned' prompts mid-probe. This block probes cold - `M104 S0` "
     "held through G28, chamber soak and MBL, `G29 P9` dropped (wipe the tip by hand while "
     "hot), heat to `first_layer_temperature` only for the purge line. It also carries "
     "`M115 U6.8.1+16182`, the firmware this was verified on, in place of the preset's "
     "6.5.3. Vendored byte-for-byte as `slicer/coreone-cold-start.gcode`.",
     "printer preset `Prusa CORE One HF0.4 nozzle - coldstart`"),
]

# Values too long to sit in a markdown cell: what OVERRIDES.md prints instead of
# the raw before/after strings. Keyed by ini key -> (flattened preset, set to).
MD_CELLS = {
    "start_gcode": ("*(the stock CORE One start block)*",
                    "*(the block in `slicer/coreone-cold-start.gcode`)*"),
}

HEADER = """\
# PrusaSlicer 2.9.6 configuration for the LDO Voron 2.4 R2 (350) print run.
# GENERATED by slicer/build_config.py - edit that script, not this file.
#
# Base system presets, read from the PrusaResearch.ini shipped with the
# installed PrusaSlicer ({bundle_version}) and flattened through `inherits`:
#   print    = {base_print}
#   filament = {base_filament}
#   printer  = {base_printer}
#
# Overrides applied on top: see slicer/OVERRIDES.md (one row per key, each
# mapped to the line in {doc} it comes from).
#
# Use:  PrusaSlicer --load slicer/{name}.ini --export-3mf ...
"""


def bundle_version(sections: dict) -> str:
    return sections.get("vendor", {}).get("config_version", "unknown")


def build(colour: str, name: str, filament_colour: str, filament_note: str) -> dict[str, str]:
    sections = load_bundle()
    cfg: dict[str, str] = {}
    cfg.update(resolve(sections, "print", BASE_PRINT))
    cfg.update(resolve(sections, "filament", BASE_FILAMENT))
    cfg.update(resolve(sections, "printer", BASE_PRINTER))
    # Provenance: name the presets this config was flattened from.
    cfg["print_settings_id"] = BASE_PRINT
    cfg["filament_settings_id"] = f"{BASE_FILAMENT} - Voron {colour}"
    cfg["printer_settings_id"] = BASE_PRINTER
    for key, value, _sec, _why, _src in OVERRIDES:
        cfg[key] = value
    cfg["filament_colour"] = filament_colour
    cfg["filament_notes"] = filament_note
    # Not config options - vendor bookkeeping that `--load` would reject.
    for junk in ("renamed_from", "compatible_prints", "compatible_printers"):
        cfg.pop(junk, None)
    # Preset-picker conditions are meaningless in a flattened config and make
    # PrusaSlicer re-filter the very presets we just flattened.
    cfg.pop("compatible_printers_condition", None)
    cfg.pop("compatible_prints_condition", None)
    return cfg


def write_ini(path: Path, cfg: dict[str, str], name: str, version: str) -> None:
    head = HEADER.format(bundle_version=version, base_print=BASE_PRINT,
                         base_filament=BASE_FILAMENT, base_printer=BASE_PRINTER,
                         doc=DOC, name=name)
    body = "\n".join(f"{k} = {v}" for k, v in sorted(cfg.items()))
    path.write_text(head + "\n" + body + "\n")


# ------------------------------------------------------------ B11: bay ducts (PETG V0)
# Ducts carry no load, so they are not printed to Voron spec. Same printer preset, same
# vendored cold start and thumbnails as the ASA bundles; its own filament and print rows.
BAY_DOC = "docs/manual/print/B11-bay-ducting.md"
BAY_FILAMENT = "Prusament PETG V0 @COREONE HF0.4"
# Rear chamber-fan pair (P3) at a fixed target lifts Walter's AFS bypass flaps even in Adv.
# Filtration mode, which otherwise zeroes those fans for the whole print; `R` hands them back
# to the firmware. Verified in Buddy 6.8.1 source (PROJECT_MEMORY › Core One+ operating notes).
FLAPS_ON = "M106 P3 S160 ; AFS bypass flaps open: rear chamber fans to a fixed 63 %"
FLAPS_OFF = "M106 P3 R ; rear chamber fans back to firmware control"


def _append_gcode(value: str, line: str) -> str:
    """Append one line to a quoted, `\n`-escaped G-code value as PrusaSlicer writes it."""
    if value.startswith('"') and value.endswith('"'):
        return value[:-1] + "\\n" + line + '"'
    return value + "\\n" + line


def bay_overrides(sections: dict) -> list[tuple[str, str, str, str]]:
    """(key, value, section, why) for bay-ducts-petg.ini."""
    fil = resolve(sections, "filament", BAY_FILAMENT)
    return [
        ("layer_height", "0.2", "print", "0.20 mm layers (already the base value)"),
        ("perimeters", "3", "print", "3 walls: stiff enough for a snap lid, no load to carry"),
        ("top_solid_layers", "4", "print", "4 top layers"),
        ("bottom_solid_layers", "4", "print", "4 bottom layers"),
        ("fill_density", "20%", "print", "20 % infill"),
        ("fill_pattern", "grid", "print",
         "grid, not gyroid: gyroid infill curls with PETG on this printer (PETG sweep 2026-09-22)"),
        ("support_material", "0", "print", "no supports: every piece prints flat on its base"),
        ("support_material_auto", "0", "print", "same"),
        ("start_filament_gcode", _append_gcode(fil["start_filament_gcode"], FLAPS_ON), "filament",
         "the preset's start block plus `M106 P3 S160` - lifts the AFS bypass flaps for PETG"),
        ("end_filament_gcode", _append_gcode(fil["end_filament_gcode"], FLAPS_OFF), "filament",
         "the preset's end block plus `M106 P3 R`"),
        ("thumbnails", next(v for k, v, *_ in OVERRIDES if k == "thumbnails"), "printer",
         "same as the ASA bundles"),
        ("start_gcode", cold_start_gcode(), "printer",
         "the vendored cold-probe start, same as the ASA bundles"),
    ]


def build_bay() -> tuple[dict[str, str], list[tuple[str, str, str, str]]]:
    sections = load_bundle()
    cfg: dict[str, str] = {}
    cfg.update(resolve(sections, "print", BASE_PRINT))
    cfg.update(resolve(sections, "filament", BAY_FILAMENT))
    cfg.update(resolve(sections, "printer", BASE_PRINTER))
    cfg["print_settings_id"] = BASE_PRINT
    cfg["filament_settings_id"] = f"{BAY_FILAMENT} - Voron bay ducts"
    cfg["printer_settings_id"] = BASE_PRINTER
    rows = bay_overrides(sections)
    for key, value, _sec, _why in rows:
        cfg[key] = value
    cfg["filament_colour"] = "#1A1A1A"
    cfg["filament_notes"] = ("Prusament PETG V0 Jet Black - B11 bay ducting only. "
                             "Textured sheet: PETG can bond to smooth PEI and tear it.")
    for junk in ("renamed_from", "compatible_prints", "compatible_printers",
                 "compatible_printers_condition", "compatible_prints_condition"):
        cfg.pop(junk, None)
    return cfg, rows


BAY_HEADER = """\
# PrusaSlicer 2.9.6 configuration for batch B11: the Voron bay ducts, Prusament PETG V0.
# GENERATED by slicer/build_config.py - edit that script, not this file.
#
# Base system presets, read from the PrusaResearch.ini shipped with the
# installed PrusaSlicer ({bundle_version}) and flattened through `inherits`:
#   print    = {base_print}
#   filament = {base_filament}
#   printer  = {base_printer}
#
# NOT Voron spec: the ducts carry no load. Overrides: slicer/OVERRIDES.md § Bay-duct
# bundle; the page that uses it is {doc}.
#
# Use:  PrusaSlicer --load slicer/bay-ducts-petg.ini --export-3mf ...
"""


def write_bay_ini(path: Path, cfg: dict[str, str], version: str) -> None:
    head = BAY_HEADER.format(bundle_version=version, base_print=BASE_PRINT,
                             base_filament=BAY_FILAMENT, base_printer=BASE_PRINTER, doc=BAY_DOC)
    body = "\n".join(f"{k} = {v}" for k, v in sorted(cfg.items()))
    path.write_text(head + "\n" + body + "\n")


def bay_overrides_md(rows, version: str) -> list[str]:
    sections = load_bundle()
    base = {}
    base.update(resolve(sections, "print", BASE_PRINT))
    base.update(resolve(sections, "filament", BAY_FILAMENT))
    base.update(resolve(sections, "printer", BASE_PRINTER))
    out = [
        "## Bay-duct bundle (B11)",
        "",
        f"`slicer/bay-ducts-petg.ini` prints batch B11 ([`{BAY_DOC}`](../{BAY_DOC})): the PETG V0",
        "bay ducts, which carry no load and are **not printed to Voron spec**. Print and printer",
        f"presets are the ASA bundles' (`{BASE_PRINT}`, `{BASE_PRINTER}`); the filament base is",
        f"`{BAY_FILAMENT}`. The print preset's modest speeds keep internal infill at 120 mm/s, under",
        "the PETG preset's own 200 mm/s infill cap and below the speeds the 2026-09-22 PETG sweep",
        "suspects of lifting strands. Every key that differs from those flattened presets:",
        "",
        "| ini key | Flattened preset value | Set to | Why |",
        "|---|---|---|---|",
    ]
    for key, value, _sec, why in rows:
        if key == "start_gcode":
            out.append(f"| `{key}` | {MD_CELLS[key][0]} | {MD_CELLS[key][1]} | {why} |")
            continue
        before = base.get(key, "*(PrusaSlicer built-in default)*")
        cell = lambda v: (v if len(v) <= 90 else v[:87] + "...").replace("|", "\\|")
        if key.endswith("filament_gcode"):
            shown = "*(preset block)* + `" + value.rsplit("\\n", 1)[-1].rstrip('"').split(" ;")[0] + "`"
            out.append(f"| `{key}` | *(preset block)* | {shown} | {why} |")
            continue
        out.append(f"| `{key}` | `{cell(before)}` | `{cell(value)}` | {why} |")
    out += [
        "",
        "Kept at the preset value: nozzle 230 C, bed 85/90 C, chamber 35 C, fan 30-60 %,",
        "`filament_max_volumetric_speed` 16, `extrusion_multiplier` 1.04, seam aligned, no skirt,",
        "no brim. Colour `#1A1A1A` (Jet Black) and the notes line are labels only.",
        "",
    ]
    return out


def write_overrides_md(black: dict[str, str], accent: dict[str, str], version: str,
                       bay_rows=None) -> None:
    sections = load_bundle()
    base = {}
    base.update(resolve(sections, "print", BASE_PRINT))
    base.update(resolve(sections, "filament", BASE_FILAMENT))
    base.update(resolve(sections, "printer", BASE_PRINTER))

    rows = {"print": [], "filament": [], "printer": []}
    for key, value, sec, why, src in OVERRIDES:
        before = base.get(key, "*(PrusaSlicer built-in default)*")
        if key in MD_CELLS:                       # multi-line values: name them, do not print them
            was, now = MD_CELLS[key]
            rows[sec].append(f"| `{key}` | {was} | {now} | {why} | {src} |")
            continue
        if len(before) > 120:
            before = before[:117] + "..."
        shown = value if len(value) <= 120 else value[:117] + "..."
        changed = "" if str(before) == value else " "
        rows[sec].append(f"| `{key}` | `{before}`{changed} | `{shown}` | {why} | {src} |")

    out = [
        "# Override map",
        "",
        "Every key in `slicer/voron-coreone-asa.ini` that differs from the flattened system",
        f"preset, mapped back to the line in [`{DOC}`](../{DOC}) it comes from.",
        f"Generated by `slicer/build_config.py` against PrusaResearch.ini `config_version = {version}`",
        "as installed with PrusaSlicer 2.9.6.",
        "",
        "## Base presets",
        "",
        "| Role | System preset | Why this one |",
        "|---|---|---|",
        f"| print | `{BASE_PRINT}` | STRUCTURAL, not SPEED. **No `0.20mm STRUCTURAL @COREONE HF0.4` "
        "exists in the bundle** - STRUCTURAL ships only in the non-HF variant at 0.20 mm. This preset's "
        "`compatible_printers_condition` is `printer_model=~/(COREONE\\|COREONEOAK\\|COREONEMMU3)/ and "
        "nozzle_diameter[0]==0.4`, with no `nozzle_high_flow` clause, so it is a valid choice on the HF0.4 "
        "printer. The alternative, `0.20mm BALANCED @COREONE HF0.4`, itself inherits from this preset and "
        "then raises perimeter 70->150, external 50->200, small-perimeter 50->170 and drops "
        "`bottom_solid_layers` to 3 - values the override table would immediately undo, except "
        "`small_perimeter_speed`, which we do not override. |",
        f"| filament | `{BASE_FILAMENT}` | HF variant, matching the installed high-flow 0.4 nozzle. "
        "Differs from `Prusament ASA @COREONE` only in the ceiling and the melt: "
        "`filament_max_volumetric_speed` 15 -> 26, `filament_infill_max_crossing_speed` 140 -> 200, "
        "nozzle temp 260 -> 265 C, shorter ramming, COREONE-only start G-code. Shrinkage compensation is "
        "0.22 % in both, so the zeroing override below is unchanged. |",
        f"| printer | `{BASE_PRINTER}` | The high-flow 0.4 preset. `Prusa CORE One 0.4 nozzle` *inherits "
        "from this one* and only sets `nozzle_high_flow = 0` / `printer_variant = 0.4` plus the two "
        "default-profile pointers - bed 250x220, 270 mm Z, retract 0.7 mm @ 45 mm/s and z-hop 0.2 mm are "
        "identical. |",
        "",
        "HF raises the ceiling only. At this build's capped speeds the peak volumetric flow is",
        "`100 mm/s x 0.4 x 0.2 = 8.0 mm3/s` on infill, well under both the 15 and the 26 mm3/s limit,",
        "so the HF base changes the temperature and the start G-code but not the time estimates.",
        "",
        "## Print settings",
        "",
        "| ini key | Flattened preset value | Set to | Why | Doc line |",
        "|---|---|---|---|---|",
        *rows["print"],
        "",
        "## Filament settings",
        "",
        "| ini key | Flattened preset value | Set to | Why | Doc line |",
        "|---|---|---|---|---|",
        *rows["filament"],
        "",
        "## Printer settings",
        "",
        "| ini key | Flattened preset value | Set to | Why | Doc line |",
        "|---|---|---|---|---|",
        *rows["printer"],
        "",
        "## Kept at the preset value on purpose",
        "",
        "These are named in the override table as *keep*, so they are asserted here rather than changed:",
        "",
        "| ini key | Value | Doc line |",
        "|---|---|---|",
    ]
    for key, doc in [
        ("layer_height", "Print row 1"), ("first_layer_height", "Print row 1"),
        ("top_solid_layers", "Print row 3"), ("fill_pattern", "Print row 6"),
        ("first_layer_extrusion_width", "Print row 8"), ("perimeter_generator", "Print row 10"),
        ("top_solid_infill_speed", "Print row 21"), ("external_perimeters_first", "Print row 23"),
        ("enable_dynamic_overhang_speeds", "Print row 24"),
        ("temperature", "Filament row 3 - HF base is 265 C, not the 260 C the non-HF preset gives"),
        ("first_layer_temperature", "Filament row 3 - HF base, 265 C"),
        ("bed_temperature", "Filament row 4"), ("first_layer_bed_temperature", "Filament row 4"),
        ("chamber_temperature", "Filament row 5"), ("chamber_minimal_temperature", "Filament row 6"),
        ("min_fan_speed", "Filament row 7"), ("max_fan_speed", "Filament row 7"),
        ("disable_fan_first_layers", "Filament row 7"),
        ("filament_max_volumetric_speed", "Filament row 8 - HF base is 26, not 15"),
        ("retract_length", "Filament row 9"), ("retract_lift", "Filament row 9"),
        ("bed_shape", "Base profiles"), ("max_print_height", "Base profiles"),
        ("filament_density", "Base profiles - used for the gram numbers"),
    ]:
        out.append(f"| `{key}` | `{black.get(key, '(default)')}` | {doc} |")

    out += [
        "",
        "## Accent bundle",
        "",
        "`slicer/voron-accent-blue.ini` differs from `slicer/voron-coreone-asa.ini` in "
        f"**{len([k for k in black if black[k] != accent.get(k)])} keys only**: "
        + ", ".join(f"`{k}`" for k in sorted(black) if black[k] != accent.get(k))
        + ". Same print, filament and printer physics; colour and label only. Used for the three "
        "B02 plates. Renamed from `voron-accent-orange.ini` on 2026-09-14 when the accent spool "
        "changed from Prusa Orange to blue; the three B02 plate 3MFs carry the new "
        "`filament_settings_id` / `filament_colour` via `sync_start_gcode.py`.",
        "",
        "## What the 2.9.6 CLI could not do, and what was done instead",
        "",
        "Three CLI limits shape `slicer/build_plates.py`. All three were established by running",
        "the installed binary, not from documentation:",
        "",
        "| Limit | Evidence | What the build does instead |",
        "|---|---|---|",
        "| **Arrange is unusable.** | `--merge` plus the default arrange segfaults (exit 139). "
        "Loading an already-merged 3MF and arranging exits 0 but is a no-op: identical parts come "
        "back with identical `<item transform>` values, stacked on each other, and the slice still "
        "succeeds - PrusaSlicer does not refuse overlapping objects. | `slicer/geom.py` packs the "
        "plate (convex-hull footprints, MaxRects with 90 deg rotation, each part inflated by its own "
        "brim plus half the clearance), the meshes are pre-transformed, and every plate is sliced "
        "with `--dont-arrange`. A plate that does not fit aborts with the overflowing parts named. |",
        "| **No per-object settings switch.** | `--help` has no per-object option; every config key "
        "on the command line is global. | Brim is written into the project as per-object "
        "`brim_width` metadata in the 3MF's `Metadata/Slic3r_PE_model.config`, which PrusaSlicer "
        "does honour (verified: a 6 mm brim on a 30 mm cube moved the slice from 15.38 g to 15.54 g "
        "with the global brim at 0). So the named parts get their brim and nothing else on the "
        "plate pays for it. |",
        "| **No thumbnails.** | The `thumbnails` value reaches the G-code config block, but no "
        "image data is written in either ASCII or binary G-code - rasterisation lives in the GUI. | "
        "`scripts/render_plate_bins.py` draws the diagram by reading the committed 3MF back (every "
        "object's mesh projected through its `<item transform>`, per-object brim from "
        "`Slic3r_PE_model.config`), and adds what a screenshot would not carry: a number on every "
        "part, its sorting bin (colour + id, from `slicer/bins.py`) and the brim ring. Re-arranging "
        "a plate in the GUI and saving it is therefore safe \u2014 `build_plates.py --from-3mf` "
        "re-slices and redraws from the file. |",
        "",
        "One more: `--export-3mf` writes model geometry only - no `Metadata/Slic3r_PE.config` - so a",
        "project straight from the CLI would open with whatever presets the reader happens to have",
        "selected. `build_plates.py` injects the config, and then slices each plate **with no",
        "`--load` at all**, so the committed 3MF is proved self-sufficient before its numbers are",
        "recorded.",
        "",
        "## Keeping the committed 3MFs in step with this file",
        "",
        "That self-sufficiency cuts both ways: opening a plate project **overrides the reader's",
        "selected presets** with the config baked into it. So a key added here does not reach the",
        "22 committed plates on its own - `build_plates.py --from-3mf` re-slices them as they are",
        "and never re-injects the config, and a full re-pack would throw away the GUI arrangement",
        "that is the QC authority.",
        "",
        "`python3 slicer/sync_start_gcode.py` closes that gap: it rewrites the single",
        "`; key = value` line inside each plate's `Metadata/Slic3r_PE.config` and copies every",
        "other zip member through byte for byte, so no object transform moves. Run it after",
        "changing a printer- or filament-level key here, then `build_plates.py --from-3mf` and",
        "`check_docs.py`. (`--check` reports without writing; `--key` picks a different key.)",
        "",
        "It matters most for `start_gcode`: the plates were written with the stock CORE One start,",
        "which would push the hot-probe sequence back over the `coldstart` printer preset every",
        "time a project was opened.",
        "",
    ]
    if bay_rows:
        out += bay_overrides_md(bay_rows, version)
    (ROOT / "OVERRIDES.md").write_text("\n".join(out) + "\n")


def main() -> None:
    version = bundle_version(load_bundle())
    black = build("black", "voron-coreone-asa", "#1D1D1F",
                  "Prusament ASA Galaxy Black - primary colour for every batch except B02.")
    blue = build("blue", "voron-accent-blue", "#1F4E9C",
                 "Prusament ASA blue - accent colour, B02 plates only "
                 "(plus Handle.stl, ldo_bestagon_insert.stl and the Igus cable bridge).")
    write_ini(ROOT / "voron-coreone-asa.ini", black, "voron-coreone-asa", version)
    write_ini(ROOT / "voron-accent-blue.ini", blue, "voron-accent-blue", version)
    bay, bay_rows = build_bay()
    write_bay_ini(ROOT / "bay-ducts-petg.ini", bay, version)
    write_overrides_md(black, blue, version, bay_rows)
    diff = [k for k in black if black[k] != blue.get(k)]
    print(f"wrote voron-coreone-asa.ini ({len(black)} keys), "
          f"voron-accent-blue.ini (differs in {len(diff)}: {', '.join(sorted(diff))}), "
          f"bay-ducts-petg.ini ({len(bay)} keys), OVERRIDES.md")


if __name__ == "__main__":
    main()
