"""split_beds / split_3mf: balanced multi-bed splits, overflow repair, pins, 3MF round trip."""
import collections

import pytest

from meshes import box
from platearrange import Item, NoFit, read_3mf, split_3mf, split_beds
from platearrange.__main__ import main
from platearrange.measure import edge_clearance, min_gap, part_from_mesh, placed_part
from test_io3mf import make_project
from test_merge import make_components_project

BED = (150.0, 150.0)
GAP = 6.0


def _check(items, sp, bed=BED, gap=GAP):
    """Every item on exactly one bed; on each bed parts stay on the bed and apart."""
    seen = sorted(i for g in sp.groups for i in g)
    assert seen == list(range(len(items)))
    for grp, res in zip(sp.groups, sp.results):
        assert res.beds == 1 and len(res.placements) == len(grp)
        by_id = {p.item_id: p for p in res.placements}
        parts = []
        for i in grp:
            it, p = items[i], by_id[items[i].id]
            parts.append(placed_part(part_from_mesh(it.vertices, it.triangles, it.brim),
                                     p.rot_deg, p.x, p.y))
        assert edge_clearance(parts, bed) >= -1e-6
        if len(parts) > 1:
            assert min_gap(parts)[0] >= gap - 1e-6


def _items(specs):
    return [Item(id=f"p{k}", vertices=box(w, h)[0], triangles=box(w, h)[1])
            for k, (w, h) in enumerate(specs)]


def test_balanced_split_fits_every_bed():
    items = _items([(60, 50)] * 8)
    sp = split_beds(items, 2, bed=BED, gap=GAP, rot_step=90)
    _check(items, sp)
    assert sorted(len(g) for g in sp.groups) == [4, 4]
    assert sp.moves == []


def test_overflow_moves_a_small_part_off_the_full_bed():
    # LPT gives the 130 mm square bed 0 and deals 30 mm squares to bed 1 until it is heavier,
    # so the 16th square lands next to the big one, where it cannot fit; it must move.
    items = _items([(130, 130)] + [(30, 30)] * 16)
    sp = split_beds(items, 2, bed=BED, gap=GAP, rot_step=90)
    _check(items, sp)
    assert len(sp.moves) == 1 and sp.moves[0][1] == 0
    assert sp.groups[0] == [0]


def test_pins_hold_and_impossible_split_raises():
    items = _items([(60, 50)] * 6)
    sp = split_beds(items, 3, bed=BED, gap=GAP, rot_step=90, pins={4: 0, 5: 0})
    assert {4, 5} <= set(sp.groups[0])
    _check(items, sp)
    with pytest.raises(NoFit):     # three 130 mm squares cannot share two beds
        split_beds(_items([(130, 130)] * 3), 2, bed=BED, gap=GAP, rot_step=90)
    with pytest.raises(ValueError):
        split_beds(items, 7, bed=BED)
    with pytest.raises(ValueError):
        split_beds(items, 2, bed=BED, pins={0: 2})


def test_deterministic():
    items = _items([(60, 50), (40, 40), (70, 20), (30, 30), (50, 25), (20, 80)])
    a = split_beds(items, 2, bed=BED, gap=GAP, rot_step=30)
    b = split_beds(items, 2, bed=BED, gap=GAP, rot_step=30)
    assert a.groups == b.groups
    assert [r.placements for r in a.results] == [r.placements for r in b.results]


def test_split_3mf_round_trip_and_cli(tmp_path):
    p1, p2 = tmp_path / "a.3mf", tmp_path / "b.3mf"
    make_project(p1)
    make_components_project(p2)
    names_in = collections.Counter(it.name.split("#")[0]
                                   for p in (p1, p2) for it in read_3mf(p).items)
    outs = [tmp_path / "s1.3mf", tmp_path / "s2.3mf"]
    sp = split_3mf([p1, p2], outs, gap=GAP, rot_step=90)
    got = [read_3mf(o) for o in outs]
    assert [len(g.items) for g in got] == [len(g) for g in sp.groups]
    assert collections.Counter(it.name.split("#")[0] for g in got for it in g.items) == names_in
    fl = got[0].first_layer_height
    for g in got:   # make_project's bed_shape is 200 x 180
        parts = [part_from_mesh(it.vertices, it.triangles, it.brim, fl) for it in g.items]
        assert edge_clearance(parts, (0, 0, 200, 180)) >= -1e-6
        if len(parts) > 1:
            assert min_gap(parts)[0] >= GAP - 0.05
    with pytest.raises(ValueError):
        split_3mf([p1, p2], [p1, tmp_path / "x.3mf"])
    pattern = str(tmp_path / "cli-{n}.3mf")
    assert main(["split", str(p1), str(p2), "--beds", "2", "-o", pattern,
                 "--rot-step", "90", "--pin", "ell.stl=2"]) == 0
    assert any(it.name.startswith("ell.stl") for it in read_3mf(tmp_path / "cli-2.3mf").items)
    with pytest.raises(SystemExit):     # the output pattern needs {n}
        main(["split", str(p1), "--beds", "2", "-o", str(tmp_path / "no-pattern.3mf")])
