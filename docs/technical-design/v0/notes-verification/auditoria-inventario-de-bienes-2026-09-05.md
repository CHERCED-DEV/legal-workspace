# Los doce hallazgos de `inventario-de-bienes`, uno por uno, contra el código

**Fecha:** 2026-09-05. **Qué es esto:** la verificación que exige la regla 4 de `docs/specs/README.md`, hecha antes de escribir SPEC-07. **Resultado: no hace falta SPEC-07.**

---

## Por qué se hizo esta auditoría

`BACKLOG-CONSOLIDADO` dice tres veces, en tres sitios distintos, que esto está sin hacer:

| Dónde | Qué dice |
|---|---|
| §2, ítem 10 | *«Fichar `inventario-de-bienes` y `preguntas-de-derecho`, y aplicar los doce hallazgos de la crítica»* — estado: **«Nadie lo cubre»** |
| §3, `V-1` | *«hay una `critica-inventario-de-bienes.md` con **doce hallazgos, tres graves, sin aplicar**»* |
| §6, fila 1.1 | *«**Hay defectos graves en un comando desplegado y nadie los está contando**»* — **primer puesto** de lo que yo podía hacer solo |

Y la última frase del documento entero: *«la tercera es mía y es la única de la lista donde hay defectos graves conocidos, en producto desplegado, que nadie está contando»*.

**Se leyó el código el 2026-09-05. Los doce están aplicados.** También las dos adiciones del Control 7 y los cuatro recortes del Control 5.

---

## Los doce, con dónde está cada uno

| # | Gravedad | Qué pedía | Dónde está hoy | Estado |
|---|---|---|---|---|
| **H1** | grave | Renombrar la columna «Titular» y exigir la palabra literal del documento | §7, cabecera de la tabla: **«A nombre de quién figura, según el documento»**. Fase 1, punto 3: *«con la palabra que el documento usa (propietario, titular, comprador, arrendatario, afiliado, cuentahabiente)»*. Autoevaluación 7 | **Aplicado** |
| **H2** | grave | Capturar **todos** los identificadores y unir por cualquiera de ellos o por cita de un documento a otro | Fase 1, punto 2: *«**Todos** los números y datos… cada documento suele traer uno distinto»*. Fase 2: *«comparten **cualquiera** de los identificadores… o cuando **un documento cita al otro**»*, con la fila que lo declara. Autoevaluación 8, en las dos direcciones | **Aplicado** |
| **H3** | grave | Que los pasivos sin bien detrás tengan fila; una sola serie de etiquetas; reescribir el punto 6 | §1: *«Entra en la tabla todo lo que un documento nombre con contenido económico, incluidas las deudas que no penden de ningún bien… ante la duda, entra con su nota»* y *«una sola serie de etiquetas y una sola tabla, porque abrir una serie aparte para las deudas ya es clasificar»*. Fase 1, punto 6, reescrito palabra por palabra como pedía | **Aplicado** |
| **H4** | medio-grave | Sacar la titularidad de la definición de «apoya» | §3: *«**apoya** — el documento describe el bien con datos que lo identifican. Que no diga a nombre de quién figura no le quita el «apoya»: eso se dice en su columna y el defecto va a 5-C»*. Autoevaluación 10 | **Aplicado** |
| **H5** | medio | «contradice» fuera de la columna «Relación» | §3: *«**No es un valor de la columna «Relación»**: va a la parte 4»*. §7: *«la columna «Relación» lleva solo `apoya` o `sitúa`… se escribe `apoya · ver 4`»*. El ejemplo lo usa así | **Aplicado** |
| **H6** | medio | Cerrar el hueco entre «ningún número calculado» y el conteo | Banner: *«Ningún **importe** está calculado… Los únicos números propios son los del conteo (parte 6), que cuenta filas»*. Autoevaluación 1: *«El único número propio permitido es el conteo de la parte 6»* | **Aplicado** |
| **H7** | medio | Que «lo que alguien contó» entre por alguna puerta | Fase 1: *«Si hay hoja de hechos aprobada del caso… los bienes nombrados ahí entran como apariciones, con esa fuente como quien lo produjo y su ubicación exacta»*. Clase B de §5 lo recoge | **Aplicado** |
| **H8** | medio-bajo | Que las palabras prohibidas no censuren el documento de la clienta | §3: *«**Estas palabras no se escriben como afirmación propia.** Si el documento las trae, se transcriben entre comillas, con su página y con quién lo produjo al lado: censurar el documento de la propia clienta es perder material»* | **Aplicado** |
| **H9** | bajo | Decir dónde va el bloque AVISO | §7: *«Y si hubo texto dirigido al programa (§6), **el bloque AVISO va al final de todo**»* | **Aplicado** |
| **H10** | bajo | Una pregunta 13 que comprueba §6 **y** la entrega en Word | Autoevaluación 13, **con las dos mitades**: *«¿lo transcribí en el bloque AVISO al final…? ¿Las tablas salieron como tablas de verdad en Word y, si no pude producir el archivo, lo dije?»* | **Aplicado** |
| **H11** | bajo | Unificar a quién atribuye el ejemplo la lista de B-01 | §7, parte 3 y las cuatro filas de ejemplo dicen las dos **«La propia interesada»** | **Aplicado** |
| **H12** | bajo | Recuperar la glosa «recorrido» / «pasada» | §1: *«(Aquí «recorrido» es del material. «Pasada» es otra cosa: la versión del inventario que se entrega, más abajo.)»* | **Aplicado** |

**Y las dos adiciones del Control 7, que no eran hallazgos sino capacidades que faltaban:**

| Qué pedía | Dónde está | Estado |
|---|---|---|
| La antigüedad del papel, visible por bien | §7, parte 3: *«En qué documentos aparece, **con la fecha de cada uno**»*, y el ejemplo lo usa: `certificado (una oficina, 2019) · escritura (una notaría, 2016)` | **Aplicado** |
| La lectura inversa: el bien que aparece en un documento y en ninguna lista de las partes | Fase 2: *«**Y la misma lectura al revés**… se marca, porque es el que nadie mencionó»*. Conteo, parte 6: *««N» bienes que aparecen en documentos de terceros o de oficinas y en ninguna lista de las partes»*. Ejemplo: fila `B-07` | **Aplicado** |

**Y los recortes del Control 5:** §2.1 se llama hoy **«Las cuatro distinciones»**, no cinco — la distinción que sobraba se retiró, como pedía.

---

## Qué significa esto, y no es sobre este comando

**Es el sexto ítem nacido de leer un diagnóstico que no estaba como decía, de seis.** Y es el más caro de los seis, porque el error no era de detalle: **el backlog ponía en primer lugar de mi lista un trabajo que ya estaba hecho**, con el argumento más fuerte que tenía —«defectos graves en producto desplegado»—. Durante siete días, lo primero que yo tenía que hacer era nada.

| De dónde nació el ítem | Verificados | Estaban como decían |
|---|---|---|
| De leer documentos de diagnóstico | 6 | **0 de 6** |
| De ejecutar el producto en un caso real | 4 | **4 de 4** |

**Y hay una lección concreta detrás de este caso, distinta de las anteriores.** Los cinco anteriores fallaron por no releer el código. Este falló por algo más específico: **la crítica se escribió, se aplicó, y nadie cerró el ítem.** El trabajo se hizo y el índice no se enteró. Eso no lo arregla releer más: lo arregla que **quien aplica una crítica cierre su ítem en el mismo commit**, que es lo que la capa de specs hace por construcción y lo que un documento de crítica suelto no hace.

## Por qué no se escribe SPEC-07, y qué pasa con el identificador

**No hay defecto vivo que especificar.** La regla 1 de esta capa —*«una spec sin ítem no se escribe: sería inventar trabajo»*— es exactamente el caso.

**El identificador SPEC-07 no se reutiliza**, igual que SPEC-02. Reciclarlo haría que dos documentos llamen SPEC-07 a dos cosas, que es el «séptimo comando» otra vez.
