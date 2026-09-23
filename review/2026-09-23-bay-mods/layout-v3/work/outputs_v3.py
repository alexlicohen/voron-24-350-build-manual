import pickle, json, math, numpy as np
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import Point, LineString, box as sbox
import os; S=os.environ['BAY_MODS_SCRATCH']  # dir holding mods/ (MSS downloads + layout-v2)
OUT=S+'/mods/layout-v3/'
d=pickle.load(open(OUT+'work/placed.pkl','rb')); P=d['P']
# ---- JSON ----
def R(x0,x1,y0,y1): return {"type":"straight","x":[round(x0,1),round(x1,1)],"y":[round(y0,1),round(y1,1)]}
def A(cx,cy,ri,ro,a0,a1): return {"type":"arc","cx":round(cx,1),"cy":round(cy,1),"r_inner":round(ri,1),"r_outer":round(ro,1),"a0":a0,"a1":a1}
def Q(p0,p1,w=24.4):
    p0=np.array(p0);p1=np.array(p1);t=(p1-p0)/np.linalg.norm(p1-p0);n=np.array([-t[1],t[0]])*w/2
    return {"type":"poly","pts":[list(np.round(p,1)) for p in (p0+n,p1+n,p1-n,p0-n)]}
h=12.2; hn=11.0; Rj=20.42; TH=40.8
pr=d['params']; xL,xR,yF,yM,yRr=pr['xL'],pr['xR'],pr['yF'],pr['yM'],pr['yRr']
j=np.array(d['joint']); up=np.array(d['up']); a_end=np.array([xR-100-21-Rj*math.sin(math.pi/4), yRr+Rj-Rj*math.cos(math.pi/4)])
dc=[R(xL+22,xL+38.8,yF-h,yF+h),A(xL+22,yF+22,9.8,34.2,180,270),R(xL-h,xL+h,yF+22,yF+42),
    R(xL+39.8,xL+39.8+154,yF-h,yF+h),R(xL+39.8+154,xR-38.8,yF-h,yF+h),
    R(xR-38.8,xR-22,yF-h,yF+h),A(xR-22,yF+22,9.8,34.2,270,360),R(xR-h,xR+h,yF+22,yF+42),
    R(xL-h,xL+h,yF+42,yM-TH),R(xL-h,xL+h,yM-TH,yM+TH),R(xL+h,xL+39.8,yM-hn,yM+hn),R(xL-h,xL+h,yM+TH,yM+TH+130),
    R(xR-h,xR+h,yF+42,yM-TH),R(xR-h,xR+h,yM-TH,yM+TH),R(xR-39.8,xR-h,yM-hn,yM+hn),R(xR-h,xR+h,yM+TH,yRr-22),
    A(xR-22,yRr-22,9.8,34.2,0,90),R(xR-42,xR-22,yRr-h,yRr+h),R(xR-100,xR-42,yRr-h,yRr+h),
    R(xR-121,xR-100,yRr-h,yRr+h),A(xR-121,yRr+Rj,Rj-h,Rj+h,225,270),Q(a_end,j),
    Q(j,2*j-a_end),A(*(2*j-np.array([xR-121,yRr+Rj])),Rj-h,Rj+h,45,90),R(up[0]-10+10,up[0]+21,up[1]-h,up[1]+h),R(up[0]-10,up[0],up[1]-h,up[1]+h)]
dc[-2]=R(up[0],up[0]+21,up[1]-h,up[1]+h)
mid=[R(xL+39.8,xL+39.8+154,yM-hn,yM+hn),R(xL+39.8+154,xR-39.8,yM-hn,yM+hn)]
ac=[R(-115.8,-38.4,152.8,201.2),A(-38.4,161.5,3.3,27.7,0,90),A(-7.4,161.5,3.3,27.7,180,270),R(-7.4,26.6,146-h,146+h),R(26.6,34.4,134.25,157.75),
    R(-102,-42,116-h,116+h),R(-84.2,-59.8,128.2,142.8),R(-42,-32,116-h,116+h),R(-84.2,-59.8,142.8,152.8),R(-109.8,-102,104.25,127.75),R(-52,-27.5,90,92.4)]
J={"runs":[
 {"id":"DC","kind":"dc","call":"switch","what":"One DC conduit: left, front, right and rear-right runs, three 90 corners (FL mirrored), two narrowed T_REG junctions, 45 S-jog to the notch. Open only at Z1 and the notch.",
  "carries":"Z0-Z3, A, B, umbilical, XY endstop, LED, nozzle probe, bed TH, filter fan (via the notch), PCB fan, Ethernet, Pi USB, HV",
  "note":"v3: rail NOT moved; middle run centred at y -2.2, T bars 81.6 long (stems narrowed to 22). PSU 6 mm left.","segments":dc},
 {"id":"MID","kind":"dc","call":"switch","what":"Printed middle run, 2 x V3L_154N (slice-and-shift, 22.0 mm outer at the bulge, 15.5 mm clear inside), stem to stem of the narrowed T_REGs.",
  "carries":"six stepper leads to the Leviathan rear-edge headers; PSU 24 V feeds, HV, SSR signal",
  "note":"1.6 mm to the Leviathan PCB edge, 1.7 mm to the PSU front (apparent, lid included). Print the 22 mm coupon first.","segments":mid},
 {"id":"AC","kind":"ac","call":"ac","what":"MSS AC look: original-proportion wire box (DANGER/WARNING lid or plain lid) at the WAGO bus, two re-radiused 90 curves (R15.5) down to a 34 mm run over the bed-lead hole; SSR run (T_SHORT) behind the SSR joins the box through a stub and an 18 mm port in the box's front wall; strip fin at the PSU.",
  "carries":"inlet->WAGO, WAGO->PSU L/N/FG (via box, stub, SSR run), WAGO L->SSR LOAD2, SSR LOAD1->bed L, bed N and PE->WAGO, frame PE",
  "note":">= 12 mm from every DC conduit (computed on placed meshes).","segments":ac}],
 "components_moved":[{"name":"PSU (DIN clips on the rear rail)","dx":-6,"dy":0},
                     {"name":"Frame PE ring lug on the rear extrusion (LDO x~+105 -> x~-20)","dx":-125,"dy":0}],
 "crossings":[
  {"at":[14.7,146],"how":"Bed deck hole AC-only (TH, probe, filter fan via the notch); the 34 mm AC run's base opening sits over it."},
  {"at":[-15,91.2],"how":"PSU strip: fin between terminal 6 (-V) and 7 (FG); DC forward to the middle run, AC rearward into the SSR run's open end."},
  {"at":[-86,70],"how":"SSR: INPUT (DC) front, LOAD (AC) rear; the SSR run's front wall is 2 mm behind it."},
  {"at":[-5,180],"how":"Upper AC curve vs DC rear-upper run: 13.7 mm apart, no crossing."},
  {"at":[40,165],"how":"AC hole run/endcap vs DC S-jog: 12.0-12.6 mm, no crossing."},
  {"at":[6,200],"how":"Rear notch: DC only, straight into the DC rear-upper run."},
  {"at":[-25,212],"how":"Frame PE from the box's rear wall to a lug at x~-20 behind the box, >= 20 mm from DC."}]}
json.dump(J,open(OUT+'layout-v3.json','w'),indent=1)
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
    if p['id']=='BOX': g=p['mid'].convex_hull
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
bx(-100,69,-114,-15.3,B,'Leviathan+Pi (not moved)',lpos=T(-15,-60))
bx(118,158,-93,-36,B,'USB adp',lpos=T(138,-65))
bx(-21.3,196,11,126.7,G,dash=True); bx(-27.3,190,11,126.7,B,'PSU LRS-200 (6 mm left)',lpos=T(85,60))
bx(-109,-62.5,25,102,B,'SSR',lpos=T(-86,62)); bx(-129,-38.4,202,220,B); bx(-145,-95,220,243,B,'inlet',lpos=T(-120,236))
for (xa,xb,ya,yb) in [(-201.7,-148,-231,-172),(175.6,229,-231,-172),(-201.7,-149.2,173.3,234),(176.7,229,173,234)]: bx(xa,xb,ya,yb,B,'Z')
bx(150,167,210,238,B,'eth',lpos=T(158.5,230)); bx(0,12,195,222,(200,0,160,255),'notch',lpos=T(6,232))
u,v=T(14.7,146); dr.ellipse([u-21,v-21,u+21,v+21],outline=(200,0,160,255),width=3)
lab={'FL':(-172,-126,'FL 90 (mirror)'),'FR':(200,-126,'FR 90'),'F1':(-60,-143,'154'),'F2':(92,-143,'154'),'L1':(-178,-72,'58c'),'TL':(-150,-2,'T (N)'),
     'L2':(-178,105,'130c'),'R1':(209,-72,'58c'),'TR':(181,-2,'T (N)'),'R2':(209,75,'70c'),'RR':(196,134,'RR 90'),'B1':(138,147,'58c'),
     'J1':(80,152,'45'),'J2':(42,180,'45'),'B2':(8,184,'10c'),'M1':(-60,-2,'154N (22 wide)'),'M2':(92,-2,'154N (22 wide)'),
     'BOX':(-77,177,'WIRE BOX (orig. size)'),'C1':(-26,171,'R15'),'C2':(-18,146,'R15'),'H1':(10,138,'34c'),'EC':(31,128,'cap'),
     'TS':(-72,112,'T_SHORT'),'S1':(-37,105,'10c'),'ST':(-72,148,'10c'),'EC2':(-106,133,'cap'),'FIN':(-40,86,'fin')}
for k,(x,y,t) in lab.items(): dr.text(T(x,y),t,fill=(0,0,0),font=f,anchor='mm',stroke_width=3,stroke_fill=(255,255,255))
dr.rectangle([0,0,W,44],fill=(255,255,255,230))
dr.text((8,5),'Layout v3 on LDO Rev D placement photo (rear at bottom, x right = printer right). Apparent mm, +/-6 % absolute; local gaps +/-1.5 mm.',fill=(0,0,0),font=fs)
dr.text((8,23),'Orange = AC conduit, black = DC conduit, hatched = remix/custom piece, dashed white = narrowed middle run, blue = components (grey dashed = LDO position), magenta = bed hole and Z-chain notch.',fill=(0,0,0),font=fs)
im.convert('RGB').save(OUT+'overlay-v3.png'); print('overlay',im.size)
