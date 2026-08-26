# 04 — Gobierno de fuentes

## 1. Regla de procedencia

Una afirmación jurídica material en este corpus necesita, como mínimo:

```text
jurisdiction + source URL/identifier + checked_at + status
```

Cuando corresponda, añada `published_at`, `effective_from`, `effective_to`, `transition_rule` y `case_relevant_date`. No se convierte una página de consulta en autoridad legal por enlazarla desde un recurso de Skill.

## 2. Jerarquía operativa de consulta

No es una jerarquía normativa inventada; es un orden de trabajo para verificar:

1. Texto promulgado/publicado y portal oficial de la entidad competente.
2. Fuente oficial que aloja, relatoría o indexa el material con identificador verificable.
3. Fuente institucional secundaria que explica o consolida, etiquetada como tal.
4. Fuente no oficial solo para descubrir pistas; nunca cierra una verificación si existe fuente oficial.

La fuente de acceso no sustituye el análisis de autoridad, vigencia ni ámbito de aplicación.

## 3. Ficha mínima de fuente

| Campo | Significado |
|---|---|
| `institution` | Entidad que publica o mantiene la fuente. |
| `content_type` | Norma, diario oficial, providencia, expediente, guía o índice. |
| `official` | Sí/no; no inferirlo por el dominio. |
| `access_role` | primaria, espejo oficial, relatoría, secundaria. |
| `identifier` | Ley, decreto, sentencia, radicado o URL estable. |
| `date_metadata` | publicación, expedición, decisión, vigencia o última actualización visible. |
| `version_status` | vigente/consolidada/histórica/desconocida, con evidencia. |
| `snapshot_feasibility` | cómo preservar el texto consultado sin confundirlo con la fuente. |
| `limitations` | disclaimer, cobertura, búsqueda, acceso, licencias o ausencia de certificación. |
| `checked_at` | fecha de revisión. |

## 4. Estados y tratamiento

| Estado | Puede usarse para | No puede usarse para |
|---|---|---|
| `VERIFIED_OFFICIAL` | Identificar el texto/fuente con fecha indicada | Asumir relevancia, vigencia de un caso o estrategia |
| `VERIFIED_SECONDARY` | Orientar búsqueda y explicar limitaciones | Cerrar una regla jurídica sensible |
| `UNVERIFIED` | Formular pregunta o tarea de verificación | Redactar como hecho |
| `CONFLICTING` | Mostrar conflicto y escalar | Elegir silenciosamente una versión |
| `OUTDATED` | Conservar trazabilidad histórica | Aplicar al caso sin nueva verificación |

### Equivalencia con las etiquetas visibles del corpus

Los estados técnicos anteriores se conservan para compatibilidad con materiales de la primera iteración. En una salida para una persona usuaria o en una conclusión de investigación, usar además la etiqueta en español que corresponda:

| Estado técnico | Etiqueta legible | Consecuencia |
|---|---|---|
| `VERIFIED_OFFICIAL` | `FUENTE_OFICIAL_VERIFICADA` | La identidad de la fuente fue comprobada; todavía se debe verificar pasaje, fecha y pertinencia. |
| `VERIFIED_SECONDARY` | `FUENTE_SECUNDARIA_VERIFICADA` | Sirve para orientar la búsqueda; no cierra un punto jurídico crítico por sí sola. |
| `UNVERIFIED` | `POR_VERIFICAR` | No se presenta como regla, requisito ni hecho. |
| `CONFLICTING` | `CONFLICTO_DE_FUENTES` | Se explica el conflicto y se escala a revisión; no se elige una versión en silencio. |
| `OUTDATED` | `VIGENCIA_POR_VERIFICAR` | Se conserva como antecedente, pero no se aplica sin una nueva comprobación. |

Para una sentencia o una transición aún no cerrada, usar respectivamente `JURISPRUDENCIA_POR_VERIFICAR` o `TRANSICION_POR_VERIFICAR`. Cuando la evidencia no alcance, la conclusión correcta es `NO_TENEMOS_INFORMACION_SUFICIENTE`.

## 4.1 Clase de fuente y verificación crítica

| Clase | Uso permitido | Control adicional |
|---|---|---|
| `PRIMARY_OFFICIAL` | Promulgación o publicación oficial con identificador verificable | Confirmar el texto, el pasaje y la fecha del caso. |
| `OFFICIAL_CONSOLIDATED` | Localizar y leer una versión institucional integrada | Cruzar el punto crítico con publicación, reforma o versión aplicable. |
| `OFFICIAL_JURISPRUDENCE` | Localizar una providencia oficial | Registrar corporación, sala/sección, fecha, identificador, pasaje, hechos y autoridad posterior/contraria. |
| `OFFICIAL_INTERPRETIVE` | Orientar una consulta o explicar un trámite | No usar como única base de una conclusión sensible. |
| `SECONDARY` | Descubrir fuentes o formular preguntas | No cerrar identidad, vigencia, alcance o estrategia. |

## 5. Protocolo de investigación jurídica

1. Formular la pregunta y el resultado que necesita justificarse.
2. Identificar jurisdicción, materia, rol, procedimiento y fecha relevante del Case.
3. Recuperar fuente oficial con identificador/snapshot y registrar su estado.
4. Separar existencia/identidad de la fuente, vigencia temporal y relevancia sustantiva.
5. Localizar el pasaje exacto; no sustituirlo por un título o resumen de buscador.
6. Declarar modificaciones, transición, incertidumbre y fuentes en conflicto.
7. Entregar una propuesta argumentada para revisión humana, nunca una afirmación "verificada" por el modelo.

## 6. Conservación y confidencialidad

Un snapshot de fuente externa debe guardar provenance y fecha de consulta, pero no habilita que una Skill escriba en el expediente. Ningún recurso de Skill contiene credenciales, documentos reales, nombres de clientes ni resultados de búsquedas de un Case. Las operaciones de retrieval y persistencia pertenecen a conectores/adapters futuros y al Core.

## 7. Antilavado de conocimiento

Copiar una norma, resumen o enlace a este directorio no la vuelve una regla permanente ni una verdad que una Skill pueda aplicar de memoria. Cada afirmación jurídica operativa debe responder: **fuente, fecha de revisión, pasaje o identificador, aplicabilidad, estado y límite**. Si falta uno de esos elementos, la afirmación se marca `POR_VERIFICAR` o `NO_TENEMOS_INFORMACION_SUFICIENTE`.
