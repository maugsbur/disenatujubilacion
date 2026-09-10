# -*- coding: utf-8 -*-
from build_common import wrap, to_px, cta

body = """
<div class="page cover">
  <div class="cover-inner">
    <div class="eyebrow">Diseña tu Jubilación</div>
    <h1>Las cuatro<br>conversaciones que<br>hay que tener antes<br>de jubilar</h1>
    <div class="sub">Una forma simple de empezar las cuatro conversaciones que casi nadie tiene a tiempo, y que casi todos terminan teniendo en el peor momento.</div>
    <div class="footer">Guía práctica · Cuatro conversaciones · Antes de jubilar</div>
  </div>
</div>

<div class="page">
  <div class="kicker">El problema</div>
  <h2>Mientras no se<br>hablan, se asumen</h2>
  <div class="rule"></div>
  <p class="lead">“Mi hijo me va a cuidar.” “Mi hermana se va a hacer cargo.” “Eso lo vemos cuando pase.”</p>
  <p>Ninguna de esas frases es un acuerdo. Son suposiciones que nadie verificó, y que muchas veces la otra persona ni siquiera sabe que existen. A veces esa persona tiene una idea completamente distinta de lo que va a pasar. A veces tiene la misma idea, pero no sabe cómo, ni con qué plata, ni por cuánto tiempo.</p>
  <div class="hl">La diferencia entre una suposición y un acuerdo es una conversación.</div>
  <p> Una sola, de treinta o cuarenta minutos, que casi siempre resulta menos incómoda de lo que uno se imaginó durante meses.</p>
  <p>Lo que sí es incómodo es la otra versión: la conversación que no se tuvo y que termina ocurriendo en un pasillo de hospital, con prisa, con miedo y con gente que no está en condiciones de pensar bien.</p>
  <p>No venimos a decirte cómo se vive esta etapa. Es una decisión personal y es tuya. Venimos con método, con evidencia y con estructura. <strong>Quien decide eres tú</strong>, empezando por cuál de estas conversaciones vas a tener primero.</p>
  <div class="note">
    <p>Estas conversaciones no se posponen por descuido. Se posponen porque tocan cosas reales: la propia fragilidad, el dinero, el peso que uno puede llegar a ser para los demás. Que incomoden no significa que estés haciendo algo mal. Significa que importan.</p>
  </div>
  <div class="pgnum">2</div>
</div>

<div class="page">
  <div class="kicker">Las cuatro</div>
  <h2>Qué hay que hablar</h2>
  <div class="rule"></div>
  <p style="margin-bottom:8mm">Cada una tiene una pregunta central. Si logras que esa pregunta quede respondida, la conversación cumplió su propósito.</p>

  <div class="item">
    <h3>1 · Cuidados</h3>
    <p>Qué pasa si en algún momento necesitas ayuda para el día a día. Quién, cómo, y con qué se paga.</p>
    <span class="qq">Si yo necesitara ayuda todos los días, ¿qué pasaría?</span>
  </div>

  <div class="item">
    <h3>2 · Dónde y cómo quieres vivir</h3>
    <p>En tu casa, con alguien de la familia, en una residencia. Y sobre todo: qué es lo que no estás dispuesto a negociar.</p>
    <span class="qq">¿Qué es lo que no querría perder, aunque todo lo demás cambie?</span>
  </div>

  <div class="item">
    <h3>3 · Dinero</h3>
    <p>Qué pasa si no alcanza. Qué esperas tú de tus hijos, y qué esperan ellos de ti. Casi nunca coincide, y casi nunca se pregunta.</p>
    <span class="qq">Si mi dinero no alcanza, ¿quién pone la diferencia?</span>
  </div>

  <div class="item">
    <h3>4 · Qué pasa con tus bienes</h3>
    <p>Qué quieres que ocurra y por qué. Si hay algo que preferirías dar en vida. Si hay algo que va a generar conflicto y conviene nombrar ahora.</p>
    <span class="qq">¿Qué está dando cada uno por hecho que ya está decidido?</span>
  </div>
  <div class="pgnum">3</div>
</div>

<div class="page">
  <div class="kicker">Un punto importante</div>
  <h2>El papel no reemplaza<br>la conversación</h2>
  <div class="rule"></div>
  <p class="lead">Mucha gente cree que esto se resuelve firmando un documento. Conviene saber dos cosas antes.</p>
  <h3>Primero: depende mucho de dónde vivas</h3>
  <p>En América Latina el estatus legal de las voluntades anticipadas varía bastante de un país a otro. En algunos existe una figura regulada, con formalidades definidas y efecto vinculante. En otros no hay norma que las regule, y el documento vale como orientación pero no obliga legalmente a nadie.</p>
  <p>Averigua cómo es en el tuyo. Es una pregunta concreta para un abogado o para tu sistema de salud, y la respuesta cambia bastante lo que conviene hacer.</p>
  <h3>Segundo: esto es igual en todas partes</h3>
  <p>Un documento que la persona designada no conoce, no entiende o no encuentra a tiempo, no sirve. Y aunque lo encuentre, si nunca conversaron, va a tener que interpretar en el peor momento qué quisiste decir con cada frase.</p>
  <div class="hl">Lo que funciona en la práctica es que alguien sepa qué querías y por qué.</div>
  <p> Con eso puede decidir bien incluso frente a una situación que ustedes nunca previeron. Sin eso, ningún papel lo salva.</p>
  <div class="note">
    <p>Por eso el orden correcto es este: primero la conversación, después el documento si en tu país corresponde. Al revés casi nunca funciona.</p>
  </div>
  <div class="pgnum">4</div>
</div>

<div class="page">
  <div class="kicker">La herramienta</div>
  <h2>Cómo diseñar<br>la conversación</h2>
  <div class="rule"></div>
  <p>Lo que hace que estas conversaciones se descarrilen no es el tema: es que empiezan como reproche o como anuncio. Esta estructura evita las dos cosas.</p>
  <div class="formula">Hecho concreto &nbsp;+&nbsp; Cómo me hace sentir<br>+&nbsp; Qué necesito &nbsp;+&nbsp; Qué te pido concretamente</div>
  <p style="margin-bottom:6mm">No culpa a nadie, no exige una respuesta inmediata y deja claro qué esperas de la otra persona.</p>

  <div class="example">
    <div class="el">Ejemplo · cuidados, con un hijo</div>
    <p>“Cumplí 64 y todavía no hemos hablado de qué pasaría si yo necesitara ayuda para el día a día. Me da algo de vergüenza sacar el tema y a la vez me deja intranquilo no haberlo hecho. Necesito estar en paz sabiendo que tú y yo tenemos claro y acordado qué vamos a hacer si eso pasa. Te pido que nos sentemos una hora este mes a conversarlo, sin decidir nada todavía.”</p>
  </div>

  <div class="example">
    <div class="el">Ejemplo · bienes, entre hermanos</div>
    <p>“Cuando hablamos de la casa el otro día, cada uno dio por hecho una cosa distinta. Me incomoda que esto quede flotando y termine saliendo en un mal momento. Necesito claridad de qué vamos a hacer. Te pido que busquemos una fecha para hablarlo con calma, antes de fin de mes.”</p>
  </div>
  <div class="pgnum">5</div>
</div>

<div class="page">
  <div class="kicker">Para que resulte</div>
  <h2>Cuatro reglas</h2>
  <div class="rule"></div>
  <div class="rules">
    <div class="rule-i">
      <span class="rn">1</span><span class="rt">Avisa el tema antes</span>
      <div class="rd">Nunca emboscar. Un mensaje corto un par de días antes, del tipo «quiero conversar contigo sobre qué pasaría si yo necesitara ayuda», le da a la otra persona tiempo de llegar pensando en vez de reaccionando. La mitad de las conversaciones difíciles fracasan por sorpresa, no por contenido.</div>
    </div>
    <div class="rule-i">
      <span class="rn">2</span><span class="rt">Un tema por conversación</span>
      <div class="rd">Cuidados, vivienda, dinero y bienes son cuatro conversaciones, no una. Juntarlas garantiza que todas queden a medias y que alguna genere problemas para las otras tres. Si el tema se desvía, anótalo y déjalo para la próxima.</div>
    </div>
    <div class="rule-i">
      <span class="rn">3</span><span class="rt">No busques cerrar, busca abrir</span>
      <div class="rd">El objetivo de la primera conversación no es llegar a un acuerdo. Es que el tema deje de ser intocable. Si terminas sin decisión pero con la certeza de que pueden volver a hablarlo, resultó.</div>
    </div>
    <div class="rule-i">
      <span class="rn">4</span><span class="rt">Si no se puede decidir hoy, define cuándo</span>
      <div class="rd">Hay cosas que no se pueden decidir con la información que tienes ahora. Está bien. Lo que no está bien es dejarlo abierto: escribe qué falta para poder decidir y en qué fecha lo van a retomar. Eso sigue siendo decidir.</div>
    </div>
  </div>
  <div class="pgnum">6</div>
</div>

<div class="page">
  <div class="kicker">Tu turno</div>
  <h2>Hoja de preparación</h2>
  <div class="rule"></div>
  <p style="margin-bottom:8mm">Llena esto antes de proponer la conversación. Diez minutos acá te ahorran una hora incómoda después.</p>

  <div class="field"><div class="fl">Con quién voy a hablar</div><div class="blank"></div></div>
  <div class="field"><div class="fl">Cuál de las cuatro conversaciones es (una sola)</div><div class="blank"></div></div>
  <div class="field"><div class="fl">Qué quiero que quede claro al terminar</div><div class="blank"></div><div class="blank"></div></div>
  <div class="field"><div class="fl">Qué temo que pase en esa conversación</div><div class="blank"></div><div class="blank"></div></div>
  <div class="field"><div class="fl">Cómo voy a avisar el tema, y cuándo se lo propongo</div><div class="blank"></div><div class="blank"></div></div>
  <div class="pgnum">7</div>
</div>

<div class="page close">
  <div class="kicker">Para terminar</div>
  <h2>Que no decida<br>la crisis por ti</h2>
  <div class="rule"></div>
  <p class="lead">Estas conversaciones van a ocurrir. Esa parte no está en discusión. Lo único que está en discusión es si van a ocurrir cuando tú las elijas, o cuando algo se rompa.</p>
  <p>La versión que eliges tú pasa un domingo en la tarde, con café, y se puede pausar y retomar. La otra pasa en un pasillo, con prisa y con gente asustada tomando decisiones que van a durar años.</p>
  <p>Empieza por una. La que menos ganas te dio tener suele ser la más importante.</p>
  <p>Y hay alguien más en juego: tu yo del futuro, la persona que vas a ser en diez, veinte o treinta años. Esta persona va a vivir con las consecuencias de estas conversaciones, las hayas tenido o no.</p>
  <div class="principle">¿Vas a actuar por inercia<br>o con intención?</div>
""" + cta("Si quieres diseñar estas conversaciones con método en vez de improvisarlas,", "pdf-hablar") + """
  <div class="pgnum">8</div>
</div>
"""

open('hablar.html','w',encoding='utf-8').write(wrap(body))
open('hablar_px.html','w',encoding='utf-8').write(to_px(wrap(body)))
print("hablar OK")
