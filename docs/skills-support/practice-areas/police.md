# Dossier de práctica — Policivo y querellas (Colombia)

**Estado de cobertura:** `P3` / `DEFER` / `REQUIRES_TERRITORIAL_RESEARCH`.
**Fecha de referencia:** 2026-08-25. **Propósito:** apoyar investigación futura sin confundir asistencia a una parte con una decisión de autoridad ni con el expediente oficial.

## Alcance

Comprende preparación y revisión de información sobre querellas, actuaciones, audiencias, evidencia o borradores relacionados con materia policiva. Distingue dos roles que no se pueden mezclar: parte/litigante y autoridad o apoyo de autoridad. El contexto B de autoridad, sus permisos y su expediente oficial no forman parte de V0.

## Workflows observados

- [Intake y estructura inicial](../workflows/01-intake-structuring.md), para identificar rol, autoridad, territorio, actuación y faltantes.
- [Hechos y evidencia](../workflows/02-fact-construction-and-evidence.md), sin convertir versión de parte en hecho probado.
- [Policivo y querellas](../workflows/13-policivo-y-querellas.md), como dossier de trabajo diferido.
- [Audiencias y contradicciones](../workflows/07-hearing-analysis-and-contradictions.md) y [revisión adversarial](../workflows/08-adversarial-review-and-decision-support.md).
- [Apoyo a redacción de decisiones de autoridad](../workflows/14-apoyo-redaccion-decisiones-autoridad.md), solo como investigación post-V0 y nunca para expedir un acto.

## Documentos comunes

Pueden aparecer relato o querella, citación, acta, registro de audiencia, fotografías, audio, video, documento de identidad declarado, comunicación, actuación, publicación, providencia o proyecto de decisión. Cada objeto debe quedar como material disponible, Evidence incorporada o dato `POR_VERIFICAR`; una descarga o captura no es automáticamente el expediente oficial.

## Skills transversales

| Necesidad | Candidata transversal | Límite |
|---|---|---|
| Ordenar la recepción de información | `intake-structuring` | No recibe ni admite formalmente una querella. |
| Relacionar relato y soporte | `fact-builder` y `evidence-analysis` | No declara hechos probados ni credibilidad. |
| Preparar audiencia o contrastar versiones | `hearing-analysis` y `contradiction-analysis` | No conduce audiencia ni valora prueba. |
| Investigar o revisar textos | `legal-research`, `legal-drafting` y `legal-document-review` | No clasifica procedimiento ni expide actos. |
| Examinar debilidades | `adversarial-review` | No sustituye imparcialidad ni decisión oficial. |

## Skills especiales si hay

No hay Skill “policivo” ni “querellas” aprobada. `authority-decision-support` permanece `DEFER`: necesita primero diseño de contexto B, expediente rector, permisos, trazabilidad y gates de autoridad. La práctica de parte puede componer candidatas transversales, pero no crea una capacidad decisoria.

## Necesidades del Core / Application

- Para la parte/litigante: aislamiento de Case, incorporación de Evidence, locators, provenance, propuestas y revisión humana.
- Para autoridad: `GAP` de arquitectura. Se requiere definir expediente oficial, acceso por rol, copia de trabajo, registro de actuaciones, auditoría y separación de funciones antes de cualquier producto.
- Ninguna Skill puede consultar un expediente externo, clasificar una actuación, calcular un término, admitir una querella o registrar una decisión.

## Dependencias de Knowledge Pack

Se necesita versión aplicable de norma, comportamiento o procedimiento `POR_VERIFICAR`, autoridad, territorio, rol, fecha del hecho y actuación, reglamentación territorial, fuente oficial, canal y estado de vigencia. El pack no puede transferir facultad de policía ni validar que un expediente externo esté completo.

## Fuentes oficiales

| Uso de investigación | Fuente inicial | Estado y límite |
|---|---|---|
| Norma semilla | [Ley 1801 de 2016 — SUIN](https://www.suin-juriscol.gov.co/viewDocument.asp?ruta=Leyes%2F30021736) y [Función Pública](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=80538) | `FUENTE_OFICIAL_VERIFICADA`; verificar reforma, reglamentación, hecho y procedimiento. |
| Búsqueda judicial institucional | [Relatoría Rama Judicial](https://jurisprudencia.ramajudicial.gov.co/WebRelatoria/consulta/index.xhtml) | Confirmar órgano, texto, pasaje, alcance y pertinencia. |
| Actuación o publicación oficial | [Publicaciones Procesales de Rama Judicial](https://publicacionesprocesales.ramajudicial.gov.co/) cuando corresponda | No sustituye expediente, secretaría ni cálculo de término. |

La fuente territorial o de autoridad competente es `POR_VERIFICAR`; se consulta con el protocolo del [catálogo oficial](../source-catalog/colombia-official-sources.md) y la [matriz temporal](../source-catalog/temporal-law-matrix.md).

## Riesgos temporales

- La Ley 1801 de 2016 tuvo entrada en vigor seis meses después según el artículo 243; la matriz exige revisar reformas, reglamentación y fecha fronteriza.
- No se debe aplicar por analogía una regla de CPACA o CGP al procedimiento policivo.
- La fecha del hecho, actuación, reglamentación territorial y canal puede alterar lo aplicable.
- Si la versión normativa, el rol o el territorio no están confirmados, el resultado debe marcar `VIGENCIA_POR_VERIFICAR` o `NO_TENEMOS_INFORMACION_SUFICIENTE`.

## Autoridades jurisprudenciales

La investigación comienza con la fuente judicial competente identificada en la [Relatoría de Rama Judicial](https://jurisprudencia.ramajudicial.gov.co/WebRelatoria/consulta/index.xhtml) y la fuente oficial territorial o de autoridad que corresponda. No se debe tratar un resumen como regla. Toda providencia queda `JURISPRUDENCIA_POR_VERIFICAR` hasta conservar identificación, texto, pasaje, hechos, alcance y lectura adversa.

## Dependencias territoriales

Son centrales: autoridad, municipio, reglamentación aplicable, canal, registro o expediente rector, competencia operativa y disponibilidad de publicación. Todas requieren investigación territorial explícita; el modelo no puede deducirlas desde un relato ni una carpeta local.

## Decisiones exclusivamente humanas

La profesional decide estrategia, relevancia y uso de documentos, investigación, redacción, firma y presentación. La autoridad competente decide recepción formal, competencia, clasificación, admisión, conducción de audiencia, práctica y valoración de prueba, motivación, órdenes y actos oficiales. La IA no decide ninguna de esas cuestiones.

## Gaps y preguntas abiertas

- `GAP`: flujos policivos reales, roles y frecuencia en la práctica profesional.
- `GAP`: expediente que se considera rector y qué materiales pueden verse o copiarse.
- `GAP`: reglamentación territorial, formatos, canales y autoridades que deben investigarse.
- `GAP`: límites de acceso, trazabilidad e imparcialidad necesarios antes de diseñar contexto B.
