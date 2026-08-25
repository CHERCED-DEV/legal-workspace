# 03 — Hoja de ruta de Skills y condiciones de prioridad

**Estado:** priorización cualitativa de investigación; no es plan de implementación del Core.

## Criterios

No se asignan frecuencias ni tiempos inventados. La posición se explica por reutilización, riesgo de error, posibilidad de evaluación, dependencia de contexto/fuentes, costo de revisión humana y necesidad de cambios posteriores de arquitectura.

| Ola | Capacidades | Razón | Condición para avanzar |
|---|---|---|---|
| P0 | fact-builder y controles existentes | Única Skill integrada en el vertical slice; trabaja sobre propuesta y revisión, no sobre decisión automática | No ampliarla desde este corpus |
| P1 | intake-structuring, evidence-analysis, legal-document-review, legal-research, legal-drafting | Método transversal distinto y valor observable | baseline, fixtures, fuentes gobernadas y límites humanos explícitos |
| P2 | legal-issue-spotting, hearing-analysis, contradiction-analysis, adversarial-review, case-status review | Requieren más material, contexto o taxonomía, pero tienen salida falsable | práctica real confirmada y evaluación diferenciada |
| P3 | tutela especializada, conciliación/negociación, policivo/querellas, apoyo a decisor | Alto riesgo, reglas especiales o contexto B sin discovery suficiente | régimen verificado, flujo profesional real y arquitectura post-V0 si aplica |

## Decisiones de composición

| Producto pedido | Decisión actual | Composición correcta |
|---|---|---|
| Demanda, contestación, memorial o recurso | MERGE | hechos/evidencia + investigación + redacción + revisión + reglas fechadas + decisión humana |
| Derecho de petición y respuesta | MERGE | clasificación + investigación + redacción/revisión + regla fechada + revisión humana |
| Concepto jurídico | MERGE | issue spotting + investigación + redacción + adversarial + decisión profesional |
| Tutela | DEFER | composición anterior más dossier y fuente constitucional específica; no Skill separada hasta validar método propio |
| Comunicación con cliente | DEFER como Skill; KEEP como recurso | contexto autorizado + plantilla de tono + revisión humana |
| Conciliación/negociación | NEEDS_DISCOVERY | información, riesgos, posiciones e intereses, sin decidir acuerdo |
| Decisión de autoridad | DEFER | contexto B, expediente oficial, permisos, trazabilidad y autoridad humana primero |

## Gate antes de crear una Skill

1. Hay un activador, entrada, salida y método que no duplica otra candidata.
2. La profesional confirma demanda, frecuencia aproximada o costo de trabajo.
3. Existen fixtures sintéticos que prueban faltantes, contradicciones, fuente no verificada e inyección.
4. Las reglas jurídicas dependen de fuentes fechadas, no de memoria del modelo.
5. El Core conserva cualquier validación, autorización o transición sensible.
6. La salida muestra el material, la incertidumbre y la decisión humana pendiente.

Ver [03-priority-roadmap.md](03-priority-roadmap.md) para el razonamiento de la primera iteración y [skill-candidates/INDEX.md](skill-candidates/INDEX.md) para el índice operativo.
