# Plantilla PILARES — los cinco pilares y el efecto dominó

Se envía al dejar el correo en `/pilares`. **Con adjunto**: el PDF **breve** (2 páginas), vía el
campo `attachment.url` de Brevo apuntando a la ruta oscura en
`site/assets/pdfs/` (ver `brevo/README.md`).

Es la versión de lectura del autodiagnóstico, para quien recién llega al
perfil de Instagram y no va a hacer las 25 preguntas. El PDF termina
invitando al autodiagnóstico online y a la llamada de evaluación.

## Cómo crearla en Brevo

**Transaccional → Plantillas → Crear plantilla → Plantilla de email**.
Sin parámetros dinámicos. Anota el **Template ID** y agrégalo en
`wrangler.toml` como `BREVO_TEMPLATE_PILARES = "<id>"`.

**Mientras esa variable no exista, el correo no sale**: el Worker responde
`config_correo_incompleta` y la persona queda guardada sin guía. No enlazar
`/pilares` desde Instagram antes de eso.

Asunto sugerido:

```
Tu guía: los cinco pilares de tu jubilación
```

## Copy

> **Aquí tienes tu guía**
>
> Hola,
>
> Adjunta va **Tu jubilación se juega en cinco pilares. Y ninguno cae
> solo.** Qué es cada pilar, las señales de que uno está bajo, cómo se
> arrastran entre sí y un ejercicio de dos minutos para encontrar el tuyo
> más débil.
>
> Si quieres el dato completo, el autodiagnóstico online toma doce minutos:
> **[disenatujubilacion.com/autodiagnostico](https://disenatujubilacion.com/autodiagnostico?utm_source=correo-pilares)**
>
> Y si prefieres revisarlo en conversación, agenda una llamada de
> evaluación gratuita de 45 minutos con Margarita, que coordina el programa:
> **[calendly.com/margarita-disenatujubilacion/45min](https://calendly.com/margarita-disenatujubilacion/45min?utm_source=correo-pilares)**
>
> Diseña tu Jubilación

## La versión completa

El correo lleva solo la versión breve. La guía completa de 8 páginas no se
enlaza en ninguna parte: la manda Margarita a quien sigue la conversación y
pide más. Las URLs están en `brevo/README.md` § 4.
