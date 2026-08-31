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

### Cuatro reglas de esta capa

1. **La spec manda sobre la implementación.** Si el código hace algo que la spec no dice, o no hace algo que dice, es la implementación la que está mal — no la spec la que se ajusta después.
2. **Ninguna spec contradice un ADR.** Si hace falta contradecirlo, primero se enmienda el ADR. Precedencia: ADR `Accepted` > ADR `Proposed` > spec > implementación.
3. **Antes de escribir una spec nueva, se lee el índice.** Es la regla que este repositorio aprendió por la mala: cuatro documentos llamaron «séptimo comando» a cuatro cosas distintas.
4. **Antes de escribir una spec de defecto, se comprueba que el defecto siga vivo.** Regla añadida el 2026-08-31 al retirar SPEC-02: iba a especificar el arreglo de algo que llevaba dos meses arreglado y verificado en ejecución real. **Un backlog no leído contra el código produce trabajo inventado**, que es el mismo pecado que esta capa existe para impedir.

---

## Dos familias de spec, y el índice del 31/08 solo tenía una

Esta es la corrección de fondo del índice original. Las ocho specs que listaba eran **todas de defecto**: cerraban un ítem del backlog, es decir, arreglaban algo que ya existe y está mal. Ninguna construía nada. Leído de corrido, el índice daba a entender que ocho specs cubrían el producto, y no cubren **ninguna** de las capacidades grandes.

| Familia | Qué hace | Cómo se reconoce |
|---|---|---|
| **Spec de defecto** | Cierra un ítem del backlog. **Algo existe y está mal** | Su apartado 1 cita un `H-NN`, `P-NN`, `PM-*` o un grupo `GNN` |
| **Spec de capacidad** | Construye algo que **no existe todavía** | Su apartado 1 cita un hueco `V-NN` o un ADR sin implementación |

---

## Mapa de capacidades — qué está construido, qué está decidido, qué tiene spec

Las tres columnas son distintas a propósito. **Decidido no es construido, y construido no es especificado.**

| Capacidad | Estado real hoy | Decisión | Spec |
|---|---|---|---|
| **Instalar y actualizar el plugin** | Remoto publicado. **Cero instalaciones fuera de esta máquina** | ADR-012 | **SPEC-01** — parcial: O-5 a O-7 solo en su máquina |
| **Los nueve métodos** | Desplegados y ejecutados en dos casos reales | los `SKILL.md` son la spec | SPEC-04 a SPEC-08 — de defecto |
| **Hablarle a una autoridad, no a una parte** | **No existe.** Los `SKILL.md` dicen «su clienta» y la única usuaria real es la inspección | ninguna | **SPEC-03** — pendiente |
| **Leer fotos sin capa de texto (OCR)** | `tools/preparar-material/` funciona. **Vive fuera del plugin** | ADR-016 | **ninguna** |
| **Detectar la omisión silenciosa (dos motores)** | `segunda_opinion.py` escrito; Tesseract **sin instalar** | ADR-016 | **ninguna** |
| **Entregable en Word** | `tools/md2docx/` produjo 139 tablas reales. **Script a mano, fuera del producto** | ADR-014 | **ninguna** |
| **Transcribir audio de audiencia** | **No existe.** Solo está decidido el límite | ADR-017 | **ninguna** |
| **Que una skill ejecute código (el Core)** | **No existe.** El plugin es texto puro | ADR-010 | **ninguna** |
| **Copia de seguridad del trabajo de ella** | **No existe.** ADR escrito, cero implementación | ADR-013 | **ninguna** — hueco `V-5` |
| **Medir horas-persona y coste por caso** | **No existe.** Todo se mide en tokens | ninguna | **ninguna** — huecos `V-2`, `V-3` |
| **Reanudar un comando que se cayó** | **No existe** | ninguna | **ninguna** — hueco `V-4` |
| **Riesgo de que la usuaria sea autoridad** | **Cero líneas en todo el repositorio** | ninguna | **ninguna** — hueco `V-7` |
| **Datos de terceros que no consintieron** | Riesgo declarado, **sin dueño** | ninguna | **ninguna** — hueco `V-8` |
| **Alcance y precio de la primera versión** | No decidido | ninguna | **no lo decide una spec** — hueco `V-10` |

### Las tres cosas que este mapa deja a la vista

1. **Tres capacidades ya construidas viven fuera del plugin.** OCR, segunda opinión y Word son Python; el plugin es texto puro y una skill no puede ejecutar código. Es la **pregunta 2 abierta de ADR-014**, dicha allí sin rodeos: *o el Core lo asume, o el entregable Word depende de que alguien corra un script a mano.* Mientras eso no se decida, ninguna spec de esas tres capacidades puede cerrarse — **y la dependencia es esa decisión, no el esfuerzo de escribirla.**

2. **Los dos riesgos mayores no tienen ni decisión ni spec.** `V-7` —si una inspectora puede apoyar un acto administrativo en una salida de IA, si debe declararlo, qué le pasa al acto si la cita sale mal— y `V-8` —quién responde por los datos de terceros—. No son deuda técnica: son los dos frenos de licenciar esto a alguien. **Les falta un ADR antes que una spec**, por la regla 2.

3. **Nada de esto se puede ordenar sin `V-10`.** Sin decidir qué es la primera versión, cualquier orden que yo proponga es una preferencia mía disfrazada de plan.

---

## Estado de las especificaciones

| # | Spec | Familia | Cierra | Estado |
|---|---|---|---|---|
| [SPEC-01](SPEC-01-instalacion-del-plugin.md) | Instalación del plugin desde el remoto | defecto | `EP-ENTRADA-0` · `H-10` | **Parcialmente ejecutada.** O-1 a O-4 pasan; O-5 a O-7 solo en su máquina |
| ~~SPEC-02~~ | ~~La hoja de hechos: dónde se escribe y cómo se aprueba~~ | — | ~~`H-05` · G17~~ | **RETIRADA — el defecto ya estaba cerrado.** Ver abajo |
| SPEC-03 | Variante de contexto B | defecto | `P-02` · G7 | Pendiente — no escrita |
| SPEC-04 | Bloque «dicho por usted, no documentado en la carpeta» | defecto | `P-05` · `P-06` · G6 | Pendiente — no escrita |
| SPEC-05 | Blindaje de la marca ` - REVISADO` | defecto | `PM-M-2` · G25 | Pendiente — no escrita |
| SPEC-06 | `0-Estado del caso`: reemplazo dirigido, no reescritura | defecto | `H-11` · G19 | Pendiente — no escrita |
| SPEC-07 | Los doce hallazgos de `inventario-de-bienes` | defecto | `V-1` | Pendiente — no escrita |
| SPEC-08 | Índice de las salidas de una pasada | defecto | `P-07` · G37 | Pendiente — no escrita |

> **Cuenta honesta: una escrita y ejecutada a medias, una retirada, seis que hoy son solo una fila de esta tabla.** «Pendiente» aquí significa que el archivo **no existe**. El índice del 31/08 marcaba SPEC-02 como «Escrita» y la enlazaba; el archivo nunca existió. Corregido.

### Por qué se retiró SPEC-02, y qué queda vivo de su grupo

Iba a especificar el arreglo de `H-05` —*«dos comandos consumen una hoja de hechos que nadie escribe»*—. **Al ir a escribirla, se leyó el código y la cadena estaba completa:**

| Eslabón | Dónde | Qué dice |
|---|---|---|
| **Productor** | `hechos-con-prueba/SKILL.md` §4 | Escribe en `2-Borradores/Hechos - <caso> - <AAAA-MM-DD>.md`, no sobrescribe, y explica cómo ella marca ` - REVISADO` — con la prohibición de que el modelo la ponga |
| **Consumidor** | `redactar-escrito/SKILL.md` §3 | Mira esa ruta exacta y **se detiene** si no hay archivo con la marca |
| **Consumidor** | `inventario-de-anexos/SKILL.md` §5 | Igual, con sus tres vías de emparejamiento en orden |
| **Verificación** | `docs/discovery/primera-ejecucion-real.md` §4 | *«`redactar-escrito` se negó a redactar»* ante un caso sin hechos aprobados. **Se comprobó en ejecución real, no en revisión de escritorio** |

**El identificador SPEC-02 no se reutiliza.** Misma disciplina que las etiquetas de hecho: si se retira, se retira con él. Reciclarlo haría que dos documentos llamen SPEC-02 a dos cosas — exactamente lo del «séptimo comando».

**Lo que sí sigue vivo del grupo G17** es la marca ` - REVISADO` frente a la extensión oculta de Windows: ella guarda `... - REVISADO` y el archivo queda `... - REVISADO.md.md` o sin extensión, y entonces **el comando no la ve y se niega a trabajar con hechos que ella sí aprobó**. Eso es `PM-M-2` y **ya tenía su propio identificador: SPEC-05**. No hacía falta SPEC-02 para nada.

---

## Qué se hace ahora, y qué no lo decido yo

**Puedo escribir y ejecutar ya**, sin depender de nadie: SPEC-05 (la marca ` - REVISADO`), SPEC-06 (`0-Estado del caso`), SPEC-04 (el bloque de lo dicho no documentado) y SPEC-08 (el índice de salidas). Las cuatro son texto dentro de los `SKILL.md`, no necesitan Core ni instalar nada.

**SPEC-03 —contexto B— es la más valiosa y la más delicada:** cambia a quién le habla el producto en su único uso real. No es una corrección de redacción; toca qué puede y qué no puede proponerle un sistema a quien decide. Merece decidirse, no escribirse de una.

**No depende de mí, y bloquea más que todo lo anterior:**

| Qué falta | Quién | Qué desbloquea |
|---|---|---|
| Instalar el plugin una vez y decir cómo aparecen los comandos | Usted o ella | Cerrar SPEC-01 · imprimir la guía |
| Decidir **dónde se procesa el material** de ella | Usted | Entregar sin mentirle · licenciar |
| Decidir **qué es la primera versión** (`V-10`) | Usted | El orden de todo lo demás |
| Un ADR para `V-7` —autoridad apoyándose en salidas de IA— | Usted, con criterio jurídico | La spec de contexto B, y la venta |

**No están todas las que faltan.** El backlog tiene 112 identificadores; estas ocho tocan lo que más pesa **y solo del lado de los defectos**. Las capacidades del mapa de arriba necesitan primero las decisiones de esa tabla.
