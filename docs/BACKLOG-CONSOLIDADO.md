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

También quedan fuera, y hay que decirlo: `docs/backlog/architecture-post-v0.md`, `docs/REFINADO-Y-FUENTES.md`, `docs/PENDIENTE-FORMA-DE-ENTREGA.md`, `docs/technical-design/` y los veinte dossiers de `docs/skills-support/`.

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
| **6** | **Una prueba capaz de fallar.** Existen 678 líneas de banco y seis fixtures que ninguna evaluación mencionó | G22 · `PM-5.1-BANCO` | La regla de composición · M-9 · M-11 · M-12 | Abierto |
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
| **0.8** | **Los dos PDF del caso-01, para reconstruir el truth set del banco** — o decir que ese caso se retira y cuál lo sustituye | Sacarlos de donde estén | **Es lo que desbloquea la fila 1.3, que estaba mal puesta en mi bloque.** Sin material no hay banco, y sin banco ningún cambio del método es reversible con criterio (G22) |
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

**Cierre honesto del §0.3:** los ADR ya están leídos y triados. Lo que **sigue sin cubrir** de aquel párrafo es `docs/REFINADO-Y-FUENTES.md`, `docs/PENDIENTE-FORMA-DE-ENTREGA.md`, `docs/backlog/architecture-post-v0.md`, `docs/technical-design/` y los veinte dossiers de `docs/skills-support/`.

---

*Consolidación asistida y verificada contra el repositorio donde se indica. **Cobertura parcial: faltan los ADR y cinco corpus más (§0.3).** Nada de este documento reemplaza a sus fuentes.*
