# Spec · Contrato de datos del envío

**Estado:** vigente · **Última revisión:** 2026-09-10 (Fase 0: se separó `origen` de `guia`, se agregó atribución UTM y el régimen de consentimiento)

Este contrato cruza cuatro codebases en dos lenguajes: el JavaScript del
navegador, la Pages Function, Apps Script y las planillas. Nada lo valida de
punta a punta. Ya causó dos bugs por desajuste, así que **este archivo es la
fuente de verdad**: si cambias un campo, cámbialo acá primero.

## El recorrido

```
navegador ──POST /api/submit──> Worker ──> Brevo (correo)
                                   │
                                   └──POST──> Apps Script ──> Sheets
```

El Worker intenta Brevo **primero** y recién después llama a Apps Script,
para poder informarle en la misma petición si el correo falló. Un solo
viaje, no dos.

## 1 · Navegador → Worker

Lo emiten `assets/js/autodiagnostico.js` y `assets/js/captura.js`.

| Campo | Tipo | Quién lo manda | Nota |
|---|---|---|---|
| `email` | texto | ambos | Obligatorio. Único campo sin el cual se rechaza |
| `guia` | texto | ambos | `DOMINO` · `PLAN` · `HABLAR` · `ENTUSIASMO` · `RETIRO`. Qué recurso pidió |
| `origen` | texto | ambos | `utm_source`, o `sitio-interno` / `directo`. **De dónde vino**, distinto de `guia`. Producido por `atribucion.js` |
| `campana` | texto | ambos | `utm_campaign`. Vacío si no vino de una campaña |
| `contenido` | texto | ambos | `utm_content`. La pieza puntual: `reel-jinetes`, `historia-3`… |
| `regimen` | texto | ambos | `PRE_LEY` o `LEY_21719`. Bajo qué régimen se captó. Ver `specs/consentimiento.md` |
| `consentMarketing` | booleano | ambos | Casilla opcional, sin premarcar |
| `consentGuardado` | booleano | ambos | En PRE_LEY el front lo manda `true` y el Worker igual lo fuerza. Ver `specs/consentimiento.md` |
| `versionTexto` | texto | ambos | Qué versión del texto legal aceptó la persona. Nombra el régimen (`…-preley-…`) |
| `sitioWeb` | texto | ambos | Honeypot. Si trae contenido, es un bot |
| `totales` | objeto | solo autodiagnóstico | `{proposito, fisico, mental, social, finanzas}`, cada uno 5–25 |
| `respuestas` | arreglo | solo autodiagnóstico | `[{pregunta, pilar, valor}]`, valor 1–5 |
| `uuid` | texto | solo autodiagnóstico | **Se descarta.** Ver *Identidad* |
| `pilarMasBajo` | texto | solo autodiagnóstico | **Se descarta.** Solo lo usa la vista de resultado |

## 2 · Worker → Apps Script

El Worker **no reenvía lo que recibió**: valida, normaliza, recorta y arma un
payload propio. Nunca confía en el navegador para el token.

Agrega:

| Campo | Qué es |
|---|---|
| `token` | Secreto compartido, **en el cuerpo** — Apps Script no lee headers |
| `fecha` | ISO, generada en el servidor. Ignora la del navegador |
| `correoEnviado` | Si Brevo aceptó el envío |
| `correoPendiente` | Solo si falló: `{cuerpoBrevo, motivo}` con el cuerpo exacto que se le iba a mandar a Brevo, listo para reintentar sin reconstruir nada |

Recortes defensivos: `email` ≤254, `guia`/`origen` ≤30, `versionTexto` ≤100,
`respuestas` ≤200 entradas, `pregunta` ≤500. Una guía que no esté en la lista
cae a `DOMINO`.

## 3 · Worker → Brevo

`POST https://api.brevo.com/v3/smtp/email`, con la llave en el header
`api-key`.

```
{ sender, to, templateId, params?, attachment? }
```

- `templateId` sale de la variable de entorno según la guía.
- `params` **solo se incluye si tiene contenido** — Brevo rechaza `{}` con
  `"params is blank"`. Hoy solo `DOMINO` manda parámetros: los cinco totales
  más `pilarMasBajo` con el nombre legible del pilar.
- `attachment` solo en las guías con PDF (PLAN, HABLAR, ENTUSIASMO); Brevo
  descarga el archivo desde la URL.

## 4 · Apps Script → Sheets

**Identidad:** la decide Apps Script, no el navegador. Se busca por correo;
si existe, se reutiliza su uuid. El `uuid` que manda el navegador se
descarta. Una persona = una fila, aunque vuelva por otra guía.

Al reencontrar a alguien: se actualiza `ultimo_contacto` y `version_texto`,
el consentimiento **sube pero nunca baja solo**, y el `origen` del primer
contacto **no se sobrescribe** (atribución de adquisición, no de última
interacción).

### `DTJ · Personas` — pestaña `personas`

```
id · email · fecha_alta · origen · campana · contenido · regimen
consent_guardado · consent_guardado_fecha
consent_marketing · consent_marketing_fecha · version_texto · ultimo_contacto
```

El **orden de las columnas no importa**: `Personas.gs` se guía por el nombre
del encabezado. `campana`, `contenido` y `regimen` se agregaron en la Fase 0;
si la planilla todavía no las tiene, la persona igual se guarda con el resto
y el log avisa qué campo no cupo.

### `DTJ · Respuestas` — pestaña `respuestas`

```
id · guia · pregunta · pilar · valor · total_pilar · fecha
```

Archivo **separado** a propósito: no contiene correos, así que una
exportación de esta tabla no identifica a nadie. Se une a `personas` solo
por uuid.

### Pestañas operativas, en el archivo de Personas

- `correos_pendientes`: `fecha_primera_falla · email · guia ·
  cuerpo_brevo_json · intentos · ultimo_error · estado`. **Tiene datos
  personales** (el correo, y para DOMINO los totales dentro del JSON), así
  que `borrarPersona()` la limpia también.
- `solicitudes`: registro de cada solicitud de derechos atendida.

## Deuda saldada en la Fase 0

**`origen` estaba sobrecargado** — significaba `utm_source` en el
autodiagnóstico y el nombre de la guía en las capturas, duplicando `guia`.
Resuelto:

| Campo | Qué es | Lo produce |
|---|---|---|
| `guia` | qué recurso pidió | el `data-guia` del form / hardcode `DOMINO` |
| `origen` | `utm_source`, o `sitio-interno` / `directo` | `atribucion.js` |
| `campana` | `utm_campaign` | `atribucion.js` |
| `contenido` | `utm_content` | `atribucion.js` |

`atribucion.js` es el único lugar donde vive esta lógica; los dos forms lo
llaman. Los PDF (`lead-magnets/build_common.py`) ponen `utm_source=pdf-<guia>`
en el enlace de Calendly, para atribuir qué guía trae llamadas agendadas.

## Deuda pendiente

- El **límite por IP** vive en KV (1.000 escrituras/día). Para un pico de
  tráfico pagado de Instagram puede quedar corto; migrar a Durable Objects
  o al binding nativo de Rate Limiting si el volumen lo pide.
- La **analítica** (PostHog + Meta Pixel) está montada como scaffold
  inerte hasta que se carguen las llaves. Ver `specs/analitica.md`.

## Reglas al cambiar este contrato

1. Un campo nuevo se agrega **primero acá**, después en el código.
2. Nunca se reusa un campo existente para otro significado. Ese fue el error
   con `origen` y costó atribución.
3. Los campos que el Worker descarta se descartan **explícitamente**, no por
   omisión, para que se note al leer el código.
4. Todo cambio de esquema de planilla se prueba con `curl` contra producción
   y se limpia después con el menú de privacidad.
