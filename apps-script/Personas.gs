/**
 * "DTJ · Personas" — una fila por correo, nunca una fila por envío.
 *
 * Encabezados de la pestaña "personas". El orden NO importa: todo lo que
 * hace este archivo se guía por el nombre de columna. Agregar columnas
 * nuevas (como campana/contenido/regimen) no rompe nada aunque el código
 * todavía no las produzca, y viceversa.
 *
 *   id · email · fecha_alta · origen · campana · contenido · regimen ·
 *   consent_guardado · consent_guardado_fecha ·
 *   consent_marketing · consent_marketing_fecha · version_texto · ultimo_contacto
 *
 * campana/contenido: utm_campaign y utm_content, para distinguir qué pieza
 * de Instagram trajo a la persona. regimen: bajo qué régimen de
 * consentimiento se captó (PRE_LEY / LEY_21719) — ver specs/consentimiento.md.
 */

/**
 * Crea o actualiza la fila de una persona.
 * - Correo nuevo: crea la fila y genera el uuid acá (nunca confía en el que
 *   mande el navegador — ese es un id de envío, no de identidad).
 * - Correo que ya existe: reutiliza el uuid, actualiza ultimo_contacto y
 *   version_texto, sube el consentimiento si ahora lo dieron (nunca lo baja
 *   solo). origen/campana/contenido del primer contacto NO se sobrescriben
 *   — es atribución de adquisición, no de última interacción.
 *
 * @return {{id: string, esNueva: boolean}}
 */
function upsertPersona_(datos) {
  var sheet = personasSheet_();
  var data = sheet.getDataRange().getValues();
  var header = data[0];
  var col = colIndex_(header);

  // Todo lo que sabemos escribir, por nombre de columna.
  var valores = {
    email: datos.email,
    fecha_alta: datos.fecha,
    origen: datos.origen,
    campana: datos.campana || '',
    contenido: datos.contenido || '',
    regimen: datos.regimen || '',
    version_texto: datos.versionTexto,
    ultimo_contacto: datos.fecha,
    consent_guardado: datos.consentGuardado,
    consent_guardado_fecha: datos.consentGuardado ? datos.fecha : '',
    consent_marketing: datos.consentMarketing,
    consent_marketing_fecha: datos.consentMarketing ? datos.fecha : ''
  };

  for (var r = 1; r < data.length; r++) {
    if (String(data[r][col.email]).toLowerCase() !== datos.email) continue;

    var fila = r + 1;
    var id = data[r][col.id];

    escribirCelda_(sheet, fila, col, 'ultimo_contacto', datos.fecha);
    escribirCelda_(sheet, fila, col, 'version_texto', datos.versionTexto);
    if (datos.regimen) escribirCelda_(sheet, fila, col, 'regimen', datos.regimen);

    if (datos.consentGuardado && data[r][col.consent_guardado] !== true) {
      escribirCelda_(sheet, fila, col, 'consent_guardado', true);
      escribirCelda_(sheet, fila, col, 'consent_guardado_fecha', datos.fecha);
    }
    if (datos.consentMarketing && data[r][col.consent_marketing] !== true) {
      escribirCelda_(sheet, fila, col, 'consent_marketing', true);
      escribirCelda_(sheet, fila, col, 'consent_marketing_fecha', datos.fecha);
    }

    return { id: id, esNueva: false };
  }

  // Fila nueva: un arreglo del largo del encabezado, cada valor en la
  // posición de su columna. Si la planilla no tiene una columna que sí
  // producimos, se avisa por log y se sigue — la persona igual queda
  // guardada con los campos que sí caben.
  var nuevoId = Utilities.getUuid();
  var filaNueva = [];
  for (var i = 0; i < header.length; i++) filaNueva.push('');
  filaNueva[col.id] = nuevoId;
  Object.keys(valores).forEach(function (nombre) {
    if (col[nombre] != null) filaNueva[col[nombre]] = valores[nombre];
    else Logger.log('Personas: la planilla no tiene columna "%s" — ese valor no se guardó', nombre);
  });
  sheet.appendRow(filaNueva);
  return { id: nuevoId, esNueva: true };
}

function escribirCelda_(sheet, fila, col, nombre, valor) {
  if (col[nombre] == null) {
    Logger.log('Personas: falta la columna "%s", no se escribió esa celda', nombre);
    return;
  }
  sheet.getRange(fila, col[nombre] + 1).setValue(valor);
}
