"""PrusaSlicer 3MF projects: read build items, write a copy with new item transforms only.

Read
  3D/3dmodel.model                 <object> meshes and <components>, <build><item> instances.
                                   World = item transform x component transforms x vertex.
  Metadata/Slic3r_PE_model.config  per-object `brim_width`, `brim_type`, `brim_separation`,
                                   object `name` (keyed by the model's object id).
  Metadata/Slic3r_PE.config        `; key = value` print/printer config: bed_shape, brim_*,
                                   first_layer_height, skirts, skirt_distance.

Write
  Only the `transform` attribute of each <item> changes (or is added): the new transform is
  Translate(x, y) . RotZ(rot) . old. Every other byte of 3dmodel.model and every other zip
  member is copied unchanged (same name, order, date and compression method).

Merge (`merge_3mf`)
  Concatenates the build items of several projects into one. Objects are renumbered 1..n in
  source order, consistently in 3dmodel.model (<object id>, <component objectid>, <item
  objectid>) and Slic3r_PE_model.config (<object id>). Each object keeps its mesh, item
  transform and attributes, name, volumes and per-object settings (brim_width, ...). The
  print config and every other member come from one source (`config_from`, default the
  first); thumbnails are dropped, since they would show only that source's parts.

Transforms are the 3MF core 4x3 matrix in row-vector order "m00 m01 m02 m10 m11 m12 m20 m21
m22 m30 m31 m32": x' = x*m00 + y*m10 + z*m20 + m30.
"""
from __future__ import annotations

import re
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from .core import Item, Placement
from .footprint import rot_cs

MODEL = "3D/3dmodel.model"
MODEL_CFG = "Metadata/Slic3r_PE_model.config"
PRINT_CFG = "Metadata/Slic3r_PE.config"

_OBJECT_RE = re.compile(r'<object\b([^>]*)>(.*?)</object>', re.S)
_ATTR_RE = re.compile(r'([A-Za-z_][\w:.-]*)\s*=\s*"([^"]*)"')
_VERTEX_FAST = re.compile(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"')
_VERTEX_ANY = re.compile(r'<vertex\b([^>]*)/?>')
_TRI_FAST = re.compile(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"')
_TRI_ANY = re.compile(r'<triangle\b([^>]*)/?>')
_COMPONENT_RE = re.compile(r'<component\b([^>]*)/?>')
_ITEM_RE = re.compile(r'<item\b[^>]*?/?>')
_CFG_OBJECT_RE = re.compile(r'<object id="(\d+)"[^>]*>(.*?)</object>', re.S)
_CFG_META_RE = re.compile(r'<metadata type="object" key="([^"]+)" value="([^"]*)"\s*/>')

IDENTITY = (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0)


def _attrs(s: str) -> Dict[str, str]:
    return dict(_ATTR_RE.findall(s))


def parse_transform(s: Optional[str]) -> Tuple[float, ...]:
    if not s:
        return IDENTITY
    m = tuple(float(v) for v in s.split())
    if len(m) != 12:
        raise ValueError(f"bad 3MF transform {s!r}")
    return m


def to_matrix(t: Sequence[float]) -> np.ndarray:
    """3MF 12-tuple -> 4x4 column-vector matrix."""
    m = np.eye(4)
    m[0, :3] = t[0], t[3], t[6]
    m[1, :3] = t[1], t[4], t[7]
    m[2, :3] = t[2], t[5], t[8]
    m[:3, 3] = t[9], t[10], t[11]
    return m


def from_matrix(m: np.ndarray) -> Tuple[float, ...]:
    return (m[0, 0], m[1, 0], m[2, 0], m[0, 1], m[1, 1], m[2, 1],
            m[0, 2], m[1, 2], m[2, 2], m[0, 3], m[1, 3], m[2, 3])


def format_transform(t: Sequence[float]) -> str:
    out = []
    for v in t:
        v = float(v)
        if abs(v) < 1e-14:
            v = 0.0
        out.append(format(v, ".15g"))
    return " ".join(out)


@dataclass
class ProjectItem:
    index: int                    # position in <build>
    object_id: int
    name: str
    transform: Tuple[float, ...]
    vertices: np.ndarray          # (n, 3) world mm
    triangles: np.ndarray         # (m, 3)
    brim: float                   # outer brim reach: brim_width + brim_separation, or 0
    settings: Dict[str, str] = field(default_factory=dict)


@dataclass
class Project:
    path: Path
    items: List[ProjectItem]
    config: Dict[str, str]
    bed: List[Tuple[float, float]]

    @property
    def first_layer_height(self) -> float:
        return _float(self.config.get("first_layer_height"), 0.2)

    def to_items(self) -> List[Item]:
        return [Item(id=it.index, vertices=it.vertices, triangles=it.triangles, brim=it.brim)
                for it in self.items]


def _float(v, default: float) -> float:
    try:
        return float(str(v).strip().rstrip("%"))
    except (TypeError, ValueError):
        return default


def _parse_mesh(body: str):
    verts = _VERTEX_FAST.findall(body)
    if len(verts) != body.count("<vertex"):
        verts = []
        for a in _VERTEX_ANY.findall(body):
            d = _attrs(a)
            verts.append((d["x"], d["y"], d["z"]))
    tris = _TRI_FAST.findall(body)
    if len(tris) != body.count("<triangle"):
        tris = []
        for a in _TRI_ANY.findall(body):
            d = _attrs(a)
            tris.append((d["v1"], d["v2"], d["v3"]))
    v = np.array(verts, dtype=np.float64).reshape(-1, 3)
    t = np.array(tris, dtype=np.int64).reshape(-1, 3)
    comps = []
    for a in _COMPONENT_RE.findall(body):
        d = _attrs(a)
        if any(k.endswith(":path") or k == "path" for k in d):
            raise ValueError("3MF production-extension components (p:path) are not supported")
        comps.append((int(d["objectid"]), parse_transform(d.get("transform"))))
    return v, t, comps


def _flatten(meshes, oid: int, m: np.ndarray, depth: int = 0):
    if depth > 16:
        raise ValueError("3MF component nesting too deep")
    v, t, comps = meshes[oid]
    vs, ts, off = [], [], 0
    if len(v):
        vs.append(np.einsum("ij,kj->ik", v, m[:3, :3]) + m[:3, 3])
        ts.append(t)
        off = len(v)
    for cid, ct in comps:
        cv, cti = _flatten(meshes, cid, m @ to_matrix(ct), depth + 1)
        vs.append(cv)
        ts.append(cti + off)
        off += len(cv)
    if not vs:
        return np.zeros((0, 3)), np.zeros((0, 3), dtype=np.int64)
    return np.concatenate(vs), np.concatenate(ts)


def _bed_shape(s: Optional[str]) -> List[Tuple[float, float]]:
    pts = []
    for p in (s or "").split(","):
        if "x" in p:
            a, b = p.strip().split("x", 1)
            pts.append((float(a), float(b)))
    return pts


def read_3mf(path) -> Project:
    path = Path(path)
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        model = z.read(MODEL).decode("utf-8")
        mcfg = z.read(MODEL_CFG).decode("utf-8") if MODEL_CFG in names else ""
        pcfg = z.read(PRINT_CFG).decode("utf-8") if PRINT_CFG in names else ""
    config = dict(re.findall(r"^; ([A-Za-z_0-9]+) = (.*)$", pcfg, re.M))
    per_obj = {int(oid): dict(_CFG_META_RE.findall(body)) for oid, body in _CFG_OBJECT_RE.findall(mcfg)}
    meshes = {}
    for a, body in _OBJECT_RE.findall(model):
        meshes[int(_attrs(a)["id"])] = _parse_mesh(body)
    if "<build" not in model:
        raise ValueError(f"{path.name}: no <build> section")
    build = model[model.index("<build"):]
    g_width = _float(config.get("brim_width"), 0.0)
    g_type = config.get("brim_type", "outer_only")
    g_sep = _float(config.get("brim_separation"), 0.0)
    items = []
    for idx, tag in enumerate(_ITEM_RE.findall(build)):
        d = _attrs(tag)
        oid = int(d["objectid"])
        if oid not in meshes:
            raise ValueError(f"{path.name}: build item refers to missing object {oid}")
        t = parse_transform(d.get("transform"))
        v, tri = _flatten(meshes, oid, to_matrix(t))
        meta = per_obj.get(oid, {})
        width = _float(meta.get("brim_width"), g_width)
        btype = meta.get("brim_type", g_type)
        sep = _float(meta.get("brim_separation"), g_sep)
        brim = width + sep if width > 0 and btype in ("outer_only", "outer_and_inner") else 0.0
        items.append(ProjectItem(idx, oid, meta.get("name", f"object-{oid}"), t, v, tri, brim,
                                 {k: x for k, x in meta.items() if k != "name"}))
    bed = _bed_shape(config.get("bed_shape"))
    return Project(path, items, config, bed)


def placement_matrix(p: Placement) -> np.ndarray:
    c, s = rot_cs(p.rot_deg)
    m = np.eye(4)
    m[0, 0], m[0, 1], m[1, 0], m[1, 1] = c, -s, s, c
    m[0, 3], m[1, 3] = p.x, p.y
    return m


def write_3mf(src, dst, placements: Sequence[Placement]) -> None:
    """Copy `src` to `dst` with each build item moved by its Placement (item_id = build index).

    Items without a placement keep their transform. Every placement must be on bed 0.
    """
    src, dst = Path(src), Path(dst)
    if src.resolve() == dst.resolve():
        raise ValueError("refusing to overwrite the source project")
    by_index = {}
    for p in placements:
        if p.bed != 0:
            raise ValueError(f"item {p.item_id!r} is on bed {p.bed}: multi-bed 3MF output is "
                             "not supported (split the project first)")
        by_index[int(p.item_id)] = p
    with zipfile.ZipFile(src) as z:
        infos = z.infolist()
        data = {i.filename: z.read(i) for i in infos}
    model = data[MODEL].decode("utf-8")
    b0 = model.index("<build")
    b1 = model.index("</build>", b0) if "</build>" in model[b0:] else len(model)
    head, build, tail = model[:b0], model[b0:b1], model[b1:]
    counter = [0]

    def sub(mo):
        tag = mo.group(0)
        idx = counter[0]
        counter[0] += 1
        p = by_index.get(idx)
        if p is None:
            return tag
        old = parse_transform(_attrs(tag).get("transform"))
        new = format_transform(from_matrix(placement_matrix(p) @ to_matrix(old)))
        if re.search(r'\stransform="[^"]*"', tag):
            return re.sub(r'(\stransform=")[^"]*(")', lambda m: m.group(1) + new + m.group(2),
                          tag, count=1)
        return re.sub(r'(<item\b)', lambda m: f'{m.group(1)} transform="{new}"', tag, count=1)

    build = _ITEM_RE.sub(sub, build)
    missing = set(by_index) - set(range(counter[0]))
    if missing:
        raise ValueError(f"placements for unknown build items {sorted(missing)}")
    data[MODEL] = (head + build + tail).encode("utf-8")
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + ".part")
    with zipfile.ZipFile(tmp, "w") as out:
        for i in infos:
            zi = zipfile.ZipInfo(i.filename, date_time=i.date_time)
            zi.compress_type = i.compress_type
            zi.external_attr = i.external_attr
            zi.create_system = i.create_system
            out.writestr(zi, data[i.filename])
    tmp.replace(dst)


# ------------------------------------------------------------------ merge

_OBJ_OPEN_RE = re.compile(r'<object\b[^>]*>')
_ID_ATTR_RE = re.compile(r'(\sid=")(\d+)(")')
_OBJID_ATTR_RE = re.compile(r'(\sobjectid=")(\d+)(")')
_CFG_BLOCK_RE = re.compile(r'[ \t]*<object id="(\d+)"[^>]*>.*?</object>[ \t]*\n?', re.S)
_CFG_NAME_RE = re.compile(r'(<metadata type="object" key="name" value=")([^"]*)(")')
_COPY_RE = re.compile(r"^(.*)#(\d+)$")


def _split_model(model: str):
    """(head up to <resources>, {id: object xml}, [ids in order], [item tags], tail)."""
    r0 = model.index("<resources>") + len("<resources>")
    r1 = model.index("</resources>")
    b0 = model.index("<build", r1)
    b1 = model.index("</build>", b0)
    objs, order = {}, []
    for mo in re.finditer(r'<object\b[^>]*>.*?</object>', model[r0:r1], re.S):
        xml = mo.group(0)
        oid = int(_attrs(_OBJ_OPEN_RE.match(xml).group(0))["id"])
        objs[oid] = xml
        order.append(oid)
    items = _ITEM_RE.findall(model[b0:b1])
    return model[:r0], objs, order, items, model[b1:]


def _needed(objs: dict, oid: int, out: list) -> None:
    """`oid` and every object its components reference, children first, each once."""
    if oid in out:
        return
    for a in _COMPONENT_RE.findall(objs[oid]):
        _needed(objs, int(_attrs(a)["objectid"]), out)
    out.append(oid)


def merge_3mf(sources: Sequence, dst, select: Optional[Sequence[Tuple[int, int]]] = None,
              title: Optional[str] = None, config_from: int = 0) -> List[Tuple[int, int]]:
    """Write `dst`: one PrusaSlicer project holding the build items of every source.

    sources      project paths; their print configs should agree (same ini), since only
                 `sources[config_from]` contributes Slic3r_PE.config and the other members
    select       (source index, build-item index) pairs, in output order; default every item
                 of every source in order. Only objects the selected items use are written
    title        replaces the model's Title and Description metadata (e.g. the new plate id)

    Item transforms are kept as they are (arrange afterwards with write_3mf). An object name
    that would occur twice is renumbered `name#1..#k` across the merged project, so a copy
    index stays unique; every other name is unchanged. Returns, per output build item, the
    (source index, item index) it came from.
    """
    srcs = [Path(s) for s in sources]
    dst = Path(dst)
    if not srcs:
        raise ValueError("merge_3mf needs at least one source")
    if any(s.resolve() == dst.resolve() for s in srcs):
        raise ValueError("refusing to overwrite a source project")
    parsed, cfgs, infos, data = [], [], None, None
    for si, s in enumerate(srcs):
        with zipfile.ZipFile(s) as z:
            if si == config_from:
                infos = z.infolist()
                data = {i.filename: z.read(i) for i in infos}
            model = z.read(MODEL).decode("utf-8")
            names = set(z.namelist())
            mcfg = z.read(MODEL_CFG).decode("utf-8") if MODEL_CFG in names else ""
        parsed.append(_split_model(model))
        cfgs.append({int(oid): mo.group(0) for mo in _CFG_BLOCK_RE.finditer(mcfg)
                     for oid in [mo.group(1)]})
    if select is None:
        select = [(si, ii) for si, p in enumerate(parsed) for ii in range(len(p[3]))]
    select = [(int(a), int(b)) for a, b in select]
    if len(set(select)) != len(select):
        raise ValueError("an item is selected twice")

    # new object ids: every object a selected item needs, in source then file order
    remap: Dict[Tuple[int, int], int] = {}
    for si, p in enumerate(parsed):
        want: list = []
        for ssi, ii in select:
            if ssi == si:
                if not 0 <= ii < len(p[3]):
                    raise ValueError(f"{srcs[si].name}: no build item {ii}")
                _needed(p[1], int(_attrs(p[3][ii])["objectid"]), want)
        for oid in p[2]:
            if oid in want:
                remap[(si, oid)] = len(remap) + 1

    def renum(si, xml, rx):
        return rx.sub(lambda m: m.group(1) + str(remap[(si, int(m.group(2)))]) + m.group(3), xml)

    objects_xml, cfg_blocks = [], []
    for (si, oid), new in sorted(remap.items(), key=lambda kv: kv[1]):
        xml = parsed[si][1][oid]
        head_tag = _OBJ_OPEN_RE.match(xml).group(0)
        xml = renum(si, head_tag, _ID_ATTR_RE) + xml[len(head_tag):]
        objects_xml.append(renum(si, xml, _OBJID_ATTR_RE))
        blk = cfgs[si].get(oid)
        if blk is not None:
            cfg_blocks.append((new, _ID_ATTR_RE.sub(lambda m: m.group(1) + str(new) + m.group(3),
                                                    blk, count=1)))
    items_xml = [renum(si, parsed[si][3][ii], _OBJID_ATTR_RE) for si, ii in select]

    # names: a base name whose full names would repeat is renumbered base#1..#k
    def base(n):
        m = _COPY_RE.match(n)
        return m.group(1) if m else n
    named = [(i, mo.group(2)) for i, (_n, blk) in enumerate(cfg_blocks)
             for mo in [_CFG_NAME_RE.search(blk)] if mo]
    by_base: Dict[str, List[Tuple[int, str]]] = {}
    for i, n in named:
        by_base.setdefault(base(n), []).append((i, n))
    for b, members in by_base.items():
        if len({n for _i, n in members}) == len(members):
            continue
        for k, (i, _n) in enumerate(members, 1):
            new, blk = cfg_blocks[i]
            cfg_blocks[i] = (new, _CFG_NAME_RE.sub(
                lambda mo, k=k: mo.group(1) + f"{b}#{k}" + mo.group(3), blk, count=1))

    head, _o, _ord, _it, tail = parsed[config_from]
    if title is not None:
        esc = (title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        for key in ("Title", "Description"):
            head = re.sub(rf'(<metadata name="{key}">)[^<]*(</metadata>)',
                          lambda m: m.group(1) + esc + m.group(2), head, count=1)
    ind = "\n  "
    model = (head + ind + ind.join(objects_xml) + "\n </resources>\n <build>" + ind
             + ind.join(items_xml) + "\n " + tail)
    data[MODEL] = model.encode("utf-8")
    src_cfg = data.get(MODEL_CFG, b"").decode("utf-8")
    if cfg_blocks or src_cfg:
        first = _CFG_BLOCK_RE.search(src_cfg)
        pre = src_cfg[:first.start()] if first else '<?xml version="1.0" encoding="UTF-8"?>\n<config>\n'
        post = src_cfg[src_cfg.rindex("</object>") + len("</object>"):].lstrip(" \t\n") \
            if first else "</config>\n"
        data[MODEL_CFG] = (pre + "".join(b if b.endswith("\n") else b + "\n"
                                         for _n, b in cfg_blocks) + post).encode("utf-8")
        if MODEL_CFG not in {i.filename for i in infos}:
            infos.append(zipfile.ZipInfo(MODEL_CFG, date_time=infos[0].date_time))
    keep = [i for i in infos if not re.match(r"Metadata/thumbnail.*\.png$", i.filename)]
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + ".part")
    with zipfile.ZipFile(tmp, "w") as out:
        for i in keep:
            zi = zipfile.ZipInfo(i.filename, date_time=i.date_time)
            zi.compress_type = i.compress_type
            zi.external_attr = i.external_attr
            zi.create_system = i.create_system
            out.writestr(zi, data[i.filename])
    tmp.replace(dst)
    return list(select)
