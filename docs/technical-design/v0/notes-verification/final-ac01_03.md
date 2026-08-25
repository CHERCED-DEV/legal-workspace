# Verificación AC-01 / AC-03 — corpus técnico V0

## Comprobaciones que pasan limpias

- **Invariante 6 de ADR-005** (línea 176): dice exactamente *"jamás commit NO AUTORIZADO, degradado ni silencioso"*, con el texto anterior conservado como superado. **PASA.**
- **`proposal_content_hash` como hash del payload del evento `FactsProposed`** — `09-events-and-audit.md:301` y la clave de idempotencia de `05-mcp-contract.md:616` — es uso **legítimo y distinto** del campo retirado de la HumanAuthorization. **PASA, no es residuo.**
- **`item_content_hash` uniforme** en `03`, `04`, `06`, `12` (y `05`, `08`, `09`, `11`): el gate, el esquema SQL y los tests están todos por item. **PASA** (falla solo en glosario y ADR-005, ver H1/H4).
- **OCHO tools** en `principles.md` (líneas 15, 99), `01` §9.1, `05` §6/§11.1, `12` §4 y `ADR-001` inv. 3. **PASA.**
- **`register_artifact` como operación interna** en `00` §6, `03` §9.7, `05` §8.2, `10` §5, `12`, `13`, `15`. **PASA.**

## Hallazgos

**H1 · ALTA · `docs/architecture/adrs/ADR-005-human-authority.md` §2 (líneas 52-60)**
Cita: `proposal_content_hash ← AÑADIDO al esquema de los dueños` … `operation ← enum v0: COMMIT_FACTS`.
Problema: el bloque del contrato sigue vigente sin marca de superado. `authorized_items[]` **sí** está correctamente marcado `[ELIMINADO por ENMIENDA AC-01]`, pero `proposal_content_hash` permanece como campo vivo, no aparecen `proposal_item_id`, `item_content_hash`, `review_session_id` ni `authorization_source`, y el campo se llama `operation` con valor **plural**. El §3 del mismo ADR ya está reescrito por item: el ADR se contradice a sí mismo.
Corrección: sustituir en el bloque `proposal_content_hash` por `proposal_item_id` + `item_content_hash` (conservando el texto viejo como superado, igual que se hizo con `authorized_items[]`), añadir `review_session_id` y `authorization_source`, y renombrar `operation → authorized_operation ← enum v0: COMMIT_FACT`.

**H2 · ALTA · `ADR-005` — invariante 4 (l. 126), validación 4 (l. 174), criterio de spike 3 (l. 111), consecuencia positiva (l. 137)**
Cita (inv. 4): "exige autorización viva, no consumida, con `proposal_content_hash` y `expected_case_revision` coincidentes".
Problema: cuatro apariciones vigentes del campo eliminado, en las partes normativas y en el test negativo. `03-application-use-cases.md:1015` ordena literalmente *"ADR-005 inv. 4 y 5 deben reformularse sobre `item_content_hash`"* — no se ejecutó.
Corrección: reescribir las cuatro sobre `item_content_hash`, con la vinculación **por item** ("por cada ProposalItem que se pretende commitear"), coherente con §3 y con ADR-008 §69.

**H3 · ALTA · `ADR-005` §4 (l. 97) y Preguntas pendientes 4 (l. 185)**
Citas: "(total o, **si los dueños confirman la aprobación parcial**, restringida a `items`)"; "qué otras operaciones entrarán en el enum `operation` … hoy solo `COMMIT_FACTS`".
Problema: presenta la aprobación parcial como no confirmada cuando AC-01 la aprobó (la Pregunta pendiente 1, l. 181, ya está marcada RESUELTA — incoherencia interna), y repite el plural.
Corrección: §4 → "con `approve` nace una `HumanAuthorization` por cada `ProposalItem` aprobado, agrupadas por `review_session_id`"; pendiente 4 → `authorized_operation`, "hoy solo `COMMIT_FACT`".

**H4 · ALTA · `docs/domain/glossary.md` §12 (l. 628-655, 662, 691) y §11 (l. 615)**
Cita: `proposal_content_hash …` / `authorized_items[] ← null = toda la propuesta … (DECISIÓN PENDIENTE de los dueños)` / `operation ← enum v0: COMMIT_FACTS`.
Problema: la entrada de HumanAuthorization del glosario **no recibió AC-01**: esquema con ambos campos eliminados, "Refinamiento 1: `proposal_content_hash` AÑADIDO", "No significa" con `COMMIT_FACTS`, Preguntas abiertas con *"aprobación parcial vía `authorized_items[]`"*, y §11 (Proposal) con *"DECISIÓN PENDIENTE: aprobación parcial (`authorized_items`)"*. Solo el invariante 3 fue actualizado a `item_content_hash` — el glosario se contradice consigo mismo.
Corrección: aplicar el mismo pase que en `04` §3.4: esquema por item, refinamiento 1 reescrito como `proposal_content_hash → item_content_hash (AC-01)`, `COMMIT_FACT` singular, y borrar las dos entradas de "DECISIÓN PENDIENTE" sobre aprobación parcial en §11 y §12.

**H5 · ALTA · `docs/architecture/vertical-slice-v0.md` (l. 49, 131, 168, 198, 328-332, 407, 419, 428, 614)**
Citas: "**Aprobación parcial activada** (`authorized_items`): … los dueños no la han confirmado"; `authorized_items[] ← null = toda la propuesta (parcial: pendiente de dueños)`; `operation ← enum v0: COMMIT_FACTS`.
Problema: el vertical slice **no recibió AC-01 en absoluto**. Mantiene el fuera-de-alcance de la aprobación parcial, el esquema por Proposal, el gate y los criterios de salida (F7, tabla de fallos) sobre `proposal_content_hash`, y el plural.
Corrección: pase completo AC-01 sobre el documento; F7 debe afirmar "una HumanAuthorization por item aprobado con `item_content_hash`", el gate debe verificar por item, y la línea 49 debe salir de "fuera de alcance".

**H6 · ALTA · `docs/architecture/boundaries.md` (l. 54, 323)**
Citas: "`ReviewProposal` … (y, **si los dueños confirman** `authorized_items[]`, aprobación parcial)"; "**DECISIÓN PENDIENTE (dueños) — Aprobación parcial de propuestas** (`authorized_items[]` en HumanAuthorization)".
Problema: dos residuos vigentes que declaran pendiente lo ya aprobado, en el documento de fronteras que un implementador lee primero.
Corrección: l. 54 → "con `approve` crea una HumanAuthorization por `ProposalItem` aprobado (AC-01)"; eliminar el bullet 323 de la lista de pendientes.

**H7 · ALTA · `docs/architecture/adrs/ADR-001-trust-boundary.md` validación 7 (l. 100)**
Cita: "el manifiesto de tools contiene exactamente **las 9 tools v0** con su clase".
Problema: contradice frontalmente su propio invariante 3 (l. 52), que ya dice **Ocho tools v0** por AC-03. `01` §9.1 y `05` §11.1 afirman ambos que "ADR-001 inv. 3 **y val. 7**" quedaron enmendados: la val. 7 quedó fuera del pase.
Corrección: "exactamente las **8** tools v0 … (ENMIENDA AC-03 aprobada, supersede §16.14)".

**H8 · ALTA · `docs/architecture/adrs/ADR-010-mcp-surface-and-command-classification.md` (Estado l. 5; l. 20, 131, 175, 183, 185, 192-193, 228, 244, 281)**
Citas: "se documenta como **conflicto sin resolver** en §11"; "Mientras no haya amendment, la cuenta normativa es **nueve**"; "**No es una resolución: es DECISIÓN PENDIENTE de los dueños**".
Problema: ADR-010 es el ADR de la superficie MCP y sigue **íntegramente sin enmendar**: declara nueve como cuenta normativa, presenta A/B/C/D como opciones abiertas, mantiene el riesgo "el conflicto de §11 bloquea un criterio de aceptación" y sigue en estado `Proposed`. Es el residuo AC-03 de mayor gravedad del corpus.
Corrección: banner de desenlace en §11 (opción **A aprobada**, AC-03), cuenta normativa = ocho, presupuesto V0 = 8 fijo (l. 131), retirar los riesgos y consecuencias que describen el conflicto como vivo, y promover el Estado a `Accepted`.

**H9 · ALTA · `docs/architecture/boundaries.md` §2.1 (l. 41), §3 (l. 64), diagrama (l. 234)**
Citas: fila `| register_artifact | COMMAND |` dentro de la tabla; "Nueve son alcanzables desde la superficie MCP"; `"tool calls · 9 tools v0 clasificadas"`.
Problema: el encabezado (l. 31) ya dice "ocho tools v0 (ENMIENDA AC-03 aprobada)" pero **la tabla que sigue tiene nueve filas** e incluye la tool retirada; §3 cuenta nueve use cases alcanzables por MCP incluyendo `RegisterArtifact`; el diagrama de la frontera dice 9. Encabezado y contenido se contradicen en el mismo documento.
Corrección: borrar la fila `register_artifact`; §3 → "**Ocho** son alcanzables desde la superficie MCP; `RegisterArtifact` es **interno** a `ProposeFacts` y `ReviewProposal` solo desde el canal humano"; diagrama → "8 tools v0 clasificadas".

**H10 · ALTA · `docs/architecture/vertical-slice-v0.md` (l. 22, 78, 133, 221, 248, 571, 617, 624)**
Citas: "| Superficie MCP | **9 tools** (kernel §4) |"; "El manifiesto de tools contiene **exactamente las 9 tools v0**"; "| F16 | … **Exactamente 9 tools** con clase declarada |"; paso 12 del happy path invocando `register_artifact` (COMMAND).
Problema: AC-03 sin aplicar. Es un defecto **ejecutable**: F16 y el criterio estructural 1 son criterios de aceptación de primera clase que hoy exigen nueve, mientras `12` `FT-013` exige ocho — los dos tests se contradicen. `13-synthetic-benchmark.md:654` y `:878` ya lo registran como "DIVERGENCIA DOCUMENTAL A CORREGIR" y sigue sin corregirse.
Corrección: 9→8 en las cinco cuentas; eliminar el paso 12 como invocación (sus eventos pasan a la transacción de `ProposeFacts`); F9 deja de ser test de tool; F16 y criterio estructural 1 → ocho, con "`register_artifact` no figura en el manifiesto".

**H11 · MEDIA · `docs/architecture/adrs/ADR-006-evidence-incorporation-boundary.md` inv. 3 (l. 48) y val. 3 (l. 89)**
Cita: "`register_artifact` valida que cada entrada de `inputs[]` sea una entidad del Case Store…".
Problema: ambas siguen redactadas con la tool retirada como sujeto. La opción A de AC-03 (aprobada) exigía explícitamente trasladar la literalidad al registro interno; la garantía no se debilita, pero el sujeto ya no existe en la superficie y la val. 3 invoca por nombre una tool inexistente.
Corrección: sujeto → "el registro interno de `FactAnalysis` **dentro de la transacción de `ProposeFacts`**"; val. 3 → ejercitar el use case interno, no la tool.

**H12 · MEDIA · `16-open-implementation-decisions.md` (l. 52, 53, 82-94, 111-121), `02-domain-model.md` (l. 432, 770), `03-application-use-cases.md` (l. 1017, 1084)**
Citas: "| **OD-02** | Superficie MCP: **8 tools vs 9** | **SÍ** |"; "| **OD-04** | Granularidad de `HumanAuthorization` … | **SÍ** |"; "`authorized_items[]` de ADR-005, que es **DECISIÓN PENDIENTE de los dueños**"; "| 18 | `authorized_operation = COMMIT_FACT` … | DECISIÓN PENDIENTE (nomenclatura) |".
Problema: OD-02 y OD-04 siguen listadas como **bloqueantes de Fase 1** con su ficha completa de decisión abierta, cuando AC-03 y AC-01 las cierran (OD-01 sí fue marcada "RESUELTA — enmienda AC-02 aprobada": el patrón existe y no se aplicó a estas dos). `02` §4 y §8.2 repiten "DECISIÓN PENDIENTE" sobre `authorized_items[]`, y `03` §13.2 punto 4 más la fila 18 de su tabla dejan `COMMIT_FACT` vs `COMMIT_FACTS` como "requiere ratificación".
Corrección: marcar OD-02 y OD-04 como `~~…~~ **RESUELTA — enmienda AC-03/AC-01 aprobada**` con `Blocking? NO (resuelta)`, conservando el análisis como registro histórico; en `02` y `03` sustituir "DECISIÓN PENDIENTE" por "RESUELTO por AC-01: singular `COMMIT_FACT`, autorización por item".

## Nota colateral (fuera de mi foco, AC-02)

Tres contradicciones vigentes que otro verificador debería recoger: `ADR-005` §1 — *"`ProposalReviewed` lo deja en N+1 … `FactsCommitted` lo deja en N+2"* — dentro del mismo párrafo que anuncia AC-02; `ADR-005` §4 — *"emite `ProposalReviewed` … **y avanza la CaseRevision**"*; y el ejemplo de `glossary.md` §12, que dice "el Case sigue en 14 … `expected_case_revision: 14`" y a renglón seguido "la autorización porta **15**". Todas contradicen la aritmética de referencia (14 → 14 → 15).