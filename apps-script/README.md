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

1. Desde el archivo `DTJ · Personas`: **Extensiones → Apps Script**. Esto lo
   deja *bound* a ese archivo, que es lo que necesitas para que el menú
   `DTJ · Privacidad` aparezca al abrirlo.
2. Borra el `Code.gs` vacío que trae por defecto.
3. Copia el contenido de cada archivo de esta carpeta a un archivo nuevo del
   mismo nombre en el editor (Config, Utilidades, Personas, Respuestas,
   Codigo, DerechosARCO, Retencion). El manifiesto (`appsscript.json`) se
   edita desde **Configuración del proyecto → Mostrar "appsscript.json"**.

   *Alternativa más rápida si ya usas [clasp](https://github.com/google/clasp):*
   ```bash
   npm install -g @google/clasp
   clasp login
   cd apps-script          # ⚠️ tiene que ser ESTA carpeta, no la raíz del repo
   clasp create --type sheets --title "DTJ · Backend" --parentId <ID_DEL_ARCHIVO_PERSONAS> --rootDir .
   ```
   Si por error corres `clasp create` desde la raíz del repo (`disenatujubilacion/`
   en vez de `disenatujubilacion/apps-script/`), te va a crear ahí un
   `.clasp.json` y un `appsscript.json` nuevos y genéricos, pisando nada
   importante pero apuntando al lugar equivocado — `clasp push` intentaría
   subir *todo* el repo (`site/`, `functions/`, etc.) como si fuera código
   de Apps Script. El proyecto en Google igual queda bien creado (atado al
   archivo de Personas); solo hay que mover `.clasp.json` a esta carpeta y
   borrar el `appsscript.json` de sobra en la raíz. Confirma con
   `clasp status` (parado en `apps-script/`) que solo aparecen los siete
   `.gs` y el `appsscript.json` de acá antes de hacer push:
   ```bash
   clasp status
   clasp push
   ```

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
