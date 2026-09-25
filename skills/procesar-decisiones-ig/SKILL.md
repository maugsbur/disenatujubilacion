---
name: procesar-decisiones-ig
description: "Ejecuta en Notion lo que decidieron sobre las propuestas de contenido de @disenatujubilacion y convierte cada corrección en regla de \"Cómo escribimos\" desde su intención. Úsala cuando digan que revisaron la bandeja o dejaron comentarios, o cuando den feedback general sobre el tono."
---

# Procesar decisiones y aprender el lenguaje

Esta skill hace dos cosas que parecen distintas y son la misma: ejecutar lo que decidieron, y quedarse con lo que esa decisión enseña.

Lo segundo es lo que hace que el sistema mejore. Cada vez que alguien escribe "esto suena vendedor" o "el gancho está muy largo", ahí hay información sobre cómo escriben ellos que hoy se perdería. Recogerla es el trabajo, no un extra.

## 1. Las piezas decididas

En ambos calendarios, busca las filas con `Decisión` puesta. Para cada una:

- **Aceptar** → `Estado` pasa a `Idea`, y deja `Decisión` vacía. La idea entra al banco.
- **Modificar** → reescribe la propuesta según el `Comentario`, deja el `Estado` en `Propuesta` y `Decisión` vacía, para que vuelva a pasar por sus ojos. Conserva el comentario original en el cuerpo, bajo un encabezado que diga de cuándo es: la próxima revisión necesita ver qué se pidió.
- **Descartar** → `Estado` pasa a `Descartada`. **Y no vuelvas a proponer nada equivalente**: lo descartado con su comentario es parte de lo que hay que leer antes de proponer.

Reescribir según un comentario es más que obedecerlo al pie. Si dicen "muy largo", acorta; pero si el comentario apunta a algo que también pasa en otras piezas, eso es una regla, no un arreglo puntual — sigue leyendo.

## 2. El feedback que no es sobre una pieza

🗳️ Decisiones y notas está congelada: ya no llegan notas por ahí. El feedback general llega de tres formas, y las tres se tratan igual:

- **En una conversación** ("esto suena vendedor", "bajemos finanzas un mes").
- **Como comentario o respuesta en una tarjeta** de Tareas DTJ.
- **Como tarea nueva** en turno Claude.

Si es sobre cómo se escribe o cómo se ve, pasa a la sección 3. Si es de dirección (qué se propone, cómo se planifica), aplícalo y déjalo escrito donde viva esa regla (🎬 Cómo creamos contenido o la descripción del calendario). Nadie debería tener que abrir Notion para decirte que algo suena mal: si te lo dicen en el chat, lo escribes tú.

## 3. Convertir la corrección en regla

La página ✍️ Cómo escribimos solo sirve si sus reglas son verdaderas y generales. Desde el 23/09/2026 **una corrección se convierte en regla de inmediato**, sin esperar a que se repita. Lo que cuida que no se llene de ruido es cómo se escribe:

- **Se escribe la intención, no el cambio puntual.** Pregúntate qué criterio hace mejor a la versión nueva, y redáctalo para que sirva en textos que todavía no existen. "No usar 'empoderar'" es débil; "preferimos verbos concretos sobre abstracciones de coaching: 'decidir' antes que 'empoderar'" se aplica a palabras que nadie mencionó.
- **Si la intención no es evidente, pregúntala antes** de escribir la regla, en la tarjeta o en el chat. Una regla mal generalizada se aplica donde no correspondía, y hace más daño que no tenerla.
- **Cada regla dice de dónde salió**, con la fecha, quién la pidió y la pieza, para poder revertirla.
- **Si contradice una regla existente, acota la existente** con el caso que la desmintió, en vez de agregar otra encima. Acotar una regla demasiado amplia es parte del mecanismo, no una falla.

Escribe en la sección que corresponda (Principios, Reglas de escritura, Palabras, Límites) y en *Antes y después* cuando la corrección se entiende mejor con el ejemplo real. Si la corrección es visual, va a 🎨 Cómo diseñamos con el mismo criterio.

**No cambies Principios ni Límites por inferencia**: son acuerdos del equipo. Si una corrección parece tocarlos, pregunta.

## Qué no hacer

No decidas tú lo que quedó sin decidir. Una fila en `Propuesta` sin `Decisión` sigue esperando a una persona, aunque lleve semanas y aunque te parezca obvia — si molesta que se acumulen, dilo, no la resuelvas.

No subas nada más allá de `Idea`. Aceptar una propuesta no es agendarla ni guionarla.

## Al terminar

Reporta en tres líneas: cuántas se aceptaron, modificaron y descartaron; qué reglas nuevas entraron a Cómo escribimos y de qué correcciones salieron; y qué sigue esperando decisión. Déjalo en la tarjeta de la tarea, si la hay.

Si una tanda trae varias correcciones sobre lo mismo, escribe una sola regla que las cubra, no una por pieza.

## Antes de nada, lee el flujo

El flujo de trabajo, las reglas de voz y las de uso del material de personas viven en Notion y se mantienen ahí, no en esta skill. Léelas antes de actuar:

- **🤝 Flujo de trabajo con Claude** — https://app.notion.com/p/3e523cb6e7af81b688daf2553a0f3ed3 (el flujo principal: Tareas DTJ y la columna Turno)
- **✍️ Cómo escribimos** — https://app.notion.com/p/3d423cb6e7af818f85a6d216c1b6a459 (obligatoria si vas a redactar)
- **🎬 Cómo creamos contenido** — https://app.notion.com/p/3e423cb6e7af8115b736d70bf97608c1 (de dónde salen las ideas, niveles de conciencia, filtro antes de producir)
- **🔁 Flujo de contenido con Claude** (deprecado) — https://app.notion.com/p/3d123cb6e7af81da9b53ee254469225e. Sirve solo como referencia del circuito de ideas, el mapeo de días, la recurrencia temática y las reglas de material de personas.

Si algo de esta skill contradice esas páginas, ganan ellas. La skill es el procedimiento; Notion es el estado, y cambia.

Carga las herramientas primero:
`ToolSearch` con `select:mcp__Notion__notion-search,mcp__Notion__notion-fetch,mcp__Notion__notion-query-data-sources,mcp__Notion__notion-update-page,mcp__Notion__notion-create-pages`

Bases (el modo SQL está topado en este workspace — usa `rows` o `view`):

| Base | Data source |
|---|---|
| ✅ Tareas DTJ | `collection://3e423cb6-e7af-80a9-b248-000ba52f0ba7` |
| 📸 Calendario de historias | `collection://b2323cb6-e7af-829f-9594-87552d04c5db` |
| 📸 Calendario de contenido | `collection://df323cb6-e7af-8277-ba21-87bd09a11fd7` |
| 🔬 Evidencia | `collection://92f7ff97-94e7-49c8-8596-208d634f6587` |
| ✂️ Extractos | `collection://e7abbe2d-4afe-44ee-bbe8-ee23a4236623` |

🗳️ Decisiones y notas quedó **congelada el 24/09/2026**: se puede leer como registro de lo decidido, pero no se escribe ahí. La 📓 Bitácora de Claude tampoco se usa para trabajo nuevo.

Los nombres de las opciones de `Categoría` en historias llevan espacios dobles y comillas tipográficas; cópialos tal cual o la escritura falla.

## Dónde va cada salida

Esta skill se corre a pedido, en una conversación o dentro de una tarea de Tareas DTJ. No hay revisión automática.

- **El trabajo va a la fila de su pieza**, en el calendario que corresponda.
- **El avance y lo pendiente van a la tarjeta de la tarea** en Tareas DTJ: una sección **Avance** con qué hiciste y la fecha, y **Preguntas de Claude** numeradas, cada una con lo que harías por defecto. Si quedan preguntas o el resultado necesita visto bueno, el `Turno` pasa a *Espera al equipo*. Si no hay tarjeta, créala.
- **Tu respuesta final es el resumen de lo que ya quedó escrito** en Notion, no un lugar para dejar cosas que no estén allá.

Cuando arriba diga "dilo" o "repórtalo", significa las dos cosas: dejarlo en la tarjeta y resumirlo en la respuesta.
