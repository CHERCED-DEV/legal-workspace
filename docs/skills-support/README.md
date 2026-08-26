# Corpus de soporte para Legal Skills

**Estado:** investigación funcional y metodológica; no es runtime, expediente, base de datos ni diseño normativo del Core.
**Fecha de referencia:** 2026-08-25.
**Estado de preparación:** `SKILL_SUPPORT_CORPUS_NOT_READY`.
**Resultado de cobertura:** `COVERAGE_GAPS_PRESENT`.

Este corpus ayuda a diseñar Skills jurídicas pequeñas, comprobables y seguras para personas que trabajan en español. No crea una Skill nueva, no cambia el Core y no convierte una norma encontrada en una respuesta automática para un caso.

## Empiece por aquí

| Si necesita saber… | Consulte… |
|---|---|
| qué incluye el corpus y qué no puede hacer | [alcance y gobierno](00-scope-and-governance.md) |
| qué tareas jurídicas se identificaron | [mapa de capacidades](01-business-capability-map.md) y [matriz de workflows](workflows/coverage-matrix.md) |
| qué pertenece a una Skill, al Core o a una persona | [matriz de fronteras](02-skill-boundary-matrix.md) |
| qué se prioriza y qué se compone en vez de crear como Skill | [hoja de ruta](03-skill-priority-roadmap.md) y [candidatas](skill-candidates/INDEX.md) |
| de dónde proviene una regla y cómo verificarla | [gobierno de fuentes](04-source-governance.md), [catálogo normativo](source-catalog/normative-sources.md) y [catálogo jurisprudencial](source-catalog/jurisprudence-sources.md) |
| cómo evitar errores por fecha, transición o norma especial | [aplicabilidad temporal](05-temporal-applicability.md) y [mapas de dependencias](legal-dependency-maps/README.md) |
| qué está cubierto y qué falta por investigar | [ledger jurídico colombiano](06-colombian-law-coverage-ledger.md) y [auditoría de completitud](09-legal-completeness-audit.md) |
| cómo revisar jurisprudencia y el argumento contrario | [gobierno de jurisprudencia](07-jurisprudence-governance.md) y [marco adversarial](08-adversarial-review-framework.md) |
| cómo probar una futura Skill sin usar casos reales | [evaluaciones sintéticas](evals/README.md) |
| qué debe confirmar una profesional antes de producto | [preguntas abiertas](open-questions/questions-for-professional.md) |

## Regla práctica

Una Skill puede ordenar información, hacer preguntas, señalar faltantes y preparar una propuesta. No puede por sí sola declarar un hecho probado, confirmar que una norma aplica, calcular un término, firmar, radicar, decidir un caso ni cambiar el estado canónico. Esas tareas siguen siendo del Core, de una fuente/control verificable o de una persona competente.

## Lenguaje para las personas usuarias

Las salidas futuras deben decir, por ejemplo, “falta este documento”, “la fuente necesita verificación” o “requiere revisión profesional”. No deben mostrar detalles de ingeniería como MCP, hashes, JSON, rutas locales o puntajes internos salvo que una profesional los necesite expresamente.

## Límites y mantenimiento

- Use las etiquetas de certeza y los estados de fuente definidos en [00](00-scope-and-governance.md) y [04](04-source-governance.md).
- Registre cada investigación en el [registro de investigación](source-catalog/research-log.md).
- Revalide fuentes cuando cambie la fecha, la materia, el territorio, el procedimiento o el portal consultado.
- Si el research contradice una decisión arquitectónica Accepted, regístrelo como `RESEARCH CONFLICT WITH ACCEPTED ARCHITECTURE`; no cambie silenciosamente la arquitectura.
- La ruta vigente del plugin existente es `plugins/despacho/skills/fact-builder/`. Cualquier referencia histórica a `plugin/skills/fact-builder/` no es una ruta de trabajo actual.
