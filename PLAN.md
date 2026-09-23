# Plan de trabajo — Diseña tu Jubilación (sitio web)

Decisiones tomadas el 2026-09-02 (Marcel): Brevo como proveedor de correo, cola con
reintento si se topa la cuota diaria, repo privado en GitHub conectado a Cloudflare
Pages, el correo de resultado incluye los cinco totales por pilar, consentimiento de
Carlos confirmado.

Apps Script (Etapa 3) verificado en producción con datos reales el 2026-09-03.

Decisiones del 2026-09-03: las planillas, el script y la cuenta de Brevo se quedan
bajo la cuenta personal de Marcel — compartidos como Editoras con Nicole y
Margarita, sin transferir propiedad a `disenatujubilacion@gmail.com` (esa cuenta
ya se bloqueó una vez, y cambiar de dueño no cambia la exposición a GDPR, que
depende del establecimiento de las personas, no de en qué cuenta vive el archivo).
Pendiente real y aparte: Google Workspace en el futuro no lejano, sobre todo por
que "Enviar como" para terceros lo elimina Google en enero de 2027.

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

## Fase 0 — El sitio en el funnel (revisión de UX, 2026-09-10)

Del plan en el artifact "El Sitio en el Funnel". Ver `specs/` y `CLAUDE.md`,
montados en esta fase.

- [x] **Lead magnets:** CTA roto (`/40min`) corregido en `build_common.py`,
      con `utm_source=pdf-<guia>` por guía. Fuentes traídas al repo
      (`lead-magnets/`). Dos bugs del build corregidos de paso: escritura
      sin encoding (cp1252 en Windows contra `charset=utf-8`) y fuentes
      Lora/Poppins que no se cargaban (caía a Arial/Times sin aviso). Los
      cuatro PDF regenerados, aprobados por Marcel. **Pendiente de Marcel:
      reemplazar los PDF en `site/assets/pdfs/`** (mismos nombres aleatorios)
- [x] Landing: "40 minutos" → "45 minutos"
- [x] **Atribución:** `atribucion.js` compartido produce `origen` (utm_source),
      `campana` (utm_campaign), `contenido` (utm_content). `captura.js` ya no
      manda `origen: guia`. `Personas.gs` pasó a header-driven. **Pendiente
      de Marcel: agregar columnas `campana`, `contenido`, `regimen` a la
      pestaña `personas`** (orden libre) + `clasp push` + redeploy
- [x] **Consentimiento (régimen PRE_LEY):** casilla de guardado quitada,
      declaración clara en su lugar, se guarda siempre. Constante `REGIMEN`
      en front/Worker/Apps Script con la rama de LEY_21719 escrita. Marcador
      de cohorte (`regimen` + `version_texto`). Política de privacidad §2/§3
      actualizada. Ver `specs/consentimiento.md` para el checklist del
      1 de diciembre
- [x] **Analítica:** scaffold de PostHog, inerte hasta cargar
      `POSTHOG_PROJECT_TOKEN`. `functions/api/config.js` + `analitica.js` +
      eventos de funnel. Sin Meta Pixel — los ads de Instagram no llevan al
      sitio (corrección de Marcel al modelo, ver artifact rev. 3)
- [x] Marcel corrió el wizard de instalación de PostHog (2026-09-15): SDK
      integrado, token real en `.dev.vars` local. **Pendiente de Marcel: el
      resto de `specs/analitica.md`** — sobre todo copiar el token al
      dashboard de Cloudflare como Secret (`/api/config` en producción
      sigue devolviendo `{}` mientras tanto), decidir proxy, autorizar
      dominio

### Modelo de funnel (corregido por Marcel, 2026-09-10)

Los ads pagados **no** llevan al sitio. El funnel de venta es Instagram:
los ads llevan a la cuenta y al contenido, se nutre a la audiencia ahí, y
recién después se redirige a la gente al sitio — sobre todo para los lead
magnets. El sitio también es prueba de que hay un negocio real detrás.

El sitio hace tres trabajos: (1) entregar el lead magnet a cambio de un
correo con contexto, (2) ser la prueba de credibilidad para quien va a
evaluar antes de agendar, (3) armar la llamada de Margarita. Lo que no
sirva a uno de esos tres es ruido.

## Fase 1 — Armar la llamada de Margarita

Mayor retorno por esfuerzo. No toca el sitio: cambia cada conversación de
venta. El dato ya está guardado, falta ponérselo enfrente.

- [x] **Formato (decidido 2026-09-11):** todo va en el mismo enlace de
      Calendly. El botón del resultado precarga `email` y `a1` (los cinco
      puntajes + el pilar más bajo, en texto legible). Sin backend nuevo;
      solo dispara cuando alguien realmente agenda
- [x] Que Margarita reciba los cinco puntajes y el pilar más bajo de quien
      agenda, antes de la llamada — llegan en el correo de confirmación de
      la reserva (`autodiagnostico.js` → `#ctaCalendly`)
- [x] Pasar el correo a Calendly por parámetro de URL — `?email=…` en el
      mismo enlace, para unir la reserva con la fila de `personas`
- [ ] **Paso manual de Margarita:** en Calendly → evento de 45 min →
      *Invitee Questions* → agregar una pregunta de texto y dejarla primera,
      para que `a1` caiga ahí. Ver `specs/contrato-datos.md` § 5. Hasta que
      lo haga, el correo prellenado funciona y el resultado no

## Fase 2 — Credibilidad (implementada 2026-09-11)

Con el modelo corregido, pasó de "una mejora más" a ser el trabajo central
del sitio. El material salió de la portada de `jubilar.me` y, sobre todo,
de Notion: la página **Testimonios** y la base **Citas** (dentro de
`THE Plan / Diseña tu Jubilación / Entrevistas`), que ya tenía las citas
curadas y con propósito de venta asignado — más completa que el sitio viejo.

- [x] Adaptar las bios de Nicole y Marcel — sección "Quiénes te acompañan"
      en la landing, con el dato de metodologías en sector privado, ONGs y
      la ONU. Sin foto todavía: el avatar es un monograma de color, listo
      para reemplazar por una foto real sin tocar el layout
- [x] Publicar tres testimonios (Alejandro, Irene, Silvia) en la landing,
      con la nota "Diseña tu Jubilación es la evolución de Jubilar.me... estos
      testimonios son de esa primera versión." Citas verificadas contra la
      transcripción original en Notion, no contra el resumen del sitio viejo
      (había pequeñas diferencias de redacción)
- [x] Credibilidad en las tres páginas de captura, cada una con una cita
      elegida por tema — no la misma en las tres: Alejandro ("no están
      improvisando") en `/plan`, Silvia (el módulo legal como "un tema de
      amor hacia los que se quedan") en `/hablar`, Irene (preparación para
      30 años) en `/carlos`
- [x] Testimonio de Alberto agregado a la landing (Marcel confirmó usarlo,
      2026-09-11): "Le diría que tomar este curso te cambiará la vida..."
      — la sección pasó de tres a cuatro testimonios (grilla 2×2)
- [ ] **De Nicole + Marcel:** foto nueva de Nicole (la de `jubilar.me` es
      240×328) y número real de egresados del Club de Implementación

## Fase 3 — Afinar cada página de llegada (implementada 2026-09-11)

Instagram ya enruta por temperatura. Esto es que cada página funcione para
quien ya eligió llegar ahí.

- [x] CTA del resultado del autodiagnóstico personalizado al pilar más bajo
      de esa persona — el texto de cierre ahora nombra el pilar ("partiendo
      por tu pilar de Propósito, que es donde hoy tienes más espacio para
      actuar") en vez de decir lo mismo para todos
- [x] Convención de UTM escrita en `specs/contrato-datos.md` § 6 —
      `utm_source` solo puede ser `bio` / `historia` / `ads` (dónde está el
      enlace), `utm_campaign` es la campaña si la hay, `utm_content` es la
      pieza. Con ejemplos de enlace completo para copiar
- [x] Orden de la landing corregido: "Quiénes te acompañan" y los
      testimonios (Fase 2) ahora van **antes** de "Recursos gratuitos" —
      primero credibilidad, después las acciones, para quien llega a evaluar

### Revisión de `hijos.jubilar.me` (2026-09-15)

Marcel pidió revisar el sitio de regalo para hijos, ya funcionando de
nuevo, y rescatar lo que sirviera adaptado (no el copy, no el enfoque de
regalo — esa audiencia sigue descartada). De las cuatro secciones
propuestas quedaron dos en la landing:

- [x] **"Es para ti si..."** — checklist de calificación + una línea de
      descalificación honesta, antes del CTA final
- [x] **Preguntas frecuentes** — acordeón nativo (`<details>`, sin JS),
      antes del CTA final. Las preguntas se escribieron de cero para este
      público — las de `hijos` (regalo, gift card) no aplicaban
- [x] ~~"Qué nos hace distintos"~~ — se agregó y luego se sacó a pedido de
      Marcel (2026-09-15)
- [ ] **"Cómo funciona"** (4 pasos) — pendiente, Marcel pidió dejarla para
      después

### Rediseño al estilo hijos (2026-09-16)

Marcel prefiere el diseño de `hijos.jubilar.me` — layout, tarjetas,
secciones y el bloque de "quiénes somos". Se portó el lenguaje visual a la
capa CSS compartida, **sin migrar a Astro**. Detalle y decisiones en
`specs/diseno.md`.

- [x] Tokens nuevos en `base.css`: papel cálido, franja alterna, sombra,
      contenedor ancho, grillas, `.card`, `.tag`, `.microcopy`
- [x] Landing reestructurada: hero con etiqueta + dos CTA + chips, franjas
      alternadas en vez de líneas, listas y checklists dentro de tarjetas
- [x] "Quiénes te acompañan" con la **foto real** de Nicole y Marcel más el
      relato "Por qué existe este programa", adaptado del de hijos al
      público nuevo. Resuelve el pendiente de la foto de Nicole
- [x] Las 4 páginas de captura y `/privacidad` heredan el lenguaje sin
      tocarlas (comparten `base.css` + `captura.css`)
- [ ] **De Marcel: la imagen del hero.** El hero ya está listo para
      recibirla — se abre a dos columnas solo cuando el `<img>` existe
- [ ] **De Marcel: un logo**, si quiere header fijo como hijos
- [ ] El autodiagnóstico quedó fuera: hereda tokens y botones, pero su UI
      de 25 preguntas tiene CSS propio y necesita una pasada aparte

## Fase 4 — Optimizar con datos

Solo cuando la analítica lleve dos o tres semanas midiendo con tráfico
real. Antes no hay nada que optimizar, solo opiniones.

- [ ] El abandono real del autodiagnóstico: 25 preguntas desde el celular
      es una apuesta fuerte que puede estar funcionando o sangrando
- [ ] Evaluar si el correo obligatorio en el peak de intención es un
      problema real. Distinto de la casilla de guardado (esa ya se decidió)
- [ ] Probar el encuadre de la landing: "Con intención y no por inercia" es
      un principio de marca excelente y quizá abstracto como primera pantalla
      para quien fue a evaluar quiénes son

## Etapa 7 — Cierre
- [ ] Prueba extremo a extremo de los cuatro flujos
- [ ] La casilla de marketing verificada en las dos combinaciones (la de
      guardado ya no existe en PRE_LEY)
- [ ] Borrado y exportación probados con un caso real
- [x] `origen`/UTM funcionando — Fase 0
- [ ] Checklist "antes de publicar" de `08-cumplimiento-datos.md` §9, punto por punto

### Revisión de contenido de la landing (2026-09-16)

Revisión completa pensando en quien llega desde Instagram a evaluar. Nueva
estructura: hero · el problema · cinco pilares · qué incluye · cómo empezar
· quiénes te acompañan · testimonios · es para ti si · recursos gratuitos ·
FAQ · CTA final. Reglas de copy nuevas en `CLAUDE.md` § Idioma y tono.

- [x] Decisiones de Marcel: formato mixto (sesiones individuales, grupales
      y material), sin precio en la página, Margarita presentada en "Cómo
      empezar" como quien coordina, la llamada pasa a llamarse **llamada de
      evaluación**, el hero mantiene "Con intención y no por inercia"
- [x] Sin rayas (—) ni "no es X, es Y" en el copy visible de todas las
      páginas; lenguaje neutro en género
- [x] Testimonios de la landing reemplazados por citas verificadas en
      Notion (Marcela, Domingo, Alejandro, Irene, Pame, Alberto)
- [x] Incoherencias: `/plan` decía "sin planes de doce semanas" en un sitio
      que vende 13; `/carlos` decía "Guía · ENTUSIASMO" y la tarjeta "Caso
      real"; `/privacidad` hablaba de "leads" y "llamada de venta"
- [x] Pregunta "¿Cuánto tiempo toma a la semana?": 4 horas; la cantidad
      de sesiones se ve en la llamada (Marcel, 2026-09-16)
- [x] Testimonios de todo el sitio tomados de "✂️ Extractos" (verificados
      contra la transcripción) y elegidos por objeción del público: la
      identidad ligada al trabajo (Irene, Alejandro), "solo me preparé en lo
      económico" (Carlos), "ya lo sé todo" (Silvia). La cita de Silvia en
      `/hablar` que no aparecía en ningún lado se reemplazó por una de Juani
- [x] Duración: **3 meses** en todo el sitio (decidido 2026-09-16), en vez
      de "13 semanas" o "90 días"
- [x] PDF regenerados (2026-09-16): el CTA dice "llamada de evaluación
      gratuita con Margarita" y nombra el programa de 3 meses; `/plan` ya no
      dice "doce semanas". Sin rayas en el texto
- [ ] Plantillas de Brevo: revisar rayas y "sesión"
- [x] Hero sin la etiqueta "Después de jubilar vienen 20 o 30 años más";
      testimonios firmados "participante del programa piloto"

### Guía PILARES: los cinco pilares y el efecto dominó (2026-09-17)

Versión de lectura del autodiagnóstico para quien recién llega al perfil y
no va a responder 25 preguntas. Mismo marco y mismas cadenas del efecto
dominó; en vez del cuestionario, tres señales por pilar y un ejercicio de
cinco frases para marcar la menos cierta. Termina invitando al
autodiagnóstico online (`utm_source=pdf-pilares`) y a la llamada.

- [x] Borrador del PDF (8 páginas, `lead-magnets/build_pilares.py`)
- [x] Página `/pilares`, guía `PILARES` en el Worker y `PDF_URL_PILARES`
- [ ] **Marcel/Nicole:** revisar el texto del PDF
- [ ] **Marcel:** crear la plantilla en Brevo (`brevo/plantillas/PILARES.md`)
      y poner `BREVO_TEMPLATE_PILARES` en `wrangler.toml`. Hasta entonces
      `/pilares` no manda correo: no enlazarla
- [ ] **Margarita:** palabra clave de Instagram. Hoy DOMINÓ lleva al
      autodiagnóstico
- [ ] Agregar la tarjeta en "Empieza por aquí" de la landing, cuando el
      correo funcione

- [x] Texto pixelado en los PDF (2026-09-17): era `opacity` en texto, que
      wkhtmltopdf rasteriza. Reemplazado por colores sólidos en las cinco
      guías; las cuatro publicadas se regeneraron con rutas nuevas

### Versiones breves de las guías (2026-09-21)

Marcel pidió una segunda versión de cada guía, más corta, porque las de 8
páginas piden demasiado tiempo a quien recién llega desde Instagram. Decidido
con él: **la breve se adjunta al correo y la completa se entrega a mano** a
quien sigue la conversación, sin enlazarla en ninguna parte (así ese pedido
es una señal de interés y la conversación sigue con una persona).

- [x] `lead-magnets/build_breves.py`: PILARES, PLAN, HABLAR y ENTUSIASMO en
      2 páginas, con la misma estructura (portada integrada · el problema ·
      lo esencial · el mismo CTA a la llamada de evaluación)
- [x] `PDF_URL_*` apunta a las breves; las completas quedan en sus rutas,
      listadas en `brevo/README.md` § 4 para envío manual
- [x] Las páginas de captura dicen "2 páginas · PDF"
- [x] La portada de ENTUSIASMO decía "No es una historia de motivación: es
      un método", el patrón que el público castiga. Ahora dice "Un método,
      contado desde un caso real"
- [ ] **Marcel/Nicole:** revisar las cuatro breves

### Más explicación de los cinco pilares en la breve (2026-09-22)

Marcel pidió que la versión breve de PILARES explicara mejor qué es cada
pilar, no solo la señal de alerta. Cada uno ahora tiene una frase de qué
es y por qué importa (tomada de la guía completa), y para que siguiera en
2 páginas se recortó la intro y se ajustó el interlineado de la lista.

### Criterio de escritura, fijado con Marcel (2026-09-22)

Marcel revisó línea por línea la guía PILARES breve y de ahí salió un
criterio de escritura que ahora vive en `CLAUDE.md` § Cómo se escribe el
copy: hablarle a quien todavía no jubila, ninguna metáfora sin explicar,
sin absolutos, sin meta-comentarios del formato, etiquetas precisas
("Alerta:", "Pregunta central:"), cada idea una sola vez, nombrar el
mecanismo y no solo el efecto, y nombrar toda pérdida junto con su salida.

- [x] Las cuatro guías breves reescritas con ese criterio
- [x] Páginas de captura alineadas con los títulos nuevos (`/pilares`,
      `/plan`, `/hablar`) y tarjeta de PLAN en la landing
- [x] Autodiagnóstico (página y PDF): fuera "se juega", "arrastra" y
      "ningún pilar grita"
- [ ] Las cuatro guías **completas** todavía tienen el lenguaje viejo. Se
      entregan a mano, así que no urge, pero conviene pasarles el mismo
      criterio antes de repartirlas mucho

### Guías de voz y diseño unificadas (2026-09-23)

Había cuatro documentos que se solapaban: `CLAUDE.md` § tono, las reglas
nuevas del repo, y en Notion *✍️ Cómo escribimos* y *🎨 Cómo diseñamos*.
Cada agente leía uno distinto, así que las reglas de las guías no llegaban a
Instagram y las de Instagram no llegaban a los PDF.

Quedó así: **una fuente por tema, con una copia publicada en Notion.**

- `specs/voz.md`: todas las reglas de texto, para todos los canales. Se
  publica en Notion como *✍️ Cómo escribimos*, que es lo que leen el equipo y
  las skills de Instagram
- `specs/diseno.md`: lo visual del sitio, los PDF y ahora también las placas.
  Se publica en Notion como *🎨 Cómo diseñamos*
- `CLAUDE.md` queda con un resumen corto y el puntero a los dos

- [x] Las cuatro guías breves pasadas por el conjunto completo de reglas:
      vuelve el principio operativo al cierre, PLAN vuelve a hablar de
      acciones y suma "Hecho:" en cada una, ENTUSIASMO recupera la
      contraposición y PILARES incorpora "puede vivirse como una pérdida o
      trabajarse como una reinvención"
- [ ] Las guías completas siguen con el lenguaje viejo

### Las reglas se escriben de inmediato (2026-09-23)

Marcel pidió no esperar a que una corrección aparezca dos veces: la regla se
escribe al primer caso, subiendo de la corrección a la intención, y si esa
intención no está clara se pregunta antes de generalizar. Actualizado en
`specs/voz.md` § 7, en `specs/diseno.md`, en `CLAUDE.md` y en las dos páginas
de Notion.

- [x] `specs/proyecto-claude.md`: qué va en el repo, en Notion, en las
      Instrucciones y en la Memoria del proyecto de claude.ai, con el bloque
      de instrucciones listo para pegar
- [ ] **Marcel:** pegar ese bloque en las Instrucciones del proyecto y, si se
      puede, conectar Notion al proyecto para que lea las guías en vivo

### Todo pasa a Notion (2026-09-23)

Marcel fijó el principio: **todo se documenta en Notion y se revisa just in
time**. Notion es la única superficie donde pueden escribir el chat, cowork,
Claude Code, las skills y el equipo, así que pasa a ser la fuente.

- [x] *✍️ Cómo escribimos* y *🎨 Cómo diseñamos* son ahora la fuente. Se les
      sumó la postura de escepticismo, la diferencia entre citas públicas y
      datos de investigación, las ilustraciones SVG, el estado del logo, y
      las reglas visuales del sitio y de los PDF
- [x] `specs/voz.md` quedó como copia que Claude Code sincroniza antes de
      escribir; `specs/diseno.md`, solo con la implementación en CSS
- [x] Los documentos 00 a 06 de agosto se migraron a *Programa vigente*, con
      las contradicciones resueltas a favor de lo más nuevo: 3 meses (espina
      recortada a 12 semanas, pendiente de Nicole), 4 horas en total, Sesión
      1 en dos encuentros, Cuatro Desgastes, Escenarios Complejos, "a los 95",
      peak, y **acción** en vez de decisión salvo en la Ficha de Decisiones
- [x] Catálogo de hábitos como base de datos (36 filas, incluidas las
      descartadas)
- [x] El checklist maestro y los pendientes de la memoria, como 53 tareas en
      *Tareas DTJ*, con una columna nueva *Área*
- [x] `specs/proyecto-claude.md` y `specs/indice-proyecto-claude.md`: el
      bloque para las Instrucciones, el texto para la Memoria y el índice
      para el Contexto del proyecto de claude.ai

**Desde acá, lo pendiente vive en Tareas DTJ**, no en este archivo.

### Limpieza de Notion (2026-09-23 y 24)

Auditoría completa de la página *Diseña tu Jubilación*: 28 acciones en Tareas
DTJ (área nueva *Orden de Notion*). Marcel aprobó reorganizar y mejorar, sin
tocar *Curso Referente Digital*; lo de datos sensibles sigue pendiente.

- [x] Página raíz como índice por secciones y un solo *Archivo*, con 17
      páginas movidas (nada se borró)
- [x] Página nueva *🎬 Cómo creamos contenido*, con lo rescatado del curso
      Referente Digital, los tips y Capacitación Marketing; ✍️ y 🎨 sumaron
      reglas (palabras, secuencia de venta, estructuras de copy, video,
      ilustraciones). `specs/voz.md` sincronizado
- [x] Flujo de contenido al día (regla inmediata, ejecución pausada) y
      frontera entre Tareas DTJ y Decisiones y notas
- [x] Prompts médicos viejos marcados como obsoletos
- [ ] Triage del Kanban antiguo: propuesta escrita en su tarea, espera
      visto bueno
