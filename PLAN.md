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

## Etapa 3 — Contrato de datos y Apps Script ✅ código listo
- [x] Código completo en `apps-script/`: `doPost` con token compartido (va en el
      cuerpo JSON, no en un header — Apps Script no expone headers personalizados),
      upsert por correo en Personas, escritura condicional en Respuestas
- [x] Comportamiento de las dos casillas implementado tal cual la tabla de
      `08-cumplimiento-datos.md` §3: las respuestas solo se escriben si
      `consentGuardado === true`, independiente de la casilla de marketing
- [x] `borrarPersona(email)`, `exportarPersona(email)`, más un menú
      "DTJ · Privacidad" en la planilla para que Nicole no necesite el editor
- [x] `limpiarRetencion18Meses()` + `instalarTriggerRetencion()`
- [x] Decisión: una fila por correo (upsert), el origen del primer contacto
      nunca se sobrescribe — confirmado por Marcel el 2026-09-02
- [ ] **Pendiente de Marcel:** crear las dos planillas con los encabezados
      exactos, pegar el código, configurar propiedades y desplegar — pasos en
      `apps-script/README.md`
- [ ] **Pendiente:** probar con datos reales una vez desplegado (curl de
      prueba incluido en el README) y confirmar en vivo que las cuatro
      combinaciones de casillas hacen lo que dicen

## Etapa 4 — Worker ✅ código listo y probado en local
- [x] Implementado como **Pages Function** (`functions/api/submit.js`), no como
      Worker/dominio aparte — se despliega solo con cada push, mismo dominio, sin CORS
- [x] Validación de payload y consentimientos
- [x] Honeypot + rate limiting por IP — se optó por **KV** (6 envíos/IP cada 60s) en vez
      del binding nativo de Rate Limiting: su soporte en Pages Functions (a diferencia de
      Workers) no está documentado con la misma claridad, y 1.000 escrituras/día de KV
      sobra por mucho para el volumen esperado. Falla abierto si KV no responde
- [x] Reenvío a Apps Script con token compartido dentro del cuerpo JSON
- [x] Secretos en variables de entorno (dashboard de Pages, no en `wrangler.toml`)
- [x] Probado en local con `wrangler pages dev` + un Apps Script simulado: envío
      válido, honeypot, correo inválido, content-type incorrecto, y el límite de
      6/60s — los cinco se comportan como se espera
- [ ] **Pendiente de Marcel:** crear el namespace de KV, pegar su ID en `wrangler.toml`,
      y configurar `APPS_SCRIPT_URL` + `SHARED_TOKEN` en el dashboard — pasos en
      el `README.md` § El Worker
- [ ] **Pendiente:** una vez Apps Script esté desplegado de verdad (Etapa 3), probar
      el flujo completo en producción, no solo contra el simulado

## Etapa 5 — Correo (Brevo)
- [ ] Cuenta Brevo + dominio verificado (SPF, DKIM, DMARC en `disenatujubilacion.com`)
- [ ] Plantillas de los cuatro envíos (DOMINÓ con totales por pilar, PLAN, HABLAR, ENTUSIASMO)
- [ ] Adjuntos de los tres PDF (PLAN, HABLAR, ENTUSIASMO)
- [ ] Cola con reintento cuando se tope la cuota diaria + alerta al equipo
- [ ] Prueba de entregabilidad real: Gmail, Outlook, un corporativo

## Etapa 6 — Landing, tres páginas de captura y privacidad
- [x] CTA de Calendly (45 min), WhatsApp (+56 9 3486 5410) e Instagram —
      agregados el 2026-09-02 en el placeholder; se trasladan tal cual al diseño final
- [ ] Landing real (hoy: placeholder con el copy y los CTA ya correctos)
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
