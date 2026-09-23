import trimesh, numpy as np
from collections import defaultdict
def fix_nonmanifold(m):
    m=m.copy(); F=m.faces.copy(); V=m.vertices.copy()
    ed=defaultdict(list)
    for fi,f in enumerate(F):
        for k in range(3):
            a,b=f[k],f[(k+1)%3]; ed[(min(a,b),max(a,b))].append((fi,(a,b)))
    for (a,b),lst in ed.items():
        if len(lst)!=4: continue
        fw=[fi for fi,(p,q) in lst if (p,q)==(a,b)]; bw=[fi for fi,(p,q) in lst if (p,q)==(b,a)]
        # pair by normal angle: fw[0] with the bw face whose normal is closer to opposite of the other pair.. choose pairing giving smallest dihedral opening
        n=m.face_normals
        c0=np.dot(n[fw[0]],n[bw[0]]); c1=np.dot(n[fw[0]],n[bw[1]])
        pair=(fw[0],bw[0]) if c0>c1 else (fw[0],bw[1])
        # duplicate vertices a,b for this pair
        na=len(V); V=np.vstack([V,V[a],V[b]]); nb=na+1
        for fi in pair:
            F[fi]=[na if x==a else nb if x==b else x for x in F[fi]]
    return trimesh.Trimesh(V,F,process=False)
