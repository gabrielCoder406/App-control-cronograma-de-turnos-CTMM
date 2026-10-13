"""Genera el fondo difuminado de la central a partir de una foto.
Uso: python3 tools/make_bg.py ruta/a/foto.jpg
Salida: android/assets/bg.jpg (vertical) y android/assets/bg-wide.jpg (horizontal)."""
import sys
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
src = Image.open(sys.argv[1]).convert("RGB")
src = ImageEnhance.Color(src).enhance(1.12)
W, H = 720, 1560
PH = 820                                   # alto de la foto en el lienzo
pw = round(src.width * PH / src.height)    # ~1493
photo = src.resize((pw, PH), Image.LANCZOS)
cx = 0.40                                  # encuadre: chimeneas, edificio y cartel
x0 = max(0, min(pw - W, round(pw * cx - W / 2)))
photo = photo.crop((x0, 0, x0 + W, PH))
# relleno inferior: la misma foto muy difuminada, estirada y oscurecida
fill = src.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
fill = ImageEnhance.Brightness(fill).enhance(0.42)
canvas = fill.copy()
mask = Image.new("L", (W, PH), 255)
d = ImageDraw.Draw(mask)
fade = 260
for y in range(PH - fade, PH):
    d.line([(0, y), (W, y)], fill=int(255 * (PH - y) / fade))
canvas.paste(photo, (0, 0), mask)
canvas = canvas.filter(ImageFilter.GaussianBlur(6))
canvas.save("android/assets/bg.jpg", quality=80, optimize=True, progressive=True)
# horizontal (celular girado / tablet)
wide = src.filter(ImageFilter.GaussianBlur(5))
wide.save("android/assets/bg-wide.jpg", quality=80, optimize=True, progressive=True)
canvas.resize((360, 780)).save("bg_preview.png")
