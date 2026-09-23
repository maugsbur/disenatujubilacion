# Spec · Sistema de diseño

**Estado:** vigente · **Última revisión:** 2026-09-23 (se suman las reglas
de las placas de Instagram, que vivían solo en Notion)

Cubre lo visual de los tres soportes: el sitio, los PDF de las guías y las
placas de Instagram. Lo que es de texto vive en [`voz.md`](voz.md).

La página de Notion *🎨 Cómo diseñamos* es la **copia publicada** de la
sección de placas, para el equipo y para la skill `disenar-placas-ig`. Si
cambias una regla acá, actualiza esa página en el mismo movimiento.

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

## Placas de Instagram

Vienen de la página de Notion *🎨 Cómo diseñamos*, que se llena con las
correcciones de Nicole en el visor de cada secuencia. Igual que en
[`voz.md`](voz.md), **una corrección se convierte en regla de inmediato**, y
lo que se escribe es la intención detrás del cambio, no el cambio puntual. Si
esa intención no es evidente, se pregunta antes de escribirla.

### Legibilidad, que manda sobre la estética

El público tiene 55 años o más y mira en un teléfono, muchas veces de paso.
Una placa elegante que no se lee es una placa fallida.

- **Nada de texto bajo 36px** en un lienzo de 1080 de ancho. El contexto en
  mayúsculas va en 46px, el pie en 38px, el matiz en 50px.
- **Contraste mínimo 4,5:1 para texto normal y 3:1 para texto grande**,
  verificado y no a ojo.
- **Ámbar `#E65F2B` solo sobre fondos oscuros o el off-white.** Sobre crema
  da 2,81:1 y no se lee, así que ahí el contexto va en verde.
- **El tamaño de la frase principal se calcula solo** hasta llenar el 62% del
  área segura. Es lo que hace que una placa de seis palabras y otra de treinta
  se vean de la misma familia.
- **Zona segura de 260px arriba y abajo** en historias, donde Instagram pone
  la barra de perfil y la caja de respuesta.

### Consistencia con un quiebre

- **Solo dos fondos: verde y blanco.** El crema no se usa de fondo, queda para
  texto de contexto sobre verde (Nicole, 08/09/2026).
- **Verde es la base de la secuencia** y **una o dos placas rompen a blanco**
  para destacar, típicamente la del dato. Si rompen todas, no destaca ninguna.
- **El CTA vuelve al verde**, para cerrar donde empezó.

### Color y tipografía

| Fondo | Texto | Contexto | Palabra del CTA |
|---|---|---|---|
| Verde `#0E3A2F` | off-white | crema | **ámbar** |
| Carbón `#1A2421` | off-white | crema | **ámbar** |
| Crema `#F6E7B0` | verde | verde | verde (el ámbar no contrasta) |
| Claro `#F8F9FA` | carbón | verde | **ámbar** |

- **Lora para lo que se lee, Poppins para lo que se etiqueta.** Frase
  principal, dato y cita en serif; contexto, autoría y pie en sans.
- **Una idea por placa**: contexto, frase, matiz. Si hace falta una cuarta
  línea, sobra algo o son dos placas.
- El **ámbar es acento, nunca fondo**.

### Dónde se revisan

Cada secuencia se publica como un **visor**, una página con las placas en tira
a proporción real y con botón de descarga. El enlace va en la fila de la pieza
en Notion, y el feedback se deja como comentario sobre la placa concreta.
Cuando la misma corrección aparece dos veces, sube a regla acá.
