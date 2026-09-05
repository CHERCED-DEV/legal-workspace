# Especificaciones — la capa que faltaba

**Desde:** 2026-08-31. **Espacio de identificadores:** `SPEC-NN`, verificado libre antes de crearlo.

---

## Por qué existe esta carpeta

Este proyecto **ya hacía desarrollo dirigido por especificación sin llamarlo así**: los once `SKILL.md` no son documentación de un programa, **son el programa** — especificaciones en prosa que un modelo ejecuta. Esa es la arquitectura, y es correcta.

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
| **Instalar y actualizar el plugin** | Remoto publicado y **con hoja de instalación**. **Cero instalaciones fuera de esta máquina** | ADR-012 | **SPEC-01** + **SPEC-11** — lo que falta ocurre en su máquina |
| **Los once métodos** | Desplegados; nueve ejecutados en dos casos reales, los dos de la oficina de programas todavía no | los `SKILL.md` son la spec | SPEC-04 · 05 · 06 · 08 **ejecutadas**; SPEC-07 pendiente |
| **Hablarle a una autoridad, no a una parte** | **Construido el 2026-09-05 en su primera mitad:** los once preguntan la posición, ninguna regla presupone bando, y la **simetría obligatoria** —probada a mano en el pase real— es ahora método. **Lo que no existe es la decisión de `V-7`** | ninguna todavía — hace falta **un ADR** | **SPEC-03**, con el valor conservador puesto mientras tanto |
| **Leer fotos sin capa de texto (OCR)** | **Dentro del plugin** desde el 2026-09-01, con su comando `/preparar-material` | ADR-016 · **ADR-018** | el `SKILL.md` es su spec |
| **Detectar la omisión silenciosa (dos motores)** | **Dentro del plugin**; sigue faltando el segundo motor | ADR-016 · **ADR-018** | Fase 5 de `/preparar-material` |
| **Entregable en Word** | **Dentro del plugin, y las siete skills que entregan lo invocan** —`/redactar-escrito` incluida— con su regla de degradación escrita | ADR-014 · **ADR-018** | el `SKILL.md` es su spec |
| **Transcribir audio de audiencia** | Motor y modelos instalados; **falta el script**. Ya no hay nada que lo bloquee salvo audio real | ADR-017 · **ADR-018** | **ninguna todavía** |
| **Que una skill ejecute código** | ~~No existe~~ **SÍ SE PUEDE, y ya se hace.** El Core nunca hizo falta | **ADR-018** | probado con `/preparar-material` |
| **Que lo que ella escribe sobreviva a una pasada** | **Construido el 2026-09-05.** El archivo de estado reemplaza solo su cabecera; lo suyo se conserva byte a byte y se comprueba | `PM-M-8` | **SPEC-06**, con banco de 13 pruebas |
| **Saber qué produjo el sistema en una carpeta** | **Construido el 2026-09-05**, dentro de `/estado-del-caso`: qué comando, de qué pasada, y cuál aprobó ella | ninguna | **SPEC-08** |
| **Copia de seguridad del trabajo de ella** | **No existe.** ADR escrito, cero implementación. **No la resuelve SPEC-06**: esa salva un archivo, no la carpeta | ADR-013 | **ninguna** — hueco `V-5` |
| **Medir horas-persona y coste por caso** | **No existe.** Todo se mide en tokens | ninguna | **ninguna** — huecos `V-2`, `V-3` |
| **Reanudar un comando que se cayó** | **No existe** | ninguna | **ninguna** — hueco `V-4` |
| **Riesgo de que la usuaria sea autoridad** | **Cero líneas en todo el repositorio** | ninguna | **ninguna** — hueco `V-7` |
| **Datos de terceros que no consintieron** | Riesgo declarado, **sin dueño** | ninguna | **ninguna** — hueco `V-8` |
| **Alcance y precio de la primera versión** | No decidido | ninguna | **no lo decide una spec** — hueco `V-10` |

### Las tres cosas que este mapa deja a la vista

1. ~~Tres capacidades ya construidas viven fuera del plugin.~~ **RESUELTO el 2026-09-01 — y era una suposición falsa, no una limitación.** Un plugin sí puede llevar y ejecutar código. Las tres ya viven dentro, en `plugins/despacho/scripts/`. **«Texto puro» describía lo construido y se leyó como límite de lo posible**; ese error puso al Core —una pieza que no existe— como dependencia de tres capacidades que funcionaban. Ver ADR-018.

2. **Los dos riesgos mayores no tienen ni decisión ni spec.** `V-7` —si una inspectora puede apoyar un acto administrativo en una salida de IA, si debe declararlo, qué le pasa al acto si la cita sale mal— y `V-8` —quién responde por los datos de terceros—. No son deuda técnica: son los dos frenos de licenciar esto a alguien. **Les falta un ADR antes que una spec**, por la regla 2.

3. **Nada de esto se puede ordenar sin `V-10`.** Sin decidir qué es la primera versión, cualquier orden que yo proponga es una preferencia mía disfrazada de plan.

4. **Y una cuarta, del 2026-09-05: «ejecutada» se está acumulando sin que nada lo comprueba en uso.** Siete specs ejecutadas, **una sola con pruebas capaces de fallar**. Las otras seis son texto en los `SKILL.md` y su único banco posible es una pasada real, que no ha ocurrido. **Un contador de specs ejecutadas es exactamente la clase de métrica que este repositorio ya se prohibió** — un autoinforme no es control (`H-12`).

---

## Estado de las especificaciones

| # | Spec | Familia | Cierra | Estado |
|---|---|---|---|---|
| [SPEC-01](SPEC-01-instalacion-del-plugin.md) | Instalación del plugin desde el remoto | defecto | `EP-ENTRADA-0` · `H-10` | **Parcialmente ejecutada.** O-1 a O-4 pasan; O-5 a O-7 solo en su máquina |
| ~~SPEC-02~~ | ~~La hoja de hechos: dónde se escribe y cómo se aprueba~~ | — | ~~`H-05` · G17~~ | **RETIRADA — el defecto ya estaba cerrado.** Ver abajo |
| [SPEC-03](SPEC-03-contexto-b-autoridad.md) | Variante de contexto B: cuando ella no representa a nadie | defecto | `P-02` · G7 | **Ejecutada en su primera mitad.** La segunda —qué puede redactarle a quien decide— **espera el ADR de `V-7`**, y mientras tanto queda puesto el valor conservador |
| [SPEC-04](SPEC-04-dicho-por-usted.md) | Bloque «dicho por usted, no documentado en la carpeta» | defecto | `P-05` · `P-06` · G6 | **Ejecutada** — falta una pasada real |
| [SPEC-05](SPEC-05-la-marca-revisado.md) | Blindaje de la marca ` - REVISADO` | defecto | `PM-M-2` · G25 | **Ejecutada** — O-1, O-6 y O-7 pasan; O-2 a O-5 piden pasada real |
| [SPEC-06](SPEC-06-escritura-dirigida-del-estado.md) | `0-Estado del caso`: reemplazo dirigido, no reescritura | defecto | `PM-M-8` · G19 | **Ejecutada** — **con banco de 13 pruebas en verde**; falta una pasada real |
| ~~SPEC-07~~ | ~~Los doce hallazgos de `inventario-de-bienes`~~ | — | ~~`V-1`~~ | **RETIRADA — los doce ya estaban aplicados.** Auditados uno por uno el 2026-09-05 · [la auditoría](../technical-design/v0/notes-verification/auditoria-inventario-de-bienes-2026-09-05.md) |
| [SPEC-08](SPEC-08-indice-de-las-salidas.md) | Índice de las salidas de una pasada | defecto | `P-07` · G37 | **Ejecutada** — falta una pasada real |
| [SPEC-09](SPEC-09-preguntas-de-derecho.md) | `preguntas-de-derecho`: las dos puertas que le faltan | defecto | salvedad de `H-04` · `V-1` | **Ejecutada** — falta probar la inyección |
| [SPEC-10](SPEC-10-limite-del-texto-extraido.md) | El límite del material extraído, dentro de los `SKILL.md` | defecto | `H-16` · `EP-1.1-COORDENADA` | **Ejecutada** — falta una pasada real |
| [SPEC-11](SPEC-11-la-primera-instalacion.md) | La primera instalación: que empezar no dependa de preguntar | defecto | `H-08` · defecto abierto de SPEC-01 | **Ejecutada** — falta que alguien instale |
| [SPEC-12](SPEC-12-lo-que-la-pasada-atrapo.md) | Que cada pasada diga qué se corrigió a sí misma | defecto | `PM-M-1` (c) y (d) · G23 | **Ejecutada** en los once — falta una pasada real que produzca cifras |

> **Cuenta honesta, al 2026-09-05: siete escritas y ejecutadas, una retirada, dos que hoy son solo una fila de esta tabla.** «Pendiente» aquí significa que el archivo **no existe**. Ninguna de las siete está *cerrada*: **seis esperan una pasada real** sobre una carpeta de ella, y así lo dice cada una en su apartado 5. Ejecutada quiere decir que el cambio está en el código y que los observables que no dependen de nadie pasan — **no que el defecto esté comprobado muerto en uso**.
>
> **Y una diferencia que conviene no perder:** SPEC-06 es la primera que trae **pruebas automáticas** —trece, y comprobadas capaces de fallar con dos mutantes—. Las otras seis son texto dentro de los `SKILL.md` y su único banco posible es una pasada real. Eso no las hace peores; hace que **`PM-5.1-BANCO` siga siendo el ítem que más pesa del lado del método**.

### Lo que las dos primeras ejecuciones enseñaron sobre el backlog

**SPEC-09 y SPEC-10 encontraron lo mismo que SPEC-02: el backlog estaba mal contado, en dirección contraria las dos veces.**

| Ítem | Lo que decía el backlog | Lo que había al leer el código |
|---|---|---|
| `H-05` | Abierto — «dos comandos consumen un archivo que nadie escribe» | **Ya cerrado y verificado en ejecución real** |
| `H-04` | Cerrable — «el bloque anti-inyección está en los nueve» | **Estaba en ocho.** Faltaba en la única skill cuyo trabajo es negarse |
| `H-16` | Parcial — «no consta la regla dentro de los `SKILL.md`» | **No constaba en ninguna de las nueve**, ni en la de revisión de rigor |
| `H-10` | Abierto — «la guía publica `/cronologia` como fiable» | **La guía ya advertía de las dos formas.** El defecto real era que **no existía hoja de instalación** |
| `H-11` | Abierto, dos mitades — «`inventario-de-anexos` sin regla de no sobrescritura; `estado-del-caso` reescribe sin copia previa» | **Las dos mitades cerradas.** La regla está en `inventario-de-anexos` §1 y la copia previa en `estado-del-caso` Fase 6.4. Lo vivo era otra cosa: `PM-M-8`, que no es la pérdida sino **la copia** |
| `PM-M-2` | Abierto | **Vivo y entero.** Es el primero que resulta estar exactamente como decía |
| `V-1` — los doce hallazgos de `inventario-de-bienes` | Abierto, «tres graves, sin aplicar», **primer puesto de mi lista** | **Los doce aplicados**, más las dos adiciones del Control 7 y los recortes del Control 5. La crítica se aplicó y **nadie cerró el ítem** |
| `P-05` · `P-06` · `P-07` | Abiertos | **Vivos y enteros.** Salieron de un pase real, no de una lectura de diagnóstico |

> **Seis de seis en el primer grupo, y el corte está donde se esperaba.** Ningún ítem **que salió de leer documentos de diagnóstico** resultó estar como decía. Los cuatro que **salieron de un pase real** —`PM-M-2`, `P-05`, `P-06`, `P-07`— estaban vivos y exactos, los cuatro.
>
> **Y `V-1` es el más caro de los seis**, porque no falló en un detalle: **puso en primer lugar de mi lista un trabajo ya hecho**, con el argumento más fuerte que tenía —«defectos graves en producto desplegado, y nadie los está contando»—. Su causa es distinta de las otras cinco: ahí la crítica **se aplicó** y nadie cerró el ítem. Eso no lo arregla releer más; lo arregla **cerrar el ítem en el mismo commit que aplica el arreglo**, que es lo que esta capa hace por construcción y lo que un documento de crítica suelto no hace.
>
> **Esa es la regla que sale de nueve verificaciones, y es más útil que la regla 4:** *un ítem que nació ejecutando el producto describe un defecto real; uno que nació leyendo un documento sobre el producto, la mitad de las veces no.* Los ~108 identificadores restantes se leen con esa lente: **primero los que tienen un pase detrás.**

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

**Las cuatro que podía escribir y ejecutar solo, están hechas** (2026-09-05): SPEC-05, SPEC-06, SPEC-04 y SPEC-08. Tres son texto dentro de los `SKILL.md`; SPEC-06 añadió además el séptimo programa del plugin y el primer banco de pruebas de la oficina.

**Lo que queda de mi lado, y en este orden:**

| # | Qué | Por qué en ese puesto |
|---|---|---|
| ~~1~~ | ~~**SPEC-07**~~ **RETIRADA el 2026-09-05:** los doce hallazgos ya estaban aplicados | — |
| 1 | **Una pasada real** que cierre los observables pendientes | **Nueve specs ejecutadas.** El 2026-09-05 se hizo una **pasada de escritorio** sobre un expediente sintético (`evals/casos/caso-02-sintetico-autoridad`) que subió un peldaño: [lo que aguantó y lo que se cayó](../technical-design/v0/notes-verification/pasada-de-escritorio-2026-09-05.md). **Encontró dos defectos, los dos míos y los dos de esa semana**, ninguno visible leyendo la spec. **No hay razón para creer que la proporción sea distinta en las siete a las que todavía no se les ha puesto nada delante** |
| ~~2~~ | ~~**`PM-M-1`, instrumentar**~~ **HECHA la mitad, el 2026-09-05 — SPEC-12.** Las partes (c) y (d) son texto y están en los once; (a) y (b) necesitan los logs de una corrida | Quedan del lado de la pasada real |
| ~~3~~ | ~~**SPEC-03** — contexto B~~ **HECHA la mitad, el 2026-09-05.** El vocabulario, la simetría obligatoria y la prohibición de orientar están en los once. Lo que falta **no es trabajo mío**: es el ADR de `V-7` | — |

> **Y una cosa que el plan daba por mía y no lo es.** `BACKLOG` §6 fila 1.3 pone *«correr el banco de evaluación que ya existe»* en «Puedo empezar ya». **No puedo:** `evals/casos/caso-01-familia.json` dice en su propio campo `_material` que **el material no está en este repositorio y no lo estará** —son documentos de una clienta real, con datos de una menor—, y que quien mida necesita los dos PDF originales, que custodia el dueño. Además el fixture **está invalidado por su propia nota desde el 2026-08-26**. Correr el banco es del bloque 0, no del 1.

**SPEC-03 —contexto B— es la más valiosa y la más delicada:** cambia a quién le habla el producto en su único uso real. No es una corrección de redacción; toca qué puede y qué no puede proponerle un sistema a quien decide. Merece decidirse, no escribirse de una.

**No depende de mí, y bloquea más que todo lo anterior:**

| Qué falta | Quién | Qué desbloquea |
|---|---|---|
| Instalar el plugin una vez y decir cómo aparecen los comandos | Usted o ella | Cerrar SPEC-01 · imprimir la guía |
| Decidir **dónde se procesa el material** de ella | Usted | Entregar sin mentirle · licenciar |
| Decidir **qué es la primera versión** (`V-10`) | Usted | El orden de todo lo demás |
| Un ADR para `V-7` —autoridad apoyándose en salidas de IA— | Usted, con criterio jurídico | La spec de contexto B, y la venta |

**No están todas las que faltan.** El backlog tiene 112 identificadores; estas ocho tocan lo que más pesa **y solo del lado de los defectos**. Las capacidades del mapa de arriba necesitan primero las decisiones de esa tabla.
