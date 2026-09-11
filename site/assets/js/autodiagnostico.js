/* Autodiagnóstico de los 5 pilares — Diseña tu Jubilación
 * Una sola página, dos vistas. El cálculo ocurre acá, en el navegador:
 * el resultado se muestra aunque el envío a /api/submit falle.
 */
(function () {
  'use strict';

  var TOTAL_QUESTIONS = 25;
  var STORAGE_KEY = 'dtj_autodiagnostico_resultado_v1';
  var SUBMIT_ENDPOINT = '/api/submit';
  // Enlace de la llamada de Margarita. Al mostrar el resultado le precargamos
  // el correo y un resumen del autodiagnóstico (los cinco puntajes + el pilar
  // más bajo). Así el correo de confirmación de cada reserva ya trae con quién
  // va a hablar y por dónde. El resumen viaja en a1: la respuesta a la primera
  // pregunta personalizada del tipo de evento en Calendly — si Margarita aún
  // no la creó, Calendly ignora el parámetro sin romper nada. Ver
  // specs/contrato-datos.md § "La llamada de Margarita".
  var CALENDLY_BASE = 'https://calendly.com/margarita-disenatujubilacion/45min';
  var RESULT_PATH = '/autodiagnostico/resultado';
  var QUESTIONS_PATH = '/autodiagnostico';

  // Régimen de consentimiento. En PRE_LEY se guarda siempre y la casilla no
  // existe. En LEY_21719 vuelve la casilla y decide de verdad. El Worker es
  // el punto de aplicación real; esto solo alinea la UI. Ver
  // specs/consentimiento.md — no borrar la rama de LEY_21719.
  var REGIMEN = 'PRE_LEY';
  var TEXT_VERSION = REGIMEN === 'PRE_LEY'
    ? 'autodiagnostico-preley-2026-09'
    : 'autodiagnostico-ley21719-2026-12';

  var PILLARS = [
    { key: 'proposito', name: 'Propósito' },
    { key: 'fisico', name: 'Físico' },
    { key: 'mental', name: 'Mental' },
    { key: 'social', name: 'Social' },
    { key: 'finanzas', name: 'Finanzas' }
  ];

  var BANDS = [
    { min: 5, max: 11, key: 'atencion', label: 'Zona de atención' },
    { min: 12, max: 18, key: 'intermedia', label: 'Zona intermedia' },
    { min: 19, max: 25, key: 'solida', label: 'Zona sólida' }
  ];

  var DOMINO = {
    proposito: {
      title: 'Si tu más bajo es Propósito',
      items: [
        'Arrastra <strong>Finanzas</strong>: sin dirección, ningún monto alcanza, porque no sabes para qué lo estás guardando.',
        'Arrastra <strong>Social</strong>: cuando el rol laboral se va, se lleva de una vez el círculo de colegas, reuniones y almuerzos.',
        'Arrastra <strong>Mental y Cognitivo</strong>: sin proyectos que te exijan, usas cada vez menos tus capacidades mentales, y lo que se deja de usar se deteriora.'
      ]
    },
    fisico: {
      title: 'Si tu más bajo es Físico',
      items: [
        'Arrastra <strong>Mental y Cognitivo</strong>: la mala salud física está fuertemente asociada a mayor riesgo de enfermedades neurodegenerativas.',
        'Arrastra <strong>Social</strong>: la autonomía física es lo que te permite salir de la casa y sostener tus vínculos.',
        'Arrastra <strong>Finanzas</strong>: la pérdida de autonomía puede desbaratar tu plan financiero, porque el gasto en cuidados es el que más se subestima.'
      ]
    },
    mental: {
      title: 'Si tu más bajo es Mental y Cognitivo',
      items: [
        'Arrastra <strong>Físico</strong>: sin descanso no hay recuperación, y tampoco energía para entrenar.',
        'Arrastra <strong>Social</strong>: cuando aparece deterioro cognitivo, seguir una conversación cuesta más, y la reacción natural es retirarse.',
        'Arrastra <strong>Propósito</strong>: perder capacidades cognitivas es lo que más preocupa a la gente en esta etapa, y sin cabeza no hay plan que se sostenga.'
      ]
    },
    social: {
      title: 'Si tu más bajo es Social',
      items: [
        'Arrastra <strong>Mental y Físico</strong> a la vez: en la literatura de longevidad, la soledad crónica se comporta como un factor de riesgo, no como un tema emocional.',
        'Arrastra <strong>Propósito</strong>: sostener un propósito necesita gente alrededor, que celebre contigo lo que logras y te acompañe cuando algo se cae.'
      ]
    },
    finanzas: {
      title: 'Si tu más bajo es Finanzas',
      items: [
        'Arrastra <strong>Social</strong>: cuando la plata aprieta, lo primero que se recorta son las salidas, los viajes y los regalos. Restarse de las instancias sociales es barato hoy y caro después.',
        'Arrastra <strong>Mental</strong>: la incertidumbre financiera es un impuesto cognitivo que se paga todos los días.',
        'Arrastra <strong>Propósito</strong>: si no sabes si te alcanza, no exploras lo que te gustaría hacer. La falta de números termina limitando lo que te permites imaginar.'
      ]
    }
  };

  var form = document.getElementById('adgForm');
  var viewQuestions = document.getElementById('view-questions');
  var viewResult = document.getElementById('view-result');
  var progressBar = document.getElementById('progressBar');
  var progressFill = document.getElementById('progressFill');
  var progressText = document.getElementById('progressText');
  var progressPillar = document.getElementById('progressPillar');
  var formError = document.getElementById('formError');

  // ---------------------------------------------------------------
  // Progreso en vivo
  // ---------------------------------------------------------------
  function answeredCount() {
    return document.querySelectorAll('.adg-q input:checked').length;
  }

  function updatePillarTotals() {
    var pillarSections = document.querySelectorAll('.adg-pillar');
    pillarSections.forEach(function (section) {
      var key = section.getAttribute('data-pillar');
      var checked = section.querySelectorAll('.adg-q input:checked');
      var out = section.querySelector('.adg-pillar-total .val');
      if (!out) return;
      if (checked.length === 5) {
        var sum = 0;
        checked.forEach(function (i) { sum += parseInt(i.value, 10); });
        out.textContent = sum + ' / 25';
      } else {
        out.textContent = checked.length + '/5 respondidas';
      }
    });
  }

  function updateProgress() {
    var n = answeredCount();
    var pct = Math.round((n / TOTAL_QUESTIONS) * 100);
    if (progressFill) progressFill.style.width = pct + '%';
    if (progressText) progressText.textContent = n + ' de ' + TOTAL_QUESTIONS + ' respondidas';
    updatePillarTotals();
    return n;
  }

  var eventoIniciado = false;
  var eventoCompletado = false;

  document.addEventListener('change', function (e) {
    if (e.target && e.target.matches('.adg-q input[type="radio"]')) {
      var q = e.target.closest('.adg-q');
      if (q) q.classList.remove('is-empty');
      var n = updateProgress();

      // Eventos de funnel: primera pregunta y cuestionario completo. Una
      // sola vez cada uno. Sin propiedades — el pilar más bajo recién se
      // sabe al enviar. Ver specs/analitica.md.
      if (!eventoIniciado && n >= 1) {
        eventoIniciado = true;
        if (window.dtjEvento) window.dtjEvento('autodiagnostico_iniciado');
      }
      if (!eventoCompletado && n >= TOTAL_QUESTIONS) {
        eventoCompletado = true;
        if (window.dtjEvento) window.dtjEvento('autodiagnostico_completado');
      }
    }
  });

  // ---------------------------------------------------------------
  // Cálculo de resultado
  // ---------------------------------------------------------------
  function bandFor(score) {
    for (var i = 0; i < BANDS.length; i++) {
      if (score >= BANDS[i].min && score <= BANDS[i].max) return BANDS[i];
    }
    return BANDS[0];
  }

  function computeTotals() {
    var totals = {};
    PILLARS.forEach(function (p) {
      var section = document.querySelector('.adg-pillar[data-pillar="' + p.key + '"]');
      var checked = section ? section.querySelectorAll('.adg-q input:checked') : [];
      var sum = 0;
      checked.forEach(function (i) { sum += parseInt(i.value, 10); });
      totals[p.key] = sum;
    });
    return totals;
  }

  function collectAnswers() {
    var answers = [];
    document.querySelectorAll('.adg-q').forEach(function (q) {
      var section = q.closest('.adg-pillar');
      var pillar = section ? section.getAttribute('data-pillar') : null;
      var checked = q.querySelector('input:checked');
      var label = q.querySelector('.adg-q-text');
      answers.push({
        pregunta: label ? label.textContent.trim() : '',
        pilar: pillar,
        valor: checked ? parseInt(checked.value, 10) : null
      });
    });
    return answers;
  }

  function lowestPillar(totals) {
    var min = null;
    PILLARS.forEach(function (p) {
      if (min === null || totals[p.key] < totals[min]) min = p.key;
    });
    return min;
  }

  // ---------------------------------------------------------------
  // Render de la vista de resultado
  // ---------------------------------------------------------------
  function pillarName(key) {
    var p = PILLARS.filter(function (x) { return x.key === key; })[0];
    return p ? p.name : key;
  }

  function renderBars(totals) {
    var container = document.getElementById('barsContainer');
    if (!container) return;
    var html = '';
    PILLARS.forEach(function (p) {
      var score = totals[p.key];
      var band = bandFor(score);
      var pct = ((score - 5) / (25 - 5)) * 100;
      // El marcador nunca se pega al borde exacto (0% o 100%), o el redondeo
      // de la barra se lo come. clamp() lo mantiene siempre visible.
      var markerLeft = 'clamp(2px, ' + pct + '%, calc(100% - 2px))';
      html += '' +
        '<div class="adg-bar-row">' +
          '<div class="bar-head"><span class="bar-name">' + p.name + '</span><span class="bar-score">' + score + ' / 25</span></div>' +
          '<div class="adg-bar-wrap">' +
            '<div class="adg-bar-track">' +
              '<div class="zone atencion"></div><div class="zone intermedia"></div><div class="zone solida"></div>' +
            '</div>' +
            '<div class="marker" style="left:' + markerLeft + '"></div>' +
          '</div>' +
          '<div class="bar-band">' + band.label + '</div>' +
        '</div>';
    });
    container.innerHTML = html;
  }

  function renderDomino(minKey) {
    var el = document.getElementById('dominoActive');
    if (!el) return;
    var d = DOMINO[minKey];
    if (!d) return;
    var items = d.items.map(function (t) { return '<li><span class="arrow">→</span> ' + t + '</li>'; }).join('');
    el.innerHTML = '<h3>' + d.title + '</h3><ul>' + items + '</ul>';
  }

  function renderLowestLine(minKey, totals) {
    var el = document.getElementById('lowestLine');
    if (!el) return;
    el.textContent = 'Tu pilar más bajo es ' + pillarName(minKey) + ', con ' + totals[minKey] + ' de 25.';
  }

  // Resumen legible para el correo de reserva de Calendly:
  // "Propósito 12/25 · Físico 18/25 · … — pilar más bajo: Social"
  function resumenParaMargarita(totals, minKey) {
    var partes = PILLARS.map(function (p) {
      return p.name + ' ' + totals[p.key] + '/25';
    });
    return partes.join(' · ') + ' — pilar más bajo: ' + pillarName(minKey);
  }

  function setCalendlyLink(totals, minKey, email) {
    var cta = document.getElementById('ctaCalendly');
    if (!cta) return;
    var q = ['utm_source=autodiagnostico'];
    q.push('a1=' + encodeURIComponent(resumenParaMargarita(totals, minKey)));
    if (email) q.push('email=' + encodeURIComponent(email));
    cta.href = CALENDLY_BASE + '?' + q.join('&');
  }

  // El CTA de cierre es el momento de mayor intención de todo el funnel
  // (Fase 3): personalizarlo al pilar más bajo en vez de repetir el mismo
  // texto para todos. Ver PLAN.md § Fase 3.
  function renderCtaBody(minKey) {
    var el = document.getElementById('ctaBody');
    if (!el) return;
    el.innerHTML = 'Si quieres que revisemos tu caso juntos — partiendo por tu pilar de <strong>' +
      pillarName(minKey) + '</strong>, que es donde hoy tienes más espacio para actuar — te invitamos ' +
      'a agendar una sesión de diagnóstico <strong>gratuita</strong> con nosotros. Dura 45 minutos y sirve ' +
      'para mirar tu caso en particular y ver si tiene sentido que trabajemos juntos.';
  }

  function renderResult(totals, email) {
    var minKey = lowestPillar(totals);
    renderLowestLine(minKey, totals);
    renderBars(totals);
    renderDomino(minKey);
    renderCtaBody(minKey);
    setCalendlyLink(totals, minKey, email);
  }

  // ---------------------------------------------------------------
  // Cambiar de vista
  // ---------------------------------------------------------------
  function showResultView(totals, email) {
    renderResult(totals, email);
    viewQuestions.hidden = true;
    viewResult.hidden = false;
    if (progressBar) progressBar.hidden = true;
    document.body.style.paddingBottom = '';
    window.scrollTo(0, 0);
    try {
      if (window.history && history.pushState && location.pathname !== RESULT_PATH) {
        history.pushState({ dtjResultado: true }, '', RESULT_PATH);
      }
    } catch (err) { /* navegación no disponible, no es crítico */ }
  }

  function showQuestionsView() {
    viewResult.hidden = true;
    viewQuestions.hidden = false;
    if (progressBar) progressBar.hidden = false;
    updateProgress();
    try {
      if (window.history && history.pushState && location.pathname !== QUESTIONS_PATH) {
        history.pushState({ dtjResultado: false }, '', QUESTIONS_PATH);
      }
    } catch (err) { /* no crítico */ }
  }

  // ---------------------------------------------------------------
  // Envío (no bloquea la vista de resultado si falla)
  // ---------------------------------------------------------------
  function setSendStatus(text) {
    var el = document.getElementById('sendStatus');
    if (el) el.textContent = text;
  }

  function sendResult(payload) {
    if (payload.sitioWeb) return; // honeypot con contenido: no se envía, pero el resultado ya se mostró
    fetch(SUBMIT_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(function (res) {
      if (!res.ok) throw new Error('status ' + res.status);
      setSendStatus('Te enviamos este resultado también a tu correo.');
    }).catch(function () {
      setSendStatus('Tu resultado es válido igual: aún no pudimos confirmar el envío a tu correo. Si no llega en unos minutos, escríbenos a disenatujubilacion@gmail.com.');
    });
  }

  function isValidEmail(v) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
  }

  function showFormError(msg) {
    if (!formError) return;
    formError.textContent = msg;
    formError.hidden = false;
  }

  function hideFormError() {
    if (!formError) return;
    formError.hidden = true;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    hideFormError();

    var n = updateProgress();
    if (n < TOTAL_QUESTIONS) {
      var firstEmpty = null;
      document.querySelectorAll('.adg-q').forEach(function (q) {
        var checked = q.querySelector('input:checked');
        if (!checked) {
          q.classList.add('is-empty');
          if (!firstEmpty) firstEmpty = q;
        }
      });
      showFormError('Faltan ' + (TOTAL_QUESTIONS - n) + ' preguntas por responder.');
      if (firstEmpty) firstEmpty.scrollIntoView({ behavior: 'smooth', block: 'center' });
      return;
    }

    var emailInput = document.getElementById('email');
    var email = emailInput.value.trim();
    if (!isValidEmail(email)) {
      showFormError('Ingresa un correo electrónico válido para poder enviarte tu resultado.');
      emailInput.focus();
      emailInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
      return;
    }

    var totals = computeTotals();
    var minKey = lowestPillar(totals);

    var saveCheckbox = document.getElementById('consentSave'); // solo existe en LEY_21719
    var atrib = (window.dtjAtribucion && window.dtjAtribucion()) || { origen: 'directo', campana: '', contenido: '' };

    var payload = {
      uuid: (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : String(Date.now()) + '-' + Math.random().toString(16).slice(2),
      guia: 'DOMINO',
      email: email,
      regimen: REGIMEN,
      consentGuardado: REGIMEN === 'PRE_LEY' ? true : (saveCheckbox ? saveCheckbox.checked : false),
      consentMarketing: document.getElementById('consentMarketing').checked,
      versionTexto: TEXT_VERSION,
      origen: atrib.origen,
      campana: atrib.campana,
      contenido: atrib.contenido,
      fecha: new Date().toISOString(),
      totales: totals,
      pilarMasBajo: minKey,
      respuestas: collectAnswers(),
      sitioWeb: document.getElementById('sitioWeb').value // honeypot
    };

    if (window.dtjEvento) window.dtjEvento('autodiagnostico_enviado', { pilarMasBajo: minKey });

    // Mostrar el resultado ya, en paralelo con el envío — nunca al revés.
    showResultView(totals, email);
    sendResult(payload);

    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify({ totals: totals }));
    } catch (err) { /* almacenamiento no disponible: no es crítico */ }
  });

  var restartLink = document.getElementById('restartLink');
  if (restartLink) {
    restartLink.addEventListener('click', function (e) {
      e.preventDefault();
      try { sessionStorage.removeItem(STORAGE_KEY); } catch (err) {}
      document.querySelectorAll('.adg-q input:checked').forEach(function (i) { i.checked = false; });
      form.reset();
      showQuestionsView();
    });
  }

  // ---------------------------------------------------------------
  // Carga directa de /autodiagnostico/resultado (refresco de página)
  // ---------------------------------------------------------------
  function init() {
    var onResultPath = location.pathname.replace(/\/$/, '') === RESULT_PATH;
    if (onResultPath) {
      var saved = null;
      try {
        var raw = sessionStorage.getItem(STORAGE_KEY);
        if (raw) saved = JSON.parse(raw);
      } catch (err) { /* sin storage disponible */ }

      if (saved && saved.totals) {
        renderResult(saved.totals);
        viewQuestions.hidden = true;
        viewResult.hidden = false;
        if (progressBar) progressBar.hidden = true;
        setSendStatus('Este es el resultado que calculaste antes.');
        return;
      }
      // No hay resultado guardado en este navegador: vuelve a las preguntas.
      try { history.replaceState({}, '', QUESTIONS_PATH); } catch (err) {}
    }
    updateProgress();
  }

  init();
})();
