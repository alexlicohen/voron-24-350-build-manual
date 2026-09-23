import pickle, json, math, numpy as np
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import Point, LineString, box as sbox
import os; S=os.environ['BAY_MODS_SCRATCH']  # dir holding mods/502306-cable-duct and mods/505838-ac-covers
OUT=S+'/mods/layout-v2/'
d=pickle.load(open(OUT+'work/placed.pkl','rb')); P=d['P']
# ---- hole containment (channel interior of H1: centre y 146, inner half-width ~8.5 at base) ----
print('hole y-margin to inner walls:', round(8.5-7.0,1), 'x-margin to right end (28 - 21.7):', round(28-21.7,1))
# ---- JSON ----
def R(x0,x1,y0,y1): return {"type":"straight","x":[round(x0,1),round(x1,1)],"y":[round(y0,1),round(y1,1)]}
def A(cx,cy,ri,ro,a0,a1): return {"type":"arc","cx":round(cx,1),"cy":round(cy,1),"r_inner":round(ri,1),"r_outer":round(ro,1),"a0":a0,"a1":a1}
def Q(p0,p1,w=24.4):
    p0=np.array(p0);p1=np.array(p1);t=(p1-p0)/np.linalg.norm(p1-p0);n=np.array([-t[1],t[0]])*w/2
    return {"type":"poly","pts":[list(np.round(p,1)) for p in (p0+n,p1+n,p1-n,p0-n)]}
h=12.2; Rj=20.42
xL,xR,yF,yM,yRr=-178.4,209.2,-147.0,-5.0,145.8
j=np.array([61.45,164.09]); a_end=np.array([109.2-21-Rj*math.sin(math.pi/4), 145.8+Rj-Rj*math.cos(math.pi/4)])
dc=[R(xL+22,xL+38.8,yF-h,yF+h),A(xL+22,yF+22,9.8,34.2,180,270),R(xL-h,xL+h,yF+22,yF+42),
    R(xL+39.8,xL+39.8+154,yF-h,yF+h),R(xL+39.8+154,xR-38.8,yF-h,yF+h),
    R(xR-38.8,xR-22,yF-h,yF+h),A(xR-22,yF+22,9.8,34.2,270,360),R(xR-h,xR+h,yF+22,yF+42),
    R(xL-h,xL+h,yF+42,yM-42),R(xL-h,xL+h,yM-42,yM+42),R(xL+h,xL+39.8,yM-h,yM+h),R(xL-h,xL+h,yM+42,yM+42+130),
    R(xR-h,xR+h,yF+42,yM-42),R(xR-h,xR+h,yM-42,yM+42),R(xR-39.8,xR-h,yM-h,yM+h),R(xR-h,xR+h,yM+42,yRr-22),
    A(xR-22,yRr-22,9.8,34.2,0,90),R(xR-42,xR-22,yRr-h,yRr+h),R(xR-100,xR-42,yRr-h,yRr+h),
    R(109.2-21,109.2,yRr-h,yRr+h),A(88.2,yRr+Rj,Rj-h,Rj+h,225,270),Q(a_end,j),
    Q(j,2*j-a_end),A(*(2*j-np.array([88.2,yRr+Rj])),Rj-h,Rj+h,45,90),R(13.7,34.7,182.38-h,182.38+h),R(-8.3,13.7,182.38-h,182.38+h)]
mid=[R(xL+39.8,xL+39.8+154,yM-h,yM+h),R(xL+39.8+154,xR-39.8,yM-h,yM+h)]
ac=[R(-125.4,-30,104,201.2),R(-30,28,146-h,146+h),R(28,35.8,134.25,157.75),R(-50,-25.5,90,92.4)]
J={"runs":[
 {"id":"DC","kind":"dc","call":"switch","what":"One DC conduit: left, front, right and rear-right runs joined by three 90° corners (FL mirrored, FR, RR), two T_REG junctions and a 45° S-jog up to the rear notch. Open ends only at Z1 (rear-left) and the notch.",
  "carries":"Z0-Z3, A, B, umbilical, XY endstop, LED, nozzle probe, bed TH, filter fan (these three rerouted via the notch), PCB fan, Ethernet, Pi USB, HV",
  "note":"Pieces: 90DEG x2 + mirrored 90DEG, T_REG x2, 154 x2, custom 58 x3 / 130 / 70 / 22, 45deg x2. Apparent mm, +/-6 % absolute.","segments":dc},
 {"id":"MID","kind":"dc","call":"cond","what":"Middle run between the rails, T_REG stem to T_REG stem (2 x 154).",
  "carries":"all six stepper leads to the Leviathan's rear-edge headers; PSU 24 V feeds, HV, SSR signal",
  "note":"Needs the front DIN rail 7 mm toward the door (gap board-edge to PSU >= 32 mm). Fallback: replace each T_REG with an 82 straight and keep LDO's PVC middle duct.","segments":mid},
 {"id":"AC","kind":"ac","call":"ac","what":"One AC conduit: V2L_AC_HUB (stretched MSS wire box) against the WAGO bus + a 58 mm hole run over the bed-lead deck hole + endcap; strip fin at the PSU.",
  "carries":"inlet->WAGO, WAGO->PSU L/N/FG, WAGO L->SSR LOAD2, SSR LOAD1->bed L, bed N and PE->WAGO, frame PE",
  "note":"Hub front wall 2 mm behind the SSR, rear wall 0.8 mm in front of the WAGO; PSU AC leads enter the hub's open right end; the fin sits between terminal 6 (-V) and 7 (FG).","segments":ac}],
 "components_moved":[{"name":"Front DIN rail with Leviathan+Pi and USB adapter","dx":0,"dy":-7},
                     {"name":"PSU (DIN clips on the rear rail)","dx":-4,"dy":0},
                     {"name":"Frame PE ring lug on the rear extrusion (LDO x~+105 -> x~-20)","dx":-125,"dy":0}],
 "crossings":[
  {"at":[14.7,146],"how":"Bed deck hole becomes AC-only: bed TH, nozzle probe and filter fan re-routed above deck to the Z-chain notch; bed L/N/PE rise straight into the AC hole run, which covers the hole."},
  {"at":[-15,91.2],"how":"PSU terminal strip: printed fin between terminal 6 (-V, y 86.7) and 7 (FG, y 95.8); DC leads leave forward to the middle run, AC leads rearward into the hub."},
  {"at":[-86,70],"how":"SSR: INPUT 3/4 (DC) at its front end, LOAD 1/2 (AC) at its rear end; the SSR body is the barrier, the hub's front wall is 2 mm behind it."},
  {"at":[40,165],"how":"AC hole run/endcap vs DC S-jog and rear-upper run: parallel, 10-11 mm apart, no crossing."},
  {"at":[6,200],"how":"Rear notch: DC only (Z chain: umbilical, XY endstop, A, B; LED; rerouted TH/probe/fan) straight into the DC rear-upper run."},
  {"at":[-25,212],"how":"Frame PE leaves the hub's rear wall to a lug on the rear extrusion at x~-20, behind the hub, >= 10 mm from the DC run's open end."}]}
json.dump(J,open(OUT+'layout-v2.json','w'),indent=1)
# ---- harness path deltas (centreline polylines) ----
def L(pts): return sum(math.dist(pts[i],pts[i+1]) for i in range(len(pts)-1))
jog=2*(21+Rj*math.pi/4+17.4)
rr=16.8+22*math.pi/2+20
v2_notch_to_Rrun107=22.6+7.5+jog+58+rr   # notch drop -> upper run -> jog -> B1 -> RR -> (209.2,107)
ldo={'A':L([(6,205),(6,172),(-169,172),(-169,-2.5),(-76,-2.5),(-76,-17)]),'B':L([(6,205),(6,172),(-169,172),(-169,-2.5),(-43,-2.5),(-43,-17)])}
v2={'A':v2_notch_to_Rrun107+112+(209.2+76)+19,'B':v2_notch_to_Rrun107+112+(209.2+43)+19}
ldo['TH']=L([(15,146),(15,172),(202,172),(202,-145),(-7,-145),(-7,-112)]); v2['TH']=55+v2_notch_to_Rrun107+212+rr+(170.4+7)+32
for k in ldo: print(f'{k}: LDO {ldo[k]:.0f}  v2 {v2[k]:.0f}  delta {v2[k]-ldo[k]:+.0f} mm')
# ---- overlay ----
Rimg='/Users/alex/projects/3d-printing/docs/manual/assets/remote/09-electronics-bay/bay-general-placement.jpg'
cx,cy,s=957,1043,3.25; x0,x1,y0,y1=-250,250,-250,250; ppm=3
im=Image.open(Rimg).convert('RGB'); W=int((x1-x0)*ppm); H=int((y1-y0)*ppm); a=s/ppm
im=im.transform((W,H),Image.AFFINE,(a,0,cx+x0*s,0,a,cy+y0*s),resample=Image.BICUBIC)
im=Image.blend(im,Image.new('RGB',im.size,(255,255,255)),0.40)
ov=Image.new('RGBA',im.size,(0,0,0,0)); dr=ImageDraw.Draw(ov)
f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',14); fs=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',12)
T=lambda x,y:((x-x0)*ppm,(y-y0)*ppm)
def polys(g): return getattr(g,'geoms',[g])
hatch=Image.new('RGBA',im.size,(0,0,0,0)); hd=ImageDraw.Draw(hatch)
for k in range(-H,W,9): hd.line([(k,0),(k+H,H)],fill=(255,255,255,200),width=2)
for p in P:
    fill={'dc':(25,25,25,150),'ac':(245,120,0,170)}[p['kind']]; outl={'dc':(0,0,0,255),'ac':(170,60,0,255)}[p['kind']]
    g=p['mid'].union(p['hi']) if p['id']!='FIN' else p['mid']
    if p['id']=='HUB': g=p['mid'].convex_hull
    for q in polys(g):
        pts=[T(*c) for c in q.exterior.coords]
        dr.polygon(pts,fill=fill,outline=outl,width=2)
        if p['custom']:
            m=Image.new('L',im.size,0); ImageDraw.Draw(m).polygon(pts,fill=255); ov.paste(hatch,(0,0),Image.composite(hatch.getchannel('A'),Image.new('L',im.size,0),m))
    if p['run']=='MID':
        for q in polys(g): 
            pts=[T(*c) for c in q.exterior.coords]
            for i in range(0,len(pts)-1,2): dr.line([pts[i],pts[i+1]],fill=(255,255,255,255),width=2)
im=Image.alpha_composite(im.convert('RGBA'),ov); dr=ImageDraw.Draw(im)
def bx(xa,xb,ya,yb,col,lab=None,dash=False,lpos=None):
    (u0,v0),(u1,v1)=T(xa,ya),T(xb,yb)
    if dash:
        for t in range(int(u0),int(u1),10): dr.line([(t,v0),(min(t+5,u1),v0)],fill=col,width=2); dr.line([(t,v1),(min(t+5,u1),v1)],fill=col,width=2)
        for t in range(int(v0),int(v1),10): dr.line([(u0,t),(u0,min(t+5,v1))],fill=col,width=2); dr.line([(u1,t),(u1,min(t+5,v1))],fill=col,width=2)
    else: dr.rectangle([u0,v0,u1,v1],outline=col,width=2)
    if lab: dr.text(lpos or ((u0+u1)/2,(v0+v1)/2),lab,fill=(0,0,0),font=fs,anchor='mm',stroke_width=3,stroke_fill=(255,255,255))
B=(20,80,220,255); G=(120,120,120,255)
bx(-100,69,-114,-15.3,G,dash=True); bx(-100,69,-121,-22.3,B,'Leviathan+Pi (7 mm fwd)',lpos=T(-15,-60))
bx(118,158,-93,-36,G,dash=True); bx(118,158,-100,-43,B,'USB adp',lpos=T(138,-72))
bx(-21.3,196,11,126.7,G,dash=True); bx(-25.3,192,11,126.7,B,'PSU LRS-200 (4 mm left)',lpos=T(85,60))
bx(-109,-62.5,25,102,B,'SSR',lpos=T(-86,62)); bx(-129,-38.4,202,220,B); bx(-145,-95,220,243,B,'inlet',lpos=T(-120,236))
for (xa,xb,ya,yb) in [(-201.7,-148,-231,-172),(175.6,229,-231,-172),(-201.7,-149.2,173.3,234),(176.7,229,173,234)]: bx(xa,xb,ya,yb,B,'Z')
bx(150,167,210,238,B,'eth',lpos=T(158.5,230)); bx(0,12,195,222,(200,0,160,255),'notch',lpos=T(6,232))
u,v=T(14.7,146); dr.ellipse([u-21,v-21,u+21,v+21],outline=(200,0,160,255),width=3)
lab={'FL':(-172,-130,'FL 90 (mirror)'),'FR':(200,-130,'FR 90'),'F1':(-60,-147,'154'),'F2':(92,-147,'154'),'L1':(-178,-76,'58c'),'TL':(-150,-5,'T'),
     'L2':(-178,102,'130c'),'R1':(209,-76,'58c'),'TR':(183,-5,'T'),'R2':(209,72,'70c'),'RR':(196,132,'RR 90'),'B1':(138,146,'58c'),
     'J1':(80,150,'45'),'J2':(42,178,'45'),'B2':(2,182,'22c'),'M1':(-60,-5,'154 (mid, cond.)'),'M2':(92,-5,'154 (mid, cond.)'),
     'HUB':(-78,165,'AC HUB (remix)'),'H1':(-2,146,'AC 58c'),'EC':(32,128,'cap'),'FIN':(-38,86,'fin')}
for k,(x,y,t) in lab.items(): dr.text(T(x,y),t,fill=(0,0,0),font=f,anchor='mm',stroke_width=3,stroke_fill=(255,255,255))
dr.rectangle([0,0,W,44],fill=(255,255,255,230))
dr.text((8,5),'Layout v2 on LDO Rev D placement photo (rear at bottom, x right = printer right). Apparent mm, +/-6 % absolute; local gaps +/-1.5 mm.',fill=(0,0,0),font=fs)
dr.text((8,23),'Orange = AC conduit, black = DC conduit, hatched = remix/custom piece, dashed white = conditional middle run, blue = components (grey dashed = LDO position), magenta = bed hole and Z-chain notch.',fill=(0,0,0),font=fs)
im.convert('RGB').save(OUT+'overlay-v2.png'); print('overlay',im.size)
