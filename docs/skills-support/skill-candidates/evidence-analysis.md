# Candidata de Skill: evidence-analysis

## Propósito

Analizar cobertura, relación y tensión entre fuentes del Case para preparar una matriz probatoria revisable, sin valorar definitivamente prueba.

## Tarea repetible que resuelve

Clasificar material, relacionar Facts propuestos con fragmentos, detectar huecos/incompletitud y comparar fuentes sin convertir evidencia en determinación.

## Cuándo usarla y cuándo no

Invocar ante “qué prueba respalda/contradice/falta”, comparación de documentos o preparación de matriz. No invocar para acreditar hechos, admitir prueba, asignar peso o modificar EvidenceLink por sí sola.

## Entradas y salidas

Entrada: Evidence incorporada, Source/DerivedRepresentation, locators, Facts/objetivo. Salida: matriz hecho–evidencia, cobertura parcial, tensiones, fuentes no utilizables y preguntas.

## Método

Separar primaria/derivada; usar locator; distinguir `SUPPORTS`, `CONTRADICTS`, `CONTEXTUALIZES` como propuestas respecto del contrato del Core; declarar búsqueda/incompletitud y no inferir autenticidad del hash.

## Referencias y recursos necesarios

[Workflow fact/evidence](../workflows/02-fact-construction-and-evidence.md), glosario/ADR-003/ADR-006 y recursos de locators. No incorporar reglas de admisibilidad colombiana al método.

## Dependencias del Core y MCP

Necesita Core para identidad, incorporación, locator, provenance, Proposal y commit. V0 no autoriza nueva tool; debe usar contratos existentes o esperar diseño posterior.

## Paquete de conocimiento (Knowledge Pack) y límite de revisión humana

La relevancia/valoración/admisibilidad dependen de área y fecha. La profesional decide peso, suficiencia y consecuencia de tensión.

## Prohibiciones estrictas

No marcar `ALLEGED`/`DETERMINED`; no tratar derivado como original, no inventar locators ni declarar no encontrado=inexistente.

## Composición, ejemplo y estructura esperada

Compone con `fact-builder`, `contradiction-analysis`, `hearing-analysis`, drafting/review. Ejemplo: “haga matriz de qué prueba cada hecho”. Estructura: fuente; fragmento; relación; alcance; incertidumbre.

## Fallos previsibles y evaluación

Riesgo de cobertura aparente, duplicados, atribución errónea y contradicción falsa. Evaluar precisión de locator, recall de huecos, primaria/derivada y hechos sin soporte.

## Prioridad y recomendación

P1 — **KEEP**; no fusionar con fact-builder porque la matriz/cobertura tiene trigger, salida y evals propios.
