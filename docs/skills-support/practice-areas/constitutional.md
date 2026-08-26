# Dossier de práctica — Constitucional y tutela (Colombia)

**Estado de cobertura:** `P3` / `DEFER` / `REQUIRES_CASE_SPECIFIC_RESEARCH`.
**Fecha de referencia:** 2026-08-25. **Propósito:** organizar investigación, evidencia y borradores para revisión profesional; no decide procedencia, urgencia, vulneración, orden, término ni resultado.

## Alcance

Este dossier cubre trabajo constitucional, con énfasis en tutela, cuando se prepara, revisa o responde información y documentos. La procedencia y los matices jurisprudenciales no se reducen a un checklist. Un resultado de búsqueda no prueba por sí solo una regla, su ratio ni su pertinencia para el Case.

## Workflows observados

- [Intake y estructura inicial](../workflows/01-intake-structuring.md) y [hechos/evidencia](../workflows/02-fact-construction-and-evidence.md).
- [Investigación y problemas jurídicos](../workflows/03-legal-research-and-issue-spotting.md), con fuentes constitucionales y jurisprudencia oficial.
- [Redacción y revisión](../workflows/04-legal-drafting-and-document-review.md) y [actuaciones procesales](../workflows/05-procedural-submissions-and-resources.md).
- [Tutela](../workflows/12-tutela.md), como composición futura con límites explícitos.
- [Revisión adversarial](../workflows/08-adversarial-review-and-decision-support.md), para buscar soporte ausente, lecturas alternativas y evidencia contraria.

## Documentos comunes

Pueden aparecer solicitud de tutela, respuesta, impugnación, comunicaciones, actuaciones o providencias, evidencia documental, audios, anexos y fuentes jurisprudenciales. Un documento puede ser evidencia, alegación, material a analizar o información faltante; no se presume que su contenido sea exacto, suficiente, oficial o procedente.

## Skills transversales

| Necesidad | Candidata transversal | Límite |
|---|---|---|
| Ordenar relato, documentos y faltantes | `intake-structuring` | No concluye procedencia ni urgencia. |
| Trazar hechos y soporte | `fact-builder` y `evidence-analysis` | No declara vulneración o hecho probado. |
| Investigar preguntas y precedentes | `legal-issue-spotting` y `legal-research` | No trata una sentencia como regla universal. |
| Borrador y revisión | `legal-drafting` y `legal-document-review` | No firma, presenta ni certifica requisitos. |
| Lectura crítica | `adversarial-review` y `contradiction-analysis` | No resuelve la acción. |

## Skills especiales si hay

`tutela-assistance` **no se crea todavía**. La decisión vigente es componer las Skills transversales con un Knowledge Pack constitucional fechado, fuentes y evaluación temporal/jurisprudencial. Solo sería una Skill especial si se confirma un método y evals propios que no sean una variación de esa composición.

## Necesidades del Core / Application

- Contexto selectivo del Case, Evidence incorporada, locators, provenance, propuestas y revisión humana.
- Separar fuente jurídica de la evidencia del Case hasta que se incorpore por el canal autorizado.
- No recuperar, radicar, calcular términos, afirmar estado judicial ni integrar expedientes externos desde una Skill.
- La identidad y snapshot verificable de fuentes, o cualquier conector de consulta/presentación, son capacidades posteriores con contrato y política explícitos.

## Dependencias de Knowledge Pack

El pack debe contener derecho o problema a investigar, fecha relevante, texto y versión aplicable, autoridad, jurisdicción, fuente oficial, pasaje jurisprudencial, hechos comparables, posible autoridad contraria, canal y estado de verificación. No puede decidir procedencia ni reemplazar la lectura profesional.

## Fuentes oficiales

| Uso de investigación | Fuente inicial | Estado y límite |
|---|---|---|
| Texto constitucional | [Constitución Política — Secretaría del Senado](https://www.secretariasenado.gov.co/senado/basedoc/constitucion_politica_1991.html) y [SUIN](https://www.suin-juriscol.gov.co/viewDocument.asp?ruta=Constitucion%2F1687988) | Confirmar pasaje y reforma específica si aplica. |
| Procedimiento especial | [Decreto 2591 de 1991 — SUIN](https://www.suin-juriscol.gov.co/viewDocument.asp?id=1470723) y [Función Pública](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=5304) | `FUENTE_OFICIAL_VERIFICADA`; no extrapolar requisitos de otros códigos. |
| Jurisprudencia | [Relatoría de la Corte Constitucional](https://www.corteconstitucional.gov.co/relatoria/) | Verificar texto, pasaje, hechos, ratio y evolución posterior. |
| Control digital identificado | [J-CC-C522-2023](../source-catalog/jurisprudence-sources.md) | Revisar el pasaje y la regla específica de tutela; no trasladar por analogía una exigencia de otro procedimiento. |

El gobierno de las fuentes está en el [catálogo oficial](../source-catalog/colombia-official-sources.md), la [matriz temporal](../source-catalog/temporal-law-matrix.md) y el [gobierno de jurisprudencia](../07-jurisprudence-governance.md).

## Riesgos temporales

- El Decreto 2591 de 1991 es un procedimiento especial; no se deben trasladar requisitos o plazos de CGP, CPACA o Ley 2213 sin comprobar la regla aplicable.
- La evolución jurisprudencial, la fecha del hecho, actuación, fuente y decisión consultada puede cambiar la pertinencia de una cita.
- La matriz identifica [J-CC-C522-2023](../source-catalog/jurisprudence-sources.md) para revisar la regla específica de tutela antes de usar una exigencia del artículo 6 de la Ley 2213.
- Si no se confirma versión, pasaje o fecha relevante, se debe mostrar `VIGENCIA_POR_VERIFICAR` o `JURISPRUDENCIA_POR_VERIFICAR`.

## Autoridades jurisprudenciales

La [Corte Constitucional](https://www.corteconstitucional.gov.co/relatoria/) es la fuente inicial. Cada registro debe indicar tipo y número de providencia, fecha, sala si aparece, texto completo, locator, pregunta jurídica, proposición atribuida, hechos, ratio, posibles límites y autoridad contraria. Hallar una providencia no permite afirmar que resuelve el Case.

## Dependencias territoriales

Despacho, canal, reparto, disponibilidad de actuaciones y expediente rector son `REQUIRES_TERRITORIAL_RESEARCH` y `POR_VERIFICAR`. Ninguna carpeta local, correo o portal parcial sustituye la confirmación humana de la actuación oficial.

## Decisiones exclusivamente humanas

La profesional decide estrategia, selección y lectura de fuentes, relación entre hechos y problema constitucional, evidencia, redacción, firma, presentación, respuesta e impugnación. La autoridad competente decide admisibilidad, procedencia, urgencia, medidas, valoración de evidencia, órdenes y resultado. La IA no puede adoptar ni simular esas decisiones.

## Gaps y preguntas abiertas

- `GAP`: variantes de tutela y demás asuntos constitucionales que la profesional atiende realmente.
- `GAP`: evidencia y fuentes consideradas mínimas antes de asumir, responder o impugnar.
- `GAP`: protocolo de actualización de jurisprudencia, búsqueda adversa y revisión de ratio.
- `GAP`: integración admisible con actuaciones o canales oficiales, que requeriría arquitectura y autorización posteriores.
