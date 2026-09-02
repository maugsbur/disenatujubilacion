/**
 * Configuración del proyecto — Apps Script "DTJ · Backend".
 *
 * Los valores reales NUNCA van escritos en el código (quedaría en git en texto
 * plano). Viven en las Propiedades del script, que no se exportan con clasp
 * ni se ven en el repo.
 *
 * Ejecuta configurarPropiedades() UNA vez desde el editor de Apps Script,
 * con tus valores reales reemplazando los placeholders, y después borra esa
 * ejecución del historial si quieres (los valores ya quedaron guardados).
 */

function configurarPropiedades() {
  PropertiesService.getScriptProperties().setProperties({
    PERSONAS_SHEET_ID: 'PEGAR_AQUI_EL_ID_DEL_ARCHIVO_DTJ_PERSONAS',
    RESPUESTAS_SHEET_ID: 'PEGAR_AQUI_EL_ID_DEL_ARCHIVO_DTJ_RESPUESTAS',
    SHARED_TOKEN: 'PEGAR_AQUI_UN_TOKEN_LARGO_Y_ALEATORIO',
    RETENCION_MESES: '18',
    // Misma llave de API que usa el Worker (Etapa 4) — solo para reintentar
    // los correos que Brevo rechazó la primera vez. Ver CorreoPendiente.gs.
    BREVO_API_KEY: 'PEGAR_AQUI_LA_MISMA_LLAVE_DE_BREVO_QUE_USA_EL_WORKER',
    ALERTA_EMAIL: 'disenatujubilacion@gmail.com'
  }, /* deleteAllOthers= */ true);
  Logger.log('Propiedades guardadas. Revísalas con revisarPropiedades().');
}

/** Útil para confirmar que quedó bien configurado, sin exponer secretos completos. */
function revisarPropiedades() {
  var cfg = getConfig_();
  Logger.log('PERSONAS_SHEET_ID: %s', cfg.PERSONAS_SHEET_ID || '(vacío)');
  Logger.log('RESPUESTAS_SHEET_ID: %s', cfg.RESPUESTAS_SHEET_ID || '(vacío)');
  Logger.log('SHARED_TOKEN: %s', cfg.SHARED_TOKEN ? (cfg.SHARED_TOKEN.slice(0, 4) + '…' + cfg.SHARED_TOKEN.length + ' caracteres') : '(vacío)');
  Logger.log('BREVO_API_KEY: %s', cfg.BREVO_API_KEY ? (cfg.BREVO_API_KEY.slice(0, 4) + '…' + cfg.BREVO_API_KEY.length + ' caracteres') : '(vacío)');
  Logger.log('ALERTA_EMAIL: %s', cfg.ALERTA_EMAIL);
  Logger.log('RETENCION_MESES: %s', cfg.RETENCION_MESES);
}

function getConfig_() {
  var p = PropertiesService.getScriptProperties();
  return {
    PERSONAS_SHEET_ID: p.getProperty('PERSONAS_SHEET_ID'),
    RESPUESTAS_SHEET_ID: p.getProperty('RESPUESTAS_SHEET_ID'),
    SHARED_TOKEN: p.getProperty('SHARED_TOKEN'),
    BREVO_API_KEY: p.getProperty('BREVO_API_KEY'),
    ALERTA_EMAIL: p.getProperty('ALERTA_EMAIL') || 'disenatujubilacion@gmail.com',
    RETENCION_MESES: Number(p.getProperty('RETENCION_MESES') || 18)
  };
}
