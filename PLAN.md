# Plan de trabajo — Diseña tu Jubilación (sitio web)

Decisiones tomadas el 2026-09-02 (Marcel): Brevo como proveedor de correo, cola con
reintento si se topa la cuota diaria, repo privado en GitHub conectado a Cloudflare
Pages, el correo de resultado incluye los cinco totales por pilar, consentimiento de
Carlos confirmado.

## Etapa 0 — Decisiones bloqueantes ✅
- [x] Proveedor de correo: **Brevo**, no Apps Script/GmailApp (el alias de dominio en
      Gmail sin Workspace deja de ser viable: Google restringe "Enviar como" para
      terceros desde 2026 y lo elimina en enero de 2027).
- [x] Comportamiento al topar cuota: encolar y reintentar, nunca perder la solicitud.
- [x] Repositorio: `git@github.com:maugsbur/disenatujubilacion.git`, privado.
- [x] El correo de resultado lleva los cinco totales por pilar.
- [x] Consentimiento de Carlos, confirmado.

## Etapa 1 — Esqueleto desplegado ✅ (este commit)
- [x] Estructura de carpetas (`site/`, `worker/`, `apps-script/`)
- [x] Siete rutas con placeholder: `/`, `/autodiagnostico`, `/plan`, `/hablar`, `/carlos`, `/privacidad`
- [x] `_redirects` y `_headers` para Cloudflare Pages
- [x] Repo en git, listo para conectar a Pages
- [ ] **Pendiente de Marcel:** conectar el repo a Cloudflare Pages desde el dashboard
      (paso manual, requiere su login — instrucciones en `README.md`) y apuntar el DNS
      de `disenatujubilacion.com`

## Etapa 2 — Autodiagnóstico: dos vistas + móvil ✅ (este commit)
- [x] Vista de preguntas: portada, instrucciones, 25 preguntas, formulario + consentimientos
- [x] Vista de resultado: totales por pilar, gráfico de zonas, efecto dominó, 5 perfiles, cierre + CTA
- [x] Cálculo 100% en el navegador; el resultado se muestra aunque el POST falle
- [x] Rediseño mobile-first: sin páginas A4, botones de respuesta ≥48px, barra de
      progreso fija, sin dependencia de `window.print()`
- [x] `/autodiagnostico/resultado` sobrevive un refresh vía `sessionStorage` + `_redirects`
- [x] Honeypot en el formulario, listo para que el Worker lo valide en la Etapa 4
- [ ] **Pendiente:** probar en el navegador integrado de Instagram real (iOS y Android),
      no solo en emulación de viewport — el comportamiento del teclado y el `100dvh`
      puede variar

## Etapa 3 — Contrato de datos y Apps Script
- [ ] Dos archivos de Sheets separados (`DTJ · Personas`, `DTJ · Respuestas`) por UUID
- [ ] `doPost` con token compartido, valida y escribe
- [ ] Comportamiento de las dos casillas verificado de verdad (sin casilla 1, no se
      escribe ninguna respuesta)
- [ ] `borrarPersona(email)`, `exportarPersona(email)`
- [ ] Disparador mensual de retención a 18 meses

## Etapa 4 — Worker
- [ ] Validación de payload y consentimientos
- [ ] Honeypot + rate limiting por IP (confirmar si el binding nativo de Rate Limiting
      de Cloudflare está disponible en el plan free; si no, KV con 1.000 escrituras/día)
- [ ] Reenvío a Apps Script con token compartido
- [ ] Secretos en variables de entorno

## Etapa 5 — Correo (Brevo)
- [ ] Cuenta Brevo + dominio verificado (SPF, DKIM, DMARC en `disenatujubilacion.com`)
- [ ] Plantillas de los cuatro envíos (DOMINÓ con totales por pilar, PLAN, HABLAR, ENTUSIASMO)
- [ ] Adjuntos de los tres PDF (PLAN, HABLAR, ENTUSIASMO)
- [ ] Cola con reintento cuando se tope la cuota diaria + alerta al equipo
- [ ] Prueba de entregabilidad real: Gmail, Outlook, un corporativo

## Etapa 6 — Landing, tres páginas de captura y privacidad
- [ ] Landing real (hoy: placeholder) — CTA a Calendly y WhatsApp
      **Pendiente: número de WhatsApp** — no está en el brief ni en los documentos, hace
      falta antes de poder poner el botón
- [ ] Copy real de `/plan`, `/hablar`, `/carlos` — para esto hay que leer el contenido
      completo de los tres PDF (en esta sesión solo se confirmaron metadatos: tamaño de
      archivo, no el texto)
- [ ] Política de privacidad completa, según checklist de `08-cumplimiento-datos.md` §7

## Etapa 7 — Cierre
- [ ] Prueba extremo a extremo de los cuatro flujos
- [ ] Las cuatro combinaciones de casillas verificadas
- [ ] Borrado y exportación probados con un caso real
- [ ] `origen`/UTM funcionando
- [ ] Checklist "antes de publicar" de `08-cumplimiento-datos.md` §9, punto por punto
