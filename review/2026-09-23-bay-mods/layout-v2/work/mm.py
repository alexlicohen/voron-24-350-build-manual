import sys
from PIL import Image, ImageDraw, ImageFont
R='/Users/alex/projects/3d-printing/docs/manual/assets/remote/'
def mmimg(path, x0,x1,y0,y1, ppm=4, cx=957, cy=1043, s=3.25, grid=True):
    im=Image.open(path).convert('RGB')
    W=int((x1-x0)*ppm); H=int((y1-y0)*ppm); a=s/ppm
    im=im.transform((W,H), Image.AFFINE, (a,0,cx+x0*s, 0,a,cy+y0*s), resample=Image.BICUBIC)
    if grid:
        d=ImageDraw.Draw(im,'RGBA'); f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 11)
        for x in range((int(x0)//10+1)*10, int(x1), 10):
            u=(x-x0)*ppm; d.line([(u,0),(u,H)], fill=(0,255,255,110 if x%50 else 220), width=1)
            if x%50==0: d.text((u+2,2), str(x), fill=(0,255,255), font=f)
        for y in range((int(y0)//10+1)*10, int(y1), 10):
            v=(y-y0)*ppm; d.line([(0,v),(W,v)], fill=(255,0,255,110 if y%50 else 220), width=1)
            if y%50==0: d.text((2,v+2), str(y), fill=(255,0,255), font=f)
    return im
if __name__=='__main__':
    p,out=sys.argv[1],sys.argv[2]; x0,x1,y0,y1=map(float,sys.argv[3:7]); ppm=float(sys.argv[7]) if len(sys.argv)>7 else 4
    mmimg(R+p,x0,x1,y0,y1,ppm).save(out)
