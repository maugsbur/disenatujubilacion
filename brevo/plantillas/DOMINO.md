# Plantilla DOMINÓ — resultado del autodiagnóstico

Se envía automáticamente al terminar las 25 preguntas en `/autodiagnostico`.
El copy de las cinco plantillas de esta carpeta se revisó con las reglas de
✍️ Cómo escribimos el 2026-09-24 (sin rayas, "llamada de evaluación",
títulos iguales a los de las guías breves).

**Sin adjunto.** El resultado completo (efecto dominó, perfiles, gráfico)
ya lo vio la persona en el sitio; este correo es el respaldo por escrito
que pidió, con los cinco números — la decisión de Marcel del 2026-09-02.

## Cómo crearla en Brevo

**Transaccional → Plantillas → Crear plantilla → Plantilla de email**
(editor de arrastrar y soltar o HTML, como prefiera Margarita) — no la
sección de Campañas, esa es para marketing y no expone el `templateId`
que necesita la API que usa el Worker. Asunto sugerido:

```
Tu resultado: los 5 pilares de tu jubilación
```

Inserta estos parámetros donde corresponda con la sintaxis de Brevo
(`{{params.NOMBRE}}` — confirmar que sigue siendo así en el editor al
momento de armarla, por si Brevo la cambia):

| Parámetro | Contiene |
|---|---|
| `{{params.proposito}}` | Total del pilar Propósito, 5 a 25 |
| `{{params.fisico}}` | Total del pilar Físico, 5 a 25 |
| `{{params.mental}}` | Total del pilar Mental, 5 a 25 |
| `{{params.social}}` | Total del pilar Social, 5 a 25 |
| `{{params.finanzas}}` | Total del pilar Finanzas, 5 a 25 |
| `{{params.pilarMasBajo}}` | Nombre del pilar más bajo, ya calculado (p.ej. "Social") |

Anota el **Template ID** que Brevo le asigna al guardar — va en la variable
de entorno `BREVO_TEMPLATE_DOMINO` del Worker (ver `brevo/README.md`).

## Copy sugerido

> **Tu resultado: los 5 pilares de tu jubilación**
>
> Hola,
>
> Este es el resultado de tu autodiagnóstico, para que lo tengas por
> escrito.
>
> | Pilar | Tu puntaje |
> |---|---|
> | Propósito | {{params.proposito}} / 25 |
> | Físico | {{params.fisico}} / 25 |
> | Mental y Cognitivo | {{params.mental}} / 25 |
> | Social | {{params.social}} / 25 |
> | Finanzas | {{params.finanzas}} / 25 |
>
> Tu pilar más bajo es **{{params.pilarMasBajo}}**. No es un diagnóstico ni
> un juicio: es el pilar donde, según lo que respondiste, una acción
> concreta puede rendir más. Y como los pilares dependen unos de otros,
> cuando uno se debilita empuja hacia abajo a los demás.
>
> Si quieres que revisemos tu caso en conversación, agenda una llamada de
> evaluación gratuita de 45 minutos con Margarita, que coordina el programa:
> **[calendly.com/margarita-disenatujubilacion/45min](https://calendly.com/margarita-disenatujubilacion/45min)**
>
> Diseña tu Jubilación
>
> *Este es un ejercicio de orientación personal, no un instrumento clínico
> ni un diagnóstico de ningún tipo.*

## Nota de cumplimiento

Este correo se envía por haber completado el autodiagnóstico — es la
Finalidad 1 de `08-cumplimiento-datos.md` (necesaria para prestar el
servicio pedido), así que sale **siempre**, sin importar qué casillas
marcó la persona. No incluyas las 25 respuestas crudas en el cuerpo,
solo los cinco totales — ya lo exige `08-cumplimiento-datos.md` §6.
