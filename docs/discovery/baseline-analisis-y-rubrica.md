# Baseline con Cowork — análisis, rúbrica y traducción a métricas

**Estado:** documento de método de la fase Discovery. **No es normativo.** Precedencia nivel 6 (kernel técnico §14): nada de lo escrito aquí redefine un ADR Accepted, el Technical Design ni el glosario.

**Audiencia: los dueños y quien adjudique los resultados. Este documento NO se le entrega a la profesional.** Lo que ella ve y hace vive en el protocolo de sesión y en la plantilla de bitácora (documentos hermanos de esta misma tanda, en `docs/discovery/`; **POR VERIFICAR** sus nombres exactos de archivo). Aquí sí se usa el vocabulario del proyecto, porque aquí nadie tiene que ser protegido de él.

**Qué es el baseline.** Entregarle una demanda real a **Cowork tal como está hoy**, sin nada de lo que hemos diseñado, y observar. **No se construye nada. No se persiste nada.** Es medición de un punto de partida.

**Qué se afirma aquí sobre Cowork: nada.** Este documento no supone ninguna conducta del producto de terceros. Lo que Cowork haga es exactamente lo que se registre en la bitácora, con la etiqueta `observed in current environment` y jamás `documented platform guarantee` (misma regla que `13-synthetic-benchmark.md` §16.12.4).

**Qué se afirma aquí sobre derecho colombiano: nada.** La rúbrica de gravedad **no declara consecuencias procesales ni disciplinarias**: **NO TENEMOS INFORMACIÓN VERIFICADA** sobre ellas y no se rellena con plausibilidad. La gravedad la califica **la profesional**, respondiendo una pregunta de su oficio (§2).

**Etiquetas en uso:** HECHO VERIFICADO / DECISIÓN APROBADA / PROPUESTA / HIPÓTESIS / SUPUESTO / POR VERIFICAR / RIESGO / DECISIÓN PENDIENTE / NO TENEMOS INFORMACIÓN SUFICIENTE.

---

## 0. Los cinco momentos de medición

El protocolo replica la forma del vertical slice para que los resultados sean comparables después (`vertical-slice-v0.md`, flujo aprobado). Todo lo que sigue se reporta **por momento**, nunca agregado en un solo número.

| Id | Momento | Equivalente en el slice | Qué se mira sobre todo |
|---|---|---|---|
| **M1** | Se le entrega el material del caso | pasos 1–7 (crear, incorporar, derivar) | Qué hace con material que no pidió; qué dice que leyó |
| **M2** | "Construyamos los hechos con su prueba" | pasos 8–9 (`fact-builder`, `propose_facts`) | El núcleo: hecho ↔ prueba. Aquí se miden casi todas las medidas |
| **M3** | Ella revisa lo producido | paso 10 (revisión humana) | Detección espontánea; coste de revisar; fatiga |
| **M4** | Se cierra y se vuelve **otro día** | pasos 13–14 (nueva sesión, `changes_since`) | Continuidad: qué sobrevive y qué se inventa de nuevo |
| **M5** | Entra un documento nuevo al final | pasos 15–17 (evidencia tardía, staleness) | Qué pasa con lo ya hecho: ¿se marca afectado, se ignora, se rehace solo? |

**Correspondencia con el eval sintético (PROPUESTA):** M2 ≈ MP-1/MP-2, M5 ≈ MP-3. La correspondencia es **de forma, no de escala**: los denominadores son distintos y las cifras **no se comparan directamente** (§3, regla de comparación).

---

## 1. Las preguntas que el baseline debe responder

Cada pregunta se formula para que la respuesta sea **comprobable** y, sobre todo, **refutable**. Una pregunta que no admite una respuesta que nos contradiga no es una pregunta: es una expectativa disfrazada.

Los cuatro fallos que justifican el proyecto entero, con nombre corto para el resto del documento:

- **F1 — Fabricación.** Inventa una norma, una sentencia, un documento, una persona, una cifra o una fecha que no existe en el material ni en el mundo.
- **F2 — Alegado tratado como probado.** Presenta como acreditado lo que solo está afirmado por una parte, o borra la diferencia entre "esto lo sostenemos" y "esto está soportado".
- **F3 — Pérdida del hilo.** Entre una sesión y otra pierde lo trabajado, lo contradice, o lo reconstruye distinto sin avisar.
- **F4 — Falta de rastro.** No queda de dónde salió cada cosa: la afirmación existe, el origen no, o el origen es una referencia que no permite llegar al pasaje.

### Bloque A — ¿Existen los cuatro fallos con material real?

| # | Pregunta | Dato que la responde | Qué respuesta nos refutaría | Quién verifica y cómo |
|---|---|---|---|---|
| A1 | ¿Aparece **F1** en alguno de los cinco momentos? | Al menos un incidente registrado verbatim con: qué afirmó, qué es lo cierto, cómo se comprobó | Cero incidentes F1 en dos pasadas completas, con muestra ciega verificada (Bloque D) | Búsqueda del nombre/cifra/fecha en el material entregado; para citas jurídicas, la profesional en su fuente habitual |
| A2 | ¿Aparece **F2**? | Un hecho enunciado en tono asertivo cuyo único respaldo es la declaración de la propia parte, sin decirlo | Todo hecho llega marcado con su grado de respaldo, o el sistema lo distingue al preguntárselo | Lectura de la salida (no requiere abrir el material) + juicio de la profesional |
| A3 | ¿Aparece **F3**? | En M4: algo dado por incorporado que reaparece distinto, se olvida o se rehace | En M4 reconstruye lo trabajado sin inventar y sin contradecirse | Comparación de la salida de M4 contra el registro verbatim de M2/M3 |
| A4 | ¿Aparece **F4**? | Afirmaciones sin origen, u origen tan vago que no permite llegar al pasaje sin adivinar | Toda afirmación llega con referencia y la referencia lleva al pasaje | Intento real de ir del hecho al pasaje, cronometrado |
| A5 | ¿Aparece algún fallo **que no está en nuestra lista de cuatro**? | Incidentes que la rúbrica no sabe clasificar, registrados como `OTRO` con descripción | — (pregunta abierta por diseño) | Bitácora; se revisan al cierre |

**A5 no es decorativa.** Es la única pregunta del bloque que puede ampliar el alcance en vez de confirmarlo, y es la que más fácilmente se pierde si el conductor solo va a buscar lo que ya cree.

### Bloque B — ¿Con qué frecuencia?

**Regla dura: el baseline produce CONTEOS CON DENOMINADOR, no tasas.** Con una profesional y un caso, un porcentaje es una cifra con más precisión que información (§6, R1). Se escribe *"3 de 24 afirmaciones verificadas"*, nunca *"12,5%"*.

| # | Pregunta | Cómo se cuenta | Denominador declarado |
|---|---|---|---|
| B1 | ¿Cuántas afirmaciones comprobables produce en total? | Numeración verbatim de la salida **antes** de verificar nada | — (es el denominador de casi todo) |
| B2 | ¿Cuántos incidentes por momento (M1…M5)? | Conteo por momento y por tipo (F1…F4, OTRO) | Afirmaciones comprobables de ese momento |
| B3 | ¿El perfil de fallos es **estable** entre pasadas? | Dos pasadas del mismo arranque, en sesiones distintas | Se reportan **las dos**, no su promedio |
| B4 | ¿La frecuencia cambia con el volumen de material? | Comparar M2 (material inicial) contra M5 (material acumulado) | Afirmaciones de cada momento |

**Definición de "afirmación comprobable"** (necesaria para que B1 signifique algo): una proposición que puede confirmarse o desmentirse abriendo el material entregado o consultando una fuente jurídica. **Se excluyen del denominador** la argumentación jurídica, las valoraciones y las recomendaciones de estrategia — no porque no importen, sino porque no se comprueban, y meterlas dentro infla el denominador y esconde la tasa de fallo.

### Bloque C — ¿Lo detecta ella sola, o hace falta comprobar?

Escala de detectabilidad, que se registra por incidente:

- **D1 — Espontánea.** Ella lo señaló sin que nadie le pidiera revisar, en el flujo normal de trabajo.
- **D2 — A petición.** Lo señaló al pedírsele expresamente que revisara la salida, pero **sin abrir el material**.
- **D3 — Solo con comprobación deliberada.** Solo apareció al abrir el documento, buscar el pasaje o consultar la fuente. Sin esa comprobación, habría pasado.

| # | Pregunta | Dato que la responde |
|---|---|---|
| C1 | ¿Qué proporción de los incidentes es D1? | Conteo por nivel de detectabilidad sobre incidentes totales |
| C2 | ¿Cuánto cuesta comprobar? | Minutos cronometrados por afirmación verificada, y total de la sesión de verificación |
| C3 | ¿La detección se degrada con el número de ítems revisados seguidos? | Número de orden del ítem donde deja de comentar uno por uno y empieza a aprobar en bloque |

**C3 responde, observando, la última parte de la pregunta de negocio 8** (*"¿cuántas puede mirar seguidas con atención de verdad?"*). El dato observado vale más que el número que ella misma estime, y alimenta directamente el **RIESGO de fatiga de revisión** de ADR-005.

### Bloque D — Los fallos invisibles (el bloque más importante)

**El fallo peligroso no es el que se ve: es el que pasa por bueno.** Un error visible cuesta un minuto; un error plausible, bien redactado y con una referencia de aspecto correcto, entra al escrito. Si el baseline solo registra lo que ella notó, mide su atención, no la fiabilidad del sistema — y sobreestimará al sistema exactamente en la dimensión que más importa.

Procedimiento (**PROPUESTA**, ejecutable en la sesión de verificación, separada de la sesión de trabajo):

1. **Numerar** todas las afirmaciones comprobables de M2 y M5, verbatim, antes de verificar nada.
2. **Pasada de reacción, sin abrir nada.** Ella marca cada afirmación como `LA DOY POR BUENA` / `ME HUELE MAL` / `ESTÁ MAL`. Esto fija D1/D2 y, sobre todo, **congela por escrito lo que dio por bueno**.
3. **Verificación total de lo sospechoso.** Se comprueban el 100 % de las marcadas `ME HUELE MAL` y `ESTÁ MAL`. Son pocas y son baratas.
4. **Muestra ciega de lo aprobado.** De las marcadas `LA DOY POR BUENA` se toman **por sorteo** (no por olfato del conductor, no por orden de aparición) un número fijo acordado antes de empezar, y se verifica cada una contra el material. Si son pocas en total, se verifican todas.
5. **La cifra que importa:** *fallos hallados entre las que ella dio por buenas / afirmaciones dadas por buenas y verificadas a ciegas*. Se reporta como fracción con ambos números a la vista.

| # | Pregunta | Dato que la responde | Por qué es la más importante |
|---|---|---|---|
| D1q | ¿Cuántos errores sobreviven a su revisión? | Paso 5 del procedimiento | Es la única cifra que mide el riesgo real de que un error llegue a un escrito |
| D2q | ¿Qué **tipo** de error es el que sobrevive? | Clasificación F1…F4 de los hallados en la muestra ciega | **HIPÓTESIS a comprobar:** el error que sobrevive es el de atribución (F4/F2), no el de fabricación evidente (F1). Si se confirma, el producto debe optimizarse para eso |
| D3q | ¿Qué señal superficial lo hizo pasar? | Nota cualitativa por incidente: tono asertivo, cita con aspecto formal, cifra redonda, coherencia con lo que ella ya creía | Alimenta el diseño de la interfaz de revisión: qué hay que hacer visible |
| D4q | ¿Cuánto del total quedó **sin verificar**? | Afirmaciones no verificadas / total | **Obligatorio reportarlo.** Lo no verificado no se extrapola ni se supone bueno |

**Advertencia de honestidad que debe sobrevivir al informe final:** la muestra ciega acota el fallo silencioso, no lo elimina. Solo se descubre lo que se busca. Cualquier conclusión del tipo *"el sistema no comete X"* es ilegítima; la única forma correcta es **"no se observó X en las N afirmaciones verificadas"**.

---

## 2. Rúbrica de gravedad de cada incidente

### 2.1 El criterio es jurídico, no técnico

La pregunta que clasifica un incidente **no** es "¿qué tipo de error de máquina es?". Es una pregunta del oficio, que se le hace a la profesional en su lengua, sin una palabra de jerga:

> Imagínese que esto que acaba de decir el programa se le cuela tal cual en un escrito, con su firma, y ya está radicado. ¿Qué pasa?

Sus tres respuestas posibles **son** los tres niveles. El conductor no clasifica: transcribe la respuesta y la mapea. Si ella duda entre dos niveles, **se registra el nivel más alto y se anota la duda** (regla de desempate).

### 2.2 Los tres niveles

| Nivel | Nombre | Cómo lo dice ella | Anclas objetivas (tipología) |
|---|---|---|---|
| **G3** | **Contaminante** | *"Eso no lo arreglo con una corrección: me toca retractarme, o me deja mal, o cambia lo que estoy sosteniendo"* | Norma o sentencia inexistente, o que no dice lo que se le atribuye. Contenido atribuido a un documento que no lo contiene. Un hecho presentado como respaldado cuando su único respaldo es el dicho de la parte. Persona, cifra, fecha o documento inventados. Dos fechas o dos entidades distintas fundidas en una |
| **G2** | **Corregible con trabajo** | *"Lo detecto y lo arreglo, pero me cuesta tiempo — y me obliga a revisar todo lo demás porque ya no me fío"* | Referencia real pero inútil (no permite llegar al pasaje sin buscar a mano). Hecho relevante omitido. Contradicción real del expediente no señalada. Un hecho que quedó bien pero mal ubicado o mal ordenado |
| **G1** | **Ruido** | *"Lo veo, lo borro y sigo; no me cuesta nada"* | Hecho irrelevante para la demanda. Redacción pobre. Repetición. Detalle de color sin consecuencia |

**El corte entre G3 y G2 es el corte del proyecto.** G3 es todo lo que, si pasa, **el escrito afirma algo falso o afirma tener un respaldo que no tiene**. G2 cuesta trabajo pero no compromete la veracidad de lo que se firma. Si al ejecutar la sesión un incidente no encaja limpiamente en ese corte, el incidente se registra igual y la duda se lleva al cierre — **no se fuerza la rúbrica** (mismo criterio que `13-synthetic-benchmark.md` §16.2: la adjudicación es juicio, no dato, y por eso lleva bitácora).

### 2.3 Segundo eje: detectabilidad, y por qué no se mezcla con la gravedad

Hay una tentación fuerte de subir de nivel a los errores invisibles. **Se resiste:** gravedad y detectabilidad son dos hechos distintos y mezclarlos destruye ambos. Se registran por separado (D1/D2/D3 del Bloque C) y se combinan solo al **priorizar**:

| | D1 espontánea | D2 a petición | D3 solo comprobando |
|---|---|---|---|
| **G3** | Alta | Alta | **Máxima — esto es lo que justifica el producto** |
| **G2** | Baja | Media | Alta |
| **G1** | Nula | Nula | Baja |

La celda **G3 × D3** es la razón de ser de todo lo que hemos diseñado: daño alto que la revisión humana normal **no atrapa**. Si esa celda sale vacía tras la muestra ciega, hay una conversación de alcance que tener (§4.3).

### 2.4 Ficha mínima de incidente

Campos obligatorios en la bitácora, por incidente. Sin los tres primeros no hay incidente, hay una impresión.

`id` · `momento` (M1…M5) · **`verbatim`** (lo que dijo el sistema, copiado, sin resumir) · **`qué es lo cierto`** · **`cómo se comprobó`** (documento y pasaje, o fuente consultada) · `tipo` (F1…F4 / OTRO) · `gravedad` (G1…G3, **según la respuesta de ella**) · `detectabilidad` (D1/D2/D3) · `quién lo detectó` · `minutos de comprobación` · `¿involucra un dato sustituido en la anonimización?` (sí/no — ver §6, R6) · `dudas de clasificación`.

---

## 3. Traducción a las siete medidas del eval

Las siete medidas están definidas en `docs/technical-design/v0/13-synthetic-benchmark.md` §16 con numerador, denominador, punto de medición, fuente de datos, adjudicación y **qué no capturan**. Aquí se dice, sin adornos, **cuáles sobreviven a la ausencia de truth set y cuáles no**.

**Tres reglas de traducción, obligatorias:**

1. **Ninguna cifra del baseline se compara directamente con una cifra del fixture.** Denominadores distintos, material distinto, adjudicador distinto. Se comparan **perfiles y órdenes de magnitud**, jamás valores.
2. **Toda medida del baseline lleva prefijo `b_`** para que nunca se confunda con la medida homónima del eval en una tabla, una diapositiva o una conversación de pasillo.
3. **Lo que no se puede estimar se declara `NO ESTIMABLE`.** No se sustituye por una impresión con nombre técnico.

| Medida del eval | ¿Estimable sin truth set? | Medida `b_` del baseline | Numerador / Denominador | Qué la limita |
|---|---|---|---|---|
| **fact_recall** | **Parcialmente** | `b_omisiones_nucleares` | Hechos de la **lista ciega** de ella que la salida no produjo / hechos de esa lista | El denominador no es un truth set: es *"los hechos nucleares según la profesional"*. **Debe construirse ANTES de mostrarle la salida** (§6, R4); si se construye después, mide anclaje y no memoria |
| **unsupported_fact_rate** | **SÍ — y es la más limpia** | `b_hechos_sin_anclaje` | Hechos enunciados sin ninguna referencia de origen **y** sin marca explícita de "esto es solo lo que dice la parte" / total de hechos enunciados | Se juzga **leyendo la salida**, sin abrir el material. Ver nota ▼ |
| **source_attribution_precision** | **SÍ, con comprobación deliberada** | `b_fuente_correcta` | Referencias cuya fuente atribuida es efectivamente la que contiene el pasaje / referencias con fuente atribuida | Sin `selector` ni hash, "la fuente" es informal (un nombre de archivo, *"el contrato"*). En documentos compuestos, si no dice la página, se registra **`no verificable a nivel de página`** y no se cuenta como acierto |
| **evidence_link_precision** | **SÍ, descompuesta — y es la más valiosa del baseline** | `b_referencia_utilizable`, `b_pasaje_dice_eso`, `b_polaridad` | (a) referencias que permiten llegar al pasaje sin adivinar; (b) de esas, las cuyo pasaje **contiene** lo que se le atribuye; (c) de esas, las que presentan bien apoyo vs. contradicción / referencias propuestas | (a) **no** es `link_resolvability`: no hay selector formal que resuelva, mide utilidad de la referencia para un humano. (b) es el **link fantasma** — cita real, contenido inexistente — y es exactamente lo que la profesional sabe juzgar |
| **contradiction_recall** | **NO como recall** | `b_contradicciones_conocidas_no_señaladas` (conteo) + `b_contradicciones_inventadas` (conteo, sin denominador) | Contradicciones que ella conoce del caso y no fueron señaladas / las que ella listó **a ciegas** antes de ver la salida | No hay catálogo `EC-xx`. El denominador es su memoria del caso, que es incompleta y ella no falta a la verdad al olvidar. Las **inventadas** se cuentan sin denominador, igual que `spurious_contradiction_count` en el fixture |
| **irrelevant_fact_rate** | **NO como tasa** | `b_extraneos` | Conteo absoluto **y** fracción sobre hechos propuestos de los que ella marca *"esto no le sirve a la demanda"* | No hay catálogo `IR-xx`: el ruido posible no tiene denominador cerrado. Además la relevancia es juicio del oficio y **varía con la estrategia**: se registra el motivo del descarte, no solo el descarte |
| **hallucinated_entity_rate** | **SÍ — la más objetiva** | `b_entidades_inventadas` | Entidades nombradas que no aparecen en ningún material entregado ni existen en el caso / entidades distintas nombradas | Verificación **mecánica** (buscar el nombre, la cifra, el número de contrato en el material), no juicio. Es la medida que menos depende del adjudicador |

▼ **Nota sobre `b_hechos_sin_anclaje` — el baseline tiene aquí una ventaja que el eval no tiene.** El fixture exige medir `unsupported_fact_rate` **sobre intentos, incluidos los rechazados por el Core**, porque medir solo lo aceptado *"esconde la propensión del modelo detrás del gate del Core"* (§16.4). En el baseline **no hay Core, no hay gate y no hay rechazo**: todo lo que el modelo se inclina a hacer se ve tal cual. El baseline es, por construcción, la condición más limpia que tendremos jamás para esta medida. Conviene aprovecharlo y decirlo en el informe.

### 3.1 Medidas que el baseline añade y las siete no cubren

- **`b_resolucion_entidades`** (colapso / escisión). El fixture reconoce que con transcripción canónica L0 esta medida *"mide el caso fácil"* y **no es transferible**. El material real trae nombres parecidos, abreviaturas de banco, razones sociales casi idénticas: **el baseline mide el caso difícil**, que es el único que importa. Se reporta con los dos modos de fallo por separado, como en §16.9.
- **`b_cita_juridica_inventada`.** El fallo n.º 1 declarado del dominio (PF-004, kernel §12) **no está entre las siete medidas**: en el eval vive en `prohibited_assertion_rate` (`PA-02`). Se cuenta aparte, y con consecuencia de alcance (§4.4).
- **`b_continuidad`** (M4) y **`b_obsolescencia`** (M5): binarias por corrida, no tasas — homólogas de `staleness_surfaced` y `no_auto_regeneration` (§16.11). ¿Reconstruyó sin inventar? ¿Marcó lo anterior como afectado, o lo rehízo por su cuenta?
- **`b_coste_verificacion`**: minutos de la profesional por afirmación verificada. No es una medida de calidad del modelo; es la **magnitud económica del problema** y la vara de coste del §4.

---

## 4. La vara: qué tendría que hacer nuestro producto para superar esto

### 4.1 Se compara conducta, no notas

**Un sistema no supera al baseline por sacar mejores números en las mismas medidas.** Puede sacarlos peores y aun así ser superior: si produce menos hechos pero cada uno llega anclado, verificable en un gesto y con su estado epistémico a la vista, es mejor herramienta aunque su `b_omisiones_nucleares` empeore. Por eso la vara se expresa en **propiedades observables**, no en porcentajes que hoy nos inventaríamos.

### 4.2 Las seis condiciones de superación

Cada una es **necesaria**, se verifica **una por una** y se responde sí/no con evidencia de la corrida.

| | Propiedad | Cómo se observa | Relación con el baseline |
|---|---|---|---|
| **V1** | **Ningún hecho sin origen adjunto, y del hecho al pasaje en un gesto** | Se toma cualquier hecho del expediente y se pide su respaldo; se cronometra | Se compara contra `b_hechos_sin_anclaje` y `b_referencia_utilizable`. Aquí el producto no "mejora una tasa": el Core **rechaza el intento** (F6 del slice). Lo que hay que medir entonces es **cuánto contenido útil se pierde** por ese rechazo — el coste de la disciplina |
| **V2** | **Alegado ≠ acreditado, visible sin preguntar** | Se mira la salida sin hacer ninguna pregunta: ¿se distingue lo propuesto de lo incorporado, y lo que solo sostiene la parte? | Contra los incidentes F2 del baseline. En v0 la distinción realizable es `PROPOSED → ALLEGED` con revisión humana de por medio; **`DETERMINED` no tiene productor en v0** (addendum v0.3 B.5) y no se le puede pedir al producto que lo demuestre |
| **V3** | **Volver otro día no depende de la memoria de la conversación** | Misma pregunta de reanudación, a los N días, en sesión nueva: lo incorporado sigue incorporado, lo pendiente aparece como pendiente sin que ella lo recuerde | Contra los incidentes F3 y contra `b_continuidad` |
| **V4** | **Material nuevo marca lo anterior como afectado, y no rehace nada solo** | Se incorpora el documento tardío y se observa: ¿aparece la marca de afectado? ¿regeneró algo sin que se lo pidieran? | Contra `b_obsolescencia`. Un sistema que **rehace solo** es peor que el baseline aunque acierte más |
| **V5** | **Cero afirmaciones presentadas como comprobadas que no lo estén** | Repetir el procedimiento de muestra ciega del Bloque D sobre la salida del sistema | Contra la celda **G3 × D3**. Aquí la vara **no es una tasa a optimizar**: cualquier G3 que sobreviva es un defecto de diseño y se trata como tal |
| **V6** | **Coste total comparable, verificación incluida** | Minutos de la profesional de punta a punta, en ambos lados | Superar en propiedades y costar el triple **no es superar**. El baseline paga la verificación al final y de golpe; el producto la paga repartida. Se comparan los totales, no las sensaciones |

**Lo que queda declarado como no cubierto, en vez de disimulado:** si el baseline exhibe citas jurídicas inventadas (`b_cita_juridica_inventada` > 0), el producto v0 **no lo previene**: `verify_legal_source` está fuera de la superficie y ningún Knowledge Pack se carga (DECISIÓN APROBADA, vertical slice, *non-goals*). Eso debe escribirse así en el informe. Un producto que no ataca un fallo y no lo dice está mintiendo por omisión.

### 4.3 Y si el baseline sale BUENO

Tres desenlaces posibles. Los tres son resultados, no notas del examen.

**(a) Los cuatro fallos aparecen y hay incidentes G3 que ella no detectó (celda G3 × D3 poblada).** El alcance actual queda confirmado con evidencia y no con convicción. Es el desenlace que esperamos; es también el que más fácil nos ciega, porque confirma lo que ya creíamos (§6, R4).

**(b) Los fallos aparecen, pero son G2 y sobre todo D1/D2 — ella los caza sola.** El valor del producto **se desplaza**: deja de estar en *prevenir* el error y pasa a estar en *dejar rastro y abaratar la verificación*. El producto se estrecha hacia custodia, provenance y continuidad, y suelta la ambición de mejorar la extracción. Es un producto más pequeño, más barato y probablemente mejor.

**(c) Los fallos casi no aparecen, o son G1.** Entonces hay que estrechar el alcance de verdad, y posiblemente mucho: puede que lo único que falte sea persistencia, trazabilidad y continuidad entre sesiones — y no un Core con gates, propuestas y autorizaciones. O puede que el cuello de botella real esté en otra parte del oficio que aún no hemos mirado.

**Este resultado sería valioso y no un fracaso, y conviene decirlo antes de conocerlo, no después.** Descubrirlo ahora cuesta unas horas de observación; descubrirlo construyendo cuesta meses de trabajo tirados a la basura. El baseline es la operación con mejor relación entre lo que cuesta y lo que puede ahorrar de todo el proyecto, **precisamente porque puede matarlo barato**.

**Dos cautelas que impiden sobreleer un baseline bueno:**

- **Ausencia de evidencia ≠ evidencia de ausencia.** La conclusión legítima es *"no reprodujimos el problema en este caso, con este material, en estas pasadas"*. Nunca *"el problema no existe"*.
- **Un baseline bueno no invalida ADR-001.** Que el operador se porte bien en una corrida no lo convierte en confiable: la razón de tratarlo como cliente externo no confiable es estructural y no estadística. Un desenlace (c) reduce el **tamaño** del producto, no el **principio** de diseño. Confundir las dos cosas sería el error de lectura más caro posible.

---

## 5. Decisiones abiertas que este baseline puede cerrar

La ventaja de observar sobre preguntar: **una profesional puede estimar mal su propio ritmo sin faltar a la verdad** (así lo reconoce ya `business-questions-next.md`). Aquí no se le pregunta: se mira.

| Pregunta abierta | Qué observación la cierra | Qué NO cierra | Etiqueta al terminar |
|---|---|---|---|
| **P1 — Qué significa "acreditado"** | Las palabras que ella usa **al corregir** en M3: cuándo dice *"eso está probado"*, cuándo *"eso lo estamos alegando"*, cuándo cambia de una a otra. Se transcribe verbatim, no se parafrasea | El mecanismo de transición (actor humano, motivación, links valorados) — está fijado en ADR-003 y no depende de esto | Insumo para el **naming** del `kind` de `DETERMINED` y el texto de interfaz |
| **P2 — Canales de recepción de evidencia** | Dónde estaba materialmente el material del caso y qué tuvo que hacer para reunirlo para la sesión. **Se observa el proceso, no se copian los datos** (no se persiste nada) | Qué metadata expone cada conector (**POR VERIFICAR**, ADR-006) | Prioridad real de conectores post-slice; contenido del sobre de origen |
| **P3 — Volumen** | El tamaño del expediente real: cuántos documentos tiene, cuántas horas de grabación, qué pesa | El **volumen semanal**: un caso no da una semana. Sigue **SUPUESTO** | Orden de magnitud **por expediente** — que es justo lo que dimensiona el presupuesto de `get_case_context` (pendiente de ADR-004) |
| **P4 — Fuentes jurídicas** | A dónde va **de verdad** cuando duda de una cita, observado en el momento de verificar (Bloque D) | Los términos de uso de bases comerciales (**POR VERIFICAR**) | Insumo del Knowledge Pack Colombia |
| **P8 — Ritmo de trabajo** | Duración de la sesión; si le entra material nuevo del mismo caso mientras trabaja; qué hace más veces, consultar o incorporar; y **C3**: en qué número de ítem deja de revisar con atención | Nada crítico: las dos decisiones que sostiene (separación de logs, concurrencia optimista) **no cambian con la respuesta** | Confirma o desmiente **BA-01** y **BA-02** en orden de magnitud; insumo del `expires_at` por defecto y del **tamaño máximo de propuesta revisable** |
| **Granularidad del par "hecho, prueba"** (§6 del glosario; hoy SUPUESTO) | **Se observa directamente**: cuando ella corrige una referencia, ¿apunta a una cláusula, a una página, a un pasaje, a un minuto? | — | Puede pasar de SUPUESTO a observado, con la muestra de un caso |
| **Cómo imagina aprobar** (glosario §12) | En qué momento de M3 pide ver el documento entero en vez de fiarse del extracto | — | Insumo del diseño del canal de revisión (ADR-005 §5, DECISIÓN PENDIENTE) |

**Lo que este baseline NO cierra, y hay que dejar de esperar que cierre:** la pregunta 5 (personas que intervienen — hay una sola persona en la sesión), la 6 (backups — no se toca el equipo), la 7 (expediente oficial en contexto autoridad — el material es una demanda, contexto A; **NO TENEMOS INFORMACIÓN SUFICIENTE** sobre el contexto B y este ejercicio no la produce).

---

## 6. Riesgos del método

Sin adornos. Cada riesgo con una mitigación **ejecutable**, no con una buena intención.

**R1 — Una profesional y un caso no son una muestra. RIESGO alto, estructural, no eliminable.**
No hay mitigación que lo convierta en muestra. Lo que sí se puede es impedir que el informe hable como si lo fuera:
- **Prohibido el lenguaje de tasa** en las conclusiones: conteos con denominador, nunca porcentajes (§1, Bloque B).
- **Preinscripción:** este documento y la rúbrica se **commitean con fecha antes de correr la sesión**. Lo que no esté aquí antes, no puede presentarse después como predicción confirmada.
- Antes de mover el alcance del producto por un desenlace (b) o (c): **un segundo caso, de tipo distinto**, y a ser posible una segunda profesional.

**R2 — Efecto de ser observada, y efecto de complacer.**
Trabajará distinto porque la miran, y además **querrá ayudarnos**: si intuye que buscamos fallos, los buscará por nosotros; si intuye que queremos que funcione, callará dudas.
- El conductor **no comenta la salida en caliente**, no evalúa en voz alta, no dice *"¿viste? se equivocó"*, no celebra los aciertos.
- **La verificación se hace en un bloque separado**, después del trabajo, no intercalada.
- Se le dice explícitamente, y en serio, que **lo que se evalúa es el programa y no ella**. Esto no elimina el efecto observador, pero sí la ansiedad de desempeño, que es la parte que más distorsiona.
- La bitácora registra **cada intervención del conductor**, con hora. Una sesión sin intervenciones registradas es una sesión mal registrada, no una sesión limpia.

**R3 — Tentación de elegir un caso fácil… o uno demasiado difícil.**
El sesgo va en las dos direcciones: un caso cómodo para que salga bien, o un caso monstruoso para "demostrar" el fallo. Ambos invalidan.
- **Criterios de selección escritos ANTES de mirar los candidatos:** tipo de asunto, rango de número de documentos, que exista al menos una contradicción o una tensión probatoria conocida, caso ya terminado.
- **Ella elige** entre los que cumplen; **el conductor no ve el contenido antes** de la sesión.
- Se registran los **casos descartados y el motivo**. Un descarte sin motivo escrito es un dedo en la balanza.

**R4 — Quien conduce quiere que funcione (o quiere que falle).**
Es el sesgo más peligroso porque es invisible desde dentro y porque el desenlace (a) del §4.3 **confirma lo que ya creíamos**, que es cuando menos se mira.
- **La gravedad la firma ella, no el conductor** (§2.1). El conductor transcribe.
- **Los incidentes se registran verbatim ANTES de clasificarse.** Primero el hecho, después la etiqueta; nunca al revés.
- **La lista ciega de hechos nucleares y de contradicciones conocidas se construye ANTES de mostrarle la salida.** Si se construye después, el denominador queda contaminado por lo que acaba de leer y `b_omisiones_nucleares` mide anclaje, no memoria.
- **Separación de roles:** quien conduce no adjudica. Si solo hay una persona disponible, la adjudicación se hace **al menos 24 h después**, sobre el registro verbatim, y una segunda lectura la hace un dueño que no condujo.

**R5 — La adjudicación es juicio, no dato.**
Decidir que una afirmación "es" un fallo, o que una omisión "es" relevante, es el mismo punto frágil que el eval ya declara en §16.2. Mitigación idéntica: **criterio escrito de antemano, bitácora de cada duda, y ninguna duda resuelta en silencio**. Si al final hay más de dos o tres dudas por sesión, el criterio está mal escrito y hay que arreglarlo antes del segundo caso.

**R6 — La anonimización puede fabricar incidentes.**
Cambiar nombres y cifras sin cuidado rompe coherencias internas: fechas que dejan de cuadrar, dos nombres que ya no se parecen (o que empiezan a parecerse), un importe que ya no coincide con su comprobante. **Un incidente causado por una sustitución descuidada es ruido nuestro, no un fallo del sistema.**
- Sustitución **consistente y de la misma forma**: si un nombre era parecido a otro, el reemplazo debe seguir siendo parecido; si el banco abreviaba, la abreviatura se mantiene; las relaciones aritméticas entre cifras se preservan.
- La hace **ella** o la revisa ella.
- Todo incidente que involucre un dato sustituido se marca en la ficha (§2.4) como **posible artefacto de anonimización** y se reporta aparte.
- **SUPUESTO explícito, y honesto:** anonimizar no degrada la medición porque medimos razonamiento y no datos. Es una afirmación razonable, **no verificada**. Si el material sustituido resulta menos coherente que el original, sí la degrada.

**R7 — Una corrida es una anécdota (no determinismo del operador).**
- **Dos pasadas** del mismo arranque, con el mismo material, en sesiones distintas.
- **No se promedian**: se reportan las dos y se mira si el **perfil** de fallos es estable. Perfil inestable es, en sí mismo, un hallazgo de primer orden.

**R8 — El conductor guía sin querer.**
La calidad de la salida depende de cómo se pida, y el conductor sabe pedir "bien". Eso mediría nuestra habilidad, no el punto de partida de ella.
- **La primera petición de cada momento la formula la profesional con sus palabras**, y se registra literal.
- El conductor **no reformula, no sugiere, no reintenta**. Si algo sale mal por cómo se pidió, ese es exactamente el dato.

**R9 — Techo de la verificación.**
Solo se descubre lo que se busca. La muestra ciega acota el fallo silencioso; no lo elimina.
- **Reportar siempre `D4q`**: cuánto quedó sin verificar.
- **Prohibido extrapolar** de la muestra al total en el informe.

**R10 — Confidencialidad.**
Material real de un cliente entra a una herramienta de terceros. **NO TENEMOS INFORMACIÓN VERIFICADA** sobre qué hace el proveedor con ese material, y este documento no la inventa: el corpus ya registra los términos de proveedor como **POR VERIFICAR**. La decisión de qué material entra es **de los dueños y de ella**, no del método. Lo que el método sí exige: **no se persiste nada de la sesión en el repositorio** — la bitácora registra incidentes y conductas, no contenido del expediente.

---

## 7. Qué se entrega al terminar

Una sola pieza corta, con cinco partes:

1. **Respuestas etiquetadas a A1–A5**, cada una con la evidencia que la sostiene o con **NO TENEMOS INFORMACIÓN SUFICIENTE**.
2. **Tabla de incidentes** con la ficha de §2.4 completa, ordenada por prioridad (matriz de §2.3).
3. **Las cifras `b_`**, cada una con su numerador, su denominador y su procedimiento — **y las que quedaron `NO ESTIMABLE`, listadas como tales**.
4. **Las decisiones de §5 que quedaron cerradas**, con la observación concreta que las cierra, y las que siguen abiertas.
5. **Cuál de los tres desenlaces del §4.3** describe lo observado, y qué implica para el alcance.

**Criterio de fracaso del propio ejercicio** (sí, el método también se somete a una vara): si al terminar **no se puede responder A1–A4 con etiqueta y con evidencia**, el baseline no se ejecutó bien — y la conclusión correcta no es *"el problema no existe"* sino *"hay que volver a correrlo"*.
