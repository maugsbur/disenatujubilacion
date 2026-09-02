# Diseña tu Jubilación — sitio web

Dominio: `disenatujubilacion.com` · Desplegado en Cloudflare Pages (plan gratuito).

Ver [`PLAN.md`](./PLAN.md) para las etapas de trabajo y su estado.

## Estructura del repositorio

```
site/              → carpeta que Cloudflare Pages publica (output directory = "site")
  index.html          landing (placeholder, Etapa 6 la reemplaza)
  autodiagnostico/
    index.html         única página interactiva: preguntas + resultado, una vista JS
  plan/ hablar/ carlos/
    index.html         páginas de captura para las guías PDF (placeholder, Etapa 6)
  privacidad/
    index.html         política de privacidad (placeholder, Etapa 6)
  assets/
    css/base.css        tokens de marca + reset, compartido por todo el sitio
    css/autodiagnostico.css
    js/autodiagnostico.js
  _redirects           rewrite de /autodiagnostico/resultado (Pages)
  _headers             headers de seguridad básicos (Pages)

worker/            → Worker delgado de Cloudflare (Etapa 4, aún no construido)
apps-script/       → código de Apps Script para Sheets + Gmail (Etapa 3, aún no construido)
```

## Desarrollo local

Cualquier servidor estático sirve. Por ejemplo:

```bash
npx serve site
```

o

```bash
python -m http.server 8080 --directory site
```

Abre `http://localhost:8080/autodiagnostico` — la vista de resultado no depende de red,
así que se puede probar completa sin el Worker ni Apps Script desplegados.

## Despliegue (Cloudflare Pages)

1. En el dashboard de Cloudflare: **Workers & Pages → Create → Pages → Connect to Git**.
2. Selecciona el repo `maugsbur/disenatujubilacion`, rama `main`.
3. Build settings:
   - Framework preset: **None**
   - Build command: *(vacío)*
   - Build output directory: **`site`**
4. Agrega el dominio personalizado `disenatujubilacion.com` en **Custom domains** una vez creado el proyecto.
5. Cada push a `main` dispara un deploy automático (dentro del límite de 500 builds/mes del plan gratuito).

El Worker (`/api/submit`) y Apps Script se conectan en la Etapa 4–5; hasta entonces, el
formulario del autodiagnóstico intenta el POST, falla en silencio (404, sin endpoint aún) y
el resultado se muestra igual — es el comportamiento esperado, ver `PLAN.md`.

## Autodiagnóstico: cómo está armado

Es una sola página (`site/autodiagnostico/index.html`) con dos `<section>`: `#view-questions`
y `#view-result`. `assets/js/autodiagnostico.js` calcula los totales por pilar en el navegador,
cambia de vista sin recargar, y actualiza la URL a `/autodiagnostico/resultado` con
`history.pushState` (la regla en `_redirects` hace que un refresh en esa URL siga sirviendo
el mismo archivo). El resultado de la sesión se guarda en `sessionStorage` solo para sobrevivir
ese refresh — no es persistencia real; esa vive en Sheets vía Apps Script.

Mobile-first a propósito: el HTML original de referencia (`autodiagnostico-interactivo.html`,
fuera de este repo) estaba maquetado como páginas A4 apiladas en `mm`/`pt` para exportar a PDF
con wkhtmltopdf. Esa maqueta no se reutiliza aquí — se reescribió el layout completo en unidades
relativas, con objetivos de toque ≥48px y una barra de progreso fija, pensando en tráfico desde
el navegador integrado de Instagram.
