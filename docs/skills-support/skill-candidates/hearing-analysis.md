# Candidata de Skill: hearing-analysis

## Propósito

Preparar y analizar audiencias mediante contexto, fuentes y locators, separando el original, la transcripción, hablante e interpretación.

## Tarea repetible que resuelve

Generar brief previo, extraer declaraciones/órdenes/compromisos posteriores y proponer preguntas o seguimiento con incertidumbre visible.

## Cuándo usarla y cuándo no

Invocar antes de audiencia o sobre acta/audio/transcripción incorporados. No invocar para atribuir voz sin base, decidir credibilidad, calcular efectos jurídicos ni actuar en audiencia.

## Entradas y salidas

Entrada: objetivo, agenda, Facts/Evidence, providencias, original y derivación con timestamps. Salida: brief, preguntas, tabla de declaraciones/locators, compromisos y acciones a verificar.

## Método

Preparar desde hechos/prueba pendiente; luego extraer pasaje antes de resumir; distinguir orden textual de efecto jurídico; enlazar siempre al original cuando sea audio.

## Referencias y recursos necesarios

[Workflow de audiencias](../workflows/07-hearing-analysis-and-contradictions.md), contrato de transcripción y Knowledge Pack de procedimiento si se pregunta por efectos.

## Dependencias del Core y MCP

Alta dependencia de Source/DerivedRepresentation/locator/provenance y staleness. Transcripción es adapter; no hay nueva tool V0.

## Paquete de conocimiento (Knowledge Pack) y límite de revisión humana

Reglas de audiencia, interrogatorio y términos son jurisdiccionales. La humana valida hablantes, compromisos, relevancia y estrategia.

## Prohibiciones estrictas

No tratar transcripción como original, no inventar timestamp/hablante, no afirmar que una mención crea un término ni tomar decisiones de audiencia.

## Composición, ejemplo y estructura esperada

Compone fact/evidence, contradiction, drafting/research. Ejemplo: “prepare resumen de audiencia con prueba pendiente”. Estructura: tema; pasaje; fuente; incertidumbre; acción humana.

## Fallos previsibles y evaluación

Fallo por atribución falsa, pasaje equivocado o omitir prueba contraria. Evaluar precisión de locators, hablante y recall de compromisos.

## Prioridad y recomendación

P2 — **KEEP**, condicionado a validar provider de transcripción y locators contra original.
