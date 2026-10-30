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

Versión del 30/10/2026: la del equipo en Brevo, ajustada por Claude para que calce con la guía breve que va adjunta (título y lo que promete). Hay que copiarla en Brevo; si difieren, manda Brevo. El asunto y el título no cambiaron.

> **Aquí tienes tu guía**
>
> Hola,
>
> Adjunta va Cuatro acciones que puedes dejar hechas antes de jubilar: un número, una hora médica, una persona y una fecha. Cuatro cosas que se hacen una sola vez y quedan hechas, cada una con su primer paso y con cómo se ve cuando está lista.
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
