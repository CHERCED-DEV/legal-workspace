# ADR-009 — Estrategia de eventos y auditoría: un log canónico hash-chained, un log operacional podable y dos contadores

## Estado

Proposed

> **Nota de vigencia (obligatoria para leer la Decisión 5).** La **enmienda AC-02 fue APROBADA por los dueños** sobre ADR-004 y ADR-005 (supersede §16.16 y §16.19). En consecuencia, **la Decisión 5 de este ADR ya no es una propuesta: describe el modelo vigente** —dos contadores, `ProposalReviewed` con `case_revision` nula, `expected_case_revision` = la revisión contra la que se generó y se revisó la Proposal—, y lo está por virtud de esas enmiendas, no por el estado de este ADR. El resto de decisiones de este ADR conserva su estado `Proposed`. También se aprobaron **AC-01** (autorización por item), **AC-03** (superficie MCP de ocho tools) y **AC-04** (`ProposalPreservedForReconciliation` sin productor en v0), que este ADR recoge donde le afectan.

## Contexto

ADR-004 (Accepted) fijó el modelo de memoria del caso y, dentro de él, **tres conceptos de registro sobre dos persistencias**: el Case Event Log canónico (que unifica Domain/Application Event y Audit Record), el Tool Invocation Log operacional, y el rechazo explícito de full event sourcing. Fijó también la semántica de `CaseRevision`: un contador monotónico por Case donde **cada evento la incrementa** y `seq == revision` resultante.

Desde entonces han aparecido cinco hechos que ese ADR no pudo considerar y que hoy exigen una decisión de arquitectura:

1. **La preimagen del hash quedó sin cerrar.** ADR-004 exige un log "hash-chained" y el kernel v0.4 §8.1 escribe `event_hash = H(event_id, event_seq, prev_event_hash, payload_hash, …)` con puntos suspensivos. Una cadena cuya preimagen no está especificada —incluida la forma canónica de serializar el payload— **no verifica nada**: dos serializaciones del mismo contenido producen dos hashes distintos.
2. **La corrección semántica `Principal` ≠ `provenance_kind`** (kernel §1, DECISIÓN APROBADA de los dueños) cambia la cabecera del evento: donde el corpus previo escribía `actor_id / actor_type / actor_role` con `actor_type` tomando valores del enum epistémico, ahora hay dos dimensiones ortogonales, y ambas deben entrar en el hash o **quién hizo qué** sería reescribible sin romper la cadena.
3. **La aprobación parcial por item** (kernel §2 y §3, aprobada; contratada en ADR-008 Proposed) cambia el contenido del evento `ProposalReviewed` y hace que las variantes `approved/rejected/partial` de la lista cerrada de ADR-004 dejen de ser tipos y pasen a ser una lectura derivada.
4. **El kernel §5.2 planteó un ADR AMENDMENT CANDIDATE sobre ADR-004**: separar `event_seq` (todo evento) de `case_revision` (solo mutación del estado epistémico canónico), de modo que la revisión humana **no** avance el reloj del conocimiento. Los dueños pidieron justificación formal y exigieron no cambiarlo en silencio. **Lo aprobaron después como enmienda AC-02**, de modo que este hecho dejó de ser una pregunta abierta y pasó a ser el modelo vigente (ADR-004 supersede §16.16; ADR-005 supersede §16.19).
5. **El spike documental de Cowork** produjo HECHOS VERIFICADOS contra documentación oficial (`docs/research/cowork-runtime-spike-v0.md`; síntesis en `docs/technical-design/v0/ESTADO-Y-HALLAZGOS-CRITICOS.md` §1.1): Cowork **no** hereda la configuración de Claude Code, **no** existe deny por ruta, y los servidores MCP locales corren en el host. Consecuencia para la auditoría: **la protección del log no puede apoyarse en reglas del anfitrión, solo en su posición dentro del private state** (ADR-002) y en la evidencia de manipulación que aporta la cadena. No invalida ninguna decisión Accepted; sí elimina la defensa en profundidad que se daba por supuesta delante de ella.

A esto se sumó un hallazgo de coherencia del corpus técnico: **convivieron dos aritméticas de revisión simultáneas**. `01-system-design.md` aplicaba el Modelo A por precedencia (con columna explícita del B); `03-application-use-cases.md` llegó a aplicar el Modelo B siguiendo la tabla del kernel §7; `04-persistence-model.md` y `09-events-and-audit.md` se mantenían neutrales. Los cuatro declaraban el conflicto —ninguno lo ocultó— pero **numeraban los mismos pasos con valores distintos**, y se dijo que la decisión no podía seguir aplazada sin coste. **Ya no lo está: AC-02 la cerró.** Lo que queda es trabajo acotado de **normalización cruzada** —`09-events-and-audit.md` ya está normalizado; `01`, `03`, `06` y `vertical-slice-v0.md` deben quedar con los valores del Modelo B—. **POR VERIFICAR:** qué documentos hermanos están ya normalizados.

Lo que este ADR **no** reabre: la frontera de confianza (ADR-001), el perímetro del private state (ADR-002), el modelo epistémico y sus estados derivados (ADR-003), el contrato de proyecciones `get_case_context` (ADR-004 (a)), la naturaleza server-side de la autorización humana (ADR-005, ADR-008), la frontera de incorporación (ADR-006) ni la ausencia de criptografía en v0.

El diseño técnico completo —schema del `CaseEvent`, payload de los once tipos de evento, algoritmos de append y verificación, schema y retención del log operacional, y el desarrollo íntegro de la enmienda AC-02 con el modelo vigente y el superado— está en `docs/technical-design/v0/09-events-and-audit.md`. Este ADR registra las decisiones y sus consecuencias.

## Decisión

### 1. Un solo log canónico: el evento **es** el registro de auditoría

Se confirma y se materializa ADR-004 (b)1. `case_events` vive en `case.db`, es **append-only** y **hash-chained**, y porta en la misma fila el qué (`event_type`, `payload`), el quién (`principal_id / principal_type / principal_role`), la naturaleza epistémica (`provenance_kind`), el con-qué (`methodology_version`, `model_id`, `knowledge_pack_versions`) y la cadena (`prev_event_hash`, `payload_hash`, `event_hash`).

El argumento decisivo no es de economía sino de veracidad: **dos streams paralelos crean una pregunta irresoluble el día que divergen.** Si un log forense afirma que la profesional aprobó un item y el log de dominio no tiene el evento, no existe criterio para decidir cuál miente — y "no sabemos cuál de nuestros dos registros es correcto" es peor, en un expediente jurídico, que no tener el segundo.

Consecuencia aceptada: **el formato del evento es un contrato de auditoría**, no un detalle interno. Cambiarlo es cambio de contrato, con las mismas consecuencias que abrir la lista de eventos.

### 2. El Tool Invocation Log permanece separado, sin cadena y podable

`tool_invocations` vive en `operational.db`, **sin claves foráneas**, sin `event_seq`, sin hash y sin `provenance_kind`. Registra **toda** invocación MCP, incluidas las `QUERY` y **sobre todo las rechazadas**.

Cuatro razones estructurales, ninguna de volumen:

1. **Debe poder registrar lo que el estado canónico no admite.** El test adversarial exige traza de invocaciones con `case_id` inexistente, ids fabricados por el modelo y rutas de path traversal. Una FK a `cases` haría **imposible registrar precisamente los intentos que el Core rechazó**.
2. **Registra invocación, no mutación.** La biyección de ADR-004 inv. 5 es mutación↔evento; nueve lecturas seguidas no son nueve hechos del expediente.
3. **Es podable y el canónico no.** Podar el archivo que contiene la cadena sería operar sobre el objeto cuya integridad se quiere demostrar.
4. **No debe parecer que participa de la cadena.** Compartir tabla llevaría a encadenarlo "por coherencia", y la verificación de la auditoría pasaría a depender de filas que una política de retención borra.

No lleva `provenance_kind` porque una invocación **no tiene naturaleza epistémica**: nada se sabe *a través de* una llamada a tool.

### 3. Preimagen del hash cerrada, con forma canónica especificada

`payload_hash = SHA-256(bytes canónicos del payload)`. `event_hash = SHA-256` sobre una preimagen que incluye, con un separador de campo inyectivo y un **separador de dominio versionado** (`legal-os/case-event/v1`): `event_id`, `case_id`, `event_seq`, `case_revision` (**también cuando es nulo**), `event_type`, `payload_hash`, la tripla `principal_*`, `provenance_kind`, metodología/modelo/packs, `occurred_at` y `prev_event_hash`.

Cuatro reglas, cada una cerrando un fallo concreto:

- **Separador de dominio versionado**: impide reutilizar un digest computado en otro contexto como si fuera un `event_hash`, y hace que un cambio de preimagen produzca hashes distintos por construcción, de modo que un cambio de contrato de auditoría no pueda pasar inadvertido.
- **Separador de campo que no puede aparecer en los campos**: sin él, `("ab","c")` y `("a","bc")` comparten preimagen.
- **La cabecera entra completa**: si `principal_*` o `provenance_kind` quedaran fuera, **quién hizo qué sería reescribible sin romper la cadena** — precisamente el dato que convierte el evento en registro de auditoría.
- **`case_revision` entra aunque sea nulo**: de lo contrario podría rellenarse a posteriori, borrando la distinción entre los dos contadores de la decisión 5.

**Forma canónica del payload:** UTF-8 con normalización Unicode, claves ordenadas de forma total y estable, sin espacios insignificantes, distinción explícita entre campo ausente y campo nulo, arrays sin orden semántico ordenados por su clave de identidad, y **prohibición de números en coma flotante** en cualquier payload de evento. Esta última no es purismo: la representación textual de un flotante varía entre runtimes, y bastaría para que la verificación fallara **en una máquina y no en otra** sobre un log íntegro — un falso positivo de manipulación en un expediente jurídico es un fallo grave.

Se añade `chain_spec_version` a la fila `cases`, para no tener que **inferir** con qué preimagen se computó un log antiguo.

### 4. Honestidad obligatoria: tamper-evident, no tamper-proof

La cadena detecta edición de payload, edición de cabecera, borrado, reordenamiento, inserción y bifurcación. **No los impide.** Se declara por escrito, y debe declararse en toda superficie que hable de integridad:

- **Una usuaria hostil con control total de la máquina puede regenerar la cadena completa**: tiene los mismos bytes, el mismo algoritmo y ninguna clave que le falte. **Este escenario está FUERA DEL THREAT MODEL V0**, por decisión.
- El **truncamiento por la cola** deja una cadena internamente válida; sin testigo externo no es detectable. Se adopta una mitigación **parcial y declarada como tal**: `current_event_hash` en la fila `cases`, de modo que truncar exija editar dos lugares coherentemente. **No protege contra quien edite ambos**, y no se presenta como si lo hiciera.
- La cadena sella **el log, no las tablas materializadas**: editar directamente `facts` no la rompe. La divergencia solo se descubre reconstruyendo desde el log y comparando.
- **No hay firma.** Un `event_hash` correcto demuestra consistencia interna, **no** que quien escribió la fila fuera quien dice `principal_id`.

**Lo que deliberadamente no se construye** (kernel §8.3): sin firmas digitales, sin HSM, sin anclaje externo obligatorio, sin timestamping de tercero. Es proporción, no omisión: cada pieza exige gestión de claves o un tercero disponible, y ninguna resuelve el primer escenario en el despliegue real de V0.

### 5. Dos contadores: `event_seq` para todo evento, `case_revision` solo para mutación epistémica canónica — **APROBADA (enmienda AC-02)**

```text
event_seq       monotónico, contiguo, +1 en TODO evento del Case Event Log
case_revision   monotónico, +1 SOLO en eventos que mutan el estado epistémico canónico
```

Cada evento registra ambos; `case_revision` es nulo en los eventos que no mutan conocimiento. La consecuencia operativa central: **`ReviewProposal` avanza `event_seq` y no `case_revision`**, y `HumanAuthorization.expected_case_revision` pasa a ser la revisión **contra la que se generó y se revisó** la propuesta, no la resultante del propio acto de revisión.

Tres argumentos:

1. **Semántica del reloj.** `case_revision` mide qué sabe el expediente. Una decisión de revisión aún no commiteada no añade hechos, evidencia ni links: el expediente sabe exactamente lo mismo antes y después. Avanzar el reloj sin cambio de conocimiento lo vacía de significado — y con él vacía `expected_revision`, que es el mecanismo entero de concurrencia optimista.
2. **Conflictos espurios evitables.** Bajo el modelo anterior (Modelo A), revisar la propuesta P-1 invalidaba análisis en vuelo que no tenían ninguna relación con P-1.
3. **Circularidad.** Bajo el modelo anterior, `expected_case_revision` era la revisión que el propio acto de revisión causó — definición circular que ya obligó a una corrección (addendum v0.3 B.2). Con dos contadores desaparece: se genera contra N, se revisa contra N, y el commit exige que el caso siga en N.

**Lo que se preserva del modelo anterior, íntegro:** la decisión de revisión **sigue siendo un hecho auditable y durable en el log append-only**, con principal humano identificado, `event_seq` propio, hash encadenado y payload completo. Lo único que deja de ocurrir es que el contador de conocimiento se mueva.

**Reformulación que esta decisión exige sobre ADR-004 inv. 5:** la biyección mutación↔evento se expresa sobre `event_seq`, con `case_revision` como **subsecuencia** — la de las mutaciones que además cambian el estado epistémico canónico. La frase "`seq == CaseRevision` resultante" deja de ser identidad y pasa a ser inclusión.

**Consecuencia obligatoria:** el cursor del delta es `event_seq`, no `case_revision`. De otro modo **las decisiones de la profesional serían invisibles en `changes_since`**, que es el peor resultado posible para un producto cuyo eje es la autoridad humana.

**Honestidad sobre el alcance:** esta decisión **no elimina todos los conflictos espurios**. `case_revision` sigue siendo un contador por Case, y cualquier incorporación no relacionada los produce (riesgo ya declarado en ADR-004). Elimina **una clase concreta y evitable**: la que causa el propio acto de revisión.

**Esta decisión enmienda ADRs Accepted y ESTÁ EN VIGOR:** los dueños la aprobaron como **enmienda AC-02**, de modo que ADR-004 (c), (b)1 e inv. 5 y ADR-005 §1, §4, inv. 9–10 quedan enmendados (supersede §16.16 y §16.19) y el kernel §5.2, §7, §8.1 y §9 ya la recogen. Su vigencia **no depende** del estado `Proposed` de este ADR. La Pregunta pendiente 1 queda **resuelta afirmativamente**; la 2 (alcance del criterio) **sigue abierta**.

### 6. Lista cerrada de eventos: se conserva, con tres precisiones

La lista cerrada de ADR-004 (b)1 se mantiene; abrirla sigue siendo cambio de contrato. Tres precisiones:

- **`ProposalReviewed` es UN tipo, no tres.** Con revisión por item, `approved / rejected / partial` se **derivan** de `decisions_summary` (`approved ⟺ rejected = 0 ∧ pending = 0`, etc.). Tres tipos donde uno basta, en una lista cuya apertura es cambio de contrato, y la mezcla real (dos aprobados, uno rechazado, cuatro pendientes) no cabe en tres etiquetas. Es la misma doctrina —no almacenar lo computable— que elimina `INVALIDATED` (ADR-008) y los estados derivados del `Fact` (ADR-003). **Cierra la cuestión abierta D.1 del addendum v0.3.**
- **`FactWithdrawn` permanece sin productor y su payload NO se contrata en v0.** Contratar la forma de un evento cuyo use case no existe sería inventar un contrato que nada valida. El tipo se conserva por la razón que ya dio ADR-004: quitarlo obligaría a reabrir el contrato al implementar el retiro de hechos.
- **`ProposalPreservedForReconciliation` permanece en la lista y queda SIN PRODUCTOR en v0 — enmienda AC-04 aprobada** (ADR-004 supersede §16.15), por el mismo patrón que `FactWithdrawn`. **La preservación de una propuesta ante conflicto de revisión es la conducta por defecto y su estado es derivado, no almacenado**: no hay marcador que persistir y, por tanto, ninguna mutación que registrar. Emitir un evento por un commit *rechazado* pondría en el log canónico un acto que no mutó nada, contra ADR-005 inv. 6 ("cero mutaciones") y contra la biyección de ADR-004 inv. 5. Su payload **sí** está contratado en `09-events-and-audit.md` §3.2, a diferencia del de `FactWithdrawn`, porque su use case existe y solo se discutía si escribe. Esto **cierra la Pregunta pendiente 3**.

### 7. Suficiencia para reconstrucción, con no duplicación intra-log

El payload contiene **por valor** el contenido que ese evento inmoviliza por primera vez, y **por referencia verificable `(id, content_hash)`** los bytes y el contenido ya fijado por un evento anterior de la misma cadena. Nunca bytes; nunca chat crudo (ADR-004 inv. 3); nunca rutas, nombres de tabla ni ids internos no emitidos a la superficie.

Efecto secundario deseable de la referencia por hash: si el contenido referenciado hubiera sido alterado, el `content_hash` del evento posterior deja de casar, y **el evento posterior denuncia la alteración del anterior** aunque la cadena se hubiera regenerado sobre él.

### 8. NO full event sourcing — se confirma, y se acota qué significa "reconstruible"

Se confirma ADR-004 (b)3. El estado vigente se **materializa en tablas**; ninguna operación cotidiana depende de replay; no hay snapshots, ni versionado de esquemas de evento como contrato de lectura, ni proyecciones incrementales.

Se acota la afirmación para que no se lea como más de lo que es: **"el expediente se puede reconstruir desde el log" describe una propiedad del contenido del log, no una capacidad implementada y ejercitada.** Convertirla en capacidad exige escribir el reconstructor. Se propone que exista en V0 **solo como test** —reconstruir el caso sintético y comparar con el estado materializado—, porque es además la única defensa disponible hoy contra la alteración del estado materializado sin tocar el log.

### 9. `occurred_at` no ordena nada

El orden del log lo fija **`event_seq`, jamás el timestamp**. Ninguna consulta, proyección, verificación o delta se ordena por reloj de pared, que en una máquina personal retrocede (NTP, zona horaria, suspensión, ajuste manual).

### 10. Retención del log operacional: forma de la política y reglas duras de la poda

Se propone la **forma**, no los números: dos horizontes sobre un **eje único de antigüedad** — el corto para `QUERY` con resultado aceptado (volumen alto, valor diagnóstico que decae), el largo para `COMMAND`, `PROPOSAL`, `SENSITIVE_COMMAND` y **cualquier** rechazo o error (son las entradas que sostienen el diagnóstico y la verificación adversarial). **Los valores concretos son DECISIÓN PENDIENTE**: cualquier cifra escrita hoy sería inventada, porque no hay uso real medido.

Cinco reglas duras, y las tres primeras son las que impiden que "retención" se convierta en "borrado selectivo de trazas incómodas":

1. **La poda es por antigüedad, nunca por contenido.** Prohibido podar por caso, tool, principal o resultado.
2. **La poda deja marca de agua durable** (`pruned_through_at`, `pruned_at`, `rows_removed`, `policy_version`), de modo que **"no hay traza" y "la traza fue podada" sean distinguibles**.
3. **La poda es del plano runtime/CLI**, jamás de la superficie del modelo: la clase `ADMIN` está vacía por diseño y no existe tool que pode nada.
4. Nunca dentro de una transacción de negocio, y nunca puede abortar una.
5. **No toca `case.db`** ni un byte.

### 11. Se propone **PF-006** para el Product Floor

**PF-006 — El Case Event Log no es desactivable, editable ni podable por configuración.**
Riesgo que previene: que una organización silencie o recorte el registro que hace verificable todo lo demás.
Enforced in: Infrastructure (append-only + trigger `RAISE(ABORT)` incondicional) + Application (el evento se escribe en la misma transacción que la mutación) + Configuration (no existe clave que lo desactive).
Configuration may relax? **NO.**
How tested: configuración que intenta desactivar o filtrar la auditoría ⇒ rechazo en carga; `UPDATE`/`DELETE` sobre `case_events` ⇒ abort; poda del log operacional ⇒ cadena intacta.

Fundamento: el kernel §12 entrega cinco políticas y señala esta como "sexta candidata natural"; el anexo de `principles.md` la lista como si ya fuera una de las cinco. Por precedencia gana el kernel, **y el resultado es que hoy ninguna política del piso protege el objeto que este ADR diseña.** Debe decidirse explícitamente, no por precedencia silenciosa.

## Invariantes derivados

1. **Todo evento del Case Event Log es simultáneamente registro de dominio y registro de auditoría**: no existe un segundo stream de auditoría, y ningún dato de auditoría vive fuera de la fila del evento.
2. **`case_events` es append-only**: no existe camino soportado de `UPDATE` ni de `DELETE`; el único trigger admitido es `RAISE(ABORT)` incondicional, que no lee valores de dominio ni ramifica.
3. **La cadena no se bifurca**: dos eventos no pueden declarar el mismo `prev_event_hash`, y solo el evento con `event_seq = 1` tiene `prev_event_hash` nulo.
4. **`event_seq` es monotónico estricto y contiguo desde 1**; `case_revision`, donde no es nulo, es monotónico no decreciente y **nunca retrocede**.
5. **`provenance_kind = HUMAN_DECISION` exige `principal_type = HUMAN`** en el evento; ningún `principal_type = AI` produce un evento `HUMAN_DECISION`. `Principal` (quién ejecutó) y `provenance_kind` (naturaleza epistémica del origen) son dimensiones distintas y ambas se registran.
6. **El evento del commit porta el `Principal` humano de la revisión, no el del invocador**: el operador queda en el Tool Invocation Log; el autor del acto epistémico, en el Case Event Log.
7. **El orden del log lo determina `event_seq`, nunca `occurred_at`**.
8. **El chat crudo, el razonamiento intermedio del modelo, los bytes, las rutas y los nombres internos no son representables** en el payload: el esquema no los admite.
9. **El Tool Invocation Log jamás es fuente para reconstruir estado canónico**; si un dato solo existe allí, ese dato no es del expediente.
10. **La poda del log operacional deja el estado canónico idéntico y la verificación de cadena en OK**, y siempre deja marca de agua.
11. **Ninguna migración cambia los bytes canónicos sobre los que se computó `event_hash`**; re-anclar la cadena es cambio de contrato de auditoría con `chain_spec_version` nuevo, jamás efecto colateral de un cambio de schema.
12. **Las migraciones no emiten eventos del Case Event Log ni avanzan `case_revision`**.
13. **El Case Event Log no es superficie del modelo**: ninguna proyección ni respuesta de tool expone `authorization_id` ni ningún campo de autorización, aunque el payload del evento los registre.
14. **La verificación de cadena es una función pura** sobre las filas ordenadas por `event_seq`: se prueba sin levantar una base de datos.
15. **Un fallo de escritura del log operacional nunca aborta ni revierte una transacción canónica**; un fallo de escritura del evento canónico **siempre** revierte la mutación.

## Consecuencias positivas

- **Auditoría sin doble contabilidad**: un solo registro canónico responde qué pasó, quién lo hizo, con qué metodología y con qué origen epistémico; la correlación con el log operacional añade el cómo se invocó, sin poder contradecirlo.
- **La cadena pasa de intención a especificación.** Con la preimagen cerrada y la forma canónica fijada, "hash-chained" deja de ser una etiqueta y se convierte en algo que un test puede fallar.
- **La honestidad queda escrita donde se lee.** "Tamper-evident, no tamper-proof" y el usuario hostil local fuera de alcance dejan de ser una nota al pie: son parte de la decisión, y ninguna superficie del producto puede prometer lo contrario sin contradecir un ADR.
- **El reloj del caso recupera su significado.** Con dos contadores, `case_revision` vuelve a responder "¿cambió lo que el expediente sabe?", que es la única pregunta que justifica que un commit se rechace por conflicto.
- **Desaparece la circularidad de `expected_case_revision`** y, con ella, la corrección que el addendum v0.3 B.2 tuvo que introducir para taparla.
- **Las decisiones de la profesional siguen visibles en el delta**, porque el cursor pasa a ser `event_seq`: separar los contadores no las esconde, las ordena.
- **La retención deja de ser un agujero.** Con eje de antigüedad, marca de agua y prohibición de poda selectiva, el log operacional no puede convertirse en un mecanismo de borrado dirigido.
- **La lista cerrada se mantiene cerrada.** Ninguna de las tensiones abiertas (procedencia adicional, preservación por conflicto) se resuelve inventando un tipo nuevo.

## Consecuencias negativas

- **Dos contadores son dos cosas que explicar**, dos que pueden desincronizarse en el código y dos que un lector puede confundir. La simplicidad de `seq == revision` se pierde, y a cambio se gana una distinción que solo importa en un punto del flujo.
- **Enmendar ADRs Accepted tiene coste documental real**: ADR-004 (b)1, (c) e inv. 5; ADR-005 §1, §4, inv. 9 y 10; addendum v0.3 B.2 puntos 1, 2 y 4; ejemplos numéricos del glosario; pasos 10–11 del vertical slice y sus tests. Y **exige recalcular por segunda vez** unos ejemplos que B.2 ya había recalculado una vez.
- **El payload es contrato**: cambiar su forma cambia los hashes futuros, y tocar los pasados rompe la cadena. Lo que en otro sistema sería un refactor interno, aquí es una decisión registrada.
- **Redundancia de almacenamiento** entre payload y estado materializado, acotada por la regla de no duplicación pero real, y sin ningún beneficio de runtime: el log se escribe siempre y se lee casi nunca.
- **El diagnóstico postmortem trabaja con hashes**, no con inputs: no se puede ver *qué* se pidió, solo que se pidió lo mismo dos veces. Es el precio de no convertir un log podable en depósito paralelo de material sin custodia.
- **La separación de contadores no elimina los conflictos espurios**, solo una clase de ellos. Quien espere que resuelva la fatiga de `REVISION_CHANGED` quedará insatisfecho, y el camino declarado —revisiones por agregado— sigue sin diseñarse.
- **Se pide una sexta política del Product Floor** cuando los dueños pidieron exactamente cinco.

## Alternativas consideradas

1. **Dos logs separados: eventos de dominio + log forense de auditoría — RECHAZADA** (ya rechazada en ADR-004 alt. 3; se confirma). Duplican el mismo contenido y crean la pregunta irresoluble de cuál manda cuando divergen. En un expediente jurídico, dos registros que se contradicen son peor que uno solo.
2. **Un único log para todo, incluidas las invocaciones MCP — RECHAZADA.** Haría imposible registrar invocaciones con `case_id` inexistente e ids fabricados —precisamente las que los tests adversariales exigen— y convertiría el historial del caso en el historial del chat, contra ADR-004 inv. 3. Además, la poda operaría sobre el archivo que contiene la cadena.
3. **Full event sourcing con estado derivado por replay — RECHAZADA** (ADR-004 alt. 2; se confirma). Complejidad sin disparador: snapshots, versionado del esquema de eventos como contrato de lectura y replay como dependencia de runtime, para una carga de eventos por minuto. La puerta queda abierta porque los payloads ya son suficientes.
4. **Mantener un solo contador (`seq == revision`, Modelo A) — RECHAZADA, y la aprobación de AC-02 la deja superada.** Era lo Accepted, es más simple de explicar y tenía coste documental cero. Se rechazó porque avanzar el reloj del conocimiento en un acto que no añade conocimiento vacía de significado al mecanismo que protege los commits, produce conflictos espurios evitables y obliga a definir `expected_case_revision` de forma circular. **Era la alternativa que los dueños podían elegir sin que ninguna otra decisión de este ADR cambiara; eligieron la contraria** (Preguntas pendientes 1, hoy resuelta).
5. **Separar los contadores pero mantener que `ProposalReviewed` avanza `case_revision` (opción C) — RECHAZADA.** Paga todo el coste conceptual de dos contadores y no usa la distinción justamente donde nació.
6. **Hash solo sobre el payload — RECHAZADA.** Dejaría fuera `principal_*` y `provenance_kind`: **quién hizo qué sería reescribible sin romper la cadena**, y el evento dejaría de funcionar como registro de auditoría.
7. **Firmar cada evento con una clave del producto — RECHAZADA para v0.** La clave viviría en la misma máquina que el atacante del escenario 1; añade gestión de claves y no cierra el escenario que pretende cerrar. Se prefiere declarar el límite a simular una garantía.
8. **Anclar el hash-cabeza en un servicio externo — NO RECHAZADA, APLAZADA.** Es la mitigación de mejor relación coste/beneficio contra la regeneración completa y el truncamiento, y exige decidir un destino aceptable para el hash de un expediente. Sigue siendo DECISIÓN PENDIENTE heredada de ADR-004.
9. **Almacenar los inputs literales en el Tool Invocation Log — RECHAZADA.** Mejoraría el diagnóstico y convertiría un archivo podable en un depósito paralelo de material sin custodia, incluido material que el Core rechazó incorporar (contra ADR-006), y con datos del cliente en un archivo sujeto a poda.
10. **Registrar la procedencia adicional de una reingestión solo en el log operacional — RECHAZADA.** Viola ADR-004 inv. 8 y, peor, la poda destruiría la custodia de una procedencia declarada. Es exactamente el caso que la regla "el log operacional nunca es fuente de estado canónico" existe para impedir.
11. **Un tipo de evento nuevo para "procedencia adicional" o para "derivación solicitada" — RECHAZADA.** Abrir la lista cerrada es cambio de contrato (ADR-004 inv. 6); ambas necesidades se cubren dentro del payload de un evento existente.

## Riesgos

- **RIESGO — Regeneración completa de la cadena por un local hostil.** Fuera del threat model V0, por decisión. No hay mitigación dentro del alcance actual; el anclaje externo del hash-cabeza es la única candidata y está sin decidir.
- **RIESGO — Estado materializado alterado sin tocar el log.** La cadena sella el log, no las tablas. Hoy **no hay detección**, salvo que se apruebe el reconstructor como test. Es el punto ciego más concreto de esta estrategia.
- **RIESGO — Truncamiento por la cola.** Sin testigo externo, una cadena truncada verifica correctamente. `current_event_hash` en `cases` es mitigación parcial y se declara como tal.
- **RIESGO — Forma canónica mal especificada.** Si la serialización no es determinista entre runtimes, la verificación produciría **falsos positivos de manipulación** sobre logs íntegros. Es la razón de prohibir la coma flotante y de dejar la especificación como POR VERIFICAR en lugar de darla por resuelta.
- **RIESGO — Reloj de pared.** No afecta al orden del log (que va por `event_seq`), pero sí a `expires_at` de la `HumanAuthorization`: un reloj atrasado podría hacer aparecer como viva una autorización expirada. El log es donde la anomalía sería visible, no donde se corrige.
- **RIESGO — Aritméticas divergentes residuales en el corpus técnico.** La causa —una decisión aplazada— desapareció con AC-02, pero el riesgo persiste **hasta que termine la normalización cruzada**: los documentos escritos bajo el Modelo A deben quedar con los valores del Modelo B. `09-events-and-audit.md` ya lo está. **POR VERIFICAR:** el estado de `01`, `03`, `06` y `vertical-slice-v0.md`.
- **RIESGO MATERIALIZADO — la separación de contadores se aprobó a medias.** AC-02 sacó `ProposalReviewed` del contador pero **no resolvió** si `FactsProposed`, `ArtifactRegistered` y `ArtifactMarkedStale` deben salir también (Pregunta pendiente 2). Consecuencia hoy en vigor: proponer una segunda propuesta sigue invalidando la autorización obtenida para la primera — **el conflicto espurio reaparece por otra puerta y solo se ha entregado la mitad del beneficio**. No es una hipótesis: es el estado actual mientras la pendiente 2 no se decida.
- **RIESGO — Crecimiento del log operacional sin política aprobada.** Mientras los horizontes no se decidan, el archivo crece sin criterio y la poda acabará improvisándose bajo presión, que es cuando peor se decide.
- **RIESGO — El payload como superficie de fuga.** Registra `note` de la profesional, `declared_origin` y contenido de propuestas. Vive en el private state y no se expone al modelo, pero cualquier proyección futura del log debe filtrar explícitamente, no confiar en que nadie mire.
- **RIESGO heredado — perímetro del anfitrión.** Con los hallazgos verificados del spike de Cowork, la protección del log **no** puede apoyarse en reglas del host. Si además B-04 resultara desfavorable (el MCP local confinado igual que el host), el Core no alcanzaría su propio estado canónico sin que el host también lo alcanzara, y la defensa en profundidad delante de la cadena se reduciría aún más. No cambia esta decisión; cambia cuánto pesa.

## Validación / pruebas necesarias

| # | Escenario | Resultado exigido | Invariante |
|---|---|---|---|
| 1 | **Verificación de cadena** — mutar el payload de un evento intermedio | La verificación falla señalando la clase de ruptura y el `event_seq` exacto | 3, 14 |
| 2 | Truncar el log por la cola | Detectado por desajuste con `cases.current_event_hash`; **se documenta que sin ese testigo no sería detectable** | 3 |
| 3 | Reordenar dos eventos / insertar uno en medio / bifurcar la cadena | Ruptura de enlace, colisión de `event_seq` o violación de `UNIQUE(prev_event_hash)` | 3, 4 |
| 4 | Editar `principal_id` o `provenance_kind` de un evento sin tocar el payload | La verificación falla: la cabecera entra en la preimagen | 5, 14 |
| 5 | **Determinismo de la forma canónica** — serializar el mismo payload dos veces, con claves en distinto orden de inserción | Bytes idénticos y `payload_hash` idéntico. Property test | 14 |
| 6 | Intentar construir un payload con un número en coma flotante | Rechazo en construcción | 14 |
| 7 | `UPDATE` o `DELETE` sobre `case_events` | Abort incondicional; el repositorio no expone la operación | 2 |
| 8 | **Property test de la biyección** — para toda secuencia de commands aceptados: toda mutación registrada tiene exactamente un evento y viceversa; `event_seq` contiguos; `case_revision` monotónica no decreciente | Se verifica **la biyección, no el conteo de invocaciones**: una invocación con *n* mutaciones deja *n* eventos | 4, 15 |
| 9 | `commit_reviewed_facts` exitoso | El evento `FactsCommitted` porta el `Principal` **de la profesional que revisó**, no el del invocador; el invocador aparece en el Tool Invocation Log | 6 |
| 10 | Intento de escribir un evento con `provenance_kind = HUMAN_DECISION` y `principal_type = AI` | Rechazo en el constructor del evento; `CHECK` redundante en el esquema | 5 |
| 11 | **F18** — invocación con `case_id` inexistente, id fabricado, path traversal | Cero eventos canónicos; **entrada presente** en el Tool Invocation Log con el id inventado en `case_ref` | 9 |
| 12 | **Poda del log operacional** | Estado canónico byte a byte idéntico; verificación de cadena OK; marca de agua presente con `pruned_through_at` | 10 |
| 13 | Intento de poda selectiva (por caso, tool, principal o resultado) | La operación no existe en el plano administrativo | 10 |
| 14 | Rechazo del commit (autorización inválida, expirada o consumida) | **Cero eventos**; solo traza operacional | 15 |
| 15 | Fallo simulado de escritura del log operacional durante una mutación exitosa | La transacción canónica **no** se revierte; el evento existe sin su invocación registrada | 15 |
| 16 | Fallo simulado de escritura del evento canónico | La mutación **se revierte entera**: no hay mutación sin evento | 15 |
| 17 | **Reconstrucción** — reconstruir el caso sintético desde el log y comparar con el estado materializado | Igualdad. *(Sujeto a la Pregunta pendiente 6: si el reconstructor entra en V0)* | 14 |
| 18 | Migración completa de un `case.db` | Cadena verificable antes y después con **los mismos `event_hash`**; ningún evento emitido por la migración | 11, 12 |
| 19 | Proyección `changes_since` sobre un tramo que incluye `ProposalReviewed` | El acto de revisión **aparece** en el delta, y **ningún campo de autorización** se expone | 7, 13 |
| 20 | Serie con `case_revision` nulo, rellenada a posteriori | La verificación falla: `case_revision` entra en la preimagen aunque sea nulo | 4, 14 |

**POR VERIFICAR:** la numeración definitiva del catálogo `F-xx` / `AT-xxx` y su correspondencia con la matriz de `vertical-slice-v0.md`.

## Preguntas pendientes

1. **RESUELTA — la Decisión 5 (dos contadores) fue APROBADA como enmienda AC-02.** Enmienda ADR-004 (b)1, (c) e inv. 5, y ADR-005 §1, §4, inv. 9–10 (supersede §16.16 y §16.19). **El Modelo B es el vigente en todo el corpus**; el Modelo A queda superado. La tabla del kernel §7, que ya la aplicaba, es hoy correcta. Lo que resta no es decisión sino **normalización cruzada** de los documentos escritos bajo el modelo anterior.
2. **DECISIÓN PENDIENTE — Alcance del criterio de la Decisión 5. Sigue abierta tras AC-02.** ¿`FactsProposed`, `ArtifactRegistered` y `ArtifactMarkedStale` mutan el "estado epistémico canónico"? Por el criterio literal, una propuesta no añade hechos, evidencia ni links — el mismo argumento que sacó a `ProposalReviewed` del contador; pero la tabla del kernel §7 dice que `ProposeFacts` sí avanza, y AC-02 no la tocó. Se advirtió que convenía decidirla junto con la 1; **no se hizo, y el resultado es el riesgo materializado que se registra más arriba**.
3. **RESUELTA — `ProposalPreservedForReconciliation`, por la enmienda AC-04** (ADR-004 supersede §16.15). Permanece en la lista cerrada y **queda sin productor en v0**, patrón `FactWithdrawn`; la preservación es **conducta por defecto y estado derivado, no almacenado**, de modo que no se persiste marcador alguno. Quedan descartadas las otras dos opciones que se registraron: persistir un marcador mínimo (almacenaría lo computable) y admitir un evento sin mutación materializada (pondría en el log canónico un acto que no mutó nada).
4. **DECISIÓN PENDIENTE — Procedencia adicional en la reingestión.** Mismos bytes con procedencia declarada distinta: ¿evento `EvidenceIncorporated` con marca de reingestión, o ninguna persistencia canónica? El log operacional queda descartado (alternativa 10).
5. **DECISIÓN PENDIENTE — Valores de los dos horizontes de retención** del Tool Invocation Log. Cualquier cifra hoy sería inventada.
6. **DECISIÓN PENDIENTE — ¿El reconstructor entra en V0 como test, o es POST-V0?** De ello depende que exista alguna detección del estado materializado alterado sin tocar el log.
7. **DECISIÓN PENDIENTE — Anclaje periódico del hash-cabeza fuera del workspace** (heredada de ADR-004): destino aceptable, frecuencia y qué se ancla exactamente.
8. **DECISIÓN PENDIENTE — ¿Entra PF-006 como sexta política del Product Floor?** Hoy ninguna de las cinco cubre la inmutabilidad de la auditoría, y `principles.md` y el kernel §12 no coinciden en si debe estar.
9. **DECISIÓN PENDIENTE — Guarda de monotonía del reloj**: ¿el Core rechaza, marca o ignora un evento cuyo `occurred_at` es anterior al del evento previo más allá de una tolerancia?
10. **DECISIÓN PENDIENTE menor — ¿`event_ref` del log operacional pasa a ser una lista** cuando una invocación produce varios eventos? Nada del contrato depende de ello.
11. **DECISIÓN PENDIENTE — ¿Lleva el canal humano su propio log operacional?** Hoy su acto queda íntegro en el log canónico; falta la traza del transporte, que sigue siendo un spike abierto de ADR-005.
12. **RATIFICACIÓN — `ProposalReviewed` como un solo tipo** con las variantes derivadas: es cambio de letra sobre una lista cerrada Accepted.
13. **POR VERIFICAR — Especificación de canonicalización** adoptada y garantías del runtime sobre orden de claves y representación numérica (spike de dependencias).
14. **POR VERIFICAR — Suficiencia del `input_hash`** para el diagnóstico real de rechazos.
15. **POST-V0** — firma criptográfica de eventos; log de auditoría multi-máquina y sincronización; reconstructor como camino de operación; revisiones por agregado frente a los conflictos espurios; payload de `FactWithdrawn` y de `RecordProfessionalDetermination`.

## Relaciones con otros ADRs

- **ADR-004 (Canonical Case State + Derived Projections) — este ADR lo REFINA y, en un punto, lo ENMIENDA (AC-02, aprobada).** Confirma sin tocar: las dos persistencias, la unificación de evento y auditoría, el rechazo de full event sourcing, la lista cerrada de eventos, el chat como canal y nunca registro, y la concurrencia optimista con preservación. **Cierra dos de sus preguntas pendientes** —política de retención (en forma; los valores siguen abiertos) y, si se aprueba PF-006, la inmutabilidad de la auditoría—, **deja abierta** la del anclaje del hash-cabeza, y **enmienda** (c) e inv. 5 (`seq == revision` deja de ser identidad; biyección sobre `event_seq` con `case_revision` como subsecuencia) y (b)1 (momento de emisión: se conserva el momento, decae "y avanza la CaseRevision") — **supersede §16.16**. Además precisa (b)1 en la letra: `ProposalReviewed` es un tipo, no tres; y recoge la **enmienda AC-04** (supersede §16.15) sobre `ProposalPreservedForReconciliation`. **El texto de ADR-004 conserva su precedencia de nivel 1 en todo lo no enmendado.**
- **ADR-005 (autoridad humana) — enmienda su aritmética, no su naturaleza.** Con la Decisión 5 aprobada (AC-02, supersede §16.19), `expected_case_revision` **es** la revisión contra la que se generó y revisó la propuesta; **la semántica aprobada, "la revisión que la profesional tenía a la vista al aprobar", se conserva literalmente** y lo que decae es la definición circular. Su **enmienda AC-01** (autorización por item, `item_content_hash`, sin `authorized_items[]`, `authorized_operation = COMMIT_FACT`) es la que este ADR asume al describir el payload de `ProposalReviewed`. Nada de lo nuclear de ADR-005 se toca: two-phase, registro server-side, cero secretos en el contexto del modelo, un solo uso, expiración y transporte desacoplado. Nota de vocabulario: donde ADR-005 inv. 1 pone el valor epistémico dentro del campo de actor, la normalización aprobada del kernel §1.5 lo expresa como **dos** afirmaciones —`provenance_kind = HUMAN_DECISION` y `principal_type = HUMAN`—; el texto histórico no se corrige y **no se reproduce**.
- **ADR-008 (Proposal y autorización por item) — reciprocidad, y es neutral respecto de la Decisión 5.** ADR-008 fija qué decide una persona y con qué granularidad; este ADR fija **cómo queda registrado** ese acto: un solo evento `ProposalReviewed` por sesión de revisión, con las decisiones por item, la `review_session_id` y `authorization_source` (incluida la marca indeleble `DEV_STUB`) dentro de un payload sellado por hash. Su invariante 7 —commit rechazado ⇒ cero mutaciones y cero eventos— es exactamente lo que la tabla de validación de este ADR ejercita. **Responde su pregunta pendiente 1** (aritmética de revisiones: el Modelo B, por AC-02) y **cierra su pregunta 2** (`ProposalPreservedForReconciliation` queda sin productor en v0, por AC-04).
- **ADR-001 (frontera de confianza):** este ADR instrumenta su invariante 2 —toda mutación pasa por un use case y produce exactamente un evento con actor— con la definición de mutación del addendum v0.3 B.3, y su invariante 3 —clase `ADMIN` vacía— es lo que impide que exista una tool capaz de podar o editar cualquiera de los dos logs. El desdoblamiento del commit (Decisión 1 / invariante 6) es consecuencia directa de que el invocador MCP sea un cliente **no confiable** cuya identidad no puede atribuirse a un acto epistémico.
- **ADR-002 (Protected Local Case Store):** ambos logs viven en el private state, alcanzables solo por el camino único host → Legal MCP → Application → Case Store. Este ADR asume y refuerza su límite declarado —tamper-evident, no tamper-proof frente a un actor con control total del equipo— y añade, con los hechos verificados del spike de Cowork, que **la protección del log es posicional y no puede apoyarse en reglas del anfitrión**.
- **ADR-003 (modelo de dominio epistémico):** su doctrina "no almacenar lo que se puede computar" —origen de los estados derivados del `Fact`— es la misma que aquí deriva las variantes de `ProposalReviewed` en lugar de materializarlas como tipos. Sus transiciones almacenadas del `Fact` son eventos de este log (`FactsCommitted`; `FactWithdrawn` sin productor), y la separación `Principal` / `provenance_kind` es la normalización aprobada de la tripla de actor que ADR-003 introdujo.
- **ADR-006 (frontera de incorporación):** reciprocidad. ADR-006 fija qué material puede entrar y por qué única puerta; este ADR fija cómo queda registrado ese ingreso, con `declared_origin` en el payload y el `content_hash` en lugar de los bytes. Su invariante 7 (idempotencia por hash) es el origen de la pregunta pendiente 4, y su prohibición de material sin custodia es lo que impide almacenar inputs literales en el log operacional.
- **ADR-007 (estrategia de persistencia v0, Proposed):** el `CaseStorePort` es el contrato; que la cadena se materialice en una tabla SQLite es detalle de plataforma sustituible. Lo que **no** es sustituible sin decisión es la preimagen del hash y la forma canónica del payload, que son contrato de auditoría y no de almacenamiento.
- **Documento técnico asociado:** `docs/technical-design/v0/09-events-and-audit.md` (schema completo del `CaseEvent`, payload conceptual de los once tipos de evento, preimagen y algoritmos de append y verificación, schema y política de retención del Tool Invocation Log, y el desarrollo íntegro de la enmienda AC-02 —modelo vigente y modelo superado, su traza comparada y su impacto sobre el addendum v0.3 B.2—).
