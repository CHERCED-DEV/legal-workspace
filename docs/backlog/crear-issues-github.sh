#!/usr/bin/env bash
# Siembra el backlog de GitHub con lo que quedó abierto tras la sesión de
# transcripción del 2026-09-18/19.
#
#   bash docs/backlog/crear-issues-github.sh
#
# Requiere `gh` autenticado con permiso de escritura sobre el repositorio.
# Es idempotente por título: si ya existe un issue abierto con el mismo
# título, lo salta en vez de duplicarlo.
#
# DOS REGLAS QUE ESTE ARCHIVO OBEDECE, Y CONVIENE NO ROMPER AL AÑADIR:
#
# 1. NO se crea un espacio de identificadores nuevo. Cada issue lleva en el
#    titulo el identificador que YA existe — ADR-NNN, su numero de validacion
#    o de pregunta pendiente — y apunta al documento que lo posee. GitHub es
#    la cola de ejecucion; el documento sigue siendo la fuente. La razon esta
#    en BACKLOG-CONSOLIDADO §0.2: cuatro documentos llamaron «septimo
#    comando» a cuatro cosas distintas, y la regla 3 de docs/specs/README.md
#    sale de ahi.
#
# 2. CERO contenido del caso. El repositorio es publico. Las transcripciones,
#    los resumenes y los nombres de las partes viven fuera del control de
#    versiones y se quedan fuera. Estos issues hablan de herramienta y de
#    metodo. Si un item solo se puede explicar citando el expediente, no es
#    un item de este backlog.
set -u

REPO="${REPO:-CHERCED-DEV/legal-workspace}"
ADRS="docs/architecture/adrs"

crear_etiqueta() {
  gh label create "$1" --repo "$REPO" --color "$2" --description "$3" --force >/dev/null 2>&1 \
    && echo "  etiqueta $1" || echo "  etiqueta $1 (ya estaba)"
}

nuevo() {
  local titulo="$1" etiquetas="$2" cuerpo="$3"
  if gh issue list --repo "$REPO" --state all --search "$titulo" --json title \
      --jq '.[].title' 2>/dev/null | grep -qxF "$titulo"; then
    echo "  = ya existe: $titulo"
    return
  fi
  gh issue create --repo "$REPO" --title "$titulo" --label "$etiquetas" --body "$cuerpo" \
    | sed 's/^/  + /'
}

echo "Etiquetas:"
crear_etiqueta "decision-pendiente" "5319e7" "ADR CANDIDATO: espera decision del dueno, no se implementa"
crear_etiqueta "validacion"         "0e8a16" "Medicion o prueba que un ADR declara necesaria y nadie ha hecho"
crear_etiqueta "bloqueante"         "b60205" "Hay trabajo detenido hasta que esto se resuelva"
crear_etiqueta "instrumentacion"    "fbca04" "Las herramientas de control del propio arnes"
crear_etiqueta "producto"           "1d76db" "Construccion y deuda tecnica"

echo
echo "Issues:"

# ─────────────────────────────────────────────────────────────── indice ────
nuevo "Sesion 2026-09-18/19 — el arnes ya oye: indice de lo construido y lo que quedo abierto" \
"producto" \
'Issue indice. No se trabaja aqui: existe para que el resto tenga contexto y para que no se vuelva a mapear lo mismo desde cero.

## Lo que se construyo y esta en `master`

| Commit | Que entro |
|---|---|
| `5c76d68` | `transcribir_audio.py` y la skill `transcribir-audio`. El arnes pasa a oir grabaciones **sin que el audio salga de la maquina** |
| `02af711` | `ADR-020`, `ADR-021`, `ADR-022`, los tres **CANDIDATO** |
| `6498a55` | La superficie de trabajo: pagina local autocontenida, se abre con doble clic y el minuto suena |
| `4749120` | El contrato desacoplado de la pagina, y la cola de comprobacion |
| `0a2c5af` | Licencias de los modelos comprobadas una a una |
| `21fff30` | Pasadas por canal: las grabaciones traian **dos microfonos**, no dos cuantizaciones del mismo |
| `dd355ca` | El diagnostico de saturacion se hacia sobre nuestra propia mezcla, e **inflaba el recorte 25 veces** |
| `2c3472d` | `comparar_iteraciones.py` |
| `6d1a9bd` | El comparador rellenaba la lista hasta ocho por grabacion, hubiera o no conflicto |
| `cfd6d16` | El verificador de citas **aprobaba en blanco** toda cita de menos de cuatro palabras |

Tambien entraron `md2html.py`, `verificar_citas.py`, `comparar_iteraciones.py` y el proyecto Vite `tools/pagina-despacho/` que compila la plantilla.

## Lo que hay que saber antes de ejecutar cualquier otro issue

**Nadie ha oido las grabaciones todavia.** Todo lo medido hasta hoy compara metodos entre si. **Acuerdo no es acierto**: tres decodificaciones pueden coincidir en el mismo error porque comparten modelo. La unica medida real de calidad es la de `ADR-017` validacion 1, que sigue sin hacerse.

**Tres fallos graves de esta sesion estuvieron en el instrumento, no en el modelo** — las cifras de saturacion, el verificador de citas y el comparador. Los tres informaban un resultado con pinta de medida que era un artefacto del procedimiento. Antes de creer una cifra de control propia, comprobar que el instrumento de verdad miro.

**Cuatro ADR estan en CANDIDATO** y nada de lo que proponen se aplica hasta que el dueno decida. Ver las issues con la etiqueta `decision-pendiente`.'

# ──────────────────────────────────────────────── decisiones pendientes ────
nuevo "[ADR-019] Decidir las dos enmiendas a ADR-017: anclaje por palabra y diarizacion" \
"decision-pendiente" \
'`ADR-019` esta en **CANDIDATO** desde el 2026-09-19 y modifica `ADR-017`, que esta en `Proposed`. Documenta que el trabajo real **violo dos decisiones** de aquel ADR.

**Conflicto 1 — §5 e invariante 5** («ningun anclaje depende de la marca de palabra»). Se habia anclado por palabra en el glosario y en las cifras, apoyandose en una marca que el propio ADR declara poco fiable. **Ya corregido en el programa**: el anclaje va al segmento que contiene la palabra. Verificado 58/58 y 11/11.

**Conflicto 2 — §4 e invariante 4** («la diarizacion automatica no cuenta como distincion de voces»). Sigue abierto: los entregables muestran «Hablante N» con advertencia, que es justo lo que el invariante prohibia. La advertencia mitiga, no cumple.

**Lo que se pide decidir:** aceptar las dos enmiendas, rechazarlas, o aceptar una y no la otra. Mientras tanto no se aplica nada y lo producido bajo el metodo viejo se conserva.

Documento: `'"$ADRS"'/ADR-019-el-audio-se-transcribio-y-dos-decisiones-no-resistieron.md`'

nuevo "[ADR-020] Decidir la superficie de trabajo: pagina local autocontenida" \
"decision-pendiente" \
'`ADR-020` esta en **CANDIDATO**. **Extiende `ADR-014`, no lo sustituye**: anade una tercera capa de entrega — una pagina HTML con todo embebido, sin servidor, que se abre con doble clic — y ataca dos consecuencias negativas que `ADR-014` declaraba.

El Word sigue siendo el entregable. Esto es la superficie donde se trabaja antes de producirlo.

**Se implemento ya una version funcional** (`tools/pagina-despacho/`, commits `6498a55` y `4749120`), lo que significa que hay codigo por delante de la decision. Eso no la da por tomada: si se rechaza, el codigo se retira.

**Lo que se pide decidir:** si la tercera capa entra en el modelo de entrega.

Bloquea a `ADR-022`, que define el comportamiento de esta superficie y sin ella no existe.

Documento: `'"$ADRS"'/ADR-020-superficie-de-trabajo-pagina-local.md`'

nuevo "[ADR-022] Decidir el mecanismo de comprobacion: cuatro estados, y que el estado no es prueba" \
"decision-pendiente" \
'`ADR-022` esta en **CANDIDATO** y **depende de `ADR-020`**.

La idea: hacer que comprobar un pasaje contra el audio sea **el camino mas facil** en vez de un deber. Cuatro estados por pasaje, y la propiedad que sostiene todo lo demas — **el estado es constancia de la profesional, no verificacion del sistema**. La decision 5 produciria el primer `provenance_kind = HUMAN_DECISION` real del arnes.

`ADR-017` inv. 1, `ADR-016` y `ADR-014` §3 declararon los tres mitigaciones **debiles**. Este ADR es el intento de hacerlas fuertes.

**Lo que se pide decidir:** si el mecanismo entra, y con el la pregunta que los duenos ya senalaron que se discute con la abogada — **si el estado exportado es dato del caso o documento de trabajo**. Si es dato del caso, entra en el modelo canonico y deja de ser un detalle de interfaz.

Depende de: la decision de `ADR-020`, y de la comprobacion bloqueante del almacenamiento local.

Documento: `'"$ADRS"'/ADR-022-la-comprobacion-es-el-camino-mas-facil.md`'

nuevo "[ADR-021] Decidir enlaces normativos — y esta bloqueado por una comprobacion que nadie ha hecho" \
"decision-pendiente,bloqueante" \
'`ADR-021` esta en **CANDIDATO** y su propio estado dice que **depende de una comprobacion que nadie ha hecho**.

La propuesta: **solo se resuelve lo que el material cita**. El arnes no sugiere normas aplicables — eso activaria la frontera de `preguntas-de-derecho` — sino que enlaza las que el documento ya menciona. Es la unica forma en que el arnes toca una norma sin afirmar nada sobre ella.

**El dueno aplazo este ADR** en la sesion del 2026-09-19. Se deja registrado, no se trabaja.

**No se puede decidir hasta cerrar la comprobacion bloqueante** de enlaces profundos a fuentes oficiales. Si esa comprobacion falla, el ADR cae a su alternativa (b) y la decision es otra.

Documento: `'"$ADRS"'/ADR-021-enlaces-normativos-solo-se-resuelve-lo-que-el-material-cita.md`'

nuevo "[ADR-020 preg.4 / ADR-011 §8] Que pasa con las paginas generadas por una plantilla anterior" \
"decision-pendiente" \
'Pregunta pendiente 4 de `ADR-020`, sin responder.

Cuando la plantilla cambia, las paginas ya generadas con la anterior **se regeneran o se conservan como estaban**. `ADR-011` §8 dice que regenerar produce version nueva y nunca sobrescribe, lo que apunta a conservarlas — pero entonces conviven paginas con comportamientos distintos y hay que poder saber cual es cual.

Se enreda con la pregunta pendiente 4 de `ADR-022`: **si el Markdown se regenera, las anotaciones ancladas al anterior tendrian que migrar o declararse huerfanas**, y eso no esta decidido. Una anotacion que se mueve sola a otro pasaje es peor que una que se declara perdida.

Documento: `'"$ADRS"'/ADR-020-superficie-de-trabajo-pagina-local.md`'

# ─────────────────────────────────────────────────────── validaciones ────
nuevo "[ADR-017 val.1] BLOQUEANTE — la verdad de referencia que nunca se hizo: diez minutos a mano" \
"validacion,bloqueante" \
'**El item mas importante del backlog.** `ADR-017` lo pide como validacion 1 y sigue sin hacerse.

Todo lo medido hasta hoy compara metodos **entre si**. Tres iteraciones sobre el mismo material dan porcentajes de acuerdo — pero **acuerdo no es acierto**: comparten modelo y pueden compartir el error. Sin una referencia hecha a mano **no sabemos el error real de ninguna de las tres**, y cualquier afirmacion sobre cual es mejor es opinion.

**Que hay que hacer:** transcribir a mano diez minutos de material real y medir **cuatro cosas por separado**:

1. Error de palabra.
2. **Cuantos segmentos son texto inventado, contados aparte de los errores.** No es lo mismo equivocarse que fabricar.
3. Deriva de las marcas de tiempo.
4. **Si las señales de confianza separan los segmentos malos de los buenos.**

**El punto 4 tiene consecuencia inmediata:** si no separan, la decision 3 de `ADR-017` pierde su base y hay que rehacerla. Hay ya un indicio en contra — el metodo por lotes resulto **mas rapido y peor**, perdiendo un 8,4 % de las palabras **mientras su confianza declarada subia**.

Documento: `'"$ADRS"'/ADR-017-audio-transcription-boundary.md`'

nuevo "[ADR-020 val.5 / ADR-022 val.4] La hipotesis central del producto, sin medir" \
"validacion,bloqueante" \
'`ADR-020` y `ADR-022` descansan enteros en una creencia: **que una pagina donde el minuto suena al pulsarlo hace que se comprueben mas pasajes que una lista en Word.** Hoy eso no esta medido. Es una hipotesis, y esta escrito asi en los dos ADR.

**Que hay que hacer:** darle a la abogada la misma lista de pasajes en las dos formas y **contar cuantos comprueba en cada una**, cuanto tarda, y — esto es lo que decide si `ADR-022` se sostiene — **si entiende que «confirmado» es afirmacion suya y no del sistema**.

**Si el numero no sube, los dos ADR se caen** y el trabajo hecho sobre la pagina hay que reconsiderarlo entero. Merece la pena medirlo antes de construir mas encima.

Documentos: `'"$ADRS"'/ADR-020-...md` (val. 5), `'"$ADRS"'/ADR-022-...md` (val. 4)'

nuevo "[ADR-022 val.1] BLOQUEANTE — almacenamiento local en file:// con dos casos abiertos a la vez" \
"validacion,bloqueante" \
'Validacion 1 de `ADR-022`, marcada **BLOQUEANTE** en el propio ADR.

Los navegadores tratan los archivos abiertos desde disco como **origen opaco**. El almacenamiento local puede estar **bloqueado**, o — peor — **compartido entre archivos distintos**. Si dos paginas de casos distintos comparten almacenamiento, las marcas de comprobacion de un caso aparecen en el otro. En material legal eso no es un fallo de interfaz.

**Que hay que hacer:** comprobarlo **en el navegador real de ella**, no en uno de desarrollo, con **dos paginas de casos distintos abiertas a la vez**.

**Si falla o se mezcla, la decision 6 de `ADR-022` cambia** y hay que buscar otro sitio donde vivan las marcas.

Relacionada: validacion 5 del mismo ADR — marcar veinte pasajes, limpiar los datos del navegador, y comprobar que la pagina **detecta la perdida y lo dice**, en vez de mostrar todo como sin comprobar sin explicar por que.

Documento: `'"$ADRS"'/ADR-022-la-comprobacion-es-el-camino-mas-facil.md`'

nuevo "[ADR-021 val.1] BLOQUEANTE — ¿existen enlaces profundos estables a fuentes oficiales colombianas?" \
"validacion,bloqueante" \
'Validacion 1 de `ADR-021`, marcada **BLOQUEANTE**. **Nadie lo ha comprobado**, y de esto depende que el ADR sea viable o haya que cambiarlo de raiz.

**Que hay que hacer:** comprobar contra fuentes oficiales colombianas que existe un patron de direccion **estable y verificable** para al menos cuatro casos: **un decreto, una ley, un articulo concreto, y una sentencia de la Corte Constitucional**.

**Si no existe patron estable, se aplica la alternativa (b) del ADR** — no hay enlaces, solo resaltado.

Dos comprobaciones mas del mismo ADR, que se pueden hacer en la misma pasada:

- **Prueba de la version:** tomar una norma **modificada despues de su expedicion** y ver que texto sirve la fuente oficial. Confirma o refuta la premisa de la decision 4. Enlazar a un texto derogado sin decirlo seria peor que no enlazar.
- **Prueba de identificador ambiguo:** material que dice «el 1077» sin mas. Debe resaltarse **sin enlace** y declarar que no se pudo resolver.

El dueno aplazo este ADR; esta comprobacion es lo unico que conviene adelantar, porque decide si el ADR tiene sentido.

Documento: `'"$ADRS"'/ADR-021-enlaces-normativos-solo-se-resuelve-lo-que-el-material-cita.md`'

nuevo "[ADR-017 val.2] Prueba adversarial del invariante 1: insertar una frase fabricada" \
"validacion" \
'Validacion 2 de `ADR-017`. La hipotesis del ADR es que **un lector no detecta una frase inventada sin oir el audio**, y de eso depende que el invariante 1 — que obliga a escuchar — este justificado.

**Que hay que hacer:** dar a un lector una transcripcion con una frase fabricada insertada y ver si la encuentra.

**Ya hay un indicio fuerte a favor de la hipotesis, y sale de esta sesion.** Al redactar un resumen a partir de transcripciones correctas se escribieron **tres citas que no eran textuales** — una palabra cambiada, una frase inventada y un cargo sustituido — y **no se detectaron releyendo**. Dieciocho de veintiuna si eran exactas, que es justo lo que hace peligroso el fallo: el documento se lee impecable. Solo cayeron al cotejarlas con un programa.

Eso apoya la hipotesis pero **no es la prueba**: el lector era quien habia escrito el texto. Hace falta un lector que no lo haya redactado.

Documento: `'"$ADRS"'/ADR-017-audio-transcription-boundary.md`'

nuevo "[ADR-017 val.3] Medir la diarizacion con numero de hablantes conocido" \
"validacion" \
'Validacion 3 de `ADR-017`. De esto depende el conflicto 2 de `ADR-019`.

**Que hay que hacer:** grabar o escoger material con **numero de hablantes conocido** y contar **frases mal atribuidas**. Si el resultado se parece al 17-20 % publicado para este tipo de sistema, la decision 4 de `ADR-017` queda confirmada empiricamente y la advertencia actual de los entregables esta bien calibrada.

Importa porque hoy los entregables muestran «Hablante N» y una advertencia, y **no hay ninguna medida propia de cuanto se equivoca**. La cifra que se usa viene de fuera.

Documento: `'"$ADRS"'/ADR-017-audio-transcription-boundary.md`'

nuevo "[ADR-022 val.2 / ADR-017] Prueba de reproduccion y deriva de marcas de tiempo" \
"validacion" \
'Validacion 2 de `ADR-022`, que **cierra ademas la prueba de deriva que `ADR-017` dejo pendiente** — dos items con una sola medicion.

**Que hay que hacer:** escoger **diez marcas de tiempo al azar** y comprobar que el audio suena donde la pagina dice. No las primeras diez: al azar, y repartidas por toda la grabacion, porque la deriva se acumula.

`ADR-011` §Riesgos nº 4 ya lo señalaba y proponia exactamente esta prueba de anclaje al azar. **No se hizo.**

Junto con esta, la validacion 3 de `ADR-022`: **copiar un fragmento y pegarlo en Word**, y comprobar que llega el localizador y la marca de derivado, y que **se ven**. Un fragmento que viaja sin su procedencia es una cita huerfana esperando a ser usada como si estuviera comprobada.

Documento: `'"$ADRS"'/ADR-022-la-comprobacion-es-el-camino-mas-facil.md`'

nuevo "[ADR-020 val.1-4] Las cuatro pruebas de la pagina: red cero, viaje, vista honesta y no divergencia" \
"validacion" \
'Validaciones 1 a 4 de `ADR-020`. Son baratas y ninguna esta hecha.

1. **Red cero.** Abrir la pagina con el equipo desconectado y el registro de red del navegador abierto. **Cero peticiones.** Si hay una, el ADR esta incumplido — y la promesa de que el material no sale de la maquina, tambien.
2. **El viaje.** Copiar **solo el `.html`** a otra carpeta y otra maquina. Debe abrir, verse igual, y **declarar que no lleva el audio** en vez de fallar en silencio al pulsar un minuto.
3. **La vista honesta.** Imprimir la pagina **en blanco y negro** y comprobar que **sigue distinguiendose lo verificado de lo dudoso**. Si la distincion vive solo en el color, desaparece en la primera fotocopia del expediente.
4. **No divergencia.** Modificar el `.md`, regenerar, y comprobar que la pagina cambia **y que no existe ningun camino para el cambio inverso**. La pagina es derivada; si se puede editar y que eso vuelva al Markdown, hay dos fuentes.

Documento: `'"$ADRS"'/ADR-020-superficie-de-trabajo-pagina-local.md`'

# ────────────────────────────────────────────────────── instrumentacion ────
nuevo "[instrumentacion] Pruebas de regresion para verificar_citas.py y comparar_iteraciones.py" \
"instrumentacion" \
'**Los dos programas de control del arnes fallaron en la misma sesion, y de la misma forma: informaban un resultado tranquilizador sin haber mirado.** Ninguno de los dos tenia prueba automatica. Arreglados en `cfd6d16` y `6d1a9bd`, pero **nada impide que vuelva a pasar**.

`verificar_citas.py` solo puntuaba fragmentos de cuatro palabras o mas; una cita mas corta salia del bucle sin comprobar y se contaba como textual. Decia «18 de 18» habiendo mirado 15.

`comparar_iteraciones.py` devolvia siempre los ocho tramos de menor acuerdo por grabacion, hubiera o no conflicto. Se reporto que habia 24 puntos que oir; habia 47, muy desigualmente repartidos.

**Casos minimos que las pruebas deben cubrir:**

- Una cita de **dos palabras que NO esta en la fuente** debe salir `NO TEXTUAL`. Es el caso que se colaba.
- Una cita que esta **solo en una de varias carpetas** debe salir textual, y decir en cual.
- Una carpeta **sin discrepancias** debe reportar **cero tramos**, no N.
- Un fichero de datos **sin marcas de palabra** no debe reventar ni contar como acuerdo perfecto.

Conviene una regla general al anadir cualquier control nuevo: **toda herramienta que pueda decir «todo bien» necesita un caso que la haga decir «mal»**, o su aprobado no vale nada.'

nuevo "[ADR-017 preg.5] Licencias de los modelos: la atribucion obligatoria y el uso comercial" \
"producto,bloqueante" \
'Pregunta pendiente 5 de `ADR-017`, **parcialmente resuelta** en el commit `0a2c5af` y con un cabo suelto que puede ser bloqueante de verdad.

**Lo comprobado:** la diarizacion se monto sobre modelos ONNX que evitan el problema — `pyannote-segmentation-3.0` (MIT) y `wespeaker` VoxCeleb CAM++ (**CC BY 4.0**).

**El cabo suelto: CC BY 4.0 EXIGE atribucion.** Hay que comprobar que la atribucion **aparece de verdad en los entregables que salen del despacho**, no solo en `scripts/modelos/PROCEDENCIA.md`. Un entregable que usa el modelo sin citarlo incumple la licencia, y lo firma una abogada.

**Y la pregunta de fondo, sin contestar:** varios modelos empaquetados por defecto con los motores recomendados estan **restringidos a uso personal sin animo de lucro**. **Trabajo juridico remunerado probablemente no cabe ahi.** Hoy se evita usandolos, pero eso es una restriccion viva sobre que se puede instalar despues, y conviene dejarla escrita donde se vea antes de anadir un modelo nuevo.

Documentos: `'"$ADRS"'/ADR-017-audio-transcription-boundary.md`, `plugins/despacho/scripts/modelos/PROCEDENCIA.md`'

nuevo "[producto] tools/pagina-despacho se publica a mano y nada comprueba que lo publicado sea el fuente" \
"producto" \
'La plantilla de la pagina se compila con Vite en `tools/pagina-despacho/` y se copia a `plugins/despacho/scripts/plantilla/pagina.html` ejecutando `publicar.mjs` **a mano**.

**No hay nada que compruebe que la plantilla publicada corresponde al fuente actual.** Si alguien toca `src/` y no publica, o publica y no comite, las dos versiones divergen en silencio — y la que se entrega es la publicada.

Es la misma forma de fallo que `ADR-014` invariante 6 describe para las dos capas de entrega: **dos artefactos que deberian decir lo mismo y nada obliga a que lo digan.**

**Salidas posibles**, por orden de coste: comprobar en CI que republicar no cambia el archivo; o generar la plantilla en tiempo de build y no versionarla; o dejarlo como esta y documentarlo, que es lo que hay hoy sin decirlo.

Nota de contexto: esto vive en `tools/` y no en `plugins/` a proposito — la abogada **no tiene Node**, y el arnes no puede depender de el. Cualquier salida tiene que respetar eso.'

echo
echo "Hecho. Revisa: https://github.com/$REPO/issues"
