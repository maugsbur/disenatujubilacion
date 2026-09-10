# specs/

Rebanada mínima de spec-driven development para este proyecto. Deliberadamente
delgada: acá no hay cobertura de tests, tipado estricto ni documentación en
inglés, porque no calzan con un sitio de diez páginas sin build que leen dos
personas no desarrolladoras.

## Por qué existe esta carpeta

Mira qué costó tiempo de verdad al construir este sitio: casi nada fue lógica
propia. Fue **comportamiento no documentado de terceros** — `clasp create`
ignorando `--parentId`, Cloudflare Pages ignorando las variables del
dashboard, Apps Script sin headers HTTP, Brevo rechazando `params:{}`, la
regla 210 mm ≡ 1024 px de wkhtmltopdf.

Cada una costó caro descubrirla y se evapora si vive solo en una conversación.
El caso que lo prueba: el repo `jubilarme-landing-hijos` **ya tenía
documentado** lo de las variables de Cloudflare en sus *Known Gotchas*, y aun
así lo redescubrimos desde cero acá, gastando una sesión completa. No era
falta de conocimiento: era falta de un lugar donde el conocimiento viajara.

Eso es lo que estas dos carpetas resuelven: `CLAUDE.md` para las restricciones
que se cargan en cada sesión, `specs/` para los contratos y las decisiones de
comportamiento.

## Qué hay

| Spec | De qué se trata |
|---|---|
| [`contrato-datos.md`](contrato-datos.md) | El payload que cruza navegador → Worker → Apps Script → Sheets → Brevo. La superficie de mayor riesgo del proyecto |
| [`consentimiento.md`](consentimiento.md) | Los dos regímenes de consentimiento y qué hacer el 1 de diciembre de 2026 |

## Cómo se trabaja

1. **Antes de tocar el pipeline, lee el spec que corresponda.** Si vas a
   cambiar comportamiento, escríbelo ahí primero.
2. **Cuando descubras una restricción de plataforma, anótala en `CLAUDE.md`**
   en el momento, no después. El costo de anotarla es un minuto; el de
   redescubrirla, ya lo medimos.
3. **Un campo o comportamiento nuevo se documenta antes de existir**, no
   después de funcionar.
4. Los specs describen **qué debe pasar y por qué**, no cómo está
   implementado. El código cambia; la intención y la restricción, mucho menos.
