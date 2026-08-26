# Candidata de Skill: client-communication

## Purpose / Propósito

Traducir información autorizada a una comunicación comprensible para la persona cliente, sin alterar su significado.

## Repeatable task / Tarea repetible

Explicar estado disponible, próximos pasos, documentos faltantes y decisiones pendientes con tono definido.

## Trigger / Activador

La profesional necesita un borrador de correo, mensaje o resumen para revisar antes de enviarlo.

## Do not invoke when / No usar cuando

No usar para enviar mensajes, revelar información no autorizada, confirmar un estado procesal ni asumir compromisos.

## Inputs / Entradas

Información autorizada, destinatario, objetivo, canal, idioma/tono y restricciones de confidencialidad.

## Canonical context / Contexto canónico

Solo el mínimo contexto autorizado; un resumen de carpeta no es estado canónico del proceso.

## External research / Investigación externa

No para el estilo. Si transmite una regla jurídica, se remite a investigación fechada y revisión humana.

## Output / Salida

Borrador claro con hechos indicados como confirmados o pendientes, próximos pasos y preguntas para la profesional.

## Method / Método

Reducir jerga, separar hechos de expectativas y conservar alertas de incertidumbre.

## Resources / Recursos

[Workflow de comunicación](../workflows/09-client-communication-and-conciliation.md) y patrón de confidencialidad.

## Core dependencies / Dependencias del Core

Lectura autorizada de información; canales externos y controles de revelación son posteriores.

## MCP dependencies / Dependencias MCP

No hay dependencia nueva V0 ni autorización de envío.

## Knowledge dependencies / Dependencias de conocimiento

Datos, secreto profesional, política de comunicación y materia si se explican efectos jurídicos.

## Temporal dependencies / Dependencias temporales

Un plazo o estado comunicado debe tener fuente, fecha y revisión; no se calcula por el texto.

## Human review boundary / Límite de revisión humana

La profesional define información revelable, compromiso, tono final y envío.

## Hard prohibitions / Prohibiciones estrictas

No prometer resultado, plazo o radicación; no enviar ni revelar otro caso.

## Composition / Composición

Contexto autorizado + template de tono + revisión humana.

## Example requests / Ejemplos de solicitud

“Prepare un mensaje claro que explique qué documentos faltan, sin prometer fechas.”

## Failure modes / Fallos previsibles

Tono impropio, información excesiva, compromiso no autorizado o confusión entre resumen y estado oficial.

## Evals / Evaluaciones

Claridad, fidelidad al contexto aprobado, protección de datos y detección de compromisos no autorizados.

## Priority / Prioridad

P2.

## Recommendation / Recomendación

`DEFER` como Skill; comenzar con patrón y revisión humana.
