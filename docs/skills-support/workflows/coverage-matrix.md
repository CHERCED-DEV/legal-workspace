# Matriz de cobertura de workflows obligatorios

Esta matriz es el **Coverage Ledger** del corpus: muestra dónde se documenta cada workflow exigido, su estado de investigación y la brecha que aún impide tratarlo como comportamiento listo para producto. Tener un archivo no certifica completitud jurídica, disponibilidad en el Core ni autorización para automatizar.

## Cómo leer los estados

| Estado | Significado |
|---|---|
| `CUBIERTO_ESPECIFICO` | **Documentado en un dossier dedicado** con método, límites, salidas y evaluaciones candidatas; no significa cobertura jurídica cerrada. |
| `CUBIERTO_COMPUESTO` | **Documentado como combinación** de capacidades reutilizables; no se recomienda una Skill por tipo de documento. |
| `CUBIERTO_CON_BRECHA` | **Documentado con brecha:** hay dossier, pero faltan investigación jurídica, discovery profesional, fuentes o condiciones de plataforma para diseñar producto. |

Las reglas y fuentes por materia se complementan con [gobierno de fuentes](../04-source-governance.md), la [matriz temporal](../source-catalog/temporal-law-matrix.md) y los dossiers de práctica. Una fuente o checklist no desplaza la decisión humana ni el Core.

## Cobertura obligatoria

| Workflow obligatorio | Archivo de cobertura | Estado | Brecha abierta relevante |
|---|---|---|---|
| Apertura de caso / intake | [01 — Intake y estructuración](01-intake-structuring.md) | `CUBIERTO_COMPUESTO` | Taxonomía real de asuntos, datos mínimos y política de aceptación por la práctica. |
| Entrevista y estructuración | [01 — Intake y estructuración](01-intake-structuring.md) | `CUBIERTO_COMPUESTO` | Guiones reales, consentimiento y criterios de calidad de entrevista. |
| Construcción de hechos | [02 — Hechos y evidencia](02-fact-construction-and-evidence.md) | `CUBIERTO_COMPUESTO` | Umbrales de revisión y tratamiento por materia de la prueba. |
| Análisis de evidencia | [02 — Hechos y evidencia](02-fact-construction-and-evidence.md) | `CUBIERTO_CON_BRECHA` | Métricas de calidad, fuentes originales disponibles y reglas específicas de valoración. |
| Clasificación de documentos | [16 — Clasificación de documentos](16-document-classification.md) | `CUBIERTO_ESPECIFICO` | Taxonomía observada, calidad de OCR y criterios para enrutar a cada flujo. |
| Análisis de contradicciones | [07 — Audiencias y contradicciones](07-hearing-analysis-and-contradictions.md) | `CUBIERTO_COMPUESTO` | Umbral entre tensión semántica y contradicción formal; validación humana por materia. |
| Identificación de problemas jurídicos | [03 — Investigación y problemas](03-legal-research-and-issue-spotting.md) | `CUBIERTO_COMPUESTO` | Cobertura de áreas y forma de priorizar problemas con la profesional. |
| Investigación jurídica | [03 — Investigación y problemas](03-legal-research-and-issue-spotting.md) | `CUBIERTO_CON_BRECHA` | Retrieval, verificación de fuentes y gobernanza de jurisprudencia no están implementados en V0. |
| Redacción jurídica | [04 — Redacción y revisión](04-legal-drafting-and-document-review.md) | `CUBIERTO_COMPUESTO` | Templates y estilos reales por despacho/materia; validación de salida profesional. |
| Revisión de documentos jurídicos | [04 — Redacción y revisión](04-legal-drafting-and-document-review.md) | `CUBIERTO_COMPUESTO` | Conjuntos de defectos reales y umbrales de severidad para evaluación. |
| Demandas | [19 — Demanda, revisión y contestación](19-demand-response-and-review.md) | `CUBIERTO_CON_BRECHA` | Mapa normativo y requisitos por civil/comercial/familia, laboral y contencioso; datos del caso y transición temporal. |
| Revisión de demandas | [19 — Demanda, revisión y contestación](19-demand-response-and-review.md) | `CUBIERTO_CON_BRECHA` | Checks verificables por jurisdicción y corpus de defectos para medir recall/falsos positivos. |
| Contestación de demandas | [19 — Demanda, revisión y contestación](19-demand-response-and-review.md) | `CUBIERTO_CON_BRECHA` | Criterios profesionales para admisión, negación, “no me consta”, excepciones y teoría alternativa. |
| Memoriales y actuaciones | [05 — Actuaciones procesales](05-procedural-submissions-and-resources.md) | `CUBIERTO_COMPUESTO` | Inventario de actuaciones más usadas y requisitos fechados por procedimiento. |
| Recursos | [05 — Actuaciones procesales](05-procedural-submissions-and-resources.md) | `CUBIERTO_CON_BRECHA` | Fuente verificada de disponibilidad, oportunidad, plazo y efecto para el caso concreto. |
| Derechos de petición | [06 — Derecho de petición](06-right-to-petition.md) | `CUBIERTO_ESPECIFICO` | Modalidades/destinatarios reales y normas especiales que desplazan la regla general. |
| Respuesta a derechos de petición | [06 — Derecho de petición](06-right-to-petition.md) | `CUBIERTO_COMPUESTO` | Reserva, competencia, información de terceros y confirmación de término/canal. |
| Tutela | [12 — Tutela](12-tutela.md) | `CUBIERTO_CON_BRECHA` | Discovery de variantes de práctica y jurisprudencia relevante por problema; prioridad P3. |
| Conceptos jurídicos | [11 — Concepto jurídico](11-legal-opinion.md) | `CUBIERTO_COMPUESTO` | Criterio profesional de suficiencia, fuentes por área y forma de comunicar incertidumbre. |
| Conciliación | [15 — Conciliación y negociación](15-conciliacion-y-negociacion.md) | `CUBIERTO_CON_BRECHA` | Materias atendidas, procedibilidad y límites materiales por asunto; prioridad P3. |
| Negociación | [15 — Conciliación y negociación](15-conciliacion-y-negociacion.md) | `CUBIERTO_CON_BRECHA` | Límites éticos, autorización del cliente y método observado para ofertas/alternativas. |
| Audiencia pre | [18 — Preparación y análisis posterior de audiencia](18-pre-and-post-hearing.md) | `CUBIERTO_ESPECIFICO` | Tipos de audiencia, formatos de brief y reglas por procedimiento. |
| Audiencia post | [18 — Preparación y análisis posterior de audiencia](18-pre-and-post-hearing.md) | `CUBIERTO_ESPECIFICO` | Calidad de audio/actas, atribución de hablante y validación de órdenes/términos. |
| Policivo / querellas | [13 — Policivo y querellas](13-policivo-y-querellas.md) | `CUBIERTO_CON_BRECHA` | Normativa territorial, flujo de autoridad y separación litigante/decisor; prioridad P3. |
| Decisión / providencia | [14 — Apoyo a autoridad](14-apoyo-redaccion-decisiones-autoridad.md) | `CUBIERTO_CON_BRECHA` | Expediente oficial, permisos, políticas y discovery de rol decisor; prioridad P3. |
| Comunicación con cliente | [09 — Comunicación](09-client-communication-and-conciliation.md) | `CUBIERTO_COMPUESTO` | Tono, canales autorizados, tratamiento de datos y límites de asesoría que usa la práctica. |
| Revisión del estado del caso | [17 — Revisión del estado del caso](17-case-status-review.md) | `CUBIERTO_CON_BRECHA` | Fuente oficial de estado, conectores, cálculo de plazos y criterios de alerta; no disponibles en V0. |
| Revisión adversarial | [08 — Revisión adversarial](08-adversarial-review-and-decision-support.md) | `CUBIERTO_COMPUESTO` | Conjunto de defectos sembrados, estándar de severidad y validación de falsos positivos. |
| Revisión con rigor judicial | [20 — Rigor judicial](20-judicial-rigor-review.md) | `CUBIERTO_ESPECIFICO` | Métricas propias, límites de rol decisor y prueba de que merece una Skill separada. |

## Conteo de inventario

| Indicador | Conteo | Alcance |
|---|---:|---|
| `TOTAL_WORKFLOWS_OBLIGATORIOS` | 29 | Inventario mínimo del prompt v1. |
| `WORKFLOWS_WITH_COVERAGE_FILE` | 29 | Cada fila tiene al menos un dossier o cobertura compuesta. |
| `WORKFLOWS_WITH_GAPS` | 29 | Todas conservan al menos una brecha explícita antes de producto. |
| `WORKFLOWS_NOT_DIRECTLY_LEGAL_DEPENDENT` | 2 | Clasificación de documentos y comunicación con cliente, a nivel metodológico; su uso concreto puede activar reglas jurídicas. |

Estos conteos describen documentación de investigación. No son un porcentaje de cumplimiento legal ni prueban que haya un mapa normativo completo por workflow.

## Regla de seguimiento

Para cerrar una brecha se debe registrar: fuente oficial o evidencia de práctica revisada, fecha de verificación, alcance (jurisdicción/rol/territorio), evaluación reproducible y decisión humana de producto. Si falta alguno, el estado se mantiene `CUBIERTO_CON_BRECHA` o `CUBIERTO_COMPUESTO`, nunca “listo para automatizar”.
