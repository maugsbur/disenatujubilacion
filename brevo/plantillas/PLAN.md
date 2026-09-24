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

> **Aquí tienes tu guía**
>
> Hola,
>
> Adjunta va **Cuatro acciones que puedes dejar hechas antes de jubilar**:
> un número, una hora médica, una persona y una fecha. Cada una se hace una
> sola vez y queda hecha, y la guía dice cómo se ve cuando lo está.
>
> Elige la que te dio más incomodidad al leerla. Suele ser la que más
> falta hace.
>
> Si quieres que revisemos tu caso en conversación, agenda una llamada de
> evaluación gratuita de 45 minutos con Margarita, que coordina el programa:
> **[calendly.com/margarita-disenatujubilacion/45min](https://calendly.com/margarita-disenatujubilacion/45min)**
>
> Diseña tu Jubilación

## La versión completa

El correo lleva solo la versión breve. La guía completa de 8 páginas no se
enlaza en ninguna parte: la manda Margarita a quien sigue la conversación y
pide más. Las URLs están en `brevo/README.md` § 4.
