#!/usr/bin/env python3
"""Read what is on a plate straight from its committed PrusaSlicer project (`slicer/plates/*.3mf`).

The 3MF is the source of truth for the arrangement: Alex may move or turn parts in the
PrusaSlicer GUI and save, and nothing here depends on how the plate was first packed.

Layout of a PrusaSlicer 3MF, as far as this reader needs it:

  3D/3dmodel.model                 `<object id>` meshes (`<vertex>`, `<triangle>`), optional
                                   `<components>`; `<build><item objectid transform>` instances.
                                   World position = item transform x vertex. The CLI writes the
                                   arranged mesh in world coordinates with an identity transform;
                                   the GUI writes a centred mesh plus a translate/rotate transform.
                                   Both come out the same through `apply()`.
  Metadata/Slic3r_PE_model.config  per-object `name` (the STL basename, `#n` for copies),
                                   per-object settings such as `brim_width`, and each volume's
                                   `source_file`. The volume `matrix` there is PrusaSlicer's own
                                   bookkeeping for the source mesh and is deliberately ignored.

The transform string is the 3MF core spec's 4x3 matrix in row-vector convention,
"m00 m01 m02 m10 m11 m12 m20 m21 m22 m30 m31 m32": x' = x*m00 + y*m10 + z*m20 + m30.
PrusaSlicer writes it column by column of its Eigen matrix, which is the same order.
"""
from __future__ import annotations

import re
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

_OBJECT_RE = re.compile(r'<object id="(\d+)"[^>]*>(.*?)</object>', re.S)
_VERTEX_RE = re.compile(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"')
_TRI_RE = re.compile(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"')
_COMPONENT_RE = re.compile(r'<component objectid="(\d+)"(?: transform="([^"]+)")?')
_ITEM_RE = re.compile(r'<item objectid="(\d+)"(?: transform="([^"]+)")?[^>]*>')
_CFG_OBJECT_RE = re.compile(r'<object id="(\d+)"[^>]*>(.*?)</object>', re.S)
_CFG_META_RE = re.compile(r'<metadata type="object" key="([^"]+)" value="([^"]*)"/>')
_CFG_SOURCE_RE = re.compile(r'<metadata type="volume" key="source_file" value="([^"]*)"/>')

Matrix = tuple[float, ...]  # 12 numbers
IDENTITY: Matrix = (1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)


def parse_transform(s: str | None) -> Matrix:
    if not s:
        return IDENTITY
    m = tuple(float(v) for v in s.split())
    if len(m) != 12:
        raise ValueError(f"bad 3MF transform: {s!r}")
    return m


def apply(m: Matrix, x: float, y: float, z: float) -> tuple[float, float, float]:
    return (x * m[0] + y * m[3] + z * m[6] + m[9],
            x * m[1] + y * m[4] + z * m[7] + m[10],
            x * m[2] + y * m[5] + z * m[8] + m[11])


def compose(outer: Matrix, inner: Matrix) -> Matrix:
    """The matrix that applies `inner` first, then `outer`."""
    # rows of the 3x3 part in row-vector convention
    a = [[outer[0], outer[1], outer[2]], [outer[3], outer[4], outer[5]], [outer[6], outer[7], outer[8]]]
    b = [[inner[0], inner[1], inner[2]], [inner[3], inner[4], inner[5]], [inner[6], inner[7], inner[8]]]
    r = [[sum(b[i][k] * a[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    tx, ty, tz = apply(outer, inner[9], inner[10], inner[11])
    return (r[0][0], r[0][1], r[0][2], r[1][0], r[1][1], r[1][2], r[2][0], r[2][1], r[2][2], tx, ty, tz)


@dataclass
class Mesh:
    vertices: list[tuple[float, float, float]]
    triangles: list[tuple[int, int, int]]
    components: list[tuple[int, Matrix]] = field(default_factory=list)


@dataclass
class PlateObject:
    """One printable instance on the bed, in world millimetres."""
    object_id: int
    name: str                     # PrusaSlicer object name, e.g. "z_drive_main_a_x2.stl#2"
    stl: str                      # source STL basename, e.g. "z_drive_main_a_x2.stl"
    copy: int                     # 1-based copy index from the `#n` suffix (1 if none)
    settings: dict[str, str]      # per-object settings from Slic3r_PE_model.config
    vertices: list[tuple[float, float, float]]
    triangles: list[tuple[int, int, int]]

    @property
    def brim(self) -> float:
        try:
            return float(self.settings.get("brim_width", "0") or 0)
        except ValueError:
            return 0.0

    def bbox(self) -> tuple[float, float, float, float, float, float]:
        xs = [v[0] for v in self.vertices]
        ys = [v[1] for v in self.vertices]
        zs = [v[2] for v in self.vertices]
        return min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)


@dataclass
class Plate:
    path: Path
    objects: list[PlateObject]
    config: dict[str, str]        # Metadata/Slic3r_PE.config, `key = value` lines


def _read_meshes(model_xml: str) -> dict[int, Mesh]:
    meshes: dict[int, Mesh] = {}
    for oid, body in _OBJECT_RE.findall(model_xml):
        verts = [(float(x), float(y), float(z)) for x, y, z in _VERTEX_RE.findall(body)]
        tris = [(int(a), int(b), int(c)) for a, b, c in _TRI_RE.findall(body)]
        comps = [(int(cid), parse_transform(t)) for cid, t in _COMPONENT_RE.findall(body)]
        meshes[int(oid)] = Mesh(verts, tris, comps)
    return meshes


def _flatten(meshes: dict[int, Mesh], oid: int, m: Matrix, depth: int = 0
             ) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int]]]:
    """World-space vertices/triangles of object `oid` under transform `m`, components included."""
    if depth > 8:
        raise ValueError("3MF component nesting too deep")
    mesh = meshes[oid]
    verts = [apply(m, *v) for v in mesh.vertices]
    tris = list(mesh.triangles)
    for cid, ct in mesh.components:
        cv, ctris = _flatten(meshes, cid, compose(m, ct), depth + 1)
        off = len(verts)
        verts.extend(cv)
        tris.extend((a + off, b + off, c + off) for a, b, c in ctris)
    return verts, tris


def _read_config(cfg_xml: str) -> dict[int, tuple[dict[str, str], list[str]]]:
    """object id -> (object metadata, volume source_file list)."""
    out: dict[int, tuple[dict[str, str], list[str]]] = {}
    for oid, body in _CFG_OBJECT_RE.findall(cfg_xml):
        meta = dict(_CFG_META_RE.findall(body))
        out[int(oid)] = (meta, _CFG_SOURCE_RE.findall(body))
    return out


def _stl_from(name: str, sources: list[str], known: set[str] | None) -> tuple[str, int]:
    """(stl basename, copy index) for an object. The object name PrusaSlicer keeps is the
    STL basename with `#n` for repeated copies (build_plates.py names them that way, and the
    GUI names an imported STL by its filename). Fall back to the volume's `source_file`,
    stripped of build_plates.py's `NN_` prefix."""
    base, copy = name, 1
    m = re.match(r"^(.*)#(\d+)$", name)
    if m:
        base, copy = m.group(1), int(m.group(2))
    base = base.rsplit("/", 1)[-1]
    if known is None or base in known:
        return base, copy
    for src in sources:
        cand = re.sub(r"^\d\d_", "", src.rsplit("/", 1)[-1])
        if cand in known:
            return cand, copy
    # an unknown name: keep it, the caller decides what to do with an unassigned part
    return base, copy


def read_plate(path: Path, known_stls: set[str] | None = None) -> Plate:
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        model_xml = z.read("3D/3dmodel.model").decode("utf-8")
        cfg_xml = z.read("Metadata/Slic3r_PE_model.config").decode("utf-8") \
            if "Metadata/Slic3r_PE_model.config" in names else ""
        pe_cfg = z.read("Metadata/Slic3r_PE.config").decode("utf-8") \
            if "Metadata/Slic3r_PE.config" in names else ""

    meshes = _read_meshes(model_xml)
    per_object = _read_config(cfg_xml)
    build = model_xml.split("<build>", 1)[1] if "<build>" in model_xml else ""
    objects: list[PlateObject] = []
    for oid_s, t in _ITEM_RE.findall(build):
        oid = int(oid_s)
        if oid not in meshes:
            raise ValueError(f"{path.name}: item refers to missing object {oid}")
        meta, sources = per_object.get(oid, ({}, []))
        name = meta.get("name") or (sources[0] if sources else f"object-{oid}")
        stl, copy = _stl_from(name, sources, known_stls)
        verts, tris = _flatten(meshes, oid, parse_transform(t))
        settings = {k: v for k, v in meta.items() if k != "name"}
        objects.append(PlateObject(oid, name, stl, copy, settings, verts, tris))

    config = dict(re.findall(r"^; ([A-Za-z_0-9]+) = (.*)$", pe_cfg, re.M))
    return Plate(path, objects, config)


if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        plate = read_plate(Path(arg))
        print(f"{plate.path.name}: {len(plate.objects)} object(s)")
        for o in plate.objects:
            x0, y0, z0, x1, y1, z1 = o.bbox()
            print(f"  {o.name:45s} {o.stl:45s} copy {o.copy}  brim {o.brim:g}  "
                  f"x {x0:6.1f}-{x1:6.1f}  y {y0:6.1f}-{y1:6.1f}  z {z0:5.1f}-{z1:5.1f}  "
                  f"{len(o.triangles)} tris")
