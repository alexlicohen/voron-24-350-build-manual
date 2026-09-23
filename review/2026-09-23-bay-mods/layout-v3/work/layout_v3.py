import trimesh, numpy as np, json, math
from shapely.geometry import Polygon, box as sbox, Point
from shapely.ops import unary_union
from shapely import affinity
import os; S=os.environ['BAY_MODS_SCRATCH']  # dir holding mods/ (MSS downloads + layout-v2)
D=S+'/mods/502306-cable-duct/'; RX=S+'/mods/layout-v2/remix/'; OUT=S+'/mods/layout-v3/'; R3=S+'/mods/layout-v3/remix/'
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
# ---------------- parameters v3 (apparent mm, frame centre origin, +y rear) ----------------
xL,xR,yM = -178.4, 209.2, -2.2
TH=40.8                      # narrowed T_REG half-bar
yF=yM-TH-58-42; yRr=yM+TH+70+38.8
C90=(-313.0,-103.16); TN=(-52.34,208.38); CR=(-306.5,-96.66)
f154=D+'CMD_V3_1H_154mm_DUCT.stl'; r154=sref(f154)
f154N=R3+'V3L_154N_DUCT.stl'; m=trimesh.load(f154N); r154N=(m.bounds[0][0], m.bounds[0][1]+11.0)
f58=RX+'V2L_58mm_DUCT.stl'; r58=sref(f58); f130=RX+'V2L_130mm_DUCT.stl'; r130=sref(f130); f70=RX+'V2L_70mm_DUCT.stl'; r70=sref(f70)
f10=R3+'V3L_10mm_DUCT.stl'; r10=sref(f10); f34=R3+'V3L_34mm_DUCT_HOLE.stl'; r34=sref(f34)
f90=D+'CMD_V3_1H_90DEG.stl'; fTN=R3+'V3L_T_REG_N.stl'; f45=D+'CMD_Remix-V3_DUCT-2B_45deg.stl'; fR15=R3+'V3L_90DEG_R15.stl'
fTS=D+'CMD_V3_1H_T_SHORT.stl'; fBOX=R3+'V3L_WIRE_BOX_PORT.stl'
sec=sections(f90,'V3'); P.append(dict(id='FL',run='DC',file='V2L_90DEG_MIRROR.stl',custom=True,kind='dc',mid=xf(sec['mid'],DIAG,C90,(xL,yF)),hi=xf(sec['hi'],DIAG,C90,(xL,yF)),note='mirror'))
place('F1','DC',f154,'V3',ROT[0],r154,(xL+38.8+1.0,yF)); place('F2','DC',f154,'V3',ROT[0],r154,(xL+38.8+1.0+154,yF))
place('FR','DC',f90,'V3',ROT[90],C90,(xR,yF))
place('L1','DC',f58,'V3',ROT[90],r58,(xL,yF+42),custom=True); place('TL','DC',fTN,'V3',ROT[90],TN,(xL,yM),custom=True)
place('L2','DC',f130,'V3',ROT[90],r130,(xL,yM+TH),custom=True)
place('R1','DC',f58,'V3',ROT[90],r58,(xR,yF+42),custom=True); place('TR','DC',fTN,'V3',ROT[-90],TN,(xR,yM),custom=True)
place('R2','DC',f70,'V3',ROT[90],r70,(xR,yM+TH),custom=True); place('RR','DC',f90,'V3',ROT[180],C90,(xR,yRr))
place('B1','DC',f58,'V3',ROT[180],r58,(xR-42,yRr),custom=True)
j0=np.array([xR-42-58,yRr]); Rl=ROT[-90]; loc_s=np.array([26.36,0.0]); loc_d=np.array([8.07,-47.75])
place('J1','DC',f45,'2B',Rl,loc_s,j0); joint=Rl@(loc_d-loc_s)+j0; place('J2','DC',f45,'2B',-Rl,loc_d,joint); up=2*joint-j0
place('B2','DC',f10,'V3',ROT[180],r10,(up[0],up[1]),custom=True)
place('M1','MID',f154N,'V3',ROT[0],r154N,(xL+39.8,yM),custom=True); place('M2','MID',f154N,'V3',ROT[0],r154N,(xL+39.8+154,yM),custom=True)
# AC: original-proportion wire box at the WAGO + two re-radiused curves down to the hole run; SSR run joins the box by a stub
place('BOX','AC',fBOX,'V3',ROT[180],(0,0),(-45.36,73.84),custom=True,color='ac')
place('C1','AC',fR15,'V3',ROT[180],CR,(-22.9,177.0),custom=True,color='ac')
place('C2','AC',fR15,'V3',ROT[0],CR,(-22.9,146.0),custom=True,color='ac')
place('H1','AC',f34,'V3',ROT[0],r34,(-7.4,146.0),custom=True,color='ac')
rect_piece('EC','AC','CMD_Remix-V3_DUCT-1M_ENDCAP.stl',26.6,34.4,134.25,157.75,'ac')
place('TS','AC',fTS,'V3',ROT[180],(-51.14,408.38),(-72.0,116.0),color='ac')
place('S1','AC',f10,'V3',ROT[0],r10,(-42.0,116.0),custom=True,color='ac')
place('ST','AC',f10,'V3',ROT[90],r10,(-72.0,142.8),custom=True,color='ac')
rect_piece('EC2','AC','CMD_Remix-V3_DUCT-1M_ENDCAP.stl',-109.8,-102.0,104.25,127.75,'ac')
rect_piece('FIN','AC','V2L_STRIP_FIN.stl',-52.0,-27.5,90.0,92.4,'ac',custom=True)
print('yF',yF,'yRr',yRr,'joint',joint.round(2),'upper',up.round(2))
OB={ 'PSU (6 mm left)':(sbox(-27.3,11,190,126.7),22.5), 'Leviathan PCB':(sbox(-100,-114,69,-15.3),25.4),
 'USB adapter':(sbox(118,-93,158,-36),0),'SSR':(sbox(-109,25,-62.5,102),0),'WAGO':(sbox(-129,202,-38.4,220),0),
 'Inlet':(sbox(-145,220,-95,243),0),'Z FL':(sbox(-201.7,-231,-148,-172),0),'Z FR':(sbox(175.6,-231,229,-172),0),
 'Z RL':(sbox(-201.7,173.3,-149.2,234),0),'Z RR':(sbox(176.7,173,229,234),0),'Z0 plug':(sbox(-148,-189,-136,-179),0),
 'Z3 plug':(sbox(164,-189,175.6,-179),0),'Z1 plug':(sbox(-149.2,178,-137,189),0),'Z2 plug':(sbox(164,180,176.7,188),0),
 'front rail':(sbox(-146,-79,172,-45),0),'rear rail':(sbox(-145,47,172,80),0),'keystone':(sbox(150,210,167,238),0),
 'notch':(sbox(0,195,12,222),0),'frame L':(sbox(-260,-260,-235,260),0),'frame R':(sbox(235,-260,260,260),0),
 'fan splicer (unverified)':(sbox(225,-15,235,15),0),'frame rear':(sbox(-260,222,260,260),0),'frame front':(sbox(-260,-260,260,-222),0)}
rep=[]
for p in P:
    if p['id']=='FIN': continue
    for name,(ob,z0) in OB.items():
        fp=p['hi'] if z0>=20 else p['mid'].union(p['hi'])
        d=fp.distance(ob); ov=fp.intersection(ob).area
        if d<6 or ov>0: rep.append((round(d,1),round(ov,1),p['id'],name))
for i,a in enumerate(P):
    for b in P[i+1:]:
        if a['kind']!=b['kind']:
            d=a['mid'].union(a['hi']).distance(b['mid'].union(b['hi']))
            if d<20: rep.append((round(d,1),0,a['id'],b['id']+' (AC/DC gap)'))
for r in sorted(rep): print(r)
import pickle; pickle.dump(dict(P=P,OB=OB,joint=joint,up=up,params=dict(xL=xL,xR=xR,yF=yF,yM=yM,yRr=yRr)), open(OUT+'work/placed.pkl','wb'))
