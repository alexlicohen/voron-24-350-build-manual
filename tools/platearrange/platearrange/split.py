"""Split parts across a fixed number of beds, each bed arranged on its own.

`arrange_detailed` overflows onto extra beds by filling bed 1 first, so its last bed is
sparse. `split_beds` balances instead: every part gets a load (its first-layer convex hull
grown by brim + gap/2, in mm²), the parts are dealt largest first to the least-loaded bed
(LPT), and each bed is arranged alone with `max_beds=1`. A bed that does not fit hands its
smallest unpinned part to the least-loaded other bed, and the split is tried again.
"""
from __future__ import annotations

import dataclasses
import math
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np

from .core import Item, NoFit, Result, arrange_detailed
from .footprint import clip_below, mesh_triangles


@dataclass
class Split:
    groups: List[List[int]]        # per bed: positions in `items`, ascending
    results: List[Result]          # per bed: placements in group order, all on bed 0
    loads: List[float]             # per bed: summed item loads, mm²
    moves: List[Tuple[int, int, int]] = field(default_factory=list)  # (position, from, to)


def _hull_area_perimeter(xy: np.ndarray) -> Tuple[float, float]:
    pts = np.unique(np.round(np.asarray(xy, dtype=np.float64), 6), axis=0)
    if len(pts) < 3:
        span = float(np.ptp(pts[:, 0]) + np.ptp(pts[:, 1])) if len(pts) else 0.0
        return 0.0, 2.0 * span
    pts = pts[np.lexsort((pts[:, 1], pts[:, 0]))]

    def half(seq):
        h: list = []
        for p in seq:
            while len(h) >= 2 and ((h[-1][0] - h[-2][0]) * (p[1] - h[-2][1])
                                   - (h[-1][1] - h[-2][1]) * (p[0] - h[-2][0])) <= 0:
                h.pop()
            h.append(p)
        return h

    hull = np.array(half(pts)[:-1] + half(pts[::-1])[:-1])
    x, y = hull[:, 0], hull[:, 1]
    area = 0.5 * abs(float(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))))
    per = float(np.sum(np.hypot(np.diff(x, append=x[0]), np.diff(y, append=y[0]))))
    return area, per


def item_load(item: Item, gap: float, first_layer: float = 0.2) -> float:
    """Bed area `item` claims, mm²: the convex hull of its first layer grown by brim + gap/2."""
    tri3 = mesh_triangles(item.vertices, item.triangles)
    low = clip_below(tri3, float(tri3[:, :, 2].min()) + first_layer)
    xy = (low if len(low) else tri3)[:, :, :2].reshape(-1, 2)
    area, per = _hull_area_perimeter(xy)
    c = float(item.brim) + gap / 2.0
    return area + per * c + math.pi * c * c


def split_beds(items: Sequence[Item], beds: int, bed=(250.0, 220.0), gap: float = 6.0,
               rot_step: float = 5.0, edge_margin: float = 0.0, exclusions=(),
               res: float = 0.5, first_layer: float = 0.2, large_centre: float = 0.0,
               pins: Optional[Mapping[int, int]] = None, max_moves: Optional[int] = None,
               **arrange_kw) -> Split:
    """Put `items` on exactly `beds` beds, balanced by load, each bed arranged alone.

    pins       {position in items: bed index} - those parts stay on that bed
    max_moves  overflow repairs before giving up (default: 2 * len(items))
    The other arguments, and any extra keyword, go to `arrange_detailed` for every bed.
    Raises NoFit when no balanced split fits, ValueError on a bad `beds` or pin.
    """
    n = len(items)
    if beds < 1 or beds > n:
        raise ValueError(f"beds must be 1..{n} (one part per bed at least), got {beds}")
    pins = dict(pins or {})
    for i, b in pins.items():
        if not (0 <= i < n and 0 <= b < beds):
            raise ValueError(f"pin {i}->{b} is out of range")
    load = [item_load(it, gap, first_layer) for it in items]
    groups: List[List[int]] = [[] for _ in range(beds)]
    for i in sorted(pins):
        groups[pins[i]].append(i)

    def lightest(exclude=None):
        return min((k for k in range(beds) if k != exclude),
                   key=lambda k: (sum(load[j] for j in groups[k]), k))

    for i in sorted((i for i in range(n) if i not in pins), key=lambda i: (-load[i], i)):
        groups[lightest()].append(i)

    cache: Dict[Tuple[int, ...], Optional[Result]] = {}

    def fit(key: Tuple[int, ...]) -> Optional[Result]:
        if key not in cache:
            try:
                r = arrange_detailed([items[i] for i in key], bed=bed, gap=gap,
                                     rot_step=rot_step, edge_margin=edge_margin,
                                     exclusions=exclusions, res=res, first_layer=first_layer,
                                     large_centre=large_centre, max_beds=1, **arrange_kw)
                cache[key] = r if r.beds == 1 else None
            except NoFit:
                cache[key] = None
        return cache[key]

    moves: List[Tuple[int, int, int]] = []
    seen = set()
    limit = 2 * n if max_moves is None else max_moves
    while True:
        keys = [tuple(sorted(g)) for g in groups]
        state = tuple(keys)
        if state in seen:
            raise NoFit(None, f"no balanced split onto {beds} bed(s): the repairs cycle")
        seen.add(state)
        bad = next((k for k in range(beds) if fit(keys[k]) is None), None)
        if bad is None:
            return Split(groups=[list(k) for k in keys], results=[fit(k) for k in keys],
                         loads=[sum(load[i] for i in k) for k in keys], moves=moves)
        movable = [i for i in groups[bad] if i not in pins]
        if not movable or beds == 1 or len(moves) >= limit:
            raise NoFit(None, f"bed {bad + 1} of {beds} does not fit its parts "
                              f"({len(moves)} repair move(s) tried)")
        mv = min(movable, key=lambda i: (load[i], i))
        to = lightest(exclude=bad)
        groups[bad].remove(mv)
        groups[to].append(mv)
        moves.append((mv, bad, to))


def split_3mf(sources: Sequence, outputs: Sequence, bed=None, gap: float = 6.0,
              pins: Optional[Mapping[int, int]] = None, titles: Optional[Sequence[str]] = None,
              **kw) -> Split:
    """Pool every build item of `sources` and split them onto len(outputs) projects.

    Items are numbered in source order (all of source 0, then source 1, ...); `pins` and the
    returned Split use that numbering. The sources are pooled with `merge_3mf` (duplicate
    names get one `#k` copy index across the pool), then each output takes its items from
    the pool, arranged with `write_3mf`: only build-item transforms change, and the print
    config, brims included, is the first source's. `bed` defaults to the first source's bed_shape. Extra keywords go to
    `split_beds`. Nothing is written unless every bed fits.
    """
    from .io3mf import merge_3mf, read_3mf, write_3mf

    srcs = [Path(s) for s in sources]
    outs = [Path(o) for o in outputs]
    if len({o.resolve() for o in outs}) != len(outs):
        raise ValueError("output paths must be distinct")
    if {o.resolve() for o in outs} & {s.resolve() for s in srcs}:
        raise ValueError("refusing to overwrite a source project")
    with tempfile.TemporaryDirectory() as td:
        # Pool first: the outputs carry the first source's config, so brims (brim_width,
        # brim_separation) must be read under it, not under each item's own source.
        pooled = Path(td) / "pool.3mf"
        merge_3mf(srcs, pooled)
        pr = read_3mf(pooled)
        items = [Item(id=k, vertices=it.vertices, triangles=it.triangles, brim=it.brim)
                 for k, it in enumerate(pr.items)]
        if bed is None:
            bed = pr.bed or [(0, 0), (250, 0), (250, 220), (0, 220)]
        kw.setdefault("first_layer", pr.first_layer_height)
        sp = split_beds(items, len(outs), bed=bed, gap=gap, pins=pins, **kw)
        for b, (grp, res, out) in enumerate(zip(sp.groups, sp.results, outs)):
            merged = Path(td) / f"bed{b}.3mf"
            title = titles[b] if titles else out.stem
            merge_3mf([pooled], merged, select=[(0, pr.items[k].index) for k in grp],
                      title=title)
            by_id = {p.item_id: p for p in res.placements}
            write_3mf(merged, out, [dataclasses.replace(by_id[k], item_id=j, bed=0)
                                    for j, k in enumerate(grp)])
    return sp
