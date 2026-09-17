# -*- coding: utf-8 -*-
# Guía PILARES: los cinco pilares y el efecto dominó, en versión de lectura.
# Es la hermana corta del autodiagnóstico (build_diag.py): mismo marco y
# mismas cadenas del efecto dominó, sin las 25 preguntas. Pensada para quien
# recién llega al perfil y no se va a sentar doce minutos con un cuestionario.
# Si cambias el texto de las cadenas acá, revisa si también cambia allá.
from build_common import wrap, to_px, cta

EXTRA = """
  .pil { margin-bottom: 8mm; padding-bottom: 7mm; border-bottom: 1px solid #E3E5E4; }
  .pil:last-of-type { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
  .pil .pn { font-size: 8.5pt; letter-spacing: 2px; text-transform: uppercase;
             color: #E65F2B; font-weight: 500; margin-bottom: 1.5mm; }
  .pil h3 { font-family: 'Lora', serif; font-size: 17pt; font-weight: 700; color: #0E3A2F;
            margin-bottom: 2mm; }
  .pil .pd { font-size: 10.5pt; font-style: italic; color: #0E3A2F; opacity: .8; margin-bottom: 3.5mm; }
  .pil p { font-size: 11pt; line-height: 1.58; margin-bottom: 3.5mm; }
  .pil .sl { font-size: 8.5pt; letter-spacing: 2px; text-transform: uppercase;
             color: #0E3A2F; opacity: .55; font-weight: 500; margin-bottom: 2mm; }
  .pil ul { list-style: none; margin: 0; padding: 0; }
  .pil li { font-size: 10.5pt; line-height: 1.5; margin-bottom: 1.6mm; padding-left: 6mm; text-indent: -6mm; }
  .pil .qt { font-family: 'Lora', serif; font-style: italic; font-size: 10.5pt; color: #0E3A2F;
             margin: 0 0 3.5mm; padding-left: 5mm; border-left: 2px solid #F6E7B0; line-height: 1.5; }
  .pil .qt span { display: block; font-family: 'Poppins', sans-serif; font-style: normal;
                  font-size: 8.5pt; opacity: .6; margin-top: 1mm; }
  .arrow { color: #E65F2B; font-weight: 600; }

  /* Fichas de dominó que se apoyan hacia la derecha: la primera (naranja) es
     la que cae y empuja a las otras. Girar en torno a la esquina inferior
     derecha evita que la ficha invada el texto de abajo. */
  .tiles { margin: 10mm 0 10mm; height: 36mm; position: relative; }
  .tile { position: absolute; bottom: 0; width: 24mm; height: 34mm; background: #0E3A2F;
          color: #F6E7B0; font-size: 8pt; font-weight: 600; letter-spacing: 1px;
          text-transform: uppercase; text-align: center; padding-top: 14mm;
          -webkit-transform-origin: 100% 100%; }
  .tile.t1 { left: 6mm;   background: #E65F2B; color: #F8F9FA; -webkit-transform: rotate(24deg); }
  .tile.t2 { left: 40mm;  -webkit-transform: rotate(16deg); }
  .tile.t3 { left: 74mm;  -webkit-transform: rotate(9deg); }
  .tile.t4 { left: 108mm; -webkit-transform: rotate(3deg); }
  .tile.t5 { left: 142mm; }

  .drag { margin-bottom: 4.5mm; padding-left: 6mm; border-left: 2.5px solid #F6E7B0; }
  .drag h3 { font-size: 11.5pt; margin-bottom: 2.5mm; }
  .drag ul { list-style: none; margin: 0; padding: 0; }
  .drag li { font-size: 10.5pt; line-height: 1.45; margin-bottom: 1.4mm; padding-left: 6mm; text-indent: -6mm; }

  .pick { border-bottom: 1px solid #E3E5E4; padding: 5mm 0; }
  .pick table { width: 100%; border-collapse: collapse; }
  .pick .bx { width: 12mm; vertical-align: top; }
  .pick .bx span { display: inline-block; width: 7mm; height: 7mm; border: 1.5px solid #0E3A2F; }
  .pick .tx { font-size: 11.5pt; line-height: 1.55; font-weight: 300; vertical-align: top; }
  .pick .pl { font-size: 8.5pt; letter-spacing: 1.8px; text-transform: uppercase; color: #E65F2B;
              font-weight: 500; display: block; margin-bottom: 1mm; }
"""


def pilar(idx, nombre, lema, porque, senales, cita=None):
    lis = "".join(f'<li><span class="arrow">→</span> {s}</li>' for s in senales)
    qt = (f'<div class="qt">"{cita[0]}"<span>{cita[1]}</span></div>' if cita else "")
    return f"""
  <div class="pil">
    <div class="pn">Pilar {idx} de 5</div>
    <h3>{nombre}</h3>
    <div class="pd">{lema}</div>
    <p>{porque}</p>
    {qt}
    <div class="sl">Señales de que está bajo</div>
    <ul>{lis}</ul>
  </div>"""


def drag(title, bullets):
    lis = "".join(f'<li><span class="arrow">→</span> {b}</li>' for b in bullets)
    return f'<div class="drag"><h3>{title}</h3><ul>{lis}</ul></div>'


def pick(nombre, frase):
    return (f'<div class="pick"><table><tr><td class="bx"><span></span></td>'
            f'<td class="tx"><span class="pl">{nombre}</span>{frase}</td></tr></table></div>')


AUTODIAG = "https://disenatujubilacion.com/autodiagnostico?utm_source=pdf-pilares"

body = """
<div class="page cover">
  <div class="cover-inner">
    <div class="eyebrow">Diseña tu Jubilación</div>
    <h1>Tu jubilación<br>se juega en cinco<br>pilares. Y ninguno<br>cae solo.</h1>
    <div class="sub">Una guía corta para entender qué sostiene esta etapa, cómo se arrastran los pilares entre sí y por dónde te conviene empezar. Se lee en diez minutos.</div>
    <div class="footer">Guía · 5 pilares · Efecto dominó</div>
  </div>
</div>

<div class="page">
  <div class="kicker">Antes de empezar</div>
  <h2>Por qué cinco<br>y no uno</h2>
  <div class="rule"></div>
  <p class="lead">Cuando se habla de jubilación, casi siempre se habla de plata. Es razonable: es lo que se puede calcular, y es lo que te han preguntado toda la vida.</p>
  <p>El dinero resuelve una parte. Para vivir bien los años que vienen también hace falta algo que hacer con tus días, un cuerpo que te permita hacerlo, una cabeza que siga aprendiendo y gente cerca. Y un plan financiero que esté al servicio de todo eso.</p>
  <p>Esos son los cinco pilares con los que trabajamos: <strong>Propósito, Salud Física, Salud Mental y Cognitiva, Salud Social y Finanzas con Propósito</strong>. En las próximas páginas vas a ver qué es cada uno, por qué se mueve tanto al dejar de trabajar, cómo se arrastran entre sí y cuál es probablemente el tuyo más débil, sin cuestionarios largos.</p>
  <p>No venimos a decirte cómo se vive esta etapa. Es una decisión personal y es tuya. Venimos con método, con evidencia y con estructura. <strong>Quien decide eres tú.</strong></p>
  <div class="note">
    <p><strong>Qué es y qué no es esto.</strong> Una guía de orientación personal, no un diagnóstico. No evalúa tu salud ni reemplaza a tu médico, a un profesional de salud mental o a un asesor financiero. Si algo de lo que leas te preocupa, la conversación correcta es con ellos.</p>
  </div>
  <div class="pgnum">2</div>
</div>

<div class="page">
  <div class="kicker">Los cinco pilares</div>
  <h2>Qué sostiene<br>esta etapa</h2>
  <div class="rule"></div>
""" + pilar(1, "Vida con Propósito",
  "Dirección, identidad y estructura del tiempo. Es el pilar que organiza a los otros cuatro.",
  "El trabajo te daba, sin que lo pidieras, una razón para levantarte, un horario y una respuesta a la pregunta “¿y tú a qué te dedicas?”. Al jubilar, las tres hay que construirlas.",
  ["No tienes claro qué quieres hacer con tu tiempo cuando dejes de trabajar.",
   "Tus semanas tienen la forma que les dio el trabajo, no una que hayas diseñado.",
   "Imaginar tu último día de trabajo te da la sensación de perder parte de quién eres."]) + pilar(2, "Salud Física",
  "Fuerza, movimiento, alimentación y prevención. El objetivo es morir joven&hellip; a los 95.",
  "Es lo que te da autonomía: salir, viajar, cuidar a otros y resolver lo cotidiano sin depender de nadie. Y es el pilar donde el tiempo perdido más cuesta recuperar.",
  ["No haces entrenamiento de fuerza de forma regular.",
   "Hay un examen o control preventivo que vienes postergando.",
   "Tu actividad física depende de que “haya tiempo”."]) + """
  <div class="pgnum">3</div>
</div>

<div class="page">
""" + pilar(3, "Salud Mental y Cognitiva",
  "Sueño, aprendizaje y manejo de emociones. El pilar que decide si vas a seguir siendo tú.",
  "El trabajo le exigía a tu cabeza todos los días. Cuando esa exigencia se va, hay que reemplazarla con algo, porque las capacidades que se dejan de usar se deterioran.",
  ["La mayoría de las noches duermes mal o despiertas sin sentir que descansaste.",
   "Hace tiempo que no aprendes algo nuevo y desafiante fuera del trabajo.",
   "Cuando algo te altera, te dura el día entero."]) + pilar(4, "Salud Social",
  "Vínculos, compañía y pertenencia. El pilar que más gente subestima.",
  "Buena parte de tu vida social ocurre en el trabajo: el café, el almuerzo, la conversación de pasillo. Se va el mismo mes que el rol, y casi nadie lo nota hasta que ya pasó.",
  ["La mayoría de tus conversaciones de la semana son con gente del trabajo.",
   "No se te ocurren tres personas a las que llamar de madrugada por un problema.",
   "Tus encuentros con amigos quedan en “tenemos que juntarnos”."],
  ("Me faltaba algo: salir a la hora de colación, echar la talla, tomarme un café con un colega.",
   "Alejandro, participante del programa piloto")) + pilar(5, "Finanzas con Propósito",
  "Cuánto sabes de lo que tienes, y para qué lo estás guardando.",
  "Un monto sin destino no da tranquilidad, porque no sabes si alcanza para la vida que quieres. Las finanzas con propósito parten por esa vida y después hacen los números.",
  ["No sabes con número cuánto cuesta un mes de tu vida.",
   "No sabes con número cuánto vas a recibir al mes cuando dejes de trabajar.",
   "Ahorras “por si acaso”, sin destinos definidos."]) + """
  <div class="pgnum">4</div>
</div>

<div class="page">
  <div class="kicker">Lo importante</div>
  <h2>El efecto dominó</h2>
  <div class="rule"></div>
  <p class="lead">Cualquiera puede hacerte una lista de cinco pilares. Lo que casi nadie explica es que funcionan conectados.</p>
  <div class="tiles">
    <div class="tile t1">Social</div><div class="tile t2">Mental</div><div class="tile t3">Físico</div>
    <div class="tile t4">Propósito</div><div class="tile t5">Finanzas</div>
  </div>
  <div class="hl">Tu pilar más débil no se queda en ese pilar. Arrastra a los otros cuatro.</div>
  <p>Por eso trabajar un pilar aislado rinde poco: puedes tener las finanzas en orden y, aun así, llegar a esta etapa sin saber qué hacer con tus días ni con quién.</p>
  <p>Y por eso también hay una buena noticia. <strong>El pilar que más frena es el que más devuelve.</strong> Cuando lo fortaleces, los otros se mueven con él, y una sola acción bien elegida tiene más efecto que cinco repartidas.</p>
  <div class="note">
    <p><strong>Un patrón frecuente.</strong> En personas cuya identidad está muy ligada al trabajo, Propósito y Social suelen venir del mismo lugar: la estructura del día y el círculo de personas los daba el rol. El día que se acaba el rol, se pierden los dos a la vez.</p>
  </div>
  <div class="pgnum">5</div>
</div>

<div class="page">
  <div class="kicker">Cómo se arrastran</div>
  <h2>Qué arrastra<br>cada pilar</h2>
  <div class="rule"></div>
""" + drag("Si tu más débil es Propósito", [
  "Arrastra <strong>Finanzas</strong>: sin dirección, ningún monto alcanza, porque no sabes para qué lo estás guardando.",
  "Arrastra <strong>Social</strong>: cuando el rol laboral se va, se lleva de una vez el círculo de colegas, reuniones y almuerzos.",
  "Arrastra <strong>Mental y Cognitivo</strong>: sin proyectos que te exijan, usas cada vez menos tus capacidades mentales.",
]) + drag("Si tu más débil es Físico", [
  "Arrastra <strong>Mental y Cognitivo</strong>: la mala salud física está fuertemente asociada a mayor riesgo de enfermedades neurodegenerativas.",
  "Arrastra <strong>Social</strong>: la autonomía física es lo que te permite salir de la casa y sostener tus vínculos.",
  "Arrastra <strong>Finanzas</strong>: la pérdida de autonomía puede desbaratar tu plan financiero, porque el gasto en cuidados es el que más se subestima.",
]) + drag("Si tu más débil es Mental y Cognitivo", [
  "Arrastra <strong>Físico</strong>: sin descanso no hay recuperación, y tampoco energía para entrenar.",
  "Arrastra <strong>Social</strong>: cuando seguir una conversación cuesta más, la reacción natural es retirarse.",
  "Arrastra <strong>Propósito</strong>: sin cabeza no hay plan que se sostenga.",
]) + drag("Si tu más débil es Social", [
  "Arrastra <strong>Mental y Físico</strong> a la vez: en la literatura de longevidad, la soledad crónica se comporta como un factor de riesgo para la salud.",
  "Arrastra <strong>Propósito</strong>: sostener un propósito necesita gente alrededor, que celebre contigo lo que logras y te acompañe cuando algo se cae.",
]) + drag("Si tu más débil es Finanzas", [
  "Arrastra <strong>Social</strong>: cuando la plata aprieta, lo primero que se recorta son las salidas, los viajes y los regalos.",
  "Arrastra <strong>Mental</strong>: la incertidumbre financiera es una preocupación que se paga todos los días.",
  "Arrastra <strong>Propósito</strong>: si no sabes si te alcanza, no exploras lo que te gustaría hacer.",
]) + """
  <div class="pgnum">6</div>
</div>

<div class="page">
  <div class="kicker">En dos minutos</div>
  <h2>¿Cuál es tu<br>pilar más débil?</h2>
  <div class="rule"></div>
  <p>Lee estas cinco frases y marca <strong>la que es menos cierta para ti hoy</strong>. Si dudas entre dos, elige la que te incomodó más al leerla. Responde por lo que haces, no por lo que sabes que sería bueno hacer.</p>
""" + pick("Propósito", "Tengo claro qué quiero hacer con mi tiempo cuando deje de trabajar, o ahora que ya dejé de hacerlo.") \
    + pick("Físico", "Hago entrenamiento de fuerza al menos dos veces por semana y tengo mis controles preventivos al día.") \
    + pick("Mental y Cognitivo", "Duermo bien la mayoría de las noches y estoy aprendiendo algo nuevo fuera del trabajo.") \
    + pick("Social", "Si dejara mi trabajo mañana, mi vida social seguiría igual de activa.") \
    + pick("Finanzas", "Sé con número cuánto cuesta un mes de mi vida y cuánto voy a recibir al mes cuando deje de trabajar.") + f"""
  <p style="margin-top:7mm;">La que marcaste es probablemente tu punto de partida. Vuelve a la página anterior y mira qué está arrastrando.</p>
  <div class="note">
    <p><strong>Si quieres el dato completo.</strong> Esto es una aproximación rápida. El autodiagnóstico online tiene 25 preguntas, toma doce minutos y te muestra cómo estás en cada uno de los cinco pilares: <a href="{AUTODIAG}"><strong>disenatujubilacion.com/autodiagnostico</strong></a></p>
  </div>
  <div class="pgnum">7</div>
</div>

<div class="page close">
  <div class="kicker">Y ahora</div>
  <h2>Los cinco se<br>diseñan juntos</h2>
  <div class="rule"></div>
  <p class="lead">Saber cuál es tu pilar más débil no cambia nada por sí solo. Lo que produce un cambio son tus acciones, basadas en tus decisiones.</p>
  <p>La mayoría de la gente no llega mal al retiro por haber tomado malas decisiones. Llega mal por no haber tomado ninguna: por dejar que el trabajo definiera la estructura del día, que el círculo social se armara solo, que el dinero se acumulara sin destino y que el cuerpo esperara a que hubiera tiempo.</p>
  <div class="hl">Tu yo del futuro va a heredar estos cinco pilares tal como se los dejes.</div>
  <div class="principle">¿Vas a actuar por inercia<br>o con intención?</div>
""" + cta("Si quieres que revisemos tus cinco pilares juntos,", "pdf-pilares") + """
  <div class="pgnum">8</div>
</div>
"""

# EXTRA va DENTRO del primer <style>: to_px() solo convierte ese bloque.
html = wrap(body).replace('</style>', EXTRA + '</style>', 1)
open('pilares.html', 'w', encoding='utf-8').write(html)
open('pilares_px.html', 'w', encoding='utf-8').write(to_px(html))
print("pilares OK")
