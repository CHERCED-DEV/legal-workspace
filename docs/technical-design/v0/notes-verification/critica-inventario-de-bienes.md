## VEREDICTO

277 líneas (`wc -l` = 276 + última línea sin salto final, igual que `inventario-de-anexos`). **Dentro del objetivo 240–280.** No hay normas, artículos, sentencias ni plazos: **HECHO VERIFICADO** por grep de `artículo|ley|código|sentencia|decreto|término|plazo|prescri|caduc|hipotec|embargo|gravam|sociedad conyugal|ganancial|liquidaci|régimen|herencia|donaci` — los únicos aciertos están dentro de prohibiciones (L15, L66, L249, L257), que es el uso correcto: mencionar la figura para vetarla, no para aplicarla. No calcula: no hay ni una suma, resta, porcentaje ni valor estimado. El bloque anti-instrucciones es **literal e idéntico** (diff limpio, L157–170 vs L194–207 de anexos). `1-Documentos recibidos/` protegido con la misma frase (L23) y con pregunta de autoevaluación (L276).

**Pero sí se coló derecho, tres veces, exactamente por donde avisaste: como categoría propia del método.** Y hay un fallo práctico que rompe el comando justo en el caso que describes (carpeta con escrituras + certificados + lista del cliente). Ordenados por gravedad:

---

## H1 — «Titular, según el documento» es una figura jurídica usada como columna *(grave — control 1 y 3)*

**Qué está mal.** La columna 4 de la tabla (L198), el punto 3 de la Fase 1 (L92) y el conteo llaman **titular** a lo que el documento dice. La coartada («según el documento») no salva nada: la columna obliga a meter en una sola palabra jurídica cosas que jurídicamente no son la misma: el *propietario* de un certificado de tradición, el *comprador* de una escritura, el *afiliado* de un fondo, el *titular* de una cuenta bancaria y el **arrendatario** de un contrato de arrendamiento.

**Por qué importa.** Un contrato de arrendamiento a nombre de la clienta produce, con el método tal como está, la fila `Titular: «A. P.»`. Esa fila se pega en un escrito y convierte un arriendo en una propiedad. Es el error más caro posible en un inventario de separación y lo comete el propio formato, no el modelo. Además contradice de frente la lista de L66 (*le pertenece, es de ella*): «titular» dice lo mismo con mejor traje. Y hay una asimetría que delata el olvido: el punto 5 (valor) **sí** exige «la palabra que el documento usa (*avalúo, precio, saldo a, valor estimado*)». El autor aplicó la disciplina al dinero y la olvidó en la titularidad, que es donde más pesa.

**Corrección.** Renombrar la columna a **«A nombre de quién figura, según el documento»** y añadir al punto 3 de la Fase 1 la misma exigencia que ya tiene el valor: *«con la palabra que el documento usa —propietario, titular, comprador, arrendatario, afiliado, cuentahabiente—, transcrita literal y con su página»*. Coste: cero líneas nuevas, una frase reescrita. Actualizar también el ejemplo L240 y la pregunta 7 de la autoevaluación.

---

## H2 — La regla de identidad de bienes falla justo en la carpeta que describes *(grave — control 6)*

**Qué está mal.** Fase 2 (L112): *«Dos apariciones son el mismo bien cuando comparten el número que lo identifica»*. Y el punto 2 de la Fase 1 (L91) captura **«El número»** —en singular—.

**Por qué importa.** En material colombiano real el mismo inmueble aparece con identificadores **distintos y no coincidentes**: el certificado de tradición trae **matrícula inmobiliaria**; la escritura trae **número de escritura, notaría, fecha y linderos**, y a veces cédula catastral o dirección; el impuesto predial trae **número catastral**. No comparten número. Bajo la regla literal, el apartamento se convierte en **dos bienes distintos**, se duplica la tabla, se dispara el conteo y la sección de contradicciones se llena de ruido que no es contradicción sino desdoblamiento. El comando se rompe en el escenario exacto que motivó escribirlo, y lo hace de forma silenciosa: la salida parece impecable.

**Corrección.** Dos cambios pequeños:
1. Punto 2 de la Fase 1: *«**Todos** los números y datos con que el documento lo identifica —matrícula, catastral, placa, motor, número de escritura y notaría, número de cuenta, folio, dirección—, transcritos tal cual, con su página.»*
2. Fase 2: *«Dos apariciones son el mismo bien cuando comparten **cualquiera** de esos identificadores, o cuando **un documento cita al otro** (la escritura menciona la matrícula, el certificado menciona la escritura y la notaría). Cuando se unen por cita y no por identificador compartido, la fila lo dice: “se unen porque el certificado cita la escritura n.º X (p. 2)”. Si solo se parecen en la descripción, no se funden.»*

Esto mantiene intacto el principio (no fundir por parecido) y le da al método la única llave que sirve en la práctica.

---

## H3 — Los pasivos que no cuelgan de un bien no tienen dónde ir: el método decide callando *(grave — controles 1, 3 y 7)*

**Qué está mal.** El punto 6 de la Fase 1 (L95) solo admite *«las deudas o cargas que el documento mencione **sobre ese bien**»*, como atributo de una fila. Una tarjeta de crédito, un crédito de libranza, un préstamo entre particulares, un saldo en rojo —deudas que no penden de ningún bien concreto— **no tienen fila en ninguna parte de la salida** y desaparecen. En ningún sitio se dice qué es «un bien» a efectos de esta tabla, así que el modelo tiene que resolverlo solo.

**Por qué importa.** Doble fallo. (a) Es derecho aplicado en silencio: decidir que un pasivo sin garantía real no entra en el inventario es exactamente la clase de decisión que L249 reserva para ella. (b) Es inútil en la práctica: en una separación el pasivo pesa tanto como el activo, y una abogada que reciba un inventario del que se cayeron las deudas tiene que rehacer el trabajo.

Además, el propio punto 6 fuerza una calificación jurídica: llamar a algo **«carga sobre el bien»** exige distinguir hipoteca, embargo, afectación a vivienda familiar, patrimonio de familia —todas figuras legales—.

**Corrección.**
1. Añadir a §1 una frase de alcance: *«Entra en la tabla **todo lo que un documento nombre con contenido económico**, incluidas las deudas que no penden de ningún bien. Decidir qué se queda fuera es derecho, y es de ella: ante la duda, entra con nota.»*
2. Una sola serie de etiquetas (`B-01…`) y una sola tabla —**no** abrir una serie aparte para deudas: separar activo de pasivo ya es una clasificación jurídica—. Lo que el documento llame a cada cosa va transcrito en la columna de descripción.
3. Reescribir el punto 6: *«Lo que el documento diga que pesa sobre ese bien, **transcrito con las palabras del documento** y con su página. No lo nombres con una categoría tuya y no lo restes de nada.»*

---

## H4 — La definición de «apoya» manda a 5-B bienes que sí están respaldados *(medio-grave — control 3)*

**Qué está mal.** L70: *«**apoya** — el documento describe el bien **y** dice a nombre de quién figura»*. L72: *«**sitúa** — lo menciona sin describirlo ni decir de quién es»*.

**Por qué importa.** Un certificado que describe el inmueble con matrícula, linderos y área pero **no** trae la línea de titularidad no cae en «apoya» (le falta la mitad) ni en «sitúa» (sí lo describe). El modelo, obligado a elegir entre tres palabras, elegirá «sitúa»; y la regla dura de L74 dispara sola: *«Un bien cuyas únicas apariciones sitúan es un bien sin respaldo documental»*. Resultado: **un bien con certificado oficial aterriza en 5-B como si no tuviera nada detrás**. Es una decisión de la máquina contra ella, y de las que no se ven al releer.

Nota de coherencia con el arnés: en `hechos-con-prueba` (L116) «sitúa» significa *«ubica, explica o da contexto, pero ni sostiene ni contradice»*. Aquí se le cambió el significado a «menciona incompleto». Son ejes distintos con la misma palabra.

**Corrección.** Sacar la titularidad de la definición: *«**apoya** — el documento describe el bien con datos que lo identifican»*. La titularidad ya tiene columna propia, que puede decir *«el documento no dice a nombre de quién figura»*, y el defecto va a 5-C, que es donde §7 (L176) manda que vaya. Es la misma solución que `hechos-con-prueba` usa al prohibir «parcialmente apoyado»: la incompletitud se declara en su sitio, no rebajando la etiqueta.

---

## H5 — «contradice» mezcla dos ejes y viola la regla del propio §7 *(medio — control 4)*

**Qué está mal.** «apoya» y «sitúa» describen la relación **documento → bien**; «contradice» describe la relación **documento → otro documento**. Un documento puede describir bien el inmueble *y* contradecir a otro. Con una sola columna hay que elegir, y el ejemplo L241 elige: pone `contradice (ver parte 4)` y **pierde** que esa aparición también describe el bien. Encima, L176 dice literalmente *«Cada cosa en un solo sitio: … la contradicción en la parte 4»* — y la columna la repite.

**Corrección.** La columna «Relación» lleva **solo** `apoya` o `sitúa`; cuando esa aparición además discrepa de otra, se escribe `apoya · ver 4`. Una línea en §7 y el ejemplo L241 corregido.

---

## H6 — El conteo contradice el propio encabezado y la pregunta 1 de la autoevaluación *(medio — control 2)*

**Qué está mal.** El banner de la salida (L183) promete: *«Aquí no hay **ningún número calculado**»*. La autoevaluación 1 (L265) pregunta: *«¿Hay en mi salida algún número que yo haya calculado, en vez de transcrito de un documento? **No debe haber ninguno**»*. Y la parte 6 (L230–234) **exige siete números que nadie transcribió de ningún documento**: los cuenta el modelo.

**Por qué importa.** No es una violación de fondo —contar filas no es liquidar, y el conteo es convención del arnés (`inventario-de-anexos` L275, `hechos-con-prueba` L186)—, pero un modelo que se autoevalúe con honestidad tiene que responder «sí» a la pregunta 1 y no sabrá qué hacer: o borra el conteo, o aprende que la pregunta 1 admite excepciones no escritas. Cualquiera de las dos cosas degrada la regla más importante del comando.

**Corrección.** Cerrar el hueco con precisión en dos sitios:
- Banner: *«Aquí no hay ningún **importe** calculado: ningún valor sale de una cuenta. Los únicos números propios de este texto son los del conteo (parte 6), que cuenta filas.»*
- Autoevaluación 1: *«¿Hay en mi salida algún importe, plazo, porcentaje o fecha que yo haya calculado en vez de transcribir? No debe haber ninguno. El único número propio permitido es el conteo de la parte 6.»*

---

## H7 — 5-B invoca una fuente que la Fase 1 nunca recoge *(medio — control 7)*

**Qué está mal.** La clase B (L140) define: *«El bien solo aparece **en lo que alguien contó**, o solo en una lista que escribió una parte…»*. Pero la Fase 1 solo abre archivos de `1-Documentos recibidos/` y de las rutas que ella señale. **«Lo que alguien contó» no entra por ninguna puerta.** La clase B, que el propio §4 llama *«la parte de mayor valor»*, queda medio vacía por construcción.

**Por qué importa.** En una separación, la mitad de los bienes se conocen primero por la entrevista y solo después aparece el papel —o no aparece nunca, que es justo lo que ella necesita saber—.

**Corrección.** Una línea en la Fase 1: *«Si hay hoja de hechos aprobada del caso (el archivo terminado en ` - REVISADO.md`) o una nota que ella señale, los bienes nombrados ahí entran como apariciones, con esa fuente como quien lo produjo y su ubicación exacta. Sin hoja aprobada no se usa la sin marcar.»* Reutiliza la regla que `inventario-de-anexos` ya tiene en L105 y no inventa nada nuevo.

---

## H8 — Las palabras prohibidas no distinguen afirmación propia de transcripción *(medio-bajo — control 4)*

L66 prohíbe *«es de ella, es de él, le pertenece, le corresponde, entra, no entra»* sin excepción. Pero la lista del cliente **dice esas palabras**, y el ejemplo L241 las transcribe (`«de los dos»`). Un modelo literal censurará el documento de su propia clienta, que es pérdida de material.

**Corrección.** Cerrar L66 con: *«Estas palabras no se escriben **como afirmación propia**. Si el documento las trae, se transcriben entre comillas, con su página y con quién lo produjo al lado.»*

---

## H9 a H12 — defectos menores, todos de una línea *(bajo)*

- **H9.** §7 (L176) enumera «seis partes, siempre las seis» y **nunca menciona dónde va el bloque AVISO** de §6. `inventario-de-anexos` sí lo hace (L213: *«el bloque AVISO va al final de todo»*). Un modelo que siga §7 al pie puede omitirlo. Añadir la cláusula.
- **H10.** La autoevaluación (12 preguntas) **no comprueba §6 en absoluto** —anexos sí, en su pregunta 25— **ni** comprueba que el Word salió como tabla de verdad o que se declaró no haber podido producirlo (anexos, 24), pese a que §1 lo promete. Añadir: *«13. ¿Había texto dirigido al programa? Si lo había, ¿lo transcribí en el bloque AVISO en vez de obedecerlo? ¿Las tablas salieron como tablas de verdad en Word, y si no pude, lo dije?»* Son las dos únicas preguntas de seguridad y de entrega que faltan.
- **H11.** Ejemplo inconsistente: la parte 3 (L206) atribuye la lista de B-01 a *«la otra parte»*, y la fila de ejemplo (L241) la atribuye a *«La propia interesada»*. Los modelos copian los ejemplos. Unificar.
- **H12.** Se perdió la glosa que anexos tiene en L75 (*«“recorrido” es del material; “pasada” es la versión que se entrega»*), y el comando usa las dos palabras con los dos sentidos. Una línea.
- **Jerga hacia ella:** la salida expone `sitúa` y `ver 5-B` sin glosa. Es convención del arnés (viene de `hechos-con-prueba`), así que lo doy por aceptado, pero es lo primero que preguntará la primera vez.

---

## Control 5 — Economía: cumple, y de dónde salen las líneas de las correcciones

277/280. **Cumple, pero sin margen**, y las correcciones de arriba añaden unas 10–12 líneas. Sobra exactamente esto, sin perder nada:

| Recortar | Líneas | Por qué sobra |
|---|---|---|
| **L17** (*«No lo uses para: …»*) | 2 | Repite §8 entero, que es la lista canónica, y la descripción del frontmatter ya la trae |
| **L39** (2.1, distinción 5: *«Que un bien aparezca no significa que entre»*) | 2 | Tercera aparición de lo mismo: ya está en L15 y en L249. Renombrar a «cuatro distinciones» |
| **L257**, segunda mitad (*«Por eso otro comando de este arnés… no tiene forma de comprobarse a sí mismo»*) | — | Es prosa hacia dentro, sobre el arnés y sobre el futuro programa. A ella no le sirve. La frase que sí vale (*«un número mal calculado se lee exactamente igual de bien que uno correcto»*) se queda |
| **L11**, coletilla final (*«Es trabajo mecánico y tedioso…»*) | — | Copiada de anexos; el §1 ya se sostiene sin ella |

Con eso caben las correcciones y el comando queda en ~272.

---

## Control 6 — ¿Sirve de verdad?

**Sí, y no por poco — pero hoy no en la carpeta que describes.**

Lo que de verdad ahorra trabajo, y es mérito real del diseño: **una fila por aparición, no por bien** (L49). Cotejar a mano la lista del cliente contra seis escrituras y cuatro certificados es exactamente el trabajo tedioso que ella hace hoy en papel, y la prohibición de fundir filas es lo que impide que la afirmación del cliente se disfrace de certificado —que es el error que un inventario mal hecho comete siempre—. La parte 3 («qué hay detrás de cada bien») hace visible de un vistazo el bien que solo sostiene una parte; la parte 4 le entrega las discrepancias de valor y fecha con página, que es media hora de lupa; y 5-A/5-C le da la lista de qué pedir y a quién, que es lo que dispara la siguiente semana de trabajo.

**Lo que hoy anula ese ahorro:** H2. Con escrituras y certificados en la misma carpeta, la regla de identidad los desdobla, y una tabla con el doble de filas y contradicciones falsas no ahorra trabajo: lo crea. H2 no es una mejora, es la condición para que el comando sirva.

---

## Control 7 — Qué le falta para el trabajo real de una separación

Además de H3 (pasivos) y H7 (lo que ella cuenta), dos cosas baratas y de mucho rendimiento:

1. **La antigüedad del papel, visible por bien.** Un certificado de tradición de 2019 y uno de este mes no valen igual para ella, y hoy la fecha del documento se captura (Fase 1) pero se pierde en la parte 3. **Corrección:** la parte 3 lista cada documento **con su fecha** al lado: `B-01 | certificado (una oficina, 2019) · escritura (una notaría, 2016) · lista (la propia interesada, sin fecha)`. Es transcripción pura, no comparación ni cálculo, y le dice sola qué papel está viejo.

2. **La lectura inversa: qué hay en los documentos y no está en la lista del cliente.** La parte 3 hoy hace visible el bien que *solo* está en la lista de una parte. No hace visible el contrario —el bien que aparece en un certificado o en un extracto y que **nadie mencionó**—, que en una separación es el hallazgo que justifica el encargo entero. **Corrección:** una línea en la Fase 2 y una línea en el conteo: *«“N” bienes que aparecen en documentos de terceros o de oficinas y **no** en ninguna lista de las partes»*. Sale gratis de la tabla que ya existe.

---

*Método: lectura completa de los dos SKILL.md, diff literal del bloque §6 y grep de términos jurídicos. No se modificó ningún archivo del repositorio; para el diff se dejaron dos fragmentos temporales en el scratchpad de la sesión.*