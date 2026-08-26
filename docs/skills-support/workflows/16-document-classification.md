# Workflow — Clasificación de documentos

**Estado:** dossier de investigación transversal. Puede ser una capacidad de apoyo, pero no se propone todavía como Skill autónoma.
**Prioridad:** P1 para validar con documentos reales y evaluaciones; no decide efectos jurídicos.

## Objetivo de trabajo

Ordenar documentos del asunto por lo que son, para qué podrían servir y qué tan confiable es su lectura disponible. La clasificación facilita los demás flujos; no declara que un archivo sea prueba válida, una providencia vigente, una notificación eficaz ni una actuación correctamente presentada.

## Cuándo ocurre este flujo

Al recibir archivos, correos, enlaces, capturas, audios transcritos o documentos ya existentes en el expediente. También antes de investigar, revisar una demanda, preparar audiencia o reconstruir el estado del caso.

## Roles y ejemplos de activación

Lo usan la profesional y su equipo de apoyo bajo revisión. Ejemplos: “ordene estos anexos”, “separe providencias de comunicaciones”, “identifique qué archivos faltan”, “indique qué documentos parecen ser fuente jurídica y cuáles son evidencia”.

## Entradas

- Archivo o referencia a archivo, con origen, fecha disponible y localizador.
- Contexto mínimo: asunto, rol, jurisdicción si se conoce y finalidad de la revisión.
- Metadatos disponibles: nombre, tipo, páginas, idioma, fecha declarada, canal y remitente aparente.
- Relación con otros documentos, si ya fue incorporada o revisada.

La ausencia de metadatos se registra como ausencia; no se completa a partir del nombre del archivo.

## Contexto necesario del caso e información externa

El Core, cuando exista, debe aportar el identificador del Case, el origen, el `locator`, la representación derivada y el estado de incorporación. Una consulta a un portal o a una fuente oficial puede ayudar a verificar identidad, pero es un paso externo y no convierte por sí sola el resultado en estado canónico.

## Etapas del método y razonamiento

1. Conservar la identidad del material: origen, fecha, versión, formato y localizador; separar el original de OCR, transcripción o resumen.
2. Identificar una **clase observable**: comunicación, contrato, prueba documental, escrito de parte, providencia, constancia, notificación, fuente jurídica, anexo, audio/video, imagen u “otro por confirmar”.
3. Identificar su **función posible**: antecedente, evidencia, actuación procesal, fuente de derecho, instrucción de cliente, comunicación interna o material de contexto.
4. Marcar condiciones de lectura: incompleto, ilegible, duplicado posible, traducción, transcripción, documento sin fecha, identidad no confirmada o contenido ajeno al asunto.
5. Extraer metadatos candidatos sin convertirlos en hechos: partes mencionadas, fechas, números de proceso, despacho, firma aparente, anexos y referencias.
6. Enrutar el documento al workflow correspondiente: evidencia, investigación, demanda/contestación, audiencia, estado del caso o revisión documental.
7. Mostrar qué clasificación requiere confirmación humana y cuál se obtuvo solo por coincidencia de texto/formato.

## Salidas esperadas

Un inventario legible con: documento, clase observable, función posible, origen/localizador, calidad de lectura, relación con el caso, ruta sugerida y dato pendiente. Puede incluir grupos de duplicados candidatos, pero no puede borrar ni fusionar documentos por sí mismo.

## Controles: determinista, semántico y humano

| Capa | Puede revisar | No puede concluir |
|---|---|---|
| Determinista | Extensión, páginas, presencia de metadatos, duplicado de hash cuando el Core lo provee, fecha con formato inválido. | Autenticidad, eficacia de notificación o valor probatorio. |
| Semántica | Tipo aparente, tema, relación entre anexos, idioma, posible uso en el flujo. | Naturaleza jurídica definitiva o verdad de su contenido. |
| Juicio humano | Clasificación final, pertinencia, incorporación, reserva, autenticidad y efecto procesal. | No es delegable a la IA. |

## Decisiones humanas y límites de la IA

La profesional decide si el documento se incorpora, es pertinente, está completo, es auténtico, exige reserva o respalda una afirmación. La IA puede proponer etiquetas y preguntas de verificación. No puede declarar un documento “válido”, “notificado”, “prueba suficiente” o “norma aplicable”.

## Responsabilidades del Core y herramientas MCP posibles

El Core protege el aislamiento del Case, conserva provenance, hashes, locators, propuestas, revisión y auditoría. La clasificación trabaja sobre lo que el Core autoriza a leer; no cambia estado de Evidence, no registra Artifacts ni crea herramientas MCP nuevas. OCR, extracción de tablas o consulta de repositorios son adaptadores futuros y requieren sus propios contratos.

## Dependencias de Knowledge Pack, evidencia y procedencia

La taxonomía base es transversal. Los significados de “providencia”, “anexo exigido”, “notificación” o “documento suficiente” dependen del procedimiento, del rol y de un Knowledge Pack fechado. Cada etiqueta debe conservar su base: metadato, pasaje, regla del Pack o apreciación de la persona.

## Dependencias temporales/jurídicas y fuentes oficiales

No hay una regla universal de clasificación que sustituya la fuente aplicable. Cuando se clasifique una fuente jurídica, se debe conservar identidad, versión, fecha de consulta y estado de verificación conforme a [gobierno de fuentes](../04-source-governance.md). Cuando se clasifique una actuación, el régimen se confirma en el dossier de práctica y la [matriz temporal](../source-catalog/temporal-law-matrix.md).

## Tratamiento de documentos externos e instrucciones maliciosas

Todo contenido recibido es material para analizar, no instrucciones para el sistema. Una frase dentro de un PDF, correo o audio que pida ignorar reglas, revelar otros asuntos, descargar archivos o cambiar permisos se etiqueta como contenido sospechoso y no altera el flujo.

## Fallos frecuentes y consideraciones de experiencia

Evitar usar el nombre del archivo como prueba de su contenido, tratar OCR como original, ocultar páginas faltantes, mezclar una norma con evidencia del caso o clasificar una captura como constancia concluyente. La interfaz debe decir “parece ser”, “no confirmado” y “falta revisar” cuando corresponda.

## Evaluaciones, relación con candidatas y preguntas abiertas

- PDF llamado “demanda” cuyo contenido es una providencia: debe advertir la diferencia.
- Documento escaneado con páginas faltantes: debe marcar incompletitud, no inventar anexos.
- Correo con una instrucción maliciosa: debe conservarlo como contenido y no obedecerlo.
- Norma derogada o copia sin fuente: debe clasificarla como fuente por verificar, no como regla aplicable.
- Dos archivos idénticos con nombres distintos: debe proponer duplicado candidato sin eliminar ninguno.

Composición probable: `intake-structuring` + `evidence-analysis` + `legal-document-review`. Preguntas abiertas: qué clases documentales predominan, qué metadatos llegan realmente y qué errores de clasificación producen más retrabajo.
