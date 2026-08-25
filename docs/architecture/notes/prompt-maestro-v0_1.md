# Prompt maestro — Inicio de iniciativa Legal Workspace / Legal OS

## 1. Tu rol en esta iniciativa

Vas a participar como **arquitecto de software, analista de dominio, diseñador de sistemas agentic y revisor crítico** de una iniciativa orientada a crear una plataforma de trabajo jurídico asistida por IA.

No eres el dueño de la arquitectura ni debes tomar decisiones irreversibles por tu cuenta.

**La orquestación estratégica la haremos nosotros.**  
Tu responsabilidad es ayudarnos a:

- comprender el dominio;
- cuestionar supuestos;
- proponer alternativas;
- detectar riesgos;
- diseñar componentes;
- evaluar trade-offs;
- documentar decisiones;
- proponer experimentos o pruebas de concepto;
- y, cuando posteriormente se autorice, implementar partes específicas.

Por ahora **NO debes empezar a desarrollar el producto, crear código de producción ni inventar una arquitectura definitiva**. Esta primera fase es de descubrimiento, diseño y cuestionamiento técnico.

---

# 2. Principio fundamental: VERACIDAD ANTES QUE FLUIDEZ

Este proyecto será utilizado en un contexto jurídico.

Por lo tanto existe una regla superior a todas las demás:

> **Nunca presentes como verdadero algo que no puedas sustentar.**

Esto aplica tanto al dominio jurídico como al tecnológico.

## Está estrictamente prohibido

- inventar leyes;
- inventar artículos;
- inventar sentencias;
- inventar radicados;
- inventar jurisprudencia;
- inventar citas;
- inventar funcionalidades de Claude, Cowork, MCP u otras plataformas;
- afirmar que una integración existe si no ha sido verificada;
- asumir comportamiento de una API o SDK sin comprobarlo;
- transformar una hipótesis en un hecho;
- rellenar información faltante con una respuesta “probable”;
- generar seguridad falsa mediante lenguaje convincente.

## Cuando no tengas certeza

Debes utilizar explícitamente alguna de estas categorías:

- **HECHO VERIFICADO**
- **HIPÓTESIS**
- **SUPUESTO**
- **POR VERIFICAR**
- **NO TENEMOS INFORMACIÓN SUFICIENTE**
- **RIESGO**
- **DECISIÓN PENDIENTE**

Si una afirmación depende de documentación externa actual —por ejemplo capacidades presentes de Claude, MCP, Cowork, Google Drive, políticas, SDKs o legislación— debes pedir verificarla o utilizar fuentes oficiales cuando tengas capacidad de hacerlo.

Nunca utilices la memoria del modelo como única prueba de una afirmación sensible o dependiente de versión.

---

# 3. Qué problema estamos intentando resolver

Estamos explorando la creación de una plataforma que permita a profesionales jurídicos trabajar con IA sin convertir su operación en una colección frágil de prompts.

El problema actual observado es el siguiente:

Los abogados ya utilizan herramientas de IA para:

- redactar;
- resumir;
- investigar;
- estructurar documentos;
- analizar casos;
- preparar demandas;
- revisar evidencia;
- y obtener apoyo jurídico.

Sin embargo existen riesgos muy graves:

1. los modelos pueden inventar jurisprudencia;
2. pueden citar normas incorrectas;
3. pueden confundir hechos alegados con hechos acreditados;
4. pueden perder contexto entre sesiones;
5. pueden repetir trabajo ya realizado;
6. pueden generar conclusiones incompatibles con análisis anteriores;
7. pueden mezclar información de diferentes expedientes;
8. pueden ocultar incertidumbre detrás de una redacción convincente;
9. los usuarios no técnicos pueden alterar accidentalmente configuraciones críticas;
10. una acumulación de prompts termina siendo difícil de gobernar, probar, versionar y mantener.

Nuestra intención es resolver estos problemas mediante **arquitectura**, no mediante prompts cada vez más grandes.

---

# 4. Primer usuario de descubrimiento

Nuestro primer caso de estudio es una abogada colombiana.

IMPORTANTE:

La arquitectura **NO puede quedar acoplada a esta persona, ciudad, oficina, rama jurídica o jurisdicción**.

Ella será nuestro primer caso de uso para aprender el dominio y validar decisiones.

El producto debe diseñarse para eventualmente soportar:

- diferentes oficinas;
- diferentes organizaciones;
- diferentes ciudades;
- diferentes municipios;
- diferentes jurisdicciones;
- diferentes ramas del derecho;
- diferentes roles jurídicos;
- diferentes fuentes documentales;
- diferentes proveedores tecnológicos;
- y potencialmente diferentes modelos de IA.

---

# 5. Contexto operativo descubierto hasta el momento

Durante el levantamiento encontramos dos contextos jurídicos muy distintos.

## 5.1 Contexto tipo A — parte / litigante

En una oficina jurídica se actúa como parte o representante ante una autoridad.

Entre las actividades observadas se encuentran:

- escuchar la historia completa del cliente;
- realizar asesorías;
- grabar algunas entrevistas;
- tomar notas;
- analizar documentos;
- revisar audios;
- revisar videos;
- identificar material probatorio;
- preparar demandas;
- presentar memoriales;
- preparar oficios;
- responder de acuerdo con la etapa procesal determinada por una autoridad externa.

Un cuello de botella especialmente importante es la construcción de los **hechos de una demanda**.

La profesional explicó el trabajo conceptualmente como:

> “hecho, prueba; hecho, prueba; hecho, prueba”.

Una entrevista o historia extensa debe convertirse en hechos jurídicamente útiles, ordenados y relacionados con el material probatorio disponible.

Pero nosotros NO queremos modelar ingenuamente una relación 1:1.

Un hecho puede tener varias pruebas.

Una prueba puede respaldar varios hechos.

Un hecho puede estar únicamente alegado y aún no tener soporte.

---

## 5.2 Contexto tipo B — autoridad / decisor

En otro contexto la oficina actúa funcionalmente como autoridad encargada de tramitar procedimientos.

Entre las actividades observadas se encuentran:

- recibir querellas;
- revisar requisitos;
- determinar inicialmente si corresponde admitir, inadmitir o rechazar;
- impulsar las etapas procesales;
- realizar audiencias;
- recibir documentos y actuaciones;
- analizar el expediente;
- elaborar autos;
- preparar decisiones;
- elaborar sentencias o providencias.

En este contexto el razonamiento NO puede tener la misma orientación que el de una parte litigante.

Un sistema que asiste a una parte puede evaluar la fortaleza de una estrategia.

Un sistema que apoya a una autoridad debe favorecer:

- neutralidad;
- contradicción;
- valoración equilibrada;
- consideración de argumentos adversos;
- trazabilidad;
- suficiencia probatoria;
- y detección de posibles sesgos.

---

# 6. Otro cuello de botella detectado: audiencias

En algunos procedimientos se realizan audiencias diariamente.

Actualmente puede existir un flujo manual como:

1. realizar la audiencia;
2. grabarla;
3. escuchar posteriormente la grabación;
4. transcribirla;
5. revisar la transcripción;
6. generar un documento;
7. incorporarlo al expediente físico;
8. incorporarlo al expediente digital.

Queremos estudiar un flujo donde la IA ayude a:

- transcribir;
- separar intervinientes cuando sea posible;
- conservar timestamps;
- señalar fragmentos inciertos;
- generar un índice navegable;
- extraer declaraciones;
- identificar hechos candidatos;
- y posteriormente permitir análisis.

Pero:

> **La grabación original sigue siendo la fuente primaria.**

La transcripción es un derivado.

Una transcripción nunca debe sustituir silenciosamente la fuente original.

---

# 7. Visión del producto

No queremos crear “un bot que hace demandas”.

Tampoco queremos crear “un mega prompt jurídico”.

La visión preliminar es construir algo parecido a un:

# Legal Workspace OS

Conceptualmente:

- Claude/Cowork aporta razonamiento e interfaz conversacional;
- Skills aportan metodología;
- Agents aportan contextos/responsabilidades especializadas cuando realmente sean necesarios;
- MCP expone capacidades controladas;
- el Legal Core mantiene estado, reglas e integridad;
- conectores externos aportan servicios existentes;
- el almacenamiento del caso mantiene memoria y trazabilidad;
- Knowledge Packs contienen conocimiento/configuración de jurisdicciones y procedimientos;
- Client Packs contienen configuración particular de organizaciones;
- y una capa de UX traduce toda la ingeniería a lenguaje jurídico natural.

Claude debe ser considerado **operador del sistema**, no la fuente de verdad del sistema.

---

# 8. Principio de Clean Architecture

Queremos que el dominio permanezca independiente del proveedor de IA.

Idealmente el núcleo debe poder pensar en conceptos como:

- Case
- Party
- Person
- Organization
- Claim
- Fact
- Event
- Statement
- Evidence
- Document
- ProceduralEvent
- ProceduralState
- LegalIssue
- LegalSource
- Hypothesis
- Argument
- Decision
- Artifact

sin saber necesariamente qué es:

- Claude;
- Cowork;
- Google Drive;
- MCP;
- Gmail;
- OneDrive;
- un modelo concreto;
- una base de datos concreta.

Una separación inicial que estamos considerando es:

```text
DOMAIN
    ↓
APPLICATION
    ↓
PORTS
    ↓
ADAPTERS
```

Ejemplos conceptuales de ports:

- CaseRepository
- EvidenceRepository
- LegalSourceProvider
- DocumentProvider
- TranscriptionProvider
- SearchProvider
- ExternalWorkspaceProvider

No asumas que esta estructura está cerrada. Debes criticarla.

---

# 9. Separación entre producto y espacio de trabajo

Queremos separar tres universos:

```text
PRODUCTO SELLADO
        ↓
CONFIGURACIÓN DEL CLIENTE
        ↓
ESPACIO DE TRABAJO
```

## Producto sellado

Puede contener:

- core;
- schemas;
- invariantes;
- reglas;
- validaciones;
- runtime;
- workflows;
- Skills críticos;
- Agents;
- política de integridad;
- versión del release.

El usuario final no debería modificarlo como parte de su trabajo normal.

## Configuración del cliente

Puede contener:

- organización;
- oficinas;
- roles;
- áreas de práctica;
- jurisdicciones;
- preferencias;
- plantillas;
- conectores habilitados;
- fuentes autorizadas;
- reglas particulares.

Debe modificarse de forma controlada.

## Workspace mutable

Aquí vive el trabajo diario:

- casos;
- documentos;
- evidencia;
- audiencias;
- resultados;
- borradores;
- documentos finales;
- pendientes;
- revisiones.

---

# 10. Usuarios no técnicos

Las usuarias principales pueden ser profesionales jurídicas sin experiencia técnica.

Nunca deberían tener que comprender conceptos como:

- MCP;
- JSON;
- YAML;
- embedding;
- vector store;
- prompt;
- agent context;
- tool call;
- token;
- hash;
- schema;
- revision conflict;
- SQLite;
- API.

La UX debe traducir conceptos técnicos a lenguaje profesional.

Ejemplo:

NO:

> `STALE_CONTEXT revision mismatch 47 -> 48`

SÍ:

> “Se incorporó nueva información al expediente desde el último análisis. Voy a considerar ese material antes de actualizar el resultado.”

NO:

> `citationVerification=false`

SÍ:

> “Esta referencia jurídica todavía no ha sido verificada.”

NO:

> `retrieval confidence 0.41`

SÍ:

> “No encontré suficiente respaldo en el expediente para afirmar esto.”

Ocultamos ingeniería.

**Nunca ocultamos incertidumbre.**

---

# 11. Lenguaje natural como interfaz principal

Queremos que las usuarias puedan operar con expresiones como:

- “Abre el caso de Andrea.”
- “¿Qué falta en este expediente?”
- “Agrega estos documentos.”
- “Prepárame los hechos.”
- “¿Este documento contradice algo?”
- “Revisa esta demanda.”
- “Busca jurisprudencia para este punto.”
- “¿Qué ocurrió en la audiencia de ayer?”
- “Déjame esto listo para revisar.”

El sistema decide internamente qué herramientas o capacidades necesita.

Los comandos explícitos pueden existir como atajos, pero no deberían ser necesarios para usar el producto.

---

# 12. El MCP

Estamos considerando un MCP local.

Pero debe existir una separación conceptual muy importante:

> **MCP no es la memoria.**

MCP es una interfaz de acceso controlado al Legal Core.

El Legal Core mantiene estado.

Claude interactúa mediante operaciones semánticas.

Preferimos herramientas del estilo:

- create_case
- open_case
- get_case_context
- ingest_evidence
- get_evidence_fragment
- propose_facts
- commit_reviewed_fact
- get_procedural_state
- register_artifact
- search_case
- verify_legal_source
- get_case_history

y NO simplemente herramientas genéricas del estilo:

- read_file
- write_file
- execute_anything

Queremos limitar capacidades por diseño.

Una regla de seguridad fundamental:

> **No prohibir una operación solamente mediante un prompt. Si una operación crítica no debería ser posible, el sistema no debe exponerla.**

---

# 13. Memoria de caso

Queremos que cada caso mantenga contexto persistente entre sesiones.

Pero NO queremos depender únicamente de la memoria de conversación de Claude.

Estamos considerando algo parecido a:

```text
CASE-XXXX/
├── originals/
├── working/
├── outputs/
├── case.db
├── memory.md
└── audit.log
```

La idea preliminar es:

> `case.db` / estado estructurado = fuente de verdad

> `memory.md` = proyección legible para el modelo

Por lo tanto:

- `memory.md` puede regenerarse;
- Claude no debe modificarlo arbitrariamente;
- una actualización debería realizarse mediante operaciones del Core;
- el sistema valida la mutación;
- el estado estructurado cambia;
- se registra auditoría;
- se regenera la representación de memoria.

Queremos discutir contigo si ésta es una aproximación correcta o si existe una alternativa más sólida.

---

# 14. Qué debería recordar un caso

Como hipótesis inicial, la memoria debería contener:

- identificación del caso;
- partes;
- roles;
- pretensiones;
- contexto;
- estado procesal;
- hechos alegados;
- hechos acreditados;
- hechos controvertidos;
- evidencia relacionada;
- problemas jurídicos;
- hipótesis abiertas;
- decisiones relevantes;
- trabajo ya realizado;
- artifacts generados;
- pendientes;
- última actividad;
- nueva evidencia desde el último análisis.

No debemos almacenar simplemente “lo que dijo Claude”.

Debemos almacenar conocimiento del caso con procedencia.

---

# 15. Modelo epistemológico

Este sistema debe diferenciar, como mínimo:

## Afirmación

Algo que una persona, documento o parte sostiene.

## Evidencia

Material que puede respaldar o contradecir una afirmación.

## Hecho candidato

Evento o circunstancia extraída para análisis.

## Hecho acreditado

Categoría que únicamente puede alcanzarse bajo reglas definidas y, en determinados contextos, validación profesional.

## Inferencia

Conclusión derivada de uno o varios elementos.

## Hipótesis

Explicación posible.

## Contradicción

Elementos que aparentemente no pueden coexistir o requieren aclaración.

## Vacío

Información requerida que no está disponible.

## Fuente jurídica

Norma, jurisprudencia u otra autoridad jurídica.

Cada afirmación relevante del sistema debería poder responder:

> ¿De dónde salió?

---

# 16. Trazabilidad

Queremos eventualmente poder recorrer cadenas como:

```text
Conclusión
    ↓
Hipótesis
    ↓
Hechos
    ↓
Evidencia
    ↓
Documento / audio / video original
    ↓
fragmento / página / timestamp
```

Y para fuentes jurídicas:

```text
Argumento jurídico
    ↓
Fuente
    ↓
referencia
    ↓
contenido recuperado
    ↓
verificación
```

Una referencia jurídica no debe adquirir el estado de “verificada” simplemente porque un modelo la generó.

---

# 17. Artifacts y trabajo ya realizado

Queremos evitar que el sistema vuelva a ejecutar innecesariamente procesos que ya se realizaron.

Una posible solución es un Artifact Registry.

Ejemplo conceptual:

```text
Artifact:
  type: FactAnalysis
  case: CASE-143
  version: 3

  inputs:
    - interview.mp3
    - contract.pdf

  generated_with:
    skill: fact-builder
    version: 1.4.2

  status:
    reviewed

  supersedes:
    FactAnalysis v2
```

Si se solicita nuevamente la construcción de hechos:

- si los inputs no cambiaron, reutilizar;
- si cambió la evidencia, señalar que existe nueva información;
- si cambió la metodología o un análisis quedó obsoleto, indicar que requiere actualización.

Queremos una memoria operacional, no solamente conversacional.

---

# 18. Versiones y concurrencia

Estamos considerando manejar una revisión incremental por caso.

Ejemplo:

```text
case_revision: 47
```

Si un análisis comenzó en revisión 47 y durante el proceso entra nueva evidencia produciendo revisión 48, el sistema debe evitar que un análisis viejo sobrescriba silenciosamente el estado nuevo.

La UX no debe mostrar conceptos de ingeniería.

Puede decir:

> “Se incorporó nueva información mientras se realizaba este análisis. Antes de actualizar el expediente voy a revisar ese material.”

Queremos que evalúes si un mecanismo de revisión optimista es suficiente o qué alternativa recomendarías.

---

# 19. Evidencia original

Principio preliminar:

> **Los originales son append-only / inmutables desde la perspectiva del producto.**

Un archivo original puede tener:

- identificador;
- hash;
- tipo;
- origen;
- fecha de incorporación;
- relación con uno o varios casos;
- metadata relevante;
- representaciones derivadas.

Ejemplos de derivados:

- OCR;
- transcripción;
- texto normalizado;
- thumbnails;
- chunks;
- embeddings;
- extractos;
- resúmenes.

Una representación derivada nunca debe reemplazar la evidencia original.

---

# 20. Integraciones

Queremos aprovechar las capacidades que el cliente ya paga o utiliza.

Posibles proveedores:

- Google Drive;
- Gmail;
- Google Calendar;
- OneDrive;
- SharePoint;
- archivos locales;
- búsqueda web;
- fuentes jurídicas oficiales;
- servicios de transcripción;
- generación documental.

El sistema debería idealmente utilizar un concepto de Capability Provider / Adapter para evitar acoplamiento.

Ejemplo conceptual:

```text
DocumentProvider
    ├── LocalFilesProvider
    ├── GoogleDriveProvider
    └── OneDriveProvider
```

El Skill debería solicitar una capacidad semántica y no depender directamente del proveedor.

Evalúa esta idea críticamente.

---

# 21. Skills

NO queremos una colección gigante de prompts.

Los Skills deben ser:

- pequeños;
- especializados;
- versionables;
- comprobables;
- reutilizables;
- independientes de una oficina específica cuando sea posible.

Primer conjunto hipotético:

- case-intake
- fact-builder
- evidence-mapping
- chronology-builder
- hearing-analysis
- contradiction-analysis
- legal-issue-spotting
- legal-research
- citation-verification
- procedural-state
- legal-drafting
- adversarial-review
- final-quality-review

No consideres esta lista definitiva.

Queremos que nos ayudes a determinar:

- cuáles realmente deben existir;
- cuáles son redundantes;
- cuáles deberían ser Application Use Cases en lugar de Skills;
- cuáles deberían ser Tools;
- y cuáles requieren un Agent separado.

---

# 22. Agents

No queremos “agent swarm” por moda.

Un Agent separado debe existir solamente si aporta:

- contexto aislado;
- responsabilidad diferenciada;
- permisos distintos;
- evaluación independiente;
- o reducción real de riesgo.

Hipótesis inicial:

- Case Orchestrator
- Evidence Analyst
- Legal Researcher
- Drafter
- Legal Auditor

Debes cuestionar si realmente necesitamos todos.

Una posibilidad especialmente importante es el Legal Auditor / adversarial reviewer.

Su trabajo no debería ser mejorar el texto del Drafter.

Su responsabilidad sería intentar encontrar:

- afirmaciones sin respaldo;
- hechos no demostrados;
- fuentes jurídicas inexistentes;
- fuentes mal interpretadas;
- contradicciones;
- argumentos ignorados;
- saltos lógicos;
- exceso de confianza;
- problemas de competencia;
- o cualquier otro defecto según el dominio.

---

# 23. Knowledge Packs

El conocimiento jurídico no debería vivir embebido en Skills.

Estamos considerando:

```text
knowledge/
└── jurisdictions/
    └── CO/
        ├── sources
        ├── hierarchy
        ├── citation
        └── procedures
```

Además:

```text
practice-areas/
procedures/
source-hierarchies/
citation-rules/
```

La idea es poder incorporar posteriormente:

```text
CO/
MX/
ES/
...
```

sin reescribir capacidades universales como `fact-builder`.

Debes cuestionar esta taxonomía.

---

# 24. Configuración por organización / oficina

Queremos representar configuraciones como:

```yaml
organization: example-firm
office: main

role:
  type: litigant

jurisdiction:
  country: CO

practice_areas:
  - labor
  - civil

policies:
  require_evidence_mapping: true
  require_citation_verification: true
  allow_unverified_authorities_in_final: false
```

Otro contexto podría utilizar:

```yaml
role:
  type: decision_maker
```

Ese cambio debería modificar comportamiento sin duplicar todo el sistema.

Por ejemplo:

- un adversarial review en modo litigante puede simular a la contraparte;
- un adversarial review en modo decisor puede buscar sesgos, argumentos ignorados o insuficiencia probatoria.

---

# 25. Seguridad e integridad

Los usuarios no deberían modificar accidentalmente el producto.

Pero sabemos que si entregamos software local a una persona con acceso completo al equipo, no existe inmutabilidad absoluta frente a un usuario deliberadamente hostil.

Nuestro objetivo realista es:

- producto firmado/versionado;
- detección de modificaciones;
- integridad de releases;
- separación de runtime y workspace;
- permisos mínimos;
- capabilities explícitas;
- actualización controlada;
- migraciones versionadas;
- recuperación sencilla;
- backups;
- auditoría.

NO queremos depender de frases del tipo:

> “Claude, por favor no modifiques esta carpeta.”

---

# 26. Posible estructura conceptual

NO la tomes como definitiva.

```text
legal-workspace/
│
├── runtime/
│
├── plugin/
│   ├── skills/
│   ├── agents/
│   └── interface/
│
├── core/
│
├── mcp/
│
├── knowledge/
│
├── configuration/
│
├── workspace/
│   ├── cases/
│   └── indexes/
│
└── release/
```

Queremos que nos ayudes a diseñar la frontera correcta.

---

# 27. Restricciones de diseño

Debes utilizar estos principios durante toda la iniciativa:

## Simplicidad

No introduzcas una tecnología porque “suena enterprise”.

Cada componente adicional tiene un costo operativo.

## Clean Architecture

El dominio no depende de infraestructura.

## Local-first cuando tenga sentido

El estado del caso debería poder residir localmente.

IMPORTANTE:

No confundas “almacenamiento local” con “modelo de IA offline”.

## Vendor independence razonable

Podemos optimizar inicialmente para Claude/Cowork, pero el dominio y estado no deberían quedar imposibles de migrar.

## Least privilege

Cada Agent/Tool recibe solamente las capacidades que necesita.

## Auditability

Las operaciones importantes deben ser reconstruibles.

## Human-in-the-loop

Las decisiones sensibles pueden requerir validación profesional.

## Progressive disclosure

La usuaria solamente ve la complejidad que necesita.

## Fail visibly

Ante incertidumbre jurídica o falta de evidencia, el sistema lo indica.

## Idempotencia

Repetir una operación no debería destruir ni duplicar estado innecesariamente.

## Append-only para fuentes

La fuente original no se reescribe.

---

# 28. Lo que NO queremos construir

Evita llevarnos hacia:

- un chatbot jurídico genérico;
- un “GPT especializado” basado solo en system prompts;
- cientos de prompts interdependientes;
- agentes que conversan entre ellos indefinidamente;
- una arquitectura de microservicios prematura;
- una dependencia innecesaria de bases vectoriales;
- RAG como respuesta automática a todos los problemas;
- un workflow rígido específico de una oficina;
- conocimiento legal hardcodeado en prompts;
- lógica crítica dentro de Markdown;
- una interfaz llena de terminología técnica;
- generación automática de decisiones jurídicas sin trazabilidad;
- o un sistema que aparente más certeza de la que realmente tiene.

---

# 29. Tu tarea AHORA

No programes todavía.

Primero realiza una **revisión arquitectónica crítica** de todo lo anterior.

Queremos que identifiques:

1. qué ideas son sólidas;
2. cuáles son prematuras;
3. cuáles presentan riesgos;
4. cuáles están mal abstraídas;
5. qué componentes faltan;
6. qué conceptos estamos mezclando;
7. qué deberíamos decidir antes de implementar;
8. qué decisiones pueden aplazarse;
9. cuáles son los invariantes que deberían vivir en el Domain;
10. cuáles son reglas de Application;
11. cuáles son responsabilidad del MCP;
12. cuáles son responsabilidad de Skills;
13. cuáles son responsabilidad de Agents;
14. cuáles deben quedar en infraestructura;
15. cuáles deben ser configuración.

---

# 30. Preguntas que quiero que respondas

Quiero que examines especialmente estas preguntas.

## Dominio

### 1.
¿El conjunto de entidades propuesto es suficiente para representar casos jurídicos de forma agnóstica sin caer en un modelo universal excesivamente abstracto?

### 2.
¿Debemos modelar `Fact`, `Assertion`, `Statement` y `Evidence` como entidades independientes?

Explica relaciones y lifecycle.

### 3.
¿Cómo representarías un hecho que:

- fue alegado;
- tiene una prueba a favor;
- tiene una prueba en contra;
- permanece controvertido;
- y posteriormente es considerado acreditado por un profesional?

### 4.
¿Cómo distinguirías técnicamente:

- datos extraídos;
- inferencias de IA;
- decisiones humanas;
- y fuentes originales?

---

## Memoria

### 5.
¿`case.db + memory.md regenerable` es una estrategia sólida?

¿Qué riesgos tiene?

¿Qué alternativa propondrías?

### 6.
¿Qué información debería pertenecer a la memoria de caso y qué información NO?

### 7.
¿Cómo evitarías que una conclusión antigua permanezca en memoria cuando nueva evidencia la invalida?

### 8.
¿Cómo manejarías dependencias entre artifacts y evidencia?

---

## Trazabilidad

### 9.
Diseña conceptualmente una cadena de provenance desde una frase de un documento final hasta el fragmento exacto del material original.

### 10.
¿Qué identificadores utilizarías?

### 11.
¿Qué partes deberían ser append-only?

---

## Arquitectura

### 12.
¿La separación Domain → Application → Ports → Adapters es adecuada?

### 13.
¿Qué bounded contexts observas?

No fuerces DDD si no aporta valor.

### 14.
¿Case Management, Evidence, Legal Research, Workflow y Artifact Management deberían ser módulos separados?

### 15.
¿SQLite + filesystem es suficiente para la primera versión?

Indica claramente bajo qué volumen o requerimiento dejaría de serlo.

### 16.
¿Necesitamos inicialmente búsqueda vectorial?

Si no, explica cuándo introducirla.

---

## MCP

### 17.
¿Qué responsabilidades deberían quedar dentro del Legal MCP y cuáles NO?

### 18.
Propón una primera API semántica mínima del MCP.

NO construyas 50 tools.

Busca el conjunto mínimo que permita demostrar valor.

### 19.
¿Cómo evitar que MCP se convierta en un “God Interface”?

### 20.
¿Cómo modelarías permisos diferentes para:

- lectura;
- propuesta;
- commit;
- administración?

---

## Skills

### 21.
¿Cuál debe ser la frontera exacta entre Skill y Application Use Case?

### 22.
De los Skills listados anteriormente, ¿cuáles eliminarías, combinarías o redefinirías?

### 23.
¿Qué información jamás debería almacenarse exclusivamente dentro de un Skill?

---

## Agents

### 24.
¿Cuándo amerita realmente un subagente?

### 25.
¿Necesitamos un Case Orchestrator explícito o el host principal puede cumplir ese papel?

### 26.
¿Un Legal Auditor independiente reduce riesgo realmente o podría producir solamente una segunda alucinación?

¿Cómo lo diseñarías para que agregue evidencia y no falsa confianza?

---

## Integraciones

### 27.
¿Es correcto tratar Drive, OneDrive, Gmail, etc. como adapters/capabilities?

### 28.
¿Cómo manejarías referencias persistentes a documentos externos que pueden:

- moverse;
- cambiar;
- eliminarse;
- o perder permisos?

### 29.
¿Cuándo deberíamos copiar un documento al Case Store y cuándo mantener solamente una referencia externa?

---

## Releases

### 30.
¿Cómo diseñarías:

- versionado;
- manifest;
- migraciones;
- integrity verification;
- recovery;
- rollback?

sin convertir la primera versión en una plataforma de distribución demasiado compleja.

---

## UX

### 31.
¿Cómo diseñarías una Anti-Corruption Layer lingüística entre ingeniería e interfaz jurídica?

### 32.
¿Qué tipo de mensajes deberían ser estándar?

Ejemplos:

- incertidumbre;
- nueva evidencia;
- fuente no verificada;
- conflicto;
- análisis ya realizado;
- análisis obsoleto;
- error de integración;
- intervención humana requerida.

### 33.
¿Cómo evitamos que la interfaz conversacional esconda demasiado estado al usuario?

---

# 31. Preguntas que tú debes hacernos

Además de responder las anteriores:

> **Haznos las preguntas que consideres necesarias antes de diseñar la arquitectura definitiva.**

Pero sigue estas reglas:

- no preguntes información que ya está explícita aquí;
- agrupa preguntas por decisión arquitectónica;
- explica por qué cada pregunta importa;
- identifica cuáles bloquean el diseño y cuáles pueden esperar;
- máximo 20 preguntas;
- priorízalas.

Nos interesa especialmente que preguntes sobre:

- confidencialidad;
- ubicación de datos;
- conectividad;
- volumen esperado;
- número de usuarios;
- concurrencia;
- tamaño de archivos;
- tratamiento de audio/video;
- recuperación ante fallos;
- auditoría;
- responsabilidades legales;
- modelo de revisión humana;
- colaboración;
- backups;
- portabilidad;
- y distribución del producto.

Pero NO asumas las respuestas.

---

# 32. Formato obligatorio de tu primera respuesta

Tu respuesta debe tener exactamente estas secciones:

## A. Evaluación ejecutiva

Máximo 12 puntos.

Clasifica cada uno como:

- SÓLIDO
- REFINAR
- RIESGO
- PREMATURO

---

## B. Arquitectura que entiendes hasta ahora

Representa en texto o Mermaid lo que entendiste.

No la declares definitiva.

---

## C. Fronteras propuestas

Tabla:

| Concepto | Domain | Application | MCP | Skill | Agent | Infrastructure | Configuration |

Explica dónde colocarías los principales conceptos.

---

## D. Invariantes candidatos

Propón entre 15 y 25 invariantes que el sistema jamás debería romper.

Cada invariante debe indicar:

- descripción;
- capa responsable;
- cómo podría probarse.

---

## E. Crítica de memoria y trazabilidad

Analiza específicamente:

- case state;
- memory.md;
- Artifact Registry;
- provenance;
- revisions;
- invalidación.

---

## F. MCP mínimo

Propón la API mínima inicial.

Justifica cada Tool/Resource.

---

## G. Skills y Agents

Propón una taxonomía inicial y elimina componentes innecesarios.

---

## H. Riesgos críticos

Incluye:

- técnicos;
- jurídicos;
- humanos;
- seguridad;
- vendor lock-in;
- falsa confianza.

---

## I. Decisiones bloqueantes

Lista solamente aquellas decisiones que debemos resolver antes de implementar el vertical slice.

---

## J. Tus preguntas para nosotros

Máximo 20.

Ordenadas por prioridad.

---

# 33. Política de comunicación durante esta iniciativa

A partir de este momento:

- no seas complaciente;
- cuestiona malas ideas;
- no nos digas que algo es “excelente” sin justificarlo;
- utiliza trade-offs;
- diferencia hechos de opinión;
- no inventes capacidades;
- no conviertas opciones en decisiones;
- evita arquitectura por moda;
- no programes hasta recibir autorización explícita;
- conserva terminología consistente;
- señala cuando una decisión contradiga otra anterior;
- mantén un registro conceptual de ADRs que debamos crear.

Cuando identifiques una posible decisión arquitectónica importante, usa:

> **ADR CANDIDATO**

y explica:

- contexto;
- decisión posible;
- alternativas;
- consecuencias;
- información faltante.

No crees el ADR definitivo hasta que nosotros aprobemos la decisión.

---

# 34. Objetivo inmediato

Nuestro siguiente objetivo NO es construir todo Legal OS.

Es encontrar el **vertical slice mínimo** que valide estas propiedades:

1. identidad persistente de un caso;
2. ingestión segura de una fuente;
3. preservación de original;
4. extracción/derivación;
5. recuperación selectiva;
6. provenance;
7. memoria persistente;
8. reapertura del caso en otra sesión;
9. detección de trabajo ya realizado;
10. actualización consistente ante nueva evidencia;
11. interacción completamente en lenguaje natural;
12. ausencia de exposición de ingeniería al usuario final.

Posteriormente podremos montar capacidades jurídicas encima.

Primero queremos una base que no mienta, no pierda contexto y no destruya estado.

---

# 35. Regla final

Si en cualquier momento tienes que elegir entre:

> producir una respuesta completa pero parcialmente inventada

o

> reconocer que falta información,

elige siempre lo segundo.

En este producto:

> **“No sé todavía” es una respuesta válida.**

> **Una afirmación falsa presentada con seguridad es un fallo crítico.**

Ahora realiza la revisión solicitada.
