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

Cuando un tema te obligue a elegir entre ser preciso y ser publicable, no elijas tú: registra la evidencia con su matiz y deja la tensión como pregunta para el equipo en la tarjeta de la tarea.

## Al terminar

Deja en la respuesta: qué afirmaciones entraron y con qué nivel de certeza, qué piezas propusiste, **qué esperabas encontrar y no encontraste**, y qué quedó como decisión. Ese tercer punto es el que más ahorra después, porque evita que alguien vuelva a buscar lo mismo dentro de tres meses.

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
