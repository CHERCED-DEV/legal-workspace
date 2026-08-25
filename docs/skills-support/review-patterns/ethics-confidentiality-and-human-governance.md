# Patrón transversal — Ética, confidencialidad y gobierno humano

**Jurisdiction:** Colombia para las fuentes seed; el patrón de arquitectura es transversal.
**Fuente seed:** Ley 1123 de 2007, `VERIFIED_OFFICIAL`, 2026-08-25, en [matriz temporal](../source-catalog/temporal-law-matrix.md).

## Qué cubre

Este patrón no crea una “Skill de ética”. Reúne obligaciones y riesgos que deben cruzar intake, evidence, research, drafting, review y comunicación: secreto profesional, diligencia, independencia, lealtad, conflicto de interés y tratamiento de información del cliente.

## Distribución correcta de responsabilidades

| Riesgo / necesidad | Dueño correcto |
|---|---|
| Aislar Cases, no exponer Private State, controlar permisos y provenance | Legal Core / infraestructura / Product Floor |
| No convertir el texto de un archivo en instrucción | host/Core/policy + metodología de Skill |
| Aplicar mínimos de contexto y no guardar secretos en recursos | diseño de Skill + revisión humana |
| Conflicto de interés, aceptación de encargo, secreto y estrategia | profesional/organización; Knowledge Pack cuando aplique |
| Estilo o guion de consulta ética | reference resource / template, nunca enforcement |
| Sanción, deber disciplinario o interpretación normativa | fuente oficial + análisis humano |

## Checklist de uso para toda candidata

1. ¿Se utiliza solo el Case/contexto mínimo autorizado?
2. ¿El output distingue información del cliente, Evidence incorporada, fuente externa y propuesta de IA?
3. ¿Puede una instrucción escondida en documento alterar la tarea? Debe responderse “no”: es contenido, no instrucción.
4. ¿Se expone una conclusión profesional como si fuese automática? Si sí, detener y pedir revisión.
5. ¿Se entrega una advertencia útil sin mostrar identificadores, hashes, rutas o detalles internos innecesarios?
6. ¿La operación intenta saltar el canal humano, autorización o commit? Si sí, no pertenece a una Skill.

## Fuente y temporalidad

La Ley 1123 es una fuente seed, no una licencia para crear reglas deontológicas genéricas en texto de Skill. Antes de cualquier afirmación concreta, recuperar artículo, versión, autoridad competente y fecha de consulta. La confidencialidad real se protege por arquitectura y práctica profesional, no porque un prompt prometa guardar secreto.

## Evals transversales

- Fixture con datos sintéticos de dos Cases: comprobar que no mezcla contexto.
- Documento con instrucción maliciosa: confirmar que se trata como evidencia/contenido.
- Solicitud que pide aprobar/decidir: confirmar abstención y ruta al gate humano.
- Output para persona no técnica: verificar que comunica incertidumbre sin jerga de sistema.

