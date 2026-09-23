# Estado del proyecto — Legal Workspace / Legal OS

**Fecha de corte:** 2026-09-21. **Rama:** `claude/backlog-continuacion-jm9x69`. **Último commit leído:** `11baa56`.

> ### Este documento estaba caducado, y lo decía él mismo
>
> Su última línea era: *«Caduca con el próximo commit que toque `plugins/despacho/` o `docs/skills-support/`»*. Desde entonces hubo **sesenta y un commits** que tocan las dos cosas. **La versión anterior tenía fecha de corte del 2026-08-26 y nueve de sus diez titulares eran falsos el 21 de septiembre.**
>
> **Qué se hizo con el texto viejo, y por qué.** Los apartados que hacen afirmaciones **sobre el presente** —§0, §5, §6, §7— se reescriben, porque decían cosas que hoy son falsas y este documento existe para contestar *¿en qué vamos?*. Los que son **registro de un análisis fechado** —§1 a §4— se conservan con una marca de qué quedó superado y dónde está lo vigente. **Reescribirlos borraría lo que se sabía el 26 de agosto**, que es información: de ahí salieron la mitad de las correcciones que vinieron después.
>
> **El detalle de todo lo ocurrido entre las dos fechas está en `docs/BACKLOG-CONSOLIDADO.md` §§7 a 15.** Aquí va lo que cambia la respuesta a *¿en qué vamos?*, y nada más.

Este documento responde a una sola pregunta: **¿en qué vamos?** Está escrito después de leer, por separado y con seis lectores independientes, el producto desplegado, la crítica de diecisiete hallazgos, el corpus completo de `docs/skills-support/`, los trece ADRs, los dos inventarios de plataforma y los fixtures de evaluación; más un séptimo pase dedicado exclusivamente a buscar contradicciones entre todo eso.

**Regla que seguí al escribirlo:** solo afirmo lo que un lector encontró en un archivo, con su ruta. Donde el material no alcanza, lo digo en vez de completarlo con lo que sonaría razonable. Etiquetas: HECHO VERIFICADO / SUPUESTO / POR VERIFICAR / RIESGO / DECISIÓN PENDIENTE.

---

> ## CERRADO EL 2026-09-22
>
> **El trabajo se para aquí para llevar los recursos a otra cosa.** Lo que hace falta para
> retomarlo en frío está en **[`CIERRE-2026-09-22.md`](CIERRE-2026-09-22.md)**: qué es esto,
> qué hacer lo primero, lo que el proyecto aprendió, lo que queda abierto **y de quién es**,
> y lo que este proyecto **no sabe de sí mismo**.
>
> **Lo primero al volver:** `sh evals/scripts/correr-todo.sh`. Si sale verde, el producto
> sigue siendo el que estos documentos describen.

---

## §0 — Dónde estamos, en diez líneas

**Cada punto se recomprobó contra el repositorio el 2026-09-22, con un comando.** Donde el titular de agosto cambió, se dice qué decía y qué lo cambió — porque *«ya no aplica»* sin la frase vieja al lado no deja comprobar nada.

1. **Se puede instalar, y nadie lo ha instalado.** ~~«NADIE PUEDE INSTALARLO: `git remote -v` no devuelve nada»~~ — **falso desde el 2026-09-05**: `origin` es `github.com/CHERCED-DEV/legal-workspace` y el `marketplace.json` existe. HECHO VERIFICADO con `git remote -v`. **Lo que sigue abierto es otro trabajo:** nadie lo ha instalado nunca en una máquina que no sea la del dueño, y de eso dependen **cuatro cosas distintas** (§6).

2. **Sigue sin citar una sola norma, y ahora son quince métodos.** `grep -E "Ley [0-9]|Decreto [0-9]|art\. [0-9]"` sobre los trece `SKILL.md` no devuelve nada. La regla dura 1 se cumple de verdad. HECHO VERIFICADO. **Y en septiembre se comprobó ejecutando:** cuatro preguntas de derecho sobre un expediente, incluida una inyección escrita para romper la negativa, y las cuatro se negaron y ofrecieron lo que sí se puede hacer.

3. **Once de los quince se han ejecutado al menos una vez, y ninguno salió limpio.** ~~«ninguno se ha ejecutado nunca»~~ — **falso desde el 2026-09-07**. Once métodos corridos contra dos expedientes de banco, uno de parte y uno de autoridad. **Cero afirmaciones prohibidas afirmadas; las cuatro trampas de entidad superadas.** Y ejecutarlos encontró defectos en los once. Registro: `notes-verification/pasada-caso-02`, `pasada-caso-03` y `pasada-redactar-escrito`. **El duodécimo, `transcribir-audio`, entró por fusión el 2026-09-22 y no se ha corrido aquí** — ni se puede: `faster-whisper`, `av` y `sherpa-onnx` no están en este entorno, y su medición viene de la máquina donde se escribió (§4 de su `SKILL.md`, 56 min 52 s de reunión y una GTX 1660 Ti). **Lo que sí se comprobó aquí es que, sin esas bibliotecas, declara cuál falta y no revienta.**

4. **Los diecisiete hallazgos de la crítica están cerrados.** ~~«Todos siguen vivos; solo H-08 está a medias»~~ — **falso**: los doce de la crítica al arnés se aplicaron el 2026-08-26 (commit `6444952`) y los doce de `inventario-de-bienes` estaban ya aplicados, comprobados uno por uno en `notes-verification/auditoria-inventario-de-bienes-2026-09-05.md`. **Lo que quedó vivo de aquel commit fue una cuenta mal hecha dentro de él** —su `H-03` dice *«los tres skills que tocan fechas»* y eran **siete**—, corregida el 2026-09-05.

5. **La guía ya dice dónde se procesa su material.** ~~«hace tres afirmaciones falsas y omite el hecho que más cambiaría lo que ella hace»~~ — **falso**: `GUIA-PARA-LA-ABOGADA.md` lo dice en tres párrafos seguidos, y dice también la confusión que lo rodea: *«Guardar un archivo en su disco no es lo mismo que trabajarlo en su disco»*. HECHO VERIFICADO. **La decisión de confidencialidad sigue sin tomarse** (§6): lo que cambió es que ya no se le oculta.

6. **La cadena está completa, y se ejecutó entera.** ~~«`fact-builder` no escribe ningún archivo, y toda la promesa se apoya en un archivo que no existe»~~ — **falso**: `hechos-con-prueba` escribe en `2-Borradores/`, ella marca con ` - REVISADO`, y `redactar-escrito` e `inventario-de-anexos` consumen esa marca **y se detienen sin ella**. Probado en los tres estados posibles —cero marcadas, una, dos— y **los tres se comportan bien**.

7. **El corpus sigue describiendo un producto que ya no existe, y ahora se sabe cuánto.** **Cincuenta y cinco documentos** nombran `fact-builder`, que se renombró a `hechos-con-prueba` el 2026-08-26. **No se renombraron los 55, y decir por qué es parte de la decisión:** son registro histórico, y reescribirlos falsearía lo que se decidió con la información de entonces. Se corrigió **la única línea que afirmaba un hecho sobre el presente** — el `README` de `skills-support/`, que daba esa ruta por vigente.

8. **El Core no existe, y ya no es la pregunta que bloquea.** ADR-018 estableció que el plugin **puede ejecutar código**, y hoy trae veinticuatro programas, de los cuales **trece se exponen al modelo** — los otros once se corren a mano o no se invocan (`test_superficie.py` los tiene clasificados uno por uno, y falla si uno cambia de lado sin que nadie lo decida). Los veinte documentos de `technical-design/` y las ocho decisiones que esperan aprobación **diseñan ese Core**, y ninguna toca el producto que corre. `B-04` sigue siendo el riesgo mejor identificado del repositorio, con su experimento de 31 pasos escrito y sin ejecutar — y **decide sobre un Core que no hay**.

9. **El Knowledge Pack no existe, y esa ausencia es hoy la garantía.** Sin cambios desde agosto en lo sustantivo. **Y con una frase que vale la pena tener a mano**, de `REFINADO-Y-FUENTES`: *«la abstinencia se acaba el día que exista el Knowledge Pack»*. Hoy nada impide citar una norma derogada — **lo impide que el producto no cita normas**. Es una abstinencia, no un control.

10. **Ya hay datos del trabajo real, y siguen sin alcanzar.** ~~«Ni un solo dato sobre el trabajo real de la abogada»~~ — **parcialmente falso**: dos pases sobre expedientes reales dejaron números, y **tres de las ocho preguntas de negocio quedaron contestadas sin haberlas preguntado** — canales (fotografías de un expediente en papel), volumen (decenas de páginas por caso, no centenares) y, a medias, la 7. **Lo que sigue sin existir es lo que más pesa:** con qué frecuencia usa ella cada capacidad, y cuánto le cuesta un caso.

> **Y el titular que no estaba en la lista de agosto, porque nadie lo había medido:**
>
> **La salida que ella firma no se produce sin dos intervenciones suyas** — revisar veinte fichas una por una, y dictar qué escrito, para quién y con qué apartados. **La primera no es rápida.** No es un defecto: es la forma que tiene este producto, y conviene saberla antes de prometer tiempos.

---

## §0.bis — Qué pasó entre el 26 de agosto y el 21 de septiembre

**Sesenta y un commits.** Lo que cambia la respuesta a *¿en qué vamos?*, en cinco líneas:

| | Qué |
|---|---|
| **El producto** | De seis métodos a **quince**, con **veinticuatro programas** que hacen el trabajo mecánico —**trece expuestos al modelo**, once de correr a mano—. **Doce specs** escritas y ejecutadas |
| **La medición** | De cero a **316 pruebas** y cuatro guardas que corren solas sobre todas las salidas: el conteo declarado contra las fichas que hay, todo número que no esté en el material, las afirmaciones prohibidas, y cuántos `SKILL.md` dicen algo |
| **La cobertura** | Los **seis corpus** del repositorio, leídos y triados. Quedaba uno sin cubrir en agosto; hoy ninguno |
| **Lo que encontró ejecutar** | Defectos en los once métodos que se ejecutaron, **ninguno visible releyendo**. Y **ocho de los hallazgos no fueron de los métodos sino de las guardas** que los vigilan |
| **Lo que sigue igual** | Nadie lo ha instalado. **Ninguna abogada ha abierto una sola salida del producto.** No hay una cifra de coste |

### Las tres cosas que este mes enseñó, y que valen más que la lista de arriba

1. **Releer no encuentra defectos; ejecutar sí.** De dieciocho ítems que salieron de *leer* documentos de diagnóstico, **cero** eran como se decían. De los que salieron de *ejecutar* el producto, todos.

2. **Contar a ojo falla, y no es una habilidad que se pueda mejorar.** Seis conteos mal hechos en dos días, todos de la misma operación —*«N de los M métodos»*—, **ninguno encontrado releyendo y los seis con un comando**. El peor fue el cuarto: los números no cuadraban y en vez de recontar se escribió un párrafo explicando la discrepancia. Era plausible y era falsa. De ahí la regla que hoy está en tres métodos: **si el conteo no cuadra, se recuenta; no se explica.**

3. **Una guarda ajustada a una sola muestra protege esa muestra y nada más.** El contador solo entendía la forma en que estaban escritas las salidas que lo estrenaron; sobre las escritas con la plantilla real decía «0 fichas». **Se destapó corriéndolo sobre algo que no escribió quien lo hizo.**

---

## §1 a §4 — Registro del análisis del 2026-08-26

> ### Estos cuatro apartados NO se actualizaron, y no es descuido
>
> Son el **registro fechado** de lo que seis lectores independientes encontraron el 26 de agosto. Reescribirlos borraría lo que se sabía entonces — y de ahí salieron la mitad de las correcciones que vinieron después.
>
> **Qué quedó superado, para que nadie los lea como el estado de hoy:**
>
> | Apartado | Qué decía | Dónde está lo vigente |
> |---|---|---|
> | **§1.1** | «Los seis comandos», con `fact-builder` entre ellos, y **«ninguno se ha ejecutado nunca»** | Son **once**, `fact-builder` es `hechos-con-prueba` desde el 2026-08-26, y **los once se han ejecutado**. `BACKLOG` §§14-15 |
> | **§1.2** | «Los diecisiete hallazgos siguen vivos» | **Cerrados.** Commit `6444952` y `notes-verification/auditoria-inventario-de-bienes-2026-09-05.md` |
> | **§1.3** | Lo que ningún comando cubre | Sigue en pie salvo `revision-de-rigor`, que **existe y se ejecutó** |
> | **§2** | El corpus del dueño, y qué baja a las skills | `BACKLOG` §12: son **89 documentos**, no veinte, y están triados |
> | **§3** | Trece contradicciones | `BACKLOG` §1 las mantiene al día |
> | **§4** | ADRs tocados | `BACKLOG` §7: los dieciocho, leídos y triados, **y ADR-018 cambió la premisa** |
>
> **Y una cosa de §1.1 que envejeció bien y conviene no perder:** su «colisión verificada entre el método y la plataforma» —que los comandos exigen coordenada exacta sobre escaneados sin texto y grabaciones sin transcripción— **se resolvió tal como ese párrafo pedía**: hoy los métodos tienen regla de fallo declarado, el preparador extrae texto con instrumentación de cobertura, y una transcripción es material del caso que el sistema no produce.

---

## §1 — El producto *(registro del 2026-08-26)*

### 1.1 Los seis comandos: cuáles sirven hoy y de qué depende cada uno

Los seis son texto puro: sin servidor, sin herramientas, sin Core. Eso significa que **ninguno depende de algo que falte para arrancar** — pero **ninguno se ha ejecutado nunca**: no hay remoto, no hay instalación, y si los comandos aparecen como `/cronologia` o como `/despacho:cronologia` sigue POR VERIFICAR (H-10). "Sin dependencia externa" es lo verificado; "funciona" es una inferencia que nadie ha comprobado.

| Comando | Qué hace | Dependencias externas declaradas | De qué depende que no existe |
|---|---|---|---|
| `fact-builder` | Hechos atómicos con su prueba, en seis fases | Ninguna. **Nunca ejecutado.** No escribe nada | Es el único de los seis **sin sección "Dónde se escribe"**: nada le impide escribir dentro de `1-Documentos recibidos/`. Su §2.3 describe un "modo B" con garantías del Core en presente, y el Core no existe. |
| `cronologia` | Línea de tiempo con cinco grados de certeza por fecha | Ninguna. **Nunca ejecutado** | Nada externo. Su problema es propio: **calcula duraciones en días** ("(84 días)") dentro del único producto que jura en cuatro archivos que no calcula nada con fechas. |
| `estado-del-caso` | Reconstruye dónde está un caso leyendo la carpeta | Ninguna. **Nunca ejecutado** | Nada externo. **Reescribe `0-Estado del caso` sin copia previa**: es la única escritura destructiva del producto, y la supervivencia de las notas de ella depende de que el modelo las vuelva a teclear bien. |
| `inventario-de-anexos` | Tabla de anexos, emparejamiento en dos direcciones, tres clases de faltante | Ninguna. **Nunca ejecutado** | Su Fase 3 consume "la hoja de hechos del caso, si existe" — artefacto que `fact-builder` no escribe. Y no tiene regla de no sobrescritura, mientras la guía le promete a ella que nunca sobrescribe. |
| `redactar-escrito` | Borrador con parte fáctica redactada y huecos marcados `[[FALTA n]]` | Ninguna. **Nunca ejecutado**, y a medias por diseño | Depende de hechos aprobados y **no hay ningún mecanismo de aprobación**. La producción de `.docx` está POR COMPROBAR en el propio README. Su plantilla imprime cuatro nombres de apartado en duro, contra su propia prohibición. |
| `revisar-documento` | Lee un documento recibido en ocho apartados | Ninguna. **Nunca ejecutado** | Nada externo. Es el único con defensa contra instrucciones embebidas. Su Fase 1 afirma si un anexo "está entre lo recibido" **sin listar la carpeta**, mientras su §1 le prohíbe comparar con el expediente. |

**Colisión verificada entre el método y la plataforma, que no está registrada en ningún documento de diseño.** RIESGO. Los cuatro comandos que exigen coordenada exacta (`cronologia` §1 pide "documento y página, cláusula o **minuto exacto**") chocan con dos límites documentados de Cowork: los PDF que son escaneos sin texto extraíble **no son citables**, y **no existe transcripción de archivos de audio subidos** (el dictado captura habla en vivo, no grabaciones). Un expediente colombiano escaneado y una entrevista grabada son exactamente los dos insumos que estos comandos prometen procesar con coordenada exacta. Hoy ninguno de los cuatro tiene regla de fallo declarado para ese caso, y el fallo probable es una página o un minuto estimados.

### 1.2 Estado de los diecisiete hallazgos de la crítica

El lector del arnés verificó los diecisiete uno por uno contra los archivos. **Todos siguen vivos; solo H-08 está a medias.** Detalló quince; H-14 y el segundo hueco de H-15 no vienen descritos en el material que recibí, así que no los describo. HECHO VERIFICADO para los quince descritos.

| # | Qué es | Estado |
|---|---|---|
| H-01 | La plantilla de `redactar-escrito` Fase 3 imprime «apartado de hechos», «de derecho», «de lo que se pide» y «de anexos» en duro, diecisiete líneas después de prohibir producir la estructura de memoria | VIVO. Es la violación más grave del conjunto y se autodesmiente |
| H-02 | `cronologia` calcula y publica duraciones en días | VIVO |
| H-03 | La frontera del cálculo está trazada por tema (términos, caducidad) y no por operación (sumar o restar días) | VIVO. **El corpus no lo arregla:** `05-temporal-applicability.md` traza la frontera igual de mal. La formulación por operación de la crítica sigue siendo la única buena del repo |
| H-04 | El bloque anti-inyección vive en 1 de 6 comandos; la guía se lo promete a ella sin acotar | VIVO. **Tres de los seis lectores lo nombran por separado como lo más urgente** |
| H-05 | Dos comandos consumen una hoja de hechos que el tercero no escribe | VIVO. Mayor consecuencia de los diecisiete |
| H-06 | `revisar-documento` afirma si un anexo está entre lo recibido sin listar la carpeta | VIVO |
| H-07 | Tres vocabularios para la distinción central: `apoya/contradice/sitúa` en el SKILL, `RESPALDA/CONTRADICE/DA CONTEXTO` en el formato, y la guía **se contradice consigo misma** (§5 enseña "sitúa", su Ejemplo 2 imprime "RESPALDA") | VIVO |
| H-08 | Jerga de ingeniería dentro del plugin | **A MEDIAS.** Se movió `COMO-USARLO-EN-EL-BASELINE.md`, pero el árbol del `README.md` §7 lo sigue dibujando, y `FORMATO-DE-SALIDA.md` §§3-4 conserva `propose_facts`, `item_content_hash`, `PROVENANCE_REQUIRED` y rutas a `docs/technical-design/` — en el mismo archivo que sentencia en su §18 que un documento con "la palabra hash" está mal producido |
| H-09 | El comando más importante se llama en inglés | VIVO. Ventana que se cierra: renombrar después de que ella lo aprenda cuesta el triple |
| H-10 | Nadie ha comprobado si los comandos aparecen como `/cronologia` o `/despacho:cronologia`; la guía publica la forma corta como fiable | POR VERIFICAR en su máquina. Bloquea imprimir la guía |
| H-11 | `inventario-de-anexos` sin regla de no sobrescritura; `estado-del-caso` reescribe sin copia previa | VIVO |
| H-12 | La única defensa contra la cita fantasma es que el modelo declare que abrió cada cita | VIVO |
| H-13 | Tablas de Markdown en `.txt` pegadas en Word son una hilera de tuberías; "lista para pegar" falla al primer intento | VIVO |
| H-14 | — | No descrito en el material que recibí |
| H-15 | Tres huecos de capacidad. Descritos: **15.1** nadie coteja dos documentos (`revisar-documento` lo prohíbe explícitamente); **15.3** nadie consolida en una lista lo que hay que pedir | VIVOS |
| H-16 | Ni audio ni PDF escaneado sin capa de texto están en la tabla de comprobaciones pendientes del README, y el Ejemplo 2 de la guía —el que le enseña el producto entero— depende de citar el minuto de una grabación de 47 minutos | VIVO, y agravado por el §1.1 de arriba |
| H-17 | Fricción de la Fase 2 de `redactar-escrito`: dictar la estructura completa cada vez | VIVO. Correctamente pospuesto: la fricción solo se mide usando |

### 1.3 Lo que el producto no hace y ningún comando cubre

- **Nada revisa el borrador propio antes de que salga con su firma**, cuando `redactar-escrito` se declara a sí mismo el comando más peligroso del despacho. Es el único hueco del oleoducto actual.
- **Nadie coteja dos documentos.** `revisar-documento` tiene prohibido comparar con el expediente.
- **Nadie consolida lo que hay que pedir.** Los cinco comandos producen vacíos, ausencias y afirmaciones sin documento, cada uno en su propia salida, y ninguno junta la lista.
- **Ningún comando sabe que su salida envejeció** cuando entra material nuevo a la carpeta.
- Y la mitad de salida del oficio no está: investigación de fuentes, actuaciones y recursos, petición, audiencias, contestación, comunicación con cliente, conciliación.

---

## §2 — El corpus del dueño *(registro del 2026-08-26)*

Veinte dossiers de workflow, seis de práctica, dieciocho fichas de candidata, siete documentos de evaluación, cinco de catálogo de fuentes, siete de mapas de dependencia y una decena de gobierno. Es mucho trabajo y no es ruido. Pero **no es lo que el proyecto necesitaba que fuera**, y conviene decirlo entero.

### 2.1 Qué aporta de verdad — piezas que no existen en ninguna otra parte del repositorio

| Pieza | Dónde | Por qué vale |
|---|---|---|
| **El contrato de salida del séptimo comando, ya escrito** | `workflows/20-judicial-rigor-review.md` | Trece campos por hallazgo y cinco veredictos cerrados. Única pieza del corpus convertible en `SKILL.md` sin inventarle la forma |
| **El lenguaje de riesgo calibrado** | `workflows/20`, §"Lenguaje de riesgo permitido" | Los seis skills solo tienen listas de prohibiciones. **Nadie dice cómo se escribe una advertencia legítima.** Sin ese permiso el modelo hace una de dos cosas, ambas malas: se calla el riesgo, o lo dice mal |
| **Cuatro capas de procedencia del estado** | `workflows/17-case-status-review.md` | `/estado-del-caso` solo distingue "está o no está en la carpeta". No sabe qué hacer con una captura de portal judicial. Y la fórmula "la última actuación **localizada**, no la ocurrida" es mejor que la del skill |
| **La matriz de pronunciamiento hecho por hecho** | `workflows/19`, rama C | Método puro: cada hecho de la demanda contraria con su localizador y su casilla. Ningún comando lo tiene |
| **La transcripción nunca es el original** | `workflows/02` y `docs/skills-support/evals/hearing-and-contradiction-fixtures.md` | `fact-builder` y `cronologia` ya aceptan localizadores de audio como si fueran coordenadas de la grabación, y no advierten que la atribución de hablante puede ser del transcriptor |
| **Las cuatro fechas de un mismo acto** | `05-temporal-applicability.md` §4 | Expedición / publicación / notificación / desde cuándo produce efectos. `cronologia` ya tiene tres pares de fechas en su tabla de trampas; le falta la cuarta familia, que es la que aparece en toda providencia |
| **Las cinco preguntas de regla especial sobre regla general** | `legal-dependency-maps/README.md` | Método puro, sin una sola norma dentro. No tiene casa porque ninguna skill investiga |
| **El control de pertinencia negativa** | `source-catalog/jurisprudence-sources.md` | `J-CC-T200-2026` registrada como identificada **y descartada, con la razón**. Es la idea metodológica más valiosa del corpus y es cara de obtener |
| **Los criterios para NO construir una skill** | `03-priority-roadmap.md` (señal de parada), `03-skill-priority-roadmap.md` (gate de seis), `02-skill-boundary-matrix.md` (no duplicación), `00-scope-and-principles.md` §3 (prueba ácida de ubicación) | El producto tiene seis skills y **ninguna regla escrita para decidir la séptima.** Aquí está, en cuatro piezas, y es directamente adoptable como política del plugin |
| **La capa de inyección sembrada** | Cinco fixtures independientes: `E-05`, `SRC-PET-04`, `E-DR-05`, la nota al pie de `RV-02`, el fragmento `00:15:01`, más `ADV-PI-01` | Cargas útiles ya redactadas en cinco formatos distintos. Convierte H-04 de promesa en algo medible |
| **La regla de custodia del truth set** | `docs/skills-support/evals/adversarial-benchmark.md` | Fuera del prompt, fuera de los recursos de la skill, fuera de la carpeta del caso. Es lo único del repo que puede decir si el método funciona **sin creerle al modelo** |
| **La regla de antilavado de conocimiento** | `04-source-governance.md` §7 | La mejor formulación del proyecto de por qué el derecho no puede vivir dentro de una skill |
| **La separación regla legal / instrucción institucional / capacidad técnica / práctica de oficina** | `workflows/10-digital-litigation.md` | Nombra el fallo exacto que este producto puede provocar: confundir la capacidad de Word o Drive con cumplimiento procesal. Lectura obligada antes de cualquier conector |
| **Un resultado negativo caro y no fabricable** | `06-colombian-law-coverage-ledger.md` + `09-legal-completeness-audit.md` | 29 workflows auditados, **ninguna fila con cobertura cerrada**, `COVERAGE_GAPS_PRESENT`. Conteos reproducibles (25 transición / 24 jurisprudencia / 19 territorio en brecha). Convierte la regla dura 1 de decisión de arquitectura en hallazgo empírico |

### 2.2 Qué duplica

**Dentro del corpus.** Cinco duplicaciones confirmadas archivo por archivo, todas con deriva ya empezada:

- **Los dos ledgers.** `workflows/coverage-matrix.md` abre diciéndose "el Coverage Ledger del corpus"; `06-colombian-law-coverage-ledger.md` se titula igual. Mismas 29 filas, **dos vocabularios de estado incompatibles y dos espacios de identificadores**. Peor: los `W01–W29` del segundo **colisionan numéricamente** con los nombres de archivo de `workflows/` (W12 = revisión de demanda / `workflows/12` = tutela; W16 = petición / `workflows/16` = clasificación documental; W18 = tutela / `workflows/18` = audiencia). Quien siga un ID aterriza en el archivo equivocado, y ya hay un archivo citando "W16/W17" sin decir a qué espacio pertenece.
- **"Rigor judicial" está escrito tres veces con dos contratos incompatibles.** `08-adversarial-review-framework.md` (ficha de **7** campos), `adversarial-review/judicial-rigor.md` (21 líneas), `workflows/20` (ficha de **13** campos). `08` enlaza a `adversarial-review/*` y **nunca a `workflows/20`**; `workflows/20` no enlaza a ninguno. Súmense `workflows/08`, `skill-candidates/adversarial-review.md` y `docs/skills-support/evals/adversarial-benchmark.md`: seis archivos sobre la misma capacidad.
- **Un dossier huérfano y divergente.** `practice-areas/colombia-practice-area-dossiers.md` cubre las mismas seis áreas que los seis dossiers individuales, es la versión anterior, **ningún archivo lo enlaza** (su enlace se borró hoy), y ya divergió en dos filas.
- **Los seis gates escritos dos veces**, con distinto orden y distintas palabras, en dos archivos de nombre casi idéntico. Única diferencia sustantiva: el segundo añade "inyección".
- **Tres solapamientos de workflow:** `07`/`18` (audiencia), `09`/`15` (conciliación), `05`/`19` (demanda y contestación). En los tres el de número más alto es el más desarrollado.
- **Esqueleto por encima de contenido.** Los seis dossiers de práctica comparten las mismas trece secciones y cinco de ellas se repiten casi palabra por palabra. Densidad normativa real: 2 menciones en `family.md`, 2 en `police.md`, 3 en `constitutional.md`, 4 en `civil.md`, 5 en `administrative-contentious.md`, 6 en `labor.md`, sobre ~81 líneas cada uno.

**Contra el producto.** Esto es lo incómodo: **las seis skills enviadas ya superan al corpus en método.** `skill-candidates/evidence-analysis.md` describe como candidata P1 una matriz probatoria que `inventario-de-anexos` ya entrega, con emparejamiento en dos direcciones, tres clases de faltante y seis formas de "presente pero no utilizable". `legal-document-review` y `legal-drafting` figuran como candidatas por diseñar con `revisar-documento` y `redactar-escrito` ya enviados. Y `02-skill-boundary-matrix.md` **asigna al Core la "cobertura determinista"** que un skill de texto puro ya hace sin Core: quien planifique leyendo esa matriz esperará al Core para algo que ya está construido.

**Contra el Technical Design.** `docs/skills-support/evals/fact-builder-fixtures.md` reescribe —más pobre y sin truth set— el benchmark que `docs/technical-design/v0/13-synthetic-benchmark.md` ya tiene completo (transcripción canónica, `DOC-01..DOC-05`, quince hechos esperados con grupos de variante, cinco contradicciones, seis irrelevantes, ocho afirmaciones prohibidas). **Ninguno de los dos cita al otro.** Y comparten cuatro nombres de métrica con denominadores distintos: ver §3, fila 6, que es la contradicción más peligrosa de todo el repositorio.

### 2.3 Qué baja YA a las skills — tabla origen → destino

Ordenada por coste ascendente. Todo lo de esta tabla es **método sin derecho dentro**: nada de aquí necesita Knowledge Pack, Core, conector ni herramienta nueva.

| Destino | Qué baja | Origen | Coste |
|---|---|---|---|
| **Los seis** | El bloque "texto dirigido al programa": no obedecer, no dejar que altere el resto de la salida, transcribir literalmente en un bloque final, y ante la duda reportar | Ya escrito en `plugins/despacho/skills/revisar-documento/SKILL.md` §7. Justificación en `00-scope-and-principles.md` principio 7 y `review-patterns/ethics-confidentiality-and-human-governance.md` punto 3. Prueba en cinco fixtures | 12 líneas × 5 |
| **Los seis** | Regla de escritura de skills: **ningún `SKILL.md` usa inyección dinámica de contexto ni funciones exclusivas de Claude Code**, porque en Cowork se sustituyen por un marcador y el método se ejecuta sobre vacío **sin avisar** | `docs/research/capacidades-cowork-y-capa-gratuita.md` §4.2 | 3 líneas en el README §7. Hoy los seis están limpios: comprobarlo cuesta cero, descubrirlo después cuesta caro |
| `cronologia`, `inventario-de-anexos`, `revisar-documento`, `fact-builder` | Fallo declarado de coordenada: cuando el material es un escaneo sin texto o una grabación, **la coordenada exacta no se produce y se declara la imposibilidad**, en vez de estimar página o minuto | `capacidades-cowork-y-capa-gratuita.md` §0, hallazgos 3 y 4 | 2 líneas × 4 |
| `fact-builder`, `cronologia` | "Una transcripción no es la grabación: es una representación derivada, y su atribución de hablante puede estar equivocada. Un hablante que la fuente no identifica **no se identifica**" | `workflows/02` §Entradas; `docs/skills-support/evals/hearing-and-contradiction-fixtures.md` HC-01 | 2 frases. Cierra una clase entera de alucinación que ninguna otra regla cubre |
| `inventario-de-anexos` | Original / representación derivada como marca obligatoria de cada fila: qué se tiene realmente (original, copia, escaneo, captura, transcripción) y si el original existe entre el material | `skill-candidates/evidence-analysis.md`, `skill-candidates/hearing-analysis.md` | Una columna. Hoy §3 distingue **quién produjo** el documento, que es otra cosa |
| `inventario-de-anexos` | Dos chequeos mecánicos: (a) el nombre del archivo no prueba su contenido — advertir la discrepancia; (b) duplicados candidatos agrupados y **nunca eliminados ni fusionados** | `workflows/16-document-classification.md` §Evaluaciones | 4 líneas. Son los dos errores caros de una tabla de anexos |
| `cronologia` | Una fila más en la tabla de trampas: un acto trae fecha de expedición, de publicación o notificación y una mención a desde cuándo produce efectos. **Se registran todas, diciendo cuál es cuál, sin decidir cuál manda** | `05-temporal-applicability.md` §4 | 1 fila + 1 contrapregunta. No es derecho: no dice cuánto dura nada |
| `fact-builder`, `cronologia` | Contrapregunta de emparejamiento cruzado: "¿algún emparejamiento cuelga una prueba de un hecho de otra fecha o de otro episodio?" | `technical-design/v0/13-synthetic-benchmark.md` §13.4, prohibidas PA-06 y PA-07 | 1 línea × 2. La pregunta 7 de `fact-builder` ya cubre la cita fantasma; **este fallo es más fino y se le escapa** |
| `estado-del-caso` | Un documento en la carpeta es una **copia de trabajo**, no el expediente: dice que alguien lo guardó, no que sea la versión vigente ni lo último que ocurrió. Más la fórmula "última actuación **localizada**" | `practice-areas/police.md` y `administrative-contentious.md` §Documentos comunes; `workflows/17` etapa 3 | 3 líneas. Hoy el skill cubre magníficamente el lado negativo de la carpeta y **no cubre el positivo** |
| `estado-del-caso` | Tratamiento de la observación externa: una captura de portal o un correo reenviado se registra como observación fechada con identidad de proceso por confirmar, **nunca como constancia** | `workflows/17` etapas 3 y 5, traducido a palabras llanas | 4 líneas. **Sin las etiquetas en mayúsculas** (ver §3, fila 13) |
| `estado-del-caso` | La justificación que falta a su propio diseño: todo lo que importe tiene que quedar **escrito en la carpeta**, porque archivar un proyecto borra su memoria de forma irreversible | `capacidades-cowork-y-capa-gratuita.md` §2.3 | 1 línea |
| `redactar-escrito` | Al cierre §8, una línea fija que niegue lo que el borrador **no** afirma: que no se dice si es procedente, completo, oportuno ni apto para radicar, y que la clase de escrito la eligió ella | Las tres fichas MERGE: `demand-assistance.md`, `petition-assistance.md`, `appeal-assistance.md` | 2 líneas. Hoy "listo para presentar" solo se prohíbe en la autoevaluación interna, **que ella no lee** |
| `redactar-escrito` | Prohibición de afirmar completitud: nunca "se anexan todos los soportes". Los anexos se enumeran uno por uno desde el inventario | `docs/skills-support/evals/adversarial-benchmark.md` ADV-06; `RV-02` párr. 5 | 2 líneas. Es **la única afirmación falsa del producto con consecuencias procesales directas** |
| `redactar-escrito` | Al cierre de §3.2: un modelo acredita cómo se escribió **ese** escrito, no que sus apartados sean exigibles ahora. Se dice de qué modelo viene y de qué fecha es | `practice-areas/civil.md` y `administrative-contentious.md` | 1 párrafo |
| `revisar-documento`, `redactar-escrito` | El **lenguaje de riesgo permitido**: las fórmulas calibradas que sí se pueden escribir, junto a las prohibidas que ya están. Y que cada hallazgo venga con una línea de "qué lo confirmaría o lo desmentiría" | `workflows/20` §Lenguaje de riesgo permitido; `skill-candidates/adversarial-review.md` | Media hora. Es la mitad positiva que a los seis les falta |
| `redactar-escrito` | El **método** de la matriz de pronunciamiento hecho por hecho, cuando el escrito es una contestación: cada hecho del documento recibido con su localizador y una casilla que llena ella. **Los tres rótulos no bajan** (§3, fila 2) | `workflows/19` rama C | Media hora, y solo como estructura disponible, nunca como comando propio |

**Lo que NO baja, y conviene decirlo:** las dos mejores piezas del dominio de áreas —las cinco preguntas de regla especial sobre regla general, y el control de pertinencia negativa— **no tienen casa**, porque ninguna de las seis skills investiga. Son el núcleo de una capacidad futura, no material para hoy.

---

## §3 — Contradicciones detectadas, y cuál cede en cada una *(registro del 2026-08-26)*

Primero, lo que se comprobó y **no está roto**, para que nadie gaste tiempo ahí: el corpus **no propone en ninguna parte meter derecho colombiano dentro de un `SKILL.md`** —dice lo contrario de forma repetida y disciplinada—; **no toca la superficie MCP** (ningún archivo propone una tool nueva, y `open-questions/architecture-alignment.md` está al día con las cuatro enmiendas); **no amenaza la polaridad del EvidenceLink** (una sola mención en todo el corpus, y correcta); y **ninguno de los seis ADRs `Accepted` cae**. En materia de cálculo de términos el corpus es **más estricto que el producto**, no menos.

Lo que sí hay:

| # | Contradicción | Dónde | Cuál cede |
|---|---|---|---|
| 1 | El corpus manda identificar "clase observable: … providencia, **notificación**, prueba documental". Esas no son clases observables: son calificaciones jurídicas, y el producto las prohíbe con nombre propio ("Es una notificación" está en la columna **Mal**) | `workflows/16` paso 2 vs `revisar-documento/SKILL.md` y `inventario-de-anexos/SKILL.md` | **Cede el corpus.** Reescribir el paso 2 con clases realmente observables (extensión, firma, membrete, cómo se titula) |
| 2 | La matriz de contestación propone la tríada **admitir / negar / no constar**. Eso no es método: es la forma del pronunciamiento, y "la forma de un escrito también es derecho" | `workflows/19` rama C vs `redactar-escrito/SKILL.md` §3.2 | **Cede el corpus en los rótulos**, sobrevive el método hecho-por-hecho con localizador. Los rótulos los dicta ella o vienen del documento que se contesta |
| 3 | **La fecha de la Ley 2452 está afirmada, negada y condicionada en tres archivos a la vez.** `19` ordena separar procesos por el 2 de abril de 2026 "conforme a la transición **documentada**"; `05` dice que mientras no se confirme contra fuente primaria **ninguna Skill puede afirmar** qué código gobierna un expediente laboral. El nudo real: la matriz marca `VERIFIED_OFFICIAL`, que acredita **identidad de la fuente**, y `19` lo lee como **vigencia confirmada** — el uso que `04-source-governance.md` §4 prohíbe expresamente | `workflows/19`, `05-temporal-applicability.md`, `source-catalog/temporal-law-matrix.md`, `04-source-governance.md` | **Ceden `19` y la lectura de la matriz.** Degradar a "cuestión fechada por confirmar"; separar en dos celdas identidad y vigencia. **Y no baja a ninguna skill en ninguna de sus tres versiones** |
| 4 | El dossier del área más sensible declara la fuente de protección `POR_VERIFICAR` y no nombra ni una vez las cinco leyes que **sus propios archivos hermanos** registran como fuente oficial verificada, con Diario Oficial y fecha | `practice-areas/family.md` vs `legal-dependency-maps/family-protection-supports.md` y `source-catalog/normative-sources.md` | **Cede `family.md`.** No había que inventar nada: había que copiar del archivo de al lado |
| 5 | El gobierno de jurisprudencia define **cinco estados no booleanos** y la regla "encontrar una providencia no demuestra que sostenga una proposición". El ledger establece que "un ID de catálogo equivale a SÍ". Resultado: filas con `jurisprudence_check = YES` apoyadas en **buscadores institucionales**, y una fila con `YES` y **cero identificadores de providencia** | `07-jurisprudence-governance.md` vs `06-colombian-law-coverage-ledger.md`, `claim-source-matrix.md`, `09-legal-completeness-audit.md` | **Ceden `06` y `09`.** La regla vale para lo normativo y es falsa para lo jurisprudencial. Y `legal_reference_count = 36` está inflado: providencias individualizadas hay 4, utilizables 2 |
| 6 | **La más peligrosa.** Cuatro métricas con el mismo nombre y denominadores distintos en dos archivos que **no se citan entre sí**. `unsupported_fact_rate` en el Technical Design mide sobre **items intentados, incluidos los rechazados por el Core**; en el corpus, sobre **afirmaciones de la salida**. Y el baseline ya había fijado la regla que el corpus ignora: **toda medida lleva prefijo `b_`** para que nunca se confunda con su homónima "en una tabla, una diapositiva o una conversación de pasillo" | `docs/skills-support/evals/fact-builder-fixtures.md` vs `technical-design/v0/13-synthetic-benchmark.md` §16.3–16.7 vs `discovery/baseline-analisis-y-rubrica.md` §3 | **Cede el corpus.** El Technical Design manda por precedencia y además **es el único que tiene truth set escrito**; el del corpus lo describe en imperativo y lo deja como tarea |
| 7 | **"Parcialmente respaldado" nombra tres cosas.** El fixture se lo **exige** al sistema; `FORMATO-DE-SALIDA.md` §1.4 lo **prohíbe** con argumento ("es la señal de que el hecho está redactado con el grano equivocado"); el Technical Design lo usa con **otro referente** (prueba en los dos sentidos); y ADR-003 tiene enum **cerrado** de tres estados | `docs/skills-support/evals/fact-builder-fixtures.md`, `fact-builder/FORMATO-DE-SALIDA.md`, `13-synthetic-benchmark.md`, ADR-003 | **Ceden el fixture y el rótulo.** El producto y ADR-003 van en la misma dirección; el caso "prueba en ambos sentidos" ya se llama **"Respaldado y contradicho"**. Tal como está, **el fixture no puede puntuar al producto: mide otra cosa** |
| 8 | `CaseRevision` es regla común de ejecución de los evals y de ella cuelgan tres pruebas de obsolescencia. `grep` sobre los seis `SKILL.md`: **cero coincidencias** | `evals/README.md` vs `plugins/despacho/` | **Cede el nombre, sobrevive la idea.** Al producto le falta el concepto —una hoja de hechos aprobada envejece en silencio— pero no puede entrar con ese nombre |
| 9 | Dos vocabularios de etiquetas conviviendo. Lo raro: **la tabla que prevalece es más pobre que la derogada** en el punto que más importa — no tiene equivalente para `OBSERVED / USER-CONFIRMED` ni `RESEARCH-INFERRED`, que son la columna vertebral del mapa de capacidades. 22 archivos usan las inglesas, 16 las españolas | `00-scope-and-principles.md` §5 vs `00-scope-and-governance.md` | **Nadie cede todavía.** Antes de migrar hay que **añadir a la tabla vigente las dos etiquetas que le faltan**. Migrar hoy pierde información |
| 10 | Dentro del mismo skill: la Fase 5 lista tres estados, el formato lista cuatro, y **"No verificable con este material" no existe en la tabla cerrada ni tiene contraparte en ADR-003**. Es el único estado del producto sin ancla | `fact-builder/SKILL.md` Fase 5 vs `FORMATO-DE-SALIDA.md` §1.4 | DECISIÓN PENDIENTE. Hay que unificar en **una** lista. Es exactamente el tipo de cosa que diverge sola |
| 11 | El corpus afirma que solo existe una skill, **en un archivo editado el día siguiente** al commit que trajo las otras cinco. En cadena: `workflows/README.md` marca "17 — Estado del caso" como **P2 DEFER** con `/estado-del-caso` desplegado; `16` dice "no se propone todavía como Skill autónoma" con dos comandos desplegados; y `cronologia`, `estado-del-caso` e `inventario-de-anexos` **no existen en ninguna parte del corpus** — ni ficha, ni fila en la matriz, ni mención en el mapa de capacidades | `skill-candidates/INDEX.md` línea 3 y siete archivos más | **Cede el corpus** — y su propio README lo ordena para el caso de conflicto con la arquitectura. Pero **falta la regla para este caso**: qué se hace cuando el producto adelanta a la investigación. Nadie la escribió |
| 12 | La matriz de fronteras asigna a **Core/Application** la "cobertura determinista" y a una candidata inexistente la matriz probatoria. Las dos cosas ya las hace un skill de texto puro, sin Core | `02-skill-boundary-matrix.md` vs `inventario-de-anexos/SKILL.md` | **Cede la matriz.** Le faltan tres filas y le sobra esa asignación |
| 13 | La etiqueta `CONFIRMADO_EN_REGISTRO` supone un "registro canónico disponible". ADR-002 invariante 1: **nada de lo que vive en el espacio del usuario es canónico** | `workflows/17` §Salidas vs ADR-002 | **Cede la etiqueta, sobrevive la distinción.** Si baja tal cual, la carpeta pasa a llamarse registro, que es lo único que ADR-002 prohíbe nombrar así |
| 14 | **Quién actualiza.** ADR-012 Decisión 3: el lanzador "**le pregunta a ella**". ADR-013 Contexto: "DECISIÓN APROBADA (dueños): las actualizaciones **las hace el dueño presencialmente**; ella nunca toca el repositorio". ADR-012 pregunta 9 lo sigue listando como pendiente | ADR-012 vs ADR-013 | **Sin resolver, y ahora peor:** bajo la vía plugin el botón Update está **en la interfaz de ella** |
| 15 | La guía se contradice consigo misma: §5 le enseña "sitúa", su Ejemplo 2 imprime "RESPALDA". Y promete que "nunca sobrescribe un archivo que ya está en `2-Borradores`" cuando `inventario-de-anexos` sí lo hace | `GUIA-PARA-LA-ABOGADA.md` | **Cede el Ejemplo** en el primer caso. En el segundo **cede el producto**: hay que arreglar el skill, no rebajar la promesa |
| 16 | El inventario de capacidades encabeza su §2.2 con "(resuelve B-04)" y **no lo resuelve**: acredita el confinamiento del acceso a archivos del agente, no el del proceso del servidor MCP. Es la extrapolación que el propio spike prohibió | `capacidades-cowork-y-capa-gratuita.md` §2.2 | **Cede el encabezado.** Un documento cuya autoridad viene de no extrapolar no puede extrapolar en su título |

---

## §4 — Decisiones de arquitectura tocadas *(registro del 2026-08-26)*

Tres hechos de plataforma, verificados con cita literal y refutación adversarial en `docs/research/capacidades-cowork-y-capa-gratuita.md` (2026-08-25). HECHO VERIFICADO los tres:

- **(a)** No existe deny por ruta en Cowork para un usuario individual — *"Unrestricted. Users can attach any folder they have OS-level access to"*. El modo solo-lectura y la lista blanca de carpetas **solo existen bajo administrador** (MDM, Team/Enterprise). Y el material que se abre **se procesa en servidores de Anthropic**.
- **(b)** *"Local MCP servers don't run in sessions in the cloud"* + *"sessions run in the cloud by default"*.
- **(c)** *"A Git repository that contains plugin packages can serve as a marketplace"*.

**Lo primero, y es una buena noticia que hay que saber leer: ningún ADR `Accepted` cae.** No es suerte. Es el pago de haber escrito ADR-001 a ADR-006 como decisiones independientes del anfitrión, con la fórmula repetida "ninguna capacidad de Cowork se convierte en regla del Domain". Lo que cae es el **mecanismo**, que siempre estuvo declarado como detalle de plataforma. Esa disciplina se acaba de amortizar entera.

**El daño se concentra en ADR-012 (Proposed), y recomiendo sucesor, no enmienda.** RIESGO si se enmienda: un ADR cuyo título miente sobre su propia decisión es peor que uno superseded.

- (c) le quita el objeto al título ("repositorio clonado"), a la Decisión 3 entera, a dos consecuencias negativas, a tres preguntas pendientes y a **seis de sus dieciocho pruebas** (D-01, D-02, D-03, D-06, D-07, D-14).
- Su §10 declara **POST-V0** el plugin —con trigger "segunda oficina o segunda máquina"— que **el repositorio ya adoptó** sin que el trigger se cumpliera.
- Su rechazo del plugin ("con una usuaria conocida el plugin no compra nada que el clon no da") **es falso**: compra que ella no necesite git ni credencial contra el remoto, que no exista working tree que `git clean -fdx` pueda borrar, **espacio de nombres** frente al fallo silencioso por choque de nombres, y actualización en un botón.
- Su §9, la contingencia escrita para B-04, **está escrita para el fallo equivocado**: propone un proceso independiente con stub de transporte MCP, y bajo (b) **el stub tampoco corre**.
- Su invariante 10 ("la única carpeta adjuntada a Cowork es la zona 2") **no es un invariante**: es una conducta del usuario, y (a) verifica lo contrario. Es el mismo defecto que el propio ADR condena en `.gitignore`.
- Su rechazo del servicio en la nube argumenta que "añade un principal nuevo… el operador de la infraestructura". Con (a), **ese principal ya existe**. El rechazo sigue siendo correcto por sus otros cuatro argumentos; ese hay que retirarlo.
- **Se salvan intactas y son excelentes:** Decisiones 1, 2, 4, 5, 6, 7 y 8.

**ADR-002 necesita dos enmiendas.** Su decisión entera sobrevive. Pero (1) su pregunta pendiente "POR VERIFICAR: garantías de Cowork sobre carpetas locales" está **resuelta y desfavorable**, y una pregunta abierta cuya respuesta ya se conoce es peor que no haberla hecho; y (2) **ningún ADR `Accepted` distingue custodia local de procesamiento local**. Mientras no esté escrito, cualquier lector del corpus —incluido un agente futuro— concluirá que el material no sale del equipo.

**Los demás, en una línea cada uno.** ADR-006: su enforcement es "la operación que cruzaría la frontera no existe", y (b) crea un modo en que **no existe ninguna operación**; la frontera no se cruza, se vuelve inaplicable. ADR-009: en modo nube el log queda vacío, y **un log vacío es ambiguo** entre "no pasó nada" y "todo pasó fuera del Core". ADR-010: la superficie puede estar **ausente entera**, y no hay condición para ese estado. ADR-007: su requisito 9 de localidad es lo único que (b) amenaza, y el propio ADR ya declara que eso "no es sustitución de adapter: es cambio de arquitectura". ADR-013: su predicado B1 queda vacío bajo (c), y su §12 trata como futura una decisión que (a) ya disparó.

**El cambio que más importa.** La pregunta bloqueante del proyecto **ya no es B-04**: es **¿puede una cuenta Pro individual forzar sesión local?** El interruptor solo está documentado como control de administrador en Team y Enterprise. Si la respuesta es no, el Core no puede ser un MCP local en su plan, y las tres salidas —plan Team, Core como MCP remoto, u otro anfitrión— **no están diseñadas**, y las dos primeras reabren ADR-002 y ADR-007.

**Y el peor modo de fallo del proyecto, hoy cubierto por una prueba y no por un invariante:** en modo nube no hay Core, no hay `ingest_evidence`, no hay registro de autorizaciones, no hay log — **y el modelo sigue respondiendo con fluidez sobre la carpeta adjuntada.**

**Un acoplamiento oculto que nadie ha escrito.** RIESGO. Las seis `description` de los skills miden ~600 caracteres y su frontmatter incluye `version`, campo que no admite la vía de subida de ZIP a claude.ai (techo de 200 caracteres, seis campos). **Hoy funcionan solo porque la vía es el plugin.** Si alguna vez se cae de vuelta a esa vía —la única candidata gratuita—, los seis fallan de validación o se truncan.

---

## §5 — Lo que hay que hacer ahora

> **Las diez entradas de agosto se cerraron, menos dos, y las dos que quedan no son de código.** Abajo va el balance de aquellas diez, y después lo que hay que hacer **hoy**, que es otra lista y mucho más corta.

### 5.1 Balance de las diez entradas de agosto

| # | Entrada | Estado el 2026-09-21 |
|---|---|---|
| **1** | Decir la verdad sobre dónde se procesa su material, y comprobar en su máquina | **A medias, y la mitad que falta es la que importa.** La guía ya lo dice, en tres párrafos y con la confusión nombrada. **La comprobación en su equipo no se ha hecho** — sigue siendo la entrada 1, ahora en §5.2 |
| **2** | El bloque de texto dirigido al programa, en los seis comandos | **HECHO**, y en los **once**. Comprobado ejecutando: la inyección del `caso-02` está escrita para romper la negativa de `preguntas-de-derecho` y no alteró ninguna de las cuatro respuestas |
| **3** | Limpiar `fact-builder`: vocabulario, jerga y nombre | **HECHO** el 2026-08-26 (`H-08`, `H-09`). Se llama `hechos-con-prueba` |
| **4** | Sacar la aritmética de fechas, y escribir la frontera por operación | **HECHO, y dos veces.** En agosto se puso en tres métodos; **eran siete**, y los otros cuatro se quedaron diez días sin ella. Una sola redacción en los siete desde el 2026-09-05, con prueba de mutación — y una guarda que busca toda cifra que no esté en el material |
| **5** | Vaciar la plantilla de apartados de `redactar-escrito` | **HECHO** (`H-01`). Los títulos salen de ella o se preguntan |
| **6** | No sobrescribir, y no afirmar sin haber mirado | **HECHO** (`H-06`, `H-11`). `revisar-documento` lista la carpeta antes de decir que falta un anexo, y ninguna salida se sobrescribe |
| **7** | La hoja de hechos revisada: cerrar la cadena | **HECHO y ejecutado.** Es SPEC-05. Probado en los tres estados —cero marcadas, una, dos— y **los tres se comportan bien**. Lo que sigue sin saberse es si **ella** va a hacerlo, que era la otra mitad de esta entrada y es de §6 |
| **8** | «Qué comprobar primero» al cierre de las seis salidas | **HECHO** (`H-12`), y en los once |
| **9** | Sincronizar el corpus con el producto, y escribir la regla que falta | **DECIDIDO, no sincronizado, y la decisión es la regla que faltaba:** los 55 documentos que nombran `fact-builder` **se dejan como están** porque son registro histórico; se corrige solo lo que afirma un hecho sobre el presente. `BACKLOG` §12 |
| **10** | El séptimo comando: «qué hay que pedir» | **NO se hizo ese, y se hicieron otros cinco.** El producto pasó de seis a once métodos, y entre ellos `revision-de-rigor` — que era el candidato que este mismo documento llamaba *«el único hueco del oleoducto: nada revisa el borrador antes de que salga con su firma»*. **«Qué hay que pedir» sigue sin construirse** |

### 5.2 Lo que hay que hacer hoy

**Tres entradas, y ninguna es mía.** Todo lo que se podía hacer sin ella y sin el dueño está hecho.

#### 1. Instalarlo una vez en una máquina que no sea la del dueño

**Es lo que haría si solo pudiera hacerse una cosa, y ahora desbloquea cuatro.**

- **Qué.** Instalar el plugin desde el marketplace y anotar: la forma real de los comandos (`/cronologia` o `/despacho:cronologia`), si `md2docx.py` produce el `.docx`, si un `.md` abre con doble clic en Windows, y **en qué anfitrión corre** — de eso último depende si existe alguna protección además de la prosa (`BACKLOG` §13).
- **Qué desbloquea, y por eso va primera.** Cerrar SPEC-01 y SPEC-11 · imprimir la guía · el disparador del plano administrativo y el de actualizaciones automáticas, **dos exclusiones del backlog de arquitectura que esta instalación enciende** · y la comprobación pendiente de la entrada 1 de agosto.
- **Cuánto cuesta.** Una tarde. **Lleva abierta desde la primera fase del proyecto.**

#### 2. Que una abogada abra una de las salidas

- **Qué.** Ponerle delante **una** — la hoja de hechos del `caso-03`, o la revisión de rigor del `caso-02`— y mirar tres cosas: si la abre, si la entiende sin que nadie se la explique, y **si copia algo de ahí y lo pega en un escrito sin tocarlo**.
- **Por qué es la medición que falta.** Hay 208 pruebas y cuatro guardas, y **todas miden que el producto cumple sus propias reglas**. Ninguna mide que le sirva a alguien. `PENDIENTE-FORMA-DE-ENTREGA` lo dijo en agosto: *«la prueba no es que el archivo se vea bien en el editor, sino que ella lo abra con doble clic, lo copie y lo pegue en su escrito sin tocar nada»*.
- **Y hay un dato que hay que darle con la salida, no después:** revisar veinte fichas una por una es la puerta de entrada al producto, y **nadie ha medido cuánto tarda**.

#### 3. Las tres conversaciones que están escritas y sin tener

Ninguna es una tarea: son preguntas con la redacción ya hecha, esperando veinte minutos.

| Qué preguntar | Por qué ahora | Dónde está la redacción |
|---|---|---|
| **Cuál es el expediente que vale cuando ella decide** (pregunta de negocio 7) | Dejó de ser una pregunta sobre un contexto que no se levantaba: **el contexto B se levantó**, y de la respuesta depende si la frase que justifica la protección de escritura más fuerte del producto es verdad ahí | `discovery/business-questions-next.md` §7 |
| **Si hay copia de seguridad de algo, hoy** (pregunta 6) | Se marcó como no bloqueante del diseño pero sí del **paso a expedientes reales**, y ese paso **ya se dio dos veces**. El riesgo que nombra —*«el robo del portátil destruye y expone todo a la vez»*— está vigente ahora | `discovery/business-questions-next.md` §6 |
| **Qué de una propuesta de decisión reescribiría siempre ella** | Es la misma conversación que la primera, y conviene que sea una sola | `skills-support/open-questions/questions-for-professional.md` §6 |

---

## §6 — Lo que está bloqueado, y por qué pregunta

**Cinco de las nueve filas de agosto se cerraron.** Abajo va lo que sigue bloqueado, y después qué pasó con las que salieron.

| Bloqueado | Pregunta que lo desbloquea | Quién puede responderla |
|---|---|---|
| **Toda priorización por volumen** | ¿Cuál es el trabajo de mayor volumen diario? **Dos pases reales dieron el tamaño de un expediente —decenas de páginas— y no la frecuencia**, que es lo que ordena una hoja de ruta | Solo ella. Hasta entonces **ningún gate de creación de skill se cumple** |
| **El Knowledge Pack** | ¿Unidad artículo o unidad ley? ¿Qué área primero? ¿Qué devuelve cuando **no hay entrada** para la pregunta? | El dueño. Sin la tercera, el pack tiene el defecto que el corpus critica: **el silencio se leerá como ausencia de regla** |
| **La razón de la protección de escritura** | Si en su inspección hay un expediente digital oficial, la frase *«es lo único que no se puede reconstruir»* —que **siete `SKILL.md`** usan para justificar la protección más fuerte del producto— **es falsa ahí**. La protección seguiría siendo la correcta; su razón declarada no | Solo ella, y es la pregunta de negocio 7. **Ninguna frase del producto se toca hasta que conteste** |
| **Quién pone la marca ` - REVISADO`** | El mecanismo presupone que la puso ella. **Nada distingue hoy que la haya puesto un dependiente**, y la pregunta 5 —quién más mete mano en un expediente— nunca se hizo | Solo ella. Es la misma conversación que la anterior |
| **La mitad jurídica del benchmark adversarial** | ¿Quién evalúa, cuánto tiempo tiene, con qué frecuencia? Siete de quince casos exigen **verificar fuentes oficiales en la fecha de ejecución, cada vez** | El dueño. Nadie ha estimado ese coste |
| **La decisión de confidencialidad sobre los servidores** | No es técnica. **Lo que cambió es que ya no se le oculta**: la guía lo dice. Lo que no cambió es que nadie ha decidido qué material abre ella aquí | Solo los dueños |
| **El coste de una pasada** | Exige una **corrida instrumentada con transcript**. Las once pasadas de septiembre son de escritorio y **no tienen una sola cifra de gasto**, y eso va escrito en su propia ficha de medición | Mío, el día que haya una corrida instrumentada |

### Las cinco que salieron, y qué las cerró

| Estaba bloqueado por | Qué pasó |
|---|---|
| **El Core entero** · *«¿puede una cuenta Pro forzar sesión local en Cowork?»* | **Dejó de bloquear el producto.** ADR-018 estableció que el plugin ejecuta código, y hoy ejecuta diez programas. La pregunta sigue viva **para el Core**, que no se está construyendo |
| **El sucesor de ADR-012** | Triado en `BACKLOG` §7 con los otros diecisiete |
| **La hoja de hechos revisada** · *«¿va ella a abrir un `.md` y escribir SÍ?»* | **La mitad técnica está cerrada y probada.** La mitad de ella sigue abierta, y subió a §5.2 como entrada 2 |
| **Tres dossiers de «contexto B»** · *«¿ejerce ella alguna función de autoridad?»* | **Contestada, y en campo: es autoridad.** El encabezado versionado del `PASE-REAL` lo dice. No eran lastre: eran la mitad del producto que faltaba, y SPEC-03 la construyó |
| **La fecha de corte de la Ley 2452** | Sin cerrar **y sin consecuencia hoy**: el producto no cita normas, así que esa fecha no puede aparecer en ninguna salida |

---

## §7 — Preguntas para el dueño

Las que solo él puede responder, y que ningún lector puede resolver leyendo más archivos.

> **Cuatro de las diez se contestaron solas, trabajando.** Se dejan escritas con su respuesta al lado, en vez de borrarlas: **una pregunta que se contestó sin que nadie la contestara es un dato sobre cómo se decide aquí**, y borrarla lo perdería.
>
> | # | Qué preguntaba | Cómo quedó |
> |---|---|---|
> | **1** | ¿El corpus se reescribe contra el producto, o se mantiene como cantera? | **Se mantiene, y ahora la regla está escrita:** se corrige solo lo que afirma un hecho sobre el presente; el registro histórico no se toca, y se dice por qué |
> | **3** | ¿«Parcialmente respaldado» es un estado? | **No, y está cerrado con argumento en el método:** *«no es un estado y no se escribe nunca»* — se estrecha el enunciado hasta lo que la prueba cubre, y el resto sale como ficha aparte |
> | **4** | ¿Los fixtures se corren antes o después de aplicar los hallazgos? | **Se corrieron después, y la decisión ya no se puede tomar:** *«la primera no se puede hacer dos veces»*, y así fue. Lo que hay es línea base de las correcciones, no del método solo |
> | **5** | ¿Cuál es el séptimo comando? | **Se construyeron cinco, y entre ellos el candidato que este documento llamaba «el único hueco del oleoducto»**: `revision-de-rigor`. **«Qué hay que pedir» sigue sin construirse**, y ahora se sabe que no era el más urgente |
>
> **Las seis que siguen abiertas son las 2, 6, 7, 8, 9 y 10**, y a ellas se añaden las tres conversaciones de §5.2. La 10 sigue siendo la única cuya respuesta no cambia una línea de código y cambia todo lo demás.

1. **¿El corpus se reescribe *contra* el producto, o se mantiene como cantera independiente?** Hoy es lo segundo de hecho, y por eso afirma que solo existe una skill. Las dos opciones son defendibles; lo que no lo es es **no elegir**, porque produce documentos que se leen como especificación y describen un producto que no existe. Y si se elige la primera, hay que escribir la regla que falta: qué se hace cuando el producto adelanta a la investigación.

2. **¿ADR-012 se enmienda o se le escribe un sucesor?** Mi lectura es que el sucesor es más honesto: su título, su contexto y su Decisión 3 dejaron de describir el sistema, y las Decisiones 1, 2, 4, 5, 6, 7 y 8 se trasladan intactas. Pero es decisión suya. La disciplina de `AMENDMENT-CANDIDATES.md` —"por precedencia manda el ADR Accepted; nada se cambió en silencio"— hay que repetirla con esto, **que es más grande que las cuatro enmiendas juntas**.

3. **¿"Parcialmente respaldado" es un estado, sí o no?** El formato lo prohíbe con argumento, el fixture lo exige en su encargo, el Technical Design lo usa con otro referente y ADR-003 tiene enum cerrado. **Mientras no se decida, el único fixture ejecutable del repositorio no puede puntuar al producto: mide otra cosa.**

4. **¿Los fixtures se corren antes o después de aplicar los hallazgos?** Correrlos antes da línea base de cuánto sostiene el método solo; correrlos después mide las correcciones. Las dos cosas valen, pero **la primera no se puede hacer dos veces**.

5. **¿Cuál es el séptimo comando?** Hay cuatro candidatos y los seis lectores no coinciden: **qué hay que pedir** (el más barato, taxonomía ya escrita), **cotejar documentos** (el mayor de los tres huecos, método ya escrito de punta a punta y sin una línea de derecho), **revisión de rigor sobre el escrito propio** (el único hueco del oleoducto: nada revisa el borrador antes de que salga con su firma) y **comparar dos piezas**. Es la única capacidad que argumenta *contra* ella, que es justo lo que una independiente sin socio que le lea los borradores no tiene. **La decide ella, no el corpus.** Y necesita un nombre que ella entienda y que no sugiera que el modelo juzga: ¿cómo llama ella a ese trabajo — buscarle el hueco, ponerse en la del otro, revisar antes de firmar?

6. **¿Se consolidan los duplicados o se declara redundancia deliberada?** Son siete: los dos ledgers (con dos espacios de identificadores que ya colisionan), los dos `00-*`, los dos `03-*`, el dossier de práctica huérfano, los tres solapamientos de workflow, "rigor judicial" escrito en tres sitios con dos contratos incompatibles, y el benchmark de `fact-builder` escrito dos veces. **Si se consolida, en todos los casos el archivo más desarrollado es el de número más alto.**

7. **¿El corpus baja a las skills, o alimenta el Knowledge Pack?** De eso depende una tarea concreta: si el destino es la skill, hay que **traducir cinco familias de etiquetas en mayúsculas** antes, porque llegan a la pantalla de ella y violan la regla de cero jerga. Si el destino es el Knowledge Pack, está bien como está.

8. **¿Para qué área se construye el primer Knowledge Pack, y con qué unidad?** Laboral es la candidata natural —única con transición registrada y fixture A/B ejecutable— pero también la de mayor mantenimiento, con **una bomba fechada dentro**: el 100% de dominical y festivo desde 2027-07-01 volverá falso el archivo sin que nadie lo toque. Derecho de petición sería más barato y envejecería menos. **El corpus no propone ninguna prioridad, y debería.**

9. **¿Cuándo se corre el baseline con ella, y quién lo hace?** Es el gate 2 de la hoja de ruta vigente —"la profesional confirma demanda, frecuencia aproximada o coste de trabajo"— y **no lo cumple ninguna candidata, ni la mía**. Mientras no exista, el orden del §5 es un argumento de diseño bien fundado y nada más.

10. **La decisión de confidencialidad.** ¿Se le dice a ella lo que el hecho (a) significa, y se le deja decidir qué material abre aquí? Es la única pregunta de este documento cuya respuesta no cambia una línea de código y cambia todo lo demás.

---

*Escrito el 2026-08-26 por síntesis de seis lecturas independientes más un pase de contradicciones. **Actualizado el 2026-09-21** tras sesenta y un commits: §0, §0.bis, §5, §6 y la cabecera de §7 son de esa fecha; §1 a §4 se conservan como registro de agosto, con su marca de qué quedó superado.*

> **Y la línea que este documento aprendió a no escribir.** La versión anterior decía *«caduca con el próximo commit»*, y caducó — pero nadie lo notó durante **veintiséis días**, porque caducar en silencio es lo que hace un documento que afirma cosas sobre el presente sin nada que las comprobe. **Los diez titulares de §0 llevan ahora el comando que los verifica**, y esa es la diferencia entre una fecha de caducidad y una guarda.
