# Diseña tu Jubilación — contexto del proyecto

Sitio de captación para un programa de acompañamiento de 3 meses en la
transición al retiro. Público: profesionales y líderes próximos a jubilar
cuya identidad está anclada al trabajo. Chile y Latinoamérica, ticket
USD 1.000, ingreso continuo sin cohortes.

**El sitio no es el funnel — Instagram lo es.** El sitio cumple tres
trabajos: convertir atención en un correo identificado, hacer creíble el
programa, y calificar y armar la llamada de evaluación de Margarita
(Calendly, 45 min). Todo lo que no sirva a uno de esos tres es ruido.

## Quiénes

| | Rol | Dónde |
|---|---|---|
| **Nicole** | Terapeuta ocupacional, magíster en Gerontología, docencia e investigación. Conduce sesiones. Punto de contacto para derechos de datos | Viña del Mar, Chile |
| **Marcel** | Ingeniero y coach, background en ciencias y computación. Metodologías en sector privado, ONGs y la ONU. Lleva lo técnico | Dinamarca |
| **Margarita** | Edición y ventas. Contactos por Instagram y la llamada de venta. El Calendly es suyo | Dinamarca |

Dos de tres están en la UE: la pregunta de si aplica GDPR está abierta y
anotada para el abogado. No la des por resuelta en ninguna dirección.

## Idioma y tono

- **Todo en español**, incluidos código, comentarios y documentación. Nicole
  y Margarita leen estos documentos y no son desarrolladoras.
- El público **castiga el tono motivacional**. Nada de "tú puedes" ni
  divulgación pop. Los mecanismos se explican sin culpa y sin arenga.
- Principio operativo: *"Con intención y no por inercia."* No decimos qué
  hacer; mostramos dónde está la persona con datos y ella decide.
- Se señala toda afirmación sin respaldo, incluidas las propias. Si una
  cifra o un mecanismo no se puede sostener, se dice.
- **Nada de rayas (—) en el copy visible**, ni del patrón "no es X, es Y"
  ("No es una historia de motivación: es un método"). El público los lee
  como señal de texto hecho con IA. Se reemplazan por comas, puntos o dos
  puntos, y la frase se reescribe en positivo. En comentarios de código y
  documentación interna da igual.
- **Lenguaje neutro en género** cuando se habla al lector ("Quieres tomarte
  esta etapa…", no "Estás dispuesto…"). La mitad del público son mujeres.
- **Testimonios: solo citas verificables** en Notion: la base "Entrevistas"
  (versiones cortas), la base "✂️ Extractos (videos de entrevistas)" (citas
  textuales, se pueden pulir sin cambiar el sentido) o la página
  "Testimonios". Todas las personas entrevistadas dieron consentimiento.
  Ojo: en Extractos, "Requiere permiso puntual" y "No publicable" son por
  terceros identificables, datos de salud, precios o críticas, no por
  consentimiento. Esas no se usan.
- La llamada con Margarita se llama **llamada de evaluación** en todo el
  sitio. No "sesión de diagnóstico": choca con "autodiagnóstico".
  En botones se abrevia: **"Agendar evaluación gratuita"** y **"Hacer test
  de autodiagnóstico"**.
- La duración se dice **3 meses**. No "13 semanas" (obliga a hacer la
  cuenta) ni "90 días" (suena a reto de Instagram, justo el tono que este
  público castiga).
  Dedicación: **unas 4 horas por semana**. La cantidad de sesiones no se
  publica, se conversa en la llamada de evaluación.
- Quienes dan testimonio se firman **"participante del programa piloto"**,
  no "ex alumno/a de Jubilar.me" (el público nuevo no conoce esa marca).
  Las citas de Silvia en el calendario de Instagram de Notion ("toda la vida
  me dediqué a otros", "el propósito me pegó fuerte") no están en su
  transcripción: no se usan. La única verificada es la de Extractos (0:23).

## Arquitectura

```
site/              → lo que Cloudflare Pages publica (output dir = "site")
  index.html          landing
  autodiagnostico/    única página interactiva: 25 preguntas + resultado, una sola página que cambia de vista
  plan/ hablar/ carlos/ pilares/  páginas de captura de las guías PDF
  privacidad/
  assets/pdfs/        los PDF de las guías, en rutas aleatorias, sin enlazar (Brevo los baja por URL)
  _redirects _headers
functions/api/submit.js  → Pages Function: valida, limita por IP (KV), honeypot, llama a Brevo, reenvía a Apps Script
apps-script/       → Web App atado a la planilla "DTJ · Personas": escribe en Sheets, cola de reintento de correo, derechos ARCO
lead-magnets/      → fuentes de los PDF (editar los .py, NO los .html). Cada guía
                     tiene versión breve de 2 páginas (build_breves.py, la que se
                     adjunta al correo) y versión completa de 8 (build_*.py, se
                     entrega a mano a quien pide más)
brevo/             → plantillas de correo y guía de configuración
specs/             → contratos y decisiones de comportamiento. Leer antes de tocar el pipeline
```

Flujo de un envío: navegador → `/api/submit` (Worker) → Brevo (correo) →
Apps Script (Sheets). Si Brevo falla, el Worker le pasa a Apps Script el
cuerpo exacto que iba a mandar, y la cola de `CorreoPendiente.gs` lo
reintenta cada 30 min.

## ⚠️ Restricciones de plataforma — cada una costó caro descubrirla

**Cloudflare Pages ignora las variables de texto plano del dashboard cuando
existe `wrangler.toml`.** Solo respeta ahí las marcadas como **Secret**. Las
no secretas van en `wrangler.toml` § `[vars]`. Esto costó una sesión completa
de diagnóstico; el síntoma es `config_del_worker_incompleta` con todo
aparentemente bien configurado. (El repo `jubilarme-landing-hijos` ya lo
tenía documentado en sus Known Gotchas.)

**Agregar o cambiar un Secret en el dashboard de Cloudflare Pages no se
aplica solo.** Pasó dos veces con `POSTHOG_PROJECT_TOKEN` y `POSTHOG_HOST`:
`/api/config` seguía devolviendo el valor viejo (o `{}`) hasta forzar un
deploy nuevo (basta un commit vacío y push). No hace falta reconstruir
nada — es solo que Pages Functions no relee las variables de un deployment
ya publicado.

**Apps Script Web Apps no pueden leer headers HTTP personalizados.** No
existe `e.headers`. El token compartido viaja **dentro del cuerpo JSON**,
nunca como `Authorization`.

**Un POST a un Web App de Apps Script devuelve 302** hacia
`script.googleusercontent.com`. Con `curl` hace falta `-L`. Y si `doPost`
lanza una excepción sin capturar, Google responde con una **página de error
de Drive** (en el idioma de la cuenta), no con un error del script — por eso
`doPost` está envuelto en try/catch. Sin eso, cualquier bug parece un
problema de permisos.

**`clasp create --type sheets --parentId <ID>` ignora el `parentId`.**
Confirmado leyendo el código de clasp 3.x: con `--type` definido siempre
crea una planilla nueva. Atar un script a una planilla existente **solo se
puede desde Extensiones → Apps Script en Sheets**; después se conecta con
`clasp clone <scriptId>`, nunca con `create`.

**clasp 3.x renombró comandos.** `create`, `push` y `status` siguen por
alias; `clasp open` ya no existe — ahora es `clasp open-script`.

**Brevo rechaza `params: {}`** con `"params is blank"`. Las guías sin
parámetros dinámicos omiten el campo entero en vez de mandarlo vacío.

**wkhtmltopdf fuerza un viewport de 1024 px** y aplica smart-shrinking que no
se puede desactivar. Los fuentes están en mm/pt y hay que convertirlos a px
tomando **210 mm ≡ 1024 px** antes de renderizar, o el contenido sale al 77%.
La función `to_px()` de `build_common.py` lo hace.

**wkhtmltopdf convierte a imagen cualquier texto con `opacity`.** El
párrafo sale rasterizado y se ve pixelado en el PDF, sin ningún error. Por
eso en `lead-magnets/` no se usa `opacity` (ni `rgba()`) en texto: los
grises son colores sólidos ya mezclados contra su fondo. Para comprobarlo,
un PDF sano no tiene ningún `/XObject` de tipo `/Image`.

**El "Enviar como" de Gmail muere en enero de 2027.** Google lo restringe
durante 2026. Las tres cuentas del equipo dependen de él hoy para escribir
desde `contacto@disenatujubilacion.com`. Por eso el correo transaccional va
por Brevo y no por Gmail. Hay que resolverlo antes de esa fecha.

**Un despliegue de Apps Script no se actualiza solo al hacer `clasp push`.**
Hay que ir a Implementar → Gestionar implementaciones → Nueva versión. Y
transferir la propiedad del archivo **no** cambia el "Ejecutar como" de un
despliegue ya publicado.

## Cómo verificar cambios

No hay arnés de tests. Lo que caza bugs de verdad acá es `curl` contra
producción, porque el riesgo vive en integraciones de terceros:

```bash
curl -s -X POST https://disenatujubilacion.com/api/submit \
  -H 'Content-Type: application/json' \
  -d '{"email":"prueba@ejemplo.com","guia":"DOMINO","totales":{...}}'
```

Ojo: el límite por IP es de **6 envíos cada 60 segundos** — un script que
sondee más rápido se auto-bloquea y el `429` se confunde fácil con otra
falla. Usa correos de prueba distintos en cada intento; las filas se
acumulan y es fácil terminar leyendo una vieja.

Después de probar, limpia con el menú **DTJ · Privacidad → Eliminar por
correo** en la planilla de Personas.

## Convenciones

- **Sin build step.** HTML, CSS y JS a mano. Es una virtud en tráfico móvil
  de Instagram, no una deuda.
- Mobile-first siempre: la mayoría del tráfico llega del navegador embebido
  de Instagram. Objetivos de toque ≥48px.
- Nada de SEO ni contenido: nadie llega por Google, y las guías están en
  `noindex` a propósito.
- Secretos solo en el dashboard de Cloudflare como Secret o en las
  propiedades del script de Apps Script. Nunca en el repo.

## Antes de tocar el pipeline

Lee `specs/`. El contrato de datos cruza cuatro codebases en dos lenguajes
y ya causó dos bugs por desajuste. Si vas a cambiar comportamiento, escribe
primero qué debe pasar y qué restricción descubriste.
