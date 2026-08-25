# Kernel de consolidación — decisiones normativas para la redacción (v0.2)

> **AVISO DE NORMALIZACIÓN (v0.4).** Este documento es **registro histórico** y conserva la escritura `actor_id / actor_type / actor_role`. Esa notación quedó **superada**: `Principal` (`principal_id`, `principal_type` ∈ HUMAN|AI|SYSTEM, `principal_role`) responde *quién ejecutó*, y `provenance_kind` (EXTERNAL_SOURCE|AI_DERIVATION|AI_INFERENCE|HUMAN_DECISION|SYSTEM) responde *cuál es la naturaleza epistemológica del origen*. Tabla de equivalencias y justificación en `docs/architecture/notes/normalizacion-principal-provenance-v0_4.md` (supersede §16.13). El texto histórico no se reescribe.


Este kernel es NORMATIVO para todos los documentos de la consolidación. Fija los refinamientos que las tareas piden decidir, para que los diez documentos sean mutuamente consistentes. Si un redactor detecta un conflicto entre este kernel y una DECISIÓN APROBADA de los dueños, NO lo resuelve por su cuenta: lo señala en su resumen de retorno. Los redactores no introducen alternativas nuevas ni reabren decisiones.

## 0. Estilo y reglas comunes

- Idioma: español. Los títulos de los 15 principios se conservan en inglés (así los aprobaron los dueños); su elaboración va en español. Nombres de entidades, estados, condiciones y tools en inglés (código conceptual), prosa en español.
- Etiquetas obligatorias donde aplique: HECHO VERIFICADO / DECISIÓN APROBADA / HIPÓTESIS / SUPUESTO / POR VERIFICAR / RIESGO / DECISIÓN PENDIENTE.
- En los ADRs, distinguir siempre "Decisión de arquitectura" de "Detalle de implementación de plataforma". Ninguna feature de Cowork puede volverse regla del Domain.
- Nada de código de producto (ni .ts/.js/.py/.sql). Sí: pseudocódigo, schemas conceptuales, tablas, Mermaid, ejemplos de estados.
- Referencias cruzadas entre ADRs por número (ADR-001…ADR-006).
- Los ADRs llevan Estado: **Accepted** (aprobados conceptualmente por los dueños). Preguntas abiertas van en su sección propia, no diluyen la decisión.

## 1. Hechos de plataforma ya verificados en esta iniciativa (reutilizables con la etiqueta HECHO VERIFICADO; no re-verificar)

- Claude Code: permisos deny/ask/allow por herramienta y por ruta (p. ej. `Read(.env)`, `mcp__server__*`); hooks `PreToolUse` bloqueantes (exit code 2); subagentes con `tools:` allowlist/denylist; sandbox Bash NO nativo en Windows. Fuente: code.claude.com/docs (permissions, hooks, subagents, sandboxing).
- Skills de Claude Code NO tienen versionado propio (solo los plugins); el versionado de metodología es metadato del producto. Fuente: code.claude.com/docs/en/skills.md.
- MCP: primitivas tools/resources/prompts; sin RBAC en la spec (permisos en capa cliente); `ToolAnnotations` (readOnlyHint, destructiveHint, idempotentHint, openWorldHint) existen pero son hints NO confiables ("MUST consider tool annotations to be untrusted"). Spec vigente 2026-07-28.
- MCP elicitation: existe desde spec 2025-06-18; **modo form NO garantiza respuesta humana** (controles de aprobación solo SHOULD); **modo URL** (desde 2025-11-25) con MUSTs fuertes: consentimiento explícito, URL visible, apertura en superficie que ni cliente ni LLM pueden inspeccionar. Candidato para el canal de autorización humana; soporte en el host concreto POR VERIFICAR.
- Cowork: verificado con docs oficiales (claude.com/product/cowork; support.claude.com art. 13345190 y 15520349): misma arquitectura agentic que Claude Code sin terminal; conectores MCP con modos de aprobación Manual/Auto/Skip; plugins que empaquetan skills/connectors/sub-agents; acceso directo a archivos locales en Desktop (macOS/Windows, planes de pago). POR VERIFICAR: granularidad de permisos (deny por ruta, hooks, superficie por subagente) y garantías de sandbox/VM sobre carpetas locales.
- SQLite (sqlite.org): WAL = lectores y escritores concurrentes, un escritor a la vez; WAL NO funciona sobre filesystems de red (todos los procesos en la misma máquina); corrupción documentada por locking defectuoso "especialmente en filesystems de red, NFS en particular"; límite ≈281 TB; FTS5 con bm25, tokenizers unicode61/ascii/porter(inglés)/trigram — sin stemming español de serie.
- W3C Web Annotation Data Model: Recomendación W3C 23-feb-2017; TextQuoteSelector (§4.2.4), TextPositionSelector (§4.2.5), composición vía refinedBy (§4.2.9).

## 2. Vocabulario canónico de entidades (glosario y todos los docs usan EXACTAMENTE estos nombres)

Case, Source, Evidence, Statement, Fact, EvidenceLink, ProvenanceRecord, ProfessionalDetermination, Artifact, CaseRevision, Proposal, HumanAuthorization, DerivedRepresentation.

- **Source**: material original incorporado (bytes preservados, hash SHA-256, provenance de incorporación, metadata). Reemplaza al "Document/original" de la revisión v0.1.1 (registrar como cambio de nombre, no de semántica).
- **Evidence**: rol probatorio de un Source dentro de un Case. Source ≠ Evidence. Deduplicación física de Sources entre Cases: DECISIÓN PENDIENTE (v0: copia por caso es aceptable).
- **DerivedRepresentation**: derivado regenerable de un Source (transcripción, OCR, texto normalizado), con versión, hash, receta (herramienta+versión) y referencia obligatoria a su Source. Nunca sustituye al Source. Estado de derivación en v0: PENDING | READY | FAILED.
- **Statement**: expresión atribuible a un actor, anclada a un fragmento verificable de una fuente (página / offsets / rango de timestamps sobre el original). Inmutable tras extracción; corrección = anulación + nuevo registro.
- **Fact**: proposición fáctica curada del Case, con historia de transiciones (nunca campo único mutable).
- **EvidenceLink**: relación N:M Fact ↔ fragmento de Evidence, con polaridad `SUPPORTS | CONTRADICTS | CONTEXTUALIZES` (enum cerrado en v0; si un redactor encuentra un caso claro donde sea insuficiente, lo señala — no agrega categorías "por si acaso"), actor creador, justificación, estado ACTIVE | RETIRED.
- **ProvenanceRecord**: obligatorio en toda entidad epistémica. actor_type ∈ `EXTERNAL_SOURCE | AI_DERIVATION | AI_INFERENCE | HUMAN_DECISION | SYSTEM`. Campos actor: `actor_id, actor_type, actor_role` (desde el schema inicial aunque v0 tenga una sola usuaria).
- **ProfessionalDetermination**: acto humano que habilita transiciones sensibles; registra actor (humano identificado), motivación, y los EvidenceLinks valorados (incluidos los CONTRADICTS). Una salida de IA jamás lo sustituye.
- **CaseRevision**: contador monotónico por Case; se incrementa en cada mutación commiteada.
- **Proposal**: conjunto de cambios propuestos (v0: hechos propuestos con sus links candidatos) pendiente de revisión humana; con content_hash. Estados: PENDING | APPROVED (parcial o total) | REJECTED | SUPERSEDED | PRESERVED_FOR_RECONCILIATION.
- **HumanAuthorization**: ver §5.
- **Artifact**: producto de trabajo registrado; ver §10.

## 3. Estados del Fact — REFINAMIENTO A SEÑALAR EXPLÍCITAMENTE

La lista de los dueños ("propuesta; alegada; respaldada; contradicha; profesionalmente determinada") mezcla estados almacenados con estados derivados. Refinamiento (marcarlo como refinamiento que no altera la intención, en ADR-003 y glosario):

- **Transiciones almacenadas** (status_history append-only, cada entrada con ProvenanceRecord): `PROPOSED` (nace de propose_facts, actor AI_INFERENCE o HUMAN_DECISION — corregido por addendum v0.3 B.1, supersede §16.7) → `ALLEGED` (commit con autorización humana) → `DETERMINED` (vía ProfessionalDetermination; kind v0: `ACCREDITED_BY_PROFESSIONAL`; reservado para contexto B: `DECLARED_PROVEN`). `WITHDRAWN` posible desde ALLEGED/DETERMINED (evento nuevo, no borrado).
- **Estados derivados** (computados desde EvidenceLinks activos, NUNCA almacenados como status): `SUPPORTED` (≥1 link SUPPORTS activo), `CONTRADICTED` (≥1 CONTRADICTS activo), `UNSUPPORTED` (0 links activos). La "controversión procesal" queda fuera del slice (reservada, ver v0.1.1 ADR CANDIDATO 3).
- Regla dura: actor `AI_*` no puede crear ni transicionar más allá de PROPOSED. Acreditar no desactiva links CONTRADICTS.

## 4. Superficie MCP v0 y clasificación (TAREA 5, §31)

Clases: `QUERY | COMMAND | PROPOSAL | SENSITIVE_COMMAND | ADMIN`.

| Tool | Clase | Nota |
|---|---|---|
| `open_case` | QUERY | Resuelve identificador natural → case_id + overview + revision. Ante ambigüedad devuelve candidatos, jamás adivina. |
| `create_case` | COMMAND | Con idempotency key. |
| `ingest_evidence` | COMMAND | Incorporación formal: snapshot + hash + provenance; idempotente por hash de contenido; dispara derivación asíncrona. Referencia material por identificador de Inbox resuelto por el Core — nunca rutas arbitrarias. |
| `get_case_context` | QUERY | Ver §8. |
| `search_case` | QUERY | Fragmentos con id + provenance. |
| `get_evidence_fragment` | QUERY | Contenido exacto + cadena de provenance. |
| `register_artifact` | COMMAND | Ver §10. |
| `propose_facts` | PROPOSAL | Crea Proposal; rechazo sintáctico si un hecho llega sin referencia de provenance ni marca explícita "solo alegado". No muta el Case state más allá de registrar la propuesta. |
| `commit_reviewed_facts` | SENSITIVE_COMMAND | Requiere HumanAuthorization vigente (ver §5). Nombre normalizado a plural (los dueños escribieron `commit_reviewed_fact` en §31 y `CommitReviewedFacts` en §32 — registrar la normalización). |

- `verify_legal_source`: FUERA del slice (decisión de los dueños).
- Clase `ADMIN`: **vacía por diseño en la superficie del modelo**. Las operaciones administrativas (migraciones, packs, reparación) existen solo en el runtime/CLI del producto, nunca como tools expuestas a Claude. Documentarlo como decisión, no como omisión.
- Toda respuesta de tool incluye `case_id` y `case_revision`. Errores como códigos semánticos estables + condición tipada.

## 5. Contrato HumanAuthorization (TAREA sobre §34) — REFINAMIENTO A SEÑALAR

Contrato semántico (independiente de transporte):

```text
HumanAuthorization
  authorization_id
  case_id
  proposal_id
  proposal_content_hash      ← AÑADIDO al esquema de los dueños: vincula la autorización
                               exactamente a lo revisado; sin él, una propuesta editada
                               tras la revisión podría commitearse
  authorized_items[]         ← null = toda la propuesta; subconjunto si la profesional
                               aprueba solo algunos hechos (pregunta abierta a dueños)
  operation                  ← enum v0: COMMIT_FACTS (genérico para futuras ops sensibles)
  actor_id, actor_type=HUMAN_DECISION, actor_role   ← corregido por addendum v0.3 B.1
                                                       (el original decía HUMAN, valor ausente
                                                        del enum canónico §2; supersede §16.7)
  expected_case_revision
  created_at
  expires_at                 ← vigencia corta configurable por política
  consumed_at                ← null hasta consumo
```

- Campo "single_use" ELIMINADO como campo: es un invariante (toda HumanAuthorization v0 es de un solo uso; consumed_at lo materializa). Señalar como simplificación del esquema propuesto.
- **Refinamiento clave (señalar en ADR-005, sección Alternativas):** la autorización es un REGISTRO SERVER-SIDE del Core, no un token portador que viaje por el contexto del modelo. `commit_reviewed_facts(proposal_id)` exige que exista una HumanAuthorization viva, no consumida, con content_hash y expected_case_revision coincidentes. El modelo no transporta ningún secreto: no hay nada que fabricar ni filtrar. Alternativa rechazada: token portador entregado al modelo (aun single-use, introduce un secreto en el contexto sin necesidad). Esto REFUERZA la intención aprobada ("un humanReviewed:true enviado por Claude es inválido"), no la altera.
- Transporte/UI: DECISIÓN PENDIENTE (spike). Candidatos: MCP elicitation modo URL (spec-verificado, soporte del host POR VERIFICAR), UI local mínima, CLI. El Domain no se acopla a ninguno.
- Sin criptografía en v0 (decisión de los dueños); dejar señalado el punto de evolución (firma del registro) sin diseñarlo.

## 6. Modelo de eventos (TAREA sobre §33, §19)

Tres conceptos, DOS persistencias en v0:

1. **Case Event Log (canónico; unifica Domain/Application Event + Audit Event).** Un solo log append-only por Case. Cada evento: `event_id, case_id, seq (== CaseRevision resultante), operation, actor_id/actor_type/actor_role, payload (cambio completo o resumen estructurado suficiente para reconstrucción), methodology_version (si aplica), model_id (si actor AI), knowledge_pack_versions (si aplica), timestamp, prev_hash, hash` (hash-chain tamper-evident). Justificación de la unificación: un evento de dominio con actor+payload+hash ES el registro de auditoría; dos streams duplicarían.
2. **Tool Invocation Log (operacional; separado).** Toda invocación MCP (incluidas QUERY): principal, tool, hash de inputs, resultado/condiciones, correlación con event_id cuando produjo mutación. No es estado canónico, no es hash-chained, es podable. Sirve para diagnóstico y para verificar los tests negativos.
3. **NO full event sourcing:** el estado vigente se materializa en tablas SQLite; el event log da reconstruibilidad y auditoría, no es el mecanismo de runtime. Eventos v0: CaseCreated, EvidenceIncorporated, DerivedRepresentationGenerated/Failed, FactsProposed, ProposalReviewed(approved/rejected/partial), FactsCommitted, FactWithdrawn, ArtifactRegistered, ArtifactMarkedStale, ProposalPreservedForReconciliation. (Lista cerrada para v0.)

## 7. Semántica de CaseRevision

- Monotónica por Case; cada evento del Case Event Log la incrementa (seq == revision).
- Toda tool COMMAND/SENSITIVE_COMMAND acepta `expected_revision`; mismatch ⇒ rechazo del commit + Proposal preservada (estado PRESERVED_FOR_RECONCILIATION) + condición `REVISION_CHANGED{expected, current, preserved_proposal_id}`. Nunca sobrescritura silenciosa, nunca descarte del trabajo. Sin locking pesimista.

## 8. Contrato de proyecciones (TAREA sobre §35, ADR-004)

- `get_case_context(scope, params?)`. Scopes v0: `overview | facts | evidence | pending | changes_since(revision)`. `procedural`: RESERVADO (documentado, no implementado en slice — el slice no tiene lógica procesal). Renombrado: `recent_changes` → `changes_since(revision)` porque requiere punto de referencia explícito (señalar el refinamiento).
- `pending` incluye: proposals PENDING, derivaciones PENDING/FAILED, artifacts stale, condiciones activas.
- Sobre (envelope) de toda respuesta: `{case_id, case_revision, scope, params, content, omissions[{section, reason}], completeness: COMPLETE|TRUNCATED|PARTIAL, conditions[]}`. Simplificación a señalar: `generated_from_revision` se elimina porque v0 SIEMPRE genera la proyección desde la revisión vigente en el momento de la llamada (sin caché); si algún día se cachean proyecciones, el campo vuelve. Presupuesto de tamaño por scope (política, no prompt); lo omitido SIEMPRE declarado en `omissions`.
- Proyecciones: regenerables, deterministas respecto del estado, jamás objetivo de escritura del modelo. Puede existir un `memory.md`-equivalente pequeño como orientación: proyección desechable, jamás canónica.

## 9. Catálogo de condiciones UX v0 (TAREA sobre §36) — 7 condiciones

Reducción normativa (señalar las unificaciones):

| Código | Severidad | ¿Bloquea? | Significado / trigger |
|---|---|---|---|
| `SEARCH_INCONCLUSIVE` | warning | no | La búsqueda no pudo completarse de forma confiable; NO afirma nada sobre el expediente (distinto de resultado vacío, que es dato normal). |
| `ANALYSIS_STALE {reasons[]}` | warning | bloquea su uso como vigente en salida final (política) | Artifact con insumos desactualizados. reasons ∈ NEW_EVIDENCE, INPUT_SUPERSEDED, METHODOLOGY_CHANGED. **Unificación: NEW_EVIDENCE_SINCE_ANALYSIS deja de ser condición aparte y pasa a ser reason; el delta al abrir un caso es CONTENIDO de changes_since, no condición.** |
| `HUMAN_REVIEW_REQUIRED {proposal_id}` | info/blocking | bloquea la operación sensible | Operación sensible intentada sin HumanAuthorization vigente. **Absorbe PENDING_CONFIRMATION de v0.1.1 (registrar como superseded).** |
| `REVISION_CHANGED {expected, current, preserved_proposal_id}` | warning | bloquea ese commit | Commit sobre revisión obsoleta; trabajo preservado como propuesta para reconciliación. |
| `UNCERTAIN_FRAGMENT {ranges}` | info | no | Fragmentos de derivado bajo umbral de confianza; el original sigue siendo la fuente. |
| `OPERATION_NOT_PERMITTED {operation, policy_reason}` | blocking | sí | Capacidad no disponible para el principal/perfil o vetada por política; motivo en términos de política, jamás de ingeniería. |
| `INTEGRATION_ERROR {integration, effect_on_state}` | warning/blocking | bloquea la operación externa | Fallo de adapter externo. El mensaje SIEMPRE afirma el efecto sobre el estado (v0: NONE — las operaciones externas del slice no dejan estado a medias visible). |

Fuera de v0 (post-slice, registrar): `SOURCE_UNVERIFIED`, `CONTRADICTION_DETECTED`, `ANALYSIS_REUSED`, `NO_SUPPORT_FOUND` (los hechos sin soporte son dato de proyección facts/pending, no condición). Cada condición en el doc del slice lleva: meaning, trigger técnico, severity, user-visible (todas lo son), blocking, mensaje humano ejemplo (es-CO profesional; redacción = SUPUESTO hasta validar con la usuaria; fidelidad epistémica obligatoria: no elevar estado, no confundir búsqueda fallida con ausencia de prueba, no confundir integridad con autenticidad).

## 10. Artifact v0 (TAREA sobre §17)

Schema conceptual mínimo = el de los dueños + 3 campos justificados (señalar):

```text
Artifact
  id, type, case_id, created_at, created_by (actor triple), case_revision
  inputs[] { entity_id, content_hash }     ← incluye la DerivedRepresentation exacta consumida
  methodology_version                       ← versión de skill/metodología (metadato del producto;
                                              HECHO VERIFICADO: la plataforma no versiona skills)
  model_id
  status: DRAFT | REGISTERED | REVIEWED(by, at, at_revision) | SUPERSEDED
  stale: bool
  stale_reasons[]            ← AÑADIDO: sin razón, ANALYSIS_STALE no puede explicarse
  supersedes_artifact_id?    ← AÑADIDO: cadena simple (no DAG) para "versión anterior"
  knowledge_pack_versions[]  ← vacío en el slice; obligatorio cuando el artifact dependa de un pack
```

Evolución declarada (NO diseñar ahora): DAG de dependencias entre artifacts, razones de supersede tipadas, branching. Reuso idempotente de análisis: post-slice.

## 11. Parámetros del vertical slice v0

- Contexto A (rol LITIGANT) únicamente; datos sintéticos o anonimizados; una máquina; una usuaria; **0 subagentes**; conectores externos: NINGUNO (solo Inbox local); skill ejercitado: `fact-builder` v0 (cubre extraer hechos candidatos desde transcripción + documento; `hearing-analysis` NO es necesario para el slice); Knowledge Packs: ninguno cargado (el slice no ejercita conocimiento jurídico; el contrato de pack se documenta aparte).
- Flujo aprobado (§23 de los dueños): crear case → abrir → incorporar audio (preservar original+hash) → derivar transcripción → incorporar documento → fact-builder → propose_facts (Fact ↔ EvidenceFragment) → revisión humana → commit → cerrar sesión → nueva sesión → recuperar contexto → nueva evidencia → detectar obsolescencia/impacto.
- Derivación asíncrona: modelo de job mínimo = estado en la DerivedRepresentation (PENDING|READY|FAILED) consultable vía `get_case_context(pending)`. Sin motor de jobs genérico en v0.
- Los 10 tests negativos de §24 son criterios de aceptación de primera clase; mapear cada uno a invariante + condición emitida en la matriz de pruebas.

## 12. Workspace vs Private State (ADR-002)

- `USER WORKSPACE` (visible/operable desde el host): `Inbox/` (entrada de material), `Exports/` (salidas para la usuaria), `Working/` (borradores). 
- `LEGAL OS PRIVATE STATE` (solo vía Core): runtime, case databases, originals, derived versions, event log, artifact registry, policies, indexes, integrity metadata. NO fijar ruta concreta (la regla es la separación, no el path; AppData es ilustrativo, no decisión).
- Único camino normal: host → Legal MCP → Application → Case Store. La ingesta lee de Inbox por referencia resuelta por el Core; el Core copia bytes al private state (snapshot) — el archivo de Inbox deja de ser la fuente tras la incorporación.
- Enforcement frente al host: decisión de arquitectura = la frontera; detalle de plataforma = con qué se impone (deny rules/hooks verificados en Claude Code; garantías de Cowork Desktop POR VERIFICAR; proceso separado como alternativa). El Domain no depende del mecanismo.

## 13. Release / integridad mínima v0 (§37) — va en boundaries.md

Tres ciclos de vida: runtime (release sellado) / configuration (mutación controlada) / workspace+private state (operativo). Mínimo v0: product version (semver) + schema version del workspace + manifest con hashes del producto sellado + verificación de integridad al arranque + migraciones numeradas solo-adelante + backup verificado antes de cada migración + degradación a solo-lectura ante fallo de integridad. NADA más (sin auto-update, firma, telemetría, canales).

## 14. Product Floor v0 (§21) — primer conjunto universal (va como anexo en principles.md)

1. Una fuente jurídica no verificada jamás se promueve a verificada de forma silenciosa ni por afirmación del modelo.
2. Ningún actor `AI_*` efectúa transiciones epistémicas sensibles (ALLEGED, DETERMINED) ni las autoriza.
3. Las condiciones de clase blocking y los avisos de incertidumbre no son suprimibles por configuración de cliente; la configuración solo endurece.
4. Los Sources son inmutables por la superficie normal del producto; no existe operación de borrado expuesta (expurgo legal futuro = procedimiento privilegiado con acta, fuera de la superficie del modelo).
5. La auditoría (Case Event Log) no es desactivable ni editable por configuración.

## 15. Skills y Agents (estado consolidado; se menciona en boundaries y slice, sin doc propio)

- Skills conservados (metodología): intake-structuring, fact-builder, hearing-analysis, contradiction-analysis, legal-issue-spotting, legal-research, legal-drafting, adversarial-review. NO todos en v0; el slice usa solo fact-builder.
- Movidos fuera de Skills: chronology-builder (proyección determinista → Application), citation-verification (→ Core/Adapter), procedural-state (→ Domain/Application), final-quality-review (→ Core gates + adversarial-review).
- Agents: 0 subagentes en el slice (DECISIÓN APROBADA). Legal Auditor: posibilidad futura condicionada a evals; no requerimiento v1.
- Regla: si el sistema deja de ser seguro porque el modelo ignoró un SKILL.md, hay lógica crítica en el lugar equivocado.

## 16. Registro de supersedes respecto de la revisión v0.1.1 (señalar en los docs que corresponda)

1. "Toda mutación exige confirmación explícita PENDING_CONFIRMATION" (v0.1.1, C.5/invariantes) → SUPERSEDED: las mutaciones se dividen en COMMAND (la orden conversacional de la usuaria basta; idempotencia + revisión protegen) y SENSITIVE_COMMAND (exigen HumanAuthorization). La condición PENDING_CONFIRMATION desaparece; HUMAN_REVIEW_REQUIRED cubre lo sensible.
2. "Document/original" → renombrado **Source** (sin cambio semántico).
3. Superficie de 10 tools con `verify_legal_source` → 9 tools sin ella (fuera del slice).
4. `commit_reviewed_fact` → `commit_reviewed_facts` (normalización singular/plural).
5. `NO_SUPPORT_FOUND` como condición → dato de proyección; solo `SEARCH_INCONCLUSIVE` queda como condición.
6. Token portador de aprobación → registro server-side de HumanAuthorization (refuerzo, ver §5).

## 17. Preguntas que NO se responden en los docs (se marcan DECISIÓN PENDIENTE / POR VERIFICAR)

- Transporte de autorización humana (spike pendiente: elicitation URL en el host / UI local / CLI).
- Deduplicación física de Sources entre Cases.
- Semántica exacta de "acreditado" para la profesional (pregunta de negocio §25.1).
- Granularidad de permisos y garantías de filesystem de Cowork Desktop.
- Lenguaje/runtime de implementación del Core (no decidido por los dueños; bloqueante para código, no para estos documentos).
- Proveedor de transcripción y sus capacidades de timestamps (adapter; POR VERIFICAR).
- Aprobación parcial de propuestas (authorized_items): propuesta en el contrato, pendiente de confirmación de los dueños.
