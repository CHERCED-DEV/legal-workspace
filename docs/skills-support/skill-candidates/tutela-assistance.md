# Candidata de Skill: tutela-assistance

## Purpose / Propósito

Documentar por qué la asistencia en tutela debe seguir siendo una composición diferida y revisada por una profesional.

## Repeatable task / Tarea repetible

Ordenar hechos, fuentes, preguntas y faltantes antes de explorar, redactar o revisar un escrito de tutela.

## Trigger / Activador

Existe una consulta de tutela con contexto suficiente para estructurar preguntas, no para decidirla.

## Do not invoke when / No usar cuando

No usar para resolver procedencia, subsidiariedad, inmediatez, perjuicio irremediable, medida provisional, término o resultado.

## Inputs / Entradas

Relato, hechos/evidencia, fecha, actuaciones, derecho alegado, fuentes y objetivo de la profesional.

## Canonical context / Contexto canónico

Solo material de caso autorizado; no confunde una conversación o URL con evidencia incorporada.

## External research / Investigación externa

Constitución, Decreto 2591, fuente oficial de la actuación y jurisprudencia por pregunta concreta, incluyendo autoridad contraria.

## Output / Salida

Matriz de preguntas, fuentes, hechos, evidencia, faltantes, riesgos y revisión humana requerida.

## Method / Método

Aplicar el [workflow de tutela](../workflows/12-tutela.md) como composición y no como checklist automática.

## Resources / Recursos

Workflow de tutela, catálogo jurisprudencial, gobierno de fuentes y marco adversarial.

## Core dependencies / Dependencias del Core

Contexto autorizado, evidencia/provenance y revisión; no hay estado oficial ni radicación V0.

## MCP dependencies / Dependencias MCP

Ninguna nueva. Búsqueda, expediente, cálculo o presentación requieren diseño posterior.

## Knowledge dependencies / Dependencias de conocimiento

Muy alta: pregunta constitucional, procedimiento, jurisprudencia, fecha, autoridad y canal.

## Temporal dependencies / Dependencias temporales

La fecha de vulneración, actuación, fuente y decisiones posteriores puede ser decisiva y debe verificarse.

## Human review boundary / Límite de revisión humana

La profesional decide estrategia, argumentos, medida, firma, presentación e impugnación; la autoridad decide el caso.

## Hard prohibitions / Prohibiciones estrictas

No afirmar procedencia, urgencia, daño irremediable, medida, cumplimiento ni resultado.

## Composition / Composición

`legal-issue-spotting` + `legal-research` + `legal-drafting` + `legal-document-review` + evidencia + gate humano.

## Example requests / Ejemplos de solicitud

“Organice las preguntas y evidencias que debo revisar antes de decidir si preparo una tutela.”

## Failure modes / Fallos previsibles

Usar una cita irrelevante, convertir informalidad en ausencia de requisitos, omitir autoridad contraria o prometer resultado.

## Evals / Evaluaciones

Preguntas críticas detectadas, fuentes oficiales, temporalidad, afirmaciones sin soporte e inyección tratada como contenido.

## Priority / Prioridad

P3.

## Recommendation / Recomendación

`DEFER`; requiere discovery, fuentes/jurisprudencia fechadas y evaluación propia antes de considerar una Skill separada.
