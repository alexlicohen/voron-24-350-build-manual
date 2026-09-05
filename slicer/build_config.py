#!/usr/bin/env python3
"""Generate the PrusaSlicer `--load` config bundles and OVERRIDES.md.

Base values come from the PrusaResearch.ini that ships with the installed
PrusaSlicer 2.9.6, with `inherits` resolved (see resolve_preset.py), so the
committed .ini is provably the system preset plus this build's overrides and
nothing else.

    python3 slicer/build_config.py
"""
from __future__ import annotations

from pathlib import Path

from resolve_preset import load_bundle, resolve

ROOT = Path(__file__).resolve().parent
DOC = "docs/manual/print/00-slicer-setup.md"

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
]

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


def write_overrides_md(black: dict[str, str], orange: dict[str, str], version: str) -> None:
    sections = load_bundle()
    base = {}
    base.update(resolve(sections, "print", BASE_PRINT))
    base.update(resolve(sections, "filament", BASE_FILAMENT))
    base.update(resolve(sections, "printer", BASE_PRINTER))

    rows = {"print": [], "filament": [], "printer": []}
    for key, value, sec, why, src in OVERRIDES:
        before = base.get(key, "*(PrusaSlicer built-in default)*")
        if len(before) > 60:
            before = before[:57] + "..."
        changed = "" if str(before) == value else " "
        rows[sec].append(f"| `{key}` | `{before}`{changed} | `{value}` | {why} | {src} |")

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
        "`slicer/voron-accent-orange.ini` differs from `slicer/voron-coreone-asa.ini` in "
        f"**{len([k for k in black if black[k] != orange.get(k)])} keys only**: "
        + ", ".join(f"`{k}`" for k in sorted(black) if black[k] != orange.get(k))
        + ". Same print, filament and printer physics; colour and label only. Used for the three "
        "B02 plates.",
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
        "`slicer/render_plate.py` draws the preview from the same arrangement that goes into the "
        "3MF, and adds a numbered part index and the brim outline, which a screenshot would not "
        "have carried. |",
        "",
        "One more: `--export-3mf` writes model geometry only - no `Metadata/Slic3r_PE.config` - so a",
        "project straight from the CLI would open with whatever presets the reader happens to have",
        "selected. `build_plates.py` injects the config, and then slices each plate **with no",
        "`--load` at all**, so the committed 3MF is proved self-sufficient before its numbers are",
        "recorded.",
        "",
    ]
    (ROOT / "OVERRIDES.md").write_text("\n".join(out) + "\n")


def main() -> None:
    version = bundle_version(load_bundle())
    black = build("black", "voron-coreone-asa", "#1D1D1F",
                  "Prusament ASA Galaxy Black - primary colour for every batch except B02.")
    orange = build("orange", "voron-accent-orange", "#FF6A13",
                   "Prusament ASA Prusa Orange - accent colour, B02 plates only "
                   "(plus Handle.stl, ldo_bestagon_insert.stl and the Igus cable bridge).")
    write_ini(ROOT / "voron-coreone-asa.ini", black, "voron-coreone-asa", version)
    write_ini(ROOT / "voron-accent-orange.ini", orange, "voron-accent-orange", version)
    write_overrides_md(black, orange, version)
    diff = [k for k in black if black[k] != orange.get(k)]
    print(f"wrote voron-coreone-asa.ini ({len(black)} keys), "
          f"voron-accent-orange.ini (differs in {len(diff)}: {', '.join(sorted(diff))}), "
          f"OVERRIDES.md")


if __name__ == "__main__":
    main()
