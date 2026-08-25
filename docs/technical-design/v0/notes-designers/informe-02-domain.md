# Informe del disenador: 02-domain

Retorno crudo del agente que redacto este documento. Contiene: rutas, decisiones que requieren aprobacion, conflictos y POST-V0 / POR VERIFICAR.

---

**(1) Rutas escritas**

- `C:/Users/HITMA/Desktop/legal-workspace/docs/technical-design/v0/02-domain-model.md` (único archivo creado o modificado)

**(2) Decisiones técnicas que tomaste y requieren aprobación** (todas etiquetadas `PROPUESTA DEL TECHNICAL DESIGN` y consolidadas en §8.1 del documento)

1. `EvidenceFragment` y `FactStatusEntry` reciben nombre de **tipo** (value object / registro hijo) sin promoverse a entidad — coherente con addendum v0.3 §B.17 — y **no se introduce `SourceVersion`**: un `Source` inmutable tiene una sola representación, y su `content_hash` es su identidad de versión.
2. `EvidenceFragment` explícito en lugar del `fragment { source_version_hash, selector }` del corpus: `{ source_id (siempre), anchored_in: SOURCE|DERIVED_REPRESENTATION, representation_hash, derivation_id?, selectors[] }`. Hace verificable ADR-003 inv. 7 (INV-D-29/30/33) en vez de dejarlo implícito.
3. `provenance_kind` de `DerivedRepresentation` se decide desde `recipe`: `AI_DERIVATION` si la receta involucra un modelo, `SYSTEM` si es determinista. `vertical-slice-v0.md` fija hoy `AI_DERIVATION` para toda derivación, lo que afirmaría IA donde no la hubo (extracción de texto por librería). Afecta una línea de ese documento; ningún ADR.
4. **Dos niveles de garantía del `HUMAN_DECISION`** —*acreditado por canal* (con `HumanAuthorization`) vs *declarado por sesión* (COMMAND no sensible invocado por el modelo)— **sin ampliar el enum cerrado**: lo que los distingue es la autorización vinculada, y el gate sensible ya la exige (INV-D-21).
5. Matriz de `provenance_kind` por registro (§2.4): `Case = HUMAN_DECISION/HUMAN`; `Source`/`Evidence` = `EXTERNAL_SOURCE/HUMAN`.
6. **Materialización diferida del `Fact`**: el Fact del Domain se crea en el commit, con dos entradas de `status_history` (`PROPOSED` con la provenance/`occurred_at`/`origin_ref` del ProposalItem, y `ALLEGED`); `fact_id` se emite en el commit; identidad estable durante la revisión = `proposal_item_id`. Alternativa rechazada documentada.
7. La marca *"solo alegado"* vive en el `ProposalItem` (Application), **no** como campo del `Fact`: un booleano paralelo podría divergir de los links y es el "atajo de atributo" que ADR-003 prohíbe.
8. `EvidenceLink.provenance` (origen epistémico: `AI_INFERENCE`) separado de `committed_under { authorization_id, event_id, at_case_revision }` (acto humano de incorporación). Rotular el link como `HUMAN_DECISION` por haberse aprobado borraría que lo infirió una IA.
9. `Fact.proposition` como nombre de campo, para no colisionar con `Statement`/`Assertion` (nombres reservados).
10. Criterio de veredicto de §6.1 (definición operativa de PASS/FAIL/NOT_IMPLEMENTED/NOT_APPLICABLE) y la partición de 38 invariantes `INV-D-01…38` con capa responsable y veredicto posible en V0, más la tabla de mapeo a los invariantes Accepted (ADR-003 1–11, ADR-006 1/4/5/6/7) que demuestra que ninguno queda sin cobertura.
11. `REFINAMIENTO A SEÑALAR`: `Principal.principal_role` (`'lawyer'`, kernel §1.1) ≠ `Case.context_role` (`'LITIGANT'`, contexto A). El corpus usa "rol" para ambas dimensiones.

**(3) Conflictos con ADRs Accepted o con el kernel**

Ninguno. Dos tensiones **preexistentes**, registradas en sus documentos de origen, que el documento describe sin resolver ni agravar:
- Kernel §5 (`event_seq` vs `case_revision`) es ADR AMENDMENT CANDIDATE sobre ADR-004/ADR-005 y **no está aprobado**; el modelo de dominio es invariante bajo ambos modelos (`FactStatusEntry.at_case_revision` registra la revisión del evento que escribió la entrada, sea cual sea la aritmética vigente). Ninguna interfaz cambia si se aprueba.
- Kernel §3.2 (una autorización por item) vs `authorized_items[]` de ADR-005 (DECISIÓN PENDIENTE de dueños): enteramente de Application; el Domain sólo exige `authorization_id` en la entrada `ALLEGED`.

**(4) POST-V0 / POR VERIFICAR / pendientes**

- `POR VERIFICAR` con efecto directo: capacidad real de timestamps del proveedor de transcripción. **Condiciona el veredicto de INV-D-33** y, si el proveedor no los entrega, ADR-003 inv. 7 quedaría comprometido para material de audio (el ancla sólo podría ser `QUOTE` sobre el derivado). Señalado, no resuelto: depende de un spike de adapter. Secundario: soporte de UUIDv7 en Node LTS (no afecta ninguna interfaz; los ids son opacos).
- `NOT_IMPLEMENTED` declarado explícitamente: la verificación **periódica** de hashes de Sources que PF-002 menciona como control no existe en V0 (sin motor de jobs); lo verificable es la comprobación bajo demanda (INV-D-11).
- `NOT_APPLICABLE` en V0 (invariantes vigentes, sin sujeto posible): INV-D-16 (`Statement` inmutable, no materializado), INV-D-24/25/26 (`DETERMINED` y `ProfessionalDetermination`, sin productor), INV-D-27 (brazo `WITHDRAWN` del append-only), INV-D-32 (retiro de links, sin productor de `RETIRED`).
- `POST-V0`: tipología probatoria de `Evidence`; re-anclaje de fragmentos tras regenerar un derivado; productores `RecordProfessionalDetermination`, `WithdrawFact` y retiro de links; materialización de `Statement` + `ExtractStatements`; `Proposal.status = SUPERSEDED`; caché de proyecciones; todas las entidades de nombre reservado.
- `DECISIÓN PENDIENTE` heredada con efecto sobre el modelo: deduplicación física de Sources entre Cases (`Source.case_id` es consecuencia directa de la copia por caso); naming del kind de `DETERMINED`; código de rechazo de la frontera de incorporación (en V0, INV-D-28 rechaza con error semántico estable, sin condición UX propia).
- Costo declarado de la evolución a `Statement` (§7): todo es aditivo —tabla nueva + columna `statement_id?` nullable, sin backfill ni reescritura de links— salvo **un** cambio de contrato: añadir el evento `StatementsExtracted` a la lista cerrada (ADR-004 inv. 6). Se listan los tres anti-patrones que hoy volverían destructiva esa migración.