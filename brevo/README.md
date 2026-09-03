# Brevo — correo transaccional

Reemplaza a Apps Script/GmailApp como remitente (decisión de Marcel del
2026-09-02): el alias de dominio en Gmail sin Workspace dejó de ser viable
— ver `PLAN.md` § Etapa 0. Quien manda el correo es **el Worker**
(`functions/api/submit.js`); Apps Script solo lo reintenta si Brevo falló
la primera vez (`apps-script/CorreoPendiente.gs`).

## 1. Cuenta y dominio

1. Crea la cuenta en [brevo.com](https://www.brevo.com) con el correo del
   equipo (no uno personal).
2. **Senders & IP → Domains → Add a domain**: `disenatujubilacion.com`.
   Brevo te muestra un SPF, un DKIM y (si lo pide) un DMARC — cada uno como
   un registro TXT/CNAME con su valor exacto.
3. Agrega esos registros en **Cloudflare → tu dominio → DNS** (la zona ya
   está en tu cuenta). Cópialos tal cual los muestra Brevo, sin editar
   nada — un espacio de más en un registro DKIM y no valida.
4. Vuelve a Brevo y verifica el dominio. Puede tardar minutos u horas en
   propagar. Sin este paso, Brevo igual envía, pero con peor
   entregabilidad (más probabilidad de spam) — no lo saltes.
5. **Senders & IP → Senders → Add a sender**: `hola@disenatujubilacion.com`,
   nombre "Diseña tu Jubilación". Con el dominio ya verificado no hace
   falta confirmar por correo cada remitente individual.

## 2. Llave de API

**SMTP & API → API Keys → Generate a new API key.** Un solo nombre
descriptivo (p.ej. "Worker DTJ") alcanza — no hace falta una llave
distinta por plantilla ni por ambiente.

Vas a pegar la misma llave en **dos lugares** (el Worker envía primero, y
si falla, Apps Script la usa para reintentar más tarde con la misma):

- Dashboard de Cloudflare Pages → variable `BREVO_API_KEY` (Secret)
- Apps Script → `configurarPropiedades()` en `Config.gs`, propiedad `BREVO_API_KEY`

## 3. Plantillas

Cuatro, una por guía. El texto y los parámetros de cada una están en
`brevo/plantillas/` — las cuatro tienen copy real (se leyeron los tres PDF
completos en la Etapa 6, ya no son borradores).

Crea las cuatro en **Transaccional → Plantillas → Crear plantilla →
Plantilla de email** — no en Campañas, esa sección es de marketing y no
expone el `templateId` numérico que necesita la API que usa el Worker.
Anota el **Template ID** que Brevo le asigna a cada una — son números
(aparecen junto al nombre de la plantilla en la lista), los vas a necesitar en la
Etapa siguiente.

## 4. Los tres PDF

Ya están en el repo, en `site/assets/pdfs/`, con nombres largos y
aleatorios — no están enlazados desde ninguna página del sitio, así que la
única forma de llegar a ellos es con la URL exacta (por eso el adjunto se
manda por `url` y no hace falta subirlos a otro lado). El archivo
`site/_headers` ya les pone `noindex` por si algún crawler los encuentra
igual.

| Guía | Archivo |
|---|---|
| PLAN | `site/assets/pdfs/plan-468b5d9455ce73904853.pdf` |
| HABLAR | `site/assets/pdfs/hablar-bf1229460d8da5438ed2.pdf` |
| ENTUSIASMO | `site/assets/pdfs/entusiasmo-9cad1ef7759af90e6233.pdf` |

Las URLs completas una vez desplegado el sitio:

```
https://disenatujubilacion.com/assets/pdfs/plan-468b5d9455ce73904853.pdf
https://disenatujubilacion.com/assets/pdfs/hablar-bf1229460d8da5438ed2.pdf
https://disenatujubilacion.com/assets/pdfs/entusiasmo-9cad1ef7759af90e6233.pdf
```

**Si alguna vez hay que reemplazar un PDF** (una corrección, quitar el
sello de borrador de ENTUSIASMO, etc.): sube el archivo nuevo con un
nombre aleatorio distinto (no reuses el nombre viejo — el correo antiguo
en la bandeja de alguien seguiría apuntando al archivo anterior si lo
conservas, lo cual está bien, pero si lo *reemplazas* con el mismo nombre
nadie se entera de que cambió) y actualiza la variable `PDF_URL_*`
correspondiente.

## 5. Variables de entorno del Worker

⚠️ **Casi ninguna de estas va en el dashboard.** Con `wrangler.toml` presente
en el proyecto (como es nuestro caso, por el binding de KV de la Etapa 4),
Cloudflare Pages ignora las variables de texto plano puestas en el
dashboard — solo respeta ahí las marcadas como **Secret**. Esto costó una
buena sesión de diagnóstico en producción, ver `README.md` § El Worker.

**En `wrangler.toml`, sección `[vars]`** (texto plano, comiteado al repo):

| Variable | Valor |
|---|---|
| `APPS_SCRIPT_URL` | la URL `/exec` del Web App (Etapa 4) |
| `BREVO_SENDER_EMAIL` | `hola@disenatujubilacion.com` |
| `BREVO_SENDER_NAME` | `Diseña tu Jubilación` |
| `BREVO_TEMPLATE_DOMINO` | Template ID de DOMINÓ |
| `BREVO_TEMPLATE_PLAN` | Template ID de PLAN |
| `BREVO_TEMPLATE_HABLAR` | Template ID de HABLAR |
| `BREVO_TEMPLATE_ENTUSIASMO` | Template ID de ENTUSIASMO |
| `PDF_URL_PLAN` | URL completa del PDF de PLAN (tabla arriba) |
| `PDF_URL_HABLAR` | URL completa del PDF de HABLAR |
| `PDF_URL_ENTUSIASMO` | URL completa del PDF de ENTUSIASMO |

**En el dashboard de Cloudflare Pages → tu proyecto → Settings →
Environment variables (Production), marcadas como Secret** — estas sí son
sensibles de verdad y nunca van al repo:

| Variable | Valor |
|---|---|
| `SHARED_TOKEN` | el mismo token que configuraste en Apps Script (Etapa 4) |
| `BREVO_API_KEY` | la llave del paso 2 de arriba |

## 6. Qué pasa si Brevo falla o se topa la cuota

El plan free de Brevo son **~300 correos/día**. Si un envío falla por lo
que sea (cuota topada, Brevo caído, un ID de plantilla mal copiado), el
Worker no lo pierde: se lo pasa a Apps Script como un correo pendiente
(`apps-script/CorreoPendiente.gs`), que reintenta cada 30 minutos. Si
sigue fallando después de 24 horas, deja de reintentar esa fila y manda
una alerta a `disenatujubilacion@gmail.com` — para entonces ya se resetea
cualquier cuota diaria, así que 24 horas fallando significa que hay algo
más que revisar (llave vencida, plantilla borrada, etc.), no un simple
pico de tráfico.

Instala ese disparador una vez, desde el editor de Apps Script:

```
instalarTriggerReintentoCorreos()
```

**Probado en local** con Brevo simulado (éxito y con un 402 forzado): el
Worker arma el cuerpo correcto para la API en ambos casos, y cuando falla
le pasa a Apps Script exactamente lo que hace falta para reintentar sin
tener que reconstruir nada. Ver el commit de esta etapa para el detalle.

## 7. Prueba de entregabilidad (pendiente, después de desplegar)

Una vez que el dominio esté verificado y las cuatro plantillas creadas,
manda una prueba real a una cuenta de Gmail, una de Outlook/Hotmail y un
correo corporativo si tienes uno a mano. Revisa que no caiga en spam y que
el remitente se vea como `Diseña tu Jubilación <hola@disenatujubilacion.com>`,
no como una dirección rara de Brevo.
