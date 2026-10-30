# Plantilla PLAN — guía de las cuatro acciones

Se envía al dejar el correo en `/plan`. **Con adjunto**: el PDF **breve** (2 páginas), vía el
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

Igual al de Brevo al 30/10/2026 (lo cambió el equipo directo en Brevo; Brevo manda si difieren). El asunto y el título no cambiaron.

> **Aquí tienes tu guía**
>
> Hola,
>
> Adjunta va Tu jubilación no se resuelve esta semana. Estas cuatro acciones sí. Un número, una hora médica, una persona y una fecha. Cuatro cosas que se hacen una sola vez y quedan hechas, cada una con un primer paso de menos de cinco minutos.
>
> Elige la que te dio más incomodidad al leerla. Casi siempre es la que más falta hace.
>
> Si quieres que revisemos tu caso juntos, agenda una llamada de evaluación de cortesía de 45 minutos con Margarita, quien coordina el programa:
> https://calendly.com/margarita-disenatujubilacion/45min
>
> --
> Diseña tu Jubilación

## La versión completa

El correo lleva solo la versión breve. La guía completa de 8 páginas no se
enlaza en ninguna parte: la manda Margarita a quien sigue la conversación y
pide más. Las URLs están en `brevo/README.md` § 4.
