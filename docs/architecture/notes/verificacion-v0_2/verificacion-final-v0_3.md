## Verificación de la aplicación del addendum v0.3

| # | Verificación | Resultado | Nota |
|---|---|---|---|
| 1 | `actor_type = HUMAN_DECISION` en ADR-005, glosario §12 y slice; cero `actor_type = HUMAN` fuera de notas de normalización | **OK** | ADR-005 §2/§inv.1, glosario §12 (contrato, lifecycle, inv. 1) y slice *Persisted state* usan `HUMAN_DECISION`. Las únicas apariciones de `HUMAN` son las notas de errata/supersede §16.7 (ADR-005 L59/78/116, glosario L652, slice L330-332) |
| 2 | `ProposalReviewed` emitido por `ReviewProposal`; `expected_case_revision` = revisión resultante del acto de revisión; ejemplos numéricos coherentes | **OK** | ADR-005 §1/§3/§4 e inv. 9-10; slice L146-152 (6→7→8) y F7/F7b; glosario §10 inv. 5-6 y §11-§12 (14→15→autorización 15). ADR-004 (b)1 concuerda |
| 3 | Definición de mutación (biyección mutación↔evento) en ADR-004 y citada por ADR-001, boundaries y principles | **OK** | ADR-004 inv. 5 (con supersede §16.11); ADR-001 inv. 2; boundaries §3 L68; principles §2 L21; slice L140-144 la cita, no la propone |
| 4 | Plano Application de `Artifact`/`Proposal`/`HumanAuthorization`/`CaseRevision` en boundaries §4, su Mermaid y el mapa del glosario | **OK** | boundaries §4 (tabla + razón), Mermaid §9.4 (los cuatro dentro del nodo `APP`), glosario mapa filas 9-12 y párrafo B.4; ADR-003 lo replica. Residuos fuera de esos tres lugares: D1 y D2 |
| 5 | `OPERATION_NOT_PERMITTED` ya no exigido para operaciones inexistentes (slice y principles) | **OK** | slice L525/528 y filas 1, 4 y 9 de adversariales + *Negative paths* L173; principles §15 L99; ADR-006 Preguntas L100 concuerda |
| 6 | "Knowledge Pack" nombre único en boundaries | **OK** | §8 titulado *Knowledge Packs*; "Content Pack" solo aparece en la línea que registra el supersede §16.8, como exige B.13 |
| 7 | `Statement` no materializado en v0, consistente en slice, ADR-003 y glosario | **OK** | slice *non-goals* L44, tabla de entidades L189, *Persisted state* L295-300, trazabilidad inv. 8; ADR-003 L109-112 y §Validación 1; glosario §4 L195, mapa fila 4, diagrama de cadena, §5 t1, §7 fila `ST-9` |
| 8 | `DerivedRepresentation` en *Persisted state* del slice | **OK** | slice L285-293 con los nueve campos de B.8 y la nota "persistido pero regenerable" |
| 9 | Toda etiqueta `HECHO VERIFICADO` con fuente | **PENDIENTE** | Una instancia sin `fuente:` — ver D5 |
| 10 | Estructura: 6 ADRs con 11 secciones y `## Validación / pruebas necesarias`; principles 15; glosario 13×6; slice 18 secciones | **OK** | ADR-001…006: 11 encabezados `##` idénticos y rótulo con barra; principles: 15 `## n.`; glosario: 13 términos × 6 subsecciones; slice: 18 secciones |
| 11 | F18 añadido sin tocar los 10 adversariales | **OK** | F18 presente (L622) con ADR-001 inv. 7 / ADR-002 val. 4 / ADR-006 val. 6; los 10 adversariales intactos, solo la columna *Condición emitida* de 1, 4 y 9 ajustada por B.6, declarado en L597 |
| 12 | Citas corregidas en glosario §2 (ADR-006 inv. 6 e inv. 7) | **OK** | §2 "No significa" cita inv. 6 (snapshot independiente del origen) e inv. 2 cita inv. 7 (idempotencia): coinciden con la numeración real de ADR-006 |

## Defectos que quedan

**D1 — `principles.md` §10, L69 (plano incorrecto; contradice B.4).**
Cita: *"Exige que el Domain razone en `Case, Source, Evidence, Statement, Fact, EvidenceLink, ProvenanceRecord, ProfessionalDetermination, Artifact, CaseRevision, Proposal, HumanAuthorization, DerivedRepresentation`…"*
Corrección: dejar en la lista del Domain las nueve entidades epistémicas y mover `Artifact`, `Proposal`, `HumanAuthorization` y `CaseRevision` a una cláusula de Application ("…y que Application razone en los cuatro conceptos de soporte…"), como en boundaries §4 y el glosario.

**D2 — `vertical-slice-v0.md`, sección *Domain entities exercised* (L179-197).**
La tabla titulada "Domain entities exercised" incluye filas `CaseRevision`, `Proposal`, `HumanAuthorization` y `Artifact`, que B.4 sitúa en Application.
Corrección: retitular a "Entidades y conceptos ejercitados" y separar las filas en dos bloques rotulados **Domain** (nueve) / **Application** (cuatro), o añadir columna "plano".

**D3 — `vertical-slice-v0.md`, *Derived state*, L374 (contradice B.14, ADR-003 inv. 6 y glosario §5/§6).**
Cita: *"`UNSUPPORTED` (0 links activos)"*.
Corrección: *"`UNSUPPORTED` (cero links de polaridad probatoria —`SUPPORTS` / `CONTRADICTS`— activos; los `CONTEXTUALIZES` activos no computan)"*. Misma corrección en L534 (*"un hecho sin links activos es `UNSUPPORTED`"*).

**D4 — `vertical-slice-v0.md`, F12 (L616) frente a la fila 6 de trazabilidad (L637).**
La fila de trazabilidad afirma que F12 verifica *"los `CONTEXTUALIZES` no computan"*, pero F12 solo dice *"sin links activos, `UNSUPPORTED`"*. B.14 exigía reflejar la precisión en F12.
Corrección: añadir a F12 el caso *"un Fact cuyos únicos links `ACTIVE` sean `CONTEXTUALIZES` se reporta `UNSUPPORTED`"*.

**D5 — `vertical-slice-v0.md`, *Questions blocking implementation* 2, L681 (incumple B.12).**
Cita: *"MCP elicitation **modo URL** (HECHO VERIFICADO en la spec, kernel §1; **POR VERIFICAR** el soporte en el host concreto)"*.
Corrección: *"(HECHO VERIFICADO, kernel §1; fuente: spec MCP — elicitation, 2025-11-25; POR VERIFICAR el soporte en el host concreto)"*, igual que en L409/L417 del mismo documento.

**D6 — `domain/glossary.md` §10, invariante 2, L554 (abreviatura sin la definición fijada en B.3).**
Cita: *"n mutaciones commiteadas ⇔ n eventos del Case Event Log (property test, ADR-004)"*.
Corrección: sustituir por la biyección con su definición — *"biyección mutación↔evento (ADR-004 inv. 5; addendum B.3): mutación = cambio de estado canónico registrado, no invocación de tool"* —, como ya hacen ADR-001, boundaries §3 y principles §2.

**D7 — `boundaries.md` §4, L98 (precisión B.14 ausente).**
Cita: *"**Estados derivados**, computados desde EvidenceLinks activos y **nunca almacenados como status**: `SUPPORTED | CONTRADICTED | UNSUPPORTED`"*.
Corrección: precisar *"desde los EvidenceLinks `ACTIVE` de polaridad probatoria (`SUPPORTS` / `CONTRADICTS`); los `CONTEXTUALIZES` no alteran el estado derivado (addendum B.14)"*.