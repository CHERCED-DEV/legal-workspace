# Crítica de producto del arnés Despacho

**Fecha:** 2026-08-25. **Alcance:** los seis skills del plugin, sus archivos de apoyo, las dos guías y los dos manifiestos.
**Método:** un revisor independiente que no participó en la escritura, con encargo de buscar derecho sustantivo colado, sitios donde el modelo puede inventar sin que se note, jerga, incoherencias, solapamientos y huecos.

**Estado: SIN APLICAR.** Diecisiete hallazgos numerados H-01 a H-17 más menores. Ninguna corrección se ha aplicado todavía.

---

No escribí ningún archivo. Leí los seis skills, los dos archivos de apoyo de `fact-builder`, el README, la guía y los dos manifiestos.

# Veredicto en cuatro líneas

El trabajo de contención del derecho es real y está bien hecho: no hay una sola norma, artículo ni plazo legal afirmado en ningún skill. Lo que hay son **dos fugas de derecho por la puerta de atrás** (una estructura de escrito recordada de memoria y una aritmética de fechas), **una cadena de tres comandos sin juntas** (nada persiste los hechos ni devuelve las decisiones de ella), y **una promesa de seguridad hecha a la abogada que solo cumple uno de los seis comandos**. Tres comandos de seis funcionan hoy y le ahorran tiempo real; los otros tres se apoyan en un artefacto que nadie produce. No son seis documentos bien escritos —son mejor que eso—, pero todavía no son una oficina.

---

## H-01 · Derecho colado: el esqueleto del escrito sale de la memoria del modelo

**Archivo:** `C:/Users/HITMA/Desktop/legal-workspace/plugins/despacho/skills/redactar-escrito/SKILL.md`, Fase 3 (§4).

**Qué está mal.** §3.2 dice, con razón y con todas las letras: *"la forma de un escrito también es derecho. Qué apartados lleva, en qué orden y con qué nombre son exigencias jurídicas... la estructura no se produce de memoria"*. Diecisiete líneas después, la plantilla de la Fase 3 imprime la estructura completa de un escrito de demanda: `«el apartado de hechos»`, `«el apartado de derecho»`, `«el apartado de lo que se pide»`, `«el apartado de anexos»`. Solo los dos primeros renglones usan « » de relleno; los cuatro siguientes están escritos en duro.

**Por qué importa.** Es la violación más grave del conjunto y además se autodesmiente: el skill le prohíbe al modelo recordar la estructura y acto seguido se la recuerda. Un modelo que ve esa plantilla la rellena, y la abogada recibe un esqueleto que parece dictado por ella y no lo fue. Si en su jurisdicción o para ese escrito el orden o los nombres son otros, el error viaja en el andamio, donde nadie lo mira.

**Corrección.** Que los seis renglones sean genéricos y vacíos: `«apartado 1, con el nombre que ella le dio» ... lo escribo con lo que usted dictó`, repetido n veces, más una única línea fija: `«cualquier apartado de derecho, calificación o petición que ella nombre» ... [[LE TOCA A USTED]]`. Ningún nombre de apartado en duro. Y añadir a la autoevaluación: *"¿algún título de mi esqueleto no lo dijo ella ni está en el modelo?"* (hoy la pregunta 6 pregunta por la estructura pero no por título suelto).

---

## H-02 · Derecho colado: la cronología calcula días entre fechas

**Archivo:** `.../skills/cronologia/SKILL.md`, Fase 5 (línea 143), tabla de la línea 147 y plantilla §6 (línea 223).

**Qué está mal.** El skill manda declarar cada vacío temporal *"con sus dos extremos y **su duración en días**"*, lo pone como columna **Bien** de una tabla (*"Entre el 10 de abril y el 3 de julio (84 días)"*) y lo fija en la plantilla (`«N» días`). Eso es aritmética sobre fechas, hecha por el modelo, en el único producto que jura en cuatro archivos distintos que jamás calcula nada con fechas.

**Por qué importa.** Es exactamente el error que la guía define como catastrófico: *"una fecha mal calculada se lee exactamente igual de bien que una correcta"*. Un conteo de días mal hecho no despierta ninguna sospecha. Peor: junto a una fila que transcribe *"dentro de los diez (10) días siguientes"*, un `(84 días)` en la misma salida invita a leerse como cómputo. Y la autoevaluación 17 pregunta *"¿Hay en mi salida alguna norma, plazo, **cómputo**...? No debe haber ninguna"* — se está entrenando al modelo a contestar que no a una pregunta cuya respuesta la propia plantilla obligó a que fuera sí.

**Corrección.** Quitar la duración. `"Entre el 10 de abril y el 3 de julio el material revisado no registra ningún evento"` dice lo mismo y no calcula. Si el tamaño del hueco importa, se expresa sin aritmética: *"entre esas dos fechas"*. Y en la tabla de la línea 147, la columna Bien queda sin el paréntesis.

---

## H-03 · La frontera del cálculo está trazada por tema, no por operación

**Archivo:** `.../skills/cronologia/SKILL.md` §3.4 (fecha deducida); en tensión con `.../skills/revisar-documento/SKILL.md` §4.

**Qué está mal.** El ejemplo canónico de "deducida" es: el correo del 12 dice *«la carta que nos llegó ayer»* → `11 de marzo`. Eso es (a) restar un día y (b) resolver una ambigüedad eligiendo la lectura probable ("ayer = día calendario anterior"), las dos cosas que el conjunto prohíbe en otros sitios. La mitigación —marcar el grado y escribir el supuesto— es buena, pero la **regla que separa esta deducción legítima del cálculo de un término no está escrita en ninguna parte**. El producto la traza por asunto ("plazos, no"), no por operación ("aritmética con fechas, no").

**Por qué importa.** Un modelo no encuentra esa frontera solo. Con el permiso explícito de deducir fechas cruzando piezas y declarando supuestos, deducirá `"la comunicación se recibió el 16 de mayo"` a partir de un sello, y de ahí a situar el arranque de un término hay un paso que nadie le prohibió dar, porque nunca lo llamó plazo.

**Corrección.** Escribir la regla de operación en los tres skills que tocan fechas: *"nunca sumas ni restas días sobre una fecha para producir otra, aunque el resultado no sea un plazo. Lo único que se deduce es lo que una fuente enuncia como relativo ('ayer', 'el día anterior') y ahí solo se traduce la palabra de la fuente; no se opera con números."* Y añadir la contrapregunta a la autoevaluación: *"¿alguna fecha de mi salida es el resultado de una suma o una resta que hice yo?"*

---

## H-04 · La defensa contra texto dirigido al programa vive en un solo comando de seis, y a ella se le promete como propiedad general

**Archivos:** solo `.../skills/revisar-documento/SKILL.md` §7 la tiene. No aparece en `fact-builder`, `cronologia`, `inventario-de-anexos`, `estado-del-caso` ni `redactar-escrito`. La guía (`GUIA-PARA-LA-ABOGADA.md` §5, último bloque) se la promete a ella sin acotar comando: *"Él no las obedece, no deja que alteren nada del resumen, y se lo transcribe a usted en un bloque titulado AVISO"*.

**Por qué importa.** Los cinco comandos sin la regla son precisamente los que **más** material externo leen: `fact-builder` y `cronologia` recorren el expediente entero, `estado-del-caso` recorre la carpeta completa, `inventario-de-anexos` abre todos los anexos. Un requerimiento de contraparte con una instrucción escondida se cuela por cualquiera de esos cinco sin que nada la detenga ni la reporte. Y ella, que leyó la guía, creerá que si no ve el bloque `AVISO` es que no había nada. Es la única promesa del producto que puede fallar en silencio y con un tercero interesado del otro lado.

**Corrección.** Sacar §7 de `revisar-documento` a un bloque idéntico en los seis SKILL.md (son doce líneas), y añadir la pregunta a las seis autoevaluaciones. Mientras no esté en los seis, corregir la guía para que diga en qué comandos vale.

---

## H-05 · La cadena está rota: nadie produce la hoja de hechos y nadie recibe las decisiones de ella

**Archivos:** `.../skills/fact-builder/SKILL.md` (cero menciones de carpetas o archivos, lo comprobé: es el único de los seis sin una sola referencia a `1-Documentos recibidos/`, `2-Borradores/` ni a un nombre de archivo de salida), contra `.../skills/inventario-de-anexos/SKILL.md` Fase 3 (*"de la **hoja de hechos** del caso, si existe —con sus mismas etiquetas"*) y `.../skills/redactar-escrito/SKILL.md` §2.1 (*"Un hecho que ella ya revisó... La etiqueta del hecho (`H-04`) y la fecha de esa pasada"*).

**Qué está mal.** Dos comandos consumen un artefacto que el tercero no escribe. `fact-builder` entrega texto en pantalla con casillas `[ ] sí [ ] no [ ] a medias` — y **no existe ninguna vía por la que esas casillas vuelvan**. La guía se lo enseña a ella (Ejemplo 2) sin decirle nunca qué hace con la hoja: ¿la imprime?, ¿le contesta "apruebo H-01, H-02 y H-04"?, ¿en la misma conversación?, ¿y la semana que viene, cuando la conversación ya no existe?

**Por qué importa.** Es el hallazgo de mayor consecuencia del conjunto, aunque no sea el más grave en la escala de "derecho colado". Toda la promesa del producto —*"hecho, prueba; hecho, prueba"* y después un borrador construido solo sobre lo aprobado— se sostiene en un eslabón que no existe. Hoy `/redactar-escrito` en la práctica solo puede caer en su propia rama de escape (*"si solo hay material en bruto, dilo y detente"*) o creerle a la conversación. Y `fact-builder`, al no tener regla de carpeta, es además el único comando que **nada le impide escribir dentro de `1-Documentos recibidos/`**.

**Corrección, concreta y barata:**
1. Añadir a `fact-builder` la sección "Dónde se escribe" que tienen los otros cinco: salida a `2-Borradores/Hechos - <caso> - <AAAA-MM-DD>.md`, prohibición explícita de tocar `1-Documentos recibidos/` y `0-Estado del caso`, y regla de no sobrescribir.
2. Definir el mecanismo de devolución en un solo sitio y repetirlo en la guía: ella abre el archivo, escribe `SÍ`/`NO`/`A MEDIAS: <corrección>` al lado de cada ficha, y lo guarda como `Hechos - <caso> - <fecha> - REVISADO.md`. Ese archivo, y solo ese, es lo que `inventario-de-anexos` y `redactar-escrito` leen.
3. Añadir a `redactar-escrito` Fase 1 la comprobación dura: *"si no encuentras un archivo de hechos con marca de revisión de ella, no hay hechos aprobados; dilo y pregunta"*.

---

## H-06 · `revisar-documento` afirma sobre la carpeta sin que ninguna fase le mande mirarla

**Archivo:** `.../skills/revisar-documento/SKILL.md`, Fase 1 (*"qué anexos anuncia y **si están entre lo recibido**"*), Fase 6 y el ejemplo del §8 (*"Anuncia «Anexo A»; **no aparece entre lo recibido**"*), contra §1 (*"No lo uses para... comparar el documento con el resto del expediente"*).

**Qué está mal.** El formato obliga a una afirmación sobre el contenido de `1-Documentos recibidos/`, el propósito prohíbe salir del documento, y **ninguna fase le dice al modelo que liste la carpeta**. El resultado previsible es una afirmación de ausencia producida sin comprobación, con la forma exacta de un dato comprobado.

**Por qué importa.** Es el sitio del producto donde inventar sale más barato y se nota menos: `"no aparece entre lo recibido"` es la línea que ella usará para decidir a quién le pide qué. Y está en el ejemplo que la guía le enseña como patrón.

**Corrección.** En Fase 1: *"antes de escribir si un anexo anunciado está o no, lista `1-Documentos recibidos/`. Si no pudiste listarla, escribe: «el documento anuncia el Anexo A; no se comprobó contra la carpeta»"*. Y quitar de §1 la prohibición de comparar con el expediente, o acotarla a "el contenido; el listado de la carpeta sí se mira".

---

## H-07 · Tres vocabularios para la distinción central del producto

**Archivos:** `.../skills/fact-builder/SKILL.md` §2.3 y Fase 4 (**apoya / contradice / sitúa**); `.../skills/fact-builder/FORMATO-DE-SALIDA.md` §1.3 y todo el ejemplo relleno (**RESPALDA / CONTRADICE / DA CONTEXTO**, y estados **Respaldado / Sin respaldo**); `GUIA-PARA-LA-ABOGADA.md` §5, que le enseña a ella *"una prueba **apoya**, **contradice** o **sitúa** — y 'sitúa' significa que no apoya"*.

**Qué está mal.** El SKILL fija un vocabulario "para lo que lee la profesional" y el archivo de formato —que es el que contiene la plantilla que el modelo va a copiar— usa otro distinto. La salida real que ella recibirá dirá `DA CONTEXTO`, palabra que la guía nunca le enseñó, y no dirá `sitúa`, que es la única que sí le enseñó y sobre la que le explicaron la trampa.

**Peor, dentro del mismo skill hay dos tablas de estados incompatibles:** `SKILL.md` Fase 5 lista *Sin respaldo / Contradicho / **No verificable con este material***; `FORMATO-DE-SALIDA.md` §1.4 lista *Respaldado / Contradicho / **Respaldado y contradicho** / Sin respaldo*. Cada tabla tiene un estado que la otra no contempla.

**Corrección.** Elegir un triple —**apoya / contradice / sitúa**, que es el que aprendió ella— y hacer un reemplazo mecánico en `FORMATO-DE-SALIDA.md`, incluido el ejemplo relleno. Unificar los estados en una sola lista de cuatro y borrar la otra. Es media hora de trabajo y es la distinción de la que depende todo el producto.

---

## H-08 · El plugin envía documentación interna del proyecto dentro del producto

**Archivos:** `.../skills/fact-builder/COMO-USARLO-EN-EL-BASELINE.md` (32 KB, entero) y `.../skills/fact-builder/FORMATO-DE-SALIDA.md` §3 y §4 (unos 12 KB).

**Qué está mal.** El README §7 dice: *"los archivos extra junto a un SKILL.md son parte del método y viajan con él"*. Es decir, se instalan en la máquina de ella y quedan disponibles como contexto del skill. Lo que viaja ahí dentro es: `propose_facts`, `ProposalItem`, `proposal_item_id`, `item_content_hash`, `evidence_basis[]`, `SUPPORTS|CONTRADICTS|CONTEXTUALIZES`, `PROVENANCE_REQUIRED`, referencias a ADR-003/005/006/008, rutas a `docs/technical-design/`, y un protocolo de investigación completo con brazos B1/B2/B3, hoja de registro, rúbrica y advertencias sobre cómo no sesgar la medición **con ella como sujeto**.

**Por qué importa.** Tres razones, en orden. (1) El propio `FORMATO-DE-SALIDA.md` sentencia: *"Un documento del modo 1 que contenga un nombre de campo, un identificador opaco o la palabra 'hash' es un documento mal producido"* — y el archivo que lo dice contiene las tres cosas, a tres pantallas de distancia de la plantilla que el modelo va a copiar. Nada impide que "modo B", "el Core" o "Proposal" aparezcan en lo que ella lee. (2) El §2.3 del `SKILL.md` describe el modo B con sus garantías (*"un hecho sin base ni marca explícita se rechaza"*) en presente; hoy no existe Core, así que esa columna solo puede desinformar. (3) `COMO-USARLO-EN-EL-BASELINE.md` es un documento sobre cómo medirla a ella sin que lo note (§3.2: *"la petición 10 es una trampa de un solo uso"*). Está instalado en su computador. Eso no es un problema de jerga: es un problema de a quién se le entrega qué.

**Corrección.** Mover los dos archivos a `docs/`. Dejar junto al SKILL, si acaso, un `FORMATO-DE-SALIDA.md` recortado a §1 y §2 (plantilla y ejemplo), sin una palabra de §3 ni §4. Y borrar del `SKILL.md` la tabla de modos de §2.3, sustituyéndola por la única frase que ella necesita: *"nada de lo que produces está verificado por ningún sistema; la única comprobación es la lectura de la profesional"*.

---

## H-09 · `/fact-builder` está en inglés

**Archivos:** `.../skills/fact-builder/SKILL.md` (campo `name`), `GUIA-PARA-LA-ABOGADA.md` §1.

**Qué está mal.** Cinco comandos en español —`revisar-documento`, `estado-del-caso`, `cronologia`, `inventario-de-anexos`, `redactar-escrito`— y el sexto, el más importante, en inglés. La guía tiene que glosarlo: *"`/fact-builder` (los hechos con su prueba)"*. Es la única línea de la guía donde el producto le pide a ella que aprenda una palabra de otro idioma para nombrar lo que hace.

**Por qué importa.** Es jerga técnica en lo que llega a ella, en el sitio de máxima visibilidad, y se arrastra por cinco archivos (`inventario` y `redactar` remiten a él por nombre). La guía además le dice que puede pedirlo en español —bien— pero le imprime el nombre corto en inglés como salida de emergencia, que es cuando más la va a necesitar.

**Corrección.** Renombrar carpeta y campo `name` a `hechos-con-prueba` (o `hechos-y-prueba`), actualizar las cuatro referencias cruzadas y la guía, y subir `version` en `plugin.json`. Hacerlo **ahora**, antes de la primera instalación: después, renombrar un comando que ella ya aprendió cuesta más que la mejora.

---

## H-10 · La guía imprime los comandos con una forma que el propio README marca como no verificada

**Archivos:** `GUIA-PARA-LA-ABOGADA.md` §1 (*"`/revisar-documento`, `/estado-del-caso`, `/fact-builder`..."*) contra `README.md` §1 (*"**POR COMPROBAR (primera instalación):** que los comandos aparezcan escritos exactamente así en la caja de mensaje y **no con algún prefijo del plugin**"*).

**Qué está mal.** El dueño sabe que puede que sean `/despacho:revisar-documento`. La abogada no. La guía se lo da como dato, sin matiz, y encima como la vía fiable: *"use el nombre corto: es la forma más directa de pedirlo"*.

**Por qué importa.** Es el único paso mecánico que la guía le pide ejecutar. Si falla, falla la primera vez que algo no arranca, que es justo el momento en que la guía la manda al nombre corto. Y la guía cierra diciendo *"si lo que ve en la pantalla no se parece a lo que aquí se dice... esta guía es la que está desactualizada"* — cierto, pero eso no se puede usar para publicar un dato que ya se sabe dudoso.

**Corrección.** Una línea en §1: *"puede que aparezcan con `despacho:` delante —`/despacho:cronologia`—; en la caja de mensaje se ve la lista completa al escribir la barra"*. O, mejor, comprobarlo antes de imprimir la guía y escribir la forma real.

**Nota sobre el resto de pasos de interfaz.** `README.md` §4 (*Customize → Plugins → Add marketplace*, botón *Install*) y §5 (botón *Update*) están escritos como hechos, sin etiqueta, en un documento que etiqueta escrupulosamente todo lo demás —incluido el comportamiento del botón Update, marcado POR COMPROBAR, mientras su existencia se da por sentada. La ausencia de etiqueta ahí es la anomalía del documento. O se marcan **POR COMPROBAR**, o se verifican en pantalla antes del primer intento.

---

## H-11 · La guía le promete que nunca se sobrescribe nada, y un comando sí lo hace

**Archivos:** `GUIA-PARA-LA-ABOGADA.md` §6 (*"**nunca sobrescribe un archivo que ya está en `2-Borradores`**"*), contra `.../skills/inventario-de-anexos/SKILL.md` §1 (*"nombre `Inventario de anexos — <fecha>.txt`"*, sin regla de no sobrescritura en todo el archivo) y contra `.../skills/estado-del-caso/SKILL.md` §4 (*"Se reescribe entero en cada pasada"*).

**Qué está mal.** `cronologia` y `redactar-escrito` sí tienen la regla escrita. `inventario-de-anexos` no la tiene, y su nombre de archivo solo lleva la fecha: dos pasadas el mismo día colisionan, y si ella anotó a mano en la primera, se pierde. `estado-del-caso` reescribe `0-Estado del caso` por diseño, y la supervivencia de las notas de ella depende de que el modelo las vuelva a teclear correctamente —que es exactamente donde ocurren las alteraciones silenciosas. Es la única escritura destructiva del producto y no tiene copia previa.

**Corrección.** (a) Añadir a `inventario-de-anexos` la misma regla de los otros dos y un sufijo de pasada en el nombre. (b) En `estado-del-caso` Fase 6, antes de reescribir: guardar el contenido anterior íntegro en `2-Borradores/0-Estado del caso — anterior (AAAA-MM-DD).txt`. Cuesta una línea y convierte una pérdida irreversible en una recuperable.

---

## H-12 · La verificación que sostiene todo el producto es un autoinforme no comprobable

**Archivos:** los seis SKILL.md, fase final (*"vuelve al material y abre cada anclaje que citaste, uno por uno"*) y las seis autoevaluaciones.

**Qué está mal.** La única línea de defensa contra la cita fantasma —diagnosticada correctamente como el error más peligroso, en los seis archivos— es que el modelo diga que abrió cada cita. No hay artefacto: la abogada no puede distinguir una salida donde se hizo de una donde no, y ninguna de las dos se ve distinta.

**Por qué importa.** El producto se vende como *"hace barato encontrar el error"*, pero no baja el coste de encontrarlo: solo le da la coordenada. Una pasada de hechos sobre seis documentos produce del orden de 30 a 60 comprobaciones, y **ninguna salida le dice cuáles hacer primero**. La única que se acerca es el bloque de cierre de `redactar-escrito` ("frases que se apoyan solo en lo que usted dijo"), y es el mejor invento del conjunto.

**Corrección, y es la mejora de mayor rendimiento por línea escrita:**
1. Generalizar ese bloque: que **las seis** salidas cierren con *"QUÉ COMPROBAR PRIMERO"* — tres a cinco anclajes elegidos por criterio explícito (los que sostienen solos un hecho, los que vienen de material producido por la propia interesada, los que van a entrar en un escrito).
2. Convertir la autoevaluación en artefacto: obligar a que, para tres anclajes elegidos al azar, la salida transcriba además **la línea completa que rodea a la cita**. Si el modelo no la tiene, no puede inventarla dos veces igual, y ella compara en cinco segundos sin abrir nada.

---

## H-13 · Formatos de salida que no encajan con la promesa

**Archivos:** `.../skills/cronologia/SKILL.md` §6 (`Cronologia - <caso corto> - <AAAA-MM-DD>.md`, *"un archivo de texto... cuya tabla se copia y se pega en un escrito"*) y `.../skills/inventario-de-anexos/SKILL.md` §1 (`Inventario de anexos — <fecha>.txt`, con tablas de tuberías en §6).

**Qué está mal.** Las dos entregas más "pegables" del producto —la tabla de anexos *"lista para pegar en un escrito"* y la cronología— salen como tablas de Markdown dentro de un `.md` y de un `.txt`. Pegadas en Word son una hilera de `|` y guiones. Y un `.md` en Windows puede no abrir en nada útil.

**Por qué importa.** "Lista para pegar" es la promesa más concreta y verificable de todo el README, y es la que falla al primer intento. Además, `redactar-escrito` sí produce `.docx`: la capacidad existe en el mismo plugin.

**Corrección.** Que ambos entreguen `.docx` con tabla real, con la rama de escape que ya tiene `redactar-escrito` (*"si no puedes producir Word, escribes texto y lo dices"*). Y unificar la convención de nombres, que hoy son tres distintas (guion vs raya, con y sin nombre de caso, `.md` / `.txt` / `.docx`). De paso: `redactar-escrito` §7 nombra los archivos `2026-014 — Borrador — ...`, con un número de radicación interno que no está definido en ningún otro archivo del producto ni en la estructura de carpetas de la guía. El modelo lo inventará.

---

## H-14 · Descripciones que colisionan al disparar

**Archivos:** los campos `description` de los seis SKILL.md.

**Qué está mal.** `fact-builder`: *"cuando pidan construir, extraer u **ordenar los hechos**"*. `cronologia`: *"cuando pidan una cronología, **ordenar los hechos** en el tiempo"*. `estado-del-caso`: *"**inventariar la carpeta**"*. `inventario-de-anexos`: *"armar la **lista de anexos**"*. Dos pares que se pisan con las mismas palabras.

**Por qué importa.** La guía le vende a ella que puede escribir en español y funciona (*"no hay botones que aprender"*). Toda esa promesa descansa en que las descripciones desambigüen. *"Hazme el inventario del caso López"* hoy puede arrancar cualquiera de dos comandos, y ella no tendrá forma de saber cuál corrió ni por qué recibió otra cosa.

**Corrección.** Quitar *"ordenar los hechos"* de `fact-builder` (deja *"construir o extraer"*) y quitar *"inventariar la carpeta"* de `estado-del-caso` (deja *"saber qué documentos hay"*). Y añadir a las cuatro descripciones la exclusión cruzada explícita, que es lo que el README §7 ya recomienda hacer y aquí no se hizo: `estado-del-caso` debe decir *"no lo uses para armar la lista de anexos de un escrito (eso es inventario-de-anexos)"`, y recíprocamente.

---

## H-15 · Huecos: tres trabajos diarios y sin derecho que ningún comando cubre

Ninguno de los tres exige una norma, un plazo ni una calificación, así que caben enteros dentro de la regla del producto.

1. **Comparar dos documentos.** *"¿La contestación responde a cada hecho de mi demanda?"*, *"¿qué cambió entre el contrato que mandaron y el que firmamos?"*. Es puro cotejo de texto, es de las tareas más tediosas del oficio, y `revisar-documento` la prohíbe explícitamente (*"no lo uses para comparar el documento con el resto del expediente"*). Es el hueco más grande.
2. **Buscar dentro del material.** *"¿Dónde dice algo sobre la instalación?"* con la cita y la página. Hoy la única forma de conseguirlo es una pasada completa de `fact-builder`, que es carísima para una pregunta de treinta segundos.
3. **La lista de lo que hay que pedir.** Los cinco comandos producen vacíos, mencionados-y-ausentes y *"qué haría falta para respaldarlo"*, repartidos en cinco salidas distintas. Nadie los junta en la única cosa que ella hará después: la lista de qué pedirle a la clienta y qué pedirle a la contraparte. Es un comando de veinte líneas que consolida lo que los otros ya produjeron, y probablemente el de mejor relación valor/coste que falta.

---

## H-16 · Supuestos de capacidad que el producto no ha comprobado

**Archivos:** `.../skills/fact-builder/FORMATO-DE-SALIDA.md` §2 y `GUIA-PARA-LA-ABOGADA.md` Ejemplo 2, que citan *"entrevista, 00:08:12"*, *"00:31:04"*; `README.md` §9 (tabla de lo que falta comprobar).

**Qué está mal.** El ejemplo insignia del producto —el que la guía le enseña a ella— depende de que el sistema pueda oír una grabación de 47 minutos y citar el minuto exacto. **Eso no aparece en la tabla de comprobaciones pendientes del README**, que sí lista el `.docx`, el plan, el repositorio y el prefijo de los comandos. Tampoco hay una sola línea en la guía sobre qué hace ella con el audio de una entrevista, ni sobre qué pasa si lo que hay es un PDF escaneado sin texto.

**Por qué importa.** Si no puede oír audio, el ejemplo 2 de la guía es una promesa que no se cumple, y `fact-builder` queda reducido a documentos —la mitad de su propósito, porque la entrevista *"es de donde sale casi todo"*, según el propio archivo. Y el modo de fallo del PDF escaneado es el peor de todos: un OCR parcial produce un resumen verosímil de un documento que no se leyó, y la regla *"declara lo que no pudiste leer"* solo funciona si el modelo sabe que no lo leyó.

**Corrección.** Añadir dos filas a la tabla del README §9: *"que pueda transcribir o citar minutos de una grabación"* (bloquea el ejemplo 2 y media promesa de `fact-builder`) y *"qué hace con un PDF escaneado sin capa de texto"* (bloquea todo). Comprobar las dos antes de sentarse con ella, con un archivo suyo real.

---

## H-17 · Nada mejora con el uso

**Archivo:** `.../skills/redactar-escrito/SKILL.md` Fase 2.

Las cuatro preguntas (*qué escrito, a quién, qué apartados, qué hechos*) se hacen **cada vez**, para siempre. Al quinto escrito del mismo tipo, dictar otra vez la estructura completa deja de ser prudencia y pasa a ser fricción, y la fricción es lo que hace que la gente abandone una herramienta buena. La corrección respeta la regla del producto porque la fuente sigue siendo ella: permitir un `Preferencias del despacho.txt` en la carpeta del caso —escrito por ella, nunca por el modelo— con su estructura habitual y su destinatario, que la Fase 2 lee y **confirma en una línea** en vez de preguntar cuatro. Si el archivo no está, se pregunta como hoy.

---

## Menores, en una línea cada uno

- **`plugin.json` / frontmatter:** el campo `version:` dentro de cada `SKILL.md` no forma parte del esquema estándar de un skill, y el `README.md` §7 lo enseña como obligatorio para añadir comandos nuevos. Comprobar que no genere un aviso de validación antes de escribirlo en la guía del dueño.
- **`README.md` §4** describe la estructura de carpetas como `1-`, `2-`, `3-` y omite `0-Estado del caso (no editar).txt`, que la guía sí incluye y que `estado-del-caso` necesita. Añadirlo.
- **Jurisdicción implícita:** *radicado* (`estado-del-caso` Fase 4, `redactar-escrito` §3.2), *tutela* (`redactar-escrito` Fase 2), *S.A.S.* y montos en pesos en todos los ejemplos. Ninguno afirma derecho —los dos primeros están dentro de prohibiciones— pero fijan país. Si es deliberado, decirlo en el README; si no, neutralizar los ejemplos.
- **Fatiga de advertencia:** cada salida abre con un recuadro de tres líneas y cierra con conteo más caveat, seis comandos, todas las veces. La abogada dejará de leerlos, y es donde vive lo peligroso. Permitir que el recuadro se reduzca a una línea a partir de la segunda entrega de la misma sesión, y **no** tocar nunca el bloque de cierre.
- **`revisar-documento` §7** contiene una etiqueta `HECHO VERIFICADO` sobre lo que *"advierte el fabricante"*, sin fuente. Es epistemología interna del proyecto dentro de un archivo de producto: sobra ahí.

---

## Lo que está bien y no hay que tocar

Para que la lista anterior no se lea como una condena. La distinción **afirma / pide / decide** de `revisar-documento` Fase 3, con el ejemplo de los $18.400.000, es el mejor párrafo del producto: aísla el error que de verdad cambia lo que ella hace hoy. Los cinco grados de certeza de `cronologia` §3 y la separación entre la fecha del documento y la fecha del hecho (§3.1) son mejores que lo que hace la mayoría de los abogados a mano. La regla del hueco **dentro de la frase** de `redactar-escrito` §5, con su justificación de cinco propiedades, está bien razonada hasta el final. Y la guía —salvo H-09, H-10 y H-11— está escrita en el registro correcto: sin jerga, sin condescendencia, y con la sección 4 diciéndole a la cara lo que el producto no va a hacer nunca. Eso es difícil y está conseguido.