# Spec · Analítica

**Estado:** scaffold listo, inerte hasta cargar la llave · **Última revisión:** 2026-09-10

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
wrangler.toml [vars]  →  GET /api/config  →  analitica.js  →  PostHog
   (POSTHOG_KEY, …)       (endpoint público)   (en cada página)
```

- **`functions/api/config.js`** devuelve la llave pública en runtime. No es
  secreta: la clave pública de PostHog vive en el navegador de todos modos.
- **`site/assets/js/analitica.js`** carga el SDK desde ese config. Si el key
  viene vacío (o falla), no hace nada. El sitio funciona igual.
- Cargado en las 6 páginas, antes de `atribucion.js` y los scripts de form.

**Se puede desplegar ahora sin cuenta.** Con `POSTHOG_KEY` vacío la analítica
no carga. Se activa después poniendo la llave en `wrangler.toml` y push.

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

- [ ] Crear el proyecto en PostHog (uno para producción; idealmente otro
      aparte para preview, para no ensuciar el reporte con tráfico de prueba)
- [ ] Decidir sobre el **proxy inverso**. PostHog directo funciona pero lo
      bloquean varios ad-blockers. `hijos` lo resolvió con un subdominio
      (`a.hijos.jubilar.me`) que reenvía a `us.i.posthog.com`. El equivalente
      sería `a.disenatujubilacion.com`. Sin proxy: se pierden pageviews de
      quienes usan bloqueador, pero los eventos custom y las grabaciones
      suelen pasar igual. Se puede empezar sin proxy y agregarlo después
      cambiando solo `POSTHOG_HOST`.
- [ ] Autorizar el dominio en PostHog (no basta con configurarlo en el
      código — sin esto los pageviews nativos quedan en cero aunque los
      eventos custom aparezcan; es la trampa que documenta el README de `hijos`)
- [ ] Cargar `POSTHOG_KEY` y, si hay proxy, `POSTHOG_HOST` en
      `wrangler.toml` § `[vars]` (NO en el dashboard — ver `CLAUDE.md`), y push
- [ ] Verificar en PostHog → Activity que llegan `autodiagnostico_iniciado`
      y compañía
