# Plan de reducción de coste y de camino a producto

**Fecha:** 2026-08-28. **Estado:** HIPÓTESIS DE TRABAJO. Nada de aquí está decidido ni empezado.

Este documento responde a una petición concreta del dueño: *«sigamos pensando en cómo disminuir esos costes… hazme un plan de posibles o de hipotéticas cosas que nos puedan ayudar a mejorar»*. Y a una segunda, más grande, que menciona de pasada: *«veo una amplia parte como para esto volverle un negocio, licenciarlo, ponérselo al servicio a cualquier tipo de abogado»*.

**Regla que sigo al escribirlo:** cada número viene de una medición de esta sesión o se marca como estimación. Donde no tengo dato, lo digo. Ya me equivoqué una vez prometiendo que el OCR dividiría el coste por siete, así que las cifras de aquí llevan su origen a la vista.

---

## §1 · La medición, primero. Y desmiente lo que yo venía diciendo

Reparto real del gasto de esta sesión:

| Concepto | Tokens | % |
|---|---:|---:|
| **Workflow adversarial de hipótesis** (41 agentes) | **4.317.150** | **89,6 %** |
| Lectura de imágenes en el hilo principal (~45 × 5k) | 225.000 | 4,7 % |
| Escritura de 12 `.md`, 13 `.docx`, 3 ADR y este plan | ~180.000 | 3,7 % |
| Lectura de los `SKILL.md`, dossiers y ADR del repositorio | ~90.000 | 1,9 % |
| OCR, conversiones y comprobaciones (script, sin modelo) | ~5.000 | 0,1 % |
| **Total aproximado de la sesión** | **~4.820.000** | |

> **El 89,6 % se fue en un ejercicio que produjo un solo documento.** Las fotografías, que llevo dos días señalando como el problema de coste, fueron el 4,7 %.

Y dentro de ese 89,6 %, el desperdicio es identificable: **35 de los 41 agentes volvieron a abrir las mismas imágenes**. Cada escéptico reabría entre 5 y 15 páginas para verificar tres citas. A ~5.000 tokens por imagen, eso son del orden de **1,75 millones de tokens gastados en releer lo mismo** — cerca del 40 % del workflow, y aproximadamente el 36 % de toda la sesión.

**Qué compró ese gasto, para ser justos.** Cosas que ninguna otra pasada encontró: que ninguna de las 31 hipótesis preguntaba si hubo acuerdo, cuando los dos poderes facultan expresamente para conciliar; el reparto de sesgo con números (19/15/6); y que 31 enunciados salían de 18 observaciones. Eso no es poco. La pregunta no es si valió: es **si valía 4,3 millones**, y la respuesta casi seguro es que lo mismo se conseguía con una fracción.

---

## §2 · Nivel 1 — Lo que de verdad mueve la aguja

Ordenado por palanca medida, no por lo que suena más avanzado. Los tres primeros no requieren escribir casi nada.

### 1.1 · Arreglar la entrada, no la tubería

**Palanca estimada: la mayor de todas, y cuesta cero.**

Una hoja escaneada plana en PDF con capa de texto se lee por ~200 tokens. La misma hoja fotografiada con celular cuesta ~5.000 y encima hay que transcribirla a ojo. **Es un factor de 25 por página, y además sube la exactitud.**

Lo que hay que producir no es código: es **una instrucción de una página** para quien aporta el material — «escanee plano, o use la app de escaneo del celular en modo documento, no la cámara» —, más una comprobación automática al ingerir que detecte el modo de captura y avise antes de gastar nada.

> **Riesgo real:** quien aporta el material no siempre es la usuaria. Un expediente que llega en fotos de WhatsApp seguirá llegando así. Por eso esto reduce el coste **cuando se puede**, y no sustituye a lo demás.

### 1.2 · Leer una vez, y que todo lo demás lea esa lectura

**Palanca estimada: ~36 % de esta sesión.**

En este pase, cada página se leyó tres veces o más: una pasada de comprensión, otra para fijar la cita literal, y después 35 agentes releyendo. La arquitectura ya prevé la solución y no la usamos: **ADR-011 §7 define la representación derivada con su receta, su hash y su procedencia.**

La forma: una **transcripción de referencia** producida una sola vez, guardada, con su huella. Todo consumidor posterior lee ese texto. **La imagen solo se abre para verificar un dato concreto**, no para volver a leer la página entera.

Y la regla que lo hace seguro, que ya está en ADR-016: *ninguna ausencia en la transcripción de referencia es información sobre el documento.* Si un verificador no encuentra la cita en el texto, **entonces** abre la imagen.

### 1.3 · No abanicar sobre imágenes

**Palanca estimada: ~1,75 M de tokens en este pase.**

Cuando se lanzan agentes en paralelo, cada uno paga su propia lectura. Reglas propuestas:

- El agente recibe **el texto de referencia**, no la carpeta de imágenes.
- La verificación es en dos tiempos: **buscar la cita en el texto** (gratis) y abrir la imagen **solo si no aparece**.
- El abanico se dimensiona por **cobertura**, no por exhaustividad: cinco lentes aportaron; treinta y cinco escépticos, no. Un escéptico por lote de hipótesis habría cazado casi lo mismo.

### 1.4 · Enrutar por dificultad

En el workflow usé el modelo más caro para los 41 agentes, incluida la verificación mecánica de «¿esta cita existe en esta página?». Esa comprobación no necesita razonamiento adversarial.

Propuesta: **modelo barato para lo mecánico** (extraer, cotejar, formatear, verificar presencia de una cadena) y **modelo caro solo para lo adversarial** (encontrar el defecto, juzgar si una hipótesis se sostiene, sintetizar). Es configurable por agente y no requiere obra.

### 1.5 · Lo determinista no lo hace un modelo

Cada una de estas tareas la hace hoy el modelo y **puede hacerla un script**, con resultado idéntico y coste cercano a cero:

| Tarea | Hoy | Podría ser |
|---|---|---|
| Cotejo de cédulas, matrículas, radicados entre OCR y lectura | Modelo | Expresión regular sobre el texto |
| Detectar saltos en la numeración de archivos | Modelo | Script (ya se hizo así) |
| Huellas, tamaños, dimensiones, inventario técnico | Script ✓ | — |
| Detectar duplicados exactos entre piezas | Modelo | Comparación de huellas |
| Construir el PDF ordenado y el paquete de entrega | Script ✓ | — |
| Convertir a Word y comprobar fidelidad | Script ✓ | — |
| Contar hechos por estado, hallazgos por severidad | Modelo | Script sobre la salida estructurada |

**Lo ya marcado ✓ es lo que se movió a `tools/md2docx/` y a la tubería de ingesta.** Lo demás está identificado y sin hacer.

---

## §3 · Nivel 2 — Lo que el dueño propuso, evaluado

### 2.1 · «Scripts propios en Python en vez de contenedores u otros plugins»

**De acuerdo, con una distinción que importa.** Hay dos cosas distintas debajo de esa idea:

**(a) Tubería de ingesta propia** — sí, y es lo más rentable de todo este documento. Un solo `preparar-material.py` que hoy son seis pasos manuales: descomprimir, ordenar, deduplicar, rotar, calcular huellas, correr OCR, construir el PDF consolidado y emitir el registro de ingesta. Se ejecuta una vez por caso, cuesta segundos de CPU y **retira trabajo del modelo de forma permanente**.

**(b) Reemplazar las skills por scripts** — no. Las skills son el método, y el método es lo único que no se puede copiar mirando. Un script no decide si un hecho está apoyado o contradicho. **La regla: al script lo mecánico y verificable; al modelo lo que exige juicio.** Cada vez que algo cruza esa frontera hacia el script, gana precio *y* reproducibilidad.

### 2.2 · «Robots que transcriban de audio a texto»

**Sí, y hay una razón que pesa más que el coste: el audio no puede salir de la máquina.** Una grabación de audiencia lleva voces de terceros identificables. Un servicio de transcripción por minuto es más barato de programar y más caro de justificar.

Tengo una investigación en curso sobre opciones locales para español; los resultados van al §7. Lo que sí puedo fijar ahora son **las reglas que esa herramienta tendrá que cumplir**, porque no son negociables y condicionan cuál sirve:

1. **La transcripción no es el original.** El original es la grabación. Un dato decisivo que solo salga de la transcripción se comprueba contra el audio.
2. **Quién la produjo se declara siempre.** Un programa de transcripción es un productor de material como cualquier tercero, y sus errores tienen forma propia: nombres propios, cifras, apellidos poco frecuentes.
3. **Si no distingue las voces, no se atribuye ninguna frase a nadie.** Sin diarización fiable, la transcripción sirve para saber qué se dijo, no quién lo dijo. Esto elimina de entrada las herramientas que no separan hablantes.
4. **Los minutos resuelven contra la línea de tiempo del original** — ADR-011 §4, sin excepción.
5. **Debe poder decir «aquí no entendí».** Un ASR que rellena silencios con texto inventado es más peligroso que no tener ASR. Es exactamente el mismo modo de fallo que el OCR que perdió la fecha de la audiencia sin avisar.

### 2.3 · «Y de texto a refinar ese texto»

**Aquí hay que frenar, y es la advertencia más importante de este documento.**

Refinar una transcripción **es alterar material probatorio**. Un texto «limpiado» se lee mejor, se cita más cómodo, y semanas después nadie recuerda que la frase original decía otra cosa. Es el mismo mecanismo por el que `redactar-escrito` se declara a sí mismo el comando más peligroso del despacho.

Si se hace, la única forma admisible es:

- **La transcripción cruda es inmutable** y es la que vale.
- El refinado es **otra representación derivada**, marcada como tal, con su receta y su versión.
- **Toda cita resuelve contra la cruda, con su minuto.** Nunca contra la refinada.
- Y el refinado **no corrige contenido**: puntúa, separa párrafos, marca hablantes. No «arregla» lo que alguien dijo mal, porque lo que alguien dijo mal es el dato.

**Formulado así, sí vale la pena.** Formulado como «que la IA mejore la transcripción», es un riesgo que no compensa.

---

## §4 · Nivel 3 — Capacidades nuevas que este pase dejó pedidas

No son de coste: son de valor. Las ordeno por lo que cada una desbloquea.

| # | Capacidad | Por qué, y de dónde sale |
|---|---|---|
| 1 | **Publicar el plugin** | Sigue sin repositorio remoto. **La abogada todavía no puede instalar nada de esto.** Es la entrada 0 del estado del proyecto y no se ha movido en tres fases. Todo lo demás de esta tabla es inútil sin esto |
| 2 | **El séptimo comando** (`revision-de-rigor`) | ADR-015. Fue el método más útil del pase y hoy hay que ejecutarlo leyendo un dossier a mano |
| 3 | **Variante de contexto B** | Los `SKILL.md` dicen «su clienta» y «el escrito que usted presenta». La única usuaria real es autoridad. Se tradujo a mano todo el vocabulario |
| 4 | **Tubería de ingesta** con OCR, cotejo y control de cobertura | ADR-016, con su trabajo pendiente: calibrar la métrica de cobertura, que hoy marca 21 de 23 páginas y por tanto no discrimina |
| 5 | **Bloque «dicho por usted, no documentado en la carpeta»** | Hubo que inventarlo cuando ella dijo que la audiencia se realizó. Ni `estado-del-caso` ni `cronologia` tienen dónde poner lo que la usuaria sabe y la carpeta no registra |
| 6 | **Comando de entrega** | Hoy el paquete de 13 documentos se armó a mano. ADR-014 pregunta 2 sigue abierta: o el Core genera el `.docx`, o el entregable depende de que alguien corra un script |
| 7 | **Segunda pasada comparativa** | Cuando llegue la transcripción hay que rehacer todo sin sobrescribir, marcando qué cambió. No hay mecanismo: se hará a mano |

---

## §5 · La parte incómoda: qué falta para que esto sea un negocio

El entusiasmo es merecido — en dos días se procesó un expediente real y salieron trece documentos que una profesional puede usar. Pero entre esto y «licenciarlo a cualquier abogado» hay cosas que no son de programación, y prefiero nombrarlas ahora que dentro de seis meses.

### 5.1 · Lo que sí es un activo

**El método, no el código.** Los ocho `SKILL.md` son lo único difícil de copiar: la separación entre alegado y acreditado, las cinco polaridades, la compuerta de hechos aprobados, la prohibición de calcular fechas, el vocabulario cerrado de veredictos. Eso es trabajo de oficio destilado, y se nota cuando se usa. El conversor a Word lo reescribe cualquiera en una tarde.

### 5.2 · Los cinco frenos, en orden de dureza

**1. Nadie lo ha instalado nunca.** Ningún comando se ha ejecutado en su forma empaquetada. Todo lo de estos dos días se hizo con el modelo leyendo los `SKILL.md` a mano. **No sabemos si el producto funciona; sabemos que el método funciona.** No es lo mismo y la diferencia es exactamente lo que hay que probar antes de venderle a nadie.

**2. El derecho no está, y es lo que más se espera de un producto jurídico.** El Knowledge Pack no existe. El sistema no dice qué norma aplica, ni si algo procede, ni cuánto es un término — y es correcto que no lo diga, porque no hay cómo verificarlo. Pero **eso es lo primero que va a pedir cualquier abogado que lo pruebe.** Vender esto exige o construir el Knowledge Pack con fuentes verificadas y fechadas, o ser muy explícito en la venta sobre lo que no hace, sabiendo que reduce el mercado.

**3. Los datos de terceros.** Este expediente lleva cédulas, direcciones, datos de salud y nombres de personas que nunca dieron permiso para nada. Hoy ese material **se procesa en servidores de un tercero**. Para uso propio es una decisión del profesional; **para licenciarlo a otros abogados es una decisión con consecuencias regulatorias**, y no es una que yo pueda resolver: hay un régimen de protección de datos personales aplicable que tiene que revisar alguien que responda por ello. **Es el freno número uno para «cualquier abogado», y no es técnico.**

**4. La responsabilidad.** Si un abogado presenta un escrito con una cita que el sistema fabricó, ¿quién responde? Todo el método está construido para que eso no pase —la compuerta, los localizadores, el «por comprobar»—, pero el diseño no es lo mismo que una respuesta contractual. Antes de licenciar hace falta saber qué se promete y qué no, por escrito.

**5. La economía unitaria.** Este caso costó ~4,8 millones de tokens. **Nadie ha dicho todavía cuánto puede costar un caso**, y sin esa cifra ninguna decisión de arquitectura tiene criterio. Es la pregunta que más falta hace y la más fácil de responder: ¿cuánto pagaría un abogado por el paquete de trece documentos que se produjo hoy?

### 5.3 · La prueba que resolvería más dudas por menos dinero

**Un segundo caso, de otra materia y de otra persona.** Todo lo que sabemos sale de un expediente policivo, con una usuaria que además es autoridad. No sabemos si el método aguanta un caso de familia, uno laboral, o un litigante de parte. Un segundo caso diría, por muy poco, si esto es un producto o si es un traje a la medida de un expediente.

---

## §6 · Lo que NO haría, y por qué

Cosas que parecen ahorro y no lo son:

| Idea | Por qué no |
|---|---|
| **Un modelo más barato para todo** | El razonamiento adversarial es donde está el valor. Abaratarlo produce hallazgos plausibles y falsos, que es el peor resultado posible: se leen igual de bien que los buenos |
| **Resumir el material antes de analizarlo** | Un resumen es una lectura, y las lecturas se equivocan. Analizar sobre el resumen propaga el error sin que nada lo delate. Va contra la regla de que el trabajo del sistema no es fuente |
| **Que el OCR reemplace la lectura** | Ya se midió: perdió la fecha de la audiencia sin avisar |
| **Quitar los descargos y las advertencias para acortar** | Son lo único que impide que un documento con aspecto terminado se lea como terminado |
| **Automatizar la segunda pasada sin comparar** | Sin comparación entre pasadas no hay forma de medir si el método mejora, que es lo único que este proyecto tiene como instrumento |
| **Correr el workflow adversarial en cada caso** | Costó el 89,6 %. Es un instrumento de calibración del método, no de producción por caso |

---

## §7 · Transcripción de audio: lo verificado el 2026-08-28

Investigación con fuentes primarias, fecha de consulta 2026-08-28.

### 7.1 · El argumento del ahorro no existe. El de los datos, sí

| Vía | Coste por hora de audio |
|---|---|
| AssemblyAI Universal-2 + diarización | ~$0,17 USD |
| OpenAI `whisper-1` | ~$0,36 USD |
| **Local, en electricidad** | **~$17 COP por audiencia de una hora** |

150 horas de audio al año —unas 100 audiencias— costarían en la nube **unos 25 dólares al año**. **El ahorro no justifica nada.**

Y esto **coincide con lo que `experiments/transcription-spike/README.md` ya había concluido el 2026-08-24**: a esta escala el coste no es criterio de decisión. Es la segunda vez en dos días que persigo un ahorro que no está donde creo.

> **El argumento válido para lo local es uno solo, y se sostiene solo: el audio lleva voces de terceros identificables y no puede salir de la máquina.** No lo debilitemos apoyándolo en un ahorro de veinticinco dólares.

**El coste que ninguna vía elimina:** el tiempo humano de revisar la transcripción. Ahí se decide si esto vale la pena, no en el motor.

### 7.2 · El hallazgo que cambia el diseño: el ASR no omite, inventa

`ADR-016` fija que *la ausencia en el OCR no es información sobre el documento* — el OCR **falla callándose**. El audio falla al revés, y está medido:

**Koenecke et al., «Careless Whisper», FAccT 2024** (arXiv 2402.08021):

- **~1 % de las transcripciones contenían frases enteras alucinadas** que no existen en el audio.
- **38 % de esas alucinaciones incluían daño explícito**, y una de las categorías nombradas es **implicar autoridad falsa**.
- Se concentran en **tramos largos de habla no vocalizada** — silencios. Una audiencia está llena de ellos.

> **En un expediente jurídico, «implicar autoridad falsa» es el peor resultado imaginable de una herramienta.** Y no se detecta leyendo: el texto que inventa un ASR es fluido y verosímil.

**Consecuencia de diseño, que hoy no está en ningún ADR:**

> **Ninguna cita literal puede provenir de un segmento de audio no cotejado contra el original.** Las señales de confianza son un filtro, no una garantía: detectan bien el bucle repetitivo y el silencio, y **detectan mal el invento fluido**.

Es material para un **ADR-017 candidato**, análogo a ADR-016 pero con el signo del fallo invertido.

### 7.3 · La diarización no permite atribuir, y confirma lo ya decidido

Error de diarización de `pyannote/speaker-diarization-community-1` en los datasets parecidos a una sala:

| Dataset | Error |
|---|---|
| AMI (reuniones) | **17,0 %** |
| AliMeeting | **20,3 %** |
| CALLHOME | 26,7 % |

**Del orden de una quinta parte del tiempo de audio queda atribuida al hablante equivocado — y no dice cuál quinta parte.**

> **La diarización local de hoy sirve para navegar («aquí cambia quien habla»), no para afirmar («esto lo dijo el señor X»).**

Esto **confirma** la decisión ya tomada en el Glosario §4 del proyecto: *v0 no modela diarización y no se afirma su fiabilidad*. Y confirma la regla que ya escribimos para la transcripción de esta audiencia: **si no distingue las voces, no se atribuye ninguna frase a nadie.** No la contradigamos por conveniencia.

El token de HuggingFace que exige pyannote es solo para descargar el modelo: **el audio nunca sale de la máquina.** No es un problema de confidencialidad, es un trámite de una vez.

### 7.4 · Las marcas de tiempo sí resuelven contra el original

Los timestamps de las herramientas locales son **desplazamientos en segundos sobre el audio de entrada**, no coordenadas de un artefacto del proveedor. **Eso cumple el invariante de ADR-011 §4** y deja resuelto, para la vía local, el riesgo nº 1 de ese ADR, que estaba `POR VERIFICAR`.

**Con dos condiciones que no esperaba:**

1. **El mapeo de tiempos ha tenido errores reales cuando el filtro de voz está activo** — y ese filtro es justo lo que hay que activar para contener la alucinación. Están corregidos en las versiones actuales, pero es exactamente la deriva de coordenada que ADR-011 nombra, y ahora sabemos que **no era hipotética**.
2. **El alineamiento por palabra falla precisamente en cifras, fechas en números y cuantías** — que es lo que más se cita en un expediente. **Anclar al segmento, nunca a la palabra.** ADR-011 §Riesgos nº 4 ya lo dejaba como límite aceptado; esto lo respalda.

### 7.5 · Por dónde empezar, y qué NO tocar

**Empezar por Faster-Whisper-XXL (Purfview):** ejecutable de Windows, **sin instalar Python ni CUDA a mano**, con filtro de voz y diarización por bandera. Modelo `large-v3` o `turbo`, **filtro de voz activado** y **`condition_on_previous_text` desactivado** — ese segundo parámetro viene activado por defecto y hace que una alucinación se realimente y arrastre los segmentos siguientes.

**Velocidad esperable:** con GPU de consumo, una audiencia de 60 minutos se transcribe en unos 5 minutos. Sin GPU hay que bajar de modelo o aceptar esperas largas; **la cifra de `large` en CPU no está verificada y no hay que suponerla.**

**Dos trampas de licencia, y son reales:**

- Los modelos de diarización **Reverb** que trae esa herramienta están restringidos a **uso personal sin ánimo de lucro**. Trabajo jurídico profesional no lo es. Usar `pyannote`, no Reverb.
- **CrisperWhisper**, que es la herramienta construida específicamente contra la alucinación, tiene **pesos con licencia no comercial**.

**Qué no tocar todavía:** WhisperX. Es la instalación más frágil y lo único que aporta es el alineamiento por palabra, que falla justo en cifras y fechas.

**La prueba que hay que hacer antes de decidir nada:** diez minutos de una audiencia real, **transcritos a mano** como referencia, y medir cuatro cosas — no una: el error de palabra, **cuántos segmentos son texto inventado** (contados aparte de los errores), la deriva de las marcas de tiempo, y si las señales de confianza separan de verdad lo malo de lo bueno. **Si no separan, toda la mitigación se cae, y hay que saberlo antes de construir sobre ella.**

### 7.6 · Lo que quedó sin verificar, y pesa

- **No existe ningún banco de pruebas de reconocimiento de voz para español colombiano.** Todas las cifras de calidad publicadas son habla leída y limpia; una audiencia es lo contrario. **La calidad real es la incógnita principal y solo se resuelve midiendo.**
- La velocidad de `large` en CPU: dos fuentes secundarias se contradicen.
- El error de diarización **con audio en español**: los datos verificados son inglés y mandarín.
- Si las señales de confianza separan de verdad las alucinaciones. **Es la base de toda la mitigación y sigue siendo hipótesis.**

---

## §7-bis · OCR: lo verificado el 2026-08-28, y una corrección mía

Esta investigación **fue a leer el código y los modelos instalados en esta máquina**. No es literatura: es diagnóstico sobre el propio sistema. Y desmiente lo que yo había concluido.

### 7b.1 · Yo dije que no era resolución. Era resolución

El 2026-08-28 escribí, en el registro del pase real: *«La causa no es resolución ni contraste; es el detector con foto de papel curvado y con brillo.»* **Es falso, y ahora se sabe por qué el experimento no lo detectó.**

En el `config.yaml` instalado hay tres filtros en cascada que **borran texto sin dejar rastro ni error**:

| Filtro | Valor por defecto | Qué hace |
|---|---|---|
| `Global.max_side_len` | **2000** | **Reduce la imagen a 2000 px de lado largo antes de todo.** Una foto de 4000 px pierde la mitad de su resolución, siempre, en silencio |
| `Det.box_thresh` | 0,5 | Descarta cajas de detección poco confiadas |
| `Global.text_score` | 0,5 | **Descarta toda línea reconocida con confianza < 0,5, sin avisar ni contarla** |

Y la razón por la que subir `det_limit_side_len` de 736 a 960 y a 1600 no cambió nada: **con `limit_type: min` ese parámetro es un piso, no un techo.** El lado corto ya era mayor, así que no hacía nada. Estuve moviendo una palanca desconectada y concluí que la causa estaba en otro sitio.

> **Lección de método, más valiosa que el hallazgo:** cuando un experimento da resultado nulo en cuatro variantes, la primera hipótesis debe ser **que la palanca no está conectada**, no que la causa está en otra parte.

### 7b.2 · La eñe no estaba rota: no existía

Se leyó el diccionario **embebido dentro del propio archivo del modelo** — 6.623 caracteres, el vocabulario chino. Resultado carácter por carácter:

| Carácter | ¿Está en el modelo que usamos? |
|---|---|
| á é í ó ú ü | Sí |
| **ñ · Ñ** | **NO** |
| Á · Í · Ú | **NO** |
| ¿ · ¡ | **NO** |

**`señora` → `senora` no era un fallo de imagen: el modelo físicamente no tiene el símbolo en su vocabulario de salida.** Ninguna mejora de resolución, contraste o enfoque podía producirlo nunca. Mis tres preprocesados estaban condenados por construcción.

**Arreglado a medias el mismo 2026-08-28.** El modelo latino de 502 caracteres —el único con los cuatro símbolos— solo se distribuye en ModelScope, **que no fue alcanzable desde esta máquina**. Pero en HuggingFace hay un PP-OCRv5 en ONNX cuyo diccionario de 18.383 caracteres **sí tiene `ñ` minúscula y las tildes**. Medido sobre las mismas 23 páginas:

| | v4 (por defecto) | v5 (adoptado) |
|---|---|---|
| Caracteres acentuados en la salida | ~0 | **124** |
| Identificadores críticos | 12 de 12 | **12 de 12 — sin regresión** |
| Regiones detectadas | 711 | 711 — la detección no cambia |

`senora` pasó a `señora`. **Lo que sigue roto: `Ñ` mayúscula, `Ú`, `¿` y `¡`** — y los encabezados de las providencias van en mayúsculas. Para eso hace falta el modelo latino, que queda pendiente de un espejo alcanzable.

Además: el paquete que instalamos está **congelado desde enero de 2025**. El vivo es otro, de julio de 2026, **cuya configuración por defecto ya usa un modelo cuyo diccionario tiene la eñe**. Es posible que solo cambiar de paquete resuelva los diacríticos.

### 7b.3 · La respuesta a la métrica de cobertura, y es gratis

ADR-016 §6 dejó la cobertura como **«no medida»** y su primera tarea de validación era calibrarla. La respuesta es más barata de lo que propuse, y **el dato ya existe dentro del motor**:

> **Contar tres números: cajas detectadas · líneas reconocidas · líneas devueltas tras el filtro de confianza.**
> La diferencia entre la primera y la última es **texto que el motor vio y decidió tirar.** Hoy ese número no se registra en ninguna parte.

Eso convierte el fallo silencioso en fallo declarado, cuesta cero y **dice de qué murió el texto**: si en la detección o en el filtro. Son dos enfermedades distintas con dos curas distintas, y hoy no sabemos cuál tenemos.

**Pero hay un límite que ninguna instrumentación salva, y es la frase que debería entrar en ADR-016 tal cual:**

> **La confianza mide la calidad de lo que se leyó, jamás la completitud de lo que se debió leer.** Una región que el detector nunca propuso no genera caja, ni score, ni entrada: no hay objeto al que asignarle una confianza baja. **No es un problema de umbral: es de tipo.**

**Por eso la única detección fiable de omisión es la redundancia:** dos motores de arquitectura distinta sobre la misma página, y alarma donde diverjan **en presencia** — no en ortografía. La técnica está establecida y el cotejo cuesta milisegundos frente a la inferencia.

### 7b.4 · Tesseract no como reemplazo, sino como el que grita

El hallazgo arquitectónico del informe, y encaja exactamente con la doctrina de ADR-016:

| | Modo de fallo |
|---|---|
| **RapidOCR / PaddleOCR** | Detectar-luego-reconocer: **omite en silencio** |
| **Tesseract** | Analiza la página entera e intenta leerlo todo: **produce basura visible** |

> **Para un uso donde «una ausencia se lee como un hecho», fallar ruidosamente es una propiedad de seguridad, no un defecto.**

De ahí que Tesseract entre como **segunda opinión permanente**, no como sustituto. Y con `tessdata_best`, no con el rápido: el cuello de botella no es la velocidad.

### 7b.5 · El orden de trabajo, y la trampa de licencia

1. **Instrumentar antes de cambiar nada** (medio día). Volver a correr las mismas 23 páginas **sin tocar ningún parámetro**, contando los tres números. Dice, sobre datos que ya tenemos, si el texto murió en la detección o en el filtro. **Toda decisión posterior depende de ese número.**
2. **Arreglar lo verificado** (medio día): modelo y diccionario latinos, subir el techo de 2000 px, y `text_score` a cero para ver lo que hoy se tira. **Los 12 identificadores correctos quedan como prueba de no-regresión: si bajan de 12, se revierte.**
3. **Segunda opinión** (un día): Tesseract con español, e **informe de divergencia por página**. Ese informe *es* la métrica de cobertura.
4. **Corrección de perspectiva**, solo si tras los pasos 1-3 quedan páginas malas. Hay un modelo de 30 MB que corre en menos de un segundo por página en CPU. **Medirlo contra el paso 2, no adoptarlo por fe.**

**Trampa de licencia:** una de las alternativas más prometedoras para español tiene el **código libre pero el modelo bajo una licencia restringida** — gratuita para investigación, uso personal y empresas pequeñas. Para trabajo jurídico remunerado hay que revisarla antes.

**Lo que no haría:** volver a tocar el preprocesado de contraste. Ya se demostró tres veces que no es ahí.

### 7b.6 · Lo que sigue sin saberse

**No existe ninguna cifra pública de calidad de OCR en español sobre fotografías de papel.** Todas las cifras publicadas salen de bancos de prueba de cada proyecto, sobre datos que no son expedientes colombianos fotografiados.

> **Nuestras 23 páginas con 12 identificadores conocidos valen más que todas esas cifras juntas.** Es el único banco de pruebas real que tenemos, y conviene tratarlo como activo del proyecto.

---

## §8 · Orden propuesto

Si hubiera que elegir, este es el orden por rendimiento decreciente. **Es una propuesta, no un plan aprobado**, y las decisiones son del dueño.

| Orden | Qué | Por qué primero | Cuesta |
|---|---|---|---|
| 1 | **Publicar el plugin** | Sin esto, nada de lo demás llega a nadie | Poco |
| 2 | **Preguntar cuánto puede costar un caso** | Sin esa cifra, ninguna decisión de coste tiene criterio | Nada |
| 3 | **Instrucción de captura del material** | Factor 25 por página, cuesta cero | Nada |
| 4 | **Transcripción de referencia leída una vez** | ~36 % del gasto de este pase | Medio |
| 5 | **Tubería de ingesta en Python** | Retira trabajo del modelo de forma permanente | Medio |
| 6 | **El séptimo comando** | La capacidad más usada y la única sin empaquetar | Medio |
| 7 | **Un segundo caso, de otra materia** | Dice si esto es producto o traje a la medida | Bajo |
| 8 | **Medir ASR local con diez minutos reales** | Desbloquea el material que hoy no se puede tocar, y la prueba que decide **cuesta una tarde**, no un proyecto. Ver §7.5 | Bajo |
| 8b | **ADR-017 candidato: el límite del audio** | El ASR falla inventando, no callándose. Ese invariante hoy no está escrito (§7.2) | Bajo |
| 9 | **Knowledge Pack** | Es lo que todo abogado va a pedir, y es el trabajo más grande de la lista | Muy alto |

---

*Documento de hipótesis. Nada de aquí está decidido ni empezado. Las cifras del §1 son medición; las de palanca son estimaciones y llevan la palabra «estimada» donde corresponde.*
