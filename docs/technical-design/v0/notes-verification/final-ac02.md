## Verificación AC-02 — aritmética de revisiones

### Comprobaciones que pasan limpias
- **(5) DDL de `case_events`** en `04-persistence-model.md` §3.5: `event_seq int NOT NULL UQ CK(event_seq >= 1)` y `case_revision int NULL` con comentario AC-02 — **correcto**.
- **(3) Rótulo de las tablas de doble columna**: `01` §4.3, `03` §0.5, `05` §12, `08` §6.1, `09` §3.1, `12` §4.2 y `13` §14.5 rotulan explícitamente el Modelo B como **VIGENTE** y el A como *anterior, superado* — **correcto**.
- **(4) Aritmética interna coherente y correcta** en `01` §4.3 (6,7 → NULL/sigue 7 → 8), `03` §0.5/§10.6/§10.9, `05` §12, `06` §1.2, `08` §6.4 (6 → NULL → 7 → 8) y `13` §14.5 (12,13 → NULL/sigue 13 → 14; `expected = 13`) — **correcto**.
- `AMENDMENT-CANDIDATES.md` rotula «Vigente (Modelo A)» dentro de un documento cuya cabecera lo declara **registro histórico**: cita histórica correcta, no residuo.

---

### HALLAZGOS

**H-01 · ALTA · `C:/Users/HITMA/Desktop/legal-workspace/docs/architecture/vertical-slice-v0.md` (tabla del happy path, líneas 130–138, y línea 152)**
Cita (fila 10): «`ReviewProposal(approve)` … `expected_case_revision` = revisión resultante de este mismo acto | `ProposalReviewed(approved)` | **7**», con fila 9 `FactsProposed` = 6. Cita (línea 152): «el Case sigue en **7** … la autorización porta `expected_case_revision = 7`; `FactsCommitted` lo deja en 8».
Problema: la columna *Rev.* sigue siendo la del Modelo A —la revisión avanza 6→7 en el acto de revisión— y contradice al párrafo que la comenta tres líneas más abajo. Toda la numeración posterior está desplazada +1 (commit 8, artifact 9, `changes_since(7)`, pasos 15–16 en 10 y 11). La celda además congela «revisión resultante de este mismo acto» (circularidad que AC-02 elimina) y `proposal_content_hash` (campo eliminado por AC-01). `09-events-and-audit.md` §7.7 lo declara literalmente pendiente: «`vertical-slice-v0.md` pasos 10–11, test F7 | **Renumerar la aritmética** — pendiente de aplicar».
Corrección: renumerar la columna con el patrón ya correcto de `01` §4.3 — fila 9 = 7 (`FactsProposed` + `ArtifactRegistered` interno), fila 10 = **NULL, el Case sigue en 7**, fila 11 = 8, fila 12 = 9 pasa a interno (AC-03), filas 15/16 = 10/11 recalculadas; sustituir la celda por «`item_content_hash` y `expected_case_revision` = la revisión contra la que se generó y se revisó la Proposal»; ajustar el cursor del paso 14 a `since_event_seq`.

**H-02 · ALTA · `.../docs/architecture/adrs/ADR-005-human-authority.md` (líneas 42, 97, 178)**
Cita (§1, l. 42): «Si `FactsProposed` deja el Case en la revisión N, `ProposalReviewed` lo deja en **N+1** (y la autorización porta N+1 como `expected_case_revision`) y `FactsCommitted` lo deja en N+2». Cita (§4, l. 97): «emite `ProposalReviewed(...)` **y avanza la CaseRevision** … porta como `expected_case_revision` la revisión resultante de ese mismo acto … El commit posterior es un acto distinto, con su propio evento y **su propia revisión**». Cita (Validación, l. 178): «en dos revisiones consecutivas del Case —si `FactsProposed` deja el Case en N, `ProposalReviewed` lo deja en N+1…».
Problema: tres afirmaciones **vigentes** del ADR enmendado contradicen la enmienda anunciada en la misma frase o el mismo párrafo. La aritmética de referencia exige N / N / N+1.
Corrección: en las tres, «`ProposalReviewed` lo deja en **N** (`case_revision` NULL; la autorización porta N) y `FactsCommitted` lo deja en **N+1**»; en §4 borrar «y avanza la CaseRevision» y «su propia revisión», y sustituir «la revisión resultante de ese mismo acto» por «la revisión contra la que se generó y se revisó la Proposal».

**H-03 · ALTA · `.../docs/architecture/adrs/ADR-004-case-memory.md` (líneas 44 y 124)**
Cita (l. 124): «El ciclo de propuesta consume **dos revisiones** … la autorización nace en ese acto y congela como `expected_case_revision` **la revisión resultante de él**». Cita (l. 44): «Texto superado: «y avanza la CaseRevision** … **`commit_reviewed_facts` … avanza la CaseRevision de nuevo**. **Son dos eventos en dos revisiones distintas**, coherente con la biyección…».
Problema: (a) l. 124 afirma como vigente lo contrario de AC-02 dentro del mismo párrafo que la invoca; (b) en l. 44 la comilla angular de «Texto superado» **nunca se cierra**, de modo que el lector no puede distinguir dónde acaba la cita histórica y la cola («dos eventos en dos revisiones distintas») se lee como norma.
Corrección: en l. 124, «El ciclo consume **una sola revisión de conocimiento** … congela la revisión contra la que se generó y se revisó la Proposal»; en l. 44 cerrar la comilla («…dos revisiones distintas.») y dejar fuera de la cita solo el texto vigente.

**H-04 · ALTA · `.../docs/domain/glossary.md` (línea 691)**
Cita: «`{… expected_case_revision: **14** …}`: la autorización porta **15**, la revisión que la profesional tenía a la vista al aprobar, **no la 14** contra la que se creó la Proposal».
Problema: el campo del ejemplo dice 14 y la prosa inmediata dice 15 y niega el 14. Es el ejemplo canónico de la aritmética de referencia y se auto-contradice; la variante «15» es Modelo A puro.
Corrección: «la autorización porta **14** — la revisión que la profesional tenía a la vista al aprobar, que es también aquella contra la que se generó y se revisó la Proposal». (Nota fuera de foco, misma cita: `operation: COMMIT_FACTS` debe ser `COMMIT_FACT` singular por AC-01.)

**H-05 · ALTA · `.../docs/domain/glossary.md` (líneas 598 y 656)**
Cita (l. 598): «…y **avanza solo `event_seq`: NO avanza la `CaseRevision`** … **Son dos eventos en dos revisiones distintas.**» Cita (l. 656): «`ReviewProposal(approve)` emite `ProposalReviewed`, **que avanza la `CaseRevision`** … la revisión que ésta congela es **la que deja ese evento** … son dos eventos en dos revisiones distintas».
Problema: dos entradas del glosario —la fuente de vocabulario del corpus— llevan titular Modelo B y cuerpo Modelo A. La l. 656 reintroduce además la definición circular de `expected_case_revision`.
Corrección: l. 598 → «Son dos eventos, pero **una sola revisión de conocimiento**»; l. 656 → «emite `ProposalReviewed`, que avanza `event_seq` y deja `case_revision` NULL; la revisión congelada es la vigente al revisar, contra la que se generó y se revisó la Proposal».

**H-06 · ALTA · `expected_case_revision` definido de dos formas incompatibles en todo el corpus**
Grupo A — «= `base_case_revision`»: `ADR-005-human-authority.md` líneas 64 (bloque de esquema), 87 y 132; `vertical-slice-v0.md` línea 150; `09-events-and-audit.md` línea 350 («la misma `FactsProposed.base_case_revision`»).
Grupo B — «la revisión vigente al revisar, posterior a `FactsProposed` (+ `ArtifactRegistered`)»: `03-application-use-cases.md` §10.6 y línea 757 («esa revisión **no** es `base_case_revision`: es `base_case_revision + 2`»); `05-mcp-contract.md` línea 625; `12-testing-strategy.md` §4.2; `13-synthetic-benchmark.md` §14.5 (`expected = 13` frente a `base = 11`); ejemplo del glosario (`expected = 14`, base = 13).
Problema: mientras `FactsProposed` y `ArtifactRegistered` avancen `case_revision` (tensión abierta, `09` §7.9), las dos lecturas **difieren en 2** y ninguna implementación puede satisfacer ambas. Es exactamente el punto de uniformidad que AC-02 debía cerrar.
Corrección: adoptar el grupo B —«la revisión vigente del Case en el momento del acto de revisión, contra la que se generó y se revisó la Proposal»— y borrar las cinco apariciones de «(= `base_case_revision`)»; si se prefiere el grupo A, hay que resolver antes `09` §7.9. Gravedad ALTA por bloquear la implementación del gate 3 del commit.

**H-07 · ALTA · `.../docs/architecture/boundaries.md` (líneas 74 y 68)**
Cita (l. 74): «**Revisiones.** `CaseRevision` monotónica por Case, con **`seq == revision`**». Cita (l. 68): «de 1 a n eventos, **avanzando la CaseRevision en n**».
Problema: `boundaries.md` es documento de arquitectura vigente y afirma sin matiz la identidad que AC-02 declara superada, además de la formulación de la biyección que ADR-001 y ADR-004 rotulan «Formulación superada». Ninguna de las dos líneas menciona AC-02.
Corrección: l. 74 → «`event_seq` monotónico por Case en todo evento; `case_revision` como subsecuencia que avanza solo en mutaciones epistémicas canónicas y es NULL en las demás (AC-02)»; l. 68 → «…de 1 a n eventos, avanzando `event_seq` en n».

**H-08 · ALTA · `.../docs/architecture/vertical-slice-v0.md` (líneas 442, 573 y 142)**
Cita (l. 442): «cada evento del Case Event Log la incrementa y **`seq == revision`** resultante». Cita (l. 573, criterio estructural 3): «con `seq` contiguos y **`seq == case_revision` reportada**». Cita (l. 142, blockquote normativo): «de 1 a n eventos del Case Event Log, **avanzando la CaseRevision en n**».
Problema: tres afirmaciones vigentes de la identidad superada, una de ellas convertida en **criterio de aceptación** del slice: un property test escrito contra ella fallaría necesariamente bajo el Modelo B (`08` §9.2 exige lo contrario: «un fixture con `event_seq = case_revision` no ejercitaría el caso que la enmienda introduce»).
Corrección: sustituir por «`event_seq` contiguos; `case_revision` subsecuencia, NULL en los eventos no canónicos» en las tres, y en el blockquote «avanzando `event_seq` en n».

**H-09 · ALTA · `.../docs/technical-design/v0/02-domain-model.md` (línea 430)**
Cita: «**Nota de aritmética de revisiones (APROBADA — enmienda AC-02).** Los dueños **aprobaron** separar `event_seq` … **No está aprobado y no se aplica.**»
Problema: negación explícita de la enmienda tres frases después de afirmarla; el residuo del texto anterior quedó dentro del párrafo reescrito. Un implementador lee «no se aplica» en un documento normativo.
Corrección: borrar «**No está aprobado y no se aplica.**» y dejar «El modelo de dominio es **invariante bajo ambos modelos**…» (la línea 769 del mismo archivo ya está bien redactada).

**H-10 · MEDIA · `.../docs/architecture/adrs/ADR-001-trust-boundary.md` (línea 51, invariante 2)**
Cita: «…**ENMIENDA AC-02 aprobada** … `case_revision` es una **subsecuencia** … Sobre esa base: cada mutación … produce exactamente un evento … con el `Principal` …, su `provenance_kind` y **`seq == CaseRevision` resultante**».
Problema: el mismo invariante enuncia la enmienda y, en su cláusula final, la identidad superada. Al ser ADR `Accepted` de nivel 1, el residuo gana por precedencia frente a los documentos técnicos.
Corrección: «…su `provenance_kind` y su `event_seq`, con `case_revision` resultante cuando el evento muta el estado epistémico canónico y NULL en los demás».

**H-11 · MEDIA · `.../docs/technical-design/v0/13-synthetic-benchmark.md` (línea 858, y cola de la línea 672)**
Cita (l. 858): «| Valor de `expected_case_revision` (13 vs 14) | **INCONCLUSIVE** | Ambigüedad entre kernel §5.2 y §7 (§14.5). El fixture la expone; no la resuelve. **POR VERIFICAR con los dueños** |». Cita (l. 672): «Texto histórico: «…la corrida revela cuál implementa el Core». **POR VERIFICAR con los dueños**».
Problema: la tabla de resultados del benchmark declara abierta una cuestión que §14.5 del mismo documento y `12` §4.2 cierran con AC-02 (`expected = 13`, y 14 es el valor del modelo superado). Un `POR VERIFICAR` vigente sobre una decisión aprobada reabre la ambigüedad justo donde se codifica el fixture.
Corrección: l. 858 → «**RESUELTO por AC-02**: `expected_case_revision = 13`; 14 es el valor del Modelo A superado. Residuo abierto distinto: la granularidad de `ProposeFacts` (§7.9 de `09`)»; en l. 672 eliminar el «POR VERIFICAR con los dueños» que arrastra el texto histórico y conservar solo el relativo a `ArtifactRegistered`.

**H-12 · MEDIA · `.../docs/technical-design/v0/09-events-and-audit.md` (líneas 846, 884–885) y `.../docs/architecture/adrs/ADR-009-event-and-audit-strategy.md` (línea 207)**
Cita (`09`, l. 846): «`03-application-use-cases.md` §10.10, §11.6, §0.7 | Deben quedar con los valores del Modelo B — **normalización pendiente en ese documento**». Cita (`09`, l. 884–885): «`01-system-design.md` … / `03-application-use-cases.md` … | **POR VERIFICAR: si ya se normalizó**». Cita (`ADR-009`, l. 207): «**POR VERIFICAR:** el estado de `01`, `03`, `06` y `vertical-slice-v0.md`».
Problema: tablas de seguimiento obsoletas. `01` §4.2–§4.3/§9.2, `03` §0.5/§0.7/§10.6/§10.9/§10.10/§13.1 y `06` §1.2 **sí** están normalizados (verificado); mantenerlos como pendientes hace dudar de documentos correctos y diluye el único pendiente real, que es `vertical-slice-v0.md` (H-01).
Corrección: marcar `01`, `03` y `06` como **normalizados** en las tres tablas y dejar `vertical-slice-v0.md` como el único «pendiente de renumerar», con puntero a los pasos 9–17 y a los criterios estructurales 3 y F13.