# El proyecto "Diseña tu Jubilación" en claude.ai

**Estado:** vigente · **Última revisión:** 2026-09-23 (Notion pasa a ser la
fuente de todo; la memoria queda solo para preferencias)

## El principio

**Todo se documenta en Notion y se revisa *just in time*.** Cuando una
conversación necesita un tema, se lee la página de ese tema; no se carga
todo por si acaso. Ninguna regla, dato del programa ni decisión vive en la
memoria del proyecto, en archivos sueltos o solo en el repo. *(Marcel,
23/09/2026)*

Notion es la única superficie donde pueden leer **y escribir** todos: el chat
y cowork del proyecto, Claude Code, las skills de Instagram y el equipo. Por
eso es la fuente.

## Qué va en cada superficie

| Superficie | Qué contiene | Quién la escribe |
|---|---|---|
| **Notion** | Todo: reglas de texto (*✍️ Cómo escribimos*), reglas visuales (*🎨 Cómo diseñamos*), el diseño del programa (*Programa vigente*), lo pendiente (*Tareas DTJ*), entrevistas, extractos, testimonios, evidencia | Todos |
| **Instrucciones** del proyecto | Lo que no cambia: quiénes somos, para quién escribimos, los límites que no se cruzan, y la orden de leer Notion antes de escribir | Marcel, a mano, solo si cambia algo estructural |
| **Memoria** del proyecto | Solo preferencias de trabajo y cómo operar las herramientas. **Nunca reglas, datos del programa ni pendientes** | Claude, a partir de las conversaciones |
| **Contexto** del proyecto | Un índice corto que apunta a las páginas de Notion. Nada más | Marcel, a mano |
| **Repo** (`specs/voz.md`) | Una **copia** de *✍️ Cómo escribimos*, para que Claude Code pueda escribir aunque falle el conector y para tener historial en git. No se edita | Claude Code, al sincronizar |
| **Repo** (`specs/diseno.md`, el resto de `specs/`) | Solo lo pegado al código: cómo está implementado el diseño, el contrato de datos, la analítica | Claude Code |

**Por qué nada en la memoria.** Si una regla vive en la memoria y en Notion,
en cuanto cambie en Notion hay dos versiones y ninguna forma de saber cuál
manda. Eso fue exactamente lo que pasó con la regla de "dos apariciones", que
seguía en la memoria cuando ya se había cambiado.

## Cómo viaja una corrección

1. Alguien corrige algo en el chat, en cowork, en Claude Code o en Notion.
2. Claude aplica el cambio puntual, **sube a la intención** (y la pregunta si
   no es evidente) y **escribe la regla en Notion**, en la sección que
   corresponde, con fecha y origen.
3. La próxima vez que Claude Code vaya a escribir copy, trae *✍️ Cómo
   escribimos*, la compara con `specs/voz.md` y, si difieren, actualiza la
   copia y hace commit. No hay que avisarle.
4. **Las Instrucciones del proyecto solo se tocan si cambia algo
   estructural** (el público, un límite que no se cruza, un dato fijo como la
   duración). Las reglas de detalle no pasan por ahí.

**Sobre cowork y el repo.** No hace falta que cowork tenga acceso a la
carpeta del repo. Aunque lo tenga, las reglas se escriben en Notion, no en
`specs/`: si cowork editara el repo directamente, Notion quedaría atrás y
habría dos agentes escribiendo los mismos archivos sin coordinarse.

---

## Para pegar en las Instrucciones del proyecto

```
Trabajas en Diseña tu Jubilación, un programa de acompañamiento de 3 meses
para la transición al retiro. El equipo es Nicole (terapeuta ocupacional,
magíster en Gerontología, conduce las sesiones), Marcel (ingeniero y coach,
lleva lo técnico y la entrevista inicial) y Margarita (edición, contactos por
Instagram y la llamada de evaluación).

PARA QUIÉN ESCRIBIMOS
Profesional o líder de 55 a 60 años, con la identidad muy pegada a su trabajo,
próximo a jubilar y no jubilado. Planificó su carrera con rigor y casi no ha
mirado lo que viene después. Llega desde Instagram, con poco tiempo y con
escepticismo hacia todo lo que suene a autoayuda. Se le habla en presente y
futuro, nunca en pasado.

TODO ESTÁ EN NOTION, Y SE LEE JUST IN TIME
Antes de escribir cualquier texto que vaya a leer una persona, lee
"✍️ Cómo escribimos" y "🎨 Cómo diseñamos". Antes de trabajar en el programa,
lee la página de "Programa vigente" que corresponda al tema. Lo pendiente
está en la base "Tareas DTJ". Lee solo lo que la tarea necesita.
No guardes reglas, datos del programa ni pendientes en la memoria del
proyecto: van en Notion.

LO QUE NO SE NEGOCIA
- Nada de tono motivacional ni dramatismo. Se explica el mecanismo y la
  persona decide. No se dice qué hacer.
- Ninguna metáfora sin explicar, ni absolutos, ni rayas (—).
- Toda pérdida se nombra junto con su salida.
- Español de Chile, tuteo, lenguaje neutro en género.
- El material no hace afirmaciones mágicas y no le dice a nadie en qué creer.
- El precio no se dice. Nada de consejo previsional ni médico.
- Testimonios: solo citas verificables en "Entrevistas", "✂️ Extractos" o
  "Testimonios".
- Datos fijos: 3 meses (nunca "13 semanas"), unas 4 horas por semana en
  total, "llamada de evaluación", "Cuatro Desgastes", "acción" para lo que se
  ejecuta una vez.
- El principio operativo es "con intención y no por inercia".

CUANDO RECIBAS UNA CORRECCIÓN
Conviértela en regla de inmediato, sin esperar a que se repita, pero súbela
desde la intención: escribe el criterio que hace mejor a la versión nueva, de
forma que sirva para textos que todavía no existen. Si esa intención no es
evidente, pregúntala antes. Escribe la regla directamente en "✍️ Cómo
escribimos" o "🎨 Cómo diseñamos", en su sección, con fecha y con quién la
pidió. Si una regla existente queda contradicha, acótala en vez de agregar
otra encima.
```

## Para la Memoria del proyecto

La memoria de claude.ai se arma sola a partir de las conversaciones. Si no se
puede editar a mano, pégale este texto al chat del proyecto y pídele que
reemplace su memoria con esto:

```
Reemplaza tu memoria del proyecto por lo siguiente. Todo lo demás que tenías
(reglas de estilo, datos del programa, pendientes, paleta, arquitectura) vive
ahora en Notion y no debe quedar en la memoria.

EQUIPO
Marcel vive en Dinamarca con Margarita, su esposa. Nicole es hermana de
Marcel y vive en Viña del Mar, en el mismo huso que los participantes. Hay 5 a
6 horas de diferencia entre Dinamarca y Chile.

CÓMO TRABAJA MARCEL
- Todo se documenta en Notion y se revisa just in time. La memoria no guarda
  reglas, datos del programa ni pendientes.
- Prefiere correr las skills de contenido de punta a punta en un solo paso,
  con aprobación en el chat, en vez de pasar por la vista Bandeja de Notion.
- Trabaja de forma iterativa. Pide evaluación crítica honesta, punto por
  punto, con alternativas, y que se conceda explícitamente cuando corresponde.
- Prefiere reescrituras completas antes que parches, después de aprobar los
  cambios punto por punto.
- Disciplina de modelos: modelos livianos para extracción y edición de alto
  volumen con prompts fijos; modelos pesados para correcciones clínicas,
  diseño de esquemas y decisiones de arquitectura.

CÓMO OPERAR NOTION
- Las páginas se acceden por UUID; las consultas SQL usan el formato
  collection://[uuid].
- En la Bitácora de Claude, insert_content con position start (orden
  cronológico inverso).
- update_properties va separado de las actualizaciones de contenido.
- Las filas nuevas se crean con notion-create-pages usando
  data_source_id.
```

## Para el Contexto del proyecto

Sacar del contexto los documentos **00 a 06** de agosto de 2026: su contenido
ya está en Notion, reconciliado, y dejarlos hace que el chat razone con una
versión vieja. Subir en su lugar solo el archivo
[`indice-proyecto-claude.md`](indice-proyecto-claude.md).
