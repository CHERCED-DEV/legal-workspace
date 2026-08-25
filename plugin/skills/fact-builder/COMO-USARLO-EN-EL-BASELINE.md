# Cómo usar `fact-builder` en el baseline

**Estado:** documento operativo de la fase Discovery. **No es normativo.** Nada de lo escrito aquí redefine un ADR Accepted, el Technical Design ni el glosario.

**Audiencia: quien conduce y quien adjudica el baseline.** No se le entrega a la profesional. Lo único que ella ve es el protocolo de sesión (`docs/discovery/baseline-protocolo.md`) y, si se usa la vía del pegado, **el texto del método** — que por eso tiene que estar escrito en su lengua, sin una palabra de jerga y sin un solo dato del caso dentro.

**Qué es este documento.** El método `fact-builder` está escrito y en esta misma carpeta (`SKILL.md`). Aquí se dice **cómo ponerlo a trabajar en el baseline de esta semana**, cómo montar la comparación para que signifique algo, qué mirar y —lo más importante— cómo leer el resultado sin estirarlo en ninguna de las dos direcciones.

**Qué NO es.** No es una ampliación del protocolo. El protocolo se ejecuta **entero y sin tocar** en su forma original; lo de aquí es un **segundo brazo de medición** que se le añade, nunca un reemplazo.

**Qué se afirma aquí sobre el producto de terceros: casi nada.** Lo que la aplicación haga es exactamente lo que se registre, con la etiqueta `observed in current environment` y jamás `documented platform guarantee`.

**Etiquetas en uso:** HECHO VERIFICADO / PROPUESTA / HIPÓTESIS / SUPUESTO / POR VERIFICAR / RIESGO / DECISIÓN PENDIENTE / NO TENEMOS INFORMACIÓN SUFICIENTE.

---

## 0. En una página

Hasta ahora el baseline medía **una** cosa: qué hace la herramienta tal como viene. Con el método escrito puede medir **tres**, y las tres responden preguntas distintas:

| Brazo | Qué se mide | Pregunta que responde | ¿Esta semana? |
|---|---|---|---|
| **B1 — sola** | La aplicación tal cual, sin nada puesto | ¿Existen de verdad los cuatro fallos con material real? ¿Dónde está la vara? | **Sí. Es el baseline y manda.** |
| **B2 — con método** | Lo mismo, con el texto del método delante | ¿Cuánto del hueco cierra **el método solo**, sin nada que lo obligue? | Sí, después de B1 |
| **B3 — con método y con Core** | Lo mismo, con el Core validando | ¿Cuánto del hueco solo se cierra **obligando**? | **No.** No hay Core. Se corre cuando exista |

**La regla que gobierna todo:** **B1 no se toca, no se adelanta, no se contamina.** Si hay que sacrificar algo por falta de tiempo, se sacrifica B2. Un B1 limpio sin B2 sigue siendo un ejercicio válido; un B2 sin B1 limpio no mide nada, porque no hay contra qué comparar.

**Y la advertencia que hay que tener escrita antes de mirar los resultados:** el método **no impide** que la herramienta invente. Es texto que se puede ignorar. Si en B2 siguen apareciendo citas inventadas, eso **no es un fallo del método** — es la medida exacta de por qué hace falta el Core, y es el dato más valioso que este ejercicio puede producir (§5).

---

## 1. Qué cambia y qué NO cambia del protocolo

| | |
|---|---|
| **No cambia** | Las peticiones, su orden, los tres días, el corte entre sesiones, las seis marcas (**I P O R B F**), la hoja previa cerrada, la prohibición de guiar, la prohibición de repetir una petición, el cierre de cinco preguntas, la hoja de registro |
| **No cambia** | Que el material se entregue tal cual, sin limpiar. Que se trabaje sobre copias. Que se conecte una sola carpeta |
| **Cambia una sola cosa** | En B2, y solo en B2, **el método está delante de la herramienta desde el primer mensaje** |
| **Deja de aplicarse en B2** | La regla del protocolo §1.3 *"no escribirle instrucciones previas de método"*. Esa regla define B1 y por eso B1 se corre primero y sin discusión. En B2 se rompe **a propósito, una sola vez, y esa es toda la diferencia entre los dos brazos** |

**Si se cambia algo más entre B1 y B2, la comparación queda inservible** y no hay forma de arreglarla después. La lista de lo que hay que mantener idéntico está en §3.7.

---

## 2. Cómo se pone el método delante de la herramienta

### 2.1 Vía A — pegarlo al inicio de la conversación · **la que seguro funciona**

**Cómo.** Se abre la conversación de la sesión, se conecta la carpeta del caso, y **antes de cualquier otra cosa** se pega el texto completo del archivo del método como primer mensaje. Se espera a que responda. Y **solo entonces** empieza la petición 1 del protocolo.

**Por qué se puede afirmar que funciona.** Pegar un texto en una conversación es escribir un mensaje. No requiere ninguna capacidad del producto, ninguna instalación y ninguna configuración: por eso es la vía que no depende de nada que no esté verificado.

**Lo que esta vía sí exige, y no es negociable:**

- **El texto pegado no puede contener ni un dato del caso.** Ni un nombre, ni una fecha, ni un número. Si lo contiene, la sesión 2 queda destruida: pegarlo sería recordarle el caso, que es exactamente lo que la sesión 2 mide.
- **Hay que volver a pegarlo, idéntico, al empezar la conversación nueva de la sesión 2.** Una conversación nueva no lo lleva dentro. Si no se repega, la sesión 2 de B2 mide *"sin método"* y la diferencia se atribuiría mal. Y como no contiene nada del caso, repegarlo **no** ayuda a la herramienta a recordar: no viola la regla de no recordarle nada.
- **La sesión 3 continúa la conversación de la sesión 2** (así lo manda el protocolo), de modo que ahí no se pega nada nuevo.
- **Se pega el mismo texto, sin editarlo, las dos veces.** Si alguien lo mejora entre sesiones, hay dos métodos y ningún resultado.

**Lo que esta vía no da.** Ninguna garantía de que la herramienta siga el método. Puede leerlo y no aplicarlo; puede aplicarlo al principio y soltarlo a mitad de la conversación; puede aplicar la forma sin la sustancia (§4.6). Eso no es un defecto del montaje: **es el fenómeno que se está midiendo.**

### 2.2 Vía B — instalarlo en la aplicación · **POR VERIFICAR**

**HECHO VERIFICADO** (documentación oficial recogida en el spike de Cowork): la aplicación **admite skills y plugins**, un plugin empaqueta *"skills, connectors, and sub-agents"* en una sola instalación, y los componentes de un plugin instalado se pueden activar y desactivar por separado.

**POR VERIFICAR**, y hay que verificarlo mirando la aplicación instalada, no razonando por analogía:

- Los pasos concretos de la interfaz para añadir un método suelto sin empaquetar un plugin.
- Si, una vez instalado, se activa solo al empezar a trabajar o hay que nombrarlo.
- Si sobrevive al cambio de conversación entre la sesión 1 y la sesión 2 — que es justo lo que haría atractiva esta vía.

**Ventaja si resulta viable:** el texto es idéntico en las tres sesiones sin depender de que alguien lo pegue bien, y no hay riesgo de contaminar la carpeta del caso.

**Riesgo propio de esta vía, y es serio:** si se instala y **no se activa**, B2 mide *"sin método"* sin que nadie se entere, y el resultado se leerá como *"el método no sirvió"*. Es la peor forma posible de equivocarse, porque produce una conclusión falsa con aspecto de dato. Por eso el ensayo en seco de §2.4 es obligatorio para esta vía.

**Regla de decisión, escrita antes del día 1:** si el ensayo en seco no confirma que el método está actuando, **se usa la vía A y punto**. No se improvisa la interfaz el día de la sesión: la fricción de instalar algo en caliente se registraría como fricción de la herramienta y sería un dato falso.

### 2.3 Vía descartada — meter el archivo del método en la carpeta del caso

**No se hace.** Dos razones, y la primera basta:

1. **Contamina la petición 1.** La petición 1 pregunta qué documentos recibió. Un documento nuestro dentro de la carpeta altera esa respuesta, altera el conteo de documentos y mete ruido en M1 que después nadie sabrá separar.
2. **HECHO VERIFICADO:** adjuntar una carpeta concede lectura **y escritura** sobre todo su contenido. Cuantas menos cosas nuestras haya ahí dentro, mejor.

Si alguna vez se quisiera probar por esa vía, sería con una carpeta aparte — pero el protocolo manda **una sola carpeta conectada**, así que en este baseline no cabe.

### 2.4 Ensayo en seco — obligatorio, en otro día, con material falso

Antes del día 1 de B2, en una **conversación de usar y tirar**, con **dos o tres documentos inventados** (nunca el caso real, nunca el caso de B1):

1. Se carga el método por la vía elegida.
2. Se hace la petición 3 del protocolo (*"para cada hecho, con qué prueba lo respaldo…"*).
3. Se mira **una sola cosa**: si la salida tiene la forma del método —hecho por hecho, con su respaldo al lado, con lo que no tiene respaldo dicho en voz alta— o si tiene la forma de siempre.
4. Se anota qué se vio, con fecha, y **la versión de la aplicación si es visible**.

Si no se puede distinguir, se asume que **no está actuando** y se usa la vía A. Ante la duda, la vía que no depende de nada.

Este ensayo **quema** los documentos falsos que use, así que no se usan los del banco sintético que se quiera preservar.

### 2.5 Qué hay que dejar anotado sobre la carga

Sin esto, un resultado negativo de B2 es ininterpretable, porque *"el método nunca llegó a actuar"* queda como explicación rival que ya no se puede descartar:

- Vía usada: pegado / instalado / otra.
- Si fue pegado: **si se repegó al empezar la sesión 2**, y a qué hora.
- Qué se vio en el ensayo en seco.
- Fecha y, si es visible, versión de la aplicación **en cada brazo**. Si la aplicación se actualizó entre B1 y B2, la comparación está confundida y hay que declararlo, no disimularlo.

---

## 3. El diseño de la comparación

### 3.1 Primero sin método, después con método — y por qué el orden no es discutible

Cinco razones, en orden de peso:

1. **B1 es la vara.** Es la referencia contra la que se compara todo lo que construyamos después. Si se contamina, no hay forma de recuperarla con esta persona y este caso.
2. **B1 responde la pregunta fundacional** —¿existen los cuatro fallos?— y esa pregunta no puede ponerse en riesgo por un cambio que introducimos nosotros.
3. **B2 solo es interpretable contra una referencia que ya exista.** Al revés no funciona: *"con método pasó esto"* no significa nada sin el *"sin método pasaba esto otro"*.
4. **El orden inverso arruina a la persona, no solo al dato.** Si ella ve primero una salida ordenada, hecho por hecho, con sus respaldos, ya no puede leer con ojos limpios una salida sin esa forma: la juzgará por comparación y no por su utilidad.
5. **La hoja previa cerrada** (los 5–10 hechos escritos antes de abrir la herramienta) solo vale una vez, y vale para el primer brazo que se corra.

### 3.2 Por qué no se puede usar el mismo caso dos veces con la misma persona

Porque la segunda vez **ella ya sabe las respuestas**, y una parte grande del instrumento depende de que no las sepa:

- Ya sabe qué hechos hay, dónde está la contradicción y dónde estaba la trampa. Su detección deja de medir la fiabilidad de la salida y pasa a medir su memoria.
- **El Bloque D entero se cae.** Marcar *"la doy por buena"* sobre una afirmación cuyo error ya vio la semana pasada no mide nada. Y el Bloque D es, según la propia rúbrica, el bloque más importante: es el único que mide el error que **sobrevive** a la revisión humana.
- **La petición 10** —preguntar por un asunto que nunca se trató— es una trampa de un solo uso. La segunda vez la está esperando.
- **La sesión 3** depende de que el documento nuevo sea una sorpresa. Solo hay una sorpresa por caso.
- **El coste de verificación** se desploma en la segunda vuelta porque ella ya sabe dónde mirar. Comparar minutos entre brazos sería comparar su familiaridad, no las dos condiciones.

**Pero no todo se quema.** Conviene separarlo con precisión, porque de esa separación sale la opción barata del §3.4:

| Sigue midiendo aunque se repita el caso | Se quema al repetir |
|---|---|
| Entidades inventadas — se comprueba buscando el nombre o la cifra en el material, mecánicamente | Todo el Bloque D: `LA DOY POR BUENA`, la muestra ciega, la detectabilidad D1/D2/D3 |
| Fuente correcta / referencia utilizable / **el pasaje dice eso** — se comprueba abriendo el documento | Los minutos de verificación (`b_coste_verificacion`) |
| Hechos sin anclaje — se juzga **leyendo la salida**, sin abrir nada | La continuidad de la sesión 2 y la trampa de la petición 10 |
| Omisiones contra la **hoja previa ya escrita y congelada** (no se reescribe: se reutiliza la misma) | La obsolescencia de la sesión 3 (el documento nuevo ya no sorprende) |
| Contradicciones inventadas — se comprueban contra el material | Su respuesta al cierre de cinco preguntas (queda anclada por la primera vuelta) |
| Si la salida separa por sí sola lo probado de lo afirmado — es una propiedad de la forma de la salida | La gravedad que ella firma, en parte: ya sabe qué consecuencias tuvo cada error |

**RIESGO transversal a las tres opciones que siguen:** en la segunda vuelta ella puede, sin querer, **conducir hacia lo que ya sabe** —preguntar por la contradicción que conoce, insistir donde recuerda que falló—. Mitigación ejecutable: en B2 se usan **sus propias palabras de B1, transcritas literalmente**, y toda desviación se anota (§3.7).

### 3.3 Las tres salidas honestas

Ninguna es limpia. Se elige una **antes de correr**, se escribe cuál se eligió y se declara su limitación en el informe.

**Opción A — Dos casos comparables.** B1 con el caso 1, B2 con el caso 2.

| | |
|---|---|
| **A favor** | Es la única que conserva **todas** las medidas en los dos brazos, incluido el Bloque D. Es la que más información produce |
| **En contra** | Cualquier diferencia entre brazos puede ser **la dificultad del caso** y no el método. Con dos casos y una persona **eso no se puede separar**, punto. Solo se separaría cruzando el orden en una segunda ronda (caso 1 con método, caso 2 sin), y para eso hacen falta cuatro corridas y dos semanas |
| **Cuesta** | Doble: dos hojas previas, dos preparaciones de material, seis sesiones |
| **Condiciones** | Criterios de comparabilidad escritos **antes** de mirar los candidatos (misma materia, rango parecido de número de documentos, ambos terminados, ambos con al menos una contradicción o tensión probatoria conocida). Cuál de los dos va a B1 se decide **por sorteo** entre los que cumplen, no por preferencia de nadie |

**Opción B — Dos partes del mismo caso.** Se parte el expediente en dos bloques autónomos (dos episodios, dos periodos) y cada bloque va a un brazo.

| | |
|---|---|
| **A favor** | Mismo caso, misma calidad de material, misma persona. Barato: una sola preparación |
| **En contra — y esto suele ser decisivo** | **Partir un expediente destruye lo que más queremos medir**: las contradicciones que cruzan de un bloque al otro dejan de existir. Se estaría midiendo sobre material más fácil que el real, en los dos brazos |
| **En contra** | Los dos bloques casi nunca son igual de difíciles, y no hay forma de demostrar que lo sean. El segundo bloque se trabaja con la familiaridad que dejó el primero. Las sesiones 2 y 3 solo caben limpias en uno de los dos brazos |
| **Cuándo tiene sentido** | Cuando el caso tiene de verdad dos episodios independientes y no hay un segundo caso disponible |

**Opción C — El mismo caso dos veces, con las medidas restringidas.** B2 repite el caso de B1 y **solo se reportan las medidas de la columna izquierda de §3.2**. El Bloque D, la continuidad, la obsolescencia y los minutos **no se reportan para B2**: se escriben como `NO ESTIMABLE EN B2` y se dice por qué.

| | |
|---|---|
| **A favor** | El material es idéntico, así que la dificultad **deja de ser una explicación rival**. Es la única opción en la que la diferencia observada apunta al método con algo de fuerza |
| **A favor** | Es la más barata: no hace falta un segundo caso ni una segunda hoja previa |
| **En contra** | Pierde el Bloque D en B2, que es el bloque más importante. Sabremos si el método mejora la **forma** de la salida; **no** sabremos si mejora lo que sobrevive a la revisión humana |
| **En contra** | Ella se aburre y trabaja distinto la segunda vez. Se anota como fricción |

**Recomendación, con su motivo:** **Opción C** si hay que correr esta semana y solo hay un caso preparado — porque neutraliza la dificultad del material, que es el factor de confusión más grande, y porque su pérdida (el Bloque D en B2) es una pérdida **declarable**, no un sesgo escondido. **Opción A** si existe un segundo caso que cumpla los criterios y hay dos semanas — porque conserva el Bloque D, que es lo que decide el alcance del producto. **Opción B solo si no hay ninguna de las dos**, y con la advertencia de que mide sobre material amputado.

**Lo que no vale en ninguna de las tres:** decir *"el método mejoró la atribución"* en porcentaje. Una persona, un caso, una semana: **conteos con denominador, jamás tasas** — *"3 de 24"*, nunca *"12,5 %"*.

### 3.4 Dos pasadas: hay que elegir qué se mide, y decidirlo antes

La rúbrica ya exige **dos pasadas del mismo arranque** para ver si el perfil de fallos es estable entre corridas idénticas (la herramienta no es determinista). Ahora hay una segunda pasada que se quiere gastar en poner el método. **Son dos preguntas distintas y una sola pasada no responde las dos:**

| Con dos pasadas se puede medir | No se puede medir a la vez |
|---|---|
| Estabilidad del perfil (dos pasadas idénticas) | El efecto del método |
| El efecto del método (una sin, una con) | Si la diferencia observada cabe dentro del ruido de la propia herramienta |

**Y ahí está el problema serio:** si solo hay dos pasadas y se gastan en *sin/con*, **no sabemos cuánto varía la herramienta consigo misma**, así que no podemos afirmar que una diferencia pequeña se deba al método. Podría ser ruido.

- **Mínimo honesto: tres pasadas** — dos sin método (para ver el ruido) y una con método. Solo así una diferencia significa algo.
- **Si solo caben dos:** se elige cuál de las dos preguntas vale más, **se escribe la elección con fecha antes de correr**, y en el informe se dice que la otra quedó sin medir. Si se eligió *sin/con*, entonces **cualquier diferencia pequeña se reporta como no concluyente**, no como efecto del método.

### 3.5 Lo que hay que mantener idéntico entre B1 y B2

Cada punto de esta lista que se rompa es una explicación rival que ya no se podrá descartar:

- **Las peticiones, palabra por palabra.** El protocolo pide que ella las formule con sus palabras; eso vale para B1. En **B2 se reutilizan sus palabras de B1, transcritas literalmente** del registro. Así los dos brazos usan las mismas palabras **y** siguen siendo las suyas. Si el caso es otro (Opción A), se cambian solo los nombres propios y se anota el cambio.
- **El orden y el número de peticiones.** Nada de añadir una petición porque la salida con método invita a preguntar más.
- **La separación entre días.** Si B1 tuvo un corte de dos días y B2 de uno, la sesión 2 no es comparable.
- **El material entregado, y cuándo se entrega cada cosa.**
- **Quién conduce y quién anota.**
- **Que el conductor no comente la salida en caliente**, en ninguno de los dos brazos.
- **La versión de la aplicación**, en la medida en que se pueda saber. Si cambió, se declara.

---

## 4. Qué observar cuando el método está puesto

Todo lo que sigue se mira **además** de lo que el protocolo ya manda mirar, y se anota con las mismas seis marcas. La comparación es siempre **contra la salida de B1, numerada y guardada**, no contra la impresión de nadie.

### 4.1 ¿Aparecen hechos que antes no aparecían?

- Contra la **hoja previa congelada** (la misma de B1, sin reescribir): cuántos de sus hechos nucleares aparecen ahora y no aparecían antes.
- Contra la salida de B1: hechos nuevos que **no** están en la hoja previa. Pueden ser aportes reales — marca **B** — o ruido. Lo decide ella, y se anota el motivo del descarte, no solo el descarte.
- **Cuidado con la lectura fácil:** **más hechos no es mejor.** Si el método produce **menos** hechos pero cada uno llega con su respaldo y sin inventar, es mejor herramienta aunque el conteo baje. Se compara conducta, no notas.

### 4.2 ¿Baja la cantidad de hechos sin respaldo presentados como ciertos?

Es la medida más limpia del baseline, porque se juzga **leyendo la salida**, sin abrir el material.

- Conteo con denominador en los dos brazos: hechos enunciados sin ninguna referencia de origen **y** sin marca explícita de *"esto es solo lo que dice la parte"*, sobre el total de hechos enunciados.
- **La observación que más dice:** en B1, la separación entre probado y afirmado solo aparecía cuando se preguntaba por ella (petición 4). En B2, **¿aparece sola, ya en la lista de hechos, sin que nadie la pida?** Ese salto —de *responde cuando se le pregunta* a *distingue por defecto*— es exactamente la propiedad que el producto tiene que exhibir.
- Y el matiz que no hay que redondear: **¿aparece el respaldo parcial?** *"El documento confirma el pago pero no la fecha que se afirma."* Si eso empieza a salir, es una señal fuerte. Si todo sigue siendo respaldado/no respaldado en blanco y negro, el método no está calando en lo que más importa.

### 4.3 ¿Señala contradicciones y vacíos por su cuenta?

- **Antes** de la petición 5, no después. Lo que se mide es la iniciativa: si en la lista de hechos ya avisa de que dos documentos no cuadran, o de que falta una prueba.
- ¿Encuentra la contradicción que ella ya sabía que estaba?
- **Y el conteo espejo, que hay que anotar aunque incomode:** **contradicciones inventadas.** Un método que empuja a buscar contradicciones puede fabricarlas. Está escrito aquí, antes de correr, precisamente para que si ocurre nadie pueda explicarlo después como un detalle.
- ¿Distingue **no encontrado** de **no existe**? Decir *"no hay contradicciones"* cuando lo cierto es *"no las encontré"* es un fallo, y con el método puesto debería empezar a decirse bien.

### 4.4 ¿Mejora el emparejamiento entre hecho y prueba?

Se descompone en tres preguntas encadenadas, y hay que responderlas por separado:

1. **¿La referencia permite llegar al pasaje sin adivinar?** ("la cláusula 4 del contrato, página 3" sí; "según el contrato" no).
2. De las que sí: **¿el pasaje dice lo que se le atribuye?** Este es el fallo fantasma —referencia real, contenido inexistente— y es el que ella sabe juzgar mejor que nadie.
3. De las que sí: **¿presenta bien si la prueba apoya, contradice o solo sitúa el hecho?** (son las tres palabras que el método le pide usar).

Y dos preguntas de forma que el método debería mover:

- **¿Maneja que un hecho tenga varias pruebas y que una prueba sirva a varios hechos?** ¿O sigue forzando un par por hecho?
- **¿Dice en voz alta los hechos que se quedaron sin ninguna prueba?** Un hecho sin soporte es información valiosa; ocultarlo es el fallo. Si el método consigue que eso salga sin preguntarlo, es un resultado concreto y se anota.

### 4.5 Lo que el método puede empeorar — y hay que mirarlo con la misma atención

Un método no es gratis. Se registra en la hoja, en fricción y con marca **F**:

- **Salida más larga.** Más que revisar, más minutos de ella. Si el coste de revisión sube más de lo que baja el coste de corregir, el método no ayuda aunque las cifras de calidad mejoren.
- **Formato rígido que no es su forma de trabajar.** Si tiene que pelearse con la estructura o rehacerla para su borrador, es fricción real y cuenta en contra.
- **Hechos útiles perdidos.** La instrucción de no convertir narración en hecho puede tirar algo que ella sí quería. Si ocurre, se anota como omisión, no como acierto de disciplina.
- **Verbosidad metodológica.** Que explique lo que va a hacer en vez de hacerlo.

### 4.6 El modo de fallo más peligroso: **la forma sin la sustancia**

Es el que hay que dejar escrito antes de correr, porque es el más fácil de leer al revés.

La herramienta puede **imitar la apariencia** del método —cada hecho con su respaldo al lado, sus etiquetas, sus avisos de lo que falta— y que **los respaldos estén mal**. El resultado sería una salida **más ordenada, más segura de sí misma y más difícil de desconfiar**: es decir, **más peligrosa** que la de B1, porque una referencia con buen aspecto pasa la revisión que una afirmación suelta no pasa.

**Cómo se comprueba:** es la única razón por la que valdría la pena gastar una muestra ciega también en B2, si el diseño elegido lo permite (Opción A sí; Opción C no). Si no se puede, **se verifica al 100 % un puñado de respaldos de B2 escogidos por sorteo** y se reporta la fracción con los dos números a la vista, sin extrapolar al total.

**Cómo se reporta si ocurre:** *"el método mejoró la forma y no la fiabilidad"*. Sería un hallazgo de primer orden y, otra vez, un argumento a favor del Core, no en contra del método.

---

## 5. La advertencia central — y cómo leer el resultado sin estirarlo

### 5.1 El método no impide inventar. No puede.

Un método es **texto** que se le pone delante a la herramienta. Puede leerlo y no aplicarlo, aplicarlo a medias, o soltarlo a mitad de la conversación. **No hay ninguna garantía técnica de que se cumpla**: nada verifica la salida, nada la rechaza, nada deja rastro. La única comprobación que existe en B2 se llama *la profesional*.

Esto es un principio de arquitectura del proyecto, no una excusa escrita a posteriori: **si el sistema deja de ser seguro porque la herramienta ignoró el texto del método, es que hay lógica crítica en el lugar equivocado.** El método es guía de calidad; la corrección la impone el Core.

**Y todo lo que produzca B2 es una propuesta.** No es el expediente, no está incorporado, no está aprobado. Quien decide qué es verdad es ella, siempre.

### 5.2 Si en B2 siguen apareciendo citas inventadas

**No es un fallo del método. Es el dato que este ejercicio existe para producir.**

Es la diferencia entre sostener por convicción que hace falta un Core y **haberlo observado**: *pusimos el mejor método que sabemos escribir delante de la herramienta, y siguió afirmando cosas que no existen*. Ese es el argumento que ninguna cantidad de arquitectura escrita puede sustituir.

Se registra con la ficha de incidente completa, más un campo nuevo: **`condición: sin método / con método`**. Y se reporta aparte, porque:

- Los incidentes de **B1** justifican que exista un producto.
- Los incidentes de **B2** justifican que ese producto tenga un **gate**, y no solo buenos métodos escritos.

**Además, hay que decirlo aunque no nos convenga:** las citas jurídicas inventadas **el v0 tampoco las previene**. La verificación de fuentes está fuera del alcance del vertical slice y no se carga ningún Knowledge Pack. Un producto que no ataca un fallo y no lo dice está mintiendo por omisión: esa frase va en el informe.

### 5.3 Si en B2 **dejan** de aparecer

Hay que tener escrita también esta lectura, antes de conocerla, para no sobreleerla:

- **Ausencia de evidencia no es evidencia de ausencia.** La conclusión legítima es *"no se observó en las N afirmaciones verificadas de esta corrida"*. Nunca *"el método lo previene"*.
- **Una corrida no separa el efecto del método del ruido de la herramienta** (§3.4). Sin las dos pasadas idénticas, una mejora pequeña no es una mejora: es una observación.
- **Un B2 bueno no invalida el principio de arquitectura.** La razón de tratar a la herramienta como cliente no confiable es **estructural, no estadística**: que se porte bien una vez no la vuelve confiable. Un resultado bueno puede reducir el **tamaño** de lo que hay que construir; no cambia el **principio** de diseño. Confundir las dos cosas sería el error de lectura más caro que podríamos cometer.

---

## 6. Dónde se anota

**No se crea ninguna hoja nueva.** Se usa `docs/discovery/baseline-hoja-de-registro.md`, **una copia por sesión y por brazo** — una sesión pertenece a un solo brazo, así que no hay filas mezcladas.

Tres añadidos mínimos, y ninguno más:

1. **En «Datos de la sesión»**, tres líneas nuevas:
   - `Brazo: ☐ sin método ☐ con método`
   - `Cómo se cargó el método: ☐ pegado al inicio ☐ instalado en la aplicación ☐ otro: ____` · `¿se repegó en la sesión 2? ☐ sí ☐ no`
   - `¿Se confirmó en el ensayo en seco que estaba actuando? ☐ sí ☐ no ☐ no se pudo` · `Fecha y versión de la aplicación: ____`
2. **En el registro de incidentes**, la fila no cambia: el brazo ya queda fijado por la cabecera de la hoja. Lo que sí se añade, y es importante, es una fila de **aciertos** cada vez que la herramienta haga por su cuenta algo que el método pedía — sobre todo el tipo 4 (*avisó de una duda o dijo que no lo sabía en vez de inventarlo*), que es el que siempre se olvida anotar.
3. **En «Momentos de fricción»**, todo lo del §4.5. Si el método hizo el trabajo más lento o más incómodo, ahí va, y cuenta.

**Las conversaciones guardadas** llevan el brazo en el nombre: `sesion-1-sin-metodo`, `sesion-1-con-metodo`, y así. Se guardan donde manda el protocolo y se borran cuando el análisis termine.

**Las cifras `b_`** van al informe de cierre de la rúbrica (`docs/discovery/baseline-analisis-y-rubrica.md` §7), **separadas por brazo y nunca fundidas en un solo número**. Las que quedaron sin poder estimarse en B2 se listan como `NO ESTIMABLE EN B2`, con el motivo.

**Preinscripción.** Este documento, la opción de comparación elegida (§3.3), el reparto de pasadas (§3.4) y qué se espera que ocurra **se commitean con fecha antes de correr B2**. Lo que no esté escrito antes no puede presentarse después como predicción confirmada.

---

## 7. Lo que NO hay que hacer

| Prohibido | Por qué |
|---|---|
| **Correr B2 antes que B1** | Destruye la vara y no se recupera |
| **Editar el método entre sesiones o entre brazos** | Serían dos métodos y ningún resultado |
| **Meter datos del caso en el texto que se pega** | Destruye la sesión 2, que es la más informativa del protocolo |
| **Mejorar las peticiones porque «ahora entiende mejor»** | Deja de compararse la condición y pasa a compararse cómo preguntamos |
| **Meter el archivo del método en la carpeta del caso** | Contamina la petición 1 y el conteo de documentos |
| **Instalar o configurar algo el día de la sesión** | La fricción de nuestra improvisación se registraría como fricción de la herramienta |
| **Decir «el método mejoró un 30 %»** | Una persona y un caso: conteos con denominador, jamás porcentajes |
| **Atribuir al método una diferencia pequeña** | Sin las dos pasadas idénticas no se sabe cuánto varía la herramienta consigo misma |
| **Presentar un B2 bueno como que el Core sobra** | El principio es estructural, no estadístico |
| **Presentar un B2 malo como fallo del método** | Es la medida de por qué hace falta el Core: el mejor dato del ejercicio |
| **Dejar sin anotar las contradicciones inventadas** | Es el modo de fallo que el propio método puede provocar. Está escrito antes por eso |

---

## Lista de comprobación

**ANTES DE B2**

- [ ] **B1 terminado, guardado y con su salida numerada**
- [ ] Opción de comparación elegida (A / B / C) y **escrita con fecha**
- [ ] Reparto de pasadas decidido (§3.4) y escrito: qué pregunta se compra y cuál se deja sin medir
- [ ] Criterios de comparabilidad escritos **antes** de mirar candidatos, si es Opción A · caso asignado **por sorteo**
- [ ] Ensayo en seco hecho, en otro día, con material falso · resultado anotado
- [ ] Vía de carga decidida — si el ensayo no confirmó nada, **vía A**
- [ ] Texto del método a mano, íntegro, **sin un solo dato del caso dentro**
- [ ] Peticiones de B1 transcritas literalmente, para reutilizar sus palabras
- [ ] Hoja previa de B1 **congelada** (no se reescribe)
- [ ] Copias de la hoja de registro con las tres líneas nuevas de la cabecera

**DURANTE**

- [ ] Pegar el método **antes** de la petición 1 · esperar respuesta · después empezar
- [ ] **Repegarlo idéntico** al abrir la conversación nueva de la sesión 2
- [ ] Mismas peticiones, mismo orden, mismo corte entre días
- [ ] No comentar la salida en caliente. No guiar. No repetir peticiones
- [ ] Anotar aciertos, y sobre todo cuando **avisa de una duda en vez de inventar**
- [ ] Anotar la fricción que introduzca el propio método

**AL CERRAR**

- [ ] Cifras por brazo, nunca fundidas · lo no estimable, listado como tal
- [ ] Citas inventadas de B2 registradas con `condición: con método` — **y leídas como argumento del Core, no como fallo del método**
- [ ] Contradicciones inventadas contadas
- [ ] Fracción verificada a ciegas o por sorteo, con los dos números a la vista, sin extrapolar
- [ ] Versión de la aplicación en cada brazo · si cambió, **declarado**
