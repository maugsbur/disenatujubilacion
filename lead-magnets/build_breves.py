# -*- coding: utf-8 -*-
# Versiones breves (2 páginas) de las cuatro guías.
#
# Qué son: lo que se adjunta al correo cuando alguien deja su dirección desde
# Instagram. La versión completa de cada guía queda para quien sigue la
# conversación, y la entrega Margarita a mano. Por eso acá no hay enlace a la
# guía larga: no está listada en ninguna parte.
#
# Para quién: profesional o líder de 55 a 60 años, con la identidad muy
# pegada a su trabajo, próximo a jubilar, que acaba de ver una pieza en
# Instagram sobre este problema. Llega interesado y con poco tiempo. Asume
# que ya entendió el problema: no hay que convencerlo de nuevo, hay que
# darle el marco completo rápido y dejar clara la conversación que sigue.
#
# Regla de estructura, igual en las cuatro: portada integrada con la promesa
# · el problema en pocas líneas · lo esencial · el mismo CTA a la llamada de
# evaluación. Todo el contenido sale de la guía larga; acá no se inventa
# nada nuevo.
from build_common import wrap, to_px, cta

EXTRA = """
  /* La portada no ocupa una página entera: es una franja verde arriba de la
     primera. En dos páginas no sobra el espacio de una portada completa. */
  .brief { padding: 0 0 15mm; }
  .brief-top { background: #0E3A2F; color: #F8F9FA; padding: 15mm 18mm 13mm; margin-bottom: 9mm; }
  .brief-top .eyebrow { font-size: 9pt; letter-spacing: 3px; text-transform: uppercase;
                        color: #E65F2B; font-weight: 500; margin-bottom: 7mm; }
  .brief-top h1 { font-family: 'Lora', serif; font-size: 23pt; line-height: 1.14;
                  font-weight: 700; color: #F6E7B0; margin-bottom: 6mm; }
  .brief-top .sub { font-size: 11.5pt; line-height: 1.55; color: #DCE2E2;
                    font-weight: 300; max-width: 150mm; }
  .brief-body { padding: 0 18mm; }
  .brief-body.p2 { padding-top: 14mm; }

  .mini { margin-bottom: 3mm; padding-left: 6mm; border-left: 2.5px solid #F6E7B0; }
  .mini .mt { font-size: 11pt; font-weight: 600; color: #0E3A2F; }
  .mini .md { font-size: 10pt; line-height: 1.38; font-weight: 300; margin-top: 1mm; }
  .mini .mq { font-family: 'Lora', serif; font-style: italic; font-size: 9.5pt;
              color: #0E3A2F; display: block; margin-top: 1mm; }

  .step { margin-bottom: 2.5mm; }
  .step .sn { font-family: 'Lora', serif; font-size: 12pt; font-weight: 700; color: #E65F2B;
              display: inline-block; width: 7mm; }
  .step .st { font-size: 10.5pt; line-height: 1.5; font-weight: 300; }
  .step .st strong { font-weight: 600; color: #0E3A2F; }

  .brief .cta { margin-top: 7mm; padding: 6mm; }
  .brief .formula { padding: 5mm; margin: 4mm 0; font-size: 12pt; }
  .brief .example { padding: 4mm 5mm; margin-bottom: 3mm; }
  .brief .note { margin-top: 5mm; }
  .brief h2 { font-size: 20pt; margin-bottom: 5mm; }
  .brief h3 { margin-top: 5mm; }
  .brief p { font-size: 11pt; line-height: 1.6; margin-bottom: 4mm; }
  .brief .lead { font-size: 12pt; }
  .brief .hl { font-size: 13pt; margin: 5mm 0; }
"""


def mini(titulo, desc, cita=None):
    q = f'<span class="mq">{cita}</span>' if cita else ""
    return f'<div class="mini"><div class="mt">{titulo}</div><div class="md">{desc}</div>{q}</div>'


def step(n, texto):
    return f'<div class="step"><span class="sn">{n}</span><span class="st">{texto}</span></div>'


def pagina1(titulo, sub, cuerpo):
    return f"""
<div class="page brief">
  <div class="brief-top">
    <div class="eyebrow">Diseña tu Jubilación</div>
    <h1>{titulo}</h1>
    <div class="sub">{sub}</div>
  </div>
  <div class="brief-body">
{cuerpo}
  </div>
  <div class="pgnum">1</div>
</div>"""


def pagina2(cuerpo, cta_lead, utm):
    return f"""
<div class="page brief">
  <div class="brief-body p2">
{cuerpo}
{cta(cta_lead, utm)}
  </div>
  <div class="pgnum">2</div>
</div>"""


def guia(archivo, titulo, sub, p1, p2, cta_lead, utm):
    html = wrap(pagina1(titulo, sub, p1) + pagina2(p2, cta_lead, utm))
    html = html.replace('</style>', EXTRA + '</style>', 1)
    open(f'{archivo}.html', 'w', encoding='utf-8').write(html)
    open(f'{archivo}_px.html', 'w', encoding='utf-8').write(to_px(html))
    print(archivo, "OK")


# ----------------------------------------------------------------- PILARES --
guia('pilares-breve',
  "Tu bienestar en la jubilación se sostiene<br>sobre cinco pilares interdependientes",
  "Qué vas a necesitar en esa etapa, cómo dependen unos pilares de otros, y por cuál te conviene comenzar.",
  """    <div class="kicker">El problema</div>
    <p class="lead">La mayoría de las personas solo se preocupa del pilar financiero, sin saber que su bienestar también depende de otros cuatro.</p>
    <h3>Los pilares y una señal de alerta para cada uno</h3>
"""
  + mini("1 · Vida con Propósito", "Dirección, identidad y estructura del tiempo. El trabajo te entrega un rol, metas y horarios, y con eso un sentido de valor propio y de eficacia. Al jubilar eso desaparece, y ahí se abre una oportunidad de reinvención para quien la trabaja a tiempo.",
         "Alerta: tus semanas tienen la estructura que les dio el trabajo, no una que hayas diseñado intencionalmente.")
  + mini("2 · Salud Física", "Fuerza, movimiento, alimentación y prevención. Es lo que sostiene tu autonomía para salir, viajar y resolver lo cotidiano sin depender de nadie, y es donde el tiempo perdido cuesta más recuperar.",
         "Alerta: hay un examen o control preventivo que vienes postergando.")
  + mini("3 · Salud Mental y Cognitiva", "Sueño, aprendizaje y manejo de emociones. Hoy tu trabajo le exige algo a tu cabeza todos los días, y esa exigencia hay que reemplazarla después, porque las capacidades que se dejan de usar se deterioran.",
         "Alerta: hace tiempo que no aprendes algo nuevo y desafiante fuera del trabajo.")
  + mini("4 · Salud Social", "Vínculos, compañía y pertenencia. Buena parte de tu vida social ocurre hoy en el trabajo: el café, el almuerzo, la conversación de pasillo. Al jubilar se va con él, y reconstruirla toma más tiempo del que se suele calcular.",
         "Alerta: la mayoría de tus conversaciones de la semana son con gente del trabajo.")
  + mini("5 · Finanzas con Propósito", "Cuánto sabes de lo que tienes, y para qué lo estás guardando. Un monto sin destino no da tranquilidad, porque no hay con qué compararlo: primero se define la vida que quieres y después se calcula cuánto cuesta.",
         "Alerta: no sabes con número cuánto cuesta un mes de tu vida."),
  """    <div class="kicker">El efecto dominó</div>
    <h2>Cómo depende cada<br>pilar de los otros</h2>
    <div class="rule"></div>
    <p>Los cinco están conectados: cuando uno se debilita, empuja hacia abajo a los demás. A eso le llamamos el efecto dominó, y es la razón por la que conviene comenzar por el pilar más débil: una acción ahí rinde más que cinco repartidas.</p>
"""
  + step("→", "<strong>Propósito</strong> afecta a Finanzas y a Social: sin una dirección ningún monto se siente suficiente, y el círculo que venía con el rol se va con él.")
  + step("→", "<strong>Físico</strong> afecta a Social y a Finanzas: sin autonomía cuesta salir y sostener los vínculos, y el gasto en cuidados es el que más se subestima.")
  + step("→", "<strong>Mental y Cognitivo</strong> afecta a Físico y a Propósito: sin descanso no hay energía para entrenar, y sin claridad mental ningún plan se sostiene.")
  + step("→", "<strong>Social</strong> afecta a Mental y a Físico a la vez: la soledad crónica se comporta como un factor de riesgo para la salud.")
  + step("→", "<strong>Finanzas</strong> afecta a Propósito: si no sabes si te alcanza, no exploras lo que te gustaría hacer.")
  + """
    <h3>Por dónde comenzar</h3>
    <p>Vuelve a las cinco alertas de la página anterior y marca la que más se parece a tu semana. Ese es el pilar por el que te conviene comenzar, y arriba está lo que está afectando.</p>
    <div class="note">
      <p><strong>Qué es y qué no es esto.</strong> Orientación personal, no un diagnóstico. No reemplaza a tu médico, a un profesional de salud mental ni a un asesor financiero.</p>
    </div>""",
  "Si quieres que revisemos tus cinco pilares juntos,", "pdf-pilares-breve")

# -------------------------------------------------------------------- PLAN --
guia('plan-breve',
  "Cuatro decisiones que puedes<br>dejar tomadas antes de jubilar",
  "Se toman una sola vez y quedan hechas. Ninguna te pide cambiar tu rutina ni sostener un hábito nuevo.",
  """    <div class="kicker">El problema</div>
    <p class="lead">“Ya lo resolveré cuando llegue” es una respuesta frecuente, y es razonable: nadie quiere ocuparse hoy de algo que va a pasar en unos años.</p>
    <p>Lo que suele ocurrir es que esas decisiones no llegan solas ni con tiempo. El dinero, la salud, los cuidados y dónde vas a vivir aparecen juntos, muchas veces empujados por algo que se rompió, y hay que resolverlos rápido y bajo presión.</p>
    <div class="hl">Decidir con tiempo y reaccionar bajo presión llevan a resultados distintos.</div>
    <h3>Las dos primeras decisiones</h3>
"""
  + mini("1 · Un número", "Cuánto cuesta un mes de tu vida: lo que cuesta sostener tu vida normal durante treinta días, con número. Es la base de cualquier otro cálculo, y las estimaciones suelen quedar bastante por debajo del gasto real.",
         "Primer paso: abre la aplicación de tu banco y anota el total del último mes cerrado.")
  + mini("2 · Una hora médica", "Ese examen o control que vienes postergando. Uno, no todos. Postergarlo solo lo mueve a un momento en que vas a tener menos margen para decidir con calma.",
         "Primer paso: busca el teléfono o la aplicación y agenda. Si no sabes cuál, parte por tu médico general."),
  """    <div class="kicker">Las otras dos</div>
    <h2>Una persona<br>y una fecha</h2>
    <div class="rule"></div>
"""
  + mini("3 · Una persona", "Quién va a decidir por ti si en algún momento no puedes hacerlo. Si no lo defines tú, lo define la circunstancia, y suele quedar en quien esté más cerca ese día, sin saber qué querías. Es la decisión más barata de las cuatro y la que más peso le saca a tu familia.",
         "Primer paso: escríbele. “Quiero conversar algo contigo, ¿cuándo puedes?”.")
  + mini("4 · Una fecha", "Un encuentro presencial y recurrente con alguien que te importa, con día y hora fijos. Los vínculos que dependen del trabajo suelen irse con el trabajo, y lo que no se agenda no ocurre.",
         "Primer paso: elige a la persona y propón un día fijo. Semanal, quincenal o mensual, mientras se repita.")
  + """
    <h3>Elige una, no cuatro</h3>
    <p>Si intentas las cuatro esta semana, es probable que no hagas ninguna. Elige la que te dio más incomodidad al leerla, que suele ser la que más falta hace. Las otras tres van a seguir estando la semana que viene.</p>
    <div class="note">
      <p>Qué examen corresponde en tu caso lo define tu médico, con tu edad y tu historia sobre la mesa. Acá solo te recordamos agendar.</p>
    </div>""",
  "Si quieres que revisemos juntos estas y otras áreas tuyas,", "pdf-plan-breve")

# ------------------------------------------------------------------ HABLAR --
guia('hablar-breve',
  "Las cuatro conversaciones<br>que conviene tener<br>antes de jubilar",
  "Cuáles son, la pregunta que cada una debería dejar respondida y una forma de proponerlas que no termina en discusión.",
  """    <div class="kicker">El problema</div>
    <p class="lead">“Mi hijo me va a cuidar.” “Mi hermana se va a hacer cargo.” “Eso lo vemos cuando pase.”</p>
    <p>Ninguna de las tres es un acuerdo. Son suposiciones que nadie verificó, y que muchas veces la otra persona ni sabe que existen.</p>
    <div class="hl">La diferencia entre una suposición y un acuerdo es una conversación.</div>
    <p>Una sola, de treinta o cuarenta minutos. La alternativa es tenerla en un pasillo de hospital, con prisa y con gente que no está en condiciones de pensar bien.</p>
    <h3>Las cuatro, con su pregunta central</h3>
"""
  + mini("1 · Cuidados", "Qué pasa si necesitas ayuda diaria: quién, cómo y con qué se paga.",
         "Pregunta central: si yo necesitara ayuda todos los días, ¿qué pasaría?")
  + mini("2 · Dónde y cómo quieres vivir", "En tu casa, con familia, en una residencia. Y qué no estás dispuesto a negociar.",
         "Pregunta central: ¿qué no querría perder, aunque todo lo demás cambie?")
  + mini("3 · Dinero", "Qué pasa si no alcanza, y qué esperan tus hijos de ti y tú de ellos.",
         "Pregunta central: si mi dinero no alcanza, ¿quién pone la diferencia?")
  + mini("4 · Qué pasa con tus bienes", "Qué quieres que ocurra y qué conviene nombrar ahora, antes de que genere conflicto.",
         "Pregunta central: ¿qué está dando cada uno por hecho que ya está decidido?"),
  """    <div class="kicker">La herramienta</div>
    <h2>Cómo proponer<br>la conversación</h2>
    <div class="rule"></div>
    <p>Lo que las descarrila casi nunca es el tema. Suelen empezar como reproche o como anuncio, y ahí la otra persona se cierra.</p>
    <div class="formula">Hecho concreto &nbsp;+&nbsp; Cómo me hace sentir<br>+&nbsp; Qué necesito &nbsp;+&nbsp; Qué te pido concretamente</div>
    <div class="example">
      <div class="el">Ejemplo · cuidados, con un hijo</div>
      <p>“Cumplí 64 y no hemos hablado de qué pasaría si yo necesitara ayuda para el día a día. Me deja intranquilo. Te pido que nos sentemos una hora este mes a conversarlo, sin decidir nada todavía.”</p>
    </div>
    <h3>Tres reglas para que resulte</h3>
"""
  + step("1", "<strong>Avisa el tema antes.</strong> Un mensaje un par de días antes deja que la otra persona llegue pensando en vez de reaccionando.")
  + step("2", "<strong>Un tema por conversación.</strong> Son cuatro, y juntarlas hace que todas queden a medias.")
  + step("3", "<strong>Busca abrir el tema, no cerrarlo.</strong> Si terminas sin decisión y con la certeza de que pueden retomarlo, resultó. Y primero la conversación, después el papel.")
  + """""",
  "Si quieres diseñar estas conversaciones con método en vez de improvisarlas,", "pdf-hablar-breve")

# -------------------------------------------------------------- ENTUSIASMO --
guia('entusiasmo-breve',
  "Carlos jubiló antes de lo<br>que pensaba. Esto es lo<br>que hizo después.",
  "Un caso real, publicado con su autorización. La secuencia de lo que fue decidiendo, en qué orden, y lo que todavía le cuesta.",
  """    <div class="kicker">El punto de partida</div>
    <p class="lead">Carlos tiene 61 años y no eligió el momento de dejar de trabajar. Jubiló por invalidez, bastante antes de lo que tenía planeado.</p>
    <p>El trabajo desapareció de un día para otro y con él se fue la estructura que le ordenaba la semana, buena parte de las relaciones que dependían de la oficina y la manera en que entendía su propio papel en la familia. El espacio que dejó no quedó vacío ni un minuto: lo llenaron los trámites, los problemas de otros y lo que había que resolver hoy.</p>
    <p>Visto desde afuera era una persona ocupada. Visto desde adentro, era alguien cuya semana la escribían otros.</p>
    <div class="hl">Le sobraba actividad y le faltaba una dirección propia.</div>
    <p>Son dos cosas que se confunden fácil y que se resuelven distinto. Lo que lo sacó de ahí fue un horizonte concreto hacia el cual avanzar, con el que podía contrastar cada decisión del día. Un propósito sirve cuando ordena decisiones: si no cambia lo que haces un martes cualquiera, todavía es una intención.</p>""",
  """    <div class="kicker">La secuencia</div>
    <h2>Qué decidió,<br>en qué orden</h2>
    <div class="rule"></div>
    <p>El orden importa: cada paso hizo posible el siguiente.</p>
"""
  + step("1", "<strong>Puso el horizonte por escrito.</strong> Dejó de rondarle en la cabeza y pasó a ser una dirección concreta.")
  + step("2", "<strong>Auditó su agenda.</strong> Separó qué de su semana era suyo y qué eran prioridades de otros. Eso liberó el tiempo para lo demás.")
  + step("3", "<strong>Buscó los apoyos que le faltaban.</strong> Profesionales que necesitaba y no estaba viendo. El paso que más gente se salta.")
  + step("4", "<strong>Instaló hábitos alineados con ese horizonte.</strong> Los que servían a su objetivo, en vez de una lista genérica de hábitos saludables.")
  + step("5", "<strong>Ordenó sus finanzas hacia ese objetivo.</strong> El dinero pasó a tener una función que financiar.")
  + step("6", "<strong>Conversó con su familia.</strong> Puso sobre la mesa lo que venía postergando.")
  + """
    <h3>Lo que le ha costado</h3>
    <p>Empezar, mucho más que sostenerlo. El dinero, porque un patrimonio en el papel no es lo mismo que uno disponible cuando lo necesitas. Y las conversaciones con su familia, que lo apoyó y aun así costaron.</p>
    <div class="hl">La persona que se cuida es la que puede seguir estando.</div>
    <p>Lo replicable es esa secuencia: primero una dirección propia, después la agenda, los apoyos, los hábitos, el dinero y al final las conversaciones.</p>""",
  "Si te reconoces en algo de lo que le pasaba a Carlos al principio,", "pdf-entusiasmo-breve")
