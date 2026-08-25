## Hallazgos

1. **"MCP no es la memoria" (sección 12) — SÓLIDO.** Separar interfaz de acceso (MCP) de estado (Legal Core) es la decisión correcta para un dominio donde la integridad importa más que la fluidez; evita que la conversación se convierta en fuente de verdad, alineado con "Claude es operador, no fuente de verdad" (sección 7).

2. **Principio "si no debe ser posible, no se expone" — SÓLIDO en intención, REFINAR en mecanismo.** El documento lo enuncia pero no define *cómo* se materializa: exposición diferenciada requiere saber quién invoca, y el documento no define un modelo de identidad del invocador. Según mi conocimiento hasta enero 2026, el protocolo MCP no transporta identidad de sub-agente dentro de una misma sesión de host — **POR VERIFICAR** contra la especificación vigente y contra lo que Cowork/Claude permite configurar por agente.

3. **Lista de tools de la sección 12 — REFINAR.** Mezcla granularidades y clases sin declararlas: `create_case` (commit), `get_case_context` (lectura), `propose_facts` (propuesta) aparecen como pares. La ausencia de clasificación lectura/propuesta/commit en el propio diseño es el germen del God Interface: sin clases, cada tool nueva se agrega "porque hace falta".

4. **`commit_reviewed_fact` expuesta al modelo — RIESGO.** Si la única interfaz es conversacional, la aprobación humana llega *mediada por el modelo*, que puede afirmar falsamente que hubo revisión. Una tool de commit cuyo prerequisito es "un humano revisó" no puede validar ese prerequisito con un parámetro booleano que el modelo rellena. Es el punto más peligroso de toda la superficie.

5. **`get_case_context` sin contrato — RIESGO.** Tal como está nombrada, invita a volcar el expediente. Sin presupuesto de tamaño, niveles de detalle y declaración explícita de omisiones, produce o bien inundación de contexto o bien contexto parcial presentado como completo — exactamente el riesgo 8 de la sección 3 (incertidumbre oculta).

6. **`verify_legal_source` — REFINAR + POR VERIFICAR.** La tool es correcta conceptualmente (una cita no es "verificada" porque el modelo la generó, sección 16), pero su implementación depende de fuentes jurídicas colombianas con acceso programático cuya existencia/estabilidad **NO TENEMOS INFORMACIÓN SUFICIENTE** para afirmar. La tool puede existir en v1 devolviendo honestamente "no verificado" — su valor inicial es epistemológico, no de búsqueda.

7. **MCP local como frontera de seguridad — RIESGO (parcialmente reconocido en sección 25).** Si Core y MCP server corren en la misma máquina del usuario con acceso completo, la frontera MCP restringe *al modelo*, no al humano hostil ni a otro proceso. Es una frontera de gobernanza del agente, no un perímetro de seguridad. El documento lo reconoce para el producto, pero debe explicitarse para el MCP: el enforcement en Core protege contra el operador-LLM, no contra el dueño del equipo.

8. **Permisos diferenciados por agente (Drafter vs Auditor) — PREMATURO como implementación, SÓLIDO como requisito.** La sección 22 aún cuestiona si esos agentes existirán. Diseñar hoy la matriz agente×tool es prematuro; diseñar hoy el *punto de enforcement* (Core) y las clases de operación no lo es, porque cambiarlo después es caro.

9. **Tools de la sección 12 incluidas antes del slice — PREMATURO parcial.** El vertical slice (sección 34) no exige capacidades jurídicas ("posteriormente podremos montar capacidades jurídicas encima"). `propose_facts`, `commit_reviewed_fact`, `verify_legal_source` y `get_procedural_state` pueden diferirse a la fase inmediatamente posterior; incluirlas en el slice infla la superficie a validar.

10. **Resources vs tools sin explorar — REFINAR.** HECHO con reserva: hasta mi corte de conocimiento, MCP define tools (invocadas por el modelo) y resources (contenido cuya inclusión controla la aplicación/cliente); si el host soporta resources bien, `memory.md`/proyecciones de caso serían candidatos naturales a resource en lugar de tool. **POR VERIFICAR**: soporte real de resources en Cowork/clientes Claude actuales y su semántica exacta de inclusión. El diseño no debe depender de resources hasta verificarlo; tools son la vía conservadora.

## Respuestas

### 17. Responsabilidades dentro del Legal MCP y cuáles NO

**Dentro del MCP (interfaz semántica delgada):**
- Traducción 1:1 de cada tool a un use case de Application; el MCP no orquesta varios use cases.
- Validación *sintáctica* de inputs (schema, tipos, ids bien formados) — la validación *semántica* (¿existe el caso?, ¿la revisión coincide?, ¿el invocador puede?) es del Core.
- Traducción de errores del Core a errores semánticos estables (`REVISION_DESACTUALIZADA`, `FUENTE_NO_VERIFICADA`) sin filtrar detalles de infraestructura; la capa UX luego los traduce a lenguaje jurídico (sección 10). El MCP emite el vocabulario intermedio, no el texto final al usuario.
- Contratos de salida: toda respuesta incluye `case_id`, `case_revision` e ids opacos reutilizables (fragmentos, evidencias) para encadenar llamadas.
- Descripciones de tools: son la "documentación que el modelo lee"; su redacción es responsabilidad del MCP y debe versionarse con el release.

**Fuera del MCP (nunca):**
- Lógica de dominio: qué es un hecho acreditado, cuándo una cita está verificada, reglas de transición de estados.
- Decidir verdad: el MCP jamás marca algo como verificado/acreditado; solo transporta la decisión del Core.
- Estado propio: cero persistencia en el server MCP (ni caché de caso, ni "sesión" con memoria). Si el MCP muere y renace, nada se pierde. Un caché de rendimiento, si algún día hace falta, vive en infraestructura del Core, no en el MCP.
- Autorización: el MCP puede *no exponer* una tool (primera línea), pero el rechazo autoritativo ocurre en el Core (segunda línea). Nunca solo en prompt.
- Acceso directo a almacenamiento: el MCP no toca `case.db` ni el filesystem del workspace; solo invoca el Core.

Trade-off explícito: un MCP tan delgado duplica aparentemente validación (schema en MCP, semántica en Core). Es duplicación deliberada — defensa en profundidad — y el costo es bajo porque los schemas se generan del contrato del Core.

### 18. API semántica mínima

Propongo **10 tools** divididas en núcleo del slice (7) y extensión jurídica inmediata (3). Clases: **[L]** lectura, **[P]** propuesta, **[C]** commit.

**Núcleo del slice (sección 34):**

1. **`open_case` [L]** — Resuelve identificador natural ("el caso de Andrea") a `case_id` + resumen mínimo + `case_revision`. Existe porque toda operación posterior necesita identidad persistente (propiedad 1 del slice). Absorbe `list_cases` vía búsqueda difusa que devuelve candidatos cuando hay ambigüedad. Input: texto o id. Output: caso o lista de candidatos — nunca "adivinar" el caso.
2. **`create_case` [C]** — Crea caso con datos mínimos. Separada de `open_case` porque crear es commit y abrir es lectura; con idempotency key para no duplicar ante reintento (sección 27, idempotencia).
3. **`ingest_evidence` [C]** — Registra un original (referencia a fuente + metadata), dispara derivaciones asíncronas. Output: `evidence_id`, hash, estado de derivación. Existe para las propiedades 2-4 del slice. No recibe rutas arbitrarias del modelo: recibe referencias que el Core/host resolvió (**DECISIÓN PENDIENTE**: mecánica exacta de cómo llega el archivo).
4. **`get_case_context` [L]** — Ver respuesta a la pregunta específica abajo; con parámetros `nivel` y `seccion`, salida acotada y con omisiones declaradas.
5. **`search_case` [L]** — Recuperación selectiva sobre evidencia/derivados/estado del caso. Output: fragmentos con `fragment_id` + provenance (documento, página/timestamp). Existe para la propiedad 5 sin volcar expediente.
6. **`get_evidence_fragment` [L]** — Dado un `fragment_id` o `evidence_id`+rango, devuelve el contenido exacto con su cadena de provenance. Complementa `search_case`: buscar es aproximado, citar exige el fragmento exacto (sección 16).
7. **`register_artifact` [C]** — Registra un producto de trabajo con inputs, versión de metodología y relación `supersedes` (sección 17). Existe para las propiedades 9-10: sin registro de artifacts no hay detección de trabajo ya realizado. La *consulta* de artifacts vigentes la cubre `get_case_context` (sección "trabajo realizado"), evitando una tool más.

**Extensión jurídica inmediata (post-slice):**

8. **`propose_facts` [P]** — Somete hechos candidatos con referencias de provenance obligatorias (rechazo sintáctico si un hecho llega sin al menos una referencia o una marca explícita de "solo alegado"). Output: `proposal_id` + resultado de validación por hecho. No muta el estado del caso: crea una propuesta pendiente.
9. **`commit_reviewed_fact` [C]** — Promueve hechos de una propuesta a estado comprometido, **solo** con token de aprobación emitido por el Core tras acción humana (ver pregunta 20). 
10. **`verify_legal_source` [P→C]** — Somete una referencia jurídica al pipeline de verificación del Core. Output: `verificada` / `no_verificada` / `no_verificable_aun`, con procedencia de la verificación. El modelo nunca escribe el estado; lo escribe el Core según sus reglas.

Deliberadamente excluidas de v1: `get_case_history` (el audit log es para humanos/soporte, no para el modelo; exponerlo invita a razonar sobre metadatos en vez de sobre el caso), `get_procedural_state` (subsumible como sección de `get_case_context` hasta que exista lógica procesal real), y cualquier tool genérica (`read_file`, `execute_*`).

**Resources:** `memory.md`/proyecciones por sección son candidatas a resources si el host los soporta bien (**POR VERIFICAR**, hallazgo 10). Hasta verificar, `get_case_context` como tool es la vía segura. HIPÓTESIS adicional **POR VERIFICAR**: la spec MCP incluye anotaciones de tools tipo read-only/destructive; si el host las respeta, deberían declararse coherentes con las clases [L]/[P]/[C], pero no puede confiarse en ellas como enforcement.

### 19. Cómo evitar el God Interface

- **Criterios de admisión por tool nueva** (todos obligatorios): (1) mapea a exactamente un use case de Application ya existente y probado; (2) tiene clase declarada [L]/[P]/[C]/[A]; (3) no es expresable componiendo tools existentes con costo razonable; (4) su descripción cabe en ~3 frases sin ambigüedad — si necesita un párrafo, la abstracción está mal; (5) no usa discriminadores tipo `operation: "..."` que la conviertan en multiplexor (eso es un God Interface con un solo nombre); (6) nace con contract tests.
- **Presupuesto de superficie**: techo explícito (propongo 15 para las primeras fases) verificable con un test que cuenta tools del manifiesto y falla el build si se excede. Superarlo exige retirar o fusionar antes de agregar. Justificación práctica: cada definición de tool consume contexto del modelo en cada sesión, y una superficie grande degrada la selección de tool correcta — observación operativa ampliamente reportada; el número exacto donde degrada es HIPÓTESIS, no lo fijo como hecho.
- **Revisión de superficie por release**: cada release lista tools agregadas/modificadas/deprecadas como parte del manifest (sección 25 ya prevé manifest de release); una tool sin invocaciones en N releases es candidata a retiro.
- **Presión estructural**: la asimetría correcta es "muchos use cases en el Core, pocas tools en la superficie". Cuando un Skill necesita algo nuevo, la primera pregunta es si se resuelve con parámetros o composición de tools existentes, no con una tool nueva.
- **Anti-patrón a vigilar**: tools "por conveniencia del Skill" (una tool por Skill). Los Skills consumen la misma API semántica; si un Skill necesita una tool privada, o el Skill está mal diseñado o falta un use case, no una tool.

### 20. Modelo de permisos lectura / propuesta / commit / administración

**Modelo:** cada use case del Core declara su clase de operación; cada *principal* (humano, sesión de agente, proceso administrativo) tiene capacidades máximas por clase, definidas en configuración firmada del producto/cliente, no en prompt.

**Enforcement en dos líneas, autoridad en una:**
1. *Exposición* (MCP): a cada conexión/perfil solo se le declaran las tools de sus clases permitidas. Un hipotético Auditor recibe solo [L]. Esto implementa "si no debe ser posible, no se expone".
2. *Autorización* (Core, autoritativa): aunque la tool esté expuesta por error o el server esté mal configurado, el use case verifica la capacidad del principal y rechaza. La línea 1 sin la línea 2 es teatro; la 2 sin la 1 funciona pero desperdicia contexto y tienta al modelo.

**Identidad del invocador — el hueco real:** según mi conocimiento hasta el corte, MCP no transporta identidad de sub-agente por llamada dentro de una sesión (**POR VERIFICAR** en la spec vigente y en Cowork). Opciones: (a) una conexión/instancia de server por perfil de agente, cada una con superficie distinta — simple, verificable, mi opción preferida si el host lo permite (**POR VERIFICAR**); (b) token de sesión por principal como parámetro implícito — frágil si el token pasa por el contexto del modelo; (c) mientras no haya subagentes, un único principal "operador" con capacidades [L]+[P]+commits no sensibles. Para el slice, (c) basta.

**¿Puede el Drafter commitear hechos? No.** "Hecho acreditado" exige validación profesional en ciertos contextos (sección 15) y la política del cliente lo configura (sección 24). Diseño propuesto para el commit sensible: flujo de dos fases — `propose_facts` crea propuesta; el Core exige una aprobación humana *fuera del canal del modelo* que emite un token de un solo uso ligado a `proposal_id` + `case_revision`; `commit_reviewed_fact` sin token válido falla siempre. El modelo puede *pedir* la aprobación, nunca *fabricarla*. **POR VERIFICAR**: si el mecanismo de elicitation/confirmación del protocolo MCP (que recuerdo incorporado a la spec en 2025) está soportado por el host y garantiza que la confirmación proviene del humano y no del modelo; si no, la aprobación requiere una superficie de UI propia — lo que conecta con una decisión de producto pendiente.

**Administración** (instalar Knowledge Packs, cambiar políticas, migraciones): fuera de la superficie del modelo por completo. No son tools [A] expuestas a Claude; son operaciones del runtime/CLI del producto. Exponer administración al operador-LLM contradice la sección 25.

## Invariantes candidatos

1. **Ninguna tool MCP escribe almacenamiento directamente; toda mutación pasa por un use case del Core.** Capa: MCP/Application. Prueba: test arquitectural de dependencias (el módulo MCP no importa infraestructura de persistencia) + revisión de que el server no posee credenciales/handles de `case.db`.
2. **Ninguna operación invocable por el modelo transiciona un hecho a "acreditado" sin token de aprobación humana validado por el Core.** Capa: Application (regla en Domain). Prueba: invocar `commit_reviewed_fact` sin token, con token expirado y con token de otra propuesta → rechazo en los tres casos.
3. **Toda respuesta de tool incluye `case_id` y `case_revision`.** Capa: MCP. Prueba: contract tests sobre schemas de salida de todas las tools.
4. **Toda tool [C] exige `expected_revision`; mismatch produce error semántico, nunca sobrescritura.** Capa: Application. Prueba: test de concurrencia (mutación intercalada entre lectura y commit).
5. **Toda tool [C] es idempotente bajo reintento con la misma idempotency key.** Capa: Application. Prueba: doble invocación → un solo efecto, misma respuesta.
6. **Ninguna tool acepta rutas de filesystem, URLs arbitrarias ni contenido ejecutable; toda referencia es un id opaco emitido por el Core.** Capa: MCP. Prueba: revisión de schemas + tests negativos con inputs tipo ruta.
7. **Todo contenido derivado devuelto por una tool lleva referencia resoluble a su original (provenance).** Capa: Domain/Application. Prueba: contract test — recorrer cada fragmento devuelto hasta el original.
8. **`get_case_context` respeta un presupuesto máximo de tamaño y declara explícitamente qué secciones omitió o truncó.** Capa: Application. Prueba: caso sintético grande → salida bajo presupuesto con lista de omisiones no vacía.
9. **La superficie no excede el presupuesto de tools del release.** Capa: Configuración/release. Prueba: test automático que cuenta tools del manifiesto.
10. **Toda invocación de tool queda en el audit log con principal, tool, hash de inputs, revisión y resultado.** Capa: Application/Infraestructura. Prueba: ejecutar secuencia conocida y reconstruirla desde el log.
11. **El server MCP es sin estado: reiniciarlo entre dos llamadas no altera ningún resultado.** Capa: MCP. Prueba: test de integración con reinicio del server a mitad de secuencia.
12. **Errores del Core llegan al modelo como códigos semánticos estables, sin stack traces ni detalles de infraestructura.** Capa: MCP. Prueba: inyección de fallos en adapters → verificar salida.

## ADR candidatos

1. **ADR: Punto de enforcement de permisos.** Contexto: "no exponer ≠ suficiente" si la exposición es la única barrera. Decisión posible: autorización autoritativa en Application por principal y clase de operación; exposición diferenciada en MCP como primera línea. Alternativas: solo exposición diferenciada; solo prompt (rechazada por sección 12). Consecuencias: duplicación deliberada, requiere modelo de principal. Falta: cómo identifica el host al invocador (**POR VERIFICAR**).
2. **ADR: Mecanismo de aprobación humana para commits sensibles.** Contexto: hallazgo 4 — aprobación mediada por el modelo es falsificable. Decisión posible: two-phase con token fuera del canal del modelo. Alternativas: elicitation MCP (**POR VERIFICAR** soporte), UI propia mínima, confirmación conversacional (rechazable: falsificable). Consecuencias: fricción de UX; define cuánta UI propia necesita v1. Falta: modelo de revisión humana del cliente (sección 31 ya lo lista).
3. **ADR: Tools vs resources para proyecciones de caso.** Contexto: hallazgo 10. Decisión posible: solo tools en v1; migrar proyecciones a resources si el host los soporta con semántica adecuada. Falta: verificación de soporte en Cowork/clientes.
4. **ADR: Topología servidor-perfil.** Contexto: permisos por agente. Decisión posible: una instancia/conexión por perfil con superficie distinta. Alternativas: server único con token por principal; server único sin diferenciación (solo viable pre-subagentes). Falta: decisión de sección 22 sobre qué agentes existen; capacidades del host.
5. **ADR: Frontera proceso MCP–Core.** Contexto: si corren en el mismo proceso, la "frontera" es solo modular; si son procesos separados, el enforcement es más real pero hay costo operativo local. Decisión posible: mismo proceso en v1 con frontera modular estricta y tests arquitecturales. Consecuencias: la garantía contra manipulación local es menor (aceptado en sección 25). Falta: requisitos de distribución/instalación.
6. **ADR: Contrato de `get_case_context`.** Contexto: hallazgo 5. Decisión posible: niveles (mínimo/estándar/sección), presupuesto de tamaño, modo delta por revisión (`desde_revision`), omisiones declaradas. Alternativas: contexto único fijo; volcado completo (rechazada). Falta: medición real de tamaños de expediente del primer caso de uso.

## Decisiones bloqueantes

1. **Mecanismo de aprobación humana (ADR 2)** — bloquea aunque el slice no incluya hechos: la propiedad 12 del slice ("sin exposición de ingeniería") y el flujo de `ingest_evidence`/`register_artifact` ya requieren saber si existe alguna superficie de confirmación fuera del chat. Diseñar la API sin resolver esto deja `commit_reviewed_fact` sin fundamento y arriesga rediseño.
2. **Contrato de `get_case_context` (ADR 6)** — bloquea: las propiedades 5, 7, 8 y 9 del slice dependen de que el contexto sea acotado, con revisión y con detección de trabajo previo. Es la tool más usada; su contrato define el patrón de todas las demás.
3. **Semántica de revisión (`expected_revision`, qué operaciones la exigen)** — bloquea la propiedad 10 del slice y los invariantes 4-5. Debe decidirse si revisión por caso es suficiente granularidad para v1.
4. **Frontera proceso MCP–Core y mecánica de entrega de archivos a `ingest_evidence`** — bloquea la propiedad 2 (ingestión segura): sin decidir cómo llega físicamente un archivo al Core sin que el modelo maneje rutas arbitrarias, la tool no puede especificarse.
5. **Identidad del invocador** — bloquea solo parcialmente: para el slice basta un principal único "operador"; pero debe decidirse *explícitamente* que se difiere, dejando el campo `principal` en el audit log desde el día uno para no migrar el log después.

## Preguntas para los dueños

1. **¿Qué host concreto ejecutará el MCP en v1 (Cowork, Claude Desktop, Claude Code, otro) y qué control ofrece sobre conexiones/superficies por agente?** Importa porque el modelo de permisos (pregunta 20) depende de capacidades del host que están **POR VERIFICAR**. Bloquea el ADR 1/4; la verificación documental puede hacerse en paralelo pero la elección de host es de ustedes.
2. **¿Cómo imaginan materialmente que la abogada aprueba algo (clic en una ventana, frase en el chat, revisión de un documento generado)?** Importa porque define si el two-phase commit necesita UI propia. Bloquea el ADR 2.
3. **¿En v1 habrá exactamente una usuaria y una sesión activa por caso, o debemos asumir concurrencia (dos sesiones, un colega) desde el inicio?** Importa para decidir si la revisión optimista por caso basta o necesitamos granularidad menor. Bloquea la decisión 3 solo si la respuesta es "concurrencia desde el día uno"; si no, puede esperar.
4. **¿Cómo llegan físicamente los archivos hoy (carpeta local, Drive, correo) en el caso de la abogada?** Importa para especificar `ingest_evidence` sin inventar la mecánica de entrega. Bloquea la decisión 4.
5. **Para `verify_legal_source`: ¿aceptan que en v1 el estado honesto por defecto sea "no verificada" con verificación manual asistida, mientras se investiga qué fuentes oficiales colombianas tienen acceso programático estable?** Importa para no prometer un pipeline de verificación que depende de infraestructura externa no confirmada. No bloquea el slice; bloquea la fase jurídica posterior.