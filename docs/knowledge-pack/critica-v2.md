# Segunda crítica del instrumento

**Fecha:** 2026-08-27. **Veredicto: NO pasa — tres vías siguen abiertas y la corrección abrió siete propias.**
**Estado: SIN APLICAR.**

---

# VEREDICTO: NO PASA

De las cinco vías, **tres siguen abiertas** (V2, V3, V5), una se cerró y volvió a abrirse por otra puerta (V1), y la única que se cerró limpiamente (V4) trajo una vía nueva. Además la corrección abrió **siete vías propias**. El instrumento mejoró mucho —el algoritmo pasó de leer cinco campos a leer diecisiete, y eso es real— pero sigue habiendo caminos por los que sale `CITABLE` una norma cuya vigencia nadie comprobó.

Archivos: `C:/Users/HITMA/Desktop/legal-workspace/docs/knowledge-pack/01-ficha-y-verificacion.md` · `C:/Users/HITMA/Desktop/legal-workspace/docs/knowledge-pack/02-contrato-de-consumo.md`

---

# I. LAS CINCO VÍAS, REINTENTADAS

## V1 — Artículo comprobado, ley entera servida — **cerrada en la ficha, abierta en la petición**

`02`:42-43 hace bien la contención: `peticion ⊆ alcance_comprobado`, y «más ancha, disjunta o NO COMPARABLE → `FUERA_DEL_ALCANCE_COMPROBADO`». Recorro A con `{norma_completa: no, articulos:["00"]}` y petición de norma completa: no contenida → sale. Cerrada.

**Pero `peticion` no está definida en ninguna parte.** `alcance_comprobado` tiene estructura obligatoria (`01` campo 2); `peticion` es «el alcance que se pide» (`02`:34) y nada dice **qué forma tiene ni quién la produce**. Y la regla que impide al modelo producir valores (`01`:133) enumera: las casillas de la ficha, y «los valores de la **consulta** (`02` §1 R3): **la fecha del caso y su tipo**». `materia` la aporta quien consulta (`02`:73). **`peticion` no aparece en ninguna de las dos listas.**

Luego el operando izquierdo de la única comparación que cierra V1 lo produce el modelo, traduciendo una pregunta en prosa a una estructura. «¿Puedo apoyarme en la Ley 0000?» se convierte en `{articulos:["00"]}` —contenido, `CITABLE`— o en `{norma_completa: si}` —fuera—, y quien elige es el intérprete generoso que `02`:25 identifica como la sexta vía. **V1 no se cerró: se movió del algoritmo a la entrada del algoritmo.**

Segundo agujero en el mismo punto: la relación de contención **entre niveles** no está definida. ¿`{incisos:["00.0"]}` ⊆ `{articulos:["00"], incisos:[]}`? Lectura estricta de conjuntos: no. Lectura jurídica natural: sí. El documento no lo dice, y «no comparable → fuera» solo salva si el implementador elige la lectura estricta.

## V2 — La norma reformada — **ABIERTA, y es el hallazgo principal**

`VIGENTE_CON_REFORMA_AL` existe, `CITABLE_CON_REFORMA` existe, la nota se transcribe siempre. Todo eso funciona **cuando ella encuentra la reforma**.

**Nada comprueba que la haya buscado.** `01`:164 ordena: «no se llegó a mirar la reforma → `VIGENCIA_NO_COMPROBADA`». Es prosa. No hay ningún campo que registre que el paso ocurrió, y por tanto **`VIGENTE_AL` escrito tras buscar reforma y no hallarla es literalmente indistinguible de `VIGENTE_AL` escrito sin mirar**. Sale `CITABLE` limpio, sin nota, sin aviso.

La asimetría prueba que es un hueco y no una decisión: para la **clase de fuente** el autor sí construyó la comprobación mecánica (A.5 lee `fuente_vigencia.clase`); para la **búsqueda adversa** de providencias sí creó un campo que B.4 lee; para la **búsqueda de reforma** no hay ni campo ni condición. La crítica proponía dos remedios (`02` de la crítica, V2): el quinto valor **o** `reformada_dentro_del_alcance: si|no|no_comprobado` con defecto seguro. El autor tomó el primero, que es el que **no es comprobable**, y la frase que acompañaba al segundo —«el valor por defecto tiene que ser el seguro»— se perdió con él.

Y A.5 no sirve de sustituto: consultar el Diario Oficial de la promulgación es `PRIMARY_OFFICIAL` y no dice nada sobre reformas posteriores.

Probabilidad previa de que el paso se salte, medida sobre el corpus: la columna `amendments_checked` de `06-colombian-law-coverage-ledger.md` vale **`GAP` en 22 filas y `NO_APLICA` en 7. Cero comprobadas.** Nadie en este proyecto ha registrado nunca una comprobación de reforma. El fallo es silencioso y su salida es la respuesta más tranquilizadora del contrato.

## V3 — Casilla vacía, valor mal escrito, etiqueta imprevista — **ABIERTA en la mitad de los campos**

La lista blanca funciona donde se aplicó: A.2, A.4, A.5, A.6 y A.3 tienen su renglón «cualquier otro o vacío». Pero `02`:31 promete más de lo que las siete condiciones cumplen: dice que **cualquier** casilla vacía no es citable, y la enumeración —que en una lista blanca es lo que manda— no cubre:

- **`verificado_por` (campo 10). No lo lee ni A ni B.** Ficha anónima con todo lo demás lleno → `CITABLE`, y la frase servida imprime «Comprobado por » con el hueco vacío. `01`:28 dice de este caso exacto: «no es una ficha a medias, es una ficha que el pack no sirve». Regla que vive solo en prosa: es V3 textual.
- **`verificado_el` (campo 11)**: no hay condición de que sea una fecha válida ni de que no sea futura. Vacío o malformado rompe el cálculo de A.1 sin resultado definido; futuro hace la ficha inmortal.
- **`fuente_identidad` (campo 5)**: puede ir vacía con `estado_identidad = IDENTIDAD_VERIFICADA`. La columna de vigencia tiene puerta con clase tipada; **la columna de identidad no tiene ninguna**.
- **`nota_de_vigencia`** es obligatoria con `VIGENTE_CON_REFORMA_AL` y con `VIGENCIA_PARCIAL_AL` (`01`:63, 65) y ninguna condición comprueba que esté llena: `CITABLE_CON_REFORMA` con nota vacía es alcanzable.
- **`pasaje` (providencia, campo 4)**: B no lo mira. `CITABLE_PRECEDENTE` con pasaje vacío, y la frase dice «sostiene la proposición … en ‹›».

Corolario contable: **`01`:29 afirma «el algoritmo consulta los doce campos de §2 y los nueve de §4». Es falso.** Medido: de los doce, 10 y 11 no se leen nunca y el 5 y el 9 solo se imprimen; de los nueve, el 4 y el 7 no se leen. La regla 5 del propio diseño está incumplida por el propio contrato.

## V4 — Providencia superada o sin búsqueda adversa — **cerrada**

B.3 y B.4 hacen exactamente el trabajo: `SUPERSEDED_OR_LIMITED` y `CONFLICTING` → `PRECEDENTE_SUPERADO_O_LIMITADO`; cualquier otro o vacío → `JURISPRUDENCIA_POR_VERIFICAR`; `busqueda_adversa` vacía o `JURISPRUDENCE_GAP` → `SIN_BUSQUEDA_ADVERSA`. Recorrí la rama con las cuatro combinaciones malas y no sale ninguna. Es la corrección mejor hecha del lote. (Reserva menor: `RELEVANCE_REVIEWED` se admite como citable, y `07`:28 lo define como «se comparó el pasaje con la proposición», un escalón por debajo de `PROFESSIONALLY_CONFIRMED`, «una persona competente validó el uso profesional». Admitir el escalón inferior es una decisión que el documento no argumenta.)

## V5 — Cita sin haber consultado el pack — **cerrada contra el olvido, ABIERTA contra la falsificación**

El `token_de_respuesta` cierra el camino «el modelo no preguntó y citó igual»: sin token no se publica. Pero el token **no tiene nada infalsificable**: es `codigo · identificador + alcance · verificado_el · fecha_de_consulta`, cuatro campos que un modelo puede escribir. No hay firma, no hay contador, no hay registro de respuestas servidas, y `02` §5 **no lleva `checksum` ni `version`**, así que un token no se puede resolver contra una versión del pack.

Y la prueba de banco de `02`:218 enumera cuatro condiciones de fallo: cita sin token, código no citable, token de ficha **caducada**, alcance del token que no contiene lo citado. **«Token que no corresponde a ninguna ficha» no está en la lista.** Un token inventado junto a una cita inventada pasa las cuatro. El modelo de amenaza de todo el instrumento es un modelo que fabrica citas plausibles; un token plausible es el mismo fallo un piso más arriba.

Segundo problema: la cuarta condición —«el `alcance_comprobado` del token no contiene lo que la entrega cita»— exige saber **qué cita la entrega**, es decir, parsear prosa. Es exactamente lo que `02`:23 declara imposible («el regex deja de servir el día uno del pack»). Tres de las cuatro condiciones son mecánicas; la que verifica el alcance no lo es.

---

# II. VÍAS NUEVAS QUE ABRIÓ LA CORRECCIÓN

**N1 — El renombrado planta en el catálogo la cadena que hace pasar A.2, en un campo marcado copiable.**
`01`:26 ordena sustituir `VERIFIED_OFFICIAL`/`FUENTE_OFICIAL_VERIFICADA` → `IDENTIDAD_VERIFICADA` en los 13 archivos. Comprobado en el catálogo: `temporal-law-matrix.md` lleva `status: VERIFIED_OFFICIAL` en **todas** sus filas y `normative-sources.md` lleva `FUENTE_OFICIAL_VERIFICADA` en la mayoría. El día después del renombrado, esos archivos dicen literalmente `IDENTIDAD_VERIFICADA` —el único valor que A.2 acepta— al lado de cada norma. Y la cuarentena de P0.b (`01`:143) alcanza **solo a las fechas** (`effective_from / to`): **la columna de estado no se pone en cuarentena.**
Peor: los dos términos no significan lo mismo. `temporal-law-matrix.md`:4 dice «`VERIFIED_OFFICIAL` verifica **el enlace y los metadatos indicados**»; `01`:57 dice que `IDENTIDAD_VERIFICADA` es «la persona **vio el texto en fuente oficial**». El renombrado funde dos estándares distintos bajo un token —que es la falla que este instrumento existe para impedir, cometida por su propio remedio, y es la tercera vez que aparece en este proyecto (tras `VERIFIED_OFFICIAL` y `VIGENCIA_POR_VERIFICAR`).

**N2 — La ventana de vigencia se comprueba por un solo lado. Es V1 otra vez, en el eje del tiempo.**
A.6 exige `fecha_del_caso >= vigencia_desde`. **No hay ninguna condición que acote `fecha_del_caso` por arriba.** Una comprobación firmada el `verificado_el` no dice nada sobre lo que pasó después, y sin embargo un caso posterior a la comprobación pasa A.6 y sale `CITABLE`. Con cadencia de 12 meses, hasta un año de vigencia no comprobada se sirve como comprobada. Y los dos textos servidos afirman una ventana cerrada que el algoritmo nunca impone: `CITABLE` dice «vigente al ‹fecha› **para** un caso cuya fecha es ‹otra›», y `FUERA_DE_LA_VIGENCIA_COMPROBADA` dice «la vigencia comprobada **va de X a Y**». El límite superior existe en la frase y no en el código. La corrección arregló la unidireccionalidad en el alcance y la dejó intacta en el tiempo.

**N3 — Las providencias no caducan nunca.**
B.1 dice «hoy <= `revisar_antes_de` calculado (§6)». `revisar_antes_de = min(verificado_el + cadencia, acortamiento_manual)`, y **la tabla de cadencias de `02`:181-187 está escrita entera sobre `estado_vigencia`**, campo que una providencia no tiene (es justamente el argumento de `01`:111 y `02`:57 para darles rama propia). Ninguna fila aplica → `cadencia` indefinida → con `acortamiento_manual: null`, `min` indefinido → **B.1 no puede fallar nunca**. Una providencia firmada hoy sigue siendo `CITABLE_PRECEDENTE` en 2040. La corrección separó la rama B y se olvidó de separar la cadencia.

**N4 — Un problema de vigencia servido bajo el código de identidad. H8 al revés.**
`02`:83-84: dos fichas del mismo identificador que «discrepan **en la vigencia** → `CONFLICTO_DE_FUENTES`». Ese código está definido (`02`:105) como `estado_identidad = CONFLICTO_DE_FUENTES` y su frase dice «dos fuentes oficiales discrepan **sobre** `LEY-0000-0000`». `01`:59 promete lo contrario en dirección única: «un problema de identidad nunca se sirve bajo un código de vigencia». La corrección cumplió esa mitad y creó la simétrica: un problema de vigencia se sirve bajo un código de identidad, con una frase que habla de fuentes cuando el conflicto es entre fichas.

**N5 — R2 no está definida para respuesta múltiple, y la lectura generosa reinstala «la mejor coincidencia».**
`02` §2.D devuelve **todas** las fichas coincidentes, cada una con su respuesta, y el caso es el normal, no el raro: P2 empuja a estrechar, luego habrá varias fichas por norma. Si vuelven `CITABLE` (art. 00) y `VIGENCIA_NO_COMPROBADA` (art. 11), R2 dice literalmente que «una respuesta distinta de una de las cuatro citables cierra el turno» — o sea, el turno se cierra pese a haber una citable. La otra lectura es que el consumidor se queda con la citable, que es exactamente «el pack elige la mejor coincidencia» trasladado del pack al consumidor, es decir, el H6 que D dice haber cerrado. El documento no dice cuál de las dos.

**N6 — El primer portón del algoritmo depende de interpretar la nota que el pack tiene prohibido interpretar.**
A.1/B.1 necesitan `cadencia`, y la fila 3 de `02`:185 la fija para el caso «la nota registra un cambio con fecha futura … o el día anterior a esa fecha futura si es antes». Eso exige **leer `nota_de_vigencia` y extraerle una fecha**. `01`:47 dice del campo 9: «el pack **nunca la interpreta** y la transcribe literal». Las dos no pueden ser verdad. Si el implementador respeta `01`, la fila no se aplica nunca y las fichas con cambio pendiente —las peligrosas— caen a la cadencia larga de 12 meses.

**N7 — El interruptor de 18 meses lo resetea cualquier ficha nueva.**
`ultima_reverificacion = max(verificado_el)` sobre todos (`02`:151). Corrige el autolimpiado de H13, y crea el espejo: **una sola ficha nueva rejuvenece el reloj global del pack entero**. Verificar un registro cada diecisiete meses mantiene el pack encendido indefinidamente con veinticinco fichas podridas dentro. La magnitud que quería medirse —«¿hay alguien manteniendo esto?»— se responde con el máximo, que es la medida menos representativa del conjunto.

**N8 — `min()` no es total, y el único ejemplo del instrumento lo demuestra.**
`SIN_VIGENCIA_DESDE` tiene cadencia «`no aplica`» (`02`:186): esas fichas son inmortales y `CITABLE_SIN_VIGENCIA_HOY` para siempre. Y `acortamiento_manual: null` —el valor de la ficha de ejemplo, `01`:82— entra en un `min` sin que se diga qué devuelve.

**Menores, del mismo recorrido:** las providencias no tienen campo `materia`, así que no alimentan `materias_declaradas` (`02`:140) y el pack puede servir `CITABLE_PRECEDENTE` en una materia que él mismo declara excluida. Y el manifiesto obligatorio de `boundaries.md`:176-190 sigue sin cumplirse: falta `provenance.source`, `checksum`, `id`, `version`, `procedure_type` y `applicable_roles[]` — el `checksum` importa porque sin él no hay a qué resolver un token (V5).

---

# III. LAS CUATRO COMPROBACIONES

**¿Veinte minutos? No. Sobra aproximadamente la mitad.**
Medido: **410 líneas, 7.227 palabras, 46,5 KB**, diez tablas y dos bloques de algoritmo. En prosa técnica española eso son 35-45 minutos, y el bloque de `02` §2 no se entiende en una pasada. Lo que sobra no es relleno, es **duplicación entre los dos archivos**: el argumento «el grep muere el día uno del pack» está entero tres veces (`01`:13, `02`:23, `02`:218); «la unidad de entrega es la ficha, `v0.1` = 5-8 registros» dos veces (`01`:185-187, `02`:219); «el pack no elige» cuatro (`01`:59, `02`:84, `02`:105, `02`:125); «la nota se transcribe literal» cinco. Además `01` §1 regla 3 (33 ocurrencias, 13 archivos) y `01` §3 (lo que se propuso y no entra) son arqueología de diseño y ticket de migración: no los necesita ni quien llena una ficha ni quien implementa la tabla. Recortando duplicación y arqueología, el núcleo operativo cabe en ~250 líneas y sí se lee en veinte minutos.

**¿Escribió derecho el autor? No. Verificado con grep.**
- Patrón `(ley|decreto|código|acto legislativo|resolución|sentencia|circular) + número`: **13 coincidencias, todas `LEY-0000-0000`**. Cero normas reales.
- Fechas `(19|20)\d{2}-\d{2}-\d{2}`: **2**, ambas «Fecha: 2026-08-27» en la cabecera. **Ninguna fecha de vigencia.**
- `art\. N` / `inciso N`: **6**, todas `art. 00`.
- `C-\d+` / `T-\d+` / `SU-\d+`: **0**.
La regla se cumplió sin excepciones. La única afirmación sobre el mundo (`01`:136, los portales no certifican vigencia) lleva su referencia al lado y está marcada como referencia, no como afirmación propia.

**¿La degradación funciona? A los doce meses sí; a los dieciocho, sí pero es rejuveneceble; en tres bolsillos, no.**
Simulado. **Mes 12+1:** con cadencia de 12 meses, toda ficha `VIGENTE_AL` supera su `revisar_antes_de`, A.1 falla y sale `PACK_CADUCADO` con nombre y fecha. `materias_declaradas` se calcula sobre fichas no caducadas → queda vacía → `recuento.citables_hoy = 0` viaja en cada respuesta. **No sigue con la misma cara: se apaga sola, y eso es lo mejor del diseño.** Un matiz: para una norma sin ficha en una materia que se pudrió, C responde `FUERA_DE_COBERTURA` —«el pack **no cubre** esta área, aquí no hay información de ninguna clase»—, que afirma más de lo cierto («cubría y caducó»). **Mes 18:** `hoy − ultima_reverificacion > 18` → apagado, `NO_TENEMOS_INFORMACION_SUFICIENTE`, identidad como dato no citable. Funciona.
Los tres bolsillos que no se apagan: **providencias** (N3, sin cadencia, inmortales), **`SIN_VIGENCIA_DESDE`** (N8, cadencia «no aplica»), y el **reloj global reseteable** por una sola ficha nueva (N7). Y el escalón `DEGRADADO` no es ninguno de los diecisiete códigos ni tiene frase propia.

**¿Sigue siendo llenable? Sí, y la aritmética aguanta.**
Contado contra el catálogo: **26 filas normativas** (verificado) × 12 campos = **312**; **4 providencias** (verificado: `J-CC-T379-2024`, `J-CC-T200-2026`, `J-CC-C522-2023`, `J-CC-C071-2024`) × 9 = **36**. **Total 348 casillas**, de ellas **172 decisiones de investigación reales**. No se añadió ningún campo al corregir, y eso es cierto: la corrección se pagó en condiciones del algoritmo, no en trabajo de la verificadora. Tiempos coherentes: 26 × 35 min ≈ 15 h + 3-5 h + 2,5 h ≈ 20,5-25,5, dentro de la banda declarada «≈18-26 h». `v0.1` de 5-8 registros = 60-96 casillas ≈ 4 h ≈ dos sesiones: correcto.
Un desliz aritmético: `01`:185 dice que «26 horas … son **once o doce sesiones** de dos horas». Son **trece**.

---

# IV. LO QUE HAY QUE CERRAR, EN ORDEN

**Bloqueantes (una sola de estas mantiene el veredicto en «no pasa»):**
1. **V2** — un campo que registre la búsqueda de reforma, con defecto inseguro: `reforma_buscada: si | no`, y `no` → `VIGENCIA_NO_COMPROBADA`. Sin esto el caso más frecuente del derecho sale `CITABLE` mudo.
2. **V1'** — tipar `peticion` con la misma estructura que `alcance_comprobado`, decir quién la produce (nunca el modelo) y definir la contención entre norma › artículo › inciso.
3. **V3'** — añadir a la lista blanca de A y B: `verificado_por` no vacío, `verificado_el` fecha válida y no futura, `nota_de_vigencia` no vacía cuando el estado la obliga, `pasaje` no vacío. Y corregir `01`:29, que hoy afirma algo falso.
4. **V5'** — quinta condición de fallo en la prueba de banco: token que no resuelve contra una respuesta servida. Exige registro de respuestas y `checksum`+`version` en el manifiesto.
5. **N3** — cadencia propia para providencias.
6. **N2** — acotar la ventana por arriba: `fecha_del_caso <= verificado_el` (o decir explícitamente por qué no, y quitar «va de X a Y» de las frases).

**Estructurales:** N1 (cuarentena de la columna de estado del catálogo antes del renombrado, y decir que los dos términos no significaban lo mismo), N4, N5, N6, N7, N8.

**De higiene:** materia en providencias; `DEGRADADO` como código con frase; los seis campos que faltan del manifiesto de `boundaries.md`; y el recorte de duplicación que devuelve el instrumento a los veinte minutos.