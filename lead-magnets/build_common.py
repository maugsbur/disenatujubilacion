import re

CSS = """
  @page { size: A4; margin: 0; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Poppins', sans-serif; color: #1A2421; background: #F8F9FA;
         -webkit-print-color-adjust: exact; }
  .page { width: 210mm; height: 297mm; padding: 20mm 18mm; position: relative;
          page-break-after: always; overflow: hidden; }
  .page:last-child { page-break-after: auto; }

  .cover { background: #0E3A2F; color: #F8F9FA; padding: 0; width: 212mm; height: 300mm; }
  .cover-inner { padding: 38mm 20mm; height: 100%; position: relative; }
  .cover .eyebrow { font-size: 10.5pt; letter-spacing: 3.2px; text-transform: uppercase;
                    color: #E65F2B; font-weight: 500; margin-bottom: 24mm; }
  .cover h1 { font-family: 'Lora', serif; font-size: 40pt; line-height: 1.1;
              font-weight: 700; color: #F6E7B0; margin-bottom: 9mm; }
  .cover .sub { font-size: 13pt; line-height: 1.6; color: #F8F9FA; opacity: .88;
                max-width: 122mm; font-weight: 300; }
  .cover .footer { position: absolute; bottom: 24mm; left: 20mm; right: 20mm;
                   border-top: 1px solid rgba(246,231,176,.28); padding-top: 6mm;
                   font-size: 9.5pt; letter-spacing: 1.6px; text-transform: uppercase;
                   color: #F6E7B0; opacity: .75; }
  .draft { position: absolute; top: 14mm; right: 20mm; background: #E65F2B; color: #F8F9FA;
           font-size: 8pt; letter-spacing: 2px; text-transform: uppercase; font-weight: 600;
           padding: 2mm 4mm; }

  h2 { font-family: 'Lora', serif; font-size: 25pt; line-height: 1.2; color: #0E3A2F;
       font-weight: 700; margin-bottom: 7mm; }
  h3 { font-size: 12.5pt; font-weight: 600; color: #0E3A2F; margin-bottom: 3mm; }
  p { font-size: 11.5pt; line-height: 1.65; margin-bottom: 5mm; font-weight: 300; }
  p strong { font-weight: 600; }
  .hl { font-family: 'Lora', serif; font-size: 14pt; line-height: 1.5; font-weight: 700;
        color: #0E3A2F; margin: 7mm 0; padding-left: 6mm; border-left: 2.5px solid #E65F2B; }
  .close .hl { color: #F6E7B0; }
  a { color: inherit; text-decoration: none; }
  .lead { font-size: 13pt; line-height: 1.6; font-weight: 300; }
  .kicker { font-size: 9pt; letter-spacing: 2.6px; text-transform: uppercase;
            color: #E65F2B; font-weight: 500; margin-bottom: 4mm; }
  .rule { height: 2px; background: #E65F2B; width: 26mm; margin: 0 0 7mm 0; }

  .bignum { font-family: 'Lora', serif; font-size: 46pt; font-weight: 700;
            color: #F6E7B0; line-height: 1; margin-bottom: 2mm; }
  .numhead { font-size: 9pt; letter-spacing: 2.6px; text-transform: uppercase;
             color: #E65F2B; font-weight: 500; margin-bottom: 3mm; }

  .field { margin-bottom: 8.5mm; }
  .field .fl { font-size: 8.5pt; letter-spacing: 2px; text-transform: uppercase;
               color: #0E3A2F; opacity: .55; font-weight: 500; margin-bottom: 2.5mm; }
  .field .fv { font-size: 11pt; line-height: 1.6; font-weight: 300; }

  .action { background: #F6E7B0; padding: 7mm 7mm; margin: 8mm 0; }
  .action .al { font-size: 8.5pt; letter-spacing: 2px; text-transform: uppercase;
                color: #0E3A2F; font-weight: 600; margin-bottom: 2.5mm; }
  .action .av { font-size: 11.5pt; line-height: 1.55; font-weight: 500; color: #1A2421; }

  .done { border: 1.5px solid #0E3A2F; padding: 6mm; margin-top: 7mm; }
  .done .dl { font-size: 8.5pt; letter-spacing: 2px; text-transform: uppercase;
              color: #0E3A2F; opacity: .55; font-weight: 500; margin-bottom: 2mm; }
  .done .dv { font-size: 11pt; line-height: 1.55; font-weight: 300; }
  .chk { display: inline-block; width: 6mm; height: 6mm; border: 1.5px solid #0E3A2F;
         margin-right: 3mm; vertical-align: -1mm; }

  .note { background: #EFF1F0; border-left: 2.5px solid #0E3A2F; padding: 5mm 6mm; margin-top: 6mm; }
  .note p { font-size: 10.5pt; line-height: 1.55; margin-bottom: 0; font-weight: 300; }
  .warn { background: #F6E7B0; border-left: 2.5px solid #E65F2B; padding: 5mm 6mm; margin: 6mm 0; }
  .warn p { font-size: 10.5pt; line-height: 1.55; margin-bottom: 0; font-weight: 400; }

  .item { margin-bottom: 7mm; padding-left: 6mm; border-left: 2.5px solid #F6E7B0; }
  .item h3 { font-size: 11.5pt; margin-bottom: 2mm; }
  .item p { font-size: 11pt; line-height: 1.58; margin-bottom: 0; }
  .item .qq { font-family: 'Lora', serif; font-style: italic; font-size: 11pt;
              color: #0E3A2F; margin-top: 2.5mm; display: block; }

  .rules { counter-reset: r; }
  .rule-i { margin-bottom: 6.5mm; }
  .rule-i .rn { font-family: 'Lora', serif; font-size: 15pt; font-weight: 700;
                color: #E65F2B; display: inline-block; width: 9mm; }
  .rule-i .rt { font-size: 11.5pt; font-weight: 600; color: #0E3A2F; }
  .rule-i .rd { font-size: 11pt; line-height: 1.58; font-weight: 300; margin-top: 2mm;
                padding-left: 9mm; }

  .formula { background: #0E3A2F; color: #F6E7B0; padding: 7mm; margin: 6mm 0; text-align: center;
             font-family: 'Lora', serif; font-size: 13pt; line-height: 1.7; }
  .example { border: 1px solid #D8DCDA; padding: 5mm 6mm; margin-bottom: 4.5mm; }
  .example .el { font-size: 8.5pt; letter-spacing: 1.8px; text-transform: uppercase;
                 color: #E65F2B; font-weight: 500; margin-bottom: 2.5mm; }
  .example p { font-size: 10.5pt; line-height: 1.6; margin-bottom: 0; font-style: italic; }

  .blank { border-bottom: 1px solid #B9C1BD; height: 9mm; margin-bottom: 2mm; }
  .blank.tall { height: 16mm; }

  .close { background: #0E3A2F; color: #F8F9FA; width: 212mm; height: 300mm; }
  .close h2 { color: #F6E7B0; font-size: 29pt; }
  .close p { color: #F8F9FA; opacity: .9; }
  .close .principle { font-family: 'Lora', serif; font-size: 20pt; line-height: 1.35;
                      color: #F6E7B0; font-style: italic; margin: 9mm 0;
                      padding-left: 7mm; border-left: 2.5px solid #E65F2B; }
  .cta { background: #E65F2B; color: #F8F9FA; padding: 7mm; margin-top: 8mm; }
  .cta .ct { font-size: 9pt; letter-spacing: 2.4px; text-transform: uppercase;
             font-weight: 600; margin-bottom: 3mm; }
  .cta .cb { font-size: 12pt; font-weight: 400; line-height: 1.55; margin-bottom: 4mm; }
  .cta .cw { font-size: 10pt; font-weight: 400; margin-bottom: 2mm; opacity: .92; }
  .cta .cl { font-family: 'Lora', serif; font-size: 13pt; font-weight: 700; word-break: break-all; }
  .cta .cl a { color: #F8F9FA; text-decoration: underline; }
  a { color: #0E3A2F; }

  .pgnum { position: absolute; bottom: 12mm; right: 18mm; font-size: 8.5pt;
           color: #0E3A2F; opacity: .35; letter-spacing: 1px; }
  .close .pgnum { color: #F6E7B0; opacity: .4; }
"""

# El enlace de agendamiento. La sesión pasó de 40 a 45 minutos y la URL vieja
# quedó muerta — los PDF que circulaban antes de 2026-09-10 apuntaban a ella.
# Si vuelve a cambiar, se cambia ACÁ y se regeneran las cuatro guías.
CAL = "https://calendly.com/margarita-disenatujubilacion/45min"
CAL_TEXTO = "calendly.com/margarita-disenatujubilacion/45min"


def cal_url(utm=None):
    """El enlace con atribución. Sin UTM no hay forma de saber qué guía
    trae las llamadas agendadas, que es justo lo que se quiere medir."""
    return CAL + "?utm_source=" + utm if utm else CAL


def cta(lead, utm=None):
    return ('\n  <div class="cta">\n    <div class="ct">Si quieres seguir</div>\n'
            '    <div class="cb">' + lead + ' te invitamos a agendar una sesión de diagnóstico '
            '<strong>gratuita</strong> con nosotros. Dura 45 minutos y sirve para mirar tu caso en '
            'particular y ver si tiene sentido que trabajemos juntos.</div>\n'
            '    <div class="cw">Haz clic en el enlace para agendar:</div>\n'
            '    <div class="cl"><a href="' + cal_url(utm) + '">' + CAL_TEXTO + '</a></div>\n'
            '  </div>\n')

# Lora y Poppins se piden por nombre en el CSS. Sin esta línea, wkhtmltopdf
# las resuelve desde las fuentes INSTALADAS EN EL SISTEMA de quien renderiza:
# si no están, cae en silencio a Arial y Times New Roman y se pierde toda la
# identidad tipográfica, sin ningún error visible. El único síntoma es que el
# PDF pesa la mitad. Cargarlas desde Google Fonts hace el build reproducible
# en cualquier máquina. Requiere red al momento de renderizar.
FUENTES = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
           'family=Lora:ital,wght@0,400;0,700;1,400;1,700&'
           'family=Poppins:wght@300;400;500;600;700&display=swap">')


def wrap(body):
    return ('<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">'
            + FUENTES + '<style>'
            + CSS + '</style></head><body>' + body + '</body></html>')

def to_px(src):
    MM = 1024/210; PT = 1024/(210/25.4*72); PX = 1024/794
    head, _, rest = src.partition('<style>')
    css, _, tail = rest.partition('</style>')
    def conv(m):
        v, u = float(m.group(1)), m.group(2)
        return f"{round(v*{'mm':MM,'pt':PT,'px':PX}[u], 2):g}px"
    css = css.replace('size: A4;','size: __A4__;')
    css = re.sub(r'(-?\d*\.?\d+)(mm|pt|px)\b', conv, css).replace('size: __A4__;','size: A4;')
    tail = re.sub(r'style="([^"]*)"',
                  lambda m: 'style="'+re.sub(r'(-?\d*\.?\d+)(mm|pt|px)\b', conv, m.group(1))+'"', tail)
    return head + '<style>' + css + '</style>' + tail
