from PIL import Image, ImageDraw, ImageFont
import io,os,sys,numpy as np
SRC='/tmp/claude-0/-home-user-hci-deu-1/ac3d3610-ff08-5bc5-81c5-0b524c36c51e/images/8.jpg'
OUT=sys.argv[1]
FACE=(254,233,181); BR=(92,58,44); PINK=(255,166,170); BLUE=(120,190,235); GOLD=(255,200,60)
LE=(631,520); RE=(953,496)
def base():
    im=Image.open(SRC).convert('RGB'); return im
def erase(d,eyes=True,mouth=True):
    if eyes:
        for cx,cy in (LE,RE): d.ellipse((cx-40,cy-40,cx+40,cy+40),fill=FACE)
    if mouth: d.rectangle((733,518,856,568),fill=FACE)
def cutout(im):
    w,h=im.size; m=im.copy()
    for seed in [(0,0),(w-1,0),(0,h-1),(w-1,h-1),(w//2,2),(w//2,h-3),(2,h//2),(w-3,h//2)]:
        ImageDraw.floodfill(m,seed,(255,0,255),thresh=40)
    a=np.array(im.convert('RGBA')); mm=np.array(m)
    sel=(mm[:,:,0]==255)&(mm[:,:,1]==0)&(mm[:,:,2]==255); a[sel]=[255,255,255,0]
    return Image.fromarray(a)
def star(d,cx,cy,r,col):
    pts=[]
    import math
    for i in range(8):
        rr=r if i%2==0 else r*0.38; t=math.pi/4*i-math.pi/2
        pts.append((cx+rr*math.cos(t),cy+rr*math.sin(t)))
    d.polygon(pts,fill=col,outline=BR); 
def make(kind):
    im=base(); d=ImageDraw.Draw(im)
    if kind=='happy':
        erase(d)
        for cx,cy in (LE,RE): d.arc((cx-34,cy-26,cx+34,cy+30),200,340,fill=BR,width=12)
        d.pieslice((752,518,838,586),0,180,fill=BR); d.pieslice((768,540,822,584),0,180,fill=(240,120,130))
        for cx,cy in ((585,585),(1000,565)): d.ellipse((cx-42,cy-20,cx+42,cy+20),fill=PINK)
    elif kind=='surprised':
        erase(d)
        for cx,cy in (LE,RE):
            d.ellipse((cx-38,cy-38,cx+38,cy+38),fill=BR); d.ellipse((cx-18,cy-24,cx+2,cy-4),fill=(255,255,255))
        d.ellipse((774,528,820,574),outline=BR,width=11)
    elif kind=='confused':
        erase(d,eyes=False)
        d.line([(742,552),(768,536),(794,552),(820,536),(846,552)],fill=BR,width=11,joint='curve')
    elif kind=='sparkle':
        erase(d,eyes=False,mouth=False)
        for cx,cy in (LE,RE):
            d.ellipse((cx-16,cy-22,cx+2,cy-4),fill=(255,255,255)); d.ellipse((cx+8,cy+6,cx+16,cy+14),fill=(255,255,255))
    rg=cutout(im); d=ImageDraw.Draw(rg)
    # outside-the-head extras on a bigger transparent canvas
    W,H=rg.size; can=Image.new('RGBA',(W+260,H+120),(0,0,0,0)); can.paste(rg,(130,120)); d=ImageDraw.Draw(can); ox,oy=130,120
    try: f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',150)
    except: f=ImageFont.load_default()
    if kind=='surprised':
        d.rounded_rectangle((1230+ox-150,60+oy-110,1290+ox-150,210+oy-110),18,fill=(255,140,90),outline=BR,width=8)
        d.ellipse((1236+ox-150,228+oy-110,1284+ox-150,276+oy-110),fill=(255,140,90),outline=BR,width=8)
    if kind=='confused':
        d.text((1180+ox-150,20+oy-120),'?',font=f,fill=(255,140,90),stroke_width=8,stroke_fill=BR)
        d.polygon([(1160+ox-150,330+oy-120),(1130+ox-150,400+oy-120),(1190+ox-150,400+oy-120)],fill=BLUE)
        d.ellipse((1128+ox-150,370+oy-120,1192+ox-150,430+oy-120),fill=BLUE,outline=None)
    if kind in ('sparkle','happy'):
        for (cx,cy,r) in ([(1240,120,60),(310,170,40),(1290,330,34)] if kind=='sparkle' else [(1260,140,46),(300,190,34)]):
            star(d,cx+ox-150,cy+oy-120,r,GOLD)
    can=can.crop(can.getbbox())
    if kind=='confused': can=can.rotate(-7,resample=Image.BICUBIC,expand=True); can=can.crop(can.getbbox())
    full=can.copy(); full.thumbnail((300,300),Image.LANCZOS)
    b=io.BytesIO(); full.save(b,'WEBP',quality=88,method=6); open(f'{OUT}/m_{kind}.webp','wb').write(b.getvalue()); full.save(f'{OUT}/m_{kind}.png')
    # face-only (head) version from the un-decorated cut-out
    fw,fh=rg.size; bb=rg.getbbox(); head=rg.crop((bb[0],bb[1],bb[2],bb[1]+int((bb[3]-bb[1])*0.56))); head=head.crop(head.getbbox()); head.thumbnail((300,150),Image.LANCZOS)
    b=io.BytesIO(); head.save(b,'WEBP',quality=90,method=6); open(f'{OUT}/f_{kind}.webp','wb').write(b.getvalue())
    print(kind, full.size, len(open(f'{OUT}/m_{kind}.webp','rb').read()), head.size)
for k in ['happy','surprised','confused','sparkle']: make(k)
