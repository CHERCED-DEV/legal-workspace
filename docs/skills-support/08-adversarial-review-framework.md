# 08 — Marco de revisión adversarial

**Propósito:** intentar debilitar intelectualmente un entregable antes de presentarlo, sin pronosticar resultados ni convertir una observación de IA en defecto confirmado.

## Dos modos complementarios

| Modo | Pregunta | Enfoque | No hace |
|---|---|---|---|
| Counterparty Counsel | ¿Por dónde podría atacar una contraparte razonable? | hechos sin soporte, excepciones, teoría alternativa, contradicción, fuente débil, regla especial o riesgo procesal | afirmar que el ataque triunfará |
| Judicial Rigor | ¿Qué conclusión no puede adoptarse rigurosamente con el expediente disponible? | simetría, prueba contraria, carga, motivación, congruencia, vigencia y sesgo | favorecer a una parte o emitir decisión |

## Ficha de hallazgo

| Campo | Regla |
|---|---|
| finding_id / modo / objetivo | Identificar qué se revisa y desde cuál modo. |
| ataque / razón | Formular una crítica concreta, no “mejorar redacción”. |
| case_references | Citar Evidence, Facts, documento o locator; si falta, decirlo. |
| legal_sources | Fuente y estado si el hallazgo depende de derecho. |
| gravedad / consecuencia | Calibrar como riesgo, no como resultado seguro. |
| información faltante / remediación | Explicar qué comprobar o fortalecer. |
| riesgo residual / soporte | Declarar lo que sigue abierto. |

Si un hallazgo no tiene soporte factual o jurídico suficiente, usar **`UNSUPPORTED_REVIEW_OBSERVATION` — observación de revisión sin soporte** y no presentarlo como defecto confirmado.

## Escala de evaluación

| Estado | Significado |
|---|---|
| `ROBUST` | No se detectaron debilidades materiales en el material revisado; **no es un pronóstico ni garantía**. |
| `DEFENSIBLE_WITH_RISKS` | Hay una postura seria, con riesgos visibles y acciones posibles. |
| `MATERIAL_WEAKNESSES` | Hay debilidades materiales que requieren revisión antes de usar el producto. |
| `HIGH_RISK` | Hay material insuficiente, contradicción grave o regla/fuente crítica pendiente. |
| `INSUFFICIENT_BASIS` | No existe base suficiente para una evaluación responsable. |

## Restricciones

- No usar “caso ganado”, “demanda aprobada”, “el juez fallará” ni equivalentes.
- No inventar hechos, fuentes, precedentes ni ataques.
- Diferenciar comprobación determinista, hallazgo semántico y juicio profesional.
- Mantener todos los hallazgos como propuestas revisables por la persona competente.

Los procedimientos detallados están en [adversarial-review/counterparty-counsel.md](adversarial-review/counterparty-counsel.md) y [adversarial-review/judicial-rigor.md](adversarial-review/judicial-rigor.md).
