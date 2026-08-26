# Candidata de Skill: fact-builder

> Esta ficha documenta la candidata ya existente. No reescribe su `SKILL.md`, sus herramientas ni el alcance V0.

## Purpose / Propósito

Proponer hechos atómicos y relaciones con evidencia para revisión humana, sin declarar los hechos acreditados.

## Repeatable task / Tarea repetible

Separar relato, evidencia, inferencia y ausencia de soporte en una propuesta revisable.

## Trigger / Activador

Una profesional necesita estructurar hechos desde material ya incorporado al caso.

## Do not invoke when / No usar cuando

No usar para valorar definitivamente una prueba, decidir un caso, incorporar evidencia o comprometer el estado canónico.

## Inputs / Entradas

Contexto autorizado, evidencia incorporada, locators y objetivo de revisión.

## Canonical context / Contexto canónico

El Core aporta únicamente el caso autorizado, su revisión y sus identificadores; la Skill no sustituye ese contexto.

## External research / Investigación externa

No requiere investigación jurídica externa para el método básico.

## Output / Salida

Propuesta de hechos, soportes, contradicciones, faltantes y revisión requerida.

## Method / Método

Atomizar, atribuir a una fuente/localizador, marcar incertidumbre y solicitar revisión antes del commit.

## Resources / Recursos

[Workflow de hechos y evidencia](../workflows/02-fact-construction-and-evidence.md) y [fixtures](../evals/fact-builder-fixtures.md).

## Core dependencies / Dependencias del Core

Las garantías de caso, evidencia, propuesta, autorización, versión y commit pertenecen al Core.

## MCP dependencies / Dependencias MCP

Solo las herramientas V0 ya aprobadas; esta ficha no crea ninguna.

## Knowledge dependencies / Dependencias de conocimiento

Las reglas probatorias específicas pertenecen a un paquete fechado por materia, no a esta Skill.

## Temporal dependencies / Dependencias temporales

La fecha de un hecho se conserva como dato; su efecto jurídico requiere investigación por caso.

## Human review boundary / Límite de revisión humana

La profesional revisa, autoriza y decide qué se incorpora o se usa.

## Hard prohibitions / Prohibiciones estrictas

No afirmar prueba suficiente, inventar un soporte, crear evidencia ni saltar revisión/autorización.

## Composition / Composición

Puede preceder a análisis de evidencia, investigación, redacción y revisión.

## Example requests / Ejemplos de solicitud

“Organice estos documentos en hechos propuestos y señale cuál evidencia falta.”

## Failure modes / Fallos previsibles

Confundir alegación con hecho, perder el locator, omitir prueba contraria o usar material de otro caso.

## Evals / Evaluaciones

Cobertura de hechos, atribución a evidencia, contradicciones y tasa de afirmaciones sin soporte.

## Priority / Prioridad

P0.

## Recommendation / Recomendación

`KEEP` como capacidad existente; mantener su alcance V0 y no ampliarlo desde este corpus.
