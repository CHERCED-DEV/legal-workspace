# 07 — Gobierno de jurisprudencia

**Estado:** metodología de investigación y trazabilidad; no registro ejecutable de precedentes.

## Regla central

Encontrar una providencia no demuestra que sostenga una proposición. La investigación debe separar identidad, texto recuperado, pasaje relevante, lectura de alcance, autoridad contraria y validación profesional.

## Registro mínimo de una providencia

| Campo | Qué debe conservarse |
|---|---|
| Identidad | corporación, sala/sección, tipo, identificador y radicado si existe |
| Fecha y autoría | fecha, ponente si aparece y enlace oficial |
| Pregunta jurídica | asunto concreto que se está investigando |
| Proposición atribuida | frase precisa que se pretende sostener; no un resumen genérico |
| Locator | página, apartado, numeral o párrafo del pasaje relevante |
| Análisis | por qué el pasaje sí o no responde la proposición y en qué hechos/fecha |
| Derecho adverso | lenguaje limitante, providencia contraria, cambio posterior o distinción fáctica |
| Tiempo y estado | fecha de consulta, evolución posterior revisada y estado de análisis |

## Estados no booleanos

| Estado | Significado |
|---|---|
| IDENTITY_VERIFIED | La providencia e identificador oficial fueron comprobados. |
| CONTENT_RETRIEVED | Se obtuvo el texto o fuente oficial suficiente para leerlo. |
| RELEVANCE_REVIEWED | Se comparó el pasaje con la proposición y el contexto. |
| PROFESSIONALLY_CONFIRMED | Una persona competente validó el uso profesional. |
| CONFLICTING | Hay autoridad o lectura contraria pendiente de resolver. |
| SUPERSEDED_OR_LIMITED | Hay cambio, límite o desarrollo posterior que reduce su uso. |
| JURISPRUDENCIA_POR_VERIFICAR | Falta alguno de los pasos anteriores. |

## Fuentes oficiales prioritarias

| Área | Punto de partida | Precaución |
|---|---|---|
| Constitucional y tutela | Relatoría oficial de la Corte Constitucional | Identificar tipo, fecha, pasaje, hechos y alcance; una tutela no crea por sí sola una regla universal. |
| Administrativo-contencioso | Consejo de Estado, Mi Relatoría / SAMAI | Distinguir sección, medio de control, fecha y sentencias de unificación. |
| Civil, familia y laboral | Relatorías oficiales de la Corte Suprema y, cuando proceda, Rama Judicial | Confirmar sala, radicado y decisión completa. |
| Policivo/territorial | Fuente judicial competente más norma/acto territorial oficial | No sustituir expediente, autoridad o regulación territorial con un resumen. |

El catálogo de portales está en [source-catalog/jurisprudence-sources.md](source-catalog/jurisprudence-sources.md).

## Búsqueda adversa obligatoria

Para una proposición material, buscar también: autoridad contraria, autoridad limitante, hechos distinguibles, cambios posteriores y decisiones de unificación. Si no se puede completar por alcance o tiempo, registrar **JURISPRUDENCE_GAP**; no presentar el resultado como investigación exhaustiva.

## Límites

- Una Skill puede proponer una ficha y preguntas de revisión.
- Un Knowledge Pack puede aportar identificadores, reglas declarativas y fechas.
- El Core o una capacidad futura debe controlar identidad, snapshots y estado verificable.
- La persona competente decide pertinencia, interpretación, citación final y estrategia.
