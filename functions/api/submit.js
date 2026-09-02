/**
 * POST /api/submit — el Worker delgado delante de Apps Script.
 *
 * Vive como Pages Function: se despliega solo, en el mismo dominio que el
 * sitio (sin CORS que configurar), cada vez que se hace push a `main` —
 * no hace falta un `wrangler deploy` aparte.
 *
 * Qué hace, en orden:
 *   1. Exige Content-Type JSON y que el cuerpo parsee.
 *   2. Límite por IP (KV — ver nota de cuota más abajo).
 *   3. Honeypot: si viene con contenido, responde éxito sin escribir nada
 *      (no le confirma al bot que lo detectamos).
 *   4. Valida forma y tamaño del payload.
 *   5. Reenvía a Apps Script agregando el token compartido DENTRO del
 *      cuerpo JSON — Apps Script no expone headers HTTP personalizados,
 *      así que no puede ir como Authorization (ver apps-script/README.md).
 *
 * Nunca confía en nada que mande el navegador para decidir el token: lo
 * agrega este archivo, desde una variable de entorno, siempre.
 */

const GUIAS_VALIDAS = ['DOMINO', 'PLAN', 'HABLAR', 'ENTUSIASMO', 'RETIRO'];
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Por IP: máximo N envíos exitosos por ventana de M segundos. Generoso para
// una persona real (nadie manda su propio autodiagnóstico seis veces en un
// minuto) y restrictivo para un bot golpeando el endpoint.
const LIMITE_POR_VENTANA = 6;
const VENTANA_SEGUNDOS = 60;

export async function onRequestPost(context) {
  const { request, env } = context;

  const contentType = request.headers.get('content-type') || '';
  if (!contentType.includes('application/json')) {
    return jsonError_('tipo_de_contenido_invalido', 400);
  }

  let body;
  try {
    body = await request.json();
  } catch (err) {
    return jsonError_('payload_invalido', 400);
  }
  if (!body || typeof body !== 'object') {
    return jsonError_('payload_invalido', 400);
  }

  const ip = request.headers.get('CF-Connecting-IP') || 'sin-ip';
  if (await estaLimitada_(env, ip)) {
    return jsonError_('demasiadas_solicitudes', 429);
  }

  // Honeypot: campo de texto oculto en el formulario que una persona nunca
  // llena. Si trae algo, es casi seguro un bot — respondemos éxito igual
  // (para no delatar el filtro) pero no reenviamos nada a Apps Script.
  if (body.sitioWeb) {
    return jsonOk_({ recibido: true });
  }

  const validado = validarPayload_(body);
  if (!validado.ok) {
    return jsonError_(validado.error, 400);
  }

  if (!env.APPS_SCRIPT_URL || !env.SHARED_TOKEN) {
    return jsonError_('config_del_worker_incompleta', 500);
  }

  const payload = Object.assign({ token: env.SHARED_TOKEN }, validado.datos);

  let upstream;
  try {
    upstream = await fetch(env.APPS_SCRIPT_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  } catch (err) {
    return jsonError_('no_se_pudo_contactar_apps_script', 502);
  }

  let resultado = null;
  try {
    resultado = await upstream.json();
  } catch (err) {
    // Apps Script devolvió algo que no es JSON — probablemente la URL de
    // implementación quedó mal configurada (te devuelve una página de login).
  }

  if (!resultado || resultado.ok !== true) {
    return jsonError_('no_se_pudo_guardar', 502);
  }

  return jsonOk_({ recibido: true, uuid: resultado.uuid });
}

// Cualquier otro método explica el error en vez de devolver el 405 genérico
// de Pages, y documenta el endpoint para quien lo visite en el navegador.
export async function onRequestGet() {
  return new Response('Este endpoint solo acepta POST con un cuerpo JSON.', {
    status: 405,
    headers: { 'Content-Type': 'text/plain; charset=utf-8' }
  });
}

/* --------------------------------- Validación --------------------------------- */

function validarPayload_(body) {
  const email = normalizarEmail_(body.email);
  if (!email || !EMAIL_RE.test(email) || email.length > 254) {
    return { ok: false, error: 'email_invalido' };
  }

  let guia = String(body.guia || 'DOMINO').toUpperCase().slice(0, 30);
  if (!GUIAS_VALIDAS.includes(guia)) guia = 'DOMINO';

  const origen = String(body.origen || guia).toUpperCase().slice(0, 30);
  const versionTexto = String(body.versionTexto || '').slice(0, 100);
  const consentGuardado = body.consentGuardado === true;
  const consentMarketing = body.consentMarketing === true;

  const datos = {
    email: email,
    guia: guia,
    origen: origen,
    versionTexto: versionTexto,
    consentGuardado: consentGuardado,
    consentMarketing: consentMarketing,
    fecha: new Date().toISOString()
  };

  // totales/respuestas son propios del autodiagnóstico (guia=DOMINO); las
  // páginas de captura de PLAN/HABLAR/ENTUSIASMO (Etapa 6) solo mandan
  // correo + consentimientos, así que acá son opcionales.
  if (body.totales && typeof body.totales === 'object' && !Array.isArray(body.totales)) {
    const totales = {};
    for (const pilar of Object.keys(body.totales).slice(0, 10)) {
      const valor = Number(body.totales[pilar]);
      if (Number.isFinite(valor)) totales[String(pilar).slice(0, 30)] = valor;
    }
    datos.totales = totales;
  }

  if (Array.isArray(body.respuestas)) {
    datos.respuestas = body.respuestas
      .slice(0, 200) // ningún cuestionario real del sitio pasa de 25 preguntas
      .filter((r) => r && typeof r === 'object')
      .map((r) => ({
        pregunta: String(r.pregunta || '').slice(0, 500),
        pilar: String(r.pilar || '').slice(0, 30),
        valor: Number.isFinite(Number(r.valor)) ? Number(r.valor) : null
      }))
      .filter((r) => r.pilar && r.valor !== null);
  }

  return { ok: true, datos: datos };
}

function normalizarEmail_(v) {
  return String(v || '').trim().toLowerCase();
}

/* ------------------------------- Límite por IP -------------------------------- */

/**
 * Cuota de KV en el plan free: 1.000 escrituras/día — cada intento (pase o
 * no el límite) cuesta como mucho una escritura acá. Muy por encima del
 * volumen esperado; si algún día se acerca, hay que migrar a Durable
 * Objects o al binding nativo de Rate Limiting de Cloudflare.
 *
 * Falla abierto a propósito: si KV no está configurado o falla, la petición
 * sigue su curso en vez de bloquear a alguien real por un problema nuestro.
 * El límite por IP es defensa en profundidad, no el único control de abuso.
 */
async function estaLimitada_(env, ip) {
  if (!env.RATE_LIMIT_KV) return false;

  const bucket = Math.floor(Date.now() / 1000 / VENTANA_SEGUNDOS);
  const key = `rl:${ip}:${bucket}`;

  try {
    const actual = Number((await env.RATE_LIMIT_KV.get(key)) || '0');
    if (actual >= LIMITE_POR_VENTANA) return true;
    await env.RATE_LIMIT_KV.put(key, String(actual + 1), { expirationTtl: VENTANA_SEGUNDOS * 2 });
    return false;
  } catch (err) {
    return false;
  }
}

/* --------------------------------- Respuestas ---------------------------------- */

function jsonOk_(obj) {
  return new Response(JSON.stringify(Object.assign({ ok: true }, obj)), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  });
}

function jsonError_(error, status) {
  return new Response(JSON.stringify({ ok: false, error: error }), {
    status: status,
    headers: { 'Content-Type': 'application/json' }
  });
}
