## TRUST DRIFT

**T1 · ALTA — `12-testing-strategy.md` §8.2 (tabla "Conflictos ya registrados", fila *Tamaño de la superficie MCP*)**
Cita: *"`SC-04` y `FT-013` afirman **ocho**, por precedencia del kernel §6"*.
Problema: invierte la regla de precedencia. El kernel §14 sitúa los ADRs Accepted (nivel 1) **por encima** del Technical Design (nivel 2); `05` §11.1 y ADR-010 §11 lo dicen literalmente (*"mientras ADR-010 esté `Proposed`, la superficie normativa es la de ADR-001"* = nueve). El test de superficie es el canario de ADR-001 inv. 3 y val. 7; escribirlo afirmando ocho **resuelve el conflicto de facto en el único artefacto ejecutable**, que es exactamente la "deriva silenciosa" que ADR-010 opción D declara inaceptable.
Corrección: reescribir la fila y `FT-013` para que afirmen **nueve mientras ADR-010 siga `Proposed`**, o parametrizar el conteo con una constante declarada cuyo valor normativo hoy es 9, con nota de cambio si se aprueba el amendment.

**T2 · ALTA — `10-artifact-lifecycle.md` §10, fila 1 de la tabla de trazabilidad, y §4.3 punto 3**
Citas: *"**Sí** — por construcción (§4.3), no por validación de payload externo"* y *"El modelo no puede equivocar `inputs[]`, porque no lo escribe"*.
Problema: es una garantía **estructural** que solo existe si `register_artifact` está retirado. Bajo la superficie normativa vigente (ADR-001 inv. 3, nueve tools), `inputs[]` vuelve a ser payload externo aportado por el modelo y ADR-006 inv. 3 se sostiene por **validación**, no por construcción. `10` §247 declara el conflicto pero después enuncia la garantía fuerte sin condicionarla; un lector la tomará como propiedad del diseño.
Corrección: condicionar la fila 1 y §4.3 punto 3 ("por construcción **si** se aprueba ADR-010; por validación de payload de `register_artifact` en caso contrario"), igual que `12` §8.2 debería hacer con `FT-013`.

**T3 · ALTA — `06-human-authorization.md` §7.1 (`HumanReviewOutcome`) + §7.2 regla 5**
Cita: `principal: Principal; // principalType debe ser 'HUMAN'` y *"`principal.principalType !== 'HUMAN'` ⇒ la respuesta se descarta"*.
Problema: el `Principal` del acto humano **lo aporta el transporte** y el Core solo comprueba el valor que el transporte declaró. Es la misma falacia que `05` §2 R5 rechaza para el MCP: *"un invocador que pudiera declarar quién es podría declarar ser humano"*. Con los hechos verificados registrados en `ESTADO-Y-HALLAZGOS-CRITICOS.md` §1.1 (elicitation auto-respondible por hook sin mostrar diálogo; modo Auto que delega la decisión en el propio modelo), un transporte alojado en el host puede producir `APPROVED` con `principalType='HUMAN'` sin acto humano, y el Core no lo distingue. Las reglas 1–4 blindan el *contenido* de la autorización, no su *humanidad*.
Corrección: (a) que el Core resuelva el principal del canal humano desde su propia sesión/registro y **ignore o solo contraste** el `principal` devuelto por el provider; (b) escribir el límite honesto: *"el Core no puede probar que hubo un acto humano; solo que la decisión llegó por el canal humano configurado"*; (c) convertirlo en criterio de admisión de transporte con test propio.

**T4 · ALTA — `06-human-authorization.md` §3.2 vs §7.1 (contradicción interna)**
Cita §3.2: *"Solo el canal humano crea autorizaciones, de modo que `principal_type = HUMAN` no puede ser otra cosa; **el test lo verifica resolviendo el principal**"*.
Problema: §3.2 afirma que el principal se **resuelve** (server-side); §7.1 lo **recibe** del provider. Las dos frases no pueden ser ambas verdaderas, y de cuál sea la correcta depende toda la garantía de T3. `FT-007` (`12` §…) prueba solo el brazo débil ("intento de escritura con `principal_type = AI` ⇒ rechazo"), que un transporte auto-respondedor pasa trivialmente.
Corrección: elegir una de las dos formulaciones y propagarla a §7.1, §7.2 regla 5, `06` §10 inv. 9 y `FT-007`.

**T5 · MEDIA — `06-human-authorization.md` §7.3**
Cita: *"Los criterios de admisión de un transporte siguen siendo los de ADR-005 §5 —consentimiento explícito por acto; superficie no inspeccionable ni accionable por el cliente ni por el LLM; vinculación verificable— y **este puerto los hace comprobables**: la regla 3 es la vinculación verificable"*.
Problema: sobreafirma. El puerto hace comprobable **solo el tercer criterio**. Los criterios 1 y 2 son propiedades del transporte concreto y quedan sin verificar; ADR-005 alt. 4 ya rechazó elicitation modo form justo por el criterio 1.
Corrección: *"el puerto hace comprobable el criterio 3; los criterios 1 y 2 son requisitos del transporte y quedan `POR VERIFICAR` por cada implementación"*.

**T6 · MEDIA — `08-case-context-projections.md` §4 (`INV-P-…`, argumento del presupuesto) y §5.3 — coherencia de superficie**
`08` §2.1 y §9 fundamentan garantías con *"La superficie de 8 tools (kernel §6)"* y *"Ninguna tool la escribe… verificable por el test de superficie (F16)"*, sin la marca de conflicto que sí llevan `01` §9.1, `05` §11.1, `10` §247 y `13` §654. Lo mismo en `11` INV-UX-12 (*"verificación contra el manifiesto de 8 tools"*).
Problema: garantías de no-capacidad ancladas a un número que hoy no es normativo, y sin remitir al conflicto.
Corrección: añadir en cada punto la coletilla que ya usan los documentos hermanos ("ocho según kernel §6; nueve según ADR-001 inv. 3 mientras ADR-010 siga `Proposed` — ver `05` §11.1"). La garantía sustantiva (ninguna tool escribe proyecciones) no depende del conteo y debe enunciarse sin él.

**Sub-comprobaciones de trust sin hallazgos** (verificadas explícitamente):
- Fact más allá de `PROPOSED` por el modelo: sin hallazgos. `02` §5.3 y §7 (INV-D-20/21), `03` §9 punto 5, ADR-003 inv. 2 y 11, `AT-001` son consistentes; la transición no es representable en Domain.
- Token o secreto de autorización hacia el modelo: sin hallazgos. `05` §2 R3/R4, ADR-008 §…("cero tokens"), `06` §6, `09` §2.5 (exclusión de `authorization_id` hacia la superficie), `03` §11.3.
- Escritura de `Source` por el modelo: sin hallazgos. ADR-006 inv. 4, `FT-013` ("no figura ninguna operación de escritura o borrado de `Source`").
- Marcar algo como verificado: sin hallazgos. ADR-011 §10 e INV-L-14 prohíben columna/campo/mensaje `verified|authentic|validated`; `verify_legal_source` fuera de superficie; PF-004 por ausencia.
- Rutas de filesystem o URLs en tools: sin hallazgos. `05` §2 R1/R2 (resolución por enumeración, sin concatenación ni symlinks), `03` §4.4, `AT-012`, nivel N5 de `12`. Defensa doble y probada por separado.
- Garantía que dependa de un prompt o `SKILL.md`: sin hallazgos. `01` §2.2 punto 2, `10` §…("el gate no vive en el skill… ni en el prompt"), `12` §3.6, `08` §4.1 (presupuesto como política, no prompt).
- Conflicto 8 vs 9 **declarado**: sí, correctamente y sin resolver, en kernel §6 (como propuesta), `ESTADO` §6.1, `01` §9.1, `05` §11.1, ADR-010 §11 (con opciones A–D y recomendación explícitamente no vinculante), `13` §654. El defecto no es la declaración sino su no propagación a `12` (T1), `10` (T2) y `08`/`11` (T6).

---

## PROVENANCE DRIFT

**P1 · ALTA — `04-persistence-model.md` §3.3 (`TABLE evidence_links`) vs `07-provenance-and-locators.md` §7 (INV-L-02, INV-L-06, INV-L-07)**
Cita `04`: `selector_kind enum{TEXT_POSITION,TEXT_QUOTE,TIME_RANGE,PAGE_RANGE} NOT NULL` + `selector json NOT NULL` → **un solo selector por link**.
Cita `07`: `selectors` en plural, INV-L-02 (*"`selectors` nunca vacío"*), INV-L-06 (*"un fragmento sobre texto lleva `TEXT_QUOTE` con `prefix` y `suffix`"*), tabla §3.3 (*"`TEXT_POSITION` **+** `TEXT_QUOTE`"* obligatorios), e INV-L-07 (*"si `TEXT_POSITION` y `TEXT_QUOTE` discrepan ⇒ fallo duro"*).
Problema: con el esquema de `04`, **INV-L-06 e INV-L-07 no son representables**: no se pueden persistir los dos selectores de un mismo link, y por tanto la comprobación cruzada que detecta la deriva del ancla (`L-06`) no tiene sustrato. Es el mecanismo que impide que una cita apunte a otro texto tras una regeneración. `07` §9.2 declara D1–D4 y **omite esta divergencia**.
Corrección: registrarla como D5 en `07` §9.2 y proponer una de las dos formas: tabla hija `evidence_link_selectors(link_id, kind, selector json)`, o `selectors json` (array) con índice derivado por `kind`.

**P2 · MEDIA — `04-persistence-model.md` §3.3 — falta el CHECK que materializa INV-L-04**
`07` §3.3 e INV-L-04 fijan: `anchored_in='DERIVED_REPRESENTATION' ⇒ ningún selector es TIME_RANGE ni PAGE_RANGE`, con la razón exacta que pide el foco: *"si aparecieran como selector de un transcript estarían midiendo la línea de tiempo del **derivado**, que es exactamente lo prohibido"*. El DDL de `04` §3.3 permite `anchor_via_derivation NOT NULL` junto con `selector_kind = 'TIME_RANGE'`, y `07` §7 asigna INV-L-04 **solo a Domain**, pese a que la misma tabla `facts` (§3.2) sí lleva `CK(...)`.
Corrección: añadir en `04` §3.3 `CK( anchor_via_derivation IS NOT NULL => selector_kind IN ('TEXT_POSITION','TEXT_QUOTE') )` y mapear INV-L-04 a "Domain + Infrastructure".

**P3 · MEDIA — `08-case-context-projections.md` §5.3 (scope `evidence`) y §6.2**
Citas: `provenance: { provenance_kind: 'EXTERNAL_SOURCE'; principal_type: 'HUMAN'|'SYSTEM'; … }` y *"incorporar una evidencia por orden de la usuaria es `principal_type = HUMAN` con `provenance_kind = EXTERNAL_SOURCE` (kernel §1.4)"*.
Problema: contradice frontalmente `05` §3.1 y `09` §2.3, que **contratan `SYSTEM`** para `ingest_evidence` con razón expresa —*"el canal MCP no autentica a nadie… escribir `HUMAN` sería una mentira permanente en el log"*— y contradice `FT-002` (`principal_type = SYSTEM`). Es deriva de trust *y* de provenance: atribuye autoría humana a un acto originado en el cliente no confiable. No figura en las divergencias declaradas de `08` §12.3.
Corrección: fijar `principal_type: 'SYSTEM'` en el tipo de §5.3 y reescribir el párrafo de §6.2 (el argumento a favor de `ProposalReviewed` como ancla del cursor **se refuerza**, no se debilita, con `SYSTEM`).

**P4 · MEDIA — `08-case-context-projections.md` §5.2 (scope `facts`)**
Cita: `origin: { proposal_id: Uuid; proposal_item_id: Uuid } | null;`
Problema: en V0 **todo Fact nace en el commit de un `ProposalItem`** (`02` §5.2: el Core escribe las entradas `PROPOSED` y `ALLEGED` en la misma transacción, con el `origin_ref` del item), de modo que `null` no tiene productor posible. Declararlo nullable legitima en el contrato un Fact **sin camino hasta sus inputs** y obliga al consumidor a manejar ese caso.
Corrección: hacerlo no nullable en V0, o nombrar el productor de `null` y la razón (y entonces declararlo como límite epistémico, no como opción del tipo).

**P5 · MEDIA — `04-persistence-model.md` §2.6 y §3.2 — `bbox` en `original_locator`**
Cita: `original_locator json NOT NULL -- coordenadas SOBRE EL ORIGINAL (ms / página / bbox)`.
Problema: `bbox` es coordenada espacial declarada **fuera de V0** (`07` §3.9 y §9.6) y no es una coordenada de la línea de tiempo ni de la paginación del original en el sentido de ADR-003 inv. 7. Ya está señalada por `07` §9.2 D3, pero sigue en el texto de `04` en dos lugares.
Corrección: retirar `bbox` de ambas enumeraciones de `04` o marcarlo `POST-V0` en línea.

**P6 · MEDIA — nombre del hash de anclaje: tres nombres para el mismo campo**
`04` §2.5 lo llama `source_version_hash` (*"no implica una tabla: es el hash de la representación exacta sobre la que el selector es válido"*), `04` §3.3 lo declara como `anchor_content_hash`, `02` §2.5 y `07` §3.1 lo llaman `representation_hash`, y `05` §6.5 vuelve a `fragment { source_version_hash, selector }`.
Problema: `source_version_hash` **nombra como "versión del Source" el hash de un derivado**, que es precisamente la confusión original↔derivado que ADR-003 inv. 8 y ADR-006 inv. 5 prohíben; `04` §2.5 tiene que dedicar un párrafo a desmentir la lectura que el propio nombre induce. `07` §9.2 no lo registra como divergencia.
Corrección: fijar `anchor_content_hash` como nombre único, propagarlo a `02` §2.5, `05` §6.5 y `07` §3.1, y añadirlo como D6 en `07` §9.2.

**P7 · BAJA — `03-application-use-cases.md` §4.11, opción (a)**
Cita: *"el `declared_origin` adicional se registra en el **Tool Invocation Log** (operacional, no canónico)… coste: esa procedencia es podable y no reconstruye estado"*.
Problema: la opción marcada como "V0 por defecto" satisface ADR-006 inv. 7 (*"la procedencia adicional se registra"*) con un registro que la política de retención de `09` §6 puede borrar. El coste está dicho, pero no se dice que la consecuencia es que **un invariante Accepted queda satisfecho de forma temporal y podable**.
Corrección: añadir esa frase al texto de la opción (a) y marcar el punto en la matriz de cobertura de invariantes Accepted de `07` §7.1 / `12` §7 como cobertura degradada mientras la decisión siga pendiente.

**Sub-comprobaciones de provenance sin hallazgos**:
- Timestamps de audio referidos al **original**: sin hallazgos de contenido. `07` §3.2, §3.3 y §3.6 (`t=0` en el primer instante del material incorporado, `ORIGINAL_TIME_RANGE`, prohibición explícita del selector temporal sobre el derivado, y **restricción del adapter en vez del invariante** si el proveedor no cumple), `05` §6.4 regla dura, `04` §2.6 (`original_locator NOT NULL`) y `13` §6 (mapa de timestamps sobre la línea de tiempo del original) son coherentes. El defecto es solo de *enforcement* en el esquema (P2).
- `inputs[]` por `entity_id + content_hash` y nunca por nombre de archivo: sin hallazgos. `10` §2.3 lo argumenta y §7 fila 2 lo prueba; `09` §3.2 (`ArtifactRegisteredP`) y `04` §3.4 (`artifact_inputs`) lo materializan; `03` §9.7 lo computa en el Core.
- Integridad ≠ autenticidad: sin hallazgos. ADR-011 §10 y INV-L-14 (lista de nombres prohibidos en schema), `07` §6, `02` §3.2, `05` §6.4, `11` §… (plantilla literal *"acredita integridad desde la incorporación; no dice nada sobre la autenticidad"*), `09` §4.6 (*"tamper-evident, no tamper-proof"* como frase normativa). Es el punto mejor blindado del corpus.
- Cadena artifact/Fact → inputs: sin hallazgos más allá de P4. `fragment_ref` opaco emitido por el Core (`05` §6.5) hace estructuralmente imposible fabricar un ancla; `08` §9.2 exige trazabilidad total de identificadores contra el Tool Invocation Log.

---

### Nota transversal

Los cuatro hallazgos de mayor gravedad (T1, T2, T3, T4) comparten un patrón: **una garantía se enuncia como estructural cuando en realidad depende de algo no aprobado o no verificable** — un amendment pendiente (T1, T2) o una afirmación del transporte (T3, T4). Ninguno es un error de razonamiento; los cuatro son deriva de *modalidad*: propuesta escrita como hecho.