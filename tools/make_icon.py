"""Genera el ícono de la app (legacy + adaptativo) en android/res/mipmap-*.
Uso: python3 tools/make_icon.py   (requiere Pillow y la fuente Poppins Bold)"""
import os
from PIL import Image, ImageDraw, ImageFont
OUT = "android"
# --- ícono ---
S = 1024
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
COLS = [("#7fd096","#0d3b1c","A"),("#f6c453","#4a3300","B"),("#89b6ee","#0e2b52","C"),("#f49cb4","#5b0f27","D")]
def bg_layer(size):
    g = Image.new("RGB",(size,size))
    d = ImageDraw.Draw(g)
    for y in range(size):
        t = y/size
        c = tuple(int(a+(b-a)*t) for a,b in zip((19,48,90),(8,20,40)))
        d.line([(0,y),(size,y)],fill=c)
    return g
def tiles(size, box):  # box = (x0,y0,x1,y1) zona del contenido
    lay = Image.new("RGBA",(size,size),(0,0,0,0))
    d = ImageDraw.Draw(lay)
    x0,y0,x1,y1 = box; w=x1-x0; gap=w*0.07; t=(w-gap)/2; r=t*0.24
    f = ImageFont.truetype(FONT,int(t*0.62))
    for i,(fill,ink,ch) in enumerate(COLS):
        cx = x0+(i%2)*(t+gap); cy = y0+(i//2)*(t+gap)
        d.rounded_rectangle([cx,cy,cx+t,cy+t],radius=r,fill=fill)
        d.text((cx+t/2,cy+t/2+t*0.03),ch,font=f,fill=ink,anchor="mm")
    return lay
dens = {"mdpi":1,"hdpi":1.5,"xhdpi":2,"xxhdpi":3,"xxxhdpi":4}
# legacy (48dp) con esquinas redondeadas
leg = bg_layer(S).convert("RGBA")
leg.alpha_composite(tiles(S,(S*0.2,S*0.2,S*0.8,S*0.8)))
mask = Image.new("L",(S,S),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,S-1,S-1],radius=S*0.22,fill=255)
legacy = Image.new("RGBA",(S,S),(0,0,0,0)); legacy.paste(leg,(0,0),mask)
# adaptativo: fondo y frente (108dp, contenido dentro de la zona segura 66dp)
fg = tiles(S,(S*0.30,S*0.30,S*0.70,S*0.70))
bgl = bg_layer(S)
for name,k in dens.items():
    p=f"{OUT}/res/mipmap-{name}"; os.makedirs(p,exist_ok=True)
    legacy.resize((int(48*k),)*2,Image.LANCZOS).save(f"{p}/ic_launcher.png")
    fg.resize((int(108*k),)*2,Image.LANCZOS).save(f"{p}/ic_launcher_fg.png")
    bgl.resize((int(108*k),)*2,Image.LANCZOS).save(f"{p}/ic_launcher_bg.png")
os.makedirs(f"{OUT}/res/mipmap-anydpi-v26",exist_ok=True)
xml='''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@mipmap/ic_launcher_bg"/>
    <foreground android:drawable="@mipmap/ic_launcher_fg"/>
</adaptive-icon>
'''
open(f"{OUT}/res/mipmap-anydpi-v26/ic_launcher.xml","w").write(xml)
print("íconos generados en", OUT + "/res")
