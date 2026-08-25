# Candidata de Skill: legal-document-review

## Propósito

Revisar un borrador o documento recibido y reportar defectos falsables de estructura, soporte, coherencia, fuente y requisitos declarados; no aprobarlo ni decidir estrategia.

## Tarea repetible que resuelve

Separar checks deterministas, hallazgos semánticos y decisiones profesionales al revisar demanda, contestación, memorial, petición, recurso, concepto o proyecto de decisión.

## Cuándo usarla y cuándo no

Invocar para “revise qué falta/qué contradice/qué no está respaldado”. No para certificar cumplimiento legal, firmar, radicar, decidir procedencia o reemplazar Knowledge Pack.

## Entradas y salidas

Entrada: tipo/objetivo/rol, documento, Facts/Evidence autorizados, fuentes y checklist aplicable. Salida: defecto, ubicación, evidencia, clase, severidad cualitativa, contraargumento y acción humana.

## Método

Revisar primero cobertura formal declarada, luego coherencia y soporte, después fuentes/temporalidad; diferenciar “no observado” de “ausente”; ofrecer pasaje de prueba y pregunta, no un juicio conclusivo.

## Referencias y recursos necesarios

[Workflow drafting/review](../workflows/04-legal-drafting-and-document-review.md), [patrón de calidad](../review-patterns/quality-and-source-review.md) y resource por tipo documental.

## Dependencias del Core y MCP

Contexto y provenance del Core; validaciones deterministas pertenecen a Application. No necesita ni crea herramienta MCP V0 adicional.

## Paquete de conocimiento (Knowledge Pack) y límite de revisión humana

Requisitos procesales, término/canal/competencia y derecho aplicable requieren pack fechado. La humana resuelve importancia, corrección y presentación final.

## Prohibiciones estrictas

No emitir “aprobado/listo para radicar”, no inventar requisitos, no citar fuentes sin verificar, no convertir formato de oficina en deber legal.

## Composición, ejemplo y estructura esperada

Compone después de drafting/research/fact evidence. Ejemplo: “revise esta demanda contra la lista de hechos y fuentes”. Salida: tabla de hallazgos comprobables, no reescritura opaca.

## Fallos previsibles y evaluación

Falsos positivos, lista genérica, omitir defecto crítico, confundir argumento/hecho. Medir recall de defectos sembrados, precisión y objeción infundada.

## Prioridad y recomendación

P1 — **KEEP**; candidato transversal de mayor valor que Skills separadas de demanda/petición/recurso.
