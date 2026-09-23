import trimesh, numpy as np, subprocess, re, json, os
import os; S=os.environ['BAY_MODS_SCRATCH']  # dir holding mods/502306-cable-duct and mods/505838-ac-covers
D=S+'/mods/502306-cable-duct/'; RX=S+'/mods/layout-v2/remix/'; OUT=S+'/mods/layout-v2/slice/'
PRUSA='/Applications/PrusaSlicer.app/Contents/MacOS/PrusaSlicer'; INI='/Users/alex/projects/3d-printing/slicer/voron-coreone-asa.ini'; NOBIN=S+'/mods/slice/nobin.ini'
def orient(path, mode):
    m=trimesh.load(path)
    if mode=='flip': m.apply_transform(trimesh.transformations.rotation_matrix(np.pi,[1,0,0]))
    if mode=='ec': m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]))
    if mode=='side': m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))
    m.apply_translation(-m.bounds[0]); return m
BLACK=[(D+'CMD_V3_1H_154mm_DUCT.stl','flip')]*4+[(D+'CMD_V2_6B_154mm_DUCT_COVER.stl',None)]*4+\
 [(RX+'V2L_130mm_DUCT.stl','flip'),(RX+'V2L_130mm_DUCT_COVER.stl',None),(RX+'V2L_70mm_DUCT.stl','flip'),(RX+'V2L_70mm_DUCT_COVER.stl',None),
  (RX+'V2L_22mm_DUCT.stl','flip'),(RX+'V2L_22mm_DUCT_COVER.stl',None)]+[(RX+'V2L_58mm_DUCT.stl','flip'),(RX+'V2L_58mm_DUCT_COVER.stl',None)]*3+\
 [(D+'CMD_V3_1H_90DEG.stl','flip'),(D+'CMD_V2_6B_90DEG_COVER.stl',None)]*2+[(RX+'V2L_90DEG_MIRROR.stl','flip'),(RX+'V2L_90DEG_COVER_MIRROR.stl',None)]+\
 [(D+'CMD_V3_1H_T_REG.stl','flip'),(D+'CMD_V2_6B_T_REG_COVER.stl',None)]*2+[(D+'CMD_Remix-V3_DUCT-2B_45deg.stl',None),(D+'CMD_Remix-V3_DUCT-2B_45deg_LID.stl',None)]*2
ORANGE=[(RX+'V2L_AC_HUB.stl','flip'),(RX+'V2L_AC_HUB_COVER.stl',None),(RX+'V2L_58mm_DUCT_HOLE.stl','flip'),(RX+'V2L_58mm_DUCT_COVER.stl',None),
        (D+'CMD_Remix-V3_DUCT-1M_ENDCAP.stl','ec'),(RX+'V2L_STRIP_FIN.stl','side')]
MID=[(D+'CMD_V3_1H_154mm_DUCT.stl','flip')]*2+[(D+'CMD_V2_6B_154mm_DUCT_COVER.stl',None)]*2
def pack(items, gap=5.0):
    ms=[(f,md,orient(f,md)) for f,md in items]
    ms.sort(key=lambda t:(-t[2].extents[1], -t[2].extents[0]))
    plates=[]; cur=[]; x=y=4.0; rowh=0
    for f,md,m in ms:
        w,h=m.extents[0],m.extents[1]
        if x+w>246: x=4.0; y+=rowh+gap; rowh=0
        if y+h>216: plates.append(cur); cur=[]; x=y=4.0; rowh=0
        cur.append((f,m,x,y)); x+=w+gap; rowh=max(rowh,h)
    plates.append(cur); return plates
def stats(g):
    t=open(g,errors='ignore').read()
    return (re.search(r'; estimated printing time \(normal mode\) = (.*)',t).group(1), float(re.search(r'; total filament used \[g\] = ([\d.]+)',t).group(1)), float(re.search(r'; filament used \[cm3\] = ([\d.]+)',t).group(1)))
res={}
for col,items in [('black_dc',BLACK),('orange_ac',ORANGE),('black_mid_cond',MID)]:
    for i,pl in enumerate(pack(items)):
        name=f'{col}_{i+1}'; files=[]
        for k,(f,m,x,y) in enumerate(pl):
            mm=m.copy(); mm.apply_translation([x,y,0]); p=f'{OUT}{name}_{k:02d}.stl'; mm.export(p); files.append(p)
        g=OUT+name+'.gcode'
        r=subprocess.run([PRUSA,'--load',INI,'--load',NOBIN,'--merge','--dont-arrange','--export-gcode','-o',g]+files,capture_output=True,text=True)
        if r.returncode: print(name,'FAILED',r.returncode,r.stderr[-600:]); continue
        tm,gr,cm3=stats(g); res[name]=dict(time=tm,grams_asa=gr,cm3=cm3,grams_petg=round(cm3*1.27,1),parts=[os.path.basename(f) for f,_,_,_ in pl])
        print(f'{name:18s} {tm:>12s} ASA {gr:6.1f} g  {cm3:6.1f} cm3  PETG {cm3*1.27:6.1f} g  n={len(pl)}')
json.dump(res,open(OUT+'results.json','w'),indent=1)
