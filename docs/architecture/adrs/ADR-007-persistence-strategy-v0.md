# ADR-007 — Estrategia de persistencia V0: SQLite en modo WAL sobre filesystem content-addressed, una máquina, un escritor lógico

## Estado

Proposed

## Contexto

ADR-002 (Accepted) decidió **dónde** vive el estado canónico —un private state fuera de toda carpeta alcanzable por el host— y declaró expresamente que *la regla es la separación, no el path*. ADR-003 y ADR-004 (Accepted) decidieron **qué** es canónico: las entidades epistémicas, el Case Event Log append-only y hash-chained, la aritmética de `CaseRevision` y la concurrencia optimista. Ninguno de los tres decidió **con qué** se materializa nada de eso.

Ese hueco tiene consecuencias que no son de detalle. Sin una decisión registrada de motor y de topología: (a) no se puede escribir el nivel de pruebas de integración de persistencia, que por definición se escribe contra un motor concreto; (b) los ocho `POR VERIFICAR` de `04-persistence-model.md` §11 —claves foráneas por conexión, índices parciales, copia consistente, integridad, FTS5, `synchronous` bajo WAL, `rename` con destino existente en Windows, PK de texto— no tienen sujeto contra el que verificarse; y (c) la afirmación de `boundaries.md` §6 de que la persistencia es *detalle de implementación sustituible* queda sin demostración, porque nadie ha escrito qué haría falta para sustituirla.

Este ADR cierra ese hueco. **No** redefine qué es canónico (ADR-003), ni dónde vive la frontera de acceso (ADR-002), ni qué se registra (ADR-004), ni el esquema concreto — que es objeto de `docs/technical-design/v0/04-persistence-model.md` y que este ADR **no contradice en ningún punto**: lo resume en lo que es decisión de arquitectura y lo referencia en lo que es especificación.

**Restricciones de partida, todas ya decididas en otro sitio:**

| Restricción | Fuente | Consecuencia para esta decisión |
|---|---|---|
| Una máquina, una usuaria, un proceso, un escritor | `01-system-design.md` §11; kernel §15 | No hace falta un motor con concurrencia de escritura multi-proceso |
| Multi-máquina, sync, replicación y PostgreSQL están **fuera de V0** | kernel §15 | No hace falta un motor servidor |
| Concurrencia **optimista**, sin locking pesimista | ADR-004 (c) | El motor no necesita bloqueos de larga duración |
| El Case Event Log es **append-only y hash-chained**, por Case | ADR-004 | El motor debe permitir prohibir `UPDATE`/`DELETE` sobre una tabla |
| Ninguna decisión de V0 se justifica por rendimiento **medido** | `04` §11 (`SUPUESTOS`) | Toda comparación por velocidad queda fuera de este ADR |
| *Vendor-independence*: cambiar de motor no debe tocar ningún invariante ni contrato del Domain | `principles.md` (principio de sustitución) | La decisión debe venir con su prueba de reversibilidad |
| Los volúmenes de V0 son pequeños (una usuaria, caso sintético) | `04` §11 | El argumento de escala no aplica en ninguna dirección |

**HECHOS VERIFICADOS que gobiernan la decisión** (fuente: sqlite.org, vía kernel §1 y `docs/research/runtime-dependencies-spike-v0.md` §3.5):

1. En modo WAL, lectores y escritores concurren con **un solo escritor a la vez**.
2. **WAL no funciona sobre filesystems de red** (*"WAL does not work over a network filesystem"*), y hay corrupción documentada por locking defectuoso, especialmente en red.
3. El modo WAL es **persistente en el fichero**: activado una vez, el fichero vuelve a abrirse en WAL.
4. FTS5 está incluido en SQLite desde 3.9.0 pero **no siempre está compilado**: *"SQLite soporta FTS5"* es una afirmación sobre el **build**, no sobre el motor.
5. No hay stemming español de serie en FTS5.

## Decision

### 1. Motor y topología

**SQLite en modo WAL** como motor del estado canónico, con la topología de cuatro almacenes de propósitos disjuntos ya especificada en `04` §1:

| Almacén | Naturaleza | Regla que lo gobierna |
|---|---|---|
| `cases/<case_id>/case.db` | **Canónico** | Estado materializado + Case Event Log **de un solo Case** |
| `cases/<case_id>/blobs/` | Canónico (originales) / regenerable (derivados) | Content-addressed, **write-once** |
| `catalog.db` | **Derivado y reconstruible** | Resolución `identificador natural → case_id` para `open_case`. Si se desfasa, **se reconstruye; jamás se reconcilia** |
| `operational.db` | **No canónico y podable** | Tool Invocation Log, con política de retención |

**Una base de datos por Case.** El aislamiento entre expedientes deja de ser un predicado que cada consulta debe recordar (`WHERE case_id = ?`, cuyo olvido produce fuga silenciosa —la peor clase de fallo en este dominio—) y pasa a ser una **frontera física**: un identificador del Case B sencillamente no existe en el archivo del Case A.

### 2. Almacén de bytes: filesystem content-addressed y write-once

Los bytes de `Source` y de `DerivedRepresentation` **no viven en la base de datos**. Viven en el filesystem, direccionados por el SHA-256 de su contenido, con fan-out de dos pares hexadecimales, `staging/` fuera de `blobs/`, y **ninguna tabla que almacene una ruta**: la ubicación es una función pura de `(content_hash, clase, storage_layout_version)` (`04` §7.1–§7.2).

Tres consecuencias buscadas: no hay segunda fuente de verdad que se desincronice de la fila; **no hay ruta que inyectar** —ninguna entrada externa influye en dónde se lee o escribe—; y un cambio de layout es una migración de copia hacia adelante, nunca un `UPDATE` masivo de rutas.

### 3. Un escritor lógico, serializado en el Core

La escritura canónica se serializa **en el Core**, no en el motor. El motor aporta la garantía de un escritor a la vez (HECHO VERIFICADO 1); el Core aporta que ese escritor sea **uno solo y lógico**, de modo que la frontera transaccional coincida con la frontera del use case.

Sobre esa base, la concurrencia es **optimista** (ADR-004 (c)): la comparación `expected_case_revision` contra `cases.current_revision` ocurre **dentro** de la transacción de escritura. No hay locking pesimista, no hay transacciones de larga duración y no hay espera del usuario dentro de una transacción.

### 4. Orden obligatorio de escritura: bytes antes que fila

```text
1. escribir bytes en staging/<tmp>, calculando SHA-256 al vuelo
2. fsync del temporal
3. si la ruta definitiva ya existe -> descartar el tmp (idempotencia a nivel de bytes)
   si no -> rename atomico tmp -> ruta definitiva
4. BEGIN IMMEDIATE
5. INSERT de filas + INSERT del case_event + UPDATE de contadores del Case
6. COMMIT
```

**Regla dura:** un blob sin fila es **basura recuperable** —no lo referencia nadie, se detecta y se recoge—; una fila sin blob es **corrupción** —el expediente afirma custodiar bytes que no existen—. Ante duda, siempre el fallo barato.

### 5. Dos puertos, contrato asíncrono, ningún tipo del driver hacia dentro

El Domain y la Application hablan con **`CaseStorePort`** y **`SourceBlobPort`**. Ningún tipo del binding concreto aparece en firmas de `domain` ni de `application` (regla de dependencias, kernel §13).

**El contrato del puerto es asíncrono (`Promise`) aunque los dos candidatos verificados sean síncronos.** Es el punto contraintuitivo de esta decisión y por eso se justifica: definir el puerto síncrono congelaría el contrato de Application a una propiedad del driver, y cualquier backend futuro obligaría a reescribir todas las firmas del Core. **Envolver una llamada síncrona en una `Promise` resuelta es trivial; desenvolver lo contrario no lo es. La asimetría del coste decide.** Corolario: mover la persistencia a un worker thread, si alguna vez hiciera falta, es posible **sin tocar el puerto**.

El adapter aísla en **un único seam** las dos cosas que difieren entre bindings: apertura y configuración de la conexión (pragmas) y manejo de transacciones. Todo lo demás es SQL, que es común.

### 6. Despliegue local obligatorio

Consecuencia directa del HECHO VERIFICADO 2: **una carpeta sincronizada (OneDrive, Dropbox, Google Drive) o una unidad de red no es despliegue válido de este adapter.** El `case.db` vive siempre en almacenamiento local.

Dos reglas operativas derivadas: el Core **verifica** el `journal_mode` al abrir cada Case y no lo asume —un `case.db` restaurado de copia o creado por una versión anterior puede no estar en WAL—; y el Core detecta y **rechaza** abrir un Case cuya ruta esté en una ubicación de ese tipo. La elección entre *rechazar* y *advertir* se registra como pregunta pendiente, con recomendación de rechazar por coherencia con la política de integridad de la evidencia original.

### 7. Binding concreto

`PROPUESTA, requiere aprobación (registrada como decisión bloqueante en 16-open-implementation-decisions.md, OD-03).` Implementar V0 sobre **`better-sqlite3`** detrás del puerto de la decisión 5, y **reevaluar `node:sqlite` cuando alcance Stability 2 — Stable**.

Razón única y decisiva, con fuente: el propio proyecto Node documenta que las features Stability 1 no están sujetas a versionado semántico y que **su uso en producción no está recomendado**; `node:sqlite` está hoy en Stability 1.2. El coste que se acepta explícitamente y no se disimula: dependencia nativa, riesgo de instalación en máquinas Windows sin prebuild disponible, y recompilación al cambiar de línea de Node. **`sqlite3` (TryGhost) queda descartada**: su propio repositorio se declara sin mantenimiento, y una dependencia así no es admisible para el almacén canónico de un expediente jurídico.

### 8. La co-localización es restricción del ADAPTER, no regla del Domain

Que `case.db` y `blobs/` vivan bajo el mismo directorio `cases/<case_id>/` es una decisión de **este** ADR y de ninguno superior. **Es normativa para el adapter y no lo es para el Domain.**

**Por qué no es regla del Domain.** El Domain razona en `Source`, `Evidence`, `EvidenceLink`, `ProvenanceRecord`, `DerivedRepresentation` y `Fact`, y en la identidad de contenido (`content_hash`). **Ningún invariante del Domain menciona un archivo, un directorio ni una base de datos**, y ninguno podría hacerlo sin violar el principio de independencia de proveedor: un invariante epistémico que dependa de la coincidencia de dos rutas dejaría de ser comprobable en cuanto el almacenamiento cambiara de forma.

**Por qué sí es restricción del adapter.** La co-localización existe por tres razones de nivel de adapter, todas verificables:

| # | Razón | Qué se rompería sin ella |
|---|---|---|
| 1 | **Frontera de atomicidad.** La transacción canónica es sobre **un** `case.db`; los blobs se escriben antes y fuera de ella | Blob y fila con ciclos de vida o latencias distintas convierten el fallo barato (huérfano) en fallo caro (fila sin bytes alcanzables) |
| 2 | **Unidad de backup, migración y degradación.** El backup verificado, la restauración automática y la apertura en solo lectura operan sobre **un directorio de Case** | "Backup verificado" dejaría de tener un objeto único que verificar |
| 3 | **Confidencialidad sin refcount.** Sin deduplicación entre Cases, cada blob pertenece a exactamente un Case; archivar o exportar un expediente es operar sobre un directorio | La confidencialidad entre expedientes pasaría a depender de un contador de referencias correcto |

**Prueba de que es adapter y no dominio (test de sustitución, `principles.md`).** Un `SourceBlobPort` respaldado por otro almacén —objeto remoto, volumen cifrado, almacén de contenido separado— con la **misma** semántica de direccionamiento por contenido y de write-once **no cambia nada** en `domain` ni en `application`. Lo que cambia es el modelo de fallo y el significado de "backup verificado", que son propiedades del adapter.

**Corolario normativo, para que no se erosione:** **ninguna regla del Domain puede justificarse por la co-localización.** Todo documento que derive un invariante epistémico de *"están en la misma carpeta"* está mal, y la corrección es mover el argumento al adapter, no debilitar el invariante.

### 9. Qué haría falta para sustituir el motor

La afirmación *"la persistencia es sustituible"* solo vale si viene con la lista de lo que un sustituto debe entregar. Nueve requisitos, todos derivados de decisiones ya tomadas en otro ADR o documento — **ninguno es una preferencia de este ADR**:

| # | Requisito del sustituto | De dónde viene | Si no lo cumple |
|---|---|---|---|
| 1 | **Atomicidad** sobre la unidad *"mutación + su evento"* en una sola transacción | ADR-004 (biyección mutación↔evento) | La biyección pasa a depender de que nada falle a mitad |
| 2 | **Comparación-y-escritura condicional** de la revisión vigente **dentro** de la transacción | ADR-004 (c), concurrencia optimista | `REVISION_CHANGED` deja de ser fiable: dos escritores podrían pasar el mismo control |
| 3 | **Unicidad aplicable** por el motor: `UNIQUE(content_hash)` y unicidad parcial de la autorización viva | ADR-006 inv. 7 (idempotencia); ADR-005 (uso único) | La idempotencia y el consumo único quedan sin red bajo carrera |
| 4 | **Prohibición efectiva de `UPDATE`/`DELETE`** sobre las tablas append-only, o declaración explícita de que esa defensa pasa a ser solo del adapter | ADR-004 (log append-only) | Se pierde la única defensa que no depende del código de aplicación |
| 5 | **Ordenación estable por `event_seq`** y lectura íntegra de la cadena para verificar el hash-chain | ADR-004 | La auditoría deja de ser verificable |
| 6 | **Búsqueda de texto** con la semántica que `04` §6 fija, o un sustituto **declarado** | Superficie `search_case` | Cambia el **contrato**, no el adapter: `search_case` deja de significar lo mismo |
| 7 | **Copia consistente + comprobación de integridad** para el backup verificado previo a migración | `boundaries.md` §10; kernel §13 | "Backup verificado" vuelve a significar "archivo escrito" |
| 8 | **Blob store write-once, direccionado por contenido, con publicación atómica** | Decisiones 2 y 4 de este ADR; PF-002 | La inmutabilidad de la evidencia original deja de estar en la infraestructura |
| 9 | **Localidad**: un solo proceso en una sola máquina, sin servidor externo | ADR-002 (private state); kernel §15 | **No es sustitución de adapter: es cambio de arquitectura**, y exige reabrir ADR-002 y su threat model |

**El test de sustitución es ejecutable, no retórico:** implementar el sustituto y volver a correr N1–N6. Los niveles de Domain y Application deben pasar **sin un solo cambio** (no tocan persistencia); el nivel de integración de persistencia se reescribe por definición. **Si N1 o N2 necesitan cambios, la conclusión no es que el sustituto sea malo: es que una regla del Domain se había filtrado al adapter**, y eso es un defecto que hay que arreglar antes de sustituir nada.

## Invariantes derivados

Numerados y comprobables. Cada uno tiene un test asignado en `Validacion / pruebas necesarias`.

1. **Ningún tipo del binding de base de datos aparece en firmas de `domain` ni de `application`.** El puerto es el único punto de contacto.
2. **Toda mutación canónica y su evento ocurren en una única transacción sobre un solo `case.db`.**
3. **Ninguna transacción abarca dos archivos canónicos.** No hay commit en dos ficheros: `catalog.db` es derivado y se reconstruye; `operational.db` es podable y se escribe fuera de la transacción canónica, también en los rechazos.
4. **Ninguna fila almacena una ruta de filesystem.** La ruta es función pura de `(content_hash, clase, storage_layout_version)`.
5. **Write-once:** ninguna ruta de `blobs/` se abre en modo escritura si ya existe.
6. **Orden bytes→fila:** ninguna fila canónica referencia un `content_hash` cuyos bytes no estén ya publicados en su ruta definitiva.
7. **Un `case.db` fuera de almacenamiento local no es despliegue válido**, y el Core lo detecta al abrir.
8. **El `journal_mode` se verifica al abrir cada Case; nunca se asume.**
9. **Un `case.db` con `schema_version` distinto del esperado se abre en solo lectura**, y no se migra al vuelo ni se "arregla".
10. **Un fallo de integridad degrada a solo lectura y lo dice**; nunca se repara solo ni en silencio.
11. **Ninguna regla del Domain se justifica por la co-localización de `case.db` y `blobs/`.**
12. **`catalog.db` nunca es autoridad**: ante discrepancia con los `case.db`, gana el `case.db` y el catálogo se reconstruye.

## Consecuencias positivas

- **El aislamiento entre expedientes deja de depender de la disciplina de cada consulta.** Un identificador de otro Case no existe en el archivo: la referencia cruzada falla antes de que nadie razone, y el rechazo autoritativo lo sigue emitiendo el Core con código semántico estable, no el motor con un error de FK.
- **Backup, migración y degradación tienen una unidad natural.** Un expediente grande no obliga a copiar el corpus completo, y un fallo de migración compromete un archivo, no todos.
- **Cero infraestructura que administrar.** Sin servidor, sin puertos abiertos, sin credenciales de base de datos, sin superficie de red. Coherente con el private state de ADR-002: lo que no existe no se puede atacar por red.
- **El `event_seq` es un contador de archivo**, no una columna que filtrar; la cadena de hashes es por fichero y su verificación no depende de excluir filas de otros Cases.
- **Portabilidad y archivo (POST-V0) son copiar un directorio**, no extraer filas entrelazadas.
- **La decisión es reversible sin cambiar el modelo de datos.** El DDL de `04` §3 es idéntico bajo base única o base por Case: todas las tablas conservan `case_id` con su FK, y en el layout adoptado la tabla `cases` tiene exactamente una fila. Un adapter de base única usaría el mismo esquema con *N* filas.
- **La ausencia de rutas en el esquema cierra estructuralmente el path traversal.** No es una lista negra: sencillamente no hay entrada externa que influya en dónde se lee o escribe.

## Consecuencias negativas

Se enumeran sin atenuar; todas son costes aceptados, no efectos imprevistos.

- **`open_case` no puede consultar un índice único sin ayuda.** Se resuelve con `catalog.db`, que introduce un objeto derivado más que mantener y una tentación permanente de tratarlo como autoridad. Mitigado por el invariante 12, no eliminado.
- **Las migraciones se ejecutan *N* veces**, una por Case, y un fallo a mitad del recorrido deja el conjunto en estados mixtos. La respuesta es **fricción deliberada**: todo Case con `schema_version` inesperado se abre en solo lectura y se reporta. Nadie "arregla" nada al vuelo.
- **Las consultas cross-case no existen.** Es deliberado —no hay caso de uso en V0— pero significa que la primera necesidad real (por ejemplo, deduplicación de Sources) obliga a resolver en el catálogo derivado o a cambiar el adapter.
- **La ejecución del binding es síncrona: bloquea el hilo mientras dura.** `ANÁLISIS, no medición`: una operación de persistencia larga no se solapa con nada en el proceso del servidor MCP. **No se afirma nada sobre magnitud**, porque eso sería una afirmación de rendimiento sin fuente. La consecuencia de diseño se absorbe con el contrato asíncrono del puerto (decisión 5).
- **Un archivo por Case multiplica los descriptores y los ficheros auxiliares** (`-wal`, `-shm`) y hace que la configuración de pragmas sea una rutina de apertura de Case, no un arranque global.
- **El despliegue queda restringido a almacenamiento local**, lo que en el entorno objetivo —una profesional que probablemente guarda todo en una carpeta sincronizada— es una restricción real, visible y molesta.
- **Elegir un binding nativo introduce un riesgo de instalación** en la máquina de la usuaria, que es un riesgo de producto y no solo de ingeniería.

## Alternativas consideradas

| Alternativa | Por qué se rechaza |
|---|---|
| **Una sola base de datos para todos los Cases** | El aislamiento entre expedientes volvería a depender de que **cada** consulta lleve su filtro por Case; un olvido produce fuga silenciosa. El coste que evita —una consulta cómoda para `open_case`— se resuelve con un catálogo derivado. **No se descarta por siempre:** el DDL es el mismo bajo ambas particiones, luego la reversión es de adapter |
| **Base de datos servidor local (PostgreSQL, MySQL)** | Aporta concurrencia multi-proceso que V0 **no necesita** (un escritor, una máquina, una usuaria) a cambio de un servicio que instalar, arrancar, administrar y actualizar en la máquina de una profesional del derecho, más credenciales y una superficie de red donde hoy no hay ninguna. Contradice el espíritu del private state de ADR-002. Queda **POST-V0** por kernel §15 |
| **Bytes dentro de la base de datos (BLOB en tabla)** | Colapsa dos ciclos de vida distintos: los originales son inmutables y write-once, el estado materializado se reescribe. Además convierte cada backup del estado en un backup de todos los bytes, encarece la verificación de integridad y elimina la propiedad más útil del content-addressing —que la existencia del contenido sea comprobable con una llamada al filesystem, sin abrir la base |
| **Solo filesystem: JSON o ficheros planos, sin motor** | No hay atomicidad multi-fila, ni unicidad aplicable, ni ordenación estable, ni prohibición efectiva de `UPDATE`/`DELETE`. Los requisitos 1–5 de la decisión 9 quedarían **todos** en el código de aplicación, es decir, sin ninguna red bajo el fallo humano |
| **Event sourcing puro, sin estado materializado** | El log ya es canónico y append-only (ADR-004); lo que se rechaza es **eliminar la materialización**. Reconstruir cada proyección desde el origen en cada lectura convierte toda consulta en un replay y hace que un cambio en la lógica de proyección altere la lectura del pasado. Con materialización, la proyección es función determinista del estado canónico y el replay sigue disponible como verificación |
| **Base documental embebida (clave-valor, documentos)** | Ninguna aporta las cinco garantías de motor que la decisión 9 exige (atomicidad multi-tabla, unicidad aplicable, condicional en transacción, prohibición de mutación, orden estable) sin construirlas encima. Construirlas encima es escribir un motor |
| **`node:sqlite` como binding** | Mismo motor, distinto binding. Se rechaza **para V0** por la etiqueta de estabilidad de su propio proyecto, no por capacidad; y se declara la reevaluación cuando alcance Stability 2. Su ventaja —cero dependencias, sin toolchain— es real y está registrada |
| **`sqlite3` (TryGhost)** | Descartada: repositorio declarado **sin mantenimiento** por sus propios responsables |

## Riesgos

| Id | Riesgo | Gravedad | Estado y mitigación |
|---|---|---|---|
| R1 | **Carpeta sincronizada o unidad de red.** El entorno objetivo hace probable que la usuaria guarde todo en OneDrive o similar, y ahí la premisa de WAL se rompe | **Alta** | Detección y rechazo al abrir (decisión 6). **`POR VERIFICAR`:** cómo se detecta de forma fiable una carpeta sincronizada en Windows — **no hay API documentada universal**; `NOT_TESTED` en el spike |
| R2 | **Prebuild nativo ausente** para la combinación exacta de versión de Node, ABI, arquitectura y plataforma ⇒ la instalación intenta compilar y falla | Alta (producto) | `POR VERIFICAR` antes de ratificar la decisión 7: existencia de prebuild en `win32-x64` y, si aplica, `win32-arm64` |
| R3 | **Migración parcial del conjunto de Cases** | Media | Fricción deliberada: solo lectura para todo Case con `schema_version` inesperado (invariante 9) |
| R4 | **FTS5 no es una garantía documentada de API** en uno de los dos bindings; en el otro está en su documentación de compilación | Media | `POR VERIFICAR` contra el binario concreto. Si falla, cambia el adapter de búsqueda, no el contrato del Domain — salvo que se sustituya sin declararlo (requisito 6 de la decisión 9) |
| R5 | **Sin stemming español**, la búsqueda por lema tendrá recall bajo en lenguaje jurídico | Media | `HIPÓTESIS no verificada`. **Cualquier afirmación sobre calidad de búsqueda antes de medirla sería inventada.** `SEARCH_INCONCLUSIVE` existe para no convertir un fallo de recuperación en una afirmación sobre el material probatorio |
| R6 | **Rotura del binding**: en un caso por release de Node; en el otro, por versión mayor de la librería controlada por lockfile | Media | Es el argumento central de la decisión 7 y la razón de existir del puerto |
| R7 | **Constraints, triggers y hash-chain son *tamper-evident*, no *tamper-proof*** | Declarada, no mitigable en V0 | Una usuaria hostil con control total del equipo está **fuera del threat model V0** (kernel §8.3) |
| R8 | **Escritura sobre el private state por herramientas genéricas del host** | Bloqueante para el compromiso con un host | Depende del punto B-04 del spike de Cowork, `INCONCLUSIVE`. La protección es **posicional** (ADR-002), no una regla del host |
| R9 | **Ninguna decisión aquí está justificada por rendimiento medido** | Declarada | Es coherente con el alcance de V0, pero significa que la primera medición real puede invalidar una preferencia — nunca un invariante |

## Validacion / pruebas necesarias

| # | Qué se prueba | Cómo | Invariante que verifica |
|---|---|---|---|
| V1 | La regla de dependencias se cumple | Test de arquitectura en CI: ningún import de `infrastructure` desde `domain` o `application`; ningún tipo del binding en sus firmas | 1 |
| V2 | Atomicidad real de *mutación + evento* | Nivel de integración de persistencia: fallo inyectado entre inserciones ⇒ **cero** filas y **cero** eventos | 2 |
| V3 | Ninguna transacción cruza ficheros | Revisión estructural + test: destruir `catalog.db` ⇒ el sistema reconstruye y **ninguna** operación canónica falla | 3, 12 |
| V4 | La ruta del blob es función pura | Property test: `ruta(hash, clase)` determinista; búsqueda de columnas de ruta en el esquema ⇒ **ninguna** | 4 |
| V5 | Write-once y orden bytes→fila | Intento de reescritura de un blob existente ⇒ rechazo; corte simulado entre el paso 3 y el 6 ⇒ huérfano recuperable, **nunca** fila sin blob | 5, 6 |
| V6 | Inmutabilidad de la evidencia original tras la incorporación | `re-hash(bytes) == content_hash`; alterar o borrar el archivo de origen tras la incorporación ⇒ Source y derivados intactos | 5; PF-002 |
| V7 | Rechazo de ubicación no local | Abrir un Case en una ruta de red o sincronizada ⇒ rechazo, con mensaje de producto y no de ingeniería | 7 |
| V8 | Verificación de `journal_mode` al abrir | Preparar un `case.db` fuera de WAL ⇒ el Core lo detecta y no asume | 8 |
| V9 | Migración con backup verificado y restauración | Migración feliz; fallo dentro de la transacción ⇒ rollback; fallo con marcador presente ⇒ restauración automática desde backup verificado y arranque en solo lectura | 9, 10 |
| V10 | El backup está **verificado**, no solo escrito | Restaurar la copia a ubicación aislada, verificar integridad, verificar la cadena de eventos **sobre la copia**, comparar conteos por tabla y `schema_version`. Solo un veredicto positivo habilita migrar | 9, 10 |
| V11 | Degradación a solo lectura ante mismatch de integridad | Alterar un blob a mano ⇒ no se sirve contenido, se degrada a solo lectura y **se dice** | 10 |
| V12 | La co-localización no sostiene ningún invariante epistémico | Revisión dirigida: ningún invariante del Domain cita fichero, directorio ni base de datos | 11 |
| V13 | Reversibilidad declarada en la decisión 9 | Los niveles de Domain y Application pasan **sin cambios** al sustituir el adapter. Si necesitan cambios, hay una regla del Domain filtrada al adapter | 1, 11 |
| V14 | Cierre de los `POR VERIFICAR` del binding | Comprobar contra el binario concreto: claves foráneas por conexión, índices parciales, copia consistente, comprobación de integridad, modo de contenido y tokenizer de FTS5, semántica de `synchronous` bajo WAL, `rename` con destino existente en Windows, PK de texto | Precondición de todo lo anterior |

**Regla de honestidad sobre V14: mientras un punto no esté verificado, la defensa que dependa de él no se cuenta como activa.** En particular, ninguna clave foránea cuenta como defensa hasta que se verifique su habilitación por conexión.

## Preguntas pendientes

1. **Binding concreto** (decisión 7): ¿`better-sqlite3` o `node:sqlite`? Bloqueante, registrada como **OD-03** en `16-open-implementation-decisions.md`. Requiere cerrar antes la comprobación de prebuilds en Windows.
2. **Ubicación no válida: ¿rechazar o advertir?** Recomendación: **rechazar**, por coherencia con la inmutabilidad de la evidencia original. Depende de resolver cómo se detecta de forma fiable una carpeta sincronizada en Windows (R1).
3. **Retención y poda de `operational.db`.** Heredada de ADR-004. No decidir significa no podar, que es el estado seguro.
4. **Recolección de blobs huérfanos:** cuándo se ejecuta y con qué registro. Vive en el plano administrativo (runtime/CLI), nunca en la superficie del modelo.
5. **Deduplicación física de Sources entre Cases.** Hoy no existe: cada blob pertenece a un Case. Introducirla exige tabla de refcount, política de expurgo y migración de layout, y **cambia la consecuencia 3 de la decisión 8**.
6. **Tratamiento de `ñ` en la normalización de búsqueda.** Recomendación registrada: conservar `ñ` como carácter propio y despojar solo tildes, para no colapsar *año/ano*. No bloquea el arranque: su reversión es reindexar dato **derivado**, jamás dato canónico.
7. **Anclaje del hash-cabeza fuera del workspace.** Refuerza el hash-chain frente a un adversario que hoy está fuera del threat model; no cambia ninguna garantía declarada.
8. **Reingestión del mismo material con procedencia declarada distinta:** si el registro de la procedencia adicional es mutación canónica —y por tanto emite evento— o no. Heredada de `04` §10 C4.
9. **Ids opacos como texto o como binario.** Propuesta: texto. Reversible; afecta a almacenamiento e índices, no a la semántica.

## Relaciones con otros ADRs

| ADR | Relación |
|---|---|
| **ADR-002 (Accepted) — Protected local case store** | **Este ADR lo materializa sin ampliarlo.** ADR-002 decidió que el estado canónico vive en un private state fuera de toda carpeta alcanzable por el host y que *la regla es la separación, no el path*; este ADR decide con qué motor y con qué layout, y **no fija la ruta**, que sigue sin ser arquitectura. La verificación periódica de integridad que ADR-002 pide se materializa en V6 y V11 |
| **ADR-003 (Accepted) — Epistemic domain model** | Fuente de la inmutabilidad del `Source` tras la incorporación, que aquí se materializa como blob **write-once**. Este ADR **no** añade ni relaja ningún invariante epistémico |
| **ADR-004 (Accepted) — Case memory** | Fuente del log append-only y hash-chained, de la biyección mutación↔evento y de la concurrencia optimista. Los requisitos 1, 2, 4 y 5 de la decisión 9 son suyos, no de este ADR. El esquema queda **neutral** respecto del *ADR AMENDMENT CANDIDATE* sobre `event_seq` / `case_revision`: no se añade ningún `CHECK` que fije uno de los dos modelos |
| **ADR-005 (Accepted) — Human authority** | Fuente del uso único de la autorización, que aquí exige del motor la capacidad de unicidad parcial aplicable (requisito 3) |
| **ADR-006 (Accepted) — Evidence incorporation boundary** | Fuente de la idempotencia por hash de contenido, que aquí se materializa como `UNIQUE(content_hash)` **más** idempotencia a nivel de bytes en el almacén de blobs |
| **ADR-008 (`Proposed`)** | Su forma de `human_authorizations` —por item, con índice parcial único por item vivo— es la que este adapter implementa. Si los dueños ratifican la forma por Proposal, cambia el esquema, **no** esta estrategia |
| **ADR-011 (`Proposed`) — Evidence locator strategy** | Consume de este ADR los refinamientos aditivos sobre `derived_representations` y la retención como restricción del almacén de blobs |
| **ADR-009 / ADR-010 (`Proposed`, pendientes de escritura)** | Sin relación conocida que altere esta decisión. **Se declara como estado, no como garantía** |
| **Product Floor (`PROPOSED`)** | **PF-002** —*original evidence cannot be overwritten or deleted through the product surface*— tiene en este ADR una de sus dos capas de enforcement: el almacén write-once. La otra es la ausencia de capacidad en la superficie MCP. La **verificación periódica** que PF-002 menciona es **`NOT_IMPLEMENTED` en V0**: no hay job ni planificador |

---

**Referencias.** `docs/technical-design/v0/00-technical-kernel.md` §1, §8, §11, §13, §14, §15 · `docs/technical-design/v0/01-system-design.md` §4.1, §7.3–§7.5, §8.2, §10, §11 · `docs/technical-design/v0/04-persistence-model.md` (documento hermano: §1, §3, §4, §5, §6, §7, §8, §9, §10, §11) · `docs/technical-design/v0/12-testing-strategy.md` §2, §3.5 · `docs/technical-design/v0/15-product-floor-proposal.md` §3.2 · `docs/technical-design/v0/16-open-implementation-decisions.md` OD-03 · `docs/research/runtime-dependencies-spike-v0.md` §2, §3 · `docs/technical-design/v0/ESTADO-Y-HALLAZGOS-CRITICOS.md` §1 · `docs/architecture/boundaries.md` §6, §10 · `docs/architecture/principles.md` · ADR-002, ADR-003, ADR-004, ADR-005, ADR-006 (Accepted); ADR-008, ADR-011 (`Proposed`).
