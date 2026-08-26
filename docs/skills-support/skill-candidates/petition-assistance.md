# Candidata de Skill: petition-assistance

## Purpose / Propósito

Asistir una petición o su respuesta como composición segura, no como Skill documental separada.

## Repeatable task / Tarea repetible

Clasificar solicitudes, estructurar puntos, identificar información faltante y preparar un borrador revisable.

## Trigger / Activador

Se requiere preparar, revisar, responder o clasificar un derecho de petición.

## Do not invoke when / No usar cuando

No usar para decidir competencia, término, reserva, traslado, cumplimiento, firma o envío.

## Inputs / Entradas

Texto, fecha/canal, solicitante, destinatario, anexos, puntos solicitados y contexto autorizado.

## Canonical context / Contexto canónico

Solo evidencia y contexto del caso autorizados; el estado de radicación no existe en V0.

## External research / Investigación externa

Constitución, Ley 1755 y normas especiales/sectoriales fechadas, con fuentes oficiales y pasajes.

## Output / Salida

Matriz de puntos, información disponible, faltantes, competencia/traslado/reserva por verificar y borrador.

## Method / Método

Aplicar el [workflow de petición](../workflows/06-right-to-petition.md), investigación, redacción y revisión.

## Resources / Recursos

Workflow de petición, [mapa petición-transparencia-datos](../legal-dependency-maps/petition-transparency-data.md) y catálogo normativo.

## Core dependencies / Dependencias del Core

Procedencia de inputs y auditoría; no hay cálculo o registro oficial de términos en V0.

## MCP dependencies / Dependencias MCP

Ninguna nueva; consulta de canal o radicación requieren diseño posterior.

## Knowledge dependencies / Dependencias de conocimiento

Alta: modalidad, sujeto obligado, competencia, transparencia, datos, reserva y sector.

## Temporal dependencies / Dependencias temporales

Fecha de recepción, vigencia y regla especial son necesarias antes de cualquier conclusión.

## Human review boundary / Límite de revisión humana

La persona competente decide competencia, traslado, prioridad, contenido de fondo, firma y envío.

## Hard prohibitions / Prohibiciones estrictas

No afirmar que la petición es completa, oportuna, procedente, reservada o radicada.

## Composition / Composición

Clasificación documental + `legal-research` + `legal-drafting` + `legal-document-review`.

## Example requests / Ejemplos de solicitud

“Ordéneme los puntos de esta petición y señale qué debo confirmar antes de responder.”

## Failure modes / Fallos previsibles

Omitir un punto, tratar una norma general como regla sectorial o inventar término/competencia.

## Evals / Evaluaciones

Cobertura de solicitudes, detección de faltantes, fuente oficial y abstención ante reserva o plazo incierto.

## Priority / Prioridad

P2.

## Recommendation / Recomendación

`MERGE`; no crear `petition-assistance` como Skill separada.
