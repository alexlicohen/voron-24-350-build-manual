#!/usr/bin/env python3
"""Committed plates vs tools/platearrange, at gap 3 and gap 6, plus a per-batch bed count.

Read-only on the repo: the committed `slicer/plates/*.3mf` are read (threemf.py), each plate's
parts are arranged with platearrange, and the candidate projects (transform-only copies of
the committed 3MF) go under --out only, with --out/compare.json and a stdout table.

    python3 slicer/arrange_compare.py --out /tmp/arr                 # all plates
    python3 slicer/arrange_compare.py --out /tmp/arr B02-P3 B06-P1   # named plates
    options: --gaps 3,6  --consolidate-gap 3  --no-consolidate  --rot-step 5  --res 0.5
             --large-centre W  (platearrange large_centre: big parts in the middle; 0 = off)

Every number is measured on the geometry read back from a 3MF (the committed one, or the
candidate re-read with threemf.py), with platearrange.measure's exact segment geometry, not
the packer's raster:
  area     part+brim bounding box of the whole plate, cm2
  maxd     largest part-centroid distance from the bed centre, mm (meand: the mean)
  edge     smallest part+brim distance to a bed edge, mm
  gap      smallest part+brim to part+brim distance, mm
  fit      the parts fit one bed (candidates only)
Brim = brim_width + brim_separation (PrusaSlicer's arrange uses the same reach). Edge margin
for candidates = geom.EDGE_MARGIN (skirt room), as for every packer in this repo.

Exit status 1 if any candidate overlaps, leaves the bed, or breaks its gap or edge margin.
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(REPO / "tools" / "platearrange"))

import threemf  # noqa: E402
from geom import EDGE_MARGIN  # noqa: E402
from plates import PLATES  # noqa: E402
from platearrange import Item, arrange_detailed, write_3mf  # noqa: E402
from platearrange.measure import (centroid, edge_clearance, min_gap,  # noqa: E402
                                  part_from_mesh, pile_bbox)

TOL = 1e-6


def _bed(plate) -> tuple:
    pts = []
    for p in plate.config.get("bed_shape", "0x0,250x0,250x220,0x220").split(","):
        a, b = p.split("x")
        pts.append((float(a), float(b)))
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))


def _num(v, default: float = 0.0) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _brim(obj, plate) -> float:
    """Outer brim reach, as PrusaSlicer's arrange counts it: width + separation."""
    width = obj.brim if "brim_width" in obj.settings else _num(plate.config.get("brim_width"))
    btype = obj.settings.get("brim_type", plate.config.get("brim_type", "outer_only"))
    if width <= 0 or btype not in ("outer_only", "outer_and_inner"):
        return 0.0
    return width + _num(obj.settings.get("brim_separation", plate.config.get("brim_separation")))


def load(pid: str):
    return load_path(ROOT / "plates" / f"{pid}.3mf")


def measure(objs, bed, fl) -> dict:
    parts = [part_from_mesh(v, t, b, fl) for _n, v, t, b in objs]
    x0, y0, x1, y1 = pile_bbox(parts)
    cx, cy = (bed[0] + bed[2]) / 2, (bed[1] + bed[3]) / 2
    d = [math.hypot(px - cx, py - cy) for px, py in (centroid(p) for p in parts)]
    gap, pair = min_gap(parts) if len(parts) > 1 else (math.inf, None)
    return dict(area_cm2=(x1 - x0) * (y1 - y0) / 100.0, pile=[x0, y0, x1, y1],
                pile_w=x1 - x0, pile_h=y1 - y0, max_d=max(d), mean_d=sum(d) / len(d),
                edge=edge_clearance(parts, bed),
                gap=None if not math.isfinite(gap) else gap,
                gap_pair=None if pair is None else [objs[pair[0]][0], objs[pair[1]][0]])


def candidate(pid, objs, bed, fl, gap, args, out: Path, failures: list) -> dict:
    items = [Item(id=i, vertices=v, triangles=t, brim=b) for i, (_n, v, t, b) in enumerate(objs)]
    t0 = time.time()
    res = arrange_detailed(items, bed=[(bed[0], bed[1]), (bed[2], bed[1]), (bed[2], bed[3]),
                                       (bed[0], bed[3])],
                           gap=gap, rot_step=args["rot_step"], edge_margin=EDGE_MARGIN,
                           res=args["res"], first_layer=fl, large_centre=args["large_centre"])
    secs = time.time() - t0
    row = dict(beds=res.beds, fits=res.beds == 1, strategy=res.strategy, secs=round(secs, 2),
               rotations={objs[p.item_id][0]: p.rot_deg for p in res.placements})
    if res.beds != 1:
        return row
    dst = out / f"gap{gap:g}" / f"{pid}.3mf"
    write_3mf(ROOT / "plates" / f"{pid}.3mf", dst, res.placements)
    # measure what the written project really holds, read back by the repo's own reader
    _plate, back, _fl = load_path(dst)
    worst = 0.0
    for p, (_n, v, _t, _b), (_n2, v2, _t2, _b2) in zip(res.placements, objs, back):
        want = p.apply(v[:, :2])
        worst = max(worst, float(np.abs(want - v2[:, :2]).max()),
                    float(np.abs(v[:, 2] - v2[:, 2]).max()))
    m = measure(back, bed, fl)
    row.update(m)
    row["transform_error_mm"] = worst
    problems = []
    if m["gap"] is not None and m["gap"] <= TOL:
        problems.append(f"overlap ({m['gap_pair']})")
    elif m["gap"] is not None and m["gap"] < gap - TOL:
        problems.append(f"gap {m['gap']:.3f} < {gap:g} ({m['gap_pair']})")
    if m["edge"] < -TOL:
        problems.append(f"off the bed by {-m['edge']:.3f} mm")
    elif m["edge"] < EDGE_MARGIN - TOL:
        problems.append(f"edge {m['edge']:.3f} < margin {EDGE_MARGIN:g}")
    if worst > 1e-4:
        problems.append(f"3MF round trip off by {worst:.2e} mm")
    if problems:
        failures.append(f"{pid} gap {gap:g}: " + "; ".join(problems))
    row["problems"] = problems
    return row


def load_path(path: Path):
    plate = threemf.read_plate(path)
    fl = float(plate.config.get("first_layer_height", "0.2") or 0.2)
    return plate, [(o.name, np.asarray(o.vertices, dtype=np.float64),
                    np.asarray(o.triangles, dtype=np.int64), _brim(o, plate))
                   for o in plate.objects], fl


def _fmt(r: dict) -> str:
    if r is None or "area_cm2" not in r:
        return f"{'-':>6s} {'-':>5s} {'-':>5s} {'-':>5s} {'-':>5s} {'NO':>3s}"
    gap = "  -  " if r["gap"] is None else f"{r['gap']:5.1f}"
    fit = "" if "fits" not in r else ("yes" if r["fits"] else "NO")
    return f"{r['area_cm2']:6.1f} {r['max_d']:5.1f} {r['mean_d']:5.1f} {r['edge']:5.1f} {gap} {fit:>3s}"


def main(argv) -> int:
    args = dict(rot_step=5.0, res=0.5, gaps=(3.0, 6.0), cgap=3.0, consolidate=True,
                large_centre=0.0)
    out, ids, i = None, [], 0
    while i < len(argv):
        a = argv[i]
        val = None
        if "=" in a and a.startswith("--"):
            a, val = a.split("=", 1)
        def take():
            nonlocal i
            if val is not None:
                return val
            i += 1
            return argv[i]
        if a == "--out":
            out = Path(take())
        elif a == "--gaps":
            args["gaps"] = tuple(float(g) for g in take().split(","))
        elif a == "--consolidate-gap":
            args["cgap"] = float(take())
        elif a == "--no-consolidate":
            args["consolidate"] = False
        elif a == "--rot-step":
            args["rot_step"] = float(take())
        elif a == "--res":
            args["res"] = float(take())
        elif a == "--large-centre":
            args["large_centre"] = float(take())
        elif a in ("-h", "--help"):
            print(__doc__)
            return 0
        elif a.startswith("-"):
            print(f"unknown option {a}", file=sys.stderr)
            return 2
        else:
            ids.append(a)
        i += 1
    if out is None:
        print("--out DIR is required (candidates are never written into the repo)", file=sys.stderr)
        return 2
    out = out.resolve()
    for guarded in (REPO / "slicer", REPO / "docs"):
        if out == guarded or guarded in out.parents:
            print(f"--out must not be inside {guarded}", file=sys.stderr)
            return 2
    unknown = [p for p in ids if p not in PLATES]
    if unknown:
        print(f"unknown plate(s): {', '.join(unknown)}", file=sys.stderr)
        return 2
    ids = ids or list(PLATES)
    out.mkdir(parents=True, exist_ok=True)

    t_all = time.time()
    failures: list = []
    report = dict(params=dict(gaps=list(args["gaps"]), rot_step=args["rot_step"], res=args["res"],
                              edge_margin=EDGE_MARGIN, consolidate_gap=args["cgap"]),
                  plates={}, consolidation=[])
    gl = args["gaps"]
    head = " | ".join(f"{name:^33s}" for name in ["current"] + [f"gap {g:g}" for g in gl])
    sub = " | ".join(f"{'area':>6s} {'maxd':>5s} {'meand':>5s} {'edge':>5s} {'gap':>5s} {'fit':>3s}"
                     for _ in range(1 + len(gl)))
    print(f"{'':6s} {'':3s}   {head}")
    print(f"{'plate':6s} {'n':>3s}   {sub}")
    batches: dict = {}
    for pid in ids:
        batches.setdefault((PLATES[pid]["batch"], PLATES[pid]["colour"]), []).append(pid)
    loaded: dict = {}
    for (batch, colour), pids in batches.items():
        for pid in pids:
            plate, objs, fl = load(pid)
            bed = _bed(plate)
            loaded[pid] = (objs, bed, fl)
            row = dict(parts=len(objs), current=measure(objs, bed, fl))
            for g in sorted(gl, reverse=True):
                row[f"gap{g:g}"] = candidate(pid, objs, bed, fl, g, args, out, failures)
            report["plates"][pid] = row
            cells = [_fmt(row["current"])] + [_fmt(row[f"gap{g:g}"]) for g in gl]
            print(f"{pid:6s} {len(objs):3d}   " + " | ".join(cells), flush=True)

    if args["consolidate"]:
        print(f"\nconsolidation at gap {args['cgap']:g} (all of a batch's parts, one colour, "
              f"first-fit-decreasing over beds)")
        print(f"{'batch':6s} {'colour':6s} {'parts':>5s} {'plates now':>10s} {'beds':>5s} "
              f"{'change':>6s} {'secs':>6s}  strategy")
        all_ids = set(ids)
        for (batch, colour), pids in batches.items():
            group = [p for p in PLATES if PLATES[p]["batch"] == batch
                     and PLATES[p]["colour"] == colour]
            if not set(group) <= all_ids:
                continue  # only whole batches are consolidated
            items, names = [], []
            fls = set()
            bed = None
            for pid in group:
                objs, bed, fl = loaded[pid]
                fls.add(fl)
                for n, v, t, b in objs:
                    items.append(Item(id=len(items), vertices=v, triangles=t, brim=b))
                    names.append(f"{pid}:{n}")
            t0 = time.time()
            res = arrange_detailed(items, bed=[(bed[0], bed[1]), (bed[2], bed[1]),
                                               (bed[2], bed[3]), (bed[0], bed[3])],
                                   gap=args["cgap"], rot_step=args["rot_step"],
                                   edge_margin=EDGE_MARGIN, res=args["res"], first_layer=max(fls),
                                   large_centre=args["large_centre"])
            secs = time.time() - t0
            per_bed: dict = {}
            for p in res.placements:
                per_bed.setdefault(p.bed, []).append(names[p.item_id])
            report["consolidation"].append(dict(
                batch=batch, colour=colour, parts=len(items), plates_now=len(group),
                beds=res.beds, strategy=res.strategy, secs=round(secs, 2),
                piles=[list(q) for q in res.piles], beds_parts=per_bed))
            print(f"{batch:6s} {colour:6s} {len(items):5d} {len(group):10d} {res.beds:5d} "
                  f"{res.beds - len(group):+6d} {secs:6.1f}  {res.strategy}", flush=True)
        now = sum(c["plates_now"] for c in report["consolidation"])
        new = sum(c["beds"] for c in report["consolidation"])
        print(f"{'total':6s} {'':6s} {'':5s} {now:10d} {new:5d} {new - now:+6d}")

    report["runtime_s"] = round(time.time() - t_all, 1)
    report["failures"] = failures
    (out / "compare.json").write_text(json.dumps(report, indent=1, default=float) + "\n")
    print(f"\n{len(ids)} plates, {report['runtime_s']:.0f} s; candidates and compare.json in {out}")
    if failures:
        print("FAILURES:\n  " + "\n  ".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
