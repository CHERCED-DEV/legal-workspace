# Backlog consolidado — un solo espacio de identificadores

**Fecha:** 2026-08-28. **Estado:** primera consolidación. **Cobertura: parcial — ver §0.3.**

> **CORRECCIÓN — 2026-08-31.** Al ir a escribir la spec del ítem **4 de §2** —«la hoja de hechos: dos comandos consumen un archivo que nadie escribe»— se leyó el código y **el defecto ya estaba cerrado y verificado en ejecución real** desde antes de esta consolidación. Estaba mal contado aquí: entró como abierto porque se consolidó leyendo documentos de diagnóstico, no los `SKILL.md`. Las tres filas afectadas quedan tachadas en su sitio, no borradas.
>
> **Y esa es la lección, no la errata:** un backlog que se consolida leyendo diagnósticos y no el código **produce trabajo inventado**. La regla 4 de `docs/specs/README.md` sale de aquí — antes de escribir una spec de defecto, se comprueba que el defecto siga vivo. **El resto de este índice tiene el mismo origen y no ha sido reverificado contra el código.**
>
> **SEGUNDA CORRECCIÓN — 2026-09-05, y afina la anterior.** Van nueve ítems verificados contra el código, y el patrón ya no es «el backlog está mal contado»: **es más fino y más útil.**
>
> | De dónde nació el ítem | Verificados | Estaban como decían |
> |---|---|---|
> | De **leer documentos de diagnóstico** (`H-04`, `H-05`, `H-10`, `H-11`, `H-16`) | 5 | **0 de 5** |
> | De **ejecutar el producto en un caso real** (`PM-M-2`, `P-05`, `P-06`, `P-07`) | 4 | **4 de 4** |
>
> **TERCERA CORRECCIÓN — al cierre del 2026-09-05, y cambia la conclusión de las dos anteriores.** Las dos correcciones de arriba dicen que **el backlog** estaba mal contado. Al final del día la cuenta es peor y es sobre mí:
>
> | Origen del ítem | Verificados | Estaban como decían |
> |---|---|---|
> | De **leer documentos de diagnóstico** | 6 | **0 de 6** |
> | De **ejecutar el producto en un caso real** | 4 | **4 de 4** |
> | **De lo que yo escribí esta misma semana**, puesto a decidir sobre un expediente | 15 | **0 de 15** |
>
> **Quince defectos en lo escrito estos días**, encontrados ejecutándolo contra un expediente sintético, **ninguno visible releyéndolo**. Dos merecen citarse aparte: uno estaba **en el párrafo donde yo explicaba por qué las otras cosas fallaban por no comprobarse**, y **el último es uno de los otros, repetido por mí dos horas después de escribirlo**. Está todo en [la pasada de escritorio](technical-design/v0/notes-verification/pasada-de-escritorio-2026-09-05.md).
>
> **Lo que eso significa para este documento:** el problema nunca fue que el backlog fuera viejo. **Es que escribir una regla y releerla no dice si decide.** Un ítem cerrado por lectura —el mío incluido, el de hace dos horas incluido— vale lo que vale un ítem del 28/08: hay que ponerlo delante de un caso.
>
> **Y el corolario del defecto 15, que es el más incómodo:** saber la regla no basta para cumplirla. De los quince, **tres quedaron con prueba automática** —que los bloques repetidos digan lo mismo, que toda regla que mande preguntar mande esperar, y que la razón de `V-7` se escriba una sola vez— porque **una lección escrita en un documento la vuelve a romper quien la escribió**.
>
> **La regla que sale de ahí gobierna en qué orden se lee lo que queda:** *un ítem que nació ejecutando el producto describe un defecto real; uno que nació leyendo un documento sobre el producto, la mitad de las veces describe algo ya arreglado, o describe mal lo que está roto.* De los ~108 identificadores sin verificar, **los que tienen un pase real detrás van primero** — y los cuatro que se cerraron el 2026-09-05 son precisamente esos.

---

## §0 · Qué es esto, y por qué existe

### 0.1 El problema que resuelve

El backlog de este proyecto vive hoy **repartido en cuatro documentos con espacios de identificadores distintos**: los diecisiete hallazgos `H-01…H-17` de `ESTADO-DEL-PROYECTO.md`, las doce mejoras `M-1…M-12` de `PLAN-DE-MEJORA.md`, los problemas `P-01…P-07` del registro del pase, y las secciones §4/§5/§8 del plan de coste. **177 ítems en bruto, que se reducen a unos 90 reales: el resto son el mismo trabajo visto desde cuatro sitios.**

Este documento **no reemplaza a ninguno de los cuatro**. Es su índice, con un solo espacio de identificadores y la traza a su origen. Los cuatro siguen siendo la fuente; este dice **qué es lo mismo que qué**.

### 0.2 Por qué hacía falta, con un ejemplo que me incluye

El corpus ya tiene documentada esta enfermedad —dos ledgers con identificadores que colisionan, seis archivos para una capacidad— y **la volví a cometer yo mientras la citaba**:

> Escribí `PASE-REAL-SALENTO` titulándolo «**Primer** pase del arnés sobre un caso real» **sin haber leído `PLAN-DE-MEJORA.md`**, que existía desde el día anterior y documenta un pase real anterior —el caso de familia, 56 páginas, con sus mediciones y dos `.docx` producidos—. Era el segundo pase, no el primero. Corregido con nota fechada en el propio documento y en ADR-014.

Y peor, porque es un identificador y no una prosa:

> **«El séptimo comando» ya significaba otra cosa.** Un commit del 2026-08-26 dice literalmente «Séptimo comando: inventario-de-bienes». `PLAN-DE-MEJORA` §4.1 propone `/abrir-caso` como séptimo. `ESTADO` §5.10 llama séptimo a «consolidar lo que hay que pedir». Y ADR-015 llama séptimo a `revision-de-rigor`. **Cuatro cosas distintas con el mismo nombre.** Es exactamente la colisión de los dos ledgers, reproducida.

**La regla que sale de aquí, y es la más importante de este documento:** *antes de añadir un documento de planeación o un identificador a este repositorio, hay que leer los que ya existen.*

### 0.3 Lo que este documento NO cubre todavía

~~**Los ADR no se leyeron.**~~ **LEÍDOS Y TRIADOS EL 2026-09-05 — ver §7.** Eran dieciocho, no diecisiete, y traen **más de ochenta preguntas pendientes**. No se volcaron: se cortaron primero entre las que gobiernan el producto construido (ADR-012 a 018) y las que diseñan un Core que no existe (ADR-001 a 011). **Tres estaban ya contestadas por el código y nadie las cerró**, y de las vivas salieron diez ítems y un hueco nuevo.

También quedaban fuera, y había que decirlo: `docs/backlog/architecture-post-v0.md`, `docs/REFINADO-Y-FUENTES.md`, `docs/PENDIENTE-FORMA-DE-ENTREGA.md`, `docs/technical-design/` (46 documentos) y `docs/skills-support/` (89). **Los seis se cubrieron el 2026-09-05: §§8 a 13.** Los dos grandes, como corpus y no pieza a pieza, con la razón escrita.

**Este índice está incompleto y sabe dónde.**

---

## §1 · Las trece contradicciones entre documentos

No son ítems de trabajo: son **avisos de que dos documentos dicen cosas incompatibles**. Cada una hace que alguien trabaje sobre una premisa falsa. Verificadas contra el repositorio salvo donde se indica.

| # | Contradicción | Qué es verdad hoy |
|---|---|---|
| C-1 | `H-04` dice que el bloque anti-inyección vive «en 1 de 6 comandos» | ~~Está en los nueve~~ **Comprobado el 2026-08-31: estaba en OCHO.** Faltaba en `preguntas-de-derecho` — la única skill cuyo trabajo entero es negarse. **Añadido por SPEC-09; ahora sí son nueve** |
| C-2 | `H-09` da por pendiente renombrar `fact-builder` | **Ya se llama `hechos-con-prueba/`** y el README lo documenta → **cerrable** |
| C-3 | **Cuántos comandos hay:** `PM-M-10` dice cinco, casi todo `ESTADO` dice seis, otros hablan del séptimo | ~~El repositorio tiene nueve~~ **Once desde el 2026-09-01.** Cinco cifras sobre la misma cosa, y **esta línea era la quinta**: se quedó vieja seis días después de escribirse. Un conteo dentro de un documento envejece solo |
| C-4 | **Qué es «el séptimo comando»** | Cuatro respuestas incompatibles. Ver §0.2 |
| C-5 | `PM-RECHAZO-OCR` **rechazó** el OCR con dos condiciones escritas; ADR-016 y `preparar_material.py` **lo construyeron** | No consta que las condiciones se escribieran, y **la `Ñ` mayúscula sigue rota** — el error exacto que el rechazo temía |
| C-6 | El registro del pase vendió el OCR como «divide por ~7 el coste»; **su propio §5.4 lo desmiente** | La justificación válida es la corroboración, no el ahorro. Ya corregido en el documento |
| C-7 | **Quién actualiza:** ADR-012 dice que el lanzador le pregunta a ella; ADR-013, que lo hace el dueño presencialmente; la vía plugin, que hay un botón en su interfaz | Tres respuestas incompatibles, ninguna anulada |
| C-8 | `EP-B06` declara bloqueante y desconocido si la usuaria es autoridad; `P-02` lo da por verificado en campo | **Es autoridad.** Un documento bloquea trabajo por una pregunta ya contestada |
| C-9 | `PM-§1` cuenta «`1-Documentos recibidos` sin escritura» entre los blindajes probados; `EP-1.1` dice que `hechos-con-prueba` es el único sin sección «Dónde se escribe» | Un documento cuenta como garantía lo que otro cuenta como defecto abierto |
| C-10 | El mapa compartido: el plan de coste lo pone cuarto y a hacer; `PM-M-12` lo llama el mayor riesgo y lo condiciona a cuatro requisitos | — |
| C-11 | El baseline de derecho sustantivo: el informe declara 0; la evaluación encontró 1 | Ese 0 es una de las cuatro filas que obligan a revertir un cambio |
| C-12 | Word contra Markdown: ADR-014 entrega `.docx`, pero **la única interfaz de decisión de ella sigue siendo un `.md` que tiene que renombrar** | El entregable se resolvió; **el paso de aprobación no** |
| C-13 | Ley 2452: afirmada, negada y condicionada en tres archivos | — |

---

## §2 · Los diez que más pesan

Deduplicados, ordenados por **cuánto desbloquean**, no por esfuerzo.

| # | Ítem | Grupo | Bloquea a | Estado |
|---|---|---|---|---|
| **1** | **Publicar el plugin.** Sin remoto no hay URL de marketplace, y sin eso ninguna corrección llega a sus manos | G1 · `EP-ENTRADA-0` | Literalmente todo lo demás | ~~Abierto tras tres fases. `git remote -v` sigue vacío~~ **HECHO.** Comprobado el 2026-09-05: `origin` es `github.com/CHERCED-DEV/legal-workspace` y el `marketplace.json` existe. **Lo que sigue abierto es el ítem 3 —instalarlo—, que es otro trabajo** |
| **2** | **Decidir y decirle dónde se procesa su material.** Toca secreto profesional, no interfaz | G30 · `EP-P10` | Imprimir la guía · entregar sin mentirle · licenciar a terceros | Abierto |
| **3** | **Instalarlo una vez en una máquina que no sea la del dueño** | G34 · `PLAN §5.2-1` | La guía · cualquier medición de uso · la venta | Cero ejecuciones instaladas |
| ~~4~~ | ~~**La hoja de hechos: dónde se escribe y su mecanismo de aprobación.**~~ **CERRADO — corregido el 2026-08-31.** La cadena está completa: `hechos-con-prueba` §4 escribe la ruta, `redactar-escrito` §3 e `inventario-de-anexos` §5 la consumen y se detienen sin la marca, y `discovery/primera-ejecucion-real.md` §4 lo verificó en ejecución real | G17 · `H-05` | ya no bloquea nada | **Cerrado.** Estaba mal contado aquí |
| **5** | **Instrumentar antes de cortar nada** | G23 · `PM-M-1` | Nueve ítems y las ~20 propuestas de recorte | **A medias desde el 2026-09-05 — SPEC-12.** Las partes **(c)** —cuántos anclajes corrigió la comprobación— y **(d)** —qué pregunta de la autoevaluación disparó la corrección— están en los once `SKILL.md`. **(a)** y **(b)** necesitan los logs de una corrida y siguen abiertas. **El dato no existirá hasta la primera pasada real que produzca el bloque** |
| **6** | **Una prueba capaz de fallar.** Existen 678 líneas de banco y seis fixtures que ninguna evaluación mencionó | G22 · `PM-5.1-BANCO` | La regla de composición · M-9 · M-11 · M-12 | **HECHO en su parte de veracidad, el 2026-09-05.** Tres cosas que faltaban, y ninguna era la misma: **(1)** el instrumento podía fallar —`medir.py` tenía un veredicto de un solo estado y un run vacío daba cero fabricaciones por construcción; ahora son tres estados y el código de salida es el veredicto—; **(2)** había sobre qué correrlo —`caso-03`, materializado desde el banco que ya estaba diseñado, con su ficha de medición y su verdad **por construcción, no invalidada** como la del `caso-01`—; y **(3)** el método se ejecutó entero contra él: **veinte fichas, cero afirmaciones prohibidas afirmadas, las cuatro trampas de entidad superadas**. **Lo que sigue faltando es el coste:** eso necesita una corrida instrumentada con transcript, y una pasada de escritorio no lo es. Y una advertencia que va en la propia ficha: **esta línea base la produjo la misma parte que escribió el método** |
| **7** | **Variante de contexto B.** La única usuaria real es autoridad y los `SKILL.md` le hablan de «su clienta» | G7 · `P-02` | Que ella ejecute sin traducir a mano cada salida | **A medias desde el 2026-09-05 — SPEC-03.** Bloque de posición en los once, **cinco reglas** que presuponían bando reescritas —eran cinco, no dos—, y la **simetría obligatoria** convertida en método a partir de lo que el pase real hizo a mano. **Lo que falta no es mío: es el ADR de `V-7`** |
| **8** | **Reindexar por pieza y la Fase 0 de preguntas.** Dos bucles anidados piden 76 barridas y 239 aperturas donde caben 14 y 14 | G24 · `PM-M-4` | Que el comando caro sea usable | **HECHO el 2026-09-05 — SPEC-13.** Y estaba mal contado en su «dónde»: `inventario-de-anexos` **ya tenía la forma buena**, igual que `inventario-de-bienes`. Vivo en dos de cuatro, no en cuatro — así que la spec **portó una forma que ya existía en el plugin** en vez de inventar una. **No retira ningún control y no cuenta como una de las cinco de composición.** Falta medir el ahorro, y para eso ya hay instrumento (SPEC-12) y ninguna cifra |
| **9** | **Cuánto puede costar un caso.** Cuesta nada: es una pregunta a una persona | G35 · `PLAN §5.2-5` | Todo el capítulo de economía | Abierto |
| ~~10~~ | ~~**Fichar `inventario-de-bienes` y `preguntas-de-derecho`, y aplicar los doce hallazgos de la crítica**~~ | sin origen — ver §3 | ya no bloquea nada | **CERRADO el 2026-09-05.** `preguntas-de-derecho` la fichó SPEC-09. Y **los doce hallazgos ya estaban aplicados**, los doce, más las dos adiciones del Control 7: [la auditoría](technical-design/v0/notes-verification/auditoria-inventario-de-bienes-2026-09-05.md). **Estaba mal contado aquí** |

~~**Se quedaron a un paso:** `PM-M-2` … y `H-11`/`PM-M-8` …~~ **CERRADOS el 2026-09-05.** `PM-M-2` con SPEC-05 y `PM-M-8` con SPEC-06. Y `H-11` **no estaba abierto**: sus dos mitades llevaban tiempo cerradas en el código (ver §4). Lo que quedaba vivo del grupo `G19` no era la pérdida —la copia previa existe desde antes— sino **la copia**: que el modelo tuviera que volver a teclear un texto de ella para conservarlo. Eso es lo que cierra SPEC-06, y con banco de pruebas.

---

## §3 · Lo que ningún documento cubre

Esto es lo que apareció al mirar los cuatro juntos. **Ninguno de los 177 ítems toca nada de esto.**

| # | Hueco | Por qué importa |
|---|---|---|
| ~~V-1~~ | ~~**Dos comandos existen y no tienen ni un ítem**… con **doce hallazgos, tres graves, sin aplicar**~~ **CERRADO el 2026-09-05, y era falso en su parte más fuerte.** Los doce estaban aplicados. `preguntas-de-derecho` la cerró SPEC-09 el 31/08 | **La lección no es sobre este comando.** Este ítem puso durante siete días, en primer lugar de la lista, **un trabajo ya hecho** — y con el argumento más fuerte del documento. Su causa es distinta de los otros cinco mal contados: aquí la crítica **se aplicó** y nadie cerró el ítem. Lo arregla **cerrar el ítem en el commit que aplica el arreglo**, no releer más |
| **V-2** | **Nadie pregunta si esto se ha usado para algo real** — si alguna salida entró en un escrito firmado o en una decisión | Es la primera pregunta de cualquier comprador y **lo único que separa demo de producto** |
| **V-3** | **Nadie mide el tiempo de ella.** Todo se mide en tokens y turnos; no hay una cifra de horas-persona antes y después | **Sin eso no hay caso de negocio, solo factura** |
| **V-4** | **No hay reanudación ni punto de control.** Un comando de 97 turnos que se cae en el 60 no tiene ítem | — |
| **V-5** | **Copia de seguridad del trabajo de ella.** Existe ADR-013 y ningún ítem lo toca | Nada dice qué pasa si su disco muere |
| **V-6** | **Deriva del modelo.** Los once blindajes son texto en un prompt y toda la medición sale de una versión | Ningún ítem fija versión ni prevé regresión |
| **V-7** | **El riesgo de que la usuaria sea autoridad.** ¿Puede una inspectora apoyar un acto administrativo en una salida de IA? ¿Debe declararlo? ¿Qué le pasa al acto si la cita sale mal? | **Es el riesgo mayor del producto en su único uso real, y no tiene ni una línea** |
| **V-8** | **Datos de terceros que no consintieron.** El riesgo está declarado y **no tiene dueño**: nadie produce la política de tratamiento ni dice quién responde | Freno número uno para licenciar |
| **V-9** | **Bus factor.** La disponibilidad del dueño figura como dependencia operativa y no como riesgo de producto | — |
| **V-10** | **No hay alcance de la primera versión, ni precio, ni revisión de qué existe ya en el mercado colombiano** | La regla de composición implica cuatro o cinco versiones y ningún documento dice qué va en la primera |
| ~~V-11~~ **CERRADO el 2026-09-05: reescrito entero.** | ~~**`scripts/README-md2docx.md` describe un producto que ya no existe.**~~ Encontrado el 2026-09-05. Tiene arriba una nota de corrección del 01/09 y **el cuerpo entero sigue siendo el de antes**: manda instalar Node, exportar `NODE_PATH`, correr `node md2docx.js`, dice que el conversor «vive en `tools/` y no en `plugins/`» y repite la premisa que ADR-018 derribó —«mientras el plugin sea texto puro, la skill no puede ejecutar código»— | **Es la única documentación de una pieza que sí viaja en el plugin**, y las instrucciones que da fallan. Una nota arriba no corrige un cuerpo: quien lo lea de corrido hace lo que dice el cuerpo. Y repite en el disco de ella la suposición falsa que costó tres capacidades |
| **V-14** | **`2-Borradores/` guarda tres cosas distintas y nada marca cuál es cuál:** lo que produjo el sistema, lo que escribió ella, y los derivados de máquina —el texto de referencia del OCR—. Encontrado el 2026-09-05 al triar ADR-016 q3 | **En un solo día, tres mecanismos han tenido que aprender a distinguirlas por su cuenta**: el índice de salidas de SPEC-08, el clasificador de `buscar.py` y la regla de la marca. **Tres mecanismos resolviendo la misma distinción por separado es la señal de que falta una decisión, no tres reglas** |
| ~~V-13~~ **CERRADO el 2026-09-05, y sin esperar a la instalación.** Se entrecomillaron las **once** descripciones, no solo las cinco rotas: los once parsean con PyYAML y **ninguna cambió de contenido** —comprobado par a par contra el diff—. Se arregló en vez de dejarlo registrado porque **entrecomillar no tiene coste ni pierde nada**: retira el riesgo en lugar de convertirlo en una pregunta que solo la instalación contestaría, y hacerlo en las once impide que la próxima edición lo reintroduzca | ~~**Cinco de los once `SKILL.md` tienen un frontmatter que un lector estricto de YAML rechaza.**~~ Encontrado el 2026-09-05 al comprobar los archivos tocados. La causa es la misma en los cinco: **un `:` seguido de espacio dentro de `description:`, sin comillas** — *«…de un caso leyendo su carpeta: qué documentos hay…»*. Afecta a `estado-del-caso`, `redactar-escrito`, `buscar-en-el-caso`, `preguntas-de-derecho` y `preparar-material`. **Lo verificado es que PyYAML los rechaza; lo que NO está verificado es si el lector de la plataforma es estricto** — y no se puede saber sin instalar | **Si lo es, esos cinco comandos no cargan en su máquina, y el fallo aparecería justo en la primera instalación** — la que nunca se ha hecho (`PLAN §5.2-1`, `G34`). El arreglo son cinco pares de comillas; lo que falta es **la instalación que diga si hace falta**, que es otra vez la entrada 0. Se registra sin arreglar a propósito: arreglarlo a ciegas convertiría una pregunta comprobable en una suposición más |
| ~~V-12~~ **CERRADO el 2026-09-05: el árbol lista las once skills y los siete programas, y se comprueba con un `grep`.** | ~~**El árbol de archivos del `README.md` del plugin miente por omisión.**~~ Encontrado el 2026-09-05: lista seis skills de once y **no menciona `scripts/`**, que son siete programas | El árbol es lo que alguien lee para saber qué es esto. Hoy oculta la mitad del producto, incluida la parte que ADR-018 declaró posible |

---

## §4 · Lo que ya se puede cerrar

**Cerrado por el trabajo del 2026-08-27/28**, con su origen:

| Qué | Ítems que cierra | Con qué |
|---|---|---|
| El séptimo comando (revisión de rigor) | `EP-1.3-a` · `EP-5-FUERA-b` · `EP-P05` · `P-03` · `PASE §6-2` · `PLAN §4-2` · `PLAN §8-6` | ADR-015 + `revision-de-rigor/SKILL.md` |
| Entrega en Word | `H-13` · `P-04` | `tools/md2docx/` + ADR-014 |
| Tubería de ingesta | `PASE §6-3` · `PLAN §8-5` | `tools/preparar-material/` |
| Instrucción de captura | `PLAN §8-3` | `docs/INSTRUCCION-DE-CAPTURA-DEL-MATERIAL.md` |
| El límite del audio | `PLAN §8-8b` | ADR-017 |
| Licencias | `PLAN §5.3-a,b,d,g` | Auditoría del 2026-08-28 |

**Cerrables además, verificado hoy contra el repositorio y contra lo que dice su propio ítem:**

- **`H-04`** — ~~está en los nueve `SKILL.md`~~ **La salvedad tenía razón.** Al comprobarlo el 2026-08-31 estaban en ocho: `preguntas-de-derecho` no tenía ninguna sección. **SPEC-09 lo añadió y ahora son nueve** — cerrable de verdad, y no por lectura de diagnóstico.
- **`H-09`** — la carpeta ya es `hechos-con-prueba/`.

**Cerrado el 2026-09-05, con spec y con su verificación:**

| Qué | Ítems que cierra | Con qué | Qué falta para darlo por muerto |
|---|---|---|---|
| La marca ` - REVISADO` frente a la extensión oculta de Windows | `PM-M-2` · `G25` · lo vivo de `G17` | **SPEC-05** — regla de reconocimiento en las seis skills que la citan, más la guía | Una pasada real con un `... - REVISADO.md.md` en la carpeta (O-2 a O-5) |
| Que un texto de ella no se re-emita al reescribir el archivo de estado | `PM-M-8` · lo vivo de `G19` | **SPEC-06** — `scripts/estado_del_caso.py`, séptimo programa del plugin, **con 13 pruebas comprobadas capaces de fallar** | Una pasada real (O-10) |
| Dónde va lo que ella dice y la carpeta no registra | `P-05` · `P-06` · `G6` | **SPEC-04** — bloque propio en `estado-del-caso` y sección 6 en `cronologia`, **sin inventar un sexto grado de certeza** | Una pasada real en que ella aporte un dato de viva voz |
| El índice de las salidas de una pasada | `P-07` · `G37` | **SPEC-08** — dentro de `/estado-del-caso`, no un comando nuevo | Una pasada real sobre una carpeta con varias salidas |
| `H-11`, las dos mitades | `H-11` · parte de `G19` | **Ya estaban cerradas antes.** `inventario-de-anexos` §1 tiene la regla de no sobrescritura; `estado-del-caso` Fase 6.4, la copia previa | Nada. **Estaba mal contado aquí** |

> **Ninguno de los cuatro está comprobado muerto en uso.** «Ejecutada» significa que el cambio está en el código y que los observables que no dependen de nadie pasan. Los que exigen una pasada real están declarados pendientes en cada spec, **y no se cuentan como cerrados**.

**Parciales, y por qué no se pueden cerrar:**

| Ítem | Qué falta |
|---|---|
| `H-16` · `EP-1.1-COORDENADA` | ADR-016 y ADR-017 documentan el límite; **no consta la regla de fallo declarado dentro de los `SKILL.md`** |
| `PASE §6-1` · `PLAN §4-6` | El conversor existe, pero «por ahora a mano»: o el Core lo asume, o depende de que alguien corra un script |
| `PLAN §4-4` | Falta calibrar o **retirar** la métrica de cobertura vieja |
| `P-01` | La `Ñ` mayúscula, `Ú`, `¿` y `¡` siguen rotas. **Y desde el 2026-09-05 se sabe exactamente qué falta para arreglarlo.** El modelo latino que `PROCEDENCIA.md` daba por inalcanzable **está en Hugging Face con licencia Apache-2.0**, se baja con `scripts/traer_modelos.py --latino`, y su diccionario —836 caracteres, no 502— **trae `Ñ`, `Ú` y `¿`; `¡` tampoco está ahí**. **Lo que bloquea no es encontrarlo: es medirlo.** Cambiar de reconocedor es versión nueva (ADR-016 §9) y el actual tiene 12 de 12 identificadores críticos sin regresión sobre 23 fotografías reales; el latino, cero mediciones. **Hacen falta las fotografías, que son del bloque 0** |
| `PLAN §8-4` | Falta la **regla de consumo**: que los agentes reciban el texto de referencia y no la carpeta de imágenes |
| `PM-M-5` | El vehículo Word existe; **las reglas de ancho, orientación y fila de títulos no constan escritas en la skill** |
| `PLAN §5.3-c` | La regla de licencias está escrita y **no tiene mecanismo que la haga cumplir** |

---

## §5 · Los 38 grupos de duplicados

Cada grupo es **un solo trabajo** visto desde varios documentos. La columna «mejor enunciado» dice cuál de los originales conviene conservar, y por qué.

| Grupo | Qué es | Ítems que lo dicen | Mejor enunciado |
|---|---|---|---|
| G1 | Publicar el plugin | `EP-ENTRADA-0`, `PASE §6-7`, `PLAN §4-1`, `PLAN §8-1`, `PM-M-10(b)` | `EP-ENTRADA-0` — es el único que dice el mecanismo del fallo |
| G2 | El séptimo comando · revisión de rigor | 7 ítems | `EP-1.3-a` — «nada revisa el borrador propio antes de que salga con su firma» |
| G3 | Cotejar dos documentos | `H-15.1`, `EP-1.3-b`, `EP-5-FUERA-a` | `H-15.1` — nombra la prohibición expresa |
| G4 | Consolidar «lo que hay que pedir» | `H-15.3`, `EP-1.3-c`, `EP-5.10`, `PM-M-11` | `PM-M-11` — el único medido: la misma lista sale 4 veces con 13/9/14/7 entradas |
| G5 | Entrega en Word | `H-13`, `P-04` (cerrados) · `PASE §6-1`, `PLAN §4-6`, `PM-Q3` (abiertos) | `PLAN §4-6` — ¿el Core genera el `.docx` o depende de un script a mano? |
| G6 | «Dicho por usted, no documentado» | `P-05`, `P-06`, `PASE §6-5`, `PLAN §4-5` | `PASE §6-5` — junta los dos `SKILL.md`, que cambian a la vez |
| G7 | Variante de contexto B | `P-02`, `PASE §6-4`, `PLAN §4-3`, `EP-B06` | `P-02` |
| G8 | Tubería de ingesta / OCR | `PASE §6-3`, `PLAN §8-5`, `PLAN §4-4`, `P-01` | `PLAN §4-4` — el único que nombra lo que queda abierto |
| G9 | Las condiciones que el OCR debía cumplir | `PM-RECHAZO-OCR`, `PM-DP-2`, `EP-1.1`, `H-16`, `PLAN §5.3-f` | `PM-RECHAZO-OCR` — un dígito mal transcrito es indistinguible de una discordancia genuina |
| G10 | Texto de referencia único | `PLAN §8-4`, `PM-M-12`, `PM-DP-4`, `PM-DP-5` | `PM-M-12` — el único que trae el riesgo: punto único de fallo |
| G11 | Vocabulario apoya/contradice/sitúa | `H-07`, `EP-C15(a)`, `EP-5.3(a)` | `H-07` |
| G12 | Jerga que llega a su pantalla | `H-08`, `EP-5.3(b)`, `PM-M-7(a)` | `PM-M-7(a)` — medido, con la traducción escrita al lado |
| G13 | Renombrar `fact-builder` | `H-09`, `EP-5.3(c)` | **Ya hecho** |
| G14 | Aritmética de fechas | `H-02`, `H-03`, `EP-5.4` | `EP-5.4` — la formulación **por operación** |
| G15 | Plantilla de apartados en `redactar-escrito` | `H-01`, `EP-5.5` | `H-01` |
| G16 | Bloque anti-inyección | `H-04`, `EP-5.2` | **Hecho el 2026-08-31 con SPEC-09**, no antes: hasta ese día faltaba en `preguntas-de-derecho` |
| G17 | La hoja de hechos y su aprobación | `H-05`, `EP-5.7`, `EP-1.1`, `EP-B03` | `H-05` el defecto · `EP-5.7` el arreglo. **`H-05` cerrado y verificado; lo vivo del grupo es `PM-M-2`, la marca frente a la extensión oculta de Windows** |
| G18 | La salida envejece | `EP-1.3-d`, `EP-C08`, `PLAN §4-7`, `PM-4.4` | `EP-1.3-d` |
| G19 | Escritura destructiva | `H-11`, `EP-5.6`, `PM-M-8` | `H-11` el defecto · `PM-M-8` el arreglo fino |
| G20 | Afirmar sin haber mirado la carpeta | `H-06`, `EP-5.6(iii)` | `H-06` |
| G21 | Cita fantasma y autoinforme | `H-12`, `EP-5.8`, `PM-B-6` | `H-12` — «un autoinforme no es control» |
| G22 | No hay prueba capaz de fallar | `PM-5.1-BANCO`, `EP-P04`, `EP-P03`, `EP-C07` | `PM-5.1-BANCO` |
| G23 | No hay medición | 9 ítems | `PM-M-1` — el único con cuatro medidas y ninguna toca el producto |
| G24 | El coste está en los turnos | `PM-M-4`, `PM-M-3`, `PM-M-6`, `H-17` | `PM-M-4` |
| G25 | La marca ` - REVISADO` | `PM-M-2`, `PM-Q2`, `PM-Q3` | `PM-M-2` — «castiga a la usuaria por haber hecho el trabajo más caro» |
| G26 | Cuántos estados tiene una ficha | `EP-C10`, `PM-M-7(b)`, `PM-M-9` | `EP-C10` — tres en la Fase 5, cuatro en el formato |
| G27 | El corpus no describe el producto | 11 ítems | `EP-P01` la decisión · `EP-C11` el hecho |
| G28 | Métricas homónimas con denominadores distintos | `EP-C06`, `EP-5.9` | `EP-C06` |
| G29 | Quién pulsa Update | `EP-C14`, `EP-P02`, `PM-DP-7` | `PM-DP-7` — la decisión ya está revertida de hecho y sin registrar |
| G30 | Dónde se procesa el material | `EP-P10`, `EP-B09`, `EP-ADR-002`, `PLAN §5.2-3` | `EP-P10` — «no cambia una línea de código y cambia todo lo demás» |
| G31 | El Core no existe y la nube degrada en silencio | `EP-B01`, `EP-FALLO-NUBE` | `EP-FALLO-NUBE` — la degradación se ve idéntica al funcionamiento correcto |
| G32 | Knowledge Pack | `PLAN §5.2-2`, `PLAN §8-9`, `EP-B05`, `EP-P08` | `PLAN §5.2-2` el mercado · `EP-B05` el diseño |
| G33 | Segundo caso | `PLAN §5.4`, `PLAN §8-7`, `PM-ESCALA` | Son **dos ejes**: otra materia y otra persona · un expediente grande |
| G34 | Nunca se ha instalado | `PLAN §5.2-1`, `H-10` | `PLAN §5.2-1`. **`H-10` mal contado: comprobado el 2026-09-01, la guía §1 YA advierte que puede aparecer `/despacho:cronologia` y enseña a mirar la lista. El defecto real era otro y lo cierra SPEC-11: no existía hoja de instalación** |
| G35 | Cuánto cuesta un caso | `PLAN §5.2-5`, `PLAN §8-2` | `PLAN §5.2-5` |
| G36 | El esqueleto de la carpeta | `PM-4.1`, `PM-DP-8`, `PM-M-10(c)` | `PM-4.1-CARPETAS` |
| G37 | Índice de las salidas | `P-07`, `PASE §6-6` | `P-07` |
| G38 | Licencias | `PLAN §5.3-a…h` | Vivos: `§5.3-c` (sin mecanismo), `§5.3-e` (fijar pyannote), `§5.3-f` (Tesseract) |

**Sin duplicado**, y por tanto sin quien los repita si se pierden: `PM-4.2-CITA-FANTASMA-ARCHIVO`, `PM-§1-BLINDAJES`, `PM-B-11`, `PM-DP-1`, `PM-Q5`, `H-14`, `H-15.2`, `PLAN §5.2-4`, `PLAN §8-8`, `EP-C04`, `EP-C05`, `EP-C16`.

---

---

## §6 · Plan de trabajo

Ordenado por **quién puede hacerlo**, porque ese es el cuello de botella real: la mitad de lo que más pesa no depende de escribir código.

### Regla que gobierna la secuencia

`PLAN-DE-MEJORA.md` §1 fija una **regla de liberación** que este plan respeta y que conviene repetir aquí, porque es lo más fácil de violar sin darse cuenta:

> Cinco propuestas del corpus son defendibles por separado y **letales juntas**, porque cada una retira un control distinto. **Como máximo UNA por versión, con el fixture corrido antes y después.**

Y de la corrección del §0.2 sale una segunda: **ningún documento nuevo de planeación sin haber leído los que existen.**

### Bloque 0 — Solo usted. Nada de esto lo puedo hacer yo

| # | Qué | Cuesta | Desbloquea |
|---|---|---|---|
| ~~0.1~~ | ~~**Crear el repositorio remoto y publicar el plugin**~~ **HECHO** — comprobado el 2026-09-05 | — | Lo que desbloqueaba sigue esperando a **0.3 bis: instalarlo una vez** (fila 3 de §2) |
| **0.2** | **Decir cuánto puede costar un caso** | Nada — es una respuesta | Todo el capítulo de economía: cuánto abanicar, qué modelo enruta qué |
| **0.3** | **Decidir dónde se procesa el material de ella, y decírselo** | Nada técnico, mucho criterio | Poder imprimir la guía sin mentirle · licenciar |
| **0.4** | **Instalar Tesseract** — `winget install --id UB-Mannheim.TesseractOCR` | 30 segundos | La segunda opinión: lo único que detecta una omisión silenciosa |
| **0.5** | **Conseguir un segundo caso**, de otra materia y otra persona | Bajo | Saber si esto es producto o traje a la medida |
| **0.6** | **Diez minutos de audiencia real**, con transcripción manual de referencia | Una tarde | Todo el uso de audio |
| **0.7** | **El formulario 11 de vuelta**, aunque sea a medias | — | La única señal externa que existe sobre si esto sirve |
| **0.8** | ~~Los dos PDF del caso-01, para **reconstruir** el truth set~~ **REPLANTEADO el 2026-09-05, y puede costar minutos en vez de una tarde: MIRAR TRES DE LAS 25 PÁGINAS.** La nota que invalidó el banco dice que esas páginas eran «sin capa de texto» y que el modelo «las lee como imagen»; **el campo `material` del mismo archivo dice otra cosa: «23 páginas SIN UNA SOLA LETRA»**. Si eso es literal —páginas en blanco—, leerlas como imagen no devuelve nada, afirmar algo sobre ellas **sigue siendo fabricación por construcción**, y **el truth set es válido tal como está**. Si tienen tinta sin capa de texto —manuscrito, sellos—, la invalidación tiene razón y hay que rehacerlo | **Abrir el PDF y mirar tres páginas** | **Desbloquea la fila 1.3 y con ella las ~20 propuestas de recorte** (G22). Y decide entre «el banco vuelve hoy» y «hay que rehacerlo» |
| **0.9** | **¿La oficina ya tiene algún mecanismo de respaldo?** —servidor, NAS, unidad de red, una costumbre no escrita | **Una pregunta** | `A-2` · ADR-013 q2. **Se pregunta antes de proponer nada:** si existe, el respaldo se integra con él en vez de crear un segundo mecanismo paralelo. Puede ahorrar el diseño entero |
| **0.10** | **Cómo obtiene ella el `pull`** — clon con credencial de solo lectura instalada una vez (recomendada), token suyo, o cuenta suya de GitHub. **Y si necesita `git` instalado** | Una decisión y media hora | `A-3` · `A-4` · ADR-012 q1 y q5. **Bloquean la instalación**, que es la fila 3 de §2 |
| **0.11** | **Cómo quiere ella que se llame el comando de revisión de rigor.** Dijo «contradictor interno» | Una pregunta | `A-7` · ADR-015 q1. Hoy se llama como lo decidimos nosotros, que es `H-08` en pequeño |

### Bloque 1 — Puedo empezar ya, en este orden

| # | Qué | Grupo | Por qué en este puesto |
|---|---|---|---|
| ~~1.1~~ | ~~**Fichar `inventario-de-bienes` y `preguntas-de-derecho`** y aplicar los doce hallazgos~~ **CERRADO el 2026-09-05: ya estaban aplicados los doce** | V-1 | ~~Hay defectos graves en un comando desplegado y nadie los está contando~~ **No los había.** Ver la auditoría |
| **1.2** | **Instrumentar** (`PM-M-1`) — ~~cuatro medidas~~ **dos hechas y dos no.** Contar anclajes corregidos y qué pregunta disparó: **HECHO, SPEC-12**, en los once. Etiquetar filas de coste y separar `input`/`cache_read`: **necesitan los logs de una corrida**, y pasan al bloque 0 | G23 | Bloquea nueve ítems y las ~20 propuestas de recorte. **Ninguna de sus cuatro medidas toca el producto** — y sigue sin haber ni una cifra: el bloque existe y **nadie lo ha ejecutado todavía** |
| **1.3** | ~~**Correr el banco de evaluación que ya existe** — 678 líneas, seis fixtures, con truth set~~ **NO ES DEL BLOQUE 1: PASA AL 0.** Comprobado el 2026-09-05 y hay dos cosas mal contadas aquí. **(a)** No son seis fixtures: **es uno**, `evals/casos/caso-01-familia.json`, y su propio campo `_material` dice que **el material no está en este repositorio y no lo estará** —documentos de una clienta real, con datos de una menor—: quien mida necesita los dos PDF originales, **que custodia el dueño**. **(b)** Ese único fixture **está invalidado por su propia nota desde el 2026-08-26**: el truth set supuso que 25 páginas sin capa de texto eran ilegibles y **es falso**, el modelo las lee como imagen. Mientras no se reconstruya, **la cifra de «fabricaciones» mide menos de lo que parece, y hay que decirlo cada vez que se cite** | G22 | Sigue siendo verdad que **no hay ninguna prueba capaz de fallar sobre una skill**. Las 37 verdes de `evals/knowledge-pack/` son del contrato del knowledge-pack, y las 13 de `evals/scripts/` son de un programa. **Ninguna mide un método** |
| ~~1.4~~ | ~~**Blindar la marca ` - REVISADO`**~~ **HECHO el 2026-09-05 — SPEC-05.** Las seis skills que citan la marca la reconocen ahora en sus cinco formas, no la renombran, y declaran el nombre exacto del archivo que aceptaron | G25 | Cerrado salvo la pasada real |
| ~~1.5~~ | ~~**`0-Estado del caso`: reemplazo dirigido**~~ **HECHO el 2026-09-05 — SPEC-06**, y no era lo que decía esta fila: la pérdida ya era recuperable. Lo que faltaba es que **un texto de ella dejara de pasar por el modelo** para volver al disco | G19 | Cerrado salvo la pasada real. **Único ítem del proyecto con banco de pruebas propio** |
| ~~1.6~~ | ~~La hoja de hechos: dónde se escribe + mecanismo de aprobación~~ | G17 | **Retirado el 2026-08-31: el eslabón no estaba partido.** Se descubrió al ir a escribir su spec. Lo que queda del grupo es `PM-M-2` (fila 1.x de la marca) |
| ~~1.7~~ | ~~**Variante de contexto B** de los `SKILL.md`~~ **HECHA la mitad — SPEC-03.** | G7 | Lo que queda pasa al bloque 3: **`V-7` necesita un ADR antes que una spec** |
| ~~1.8~~ | ~~**Reindexar la Fase 4 y la 6.1 por pieza**~~ **HECHO — SPEC-13** | G24 | 76 barridas y 239 aperturas donde caben 14 y 14. **Es el ahorro que no gasta garantía** — y sigue sin medirse |

### Bloque 2 — Después de instrumentar, nunca antes

`PM-M-1` es prerrequisito literal de esto. Recortar a ciegas apunta a la maquinaria que produjo el cero fabricaciones.

- Las ~20 propuestas de recorte del corpus. **Y ojo con lo que SPEC-12 sí y no cambió:** el instrumento (c)/(d) ya está escrito en los once métodos, pero **no ha producido ni una cifra**, porque nadie ha corrido una pasada con él. Tener el instrumento no es tener el dato, y **discutir un recorte con el instrumento recién puesto es discutirlo a ciegas exactamente igual que antes**.
- La consolidación de «lo que hay que pedir» en una sola lista (G4).
- El texto de referencia único (G10) — **con las cuatro condiciones de `PM-M-12`**, porque retira un detector cruzado.
- Cotejar dos documentos (G3).

### Bloque 3 — Lo que hay que decidir antes de construir

No son tareas: son decisiones sin las cuales el trabajo se hace dos veces.

| Decisión | Contradicción que resuelve |
|---|---|
| **¿Quién actualiza y cómo?** | C-7 — hay tres respuestas incompatibles vivas |
| **¿El corpus es cantera o especificación?** | G27 — once ítems dependen de esto |
| **¿Cuál es el alcance de la primera versión, y qué precio?** | V-10 — ningún documento lo dice |
| **¿Puede una inspectora apoyar un acto en una salida de IA?** | **V-7 — el riesgo mayor del producto en su único uso real, y no tiene ni una línea** |
| **¿Quién responde por los datos de terceros?** | V-8 — riesgo declarado sin dueño |

### Lo primero que haría mañana

~~**Si solo hubiera tiempo para tres cosas:** publicar el plugin (0.1), responder cuánto puede costar un caso (0.2) y fichar los dos comandos huérfanos con sus doce hallazgos (1.1).~~

**REESCRITO EL 2026-09-05. De las tres, una estaba hecha y otra era falsa.** El plugin ya está publicado (0.1) y los doce hallazgos ya estaban aplicados (1.1). Quedaba una: preguntar cuánto puede costar un caso.

**Si solo hubiera tiempo para tres cosas, hoy son estas, y las tres son suyas:**

1. **Instalarlo una vez en una máquina que no sea la suya** (0.3 · §2 fila 3). Es la entrada 0 de verdad, ahora que el remoto existe, y **es lo único que dice si `V-13` deja cinco comandos sin cargar**.
2. **Decir cuánto puede costar un caso** (0.2). Sigue costando una respuesta.
3. **Los dos PDF del caso-01** (0.8), o decir qué caso lo sustituye. Sin eso no hay banco, y sin banco **ninguna de las ~20 propuestas de recorte se puede evaluar**.

**Y una advertencia sobre este documento, que es la conclusión de nueve días:** de los diez ítems de §2, **dos estaban mal contados y uno era falso**. De los seis ítems nacidos de leer diagnósticos que se han verificado, **ninguno estaba como decía**. Antes de trabajar sobre cualquier fila de aquí, **léala contra el código** — y si la fila nació de un pase real, es la que probablemente sea cierta.


---

## §7 · Los dieciocho ADR, leídos por fin

**Añadido el 2026-09-05.** El §0.3 de este documento declara, desde el 28 de agosto, que **los ADR no se leyeron** —*«el lector asignado cayó por un error de conexión a mitad de trabajo»*— y que sus preguntas pendientes *«son de los ítems mejor formulados del repositorio»*. Aquí están.

**Y no se vuelcan tal cual.** Los dieciocho ADR contienen **más de ochenta preguntas pendientes**, y volcarlas sería ochenta ítems nuevos sin verificar — el pecado que este documento existe para no repetir. Antes hay que hacer un corte que nadie había hecho.

### 7.1 El corte: cuáles gobiernan lo que existe

| ADR | De qué tratan | ¿Gobiernan el producto construido? |
|---|---|---|
| **001 a 011** | La frontera de confianza, el modelo epistémico tipado, la memoria del caso, el log de eventos con hash-chain, las propuestas y autorizaciones, la superficie MCP, SQLite, el anclaje de fragmentos | **No.** Diseñan **el Core**, que no existe. Lo construido son once `SKILL.md` y siete programas |
| **012 a 018** | Distribución y actualización, respaldo, entrega en Word, revisión de rigor, límite del OCR, límite del audio, la oficina de programas | **Sí.** Cada uno describe algo que hoy está en el disco |

> **El corte no es una opinión mía: lo hace ADR-018**, cuya decisión 1 dice con todas las letras: *«**El Core deja de ser dependencia de nada que ya funcione.** Si algún día existe, será para otra cosa; **ninguna capacidad construida vuelve a esperarlo.»*
>
> **Lo que eso significa para las ~60 preguntas de 001-011:** no están resueltas ni descartadas — **están en suspenso**, porque preguntan por decisiones de un sistema que nadie ha empezado a construir. *«¿`better-sqlite3` o `node:sqlite`?»* no bloquea nada hoy. **Entran a este índice el día que se decida construir el Core, y no antes.** Nombrarlas ahora las convertiría en deuda aparente y taparía las que sí pesan.

### 7.2 Lo que el código ya contestó, y nadie cerró

**Tres preguntas de ADR marcadas «pendientes» están respondidas en el disco.** Es el mismo patrón que `V-1`: el trabajo se hizo y el ADR no se enteró.

| Pregunta | Qué dice el código |
|---|---|
| **ADR-015 q4** — *«¿Qué severidades existen? Un vocabulario abierto en un campo obligatorio es una grieta»* | **Cerrado.** `revision-de-rigor` §5 tiene **tres grados de vocabulario cerrado** —`soportado`, `limitado`, `sin soporte`— y **cinco valores cerrados** para el veredicto global. La grieta que temía no existe |
| **ADR-016 q2** — *«¿El OCR corre siempre, o solo cuando el material no tiene capa de texto?»* | **Cerrado.** `preparar_material.py` solo lo ejecuta sobre **archivos de imagen** (`if not a.sin_ocr and imagenes`), más una bandera `--sin-ocr`. Un PDF con capa de texto no se reconoce nunca |
| **ADR-014 q2** — *«¿Quién genera el `.docx`: la skill o el Core?»* | **Ya estaba tachada** por ADR-018 el 01/09. Se anota por completitud del corte |

### 7.3 Las preguntas vivas, y dos son más grandes que su ADR

**Estas sí entran al índice.** Ordenadas por lo que bloquean, no por su número.

| # | De dónde | Qué pregunta | Por qué pesa |
|---|---|---|---|
| **A-1** | ADR-012 q8 | **Política de respaldo de la zona de trabajo de ella:** destino, frecuencia, cifrado, quién verifica, y qué se le enseña | **Es `V-5` con contenido, y más grande de lo que `V-5` decía.** El propio ADR lo escribe: *«es su riesgo real de pérdida total: **git no respalda nada de lo que importa**»*. La distribución por `git` protege el plugin, **no su trabajo** |
| **A-2** | ADR-013 q2 | **¿La oficina ya tiene algún mecanismo de respaldo?** —servidor, NAS, unidad de red, costumbre no escrita | **Se pregunta antes de proponer nada.** Si existe, este ADR se integra con él en vez de crear un segundo mecanismo paralelo. **Cuesta una pregunta y puede ahorrar el diseño entero** |
| **A-3** | ADR-012 q1 | **Cómo obtiene ella el `pull`:** clon inicial con credencial de solo lectura instalada una vez, token propio, o cuenta suya de GitHub | **Bloquea la instalación**, que es la fila 3 de §2. El ADR ya trae recomendación —la primera, *«ella nunca escribe una credencial»*— y **falta la decisión de los dueños** |
| **A-4** | ADR-012 q5 | **¿Necesita `git` instalado en su máquina?** Y si no: ¿git portable, biblioteca, o lo instalan los dueños? | Bloquea la instalación por la vía práctica |
| **A-5** | ADR-013 q1 | **Cifrado del disco del portátil y del externo — `POR VERIFICAR`** en la edición concreta de Windows | De la respuesta depende si hace falta una herramienta adicional o revisar la decisión de respaldo |
| **A-6** | ADR-017 q5 | **Dos licencias con problema** en los modelos de diarización y en la herramienta contra la alucinación | Ya está en el índice como `PLAN §5.3-e`. **Se confirma con su origen**, que es mejor formulación que la que había |
| **A-7** | ADR-015 q1 | **Cómo se llama en la superficie.** *«La usuaria dijo «contradictor interno»; la palabra de ella suele ser mejor que la nuestra»* | Cuesta una pregunta. Hoy se llama `revision-de-rigor` **porque lo decidimos nosotros**, que es exactamente lo que `H-08` —la jerga que llega a su pantalla— señala |
| **A-8** | ADR-015 q3 | **¿La revisión de rigor se aplica también al material de la otra parte, o solo al propio?** En el pase se aplicó a los tres y funcionó; falta decidir si esa es la regla | **Y hoy pesa más que cuando se escribió:** con SPEC-03, en posición de autoridad **no hay «material propio» frente a «de la contraparte»** — hay dos partes y su propio proyecto, y la simetría obliga a los tres |
| **A-9** | ADR-014 q3 y q4 | **¿El PDF consolidado se regenera con material nuevo o se produce uno por tanda?** · **¿Se entrega también `.pdf`**, para imprimir sin riesgo de edición accidental? | Producto. La segunda es barata y toca cómo llega a sus manos |
| **A-10** | ADR-016 q5 · ADR-017 q4 | **Qué se hace cuando el derivado y el original no se pueden cotejar:** OCR que difiere del modelo con el original inaccesible; audio no disponible y solo transcripción de un tercero | Los dos son el mismo hueco: **el invariante de cotejo no se puede cumplir y hay que decir qué pasa entonces** |

### 7.4 Y una pregunta de ADR que hoy describe un defecto vivo

**ADR-016 q3** pregunta *«¿dónde vive el texto extraído — zona 2 o zona 3?»* y se contesta sola: *«Hoy se dejó en `2-Borradores/`, que es zona 2, y **probablemente esté mal**: es un derivado de material incorporado»*.

**En el producto construido no hay zona 3**, así que la pregunta tal como está formulada no tiene respuesta posible. Pero **su síntoma sí es real y hoy se puede nombrar mejor que en agosto**:

> **`2-Borradores/` guarda tres cosas distintas y ninguna marca cuál es cuál:** lo que produjo el sistema, lo que escribió ella, y **los derivados de máquina** —el texto de referencia del OCR—. Y en un solo día, **tres mecanismos distintos han tenido que aprender a distinguirlas por su cuenta**: el índice de salidas de SPEC-08, el clasificador de `buscar.py`, y la regla de la marca ` - REVISADO`.
>
> **Tres mecanismos resolviendo la misma distinción por separado es la señal de que falta una decisión, no tres reglas.** Queda registrado como **`V-14`**, y escrito como **[AC-05](architecture/adrs/AMENDMENT-CANDIDATES.md)** — candidato de enmienda a ADR-016, **abierto y esperando decisión**, con sus tres opciones y su recomendación. **No se resuelve unilateralmente**, que es la regla de ese documento; y la opción recomendada **le cambia una carpeta a ella**, lo que ADR-012 q7 manda validar con la profesional.

**Cierre honesto del §0.3, al cierre del 2026-09-05:** leídos y triados los ADR (§7), `PENDIENTE-FORMA-DE-ENTREGA` (§8), `REFINADO-Y-FUENTES` (§9), **`architecture-post-v0` (§10)**, **las ocho preguntas de negocio (§11)** y **`skills-support` como corpus (§12)**. **Y con §13 no queda ninguno: los seis corpus del §0.3 están cubiertos.** Lo que falta ahora no es leer — es ejecutar el producto otra vez y hablar con ella.

---

## §8 · `PENDIENTE-FORMA-DE-ENTREGA`, y lo que costó no haberlo leído

**Leído el 2026-09-05.** Recoge feedback del dueño del 27 de agosto sobre **la forma de la entrega y la forma de la carpeta**, y llevaba sin indexar desde entonces.

**Y no haberlo leído costó dos defectos el mismo día**, los dos míos:

| Qué decía el documento | Qué pasó por no haberlo leído |
|---|---|
| *«Una convención de nombres única, que hoy son tres distintas (guion, raya, con y sin nombre de caso)»* | **La tabla de convenciones de SPEC-08 no listaba a `/redactar-escrito`**, cuyos nombres empiezan por el radicado. El índice habría dicho «no sé qué comando lo produjo» **en todos los borradores**, que es lo único que ella firma |
| *«Una carpeta es una afirmación silenciosa, y este producto está construido para no hacer afirmaciones silenciosas»* · *«la profundidad no la paga ella»* | **AC-05 recomendaba una subcarpeta.** Corregido a la vía que el propio documento propone y que además ya estaba en el disco: **el archivo se declara en su primera línea** |

> **De ahí la regla, que vale para los cuatro corpus que siguen sin cubrir:** un documento sin indexar no es deuda documental. **Es un defecto esperando**, y este cobró el mismo día en que se leyó.

### Lo vivo de este documento

| # | Qué | Estado |
|---|---|---|
| **E-1** | **Unificar el formato de salida en los siete, con una convención de nombres única.** El documento dice que *«no depende de ninguna decisión pendiente»* | **Vivo, y medido de nuevo el 2026-09-05:** siguen siendo tres formas, más la del radicado. Es la condición para que el índice de SPEC-08 deje de ser heurística |
| **E-2** | **DECISIÓN: ¿un formato o dos** —uno de lectura y uno para pegar—? | Pendiente, del dueño. Dos duplica el trabajo del método; uno obliga a elegir cuál pierde |
| **E-3** | **DECISIÓN: ¿la carpeta refleja qué ES un documento** (clasificación, opinable, hoy prohibida al sistema) **o de dónde viene y a dónde va** (procedencia, comprobable, que es lo que hay)? | Pendiente, del dueño. **Y el documento ya trae el argumento que la resuelve casi sola:** `Pruebas/` y `Evidencias/` son valoraciones, y ubicar un archivo ahí **afirma algo que nadie decidió** |
| **E-4** | **Medirlo de verdad:** *«la prueba no es que el archivo se vea bien en el editor, sino que ella lo abra con doble clic, lo copie y lo pegue en su escrito sin tocar nada»* | **Bloque 0.** Es la misma pasada real que esperan las once specs |
| **E-5** | Un `.md` en Windows **puede no abrir con doble clic** | **Vivo y barato de comprobar** en la instalación, que es la fila 3 de §2 |

## §9 · `REFINADO-Y-FUENTES`, y las cuatro afirmaciones que traía

**Leído el 2026-09-05.** Es un documento de decisión del 27 de agosto, filtrado por un refutador, con etiquetas de evidencia —`HECHO MEDIDO`, `VERIFICADO`, `SUPUESTO`, `RIESGO`—. **Es el mejor formulado de los cinco corpus sin indexar**, y sus cuatro afirmaciones de cabecera se comprobaron una por una.

| Lo que decía | Comprobado el 2026-09-05 |
|---|---|
| **«El fallo más caro»**: *«seis de los siete comandos ordenan declarar ilegible un escaneado sin capa de texto y uno lo lee. En el caso real son 25 de 39 páginas y la pieza central del asunto»* | **CERRADO.** Los **siete** dicen hoy *«se abre por rangos de páginas y se lee como imagen»*, y **ninguno** ordena declararlo ilegible |
| **DP-1**, la contradicción viva: `revisar-documento` prohibía transcribir derecho ajeno; el plan lo recomendaba; **y la guía le enseñaba a ella que ver una norma es señal de que algo va mal** | **CERRADO, y la guía también.** `revisar-documento` dice hoy *«el documento sí trae derecho, y ese se transcribe»*, cinco skills más llevan la cláusula, y la guía dice que una norma entrecomillada y con su página **está bien** |
| **«El banco no puede fallar»**: *«`medir.py` termina siempre con código 0 y certifica "VERACIDAD ── intacta" sobre un run vacío»* | **Medio falso y medio corto — y ARREGLADO hoy.** Un run inexistente **sí** salía con código 1; **un run válido y vacío salía con 0 y certificaba «intacta»**, porque un run donde no pasó nada tiene cero fabricaciones por construcción. Y las 25 páginas sin declarar se imprimían debajo sin tocar el veredicto. Ahora son tres estados y el código de salida es el veredicto |
| **El paso 9 de su orden**: *«caso-02 sintético desde `13-synthetic-benchmark.md`. **El truth set ya está escrito**»* | **HECHO hoy, y con vergüenza:** esa misma mañana yo había construido un caso sintético **de mi cabeza**, escribiendo que su límite era no traer lo que a nadie se le ocurriría. **Estaba en el repositorio.** Materializado como `caso-03` |

### Lo vivo de este documento

| # | Qué | Estado |
|---|---|---|
| **R-1** | **Canal 3: la pregunta directa de ella.** *«No se activa ninguna skill: contesta el modelo desnudo, sin método, sin marcas, sin regla 1»*. Lo llamaba *«la corrección de fuentes jurídicas con mejor relación de todo el refinado»* | **Cerrado por dos vías:** existe `/preguntas-de-derecho` (SPEC-09) y la guía lo dice con esas palabras. **Lo que no está comprobado es que la skill se active sola**, y eso solo lo enseña una pasada |
| **R-2** | **`cita_juridica[]` obligatoriamente vacío como prueba del banco que falla** — paso 1 de su orden, mitad no hecha | **Vivo y barato.** Es una prueba determinista sobre una salida guardada, y ahora hay dos expedientes con salidas de referencia |
| **R-3** | **8.2 — ¿existe una abogada que verifique vigencia, con nombre?** Y si existe, ¿se acepta que *«sin `vigencia_hasta` comprobada, la norma no se sirve como citable»*? | **Del dueño.** Su propia lectura: *«no construirlo este ciclo. Un pack sin mantenedor da confianza en datos viejos»* |
| **R-4** | **8.4 — ¿la palabra de ella manda sobre un documento, o va al lado?** | **Del dueño, y urge más de lo que parece:** *«hoy el modelo elige solo, y lo más probable es que corrija en silencio»* |
| **R-5** | **8.6 — el presupuesto de medición:** cuántas corridas por brazo (7 para detectar un 20 %; con 3 solo se detecta 30-39 %), quién transcribe, y si el banco se parte en `verificar.py` + `medir.py` | **Del dueño.** Y su nota vale por sí sola: **la transcripción no puede hacerla el modelo** —circularidad— **ni entrar al repositorio** —custodia— |
| **R-6** | El **−34 %** con que se adoptó `inventario-de-anexos` v0.2.0 **no es distinguible del ruido** (n=1, efecto mínimo detectable 52-67 %) | **Vivo, y es una advertencia sobre cómo se citan las cifras de este proyecto** |

> **Y la frase de este documento que más vale, porque describe la garantía real del producto:** *«la abstinencia se acaba el día que exista el Knowledge Pack»*. Hoy no hay mecanismo que impida citar una norma derogada — **lo impide que el producto no cita normas**. Es una abstinencia, no un control.

---

---

## §10 · `architecture-post-v0`, y el disparador que ya se disparó

**Leído el 2026-09-05.** Es el registro de **24 exclusiones decididas y no olvidadas**, cada una con tres preguntas obligatorias: por qué está fuera de V0, **qué disparador la trae de vuelta**, y **qué no debe romperse hoy para que sea posible mañana**. La tercera es la que convierte el documento en algo distinto de una lista de deseos: es *«una restricción activa sobre el diseño de hoy»*.

Así que se leyó como lo que dice ser —una lista de restricciones vigentes— y se auditó **contra el producto que existe**, no contra el Core que no existe.

### Lo primero: un disparador ya se disparó, y nadie lo notó

**`Ruling`** dice, palabra por palabra:

> *«Pertenece al **contexto B (autoridad/decisor)**, cuyo trabajo real **NO HA SIDO LEVANTADO** […] Que la primera usuaria opere ambos contextos es **SUPUESTO, no hecho verificado**.»*
>
> *«**Disparador de vuelta.** El levantamiento del contexto B, y en particular la respuesta a la **pregunta de negocio 7** […] que puede **invertir la política de custodia**.»*

Y la pregunta 7, en `docs/discovery/business-questions-next.md`, se aparcó con este argumento: *«Esta pregunta bloquea el diseño del contexto B — **que no se está haciendo**»*.

**Las dos premisas son falsas hoy, y lo son por trabajo de este mismo repositorio:**

| Lo que el documento asume | Lo que hay |
|---|---|
| Que la usuaria opere ambos contextos es **SUPUESTO** | **Verificado en campo.** Fila `C-8` de este backlog: *«**Es autoridad.**»* |
| El diseño del contexto B **no se está haciendo** | **Se hizo el 2026-09-05.** SPEC-03 puso el bloque de posición en **los once** `SKILL.md`, reescribió las cinco reglas que presuponían bando y convirtió la simetría en método |

> **El disparador se disparó, y su documento no se enteró.** No es un descuido del documento: es exactamente el modo de fallo que §8 dejó nombrado — *un documento sin indexar no es deuda documental, es un defecto esperando*. Aquí el defecto no era del documento, era **del índice que no lo tenía**.

### Y la consecuencia que nadie había conectado

La pregunta 7 no es una curiosidad de diseño. Dice que si en el contexto autoridad existe **un expediente digital oficial en un sistema externo**, nuestro almacén sería *«copia de trabajo y no custodio primario»* — y llama a eso *«una inversión, no un ajuste»*.

**Siete `SKILL.md` justifican hoy la protección de escritura más fuerte del producto con esa razón**, tres de ellos con esta frase exacta:

> *«Nunca escribe dentro de `1-Documentos recibidos/`: eso es el material tal como llegó y **es lo único que no se puede reconstruir**.»*

Si ella, decidiendo, tiene el expediente oficial en el sistema de su entidad, **esa frase es falsa ahí**: sí se puede reconstruir, bajándolo otra vez.

> **Y una corrección a este mismo apartado, hecha unas horas después de escribirlo.** Aquí decía **«tres `SKILL.md`»**. Son **siete** los que llevan la regla; tres usan esa redacción exacta y los otros cuatro dicen lo mismo con otras palabras. **Es la misma cuenta mal hecha que §12 encontró en el commit del 26 de agosto** —*«los tres skills que tocan fechas»*, cuando eran siete— **cometida por mí el mismo día en que la estaba señalando.** Dos veces «tres» donde había siete, con diez días de distancia y por la misma causa: contar con la vista en vez de contar con un comando. La **protección seguiría siendo correcta** —es la conservadora, y no depende de la frase—, pero **su razón declarada no lo sería**. Y este producto entero se sostiene sobre que las razones que escribe sean verdad: es la misma disciplina que le prohíbe escribir una fecha que no leyó.

> **Esto se registra como pregunta, no como corrección.** Cuál es el expediente que vale cuando ella decide **es un hecho sobre su despacho**, no una decisión de arquitectura, y el propio documento ya trae la redacción para preguntárselo sin jerga. **Ninguna frase del producto se toca hasta que ella conteste.**

| # | Qué | De quién | Estado |
|---|---|---|---|
| **A-4** | **Preguntarle la pregunta 7**, con la redacción que ya está escrita: *«cuando le toca decidir, ¿cuál es el expediente que vale? ¿El que está en el sistema de la entidad, o el que usted arma para poder trabajar?»* | **Del dueño.** Es una conversación, no una tarea | **Abierta, y ahora sí bloqueante:** dejó de bloquear «un contexto que no se levanta» el día en que se levantó |
| **A-5** | Según la respuesta, **revisar la frase «es lo único que no se puede reconstruir»** en los tres `SKILL.md` que la usan | Mía, cuando A-4 tenga respuesta | **En espera de A-4.** No antes: cambiarla ahora sería sustituir un supuesto por otro |

### Los 24 disparadores, auditados

| Estado | Cuántos | Cuáles |
|---|---|---|
| **Disparado** | **1** | `Ruling` — arriba |
| **Armado: lo dispara la instalación pendiente** | **2** | **Plano administrativo** (*«una migración en la máquina de la profesional […] o la existencia de una segunda instalación»*) y **actualizaciones automáticas** (*«más de una instalación que mantener»*). Los dos los enciende la fila 3 de §2, que ya estaba en el backlog por otro motivo |
| **Cuelgan de una pregunta de negocio sin responder** | **5** | Conectores (2), PostgreSQL y búsqueda vectorial (3), Knowledge Pack (4), multi-máquina (5) |
| **Cuelgan de trabajo no levantado o de una decisión comercial** | **16** | El resto |

> **Y el dato que vale de esa tabla:** cinco disparadores dependen de las ocho preguntas de negocio, **ninguna de las ocho tiene respuesta escrita en el repositorio**, y la única que sí tiene un hecho de campo asociado —la 7— es precisamente la que nadie fue a mirar. Las preguntas están redactadas y listas desde hace semanas en `docs/discovery/business-questions-next.md`. **Lo que falta no es escribirlas: es una conversación de veinte minutos.**

### La restricción más dura, comprobada contra el producto — y arreglada

`Term / Deadline` se llama a sí misma *«la restricción más dura del documento»*:

> *«Nada en V0 debe calcular, almacenar ni mostrar algo que se parezca a un plazo. Ni un campo de fecha derivada presentado como término, ni un “vence en N días”, ni una fecha calculada que la usuaria pueda leer como cómputo procesal. **La razón es de confianza, no de arquitectura**: una fecha que aparece en la pantalla se lee como afirmación del sistema, aunque en el código sea un cálculo ingenuo.»*

**Se comprobó contra los once métodos, y el resultado tiene dos mitades.**

**La buena:** el producto la cumple, y la cumple **por convergencia, no por obediencia** — se escribió sin leer este documento, y llegó a la misma prohibición desde el techo epistémico. `revisar-documento` llega a listar las frases exactas que nunca escribe (*«vence el…»*, *«le quedan N días»*), y `revision-de-rigor` §3.7 hace lo que ningún documento de arquitectura pidió: **buscar la cuenta ya hecha en el escrito que ella va a firmar**.

**La mala, y era real:** la cumplía **con siete redacciones distintas**. Solo tres de los once traían la cláusula literal; los otros cuatro que escriben fechas la sostenían con el *«no calcular»* genérico del bloque de posición, que **no dice nada de convertir «treinta días» en una fecha**. Es la enfermedad de este repositorio otra vez: *una regla con dos redacciones se parte*.

**Arreglado el mismo día.** Una sola cláusula, byte a byte, en los **siete** métodos que pueden escribir una fecha en su salida. Los otros cuatro no la llevan, y uno de ellos **no puede llevarla**: `preguntas-de-derecho` §6 tiene la única excepción del producto —si ella pone la regla de cómputo, se le hace la cuenta a la vista— y una frase absoluta ahí la contradiría. **Dos pruebas nuevas** vigilan las dos mitades: que la prohibición sea idéntica donde va, y que la excepción siga viviendo en un solo sitio. Comprobadas por mutación.

### Las tres restricciones que no se pueden cumplir, y por qué decirlo importa

`architecture-post-v0` escribe sus *«qué no debe romperse hoy»* para un **Core que no existe** (§7, ADR-018). Tres se leyeron con cuidado porque su enunciado suena aplicable y no lo es:

| Restricción | Por qué hoy no aplica | Qué queda de ella |
|---|---|---|
| *«`ADMIN` sigue contando cero elementos, verificable por el test de superficie»* | No hay superficie MCP ni manifiesto de tools. **El canario no puede cantar porque no hay jaula** | **Se le construyó una jaula el mismo día, y cantó bien** — ver abajo |
| *«toda mutación produce exactamente un evento»* (biyección mutación↔evento) | No hay Case Event Log. Las escrituras de hoy las hacen scripts sobre archivos | Queda **la disciplina**, y sí se cumple: `estado_del_caso.py` no reescribe, **sustituye solo la cabecera y conserva sus notas byte a byte** |
| *«un backup sin round-trip de restauración probado no cuenta como backup»* | No hay backup | Queda como **la mejor frase del documento para el producto de hoy**, y aplicable tal cual: la copia que `estado_del_caso.py` hace antes de escribir **se restaura de verdad ante fallo**, y hay prueba que lo comprueba |

> **Por qué esto se registra en vez de callarse.** La tentación al auditar un documento así es marcar las tres como «cumplidas» —suenan a cumplidas— o como «no aplica» y pasar. Las dos serían mentira: **una restricción que no puede violarse porque su objeto no existe no está cumplida, está vacía**, y el día que el Core exista alguien las dará por vigentes sin haberlas ejercitado nunca. Y hay una **cuarta** que sí es una restricción viva y hoy nadie vigila: *«el techo epistémico vive en el Domain, no en la superficie»*. **Hoy el techo epistémico vive entero en la superficie** —es prosa, en once `SKILL.md`— y no hay otro sitio donde ponerlo. No es un defecto del producto: es la descripción exacta de qué es este producto, y conviene tenerla escrita antes de que alguien construya el Core creyendo que la duplica.

### El canario de `ADMIN`, traducido al producto que sí existe

El **Principio 1** del plano administrativo dice que migraciones, packs y reparación *«existen solo en el runtime/CLI del producto, nunca como tools expuestas a Claude»*, y que eso **se comprueba con una prueba, no con una revisión que alguien recuerde hacer**: *«si algún día cuenta más de cero, la frontera se movió»*.

Ese principio **sí tiene objeto hoy**, aunque no haya MCP: la superficie por la que este producto puede ejecutar código es el `allowed-tools` de cada `SKILL.md` (ADR-018). Así que se contó, por primera vez:

| | |
|---|---|
| `SKILL.md` que declaran `allowed-tools` | **10 de 11** — todos menos `preguntas-de-derecho`, que no toca material |
| Programas alcanzables desde la superficie | **6** — `md2docx`, `verificar_fidelidad`, `buscar`, `estado_del_caso`, `preparar_material`, `segunda_opinion` |
| Programas en el disco **no** alcanzables desde ninguna skill | **2** — `traer_modelos.py` (baja los modelos de OCR) y `medir_realce.py` (mide si el realce mejora el OCR) |

> **Y los dos que no están expuestos son exactamente de la clase `ADMIN`.** Bajar modelos de terceros es **instalar un pack**; medir el realce sobre material real es **instrumentación de desarrollo**. Ninguno de los dos tiene por qué poder invocarlo el modelo, y ninguno de los dos puede. **La cuenta de `ADMIN` en la superficie es cero** — no porque alguien la vigilara, sino porque la frontera se respetó sin nombrarla.
>
> **Ahora sí la vigila algo.** Una prueba fija los seis alcanzables y los dos reservados: si aparece un séptimo expuesto, o si uno de los dos administrativos se cuela en un `allowed-tools`, falla. Es la traducción literal del canario, y costó veinte líneas.

### Lo vivo

| # | Qué | Estado |
|---|---|---|
| **A-4** | Preguntar la pregunta de negocio 7 | **Del dueño. Bloqueante desde hoy** (arriba) |
| **A-5** | Revisar *«lo único que no se puede reconstruir»* según la respuesta | En espera de A-4 |
| ~~**A-6**~~ | ~~Contar la superficie real de hoy~~ | **HECHA el 2026-09-05**, y con prueba que falla si crece — arriba |
| **A-7** | Que la instalación en otra máquina (fila 3 de §2) **se registre como el disparo de dos exclusiones**, no solo como una prueba de que abre el `.md` | Cuando ocurra |
| ~~**A-8**~~ | ~~Indexar `docs/discovery/business-questions-next.md`~~ | **HECHA el mismo día: §11**, y contestó tres de las ocho desde el disco |

---
---

## §11 · Las ocho preguntas de negocio, y las tres que ya tienen respuesta en el disco

**Leído el 2026-09-05**, porque §10 lo obligó: **cinco de los 24 disparadores del backlog de arquitectura cuelgan de estas ocho preguntas**, y una de ellas —la 7— resultó ser el disparador que ya se había disparado.

`docs/discovery/business-questions-next.md` es lo mejor escrito de este corpus para su propósito: ocho preguntas **redactadas para ella y no para un ingeniero**, cada una con qué decisión depende, si bloquea, y una redacción sin jerga. Trae incluso la advertencia de método correcta: *«una pregunta que sugiere su propia respuesta produce confirmación, no información»*.

**Y ninguna de las ocho tiene respuesta escrita.** Pero tres ya la tienen **en el disco de este repositorio**, puestas ahí por el trabajo de campo y nunca devueltas al documento que las esperaba.

### Las tres que el propio repositorio ya contestó

| # | Qué pregunta | Qué hay ya escrito, y dónde |
|---|---|---|
| **2** | *«¿cómo le llegan los documentos, en la práctica y sin idealizar?»* | **Contestada por dos pases reales.** `PASE-REAL-SALENTO` §encabezado: **23 fotografías JPG, 8 documentos, 23 páginas, 45,5 MB**. El canal real es *fotografiar un expediente en papel* — ni correo, ni plataforma. **Y el producto ya está construido sobre esa respuesta**: `preparar-material` existe porque el material llega así |
| **3** | *«¿hablamos de cinco documentos o de quinientos?»* — el propio documento dice que **no necesita el número exacto** | **Contestada en orden de magnitud, dos veces.** Caso de familia: **56 páginas**, 39 de anexos, **14 legibles**. Salento: **8 documentos, 23 páginas**. Son **decenas**, no centenares. Es exactamente la precisión que la pregunta pide |
| **7** | *«cuando le toca decidir, ¿cuál es el expediente que vale?»* | **Contestada a medias** — ver §10. La mitad que sí: **es autoridad**, y consta versionado en el encabezado del `PASE-REAL` (*«abogada de la Inspección de Policía de Salento, actúa como contradictor interno»*). **La mitad que falta es la que importa** y sigue siendo A-4 |

> **Lo que esto dice del proyecto no es que el documento estuviera mal.** Estaba bien, y sigue estándolo. Es que **el trabajo de campo y el documento que lo esperaba nunca se cruzaron**: el pase midió, escribió sus números y siguió; las preguntas se quedaron en la carpeta de al lado, esperando una conversación que ya había ocurrido en parte. Es la misma enfermedad de §8 en su otra dirección — allí un documento sin leer costó dos defectos; aquí **un hecho sin devolver dejó cinco disparadores colgando de una pregunta que ya tenía media respuesta**.

### La columna «¿BLOQUEA?» mide algo que ya no existe

Las ocho responden **NO** a *«¿bloquea el Technical Design?»*, y el documento aclara que el resultado no se forzó: *«es consecuencia de que varias decisiones ya tomadas se tomaron precisamente para que estas preguntas no bloquearan»*. Es verdad y está bien argumentado.

**Pero el Technical Design describe un Core que no se está construyendo** (§7, ADR-018). La pregunta que hoy vale es otra: **¿bloquea el producto que sí existe?** Releídas contra ese eje, la respuesta cambia en tres:

| # | ¿Bloquea el Technical Design? | ¿Bloquea el producto de hoy? |
|---|---|---|
| **1** · «hecho acreditado» | NO — `ProfessionalDetermination` no tiene productor en V0 | **NO, y por una razón más fuerte que la del documento.** El riesgo que la pregunta existe para desactivar —*«un nombre equivocado puede sugerir efectos procesales»*— **no puede materializarse aquí**: este producto **nunca escribe la palabra «acreditado» como afirmación propia**. Está en la lista de palabras prohibidas de cinco métodos. No hay estado que nombrar mal porque no hay estado |
| **2** · canales | NO — frontera de incorporación invariante al origen | **Ya no bloquea: está contestada** (arriba) |
| **3** · volumen | NO — los umbrales son calibrables | **Ya no bloquea en su parte útil** (arriba). Lo que sigue abierto es *«cuando un caso se acaba, ¿cuánto tiempo necesita el material a la mano?»*, que no es volumen sino retención |
| **4** · fuentes jurídicas | NO — ningún Knowledge Pack se carga | **NO. Y menos aún:** el producto **no cita derecho en absoluto** (§9). La abstinencia es total |
| **5** · personas | NO — la tripleta de actor está en el schema | **SÍ, de otra manera.** Aquí no hay schema donde reservar un hueco: la única persona que el producto nombra es **ella**, en prosa, once veces. Si mañana un dependiente ejecuta un comando, **no hay dónde registrarlo** — y la marca ` - REVISADO` presupone que quien la puso fue ella |
| **6** · backups | NO — pero **bloquea operar con datos reales** | **SÍ, y hoy más:** el producto ya corrió sobre **dos expedientes reales**, sin que esa pregunta se contestara. El documento decía que su respuesta *«habilita el paso de datos sintéticos a expedientes reales»*. **Ese paso ya se dio** |
| **7** · expediente oficial | NO — «bloquea el diseño del contexto B, que no se está haciendo» | **SÍ.** El contexto B se hizo. Ver §10 |
| **8** · ritmo | NO | NO |

> **La fila 6 es la que incomoda, y por eso se escribe.** Es la única de las ocho que el documento marca como bloqueante de algo con nombre propio —*operar con datos reales*— y es el único umbral que el proyecto ya cruzó **sin la respuesta**. No es reprochable: el pase real fue lo que hizo bueno a este producto, y los cuatro de los cinco defectos vivos salieron de ahí. Pero **el riesgo que la pregunta 6 nombra sigue entero**: *«el robo del portátil destruye y expone todo a la vez»*, y hoy no consta que exista copia de nada.

### Una referencia que no lleva a ninguna parte

El encabezado del `PASE-REAL-SALENTO` —la pieza versionada que sostiene *«es autoridad»*— remite a `memory/contexto-b-inspeccion-salento.md`. **Ese archivo no está en el repositorio y no puede estarlo:** `memory/` es la carpeta que el asistente se guarda **por máquina**, fuera del control de versiones (`platform-facts.md` lo documenta: `~/.claude/projects/<proyecto>/memory/`).

**El hecho no se cae** —el propio encabezado lo dice con todas las letras, y eso sí está versionado—, **pero su ampliación no la puede abrir nadie más**. Y de ese hecho cuelgan hoy `C-8`, SPEC-03 completa, el disparador de §10 y las preguntas A-4/A-5.

### Lo vivo

| # | Qué | Estado |
|---|---|---|
| **A-8** | ~~Indexar las ocho preguntas~~ | **HECHA.** Este apartado |
| ~~**A-9**~~ | ~~Devolver al documento de preguntas lo que el campo ya contestó~~ | **HECHA el mismo día.** Las preguntas 2, 3 y 7 llevan ahora su respuesta parcial, con fuente, fecha **y lo que siguen sin contestar** — que es la parte que no se puede saltar: dos casos no son una semana |
| **A-10** | **La pregunta 6 —copia de seguridad— pasa de «no bloquea» a bloqueante retroactivo**, porque el paso que habilitaba ya se dio dos veces | **Del dueño.** No es diseño: es preguntarle a ella si hay copia de algo, hoy |
| **A-11** | **La pregunta 5 empieza a bloquear el producto de hoy**, no el Core: la marca ` - REVISADO` presupone que la puso ella, y no hay nada que lo distinga si la pone otra persona | **Registrada, sin decidir.** Cuelga de A-4 en la práctica: las dos son la misma conversación |
| ~~**A-12**~~ | ~~La referencia colgante a `memory/…`~~ | **HECHA el mismo día**, y con la corrección explicada dentro del propio documento de campo, no en silencio |

---
---

## §12 · `skills-support`, y una cuenta mal hecha el 26 de agosto que se cerró hoy

**Leído el 2026-09-05.** Y lo primero es una corrección a este mismo backlog: **no son «los veinte dossiers»**. Son **89 documentos y 5.429 líneas**, en once carpetas. La cifra venía de contar la raíz sin abrir las subcarpetas, y se arrastró por tres apartados.

### Qué es, y por qué no cubrirlo no era deuda

Es investigación para **skills jurídicas**: catálogo normativo, gobierno de jurisprudencia, cobertura del derecho colombiano, mapas de dependencias, marcos adversariales, evaluaciones sintéticas. **Y el producto que existe no cita derecho en absoluto** (§9, *«la abstinencia»*).

> **Así que este corpus no está desactualizado: está por delante.** Describe la línea de producto que empieza el día que exista el Knowledge Pack, y §9 ya dejó dicho qué garantiza mientras tanto — *«hoy no hay mecanismo que impida citar una norma derogada; lo impide que el producto no cita normas»*. **Un corpus por delante no cobra defectos**, que es exactamente lo contrario de lo que pasó con `PENDIENTE-FORMA-DE-ENTREGA` (§8). Por eso este quedó de último, y estuvo bien.

Y **se declara a sí mismo con honestidad**, en su primera pantalla: `SKILL_SUPPORT_CORPUS_NOT_READY`, `COVERAGE_GAPS_PRESENT`. No hay que descubrir que no está listo: lo dice.

### La disciplina que este corpus sí practica

Dos cosas que en otros sitios de este repositorio salieron mal, aquí salieron bien, y merece decirse porque §5 solo cuenta duplicados:

| Riesgo | Cómo lo resolvió |
|---|---|
| **Dos documentos para lo mismo** — `00-scope-and-governance` / `00-scope-and-principles`, `03-priority-roadmap` / `03-skill-priority-roadmap` | **Cada uno abre con una nota de navegación que dice cuál prevalece.** No es la enfermedad de §5: es la enfermedad tratada |
| **Dos listas de preguntas para la misma profesional** | `open-questions/questions-for-professional.md` **abre declarando la regla**: *«no repetir preguntas ya cubiertas sobre canales de evidencia, volumen, fuentes habituales, participantes, backups, expediente oficial y ritmo»*, y nombra el documento que las tiene. **Quince preguntas, cero solapes** |

### Y la misma pregunta que §10 y §11, por tercera vez

Esa segunda lista tiene, bajo **`BLOCKING SKILL DESIGN`**, esta:

> *6. **Si llegara a actuar como autoridad**, ¿qué partes de una propuesta de decisión tendría que revisar o reescribir siempre usted misma, aunque una herramienta hubiera organizado el material?*

**«Si llegara a actuar como autoridad.» Actúa.** Es la tercera vez en dos apartados que un documento aparca algo sobre el condicional de un hecho que el trabajo de campo ya estableció — el disparador `Ruling` (§10), la pregunta de negocio 7 (§11) y ahora esta. **Tres documentos, tres corpus distintos, la misma pregunta sin hacer.**

Y hay una cuarta de esa lista que este producto ya contestó **sin preguntar**:

> *2. ¿Qué revisión hace personalmente antes de permitir que un hecho llegue a un escrito?*

La respuesta que el producto lleva escrita es la marca ` - REVISADO`: ella escribe `SÍ`, `NO` o `A MEDIAS` al lado de cada ficha y renombra el archivo. **Es una respuesta buena y es una suposición**, y coincide con `A-11` de §11 por el otro extremo — **nada distingue hoy que la marca la haya puesto ella y no un dependiente**.

### La cuenta mal hecha, que es el hallazgo de este apartado

El `README` de este corpus cierra con una corrección de ruta: *«la ruta vigente del plugin existente es `plugins/despacho/skills/fact-builder/`»*. **Esa carpeta no existe.** Se borró el **2026-08-26**, un día después de la fecha de referencia del corpus, en el commit que aplicó la crítica al arnés: **`H-09 fact-builder pasa a llamarse hechos-con-prueba`**. Hoy la nombran **55 documentos** del repositorio, 27 de ellos aquí.

**No se van a renombrar los 55**, y decir por qué importa: son **registro histórico** —ADRs, notas de diseño, verificaciones— y reescribirlos falsearía lo que se decidió con la información de entonces. Se corrige **la única línea que afirma un hecho sobre hoy** y es falsa, y se deja dicho en qué se convirtió.

**Pero ese mismo commit trae el hallazgo bueno**, en su propio texto:

> *`H-03` la frontera del cálculo pasa a estar escrita por operación, no por tema, **en los tres skills que tocan fechas***

**No son tres. Son siete.** Ese mismo día se contaron mal los métodos que pueden escribir una fecha en la salida de ella, la regla se puso en tres, y los otros cuatro se quedaron con el *«no calcular»* genérico —que no dice nada de convertir *«treinta días»* en una fecha— **durante diez días**.

> **Y esto es lo que retro-justifica §10 entero.** La cuenta no se corrigió leyendo el producto: **once relecturas de estos `SKILL.md` en dos semanas no la vieron**. Se corrigió porque un documento de **otro corpus**, `architecture-post-v0`, obligó a contar: *«nada en V0 debe calcular, almacenar ni mostrar algo que se parezca a un plazo»*. Es la misma lección de la tabla de §0 con un tercer renglón:
>
> | Origen del hallazgo | Encontró algo |
> |---|---|
> | Releer lo que uno escribió | **No** — diez días mirándolo |
> | Ejecutar el producto | **Sí** — 4 de 4 |
> | **Cruzar dos corpus que nadie había cruzado** | **Sí — y encontró lo que releer no encontraba** |
>
> Escribir una regla y releerla no dice si decide. **Y contarla contra un documento que no la escribió, sí.**

### Lo vivo

| # | Qué | Estado |
|---|---|---|
| ~~**S-1**~~ | ~~La ruta `fact-builder` que el `README` da por vigente~~ | **HECHA el 2026-09-05.** Corregida la línea, con la fecha del cambio y su commit; los 55 usos históricos **se dejan como están, y se dice por qué** |
| **S-2** | **Preguntar la pregunta 6 de esta lista** — qué de una propuesta de decisión reescribiría siempre ella | **Del dueño. Es la misma conversación que `A-4`**, y conviene que sea una sola |
| **S-3** | Las **89 piezas** de este corpus siguen sin triar una por una. **No urge**, por la razón de arriba | Vivo, de baja prioridad declarada |
| **S-4** | Corregida en este backlog la cifra **«veinte dossiers»** → **89 documentos** | **HECHA.** Estaba en tres sitios |

---
---

## §13 · `technical-design`, y una regla que este mismo corpus demostró que no protege

**Leído el 2026-09-05, y con esto se cierra el §0.3.** Es el corpus más grande del repositorio: **46 documentos, 17.990 líneas** — veinte documentos numerados del kernel al despliegue, más notas de diseñadores y de verificación.

### El triaje es el mismo que el de los ADR, y por la misma razón

Los veinte documentos numerados diseñan **el Core que no existe** (§7, ADR-018): modelo de dominio, contrato MCP, persistencia, proyecciones, ciclo de vida del artefacto, autorización humana server-side. Sus **ocho decisiones que esperan aprobación** —`principal_type` sin `EXTERNAL`, el retiro de `register_artifact`, separar `event_seq` de `case_revision`, las cinco políticas del Product Floor— son decisiones **sobre ese Core**, y ninguna toca el producto que hoy corre.

Y lo que ya se aprovechó de aquí, se aprovechó bien: **su §13 se materializó como `caso-03`**, el banco sintético que este backlog dio por inexistente y estaba diseñado desde el principio.

### Pero un hallazgo sí transfiere, y es el más duro del repositorio

`ESTADO-Y-HALLAZGOS-CRITICOS.md` §1.1 registra cinco hechos **verificados contra documentación oficial**. El segundo:

> *«**No existe deny por ruta en Cowork.** Adjuntar una carpeta concede su árbol completo; el agente puede leer y escribir todo lo que alcance la cuenta del sistema operativo. **El único remedio documentado es posicional:** dejar los datos fuera de las carpetas permitidas.»*

Y la conclusión que saca en §1.3, sobre el almacén del Core:

> *«**La protección del case store no puede ser una regla; tiene que ser una posición.**»*

**Aplíquese eso a `1-Documentos recibidos/`, que es la carpeta que este producto protege con más fuerza.** El resultado no es cómodo:

| | |
|---|---|
| **¿La protección es una regla o una posición?** | **Una regla.** Prosa, en **nueve** `SKILL.md` — se contaron |
| **¿Está disponible el remedio posicional?** | **No, y no puede estarlo.** El remedio es *«dejar los datos fuera de las carpetas permitidas»*, y **los métodos tienen que leer esa carpeta**. Sacarla de alcance es apagar el producto |
| **¿Hay algún mecanismo del anfitrión que la respalde?** | **Ninguno.** `plugin.json` trae nombre, versión, descripción y palabras clave. **Cero hooks, cero `permissions`, cero `deny`** en todo el repositorio |

> **Así que hoy la protección más fuerte del producto descansa entera en que el modelo obedezca un párrafo, nueve veces.** No es un defecto encontrado —la regla está en los nueve, incluidos los dos casos especiales, y se comprobó uno por uno—; es **el mecanismo, dicho con precisión**, y este corpus es el que verificó que un mecanismo así no es un perímetro.
>
> **Lo que sí se puede hacer desde aquí se hizo:** una prueba que **fija la cuenta de los nueve**. No convierte la regla en perímetro —nada de este lado puede—, pero el modo de fallo real no es que alguien borre la regla: es **un método nuevo que lea esa carpeta y no la traiga**. Eso ahora falla.
>
> **Y una distinción que hay que dejar escrita antes de que alguien la borre:** este hallazgo es sobre **Cowork**. Que Cowork *no* herede la configuración de Claude Code (hallazgo §1.1.1) implica que **Claude Code sí tiene** reglas de permiso; de dónde se ejecute el plugin **cambia qué protecciones existen**. Nadie ha escrito esa decisión, y vuelve a caer sobre la instalación pendiente — **la cuarta cosa que esa fila de §2 desbloquea**.

### El riesgo abierto que este corpus llama el más grave, y a quién le toca

`B-04`: no está documentado si un servidor MCP local puede alcanzar rutas fuera de las carpetas adjuntadas. *«Hasta resolverlo empíricamente no puede afirmarse que el perímetro de ADR-002 sea realizable sobre Cowork»*, y el protocolo de 31 pasos ya está escrito en `experiments/cowork-capability-spike/`.

**No es trabajo de este backlog y conviene decirlo:** `B-04` decide si **el Core** es construible sobre ese anfitrión. Hoy no hay Core. Queda registrado como lo que es — **el riesgo mejor identificado del repositorio, con su experimento ya diseñado y sin ejecutar** — y no como deuda del producto que corre.

### Lo vivo

| # | Qué | Estado |
|---|---|---|
| ~~**T-1**~~ | ~~Contar la protección de `1-Documentos recibidos/`~~ | **HECHA.** Nueve métodos, nueve prohibiciones, y una prueba que falla si aparece un décimo sin ella |
| **T-2** | **Decidir y escribir en qué anfitrión corre esto**, porque de eso depende si existe algún mecanismo además de la prosa | **Del dueño, y es la fila 3 de §2 otra vez.** Ya desbloquea cuatro cosas distintas |
| **T-3** | **La razón de la protección queda pendiente de `A-4`** — la dan siete métodos, y si el contexto autoridad tiene expediente oficial es falsa ahí. La prueba fija los siete **para que el día que se decida se toquen los siete y no tres** | En espera de A-4 |
| **T-4** | `B-04` — ejecutar el spike de 31 pasos | **Del dueño, y no urge:** decide sobre un Core que no existe |
| **T-5** | Los **46 documentos** no se triaron pieza a pieza, por la misma razón que `S-3` | Vivo, de baja prioridad declarada |

---
---

## §14 · Lo que pasó al ejecutar el producto en los dos contextos

**2026-09-05, después de cerrar el §0.3.** Once specs estaban «ejecutadas» y ninguna comprobada **corriendo el método**. Se corrieron cinco contra el `caso-03`, cuyo truth set estaba escrito antes de esta sesión. [El registro completo está aparte](technical-design/v0/notes-verification/pasada-caso-03-2026-09-05.md); aquí va lo que cambia el backlog.

### El resultado de veracidad, que es el que manda

**Cero afirmaciones prohibidas afirmadas. Cuatro trampas de entidad de cuatro superadas.** Nariño y Mariño separados —con la advertencia de que la entrevista los distingue una sola vez—, las dos sociedades Delmonte separadas con sus dos NIT, «M E QUIROGA B» **resuelta** diciendo sobre qué se apoya la lectura, y la vecina sin nombre.

**Y la pasada más valiosa no produjo archivo.** `inventario-de-anexos` se detuvo en su Fase 2: no hay hoja de hechos con la marca ` - REVISADO`, así que preguntó **y esperó**, en vez de emparejar con la hoja sin marcar «para ir adelantando». Las otras cuatro comprueban que el método hace bien lo que hace; **esta comprueba que no hace lo que no debe**, que es la mitad difícil.

### Y lo que ejecutar encontró, que releer no encontraba

**Seis defectos, todos míos.** Los dos que más pesan:

| Qué | Cuándo |
|---|---|
| *«las dos actas, con veintiún días de diferencia»* — veintiuno no está en ninguna pieza | En la **primera salida producida bajo la regla unificada esa misma mañana** |
| *«la diferencia es de $500.000»* — no aparece en el material | En el **mismo archivo**. La guarda de esa mañana solo miraba fechas |

### La cuenta que hay que mirar de frente

**Cinco conteos mal hechos el mismo día**, todos de la misma operación:

| Cuándo | Qué se contó | Dijo | Era |
|---|---|---|---|
| 26-08 | Skills que tocan fechas (`H-03` del commit del arnés) | tres | **siete** |
| 05-09 | `SKILL.md` que justifican la protección de escritura (§10) | tres | **siete** |
| 05-09 | Fichas apoyadas de la pasada de hechos | 10 y 7 | **9 y 6** |
| 05-09 | Documentadas de la cronología | cinco | **cuatro** |
| 05-09 | Métodos con el bucle anidado (SPEC-13) | dos | **cuatro** |

**Ninguna se encontró releyendo. Las cinco con un comando.** Y el cuarto fue el peor, porque los números **no cuadraban** —15 donde había 14— **y en vez de recontar se escribió un párrafo explicando la discrepancia**. La explicación era plausible y era falsa.

> **La conclusión no es «hay que contar mejor».** Es que **un documento que pide una cifra sin dar con qué obtenerla está pidiendo un error**, y este arnés lo hacía en tres métodos. Ahora los tres invocan un programa, y la regla nueva está escrita en dos de ellos: **si el conteo no cuadra, se recuenta; no se explica.**

### La tabla de §0, con su cuarta fila

| Origen del hallazgo | Verificados | Eran como se decía |
|---|---|---|
| Leer documentos de diagnóstico | 6 | **0 de 6** |
| Ejecutar el producto en un caso real | 4 | **4 de 4** |
| Releer lo que uno mismo escribió esa semana | 18 | **0 de 18** |
| **Cruzar dos corpus que nadie había cruzado** (§12) | — | **encontró lo que releer no encontraba** |
| **Ejecutar el producto contra material con verdad conocida** | 5 métodos | **6 defectos, cero visibles releyendo** |

### Lo vivo

| # | Qué | Estado |
|---|---|---|
| **§2 · 6** | Una prueba capaz de fallar | **Hecho en veracidad.** Instrumento, material y cinco pasadas. **Falta el coste** |
| **§2 · 5** | `PM-M-1` (a) y (b) — instrumentar | **Sigue abierto y seguirá:** necesita una corrida con transcript, y una pasada de escritorio no lo es |
| **P-1** | **Que una abogada abra una de estas nueve salidas.** Ninguna la ha visto nadie | **Del dueño.** Es la única medición que importa y la que no se ha hecho |
| ~~**P-2**~~ | ~~Correr las cinco contra el `caso-02`, contexto B~~ | **HECHO el 2026-09-05.** Cuatro salidas existían y **ninguna había pasado por las guardas**: encontraron seis cosas, tres de ellas **vocabulario cerrado abierto sin que nadie lo decidiera** —grados renombrados, un veredicto global que no es uno de los cinco, un evento contado dos veces—. Y la quinta pasada **tampoco produjo archivo**: aquí `inventario-de-anexos` para porque hay **dos** hojas marcadas, donde en el `caso-03` paraba porque no había **ninguna**. [Registro](technical-design/v0/notes-verification/pasada-caso-02-2026-09-05.md) |

---
---

*Consolidación asistida y verificada contra el repositorio donde se indica. **Cobertura completa del §0.3 desde el 2026-09-05** (§§7 a 13). Los dos corpus grandes están triados **como corpus**, no pieza a pieza (`S-3`, `T-5`), y se dice por qué. Nada de este documento reemplaza a sus fuentes.*
