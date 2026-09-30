"""Renderiza placas de @disenatujubilacion como PNG.

Uso: python render.py entrada.json carpeta_salida

Los colores y tamaños salen de 🎨 Cómo diseñamos (Notion). Si cambian allá,
se cambian aquí: la página manda.
"""
import json
import pathlib
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

# fondo, texto, contexto, acento del CTA  (🎨 › Placas de Instagram)
# Fondos permitidos: verde (base) y claro (el quiebre). Carbón queda disponible
# para casos puntuales. El crema no se usa como fondo (Nicole, 08/09/2026).
PAL = {
    "verde":  ("#0E3A2F", "#F8F9FA", "#F6E7B0", "#E65F2B"),
    "carbon": ("#1A2421", "#F8F9FA", "#F6E7B0", "#E65F2B"),
    "claro":  ("#F8F9FA", "#1A2421", "#0E3A2F", "#E65F2B"),
}

CSS = """*{margin:0;padding:0;box-sizing:border-box}html,body{width:%(W)spx;height:%(H)spx}
body{background:%(bg)s;color:%(fg)s;font-family:Poppins,sans-serif;display:flex;
flex-direction:column;justify-content:center;padding:%(safe)spx 96px;overflow:hidden}
.eyebrow{font-size:46px;font-weight:700;letter-spacing:.10em;text-transform:uppercase;
color:%(ctx)s;margin-bottom:44px;line-height:1.25}
.principal{font-family:Lora,serif;font-size:78px;font-weight:600;line-height:1.22}
.matiz{font-size:50px;font-weight:300;line-height:1.5;margin-top:44px}
.dato{font-family:Lora,serif;font-size:210px;font-weight:600;line-height:1;color:%(ac)s}
.cita{font-family:Lora,serif;font-size:64px;font-style:italic;line-height:1.35}
.autor{font-size:44px;font-weight:500;margin-top:48px;line-height:1.45}
.autor span{display:block;font-weight:400;font-size:36px;margin-top:6px}
.palabra{font-size:112px;font-weight:700;letter-spacing:.04em;color:%(ac)s;margin:12px 0}
.pie{position:absolute;left:96px;bottom:%(pie)spx;font-size:38px;font-weight:500;
letter-spacing:.08em;text-transform:uppercase}
.foto{position:absolute;inset:0;object-fit:cover;width:100%%;height:100%%}
.velo{position:absolute;inset:0;background:linear-gradient(180deg,rgba(26,36,33,.15),
rgba(26,36,33,.55) 55%%,rgba(26,36,33,.88))}
.capa{position:relative;z-index:2}"""


def html(p, W, H):
    bg, fg, ctx, ac = PAL[p.get("fondo", "verde")]
    safe, pie = (260, 300) if H == 1920 else (110, 90)
    c, extra, t = "", "", p["tipo"]
    if p.get("contexto"):
        c += '<div class="eyebrow">%s</div>' % p["contexto"]
    if t == "texto":
        c += '<div class="principal">%s</div>' % p["principal"]
    elif t == "dato":
        c += ('<div class="dato">%s</div><div class="principal" style="margin-top:36px">%s</div>'
              % (p["numero"], p["principal"]))
    elif t == "cita":
        c += '<div class="cita">&laquo;%s&raquo;</div>' % p["principal"]
        if p.get("autor"):
            c += '<div class="autor">%s<span>%s</span></div>' % (p["autor"], p.get("rol", ""))
    elif t == "cta":
        c += '<div class="principal">%s</div><div class="palabra">%s</div>' % (p["principal"], p["palabra"])
    if p.get("matiz"):
        c += '<div class="matiz">%s</div>' % p["matiz"]
    if p.get("imagen"):
        extra = '<img class="foto" src="%s"><div class="velo"></div>' % p["imagen"]
        c = '<div class="capa">%s</div>' % c
    pie_html = '<div class="pie">%s</div>' % p["pie"] if p.get("pie") else ""
    css = CSS % dict(W=W, H=H, bg=bg, fg=fg, ctx=ctx, ac=ac, safe=safe, pie=pie)
    return ("<!doctype html><meta charset='utf-8'><style>%s</style>%s<div id='bloque'>%s</div>%s"
            % (css, extra, c, pie_html))


def ajustar(pg, H, safe):
    """Agranda la frase principal hasta llenar el 62% del área segura (🎨)."""
    obj = (H - 2 * safe) * 0.62

    def poner(px):
        pg.eval_on_selector(
            "#bloque",
            "(el,px)=>{const p=el.querySelector('.principal,.cita');if(p)p.style.fontSize=px+'px'}",
            px)

    lo, hi, best = 36, 132, 36  # nada bajo 36 px (🎨)
    while lo <= hi:
        mid = (lo + hi) // 2
        poner(mid)
        if pg.eval_on_selector("#bloque", "el=>el.getBoundingClientRect().height") <= obj:
            best, lo = mid, mid + 1
        else:
            hi = mid - 1
    poner(best)


def render(placas, salida, formato="historia"):
    W, H = (1080, 1920) if formato == "historia" else (1080, 1350)
    safe = 260 if H == 1920 else 110
    out = pathlib.Path(salida)
    out.mkdir(parents=True, exist_ok=True)
    hechos = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        for i, p in enumerate(placas, 1):
            pg.set_content(html(p, W, H))
            pg.wait_for_timeout(120)
            if p["tipo"] in ("texto", "cita", "cta"):
                ajustar(pg, H, safe)
                pg.wait_for_timeout(60)
            f = out / ("placa-%d.png" % i)
            pg.screenshot(path=str(f))
            # Colores planos: 64 colores bajan el peso a un tercio sin que se note.
            Image.open(f).convert("RGB").quantize(colors=64).save(f, optimize=True)
            hechos.append(str(f))
        b.close()
    return hechos


if __name__ == "__main__":
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    for f in render(d["placas"], sys.argv[2], d.get("formato", "historia")):
        print(f)
