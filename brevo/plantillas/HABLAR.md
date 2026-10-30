# Plantilla HABLAR — guía de conversaciones

Se envía al dejar el correo en `/hablar`. **Con adjunto**: el PDF **breve** (2 páginas), vía el
campo `attachment.url` de Brevo apuntando a la ruta oscura en
`site/assets/pdfs/` (ver `brevo/README.md`).

## Cómo crearla en Brevo

**Transaccional → Plantillas → Crear plantilla → Plantilla de email**
(no Campañas, esa es de marketing). Sin parámetros dinámicos.

Asunto sugerido:

```
Tu guía: cómo hablar de tu jubilación
```

Anota el **Template ID** — va en `BREVO_TEMPLATE_HABLAR`.

## Copy

Versión del 30/10/2026: la del equipo en Brevo, ajustada por Claude para que calce con la guía breve que va adjunta (título y lo que promete). Hay que copiarla en Brevo; si difieren, manda Brevo. El asunto y el título no cambiaron.

> **Aquí tienes tu guía**
>
> Hola,
>
> Adjunta va Las cuatro conversaciones que conviene tener antes de jubilar: cuidados, dónde y cómo vivir, dinero, y qué pasa con tus bienes. Para cada una, la pregunta que debería dejar respondida, y una estructura para proponerla sin que suene a reproche ni a anuncio, con un ejemplo.
>
> Empieza por una sola. La que menos ganas te dé tener suele ser la más importante.
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
