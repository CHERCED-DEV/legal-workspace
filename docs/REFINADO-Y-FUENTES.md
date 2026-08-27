# REFINADO Y FUENTES — arnés Despacho

**Fecha: 2026-08-27. Documento de decisión.** Está filtrado por la refutación: lo que el refutador tumbó no aparece como propuesta, aparece en §6 con el motivo. Lo dudoso entra marcado y con lo que habría que comprobar antes.

**Etiquetas.** `HECHO MEDIDO` = hay un número de una corrida o de un instrumento. `VERIFICADO` = comprobado hoy contra el archivo, con la orden a la vista. `SUPUESTO` = razonamiento, no comprobación. `POR VERIFICAR` = hay que comprobarlo antes de decidir. `RIESGO` = fallo que puede ocurrir y hoy nada detecta. `DECISIÓN PENDIENTE` = solo la toma el dueño, y está en §8.

---

## §0 — El refinado en diez líneas

1. **Lo que está bien** (y aquí se acaba el elogio): el interior de las salidas —cita literal con página, propuesta y conteo, ausencias formuladas sobre la carpeta y no sobre el mundo— y la cadena de aprobación por nombre de archivo, que se vio funcionar y detenerse. No se toca nada de eso.
2. **El fallo más caro no está en las fuentes jurídicas.** Seis de los siete comandos ordenan declarar ilegible un escaneado sin capa de texto y uno lo lee. En el caso real son 25 de 39 páginas y la pieza central del asunto. `HECHO MEDIDO`
3. **La pregunta dura, contestada: hoy nada lo impide.** Lo impide la abstinencia. Cero derecho sustantivo en las siete skills `VERIFICADO hoy`; `repealed_at` definido una vez y usado cero veces `VERIFICADO hoy`. La abstinencia se acaba el día que exista el Knowledge Pack.
4. **Por eso este ciclo NO construye el Knowledge Pack.** Sus 55 campos suponen un curador que no existe: la palabra «curador» no aparece en el corpus `VERIFICADO hoy`. Sobreviven dos campos y una frase.
5. **El banco no puede fallar.** `medir.py` termina siempre con código 0 y certifica «VERACIDAD ── intacta» sobre un run vacío `HECHO MEDIDO por ejecución`. Hoy, «pasó el banco» no significa nada.
6. **La única propiedad demostrada del producto no la produce el instrumento.** Los 647 fragmentos citados y el «1 error en 239 anclajes» los produjo una persona leyendo; `medir.py` cuenta 555 citas y no abre ni una fuente.
7. **El −34 % con el que se adoptó `inventario-de-anexos` v0.2.0 no es distinguible del ruido** (n=1, efecto mínimo detectable 52-67 %). El +177 % de caché escrita por +31 % de método sí sobrevive a ese suelo, y es la razón de todo lo que sigue.
8. **El refinado completo añade ~575 líneas sobre 2.152: +27 % de método** `VERIFICADO hoy el denominador`. No se aplica entero: se aplica por tramos, con una medición de coste entre el tramo 3 y el 4.
9. **Lo que decide el dueño** (§8): si el trabajo derivado es fuente —bloquea la mitad de lo que queda—, si existe una abogada que verifique vigencia con nombre, si el audio se puede leer, y DP-1.
10. **El orden (§7) empieza por lo que cuesta cero líneas de método**: cuatro pruebas de banco que sí pueden fallar, una de ellas «ninguna entrega contiene una cita jurídica».

---

## §1 — LAS FUENTES

### 1.a — Fuentes jurídicas

#### La pregunta dura: ¿qué impide hoy que el sistema cite una norma que ya no rige?

**Nada. Lo impide que el producto no cita normas.** `grep -rE "Ley [0-9]|Decreto [0-9]|art\. [0-9]|C-[0-9]{3}/|T-[0-9]{3}/"` sobre `plugins/despacho/` devuelve cero coincidencias `VERIFICADO hoy`. La garantía es una abstinencia, no un mecanismo, y la abstinencia se acaba el día que exista el Knowledge Pack.

No hay ningún mecanismo detrás porque no hay ningún campo donde escribirlo:

| Lo que haría falta | Lo que hay | Fuente |
|---|---|---|
| Un campo de derogación | `repealed_at` se define una vez y se usa cero veces en todo el repositorio | `docs/skills-support/05-temporal-applicability.md:13` `VERIFICADO hoy` |
| Una fecha de pérdida de vigencia | `effective_to` dice «desconocido» en las 7 filas que llevan fecha y es prosa en las otras 5 (100 % de la matriz) | `source-catalog/temporal-law-matrix.md:8-19` |
| Un estado que distinga identidad de vigencia | `VERIFIED_OFFICIAL` en la misma fila donde la vigencia está en blanco. Ya se leyó una vez como «vigente» dentro del propio corpus | `04-source-governance.md:43`; el error, en `ESTADO-DEL-PROYECTO.md` §3 fila 3 |
| Alguien que responda por la comprobación | `curator` es obligatorio en el manifiesto del pack y «curador» no aparece en ninguno de los 89 archivos del corpus | `docs/architecture/boundaries.md:186` frente a `docs/skills-support/` `VERIFICADO hoy` |
| Texto que citar | Cero líneas de artículo transcritas. Y ya hay afirmaciones sobre lo que dicen artículos que nadie puede comprobar sin salir a internet | `temporal-law-matrix.md:16,19` |

**El fallo ya está dentro del material, no es hipotético.** `normative-sources.md:41` registra que el art. 331 de la Ley 2452 es derogatorio; `temporal-law-matrix.md:12-13` fecha esa vigencia el 2026-04-02 y coloca al Decreto Ley 2158 bajo esos artículos; la fila del 2158 sigue marcada `VERIFIED_OFFICIAL`, sin fecha de pérdida de vigencia. Hoy es 2026-08-27. Es el ensayo general del fallo, ya ocurrido, en la primera fila que un pack laboral tendría que servir. `RIESGO`

**El segundo filo, que ningún examinador vio y el refutador sí.** Tampoco está verificada la identidad. Sin `verificado_por`, las 4 providencias del catálogo están **afirmadas**, no comprobadas —con toda probabilidad por el mismo modelo que después las citaría—. El corpus podría contener hoy una providencia inexistente con radicado, sala y ponente plausibles, y nadie lo sabría. Eso es la cita fantasma en el sitio donde más duele, y no lo detecta nada. `RIESGO`

#### Los cuatro canales por los que el derecho puede entrar al producto

Esta tabla es la respuesta operativa a la pregunta dura. Tres de los cuatro canales están abiertos hoy y dos son gratis de cerrar.

| # | Canal | Estado hoy | Qué lo protege | Qué se hace en este ciclo |
|---|---|---|---|---|
| 1 | **El método** (las siete skills) | Cero derecho `VERIFICADO hoy` | La regla dura 1 y la abstinencia. Nada lo comprueba. | `cita_juridica[]` obligatoriamente vacío como prueba del banco que **falla**. §2 |
| 2 | **El documento ajeno** (toda demanda trae su apartado de normas) | Contradicción viva: `revisar-documento/SKILL.md:15` y su autoevaluación 9 lo prohíben en absoluto; `PLAN-DE-MEJORA.md:362` (DP-1) recomienda permitirlo transcrito; `GUIA-PARA-LA-ABOGADA.md:305` le enseña que ver una norma **es señal de que algo va mal** | Nada coherente | `DECISIÓN PENDIENTE` DP-1 (§8), y en el mismo cambio se corrige GUIA:305, que quedaría falsa el mismo día |
| 3 | **La pregunta directa de ella** («¿qué dice la ley sobre alimentos?») | No se activa ninguna skill: contesta el modelo desnudo, sin método, sin marcas, sin regla 1, sin fuente | **Nada** | Dos líneas: una en GUIA §5 y otra en README. Es la corrección de fuentes jurídicas con mejor relación de todo el refinado `RIESGO` |
| 4 | **El derecho que dice ella** («esto lo cubre el art. 24») | Entra como fuente admitida por `redactar-escrito/SKILL.md:26` con coordenada «lo dijo usted el «fecha»» | Nada: la regla 1 dice que el *método* no contiene derecho, no cubre este canal | La misma cláusula de DP-1, extendida al canal oral `RIESGO` |

**La cláusula que cierra los canales 2 y 4** es la mejor frase producida por el refinado y hay que escribirla igual en los siete comandos: *«el método no contiene derecho; la salida puede contener derecho ajeno, entrecomillado, con su página y marcado como transcripción de lo que el documento dice, **sin que eso afirme que esa norma existe, rige o dice lo que el documento le atribuye**»*. La última cláusula es la que faltaba en la formulación de DP-1.

#### Qué campos necesita una norma para que citarla sea seguro

Se responde entero, porque la pregunta es del encargo. Pero la columna de la derecha manda: en este ciclo se escriben **dos**.

| Campo | Qué fallo evita | ¿Entra ahora? |
|---|---|---|
| `identificador_canonico` (`LEY-1755-2015`) separado de `url_acceso[]` | Hoy la clave de hecho es la URL, y SUIN convive con tres formas de dirección dentro del propio catálogo | No — con el pack |
| `unidad` (ley / artículo / inciso / parágrafo) | Citar «la Ley 1755» cuando la regla está en un inciso; no saber si una derogación parcial alcanza lo citado | No — y antes hay que responder la `DECISIÓN PENDIENTE` de §8.1 |
| `texto_literal` + `locator` + `fecha_de_captura` | La cita fantasma sobre normas: hoy nadie puede comprobar «el art. 243 dice seis meses» sin salir del sistema | No — con el pack |
| `vigencia_desde` + `regla_de_entrada_en_vigor` + su pasaje | «Escalonada por art. 627» es prosa incomparable contra la fecha de un caso | No — con el pack |
| **`vigencia_hasta`** (fecha ISO \| `VIGENTE_AL <fecha>` \| `NO_COMPROBADO`) | **Es el campo que decide si la norma sigue rigiendo.** Hoy está vacío en el 100 % de las filas junto a un estado que dice VERIFIED | No — pero es el que convierte el problema en un fallo detectable. §8.2 |
| `derogada_por` + `derogada_desde` | El caso del Decreto Ley 2158, ya dentro del catálogo | No — con el pack. `alcance_derogacion` y `pasaje_derogatorio`: **rechazados**, §6 |
| `modificada_por[]` con fecha y artículo | Citar la redacción original de un artículo reformado sin que nada lo señale | No — con el pack |
| `estado_identidad` **separado de** `estado_vigencia` | «Comprobé que existe» leído como «comprobé que rige». Ya ocurrió y está documentado | No — pero renombrar `VERIFIED_OFFICIAL` a `IDENTIDAD_VERIFICADA` cuesta una sustitución y es media causa del error |
| `verificado_por` + `verificado_el` + `revisar_antes_de` | Sin nombre detrás, ningún registro pasa de afirmado a comprobado. Condiciona a todos los anteriores | No — porque **no hay quién**. §8.2 |
| `respuesta_cuando_no_hay_entrada` | El silencio se lee como ausencia de regla: el pack reproduciría dentro el error que el producto persigue fuera | **SÍ.** Cuesta cero por registro: es contrato, no dato |
| `cobertura_declarada` (qué áreas y fechas cubre y cuáles no) | «No encontrado ≠ no existe» dentro del único componente que el producto no puede inspeccionar | **SÍ.** Cuesta cero por registro |

**Providencias.** La identidad está bien capturada en las 4 fichas (corporación, sala, expediente, fecha, ponente) y no hay que rehacerla. Lo que falta —pasaje transcrito, regla atribuida, ratio/obiter declarado, salvamentos, `providencia_sin_efecto`, y la constancia de la búsqueda adversa— espera al pack. Dos datos para dimensionar: las 4 fichas tienen «Autoridad contraria o posterior» en `POR_VERIFICAR`, y 5 de los 7 estados definidos en `07-jurisprudence-governance.md` no se usan una sola vez fuera de su definición, incluido `SUPERSEDED_OR_LIMITED`, que es el mecanismo entero contra citar un precedente superado. `RIESGO`

#### Cómo se evita citar derogado

Hoy: no citando. Mañana, y es una sola regla: **sin `vigencia_hasta` comprobada por una persona con nombre, la norma no se sirve como citable.** Es la única formulación que convierte «norma derogada» en un fallo detectable en vez de en una salida fluida. Su coste es que el primer pack servirá muy poco; su alternativa es que sirva mucho y a veces mal. `DECISIÓN PENDIENTE` §8.2.

Mientras tanto, y esto sí se hace: **retirar afirmaciones, no rellenar campos.** Degradar la fila `N-DL2158` a `VIGENCIA_POR_VERIFICAR` no exige leer el art. 331 —retirar una afirmación no exige leer nada—. Rellenar `derogada_por` con «lo que el propio corpus ya afirma», como se propuso, sería copiar una afirmación de un sitio a otro y darla por comprobada: exactamente el lavado de conocimiento que prohíbe `04-source-governance.md:87-89`, la mejor regla del corpus. Va a §6.

#### Cómo caduca el material y quién lo mantiene

**Nadie lo mantiene y no caduca: se pudre en silencio.** La única fecha del catálogo es un sello global —2026-08-25— repetido a mano en las cabeceras de los cuatro archivos y en la columna `last_checked` de las 12 filas, con el mismo valor en todas, sin nombre y sin vencimiento. Y sin embargo `09-legal-completeness-audit.md:45-50` clasifica 5 de 6 grupos como `HIGH_MAINTENANCE`.

La bomba está armada y con fecha impresa: `temporal-law-matrix.md:19` registra un cambio de porcentaje «desde 2026-07-01» —que ya pasó— y otro «desde 2027-07-01» que volverá falsa esa fila sin que nadie la toque. Que el material tenga dos días es irrelevante: el defecto es estructural. `RIESGO`

La corrección conocida —`verificado_por`, `verificado_el`, `revisar_antes_de`, y una comprobación que **falle** cuando la fecha vence— no entra en este ciclo por una razón que no es de esfuerzo: no hay quién ocupe el primer campo. Un aviso que solo se lee no sirve; en el corpus hay ya tres avisos de obsolescencia y ninguno ha disparado nada.

---

### 1.b — Fuentes de verdad del caso

El arnés sí tiene reglas de precedencia y las tres que existen están bien escritas. Comparten una lógica que nadie ha nombrado y que es la llave para escribir las que faltan sin meter derecho: **no ordenan por peso probatorio —eso sería valorar— sino por cercanía al material.** Escríbase así, porque es lo que permite añadir reglas sin cruzar la regla 1.

#### Tabla de precedencias

| # | Cuando dicen distinto… | Qué manda | Dónde está escrito | Estado |
|---|---|---|---|---|
| 1 | La fecha del documento / la del nombre del archivo / la del sistema de archivos | La del documento. Si no hay, se ofrecen (b) o (c) **etiquetadas como lo que son**. Si (a) y (b) se contradicen, se entregan las dos y no se elige | `estado-del-caso/SKILL.md:73-85` | **EXISTE**, en 1 de los 5 comandos que tocan fechas de archivo. En `cronologia` falta la línea: una fecha que solo está en el nombre no cabe en ninguno de sus cinco grados |
| 2 | `0-Estado del caso (no editar).txt` / los documentos | Los documentos, y la diferencia se señala | `estado-del-caso/SKILL.md:169` | **EXISTE en 1 de 7.** `cronologia:189` lo manda leer «para el contexto» sin la regla; tres comandos no lo nombran nunca |
| 3 | Hoja de hechos sin marca / con ` - REVISADO` | Solo la marcada, «ni aunque esté completa y bien hecha» | `hechos:247-253`, `anexos:105`, `redactar:102-104` | **EXISTE y funciona.** Transcrita carácter a carácter en los tres sitios. Es el único acoplamiento entre comandos que hoy no falla |
| 4 | La decisión de ella ficha por ficha / el texto de la ficha original | `SÍ` entra; `A MEDIAS` entra **con su corrección**; `NO` no entra; **en blanco = no aprobada** | `redactar:26,29` | **FALTA en los dos inventarios**, que consumen el archivo revisado como bloque. Un hecho que ella rechazó reaparece como «afirmación sin ningún documento» |
| 5 | Trabajo derivado del sistema (cronología, inventarios, `0-Estado`) / material del caso | El material. El trabajo derivado dice **dónde mirar**, nunca de dónde sale un dato | `redactar §7:221-223`, y solo para el borrador | **FALTA como regla del producto.** `DECISIÓN PENDIENTE` §8.3 |
| 6 | Lo que ella dice en la conversación / un documento | **Al lado**: si discrepan es un conflicto y se entregan los dos, con sus dos etiquetas | No existe | **FALTA.** `DECISIÓN PENDIENTE` §8.4 — hoy el modelo elige solo, y lo más probable es que corrija en silencio |
| 7 | Una salida aprobada / material llegado después de ella | El material nuevo: el comando **se detiene y lo dice**, no redacta sobre una foto vencida | No existe. Diseñado en `ESTADO-DEL-PROYECTO.md:251` (iv), sin escribir en ningún SKILL | **FALTA.** Es el fallo silencioso más caro del oleoducto |
| 8 | Dos archivos ` - REVISADO.md` del mismo caso | **No se elige.** Se nombran los dos con su fecha y se pregunta cuál rige | No existe | **FALTA.** Las etiquetas `H-02` son estables entre pasadas, así que las dos versiones se leen igual de bien |
| 9 | Dos pasadas del mismo inventario con numeraciones distintas | No se elige; y antes: **no se renumera** entre pasadas, los anexos nuevos van al final | No existe | **FALTA.** Medido: el poder pasó del anexo 1 al 22 y el anexo 18 cambió de contenido conservando el número `HECHO MEDIDO` |
| 10 | `3-Para presentar/` | Se lee, nunca se escribe. Y estar ahí **no acredita** que se presentó: eso solo lo dice una constancia dentro del documento | `estado-del-caso:48`, `redactar:198` | **EXISTE en 2 de 7.** Un escrito con sello de recibido es hoy invisible para la cronología y los dos inventarios |
| 11 | Un escaneado sin capa de texto / «no se pudo leer» | Se abre por rangos de páginas y se lee como imagen | `inventario-de-bienes/SKILL.md:17` | **EXISTE en 1 de 7.** Es el hueco número uno del producto entero |

#### Lo que falta, y lo que cuesta cada pieza

- **Filas 2, 5, 10**: una línea idéntica por skill. Es lo más barato del refinado y cierra la ruta de lavado completa (una fecha «deducida» de la cronología reaparece tres semanas después como afirmación redactada, con «Cronología, p. 2» registrado como su origen).
- **Fila 4**: una frase en dos skills.
- **Filas 7 y 8**: no son un campo por fila, son **una rama de detención**. Cuestan un turno cada vez que se dispare, y solo se disparan cuando el daño ya está a punto de ocurrir.
- **Fila 9**: una línea. Documentar la inestabilidad de la numeración cuesta N filas por pasada; no fabricarla cuesta una frase. Ver §6.
- **Fila 6**: barata de escribir, pero antes hay que decidir si su palabra manda o va al lado.
- **Fila 11**: ~30 líneas repartidas en seis skills, y se aplica **sin medir**. No es una mejora de coste: es retirar una falsedad demostrada.

#### La decisión que gobierna la mitad de esta tabla

Dos examinadores se contradijeron de frente: uno propone que ninguna salida del sistema sea fuente jamás; otro propone que los inventarios **reutilicen la captura del hermano** «en vez de volver a abrirlo todo», y que la marca ` - REVISADO` se extienda a cronología e inventarios.

**No se pueden aplicar los dos, y la reutilización pierde por un motivo que no es doctrinal:** que los cuatro comandos coincidieran en las 25 páginas ilegibles fue una **medición independiente, no redundancia**. Siete lecturas del mismo material son el único control cruzado que el producto tiene hoy, y está justo en el eje —la veracidad— que es lo único demostrado. Reutilizar capturas lo destruye para ahorrar una pasada.

**Mi lectura: el producto es siete lecturas independientes, no un oleoducto.** La única excepción es la hoja de hechos con marca, porque ahí lo que se consume no es trabajo del sistema: es una decisión de ella. `DECISIÓN PENDIENTE` §8.3.

---

## §2 — Campos técnicos que hay que traer

Solo los que sobrevivieron al refutador. El criterio de corte no fue la utilidad: fue **dónde se paga**. Un campo que se paga una vez por salida entra; uno que se paga por fila tiene que ganárselo; uno que solo puede llenar alguien que no existe, no entra.

**Los cinco primeros son una sola cosa: tres líneas de cabecera en las siete salidas.** Se escriben juntas o no se escriben.

| # | Campo | Dónde vive | Qué fallo concreto evita | Coste | Estado |
|---|---|---|---|---|---|
| 1 | `Caso: <nombre literal de la carpeta>` | Cabecera x7 | El modelo inventó «2026-001 Custodia» y lo puso en cuatro salidas; la pasada 2 lo cambió por su cuenta a otro nombre. Dos salidas del mismo caso no se emparejan `HECHO MEDIDO` | Cero: copiar una cadena que ya está en la ruta | **SOSTENIDO** |
| 2 | `Hecho con: <comando> v<x.y.z> · pasada <n> · <AAAA-MM-DD HH:MM>` | Cabecera x7 | Seis de siete salidas no dicen qué las produjo. Las mtime de los ocho archivos del caso se colapsaron en `11:42:18` al copiar la carpeta, así que el disco no lo suple. `medir.py:339` recibe la versión por bandera con `default="sin-versión"` | Una línea por salida | **SOSTENIDO.** Y `plugin.json` a la versión que corresponda: hoy dice `0.1.0` con dos skills en `0.2.0` `VERIFICADO hoy` |
| 3 | `Cómo se leyó`: con texto / abierto como imagen (con los rangos) / no se pudo abrir (con el motivo) | Cabecera x7 | La afirmación falsa sobre 25 de 39 páginas, y que dos pasadas del mismo caso dejen de ser comparables | Dos líneas por salida, declaradas por rango y no cita por cita | **SOSTENIDO.** Se aplica **sin medir** |
| 4 | `Fecha de corte` + la lista del material leído | Cabecera x7 | Ella aprueba 40 fichas el lunes, llega un anexo el martes, y el borrador del miércoles se redacta sobre hechos aprobados sin ese anexo, sin una línea de aviso | Una línea; cuatro plantillas ya imprimen la lista | **SOSTENIDO.** Es la entrada de la rama de detención (§1.b, fila 7) |
| 5 | Marca de **transcripción a la vista** para las páginas leídas como imagen | Misma cabecera, junto al campo 3 | Una cita transcrita a ojo no se puede buscar con Ctrl+F y puede tener un dígito cambiado. El activo del inventario son discordancias del tipo «1.034.959.525 / 1.094.959.625»: una de ellas salida de una transcripción es indistinguible de una real | Una frase, por rango de páginas | **SOSTENIDO** |
| 6 | `Decisión de ella por ficha` leída por los dos inventarios | `inventario-de-anexos:103-107`, `inventario-de-bienes:79` | Un hecho que ella marcó `NO` reaparece en la parte 5-B como «afirmación sin ningún documento»: un hecho descartado presentado como hueco de prueba del caso | Una frase en dos skills | **SOSTENIDO.** Es el único acto de decisión de ella que existe en el producto, y dos de tres consumidores no lo leen |
| 7 | `Nivel de fuente`: material recibido (`1-`, `3-`) / lo que ella dijo / trabajo derivado (`2-`, `0-Estado`) | Lista «No son fuente» de `redactar §2.1:29`, más una línea en los otros seis | La ruta de lavado completa: una fecha marcada «deducida» reaparece como afirmación redactada en un escrito que ella firma, con la marca y el supuesto perdidos | Una línea por skill | **SOSTENIDO, condicionado a §8.3** |
| 8 | `cita_juridica[]`, obligatoriamente vacío en toda entrega | Banco | Hoy una entrega puede citar «Sentencia X-999 de 2031» y el banco certifica «VERACIDAD ── intacta». Protege la regla dura 1, que es el eje del encargo | ~20 líneas de código, **cero de método** | **SOSTENIDO. Lo mejor del refinado.** Detalle: la clase de letra ha de ser `[A-Z]{1,3}`, no `[CTSU]` — la sala inventada es la señal, no el ruido |
| 9 | `escrituras_prohibidas[]` | Banco, desde el rastro | Un comando escribe en `1-Documentos recibidos/` y nadie se entera hasta que ella pierda un original. Violación binaria, sin truth set y sin derecho | Una función corta, cero de método | **SOSTENIDO.** La prueba más barata que falta |
| 10 | `texto_de(path)` para `.docx` | Banco | Dos de los siete comandos son invisibles a toda métrica de contenido: el A/B completo reportó `fabricaciones: 0` sobre entregas que el instrumento nunca abrió | Seis líneas de biblioteca estándar | **SOSTENIDO** |
| 11 | `veredicto {estado, fallos[]}` + código de salida (`NO_MEDIDO` incluido) | Banco | El instrumento no tiene forma de decir FALLA, y dice «intacta» junto a «declaradas 0 de 25» | Bajo, cero de método | **SOSTENIDO** |
| 12 | `ejecuciones[] {valores, mediana, rango}` en lugar de una cifra | `casos/` y `resultados/` | Presentar n=1 como «el número». Todo lo publicado por debajo del 52 % se citó como hecho medido sin serlo | Bajo | **SOSTENIDO** |
| 13 | `respuesta_cuando_no_hay_entrada` (`NO_TENEMOS_INFORMACION_SUFICIENTE`, nunca el vacío) | Contrato del pack | El silencio se lee como ausencia de regla | Cero por registro | **SOSTENIDO** — uno de los dos supervivientes del pack |
| 14 | `cobertura_declarada` (qué cubre y qué no) | Manifiesto del pack | «No encontrado ≠ no existe» donde el producto no puede inspeccionar | Cero por registro | **SOSTENIDO** |
| 15 | `content_manifest[] {file, sha256, paginas}` | `casos/caso-01-familia.json` + `medir.py --material` | Dos corridas pueden haber leído PDF distintos y la diferencia se atribuye al método. Y sin `paginas` no se detecta la cita a la página 47 de un documento de 39 | Cero de método | `NO REFUTADO` — entra en la segunda tanda del banco. El nombre ya está elegido en `13-synthetic-benchmark.md` §11.3: usar ese |
| 16 | `imagenes` por agente (bloques `image` en los `tool_result`) | `metricas_de_agente()` | La contaminación de capacidad que ya invalidó una comparación se volvió a contar a mano (46/48). La lección quedó como advertencia en prosa, no como instrumento | Cero de método | `NO REFUTADO` — segunda tanda |
| 17 | `0-Datos del caso.txt`: a quién representa, en qué calidad, quién es la contraparte | Raíz del caso | La columna «Quién lo produjo» quedó sin poder llenarse en todo el inventario: «no se pudo establecer con este material» `HECHO MEDIDO` | 3 líneas una vez por caso, **pero 4 líneas de Fase 1 en cada skill que lo lea** | `DUDOSA` — se paga donde se usa: los dos inventarios y `hechos-con-prueba`, no los siete. **Comprobar antes**: si el dato existe hoy en algún sitio de su flujo |
| 18 | `Lo dijo usted el <fecha>` como coordenada del canal oral | `hechos`, `cronologia`, `redactar` | Ella corrige una fecha en la conversación y `cronologia`, que no tiene grado donde ponerla, la aplica **en silencio** — justo lo que el skill prohíbe hacer con un conflicto | Una fórmula en tres skills | `DUDOSA` — acotada a los tres que producen enunciados fechados, y **su regla de precedencia es §8.4** |
| 19 | `A quién pedírselo` en cada entrada de faltante | Hoy solo en `inventario-de-anexos` parte 5-A, y ahí funciona | Ella recibe cuatro listas de cosas ausentes y ninguna dice a quién se pide cada una | Se paga **por entrada**, en seis secciones más | `DUDOSA` — y la consolidación que lo justificaría choca con §8.3. **Comprobar antes**: si consolidar sin consumir trabajo derivado es posible |

**Lo que no está en esta tabla y se propuso**: 55 campos del Knowledge Pack, la tabla de correspondencia de etiquetas entre pasadas, la cuarta columna de la tabla de correspondencias, `anexo_id` interno, `snapshot_hash`, `consulted_at`. Está en §6 con el motivo.

---

## §3 — Coherencia entre los siete comandos

**Lo formal está mejor de lo esperado y no hay que tocarlo, en una línea:** el bloque anti-instrucciones es byte-idéntico en los siete (1104 bytes, mismo md5) y el párrafo «Palabras que no se escriben nunca» es idéntico en tres. No unificarlos en un archivo común: un núcleo compartido cuya ausencia falle en silencio es lo contrario de lo que esa regla necesita.

Lo semántico está peor. Lo que diverge y hay que unificar:

| # | Qué diverge | Quién dice qué | Qué se unifica | Estado |
|---|---|---|---|---|
| 1 | **Qué material es legible** | `inventario-de-bienes:17` lo lee como imagen; `cronologia:106`, `revisar-documento:167`, `inventario-de-anexos:95`, `estado-del-caso:86`, `hechos:65`, `redactar:106` lo declaran ilegible | El párrafo de `bienes:17`, literal, en los otros seis, bajo el título «Cómo se accede al material», más su pregunta de autoevaluación | **CRÍTICO. Se aplica sin medir.** Seis comandos escriben hoy «no se pudo leer» sobre material que el séptimo lee |
| 2 | **El audio** | `hechos-con-prueba` está construido entero sobre citar minutos (`00:08:12`) y su `FORMATO` imprime seis fichas ancladas a minutos; `cronologia:106`, `anexos:95` y `bienes:99` lo declaran no legible | Nada todavía | `POR VERIFICAR` **bloqueante.** No es diferencia de redacción: es una capacidad no comprobada. Mientras tanto, lo prudente y lo que dicen tres de cuatro: la entrevista entra transcrita. §8.5 |
| 3 | **De dónde sale `<caso>`** | Cinco notaciones distintas: `<caso>`, `<caso corto>`, `«caso»`, «nombre de la carpeta», y un `2026-014` con pinta de radicado interno que no existe en ningún otro archivo | **El nombre de la carpeta, literal.** Es el único origen que no depende de un archivo que el propio sistema escribe | **SOSTENIDO.** Antes hay que resolver si la carpeta lleva nivel de área (§8.7) |
| 4 | **Varios ` - REVISADO.md`** | Los tres consumidores dicen «el archivo» —singular— y solo contemplan el caso de cero | No se elige: se nombran los dos con su fecha y se pregunta | **SOSTENIDO** (§1.b fila 8) |
| 5 | **`apoya` / `contradice` / `sitúa`** | Cuatro vocabularios. `bienes:65` dice «las mismas de `hechos-con-prueba`» y redefine las tres; `contradice` queda expulsado de una lista cerrada de tres, o sea que hay un valor que nunca puede aparecer | Definición canónica en `hechos §2.3`, **citada y no reescrita** por los otros dos | **SOSTENIDO.** La GUIA:308 le enseña una sola definición: la de `hechos` |
| 6 | **El nombre del fenómeno** | contradicción (`hechos`) / en conflicto (`cronologia`) / discordancias (`anexos`) / contradicciones entre documentos (`bienes`) | **«en conflicto»**, y no por elegancia: es la única de las tres que ella ya tiene aprendida de la GUIA. Reentrenarla cuesta más que renombrar un bloque | **SOSTENIDO** |
| 7 | **Prefijos de etiqueta** | `C1` (hechos) y `C-1` (cronologia) nombran cosas distintas en la misma carpeta; `H-14` es un hecho en una salida y el hecho DÉCIMO CUARTO de la demanda en otra; `B-05` y `5-B` conviven en la misma fila del mismo ejemplo | Un solo esquema | `DECISIÓN PENDIENTE` §8.8: se propusieron **dos esquemas incompatibles** (`A-`/`HC-`/`FC-` frente a `AX-`/`D-`). Aplicar los dos reproduce el problema |
| 8 | **Clases A / B / C de «lo que falta»** | Los dos inventarios | `5.1 MENCIONADOS Y AUSENTES` / `5.2 SIN NINGÚN DOCUMENTO` / `5.3 PRESENTES CON PROBLEMA`, y `ver 5-B` → `ver 5.2` | **SOSTENIDO.** Es el lado barato de la colisión de la fila 7 |
| 9 | **Autoevaluación** | De 11 a 25 preguntas sin núcleo declarado; se cayeron tres que son promesas centrales: «¿presenté algo como verificado?» falta en tres, «¿entregué el conteo?» en dos, «¿sobrescribí algo?» en `cronologia` | Un núcleo de ocho preguntas declarado en README §7; lo demás, libre | **SOSTENIDO** |
| 10 | **Nombres de archivo** | Tres separadores, tres formas de versionar, tres notaciones de fecha; `revisar-documento` no dice cómo se llama su archivo ni prohíbe sobrescribir | Una convención en seis. **`Hechos - <caso> - <AAAA-MM-DD> - REVISADO.md` NO se toca** | **SOSTENIDO con la excepción.** Es el literal transcrito en cinco sitios y el único acoplamiento que funciona: no se arriesga a cambio de que la carpeta ordene alfabéticamente |
| 11 | **`0-Estado del caso` y `3-Para presentar/`** | El primero es desconocido para tres comandos y `hechos:243` lo nombra sin extensión, como si fuera una carpeta; el segundo no está acotado en cuatro | Una línea idéntica en los siete para cada uno | **SOSTENIDO** (§1.b filas 2 y 10) |
| 12 | **Dónde va el bloque AVISO** | Está en los siete `VERIFICADO`, pero `revisar-documento §5` («siempre los ocho apartados, en este orden») y `redactar §8` no lo prevén en su formato de salida | Una línea al final de los dos formatos | **SOSTENIDO.** Un bloque que no está en la lista tiene probabilidad real de no salir, y `redactar` es donde un documento hostil más gana callándose |
| 13 | **«sin respaldo» / «sin apoyo»** | La GUIA le enseña a buscar «sin respaldo en el material revisado»; los comandos escriben «Sin apoyo». `bienes:71` usa una tercera | Sustitución mecánica a «sin apoyo», y la lista de palabras prohibidas de la GUIA pasa de seis a las ocho canónicas | **SOSTENIDO.** Es su única red de detección y está mal calibrada |
| 14 | **La comprobación en bloque (v0.2.0)** | En 2 de 7. Los otros cinco dicen «abre cada anclaje uno por uno» | Propagarla a `hechos`, `cronologia` y `estado-del-caso`; `revisar-documento` es excepción legítima y hay que decirlo para que no parezca olvido | `DUDOSA`. **Comprobar antes**: su justificación —el «−34 % medido»— no existe (§4). Puede seguir siendo buena idea; su número, no |
| 15 | **Los dos inventarios no se mencionan** | Cero menciones cruzadas | Dos líneas de remisión mutua. **No** reutilización de capturas | **SOSTENIDO acotado** (§1.b, última sección) |

---

## §4 — El banco de medición

### Qué prueba puede fallar hoy: ninguna

Está demostrado por ejecución, no argumentado: `medir.py` sobre un run sintético de un agente y sin `--salidas` imprime «VERACIDAD ── intacta · fabricaciones 0» y sale con código 0. `HECHO MEDIDO`

| # | Defecto | Evidencia | Corrección | Estado |
|---|---|---|---|---|
| 1 | No hay veredicto ni umbrales: siempre sale con 0 | El único `sys.exit` es por run no encontrado | `veredicto` + código de salida; `NO_MEDIDO` cuando no hay coste o no hay salidas; «intacta» exige `declaradas>0` y `archivos>0` | **SOSTENIDO — tramo 1** |
| 2 | El detector de fabricaciones es ciego al formato que los propios métodos ordenan | Detecta 3 de 12 formas naturales y 1 de 5 casos realistas; el ejemplo canónico de la propia skill da cero | No parchear: sustituir por cita localizable + `cita_juridica[]` | **SOSTENIDO** |
| 3 | Los `.docx` nunca se analizan | Los dos JSON del A/B traen `fabricaciones: 0` y `declaradas: 0` sobre una entrega que el instrumento no abrió | `texto_de(path)`, seis líneas | **SOSTENIDO — tramo 1** |
| 4 | `declaradas()` absuelve con cualquiera de 18 palabras en ±300 caracteres | Sobre «El contrato tiene 7 clausulas. No aparece el nombre…» devuelve `[7]` | **Se retira.** Tras la invalidación del truth set, declarar una página ilegible ya no es la conducta correcta. La sustituyen `paginas_citadas` y `paginas_no_abiertas` | **SOSTENIDO** |
| 5 | Cero medición sobre fuentes | `citas()` cuenta `«...»` y no abre ninguna fuente; `medir()` nunca recibe la ruta del material | `cita_no_localizable` (a triaje humano, no a fallo automático) y `cita_juridica[]` (a fallo) | **SOSTENIDO** |
| 6 | No mide un A/B | Los dos JSON traen coste **idéntico byte a byte** y `comparar()` imprime +0 % en todo | Un run por versión y `--comparar-con`, o `--agente <id>=<version>`. Escribirlo en el README, que documenta un uso que el A/B real no siguió | **SOSTENIDO** |
| 7 | El séptimo comando no existe para el instrumento | `COMANDOS` tiene seis nombres; `inventario-de-bienes` no está | Añadirlo, y avisar al arrancar si `skills/` no coincide con `COMANDOS` | **SOSTENIDO** |
| 8 | `coste.segundos` suma agentes que corrieron en paralelo | 3.896 s en el JSON frente a 35:58 y 28:58 por separado | `segundos_pared` y `segundos_agente`, y se imprime el primero | **SOSTENIDO** |
| 9 | La métrica de decisiones solo conoce `[HAE]-` y cae en silencio a otra unidad | `bienes` usa `B-`, `cronologia` usa `C-`; `A-` es rama muerta | `[A-Z]{1,2}-\d{1,3}`, y sin fallback: `decisiones=None` antes que un número de otra unidad | **SOSTENIDO** |
| 10 | `~$` cuenta como entrega; `volumen` se calcula sobre toda la carpeta | `volumen.archivos` dice 7 cuando son 6; una corrida de un comando reporta el volumen de cinco | Mismo filtro en las dos funciones; exigir carpeta de salidas vacía | **SOSTENIDO** |

### Cómo se reconstruye el truth set

El plan escrito —transcribir las 25 páginas— es viable y es el camino más caro. Tres problemas que hay que decir antes de empezarlo: **circularidad** (si transcribe el modelo, el truth set lo produce la misma facultad que se está midiendo, y una alucinación de transcripción se vuelve verdad de referencia); **custodia** (una transcripción literal **es** el material, con los datos de una menor: no puede entrar al repositorio, tiene que vivir con los PDF y el caso JSON solo guarda hashes — y eso no está escrito en ninguna parte); y **alcance** (sirve para citas literales por coincidencia de cadena, no para la paráfrasis).

Orden recomendado, y las dos primeras hacen innecesaria buena parte de la tercera:

| Vía | Qué es | Coste | Estado |
|---|---|---|---|
| **C — caso-02 sintético** | `13-synthetic-benchmark.md` **ya tiene el truth set completo escrito**: transcripción canónica SEG-001…031, DOC-01…05, 15 hechos esperados con locator, 5 contradicciones, 6 irrelevantes, 8 afirmaciones prohibidas (incluida «cualquier cita normativa o jurisprudencial, real o inventada»). Es sintético: vive en el repositorio, se corre mil veces, no tiene custodia | Un día: materializarlo en archivos y pasar las tablas a JSON | **SOSTENIDO. Empezar por aquí** |
| **B — OCR local como índice** | Capa de texto donde exista (14 páginas, gratis) + Tesseract offline en las otras 25, usado **como índice de búsqueda, no como verdad**: una cita no localizada va a triaje humano, nunca a fallo automático | 2-4 h de ingeniería, minutos por corrida | `DUDOSA` — **sostenida si esa condición se escribe en el código y no en el informe**. §8.6 |
| **A — transcripción, acotada** | Solo las páginas que los comandos **citan de verdad**, no las 25 a ciegas. Se corre una vez, se recoge el conjunto (documento, página) citado y se transcribe eso; cada corrida añade las nuevas | 15-40 min por página, humanas | `DECISIÓN PENDIENTE` §8.6. El truth set crece para cubrir lo que el producto toca |

### El suelo del instrumento, y qué números sobreviven

`HECHO MEDIDO`: con la única dispersión conocida (76 → 63 fichas del mismo método sin cambiar una coma, CV 13,2-17 %), **con una corrida por brazo el efecto mínimo detectable es 52-67 %**.

- El **−34 % de turnos** de `inventario-de-anexos` v0.2.0 tiene p entre 0,07 y 0,16: **deja de citarse como hecho medido.** La v0.2.0 se conserva igual, por otras razones (cierra una duplicación, encontró 13 discordancias).
- El **−2 % de turnos** y el **−16 % de decisiones** de `hechos-con-prueba` están por debajo del suelo y no debieron reportarse.
- El **+177 % de caché escrita por +31 % de método sí sobrevive** al mismo suelo. Es el único número que sostiene la economía de este refinado, y por eso el §7 tiene una puerta de medición en el paso 4.
- Presupuesto para detectar un 20 %: 7 corridas por brazo si el CV es 13,2 %, 12 si es 17 %. Con tres por brazo solo se detecta un 30-39 %. `DECISIÓN PENDIENTE` §8.6.
- Primero conviene medir el CV de cada métrica con 5 corridas de **una sola** versión (≈3 h, una vez): el ±17 % se midió sobre un recuento de producción y se está extrapolando a turnos y a caché sin evidencia. `SUPUESTO`

---

## §5 — El producto: los huecos de experiencia

**Lo que está bien, en una línea:** el interior de las salidas y la guía §3 sobre dónde se procesa el material —que distingue guardar de trabajar y admite que no se ha encontrado forma de cambiarlo— son lo mejor del repositorio. El problema es todo lo que rodea a una salida: el producto no tiene principio, no tiene orden y no tiene final.

| # | Hueco | Qué le pasa a ella | Corrección | Coste |
|---|---|---|---|---|
| 1 | **La guía está escrita para seis comandos y hay siete** `VERIFICADO hoy`. `inventario-de-bienes` no aparece ni una vez; el README dice «seis» en seis sitios; `plugin.json` sigue en `0.1.0` con dos skills en `0.2.0` | Un comando que la guía no nombra no existe para ella. Y la comprobación que el README propone —mirar la versión en su pantalla— ya no distingue nada, justo cuando la v0.2.0 es la que corrige lo de los escaneados | Fila nueva en GUIA §1 y README §1, seis→siete, carpeta en el árbol, subir `plugin.json` y las dos descripciones | BAJO |
| 2 | **No hay orden de uso.** Los siete se presentan como tabla de consulta por síntoma. Una sola referencia cruzada en todo el juego | El orden existe y es forzoso en dos tramos. En el caso real se saltó y el producto gastó 4,7 minutos y 332 líneas en explicar que no podía redactar `HECHO MEDIDO` | Un §1.bis de doce líneas con los cuatro momentos, y un renglón «SIGUIENTE PASO SUGERIDO: `<comando>` — porque `<motivo>`» al cierre de las siete | BAJO |
| 3 | **Nadie crea la oficina, ni el caso, ni las carpetas**, y `estado-del-caso:13` prohíbe reorganizar | Cinco comandos escriben en `2-Borradores/`. Si no existe —el estado más probable el primer día— no hay regla escrita: el comportamiento queda al azar | «Si `2-Borradores/` no existe, dilo y pregunta antes de crearla; no reorganices nada más». El comando nuevo está rechazado (§6) | BAJO |
| 4 | **El tiempo está medido y ella no lo sabe** | El rango real es **5 a 36 minutos**, no 5 a 20 `HECHO MEDIDO`. Lo pide entre dos audiencias, se encuentra media hora de espera sin aviso, y no vuelve a pedirlo — sin que el producto haya fallado en nada de lo que sabe hacer | Columna «Cuánto suele tardar» en la tabla de la GUIA con los rangos medidos y la frase «medido sobre un caso de dos documentos y 56 páginas; con más material, más». **Antes**: cronometrar `estado-del-caso` e `inventario-de-bienes`, que no tienen ni una corrida medida. No se estiman | BAJO |
| 5 | **Las listas de «lo que falta» salen cuatro veces**, calculadas por separado, y se contradicen: `hechos` dice que el acta de la Comisaría no aparece y el inventario la lista como anexo 4 `HECHO MEDIDO` | Lo único que ella hace después de leer es coger el teléfono y pedir. Hoy tiene que fundir cuatro listas de origen distinto sin saber cuál se calculó sobre la carpeta completa | Depende de §8.3: consolidar significa consumir trabajo derivado. La materia prima ya existe y es buena («A quién pedírselo», en el inventario de anexos) | MEDIO, bloqueado |
| 6 | **`revisar-documento` no nombra su archivo, no lo fecha, no prohíbe sobrescribir**, y por defecto solo va a pantalla | Dos revisiones del mismo documento producen el mismo nombre y la segunda borra la primera con las anotaciones que ella hubiera puesto encima — contra lo que la GUIA:329 le promete. Y 11,5 minutos y 197 citas desaparecen al cerrar la sesión | Copiar el bloque de `cronologia §6`, y cambiar el defecto: el archivo se escribe siempre; si no lo quiere, lo borra ella | BAJO |
| 7 | **`QUÉ COMPROBAR PRIMERO` está en 1 de 7** | 555 citas en las salidas de texto `HECHO MEDIDO`, más las del `.docx` que el banco ni cuenta. Darle 555 coordenadas sin prioridad es pedirle una revisión que no cabe en su día; el resultado previsible es que no revise ninguna, y su revisión es el único control real | Copiar el bloque a las otras seis, con criterio propio de cada salida | `DUDOSA`. **Comprobar antes**: ya se midió en el A/B de `hechos` y **no rindió como coste**. El argumento de que la métrica era la equivocada es legítimo y no tiene datos: es revertir una decisión tomada con datos usando un argumento sin ellos. Que se diga así al aplicarlo |
| 8 | **El Ejemplo 2 de la guía promete citar el minuto de una grabación** y `cronologia:106` lo prohíbe expresamente | Si llega con una entrevista grabada, los minutos serían coordenadas estimadas: la única cita fantasma que ni siquiera se puede descubrir reabriendo el archivo | `POR VERIFICAR` bloqueante. §8.5 |
| 9 | **La GUIA no nombra a Anthropic**: dice «la empresa que hace el programa» | Es la única sección que puede cambiar lo que ella hace, y la decisión —y la conversación que tendrá con su clienta— exige un nombre propio. El circunloquio es aquí menos claro, no más | Siete palabras | BAJO |
| 10 | **La guía dibuja una estructura de carpetas que no es la de la máquina**: falta el nivel de área (`Despacho/Familia/<caso>/`) | Es la primera decisión que toma cada mañana —qué carpeta adjunta— y está sin documentar. Y de ahí cuelga qué ve `estado-del-caso` en su Fase 1 | §8.7 |
| 11 | **La pregunta jurídica directa no activa ninguna skill** | Contesta el modelo desnudo, sin método y sin fuente. Es el camino más corto por el que entra derecho fabricado en este producto | Dos líneas (§1.a, canal 3) | BAJO. **La mejor relación del refinado entero** |

---

## §6 — Lo que NO se hace, y por qué

El refinado propuso ~90 huecos y más de 100 campos atómicos, casi todos por adición, **con una sola supresión en todo el conjunto** y ninguna estimación de coste de ejecución. El campo `esfuerzo: BAJO/MEDIO/ALTO` mide la tarde de quien escribe, no la factura del producto: el autor paga una vez, el producto paga en cada corrida, para siempre. Esto es lo que se queda fuera.

| Qué se propuso | Por qué no entra |
|---|---|
| **Construir el Knowledge Pack** (55 campos) | Su propio diagnóstico lo mata: el dueño no puede comprobar vigencia ni pertinencia; `curator` es obligatorio y «curador» no aparece en el corpus `VERIFICADO hoy`; 29 workflows con **cobertura cero**; 5 de 6 grupos `HIGH_MAINTENANCE` sin cadencia ni responsable. La pregunta del propio examinador —«si no hay una abogada haciendo ese paso, ¿para qué construirlo?»— no está contestada. Y un pack sin mantenedor no es neutral: **da confianza en datos viejos**, que es peor que no tenerlo |
| `fecha_expedicion` como campo tipado | Ninguna decisión del producto depende de ella; el año ya va en el identificador canónico. El fallo declarado —confundir los tres momentos— lo evita `vigencia_desde`. Completitud registral |
| `snapshot_hash`, `titulo_esperado`, `ultima_resolucion_ok` | No existe proceso que los recalcule ni que compare. El propio examinador escribe tres huecos antes que «un aviso que solo se lee no sirve». **Un hash que nadie verifica es peor que ningún hash: da confianza sin comprobar.** Vuelve el día que exista el proceso |
| `alcance_derogacion`, `pasaje_derogatorio`, `control_constitucional[]`, `regimen_transitorio` + `a_que_actos_aplica` | Determinar el alcance de una derogatoria o a qué actos alcanza un régimen de transición **es interpretación jurídica**. Son campos definidos para un curador que no existe |
| `consulted_at` + `pinned_passage` «porque es el momento más barato de añadirlos» | El motivo está escrito en la propuesta y es literalmente el criterio que este refinado manda rechazar. El coste es casi cero; el criterio no, y es el que genera los otros 68 campos |
| Rellenar `derogada_por` / `derogada_desde` del Decreto Ley 2158 con «lo que el corpus ya afirma» | Es copiar una afirmación de un sitio a otro y darla por comprobada: el lavado de conocimiento que prohíbe `04-source-governance.md:87-89`, que el mismo examinador lista como uno de los aciertos del corpus. **Sostiene solo la mitad**: degradar la etiqueta a `VIGENCIA_POR_VERIFICAR`, que no exige leer nada |
| La tabla completa de las tres fechas copiada a cuatro comandos (~40 líneas) | El fallo concreto es uno y es real —en `cronologia` no hay grado donde poner una fecha que solo está en el nombre del archivo— y lo arregla **la línea** que la propia corrección escribe al final. Cuarenta líneas para el efecto de cuatro |
| Cuarta columna «Quién produjo ese documento» en la tabla de correspondencias | Se paga en **cada fila** —una por frase del borrador— para dar un dato que la lista 3 bis del cierre, de la misma propuesta, entrega ya filtrado a lo accionable. Sostiene la lista, no la columna |
| La tabla de correspondencia de etiquetas entre pasadas | El hallazgo está demostrado y es grave, pero la corrección **documenta el defecto y se paga por fila**. La corrección de una línea es no producirlo: el criterio de numeración no se cambia entre pasadas y los anexos nuevos van al final |
| `anexo_id` interno (`A-07`) citado dentro del escrito | **Un identificador interno del sistema dentro de un escrito que ella firma es jerga** y rompe una regla dura. Se resuelve con archivo y página: «el anexo 3 (`pagos.pdf`, p. 2)» |
| `/abrir-caso` y `/que-hay-que-pedir` como comandos nuevos | El producto acaba de gastar su séptimo comando en `inventario-de-bienes` en vez de en la consolidación, y la respuesta propuesta es un octavo y un noveno. El problema real de `/abrir-caso` lo resuelve una línea (§5, hueco 3); la consolidación barata consume trabajo derivado y choca con §8.3 |
| Que los dos inventarios **reutilicen la captura** del hermano | Destruye el único control cruzado del producto: que cuatro comandos coincidieran en las 25 páginas ilegibles fue una medición independiente, no redundancia. Se conservan las dos líneas de remisión mutua |
| Renombrar `Hechos - <caso> - <AAAA-MM-DD> - REVISADO.md` | Es el literal transcrito en cinco sitios y el único acoplamiento entre comandos que funciona. No se arriesga a cambio de que la carpeta ordene alfabéticamente. Los otros seis sí se alinean |
| Propagar **ahora** la comprobación en bloque a cinco comandos | Su justificación es el «−34 % medido», y ese número no existe (§4): n=1, p entre 0,07 y 0,16, y `comparar()` sobre los dos JSON del A/B imprime +0 % porque el coste es idéntico byte a byte. Puede seguir siendo buena idea; vuelve cuando el banco pueda medirla |
| Extender la marca ` - REVISADO` a cronología e inventarios | Depende de §8.3: si el trabajo derivado no es fuente, no hay nada que aprobar. La corrección barata y honesta es la contraria: quitar «cronología, inventario de anexos» de `redactar-escrito:11`, que promete un material revisado que su propia §2.1 no admite |
| Un juez LLM para adjudicar el truth set | Introduciría un segundo operador no determinista dentro del instrumento que mide al primero. No se adopta en este ciclo |

---

## §7 — Orden de trabajo

Por valor entre esfuerzo, y con una puerta. **El refinado no se aplica entero: se aplica por tramos y se mide el coste entre tramo y tramo.** Cualquier orden que no empiece por eso está comprando un +177 % a ciegas.

| # | Qué | Por qué va aquí | Esfuerzo | Depende de |
|---|---|---|---|---|
| 1 | **Banco, tramo 1**: veredicto + código de salida; `texto_de()` para `.docx`; `cita_juridica[]` obligatoriamente vacío; `escrituras_prohibidas[]` | Es lo único que convierte el banco en algo que puede fallar, y protege la regla 1 —el eje del encargo— con una prueba determinista. **Cero líneas de método** | BAJO | — |
| 2 | **El párrafo del escaneado de `inventario-de-bienes:17` a los otros seis**, con su pregunta de autoevaluación | Retira una falsedad demostrada sobre 25 de 39 páginas y sobre la pieza central del caso. **No se mide antes: no es una mejora de coste** | BAJO (~30 líneas) | — |
| 3 | **Cabecera de tres líneas en las siete** (caso literal · comando+versión+pasada+hora · cómo se leyó + fecha de corte) y `plugin.json` a la versión que corresponda | Se paga una vez por salida, no por fila, y desbloquea la rama de detención, la comparabilidad entre pasadas y la atribución de versiones | BAJO (~28 líneas) | — |
| 4 | **PUERTA: medir el coste de 2 y 3** | Si +58 líneas mueven la caché escrita más de lo que ahorra el descuento del párrafo del escaneado, **el resto del refinado se replantea entero**. Es el único punto del plan donde se compra información | BAJO | 1 |
| 5 | **Las tres líneas de la GUIA que no cuestan ejecución**: nombrar a Anthropic; «este programa no contesta preguntas de derecho»; la cláusula de DP-1 extendida al canal oral | Cierran dos de los cuatro canales por los que entra derecho, y no añaden una sola línea a ningún método | BAJO | §8.9 para la tercera |
| 6 | **Reglas baratas de precedencia**: rama de detención ante varios ` - REVISADO.md` y ante material posterior al corte; la decisión por ficha leída por los dos inventarios; y no renumerar anexos entre pasadas | Los tres fallos silenciosos más caros del oleoducto, y ninguno se corrige con un campo por fila | BAJO | 3 (fecha de corte) |
| 7 | **Nivel de fuente**: el trabajo derivado no es fuente; `0-Estado del caso` es resumen; `3-Para presentar/` se lee y no se escribe | Cierra la ruta de lavado completa —de «fecha deducida» a afirmación firmada— con una línea por skill | BAJO | **§8.3** |
| 8 | **Banco, tramo 2**: retirar `declaradas()`; `content_manifest[]` con sha256; `imagenes` por agente; `segundos_pared`; `[A-Z]{1,2}-` en decisiones; `inventario-de-bienes` en `COMANDOS`; `ejecuciones[]` con mediana y rango | Hace comparables dos corridas y detecta la contaminación de capacidad que ya invalidó una comparación entera | MEDIO | 1 |
| 9 | **caso-02 sintético** desde `13-synthetic-benchmark.md` | El truth set ya está escrito, es sintético —vive en el repositorio, sin problema de custodia— y es reproducible para siempre. Un día contra 8-15 horas de transcripción | MEDIO | 8 |
| 10 | **Documentación de cara a ella**: seis→siete y `inventario-de-bienes` en GUIA y README; duraciones medidas (tras cronometrar los dos que faltan); «sin respaldo»→«sin apoyo»; orden de uso; nombre y no-sobrescritura del archivo de `revisar-documento` | Es lo que decide la adopción, y hoy la guía describe un producto que no es el que hay | BAJO | 4 |

Todo lo demás espera a que exista un número.

---

## §8 — Decisiones que solo puede tomar el dueño

Por urgencia: **8.3 y 8.5 bloquean trabajo ya en el orden; 8.9 bloquea el paso 5; el resto puede esperar.**

| # | Decisión | Qué bloquea | Opciones | Mi lectura |
|---|---|---|---|---|
| **8.1** | **¿Unidad artículo o unidad ley** en el registro de norma? | Todo el diseño del pack: no se puede definir ningún campo antes | Ley: el pack es la bibliografía que ya existe. Artículo: es utilizable y cuesta uno o dos órdenes de magnitud más | Sin respuesta a 8.2, la pregunta es teórica |
| **8.2** | **¿Existe una abogada que verifique vigencia y pertinencia, con nombre?** Y si existe: ¿se acepta la regla dura «sin `vigencia_hasta` comprobada, la norma no se sirve como citable»? | El Knowledge Pack entero. Y con él, la respuesta a la pregunta dura | Si no hay nadie: **no se construye**, y la abstinencia sigue siendo la garantía. Si lo hay: la regla dura hace que el primer pack sirva muy poco; su alternativa es que sirva mucho y a veces mal | No construirlo este ciclo. Un pack sin mantenedor da confianza en datos viejos |
| **8.3** | **¿El trabajo derivado del sistema es fuente?** (cronología, inventarios, `0-Estado del caso`) | Los pasos 5 y 7 del orden, la consolidación de faltantes, y la marca ` - REVISADO` en cronología e inventarios | (a) Nunca es fuente: siete lecturas independientes, se paga abrir dos veces la carpeta. (b) Sí lo es: se reutilizan capturas y se ahorra una pasada | **(a).** El coste es el precio del único control cruzado que el producto tiene, y está justo en el eje que es lo único demostrado |
| **8.4** | **¿La palabra de ella manda sobre un documento, o va al lado?** | La fila 6 de la tabla de precedencias y el campo `Lo dijo usted el <fecha>` | Al lado (si discrepan, conflicto, se entregan los dos) / su corrección manda | **Al lado.** Pero si su intención es que mande, hay que escribirlo: hoy el modelo elige solo, y lo más probable es que corrija en silencio |
| **8.5** | **El audio: ¿la plataforma lo lee?** | `hechos-con-prueba` entero, su `FORMATO-DE-SALIDA.md` (seis fichas ancladas a minutos) y el Ejemplo 2 de la GUIA | Medirlo con un audio real suyo antes de tocar nada | **No adivinar.** Mientras tanto, estandarizar hacia lo que dicen tres de los cuatro: la entrevista entra transcrita `POR VERIFICAR` |
| **8.6** | **Truth set y presupuesto de medición**: ¿se acepta OCR local (offline, como índice de búsqueda y nunca como verdad, con triaje humano)? ¿Quién transcribe, y dónde vive la transcripción? ¿Cuántas corridas por brazo? ¿Se parte el banco en `verificar.py` + `medir.py`? | La capacidad de medir cualquier cosa de aquí en adelante | OCR: 2-4 h contra 8-15 h de transcripción humana. Corridas: 7 por brazo (CV 13,2 %) o 12 (CV 17 %) para detectar un 20 %; con 3 solo se detecta 30-39 % | Sí a OCR con la condición escrita **en el código**. La transcripción **no puede hacerla el modelo** (circularidad) ni entrar al repositorio (custodia). Partir el banco: sí — un test determinista sobre una salida guardada tiene varianza cero |
| **8.7** | **¿La carpeta de trabajo lleva nivel de área** (`Despacho/Familia/<caso>/`) y qué adjunta ella cada mañana? | El campo `caso`, la GUIA §2 y la Fase 1 de `estado-del-caso` | La máquina dice que sí; la guía dibuja que no | Documentar lo que hay, y «adjunte siempre la carpeta del caso» |
| **8.8** | **Un solo esquema de prefijos de etiqueta** | La colisión `C1`/`C-1`, `H-14`/`H-14`, `B-05`/`5-B` | Se propusieron dos esquemas incompatibles (`A-`/`HC-`/`FC-` frente a `AX-`/`D-`). Aplicar los dos reproduce el problema | Elegir uno y escribirlo en el README §7. El lado barato (clases → 5.1/5.2/5.3) puede ir antes |
| **8.9** | **DP-1: ¿la salida puede transcribir el derecho que invoca el documento ajeno?** | El paso 5 del orden, y `GUIA-PARA-LA-ABOGADA.md:305`, que quedaría falsa el mismo día | Sí, entrecomillado y marcado como transcripción, con la cláusula final. O no, y entonces toda demanda que ella reciba se entrega sin su apartado de normas | **Sí, con la cláusula**: «sin que eso afirme que esa norma existe, rige o dice lo que el documento le atribuye». Y GUIA:305 se corrige **en el mismo cambio**, no después |
| **8.10** | **¿Se re-etiquetan los resultados ya publicados** que caen bajo el suelo del instrumento, y se sube `plugin.json` avisándole de pulsar Update? | La credibilidad de las cifras del proyecto y saber qué versión corre en su máquina | El −34 % deja de citarse como hecho medido; la v0.2.0 se conserva por otras razones | Sí a las dos. Un documento que etiqueta `POR COMPROBAR` pierde su valor en cuanto conserva un `POR COMPROBAR` ya resuelto |


