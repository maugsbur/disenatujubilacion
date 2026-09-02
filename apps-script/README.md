# Apps Script — DTJ · Backend

Escribe en las dos planillas y expone el endpoint que el Worker de Cloudflare
va a llamar en la Etapa 4. No envía correos — eso lo hace Brevo, desde el
Worker o desde donde se decida en la Etapa 5.

## 1. Crear las dos planillas

Créalas en la cuenta de Google del equipo (no en la personal), y compártelas
**solo** con las tres cuentas (Nicole, Marcel, Margarita), nunca por enlace
público. Antes de seguir: verificación en dos pasos activada en las tres.

**Archivo A — `DTJ · Personas`**, pestaña llamada exactamente `personas`,
con esta fila de encabezados (columna A a J):

```
id | email | fecha_alta | origen | consent_guardado | consent_guardado_fecha | consent_marketing | consent_marketing_fecha | version_texto | ultimo_contacto
```

**Archivo B — `DTJ · Respuestas`**, pestaña llamada exactamente `respuestas`,
con esta fila de encabezados (columna A a G):

```
id | guia | pregunta | pilar | valor | total_pilar | fecha
```

No hace falta crear la pestaña `solicitudes` a mano — el código la crea sola
la primera vez que hace falta, dentro del archivo de Personas.

## 2. Crear el proyecto de Apps Script

**El binding a una planilla que ya existe SOLO se puede hacer desde la
interfaz de Sheets — no hay ningún comando de clasp que ate un script a un
archivo existente.** (`clasp create --type sheets --parentId <ID>` no
sirve para esto: con `--type` definido, clasp ignora por completo
`--parentId` y siempre crea una planilla nueva — se confirmó leyendo el
código fuente de clasp 3.x, después de dos intentos fallidos tratando de
usarlo así.)

1. Desde el archivo `DTJ · Personas`: **Extensiones → Apps Script**. Esto
   crea (o abre, si ya existe) el proyecto *bound* a ese archivo — es lo
   que hace que el menú `DTJ · Privacidad` aparezca al abrirlo, y es un
   paso que no se puede saltar ni reemplazar con clasp.
2. Copia el **Id. de secuencia de comandos** (Script ID) desde el ícono de
   engranaje **Configuración del proyecto**.
3. Ahora sí, para subir el código: **copia y pega manualmente** el
   contenido de cada archivo de esta carpeta en un archivo nuevo del mismo
   nombre en el editor (Config, Utilidades, Personas, Respuestas, Codigo,
   DerechosARCO, Retencion — y borra el `Code.gs` vacío que trae por
   defecto). El manifiesto (`appsscript.json`) se edita desde
   **Configuración del proyecto → Mostrar "appsscript.json" en el editor**.

   *Alternativa con [clasp](https://github.com/google/clasp), una vez que
   ya tienes el Script ID del paso 2:*
   ```bash
   npm install -g @google/clasp
   clasp login
   cd apps-script          # ⚠️ tiene que ser ESTA carpeta, no la raíz del repo
   clasp clone TU_SCRIPT_ID --rootDir .
   ```
   `clone` trae de vuelta un `Code.gs` vacío y probablemente pisa
   `appsscript.json` con uno genérico — bórralo y revisa el manifiesto
   antes de seguir:
   ```bash
   rm Code.gs
   cat appsscript.json    # ¿sigue el bloque "webapp"? si no, restáuralo desde git
   clasp status            # confirma que solo aparecen los siete .gs + appsscript.json
   clasp push
   ```

   *Nota sobre versiones:* clasp 3.x renombró varios comandos. `push` y
   `status` siguen funcionando igual (son alias), pero **`clasp open` ya
   no existe** — ahora es `clasp open-script` (abre el editor del proyecto
   en el navegador; útil para confirmar que el push llegó a donde
   correspondía, sobre todo si entrar por Extensions → Apps Script desde
   la planilla no muestra los archivos — a veces es solo la pestaña vieja
   del editor, sin recargar).

## 3. Configurar las propiedades (el token y los IDs de los dos archivos)

El ID de cada planilla es la parte larga de su URL:
`https://docs.google.com/spreadsheets/d/`**`ESTE_ID`**`/edit`.

Genera un token largo y aleatorio, por ejemplo con:

```bash
openssl rand -hex 32
```

En el editor de Apps Script, abre `Config.gs`, reemplaza los `PEGAR_AQUI_...`
por los valores reales dentro de `configurarPropiedades()` — incluida
`BREVO_API_KEY` (Etapa 5: la misma llave que configuraste en el Worker,
ver `brevo/README.md` § 2), **ejecuta esa función una vez** (▶ en el
editor), y después revierte el archivo a los placeholders antes de
guardar/subir — así ningún secreto real queda escrito en el código ni en
git. Confirma que quedó bien con `revisarPropiedades()` (te muestra los
primeros caracteres de cada secreto, no el valor completo).

Guarda el token compartido en un lugar seguro — el Worker de la Etapa 4 lo
necesita para poder llamar a este endpoint.

## 4. Publicar como Web App

**Implementar → Nueva implementación → tipo: Aplicación web.**

| Campo | Valor |
|---|---|
| Ejecutar como | Yo (tu cuenta) |
| Quién tiene acceso | Cualquier usuario |

Copia la URL que te da (termina en `/exec`) — es el `APPS_SCRIPT_URL` que
el Worker va a necesitar en la Etapa 4.

⚠️ **Cada vez que cambies el código hay que crear una implementación nueva**
(o editar la existente con "Gestionar implementaciones" → ✏️ → nueva
versión) para que los cambios se reflejen en esa URL.

## 5. Instalar los disparadores

Una sola vez cada uno, ejecuta desde el editor (▶) — vas a tener que
autorizar los permisos del script la primera vez:

- `instalarTriggerRetencion()` — retención a 18 meses (Etapa 3)
- `instalarTriggerReintentoCorreos()` — reintento de correos que Brevo
  rechazó, cada 30 minutos (Etapa 5, ver `brevo/README.md` § 6)

## 6. Probar que responde

```bash
curl -X POST 'TU_URL_TERMINADA_EN_/exec' \
  -H 'Content-Type: application/json' \
  -d '{
    "token": "EL_TOKEN_QUE_CONFIGURASTE",
    "email": "prueba@ejemplo.com",
    "guia": "DOMINO",
    "origen": "DOMINO",
    "consentGuardado": true,
    "consentMarketing": false,
    "versionTexto": "autodiagnostico-v1-2026-09",
    "totales": {"proposito": 15, "fisico": 20, "mental": 18, "social": 10, "finanzas": 22},
    "respuestas": [{"pregunta": "pregunta de prueba", "pilar": "social", "valor": 2}]
  }'
```

Debería responder `{"ok":true,"uuid":"...","personaNueva":true,"respuestasGuardadas":1}`
y aparecer una fila en cada planilla. Repite el POST con el mismo correo:
la fila de Personas se actualiza en vez de duplicarse (`personaNueva:false`).

Cuando termines de probar, usa el menú **DTJ · Privacidad → Eliminar por
correo…** en el archivo de Personas para borrar `prueba@ejemplo.com`.

## Qué falta después de esto (Etapa 4)

El Worker de Cloudflare es quien realmente valida el payload, filtra bots y
limita por IP — este endpoint hace una validación mínima (token, formato de
correo, honeypot) porque técnicamente queda expuesto en internet, pero **no
está pensado para recibir tráfico directo del navegador.**

Nota importante para cuando construyamos el Worker: los Web Apps de Apps
Script **no exponen headers HTTP personalizados** (no existe `e.headers`).
El token compartido tiene que ir dentro del cuerpo JSON (campo `"token"`),
no como `Authorization` — el Worker lo agrega al payload antes de reenviarlo,
nunca confiando en un token que mande el navegador.
