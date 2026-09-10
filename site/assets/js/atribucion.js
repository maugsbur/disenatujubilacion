/* atribucion.js — de dónde vino la persona. Compartido por
 * autodiagnostico.js y captura.js.
 *
 * ⚠️ Mantener en UN solo lugar. Si esta lógica se duplica y diverge, la
 * atribución del funnel se rompe — ya pasó con el campo `origen`, que
 * significaba una cosa en el autodiagnóstico y otra en las capturas.
 * Ver specs/contrato-datos.md.
 *
 * Los tres campos que produce, alineados con los parámetros UTM que
 * Instagram Ads pone en los enlaces:
 *   origen    ← utm_source    (instagram, un reel puntual, un ad…)
 *   campana   ← utm_campaign  (la campaña pagada)
 *   contenido ← utm_content   (la pieza específica: reel-jinetes, historia-3…)
 */
(function () {
  'use strict';

  function limpio(v) {
    return String(v || '').trim().slice(0, 80);
  }

  window.dtjAtribucion = function () {
    var p = new URLSearchParams(location.search);
    var origen = limpio(p.get('utm_source'));

    if (!origen) {
      // Sin UTM: distinguir "llegó desde otra página nuestra" de "llegó de
      // afuera sin marcar". Útil para no contar la navegación interna como
      // tráfico nuevo.
      try {
        origen = document.referrer && document.referrer.indexOf(location.origin) === 0
          ? 'sitio-interno'
          : 'directo';
      } catch (e) {
        origen = 'directo';
      }
    }

    return {
      origen: origen,
      campana: limpio(p.get('utm_campaign')),
      contenido: limpio(p.get('utm_content'))
    };
  };
})();
