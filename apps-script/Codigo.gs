/**
 * Punto de entrada del Web App. Lo llama el Worker de Cloudflare (Etapa 4),
 * nunca el navegador directamente.
 *
 * IMPORTANTE — límite real de Apps Script: un Web App no puede leer headers
 * HTTP personalizados (no existe e.headers). El token compartido viaja
 * DENTRO del cuerpo JSON, como el campo "token" — no como Authorization.
 * Esto lo tiene que respetar el Worker cuando reenvíe la petición.
 *
 * Comportamiento de las dos casillas (08-cumplimiento-datos.md §3):
 *   - Ninguna casilla:      se guarda correo + fecha + origen. Nada más.
 *   - Solo "guardar":       además se guardan las respuestas.
 *   - Solo "marketing":     solo cambia el consentimiento; no se guardan respuestas.
 *   - Ambas:                las dos cosas.
 * Eso se traduce acá en una sola regla: las respuestas SOLO se escriben si
 * consentGuardado === true. El consentimiento de marketing no habilita ni
 * bloquea el guardado de respuestas — son independientes, a propósito.
 *
 * Correo (Etapa 5): el Worker ya intentó mandarlo con Brevo antes de llamar
 * acá. Si falló, el mismo payload trae `correoEnviado:false` y
 * `correoPendiente` con el cuerpo exacto que se le iba a mandar a Brevo —
 * esta función solo lo deja en la cola de reintento (CorreoPendiente.gs),
 * no vuelve a intentar el envío ella misma.
 */
function doPost(e) {
  var cfg = getConfig_();
  var body;

  try {
    body = JSON.parse(e.postData.contents);
  } catch (err) {
    return jsonResponse_({ ok: false, error: 'payload_invalido' });
  }

  if (!cfg.SHARED_TOKEN || body.token !== cfg.SHARED_TOKEN) {
    return jsonResponse_({ ok: false, error: 'token_invalido' });
  }

  // Honeypot: si vino con contenido, es casi seguro un bot. No es un error
  // de la persona real, así que respondemos "ok" para no delatar el filtro,
  // pero no escribimos nada.
  if (body.sitioWeb) {
    return jsonResponse_({ ok: true, guardado: false, motivo: 'honeypot' });
  }

  var email = normalizarEmail_(body.email);
  if (!email || !validarEmail_(email)) {
    return jsonResponse_({ ok: false, error: 'email_invalido' });
  }

  var guia = String(body.guia || 'DOMINO').toUpperCase().slice(0, 30);
  var origen = String(body.origen || guia).toUpperCase().slice(0, 30);
  var consentGuardado = body.consentGuardado === true;
  var consentMarketing = body.consentMarketing === true;
  var versionTexto = String(body.versionTexto || '').slice(0, 100);
  var ahora = new Date();

  // Todo lo que sigue toca las planillas (SpreadsheetApp.openById) y puede
  // fallar por una razón de configuración (un ID mal copiado, una pestaña
  // que no se llama exactamente "personas"/"respuestas"...). Sin este
  // try/catch, esa excepción tumba toda la respuesta y Apps Script termina
  // devolviendo una página de error de Google Drive genérica en vez del
  // error real — pasó exactamente eso la primera vez que se probó esto en
  // producción. Con el catch, el error queda legible en el cuerpo JSON y,
  // sobre todo, en el registro de ejecuciones del editor.
  try {
    var persona = upsertPersona_({
      email: email,
      origen: origen,
      consentGuardado: consentGuardado,
      consentMarketing: consentMarketing,
      versionTexto: versionTexto,
      fecha: ahora
    });

    var respuestasGuardadas = 0;
    if (consentGuardado && Array.isArray(body.respuestas) && body.respuestas.length) {
      respuestasGuardadas = escribirRespuestas_(persona.id, guia, body.respuestas, body.totales || {}, ahora);
    }

    var correoEnviado = body.correoEnviado !== false; // por defecto true: no todo llamador informa este campo
    if (!correoEnviado && body.correoPendiente) {
      registrarCorreoPendiente_(email, guia, body.correoPendiente.cuerpoBrevo, body.correoPendiente.motivo);
    }

    return jsonResponse_({
      ok: true,
      uuid: persona.id,
      personaNueva: persona.esNueva,
      respuestasGuardadas: respuestasGuardadas
    });
  } catch (err) {
    Logger.log('Error en doPost: %s', err.message);
    return jsonResponse_({ ok: false, error: 'error_interno', detalle: err.message });
  }
}

/** Solo para confirmar manualmente que el deploy está vivo — abre la URL del
 *  Web App en el navegador y deberías ver este mensaje. */
function doGet(e) {
  return ContentService.createTextOutput('DTJ Apps Script activo. Este endpoint solo acepta POST.');
}
