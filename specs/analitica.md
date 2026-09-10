# Spec · Analítica

**Estado:** scaffold listo, inerte hasta cargar llaves · **Última revisión:** 2026-09-10

## Por qué existe y por qué así

El sitio está por recibir tráfico pagado de Instagram. Sin medición se
optimizaría a ciegas, y el costo de eso escala con cada peso invertido.

**Se eligió PostHog + Meta Pixel**, no Cloudflare Web Analytics: el repo
`jubilarme-landing-hijos` ya usa PostHog, con taxonomía de eventos y lecciones
de depuración escritas, y el Meta Pixel no es opcional para un funnel de ads
de Meta — es lo que permite que la entrega se optimice hacia conversiones.

## Cómo está armado

```
wrangler.toml [vars]  →  GET /api/config  →  analitica.js  →  PostHog + fbq
   (POSTHOG_KEY, …)       (endpoint público)   (en cada página)
```

- **`functions/api/config.js`** devuelve las llaves públicas en runtime. Nada
  de esto es secreto: la clave pública de PostHog y el ID del Pixel viven en
  el navegador de todos modos.
- **`site/assets/js/analitica.js`** carga los dos SDK desde ese config. Si el
  config viene vacío (o falla), no hace nada. El sitio funciona igual.
- Cargado en las 6 páginas, antes de `atribucion.js` y los scripts de form.

**Se puede desplegar ahora mismo sin cuentas.** Con las variables vacías, la
analítica no carga y no rompe nada. Se activa después solo poniendo las
llaves en `wrangler.toml` y haciendo push.

## Eventos

Reglas (del README de `jubilarme-landing-hijos`): nombres estables y
aburridos, nunca PII en las propiedades, primero los cambios de estado del
funnel.

| Evento | Cuándo | Propiedades | Meta |
|---|---|---|---|
| *(pageview)* | cada carga | — | PageView (nativo de cada SDK) |
| `autodiagnostico_iniciado` | primera pregunta respondida | — | — |
| `autodiagnostico_completado` | las 25 respondidas | — | — |
| `autodiagnostico_enviado` | formulario enviado | `pilarMasBajo` | `Lead` |
| `guia_solicitada` | captura enviada | `guia` | `Lead` |
| `cta_calendly` | clic en un enlace de Calendly | `ubicacion` | `Schedule` |
| `cta_whatsapp` | clic en un enlace de wa.me | `ubicacion` | — |

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
- [ ] Crear el Pixel en Meta Business y sacar su ID
- [ ] Cargar `POSTHOG_KEY`, `POSTHOG_HOST` y `META_PIXEL_ID` en
      `wrangler.toml` § `[vars]` (NO en el dashboard — ver `CLAUDE.md`), y push
- [ ] Verificar: abrir el sitio, revisar en PostHog → Activity que llegan
      `autodiagnostico_iniciado` y compañía; en el Meta Events Manager que
      llega `PageView` y `Lead`
