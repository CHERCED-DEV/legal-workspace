# Principios de arquitectura — Legal Workspace / Legal OS

## Estado

**Accepted.** Los quince principios que siguen son **DECISIÓN APROBADA** por los dueños en la fase de consolidación. Sus títulos se conservan en inglés tal como fueron aprobados; la elaboración va en español, y los nombres de entidades, estados, condiciones y tools se escriben en inglés conforme al vocabulario canónico del kernel de consolidación v0.2 (§2–§4).

La lista es **cerrada: quince, ni uno más**. Un principio nuevo es un cambio de contrato de esta capa, no una extensión silenciosa.

Cada principio declara tres cosas: **qué exige**, **qué prohíbe** y **cómo se verifica** — por un mecanismo o un test, nunca por una declaración de intenciones. Un principio que no puede fallar en una prueba no es un principio: es un eslogan, y en este dominio los eslóganes producen exactamente los riesgos que la iniciativa quiere evitar (confundir alegado con acreditado, dar por verificado lo que el modelo generó, mezclar expedientes, destruir trabajo).

---

## 1. LLM is untrusted

Exige tratar al modelo y a cualquier host agentic (Claude Code, Cowork u otro) como **cliente externo situado fuera de la frontera de confianza** del Legal Core: puede interpretar lenguaje natural, leer proyecciones y fragmentos, razonar, proponer y solicitar operaciones. Prohíbe toda autoridad directa sobre el estado canónico — el modelo no escribe la base de datos, no cambia el status de ninguna entidad, no marca nada como verificado, no acredita hechos, no modifica Sources, no altera políticas, no ejecuta migraciones ni administra el runtime. Se verifica de forma adversarial: los tests negativos del slice deben pasar **sin cooperación del modelo** (acreditación directa con actor `AI_*` rechazada, aprobación fabricada rechazada, ids inventados rechazados, operación sobre el Case A con ids del Case B rechazada), y el manifiesto de tools debe contener exactamente las **ocho** tools v0 (**ENMIENDA AC-03 aprobada**, supersede §16.14: `register_artifact` retirado por ser consecuencia necesaria de `propose_facts`) con su clase declarada.

**Materializado en:** ADR-001, con proyección epistémica en ADR-003 y de autoridad en ADR-005.

## 2. Core owns canonical state

Exige que exista un único **Canonical Case State** mantenido por el Core, materializado en el `LEGAL OS PRIVATE STATE` y accesible solo por el camino `host → Legal MCP → Application → Case Store`; nada de lo que vive en el `USER WORKSPACE` (`Inbox/`, `Exports/`, `Working/`) es canónico. Prohíbe todo camino alterno de escritura — nunca `host → filesystem → case.db` — y prohíbe que una proyección, un export o un borrador sean tratados como fuente de verdad. Se verifica con un property test de **biyección mutación↔evento**, según la definición normativa del invariante 5 de ADR-004: **mutación** = cambio de estado canónico registrado, **no** invocación de tool; una sola invocación puede producir de 1 a n mutaciones, y por tanto de 1 a n eventos del Case Event Log. El invariante es que toda mutación produce exactamente un evento y todo evento corresponde a exactamente una mutación (cada evento con su `event_seq`; `case_revision` avanza solo en los eventos que mutan el estado epistémico canónico — **ENMIENDA AC-02 aprobada**, supersede §16.16) — biyección mutación↔evento, no invocación↔evento; el property test verifica la biyección, no el conteo de llamadas. Se verifica además con el test de superficie (ninguna tool acepta rutas de filesystem ni realiza escritura arbitraria) y con la verificación del hash-chain del log.

**Materializado en:** ADR-002 (frontera de estado) y ADR-004 (estado canónico + proyecciones derivadas).

## 3. Prompts cannot enforce invariants

Exige que todo invariante viva en Domain o Application, ejecutado por código del producto sellado, y que la superficie no exponga lo que no debe ser posible. Prohíbe delegar la garantía de una regla crítica a un `SKILL.md`, a un prompt de sistema, a una instrucción conversacional o a un archivo de configuración: son texto que el modelo puede ignorar, malinterpretar o recibir truncado, y un archivo editable no es un mecanismo de cumplimiento. La regla operativa del kernel (§15) es también su test: **si el sistema deja de ser seguro porque el modelo ignoró un SKILL.md, hay lógica crítica en el lugar equivocado**; se verifica ejecutando los tests de invariantes con el skill removido o desobedecido y comprobando que ninguno cambia de resultado.

**Materializado en:** ADR-001.

## 4. Original evidence is preserved

Exige preservar los bytes originales de todo **Source** con su hash SHA-256, su ProvenanceRecord de incorporación y su metadata; los **DerivedRepresentation** (transcripción, OCR, texto normalizado) llevan versión, hash, receta —herramienta y versión— y referencia obligatoria a su Source, y **nunca lo sustituyen**. Prohíbe mutar Sources por la superficie normal del producto y prohíbe exponer cualquier operación de borrado (un expurgo legal futuro sería un procedimiento privilegiado con acta, fuera de la superficie del modelo). Se verifica comprobando que regenerar un derivado no altera el Source ni su hash, que todo anclaje de fragmento refiere a la paginación, offsets o línea de tiempo **del original** y no a la de un derivado o clip, y que el manifiesto de tools no contiene ninguna operación de escritura o borrado sobre Sources.

**Materializado en:** ADR-006 (incorporación y snapshot) y ADR-002 (custodia en el private state).

## 5. Exploration is not incorporation

Exige una única operación formal de incorporación (`ingest_evidence`) para que material externo se convierta en Source y adquiera rol probatorio como Evidence dentro de un Case. Prohíbe que un hallazgo del modelo en un conector, en la web o en `Inbox/` fundamente por sí mismo una transición canónica: la información externa puede **orientar**, nunca **fundamentar**, hasta ser incorporada — regla que no cambia cuando lleguen los conectores post-slice, porque cambia el origen del material, no la operación que lo convierte en evidencia. Se verifica con tests negativos de primera clase: crear un EvidenceLink contra material no incorporado (URL, id de conector, ruta, texto pegado) **falla**; `register_artifact` rechaza cualquier `inputs[]` que no sea entidad del Case Store identificada por id + `content_hash`.

**Materializado en:** ADR-006.

## 6. AI proposes; sensitive state requires human authority

Exige un techo epistémico duro — ningún actor `AI_*` crea ni transiciona un Fact más allá de `PROPOSED` — y un diseño two-phase para lo sensible: `propose_facts` registra una Proposal con `content_hash`, la revisión ocurre fuera del canal del modelo y solo entonces `commit_reviewed_facts` puede ejecutarse contra una **HumanAuthorization** viva, no consumida, registrada server-side en el Core. Prohíbe que cualquier parámetro provisto por el modelo constituya prueba de revisión humana: un `humanReviewed: true` es inválido por construcción porque el contrato no admite tal parámetro, y ningún token portador viaja por el contexto del modelo. Se verifica con los tests de autoridad: commit sin autorización vigente ⇒ `HUMAN_REVIEW_REQUIRED {proposal_id}` sin mutación; autorización consumida o expirada ⇒ mismo rechazo; Proposal editada tras la revisión ⇒ rechazo por discrepancia de `item_content_hash` (**ENMIENDA AC-01 aprobada**, supersede §16.17: la vinculación es por item).

**Materializado en:** ADR-005, con el ciclo de vida epistémico en ADR-003.

## 7. Chat is a channel, not memory

Exige que la memoria operativa del modelo sea un conjunto de **proyecciones tipadas y regeneables** servidas por el Core (`get_case_context` con scopes `overview | facts | evidence | pending | changes_since(revision)`) — donde `changes_since(revision)` es un **refinamiento de la consolidación** sobre el `recent_changes` de la formulación previa, señalado como tal: el delta exige un punto de referencia explícito, y sin él la proyección no es reproducible (kernel §8) —, y que la reapertura de un caso en otra sesión se resuelva desde el estado, no desde el historial conversacional del host. Prohíbe persistir el chat crudo o el razonamiento intermedio del modelo como estado del caso, y prohíbe un `memory.md` monolítico creciente: una proyección orientativa puede existir, pero es **desechable, regenerable y jamás canónica**, y ninguna tool permite escribirla. Se verifica con un golden test de regeneración determinista (mismo estado y misma revisión ⇒ salida idéntica byte a byte), con el rechazo por schema de todo commit cuyo payload sea diálogo, y comprobando que el envelope de respuesta declara `completeness` y `omissions[]` en toda proyección.

**Materializado en:** ADR-004.

## 8. Every relevant claim has provenance

Exige un **ProvenanceRecord** en toda entidad epistémica, con `provenance_kind ∈ EXTERNAL_SOURCE | AI_DERIVATION | AI_INFERENCE | HUMAN_DECISION | SYSTEM` y el `Principal` que ejecutó la operación (`principal_id`, `principal_type ∈ HUMAN | AI | SYSTEM`, `principal_role`), ambos desde el schema inicial; los Artifacts registran `inputs[]` por `entity_id + content_hash` —incluida la DerivedRepresentation exacta consumida—, `methodology_version`, `model_id` y `knowledge_pack_versions[]`. Prohíbe hechos, links y artifacts huérfanos: `propose_facts` rechaza sintácticamente un hecho que llegue sin referencia de provenance y sin la marca explícita "solo alegado", y no existe tercera vía. Se verifica con validación de schema (registro con campos faltantes ⇒ falla), con la ausencia de referencias externas en `inputs[]` y con la trazabilidad completa Fact → EvidenceLink → fragmento → Source por hash.

**Materializado en:** ADR-003 (modelo epistémico), ADR-006 (provenance de incorporación) y ADR-004 (provenance en el Case Event Log).

## 9. Uncertainty must remain visible

Exige que la incertidumbre viaje **tipada y adherida al estado o al Artifact**, no solo al diálogo: catálogo cerrado de siete condiciones v0 (`SEARCH_INCONCLUSIVE`, `ANALYSIS_STALE`, `HUMAN_REVIEW_REQUIRED`, `REVISION_CHANGED`, `UNCERTAIN_FRAGMENT`, `OPERATION_NOT_PERMITTED`, `INTEGRATION_ERROR`), todas user-visible, más `completeness` y `omissions[]` en cada proyección. Ese catálogo se señala como **reducción normativa de la consolidación** —no como recorte silencioso— y descansa en tres unificaciones explícitas (kernel §9, §16): `HUMAN_REVIEW_REQUIRED` **absorbe** `PENDING_CONFIRMATION` de la revisión previa (registrado como superseded); `NEW_EVIDENCE_SINCE_ANALYSIS` deja de ser condición aparte y **se convierte en un `reason` de `ANALYSIS_STALE`** (el delta al abrir un caso es contenido de `changes_since`, no condición); y `NO_SUPPORT_FOUND` **se degrada a dato de proyección** de los scopes `facts`/`pending`, porque un hecho sin soporte es información del expediente, no una anomalía del sistema. Prohíbe tres infidelidades concretas — elevar el estatus epistémico en la presentación (propuesto ≠ alegado ≠ acreditado), confundir una búsqueda fallida con ausencia de prueba, y confundir integridad desde la ingestión con autenticidad del material — y prohíbe que la configuración del cliente suprima condiciones blocking o avisos de incertidumbre. Se verifica con golden tests condición → mensaje, con un caso sintético grande que debe producir `completeness ≠ COMPLETE` y `omissions` no vacío, y comprobando que la marca sobrevive aunque se pierda el canal conversacional.

**Materializado en:** ADR-004 (envelope y condiciones activas); catálogo completo en el documento del vertical slice.

## 10. Domain is vendor-independent

Exige que el Domain razone en sus nueve entidades epistémicas — `Case, Source, Evidence, Statement, Fact, EvidenceLink, ProvenanceRecord, ProfessionalDetermination, DerivedRepresentation` — y que Application razone en los cuatro conceptos de soporte — `Artifact, Proposal, HumanAuthorization, CaseRevision` (addendum v0.3 B.4) — sin que ninguno de los dos planos sepa qué es Claude, Cowork, MCP, un modelo concreto ni una base de datos concreta. Prohíbe que una feature de plataforma se convierta en regla del Domain: los modos de aprobación de conectores, las `ToolAnnotations` del protocolo, los hooks del host o el soporte de elicitation son **detalle de implementación de plataforma** y pueden endurecer el perímetro, nunca sustituir la regla. Se verifica por sustitución: cambiar de host, de modelo o de motor de persistencia no debe tocar ningún invariante ni ningún contrato del Domain, y ningún nombre de proveedor debe aparecer en Domain ni en la firma de un use case.

**Materializado en:** ADR-001 (frontera y vendor independence) y ADR-004 (contratos independientes del host).

## 11. Integrations are adapters

Exige que toda capacidad externa —almacenamiento documental, transcripción, correo, calendario, fuentes jurídicas, búsqueda— se declare como **driven port semántico** y se consuma por adapters intercambiables, de modo que un use case pida una capacidad y nunca un proveedor. Prohíbe que un skill o un use case dependan de un proveedor concreto y prohíbe que un fallo de integración deje al usuario sin saber qué pasó con su expediente: `INTEGRATION_ERROR {integration, effect_on_state}` declara **siempre** el efecto sobre el estado (v0: `NONE`). Se verifica por sustitución de adapter (cambiar el proveedor de transcripción no toca Domain ni Application) y con un contract test por port que corra contra un adapter falso.

**Materializado en:** ADR-006 (frontera de material externo) y la sección *Driven Ports* de `boundaries.md`.

## 12. Local-first does not mean LLM-offline

Exige, en términos de dominio, que **el estado canónico y la evidencia vivan bajo control exclusivo del Core, con custodia local**: ninguna entidad canónica ni ningún byte original quedan en manos del host, de un servicio externo o del `USER WORKSPACE`. La co-localización de procesos **no es regla del sistema**, sino consecuencia del adapter de persistencia elegido para v0: mientras la persistencia sea SQLite en modo WAL, la co-localización de todos los procesos en una misma máquina es requisito de corrección **de ese adapter** — **HECHO VERIFICADO** (kernel §1; fuente: sqlite.org): en modo WAL lectores y escritores corren concurrentemente con un solo escritor a la vez, y WAL **no funciona sobre filesystems de red**, con corrupción documentada por locking defectuoso especialmente en NFS. A ello se suma que el slice fija **una máquina** como parámetro aprobado (kernel §11). Si el adapter cambia, cambia la restricción; la exigencia de dominio permanece. No exige, en cambio, que el sistema funcione sin modelo: la IA como capacidad (transcripción, extracción) puede ser remota y se consume por driven ports con provenance `AI_DERIVATION`/`AI_INFERENCE`. Prohíbe que la disponibilidad del proveedor se vuelva condición de la integridad del expediente: abrir un caso, servir proyecciones, leer el Case Event Log y verificar el hash-chain no dependen de ningún servicio externo. Se verifica deshabilitando toda capacidad de IA y comprobando que el Core sigue operando en lectura y auditoría, con las derivaciones en `PENDING`/`FAILED` visibles en `get_case_context(pending)`.

**Materializado en:** ADR-002 (localidad del private state) y ADR-001 (la IA como capacidad entra por ports, no por la frontera del operador).

## 13. Prefer deterministic mechanisms over LLM judgment when possible

Exige que toda función computable desde el estado se implemente como código determinista del Core: cronología, staleness de Artifacts, estados derivados del Fact (`SUPPORTED | CONTRADICTED | UNSUPPORTED`), idempotencia por hash, resolución de identificadores, presupuesto y truncado de proyecciones. Prohíbe encargar al modelo lo que una consulta o una regla resuelven — por eso `chronology-builder`, `citation-verification`, `procedural-state` y `final-quality-review` salieron del catálogo de Skills hacia Application, Core/Adapter y gates del Core (kernel §15) — y reserva el juicio del modelo para donde su salida es una **Proposal revisable**, nunca un hecho consumado. Se verifica con el golden test de regeneración determinista y con una revisión de catálogo: todo skill cuya salida sea reproducible por código es un candidato a mover, y la carga de la prueba recae en quien quiera mantenerlo como skill.

**Materializado en:** ADR-004 (proyecciones deterministas); catálogo consolidado en kernel §15 y en `boundaries.md`.

## 14. No premature distributed architecture

Exige la solución más simple que satisfaga los invariantes para el alcance real del slice (una usuaria, una máquina, cero subagentes, ningún conector externo): estado materializado en tablas, concurrencia optimista sin locking pesimista, estado de derivación en la propia `DerivedRepresentation` en lugar de un motor de jobs genérico, y **no** full event sourcing. Prohíbe introducir replicación, colas, microservicios, enjambres de agentes o caché de proyecciones sin un trigger presente en los requisitos; cada rechazo se registra como decisión con su condición de reapertura declarada, no como omisión. Se verifica exigiendo una medida antes de cada pieza distribuida —latencia observada, contención real, frecuencia de `REVISION_CHANGED` espurios— y comprobando que el camino de evolución sigue abierto (el Case Event Log ya guarda payloads suficientes para reconstrucción).

**Materializado en:** ADR-004 (no event sourcing, sin locking pesimista) y los parámetros del slice en kernel §11.

## 15. Security through capabilities, not instructions

Exige que lo que no debe ser posible **no se exponga**: superficie MCP cerrada de **ocho** tools v0 (**ENMIENDA AC-03 aprobada** (supersede §16.14: `register_artifact` retirado por ser consecuencia necesaria de `propose_facts`)), cada una con clase declarada (`QUERY | COMMAND | PROPOSAL | SENSITIVE_COMMAND | ADMIN`), con la clase `ADMIN` **vacía por diseño** —migraciones, gestión de packs y reparación existen solo en el runtime/CLI del producto— y con least privilege por principal y perfil. Prohíbe apoyar una restricción en una instrucción al modelo o en un hint del protocolo: **HECHO VERIFICADO** (kernel §1; fuente: spec MCP vigente 2026-07-28) la spec no define RBAC —los permisos se aplican en la capa cliente— y las `ToolAnnotations` (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`) son explícitamente no confiables. Se verifica con dos mecanismos distintos, que no deben confundirse. Primero, el **test de superficie** (**ocho** tools con clase; `ADMIN` cuenta cero elementos, canario verificable contra la erosión incremental): una operación **inexistente en la superficie** —acreditar directamente, modificar un Source, marcar una fuente jurídica como verificada en v0— **no produce ninguna condición del catálogo**, porque el resultado esperado es que la tool no exista en el manifiesto; el fallo ocurre en el protocolo y el Core nunca ve la operación, y lo que llega a la usuaria es mensaje de producto, no condición tipada. Segundo, los **tests de perfil**, que deben producir `OPERATION_NOT_PERMITTED {operation, policy_reason}` con motivo en términos de política, jamás de ingeniería: esa condición es del Core y se emite **únicamente cuando la capacidad existe y una política o el perfil del principal la vetan**.

**Materializado en:** ADR-001 (superficie como perímetro de gobernanza) y ADR-002 (perímetro de escritura frente al host).

---

## Anexo — Product Floor v0

**DECISIÓN APROBADA** (kernel §14; etiqueta de la taxonomía del kernel §0). Lo que los dueños calificaron "en principio" se expresa aquí en prosa y no como etiqueta nueva: **el mecanismo del piso está aprobado** —existirán políticas de seguridad e integridad que el cliente no puede relajar, y la configuración solo puede endurecerlas— mientras que **el contenido de la lista es un primer conjunto universal, abierto a ampliación** cuando el uso real revele otras políticas que no admiten configuración. Fuente auditable: cita literal de los dueños en el §21 del prompt de consolidación, recogida en el Anexo B.4 del addendum normativo v0.3: *"Existirán políticas de seguridad/integridad que el cliente no puede relajar. La configuración puede endurecerlas. No debilitarlas."* La regla que gobierna el anexo completo es una sola: **la configuración del cliente solo endurece, nunca relaja**. Sin este piso, el producto podría configurarse para producir exactamente el riesgo que la iniciativa existe para evitar.

1. **Una fuente jurídica no verificada jamás se promueve a verificada de forma silenciosa ni por afirmación del modelo.**
2. **Ningún actor `AI_*` efectúa transiciones epistémicas sensibles** (`ALLEGED`, `DETERMINED`) **ni las autoriza.**
3. **Las condiciones de clase blocking y los avisos de incertidumbre no son suprimibles por configuración de cliente**; la configuración solo endurece.
4. **Los Sources son inmutables por la superficie normal del producto y no existe operación de borrado expuesta** (un expurgo legal futuro sería un procedimiento privilegiado con acta, fuera de la superficie del modelo).
5. **La auditoría (Case Event Log) no es desactivable ni editable por configuración.**

**Enforcement:** el piso se aplica en el Core, en los gates de commit y de export, con independencia del host y de la configuración cargada. Una Client Config que intente relajar cualquiera de las cinco políticas es **inválida** y se rechaza de forma visible: nunca se degrada silenciosamente a defaults.

**Relación con los principios:** la política 1 realiza los principios 8 y 9; la 2 realiza el 6; la 3 realiza el 9; la 4 realiza el 4; la 5 realiza el 2 y el 8.
