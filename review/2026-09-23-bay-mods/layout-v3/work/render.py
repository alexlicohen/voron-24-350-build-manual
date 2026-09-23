import trimesh, numpy as np, matplotlib, pickle
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os; S=os.environ['BAY_MODS_SCRATCH']  # dir holding mods/ (MSS downloads + layout-v2)
D=S+'/mods/502306-cable-duct/'; A=S+'/mods/505838-ac-covers/'; R=S+'/mods/layout-v3/remix/'; V2=S+'/mods/layout-v2/remix/'; O=S+'/mods/layout-v3/renders/'
FLIP=np.diag([-1,1,-1,1])   # 180 deg about Y: open side up, lid text reads upright (checked against the inlay plan)
def L(p, t=(0,0,0), dz=0.0):
    m=trimesh.load(p); m.apply_translation(t); m.apply_transform(FLIP); m.apply_translation([0,0,dz])
    v,f=trimesh.remesh.subdivide_to_size(m.vertices,m.faces,max_edge=4.0); return trimesh.Trimesh(v,f,process=False)
LIGHT=np.array([0.4,-0.5,0.8]); LIGHT/=np.linalg.norm(LIGHT)
def draw(ax, parts, lims, elev=32, azim=-58):
    for m,col in parts:
        n=m.face_normals; sh=0.35+0.65*np.clip(n@LIGHT,0,1)
        c=np.array(matplotlib.colors.to_rgb(col)); fc=np.clip(c[None,:]*sh[:,None],0,1)
        pc=Poly3DCollection(m.triangles, facecolors=fc, edgecolors='none', linewidths=0); ax.add_collection3d(pc)
    (x0,x1),(y0,y1),(z0,z1)=lims; ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); ax.set_zlim(z0,z1)
    ax.set_box_aspect((x1-x0,y1-y0,z1-z0)); ax.view_init(elev,azim); ax.set_axis_off()
def lims_of(ms, pad=3):
    b=np.vstack([m.bounds for m,_ in ms]); lo=b.min(0)-pad; hi=b.max(0)+pad; return list(zip(lo,hi))
def pair(name, left, right, titles, orig_col='#5a5a5a', new_col='#2b2b2b'):
    """left/right: (duct_parts, lid_parts). Same camera and scale; each column centred on its own piece."""
    fig=plt.figure(figsize=(12,8.5),dpi=110)
    for col,(dparts,lparts),title in [(0,left,titles[0]),(1,right,titles[1])]:
        allp=dparts+lparts; b=np.vstack([m.bounds for m,_ in allp]); c=(b.min(0)+b.max(0))/2
        span=max(np.ptp(np.vstack([m.bounds for m,_ in left[0]+left[1]+right[0]+right[1]]),axis=0)[:2].max(),30)
        lim=[(c[0]-span/2-2,c[0]+span/2+2),(c[1]-span/2-2,c[1]+span/2+2),(b.min(0)[2]-1,b.max(0)[2]+1)]
        for row,parts,lab in [(0,dparts,'lid off'),(1,allp,'lid on')]:
            ax=fig.add_subplot(2,2,row*2+col+1,projection='3d',computed_zorder=False); draw(ax,parts,lim); ax.set_title(f'{title} — {lab}',fontsize=10)
    plt.tight_layout(); fig.savefig(O+name,dpi=110); plt.close(fig); print(name)
ORIG,NEW,LID,ACC='#8a8a8a','#3a3a3a','#b0b0b0','#e07a10'
# 1 middle duct
pair('01_middle_154_vs_154N.png',
 ([(L(D+'CMD_V3_1H_154mm_DUCT.stl'),ORIG)],[(L(D+'CMD_V2_6B_154mm_DUCT_COVER.stl'),LID)]),
 ([(L(R+'V3L_154N_DUCT.stl'),NEW)],[(L(R+'V3L_154N_DUCT_COVER.stl'),LID)]),
 ('MSS CMD_V3_1H_154mm_DUCT (24.4 wide)','V3L_154N_DUCT (22.0 wide, slice-and-shift 2.4)'))
# 2 T_REG
pair('02_TREG_vs_TREG_N.png',
 ([(L(D+'CMD_V3_1H_T_REG.stl'),ORIG)],[(L(D+'CMD_V2_6B_T_REG_COVER.stl'),LID)]),
 ([(L(R+'V3L_T_REG_N.stl'),NEW)],[(L(R+'V3L_T_REG_N_COVER.stl'),LID)]),
 ('MSS CMD_V3_1H_T_REG','V3L_T_REG_N (stem 22, bar 81.6)'))
# 3 coupon vs 22 custom
pair('03_coupon_22_vs_22N.png',
 ([(L(V2+'V2L_22mm_DUCT.stl'),ORIG)],[(L(V2+'V2L_22mm_DUCT_COVER.stl'),LID)]),
 ([(L(R+'V3L_COUPON_22N_DUCT.stl'),NEW)],[(L(R+'V3L_COUPON_22N_DUCT_COVER.stl'),LID)]),
 ('22 mm full-width straight','V3L_COUPON_22N (snap-fit test)'))
# 4 curve
dx=-263.24
pair('04_curve_90DEG_vs_R15.png',
 ([(L(D+'CMD_V3_1H_90DEG.stl'),ORIG)],[(L(D+'CMD_V2_6B_90DEG_COVER.stl',(dx,0,0)),LID)]),
 ([(L(R+'V3L_90DEG_R15.stl'),'#c96a0e')],[(L(R+'V3L_90DEG_R15_COVER.stl',(dx,0,0)),LID)]),
 ('MSS CMD_V3_1H_90DEG (R22 + arms)','V3L_90DEG_R15 (arc only, R15.5)'))
# 5 wire box with WARNING lid (+ inlay)
wl=trimesh.load(A+'CMD_Remix-V3_DUCT-1V_WIRE_BOX_LID_WARNING.stl'); cv=trimesh.load(D+'CMD_V2_6B_WIRE_BOX_COVER.stl')
t=tuple((cv.bounds.mean(0)-wl.bounds.mean(0))*[1,1,0]+[0,0,cv.bounds[0][2]-wl.bounds[0][2]])
pair('05_wirebox_vs_port_WARNING.png',
 ([(L(D+'CMD_V3_1H_WIRE_BOX.stl'),'#e07a10')],[(L(A+'CMD_Remix-V3_DUCT-1V_WIRE_BOX_LID_WARNING.stl',t),'#222222'),(L(A+'CMD_Remix-V3_DUCT-1V_WIRE_BOX_LID_WARNING_INLAY.stl',t,0.15),'#e8c040')]),
 ([(L(R+'V3L_WIRE_BOX_PORT.stl'),'#e07a10')],[(L(A+'CMD_Remix-V3_DUCT-1V_WIRE_BOX_LID_WARNING.stl',t),'#222222'),(L(A+'CMD_Remix-V3_DUCT-1V_WIRE_BOX_LID_WARNING_INLAY.stl',t,0.15),'#e8c040')]),
 ('MSS CMD_V3_1H_WIRE_BOX + WARNING lid','V3L_WIRE_BOX_PORT (18 mm port) + same lid'))

# 6 assembled AC conduit, installed positions (global apparent mm), WARNING lid on the box, plain lids elsewhere
import sys; sys.path.insert(0,'.')
def G(p, R2, ref, g, t=(0,0,0), col='#e07a10', dz=0.0):
    m=trimesh.load(p); m.apply_translation(t)
    M=np.eye(4); M[:2,:2]=R2; m.apply_translation([-ref[0],-ref[1],0]); m.apply_transform(M); m.apply_translation([g[0],g[1],0])
    m.apply_transform(FLIP); m.apply_translation([0,0,dz]); v,f=trimesh.remesh.subdivide_to_size(m.vertices,m.faces,max_edge=4.0); return (trimesh.Trimesh(v,f,process=False),col)
ROT={0:np.eye(2),90:np.array([[0,-1],[1,0]]),180:-np.eye(2),-90:np.array([[0,1],[-1,0]])}
CR=(-306.5,-96.66); CRc=(-306.5+263.24,-96.66)
def sref(p): m=trimesh.load(p); return (m.bounds[0][0], m.bounds[0][1]+12.2)
tsr=(-51.14,408.38)
ducts=[G(R+'V3L_WIRE_BOX_PORT.stl',ROT[180],(0,0),(-45.36,73.84)),G(R+'V3L_90DEG_R15.stl',ROT[180],CR,(-22.9,177.0)),G(R+'V3L_90DEG_R15.stl',ROT[0],CR,(-22.9,146.0)),
 G(R+'V3L_34mm_DUCT_HOLE.stl',ROT[0],sref(R+'V3L_34mm_DUCT_HOLE.stl'),(-7.4,146.0)),G(D+'CMD_V3_1H_T_SHORT.stl',ROT[180],tsr,(-72.0,116.0)),
 G(R+'V3L_10mm_DUCT.stl',ROT[0],sref(R+'V3L_10mm_DUCT.stl'),(-42.0,116.0)),G(R+'V3L_10mm_DUCT.stl',ROT[90],sref(R+'V3L_10mm_DUCT.stl'),(-72.0,142.8))]
ec=trimesh.load(D+'CMD_Remix-V3_DUCT-1M_ENDCAP.stl'); 
lids=[G(A+'CMD_Remix-V3_DUCT-1V_WIRE_BOX_LID_WARNING.stl',ROT[180],(0,0),(-45.36,73.84),t=t,col='#222222'),
      G(A+'CMD_Remix-V3_DUCT-1V_WIRE_BOX_LID_WARNING_INLAY.stl',ROT[180],(0,0),(-45.36,73.84),t=t,col='#e8c040',dz=0.15),
      G(R+'V3L_90DEG_R15_COVER.stl',ROT[180],CRc,(-22.9,177.0),col='#222222'),G(R+'V3L_90DEG_R15_COVER.stl',ROT[0],CRc,(-22.9,146.0),col='#222222'),
      G(R+'V3L_34mm_DUCT_COVER.stl',ROT[0],sref(R+'V3L_34mm_DUCT_COVER.stl'),(-7.4,146.0),col='#222222'),
      G(D+'CMD_V2_6B_T_SHORT_COVER.stl',ROT[180],tsr,(-72.0,116.0),col='#222222'),
      G(R+'V3L_10mm_DUCT_COVER.stl',ROT[0],sref(R+'V3L_10mm_DUCT_COVER.stl'),(-42.0,116.0),col='#222222'),
      G(R+'V3L_10mm_DUCT_COVER.stl',ROT[90],sref(R+'V3L_10mm_DUCT_COVER.stl'),(-72.0,142.8),col='#222222')]
allp=ducts+lids; b=np.vstack([m.bounds for m,_ in allp]); lo=b.min(0)-4; hi=b.max(0)+4
fig=plt.figure(figsize=(13,6.5),dpi=110)
for i,(parts,lab) in enumerate([(ducts,'lids off'),(allp,'lids on (WARNING lid on the box, black lids)')]):
    ax=fig.add_subplot(1,2,i+1,projection='3d',computed_zorder=False); draw(ax,parts,list(zip(lo,hi)),elev=42,azim=-70); ax.set_title('Assembled AC conduit v3 — '+lab,fontsize=10)
plt.tight_layout(); fig.savefig(O+'06_AC_conduit_assembled.png',dpi=110); plt.close(fig); print('06')
