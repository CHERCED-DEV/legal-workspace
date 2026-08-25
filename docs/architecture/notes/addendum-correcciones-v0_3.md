# Addendum normativo v0.3 — correcciones de la consolidación

> **AVISO DE NORMALIZACIÓN (v0.4).** Este documento es **registro histórico** y conserva la escritura `actor_id / actor_type / actor_role`. Esa notación quedó **superada**: `Principal` (`principal_id`, `principal_type` ∈ HUMAN|AI|SYSTEM, `principal_role`) responde *quién ejecutó*, y `provenance_kind` (EXTERNAL_SOURCE|AI_DERIVATION|AI_INFERENCE|HUMAN_DECISION|SYSTEM) responde *cuál es la naturaleza epistemológica del origen*. Tabla de equivalencias y justificación en `docs/architecture/notes/normalizacion-principal-provenance-v0_4.md` (supersede §16.13). El texto histórico no se reescribe.


Este addendum es **normativo y posterior** al `kernel-consolidacion-v0_2.md`. Resuelve los hallazgos de las tres verificaciones cruzadas (estructura, consistencia, veracidad) ejecutadas sobre los diez documentos de la consolidación. Donde este addendum contradice al kernel v0.2, **manda este addendum**.

Origen de los hallazgos: `notes/verificacion-v0_2/` (informes de estructura, consistencia y veracidad).

---

## A. Fuentes primarias ahora auditables dentro del repositorio

La verificación de veracidad señaló (H14) que varias decisiones se citaban contra documentos ausentes del repositorio. Corregido: las fuentes primarias viven ahora en `docs/architecture/notes/`.

| Documento | Ruta en el repo | Qué autoriza |
|---|---|---|
| Prompt maestro v0.1 | `notes/prompt-maestro-v0_1.md` | Contexto original, §§1–35 citadas en los ADRs |
| Revisión arquitectónica v0.1.1 | `notes/revision-arquitectonica-v0_1_1.md` | Secciones A–J citadas como antecedente |
| Prompt de consolidación (dueños) | Ver Anexo B de este documento | Las seis decisiones aprobadas y las reglas literales |

### Falsos positivos de la verificación, resueltos por esta incorporación

Tres hallazgos de veracidad (H3, H4, H5) sostenían que ciertas reglas se habían promovido indebidamente a "DECISIÓN APROBADA". **Son falsos positivos**: las tres constan literalmente en el prompt de consolidación de los dueños (ver Anexo B, citas B.1, B.2 y B.3). La etiqueta `DECISIÓN APROBADA` se mantiene y ahora es auditable. Igualmente, el hallazgo estructural H9 (rótulo `Validación · pruebas necesarias`) es falso positivo: los dueños escribieron `## Validación / pruebas necesarias` con barra; **los seis ADRs son correctos y no se tocan**.

---

## B. Correcciones normativas (obligatorias en todos los documentos)

### B.1 `actor_type` de la HumanAuthorization: `HUMAN_DECISION`

**Problema real (consistencia H1, veracidad H7):** el kernel v0.2 §5 escribió `actor_type=HUMAN`, valor que no pertenece al enum canónico del §2. Error del kernel, propagado a ADR-005, glosario §12 y slice.

**Corrección:** el valor es **`HUMAN_DECISION`** en todos los casos. El enum canónico es y sigue siendo `EXTERNAL_SOURCE | AI_DERIVATION | AI_INFERENCE | HUMAN_DECISION | SYSTEM`. Registrar como **supersede §16.7 — normalización de nombre, no de semántica**. No es DECISIÓN PENDIENTE: es una errata del kernel, ya corregida aquí.

### B.2 Momento de emisión de `ProposalReviewed` y valor de `expected_case_revision`

**Problema real (estructura H2, consistencia C2 y C3):** ADR-005 emitía `ProposalReviewed` en el commit; slice y glosario lo emiten en el acto de revisión. No es cosmético: cambia la aritmética de revisiones.

**ESTADO v0.4 — ENMIENDA AC-02 aprobada: supersede los puntos 1, 3 y 4 de este apartado** (kernel §5.2; ADR-004 supersede §16.16, ADR-005 supersede §16.19). **Vigente:** `ProposalReviewed` avanza `event_seq` y lleva `case_revision` **NULL** —**no** avanza la revisión del Case—; `expected_case_revision` es **la revisión vigente del Case en el momento del acto de revisión**, la que la profesional tiene a la vista al aprobar, y **no** `base_case_revision`: `FactsProposed` y `ArtifactRegistered` ya avanzaron el contador. Ejemplo recalculado: si `propose_facts` deja el Case en **14**, `ProposalReviewed` lo deja **en 14** (`case_revision` NULL) y `FactsCommitted` en **15**. El punto 2 conserva lo único que AC-02 no toca: el **momento de emisión** en el acto de revisión. Lo que sigue es el texto histórico de v0.3, conservado por trazabilidad.

**Corrección normativa de v0.3 — texto superado en su aritmética por AC-02:**

1. `ReviewProposal(approve)` emite **`ProposalReviewed(approved)`** y avanza la CaseRevision. En ese mismo acto se crea la `HumanAuthorization`.
2. `commit_reviewed_facts` emite **`FactsCommitted`** y avanza la CaseRevision de nuevo. Son dos eventos en dos revisiones distintas.
3. **`expected_case_revision` de la HumanAuthorization = la revisión resultante del acto de revisión** (la que deja `ProposalReviewed`), no la revisión contra la que se creó la Proposal. Semántica: "la revisión del expediente que la profesional tenía a la vista al aprobar".
4. Los ejemplos numéricos del glosario §10 y §12 deben recalcularse con esta regla (si `FactsProposed` deja el Case en 14, `ProposalReviewed` lo deja en 15 y la autorización porta 15).

Corregir ADR-005 §3 e Invariantes; ajustar los ejemplos del glosario. El slice ya es correcto: sustituir su nota conciliatoria ("la diferencia es de momento de emisión, no de contenido") por la cita de esta regla.

### B.3 Definición normativa de "mutación" para el invariante de auditoría

**Problema real (estructura H1, consistencia C4):** cinco documentos afirman "n mutaciones == n eventos" sin definir mutación; el slice necesita que un COMMAND produzca varios eventos (`EvidenceIncorporated` + `ArtifactMarkedStale`).

**Corrección normativa (texto a incorporar en ADR-004, invariante 5, y a citar desde ADR-001 inv. 2, boundaries §3 y principles §2):**

> **Mutación** = cambio de estado canónico registrado, **no** invocación de tool. Una sola invocación puede producir de 1 a n mutaciones, y por tanto de 1 a n eventos del Case Event Log, avanzando la CaseRevision en n. El invariante es: **toda mutación produce exactamente un evento, y todo evento corresponde a exactamente una mutación** — biyección mutación↔evento, no invocación↔evento. El property test verifica la biyección, no el conteo de llamadas.

El slice deja de proponer esta lectura y pasa a citarla.

### B.4 Plano de cada término: Domain vs Application

**Problema real (estructura H3, consistencia C12):** `boundaries.md` sitúa `Artifact`, `Proposal`, `HumanAuthorization` y `CaseRevision` dentro del Domain; el glosario y ADR-003 los tratan como conceptos de soporte de Application.

**Corrección normativa — manda el glosario:**

| Plano | Términos |
|---|---|
| **Domain** (entidades epistémicas, ADR-003) | `Case`, `Source`, `Evidence`, `Statement`, `Fact`, `EvidenceLink`, `ProvenanceRecord`, `ProfessionalDetermination`, `DerivedRepresentation` |
| **Application** (conceptos de soporte) | `Artifact`, `Proposal`, `HumanAuthorization`, `CaseRevision` |

Razón: los cuatro de Application no son proposiciones sobre el mundo jurídico ni portan estatus epistémico; son mecanismos de trabajo, control de concurrencia y autorización. `CaseRevision` es propiedad observable del Case pero su administración (incremento, comparación, conflicto) es lógica de Application. Corregir `boundaries.md` §4 y su Mermaid §9.4 (mover los cuatro al nodo `APP`).

### B.5 `DETERMINED`, `ProfessionalDetermination` y `FactWithdrawn`: sin productor en v0

**Problema real (estructura H4, consistencia C5):** `DETERMINED` es transición almacenada y criterio de aceptación de ADR-003, pero ninguna tool, use case ni evento de la lista cerrada la produce; lo mismo para `FactWithdrawn`.

**Corrección normativa:**

1. En **ADR-003**, el escenario t1–t6 se declara **ilustrativo del modelo**, no ejecutable en v0; sus asserts sobre `ProfessionalDetermination` se marcan **post-slice**.
2. Se registran dos use cases **conocidos y diferidos** (no v0, pero con nombre reservado para no improvisarlos después): `RecordProfessionalDetermination` y `WithdrawFact`, ambos del canal humano, ambos SENSITIVE (exigen HumanAuthorization).
3. La lista cerrada de eventos v0 conserva `FactWithdrawn` pero **anota explícitamente que no tiene productor en v0**. Alternativa rechazada: eliminarlo de la lista (obligaría a reabrir el contrato de eventos al implementar el retiro de hechos, que es funcionalidad segura y previsible).
4. El slice mantiene `ProfessionalDetermination` en "no ejercitada" y lo dice también en *Explicit non-goals*.

### B.6 `OPERATION_NOT_PERMITTED`: solo capacidad existente vetada

**Problema real (estructura H5, consistencia C9, veracidad H6):** el slice exige esa condición para operaciones que no existen en la superficie; si la tool no está en el manifiesto, el fallo ocurre en el protocolo y el Core nunca la ve.

**Corrección normativa:**

- `OPERATION_NOT_PERMITTED` se emite **únicamente** cuando la capacidad existe y una política o el perfil del principal la vetan. Es condición del Core.
- Para operaciones **inexistentes en la superficie** (acreditar directamente, modificar un Source, marcar una fuente como verificada en v0): **no hay condición del catálogo**. El resultado esperado es que la tool no exista en el manifiesto, verificable por el test de superficie; la respuesta al usuario es mensaje de producto, no condición tipada.
- Corregir en el slice las filas 1, 4 y 9 de la matriz y la entrada correspondiente de *Negative paths*; alinear `principles.md` §15.

### B.7 `Statement` no se materializa en v0

**Problema real (estructura H7, consistencia C10):** el slice lo cuenta como ejercitado y a la vez como prescindible; ningún use case lo crea y ningún test lo verifica.

**Corrección normativa:** en v0 **no se materializan Statements**. La cadena de provenance del slice es `Fact → EvidenceLink → fragmento → DerivedRepresentation → Source`, que es suficiente para la propiedad 6 del maestro §34. Consecuencias a reflejar:

- Slice: mover `Statement` a la columna "no ejercitado" y añadirlo a *Explicit non-goals*, declarando qué invariantes quedan sin verificar en v0.
- ADR-003 y glosario: marcar los ejemplos que arrancan en `ST-9` como **ilustrativos del modelo, no ejercitados en v0**.
- La entidad permanece definida en el Domain: se materializará cuando exista un extractor (`ExtractStatements`, post-slice).

### B.8 `DerivedRepresentation` en *Persisted state*

**Problema real (estructura H6):** es entidad persistida y sustrato de tres pasos del happy path, pero falta en la sección que fija el estado persistido.

**Corrección:** añadir al slice el bloque conceptual `DerivedRepresentation { derivation_id, case_id, source_id, version, content_hash, recipe { tool, version }, state: PENDING|READY|FAILED, provenance, created_at }`, con la nota "persistido pero regenerable".

### B.9 Windows: separar el hecho de plataforma del contexto del equipo

**Problema real (veracidad H1):** tres documentos etiquetan `HECHO VERIFICADO (kernel §1)` una frase que mezcla el hecho verificado con la edición del equipo.

**Corrección:** partir la frase en todos los casos.
- `HECHO VERIFICADO (kernel §1; fuente: code.claude.com/docs — sandboxing): el sandbox de Bash de Claude Code no es nativo en Windows.`
- `CONTEXTO DEL PROYECTO (SUPUESTO): el equipo objetivo es Windows; la edición concreta y la disponibilidad de cifrado de disco quedan POR VERIFICAR.`

### B.10 SQLite: la co-localización es restricción del adapter, no regla del Domain

**Problema real (veracidad H2):** `principles.md` §12, `boundaries.md` §6 y el slice elevan una propiedad de SQLite/WAL a "requisito de corrección" del sistema, contradiciendo la regla del propio corpus ("ninguna feature de plataforma se convierte en regla del Domain").

**Corrección:** el principio se enuncia en términos de dominio ("el estado canónico y la evidencia viven bajo control exclusivo del Core, con custodia local") y la co-localización se degrada a consecuencia del adapter v0: *mientras la persistencia sea SQLite en modo WAL, la co-localización de procesos es requisito de corrección **de ese adapter** (HECHO VERIFICADO, kernel §1); además el slice fija una máquina como parámetro aprobado (kernel §11)*. Aplicar en los tres documentos.

### B.11 Supuestos operativos etiquetados

**Problema real (veracidad H10, H11):** afirmaciones sobre la conducta de los LLM y sobre frecuencias de lectura/escritura y duración de análisis se presentan como hechos.

**Corrección:**
- Conducta de modelos → `SUPUESTO de diseño (premisa de robustez): el sistema asume que cualquiera de esas conductas puede ocurrir; la seguridad no depende de que no ocurran.`
- "No existe forma conocida de forzar a un modelo a transmitir un texto literal" → `SUPUESTO: no conocemos mecanismo que lo garantice; POR VERIFICAR si el host permite mostrar salida de tools sin mediación del modelo.`
- Frecuencias y duraciones (ADR-004 §(b)2 y Alternativas 4; slice *Revision behavior*) → anteponer `SUPUESTO (a validar con uso real; ver preguntas de negocio abiertas):`. La decisión no cambia; cambia su fundamento declarado.

### B.12 `HECHO VERIFICADO` siempre con fuente

**Problema real (veracidad H12):** cuatro instancias llevan la etiqueta sin fuente.

**Corrección:** toda etiqueta `HECHO VERIFICADO` cita `(kernel §1; fuente: <URL o documento>)`. Para deny rules y hooks: `code.claude.com/docs — permissions, hooks`. Para el versionado de skills: `code.claude.com/docs/en/skills.md`.

### B.13 Nombre único: **Knowledge Pack**

**Problema real (consistencia C11):** `boundaries.md` introduce "Content Pack" como renombre canónico; el resto del corpus y el campo `knowledge_pack_versions[]` usan "Knowledge Pack".

**Corrección:** el nombre canónico es **Knowledge Pack**. La distinción que `boundaries.md` quería capturar se conserva en prosa: *un Knowledge Pack contiene únicamente contenido declarativo con procedencia; las reglas ejecutables viven en el producto sellado y la configuración de cliente es un tercer artefacto* (kernel §14 del maestro §23). Registrar como supersede §16.8.

### B.14 Estado derivado `UNSUPPORTED`: precisión

**Problema real (consistencia C8):** un Fact con solo links `CONTEXTUALIZES` activos no cae en ningún estado derivado.

**Corrección (precisión, no decisión nueva):** `UNSUPPORTED` = **cero links de polaridad probatoria (`SUPPORTS` / `CONTRADICTS`) activos**. Los links `CONTEXTUALIZES` no alteran el estado derivado; aportan contexto, no soporte ni contradicción. Reflejar en ADR-003, glosario §5/§6 y en el test F12 del slice, señalado como precisión de la consolidación.

### B.15 Criterio del spike de autorización humana, en términos propios

**Problema real (veracidad H18):** el criterio de aceptación del canal humano se expresa por referencia a los MUSTs de una versión de la spec MCP.

**Corrección:** enunciar el criterio como propiedad del sistema y citar la spec solo como precedente:

> **Criterio de salida del spike (propio del sistema):** (1) consentimiento humano explícito por acto; (2) superficie de decisión no inspeccionable ni accionable por el cliente ni por el LLM; (3) vinculación verificable al `proposal_content_hash` y a `expected_case_revision`. El modo URL de elicitation MCP (HECHO VERIFICADO, kernel §1) satisface (1) y (2) y sirve de **referencia**, no de definición.

### B.16 Product Floor: etiqueta dentro de la taxonomía

**Problema real (veracidad H17):** `DECISIÓN APROBADA EN PRINCIPIO` crea una octava etiqueta fuera de la taxonomía.

**Corrección:** usar `DECISIÓN APROBADA` y expresar en prosa lo que los dueños calificaron "en principio": *el mecanismo del piso está aprobado; el contenido de la lista es un primer conjunto universal, abierto a ampliación*. (Cita literal de los dueños en Anexo B.4.)

### B.17 Correcciones de referencia (menores, mecánicas)

| Documento | Corrección |
|---|---|
| `glossary.md` §2 Source | `ADR-006, inv. 5` → **inv. 6**; `ADR-006, inv. 6` → **inv. 7** |
| `glossary.md` §9 | La unificación de `NEW_EVIDENCE_SINCE_ANALYSIS` se cita como **kernel §9** (no §16) |
| `glossary.md` §10 CaseRevision | Añadir desambiguación: `case_revision` (revisión vigente reportada) / `expected_revision` (la que declara el invocador de un COMMAND) / `expected_case_revision` (la congelada en la HumanAuthorization) |
| `glossary.md` §7 | Marcar la semántica de `EXTERNAL_SOURCE` y `SYSTEM` como **precisión de la consolidación**, propuesta como invariante |
| `boundaries.md` §3 | Restituir `REVIEWED(by, at, at_revision)` y el enum `completeness: COMPLETE | TRUNCATED | PARTIAL`; marcar `stale_reasons[]` y `supersedes_artifact_id?` como **AÑADIDOS en la consolidación (kernel §10)**; añadir los use cases internos (`GenerateDerivedRepresentation`, propagación de staleness) |
| `boundaries.md` §7 | Etiquetar como **DECISIÓN APROBADA (dueños, §13 del prompt de consolidación)** que el rol se resuelve por Case/contexto activo; el trabajo real del contexto B sigue **NO LEVANTADO** |
| `boundaries.md` §2.1 y `ADR-001` inv. 3 | Añadir "(kernel §16.3: supersede de la superficie de 10 tools de v0.1.1)" |
| `principles.md` §7 y `boundaries.md` §3 | Señalar el refinamiento `recent_changes → changes_since(revision)` (kernel §8) |
| `principles.md` §9 | Señalar que el catálogo de 7 condiciones es **reducción normativa** con sus tres unificaciones (kernel §9, §16) |
| `ADR-005` Relaciones | Añadir ADR-006 (reciprocidad: ADR-006 controla qué puede fundamentar; ADR-005, quién puede consolidar) |
| Los 6 ADRs, Relaciones | Cerrar la malla: ADR-002↔ADR-003/005, ADR-004↔ADR-006 |
| `vertical-slice-v0.md` | `EvidenceFragment` → "fragmento de Evidence" (no es entidad del vocabulario canónico) |
| `vertical-slice-v0.md` Test matrix | Añadir **F18**: identificadores inventados y rutas arbitrarias (incluido path traversal `..`, rutas absolutas, symlinks/junctions) → rechazo con código semántico estable (ADR-001 inv. 7, ADR-002 val. 4, ADR-006 val. 6). Los 10 adversariales aprobados permanecen intactos |
| `vertical-slice-v0.md` | Añadir tabla de trazabilidad invariante→test→condición, marcando explícitamente los invariantes **no verificados en v0** (ADR-003 inv. 3, 4, 5, 8) |
| `ADR-001` Validación | Encabezar la lista: "Subconjunto que ataca esta frontera; la matriz completa (10 adversariales + funcionales) está en `vertical-slice-v0.md`" |
| `boundaries.md` Preguntas abiertas | Añadir los pendientes vivos de ADR-004 (destino de anclaje del hash-cabeza; valores del presupuesto por scope; retención del Tool Invocation Log) y de ADR-006 |

---

## C. Registro de supersedes ampliado (continúa kernel §16)

7. `actor_type = HUMAN` (kernel v0.2 §5) → **`HUMAN_DECISION`** (normalización al enum canónico; errata del kernel).
8. "Content Pack" (boundaries) → **"Knowledge Pack"** (nombre canónico único).
9. `ApproveProposal` → **`ReviewProposal(approve|reject)`** (consolidación del canal humano; incluye el rechazo, que antes no tenía dueño).
10. `ProposalReviewed` emitido en el commit (ADR-005 borrador) → **emitido por `ReviewProposal`**; el commit emite solo `FactsCommitted`.
11. "n mutaciones == n eventos" sin definir → **biyección mutación↔evento**, con `mutación = cambio de estado registrado` (B.3).
12. `OPERATION_NOT_PERMITTED` para operaciones inexistentes → **solo para capacidad existente vetada por política/perfil** (B.6).

---

## D. Cuestiones abiertas detectadas durante la corrección (para los dueños)

Los correctores señalaron cuatro puntos que **no** resuelven por su cuenta y que quedan para decisión de ustedes. Ninguno bloquea el diseño del vertical slice.

1. **`ProposalReviewed(partial)` presupone una decisión no tomada.** La lista cerrada de eventos incluye la variante `partial`, pero la aprobación parcial (`authorized_items[]`) es DECISIÓN PENDIENTE. Si ustedes rechazan la aprobación parcial, hay que retirar también esa variante del enum de eventos, no solo el campo del contrato.
2. **Granularidad de "invariante no verificado en v0".** Los invariantes 3 y 8 de ADR-003 agrupan tramos de verificabilidad distinta: el invariante 3 (`status_history` append-only) sí es ejercitable en `PROPOSED → ALLEGED` y solo el brazo `WITHDRAWN` queda fuera; el invariante 8 mezcla la inmutabilidad de `Statement` (no verificable en v0) con la de `Source` y la referencia `DerivedRepresentation → Source` (ambas sí ejercitadas). Marcarlos enteros como "no verificados" subdeclara la cobertura real. Decidir si se parten.
3. **Momento exacto en que `propose_facts` avanza la revisión.** El kernel §4 dice que `propose_facts` "no muta el Case state más allá de registrar la propuesta"; la aritmética de B.2 asume que `FactsProposed` avanza la revisión. Ambas cosas son compatibles bajo la definición de mutación de B.3 (registrar la propuesta *es* un cambio de estado registrado), pero conviene que quede dicho de forma explícita en el kernel.
4. **Las etiquetas SUPUESTO de B.11 remiten a preguntas de negocio que aún no existen como tales.** Frecuencia de lecturas frente a mutaciones y duración típica de un análisis no figuran entre las preguntas abiertas del corpus. O se crean como preguntas, o la etiqueta se redirige al `POR VERIFICAR` sobre el umbral de revisiones por agregado que ya existe en ADR-004.

---

## Anexo B — Citas literales del prompt de consolidación (fuente de las decisiones aprobadas)

Incorporadas para que las etiquetas `DECISIÓN APROBADA` sean auditables dentro del repositorio.

**B.1 — Regla de entrada al dominio** (prompt de consolidación, §7): *"La regla será: Una entidad entra al dominio cuando existe evidencia de que tiene lifecycle, identidad o invariantes propios."*

**B.2 — Nombres reservados** (§7): *"Reserva conceptualmente para evolución posterior: Assertion, Contradiction, Gap, LegalIssue, Hypothesis, Argument, Ruling, ProceduralEvent, Term, Deadline — pero NO los conviertas automáticamente en entidades v0."*

**B.3 — Frontera de incorporación** (§11): *"La información encontrada en una integración externa puede orientar al modelo, pero no puede fundamentar una transición canónica del Case hasta ser incorporada formalmente."* Y: *"EXPLORATION ≠ CASE EVIDENCE."* Y, sobre el resultado buscado: *"Queremos conservar la hiperconectividad de Claude/Cowork"* … *"Esto nos permite tener: hiperconectividad + trazabilidad."* — con lo que la formulación que ADR-006 atribuye a los dueños queda auditable.

**B.4 — Product Floor** (§21): *"DECISIÓN APROBADA EN PRINCIPIO. Existirán políticas de seguridad/integridad que el cliente no puede relajar. La configuración puede endurecerlas. No debilitarlas."*

**B.5 — Roles jurídicos** (§13): *"El rol NO pertenece a la organización de manera fija. Debe poder resolverse por Case o por active working context."*

**B.6 — Revisiones** (§18): *"Una operación iniciada sobre revisión N no puede sobrescribir silenciosamente revisión N+1. Pero: no queremos perder el trabajo generado."*

**B.7 — Estructura de sección de los ADRs** (§26): los dueños escribieron `## Validación / pruebas necesarias` **con barra**. Los seis ADRs son correctos.

**B.8 — Los 15 títulos de principios** (§27): LLM is untrusted · Core owns canonical state · Prompts cannot enforce invariants · Original evidence is preserved · Exploration is not incorporation · AI proposes; sensitive state requires human authority · Chat is a channel, not memory · Every relevant claim has provenance · Uncertainty must remain visible · Domain is vendor-independent · Integrations are adapters · Local-first does not mean LLM-offline · Prefer deterministic mechanisms over LLM judgment when possible · No premature distributed architecture · Security through capabilities, not instructions.

**B.9 — Los 10 tests adversariales** (§24): acreditar directamente un hecho · enviar aprobación humana inventada · crear EvidenceLink contra material no incorporado · modificar Source original · reintentar ingestión del mismo material (idempotencia) · commit basado en revisión vieja (falla y preserva la propuesta) · mezclar Case A con Case B · usar Artifact stale como vigente · marcar fuente jurídica como verificada por afirmación propia · perder contexto conversacional y reabrir el Case (reconstruye desde estado canónico).
