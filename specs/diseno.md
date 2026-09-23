# Spec · Sistema de diseño

**Estado:** vigente · **Última revisión:** 2026-09-23 (las reglas visuales
pasan a vivir en Notion; acá queda solo la implementación)

**Las reglas visuales viven en Notion**, en *🎨 Cómo diseñamos*
(https://app.notion.com/p/3d523cb6e7af81f9a703eb234cce4a22): paleta,
tipografía, logo, placas de Instagram, guías en PDF y sitio. Esa página es
la fuente, y la escriben el chat, cowork, Claude Code y el equipo.

Este archivo guarda solo lo que está pegado al código: cómo se implementó el
sistema en el CSS del sitio, qué se tomó de `hijos.jubilar.me`, el truco del
hero con `:has()` y cómo se procesan logo y fotos. Si cambia una regla
visual, se cambia en Notion; si cambia la forma de implementarla, acá.

## De dónde viene

Marcel pidió que el sitio se pareciera a `hijos.jubilar.me` (repo
`jubilarme-landing-hijos`, clonado en `workspace/jubilarme-hijos`) en
layout, tarjetas, secciones y el bloque de "quiénes somos", adaptado al
público nuevo y a los colores de DTJ.

**Se portó el lenguaje visual, no el código.** Se descartó migrar a Astro:
el autodiagnóstico, las páginas de captura y las Pages Functions funcionan
y están verificadas en producción, y migrarlas para conseguir un aspecto
que se logra con CSS es mucho riesgo sin ganancia funcional. Lo único que
se pierde de Astro: en hijos el copy vive en un objeto de datos, así que
alguien sin perfil técnico puede editar textos sin tocar markup. Si eso
llega a doler, se reevalúa — pero por contenido, no por diseño.

## Qué se tomó de hijos

| Elemento | Cómo quedó en DTJ |
|---|---|
| Contenedor ancho (1080px) | `.container-wide`. **Solo** para secciones con grillas o dos columnas |
| Franjas alternadas | `.bg-alt` sobre `--dtj-paper-alt`. Reemplaza las líneas divisorias en la landing |
| Tarjetas con sombra | `.card` + sombra en `.res-card` / `.testi-card` |
| Hero de dos columnas | `.hero-grid` (ver *El hero* abajo) |
| Quiénes somos | Relato + una tarjeta por persona con foto (`.person-grid`, `.person-card`) |
| Chips de datos | `.microcopy`, solo en el hero (sus colores asumen fondo oscuro) |
| Botones píldora | Ya existían — `.btn` con `border-radius: 999px` |

## Decisiones propias, distintas de hijos

**El hero se queda verde oscuro.** hijos tiene el hero claro con una
etiqueta verde. DTJ mantiene su bloque verde: es el activo de marca más
fuerte que tiene y da un contraste que hijos no tiene. Si se prefiere el
tratamiento claro de hijos, es cambiar el fondo de `.cap-hero` — pero
afecta también a las 4 páginas de captura, que lo comparten.

**La prosa no se ensancha.** `--max-w` (40rem) sigue mandando en el texto
largo; `--max-w-wide` (67.5rem) es solo para layout. 1080px de ancho de
lectura cansa. Por eso las páginas de captura y `/privacidad` conservan el
contenedor angosto: heredan el lenguaje visual (papel cálido, tarjetas con
sombra, botones) sin volverse ilegibles.

**El fondo es papel cálido, no gris.** `--dtj-paper: #FAF9F6` reemplazó a
`--dtj-offwhite` como fondo de `body`. `--dtj-offwhite` se queda como el
"casi blanco" para texto y rellenos sobre fondos oscuros.

## El hero y la imagen que falta

`.hero-grid` arranca en **una columna** y se parte en dos solo cuando el
HTML trae de verdad un `<img class="hero-media">`, vía `:has()`:

```css
@media (min-width: 860px) {
  .hero-grid:has(.hero-media) { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
```

Así no queda medio hero vacío mientras no exista la imagen. Verificado en
el navegador: sin imagen `grid-template-columns` da `1032px`; al agregarla
pasa a `492px 492px`. Si un navegador no soporta `:has()`, se queda en una
columna con la imagen abajo — que es el layout móvil, aceptable.

**Pendiente de Marcel:** la imagen del hero. La de hijos
(`jubilados-felices.png`) es una ilustración de jubilados abrazados en el
campo: para "líderes y profesionales exitosos cuya identidad está ligada al
trabajo" apunta al lado equivocado y puede leerse condescendiente. Cuando
exista, va como segundo hijo de `.hero-grid` y no hay que tocar CSS.

## Imágenes y marca

- **Logo:** el de Jubilar.me (anillos de árbol) con las tintas de DTJ. El
  `logo-jubilarme.svg` original no es vectorial: es un PNG embebido en base64.
  Se recoloreó pixel a pixel (cada pixel toma la tinta más cercana, verde o
  terracota, y conserva su alfa). Master en `brand/logo-dtj-512.png`; en el
  sitio `assets/img/logo-dtj.png` (192px, paleta de 48 colores, 9 KB),
  `favicon.ico` y `apple-touch-icon.png` (este sobre fondo papel: iOS pinta
  de negro la transparencia).
- **Fotos individuales**, no la de los dos juntos (Marcel prefirió fotos
  donde se vean más profesionales, y están lejos para sacarse una juntos):
  `nicole.jpg` es la de jubilar.me (240×328, **provisoria**, Marcel busca
  una de mejor calidad) y `marcel.jpg` la que mandó Marcel (300×300). Se
  muestran como círculo de 88px, así que alcanza.
- **Ojo con la orientación EXIF** al procesar fotos con PIL: la ignora y la
  foto sale rotada. Pasar siempre `ImageOps.exif_transpose()` antes.

## Lo que falta

- [ ] Imagen del hero (arriba)
- [x] Logo y header fijo (2026-09-16)
- [x] Fotos individuales en las bios (2026-09-16)
- [ ] Foto de Nicole en mejor calidad (Marcel la está buscando)
- [ ] El autodiagnóstico quedó fuera de esta pasada: hereda tokens y
      botones de `base.css`, pero su UI de 25 preguntas tiene CSS propio
