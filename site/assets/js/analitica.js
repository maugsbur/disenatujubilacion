/* analitica.js — PostHog + Meta Pixel, cargados en runtime desde /api/config.
 *
 * No-op sin llaves: si /api/config devuelve todo vacío (o falla), este
 * archivo no hace nada y el sitio funciona igual. Así se puede desplegar
 * antes de tener las cuentas, y activar después solo cargando las
 * variables en wrangler.toml. Ver specs/analitica.md.
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
    // Meta: solo eventos estándar mapeados; el resto se ignora para no
    // ensuciar el pixel.
    if (window.fbq) {
      var meta = { guia_solicitada: 'Lead', autodiagnostico_enviado: 'Lead', cta_calendly: 'Schedule' }[nombre];
      if (meta) window.fbq('track', meta);
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
      capture_pageview: true,
      autocapture: false, // eventos explícitos, no todo clic
      loaded: drenarCola
    });
  }

  function cargarMetaPixel(id) {
    !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments) }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s) }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', id);
    window.fbq('track', 'PageView');
  }

  fetch('/api/config')
    .then(function (r) { return r.json(); })
    .then(function (cfg) {
      if (cfg.posthogKey) cargarPostHog(cfg.posthogKey, cfg.posthogHost || 'https://us.i.posthog.com');
      else listo = true; // sin PostHog: los eventos encolados se descartan, sin ruido
      if (cfg.metaPixelId) cargarMetaPixel(cfg.metaPixelId);
    })
    .catch(function () { listo = true; });

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
