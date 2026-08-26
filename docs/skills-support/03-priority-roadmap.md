# 03 — Roadmap cualitativo

> **Nota de navegación:** esta hoja de ruta conserva el detalle de la primera iteración. La hoja de ruta de referencia de la revisión v1 es [03-skill-priority-roadmap.md](03-skill-priority-roadmap.md).

**Estado:** propuesta de investigación; no es plan de implementación del Core.
**Criterios sin pesos:** frecuencia, tiempo consumido, severidad de error, repetición, disponibilidad de input, verificabilidad del output, costo de revisión humana, riesgo jurídico, reutilización y dependencia de derecho no verificado.

| Ola | Capacidades | Por qué ahora / después | Condiciones de entrada |
|---|---|---|---|
| **P0 — V0 existente** | `fact-builder`; límites de evidencia, proposal y revisión | Ya forma parte del vertical slice; su valor está en "hecho, prueba" | No ampliar V0 por este corpus |
| **P1 — siguiente ola** | `intake-structuring`, `evidence-analysis`, `legal-document-review`, `legal-research`, `legal-drafting` | Alta reutilización transversal y trabajo observado; cubren entrada, comprensión, revisión, fuentes y borrador | Baseline con profesional; source governance; diseños de eval; no autorizar sin gates |
| **P2 — capacidades compuestas** | `legal-issue-spotting`, `hearing-analysis`, `contradiction-analysis`, `adversarial-review`; workflows de petición, demanda, contestación y recursos | Metodologías diferenciadas, pero dependen de contexto y conocimiento más rico | P1 validada, Knowledge Packs fechados, transcripción/locators cuando aplique |
| **P3 — discovery adicional** | negociación/conciliación; apoyo a decisor/autoridad; tutela especializada; conectores/radicación | Alto riesgo o contexto real todavía incompleto | Descubrir flujo de autoridad, régimen aplicable, seguridad y permisos |

## Trazabilidad cualitativa por candidata o capacidad

Esta matriz no inventa una puntuación ni una frecuencia. Explica por qué una capacidad está en su ola y qué evidencia faltaría para moverla.

| Candidata o capacidad | Ola | Reutilización / riesgo | Dependencia que explica la posición | Evidencia para avanzar |
|---|---|---|---|---|
| fact-builder | P0 | ya ejercita el valor central de hechos con soporte | vertical slice vigente; solo contexto litigante | no ampliar V0 desde este corpus |
| intake-structuring | P1 | entrada transversal y repetible; riesgo medio | confirmar formato real de entrevista y revisión | baseline de entrevistas con la profesional |
| evidence-analysis | P1 | cobertura transversal; error probatorio alto | usa Evidence/provenance sin crear nuevos enlaces o entidades | fixtures de cobertura, huecos y contradicción |
| legal-document-review | P1 | reutilización alta; evita defectos visibles | reglas duras siguen en Core y requisitos específicos en Pack | muestras sintéticas por tipo de documento |
| legal-research | P1 | riesgo jurídico muy alto, pero método claramente separado | requiere gobierno de fuentes y futura verificación; no existe en V0 | fuentes reales de la profesional y eval de citas |
| legal-drafting | P1 | valor transversal alto; borrador siempre revisable | depende de hechos/fuentes trazables y de gate humano | patrones de salida y revisión profesional |
| legal-issue-spotting | P2 | útil, pero depende de investigación y contexto suficiente | no resuelve derecho ni crea un Issue canónico V0 | distinguir su método frente a legal-research |
| hearing-analysis | P2 | riesgo alto y buena reutilización | exige transcripciones/locators y práctica real de audiencia | fixture con atribución e incertidumbre |
| contradiction-analysis | P2 | valor alto, pero sin entidad canónica V0 | debe separar conflicto formal de tensión semántica | casos sintéticos con ambos tipos de conflicto |
| adversarial-review | P2 | alto valor estratégico; revisión humana esencial | depende de borrador, evidencia y objetivo procesal | criterios de utilidad validados por la profesional |
| Petición, demanda, contestación, memorial y recurso | P2 | productos frecuentes, pero son composición de métodos | requisitos/estado/plazo dependen de procedimiento, fecha y registro verificable | Knowledge Pack fechada y caso de uso de estado futuro |
| Concepto jurídico y comunicación con cliente | P2 | valor claro; no justifican Skill autónoma | composición de investigación, redacción y revisión; estilo es template | validar tono, contenido mínimo y decisiones reservadas |
| Conciliación / negociación | P3 | alto riesgo y demanda todavía inferida | estrategia, intereses y reglas requieren discovery propio | flujo real, límites y criterios de la profesional |
| Tutela especializada | P3 | trámite sensible y especial | reglas/jurisprudencia/temporalidad requieren Pack y práctica confirmada | dossier y fixture específicos antes de producto |
| Apoyo a decisor / autoridad | P3 | riesgo máximo | contexto B, expediente oficial, permisos y gates no están levantados | discovery de autoridad y arquitectura post-V0 |

## Gates antes de convertir P1 en producto

1. La profesional confirma el problema, frecuencia aproximada y forma de revisión.
2. Existe fixture sintético con información faltante, contradicción y fuente no verificada.
3. Las dependencias del Core están declaradas y no se suplirán con texto de Skill.
4. El Knowledge Pack indica jurisdicción, fecha aplicable, fuente y estado de verificación.
5. Hay una salida que permite revisión humana rápida sin fingir certeza.
6. La candidata supera la prueba de no duplicación frente a las demás.

## Señal de parada

No diseñar una Skill nueva si solo cambia el nombre del documento, la plantilla, el área jurídica o la fuente. Crear o ajustar un recurso/workflow/Knowledge Pack es preferible hasta que aparezcan un trigger, método y eval distintos.
