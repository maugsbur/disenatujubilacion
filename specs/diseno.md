# Spec · Sistema de diseño

**Estado:** vigente · **Última revisión:** 2026-09-16 (se portó el lenguaje visual de `hijos.jubilar.me`)

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
| Relato con foto | `.story-grid` + `.story-photo-shell` |
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

## Imágenes

- `site/assets/img/nicole-marcel-{800,1200}.jpg` — foto de los dos, sacada
  de `jubilarme-hijos/src/assets/marcel-nicole.jpg` (4000×3000). Resuelve
  el pendiente de "foto nueva de Nicole" (la de `jubilar.me` era 240×328).
- **El original trae orientación EXIF.** PIL la ignora al redimensionar y
  la foto sale rotada 90°; Astro la corregía sola, por eso en hijos se ve
  bien. Hay que pasar `ImageOps.exif_transpose()` antes de redimensionar.
- Las caras quedan bajo el centro del encuadre: `object-position: center 42%`
  evita que el recorte las corte en pantallas anchas.

## Lo que falta

- [ ] Imagen del hero (arriba)
- [ ] **Logo.** hijos tiene un header fijo con logo y CTA. DTJ no tiene
      ningún logo en el repo, así que no se agregó header. Si aparece uno,
      el header es directo
- [ ] Fotos individuales de Nicole y Marcel en las bios (hoy solo texto;
      los avatares con letras "N"/"M" se quitaron al entrar la foto real)
- [ ] El autodiagnóstico quedó fuera de esta pasada: hereda tokens y
      botones de `base.css`, pero su UI de 25 preguntas tiene CSS propio
