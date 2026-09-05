#!/usr/bin/env python3
"""Load a STEP assembly via OCCT/XCAF, walk the product tree, tessellate every
leaf part in world coordinates and write a reusable mesh cache.

Outputs (in --out):
  index.json   one record per leaf instance: id, name, path, bbox, tri count, colour
  meshes.npz   per-instance 'v{id}' float32 (n,3) verts and 't{id}' int32 (m,3) tris

Run once per STEP file (expensive); every render then reads the cache (cheap).
"""
import argparse, json, os, sys, time

import numpy as np
from OCP.BRep import BRep_Tool
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.IFSelect import IFSelect_ReturnStatus
from OCP.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDataStd import TDataStd_Name
from OCP.TDF import TDF_Label, TDF_LabelSequence
from OCP.TDocStd import TDocStd_Document
from OCP.TopAbs import TopAbs_FACE
from OCP.TopExp import TopExp_Explorer
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorType


def label_name(label: TDF_Label) -> str:
    from OCP.TDataStd import TDataStd_Name
    attr = TDataStd_Name()
    if label.FindAttribute(TDataStd_Name.GetID_s(), attr):
        return attr.Get().ToExtString()
    return ""


def tessellate(shape, lin_defl, ang_defl):
    """Mesh `shape` (already positioned) and return (verts, tris) in world coords."""
    BRepMesh_IncrementalMesh(shape, lin_defl, False, ang_defl, True)
    vs, ts, off = [], [], 0
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        face = TopoDS.Face_s(exp.Current())
        loc = TopLoc_Location()
        tri = BRep_Tool.Triangulation_s(face, loc)
        exp.Next()
        if tri is None:
            continue
        trsf = loc.Transformation()
        n = tri.NbNodes()
        arr = np.empty((n, 3), dtype=np.float64)
        for i in range(1, n + 1):
            p = tri.Node(i).Transformed(trsf)
            arr[i - 1] = (p.X(), p.Y(), p.Z())
        m = tri.NbTriangles()
        idx = np.empty((m, 3), dtype=np.int64)
        reverse = face.Orientation() == 1  # TopAbs_REVERSED
        for i in range(1, m + 1):
            a, b, c = tri.Triangle(i).Get()
            idx[i - 1] = (a - 1, c - 1, b - 1) if reverse else (a - 1, b - 1, c - 1)
        vs.append(arr)
        ts.append(idx + off)
        off += n
    if not vs:
        return np.zeros((0, 3), np.float32), np.zeros((0, 3), np.int32)
    return (np.concatenate(vs).astype(np.float32),
            np.concatenate(ts).astype(np.int32))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step")
    ap.add_argument("--out", required=True)
    ap.add_argument("--lin-defl", type=float, default=0.0, help="0 = adaptive per part")
    ap.add_argument("--ang-defl", type=float, default=0.4)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    t0 = time.time()

    def log(msg):
        print(f"[{time.time() - t0:7.1f}s] {msg}", flush=True)

    doc = TDocStd_Document(TCollection_ExtendedString("doc"))
    reader = STEPCAFControl_Reader()
    reader.SetNameMode(True)
    reader.SetColorMode(True)
    reader.SetLayerMode(True)
    log(f"reading {args.step} ({os.path.getsize(args.step)/1e6:.0f} MB)")
    if reader.ReadFile(args.step) != IFSelect_ReturnStatus.IFSelect_RetDone:
        sys.exit("STEP read failed")
    log("parsed; transferring to XCAF document")
    if not reader.Transfer(doc):
        sys.exit("STEP transfer failed")
    log("transfer done")

    st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    ct = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())

    def colour_of(lab, shape):
        c = Quantity_Color()
        for t in (XCAFDoc_ColorType.XCAFDoc_ColorSurf,
                  XCAFDoc_ColorType.XCAFDoc_ColorGen,
                  XCAFDoc_ColorType.XCAFDoc_ColorCurv):
            try:
                if ct.GetColor(lab, t, c):
                    return [round(c.Red(), 4), round(c.Green(), 4), round(c.Blue(), 4)]
                if shape is not None and ct.GetColor(shape, t, c):
                    return [round(c.Red(), 4), round(c.Green(), 4), round(c.Blue(), 4)]
            except Exception:
                pass
        return None

    records, meshes = [], {}
    counter = [0]

    def leaf(lab, loc, path, colour):
        if args.limit and counter[0] >= args.limit:
            return
        shape = st.GetShape_s(lab)
        if shape.IsNull():
            return
        moved = shape.Moved(loc)
        box = Bnd_Box()
        BRepBndLib.Add_s(moved, box, False)
        if box.IsVoid():
            return
        x0, y0, z0, x1, y1, z1 = box.Get()
        diag = float(np.linalg.norm([x1 - x0, y1 - y0, z1 - z0]))
        defl = args.lin_defl or min(1.0, max(0.06, diag / 260.0))
        v, t = tessellate(moved, defl, args.ang_defl)
        if len(t) == 0:
            return
        i = counter[0]
        counter[0] += 1
        col = colour_of(lab, shape) or colour
        records.append(dict(id=i, name=path[-1], path="/".join(path), tris=int(len(t)),
                            bbox=[round(x0, 2), round(y0, 2), round(z0, 2),
                                  round(x1, 2), round(y1, 2), round(z1, 2)],
                            colour=col, deflection=round(defl, 3)))
        meshes[f"v{i}"] = v
        meshes[f"t{i}"] = t
        if i % 100 == 0:
            log(f"  {i} parts, {sum(r['tris'] for r in records)/1e6:.2f}M tris")

    def walk(lab, loc, path, colour, depth=0):
        if args.limit and counter[0] >= args.limit:
            return
        colour = colour_of(lab, None) or colour
        if st.IsAssembly_s(lab):
            comps = TDF_LabelSequence()
            st.GetComponents_s(lab, comps)
            for k in range(1, comps.Length() + 1):
                comp = comps.Value(k)
                cloc = st.GetLocation_s(comp)
                ref = TDF_Label()
                nm = label_name(comp)
                ccol = colour_of(comp, None) or colour
                if st.GetReferredShape_s(comp, ref):
                    rn = label_name(ref)
                    walk(ref, loc.Multiplied(cloc), path + [nm or rn or f"part{k}"],
                         ccol, depth + 1)
                else:
                    walk(comp, loc.Multiplied(cloc), path + [nm or f"part{k}"],
                         ccol, depth + 1)
        else:
            leaf(lab, loc, path, colour)

    roots = TDF_LabelSequence()
    st.GetFreeShapes(roots)
    log(f"{roots.Length()} free shape root(s)")
    for k in range(1, roots.Length() + 1):
        r = roots.Value(k)
        walk(r, TopLoc_Location(), [label_name(r) or f"root{k}"], None)

    log(f"{len(records)} leaf parts, {sum(r['tris'] for r in records)/1e6:.2f}M triangles")
    with open(os.path.join(args.out, "index.json"), "w") as f:
        json.dump(records, f, indent=1)
    np.savez(os.path.join(args.out, "meshes.npz"), **meshes)
    log(f"wrote {args.out}/index.json + meshes.npz "
        f"({os.path.getsize(os.path.join(args.out,'meshes.npz'))/1e6:.0f} MB)")


if __name__ == "__main__":
    main()
