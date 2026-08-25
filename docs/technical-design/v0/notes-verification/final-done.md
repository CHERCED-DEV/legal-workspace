## A. DEFINITION OF DONE — doce preguntas

| # | Pregunta | Veredicto | Dónde está la respuesta |
|---|---|---|---|
| 1 | Entidades que existen en V0 y cuáles no | **SÍ** | `02-domain-model.md` §3 (nueve entidades, `Case` raíz), §3.8 (`Statement` definido y no materializado), §7–§8; kernel §15 |
| 2 | Qué use cases existen | **SÍ** | `03-application-use-cases.md` §1 (once, con puerto, clase, tx, eventos y efecto sobre `case_revision`; ya con AC-02 y AC-03 aplicados: ocho tools MCP + canal humano + dos internos) |
| 3 | Qué se persiste y dónde | **SÍ** | `04-persistence-model.md` §1 (cuatro almacenes), §3 (DDL), §7 (filesystem, content-addressing); `09-events-and-audit.md` §1 (dos persistencias) |
| 4 | Qué operaciones puede solicitar el modelo | **PARCIAL** | Norma: ocho — ADR-001 inv. 3, `principles.md` §15, `05-mcp-contract.md` §6/§11.1, `12` §4 (`FT-013`+`SC-04`). Residuos vigentes en ADR-001 val. 7, `boundaries.md` §2.1, ADR-010 §11 y `16` OD-02 (H-04, H-10, H-12) |
| 5 | Qué decide Claude y qué necesita humano | **PARCIAL** | Reparto de autoridad: SÍ (ADR-005 §Decisión, `06-human-authorization.md` completo con AC-01 aplicado, ADR-008). La **forma del contrato** no: el esquema de nivel 1 (ADR-005 §2) sigue siendo el previo a AC-01 y ADR-008 declara la sustitución "no vigente" (H-03, H-12) |
| 6 | De un Fact a los bytes originales | **SÍ** | `07-provenance-and-locators.md` §1 (cadena `Fact → EvidenceLink → fragment → DerivedRepresentation → Source`), §3 (locator), §1.5 (re-hash); ADR-011 |
| 7 | Trabajo creado contra contexto viejo | **PARCIAL** | Sustancia resuelta: `03` §11.6 (cero mutaciones, rótulo derivado), `06` §2.7 y §5.4 (predicado canónico), `11` §3.6, `09` §3.4. Falta cerrar la lista cerrada de eventos: kernel §8.1 no enumera `ProposalPreservedForReconciliation` (H-11) |
| 8 | Cómo se detecta obsolescencia | **SÍ** | `10-artifact-lifecycle.md` §5 (dos clases) y §6 (detección dentro de la tx del mutador, `reasons` y cuáles tienen productor); `03` §12; `11` §3.2 |
| 9 | Reabrir un Case sin conversación anterior | **SÍ** | `08-case-context-projections.md` §9 (`AT-010` con asserts), §5.1 `overview`, §6 `changes_since`, §7 `memory.md` (audiencia = modelo, cursor `event_seq`) |
| 10 | Cómo se evita acceso directo al Canonical State | **SÍ** | `08` §1.2 (tres capas), ADR-002, `01` §6, `05` §2 (R1–R6), `12` §3.5. B-04 es riesgo de anfitrión, no hueco de la respuesta |
| 11 | Condiciones técnicas → lenguaje profesional | **SÍ** | `11-ux-condition-catalog.md` §3 (siete condiciones), §6.2 (presupuesto), **§6.6** (segundo catálogo cerrado de mensajes de producto, INV-UX-13/14, T-UX-05/11) y `12` §2.11 + `SC-07`/`SC-08`. Cierra los huecos H-01 y H-03 de la verificación previa |
| 12 | Demostración frente a rutas adversariales | **PARCIAL** | `12` §3 (`AT-001..AT-013` con nivel, invariante y condición) y §3.5 (declaración honesta de lo no cubierto) + `13`. Abierto: escritura del host sobre `private-state/` — punto **B-04**, `INCONCLUSIVE`, declarado **BLOQUEANTE** (`12` §3.5, §7.x, §9; `16` OD-11) |

## B. CONTRADICCIONES DE ADR-001, ADR-004 y ADR-005 CONTRA SU PROPIA ENMIENDA

**H-01 · ADR-005 §1 fija la aritmética que su propia enmienda derogó — ALTA**
`C:/Users/HITMA/Desktop/legal-workspace/docs/architecture/adrs/ADR-005-human-authority.md` líneas 42 y 178.
Cita: «…deja `case_revision` **NULL** — la revisión del Case **no cambia** —… Si `FactsProposed` deja el Case en la revisión N, `ProposalReviewed` lo deja en **N+1** (y la autorización porta N+1 como `expected_case_revision`) y `FactsCommitted` lo deja en N+2.»
Problema: las dos mitades del mismo párrafo se contradicen, y la segunda es el Modelo A superado. Se repite literal en "Complementos" de §Validación ("en dos revisiones consecutivas… N+1… N+2"). Contradice la aritmética de referencia del glosario (14 / 14 / 15).
Corrección: sustituir ambas frases por «si `FactsProposed` deja el Case en N, `ProposalReviewed` lo deja **en N** (`case_revision` NULL) y la autorización porta **N**; `FactsCommitted` lo deja en N+1».

**H-02 · ADR-005 §4 (`ReviewProposal`) afirma lo contrario de su etiqueta AC-02 — ALTA**
Mismo archivo, línea 97.
Cita: «**NO muta el estado epistémico canónico** (ENMIENDA AC-02 aprobada): emite `ProposalReviewed(...)` **y avanza la CaseRevision**… que porta como `expected_case_revision` **la revisión resultante de ese mismo acto**… El commit posterior… con su propia revisión.» Añade «(total o, **si los dueños confirman la aprobación parcial**, restringida a `items`)», decisión ya resuelta por AC-01.
Corrección: «avanza `event_seq` y deja `case_revision` NULL»; `expected_case_revision` = la revisión contra la que se generó y revisó la Proposal; suprimir la condicional sobre la aprobación parcial (una autorización por item aprobado, agrupadas por `review_session_id`).

**H-03 · ADR-005 §2: el bloque de contrato normativo sigue siendo el anterior a AC-01 — ALTA**
Mismo archivo, líneas 53–60, 111, 126, 137, 160, 174, 185.
Cita (bloque §2): «`proposal_content_hash` ← AÑADIDO al esquema de los dueños» … «`operation` ← enum v0: **COMMIT_FACTS**».
Problema: el bloque que ADR-008 reconoce como precedencia de nivel 1 no contiene `item_content_hash`, `proposal_item_id` ni `review_session_id`, mantiene `proposal_content_hash` y el enum en plural — todo ello derogado por AC-01 diez líneas más abajo, en el propio ADR. El residuo se propaga al invariante 4, al criterio de salida del spike (§5.3), a Consecuencias positivas, a Riesgos, a la fila 4 de la tabla de validación y a la Pregunta pendiente 4 («hoy solo `COMMIT_FACTS`»).
Corrección: reescribir el bloque con `proposal_item_id`, `item_content_hash`, `review_session_id` y `authorized_operation = COMMIT_FACT`; reemplazar `proposal_content_hash` por `item_content_hash` en las seis apariciones restantes.

**H-04 · ADR-001: identidad `seq == CaseRevision` vigente, manifiesto de nueve tools y decisión ya resuelta — ALTA**
`C:/Users/HITMA/Desktop/legal-workspace/docs/architecture/adrs/ADR-001-trust-boundary.md` líneas 51, 100, 110.
Citas: inv. 2, tras declarar AC-02 — «…produce exactamente un evento… y **`seq == CaseRevision` resultante**»; val. 7 — «el manifiesto de tools contiene exactamente las **9 tools v0**» (inv. 3 dice ocho); Preguntas pendientes — «**DECISIÓN PENDIENTE (dueños) — Aprobación parcial** (`authorized_items` en HumanAuthorization)».
Corrección: «con su `event_seq`; `case_revision` solo si la mutación es epistémica canónica»; val. 7 a **ocho**; convertir la pregunta pendiente en RESUELTA por AC-01.

**H-05 · ADR-004 inv. 5 y validación 2 reinstalan la identidad superada — ALTA**
`C:/Users/HITMA/Desktop/legal-workspace/docs/architecture/adrs/ADR-004-case-memory.md` líneas 69 y 106.
Citas: inv. 5 — «**Cada evento porta `seq == CaseRevision` resultante**»; val. 2 — «una invocación que produce n mutaciones debe dejar n eventos y **avanzar la revisión en n**», dentro del mismo ítem que declara superada la identidad. Además, en inv. 5 y en (b)1 el delimitador «Formulación superada: «…» queda **sin cerrar**, de modo que texto vigente («`commit_reviewed_facts` … avanza la CaseRevision de nuevo») queda absorbido en la cita histórica y una afirmación falsa («Son dos eventos en dos revisiones distintas») queda **fuera** de ella.
Corrección: eliminar la frase `seq == CaseRevision`; en val. 2, «n eventos con `event_seq` contiguos; la revisión avanza solo por las mutaciones epistémicas canónicas»; cerrar las comillas angulares de las dos citas históricas.

**H-06 · ADR-004 §Relaciones-ADR-005 se contradice dentro de la misma frase — ALTA**
Mismo archivo, línea 124.
Cita: «El ciclo de propuesta consume **dos revisiones**: `ReviewProposal(approve)` … avanza **solo `event_seq`**, dejando `case_revision` NULL … —la autorización … congela como `expected_case_revision` **la revisión resultante de él**—».
Problema: si `case_revision` es NULL no existe "revisión resultante" que congelar; es exactamente la circularidad que AC-02 eliminó.
Corrección: «El ciclo de propuesta consume **una** revisión»; `expected_case_revision` = la revisión contra la que se generó y revisó la Proposal.

**H-07 · ADR-004 (c) e inv. 7 tratan la preservación como estado almacenado, contra la AC-04 del mismo ADR — ALTA**
Mismo archivo, líneas 60 y 71 (y ADR-005 línea 92).
Cita: «la Proposal implicada **se preserva en estado `PRESERVED_FOR_RECONCILIATION`**», frente a la AC-04 de la línea 45: «la preservación es la **conducta por defecto** y su estado es **derivado, no almacenado**».
Corrección: «su rótulo `PRESERVED_FOR_RECONCILIATION` se **deriva** según el predicado canónico de `06` §2.7; nada se marca ni se escribe». Alinear también el nombre del parámetro (`expected_revision` → `expected_case_revision`) en (c) y en inv. 7.

## Residuos fuera de los tres ADRs (mismo foco de coherencia)

**H-08 · `glossary.md` — la aritmética de referencia se rompe en su propio ejemplo — ALTA**
`C:/Users/HITMA/Desktop/legal-workspace/docs/domain/glossary.md` línea 691.
Cita: «…se registra `AUTH-9 {… expected_case_revision: **14** …}`: la autorización porta **15**, la revisión que la profesional tenía a la vista al aprobar, **no la 14** contra la que se creó la Proposal».
Problema: el registro dice 14 y la prosa inmediata dice 15 negando el 14. El ejemplo que fija la aritmética canónica es el que la desmiente. También `operation: COMMIT_FACTS` (plural).
Corrección: suprimir la cláusula «la autorización porta 15…» y dejar «porta **14**, la revisión que la profesional tenía a la vista»; `authorized_operation: COMMIT_FACT`.

**H-09 · `glossary.md` — tres residuos del Modelo A y el contrato de autorización sin AC-01 — ALTA**
Mismo archivo, líneas 547, 552, 598, 633–637, 649, 656.
Citas: bloque de lifecycle — «cada evento del Case Event Log --> revisión + 1 (**seq == revisión resultante**)»; §Proposal — «Son **dos eventos en dos revisiones distintas**» inmediatamente después de decir que no avanza la revisión; refinamiento 5 de `HumanAuthorization` — bajo rótulo «ENMIENDA AC-02 aprobada», el texto íntegro del Modelo A («emite `ProposalReviewed`, **que avanza la `CaseRevision`**… son dos eventos en dos revisiones distintas»); bloque de contrato — «`authorized_items[]` ← null = toda la propuesta… **(DECISIÓN PENDIENTE de los dueños)**», «`proposal_content_hash`», «`operation ← COMMIT_FACTS`».
Corrección: reescribir el bloque de lifecycle sobre `event_seq`; suprimir las dos frases "dos revisiones distintas"; sustituir el refinamiento 5 por la formulación de AC-02; reemplazar el bloque de contrato por el esquema por item.

**H-10 · `vertical-slice-v0.md` — AC-01 no aplicado al cuerpo, y AC-02 aplicado a medias — ALTA**
`C:/Users/HITMA/Desktop/legal-workspace/docs/architecture/vertical-slice-v0.md` líneas 49, 131, 149, 168, 198, 330–332, 407, 419, 428, 442, 573, 614.
Citas: §Scope — «**Aprobación parcial activada** (`authorized_items`): … **los dueños no la han confirmado**», mientras §Preguntas 688 dice «**RESUELTA — ENMIENDA AC-01 aprobada**»; paso 10 — «HumanAuthorization … con `proposal_content_hash` y `expected_case_revision` = **revisión resultante de este mismo acto**»; línea 149 — «Son **dos eventos en dos revisiones distintas**» justo después de que 148 declare `case_revision` NULL; línea 442 — «cada evento del Case Event Log la incrementa y **`seq == revision`** resultante».
Corrección: aplicar AC-01 al bloque de contrato, al paso 10, a F7, a F16 y al criterio de salida del spike; borrar "dos revisiones distintas" y la identidad `seq == revision` de §B y §Test matrix.

**H-11 · `boundaries.md` y kernel §8.1 — las dos listas cerradas del corpus están desalineadas — ALTA**
`C:/Users/HITMA/Desktop/legal-workspace/docs/architecture/boundaries.md` líneas 31/41/74/234/54/323 y `C:/Users/HITMA/Desktop/legal-workspace/docs/technical-design/v0/00-technical-kernel.md` línea 310.
Citas: boundaries §2.1 titula «**ocho tools v0** (ENMIENDA AC-03 aprobada)» y a continuación su tabla lista **nueve filas**, incluida «`register_artifact` | COMMAND»; el diagrama de §5 rotula «**9 tools v0 clasificadas**»; §Revisiones — «`CaseRevision` monotónica por Case, **con `seq == revision`**»; §2.2 y §Preguntas conservan `authorized_items[]` como pendiente. Kernel §8.1 — «Eventos v0 (lista cerrada): … **Declarados sin productor en v0: `FactWithdrawn`**», **sin** `ProposalPreservedForReconciliation`, que AC-04 y ADR-004 (b)1 sí incluyen (`04` §10 lo señala como POR VERIFICAR).
Corrección: borrar la fila `register_artifact` y corregir el rótulo del diagrama a ocho; reescribir §Revisiones sobre `event_seq`; marcar la aprobación parcial como resuelta; añadir `ProposalPreservedForReconciliation` a la segunda categoría del kernel §8.1.

**H-12 · El tablero de bloqueantes y dos ADRs siguen declarando abierto lo aprobado — ALTA**
`C:/Users/HITMA/Desktop/legal-workspace/docs/technical-design/v0/16-open-implementation-decisions.md` §2 y §3; `.../adrs/ADR-010-...md` líneas 20, 103, 131, 193–194, 261; `.../adrs/ADR-008-...md` línea 178.
Citas: `16` §2 — «**OD-02** … ¿8 tools vs 9? | **SÍ** [bloquea] | **Dueños**» y «**OD-04** Granularidad de `HumanAuthorization` … | **SÍ** | **Dueños**», con el recuento «**Cinco bloqueantes**» (OD-01 sí figura tachada como resuelta); ADR-010 — «se documenta como **conflicto sin resolver** en §11» y «**ocho** si se aprueba el retiro …, **nueve** mientras ADR-001 siga vigente sin enmienda»; ADR-008 — «**Mientras este ADR siga en `Proposed`**, el esquema literal de ADR-005 §2 conserva su precedencia de nivel 1 … y **esta sustitución no está vigente**».
Problema: la puerta de entrada a implementación afirma que dos decisiones ya aprobadas siguen bloqueando, y ADR-008 declara no vigente precisamente la sustitución que AC-01 aprobó — con ADR-005 §2 sin enmendar (H-03), el corpus no tiene ningún esquema de autorización vigente de nivel 1.
Corrección: tachar OD-02 y OD-04 como RESUELTAS por AC-03 y AC-01, recontar a **tres bloqueantes**; añadir a ADR-010 y ADR-008 la misma **Nota de vigencia** que ADR-009 ya lleva en su cabecera; en ADR-008 §Relaciones, sustituir la cláusula de precedencia por «AC-01 aprobada: la sustitución **está vigente** con independencia del estado de este ADR».

## C. QUÉ SIGUE EN PARCIAL Y POR QUÉ

- **Q4 (operaciones del modelo) — PARCIAL por residuo, no por decisión.** AC-03 fijó ocho y el Technical Design lo ejecuta (`FT-013` + `SC-04` cuentan ocho). Bloquea que el test de superficie tiene **dos fuentes normativas que dan cifras distintas**: ADR-001 val. 7 dice nueve y la tabla de `boundaries.md` §2.1 enumera nueve. Cierra con H-04 y H-11.
- **Q5 (reparto de autoridad) — PARCIAL por forma de contrato.** El *quién decide qué* está cerrado y es coherente en `06` y ADR-008. Lo que falta es el esquema: ADR-005 §2 sigue siendo el previo a AC-01 y ADR-008 declara su sustitución no vigente, de modo que un implementador no puede saber qué tabla `human_authorizations` construir. Cierra con H-03 y H-12.
- **Q7 (trabajo contra contexto viejo) — PARCIAL por la lista cerrada de eventos.** La aritmética (AC-02) y el estatuto de la preservación (AC-04) están resueltos y bien aplicados en `03` §11.6 y `06` §2.7. Falta que kernel §8.1 enumere `ProposalPreservedForReconciliation` sin productor; hoy la lista cerrada difiere entre kernel y ADR-004, y `04` §10 ya lo dejó señalado como POR VERIFICAR. Cierra con H-11.
- **Q12 (rutas adversariales) — PARCIAL por causa externa, no documental.** `AT-001..AT-013` y la declaración de no-cobertura de `12` §3.5 son completas; lo que impide el SÍ es **B-04** (`INCONCLUSIVE`), que ninguna prueba del Domain puede sustituir y que el propio corpus declara BLOQUEANTE para comprometerse con Cowork como host. No se cierra con edición: exige el spike.

Comprobaciones limpias, en una línea cada una: Q1, Q2, Q3, Q6, Q8, Q9 y Q10 están respondidas de forma completa y localizable, y ninguna de las cuatro enmiendas las altera. **Q11 pasa de PARCIAL a SÍ**: `11` §6.6 cierra el hueco de los mensajes que no nacen de una condición sin ampliar el catálogo cerrado de siete, y `12` §2.11 con `SC-07`/`SC-08` le da nivel de prueba. `principles.md` está íntegramente alineado con las cuatro enmiendas y no presenta ningún residuo. `03-application-use-cases.md` es el documento mejor aplicado del corpus: `05` §11.1, `06`, `09` y `12` también aplican las cuatro sin residuo detectado.