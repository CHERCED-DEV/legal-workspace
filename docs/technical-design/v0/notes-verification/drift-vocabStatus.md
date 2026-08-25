## Resumen

Revisados los 18 documentos del encargo. **Todos existen** salvo `ADR-007`, citado como `Proposed` por tres documentos y **ausente del repositorio** (hallazgo 15). Aparecieron además, fuera de la lista, `15-product-floor-proposal.md` y `16-open-implementation-decisions.md` (creados durante esta revisión, no auditados).

**Categorías sin hallazgos (una línea cada una):**
- **Reintroducción de `DEFERRED` / `INVALIDATED` como estado almacenado: NINGUNA.** Las 6 apariciones de `DEFERRED` y las 20 de `INVALIDATED` son todas justificaciones de su eliminación; `04` §3 registra explícitamente la ausencia de columna.
- **Lifecycle de `ProposalItem` en dos dimensiones: CONSISTENTE** en 00, 01, 02, 03, 04, 05, 06, 08, 10, 12 y ADR-008 (`review_decision PENDING|APPROVED|REJECTED` × `commit_state UNCOMMITTED|COMMITTED`). Ningún documento lo colapsa en un enum único.
- **`commit_reviewed_facts`: 66 apariciones, todas en plural y con el mismo nombre.** Los 8 nombres de tool son idénticos en todo el corpus; cero variantes.
- **`EvidenceSource`, `Content Pack`, `NOT_COMMITTED`, `PENDING_REVIEW` (como valor vigente), `CONFIRMED`: cero apariciones.** No hay drift en esos ejes.
- **`DerivedRepresentation`: `PENDING|READY|FAILED` consistente** en 01, 02, 03, 04, 05, 07, 08, 09, 11, 12, 13, ADR-003, ADR-006, ADR-011.
- **Normalización `actor_*` → `Principal`/`provenance_kind`: aplicada.** Las apariciones restantes son notas de supersede o citas históricas etiquetadas.

---

## Hallazgos (19, por gravedad)

### ALTA

**1. `Proposal` — cuatro vocabularios de estado incompatibles, uno de ellos almacenado**
- `02-domain-model.md` §4: `interface Proposal { … readonly status: 'PENDING'|'APPROVED'|'REJECTED'|'PRESERVED_FOR_RECONCILIATION'|'SUPERSEDED' }`
- `03-application-use-cases.md` §10.7: derivado, con un dato almacenado `preserved_for_reconciliation`; valores `PRESERVED_FOR_RECONCILIATION|PENDING|REJECTED|APPROVED|SUPERSEDED`
- `06-human-authorization.md` §2.7: derivado; valores `PENDING|PARTIALLY_COMMITTED|RESOLVED|PRESERVED_FOR_RECONCILIATION`
- `08-case-context-projections.md` §5.4: `reconciliation_state: 'NONE'|'PRESERVED_FOR_RECONCILIATION'`
- **Problema:** el kernel §2.1 define `Proposal` **sin campo de estado**. `02` —cuya sección se titula literalmente *"Conceptos de Application que el Domain toca (sin redefinirlos)"*— lo redefine añadiendo un `status` almacenado. Además los tres conjuntos de rótulos derivados **no comparten valores** (`APPROVED`/`REJECTED` vs `PARTIALLY_COMMITTED`/`RESOLVED`), y `PRESERVED_FOR_RECONCILIATION` tiene **tres predicados distintos**: booleano almacenado (`03`), invalidación por hash (`06`), existencia de evento sin `FactsCommitted` posterior (`08`).
- **Corrección:** fijar un único conjunto de rótulos derivados en el kernel §2 (recomendado: el de `06` §2.7, que es el único que expresa el commit parcial) y borrar `Proposal.status` de `02` §4 con nota de remisión. Unificar el predicado de `PRESERVED_FOR_RECONCILIATION` en un solo documento y que los otros dos lo citen.

**2. `09` colapsa `principal_role` con `Case.context_role` — exactamente lo que `02` §2.2 prohíbe**
- `09-events-and-audit.md` §2.1: `principal_role: string; // v0: 'lawyer' / LITIGANT`
- **Problema:** `02` §2.2 (REFINAMIENTO A SEÑALAR) separa `Principal.principal_role` (rol funcional, v0 `'lawyer'`) de `Case.context_role` (rol procesal, v0 `'LITIGANT'`) y advierte que colapsarlos obliga a duplicar el principal. `09` los mete en el mismo campo — y ese campo entra en la **preimagen del hash encadenado** (§4), de modo que el error queda fijado en el registro de auditoría.
- **Corrección:** dejar `principal_role: string; // v0: 'lawyer'` y, si el rol procesal debe viajar en el evento, añadirlo como campo separado `context_role` decidido explícitamente (afecta al hash: requiere decisión, no edición de comentario).

**3. `EvidenceFragment` — dos formas de ancla coexisten en documentos hermanos**
- Forma nueva (`{ v, source_id, anchored_in, derivation_id?, representation_hash, selectors[], original_locator }`): `02` §2.5, `07` §3.1, `ADR-011` §…
- Forma antigua (`{ source_version_hash, selector }`): `01` §…, `03` §7 y §8 (`GetEvidenceFragmentOutput`), `04` §2.2, `05` §6.4–6.5, `12`, `13`
- **Problema:** `representation_hash` aparece 40 veces (solo en 02/07/ADR-011) y `source_version_hash` 20 veces (en los demás). Son el mismo concepto con nombre y aridad distintas (`selector` singular vs `selectors[]` plural), y `02` §12 marca el cambio como `PROPUESTA` pendiente de aprobación. Quien implemente `get_evidence_fragment` leyendo `05` construirá un ancla que `07` declara insuficiente para ADR-003 inv. 7.
- **Corrección:** decidir la forma en el kernel §11 (o promover ADR-011 a Accepted) y propagar el resultado a `03` §8, `04` §2.2/§3.3, `05` §6.4–6.5, `12`, `13` en una sola pasada. Hasta entonces, que `05` cite explícitamente la divergencia como hace `07`.

**4. `08` proyecta la decisión **almacenada**, no la efectiva — contradice el riesgo mitigado por ADR-008**
- `08-case-context-projections.md` §5.4: `SUM(i.review_decision = 'APPROVED') AS approved`, `… AND i.commit_state='UNCOMMITTED') AS approved_uncommitted`; §5.1: `COUNT(DISTINCT proposal_id) … WHERE review_decision='PENDING'`
- **Problema:** ADR-008 §Consecuencias es literal: *"Exige que las proyecciones expongan siempre la efectiva y nunca la almacenada"*, y su RIESGO declarado es *"si una proyección expusiera la almacenada, mostraría como aprobado algo que no puede commitearse"*. El término "decisión efectiva" **no aparece ni una vez** en `08` (ni en `03`, ni en `04`); solo en `06` §2.5, `12` (AT-004) y ADR-008.
- **Corrección:** en `08` §5.1 y §5.4, sustituir el predicado por la decisión efectiva (`review_decision='APPROVED'` **y** autorización viva con hash y revisión coincidentes) y nombrar el campo de salida `effective_decision`; añadir el contract test que ADR-008 exige como mitigación.

**5. El enum de estatus almacenado del `Fact` se trunca de dos formas opuestas**
- `05-mcp-contract.md` §6.2: `status_filter?: ('PROPOSED' | 'ALLEGED')[]`
- `08-case-context-projections.md` §5.1: `facts_by_stored_status: { ALLEGED: number; DETERMINED: number; WITHDRAWN: number }`
- **Problema:** el enum canónico es `PROPOSED|ALLEGED|DETERMINED|WITHDRAWN` (ADR-003, `02` §5). `05` expone dos valores y omite `DETERMINED`/`WITHDRAWN`; `08` expone tres y omite `PROPOSED`. Son subconjuntos **complementarios** del mismo enum en dos contratos que se consumen juntos: un filtro por `DETERMINED` es inexpresable, y un contador de `PROPOSED` inexistente.
- **Corrección:** exponer los cuatro valores en ambos contratos, con la nota "sin productor en V0" donde corresponda (mismo patrón que `FactWithdrawn` en la lista cerrada de eventos), en vez de truncar el enum de forma distinta en cada documento.

**6. Contrato del `Artifact`: `10` y `04`/`03`/`05`/`09` usan nombres y formas distintas para los mismos campos**
- `10-artifact-lifecycle.md` §2.1: `artifact_type`, `methodology: { skill_id, version }`, `model: { model_id } | null`
- `04-persistence-model.md` §3.4 (`TABLE artifacts`): `type enum{FactAnalysis}`, `methodology_version text`, `model_id text`
- `03` §9, `05` §…, `09` §2.1 y kernel §8.1: `methodology_version` / `model_id` planos
- **Problema:** tres divergencias simultáneas (nombre del tipo, y estructura objeto vs escalar para metodología y modelo). `10` §2.5 declara **solo** la divergencia de `base_case_revision`; las de `artifact_type`, `methodology` y `model` no están declaradas en ninguna parte.
- **Corrección:** alinear `10` §2.1 con el vocabulario ya usado por el kernel §8.1 y `04` (`type`, `methodology_version`, `model_id`), o —si la forma estructurada se prefiere— registrarla como `PROPUESTA` explícita y corregir `04`, `03`, `05`, `09` a la vez. No dejar las dos formas conviviendo.

**7. `06` escribe todos sus contratos en camelCase; el resto del corpus, en snake_case**
- `06-human-authorization.md` §3: `authorizationId, caseId, proposalId, proposalItemId, itemContentHash, expectedCaseRevision, authorizedOperation, principalId, authorizationSource, createdAt, expiresAt, consumedAt`
- **Problema:** 35 identificadores camelCase, **todos concentrados en `06`** (cero en los otros 17 documentos). El kernel §3 fija el contrato en snake_case y su preámbulo exige usar los nombres **literalmente**; `04` §3.3 crea las columnas en snake_case. Peor: dentro del propio `06`, la tabla §3.1 justifica los campos usando snake_case (`authorization_id`, `item_content_hash`) mientras la interfaz de arriba usa camelCase — el mismo documento se contradice a dos párrafos de distancia.
- **Corrección:** reescribir el bloque de interfaces de `06` §3 (y los equivalentes de `ProposalItemReview`) en snake_case, idéntico al kernel §3.

### MEDIA

**8. `knowledge_pack_versions` tiene tres tipos distintos, y uno de ellos entra en el hash de auditoría**
- `02` §2.3: `readonly string[]` · `09` §2.1: `Record<string, string> | null` · `10` §2.1: `Array<{ pack_id, version }>` · `04` §3.4: `json`
- **Problema:** `09` §4 incluye `hash_or_nil(knowledge_pack_versions)` en la preimagen del `event_hash`. Sin una forma canónica única, dos implementaciones producen cadenas distintas para el mismo contenido. Que en V0 esté vacío oculta el defecto hasta que deje de estarlo.
- **Corrección:** fijar una sola forma en el kernel (recomendado el par explícito `{pack_id, version}[]` de `10`, ordenado por `pack_id`) y declararla como forma normalizada para el hash.

**9. `artifacts.case_revision` (`04`) vs `base_case_revision` (`10`) — mismo campo, semántica opuesta**
- `04` §3.4: `case_revision int NOT NULL -- revisión vigente al registrarlo`
- `10` §2.2: *"la revisión **que el análisis leyó**, no aquella en la que se escribió la fila"*
- **Problema:** no es solo el nombre: los comentarios describen **dos valores distintos**, y el campo es el ancla de staleness. `10` §2.5 declara la divergencia y propone el renombrado, pero `04` no la incorpora.
- **Corrección:** renombrar la columna a `base_case_revision` en `04` §3.4 con el comentario de `10`, o registrar la disputa como `DECISIÓN PENDIENTE` en ambos documentos. Dejarla declarada en un solo lado invita a implementar el otro.

**10. `changes_since`: `05` solo conoce `since_revision`; `08` contrata `since_event_seq`**
- `05` §6.2: `since_revision?: number; // OBLIGATORIO si scope='changes_since'`
- `08` §6.1: *"El cursor es `event_seq`, no `case_revision`"*, con `ChangesSinceParams { since_event_seq?, since_revision? }` y ejemplos que invocan `{since_event_seq: 7}`
- **Problema:** `08` declara la divergencia (*"Requiere reconciliación de `05`"*), pero mientras no se reconcilie el contrato MCP publicado rechaza por `VALIDATION_FAILED` el parámetro que la proyección considera el único correcto bajo el Modelo B.
- **Corrección:** añadir `since_event_seq` al `GetCaseContextInput` de `05` §6.2 con la regla "exactamente uno de los dos" de `08` §6.1, o congelar `08` en `since_revision` hasta que se apruebe el amendment del kernel §5.2.

**11. `completeness`: dos valores en el corpus técnico, tres en un ADR Accepted**
- kernel §9, `05` §6.2, `08` §2.2: `COMPLETE | PARTIAL` · `ADR-004` (Accepted): `COMPLETE | TRUNCATED | PARTIAL`
- **Problema:** por la regla de precedencia del propio kernel §14, un documento de nivel 2 no puede redefinir una regla de nivel 1. La divergencia está declarada en `01` §… y `08` §2.2, pero los documentos técnicos ya implementan el enum de dos valores.
- **Corrección:** tramitar el amendment de ADR-004 antes de congelar los contratos, o restaurar `TRUNCATED` en `05`/`08` mientras ADR-004 siga Accepted con tres valores.

**12. Nombres de tipo primitivos divergentes entre documentos**
- Hash: `ContentHash` (`02`, `06`, `07`) vs `Sha256` (`03`, `05`, `08`, `09`, `10`) vs `Sha256Hex` (`06`, en el mismo documento que usa `ContentHash` 13 veces)
- Tiempo: `Timestamp` (`02`, `07`, `10`) vs `Instant` (`06`) vs `Iso8601Utc` (`09`)
- Identidad: `06` usa `UUID` desnudo donde `02` §2.1 define tipos opacos marcados (`CaseId`, `SourceId`, …) y el kernel §11 deja ULID como alternativa equivalente — escribir `UUID` en el contrato congela una decisión que el kernel dejó abierta.
- **Corrección:** declarar en el kernel §11 los tres alias canónicos (`ContentHash`, `Timestamp`, `<Entity>Id` opaco) y sustituir en `03`, `05`, `06`, `08`, `09`, `10`.

**13. `13` reutiliza `CONTRADICTED` y acuña `PARTIALLY_SUPPORTED` para un concepto distinto del estado derivado del `Fact`**
- `13-synthetic-benchmark.md` §…: `classification CONSISTENT | CONTRADICTED | PARTIALLY_SUPPORTED | DECLARANT_ONLY | LATE_EVIDENCE_ONLY`
- **Problema:** `CONTRADICTED` es un valor del enum derivado canónico (`SUPPORTED|CONTRADICTED|UNSUPPORTED`) y aquí significa otra cosa: `EF-03` tiene `classification = CONTRADICTED` pero estado derivado `SUPPORTED + CONTRADICTED`. `PARTIALLY_SUPPORTED` no pertenece a ningún enum del corpus. El propio documento distingue *soporte formal* de *corroboración* en §16.11, lo que demuestra que el solapamiento es conocido y no resuelto.
- **Corrección:** prefijar el vocabulario del fixture (`FX_CONSISTENT`, `FX_DISPUTED`, `FX_PARTIAL`, `FX_DECLARANT_ONLY`, `FX_LATE_EVIDENCE`) para que ningún token del benchmark colisione con un enum de dominio.

**14. `RESOLVED` de `open_case` tiene dos predicados contradictorios**
- `03` §3.4: *"`RESOLVED` **si y solo si** … coincidencia exacta única … sin score"* (listado como DECISIÓN QUE REQUIERE APROBACIÓN)
- `05` §7: *"`RESOLVED` si y solo si **un** candidato supera el umbral de aceptación **y** su margen sobre el segundo supera un mínimo configurado"*
- **Problema:** mismo valor de enum, dos reglas incompatibles (determinista vs puntuación con umbral), ninguna de las dos declara la otra. Si se aprueban por separado, quedan ambas en el corpus.
- **Corrección:** resolver en el kernel §6 (`open_case`) cuál es la regla y que el otro documento la cite; ambas no pueden ser `PROPUESTA` simultánea del mismo valor.

**15. `ADR-007` se cita como `Proposed` pero no existe**
- `04` §0 y §Referencias (*"`ADR-007-persistence-strategy-v0.md` (Proposed)"*), `04` §3.1 y §5, `ADR-009` §…, `ADR-011` §…
- **Problema:** cuatro documentos atribuyen un estado (`Proposed`) y contenido (`CaseStorePort`, retención de blobs, tres refinamientos aditivos sobre `derived_representations`) a un archivo ausente de `docs/architecture/adrs/`. El kernel se declara normativo "para los ADRs 007–011". Una referencia a un documento inexistente no es verificable y sostiene decisiones que nadie puede auditar.
- **Corrección:** crear ADR-007 con el contenido que los cuatro documentos ya le atribuyen, o sustituir las citas por la sección concreta de `04` que efectivamente decide cada punto.

### BAJA

**16. `EVIDENCE_ADDED` contradice el vocabulario de incorporación**
- `08` §6.3: `EvidenceIncorporated → EVIDENCE_ADDED`
- **Problema:** "incorporado" es término de carga en ADR-006 (*material no incorporado* ≠ *añadido*), y el propio `08` §6.3 impone una *"Regla de fidelidad epistémica del vocabulario"* según la cual el delta nombra la transición almacenada. `EVIDENCE_ADDED` es el único `DeltaEntryKind` que se aparta del nombre del evento que proyecta.
- **Corrección:** renombrar a `EVIDENCE_INCORPORATED`.

**17. `facts_by_derived_state` usa claves en minúscula para un enum canónico en mayúscula**
- `08` §5.1: `facts_by_derived_state: { supported: number; contradicted: number; unsupported: number }` frente a `facts_by_stored_status: { ALLEGED: …, DETERMINED: …, WITHDRAWN: … }` en la línea inmediatamente anterior.
- **Corrección:** unificar a mayúsculas (`SUPPORTED|CONTRADICTED|UNSUPPORTED`), que es la forma canónica de ADR-003.

**18. `RESOLVED` nombra dos cosas distintas en el mismo corpus**
- Rótulo agregado de `Proposal` (`06` §2.7) y valor de `resolution` de `open_case` (`03` §3.4, `05` §6.1, `08` §5.x).
- **Corrección:** renombrar el rótulo de `06` a `COMPLETED` o `FULLY_RESOLVED`; `RESOLVED` ya está tomado por la desambiguación de nombres.

**19. Nombres asimétricos dentro del mismo objeto `window`**
- `08` §6.4: `{ since_event_seq, since_revision, to_event_seq, to_case_revision }`
- **Problema:** el mismo eje se llama `since_revision` en un extremo y `to_case_revision` en el otro.
- **Corrección:** `since_case_revision` / `to_case_revision`, o `since_revision` / `to_revision`; una de las dos, no ambas.