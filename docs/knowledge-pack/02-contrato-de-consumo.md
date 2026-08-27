# El contrato de consumo, la cobertura declarada y la caducidad

**Fecha: 2026-08-27. Material de trabajo, no una Skill.** Es la mitad que hace útil a la otra: [01-ficha-y-verificacion.md](01-ficha-y-verificacion.md) define qué se comprueba; esto define **qué pasa cuando el sistema pide una norma**.

**No contiene una sola norma, una sola fecha ni un solo estado de vigencia.** Los ejemplos usan rellenos evidentes (`LEY-0000-0000`, `AAAA-MM-DD`, `art. 00`).

---

## §1 — Las cuatro reglas duras

> **R1. Sin vigencia comprobada y firmada, la norma no se sirve como citable.**

Esa sola no basta, porque deja abierta la salida por la que hoy se escapa todo:

> **R2. Una respuesta del pack distinta de una de las cuatro citables cierra el turno. No habilita al modelo a contestar de memoria, ni a «orientar», ni a decir lo que cree recordar.**

Sin R2, R1 es un badén: el pack calla, el modelo habla, y el resultado se lee igual de fluido que si el pack hubiera contestado. R2 es la línea más importante de los dos archivos. Es también la que cierra el canal 3 del refinado (la pregunta directa de ella, que hoy contesta el modelo desnudo).

> **R3. Toda consulta lleva `fecha_del_caso` **y** `tipo_de_fecha`. Sin las dos, el pack no contesta.** Una norma no es vigente o no vigente: lo es *para una fecha*, y «la fecha del caso» no existe en singular — `05-temporal-applicability.md` §1 distingue `case_relevant_date`, `procedural_start_date`, `event_date`, `decision_date` y `published_at`. La transición de una norma puede girar sobre la fecha de inicio del proceso y no sobre la del hecho: pasar la equivocada convierte `FUERA_DE_LA_VIGENCIA_COMPROBADA` en citable en silencio. Las dos las aporta quien consulta, **tomadas de la carpeta del caso y nunca inferidas por el modelo** (`01` §5 regla 1), y las dos se repiten en la respuesta para que una elección equivocada sea visible para ella.

> **R4. Toda respuesta del pack devuelve un `token_de_respuesta`, y toda cita jurídica en una entrega viaja con su token al lado.** Formato: `codigo · identificador_canonico + alcance_comprobado · verificado_el · fecha_de_consulta`. Sin token, la cita no se publica.

R4 no es burocracia: es lo único que repone la comprobación mecánica que el pack retira. Hoy la seguridad se demuestra con un grep que exige **cero citas jurídicas** en las entregas (`REFINADO-Y-FUENTES.md` §1.a); el día uno del pack las citas pasan a ser legítimas y ese grep ya no distingue la buena de la fabricada. Con tokens la prueba de banco vuelve a ser mecánica (§7.4). Es la diferencia entre una regla y un mecanismo.

**Dónde vive este contrato.** `architecture/boundaries.md`:170 prohíbe que las reglas ejecutables viajen dentro de un pack. La tabla del §2 **es** una regla ejecutable: pertenece al producto sellado, no a los datos del pack, y **hasta que el producto la implemente, el pack no se consume**. Un modelo que interpreta la tabla también puede interpretarla con generosidad, y esa sería una sexta vía de escape.

---

## §2 — El pack no almacena estados: almacena afirmaciones fechadas, y el estado se calcula al leer

Este es el mecanismo del que cuelga todo lo demás, incluida la caducidad (§6). En la ficha no existe el valor «vigente»: existe `VIGENTE_AL AAAA-MM-DD` **firmado por una persona**. **Y el contrato es lista blanca:** se es citable solo cumpliendo todas las condiciones enumeradas. Cualquier otra cosa —un valor no reconocido, un valor con un comentario detrás, una casilla vacía, un guion bajo cambiado por un espacio, dos alcances que no se pueden comparar— **no es citable**. Antes el último renglón decía «en otro caso → `CITABLE`», y eso convertía cada errata en una autorización.

```text
Entrada: la(s) ficha(s), `peticion` (el alcance que se pide), `fecha_del_caso`,
         `tipo_de_fecha`, `materia` (la aporta quien consulta) y `hoy`.
         Falta fecha o tipo -> el pack no contesta (R3).

A. NORMA — citable solo si se cumplen las SIETE
   1  hoy <= revisar_antes_de calculado (§6)          si no -> PACK_CADUCADO
   2  estado_identidad = IDENTIDAD_VERIFICADA         CONFLICTO_DE_FUENTES -> CONFLICTO_DE_FUENTES
                                                      cualquier otro -> IDENTIDAD_POR_VERIFICAR
   3  peticion ⊆ alcance_comprobado, comparados como  más ancha, disjunta o NO COMPARABLE
      estructura (`01` campo 2), no como prosa            -> FUERA_DEL_ALCANCE_COMPROBADO
   4  estado_vigencia ∈ {VIGENTE_AL,                  VIGENCIA_PARCIAL_AL -> VIGENCIA_PARCIAL
      VIGENTE_CON_REFORMA_AL, SIN_VIGENCIA_DESDE}     cualquier otro o vacío -> VIGENCIA_NO_COMPROBADA
   5  fuente_vigencia llena y clase = PRIMARY_OFFICIAL    si no -> VIGENCIA_NO_COMPROBADA
   6  vigencia_desde es una fecha (no ESCALONADA)
      y fecha_del_caso >= vigencia_desde              si no -> FUERA_DE_LA_VIGENCIA_COMPROBADA
   7  si estado_vigencia = SIN_VIGENCIA_DESDE D:
      fecha_del_caso < D                              si no -> FUERA_DE_LA_VIGENCIA_COMPROBADA

   Cumplidas las siete, el código lo da el campo 6:
      VIGENTE_AL              -> CITABLE
      VIGENTE_CON_REFORMA_AL  -> CITABLE_CON_REFORMA
      SIN_VIGENCIA_DESDE      -> CITABLE_SIN_VIGENCIA_HOY

B. PROVIDENCIA — no entra por A: no tiene estado_vigencia, vigencia_desde ni
   alcance_comprobado, y una tabla de normas la atraviesa entera sin tocarla.
   Citable solo si se cumplen las CINCO
   1  hoy <= revisar_antes_de calculado (§6)          si no -> PACK_CADUCADO
   2  estado_identidad = IDENTIDAD_VERIFICADA         CONFLICTO_DE_FUENTES -> CONFLICTO_DE_FUENTES
                                                      cualquier otro -> IDENTIDAD_POR_VERIFICAR
   3  estado_uso ∈ {PROFESSIONALLY_CONFIRMED,         SUPERSEDED_OR_LIMITED o CONFLICTING
      RELEVANCE_REVIEWED}                                 -> PRECEDENTE_SUPERADO_O_LIMITADO
                                                      cualquier otro o vacío
                                                          -> JURISPRUDENCIA_POR_VERIFICAR
   4  busqueda_adversa llena y distinta de            si no -> SIN_BUSQUEDA_ADVERSA
      JURISPRUDENCE_GAP
   5  la proposición que se pide = proposicion_       si no -> FUERA_DEL_ALCANCE_COMPROBADO
      atribuida, literal
   Cumplidas las cinco -> CITABLE_PRECEDENTE

C. NO HAY FICHA — la materia la aporta quien consulta; el pack no la infiere de un
   identificador que no tiene (inferirla sería el modelo produciendo derecho).
   materia en la cobertura calculada (§5)   -> NO_ESTA_EN_EL_PACK
   materia en materias_excluidas, consulta territorial, o fecha fuera de la ventana
                                            -> FUERA_DE_COBERTURA
   materia indeterminable                   -> NO_TENEMOS_INFORMACION_SUFICIENTE (las dos lecturas)

D. VARIAS FICHAS — la clave de una ficha es el par (identificador_canonico,
   alcance_comprobado). Se devuelven TODAS las que coincidan con la petición, cada una
   con su respuesta; **el pack no elige la mejor coincidencia**, porque la mejor
   coincidencia siempre sería la que dice citable. Si dos coinciden y discrepan en la
   vigencia -> CONFLICTO_DE_FUENTES, con las dos transcritas.
```

**Consecuencia buscada: si nadie mantiene el pack, el pack se apaga solo.** No hace falta que alguien lea un aviso —en el corpus hay ya tres avisos de obsolescencia y ninguno ha disparado nada—: la degradación es el resultado por defecto de no hacer nada.

---

## §3 — Las diecisiete respuestas: cuatro citables y trece que cierran el turno

Cada respuesta tiene un código para el sistema y **una frase literal para ella**. La frase importa tanto como el código: el silencio se lee como «no hay regla», y esa lectura es el fallo que el pack existe para impedir. **Toda respuesta lleva su `token_de_respuesta` (R4) y el `recuento` del pack (§5); toda respuesta con fecha transcribe `nota_de_vigencia` literal, sin interpretar.**

| Código | Cuándo | Lo que ella lee | Qué puede hacer el sistema después |
|---|---|---|---|
| `CITABLE` | A.1-A.7 y `VIGENTE_AL` | «`LEY-0000-0000`, `art. 00` — identidad comprobada; vigente al `AAAA-MM-DD` para un caso cuya `<tipo_de_fecha>` es `AAAA-MM-DD`. Comprobado por Nombre Apellido el `AAAA-MM-DD` contra `<fuente PRIMARY_OFFICIAL>`. Nota: `<nota_de_vigencia>`. Revisar antes de `AAAA-MM-DD`.» | Citar el identificador con su token. **No** afirmar qué dice (§4) |
| `CITABLE_CON_REFORMA` | A.1-A.7 y `VIGENTE_CON_REFORMA_AL` | «`LEY-0000-0000`, `art. 00` — rige al `AAAA-MM-DD`, **en redacción distinta de la original**. La comprobación cubre el identificador y su vigencia, **no la redacción**. Nota: `<nota_de_vigencia>`.» | Citar el identificador. **Nunca** presentar la redacción original como vigente |
| `CITABLE_SIN_VIGENCIA_HOY` | A.1-A.7 y `SIN_VIGENCIA_DESDE D`, con el caso anterior a `D` | «`LEY-0000-0000` **rigió** de `AAAA-MM-DD` a `AAAA-MM-DD`; el caso cae dentro. **Hoy no rige.** Nota: `<nota_de_vigencia>`.» | Citar para ese momento, diciendo siempre que hoy no rige |
| `CITABLE_PRECEDENTE` | B.1-B.5 | «`SENTENCIA-X-000-0000` — identidad comprobada; sostiene la proposición `<proposicion_atribuida>` en `<pasaje>`; búsqueda adversa hecha el `AAAA-MM-DD`: `<constancia>`. Comprobado por Nombre Apellido.» | Citar la providencia **para esa proposición y ninguna otra** |
| `FUERA_DE_LA_VIGENCIA_COMPROBADA` | A.6 o A.7 | «Para un caso cuya `<tipo_de_fecha>` es `AAAA-MM-DD`, la comprobación firmada de `LEY-0000-0000` **no la cubre**: la vigencia comprobada va de `AAAA-MM-DD` a `AAAA-MM-DD`. Qué norma regía en esa fecha es una pregunta que el pack no contesta.» | Detenerse. Es un dato positivo y valioso, no un error |
| `VIGENCIA_NO_COMPROBADA` | A.4 o A.5 | «El pack **tiene** `LEY-0000-0000` y **no tiene comprobada su vigencia** — nadie miró, o la fuente no era de clase `PRIMARY_OFFICIAL`. Eso no es lo mismo que decir que no rige, ni que sí.» | Detenerse. Puede ofrecer abrir la ficha para que ella la verifique |
| `VIGENCIA_PARCIAL` | `VIGENCIA_PARCIAL_AL` | Lo mismo, más la `nota_de_vigencia` transcrita literal | Detenerse |
| `IDENTIDAD_POR_VERIFICAR` | A.2 / B.2 | «Nadie ha comprobado que `LEY-0000-0000` **sea** la norma que dice ser. Esto no es un problema de vigencia: es anterior.» | Detenerse. Un fallo de identidad nunca se sirve bajo un código de vigencia |
| `CONFLICTO_DE_FUENTES` | `estado_identidad` = `CONFLICTO_DE_FUENTES`, o D | «Dos fuentes oficiales discrepan sobre `LEY-0000-0000`: `<fuente 1>` dice `<…>`; `<fuente 2>` dice `<…>`. **El pack no elige.**» | Detenerse. Las dos transcritas, sin elegir (`04` §4) |
| `FUERA_DEL_ALCANCE_COMPROBADO` | A.3 / B.5 | «Se comprobó `LEY-0000-0000` en `<alcance_comprobado>`; usted pide `<peticion>`. **Esa comprobación no llega hasta ahí.**» — y en providencias: «se comprobó para `<proposicion_atribuida>`, no para lo que usted pide» | Detenerse. Cubre las dos direcciones: pedir más fino y pedir más ancho |
| `PRECEDENTE_SUPERADO_O_LIMITADO` | B.3 | «`SENTENCIA-X-000-0000` está marcada como superada o limitada, o en conflicto con otra. Nota de quien la revisó: `<busqueda_adversa>`.» | Detenerse. Es el mecanismo entero contra citar un precedente superado |
| `SIN_BUSQUEDA_ADVERSA` | B.4 | «Nadie buscó autoridad en contra de `SENTENCIA-X-000-0000`, o la búsqueda quedó en `JURISPRUDENCE_GAP`. Un solo resultado no es una revisión.» | Detenerse |
| `JURISPRUDENCIA_POR_VERIFICAR` | B.3, valor no reconocido o vacío | «El pack **tiene** `SENTENCIA-X-000-0000` y nadie ha revisado si sigue en pie.» | Detenerse |
| `PACK_CADUCADO` | A.1 / B.1 | «Esta ficha **caducó el `AAAA-MM-DD`**. Lo que dice es lo que Nombre Apellido comprobó el `AAAA-MM-DD`, y desde entonces nadie lo ha vuelto a mirar.» | Detenerse. La fecha y el nombre van siempre: son lo que permite ir a pedir una revisión |
| `NO_ESTA_EN_EL_PACK` | C, materia cubierta | «El pack cubre esta área y **no tiene** `LEY-0000-0000`. Eso significa que nadie la ha metido ni comprobado. **No significa que no exista.**» | Detenerse |
| `FUERA_DE_COBERTURA` | C, materia excluida, territorial o fuera de ventana | «El pack **no cubre** esta área, este nivel territorial o esta fecha. Aquí no hay información de ninguna clase: ni a favor ni en contra.» | Detenerse. Con la cobertura al lado, para que ella vea de un vistazo qué sí cubre |
| `NO_TENEMOS_INFORMACION_SUFICIENTE` | Materia indeterminable (C), o pack apagado (§6) | «No se puede saber si esto entra en lo que el pack cubre. Las dos lecturas están abiertas: puede que el pack cubra el área y no tenga la norma, o puede que no cubra el área.» | Detenerse. **Nunca** se responde solo identidad: identidad sola leída como vigencia es el fallo original |

`NO_TENEMOS_INFORMACION_SUFICIENTE` es además la **etiqueta visible** común a las trece no citables, ya existente en el corpus. El código dice *por qué*; la etiqueta dice *qué se puede hacer con eso*. **Y «no encontrado no es inexistente» rige también dentro del pack.** La regla ya está escrita carácter a carácter en las siete skills, sobre la carpeta del caso. Aquí duele más, porque el pack es el único componente que ella no puede abrir y revisar por su cuenta: si calla, su silencio no es inspeccionable.

---

## §4 — Lo que ninguna respuesta del pack contiene

- **El texto de la norma.** El pack no lo guarda (`01` §3). Una respuesta citable es un identificador comprobado, nunca un contenido.
- **Qué dice, qué exige o qué plazo fija.** El pack no responde «¿qué dice la ley sobre X?». Responde «¿está `LEY-0000-0000` comprobada y para qué fechas?».
- **Si aplica al caso.** Pertinencia, subsunción y estrategia son de ella.
- **Cálculo de términos.**
- **Jerarquía o especialidad entre dos normas comprobadas.** Si dos fichas responden, se entregan las dos; el pack no elige (§2.D). Las reglas de precedencia entre packs siguen siendo `DECISIÓN PENDIENTE` en `architecture/boundaries.md`.

El riesgo que esto deja abierto, escrito en voz alta: **el sistema puede citar una norma que existe y que rige, y atribuirle algo que no dice.** Contra eso el pack no hace nada; lo único que lo contiene es la regla 1 del método —«el método no contiene derecho»— y que ninguna respuesta del pack sea un texto que el modelo pueda parafrasear.

---

## §5 — La cobertura: el pack habla de sí mismo, y no puede mentir por inacción

Sin esto, el sistema reproduce dentro el error que persigue fuera. **La cobertura no se declara a mano: se calcula**, porque una lista escrita una vez por versión sigue afirmando «yo cubro esta área» cuando dentro no queda una sola ficha viva — la más tranquilizadora de las respuestas negativas servida por un pack vacío.

```yaml
cobertura:                         # calculada al leer, no escrita a mano
  jurisdiccion: colombia
  nivel_territorial: [nacional]    # toda consulta territorial -> FUERA_DE_COBERTURA,
                                   # con la frase de `06` (REQUIRES_TERRITORIAL_RESEARCH)
  materias_declaradas: [<materias con >=1 ficha NO caducada; vocabulario de `06`>]
  materias_excluidas:  [<todas las demás del vocabulario, nombradas una a una>]
  ventana_temporal:
    desde: AAAA-MM-DD
    hasta: AAAA-MM-DD
  granularidad: "por registro, en alcance_comprobado; no hay garantía uniforme"
  no_contiene: [texto normativo, interpretacion, pertinencia, calculo de terminos]

provenance:                        # exigido por boundaries.md §8
  curator: "Nombre Apellido"       # una persona, no «el equipo»
  validity_cutoff_date: AAAA-MM-DD # el verificado_el más antiguo de TODOS los registros
  ultima_reverificacion: AAAA-MM-DD # = max(verificado_el) de TODOS; de ella cuelga el apagado

recuento:                          # viaja en CADA respuesta, no solo en el manifiesto
  registros: 00
  citables_hoy: 00
  vigencia_no_comprobada: 00
  caducados_hoy: 00
```

- **`materias_excluidas` se nombra una a una.** Una lista de lo que sí cubre deja el resto en penumbra; nombrar lo excluido convierte `FUERA_DE_COBERTURA` en una respuesta comprobable. El vocabulario sale de `06-colombian-law-coverage-ledger.md`, no de una lista nueva — con la consecuencia incómoda de que `06` está casi entero en `GAP`, así que **la cobertura honesta del primer pack es casi vacía**. Eso es un dato, no un defecto.
- **`nivel_territorial` no es formalismo.** `06` tiene un estado propio `REQUIRES_TERRITORIAL_RESEARCH` y una columna `territorial_rules_checked`; hay materias cuya respuesta vive en un acto territorial que un pack nacional no puede tener nunca. Declarar «cubro esa área» ahí es exactamente leer el silencio como «no hay regla».
- **`validity_cutoff_date` se calcula sobre todos los registros, no solo sobre los citables.** Calculado solo sobre los citables saltaba hacia adelante cada vez que un registro viejo caducaba y salía del conjunto: nunca podía quedar atrasado, y el interruptor de §6 que colgaba de él era código muerto.
- **`recuento` viaja en cada respuesta.** Un pack donde 22 de 26 registros están en `VIGENCIA_NO_COMPROBADA` tiene que **verse así desde fuera** — y tiene que verlo quien consume, no solo quien audita el manifiesto.

---

## §6 — Cómo caduca y quién lo mantiene

**Quién.** `curator` es una persona con nombre y responde por el pack. `verificado_por` es quien firmó cada registro. Cuando no coinciden, manda el segundo: la responsabilidad es por ficha, no por archivo.

**`revisar_antes_de` no es un campo: es una cuenta.** Se calcula al leer:

```text
revisar_antes_de = min(verificado_el + cadencia, acortamiento_manual)
```

Un `acortamiento_manual` posterior a la fecha calculada **se ignora**, no se acepta. Cuando la fecha era escribible y almacenada, una sola casilla —por error o por presión de entrega— hacía inmortal una ficha y apagaba toda la degradación del §2.

**Cadencia — `PROPUESTA`, la cierran el dueño y la verificadora en P0.** Ninguna de estas cifras es un dato jurídico; son política operativa:

| Situación de la ficha | cadencia por defecto |
|---|---|
| `VIGENTE_AL`, sin nada pendiente en la nota | `verificado_el` + 12 meses |
| `VIGENTE_CON_REFORMA_AL` | igual, y la nota se transcribe siempre en la respuesta |
| La nota registra un cambio con fecha futura, una entrada escalonada o un control pendiente | `verificado_el` + 3 meses, **o el día anterior a esa fecha futura si es antes** |
| `SIN_VIGENCIA_DESDE` | `no aplica`: una norma que dejó de regir no vuelve. Se revisa solo por disparador extraordinario |
| `VIGENCIA_PARCIAL_AL` / `VIGENCIA_NO_COMPROBADA` | irrelevante: nunca fue citable |

**Revisión extraordinaria — la dispara cualquiera de estos, sin esperar a la cadencia:**
1. Una reforma que toca una `materia` declarada en la cobertura.
2. Una ficha cuya `nota_de_vigencia` anunciaba un cambio con fecha, y esa fecha llega.
3. Una entrada `CORRECTIVE` en el changelog de un registro relacionado.
4. **Ella reporta una discrepancia desde un caso real.** Es el disparador más barato y el único que mira al mundo en vez de al calendario. Necesita una vía de una línea para llegar al curador; si no la tiene, no existe.

**Qué pasa si nadie revisa: nada, y esa es la respuesta.** El estado se calcula al leer (§2), así que la ficha vencida deja de servirse sin que nadie actúe. Dos escalones más, por encima del registro:
- Si `recuento.caducados_hoy` supera un umbral —**`PROPUESTA`: un tercio de los citables**— el pack se declara `DEGRADADO` y lo dice en cada respuesta, citables incluidas.
- Si `hoy − ultima_reverificacion` supera **`PROPUESTA`: 18 meses**, el pack se apaga: deja de servir respuestas citables por completo y contesta `NO_TENEMOS_INFORMACION_SUFICIENTE`, entregando la identidad **como dato no citable y con la frase explícita «esto no dice que rija»**. Nunca en forma de respuesta afirmativa: un pack sin mantenedor que solo responde identidad reproduce el fallo del `01` §0 en el peor momento posible.

**Changelog tipado — se reutiliza el de `boundaries.md` §8, sin inventar nada:**

| Qué cambió en una reverificación | Entrada | Efecto |
|---|---|---|
| `estado_vigencia` cambia de valor (lo anterior estaba mal o dejó de ser cierto) | `CORRECTIVE` | Invalidación fuerte: los artifacts que dependen del pack **requieren revisión**. Es el caso que este instrumento existe para hacer visible |
| Se añade un registro, o se estrecha/amplía `alcance_comprobado` | `ADDITIVE` | Aviso suave que ella decide atender |
| Cambia una URL, un rótulo o la presentación | `FORMAL` | Solo afecta al render futuro |

`POR VERIFICAR`, ya señalado en `boundaries.md` y todavía sin cerrar: un artifact producido bajo la comprobación vigente en su momento procesal puede seguir siendo correcto para ese momento. Hasta que se decida, `CORRECTIVE` avisa; no reescribe nada.

---

## §7 — Lo que este instrumento sigue sin impedir

Se escribe para que nadie lo lea como una garantía que no da:

1. **Que se cite una norma vigente atribuyéndole lo que no dice.** El pack no guarda texto (§4). Lo contiene el método, no esto.
2. **Que se cite la redacción de un artículo reformado sin saber cuál es.** `CITABLE_CON_REFORMA` avisa de que la reforma existe y prohíbe presentar la redacción original como vigente, pero **no dice qué norma reformó ni desde cuándo**: el pack no ficha las ~20 modificatorias que el propio catálogo ya nombra (`01` §0). Registrar que existen sin obligar a ficharlas es todo lo que se compró, y hay que decir el número.
3. **Que la comprobación sea sincera pero equivocada.** El pack registra quién y cuándo, no acierta por ella. Lo que sí garantiza es que el error tiene nombre, fecha y fuente, y por tanto se puede encontrar y corregir — que es todo lo que hoy no ocurre.
4. **Que el modelo conteste igual por fuera del pack.** Lo cierra R2, y R2 se comprueba con una prueba de banco que **falla** cuando: una cita jurídica aparece **sin token**; el token lleva un código que no es de los cuatro citables; el token apunta a una ficha caducada; o el `alcance_comprobado` del token no contiene lo que la entrega cita. Es una comprobación sobre tokens, no un regex sobre prosa — el regex deja de servir el día uno del pack (R4).
5. **Que el primer pack sirva muy poco.** Va a servir muy poco, y por eso la unidad de entrega es la ficha y no el pack: `v0.1` son 5-8 registros (`01` §5), con la cobertura declarando solo lo que hay. La alternativa era que sirviera mucho y a veces mal.
