/**
 * GET /api/config — configuración pública que el navegador necesita en
 * runtime. Hoy solo PostHog.
 *
 * Por qué un endpoint y no meterlo en el HTML directo: el sitio se sirve
 * estático y cacheado, pero las llaves las manda Cloudflare Pages en
 * runtime. Así se cambian sin reconstruir nada, y si están vacías la
 * analítica simplemente no carga (analitica.js es no-op).
 *
 * NADA de esto es secreto: la clave pública de PostHog termina en el
 * navegador de todas formas. Los secretos de verdad (SHARED_TOKEN,
 * BREVO_API_KEY) nunca pasan por acá.
 */
export async function onRequestGet(context) {
  const { env } = context;
  return new Response(
    JSON.stringify({
      posthogKey: env.POSTHOG_KEY || '',
      posthogHost: env.POSTHOG_HOST || 'https://us.i.posthog.com'
    }),
    {
      headers: {
        'Content-Type': 'application/json',
        // Se puede cachear un ratito — no cambia seguido y evita un fetch
        // bloqueante en cada carga.
        'Cache-Control': 'public, max-age=300'
      }
    }
  );
}
