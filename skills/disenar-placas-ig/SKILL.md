---
name: disenar-placas-ig
description: "Genera las placas de @disenatujubilacion como PNG con la identidad de marca — 1080×1920 historias, 1080×1350 carrusel — a partir de un guion ya aprobado en Notion. Úsala cuando pidan las placas, las imágenes o el diseño de una pieza."
---

# Diseñar las placas

Convierte un guion **ya escrito** en imágenes listas para subir. No escribe el guion (eso es `escribir-guion-ig`) ni decide qué dice.

Cada bloque **Placa N** del guion se convierte en una placa, y la línea de fondo que lo acompaña —"— foto de Carlos a sangre completa", "— placa sobria con el dato grande"— te dice qué tipo usar.

**Lee 🎨 Cómo diseñamos antes de renderizar** — https://app.notion.com/p/3d523cb6e7af81f9a703eb234cce4a22. Ahí viven las reglas visuales y crecen con cada revisión; si algo de aquí las contradice, gana esa página.

## Cómo llegan las placas a Notion

Claude **no puede adjuntar archivos a Notion desde este entorno**: la política de egreso de la organización bloquea la subida a `api.notion.com`. No intentes rodearla con `curl` ni con un servicio intermedio — es una denegación de política, no un fallo. Tres caminos, de mejor a peor:

1. **Carpeta de Google Drive conectada desde el computador.** Escribe los PNG ahí con `device_commit_files` y pon el enlace de Drive en la fila. Ningún archivo pasa por la conversación. Comprueba con `get_device_info` que haya carpetas conectadas.
2. **El conector de Google Drive** (`create_file` con `base64Content`). Funciona, pero la imagen viaja codificada por la conversación y pesa unas cinco veces el archivo. Úsalo solo para una o dos placas sueltas.
3. **Entrega en la conversación** con `SendUserFile`, diciendo en qué fila hay que arrastrarlas. Es lo que funciona sin configurar nada.

**No cambies el estado a `Para subir`**: eso lo hace quien adjunta, después de la revisión visual. Y por lo mismo esta skill **no corre sola en la revisión de las 4:00**.

## La revisión visual

Las placas se revisan antes de subirse, igual que las ideas. Nicole o Margarita responden si sirven, si hay que cambiar algo, o si no van.

Cuando el comentario sea sobre cómo se ven, regístralo como **Nota de diseño** en 🗳️ Decisiones y notas. Cuando el mismo tipo de corrección aparezca **dos veces**, destílalo como regla en 🎨 Cómo diseñamos citando de dónde salió — el mismo mecanismo que ✍️ Cómo escribimos, pero para lo visual. Una corrección puntual no es una regla, y las Reglas de base no se tocan sin que te lo pidan.

## El renderizador

Chromium y las fuentes Lora y Poppins ya están en el entorno. Escribe este archivo y córrelo con un JSON de entrada:

```python
import json, sys, pathlib
from PIL import Image
from playwright.sync_api import sync_playwright
# fondo, texto, contexto (>=4.5:1), acento del CTA (>=3:1 en tamaño grande)
PAL = {"verde":  ("#0E3A2F","#F8F9FA","#F6E7B0","#E65F2B"),
       "carbon": ("#1A2421","#F8F9FA","#F6E7B0","#E65F2B"),
       "crema":  ("#F6E7B0","#0E3A2F","#0E3A2F","#0E3A2F"),
       "claro":  ("#F8F9FA","#1A2421","#0E3A2F","#E65F2B")}
CSS = """*{margin:0;padding:0;box-sizing:border-box}html,body{width:%(W)spx;height:%(H)spx}
body{background:%(bg)s;color:%(fg)s;font-family:Poppins,sans-serif;display:flex;
flex-direction:column;justify-content:center;padding:%(safe)spx 96px;overflow:hidden}
.eyebrow{font-size:46px;font-weight:700;letter-spacing:.10em;text-transform:uppercase;
color:%(ctx)s;margin-bottom:44px;line-height:1.25}
.principal{font-family:Lora,serif;font-size:78px;font-weight:600;line-height:1.22}
.matiz{font-size:50px;font-weight:300;line-height:1.5;margin-top:44px;opacity:.85}
.dato{font-family:Lora,serif;font-size:210px;font-weight:600;line-height:1;color:%(ac)s}
.cita{font-family:Lora,serif;font-size:64px;font-style:italic;line-height:1.35}
.autor{font-size:44px;font-weight:500;margin-top:48px;line-height:1.45}
.autor span{display:block;font-weight:400;opacity:.75;font-size:36px;margin-top:6px}
.palabra{font-size:112px;font-weight:700;letter-spacing:.04em;color:%(ac)s;margin:12px 0}
.pie{position:absolute;left:96px;bottom:%(pie)spx;font-size:38px;font-weight:500;
letter-spacing:.08em;text-transform:uppercase;opacity:.75}
.foto{position:absolute;inset:0;object-fit:cover;width:100%%;height:100%%}
.velo{position:absolute;inset:0;background:linear-gradient(180deg,rgba(26,36,33,.15),
rgba(26,36,33,.55) 55%%,rgba(26,36,33,.88))}
.capa{position:relative;z-index:2}"""
def html(p, W, H):
    bg, fg, ctx, ac = PAL[p.get("fondo","verde")]
    safe, pie = (260, 300) if H == 1920 else (110, 90)
    c, extra, t = "", "", p["tipo"]
    if p.get("contexto"): c += '<div class="eyebrow">%s</div>' % p["contexto"]
    if t == "texto":  c += '<div class="principal">%s</div>' % p["principal"]
    elif t == "dato": c += '<div class="dato">%s</div><div class="principal" style="margin-top:36px">%s</div>' % (p["numero"], p["principal"])
    elif t == "cita":
        c += '<div class="cita">&laquo;%s&raquo;</div>' % p["principal"]
        if p.get("autor"): c += '<div class="autor">%s<span>%s</span></div>' % (p["autor"], p.get("rol",""))
    elif t == "cta":  c += '<div class="principal">%s</div><div class="palabra">%s</div>' % (p["principal"], p["palabra"])
    if p.get("matiz"): c += '<div class="matiz">%s</div>' % p["matiz"]
    if p.get("imagen"):
        extra = '<img class="foto" src="%s"><div class="velo"></div>' % p["imagen"]
        c = '<div class="capa">%s</div>' % c
    pie_html = '<div class="pie">%s</div>' % p["pie"] if p.get("pie") else ""
    css = CSS % dict(W=W, H=H, bg=bg, fg=fg, ctx=ctx, ac=ac, safe=safe, pie=pie)
    return "<!doctype html><meta charset='utf-8'><style>%s</style>%s<div id='bloque'>%s</div>%s" % (css, extra, c, pie_html)
def ajustar(pg, H, safe):
    obj = (H - 2*safe) * 0.62
    poner = lambda px: pg.eval_on_selector("#bloque",
        "(el,px)=>{const p=el.querySelector('.principal,.cita');if(p)p.style.fontSize=px+'px'}", px)
    lo, hi, best = 34, 132, 34
    while lo <= hi:
        mid = (lo+hi)//2; poner(mid)
        if pg.eval_on_selector("#bloque", "el=>el.getBoundingClientRect().height") <= obj: best, lo = mid, mid+1
        else: hi = mid-1
    poner(best)
def render(placas, salida, formato="historia"):
    W, H = (1080,1920) if formato == "historia" else (1080,1350)
    safe = 260 if H == 1920 else 110
    out = pathlib.Path(salida); out.mkdir(parents=True, exist_ok=True); hechos = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width":W,"height":H})
        for i, p in enumerate(placas, 1):
            pg.set_content(html(p, W, H)); pg.wait_for_timeout(120)
            if p["tipo"] in ("texto","cita","cta"): ajustar(pg, H, safe); pg.wait_for_timeout(60)
            f = out / ("placa-%d.png" % i); pg.screenshot(path=str(f))
            Image.open(f).convert("RGB").quantize(colors=64).save(f, optimize=True)
            hechos.append(str(f))
        b.close()
    return hechos
if __name__ == "__main__":
    d = json.load(open(sys.argv[1]))
    for f in render(d["placas"], sys.argv[2], d.get("formato","historia")): print(f)
```

La cuantización a 64 colores al final baja el peso a un tercio sin que se note — son colores planos. Importa cuando las placas viajan a Drive.

## La entrada

```json
{"formato": "historia",
 "placas": [
  {"tipo":"texto","fondo":"verde","contexto":"Una frase que escuchamos mucho",
   "principal":"«Lo importante es solo lo financiero.»","pie":"Diseña tu Jubilación"},
  {"tipo":"dato","fondo":"crema","numero":"12 de 13",
   "principal":"personas del piloto reportaron mejoras.","pie":"Piloto 2026"},
  {"tipo":"cita","fondo":"verde","principal":"La vejez te pilla desprevenido.",
   "autor":"Carlos","rol":"Químico laboratorista en minería · Jubilado"},
  {"tipo":"cta","fondo":"verde","contexto":"Si quieres empezar por algún lado",
   "principal":"Comenta","palabra":"PLAN","matiz":"y te mando la guía de las cinco áreas."}
]}
```

`formato` es `historia` (1080×1920) o `carrusel` (1080×1350). `imagen` acepta una ruta local o un data URI y pone la foto de fondo con un velo para que el texto se lea.

## Cómo componer la secuencia

- **Un fondo base para toda la secuencia**, normalmente verde. **Una o dos placas rompen** — típicamente la del dato — y ese quiebre es el énfasis. Si rompen todas, no destaca ninguna.
- **El CTA vuelve al fondo base.** Y nunca sobre crema: el ámbar no contrasta ahí, y la palabra es justo lo que tiene que verse.
- **El tipo se ajusta solo** hasta llenar el 62% del área segura. No fijes tamaños a mano: es lo que hace que una placa de seis palabras y otra de treinta se vean de la misma familia.
- **Zona segura de 260px arriba y abajo** en historias, donde van la barra de perfil y la caja de respuesta de Instagram.
- **Una idea por placa.** Contexto, frase, matiz. Si hace falta una cuarta línea, sobra algo o son dos placas.
- **Lora para lo que se lee, Poppins para lo que se etiqueta.**

## Al terminar

Entrega las placas numeradas en orden, di a qué fila pertenecen y qué falta. Si una placa pedía una foto que no existe, dilo en vez de renderizarla vacía: una placa de texto donde debía ir una cara es un problema de producción, no un detalle.

## Contexto

- **🔁 Flujo de contenido con Claude** — https://app.notion.com/p/3d123cb6e7af81da9b53ee254469225e
- **🎨 Cómo diseñamos** — https://app.notion.com/p/3d523cb6e7af81f9a703eb234cce4a22
- **✍️ Cómo escribimos** — https://app.notion.com/p/3d423cb6e7af818f85a6d216c1b6a459

Carga las herramientas con `ToolSearch`: `select:mcp__Notion__notion-fetch,mcp__Notion__notion-query-data-sources,mcp__Notion__notion-update-page,mcp__Notion__notion-create-pages`

Calendarios: historias `collection://b2323cb6-e7af-829f-9594-87552d04c5db` · contenido `collection://df323cb6-e7af-8277-ba21-87bd09a11fd7` · decisiones `collection://57e0fe61-5ec6-480c-8cb6-cd8de0899542`. El modo SQL está topado: usa `rows` o `view`.