#!/usr/bin/env python3
"""Which bag each sorting bin needs, measured from the STL geometry.

slicer/bins.py stores the answer (`BAG`, one entry per bin) so the build never needs the STLs;
this script derives it from the fetched files (`python3 slicer/fetch_stls.py` first; the two
Nevermore cartridges are measured from the STL that `slicer/build_plates.py` converts them to).

The rule, every number from slicer/bins.py `BAGS` / `BAG_THICK` or below:

  * A bag's usable inside is the paper size it is sold for (A5 148 x 210 mm, B5 176 x 250 mm),
    BAG_THICK (25 mm) deep. A pouch's perimeter is fixed, so a piece thicker than that still
    goes in if every extra millimetre comes off both flat dimensions; nothing over 2 x BAG_THICK.
  * A piece lies flat: it fits when one of its three faces-down orientations (the file's X, Y or
    Z axis up), turned in 1 degree steps, has a footprint inside the bag under that rule.
  * Its packed volume is its smallest bounding box over the same orientations. A bag holds a set
    of pieces when each fits and their packed volumes add up to at most FILL of the bag's
    nominal volume (flat x BAG_THICK): odd shapes in a soft pouch pack to about half of it.
    One piece alone always fits a bag it fits.
  * A bin takes the first that works of: one A5, one B5, two A5, two B5, three A5, three B5
    (fewest bags, A5 first because there are twice as many). A piece that fits no B5, or a bin
    that would need more than three bags, makes the whole bin a box.
  * A bin with fallback parts (slicer/bins.py FALLBACK_PARTS) is sized for the worse of its two
    cases, bins.scenarios(); bought parts (BOUGHT_PARTS) are packed as their nominal box.

    python3 slicer/bin_bags.py          # per-bin table and the totals against the stock
    python3 slicer/bin_bags.py --check  # exit 1 if bins.py BAG disagrees with the geometry
"""
from __future__ import annotations

import argparse
import math
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import bins  # noqa: E402
from geom import convex_hull, read_stl, rotated_extent  # noqa: E402
from plates import local_path  # noqa: E402

STL = ROOT / "stl"
FILL = 0.5
MAX_BAGS = 3
STEP_DEG = 1


@lru_cache(maxsize=None)
def orientations(repo: str, path: str) -> tuple[tuple[float, float, float], ...]:
    """(long, short, thickness) of the footprint for each faces-down orientation and each
    1-degree turn about the vertical, in mm."""
    rel = local_path(repo, path)
    if rel.endswith(".3mf"):
        rel = rel[:-4] + ".stl"     # build_plates.source_stl's PrusaSlicer conversion
    src = STL / rel
    if not src.exists():
        raise SystemExit(f"bin_bags.py: {src.relative_to(ROOT.parent)} missing — run "
                         "python3 slicer/fetch_stls.py (and slicer/build_plates.py for a 3MF)")
    return _orient(frozenset(v for t in read_stl(src) for v in t))


@lru_cache(maxsize=None)
def box_orientations(size: tuple[float, float, float]) -> tuple[tuple[float, float, float], ...]:
    """orientations() of a bought part given as a nominal box (l, w, h) in mm."""
    l, w, h = size
    return _orient(frozenset((x, y, z) for x in (0.0, l) for y in (0.0, w) for z in (0.0, h)))


def _orient(pts) -> tuple[tuple[float, float, float], ...]:
    out = []
    for up in range(3):
        a, b = (i for i in range(3) if i != up)
        zs = [p[up] for p in pts]
        thick = max(zs) - min(zs)
        hull = convex_hull([(p[a], p[b]) for p in pts])
        for deg in range(0, 90, STEP_DEG):
            x0, y0, x1, y1 = rotated_extent(hull, deg)
            w, h = x1 - x0, y1 - y0
            out.append((max(w, h), min(w, h), thick))
    return tuple(out)


def packed_volume(o) -> float:
    """cm³ of the smallest bounding box."""
    return min(l * s * t for l, s, t in o) / 1000.0


def flat(o) -> tuple[float, float, float]:
    """(long, short, thickness) lying on its thinnest side, tightest footprint: what the table reports."""
    return min(o, key=lambda d: (round(d[2], 1), d[0] * d[1]))


def mm(d) -> str:
    return "×".join(f"{x:.0f}" for x in d) + " mm"


def fits(o, bag: str) -> bool:
    w, l = sorted(bins.BAGS[bag]["flat"])
    for long_, short, thick in o:
        extra = max(0.0, thick - bins.BAG_THICK)
        if thick <= 2 * bins.BAG_THICK and short <= w - extra and long_ <= l - extra:
            return True
    return False


def capacity(bag: str) -> float:
    w, l = bins.BAGS[bag]["flat"]
    return FILL * w * l * bins.BAG_THICK / 1000.0


def pack(vols: list[float], bag: str, n: int) -> bool:
    """First-fit decreasing into n bags; a piece alone may exceed the capacity."""
    load = [0.0] * n
    count = [0] * n
    cap = capacity(bag)
    for v in sorted(vols, reverse=True):
        for i in range(n):
            if count[i] == 0 or load[i] + v <= cap:
                load[i] += v
                count[i] += 1
                break
        else:
            return False
    return True


def decide(pieces: list[tuple[str, tuple]]) -> tuple[str, str]:
    """(bag, why) for one bin. `pieces` holds one (name, orientations) per printed copy."""
    vols = [packed_volume(o) for _n, o in pieces]
    total = sum(vols)
    big = max(pieces, key=lambda p: packed_volume(p[1]))
    largest = f"largest {big[0]} {mm(flat(big[1]))}"
    head = f"{len(pieces)} pc, {total:.0f} cm³ packed"
    misfit = sorted({n for n, o in pieces if not fits(o, "B5")})
    if misfit:
        dims = {n: flat(o) for n, o in pieces}
        return "box", f"{head}; fits no bag: " + ", ".join(f"{n} {mm(dims[n])}" for n in misfit)
    for n in range(1, MAX_BAGS + 1):
        for kind in ("A5", "B5"):
            if all(fits(o, kind) for _n, o in pieces) and pack(vols, kind, n):
                why = f"{head} (one {kind} takes {capacity(kind):.0f}); {largest}"
                if kind == "B5" and not all(fits(o, "A5") for _n, o in pieces):
                    why += "; " + ", ".join(sorted({x for x, o in pieces if not fits(o, "A5")})) \
                           + " too big for A5"
                return (kind if n == 1 else f"{kind} ×{n}"), why
    return "box", f"{head}, more than {MAX_BAGS} B5 bags; {largest}"


def piece_list(parts: dict[str, dict]) -> list[tuple[str, tuple]]:
    """One (name, orientations) per piece of a contents() mapping, bought parts as their box."""
    out = []
    for e in parts.values():
        o = box_orientations(tuple(e["size"])) if e["bought"] else orientations(*e["geom"])
        out += [(e["name"].strip("`"), o)] * e["n"]
    return out


def rank(bag: str) -> tuple[int, int]:
    """Order of the rule's options: one A5 < one B5 < two A5 < ... < box."""
    kind, n = bins.bag_parse(bag)
    return (99, 0) if kind == "box" else (n, 0 if kind == "A5" else 1)


def per_bin() -> dict[str, tuple[str, str]]:
    out = {}
    content = bins.contents()
    for b in bins.BINS:
        cases = [piece_list(s) for s in bins.scenarios(content.get(b, {}))]
        decs = [decide(p) for p in cases if p]
        if not decs:
            out[b] = ("A5", "empty")
            continue
        bag, why = max(decs, key=lambda d: rank(d[0]))
        if len(decs) > 1:
            why += f"; worse of {len(decs)} cases (fallback)"
        out[b] = (bag, why)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="fail if bins.py BAG disagrees")
    args = ap.parse_args()
    result = per_bin()
    bad = []
    for b, (bag, why) in result.items():
        stored = bins.BINS[b].get("bag")
        if b in bins.BAG_SPLIT:
            # A split bin may use more bags than the volume minimum (e.g. one per print plate);
            # each of its bags is checked on its own below.
            skind, sn = bins.bag_parse(stored)
            dkind, dn = bins.bag_parse(bag)
            ok = skind == dkind and sn >= dn
        else:
            ok = stored == bag
        flag = "" if ok else f"   <-- bins.py says {stored!r}"
        if not ok:
            bad.append(b)
        if not args.check or not ok:
            print(f"{b:14} {bag:7} {why}{flag}")
    # Every physical container must hold its own share: a bin can fit its bags as a whole while
    # its BAG_SPLIT overfills one of them.
    for c in bins.containers():
        if c["kind"] == "box":
            continue
        for case in bins.scenarios(c["parts"]):
            pieces = [o for _n, o in piece_list(case)]
            vols = [packed_volume(o) for o in pieces]
            if not all(fits(o, c["kind"]) for o in pieces) or not pack(vols, c["kind"], 1):
                bad.append(f"{c['bin']} bag {c['k']}")
                print(f"{c['bin']} bag {c['k']} of {c['of']}: {sum(vols):.0f} cm³ overfills one "
                      f"{c['kind']} ({capacity(c['kind']):.0f} cm³)")
    counts = {"A5": 0, "B5": 0, "box": 0}
    for b in bins.BINS:
        kind, n = bins.bag_parse(bins.BINS[b]["bag"])
        counts[kind] += n
    over = {k: counts[k] - bins.BAGS[k]["owned"] for k in ("A5", "B5")
            if counts[k] > bins.BAGS[k]["owned"]}
    print(f"A5 {counts['A5']} of {bins.BAGS['A5']['owned']}, B5 {counts['B5']} of "
          f"{bins.BAGS['B5']['owned']}, boxes {counts['box']}"
          + (f"; OVER by {over}" if over else ""))
    if bad:
        print(f"bins.py BAG out of date for: {', '.join(bad)}")
    return 1 if (bad and args.check) or over else 0


if __name__ == "__main__":
    sys.exit(main())
