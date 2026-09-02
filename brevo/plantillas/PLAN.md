# Plantilla PLAN — guía de las cuatro acciones

> ⚠️ **Borrador mínimo, no el copy final.** Todavía no leí el contenido
> completo del PDF (`guia-PLAN-cuatro-acciones.pdf`, 8 páginas) — solo lo
> tengo como archivo adjunto, no como texto. Esto alcanza para que el envío
> funcione de punta a punta en la Etapa 5. La Etapa 6 (páginas de captura)
> es el momento de leer la guía completa y escribir un copy que realmente
> la describa, en vez de este texto genérico.

**Con adjunto**: el PDF, vía el campo `attachment.url` de Brevo apuntando a
la ruta oscura en `site/assets/pdfs/` (ver `brevo/README.md`).

## Cómo crearla en Brevo

Igual que `DOMINO.md`: **Campañas → Plantillas → Crear una plantilla**.
Esta no necesita parámetros dinámicos — el Worker igual manda
`params: {}`, así que si más adelante quieres personalizarla (por
ejemplo con el nombre de la persona) no hay que tocar el Worker, solo
agregar el parámetro ahí y en la plantilla.

Asunto sugerido:

```
Tu guía: cuatro acciones para tu jubilación
```

Anota el **Template ID** — va en `BREVO_TEMPLATE_PLAN`.

## Copy sugerido (genérico, a reemplazar en Etapa 6)

> **Aquí tienes tu guía**
>
> Hola,
>
> Adjunta va la guía que pediste. Tómate un momento para leerla con calma.
>
> Si quieres que revisemos tu caso juntos, agenda una sesión de
> diagnóstico gratuita de 45 minutos:
> **[calendly.com/margarita-disenatujubilacion/45min](https://calendly.com/margarita-disenatujubilacion/45min)**
>
> — Diseña tu Jubilación
