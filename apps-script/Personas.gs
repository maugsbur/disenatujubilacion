/**
 * "DTJ · Personas" — una fila por correo, nunca una fila por envío.
 *
 * Encabezados esperados en la fila 1 de la pestaña "personas":
 * id | email | fecha_alta | origen | consent_guardado | consent_guardado_fecha |
 * consent_marketing | consent_marketing_fecha | version_texto | ultimo_contacto
 */

/**
 * Crea o actualiza la fila de una persona.
 * - Si el correo no existe: crea la fila, genera el uuid acá (nunca confía
 *   en el uuid que mande el navegador — ese es solo un identificador de
 *   envío, la identidad la decide este archivo, por correo).
 * - Si el correo ya existe: reutiliza el mismo uuid, actualiza
 *   ultimo_contacto, y sube el consentimiento a "sí" si ahora lo dieron
 *   (nunca lo baja solo — revocar consentimiento es un flujo aparte,
 *   ver borrarPersona). El origen del primer contacto NUNCA se sobrescribe.
 *
 * @return {{id: string, esNueva: boolean}}
 */
function upsertPersona_(datos) {
  var sheet = personasSheet_();
  var data = sheet.getDataRange().getValues();
  var header = data[0];
  var col = colIndex_(header);

  for (var r = 1; r < data.length; r++) {
    if (String(data[r][col.email]).toLowerCase() !== datos.email) continue;

    var fila = r + 1;
    var id = data[r][col.id];

    sheet.getRange(fila, col.ultimo_contacto + 1).setValue(datos.fecha);
    sheet.getRange(fila, col.version_texto + 1).setValue(datos.versionTexto);

    if (datos.consentGuardado && data[r][col.consent_guardado] !== true) {
      sheet.getRange(fila, col.consent_guardado + 1).setValue(true);
      sheet.getRange(fila, col.consent_guardado_fecha + 1).setValue(datos.fecha);
    }
    if (datos.consentMarketing && data[r][col.consent_marketing] !== true) {
      sheet.getRange(fila, col.consent_marketing + 1).setValue(true);
      sheet.getRange(fila, col.consent_marketing_fecha + 1).setValue(datos.fecha);
    }

    return { id: id, esNueva: false };
  }

  var nuevoId = Utilities.getUuid();
  sheet.appendRow([
    nuevoId,
    datos.email,
    datos.fecha,
    datos.origen,
    datos.consentGuardado,
    datos.consentGuardado ? datos.fecha : '',
    datos.consentMarketing,
    datos.consentMarketing ? datos.fecha : '',
    datos.versionTexto,
    datos.fecha
  ]);
  return { id: nuevoId, esNueva: true };
}
