# Kernel técnico v0.4 — decisiones normativas del Technical Design V0

**Estado:** normativo para todos los documentos de `docs/technical-design/v0/` y para los ADRs 007–011.
**Precedencia:** por debajo de los ADRs Accepted (001–006), por encima del kernel de consolidación v0.2 y del addendum v0.3 en materia técnica. Ver §14.

Este documento fija el vocabulario, los contratos y las decisiones que los documentos técnicos deben usar **literalmente**. Donde una decisión sea mía y no de los dueños, va etiquetada `PROPUESTA DEL TECHNICAL DESIGN` y aparece en la lista de aprobaciones pendientes.

---

## 1. Corrección semántica obligatoria: Principal ≠ ProvenanceKind

**DECISIÓN APROBADA (dueños, §3).** Se separan dos conceptos que estaban colapsados en `actor_type`.

### 1.1 Principal — *quién ejecutó la operación*

```text
Principal
  principal_id      identificador opaco, estable
  principal_type    ver §1.2
  principal_role    rol funcional dentro de la organización (v0: 'lawyer')
```

Todo evento, mutación y registro de auditoría lleva un `Principal`. Es una propiedad **operacional**: responde a la pregunta de autoría de la acción.

### 1.2 `principal_type` — crítica del enum propuesto

Los dueños proponen `HUMAN | AI | SYSTEM | EXTERNAL` y autorizan proponer algo mejor.

**PROPUESTA DEL TECHNICAL DESIGN: `HUMAN | AI | SYSTEM` (tres valores, sin `EXTERNAL`).**

Razón: un *principal* es quien **invoca** una operación contra el Core. Un tercero externo (la contraparte que envió un correo, el juzgado que emitió un oficio) nunca invoca nada en nuestro sistema: aparece como **origen del material**, que es exactamente lo que `provenance_kind = EXTERNAL_SOURCE` ya expresa, junto con los metadatos de origen declarado en la incorporación. Incluir `EXTERNAL` como `principal_type` produciría registros de auditoría con un ejecutor que no ejecutó nada, y volvería a mezclar las dos dimensiones que esta corrección separa.

Cuando la incorporación de un Source deba registrar de quién procede el material, se usa el sobre de ingestión (`declared_origin`), no el principal: el principal de esa operación es la profesional que incorpora (`HUMAN`) o el sistema que la ejecuta en su nombre (`SYSTEM`).

### 1.3 `provenance_kind` — *cuál es la naturaleza epistemológica del origen*

Enum sin cambios (kernel v0.2 §2):

```text
EXTERNAL_SOURCE | AI_DERIVATION | AI_INFERENCE | HUMAN_DECISION | SYSTEM
```

Es una propiedad **epistémica**: responde de dónde procede el conocimiento, no quién apretó el botón.

### 1.4 Relación entre ambos y regla dura

Son ortogonales pero no independientes: no toda combinación es válida.

| `provenance_kind` | `principal_type` admisible | Ejemplo |
|---|---|---|
| `EXTERNAL_SOURCE` | `HUMAN`, `SYSTEM` | La profesional incorpora un contrato |
| `AI_DERIVATION` | `AI`, `SYSTEM` | Transcripción generada por el proveedor |
| `AI_INFERENCE` | `AI` | Hecho candidato propuesto por el modelo |
| `HUMAN_DECISION` | `HUMAN` | Aprobación de un ProposalItem |
| `SYSTEM` | `SYSTEM` | Regeneración de una proyección, migración |

**Invariante (comprobable):** `HUMAN_DECISION` exige `principal_type = HUMAN`; ningún `principal_type = AI` puede producir `provenance_kind = HUMAN_DECISION`. Esta es la formulación correcta de lo que antes se escribía —mal— como `actor_type = HUMAN_DECISION`.

### 1.5 Nota de normalización (no destruir historia)

El corpus previo escribía `actor_id / actor_type / actor_role` con `actor_type` tomando valores del enum epistémico. Se normaliza así, **sin pérdida de información**:

| Antes | Ahora |
|---|---|
| `actor_id` | `principal_id` |
| `actor_type` (valor operacional) | `principal_type` ∈ `HUMAN \| AI \| SYSTEM` |
| `actor_type = HUMAN_DECISION` (uso epistémico) | `provenance_kind = HUMAN_DECISION` + `principal_type = HUMAN` |
| `actor_role` | `principal_role` |

Registrar como **supersede §16.13**. Los documentos afectados (ADR-003, ADR-005, glosario, vertical-slice, kernel v0.2, addendum v0.3) llevan la nota; el texto histórico no se borra.

---

## 2. Proposal y aprobación parcial

**DECISIÓN APROBADA (dueños, §4 y §5).**

### 2.1 Estructura

```text
Proposal
  proposal_id
  case_id
  base_case_revision        revisión contra la que se generó
  created_by (Principal)
  provenance_kind           AI_INFERENCE en el flujo del slice
  methodology / model       metodología y modelo que la produjeron
  created_at

ProposalItem
  proposal_item_id          identidad estable y opaca — NUNCA índice posicional
  proposal_id
  item_content_hash         hash del contenido normalizado del item
  payload                   el hecho candidato + sus links propuestos
  review_decision           ver §2.2
  commit_state              ver §2.2
```

**Invariante:** la identidad de un item no depende de su posición ni de su orden; reordenar la propuesta no cambia ningún `proposal_item_id`.

### 2.2 Lifecycle — crítica del enum propuesto

Los dueños proponen `PENDING_REVIEW | APPROVED | REJECTED | DEFERRED | COMMITTED | INVALIDATED` y piden crítica, distinguiendo *decisión profesional* de *estado de commit*.

**PROPUESTA DEL TECHNICAL DESIGN: dos dimensiones separadas, seis valores en total.**

```text
review_decision : PENDING | APPROVED | REJECTED
commit_state    : UNCOMMITTED | COMMITTED
```

Justificación de cada eliminación respecto del enum propuesto:

- **`PENDING_REVIEW` → `PENDING`.** Mismo valor, nombre más corto y sin redundancia (está en la dimensión de revisión, no hace falta repetir "review").
- **`DEFERRED` eliminado.** Los dueños fijaron en §4 tres decisiones por item: `APPROVE`, `REJECT`, `PENDING`. "Diferido" y "pendiente" son el mismo estado observable — el item no se commitea y sigue disponible para revisión. Añadir `DEFERRED` obligaría a definir en qué se diferencia operativamente de `PENDING`, y no hay diferencia. Si más adelante aparece la necesidad de distinguir "aún no lo he mirado" de "lo miré y lo dejo para después", se añade como matiz de `PENDING`, no como estado nuevo.
- **`COMMITTED` movido a su propia dimensión.** Era el caso más claro de mezcla: un item puede estar `APPROVED` y todavía no commiteado; con un solo enum habría que elegir cuál de los dos hechos representar.
- **`INVALIDATED` eliminado como estado almacenado; pasa a ser derivado.** Un item se considera inválido cuando su `item_content_hash` ya no coincide con el de la autorización, o cuando la `expected_case_revision` de la autorización ya no es la vigente. Ambas cosas son **computables**; almacenarlas como estado abriría la posibilidad de que el estado almacenado y la realidad divirjan, que es precisamente el defecto que el modelo epistémico evita en `Fact`.

**Transiciones válidas:** `PENDING → APPROVED`, `PENDING → REJECTED`, y la re-revisión `APPROVED → PENDING` / `REJECTED → PENDING` cuando el contenido cambia. `commit_state` solo avanza `UNCOMMITTED → COMMITTED`, y únicamente para items con `review_decision = APPROVED`.

### 2.3 Integridad de la aprobación parcial (dueños, §5)

**Invariante comprobable:** una `HumanAuthorization` es válida para un commit solo si, en el momento del commit, se cumplen simultáneamente:

1. existe y no ha sido consumida (`consumed_at IS NULL`);
2. `authorization.item_content_hash == item.item_content_hash` (el contenido no cambió desde la revisión);
3. `authorization.expected_case_revision == case.current_revision`;
4. `authorization.authorized_operation` corresponde a la operación intentada;
5. no ha expirado (§3.3).

Si (2) falla ⇒ la autorización queda **inutilizable para ese contenido**; el item vuelve a `review_decision = PENDING` y se emite `HUMAN_REVIEW_REQUIRED`. Si (3) falla ⇒ `REVISION_CHANGED`, con la propuesta preservada.

---

## 3. HumanAuthorization — contrato depurado

**Crítica campo por campo, según pide §27.**

```text
HumanAuthorization
  authorization_id            id opaco
  case_id
  proposal_id
  proposal_item_id            UNA autorización POR ITEM (ver §3.2)
  item_content_hash           vincula al contenido exacto revisado
  expected_case_revision      revisión VIGENTE del Case al revisar (NO base_case_revision:
                              FactsProposed y ArtifactRegistered ya la avanzaron)
  authorized_operation        enum; v0: COMMIT_FACT
  principal_id                quién autorizó (principal_type = HUMAN)
  authorization_source        REAL | DEV_STUB   ← ver §4
  created_at
  expires_at
  consumed_at                 NULL hasta el commit; una sola vez
```

### 3.1 Campos cuestionados y resueltos

- **`decision` — ELIMINADO.** Una `HumanAuthorization` solo se crea al aprobar; un objeto llamado "autorización" con `decision = REJECTED` es una contradicción de nombre. El rechazo se registra en `ProposalItemReview` (§3.4), que sí lleva la decisión. Esto responde a la pregunta literal de los dueños: *reject genera ReviewDecision, no authorization*.
- **`expires_at` — CONSERVADO.** Argumento para eliminarlo: el par (`item_content_hash`, `expected_case_revision`) ya invalida la autorización ante cualquier cambio. Argumento por el que se conserva, y que gana: ese par **no** cubre el caso de que nada cambie. Si un caso queda inactivo tres meses, una autorización aprobada al inicio seguiría siendo consumible sin que nadie la haya vuelto a mirar. Una autorización viva indefinidamente es superficie latente; el coste de cerrarla es un campo y una comparación. Valor por defecto configurable (`PROPUESTA: 24 h`), endurecible por política, nunca relajable a "sin expiración".
- **`single_use` — no existe como campo.** Es un invariante materializado por `consumed_at`.
- **`authorized_operation` — CONSERVADO** aunque en v0 tenga un solo valor. Sin él, una autorización obtenida para commitear un hecho serviría para cualquier operación sensible futura; añadirlo después obligaría a migrar autorizaciones existentes con una operación inferida.

### 3.2 Una autorización por item, no un conjunto

**PROPUESTA DEL TECHNICAL DESIGN.** La aprobación parcial es por item; si la autorización cubriera un conjunto, un cambio en un solo item invalidaría la aprobación de todos los demás — penalizando a la profesional por una edición no relacionada. Con una autorización por item, la invalidación es quirúrgica.

Para no perder la unidad del acto de revisión (útil para auditoría y UX), todas las autorizaciones emitidas en una misma sesión de revisión comparten `review_session_id`, que vive en `ProposalItemReview`.

### 3.3 Naturaleza server-side (ratificado por los dueños, §28)

La autorización **no viaja al modelo**. `commit_reviewed_facts(proposal_id, item_ids[])` no recibe ningún secreto: el Core resuelve internamente si existe autorización válida para cada item. El modelo puede saber que *hace falta* revisión; nunca recibe con qué autorizarla. Superficie de ataque: cero tokens en el contexto.

### 3.4 `ProposalItemReview` — el registro de la decisión

```text
ProposalItemReview
  review_id
  review_session_id
  proposal_item_id
  item_content_hash           el contenido efectivamente revisado
  decision                    APPROVED | REJECTED | PENDING
  principal_id                principal_type = HUMAN
  reviewed_at
  note                        opcional, texto de la profesional
```

Append-only. `APPROVED` produce además una `HumanAuthorization`. `REJECTED` y `PENDING` no producen ninguna.

---

## 4. DevHumanAuthorizationProvider (dueños, §6)

**DECISIÓN APROBADA.** Existe un stub para DEV/TEST con dos requisitos duros:

1. **FAIL TO START, no warning.** Si la configuración efectiva es de producción y el provider resuelto es el stub, el arranque **aborta** con error de configuración. No hay modo degradado ni advertencia ignorable.
2. **Marca indeleble.** Toda autorización emitida por el stub lleva `authorization_source = DEV_STUB`, persistido junto a la autorización y propagado al evento y al registro de auditoría. Un `case.db` que contenga autorizaciones `DEV_STUB` es identificable para siempre como caso de desarrollo; el Core rechaza abrir en modo producción un Case que contenga autorizaciones `DEV_STUB` consumidas.

**Test obligatorio (`AT-013`):** arrancar con configuración de producción y provider stub ⇒ el proceso no llega a estado operativo.

---

## 5. CaseRevision — ADR AMENDMENT CANDIDATE (dueños, §30)

Los dueños piden justificación formal de si la revisión humana debe avanzar `case_revision` antes del commit, y exigen no cambiarlo silenciosamente.

### 5.1 Análisis de los dos modelos

**Modelo A (consolidado en addendum v0.3 B.2):** `ReviewProposal` emite `ProposalReviewed` y avanza `case_revision`; el commit avanza otra vez.

**Modelo B (alternativa que plantean los dueños):** el estado de revisión de una propuesta vive en Application y **no** avanza `case_revision` hasta el commit.

**Argumentos decisivos a favor de B:**

1. **Semántica del reloj.** `case_revision` es el reloj del *estado epistémico canónico*: qué sabe el expediente. Una decisión de revisión aún no commiteada no añade hechos, evidencia ni links: el expediente sabe exactamente lo mismo antes y después. Avanzar el reloj sin cambio de conocimiento vacía de significado al reloj.
2. **Conflictos espurios.** Con el Modelo A, revisar la propuesta P-1 invalida cualquier análisis en vuelo generado contra la revisión anterior, aunque ese análisis no tuviera relación alguna con P-1. Es exactamente el falso conflicto que ADR-004 quiere evitar.
3. **Circularidad ya detectada.** Con el Modelo A, `expected_case_revision` de la autorización acaba siendo *la revisión resultante del propio acto de revisión*, definición circular que ya obligó a una corrección (addendum B.2). Con B desaparece: la propuesta se genera contra la revisión N, se revisa contra N y se commitea exigiendo que el caso siga en N. Limpio y verificable.

**Argumento a favor de A que hay que preservar:** la decisión de revisión **sí** es un hecho auditable y durable, y debe estar en el log append-only. Esto no exige avanzar `case_revision`.

### 5.2 Resolución propuesta: separar dos contadores

**PROPUESTA DEL TECHNICAL DESIGN (ADR AMENDMENT CANDIDATE sobre ADR-004):**

```text
event_seq       monotónico, +1 en TODO evento del Case Event Log
case_revision   monotónico, +1 SOLO en eventos que mutan el estado epistémico canónico
```

Cada evento registra ambos. Los eventos de revisión (`ProposalReviewed`) avanzan `event_seq` pero **no** `case_revision`. Los eventos de mutación canónica (`EvidenceIncorporated`, `FactsCommitted`, …) avanzan ambos.

Esto conserva la auditoría completa de A, elimina los conflictos espurios y la circularidad, y mantiene el invariante de biyección mutación↔evento del addendum B.3 (ahora expresado sobre `event_seq`, con `case_revision` como subsecuencia).

> **APROBADO — enmienda AC-02.** Los dueños aprobaron este amendment. **El Modelo B es ahora el vigente en todo el corpus**: `event_seq` avanza en todo evento; `case_revision` avanza solo en eventos que mutan el estado epistémico canónico; `ProposalReviewed` avanza `event_seq` y lleva `case_revision` nula. ADR-004 y ADR-005 quedan enmendados (supersedes §16.16 y §16.19). Queda sin efecto el aviso anterior de esta sección, que mantenía el Modelo A mientras la decisión estuviera pendiente.

Consecuencia sobre el addendum v0.3 B.2, **ya en vigor**: su punto 1 ("`ReviewProposal` … avanza la CaseRevision") queda **enmendado y superado**; su punto 3 se corrige — `expected_case_revision` es la **revisión vigente del Case en el momento del acto de revisión** — la que la profesional tiene a la vista al aprobar. **No es `base_case_revision`**: entre la generación de la Proposal y su revisión, los eventos `FactsProposed` y `ArtifactRegistered` ya avanzaron el contador, con lo que desaparece la circularidad de la definición anterior (que hacía portar a la autorización *la revisión resultante de su propio acto de revisión*). Los documentos técnicos aplican el Modelo B como norma y conservan el Modelo A solo como columna de trazabilidad, rotulada *anterior (superado)*.

---

## 6. Superficie MCP — reevaluación (dueños, §36–38)

**PROPUESTA DEL TECHNICAL DESIGN: 8 tools** (de 9).

| Tool | Clase | Cambio |
|---|---|---|
| `create_case` | COMMAND | — |
| `open_case` | QUERY | Devuelve candidatos ante ambigüedad; nunca adivina (§58 de los dueños) |
| `ingest_evidence` | COMMAND | Idempotente por hash de contenido |
| `get_case_context` | QUERY | Scopes §9 |
| `search_case` | QUERY | — |
| `get_evidence_fragment` | QUERY | — |
| `propose_facts` | PROPOSAL | Crea Proposal + ProposalItems |
| `commit_reviewed_facts` | SENSITIVE_COMMAND | Sin token; el Core resuelve autorizaciones |
| ~~`register_artifact`~~ | — | **RETIRADO de la superficie** |
| ~~`verify_legal_source`~~ | — | Fuera del slice (decisión de los dueños) |

**Justificación del retiro de `register_artifact`:** el único artifact del slice (`FactAnalysis`) es consecuencia directa de `propose_facts`; que el modelo lo registre por separado abre dos fallos —olvidar registrarlo, o registrar un artifact que no corresponde a ningún análisis real— sin aportar ninguna capacidad. El Core lo registra internamente dentro de la transacción de `ProposeFacts`. Regla general derivada: **una operación se expone solo si el modelo debe decidir cuándo ocurre**; si es consecuencia necesaria de otra, es interna.

`ADMIN` permanece **vacía por diseño** en la superficie del modelo.

---

## 7. Application Use Cases

| Use case | Expuesto | Transacción | Eventos | ¿Avanza `case_revision`? |
|---|---|---|---|---|
| `CreateCase` | sí | 1 | `CaseCreated` | sí |
| `OpenCase` | sí (`open_case`) | lectura | — | no |
| `IngestEvidence` | sí | 1 | `EvidenceIncorporated` (+ `ArtifactMarkedStale`*) | sí |
| `GenerateDerivedRepresentation` | **interno** | 1 | `DerivedRepresentationGenerated` \| `…Failed` | sí |
| `GetCaseContext` | sí | lectura | — | no |
| `SearchCase` | sí | lectura | — | no |
| `GetEvidenceFragment` | sí | lectura | — | no |
| `ProposeFacts` | sí | 1 | `FactsProposed` + `ArtifactRegistered` | sí |
| `ReviewProposal` | **canal humano**, no MCP | 1 | `ProposalReviewed` | **no** — avanza `event_seq`, no `case_revision` (enmienda AC-02 aprobada, §5.2) |
| `CommitReviewedFacts` | sí | 1 | `FactsCommitted` | sí |
| `EvaluateArtifactStaleness` | **interno** | dentro de mutadores | `ArtifactMarkedStale` | sí |
| ~~`RegisterArtifact`~~ | **interno**, dentro de `ProposeFacts` | — | `ArtifactRegistered` | (parte de la anterior) |

\* La propagación de staleness ocurre dentro de la misma transacción que la mutación que la causa.

`ReviewProposal` **no** entra por el MCP: entra por el canal de autorización humana, que es un driving adapter distinto (ADR-005). Es la materialización de que la revisión humana no pasa por el modelo.

---

## 8. Modelo de eventos y auditoría

**PROPUESTA DEL TECHNICAL DESIGN:** dos persistencias, tres conceptos (confirma la preferencia de los dueños en §31).

### 8.1 Case Event Log (canónico, append-only, hash-chained)

Unifica *Domain/Application Event* y *Audit Record*: un evento con principal, payload y hash **es** el registro de auditoría; dos streams duplicarían sin añadir información.

```text
CaseEvent
  event_id
  case_id
  event_seq                 monotónico por caso, +1 en TODO evento (enmienda AC-02 aprobada)
  case_revision             revisión resultante; **NULL** si el evento no muta estado epistémico
                            canónico (caso de `ProposalReviewed`)
  event_type
  payload                   estructurado, suficiente para reconstrucción
  principal_id / principal_type / principal_role
  provenance_kind
  methodology / model_id    cuando aplique
  occurred_at
  prev_event_hash
  payload_hash
  event_hash                = H(event_id, event_seq, prev_event_hash, payload_hash, …)
```

**Eventos v0 (lista cerrada):** `CaseCreated`, `EvidenceIncorporated`, `DerivedRepresentationGenerated`, `DerivedRepresentationFailed`, `FactsProposed`, `ArtifactRegistered`, `ProposalReviewed`, `FactsCommitted`, `ArtifactMarkedStale`. **Declarados sin productor en v0:** `FactWithdrawn` (conservado para no reabrir el contrato al implementar el retiro de hechos).

### 8.2 Tool Invocation Log (operacional, separado, podable)

Toda invocación MCP, incluidas las QUERY: `tool`, `principal/session`, hash de inputs, resultado y condiciones, duración, correlación con `event_id` cuando produjo mutación. No es estado canónico, no participa en el hash-chain, tiene política de retención. Sirve para diagnóstico y para verificar los tests adversariales.

### 8.3 Honestidad sobre el hash-chain

**Tamper-evident, no tamper-proof.** Detecta modificación, truncamiento y reordenamiento del log por parte de un proceso que no controle deliberadamente toda la cadena. Una usuaria hostil con control total de la máquina puede regenerar la cadena completa: está **fuera del threat model V0** y debe decirse por escrito. No se construye infraestructura criptográfica corporativa (sin firmas, sin HSM, sin anclaje externo obligatorio).

---

## 9. Proyecciones — `get_case_context`

Scopes v0: `overview | facts | evidence | pending | changes_since`. `procedural`: **RESERVADO**, no implementado.

```text
CaseContextResponse
  case_id
  case_revision            revisión vigente al generar
  event_seq                 ancla del delta preciso (enmienda AC-02 aprobada)
  scope
  params
  content                   dependiente del scope
  completeness             COMPLETE | PARTIAL
  omissions[]              { section, reason }   obligatorio si PARTIAL
  conditions[]             condiciones tipadas activas
```

`COMPLETE | PARTIAL` (dos valores; `TRUNCATED` del corpus previo se absorbe en `PARTIAL` con `reason = 'budget'`, porque para la usuaria y para el modelo la distinción operativa es la misma: falta algo y está declarado).

**Invariante:** `completeness = PARTIAL ⇒ omissions` no vacío. Un contexto parcial nunca puede parecer expediente completo.

`changes_since(revision)` alimenta el delta de sesión (§50 de los dueños) sin pedir al modelo que recuerde la sesión anterior.

---

## 10. Condiciones UX — clasificación por familia (dueños, §45)

Los dueños sospechan que `INTEGRATION_ERROR` no pertenece al Core. **Correcto.** Clasificación en tres familias:

| Familia | Origen | Condiciones v0 |
|---|---|---|
| **Epistemic** | Estado del conocimiento del caso | `ANALYSIS_STALE`, `SEARCH_INCONCLUSIVE`, `UNCERTAIN_FRAGMENT` |
| **Authority** | Reglas de autoridad y concurrencia | `HUMAN_REVIEW_REQUIRED`, `REVISION_CHANGED`, `OPERATION_NOT_PERMITTED` |
| **Infrastructure** | Fallos de adapters externos | `INTEGRATION_ERROR` |

`INTEGRATION_ERROR` sale del catálogo epistémico y pasa a familia propia: no dice nada sobre el caso, dice que un adapter falló. En v0 el slice no tiene conectores externos, así que **queda declarada sin disparador ejercitado** (honesto, en vez de simulado).

Pipeline obligatorio, para evitar que N códigos internos se conviertan en N mensajes:

```text
internal condition  →  presentation category  →  human message (plantilla por locale)
```

Categorías de presentación (cuatro): `NEEDS_YOUR_DECISION`, `SOMETHING_CHANGED`, `LIMITED_CERTAINTY`, `CANNOT_DO_THAT`. Varias condiciones internas pueden mapear a la misma categoría; la plantilla concreta añade el detalle.

---

## 11. Identificadores y hashing

- **Identidad de entidad:** `PROPUESTA DEL TECHNICAL DESIGN — UUIDv7`, opacos, generados por el Core, ordenables por tiempo, generables offline, no derivados de nombres ni de contenido. Sujeto a verificación de soporte real en Node LTS (§13, spike de dependencias). Alternativa equivalente: ULID.
- **Identidad de contenido:** SHA-256 sobre los bytes del original y sobre la forma normalizada de cada `item_content_hash` y `payload_hash`.
- **Regla dura:** un hash **nunca** es un identificador de entidad ni se muestra a la usuaria. `entity identity ≠ content identity`.

---

## 12. Product Floor propuesto (estado `PROPOSED`, dueños §17 y §44)

Cinco políticas, con el formato exigido. Comparadas con mi conjunto anterior; ver §12.6.

**PF-001 — AI cannot assign sensitive epistemic state.**
Riesgo que previene: que una inferencia del modelo adquiera el estatus de hecho alegado o determinado sin decisión humana.
Enforced in: Domain (reglas de transición) + Application (gate de commit).
Configuration may relax? **NO.**
How tested: `AT-001`, `AT-002`.

**PF-002 — Original evidence cannot be overwritten or deleted through the product surface.**
Riesgo: pérdida o alteración de la fuente primaria sobre la que se razona.
Enforced in: Infrastructure (almacén inmutable) + MCP (no existe la capacidad).
Configuration may relax? **NO.**
How tested: `AT-011`, verificación periódica de hash.

**PF-003 — Unincorporated external information cannot become canonical evidence or support.**
Riesgo: fundamentar un hecho en material que nadie incorporó y que puede desaparecer o no haber existido.
Enforced in: Domain (EvidenceLink exige Evidence incorporada) + Application.
Configuration may relax? **NO.**
How tested: `AT-005`.

**PF-004 — Unverified legal authority cannot become verified by model assertion.**
Riesgo: jurisprudencia o normas inventadas presentadas como verificadas — el riesgo n.º 1 del dominio.
Enforced in: Domain (transición de estado) + MCP (la capacidad no existe en v0).
Configuration may relax? **NO.**
How tested: test de superficie (la operación no existe); post-slice, test de transición.

**PF-005 — Mandatory uncertainty and integrity conditions cannot be suppressed by client configuration.**
Riesgo: que una organización silencie los avisos que hacen visible la incertidumbre.
Enforced in: Application (emisión) + Configuration (validación: solo endurece).
Configuration may relax? **NO.**
How tested: config que intenta suprimir una condición obligatoria ⇒ rechazo en carga.

### 12.6 Nota sobre la política desplazada

Mi conjunto previo incluía *"la auditoría no es desactivable ni editable por configuración"*. Al comparar, las cinco de los dueños cubren riesgos **directos del dominio jurídico**, mientras la auditoría es una meta-garantía. Como piden exactamente cinco, entrego las cinco de arriba y señalo que **"audit log cannot be disabled or edited by configuration"** es la sexta candidata natural: no la incluyo por disciplina de alcance, pero conviene decidir explícitamente si entra, porque hoy ninguna de las cinco la cubre.

---

## 13. Stack y layout

- **TypeScript + Node.js LTS** (DECISIÓN APROBADA). Versión concreta: se fija en implementación contra fuente oficial; no se congela aquí.
- **Sin framework grande.** `PROPUESTA`: TypeScript modular con composición explícita e inyección por constructor. NestJS no se justifica: aporta DI y modularidad que un core de este tamaño resuelve con composición, a cambio de decoradores, metadatos y acoplamiento del dominio al framework — contrario a la regla de vendor-independence.
- **Modular monolith**, fronteras lógicas `legal-core` / `legal-mcp` / `legal-plugin`; no implica procesos, paquetes ni repos separados.
- **Regla de dependencias** verificable automáticamente más adelante: `domain` no importa `application` ni `infrastructure`; `application` importa `domain`; `infrastructure` implementa puertos de `application`; `mcp` depende de contratos de `application`; `skills` nunca acceden a `infrastructure`; **`src/` nunca importa de `experiments/`**.

---

## 14. Precedencia documental (dueños, §83)

```text
1. ADRs Accepted (001–006)
2. Technical Design V0  (incluido este kernel)
3. Architecture Principles
4. Glossary
5. Addenda / notas de normalización (kernel v0.2, addendum v0.3)
6. Discovery / research / spikes
```

Regla: un documento de nivel inferior **no** puede redefinir una regla fijada en uno superior; si la contradice, gana el superior y el inferior debe corregirse. Un ADR `Proposed` no manda sobre un ADR `Accepted`. Los resultados de spike son **observaciones**, jamás garantías de plataforma, y viven en el nivel 6 aunque informen decisiones superiores.

---

## 15. Alcance: qué NO se diseña en esta iteración

Post-V0, registrados en `docs/backlog/architecture-post-v0.md`: Knowledge Pack Colombia, jurisprudencia, Legal Auditor, multi-máquina, sync, PostgreSQL, búsqueda vectorial, multi-agente, conectores (Gmail/Drive/Calendar), motor de plazos, motor procesal, actualizaciones automáticas, telemetría, licenciamiento, admin empresarial, multi-tenant. Y del dominio: `Statement` (reservado, §Q5), `Contradiction`, `Gap`, `LegalIssue`, `Hypothesis`, `Ruling`, `Term`/`Deadline`.
