---
name: proponer-ideas-ig
description: "Propone ideas de historias y reels para @disenatujubilacion y las deja en estado Propuesta en la Bandeja de Notion. Úsala cuando pidan ideas, temas o ángulos, digan que el banco está vacío, o quieran alimentar una categoría o un hilo temático."
---

# Proponer ideas

Esta skill llena la Bandeja: filas en `Estado` = `Propuesta`, sin fecha, esperando que Nicole marque Aceptar, Modificar o Descartar. No agenda y no guiona.

Una idea no es un tema. "Hablar del propósito" no es una idea; "Silvia: toda la vida me dediqué a otros" sí lo es, porque ya tiene una escena, una voz y un punto de vista, y por eso alguien puede grabarla mañana. Si lo que estás por escribir podría publicarlo cualquier cuenta de coaching, no es una idea de esta cuenta.

## Antes de proponer, mira qué falta

No propongas a ciegas. Tres consultas, en este orden:

1. **La Bandeja**: qué hay ya en `Propuesta` esperando decisión. Si hay más de diez, no agregues más — dilo y ofrece ayudar a despacharlas.
2. **Lo descartado**: filas en `Descartada` y su `Comentario`. Eso es lo que ya dijeron que no. Reproponerlo con otro título es el peor error de esta skill.
3. **Los hilos vivos**: qué `Tema` está en curso, qué `Ángulo` de la escalera le falta a cada uno, y qué hilo quedó a medias. Un hilo introducido y nunca retomado vale más que un tema nuevo.

## De dónde salen las ideas buenas

Por orden de rendimiento. Agota los primeros antes de bajar.

1. **Material real que ya existe y nadie usó.** Las 11 transcripciones de Entrevistas (~74.000 palabras), la base ✂️ Extractos, la página Testimonios, el material del programa en Sesiones, las Retros. Casi siempre hay más sin publicar de lo que ellos recuerdan.
2. **Objeciones y frases textuales.** Las documentadas: "sigo con energía, todavía no lo necesito", "ya lo resolveré cuando llegue", "esto no es para mí, me cuesta hablar en grupo", "qué se creen estos cabros chicos". Una objeción literal es el mejor gancho de esta cuenta, porque la persona se escucha a sí misma.
3. **Los mecanismos del método**, para explicar — nunca para arengar.
4. **La base 🔬 Evidencia**, cuando el hilo pide el ángulo de evidencia.
5. **Momentos de la dupla**, para los días livianos.

Si inventas desde cero es porque los cinco pozos están secos, y entonces dilo.

## Cuántas

Si no te dicen otra cosa, propón **seis a ocho**. Menos no vale una sesión de revisión; más se vuelve difícil de despachar de una sentada y termina atascando la Bandeja, que es peor que no tener ideas.

Reparte según lo que falte, no en partes iguales: mira qué categoría está flaca y qué ángulo le falta a cada hilo vivo.

## Qué lleva cada propuesta

Propiedades: `Estado` = `Propuesta`, `Origen` = `Claude`, **sin fecha**, `Categoría` siempre, y `Tema` + `Ángulo` cuando la idea pertenece a un hilo. Si no sabes qué ángulo es, probablemente la idea todavía no está lista.

Cuerpo, tres secciones y nada más:

```
### Objetivo
[Una línea: qué creencia mueve o qué muestra. No "generar engagement".]

### Ángulo
[Dos o tres líneas: por dónde entra, qué frase textual usa, qué se ve.]

### Necesita
[Qué material hace falta para poder grabarla. Si no necesita nada,
escribe "nada, se graba a cámara".]
```

Ese campo **Necesita** es lo que hace útil el banco. Una idea preciosa que depende de un video que nadie ha pedido es una idea bloqueada, y conviene que se vea desde el principio en vez de descubrirlo el día de grabar.

## La honestidad sobre la prueba

Puedes proponer ideas que dependan de material que no existe —conviene, porque es lo que empuja a pedirlo— pero **Necesita** tiene que decirlo sin rodeos: "testimonio de X en video; hoy no existe, hay que pedírselo". Nunca escribas la idea como si la prueba ya estuviera, y nunca inventes una cita para tapar el hueco. La credibilidad es lo que vende aquí.

Verifica el consentimiento antes de proponer una pieza sobre una persona, y respeta las reglas de material sensible del flujo. Si una idea es buena pero el material es sensible, propónla marcando en **Necesita** que requiere permiso puntual, y deja además una fila en 🗳️ Decisiones y notas.

## Al terminar

En tu respuesta, muestra la lista con su categoría, su hilo y su "Necesita", y señala cuáles quedaron bloqueadas. Si una categoría no se puede alimentar más sin material nuevo, dilo: eso es una decisión de Nicole, no un problema que se resuelva escribiendo más ideas.

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