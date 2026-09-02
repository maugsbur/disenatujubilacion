/**
 * Derechos de acceso, portabilidad y supresión (08-cumplimiento-datos.md §5).
 *
 * Pensado para que Nicole los use SIN abrir el editor de código: al abrir el
 * archivo "DTJ · Personas" aparece un menú "DTJ · Privacidad" con las tres
 * acciones. También se pueden llamar directamente desde el editor si hace
 * falta (borrarPersona('alguien@correo.com'), etc.).
 */

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('DTJ · Privacidad')
    .addItem('Buscar por correo…', 'menuBuscar_')
    .addItem('Exportar por correo…', 'menuExportar_')
    .addSeparator()
    .addItem('Eliminar por correo…', 'menuBorrar_')
    .addToUi();
}

/**
 * Junta todo lo asociado a un correo: la fila de Personas + todas las filas
 * de Respuestas (si las hay). No envía nada — solo devuelve los datos; el
 * envío a la persona lo hace quien atienda la solicitud, por su cuenta.
 *
 * @return {{persona: Object, respuestas: Array}}
 */
function buscarTodoPorCorreo(email) {
  email = normalizarEmail_(email);
  var encontrada = buscarPersonaPorEmail_(email);
  if (!encontrada) return null;
  var respuestas = buscarRespuestasPorUuid_(encontrada.datos.id);
  return { persona: encontrada.datos, respuestas: respuestas };
}

/**
 * Exportación para efectos de acceso y portabilidad: crea una planilla NUEVA
 * e independiente (no toca ni Personas ni Respuestas) con todo lo de esa
 * persona en texto plano, lista para bajar o reenviar. Bórrala una vez que
 * se la hayas mandado — es una copia temporal, no un tercer archivo permanente.
 *
 * @return {string} URL de la planilla creada
 */
function exportarPersona(email) {
  email = normalizarEmail_(email);
  var todo = buscarTodoPorCorreo(email);
  if (!todo) throw new Error('No se encontró a ' + email + ' en Personas.');

  var ss = SpreadsheetApp.create('DTJ - Exportación - ' + email + ' - ' + formatearFecha_(new Date()));
  var sh = ss.getSheets()[0];
  sh.setName('Datos de ' + email);

  sh.appendRow(['Campo', 'Valor']);
  Object.keys(todo.persona).forEach(function (k) { sh.appendRow([k, String(todo.persona[k])]); });

  if (todo.respuestas.length) {
    sh.appendRow([]);
    sh.appendRow(['Respuestas guardadas (' + todo.respuestas.length + ')']);
    sh.appendRow(['id', 'guia', 'pregunta', 'pilar', 'valor', 'total_pilar', 'fecha']);
    todo.respuestas.forEach(function (r) { sh.appendRow(r); });
  } else {
    sh.appendRow([]);
    sh.appendRow(['Esta persona no tiene respuestas guardadas (no marcó esa casilla, o no respondió el autodiagnóstico).']);
  }

  sh.autoResizeColumns(1, 7);
  registrarSolicitud_('exportacion', email, 'Exportado a ' + ss.getUrl());
  return ss.getUrl();
}

/**
 * Elimina a la persona de Personas y todas sus filas de Respuestas.
 * Deja constancia en la pestaña "solicitudes" pase lo que pase, incluso si
 * no se encontró a nadie (para poder demostrar que la solicitud se atendió).
 *
 * @return {{ok: boolean, filasBorradas: number, mensaje: string}}
 */
function borrarPersona(email) {
  email = normalizarEmail_(email);
  var encontrada = buscarPersonaPorEmail_(email);

  if (!encontrada) {
    registrarSolicitud_('borrado', email, 'No se encontró ninguna fila para este correo.');
    return { ok: false, filasBorradas: 0, mensaje: 'No se encontró a ' + email + '.' };
  }

  var uuid = encontrada.datos.id;
  personasSheet_().deleteRow(encontrada.fila);
  var respuestasBorradas = eliminarRespuestasPorUuid_(uuid);

  var mensaje = 'Eliminada 1 fila en personas y ' + respuestasBorradas + ' en respuestas (uuid ' + uuid + ').';
  registrarSolicitud_('borrado', email, mensaje);
  return { ok: true, filasBorradas: 1 + respuestasBorradas, mensaje: mensaje };
}

/* ---------------------- Menú: diálogos con la interfaz ---------------------- */

function menuBuscar_() {
  var ui = SpreadsheetApp.getUi();
  var resp = ui.prompt('Buscar por correo', 'Correo electrónico:', ui.ButtonSet.OK_CANCEL);
  if (resp.getSelectedButton() !== ui.Button.OK) return;

  var email = resp.getResponseText();
  var todo = buscarTodoPorCorreo(email);
  if (!todo) {
    ui.alert('No se encontró a ' + email + ' en Personas.');
    return;
  }
  var p = todo.persona;
  var resumen = [
    'Correo: ' + p.email,
    'Alta: ' + p.fecha_alta,
    'Origen: ' + p.origen,
    'Último contacto: ' + p.ultimo_contacto,
    'Consiente guardar respuestas: ' + (p.consent_guardado ? 'sí (' + p.consent_guardado_fecha + ')' : 'no'),
    'Consiente marketing: ' + (p.consent_marketing ? 'sí (' + p.consent_marketing_fecha + ')' : 'no'),
    'Versión de texto aceptada: ' + p.version_texto,
    '',
    'Respuestas guardadas: ' + todo.respuestas.length
  ].join('\n');
  ui.alert('Encontrado', resumen, ui.ButtonSet.OK);
}

function menuExportar_() {
  var ui = SpreadsheetApp.getUi();
  var resp = ui.prompt('Exportar por correo', 'Correo electrónico:', ui.ButtonSet.OK_CANCEL);
  if (resp.getSelectedButton() !== ui.Button.OK) return;

  try {
    var url = exportarPersona(resp.getResponseText());
    ui.alert('Listo', 'Se creó la exportación:\n' + url + '\n\nBórrala una vez que se la hayas enviado a la persona.', ui.ButtonSet.OK);
  } catch (err) {
    ui.alert('No se pudo exportar: ' + err.message);
  }
}

function menuBorrar_() {
  var ui = SpreadsheetApp.getUi();
  var resp = ui.prompt('Eliminar por correo', 'Correo electrónico:', ui.ButtonSet.OK_CANCEL);
  if (resp.getSelectedButton() !== ui.Button.OK) return;

  var email = normalizarEmail_(resp.getResponseText());
  var confirmar = ui.alert(
    'Confirmar eliminación',
    'Esto borra para siempre la fila de "' + email + '" en Personas y todas sus filas en Respuestas. No se puede deshacer.\n\n¿Continuar?',
    ui.ButtonSet.YES_NO
  );
  if (confirmar !== ui.Button.YES) return;

  var resultado = borrarPersona(email);
  ui.alert(resultado.mensaje);
}
