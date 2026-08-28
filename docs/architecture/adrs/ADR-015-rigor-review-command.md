# ADR-015 — El séptimo comando: modo de revisión con rigor, contrato único y frontera con los seis existentes

## Estado

Proposed

## Contexto

El producto tiene seis comandos y **ninguna regla escrita para decidir el séptimo**. `ESTADO-DEL-PROYECTO.md` §1.3 registra además que *«nada revisa el borrador propio antes de que salga con su firma»*, y lo llama el único hueco del oleoducto actual.

El pase real del 2026-08-27/28 añadió tres hechos:

1. **El método más útil de todo el pase no fue ninguna de las seis skills.** Fue `docs/skills-support/workflows/20-judicial-rigor-review.md`, ejecutado a mano leyendo el dossier. Produjo los 14 hallazgos que sostienen todo el trabajo entregado sobre el expediente [radicado del expediente].
2. **La usuaria real lo pidió por su nombre funcional:** *«soy contradictor interno»*. No pidió redactar: pidió poner a prueba.
3. **El contrato ya está escrito y es el único del corpus convertible en `SKILL.md` sin inventarle la forma**: trece campos por hallazgo y cinco veredictos cerrados.

Y un problema que este ADR debe resolver, no heredar: **la misma capacidad está descrita en seis archivos con dos contratos incompatibles** —`08-adversarial-review-and-decision-support.md` (ficha de 7 campos), `adversarial-review/judicial-rigor.md` (21 líneas), `workflows/20` (ficha de 13 campos), `workflows/08`, `skill-candidates/adversarial-review.md` y `evals/adversarial-benchmark.md`—. `08` enlaza a `adversarial-review/*` y **nunca a `workflows/20`**. Quien implemente siguiendo el índice equivocado construye otra cosa.

## Decision

### 1. Se crea `revision-de-rigor` como séptimo comando

Nombre en español, como los otros seis salvo el que ya está señalado por H-09. Objeto: **poner a prueba una conclusión, un escrito, un borrador o un expediente, con una sola pregunta** — ¿qué conclusión no se puede sostener rigurosamente con el material disponible?

### 2. El contrato es el de `workflows/20`, y los otros cinco archivos dejan de ser fuente

Trece campos por hallazgo: `finding_id`, `mode`, `target`, `attack`, `reason`, `case_references`, `legal_sources`, `severity`, `possible_consequence`, `missing_information`, `recommended_remediation`, `residual_risk`, `support_status`.

Cinco veredictos globales, **vocabulario cerrado**: `ROBUST` · `DEFENSIBLE_WITH_RISKS` · `MATERIAL_WEAKNESSES` · `HIGH_RISK` · `INSUFFICIENT_BASIS`. Describen la **calidad del soporte revisado**; no significan «ganará», «perderá», «aprobado» ni «decisión correcta», y el SKILL debe decirlo con esas palabras.

Los otros cinco archivos quedan como material histórico. **La ficha de 7 campos de `08` queda supersedida.**

### 3. El lenguaje de riesgo calibrado baja al SKILL

Es la pieza que ninguna de las seis skills tiene: **todas tienen listas de prohibiciones y ninguna dice cómo se escribe una advertencia legítima.** Sin ese permiso el modelo hace una de dos cosas, ambas malas: se calla el riesgo, o lo dice mal.

Permitido: *«existe una vía seria para controvertir este punto»*, *«la prueba incorporada no permite sostener con seguridad esta conclusión»*, *«una contraparte razonable podría alegar X con base en Y»*.

Prohibido: *«esta demanda se gana»*, *«el caso está ganado»*, *«seguro el juez fallará a favor»*.

### 4. Falsabilidad obligatoria: cada hallazgo dice qué lo refutaría

Añadido sobre `workflows/20` a partir del pase real. Un hallazgo sin condición de refutación **no es un hallazgo, es una opinión**. En el pase, esa columna hizo que el hallazgo más grave —la descripción del objeto en el auto— se entregara diciendo cuál era la comprobación que podía tumbarlo, que además era la única que dependía de un error de lectura propio.

### 5. Observación sin base se marca, no se calla ni se disfraza

`UNSUPPORTED_REVIEW_OBSERVATION` es obligatorio y se entrega como tal. No se presenta como defecto confirmado y no se elimina: callarla es decidir por la profesional.

### 6. Frontera con los seis comandos existentes

| Comando | Objeto | Pregunta |
|---|---|---|
| `revisar-documento` | **Una pieza recibida** | ¿Qué dice, qué pide, qué decide? |
| `revision-de-rigor` | **Una conclusión, un escrito propio o un expediente** | ¿Qué de esto no se sostiene? |

`revisar-documento` tiene prohibido comparar con el expediente; `revision-de-rigor` **existe para comparar**. No se solapan: uno describe una pieza, el otro pone a prueba un razonamiento. La prueba ácida: si la pregunta se responde leyendo una sola pieza, no es este comando.

### 7. Simetría obligatoria cuando el objeto es un expediente

Descubierta en el pase, no en el dossier. Cuando lo revisado es un expediente con dos partes, **los defectos del acto de la autoridad y las debilidades del escrito de una parte se buscan con el mismo rigor**, y el informe lo dice explícitamente. Un informe que solo halla defectos en un lado suele estar mirando con un ojo, y en contexto de autoridad eso es además un vicio.

### 8. Este comando no delega ninguna decisión, y en contexto de autoridad menos

No determina hechos probados, no valora prueba, no declara parcialidad, no dice qué norma aplica, no calcula términos, no pronostica resultado, no redacta acto oficial ni proyecto de decisión. Cuando quien lo usa es una autoridad, el comando funciona —el pase lo demuestra— pero **el alcance V0 no delega decisiones** y el SKILL debe repetirlo en su primera sección.

### 9. Puede correr sin hechos aprobados, y lo dice

A diferencia de `redactar-escrito`, este comando **no exige** el archivo ` - REVISADO`: revisar es precisamente lo que se hace antes de aprobar. Pero cuando trabaja sobre material no aprobado **lo declara en el encabezado**, porque sus hallazgos citan localizadores que nadie ha comprobado.

## Invariantes derivados

1. **Todo hallazgo lleva los trece campos.** Un hallazgo incompleto no se entrega a medias: se entrega diciendo qué campo no se pudo llenar.
2. **El veredicto global sale del vocabulario cerrado de cinco.** No hay sexto valor, no se renombra ninguno y no se matiza con adverbios.
3. **Todo hallazgo declara qué lo refutaría.**
4. **Ningún hallazgo afirma un resultado del caso**, ni con matices, ni «probablemente».
5. **Una observación sin base se marca `UNSUPPORTED_REVIEW_OBSERVATION`**, nunca se presenta como defecto ni se suprime.
6. **Cuando el objeto es un expediente con dos partes, el informe declara que buscó en ambos lados** y qué encontró en cada uno.
7. **El comando no produce ningún acto oficial ni proyecto de decisión**, sea quien sea quien lo invoque.
8. **Si trabaja sobre material no aprobado, lo dice en el encabezado.**

## Consecuencias positivas

- Cierra el único hueco del oleoducto: por primera vez algo revisa el trabajo antes de que salga firmado.
- Adopta un contrato **ya escrito y ya probado en un caso real**, sin inventarle la forma.
- Resuelve la duplicación de seis archivos sobre la misma capacidad, que hoy hace que dos implementadores construyan cosas distintas.
- Da al modelo el permiso que le faltaba para advertir un riesgo sin exagerarlo ni callarlo.
- Es el comando que sirve en contexto de autoridad, que es donde está la usuaria real.

## Consecuencias negativas

- **Trece campos por hallazgo son caros.** En el pase, 14 hallazgos ocuparon ~25 KB. Un informe así se lee entero una vez y después se hojea; el riesgo de que la profesional lo abandone a la mitad es real.
- **Es el segundo comando peligroso del despacho.** `redactar-escrito` puede producir un escrito mal fundado; este puede producir **una crítica falsa con trece campos bien llenos**, que es más difícil de detectar porque tiene forma de rigor.
- Añade un séptimo comando a un producto que **todavía no ha ejecutado ninguno de los seis en su forma instalada**.
- La simetría obligatoria alarga el trabajo y a veces produce hallazgos que a quien encarga la revisión no le convienen. Es el punto en que este comando será impopular, y es el que no se debe negociar.

## Alternativas consideradas

### (a) No crear el séptimo comando y dejarlo dentro de `revisar-documento`
Descartada: `revisar-documento` tiene prohibido comparar con el expediente, y esa prohibición es correcta. Meter aquí la revisión adversarial obligaría a levantarla y rompería el comando que hoy funciona.

### (b) Adoptar la ficha de 7 campos de `08`
Descartada: pierde `residual_risk`, `missing_information` y `support_status`, que son los tres campos que en el pase real impidieron presentar como defecto confirmado lo que era una ausencia de mi propia lectura.

### (c) Un comando por tipo de revisión (probatoria, procesal, sustantiva, temporal)
Descartada: multiplica comandos sin multiplicar método. Las cuatro dimensiones son secciones del mismo informe, no comandos distintos.

### (d) Esperar al Core
Descartada: el comando es texto puro. Esperar solo posterga la única capacidad que la usuaria pidió por su nombre.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Crítica falsa con forma de rigor | Falsabilidad obligatoria (decisión 4) y `support_status` en cada hallazgo |
| El informe no se lee entero | Veredicto global y bloque de qué comprobar primero, al frente |
| Se usa para respaldar una decisión ya tomada | El comando no concluye; los cinco veredictos describen soporte, no resultado |
| En contexto de autoridad, parece delegar la decisión | Decisión 8, repetida en la primera sección del SKILL |
| Duplicación con los cinco archivos supersedidos | Marcarlos en el corpus, no borrarlos |

## Validación / pruebas necesarias

1. **Convertir `workflows/20` en `SKILL.md` y ejecutarlo sobre el mismo expediente [radicado del expediente]**, comparando contra los 14 hallazgos producidos a mano. Es la única prueba que dice si el SKILL preserva el método.
2. Comprobar contra `evals/adversarial-benchmark.md` que la custodia del truth set sigue fuera de la skill.
3. Medir cuántos hallazgos sobreviven a la verificación de la profesional, y cuántos eran `UNSUPPORTED_REVIEW_OBSERVATION` mal marcados.
4. Probar la simetría con un expediente donde solo una parte tenga defectos: comprobar que el informe **dice** que buscó en las dos y no encontró en una.

## Preguntas pendientes

1. **¿Cómo se llama en la superficie?** `revision-de-rigor`, `contradiccion`, `revision-adversarial`. La usuaria dijo *«contradictor interno»*; la palabra de ella suele ser mejor que la nuestra.
2. **¿El informe entra en la capa de entrega `.docx` completo, o resumido?** Trece campos por hallazgo en Word son muchas páginas. Ver ADR-014.
3. ¿Se aplica también al material de la contraparte, o solo al trabajo propio y al expediente? En el pase se aplicó a los tres y funcionó; falta decidir si eso es la regla.
4. ¿Qué severidades existen? `workflows/20` dice «prioridad de revisión, no decisión del caso» y no cierra la lista. Un vocabulario abierto en un campo obligatorio es una grieta.

## Relaciones con otros ADRs

- **ADR-005** (autoridad humana): la decisión 8 es su aplicación directa; este comando propone y jamás decide.
- **ADR-003** (modelo epistémico): `support_status` y la distinción alegado/acreditado son las que el ADR-003 fija; el informe no puede subir el estado de nada.
- **ADR-010** (superficie MCP y clasificación de comandos): el séptimo comando debe clasificarse allí antes de existir en la superficie.
- **ADR-014** (forma de entrega): el informe de rigor es el caso más exigente de la capa `.docx`.
- **ADR-016** (ingesta sin capa de texto): en el pase, cuatro hallazgos quedaron con `support_status: limitado` **por el modo de lectura del material**, no por el método.
