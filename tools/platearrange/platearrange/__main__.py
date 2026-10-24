"""python3 -m platearrange project.3mf -o out.3mf [--gap 6 --rot-step 5 --edge-margin 0
                                                --res 0.5 --report out.json]

Arranges every build item of a PrusaSlicer project on one bed and writes a copy in which
only the items' transforms differ. If the parts need more than one bed, nothing is written:
the report (and stderr) says which part goes on which bed, and the exit status is 3.
"""
from __future__ import annotations

import argparse
import json
import sys
import time

from . import arrange_detailed, read_3mf, write_3mf
from .core import NoFit
from .measure import edge_clearance, min_gap, part_from_mesh, pile_bbox


def _rect(s: str):
    v = [float(x) for x in s.split(",")]
    if len(v) != 4:
        raise argparse.ArgumentTypeError("expected x0,y0,x1,y1")
    return tuple(v)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="platearrange", description=__doc__.split("\n\n")[1])
    ap.add_argument("project", help="PrusaSlicer .3mf project")
    ap.add_argument("-o", "--output", required=True, help="arranged copy to write")
    ap.add_argument("--gap", type=float, default=6.0, help="mm between parts incl. brims (6)")
    ap.add_argument("--rot-step", type=float, default=5.0, help="Z rotation step, degrees (5)")
    ap.add_argument("--edge-margin", type=float, default=0.0, help="mm from the bed edge (0)")
    ap.add_argument("--res", type=float, default=0.5, help="raster cell, mm (0.5)")
    ap.add_argument("--exclude", type=_rect, action="append", default=[],
                    metavar="X0,Y0,X1,Y1", help="bed area to keep clear (repeatable)")
    ap.add_argument("--report", help="write a JSON report here")
    a = ap.parse_args(argv)

    pr = read_3mf(a.project)
    if not pr.items:
        print("no build items in the project", file=sys.stderr)
        return 2
    bed = pr.bed or [(0, 0), (250, 0), (250, 220), (0, 220)]
    try:
        skirts = int(float(pr.config.get("skirts", "0") or 0))
        skirt_d = float(pr.config.get("skirt_distance", "0") or 0)
    except ValueError:
        skirts, skirt_d = 0, 0.0
    if skirts > 0 and a.edge_margin < skirt_d + 0.5 * skirts:
        print(f"note: the project prints {skirts} skirt loop(s) {skirt_d:g} mm out; "
              f"--edge-margin {skirt_d + 0.5 * skirts:g} keeps them on the bed", file=sys.stderr)
    t0 = time.time()
    try:
        res = arrange_detailed(pr.to_items(), bed=bed, gap=a.gap, rot_step=a.rot_step,
                               edge_margin=a.edge_margin, exclusions=a.exclude, res=a.res,
                               first_layer=pr.first_layer_height)
    except NoFit as e:
        print(f"does not fit: {pr.items[e.item_id].name}: {e}", file=sys.stderr)
        return 2
    secs = time.time() - t0
    report = dict(project=str(a.project), output=None, beds=res.beds, strategy=res.strategy,
                  seconds=round(secs, 2), params=res.params,
                  piles=[list(map(float, q)) for q in res.piles],
                  items=[dict(index=it.index, name=it.name, brim=it.brim, bed=p.bed,
                              rot_deg=p.rot_deg, x=p.x, y=p.y)
                         for it, p in zip(pr.items, res.placements)])
    code = 0
    if res.beds > 1:
        print(f"the parts need {res.beds} beds; nothing written (multi-bed 3MF output is "
              f"not supported). Per bed:", file=sys.stderr)
        for b in range(res.beds):
            names = [it.name for it, p in zip(pr.items, res.placements) if p.bed == b]
            print(f"  bed {b + 1}: {', '.join(names)}", file=sys.stderr)
        code = 3
    else:
        write_3mf(a.project, a.output, res.placements)
        back = read_3mf(a.output)
        fl = pr.first_layer_height
        parts = [part_from_mesh(it.vertices, it.triangles, it.brim, fl) for it in back.items]
        xs, ys = [p[0] for p in bed], [p[1] for p in bed]
        gap, _pair = min_gap(parts) if len(parts) > 1 else (float("inf"), None)
        edge = edge_clearance(parts, (min(xs), min(ys), max(xs), max(ys)))
        x0, y0, x1, y1 = pile_bbox(parts)
        report["output"] = str(a.output)
        report["check"] = dict(min_gap=gap if gap != float("inf") else None, edge=edge,
                               pile=[x0, y0, x1, y1])
        print(f"{len(parts)} parts on one bed in {secs:.1f} s ({res.strategy}): pile "
              f"{x1 - x0:.1f} x {y1 - y0:.1f} mm, min gap "
              f"{'-' if gap == float('inf') else f'{gap:.2f}'} mm, edge {edge:.2f} mm -> {a.output}")
    if a.report:
        with open(a.report, "w") as fh:
            json.dump(report, fh, indent=1)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
