# Spec · Régimen de consentimiento y el switch de diciembre

**Estado:** decidido, pendiente de implementar · **Última revisión:** 2026-09-10
**Fecha que gobierna este spec:** 1 de diciembre de 2026 — entrada en
vigencia de la Ley 21.719.

## Qué se decidió y por qué

Hasta que entre en vigencia la ley, el objetivo del negocio es **armar una
base para conocer al público**: guardar siempre las respuestas del
autodiagnóstico, no solo las de quien marca una casilla.

La decisión de Marcel (2026-09-10) fue la versión honesta de eso:

> **Guardar siempre _y quitar la casilla_**, en vez de preguntar y guardar
> igual.

El razonamiento importa y hay que preservarlo: preguntar *"¿autorizas que
guardemos tus respuestas?"* e ignorar la respuesta no es una zona gris que
dependa de qué ley esté vigente — es afirmarle algo falso a la persona. No
preguntar y declarar con claridad qué se guarda es honesto. Preguntar e
ignorar, no.

**Lo que NO cambia:**

- El correo sigue siendo obligatorio. El argumento que lo sostiene —se pide
  porque es necesario para entregar lo que la persona pidió— no se toca.
- La casilla de **marketing** sigue existiendo, sigue siendo opcional, sin
  premarcar, y sigue decidiendo de verdad. Es una finalidad distinta y
  separada.

## Los dos regímenes

El comportamiento anterior **no se borra: queda detrás de una bandera**, para
poder reintegrarlo sin rehacerlo.

| | `PRE_LEY` (activo hoy) | `LEY_21719` (a activar) |
|---|---|---|
| Correo | Obligatorio | Obligatorio |
| Casilla "guardar mis respuestas" | **No existe** | Visible, opcional, sin premarcar |
| ¿Se guardan las respuestas? | Siempre | Solo si la marcó |
| Qué se le dice a la persona | Declaración clara en el formulario de qué se guarda y para qué | La casilla, más el texto de la política |
| Casilla de marketing | Opcional, real | Opcional, real |

### Cómo se implementa la bandera

Una sola constante gobierna el comportamiento en los dos lados:

- **Worker** (`functions/api/submit.js`): decide si fuerza `consentGuardado`
  a `true` o si respeta lo que llegó del formulario.
- **Apps Script** (`Codigo.gs`): decide si `escribirRespuestas_()` se llama
  siempre o solo con `consentGuardado === true`.

La lógica de ambos caminos queda escrita en el código, no comentada ni
eliminada. Cambiar de régimen debe ser cambiar un valor, no reescribir.

El front (`autodiagnostico/index.html`) muestra u oculta la casilla según el
mismo régimen, y el texto declarativo acompaña al que esté activo.

## El marcador de cohorte pre-ley

**Este es el punto que ahorra el dolor de diciembre.** Sin él, el 1 de
diciembre habría una base donde no se puede distinguir bajo qué régimen se
captó cada persona, y separarlas sería arqueología.

Cada fila de `personas` queda marcada con el régimen bajo el cual se captó:

- `version_texto` ya existe y ya cumple parte de esta función; los valores
  tienen que ser disciplinados y nombrar el régimen.
- Además, una **columna explícita** de régimen en la planilla — porque esa
  planilla la leen Nicole y Margarita, que no son desarrolladoras, y un
  campo llamado `version_texto` no le dice nada a nadie a simple vista.

Con eso, en diciembre la pregunta *"¿a quiénes captamos antes de la ley?"* es
un filtro, no una investigación.

## Qué hay que hacer el 1 de diciembre de 2026

Lista de verificación, para que ese día sea mecánico:

- [ ] Cambiar la bandera a `LEY_21719` en el Worker y en Apps Script
- [ ] Volver a mostrar la casilla de guardado en el autodiagnóstico
- [ ] Actualizar `version_texto` al valor del nuevo régimen
- [ ] Actualizar la **política de privacidad** (`site/privacidad/`): hoy su
      sección 3 declarará que guardar respuestas es parte del servicio; vuelve
      a ser consentimiento separado y opcional
- [ ] Actualizar la sección 3 de `08-cumplimiento-datos.md` — documento de
      Marcel, no se edita desde acá
- [ ] **Decidir qué pasa con la cohorte pre-ley.** Es la decisión de fondo y
      no la resuelve el código: o se pide re-consentimiento, o se purgan las
      respuestas de quienes no lo den. Hay que llegar con esto conversado con
      el abogado, no improvisado ese día
- [ ] Verificar que el disparador de retención a 18 meses sigue activo

## Advertencias que no dependen de diciembre

Se dejan escritas para que nadie las redescubra ni las confunda con el
calendario chileno:

- **La Ley 19.628 ya existe** desde 1999. Es más débil y no tiene agencia
  fiscalizadora hasta que la 21.719 la cree, pero existe hoy.
- **La pregunta del GDPR no depende de diciembre.** Dos de las tres personas
  del equipo están establecidas en Dinamarca. Si aplica, aplica ahora. Está
  anotada para el abogado aliado en `08-cumplimiento-datos.md` §8 y sigue
  abierta.
- Cambiar quién es dueño de los archivos de Drive **no cambia** ese análisis:
  depende de dónde están establecidas las personas que deciden y acceden, no
  de en qué cuenta vive el archivo.

## Alcance del cambio

Tocar esto no es borrar un `<input>`. Cruza cinco lugares:

1. `site/autodiagnostico/index.html` — la casilla y el texto declarativo
2. `site/assets/js/autodiagnostico.js` — qué manda en `consentGuardado`
3. `functions/api/submit.js` — la bandera del lado del Worker
4. `apps-script/Codigo.gs` — la compuerta de `escribirRespuestas_()`
5. `site/privacidad/index.html` — la base de licitud declarada

Las páginas de captura (`plan`, `hablar`, `carlos`) no tienen respuestas que
guardar, así que solo las toca el texto, no la lógica.
