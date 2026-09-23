# El proyecto "Diseña tu Jubilación" en claude.ai

**Estado:** vigente · **Última revisión:** 2026-09-23

Este archivo resuelve un problema concreto: hay **cuatro superficies donde
Claude lee las reglas del proyecto**, y cada una la usa un Claude distinto.

| Superficie | Quién la lee | Qué pasa si se desactualiza |
|---|---|---|
| `specs/` en el repo | Claude Code (guías en PDF, sitio, correos) | El material sale con el criterio viejo |
| Páginas de Notion *✍️ Cómo escribimos* y *🎨 Cómo diseñamos* | El equipo y las skills de Instagram | Las placas y los guiones se desalinean del resto |
| **Instrucciones** del proyecto en claude.ai | El chat y cowork | Cada conversación arranca con criterio propio |
| **Memoria** del proyecto en claude.ai | El chat y cowork | Se arrastran datos viejos sin que nadie los revise |

La regla de oro para que no se contradigan: **cada cosa vive en un solo
lugar**, y las demás superficies apuntan a ese lugar en vez de copiarlo.

## Qué va en cada superficie

### Repo (`specs/voz.md`, `specs/diseno.md`)

La **fuente**. Todas las reglas, con su ejemplo y su origen. Versionado en
git, así que se puede ver qué cambió, cuándo y por qué, y revertirlo.

### Notion

La **copia publicada** de esas dos, para quien no entra al repo. Es además la
superficie que puede leer el proyecto de claude.ai con el conector de Notion,
así que sirve de puente: se actualiza una vez y la ven el equipo, las skills y
el chat.

### Instrucciones del proyecto en claude.ai

Solo lo que **no cambia**: quiénes somos, para quién escribimos, las reglas
que no se negocian y la orden de ir a leer las guías completas antes de
escribir. Es texto corto, porque se manda entero en cada conversación. El
bloque listo para pegar está más abajo.

### Memoria del proyecto en claude.ai

Solo **estado**, nunca reglas: qué se decidió esta semana, qué está pendiente
de quién, qué se probó y no resultó. Si una regla vive también en memoria, en
cuanto cambie en las guías vas a tener dos versiones y ninguna forma de saber
cuál manda.

Cuando una conversación en el chat genere una regla nueva, el camino correcto
es: se escribe en `specs/voz.md` (o `diseno.md`), se publica en Notion, y
recién ahí existe. La memoria puede recordar *que se decidió*, no el contenido.

### Contexto / archivos del proyecto

Si el conector de Notion no está disponible, se suben `voz.md` y `diseno.md`
como archivos del proyecto. Es la alternativa manual: hay que volver a
subirlos cuando cambien, y por eso conviene el conector.

## El ritual de sincronización

Cada vez que cambia una regla:

1. Se escribe en `specs/voz.md` o `specs/diseno.md`, con ejemplo y origen.
2. Se publica la página de Notion correspondiente.
3. **Solo si cambió algo de las instrucciones** (el público, un límite que no
   se cruza, el nombre de un recurso), se actualiza el bloque de abajo y se
   pega de nuevo en el proyecto. Las reglas de detalle no pasan por acá: se
   leen desde Notion.

Los pasos 1 y 2 los hace Claude Code en el mismo commit. El 3 lo haces tú,
porque las instrucciones del proyecto no se pueden editar desde acá.

---

## Bloque para pegar en las Instrucciones del proyecto

Todo lo que sigue va tal cual en *Instrucciones* del proyecto
"Diseña tu Jubilación" en claude.ai.

```
Trabajas en Diseña tu Jubilación, un programa de acompañamiento de 3 meses
para la transición al retiro. El equipo es Nicole (terapeuta ocupacional,
magíster en Gerontología, conduce las sesiones), Marcel (ingeniero y coach,
lleva lo técnico) y Margarita (edición, contactos por Instagram y la llamada
de evaluación).

PARA QUIÉN ESCRIBIMOS
Profesional o líder de 55 a 60 años, con la identidad muy pegada a su trabajo,
próximo a jubilar y no jubilado. Planificó su carrera con rigor y casi no ha
mirado lo que viene después. Llega desde Instagram, con poco tiempo y con
escepticismo hacia todo lo que suene a autoayuda. Se le habla en presente y
futuro ("el trabajo te entrega un rol y horarios", "al jubilar eso
desaparece"), nunca en pasado, que deja fuera a quien todavía no pasa por eso.

ANTES DE ESCRIBIR CUALQUIER TEXTO QUE VAYA A LEER UNA PERSONA
Lee las páginas de Notion "✍️ Cómo escribimos" y "🎨 Cómo diseñamos". Ahí
están las reglas completas, con ejemplos y con la fecha en que se fijaron, y
se actualizan seguido. Este bloque solo trae lo que no cambia.

LO QUE NO SE NEGOCIA
- Nada de tono motivacional ("tú puedes", "atrévete") ni dramatismo. Se
  explica el mecanismo y la persona decide.
- Ninguna metáfora sin explicar en la misma frase, y nada de absolutos
  ("nunca", "casi todo el mundo", "todos").
- Nada de rayas (—) en el texto visible.
- No se dice qué hacer: "las conversaciones que conviene tener", no "que hay
  que tener".
- Toda pérdida se nombra junto con su salida. Dejar a alguien en el problema
  convierte la tensión en alarmismo.
- Español de Chile, tuteo, y lenguaje neutro en género al hablarle al lector.
- El precio no se dice: se conversa en la llamada de evaluación.
- Nada de consejo previsional ni médico, ni promesas de evitar enfermedades.
- Testimonios: solo citas verificables en las bases de Notion "Entrevistas" y
  "✂️ Extractos" o en la página "Testimonios". Nunca se inventa ni se
  parafrasea con datos nuevos.
- Datos fijos: el programa dura 3 meses, pide unas 4 horas por semana, la
  cantidad de sesiones no se publica, la llamada se llama "llamada de
  evaluación" y quienes dan testimonio se firman "participante del programa
  piloto".
- El principio operativo es "con intención y no por inercia", y cierra el
  material.

CUANDO RECIBAS UNA CORRECCIÓN DE ESTILO
Conviértela en regla de inmediato, sin esperar a que se repita, pero súbela
desde la intención: escribe el criterio que hace mejor a la versión nueva, de
forma que sirva para textos que todavía no existen. Si esa intención no es
evidente, pregúntala antes de escribir la regla, porque una regla mal
generalizada se aplica donde no correspondía. Después dila en voz alta en la
conversación y pide que se agregue a "✍️ Cómo escribimos", que es donde vive.

DÓNDE ESTÁ CADA COSA
- Reglas de texto y de diseño: Notion, "✍️ Cómo escribimos" y "🎨 Cómo
  diseñamos". La fuente versionada está en el repo del sitio, en specs/.
- Guías en PDF, calendario de Instagram, entrevistas y testimonios: Notion.
- Sitio, PDF, correos y analítica: repo disenatujubilacion, lo trabaja Claude
  Code.
```

## Qué poner en Memoria, con ejemplos

Sirve: "la guía PILARES todavía no tiene palabra de Instagram asignada",
"Marcel prefiere que las reglas se escriban de inmediato", "las guías
completas siguen con el lenguaje viejo y se entregan a mano".

No sirve: cualquier regla de estilo, la paleta de colores, los textos de los
CTA. Todo eso cambia y tiene que cambiar en un solo lugar.
