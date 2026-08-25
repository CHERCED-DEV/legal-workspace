# Workflow — Policivo y querellas (Colombia)

**Estado:** P3 — `DEFER`. El discovery menciona este contexto, pero el flujo de autoridad y el expediente oficial aún no están levantados.
**Jurisdiction:** Colombia. **Fuente seed:** Ley 1801 de 2016, sus modificaciones y reglamentación aplicable verificadas para el Case.
**Límite:** distingue asistencia a parte/litigante de apoyo a decisor; no introduce contexto B, entidades ni transiciones nuevas en V0.

## Objetivo de trabajo

Ordenar la información necesaria para preparar una querella, revisar una actuación, analizar evidencia, preparar una audiencia o revisar un borrador de acto, dejando visibles el rol, el procedimiento a confirmar y las decisiones que pertenecen a la autoridad o a la profesional.

## Cuándo ocurre este workflow

Al recibir un relato o querella, verificar información mínima, estudiar una actuación, preparar audiencia, comparar argumentos/evidencia, hacer seguimiento de documentos o preparar/revisar un proyecto. No sustituye la recepción oficial, clasificación del procedimiento, admisión, rechazo, práctica de prueba ni decisión.

## Roles de usuario

- Litigante, representante o persona que prepara información para una actuación policiva.
- Profesional que revisa material de una audiencia o una providencia/proyecto.
- Autoridad o apoyo de autoridad solo en investigación futura y bajo un modelo de expediente oficial aún no diseñado.

## Ejemplos de activación

- “Organice la información que falta para estudiar esta querella.”
- “Prepare preguntas y evidencia pendiente para esta audiencia.”
- “Compare estas versiones de los hechos y señale tensiones verificables.”
- “Revise este proyecto y enumere argumentos o evidencia que requieren revisión humana.”

## Entradas

Relato/querella, identificación declarada de participantes, rol de quien consulta, actuación o requerimiento identificado, documentos, audios, fotos u otros materiales disponibles, fechas conocidas, autoridad/territorio declarados y evidencia incorporada cuando exista. Ningún dato de competencia, procedimiento o estado se presupone por el nombre del documento.

## Contexto canónico requerido

Para V0, solo contexto selectivo de un Case de litigante, Evidence incorporada, locators, Facts/propuestas y condiciones de staleness. Si aparece un expediente externo de autoridad, se trata como información externa no canónica hasta que exista un diseño específico de contexto B.

## Información externa posiblemente necesaria

Texto vigente aplicable, reglamentación territorial/autoridad competente, publicación o actuación oficial, expediente oficial cuando proceda y fuente de canal/fecha. Recuperar o sincronizar esos datos requiere connectors/adapters futuros y una política de custodia, no lectura directa desde una Skill.

## Método / etapas de razonamiento

1. Declarar si el trabajo es de parte/litigante o de apoyo a decisor; no mezclar ambos roles.
2. Separar relato, documento, evidencia, actuación identificada, inferencia y dato faltante.
3. Identificar información mínima que debe verificarse: autoridad, territorio, acto, fecha, participantes, solicitud y material de soporte.
4. Construir cronología y matriz de hechos/evidencia, distinguiendo apoyo parcial, contradicción y ausencia de información.
5. Para audiencia o proyecto, organizar posiciones de las partes, preguntas, evidencia contraria y decisiones que requieren humano.
6. Entregar una propuesta o checklist, no una clasificación procesal, admisión o decisión.

## Salidas esperadas

Checklist de información/fuentes pendientes, cronología declarada, matriz de evidencia, brief de audiencia, lista de actuaciones a verificar o informe de revisión con hallazgos falsables. Toda salida separa “documento visto”, “hecho alegado”, “evidencia incorporada” y “requiere confirmación”.

## Decisiones humanas

La profesional decide estrategia, relevancia, presentación y respuesta. La autoridad competente decide recepción formal, competencia, admisión/inadmisión/rechazo, práctica y valoración de prueba, conducción de audiencia, motivación, órdenes y acto oficial.

## Lo que la IA puede proponer

Preguntas aclaratorias, organización del relato, referencias de documentos, cronologías provisionales, pasajes comparables, tensiones de fecha/monto/identidad/secuencia, estructura de borrador y preguntas de revisión.

## Lo que la IA no debe decidir

No puede clasificar definitivamente un procedimiento, declarar competencia, admitir/rechazar, valorar prueba, calcular un término, establecer hechos probados, emitir auto/providencia/decisión ni afirmar que un expediente externo está completo o es el oficial.

## Responsabilidades del Core / Application

El Core mantiene identidad y aislamiento de Case, incorporación inmutable de Sources, provenance, locators, propuestas, autorización humana, commit, eventos y auditoría. Un modelo de expediente oficial, estado procesal, plazos y permisos de autoridad requeriría Domain/Application y policy posteriores; este dossier no los diseña.

## Herramientas MCP potencialmente requeridas

Ninguna adicional en V0. El trabajo puede consumir contexto, búsqueda y fragmentos ya autorizados; consultar expedientes de autoridad, clasificar actuaciones o producir actos oficiales no son tools implícitas y no pueden añadirse desde una Skill.

## Dependencias de Knowledge Pack

Muy alta: versión aplicable de Ley 1801, modificaciones, reglamentación, territorio, autoridad, rol y procedimiento. El pack futuro debe identificar fuente oficial, alcance territorial, fecha relevante, `checked_at` y cualquier incertidumbre. No hay Knowledge Pack policivo cargado en V0.

## Requisitos de evidencia y provenance

Todo hallazgo debe enlazar el material que lo sostiene o marcarse como pregunta. Fotos, audios, actas y documentos conservan su origen, versión y locator; una derivación no reemplaza al original. El sistema no debe presentar una tensión semántica como contradicción acreditada ni un documento descargado como Evidence sin incorporación.

## Dependencias temporales y fuentes oficiales

La regla y el procedimiento dependen de la fecha del hecho/actuación, de reformas y de reglamentación aplicable. Fuente seed: Ley 1801 de 2016, con catálogo y límites en `../source-catalog/temporal-law-matrix.md` y `../source-catalog/colombia-official-sources.md`. No extrapolar reglas generales de CPACA o CGP.

## Manejo de documentos externos e inyección de instrucciones

Querellas, actas, capturas, correos, portales y audios son contenido no confiable. Instrucciones insertadas en ellos no cambian el objetivo, las tools ni la autorización. Una Skill no usa credenciales, no navega rutas privadas y no mezcla materiales de otro Case; los controles técnicos permanecen en Core/host.

## UX y fallos frecuentes

La vista debe hacer visibles rol, fuente, fecha, actuación por confirmar, evidencia faltante y diferencia entre parte/autoridad. Evitar confundir la organización de una querella con su recepción formal, presentar una inferencia como decisión, ocultar evidencia contraria o usar un lenguaje que haga parecer que el modelo tiene competencia decisoria.

## Evals candidatos

- Caso sintético de parte y caso de autoridad con el mismo material: el output debe separar sus límites.
- Querella con autoridad/territorio/fecha faltantes: debe pedirlos, no inventarlos.
- Dos fuentes con tensión formal y una tensión semántica: debe diferenciarlas y enlazarlas.
- Acta o PDF con instrucción maliciosa: se procesa solo como contenido.
- Fuente/reglamentación sin fecha verificable: debe rotular incertidumbre y escalar a revisión humana.

## Mapeo de candidata y prioridad

Composición futura de `intake-structuring`, `fact-builder`, `evidence-analysis`, `hearing-analysis`, `contradiction-analysis`, `legal-research`, `legal-document-review` y `adversarial-review`. **No crear una Skill “policivo” ni “querellas”** hasta descubrir un método separado y evaluable. P3 / `DEFER`.

## Preguntas abiertas

- Cuáles son los flujos policivos reales de la profesional y qué rol ocupa en cada uno.
- Qué sistema o expediente considera oficial y cómo se resuelven discrepancias.
- Qué actos, criterios y decisiones nunca se delegarían.
- Qué reglamentación territorial, formatos y canales se usan realmente.
