"""Remixes for layout v2. Derived from MyStoopidStuff's CMD remix (Printables 502306) of
RyanDam's Cable Management Duct; GPL-3.0 carried over. All outputs keep the PARENT's frame
(ducts/box: base at z-max as published -> flip base-down to print, as v1; covers: print as-is)."""
import trimesh, numpy as np, manifold3d as mf, os
import os; S=os.environ['BAY_MODS_SCRATCH']  # dir holding mods/502306-cable-duct and mods/505838-ac-covers
D=S+'/mods/502306-cable-duct/'; OUT=S+'/mods/layout-v2/remix/'
def to_mf(m): return mf.Manifold(mf.Mesh(vert_properties=np.asarray(m.vertices,np.float32), tri_verts=np.asarray(m.faces,np.uint32)))
def from_mf(M):
    g=M.to_mesh(); return trimesh.Trimesh(np.asarray(g.vert_properties)[:,:3], np.asarray(g.tri_verts), process=True)
def half(M, x, keep_left):
    big=1e4; box=mf.Manifold.cube([big,big,big]).translate([x-big if keep_left else x, -big/2, -big/2])
    return M ^ box
def shorten(src, remove, off=11.0):
    """cut [x0+off, x0+off+remove] out of a straight (remove = multiple of 12) and rejoin."""
    m=trimesh.load(D+src); assert m.is_volume, src
    x0=m.bounds[0][0]; M=to_mf(m); a=x0+off; b=a+remove
    L=half(M,a,True); R=half(M,b,False).translate([-remove,0,0])
    out=from_mf(L+R); assert out.is_volume
    return out
def xmirror(src):
    m=trimesh.load(D+src); m.apply_transform(trimesh.transformations.reflection_matrix([m.centroid[0],0,0],[1,0,0])); m.fix_normals(); return m
def vstretch(m, axis, at, delta):
    v=m.vertices.copy(); sel=v[:,axis]>at; v[sel,axis]+=delta; return trimesh.Trimesh(v, m.faces, process=False)
res={}
# custom straights (lengths 12n+10 keep the 12 mm tine pitch; seam planes are section-identical, verified)
for name,src,cov,rem in [('58mm','CMD_V3_1H_154mm_DUCT.stl','CMD_V2_6B_154mm_DUCT_COVER.stl',96),
                         ('130mm','CMD_V3_1H_142mm_DUCT.stl','CMD_V2_6B_142mm_DUCT_COVER.stl',12),
                         ('70mm','CMD_V3_1H_82mm_DUCT.stl','CMD_V2_6B_82mm_DUCT_COVER.stl',12),
                         ('22mm','CMD_V3_1H_82mm_DUCT.stl','CMD_V2_6B_82mm_DUCT_COVER.stl',60)]:
    d=shorten(src,rem); c=shorten(cov,rem)
    d.export(OUT+f'V2L_{name}_DUCT.stl'); c.export(OUT+f'V2L_{name}_DUCT_COVER.stl')
    res[name]=(round(d.extents[0],2), round(c.extents[0],2))
# mirrored 90 deg corner + cover (front-left corner)
xmirror('CMD_V3_1H_90DEG.stl').export(OUT+'V2L_90DEG_MIRROR.stl'); xmirror('CMD_V2_6B_90DEG_COVER.stl').export(OUT+'V2L_90DEG_COVER_MIRROR.stl')
# AC hub = CMD_V3_1H_WIRE_BOX stretched: +18 mm in x through the slot at x=39.04 (widens that slot to 22 mm),
# +48.8 mm in y through the vertex-free band -111.16..-95.17 (short walls + base extend). Pure vertex moves: topology kept.
HX, HY = 18.0, 48.8
box=trimesh.load(D+'CMD_V3_1H_WIRE_BOX.stl', process=True)
hub=vstretch(vstretch(box,0,39.04,HX),1,-103.2,HY)
# close the stretched end notch above y=... : notch end is at x-min (-6.96..-4.56). keep open for yA in [-86.2,-43.2]?? -> computed in layout frame
# layout frame: xG=-xA-33.96, yG=-yA+73.83 ; open wanted yG 117..160 -> yA -86.2..-43.8 ; close yG 160..190.5 -> yA -116.7..-86.2
fill=trimesh.creation.box(extents=[2.4, 30.5, 25.0]); fill.apply_translation([-6.96+1.2, (-116.67-86.17)/2, (18.28-6.72)/2])
hub=trimesh.util.concatenate([hub, fill])
hub.export(OUT+'V2L_AC_HUB.stl')
cov=trimesh.load(D+'CMD_V2_6B_WIRE_BOX_COVER.stl')
hubc=vstretch(vstretch(cov,0,39.04,HX),1,-103.2,HY); hubc.export(OUT+'V2L_AC_HUB_COVER.stl')
res['hub']=(hub.bounds.round(2).tolist(), hubc.bounds.round(2).tolist())
# PSU strip divider fin (new part, simple): plate 2.4 x 25 x 55 with a 12 mm foot on the DC side; printed on its side.
plate=trimesh.creation.box(extents=[25.0,2.4,55.0]); plate.apply_translation([12.5,1.2,27.5])
foot=trimesh.creation.box(extents=[22.0,12.0,2.4]); foot.apply_translation([11.0,-6.0+0.0,1.2])
rib=trimesh.creation.box(extents=[2.4,12.0,20.0]); rib.apply_translation([1.2,-6.0,10.0])
fin=from_mf(to_mf(plate)+to_mf(foot)+to_mf(rib)); fin.export(OUT+'V2L_STRIP_FIN.stl'); res['fin']=fin.extents.round(1).tolist()
for k,v in res.items(): print(k,v)
for f in sorted(os.listdir(OUT)):
    m=trimesh.load(OUT+f); print(f, m.extents.round(2), 'watertight' if m.is_watertight else 'OPEN', round(m.volume/1000,2) if m.is_volume else '-')
# AC hole run: custom 58 with a 17 x 16 mm opening through its base over the bed-lead deck hole
# (hole centre 44.7 mm from the run's start at global x -30; the base lattice windows are too small for L/N/PE + ring lug).
h=trimesh.load(OUT+'V2L_58mm_DUCT.stl'); x0=h.bounds[0][0]; yc=h.bounds[0][1]+12.2; zt=h.bounds[1][2]
cut=mf.Manifold.cube([17.0,16.0,6.0]).translate([x0+44.7-8.5, yc-8.0, zt-5.0])
hh=from_mf(to_mf(h)-cut); assert hh.is_volume; hh.export(OUT+'V2L_58mm_DUCT_HOLE.stl'); print('hole run', hh.extents.round(2), round(hh.volume/1000,2))
