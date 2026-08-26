# Dossier de práctica — Laboral y seguridad social (Colombia)

**Estado de cobertura:** `PARTIALLY_COVERED`; riesgo temporal `ALTO`.
**Fecha de referencia:** 2026-08-25. **Propósito:** orientar investigación y diseño de asistencia; no decide régimen, vínculo, liquidación, término ni resultado.

## Alcance

Este dossier cubre trabajo laboral y de seguridad social que requiera intake, hechos, evidencia, investigación, redacción, revisión, audiencias, contradicciones o análisis de régimen temporal. Distingue el procedimiento de las reglas materiales. No se puede usar “la ley vigente hoy” como sustituto de la fecha de inicio del proceso, los hechos relevantes o la versión aplicable.

## Workflows observados

- [Intake y estructura inicial](../workflows/01-intake-structuring.md), para levantar roles, fechas, documentos y preguntas pendientes.
- [Hechos y evidencia](../workflows/02-fact-construction-and-evidence.md), con soporte de fecha y hora de presentación o inicio cuando sea relevante.
- [Investigación y problemas jurídicos](../workflows/03-legal-research-and-issue-spotting.md), incluyendo versión normativa y derecho contrario.
- [Redacción y revisión](../workflows/04-legal-drafting-and-document-review.md), [actuaciones procesales](../workflows/05-procedural-submissions-and-resources.md) y [concepto jurídico](../workflows/11-legal-opinion.md).
- [Audiencias y contradicciones](../workflows/07-hearing-analysis-and-contradictions.md) y [revisión adversarial](../workflows/08-adversarial-review-and-decision-support.md).

## Documentos comunes

Pueden aparecer demanda, contestación, memorial, recurso, certificado, contrato o documento de relación, desprendible o soporte de pago, historia de aportes, liquidación propuesta, prueba documental, acta, providencia y constancia de radicación. Su existencia no autoriza al modelo a calcular valores, afirmar procedencia ni concluir que la prueba acredita un hecho.

## Skills transversales

| Necesidad | Candidata transversal | Límite |
|---|---|---|
| Ordenar información y fechas | `intake-structuring` | No selecciona el régimen aplicable. |
| Evidencia y trazabilidad | `fact-builder` y `evidence-analysis` | No determina relación laboral ni cuantía. |
| Preguntas y fuentes | `legal-issue-spotting` y `legal-research` | No convierte una fecha aislada en conclusión jurídica. |
| Texto de trabajo | `legal-drafting` y `legal-document-review` | No radica ni certifica requisitos. |
| Revisión de tensiones | `contradiction-analysis`, `hearing-analysis` y `adversarial-review` | Hallazgos revisables, no valoración probatoria. |

## Skills especiales si hay

**No se propone una Skill “laboral” separada.** La necesidad especial confirmada es una prueba temporal fuerte para la composición de investigación, redacción y revisión. Un eventual cálculo verificable de régimen, plazo o liquidación pertenece a Core/Application o a una capacidad posterior diseñada y validada, no a una instrucción de Skill.

## Necesidades del Core / Application

- Preservar la Evidence y el locator de la fecha/hora que se utilice para analizar transición.
- Mantener separados hechos, alegaciones, inferencias, fuente normativa y decisión humana sobre el régimen.
- No usar la fecha de consulta del sistema como fecha de inicio del proceso.
- No calcular de forma implícita término, liquidación, aportes o estado procesal; una capacidad de ese tipo necesita diseño, datos confiables y control profesional.

## Dependencias de Knowledge Pack

El pack debe declarar procedimiento, fecha de presentación o inicio `POR_VERIFICAR`, fecha de hechos, texto y versión de la norma, transición, materia laboral o de seguridad social, canal, autoridad y fuentes jurisprudenciales relevantes. Debe mostrar la incertidumbre si el soporte de fecha es incompleto o contradictorio.

## Fuentes oficiales

| Uso de investigación | Fuente inicial | Estado y límite |
|---|---|---|
| Régimen anterior | [Decreto Ley 2158 de 1948 — Función Pública](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=5259) | `FUENTE_OFICIAL_VERIFICADA`; no aplicarlo por defecto a demanda nueva. |
| Nuevo régimen procesal | [Ley 2452 de 2025 — SUIN](https://www.suin-juriscol.gov.co/viewDocument.asp?ruta=Leyes%2F30054744) y [Función Pública](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=259639) | Confirmar artículo, fecha y transición. |
| Control de pertinencia jurisprudencial | [J-CC-T200-2026](../source-catalog/jurisprudence-sources.md) | Identificada y descartada como soporte de la transición de Ley 2452: trata una controversia pensional, no esa transición procesal. |
| Regla material si el problema la exige | [Ley 2466 de 2025 — SUIN](https://www.suin-juriscol.gov.co/viewDocument.asp?ruta=Leyes%2F30055086) y [Función Pública](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=260676) | No aplicar sin vínculo, fecha, sector y condición normativa pertinentes. |
| Jurisprudencia | [Corte Suprema de Justicia](https://cortesuprema.gov.co/corte/index.php/jurisprudencia/) y [Relatoría Rama Judicial](https://jurisprudencia.ramajudicial.gov.co/WebRelatoria/consulta/index.xhtml) | Registrar autoridad, pasaje y derecho contrario. |

Consultar la [matriz temporal](../source-catalog/temporal-law-matrix.md) antes de formular una regla y el [catálogo oficial](../source-catalog/colombia-official-sources.md) para los límites de consulta.

## Riesgos temporales

- La matriz identifica que la Ley 2452 de 2025 entra en vigor el 2026-04-02 y que su artículo 330 conserva el régimen anterior para procesos iniciados antes de esa fecha. El Case debe conservar el soporte de la fecha/hora y una profesional debe verificar el pasaje y su aplicación.
- La Ley 2466 de 2025 tiene reglas de vigencia diferida identificadas en la matriz; no se debe calcular un efecto material sin fecha, norma y condición aplicable.
- Una reforma procesal, un hecho de ejecución continuada o una fuente posterior pueden requerir `TRANSICION_POR_VERIFICAR`.
- La fecha de consulta, por sí sola, no resuelve cuál norma aplica al Case.

## Autoridades jurisprudenciales

La investigación empieza en la [Corte Suprema de Justicia](https://cortesuprema.gov.co/corte/index.php/jurisprudencia/) y, cuando corresponda, en la [Relatoría de Rama Judicial](https://jurisprudencia.ramajudicial.gov.co/WebRelatoria/consulta/index.xhtml). [J-CC-T200-2026](../source-catalog/jurisprudence-sources.md) queda documentada solo como control de pertinencia negativa, no como fuente de la transición procesal. Una providencia solo puede pasar de `JURISPRUDENCIA_POR_VERIFICAR` tras comprobar identidad, texto, pasaje, hechos, alcance y autoridad contraria.

## Dependencias territoriales

Despacho, competencia territorial, canal, entidad o administradora involucrada y práctica de expediente son `REQUIRES_TERRITORIAL_RESEARCH`. No se deben derivar automáticamente de una ciudad, correo o nombre de archivo.

## Decisiones exclusivamente humanas

La profesional decide la caracterización del vínculo, la lectura del régimen temporal, estrategia, selección de fuentes, pertinencia y valoración de evidencia, cálculos a presentar, firma y radicación. La autoridad competente decide competencia, admisión, valoración de prueba, términos, providencias y resultado.

## Gaps y preguntas abiertas

- `GAP`: asuntos laborales y de seguridad social que atiende la práctica, volumen y secuencia real de documentos.
- `GAP`: evidencia mínima aceptada para fecha/hora de presentación o inicio y protocolo ante conflicto de fechas.
- `GAP`: controles humanos requeridos antes de usar una liquidación propuesta o una fuente jurisprudencial.
- `GAP`: si un cálculo determinista futuro es útil, qué datos verificables, fuentes y validaciones necesita fuera de una Skill.
