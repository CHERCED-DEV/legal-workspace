# El instrumento de verificación — la ficha y cómo se llena

**Fecha: 2026-08-27. Material de trabajo, no una Skill.** Se escribe porque §8.2 quedó decidida: hay una abogada que verifica, y se acepta la regla dura *sin vigencia comprobada y firmada, la norma no se sirve como citable*.

**Este archivo no contiene una sola norma, una sola fecha de vigencia ni un solo estado.** Todo lo que aquí parece un dato jurídico es un relleno evidente (`LEY-0000-0000`, `AAAA-MM-DD`, `art. 00`). El contenido lo escribe la verificadora. Si el modelo escribe un dato en una ficha, el instrumento queda anulado: ver §5, regla 1.

El contrato de consumo —qué contesta el pack y qué no— está en [02-contrato-de-consumo.md](02-contrato-de-consumo.md). Los dos archivos se leen juntos: la ficha sin el contrato es una tabla bonita, y el contrato sin la ficha no tiene qué servir.

---

## §0 — Qué sustituye este instrumento

Hoy lo único que impide que el sistema cite una norma derogada es que **no cita normas** (`REFINADO-Y-FUENTES.md` §1.a). Es una abstinencia, no un mecanismo, y se acaba el día que exista el pack. Esto es lo que la reemplaza. Y hay que decirlo entero: la seguridad del producto se demuestra hoy con un grep sobre la prosa de la entrega que exige **cero citas jurídicas**. **El día uno del pack ese instrumento deja de funcionar**, porque a partir de ahí las citas son legítimas y el grep ya no distingue la buena de la fabricada. El pack retira la única comprobación mecánica que existe; el que la repone es el `token_de_respuesta` de `02` §1 R4. Sin ese token, este instrumento resta seguridad en vez de añadirla.

El fallo concreto que hay que hacer imposible ya ocurrió dentro del propio corpus: **un registro comprobado en su identidad —«esta norma existe y es esta»— leído como comprobado en su vigencia —«esta norma rige»—**. Hoy las dos cosas comparten una sola etiqueta (`VERIFIED_OFFICIAL` / `FUENTE_OFICIAL_VERIFICADA`) y esa etiqueta convive con la columna de vigencia en blanco en el 100 % de las filas.

**Volumen, contado sobre el catálogo: 26 filas normativas** —no 25— **y 4 providencias**. Pero el catálogo **nombra ~46 identificadores normativos distintos**: las ~20 que no son filas propias aparecen en la columna «Relaciones y dependencia» y son justamente las **modificatorias**, es decir, las que deciden si las 26 rigen en su redacción original. No entran al primer pack. Lo que se hace con ellas en vez de ficharlas está en el campo 6 (`VIGENTE_CON_REFORMA_AL`) y en `02` §7. **Qué está comprobado hoy:** el hasta cuándo, en ninguna fila —`effective_to` es «desconocido» o prosa en el 100 % de la matriz—. El desde sí está escrito en el catálogo, y eso es un problema, no un alivio: el riesgo de P3 no es el tiempo, es la copia (P0.b).

---

## §1 — La regla de diseño: dos columnas que nunca se juntan

1. **`estado_identidad` y `estado_vigencia` son dos campos.** No hay ningún campo, ninguna etiqueta y ninguna respuesta del pack que combine las dos en un solo valor. Tampoco hay un estado «verificado» a secas.
2. **La disciplina baja hasta la fuente.** Identidad y vigencia se comprueban contra fuentes distintas y se registran en campos distintos (`fuente_identidad`, `fuente_vigencia`). Una sola casilla de «fuente» vuelve a fundir las dos columnas por la puerta de atrás.
3. **Dos renombrados antes de que nada del catálogo entre al pack, y hay que decir su tamaño real.**
   - `VERIFIED_OFFICIAL` / `FUENTE_OFICIAL_VERIFICADA` → **`IDENTIDAD_VERIFICADA`**. Medido: **33 ocurrencias en 13 archivos**. `source-catalog/` son 4 de ellos; los otros 9 son `practice-areas/`, `workflows/05, 06, 10`, `evals/`, `review-patterns/` y sobre todo **`04-source-governance.md` §4 y §4.1, que es donde el término está definido**. Alcanza a los 13 o no se hace: renombrar solo el catálogo deja la definición en un vocabulario, los workflows en otro y el catálogo en un tercero — el problema que `ESTADO-DEL-PROYECTO.md` §3 fila 9 ya tiene abierto, agravado.
   - `VIGENCIA_POR_VERIFICAR` **se parte en dos, porque hoy significa dos cosas opuestas**: en `04`:59 es la etiqueta visible de `OUTDATED` («se comprobó y está vieja»); aquí significaba «nadie miró». Dentro del pack: **`VIGENCIA_NO_COMPROBADA`** = nadie miró; **`VIGENCIA_DESACTUALIZADA`** = se comprobó y está vieja, que en el pack se escribe `SIN_VIGENCIA_DESDE`. Sin esta separación, una etiqueta copiada asciende de «sabemos que caducó» a «no sabemos», que es el mismo colapso de dos significados en uno que este instrumento existe para impedir.
4. **Un registro sin nombre y sin fecha está afirmado, no comprobado.** No existe la ficha anónima: una ficha sin `verificado_por` no es una ficha a medias, es una ficha que el pack no sirve.
5. **Todo campo se lee, o no existe.** El algoritmo de `02` §2 consulta los doce campos de §2 y los nueve de §4. Un campo que se llena treinta veces y no gobierna ninguna rama no es documentación: es trabajo tirado y falsa confianza.

---

## §2 — La ficha de una norma: 12 campos

`Quién`: **V** = la verificadora. **C** = viene del catálogo actual. `Cómo` remite al paso del procedimiento (§5). **Qué significa `C`, operativamente:** se copia como **hipótesis de partida** y no se firma hasta verla en la fuente oficial. El ahorro es de tecleo, no de comprobación — no es «barato». Copiar al pack no vuelve nada verificado (`04-source-governance.md` §7), y 2 de las 26 filas del catálogo ni siquiera tienen la identidad comprobada, así que ahí `C` no ahorra nada.

| # | Campo | Valores admitidos | Quién | Cómo | Qué fallo concreto evita |
|---|---|---|---|---|---|
| 1 | `identificador_canonico` | `TIPO-NUMERO-AÑO` (`LEY-0000-0000`) | C | P1 | La clave de hecho hoy es la URL, y el mismo texto convive con tres formas de dirección dentro del catálogo |
| 2 | `alcance_comprobado` | **estructura, no prosa**: `{norma_completa: si\|no, articulos: [00], incisos: ["00.0"]}` | V | P2 | Comprobar el artículo y servir la ley. Prosa contra prosa no se puede comparar, y lo que no se puede comparar el algoritmo lo daba por bueno |
| 3 | `materia[]` | vocabulario de `06-colombian-law-coverage-ledger.md` | C | P1 | Sin esto, la cobertura no se puede calcular y la ausencia se lee como inexistencia |
| 4 | `estado_identidad` | `IDENTIDAD_VERIFICADA` \| `IDENTIDAD_POR_VERIFICAR` \| `CONFLICTO_DE_FUENTES` | V | P1 | La cita fantasma: un identificador plausible que nadie comprobó |
| 5 | `fuente_identidad` | URL o referencia de publicación oficial + fecha de consulta | C+V | P1 | «Verificado» contra un compilador que en sus propios avisos dice que no certifica |
| 6 | `estado_vigencia` | `VIGENTE_AL AAAA-MM-DD` \| `VIGENTE_CON_REFORMA_AL AAAA-MM-DD` \| `SIN_VIGENCIA_DESDE AAAA-MM-DD` \| `VIGENCIA_PARCIAL_AL AAAA-MM-DD` \| `VIGENCIA_NO_COMPROBADA` | V | P4 | **El campo del encargo.** El quinto valor es el caso más común del derecho —la norma reformada que sigue rigiendo— y antes no tenía dónde ponerse: salía `CITABLE` limpia |
| 7 | `vigencia_desde` | `AAAA-MM-DD` \| `ESCALONADA` | V | P3 | Aplicar la norma nueva a un caso anterior a su entrada en vigor |
| 8 | `fuente_vigencia` | `clase:` **tipada y aparte** (`PRIMARY_OFFICIAL` \| `OFFICIAL_CONSOLIDATED` \| … de `04` §4.1, o `NINGUNA` si no se localizó) + URL o referencia + fecha de consulta. **Nunca un archivo de este corpus** | V | P4 | Que la vigencia se dé por buena porque «el portal no decía nada». Es condición dura de `CITABLE` en `02` §2, no una recomendación en prosa |
| 9 | `nota_de_vigencia` | prosa, máximo dos líneas | V | P3-P4 | La mentira forzada: derogación parcial, entrada escalonada, reforma o control pendiente que no caben en un valor. **El pack nunca la interpreta y la transcribe literal en toda respuesta fechada, `CITABLE` incluida** |
| 10 | `verificado_por` | nombre completo de la persona | V | P5 | Sin nombre no hay nadie que responda, y el registro vuelve a estar afirmado |
| 11 | `verificado_el` | `AAAA-MM-DD` | V | P5 | Un pack sin fechas no envejece: se pudre en silencio |
| 12 | `acortamiento_manual` | `AAAA-MM-DD`, opcional, **solo para acortar** | V | P5 | `revisar_antes_de` **no se almacena**: se calcula al leer (`02` §6). Cuando era escribible, una sola casilla hacía inmortal una ficha |

**Por qué doce y no más.** Seis campos (2, 4, 6, 7, 8, 9) son el trabajo real; tres (1, 3, 5) vienen del catálogo y se confirman; dos (10, 11) son la firma; uno (12) es opcional y solo resta plazo. Cada campo añadido se llena 26 veces: los que se propusieron y no entran están en §3, con el motivo y con el riesgo que queda abierto. **No se añadió ningún campo nuevo al corregir el algoritmo**: lo que cambió es que ahora se leen todos.

### Los dos estados, escritos entero

`estado_identidad`
- `IDENTIDAD_VERIFICADA` — la persona vio el texto en fuente oficial y el identificador corresponde. **No dice nada sobre si rige.**
- `IDENTIDAD_POR_VERIFICAR` — no se pudo cerrar. Es un valor legítimo, no un fracaso.
- `CONFLICTO_DE_FUENTES` — dos fuentes oficiales discrepan en la identidad. Se registran las dos en `fuente_identidad` y **no se elige** (`04` §4). Tiene respuesta propia: un problema de identidad nunca se sirve bajo un código de vigencia.

`estado_vigencia`
- `VIGENTE_AL AAAA-MM-DD` — al día de la comprobación, **solo dentro de `alcance_comprobado`**, y **habiendo buscado también reforma**: es lo que separa este valor del siguiente.
- `VIGENTE_CON_REFORMA_AL AAAA-MM-DD` — rige, **en redacción distinta de la original**. La comprobación cubre el identificador y su vigencia, no la redacción. Obliga a llenar `nota_de_vigencia`.
- `SIN_VIGENCIA_DESDE AAAA-MM-DD` — dato positivo y valioso: el pack sabe que no rige y puede decirlo, y puede servirla para un caso anterior a esa fecha diciendo que hoy no rige.
- `VIGENCIA_PARCIAL_AL AAAA-MM-DD` — rige en parte. Obliga a llenar `nota_de_vigencia` y **nunca se sirve como citable**.
- `VIGENCIA_NO_COMPROBADA` — se buscó y no se pudo establecer, o no se buscó, o no se buscó la reforma. **Es el valor por defecto de todo lo que no encaje**, incluida una casilla vacía o un valor escrito de otra forma. **Será el valor mayoritario del primer pack, y así debe verse desde fuera.**

### Ficha de ejemplo — datos inventados

```yaml
identificador_canonico: LEY-0000-0000
alcance_comprobado: {norma_completa: no, articulos: ["00"], incisos: []}
materia: [area-de-ejemplo]
estado_identidad: IDENTIDAD_VERIFICADA
fuente_identidad: "https://ejemplo.invalido/publicacion-oficial — consultada AAAA-MM-DD"
estado_vigencia: VIGENCIA_NO_COMPROBADA
vigencia_desde: ESCALONADA
fuente_vigencia: {clase: NINGUNA, referencia: "no se localizó fuente PRIMARY_OFFICIAL para el art. 00", consultada: AAAA-MM-DD}
nota_de_vigencia: "la entrada en vigor no es única para toda la norma; no se pudo fijar la del art. 00 en el tiempo disponible"
verificado_por: "Nombre Apellido"
verificado_el: AAAA-MM-DD
acortamiento_manual: null
```

Esta ficha —incompleta, firmada y honesta— **es una ficha válida**. Lo que el pack hará con ella es negarse a servirla como citable y decir por qué. Eso es exactamente lo que se está comprando.

---

## §3 — Lo que se propuso y no entra en la ficha

| Campo del refinado §1.a | Qué se hace | Por qué | Riesgo que queda abierto |
|---|---|---|---|
| `texto_literal` + `locator` + `fecha_de_captura` | **Fuera.** El pack no contiene texto normativo | Transcribir 26 normas es el campo más caro de todos y reabre la superficie de invención justo donde más duele. La decisión de citabilidad no lo necesita | El pack puede confirmar que una norma existe y rige, y el sistema atribuirle algo que no dice. Lo contiene la regla 1 del método y el §4 del contrato, no la ficha |
| `regla_de_entrada_en_vigor` + su pasaje | **Plegado** en `vigencia_desde: ESCALONADA` + `nota_de_vigencia` | La parte comparable contra la fecha de un caso es la fecha; el resto es prosa, y como campo propio era prosa que se creía dato | `ESCALONADA` **nunca es citable** (`02` §2 A.6): solo sirve si se estrecha el alcance hasta donde hay fecha |
| `derogada_por` + `derogada_desde` | **Plegado** en `SIN_VIGENCIA_DESDE` + nota | Para decidir si se cita basta la fecha. Como campo propio invitaba a copiar una afirmación que ya está en otro archivo del corpus y darla por comprobada — el lavado que prohíbe `04` §7 | La abogada ve la fecha y la nota, no un identificador estructurado del acto derogatorio |
| `modificada_por[]` | **Fuera**, pero el hecho de la reforma sí entra | N entradas por registro, y ficharlas serían las ~20 modificatorias del §0: el coste casi se dobla | El pack no dice **qué** norma reformó ni desde cuándo. Sí dice que la reforma existe, con `VIGENTE_CON_REFORMA_AL`, y obliga a decirlo en la respuesta. Registrar que existen sin obligar a ficharlas es todo lo que compra este valor |
| `alcance_derogacion` + `pasaje_derogatorio` | **Fuera** | Ya rechazados en `REFINADO-Y-FUENTES.md` §6. No se resucitan | — |
| `unidad` (ley/artículo/inciso) como taxonomía | **Sustituido** por la estructura de `alcance_comprobado` | §8.1 sigue sin decidir. Declarar qué se comprobó funciona bajo cualquiera de las dos respuestas, y además es comparable | Ninguno: el campo es más honesto que la taxonomía |
| `url_acceso[]` (varias) | **Colapsado** en `fuente_identidad` + `fuente_vigencia` | Tres URLs por registro son copia que no cambia ninguna decisión | — |

**Campos que no estaban en la tabla del refinado y sí entran:** `materia[]`, `fuente_vigencia` (el refinado pedía quién comprobó, pero no contra qué) y `alcance_comprobado`.

---

## §4 — La ficha de una providencia: 9 campos

**La unidad no es la providencia: es el par providencia + proposición.** La misma sentencia puede sostener una afirmación y no sostener otra; el propio catálogo ya tiene una registrada como control negativo. Una providencia usada para dos cosas son dos fichas.

La identidad ya está bien capturada en las 4 fichas actuales (corporación, sala, expediente, fecha, ponente) y **no se rehace**: se copia. Lo que falta es el pasaje, la regla atribuida y la constancia de la búsqueda adversa — que `07-jurisprudence-governance.md` declara obligatoria y que las cuatro fichas dejaron en `POR_VERIFICAR`.

**Una providencia no entra por la tabla de las normas.** No tiene `estado_vigencia`, ni `vigencia_desde`, ni `alcance_comprobado`, y recorrer una tabla escrita para normas con una ficha que no tiene sus campos daba `CITABLE` por omisión. Tiene su propia rama en `02` §2.B.

| # | Campo | Valores | Quién | Qué fallo evita |
|---|---|---|---|---|
| 1 | `identificador` | el del catálogo (`J-XX-0000-0000`) + enlace oficial | C | — |
| 2 | `estado_identidad` | `IDENTIDAD_VERIFICADA` \| `IDENTIDAD_POR_VERIFICAR` \| `CONFLICTO_DE_FUENTES` | C+V | La providencia inexistente con radicado, sala y ponente plausibles. **Mismo vocabulario que las normas**: cuando había dos idiomas, lo único que atrapaba a las providencias era el desajuste de cadena, y normalizar la etiqueta abría la vía |
| 3 | `proposicion_atribuida` | la frase exacta que se pretende sostener. **Nunca un resumen** | V | «La Corte dijo que…» sobre una providencia que decidió otra cosa. Si lo que se pide no es esta frase, la respuesta es `FUERA_DEL_ALCANCE_COMPROBADO` |
| 4 | `pasaje` | párrafo / numeral / página del texto que la sostiene | V | Sustituir el pasaje por el título o el resumen del buscador |
| 5 | `estado_uso` | `PROFESSIONALLY_CONFIRMED` \| `RELEVANCE_REVIEWED` \| `CONFLICTING` \| `SUPERSEDED_OR_LIMITED` \| `JURISPRUDENCIA_POR_VERIFICAR` (`07`) | V | Citar un precedente superado. Es el mecanismo entero contra eso, y **ahora está conectado**: los dos últimos valores y cualquier valor no reconocido nunca son citables |
| 6 | `busqueda_adversa` | constancia en una línea —**dónde, con qué criterio, qué día y qué salió**— o `JURISPRUDENCE_GAP` | V | Presentar como exhaustivo lo que fue un solo resultado. Vacía o `JURISPRUDENCE_GAP` **nunca es citable** |
| 7 | `verificado_por` | nombre completo | V | — |
| 8 | `verificado_el` | `AAAA-MM-DD` | V | — |
| 9 | `acortamiento_manual` | `AAAA-MM-DD`, opcional, solo para acortar | V | Igual que el campo 12 de la norma: la caducidad se calcula, no se declara |

Ejemplo de `busqueda_adversa` con datos inventados: `"buscada AAAA-MM-DD en <relatoría oficial>, criterio «<tema>», años 0000-0000; apareció una decisión posterior en sentido contrario, SENTENCIA-X-000-0000 — por eso estado_uso = CONFLICTING"`. Y su forma honesta cuando no se cerró: `JURISPRUDENCE_GAP — buscada AAAA-MM-DD; la cobertura del portal no alcanza el periodo`.

---

## §5 — El procedimiento, paso a paso

### Las cinco reglas que no se negocian

1. **El modelo no llena ninguna casilla de ninguna ficha, ni siquiera una que «ya sabe».** Puede abrir un buscador, transcribir una URL que ella dicte o formatear la tabla. En el momento en que produce un valor, este instrumento deja de existir: el pack pasaría a certificar exactamente aquello que estaba puesto para vigilar. Esto alcanza también a los valores de la **consulta** (`02` §1 R3): la fecha del caso y su tipo salen de la carpeta, no del modelo.
2. **Ninguna casilla se queda vacía.** Y ya no hace falta confiar en que así sea: vacío y valor no reconocido caen en el estado inseguro, no en `CITABLE`. `VIGENCIA_NO_COMPROBADA` y `JURISPRUDENCE_GAP` son respuestas correctas y frecuentes.
3. **No se copia una afirmación de otro archivo del corpus a una ficha.** Que un archivo del proyecto diga algo no es una comprobación; moverlo de sitio tampoco (`04` §7). Por eso `fuente_vigencia` no puede apuntar a un archivo de este corpus.
4. **La ausencia de aviso en un compilador no es una comprobación de vigencia.** Los propios portales institucionales advierten que no certifican vigencia por sí solos (`source-catalog/normative-sources.md`:9 — es una referencia, no una afirmación de este archivo).
5. **Si se acaba el tiempo, se firma lo comprobado y se para.** Media ficha firmada vale; una ficha entera completada de memoria destruye el pack, y no se nota hasta el caso real.

### P0 — Una sola vez, antes de empezar (≈2,5 h, y exige al dueño y a la verificadora **juntos**)

**P0.a — decidir (≈1 h).** La cadencia por defecto de `revisar_antes_de` (`02` §6) y, cuando las dos cosas sean posibles, si se comprueba a nivel de norma completa o de artículo (§8.1). Hacer **una ficha completa entre los dos** y cronometrarla: es la única forma de saber cuánto cuesta de verdad el resto. Que sean dos agendas y no una es una dependencia que no estaba en el presupuesto de horas y aquí queda dicha.

**P0.b — cuarentena del catálogo (≈30 min, y sin esto P3 no vale nada).** En `temporal-law-matrix.md` y `normative-sources.md`, cada fecha de vigencia se marca `VIGENCIA_NO_COMPROBADA — dato de catálogo, no comprobación`, o se borra la columna `effective_from / to`. Hoy esas fechas están pobladas en filas marcadas `VERIFIED_OFFICIAL`: la respuesta de P3 está escrita delante de ella con cara de comprobada, y la conducta previsible no es investigar, es copiar.

### P1 — Identidad (5-10 min)

Localizar el texto en fuente de publicación oficial. Orden de trabajo: `04` §2; los portales, en `source-catalog/colombia-official-sources.md`. Llenar 1, 3, 4, 5. Si dos fuentes oficiales discrepan → `CONFLICTO_DE_FUENTES`, las dos anotadas, no se elige.

### P2 — Alcance (2 min, y decide el coste de todo lo demás)

Escribir en `alcance_comprobado`, **con su estructura**, qué se va a comprobar. Estrechar es siempre legítimo y casi siempre más barato. El precio de estrechar es que la ficha solo responde dentro de lo estrechado: comprobar un artículo ya **no** sirve para una petición de norma completa, y esa es la corrección más importante de todo el instrumento.

### P3 — Desde cuándo (5-10 min)

Buscar la regla de entrada en vigor **para el alcance elegido**. Si es una fecha, va en `vigencia_desde`. Si la norma entra por partes y no se puede fijar la del alcance: `ESCALONADA`, la explicación en `nota_de_vigencia`, y `estado_vigencia = VIGENCIA_NO_COMPROBADA` salvo que se estreche el alcance hasta donde sí hay fecha.

### P4 — Hasta cuándo (10-15 min; es el paso caro y el que justifica todo)

Buscar activamente si algo posterior alcanza lo comprobado: derogatoria, sustitución, **reforma** o decisión de control. **La comprobación no es leer una etiqueta: es buscar y registrar qué se buscó.**
- Algo lo deroga o lo sustituye por entero → `SIN_VIGENCIA_DESDE AAAA-MM-DD`.
- Algo alcanza solo una parte del alcance → `VIGENCIA_PARCIAL_AL AAAA-MM-DD` + nota.
- **Hay reforma que cambia la redacción y la norma sigue rigiendo** → `VIGENTE_CON_REFORMA_AL AAAA-MM-DD` + nota. Es el caso más frecuente y antes no tenía casilla. **No cuesta un minuto más**: la búsqueda ya se hizo en este mismo paso; lo único que faltaba era dónde escribir el resultado.
- Se buscó lo cuatro y no apareció nada, **con al menos una fuente de clase `PRIMARY_OFFICIAL`** → `VIGENTE_AL AAAA-MM-DD` (la fecha de hoy).
- Se buscó y no se pudo cerrar, o solo hubo fuente consolidada, **o no se llegó a mirar la reforma** → `VIGENCIA_NO_COMPROBADA`, y en `fuente_vigencia` qué se consultó y por qué no basta.

### P5 — Firma (2 min)

`verificado_por`, `verificado_el`. `revisar_antes_de` **no se escribe**: lo calcula el contrato. Si la nota registra un cambio con fecha futura o un control pendiente, ella pone `acortamiento_manual`, que solo puede adelantar la revisión; una fecha posterior a la calculada se ignora.

### PJ — Providencias (45-75 min por par providencia+proposición)

**PJ1** copiar la identidad del catálogo y confirmarla (5 min). **PJ2** escribir `proposicion_atribuida` **antes** de leer, para no ajustar la frase al pasaje que aparezca (5 min). **PJ3** localizar el pasaje y decidir si de verdad la sostiene (15-25 min). **PJ4 búsqueda adversa**: autoridad contraria, limitante, posterior, de unificación y hechos distinguibles (20-40 min; domina el coste, y es el paso que hoy no se ha hecho nunca).

### El coste real, sin adornos

| | Por unidad | Total |
|---|---|---|
| Norma sencilla, alcance de artículo | 20-30 min | |
| Norma con entrada escalonada, reforma o control pendiente | 45-90 min | |
| **26 normas** | media ≈35 min | **13-18 h** |
| **Providencias**, por par providencia+proposición | 45-75 min | **3-5 h** |
| P0 (decisión, ficha cronometrada y cuarentena del catálogo) | | **+2,5 h** |
| | | **≈18-26 h de trabajo profesional** |

**La unidad de entrega es la ficha, no el pack.** 26 horas al ritmo de encargo secundario son once o doce sesiones de dos horas, y una regla dura que no puede cumplirse hasta la sesión doce no se cumple: se salta. Por eso:

> **`pack v0.1` = 5-8 registros ≈ 4 h ≈ dos sesiones.** Se publica con la `cobertura` declarando **solo lo que hay dentro** —todo lo demás nombrado en `materias_excluidas`— y con el `recuento` visible. Un pack que cubre poco y lo dice sirve; uno que promete un área y está vacío es el fallo del §0 otra vez.

El orden de las fichas lo fija un dato que el proyecto ya tiene y no está usando: **qué normas cita de verdad el trabajo real**, no cuáles están primero en el catálogo.

**La reverificación posterior es mucho más barata —10-15 min— porque solo se mueve la columna de vigencia**: la identidad no se pudre. Ese es el argumento económico para separar las dos columnas, además del argumento de veracidad.
