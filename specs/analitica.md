# Spec · Analítica

**Estado:** SDK integrado (wizard de PostHog), inerte hasta cargar la llave como Secret en Cloudflare · **Última revisión:** 2026-09-15

## El modelo de funnel (corregido por Marcel, 2026-09-10)

El tráfico pagado de Instagram **no llega al sitio**. El funnel de venta es
Instagram: los ads llevan a la cuenta y al contenido, ahí se nutre a la
audiencia, y recién después se redirige a la gente al sitio — esencialmente
para entregar los lead magnets. El sitio también sirve como prueba de que
detrás hay un negocio real.

Consecuencia: **no hay Meta Pixel.** Meta no manda tráfico al sitio, así que
no tiene una cadena clic → sitio → conversión que optimizar. Se quitó de
`analitica.js`, `config.js` y `wrangler.toml`. Si algún día se hace
retargeting (mostrar ads a quien visitó `/plan` y no dejó el correo), se
vuelve a agregar: el snippet de Meta es de ~5 líneas y el patrón —cargar
desde `/api/config`, no-op sin ID— ya está probado con PostHog.

## Qué mide PostHog, y por qué sigue valiendo la pena

Aunque el tráfico llegue por enlaces de Instagram y no por ads, las
preguntas del sitio siguen siendo reales:

- De quienes caen en `/plan`, ¿cuántos dejan el correo?
- De quienes empiezan el autodiagnóstico, ¿cuántos llegan a las 25
  preguntas? 25 preguntas en el celular es una apuesta fuerte — sin este
  dato no se sabe si funciona o si sangra en la pregunta 12.
- ¿Qué lead magnet convierte mejor?
- ¿Cuánta gente hace clic en el CTA de Calendly desde el resultado?

## Cómo está armado

```
Secret de Cloudflare Pages  →  GET /api/config  →  analitica.js  →  PostHog
(POSTHOG_PROJECT_TOKEN, POSTHOG_HOST)  (endpoint público)   (en cada página)
```

- **`functions/api/config.js`** devuelve la llave pública en runtime. No es
  secreta: la clave pública de PostHog vive en el navegador de todos modos.
  Se marca como Secret en el dashboard igual, no por confidencialidad sino
  porque así se evita tener que tocar `wrangler.toml` cada vez que cambia.
- **`site/assets/js/analitica.js`** carga el SDK desde ese config. Si falta
  alguna variable, no hace nada en producción (en `localhost` sí avisa con
  una excepción, para no perder eventos en silencio durante el desarrollo).
- Cargado en las 6 páginas, antes de `atribucion.js` y los scripts de form.

**Se puede desplegar ahora sin cuenta.** Sin las dos variables, la analítica
no carga y el sitio funciona igual. Se activa poniendo `POSTHOG_PROJECT_TOKEN`
y `POSTHOG_HOST` como **Secret** en el dashboard de Cloudflare Pages
(Settings → Environment variables del proyecto) — no hace falta tocar el
repo ni hacer push. El wizard de instalación de PostHog (`npx @posthog/wizard`)
dejó los valores reales en `.dev.vars` para pruebas en local; son los mismos
que van al dashboard.

## Eventos

Reglas (del README de `jubilarme-landing-hijos`): nombres estables y
aburridos, nunca PII, primero los cambios de estado del funnel.

| Evento | Cuándo | Propiedades |
|---|---|---|
| *(pageview)* | cada carga | — (nativo de PostHog) |
| `autodiagnostico_iniciado` | primera pregunta respondida | — |
| `autodiagnostico_completado` | las 25 respondidas | — |
| `autodiagnostico_enviado` | formulario enviado | `pilarMasBajo` |
| `guia_solicitada` | captura enviada | `guia` |
| `cta_calendly` | clic en un enlace de Calendly | `ubicacion` |
| `cta_whatsapp` | clic en un enlace de wa.me | `ubicacion` |

`ubicacion` es `location.pathname`, nunca la URL completa (podría traer el
correo en un parámetro). Ningún evento manda el correo, ni las respuestas,
ni nada identificable.

Todos nuestros eventos ocurren sin navegación de por medio (el resultado se
muestra sin recargar, la captura confirma en la misma página, los CTA abren
en pestaña nueva), así que no hay carrera con el `flush` como en el flujo de
regalo de `hijos`.

## Lo que falta — todo es de Marcel

- [x] Crear el proyecto en PostHog y correr el wizard de instalación
      (2026-09-15) — integró el SDK en `analitica.js`/`config.js` y dejó
      el token real en `.dev.vars` (gitignored)
- [ ] **Cargar `POSTHOG_PROJECT_TOKEN` y `POSTHOG_HOST` como Secret en el
      dashboard de Cloudflare Pages** — el wizard los dejó listos en
      `.dev.vars`, solo hay que copiarlos ahí. Sin esto, `/api/config`
      sigue devolviendo `{}` y la analítica no carga (confirmado en
      producción el 2026-09-15)
- [ ] Decidir sobre el **proxy inverso**. PostHog directo funciona pero lo
      bloquean varios ad-blockers. `hijos` lo resolvió con un subdominio
      (`a.hijos.jubilar.me`) que reenvía a `us.i.posthog.com`. El equivalente
      sería `a.disenatujubilacion.com`. Sin proxy: se pierden pageviews de
      quienes usan bloqueador, pero los eventos custom y las grabaciones
      suelen pasar igual. Se puede empezar sin proxy y agregarlo después
      cambiando solo `POSTHOG_HOST`
- [ ] Autorizar el dominio en PostHog (no basta con configurarlo en el
      código — sin esto los pageviews nativos quedan en cero aunque los
      eventos custom aparezcan; es la trampa que documenta el README de `hijos`)
- [ ] Verificar en PostHog → Activity que llegan `autodiagnostico_iniciado`
      y compañía
