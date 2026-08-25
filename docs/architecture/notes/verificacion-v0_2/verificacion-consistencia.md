# HALLAZGOS — verificación de consistencia cruzada (kernel v0.2 + 10 documentos)

Formato: `archivo` · sección/cita · problema · corrección sugerida. Ordenados por gravedad. **No se reescribió ningún documento.**

---

## Bloqueantes / alta gravedad

### 1. `actor_type = HUMAN` no existe en el enum canónico (`HUMAN_DECISION`)
- **Archivos:** `C:\Users\HITMA\Desktop\legal-workspace\docs\architecture\adrs\ADR-005-human-authority.md` (§2 del contrato e invariante 1: «`actor_id, actor_type=HUMAN, actor_role`» y «`actor_type = HUMAN` es obligatorio en el registro (kernel §3, ADR-003)»); `docs\domain\glossary.md` §12 (bloque de contrato, lifecycle e invariante 1); `docs\architecture\vertical-slice-v0.md` (Persisted state: «`actor_id, actor_type = HUMAN, actor_role`»).
- **Problema:** el enum cerrado de `ProvenanceRecord` es `EXTERNAL_SOURCE | AI_DERIVATION | AI_INFERENCE | HUMAN_DECISION | SYSTEM` (kernel §2; ADR-003 Decisión e inv. 1; glosario §7; boundaries §4; principles §8). `HUMAN` no es un valor válido y ADR-005 lo justifica citando precisamente kernel §3/ADR-003, que dicen lo contrario. El conflicto nace en el kernel (§5 vs §2) y **ningún documento lo señala**, pese a que el kernel exige señalarlo en lugar de resolverlo por cuenta propia. Con validación por schema, una HumanAuthorization v0 sería inconstruible o exigiría un segundo enum paralelo.
- **Corrección:** en los tres documentos, escribir `actor_type = HUMAN_DECISION` y añadir una nota «Refinamiento a señalar: el kernel §5 escribe `HUMAN`; se normaliza al enum canónico del kernel §2/§3 — cambio de nombre, no de semántica», y devolver el punto al dueño del kernel para registrar la normalización en §16 (nuevo ítem 7). Alternativa mínima si no se quiere tocar el valor: nota explícita en los tres archivos declarando que `HUMAN` es un alias pendiente de resolución (DECISIÓN PENDIENTE), nunca dejarlo silencioso.

### 2. Momento de emisión de `ProposalReviewed`: ADR-005 contradice al slice y al glosario
- **Archivos:** `docs\architecture\adrs\ADR-005-human-authority.md` §3 («Si todo coincide: ejecuta, marca `consumed_at` y emite `ProposalReviewed` y `FactsCommitted` en el Case Event Log») vs `docs\architecture\vertical-slice-v0.md` happy path paso 10 (`ReviewProposal(approve)` → evento `ProposalReviewed(approved)`, rev 7) y `docs\domain\glossary.md` §11 Lifecycle (`--ReviewProposal(approve)--> APPROVED [ProposalReviewed]`).
- **Problema:** dos documentos emiten el evento en el acto de revisión y uno en el instante del commit. No es cosmético: si la revisión emite evento, incrementa `CaseRevision`, y entonces el `expected_case_revision` grabado en la autorización **no puede** ser la revisión contra la que se creó la Proposal. El slice lo señala («la diferencia es de momento de emisión, no de contenido») pero la afirmación es incorrecta: cambia la aritmética de revisiones y el criterio de coincidencia del commit.
- **Corrección:** fijar un solo momento (recomendado: el del slice y el glosario — el acto de revisión produce `ProposalReviewed`, el commit produce `FactsCommitted`) y corregir ADR-005 §3 para que describa dos eventos en dos momentos; sustituir en `vertical-slice-v0.md` la nota conciliatoria por el enunciado de la regla ya unificada. Si la elección corresponde a los dueños, marcarlo **DECISIÓN PENDIENTE** idéntica en los tres archivos, no como diferencia inocua.

### 3. `expected_case_revision` con valores incompatibles entre el ejemplo del glosario y el flujo del slice
- **Archivos:** `docs\domain\glossary.md` §12 Ejemplo («`AUTH-9 {proposal_id: P-3, proposal_content_hash: H1, … expected_case_revision: 14 …}`», con `P-3` creada contra la revisión 14) y §10 Ejemplo; vs `docs\architecture\vertical-slice-v0.md` paso 10 («`expected_case_revision` = revisión resultante de este mismo acto»).
- **Problema:** bajo el modelo del slice, `FactsProposed` deja el Case en 14 y `ProposalReviewed` lo deja en 15; la autorización debería portar 15. Con 14, el commit del ejemplo feliz del glosario fallaría siempre con `REVISION_CHANGED` contra su propia revisión de revisión.
- **Corrección:** una vez resuelto el hallazgo 2, recalcular los ejemplos del glosario §10 y §12 (y verificar la coherencia numérica con `docs\architecture\vertical-slice-v0.md` *Revision behavior*, rev 41/42), o declarar explícitamente en el glosario que `expected_case_revision` es la revisión **al momento de aprobar**, no la de creación de la Proposal.

### 4. «n mutaciones == n eventos» está definido de tres formas incompatibles
- **Archivos:** `docs\architecture\adrs\ADR-004-case-memory.md` inv. 5 («Toda mutación commiteada produce exactamente un evento … (n mutaciones == n eventos)»); `docs\architecture\adrs\ADR-001-trust-boundary.md` inv. 2; `docs\architecture\boundaries.md` §3 Use cases; `docs\architecture\principles.md` principio 2 («property test de correlación n mutaciones commiteadas ⇔ n eventos»); vs `docs\architecture\vertical-slice-v0.md` («un COMMAND puede producir más de un evento y avanzar la revisión más de una unidad», pasos 15–16).
- **Problema:** el slice reinterpreta «mutación» como *cambio de estado registrado* para poder emitir `EvidenceIncorporated` + `ArtifactMarkedStale` en una sola invocación, pero los otros cuatro documentos formulan el invariante sobre «mutación commiteada» sin definirla, y el property test (criterio de aceptación B3/F13) resulta ambiguo. La misma ambigüedad reaparece en `ReviewProposal` (cambia `Proposal.status` **y** crea una `HumanAuthorization` con un solo evento) y en el commit (N Facts + N EvidenceLinks + `consumed_at` con un solo `FactsCommitted`).
- **Corrección:** llevar la definición operativa («mutación = cambio de estado registrado, no invocación de tool; una invocación puede producir 1..n eventos y avanzar la revisión en n») al texto de ADR-004 inv. 5 como definición normativa, y referenciarla desde ADR-001 inv. 2, boundaries §3 y principles §2. El slice debe entonces citar la definición, no proponerla.

### 5. `DETERMINED` es transición almacenada pero no tiene evento ni use case en ningún documento
- **Archivos:** `docs\architecture\notes\kernel-consolidacion-v0_2.md` §3 y §6 (lista cerrada de eventos: `…FactsCommitted, FactWithdrawn…`, sin evento de determinación); `docs\architecture\adrs\ADR-004-case-memory.md` Relaciones («cada transición almacenada de `status_history` se materializa como evento del Case Event Log (`FactsCommitted`, `FactWithdrawn`)»); `docs\architecture\boundaries.md` §3 (lista de use cases sin ninguno para `ProfessionalDetermination`); `docs\architecture\adrs\ADR-003-epistemic-domain-model.md` Validación #1 (exige el escenario t1–t6 **completo**, cuyo t5 registra `D-4` → `DETERMINED`).
- **Problema:** ADR-003 declara `DETERMINED` como transición almacenada y la hace criterio de aceptación; el slice la excluye («ninguna tool de la superficie v0 la habilita»); pero además **no existe canal alguno** (ni tool, ni use case del canal humano, ni evento en la lista cerrada) por el que pudiera registrarse. Como la lista de eventos es cerrada, hoy es imposible cumplir el test de aceptación de ADR-003 sin cambiar el contrato.
- **Corrección:** o (a) ADR-003 reclasifica su escenario t1–t6 como **ilustrativo** y traslada el test de aceptación a post-slice, o (b) se registra explícitamente como **DECISIÓN PENDIENTE** compartida (ADR-003 + ADR-004 + boundaries §3 + kernel §6) que la lista cerrada de eventos v0 y la lista de use cases carecen de entrada para `ProfessionalDetermination`/`FactWithdrawn`. En cualquier caso, `boundaries.md` §3 debe decir qué use case produce `FactWithdrawn`, que sí está en la lista cerrada y hoy tampoco tiene dueño.

---

## Media gravedad

### 6. Falta en el slice el test adversarial de ids inventados / rutas arbitrarias, exigido por tres ADRs
- **Archivos:** `docs\architecture\vertical-slice-v0.md` *Test matrix* («los 10 aprobados» y criterio B7: «Los 10 tests negativos pasan…») vs `docs\architecture\adrs\ADR-001-trust-boundary.md` Validación #4, `docs\architecture\adrs\ADR-002-protected-local-case-store.md` Validación #4 («Rechazo de rutas … incluir path traversal (`..`, rutas absolutas, symlinks/junctions de Windows)») y `docs\architecture\adrs\ADR-006-evidence-incorporation-boundary.md` Validación #6.
- **Problema:** el invariante 7 de ADR-001 («Ids opacos emitidos por el Core») no tiene ninguna fila en la matriz del slice —ni en los 10 adversariales ni en F1–F17—, pese a que el slice se presenta como la matriz consolidada y `principles.md` principio 2 lo declara verificable.
- **Corrección:** añadir una fila a la matriz adversarial del slice: «Inventar identificadores plausibles / pasar ruta de filesystem a `ingest_evidence` (incluido path traversal) → rechazo con código semántico estable (ADR-001 inv. 7; ADR-002 val. 4; ADR-006 val. 6)». Si los «10 aprobados» son una lista cerrada por los dueños, dejarla intacta y añadir el caso como `F18` funcional-negativo, señalando la procedencia.

### 7. La matriz de trazabilidad por invariante que ADR-003 delega al slice no existe
- **Archivos:** `docs\architecture\adrs\ADR-003-epistemic-domain-model.md` Validación #6 («**matriz de trazabilidad**: cada invariante de este ADR mapeado a su test negativo y a la condición emitida, en el documento del vertical slice») vs `docs\architecture\vertical-slice-v0.md` *Test matrix*.
- **Problema:** los invariantes 3 (property test de `status_history`), 4 (determinación sin motivación/links ⇒ rechazo), 5 (determinar no retira `CONTRADICTS`) y 8 (inmutabilidad de Statement) de ADR-003 no tienen fila en el slice. El slice cubre 1, 2, 6, 7, 9, 10 vía F12/adversariales 1, 3, 7.
- **Corrección:** añadir en el slice una tabla «invariante ADR-00X → test → condición» (aunque varias filas queden marcadas *fuera del slice, post-slice*), o corregir ADR-003 Validación #6 para que delegue solo los invariantes efectivamente ejercitados en v0.

### 8. Hueco semántico: un Fact con solo links `CONTEXTUALIZES` activos no cae en ningún estado derivado
- **Archivos:** definición idéntica en `docs\architecture\notes\kernel-consolidacion-v0_2.md` §3, `docs\architecture\adrs\ADR-003-epistemic-domain-model.md` («`UNSUPPORTED` (0 links activos)»), `docs\domain\glossary.md` §5 y §6 («Cuando todos los links de un Fact pasan a `RETIRED`, el Fact vuelve a computarse como `UNSUPPORTED`»), `docs\architecture\vertical-slice-v0.md` *Derived state* y F12.
- **Problema:** los cuatro documentos son mutuamente consistentes, pero la definición deja un caso sin cubrir: con ≥1 link `CONTEXTUALIZES` `ACTIVE` y ningún `SUPPORTS`/`CONTRADICTS`, el Fact no es `SUPPORTED`, ni `CONTRADICTED`, ni `UNSUPPORTED` (no tiene 0 links activos). La proyección `facts` no sabría qué mostrar y F12 no lo prueba.
- **Corrección:** no resolverlo unilateralmente: señalarlo como **DECISIÓN PENDIENTE** en ADR-003 y glosario §5/§6 («¿`UNSUPPORTED` se define como *0 links de polaridad probatoria activos* o como *0 links activos*?»), y añadir el caso a F12. Es exactamente el tipo de refinamiento que el kernel pide señalar, no inventar.

### 9. `OPERATION_NOT_PERMITTED` se usa para operaciones que no existen en la superficie, contra su semántica del kernel
- **Archivos:** `docs\architecture\vertical-slice-v0.md` *Negative paths* («Operación inexistente en la superficie … | La operación no existe; **no hay nada que rechazar** … | `OPERATION_NOT_PERMITTED`»), Test matrix filas 1, 4 y 9; vs `docs\architecture\notes\kernel-consolidacion-v0_2.md` §9 («Capacidad no disponible **para el principal/perfil** o vetada por política») y `docs\architecture\principles.md` principio 15 («tests de perfil que deben producir `OPERATION_NOT_PERMITTED`»).
- **Problema:** dos lecturas incompatibles. Si la tool no existe en el manifiesto, el MCP devuelve *tool desconocida*, no una condición tipada del Core; el propio slice lo admite («no hay camino») y aun así exige la condición. Además `ADR-006` (Preguntas pendientes) razona lo contrario: «`OPERATION_NOT_PERMITTED` es de política, no de este caso».
- **Corrección:** precisar en el slice y en el kernel §9 si el código cubre también «capacidad inexistente en esta versión del producto» (y entonces quién la emite: el driving adapter con condición tipada) o solo veto por política/perfil; en el segundo caso, sustituir la condición por «error semántico estable» en las filas 1 (`DETERMINED`), 4 (modificar Source) y 9 (verificar fuente) y en *Negative paths*.

### 10. `Statement` declarado opcional en el slice, obligatorio en el ejemplo canónico de ADR-003 y del glosario
- **Archivos:** `docs\architecture\vertical-slice-v0.md` *Domain entities exercised* («**SUPUESTO del slice:** … el slice puede completarse sin materializar Statements») y criterio A6 (cadena «Fact → EvidenceLink → fragmento → DerivedRepresentation → Source», sin Statement) vs `docs\architecture\adrs\ADR-003-epistemic-domain-model.md` t1 (`ST-9` como primer eslabón) y `docs\domain\glossary.md` §4 y §5 t1 (`ST-9`).
- **Problema:** el escenario de aceptación de ADR-003 y el ejemplo del glosario arrancan en un Statement que el slice puede no producir; el happy path del slice no tiene ningún paso que cree Statements. Queda sin definir quién ejercita el invariante 8 de ADR-003 y la entrada 4 del glosario.
- **Corrección:** o el slice añade un paso explícito de extracción de Statements (coherente con `AI_DERIVATION` y con la propiedad 6 del §34), o ADR-003 y el glosario marcan sus ejemplos t1 como **ilustrativos, no ejercitados en v0**, y el slice declara qué invariantes de Statement quedan sin verificar.

### 11. Terminología divergente: «Content Pack» (boundaries) vs «Knowledge Pack» (kernel, glosario, slice)
- **Archivos:** `docs\architecture\boundaries.md` §8 («## 8. Content Packs — contrato v0», §2.1 «gestión de Content Packs», §10 tabla de ciclos) vs `docs\architecture\notes\kernel-consolidacion-v0_2.md` §11 y §10 (`knowledge_pack_versions[]`), `docs\domain\glossary.md` §9 («dependa de un **Knowledge Pack**»), `docs\architecture\vertical-slice-v0.md` (Scope: «Knowledge Packs | Ninguno cargado»).
- **Problema:** `boundaries.md` introduce un renombre canónico («bajo el nombre "Knowledge Pack" convivían tres naturalezas…») que ningún otro documento adopta, y conserva a la vez el campo `knowledge_pack_versions[]`, con lo que el mismo concepto tiene dos nombres y el campo apunta al nombre viejo. El renombre no está registrado como supersede en kernel §16 (a diferencia de `Document/original → Source`, que sí lo está).
- **Corrección:** decidir un nombre único y registrarlo como supersede en el kernel §16 (nuevo ítem), propagarlo a glosario §9, slice (Scope y no-goals) y a la anotación del campo; si se conserva `knowledge_pack_versions[]` por compatibilidad, decirlo explícitamente en los tres archivos («nombre del campo conservado; el concepto se llama X»).

### 12. Asignación de plano contradictoria para `Artifact`, `Proposal` y `HumanAuthorization`
- **Archivos:** `docs\domain\glossary.md` *Mapa de los trece términos* (`Artifact` → **Application**; `Proposal` → Application (soporte); `HumanAuthorization` → Application (soporte); `CaseRevision` → Application/Domain) vs `docs\architecture\boundaries.md` §4 Domain («Entidades canónicas (kernel §2), sin más: `Case, Source, … Artifact, CaseRevision, Proposal, HumanAuthorization, DerivedRepresentation`») y su diagrama §9.4, cuyo nodo DOMAIN incluye `Proposal`, `HumanAuthorization` y `Artifact`.
- **Problema:** el mismo término está en Domain en un documento y en Application en otro; el glosario incluso afirma «Artifact ≠ entidad jurídica del dominio. Es un registro de trabajo del plano Application». Afecta a dónde viven los invariantes.
- **Corrección:** unificar. Sugerencia mínima invasiva: `boundaries.md` §4 mantiene la lista de vocabulario canónico pero anota el plano de cada término conforme al glosario (o el glosario ajusta su columna «Plano»); el diagrama §9.4 debe reflejar la misma partición.

### 13. `boundaries.md` afirma como hecho el contexto B, que el resto de documentos declara no levantado
- **Archivo:** `docs\architecture\boundaries.md` §7 («**La primera usuaria opera ambos contextos** (parte/litigante y autoridad/decisor), de modo que anclar `role` a la organización sería incorrecto desde el primer día»), sin etiqueta.
- **Problema:** `docs\domain\glossary.md` §3 lo formula como **Pregunta de negocio** abierta («si una misma instalación atenderá asuntos de contextos distintos…»), §8 dice «**Contexto B (`DECLARED_PROVEN`): NO TENEMOS INFORMACIÓN SUFICIENTE**. El trabajo real del rol decisor no está levantado», y ADR-003 (Preguntas #1) lo deja pendiente. `boundaries.md` construye un refinamiento de arquitectura (anclaje del rol por Case) sobre una premisa que los demás tratan como no verificada.
- **Corrección:** etiquetar la premisa en `boundaries.md` §7 como **HIPÓTESIS** o **POR VERIFICAR** con la profesional, o citar la fuente que la convierte en HECHO VERIFICADO; el refinamiento de anclaje puede sostenerse igualmente sin afirmar el hecho.

### 14. La lista de use cases de `boundaries.md` omite los mutadores internos que el slice declara
- **Archivos:** `docs\architecture\boundaries.md` §3 («**Use cases.** Uno por operación con significado de negocio: `OpenCase, … ReviewProposal, CommitReviewedFacts`. … Toda mutación commiteada pasa por un use case y produce **exactamente un** evento») vs `docs\architecture\vertical-slice-v0.md` *Application use cases required* → **Internos**: `GenerateDerivedRepresentation` y propagación de staleness.
- **Problema:** `DerivedRepresentationGenerated/Failed` y `ArtifactMarkedStale` son eventos de la lista cerrada (kernel §6) y mutaciones commiteadas, pero ningún use case de boundaries los produce; el documento que fija «dónde se cumple» deja fuera dos productores de eventos.
- **Corrección:** añadir en `boundaries.md` §3 una línea «Use cases internos (sin superficie): `GenerateDerivedRepresentation`; propagación de staleness como paso dentro de los mutadores», coherente con el slice.

---

## Baja gravedad / higiene de referencias

### 15. Números de invariante equivocados al citar ADR-006 en el glosario
- **Archivo:** `docs\domain\glossary.md` §2 Source — «No es el archivo del `Inbox/`… (**ADR-006, inv. 5**)» e invariante 2 «Idempotencia por hash… (**ADR-006, inv. 6**)».
- **Problema:** en `ADR-006` el inv. 5 es «El fragmento siempre resuelve a un Source», el inv. 6 es «El snapshot es independiente del origen» y el inv. 7 es «Idempotencia por hash». `vertical-slice-v0.md` (adversarial 5) cita correctamente «ADR-006 inv. 7», lo que confirma el desfase.
- **Corrección:** `inv. 5 → inv. 6` y `inv. 6 → inv. 7` en el glosario §2. (El resto de citas numeradas del glosario y del slice verificadas una a una: correctas.)

### 16. Relación no recíproca ADR-005 ↔ ADR-006
- **Archivos:** `docs\architecture\adrs\ADR-006-evidence-incorporation-boundary.md` Relaciones («**ADR-005 (autoridad humana):** frontera complementaria … Juntas cierran las dos vías») vs `docs\architecture\adrs\ADR-005-human-authority.md` Relaciones (solo ADR-001, ADR-003, ADR-004).
- **Problema:** es el único par con afirmación explícita de complementariedad y sin reciprocidad. (El resto de referencias entre ADRs se verificó: todas válidas y recíprocas donde procede.)
- **Corrección:** añadir en ADR-005 un ítem «**ADR-006 (frontera de incorporación):** ADR-006 controla qué puede fundamentar; este ADR, quién puede consolidar».

### 17. El supersede kernel §16.3 (10 → 9 tools) no se registra donde se define la superficie
- **Archivos:** `docs\architecture\adrs\ADR-001-trust-boundary.md` inv. 3 y test 7 («Nueve tools v0»); `docs\architecture\boundaries.md` §2.1 («`verify_legal_source` queda **fuera del slice**») — ninguno lo etiqueta como supersede; solo `docs\architecture\vertical-slice-v0.md` lo hace («supersede de la superficie de 10 tools de v0.1.1 — kernel §16.3»).
- **Corrección:** añadir la mención «(kernel §16.3, superseded de la superficie de 10 tools de v0.1.1)» en ADR-001 inv. 3 y en boundaries §2.1, que son los lugares normativos de la superficie.

### 18. `boundaries.md` abrevia dos contratos que el kernel declara exactos
- **Archivo:** `docs\architecture\boundaries.md` §3 — «`status: DRAFT | REGISTERED | REVIEWED | SUPERSEDED`» (sin los parámetros `(by, at, at_revision)`) y envelope «`… completeness, conditions[]`» (sin el enum `COMPLETE | TRUNCATED | PARTIAL`).
- **Problema:** kernel §10, glosario §9 y slice *Artifact behavior* escriben `REVIEWED(by, at, at_revision)`; ADR-004 y el slice escriben el enum de `completeness`. La abreviatura en el documento de fronteras invita a implementar un `REVIEWED` sin actor ni revisión.
- **Corrección:** restituir ambos literales en boundaries §3.

### 19. `EvidenceFragment` aparece con forma de entidad sin estar en el vocabulario canónico
- **Archivo:** `docs\architecture\vertical-slice-v0.md` — *Scope* («`propose_facts` con Fact ↔ **EvidenceFragment**») y happy path («`propose_facts` (Fact ↔ EvidenceFragment)»).
- **Problema:** el glosario fija: «Un nombre no listado aquí no existe como entidad de v0», y `EvidenceFragment` no está entre los trece. En el resto de los documentos el concepto se escribe «fragmento de Evidence». (El uso viene heredado del kernel §11, así que es normalización, no corrección de fondo.)
- **Corrección:** escribir «Fact ↔ fragmento de Evidence» en ambos lugares, o añadir una nota de una línea aclarando que `EvidenceFragment` es una abreviatura descriptiva y no una entidad.

### 20. Cita de supersede inexistente en el glosario
- **Archivo:** `docs\domain\glossary.md` §9 — «**Unificación a señalar (kernel §9 y §16):** `NEW_EVIDENCE_SINCE_ANALYSIS` deja de ser condición propia…».
- **Problema:** la unificación está en kernel §9; el registro de supersedes del §16 tiene seis ítems y ninguno es este (a diferencia de `NO_SUPPORT_FOUND`, §16.5, y `PENDING_CONFIRMATION`, §16.1, correctamente citados en el mismo documento).
- **Corrección:** citar solo «kernel §9», o proponer al kernel añadirlo como ítem 7 de §16 si se quiere trazar como supersede formal.

### 21. `ReviewProposal` es una decisión nueva no registrada en el kernel
- **Archivos:** `docs\architecture\adrs\ADR-005-human-authority.md` §4 («consolida en `ReviewProposal` lo que en borradores previos era un `ApproveProposal` separado»), adoptado sin fisuras por `boundaries.md` §2.2, `glossary.md` §12 y `vertical-slice-v0.md`.
- **Problema:** el kernel no nombra ningún use case del canal humano; el nombre y la consolidación se deciden en el ADR. Está señalado como refinamiento y es consistente en los cuatro documentos, pero no figura en el registro de supersedes del kernel §16, a diferencia de las otras normalizaciones equivalentes (§16.2, §16.4, §16.6).
- **Corrección:** proponer al kernel un ítem §16.7 («`ApproveProposal` (+ rechazo sin dueño) → `ReviewProposal(approve|reject)`»); no requiere tocar los cuatro documentos.

### 22. La lista consolidada de «Preguntas abiertas» de `boundaries.md` omite pendientes vivos de ADR-004 y ADR-006
- **Archivo:** `docs\architecture\boundaries.md` *Preguntas abiertas*.
- **Problema:** no recoge: destino para anclar el hash-cabeza del Case Event Log, valores del presupuesto por scope, política de retención/poda del Tool Invocation Log (los tres en `ADR-004-case-memory.md`), ni «si la referencia a material no incorporado merece condición UX propia» (`ADR-006`, heredado por el slice). Al ser el documento de fronteras el índice consolidado, esos pendientes quedan solo en sus ADRs.
- **Corrección:** añadir las cuatro entradas con su etiqueta y referencia al ADR de origen, o declarar en el encabezado de la sección que la lista es selectiva y no exhaustiva.

### 23. Tres nombres cercanos para la misma magnitud, sin nota de desambiguación
- **Archivos:** `case_revision` (envelope y respuestas de tool), `expected_revision` (parámetro de COMMAND/SENSITIVE_COMMAND) y `expected_case_revision` (campo de HumanAuthorization) — usados correctamente en kernel, ADR-004, ADR-005, glosario §10/§12, boundaries §3 y slice.
- **Problema:** no hay inconsistencia de uso, pero ningún documento explica por qué son tres nombres, y la entrada `CaseRevision` del glosario —el lugar natural— no los distingue.
- **Corrección:** una línea en `docs\domain\glossary.md` §10 («`case_revision` = revisión vigente reportada; `expected_revision` = la que declara el invocador de un COMMAND; `expected_case_revision` = la congelada en la HumanAuthorization»).

---

## Categorías sin hallazgos

- **(b) Superficie MCP:** las 9 tools y sus clases son idénticas en kernel §4, `boundaries.md` §2.1 y `vertical-slice-v0.md`; `commit_reviewed_facts` aparece en plural en todos los documentos producidos (las únicas apariciones en singular son las notas que registran la normalización, más los `notes\research-v0_1\*` previos, fuera de alcance). `ADMIN` vacía y `verify_legal_source` fuera del slice, consistentes en ADR-001, principles 15, boundaries y slice.
- **(d) Campos de `HumanAuthorization`:** la lista de campos es idéntica en ADR-005 §2, glosario §12 y slice *Persisted state*; `single_use` no aparece como campo en ninguno y `proposal_content_hash` está presente en los tres. El único defecto es el valor de `actor_type` (hallazgo 1).
- **(e) Sobre de `get_case_context`:** idéntico campo a campo entre `ADR-004-case-memory.md` y `vertical-slice-v0.md`, incluidos scopes v0, `procedural` RESERVADO y el renombre `recent_changes → changes_since(revision)` señalado en ambos. Única desviación: la abreviatura de `boundaries.md` (hallazgo 18).
- **(f) Schema de `Artifact`:** idéntico en kernel §10, glosario §9 y slice *Artifact behavior*, incluidas las marcas AÑADIDO y el estado de `knowledge_pack_versions[]`; la discrepancia «3 campos / 2 marcas» del kernel está correctamente señalada por el slice.