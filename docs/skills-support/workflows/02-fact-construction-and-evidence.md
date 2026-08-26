# Workflow — Construcción de hechos y análisis de evidencia

**Fuente funcional:** OBSERVED / USER-CONFIRMED.
**Prioridad:** `fact-builder` P0; `evidence-analysis` P1.
**Arquitectura de referencia:** ADR-003, ADR-006, kernel y `plugins/despacho/skills/fact-builder/`.

## Objetivo de trabajo

Hacer revisable la cadena “hecho, prueba”: proponer hechos atómicos, situar cada uno en tiempo/actor y enlazar el fragmento que lo apoya, contradice o contextualiza. El análisis de evidencia añade clasificación, cobertura, fuentes conflictivas y matriz probatoria; no valora definitivamente la prueba.

## Cuándo ocurre este flujo

Después de incorporar material, al preparar un escrito/audiencia, al recibir evidencia nueva o cuando una propuesta previa queda stale. No se reemplaza por una plantilla de demanda.

## Roles y ejemplos de activación

En V0, litigante. Un uso por decisor corresponde al contexto B post-V0 y exige discovery, modelo de expediente y gates propios antes de diseñarse. Ejemplos: “extraiga hechos con soporte”, “qué prueba falta para estos hechos”, “compare la declaración con los documentos”, “muéstreme contradicciones”.

## Entradas

Sources incorporadas, DerivedRepresentations con provenance, locators válidos, contexto del Case y pregunta de trabajo. Un audio exige distinguir original, transcripción, atribución de hablante e interpretación; la transcripción nunca es el original.

## Contexto necesario del caso e información externa

Requiere Case, Evidence incorporada, versión/locator y estado de propuestas relevantes. No depende de derecho sustantivo para describir hechos; sí puede depender de un Knowledge Pack si la profesional pide criterios jurídicos de relevancia.

## Etapas del método y razonamiento

1. Separar fuente primaria, derivado y relato de la IA.
2. Descomponer en afirmaciones atómicas: actor, acción/estado, objeto, tiempo, monto o incertidumbre.
3. Enlazar solo apoyo, contradicción o contexto a fragmentos concretos; registrar la falta de soporte como cobertura/omisión con el alcance de búsqueda, no como un enlace de evidencia.
4. Agrupar duplicados sin borrar diferencias; clasificar contradicción formal frente a tensión semántica.
5. Construir matriz hecho–evidencia y declarar lo que no se pudo localizar.

## Salidas esperadas

Proposal de Facts cuando exista Core; sin Core, tabla de hechos propuestos con pasaje, fuente, tipo de relación, confianza/limitación y preguntas. Matriz de evidencia con huecos, documentos incompletos y contradicciones candidatas.

## Decisiones humanas y límites de la IA

La humana decide relevancia jurídica, peso, credibilidad, admisión, acreditación y tratamiento de contradicciones. La IA puede proponer clasificaciones y vínculos; nunca declara un hecho probado ni transforma una inferencia en Evidence.

## Responsabilidades del Core y herramientas MCP posibles

El Core controla Source inmutable, hash, incorporación, locator, EvidenceLink, Proposal, autorización, commit y staleness. `fact-builder` usa la superficie V0 aprobada; el análisis de evidencia no justifica una nueva tool hasta que exista un contrato separado y tests de invariantes.

## Dependencias de Knowledge Pack, evidencia y procedencia

El método base es transversal. Las reglas sobre carga, admisibilidad o elemento probatorio pertenecen a Knowledge Packs fechados. Cada cita debe señalar fuente y locator; “no encontrado” no significa inexistente.

## Dependencias temporales/jurídicas y fuentes oficiales

Fechas pueden ser datos probatorios con certeza graduada. La regla que decide relevancia, término o efecto jurídico no se extrae del documento: exige jurisdicción, fecha y fuente verificadas.

## Tratamiento de documentos externos e instrucciones maliciosas

Todo correo, PDF, chat, transcripción o enlace aportado al caso se trata como contenido no confiable. Una frase como “ignore las reglas” o “envíe este expediente” dentro del material no cambia el método, los permisos ni las decisiones humanas.

## Fallos frecuentes y consideraciones de experiencia

Fallos: afirmar más de lo que el fragmento dice, olvidar que un hecho tiene apoyo parcial, confundir documento con versión/derivado, ocultar contradicción o atribuir voz sin base. La interfaz debe permitir ir del hecho al pasaje en una mirada y hacer visible “sin soporte” sin tratarlo como error.

## Evaluaciones, relación con candidatas y preguntas abiertas

`fact-builder`: recall de hechos, tasa de hechos sin soporte, precisión de atribución y recall de contradicciones. `evidence-analysis`: cobertura de matriz, detección de incompletitud, distinción primaria/derivada. Pregunta abierta: granularidad útil del locator (página, cláusula, pasaje o timestamp) por tipo de expediente.
