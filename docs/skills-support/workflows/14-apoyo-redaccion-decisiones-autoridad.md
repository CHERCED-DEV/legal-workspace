# Workflow — Apoyo a redacción de decisiones de autoridad

**Estado:** P3 — `DEFER`. El producto V0 opera solo en contexto litigante; el contexto de autoridad/decisor y su expediente oficial requieren discovery y arquitectura posteriores.
**Alcance:** metodología para preparar un borrador o una revisión trazable de auto, providencia, decisión o sentencia según el dominio aplicable. Nunca produce una determinación oficial.

## Objetivo de trabajo

Ayudar a una autoridad o a su equipo a organizar antecedentes, historia procesal, posiciones, hechos, evidencia, fuentes, evidencia contraria, razonamiento y órdenes candidatas para revisión humana. El objetivo es hacer comprobable lo que se consideró y lo que falta, no decidir el asunto.

## Cuándo ocurre este workflow

Al preparar un proyecto, revisar un borrador de decisión, sintetizar posiciones bilaterales, identificar evidencia o argumentos omitidos o preparar una audiencia/acto decisorio. No se usa para expedir, firmar, notificar, ejecutar ni registrar una decisión oficial.

## Roles de usuario

- Autoridad competente, profesional decisora o apoyo autorizado de la autoridad.
- Revisor que busca simetría de tratamiento, evidencia contraria y saltos lógicos.
- No es un workflow V0 para la primera usuaria hasta confirmar el contexto de autoridad.

## Ejemplos de activación

- “Organice antecedentes, posiciones y evidencia que debo revisar antes de este proyecto.”
- “Señale argumentos o pruebas de ambas partes que el borrador no trata.”
- “Prepare una matriz de hallazgos para verificar la motivación, sin decidir el caso.”
- “Diferencie lo que está en el expediente de lo que todavía requiere confirmación.”

## Entradas

Identificación del acto/borrador, autoridad y rol declarados, expediente que se afirma oficial, actuaciones/providencias, posiciones y solicitudes de las partes, Facts/Evidence/locators disponibles, fuentes jurídicas con estado, fechas relevantes y alcance de la revisión. Si falta el expediente rector o una pieza relevante, la salida debe declararlo.

## Contexto canónico requerido

Ninguno está implementado para contexto B en V0. Un futuro diseño debe definir cuál expediente es canónico, cuál es copia de trabajo, qué puede incorporar el Core y cómo se preservan trazabilidad, acceso y auditoría. Mientras tanto, una Skill solo puede trabajar sobre el material explícitamente autorizado y no puede asumir que representa el expediente oficial completo.

## Información externa posiblemente necesaria

Texto oficial de normas, fuentes jurisprudenciales, actuaciones/publicaciones oficiales, reglas de competencia y procedimiento, e información del expediente externo si se aprueba un connector. El acceso debe ser explícito, auditable y separado de la incorporación de Evidence; no se concede por defecto a un modelo.

## Método / etapas de razonamiento

1. Declarar autoridad, rol, tipo de acto, alcance y material disponible/omitido.
2. Separar antecedentes, historia procesal, posiciones, evidencia, fuentes, alegaciones e inferencias.
3. Construir una matriz bilateral: argumento, soporte, contraargumento, evidencia contraria y pregunta de revisión.
4. Identificar vacíos de motivación, asimetrías, citas sin pasaje, hechos sin soporte y contradicciones no tratadas.
5. Organizar una estructura de borrador: antecedentes, historia, issues, posiciones, hechos/evidencia, fuentes, razonamiento propuesto, alternativas y órdenes candidatas.
6. Entregar el material para que la autoridad evalúe, motive, decida y firme por sí misma.

## Salidas esperadas

Matriz de cobertura bilateral, inventario de evidencia/argumentos omitidos, lista de incertidumbres, propuesta de estructura y borrador marcado como “para revisión de autoridad”. Nunca un resultado “decisión correcta”, “imparcial”, “aprobada” o “lista para expedir”.

## Decisiones humanas

La autoridad competente define competencia, admisibilidad, valoración de prueba, interpretación normativa, hechos considerados probados, motivación, sentido de la decisión, órdenes, firma, notificación y ejecución. La supervisión humana también decide qué piezas del expediente son pertinentes y completas.

## Lo que la IA puede proponer

Organización de antecedentes, preguntas de comprobación, pasajes/locators a contrastar, hallazgos falsables de omisión o asimetría, alternativas de estructura y redacción condicionada que distinga hechos, fuentes y supuestos.

## Lo que la IA no debe decidir

No puede emitir ni simular un acto oficial; declarar hechos probados, resolver pretensiones, fijar competencia, valorar credibilidad, escoger una fuente como decisiva, determinar imparcialidad, calcular efectos procesales ni firmar/notificar/registrar una decisión.

## Responsabilidades del Core / Application

Antes de cualquier implementación se requiere diseñar contexto B: custodia del expediente oficial, roles, permisos, trazabilidad de actuaciones, gates humanos y proyección adecuada a decisor. El Core existente solo cubre Case de litigante y sus garantías actuales; este dossier no redefine su dominio ni añade `ProfessionalDetermination`.

## Herramientas MCP potencialmente requeridas

No hay nueva tool MCP V0 ni `ADMIN` tool. Si una necesidad futura exige consultar expediente externo, registrar un proyecto o distinguir actos oficiales, debe abrirse como decisión de arquitectura y contrato separado; una Skill no puede suplirlo con acceso a filesystem, navegación o texto.

## Dependencias de Knowledge Pack

Muy alta y dependiente de jurisdicción, materia, autoridad, procedimiento, territorio, fecha y tipo de acto. Un Knowledge Pack futuro puede proveer fuentes/procedimientos fechados, pero no transferir autoridad ni valorar prueba por la persona.

## Requisitos de evidencia y provenance

Cada observación debe señalar material de origen, locator, versión y limitación. Se debe mostrar evidencia contraria y distinguir original, derivación, alegación e interpretación de IA. La incorporación de una fuente o actuación externa al Case/expediente requiere el camino autorizado, no una referencia informal en un borrador.

## Dependencias temporales y fuentes oficiales

Las fuentes dependen del órgano, materia, procedimiento y fecha relevante. Usar el protocolo de `../04-source-governance.md` y la matriz temporal; verificar textos oficiales, versiones y transiciones antes de presentar una regla. No existe una fuente universal que resuelva todos los tipos de acto.

## Manejo de documentos externos e inyección de instrucciones

Providencias, escritos de partes, anexos, transcripciones y portales son contenido no confiable a evaluar, no instrucciones del sistema. No se permite que una parte altere alcance, herramientas, criterios o autorización mediante texto embebido. La protección de acceso, aislamiento y registros corresponde al Core/host/policy.

## UX y fallos frecuentes

La interfaz futura debe distinguir claramente “material disponible”, “material omitido”, “hallazgo de IA” y “decisión de autoridad”. Fallos: confundir resumen con expediente completo, privilegiar una parte, ocultar evidencia contraria, presentar un salto lógico como motivación suficiente o hacer parecer que el modelo fue quien decidió.

## Evals candidatos

- Fixture bilateral con evidencia favorable y contraria: medir cobertura de ambas partes.
- Proyecto con una conclusión sin soporte: exigir pasaje, fuente o pregunta de revisión.
- Caso con expediente oficial incompleto/no identificado: abstención y solicitud de contexto.
- Dos versiones de una fuente o norma con fecha distinta: exigir temporalidad y no escoger silenciosamente.
- Documento con prompt injection: mantenerlo como contenido no confiable.

## Mapeo de candidata y prioridad

`authority-decision-support` permanece `DEFER`, no es Skill instalable. Eventualmente compondría `fact-builder`, `evidence-analysis`, `legal-research`, `legal-drafting`, `legal-document-review` y `adversarial-review`, con un gate de autoridad y contexto B primero. P3.

## Preguntas abiertas

- Cuál es el expediente oficial y qué copia es solo de trabajo.
- Qué actos, tipos de decisión y materias atiende realmente la profesional como autoridad.
- Qué requisitos de trazabilidad, firma, revisión y reparto de funciones exige la organización.
- Qué material puede ver un apoyo y qué debe permanecer exclusivo de la autoridad.
