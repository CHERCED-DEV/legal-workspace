# Candidata de Skill: legal-opinion

## Purpose / Propósito

Preparar un concepto jurídico claro, trazable y prudente mediante composición, no como Skill separada inicial.

## Repeatable task / Tarea repetible

Ordenar pregunta, hechos, fuentes, alternativas, riesgos y recomendación para revisión profesional.

## Trigger / Activador

Una profesional pide una estructura de concepto o una revisión de su consistencia.

## Do not invoke when / No usar cuando

No usar para emitir una opinión final, certificar vigencia, aceptar riesgo crítico o reemplazar el juicio profesional.

## Inputs / Entradas

Pregunta concreta, rol, hechos/evidencia disponibles, fecha, territorio, fuentes y propósito del concepto.

## Canonical context / Contexto canónico

Solo contexto autorizado y material incorporado; no infiere hechos ni estado procesal.

## External research / Investigación externa

Investigación de fuentes oficiales y autoridad contraria conforme al gobierno de fuentes.

## Output / Salida

Esquema de concepto: pregunta, supuestos, fuentes, análisis alternativo, riesgos, faltantes y revisión requerida.

## Method / Método

Combinar issue spotting, investigación, redacción y revisión adversarial; separar fuente de conclusión.

## Resources / Recursos

[Workflow de concepto](../workflows/11-legal-opinion.md), [gobierno de fuentes](../04-source-governance.md) y [revisión adversarial](../08-adversarial-review-framework.md).

## Core dependencies / Dependencias del Core

Lectura de contexto y provenance existentes; no requiere escritura canónica.

## MCP dependencies / Dependencias MCP

Ninguna nueva en V0; la verificación de fuentes es futura y no se finge.

## Knowledge dependencies / Dependencias de conocimiento

Alta: materia, jurisdicción, rol, norma especial, procedimiento y territorio.

## Temporal dependencies / Dependencias temporales

Siempre requiere fecha relevante, vigencia, reformas y transición cuando corresponda.

## Human review boundary / Límite de revisión humana

La profesional determina la recomendación, el grado de certeza y el uso final.

## Hard prohibitions / Prohibiciones estrictas

No inventar fuente, convertir una alternativa en respuesta cierta ni presentar una sugerencia como asesoría final.

## Composition / Composición

`legal-issue-spotting` + `legal-research` + `legal-drafting` + `adversarial-review`.

## Example requests / Ejemplos de solicitud

“Estructure las preguntas y fuentes que debo revisar antes de emitir un concepto.”

## Failure modes / Fallos previsibles

Omitir derecho adverso, confundir resumen con ratio o ignorar fecha y territorio.

## Evals / Evaluaciones

Tasa de fuente oficial, trazabilidad de afirmaciones, cobertura de alternativas y abstención correcta.

## Priority / Prioridad

P2.

## Recommendation / Recomendación

`MERGE`; no crear una Skill autónoma hasta demostrar un método y evaluaciones propios.
