import os
import trimesh, numpy as np, itertools
from collections import defaultdict
from splitnm import to_mf
def unpinch(m, choice):
    V=m.vertices; F=m.faces; nF=len(F)
    he=defaultdict(list)  # (a,b) directed -> list of (f,k)
    for f in range(nF):
        for k in range(3): he[(int(F[f][k]),int(F[f][(k+1)%3]))].append((f,k))
    twin={}
    bad=sorted({tuple(sorted(e)) for e,l in he.items() if len(l)>1 or len(he.get((e[1],e[0]),[]))>1})
    for (a,b),l in he.items():
        r=he.get((b,a),[])
        if len(l)==1 and len(r)==1: twin[l[0]]=r[0]
    for i,(a,b) in enumerate(bad):
        fw=he[(a,b)]; bw=he[(b,a)]
        p=[(fw[0],bw[0]),(fw[1],bw[1])] if choice[i]==0 else [(fw[0],bw[1]),(fw[1],bw[0])]
        for x,y in p: twin[x]=y; twin[y]=x
    # corners -> new vertex ids by walking fans
    newid={}; NV=[]
    for f in range(nF):
        for i in range(3):
            if (f,i) in newid: continue
            v=int(F[f][i]); vid=len(NV); NV.append(V[v]); cur=(f,i); guard=0
            while cur not in newid and guard<1000:
                newid[cur]=vid; g,j=cur
                inc=(g,(j-1)%3)          # half-edge u->v in face g
                t=twin.get(inc)
                if t is None: break
                cur=t                     # t is v->u in another face: its corner at v is index t[1]
                guard+=1
    NF=np.array([[newid[(f,i)] for i in range(3)] for f in range(nF)])
    return trimesh.Trimesh(np.array(NV),NF,process=False), len(bad)
if __name__=='__main__':
    m=trimesh.load(os.environ['BAY_MODS_SCRATCH']+'/mods/502306-cable-duct/CMD_V3_1H_WIRE_BOX.stl')
    for ch in itertools.product([0,1],repeat=4):
        u,nb=unpinch(m,ch); M=to_mf(u)
        print(ch, nb, u.is_watertight, M.status(), round(M.volume()/1000,2))
