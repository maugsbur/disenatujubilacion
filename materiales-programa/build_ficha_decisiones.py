# -*- coding: utf-8 -*-
# Ficha de Decisiones Intencionales, versión imprimible (2 páginas, A4).
#
# La fuente es la página de Notion "Ficha de Decisiones Intencionales"
# (Programa vigente › Hábitos e instrumentos). La ficha se llena en la
# bitácora del participante; este PDF es el respaldo para quien prefiera
# una hoja impresa. Si cambian los campos en Notion, se cambian acá.
#
# Página 1: tres fichas en blanco. Página 2: cómo se llena, un ejemplo
# ficticio y la tabla de las dos revisiones.
#
#   python build_ficha_decisiones.py
#   wkhtmltopdf --enable-local-file-access --page-size A4 -T 0 -B 0 -L 0 -R 0 \
#       ficha-decisiones_px.html ficha-decisiones.pdf
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "lead-magnets"))
from build_common import CSS, FUENTES, to_px  # noqa: E402

EXTRA = """
  .top { background: #0E3A2F; color: #F8F9FA; padding: 8mm 16mm 6mm; }
  .top .eyebrow { font-size: 8pt; letter-spacing: 3px; text-transform: uppercase;
                  color: #E65F2B; font-weight: 500; margin-bottom: 2.5mm; }
  .top h1 { font-family: 'Lora', serif; font-size: 19pt; line-height: 1.15;
            font-weight: 700; color: #F6E7B0; margin-bottom: 3mm; }
  .top .sub { font-size: 10pt; line-height: 1.5; color: #DCE2E2; font-weight: 300; }
  .body { padding: 5mm 16mm 0; }
  .sheet { padding: 0; }

  .card { border: 1.2px solid #0E3A2F; padding: 3mm 5mm 1.5mm; margin-bottom: 3.5mm; }
  .card .ch { font-size: 8pt; letter-spacing: 2px; text-transform: uppercase;
              color: #E65F2B; font-weight: 600; margin-bottom: 1.5mm; }
  /* wkhtmltopdf usa un WebKit viejo sin flexbox: las filas van como tabla. */
  .row { display: table; width: 100%; table-layout: fixed; }
  .row .f { display: table-cell; vertical-align: top; }
  .row .f + .f { padding-left: 6mm; }
  .row .f.narrow { width: 30mm; }
  .f { margin-bottom: 1mm; }
  .fl { font-size: 7.5pt; letter-spacing: 1.6px; text-transform: uppercase;
        color: #3D6058; font-weight: 500; }
  .ln { border-bottom: 1px solid #B9C1BD; height: 6mm; }
  .opts { font-size: 9pt; color: #1A2421; font-weight: 300; padding-top: 1.5mm; height: 6mm;
          border-bottom: 1px solid #B9C1BD; }
  .opts .chk { width: 3.6mm; height: 3.6mm; margin: 0 1.5mm 0 3mm; vertical-align: -0.6mm; border-width: 1.2px; }
  .opts .chk:first-child { margin-left: 0; }

  .ex .val { font-family: 'Lora', serif; font-style: italic; font-size: 9.5pt; color: #0E3A2F;
             line-height: 1.4; border-bottom: 1px solid #D8DCDA; padding: 1mm 0 1.5mm; }
  h2.s { font-size: 15pt; margin: 0 0 3mm; }
  .howto p { font-size: 10pt; line-height: 1.5; margin-bottom: 2.5mm; }
  .tip { font-size: 9.5pt; line-height: 1.45; font-weight: 300; margin-bottom: 1.8mm;
         padding-left: 5mm; border-left: 2px solid #F6E7B0; }
  .tip strong { font-weight: 600; color: #0E3A2F; }
  table.rev { width: 100%; border-collapse: collapse; margin-top: 2mm; }
  table.rev th { font-size: 7.5pt; letter-spacing: 1.6px; text-transform: uppercase; color: #3D6058;
                 font-weight: 500; text-align: left; padding: 1.5mm 2mm; border-bottom: 1.2px solid #0E3A2F; }
  table.rev td { font-size: 9.5pt; font-weight: 300; padding: 2.2mm 2mm; border-bottom: 1px solid #D8DCDA;
                 vertical-align: top; }
  .foot { position: absolute; bottom: 9mm; left: 16mm; right: 16mm; font-size: 8pt;
          color: #77908A; letter-spacing: 1px; border-top: 1px solid #D8DCDA; padding-top: 2.5mm; }
"""


def campo(label, alto=1, clase=""):
    lineas = '<div class="ln"></div>' * alto
    return f'<div class="f {clase}"><div class="fl">{label}</div>{lineas}</div>'


def cuando():
    return ('<div class="f"><div class="fl">Cuándo</div><div class="opts">'
            '<span class="chk"></span>Ahora<span class="chk"></span>Después: cuando / fecha'
            ' ______________<span class="chk"></span>No</div></div>')


def ficha_vacia(n):
    return f"""
  <div class="card">
    <div class="ch">Decisión {n}</div>
    <div class="row">{campo("Fecha", clase="narrow")}{campo("Momento: rutas · hábitos · ponerse al día · batallas · escenarios")}</div>
    <div class="row">{campo("Qué elegí", 2)}{campo("Qué dejé fuera", 2)}</div>
    {campo("Por qué")}
    {cuando()}
    <div class="row">{campo("Primer paso (qué y qué día)", 2)}{campo("Cómo se ve hecho", 2)}</div>
  </div>"""


def valor(label, texto, clase=""):
    return f'<div class="f {clase}"><div class="fl">{label}</div><div class="val">{texto}</div></div>'


PAGINA_1 = f"""
<div class="page sheet">
  <div class="top">
    <div class="eyebrow">Diseña tu Jubilación · Programa de 3 meses</div>
    <h1>Tu Ficha de Decisiones Intencionales</h1>
    <div class="sub">Lo que eliges y también lo que dejas fuera, con tu razón. Escríbela tú, el mismo día, en tus palabras.</div>
  </div>
  <div class="body">
    {ficha_vacia(1)}
    {ficha_vacia(2)}
    {ficha_vacia(3)}
  </div>
</div>"""

PAGINA_2 = f"""
<div class="page sheet">
  <div class="body" style="padding-top: 14mm;">
    <div class="kicker">Cómo se llena</div>
    <h2 class="s">Una ficha por decisión</h2>
    <div class="howto">
      <p>Durante estos 3 meses vas a elegir varias veces: por dónde empezar, qué hábitos instalar,
      qué batallas dar y cuáles no. Decidir no hacer algo, o hacerlo más adelante, es tan válido
      como hacerlo ahora. Lo único que buscamos evitar es decidir por inercia.</p>
    </div>
    <div class="tip"><strong>Qué elegí:</strong> una frase concreta. "Instalo sueño y movimiento", no "me voy a cuidar más".</div>
    <div class="tip"><strong>Qué dejé fuera:</strong> casi siempre hay algo. Pregúntate qué no vas a hacer por hacer esto.</div>
    <div class="tip"><strong>Después:</strong> necesita un criterio, "cuando pase tal cosa" o una fecha. Sin eso, es inercia con otro nombre.</div>
    <div class="tip"><strong>Primer paso:</strong> lo que haces esta semana, con día. Si no lo puedes nombrar, la acción todavía es muy grande.</div>

    <div class="card ex" style="margin-top: 5mm;">
      <div class="ch">Ejemplo (ficticio)</div>
      <div class="row">{valor("Fecha", "14/10", "narrow")}{valor("Momento", "Rutas")}</div>
      <div class="row">{valor("Qué elegí", "Empiezo por Vínculos")}{valor("Qué dejé fuera", "Cuerpo queda segunda, aunque mi panel la marcaba primero")}</div>
      {valor("Por qué", "Desde que dejé la empresa no veo a nadie entre semana, y eso me pesa más que el colesterol")}
      {valor("Cuándo", "Ahora")}
      <div class="row">{valor("Primer paso", "El jueves le escribo a Jorge para almorzar la próxima semana")}{valor("Cómo se ve hecho", "Un encuentro presencial a la semana con alguien fuera de mi familia")}</div>
    </div>

    <div class="kicker" style="margin-top: 6mm;">Dos veces vas a volver a mirarla</div>
    <p style="font-size: 10pt; line-height: 1.5; margin-bottom: 1mm;">La pregunta es siempre la misma: <strong>¿sigue siendo tu decisión?</strong></p>
    <table class="rev">
      <tr><th>Revisión</th><th>Qué se revisa</th><th>Respuesta</th><th>Qué sigue</th></tr>
      <tr><td>Sesión 3</td><td>Rutas y hábitos</td><td>Sí · La cambio · No sé · Ya no aplica</td><td>Una línea</td></tr>
      <tr><td>Cierre</td><td>Todas</td><td>Sí · La cambio · No sé · Ya no aplica</td><td>Una línea y una fecha</td></tr>
    </table>
  </div>
  <div class="foot">Con intención y no por inercia. · Diseña tu Jubilación</div>
</div>"""


def main():
    html = ('<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">' + FUENTES
            + '<style>' + CSS + EXTRA + '</style></head><body>'
            + PAGINA_1 + PAGINA_2 + '</body></html>')
    with open(os.path.join(AQUI, "ficha-decisiones.html"), "w", encoding="utf-8") as f:
        f.write(html)
    with open(os.path.join(AQUI, "ficha-decisiones_px.html"), "w", encoding="utf-8") as f:
        f.write(to_px(html))


if __name__ == "__main__":
    main()
