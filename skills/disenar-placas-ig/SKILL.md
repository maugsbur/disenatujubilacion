---
name: disenar-placas-ig
description: "Genera las placas de @disenatujubilacion como PNG con la identidad de marca (1080×1920 historias, 1080×1350 carrusel) a partir de un guion ya aprobado en Notion. Úsala cuando pidan las placas, las imágenes o el diseño de una pieza."
---

# Diseñar las placas

**Produce** las placas PNG de un guion **ya escrito y aprobado**, listas para revisar. **No** escribe el guion (eso es `escribir-guion-ig`) ni decide qué dice.

Cada bloque **Placa N** del guion es una placa, y la línea de fondo que lo acompaña ("foto de Carlos a sangre completa", "placa sobria con el dato grande") dice qué tipo usar.

## Antes de empezar, lee

- 🤝 [Flujo de trabajo con Claude](https://app.notion.com/p/3e523cb6e7af81b688daf2553a0f3ed3) › *Lo común a las skills de Instagram*.
- 🎨 [Cómo diseñamos](https://app.notion.com/p/3d523cb6e7af81f9a703eb234cce4a22), completa: colores y su uso, legibilidad, qué fondos se usan y cuándo se rompe la secuencia, zonas seguras, y *Dónde se revisan*. Esa página manda sobre esta skill y sobre `render.py`.
- ✍️ [Cómo escribimos](https://app.notion.com/p/3d423cb6e7af818f85a6d216c1b6a459), por si al pasar a placa hay que ajustar una palabra.

## Pasos

1. **Lee el guion** en la fila de la pieza. Si una placa pide una foto que no existe, no la renderices vacía: dilo. Una placa de texto donde debía ir una cara es un problema de producción, no un detalle.
2. **Arma la entrada** (`entrada.json`), una placa por bloque del guion, con la composición de 🎨 (un fondo base, uno o dos quiebres, el CTA vuelve al fondo base):

```json
{"formato": "historia",
 "placas": [
  {"tipo":"texto","fondo":"verde","contexto":"Una frase que escuchamos mucho",
   "principal":"«Sigo con energía. Todavía no lo necesito.»","pie":"Diseña tu Jubilación"},
  {"tipo":"dato","fondo":"claro","numero":"12 de 13",
   "principal":"personas del piloto reportaron mejoras.","pie":"Piloto 2026"},
  {"tipo":"cita","fondo":"verde","principal":"La vejez te pilla desprevenido.",
   "autor":"Carlos","rol":"Participante del programa piloto"},
  {"tipo":"cta","fondo":"verde","contexto":"Si quieres empezar por algún lado",
   "principal":"Comenta","palabra":"PALABRA","matiz":"y te mando el recurso."}
]}
```

   `tipo`: `texto`, `dato`, `cita` o `cta`. `formato`: `historia` o `carrusel`. `imagen` acepta una ruta local o un data URI y pone la foto de fondo con un velo. La palabra del CTA sale de 🧲 Lead Magnets › *Palabras de CTA vigentes*; nunca una inventada.
3. **Renderiza** con `render.py` (en los archivos de esta skill; necesita Chromium de Playwright y las fuentes Lora y Poppins): `python render.py entrada.json salida/`. El tamaño de la frase se ajusta solo; no fijes tamaños a mano.
4. **Mira cada PNG** antes de entregarlo: contraste, que nada quede en la zona segura, una idea por placa.
5. **Entrega para revisión** como dice 🎨 › *Dónde se revisan*. Si no hay visor disponible, entrégalas en la conversación y di a qué fila van. Claude no puede adjuntar archivos a Notion desde su entorno: los adjunta una persona.

## Terminada cuando

- [ ] Hay una placa por bloque del guion, numeradas en orden.
- [ ] Todas cumplen 🎨 (colores, tamaños mínimos, zona segura).
- [ ] Lo que falta (fotos, pruebas) está dicho.

## Después de la revisión

La revisión visual es de una persona: no cambies el `Estado` a `Para subir`, eso lo hace quien adjunta. Si el comentario es sobre cómo se ven, conviértelo en regla en 🎨 de inmediato, desde la intención, con fecha y quién la pidió; si contradice una regla, acótala. Luego vuelve a renderizar.

## Entrega

En la tarjeta y en tu respuesta: las placas numeradas, a qué fila pertenecen y qué falta.
