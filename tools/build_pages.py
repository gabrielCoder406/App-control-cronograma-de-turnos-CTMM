"""Genera las páginas a partir de la fuente única src/app.html.

Salidas:
  android/assets/index.html  app Android (documento completo, sin fuentes web)
  web/index.html             versión web independiente (fondo embebido; abrir en el navegador o GitHub Pages)
  build/artifact.html        versión para publicar como artefacto en claude.ai (sin <html>/<head>)
Uso: python3 tools/build_pages.py
"""
import base64, re, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "src/app.html").read_text(encoding="utf-8")
META = ('<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="theme-color" content="#060c18">\n')

def doc(body):
    return '<!doctype html>\n<html lang="es">\n<head>\n' + META + '</head>\n<body>\n' + body + '\n</body>\n</html>\n'

# App Android: sin los bloques <!--web--> (no hay internet en la app)
android = re.sub(r"<!--web-->.*?<!--/web-->\n?", "", src, flags=re.S)
(root / "android/assets/index.html").write_text(doc(android), encoding="utf-8")

# Web: fondo embebido como data URI para que sea un único archivo
web = src.replace("<!--web-->\n", "").replace("<!--/web-->\n", "")
for name in ("bg-wide.jpg", "bg.jpg"):
    b64 = base64.b64encode((root / "android/assets" / name).read_bytes()).decode()
    web = web.replace(f"url({name})", f"url(data:image/jpeg;base64,{b64})")
(root / "web").mkdir(exist_ok=True)
(root / "web/index.html").write_text(doc(web), encoding="utf-8")
(root / "build").mkdir(exist_ok=True)
(root / "build/artifact.html").write_text(web, encoding="utf-8")
print("páginas generadas: android/assets/index.html, web/index.html, build/artifact.html")
