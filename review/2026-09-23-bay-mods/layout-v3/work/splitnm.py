import trimesh, numpy as np, manifold3d as mf
from collections import defaultdict
def unpinch(m):
    """Duplicate vertices at non-manifold (4-face) edges so each touching solid gets its own copy."""
    V=m.vertices.copy(); F=m.faces.copy(); ed=defaultdict(list)
    for fi,f in enumerate(F):
        for k in range(3):
            a,b=sorted((int(f[k]),int(f[(k+1)%3]))); ed[(a,b)].append(fi)
    bad=[e for e,l in ed.items() if len(l)>2]
    verts=sorted(set([v for e in bad for v in e]))
    vf=defaultdict(list)
    for fi,f in enumerate(F):
        for v in f: vf[int(v)].append(fi)
    for v in verts:
        fs=vf[v]; parent={f:f for f in fs}
        def find(x):
            while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
            return x
        for (a,b),l in ed.items():
            if v in (a,b) and len(l)==2 and l[0] in parent and l[1] in parent: parent[find(l[0])]=find(l[1])
        groups=defaultdict(list)
        for f in fs: groups[find(f)].append(f)
        for gi,(k,g) in enumerate(groups.items()):
            if gi==0: continue
            nv=len(V); V=np.vstack([V,V[v]])
            for f in g: F[f]=[nv if x==v else x for x in F[f]]
    return trimesh.Trimesh(V,F,process=False)
def to_mf(m): return mf.Manifold(mf.Mesh(vert_properties=np.asarray(m.vertices,np.float32), tri_verts=np.asarray(m.faces,np.uint32)))
def from_mf(M):
    g=M.to_mesh(); return trimesh.Trimesh(np.asarray(g.vert_properties)[:,:3], np.asarray(g.tri_verts), process=False)
