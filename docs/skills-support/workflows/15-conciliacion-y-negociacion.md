# Workflow — Preparación de conciliación y negociación

**Estado:** P3 — `NEEDS_DISCOVERY` / `DEFER`. La negociación estratégica no se modela como verdad jurídica ni como decisión autónoma del modelo.
**Jurisdiction:** Colombia cuando se use la Ley 2220 de 2022; el método de ordenar posiciones e intereses es transversal.
**Fuente seed:** Ley 2220 de 2022 y normativa aplicable por materia, con versión y temporalidad verificadas para el Case.

## Objetivo de trabajo

Preparar una conversación o revisión humana de conciliación/negociación mediante un mapa trazable de posiciones, intereses declarados, hechos, evidencia, incertidumbres, riesgos, alternativas y no negociables definidos por la profesional. No recomienda aceptar, rechazar, ofrecer ni cerrar un acuerdo.

## Cuándo ocurre este workflow

Antes de una reunión, audiencia de conciliación, intercambio de propuestas, análisis de una oferta o preparación de comunicación. No se usa para enviar propuestas, acceder a calendarios/correo, aceptar condiciones, generar obligaciones ni registrar un acuerdo.

## Roles de usuario

- Profesional litigante o asesora que prepara una conversación o revisa una propuesta.
- Cliente o representante solo a través de contenido autorizado por la profesional.
- Facilitador/autoridad cuando corresponda, sin que el modelo sustituya su función.

## Ejemplos de activación

- “Organice posiciones, intereses y evidencia antes de esta reunión.”
- “Separe lo que sabemos de lo que debemos confirmar antes de discutir una alternativa.”
- “Prepare preguntas para revisar esta propuesta de acuerdo con la clienta.”
- “Compare esta oferta con los hechos, documentos y riesgos que ya identificamos.”

## Entradas

Objetivo de la reunión, participantes/roles declarados, posiciones e intereses expresados, límites/no negociables indicados por la profesional, Facts/Evidence disponibles, propuestas recibidas, documentos, fechas, restricciones de confidencialidad y fuentes jurídicas cuando se invoquen efectos legales. El silencio o una omisión no se interpreta como consentimiento.

## Contexto canónico requerido

Solo contexto mínimo del Case autorizado, Evidence incorporada y Facts/propuestas revisados. Las alternativas de negociación, preferencias y borradores no pasan a estado canónico por aparecer en una salida de IA; necesitan el canal y el modelo de datos que una futura capacidad defina.

## Información externa posiblemente necesaria

Texto oficial aplicable, requisitos del mecanismo de conciliación según área, fuente/canal de la convocatoria y reglas organizacionales. Correo, calendario, plataformas de reunión, firma y radicación son connectors futuros sujetos a policy y autorización, no extensiones implícitas de este workflow.

## Método / etapas de razonamiento

1. Definir la finalidad de la preparación y quién tomará las decisiones.
2. Separar hechos/evidencia, posiciones, intereses declarados, inferencias, riesgos y datos faltantes.
3. Mapear cada propuesta a sus condiciones, soporte disponible, incertidumbres y preguntas de revisión.
4. Identificar documentación, fuente o decisión humana necesaria antes de discutir una alternativa.
5. Organizar alternativas sin calificarlas como convenientes, válidas, aceptables o obligatorias.
6. Entregar un brief para revisión humana y una comunicación/borrador solo si la profesional lo solicita.

## Salidas esperadas

Brief con posiciones, intereses, evidencia, riesgos declarados, alternativas, no negociables, preguntas y faltantes; opcionalmente un borrador de comunicación para revisión. Las salidas indican de quién proviene cada posición y qué parte no se ha confirmado.

## Decisiones humanas

La profesional y la persona con autoridad deciden estrategia, revelación, rango de negociación, oferta, aceptación, transacción, concesiones, firma y comunicación. El conciliador o autoridad desempeña su función conforme al régimen aplicable; ninguna IA sustituye ese juicio.

## Lo que la IA puede proponer

Organización de información, preguntas, comparaciones entre propuesta y evidencia, lista de condiciones, riesgos a explorar, huecos documentales y redacción tentativa que conserve incertidumbres y decisiones pendientes.

## Lo que la IA no debe decidir

No puede establecer la verdad jurídica de una posición, aconsejar una aceptación como determinación final, inferir consentimiento, evaluar vinculancia/validez de un acuerdo, comprometer a una parte, enviar un mensaje, firmar ni registrar el cierre de una conciliación.

## Responsabilidades del Core / Application

El Core protege aislamiento, provenance, Evidence, propuestas y auditoría. Un eventual registro de oferta, acuerdo, plazo, estado procesal, autorización o comunicación requiere diseño de dominio/Application y revisión humana; no existe en V0 y no se crea desde este dossier.

## Herramientas MCP potencialmente requeridas

No hay herramienta MCP adicional en V0. Leer contexto y evidencia ya incorporados no habilita envío, calendario, firma, radicación, cálculo de efectos o commit de un acuerdo. Cualquier integración futura debe tener contrato, política y límites explícitos.

## Dependencias de Knowledge Pack

Alta cuando se presenten reglas o efectos jurídicos: materia, jurisdicción, fecha, mecanismo, autoridad y fuente oficial. Para Colombia, Ley 2220 de 2022 es fuente seed, no una checklist permanente ni una garantía de que el mecanismo aplica al Case.

## Requisitos de evidencia y provenance

Los hechos y documentos usados para un brief deben distinguir Evidence incorporada, declaración de parte, propuesta externa e inferencia de IA. Las propuestas recibidas no prueban aceptación ni obligación. Toda cita jurídica conserva fuente, fecha, versión y estado; una fuente externa no se convierte en Evidence sin incorporación autorizada.

## Dependencias temporales y fuentes oficiales

La aplicabilidad depende de materia, mecanismo, fecha del Case, reformas y transición. Consultar `../source-catalog/temporal-law-matrix.md` y `../04-source-governance.md`; confirmar texto/pasaje oficial y no afirmar efectos, términos o requisitos sin revisión humana.

## Manejo de documentos externos e inyección de instrucciones

Ofertas, borradores de acuerdo, correos, chats y anexos son contenido no confiable. Una instrucción embebida no puede modificar el alcance del análisis, autorizar contacto, revelar información ni cambiar los límites de la Skill. El Core/host conserva controles técnicos de acceso y aislamiento.

## UX y fallos frecuentes

Mostrar claramente “posición declarada”, “interés expresado”, “evidencia disponible”, “riesgo a revisar” y “decisión de la profesional”. Evitar tono coercitivo, promesas sobre resultado, confundir una alternativa con acuerdo, esconder incertidumbre o usar jerga técnica frente al cliente.

## Evals candidatos

- Caso sintético con dos posiciones y evidencia parcial: distinguir hecho, interés y alegación.
- Oferta con condición ambigua: devolver preguntas, no una aceptación implícita.
- Fuente jurídica no verificada: tratarla como pendiente de comprobación.
- Material de otra parte con prompt injection: conservarlo como contenido.
- Solicitud de enviar/aceptar: abstención y remisión a decisión humana.

## Mapeo de candidata y prioridad

No crear `conciliation-negotiation` como Skill todavía. Puede reutilizar `fact-builder`, `evidence-analysis`, `legal-research`, `legal-drafting`, `legal-document-review` y comunicación como recurso, pero requiere discovery de frecuencia, áreas, protocolos y límites de delegación. P3 / `NEEDS_DISCOVERY`.

## Preguntas abiertas

- En qué materias y con qué frecuencia concilia o negocia la profesional.
- Qué información jamás compartiría antes de una reunión y quién puede autorizarla.
- Qué criterios usa para definir no negociables, alternativas y revisión del cliente.
- Qué canales, formatos y constancias utiliza, y qué integración sería aceptable.
