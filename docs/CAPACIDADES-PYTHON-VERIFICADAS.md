# Capacidades en Python — qué se puede añadir gratis, y qué no existe

**Fecha:** 2026-08-31. **Encargo:** *«mira qué más habilidades haciendo uso de Python podemos usar: aclarar imágenes, interpretar letra escrita, traducir de voz a texto con precisión, todo gratis eso sí.»*

**Cómo leer este documento.** Cada afirmación lleva su estado. **Ninguna capacidad se propone sin licencia verificada hoy**, porque en la auditoría anterior aparecieron tres trampas de «gratis pero no comercial» y una de ellas —Surya— vuelve a aparecer aquí.

| Etiqueta | Significa |
|---|---|
| **VERIFICADO** | Comprobado hoy, en esta máquina o en la fuente oficial, y se dice cuál |
| **MEDIDO** | Hay números, sobre el material real del caso, con su método |
| **POR VERIFICAR** | Plausible y no comprobado. **No se construye encima sin comprobarlo** |
| **DESCARTADO** | Se miró y no sirve, con la razón |

---

## 1. Lo primero: ya hay más instalado de lo que se está usando

**VERIFICADO — inventario de esta máquina, 2026-08-31:**

| Pieza | Versión | Estado de uso |
|---|---|---|
| `faster-whisper` | 1.2.1 | **Instalado y sin usar nunca** |
| `ctranslate2` | 4.8.1 | Idem — es el motor de cálculo del anterior |
| Modelos `large-v3`, `medium`, `small` | descargados en caché | **Ya en disco. No hay que bajar nada** |
| `opencv-python` | 5.0.0.93 | Sin usar |
| `rapidocr-onnxruntime` | 1.4.4 | En producción, es el OCR actual |
| `onnxruntime` | 1.29.0 | En producción |
| **Tesseract** | — | **NO instalado.** Comprobado hoy: ni en PATH ni en Archivos de programa |

> **La transcripción de audiencia no está a una compra de distancia: está a un script de distancia.** El motor y los tres modelos ya están en el disco. Lo que no existe es el programa que los llame con los valores correctos — y eso es justo lo que decide si sirve o hace daño.

Y la otra cara: **`segunda_opinion.py` sigue sin poder ejecutarse.** El único control capaz de detectar una omisión silenciosa del OCR necesita un segundo motor, y ese segundo motor nunca se instaló.

---

## 2. Voz a texto — el motor está bien; los valores por defecto son peligrosos

**VERIFICADO hoy, inspeccionando la firma real de `WhisperModel.transcribe` en la versión instalada:**

| Palanca | Valor por defecto | Qué hace | Por qué importa aquí |
|---|---|---|---|
| `vad_filter` | **`False`** | No recorta los silencios antes de transcribir | **Es la principal fuente de alucinación.** ADR-017 cita que las invenciones se concentran en tramos largos sin habla. Una audiencia está llena de ellos |
| `condition_on_previous_text` | **`True`** | Cada tramo se condiciona con el anterior | Un error se propaga hacia adelante y produce bucles. Con `False` cada tramo es independiente |
| `hallucination_silence_threshold` | **`None`** | Desactivado | Existe una palanca específica contra esto **y viene apagada** |
| `temperature` | lista con recaída hasta `1.0` | Si un tramo falla, reintenta con más azar | Más azar es más invención. Fijarla en `0.0` prefiere fallar a inventar |
| `word_timestamps` | `False` | — | **Debe quedarse en `False`:** ADR-017 §5 lo prohíbe como base de cualquier regla |
| `initial_prompt` | `None` | Sesga el vocabulario | Útil para nombres propios del caso, **y arriesgado**: sesgar hacia un nombre hace que aparezca |

> **Los tres valores por defecto que más importan están puestos en el lado peligroso.** No es un defecto de la biblioteca: son los valores razonables para subtitular vídeo. Para una audiencia son exactamente los contrarios a los que hacen falta.

**La tensión que no se resuelve sola, y ADR-017 §3 ya la había señalado:** activar el filtro de voz es lo que contiene la alucinación, **y es justo lo que históricamente ha roto el mapeo de marcas de tiempo contra el original**. Como ADR-017 §2 exige que toda cita literal se coteje escuchando su minuto, **un minuto mal mapeado rompe el único control que hay**. Eso no se decide leyendo: se mide con audio real, y es el primer observable de la spec.

**DESCARTADO — diarización.** `pyannote.audio` es MIT en el código, pero sus modelos están **restringidos** (hay que aceptar condiciones y usar credencial) y su versión de pago se anuncia al lado. Y sobre todo: ADR-017 §4 ya decidió que con un error de atribución del 17–20 % **no se atribuye ninguna frase a nadie**. Un servicio de pago con menos error no cambia la decisión, la encarece.

**Lo que sí se puede hacer sin atribuir, y es útil:** un **mapa de la audiencia** — dónde hay habla y dónde no, en minutos. No dice quién habla. Le dice a ella dónde saltar. `silero-vad` es **MIT VERIFICADO**, pesa unos 2 MB y corre en CPU.

---

## 3. Letra escrita a mano — la respuesta honesta es que gratis no existe

Es la parte del encargo donde más fácil sería complacer. **VERIFICADO, y el resultado es que no:**

| Candidato | Licencia | Por qué no sirve |
|---|---|---|
| `qantev/trocr-base-spanish` | MIT | **Su propia ficha dice que no soporta manuscrito.** Está entrenado con texto impreso sintético de Wikipedia. Es el que cualquiera encontraría buscando «TrOCR español» |
| `microsoft/trocr-*-handwritten` | MIT | Entrenado en **inglés** (corpus IAM). Para español haría falta reentrenarlo con un corpus de escritura española que habría que construir |
| Kraken | Apache-2.0 · **permite cobrar** | Es un **motor**, no un modelo. Sus modelos públicos son de **manuscrito histórico** — procesal, cortesana, colonial |
| PyLaia · Calamari | libres | Igual: motores que hay que entrenar |
| Transkribus | **servicio con créditos de pago** | Tiene los modelos de español que faltan. **Es la trampa**: aparece primero en toda búsqueda y no es gratis |
| Surya | código Apache-2.0 · **pesos NO** | **Segunda trampa, y de la peor clase.** Sus pesos usan una licencia *Open RAIL-M modificada*: gratis solo por debajo de 5 M USD de ingreso o financiación. **Hoy usted está por debajo, luego hoy es gratis** — y esa es exactamente la forma que tiene una licencia de caducar cuando el producto funcione |

### La conclusión que importa, y no es la que se esperaba

> **El mejor lector de letra manuscrita en español que este proyecto tiene ya lo está usando: el modelo multimodal del arnés.** Fue el que leyó las 23 fotografías del expediente. Ninguna alternativa gratuita en Python se le acerca, y las que se acercan cuestan dinero o caducan por ingreso.

**Entonces el trabajo de Python no es reemplazar al lector caro. Es apuntarlo y recortarle el trabajo.** Ahí sí hay una capacidad real, gratuita y honesta:

**Decir dónde el reconocedor no está leyendo, y mandar ahí al lector caro.** El detector encuentra la caja; el reconocedor, entrenado en imprenta, devuelve confianza baja. Se recorta esa zona y se manda al modelo, en vez de mandarle la página entera.

> **CORRECCIÓN — escrita después de medir, el mismo día.** La primera versión de este párrafo decía *«caja detectada + confianza baja = candidato a escritura a mano»*. **La medición del §4 lo desmiente.** La página `…705` es la de peor confianza de la muestra —0,396 de mediana— y **no tiene letra a mano: es texto impreso mal capturado**, con renglones que salen invertidos. La confianza baja marca **lectura mala, sea cual sea la causa**: manuscrito, foto torcida, papel curvado, sello encima o tinta débil.
>
> **Sirve igual para apuntar al lector caro —que era el objetivo—, y no sirve para anunciar «aquí hay letra a mano».** Prometer lo segundo sería inventar una capacidad; es exactamente el error que este documento existe para no cometer.

- **Es seguro por construcción:** el peor error posible es señalar un renglón que sí se leía bien. **Nunca afirma qué dice.**
- **Es el ahorro grande:** en vez de mandar 23 páginas enteras al lector caro, se le mandan los recortes marcados. **POR VERIFICAR** cuánto ahorra — hay que medirlo, no anunciarlo.
- **Y si además se quiere distinguir manuscrito de mala captura**, hace falta otra señal —densidad de trazo, ausencia de líneas base rectas—, que **no está verificada** y hoy no la tenemos.

---

## 4. Aclarar imágenes — MEDIDO, y el resultado no es el que yo esperaba

**Método.** Cinco fotografías reales del expediente, seis variantes de realce, la misma instrumentación de tres niveles que ya usa la ingesta: **cajas detectadas -> líneas devueltas tras el filtro -> caracteres**. Se trabaja sobre copias en memoria; `1-Documentos recibidos/` no se toca.

| Variante | Cajas | Líneas devueltas | Caracteres | Confianza mediana |
|---|---|---|---|---|
| **A** base (la pasada de hoy) | 160 | 85 | 2.783 | 0,710 |
| **B** CLAHE | 160 · **+0,0 %** | 81 · −4,7 % | 3.115 · +11,9 % | 0,568 |
| **C** ampliar x2 | 161 · **+0,6 %** | 88 · +3,5 % | 2.913 · +4,7 % | 0,642 |
| **D** CLAHE + x2 | 159 · **−0,6 %** | 83 · −2,4 % | 3.034 · +9,0 % | 0,552 |
| **E** nitidez *(CLAHE + suavizado que respeta bordes + máscara de enfoque)* | 158 · **−1,2 %** | **95 · +11,8 %** | **4.000 · +43,7 %** | 0,627 |
| **F** enderezar + CLAHE + x2 | 157 · **−1,9 %** | 82 · −3,5 % | 2.946 · +5,9 % | 0,558 |

### 4.1 Lo primero: la palanca desconectada, predicha y confirmada

Antes de correr la prueba quedó escrito que **ampliar al doble no podía servir de nada**, porque la configuración recorta el lado largo a 2560 px antes de mirar la imagen. **Se confirmó:** C mueve las cajas un +0,6 %, y D y F —que también amplían— salen **peor** que B, que no amplía.

> Es la lección de los cuatro experimentos nulos, aplicada a tiempo por primera vez: *cuando el resultado no se mueve, la primera hipótesis es que la palanca no está conectada.* Esta vez se dijo antes de medir, y medir lo confirmó. **Ampliar la imagen se descarta.**

### 4.2 Lo segundo, y es lo importante: el realce NO ayuda a detectar

**Las cajas no se mueven en ninguna variante: entre −1,9 % y +0,6 %.** Y una medición de solapamiento entre la pasada base y la realzada lo confirma región por región:

| | Cajas | Solo las ve una pasada |
|---|---|---|
| Base | 160 | **11 · 6,9 %** |
| Nitidez | 158 | **9 · 5,7 %** |
| **Comunes (solapamiento ≥ 0,5)** | **149** | **93 % coinciden** |

> **El realce mejora el reconocimiento, no la detección.** Lee mejor dentro de las cajas que ya encontraba; **no encuentra las que se le escapaban.** Y por tanto —esto es lo que hay que decir con todas las letras— **no reduce en nada la omisión silenciosa que ADR-016 declara.** Lo que el detector no ve sigue sin verse, y sigue sin que nadie se entere.
>
> **El realce no sustituye a la segunda opinión.** Quien lo presente como si la sustituyera está vendiendo lo contrario de lo que hace.

### 4.3 Lo tercero: sobre lo que sí lee, el realce recupera contenido sustantivo — y pierde otro

Los promedios ocultan lo que pasa. Dos páginas, con el texto real:

**`…673` — la que gana.** Devueltas 10 -> 22, caracteres 736 -> 1.353. La pasada base entrega renglones como `10uDyoagoppoqo`, `LouDyoaDopDBoqpg`, `DD ASNO`. La realzada recupera **un nombre y una dirección de correo de notificaciones judiciales** que la base no veía en absoluto.

**`…705` — la que «pierde».** Devueltas 15 -> 7. Pero al abrir el texto, la realzada es la única que recupera:

> `0,91  ARTICULO SEGUNDO: TRAMITAR la presente querella de conformidad con…`

**Un artículo entero de la parte resolutiva que la pasada actual no lee.** «Perder» en el conteo y ganar en lo que importa.

> **Ni la base ni la realzada domina.** Son **dos lecturas distintas del mismo papel**, y cuál conviene depende de la página. Elegir una para todas es la decisión equivocada disponible en dos formas.

### 4.4 Dos defectos que la prueba destapó sin buscarlos

**El filtro de confianza deja pasar basura.** El umbral vigente es 0,5, y en la muestra pasaron renglones como `0,52 sso d nn i`, `0,64 Cetdcacon`, `0,88 Rla`. **No son lecturas dudosas: no son nada.** Y entran en el texto de referencia como si fueran texto del expediente.

**El reconocedor emite caracteres chinos sobre un documento en español.** El vocabulario de PP-OCRv5 es multilingüe; en la muestra salió al menos un ideograma. **Y eso es un regalo:** un documento jurídico colombiano no contiene nunca un carácter CJK, así que **cualquier renglón que traiga uno es basura con certeza**. Es un filtro de calidad exacto, gratis, de tres líneas.

### 4.5 Qué se propone construir, entonces

**No** «aplicar realce». **Sí** esto:

1. **Dos lecturas de cada página —base y nitidez— y se conserva lo que aporta cada una**, marcando de cuál salió. Es la única forma fiel a lo medido.
2. **Divergencia como señal:** donde las dos lecturas discrepan, se marca la página para mirada humana. Es la mitad barata de la segunda opinión — **la mitad de reconocimiento, no la de detección**, que sigue necesitando Tesseract.
3. **Descartar por vocabulario imposible** (CJK) antes de escribir el texto de referencia.
4. **Revisar el umbral de 0,5**, que hoy admite ruido.
5. **Nada de ampliar la imagen.** Medido: no hace nada.

## 5. Por qué un segundo motor de OCR de la misma familia no es una segunda opinión

Tesseract sigue sin instalar, y su instalador pide elevación de permisos. La tentación es sustituirlo por algo que se instale con `pip` — docTR, EasyOCR, PaddleOCR.

**Y sería un error, por una razón de arquitectura, no de calidad:**

| Familia | Cómo funciona | Cómo falla |
|---|---|---|
| RapidOCR · PaddleOCR · docTR · EasyOCR | **Detectar y luego reconocer**: primero buscan cajas, luego leen dentro | **Callándose.** Lo que el detector no encuentra no existe y nadie se entera |
| Tesseract | **Analiza la página entera** y segmenta renglones sobre ella | **A gritos.** Produce basura visible cuando falla, y la basura se ve |

> **La redundancia solo detecta la omisión si las dos lecturas fallan de forma distinta.** Dos motores que detectan-y-luego-reconocen comparten el punto ciego: se callarían **en el mismo sitio** y su coincidencia se leería como confirmación. **Sería peor que no tener segunda opinión, porque daría confianza falsa.**

Por eso el segundo motor tiene que ser Tesseract —o algo con análisis de página completa—, y por eso instalarlo sigue siendo el pendiente que es. **POR VERIFICAR:** si existe alguna vía de instalación sin elevación de permisos.

---

## 6. Otras capacidades en Python que este proyecto puede usar y no ha mirado

Todas gratis, todas sin modelo nuevo, ordenadas por lo que ahorran o lo que evitan.

| # | Capacidad | Qué resuelve | Estado |
|---|---|---|---|
| **1** | **Recortar y mandar solo lo dudoso al lector caro** | Hoy se mandan páginas enteras. Con las cajas de baja confianza se mandan recortes | **La palanca de coste más grande que queda.** POR VERIFICAR cuánto |
| **2** | **Detectar página faltante por su propio texto** | «Página 1 de 2» y solo llega la 1; «8 mensajes» y se ven 3. En el pase real esto **emergió sin que nadie lo programara** | Sistematizable con expresiones regulares sobre el texto ya extraído |
| **3** | **Cotejar identificadores con su dígito de verificación** | ADR-016 invariante 6 exige que todo identificador lleve su estado de cotejo. **Un NIT colombiano tiene dígito comprobable; una cédula no** | Cierra un invariante que hoy se cumple a mano |
| **4** | **Buscar dentro del expediente sin abrir nada** | Ella tiene 23 fotos y un PDF. «¿Dónde aparece este nombre?» hoy no tiene respuesta rápida | Índice local sobre el texto de referencia. Sin modelo, sin red |
| **5** | **Medir el tiempo de ella, no los tokens** | Huecos `V-2` y `V-3`: **sin horas-persona no hay caso de negocio, solo factura** | Marcas de tiempo en el registro de cada pasada |
| **6** | **Índice de las salidas de una pasada** | `SPEC-08`. Doce archivos y nadie sabe por dónde empezar | Trivial, y ya está especificado |

---

## 7. Licencias verificadas hoy — la tabla que decide

| Pieza | Licencia | ¿Permite cobrar? | Verificado en |
|---|---|---|---|
| `faster-whisper` | **MIT** | Sí | Archivo LICENSE del repositorio |
| Modelos `Systran/faster-whisper-*` | **MIT** | Sí | Ficha del modelo; conversión de `openai/whisper-large-v3` |
| `silero-vad` | **MIT** | Sí — *«sin ataduras: sin telemetría, sin claves, sin registro»* | Repositorio oficial |
| OpenCV | **Apache-2.0** | Sí | Repositorio oficial |
| Kraken | **Apache-2.0** | Sí | Repositorio oficial |
| `qantev/trocr-base-spanish` | **MIT** | Sí — **pero no lee manuscrito** | Ficha del modelo |
| `pyannote.audio` | MIT el código; **modelos restringidos** | **Dudoso** — no lo declara, y vende versión premium | Repositorio oficial |
| **Surya** | Apache-2.0 el código; **pesos Open RAIL-M modificada** | **NO por encima de 5 M USD** | Repositorio oficial |
| **Transkribus** | **servicio de pago por créditos** | No aplica | Sitio oficial |
| Real-ESRGAN | BSD-3 el código; **pesos sin licencia declarada** | **Indeterminado** | Repositorio oficial |

**Las cuatro últimas filas son las que había que encontrar.** Las tres primeras búsquedas que cualquiera haría —Transkribus para manuscrito, Surya para OCR moderno, pyannote para separar voces— **llevan a las tres que no cumplen la condición «todo gratis»**, y dos de ellas lo disimulan bien.

---

## 8. Qué se propone construir, y en qué orden

Según `docs/specs/README.md` estas son **specs de capacidad** —construyen algo que no existe—. Ninguna se escribe sin que su medición la respalde, y **una de las cuatro ya quedó descartada por la medición de hoy.**

| Candidata | Qué la respalda | Qué falta antes de escribirla |
|---|---|---|
| **Doble lectura de cada página, y divergencia como señal** | **MEDIDO hoy.** Las dos pasadas recuperan contenido distinto: un correo de notificaciones en una página, un artículo entero de la parte resolutiva en otra | Nada. **Es la que está lista** |
| **Descarte por vocabulario imposible (CJK) y revisión del umbral 0,5** | **MEDIDO hoy.** Pasaron `sso d nn i` con 0,52 y salió un ideograma chino | Nada. Es de tres líneas |
| **Recortar lo dudoso y mandarlo al lector caro** | La confianza baja localiza bien lo mal leído | Medir **cuánto ahorra de verdad**. Sin esa cifra es una promesa |
| **Transcripción de audiencia con valores endurecidos** | Motor y modelos ya instalados; los tres valores por defecto que importan están en el lado peligroso | **Diez minutos de audio real.** No se escribe sin medir si el filtro de voz rompe los minutos, que es lo único que sostiene la regla de cotejo de ADR-017 §2 |
| ~~Ampliar la imagen antes del OCR~~ | — | **DESCARTADA por la medición.** La configuración recorta a 2560 px: la palanca no está conectada |
| ~~«Aquí hay letra a mano»~~ | — | **DESCARTADA.** La confianza baja marca lectura mala, no manuscrito. Ver la corrección del §3 |

### La advertencia de método que vale para todas

ADR-016 invariante 10: **cambiar de reconocedor produce versión nueva y nunca sobrescribe.** Cambiar el realce previo cambia la receta igual que cambiar el motor. **Ninguna de estas capacidades puede pisar una extracción anterior ni «mejorarla» en su sitio**, y las dos lecturas tienen que decir de cuál salió cada renglón.

### Y lo que sigue sin resolverse, que es más grande que todo lo anterior

El realce **no toca la omisión silenciosa**: 93 % de las zonas detectadas coinciden entre las dos pasadas. **Instalar Tesseract sigue siendo el único camino conocido hacia la mitad que falta de la segunda opinión**, y sigue bloqueado por un instalador que pide elevación de permisos. Ninguna de las capacidades de este documento lo sustituye, y ninguna debe presentarse como si lo hiciera.
