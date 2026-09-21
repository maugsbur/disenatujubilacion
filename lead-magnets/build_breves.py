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
  .brief-top h1 { font-family: 'Lora', serif; font-size: 27pt; line-height: 1.13;
                  font-weight: 700; color: #F6E7B0; margin-bottom: 6mm; }
  .brief-top .sub { font-size: 11.5pt; line-height: 1.55; color: #DCE2E2;
                    font-weight: 300; max-width: 150mm; }
  .brief-body { padding: 0 18mm; }
  .brief-body.p2 { padding-top: 14mm; }

  .mini { margin-bottom: 4mm; padding-left: 6mm; border-left: 2.5px solid #F6E7B0; }
  .mini .mt { font-size: 11pt; font-weight: 600; color: #0E3A2F; }
  .mini .md { font-size: 10.5pt; line-height: 1.5; font-weight: 300; margin-top: 1mm; }
  .mini .mq { font-family: 'Lora', serif; font-style: italic; font-size: 10.5pt;
              color: #0E3A2F; display: block; margin-top: 1.5mm; }

  .step { margin-bottom: 2.5mm; }
  .step .sn { font-family: 'Lora', serif; font-size: 12pt; font-weight: 700; color: #E65F2B;
              display: inline-block; width: 7mm; }
  .step .st { font-size: 10.5pt; line-height: 1.5; font-weight: 300; }
  .step .st strong { font-weight: 600; color: #0E3A2F; }

  .brief .cta { margin-top: 8mm; padding: 6mm; }
  .brief .formula { padding: 5mm; margin: 4mm 0; font-size: 12pt; }
  .brief .example { padding: 4mm 5mm; margin-bottom: 3mm; }
  .brief .note { margin-top: 6mm; }
  .brief h2 { font-size: 20pt; margin-bottom: 5mm; }
  .brief h3 { margin-top: 6mm; }
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
  "Tu jubilación se juega en cinco pilares.<br>Y ninguno cae solo.",
  "Lo esencial en dos páginas: qué sostiene esta etapa, cómo se arrastran los pilares entre sí y cuál es el que hoy te está frenando.",
  """    <div class="kicker">El problema</div>
    <p class="lead">Casi todo el mundo llega a esta etapa con el pilar financiero revisado y los otros cuatro sin mirar nunca.</p>
    <p>El dinero resuelve una parte. Para vivir bien los años que vienen también hacen falta dirección, cuerpo, cabeza y gente cerca.</p>
    <div class="hl">Tu pilar más débil no se queda en ese pilar. Arrastra a los otros cuatro.</div>
    <h3>Los cinco pilares, y una señal de cada uno</h3>
"""
  + mini("1 · Vida con Propósito", "Dirección, identidad y estructura del tiempo. Organiza a los otros cuatro.",
         "Señal: tus semanas tienen la forma que les dio el trabajo, no una que hayas diseñado.")
  + mini("2 · Salud Física", "Fuerza, movimiento, alimentación y prevención. Es lo que sostiene tu autonomía.",
         "Señal: hay un examen o control preventivo que vienes postergando.")
  + mini("3 · Salud Mental y Cognitiva", "Sueño, aprendizaje y manejo de emociones. Decide si vas a seguir siendo tú.",
         "Señal: hace tiempo que no aprendes algo nuevo y desafiante fuera del trabajo.")
  + mini("4 · Salud Social", "Vínculos, compañía y pertenencia. El que más rápido se desarma al dejar de trabajar.",
         "Señal: la mayoría de tus conversaciones de la semana son con gente del trabajo.")
  + mini("5 · Finanzas con Propósito", "Cuánto sabes de lo que tienes, y para qué lo estás guardando.",
         "Señal: no sabes con número cuánto cuesta un mes de tu vida."),
  """    <div class="kicker">El efecto dominó</div>
    <h2>Qué arrastra cada pilar</h2>
    <div class="rule"></div>
    <p>Los cinco funcionan conectados, así que el que está más abajo frena a los demás. Por eso una acción bien elegida rinde más que cinco repartidas.</p>
"""
  + step("→", "<strong>Propósito</strong> arrastra a Finanzas, porque ningún monto alcanza si no sabes para qué lo guardas, y a Social, porque el círculo venía con el rol.")
  + step("→", "<strong>Físico</strong> arrastra a Social, porque la autonomía es lo que te permite salir, y a Finanzas, porque el gasto en cuidados es el más subestimado.")
  + step("→", "<strong>Mental y Cognitivo</strong> arrastra a Físico, porque sin descanso no hay energía, y a Propósito, porque sin cabeza no hay plan que se sostenga.")
  + step("→", "<strong>Social</strong> arrastra a Mental y a Físico a la vez: en la literatura de longevidad, la soledad crónica se comporta como un factor de riesgo para la salud.")
  + step("→", "<strong>Finanzas</strong> arrastra a Propósito, porque si no sabes si te alcanza, no exploras lo que te gustaría hacer.")
  + """
    <h3>El ejercicio de un minuto</h3>
    <p>Vuelve a las cinco señales de la página anterior y marca la que más se parece a tu semana de hoy. Ese es tu punto de partida, y arriba está lo que ese pilar está frenando.</p>
    <div class="note">
      <p><strong>Qué es y qué no es esto.</strong> Orientación personal, no un diagnóstico. No reemplaza a tu médico, a un profesional de salud mental ni a un asesor financiero.</p>
    </div>""",
  "Si quieres que revisemos tus cinco pilares juntos,", "pdf-pilares-breve")

# -------------------------------------------------------------------- PLAN --
guia('plan-breve',
  "Tu jubilación no se resuelve esta semana.<br>Estas cuatro acciones sí.",
  "Cuatro cosas que se hacen una sola vez y quedan hechas. Ninguna te pide cambiar tu rutina ni sostener un hábito nuevo.",
  """    <div class="kicker">El problema</div>
    <p class="lead">“Ya lo resolveré cuando llegue” es la respuesta más común, y es razonable. El problema es lo que pasa cuando llega.</p>
    <p>Las conversaciones de dinero, de salud, de cuidados y de dónde vas a vivir no llegan solas ni con tiempo. Llegan el mismo mes, casi siempre empujadas por algo que se rompió, y hay que resolverlas rápido y bajo presión.</p>
    <div class="hl">Diseñar y reaccionar son dos modos de actuar distintos, y el segundo produce resultados mucho peores.</div>
    <h3>Las dos primeras acciones</h3>
"""
  + mini("1 · Un número", "Cuánto cuesta un mes de tu vida. No lo que te gustaría gastar: lo que cuesta sostener tu vida normal durante treinta días. Es el número desde el cual se calcula todo lo demás, y las estimaciones suelen quedar bastante por debajo del gasto real.",
         "Primer paso: abre la aplicación de tu banco y anota el total del último mes cerrado.")
  + mini("2 · Una hora médica", "Ese examen o control que vienes postergando. Uno, no todos. Postergarlo no lo cancela, solo lo mueve a un momento en que tengas menos margen para decidir con calma.",
         "Primer paso: busca el teléfono o la aplicación y agenda. Si no sabes cuál, parte por tu médico general."),
  """    <div class="kicker">Las otras dos</div>
    <h2>Una persona<br>y una fecha</h2>
    <div class="rule"></div>
"""
  + mini("3 · Una persona", "Quién va a decidir por ti si en algún momento tú no puedes hacerlo. Si no lo decides tú, lo decide la circunstancia, y normalmente elige a quien esté más cerca ese día, sin que sepa qué querías. Es la decisión más barata de esta guía y la que más peso le saca a tu familia.",
         "Primer paso: escríbele. “Quiero conversar algo contigo, ¿cuándo puedes?”.")
  + mini("4 · Una fecha", "Un encuentro presencial y recurrente con alguien que te importa, con día y hora fijos. Los vínculos que dependen del trabajo se van con el trabajo, normalmente el mismo mes. Y lo que no se agenda no ocurre.",
         "Primer paso: elige a la persona y propón un día fijo. Semanal, quincenal o mensual, mientras se repita.")
  + """
    <h3>Elige una, no cuatro</h3>
    <p>Si intentas las cuatro esta semana, es bastante probable que no hagas ninguna. Elige la que te dio más incomodidad al leerla: casi siempre es la que más falta hace. Las otras tres van a seguir estando la semana que viene.</p>
    <div class="note">
      <p>La lista de exámenes y las decisiones de salud las define tu médico, con tu edad y tu historia sobre la mesa. Acá solo te recordamos agendar.</p>
    </div>""",
  "Si quieres que revisemos juntos estas y otras áreas tuyas,", "pdf-plan-breve")

# ------------------------------------------------------------------ HABLAR --
guia('hablar-breve',
  "Las cuatro conversaciones<br>que hay que tener<br>antes de jubilar",
  "Cuáles son, la pregunta que cada una tiene que dejar respondida y una forma de proponerlas que no termina en discusión.",
  """    <div class="kicker">El problema</div>
    <p class="lead">“Mi hijo me va a cuidar.” “Mi hermana se va a hacer cargo.” “Eso lo vemos cuando pase.”</p>
    <p>Ninguna es un acuerdo. Son suposiciones que nadie verificó, y que muchas veces la otra persona ni sabe que existen.</p>
    <div class="hl">La diferencia entre una suposición y un acuerdo es una conversación.</div>
    <p>Una sola, de treinta o cuarenta minutos. Lo incómodo es la otra versión: la que ocurre en un pasillo de hospital, con prisa.</p>
    <h3>Las cuatro, con su pregunta central</h3>
"""
  + mini("1 · Cuidados", "Qué pasa si necesitas ayuda diaria: quién, cómo y con qué se paga.",
         "Si yo necesitara ayuda todos los días, ¿qué pasaría?")
  + mini("2 · Dónde y cómo quieres vivir", "En tu casa, con familia, en una residencia. Y qué no estás dispuesto a negociar.",
         "¿Qué no querría perder, aunque todo lo demás cambie?")
  + mini("3 · Dinero", "Qué pasa si no alcanza, y qué esperan tus hijos de ti y tú de ellos.",
         "Si mi dinero no alcanza, ¿quién pone la diferencia?")
  + mini("4 · Qué pasa con tus bienes", "Qué quieres que ocurra y qué conviene nombrar ahora, antes de que genere conflicto.",
         "¿Qué está dando cada uno por hecho que ya está decidido?"),
  """    <div class="kicker">La herramienta</div>
    <h2>Cómo proponer<br>la conversación</h2>
    <div class="rule"></div>
    <p>Lo que las descarrila no es el tema: es que empiezan como reproche o como anuncio.</p>
    <div class="formula">Hecho concreto &nbsp;+&nbsp; Cómo me hace sentir<br>+&nbsp; Qué necesito &nbsp;+&nbsp; Qué te pido concretamente</div>
    <div class="example">
      <div class="el">Ejemplo · cuidados, con un hijo</div>
      <p>“Cumplí 64 y no hemos hablado de qué pasaría si yo necesitara ayuda para el día a día. Me deja intranquilo. Te pido que nos sentemos una hora este mes a conversarlo, sin decidir nada todavía.”</p>
    </div>
    <h3>Tres reglas para que resulte</h3>
"""
  + step("1", "<strong>Avisa el tema antes.</strong> Un mensaje un par de días antes deja que la otra persona llegue pensando en vez de reaccionando.")
  + step("2", "<strong>Un tema por conversación.</strong> Son cuatro, no una. Juntarlas garantiza que todas queden a medias.")
  + step("3", "<strong>No busques cerrar, busca abrir.</strong> Si terminas sin decisión y con la certeza de que pueden retomarlo, resultó. Y primero la conversación, después el papel.")
  + """""",
  "Si quieres diseñar estas conversaciones con método en vez de improvisarlas,", "pdf-hablar-breve")

# -------------------------------------------------------------- ENTUSIASMO --
guia('entusiasmo-breve',
  "Carlos jubiló antes de lo que pensaba.<br>Esto es lo que hizo después.",
  "Un caso real, publicado con su autorización. La secuencia de lo que fue decidiendo, en qué orden, y lo que todavía le cuesta.",
  """    <div class="kicker">El punto de partida</div>
    <p class="lead">Carlos tiene 61 años y no eligió el momento de dejar de trabajar. Jubiló por invalidez, bastante antes de lo que tenía planeado.</p>
    <p>El trabajo desapareció de un día para otro y con él se fue la estructura que le ordenaba la semana, buena parte de las relaciones que dependían de la oficina y la manera en que entendía su propio papel en la familia. El espacio que dejó no quedó vacío ni un minuto: lo llenaron los trámites, los problemas de otros y lo que había que resolver hoy.</p>
    <p>Visto desde afuera era una persona ocupada. Visto desde adentro, era alguien cuya semana la escribían otros.</p>
    <div class="hl">El problema de Carlos no era falta de actividad. Era falta de dirección propia.</div>
    <p>Son dos cosas que se confunden muy fácil y que se arreglan de manera distinta. Lo que lo sacó de ahí fue un horizonte concreto hacia el cual avanzar, contra el cual podía contrastar cada decisión del día. Un propósito sirve cuando ordena decisiones: si no cambia lo que haces un martes cualquiera, todavía es una intención.</p>""",
  """    <div class="kicker">La secuencia</div>
    <h2>Qué decidió,<br>en qué orden</h2>
    <div class="rule"></div>
    <p>El orden importa: cada paso hizo posible el siguiente.</p>
"""
  + step("1", "<strong>Puso el horizonte por escrito.</strong> Dejó de rondarle en la cabeza y pasó a ser una dirección concreta.")
  + step("2", "<strong>Auditó su agenda.</strong> Separó qué de su semana era suyo y qué eran prioridades de otros. Eso liberó el tiempo para lo demás.")
  + step("3", "<strong>Buscó los apoyos que le faltaban.</strong> Profesionales que necesitaba y no estaba viendo. El paso que más gente se salta.")
  + step("4", "<strong>Instaló hábitos alineados con ese horizonte.</strong> No hábitos saludables en abstracto, sino los que servían a su objetivo.")
  + step("5", "<strong>Ordenó sus finanzas hacia ese objetivo.</strong> El dinero pasó a tener una función que financiar.")
  + step("6", "<strong>Conversó con su familia.</strong> Puso sobre la mesa lo que venía postergando.")
  + """
    <h3>Lo que le ha costado</h3>
    <p>Empezar, mucho más que sostenerlo. El dinero, porque un patrimonio en el papel no es lo mismo que uno disponible cuando lo necesitas. Y las conversaciones con su familia, que lo apoyó y aun así costaron.</p>
    <div class="hl">La persona que se cuida es la que puede seguir estando.</div>
    <p>Lo replicable es esa secuencia: primero una dirección propia, después la agenda, los apoyos, los hábitos, el dinero y al final las conversaciones.</p>""",
  "Si te reconoces en algo de lo que le pasaba a Carlos al principio,", "pdf-entusiasmo-breve")
