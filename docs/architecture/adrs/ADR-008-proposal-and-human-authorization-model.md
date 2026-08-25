# ADR-008 — Modelo de Proposal con aprobación parcial y autorización humana server-side por item

## Estado

Proposed

## Contexto

ADR-005 (Accepted) fijó **quién** autoriza las operaciones sensibles y **con qué naturaleza**: two-phase obligatorio, autoridad humana no falsificable, y un registro `HumanAuthorization` **server-side** —ningún token portador cruza el contexto del modelo—. Dejó dos huecos declarados como preguntas pendientes:

1. **Pregunta pendiente 1 de ADR-005:** *"¿se admite aprobación parcial vía `authorized_items[]`, o toda Proposal se aprueba/rechaza en bloque? El contrato la deja preparada sin activarla."* El mismo hueco figura en ADR-001 (Preguntas pendientes) y en `boundaries.md` §2.2 y §Preguntas.
2. El **ciclo de vida de la Proposal** nunca se contrató: ADR-005 habla de `APPROVED (parcial o total)` y ADR-004 de `PRESERVED_FOR_RECONCILIATION`, sin máquina de estados ni unidad de identidad de los items.

Los dueños **aprobaron la aprobación parcial** y fijaron tres decisiones por item (`APPROVE`, `REJECT`, `PENDING`), recogidas en el kernel técnico v0.4 §2 y §3, junto con el requisito del `DevHumanAuthorizationProvider` con **FAIL TO START** (§4). Ese material es normativo para el Technical Design V0 pero **no está registrado como decisión de arquitectura**: hoy vive en un documento de nivel 2 (kernel §14) mientras contradice, en la forma del contrato, un ADR Accepted de nivel 1. Este ADR existe para cerrar esa brecha.

Lo que este ADR **no** reabre: la frontera de confianza (ADR-001), el techo epistémico de la IA (ADR-003), la semántica de `CaseRevision` y de conflicto (ADR-004), la naturaleza server-side y el two-phase (ADR-005), la incorporación de evidencia (ADR-006), la ausencia de criptografía en v0 y el transporte del canal humano (spike abierto).

El diseño técnico completo —contratos, máquina de estados, escenarios, puerto del provider— está en `docs/technical-design/v0/06-human-authorization.md`; este ADR registra las decisiones y sus consecuencias.

## Decisión

### 1. La unidad de revisión, de autorización y de commit es el **`ProposalItem`**, no la `Proposal`

Una `Proposal` es un contenedor con identidad; los `ProposalItem` son las unidades sobre las que una persona decide. Cada item lleva **identidad estable y opaca** (`proposal_item_id`, UUIDv7 emitido por el Core) — **nunca un índice posicional**: reordenar la propuesta no cambia ningún identificador. Cada item lleva además `item_content_hash`, hash SHA-256 de su **forma normalizada**, cuya regla de normalización es parte del contrato.

### 2. Dos dimensiones ortogonales, seis valores

```
review_decision : PENDING | APPROVED | REJECTED       ← decisión profesional
commit_state    : UNCOMMITTED | COMMITTED             ← hecho operacional
```

Respecto del enum de partida (`PENDING_REVIEW | APPROVED | REJECTED | DEFERRED | COMMITTED | INVALIDATED`):

- `PENDING_REVIEW` → `PENDING` (mismo valor, sin redundancia con el nombre de la dimensión).
- **`DEFERRED` eliminado**: no se distingue de `PENDING` por ningún comportamiento observable — mismo gate, mismo efecto sobre el commit, misma visibilidad en `pending`. Si aparece la necesidad de separar "no lo he mirado" de "lo dejo para después", es un matiz de `PENDING`, no un estado nuevo.
- **`COMMITTED` movido a su propia dimensión**: con un solo enum, el estado real "aprobado y todavía no commiteado" obliga a elegir cuál de los dos hechos representar y perder el otro.
- **`INVALIDATED` eliminado como estado almacenado; es derivado**: se computa comparando `item_content_hash` y `expected_case_revision` con los de la autorización. Almacenarlo permitiría que estado y realidad divergieran y exigiría un proceso invalidador —una fuente de bugs— para producir un dato que una comparación de dos campos ya da con certeza.

`commit_state` solo avanza `UNCOMMITTED → COMMITTED`, y únicamente para items cuya decisión de revisión **efectiva** sea `APPROVED`. No existe "descommitear": retirar un hecho ya `ALLEGED` es `WithdrawFact` sobre el `Fact` (use case diferido, ADR-003/ADR-004).

`ProposalItem.review_decision` almacena la **última decisión humana**; la **decisión efectiva** que usan el gate y las proyecciones es `PENDING` siempre que la aprobación haya quedado invalidada. Así el item "vuelve a `PENDING`" para todo observador sin que el sistema reescriba una decisión humana ni mute estado durante un commit rechazado.

### 3. `ProposalItemReview` es el registro append-only de la decisión

`{review_id, review_session_id, proposal_item_id, item_content_hash, decision, principal_id, reviewed_at, note}`. Append-only; una re-revisión es una fila nueva. Solo lo escriben humanos (`principal_type = HUMAN`, `provenance_kind = HUMAN_DECISION`). `APPROVED` produce además una `HumanAuthorization` en la misma transacción; `REJECTED` y `PENDING` no producen ninguna.

**El rechazo se registra aquí, no como autorización.** Esto responde a la pregunta literal que abrió el contrato: *reject genera decisión de revisión, no autorización*.

### 4. Contrato de `HumanAuthorization` — depurado

```
authorization_id · case_id · proposal_id · proposal_item_id · item_content_hash
expected_case_revision · authorized_operation · principal_id · authorization_source
created_at · expires_at · consumed_at
```

- **`decision` NO existe.** Una autorización solo se crea al aprobar; un objeto llamado "autorización" con `decision = REJECTED` es una contradicción de nombre y una trampa de lectura (cualquier consulta que olvide filtrar trataría un rechazo como permiso). **La existencia del registro ES el permiso.**
- **`single_use` NO es campo: es invariante**, materializado por `consumed_at`. Un booleano que siempre vale lo mismo no informa; invita a que alguien lo ponga en `false`.
- **`expires_at` SE CONSERVA.** El par (`item_content_hash`, `expected_case_revision`) invalida ante cualquier cambio, pero **no cubre el caso en que nada cambia**: un caso inactivo tres meses conservaría una aprobación consumible sin que nadie la haya vuelto a mirar. Valor por defecto configurable (propuesto: 24 h); la política **solo endurece**, nunca se relaja a "sin expiración".
- **`authorized_operation` SE CONSERVA aunque en v0 tenga un solo valor (`COMMIT_FACT`).** Sin él, una autorización obtenida para commitear un hecho autorizaría cualquier operación sensible futura —`RecordProfessionalDetermination` y `WithdrawFact` ya están nombrados y diferidos—; añadirlo después obligaría a migrar autorizaciones existentes asignándoles una operación **inferida**, es decir, a decidir retroactivamente qué autorizó una persona.

### 5. Una autorización **por item**, agrupadas por `review_session_id`

Si una autorización cubriera un conjunto, cambiar un solo item invalidaría la aprobación de todos los demás — penalizando a la profesional por una edición no relacionada. Con una autorización por item, la invalidación es **quirúrgica**. La unidad del acto de revisión —necesaria para auditoría y UX— se preserva mediante `review_session_id`, que vive en `ProposalItemReview`, y mediante un único evento `ProposalReviewed` por sesión que enumera las decisiones.

### 6. Cinco condiciones de validez, evaluadas en la transacción del commit

Una autorización es válida **si y solo si**, simultáneamente: (1) existe y `consumed_at IS NULL`; (2) `item_content_hash` coincide con el del item; (3) `expected_case_revision` coincide con la revisión vigente; (4) `authorized_operation` corresponde a la operación intentada; (5) no ha expirado.

Fallo de (1), (2) o (5) ⇒ `HUMAN_REVIEW_REQUIRED`. Fallo de (3) ⇒ `REVISION_CHANGED` con la propuesta preservada. Fallo de (4) ⇒ `OPERATION_NOT_PERMITTED`. En los cinco casos: **cero mutaciones, cero eventos**, nunca commit parcial silencioso, degradado ni reintento automático.

**El commit es todo-o-nada sobre los `item_ids[]` recibidos**: si alguna condición falla para cualquier item de la lista, se rechaza la llamada completa y la condición nombra los items ofensores. Ante un invocador no confiable, el fail-closed es preferible a un éxito parcial que el modelo debe interpretar y relatar correctamente.

### 7. La autorización es **server-side**: el modelo no recibe nada

`commit_reviewed_facts(case_id, proposal_id, item_ids[], expected_revision)` no admite —ni sintáctica ni semánticamente— ningún campo que transporte prueba de revisión humana. El Core resuelve contra su propio registro si existe autorización válida para cada item. Ninguna respuesta de tool devuelve `authorization_id`. Superficie de ataque en el contexto del modelo: **cero tokens**.

### 8. `HumanAuthorizationProvider`: puerto que desacopla contrato y transporte

Driven port de Application con `kind: REAL | DEV_STUB` y una operación `requestReview(request) → outcome`. Reglas duras: **el provider devuelve decisiones, nunca acuña autorizaciones** (quien escribe `ProposalItemReview` y `HumanAuthorization` es el use case `ReviewProposal`); `authorization_source` deriva de `provider.kind` y jamás de datos devueltos por el adapter; el eco del `item_content_hash` se verifica y una discrepancia descarta la respuesta completa; ausencia de decisión, timeout o fallo del transporte se tratan como `PENDING` (**fail closed**: ninguna ruta de error produce `APPROVED`).

### 9. `DevHumanAuthorizationProvider`: FAIL TO START y marca indeleble

1. **FAIL TO START, no warning.** Configuración efectiva de producción + provider stub ⇒ el arranque **aborta**. No hay modo degradado ni advertencia ignorable. Perfil de ejecución indeterminado ⇒ se trata como producción (fail-closed).
2. **Marca indeleble.** Toda autorización emitida por el stub lleva `authorization_source = DEV_STUB`, persistida y propagada al evento `ProposalReviewed` (que es también el registro de auditoría). El Core rechaza abrir en modo producción un Case que contenga autorizaciones `DEV_STUB` consumidas; este ADR propone extender el rechazo a las **no consumidas** para cerrar la trampa descrita en Riesgos.

## Invariantes derivados

1. La identidad de un `ProposalItem` es opaca, emitida por el Core y **no posicional**; reordenar una propuesta no altera ningún `proposal_item_id` ni ningún `item_content_hash`.
2. `commit_state` avanza únicamente `UNCOMMITTED → COMMITTED` y solo para items cuya decisión de revisión efectiva sea `APPROVED`; las combinaciones `REJECTED + COMMITTED` y `PENDING + COMMITTED` son inalcanzables.
3. La invalidación de una aprobación es **derivada, jamás almacenada**: se computa desde `item_content_hash`, `expected_case_revision`, `consumed_at` y `expires_at`.
4. Ninguna `HumanAuthorization` existe sin un `ProposalItemReview` con `decision = APPROVED` creado en la misma transacción; el recíproco también vale (toda fila `APPROVED` produce exactamente una autorización).
5. `ProposalItemReview` es append-only y solo lo escriben principals con `principal_type = HUMAN`; ningún `principal_type = AI` produce una fila.
6. Toda `HumanAuthorization` es de un solo uso: `consumed_at` no nulo la inutiliza definitivamente y **no se revive** por ningún camino.
7. Un commit rechazado produce **cero mutaciones y cero eventos** del Case Event Log; solo deja traza en el Tool Invocation Log.
8. Ningún input de la superficie MCP transporta prueba de revisión humana, y ninguna salida expone `authorization_id`.
9. `authorization_source` se deriva del provider resuelto en composición, nunca de datos suministrados por el adapter, y es indeleble una vez persistido.
10. Configuración de producción con provider stub ⇒ el proceso **no alcanza estado operativo**.
11. Una autorización nunca se recicla ni se "actualiza" a una revisión o a un contenido nuevos: cambiar cualquiera de los dos exige una decisión humana nueva.

## Consecuencias positivas

- **Se cierra la pregunta pendiente 1 de ADR-005** con un mecanismo, no con un campo preparado: la aprobación parcial pasa de contrato latente a máquina de estados verificable.
- **Invalidación quirúrgica.** Un cambio en un item no destruye el trabajo de revisión hecho sobre los demás.
- **La fricción se vuelve granular y por tanto más deliberada.** Aprobar hecho por hecho es peor negocio para el clic reflejo que aprobar en bloque: mitiga la fatiga de revisión en vez de agravarla, y la tasa de rechazo por item es una señal medible de que la revisión ocurre.
- **Menos estado que puede mentir.** Eliminar `DEFERRED` e `INVALIDATED` como estados almacenados elimina dos clases enteras de divergencia entre lo registrado y lo real, igual que ADR-003 hizo con los estados derivados del `Fact`.
- **El rechazo deja de ser un hueco.** `ProposalItemReview` da dueño al "no", que antes solo existía como ausencia de autorización.
- **Transporte verdaderamente intercambiable.** El puerto convierte el criterio de admisión de ADR-005 §5 en algo comprobable en código de test: la vinculación verificable es la regla del eco de hash.
- **El stub deja de ser un riesgo latente.** FAIL TO START convierte "producción con aprobación simulada" en un fallo ruidoso e imposible de ignorar, y la marca indeleble hace que un caso de desarrollo nunca pueda hacerse pasar por real.

## Consecuencias negativas

- **Más entidades y más filas.** Una autorización por item y una fila de revisión por decisión multiplican el volumen respecto de un registro por propuesta; el coste es real aunque modesto para el tamaño de caso previsto.
- **Más superficie de consulta.** Determinar el estado efectivo de un item exige leer item, última revisión, autorización y revisión vigente del Case. La simplicidad se paga en joins, no en riesgo.
- **El todo-o-nada del commit puede bloquear un lote** por un solo item inválido. Se acepta a cambio de respuestas inequívocas; se mitiga porque la condición enumera los items ofensores y el reintento con el subconjunto válido es inmediato.
- **La distinción entre decisión almacenada y decisión efectiva es sutil** y puede confundir a quien lea el esquema sin leer el contrato. Exige que las proyecciones expongan siempre la efectiva y nunca la almacenada.
- **Aumenta la carga del canal humano:** una UX de revisión por item es más trabajo de producto que un botón de aprobar propuesta.
- **La condición 4 queda sin disparador en v0** (un solo valor en el enum): es una guarda que se paga hoy y sirve mañana.

## Alternativas consideradas

1. **Aprobación en bloque de toda la Proposal (statu quo de ADR-005 sin activar `authorized_items[]`) — RECHAZADA.** Es más simple, pero fuerza a la profesional a aceptar o descartar un paquete completo: en un dominio donde de cinco hechos propuestos por un modelo dos suelen ser correctos, obliga a rechazar todo o a aprobar lo que no se cree. Además hace catastrófica cualquier invalidación.
2. **Una autorización para un conjunto de items (`authorized_items[]` tal como estaba propuesto en ADR-005 §2) — RECHAZADA.** Permite aprobación parcial, pero la unidad de invalidación sigue siendo el conjunto: cambiar un item mata la aprobación de todos. La autorización por item logra lo mismo sin ese acoplamiento, al precio de más filas.
3. **Enum único de seis estados con `DEFERRED` e `INVALIDATED` — RECHAZADA.** Mezcla decisión profesional con hecho operacional (pierde el estado "aprobado y no commiteado"), añade un valor sin comportamiento propio y almacena como estado algo computable que puede divergir de la realidad.
4. **Índice posicional como identidad del item — RECHAZADA.** Convierte la aprobación en la aprobación de una **ranura**, no de un contenido: cualquier reordenación —incluso un `ORDER BY` no determinista— transfiere una aprobación a otro hecho, sin necesidad de mala fe. Además regala al modelo identificadores adivinables, contra ADR-001 inv. 7.
5. **Que el provider acuñe la `HumanAuthorization` — RECHAZADA.** Un adapter defectuoso o comprometido podría fijar `expected_case_revision`, `expires_at` o `authorization_source`: el transporte fabricaría el permiso, que es exactamente lo que ADR-005 impide para el modelo. El transporte informa; el Core decide y registra.
6. **Escribir un `ProposalItemReview` de sistema para "devolver el item a `PENDING`" — RECHAZADA.** Rompe dos reglas a la vez: mutaría estado durante un commit que debe producir cero mutaciones, y metería un `principal_type = SYSTEM` en un registro contratado como exclusivamente humano. La decisión efectiva derivada logra el mismo efecto observable sin ninguna de las dos.
7. **Warning en lugar de FAIL TO START para el stub en producción — RECHAZADA.** Una advertencia es un mensaje que alguien debe leer en el arranque de un servicio que nadie mira. El modo de fallo que previene —producción con aprobación humana simulada— vacía a la vez **todas** las garantías de ADR-005, en silencio.
8. **Token portador de un solo uso entregado al modelo — YA RECHAZADA en ADR-005 (alternativa 2).** No se reabre; este ADR la materializa: no hay campo en el contrato de la tool que pudiera transportarlo.

## Riesgos

- **RIESGO — Fatiga de revisión, ahora por item.** La granularidad mitiga el clic reflejo pero multiplica el número de decisiones. Si la lista es larga, la profesional puede aprobar en barrido. Mitigaciones a diseñar post-contrato (heredadas de ADR-005): revisar diffs y no bloques, fricción proporcional a la sensibilidad, y **medir la tasa de rechazo por item** como señal: si nunca se rechaza nada, la revisión probablemente no está ocurriendo.
- **RIESGO — Falsos conflictos de revisión.** `CaseRevision` es un contador por Case: incorporar evidencia no relacionada invalida autorizaciones vivas (ADR-004, riesgo de granularidad). Camino declarado si genera fatiga: revisiones por agregado antes que cualquier locking. No se diseña aquí.
- **RIESGO — Calibración de `expires_at`.** Demasiado corta: re-revisiones irritantes. Demasiado larga: ventana de desincronización mayor. **SUPUESTO a validar con la usuaria real.**
- **RIESGO — Trampa del `DEV_STUB` no consumido.** Con la regla literal del kernel (rechazo solo ante `DEV_STUB` **consumidas**), un Case con una autorización stub viva se abre en producción, el primer commit la consume —commiteando un hecho con aprobación simulada— y desde ese instante el Case ya no se puede abrir: el daño ocurre **y** el expediente queda inaccesible. Por eso este ADR propone extender el rechazo a cualquier autorización `DEV_STUB`.
- **RIESGO — La condición (2) no tiene disparador en el flujo normal de v0.** Los `ProposalItem` son inmutables tras su creación: la guarda de contenido protege contra manipulación del store fuera de la superficie y contra un futuro use case de edición, y se ejercita en test sembrando la divergencia. Debe documentarse como guarda, **nunca** presentarse como capacidad de producto.
- **RIESGO — Ausencia de firma (heredado, ADR-005 §6).** La fuerza probatoria de la autorización es la del hash-chain y la del perímetro del private state (ADR-002): tamper-evident, no tamper-proof frente a un actor con control total de la máquina. Límite asumido por el modelo de amenaza v0.
- **RIESGO — Confusión entre decisión almacenada y decisión efectiva.** Si una proyección expusiera la almacenada, mostraría como aprobado algo que no puede commitearse. Mitigación: contract test sobre `get_case_context(pending)`.

## Validación / pruebas necesarias

| # | Escenario | Resultado exigido | Invariante |
|---|---|---|---|
| 1 | `AT-002` — el modelo inventa una autorización: campo fabricado, o afirmación conversacional de que ya se revisó | Campo fabricado ⇒ rechazo **sintáctico** en el adapter; afirmación ⇒ no es input del Core. `HUMAN_REVIEW_REQUIRED`; cero mutaciones | 7, 8 |
| 2 | `AT-003` — segundo commit con autorización ya consumida | Rechazo; la autorización no se revive; ningún `Fact` recibe una segunda entrada `ALLEGED` | 6, 7 |
| 3 | `AT-004` — divergencia entre `item_content_hash` de la autorización y del item (sembrada a nivel de store) | Rechazo; cero mutaciones; decisión efectiva del item pasa a `PENDING`; el `ProposalItemReview` histórico se conserva íntegro | 3, 7, 11 |
| 4 | `AT-008` — la `CaseRevision` cambió entre revisión y commit | Rechazo; `REVISION_CHANGED {expected, current, preserved_proposal_id}`; propuesta preservada y visible en `pending`; el trabajo no se descarta | 7, 11 |
| 5 | Autorización expirada | Rechazo; `HUMAN_REVIEW_REQUIRED`; se exige nueva revisión | 3, 7 |
| 6 | Autorización con `authorized_operation` distinto de la operación intentada (guarda sin disparador en v0) | Rechazo; `OPERATION_NOT_PERMITTED` | 7 |
| 7 | `AT-013` — arranque con configuración de producción y provider stub | El proceso **no alcanza estado operativo** | 10 |
| 8 | Autorización emitida por el stub | `authorization_source = DEV_STUB` en el registro y en el payload del evento; alterarla rompe el hash-chain; apertura en modo producción rechazada | 9 |
| 9 | Property test de identidad | Permutar el orden de los items de una propuesta ⇒ `proposal_item_id` e `item_content_hash` idénticos | 1 |
| 10 | Property test de pareja revisión↔autorización | Por sesión: `count(HumanAuthorization) == count(ProposalItemReview where decision = APPROVED)`; ninguna autorización huérfana | 4 |
| 11 | Intento de escritura en `ProposalItemReview` con `principal_type = AI`, o `UPDATE` de una fila existente | Rechazo; el registro es append-only y humano | 5 |
| 12 | Intento de commit de un item con decisión efectiva `PENDING` o `REJECTED` | Rechazo; `commit_state` no avanza | 2 |
| 13 | Test de superficie | El esquema de `commit_reviewed_facts` no declara ningún campo de prueba de revisión; ninguna respuesta de tool contiene `authorization_id` | 8 |
| 14 | Camino feliz | 3 items (`APPROVE`/`REJECT`/`PENDING`) ⇒ 1 autorización, 3 `ProposalItemReview` con el mismo `review_session_id`, 1 `ProposalReviewed`, 1 `FactsCommitted`, `consumed_at` marcado, `Fact` con entrada nueva `ALLEGED` | 2, 4 |

**POR VERIFICAR:** la numeración definitiva del catálogo `AT-xxx` y su correspondencia con los 10 tests adversariales de `vertical-slice-v0.md` §Test matrix.

## Preguntas pendientes

1. **RESUELTA — Aritmética de revisiones (enmienda AC-02, aprobada).** Los dueños aprobaron separar `event_seq` de `case_revision`: `ProposalReviewed` avanza `event_seq` y lleva `case_revision` **nula**; `expected_case_revision` es la revisión **contra la que se generó y se revisó la Proposal**, con lo que desaparece la definición circular anterior. ADR-004 y ADR-005 quedan enmendados (supersedes §16.16 y §16.19). El modelo anterior —todo evento avanzaba la revisión— queda superado.
2. **DECISIÓN PENDIENTE — `ProposalPreservedForReconciliation`.** Figura en la lista cerrada de eventos de ADR-004 y no en la del kernel §8.1. Si la preservación es un rótulo derivado, el evento **no tiene productor**. Opción recomendada: conservarlo en la lista declarado sin productor en v0, el mismo patrón que ADR-004 ya aplica a `FactWithdrawn`. Ver el bloque de conflicto en `06-human-authorization.md` §5.4.
3. **DECISIÓN PENDIENTE — Atomicidad del commit** todo-o-nada sobre `item_ids[]` (Decisión §6).
4. **DECISIÓN PENDIENTE — `review_id` en `HumanAuthorization`** para trazabilidad explícita autorización↔decisión, en vez de inferirla por join sobre `(proposal_item_id, item_content_hash)`. El kernel §3 fija la lista de campos y no lo incluye.
5. **DECISIÓN PENDIENTE — Extensión del rechazo de apertura en producción** a autorizaciones `DEV_STUB` **no consumidas** (Decisión §9, riesgo de la trampa).
6. **SUPUESTO a validar — `expires_at` por defecto** (propuesto: 24 h) y política de endurecimiento.
7. **DECISIÓN PENDIENTE — Transporte del canal humano** (spike abierto de ADR-005 §5; elicitation MCP modo URL con soporte del host **POR VERIFICAR**, UI local mínima, CLI). No afecta a este ADR: el puerto lo aísla.
8. **DECISIÓN PENDIENTE — Qué operaciones entrarán en `authorized_operation`** cuando la superficie crezca (`RecordProfessionalDetermination`, `WithdrawFact` son las candidatas ya nombradas) y con qué criterio de admisión.
9. **POR VERIFICAR — Soporte de UUIDv7** en el runtime elegido (kernel §11, spike de dependencias). Alternativa equivalente: ULID.
10. **POST-V0 — Edición de un `ProposalItem` durante la revisión**, que sería el disparador real de la condición (2), y **re-autorización en lote** tras `REVISION_CHANGED` — útil contra la fatiga, y precisamente el mecanismo capaz de vaciar la revisión de contenido.

## Relaciones con otros ADRs

- **ADR-005 (autoridad humana) — este ADR lo REFINA, no lo reabre.** Conserva íntegras sus decisiones nucleares: two-phase obligatorio, registro server-side, cero secretos en el contexto del modelo, un solo uso, expiración, transporte desacoplado y ausencia de criptografía en v0. **Responde su pregunta pendiente 1** (aprobación parcial: **sí**, por item) y, en consecuencia, **sustituye la forma del contrato de su §2**: `authorized_items[]` desaparece a favor de `proposal_item_id`; `proposal_content_hash` se sustituye por `item_content_hash`; `operation` se nombra `authorized_operation` con valor `COMMIT_FACT`; se añaden `authorization_source` y el registro `ProposalItemReview`. **Mientras este ADR siga en `Proposed`, el esquema literal de ADR-005 §2 conserva su precedencia de nivel 1** (kernel §14) y esta sustitución no está vigente. Nota adicional: el invariante 1 de ADR-005 escribe `actor_type = HUMAN_DECISION`, forma que el kernel §1.5 normaliza —**decisión aprobada de los dueños**— a `provenance_kind = HUMAN_DECISION` + `principal_type = HUMAN`; el texto histórico no se corrige, no se reproduce.
- **ADR-001 (frontera de confianza):** este ADR es la instrumentación fina de su invariante 4 ("lo sensible exige autorización humana server-side") y de su invariante 7 (ids opacos emitidos por el Core), que aquí prohíbe la identidad posicional del item. Cierra también su pregunta pendiente sobre aprobación parcial.
- **ADR-003 (modelo de dominio epistémico):** la transición que este ciclo habilita es exactamente `PROPOSED → ALLEGED`. La regla dura "ningún actor `AI_*` más allá de `PROPOSED`" es el invariante de dominio que el gate de commit vuelve ejecutable. La doctrina "no almacenar lo que se puede computar" —origen de los estados derivados del `Fact`— es la misma que elimina `INVALIDATED`. La asimetría (el `ProposalItem` sí materializa `review_decision`) se justifica porque `Proposal` es un **concepto de soporte de Application**, no una entidad epistémica.
- **ADR-004 (estado canónico y proyecciones):** aporta `CaseRevision`, el Case Event Log y la semántica de conflicto (`REVISION_CHANGED` + preservación) que la condición (3) reutiliza; `get_case_context(pending)` es donde la propuesta preservada se hace visible y `changes_since(revision)` el insumo natural de la re-revisión. Dos puntos abiertos con él: la aritmética de revisiones (pregunta 1) y `ProposalPreservedForReconciliation` (pregunta 2).
- **ADR-002 (Protected Local Case Store):** el registro de autorizaciones y las filas de revisión viven en el private state, alcanzables solo por el camino único host → Legal MCP → Application → Case Store. Sin ese perímetro, escribir directamente una fila bastaría para simular una revisión humana; la ausencia de firma en v0 se apoya precisamente en él. La marca `DEV_STUB` y el rechazo de apertura en producción son reglas de ese store.
- **ADR-006 (frontera de incorporación):** reciprocidad. ADR-006 controla **qué puede fundamentar** una transición canónica —los `EvidenceLink` propuestos en el payload de un item solo pueden anclar a Evidence formalmente incorporada—; este ADR controla **quién puede consolidarla** y **con qué granularidad**.
- **Documento técnico asociado:** `docs/technical-design/v0/06-human-authorization.md` (contratos completos, máquina de estados, puerto del provider, escenarios `AT-002` / `AT-003` / `AT-004` / `AT-008`, trazabilidad invariante→prueba).
