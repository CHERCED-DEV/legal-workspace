## OWNERSHIP DRIFT y REVISION DRIFT — 15 hallazgos

### ALTA

**1. `00-technical-kernel.md` §7, §8.1 y §9 aplican el Modelo B que §5.2 declara no aplicable**
Cita: §5.2 «**No se aplica hasta que los dueños aprueben el amendment.**» Pero §7, fila `ReviewProposal`: «¿Avanza `case_revision`? **no** (§5.2)»; §8.1 contrata `event_seq monotónico por caso, TODOS los eventos` + `case_revision … NULL si el evento no muta estado canónico`; §9 añade `event_seq` al `CaseContextResponse`. Bajo el modelo vigente (ADR-004 (c): «cada evento la incrementa y `seq == revision` resultante») no existe `event_seq` distinto ni `case_revision` nula.
Problema: el documento normativo de nivel 2 **ya aplica** en tres contratos la enmienda que él mismo declara no aprobada, contra ADR-004/ADR-005 Accepted (nivel 1, kernel §14). Es la raíz de todo el drift del corpus.
Corrección: revertir §7 fila `ReviewProposal` a «sí (ADR-004 (b)1, ADR-005 §1)», reescribir §8.1 con `seq == case_revision` y mover `event_seq`/`case_revision NULL` a §5.2 como parte del candidato; o —alternativa— elevar §5.2 a decisión aprobada por los dueños antes de que ningún documento la use. No hay tercera opción coherente.
Gravedad: **ALTA**

**2. `03-application-use-cases.md` especifica el Modelo B como norma, no como candidato**
Citas: §0.5 tabla, fila `ProposalReviewed` → «**0** (Modelo B, §12.1)»; §10.9 «`event_seq` avanza; `case_revision` **no** (Modelo B)»; §10.10 «**No avanza** (kernel §7, §5.2)»; §10.6 «`expected_case_revision` — precisión obligatoria **bajo el Modelo B**»; §13.1 «Este documento aplica el kernel §7».
Problema: es el único documento que **adopta** el modelo no aprobado como especificación de sus use cases. Declara el conflicto (mérito real, §13.1), pero declarar no es lo mismo que no aplicar: sus postcondiciones, su cursor de delta y su aritmética son inejecutables bajo ADR-004/005 Accepted.
Corrección: convertir §0.5, §10.6, §10.9 y §10.10 al formato de doble columna que ya usa `09-events-and-audit.md` §3.1 («`case_revision` Modelo A | Modelo B»), dejando el Modelo A como valor vigente y el B como columna candidata. §0.7 (cursor por `event_seq`) puede conservarse tal cual: es correcto bajo ambos.
Gravedad: **ALTA**

**3. `ProposalPreservedForReconciliation`: cuatro lecturas incompatibles de si el rechazo muta el Case**
- `03` §0.5: evento existente, `case_revision` = **0**.
- `05` §12: «el rechazo por `REVISION_MISMATCH` emite `ProposalPreservedForReconciliation`, que es mutación y por tanto **avanza `case_revision`**».
- `06` §5.4: hipótesis de trabajo = **sin productor en v0**, es decir no se emite.
- `09` §3.1 fila 10: doble columna +1/0 «**o sin productor**, §8.2».
Problema: cuatro documentos de la misma iteración discrepan sobre si un commit rechazado produce evento y mueve el reloj. Afecta directamente a ADR-005 inv. 6 («cero mutaciones») y a la biyección de ADR-004 inv. 5.
Corrección: resolver como DECISIÓN de los dueños (ADR-009 pendiente 3) y, hasta entonces, imponer una sola formulación en los cuatro: la opción 1 de `06` §5.4 (conservarlo en la lista cerrada de ADR-004, declarado **sin productor en v0**, patrón `FactWithdrawn`) es la única compatible con «cero mutaciones». Requiere corregir `03` §0.5 (retirar la fila), `05` §12 (retirar la afirmación de que se emite) y la lista del kernel §8.1.
Gravedad: **ALTA**

**4. `06-human-authorization.md` §10, invariantes 7 y 8 — lógica de dominio sobre entidad de Application**
Citas: «| 7 | La identidad del item es opaca y no posicional… | **Domain/Application** |» y «| 8 | `commit_state` avanza solo desde `review_decision = APPROVED` efectivo | **Domain (transición)** |».
Problema: `ProposalItem`, `review_decision` y `commit_state` son de **Application** (addendum v0.3 B.4; `02` §4; ADR-008 «`Proposal` es un concepto de soporte de Application»). Imponer esa transición en el Domain exigiría que `domain` importe `application`, arista prohibida por `01` §2.3 y por la matriz verificable de `12` §7.1 (`domain` → «nada del sistema»). El test de arquitectura de `12` §7 fallaría contra la especificación.
Corrección: cambiar el locus de ambas filas a **Application**; el `CK( commit_state = 'COMMITTED' => review_decision = 'APPROVED' … )` de `04` §3.4 se mantiene como cinturón mecánico, conforme a `04` §4 cláusula 15. Nota adicional: hoy el mismo invariante tiene tres loci distintos en el corpus (`06` Domain, `04` SQL, `12` §6.2 INV-H-08 vía `FT-008.b` funcional); unificar en Application + CHECK redundante.
Gravedad: **ALTA**

**5. `12-testing-strategy.md` INV-H-14 es inejecutable contra su propio `AT-008`**
Citas: §6.2 «INV-H-14 rechazo ⇒ cero mutaciones y cero eventos | `assertNoEffect` en **los trece `AT`**»; §3.1 `AT-008` exige «la propuesta **se preserva**… visible en `get_case_context(pending)`»; `03` §10.7 persiste `preserved_for_reconciliation` como el único dato de estado almacenado de la Proposal.
Problema: `assertNoEffect` aplicado a `AT-008` contradice la postcondición del propio `AT-008`. `12` §8 (línea 888) reconoce la ambigüedad pero INV-H-14 sigue redactado en absoluto.
Corrección: acotar INV-H-14 a «cero mutaciones **del estado epistémico canónico** y cero eventos canónicos», y excluir explícitamente `AT-008` del `assertNoEffect` genérico o declarar la preservación como estado de Application no canónico. Depende del hallazgo 3.
Gravedad: **ALTA**

### MEDIA

**6. `10-artifact-lifecycle.md` §10, invariantes 10 y 16 — locus Domain sobre `Artifact`**
Citas: «| 10 | La vigencia es derivada… | **Domain/Application** |» y «| 16 | `created_by` del artifact hereda el `Principal`… | **Domain (regla de combinación)** |», frente a §1 del mismo documento: «Pertenece al plano **Application**, no al Domain».
Problema: contradicción interna; ninguna regla cuyo sujeto es `Artifact` puede imponerse en el Domain sin romper la regla de dependencias.
Corrección: fila 10 → «Application (cómputo) + Infrastructure (ausencia de columna)»; fila 16 → «Application (construcción del Artifact), reutilizando la matriz `Principal` × `provenance_kind` del kernel §1.4 como función pura del Domain sin conocer `Artifact`».
Gravedad: **MEDIA**

**7. `11-ux-condition-catalog.md` §7.1 introduce dos loci fuera del mapa de capas**
Cita: filas con «Dónde se aplica: **Presentation**» (INV-UX-04, 05, 11, 12) y «**Configuration**» (INV-UX-08).
Problema: ni `Presentation` ni `Configuration` figuran en la matriz de dependencias de `01` §2.3 ni en el mapa `architecture-layers` de `12` §7.1 (`domain, application, ports, infrastructure, mcp, plugin`). Peor: `01` §2.3 fija que `plugin/skills` puede importar «nada del Core», mientras el diagrama de `01` §3 dibuja `legal-plugin/presentation -.->|"lee condiciones tipadas"| APP`. Esa arista no está en `allowed_edges` de `12` §7.1, de modo que el test de arquitectura o la prohíbe o —si la fila `plugin/skills` no cubre `plugin/presentation`— deja la capa sin control.
Corrección: añadir en `01` §2.3 y en `12` §7.1 una fila propia `plugin/presentation` con la arista permitida `plugin/presentation → application_contracts` (solo tipos de `Condition`), y mapear `Configuration` a una raíz declarada (composición/arranque, `06` inv. 12).
Gravedad: **MEDIA**

**8. `08-case-context-projections.md` línea ~712 aplica el Modelo B en un campo del contrato**
Cita: `case_revision: CaseRevision | null;   // null si el evento no mutó estado canónico (kernel §5.2)`.
Problema: el documento declara en §6.1 que «**Bajo el Modelo A** (vigente mientras no se apruebe el amendment…)» y adopta el cursor por `event_seq` porque «es correcto bajo ambos»; pero este campo solo es admisible bajo el Modelo B — bajo el A nunca es nulo. El resto del documento usa doble lectura; este punto no.
Corrección: anotar el campo como «`null` **solo si se aprueba** el amendment del kernel §5.2; bajo el Modelo A vigente nunca es nulo», igual que `04` §10 C3 hace con la columna homóloga.
Gravedad: **MEDIA**

**9. `ADR-009` — el censo de la divergencia está incompleto**
Cita (Contexto): «`01-system-design.md` aplica el Modelo A por precedencia…; `03-application-use-cases.md` aplica el Modelo B…; `04-persistence-model.md` y `09-events-and-audit.md` se mantienen neutrales».
Problema: omite `05-mcp-contract.md` §12 y `06-human-authorization.md` §1.2 (ambos Modelo A explícito), `08` §6.1 (neutral en el diseño pero Modelo B en un campo, ver hallazgo 8), `11` §5, `12` §4.2/§6, `13` §14.5 y `ADR-008` pendiente 1 (neutral declarado). El riesgo registrado («dos aritméticas simultáneas») subestima el alcance.
Corrección: sustituir el censo por la lista completa con la postura de cada documento, y añadir el kernel §7/§8.1/§9 como aplicador del Modelo B (hallazgo 1) — que hoy el ADR solo menciona de pasada en la pendiente 1.
Gravedad: **MEDIA**

**10. `00-technical-kernel.md` §7 — `ProposeFacts` «sí» avanza `case_revision`, sin decir cuánto ni por qué**
Problema: la fila agrupa `FactsProposed` + `ArtifactRegistered` bajo un único «sí». `03` §10.6 y `05` §propose_facts lo leen como **+2**; `13` §14.5 lo demuestra en el libro de eventos. Y el criterio del propio §5.2 («solo eventos que mutan el estado epistémico canónico») implicaría que una propuesta **no** debería avanzarlo — la misma razón por la que saca a `ProposalReviewed`. El resultado es que `expected_case_revision` vale 13 o 14 según el documento (`12` §4.3 lo declara `INCONCLUSIVE`).
Corrección: desdoblar la fila §7 en `FactsProposed` y `ArtifactRegistered` con su valor cada una, y resolver junto con la pendiente 2 de ADR-009 si ambos avanzan `case_revision`.
Gravedad: **MEDIA**

**11. `05-mcp-contract.md` §12 afirma como vigente algo que ningún otro documento sostiene**
Cita: «Bajo el modelo vigente, el rechazo por `REVISION_MISMATCH` emite `ProposalPreservedForReconciliation`, que es mutación y por tanto **avanza `case_revision`**».
Problema: presentado como hecho del modelo vigente para fundamentar un «argumento adicional a favor del amendment», cuando `06` §5.4 sostiene lo contrario y `09` §3.1 lo deja abierto. Un argumento a favor del candidato apoyado en una premisa no acordada.
Corrección: reformular como condicional («**si** el evento se conserva con productor, entonces…»), remitiendo a la DECISIÓN PENDIENTE del hallazgo 3.
Gravedad: **MEDIA**

**12. `08-case-context-projections.md` §5 — proyecciones especificadas en SQL sin capa ni puerto asignados**
Cita: bloques «**Consultas que lo alimentan.**» con `SELECT` sobre las tablas de `04` §3; §... aclara que es «pseudocódigo conceptual», pero el documento nunca nombra `CaseStorePort` ni dice qué capa ejecuta esas consultas (las únicas menciones a «puerto» son negativas: «no existe puerto que acepte una proyección como entrada»).
Problema: `01` §2.2 sitúa las proyecciones en `application/`, que tiene prohibido importar `infrastructure`. Sin decir que las consultas viven detrás del puerto, el documento deja abierta la lectura de que Application conoce el esquema físico.
Corrección: añadir una línea en §1 o §5: «las consultas se ejecutan **detrás de `CaseStorePort`**; Application consume el resultado tipado y no conoce el DDL».
Gravedad: **MEDIA**

### BAJA

**13. `01-system-design.md` §2.2 y §3 — la lista de Application está incompleta**
Cita: «conceptos de soporte (Artifact · Proposal · HumanAuthorization · CaseRevision)», idéntica en el nodo `APP` del Mermaid.
Problema: faltan `ProposalItem` (kernel §2.1) y `ProposalItemReview` (kernel §3.4), que son precisamente las entidades sobre las que `06` §10 desliza el locus al Domain (hallazgo 4). Una lista incompleta invita a la ambigüedad.
Corrección: añadir ambos en §2.2 y en el nodo `APP`.
Gravedad: **BAJA**

**14. `04-persistence-model.md` §3.1 — dos contadores materializados sin nota de equivalencia**
Cita: `current_revision int NOT NULL CK(current_revision >= 0)` y `current_event_seq int NOT NULL CK(current_event_seq >= 0)`.
Problema: §10 C3 declara neutralidad y explica que bajo el Modelo A «`case_revision = event_seq` en **todas** las filas» — pero eso se dice de `case_events`, no de estas dos columnas de `cases`, que bajo el Modelo A deben ser idénticas y no llevan `CHECK` ni nota. Dos columnas que deben coincidir y nadie comprueba son una divergencia esperando ocurrir.
Corrección: anotar en §3.1 «bajo el Modelo A vigente `current_event_seq == current_revision`; el `CHECK` no se añade para no fijar un modelo (§10 C3)», o añadir el invariante a la lista de §4.
Gravedad: **BAJA**

**15. `02-domain-model.md` §4 remite el contrato de `Artifact` y `CaseRevision` a un documento de nivel inferior**
Cita: «Sus contratos completos están en el kernel §2…, §3…, `boundaries.md` §3 (`Artifact`, `CaseRevision`) y ADR-004/ADR-005».
Problema: `boundaries.md` es nivel 3 (kernel §14) y el contrato completo de `Artifact` vive hoy en `10-artifact-lifecycle.md` (nivel 2). Remitir hacia abajo invierte la precedencia y deja el puntero obsoleto.
Corrección: sustituir la referencia por `10-artifact-lifecycle.md` §2–§3 para `Artifact` y por ADR-004 (c) + `09` §2.2 para `CaseRevision`. (Verificado: `boundaries.md` §4 y su Mermaid §9.4 **sí** están corregidos conforme al addendum B.4 — los cuatro conceptos están en `APP`; no hay drift ahí.)
Gravedad: **BAJA**

---

### Categorías sin hallazgos

- **Ownership limpio y explícito** en: `02-domain-model.md` (§3.1 `Case.current_revision` marcada «ADMINISTRADA por Application», §4 «Conceptos de Application que el Domain toca sin redefinirlos»), `04-persistence-model.md` §4 cláusula 3 («ningún trigger contiene lógica jurídica»; solo `RAISE(ABORT)` incondicional), `07-provenance-and-locators.md` §... tabla INV-L, `ADR-008` (línea 180, `Proposal` es Application), `ADR-010` («la clase se aplica en **Application**, nunca en el protocolo»), `ADR-011` (rechaza promover `EvidenceFragment` a entidad).
- **Ningún documento pone lógica de dominio en el MCP.** `05` R4 y `ADR-010` §5 limitan el adapter a validación sintáctica; `10` §8.2 lo dice explícitamente («el gate no vive… en el adapter MCP, que traduce y valida sintaxis, no decide política»).
- **Revision drift correctamente tratado, sin hallazgo,** en: `09-events-and-audit.md` (§0 «este documento **no aplica ninguno de los dos modelos**» + §3.1 doble columna — es el modelo a imitar), `04-persistence-model.md` §10 C3, `13-synthetic-benchmark.md` §14.5 («el fixture no elige»), `10-artifact-lifecycle.md` §... («`base_case_revision` es estable frente al amendment»), `ADR-008` pendiente 1 («Este ADR es **neutral**… No se aplica el amendment aquí»), `02-domain-model.md` §4 («**No está aprobado y no se aplica**»).

**Nota de corpus:** apareció durante la revisión un archivo no incluido en la lista de encargo, `C:\Users\HITMA\Desktop\legal-workspace\docs\technical-design\v0\15-product-floor-proposal.md` (creado a las 20:31, en escritura concurrente). No fue revisado. Tampoco existe `14-*`.