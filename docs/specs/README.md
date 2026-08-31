# Especificaciones — la capa que faltaba

**Desde:** 2026-08-31. **Espacio de identificadores:** `SPEC-NN`, verificado libre antes de crearlo.

---

## Por qué existe esta carpeta

Este proyecto **ya hacía desarrollo dirigido por especificación sin llamarlo así**: los nueve `SKILL.md` no son documentación de un programa, **son el programa** — especificaciones en prosa que un modelo ejecuta. Esa es la arquitectura, y es correcta.

Lo que faltaba es la capa intermedia. Hoy hay:

| Capa | Qué contiene | Dónde |
|---|---|---|
| **Decisión** | Por qué se decidió así, con sus alternativas y consecuencias | `docs/architecture/adrs/ADR-NNN` |
| **Método** | El procedimiento que el modelo ejecuta | `plugins/despacho/skills/*/SKILL.md` |
| **Diagnóstico** | Qué está mal y qué falta, con su origen | `docs/BACKLOG-CONSOLIDADO.md` |
| **← esto faltaba** | **Qué se va a construir, y cómo se sabe que quedó** | `docs/specs/SPEC-NN` |

Sin esa capa pasa lo que ya pasó: **una implementación se desvía de una decisión y nadie lo nota.** `PLAN-DE-MEJORA` rechazó el OCR con dos condiciones escritas; ADR-016 y `preparar_material.py` lo construyeron sin cumplirlas, y la `Ñ` mayúscula sigue rota — el error exacto que el rechazo temía. Una spec con criterios de aceptación lo habría atrapado antes de escribir la primera línea.

## El contrato de una spec

Cada `SPEC-NN` tiene **siete apartados, siempre los siete**. Si uno queda vacío, se dice que quedó vacío.

| Apartado | Qué va, y qué no |
|---|---|
| **1. Qué problema cierra** | El ítem del backlog y su origen. **Una spec sin ítem no se escribe**: sería inventar trabajo |
| **2. Comportamiento observable** | Qué ve la usuaria, en su idioma. **Nunca cómo está hecho por dentro** |
| **3. Reglas duras** | Los invariantes que no se negocian, y de qué ADR salen |
| **4. Qué NO hace** | Tan importante como lo que hace. Es lo que impide que la implementación crezca sola |
| **5. Cómo se sabe que quedó** | **Observables, no pruebas unitarias.** «Se abre y aparece X», «el registro dice Y», «el conteo coincide». Cada uno tiene que poder fallar |
| **6. Qué toca** | Los archivos concretos. Si toca un `SKILL.md`, dice cuál sección |
| **7. Qué queda fuera y por qué** | Lo que se decidió posponer, con su razón. Evita que vuelva a discutirse |

### Tres reglas de esta capa

1. **La spec manda sobre la implementación.** Si el código hace algo que la spec no dice, o no hace algo que dice, es la implementación la que está mal — no la spec la que se ajusta después.
2. **Ninguna spec contradice un ADR.** Si hace falta contradecirlo, primero se enmienda el ADR. Precedencia: ADR `Accepted` > ADR `Proposed` > spec > implementación.
3. **Antes de escribir una spec nueva, se lee el índice.** Es la regla que este repositorio aprendió por la mala: cuatro documentos llamaron «séptimo comando» a cuatro cosas distintas.

## Estado de las especificaciones

| # | Spec | Cierra | Estado |
|---|---|---|---|
| [SPEC-01](SPEC-01-instalacion-del-plugin.md) | Instalación del plugin desde el remoto | `EP-ENTRADA-0` · `H-10` | **En ejecución** |
| [SPEC-02](SPEC-02-hoja-de-hechos-aprobada.md) | La hoja de hechos: dónde se escribe y cómo se aprueba | `H-05` · G17 | Escrita |
| SPEC-03 | Variante de contexto B | `P-02` · G7 | Pendiente |
| SPEC-04 | Bloque «dicho por usted, no documentado en la carpeta» | `P-05` · `P-06` · G6 | Pendiente |
| SPEC-05 | Blindaje de la marca ` - REVISADO` | `PM-M-2` · G25 | Pendiente |
| SPEC-06 | `0-Estado del caso`: reemplazo dirigido, no reescritura | `H-11` · G19 | Pendiente |
| SPEC-07 | Los doce hallazgos de `inventario-de-bienes` | V-1 | Pendiente |
| SPEC-08 | Índice de las salidas de una pasada | `P-07` · G37 | Pendiente |

**Orden:** SPEC-01 primero porque desbloquea todo lo demás —hasta que ella pueda instalar, ninguna corrección le llega—. Después SPEC-02, que es el eslabón partido del oleoducto. El resto por valor.

**No están todas las que faltan.** El backlog tiene ~90 ítems reales; estas ocho son las que se pueden construir **sin el Core** y cierran lo que más pesa. Las demás esperan a que se decida qué es la primera versión — que es el hueco V-10 y no lo decide una spec.
