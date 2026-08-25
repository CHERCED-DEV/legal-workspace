# Verificación de cumplimiento estructural — consolidación Legal OS

## Resumen por requisito

| Req. | Resultado |
|---|---|
| (a) 11 secciones exactas en cada ADR, Estado = Accepted | **Cumple en estructura y orden** en los 6 ADRs (verificado por encabezados H2). Única desviación: el rótulo de la 9.ª sección (ver H9). Contenido decisorio mal ubicado en 2 ADRs (H10). |
| (b) principles.md: 15 principios con títulos en inglés + anexo Product Floor | **Cumple**: 15 principios numerados, títulos en inglés, cada uno con exige/prohíbe/verifica, y `## Anexo — Product Floor v0` con las 5 políticas del kernel §14. Fidelidad literal de los títulos no verificable (H16). |
| (c) glossary.md: 13 términos × 6 subsecciones | **Cumple exactamente**: los 13 términos canónicos en el orden del kernel §2 y 78 subsecciones = 13 × 6 (Definición / No significa / Lifecycle preliminar / Invariantes / Ejemplo / Preguntas abiertas). Sin términos extra ni faltantes. |
| (d) boundaries.md: 8 capas + los 2 roles de la IA + Mermaid + ciclos de vida y mínimo de release | **Cumple**: §1 External Actors, §2 Driving Adapters, §3 Application, §4 Domain, §5 Driven Ports, §6 Infrastructure, §7 Configuration, §8 Content Packs, §9.1/§9.2 los dos roles por separado + §9.3 advertencia, §9.4 Mermaid, §10 tres ciclos de vida + los 7 puntos del mínimo de release. |
| (e) vertical-slice-v0.md: 18 secciones en orden + 10 tests adversariales | **Cumple**: las 18 secciones aparecen en el orden exigido (líneas 9–578) y la matriz tiene 10 filas adversariales + 17 funcionales (F1–F17). Una sección adicional al final (H12). |
| (f) Ningún archivo de código creado | **Cumple**: el árbol completo del workspace contiene solo `.md` (más `.claude/scheduled_tasks.lock`, preexistente, no es código). Cero `.ts/.js/.py/.sql`. |
| (g) Los 10 archivos existen | **Cumple**: los 10 existen con contenido sustantivo (15–65 KB c/u). |

---

## Hallazgos accionables

### H1 — ALTA · Invariante "n mutaciones == n eventos" contradicho por el propio slice, en 6 documentos
- **Archivos:** `C:\Users\HITMA\Desktop\legal-workspace\docs\architecture\adrs\ADR-004-case-memory.md` (Invariantes derivados, 5), `...\ADR-001-trust-boundary.md` (Invariantes derivados, 2), `...\boundaries.md` (§3 Application), `...\principles.md` (principio 2), `...\docs\domain\glossary.md` (Case inv. 3; CaseRevision inv. 2), `...\vertical-slice-v0.md` (Happy path, nota final).
- **Cita:** ADR-004: "Toda mutación commiteada produce exactamente un evento del Case Event Log con `seq == CaseRevision` resultante (n mutaciones == n eventos)". El slice: "un COMMAND puede producir más de un evento y avanzar la revisión más de una unidad (pasos 15–16)".
- **Problema:** el slice ya detecta la colisión (paso 15 `EvidenceIncorporated` rev 10 + paso 16 `ArtifactMarkedStale` rev 11) y propone leer *mutación = cambio de estado registrado*, pero ninguno de los cinco documentos normativos incorpora esa lectura. Tal como están redactados, el property test B.3/F13 y el invariante de ADR-004 son mutuamente inconsistentes.
- **Corrección:** añadir en ADR-004 inv. 5 la definición explícita ("mutación = cambio de estado registrado, no invocación de tool; un COMMAND puede producir N eventos y avanzar N revisiones") y propagar la misma glosa a ADR-001 inv. 2, boundaries §3, principio 2 y las dos entradas del glosario.

### H2 — ALTA · Momento de emisión de `ProposalReviewed`: ADR-005 contradice al slice
- **Archivos:** `...\adrs\ADR-005-human-authority.md` (Decisión §3) vs `...\vertical-slice-v0.md` (Happy path, paso 10).
- **Cita:** ADR-005: "Si todo coincide: ejecuta, marca `consumed_at` y emite `ProposalReviewed` y `FactsCommitted` en el Case Event Log". Slice: paso 10 `ReviewProposal(approve)` → evento `ProposalReviewed(approved)`, rev 7; paso 11 commit → `FactsCommitted`, rev 8.
- **Problema:** si `ProposalReviewed` se emitiera en el commit, la `HumanAuthorization` creada en la revisión no podría llevar el `expected_case_revision` "resultante de este mismo acto" que el slice le asigna. El slice señala la divergencia ("La diferencia es de momento de emisión, no de contenido") pero ADR-005 —que es el ADR rector de la operación sensible— sigue afirmando lo contrario.
- **Corrección:** editar ADR-005 §3 para que `ReviewProposal` emita `ProposalReviewed` y el commit emita solo `FactsCommitted`, y añadir una línea en Invariantes derivados 9 aclarando que son dos eventos en dos revisiones distintas.

### H3 — ALTA · `Artifact`, `Proposal`, `HumanAuthorization` y `CaseRevision` ubicados en el Domain en boundaries y en Application en el glosario
- **Archivos:** `...\boundaries.md` (§4 Domain y nodo `DOM` del Mermaid §9.4) vs `...\docs\domain\glossary.md` (Mapa de los trece términos) y `...\adrs\ADR-003-epistemic-domain-model.md` (Decisión, "Conceptos de soporte").
- **Cita:** boundaries §4: "Entidades canónicas (kernel §2), **sin más**: `Case, Source, …, Artifact, CaseRevision, Proposal, HumanAuthorization, DerivedRepresentation`". Glosario: `Artifact` → "**Application** (registro de trabajo)"; `Proposal` → "Application (soporte)"; `HumanAuthorization` → "Application (soporte)".
- **Problema:** contradicción directa sobre a qué lado de la frontera Application/Domain viven cuatro de los trece términos; el Mermaid la fija visualmente al meter los cuatro dentro del subgraph `DOMAIN`. ADR-003 refuerza al glosario ("conceptos de soporte … definidos en detalle en sus propios documentos").
- **Corrección:** en boundaries §4, separar dos bloques —"entidades epistémicas del Domain" (los 8 de ADR-003) y "conceptos de soporte del plano Application"— y mover `Artifact`, `Proposal`, `HumanAuthorization` (y `CaseRevision` como compartido) al nodo `APP` del Mermaid.

### H4 — ALTA · `DETERMINED`, `ProfessionalDetermination` y `FactWithdrawn` carecen de productor en toda la consolidación
- **Archivos:** `...\adrs\ADR-003-epistemic-domain-model.md` (Validación, 5), `...\boundaries.md` (§3 Application, lista de use cases), `...\vertical-slice-v0.md` (Application use cases required; Domain entities exercised).
- **Cita:** ADR-003 exige probar que "una ProfessionalDetermination sin motivación o sin la lista de links valorados … ⇒ rechazo"; boundaries lista 10 use cases y ninguno la crea; el slice declara "ProfessionalDetermination: **No ejercitada como flujo positivo**".
- **Problema:** la única vía a `DETERMINED` no tiene use case ni canal en ningún documento, y el mismo vacío afecta a `WITHDRAWN` / `FactWithdrawn`, que está en la lista **cerrada** de eventos v0 (kernel §6, ADR-004, slice) sin emisor. El test 5 de ADR-003 no es ejecutable en v0 y no aparece en la matriz del slice.
- **Corrección:** en ADR-003 Validación, marcar los asserts de ProfessionalDetermination como **post-slice** (o añadir el use case `RecordProfessionalDetermination` al canal humano en boundaries §3 y al slice); y anotar en ADR-004/slice que `FactWithdrawn` es evento declarado sin productor en v0.

### H5 — MEDIA-ALTA · `OPERATION_NOT_PERMITTED` emitida para operaciones que no existen en la superficie (fila autocontradictoria)
- **Archivos:** `...\vertical-slice-v0.md` (Test matrix, filas 1, 4 y 9; Negative paths) vs `...\adrs\ADR-006-evidence-incorporation-boundary.md` (Preguntas pendientes).
- **Cita:** slice, test 9: "**En v0 la operación ni siquiera existe en la superficie** … No hay estado 'verificada' que alcanzar **ni camino que rechazar**" → columna condición: "`OPERATION_NOT_PERMITTED {operation, policy_reason}`". ADR-006: "`OPERATION_NOT_PERMITTED` es de política, no de este caso".
- **Problema:** la misma fila afirma que no hay camino de código y a la vez exige una condición tipada; sin tool registrada, el MCP devuelve "tool desconocida", no una condición del catálogo. El criterio de aceptación queda no verificable.
- **Corrección:** en el slice, precisar el disparador: o bien la condición la emite un gate de política ante una intención reconocida por una tool existente (y decirlo), o bien la celda pasa a "sin condición del catálogo: la operación no existe en el manifiesto (verificable por el test de superficie F16)".

### H6 — MEDIA-ALTA · `DerivedRepresentation` no tiene esquema en "Persisted state"
- **Archivo:** `...\vertical-slice-v0.md` (§ Persisted state, bloque de esquemas conceptuales, líneas ~248–321).
- **Cita:** el bloque define `Case, Source, Evidence, Statement, Fact, Fact.status_history, EvidenceLink, Proposal, HumanAuthorization, Artifact (referencia), Case Event Log, Tool Invocation Log`.
- **Problema:** `DerivedRepresentation` es entidad persistida (versión, hash, receta, `PENDING|READY|FAILED`, referencia obligatoria al Source) y es el sustrato de los pasos 4, 7 y 12 del happy path y de F3/F3b/F9, pero no aparece en la sección que debe fijar el estado persistido. La sección "Derived state" la lista como "**Persistido** pero regenerable", lo que confirma la omisión.
- **Corrección:** añadir el bloque `DerivedRepresentation { derivation_id, case_id, source_id, version, content_hash, recipe {tool, version}, state, provenance, created_at }` a Persisted state, con nota de que es persistido-regenerable.

### H7 — MEDIA · `Statement` figura como entidad ejercitada, sin productor ni prueba
- **Archivo:** `...\vertical-slice-v0.md` (§ Domain entities exercised, fila Statement; § Application use cases required; § Test matrix F1–F17).
- **Cita:** columna "Qué ejercita el slice": "Anclaje a fragmento verificable sobre el **original** …"; columna contigua: "**SUPUESTO del slice:** … el slice puede completarse **sin materializar Statements**".
- **Problema:** la tabla lo cuenta como ejercitado y a la vez como prescindible; ninguno de los 9 use cases externos, ni los 2 internos, crea Statements, y ningún test F1–F17 los verifica, pese a que ADR-003, el glosario (ST-9) y Persisted state los tratan como entidad de primera clase.
- **Corrección:** decidir y reflejarlo en una sola dirección — o mover `Statement` a la columna "Qué **no** ejercita" (y a Explicit non-goals), o añadir el productor (`ExtractStatements` interno) y un test F correspondiente.

### H8 — MEDIA · Referencias cruzadas del glosario a ADR-006 desplazadas en uno
- **Archivo:** `...\docs\domain\glossary.md` (§2 Source, "No significa" e "Invariantes" 2).
- **Cita:** "el archivo de Inbox **deja de ser la fuente** … (**ADR-006, inv. 5**)" y "**Idempotencia por hash** … (**ADR-006, inv. 6**)".
- **Problema:** en ADR-006 la inv. 5 es "El fragmento siempre resuelve a un Source", la inv. 6 es "El snapshot es independiente del origen" y la inv. 7 es "Idempotencia por hash". Ambas citas apuntan un número por debajo del invariante correcto.
- **Corrección:** cambiar a `ADR-006, inv. 6` y `ADR-006, inv. 7` respectivamente; verificar de paso las demás citas numéricas del glosario a ADR-003/ADR-006 (las revisadas — Evidence inv. 4 → ADR-006 inv. 1; Artifact inv. 2 → ADR-006 inv. 3; Proposal inv. 2 → ADR-006 inv. 2 — son correctas).

### H9 — MEDIA · Rótulo de la 9.ª sección: "Validación / pruebas necesarias" en lugar de "Validación · pruebas necesarias"
- **Archivos:** los 6 ADRs (`ADR-001` L86, `ADR-002` L111, `ADR-003` L162, `ADR-004` L93, `ADR-005` L138, `ADR-006` L79).
- **Problema:** la lista de secciones exigida por los dueños usa el separador "·"; los seis documentos usan "/" de forma uniforme. Es desviación literal del contrato de secciones (uniforme, por lo que la corrección es mecánica y de bajo riesgo).
- **Corrección:** renombrar la sección en los 6 archivos a `## Validación · pruebas necesarias`, o —si el "·" era solo separador de la especificación— dejar constancia escrita de la equivalencia en el kernel §0 para cerrar la ambigüedad de una vez.

### H10 — MEDIA-BAJA · Contenido decisorio ubicado en "Contexto" en ADR-005 y ADR-006
- **Archivos:** `...\ADR-005-human-authority.md` (Contexto: bloque "**DECISIÓN APROBADA.** El reparto de autoridad del sistema es fijo:" + tabla Claude/Core/Humano), `...\ADR-006-evidence-incorporation-boundary.md` (Contexto: "DECISIÓN APROBADA por los dueños: se adopta la variante (b)").
- **Problema:** con un conjunto de secciones cerrado, la decisión debe vivir en "Decisión"; ADR-005 coloca allí la tabla de reparto de autoridad —que es la decisión nuclear del ADR— y ADR-006 anuncia la adopción de la variante (b) antes de la sección "Decisión", donde vuelve a enunciarse.
- **Corrección:** mover la tabla de reparto de autoridad al inicio de "Decisión" en ADR-005 (dejando en Contexto solo el riesgo y el antecedente v0.1.1) y reducir el párrafo de ADR-006 a la formulación de las dos variantes, sin anticipar la elección.

### H11 — BAJA · "Relaciones con otros ADRs" incompletas y asimétricas
- **Archivos:** los 6 ADRs, sección final.
- **Problema:** ADR-002 no referencia ADR-003 ni ADR-005; ADR-003 no referencia ADR-002; ADR-004 no referencia ADR-006; ADR-005 no referencia ADR-002 ni ADR-006; ADR-006 no referencia ADR-004 (pese a citar `EvidenceIncorporated`, el Case Event Log y `INTEGRATION_ERROR`). Solo ADR-001 es completo.
- **Corrección:** cerrar la malla con una línea por relación faltante (bastan 7 líneas), de modo que cada par citado en el cuerpo tenga entrada recíproca.

### H12 — BAJA · Sección 19.ª ("Referencias") fuera de las 18 exigidas
- **Archivo:** `...\vertical-slice-v0.md` (L590 `## Referencias`).
- **Problema:** las 18 secciones exigidas están completas y en orden, pero el documento añade una sección extra al final; si el contrato de secciones se lee como cerrado, sobra.
- **Corrección:** convertir "Referencias" en un bloque sin encabezado H2 (nota al pie tras "Questions blocking implementation") o registrar explícitamente que el contrato admite un apéndice de referencias.

### H13 — BAJA · Paso 14 del happy path usa `changes_since(9)` sobre un Case en revisión 9 (delta vacío)
- **Archivo:** `...\vertical-slice-v0.md` (Happy path, filas 13–14).
- **Cita:** fila 13 "cierre de sesión … Rev. 9"; fila 14 "`get_case_context(changes_since(9))` … Rev. 9".
- **Problema:** el delta es necesariamente vacío, de modo que el paso no evidencia la propiedad §34.8 ("reapertura en otra sesión") que el criterio de aceptación A.8 le atribuye; la demostración real solo ocurre después, en el paso 17.
- **Corrección:** cambiar el paso 14 a `changes_since(<última revisión conocida por la usuaria>)` con un valor menor que 9 (p. ej. 6, la revisión anterior al commit) o anotar que el delta vacío es el resultado esperado y trasladar la verificación de A.8 al paso 17.

### H14 — BAJA · `REVIEWED` sin sus parámetros en el Artifact Registry de boundaries
- **Archivo:** `...\boundaries.md` (§3 Application, "Artifact Registry").
- **Cita:** "`status: DRAFT | REGISTERED | REVIEWED | SUPERSEDED`".
- **Problema:** kernel §10, glosario §9 y el slice fijan `REVIEWED(by, at, at_revision)`; boundaries pierde los tres parámetros, que son justamente lo que distingue "revisado por alguien identificado" de un flag.
- **Corrección:** escribir `REVIEWED(by, at, at_revision)` en boundaries §3.

### H15 — BAJA · "Techo epistémico: `PROPOSED`" atribuido a la IA-como-capacidad
- **Archivo:** `...\boundaries.md` (§9.3, tabla comparativa, última fila).
- **Problema:** la IA-como-capacidad no transiciona Facts: su salida es `DerivedRepresentation` (o insumo de una Proposal). Decir que su techo es `PROPOSED` sugiere que puede llegar hasta ahí por sí sola, cuando el propio §9.2 dice que "aquí la IA no decide nada". La prosa posterior lo corrige, la tabla no.
- **Corrección:** en esa celda, escribir "No transiciona Facts; produce `DerivedRepresentation` o insumo de `Proposal`", y dejar el enunciado común ("por ninguna de las dos vías la IA supera `PROPOSED`") solo en la prosa.

### H16 — BAJA (limitación de verificación) · No hay fuente en el workspace contra la que cotejar los 15 títulos aprobados ni los 10 tests de §24
- **Archivos:** `...\docs\architecture\notes\kernel-consolidacion-v0_2.md` (§0, §11) y ausencia del prompt maestro v0.1 en el árbol.
- **Cita:** kernel §0: "Los títulos de los 15 principios se conservan en inglés (así los aprobaron los dueños)" — sin enumerarlos; §11: "Los 10 tests negativos de §24" — sin listarlos.
- **Problema:** puedo verificar cardinalidad (15 principios, 10 filas adversariales, títulos en inglés) pero **no** fidelidad literal a la lista aprobada, porque el maestro §21/§24 no está en el repositorio (`revision-arquitectonica-legal-os.md` no los reproduce).
- **Corrección:** incorporar al kernel un anexo con los 15 títulos y los 10 tests verbatim (o versionar el prompt maestro en `docs/architecture/notes/`), para que la verificación de fidelidad sea reproducible y no dependa de memoria de los dueños.

### H17 — BAJA · ADR-001 enumera 8 pruebas sin declarar que son subconjunto de los 10 adversariales
- **Archivo:** `...\adrs\ADR-001-trust-boundary.md` (Validación / pruebas necesarias).
- **Cita:** "Los tests negativos del slice (kernel §11 …) validan esta frontera de forma adversarial" seguido de 8 ítems numerados; el slice cita "ADR-001 test 3" en su fila 7, creando dos numeraciones paralelas.
- **Problema:** un lector puede tomar los 8 de ADR-001 por "los tests negativos del slice", que son 10 y viven en `vertical-slice-v0.md`.
- **Corrección:** encabezar la lista con "Subconjunto que ataca esta frontera; la matriz completa (10 adversariales + F1–F17) está en `vertical-slice-v0.md` §Test matrix" y, si es posible, alinear la numeración con la de la matriz.

---

**Categorías sin hallazgos:** requisito (c) — el glosario cumple íntegramente (13 términos, 6 subsecciones cada uno, sin extras). Requisito (f) — no se creó ningún archivo de código. Requisito (g) — los 10 archivos exigidos existen.