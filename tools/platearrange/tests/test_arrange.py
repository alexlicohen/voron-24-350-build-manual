import math

import numpy as np
import pytest

from meshes import box, boxes, cee, ell
from platearrange import Item, NoFit, Placement, arrange, arrange_detailed, clear_cache
from platearrange.footprint import Kernels, MeshFootprints, mesh_triangles
from platearrange.measure import edge_clearance, min_gap, part_from_mesh, placed_part


# ---------------------------------------------------------------- independent check
# Pure-python polygon geometry, sharing nothing with the package: the parts here are
# boxes, so each placed footprint is a rotated rectangle given by its four corners.

def _seg_dist(p, q, a, b):
    def pt(px, py, ax, ay, bx, by):
        dx, dy = bx - ax, by - ay
        L = dx * dx + dy * dy
        t = 0.0 if L == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L))
        return math.hypot(px - ax - t * dx, py - ay - t * dy)

    def orient(o, u, v):
        return (u[0] - o[0]) * (v[1] - o[1]) - (u[1] - o[1]) * (v[0] - o[0])
    d1, d2 = orient(p, q, a), orient(p, q, b)
    d3, d4 = orient(a, b, p), orient(a, b, q)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return 0.0
    return min(pt(*p, *a, *b), pt(*q, *a, *b), pt(*a, *p, *q), pt(*b, *p, *q))


def _inside(pt, poly):
    s = [((b[0] - a[0]) * (pt[1] - a[1]) - (b[1] - a[1]) * (pt[0] - a[0]))
         for a, b in zip(poly, poly[1:] + poly[:1])]
    return all(v >= 0 for v in s) or all(v <= 0 for v in s)


def _poly_dist(P, Q):
    if _inside(P[0], Q) or _inside(Q[0], P):
        return 0.0
    return min(_seg_dist(P[i], P[(i + 1) % 4], Q[j], Q[(j + 1) % 4])
               for i in range(4) for j in range(4))


def _corners(w, h, pl: Placement):
    c, s = math.cos(math.radians(pl.rot_deg)), math.sin(math.radians(pl.rot_deg))
    return [(c * x - s * y + pl.x, s * x + c * y + pl.y) for x, y in ((0, 0), (w, 0), (w, h), (0, h))]


def _check_boxes(sizes, brims, pls, gap, bed, margin):
    rects = [_corners(w, h, pl) for (w, h), pl in zip(sizes, pls)]
    for i in range(len(rects)):
        xs = [p[0] for p in rects[i]]
        ys = [p[1] for p in rects[i]]
        b = brims[i]
        assert min(xs) - b >= margin - 1e-6 and min(ys) - b >= margin - 1e-6
        assert max(xs) + b <= bed[0] - margin + 1e-6 and max(ys) + b <= bed[1] - margin + 1e-6
        for j in range(i + 1, len(rects)):
            if pls[i].bed != pls[j].bed:
                continue
            d = _poly_dist(rects[i], rects[j])
            assert d >= gap + brims[i] + brims[j] - 1e-6, (i, j, d)


# ---------------------------------------------------------------- tests

def test_no_overlap_and_on_bed_independent():
    sizes = [(60, 40), (50, 50), (90, 20), (30, 30), (25, 70), (40, 15), (15, 15), (70, 35)]
    brims = [0, 3, 0, 5, 0, 2, 0, 0]
    items = [Item(i, *box(w, h, x0=100 * i, y0=-7 * i), brim=b)
             for i, ((w, h), b) in enumerate(zip(sizes, brims))]
    bed, gap, margin = (250, 220), 6.0, 2.0
    res = arrange_detailed(items, bed=bed, gap=gap, edge_margin=margin)
    assert res.beds == 1
    # placements are relative to the item frame the vertices were given in
    shifted = [Placement(p.item_id, p.bed, p.rot_deg,
                         *Placement(0, 0, p.rot_deg, p.x, p.y).apply(np.array([100.0 * i, -7.0 * i])))
               for i, p in enumerate(res.placements)]
    _check_boxes(sizes, brims, shifted, gap, bed, margin)


def test_no_overlap_concave_and_brims_exact():
    meshes = [cee(), ell(), box(30, 30), ell(50, 60, 12), box(20, 80), box(18, 18)]
    brims = [0.0, 3.0, 5.0, 0.0, 0.0, 2.0]
    items = [Item(i, v, t, brim=b) for i, ((v, t), b) in enumerate(zip(meshes, brims))]
    res = arrange_detailed(items, bed=(250, 220), gap=4.0, edge_margin=3.0)
    assert res.beds == 1
    parts = [placed_part(part_from_mesh(v, t, b), p.rot_deg, p.x, p.y)
             for (v, t), b, p in zip(meshes, brims, res.placements)]
    gap, pair = min_gap(parts)
    assert gap >= 4.0 - 1e-6, (gap, pair)
    assert edge_clearance(parts, (250, 220)) >= 3.0 - 1e-6


def test_rotation_exact_90_when_needed():
    v, t = box(230, 20)
    pl = arrange([Item("bar", v, t)], bed=(60, 250), gap=6, rot_step=5)[0]
    assert pl.rot_deg in (90.0, 270.0)
    xy = pl.apply(v[:, :2])
    assert xy[:, 0].min() >= -1e-9 and xy[:, 0].max() <= 60 + 1e-9
    assert xy[:, 1].min() >= -1e-9 and xy[:, 1].max() <= 250 + 1e-9


def test_rotation_set_and_apply():
    from platearrange.footprint import rotation_set
    rs = rotation_set(5)
    assert len(rs) == 72 and 90.0 in rs and 270.0 in rs
    assert 90.0 in rotation_set(7) and 180.0 in rotation_set(7)
    p = Placement(0, 0, 30.0, 10.0, -5.0)
    got = p.apply(np.array([[2.0, 1.0]]))[0]
    c, s = math.cos(math.radians(30)), math.sin(math.radians(30))
    assert np.allclose(got, [c * 2 - s * 1 + 10, s * 2 + c * 1 - 5])
    # 90 is exact, not 6e-17 off
    assert tuple(Placement(0, 0, 90.0, 0, 0).apply(np.array([1.0, 0.0]))) == (0.0, 1.0)


def test_rotation_footprint_matches_rotated_mesh():
    """Each rotation's raster covers the exactly rotated outline (conservative)."""
    v, t = ell(70, 40, 10)
    fp = MeshFootprints(mesh_triangles(v, t), [0.0, 35.0, 90.0, 215.0], 0.5, 0.2)
    for r, deg in enumerate(fp.rotations):
        c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        m, (i0, j0) = fp.sil_masks[r], fp.sil_org[r]
        # sample points inside the L, rotate them, they must land in set cells
        rng = np.random.RandomState(0)
        pts = np.vstack([np.c_[rng.uniform(0, 70, 400), rng.uniform(0, 10, 400)],
                         np.c_[rng.uniform(0, 10, 400), rng.uniform(0, 40, 400)]])
        rx = c * pts[:, 0] - s * pts[:, 1] + fp.phase[r][0]
        ry = s * pts[:, 0] + c * pts[:, 1] + fp.phase[r][1]
        ci = np.floor(rx / 0.5).astype(int) - i0
        cj = np.floor(ry / 0.5).astype(int) - j0
        assert m[cj, ci].all()
        # and the raster is not much bigger than the part (area within 25 %)
        assert m.sum() * 0.25 < (70 * 10 + 10 * 30) * 1.25 + 60
    # grid-aligned box at 0 deg costs exactly w/res x h/res cells
    fb = MeshFootprints(mesh_triangles(*box(120, 100)), [0.0], 0.5, 0.2)
    assert fb.sil_masks[0].shape == (200, 240) and fb.sil_masks[0].all()


def test_small_part_goes_into_the_notch():
    cv, ct = cee(100, 100, 20)
    sv, st = box(20, 20)
    res = arrange_detailed([Item("C", cv, ct), Item("cube", sv, st)], bed=(170, 170), gap=6)
    pc, pq = res.placements
    c = pc.apply(cv[:, :2])
    q = pq.apply(sv[:, :2])
    assert res.beds == 1
    assert q[:, 0].min() >= c[:, 0].min() and q[:, 0].max() <= c[:, 0].max()
    assert q[:, 1].min() >= c[:, 1].min() and q[:, 1].max() <= c[:, 1].max()
    parts = [placed_part(part_from_mesh(cv, ct), pc.rot_deg, pc.x, pc.y),
             placed_part(part_from_mesh(sv, st), pq.rot_deg, pq.x, pq.y)]
    assert min_gap(parts)[0] >= 6 - 1e-6


@pytest.mark.parametrize("brim", [0.0, 4.0])
def test_single_part_centred(brim):
    v, t = box(50, 30, x0=-200, y0=37)
    pl = arrange([Item(0, v, t, brim=brim)], bed=(250, 220), gap=6)[0]
    xy = pl.apply(v[:, :2])
    assert abs((xy[:, 0].min() + xy[:, 0].max()) / 2 - 125) < 1e-6
    assert abs((xy[:, 1].min() + xy[:, 1].max()) / 2 - 110) < 1e-6


def test_deterministic():
    meshes = [cee(), ell(), box(30, 30), box(30, 30), box(45, 12), ell(40, 30, 8)]
    items = [Item(i, v, t, brim=1.0 * (i % 2)) for i, (v, t) in enumerate(meshes)]
    a = arrange(items, bed=(250, 220), gap=6)
    clear_cache()
    b = arrange(items, bed=(250, 220), gap=6)
    assert a == b


def test_overflow_to_second_bed():
    v, t = box(120, 100)
    four = arrange_detailed([Item(i, v, t) for i in range(4)], bed=(250, 220), gap=6)
    assert four.beds == 1
    five = arrange_detailed([Item(i, v, t) for i in range(5)], bed=(250, 220), gap=6)
    assert five.beds == 2
    assert {p.bed for p in five.placements} == {0, 1}
    _check_boxes([(120, 100)] * 5, [0] * 5, five.placements, 6, (250, 220), 0)
    with pytest.raises(NoFit):
        arrange_detailed([Item(i, v, t) for i in range(5)], bed=(250, 220), gap=6, max_beds=1)


def test_too_large_raises():
    v, t = box(300, 300)
    with pytest.raises(NoFit):
        arrange([Item("big", v, t)], bed=(250, 220))


def test_exclusion_zone_respected():
    v, t = box(40, 40)
    excl = (100, 80, 150, 140)
    res = arrange_detailed([Item(i, v, t) for i in range(3)], bed=(250, 220), gap=6,
                           exclusions=[excl])
    for p in res.placements:
        xy = p.apply(v[:, :2])
        x0, y0 = xy.min(axis=0)
        x1, y1 = xy.max(axis=0)
        dx = max(0.0, excl[0] - x1, x0 - excl[2])
        dy = max(0.0, excl[1] - y1, y0 - excl[3])
        assert math.hypot(dx, dy) >= 3.0 - 1e-6


def test_polygon_bed():
    bed = [(0, 0), (200, 0), (200, 100), (100, 200), (0, 200)]   # one corner cut off
    v, t = box(60, 60)
    res = arrange_detailed([Item(i, v, t, brim=2.0) for i in range(4)], bed=bed, gap=6,
                           edge_margin=1.0)
    assert res.beds == 1
    for p in res.placements:
        for x, y in p.apply(v[:, :2]):
            assert -1e-9 <= x <= 200 and -1e-9 <= y <= 200
            assert x + y <= 300 - (2.0 + 1.0) * math.sqrt(2) + 1e-6   # brim + margin off the cut


def test_first_layer_brim_only_around_the_base():
    # mushroom: 10 x 10 stem, 40 x 40 cap from z 20; a 5 mm brim reaches 5 mm round the stem
    v, t = boxes((15, 15, 25, 25, 0, 20), (0, 0, 40, 40, 20, 25))
    fp = MeshFootprints(mesh_triangles(v, t), [0.0], 0.5, 0.2)
    k = Kernels(fp, gap=2.0, brim=5.0, need_brim_mask=False)
    x0, y0, x1, y1 = k.ext[0]
    assert abs(x1 - x0 - 40) < 1e-9 and abs(y1 - y0 - 40) < 1e-9   # the cap, not cap + 5
    two = arrange_detailed([Item(i, v, t, brim=5.0) for i in range(2)], bed=(200, 100), gap=2.0)
    parts = [placed_part(part_from_mesh(v, t, 5.0), p.rot_deg, p.x, p.y) for p in two.placements]
    d, _ = min_gap(parts)
    assert 2.0 - 1e-6 <= d < 2.0 + 3.0   # caps nest at the gap, not gap + 2 brims


def _big_and_small():
    sizes = [(150, 60), (120, 30)] + [(22, 18)] * 28
    brims = [3, 3] + [0] * 28
    items = [Item(i, *box(w, h), brim=b) for i, ((w, h), b) in enumerate(zip(sizes, brims))]
    return sizes, brims, items


def _centre_dist(w, h, pl: Placement, bed):
    xs, ys = zip(*_corners(w, h, pl))
    return math.hypot((min(xs) + max(xs)) / 2 - bed[0] / 2, (min(ys) + max(ys)) / 2 - bed[1] / 2)


def test_large_centre_puts_the_big_parts_in_the_middle():
    sizes, brims, items = _big_and_small()
    bed, gap, margin = (250, 220), 6.0, 4.0
    plain = arrange_detailed(items, bed=bed, gap=gap, edge_margin=margin)
    lc = arrange_detailed(items, bed=bed, gap=gap, edge_margin=margin, large_centre=1.0)
    assert plain.beds == lc.beds == 1
    _check_boxes(sizes, brims, lc.placements, gap, bed, margin)     # independent geometry
    d_plain = [_centre_dist(*sizes[i], plain.placements[i], bed) for i in (0, 1)]
    d_lc = [_centre_dist(*sizes[i], lc.placements[i], bed) for i in (0, 1)]
    assert d_lc[0] <= 15.0, d_lc                    # the largest part sits on the bed centre
    assert d_lc[0] <= d_plain[0] + 1e-6, (d_lc, d_plain)
    assert lc.params["large_centre"] == 1.0


def test_large_centre_deterministic_and_off_by_default():
    sizes, brims, items = _big_and_small()
    a = arrange_detailed(items, gap=6.0, edge_margin=4.0, large_centre=1.0)
    clear_cache()
    b = arrange_detailed(items, gap=6.0, edge_margin=4.0, large_centre=1.0)
    assert a.placements == b.placements and a.strategy == b.strategy
    plain = arrange_detailed(items, gap=6.0, edge_margin=4.0)
    assert "anchored" not in plain.strategy and not plain.strategy.startswith("ring")
