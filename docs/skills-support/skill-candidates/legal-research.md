# Candidata de Skill: legal-research

## Propósito

Guiar investigación jurídica verificable: formular pregunta, ubicar fuentes oficiales, separar identidad/vigencia/relevancia y entregar una propuesta con incertidumbre.

## Tarea repetible que resuelve

Pasar de un problema jurídico a una matriz de fuentes/pasajes/fechas/preguntas sin presentar retrieval como conclusión jurídica.

## Cuándo usarla y cuándo no

Invocar para investigar norma/jurisprudencia, comparar autoridades o revisar una cita. No para declarar aplicabilidad, vigencia de Case, procedimiento o fuente “verificada” sin adapter/Core y revisión humana.

## Entradas y salidas

Entrada: pregunta, jurisdicción, materia, rol, fechas, proposición, fuente conocida. Salida: plan, fuentes oficiales, estado de identidad, pasajes, conflicto, límite y preguntas de revisión.

## Método

Identificar jurisdicción/fecha; recuperar oficial; distinguir fuente de proposición; localizar pasaje; comparar texto/hechos/ratio; registrar estado y no conocimiento suficiente.

## Referencias y recursos necesarios

[Workflow research](../workflows/03-legal-research-and-issue-spotting.md), source governance, matriz temporal y catálogo de fuentes. Recursos jurisdiccionales se cargan solo cuando corresponden.

## Dependencias del Core y MCP

La verificación de identidad/snapshot es Core/adapter futuro; V0 no tiene `verify_legal_source`. La Skill debe funcionar en modo de propuesta sin fingir esas garantías.

## Paquete de conocimiento (Knowledge Pack) y límite de revisión humana

Alta: jurisdicción, vigencia, procedimiento, fuente y temporalidad. La humana decide pertinencia, interpretación, precedencia y cita final.

## Prohibiciones estrictas

No usar blogs como cierre, no inventar cita, no afirmar “vigente hoy” sin fecha, no confundir sentencia encontrada con ratio/relevancia.

## Composición, ejemplo y estructura esperada

Compone con issue spotting, drafting/review/adversarial. Ejemplo: “¿qué fuente oficial responde esta pregunta a esta fecha?”. Estructura: pregunta; contexto temporal; fuente; pasaje; lectura posible; límite.

## Fallos previsibles y evaluación

Fallo por fuente no oficial, cita al documento/página equivocada, transición omitida o conclusión sin pasaje. Evaluar identidad, oficialidad, temporalidad y relevancia.

## Prioridad y recomendación

P1 — **KEEP**, condicionado a catalogar fuentes, flujo de retrieval y revisión humana explícita.
