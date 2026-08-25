# ADR-004 — Canonical Case State + Derived Projections

## Estado

Accepted

## Contexto

El prompt maestro (§13–§14) planteaba `case.db` como fuente de verdad y un `memory.md` regenerable como "proyección legible para el modelo", y pedía evaluar si esa aproximación era sólida. La revisión arquitectónica v0.1.1 (secciones E.1, E.2, E.5) concluyó que la dirección era correcta pero el contrato no existía: un `memory.md` monolítico crece sin límite con la vida del caso, mezcla audiencias distintas (modelo, abogada) y carece de política editorial; además quedaban tres nociones distintas conviviendo bajo el nombre `audit.log` y una semántica de conflicto de revisión sin definir.

Los dueños aprobaron la resolución (DECISIÓN APROBADA): **no existe "la memoria de Claude" como fuente de verdad**. Existe un **Canonical Case State** mantenido por el Core y un conjunto de **Derived Projections** regenerables que el modelo consume. **El chat es canal, nunca registro**: el diálogo crudo y el razonamiento intermedio del modelo no se persisten como estado del caso. **No hay `memory.md` monolítico creciente.**

Este ADR consolida los tres contratos que materializan esa decisión: (a) el contrato de proyecciones (`get_case_context`), (b) el modelo de eventos y auditoría (Case Event Log + Tool Invocation Log), y (c) la semántica de `CaseRevision` y de conflicto. Los tres son contratos del Domain/Application, independientes del host conversacional: ninguna capacidad de Cowork o Claude Code es regla del Domain aquí.

**Fuentes primarias (auditables dentro del repositorio).** Las citas de este ADR al prompt maestro v0.1 y a la revisión arquitectónica v0.1.1 se verifican contra `notes/prompt-maestro-v0_1.md` y `notes/revision-arquitectonica-v0_1_1.md`; las reglas etiquetadas `DECISIÓN APROBADA` constan literalmente en el Anexo B de `notes/addendum-correcciones-v0_3.md`. Este ADR se lee además conforme al addendum normativo v0.3 (`notes/addendum-correcciones-v0_3.md`), posterior al kernel v0.2 y prevalente sobre él donde lo contradiga.

## Decisión

### (a) Contrato de proyecciones — `get_case_context`

La memoria operativa del modelo es un conjunto de proyecciones tipadas por alcance, servidas por el Core mediante la tool QUERY `get_case_context(scope, params?)`.

- **Scopes v0:** `overview | facts | evidence | pending | changes_since(revision)`. El scope `procedural` queda **RESERVADO**: documentado en el contrato pero no implementado en el slice, porque el slice no contiene lógica procesal.
- **Refinamiento a señalar (no altera la intención aprobada):** el scope aprobado como `recent_changes` se renombra a **`changes_since(revision)`**, porque "reciente" exige un punto de referencia explícito; el delta solo tiene semántica precisa respecto de una revisión concreta que el invocador declara.
- `pending` incluye: Proposals en estado PENDING, DerivedRepresentations en PENDING/FAILED, Artifacts marcados stale y condiciones activas.
- **Sobre (envelope) de toda respuesta:**

```text
{ case_id, case_revision, scope, params,
  content,
  omissions[ { section, reason } ],
  completeness: COMPLETE | TRUNCATED | PARTIAL,
  conditions[] }
```

- **Simplificación a señalar:** se elimina el campo `generated_from_revision` porque en v0 toda proyección se genera **siempre** desde la revisión vigente en el momento de la llamada, sin caché — el campo sería idéntico a `case_revision`. Si algún día se cachean proyecciones, el campo vuelve al contrato.
- **Presupuesto por scope como política:** cada scope tiene un presupuesto máximo de tamaño definido como política del producto (no como instrucción de prompt). Lo omitido o truncado se declara SIEMPRE en `omissions`; un contexto parcial jamás se presenta como completo.
- Las proyecciones son **regenerables y deterministas** respecto del estado canónico, y **jamás son objetivo de escritura del modelo**. Puede existir un equivalente pequeño de `memory.md` como orientación al abrir un caso: es una **proyección desechable opcional, jamás canónica** — se regenera, no se migra, y ninguna tool permite escribirla.

### (b) Modelo de eventos: tres conceptos, dos persistencias

1. **Case Event Log (canónico).** Un solo log **append-only, hash-chained**, por Case, que **unifica** el evento de dominio/aplicación y el evento de auditoría. Cada evento: `event_id, case_id, seq (== CaseRevision resultante), operation, principal_id / principal_type / principal_role, provenance_kind, payload` (cambio completo o resumen estructurado suficiente para reconstrucción), `methodology_version` (si aplica), `model_id` (si el actor es AI), `knowledge_pack_versions` (si aplica), `timestamp, prev_hash, hash`. **Justificación de la unificación:** un evento de dominio que ya porta actor, payload y hash encadenado ES el registro de auditoría; mantener dos streams (eventos + auditoría) duplicaría el mismo contenido con riesgo de divergencia entre ambos. Esto resuelve la ambigüedad detectada en v0.1.1 E.1.
   **Lista cerrada de eventos v0:** `CaseCreated, EvidenceIncorporated, DerivedRepresentationGenerated/Failed, FactsProposed, ProposalReviewed(approved/rejected/partial), FactsCommitted, FactWithdrawn, ArtifactRegistered, ArtifactMarkedStale, ProposalPreservedForReconciliation`.
   **Momento de emisión en el ciclo de propuesta (regla normativa, ver ADR-005):** `propose_facts` emite `FactsProposed`; **`ReviewProposal(approve|reject)` emite `ProposalReviewed(...)` en el acto mismo de revisión y avanza la CaseRevision** —en ese acto se crea la HumanAuthorization, que congela como `expected_case_revision` la revisión resultante de ese acto de revisión, no la revisión contra la que se creó la Proposal—; **`commit_reviewed_facts` emite `FactsCommitted` y avanza la CaseRevision de nuevo**. Son dos eventos en dos revisiones distintas, coherente con la biyección del invariante 5.
   **ENMIENDA AC-04 (aprobada): `ProposalPreservedForReconciliation` queda también en la lista cerrada, sin productor en v0**, por el mismo patrón que `FactWithdrawn`. Razón: bajo el modelo de dos dimensiones (`review_decision` × `commit_state`), la preservación de una propuesta ante conflicto de revisión **no es un cambio de estado** — nada se descarta, la propuesta sigue viva y su condición se computa. Emitir un evento por un commit *rechazado* registraría en el log canónico algo que no mutó nada, contra el invariante 6 de ADR-005 ("cero mutaciones") y contra la biyección del invariante 5 de este ADR. La preservación es la **conducta por defecto** y su estado es **derivado**, no almacenado. Supersede §16.15.

   **`FactWithdrawn`: en la lista cerrada, sin productor en v0.** Ninguna tool ni use case de la superficie v0 emite `FactWithdrawn`; lo mismo vale para la transición almacenada `DETERMINED` del Fact (ADR-003). Los use cases que los producirían quedan **diferidos con nombre reservado** —`RecordProfessionalDetermination` y `WithdrawFact`, ambos del canal humano y ambos SENSITIVE (exigen HumanAuthorization)—, reservados para no improvisar su nombre ni su contrato después. **Por qué el evento no se elimina de la lista:** la lista es cerrada y ampliarla es cambio de contrato (invariante 6); quitar `FactWithdrawn` obligaría a reabrir el contrato de eventos al implementar el retiro de hechos, que es funcionalidad segura y previsible. Alternativa rechazada: eliminarlo ahora y volver a negociarlo después.
2. **Tool Invocation Log (operacional, separado).** Registra toda invocación MCP, incluidas las QUERY: principal, tool, hash de inputs, resultado/condiciones, y correlación con `event_id` cuando la invocación produjo mutación. **No es estado canónico, no es hash-chained y es podable.** Sirve para diagnóstico y para verificar los tests negativos del slice. Se mantiene separado porque no forma parte de la historia del expediente y por volumen esperado: **SUPUESTO (a validar con uso real; ver preguntas de negocio abiertas):** las lecturas son órdenes de magnitud más frecuentes que las mutaciones. La decisión de separar los dos logs no cambia si el supuesto no se confirma —el Tool Invocation Log seguiría siendo no canónico, no hash-chained y podable—; lo etiquetado como supuesto es el fundamento cuantitativo declarado, no la separación.
3. **NO full event sourcing — decisión anti-moda deliberada.** El estado vigente se **materializa** en tablas (persistencia v0: SQLite). HECHO VERIFICADO (kernel §1; fuente: sqlite.org): en modo WAL lectores y escritores corren concurrentemente con un solo escritor a la vez, y WAL no funciona sobre filesystems de red — todos los procesos en la misma máquina. El Case Event Log aporta **reconstruibilidad y auditoría**; no es el mecanismo de runtime: ninguna operación cotidiana depende de replay de eventos. Se registra explícitamente como decisión, no como omisión: event sourcing pleno añadiría complejidad (replay, snapshots, versionado de eventos como contrato de lectura) sin ningún trigger presente en los requisitos del slice, y la puerta queda abierta porque el log ya captura payloads suficientes para reconstrucción.

**Distinción de capas:** la decisión de arquitectura es "estado materializado + log canónico unificado hash-chained + log operacional podable". Que la materialización sea SQLite y los blobs vivan en filesystem es **detalle de implementación de plataforma** (consistente con los hechos verificados del kernel), sustituible sin tocar el contrato.

### (c) Semántica de CaseRevision

- **ENMIENDA AC-02 (aprobada): dos contadores separados.** `event_seq` es monotónico por Case y avanza en **todo** evento del Case Event Log; `CaseRevision` es monotónico por Case y avanza **solo** en eventos que mutan el estado epistémico canónico. Cada evento registra ambos; los eventos que no mutan estado canónico (`ProposalReviewed`) llevan `case_revision` nula y no la incrementan.

  **Razón.** `case_revision` es el reloj de *lo que el expediente sabe*. Una revisión humana aún no commiteada no añade hechos, evidencia ni links: el expediente sabe exactamente lo mismo antes y después. Hacer avanzar ese reloj invalidaba análisis en vuelo sin relación con la propuesta revisada (conflictos espurios) y producía una definición circular de `expected_case_revision` — *la revisión resultante de su propio acto de revisión* — que ya obligó a una corrección en el addendum v0.3 B.2. Con la enmienda, la propuesta se genera contra la revisión N, se revisa contra N y se commitea exigiendo que el Case siga en N.

  La formulación anterior ("cada evento la incrementa y `seq == revision`") queda **superada**; supersede §16.16. El invariante 5 (biyección) se expresa ahora sobre `event_seq`, con `case_revision` como subsecuencia de los eventos canónicos. Toda respuesta de tool incluye `case_id` y `case_revision`. Toda respuesta de tool incluye `case_id` y `case_revision`.
- Toda tool COMMAND/SENSITIVE_COMMAND acepta **`expected_revision`**. Ante mismatch: **rechazo del commit** + la Proposal implicada se preserva en estado **`PRESERVED_FOR_RECONCILIATION`** + emisión de la condición **`REVISION_CHANGED {expected, current, preserved_proposal_id}`**. Nunca sobrescritura silenciosa; **el trabajo nunca se descarta** — el análisis producido contra la revisión N sigue siendo válido respecto de N y queda disponible para reconciliación humana.
- **Sin locking pesimista**: concurrencia optimista únicamente.

## Invariantes derivados

1. Ninguna proyección es objetivo de escritura del modelo; toda proyección es función determinista del Canonical Case State a la revisión vigente en el momento de la llamada.
2. Toda respuesta de `get_case_context` porta el envelope completo; todo lo omitido o truncado aparece en `omissions[]` con razón; `completeness` nunca declara COMPLETE si hubo omisión.
3. El chat crudo y el razonamiento intermedio del modelo jamás se persisten como estado del caso; el esquema canónico no los admite.
4. El Case Event Log es append-only y hash-chained; editar, truncar o reordenar rompe la verificación de cadena (tamper-evident; límite documentado: no tamper-proof frente a un local hostil — detalle de plataforma, no promesa del Domain).
5. **Biyección mutación↔evento.** **Mutación** = cambio de estado canónico registrado, **no** invocación de tool. Una sola invocación puede producir de 1 a n mutaciones, y por tanto de 1 a n eventos del Case Event Log, avanzando la CaseRevision en n (caso real del slice: una incorporación que además invalida análisis deja `EvidenceIncorporated` + `ArtifactMarkedStale`, dos eventos y dos revisiones). El invariante es: **toda mutación produce exactamente un evento, y todo evento corresponde a exactamente una mutación** — biyección mutación↔evento, no invocación↔evento. Cada evento porta `seq == CaseRevision` resultante. La formulación previa "n mutaciones == n eventos" queda como abreviatura de esta biyección y solo es correcta bajo esta definición de mutación (supersede §16.11 del addendum v0.3: enunciado sin definir mutación → biyección con `mutación = cambio de estado canónico registrado`).
6. La lista de eventos v0 es cerrada; un tipo de evento nuevo es cambio de contrato, no extensión silenciosa.
7. Un commit con `expected_revision` desactualizada jamás sobrescribe ni descarta: rechazo + preservación (`PRESERVED_FOR_RECONCILIATION`) + `REVISION_CHANGED`.
8. El Tool Invocation Log nunca es fuente para reconstruir estado canónico; su poda no afecta el expediente.

## Consecuencias positivas

- Reapertura de caso en otra sesión sin dependencia de la memoria conversacional del host: `overview` + `changes_since(última revisión conocida)` reconstruyen la orientación (propiedades 7–8 del objetivo del slice).
- Auditoría sin doble contabilidad: un solo registro canónico responde "qué pasó, quién, con qué versiones", y la correlación con el Tool Invocation Log da el "cómo se invocó".
- La eliminación del caché (y de `generated_from_revision`) elimina por construcción la clase de bugs de proyección desfasada en v0.
- El conflicto de revisión se convierte en flujo de trabajo (reconciliación de una Proposal preservada) en lugar de pérdida o sobrescritura.
- `memory.md` deja de ser un pasivo de migración: se regenera, nunca se migra.

## Consecuencias negativas

- Regenerar cada proyección en cada llamada tiene costo lineal con el tamaño del caso; aceptado en v0 (una usuaria, una máquina), y es el punto que reintroduciría caché — con `generated_from_revision` de vuelta — si la latencia lo exige.
- La lista cerrada de eventos obliga a tocar el contrato para cada operación nueva; es fricción deliberada.
- Payloads "suficientes para reconstrucción" en cada evento implican redundancia de almacenamiento frente al estado materializado; asumida como costo de la reconstruibilidad.
- La reconciliación de Proposals preservadas es trabajo humano adicional que el slice debe hacer visible vía `pending`.

## Alternativas consideradas

1. **`memory.md` monolítico creciente** (idea original de §13). Rechazada: no escala con la vida del caso frente a cualquier presupuesto de contexto, mezcla audiencias (modelo vs abogada) con criterios de completitud y lenguaje distintos, y carece de política editorial — quien decidiera qué entra sería el modelo, reintroduciendo el problema que se quería evitar.
2. **Full event sourcing** (estado derivado por replay). Rechazada para v0: complejidad sin trigger — snapshots, versionado del esquema de eventos como contrato de lectura, replay como dependencia de runtime — para una carga de eventos por minuto. El log unificado con payloads completos preserva el camino de evolución sin pagarlo hoy.
3. **Dos logs de auditoría separados** (event log de dominio + audit log forense). Rechazada: el evento unificado con actor + payload + hash ya es el registro de auditoría; dos streams duplican contenido y crean la pregunta irresoluble de cuál manda cuando divergen.
4. **Locking pesimista** para concurrencia. Rechazada. **SUPUESTO (a validar con uso real; ver preguntas de negocio abiertas):** el escritor típico es un agente cuya operación dura minutos, de modo que un lock bloquearía a la usuaria (por ejemplo, la ingesta de un documento) durante todo un análisis. La decisión no cambia con el resultado de esa validación —la concurrencia optimista con preservación protege el estado sin bloquear a nadie y sin descartar trabajo—; lo etiquetado como supuesto es la duración observada del escritor-agente, que solo el uso real puede confirmar.

## Riesgos

- **RIESGO — Granularidad de la revisión única por Case:** una mutación irrelevante para un análisis en curso (ingestar un documento no relacionado) también produce `REVISION_CHANGED`. Si los conflictos espurios generan fatiga, el camino declarado en v0.1.1 (E.5) es revisiones por agregado antes que cualquier locking; no se diseña ahora.
- **RIESGO — Señal/ruido de `pending`:** si `pending` acumula demasiado, la usuaria dejará de mirarlo; el presupuesto por scope y la curación de qué entra en `pending` son política a calibrar con uso real.
- **RIESGO — Tamper-evidence local:** el hash-chain detecta alteración pero no la impide en una máquina bajo control total del usuario; el anclaje del hash-cabeza fuera del workspace mitigaría y no está decidido (ver Preguntas).
- **POR VERIFICAR —** si el host permite mostrar salida de tools sin mediación del modelo; mientras tanto, "el chat es canal, nunca registro" implica que las garantías de fidelidad se apoyan en el estado y los artifacts, no en el diálogo.

## Validación / pruebas necesarias

1. **Golden test de regeneración determinista:** mismo estado canónico, misma revisión → dos generaciones de cada scope producen salida idéntica byte a byte.
2. **Property test de la biyección mutación↔evento:** para toda secuencia de commands aceptados, cada mutación de estado canónico registrada tiene exactamente un evento del Case Event Log y cada evento corresponde exactamente a una mutación, con `seq` contiguos y `seq == case_revision` reportada por las tools. El test verifica **la biyección, no el conteo de invocaciones**: una invocación que produce n mutaciones debe dejar n eventos y avanzar la revisión en n (invariante 5); contar llamadas a tools daría un falso fallo en ese caso legítimo.
3. **Test de hash-chain:** mutar, truncar o reordenar una entrada intermedia del log → la verificación de cadena falla señalando el punto de ruptura.
4. **Test de conflicto de revisión con preservación:** dos escritores, commit con `expected_revision` obsoleta → rechazo, condición `REVISION_CHANGED` con los tres parámetros, Proposal recuperable en `PRESERVED_FOR_RECONCILIATION` y visible vía `get_case_context(pending)`.
5. Complementarios: envelope presente en toda respuesta (contract test); caso sintético grande → salida bajo presupuesto con `omissions` no vacío y `completeness` ≠ COMPLETE; poda del Tool Invocation Log → estado canónico y verificación de cadena intactos.

## Preguntas pendientes

- **DECISIÓN PENDIENTE —** valores concretos del presupuesto por scope (política del producto; calibrar con casos reales de la usuaria).
- **DECISIÓN PENDIENTE —** la proyección para audiencia humana ("carátula del expediente"): si la abogada la anota y la considera "suya", la regeneración silenciosa destruiría sus anotaciones (pregunta J.7 de la revisión); fuera del alcance de este ADR pero condiciona qué proyecciones pueden regenerarse sin aviso.
- **DECISIÓN PENDIENTE —** destino aceptable para anclar periódicamente el hash-cabeza del Case Event Log fuera del workspace.
- **DECISIÓN PENDIENTE —** política de retención/poda del Tool Invocation Log (horizonte, criterio).
- **POR VERIFICAR —** umbral medible que dispararía revisiones por agregado (frecuencia de `REVISION_CHANGED` espurios en uso real).

## Relaciones con otros ADRs

- **ADR-001** (posición del LLM como cliente externo no confiable y contrato MCP↔Application): este ADR asume que el modelo solo lee estado vía tools QUERY; las proyecciones son exactamente la vista que ese cliente no confiable recibe, y por eso jamás son escribibles por él.
- **ADR-002** (Workspace vs Private State): el Canonical Case State — case databases, event log, originals, artifact registry — vive en el LEGAL OS PRIVATE STATE, accesible solo vía Core; una proyección desechable puede materializarse hacia el workspace sin volverse canónica.
- **ADR-003** (estados del Fact): las transiciones almacenadas del Fact son eventos del Case Event Log (`FactsCommitted`, `FactWithdrawn`); los estados derivados (`SUPPORTED | CONTRADICTED | UNSUPPORTED`) son contenido computado de las proyecciones `facts`/`overview`, nunca status almacenado. `FactWithdrawn` —y la transición `DETERMINED`— permanecen sin productor en v0 (ver la lista cerrada de eventos en (b)1).
- **ADR-005** (HumanAuthorization): `commit_reviewed_facts` valida `expected_case_revision` de la autorización contra la CaseRevision vigente; el mismo mecanismo de conflicto de este ADR (rechazo + preservación + `REVISION_CHANGED`) protege ese commit sensible, y su éxito produce el evento `FactsCommitted`. El ciclo de propuesta consume **dos revisiones**: `ReviewProposal(approve)` emite `ProposalReviewed(approved)` y avanza la CaseRevision —la autorización nace en ese acto y congela como `expected_case_revision` la revisión resultante de él, "la revisión que la profesional tenía a la vista al aprobar"—, y el commit emite `FactsCommitted` avanzando la revisión de nuevo.
- **ADR-006** (frontera de incorporación: exploración ≠ evidencia del Case): reciprocidad. ADR-006 fija **qué material puede entrar** al expediente y por qué única puerta; este ADR fija **cómo queda registrado** ese ingreso y con qué aritmética de revisiones: `ingest_evidence` produce `EvidenceIncorporated` —y la derivación asíncrona, `DerivedRepresentationGenerated/Failed`— en el Case Event Log, cada evento avanzando la CaseRevision, con las derivaciones `PENDING/FAILED` visibles vía `get_case_context(pending)`. En sentido inverso: ninguna proyección de este ADR puede presentar como contenido del Case material no incorporado, y el Tool Invocation Log —que sí registra la exploración— nunca es fuente para reconstruir estado canónico (invariante 8).
