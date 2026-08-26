# Candidata de Skill: appeal-assistance

## Purpose / Propósito

Organizar información y argumentos para revisar un recurso, sin decidir su procedencia u oportunidad.

## Repeatable task / Tarea repetible

Comparar una decisión identificada, agravios propuestos, hechos/evidencia y fuentes aplicables.

## Trigger / Activador

Una profesional pide una matriz o borrador de recurso contra una providencia identificada.

## Do not invoke when / No usar cuando

No usar si falta la decisión, su fecha/notificación o el contexto mínimo; tampoco para calcular término o decidir recurribilidad.

## Inputs / Entradas

Providencia y locator, rol, objetivo, fechas conocidas, agravios, evidencia y fuentes ya recuperadas.

## Canonical context / Contexto canónico

Solo material autorizado. El estado dinámico del proceso y los términos verificables no están disponibles en V0.

## External research / Investigación externa

Regla de recurso, legitimación, efecto, término, transición, jurisdicción y autoridad posterior/contraria.

## Output / Salida

Matriz “dato necesario / fuente / estado / falta”, posibles agravios trazables y revisión humana requerida.

## Method / Método

Seguir el [workflow de actuaciones y recursos](../workflows/05-procedural-submissions-and-resources.md) y separar texto de procedencia.

## Resources / Recursos

Workflow, matriz temporal, catálogo normativo y dossier de práctica aplicable.

## Core dependencies / Dependencias del Core

Provenance del material y aislamiento; la verificación de estado/notificación es un caso de uso futuro.

## MCP dependencies / Dependencias MCP

No hay herramienta nueva V0; consultar expediente o presentar recurso requiere integración posterior.

## Knowledge dependencies / Dependencias de conocimiento

Alta: tipo de proceso, recurso, autoridad, norma especial y jurisprudencia relevante.

## Temporal dependencies / Dependencias temporales

La fecha de decisión/notificación, el término y las transiciones deben probarse con fuente verificable.

## Human review boundary / Límite de revisión humana

La profesional decide si recurre, cuáles agravios formula, firma y presenta.

## Hard prohibitions / Prohibiciones estrictas

No declarar recurso procedente, término vigente, efecto o presentación realizada.

## Composition / Composición

Contexto/evidencia + `legal-research` + `legal-drafting` + `legal-document-review` + decisión humana.

## Example requests / Ejemplos de solicitud

“Compare esta providencia con estos agravios y diga qué fuente o fecha falta revisar.”

## Failure modes / Fallos previsibles

Omitir la providencia atacada, confundir recurso, inventar plazo o atribuir un agravio a evidencia inexistente.

## Evals / Evaluaciones

Cobertura de datos necesarios, precisión de abstención, trazabilidad de agravios y detección de temporalidad incierta.

## Priority / Prioridad

P2.

## Recommendation / Recomendación

`MERGE`; no crear `appeal-assistance` como Skill separada.
