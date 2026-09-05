# Segundo pase del arnés sobre un caso real — Salento, expediente [radicado del expediente]

**Fecha:** 2026-08-27/28. **Material:** 23 fotografías JPG (8 documentos, 23 páginas, 45,5 MB).
**Contexto:** B — la usuaria es abogada de la Inspección de Policía de Salento y actúa como
contradictor interno.

> **Nota de 2026-09-05 sobre esta línea.** Decía *«Ver `memory/contexto-b-inspeccion-salento.md`»*, y **ese archivo no está en el repositorio ni puede estarlo**: `memory/` es la carpeta que el asistente guarda por máquina, fuera del control de versiones. **El hecho no depende de ella** —está dicho aquí arriba, versionado, y es lo que se cita—, pero su ampliación **no la puede abrir nadie más**, y de ese hecho cuelgan hoy la fila `C-8` del backlog, `SPEC-03` entera y la pregunta de negocio 7. Se retira la remisión en vez de dejarla apuntando al vacío.

> ## CORRECCIÓN — 2026-08-28. Este documento se llamaba «Primer pase» y no lo era.
>
> **Hubo un pase real anterior:** el caso **el caso de familia**, el 2026-08-26 — 56 páginas, cuatro
> de los seis comandos, con sus salidas en la carpeta de ese caso, en `2-Borradores/`,
> **incluidos dos `.docx`**. Está documentado en `docs/PLAN-DE-MEJORA.md`, que además trae sus
> mediciones: 180 turnos, ~207 KB de salida, **50,8 M de contexto releído y ~3 M facturables**.
>
> **Las dos afirmaciones que este documento hacía en su encabezado eran falsas:**
>
> 1. **«Primer pase».** Era el segundo.
> 2. **«El proyecto llevaba tres fases sin un solo dato del trabajo real».** Falso. Lo que dice
>    `ESTADO-DEL-PROYECTO.md` §0.10 es algo distinto y más estrecho: que no hay datos sobre **la
>    frecuencia con que la abogada usa cada capacidad**. Confundí una cosa con la otra.
>
> **Por qué ocurrió, que es lo que importa:** escribí este documento **sin haber leído
> `docs/PLAN-DE-MEJORA.md`**, que existía desde el día anterior y contenía el diagnóstico, las
> mediciones y once mejoras numeradas. Es exactamente la enfermedad que este mismo corpus ya tiene
> documentada —dos ledgers con identificadores que colisionan, seis archivos para una capacidad— y
> la cometí yo mientras la citaba.
>
> **La regla que sale de aquí:** *antes de añadir un documento de planeación a este repositorio, hay
> que leer los que ya existen.* No es una cortesía: es la única forma de que el corpus no siga
> creciendo en anchura en vez de en profundidad.
>
> Lo que sigue es lo que se midió en el pase de Salento, y sigue siendo válido — pero léase como
> **el segundo** pase, y contra el primero, no en el vacío.

> ## NOTA SOBRE LOS IDENTIFICADORES — 2026-08-31
>
> Antes de publicar este repositorio se **retiraron de toda la historia** los identificadores de
> personas reales que yo había dejado en documentos versionados: cédulas, matrículas inmobiliarias,
> números de radicado, tarjetas profesionales y apellidos de las partes. Aparecen ahora como
> `[cedula 1]`, `[matricula A]`, `[radicado del expediente]` y similares.
>
> **Por qué:** el repositorio iba a un remoto, y con una cédula y un radicado se llega al expediente
> completo de un proceso activo. Escribir esas cifras aquí fue innecesario —el hallazgo era «12 de 12
> coinciden», y para eso no hacía falta transcribir ninguna— y es un error mío.
>
> Los hallazgos no pierden nada: «dos matrículas distintas» dice exactamente lo mismo que los dos
> números. **El material del caso nunca estuvo en este repositorio** y sigue sin estarlo.

---

## 1. Qué se ejecutó, y cómo

El plugin **no está instalado** (sin remoto, sin marketplace). Se ejecutaron los métodos **a mano**,
leyendo cada `SKILL.md` y siguiéndolo. Eso mide el método, no el producto empaquetado.

| Skill | ¿Se ejecutó? | Resultado |
|---|---|---|
| `hechos-con-prueba` | Sí | 26 hechos, con estado y localizador |
| `cronologia` | Sí | 5 grados de certeza; 8 eventos sin fecha |
| `inventario-de-anexos` | Sí | Tabla, discordancias, tres clases de faltante |
| `revisar-documento` | Sí, ×3 | Querella, auto y los dos poderes |
| `estado-del-caso` | Sí | Escrito y luego actualizado |
| `preguntas-de-derecho` | Sí | Se negó a responder derecho, como debe |
| `redactar-escrito` | **No, y correctamente** | Compuerta de hechos aprobados: no hay ` - REVISADO` |
| `inventario-de-bienes` | No | No aplica: no es separación ni sucesión |
| `workflows/20` (rigor judicial) | Sí, a mano | **Fue el método más útil de todos, y no es una skill** |

## 2. Lo que funcionó

1. **La compuerta de `redactar-escrito` funcionó de verdad.** Se pidió «ejecuta todas las skills» y el
   comando se detuvo solo, con las palabras exactas del SKILL. Es la primera vez que una regla dura del
   arnés se prueba contra presión real de un usuario. **Pasó.**
2. **La regla de no calcular fechas resistió.** La audiencia estaba fijada para el 19/08 y la revisión se
   hizo el 27/08: la tentación de escribir «hace 8 días» fue permanente y no se cedió una sola vez.
3. **`preguntas-de-derecho` se activó sola** al menos cinco veces (Ley 1801 vs «1806», art. 206 literal
   E vs f), qué se exige para acreditar la calidad de abogado). En todas se dijo que no.
4. **La distinción «quién produjo el documento» de `inventario-de-anexos` fue la que más valor produjo:**
   al aplicarla salió que de 8 documentos, 3 los produjo la propia querellante y **ningún tercero se
   refiere al inmueble**. Ese hallazgo no lo encuentra ningún otro método del arnés.
5. **La simetría obligatoria** evitó el error más fácil del contexto B: al plantear la falta de
   acreditación del apoderado de una parte, la misma carencia aparecía en la otra.

## 3. Lo que falló, o faltó

| # | Qué | Consecuencia |
|---|---|---|
| P-01 | **Ninguna pieza tenía capa de texto.** Todo se transcribió a ojo desde fotos | Cada cifra del expediente quedó marcada «por comprobar». Es H-16 del informe de crítica, materializado |
| P-02 | **El contexto B no está diseñado.** Los SKILL.md hablan de «la profesional», «su clienta», «el escrito que usted presenta» | Hubo que traducir el vocabulario en cada salida. Funcionó, pero a mano |
| P-03 | **El séptimo comando no existe.** `workflows/20` fue lo más útil y hay que ejecutarlo leyendo un dossier | Es la brecha de capacidad más cara del producto hoy |
| P-04 | **Markdown no le sirve a la usuaria.** Trabaja en Word | Se generaron 3 `.docx` con `docx` (npm). Es H-13, confirmado en campo |
| P-05 | **Sin `estado-del-caso` no hay dónde poner lo que el usuario dice y la carpeta no registra** | Se inventó un bloque «DICHO POR USTED, NO DOCUMENTADO EN LA CARPETA». El formato del SKILL no lo prevé |
| P-06 | **`cronologia` no tiene grado para «lo dijo el usuario en la conversación»** | Mismo problema que P-05, en otra salida |
| P-07 | **Nada consolida las salidas.** Doce archivos y ningún índice | Se escribió a mano un análisis forense que hace de documento de entrada |

---

## 4. El costo: de dónde se fueron los tokens

**Medición honesta:** no tengo un contador exacto de esta sesión. Lo que sigue es una estimación con la
fórmula pública de coste de imagen (`ancho × alto / 750` tokens) y el conteo real de lecturas.

| Concepto | Cuenta | Estimación |
|---|---|---|
| Lecturas de imagen (mitades de página, a ~2000×1880) | **~45** | ~5.000 tokens cada una → **~225.000** |
| Lectura de los 8 `SKILL.md` + dossiers del corpus | ~10 archivos | ~60.000 |
| Escritura de las 12 salidas + 3 `.docx` | — | ~90.000 |
| **Total aproximado del pase** | | **~375.000–400.000** |

> **El 60% del gasto fue mirar fotos.** Y no es un gasto que compre precisión: compra una transcripción
> del modelo que hay que volver a comprobar. Es el peor tipo de gasto posible — caro **y** no confiable.

**Por qué fueron ~45 y no 23:** cada página se partió en dos mitades para ganar resolución (46), y
varias páginas clave se releyeron para fijar la cita literal. La partición en mitades fue una decisión
correcta para la exactitud y duplicó el costo.

## 5. OCR local: PROBADO el 2026-08-28. El resultado no fue el que predije

Autorizado y ejecutado. `pip install rapidocr-onnxruntime` — sin binario externo, sin admin,
onnxruntime 1.29.0, carga de modelo 0,9 s. **Corrió sobre las mismas 23 fotografías.**

### 5.1 Lo medido

| Medida | Valor |
|---|---|
| Tiempo | 272 s sobre 46 mitades (11,8 s/pág.) · 145 s sobre 23 páginas completas |
| Texto extraído | **20.164 caracteres ≈ 5.041 tokens** |
| Líneas reconocidas | 581 · **11 % por debajo de 0,85 de confianza** |
| Comparación | ~225.000 tokens de lectura de imagen vs ~5.000 de texto |

### 5.2 Lo que salió muy bien: los identificadores

**12 de 12 datos críticos, exactos**, cotejados contra mi transcripción visual:
matrícula [matricula A] · matrícula [matricula B] · cédulas [cedula 1], [cedula 2], [cedula 3],
[T.P./C.C. del apoderado A] · tarjetas profesionales [T.P. del apoderado A] y [T.P. del apoderado B] · radicado [radicado del expediente] ·
PQRS [PQRS asociado] · escritura [numero de la escritura] · «Ley 1801».

Son exactamente los datos que más riesgo tenían de estar mal por lectura visual, y ahora están
**corroborados por un medio independiente**. Eso es un resultado real y no lo esperaba tan limpio.

### 5.3 Lo que salió mal, y es más importante

**a) Extracción parcial que falla en silencio.** En varias páginas —el auto sobre todo— RapidOCR
devolvió una fracción del cuerpo **sin error alguno**. Cuatro afirmaciones mías no aparecieron:
«ley 1806», «bienes de uso público», «19 de agosto de 2026», «afectación indebida». No porque
estuvieran mal: el OCR capturó *«publico.»*, *«despacho.»* y *«querella.»* — las colas exactas de
esas mismas frases. Leyó el final del párrafo y perdió el resto.

> **Un arnés que confiara en esta salida habría concluido que el auto no fija fecha de audiencia.**
> Ese es el modo de fallo que importa: no es ruido, es una ausencia que se lee como un hecho.

**b) Diacríticos rotos.** Los modelos por defecto son PP-OCR chino/inglés: escribe `C6digo`,
`aplicaci6n`, `senora`, `Restitucion`. **El texto no es citable como literal en español.**

**c) No se arregló subiendo resolución ni con preprocesado.** Se probaron `det_limit_side_len`
960 y 1600, y tres preprocesados (autocontraste, normalización local de fondo, y normalización
+ máscara de enfoque). Las cuatro variantes devolvieron las mismas 3 líneas en la página del auto.
~~La causa no es resolución ni contraste global; es el detector con foto de papel curvado y con brillo.~~

> **CORRECCIÓN — 2026-08-28.** Esa última frase es **falsa**, y la corrijo aquí en vez de borrarla.
> Una investigación posterior leyó el `config.yaml` y los modelos instalados en esta máquina:
>
> - **`Global.max_side_len: 2000` reduce la imagen antes de todo.** Las fotos de 4000 px perdían la
>   mitad de su resolución, siempre y en silencio. **La causa sí era resolución.**
> - **`det_limit_side_len` es un piso, no un techo**, porque `limit_type` viene en `min`. Subirlo de
>   736 a 960 y a 1600 no hacía absolutamente nada: **estuve moviendo una palanca desconectada.**
> - **`text_score: 0.5` descarta toda línea reconocida por debajo de esa confianza**, sin avisar ni
>   contarla. Tercer filtro silencioso.
> - Y los diacríticos no estaban rotos: **el diccionario del modelo no contiene `ñ`, `Ñ`, `¿` ni `¡`.**
>   Ningún preprocesado podía producirlos. Los tres que probé estaban condenados por construcción.
>
> **Lección de método, que vale más que el hallazgo:** cuando un experimento da resultado nulo en
> cuatro variantes, la primera hipótesis debe ser **que la palanca no está conectada**, no que la
> causa está en otra parte. Detalle completo y plan de corrección en
> `docs/PLAN-DE-COSTE-Y-PRODUCTIZACION.md` §7-bis.

**d) El control de cobertura que intenté no sirve todavía.** Medir «qué fracción de la tinta quedó
dentro de una caja de OCR» marcó 21 de 23 páginas como sub-extraídas, porque cuenta como tinta los
logos, el membrete negro, las sombras y el fondo. **Sin calibrar, no es un control: es una alarma
que suena siempre.** Queda como trabajo pendiente y no como cosa hecha.

### 5.4 La corrección a mi propia recomendación

**Lo que dije el 27/08:** que el OCR dividiría el costo por ~7. **Es falso para este material.**
Con fotos de papel, el modelo tiene que seguir leyendo las páginas, y ahí está el gasto.

**Lo que el OCR sí compra, por ~5.000 tokens y 4,5 minutos:**

1. **Corroboración independiente de todo identificador numérico** — el dato más caro de equivocar.
2. **Búsqueda dentro del expediente** (con la advertencia de los diacríticos).
3. Una vía barata de **detectar desacuerdos**: donde OCR y modelo difieran, va a «por comprobar».

**Arquitectura corregida:** el OCR **no reemplaza la lectura**, la **audita**. Corre primero, barato;
el modelo sigue leyendo; y cada cifra que el modelo transcribe se contrasta contra el OCR. El ahorro
grande de tokens solo aparece con PDF nativo o escaneo plano — no con fotografías de papel.

## 6. Lo que este pase deja para el producto

**Orden propuesto, de mayor a menor valor por unidad de trabajo:**

1. **Salida en `.docx` como forma nativa del arnés** (P-04). Confirmado en campo: ella trabaja en Word.
   Hoy funciona un script de `docx` (npm) con tablas reales; convertirlo en parte del producto.
2. **El séptimo comando: `revision-de-rigor`** (P-03), a partir de `workflows/20`. Es la única pieza del
   corpus convertible sin inventarle la forma, y fue lo más útil de todo el pase.
3. **Tubería de ingesta con OCR** (§5). Divide por ~7 el costo y **sube** la calidad de la cita.
4. **Variante de contexto B** (P-02): mismo método, vocabulario de autoridad, prohibiciones endurecidas.
5. **Bloque «dicho por el usuario, no documentado»** en `estado-del-caso` y grado equivalente en
   `cronologia` (P-05, P-06).
6. **Documento índice** que consolide las salidas de una pasada (P-07).
7. **Publicar el plugin.** Sigue sin remoto: ella todavía no puede instalar nada. Es la entrada 0 de
   `ESTADO-DEL-PROYECTO.md` §5 y no se ha movido.

## 7. Advertencia de método sobre este mismo documento

Un pase, un caso, un contexto. **No es una medición: es una observación.** Todo lo que dice «funcionó»
significa «funcionó una vez, con este material, con este lector». La única cifra dura de aquí es la del
§4, y es una estimación con su fórmula a la vista.
