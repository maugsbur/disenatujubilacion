/* Formulario de captura — compartido por /plan, /hablar y /carlos.
 * El <form> declara data-guia="PLAN|HABLAR|ENTUSIASMO"; este script hace
 * el resto. A diferencia del autodiagnóstico, acá SÍ importa si el correo
 * realmente se mandó (el "producto" es el PDF adjunto, no algo que ya se
 * calculó en el navegador) — por eso el mensaje final depende de
 * `correoEnviado` en la respuesta del Worker, no de un simple "ok".
 */
(function () {
  'use strict';

  var TEXT_VERSION = 'captura-v1-2026-09';
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  var form = document.getElementById('capForm');
  if (!form) return;

  var guia = form.getAttribute('data-guia') || 'PLAN';
  var formError = document.getElementById('capFormError');
  var formOk = document.getElementById('capFormOk');
  var submitBtn = form.querySelector('.cap-submit');

  function showError(msg) {
    if (!formError) return;
    formError.textContent = msg;
    formError.hidden = false;
  }
  function hideError() {
    if (formError) formError.hidden = true;
  }
  function showOk(msg) {
    form.hidden = true;
    if (formOk) {
      formOk.innerHTML = msg;
      formOk.hidden = false;
    }
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    hideError();

    var emailInput = document.getElementById('capEmail');
    var email = emailInput.value.trim();
    if (!EMAIL_RE.test(email)) {
      showError('Ingresa un correo electrónico válido para poder enviarte la guía.');
      emailInput.focus();
      return;
    }

    var consentMarketing = document.getElementById('capConsentMarketing');
    var honeypot = document.getElementById('capHp');

    var payload = {
      email: email,
      guia: guia,
      origen: guia,
      consentGuardado: false, // estas páginas no tienen respuestas de cuestionario que guardar
      consentMarketing: consentMarketing ? consentMarketing.checked : false,
      versionTexto: TEXT_VERSION,
      sitioWeb: honeypot ? honeypot.value : ''
    };

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Enviando…';
    }

    fetch('/api/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(function (res) { return res.json().then(function (data) { return { status: res.status, data: data }; }); })
      .then(function (r) {
        if (!r.data || r.data.ok !== true) {
          throw new Error((r.data && r.data.error) || 'error_desconocido');
        }
        if (r.data.correoEnviado) {
          showOk('<strong>Listo.</strong> Te enviamos la guía a tu correo — revisa también la carpeta de spam por si acaso.');
        } else {
          showOk('<strong>Recibimos tu solicitud.</strong> Tu guía va en camino; si no te llega en unos minutos, escríbenos a disenatujubilacion@gmail.com.');
        }
      })
      .catch(function () {
        showError('No pudimos procesar tu solicitud. Inténtalo de nuevo en un momento, o escríbenos a disenatujubilacion@gmail.com.');
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = 'Enviarme la guía';
        }
      });
  });
})();
