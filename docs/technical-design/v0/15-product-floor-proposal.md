# 15 — Product Floor V0: propuesta de las cinco políticas no relajables

**Estado del documento:** propuesta técnica de la fase TECHNICAL DESIGN V0.
**Estado de las políticas: `PROPOSED`.** Ninguna política de este documento está `Accepted`. Lo que sí está aprobado es el **mecanismo** del piso (ver §1.2); el **contenido** de la lista es propuesta y requiere decisión explícita de los dueños.
**Precedencia (kernel §14):** ADRs Accepted (001–006) > Technical Design V0 (incl. `00-technical-kernel.md`) > `principles.md` > glosario > addenda > spikes.
**Derivado de:** kernel técnico v0.4 §12 (las cinco políticas y el formato), §10 (familias de condiciones), §11 (identidad y hashing), §13 (regla de dependencias), §14 (precedencia); `principles.md` (anexo Product Floor v0); `boundaries.md` §2.2, §6, §10; ADR-001…ADR-006 (Accepted).

Este documento **no inventa políticas**. Toma las cinco de kernel §12 **literalmente**, las amplía con el mecanismo concreto de enforcement (capa, punto de aplicación, artefacto de código o de esquema que lo materializa) y con los identificadores de prueba consolidados en `12-testing-strategy.md`. Donde una ampliación es mía, va etiquetada `PROPUESTA DEL TECHNICAL DESIGN` y entra en §9.

---

## 1. Qué es el Product Floor y qué no es

### 1.1 Definición operativa

El **Product Floor** es el conjunto cerrado de políticas que **la configuración de un cliente no puede relajar**, aplicadas por el Core en los gates de commit y de export, con independencia del host, del modelo y de la configuración cargada.

Tres precisiones que evitan los tres malentendidos habituales:

1. **No es una lista de buenas prácticas.** Cada política nombra un riesgo del dominio jurídico que, de materializarse, produce un daño que el producto existe para evitar. Una política que no nombre un daño concreto no pertenece al piso.
2. **No es el catálogo de invariantes.** El Domain tiene decenas de invariantes (`INV-D-01`…`INV-D-33`, `INV-H-01`…`INV-H-13`, `INV-UX-01`…`INV-UX-08`). El piso es el subconjunto **cuya relajación por configuración está prohibida**. Un invariante puede ser durísimo y no estar en el piso porque nadie ha propuesto nunca configurarlo.
3. **No es un mecanismo nuevo.** Ninguna de las cinco introduce código que no exista ya por otra razón. El piso **declara** que ese código no es negociable; el enforcement lo hacen el Domain, la Application, la Infrastructure y la ausencia de superficie MCP, cada uno donde ya vive.

### 1.2 Qué está aprobado y qué no — distinción obligatoria

| Elemento | Estado | Fuente |
|---|---|---|
| **El mecanismo:** existen políticas que el cliente no puede relajar; la configuración solo endurece | **DECISIÓN APROBADA** | Cita literal de los dueños, §21 del prompt de consolidación, recogida en addendum v0.3 B.4: *"Existirán políticas de seguridad/integridad que el cliente no puede relajar. La configuración puede endurecerlas. No debilitarlas."* |
| **El contenido:** que las políticas sean **estas cinco** y no otras | **`PROPOSED`** | kernel §12 (propuesta), este documento |
| **La sexta candidata** (auditoría) | **DECISIÓN PENDIENTE de los dueños** | kernel §12.6; §6 de este documento; `09-events-and-audit.md` §8.3 |
| **El enforcement concreto** (capa y mecanismo de cada política) | **PROPUESTA DEL TECHNICAL DESIGN** | §3 de este documento |

`principles.md` (anexo) califica el contenido como *"primer conjunto universal, abierto a ampliación"*. Este documento lo respeta: propone cinco, no las cierra, y hace visible el hueco (§6).

### 1.3 Regla de admisión de una política al piso

`PROPUESTA DEL TECHNICAL DESIGN.` Para que una política entre al piso debe cumplir las cuatro condiciones:

| # | Condición | Por qué |
|---|---|---|
| A1 | Nombra un **riesgo del dominio**, no un riesgo de ingeniería | Si el daño es "el sistema se corrompe" y no "la profesional afirma algo falso ante un juez", el sitio es el catálogo de invariantes, no el piso |
| A2 | Existe un **punto de aplicación identificable** en el Core | Una política que solo se cumple si el modelo colabora no es una política: es una instrucción (principio 3) |
| A3 | Es **comprobable** por al menos un test determinista, o su cumplimiento es verificable por **ausencia de superficie** | Sin esto, "se cumple" es una afirmación sin sujeto |
| A4 | Alguien podría querer **configurarla en contra** | Es lo que distingue el piso de un invariante cualquiera. Si nadie la relajaría nunca, declararla no negociable no añade nada |

Las cinco de kernel §12 cumplen A1, A2 y A4. **A3 se cumple con matices declarados** en PF-002 (la verificación periódica es `NOT_IMPLEMENTED` en V0), PF-004 (se comprueba por ausencia, sin `AT` propio) y PF-005 (depende del mecanismo de configuración efectiva, `POR VERIFICAR`). Los matices se escriben, no se disimulan.

---

## 2. Formato

El kernel §12 fija cinco campos por política y este documento los conserva **con sus nombres en inglés y su orden**:

```text
PF-XXX
Name
Risk prevented
Enforced in
Configuration may relax?
How tested
```

**Ampliación de este documento, sin alterar el enunciado:** bajo la tabla de cada política se añaden tres bloques.

- **Mecanismo concreto** — qué artefacto materializa la política en cada capa (regla de transición, constraint, ausencia de tool, validación de schema), con referencia al documento donde está especificado.
- **Qué NO cubre** — el límite honesto de la política. Sin este bloque, una política se lee como si cubriera todo lo adyacente.
- **Prueba** — identificadores `AT-xxx` / `FT-xxx` / `T-UX-xx` consolidados en `12-testing-strategy.md` §3 y §4, con su nivel y su veredicto disponible en V0.

Los enunciados en inglés (`Name`) son **literales de kernel §12** y no se traducen: son el identificador legible de la política.

---

## 3. Las cinco políticas

### 3.1 PF-001

| Campo | Valor |
|---|---|
| **PF-001** | — |
| **Name** | **AI cannot assign sensitive epistemic state.** |
| **Risk prevented** | Que una inferencia del modelo adquiera el estatus de hecho **alegado** o **determinado** sin decisión humana. Daño concreto en el dominio: una afirmación generada por un modelo entra al expediente con el mismo peso que una afirmación que una profesional revisó y asumió, y desde ahí se propaga a escritos, cronologías y decisiones sin que nadie pueda distinguirla. |
| **Enforced in** | **Domain** (reglas de transición de estado del `Fact`) **+ Application** (gate de commit de `CommitReviewedFacts`), con dos defensas de superficie en **MCP** que no son la regla sino su blindaje. |
| **Configuration may relax?** | **NO.** |
| **How tested** | **`AT-001`** (acreditar un hecho directamente con `principal_type = AI`) y **`AT-002`** (inventar una autorización, en sus tres variantes). Niveles: N1 primario para `AT-001`; N4 para `AT-002(a)`; N2 para `AT-002(b,c)`. Veredicto disponible en V0: `PASS\|FAIL`. |

**Mecanismo concreto**

| Capa | Artefacto que la materializa | Especificado en |
|---|---|---|
| **Domain** | La transición a `ALLEGED` o `DETERMINED` con un `Principal` de `principal_type = AI` **no es representable**: no existe función de transición que la construya. `INV-D-20` y `INV-D-22` la expresan; `ADR-003` inv. 2 y 11 la fundan | `02-domain-model.md` §INV-D-20/22; ADR-003 |
| **Domain** | `provenance_kind = HUMAN_DECISION` exige `principal_type = HUMAN` (kernel §1.4, invariante duro). Es la formulación correcta de lo que el corpus antiguo escribía —mal— como `actor_type = HUMAN_DECISION` | kernel §1.4–§1.5 |
| **Application** | Gate de commit: las cinco condiciones de kernel §2.3 se evalúan contra el **registro propio del Core**, no contra ningún input. La pregunta que el Core se hace no es *"¿es real esta autorización?"* sino *"¿tengo yo una autorización válida?"* | `06-human-authorization.md` §5, §9 |
| **MCP (blindaje 1)** | **R5** — el principal no viaja en el input. Ninguna tool acepta `principal_id`, `actor_type`, `on_behalf_of`. Un invocador que pudiera declarar quién es podría declarar ser humano | `05-mcp-contract.md` §2 R5 |
| **MCP (blindaje 2)** | **R3 + R4** — ningún secreto de autorización viaja al modelo, y los schemas son cerrados (`additionalProperties: false`): `humanReviewed: true` muere en el adapter con `VALIDATION_FAILED` | `05-mcp-contract.md` §2 R3, R4 |
| **Persistencia** | `CHECK` redundante sobre `fact_status_history` — **cinturón, no motor**: el invariante jurídico no puede depender de SQLite | `04-persistence-model.md` §4 #15 |

**Qué NO cubre.** (i) No impide que el modelo **proponga** cualquier cosa: proponer es su función, y `PROPOSED` es exactamente el techo (`propose_facts` es clase `PROPOSAL`). (ii) No garantiza que la revisión humana sea **atenta**: garantiza que existió y que fue sobre el contenido exacto, no que fuera buena. (iii) No impide que el modelo **relate mal** un rechazo a la usuaria ("ya quedó guardado"): `12` §3.5 registra ese hueco como `SUPUESTO` declarado, y la mitigación de diseño es que las condiciones se adhieren al estado y a los artifacts, no solo al diálogo.

---

### 3.2 PF-002

| Campo | Valor |
|---|---|
| **PF-002** | — |
| **Name** | **Original evidence cannot be overwritten or deleted through the product surface.** |
| **Risk prevented** | Pérdida o alteración de la fuente primaria sobre la que se razona. Daño concreto: el expediente afirma custodiar unos bytes y custodia otros —o ninguno—, y toda cadena de provenance construida sobre ellos pasa a ser una afirmación sin respaldo, **sin que nada lo señale**. |
| **Enforced in** | **Infrastructure** (almacén write-once content-addressed) **+ MCP** (la capacidad no existe en la superficie). |
| **Configuration may relax?** | **NO.** |
| **How tested** | **`AT-011`** (escribir o borrar un `Source` a través del MCP) — modo *por ausencia*: se verifica que **ninguna tool del manifiesto** lo intenta, más `re-hash(bytes) == content_hash` tras el intento. Complemento: **`FT-013`** (test de superficie sobre el manifiesto) y `FT-002.c` (alterar el archivo en `Inbox/` tras la incorporación ⇒ Source y derivados intactos). Niveles: N4 (manifiesto), N5 (re-hash, write-once), N6. **Verificación periódica de hashes: `NOT_IMPLEMENTED` en V0** (§3.2 nota). |

**Mecanismo concreto**

| Capa | Artefacto que la materializa | Especificado en |
|---|---|---|
| **Infrastructure** | **Write-once**: el escritor nunca abre en modo escritura una ruta de `blobs/` que ya exista. Es la materialización en el adapter de PF-002 y de ADR-003 inv. 8 | `04-persistence-model.md` §7.3 |
| **Infrastructure** | La ruta del blob es **función pura** de `(content_hash, clase, storage_layout_version)`; ninguna tabla guarda rutas. No hay ruta que inyectar ni segunda fuente de verdad que desincronizar | `04-persistence-model.md` §7.2 |
| **Infrastructure** | El repositorio **no expone** `UPDATE` ni `DELETE` sobre `sources`. La incorporación es el único productor | `04-persistence-model.md` §4 #11; `02` `INV-D-10`, `INV-D-12` |
| **Infrastructure** | Orden obligatorio **bytes → fila**: un blob sin fila es basura recuperable; una fila sin blob es corrupción. Ante duda, siempre el fallo barato | `04-persistence-model.md` §7.3 |
| **MCP** | **Ausencia de capacidad**: no existe tool de escritura ni de borrado de `Source`. *No exponer es la forma más fuerte de prohibir* | `05-mcp-contract.md` §1 (3), §9 |
| **Domain/Schema** | Regla de esquema: **no existe, y no se añadirá sin ADR**, columna `authentic`, `verified`, `validated` ni `trusted` sobre `sources`, `evidence` o `derived_representations` | `07-provenance-and-locators.md` §6 |
| **Recolección de huérfanos** | Plano administrativo (runtime/CLI), **jamás** superficie del modelo (clase `ADMIN` vacía por diseño); solo elimina blobs no referenciados y nunca dentro de una transacción de negocio | `04-persistence-model.md` §7.4 |

**Qué NO cubre — declaración obligatoria.** La política dice literalmente *"through the product surface"*, y ese límite es real, no retórico:

1. **No protege frente a la usuaria con control total de la máquina.** Está **fuera del threat model V0**, declarado en kernel §8.3. El hash-chain y el re-hash son **tamper-evident, no tamper-proof**.
2. **No protege frente a herramientas genéricas del host** que escriban sobre el private state. Eso depende del punto **B-04** del spike de Cowork, hoy `INCONCLUSIVE` (`ESTADO-Y-HALLAZGOS-CRITICOS.md` §1.2). La protección es **posicional**, no una regla del host (§1.3 de ese documento).
3. **La verificación periódica de hashes que kernel §12 menciona como control NO EXISTE en V0.** No hay job ni planificador (`02` nota a `INV-D-11`; `12` §7). Lo verificable en V0 es la comprobación **bajo demanda**. Se registra como `NOT_IMPLEMENTED`, no como invariante cumplido.
4. **No impide borrar el archivo del `Inbox/`.** El `Inbox/` no es el almacén: `FT-002.c` prueba precisamente que alterarlo o borrarlo después de la incorporación **no afecta** al `Source` ni a sus derivados. Esa es la frontera de ADR-006.

---

### 3.3 PF-003

| Campo | Valor |
|---|---|
| **PF-003** | — |
| **Name** | **Unincorporated external information cannot become canonical evidence or support.** |
| **Risk prevented** | Fundamentar un hecho en material que nadie incorporó y que puede desaparecer, cambiar o no haber existido nunca. Daño concreto: un `Fact` sostenido por una URL, por un id de conector o por texto pegado en el chat es un hecho **sin custodia**: no se puede volver a leer, no se puede citar con precisión y no se puede auditar quién lo trajo. |
| **Enforced in** | **Domain** (`EvidenceLink` exige `Evidence` incorporada del mismo Case) **+ Application** (validación en `ProposeFacts` y en el gate de `CommitReviewedFacts`), con **MCP R1/R2** cerrando la vía de entrada. |
| **Configuration may relax?** | **NO.** |
| **How tested** | **`AT-005`** (crear un `EvidenceLink` contra material no incorporado: URL, id de conector, ruta o texto pegado). Niveles: N1 primario · N2 · N4 · N6. Código de rechazo: `NOT_INCORPORATED`. Fixture: `FX-P1`, cuyo tercer item está diseñado para este gate. |

**Mecanismo concreto**

| Capa | Artefacto que la materializa | Especificado en |
|---|---|---|
| **Domain** | `INV-D-28`: todo `EvidenceLink` referencia `Evidence` **incorporada** y **del mismo Case**. La frontera es de ADR-006 inv. 1 | `02-domain-model.md`; ADR-006 |
| **Domain** | Aislamiento por Case (`INV-D-06..09`): el rechazo autoritativo es del Core y ocurre **antes** de que la FK falle. Un error de motor no es una decisión de dominio | `04-persistence-model.md` §4 #3; `12` `AT-006` |
| **Application** | `ProposeFacts` valida cada entrada de `inputs[]` y de los links propuestos contra el Case Store **dentro de su transacción**. Con el retiro de `register_artifact` (kernel §6) la validación de ADR-006 inv. 3 conserva su semántica y cambia de sujeto: la hace el Core, no una tool | `03-application-use-cases.md`; `01` §9.1 |
| **MCP — R1** | Ninguna tool acepta rutas de filesystem ni URLs arbitrarias. No hay parámetro `path`, `uri`, `url`, `file`, `directory` en ningún schema | `05-mcp-contract.md` §2 R1 |
| **MCP — R2** | Toda referencia es un identificador **opaco emitido por el Core**. El texto libre de `inbox_query` se compara contra la **enumeración** que el Core hace del `Inbox/`: no se concatena, no se resuelve `..`, no se siguen symlinks ni junctions | `05-mcp-contract.md` §2 R2 |

**Qué NO cubre.** (i) No prohíbe **explorar**: la exploración puede **orientar**, nunca **fundamentar** (`12` `AT-005`). (ii) No garantiza que el material incorporado sea **auténtico**: garantiza que existe, que está custodiado y que su procedencia declarada quedó registrada — la autenticidad probatoria es juicio profesional, y PF-002 §Qué NO cubre lo complementa. (iii) **`DECISIÓN PENDIENTE` heredada de ADR-006**: `NOT_INCORPORATED` no tiene hoy condición del catálogo UX asociada (`05` §4.3; `12` `AT-005`). La política se cumple; su presentación a la usuaria está sin decidir.

---

### 3.4 PF-004

| Campo | Valor |
|---|---|
| **PF-004** | — |
| **Name** | **Unverified legal authority cannot become verified by model assertion.** |
| **Risk prevented** | Jurisprudencia o normas **inventadas** presentadas como verificadas — **el riesgo n.º 1 del dominio**. Daño concreto: un escrito que cita una sentencia que no existe, o que existe y no dice lo que se le atribuye, firmado por una profesional que confió en que el sistema había verificado. |
| **Enforced in** | **Domain** (no existe estado "verificada" al que transicionar, ni columna que lo represente) **+ MCP** (la capacidad **no existe** en la superficie V0). |
| **Configuration may relax?** | **NO.** |
| **How tested** | **`FT-013`** — test de superficie sobre el manifiesto: `verify_legal_source` **no figura** entre las tools. Modo *por ausencia* (`12` §3.3): donde la capacidad no existe, el resultado esperado no es una condición del catálogo sino la ausencia de la tool. **No tiene `AT-xxx` propio** — asimetría deliberada, con `DECISIÓN PENDIENTE` menor en `12` §3.7. Post-slice, cuando `verify_legal_source` exista: test de transición de estado. |

**Mecanismo concreto**

| Capa | Artefacto que la materializa | Especificado en |
|---|---|---|
| **MCP** | `verify_legal_source` está **fuera de la superficie V0** por decisión de los dueños (kernel §6). La única respuesta posible a *"marca esta sentencia como verificada"* es que **la operación no existe**: no hay estado que alcanzar, ni camino que rechazar, ni condición que emitir | `05-mcp-contract.md` §8.3, §9 |
| **Domain/Schema** | No existe columna `verified` / `validated` / `authentic` / `trusted` sobre ninguna entidad, **y no se añadirá sin ADR**. Es la traducción a schema de PF-004 y de ADR-006 inv. 6 | `07-provenance-and-locators.md` §6 |
| **Contenido** | El fixture del benchmark **carece de material jurídico real por diseño**, precisamente para no crear la ocasión | `13-synthetic-benchmark.md` §1 |
| **UX** | El catálogo de condiciones registra el arquetipo de afirmación prohibida (*"verifiqué", "confirmé la jurisprudencia", "según la sentencia vigente"*) frente al enunciado correcto: *"en esta versión no existe forma de marcar una fuente jurídica como verificada"* | `11-ux-condition-catalog.md` §… (tabla de arquetipos) |

**Qué NO cubre — el punto más incómodo de las cinco, y por eso se escribe.** En V0 la política se cumple **por ausencia de superficie**, que es la forma más fuerte disponible *hoy* y a la vez la menos informativa sobre el futuro:

1. **No impide que el modelo afirme en conversación** que verificó algo. Ninguna política del piso puede impedirlo: el diálogo no pasa por el Core. Lo que el diseño garantiza es que esa afirmación **no deja rastro en el estado canónico** — no existe campo donde escribirla.
2. **Cuando `verify_legal_source` entre (POST-V0), esta política pasa de ser un test de forma a ser un test de comportamiento**, y necesitará: (a) una transición de estado con productor único y determinista, (b) cotejo contra fuente autorizada — *determinista o no ocurre* —, y (c) `POR VERIFICAR`: existencia de fuentes oficiales colombianas consultables programáticamente. Si no existen, la verificación se degrada honestamente a *"recuperación + confirmación humana"* y el diseño debe **decirlo**, no simular verificación.
3. **La asimetría de prueba está registrada, no resuelta.** `12` §3.7 recomienda la opción (a) —dejarlo en `FT-013` con referencia cruzada explícita desde esta política— frente a (b) —crear `AT-014`—. Este documento **es** esa referencia cruzada.

---

### 3.5 PF-005

| Campo | Valor |
|---|---|
| **PF-005** | — |
| **Name** | **Mandatory uncertainty and integrity conditions cannot be suppressed by client configuration.** |
| **Risk prevented** | Que una organización **silencie los avisos** que hacen visible la incertidumbre. Daño concreto: una firma configura el producto para no mostrar `ANALYSIS_STALE` ni `LIMITED_CERTAINTY` porque "confunden al cliente", y a partir de ahí el sistema presenta como firme lo que sabe que no lo es. Es la vía por la que el producto podría configurarse para producir exactamente el riesgo que existe para evitar. |
| **Enforced in** | **Application** (emisión de la condición, adherida al estado y no solo al diálogo) **+ Configuration** (validación de la Client Config en carga: solo endurece). |
| **Configuration may relax?** | **NO.** |
| **How tested** | **`T-UX-06`** — una Client Config que intenta suprimir una condición obligatoria ⇒ **rechazo en carga**, visible, jamás degradación silenciosa a defaults. Invariante asociado: `INV-UX-08`. Complementos: **`AT-009.a`** (property test: todo artifact devuelto porta `stale` y, si `stale = true`, `stale_reasons[]` no vacío, en **todos** los scopes) y **`AT-009.b`** (el modelo intenta limpiar la marca ⇒ rechazo sintáctico o no-input). **`POR VERIFICAR`:** el mecanismo de configuración del perfil efectivo (`12` §7; `06` §11), del que depende este test. |

**Mecanismo concreto**

| Capa | Artefacto que la materializa | Especificado en |
|---|---|---|
| **Application** | Las condiciones se emiten **tipadas** desde el Core y viajan **adheridas al estado y a los artifacts**, no solo al diálogo. `ANALYSIS_STALE` viaja pegada al artifact en toda proyección | `11-ux-condition-catalog.md` §6.4; `10-artifact-lifecycle.md` inv. 7–9 |
| **Application** | Invariante del sobre: `completeness = PARTIAL ⇒ omissions[]` no vacío. Un contexto parcial nunca puede parecer expediente completo | kernel §9; `08-case-context-projections.md` |
| **Application** | **Presupuesto de atención** (`PROPUESTA`): con más de tres condiciones se muestran íntegras las bloqueantes y se agrupa el resto por categoría con su conteo. **Nunca se descartan**; suprimir por presupuesto una condición obligatoria está prohibido por esta política | `11-ux-condition-catalog.md` §… |
| **MCP** | **Ausencia de capacidad**: ninguna tool permite limpiar la marca de staleness. Un parámetro fabricado muere en el adapter (`R4`) | `10-artifact-lifecycle.md` `LE-04`; `05` §2 R4 |
| **Configuration** | Client Config **validada por schema**; una configuración inválida se rechaza **de forma visible**, nunca se degrada silenciosamente a defaults — un default silencioso convierte un error de configuración en una política tácita | `boundaries.md` §… ; §7 de este documento |

**Qué NO cubre.** (i) No cubre el **sobre de proyección**: `08` §… registra que **ninguna** política del piso protege la no-supresibilidad de `omissions[]`; hoy esa regla está cubierta por ADR-004 inv. 2, que es nivel 1 de precedencia y por tanto suficiente, pero **no** por el piso. Queda registrada como **segunda candidata** (§6.3). (ii) No cubre **qué mensaje** ve la usuaria: el pipeline `condición interna → categoría de presentación → mensaje por locale` (kernel §10) permite adaptar el texto; lo que no permite es **no emitirlo**. (iii) No cubre la **presentación en el cliente de chat**, que no controlamos: si el host decide no renderizar, el Core no puede impedirlo — por eso la condición se adhiere también al estado consultable.

---

## 4. Resumen de las cinco

| Id | Name (literal, kernel §12) | Enforced in | Relax? | How tested | Modo de defensa | Veredicto disponible en V0 |
|---|---|---|---|---|---|---|
| **PF-001** | AI cannot assign sensitive epistemic state | Domain + Application (+ MCP R3/R4/R5) | **NO** | `AT-001`, `AT-002` | Rechazo (y ausencia en el tramo `DETERMINED`) | `PASS\|FAIL` |
| **PF-002** | Original evidence cannot be overwritten or deleted through the product surface | Infrastructure + MCP | **NO** | `AT-011` + `FT-013` + re-hash | **Ausencia** | `PASS\|FAIL` **por la superficie**; verificación periódica `NOT_IMPLEMENTED` |
| **PF-003** | Unincorporated external information cannot become canonical evidence or support | Domain + Application (+ MCP R1/R2) | **NO** | `AT-005` | Rechazo | `PASS\|FAIL` |
| **PF-004** | Unverified legal authority cannot become verified by model assertion | Domain + MCP | **NO** | **`FT-013`** (sin `AT` propio, `12` §3.7) | **Ausencia** | `PASS\|FAIL` **por ausencia de superficie** |
| **PF-005** | Mandatory uncertainty and integrity conditions cannot be suppressed by client configuration | Application + Configuration | **NO** | `T-UX-06` (+ `AT-009.a/b`) | Rechazo en carga | `PASS\|FAIL`, **condicionado** al mecanismo de configuración efectiva (`POR VERIFICAR`) |

**Lectura de la columna *Modo de defensa*** (distinción de addendum v0.3 B.6, consolidada en `12` §3.3): confundir *rechazo* con *ausencia* produce afirmaciones falsas de seguridad. Donde la defensa es **ausencia**, lo que hay que probar es que la capacidad **no está en el manifiesto** y que no existe camino alternativo — un test de forma, no de comportamiento. Dos de las cinco políticas (PF-002 y PF-004) se sostienen hoy, total o parcialmente, sobre ausencia. **El día que alguien añada el camino, el test es lo único que lo notará.**

---

## 5. Comparación con el conjunto anterior

### 5.1 Los dos conjuntos, uno al lado del otro

| # | Conjunto anterior (`principles.md`, anexo Product Floor v0) | Conjunto propuesto (kernel §12) | Correspondencia |
|---|---|---|---|
| 1 | Una fuente jurídica no verificada jamás se promueve a verificada de forma silenciosa ni por afirmación del modelo | **PF-004** | **Idéntica en sustancia.** Cambia la formulación: de "no se promueve silenciosamente" a "no se vuelve verificada por afirmación del modelo". La nueva es más precisa —nombra al sujeto (el modelo) y no al modo (silenciosamente)— y por tanto más comprobable |
| 2 | Ningún actor `AI_*` efectúa transiciones epistémicas sensibles (`ALLEGED`, `DETERMINED`) ni las autoriza | **PF-001** | **Idéntica en sustancia**, con el vocabulario corregido: `actor AI_*` → `principal_type = AI` (kernel §1.5, normalización aprobada). El enunciado nuevo dice *"assign sensitive epistemic state"*, que cubre tanto efectuar como autorizar |
| 3 | Las condiciones de clase blocking y los avisos de incertidumbre no son suprimibles por configuración de cliente | **PF-005** | **Idéntica en sustancia.** El enunciado nuevo añade *"and integrity"*, que amplía de "incertidumbre" a "incertidumbre e integridad" |
| 4 | Los `Source` son inmutables por la superficie normal del producto y no existe operación de borrado expuesta | **PF-002** | **Idéntica en sustancia**, con un nombre de dominio en vez de un nombre de entidad: *"original evidence"* en lugar de *"`Source`"*. Mejor: una política del piso debe ser legible por quien no conoce el modelo de datos |
| 5 | **La auditoría (Case Event Log) no es desactivable ni editable por configuración** | **— ninguna —** | **DESPLAZADA.** Ver §6 |
| — | **— ninguna —** | **PF-003** — Unincorporated external information cannot become canonical evidence or support | **NUEVA.** El conjunto anterior no tenía política de frontera de incorporación, pese a que ADR-006 (Accepted) la funda. Es la ganancia neta del conjunto nuevo |

### 5.2 Balance

- **Cuatro políticas sobreviven** (1↔PF-004, 2↔PF-001, 3↔PF-005, 4↔PF-002), tres de ellas con enunciado mejorado y una con vocabulario corregido.
- **Una entra**: PF-003, que cubre un riesgo que el conjunto anterior dejaba fuera del piso pese a tener ADR Accepted propio.
- **Una sale**: la inmutabilidad de la auditoría.
- **El número cinco se conserva porque los dueños pidieron exactamente cinco** (kernel §12.6), no porque cinco sea el número correcto. `principles.md` (anexo) declara el contenido *"abierto a ampliación"*. La disciplina de alcance produjo un intercambio 1:1 —entra PF-003, sale la auditoría— que **no es neutro** y que este documento no deja pasar en silencio.

### 5.3 Nivel documental y precedencia — por qué esto no se resuelve solo

El conjunto anterior vive en `principles.md`, **nivel 3** de precedencia. El conjunto nuevo vive en el kernel técnico, **nivel 2**. Por la regla de kernel §14, **gana el kernel**. La consecuencia es que la política de auditoría desaparecería del piso **por precedencia silenciosa**, que es exactamente el mecanismo que este documento existe para impedir. Ya está registrado como divergencia en `01-system-design.md` §9.3 (fila 2) y en `09-events-and-audit.md` §8.3.

---

## 6. La política desplazada: la auditoría

### 6.1 Por qué las cinco cubren riesgos directos del dominio y la auditoría no

La diferencia no es de importancia sino de **naturaleza**, y es la razón defendible del desplazamiento:

| Dimensión | Las cinco | La auditoría |
|---|---|---|
| **Qué falla si se relaja** | Una afirmación falsa entra al expediente (PF-001, PF-003, PF-004); la prueba se pierde (PF-002); la incertidumbre se vuelve invisible (PF-005) | **No falla nada de forma inmediata.** Lo que se pierde es la capacidad de **saber después** qué pasó |
| **A quién daña** | A la profesional y a su cliente, **en el asunto concreto** | A la profesional **frente a un cuestionamiento posterior**, y al producto frente a una auditoría |
| **Naturaleza** | **Riesgo directo del dominio jurídico** | **Meta-garantía**: no protege el conocimiento del expediente, protege la posibilidad de verificar cómo se formó |
| **Criterio A1 (§1.3)** | Cumplen: nombran un daño jurídico | **No lo cumple en la misma forma**: nombra la pérdida de un instrumento de verificación |

Aplicando el criterio de admisión de §1.3 con honestidad: la auditoría cumple **A2** (punto de aplicación identificable: el Case Event Log), **A3** (comprobable) y **A4** de forma clarísima (*"desactivar el log por rendimiento"* o *"podar eventos antiguos por espacio" son configuraciones que alguien pediría*). Donde no encaja limpiamente es en **A1**. Ese es el argumento del desplazamiento — **y es un argumento discutible**, porque una meta-garantía perdida solo se descubre cuando ya hace falta.

### 6.2 Declaración explícita: hoy ninguna de las cinco la cubre

**Verificado política por política, no afirmado en bloque:**

| Política | ¿Cubre la inmutabilidad de la auditoría? | Por qué no |
|---|---|---|
| PF-001 | **No** | Habla de estado epistémico de `Fact`, no del log |
| PF-002 | **No** | Habla de *original evidence* — `Source` y sus bytes. El Case Event Log no es evidencia original: es registro de actos |
| PF-003 | **No** | Habla de la frontera de incorporación |
| PF-004 | **No** | Habla de autoridad jurídica |
| PF-005 | **No** | Habla de **condiciones** (avisos de incertidumbre e integridad emitidos a la usuaria), no del registro append-only. `11` `INV-UX-08` lo confirma: su sujeto es la condición, no el evento |

**Conclusión, sin ambigüedad: si los dueños aprueban las cinco tal cual, el Product Floor no protegerá el Case Event Log.** La protección seguirá existiendo —append-only, trigger `RAISE(ABORT)` incondicional, hash-chain, `04` §4— pero **como decisión de implementación**, no como política que la configuración no puede relajar. Y una protección que vive solo en el adapter es, por definición, una protección que un cambio de adapter puede perder.

### 6.3 Las dos candidatas registradas, para que la decisión sea informada

**Candidata 1 — la sexta política (la que el kernel §12.6 señala).** Forma propuesta, con el formato exigido, ya redactada en `09-events-and-audit.md` §8.3 y reproducida aquí **sin cambios** para que la decisión se tome sobre un texto único:

> **PF-006 — El Case Event Log no es desactivable, editable ni podable por configuración.**
> *Risk prevented:* que una organización desactive, edite o pode el registro que hace verificable todo lo demás — con el efecto de que las otras cinco políticas dejarían de ser comprobables *a posteriori*.
> *Enforced in:* Infrastructure (append-only + trigger `RAISE(ABORT)` incondicional + hash-chain) + Configuration (validación en carga) + ausencia de superficie (ninguna tool escribe, edita ni borra eventos).
> *Configuration may relax?* **NO.**
> *How tested:* config que intenta desactivar o podar el log ⇒ rechazo en carga; intento de `UPDATE`/`DELETE` sobre `case_events` ⇒ aborta; verificación de cadena tras alteración manual ⇒ mismatch detectado (tamper-evident, kernel §8.3).

**Candidata 2 — registrada por completitud, NO propuesta como política.** `08-case-context-projections.md` §… señala que **ninguna** de las cinco cubre la no-supresibilidad de `omissions[]` en el sobre de proyección; PF-005 cubre condiciones, no el sobre. Hoy la regla está sostenida por ADR-004 inv. 2 (nivel 1), que es suficiente para que sea normativa. Se menciona aquí **solo** para que los dueños vean el mapa completo de huecos, no como sexta ni séptima política.

### 6.4 Las tres opciones, sin elegir por los dueños

| Opción | Qué implica | Coste | Consecuencia si se elige |
|---|---|---|---|
| **(a)** Cinco políticas, sin la de auditoría | Disciplina de alcance estricta; se respeta "exactamente cinco" | Cero coste de implementación | **El piso no protege la auditoría.** La protección queda en el adapter y en ADR-004. Debe quedar escrito en `principles.md` que la política 5 del anexo **se retira**, con su razón |
| **(b)** Seis políticas: entra **PF-006** | El piso protege también la meta-garantía | Cero coste de implementación adicional: el mecanismo (append-only, trigger, hash-chain) **ya existe** por ADR-004. Lo único que se añade es la **validación de configuración** y su test | Rompe el "exactamente cinco" del encargo. Reconcilia el kernel con `principles.md` sin retirar nada |
| **(c)** Cinco, sustituyendo una | No recomendada | — | Cualquier sustitución retira una política que cubre un riesgo **directo** del dominio para meter una meta-garantía. Es el peor intercambio de los tres |

**Recomendación del Technical Design: (b).** Razón única: el coste marginal es **cero en mecanismo** —todo lo que PF-006 exigiría ya está construido por ADR-004— y lo que se gana es que la garantía deje de ser revocable por un cambio de adapter o por una configuración que hoy nadie ha prohibido. Contra-argumento que hay que reconocer: el número cinco lo fijaron los dueños, y ampliarlo sienta el precedente de que el piso crece por argumentos de diseño y no por decisión de producto. **Por eso se presenta como decisión y no se aplica.**

---

## 7. CAN TIGHTEN / CANNOT WEAKEN

### 7.1 El principio

> **CAN TIGHTEN / CANNOT WEAKEN.** La Client Config puede hacer el comportamiento del producto **más restrictivo** que el piso en cualquier dimensión. **Nunca menos.** Una configuración que relaje cualquier política del Product Floor no es una configuración permisiva: es una configuración **inválida**, y se rechaza de forma visible en carga.

Fuente aprobada: cita de los dueños en addendum v0.3 B.4. Materialización previa: `boundaries.md` §… (*"la Client Config solo endurece"*), `principles.md` (anexo, *Enforcement*), `06` §4 (la política de `expires_at` puede acortarse, nunca relajarse a "sin expiración").

### 7.2 Qué significa "endurecer" en términos operativos

`PROPUESTA DEL TECHNICAL DESIGN.` El principio es inútil sin un criterio decidible. Criterio propuesto:

> Una configuración **endurece** si, para todo estado del sistema, el conjunto de operaciones que permite es **subconjunto** del que permite el piso, y el conjunto de condiciones que emite es **superconjunto** del que emite el piso.

De ahí salen cuatro dimensiones comprobables:

| Dimensión | Endurecer (permitido) | Relajar (prohibido) |
|---|---|---|
| **Superficie** | Retirar tools del perfil efectivo (p. ej. un perfil de decisor sin evaluación de posición estratégica) | Añadir una tool que no está en el manifiesto sellado |
| **Gates** | Añadir gates de commit/export (p. ej. exigir doble revisión) | Retirar cualquiera de las cinco condiciones del gate de autorización (kernel §2.3) |
| **Condiciones** | Añadir condiciones obligatorias, o subir una a categoría más visible | Suprimir, degradar o silenciar una condición obligatoria (PF-005) |
| **Umbrales temporales** | Acortar `expires_at` | Alargarlo más allá del máximo del piso, o fijar "sin expiración" (`06` §4) |

**Regla de asimetría, que es lo que hace el criterio decidible:** una configuración se evalúa **campo a campo contra el piso**, y basta **un** campo que relaje para que la configuración completa sea inválida. No hay compensación entre campos: endurecer mucho en un sitio no autoriza a relajar un poco en otro.

### 7.3 Cómo se valida al cargar una Client Config

`PROPUESTA DEL TECHNICAL DESIGN.` Secuencia obligatoria, ejecutada en el arranque del Core, **antes** de que ninguna base se abra y ningún puerto quede escuchando (misma disciplina que kernel §4: *fail to start, no warning*):

```text
1. PARSEAR            la Client Config
                      fallo -> RECHAZO VISIBLE. No se arranca.

2. VALIDAR POR SCHEMA (schema cerrado; propiedades desconocidas NO se ignoran)
                      fallo -> RECHAZO VISIBLE, identificando el campo.
                      NUNCA degradar a defaults: un default silencioso
                      convierte un error de configuracion en politica tacita.

3. COMPARAR CON EL PISO, campo a campo
                      para cada campo gobernado por una politica PF-xxx:
                        valor_config  vs  valor_piso
                        veredicto ∈ { IGUAL, ENDURECE, RELAJA }
                      un solo RELAJA -> RECHAZO VISIBLE, nombrando
                        (a) el campo, (b) la politica PF-xxx violada,
                        (c) el valor del piso, (d) el valor propuesto.

4. COMPONER el perfil efectivo = piso ⊓ config   (interseccion, nunca union)

5. REGISTRAR configuration_version + hash del texto de la config,
                      para que el rechazo o la aceptacion sean
                      reproducibles entre releases (01 §7.1)

6. ARRANCAR
```

Cinco propiedades que la secuencia garantiza y que se pueden probar:

| # | Propiedad | Cómo se prueba |
|---|---|---|
| 1 | **Fail closed en carga.** Ninguna ruta de error produce un perfil efectivo más permisivo que el piso | Suite de configs malformadas y de configs que relajan; se afirma **no-arranque** |
| 2 | **Sin degradación silenciosa.** Nunca se sustituye un campo inválido por su default | El test afirma el **mensaje** de rechazo, no solo el código de salida |
| 3 | **El mensaje es de política, no de ingeniería.** Nombra la política violada y los dos valores | `OPERATION_NOT_PERMITTED {operation, policy_reason}` usa la misma regla en runtime (`11` §…) |
| 4 | **Composición por intersección.** El perfil efectivo nunca amplía la superficie ni reduce las condiciones | Property test: para toda config válida, `permitido(efectivo) ⊆ permitido(piso)` y `condiciones(efectivo) ⊇ condiciones(piso)` |
| 5 | **Reproducibilidad.** El mismo texto de config produce el mismo veredicto en la misma versión de producto | `configuration_version` + hash del texto (`01` §7.1, decisión 8) |

**Nota de ubicación (regla de dependencias, kernel §13):** el piso vive en el **producto sellado**, jamás en un archivo de configuración. Un piso configurable no es un piso. Corolario ya escrito en el corpus: *no hacer cumplir una regla críticamente importante solamente mediante un archivo de configuración*.

**`POR VERIFICAR` que condiciona esta sección.** El **mecanismo de configuración del perfil efectivo de ejecución** (`production` / `development` / `test`, y la forma concreta de la Client Config) no está decidido. Condiciona a la vez el test de PF-005 y `AT-013` (`12` §7). Mientras no se decida, la secuencia de §7.3 es un **contrato de comportamiento**, no una especificación implementable. Registrado como decisión bloqueante en `16-open-implementation-decisions.md`.

### 7.4 Ejemplos concretos, para que el criterio no sea abstracto

| Configuración propuesta | Veredicto | Razón |
|---|---|---|
| `authorization.expires_at_default: 4h` (piso: 24 h) | **ENDURECE** — válida | Acorta la ventana de una autorización viva |
| `authorization.expires_at_default: never` | **RELAJA** — inválida | `06` §4: la política nunca se relaja a "sin expiración" |
| `conditions.suppress: ["ANALYSIS_STALE"]` | **RELAJA** — inválida | **PF-005** directa. Rechazo en carga (`T-UX-06`) |
| `conditions.always_blocking: ["UNCERTAIN_FRAGMENT"]` | **ENDURECE** — válida | Sube una condición a categoría más visible |
| `surface.disable_tools: ["search_case"]` | **ENDURECE** — válida | Subconjunto de la superficie sellada |
| `surface.enable_tools: ["verify_legal_source"]` | **RELAJA** — inválida | **PF-004**: la capacidad no existe en el producto sellado; la configuración no puede crearla |
| `evidence.allow_source_deletion: true` | **RELAJA** — inválida | **PF-002**. Además, la operación no existe: la configuración no puede inventar una capacidad |
| `facts.allow_ai_commit: true` | **RELAJA** — inválida | **PF-001**. No hay campo que la configuración pueda tocar para lograrlo; el rechazo es en el schema |
| `commit.require_second_reviewer: true` | **ENDURECE** — válida | Añade un gate. POST-V0 en cuanto a implementación; el criterio ya lo admite |
| `audit.retention_days: 90` sobre el Case Event Log | **HOY: no gobernado por ninguna política** | Es exactamente el hueco de §6.2. Con **PF-006** sería `RELAJA`; sin él, el criterio no tiene contra qué comparar |

La última fila es la demostración práctica del §6: **no es que la configuración pudiera desactivar la auditoría hoy** —el mecanismo no lo permite— sino que **el validador no tendría regla contra la que rechazarla**, y el rechazo dependería de que alguien recordara escribirlo.

---

## 8. Lo que el Product Floor NO garantiza — declaración obligatoria

Ninguna de las cinco políticas garantiza nada de lo siguiente, y decirlo forma parte de proponerlas:

| Límite | Estado | Dónde vive |
|---|---|---|
| Protección frente a una **usuaria hostil con control total del equipo** | **Fuera del threat model V0**, declarado. Tamper-**evident**, no tamper-proof | kernel §8.3 |
| Protección frente a **herramientas genéricas del host** que escriban en el private state | Depende de **B-04** del spike de Cowork, `INCONCLUSIVE`. La protección es **posicional** | `ESTADO-Y-HALLAZGOS-CRITICOS.md` §1.2, §1.3 |
| **Verificación periódica** de integridad de blobs (PF-002) | **`NOT_IMPLEMENTED`**: no hay job ni planificador en V0. Solo bajo demanda | `02` nota `INV-D-11`; `12` §7 |
| Que el modelo **relate correctamente** un rechazo a la usuaria | `SUPUESTO` declarado: no hay mecanismo conocido que lo garantice. Mitigación: condiciones adheridas al estado y a los artifacts | `01` §2.2; `12` §3.5 |
| Que la **revisión humana sea atenta** | Fuera del alcance de cualquier política técnica. El piso garantiza que **existió** y que fue sobre el **contenido exacto** | `06` §5 |
| Que el **host** muestre el diálogo de autorización a una persona | El host puede auto-aprobar (hallazgo 5 del spike). **Nuestro diseño no confía en el diálogo del host**: la autorización se resuelve server-side | `ESTADO-Y-HALLAZGOS-CRITICOS.md` §1.1 (5), §1.3 |
| Que un **skill** se cumpla | Un skill es texto que el modelo puede ignorar. Si el sistema deja de ser seguro porque el modelo ignoró un skill, hay lógica crítica en el lugar equivocado | `01` §2.2 |

---

## 9. Estado y decisiones que requieren aprobación

| # | Decisión | Sección | Estado | Coste de no decidirla |
|---|---|---|---|---|
| 1 | **Aprobar las cinco políticas** tal como están enunciadas | §3 | **`PROPOSED`** | El piso queda declarado en un documento de nivel 2 sin ratificación; `principles.md` (nivel 3) sigue listando un conjunto distinto |
| 2 | **PF-006 (auditoría): ¿entra como sexta?** Opciones (a), (b), (c) de §6.4; recomendación **(b)** | §6 | **DECISIÓN PENDIENTE de los dueños** | La política 5 del anexo de `principles.md` desaparece **por precedencia silenciosa** — el mecanismo que este documento existe para impedir |
| 3 | Retirar formalmente la política 5 del anexo de `principles.md` si se elige (a), con su razón escrita | §5.3, §6.4 | Consecuencia de (2) | Dos documentos vigentes con dos pisos distintos |
| 4 | **Criterio operativo de "endurecer"** (§7.2) y **secuencia de validación** (§7.3) | §7 | `PROPUESTA DEL TECHNICAL DESIGN` | "Solo endurece" queda como principio sin criterio decidible, y cada validación lo interpretará |
| 5 | **Mecanismo de configuración del perfil efectivo** (`production`/`development`/`test` + forma de la Client Config) | §7.3 | **`POR VERIFICAR` / BLOQUEANTE** | Sin él, ni PF-005 ni `AT-013` son ejecutables. Ver `16-open-implementation-decisions.md` |
| 6 | **PF-004 sin `AT` propio**: dejarlo en `FT-013` con referencia cruzada (opción a, recomendada) o crear `AT-014` (opción b) | §3.4 | **DECISIÓN PENDIENTE menor** (`12` §3.7) | El riesgo n.º 1 del dominio queda probado solo desde la matriz funcional |
| 7 | Registrar la **candidata 2** (no-supresibilidad de `omissions[]`) como conocida y **no** promovida | §6.3 | Registro, no propuesta | Se descubre el hueco más tarde y parece omisión |

**Ninguna de las siete está resuelta en este documento.** El documento las presenta; los dueños deciden.

---

**Referencias.** `00-technical-kernel.md` §1, §2.3, §3.3, §4, §6, §8.3, §9, §10, §11, §12, §13, §14, §15 · `01-system-design.md` §2.2, §7.1, §9.1–§9.3, §10 · `02-domain-model.md` (`INV-D-10`, `INV-D-11`, `INV-D-12`, `INV-D-20`, `INV-D-22`, `INV-D-28`) · `03-application-use-cases.md` · `04-persistence-model.md` §4 (#11, #15), §7.2–§7.4 · `05-mcp-contract.md` §1, §2 (R1–R6), §8.3, §9 · `06-human-authorization.md` §4, §5, §9 · `07-provenance-and-locators.md` §6 · `08-case-context-projections.md` (candidata 2) · `09-events-and-audit.md` §8.3 (PF-006) · `10-artifact-lifecycle.md` (`LE-04`, inv. 7–9) · `11-ux-condition-catalog.md` (`INV-UX-08`, `T-UX-06`) · `12-testing-strategy.md` §3.1, §3.3, §3.5, §3.7, §4, §7 · `13-synthetic-benchmark.md` §1 · `16-open-implementation-decisions.md` · `ESTADO-Y-HALLAZGOS-CRITICOS.md` §1 · ADR-001 (inv. 1, 3, 4, 7), ADR-002 (inv. 5, val. 2, 4), ADR-003 (inv. 2, 8, 10, 11), ADR-004 (inv. 2), ADR-005 (inv. 2), ADR-006 (inv. 1, 3, 6, 7) · `docs/architecture/principles.md` (anexo Product Floor v0) · `docs/architecture/boundaries.md` · `docs/architecture/notes/addendum-correcciones-v0_3.md` B.4, B.6.
