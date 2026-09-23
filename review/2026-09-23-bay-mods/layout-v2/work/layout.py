import trimesh, numpy as np, json, math
from shapely.geometry import Polygon, box as sbox, Point
from shapely.ops import unary_union
from shapely import affinity
import os; S=os.environ['BAY_MODS_SCRATCH']  # dir holding mods/502306-cable-duct and mods/505838-ac-covers
D=S+'/mods/502306-cable-duct/'; RX=S+'/mods/layout-v2/remix/'; OUT=S+'/mods/layout-v2/'
ROT={0:np.eye(2),90:np.array([[0,-1],[1,0]]),180:-np.eye(2),-90:np.array([[0,1],[-1,0]])}
DIAG=np.array([[0,1],[1,0]])   # reflection across the local diagonal (mirrored corner)
_cache={}
def sections(path, family):
    if path in _cache: return _cache[path]
    m=trimesh.load(path); out={}
    for h in (12.5,24.0):
        if family=='2B': z=h; flipy=True
        else: z=m.bounds[1][2]-h; flipy=False
        s=m.section(plane_origin=[0,0,z],plane_normal=[0,0,1]); U=Polygon()
        for e in s.discrete:
            if len(e)>3:
                pts=e[:,:2].copy()
                if flipy: pts[:,1]*=-1
                U=U.symmetric_difference(Polygon(pts).buffer(0))
        out[h]=U
    # outer footprint (fill holes = channel interior counts as occupied)
    def fill(U):
        gs=getattr(U,'geoms',[U]); return unary_union([Polygon(g.exterior) for g in gs if not g.is_empty])
    cl=lambda U: fill(U).buffer(12.5,join_style=1).buffer(-12.5,join_style=1)
    out['mid']=cl(out[12.5]); out['hi']=cl(out[24.0]).buffer(1.7)
    _cache[path]=out; return out
def xf(poly, R, ref, g):
    a,b,c,d=R[0,0],R[0,1],R[1,0],R[1,1]
    p=affinity.translate(poly,-ref[0],-ref[1]); p=affinity.affine_transform(p,[a,b,c,d,0,0]); return affinity.translate(p,g[0],g[1])
P=[]  # placed pieces
def place(pid, run, file, family, R, ref, g, custom=False, color='dc', note=''):
    sec=sections(file, family); P.append(dict(id=pid, run=run, file=file.split('/')[-1], custom=custom, kind=color,
        mid=xf(sec['mid'],R,ref,g), hi=xf(sec['hi'],R,ref,g), note=note))
def rect_piece(pid, run, name, x0,x1,y0,y1, color, custom=False):
    r=sbox(x0,y0,x1,y1); P.append(dict(id=pid,run=run,file=name,custom=custom,kind=color,mid=r,hi=r,note=''))
def sref(f): m=trimesh.load(f); return (m.bounds[0][0], m.bounds[0][1]+12.2)
# ---------------- parameters (apparent mm, frame centre origin, +y rear) ----------------
xL,xR,yF,yM,yRr = -178.4, 209.2, -147.0, -5.0, 145.8
C90=(-313.0,-103.16); TREG=(-51.14,208.38)
f154=D+'CMD_V3_1H_154mm_DUCT.stl'; r154=sref(f154)
f58=RX+'V2L_58mm_DUCT.stl'; r58=sref(f58); f130=RX+'V2L_130mm_DUCT.stl'; r130=sref(f130)
f70=RX+'V2L_70mm_DUCT.stl'; r70=sref(f70); f22=RX+'V2L_22mm_DUCT.stl'; r22=sref(f22)
f90=D+'CMD_V3_1H_90DEG.stl'; fT=D+'CMD_V3_1H_T_REG.stl'; f45=D+'CMD_Remix-V3_DUCT-2B_45deg.stl'
# DC loop
place('FL','DC','V2L_90DEG_MIRROR.stl (mirror of CMD_V3_1H_90DEG)','V3',DIAG,C90,(xL,yF),custom=True) if False else None
P.append(None); P.pop()
sec=sections(f90,'V3'); P.append(dict(id='FL',run='DC',file='V2L_90DEG_MIRROR.stl',custom=True,kind='dc',mid=xf(sec['mid'],DIAG,C90,(xL,yF)),hi=xf(sec['hi'],DIAG,C90,(xL,yF)),note='mirror'))
place('F1','DC',f154,'V3',ROT[0],r154,(xL+38.8+1.0,yF))
place('F2','DC',f154,'V3',ROT[0],r154,(xL+38.8+1.0+154,yF))
place('FR','DC',f90,'V3',ROT[90],C90,(xR,yF))
place('L1','DC',f58,'V3',ROT[90],r58,(xL,yF+42),custom=True)
place('TL','DC',fT,'V3',ROT[90],TREG,(xL,yM))
place('L2','DC',f130,'V3',ROT[90],r130,(xL,yM+42),custom=True)
place('R1','DC',f58,'V3',ROT[90],r58,(xR,yF+42),custom=True)
place('TR','DC',fT,'V3',ROT[-90],TREG,(xR,yM))
place('R2','DC',f70,'V3',ROT[90],r70,(xR,yM+42),custom=True)
place('RR','DC',f90,'V3',ROT[180],C90,(xR,yRr))
place('B1','DC',f58,'V3',ROT[180],r58,(xR-42,yRr),custom=True)
j0=np.array([xR-42-58,yRr]); Rl=ROT[-90]; loc_s=np.array([26.36,0.0]); loc_d=np.array([8.07,-47.75])
place('J1','DC',f45,'2B',Rl,loc_s,j0)
joint=Rl@(loc_d-loc_s)+j0; place('J2','DC',f45,'2B',-Rl,loc_d,joint)
up=2*joint-j0
place('B2','DC',f22,'V3',ROT[180],r22,(up[0],up[1]),custom=True)
place('M1','MID',f154,'V3',ROT[0],r154,(xL+39.8,yM))
place('M2','MID',f154,'V3',ROT[0],r154,(xL+39.8+154,yM))
# AC
place('HUB','AC',RX+'V2L_AC_HUB.stl','V3',ROT[180],(0,0),(-36.96,73.83),custom=True,color='ac')
place('H1','AC',RX+'V2L_58mm_DUCT_HOLE.stl','V3',ROT[0],r58,(-30.0,146.0),custom=True,color='ac')
rect_piece('EC','AC','CMD_Remix-V3_DUCT-1M_ENDCAP.stl',28.0,35.8,134.25,157.75,'ac')
rect_piece('FIN','AC','V2L_STRIP_FIN.stl',-50.0,-25.5,90.0,92.4,'ac',custom=True)
print('joint',joint.round(2),'upper start',up.round(2))
# ---------------- obstacles ----------------
dy=-7.0  # front rail shift
OB={ 'PSU (4 mm left)':(sbox(-25.3,11,192,126.7),22.5), 'Leviathan PCB':(sbox(-100,-114+dy,69,-15.3+dy),25.4),
 'USB adapter':(sbox(118,-93+dy,158,-36+dy),0),'SSR':(sbox(-109,25,-62.5,102),0),'WAGO':(sbox(-129,202,-38.4,220),0),
 'Inlet':(sbox(-145,220,-95,243),0),'Z FL':(sbox(-201.7,-231,-148,-172),0),'Z FR':(sbox(175.6,-231,229,-172),0),
 'Z RL':(sbox(-201.7,173.3,-149.2,234),0),'Z RR':(sbox(176.7,173,229,234),0),'Z0 plug':(sbox(-148,-189,-136,-179),0),
 'Z3 plug':(sbox(164,-189,175.6,-179),0),'Z1 plug':(sbox(-149.2,178,-137,189),0),'Z2 plug':(sbox(164,180,176.7,188),0),
 'front rail':(sbox(-146,-79+dy,172,-45+dy),0),'rear rail':(sbox(-145,47,172,80),0),'keystone':(sbox(150,210,167,238),0),
 'notch':(sbox(0,195,12,222),0),'frame L':(sbox(-260,-260,-235,260),0),'frame R':(sbox(235,-260,260,260),0),
 'fan splicer (unverified)':(sbox(225,-15,235,15),0),'frame rear':(sbox(-260,222,260,260),0),'frame front':(sbox(-260,-260,260,-222),0)}
hole=Point(14.7,146).buffer(7.0)
rep=[]
for p in P:
    if p['id']=='FIN': continue
    for name,(ob,z0) in OB.items():
        fp=p['hi'] if z0>=20 else p['mid'].union(p['hi'])
        d=fp.distance(ob); ov=fp.intersection(ob).area
        if d<6 or ov>0: rep.append((round(d,1),round(ov,1),p['id'],name))
# piece-piece overlaps between different runs / AC vs DC
for i,a in enumerate(P):
    for b in P[i+1:]:
        if a['kind']!=b['kind']:
            d=a['mid'].union(a['hi']).distance(b['mid'].union(b['hi']))
            if d<15: rep.append((round(d,1),0,a['id'],b['id']+' (AC/DC gap)'))
for r in sorted(rep): print(r)
hub=[p for p in P if p['id']=='H1'][0]
# hole inside channel interior? interior approx = footprint shrunk by 3.5 (wall+bulge)
inner=hub['mid'].buffer(-3.6)
print('hole inside AC hole-run interior:', inner.contains(hole), 'margin', round(inner.exterior.distance(Point(14.7,146))-7.0 if inner.geom_type=='Polygon' else -1,2))
import pickle; pickle.dump(dict(P=P,OB=OB,joint=joint,up=up,params=dict(xL=xL,xR=xR,yF=yF,yM=yM,yRr=yRr,dy=dy)), open(OUT+'work/placed.pkl','wb'))
