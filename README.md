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
    pdfs/                los tres PDF de las guías, en rutas oscuras y sin enlazar (Etapa 5)
  _redirects           rewrite de /autodiagnostico/resultado (Pages)
  _headers             headers de seguridad básicos + noindex de /assets/pdfs/ (Pages)

functions/         → Worker delgado, como Cloudflare Pages Function (Etapa 4)
  api/submit.js       POST /api/submit: valida, limita por IP, reenvía a Apps Script y Brevo

brevo/             → plantillas de correo + guía de configuración (Etapa 5)
apps-script/       → código de Apps Script: dos planillas, derechos ARCO, cola de reintento
wrangler.toml      → config del proyecto Pages: KV para el límite por IP
.dev.vars.example  → plantilla de variables de entorno para probar en local
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

## El Worker (`/api/submit`)

Vive en `functions/api/submit.js` como **Pages Function** — se despliega solo con cada
push a `main`, en el mismo dominio que el sitio (sin CORS que configurar), sin un
`wrangler deploy` aparte. Valida el payload, limita por IP con KV, filtra el honeypot,
y reenvía a Apps Script agregando el token compartido dentro del cuerpo JSON (Apps Script
no expone headers HTTP personalizados — no puede ir como `Authorization`).

**Para activarlo en producción**, dos cosas en el dashboard de Cloudflare (proyecto Pages
→ Settings):

1. **Crear el namespace de KV** para el límite por IP: **Workers & Pages → KV → Create
   namespace** (nómbralo `dtj-rate-limit`), copia su ID, y pégalo en `wrangler.toml` en
   este repo, reemplazando `PEGAR_AQUI_EL_ID_DEL_NAMESPACE_KV`. Al hacer push, Pages lo
   detecta solo (los bindings de `wrangler.toml` se aplican en cada deploy conectado a Git).
2. **Variables de entorno** (Settings → Environment variables, en Production): agrega
   `APPS_SCRIPT_URL` (la URL `/exec` del Web App, ver `apps-script/README.md`) y
   `SHARED_TOKEN` (el mismo token que configuraste en Apps Script) — marca esta última
   como **Secret**, no como texto plano. Estas dos NO van en `wrangler.toml` ni en el
   repo: solo en el dashboard.

Hasta que esas dos cosas estén configuradas, el formulario del autodiagnóstico sigue
mostrando el resultado igual (el diseño nunca dependió del envío para eso), pero el POST
le va a devolver `config_del_worker_incompleta` en vez de guardar nada.

**Probado en local** con `wrangler pages dev` y un Apps Script simulado: envío válido,
honeypot, correo inválido, tipo de contenido incorrecto y el límite de 6 envíos por
IP cada 60 segundos — los cinco se comportan como se espera antes de este commit.

## El correo (Brevo, Etapa 5)

El Worker intenta mandar el correo con Brevo **antes** de reenviar a Apps Script; si
Brevo falla, se lo dice a Apps Script en el mismo request para que quede en la cola de
reintento (`apps-script/CorreoPendiente.gs`). Ver `brevo/README.md` para la cuenta, el
dominio (SPF/DKIM/DMARC), las cuatro plantillas y todas las variables de entorno que
faltan (`BREVO_API_KEY`, `BREVO_SENDER_EMAIL`, `BREVO_SENDER_NAME`,
`BREVO_TEMPLATE_DOMINO/PLAN/HABLAR/ENTUSIASMO`, `PDF_URL_PLAN/HABLAR/ENTUSIASMO`).

Los tres PDF ya están en el repo (`site/assets/pdfs/`), en rutas largas y aleatorias,
sin enlazar desde ninguna página — Brevo los descarga con el campo `url` de su API al
momento de mandar el correo. `BREVO_API_URL` es opcional y solo existe para poder
apuntar a un servidor simulado al probar en local; sin definirla, el Worker usa la URL
real de Brevo.

**Probado en local** con Brevo simulado, éxito y con un 402 forzado (cuota topada): el
correo con adjunto solo se arma para PLAN/HABLAR/ENTUSIASMO, DOMINÓ lleva los cinco
totales por pilar en los parámetros, y cuando el envío falla, el cuerpo que llega a
Apps Script para la cola de reintento es exactamente el que hacía falta para
reintentarlo sin reconstruir nada.

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
