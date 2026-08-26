# 02 — Matriz de frontera: documento ≠ Skill

**Regla:** la tabla clasifica responsabilidades; no autoriza capacidades ni modifica la superficie MCP V0.

| Trabajo | Skill/metodología | Core / Application | Knowledge Pack | Template / recurso | Conector | Humana / gate |
|---|---|---|---|---|---|---|
| Construir hechos | `fact-builder` | incorporar, validar EvidenceLink, Proposal, commit y staleness | — | formato de salida | transcripción/OCR futuros | revisar y decidir |
| Clasificar/contrastar evidencia | `evidence-analysis` | identidad, hashes, locators, cobertura determinista | reglas por materia solo si aplica | matriz probatoria | OCR/transcripción | decidir relevancia/peso |
| Verificar existencia de norma/sentencia | — | retrieval/identity verificable, snapshot y estado de verificación futuros | catálogo de fuentes | protocolo de consulta | web/fuente jurídica | decidir pertinencia |
| Analizar relevancia de autoridad | `legal-research` | provenance de la consulta futura | jurisdicción, fecha, jerarquía | ficha de ratio | buscador jurídico | validar lectura y conclusión |
| Redactar demanda/petición/memorial | `legal-drafting` | contexto de caso y provenance de inputs | requisitos procedimentales vigentes | plantilla de oficina y dossier | Word/export futuro | aprobar, firmar/radicar |
| Revisar una demanda | `legal-document-review` | checks deterministas y presentación de condiciones | requisitos por procedimiento | checklist de tipo documental | lector DOCX/PDF futuro | resolver juicio jurídico |
| Contestar demanda | composición | estado de caso y trazabilidad | carga/forma/procedimiento | workflow de contestación | — | estrategia y admisiones |
| Recursos | composición | estado procesal y cálculo verificable futuro | regla fechada sobre disponibilidad/término/legitimación; no verifica el estado actual | workflow de recurso | consulta de expediente | decidir si procede/firmar |
| Derecho de petición | composición | contexto, fuente y checklist determinista futuro | Constitución art. 23 / Ley 1755 y régimen aplicable | patrón de petición/respuesta | canal/radicación futuro | juicio y envío |
| Audiencia antes/después | `hearing-analysis` | Source/derivación/locators/staleness | reglas de audiencia por área | guion y matriz | transcripción | validar hablante, compromisos y estrategia |
| Contradicciones | `contradiction-analysis` | detectar igualdad/diferencia formal donde proceda | — | taxonomía de contradicciones | — | decidir si es contradicción material |
| Adversarial review | `adversarial-review` | no aplica cambios | derecho/contexto de la causa | checklist falsable | — | valorar riesgo y respuesta |
| Providencia/decisión | composición posterior | expediente, gates y log | procedimiento/rol de autoridad | patrón de motivación | expediente externo futuro | autoridad competente decide |
| Backups, permisos, actualización | — | bootstrap, policy, infraestructura | — | guía operativa | SO/disco | dueños/operador |
| Ética, confidencialidad, conflicto de interés | — | policy/product floor donde sea verificable | reglas deontológicas fechadas | checklist de intake | — | profesional y organización |

## Checks por tipo

| Tipo de check | Ejemplo | Dueño |
|---|---|---|
| Determinista | campo obligatorio, ID existente, hash, fecha que no tiene formato válido, item ajeno al Case | Core/Application |
| De fuente/identidad | la URL/identificador recupera la norma o providencia indicada | adapter/Core futuro + source registry |
| Semántico | una pretensión contradice el relato; una cita no sostiene la proposición | Skill propone hallazgo falsable |
| Jurídico/profesional | procedencia, estrategia, alcance de ratio, valoración probatoria, decisión | humana con Knowledge Pack/fuentes |

## Decisiones explícitas de no duplicación

`petition-assistance`, `demand-assistance` y `appeal-assistance` no sobreviven como Skills autónomas iniciales. Son composiciones de `legal-drafting`, `legal-document-review`, `legal-research`, `fact-builder`/`evidence-analysis`, un workflow específico, un Knowledge Pack fechado y gates humanos. Crear una Skill por nombre de documento duplicaría metodología y volvería opaco qué cambia realmente entre jurisdicciones.

## Tipos de documento: desglose v1

Un tipo de documento puede activar una composición, pero no es por sí mismo una Skill. Esta tabla desglosa los productos que suelen confundirse con capacidades independientes.

| Tipo de documento | Skill / método | Core | Knowledge Pack | Template | Conector | Revisión humana |
|---|---|---|---|---|---|---|
| Demanda | redacción + revisión + investigación | contexto autorizado; estado futuro | procedimiento, materia y fecha | formato del despacho | lector/exportador futuro | estrategia, firma y presentación |
| Contestación | composición de hechos, investigación, redacción y revisión | estado verificable futuro | carga, plazo, excepciones y materia | estructura de respuesta | consulta de expediente futura | admisiones, negaciones y estrategia |
| Derecho de petición | clasificación + investigación + redacción/revisión | contexto y trazabilidad futuros | Constitución, Ley 1755 y régimen especial | patrón de solicitud | radicación futura | destinatario, reserva, firma y envío |
| Respuesta a derecho de petición | clasificación + investigación + redacción/revisión | contexto y checklist futuro | competencia, reserva y norma sectorial | patrón de respuesta | canal institucional futuro | fondo, completitud, firma y envío |
| Recurso | composición; no decide procedencia | estado, notificación y término verificables futuros | recurso, efecto, legitimación y transición | esquema de agravios | expediente/consulta futura | procedencia, argumentos, firma y presentación |
| Tutela | composición diferida; no `tutela-assistance` inicial | contexto de caso y trazabilidad futura | Constitución, Decreto 2591 y jurisprudencia fechada | formato de escrito | canal judicial futuro | subsidiariedad, medida, firma y presentación |
| Concepto jurídico | investigación + redacción + adversarial | no hay decisión canónica V0 | derecho aplicable por materia, fecha y territorio | formato de concepto | fuentes jurídicas futuras | recomendación y grado de certeza |
| Memorial | redacción + revisión + investigación cuando aplique | estado/canal verificables futuros | actuación, término y procedimiento | plantilla de memorial | expediente/canal futuro | intención, firma y envío |
| Auto | apoyo de decisión posterior, no acto automático | expediente, permisos y auditoría futuros | competencia, procedimiento y estándar | patrón de motivación | expediente oficial futuro | autoridad competente decide |
| Providencia | apoyo de decisión posterior, no acto automático | expediente, permisos y auditoría futuros | competencia, procedimiento y precedente | patrón de motivación | expediente oficial futuro | autoridad competente decide |
| Decisión | apoyo de decisión posterior, no acto automático | expediente, permisos y auditoría futuros | norma, prueba, territorio y procedimiento | forma de la entidad | expediente oficial futuro | autoridad competente decide y firma |
| Informe de audiencia | preparación/análisis posterior de audiencia | evidencia, locators y derivación | reglas de audiencia por área | formato de informe | audio/transcripción futura | validar hablante, orden y consecuencia |

**Decisión de diseño:** ninguna fila autoriza una ejecución autónoma. La etiqueta de una futura salida debe indicar si falta evidencia, fuente, fecha, estado procesal o revisión profesional.
