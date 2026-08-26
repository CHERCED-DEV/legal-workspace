# Candidata de Skill: demand-assistance

## Purpose / Propósito

Preparar o revisar una demanda mediante capacidades compuestas, no por el nombre del documento.

## Repeatable task / Tarea repetible

Ordenar pretensiones, hechos, evidencia, fuentes, anexos y preguntas de procedimiento para revisión.

## Trigger / Activador

Una profesional necesita un borrador o una revisión de demanda por materia/procedimiento identificado.

## Do not invoke when / No usar cuando

No usar para concluir competencia, caducidad, cuantía, procedencia, cautelar, plazo, firma o radicación.

## Inputs / Entradas

Rol, jurisdicción, objetivo, hechos/evidencia, documentos, fechas, fuente de acto previo y reglas conocidas.

## Canonical context / Contexto canónico

Contexto autorizado, hechos/evidencia ya incorporados y locators; no se inventa estado procesal.

## External research / Investigación externa

Código/procedimiento, ley especial, reformas, transición, fuente oficial y jurisprudencia pertinente/contraria.

## Output / Salida

Matriz de requisitos por verificar, borrador estructurado, afirmaciones sin soporte y alertas de revisión.

## Method / Método

Usar el [workflow de demanda, revisión y contestación](../workflows/19-demand-response-and-review.md) con hechos, investigación, redacción y revisión.

## Resources / Recursos

Workflow, matriz temporal, dossiers de práctica y mapas de dependencias.

## Core dependencies / Dependencias del Core

Lectura autorizada, procedencia y trazabilidad; controles de estado/canal deben ser casos de uso posteriores.

## MCP dependencies / Dependencias MCP

Ninguna nueva en V0; expediente, cálculo de términos y presentación requieren diseño posterior.

## Knowledge dependencies / Dependencias de conocimiento

Muy alta: materia, procedimiento, rol, territorio, requisitos especiales y evidencia.

## Temporal dependencies / Dependencias temporales

Fecha de hechos, actuación, régimen aplicable, reforma y transición deben verificarse.

## Human review boundary / Límite de revisión humana

La profesional decide pretensiones, estrategia, admisiones, fuente aplicable, firma y presentación.

## Hard prohibitions / Prohibiciones estrictas

No afirmar que el escrito es procedente, completo, radicable u oportuno.

## Composition / Composición

`fact-builder`/evidencia + issue spotting + investigación + redacción + revisión + gate humano.

## Example requests / Ejemplos de solicitud

“Revise qué hechos y anexos faltan antes de preparar esta demanda laboral.”

## Failure modes / Fallos previsibles

Aplicar el código equivocado, omitir transición, presentar pretensión incongruente o usar hecho sin soporte.

## Evals / Evaluaciones

Cobertura de secciones, trazabilidad, falta de anexo, régimen temporal y defectos sembrados.

## Priority / Prioridad

P2.

## Recommendation / Recomendación

`MERGE`; no crear `demand-assistance` como Skill separada.
