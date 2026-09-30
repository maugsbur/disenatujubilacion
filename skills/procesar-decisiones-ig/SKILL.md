---
name: procesar-decisiones-ig
description: "Ejecuta en Notion lo que el equipo decidió sobre las propuestas de contenido de @disenatujubilacion (Aceptar, Modificar, Descartar) y convierte cada corrección en regla de ✍️ Cómo escribimos o 🎨 Cómo diseñamos, desde su intención. Úsala cuando digan que revisaron la bandeja o dejaron comentarios, o cuando den feedback general sobre el tono."
---

# Procesar decisiones

**Produce** dos cosas que son la misma: ejecuta lo que el equipo decidió sobre cada propuesta, y se queda con lo que esa decisión enseña, como regla escrita. Lo segundo es lo que hace que el sistema mejore: cada "esto suena vendedor" es información sobre cómo escribimos que, si no se escribe, se pierde.

## Antes de empezar, lee

- 🤝 [Flujo de trabajo con Claude](https://app.notion.com/p/3e523cb6e7af81b688daf2553a0f3ed3) › *Lo común a las skills de Instagram*.
- ✍️ [Cómo escribimos](https://app.notion.com/p/3d423cb6e7af818f85a6d216c1b6a459), completa, incluido el párrafo inicial que explica cómo se escribe una regla. Si la corrección es visual, 🎨 [Cómo diseñamos](https://app.notion.com/p/3d523cb6e7af81f9a703eb234cce4a22).

## Pasos

1. **Las piezas decididas.** En los dos calendarios, las filas con `Decisión` puesta:
   - **Aceptar** → `Estado` = `Idea`, `Decisión` vacía. Entra al banco.
   - **Modificar** → reescríbela según el `Comentario`, deja `Estado` = `Propuesta` y `Decisión` vacía. Conserva el comentario en el cuerpo, bajo un encabezado con la fecha.
   - **Descartar** → `Estado` = `Descartada`.
2. **El feedback que no es sobre una pieza** llega en el chat, como comentario en una tarjeta o como tarea nueva. Si es de estilo o diseño, va al paso 3. Si es de dirección (qué se propone, cómo se planifica), aplícalo y escríbelo donde vive esa regla (🎬).
3. **Convierte cada corrección en regla, de inmediato:**
   - Escribe **la intención**, no el cambio puntual, para que sirva en textos que todavía no existen. "No usar 'empoderar'" es débil; "preferimos verbos concretos sobre abstracciones de coaching" se aplica a palabras que nadie mencionó.
   - **Si la intención no es evidente, pregúntala antes**, en la tarjeta o en el chat. Una regla mal generalizada hace más daño que no tenerla.
   - Cada regla con fecha, quién la pidió y de qué pieza salió.
   - **Si contradice una regla existente, acota la existente** con el caso, en vez de agregar otra encima.
   - Si la corrección se entiende mejor con el ejemplo real, súmala a *Antes y después*.
   - Varias correcciones sobre lo mismo son una sola regla.
4. **Sincroniza** `specs/voz.md` si trabajas en Claude Code.

## Lo que no se hace

- No decidas tú lo que quedó sin decidir: una fila en `Propuesta` sin `Decisión` sigue esperando a una persona.
- No subas nada más allá de `Idea`: aceptar no es agendar ni guionar.
- No cambies *Principios* ni *Límites* de ✍️ por inferencia: son acuerdos del equipo; si una corrección parece tocarlos, pregunta.

## Terminada cuando

- [ ] Ninguna fila con `Decisión` puesta quedó sin procesar.
- [ ] Cada corrección quedó como regla (o como pregunta, si la intención no era clara).

## Entrega

En la tarjeta y en tu respuesta, tres líneas: cuántas se aceptaron, modificaron y descartaron; qué reglas entraron y de qué correcciones salieron; y qué sigue esperando decisión.
