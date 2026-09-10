# -*- coding: utf-8 -*-
from build_common import wrap, to_px, cta

def decision(n, num, kicker, title, que, porque, accion, hecho, extra=""):
    return f"""
<div class="page">
  <div class="numhead">{kicker}</div>
  <h2>{title}</h2>
  <div class="rule"></div>
  <div class="field"><div class="fl">Qué es</div><div class="fv">{que}</div></div>
  <div class="field"><div class="fl">Por qué esta y no otra</div><div class="fv">{porque}</div></div>
  <div class="action"><div class="al">Primer paso · menos de 5 minutos</div><div class="av">{accion}</div></div>
  <div class="done"><div class="dl">Cómo se ve "hecho"</div><div class="dv"><span class="chk"></span>{hecho}</div></div>
  {extra}
  <div class="pgnum">{n}</div>
</div>"""

body = """
<div class="page cover">
  <div class="cover-inner">
    <div class="eyebrow">Diseña tu Jubilación</div>
    <h1>Tu jubilación no<br>se resuelve esta<br>semana. Estas cuatro<br>acciones sí.</h1>
    <div class="sub">Sin planes de doce semanas, sin hábitos nuevos y sin agobio. Cuatro acciones que se hacen una vez y quedan hechas.</div>
    <div class="footer">Guía práctica · Cuatro acciones · Sin agobio</div>
  </div>
</div>

<div class="page">
  <div class="kicker">Antes de empezar</div>
  <h2>Esto no es un plan</h2>
  <div class="rule"></div>
  <p class="lead">No vas a diseñar tu jubilación en las próximas páginas. Vas a <strong>tomar acción y terminar cuatro cosas de tu lista</strong>.</p>
  <p>La diferencia importa. Hay áreas donde el cambio necesita hábitos: comer distinto, moverte, dormir mejor. Esos hay que sostenerlos, practicarlos y defenderlos de la vida que se te atraviesa, y por eso cuestan.</p><p>Estas cuatro no son de esas.</p>
  <p><strong>Son acciones que se hacen una sola vez.</strong> Y ojo con esto: no basta con decidirlas, hay que ejecutarlas. Ninguna te pide cambiar tu rutina, ninguna te pide constancia y ninguna se te puede caer en dos semanas. Cada una arranca con un primer paso que toma menos de cinco minutos y que puedes dar hoy mismo.</p>
  <p>Si el tema te viene pesando hace tiempo, ese es exactamente el motivo por el que esta guía es corta.</p>
  <div class="note">
    <p>No venimos a decirte cómo se vive esta etapa. Esa es una decisión personal y es tuya. Venimos con método, con evidencia y con estructura. <strong>Quien decide eres tú.</strong></p>
  </div>
  <div class="pgnum">2</div>
</div>

<div class="page">
  <div class="kicker">El costo de esperar</div>
  <h2>Por qué "ya lo<br>resolveré" no funciona</h2>
  <div class="rule"></div>
  <p class="lead">Es la respuesta más común, y es razonable: nadie quiere ocuparse hoy de algo que va a pasar en unos años.</p>
  <p>El problema es lo que ocurre cuando llega el momento.</p>
  <h3>Primero: llega todo junto</h3>
  <p>Las conversaciones de dinero, las de salud, las de cuidados, las de dónde vas a vivir y con quién. Ninguna llega sola y ninguna llega con tiempo. Llegan el mismo mes, casi siempre empujadas por algo que se rompió, y hay que resolverlas rápido y bajo presión. <strong>Diseñar y reaccionar son dos modos de actuar distintos</strong>, y el segundo produce resultados mucho peores.</p>
  <h3>Segundo: el dinero es una pata de cuatro</h3>
  <p>Tener las finanzas ordenadas es necesario y no es suficiente. Ningún monto compra una dirección para tus días, condición física, una cabeza que funcione ni gente cerca. Esas cuatro cosas se construyen con tiempo, y el tiempo es justamente lo que no vas a tener cuando decidas ocuparte.</p>
  <div class="note">
    <p>Las decisiones que tomas hoy, y sobre todo las que no tomas, las va a vivir tu yo del futuro. Es la persona que vas a ser en diez, veinte o treinta años. Esta persona va a heredar el cuerpo, la cabeza, los vínculos y las finanzas que resulten de las acciones que tomes hoy.</p>
  </div>
  <div class="pgnum">3</div>
</div>
"""

body += decision(4, 1, "Acción 1 de 4", "Un número",
  "Cuánto cuesta un mes de tu vida. No lo que te gustaría gastar ni lo que gastaste el mes de las vacaciones: lo que cuesta sostener tu vida normal durante treinta días.",
  "Porque <strong>es el número desde el cual se calcula cualquier otra cosa</strong>. Sin él, no se puede saber si te alcanza, cuánto te falta ni por cuánto tiempo estás cubierto. La mayoría de la gente tiene una estimación, y las estimaciones suelen estar entre un 20% y un 30% por debajo del gasto real.",
  "Abre la aplicación de tu banco y anota el total de gastos del último mes cerrado. Ese es tu punto de partida, aunque esté sucio.",
  "Tienes un número escrito en alguna parte, con fecha, y sabes qué incluye y qué no.",
  """<div class="note"><p><strong>Hay un segundo número.</strong> Este es el costo de subsistir. El otro es cuánto cuesta vivir bien: los viajes, los nietos, lo que le da sentido al resto. Casi nadie lo ha calculado nunca. Por ahora quédate con el primero.</p></div>""")

body += decision(5, 2, "Acción 2 de 4", "Una hora médica",
  "Agendar ese examen o control que vienes postergando. Uno. No todos.",
  "Porque postergarlo no lo cancela, solo lo mueve a un momento en que tengas menos margen para decidir con calma. Y porque el costo de agendar es una llamada, mientras que el costo de no hacerlo es desconocido.",
  "Busca el teléfono o la aplicación y agenda. Si no sabes cuál corresponde, agenda con tu médico general y llega con la pregunta.",
  "<strong>Ya te lo hiciste, conoces el resultado y sabes qué significa.</strong> No basta con agendarlo: la hora se puede postergar por algo que parezca más importante, y normalmente aparece algo.",
  """<div class="field" style="margin-top:6mm"><div class="fl">Por si te sirve para recordar cuál</div><div class="fv">El que tu médico te pidió y no hiciste &nbsp;·&nbsp; el control anual que dejaste de hacer en algún momento y no retomaste &nbsp;·&nbsp; el dental &nbsp;·&nbsp; el oftalmológico &nbsp;·&nbsp; el de audición</div></div>
  <div class="warn"><p>Esta lista es solo para ayudarte a recordar. No es una indicación médica ni una recomendación de qué examen corresponde en tu caso: eso lo define tu médico, con tu edad, tu historia y la de tu familia sobre la mesa.</p></div>""")

body += decision(6, 3, "Acción 3 de 4", "Una persona",
  "Definir quién va a decidir por ti si en algún momento tú no puedes hacerlo, y decírselo a esa persona.",
  "Porque si no lo decides tú, lo decide la circunstancia. Y la circunstancia normalmente elige a quien esté más cerca ese día, sin que esa persona sepa qué querías, sin que se lo haya pensado nunca y en el peor momento posible para pensarlo. <strong>Es la decisión más barata de esta guía y la que más peso le saca de encima a tu familia.</strong>",
  "Escríbele a esa persona: “quiero conversar algo contigo, ¿cuándo puedes?”. Nada más. La conversación viene después.",
  "Esa persona sabe que es ella, y sabe a grandes rasgos qué querrías tú.",
  """<div class="note"><p>No necesitas tener todas las respuestas para tener la conversación. Basta con que la otra persona entienda tu criterio general: qué es importante para ti y qué no estarías dispuesto a aceptar. El detalle se puede ir llenando después.</p></div>""")

body += decision(7, 4, "Acción 4 de 4", "Una fecha",
  "Un encuentro presencial y recurrente con alguien que te importa, con día y hora fijos en el calendario.",
  "Porque los vínculos que dependen del trabajo se van con el trabajo, normalmente el mismo mes. Y porque lo que no se agenda no ocurre: los encuentros que quedan en “tenemos que juntarnos alguna vez” no se materializan casi nunca. Presencial y recurrente, porque es la combinación que sostiene una relación en el tiempo.",
  "Elige a la persona y propón un día y una hora fijos. Semanal, quincenal o mensual: da lo mismo cuál, mientras se repita.",
  "Está en el calendario, tiene día fijo y ya ocurrió al menos una vez.")

body += """
<div class="page close">
  <div class="kicker">Para terminar</div>
  <h2>Elige una,<br>no cuatro</h2>
  <div class="rule"></div>
  <p class="lead">Si intentas las cuatro esta semana, es bastante probable que no hagas ninguna. Eso no sería falta de compromiso: sería exactamente el mismo agobio que te trajo hasta acá.</p>
  <p><strong>Elige la que te dio más incomodidad al leerla.</strong> Casi siempre es la que más falta hace, y esa incomodidad es información, no una señal de que no corresponde.</p>
  <p><strong>Da tu primer paso hoy.</strong> Las otras tres van a seguir estando la semana que viene.</p>
  <div class="principle">¿Vas a actuar por inercia<br>o con intención?</div>
""" + cta("Si quieres que revisemos juntos estas y otras áreas tuyas,", "pdf-plan") + """
  <div class="pgnum">8</div>
</div>
"""

open('plan.html','w',encoding='utf-8').write(wrap(body))
open('plan_px.html','w',encoding='utf-8').write(to_px(wrap(body)))
print("plan OK")
