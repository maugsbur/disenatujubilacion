/** Utilidades compartidas por el resto de los archivos. */

function jsonResponse_(obj) {
  // Apps Script Web Apps no permiten fijar el código de estado HTTP: siempre
  // responden 200. El estado real del intento va en el campo "ok" del cuerpo,
  // y quien llama (el Worker) decide qué código HTTP mostrarle al navegador.
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function normalizarEmail_(v) {
  return String(v || '').trim().toLowerCase();
}

function validarEmail_(v) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
}

/** {id:0, email:1, ...} a partir de la fila de encabezados, para no depender
 *  de índices numéricos fijos si alguien reordena columnas. */
function colIndex_(header) {
  var idx = {};
  header.forEach(function (nombre, i) { idx[String(nombre).trim()] = i; });
  return idx;
}

function formatearFecha_(d) {
  var tz = Session.getScriptTimeZone() || 'America/Santiago';
  return Utilities.formatDate(d, tz, 'yyyy-MM-dd_HHmm');
}

function personasSheet_() {
  var cfg = getConfig_();
  if (!cfg.PERSONAS_SHEET_ID) throw new Error('Falta PERSONAS_SHEET_ID — corre configurarPropiedades() primero.');
  var sheet = SpreadsheetApp.openById(cfg.PERSONAS_SHEET_ID).getSheetByName('personas');
  if (!sheet) throw new Error('El archivo de Personas no tiene una pestaña llamada "personas".');
  return sheet;
}

function respuestasSheet_() {
  var cfg = getConfig_();
  if (!cfg.RESPUESTAS_SHEET_ID) throw new Error('Falta RESPUESTAS_SHEET_ID — corre configurarPropiedades() primero.');
  var sheet = SpreadsheetApp.openById(cfg.RESPUESTAS_SHEET_ID).getSheetByName('respuestas');
  if (!sheet) throw new Error('El archivo de Respuestas no tiene una pestaña llamada "respuestas".');
  return sheet;
}

/** Busca una persona por correo. Devuelve {fila, datos} o null. `fila` es
 *  1-based y lista para usar con sheet.deleteRow(fila) / getRange(fila, ...). */
function buscarPersonaPorEmail_(email) {
  var sheet = personasSheet_();
  var data = sheet.getDataRange().getValues();
  var header = data[0];
  var col = colIndex_(header);
  for (var r = 1; r < data.length; r++) {
    if (String(data[r][col.email]).toLowerCase() === email) {
      var datos = {};
      header.forEach(function (h, i) { datos[h] = data[r][i]; });
      return { fila: r + 1, datos: datos };
    }
  }
  return null;
}

function buscarRespuestasPorUuid_(uuid) {
  var sheet = respuestasSheet_();
  var data = sheet.getDataRange().getValues();
  var out = [];
  for (var r = 1; r < data.length; r++) {
    if (data[r][0] === uuid) out.push(data[r]);
  }
  return out;
}

function eliminarRespuestasPorUuid_(uuid) {
  var sheet = respuestasSheet_();
  var data = sheet.getDataRange().getValues();
  var borrados = 0;
  // De abajo hacia arriba: borrar una fila corre los índices de las que
  // quedan más abajo, y ya las recorrimos.
  for (var r = data.length - 1; r >= 1; r--) {
    if (data[r][0] === uuid) {
      sheet.deleteRow(r + 1);
      borrados++;
    }
  }
  return borrados;
}

/** Deja constancia de cada solicitud de derechos ARCO, en una tercera pestaña
 *  dentro del archivo de Personas (no del de Respuestas: es un registro
 *  administrativo, no un dato de la persona en sí, y así no hace falta un
 *  tercer archivo). Ver 08-cumplimiento-datos.md §5. */
function registrarSolicitud_(tipo, email, resultado) {
  var cfg = getConfig_();
  var ss = SpreadsheetApp.openById(cfg.PERSONAS_SHEET_ID);
  var sheet = ss.getSheetByName('solicitudes') || crearHojaSolicitudes_(ss);
  sheet.appendRow([new Date(), tipo, email, resultado]);
}

function crearHojaSolicitudes_(ss) {
  var sheet = ss.insertSheet('solicitudes');
  sheet.appendRow(['fecha', 'tipo', 'email', 'resultado']);
  sheet.setFrozenRows(1);
  return sheet;
}
