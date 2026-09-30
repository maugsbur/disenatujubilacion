# Skills del proyecto (copia de respaldo)

COPIA. No se edita acá.

La fuente es la base "Skills del proyecto" en Notion, dentro de la página
"🧰 Skills de Claude" (https://app.notion.com/p/3e523cb6e7af81b78e4ee8f19d686d79),
desde el 24/09/2026. Esta carpeta existe para que las skills sigan
disponibles si se pierde la conexión o el acceso a Notion, y para que git
guarde su historial.

Cuando una skill cambia en Notion, Claude Code la descarga
(`notion-download-skill`) y pone al día esta copia.

| Skill | Qué hace |
|---|---|
| proponer-ideas-ig | Propone ideas y las deja en Propuesta |
| procesar-decisiones-ig | Ejecuta lo decidido y convierte cada corrección en regla |
| planificar-calendario-ig | Agenda respetando la semana de historias, la mezcla y los hilos |
| escribir-guion-ig | Escribe el guion de una pieza |
| disenar-placas-ig | Genera las placas PNG (con `render.py`) |
| investigar-evidencia-ig | Llena la base Evidencia y propone piezas respaldadas |

**Reescritas desde cero el 30/09/2026** *(pedido de Marcel)*. Cada skill es
solo procedimiento: qué produce, qué leer antes, pasos, cuándo está
terminada y qué se entrega. El contexto (voz, embudo, semana de historias,
palabras de CTA, paleta) vive en las páginas de Notion que cada skill enlaza,
y lo común a todas (bases, dónde va cada salida) en 🤝 Flujo de trabajo con
Claude › *Lo común a las skills de Instagram*.

## Las skills de la cuenta de claude.ai

La carpeta `cuenta/` tiene la versión para subir al plugin de la cuenta
(chat y cowork): un archivo corto por skill que dice cuándo usarla y le
pide a Claude leer la skill completa en Notion. Así hay una sola versión
que mantener, la de Notion.
