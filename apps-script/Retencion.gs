/**
 * Retención a 18 meses (08-cumplimiento-datos.md §5). Corre sola una vez al
 * mes: instálala UNA vez ejecutando instalarTriggerRetencion() desde el
 * editor. Volver a ejecutarlo no duplica el disparador (borra el anterior
 * antes de crear uno nuevo).
 */

function instalarTriggerRetencion() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'limpiarRetencion18Meses') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('limpiarRetencion18Meses').timeBased().onMonthDay(1).atHour(4).create();
  Logger.log('Disparador de retención instalado: corre el día 1 de cada mes, cerca de las 04:00.');
}

/**
 * Elimina (no anonimiza) a quien lleve más de RETENCION_MESES sin contacto.
 * "Sin contacto" = ultimo_contacto no se movió, es decir no volvió a
 * completar ninguna guía ni se le actualizó el consentimiento.
 *
 * Se podría anonimizar en vez de borrar (dejar la fila sin email, con un
 * hash), pero como Respuestas no tiene email y ya se borra por uuid al
 * mismo tiempo, no queda ningún beneficio real en conservar la fila de
 * Personas vacía — por eso se borra directo.
 */
function limpiarRetencion18Meses() {
  var cfg = getConfig_();
  var limite = new Date();
  limite.setMonth(limite.getMonth() - cfg.RETENCION_MESES);

  var sheet = personasSheet_();
  var data = sheet.getDataRange().getValues();
  var header = data[0];
  var col = colIndex_(header);
  var eliminados = 0;

  for (var r = data.length - 1; r >= 1; r--) {
    var ultimoContacto = data[r][col.ultimo_contacto];
    if (!ultimoContacto || !(new Date(ultimoContacto) < limite)) continue;

    var uuid = data[r][col.id];
    var email = data[r][col.email];
    var respuestasBorradas = eliminarRespuestasPorUuid_(uuid);
    sheet.deleteRow(r + 1);
    registrarSolicitud_(
      'retencion_automatica',
      email,
      'Eliminado por superar ' + cfg.RETENCION_MESES + ' meses sin contacto (uuid ' + uuid + ', ' + respuestasBorradas + ' filas de respuestas)'
    );
    eliminados++;
  }

  Logger.log('Retención: %s personas eliminadas.', eliminados);
  return eliminados;
}
