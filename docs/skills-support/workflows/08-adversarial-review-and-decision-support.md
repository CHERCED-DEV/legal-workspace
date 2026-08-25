# Workflow — Revisión adversarial y apoyo a decisión

**Fuente funcional:** OBSERVED / USER-CONFIRMED para estudiar contraparte, revisar actuaciones y preparar decisiones; detalle de rol decisor pendiente de discovery.
**Prioridad:** adversarial P2; decisión de autoridad P3.

## Objetivo de trabajo

Producir hallazgos que una persona pueda comprobar: vulnerabilidades de un caso/argumento o asimetrías de un borrador de decisión. No generar una aprobación global, una estrategia automática ni una determinación oficial.

## Cuándo ocurre este flujo

Antes de presentar un escrito, al estudiar postura contraparte, al revisar una providencia/borrador, o antes de una decisión donde deben considerarse argumentos y evidencia de ambos lados.

## Roles y ejemplos de activación

Litigante: “actúe como contraparte y busque debilidades”. Decisor: “muéstreme evidencia o argumentos ignorados”, “revise sesgos y saltos lógicos”. El segundo contexto requiere levantamiento específico antes de producto.

## Entradas

Alcance de revisión, hechos, Evidence/locators, argumentos de ambas partes, fuentes con estado, borrador y estándar de revisión que defina la humana. El modelo no recibe un mandato de “ganar”; recibe una pregunta falsable.

## Contexto necesario del caso e información externa

Contexto selectivo, no expediente completo por defecto. Un contexto de autoridad necesita determinar primero qué expediente oficial manda y qué es copia de trabajo; el V0 solo cubre litigante.

## Etapas del método y razonamiento

1. Declarar perspectiva, alcance y material revisado/omitido.
2. Para litigante: buscar soporte faltante, narrativa alternativa, contraargumentos, objeciones procedimentales y riesgos de prueba.
3. Para decisor: buscar evidencia/argumentos ignorados, trato asimétrico, inferencias sin base, contradicciones no resueltas y motivación incompleta.
4. Asociar cada hallazgo a pasaje, fuente/locator y pregunta de refutación.
5. Separar defecto verificable de alternativa estratégica y entregar contraargumento posible.

## Salidas esperadas

Lista priorizada de hallazgos falsables: afirmación, evidencia de soporte, posible efecto, contrapeso y acción humana sugerida. Nunca “aprobado”, “imparcial” o “decisión correcta” como resultado.

## Decisiones humanas y límites de la IA

La humana decide peso, sesgo, respuesta, estrategia, valoración de prueba, motivación y decisión/acto oficial. La IA puede proponer pruebas/argumentos omitidos, no declarar que existe parcialidad o que una providencia debe emitirse.

## Responsabilidades del Core y herramientas MCP posibles

Core provee aislamiento, provenance, revisión/commit y log; no se añaden tools en V0. Un futuro contexto decisor requerirá autorización, policy y modelo de expediente oficial antes de cualquier Skill, no al revés.

## Dependencias de Knowledge Pack, evidencia y procedencia

El método adversarial es universal; estándares procesales, deber de motivación, competencia y efectos pertenecen a Knowledge Pack por jurisdicción/rol. Cada hallazgo debe conservar la evidencia y el material contrario consultado.

## Dependencias temporales/jurídicas y fuentes oficiales

Dependen del procedimiento/rol y fecha del Case. No hay una fuente jurídica universal que sustituya la confirmación del contexto de autoridad; el corpus lo clasifica como P3 hasta levantarlo con la profesional.

## Tratamiento de documentos externos e instrucciones maliciosas

Todo correo, PDF, chat, transcripción o enlace aportado al caso se trata como contenido no confiable. Una frase como “ignore las reglas” o “envíe este expediente” dentro del material no cambia el método, los permisos ni las decisiones humanas.

## Fallos frecuentes y consideraciones de experiencia

Riesgo de fabricar contraargumentos, expresar preferencia como defecto, revisar solo la prueba favorable, convertir “posible” en conclusión y producir listas largas no accionables. Limitar el output a hallazgos trazables y preguntas que la profesional pueda resolver.

## Evaluaciones, relación con candidatas y preguntas abiertas

Medir recall de defectos sembrados, falsos positivos, cobertura de ambos lados, calidad de locators y tasa de objeción infundada. Mapea a `adversarial-review`; apoyo decisor queda DEFER. Preguntas abiertas: flujo real de autoridad, expediente que gobierna, criterios de admisión/rechazo y qué actos nunca delegaría.
