"""Layout v3 remixes. Derived from MyStoopidStuff's CMD remix (Printables 502306, 505838) of RyanDam's
Cable Management Duct (GPL-3.0). Outputs keep the parent's frame: ducts / box / curves base at z-max
(flip base-down to print), covers and lids as-is."""
import trimesh, numpy as np, manifold3d as mf, os, shutil, math
from splitnm import to_mf, from_mf
from unpinch2 import unpinch
import os; S=os.environ['BAY_MODS_SCRATCH']  # dir holding mods/ (MSS downloads + layout-v2)
D=S+'/mods/502306-cable-duct/'; A=S+'/mods/505838-ac-covers/'; V2=S+'/mods/layout-v2/remix/'; OUT=S+'/mods/layout-v3/remix/'
BIG=1e4
def halfspace(axis, c, keep_low):
    lo=[-BIG/2]*3; lo[axis]= c-BIG if keep_low else c
    return mf.Manifold.cube([BIG]*3).translate(lo)
def slice_shift(M, axis, c, delta):
    """remove slab [c, c+delta] along axis, pull the high side back by delta, re-close (union)."""
    t=[0,0,0]; t[axis]=-delta
    E=0.05  # 0.1 mm overlap so the union fuses instead of leaving two shells touching on the seam
    return (M ^ halfspace(axis,c+E,True)) + (M ^ halfspace(axis,c+delta-E,False)).translate(t)
def load_mf(p): m=trimesh.load(p); assert m.is_volume, p; return to_mf(m)
def save(M,name):
    m=from_mf(M); assert m.is_volume, name; m.export(OUT+name); return m
DW=2.4          # width reduction of the middle run (24.4 -> 22.0 outer at the tine bulge)
CY=207.18       # long mid-plane cut (duct centre 208.38; seam-mismatch minimum)
CT=-52.34       # T_REG stem cut (stem centre -51.14; seam-mismatch minimum)
res={}
# 1. middle run: 154 duct + cover narrowed by slice-and-shift along the long mid-plane
res['154N']=save(slice_shift(load_mf(D+'CMD_V3_1H_154mm_DUCT.stl'),1,CY,DW),'V3L_154N_DUCT.stl').extents
res['154N_c']=save(slice_shift(load_mf(D+'CMD_V2_6B_154mm_DUCT_COVER.stl'),1,CY,DW),'V3L_154N_DUCT_COVER.stl').extents
# T_REG: stem narrowed by the same cut (bar 84 -> 81.6 long, bar width unchanged)
res['TN']=save(slice_shift(load_mf(D+'CMD_V3_1H_T_REG.stl'),0,CT,DW),'V3L_T_REG_N.stl').extents
res['TN_c']=save(slice_shift(load_mf(D+'CMD_V2_6B_T_REG_COVER.stl'),0,CT,DW),'V3L_T_REG_N_COVER.stl').extents
# test coupon: 22 mm narrowed duct + lid (from the v2 22 mm custom straight)
res['coupon']=save(slice_shift(load_mf(V2+'V2L_22mm_DUCT.stl'),1,CY,DW),'V3L_COUPON_22N_DUCT.stl').extents
res['coupon_c']=save(slice_shift(load_mf(V2+'V2L_22mm_DUCT_COVER.stl'),1,CY,DW),'V3L_COUPON_22N_DUCT_COVER.stl').extents
# 2. short straights (12 mm tine pitch kept; seam planes at 1 mm from the end are section-identical)
def shorten(src, remove, off):
    M=load_mf(src); x0=trimesh.load(src).bounds[0][0]; a=x0+off
    return (M ^ halfspace(0,a+0.05,True)) + (M ^ halfspace(0,a+remove-0.05,False)).translate([-remove,0,0])
save(shorten(D+'CMD_V3_1H_82mm_DUCT.stl',72,1.0),'V3L_10mm_DUCT.stl'); save(shorten(D+'CMD_V2_6B_82mm_DUCT_COVER.stl',72,1.0),'V3L_10mm_DUCT_COVER.stl')
h34=shorten(D+'CMD_V3_1H_82mm_DUCT.stl',48,11.0); save(shorten(D+'CMD_V2_6B_82mm_DUCT_COVER.stl',48,11.0),'V3L_34mm_DUCT_COVER.stl')
m34=from_mf(h34); x0=m34.bounds[0][0]; yc=m34.bounds[0][1]+12.2; zt=m34.bounds[1][2]
save(h34 - mf.Manifold.cube([17.0,16.0,6.0]).translate([x0+22.1-8.5,yc-8.0,zt-5.0]),'V3L_34mm_DUCT_HOLE.stl')
# 3. re-radiused 90 deg curve: keep only the arc of CMD_V3_1H_90DEG (drop the 16.8 / 20 mm straight arms),
#    then shift every vertex radially by -6.5 about the arc centre: centreline R 22 -> 15.5, wall/floor sections unchanged.
RR=6.5
def reradius(src, C):
    ac=(C[0]+22.0, C[1]+22.0)
    M=load_mf(src) ^ halfspace(0,ac[0],True) ^ halfspace(1,ac[1],True)
    m=from_mf(M); v=m.vertices.copy(); d=v[:,:2]-ac; r=np.linalg.norm(d,axis=1); v[:,:2]=ac+d*((r-RR)/r)[:,None]
    out=trimesh.Trimesh(v,m.faces,process=True); assert out.is_volume; return out
reradius(D+'CMD_V3_1H_90DEG.stl',(-313.0,-103.16)).export(OUT+'V3L_90DEG_R15.stl')
reradius(D+'CMD_V2_6B_90DEG_COVER.stl',(-49.76,-103.16)).export(OUT+'V3L_90DEG_R15_COVER.stl')
# 4. wire box, original proportions: repair the parent's 4 pinched edges, cut one 18 mm port through the
#    front tined wall for the SSR-run stub (author x 26.64 = global x -72), floor kept.
box,_=unpinch(trimesh.load(D+'CMD_V3_1H_WIRE_BOX.stl'),(0,1,0,0)); B=to_mf(box)
port=mf.Manifold.cube([18.0,8.0,22.0]).translate([26.64-9.0,-83.0,-7.5])
save(B-port,'V3L_WIRE_BOX_PORT.stl')
# 5. unchanged carry-overs
shutil.copy(V2+'V2L_STRIP_FIN.stl',OUT+'V2L_STRIP_FIN.stl')
for k,v in res.items(): print(k, np.round(v,2))
for f in sorted(os.listdir(OUT)):
    m=trimesh.load(OUT+f); print(f'{f:32s}', m.extents.round(2), 'watertight' if m.is_watertight else 'OPEN')
