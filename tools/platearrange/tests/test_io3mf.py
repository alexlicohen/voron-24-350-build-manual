import json
import subprocess
import sys
import zipfile
from pathlib import Path

import numpy as np

from meshes import box, ell
from platearrange import arrange_detailed, read_3mf, write_3mf
from platearrange.io3mf import MODEL

PKG = Path(__file__).resolve().parents[1]


def _mesh_xml(oid, v, t):
    vs = "".join(f'<vertex x="{x:g}" y="{y:g}" z="{z:g}"/>' for x, y, z in v)
    ts = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in t)
    return (f' <object id="{oid}" type="model">\n  <mesh>\n   <vertices>{vs}</vertices>\n'
            f'   <triangles>{ts}</triangles>\n  </mesh>\n </object>\n')


def make_project(path: Path):
    v1, t1 = box(40, 30)
    v2, t2 = ell(60, 50, 15)
    model = ('<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
             'xmlns:slic3rpe="http://schemas.slic3r.org/3mf/2017/06">\n'
             ' <metadata name="Title">t</metadata>\n <resources>\n'
             + _mesh_xml(1, v1, t1) + _mesh_xml(2, v2, t2) +
             ' </resources>\n <build>\n'
             '  <item objectid="1" transform="1 0 0 0 1 0 0 0 1 10 20 0" printable="1"/>\n'
             '  <item objectid="2" transform="0 1 0 -1 0 0 0 0 1 150 30 0" printable="1"/>\n'
             ' </build>\n</model>\n')
    model_cfg = ('<?xml version="1.0" encoding="UTF-8"?>\n<config>\n'
                 ' <object id="1" instances_count="1">\n'
                 '  <metadata type="object" key="name" value="box.stl"/>\n </object>\n'
                 ' <object id="2" instances_count="1">\n'
                 '  <metadata type="object" key="brim_width" value="3"/>\n'
                 '  <metadata type="object" key="name" value="ell.stl"/>\n </object>\n</config>\n')
    cfg = ("; generated\n; bed_shape = 0x0,200x0,200x180,0x180\n; brim_separation = 0.1\n"
           "; brim_type = outer_only\n; brim_width = 0\n; first_layer_height = 0.2\n")
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("[Content_Types].xml", "<Types/>", compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("_rels/.rels", "<Relationships/>", compress_type=zipfile.ZIP_STORED)
        z.writestr(MODEL, model, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("Metadata/Slic3r_PE_model.config", model_cfg, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("Metadata/Slic3r_PE.config", cfg, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("Metadata/thumbnail.png", bytes(range(256)) * 4, compress_type=zipfile.ZIP_STORED)


def test_read(tmp_path):
    src = tmp_path / "p.3mf"
    make_project(src)
    pr = read_3mf(src)
    assert [it.name for it in pr.items] == ["box.stl", "ell.stl"]
    assert pr.items[0].brim == 0.0 and abs(pr.items[1].brim - 3.1) < 1e-12
    assert pr.bed == [(0, 0), (200, 0), (200, 180), (0, 180)]
    v = pr.items[0].vertices
    assert np.allclose(v[:, :2].min(axis=0), [10, 20])
    v = pr.items[1].vertices        # 90 deg about Z, then (150, 30)
    assert np.allclose(v[:, :2].min(axis=0), [150 - 50, 30])


def test_round_trip_only_transforms_change(tmp_path):
    src, dst = tmp_path / "p.3mf", tmp_path / "out.3mf"
    make_project(src)
    pr = read_3mf(src)
    res = arrange_detailed(pr.to_items(), bed=pr.bed, gap=6, first_layer=pr.first_layer_height)
    assert res.beds == 1
    write_3mf(src, dst, res.placements)
    with zipfile.ZipFile(src) as a, zipfile.ZipFile(dst) as b:
        ia, ib = a.infolist(), b.infolist()
        assert [i.filename for i in ia] == [i.filename for i in ib]
        for x, y in zip(ia, ib):
            assert x.compress_type == y.compress_type and x.date_time == y.date_time
            if x.filename != MODEL:
                assert a.read(x) == b.read(y), x.filename
        ma, mb = a.read(MODEL).decode(), b.read(MODEL).decode()
    cut = ma.index("<build")
    assert ma[:cut] == mb[:mb.index("<build")]
    assert ma[ma.index("</build>"):] == mb[mb.index("</build>"):]
    import re
    strip = lambda s: re.sub(r'transform="[^"]*"', "", s[s.index("<build"):])
    assert strip(ma) == strip(mb)
    back = read_3mf(dst)
    for it, nb, p in zip(pr.items, back.items, res.placements):
        assert np.allclose(p.apply(it.vertices[:, :2]), nb.vertices[:, :2], atol=1e-6)
        assert np.allclose(it.vertices[:, 2], nb.vertices[:, 2], atol=1e-9)   # Z untouched


def test_cli(tmp_path):
    src, dst, rep = tmp_path / "p.3mf", tmp_path / "o.3mf", tmp_path / "r.json"
    make_project(src)
    r = subprocess.run([sys.executable, "-m", "platearrange", str(src), "-o", str(dst),
                        "--gap", "6", "--rot-step", "15", "--report", str(rep)],
                       cwd=PKG, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    data = json.loads(rep.read_text())
    assert data["beds"] == 1 and len(data["items"]) == 2
    assert data["check"]["min_gap"] >= 6 - 1e-6 and data["check"]["edge"] >= -1e-6
    assert dst.exists()
