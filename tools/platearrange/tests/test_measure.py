import math

from meshes import box, cee
from platearrange.measure import edge_clearance, min_gap, part_from_mesh, placed_part


def test_box_distances():
    a = part_from_mesh(*box(10, 10))
    b = placed_part(part_from_mesh(*box(10, 10)), 0, 13, 4)
    assert abs(min_gap([a, b])[0] - 3.0) < 1e-9
    c = placed_part(part_from_mesh(*box(10, 10)), 0, 13, 14)
    assert abs(min_gap([a, c])[0] - math.hypot(3, 4)) < 1e-9


def test_brims_subtract():
    a = part_from_mesh(*box(10, 10), brim=1.0)
    b = placed_part(part_from_mesh(*box(10, 10), brim=1.5), 0, 15, 0)
    assert abs(min_gap([a, b])[0] - 2.5) < 1e-9


def test_overlap_and_containment_are_zero():
    a = part_from_mesh(*box(20, 20))
    b = placed_part(part_from_mesh(*box(4, 4)), 0, 8, 8)         # inside, no edge crossing
    assert min_gap([a, b])[0] == 0.0
    c = placed_part(part_from_mesh(*box(20, 20)), 45, 15, 0)     # crossing
    assert min_gap([a, c])[0] == 0.0


def test_notch_is_not_filled():
    c = part_from_mesh(*cee(100, 100, 20))
    q = placed_part(part_from_mesh(*box(20, 20)), 0, 50, 40)     # inside the notch
    assert abs(min_gap([c, q])[0] - 20.0) < 1e-9


def test_edge_clearance():
    a = placed_part(part_from_mesh(*box(10, 10), brim=2), 0, 5, 6)
    assert abs(edge_clearance([a], (100, 100)) - 3.0) < 1e-9
    b = placed_part(part_from_mesh(*box(10, 10)), 0, 95, 0)
    assert edge_clearance([b], (100, 100)) < 0


def test_degenerate_triangles_do_not_contain_points():
    import numpy as np
    v, t = box(10, 10)
    # add a vertical sliver whose projection is a single point far away
    v2 = np.vstack([v, [[50, 50, 0], [50, 50, 5], [50, 50, 9]]])
    t2 = np.vstack([t, [[8, 9, 10]]])
    far = placed_part(part_from_mesh(*box(5, 5)), 0, 30, 0)
    d, _ = min_gap([part_from_mesh(v2, t2), far])
    assert abs(d - 20.0) < 1e-9
