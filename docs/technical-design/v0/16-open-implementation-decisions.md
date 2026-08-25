# 16 — Decisiones abiertas que condicionan la implementación de la Fase 1

**Estado:** documento de cierre de la fase TECHNICAL DESIGN V0. No decide nada: **clasifica**.
**Precedencia (kernel §14):** ADRs Accepted (001–006) > Technical Design V0 (incl. `00-technical-kernel.md`) > `principles.md` > glosario > addenda > spikes.
**Fuente de cada fila:** el documento donde la decisión ya está planteada. Este documento **no reabre** ninguna discusión y **no repite** su análisis: lo referencia y añade una sola cosa nueva — el **veredicto de bloqueo**.

Este documento existe porque la lista de "decisiones pendientes" del corpus mezcla dos cosas que exigen respuestas distintas: las que **impiden escribir código defendible** y las que **conviene decidir** pero no detienen a nadie. Tratarlas igual produce dos fallos simétricos: paralizarse por decisiones que no bloquean, o arrancar sobre decisiones que sí.

---

## 0. Definición operativa de "Fase 1"

`SUPUESTO — requiere confirmación de los dueños.` El corpus no define fases de implementación (la única aparición de "primera fase" es la de descubrimiento, `prompt-maestro-v0_1.md` §…). Este documento adopta la definición mínima coherente con el vertical slice y la declara para que sea corregible:

> **Fase 1 = implementar el vertical slice V0 de extremo a extremo, en una máquina, con una usuaria, sin usuaria real.**

| Dentro de Fase 1 | Fuera de Fase 1 |
|---|---|
| `domain` + `application` completos para los use cases de kernel §7 | Transporte real del canal humano (UI, elicitation, CLI de producción) |
| Adapter de persistencia (`04`) y de blobs, con migraciones y backup verificado | Cowork —o cualquier host concreto— como anfitrión **de producción** |
| Servidor MCP con la superficie de `05` | Distribución del producto (instalador, firma, actualizaciones) |
| Canal de autorización humana **por `DevHumanAuthorizationProvider`** | Primer expediente real de una profesional |
| Suite N1–N6 completa (`12`), incluidos `AT-001`…`AT-013` | Knowledge Pack, jurisprudencia, conectores, motor de plazos (kernel §15) |
| N7 sobre el fixture `legal-case-v0` (`13`) | Multi-máquina, sync, PostgreSQL, búsqueda vectorial |

**Consecuencia de la definición:** una decisión que solo hace falta para el **primer usuario real** no bloquea la Fase 1, pero bloquea la Fase 2 y debe estar en el mapa. La columna *"Cuándo deja de estar mitigada"* de §4 sirve exactamente para eso.

---

## 1. Criterio de bloqueo — decidido antes de aplicarlo

`PROPUESTA DEL TECHNICAL DESIGN.` Sin criterio explícito, "bloqueante" se convierte en un adjetivo de énfasis. El criterio es:

> Una decisión **BLOQUEA** la Fase 1 si se cumple **al menos una** de estas dos condiciones:
>
> **B1 — No hay respuesta determinada.** Ni los dueños, ni un ADR Accepted, ni la regla de precedencia proporcionan un valor con el que escribir el código o el test; **o bien** el corpus normativo se contradice a sí mismo sobre ese valor, de modo que la precedencia no resuelve. Escribir igualmente exige **inventar** la respuesta, que es exactamente lo que la regla de veracidad prohíbe.
>
> **B2 — La respuesta provisional no se corrige por refactor.** Adoptar una respuesta provisional produce un artefacto cuya corrección posterior no es un cambio de código sino un **cambio de contrato ya ejercitado** (número de tools contado por un test de superficie, forma de la tabla de autorizaciones, valores escritos en un log append-only hash-chained) o un **cambio de plataforma** (motor, driver, piso de runtime).

Y **NO bloquea** —aunque esté pendiente— si existe una **mitigación construida**: un puerto que aísla la decisión, un doble que la sustituye, o una respuesta que la precedencia entrega sin ambigüedad. En ese caso la decisión pasa a §4 con su mitigación nombrada y con la fecha operativa en que deja de valer.

**Regla de honestidad aplicada al propio criterio:** una mitigación solo cuenta si **existe en el diseño**, no si es imaginable. `DevHumanAuthorizationProvider` cuenta porque `06` §7–§8 lo especifica y `12` §2.9 lo cataloga; "ya haremos un stub" no contaría.

---

## 2. Cuadro de mando

| Id | Decisión | ¿Bloquea Fase 1? | Condición | Quién decide | Documento fuente |
|---|---|---|---|---|---|
| **OD-01** | ~~Amendment de `CaseRevision`: `event_seq` vs `case_revision`~~ **RESUELTA — enmienda AC-02 aprobada** | **NO (resuelta)** | B1 | **Dueños** (amendment de ADR-004 y ADR-005, Accepted) | kernel §5.2; `01` §9.2; `04` §10 C3 |
| **OD-02** | Superficie MCP: **8 tools vs 9** | **SÍ** | B1 + B2 | **Dueños** (amendment de ADR-001 inv. 3, Accepted) | kernel §6; `01` §9.1; `05` §13 |
| **OD-03** | Librería de acceso a SQLite | **SÍ** | B1 | Technical Design propone; **dueños ratifican** (el coste aceptado es un riesgo de producto) | spike de dependencias §3.8; `04` §1.3, §11 |
| **OD-04** | Granularidad de `HumanAuthorization`: por item vs por Proposal (**aprobación de ADR-008**) | **SÍ** | B1 + B2 | **Dueños** (enmienda ADR-005 §2, Accepted) | `04` §10 C2; ADR-008; kernel §2, §3 |
| **OD-05** | Mecanismo de **configuración del perfil efectivo** (`production`/`development`/`test`) | **SÍ** | B1 | Technical Design propone; **dueños ratifican** | `12` §7; `06` §11; `15` §7.3. **Detectada al evaluar, no encargada** |
| **OD-06** | **Transporte** del canal de autorización humana | **NO — mitigada** | Puerto + `DevHumanAuthorizationProvider` | **Dueños** (producto/UX), informados por el spike | `06` §7–§8; ADR-005 §5 |
| **OD-07** | **Proveedor de transcripción** | **NO — mitigada** | `FixtureDerivationProvider` | **Dueños** (admisión del proveedor); técnico ejecuta el spike | `07` §4; `12` §2.9; `02` §2.5 |
| **OD-08** | Identificador de entidad: **UUIDv7 vs ULID** | **NO — mitigada** | `IdPort` + ausencia de datos de producción | Technical Design propone; **dueños ratifican** el piso de Node | spike de dependencias §2; kernel §11 |
| **OD-09** | Aprobación de **las cinco políticas del Product Floor** (+ ¿PF-006?) | **NO — mitigada** | El mecanismo ya lo exigen los ADRs Accepted | **Dueños** | `15`; kernel §12; `09` §8.3 |
| **OD-10** | Aprobación de **ADR-007, 009, 010, 011** | **NO — mitigada** | Ratificación documental de decisiones ya especificadas | **Dueños** | ADR-007 (este ciclo), ADR-011; ADR-009/010 pendientes de escritura |
| **OD-11** | **B-04** del spike de Cowork (¿el MCP local alcanza el private state mientras el host no?) | **NO para Fase 1** — **SÍ para comprometerse con Cowork** | Perímetro posicional + Core como frontera real | Técnico ejecuta; **dueños** deciden el host | `ESTADO-Y-HALLAZGOS-CRITICOS.md` §1.2, §4 |

**Cinco bloqueantes, seis mitigadas.** Cuatro de los cinco bloqueantes son **decisiones de los dueños sobre ADRs Accepted**, no problemas técnicos abiertos: se resuelven en una sesión de decisión, no con un spike.

---

## 3. BLOQUEANTES

### OD-01 — Amendment de `CaseRevision`: `event_seq` vs `case_revision`

| Campo | Contenido |
|---|---|
| **Decision** | ¿El acto de **revisión humana** (`ProposalReviewed`) avanza `case_revision`, o solo avanza `event_seq`? Equivale a decidir si el reloj del caso mide *eventos* o *conocimiento canónico*. |
| **Recommended option** | **Aprobar el amendment (Modelo B):** dos contadores — `event_seq` monotónico en **todo** evento; `case_revision` monotónico **solo** en eventos que mutan el estado epistémico canónico. `ProposalReviewed` avanza `event_seq` y escribe `case_revision = NULL`. Razones ya argumentadas en kernel §5.2: semántica del reloj, eliminación de conflictos espurios, eliminación de la circularidad de `expected_case_revision`. |
| **Rama descartada (Modelo A)** | Todo evento avanza `case_revision`; `seq == revision`. Era lo que decían ADR-004 (c) e inv. 5, ADR-005 inv. 9–10 y el vertical slice (paso 10). Coste declarado: revisar la propuesta P-1 invalida análisis en vuelo sin relación con P-1 — el falso conflicto que ADR-004 quiere evitar — y `expected_case_revision` vuelve a definirse en términos del propio acto que la produce. |
| **Impact** | Valor de `expected_case_revision` en toda `HumanAuthorization`; condición (3) del gate de commit; numeración del happy path (pasos 10–11); tests `F7`, `F8`, **`AT-008`**; contexto de comparabilidad de toda corrida del benchmark (`13` exige reportar *"modelo de revisión (A o B) observado"*). **Impacto estructural en persistencia: ninguno** — `04` §10 C3 dejó el esquema neutral a propósito (`event_seq NOT NULL UNIQUE`, `case_revision NULL`, sin `CHECK` que fije un modelo, índice de `changes_since` parcial). |
| **Blocking?** | **NO — RESUELTA.** Los dueños aprobaron la enmienda AC-02: `event_seq` avanza en todo evento, `case_revision` solo en mutaciones epistémicas canónicas, `ProposalReviewed` lleva `case_revision` NULL y `expected_case_revision` es la revisión contra la que se generó y se revisó la Proposal. ADR-004 y ADR-005 quedan enmendados (supersedes §16.16 y §16.19) y el corpus está normalizado. Registro histórico del bloqueo anterior: *"no se aplica hasta que los dueños aprueben el amendment"* y kernel §7 ya presenta la tabla con `ReviewProposal → ¿avanza case_revision? no (§5.2)`. `01` §9.2 lo registra literalmente: *"Ambas cosas no pueden ser ciertas a la vez en un documento normativo"*. Un implementador que abra el kernel encuentra dos respuestas y **tiene que inventar** cuál vale. Agravante B2: los valores ya escritos en `case_events.case_revision` viven en un log append-only hash-chained; corregirlos después no es migración sino **re-anclaje de la cadena**, que `01` §10 (decisión 10) declara **cambio de contrato**. |
| **Quién decide** | **Los dueños.** Es amendment de dos ADRs Accepted (ADR-004 (c) e inv. 5; ADR-005 inv. 9–10) y corrección del addendum v0.3 B.2. Ningún documento de nivel 2 puede hacerlo. |

**Lo mínimo para desbloquear:** una sola respuesta —A o B— y, si es B, la instrucción de corregir el kernel §7 o el kernel §5.2 para que dejen de contradecirse. Si es A, basta corregir el kernel §7.

---

### OD-02 — Superficie MCP: ocho tools frente a nueve

| Campo | Contenido |
|---|---|
| **Decision** | ¿La superficie expone **8 tools** (kernel §6, retirando `register_artifact`) o **9** (ADR-001 inv. 3, Accepted)? |
| **Recommended option** | **Ocho.** Enmendar ADR-001 inv. 3 y su validación 7. Razón del kernel §6, que este documento suscribe: `FactAnalysis` es **consecuencia necesaria** de `propose_facts`; exponer su registro abre dos fallos —olvidarlo, o registrar un artifact que no corresponde a ningún análisis real— sin aportar ninguna capacidad. Regla general derivada: *una operación se expone solo si el modelo debe decidir cuándo ocurre*. |
| **Alternative** | **Nueve.** Conservar `register_artifact` como tool y enmendar el kernel §6/§7. Coste: reaparecen los dos fallos, y el diseño debe explicitar qué ocurre con una `Proposal` cuyo `FactAnalysis` nunca se registró. Tercera opción **no recomendada**: aprobar el retiro y meter otra tool para conservar el número nueve — convertiría el número en una cuota en vez de en una consecuencia. |
| **Impact** | (a) ADR-001 inv. 3 y val. 7 cambian de número; (b) desaparece el paso 12 del happy path como invocación y sus dos eventos pasan a la transacción de `ProposeFacts`; (c) ADR-006 inv. 3 conserva su semántica y cambia de sujeto (la validación de `inputs[]` la hace el Core, no una tool); (d) `FT-013` pasa a contar ocho y `F9` deja de ser test de tool; (e) `04`: la fila de `artifacts` y sus `artifact_inputs` se escriben en la misma transacción que `proposals`. |
| **Blocking?** | **YES — por B1 y B2.** B1: el corpus está partido — ADR-001 (nivel 1) dice **nueve**, y el Technical Design ya escribió el test que afirma **"exactamente ocho tools"** (`12` §4, `FT-013`) y la tabla transaccional que lo asume (`01` §4.3, fila 9). B2: el manifiesto es un **contrato ejercitado por un test de superficie con conteo exacto**; no es un detalle que se corrija después, porque el test que lo verifica es el mismo que sostiene **PF-002 y PF-004 por ausencia** (`15` §3.2, §3.4). |
| **Quién decide** | **Los dueños.** Amendment de ADR-001 (Accepted), con efecto en ADR-006 inv. 3 y en `vertical-slice-v0.md` (criterio estructural 1). |

---

### OD-03 — Librería de acceso a SQLite

| Campo | Contenido |
|---|---|
| **Decision** | ¿Sobre qué binding se implementa el adapter de persistencia: **`better-sqlite3`** o **`node:sqlite`**? (Una tercera, `sqlite3` de TryGhost, quedó **descartada**: su propio repositorio se declara sin mantenimiento — `HECHO VERIFICADO`.) |
| **Recommended option** | **`better-sqlite3`, detrás del `CaseStorePort`**, y reevaluar `node:sqlite` cuando alcance **Stability 2 — Stable**. Razón única y decisiva, con fuente: el propio proyecto Node documenta que las features Stability 1 *"no están sujetas a versionado semántico"* y que **su uso en producción no está recomendado** (`HECHO VERIFICADO`, índice de estabilidad de Node). `node:sqlite` está hoy en 1.2 — Release candidate, que es Stability 1. Construir el almacén canónico de expedientes jurídicos sobre esa etiqueta es aceptar que una actualización de Node rompa la persistencia. |
| **Alternative** | **`node:sqlite`.** Ventaja real y no despreciable: **cero dependencias externas**, sin toolchain ni prebuilds, lo que elimina de raíz el riesgo de instalación en Windows. Coste: superficie de rotura = cualquier release de Node; WAL **no mencionado** en su documentación (funciona vía `exec()` por `HIPÓTESIS` razonable, no por garantía documentada); FTS5 aparece en el fichero de build de la rama `main` pero **no** en la documentación de API — *fichero de build ≠ garantía de plataforma*. |
| **Impact** | Determina si `04` §11 puede resolver sus ocho `POR VERIFICAR`: FK por conexión, índices parciales, copia consistente e integridad para el backup, modo de contenido y tokenizer de FTS5, semántica de `synchronous` bajo WAL, `rename` con destino existente en Windows, PK de texto e índice implícito. **Todos son condicionales al driver**: ninguno se puede cerrar antes de elegir. Determina además el nivel **N3** completo (`12`), que por definición se escribe contra el driver real. |
| **Blocking?** | **YES — por B1.** Nadie ha decidido, y no hay precedencia que lo supla: es una decisión nueva. El `CaseStorePort` (spike §3.7) **acota el daño** —ningún tipo del driver cruza a `domain` ni `application`, y el contrato del puerto es asíncrono aunque ambos candidatos sean síncronos— pero no elimina el bloqueo: sin driver no hay N3, y sin N3 no hay verificación de que las constraints, la atomicidad, el orden bytes→fila y la migración con backup hagan lo que `04` dice. **Coste de desbloquear: bajo.** Es una decisión más una medición, no un problema de diseño. |
| **Quién decide** | **Technical Design propone; los dueños ratifican.** No es puramente técnica: el coste aceptado al elegir `better-sqlite3` es un **riesgo de producto** —un fallo de compilación en la instalación en la máquina de una profesional es un fallo de producto— y ese riesgo lo asume quien responde por el producto. |

**Medición previa obligatoria antes de ratificar (no es un spike nuevo; es cerrar el existente):** existencia de prebuild para el piso de Node elegido en `win32-x64` y, si aplica, `win32-arm64`.

---

### OD-04 — Granularidad de `HumanAuthorization` (aprobación de ADR-008)

| Campo | Contenido |
|---|---|
| **Decision** | ¿La `HumanAuthorization` es **una por `ProposalItem`** (kernel §3.2, ADR-008) o **una por `Proposal`** con `authorized_items[]` (ADR-005 §2, Accepted)? |
| **Recommended option** | **Una por item**, agrupadas por `review_session_id`. Dos razones: (i) la invalidación es **quirúrgica** — un cambio en un item no penaliza la aprobación de los demás, que es el defecto exacto de la forma por conjunto; (ii) **la forma por item puede representar la semántica en bloque, y no al revés**: si los dueños rechazaran la aprobación parcial, aprobar toda la Proposal son *N* autorizaciones creadas en la misma transacción con la misma `review_session_id`. |
| **Alternative** | Implementar la forma por Proposal de ADR-005 §2 y migrar después. Tercera opción **rechazada explícitamente** en `04` §10 C2: esquema doble — dos formas de autorizar es la peor de las tres. |
| **Impact** | Forma de `human_authorizations`: `proposal_item_id NOT NULL` + `item_content_hash` + índice parcial único por item vivo, frente a `proposal_id` + lista embebida. Condición (2) del gate de commit. Comportamiento de `AT-004` (modificar un item tras la aprobación). Contenido del payload de `ProposalReviewed`. |
| **Blocking?** | **YES — por B1 y B2.** B1: los dueños **aprobaron la aprobación parcial** (kernel §2 y §3, `DECISIÓN APROBADA`), lo que contradice la forma del contrato de un ADR **Accepted**; `04` §10 C2 dice literalmente que implementar por item *"requiere aprobación explícita: es enmienda de un ADR Accepted, no lectura de él"*. B2: la tabla y su índice parcial único son la forma del registro que **es** el permiso; cambiarla después es migrar autorizaciones ya emitidas, es decir, reescribir el rastro del acto humano. |
| **Quién decide** | **Los dueños.** Enmienda de ADR-005 §2 (Accepted). Se resuelve aprobando **ADR-008**, que ya está escrito y en estado `Proposed`. |

**Nota de alcance:** esta es la **única** parte de "aprobar los ADRs 007–011" que bloquea. El resto está en OD-10.

---

### OD-05 — Mecanismo de configuración del perfil efectivo

> **Detectada al evaluar, no encargada.** Se incluye porque cumple el criterio de bloqueo y porque dos comprobaciones obligatorias dependen de ella.

| Campo | Contenido |
|---|---|
| **Decision** | ¿Cómo se determina el **perfil efectivo de ejecución** (`production` / `development` / `test`) y cuál es la forma de la **Client Config** que el Core valida al arrancar? |
| **Recommended option** | Perfil efectivo **explícito y no inferible**: un valor declarado en la configuración compuesta, sin default permisivo — la ausencia de valor se trata como error de configuración, no como `development`. Client Config **validada por schema cerrado**, comparada campo a campo contra el Product Floor, con la secuencia de seis pasos de `15` §7.3 y `configuration_version` + hash del texto para reproducibilidad (`01` §7.1). |
| **Alternative** | Inferir el perfil del entorno (variable de entorno, presencia de artefactos de build, nombre de la carpeta). **Rechazable con argumento:** kernel §4 exige *fail to start* cuando la configuración es de producción y el provider resuelto es el stub; una inferencia que falle en el sentido permisivo convierte ese requisito duro en una lotería. |
| **Impact** | **`AT-013`** —el test de la `DECISIÓN APROBADA` de kernel §4— no es ejecutable sin la noción de "configuración efectiva de producción" (`12` §3.4 paso 1: *componer `FX-CFG-PROD`*). **El test de PF-005** tampoco (`12` §7: *"POR VERIFICAR: mecanismo de configuración del perfil efectivo"*). Y `15` §7.3 queda como contrato de comportamiento sin especificación implementable. |
| **Blocking?** | **YES — por B1.** No existe respuesta en ningún documento del corpus. Y lo que queda sin comprobar no es un detalle: es el mecanismo que impide que un build de producción opere con autorizaciones simuladas. |
| **Quién decide** | **Technical Design propone; los dueños ratifican.** Tiene componente de producto: define qué significa "producción" para un producto que se instala en la máquina de la usuaria. |

---

## 4. NO BLOQUEANTES — con mitigación construida

Cada bloque añade dos campos a los seis del formato: **qué cubre la mitigación** y **cuándo deja de estar mitigada**. Una mitigación sin fecha de caducidad es una decisión olvidada.

### OD-06 — Transporte del canal de autorización humana

| Campo | Contenido |
|---|---|
| **Decision** | ¿Por qué canal revisa la profesional y aprueba: elicitation MCP **modo URL**, UI local mínima, o CLI del runtime? |
| **Recommended option** | **No decidirlo todavía.** Cerrar el spike (`experiments/authorization-spike/`) y decidir con datos, aplicando los criterios de admisión de ADR-005 §5: consentimiento explícito por acto; superficie no inspeccionable ni accionable por el cliente ni por el LLM; vinculación verificable al contenido y a la revisión. |
| **Alternative** | Elegir ahora el candidato más barato (CLI) y sustituirlo después. Coste: bajo, precisamente por la mitigación — pero decidir sin datos un canal cuyo requisito es *probar un acto humano* es la clase de decisión que conviene no adelantar. |
| **Impact** | Ninguno sobre Domain, Application, el contrato de `HumanAuthorization` ni las condiciones UX. Los tres candidatos son **tres implementaciones del mismo puerto**. |
| **Blocking?** | **NO.** |
| **Quién decide** | **Los dueños** (producto/UX), informados por el spike. |
| **Qué cubre la mitigación** | El puerto `HumanAuthorizationProvider` (`06` §7) desacopla contrato y transporte con tres reglas que hacen la sustitución segura: (1) **el provider no emite autorizaciones, devuelve decisiones** —quien escribe `ProposalItemReview` y `HumanAuthorization` es el use case `ReviewProposal`, dentro de su transacción, para que el transporte no pueda fabricar el permiso—; (2) ausencia de decisión = `PENDING`, **fail closed** en timeout, cancelación o fallo; (3) `DevHumanAuthorizationProvider` **es parte del producto**, no un doble de test, y permite ejecutar N2, N6 y N7 completos con política determinista. |
| **Qué NO cubre** | Cualquier afirmación sobre **prueba de acto humano**. `HECHO VERIFICADO` del spike de Cowork: elicitation en modo form **no prueba acto humano en este stack** (existe hook que responde sin mostrar diálogo, con advertencia oficial). El diseño ya no depende del diálogo del host — pero tampoco puede prometer lo contrario. |
| **Cuándo deja de estar mitigada** | En el **primer uso real por una profesional**. A partir de ahí el stub no es admisible (kernel §4: *fail to start*), luego el transporte deja de ser opcional. **Dependencia dura: la mitigación solo es válida si `AT-013` pasa, y `AT-013` depende de OD-05.** |

---

### OD-07 — Proveedor de transcripción

| Campo | Contenido |
|---|---|
| **Decision** | Qué proveedor genera la `DerivedRepresentation` de audio, y si entrega marcas de tiempo **referidas al original** con granularidad al menos de segmento. |
| **Recommended option** | Mantener el **criterio de admisión** de `07` §4 —un proveedor que no entregue esas marcas **no es admisible para V0**— y medir candidatos en `experiments/transcription-spike/` antes de elegir. Fundamento: sin esa coordenada, el ancla de un audio solo podría expresarse como cita sobre el derivado, y un `EvidenceLink` así **viola ADR-003 inv. 7**: la cadena terminaría en un artefacto de la transcripción en lugar de en la prueba. |
| **Alternative** | Relajar el criterio y admitir proveedores sin timestamps utilizables, aceptando que para material de audio la resolución al original deje de ser posicional. **Consecuencia que habría que escribir:** `INV-D-33` pasa a `NOT_IMPLEMENTED` y ADR-003 inv. 7 queda comprometido para audio. |
| **Impact** | Diseño del locator de audio (`07` §3): `TIME_RANGE` vive en `original_locator`, nunca como selector sobre el derivado. Veredicto de `INV-D-33`. Coste y calendario del slice —el criterio puede excluir proveedores por lo demás adecuados (`RIESGO` declarado en `07` §4). |
| **Blocking?** | **NO.** |
| **Quién decide** | **Los dueños** ratifican el criterio de admisión (es una restricción de compra, no solo técnica); el equipo técnico ejecuta la medición. |
| **Qué cubre la mitigación** | **`FixtureDerivationProvider`** (`12` §2.9) — el doble que el encargo llama *FixtureTranscriptionProvider*; **el nombre canónico en el corpus es `FixtureDerivationProvider`** y este documento lo usa para no crear un segundo nombre. Devuelve la transcripción canónica del fixture con su mapa de timestamps (`FX-AUD`, `13` §6–§7) y marca `derivation_source = FIXTURE`. Con él son ejecutables `FT-002`, `FT-003` (incluido el camino negativo con `FailingDerivationProvider`), `FT-005` y **todo N7**. |
| **Qué NO cubre** | Que un proveedor real cumpla el criterio. Eso es **un hecho a medir, no a suponer** (`07` §4). Tampoco cubre la estabilidad de los timestamps entre ejecuciones, que es la propiedad de la que depende el re-anclaje de citas (`07` §5). |
| **Cuándo deja de estar mitigada** | Al incorporar el **primer audio real**. Sub-decisión asociada, hoy `PROPUESTA` sin aprobar (`12` §2.9): **FAIL-TO-START en producción también para `FixtureDerivationProvider`**, por analogía con kernel §4. Sin ella, un build de producción podría transcribir con el fixture y nadie lo notaría. |

---

### OD-08 — Identificador de entidad: UUIDv7 frente a ULID

| Campo | Contenido |
|---|---|
| **Decision** | ¿Los identificadores opacos de entidad son **UUIDv7** o **ULID**? Y, acoplado a ello, ¿cuál es el piso mínimo de Node en `package.json#engines`? |
| **Recommended option** | **UUIDv7**, generado con `crypto.randomUUIDv7()` de la biblioteca estándar, con piso `>= 24.16.0` (**Camino A** del spike). Tres razones en orden de peso: (1) **estatus normativo** — RFC 9562 es Standards Track del IETF y obsoleta el RFC 4122, frente a una especificación comunitaria; para un producto cuyo dominio es jurídico y que declara *vendor-independence*, apoyar la identidad de todas las entidades del expediente sobre una norma citable es cualitativamente distinto; (2) **cero dependencias de terceros para la identidad** — el elemento de infraestructura menos apropiado para depender de un paquete de npm; (3) interoperabilidad de tipo si POST-V0 apareciera PostgreSQL. |
| **Alternative** | **ULID** (26 caracteres, sin guiones, case-insensitive) o UUIDv7 vía librería, lo que permitiría piso `22.x`. El argumento a favor de ULID —ergonomía humana— **no gana** porque el kernel §11 exige identificadores **opacos**, y optimizar la legibilidad de algo que por diseño no se lee ni se dicta es optimizar una propiedad declarada irrelevante. |
| **Impact** | Piso de Node en `engines` (excluye 22.x en el Camino A); forma almacenada de todos los ids (`04` §5, D8: texto y no binario, reversible); nada más. |
| **Blocking?** | **NO.** |
| **Quién decide** | **Technical Design propone; los dueños ratifican el piso de Node**, porque el piso condiciona en qué máquinas se instala el producto. |
| **Qué cubre la mitigación** | `IdPort.newId() -> EntityId` (spike §2.7) aísla la generación en un único punto; y **en Fase 1 no existe ningún dato de producción**, luego cambiar de esquema de identidad cuesta regenerar fixtures, no migrar expedientes. |
| **Qué NO cubre** | Nada relevante: `NOT_FOUND` en el spike si `crypto.randomUUIDv7()` implementa contador monótono intra-milisegundo — y **es irrelevante por diseño**, porque el orden canónico del Case Event Log es **`event_seq`** y jamás el orden de los `event_id`. Ninguna consulta, proyección, hash-chain ni invariante puede depender de que ordenar por identificador produzca el orden de ocurrencia. |
| **Cuándo deja de estar mitigada** | En el **primer expediente real**. Después, cambiar de esquema de identidad es reescribir toda referencia del corpus. |

---

### OD-09 — Aprobación de las cinco políticas del Product Floor

| Campo | Contenido |
|---|---|
| **Decision** | (a) ¿Se aprueban las cinco políticas de kernel §12 tal como las formula `15`? (b) ¿Entra **PF-006** —el Case Event Log no es desactivable, editable ni podable por configuración— como sexta? |
| **Recommended option** | (a) Aprobarlas. (b) **Sí, entra** (opción (b) de `15` §6.4): el coste marginal en mecanismo es **cero** —append-only, trigger `RAISE(ABORT)` incondicional y hash-chain ya existen por ADR-004— y lo que se gana es que la garantía deje de ser revocable por un cambio de adapter. |
| **Alternative** | Mantener exactamente cinco y **retirar formalmente** la política 5 del anexo de `principles.md`, con su razón escrita. Lo que **no** es aceptable es que desaparezca por precedencia silenciosa. |
| **Impact** | Sobre el código de Fase 1: **ninguno para (a)**; todo el enforcement de las cinco ya lo exigen ADRs Accepted (ADR-001 inv. 1, ADR-003 inv. 2 y 8, ADR-006 inv. 1). Para (b): una regla más en el validador de configuración y su test. Sobre la documentación: si se aprueba (a) sin (b), hay que corregir `principles.md`. |
| **Blocking?** | **NO.** |
| **Quién decide** | **Los dueños.** El mecanismo del piso ya está aprobado (addendum v0.3 B.4); lo que se decide es el contenido. |
| **Qué cubre la mitigación** | Que las políticas **describan** garantías ya exigidas por nivel 1 de precedencia: no aprobarlas no permite escribir código distinto. |
| **Qué NO cubre** | **El test de PF-005**, que depende de **OD-05** (bloqueante). Y **PF-004**, cuya prueba vive hoy solo en la matriz funcional (`FT-013`) sin `AT` propio — decisión menor abierta en `12` §3.7, recomendación (a). |
| **Cuándo deja de estar mitigada** | Cuando se escriba el **validador de Client Config**: ahí hace falta la lista cerrada contra la que comparar, y `15` §7.4 muestra que sin PF-006 el validador **no tendría regla** contra la que rechazar una retención sobre el log. |

---

### OD-10 — Aprobación de ADR-007, ADR-009, ADR-010 y ADR-011

| Campo | Contenido |
|---|---|
| **Decision** | ¿Se ratifican los ADRs `Proposed` del ciclo Technical Design V0? **Estado verificado en disco hoy:** existen `ADR-007` (este ciclo), `ADR-008` y `ADR-011`; **`ADR-009` y `ADR-010` aún no están escritos** (en curso según `ESTADO-Y-HALLAZGOS-CRITICOS.md` §5). |
| **Recommended option** | Ratificarlos **después** de resolver OD-01, OD-02 y OD-04, porque esos tres cambian el texto de varios de ellos. Ratificar antes obligaría a re-ratificar. |
| **Alternative** | Implementar contra ADRs `Proposed` y ratificar al final. Es lo que ocurre por defecto si nadie decide; el coste es que la Fase 1 se construye sobre decisiones no registradas como arquitectura, que es exactamente la brecha que ADR-008 §Contexto describe. |
| **Impact** | Documental. Ninguno de los cuatro introduce un mecanismo que no esté ya especificado en su documento técnico hermano (`04`, `09`, `05`, `07`). |
| **Blocking?** | **NO** — con **una excepción ya escalada**: la parte de **ADR-008** que enmienda ADR-005 §2 **sí bloquea** y está en **OD-04**. |
| **Quién decide** | **Los dueños.** |
| **Qué cubre la mitigación** | Que un ADR `Proposed` cuyo contenido no contradiga un ADR Accepted es implementable sin riesgo de reversión: describe lo que el documento técnico ya especifica. |
| **Qué NO cubre** | ADR-009 y ADR-010 **no existen en disco**: no se puede afirmar que no contradigan nada hasta leerlos. Se declara como estado, no como garantía. |
| **Cuándo deja de estar mitigada** | Al cerrar la Fase 1: entregar un slice funcionando cuyas decisiones de arquitectura sigan en `Proposed` deja el corpus sin registro autoritativo de por qué el sistema es como es. |

---

### OD-11 — Punto B-04 del spike de Cowork

| Campo | Contenido |
|---|---|
| **Decision** | ¿Puede un **servidor MCP local** alcanzar rutas fuera de las carpetas adjuntadas —es decir, alcanzar el private state— **mientras el host no puede**? |
| **Recommended option** | **Ejecutar el protocolo empírico ya escrito** (`experiments/cowork-capability-spike/README.md`, 31 pasos, con la estructura de prueba en `experimental-root/`) **antes o en paralelo al inicio de la Fase 1**, no al final. Razón: un resultado desfavorable no cambia el diseño, pero **sí cambia la forma del despliegue** (Core como proceso independiente con permisos de sistema operativo propios, opción que ADR-002 ya contempla), y absorber ese cambio es mucho más barato antes de fijar el composition root. |
| **Alternative** | Aplazarlo hasta el final de la Fase 1. Coste: si sale desfavorable, se descubre con el sistema construido sobre un supuesto de empaquetado que hay que rehacer. |
| **Impact** | **Sobre el Technical Design: ninguno.** El diseño es independiente del anfitrión y los cinco hallazgos del spike **refuerzan, sin alterarlo**, el diseño de autorización server-side (`ESTADO-Y-HALLAZGOS-CRITICOS.md` §1.3). Sobre el compromiso con Cowork como host de producción: **decisivo**. |
| **Blocking?** | **NO para la Fase 1** tal como se define en §0 — **SÍ para comprometerse con Cowork como host de producción** (`ESTADO-Y-HALLAZGOS-CRITICOS.md` §4: *"no bloquea el Technical Design […] pero sí bloquea comprometerse con Cowork como host de producción"*). |
| **Quién decide** | El equipo técnico **ejecuta y reporta**; los **dueños** deciden el host a la vista del resultado. |
| **Qué cubre la mitigación** | Tres capas, todas ya decididas: (1) **la protección del case store es posicional, no una regla** — `case.db`, originales y event log fuera de toda carpeta adjuntable, que es literalmente lo que ADR-002 decidió; (2) **Cowork no es una frontera de seguridad, es defensa en profundidad** — la frontera real es el Core (ADR-001); (3) la autorización se resuelve **server-side**, sin token para el modelo: si el host puede auto-aprobar, cualquier diseño que confíe en su diálogo queda comprometido, **y el nuestro no lo hace**. |
| **Qué NO cubre** | La escritura directa sobre `private-state/` por herramientas genéricas del host. `12` §3.5 lo declara fuera de la matriz adversarial porque **es prueba de plataforma, no del Domain**, y lo remite a este punto. Es el `RIESGO` abierto de mayor gravedad del corpus. |
| **Cuándo deja de estar mitigada** | En el momento de **comprometerse con un host de producción**, que en el calendario es antes del primer usuario real y puede ser mucho antes que el final de la Fase 1. |

---

## 5. Decisiones pendientes que NO están en las listas anteriores, y por qué

Se enumeran para que su ausencia sea **decisión registrada** y no descuido. Ninguna cumple el criterio de §1.

| Decisión pendiente | Dónde vive | Por qué no bloquea |
|---|---|---|
| **`ProposalPreservedForReconciliation`** (C1): ¿evento, columna de estado, o conducta derivada? | `04` §10 C1 | **La precedencia resuelve**: ADR-004 (b)1 es una lista **cerrada** y **Accepted** que incluye el evento. `04` ya admite el valor en el `CHECK` de `event_type` sin escribirlo —admitir un valor que nadie produce no cuesta nada; omitirlo obligaría a migrar—. Recomendación registrada: opción 3 (preservación derivada, evento sin productor en V0, como `FactWithdrawn`). **Debe ratificarse antes del primer caso real**, no antes de escribir código |
| **Reingestión con procedencia declarada distinta** (C4): ¿fila nueva en `source_ingestions` con evento, o sin él? | `04` §10 C4; `12` `AT-007` | **La precedencia resuelve**: si registrar la procedencia adicional es mutación canónica, ADR-004 inv. 5 exige exactamente un evento. Eso es la opción 1, ya recomendada, con `event_id` nullable mientras se decide. El `UNIQUE(source_id, ingestion_hash)` garantiza que el reintento **idéntico** no cree filas |
| **Normalización de búsqueda: `ñ`** (D7) | `04` §6.2 | `04` la califica de *"bloquea el pipeline"*, y es correcto **para escribir el pipeline**, no para arrancar la Fase 1. Coste de reversión: **reindexar `derived_segments.text_normalized`**, que es dato **derivado y regenerable** — nunca dato canónico. Por el criterio B2, no bloquea. **Recomendación: conservar `ñ` como carácter propio y despojar solo tildes**, para no colapsar *año/ano* |
| **Valor por defecto de `expires_at`** (24 h propuesto) | `06` §11; `12` §3.6 | El test **no codifica el valor**: lo lee de la configuración efectiva, de modo que fijarlo o endurecerlo no rompe nada. La política solo endurece (PF-005) |
| **Extensión del rechazo de apertura a autorizaciones `DEV_STUB` no consumidas** | `06` §8.2; `12` §3.4 | `AT-013` cubre hoy el caso **consumido** y esa limitación se declara. Ampliar la regla después es aditivo. **Recomendación registrada: ampliarla** — la trampa actual es que un Case con `DEV_STUB` viva se abre, la primera llamada la consume commiteando con aprobación simulada, y **después** el Case queda inaccesible: el daño ocurre y luego se pierde el acceso |
| **`completeness`: dos valores vs tres** | `01` §9.3 (1) | Divergencia menor. El invariante *"`PARTIAL` ⇒ `omissions` no vacío"* se cumple en ambos. Requiere amendment de ADR-004 para adoptar dos, pero no impide escribir el envelope |
| **Retención y poda del Tool Invocation Log** | ADR-004; `04` §1 | El log es **no canónico y podable** por decisión. No decidir la política significa no podar, que es el estado seguro |
| **Recolección de blobs huérfanos** | `04` §7.4 | Operación del plano administrativo. No ejecutarla deja basura recuperable, nunca corrupción — el fallo barato que el orden bytes→fila elige a propósito |
| **Anclaje del hash-cabeza fuera del workspace** | `01` §11 | Refuerza el hash-chain frente a un adversario que ya está **fuera del threat model V0** (kernel §8.3). No cambia ninguna garantía declarada |
| **Deduplicación física de Sources** | `04` §7.4, §8 | Aditivo: tabla `blobs` con refcount + migración de layout. En V0 no hay deduplicación y la confidencialidad entre expedientes no depende de un refcount |
| **Hueco de numeración de `AT` para PF-004** | `12` §3.7 | La **cobertura ya existe** (`FT-013`); lo que falta es un identificador. Recomendación (a): referencia cruzada explícita desde `15` §3.4 — **ya escrita** |
| **`NOT_INCORPORATED` sin condición del catálogo UX** | `05` §4.3; `12` `AT-005` | El rechazo funciona y tiene código semántico estable. Lo que falta es cómo se le presenta a la usuaria |

---

## 6. Orden recomendado de resolución

Ordenado por dependencia, no por importancia.

```text
PASO 1 — sesion de decision de los duenos (no requiere trabajo tecnico previo)
         OD-01  modelo de revision  (A o B)  -> corrige la contradiccion del kernel
         OD-02  8 vs 9 tools               -> fija el manifiesto y FT-013
         OD-04  aprobar ADR-008            -> fija la forma de human_authorizations
         OD-09  aprobar las cinco PF (+ decidir PF-006)

PASO 2 — decision tecnica con ratificacion (requiere cerrar una medicion)
         OD-03  libreria SQLite   <- medir prebuilds win32 para el piso de Node
         OD-08  UUIDv7 + piso de Node  (acoplada a OD-03 solo por el piso)
         OD-05  perfil efectivo de configuracion   <- desbloquea AT-013 y PF-005

PASO 3 — en paralelo al inicio de la implementacion
         OD-11  ejecutar el protocolo B-04 (31 pasos)  <- antes de fijar el
                composition root, porque un resultado desfavorable cambia el
                empaquetado (Core como proceso independiente), no el diseno
         OD-07  spike de transcripcion  <- antes del primer audio real
         OD-06  spike de transporte     <- antes del primer usuario real

PASO 4 — al cerrar la Fase 1
         OD-10  ratificar ADR-007, 009, 010, 011 con el texto ya corregido
                por los resultados del PASO 1
```

**Los cuatro del PASO 1 no requieren ningún trabajo técnico previo.** Están analizados, con opciones escritas y recomendación registrada en su documento fuente. Es la observación más accionable de este documento: **cuatro de los cinco bloqueantes se resuelven en una sesión de decisión**, y el quinto (OD-05) es una propuesta técnica que cabe en la misma sesión.

---

## 7. Qué ocurre si no se decide nada

Declaración honesta, porque "queda pendiente" suele significar "se decidirá solo, mal y tarde":

| Si no se decide… | Lo que pasa por defecto | Por qué es peor que decidir |
|---|---|---|
| **OD-01** | El implementador elige entre dos respuestas del mismo documento normativo | La elección queda **sin registrar**, y el corpus sigue afirmando las dos cosas |
| **OD-02** | Se implementa lo que diga el último documento leído: `12` ya afirma ocho, ADR-001 afirma nueve | El test de superficie que sostiene **PF-002 y PF-004 por ausencia** queda escrito contra un manifiesto no ratificado |
| **OD-03** | Se elige el driver por conveniencia del primer día | Los ocho `POR VERIFICAR` de `04` §11 se dan por buenos sin comprobar, que es como se cuelan las garantías inventadas |
| **OD-04** | Se implementa por item (es lo que `04` ya escribió) | Se enmienda de facto un ADR **Accepted** sin que nadie lo apruebe — exactamente lo que `04` §10 C2 pide evitar |
| **OD-05** | "Producción" se infiere del entorno | El *fail to start* de kernel §4 pasa a depender de una inferencia; el stub podría operar en producción |
| **OD-09 (b)** | PF-006 no entra | La política 5 del anexo de `principles.md` desaparece **por precedencia silenciosa**, y el validador de configuración no tendrá regla contra la que rechazar una poda del log de auditoría |
| **OD-11** | Se construye asumiendo Cowork | Se descubre al final, con el sistema hecho, que el perímetro exige otro empaquetado |

---

**Referencias.** `00-technical-kernel.md` §2, §3, §4, §5.2, §6, §7, §8.3, §11, §12, §14, §15 · `01-system-design.md` §4.1, §4.3, §7.1, §9.1–§9.3, §10, §11 · `02-domain-model.md` §2.5 (`INV-D-33`) · `04-persistence-model.md` §1.3, §4, §5, §6.2, §7.3–§7.4, §8, §10 (C1–C5, D1–D8), §11 · `05-mcp-contract.md` §2, §4.3, §13 · `06-human-authorization.md` §7, §8, §11 · `07-provenance-and-locators.md` §3, §4, §5 · `09-events-and-audit.md` §8.2–§8.3 · `12-testing-strategy.md` §2.9, §3.1, §3.4–§3.7, §4, §7 · `13-synthetic-benchmark.md` §6, §7, §14 · `15-product-floor-proposal.md` §6, §7, §9 · `ESTADO-Y-HALLAZGOS-CRITICOS.md` §1, §3, §4, §5, §6 · `docs/research/runtime-dependencies-spike-v0.md` §2, §3 · `docs/research/cowork-runtime-spike-v0.md` · `experiments/cowork-capability-spike/README.md` · `experiments/transcription-spike/README.md` · `experiments/authorization-spike/README.md` · ADR-001 (inv. 3, val. 7), ADR-002, ADR-003 (inv. 2, 7, 8), ADR-004 ((b)1, (c), inv. 5, 7), ADR-005 (§2, §5, inv. 9–10), ADR-006 (inv. 1, 3, 7), ADR-008 (`Proposed`), ADR-011 (`Proposed`) · `docs/architecture/principles.md` (anexo Product Floor v0) · `docs/architecture/notes/addendum-correcciones-v0_3.md` B.2, B.4.
