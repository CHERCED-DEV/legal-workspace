**Nota de estado.** Los 18 documentos de la lista existen y fueron leídos. Durante la revisión se escribieron además `14-repository-layout.md`, `15-product-floor-proposal.md`, `16-open-implementation-decisions.md` y `ADR-007`; no estaban en mi lista y solo los consulté para verificar dos hallazgos (se indica dónde).

---

## A. HALLAZGOS DE UX DRIFT (17, ordenados por gravedad)

### ALTA

**H-01 · Los mensajes que no nacen de una condición no tienen catálogo, clave, plantilla ni test**
`11-ux-condition-catalog.md` §1.1, §4.1, §4.3, §5.2 · `05-mcp-contract.md` §4.3 · `12-testing-strategy.md` §3.1, §3.3 · `ADR-006` §100 · `ADR-010` §120.
Cita: «lo que llega a la profesional es **mensaje de producto**, no condición tipada» (11 §3.7); «la única defensa es que la plantilla del resultado vacío declare su alcance» (11 §4.1).
Problema: tres de los cuatro pares epistémicos se entregan **fuera** del pipeline. `hits: []` no lleva condición; la coincidencia de hash no emite condición (11 §4.3 pt.3); las capacidades inexistentes (`verify_legal_source`, acreditar, modificar `Source`) y 6 `ErrorCode` MCP + 14 de Application llegan como «mensaje de producto». Ninguno de esos textos tiene `message_key`, ninguno entra en el presupuesto de 10 plantillas (§6.2), ninguno lo cubre `INV-UX-11` (que solo exige plantilla para las filas del catálogo) ni el test léxico `T-UX-04` (que corre «sobre el catálogo de plantillas»). Consecuencia dura: cuando la tool no existe, el Core **nunca es invocado**, no viaja `rendered`, y el texto lo compone el modelo — exactamente el modo de fallo que PF-004 existe para impedir.
Corrección: añadir a `11` una sección **Catálogo cerrado de mensajes de producto** con claves `prod.<situación>` sometidas a `INV-UX-04`, `INV-UX-05`, `INV-UX-11`, `INV-UX-12` y a `T-UX-04/05`. Mínimo V0: `prod.search.no_hits`, `prod.integrity.match`, `prod.capability.absent.verify_legal_source`, `prod.capability.absent.determine_fact`, `prod.capability.absent.modify_source`, `prod.not_incorporated`, `prod.startup.integrity_failure`. Gravedad: **ALTA**.

**H-02 · El mecanismo estructural de `retrieval failed ≠ no evidence` está roto en Application**
`03-application-use-cases.md` §7.3: `interface SearchCaseOutput { hits: SearchHit[]; truncated: boolean; }`.
Problema: `05` §6.3 y `11` §4.2 fijan `hits: SearchHit[] | null`, con `null` —«**NO `[]`**»— como la garantía de tipo que hace la confusión imposible (`INV-UX-06`). El contrato de Application, que es **donde se emite la condición**, no admite `null`: el mecanismo que `11` presenta como estructural no existe en la capa que lo produce.
Corrección: `03` §7.3 → `hits: SearchHit[] | null`, con nota explícita «`null` ⇔ `SEARCH_INCONCLUSIVE`; `[]` ⇒ ninguna condición»; y unificar `truncated` (03) con `exhaustive` (05), que son booleanos inversos con el mismo propósito. Gravedad: **ALTA**.

**H-03 · La estrategia de pruebas no contiene la capa de presentación: cero referencias al catálogo UX**
`12-testing-strategy.md` §2.1 (pirámide de siete niveles), §6 (trazabilidad).
Problema: `12` no menciona ni una vez `11-ux-condition-catalog.md`, `T-UX-01..10`, `INV-UX-01..12`, «plantilla» ni «léxico». Los siete niveles van de `SC` a `N7` sin nivel de presentación. La afirmación central de `11` §10 —«ningún mensaje eleva la certeza… porque una plantilla que lo intente **no pasa la build**»— no tiene test en el documento que gobierna los tests. (`14-repository-layout.md` §409 ya ubica `T-UX-05-completitud-de-plantillas.test.ts`, lo que confirma que el hueco es de `12`, no del diseño.)
Corrección: añadir a `12` un nivel de presentación (o incorporarlo a `SC`, ya que `T-UX-04/05/07` son comprobaciones estructurales sobre datos), incorporar `INV-UX-01..12` al bloque de trazabilidad §6 y ejecutar la unificación de numeración `AT-xxx ↔ T-UX-xx` que `11` §7.2 deja `POR VERIFICAR`. Gravedad: **ALTA**.

**H-04 · `11` promete una medición de deformación que el benchmark no define y que un invariante del corpus impide**
`11-ux-condition-catalog.md` §6.4 y `T-UX-10` («el benchmark sintético revisa las transcripciones de sesión contra el lexicón prohibido y **mide** la tasa de deformación») vs. `13-synthetic-benchmark.md` §16.1 y §16.8–16.11.
Problema: las fuentes de datos del harness son Case Event Log, Tool Invocation Log, proyecciones y `expected/`; **ninguna es la transcripción de sesión**. Las métricas no incluyen deformación léxica, y las `PA-01..PA-08` cubren afirmaciones sobre el caso, no elevación de certeza («quedaron establecidos», «documento auténtico», «no existe»). Además `04` §4 #29 / `12` §6.3 fijan que **el chat crudo nunca se persiste**. La única verificación honesta de la regla suprema queda sin instrumento.
Corrección: o bien añadir a `13` §16 una métrica `message_fidelity_deformation_rate` con captura de transcripción **declarada del lado del harness**, fuera del estado canónico y con retención propia; o bien retirar la afirmación de `11` §6.4 y declarar la fidelidad del mensaje final como **NO MEDIBLE en V0**, coherente con `12` §6.5 («Que la usuaria reciba el texto de una condición | Fuera de la suite»). Gravedad: **ALTA**.

**H-05 · `OPERATION_NOT_PERMITTED` se usa con tres semánticas incompatibles**
`11` §3.7 y `T-UX-07` («en V0 el conjunto está vacío, de modo que la condición **no puede emitirse**») · `03` §10.12 («`OPERATION_NOT_PERMITTED` si el canal invocante no es el humano o el principal no es `HUMAN`») · `12` §6.5 («`PASS|FAIL` **por construcción del perfil** — Verificable con un perfil sin capability»).
Problema: `11`, `05` §8.3, `ADR-006` §100 y el addendum B.6 reservan el código a **capacidad existente vetada por política**; `03` lo emite para una invocación por un canal que no es la superficie del modelo (`ReviewProposal` no está en el manifiesto: no hay capacidad que vetar), y `12` presume perfiles que `03` §2.10 y `11` §2.4 declaran inexistentes en V0. El daño es el que `11` §3.7 nombra: «Confundirlas haría creer que existe una palanca que podría activarse».
Corrección: en `03` §10.12, sustituir por un `ErrorCode` de Application (p. ej. `E_CHANNEL_NOT_PERMITTED`, añadido a la lista de §0.3) y declarar que la respuesta a la usuaria es mensaje de producto; en `12` §6.5, cambiar el veredicto a `NOT_TESTED` / «por siembra», alineado con `T-UX-07`. Gravedad: **ALTA**.

**H-06 · El único mensaje aprobado literalmente por los dueños no puede renderizarse: falta su parámetro en todos los sitios de emisión**
`11` §3.5 (payload `{ proposal_id, item_ids[], pending_item_count }`; «La plantilla usa exclusivamente `pending_item_count`») vs. `03` §9.12, §10.12, §11.13 y `05` §4.3, §11.2 (`HUMAN_REVIEW_REQUIRED {proposal_id}`) y `06` §5.2, `12` §3.1 (`{proposal_id, item_ids[]}`).
Problema: ningún sitio de emisión del corpus lleva `pending_item_count`. La plantilla «Preparé 12 hechos candidatos…» (DECISIÓN APROBADA, literal) no tiene de dónde sacar el 12, y `INV-UX-04` prohíbe sustituirlo por identificadores.
Corrección: fijar el payload de `HUMAN_REVIEW_REQUIRED` en los tres campos y corregir `03` y `05`; añadir invariante «todo sitio de emisión porta los `params` que consume la plantilla de su ocasión», verificable en `T-UX-01`. Gravedad: **ALTA**.

### MEDIA

**H-07 · Jerga de ingeniería en un mensaje humano: la palabra «hash»**
`11` §3.8, mensaje propuesto de `INTEGRATION_ERROR`: «la grabación quedó incorporada **con su hash** y la transcripción figura como fallida».
Problema: viola tres reglas del propio documento — `INV-UX-04` («ningún mensaje humano contiene… hashes»), §6.3 («Hashes, en cualquier forma o longitud» prohibidos) y §4.3 pt.2 («Ningún hash se muestra jamás a la usuaria… invita a leerlo como sello de autoridad») — y `08` §1.3 («Nunca contiene `content_hash` de ningún tipo»). Además es el único mensaje del catálogo que fallaría `T-UX-04` hoy.
Corrección: «la grabación quedó incorporada y su contenido no ha cambiado desde entonces». Gravedad: **MEDIA**.

**H-08 · `07` asigna categorías de presentación a situaciones sin código del catálogo, y se contradice consigo mismo**
`07-provenance-and-locators.md` §6.4, filas «Mismatch de hash → `CANNOT_DO_THAT`», «Fragmento no re-anclable → `NEEDS_YOUR_DECISION`»; §5.5 («`ORIGINAL_COORDINATE_DRIFT` … `SOMETHING_CHANGED`»).
Problema: (a) el catálogo es cerrado en siete códigos y `family`/`presentation_category` son **derivadas del código** (`11` §1.4, `INV-UX-02`); asignar categoría sin código viola la regla de dirección única («la presentación jamás inventa una condición», `11` §1.3). (b) `07` §5.6 recomienda reutilizar `UNCERTAIN_FRAGMENT` para el fragmento no re-anclable, cuya categoría fija es `LIMITED_CERTAINTY` — contradiciendo el `NEEDS_YOUR_DECISION` de su propio §6.4. (c) `NEEDS_YOUR_DECISION` exige «entrada al canal de revisión humana» (`11` §5.1), que para re-anclaje no existe en V0.
Corrección: en §6.4, retirar la columna de categoría en las filas sin código y rotularlas «mensaje de producto» o «pendiente de §5.6»; si se ratifica la reutilización, usar `LIMITED_CERTAINTY`. Gravedad: **MEDIA**.

**H-09 · Plantilla para una capacidad que V0 no tiene**
`07` §6.4, fila «Verificación periódica de integridad correcta → *"Los archivos del expediente conservan el contenido con el que se incorporaron"*».
Problema: `12` §6.5 declara la verificación periódica `NOT_IMPLEMENTED` («no hay job ni planificador en V0») y `04` §7 solo garantiza la comprobación bajo demanda. Una plantilla para un evento sin productor contraviene `INV-UX-12`.
Corrección: marcar la fila `POST-V0` o reescribirla ligada a la comprobación bajo demanda que sí existe. Gravedad: **MEDIA**.

**H-10 · El fallback de plantilla muestra un identificador interno a la usuaria**
`11` §6.5: «locale pedido → `es-CO` → mensaje genérico de la **categoría** + `invocation_id`».
Problema: `INV-UX-04` prohíbe identificadores en mensajes humanos y §6.3 prohíbe «Identificadores de entidad de cualquier tipo». El fallback es precisamente el camino menos revisado, y hoy incumple el invariante del propio documento.
Corrección: o declarar `invocation_id` excepción explícita y nombrada («referencia de soporte»), con formato estable, en `INV-UX-04` y §6.3; o retirarlo del texto y encaminar el diagnóstico por un canal de soporte. Gravedad: **MEDIA**.

**H-11 · El contrato `Condition` tiene tres formas distintas en tres documentos del mismo nivel**
`03` §0.2 (`TypedCondition`: `code`, `family`, `params`, `presentation_category`) · `05` §4.1 (`conditions: Condition[]`, sin definir el tipo) · `11` §1.4 (once campos, incluidos `severity`, `blocking`, `occasion`, `message_key`, `rendered`, `attached_to`).
Problema: `11` declara «esta forma única, válida en ambos planos», pero Application emite un subconjunto que **no puede transportar** `blocking` (base de `INV-UX-03`), `occasion` (base del presupuesto de plantillas §6.2) ni `attached_to` (base de `INV-UX-10`, la adherencia de `ANALYSIS_STALE` al artifact).
Corrección: fijar la forma de `11` §1.4 como única y corregir `03` §0.2 y `05` §4.1 por referencia, o declarar explícitamente qué campos añade el adapter y con qué dato. Gravedad: **MEDIA**.

**H-12 · `memory.md` expone relojes internos en un formato legible por una persona**
`08-case-context-projections.md` §7.2: «Encabezado: etiqueta, **revisión, `event_seq`** — Puede omitirse: **No**»; §7.5 contempla «que la profesional lea el estado del caso sin abrir el chat».
Problema: `11` §3.6 («los relojes internos no se muestran… Un número de revisión no tiene significado profesional; mostrarlo es exposición de ingeniería con apariencia de precisión») y §6.3 los prohíben. `08` no declara que `memory.md` sea de audiencia exclusivamente modelo, y §7.6 deja la audiencia humana `POST-V0` sin cerrar la puerta.
Corrección: declarar en §7.1 que `memory.md` es **artefacto dirigido al modelo** y que cualquier renderizado para audiencia humana pasa por el pipeline de presentación con los relojes suprimidos. Gravedad: **MEDIA**.

**H-13 · El registro consolidado de decisiones abiertas omite once de las doce aprobaciones UX**
`11` §8.5 (doce decisiones) vs. `16-open-implementation-decisions.md` §3, §4 y §5.
Problema: `16` no contiene ninguna referencia a `11`; de las doce solo registra `NOT_INCORPORATED`. Quedan fuera dos que **tocan contratos de otros documentos**: el campo `coverage` en `search_case` (§8.5 #8 — sin él la plantilla de resultado vacío no puede decir la verdad completa cuando hay derivaciones fuera de `READY`) y la unificación del formato de rango temporal con `locator_summary` (#9 — un rango mal interpretado envía a escuchar el tramo equivocado). `05` §14 tampoco registra `coverage` en su propia lista de pendientes: el contrato de `search_case` puede congelarse sin él.
Corrección: incorporar las once a `16` §4/§5 con su criterio de bloqueo, y añadir `coverage` a la lista de pendientes de `05` §14. Gravedad: **MEDIA**.

### BAJA

**H-14 · La matriz adversarial no declara la subafirmación no verificable de `AT-009`**
`12` §3.1, fila `AT-009` («presentarlo en una salida final») vs. `10-artifact-lifecycle.md` §8.4 (`AT-009.d`: «**DECLARADO NO VERIFICABLE EN V0**»).
Problema: leído solo `12`, `AT-009` parece cubierto de extremo a extremo, cuando una de sus cuatro afirmaciones (gate de salida final) no tiene superficie que ejercitar.
Corrección: reproducir en `12` la descomposición C1–C4 / `AT-009.a–d` con su veredicto declarado. Gravedad: **BAJA**.

**H-15 · Una categoría de presentación con flecha no es un valor del enum, y contradice el mapa de `11`**
`03` §0.3, fila `E_DERIVATION_UNAVAILABLE`: categoría «`LIMITED_CERTAINTY`→`CANNOT_DO_THAT`» vs. `11` §5.2 («los 14 `ErrorCode` de `03` §0.3 → `CANNOT_DO_THAT`, salvo `E_ITEM_CONTENT_MISMATCH`»).
Corrección: elegir un valor único (`CANNOT_DO_THAT`, coherente con `11`) o justificar la doble ocasión con dos plantillas contadas en §6.2. Gravedad: **BAJA**.

**H-16 · Registro de tratamiento mezclado en textos ya aprobados**
`11` §8.2: `HUMAN_REVIEW_REQUIRED.proposed` tutea («necesito que **revises**»), el resto usa «usted».
Problema: ya está registrado como DECISIÓN PENDIENTE, pero hasta resolverse conviven en un solo flujo (`propose_facts` → commit bloqueado) dos mensajes aprobados con registros distintos.
Corrección: decidir el `register` por defecto de `es-CO` en la misma sesión que las demás aprobaciones. Gravedad: **BAJA**.

**H-17 · Nombres divergentes en el resultado de búsqueda**
`03` §7.3 (`excerpt`, `truncated`) vs. `05` §6.3 (`snippet`, `exhaustive`, `locator_summary`).
Problema: `truncated`/`exhaustive` son booleanos **inversos** con el mismo propósito: riesgo de inversión silenciosa que la plantilla de resultado vacío no detectaría.
Corrección: adoptar los nombres de `05` en `03`. Gravedad: **BAJA**.

**Categorías de mi foco sin hallazgos propios:** `AI inferred ≠ verified` está bien sostenido de forma estructural (`11` §4.4, `02` §5, PF-001/PF-004, `AT-001`, ausencia de `verify_legal_source`); su única fisura es la vía de entrega descrita en H-01.

---

## B. COMPLETITUD CONTRA EL «DEFINITION OF DONE» (12 preguntas)

| # | Pregunta | Veredicto | Dónde está la respuesta |
|---|---|---|---|
| 1 | Qué entidades existen en V0 y cuáles no | **SÍ** | `02` §3 (nueve entidades), §3.8 (`Statement` definido y no materializado), §7, §8; kernel §15 |
| 2 | Qué use cases existen | **SÍ** | `03` §1 (once, con puerto, clase, tx, eventos y revisión); kernel §7 |
| 3 | Qué se persiste y dónde | **SÍ** | `04` §1 (cuatro almacenes), §3 (DDL), §7 (filesystem y content-addressing); `09` §1 (dos persistencias) |
| 4 | Qué operaciones puede solicitar el modelo | **PARCIAL** | `05` §6 y `ADR-010` responden «ocho tools», pero el **CONFLICTO con ADR-001 Accepted (nueve)** sigue abierto y por precedencia manda el ADR (`ESTADO` §6.1; `16` OD-02). Hasta que los dueños decidan, el manifiesto —y con él `FT-013`— no está fijado |
| 5 | Qué puede decidir Claude y qué necesita humano | **SÍ** | `06` completo (§1 ciclo, §5 las cinco guardas, §6 naturaleza server-side); `ADR-008`; kernel §3 |
| 6 | Cómo se vuelve desde un Fact a los bytes originales | **SÍ** | `07` §1 (cadena `Fact → EvidenceLink → fragment → DerivedRepresentation → Source`), §3 (locator), §1.5 (re-hash en lectura); `ADR-011` |
| 7 | Qué ocurre con trabajo creado contra contexto viejo | **PARCIAL** | `03` §11.6, `06` §5.4 y `11` §3.6 describen `REVISION_CHANGED` + `PRESERVED_FOR_RECONCILIATION`. Falta cerrar dos cosas: la aritmética de revisiones (`16` OD-01), que decide si el mecanismo dispara **espuriamente** (`11` §3.6), y el estatuto de `ProposalPreservedForReconciliation`, que `03` §1 emite como evento y el kernel §8.1 no lista (`06` §5, `16` §5) |
| 8 | Cómo se detecta obsolescencia | **SÍ** | `10` §5 (dos clases), §6 (detección dentro de la tx del mutador, tres `reasons` y cuáles tienen productor); `03` §12; `11` §3.2 |
| 9 | Cómo se reabre un Case sin conversación anterior | **SÍ** | `08` §9 (`AT-010` con sus asserts), §5.1 `overview`, §6 `changes_since`, §7 `memory.md` |
| 10 | Cómo se evita acceso directo al Canonical State | **SÍ** | `08` §1.2 (tres capas, con la tercera declarada como la que aguanta), `ADR-002`, `01` §6, `05` §2 (R1–R6), `12` §3.5. El riesgo B-04 es de anfitrión, no un hueco de la respuesta |
| 11 | Cómo se convierten condiciones técnicas en lenguaje profesional | **PARCIAL** | `11` responde de forma ejemplar para las **siete condiciones** (pipeline, cuatro categorías, lexicón de techo, presupuesto de ocasiones). No responde para lo que **no** es condición: mensajes de producto, resultado vacío, integridad de hash y ~20 `ErrorCode` (H-01), y `07` §6.4 añade plantillas paralelas fuera del catálogo (H-08). Además el mecanismo que lo haría comprobable no está en la estrategia de pruebas (H-03) ni medido en el benchmark (H-04) |
| 12 | Cómo se demuestra que no puede romperse por las rutas adversariales conocidas | **PARCIAL** | `12` §3 (`AT-001..AT-013` con nivel, invariante y condición) y §3.5 (declaración honesta de lo **no** cubierto) + `13`. Queda abierto: `AT-009.d` sin superficie (`10` §8.4); PF-004 sin `AT` propio (`12` §3.7); `OPERATION_NOT_PERMITTED`, `UNCERTAIN_FRAGMENT` e `INTEGRATION_ERROR` sin disparador real; ninguna prueba de la capa de presentación; y la ruta decisiva —escritura del host sobre `private-state/`— depende de B-04, `INCONCLUSIVE` y declarado **BLOQUEANTE** |

---

## C. POR QUÉ EL TECHNICAL DESIGN NO ESTARÍA CERRADO

Cuatro preguntas en **PARCIAL**, y ninguna lo está por falta de trabajo:

1. **Q4** depende de una decisión de los dueños ya analizada (8 vs 9 tools).
2. **Q7** depende de otra (modelo A/B de revisión) más la ratificación de un evento de lista cerrada.
3. **Q11** es el único hueco **de diseño**, no de decisión: el corpus tiene un pipeline riguroso para las condiciones y **ningún** pipeline para los mensajes que no nacen de una condición — que son precisamente los de mayor carga jurídica (capacidad inexistente, resultado vacío, integridad). H-01 lo cierra sin ampliar el catálogo cerrado.
4. **Q12** no puede cerrarse mientras B-04 siga `INCONCLUSIVE` y mientras la capa de presentación no tenga nivel de prueba (H-03) ni instrumento de medición (H-04).

Las seis correcciones ALTA son todas locales y no requieren reabrir ningún ADR Accepted: cuatro son ediciones de contrato en `03`, `05` y `12`; dos son ampliaciones aditivas de `11` y `13`.