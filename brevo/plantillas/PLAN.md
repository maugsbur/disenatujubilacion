# Plantilla PLAN — guía de las cuatro acciones

Se envía al dejar el correo en `/plan`. **Con adjunto**: el PDF, vía el
campo `attachment.url` de Brevo apuntando a la ruta oscura en
`site/assets/pdfs/` (ver `brevo/README.md`).

## Cómo crearla en Brevo

**Transaccional → Plantillas → Crear plantilla → Plantilla de email**
(no Campañas, esa es de marketing). Sin parámetros
dinámicos — el Worker manda `params: {}}` para esta guía, así que si más
adelante se quiere personalizar (el nombre de la persona, por ejemplo) no
hay que tocar el Worker, solo agregar el parámetro ahí y acá.

Asunto sugerido:

```
Tu guía: cuatro acciones para tu jubilación
```

Anota el **Template ID** — va en `BREVO_TEMPLATE_PLAN`.

## Copy

> **Aquí tienes tu guía**
>
> Hola,
>
> Adjunta va **Tu jubilación no se resuelve esta semana. Estas cuatro
> acciones sí.** — un número, una hora médica, una persona y una fecha.
> Cuatro cosas que se hacen una sola vez y quedan hechas, cada una con un
> primer paso de menos de cinco minutos.
>
> Elige la que te dio más incomodidad al leerla. Casi siempre es la que
> más falta hace.
>
> Si quieres que revisemos tu caso juntos, agenda una sesión de
> diagnóstico gratuita de 45 minutos:
> **[calendly.com/margarita-disenatujubilacion/45min](https://calendly.com/margarita-disenatujubilacion/45min)**
>
> — Diseña tu Jubilación
