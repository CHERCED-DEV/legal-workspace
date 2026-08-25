# Candidata de Skill: legal-issue-spotting

## Propósito

Convertir hechos, objetivos y contexto en preguntas jurídicas potenciales que deben investigarse, sin afirmar qué regla las resuelve.

## Tarea repetible que resuelve

Identificar asuntos de materia, procedimiento, evidencia, jurisdicción, oportunidad, legitimación, remedio y riesgo cuando los inputs lo permiten.

## Cuándo usarla y cuándo no

Invocar al inicio de análisis o cuando se pide “qué debo investigar”. No invocar para dar concepto, elegir norma, calificar hechos o declarar que existe un recurso/acción.

## Entradas y salidas

Entrada: hechos/Evidence disponibles, objetivo, rol, jurisdicción y fecha conocida. Salida: mapa de preguntas, hechos que las disparan, datos faltantes y ruta a `legal-research`.

## Método

Separar descripción de hipótesis; clasificar solo con soporte; proponer varias preguntas cuando hay interpretaciones; asociar cada pregunta a fuente/contexto que falta.

## Referencias y recursos necesarios

[Workflow research/issue spotting](../workflows/03-legal-research-and-issue-spotting.md) y taxonomía transversal. No cargar derecho colombiano en el método.

## Dependencias del Core y MCP

Necesita contexto autorizado/provenance si trabaja sobre Case; no necesita nueva tool. Los issues no son entidades canónicas V0.

## Paquete de conocimiento (Knowledge Pack) y límite de revisión humana

El marco de clasificación puede ser universal; reglas y relevancia dependen de Knowledge Pack. La humana decide qué investigar y cómo encuadrarlo.

## Prohibiciones estrictas

No convertir pregunta en conclusión; no usar “posible” para esconder una afirmación legal sin fuente; no crear plazo/estado procedimental canónico.

## Composición, ejemplo y estructura esperada

Compone antes de research/drafting/adversarial. Ejemplo: “a partir de este relato, enumere problemas por investigar”. Entrega: pregunta; hecho disparador; información faltante; fuente/capacidad siguiente.

## Fallos previsibles y evaluación

Riesgo de listar todo el derecho, omitir el rol/fecha o presentar taxonomía como diagnóstico. Evaluar precisión de abstención, cobertura de problemas sembrados y no invención.

## Prioridad y recomendación

P2 — **KEEP**; distinto de legal-research por objetivo y evaluación.
