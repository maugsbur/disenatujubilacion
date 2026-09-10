# -*- coding: utf-8 -*-
from build_common import wrap, to_px, cta

EXTRA = """
<style>
  .scale { background: #F6E7B0; padding: 5.5mm 6mm; margin-bottom: 8.5mm; }
  .scale-q { font-size: 10.5pt; font-weight: 600; color: #0E3A2F; margin-bottom: 3mm; }
  .scale table { width: 100%; border-collapse: collapse; }
  .scale td { font-size: 9.5pt; color: #1A2421; text-align: center; padding: 0 1mm; width: 20%; }
  .scale td .num { font-family: 'Lora', serif; font-size: 13pt; font-weight: 700;
                   color: #0E3A2F; display: block; margin-bottom: .5mm; }
  .q { border-bottom: 1px solid #E3E5E4; padding: 6.6mm 0; }
  .q:last-of-type { border-bottom: none; }
  .q table { width: 100%; border-collapse: collapse; }
  .q .txt { font-size: 12pt; line-height: 1.55; font-weight: 300; color: #1A2421;
            padding-right: 7mm; vertical-align: middle; }
  .q .boxes { width: 46mm; text-align: right; vertical-align: middle; white-space: nowrap; }
  .bx { display: inline-block; width: 7.5mm; height: 7.5mm; border: 1.2px solid #B9C1BD;
        margin-left: 1.4mm; text-align: center; font-size: 8pt; color: #B9C1BD;
        line-height: 7.3mm; font-weight: 500; }
  .total-row { margin-top: 7mm; background: #0E3A2F; color: #F6E7B0; padding: 5mm 6mm; }
  .total-row table { width: 100%; border-collapse: collapse; }
  .total-row .lbl { font-size: 10pt; letter-spacing: 2px; text-transform: uppercase; font-weight: 500; }
  .total-row .val { text-align: right; }
  .total-row .val .bl { display: inline-block; width: 18mm; border-bottom: 1.5px solid #F6E7B0; height: 6mm; }
  .total-row .val .of { font-family: 'Lora', serif; font-size: 13pt; margin-left: 3mm; color: #F8F9FA; opacity: .7; }

  .scoregrid { width: 100%; border-collapse: collapse; margin-bottom: 5mm; }
  .scoregrid td { padding: 2.4mm 0; vertical-align: middle; }
  .scoregrid .pname { font-family: 'Lora', serif; font-size: 11.5pt; font-weight: 700; color: #0E3A2F; width: 30mm; }
  .scoregrid .cells { white-space: nowrap; }
  .cell { display: inline-block; width: 5.2mm; height: 6.6mm; border: 1px solid #CFD5D2;
          margin-right: .6mm; text-align: center; font-size: 7.5pt; line-height: 6.4mm;
          color: #1A2421; font-weight: 500; }
  .cell.z1 { background: #FBDACB; border-color: #E9A183; }
  .cell.z2 { background: #F9EFC9; border-color: #DFC97F; }
  .cell.z3 { background: #CBDCD5; border-color: #7FA598; }
  .scoregrid .sc { width: 16mm; text-align: right; }
  .scoregrid .sc .bl { display: inline-block; width: 13mm; border-bottom: 1.5px solid #0E3A2F; height: 6mm; }
  .zonekey { width: 100%; border-collapse: collapse; margin-bottom: 6mm; }
  .zonekey td { font-size: 9pt; letter-spacing: 1.2px; text-transform: uppercase;
                color: #0E3A2F; opacity: .6; font-weight: 500; }

  .band { padding: 5mm 6mm; margin-bottom: 4mm; }
  .band.at { background: #E65F2B; color: #1A2421; }
  .band.mid { background: #F6E7B0; color: #1A2421; }
  .band.ok { background: #0E3A2F; color: #F6E7B0; }
  .band .bn { font-family: 'Lora', serif; font-size: 15pt; font-weight: 700; display: inline-block; width: 26mm; }
  .band .bt { font-size: 10.5pt; font-weight: 500; }
  .band .bd { font-size: 10.5pt; font-weight: 400; line-height: 1.55; margin-top: 2mm; opacity: .95; }

  .drag { margin-bottom: 6mm; padding-left: 6mm; border-left: 2.5px solid #F6E7B0; }
  .drag h3 { font-size: 11.5pt; margin-bottom: 2.5mm; }
  .drag ul { list-style: none; margin: 0; padding: 0; }
  .drag li { font-size: 10.5pt; line-height: 1.5; margin-bottom: 2mm; padding-left: 6mm; text-indent: -6mm; }
  .arrow { color: #E65F2B; font-weight: 600; }

  .arch { margin-bottom: 6mm; }
  .arch .an { font-family: 'Lora', serif; font-size: 13pt; font-weight: 700; color: #0E3A2F; margin-bottom: 1mm; }
  .arch .ap { font-size: 8.5pt; letter-spacing: 1.4px; text-transform: uppercase; color: #E65F2B;
              font-weight: 500; margin-bottom: 2mm; }
  .arch p { font-size: 10.5pt; line-height: 1.55; margin-bottom: 0; }
</style>
"""

SCALE = """
  <div class="scale">
    <div class="scale-q">¿Qué tan cierto es esto para ti hoy?</div>
    <table><tr>
      <td><span class="num">1</span>Nada cierto</td>
      <td><span class="num">2</span>Poco cierto</td>
      <td><span class="num">3</span>A medias</td>
      <td><span class="num">4</span>Bastante cierto</td>
      <td><span class="num">5</span>Totalmente cierto</td>
    </tr></table>
  </div>"""

BX = "".join(f'<span class="bx">{i}</span>' for i in range(1,6))

def pillar(n, idx, title, sub, items, total):
    qs = "".join(f'<div class="q"><table><tr><td class="txt">{t}</td>'
                 f'<td class="boxes">{BX}</td></tr></table></div>' for t in items)
    return f"""
<div class="page">
  <div class="kicker">Pilar {idx} de 5</div>
  <h2>{title}</h2>
  <div class="rule"></div>
  <p style="font-size:11pt; opacity:.75; margin-bottom:6mm;">{sub}</p>
  {SCALE}
  {qs}
  <div class="total-row"><table><tr><td class="lbl">Total {total}</td>
    <td class="val"><span class="bl"></span><span class="of">/ 25</span></td></tr></table></div>
  <div class="pgnum">{n}</div>
</div>"""

CELLS = "".join(f'<span class="cell z{1 if v<=11 else (2 if v<=18 else 3)}">{v}</span>' for v in range(5,26))
def row(name):
    return (f'<tr><td class="pname">{name}</td><td class="cells">{CELLS}</td>'
            f'<td class="sc"><span class="bl"></span></td></tr>')

def drag(title, bullets):
    lis = "".join(f'<li><span class="arrow">→</span> {b}</li>' for b in bullets)
    return f'<div class="drag"><h3>{title}</h3><ul>{lis}</ul></div>'

body = """
<div class="page cover">
  <div class="cover-inner">
    <div class="eyebrow">Diseña tu Jubilación</div>
    <h1>Tu jubilación<br>se juega en cinco<br>pilares. ¿Cuál te<br>está frenando?</h1>
    <div class="sub">Un autodiagnóstico de 25 preguntas para descubrir dónde está tu cuello de botella antes de que llegue el momento. Toma doce minutos y se responde con lápiz.</div>
    <div class="footer">Autodiagnóstico · 5 pilares · Efecto dominó</div>
  </div>
</div>

<div class="page">
  <div class="kicker">Antes de empezar</div>
  <h2>Cómo usar esto</h2>
  <div class="rule"></div>
  <p class="lead">La mayoría de la gente que se acerca al retiro no tiene un problema en los cinco pilares. Tiene un problema en uno o dos, y esos le están arrastrando a los demás.</p>
  <p>Este cuadernillo sirve para encontrar cuáles son. No para arreglarlos (eso toma bastante más de doce minutos), sino para saber dónde estás parado antes de decidir qué hacer.</p>
  <p>No venimos a decirte cómo se vive esta etapa. Es una decisión personal y es tuya. Venimos con método, con evidencia y con estructura. <strong>Quien decide eres tú</strong>, empezando por este cuadernillo, que respondes por tu cuenta y que nadie más tiene que ver.</p>
  <h3>Cuatro instrucciones</h3>
  <p><strong>1. Responde rápido.</strong> La primera reacción es más honesta que la reflexionada. Si llevas más de quince segundos en una pregunta, marca lo que sentiste primero y sigue.</p>
  <p><strong>2. Responde por lo que haces, no por lo que sabes.</strong> Varias preguntas describen cosas que probablemente ya sabes que son buena idea. La pregunta no es si lo sabes: es si ocurre.</p>
  <p><strong>3. No optimices el resultado.</strong> Un puntaje alto que no es real no te sirve para nada.</p>
  <p><strong>4. Suma cada pilar al final de su página.</strong> Al final vas a traspasar los cinco totales a una sola hoja.</p>
  <div class="note">
    <p><strong>Qué es y qué no es esto.</strong> Este es un ejercicio de orientación personal, no un instrumento clínico ni un diagnóstico de ningún tipo. No detecta enfermedades, no evalúa tu salud mental y no reemplaza a ningún profesional. Si algo de lo que respondas te preocupa, sea de salud, de ánimo o de dinero, la conversación correcta es con tu médico, con un profesional de salud mental o con un asesor, no con un cuadernillo.</p>
  </div>
  <div class="pgnum">2</div>
</div>
"""

body += pillar(3, 1, "Vida con Propósito",
  "Dirección, identidad y estructura del tiempo. Es el pilar que organiza a los otros cuatro.", [
  "Tengo claro qué quiero hacer con mi tiempo cuando deje de trabajar, o ahora que ya dejé de hacerlo.",
  "Mis semanas tienen una estructura que yo diseñé, no una que simplemente ocurrió.",
  "Si mañana dejara de trabajar, no sentiría que pierdo una parte de mi valor ni de mi identidad.",
  "Fuera del trabajo, realizo actividades que me producen una gran satisfacción personal.",
  "Si sigo con mi vida tal como va, sin realizar ningún cambio importante, lograría hacer todo lo que me gustaría hacer en ella."],
  "Propósito")

body += pillar(4, 2, "Salud Física",
  "El objetivo es morir joven&hellip; a los 95.", [
  "Hago entrenamiento de fuerza al menos dos veces por semana.",
  "Camino, pedaleo, nado o hago otra actividad física a ritmo sostenido varias horas a la semana.",
  "Sé cuáles son mis necesidades nutricionales y me alimento y suplemento acorde a ellas, en tipos y en cantidades.",
  "Tengo bajo control el alcohol, el azúcar, el tabaco y otras cosas que sé que me hacen daño.",
  "Me he hecho todos mis exámenes preventivos en los últimos doce meses."],
  "Físico")

body += pillar(5, 3, "Salud Mental<br>y Cognitiva",
  "Sueño, aprendizaje y manejo de emociones. El pilar que decide si vas a seguir siendo tú.", [
  "Duermo entre siete y ocho horas la mayoría de las noches y despierto descansado.",
  "Estoy aprendiendo algo nuevo y desafiante, fuera de lo laboral.",
  "Cuando algo me altera, se me pasa en minutos y no me dura el día entero.",
  "Tengo espacios en la semana donde mi cabeza descansa de verdad, sin pantallas, sin entretenimiento y sin preocupaciones.",
  "Cuando hay tensión en mi casa, logramos conversarla y llegar a acuerdos que dejan a todos conformes."],
  "Mental")

body += pillar(6, 4, "Salud Social",
  "El pilar que más gente subestima y el que más rápido se desarma al dejar de trabajar.", [
  "Tengo al menos tres personas a las que podría llamar de madrugada por un problema, aunque no fuera de vida o muerte.",
  "Al menos una vez a la semana me reúno con personas importantes para mí, que no viven conmigo, a pasar tiempo de calidad.",
  "Si dejara mi trabajo mañana, mi vida social sería igual de activa.",
  "Tengo vínculos cercanos con personas de otras generaciones, que no son de mi familia.",
  "Tengo conversaciones frecuentes en las que digo lo que me pasa sin miedo a que me juzguen."],
  "Social")

body += pillar(7, 5, "Finanzas<br>con Propósito",
  "No cuánto tienes. Cuánto sabes de lo que tienes, y para qué lo estás guardando.", [
  "Sé cuánto cuesta un mes de mi vida. Con número, no con estimación.",
  "Sé cuánto voy a recibir al mes cuando deje de trabajar. También con número.",
  "Puedo acceder en menos de una semana al dinero que necesitaría para cubrir un año de mis gastos, ya sea en efectivo o vendiendo algo.",
  "Tengo planificado con números cómo voy a financiar los años en que pueda necesitar cuidados, y lo tengo conversado con mi familia.",
  "Lo que ahorro tiene destinos definidos y planificados, no es solo ahorrar por si acaso."],
  "Finanzas")

body += f"""
<div class="page">
  <div class="kicker">Tu perfil</div>
  <h2>Los cinco juntos</h2>
  <div class="rule"></div>
  <p style="margin-bottom:7mm;">Anota el total de cada pilar y marca ese número en su fila. El color te dice en qué zona caíste, y la forma del conjunto dice más que los números sueltos.</p>
  <table class="scoregrid">
    {row("Propósito")}{row("Físico")}{row("Mental")}{row("Social")}{row("Finanzas")}
  </table>
  <table class="zonekey"><tr>
    <td style="width:30mm"></td><td style="width:41mm">Atención (5–11)</td>
    <td style="width:41mm">Intermedia (12–18)</td><td>Sólida (19–25)</td><td style="width:16mm"></td>
  </tr></table>
  <div class="band at"><span class="bn">5 – 11</span><span class="bt">Zona de atención</span>
    <div class="bd">Probablemente este es tu cuello de botella. No significa que estés mal: significa que es el pilar donde una acción tiene más impacto que en cualquier otro lado.</div></div>
  <div class="band mid"><span class="bn">12 – 18</span><span class="bt">Zona intermedia</span>
    <div class="bd">Hay algo funcionando, aunque no de forma sistemática. Es el rango más frecuente y también el más fácil de mover: acá los cambios pequeños se notan rápido.</div></div>
  <div class="band ok"><span class="bn">19 – 25</span><span class="bt">Zona sólida</span>
    <div class="bd">Está instalado. Este pilar no es donde tienes que poner tu energía ahora.</div></div>
  <div class="pgnum">8</div>
</div>

<div class="page">
  <div class="kicker">Lo importante</div>
  <h2>El efecto dominó</h2>
  <div class="rule"></div>
  <p class="lead">Cualquiera puede hacerte una lista de cinco pilares. Lo que casi nadie explica es que no funcionan por separado.</p>
  <div class="hl">Tu pilar más bajo no es solamente tu pilar más bajo. Es el que está frenando a los otros cuatro.</div>
  <p style="margin-bottom:6mm;">Por eso es donde una sola acción genera más impacto. Busca el tuyo abajo.</p>
""" + drag("Si tu más bajo es Propósito", [
  "Arrastra <strong>Finanzas</strong>: sin dirección, ningún monto alcanza, porque no sabes para qué lo estás guardando.",
  "Arrastra <strong>Social</strong>: cuando el rol laboral se va, se lleva de una vez el círculo de colegas, reuniones y almuerzos.",
  "Arrastra <strong>Mental y Cognitivo</strong>: sin proyectos que te exijan, usas cada vez menos tus capacidades mentales, y lo que se deja de usar se deteriora.",
]) + drag("Si tu más bajo es Físico", [
  "Arrastra <strong>Mental y Cognitivo</strong>: la mala salud física está fuertemente asociada a mayor riesgo de enfermedades neurodegenerativas.",
  "Arrastra <strong>Social</strong>: la autonomía física es lo que te permite salir de la casa y sostener tus vínculos.",
  "Arrastra <strong>Finanzas</strong>: la pérdida de autonomía puede desbaratar tu plan financiero, porque el gasto en cuidados es el que más se subestima.",
]) + drag("Si tu más bajo es Mental y Cognitivo", [
  "Arrastra <strong>Físico</strong>: sin descanso no hay recuperación, y tampoco energía para entrenar.",
  "Arrastra <strong>Social</strong>: cuando aparece deterioro cognitivo, seguir una conversación cuesta más, y la reacción natural es retirarse.",
  "Arrastra <strong>Propósito</strong>: perder capacidades cognitivas es lo que más preocupa a la gente en esta etapa, y sin cabeza no hay plan que se sostenga.",
]) + drag("Si tu más bajo es Social", [
  "Arrastra <strong>Mental y Físico</strong> a la vez: en la literatura de longevidad, la soledad crónica se comporta como un factor de riesgo, no como un tema emocional.",
  "Arrastra <strong>Propósito</strong>: sostener un propósito necesita gente alrededor, que celebre contigo lo que logras y te acompañe cuando algo se cae.",
]) + drag("Si tu más bajo es Finanzas", [
  "Arrastra <strong>Social</strong>: cuando la plata aprieta, lo primero que se recorta son las salidas, los viajes y los regalos. Restarse de las instancias sociales es barato hoy y caro después.",
  "Arrastra <strong>Mental</strong>: la incertidumbre financiera es un impuesto cognitivo que se paga todos los días.",
  "Arrastra <strong>Propósito</strong>: si no sabes si te alcanza, no exploras lo que te gustaría hacer. La falta de números termina limitando lo que te permites imaginar.",
]) + """
  <div class="pgnum">9</div>
</div>

<div class="page">
  <div class="kicker">Patrones frecuentes</div>
  <h2>Cinco perfiles<br>comunes</h2>
  <div class="rule"></div>
  <p style="margin-bottom:7mm;">Hay combinaciones que aparecen seguido en este perfil de personas. No son categorías clínicas ni salen de un estudio: son patrones que vale la pena mirar.</p>
  <div class="arch"><div class="ap">Finanzas alto · Propósito bajo</div><div class="an">El financista sin destino</div>
    <p>Tienes resuelto el cómo y no el para qué. Es frecuente en quien lleva años planificando el retiro en una planilla: el número está, la vida que quieres financiar con ese número no.</p></div>
  <div class="arch"><div class="ap">Propósito bajo · Social bajo</div><div class="an">Sostenido por el trabajo</div>
    <p>El perfil de mayor riesgo en la transición. Tu estructura de tiempo y tu círculo social vienen del mismo lugar, así que el día que se acabe el rol, pierdes los dos.</p></div>
  <div class="arch"><div class="ap">Social alto · Físico y Propósito bajos</div><div class="an">El que cuida a todos menos a sí mismo</div>
    <p>Tu semana está llena, pero de las urgencias y prioridades de otros. Se siente como cuidar a los tuyos, y por eso cuesta tanto verlo. La paradoja es que la persona que se cuida es la que puede seguir estando.</p></div>
  <div class="arch"><div class="ap">Todo entre 12 y 18</div><div class="an">El perfil parejo</div>
    <p>Ningún pilar grita, y eso hace más difícil saber por dónde empezar. Las causas son variadas: puede que nada esté instalado de forma sistemática, que estés en un momento de transición, que tu vida esté efectivamente equilibrada, o simplemente que hayas respondido con cautela sin marcar extremos. Acá la pregunta útil no es cuál está más bajo, sino cuál de los cinco arrastra más a los otros. Esa respuesta está en la página anterior.</p></div>
  <div class="arch"><div class="ap">Todo alto menos Físico</div><div class="an">El cuerpo postergado</div>
    <p>Ordenaste la carrera, la familia y las platas. El cuerpo era el que siempre podía esperar un poco más. Es un pilar donde el tiempo perdido cuesta mucho recuperarlo, aunque sí se puede.</p></div>
  <div class="note"><p>Si no te reconoces en ninguno, no fuerces la comparación. Estos son patrones frecuentes, no todas las categorías posibles, y tu perfil es simplemente tu perfil.</p></div>
  <div class="pgnum">10</div>
</div>

<div class="page close">
  <div class="kicker">Y ahora</div>
  <h2>Ya sabes cuál es el<br>pilar que te está<br>frenando</h2>
  <div class="rule"></div>
  <p class="lead">Tener el número no cambia nada por sí solo. Lo que sí produce un cambio son tus acciones, basadas en tus decisiones. Y eso incluye decidir, conscientemente, no hacer nada por ahora.</p>
  <p>La mayoría de la gente no llega mal al retiro por haber tomado malas decisiones. Llega mal por no haber tomado ninguna: por haber dejado que el trabajo definiera la estructura del día, que el círculo social se armara solo con quien aparecía, que el dinero se acumulara sin destino y que el cuerpo esperara a que hubiera tiempo.</p>
  <p>Hay una persona concreta que va a heredar estos cinco pilares exactamente como tú se los dejes. Es tu yo del futuro, la persona que vas a ser en diez, veinte o treinta años. Esta persona va a heredar el cuerpo, la cabeza, los vínculos y las finanzas que resulten de las acciones que tomes hoy.</p>
  <div class="hl">No hay nadie en el mundo en mejor posición que tú para cuidar a esa persona.</div>
  <div class="principle" style="font-family:Lora,serif; font-size:19pt; line-height:1.35; color:#F6E7B0; font-style:italic; margin:8mm 0; padding-left:7mm; border-left:2.5px solid #E65F2B;">¿Vas a actuar por inercia<br>o con intención?</div>
""" + cta("Si quieres que revisemos tu caso juntos,", "pdf-autodiagnostico") + """
  <div class="pgnum">11</div>
</div>
"""

html = wrap(body).replace('</style>', '</style>' + EXTRA)
open('autodiagnostico.html','w',encoding='utf-8').write(html)
open('autodiagnostico_px.html','w',encoding='utf-8').write(to_px(html))
print("diag OK")
