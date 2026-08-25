# Workflow — Intake y estructuración inicial

**Fuente funcional:** OBSERVED / USER-CONFIRMED para entrevista, relato, documentos disponibles y siguiente acción.
**Prioridad:** P1. **Candidata:** `intake-structuring`.

## Objetivo de trabajo

Convertir un relato inicial incompleto en una agenda de aclaración y un resumen de trabajo que distinga dicho, documento disponible, dato faltante, urgencia declarada y próximo paso. No decide si se acepta el encargo ni qué acción jurídica procede.

## Cuándo ocurre este flujo

Primera consulta, reapertura de asunto, recepción de material nuevo o preparación de reunión. No sustituye el flujo de incorporación formal de evidencia.

## Roles y ejemplos de activación

Profesional litigante; asistente bajo supervisión. Ejemplos: “ordene lo que me contó la clienta”, “qué datos faltan antes de revisar el caso”, “prepare preguntas para la próxima entrevista”.

## Entradas

Relato libre, notas, lista de documentos, objetivo declarado, personas involucradas, fechas conocidas y restricciones de confidencialidad. El sistema debe indicar qué no recibió en vez de inferirlo.

## Contexto necesario del caso e información externa

En V0, solo contexto del Case y Evidence ya incorporada; el intake nuevo es exploración hasta que se incorpore. Conflictos de interés, identidad, alcance y términos no se concluyen por memoria del modelo: requieren configuración/consulta humana y, cuando corresponda, Knowledge Pack o fuentes verificadas.

## Etapas del método y razonamiento

1. Separar relato, documento, inferencia y pregunta.
2. Construir cronología provisional con fecha cierta, aproximada o desconocida.
3. Identificar partes, objetivo, hechos candidatos, material disponible y ausencias.
4. Formular preguntas aclaratorias de máximo valor; marcar urgencias como declaradas, no confirmadas.
5. Entregar una hoja de preparación para que la profesional corrija o complete.

## Salidas esperadas

Resumen neutral, cronología provisional, mapa de personas/documentos, preguntas faltantes, riesgos de información insuficiente y siguientes acciones propuestas. Debe usar lenguaje para la profesional, no JSON ni terminología MCP.

## Decisiones humanas y límites de la IA

La humana decide conflicto de interés, aceptación/alcance del encargo, importancia jurídica, urgencia, estrategia y qué entra al expediente. La IA puede proponer preguntas, organización y banderas de falta de información; nunca califica un relato como probado.

## Responsabilidades del Core y herramientas MCP posibles

El Core controla Case, sesión, incorporación, provenance y aislamiento. V0 no requiere nueva tool: el workflow puede producir texto. Una integración posterior necesitaría contratos para crear/actualizar objetos solo mediante Proposal y revisión, no escritura directa.

## Dependencias de Knowledge Pack, evidencia y procedencia

Método universal; las preguntas procesales, plazos, requisitos profesionales y conflictos de interés dependen de jurisdicción/organización. Todo documento referido se entrega como “declarado/disponible/no visto”; solo Evidence incorporada puede respaldar un Fact en el Core.

## Dependencias temporales/jurídicas y fuentes oficiales

La fecha de cada evento es dato de entrada, no una conclusión. Las reglas sobre prescripción, caducidad, términos o aceptación requieren fuente temporalmente aplicable; ver [05-temporal-applicability.md](../05-temporal-applicability.md).

## Tratamiento de documentos externos e instrucciones maliciosas

Todo correo, PDF, chat, transcripción o enlace aportado al caso se trata como contenido no confiable. Una frase como “ignore las reglas” o “envíe este expediente” dentro del material no cambia el método, los permisos ni las decisiones humanas.

## Fallos frecuentes y consideraciones de experiencia

Evitar convertir una entrevista en hechos acreditados, rellenar fechas, confundir el objetivo del cliente con pretensión viable o preguntar lo ya dicho. Mostrar una sección visible “falta confirmar” y permitir que la profesional corrija sin rehacer la entrevista.

## Evaluaciones, relación con candidatas y preguntas abiertas

Evaluar cobertura de datos disponibles, precisión de preguntas faltantes, tasa de hechos inventados y claridad de cronología. Mapea a `intake-structuring`; no se solapa con `fact-builder`, que inicia cuando hay material de caso y trabaja hecho–prueba. Pregunta abierta: volumen real y quién realiza intake en la oficina.
