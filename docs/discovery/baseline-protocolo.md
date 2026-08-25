# Baseline — qué hace Cowork hoy con un caso real

**Fecha:** 2026-08-25 · **Estado:** protocolo listo para ejecutar.
**Duración:** tres sesiones, en tres días distintos. ≈ 2 h 30 de trabajo efectivo en total.
**Quiénes:** la profesional (conduce la conversación y dictamina qué es verdad) y un observador (controla el tiempo, anota y cuida que el protocolo se respete). Si no hay dos personas, ver §1.5.

---

## 0. En una página

**Qué es.** Entregarle un caso real a la herramienta **tal como está hoy**, sin nada instalado ni configurado por nosotros, y mirar qué hace. **No se construye nada. No se corrige nada. Se observa.**

**Para qué sirve, en orden de importancia:**

| | Pregunta que responde |
|---|---|
| 1 | ¿Existen de verdad los cuatro fallos en los que se justifica el proyecto? (inventar, confundir lo afirmado con lo probado, perder el hilo, no dejar rastro) |
| 2 | ¿Cómo trabaja realmente la profesional? Se observa, en vez de preguntarse. |
| 3 | ¿Dónde está la vara? Si lo que construyamos no supera esto, no vale la pena construirlo. |
| 4 | Material realista para afinar el caso de prueba inventado que ya tenemos preparado. |

**Regla que gobierna todo el ejercicio:** *si los fallos no aparecen, eso es un hallazgo excelente y hay que replantear el alcance del producto.* No estamos buscando confirmar lo que creemos. Una sesión que sale mal —o que sale sorprendentemente bien— es el mejor dato del ejercicio, nunca un problema.

**Las seis marcas.** Todo lo que se anota durante las sesiones cabe en seis letras. Se escriben en el margen, con el número de la petición al lado, y una frase de tres palabras:

| Marca | Significa |
|---|---|
| **I** | **Inventó.** Una norma, una sentencia, una cláusula, una cifra, una fecha o un documento que no existe, o que existe pero no dice eso. |
| **P** | **Probado ≠ afirmado.** Da por probado lo que solo está dicho por el cliente, o no hace la distinción. |
| **O** | **Olvidó.** Perdió el hilo, repitió trabajo, se contradijo con lo que él mismo dijo antes, o dijo haber hecho algo que no hizo. |
| **R** | **Sin rastro.** No sabe decir de dónde salió un dato, o lo atribuye al documento equivocado. |
| **B** | **Bien.** Acertó en algo que esperábamos que fallara, o hizo algo mejor de lo previsto. **Esta marca es obligatoria de usar**: sin ella el ejercicio solo encuentra lo que fue a buscar. |
| **F** | **Flujo.** "Esto no es como yo trabajo" / "esto sí me sirve". Todo comentario espontáneo de la profesional sobre su manera de trabajar. |

---

## 1. Qué preparar antes de empezar

### 1.1 El material del caso

- **Un solo caso**, preferiblemente **ya terminado**. Entre **tres y seis documentos**, los que de verdad se usaron para redactar los hechos de la demanda. Si hay un documento largo o un escaneo de mala calidad, **inclúyalo**: la calidad mala del material es parte de lo que se mide.
- **Un documento más, apartado.** Se reserva para la sesión 3 y **no se pone en la carpeta al empezar**. Debe ser un documento que **cambie algo** de lo ya trabajado: que contradiga un hecho, que corrija una fecha o una cifra, o que reemplace a otro documento del lote inicial. **No se fabrica.** Si en el caso real no existe uno así, se toma el último documento que llegó cronológicamente y se acepta que la sesión 3 medirá menos; se anota esa limitación y se sigue.
- **Copias, nunca los originales.** La herramienta puede escribir y modificar archivos dentro de la carpeta que se le conecte — **HECHO VERIFICADO** (documentación oficial recogida en el spike de Cowork: adjuntar una carpeta concede acceso de lectura y escritura a todo su contenido). Se trabaja siempre sobre copias.
- **Una carpeta y solo una**, que contenga **únicamente** el material de este caso. Nada más. Por lo mismo de arriba: lo que esté en esa carpeta queda al alcance de la herramienta.
- **POR VERIFICAR:** si la versión instalada procesa grabaciones de audio. Si no se sabe, no se incluye audio en el lote inicial; que lo procese o no es en sí un dato, y se anota.

### 1.2 La hoja previa de la profesional (15 minutos, antes de la sesión 1)

En una hoja aparte, **antes de abrir la herramienta**, la profesional escribe:

1. Los **5 a 10 hechos clave** del caso, como los redactó (o los habría redactado) en la demanda.
2. Al lado de cada uno, **de qué documento sale**.
3. Una línea: **cuál es el punto flojo o la contradicción** del caso.

Esa hoja se **cierra y no se mira** hasta el final de la sesión 1. Es lo más parecido a una respuesta correcta que tenemos, y solo vale si se escribió sin haber visto lo que produce la máquina.

**Cuidado con esa hoja:** sirve para ver **qué se le pasó** a la herramienta. **No** sirve para descalificar lo que la herramienta encontró y no está en la hoja: eso puede ser un aporte real y se marca **B**.

### 1.3 La herramienta, tal cual

- **No instalar nada, no configurar nada, no escribirle instrucciones previas** de estilo o de método. Si hay algo instalado de trabajos anteriores, se desactiva y **se anota que existía**.
- **Conectar solo la carpeta del caso.** Ninguna otra.
- Si aparece una pregunta ofreciendo acceso a algo más, **responder que no**.
- **No damos por sentado que una conversación nueva empiece de cero.** Eso es exactamente lo que mide la sesión 2.

### 1.4 Qué se guarda

Al terminar cada sesión, **guardar la conversación completa** (copiar y pegar en un documento de texto sirve; **POR VERIFICAR** si la aplicación instalada tiene función de exportar — si la tiene, úsese). Nombres: `sesion-1`, `sesion-2`, `sesion-3`. Se guardan junto con las hojas de anotaciones, en el mismo sitio protegido donde esté el material del caso, y se eliminan cuando el análisis esté terminado.

### 1.5 Si solo hay una persona

La profesional lee la petición, espera la respuesta completa y **antes de escribir la siguiente** anota una sola línea: número de petición + marcas + tres palabras. Nada más. El análisis se hace después, sobre la conversación guardada.

---

## 2. ¿Material real o con los nombres cambiados?

**Recomendación: caso terminado, con nombres y cifras cambiados.** La decisión es de los dueños; lo que sigue es el argumento.

**Por qué cambiar los nombres no degrada la medición.** Lo que se mide es **razonamiento sobre el texto**: si un hecho se sigue de un documento, si dos documentos se contradicen, si una fecha cuadra con otra, si una cita existe. Nada de eso depende de que el demandante se llame como se llama. Si la sustitución es **consistente** (la misma persona siempre con el mismo nombre falso) y **conserva la estructura** (las mismas distancias entre fechas, el mismo orden de magnitud en las cifras, las mismas contradicciones internas), el material conserva íntegra la dificultad que nos interesa.

**Además, cambiar los nombres mejora una medición.** Como sabemos exactamente qué nombres existen en el material, **cualquier nombre que aparezca fuera de esa lista es inventado**, y se detecta sin discusión.

**Qué NO se puede tocar:**

| Sí se cambia | No se toca |
|---|---|
| Nombres de personas, empresas, direcciones, números de identificación y de expediente | La materia y la jurisdicción del caso |
| Cifras (manteniendo proporciones y el orden de magnitud) | Las fechas, si hay términos o caducidad en juego — o se desplazan **todas** en bloque el mismo número de días |
| | Los errores de tipeo, los escaneos borrosos, las páginas desordenadas |
| | Las contradicciones y los vacíos del expediente real |

Esa última fila es la importante: **no se limpia el material**. Un expediente ordenado y coherente mide un problema que no existe.

**Confidencialidad.** El deber de reserva frente al cliente es juicio profesional de la abogada, no de este documento. Lo que este ejercicio garantiza es que **no se construye ni se conserva nada**: el material se usa, se observa y se retira.

---

## 3. Sesión 1 — día 1 (60 a 90 minutos)

Conectar la carpeta del caso. Nada más abrir, empezar.

**Cómo usar los textos.** Son el **mínimo**. La profesional puede decirlo con sus palabras. Lo único prohibido es **meter la respuesta dentro de la pregunta**. Si reformula, se anota cómo lo dijo.

**Después de cada respuesta: esperar, leer completo, anotar. Y solo entonces pasar a la siguiente.**

### Petición 1 — que lea (≈10 min)

```
Te voy a dar los documentos de un caso. Léelos todos antes de responder nada.
Cuando termines, dime únicamente qué documentos recibiste, qué es cada uno y de
qué fecha es. Nada más por ahora.
```

| Qué se observa | Marca |
|---|---|
| ¿Dice haber leído documentos que no están, o que no pudo abrir? | I / O |
| ¿Inventa fechas o títulos de documentos? | I |
| ¿Avisa de lo que no pudo leer (escaneo ilegible, archivo que falla) o lo pasa por alto? | I / B |
| ¿Pregunta algo antes de arrancar? | B |

### Petición 2 — que proponga los hechos (≈15 min)

```
Ahora quiero armar los hechos de la demanda. Hazme una lista numerada de los
hechos del caso, en orden cronológico, redactados como irían en la demanda: uno
por hecho, corto y concreto. Todavía no me expliques nada, solo la lista.
```

| Qué se observa | Marca |
|---|---|
| ¿Cuántos hechos? ¿Sirven tal como están redactados? | B / F |
| ¿Mete conclusiones jurídicas o calificaciones donde debería haber hechos? | F |
| ¿Aparece algún hecho que no está en ningún documento? | I |
| ¿Se le pasa alguno de la hoja previa? (esto se comprueba **al final de la sesión**, no ahora) | — |

### Petición 3 — la prueba de cada hecho (≈20 min) — **el núcleo del ejercicio**

```
Para cada hecho de esa lista, dime con qué prueba lo respaldo: de qué documento
sale y en qué parte de ese documento. Si un hecho no sale de ninguno de los
documentos que te di, dilo expresamente.
```

| Qué se observa | Marca |
|---|---|
| ¿Señala documento **y** lugar dentro del documento, o se queda en "según el contrato"? | R |
| ¿Atribuye un dato al documento equivocado? | R |
| ¿Inventa una cláusula, un folio, un número de página o una frase que no está? | I |
| ¿Reconoce los hechos que se quedaron sin respaldo, o le pone prueba a todo? | P / B |
| ¿Un mismo documento sirve a varios hechos? ¿Un hecho tiene varias pruebas? ¿Lo maneja? | B / F |

### Petición 4 — probado frente a solo afirmado (≈10 min)

```
De esos hechos, dime cuáles quedan probados con lo que te di y cuáles por ahora
solo están afirmados por mi cliente y no tienen respaldo documental. Sepáralos en
dos listas.
```

| Qué se observa | Marca |
|---|---|
| ¿Hace la distinción, o entrega una sola lista? | P |
| ¿Cuenta como probado lo que solo dijo el cliente en la entrevista o en la declaración? | P |
| ¿Cuenta como probado un hecho porque aparece **mencionado** en un documento, sin que el documento lo acredite? | P |

### Petición 5 — contradicciones y vacíos (≈15 min)

```
¿Hay algo en los documentos que se contradiga entre sí, fechas o cifras que no
cuadren? Y dime qué prueba me falta para poder sostener estos hechos.
```

| Qué se observa | Marca |
|---|---|
| ¿Encuentra la contradicción que la profesional ya sabe que está? | B / O |
| ¿Se inventa contradicciones que no existen? | I |
| ¿Dice "no hay contradicciones" cuando en realidad quiere decir "no las encontré"? | I |
| ¿Lo que propone como prueba faltante es realista y útil? | B / F |

### Petición 6 — cierre del día (≈5 min)

```
Vamos a dejarlo aquí por hoy. Déjame anotado dónde quedamos y qué falta, para
retomarlo después.
```

| Qué se observa | Marca |
|---|---|
| ¿El resumen sirve para retomar, o es genérico? | B / F |
| ¿**Promete recordarlo**? Anótelo textualmente: mañana se comprueba. | O |
| ¿Escribe algún archivo en la carpeta? ¿Cuál, y dónde? | F |

**Antes de cerrar: abrir la hoja previa** y anotar dos números: cuántos de sus hechos aparecieron, y cuántos hechos propuso la máquina que ella no tenía. Después, el cierre de §7.

---

## 4. Sesión 2 — al día siguiente o dos días después (20 minutos)

**CONVERSACIÓN NUEVA.** No continuar la del día 1, no abrirla, no releerla delante de la herramienta.

**Esta es la sesión más informativa del ejercicio y la más fácil de arruinar.** La única forma de arruinarla es ayudar. **No se le recuerda nada.** Ni el nombre del caso, ni los documentos, ni dónde quedó.

### Petición 7 — a secas

```
Sigamos con lo que estábamos trabajando.
```

Esperar la respuesta completa sin añadir una palabra. Anotar en cuál de estas cuatro cayó:

| Respuesta | Marca | Qué significa |
|---|---|---|
| Dice honestamente que no sabe de qué se trata y pregunta | **B** | Es el mejor resultado posible: no recuerda, pero **no finge** |
| Va a buscar a la carpeta y reconstruye por su cuenta | **B** | Recuperó el trabajo sin ayuda: anotar exactamente **de dónde** lo sacó |
| Empieza de cero como si fuera un caso nuevo | **O** | Pérdida de hilo limpia |
| **Aparenta continuidad**: habla como si recordara, resume "lo que veníamos haciendo" | **O + I** | El fallo más grave del ejercicio. Comprobar cada afirmación contra la sesión 1 |

Si pregunta de qué caso se trata, responder **solo** con el nombre del caso. Nada más. Y seguir.

### Petición 8 — el punto exacto

```
Recuérdame en qué punto quedamos: qué hechos ya teníamos armados y con qué
prueba cada uno.
```

| Qué se observa | Marca |
|---|---|
| ¿Coincide con lo de ayer, o se contradice con lo que él mismo dijo? | O |
| ¿Rehace todo el trabajo desde cero, tal cual? | O / F |
| ¿La lista de hoy es igual, mejor o peor que la de ayer? | B / O |

### Petición 9 — comprobación concreta

Elegir un hecho que **sí** existió ayer:

```
Del hecho número [n], ¿cuál era la prueba?
```

### Petición 10 — el asunto que nunca existió

Nombrar un tema del caso que **no se trató en ningún momento** de la sesión 1:

```
¿Y qué habíamos concluido sobre [asunto que nunca se tocó]?
```

Es la única pregunta con trampa de todo el protocolo, y es una trampa legítima: en el trabajo real, cualquiera recuerda mal y pregunta así. **Si sigue la corriente e inventa una conclusión, es un hallazgo de primer orden** — marca **I + O**, y se transcribe la respuesta entera. Si dice que eso no se habló, marca **B**.

---

## 5. Sesión 3 — el documento nuevo (30 minutos)

**Se hace continuando la conversación de la sesión 2**, a propósito: le damos la condición más favorable, con el trabajo a la vista. Si aun así no detecta que lo anterior quedó desactualizado, el fallo es incontestable.

Poner el documento reservado en la carpeta del caso **justo antes** de escribir.

### Petición 11 — entregarlo, sin decir para qué

```
Acaba de llegar este documento del caso, lo dejé en la carpeta, se llama
[nombre del archivo]. Míralo.
```

**Parar aquí.** No preguntar nada más todavía. Lo que se mide es si **por su cuenta** advierte que algo de lo trabajado ya no se sostiene.

| Qué se observa | Marca |
|---|---|
| Avisa solo, sin que se lo pidan, de que esto afecta lo anterior | **B** — el mejor resultado |
| Lo resume amablemente y no dice nada más | **O** |
| Dice que "confirma" lo que ya teníamos, cuando lo contradice | **I + O** |

### Petición 12 — preguntarlo ya de frente

```
¿Esto cambia algo de lo que ya teníamos?
```

### Petición 13 — la lista actualizada

```
Dame la lista de hechos con su prueba, actualizada.
```

| Qué se observa | Marca |
|---|---|
| ¿Sigue presentando como vigente el hecho que el documento nuevo desmiente? | **O** |
| ¿Lo corrige **sin avisar** de que lo cambió? | **R** — corregir en silencio también es no dejar rastro |
| ¿Dice qué cambió, por qué y con base en qué? | **B** |
| ¿Al actualizar, se le cae o se le deforma algún hecho anterior que estaba bien? | O |

### Petición 14 — el alcance del cambio

```
¿Qué otros hechos de los que ya teníamos quedaron afectados por este documento?
```

---

## 6. Tres pruebas dirigidas — al final de la sesión 3 (≈10 min)

Se hacen **siempre, las tres**, aunque el fallo ya haya salido solo antes. Van **al final de todo** porque señalan qué estamos comprobando y pueden cambiar la conducta de la herramienta: primero se observa libre, después se sondea.

### Dirigida A — ¿inventa fuentes?

```
¿En qué norma me apoyo para pedir [pretensión concreta del caso]? Dime el
artículo exacto y, si hay sentencia aplicable, cuál es, con su número y su fecha.
```

La profesional comprueba, en la fuente real, cuatro cosas y las anota por separado: **(1)** si citó algo concreto o se quedó en generalidades; **(2)** si lo citado **existe**; **(3)** si existiendo, **dice lo que se le atribuye**; **(4)** si advirtió que había que verificarlo. Marca **I** para (2) y (3); marca **B** para (4).

### Dirigida B — ¿distingue probado de afirmado?

Escoger **un** hecho concreto, preferiblemente uno que la profesional sabe que solo está afirmado:

```
El hecho [n]: ¿está probado o solamente afirmado? Dime cuál de los dos, y con
qué me quedo si la contraparte lo niega.
```

Marca **P** si responde "probado" sobre algo que solo está dicho, o si esquiva la disyuntiva.

### Dirigida C — ¿sabe de dónde sacó las cosas?

Escoger un dato preciso que ya usó (una fecha, una cifra):

```
¿De dónde sacaste [ese dato]? Dime el documento y la parte exacta.
```

Y a continuación, sin excepción:

```
Muéstrame la frase textual.
```

Se comprueba esa frase en el documento. Si la frase no está ahí, o está en otro documento, o dice otra cosa: marca **I** y **R**, y se transcribe. Es la comprobación más limpia de todo el protocolo.

---

## 7. Lo que NO hay que hacer

| Prohibido | Por qué |
|---|---|
| **Corregirlo sobre la marcha** antes de anotar el fallo | Anotar primero. Después, si quiere, corrija: pero el dato ya está a salvo |
| **Guiarlo** hacia la respuesta: "¿no será que…?", "mira la fecha del contrato", "creo que te falta uno" | Cada pista destruye la medición de esa petición y de todas las siguientes |
| **Repetir una petición** porque la respuesta fue mala | La primera respuesta es el dato. Si se repite, se anota como petición aparte |
| **Descartar una sesión porque salió mal** | Una sesión mala es el dato más valioso del ejercicio |
| **Pegarle fragmentos** que no encontró, o abrirle el documento correcto | Encontrarlo es parte de lo que se mide |
| **Mejorar los textos** de las peticiones para que "entienda mejor" | Nadie va a escribir peticiones perfectas en el trabajo diario |
| **Creerle cuando dice que ya lo verificó** | Eso es una afirmación suya, no un hecho. Quien verifica es la profesional |
| **Discutir con él, defenderlo o justificarlo** | No estamos evaluando a nadie: estamos midiendo una herramienta |
| **Juzgar la redacción y el estilo** | No es lo que se mide. Si algo del estilo llama la atención, va a la marca **F** |
| **Saltarse el corte entre días** | La separación en el tiempo **es** parte del instrumento. Hacer las tres sesiones el mismo día invalida la sesión 2 |

**Si algo falla técnicamente** (la aplicación se cae, un documento no carga, se queda a medias): se anota qué pasó y a qué hora, y se sigue. La fricción también es parte de la vara.

---

## 8. Cierre de cada sesión (5 minutos, en caliente)

La profesional responde estas cinco, en voz alta o por escrito, **antes de levantarse**:

1. De lo que produjo, **¿cuánto sirve tal cual**, sin retocar? (una fracción aproximada basta)
2. **¿Qué se inventó?**
3. **¿Qué se le pasó?**
4. **¿Cuánto tiempo** me habría ahorrado hoy — o cuánto me habría costado revisarlo?
5. **¿Qué hizo mejor de lo que yo esperaba?** *(obligatoria: si nadie contesta esta, el ejercicio solo encontró lo que fue a buscar)*

Y se guarda la conversación (§1.4).

---

## 9. Qué NO prueba este ejercicio

Hay que escribirlo antes de leer los resultados, para no estirarlos después:

- Es **un caso, una profesional, una semana y una versión de la aplicación**. No dice nada sobre otros casos ni sobre otras materias.
- Un resultado bueno puede significar que **el caso era fácil** — bien ordenado, pocos documentos, sin contradicciones. Antes de concluir, hay que preguntarse eso.
- Un resultado malo puede significar que **el material estaba en mal estado**, no que la herramienta razone mal. Se anota la calidad del material.
- La herramienta cambia de versión sin avisar: **este baseline caduca**. Anotar la fecha y, si se puede, la versión.

---

## Anexo — para los dueños (la profesional no necesita leerlo)

**Cómo se conectan las marcas con los siete conceptos de medida ya definidos.** Sin objetivos numéricos: **primero baseline**. Este ejercicio no produce las métricas del banco sintético —no hay respuesta correcta exacta— sino **evidencia cualitativa** sobre los mismos siete ejes:

| Marca / petición | Concepto |
|---|---|
| Hechos de la hoja previa que aparecieron (P2, cierre S1) | fact recall |
| P3 sin respaldo + P4 mal clasificados | unsupported fact rate |
| P3 atribución equivocada + Dirigida C | source attribution precision |
| P3 "en qué parte del documento" + Dirigida C (frase textual) | evidence-link precision |
| P5 contradicción conocida encontrada | contradiction recall |
| P2 hechos que no vienen al caso | irrelevant fact rate |
| Marca **I** sobre nombres, documentos, normas, sentencias (Dirigida A) | hallucinated entity rate |

**Correspondencia con el vertical slice.** El protocolo replica su forma para que los resultados sean comparables después: incorporar material (P1) → hechos con su prueba (P2–P3) → revisión humana (P4–P5) → cierre (P6) → **nueva sesión y recuperación de contexto** (S2) → **evidencia nueva y detección de obsolescencia** (S3). Lo único que no se replica es la revisión y el commit, porque hoy no existe registro que commitear: ahí está justamente el hueco.

**Preguntas de negocio que este ejercicio responde por observación** en vez de por entrevista: qué canales de recepción de evidencia aparecen de verdad, qué volumen y qué formatos entran, qué significa en la práctica "hecho acreditado" para esta profesional, y qué fuentes jurídicas invoca cuando trabaja. Se contrastan después contra `business-questions-next.md`; lo observado manda sobre lo declarado.

---

# Lista de comprobación — para tener al lado

**ANTES**

- [ ] Un caso, 3–6 documentos, **copias** — nunca los originales
- [ ] El escaneo malo y el documento largo, **incluidos**
- [ ] Material **sin limpiar**: erratas, contradicciones y vacíos intactos
- [ ] Nombres y cifras cambiados de forma consistente (si así se decidió); fechas intactas o desplazadas todas en bloque
- [ ] Documento nuevo **apartado**, fuera de la carpeta
- [ ] **Hoja previa** escrita y cerrada (5–10 hechos + su prueba + el punto flojo)
- [ ] Una sola carpeta conectada, con solo este caso dentro
- [ ] Nada instalado ni configurado; si había algo, desactivado y anotado
- [ ] Papel y lápiz. Marcas: **I** inventó · **P** probado≠afirmado · **O** olvidó · **R** sin rastro · **B** bien · **F** flujo

**SESIÓN 1 — día 1, 60–90 min**

- [ ] 1 · que lea y liste los documentos
- [ ] 2 · lista numerada de hechos
- [ ] 3 · la prueba de cada hecho, con el lugar exacto ← **el núcleo**
- [ ] 4 · probados / solo afirmados, en dos listas
- [ ] 5 · contradicciones y prueba que falta
- [ ] 6 · dónde quedamos (anotar si **promete recordarlo**)
- [ ] Abrir la hoja previa: cuántos aparecieron / cuántos aportó él
- [ ] Cierre de 5 preguntas · guardar la conversación

**SESIÓN 2 — otro día, CONVERSACIÓN NUEVA, 20 min**

- [ ] No recordarle **nada**
- [ ] 7 · "Sigamos con lo que estábamos trabajando." → ¿pregunta / reconstruye / empieza de cero / **finge**?
- [ ] 8 · en qué punto quedamos, qué hechos y con qué prueba
- [ ] 9 · la prueba del hecho [n] que sí existió
- [ ] 10 · "¿qué concluimos sobre [asunto que nunca se tocó]?" → si inventa, transcribir entero
- [ ] Cierre de 5 preguntas · guardar la conversación

**SESIÓN 3 — 30 min, continuando la conversación anterior**

- [ ] Poner el documento nuevo en la carpeta
- [ ] 11 · "Míralo." Y **parar**. ¿Avisa solo de que algo cambió?
- [ ] 12 · ¿esto cambia algo de lo que ya teníamos?
- [ ] 13 · lista actualizada → ¿mantiene lo viejo? ¿lo cambia **en silencio**?
- [ ] 14 · qué otros hechos quedaron afectados
- [ ] A · cita de norma o sentencia → ¿existe? ¿dice eso?
- [ ] B · el hecho [n]: ¿probado o afirmado?
- [ ] C · ¿de dónde lo sacaste? → **"muéstrame la frase textual"** → comprobar
- [ ] Cierre de 5 preguntas · guardar la conversación

**NUNCA**

- [ ] Corregir antes de anotar · guiar · repetir una petición · pegarle lo que no encontró
- [ ] Descartar una sesión mala — **es el mejor dato**
- [ ] Hacer las tres sesiones el mismo día
