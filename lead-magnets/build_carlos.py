# -*- coding: utf-8 -*-
from build_common import wrap, to_px, cta

body = """
<div class="page cover">
  <div class="cover-inner">
    <div class="eyebrow">Diseña tu Jubilación</div>
    <h1>Carlos jubiló antes<br>de lo que pensaba.<br>Esto es lo que<br>hizo después.</h1>
    <div class="sub">La secuencia real de las acciones que fue tomando, en qué orden, y lo que todavía le está costando. No es una historia de motivación: es un método.</div>
    <div class="footer">Caso real · Publicado con su autorización</div>
  </div>
</div>

<div class="page">
  <div class="kicker">El punto de partida</div>
  <h2>Todo cambió<br>de golpe</h2>
  <div class="rule"></div>
  <p class="lead">Carlos tiene 61 años y no eligió el momento de dejar de trabajar. Jubiló por invalidez, bastante antes de lo que tenía planeado.</p>
  <p>Cuando el retiro se planifica, hay tiempo para prepararse. Cuando llega de golpe, no lo hay. El trabajo desapareció de un día para otro y con él se fue la estructura que le ordenaba la semana, buena parte de las relaciones que dependían de la oficina y la manera en que entendía su propio papel en la familia.</p>
  <p>El espacio que dejó no quedó vacío ni un minuto. Lo llenaron las urgencias cotidianas y las preocupaciones de los suyos: los trámites, los problemas de otros, lo que había que resolver hoy.</p>
  <p>Visto desde afuera era una persona ocupada. Visto desde adentro, era alguien cuya semana la escribían otros. Mientras tanto subió de peso, las finanzas quedaron sin un plan que reemplazara al sueldo, y su condición física fue cediendo.</p>
  <div class="hl">El problema de Carlos no era falta de actividad. Era falta de dirección propia.</div>
  <p>Son dos cosas que se confunden muy fácil, y se arreglan de manera distinta.</p>
  <div class="pgnum">2</div>
</div>

<div class="page">
  <div class="kicker">El giro</div>
  <h2>Un horizonte<br>propio</h2>
  <div class="rule"></div>
  <p class="lead">Carlos tiene Parkinson. En algún momento apareció frente a él una posibilidad concreta: una operación con tecnología nueva que podría ayudarle a controlar la enfermedad.</p>
  <p>Todavía no tiene fecha. Y aun así, esa posibilidad cambió su forma de organizar el tiempo, porque le dio algo que no tenía: un horizonte propio hacia el cual avanzar. Llegar en las mejores condiciones posibles cuando esa puerta se abra, para poder controlar la enfermedad mientras todavía es posible y disfrutar los años que vienen.</p>
  <p>La decisión médica es suya y de sus médicos, y no es de lo que trata esta guía. Lo que cuenta acá es lo que ese horizonte hizo con su agenda.</p>
  <p>Eso es un propósito en el sentido útil de la palabra. No una frase inspiradora ni una declaración sobre quién es uno, sino una dirección concreta que permite preguntarse, frente a cada decisión del día, si acerca o si aleja.</p>
  <div class="note">
    <p><strong>Un propósito sirve cuando ordena decisiones.</strong> Si no cambia lo que haces un martes cualquiera, todavía no es un propósito: es una intención. Y no necesita fecha para funcionar. Necesita dirección.</p>
  </div>
  <div class="pgnum">3</div>
</div>

<div class="page">
  <div class="kicker">La secuencia</div>
  <h2>Qué decidió,<br>en qué orden</h2>
  <div class="rule"></div>
  <p style="margin-bottom:7mm">El orden importa más de lo que parece. Cada paso hizo posible el siguiente.</p>

  <div class="item"><h3>1 · Puso el horizonte por escrito</h3>
  <p>Dejó de ser algo que rondaba en la cabeza y pasó a ser una dirección concreta, contra la cual se podía contrastar cualquier decisión.</p></div>

  <div class="item"><h3>2 · Auditó su agenda</h3>
  <p>Separó qué de lo que ocupaba su semana era suyo y qué eran prioridades de otros que había ido adoptando sin decidirlo. Ese paso fue el que liberó el tiempo para todo lo que vino después.</p></div>

  <div class="item"><h3>3 · Buscó los apoyos que le faltaban</h3>
  <p>Se dio cuenta de que había profesionales que necesitaba y no estaba viendo: terapia ocupacional y kinesiología. Aprendió con ellos y después armó sus propias rutinas en la casa. Es el paso que más gente se salta, y el que hace que lo demás sea sostenible.</p></div>

  <div class="item"><h3>4 · Instaló hábitos alineados con ese horizonte</h3>
  <p>No hábitos saludables en abstracto, sino los que servían a su objetivo. La diferencia es enorme para sostenerlos: no estaba cumpliendo una recomendación ajena, se estaba preparando para algo suyo.</p></div>

  <div class="item"><h3>5 · Empezó a ordenar sus finanzas hacia ese objetivo</h3>
  <p>El dinero dejó de ser un número que había que cuidar y pasó a tener una función concreta que financiar. Sigue siendo la parte más difícil, y en la página 6 está por qué.</p></div>

  <div class="item"><h3>6 · Conversó con su familia</h3>
  <p>Puso sobre la mesa lo que venía postergando. Lo apoyaron, y aun así hubo conversaciones difíciles.</p></div>
  <div class="pgnum">4</div>
</div>

<div class="page">
  <div class="kicker">Dónde está hoy</div>
  <h2>En proceso,<br>no terminado</h2>
  <div class="rule"></div>
  <p class="lead">Carlos no llegó a la meta. Está en camino, y esa distinción importa más que cualquier cifra.</p>
  <h3>En el cuerpo</h3>
  <p>Bajó diez kilos y está aumentando su masa muscular. Esa combinación importa mucho más que el peso solo: bajar conservando fuerza es lo que preserva autonomía, y también es lo más difícil de conseguir después de los 60. Todavía no está donde quiere estar, y lo sigue trabajando.</p>
  <h3>En las finanzas</h3>
  <p>Dejó de administrar sin destino y está construyendo una estructura ordenada en función de un objetivo que él definió. Sigue en curso.</p>
  <h3>En la agenda</h3>
  <p>Es el cambio más difícil de mostrar en una foto y el más importante de todos: su semana volvió a tener cosas que él eligió.</p>
  <div class="note">
    <p>Los diez kilos son el dato más fácil de contar y el menos importante. Son consecuencia de haber tenido una razón concreta para cuidarse, no la meta. Si el objetivo hubiera sido bajar de peso, probablemente no habría durado.</p>
  </div>
  <div class="pgnum">5</div>
</div>

<div class="page">
  <div class="kicker">La parte que nadie publica</div>
  <h2>Lo que le<br>ha costado</h2>
  <div class="rule"></div>
  <p class="lead">Contar solo la parte que sale bien sería vender una historia falsa. Esto es lo que Carlos dice que le costó y le sigue costando.</p>

  <div class="item"><h3>Empezar</h3>
  <p>Cuando se le pregunta qué fue lo más difícil de todo el proceso, responde que empezar. No sostenerlo: arrancar. El primer paso concentra casi toda la resistencia, y es exactamente por eso que conviene que sea pequeño.</p></div>

  <div class="item"><h3>El dinero, y sigue costando</h3>
  <p>Es su mayor dificultad hoy. Contaba con liquidar un bien para financiar parte de su plan, y ha resultado mucho más lento y más complicado de lo que pensaba. Es un recordatorio incómodo y útil: un patrimonio que existe en el papel no es lo mismo que un patrimonio disponible cuando lo necesitas.</p></div>

  <div class="item"><h3>Las conversaciones con su familia</h3>
  <p>Lo han apoyado desde el principio. Eso no las hizo fáciles. Poner sobre la mesa la salud, el dinero y el futuro obliga a decir cosas que llevaban años sin decirse, y el apoyo no evita la incomodidad: solo hace que valga la pena atravesarla.</p></div>

  <div class="pgnum">6</div>
</div>

<div class="page">
  <div class="kicker">Lo más importante</div>
  <h2>“No quiero ser una<br>carga para mi familia”</h2>
  <div class="rule"></div>
  <p class="lead">Son sus palabras, y son el motor de todo lo demás.</p>
  <p>Es una frase que se escucha mucho en esta etapa y que normalmente se dice con culpa, como si uno estuviera pidiendo disculpas por envejecer. Vale la pena mirarla de otra manera, porque lo que Carlos hizo con ella fue convertirla en un plan.</p>
  <p>Durante los meses en que su agenda estaba llena de las urgencias de otros, él creía que eso era cuidar a los suyos. No era desorden: era una forma de estar presente. Lo que descubrió es que había una manera más eficaz de hacer exactamente lo mismo.</p>
  <div class="hl">La persona que se cuida es la que puede seguir estando.</div>
  <p>La autonomía que construyes y financias hoy es la que tu familia no va a tener que sostener mañana. Y la energía que tienes para acompañar a otros sale de algún lado: si no la repones, se acaba, y lo que queda es presencia sin capacidad.</p>
  <p><strong>No es un juego de suma cero.</strong> El tiempo que Carlos empezó a dedicarse no se lo quitó a nadie. Hizo posible todo lo demás.</p>
  <div class="pgnum">7</div>
</div>

<div class="page close">
  <div class="kicker">Para terminar</div>
  <h2>Qué es replicable<br>y qué no</h2>
  <div class="rule"></div>
  <p class="lead">El horizonte de Carlos es suyo, y su situación de salud es particular. No sirve de nada copiarlo.</p>
  <p>No venimos a decirte cómo se vive esta etapa. Es una decisión personal y es tuya. Lo que traemos es método, evidencia y estructura. <strong>Quien decide eres tú.</strong></p>
  <p>Lo replicable no es su objetivo. Es la secuencia: primero una dirección propia y concreta, después una auditoría honesta de en qué se te va la semana, después los apoyos profesionales que te faltan, después los hábitos que sostienen esa dirección, después el dinero que la financia, y al final las conversaciones que hacen que todo eso sea sostenible con tu gente.</p>
  <p>Ese orden no es casual. Casi todo el mundo intenta empezar por los hábitos o por la plata, y por eso casi todo el mundo lo abandona: sin una dirección propia, cuidarse es una obligación más en una agenda que ya está llena de obligaciones ajenas.</p>
  <p>Hay alguien más en juego: tu yo del futuro, la persona que vas a ser en diez, veinte o treinta años. Esta persona va a heredar el cuerpo, la cabeza, los vínculos y las finanzas que resulten de las acciones que tomes hoy.</p>
  <div class="principle">¿Vas a actuar por inercia<br>o con intención?</div>
""" + cta("Si te reconoces en algo de lo que le pasaba a Carlos al principio,", "pdf-entusiasmo") + """
  <div class="pgnum">8</div>
</div>
"""

open('carlos.html','w',encoding='utf-8').write(wrap(body))
open('carlos_px.html','w',encoding='utf-8').write(to_px(wrap(body)))
print("carlos OK")
