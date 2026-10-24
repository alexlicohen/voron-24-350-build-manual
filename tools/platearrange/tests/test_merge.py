"""merge_3mf: several PrusaSlicer projects -> one, objects renumbered, metadata kept."""
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pytest

from meshes import box
from platearrange import arrange_detailed, merge_3mf, read_3mf, write_3mf
from platearrange.io3mf import MODEL, MODEL_CFG, PRINT_CFG
from test_io3mf import _mesh_xml, make_project

SLICER = Path(__file__).resolve().parents[3] / "slicer"


def make_components_project(path: Path):
    """Object 2 is a mesh used only as a component of object 5 (rotated about X); the item
    names collide with make_project's box.stl, and object 5 carries a per-object brim."""
    v, t = box(20, 10, z=6)
    model = ('<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">\n'
             ' <metadata name="Title">second</metadata>\n <resources>\n'
             + _mesh_xml(2, v, t)
             + ' <object id="5" type="model">\n  <components>\n'
               '   <component objectid="2" transform="1 0 0 0 0 1 0 -1 0 0 0 10"/>\n'
               '  </components>\n </object>\n'
             + _mesh_xml(7, *box(15, 15)) +
             ' </resources>\n <build>\n'
             '  <item objectid="5" transform="1 0 0 0 1 0 0 0 1 50 50 0" printable="1"/>\n'
             '  <item objectid="7" transform="1 0 0 0 1 0 0 0 1 120 40 0" printable="1"/>\n'
             ' </build>\n</model>\n')
    cfg = ('<?xml version="1.0" encoding="UTF-8"?>\n<config>\n'
           ' <object id="5" instances_count="1">\n'
           '  <metadata type="object" key="name" value="box.stl"/>\n'
           '  <metadata type="object" key="brim_width" value="5"/>\n'
           '  <volume firstid="0" lastid="11">\n'
           '   <metadata type="volume" key="source_file" value="01_box.stl"/>\n  </volume>\n'
           ' </object>\n'
           ' <object id="7" instances_count="1">\n'
           '  <metadata type="object" key="name" value="cube.stl"/>\n </object>\n</config>\n')
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("[Content_Types].xml", "<Types/>", compress_type=zipfile.ZIP_DEFLATED)
        z.writestr(MODEL, model, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr(MODEL_CFG, cfg, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr(PRINT_CFG, "; other config\n", compress_type=zipfile.ZIP_DEFLATED)


@pytest.fixture
def two(tmp_path):
    a, b = tmp_path / "a.3mf", tmp_path / "b.3mf"
    make_project(a)
    make_components_project(b)
    return a, b


def _cfg_objects(path):
    with zipfile.ZipFile(path) as z:
        cfg = z.read(MODEL_CFG).decode()
    return {int(i): dict(re.findall(r'key="([^"]+)" value="([^"]*)"', body))
            for i, body in re.findall(r'<object id="(\d+)"[^>]*>(.*?)</object>', cfg, re.S)}


def test_merge_counts_ids_and_metadata(two, tmp_path):
    a, b = two
    dst = tmp_path / "m.3mf"
    src = merge_3mf([a, b], dst, title="M-P1")
    assert src == [(0, 0), (0, 1), (1, 0), (1, 1)]
    pa, pb, pm = read_3mf(a), read_3mf(b), read_3mf(dst)
    assert len(pm.items) == len(pa.items) + len(pb.items) == 4
    with zipfile.ZipFile(dst) as z:
        model = z.read(MODEL).decode()
        names = z.namelist()
        assert z.read(PRINT_CFG) == zipfile.ZipFile(a).read(PRINT_CFG)   # config from source 0
    assert "Metadata/thumbnail.png" not in names
    assert '<metadata name="Title">M-P1</metadata>' in model
    ids = [int(x) for x in re.findall(r'<object id="(\d+)"', model)]
    assert ids == [1, 2, 3, 4, 5]                      # a: 1, 2; b: 2 -> 3, 5 -> 4, 7 -> 5
    assert re.findall(r'<item objectid="(\d+)"', model) == ["1", "2", "4", "5"]
    assert re.findall(r'<component objectid="(\d+)"', model) == ["3"]
    cfg = _cfg_objects(dst)
    # colliding "box.stl" renumbered, per-object brim and volume metadata kept
    assert cfg[1]["name"] == "box.stl#1" and cfg[4]["name"] == "box.stl#2"
    assert cfg[2]["name"] == "ell.stl" and cfg[2]["brim_width"] == "3"
    assert cfg[4]["brim_width"] == "5" and cfg[4]["source_file"] == "01_box.stl"
    assert cfg[5]["name"] == "cube.stl"
    # world geometry and brims unchanged, item for item
    for old, new in zip(pa.items + pb.items, pm.items):
        assert np.array_equal(old.vertices, new.vertices)
        assert old.transform == new.transform
    assert [it.brim for it in pm.items] == [it.brim for it in pa.items] + [
        5 + float(pa.config["brim_separation"]), 0.0]   # sep from the merged (first) config


def test_merge_select_subset_and_arrange(two, tmp_path):
    a, b = two
    dst = tmp_path / "s.3mf"
    merge_3mf([a, b], dst, select=[(1, 0), (0, 1)])
    pm = read_3mf(dst)
    assert len(pm.items) == 2
    with zipfile.ZipFile(dst) as z:
        model = z.read(MODEL).decode()
    # only the objects in use: ell (a:2) -> 1, b's component mesh 2 -> 2, its parent 5 -> 3
    assert re.findall(r'<object id="(\d+)"', model) == ["1", "2", "3"]
    assert re.findall(r'<item objectid="(\d+)"', model) == ["3", "1"]
    assert np.array_equal(pm.items[0].vertices, read_3mf(b).items[0].vertices)
    zext = np.ptp(pm.items[0].vertices[:, 2])
    res = arrange_detailed(pm.to_items(), bed=pm.bed, gap=3, first_layer=pm.first_layer_height)
    assert res.beds == 1
    out = tmp_path / "s-arr.3mf"
    write_3mf(dst, out, res.placements)
    back = read_3mf(out)
    assert abs(np.ptp(back.items[0].vertices[:, 2]) - zext) < 1e-9   # Z rotation only


def test_merge_rejects_bad_input(two, tmp_path):
    a, b = two
    with pytest.raises(ValueError):
        merge_3mf([a, b], a)
    with pytest.raises(ValueError):
        merge_3mf([a, b], tmp_path / "x.3mf", select=[(0, 0), (0, 0)])
    with pytest.raises(ValueError):
        merge_3mf([a], tmp_path / "x.3mf", select=[(0, 9)])


def test_merge_round_trip_threemf(two, tmp_path):
    """The repo's own reader (slicer/threemf.py) sees every object once, with its settings."""
    if not (SLICER / "threemf.py").exists():
        pytest.skip("slicer/threemf.py not in this checkout")
    sys.path.insert(0, str(SLICER))
    import threemf
    a, b = two
    dst = tmp_path / "m.3mf"
    merge_3mf([a, b], dst)
    plates = [threemf.read_plate(p) for p in (a, b)]
    merged = threemf.read_plate(dst)
    old = [o for p in plates for o in p.objects]
    assert len(merged.objects) == len(old) == 4
    assert [o.stl for o in merged.objects] == [o.stl for o in old]
    assert [o.copy for o in merged.objects] == [1, 1, 2, 1]
    assert [o.settings for o in merged.objects] == [o.settings for o in old]
    for o, n in zip(old, merged.objects):
        assert np.allclose(o.vertices, n.vertices) and o.triangles == n.triangles
