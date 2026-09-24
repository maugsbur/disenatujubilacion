---
name: procesar-decisiones-ig
description: "Ejecuta en Notion lo que decidieron sobre las propuestas de contenido de @disenatujubilacion y destila las correcciones repetidas en la página \"Cómo escribimos\". Úsala cuando digan que revisaron la bandeja o dejaron comentarios, o cuando den feedback general sobre el tono."
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

## 2. Las notas que no son sobre una pieza

En 🗳️ Decisiones y notas, las filas `Abierta`:

- **Nota de estilo** → aplícala y trátala como candidata a regla.
- **Nota de dirección** → afecta qué se propone y cómo se planifica ("bajemos finanzas un mes", "más casos"). Aplícala y márcala `Aplicada por Claude`.
- **Decisión pendiente** y **Bloqueo** → si está `Resuelta` y no aplicada, aplica lo resuelto y marca el checkbox. Si sigue abierta, no la fuerces: repórtala.

Si Nicole te da feedback general hablando contigo en vez de en Notion, **regístralo tú** como fila nueva con su `Tipo` y `Origen`. No debería tener que abrir Notion para decirte que algo suena mal.

## 3. Destilar el lenguaje

Aquí está el cuidado. La página ✍️ Cómo escribimos solo sirve si tiene reglas verdaderas; si se llena de correcciones puntuales, deja de leerse y el mecanismo muere.

Tres candados:

- **Una corrección puntual no es una regla.** Anótala solo cuando el mismo tipo de corrección aparezca **dos veces**, en piezas distintas. Hasta entonces, la corrección vive en el `Comentario` de su fila y nada más.
- **Cada regla dice de dónde salió**, con la fecha y las piezas que la originaron, para poder revertirla si resultó ser un caso y no un patrón.
- **La regla se escribe como criterio, no como prohibición suelta.** "No usar 'empoderar'" es débil; "preferimos verbos concretos sobre abstracciones de coaching: 'decidir' antes que 'empoderar'" se puede aplicar a palabras que nadie mencionó todavía.

Escribe en las tres secciones según corresponda: *Reglas aprendidas*, *Palabras* (la tabla usamos/no usamos), y *Antes y después* cuando la corrección se entiende mejor con el ejemplo real que con la explicación.

**Nunca edites las Reglas de base** sin que te lo pidan explícitamente: son el acuerdo del equipo, no algo que se infiera de un comentario.

## Qué no hacer

No decidas tú lo que quedó sin decidir. Una fila en `Propuesta` sin `Decisión` sigue esperando a una persona, aunque lleve semanas y aunque te parezca obvia — si molesta que se acumulen, dilo, no la resuelvas.

No subas nada más allá de `Idea`. Aceptar una propuesta no es agendarla ni guionarla.

## Al terminar

Reporta en tres líneas: cuántas se aceptaron, modificaron y descartaron; qué reglas nuevas entraron a Cómo escribimos y de qué correcciones salieron; y qué sigue esperando decisión. Deja la entrada en la Bitácora.

Si en una tanda hay muchas modificaciones sobre lo mismo, dilo aunque no llegue a ser regla todavía: dos correcciones parecidas son un patrón naciendo, y a veces Nicole prefiere nombrarlo ella.

## Antes de nada, lee el flujo

El circuito completo, las reglas de voz y las de uso del material de personas viven en Notion y se mantienen ahí, no en esta skill. Léelas siempre antes de actuar:

- **🔁 Flujo de contenido con Claude** — https://app.notion.com/p/3d123cb6e7af81da9b53ee254469225e
- **✍️ Cómo escribimos** — https://app.notion.com/p/3d423cb6e7af818f85a6d216c1b6a459 (obligatoria si vas a redactar)
- **📓 Bitácora de Claude** — https://app.notion.com/p/3d423cb6e7af812e8be5c693db97deb0 (las últimas entradas, para saber dónde quedaste)

Si algo de esta skill contradice esas páginas, ganan ellas. La skill es el procedimiento; Notion es el estado, y cambia.

Carga las herramientas primero:
`ToolSearch` con `select:mcp__Notion__notion-search,mcp__Notion__notion-fetch,mcp__Notion__notion-query-data-sources,mcp__Notion__notion-update-page,mcp__Notion__notion-create-pages`

Bases (el modo SQL está topado en este workspace — usa `rows` o `view`):

| Base | Data source |
|---|---|
| 📸 Calendario de historias | `collection://b2323cb6-e7af-829f-9594-87552d04c5db` |
| 📸 Calendario de contenido | `collection://df323cb6-e7af-8277-ba21-87bd09a11fd7` |
| 🗳️ Decisiones y notas | `collection://57e0fe61-5ec6-480c-8cb6-cd8de0899542` |
| 🔬 Evidencia | `collection://92f7ff97-94e7-49c8-8596-208d634f6587` |
| ✂️ Extractos | `collection://e7abbe2d-4afe-44ee-bbe8-ee23a4236623` |

Los nombres de las opciones de `Categoría` en historias llevan espacios dobles y comillas tipográficas; cópialos tal cual o la escritura falla.

## Dónde va cada salida

Esta skill la puede correr una persona en una conversación, o la revisión automática de las 4:00 de la mañana, donde no hay nadie leyendo y la conversación no queda guardada en ninguna parte. Por eso:

- **Todo lo que deba sobrevivir va a Notion**: el trabajo, a la fila de su pieza; lo que quedó pendiente o necesita una decisión, a 🗳️ Decisiones y notas; y el resumen de la corrida, a 📓 la Bitácora.
- **Tu respuesta final es solo el resumen de lo que ya quedó escrito.** Nunca dejes ahí algo que no esté también en Notion: si la corrida fue automática, ese texto no lo lee nadie.

Cuando arriba diga "dilo" o "repórtalo", significa las dos cosas: dejarlo en Notion donde corresponda, y resumirlo en la respuesta.