# Crítica del instrumento de verificación

**Fecha:** 2026-08-27. **Veredicto: NO pasa la prueba — cinco vías.**
**Estado: SIN APLICAR.**

---

He leído los dos archivos, el contrato de `boundaries.md` §8, `04-source-governance.md`, `05-temporal-applicability.md`, `06-colombian-law-coverage-ledger.md`, `07-jurisprudence-governance.md`, el `source-catalog/` completo y `REFINADO-Y-FUENTES.md` §1.a. Resultado del examen.

---

# VEREDICTO

**La prueba no la pasa.** Encontré **cinco vías independientes** por las que el sistema sirve como `CITABLE` una norma cuya vigencia nadie comprobó, o cuya redacción vigente no es la comprobada, sin que nada lo detecte. Cuatro están en la tabla de decisión de `02-contrato-de-consumo.md` §2 (líneas 29-38) y una está en que nadie obliga a consultar el pack.

El diseño conceptual es correcto y la separación de columnas está bien pensada. **El fallo es que la tabla de decisión no implementa el diseño**: la ficha tiene doce campos y el algoritmo lee cinco. Los campos que contienen el trabajo caro —`fuente_vigencia`, `nota_de_vigencia`, `estado_uso`, `busqueda_adversa`— se llenan y nunca se leen. La corrección es acotada: no hay que rediseñar la ficha, hay que reescribir doce líneas de algoritmo.

---

# LAS CINCO VÍAS (la prueba del encargo)

## V1 — El alcance solo se comprueba en una dirección → se sirve la ley entera habiendo comprobado un artículo

`C:/Users/HITMA/Desktop/legal-workspace/docs/knowledge-pack/02-contrato-de-consumo.md:31`

```text
si  la petición es más fina que alcance_comprobado -> FUERA_DEL_ALCANCE_COMPROBADO
```

**Qué está mal.** La comparación es unidireccional. Ficha con `alcance_comprobado: "art. 00"`, `estado_vigencia: VIGENTE_AL <hoy>`. Petición: la norma completa. ¿Es la petición *más fina*? No: es más ancha. No entra por esa rama, la identidad está bien, la vigencia está bien, las fechas caen dentro → **`CITABLE`**. El pack acaba de afirmar como vigente una ley de la que comprobó un artículo.

**Por qué importa.** No es un caso de laboratorio: P2 (`01`:145) **empuja activamente a estrechar** — «estrechar es siempre legítimo y casi siempre más barato». El diseño garantiza que la mayoría de las fichas serán de artículo, y por tanto que la mayoría de las fichas son vulnerables a una petición de norma completa. Y el escenario exacto del encargo se construye solo: comprobar el art. 5 (vivo) de una ley derogada en todo lo demás, pedir la ley, recibir `CITABLE`.

**Corrección.** La prueba no es de finura sino de **contención**: `CITABLE` solo si `petición ⊆ alcance_comprobado`. Cualquier otra relación —más ancha, disjunta, o **no comparable**— cae en `FUERA_DEL_ALCANCE_COMPROBADO`. Y como `alcance_comprobado` es hoy texto libre («texto corto y cerrado» sigue siendo prosa), la contención no es computable: hay que darle forma mínima estructurada (`{norma_completa: si|no, articulos: [], incisos: []}`) o escribir explícitamente **«si no se pueden comparar, `FUERA_DEL_ALCANCE_COMPROBADO`»**. Hoy el algoritmo finge comparar dos cadenas de prosa.

## V2 — La norma reformada: la verificadora encuentra la reforma, la anota, y el pack tira la nota

**Qué está mal.** Es el caso que el encargo pedía buscar, y no hay dónde ponerlo. `estado_vigencia` tiene cuatro valores (`01`:41) y ninguno dice «rige, en redacción distinta a la original». P4 (`01`:153) ordena buscar «derogatoria, sustitución, **reforma** o decisión de control», pero sus tres desenlaces (`01`:154-157) solo contemplan derogación total, parcial, o nada. Una reforma que cambia la redacción del artículo sin derogarlo **alcanza todo el alcance y la norma sigue rigiendo**: `SIN_VIGENCIA_DESDE` es falso, `VIGENCIA_PARCIAL_AL` es falso, y el único valor que queda es `VIGENTE_AL` → **`CITABLE`**, con la frase «vigente al `AAAA-MM-DD`».

Peor: el campo 9 dice «el pack **nunca la interpreta**: se muestra tal cual a la abogada» (`01`:44), pero `02` §3 **solo transcribe `nota_de_vigencia` en la fila `VIGENCIA_PARCIAL`** (`02`:53). En `CITABLE` no aparece. Los dos archivos se contradicen, y la contradicción se resuelve tirando exactamente el dato que costó 10-15 minutos obtener.

**Por qué importa.** `06-colombian-law-coverage-ledger.md` tiene una columna `amendments_checked` y dice **`GAP` en las diez filas**. Nadie en el corpus ha comprobado una reforma nunca. El pack decide dejar fuera `modificada_por[]` (`01`:92) —decisión defendible por coste— y declara el riesgo en `02`:151, pero **el riesgo declarado se materializa como un `CITABLE` limpio**, no como una advertencia. Un riesgo asumido que sale por la respuesta más tranquilizadora del contrato no está asumido: está oculto.

**Corrección, y es barata porque el trabajo ya está hecho** (la verificadora hizo la búsqueda en P4, solo no tiene dónde escribir el resultado):
1. Un quinto valor: `VIGENTE_CON_REFORMA_AL AAAA-MM-DD`, o un campo booleano `reformada_dentro_del_alcance: si | no | no_comprobado`. Cero investigación adicional.
2. `no_comprobado` **degrada a `VIGENCIA_POR_VERIFICAR`**, no a `CITABLE`. El valor por defecto tiene que ser el seguro.
3. Novena respuesta `CITABLE_CON_REFORMA`, cuya frase diga: «la comprobación cubre el identificador y su vigencia, **no la redacción**».
4. `nota_de_vigencia` se transcribe literal en **toda** respuesta que lleve fecha, `CITABLE` incluida. Coste cero: ya está escrita.

## V3 — El algoritmo es lista negra, no lista blanca: `en otro caso -> CITABLE`

`02-contrato-de-consumo.md:37`

**Qué está mal.** El estado por defecto es servir. Todo valor de `estado_vigencia` que no sea literalmente `VIGENCIA_POR_VERIFICAR` o `VIGENCIA_PARCIAL_AL` termina en `CITABLE`: la casilla vacía, el espacio en vez de guion bajo, `POR_VERIFICAR` a secas, un valor con comentario detrás. `01` §5 regla 2 dice «ninguna casilla se queda vacía» — es disciplina humana, no una comprobación, y quien decide es el algoritmo.

Y hay algo peor que un typo. **P4 exige «al menos una fuente de clase `PRIMARY_OFFICIAL`» para escribir `VIGENTE_AL`** (`01`:156) — es la regla que separa «comprobé» de «el portal no dijo nada», la regla 4 de las que no se negocian. **El algoritmo no lee `fuente_vigencia` nunca.** Una ficha con `estado_vigencia: VIGENTE_AL <hoy>` y `fuente_vigencia: "no se localizó fuente de clase PRIMARY_OFFICIAL"` —la combinación literal del ejemplo de `01`:74— sale `CITABLE`. La regla más importante del procedimiento vive solo en prosa.

**Corrección.** Invertir la lógica: `CITABLE` **solo si** se cumplen todas las condiciones positivas, enumeradas; cualquier otra cosa, incluido un valor no reconocido, cae en `VIGENCIA_POR_VERIFICAR`. Y añadir como condición dura de `CITABLE`: `fuente_vigencia` no vacía **y** de clase `PRIMARY_OFFICIAL` (`04-source-governance.md` §4.1) — con la clase como campo tipado, no como texto dentro de la cadena de la URL, que es como está hoy (`01`:43).

## V4 — Las providencias entran por una tabla que no las mira

**Qué está mal.** La ficha de providencia (`01` §4) tiene 9 campos y **ninguno es `estado_vigencia`, `vigencia_desde` ni `alcance_comprobado`**. La tabla de decisión de `02` §2 está escrita para normas. Recorriéndola con una providencia: caducidad (pasa), alcance (no existe → no dispara), `estado_vigencia = VIGENCIA_POR_VERIFICAR` (no existe → falso), fechas (no existen → falso) → **`CITABLE`**.

Hoy no explota por un accidente: el campo 2 usa `IDENTITY_VERIFIED` en inglés (`01`:110) y el algoritmo compara contra `IDENTIDAD_VERIFICADA` en español, así que la rama de identidad lo atrapa por desajuste de cadena. **El día que alguien normalice esa etiqueta —que es justo lo que ordena `01` §1 regla 3— la vía se abre.** Estar a salvo por una errata no es estar a salvo.

Y lo decisivo: **`estado_uso` y `busqueda_adversa` no se leen en ninguna parte.** `01`:113 dice de `SUPERSEDED_OR_LIMITED` que «es el mecanismo entero contra eso [citar un precedente superado]». El mecanismo entero no está conectado a nada. Una providencia marcada `SUPERSEDED_OR_LIMITED`, o `CONFLICTING`, o con `busqueda_adversa: JURISPRUDENCE_GAP`, atraviesa el contrato sin que nadie la toque. Tampoco hay respuesta para ellas: las ocho de `02` §3 son todas de norma.

**Corrección.** O una segunda tabla de decisión para providencias, o extender la única que hay con ramas explícitas: `estado_uso ∈ {SUPERSEDED_OR_LIMITED, CONFLICTING, JURISPRUDENCIA_POR_VERIFICAR}` → nunca `CITABLE`; `busqueda_adversa` vacía o `JURISPRUDENCE_GAP` → nunca `CITABLE`; `proposicion_atribuida` distinta de la que se pide → `FUERA_DEL_ALCANCE_COMPROBADO`. Más dos respuestas: `PRECEDENTE_SUPERADO_O_LIMITADO` y `SIN_BUSQUEDA_ADVERSA`, con su frase. Y unificar el idioma de las etiquetas de identidad: hoy hay dos.

## V5 — Nadie obliga a consultar el pack, y el día que exista el pack se rompe la única prueba que hoy detecta el fallo

**Qué está mal.** El pack es un oráculo pasivo. R2 (`02`:15) cierra el turno *cuando el pack contesta algo distinto de `CITABLE`* — no cubre el camino en que el modelo cita sin haber preguntado. `02` §7.4 lo reconoce y remite a «una prueba de banco que **falle** cuando una entrega contiene una cita jurídica sin respuesta `CITABLE` detrás». Esa prueba **no es construible con lo que definen estos dos archivos**: ninguna respuesta del pack tiene identificador, así que la única forma de escribirla es un regex sobre la prosa de la entrega.

**Por qué importa, y esto es lo más serio del informe.** El regex sobre prosa es exactamente el instrumento con el que `REFINADO-Y-FUENTES.md` §1.a demuestra hoy la seguridad del producto (`grep -rE "Ley [0-9]|Decreto [0-9]|art\. [0-9]|C-[0-9]{3}/|T-[0-9]{3}/"` → cero coincidencias). **Ese instrumento deja de funcionar el día uno del pack**, porque a partir de ese día las citas son legítimas y el regex ya no distingue la buena de la fabricada. El pack retira la única comprobación mecánica que existe y no pone otra en su lugar.

**Corrección.** Cada respuesta del pack devuelve un `token_de_respuesta` (código + clave de ficha + `verificado_el` + fecha de consulta), y **toda cita jurídica en una entrega debe llevar su token al lado**. La prueba de banco pasa a comprobar tokens, no prosa: cita sin token → falla; token cuyo código no es `CITABLE` → falla; token de ficha caducada → falla. Es la diferencia entre una regla y un mecanismo, que es la distinción con la que abre `01` §0.

---

# LOS SIETE FRENTES

## 1. ¿Se puede servir un registro sin vigencia comprobada? — **Sí: V1, V3, V4.**

Añado dos hallazgos más de esa familia.

**H6 — No hay clave de ficha ni regla de selección entre varias fichas de la misma norma.**
*Qué está mal.* P2 empuja a estrechar, luego habrá varias fichas de `LEY-0000-0000` con alcances distintos (art. 5, art. 12). El algoritmo está escrito en singular («si la petición es más fina que `alcance_comprobado`») y nunca dice cuál ficha se elige. `02` §4 solo trata el caso de dos normas distintas.
*Por qué importa.* Una implementación natural devuelve la mejor coincidencia; la mejor coincidencia es la que dice `CITABLE`. El pack elegiría en silencio, que es lo que `04-source-governance.md` §4 prohíbe para `CONFLICTING`.
*Corrección.* La clave es el par (`identificador_canonico`, `alcance_comprobado`). La búsqueda devuelve **todas** las fichas del identificador y el pack responde por cada una, sin elegir; si dos coinciden con la petición y discrepan, `CONFLICTO_DE_FUENTES`.

**H7 — R3 exige «la fecha del caso» y el corpus tiene cinco fechas distintas.**
*Qué está mal.* `05-temporal-applicability.md` §1 distingue `case_relevant_date`, `procedural_start_date`, `event_date`, `decision_date`, `published_at`. `02`:19 pide «la fecha del caso», en singular y sin tipo.
*Por qué importa.* Es literalmente la prueba de calidad temporal que el propio corpus se impuso: la transición de la Ley 2452 (`temporal-law-matrix.md`:13, «art. 330: transición para procesos iniciados antes de 2026-04-02») **gira sobre la fecha de inicio del proceso, no sobre la del hecho**. Pasar la fecha equivocada convierte `FUERA_DE_LA_VIGENCIA_COMPROBADA` en `CITABLE` en silencio, y `02` §2 no tiene forma de notarlo. Además: si la fecha la produce el modelo, es el modelo produciendo el valor que decide la respuesta —lo que `01` §5 regla 1 prohíbe para las fichas y no prohíbe para la consulta.
*Corrección.* La consulta lleva `fecha_del_caso` **y** `tipo_de_fecha` (con el vocabulario de `05`), tomados de la carpeta del caso y no inferidos; sin tipo, el pack no contesta, igual que sin fecha. Y la frase de `CITABLE` **repite qué fecha usó y de qué tipo**, para que una elección equivocada sea visible para ella.

## 2. ¿Se distingue «existe» de «rige»? — **En la ficha sí. En el contrato, no: el algoritmo vuelve a fundirlas.**

**H8 — La tabla de decisión contradice literalmente la regla 1 del diseño.**
`01` §1 regla 1: «No hay ningún campo, ninguna etiqueta y **ninguna respuesta del pack** que combine las dos en un solo valor.»
`02`:32-34: `si estado_vigencia = VIGENCIA_POR_VERIFICAR o estado_identidad != IDENTIDAD_VERIFICADA ... -> VIGENCIA_POR_VERIFICAR`.
*Qué está mal.* Un fallo de **identidad** se sirve bajo un código que se llama **vigencia**, con una frase (`02`:52) que dice «la identidad puede estar comprobada» y «Última revisión de identidad: Nombre Apellido, `AAAA-MM-DD`».
*Por qué importa.* Es la fusión del §0 en la dirección contraria, y es peor que la original: una `CONFLICTO_DE_FUENTES` —dos fuentes oficiales que discrepan sobre **qué norma es**— se le presenta a la abogada como un problema de vigencia con la identidad aparentemente revisada y firmada. La cita fantasma queda tapada por un aviso sobre otra cosa. `02` §3 no tiene ni un código `IDENTIDAD_POR_VERIFICAR` ni uno `CONFLICTO_DE_FUENTES`.
*Corrección.* Sacar la condición de identidad de la rama de vigencia y darle dos respuestas propias: `IDENTIDAD_POR_VERIFICAR` y `CONFLICTO_DE_FUENTES`, esta última **transcribiendo las dos fuentes** sin elegir. Diez líneas.

**H9 — `VIGENCIA_POR_VERIFICAR` ya significa otra cosa en el corpus, y significa lo contrario.**
*Qué está mal.* `04-source-governance.md`:59 mapea `OUTDATED` → etiqueta visible `VIGENCIA_POR_VERIFICAR` («se conserva como antecedente»). En el pack, `VIGENCIA_POR_VERIFICAR` significa «nadie miró». En `04` significa «sabemos que está vieja». **Mismo token, dos significados opuestos**: ignorancia y hallazgo positivo. Aparece hoy en 8 archivos fuera del pack.
*Por qué importa.* Los campos 1, 3 y 5 están marcados `C` = copiado del catálogo. Una etiqueta copiada que significaba `OUTDATED` aterriza en un campo que el pack lee como «desconocido», y el registro asciende de «sabemos que caducó» a «no sabemos» — exactamente la clase de colapso de dos significados en uno que el instrumento existe para impedir, en su segunda instancia.
*Corrección.* Renombrar dentro del pack: `VIGENCIA_NO_COMPROBADA` (nadie miró) frente a `VIGENCIA_DESACTUALIZADA` (se comprobó y está vieja), y añadir a §1 regla 3 la misma orden de sustitución textual que da para `VERIFIED_OFFICIAL`.

**H10 — La regla 3 del renombrado está mal dimensionada y crea un tercer vocabulario.**
*Qué está mal.* `01`:25 ordena renombrar `VERIFIED_OFFICIAL` / `FUENTE_OFICIAL_VERIFICADA` → `IDENTIDAD_VERIFICADA` **«en `source-catalog/`»** y lo llama «una sustitución de texto». Medido: `VERIFIED_OFFICIAL` aparece 33 veces en **13 archivos**, y `FUENTE_OFICIAL_VERIFICADA` en otros **13**; `source-catalog/` son 4 de ellos. Los demás son `practice-areas/*` (los seis dossiers), `workflows/05, 06, 10`, `evals/legal-research-fixtures.md`, `review-patterns/`, y sobre todo **`04-source-governance.md`, que es donde el término está *definido***.
*Por qué importa.* Renombrar solo en `source-catalog/` deja `04` definiendo `VERIFIED_OFFICIAL`, los workflows usándolo, y el catálogo con un tercer nombre. `ESTADO-DEL-PROYECTO.md` §3 fila 9 ya registra «dos vocabularios de etiquetas conviviendo» como problema abierto; esto añade el tercero.
*Corrección.* El renombrado alcanza a `04-source-governance.md` §4 y §4.1 (la definición) y a los 13 archivos, o no se hace. Y hay que decir el número: 33 ocurrencias, 13 archivos, no «una sustitución de texto».

**H11 — El catálogo del que se copia ya contiene afirmaciones de vigencia bajo una etiqueta de identidad, y el pack no las pone en cuarentena.**
*Qué está mal.* `temporal-law-matrix.md` tiene la columna `effective_from / to` **poblada** («2015-06-30», «2012-07-02», «2022-12-30», «2026-04-02») y `status: VERIFIED_OFFICIAL` en todas las filas. `normative-sources.md` lleva «vigencia 2022-12-30», «vigencia general 2012-07-02», «vigente desde publicación», «vigente y modificada» en la columna «Fecha / estado conocido». Ese es **el error documentado, todavía vivo** (`ESTADO-DEL-PROYECTO.md`:152).
*Por qué importa.* El campo 7 `vigencia_desde` es trabajo de verificadora (P3, 5-10 min) y **la respuesta ya está escrita delante de ella, en una tabla marcada VERIFIED**. La conducta previsible no es investigar: es copiar. `01` §5 regla 3 lo prohíbe, pero los campos vecinos están marcados `C` = «copiado del catálogo (barato)». El instrumento le pide distinguir, en la misma pantalla, qué se copia y qué no, sin ninguna marca que lo distinga.
*Corrección.* Antes de abrir la primera ficha, marcar en `temporal-law-matrix.md` y `normative-sources.md` **cada fecha de vigencia** como `VIGENCIA_NO_COMPROBADA — dato de catálogo, no comprobación`, o borrar la columna `effective_from / to`. Y prohibir explícitamente que `fuente_vigencia` apunte a un archivo del corpus (hoy solo se dice en general).

**H12 — La marca `C` («copiado del catálogo y confirmado, barato») contradice de frente la regla 3 y el antilavado de `04` §7.**
*Qué está mal.* `01`:32 define `C` como copia confirmada y barata; `01`:131 dice «no se copia una afirmación de otro archivo del corpus a una ficha»; `04` §7 dice que copiar al directorio no vuelve nada verificado. Las tres no pueden ser verdad a la vez. Además 2 de las 26 filas del catálogo (`N-CIVIL` = `UNVERIFIED`, `N-L2080` = `POR_VERIFICAR`) no tienen ni identidad comprobada, así que ahí `C` no ahorra nada.
*Corrección.* Definir `C` operativamente: «se copia como **hipótesis de partida** y no se firma hasta verla en la fuente oficial; el ahorro es de tecleo, no de comprobación». Y quitar «(barato)», porque es el supuesto sobre el que se sostiene la estimación de coste.

## 3. ¿Qué pasa si nadie revisa durante un año? — **Se degrada, pero los dos escalones de arriba no funcionan.**

El mecanismo de fondo es correcto y es lo mejor del diseño: el estado se calcula al leer, así que las fichas vencen sin que nadie actúe. Pero:

**H13 — `validity_cutoff_date` se autolimpia y deja el interruptor de 18 meses en código muerto.**
*Qué está mal.* `02`:107 lo define como «el `verificado_el` **más antiguo** entre los registros **que el pack sirve como citables**». Cuando el registro más viejo caduca, deja de servirse como citable, **sale del conjunto**, y `validity_cutoff_date` **salta hacia adelante**. Con cadencia de 12 meses ningún registro citable puede tener un `verificado_el` de más de 12 meses. Luego `validity_cutoff_date` **nunca puede quedar 18 meses atrás**, y la regla de `02`:132 —«el pack deja de servir `CITABLE` por completo»— **no puede dispararse jamás**. Es exactamente el escalón puesto para el escenario «pack sin mantenedor» del §8.2.
*Corrección.* Dos fechas distintas. `validity_cutoff_date` se calcula sobre **todos** los registros del pack, no solo los citables. Y el interruptor cuelga de otra: `ultima_reverificacion = max(verificado_el)` sobre todo el pack; si `hoy − ultima_reverificacion > 18 meses`, el pack se apaga. Esa sí se mueve en la dirección correcta cuando nadie trabaja.

**H14 — `revisar_antes_de` es un campo escribible y nada lo recalcula: una casilla apaga toda la caducidad.**
*Qué está mal.* El campo 12 está marcado `= / V` (calculado **o** de la verificadora), aparece almacenado en el YAML de ejemplo (`01`:78), y su regla —«ella puede acortarla, nunca alargarla»— es una frase, no una comprobación. Toda la degradación por defecto de `02` §2 cuelga de él.
*Por qué importa.* Un solo `revisar_antes_de: 2099-01-01`, por error o por presión de entrega, hace inmortal a esa ficha. Y contradice el principio rector del propio archivo: «el pack no almacena estados».
*Corrección.* `revisar_antes_de` **no se almacena**: se calcula al leer como `min(verificado_el + cadencia, acortamiento_manual)`. Lo único que se guarda es `acortamiento_manual`, opcional, y una fecha posterior a la calculada se ignora en vez de aceptarse.

**H15 — La cobertura no caduca: un pack muerto sigue diciendo «yo cubro esta área».**
*Qué está mal.* `materias_declaradas` se escribe una vez por versión (`02`:81, «coste por registro cero») y es estática. Al año, con todas las fichas caducadas, cada consulta de esa materia recibe `NO_ESTA_EN_EL_PACK`: «El pack **cubre** esta área y **no tiene** `LEY-0000-0000`».
*Por qué importa.* Es la más tranquilizadora de las siete respuestas negativas, servida por un pack sin nada dentro. El §2 promete «si nadie mantiene el pack, el pack se apaga solo»; lo que se apaga es la capacidad de servir, no la de **afirmar cobertura**. El pack sigue con la misma cara, que es lo que el encargo pregunta.
*Corrección.* `materias_declaradas` se **calcula**, no se declara: una materia está cubierta mientras tenga ≥1 ficha no caducada; en cuanto se queda sin ninguna, pasa a excluida y la respuesta es `FUERA_DE_COBERTURA`. Y `recuento` (citables / por verificar / caducados) viaja **en cada respuesta**, no solo en el manifiesto: el estado de salud tiene que verlo quien consume, no quien audita.

**H16 — El pack degradado «solo responde identidad», que es reproducir el fallo del §0 en el peor momento.**
*Qué está mal.* `02`:132: pasados los 18 meses «deja de servir `CITABLE` por completo y **solo responde identidad**». «Responder identidad» no es ninguna de las ocho respuestas, y servir identidad sola es literalmente el error que abre el documento: identidad leída como vigencia.
*Corrección.* Un pack apagado responde `NO_TENEMOS_INFORMACION_SUFICIENTE` y entrega la identidad como dato no citable, con la frase explícita «esto no dice que rija». Nunca en la forma de una respuesta afirmativa.

**H17 — Falta la fila de cadencia de `SIN_VIGENCIA_DESDE`, y `CITABLE` dice «vigente» de una norma derogada.**
*Qué está mal.* La tabla de `02`:118-122 tiene tres filas y ninguna cubre `SIN_VIGENCIA_DESDE`. Y para un caso anterior a la derogatoria, la vía es `CITABLE` —jurídicamente defendible— pero la frase servida (`02`:50) dice «**vigente al** `AAAA-MM-DD`» y no menciona en ninguna parte que la norma esté derogada hoy.
*Corrección.* Añadir la fila (una norma derogada no cambia: cadencia larga o `no aplica`) y una frase propia para ese caso: «`LEY-0000-0000` **rigió** de `AAAA-MM-DD` a `AAAA-MM-DD`; el caso cae dentro. **Hoy no rige.**»

## 4. ¿El silencio se puede leer como «no hay regla»? — **Está bien resuelto salvo en dos puntos.**

La distinción `NO_ESTA_EN_EL_PACK` / `FUERA_DE_COBERTURA` con `materias_excluidas` nombradas una a una es la parte más sólida de los dos archivos, y `02`:61 acierta al señalar que aquí duele más porque el pack no es inspeccionable por ella. Pero:

**H18 — Para decidir entre esas dos respuestas hace falta la materia de una norma que **no tiene ficha**.**
*Qué está mal.* Si el pack no tiene la norma, no tiene su `materia[]`. Alguien tiene que clasificar `LEY-0000-0000` en un área para saber si contesta «cubro esto y no la tengo» o «no cubro esto». Ese alguien, hoy, sería el modelo — y el modelo clasificando una norma que no conoce es el modelo produciendo derecho, por la puerta de la consulta en vez de la de la ficha.
*Corrección.* La materia la aporta **quien consulta** (la skill, desde la carpeta del caso), no se infiere del identificador. Y si la materia no se puede determinar, la respuesta es `NO_TENEMOS_INFORMACION_SUFICIENTE` mostrando **las dos lecturas**, nunca `FUERA_DE_COBERTURA`, que afirma más de lo que se sabe.

**H19 — La cobertura no tiene jurisdicción ni nivel territorial, y el manifiesto de `boundaries.md` sí los exige.**
*Qué está mal.* `boundaries.md`:176-181 hace obligatorias `dimensions {jurisdiction, practice_area, procedure_type, applicable_roles[]}`. El bloque `cobertura` de `02` §5 no tiene ninguna de las cuatro: inventa `materias_declaradas / materias_excluidas / ventana_temporal / granularidad / no_contiene`.
*Por qué importa.* No es formalismo. `06-colombian-law-coverage-ledger.md` tiene un estado propio `REQUIRES_TERRITORIAL_RESEARCH` y una columna `territorial_rules_checked`; `07` §Fuentes marca «Policivo/territorial → norma/acto territorial oficial»; `normative-sources.md` dice de la Ley 1801 que «reformas, reglamentación y **norma territorial** [son] materialmente relevantes». Un pack de alcance nacional que declara cubrir «policivo» responderá `NO_ESTA_EN_EL_PACK` —«cubro esta área»— a una consulta cuya respuesta está en un acuerdo municipal que el pack no puede tener nunca. El silencio se lee como «no hay regla» precisamente en el punto donde el corpus ya sabe que sí la hay.
*Corrección.* `cobertura` incorpora `jurisdiccion` y `nivel_territorial: [nacional]`; toda consulta territorial cae en `FUERA_DE_COBERTURA` con la frase de `06` (`REQUIRES_TERRITORIAL_RESEARCH`). Y `materias_declaradas` se deriva de `06`, no de una lista nueva — con la consecuencia incómoda de que `06` está en `GAP` casi por completo, así que la cobertura honesta del primer pack es casi vacía.

## 5. ¿Es realmente llenable? — **La aritmética es honesta. El modelo de entrega, no.**

Conteo real, contra el catálogo:

| | Cantidad | Casillas |
|---|---|---|
| Filas normativas en `normative-sources.md` | **26** (el pack dice 25) | 26 × 12 = **312** |
| Providencias en `jurisprudence-sources.md` | 4 | 4 × 9 = **36** |
| **Total** | 30 | **348 casillas** |
| De ellas, decisiones de investigación reales (campos 2,4,6,7,8,9 / 3,4,5,6) | | **172** |

Tiempos: 26 × 35 min ≈ 15 h + providencias 3-5 h + P0 2 h ≈ **20-22 h**, dentro de la banda declarada de 17-25 h. La estimación es honesta y las cinco reglas están bien calibradas. Dicho eso:

**H20 — El volumen está subcontado, y lo que falta son exactamente las modificatorias.**
*Qué está mal.* Son 26 filas, no 25. Y las 26 son **semillas**: las normas que el propio catálogo nombra en su columna «Relaciones y dependencia» son otras ~20 (Ley 2080/2021, Ley 2157/2021, Ley 640/2001, Ley 1878/2018, Ley 575/2000, Leyes 50/1990, 789/2002, 2101/2021, D. 1072/2015, D. 1074/2015, D. 2364/2012, D. 1747/2000, D. 333/2014, D. 1429/2020, D.L. 806/2020, D. 42/2026, D. 4463/4796/4798/4799 de 2011…). Medido sobre el catálogo: **~46 identificadores normativos distintos nombrados**, no 25.
*Por qué importa.* Esas ~20 no son opcionales: **son las normas que determinan si las 26 rigen en su redacción original**. O entran al pack —y el coste casi se dobla— o el pack asume V2 conscientemente. Hoy el documento hace lo segundo sin decir el número.
*Corrección.* Corregir el volumen a 26 + 4, y añadir una línea: «el pack no comprueba las ~20 normas modificatorias que el catálogo ya nombra; por eso hace falta `reformada_dentro_del_alcance`, que registra que existen sin obligar a ficharlas».

**H21 — No hay unidad de entrega menor que «el pack», y la regla dura muerde desde el día cero.**
*Qué está mal.* R1 se aplica desde el primer día; el primer día hay cero fichas; el pack completo son 20-22 h que, al ritmo de encargo secundario que el propio documento describe (sesiones de dos horas), son 10-11 sesiones. El documento admite en §7.5 que «va a servir muy poco» pero no da ningún camino para que sirva algo pronto, ni criterio de orden, ni un mínimo publicable.
*Por qué importa.* Ese es el escenario en que la regla dura no se respeta: se salta. Y `02` no tiene defensa contra una regla saltada — sus siete respuestas negativas suponen que R1 se cumple.
*Corrección.* **La unidad de entrega es la ficha, no el pack.** Definir `pack v0.1` = 5-8 registros ≈ 4 h ≈ dos sesiones, con `cobertura` declarando solo lo que hay y `recuento` publicado. El orden lo fija un dato que el proyecto ya tiene y no está usando: qué normas cita de verdad el trabajo real, no cuáles están primero en el catálogo. Y P0 exige al dueño y a la verificadora **juntos**: eso es una dependencia de agenda que no está en el presupuesto de horas.

## 6. ¿Escribió derecho el autor? — **No. Verificado con grep.**

- Patrón de norma con número (`ley|decreto|código|acto legislativo|resolución|sentencia + [0-9]{1,5}`): **0 coincidencias reales**. Todo lo que aparece es `LEY-0000-0000` y `SENTENCIA-X-000-0000`.
- Fechas `(19|20)\d{2}-\d{2}-\d{2}`: **2 coincidencias**, ambas «Fecha: 2026-08-27» en la cabecera de cada archivo. Ninguna fecha de vigencia.
- `art\.?\s*[0-9]+`: **6 coincidencias**, todas `art. 00` / `inciso 0`.
- Ningún año real, ningún número de artículo real, ningún estado de vigencia asignado a nada.

**La regla se cumplió.** Dos observaciones menores, no incumplimientos:
- `01`:132 afirma «los propios portales institucionales advierten que no certifican vigencia por sí solos». Es una afirmación sobre el mundo, no sobre el método. Está respaldada en `normative-sources.md`:9 — pero es, técnicamente, copiar una afirmación del corpus, que es lo que la regla 3 del propio §5 prohíbe. Ponerle la referencia al lado la deja limpia.
- `01`:17 «Ninguno tiene vigencia comprobada hoy» es exacto para la vigencia *hasta* (`effective_to` = «desconocido» o prosa en el 100 % de la matriz, `REFINADO` §1.a) y discutible para la vigencia *desde*, que está poblada. La imprecisión importa porque es lo que justifica que P3 cueste 5-10 min: si las fechas de entrada están escritas, el riesgo de P3 no es el tiempo, es la copia (H11).

## 7. La norma modificada — **V2, arriba. Es el hallazgo principal junto con V1.**

---

# LO QUE HAY QUE ARREGLAR, EN ORDEN

**Bloqueantes — el instrumento no sirve hasta que estén:**
1. V1 — contención de alcance en las dos direcciones (`02`:31).
2. V3 — invertir el algoritmo a lista blanca y exigir `fuente_vigencia` de clase `PRIMARY_OFFICIAL` (`02`:37).
3. V2 — `reformada_dentro_del_alcance` con defecto seguro + `nota_de_vigencia` transcrita en toda respuesta.
4. V4 — leer `estado_uso` y `busqueda_adversa`, o una tabla propia para providencias.
5. H8 — separar la rama de identidad de la de vigencia; dos respuestas nuevas.

**Estructurales — sin esto el pack envejece con buena cara:**
6. H13 — `validity_cutoff_date` sobre todos los registros + interruptor sobre `max(verificado_el)`.
7. H14 — `revisar_antes_de` calculado, nunca almacenado.
8. H15 — cobertura calculada, `recuento` en cada respuesta.
9. V5 — `token_de_respuesta` y la prueba de banco sobre tokens.

**De higiene del corpus, y baratos:**
10. H9, H10, H11, H12 — colisión de `VIGENCIA_POR_VERIFICAR`, alcance real del renombrado (33 ocurrencias / 13 archivos), cuarentena de las fechas del catálogo, definición operativa de `C`.
11. H7, H18, H19 — tipo de fecha del caso, materia aportada por quien consulta, jurisdicción y territorio en la cobertura.
12. H20, H21 — volumen corregido a 26+4 y entrega por fichas, con un `v0.1` de 5-8 registros.

**Una pregunta que los dos archivos no contestan y que condiciona todo lo anterior:** `boundaries.md`:170 dice que «las reglas ejecutables **jamás viajan dentro de un pack**», y `boundaries.md`:45 y :194 dicen que la clase `ADMIN` está vacía y que no hay ningún pack cargado en el slice. La tabla de decisión de `02` §2 **es** una regla ejecutable. Si vive en el pack, las validaciones críticas son datos editables — el corolario que ese mismo párrafo prohíbe. Si vive en el Core, el Core todavía no existe, y hoy el único intérprete posible de esa tabla es el modelo leyendo un YAML. `01` §5 regla 1 le prohíbe al modelo **llenar** casillas y no le prohíbe **evaluar** el contrato. Hay que escribirlo: la tabla es del producto sellado, y hasta que el producto la implemente, **el pack no se consume**. Un modelo que interpreta la tabla también puede interpretarla con generosidad, y esa es la sexta vía.

**Archivos:**
`C:/Users/HITMA/Desktop/legal-workspace/docs/knowledge-pack/01-ficha-y-verificacion.md`
`C:/Users/HITMA/Desktop/legal-workspace/docs/knowledge-pack/02-contrato-de-consumo.md`

No escribí ningún archivo.