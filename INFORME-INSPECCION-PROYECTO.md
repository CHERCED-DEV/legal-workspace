# Informe de inspección — Legal Workspace / Legal OS

**Fecha de inspección inicial:** 2026-08-25
**Revisión tras los cambios confirmados:** 2026-08-25
**Alcance:** todos los archivos versionados del repositorio, estructura Git, documentación, experimentos y código presente.  
**Método:** lectura de la estructura completa, títulos y contenido de los documentos rectores, estado técnico, ADRs, spikes y el único archivo de código. No se modificó ningún artefacto existente.

---

## 1. Resumen ejecutivo

Este repositorio **no contiene aún el producto implementado**. Es un corpus muy avanzado de descubrimiento, arquitectura y diseño técnico para un sistema local de apoyo al trabajo jurídico, llamado indistintamente **Legal Workspace / Legal OS**.

El propósito del producto V0 es asistir a una profesional en la gestión de expedientes y evidencia, sin conceder al modelo de IA autoridad sobre el estado oficial del caso. El diseño prioriza custodia de evidencia, trazabilidad, distinción epistemológica y autorización humana sobre automatización o investigación jurídica.

La idea central se puede resumir así:

```text
Persona / agente host / LLM (no confiables)
                 │ MCP
                 ▼
        Legal Core (frontera de confianza)
                 │
                 ▼
  estado canónico local + originales + log de auditoría
```

El V0 pretende probar un único flujo completo: crear un caso, incorporar evidencia de audio y documento, derivar una transcripción, proponer hechos con anclajes probatorios, revisarlos por una persona, consolidarlos y detectar que un análisis quedó desactualizado cuando llega evidencia nueva.

---

## 2. Inventario físico

| Métrica | Resultado |
|---|---:|
| Archivos versionados | 112 |
| Markdown | 109 |
| JavaScript | 1 |
| Fixtures de texto | 2 |
| Líneas aproximadas | 24.605 |
| Tamaño total aproximado | 3,69 MB |
| Código de producto | No presente |
| Estado de Git | Limpio, sin cambios locales |

La raíz contiene:

```text
.
├── docs/                         Diseño, arquitectura, investigación y backlog
├── experiments/                  Spikes no productivos
├── plugin/                       Skill operativo para el baseline y el futuro producto
├── .claude/scheduled_tasks.lock  Estado local ignorado por Git
├── .gitignore
├── revision-arquitectonica-legal-os.md
└── INFORME-INSPECCION-PROYECTO.md (este informe)
```

`.gitignore` solo excluye `.claude/scheduled_tasks.lock`. No hay `package.json`, `src/`, pruebas ejecutables, manifiestos de despliegue, CI/CD ni dependencias instalables: otra señal consistente con una fase de diseño preimplementación.

---

## 3. Qué producto se está diseñando

La documentación de descubrimiento describe una herramienta para que una abogada pueda trabajar con expedientes sin que la IA convierta por sí misma una inferencia en un hecho oficial.

Restricciones de producto especialmente importantes:

- La IA puede leer proyecciones, razonar y proponer, pero no escribe directamente el expediente canónico.
- Un hecho no pasa a acreditado por decisión del modelo; la decisión profesional es separada y explícita.
- Los originales de evidencia se preservan y no se editan ni borran desde el flujo ordinario.
- La evidencia incorporada formalmente se distingue de materiales vistos durante exploración.
- Cada conclusión debe poder rastrearse hasta su fuente, versión y fragmento.
- Cuando entra evidencia que puede afectar un análisis anterior, el sistema muestra la incertidumbre u obsolescencia; no la silencia.
- Los expedientes permanecen aislados entre sí.

El alcance V0 es deliberadamente estrecho: una máquina, una usuaria, un escritor lógico, casos y datos sintéticos/anonimizados, carpeta `Inbox/` como única entrada y un único skill ejercitado (`fact-builder`). No incluye conectores, investigación jurídica, redacción, multiagente, sincronización, multitenancy ni datos reales.

---

## 4. Documentación por área

### 4.1 Descubrimiento y dominio

| Ubicación | Contenido |
|---|---|
| `docs/discovery/resumen-producto-para-la-abogada.md` | Explicación funcional del producto, sus límites y las preguntas para la profesional. |
| `docs/discovery/business-questions-next.md` | Preguntas de negocio pendientes: definición de hecho acreditado, canales de evidencia, volumen, fuentes jurídicas, participantes, backups y ritmo de uso. |
| `docs/domain/glossary.md` | Glosario canónico extenso: entidades, estados, invariantes, cadena de trazabilidad y términos reservados. |

El glosario es esencial: fija diferencias que no pueden relajarse, por ejemplo entre *quién ejecutó una acción* (`Principal`) y *de dónde procede epistemológicamente la información* (`provenance_kind`).

### 4.2 Arquitectura base

| Ubicación | Contenido |
|---|---|
| `docs/architecture/principles.md` | 15 principios accepted: LLM no confiable, Core dueño del estado canónico, invariantes en código, separación de expedientes, evidencia inmutable, autorización humana, auditabilidad y otros. |
| `docs/architecture/boundaries.md` | Límites entre workspace de usuario, estado privado del Legal OS, Core, host, LLM, integraciones y planos administrativos. |
| `docs/architecture/vertical-slice-v0.md` | Contrato del único flujo que V0 debe demostrar integralmente; define scope, exclusiones, propiedades y tests negativos. |
| `docs/architecture/notes/` | Historial de consolidación, addenda, revisión crítica, verificaciones y material de investigación previo. |

### 4.3 ADRs

Hay trece ADRs. Los seis primeros son la base **Accepted**; los ADRs 007–013 están diseñados y requieren ratificación o se relacionan con decisiones pendientes.

| ADR | Decisión principal |
|---|---|
| ADR-001 | LLM y host agentic son clientes externos no confiables del Legal Core. |
| ADR-002 | Estado local protegido: separación entre workspace de usuario y estado privado del Legal OS; acceso únicamente a través del Core. |
| ADR-003 | Modelo de dominio epistémico mínimo: alegado, acreditado, evidencia, derivaciones y trazabilidad. |
| ADR-004 | Estado canónico del caso y proyecciones derivadas para memoria/contexto. |
| ADR-005 | Autoridad humana y operaciones sensibles mediante modelo de dos fases. |
| ADR-006 | Exploración no equivale a evidencia incorporada al caso. |
| ADR-007 | Persistencia V0 con SQLite/WAL, filesystem content-addressed, una máquina y escritor lógico único. |
| ADR-008 | Propuestas y autorización humana server-side por ítem, con soporte para aprobación parcial. |
| ADR-009 | Log canónico hash-chained, log operacional podable y dos contadores. |
| ADR-010 | Superficie MCP mínima y clasificación de comandos. |
| ADR-011 | Locators de evidencia basados en un subconjunto adoptado de W3C Web Annotation. |
| ADR-012 | Distribución y actualización: repositorio clonado, tres zonas físicas disjuntas y arranque que migra o no arranca. |
| ADR-013 | Respaldo y recuperación: copia local, disco externo cifrado y restauración verificada. |

`AMENDMENT-CANDIDATES.md` mantiene enmiendas que deben decidir los dueños, en lugar de introducir cambios silenciosos en ADRs aceptados.

### 4.4 Technical Design V0

`docs/technical-design/v0/` es el núcleo más completo del repositorio. El archivo `00-technical-kernel.md` establece vocabulario, contratos, precedencia documental y decisiones normativas para el resto.

| Documento | Qué especifica |
|---|---|
| `01-system-design.md` | Componentes, frontera del Core, transacciones y composición del sistema. |
| `02-domain-model.md` | Entidades, value objects, invariantes y transiciones de dominio. |
| `03-application-use-cases.md` | Casos de uso y sus transacciones. |
| `04-persistence-model.md` | Schema, constraints, migraciones, backups y adapter SQLite/filesystem. |
| `05-mcp-contract.md` | Tools MCP, contratos de entrada/salida, errores y clasificaciones. |
| `06-human-authorization.md` | Proposals, revisión humana, autorización y commit. |
| `07-provenance-and-locators.md` | Provenance de derivados y anclajes de evidencia. |
| `08-case-context-projections.md` | Memoria, proyecciones y recuperación selectiva de contexto. |
| `09-events-and-audit.md` | Case Event Log y Tool Invocation Log. |
| `10-artifact-lifecycle.md` | `FactAnalysis`, estados, staleness e impacto potencial. |
| `11-ux-condition-catalog.md` | Condiciones UX, categorías de presentación, locale y mensajes. |
| `12-testing-strategy.md` | Niveles de prueba, fixtures, tests adversariales y criterios de aceptación. |
| `13-synthetic-benchmark.md` | Caso jurídico ficticio para benchmark y evaluación repetible. |
| `14-repository-layout.md` | Layout esperado del futuro código y reglas de dependencia. |
| `15-product-floor-proposal.md` | Cinco políticas no relajables y cómo validar configuración cliente. |
| `16-open-implementation-decisions.md` | Clasificación de bloqueantes de Fase 1 y decisiones mitigadas. |
| `17-deployment-layout.md` | Materialización física de tres zonas: programa, mesa de trabajo y expediente privado. |
| `18-update-and-recovery.md` | Arranque, actualización, migración, degradación a solo lectura y recuperación. |
| `19-integraciones-y-herramientas.md` | Perímetro para conectar herramientas: explorar, incorporar y producir; incluye Word, M365 y Cowork. |

Las subcarpetas `notes-designers/` y `notes-verification/` preservan informes de diseño, controles de consistencia, análisis de drift y comprobaciones finales. Son evidencia útil de la revisión del corpus, no implementación.

### 4.5 Investigación y spikes

| Ubicación | Estado y objetivo |
|---|---|
| `docs/research/runtime-dependencies-spike-v0.md` | Investigación de runtime y dependencias, especialmente decisión de driver SQLite. |
| `docs/research/cowork-runtime-spike-v0.md` | Verificación documental de capacidades y límites de Cowork. |
| `docs/research/spike-summaries/` | Resúmenes de spikes de autorización, benchmark, Cowork, dependencias, registro y transcripción. |
| `experiments/authorization-spike/README.md` | Diseño/validación documental de transporte de autorización humana; la validación empírica aún no se ha ejecutado. |
| `experiments/transcription-spike/README.md` | Contrato del puerto de transcripción y contraste documental de proveedores; protege que los timestamps remitan al original. |
| `experiments/cowork-capability-spike/` | Protocolo manual de 31 pasos para medir límites reales de Cowork en Windows. Está `NOT_RUN`. |

El spike de Cowork sí incluye el único código JavaScript: `spike-mcp-server/server.js`. Es un servidor MCP JSON-RPC por `stdio`, sin dependencias, que expone herramientas de lectura, escritura e identidad del proceso únicamente para medir si un MCP local puede salir de las carpetas adjuntas. El propio código indica explícitamente que es **no productivo**, no valida rutas y no debe importarse desde `src/`.

También hay dos fixtures deliberadamente separados:

```text
experiments/cowork-capability-spike/experimental-root/
├── accessible/visible.txt
└── private/private.txt
```

Sirven para comprobar empíricamente la frontera de rutas. No contienen componentes del producto.

---

## 5. Estado real de madurez

La documentación está madura para iniciar implementación controlada, pero el proyecto no está listo para construir sin resolver decisiones explícitamente marcadas.

### Listo o ampliamente especificado

- Arquitectura de confianza, custodia local y separación de responsabilidades.
- Modelo epistemológico de evidencia, hechos, derivaciones y provenance.
- Flujo vertical V0 y exclusiones explícitas.
- Casos de uso, persistencia conceptual, eventos, auditoría, MCP, UX, pruebas y benchmark sintético.
- Reglas de dependencia para un futuro `src/`.
- Estrategia para trabajar de forma segura con dobles de desarrollo donde la plataforma real todavía no está confirmada.

### No existe todavía

- Directorio `src/` ni dominios implementados.
- Base de datos, migraciones y adapter SQLite reales.
- Servidor MCP de producto.
- UI/canal real de revisión humana.
- Tests automatizados o pipeline de CI.
- Paquetización, distribución, despliegue, telemetría o configuración de producción.
- Ejecución de los spikes manuales de plataforma.

### Ampliación confirmada en esta revisión

Desde la inspección inicial se añadieron **14 archivos y 5.859 líneas**, todos confirmados en la rama `master`. El proyecto ya no solo describe el Core: ahora especifica también su operación alrededor del Core.

- **Distribución y operación local.** ADR-012 y los documentos 17–18 separan físicamente tres árboles: programa versionado, mesa de trabajo visible y expediente privado. El objetivo es que una actualización o reparación con Git nunca toque datos de clientes.
- **Respaldo.** ADR-013 introduce una política concreta: estado pequeño con copia local frecuente, evidencia/originales en disco externo, retención escalonada y restauración ensayada. Git queda explícitamente descartado como mecanismo de respaldo de expedientes.
- **Uso con personas reales antes del Core.** Se añadieron protocolo de baseline, hoja de observación y rúbrica para medir el trabajo real con la abogada antes de atribuir mejoras al diseño.
- **Skill `fact-builder`.** Vive en `plugin/skills/fact-builder/` y transforma material del caso en hechos candidatos con soporte, contradicciones y ausencias de soporte. Está diseñado para proponer, nunca decidir, y puede operar sin Core (sin garantías técnicas) o posteriormente integrado con `propose_facts`.
- **Integraciones.** El documento 19 separa lo que el modelo puede explorar de lo que se incorpora formalmente al expediente y de lo que se produce para la profesional. Identifica los riesgos de prompt injection en documentos externos y las limitaciones de control/auditoría del complemento de Word.

---

## 6. Bloqueantes y riesgos prioritarios

El documento `16-open-implementation-decisions.md` clasifica cinco asuntos que bloquean la Fase 1 definida como el vertical slice V0 implementado y probado, en una sola máquina y con una usuaria sintética.

| ID | Bloqueante | Recomendación registrada |
|---|---|---|
| OD-02 | Contradicción: superficie MCP de 8 vs. 9 tools. | Ratificar 8 y enmendar ADR-001; `register_artifact` sería interno a `propose_facts`. |
| OD-03 | Elegir binding SQLite. | `better-sqlite3` detrás de `CaseStorePort`, tras verificar prebuilds para Windows/Node elegido. |
| OD-04 | Autorización humana por ítem vs. por Proposal. | Aprobar ADR-008: una autorización por ítem, agrupable por sesión de revisión. |
| OD-05 | Definir configuración efectiva `production`/`development`/`test`. | Perfil explícito, schema cerrado, sin default permisivo y validación contra Product Floor. |
| OD-11 | No bloquea el código V0, pero sí comprometer Cowork como host de producción. | Ejecutar el protocolo empírico del spike de Cowork antes o en paralelo al inicio. |

El riesgo de plataforma más severo es la pregunta B-04 del spike de Cowork: si un servidor MCP local no puede acceder al estado privado sin que el host también lo pueda leer, la forma concreta prevista para ADR-002 no es realizable en Cowork Desktop. La alternativa contemplada es ejecutar el Core como proceso independiente con sus propios permisos del sistema operativo.

Hay además decisiones mitigadas por el diseño, pero relevantes antes de un primer uso real: transporte de autorización humana, proveedor de transcripción, formato de ID, aprobación del Product Floor y ratificación de ADRs posteriores.

Los cambios nuevos añaden decisiones operativas que conviene verificar antes de instalar en una máquina real:

- Confirmar B-04: si el MCP local puede acceder al expediente privado sin exponerlo a Cowork.
- Verificar la ubicación y el formato de registro de un servidor MCP local en Cowork.
- Confirmar que la zona privada y los destinos de backup no están dentro de OneDrive, otra carpeta sincronizada ni una unidad de red.
- Verificar el mecanismo de cifrado disponible para el disco externo de respaldo en la edición real de Windows.
- Confirmar si OneDrive/Microsoft 365 es corporativo y qué plan/versiones hacen viable cualquier integración planteada.
- Verificar si un plugin puede transportar el runtime del Core, no solo skills y conectores.

---

## 7. Observaciones de mantenimiento

1. `revision-arquitectonica-legal-os.md` en la raíz y `docs/architecture/notes/revision-arquitectonica-v0_1_1.md` son idénticos byte por byte (mismo SHA-256). Es una duplicación documental; no la eliminé porque no hay una política de fuente canónica declarada.
2. Muchos documentos contienen términos como `TODO`, `POR VERIFICAR` o `PENDIENTE`. En este corpus normalmente no son deuda accidental: son marcas intencionales de incertidumbre, decisiones de dueños o experimentos no ejecutados.
3. Hay coherencia deliberada de precedencia documental: ADRs Accepted > Technical Design V0 > principios/glosario/addenda > investigación y spikes. Un cambio de producto debe actualizar el nivel correcto, no solo una nota inferior.
4. El archivo `.claude/scheduled_tasks.lock` es estado local correctamente ignorado. No parece formar parte del producto.
5. El repositorio está limpio; no detecté cambios no confirmados que deban preservarse antes de iniciar trabajo de implementación.

---

## 8. Lectura recomendada según objetivo

| Si se necesita… | Empezar por… |
|---|---|
| Entender el producto sin detalles de ingeniería | `docs/discovery/resumen-producto-para-la-abogada.md` |
| Entender las restricciones fundamentales | `docs/architecture/principles.md` y `docs/architecture/boundaries.md` |
| Implementar el V0 | `docs/technical-design/v0/00-technical-kernel.md`, `vertical-slice-v0.md`, luego `01`–`14` |
| Decidir qué impide comenzar | `docs/technical-design/v0/16-open-implementation-decisions.md` |
| Entender estado y riesgo de Cowork | `docs/technical-design/v0/ESTADO-Y-HALLAZGOS-CRITICOS.md` y `experiments/cowork-capability-spike/README.md` |
| Conocer la terminología exacta | `docs/domain/glossary.md` |
| Ver lo que se difiere conscientemente | `docs/backlog/architecture-post-v0.md` |

---

## 9. Conclusión

El proyecto es una **especificación arquitectónica, operativa y de producto muy detallada**, no una aplicación en funcionamiento. Su mayor fortaleza es la claridad sobre límites: la IA no es autoridad, la evidencia debe ser rastreable, el estado canónico debe estar fuera del alcance directo del host y el diseño no inventa garantías de plataforma no verificadas.

El siguiente paso razonable no es escribir código de forma indiscriminada: es ejecutar primero el baseline con la profesional, resolver los bloqueantes de diseño/decisión de Fase 1, comprobar el perímetro de Cowork y las condiciones de instalación/backup, y después crear el esqueleto de implementación definido por `14-repository-layout.md`, empezando por Domain, Application y sus pruebas.
