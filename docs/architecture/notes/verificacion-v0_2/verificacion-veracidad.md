# Verificación de VERACIDAD — consolidación documental Legal OS

Ámbito: kernel v0.2 (§1–§17) contra los 10 documentos producidos. 18 hallazgos, ordenados por gravedad. Categorías entre corchetes según el foco asignado (a)–(g).

---

## Resumen por categoría

- **(a) Afirmaciones de plataforma fuera del kernel §1** — 3 hallazgos (H1, H10 parcial, H14). Lo demás está limpio: las afirmaciones sobre elicitation (form/URL, fechas 2025-06-18 y 2025-11-25), spec MCP 2026-07-28, ToolAnnotations, Cowork (Manual/Auto/Skip, archivos locales Desktop), SQLite (WAL, 281 TB, FTS5/bm25/tokenizers sin stemming español), W3C Web Annotation (Rec. 23-feb-2017, §4.2.4/§4.2.5/§4.2.9) y skills-sin-versionado **corresponden literalmente al kernel §1**, y el soporte del host para elicitation va siempre POR VERIFICAR.
- **(b) Etiquetas HECHO VERIFICADO con fuente** — 4 hallazgos (H1, H10, H12, H14).
- **(c) Muletilla «HECHO VERIFICADO a nivel general»** — **no existe en ninguno de los diez documentos**. Solo aparece en `docs/architecture/notes/research-v0_1/` (fuera de alcance, y allí la propia `critique.md` la prohíbe). Categoría limpia en cuanto a muletilla; 3 hallazgos por hipótesis presentadas como hechos (H5-bis/H9/H11).
- **(d) Derecho colombiano inventado** — **sin hallazgos**. No hay normas, artículos ni jurisprudencia citada; `CO/` se declara convención de carpeta, la vigencia temporal va POR VERIFICAR (boundaries §8) y el glosario declara expresamente «Este documento no afirma derecho».
- **(e) Uso de DECISIÓN APROBADA** — 3 hallazgos (H3, H4, H8).
- **(f) Refinamientos del kernel señalados** — 4 hallazgos (H6, H7, H12, H16). Los refinamientos centrales (estados de Fact, registro server-side, `proposal_content_hash`, `single_use` eliminado, `changes_since`) **sí** están señalados en ADR-003/ADR-005/glosario/slice.
- **(g) Feature de plataforma convertida en regla** — 2 hallazgos (H2, H18).

---

## Hallazgos

### H1 — [a][b] «El entorno real es Windows 11 Home» etiquetado HECHO VERIFICADO y atribuido al kernel §1
- **Archivos:** `C:\Users\HITMA\Desktop\legal-workspace\docs\architecture\adrs\ADR-002-protected-local-case-store.md` (Riesgos, primera viñeta) · `...\adrs\ADR-001-trust-boundary.md` (Riesgos, «Enforcement frente al host») · `...\boundaries.md` §6.
- **Cita:** ADR-002: «**HECHO VERIFICADO** (kernel §1): el sandbox de Bash de Claude Code no es nativo en Windows, **y el entorno real del proyecto es Windows 11 Home**». ADR-001: «el sandbox de Bash no es nativo en Windows (el entorno real es Windows 11 Home)». boundaries §6: «…**y el entorno real es Windows**».
- **Problema:** el kernel §1 verifica el sandbox, **no** el equipo ni su edición. La edición «Windows 11 Home» solo aparece en `notes/research-v0_1/critique.md` (contexto de proyecto, no hecho de plataforma con fuente). La etiqueta fuerte se extiende sobre una afirmación no verificada y ADR-002 la mis-atribuye explícitamente al kernel §1.
- **Corrección:** partir la frase. Dejar «HECHO VERIFICADO (kernel §1, fuente code.claude.com/docs — sandboxing): el sandbox de Bash no es nativo en Windows» y mover la máquina a línea aparte: «CONTEXTO/SUPUESTO: el equipo objetivo es Windows; edición y disponibilidad de cifrado de disco POR VERIFICAR». Aplicar en los tres archivos.

### H2 — [g] Una propiedad de SQLite (WAL) se convierte en regla de arquitectura («una sola máquina», «requisito de corrección»)
- **Archivos:** `...\principles.md` §12 *Local-first does not mean LLM-offline* · `...\boundaries.md` §6 *Persistencia* · `...\vertical-slice-v0.md` Preconditions #3.
- **Cita:** principles §12: «Exige que el estado canónico y la evidencia vivan localmente bajo control del Core, **en una sola máquina** — HECHO VERIFICADO (sqlite.org)… **la co-localización de todos los procesos es por tanto requisito, no preferencia**». boundaries §6: «Consecuencias directas: **la co-localización es requisito de corrección, no preferencia**». Slice: «**Un despliegue en carpeta compartida no es válido.**»
- **Problema:** contradice tres reglas del propio corpus: kernel §0 («ninguna feature… puede volverse regla del Domain»), boundaries línea 7 («**ninguna feature de… SQLite se convierte en regla del Domain**») y ADR-004 §(b)3 («que la materialización sea SQLite es **detalle de implementación de plataforma**, sustituible sin tocar el contrato»). Si se sustituye el motor, el «requisito de corrección» desaparece: no es regla del sistema, es restricción del adapter v0.
- **Corrección:** reformular la exigencia del principio en términos de dominio («el estado canónico y la evidencia viven bajo control exclusivo del Core, con custodia local») y degradar la co-localización a consecuencia del adapter: «**Detalle de plataforma:** mientras la persistencia sea SQLite en modo WAL, la co-localización de procesos es requisito de corrección **de ese adapter** (HECHO VERIFICADO, kernel §1); además el slice v0 fija una máquina como parámetro aprobado (kernel §11)». Igual en boundaries §6 y en la precondición 3 del slice («precondición del adapter v0», no «no es válido» en abstracto).

### H3 — [e] «Regla de entrada al dominio (DECISIÓN APROBADA)» sin decisión de los dueños
- **Archivos:** `...\adrs\ADR-003-epistemic-domain-model.md` (Decisión, tras «Nombres reservados») · `...\domain\glossary.md` (Nota final).
- **Cita:** «**Regla de entrada al dominio (DECISIÓN APROBADA):** una entidad entra al modelo cuando existe evidencia —del trabajo real— de que tiene lifecycle, identidad o invariantes propios».
- **Problema:** el kernel (§1–§17) **no contiene esta regla en ningún punto**. Su origen literal es una recomendación de analista: `notes/research-v0_1/analysis-dominio.md` — «**Regla propuesta:** cada entidad existe solo si tiene lifecycle o invariantes propios». Una propuesta de análisis fue promovida a decisión aprobada por los dueños, que es exactamente el tipo de elevación de estatus que este corpus existe para impedir.
- **Corrección:** cambiar la etiqueta a «**REGLA PROPUESTA en la consolidación** (origen: revisión v0.1.1 / análisis de dominio; no registrada como decisión de los dueños en el kernel)» y añadir en «Preguntas pendientes» de ADR-003: «DECISIÓN PENDIENTE (dueños) — ratificar la regla de entrada al dominio». Ajustar la Nota final del glosario en el mismo sentido.

### H4 — [e] Lista de diez «nombres reservados» presentada dentro del bloque DECISIÓN APROBADA
- **Archivos:** `...\adrs\ADR-003-epistemic-domain-model.md` §*Nombres reservados, no entidades v0* · replicada en `...\domain\glossary.md` (Nota final) y `...\vertical-slice-v0.md` (*Domain entities exercised*).
- **Cita:** «`Assertion`, `Contradiction`, `Gap`, `LegalIssue`, `Hypothesis`, `Argument`, `Ruling`, `ProceduralEvent`, `Term`, `Deadline` quedan **RESERVADOS**… ningún documento de la consolidación debe tratarlos como entidades existentes».
- **Problema:** el kernel §2 fija **solo** las trece entidades canónicas; nunca enumera reservados. La lista procede de recomendaciones de análisis (`analysis-dominio.md`: «PREMATURO… mantenerlos como nombres reservados»). Al ir bajo el encabezado «**DECISIÓN APROBADA**» de la sección Decisión, se lee como vocabulario ratificado por los dueños.
- **Corrección:** mover la subsección fuera del bloque aprobado o encabezarla «**Refinamiento de la consolidación (no ratificado por los dueños): registro de nombres reservados**». El contenido no cambia; cambia su estatus declarado.

### H5 — [e] ADR-006 afirma aprobación de los dueños («variante (b)», «regla literal aprobada») sin respaldo en el kernel
- **Archivo:** `...\adrs\ADR-006-evidence-incorporation-boundary.md` (Contexto y Decisión).
- **Cita:** «**DECISIÓN APROBADA por los dueños: se adopta la variante (b)**…» y «**Regla literal aprobada:** la información hallada en una integración externa puede **ORIENTAR**… pero no puede **FUNDAMENTAR**».
- **Problema:** el kernel —fuente normativa donde se consolidan las decisiones de los dueños y sus supersedes (§16, §17)— **no registra** esta decisión, ni el «ADR CANDIDATO 10», ni la elección entre variantes (a) y (b). Dos afirmaciones de aprobación y una cita presentada como «literal» quedan sin fuente auditable, en el único ADR cuya decisión nuclear no aparece en el kernel.
- **Corrección:** citar la fuente exacta junto a la etiqueta («prompt de consolidación, TAREA N» o «maestro §20»), o degradar a «Decisión de arquitectura de esta consolidación, **pendiente de ratificación**», y añadir la decisión al registro del kernel §16 para que quede consolidada como las demás.

### H6 — [c] Se promete una condición tipada (`OPERATION_NOT_PERMITTED`) para operaciones que, por diseño, no pueden llegar al Core
- **Archivos:** `...\vertical-slice-v0.md` (*Negative paths*, fila «Operación inexistente en la superficie»; *Test matrix* tests 4 y 9) · `...\principles.md` §15.
- **Cita:** slice, test 9: «**En v0 la operación ni siquiera existe en la superficie**… **No hay estado “verificada” que alcanzar ni camino que rechazar**» — y sin embargo, columna *Condición emitida*: «`OPERATION_NOT_PERMITTED {operation, policy_reason}`». Test 4 (modificar un Source): «**Imposible por la superficie normal:** no hay tool que lo intente», con la misma condición como resultado exigido.
- **Problema:** si la tool no existe, el fallo ocurre en el protocolo (tool desconocida) y el Core nunca la ve, luego no puede emitir una condición tipada. Además el kernel §9 define `OPERATION_NOT_PERMITTED` como «capacidad no disponible para el **principal/perfil** o vetada por **política**», y ADR-006 lo reconoce: «`OPERATION_NOT_PERMITTED` es de política, no de este caso». Se está declarando verificable en criterios de aceptación un comportamiento que la arquitectura descrita no produce.
- **Corrección:** en las tres filas, sustituir por: «Sin condición del Core: la ausencia de tool se resuelve en el protocolo; la respuesta al usuario es mensaje de producto. `OPERATION_NOT_PERMITTED` solo aplica cuando existe la capacidad y una política la veta». Si se quiere conservar el código, registrar en el kernel §9 la ampliación de su semántica como refinamiento explícito.

### H7 — [b] Conflicto `actor_type = HUMAN` vs enum canónico `HUMAN_DECISION` reproducido sin señalarlo
- **Archivos:** `...\adrs\ADR-005-human-authority.md` (contrato §2 e invariante 1) · `...\domain\glossary.md` §12 (contrato e invariante 1) · `...\vertical-slice-v0.md` (*Persisted state*, `HumanAuthorization`). Frente a: kernel §2 y su réplica en ADR-003, boundaries §4, glosario §7 y §8 («`actor_type = HUMAN_DECISION`»).
- **Cita:** ADR-005: «`actor_id, actor_type=HUMAN, actor_role`» e «invariante 1: `actor_type = HUMAN` es obligatorio».
- **Problema:** `HUMAN` **no es** un valor del enum canónico (`EXTERNAL_SOURCE | AI_DERIVATION | AI_INFERENCE | HUMAN_DECISION | SYSTEM`). El conflicto está en el propio kernel (§2 vs §5) y el kernel ordena que un redactor que detecte conflicto **lo señale y no lo resuelva por su cuenta**; ninguno de los tres documentos lo señala, y el glosario llega a usar los dos valores en secciones distintas del mismo archivo.
- **Corrección:** añadir una línea en ADR-005 §2, glosario §12 y slice: «**Conflicto a señalar (kernel §2 vs §5):** el enum canónico de `actor_type` es `HUMAN_DECISION`; §5 escribe `HUMAN`. Se documenta como discrepancia del kernel; queda a decisión de los dueños si `HUMAN` es un valor distinto o una errata».

### H8 — [f] boundaries.md presenta los campos AÑADIDOS del Artifact como esquema original
- **Archivo:** `...\boundaries.md` §3 *Application*, párrafo «Artifact Registry».
- **Cita:** «…`status: DRAFT | REGISTERED | REVIEWED | SUPERSEDED`, `stale`, `stale_reasons[]` y `supersedes_artifact_id?` (cadena simple, no DAG)».
- **Problema:** el kernel §10 exige señalar que el esquema es «el de los dueños **+ 3 campos justificados**» y marca `stale_reasons[]` y `supersedes_artifact_id?` como AÑADIDOS. El glosario §9 y el slice sí lo marcan; boundaries los enumera como contrato liso, de modo que quien lea solo este documento no distingue lo aprobado de lo añadido en consolidación.
- **Corrección:** «…`stale_reasons[]` y `supersedes_artifact_id?` (**AÑADIDOS en la consolidación**, kernel §10; justificación en glosario §9 y en el slice)».

### H9 — [f] Las unificaciones/supersedes del catálogo de condiciones no se señalan en principles.md
- **Archivo:** `...\principles.md` §9 *Uncertainty must remain visible*.
- **Cita:** «catálogo cerrado de siete condiciones v0 (`SEARCH_INCONCLUSIVE`, `ANALYSIS_STALE`, …), todas user-visible».
- **Problema:** el kernel §9 lo define como «**reducción normativa (señalar las unificaciones)**»: absorbe `PENDING_CONFIRMATION` en `HUMAN_REVIEW_REQUIRED` (§16.1), convierte `NEW_EVIDENCE_SINCE_ANALYSIS` en *reason* y degrada `NO_SUPPORT_FOUND` a dato de proyección (§16.5). El slice y el glosario lo señalan; principles presenta las siete como si fueran el catálogo originalmente aprobado.
- **Corrección:** añadir una cláusula: «catálogo cerrado de siete condiciones v0 — **reducción normativa de la consolidación (kernel §9, §16)**: absorbe `PENDING_CONFIRMATION`, convierte `NEW_EVIDENCE_SINCE_ANALYSIS` en *reason* de `ANALYSIS_STALE` y degrada `NO_SUPPORT_FOUND` a dato de proyección».

### H10 — [c] Afirmaciones sobre la conducta de los LLM presentadas como hechos establecidos
- **Archivos:** `...\adrs\ADR-001-trust-boundary.md` (Contexto) · `...\boundaries.md` §1 *External Actors* · `...\vertical-slice-v0.md` (*Conditions emitted to UX*, «Límite honesto»).
- **Cita:** ADR-001: «Un LLM es un invocador no determinista: puede ignorar instrucciones… **Ninguna de esas conductas es hipotética: son modos de operación normales de un agente**». Slice: «**no existe forma conocida de forzar a un modelo a transmitir un texto literal**».
- **Problema:** son generalizaciones empíricas sobre modelos, no listadas en el kernel §1 y sin etiqueta. En un corpus que etiqueta todo, una afirmación categórica sin marca se lee como verificada — y el argumento no necesita el hecho: le basta la premisa de robustez.
- **Corrección:** reformular como premisa declarada: «**SUPUESTO de diseño (premisa de robustez):** el sistema asume que cualquiera de esas conductas puede ocurrir; la seguridad no depende de que no ocurran». En el slice: «**SUPUESTO:** no conocemos mecanismo que garantice la transmisión literal por el modelo; POR VERIFICAR si el host permite mostrar salida de tools sin mediación».

### H11 — [c] Supuestos operativos sin datos presentados como hechos que fundamentan un rechazo de alternativa
- **Archivos:** `...\adrs\ADR-004-case-memory.md` (§(b)2 y Alternativas 4) · `...\vertical-slice-v0.md` (*Revision behavior*).
- **Cita:** «Se mantiene separado porque **las lecturas son órdenes de magnitud más frecuentes** que las mutaciones»; «**el escritor típico es un agente cuya operación dura minutos**; un lock bloquearía a la usuaria… durante todo un análisis».
- **Problema:** el propio corpus declara que el ritmo real de trabajo, el volumen y la latencia son **preguntas de negocio abiertas y SUPUESTO** (glosario §1, §10, §13). Aquí esas magnitudes se usan sin etiqueta como fundamento fáctico para rechazar el locking pesimista y para separar logs. La conclusión puede ser correcta; la presentación convierte hipótesis en dato.
- **Corrección:** anteponer «SUPUESTO (a validar con uso real; ver glosario §10, pregunta de ritmo de trabajo):» a ambas afirmaciones, dejando intacta la decisión y su condición de reapertura.

### H12 — [b] Etiquetas HECHO VERIFICADO sin fuente ni referencia al kernel
- **Archivos y cita:** `...\adrs\ADR-001-trust-boundary.md` — «deny rules y hooks, **HECHO VERIFICADO en Claude Code**» (Decisión) y «**HECHO VERIFICADO**: en Claude Code existen deny rules por herramienta/ruta y hooks bloqueantes» (Riesgos) · `...\adrs\ADR-006-...md` — «(deny rules/hooks: **HECHO VERIFICADO en Claude Code**; Cowork POR VERIFICAR)» · `...\vertical-slice-v0.md` — «**HECHO VERIFICADO**: la plataforma no versiona skills» (bloque de schema de Artifact).
- **Problema:** kernel §0 exige la etiqueta y el resto del corpus la acompaña siempre de «(kernel §1, fuente: …)». Estas cuatro instancias llevan la etiqueta fuerte sin fuente, lo que las vuelve no auditables y facilita su reutilización descontextualizada.
- **Corrección:** añadir la fuente en cada una: «(kernel §1; fuente: code.claude.com/docs — permissions, hooks)» y, para skills, «(kernel §1; fuente: code.claude.com/docs/en/skills.md)».

### H13 — [f] El renombre `recent_changes → changes_since(revision)` no se señala en principles.md ni en boundaries.md
- **Archivos:** `...\principles.md` §7 · `...\boundaries.md` §3 *Proyecciones*.
- **Cita:** «`get_case_context` con scopes `overview | facts | evidence | pending | changes_since(revision)`».
- **Problema:** el kernel §8 marca el renombre como refinamiento **a señalar**. ADR-004 y el slice lo señalan; estos dos usan el nombre nuevo como si fuera el aprobado por los dueños.
- **Corrección:** añadir tras la enumeración: «(**refinamiento señalado**, kernel §8: el scope aprobado como `recent_changes` se renombra a `changes_since(revision)` porque el delta exige punto de referencia explícito)».

### H14 — [a][b] Citas textuales y referencias a documentos que no existen en el repositorio
- **Archivos:** transversal; casos con comillas literales en `...\adrs\ADR-001-trust-boundary.md` («Claude debe ser considerado operador del sistema, no la fuente de verdad del sistema» §7; «no prohibir una operación solamente mediante un prompt» §12) y `...\adrs\ADR-002-...md` («Claude, por favor no modifiques esta carpeta» §25). Referencias a «v0.1.1 §A.5, §A.9, §B, §C.1, §C.5, §E.1, §E.5, §E.6, §E.7, §H, §J.7, §K3, ADR CANDIDATO 1/2/3/10» y a «maestro §3…§37» en los seis ADRs, boundaries y el slice.
- **Problema:** ni el prompt maestro v0.1 ni la revisión v0.1.1 existen como archivos en `docs\`; `notes\research-v0_1\` contiene otros documentos, con otra numeración. Ninguna de esas citas —varias entre comillas, presentadas como texto literal— es verificable dentro del repositorio, incluidas las que sostienen decisiones nucleares (H5).
- **Corrección:** incorporar ambos documentos fuente a `docs\architecture\notes\` (o un anexo de citas con los pasajes referenciados) y, mientras tanto, declarar al inicio de cada ADR: «Fuentes primarias fuera de este repositorio: prompt maestro v0.1 y revisión arquitectónica v0.1.1; sus citas no son auditables desde `docs/`».

### H15 — [b] Referencias cruzadas mal numeradas en el glosario (invariantes de ADR-006)
- **Archivo:** `...\domain\glossary.md` §2 *Source*.
- **Cita:** «si se altera o se borra, el Source no cambia (**ADR-006, inv. 5**)» y «Idempotencia por hash de contenido… (**ADR-006, inv. 6**)».
- **Problema:** en ADR-006, inv. 5 es «El fragmento siempre resuelve a un Source», inv. 6 «El snapshot es independiente del origen» e inv. 7 «Idempotencia por hash». Las dos referencias apuntan al invariante equivocado. En un corpus cuyo valor es la trazabilidad, una cita verificable que resuelve mal es un defecto de veracidad, no de estilo.
- **Corrección:** cambiar a «ADR-006, inv. 6» (independencia post-incorporación) y «ADR-006, inv. 7» (idempotencia).

### H16 — [f] Semántica nueva de `EXTERNAL_SOURCE` y `SYSTEM` presentada como invariante sin marcar que es precisión de la consolidación
- **Archivo:** `...\domain\glossary.md` §7 *ProvenanceRecord*, invariantes 3 y 4.
- **Cita:** «`EXTERNAL_SOURCE` corresponde a la incorporación de material y **jamás** a algo producido por IA»; «`SYSTEM` cubre mutaciones mecánicas (regeneraciones, migraciones), **nunca** juicios epistémicos».
- **Problema:** el kernel §2 enumera los valores del enum pero **no fija** su semántica ni prohibiciones. Ambas reglas son razonables y probablemente deseables, pero son adiciones de la consolidación presentadas como invariantes ya vigentes.
- **Corrección:** marcarlas: «**Precisión de la consolidación (no fijada en el kernel §2), propuesta como invariante:** …», y listarlas en «Preguntas abiertas» del glosario §7 para ratificación.

### H17 — [e] Etiqueta «DECISIÓN APROBADA EN PRINCIPIO» fuera de la taxonomía del kernel
- **Archivo:** `...\principles.md` — Anexo *Product Floor v0*.
- **Cita:** «**DECISIÓN APROBADA EN PRINCIPIO** (kernel §14)».
- **Problema:** kernel §0 fija siete etiquetas (HECHO VERIFICADO / DECISIÓN APROBADA / HIPÓTESIS / SUPUESTO / POR VERIFICAR / RIESGO / DECISIÓN PENDIENTE). «APROBADA EN PRINCIPIO» es una octava categoría inventada, con fuerza intermedia indefinida — la misma clase de problema que la muletilla «a nivel general» que la revisión anterior prohibió.
- **Corrección:** usar «**DECISIÓN APROBADA** (kernel §14)» y expresar la apertura del conjunto en prosa, como ya hace la línea siguiente («primer conjunto universal… no una lista definitiva»), sin crear etiqueta nueva.

### H18 — [g] Un MUST de la spec MCP se usa como criterio de aceptación del canal de autoridad humana
- **Archivos:** `...\adrs\ADR-005-human-authority.md` (Riesgos) · `...\vertical-slice-v0.md` (*Human review boundary*, tabla del stub; *Questions blocking implementation* #2).
- **Cita:** «**Criterio para el spike: propiedades equivalentes a los MUSTs del modo URL**»; en la tabla del stub, columna NO GARANTIZA: «Propiedades equivalentes a los MUSTs del modo URL: **ese es el criterio de salida del spike**».
- **Problema:** la vara de una garantía de arquitectura (no falsificabilidad del acto humano) queda expresada por referencia a una versión de spec de plataforma. Si la spec cambia, cambia el criterio de aceptación de una propiedad que el corpus declara independiente de transporte. Es el caso más suave de (g), pero es el único que resta.
- **Corrección:** enunciar el criterio en términos propios y citar la spec solo como precedente: «**Criterio de salida del spike (propio del sistema):** (1) consentimiento humano explícito por acto, (2) superficie de decisión no inspeccionable ni accionable por el cliente ni por el LLM, (3) vinculación al `proposal_content_hash` y a `expected_case_revision`. El modo URL de MCP (HECHO VERIFICADO, kernel §1) satisface (1) y (2) y sirve de referencia, no de definición».

---

## Nota de verificación

Los diez documentos son, en conjunto, **notablemente disciplinados** en veracidad: no hay derecho colombiano inventado, no aparece la muletilla proscrita, los siete hechos de plataforma del kernel §1 se reproducen con fidelidad literal (incluidas las fechas de spec y el matiz form/URL de elicitation), y el slice llega a señalar por su cuenta dos imprecisiones del propio contrato (la lectura de «n mutaciones == n eventos» y la discrepancia «3 campos» del Artifact). Los hallazgos H2, H3 y H5 son los únicos que afectan el **estatus declarado de una decisión o regla**, y son los tres que conviene corregir antes de que otro documento los cite como aprobados.