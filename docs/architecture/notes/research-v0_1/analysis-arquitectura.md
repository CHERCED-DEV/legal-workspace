## Hallazgos

1. **Independencia del dominio respecto al proveedor de IA (sec. 8) — SÓLIDO.** Es la única forma de que el sistema sobreviva a cambios de modelo/plataforma y es coherente con la restricción de vendor independence (sec. 27). Pero está enunciada, no diseñada: el documento no dice dónde queda el LLM en la arquitectura, y esa omisión es el mayor hueco de la sección.

2. **El diagrama lineal `DOMAIN → APPLICATION → PORTS → ADAPTERS` (sec. 8) — REFINAR.** Ports no es una capa debajo de Application: los ports son las interfaces que Application declara, y existen en dos direcciones (entrantes/driving y salientes/driven). El diagrama lineal induce a pensar que todo adapter es "salida", cuando el adapter más importante del sistema (el servidor MCP) es de *entrada*.

3. **Posición del LLM sin definir — RIESGO.** El documento dice "Claude es operador, no fuente de verdad" (sec. 7) pero la arquitectura no lo ubica. Sin esa decisión, el contrato MCP↔Application, el modelo de permisos y la validación de mutaciones quedan flotando. Es la decisión arquitectónica número uno de esta dimensión (ver ADR-1).

4. **Estructura de la sec. 26 mezcla tres ciclos de vida distintos — REFINAR.** `runtime/`, `core/`, `mcp/`, `plugin/` son código (ciclo de release); `knowledge/` y `configuration/` son contenido versionable (ciclo editorial); `workspace/` es datos del usuario (ciclo operativo). Presentarlos como carpetas hermanas sugiere un solo empaquetado, lo que contradice la separación producto/configuración/workspace de la sec. 9. La frontera correcta es por ciclo de vida y política de mutación, no por carpeta.

5. **Ausencia del audit log y del Artifact Registry en el árbol de la sec. 26 — REFINAR.** Ambos aparecen en secs. 13 y 17 pero no tienen lugar físico definido. Si el audit log vive dentro de `case.db` o como archivo aparte cambia el modelo de recovery y de integridad; hoy es DECISIÓN PENDIENTE no señalada.

6. **`workspace/indexes/` como hermano de `cases/` — REFINAR.** Los índices son derivados regenerables (coherente con sec. 19); si conviven al mismo nivel que la fuente de verdad sin marca explícita de "reconstruible", el backup/recovery los tratará como estado primario. Deben declararse desechables por diseño.

7. **Restricciones de la sec. 27 (simplicidad, local-first, idempotencia, append-only) — SÓLIDO.** Son internamente consistentes y descartan de antemano microservicios y RAG-por-defecto (sec. 28), lo cual reduce el espacio de decisión sano. La tensión no resuelta: "local-first" + "diferentes oficinas/organizaciones" (sec. 4) implica en algún momento sincronización o servidor, y ese futuro condiciona hoy el esquema de identidades (ver Decisiones bloqueantes).

8. **Las 18 entidades de la sec. 8 como insumo del slice — PREMATURO.** Para el vertical slice de la sec. 34 bastan ~6 (Case, Evidence/Document, Fact, Statement, Artifact, ProceduralState mínimo). Modelar los 18 antes de validar la base es riesgo de modelo universal especulativo; el resto puede entrar de forma incremental.

9. **Las 12 propiedades de la sec. 34 son un buen contrato de aceptación, pero no están priorizadas — REFINAR.** Tal como están, sugieren que todas pesan igual; no es cierto: 1–4 y 6–8 son el núcleo irreducible; 5, 9, 10 son de segunda ola; 11–12 son capa de presentación que puede validarse con menos rigor al inicio (propuesta concreta en Decisiones bloqueantes).

10. **SQLite + filesystem como hipótesis de persistencia v1 — SÓLIDO bajo condiciones que el documento no ha fijado.** Es adecuado solo si la topología es una máquina y escritores serializados. El documento explícitamente no sabe cuántos usuarios ni qué concurrencia habrá (sec. 31 pide preguntarlo), así que hoy es un SUPUESTO razonable, no una decisión tomada. Límites concretos en la Respuesta 15.

11. **Búsqueda vectorial ausente de la v1 (implícito en sec. 28) — SÓLIDO.** Coherente con el corpus per-case pequeño y con provenance: el retrieval estructurado es explicable; el vectorial no. Falta definir el trigger objetivo de introducción (Respuesta 16).

## Respuestas

### 12. ¿La separación Domain → Application → Ports → Adapters es adecuada?

Adecuada como intención, incorrecta como diagrama. Crítica en tres puntos:

**(a) Ports no es una capa.** En la arquitectura hexagonal los ports son interfaces *declaradas por* Application/Domain, no un estrato intermedio. Y hay dos familias que el documento no distingue: **driving ports** (casos de uso invocables desde fuera: `ingest_evidence`, `propose_facts`) y **driven ports** (dependencias hacia fuera: `CaseRepository`, `TranscriptionProvider`). Todos los ejemplos de la sec. 8 son driven ports; los driving ports —que son exactamente el contrato que MCP expone— no aparecen. Eso explica el hueco del punto (b).

**(b) ¿Dónde queda el LLM?** Mi posición: **el LLM es un cliente externo no determinista, no un adapter ni un componente interno**. El servidor MCP es el *driving adapter* (adapter de entrada) que traduce tool calls en invocaciones a casos de uso de Application. La analogía correcta: el LLM es al MCP lo que un usuario es a una UI — actor externo que opera el sistema pero está fuera de su frontera. Consecuencias de diseño que se derivan y que el documento aún no extrae:
- Application debe diseñarse para un **caller no confiable en secuencia y contenido**: validación total de entradas, idempotencia (sec. 27 ya la pide), errores explícitos y recuperables, ninguna operación cuyo daño dependa de que "el modelo la use bien". Esto convierte la regla de la sec. 12 ("no prohibir solo por prompt") en propiedad estructural: la superficie MCP *es* el perímetro de seguridad.
- El LLM aparece una **segunda vez**, en el lado opuesto: cuando el Core necesita capacidades de IA (transcripción, extracción, resumen) las consume vía driven ports (`TranscriptionProvider`, un eventual `ExtractionProvider`). Son dos roles distintos del mismo proveedor y deben modelarse por separado; confundirlos acopla el dominio a Claude por la puerta de atrás. RIESGO si no se separa.
- Nada del estado puede depender de la memoria conversacional del host (el documento ya lo dice en sec. 13; esta ubicación del LLM lo hace forzoso, no preferible).

**(c) Diagrama corregido:** `[LLM/host conversacional] → MCP server (driving adapter) → Application (use cases + driving ports) → Domain`, con Application dependiendo de driven ports implementados por adapters de infraestructura (SQLite, filesystem, Drive, transcripción). POR VERIFICAR: qué garantías da el host MCP concreto (Cowork/Claude) sobre sesiones, notificaciones de recursos y concurrencia de tool calls; el contrato fino del adapter de entrada depende de eso y no debe asumirse.

### 13. ¿Qué bounded contexts observas?

Sin forzar DDD, veo **tres lenguajes ubicuos claramente distintos** y dos zonas que aún no ameritan frontera:

1. **Gestión de expediente** (Case, Party, ProceduralState, ProceduralEvent, pendientes): lenguaje de "expediente, etapa, término, actuación". Consistencia transaccional por caso.
2. **Ingesta y custodia de evidencia** (Evidence, Document, original, derivado, hash, transcripción): lenguaje de custodia y derivación. Sus reglas (originales inmutables, derivados trazables) no dependen de ningún caso concreto; una misma evidencia puede relacionarse con varios casos (sec. 19 lo prevé).
3. **Conocimiento jurídico** (LegalSource, cita, verificación, jerarquía, jurisdicción): el más claramente separado. Su ciclo de vida es transversal a casos, su verdad es externa (normas, jurisprudencia), su estado clave es "verificada/no verificada", y es el único contexto donde los Knowledge Packs mandan. Mezclarlo con el expediente contaminaría dos nociones de "fuente" distintas.

**Qué NO separar aún:** (a) el *razonamiento del caso* (Fact, Assertion, Hypothesis, Contradiction) frente a gestión de expediente: comparten transacciones y su lenguaje ubicuo apenas está emergiendo del descubrimiento; separarlos hoy sería especulación. (b) *Workflow/etapas procesales* como contexto propio: PREMATURO; en v1 es orquestación dentro de casos de uso. (c) *Artifact Registry*: es un módulo de soporte de Application, no un contexto con lenguaje propio. La separación en v1 debe ser **lógica** (paquetes, namespaces de tablas, interfaces entre módulos), nunca de despliegue.

### 14. ¿Case Management, Evidence, Legal Research, Workflow y Artifact Management como módulos separados?

**Monolito modular con fronteras internas exigidas**, no módulos desplegables. Justificación: un solo proceso local, un solo ciclo de release (sec. 9), cero costo de red/serialización, y la sec. 28 ya veta microservicios. Pero las fronteras deben ser reales: paquetes separados, dependencias solo vía interfaces, prohibición de imports cruzados verificada en CI, y tablas con namespace por módulo dentro de `case.db` (o bases separadas para conocimiento jurídico, que es cross-case — ver ADR-4). Matices por módulo: **Evidence** y **Legal Research** tienen el derecho más claro a módulo (fronteras del punto 13). **Case Management** es el módulo anfitrión. **Artifact Management** es módulo de soporte pequeño (registro + staleness), no unidad mayor. **Workflow NO es módulo en v1**: es la secuenciación dentro de use cases; introducir un motor de workflow sería arquitectura por moda (sec. 27, simplicidad). Trade-off aceptado: el monolito modular exige disciplina sin frontera física; el mecanismo de enforcement (lint de dependencias) es barato y suficiente a esta escala.

### 15. ¿SQLite + filesystem es suficiente para la primera versión?

Sí, **bajo topología de una sola máquina**. Límites concretos y honestos:

- **Concurrencia de escritores — HECHO VERIFICADO** (comportamiento documentado y estable de SQLite): un solo escritor a la vez; en modo WAL los lectores no bloquean al escritor ni viceversa. Para esta carga (ingestas y commits de hechos: eventos por minuto, no por milisegundo) la serialización de escritores es irrelevante en la práctica.
- **Multi-usuario en red — HECHO VERIFICADO como advertencia documentada de SQLite**: el locking sobre filesystems de red (NFS/SMB) es poco fiable y hay riesgo de corrupción. Traducción operativa: `case.db` en una carpeta compartida de oficina **no es un despliegue válido**. Este es el verdadero límite, no el volumen.
- **Volumen — HECHO VERIFICADO** que los límites teóricos de SQLite (tamaño de BD del orden de terabytes) superan por órdenes de magnitud este caso. Estimación propia (HIPÓTESIS con aritmética simple): una audiencia diaria de ~2h produce en el orden de 100–300 KB de transcripción; años de operación de una oficina caben en decenas–cientos de MB de texto. Los blobs (audio/video) van al filesystem, no a la BD; el límite ahí es disco y estrategia de backup, no SQLite.
- **Full-text — HECHO VERIFICADO**: FTS5 existe y da búsqueda con ranking. **Limitación real**: sus tokenizers de serie no incluyen stemming en español (porter es para inglés); búsqueda "demandó/demandar" no matchea sin trabajo adicional. POR VERIFICAR: extensiones de stemming español disponibles y su costo; alternativa v1: normalización propia (minúsculas, tildes) + búsqueda por prefijo, que probablemente baste para el slice.
- **Sincronización/multi-dispositivo**: SQLite no la resuelve; copiar el archivo entre máquinas sin coordinación es receta de pérdida silenciosa. NO TENEMOS INFORMACIÓN SUFICIENTE sobre si esto se necesita (pregunta 1 a los dueños).

**Deja de ser suficiente cuando**: (a) dos o más personas escriben desde máquinas distintas; (b) el expediente debe residir en red; (c) se requiere colaboración simultánea o sincronización entre dispositivos. Ninguno de los triggers es de tamaño; todos son de topología. SUPUESTO de trabajo: v1 = una abogada, una máquina.

### 16. ¿Necesitamos inicialmente búsqueda vectorial?

**No.** Argumentos: (1) el corpus de recuperación en v1 es *per-case* y pequeño (decenas–cientos de documentos); a esa escala, retrieval estructurado (hechos↔evidencia, metadata, cronología) + FTS + lectura selectiva de fragmentos anclados (página/timestamp) cubre la propiedad 5 de la sec. 34. (2) El retrieval vectorial es inexplicable frente al requisito de provenance: "similitud 0.78" no responde "¿de dónde salió?". (3) Introduce pipeline de embeddings, dependencia de modelo (acoplamiento que la sec. 27 quiere evitar) y estado derivado adicional. (4) La sec. 28 ya rechaza "RAG como respuesta automática".

**Qué usar primero**: consultas estructuradas sobre `case.db` + FTS5 + índices navegables generados en la ingesta (índice de transcripción con timestamps, índice documental). El LLM como operador puede navegar un caso con eso, igual que un humano navega un expediente indexado.

**Trigger objetivo para introducirla** (medible, no vibes): construir un set de evaluación de consultas reales de la usuaria ("¿este documento contradice algo?", "busca dónde se mencionó X"); cuando la tasa de fallo de recall de FTS+estructurado supere un umbral acordado sobre ese set, o cuando entre el caso de uso de **búsqueda sobre corpus jurisprudencial masivo cross-case** (Legal Research a escala, que es donde la semántica sí paga), se introduce como adapter detrás del port `SearchProvider` ya previsto en sec. 8 — sin tocar Domain. Los embeddings serían derivados regenerables, categoría que la sec. 19 ya contempla. POR VERIFICAR en su momento: opciones concretas de almacenamiento vectorial local compatible con SQLite; no debe decidirse hoy.

## Invariantes candidatos

1. **Original inmutable**: tras la ingesta, el blob original y su hash no cambian nunca; ninguna operación expuesta puede sobrescribirlo. Capa: Infraestructura (store direccionado por contenido) + regla de Domain. Prueba: test que intenta mutación por cada operación expuesta + re-verificación periódica de hashes.
2. **Todo derivado referencia su original y su método/versión de generación**. Capa: Domain (modelo) + Application (al crear derivados). Prueba: constraint de esquema + property test sobre la ingesta.
3. **`case.db` es la única fuente de verdad; `memory.md` es proyección regenerable**: borrar y regenerar `memory.md` produce contenido semánticamente equivalente. Capa: Application. Prueba: golden test de regeneración.
4. **Ninguna mutación de estado ocurre fuera de un caso de uso de Application**: el adapter MCP no escribe persistencia directamente. Capa: MCP + Application. Prueba: lint de dependencias en CI (el paquete MCP no importa persistencia) + ausencia de tools genéricas de escritura.
5. **Revisión optimista**: un commit basado en una revisión obsoleta del caso se rechaza con error explícito, jamás se fusiona silenciosamente. Capa: Application. Prueba: test de integración con dos escrituras concurrentes simuladas.
6. **Ingesta idempotente**: re-ingerir bytes idénticos no duplica el original (dedupe por hash) y queda registrado el intento. Capa: Application. Prueba: doble ingesta → un original, dos eventos.
7. **Aislamiento entre casos**: ninguna operación con un caso abierto retorna datos de otro caso salvo operación multi-caso explícita. Capa: Application + MCP. Prueba: fuzzing de tool calls con dos casos sembrados, verificando que ninguna respuesta cruza IDs.
8. **Audit log append-only y completo**: cada caso de uso mutador emite exactamente un evento; los eventos pasados no son editables por ninguna operación expuesta. Capa: Application (emisión) + Infraestructura (almacenamiento). Prueba: conteo mutaciones == conteo eventos; intento de edición falla.
9. **Domain sin dependencias de infraestructura/IA**: el paquete de dominio no importa SQLite, MCP, ni SDKs de proveedores. Capa: Configuración de build/CI. Prueba: lint de imports.
10. **Índices reconstruibles**: destruir `indexes/` y reconstruir desde originales + `case.db` produce resultados de consulta equivalentes; ningún dato primario vive en índices. Capa: Infraestructura. Prueba: test de destrucción/reconstrucción.
11. **Superficie MCP cerrada**: el conjunto de tools es enumerado y ninguna acepta rutas arbitrarias fuera del case store. Capa: MCP. Prueba: contract tests + intentos de path traversal.
12. **Artifact con insumos por hash y generador versionado**: el staleness de un artifact es computable comparando hashes de insumos y versión de skill. Capa: Application. Prueba: cambiar un insumo → artifact marcado obsoleto sin intervención manual.

## ADR candidatos

**ADR-1 — Posición del LLM: cliente externo vía driving adapter MCP.** Contexto: el documento declara a Claude "operador" sin ubicarlo arquitectónicamente. Decisión posible: LLM fuera de la frontera del sistema; MCP server como único adapter de entrada; capacidades de IA consumidas por el Core solo vía driven ports separados. Alternativas: (a) LLM como componente interno de Application (acopla el dominio al proveedor, viola sec. 8); (b) LLM como "adapter" (categoría errónea: no adapta nada, origina intenciones). Consecuencias: Application debe ser defensiva e idempotente; el perímetro de seguridad es la superficie MCP; testeable sin LLM. Información faltante: garantías del host MCP concreto (POR VERIFICAR).

**ADR-2 — Monolito modular con fronteras verificadas por CI.** Contexto: cinco módulos candidatos, escala de una oficina. Decisión posible: un proceso, paquetes separados con interfaces, namespaces de tablas. Alternativas: microservicios (vetado, sec. 28); monolito sin fronteras (erosión garantizada). Consecuencias: refactor barato de fronteras mientras el dominio se aprende; requiere disciplina automatizada. Faltante: lenguaje/runtime de implementación (no decidido en el documento).

**ADR-3 — Persistencia v1: SQLite (WAL) + filesystem, una máquina, un escritor lógico.** Contexto: local-first, usuaria única supuesta. Alternativas: Postgres embebido/local (más capacidad multi-cliente, más operación); solo filesystem+JSON (sin transacciones ni FTS). Consecuencias: veto explícito a carpeta de red; estrategia de backup por archivos; migraciones versionadas de esquema desde el día 1. Faltante: número real de usuarios/máquinas y requisito de ubicación del expediente — **bloqueante**.

**ADR-4 — Conocimiento jurídico en almacenamiento separado del expediente.** Contexto: LegalSource es cross-case con ciclo de vida propio; `case.db` es per-case. Decisión posible: base/almacén separado para fuentes jurídicas verificadas y caché de investigación, referenciado desde casos por identificador estable. Alternativas: todo en cada `case.db` (duplica y desincroniza verificaciones). Consecuencias: la "verificación" de una fuente se hace una vez y se comparte; requiere definir identidad estable de fuentes jurídicas. Faltante: formato de citación/identidad de fuentes colombianas (dominio, POR VERIFICAR con la profesional).

**ADR-5 — Retrieval v1 = estructurado + FTS; vectorial diferido detrás de `SearchProvider` con trigger medible.** (Contenido en Respuesta 16.) Faltante: set de evaluación de consultas reales.

**ADR-6 — Identidad y anclaje: IDs opacos por entidad + hash de contenido para originales + anclas de fragmento (página/rango/timestamp).** Contexto: provenance (props. 3, 6) y futura sincronización exigen identidades estables desde v1; cambiarlas después es migración dolorosa. Alternativas: rutas de archivo como identidad (frágil), IDs secuenciales por tabla (chocan al sincronizar). Faltante: decisión sobre futuro multi-dispositivo, que inclinaría a IDs globalmente únicos.

## Decisiones bloqueantes

1. **Topología de despliegue** (¿cuántos usuarios, cuántas máquinas, dónde reside el expediente?): decide si ADR-3 es viable o nace muerto. Todo lo demás de almacenamiento cuelga de esto.
2. **ADR-1 (posición del LLM y contrato MCP↔Application)**: sin él no se puede diseñar la superficie de tools del slice ni el modelo de validación; las propiedades 11–12 de la sec. 34 dependen del host elegido (POR VERIFICAR sus capacidades).
3. **ADR-6 (esquema de identidades y anclas)**: la propiedad 6 (provenance) es indemostrable sin decidir cómo se identifica un fragmento; y es la decisión más cara de revertir.
4. **Mecanismo de revisión** (¿revisión optimista por caso basta?): bloquea la propiedad 10; propongo aceptar revisión optimista para el slice y revisarla con datos.
5. **Frontera exacta de fuente de verdad** (qué vive en `case.db`, qué en filesystem, qué es proyección): bloquea las propiedades 3 y 7 y la estrategia de backup.

**Propuesta de vertical slice (sec. 34).** Orden por dependencia: núcleo irreducible = propiedades **1, 2, 3, 4, 6, 7, 8** (identidad de caso, ingesta segura, original preservado, derivación, provenance, memoria persistente, reapertura). Segunda ola sobre el mismo slice: **5, 9, 10** (recuperación selectiva, detección de trabajo hecho vía Artifact Registry mínimo, actualización consistente vía revisión optimista). Pueden **simularse manualmente al inicio**: 9 y 10 (sembrar el escenario a mano y verificar la reacción), y 12 parcialmente (la traducción de mensajes puede ser una tabla estática de mensajes estándar antes que una capa completa). La 11 se valida por construcción si el host es conversacional. **Caso de uso demostrador**: *ingesta de una entrevista grabada + un documento → transcripción como derivado anclado con timestamps → `propose_facts` produce hechos candidatos cada uno con provenance a fragmento → revisión humana y `commit_reviewed_fact` → cierre de sesión → reapertura en sesión nueva con contexto intacto → ingesta de un segundo documento → el sistema señala que el análisis de hechos existente quedó potencialmente obsoleto sin regenerarlo solo*. Ese único flujo ejercita las 12 propiedades y el cuello de botella real declarado ("hecho, prueba" — sec. 5.1).

## Preguntas para los dueños

1. **¿Cuántas personas usarán el sistema en v1, desde cuántas máquinas, y puede el expediente residir en el disco local de una sola máquina?** Importa: valida o invalida SQLite+filesystem (ADR-3) y el veto a carpetas de red. **Bloquea el diseño.**
2. **¿Sobre qué host conversacional correrá el slice (Cowork, Claude Code, otro) y qué capacidades MCP de ese host podemos asumir?** Importa: define el driving adapter y las propiedades 11–12; nada de esto debe asumirse de memoria (POR VERIFICAR con documentación oficial). **Bloquea el contrato MCP del slice.**
3. **¿Volumen y retención esperados de audio/video (horas de audiencia por semana, duración de retención, tamaño de archivos)?** Importa: dimensiona filesystem, backup y costos de transcripción; no cambia la arquitectura lógica. **Puede esperar al diseño del slice, bloquea su operación.**
4. **¿Existe algún requisito externo (confidencialidad, normativa, política de la entidad) sobre dónde pueden residir físicamente los datos del expediente y si pueden salir hacia servicios cloud (transcripción, modelo)?** Importa: puede vetar adapters completos (transcripción cloud) y condiciona el flujo de ingesta. **Bloquea la selección de adapters del slice, no el núcleo.**
5. **Para `commit_reviewed_fact`: ¿la validación humana ocurrirá dentro de la misma interfaz conversacional o se requiere una superficie de revisión aparte (documento, UI)?** Importa: define si el slice puede demostrar human-in-the-loop solo con MCP o necesita un artefacto de revisión adicional. **Puede esperar unas semanas, pero debe resolverse antes de congelar la API del slice.**