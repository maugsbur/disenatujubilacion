/**
 * Cola de reintento de correos — decisión de Marcel del 2026-09-02: "cola
 * con reintento, nunca perder la solicitud" en vez de fallar en silencio.
 *
 * Cómo llega acá un correo: el Worker (functions/api/submit.js) intenta
 * enviar con Brevo primero. Si falla, manda el mismo cuerpo que le iba a
 * pasar a Brevo dentro del payload normal de doPost, en `correoPendiente`.
 * Codigo.gs lo detecta y llama a registrarCorreoPendiente_().
 *
 * El reintento (reintentarCorreosPendientes) NO necesita saber nada sobre
 * guías, plantillas ni PDF: solo vuelve a mandar exactamente el mismo
 * cuerpo JSON a la API de Brevo. Toda esa lógica vive en un solo lugar
 * (el Worker) — acá solo se repite el intento.
 *
 * Encabezados de la pestaña "correos_pendientes" (vive en el archivo de
 * Personas, igual que "solicitudes" — es un registro operativo, no un dato
 * de la persona en sí):
 * fecha_primera_falla | email | guia | cuerpo_brevo_json | intentos | ultimo_error | estado
 *
 * estado: "pendiente" → "enviado" | "fallido_definitivo" | "error_datos"
 */

function registrarCorreoPendiente_(email, guia, cuerpoBrevo, motivo) {
  var sheet = correosPendientesSheet_();
  sheet.appendRow([
    new Date(),
    email,
    guia,
    JSON.stringify(cuerpoBrevo || {}),
    0,
    String(motivo || '').slice(0, 200),
    'pendiente'
  ]);
}

/**
 * Instala el disparador UNA vez desde el editor. Reintenta cada 30 minutos
 * — bastante seguido para que una falla transitoria (Brevo caído un rato)
 * se resuelva sola rápido, sin ser tan seguido como para gastar la cuota de
 * runtime diario de Apps Script en cuentas de consumo (90 min/día).
 */
function instalarTriggerReintentoCorreos() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'reintentarCorreosPendientes') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('reintentarCorreosPendientes').timeBased().everyMinutes(30).create();
  Logger.log('Disparador de reintento de correos instalado: cada 30 minutos.');
}

/**
 * Reintenta cada fila "pendiente". Si una fila lleva más de 24 horas
 * fallando (le da tiempo de sobra a que se resetee una cuota diaria de
 * Brevo topada), deja de reintentarla y junta una alerta para el equipo en
 * vez de seguir gastando cuota en algo que probablemente necesita que
 * alguien mire — no seguimos reintentando para siempre en silencio.
 */
function reintentarCorreosPendientes() {
  var cfg = getConfig_();
  if (!cfg.BREVO_API_KEY) {
    Logger.log('Falta BREVO_API_KEY en las propiedades del script — no se puede reintentar nada.');
    return;
  }

  var sheet = correosPendientesSheet_();
  var data = sheet.getDataRange().getValues();
  var header = data[0];
  var col = colIndex_(header);
  var alertas = [];
  var reintentados = 0;

  for (var r = 1; r < data.length; r++) {
    if (data[r][col.estado] !== 'pendiente') continue;
    reintentados++;

    var fila = r + 1;
    var cuerpo;
    try {
      cuerpo = JSON.parse(data[r][col.cuerpo_brevo_json]);
    } catch (err) {
      sheet.getRange(fila, col.estado + 1).setValue('error_datos');
      sheet.getRange(fila, col.ultimo_error + 1).setValue('cuerpo_brevo_json no es JSON válido');
      continue;
    }

    var resultado = enviarBrevo_(cfg.BREVO_API_KEY, cuerpo);
    var intentos = Number(data[r][col.intentos] || 0) + 1;
    sheet.getRange(fila, col.intentos + 1).setValue(intentos);

    if (resultado.enviado) {
      sheet.getRange(fila, col.estado + 1).setValue('enviado');
      sheet.getRange(fila, col.ultimo_error + 1).setValue('');
      continue;
    }

    sheet.getRange(fila, col.ultimo_error + 1).setValue(String(resultado.motivo || '').slice(0, 200));

    var primeraFalla = new Date(data[r][col.fecha_primera_falla]);
    var horasPendiente = (new Date() - primeraFalla) / 36e5;
    if (horasPendiente > 24) {
      sheet.getRange(fila, col.estado + 1).setValue('fallido_definitivo');
      alertas.push(data[r][col.email] + ' (' + data[r][col.guia] + '): ' + resultado.motivo + ', ' + intentos + ' intentos en ' + Math.round(horasPendiente) + 'h');
    }
  }

  Logger.log('Reintento de correos: %s pendientes procesados, %s pasaron a fallido_definitivo.', reintentados, alertas.length);
  if (alertas.length) avisarAlEquipo_(cfg.ALERTA_EMAIL, alertas);
}

function enviarBrevo_(apiKey, cuerpo) {
  try {
    var resp = UrlFetchApp.fetch('https://api.brevo.com/v3/smtp/email', {
      method: 'post',
      contentType: 'application/json',
      headers: { 'api-key': apiKey, accept: 'application/json' },
      payload: JSON.stringify(cuerpo),
      muteHttpExceptions: true
    });
    var codigo = resp.getResponseCode();
    if (codigo >= 200 && codigo < 300) return { enviado: true };
    return { enviado: false, motivo: 'brevo_' + codigo + ': ' + resp.getContentText().slice(0, 150) };
  } catch (err) {
    return { enviado: false, motivo: 'excepcion: ' + err.message };
  }
}

function avisarAlEquipo_(destinatario, alertas) {
  MailApp.sendEmail({
    to: destinatario,
    subject: 'DTJ — ' + alertas.length + ' correo(s) sin poder enviarse en 24 horas',
    body:
      'Estos envíos llevan más de 24 horas fallando y se dejó de reintentar ' +
      '(probablemente se topó la cuota diaria de Brevo, o hay un problema de ' +
      'configuración — revisa BREVO_API_KEY y los IDs de plantilla):\n\n' +
      alertas.join('\n') +
      '\n\nDetalle completo en la pestaña "correos_pendientes" del archivo DTJ · Personas.'
  });
}

function correosPendientesSheet_() {
  var cfg = getConfig_();
  var ss = SpreadsheetApp.openById(cfg.PERSONAS_SHEET_ID);
  return ss.getSheetByName('correos_pendientes') || crearHojaCorreosPendientes_(ss);
}

function crearHojaCorreosPendientes_(ss) {
  var sheet = ss.insertSheet('correos_pendientes');
  sheet.appendRow(['fecha_primera_falla', 'email', 'guia', 'cuerpo_brevo_json', 'intentos', 'ultimo_error', 'estado']);
  sheet.setFrozenRows(1);
  return sheet;
}
