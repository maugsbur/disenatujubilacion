/* analitica.js — PostHog, cargado en runtime desde /api/config.
 *
 * No-op en producción sin configuración: si /api/config no devuelve las
 * variables, este archivo no carga el SDK y el sitio sigue funcionando. En
 * desarrollo informa el problema para evitar perder eventos silenciosamente.
 * Ver specs/analitica.md.
 *
 * Sin Meta Pixel: los ads de Instagram no llevan al sitio (el funnel de
 * venta es Instagram mismo), así que el pixel no tendría nada que
 * optimizar. Si más adelante se hace retargeting, ver specs/analitica.md.
 *
 * Reglas de eventos (aprendidas del repo jubilarme-landing-hijos):
 *   - Nombres estables y aburridos. No se renombran.
 *   - Nunca PII en las propiedades. Ni el correo, ni nombres, ni respuestas.
 *   - Primero los cambios de estado del funnel y las acciones de alta
 *     intención. Un evento nuevo solo si hay una pregunta real detrás.
 *   - PostHog captura los pageviews solo. No los simulamos a mano.
 */
(function () {
  'use strict';

  var cola = []; // eventos disparados antes de que PostHog termine de cargar
  var listo = false;

  // API pública, disponible desde el primer momento aunque PostHog aún no cargue.
  window.dtjEvento = function (nombre, props) {
    props = props || {};
    if (listo && window.posthog) {
      window.posthog.capture(nombre, props);
    } else {
      cola.push([nombre, props]);
    }
  };

  function drenarCola() {
    listo = true;
    if (!window.posthog) return;
    cola.forEach(function (e) { window.posthog.capture(e[0], e[1]); });
    cola = [];
  }

  function cargarPostHog(key, host) {
    // Snippet oficial de PostHog, recortado. `host` permite apuntar a un
    // proxy inverso propio para esquivar bloqueadores (ver specs/analitica.md).
    !function (t, e) { var o, n, p, r; e.__SV || (window.posthog = e, e._i = [], e.init = function (i, s, a) { function g(t, e) { var o = e.split("."); 2 == o.length && (t = t[o[0]], e = o[1]), t[e] = function () { t.push([e].concat(Array.prototype.slice.call(arguments, 0))) } } (p = t.createElement("script")).type = "text/javascript", p.async = !0, p.src = s.api_host + "/static/array.js", (r = t.getElementsByTagName("script")[0]).parentNode.insertBefore(p, r); var u = e; for (void 0 !== a ? u = e[a] = [] : a = "posthog", u.people = u.people || [], u.toString = function (t) { var e = "posthog"; return "posthog" !== a && (e += "." + a), t || (e += " (stub)"), e }, u.people.toString = function () { return u.toString(1) + ".people (stub)" }, o = "capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys onSessionId".split(" "), n = 0; n < o.length; n++) g(u, o[n]); e._i.push([i, s, a]) }, e.__SV = 1) }(document, window.posthog || []);

    window.posthog.init(key, {
      api_host: host,
      person_profiles: 'identified_only',
      defaults: '2026-05-30',
      capture_pageview: true,
      autocapture: false, // eventos explícitos, no todo clic — ver "Reglas de eventos" arriba
      capture_exceptions: {
        capture_unhandled_errors: true,
        capture_unhandled_rejections: true,
        capture_console_errors: false
      },
      loaded: drenarCola
    });
  }

  function faltaConfiguracion(nombre) {
    listo = true;
    if (location.hostname === 'localhost' || location.hostname === '127.0.0.1') {
      throw new Error(nombre + ' variable required by PostHog is missing or un-configured, this causes events to be silently missed. This error stops appearing once ' + nombre + ' is configured');
    }
  }

  fetch('/api/config')
    .then(function (r) { return r.json(); })
    .then(function (cfg) {
      if (!cfg || !cfg.posthogKey) return faltaConfiguracion('POSTHOG_PROJECT_TOKEN');
      if (!cfg.posthogHost) return faltaConfiguracion('POSTHOG_HOST');
      cargarPostHog(cfg.posthogKey, cfg.posthogHost);
    })
    .catch(function (error) {
      if (location.hostname === 'localhost' || location.hostname === '127.0.0.1') throw error;
      listo = true;
    });

  // Clics de CTA: se instrumentan acá para no repetir el listener en cada
  // página. Los enlaces abren en pestaña nueva, así que no hay carrera con
  // la navegación.
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.indexOf('calendly.com') !== -1) {
      window.dtjEvento('cta_calendly', { ubicacion: location.pathname });
    } else if (href.indexOf('wa.me') !== -1) {
      window.dtjEvento('cta_whatsapp', { ubicacion: location.pathname });
    }
  }, true);
})();
