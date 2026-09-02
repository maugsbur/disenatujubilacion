/**
 * "DTJ · Respuestas" — sin correos, unida a Personas solo por uuid.
 *
 * Encabezados esperados en la fila 1 de la pestaña "respuestas":
 * id | guia | pregunta | pilar | valor | total_pilar | fecha
 *
 * (id = el mismo uuid que en Personas, no un id propio de esta tabla.)
 */

/**
 * Escribe una fila por cada pregunta respondida. Solo se llama cuando la
 * persona marcó la casilla de "guardar mis respuestas" — si no, esta función
 * ni se invoca y no queda ningún rastro de las respuestas, en ningún lado.
 *
 * @param {string} uuid
 * @param {string} guia p.ej. "DOMINO"
 * @param {Array<{pregunta:string, pilar:string, valor:number}>} respuestas
 * @param {Object<string,number>} totales p.ej. {proposito: 18, fisico: 12, ...}
 * @param {Date} fecha
 * @return {number} filas escritas
 */
function escribirRespuestas_(uuid, guia, respuestas, totales, fecha) {
  var sheet = respuestasSheet_();

  var filas = respuestas
    .filter(function (r) { return r && r.pilar && r.valor != null; })
    .slice(0, 200) // tope defensivo — el Worker es la validación real (Etapa 4)
    .map(function (r) {
      var totalPilar = totales && totales[r.pilar] != null ? totales[r.pilar] : '';
      var pregunta = String(r.pregunta || '').slice(0, 500);
      return [uuid, guia, pregunta, r.pilar, r.valor, totalPilar, fecha];
    });

  if (filas.length) {
    sheet.getRange(sheet.getLastRow() + 1, 1, filas.length, 7).setValues(filas);
  }
  return filas.length;
}
