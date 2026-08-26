# 09 — Auditoría de completitud jurídica

**Fecha de corte:** 2026-08-25.
**Resultado honesto:** esta auditoría verifica estructura, trazabilidad y vacíos visibles dentro del universo funcional definido. No demuestra que todo el derecho colombiano haya sido investigado.

## Inventario y conteos

| Métrica | Resultado | Método |
|---|---:|---|
| total_workflows | 29 | Filas W01–W29 del [ledger de cobertura](06-colombian-law-coverage-ledger.md). |
| workflows_with_coverage_map | 29 | Cada workflow tiene fila en el ledger. |
| workflows_with_gaps | 29 | Ninguna fila se presenta como cobertura jurídica completa; todas conservan una brecha o investigación por caso/territorio. |
| workflows_not_legal_dependent | 2 | Clasificación documental y comunicación con cliente son métodos no jurídicos en abstracto; su uso concreto aún puede activar reglas jurídicas. Criterio unificado con la [matriz de workflows](workflows/coverage-matrix.md). |
| legal_reference_count | 36 | 26 IDs normativos `N-*` y 10 jurisprudenciales `J-*` definidos en los catálogos. |
| orphan_legal_reference_count | 0 | Los IDs estructurados usados en la matriz de claims resuelven a catálogo. No equivale todavía a reconciliar las 295 líneas con menciones jurídicas textuales. |
| unverified_reference_count | 2 | `N-CIVIL` y `N-L2080` aún no tienen fuente oficial concreta registrada. |
| temporal_gap_count | 25 | Filas del ledger cuyo check de transición queda en `GAP`; no mide todas las preguntas temporales posibles. |
| jurisprudence_gap_count | 24 | Filas cuyo check jurisprudencial queda en `GAP`; no mide todas las preguntas jurisprudenciales posibles. |
| territorial_gap_count | 19 | Filas cuyo check territorial queda en `GAP`; no mide todas las reglas territoriales posibles. |

## Auditorías 1 a 15

| Auditoría | Evidencia | Resultado |
|---|---|---|
| 1. Inventario de workflows | W01–W29 en el ledger y matriz de workflows | **Estructura revisada:** los 29 tienen mapa. |
| 2. Cobertura normativa | campos de ley principal, especiales, reformas, reglamentos y transición en ledger | **Brecha:** predominan `PARTIALLY_COVERED` / `REQUIRES_CASE_SPECIFIC_RESEARCH`. |
| 3. Cobertura jurisprudencial | [07](07-jurisprudence-governance.md) y catálogo J | **Brecha:** no hay líneas exhaustivas por pregunta material. |
| 4. Temporalidad | [05](05-temporal-applicability.md), matriz temporal y fixture laboral | **Método revisado; brecha por caso** y norma especial. |
| 5. Fuente oficial | catálogos normativo/jurisprudencial y disclaimer | **Método revisado; contraste adicional requerido** en puntos críticos. |
| 6. Trazabilidad | [claim-source matrix](legal-dependency-maps/claim-source-matrix.md) | **Muestra revisada; brecha** para todas las afirmaciones. |
| 7. Derecho adverso | marco adversarial y gobierno de jurisprudencia | **Diseño revisado; brecha** de investigación por asunto. |
| 8. Especial vs. general | mapas de dependencia y regla de prioridad | **Diseño revisado; brecha** de aplicación concreta. |
| 9. Territorialidad | mapa policivo y filas W24/W25 | **Brecha material:** reglas locales no cargadas. |
| 10. Derecho transversal | mapas de datos, familia, digital y constitucionalidad | **Documentado con vacíos** (`PARTIALLY_COVERED`). |
| 11. Disclaimers | catálogo de fuentes y regla de contraste | **Método revisado.** |
| 12. No-hallucination check | 36 IDs N/J: 0 sin resolver; 295 líneas con menciones jurídicas textuales | **Brecha:** falta reconciliar todas las menciones textuales a nivel de pasaje/regla. |
| 13. Claim-source matrix | 12 afirmaciones críticas muestreadas | **Muestra revisada; brecha** de cobertura completa. |
| 14. Riesgo de obsolescencia | tabla siguiente | **Clasificación editorial revisada.** |
| 15. Resultado de cobertura | ledger + gaps materiales | `COVERAGE_GAPS_PRESENT` |

## Riesgo editorial de obsolescencia

| Grupo | Riesgo | Razón |
|---|---|---|
| Ley 2452 / Ley 2466 / transición laboral | HIGH_MAINTENANCE | reformas recientes, vigencias diferidas y transición |
| Petición, transparencia, datos y digital | HIGH_MAINTENANCE | interacción sectorial, reservas, reglamentación y canales |
| Tutela y jurisprudencia | HIGH_MAINTENANCE | desarrollo jurisprudencial y evaluación por hechos |
| Familia/protección/apoyos | HIGH_MAINTENANCE | normas especiales, sujetos protegidos, rutas y territorio |
| Policivo/autoridad | HIGH_MAINTENANCE | territorialidad, reglamentación y contexto B pendiente |
| Métodos universales de hechos/evidencia | MEDIUM_MAINTENANCE | el método es estable, pero sus efectos jurídicos cambian por área |

## Gaps concretos que impiden cerrar cobertura

1. No se verificó una red completa de reformas, derogatorias, reglamentos y controles constitucionales para cada combinación de workflow, materia y fecha.
2. No se elaboraron líneas jurisprudenciales exhaustivas, con autoridad adversa y posterior, para cada pregunta jurídica material.
3. Policivo, administrativo territorial y apoyo a autoridad requieren acto, entidad, municipio/territorio y expediente oficial.
4. Las reglas procedimentales, términos y recursos requieren estado procesal verificable que no existe en V0.
5. Tutela, datos, familia/protección, documento digital y laboral necesitan investigación según hechos, sujeto, fecha y norma especial.

## Condición de cierre

No usar `COVERAGE_CONFIRMED_WITHIN_DEFINED_SCOPE` mientras las métricas de trazabilidad textual y los gaps materiales anteriores sigan abiertos. El cierre actual es **`COVERAGE_GAPS_PRESENT`**.
