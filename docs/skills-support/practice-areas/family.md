# Dossier de práctica — Familia (Colombia)

**Estado de cobertura:** `PARTIALLY_COVERED` / `REQUIRES_CASE_SPECIFIC_RESEARCH`.
**Fecha de referencia:** 2026-08-25. **Propósito:** mapear necesidades de investigación y diseño futuro, sin convertirlas en reglas automáticas ni alterar el Core.

## Alcance

Este dossier reúne trabajo de familia que pueda requerir organización de información, evidencia, investigación, redacción, revisión, audiencia o comunicación. No reemplaza el análisis del asunto, la identificación de personas sujetas a especial protección, la representación, las medidas aplicables ni la autoridad competente. Esos puntos son `POR_VERIFICAR` en cada Case.

## Workflows observados

- [Intake y estructura inicial](../workflows/01-intake-structuring.md), con especial cuidado en identidad declarada, documentos sensibles y faltantes.
- [Hechos y evidencia](../workflows/02-fact-construction-and-evidence.md), sin presentar una alegación familiar como hecho acreditado.
- [Investigación y problemas jurídicos](../workflows/03-legal-research-and-issue-spotting.md), usando fuentes fechadas y pertinentes al asunto.
- [Redacción y revisión](../workflows/04-legal-drafting-and-document-review.md), [actuaciones procesales](../workflows/05-procedural-submissions-and-resources.md) y [audiencias](../workflows/07-hearing-analysis-and-contradictions.md).
- [Comunicación y conciliación](../workflows/09-client-communication-and-conciliation.md) y [conciliación/negociación](../workflows/15-conciliacion-y-negociacion.md), solo como preparación humana y no como decisión de acuerdo.

## Documentos comunes

Según el asunto y la autoridad, pueden aparecer escritos iniciales o de respuesta, documentos de identificación o registro, comunicaciones, actas, informes, soportes económicos, prueba documental, informes profesionales, providencias y borradores de acuerdo. Esta lista es orientativa: no declara que un documento sea exigible, suficiente o admisible.

## Skills transversales

| Necesidad | Candidata transversal | Límite |
|---|---|---|
| Estructurar un relato sensible | `intake-structuring` | No decide representación ni protección aplicable. |
| Construir matriz de soporte | `fact-builder` y `evidence-analysis` | No determina credibilidad, interés superior ni prueba. |
| Investigar y delimitar preguntas | `legal-issue-spotting` y `legal-research` | No convierte una sentencia en respuesta universal. |
| Preparar y revisar documentos | `legal-drafting` y `legal-document-review` | No valida requisitos ni autoriza presentación. |
| Contrastar versiones y riesgos | `contradiction-analysis` y `adversarial-review` | No resuelve conflictos familiares. |

## Skills especiales si hay

**No hay una Skill genérica de “familia”.** Las variaciones de procedimiento, protección, reserva, autoridad y materia deben ir en un Knowledge Pack fechado y en flujos observados. Una Skill especial solo sería candidata si se confirma un método propio y evaluable; hoy es `GAP`.

## Necesidades del Core / Application

- Aislamiento estricto de Case, evidencia incorporada, locators, provenance y gates de revisión.
- Separar documento disponible, alegación, evidencia e inferencia; no mezclar información de personas o Cases distintos.
- La necesidad de visibilidad por rol, manejo reforzado de datos sensibles, conservación o expediente oficial es un requisito de producto/arquitectura futuro `POR_VERIFICAR`; este dossier no lo implementa.
- No calcular términos, asumir representación, consultar registros o radicar mediante una Skill.

## Dependencias de Knowledge Pack

El pack futuro debe declarar materia específica, personas y roles relevantes solo en el alcance autorizado, fecha, procedimiento, autoridad, fuente oficial, regla material y procesal aplicable, reserva/confidencialidad que corresponda y estado de vigencia. Si falta alguno, el resultado debe indicar `NO_TENEMOS_INFORMACION_SUFICIENTE`.

## Fuentes oficiales

| Uso de investigación | Fuente inicial | Estado y límite |
|---|---|---|
| Procedimiento cuando corresponda | [Ley 1564 de 2012 — SUIN](https://www.suin-juriscol.gov.co/viewDocument.asp?id=1683572) y [PDF de Rama Judicial](https://www.ramajudicial.gov.co/documents/6342549/27434411/Ley_1564_2012.pdf/3dc3d888-db54-4fe5-8173-8911d110efca) | `FUENTE_OFICIAL_VERIFICADA`; confirmar artículo, especialidad y versión. |
| Canales digitales cuando proceda | [Ley 2213 de 2022 — Secretaría del Senado](https://www.secretariasenado.gov.co/senado/basedoc/ley_2213_2022.html) | `POR_VERIFICAR` por actuación; no sirve como checklist universal. |
| Jurisprudencia | [Corte Suprema de Justicia](https://cortesuprema.gov.co/corte/index.php/jurisprudencia/) y [Relatoría Rama Judicial](https://jurisprudencia.ramajudicial.gov.co/WebRelatoria/consulta/index.xhtml) | Revisar órgano, texto completo, pasaje y contexto. |

La fuente material o de protección aplicable se identifica por tipo de asunto y queda `POR_VERIFICAR`; no se inventa una fuente única de familia. Consultar el [catálogo oficial](../source-catalog/colombia-official-sources.md) y la [matriz temporal](../source-catalog/temporal-law-matrix.md).

## Riesgos temporales

- La vigencia escalonada del CGP y sus reformas deben verificarse por norma y fecha.
- La fecha del hecho, actuación, medida, comunicación o inicio de proceso puede ser relevante y no se presume.
- Una regla de canal digital o una plantilla anterior no demuestra la aplicabilidad presente.
- Regímenes especiales y cambios jurisprudenciales requieren `VIGENCIA_POR_VERIFICAR` y revisión profesional.

## Autoridades jurisprudenciales

La búsqueda inicia en la [Corte Suprema de Justicia](https://cortesuprema.gov.co/corte/index.php/jurisprudencia/) y la [Relatoría de Rama Judicial](https://jurisprudencia.ramajudicial.gov.co/WebRelatoria/consulta/index.xhtml), sin excluir la autoridad que corresponda al problema concreto. Toda cita debe conservar corporación, sala, fecha, identificador, texto y pasaje; de lo contrario queda `JURISPRUDENCIA_POR_VERIFICAR`.

## Dependencias territoriales

Autoridad, despacho, municipio, ruta de protección, canal y reglas operativas locales son `REQUIRES_TERRITORIAL_RESEARCH`. La herramienta no debe deducirlos por domicilio, relato o formato de archivo.

## Decisiones exclusivamente humanas

La profesional decide estrategia, reserva de información, pertinencia de una fuente, relevancia y valoración de evidencia, comunicaciones, negociación y presentación. La autoridad competente decide competencia, medidas, práctica y valoración de prueba, protección, providencias y actos oficiales. La IA no decide intereses, representación, cuidado, acuerdos ni resultado.

## Gaps y preguntas abiertas

- `GAP`: materias de familia atendidas realmente y sus documentos repetitivos.
- `GAP`: protocolo profesional para información sensible, menores u otros sujetos protegidos.
- `GAP`: fuentes materiales y jurisprudenciales que deben integrar cada asunto.
- `GAP`: criterios humanos para detectar urgencia, representación y escalamiento sin automatizarlos.
