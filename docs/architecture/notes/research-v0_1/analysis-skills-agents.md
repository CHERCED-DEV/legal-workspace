## Hallazgos

1. **La distinción Skill = metodología / Core = integridad está bien orientada pero incompleta** — REFINAR. El documento (§21) pide clasificar skills, pero no define el criterio de clasificación; sin una regla de decisión explícita, la lista de 13 se leerá como taxonomía de features y volverá a mezclar metodología con lógica crítica.

2. **La lista de 13 skills está inflada por conflación de tres cosas distintas** — REFINAR. Al menos 4 de los 13 (citation-verification, procedural-state, chronology-builder, final-quality-review) son total o mayoritariamente lógica determinista o proyecciones de estado, no metodología para el modelo. Mantenerlos como skills contradiría el propio principio de §12 ("si no debería ser posible, no se expone") y §28 ("lógica crítica dentro de Markdown").

3. **Los 5 agents hipotéticos no pasan los criterios que el propio documento fija en §22** — RIESGO. Drafter y Case Orchestrator no aportan contexto aislado, permisos distintos ni evaluación independiente; incluirlos "por simetría de roles humanos" es exactamente el agent-swarm por moda que §22 dice querer evitar.

4. **El Legal Auditor como concepto es sólido, pero su diseño ingenuo (segunda pasada del mismo modelo sobre el mismo texto) es el punto de mayor falsa confianza del sistema** — RIESGO. HIPÓTESIS con fundamento: dos pasadas del mismo modelo comparten pesos, priors y sesgos; sus errores no son estadísticamente independientes, y el error típico del generador (texto plausible pero sin soporte) es precisamente el que una lectura de plausibilidad no detecta. Sin anclaje determinista externo, el auditor produce ritual, no evidencia.

5. **El documento ya contiene el antídoto correcto sin explotarlo: propose vs commit** — SÓLIDO. La pareja `propose_facts` / `commit_reviewed_fact` (§12) es el patrón que resuelve la frontera skill/core: el skill guía la propuesta, el Core valida y commitea. Debe generalizarse a todo skill que toque estado, no solo a hechos.

6. **No existe aún un contrato de salida de skills** — PREMATURO clasificar skills sin él. Si un skill produce prosa libre, el Core no puede validar nada; si produce propuestas tipadas vía tools, la frontera se vuelve ejecutable. POR VERIFICAR: el mecanismo concreto depende del runtime elegido (Claude Code plugin, Cowork, Agent SDK), que el documento no fija.

7. **La parametrización por rol (litigante/decisor) de adversarial-review (§24) es el mejor argumento a favor de separar metodología (skill) de configuración (Client Pack)** — SÓLIDO. Un mismo skill con perspectiva inyectada por configuración evita duplicar el sistema, exactamente lo que §24 pide.

8. **El documento no dice quién ejecuta los checklists de política (`require_citation_verification`, etc.)** — REFINAR. Si esas políticas se "recuerdan" en prompts de skills, son violables; deben ser gates del Application layer evaluados en el commit/registro de artifacts.

## Respuestas

### 21. Frontera Skill vs Application Use Case

**Regla de decisión (tres preguntas, en orden):**

1. **¿El resultado correcto es computable o verificable determinísticamente por código?** → Application Use Case en el Core, expuesto (si el modelo debe invocarlo) como Tool MCP. Ejemplos: verificar una cita contra fuente autorizada, ordenar hechos fechados en cronología, evaluar `allow_unverified_authorities_in_final`, calcular qué artifacts quedaron obsoletos.
2. **¿El paso muta estado del caso o asigna un estado epistemológico (acreditado, verificada, revisado)?** → Use Case con validación de invariantes, siempre, aunque el input venga del modelo. El modelo puede *proponer*; jamás *commitear* directamente.
3. **¿El paso requiere juicio, interpretación o producción de lenguaje no formalizable (leer una entrevista y extraer hechos candidatos, detectar una contradicción semántica, redactar)?** → Skill: metodología que instruye al modelo *cómo* hacerlo, con salida obligatoriamente canalizada por tools de propuesta.

Corolario: **casi ningún "skill" de la lista es solo un skill**; la unidad real es la tríada *skill (método) + tools (capacidades de lectura/propuesta) + use case (validación/commit)*. Un Tool es la tercera categoría: capacidad nombrada con contrato tipado y permisos, ejecutada por el Core; el skill la consume, no la reimplementa.

**Prueba ácida:** si el sistema sigue siendo seguro cuando el modelo ignora por completo el texto del skill, la frontera está bien puesta. Si ignorar el skill puede corromper estado o marcar algo como verificado, hay lógica crítica en Markdown.

### 22. Depuración de los 13 skills

- **case-intake** → REDEFINIR. La creación del caso es use case (`create_case`); lo que queda de skill es la metodología de estructuración de la historia del cliente (entrevista → partes, pretensiones, hechos candidatos). Renombrar a algo como *intake-structuring*.
- **fact-builder** → MANTENER. Metodología nuclear ("hecho, prueba" de §5.1, con relación N:M). Es el arquetipo de skill legítimo: juicio interpretativo, salida vía `propose_facts`.
- **evidence-mapping** → COMBINAR con fact-builder. El vínculo hecho↔prueba es una operación del Core (relación N:M con provenance); la *sugerencia* de vínculos es parte inseparable de construir hechos. Mantenerlo aparte invita a ejecutar uno sin el otro.
- **chronology-builder** → ELIMINAR como skill. Una cronología de hechos con fecha es una proyección determinista del estado (query/use case). El residuo que sí requiere modelo —normalizar fechas ambiguas ("a mediados del año pasado")— es un paso dentro de fact-builder, no un skill autónomo.
- **hearing-analysis** → MANTENER, acotado. La transcripción es infraestructura (`TranscriptionProvider`, §6); el skill es la metodología sobre la transcripción: declaraciones, hechos candidatos, fragmentos inciertos, respetando que el audio es fuente primaria.
- **contradiction-analysis** → MANTENER con partición. Contradicciones formales (fechas incompatibles, montos que no cuadran) son detectables por el Core; el skill cubre solo la contradicción semántica, y su salida es una entidad `Contradiction` propuesta con referencias, no prosa.
- **legal-issue-spotting** → MANTENER, pero es el skill con mayor riesgo de conocimiento jurídico embebido; debe ser un método vacío de derecho sustantivo que consume Knowledge Packs (§23). Si en la práctica no puede escribirse sin derecho colombiano dentro, la frontera Knowledge Pack falló y hay que rediseñar.
- **legal-research** → MANTENER (metodología de búsqueda, evaluación de pertinencia y jerarquía de fuentes) sobre tools de búsqueda. Fuera del vertical slice.
- **citation-verification** → ELIMINAR como skill; convertir en use case `verify_legal_source`. La verificación es cotejo contra fuente autorizada: determinista o no ocurre. Un modelo "verificando" su propia cita es el fallo que §16 prohíbe. Residuo de modelo legítimo y separado: dado el contenido *ya recuperado*, evaluar si la fuente dice lo que el borrador le atribuye (interpretación); eso puede ser parte de adversarial-review. POR VERIFICAR: existencia de fuentes oficiales colombianas consultables programáticamente; si no existen, la verificación determinista se degrada a "recuperación + confirmación humana", y el diseño debe decirlo explícitamente en vez de simular verificación.
- **procedural-state** → ELIMINAR como skill. El estado procesal es dominio (`ProceduralState`) + reglas de procedimiento en Knowledge Packs + tool `get_procedural_state`. Un skill aquí garantizaría deriva entre lo que el modelo "cree" y lo que el expediente registra.
- **legal-drafting** → MANTENER, con restricción dura: solo puede citar `fact_id`/`source_id` existentes en el registro; el enforcement es del Core al registrar el artifact (rechazo o marcado de afirmaciones huérfanas), no del prompt.
- **adversarial-review** → MANTENER. Metodología genuina, parametrizada por rol vía configuración (§24). Es el skill que ejecutaría el Legal Auditor.
- **final-quality-review** → ELIMINAR como skill; partir en dos: (a) gate determinista del Core (checklist de políticas org: citas verificadas, hechos con soporte, campos obligatorios) y (b) lectura crítica, que ya es adversarial-review. Un tercer skill de "calidad" diluye responsabilidad.

**Resultado: 6 skills** (intake-structuring, fact-builder+evidence-mapping, hearing-analysis, contradiction-analysis, legal-issue-spotting, legal-research, legal-drafting, adversarial-review — 8 si no se fusiona evidence-mapping; 4 movidos a Core/configuración).

### 23. Qué jamás debe vivir solo en un Skill

- **Umbrales y políticas** (`require_citation_verification`, `allow_unverified_authorities_in_final`): Configuration, evaluadas por Application. Un skill puede *mencionarlas*; nunca ser su única implementación.
- **Conocimiento jurídico sustantivo**: jerarquía de fuentes, reglas de citación, plazos, requisitos procesales → Knowledge Packs versionados (§23 del doc).
- **Definiciones del modelo epistemológico** (§15) y transiciones de estado (candidato→acreditado): Domain. Si el skill redefine qué es "acreditado", dos skills pueden divergir silenciosamente.
- **Permisos y capacidades**: MCP/Configuración. "Este skill no debe escribir" escrito en el skill es la prohibición-por-prompt que §12 veta.
- **Identificadores, esquemas y formatos de provenance**: contrato del Core; el skill los usa, no los define.
- Regla general: **nada cuyo incumplimiento sea un fallo crítico**, porque un skill es texto que el modelo puede ignorar, malinterpretar o recibir truncado. El skill es guía de calidad; la corrección pertenece a capas ejecutables. Esto además es condición de comprobabilidad: los skills solo son "comprobables" (§21) si su salida es estructurada y el criterio de corrección vive fuera de ellos.

### 24. Cuándo amerita un subagente

Los criterios de §22 son correctos; aplicados con rigor:

- **Contexto aislado**: cuando el material contaminaría o agotaría el hilo principal (transcripciones de horas, evidencia masiva), o cuando la independencia exige *no ver* el razonamiento previo.
- **Permisos distintos**: cuando least privilege real lo exige (acceso web sí/no; escritura sí/no) y el runtime puede *imponer* superficies de tools distintas por subagente — POR VERIFICAR según plataforma; si los permisos por subagente no son técnicamente imponibles, este criterio no justifica nada.
- **Evaluación independiente**: cuando el valor depende de que el evaluador no esté anclado al proceso de producción.

Aplicado a los 5:

- **Case Orchestrator**: NO cumple ninguno. Ver respuesta 25.
- **Evidence Analyst**: cumple parcialmente (contexto aislado por volumen). En v1, con `get_evidence_fragment` y recuperación selectiva, el host basta; aplazar hasta que el volumen lo demuestre. PREMATURO en v1.
- **Legal Researcher**: cumple permisos distintos (solo él toca web/fuentes externas; el hilo principal no necesita red). Justificable, pero legal-research está fuera del vertical slice → aplazar.
- **Drafter**: NO cumple ninguno — mismo contexto, mismos permisos, ninguna independencia. Es el skill legal-drafting ejecutado por el host. Eliminar como agent.
- **Legal Auditor**: el único con justificación fuerte en v1 tardío (evaluación independiente + permisos read-only). Ver respuesta 26.

**Para el vertical slice (§34): cero subagentes.** Nada en las 12 propiedades del slice los requiere.

### 25. ¿Case Orchestrator explícito?

El host principal (Claude como operador conversacional) ya es el orquestador: interpreta lenguaje natural, decide qué tools invocar, secuencia trabajo. Un agente Orchestrator separado duplicaría ese loop, añadiría latencia y un canal agente-a-agente — la conversación indefinida entre agentes que §28 prohíbe — sin aportar aislamiento, permisos ni independencia.

Lo que sí falta no es un agente sino **autoridad de workflow en el Core**: qué operaciones son válidas dado el estado del caso (no commitear hechos sobre revisión obsoleta, no registrar artifact final si el gate de políticas falla). Esa autoridad debe ser código en Application, invocada vía MCP, de modo que el host pueda *intentar* cualquier secuencia y el Core rechace las inválidas. Orquestación flexible arriba, integridad rígida abajo. Reconsiderar un orquestador explícito solo si aparecen flujos largos desatendidos (procesamiento nocturno de audiencias) — y eso sería un scheduler, no un agente conversacional. DECISIÓN PENDIENTE solo en ese escenario.

### 26. Legal Auditor: ¿evidencia o segunda alucinación?

**El riesgo es real.** HIPÓTESIS con fundamento estructural: dos pasadas del mismo modelo no son revisores independientes; comparten pesos y sesgos, así que la probabilidad de que ambas fallen en el mismo punto es mucho mayor que el producto de sus probabilidades individuales. Peor: el modo de fallo del generador es texto *plausible* sin soporte, y una revisión de plausibilidad es ciega justamente a eso. Un auditor mal diseñado produce el daño máximo del sistema: un sello de calidad sobre contenido no verificado — la falsa confianza de §28.

**Diseño para que agregue evidencia:**

1. **Cotejo, no opinión.** La tarea del auditor no es "¿es bueno este documento?" sino "mapea cada afirmación fáctica y cada cita del borrador contra el registro del caso". Esto rompe la correlación porque la referencia externa (provenance del Core) es independiente de los pesos del modelo: el auditor con tools read-only recorre `fact_id`, `evidence_id`, `source_id`; lo que no mapea es objeción automática. Verificar-contra-registro es una tarea distinta de generar, con anclaje que la generación no tuvo.
2. **El Core primero.** Los checks deterministas (toda cita en estado verificada, todo hecho citado existe y su estado epistemológico es compatible con cómo se usa —un hecho *alegado* presentado como *acreditado* es detectable por código—, políticas org satisfechas) los ejecuta Application antes o además del auditor. El auditor nunca es la única línea de defensa; cubre solo el residuo semántico (fuente mal interpretada, argumento adverso ignorado, salto lógico).
3. **Objeciones con carga de la prueba.** Toda objeción debe citar elementos del expediente por id. Objeción sin referencia se degrada a "observación no fundada" y no puede bloquear nada — esto también filtra las alucinaciones del propio auditor, porque el Core valida que los ids citados existan.
4. **Salida falsable y tipada.** Lista de objeciones con categoría (afirmación-sin-soporte, fuente-no-verificada, contradicción-con-X, argumento-ignorado), ubicación en el borrador y referencias; nunca prosa evaluativa. Cada objeción es verificable por el Core o por la abogada. Prohibido el veredicto "aprobado": el auditor solo reporta defectos o "sin hallazgos en las categorías revisadas", y la aprobación es del gate determinista + humano.
5. **Aislamiento de contexto.** El auditor recibe borrador + estado del caso, jamás la conversación del drafter — el razonamiento del autor es un ancla que induce a validar.
6. **Auditor auditable.** Sembrar defectos conocidos en borradores de prueba y medir tasa de detección por categoría; un auditor cuyo recall no se mide es teatro. Esto es además el mecanismo para decidir con datos si aporta.
7. **Opcional futuro**: auditar con un modelo de otra familia (la independencia del dominio respecto del proveedor, §8, lo permite) — reduce correlación real. POR VERIFICAR costo y viabilidad; no para v1.

Con 1–4, el auditor agrega evidencia aunque comparta modelo, porque la mayor parte de su valor proviene del cotejo contra un registro que no alucina. Sin ellos, NO debería existir.

## Invariantes candidatos

1. **Ninguna salida de skill muta estado del caso directamente; todo cambio pasa por un use case que valida invariantes.** Capa: Application + MCP (superficie de tools). Prueba: test de integración — no existe tool de escritura arbitraria; intentos de commit inválido son rechazados.
2. **El estado "verificada" de una fuente jurídica solo lo asigna el Core tras cotejo con fuente autorizada configurada; ningún texto de skill/agente puede otorgarlo.** Capa: Domain (estado) + Application (transición). Prueba: unit test de la máquina de estados; revisión de que ninguna tool expone escritura directa de ese campo.
3. **Un artifact final no se registra como tal si el gate de políticas de la organización falla.** Capa: Application, con políticas en Configuration. Prueba: test con `allow_unverified_authorities_in_final: false` y una cita no verificada → rechazo.
4. **Ningún skill contiene valores de política, umbrales ni conocimiento jurisdiccional; los resuelve por referencia a Configuration/Knowledge Packs.** Capa: Configuración + proceso de release. Prueba: lint estático de skills en CI (lista de patrones prohibidos: nombres de normas, números, umbrales).
5. **Toda objeción del Legal Auditor referencia ids existentes del expediente o queda marcada como no fundada e incapaz de bloquear.** Capa: Application (validación de la salida del auditor). Prueba: unit test del validador con objeciones sin referencias.
6. **El contexto de un subagente evaluador se construye solo desde el estado del caso, nunca desde la conversación del productor.** Capa: Infraestructura (construcción del payload de spawn). Prueba: inspección del payload en tests de integración.
7. **La superficie de tools de cada agente es un subconjunto declarado en configuración sellada: auditor read-only + registro de revisión; drafter sin commit de hechos.** Capa: MCP. Prueba: tests de autorización por perfil.
8. **Re-invocar un skill con inputs sin cambios reutiliza el artifact del registry en lugar de regenerar.** Capa: Application (Artifact Registry). Prueba: test de idempotencia con hash de inputs.
9. **Todo artifact registra skill y versión con que fue generado; un cambio de versión de skill marca los artifacts dependientes como potencialmente obsoletos, nunca los reescribe.** Capa: Application. Prueba: test de invalidación al subir versión.

## ADR candidatos

1. **Regla de frontera Skill/UseCase/Tool.** Contexto: 13 skills mezclan metodología y lógica crítica. Decisión posible: la regla de tres preguntas de la respuesta 21, con la tríada skill+tools+use case como unidad. Alternativas: skills "gordos" autocontenidos (más simples de escribir, imposibles de garantizar); todo como use cases (pierde la flexibilidad interpretativa del modelo). Consecuencias: reduce la lista a 6–8 skills; exige contrato de salida estructurada. Información faltante: mecanismo de salida estructurada del runtime elegido (POR VERIFICAR).
2. **Sin Case Orchestrator ni Drafter como agentes; el host orquesta y el Core impone workflow.** Alternativas: orquestador explícito (más control aparente, duplica el loop, riesgo de agent-chatter). Consecuencias: menos piezas; la autoridad de secuencia vive en Application. Información faltante: si aparecerán flujos desatendidos largos que pidan un scheduler.
3. **Legal Auditor como subagente con diseño de cotejo (respuesta 26), fuera del vertical slice.** Alternativas: auditoría como skill en el host (pierde aislamiento); auditoría con modelo distinto (menos correlación, más costo — POR VERIFICAR). Consecuencias: requiere perfiles de permisos por agente en MCP y validador de objeciones en el Core. Información faltante: capacidad real del runtime para imponer superficies de tools distintas por subagente (POR VERIFICAR).
4. **`verify_legal_source` como use case determinista, no skill.** Contexto: la verificación no puede depender del modelo. Alternativas: verificación asistida (recuperación + confirmación humana) si no hay fuentes programáticas. Consecuencias: define el backend de la política `require_citation_verification`. Información faltante: NO TENEMOS INFORMACIÓN SUFICIENTE sobre APIs/acceso estable a fuentes oficiales colombianas — condiciona todo el diseño de esta pieza.
5. **Versionado de skills acoplado al Artifact Registry** (skill version como input del hash de reuse/invalidación). Alternativas: versionar solo el release completo (más simple, invalidación gruesa). Consecuencias: invalidación fina pero más metadatos. Información faltante: granularidad de release deseada.

## Decisiones bloqueantes

1. **Runtime objetivo de v1** (Claude Code + plugin, Cowork, Agent SDK propio). Bloquea porque define qué es técnicamente un skill, si existen subagentes con permisos imponibles y cómo se estructura la salida hacia tools. Sin esto, la clasificación skill/agent es papel. POR VERIFICAR capacidades concretas de cada opción antes de decidir.
2. **Contrato de salida skill→Core** (propuestas tipadas vía tools de propuesta, patrón propose/commit generalizado). Bloquea el slice: las propiedades 4 (extracción/derivación), 6 (provenance) y 9 (detección de trabajo realizado) del §34 dependen de que la salida del modelo sea capturable y validable, no prosa.
3. **Declaración explícita de que el slice lleva cero subagentes y qué skill mínimo incluye** (probablemente solo intake-structuring o un fact-builder reducido). Bloquea porque evita construir infraestructura de agentes que el slice no ejercita.
4. **Modelo mínimo de permisos por perfil de ejecución** (aunque solo exista el host en el slice: lectura/propuesta/commit ya aparecen en la pregunta 20 del doc). Bloquea porque la superficie MCP del slice debe nacer con esa distinción; retrofitearla después toca todos los tools.

No bloquean: diseño fino del Legal Auditor, Legal Researcher, política multi-modelo para auditoría, fusión definitiva evidence-mapping/fact-builder.

## Preguntas para los dueños

1. **¿Cuál es el runtime concreto previsto para v1 y está dispuesto el equipo a verificar sus capacidades de subagentes/permisos antes de fijar la taxonomía de agents?** Importa porque toda la frontera skill/agent depende de qué puede *imponerse* técnicamente, no de la intención. BLOQUEA.
2. **¿Existe alguna fuente jurídica oficial colombiana con acceso programático estable que el cliente use o pueda usar?** Importa porque decide si `citation-verification` puede ser determinista o debe rediseñarse como verificación asistida por humano; afecta la política `require_citation_verification`. BLOQUEA el diseño de esa pieza (no el slice, que no incluye research).
3. **¿La revisión humana previa a cualquier documento final es política dura del producto o configurable por organización?** Importa porque determina si el gate final es invariante de Domain o política de Configuration, y qué rol juega el auditor (filtro previo a humano vs sustituto parcial). Puede esperar al slice, bloquea el diseño de drafting/auditoría.
4. **¿Los modos litigante y decisor pueden coexistir en la misma instalación (y hasta en el mismo caso), o son despliegues separados?** Importa para decidir si la parametrización de adversarial-review y los permisos se resuelven por configuración por caso o por instalación. Puede esperar.
5. **¿Qué presupuesto de latencia y costo por operación se considera aceptable para pasadas adicionales (auditoría, subagentes con contexto aislado)?** Importa porque el diseño del auditor multiplica tokens y tiempo; sin presupuesto, el riesgo es diseñar una auditoría que nadie ejecuta en la práctica. Puede esperar.