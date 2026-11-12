#!/usr/bin/env python3
"""Audit the committed plate 3MFs against the layout rules, as they are on disk.

The packer enforces these rules when it places parts; nothing else did once a plate was
moved by hand in PrusaSlicer and saved. This reads each `slicer/plates/<id>.3mf` back and
measures it with tools/platearrange (first-layer footprint + brim reach, the same measure
the packer uses):

  edge   every part + brim at least geom.EDGE_MARGIN from every bed edge
  gap    every part + brim at least build_plates.PA_GAP from its neighbour's part + brim
  brim   every part gets at least the brim plates.brim_for asks for (3 mm on every ASA part
         whose footprint is plates.BRIM_MIN_MM or longer; B11's PETG prints brimless)

    python3 slicer/audit_plates.py                # every plate
    python3 slicer/audit_plates.py B03-P1 B07-P2  # named plates
    python3 slicer/audit_plates.py --no-brim      # edge, gap and part list only: needs no
                                                  # source STLs (slicer/stl/ is not in git), so
                                                  # this is the form CI runs

Plates in plates.AS_PRINTED were printed before the current rules and are kept as the record
of what was printed: they are measured and listed, never failed. A plate in plates.EDGE_EXEMPT
(B12-P1, the 212 mm side spool frame) is exempt from the edge rule alone: its edge figure is
measured and listed with the exemption's reason, and its gap and brim rules fail as for any
plate. Exit 1 if any other plate breaks a rule. `build_plates.py --from-3mf` runs this on the plates it re-slices.
Needs numpy (tools/platearrange), so it runs on the interpreter that packs plates, not in
`make verify`'s docs venv: `make audit-plates`.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(REPO / "tools" / "platearrange"))

from geom import BED_X, BED_Y, EDGE_MARGIN  # noqa: E402
from plates import AS_PRINTED, EDGE_EXEMPT, PLATES  # noqa: E402

TOL = 0.05   # mm: a GUI save rounds transforms; the packer's own plates land within this


def audit(plate_id: str, plate_dir: Path | None = None,
          brim: bool = True) -> tuple[dict, list[str]]:
    """Measure one plate. Returns (numbers, rule breaks); the breaks are empty when it passes.
    `brim=False` skips the brim-width rule, the only one that reads the source STLs."""
    import build_plates
    import threemf
    from platearrange.io3mf import read_3mf
    from platearrange.measure import edge_clearance, min_gap, part_from_mesh

    path = (plate_dir or build_plates.OUT_3MF) / f"{plate_id}.3mf"
    project = read_3mf(path)
    fl = project.first_layer_height
    parts = [part_from_mesh(it.vertices, it.triangles, it.brim, fl) for it in project.items]
    names = [it.name for it in project.items]
    bed = (0.0, 0.0, BED_X, BED_Y)

    problems: list[str] = []
    edge, edge_who = math.inf, ""
    for name, part in zip(names, parts):
        e = edge_clearance([part], bed)
        if e < edge:
            edge, edge_who = e, name
        if e < EDGE_MARGIN - TOL:
            problems.append(f"edge: {name} is {e:.2f} mm from the bed edge "
                            f"(rule {EDGE_MARGIN:g})")
    gap, pair = min_gap(parts) if len(parts) > 1 else (math.inf, None)
    if pair is not None and gap < build_plates.PA_GAP - TOL:
        problems.append(f"gap: {names[pair[0]]} to {names[pair[1]]} is {gap:.2f} mm "
                        f"(rule {build_plates.PA_GAP:g})")

    want = (build_plates.expected_brims(plate_id) if brim else
            {Path(path).name: 0.0 for _repo, path, _qty in PLATES[plate_id]["parts"]})
    for obj in threemf.read_plate(path).objects:
        need = want.get(obj.stl)
        if need is None:
            problems.append(f"parts: {obj.stl} is not in plates.py for {plate_id}")
        elif obj.brim < need - 1e-6:
            problems.append(f"brim: {obj.name} has {obj.brim:g} mm (rule {need:g})")
    return dict(edge=edge, edge_part=edge_who, gap=gap, parts=len(parts)), problems


def split_exempt(plate_id: str, problems: list[str]) -> tuple[list[str], list[str]]:
    """(problems that fail the plate, problems an exemption covers): every problem for a plate in
    plates.AS_PRINTED; only the edge rule's for a plate in plates.EDGE_EXEMPT."""
    if plate_id in AS_PRINTED:
        return [], problems
    if plate_id in EDGE_EXEMPT:
        return ([p for p in problems if not p.startswith("edge:")],
                [p for p in problems if p.startswith("edge:")])
    return problems, []


def run(plate_ids: list[str], plate_dir: Path | None = None, brim: bool = True) -> int:
    """Print one line per plate and every rule break; 1 if a plate breaks a rule that no
    exemption covers (plates.AS_PRINTED: every rule; plates.EDGE_EXEMPT: the edge rule)."""
    failed = 0
    for pid in plate_ids:
        m, problems = audit(pid, plate_dir, brim)
        fail, exempt = split_exempt(pid, problems)
        state = ("FAIL" if fail else "as printed" if exempt and pid in AS_PRINTED
                 else "edge exempt" if exempt else "ok")
        gap = "    -" if not math.isfinite(m["gap"]) else f"{m['gap']:5.2f}"
        print(f"audit {pid:8s} edge {m['edge']:6.2f}  gap {gap}  {m['parts']:2d} parts  {state}")
        if pid in EDGE_EXEMPT:
            print(f"    edge rule exempt (plates.EDGE_EXEMPT): {EDGE_EXEMPT[pid]}")
        for p in problems:
            print(f"    {'(exempt) ' if p in exempt else ''}{p}")
        failed += bool(fail)
    if failed:
        print(f"audit: {failed} plate(s) break a layout rule. Move the parts by hand in "
              "PrusaSlicer (never Arrange), save, and re-run with --from-3mf.", file=sys.stderr)
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser(
        allow_abbrev=False,
        description="Audit the committed plate 3MFs against the edge, gap and brim rules.")
    ap.add_argument("plates", nargs="*", metavar="PLATE", help="plate ids (default: every plate)")
    ap.add_argument("--plate-dir", type=Path, help="read the 3MFs from here instead of slicer/plates")
    ap.add_argument("--no-brim", action="store_true",
                    help="skip the brim-width rule (the only one that needs slicer/stl/)")
    a = ap.parse_args()
    unknown = [p for p in a.plates if p not in PLATES]
    if unknown:
        ap.error(f"unknown plate id(s): {', '.join(unknown)}")
    return run(a.plates or list(PLATES), a.plate_dir, brim=not a.no_brim)


if __name__ == "__main__":
    raise SystemExit(main())
