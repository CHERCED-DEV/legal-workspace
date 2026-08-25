# Corpus de soporte para Legal Skills

**Estado:** research funcional y metodológico; no es runtime ni diseño normativo del Core.
**Última revisión del corpus:** 2026-08-25.
**Precedencia:** los ADRs Accepted y el Technical Design V0 prevalecen sobre este directorio. Una observación de research nunca modifica por sí sola una decisión de arquitectura.

## Qué resuelve

Este corpus convierte el trabajo jurídico observado y el research externo en insumos revisables para diseñar Skills pequeñas, componibles y evaluables. Responde cuatro preguntas antes de crear una Skill:

1. ¿La tarea es repetible y tiene una metodología propia?
2. ¿Qué necesita como contexto, fuentes y evidencia?
3. ¿Qué puede proponer el modelo y qué debe decidir una persona o validar el Core?
4. ¿Cómo se comprobará que mejora el trabajo sin inventar derecho ni contaminar un expediente?

No es un conjunto de prompts, un Knowledge Pack ejecutable, un repositorio de expedientes ni una fuente de verdad jurídica. Tampoco altera el alcance V0: `fact-builder` continúa siendo la única Skill ejercitada del vertical slice.

## Cómo leerlo en diez minutos

| Pregunta | Documento |
|---|---|
| Límites, lenguaje y prueba ácida | [00-scope-and-principles.md](00-scope-and-principles.md) |
| Qué trabajo jurídico se quiere asistir | [01-business-capability-map.md](01-business-capability-map.md) |
| Dueño correcto de cada capacidad | [02-skill-boundary-matrix.md](02-skill-boundary-matrix.md) |
| Orden cualitativo de producto | [03-priority-roadmap.md](03-priority-roadmap.md) |
| Cómo se gobiernan fuentes y cambios | [04-source-governance.md](04-source-governance.md) y [05-temporal-applicability.md](05-temporal-applicability.md) |
| Dossiers de trabajo | [índice de workflows](workflows/README.md) y [dossiers por área](practice-areas/colombia-practice-area-dossiers.md) |
| Candidatas que merecen una Skill | [skill-candidates/INDEX.md](skill-candidates/INDEX.md) |
| Fuentes y trazabilidad de la investigación | [catálogo oficial](source-catalog/colombia-official-sources.md) y [matriz temporal](source-catalog/temporal-law-matrix.md) |
| Cómo se evalúan | [guía de evaluaciones](evals/README.md) |
| Vacíos que debe contestar la profesional | [open-questions/questions-for-professional.md](open-questions/questions-for-professional.md) |

## Candidatas y orden de producto

| Ola | Qué incluye | Estado |
|---|---|---|
| P0 | fact-builder y sus límites de evidencia, propuesta, autorización y commit | ya forma parte del vertical slice; este corpus no lo modifica |
| P1 | intake-structuring, evidence-analysis, legal-document-review, legal-research y legal-drafting | candidatas con método propio, pendientes de baseline, fuentes y evals |
| P2 | legal-issue-spotting, hearing-analysis, contradiction-analysis, adversarial-review y workflows compuestos | valiosas, pero dependen de más contexto, material o Knowledge Packs |
| P3 | conciliación/negociación, tutela especializada y apoyo a autoridad | DEFER: requieren discovery, régimen aplicable y gates post-V0 |

La decisión detallada por capacidad está en [03-priority-roadmap.md](03-priority-roadmap.md) y el índice de candidatas en [skill-candidates/INDEX.md](skill-candidates/INDEX.md).

## Modelo de separación

| Capa | Responsabilidad |
|---|---|
| **Skill** | Método interpretativo, estructura de una propuesta, preguntas de aclaración y presentación de incertidumbre. |
| **Legal Core / Application** | Estado canónico, aislamiento de casos, persistence, provenance, validaciones duras, transiciones, autorizaciones y commits. |
| **Knowledge Pack** | Contenido dependiente de jurisdicción, fecha, materia, procedimiento, rol y territorio. |
| **Reference resource** | Método, checklist, fuente, patrón, taxonomía o fixture que una Skill carga solo cuando lo necesita. |
| **Template** | Forma o estilo propio de una oficina; nunca prueba validez jurídica. |
| **Connector / Tool** | Recupera material o llama una capacidad externa; no convierte lo recuperado en evidencia ni en derecho verificado. |
| **Humana / gate humano** | Determinación profesional, aprobación, estrategia, admisión de riesgo, pertinencia jurídica final y acto oficial. |

La regla de seguridad es simple: si ignorar por completo una Skill permitiría acreditar un hecho, aceptar una fuente inexistente, saltar una autorización o corromper estado, el control obligatorio pertenece al Core, a una política validada o a una decisión humana. Un Knowledge Pack solo puede aportar contenido declarativo y versionado; nunca puede imponer por sí mismo un punto de control, una autorización o un invariante.

## Idioma y claridad para las personas usuarias

El corpus está escrito en español claro. Los identificadores técnicos que ya existen en la arquitectura (`fact-builder`, `EvidenceLink`, `ProposalItem`, nombres de herramientas) se conservan para no romper trazabilidad, pero siempre se explican en español. Una futura Skill debe producir documentos para una profesional jurídica, no para una persona técnica: debe decir “fuente pendiente de comprobar”, “documento faltante” o “requiere su revisión”, y no exponer MCP, hashes, JSON, rutas, bases de datos o puntuaciones internas.

## Convención de fuentes y tiempo

Toda afirmación jurídica concreta de este corpus usa una ficha de fuente con `source`, `checked_at` y `status`. Los estados permitidos son `VERIFIED_OFFICIAL`, `VERIFIED_SECONDARY`, `UNVERIFIED`, `CONFLICTING` y `OUTDATED`. Las fuentes oficiales y la matriz temporal están separadas del método universal para evitar convertir Colombia o una fecha concreta en comportamiento implícito de una futura Skill.

## Cómo una candidata se convierte en Skill real

1. Confirmar demanda con la profesional y ejecutar los evals de baseline pertinentes.
2. Confirmar que la metodología es distinta de las candidatas ya existentes y que tiene trigger, input, output y evaluación propios.
3. Separar recursos universales, Knowledge Packs jurisdiccionales y templates de oficina.
4. Diseñar dependencias explícitas del Core/MCP; no inventar herramientas para compensar una Skill débil.
5. Escribir un `SKILL.md` corto, con recursos bajo demanda, siguiendo las prácticas de progressive disclosure verificadas en la documentación oficial de Anthropic.
6. Probar contra fixtures sintéticos: camino feliz, información faltante, contradicción, fuente no verificada, jurisdicción errónea y régimen temporal erróneo cuando aplique.
7. Someter todo output con impacto jurídico a la revisión humana definida por la arquitectura.

## Mantenimiento

- Registre cada sesión de investigación en [source-catalog/research-log.md](source-catalog/research-log.md).
- Revalide fuentes cuya vigencia, interfaz o condiciones cambien; no use la frase "derecho actual" sin fecha.
- Mantenga el método universal fuera de los detalles colombianos; esos detalles viven en dossiers y Knowledge Packs futuros.
- Declare un conflicto real con ADR Accepted como `RESEARCH CONFLICT WITH ACCEPTED ARCHITECTURE`; no lo resuelva modificando silenciosamente el research.
