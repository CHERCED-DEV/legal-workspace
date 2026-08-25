# Candidata de Skill: contradiction-analysis

## Propósito

Encontrar y presentar tensiones entre fuentes sin convertir una comparación semántica en una determinación de falsedad.

## Tarea repetible que resuelve

Comparar fecha, monto, identidad, secuencia, documento/testimonio, testimonio/testimonio, alegación/evidencia y salida previa/cambio posterior.

## Cuándo usarla y cuándo no

Invocar cuando se pide comparar versiones o revisar coherencia. No invocar para decidir credibilidad, declarar fraude, retirar un Fact ni escribir una entidad `Contradiction` canónica V0.

## Entradas y salidas

Entrada: dos o más fragmentos/Evidence, Facts o textos con fuente. Salida: lado A, lado B, tipo formal/semántico, locators, explicación neutral y pregunta de revisión.

## Método

Primero normalizar solo datos verificables (fecha/valor/identidad); luego contrastar significado y condiciones; mostrar evidencia contraria; etiquetar tensión y confianza, no veredicto.

## Referencias y recursos necesarios

[Workflow de audiencias/contradicciones](../workflows/07-hearing-analysis-and-contradictions.md), patrón de calidad y recursos de evidence analysis.

## Dependencias del Core y MCP

Core da identidades, versiones, locators y provenance. La detección formal puede ser Application futura; el análisis semántico es candidata. Sin herramienta MCP nueva V0.

## Paquete de conocimiento (Knowledge Pack) y límite de revisión humana

Puede ser transversal; la relevancia jurídica/consecuencia requiere Knowledge Pack y humana.

## Prohibiciones estrictas

No afirmar que una parte miente, no alterar estados de Fact, no omitir una condición que reconciliaría las versiones, no confundir coincidencia textual con contradicción material.

## Composición, ejemplo y estructura esperada

Compone evidence, hearing, review y adversarial. Ejemplo: “compare estos dos documentos”. Estructura: afirmaciones; pasajes; diferencia; explicaciones alternativas; revisión necesaria.

## Fallos previsibles y evaluación

Falsos positivos por contexto, diferencias de formato o fechas parciales; falso negativo por sinónimos/derivados. Medir recall/precisión formal y semántica por separado.

## Prioridad y recomendación

P2 — **KEEP**; metodología y evals diferentes justifican separarla de evidence-analysis.
