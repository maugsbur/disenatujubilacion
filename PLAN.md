# Plan de trabajo — Diseña tu Jubilación (sitio web)

Decisiones tomadas el 2026-09-02 (Marcel): Brevo como proveedor de correo, cola con
reintento si se topa la cuota diaria, repo privado en GitHub conectado a Cloudflare
Pages, el correo de resultado incluye los cinco totales por pilar, consentimiento de
Carlos confirmado.

Apps Script (Etapa 3) verificado en producción con datos reales el 2026-09-03.

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
- [x] Secretos de verdad en el dashboard como **Secret** (`SHARED_TOKEN`); el resto
      de las variables (no secretas) en `wrangler.toml` § `[vars]`
- [x] Probado en local con `wrangler pages dev` + un Apps Script simulado: envío
      válido, honeypot, correo inválido, content-type incorrecto, y el límite de
      6/60s — los cinco se comportan como se espera
- [x] **Probado en producción real, 2026-09-03**, contra Apps Script real (no
      simulado): `{"ok":true,"recibido":true,"uuid":"...","correoEnviado":false}`
      — `correoEnviado:false` es lo esperado, Brevo (Etapa 5) aún no está configurado
- [x] **Bug real encontrado y corregido:** con `wrangler.toml` presente, Cloudflare
      Pages ignora las variables de texto plano puestas en el dashboard — solo
      respeta ahí las marcadas como Secret. `APPS_SCRIPT_URL` se agregó bien en el
      dashboard y el Worker nunca la vio; costó una sesión completa de diagnóstico
      (incluida una pista falsa sobre "propagación" que resultó ser un bug en mi
      propio script de prueba, no del sistema). Ahora `APPS_SCRIPT_URL` vive en
      `wrangler.toml` § `[vars]`; solo lo genuinamente secreto queda en el dashboard.
      Ver `README.md` § El Worker para el detalle completo

## Etapa 5 — Correo (Brevo) ✅ configurado y verificado en producción
- [x] **Decisión de arquitectura, confirmada por Marcel el 2026-09-02:** los tres PDF
      viven en `site/assets/pdfs/`, en rutas largas y aleatorias, sin enlazar desde
      ninguna página — Brevo los descarga con `attachment.url`. Se descartó Cloudflare
      R2 (exige tarjeta de crédito para activarlo, incluso en el nivel gratuito) y volver
      a rutear adjuntos por Apps Script/Drive (reabría la Etapa 3 sin necesidad)
- [x] Worker: intenta Brevo primero; si falla, le pasa a Apps Script el cuerpo exacto
      que se le iba a mandar a Brevo, listo para reintentar sin reconstruir nada
- [x] Apps Script: `CorreoPendiente.gs` — cola de reintento cada 30 min, alerta al
      equipo si una fila lleva 24h fallando (tiempo de sobra para que se resetee
      una cuota diaria topada)
- [x] Las cuatro plantillas creadas en Brevo con copy real (Etapa 6 leyó los tres
      PDF completos), Template ID: DOMINO=1, ENTUSIASMO=2, HABLAR=3, PLAN=4
- [x] Cuenta Brevo configurada, dominio autenticado — SPF, DKIM y DMARC en `PASS`,
      confirmado tanto a nivel de dominio como en un mensaje real
- [x] Los tres PDF copiados al repo con nombres aleatorios (`brevo/README.md` tiene
      la tabla exacta) y `noindex` en `_headers` — confirmados accesibles en producción
- [x] **Probado en producción real, 2026-09-03**, las cuatro plantillas: DOMINO,
      PLAN y ENTUSIASMO devuelven `correoEnviado:true` de la API de Brevo
- [x] **Bug real encontrado y corregido:** Brevo rechaza `params:{}` (objeto vacío)
      con `"params is blank"` — las guías sin parámetros dinámicos (PLAN, HABLAR,
      ENTUSIASMO) ahora omiten el campo por completo en vez de mandarlo vacío
- [x] **Vacío real encontrado y corregido:** `borrarPersona()` no limpiaba
      `correos_pendientes`, que sí tiene datos de la persona (correo, y para
      DOMINO los totales). Ahora se borra junto con Personas y Respuestas
- [ ] **Riesgo abierto, no resuelto — no es un bug de configuración:** un correo de
      PLAN a la casilla real de Marcel se entregó pero no apareció en ninguna
      pestaña de Gmail ni en spam (solo con `in:all`) — con SPF/DKIM/DMARC en PASS
      confirmado en el mensaje mismo, sin filtro de Gmail ni hilo anterior de por
      medio. Explicación más probable: el dominio empezó a enviar hoy, en IP
      compartida, y este fue su primer correo con adjunto — sin reputación aún,
      Gmail puede clasificar de forma inconsistente mensaje a mensaje. Se resuelve
      con volumen y consistencia de envío, no con más configuración. **Seguir
      probando en los próximos días** (Gmail, Outlook, un corporativo — ítem ya
      pendiente en el checklist de `08-cumplimiento-datos.md`) antes de asumir que
      quedó resuelto
- [ ] **Pendiente:** prueba de entregabilidad real una vez desplegado: Gmail,
      Outlook, un corporativo
- [x] Los tres PDF ya se leyeron completos (Etapa 6) y las plantillas de
      Brevo se actualizaron con copy real

## Etapa 6 — Landing, tres páginas de captura y privacidad ✅
- [x] CTA de Calendly (45 min), WhatsApp (+56 9 3486 5410) e Instagram
- [x] Landing real: qué es el programa, los cinco pilares, grilla de recursos
      gratuitos (autodiagnóstico + las tres guías), CTA final
- [x] Copy real de `/plan`, `/hablar`, `/carlos` — se leyeron los tres PDF
      completos y se escribió una versión condensada para cada página (no el
      PDF entero: la guía completa es el incentivo para dejar el correo)
- [x] Formulario de captura compartido (`assets/js/captura.js`): valida,
      manda a `/api/submit`, y el mensaje final depende de si Brevo
      realmente envió el correo o quedó en la cola de reintento
- [x] Política de privacidad completa, según checklist de
      `08-cumplimiento-datos.md` §7 — **borrador de buena fe, no revisión
      legal.** Esa revisión sigue listada para antes del 1 de diciembre en
      la sección de abajo, tal como ya lo marcaba `08-cumplimiento-datos.md`
- [x] Bug real encontrado y corregido de paso: `wrangler.toml` tenía el ID
      del namespace de KV sin comillas (TOML inválido) — habría roto el
      deploy real, no solo las pruebas locales
- [x] Probado en local con `wrangler pages dev`: landing, las tres páginas
      de captura y la política de privacidad en viewport móvil; el
      formulario de captura probado de punta a punta (envío exitoso y
      camino de error) contra Apps Script y Brevo simulados

## Etapa 7 — Cierre
- [ ] Prueba extremo a extremo de los cuatro flujos
- [ ] Las cuatro combinaciones de casillas verificadas
- [ ] Borrado y exportación probados con un caso real
- [ ] `origen`/UTM funcionando
- [ ] Checklist "antes de publicar" de `08-cumplimiento-datos.md` §9, punto por punto
