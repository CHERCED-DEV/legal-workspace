# Dossier de práctica — Administrativo y contencioso administrativo (Colombia)

**Estado de cobertura:** `PARTIALLY_COVERED` / `REQUIRES_CASE_SPECIFIC_RESEARCH`.
**Fecha de referencia:** 2026-08-25. **Propósito:** distinguir investigación y trabajo de redacción/revisión de cualquier decisión sobre actuación, medio, término o resultado.

## Alcance

Incluye trabajo relacionado con actuación administrativa, acto administrativo, expediente administrativo, derecho de petición cuando corresponda, demandas y escritos ante la jurisdicción contencioso-administrativa. No presupone que el CPACA sea el régimen suficiente para el asunto, ni identifica automáticamente medio de control, agotamiento, caducidad, competencia, notificación o canal.

## Workflows observados

- [Intake y estructura inicial](../workflows/01-intake-structuring.md) y [hechos/evidencia](../workflows/02-fact-construction-and-evidence.md), para separar acto, comunicación, expediente, alegación y soporte.
- [Investigación y problemas jurídicos](../workflows/03-legal-research-and-issue-spotting.md), con búsqueda de norma, acto, versión, jurisdicción y precedente.
- [Redacción y revisión](../workflows/04-legal-drafting-and-document-review.md), [actuaciones procesales](../workflows/05-procedural-submissions-and-resources.md) y [derecho de petición](../workflows/06-right-to-petition.md) cuando aplique.
- [Audiencias y contradicciones](../workflows/07-hearing-analysis-and-contradictions.md), [revisión adversarial](../workflows/08-adversarial-review-and-decision-support.md) y [concepto jurídico](../workflows/11-legal-opinion.md).

## Documentos comunes

Pueden aparecer acto administrativo, comunicación o constancia de notificación, petición, respuesta, recurso administrativo, expediente o extracto, solicitud, demanda, contestación, memorial, prueba, providencia y publicación oficial. Cada elemento requiere identificación de origen, fecha, versión y locator; no se asume que una copia informal sea el expediente rector.

## Skills transversales

| Necesidad | Candidata transversal | Límite |
|---|---|---|
| Clasificar material y faltantes | `intake-structuring` | No identifica de forma definitiva el medio o trámite. |
| Contrastar acto, relato y soporte | `fact-builder` y `evidence-analysis` | No determina validez del acto ni prueba un hecho. |
| Investigar norma, jurisprudencia y preguntas | `legal-issue-spotting` y `legal-research` | No calcula caducidad ni concluye procedencia. |
| Preparar o revisar escrito | `legal-drafting` y `legal-document-review` | No certifica requisito, firma ni presenta. |
| Examinar objeciones | `contradiction-analysis` y `adversarial-review` | No decide el litigio. |

## Skills especiales si hay

**No hay una Skill autónoma de “medio de control”, “acto administrativo” o “petición”.** Son composiciones de investigación, hechos/evidencia, redacción, revisión y Knowledge Pack fechado. Una especialización futura debe demostrar método propio; hoy permanece `GAP`.

## Necesidades del Core / Application

- Preservar Case, Sources/Evidence incorporadas, locators, provenance, propuestas y revisión humana.
- Mantener separada la actuación oficial del resumen, descarga o transcripción de trabajo.
- No calcular término, caducidad, agotamiento, estado de expediente ni notificación desde una Skill.
- Consultar expedientes o sistemas de entidad requiere conector con contrato, permiso, trazabilidad y política posterior; V0 no lo habilita.

## Dependencias de Knowledge Pack

Se requiere materia, entidad o autoridad, tipo y fecha del acto, fecha y soporte de notificación, procedimiento administrativo o judicial `POR_VERIFICAR`, regla especial, fuente oficial, versión, transición, territorio y pasaje pertinente. La aplicabilidad del derecho de petición se analiza separadamente: no se debe confundir con cualquier actuación judicial.

## Fuentes oficiales

| Uso de investigación | Fuente inicial | Estado y límite |
|---|---|---|
| Texto base administrativo-contencioso | [Ley 1437 de 2011 — SUIN](https://www.suin-juriscol.gov.co/viewDocument.asp?ruta=Leyes%2F1680117) y [Función Pública](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=41249) | `FUENTE_OFICIAL_VERIFICADA`; comprobar reforma, artículo y régimen especial. |
| Derecho de petición, cuando aplique | [Ley 1755 de 2015 — SUIN](https://www.suin-juriscol.gov.co/viewDocument.asp?id=30043679) y [Función Pública](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=65334) | No trasladar automáticamente su régimen a actuación judicial. |
| Canales digitales, cuando proceda | [Ley 2213 de 2022 — Secretaría del Senado](https://www.secretariasenado.gov.co/senado/basedoc/ley_2213_2022.html) | Verificar actuación y canal concretos. |
| Jurisprudencia | [Buscador del Consejo de Estado](https://consejodeestado.gov.co/buscador-de-jurisprudencia2/index.htm) y [SAMAI](https://samai.consejodeestado.gov.co/titulacionrelatoria/buscadorprovidenciastituladas.aspx) | Leer providencia, sección, radicado, fecha y pasaje. |

Las fuentes y límites se mantienen en el [catálogo oficial](../source-catalog/colombia-official-sources.md) y la [matriz temporal](../source-catalog/temporal-law-matrix.md).

## Riesgos temporales

- La matriz registra la vigencia general del CPACA desde 2012-07-02 y reformas, incluida la Ley 2080 de 2021, que deben verificarse para la disposición concreta.
- La Ley 1755 sustituyó el Título II, artículos 13 a 33, de la Ley 1437; no se debe utilizar el texto histórico como si fuera el régimen vigente.
- Fecha del acto, notificación, actuación previa, inicio de proceso, transición y canal pueden ser determinantes; si faltan, corresponde `VIGENCIA_POR_VERIFICAR` o `TRANSICION_POR_VERIFICAR`.
- No se generaliza un plazo, requisito o medio de control a partir de una plantilla.

## Autoridades jurisprudenciales

La fuente inicial es el [Consejo de Estado](https://consejodeestado.gov.co/buscador-de-jurisprudencia2/index.htm) y [SAMAI](https://samai.consejodeestado.gov.co/titulacionrelatoria/buscadorprovidenciastituladas.aspx). La ficha de investigación debe indicar corporación, sección, fecha, radicado, texto, pasaje, cuestión estudiada, autoridad contraria y limitaciones. Sin ello, el estado permanece `JURISPRUDENCIA_POR_VERIFICAR`.

## Dependencias territoriales

Entidad, acto local, autoridad que expide, sede, competencia territorial, reglamentación sectorial, canal y expediente institucional son `REQUIRES_TERRITORIAL_RESEARCH`. El modelo no debe elegirlos ni inferirlos desde el logo, correo o lugar mencionado en un documento.

## Decisiones exclusivamente humanas

La profesional decide la identificación del problema, estrategia, lectura de fuentes, medio o actuación a estudiar, pertinencia y valoración de evidencia, comunicaciones, firma y presentación. La autoridad competente decide competencia, trámite, admisión, medidas, valoración probatoria, actos, providencias y resultado.

## Gaps y preguntas abiertas

- `GAP`: entidades, sectores y tipos de actuación que realmente atiende la práctica.
- `GAP`: mecanismo autorizado para obtener o contrastar el expediente oficial.
- `GAP`: criterios humanos para revisar acto, notificación y procedibilidad sin automatizarlos.
- `GAP`: Knowledge Packs sectoriales, territoriales y temporales que faltan.
