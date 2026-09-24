---
name: investigar-evidencia-ig
description: "Investiga qué dice la evidencia sobre un tema de salud o envejecimiento para @disenatujubilacion, la registra en la base Evidencia de Notion con su fuente, certeza y matiz, y propone las piezas que ese respaldo permite. Úsala al investigar, verificar un dato o armar un hilo temático nuevo."
---

# Investigar evidencia

Esta skill existe porque el diferencial de esta cuenta es el rigor. El público castiga la divulgación pop y premia que se nombre el nivel de evidencia, se marquen las discrepancias entre guías y se digan las extrapolaciones. **Fingir certeza uniforme destruye la confianza más rápido de lo que la construye una cifra llamativa.**

Produce dos cosas: filas en 🔬 Evidencia, y piezas en `Propuesta` que se apoyan en ellas.

## El orden importa

1. **Empieza por el material propio.** Las cápsulas del Programa en Sesiones ya afirman cosas sobre este tema. Esas son las afirmaciones que hay que respaldar primero, porque ya se las están diciendo a alumnos que pagan. Si una no se sostiene, eso es un hallazgo más valioso que cualquier dato nuevo.
2. **Luego busca, de la fuente más fuerte a la más débil**: revisiones sistemáticas y metaanálisis, guías clínicas y documentos de consenso, ensayos controlados, estudios observacionales, informes de organismos. Un artículo de prensa no es una fuente: es una pista para encontrar la fuente.
3. **Verifica la cifra contra el original**, no contra el resumen que la cita. Los números se deforman al pasar de mano en mano, y los que más circulan son los más deformados.

## Qué se registra

Una fila por afirmación, no por estudio. El título es **la frase publicable**, no el nombre del paper: "entrenar fuerza dos veces por semana mantiene la masa muscular después de los 60" y no "Efectos del entrenamiento de resistencia en adultos mayores".

Los campos que hacen el trabajo:

- **Nivel de certeza.** *Alta* es consenso o revisión sistemática. *Media* es evidencia consistente con matices importantes. *Preliminar* no se publica sin decir que es preliminar. Ante la duda, baja el nivel: es más barato ser conservador que corregir en público.
- **Matiz.** Qué **no** dice la evidencia, y dónde las guías se contradicen. Este campo es el que más se salta y el más importante — es literalmente lo que separa a esta cuenta de la divulgación que su público desprecia.
- **Cita textual.** La frase original, para que cualquiera pueda verificar sin rehacer la búsqueda.

Si un dato es llamativo pero no lo puedes confirmar contra su fuente, **déjalo fuera y dilo**. Un hueco declarado vale más que un número que después haya que retirar.

## De la evidencia a las piezas

La evidencia no se publica tal cual: alimenta el ángulo **Evidencia** de un hilo, que es uno de seis. Un hilo que solo cita estudios es tan malo como uno que solo cuenta anécdotas.

Al proponer las piezas, distribuye: el mecanismo explica, la evidencia respalda, el caso encarna. Y enlaza cada pieza a la fila de 🔬 Evidencia en la que se apoya, para que quien la guione después pueda ver el matiz sin buscarlo.

## Casos reales en redes

Cuando el encargo lo pida, busca publicaciones o videos de casos reales que valga la pena comentar. Dos cuidados:

- **Comentar no es republicar.** Instagram penaliza a las cuentas que publican mayoritariamente contenido de otros. Reaccionar a un caso, citarlo o discutirlo con criterio propio es distinto de subirlo como pieza propia — y solo lo primero sirve aquí.
- **Nunca uses a una persona identificable como ejemplo negativo.** Si el caso solo funciona señalando el error de alguien con nombre y cara, no va.

Deja los hallazgos como propuestas con su enlace en el cuerpo, para que Nicole decida si quiere entrar en esa conversación.

## Los límites, que aquí son el trabajo

- **Nada de promesas de salud.** Un hábito cambia probabilidades, no compra desenlaces. Si una frase se puede leer como "haz esto y no te pasará aquello", está mal escrita.
- **Nada de consejo clínico ni criterios diagnósticos.** No listes señales de alerta de forma que inviten a autodiagnosticarse.
- **Nada de asesoría previsional o financiera concreta**: está fuera del alcance del programa y se deriva a un aliado.
- **No conviertas un factor asociado en una causa.** Si el estudio es observacional, la afirmación tiene que sonar como observacional.

Cuando un tema te obligue a elegir entre ser preciso y ser publicable, no elijas tú: registra la evidencia con su matiz y deja la tensión como decisión en 🗳️ Decisiones y notas.

## Al terminar

Deja en la respuesta: qué afirmaciones entraron y con qué nivel de certeza, qué piezas propusiste, **qué esperabas encontrar y no encontraste**, y qué quedó como decisión. Ese tercer punto es el que más ahorra después, porque evita que alguien vuelva a buscar lo mismo dentro de tres meses.

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