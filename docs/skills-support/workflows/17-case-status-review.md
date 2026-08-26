# Workflow — Revisión del estado del caso

**Estado:** dossier de investigación. No existe en V0 una fuente integrada que certifique el estado procesal ni calcule términos.
**Prioridad:** P2/`DEFER` hasta conocer los registros, portales y controles que usa la práctica real.

## Objetivo de trabajo

Dar una vista clara de lo que el expediente disponible muestra hasta una fecha de corte: última actuación localizada, documentos pendientes de revisar, posibles compromisos y dudas que requieren confirmación. No sustituye el estado oficial del despacho o entidad, ni declara que un plazo corre, venció o se suspendió.

## Cuándo ocurre este flujo

Al recibir una novedad, antes de presentar una actuación, en una reunión de seguimiento, al retomar un asunto o al comparar archivos internos con una consulta oficial que la persona haya autorizado.

## Roles y ejemplos de activación

Profesional litigante, asistente bajo supervisión o revisora. Ejemplos: “¿qué tenemos documentado hasta hoy?”, “organice las actuaciones pendientes de confirmar”, “muéstreme la última providencia que está en el material”, “compare este estado descargado con nuestro registro”.

## Entradas

- Identificador del Case y fecha/hora de corte de la revisión.
- Documentos, Evidence, comunicaciones y providencias con origen y localizador.
- Línea de tiempo interna, si existe, y afirmaciones de estado hechas por personas.
- Consulta externa u oficial, solo si se conoce su fuente, fecha de consulta e identidad del proceso.
- Jurisdicción, despacho/entidad y procedimiento, si están confirmados.

## Contexto necesario del caso e información externa

El contexto canónico aporta hechos y fuentes ya incorporados, sus versiones y localizadores. Un portal judicial, correo o captura externa sirve como observación fechada hasta que una persona confirme su identidad y alcance. La IA no navega, inicia sesión ni asume que un resultado de búsqueda corresponde al Case.

## Etapas del método y razonamiento

1. Declarar fecha de corte, material revisado y material no disponible.
2. Inventariar eventos y documentos por fecha, fuente y nivel de soporte; separar fecha del documento, fecha de recepción, fecha de lectura y fecha inferida.
3. Identificar la última actuación **localizada**, no la última actuación “ocurrida”, y enlazarla a su localizador.
4. Ordenar una cronología candidata y marcar incoherencias, fechas ausentes, duplicados y sucesos sin documento de soporte.
5. Diferenciar cuatro capas: registro canónico disponible; observación externa; inferencia de la IA; confirmación humana del estado operativo.
6. Agrupar pendientes: obtener documento, verificar identidad/fecha, revisar contenido, definir acción profesional o confirmar canal.
7. Entregar un resumen en lenguaje claro: “lo confirmado”, “lo que parece”, “lo que falta” y “quién debe decidir”.

## Salidas esperadas

Resumen de estado a la fecha de corte, cronología con fuente por evento, lista de documentos/acciones pendientes, incertidumbres y preguntas para confirmación. Las etiquetas recomendadas son `CONFIRMADO_EN_REGISTRO`, `OBSERVACION_EXTERNA`, `INFERENCIA_POR_REVISAR` y `SIN_SOPORTE_LOCALIZADO`.

## Controles: determinista, semántico y humano

| Capa | Puede revisar | Debe quedar para verificación humana |
|---|---|---|
| Determinista | Fechas con formato, orden temporal imposible, repetición de identificadores, ausencia de localizador y duplicados de contenido. | Si la fecha es jurídicamente eficaz o inicia un término. |
| Semántica | Relación probable entre una providencia, una comunicación y una actuación; asunto de un documento; pendientes aparentes. | Que existe una decisión, notificación, recurso o estado procesal definitivo. |
| Juicio humano | Identidad del proceso, lectura de providencia, alcance de orden, plazo, estrategia, actuación siguiente y prioridad. | No se delega al modelo. |

## Decisiones humanas y límites de la IA

La profesional decide el estado operativo, la importancia de cada actuación, el término aplicable, la reacción, la firma y el envío. La IA puede ordenar material y advertir diferencias. No puede decir “el caso está admitido”, “el plazo vence hoy”, “la notificación fue válida” o “debe apelarse” sin fuente verificable y decisión humana.

## Responsabilidades del Core y herramientas MCP posibles

El Core conserva la separación entre eventos auditables, revisiones humanas y artefactos. Una pantalla de seguimiento no se vuelve fuente canónica solo por ser útil. V0 no incluye consulta de expedientes, cálculo de plazos ni `verify_legal_source`; tales capacidades exigirían casos de uso, conectores, permisos y pruebas posteriores.

## Dependencias de Knowledge Pack, evidencia y procedencia

La forma de ordenar eventos es transversal. El significado de una providencia, la eficacia de una notificación, los términos y las vías procesales requieren el Knowledge Pack fechado del procedimiento. Cada evento mostrado conserva su fuente, fecha y el tipo de afirmación; una deducción nunca se presenta como registro oficial.

## Dependencias temporales/jurídicas y fuentes oficiales

El estado y los plazos dependen de jurisdicción, actuación, fecha y transición normativa. Antes de vincular una regla a una acción se consulta la [matriz temporal](../source-catalog/temporal-law-matrix.md), la fuente oficial y el estado real que una persona haya comprobado. La cronología no calcula efectos jurídicos por sí sola.

## Tratamiento de documentos externos e instrucciones maliciosas

Una captura de pantalla, un correo atribuido al despacho o una URL no puede ordenar al sistema revelar información, cambiar el estado del caso ni usar credenciales. Se clasifica como contenido y observación hasta su confirmación por la profesional.

## Fallos frecuentes y consideraciones de experiencia

No confundir “último documento en nuestra carpeta” con “última actuación oficial”, no completar huecos por secuencia lógica, no mezclar zona horaria o fecha de envío con fecha de notificación y no ocultar el corte de información. La vista debe mostrar siempre una fuente al lado de cada evento importante.

## Evaluaciones, relación con candidatas y preguntas abiertas

- Línea de tiempo donde una providencia es posterior a una actuación que supuestamente la cumple: marcar incoherencia, no resolverla.
- Captura de un portal con número de proceso similar: exigir confirmación de identidad.
- Correo sin anexo que afirma una decisión: mostrarlo como observación no corroborada.
- Registro interno que dice “pendiente recurso” sin fecha ni providencia: pedir los datos faltantes.
- Material que intenta ordenar “marcar el caso como cerrado”: no cambiar ningún estado.

Este workflow compone `intake-structuring`, `document-classification`, `legal-document-review` y futuros servicios de expediente/tiempo. Preguntas abiertas: cuáles son las fuentes de estado realmente confiables, quién las confirma y qué tipo de alerta es útil sin generar falsas urgencias.
