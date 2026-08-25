## NO-REGRESIÓN — resultado por comprobación

**Limpias (1 línea cada una):**
- (2) `principal_role` vs `Case.context_role` en `09`: **PASA** — §2.3 los separa, la cabecera §2.1 no lleva `context_role`, la preimagen §4.2 lo excluye y el rol procesal viaja solo en el payload de `CaseCreated` (§3.2).
- (4) Decisión EFECTIVA en `08`: **PASA** — CTE único `effective` (§5.4), `INV-P-13`, y ninguna proyección de §5 emite `review_decision` almacenado.
- (5) Enum `PROPOSED|ALLEGED|DETERMINED|WITHDRAWN`: **PASA** — completo en `05` §6.2 (líneas 271-276) y `08` §5.2/§5.3 (417, 427) con productor declarado por valor.
- (7) snake_case en `06`: **PASA** — solo `effectiveReviewDecision` (nombre de función en pseudocódigo, citado igual por `08` §5.4) y `assertNoEffect` (helper de test); ningún campo en camelCase.
- (8) Pipeline de mensajes de producto y nivel de presentación: **PASA** — `11` §6.6 intacto y `12` §2.11/§6.6/§7.4 aloja `T-UX-01..12`, `INV-UX-01..14`, `SC-07` y `SC-08` con anfitrión declarado.
- (9) `pending_item_count` dentro del Technical Design: **PASA** — los tres campos en `03` §9.12/§10.12/§11.13, `05` §4.3 y §6.9, `06` §5.2 (filas 1/2/5) y §9, `10` §7, `11` §3.5, `12` §3.1. (Ver hallazgo 7 para los ADRs.)
- (10) Normalización Principal/`provenance_kind`: **PASA** — todo `actor_*` restante es nota histórica explícitamente marcada (kernel §1.5, `02` §1, `06` §0, `08` §0, `09` §2.4, `10` §0, ADR-005 §85, ADR-008 §178, glosario §655).

---

## HALLAZGOS

**1 · ALTA — kernel §8.1 no aplicó AC-04: `ProposalPreservedForReconciliation` sigue fuera de la lista cerrada**
`C:\Users\HITMA\Desktop\legal-workspace\docs\technical-design\v0\00-technical-kernel.md:310` — «**Declarados sin productor en v0:** `FactWithdrawn`».
Problema: AC-04 exige el evento **en la lista cerrada sin productor**. Cinco documentos ya lo aplican y señalan al kernel como el que falta (`04` §10 C1: *«el kernel §8.1 todavía no lo enumera en esa segunda categoría»*; `06` §5.4 opción 1: *«Requiere corregir la lista del kernel §8.1»*; también `03` §0.5, `05` §11.2, `09` §8.2). Con el kernel sin corregir, el documento raíz contradice la enmienda que todos los demás citan.
Corrección: en §8.1, añadir el evento a la lista cerrada y ampliar la segunda categoría a «**Declarados sin productor en v0:** `FactWithdrawn`, `ProposalPreservedForReconciliation`», con remisión a AC-04.

**2 · ALTA — AC-03 no aplicado en `boundaries.md` ni en `vertical-slice-v0.md` (el pase que `05` §11.1 dejó nombrado por escrito)**
`docs\architecture\boundaries.md:31` dice «**ocho tools v0** (ENMIENDA AC-03 aprobada)» pero la tabla inmediata (`:41`) sigue listando «`register_artifact` | COMMAND», `:64` dice «**Nueve** son alcanzables desde la superficie MCP» y `:234` rotula «tool calls · **9 tools v0** clasificadas». `docs\architecture\vertical-slice-v0.md:22` («Superficie MCP | **9 tools**»), `:78`, `:133` (paso 12 = `register_artifact`), `:248`, `:571` («exactamente las **9** tools v0»), `:617` (F9) y `:624` (F16: «Exactamente **9** tools»).
Problema: `05` §11.1 (línea 873) enumera **exactamente estos sitios** como «documentos de nivel inferior que **deben** corregirse en el pase de aplicación de AC-03»; el pase no se hizo. `boundaries.md` queda además autocontradictorio en 10 líneas.
Corrección: retirar `register_artifact` de ambas tablas de tools; `:64` → «**Ocho** son alcanzables desde la superficie MCP; `ReviewProposal` y `RegisterArtifact` no»; `:234` → «8 tools v0»; en el slice, retirar el paso 12 como invocación (sus eventos van en la transacción de `ProposeFacts`), reescribir F9 como test de use case interno y poner F16 y el criterio estructural 1 en ocho.

**3 · ALTA — `boundaries.md` conserva viva la identidad `seq == case_revision` y la formulación superada de AC-02**
`docs\architecture\boundaries.md:74` — «`CaseRevision` monotónica por Case, con **`seq == revision`**»; `:68` — «de 1 a n eventos, **avanzando la CaseRevision en n**».
Problema: AC-02 declara la identidad **SUPERADA** y ADR-001 §51 marca literalmente «Formulación superada: “avanzando la CaseRevision en n”». Aquí ambas aparecen sin marca alguna, como contrato vigente.
Corrección: `:74` → «`event_seq` avanza en todo evento; `case_revision` es la subsecuencia que avanza solo en mutaciones epistémicas canónicas y es NULL en las demás (ENMIENDA AC-02)»; `:68` → «de 1 a n eventos, avanzando `event_seq` en n y `case_revision` solo en los canónicos».

**4 · ALTA — ADR-001 inv. 2 reintroduce `seq == CaseRevision` en la misma frase que aplica AC-02**
`docs\architecture\adrs\ADR-001-trust-boundary.md:51` — tras el bloque «**ENMIENDA AC-02 aprobada**… `case_revision` es una **subsecuencia**», cierra: «…su `provenance_kind` y **`seq == CaseRevision` resultante**».
Problema: la cola del párrafo restablece la identidad que su propia cabeza acaba de superar. Un implementador que lea el invariante entero se queda con la última afirmación.
Corrección: sustituir por «…su `provenance_kind`, el `event_seq` resultante y el `case_revision` resultante **cuando el evento sea una mutación epistémica canónica** (NULL en caso contrario)».

**5 · ALTA — `05` §7 reintroduce estado agregado almacenado de la `Proposal` (regresión de la comprobación 1)**
`docs\technical-design\v0\05-mcp-contract.md:611` — «**postconditions.** `Proposal` en **`PENDING`** con `content_hash`»; `:620` — «la anterior sigue **`PENDING`**… **El estado `SUPERSEDED` de la Proposal existe en el enum** pero no tiene productor en V0».
Problema: el kernel §2.1 define `Proposal` **sin campo de estado**, `02` §4 (línea 401) lo declara así, `03` §10.7 dice «la Proposal **no almacena ningún dato de estado agregado**» y `04` §3.4 (`:334`) «SIN columna de estado agregado». Hablar de un «enum» de estado de la Proposal con valor `SUPERSEDED` resucita justo lo eliminado, y en el documento de contrato de superficie.
Corrección: `:611` → «`Proposal` registrada con `content_hash`; items con `review_decision = PENDING` y `commit_state = UNCOMMITTED`»; `:620` → sustituir la frase del enum por «el rótulo agregado es **derivado** (`06` §2.7); `SUPERSEDED` es vocabulario POST-V0 y **no es estado almacenado**».

**6 · ALTA — contrato de `Artifact`: tres formas incompatibles de `methodology`, y la nota de alineación de `10` afirma un hecho falso**
`10-artifact-lifecycle.md:118` — «`03` §9.6, `04` §3.4 y `05` §8.2 usan **`methodology_version` y `model_id` planos**». Pero `03-application-use-cases.md:644` escribe `methodology: { skill_id: 'fact-builder'; version: string }` y `05-mcp-contract.md:574` escribe `methodology: { skill: string; methodology_version: string }`; `04` (`:329`, `:391`) sí es plano.
Problema: la comprobación 6 falla. Un implementador tiene tres nombres para el mismo dato (`methodology_version` / `methodology.version` / `methodology.methodology_version`) y dos para el skill (`skill_id` / `skill`), y la nota que debería resolverlo declara una uniformidad que no existe.
Corrección: adoptar la forma plana del esquema (`methodology_version: string`, `model_id: string`) en `03` §9.3 y `05` §7 `propose_facts`; si el `skill_id` debe viajar, nombrarlo campo aparte y uniforme. Reescribir la nota de `10` §2.2 para que declare la corrección aplicada en vez de suponerla.

**7 · ALTA — ADR-005 se contradice a sí mismo sobre el payload de `HUMAN_REVIEW_REQUIRED`**
`docs\architecture\adrs\ADR-005-human-authority.md:128` (inv. 6, ya enmendado por AC-01) — «`HUMAN_REVIEW_REQUIRED {proposal_id, item_ids[], pending_item_count}`». Pero `:40` — «emite `HUMAN_REVIEW_REQUIRED {proposal_id}`» y la tabla de Validación `:171` fila 1 — «Rechazo; **`HUMAN_REVIEW_REQUIRED {proposal_id}`**; cero mutaciones». Igual en `ADR-001:95`, `glossary.md:678`, `principles.md:45` y `vertical-slice-v0.md:167,168,526,590,591,637,646,654,667,668`.
Problema: `11` §3.5 exige los tres campos «sin excepción y en **todo** sitio de emisión» (INV-UX-13), pero la corrección solo se aplicó al Technical Design. Los ADRs son **nivel 1** (kernel §14): su literalidad manda sobre `05`/`11`, y una tabla de tests normativa que pide `{proposal_id}` haría fallar `SC-07`.
Corrección: unificar a `{proposal_id, item_ids[], pending_item_count}` en ADR-005 §Decisión y su tabla de Validación, ADR-001 val. 2, glosario, `principles.md` y el slice; o, si no se tocan los ADRs, añadir en cada uno la nota de remisión «payload normativo completo en `11` §3.5 (INV-UX-13)».

**8 · MEDIA — `vertical-slice-v0.md` sigue escribiendo la forma superada del ancla como si fuera normativa**
`docs\architecture\vertical-slice-v0.md:28` — «el anclaje es un atributo del EvidenceLink (**`fragment { source_version_hash, selector }`**), no una entidad con identidad propia».
Problema: `04` §2.2 (`:123`) dice literalmente «Esa forma **queda superseded**», y `03` §8.3 y `05` §12 la marcan «SUPERSEDE… (nivel 5 < nivel 2)». Aquí aparece sin marca, y el slice es la fuente que esos documentos citan como origen del addendum B.17.
Corrección: añadir tras la cita «**forma SUPERSEDED** (`04` §2.2); la vigente es `{ v, source_id, anchored_in, derivation_id?, representation_hash, selectors[], original_locator }` (`07` §3.1)». No borrar el texto histórico.

**9 · MEDIA — tres nombres para el ancla de revisión del `Artifact`, y solo dos declarados como divergencia**
`10-artifact-lifecycle.md:77` `base_case_revision`; `04-persistence-model.md:388-390` (`TABLE artifacts`) `case_revision int NOT NULL -- revisión vigente al registrarlo`; `09-events-and-audit.md:328` `registered_at_case_revision: number`.
Problema: `10` §2.5 declara la divergencia **solo** frente a `04`; el tercer nombre de `09` no está declarado en ninguna parte. Además `04` y `09` no significan lo mismo que `10` (revisión al registrar vs revisión leída), de modo que no es solo nomenclatura.
Corrección: fijar dos campos con nombre único y semántica explícita —`base_case_revision` (la que el análisis leyó) y, si se necesita, `registered_at_case_revision` (la vigente al registrar)— y replicarlos idénticos en `04` §3.4, `09` §3.3 y `10` §2.2/§2.5, retirando `artifacts.case_revision`.

**10 · MEDIA — `02` §2.5 define `EvidenceFragment` con dos campos menos y sin remisión hacia la forma consolidada**
`02-domain-model.md:164-171` — la interfaz carece de `v` y de `original_locator`, presentes en `03` §8.3, `04` §2.2, `05` §6.4, `07` §3.1 y ADR-011 §29.
Problema: `07` §3.1 declara que «Consolida `02` §2.5… añade `original_locator` y `v`», pero `02` no dice nada: leído solo, define una forma de cinco campos incompatible con la de los otros cinco documentos.
Corrección: añadir en `02` §2.5, bajo la interfaz, una línea de remisión: «**Forma consolidada vigente en `07` §3.1**: añade `v: LocatorSchemaVersion` y `original_locator`. Esta sección define los campos del plano de recuperación; no es la forma completa del contrato».

**11 · MEDIA — ADR-005 conserva `proposal_content_hash` como vínculo exigido, contra AC-01**
`ADR-005-human-authority.md:165` — «vinculación verificable a **`proposal_content_hash`** y `expected_case_revision`»; tabla de Validación `:171` fila 4 — «Autorización cuyo **`proposal_content_hash`** no coincide…».
Problema: AC-01 sustituye `proposal_content_hash` por `item_content_hash` y lo retira como campo de la `HumanAuthorization`; ADR-008 §178 lo dice explícitamente. El criterio del spike de canal y el test 4 siguen redactados sobre el campo eliminado. (Residuo colateral: `05` §7 `:616` usa `proposal_content_hash` en la clave de idempotencia sin que ningún documento lo defina — `04` lo llama `proposals.content_hash`.)
Corrección: en ADR-005, `item_content_hash` en el criterio del canal y en la fila 4, con nota «(ENMIENDA AC-01: la vinculación es por `ProposalItem`)»; en `05` §7, renombrar a `proposal_content_hash → proposals.content_hash` o al nombre único que se fije.

**12 · MEDIA — `PRESERVED_FOR_RECONCILIATION` escrito como estado en el que la Proposal *queda*, contra AC-04**
`docs\architecture\boundaries.md:74` — «Proposal **preservada en `PRESERVED_FOR_RECONCILIATION`**»; `ADR-001-trust-boundary.md:55` — «Proposal preservada (**`PRESERVED_FOR_RECONCILIATION`**)».
Problema: AC-04 fija que la preservación es **conducta por defecto y estado DERIVADO, nunca almacenado**, y `08` §5.4 precisa que en V0 `status_derived` **nunca** toma ese valor porque el evento no tiene productor. La redacción actual se lee como transición a un estado guardado.
Corrección: en ambos sitios, «Proposal **preservada** —cero mutaciones: items, decisiones y autorizaciones quedan intactos y visibles en `get_case_context(pending)`—; el rótulo `PRESERVED_FOR_RECONCILIATION` es **derivado** y **sin productor en v0** (ENMIENDA AC-04)».

---

**Lectura de conjunto.** Las diez comprobaciones de no-regresión se sostienen **dentro** de `docs/technical-design/v0/` salvo dos puntos (hallazgos 5 y 6, ambos en `05` y `03`). El daño real está **fuera**: el kernel `00` (AC-04) y los documentos de nivel 1 y 5 —`boundaries.md`, `vertical-slice-v0.md`, `ADR-001`, `ADR-005`— nunca recibieron el pase de aplicación que `05` §11.1 y `06` §5.4 dejaron nombrado por escrito. Como los ADRs tienen precedencia sobre el Technical Design (kernel §14), esos residuos no son cosméticos: son el contrato que un implementador leería primero.