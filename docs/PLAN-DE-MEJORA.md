# Plan de mejora del arnés Despacho

**Fecha:** 2026-08-26 · **Base:** primera ejecución real sobre el caso de familia (56 páginas, 4 de 6 comandos), nueve evaluaciones por comando y transversales, y una refutación que verificó contra los archivos.

**Regla de este documento:** manda el refutador. Lo que tumbó no entra. Lo dudoso entra marcado como dudoso, con lo que hay que comprobar antes de tocarlo. Las cifras llevan etiqueta: **HECHO MEDIDO** (verificado contra archivo o log), **SUPUESTO** (estimación razonada, no medición), **POR VERIFICAR**, **RIESGO**, **DECISIÓN PENDIENTE**.

---

## §0 — El diagnóstico en diez líneas

1. **La veracidad aguantó y es el activo del producto.** HECHO MEDIDO: 0 contenidos atribuidos a las 25 páginas ilegibles, 25 de 25 declaradas, 647 fragmentos contrastados, 239 anclajes verificados con **1** error.
2. **La proporción no aguantó.** HECHO MEDIDO: 3.286 líneas de salida en `.md`/`.txt` (215 KB) más un `.docx` de 51 KB, producidas sobre **14 páginas legibles de 39** de anexos.
3. **El coste.** HECHO MEDIDO: cuatro comandos, 16 / 30 / 37 / 97 turnos, 0,9 / 2,9 / 2,7 / 12,0 M de contexto releído. **~3 M facturables y 50,8 M releídos** por un caso.
4. **Nadie sabe dónde se fue ese dinero.** POR VERIFICAR: los logs no separan `cache_read` de `input`. El `SKILL.md` va al frente del prefijo, que es lo más cacheable que existe. Todo cálculo de ahorro por recortar prosa del método es hoy conjetura.
5. **La causa medible del coste no es la longitud del método: son los turnos**, y los turnos salen de dos bucles escritos dentro del método — la Fase 4 manda recorrer el material *por hecho* (76 barridas) y la Fase 6.1 abrir los anclajes *uno por uno* (239 aperturas), donde caben 14 y 14.
6. **El tapón que el informe declaró no existe.** HECHO VERIFICADO en `redactar-escrito/SKILL.md:106`: la puerta es blanda, ofrece seguir con encabezado sellado. Lo que detuvo la corrida fue que **nadie dijo nunca a quién representa ella**.
7. **La hoja de decisiones no lleva cita ni página.** HECHO VERIFICADO en la salida, líneas 99-112: las columnas son `Hecho | Enunciado | Estado y apoyo | Sí | No | A medias`. El enunciado es prosa del modelo. Aprobar desde ahí es aprobar texto que ella no vio.
8. **El camino de instalación tiene cero ejecuciones.** HECHO VERIFICADO: `git remote -v` vacío, `installed_plugins.json` = `{}`. El producto nunca ha llegado a ninguna máquina por la vía prevista; las 3.286 líneas salieron de leer el árbol de trabajo.
9. **Existe un banco de evaluación escrito —678 líneas, seis fixtures, protocolo con truth set— y ninguna de las nueve evaluaciones lo mencionó.** Hoy no hay ninguna prueba capaz de fallar.
10. **Lo que cuesta hoy para ella:** un día que empieza en el Explorador de Windows, termina sin una sola pieza presentable, y deja por delante ~2 horas de marcar 76 casillas en un `.md` que quizá no abra con doble clic.

---

## §1 — Lo que NO se toca

Se empieza por aquí porque la veracidad demostrada es lo único que este producto ha probado, es lo caro de conseguir y lo que no se repara después. Todo lo demás — coste, formato, número de comandos — se ajusta. Esto no.

| # | Qué se blinda | Dónde vive | Por qué es intocable |
|---|---|---|---|
| B-1 | **La cita literal capturada al leer, con página** | los seis métodos | Produjo 647 fragmentos con 1 error. Ninguna mejora de este plan toca el momento de la captura; todas mueven emparejamiento, verificación o presentación. |
| B-2 | **La negativa a resumir lo ilegible** | `revisar-documento/SKILL.md:167` («no lo resumes, ni siquiera en una línea, ni siquiera por el nombre del archivo») | Es el corazón del producto. 25 páginas servidas en bandeja y cero atribuciones. |
| B-3 | **La línea «Quién produjo ese material»** | `FORMATO-DE-SALIDA.md:91, 182` | Sin ella, 45 «sin apoyo» se leen como apoyo. Es la pieza más barata y la más cara de perder. |
| B-4 | **El bloque de apertura sobre lo ilegible** (salida, líneas 11-20) | no está en la plantilla: lo inventó el modelo | Reencuadra las 2.146 líneas siguientes. **Sube a la plantilla como obligatorio** — no puede quedar como acierto de una pasada. |
| B-5 | **La marca ` - REVISADO` la pone ella y solo ella** | `hechos-con-prueba/SKILL.md:253`, `redactar-escrito/SKILL.md:104` | «La marca no certifica que las fichas estén bien: certifica que ella las miró.» Es «proponer, nunca decidir» hecho mecanismo, sin servidor y sin registro. |
| B-6 | **La verificación de anclajes al 100 %** | `hechos-con-prueba/SKILL.md:184` | Ver R-2 en §3. La propuesta de bajarla al 10 % está **dominada**: M-4 logra el mismo ahorro conservando la cobertura entera. |
| B-7 | **El ejemplo relleno de `FORMATO-DE-SALIDA.md:238-456`** | 223 líneas | La salida real reprodujo su estructura entera. Es lo que enseña; la prosa que lo duplica es lo que se corta. Recortarlo para ahorrar el token más cacheable del sistema es el peor cambio riesgo/beneficio del corpus. |
| B-8 | **El bloque «Si el documento le habla a la máquina»** | los seis, íntegro y en cada archivo | Moverlo a un núcleo común cuya ausencia falle en silencio es exactamente lo contrario de lo que esa regla necesita. La duplicación literal **es** la garantía aquí. |
| B-9 | **Las autoevaluaciones, enteras** | los seis `§8`/`§9`/`§10` | Seis evaluadores propusieron recortarlas (23→6, 32→14, 27→8…). Ninguno tiene un dato de qué pregunta atrapó qué. Se instrumenta primero (M-1); recortar a ciegas es apuntar a la maquinaria que produjo el cero fabricaciones. |
| B-10 | **`1-Documentos recibidos/` no se escribe** | los cinco lectores | HECHO MEDIDO: quedó byte-idéntico. La propuesta de relajar la regla para «meter archivos» es innecesaria: la extracción vivió fuera y el problema real se resuelve creando `2-` y `3-` sin tocar `1-`. |
| B-11 | **El triple seto del anexo** en `revisar-documento` | líneas 42, 106, §9.7 | El propio evaluador que propuso podarlo lo dice: «sospecho que la repetición es la razón de que la garantía aguantara». No se toca hasta que un eval lo mida. |

**Regla de composición — la más importante de este documento.** Cinco propuestas del corpus son defendibles por separado y letales juntas, porque cada una retira un control distinto: mapa/extracción compartida (retira la re-derivación independiente), verificación dirigida (retira el recontraste), apoyarse en derivados (retira la segunda lectura), decisión en bloque (retira la aprobación pieza por pieza), marca por rango (retira el paso del ojo). Juntas dan un sistema donde nada se deriva dos veces, nada se recomprueba y nada se aprueba individualmente. Y que cuatro comandos coincidieran en las 25 páginas ilegibles no es redundancia: **esa coincidencia es la medición**.

> **REGLA DE LIBERACIÓN: como máximo UNA de esas cinco por versión, con el fixture corrido antes y después.**

---

## §2 — La economía

### 2.1 Lo que se midió

| | Turnos | Salida (bytes) | Contexto releído |
|---|---:|---:|---:|
| Comando más barato (`revisar-documento`) | **16** | 19.223 | 0,9 M |
| Sin etiquetar | 30 | 64.332 | 2,9 M |
| Sin etiquetar | 37 | 48.441 | 2,7 M |
| Comando más caro (`hechos-con-prueba`) | **97** | 75.524 | 12,0 M |
| **Total** | **180** | ~207 KB | **50,8 M** · ~3 M facturables |

HECHO MEDIDO, pero incompleto: **dos de las cuatro filas no tienen nombre de comando.** Por eso `cronologia` tuvo que pedirle el dato al dueño y `estado-del-caso` estimó 35-55 turnos a ciegas. Etiquetarlas cuesta un minuto y contesta preguntas de dos evaluaciones.

### 2.2 Dónde se va el gasto — y por qué la respuesta de todos era la equivocada

Reparto estimado del contexto en la corrida de 97 turnos (**SUPUESTO**, aritmética del evaluador transversal, no medición):

| Componente | Peso | Consecuencia |
|---|---:|---|
| Método releído (829 líneas ≈ 16.100 tokens × 97) | ~13 % | recortarlo a la mitad ahorra **~6 %** de la corrida |
| Material extraído | ~23 % | se ataca no volviendo a extraer |
| **Transcripción acumulada** (salida en construcción, resultados de herramienta, razonamiento) | **~64 %** | **se multiplica por el número de turnos** |

Y encima ese ~13 % está probablemente sobrevalorado. **POR VERIFICAR (R-4):** los mismos logs dan ~3 M facturables contra 50,8 M releídos — 17× de diferencia. Si cada turno pagara el prefijo entero a precio completo, esa proporción no sería posible. El `SKILL.md` va al frente del prefijo: es el contenido más cacheable de toda la corrida.

> **Unas 20 de las ~65 propuestas del corpus son recorte de prosa del método. Todas juntas valen ~6 % de la corrida, y probablemente mucho menos. Cinco evaluadores lo intuyeron sin saber por qué — «recortar líneas es propina». Tenían razón.**

**Bajar de 97 a 35 turnos ahorra ~60 % por sí solo**, porque todo lo demás se multiplica por el número de turnos. Ahí está el dinero.

### 2.3 Líneas actuales y objetivo por método

| Método | Hoy | Objetivo | Δ | Qué se corta / se añade |
|---|---:|---:|---:|---|
| `hechos-con-prueba` (SKILL + FORMATO) | 373 + 456 = **829** | ~600 | −28 % | fusionar los dos archivos (**por ambigüedad de plantillas, no por economía**: hay dos plantillas de ficha que difieren y la salida tuvo que reconciliarlas 76 veces); borrar el esqueleto de `SKILL.md:196-229`; **el ejemplo relleno no se toca** |
| `estado-del-caso` | **319** | ~290 | −9 % | −55 (§6, §5 colapsado sobre §4), +25 (escritura dirigida, unidad «pieza», excepción de la fecha de hoy) |
| `inventario-de-anexos` | **297** | ~287 | −3 % | −29 de prosa duplicada, +19 de reglas del `.docx` y etiquetas `A-xx` |
| `cronologia` | **288** | ~272 | −6 % | −31 (plegar *deducida*, remates duplicados), +15 (conductas sostenidas, jerga, cabecera) |
| `redactar-escrito` | **285** | ~273 | −4 % | −28 de justificación de diseño, +16 (Fase 0, aprobación parcial) |
| `revisar-documento` | **272** | ~262 | −4 % | −25 de reglas repetidas tres veces, +15 (página cero, regla de escala) |
| **Total método** | **2.290** | **~1.984** | **−13 %** | |

**Léase esta tabla con desconfianza.** Es la parte del plan que menos rinde y la que más fácil parece. Su justificación real no es el token: es que hoy hay reglas contradictorias entre archivos (dos plantillas de ficha, «SOLO ALEGADO» como sexto estado clandestino, la fecha de hoy prohibida por la línea 85 y exigida por la 184), y una regla contradictoria enseña a incumplirla.

### 2.4 Reducción estimada de turnos

**SUPUESTO en su totalidad. Ninguna de estas cifras es una medición y ninguna se puede confirmar sin M-1.**

| Palanca | Mecanismo | Turnos hoy | Turnos objetivo |
|---|---|---:|---:|
| M-4 · reindexar por pieza | Fase 4: 76 barridas → 14. Fase 6.1: 239 aperturas → 14 | 97 | **45-60** |
| M-3 · preguntar antes de leer | el camino de fallo garantizado deja de leer 56 páginas | ~30 | **1-2** |
| M-12 · mapa compartido *(dudosa)* | 4 derivaciones del mismo mapa → 1 | −20 a −35 % en cada comando posterior al primero | |
| Recorte de prosa del método | −13 % de líneas | | **~−2 %** de la corrida |

**El techo honesto:** con M-4 y M-3, el comando caro baja quizá a la mitad y el flujo deja de tener un camino que siempre falla caro. Eso **no** es un cambio de orden de magnitud. El cambio de orden de magnitud está en el conjunto que la regla de composición limita a uno por versión — es decir, en cuatro o cinco versiones con medición entre cada una, no en un empujón.

---

## §3 — Las mejoras, ordenadas por valor entre esfuerzo

Doce. Cada una con el veredicto del refutador tal como quedó.

---

### M-1 · Instrumentar antes de cortar una sola línea
**Qué.** Cuatro medidas, ninguna de las cuales toca el producto: (a) etiquetar con nombre de comando las cuatro filas de la tabla de coste; (b) separar `input` / `cache_creation` / `cache_read` en los logs de la corrida de 97 turnos; (c) hacer que la Fase 6.1 registre **cuántos anclajes corrigió**; (d) que cada pasada imprima qué preguntas de la autoevaluación provocaron una corrección.
**Dónde.** `docs/discovery/primera-ejecucion-real.md:100`; logs de la corrida; `hechos-con-prueba/SKILL.md:184` y §10; equivalentes en los otros cinco.
**Qué gana.** Convierte todo el debate de §2 en ingeniería. (b) decide si veinte propuestas valen algo. (c) decide si la Fase 6.1 se puede tocar: HECHO MEDIDO es que **1 error atravesó esa fase y llegó al entregable**; nadie sabe cuántos atrapó. (d) desactiva las seis propuestas de recortar autoevaluación o las autoriza con datos.
**Qué cuesta.** Una corrida y unas horas. Nada más.
**Qué garantía toca.** Ninguna. Solo produce información.
**Esfuerzo.** BAJO. **Veredicto: prerrequisito de todo lo demás (R-4, R-5, R-7).**

---

### M-2 · Blindar la marca ` - REVISADO` contra la extensión oculta de Windows
**Qué.** Aceptar como marca válida cualquier nombre que **contenga** ` - REVISADO` antes de la extensión, no solo el que **termine** en ` - REVISADO.md`.
**Dónde.** `redactar-escrito/SKILL.md:104`, `hechos-con-prueba/SKILL.md:250`, `inventario-de-anexos/SKILL.md:89`, `GUIA-PARA-LA-ABOGADA.md:279`.
**Qué gana.** La instrucción que ella recibe es «añada ` - REVISADO` al final del nombre». Con extensiones ocultas (el defecto de Windows) sale `Hechos - … - REVISADO.md` y funciona; con extensiones visibles sale `Hechos - … .md - REVISADO`, que **no cuenta**. El síntoma: revisó las 76 fichas, hizo lo que le pidieron, y el sistema le dice que no hay hechos aprobados. **Es el único fallo del producto que castiga a la usuaria por haber hecho el trabajo más caro que se le pide.**
**Qué cuesta.** Nada de veracidad. Un archivo llamado `Hechos - REVISADO - borrador viejo.md` contaría; caso rebuscado frente a un fallo cotidiano.
**Qué garantía toca.** Ninguna. La marca la sigue poniendo ella; cambia cuántas formas de escribirla se reconocen.
**Esfuerzo.** BAJO. **Veredicto: SOSTIENE. La victoria más barata del corpus.**

---

### M-3 · «¿A quién representa usted?», antes de abrir ningún documento
**Qué.** Una Fase 0 en `redactar-escrito` que (a) haga las preguntas que no dependen del expediente **antes** de leerlo, empezando por a quién representa ella, y (b) **guarde la respuesta** para que los otros cinco no la vuelvan a descubrir, esquivar o suponer.
**Dónde.** `redactar-escrito/SKILL.md`, insertar antes de la línea 98; consumo en `inventario-de-anexos` §1 y `revisar-documento` Fase 5.
**Qué gana.** Es lo que de verdad detuvo la corrida. HECHO VERIFICADO: de las cinco preguntas del archivo de no-borrador, **cuatro no tocan los hechos**. Dos salidas independientes hicieron la misma pregunta y **ninguna guardó la respuesta**. Y la primera invocación sobre cualquier caso recorre hoy el camino caro por definición: lee 56 páginas para terminar preguntando cinco cosas. Con Fase 0 ese fallo garantizado cuesta 1-2 turnos.
**Qué cuesta.** Se pregunta con menos contexto. Se compensa leyendo solo carátula, firma y poder — unas cuatro páginas — que es de donde salió el hallazgo bueno («no doy por hecho que usted sea esa apoderada»).
**Qué garantía toca.** Refuerza «no inventar»: hoy nada prohíbe suponer que ella es la firmante del escrito que tiene delante.
**Esfuerzo.** BAJO. **Veredicto: SOSTIENE. Junto con M-4, lo más importante del corpus.**

---

### M-4 · Reindexar la Fase 4 y la Fase 6.1 por pieza, no por hecho ni por anclaje
**Qué.** Fase 4: para cada pieza legible, decir a qué hechos candidatos apoya, contradice o sitúa. Fase 6.1: abrir cada pieza **una vez** y contrastar de golpe todas las citas que dicen salir de ella.
**Dónde.** `hechos-con-prueba/SKILL.md:111` («Para cada hecho candidato, **recorre el material**») y `:184` («abre cada anclaje que citaste, **uno por uno**»). Misma cadena en `cronologia` Fases 1-3 e `inventario-de-anexos` Fases 1-4.
**Qué gana.** Ahí está el multiplicador de los 97 turnos: el método escribe dos bucles anidados. Este caso pide 76 barridas y 239 aperturas donde caben **14 y 14** — solo hay 14 páginas legibles más la demanda. Con 647 citas sobre 31 páginas, cada página se visitó unas 21 veces.
**Qué cuesta.** Hay que sostener la lista de candidatos mientras se lee una pieza. Mitiga que la lista ya está escrita: es el producto declarado de la Fase 3.
**Qué garantía toca.** **La refuerza.** Ver de una vez las doce afirmaciones que dicen «Anexos, p. 23» contra la p. 23 real detecta la que sobra; abrirlas de una en una, no. Y conserva la cobertura al **100 %**.
**Esfuerzo.** BAJO. **Veredicto: SOSTIENE — la mejor del corpus. Y domina a la propuesta de verificación dirigida (R-2): mismo ahorro, cobertura entera, más detectora. Cheaper *and* stronger.**

---

### M-5 · Que la tabla del inventario sirva para pegarla en un escrito
**Qué.** Escribir en la skill las reglas de construcción del `.docx`: orientación vertical, anchos de columna por contenido, fila de títulos repetida en cada página, y §3 como lista y no como tabla. Y partir §2 en dos: la tabla que se pega (`N.º · Qué es · Quién lo produjo · Fecha`) y la de trabajo.
**Dónde.** `inventario-de-anexos/SKILL.md:17` y §7 líneas 184, 206-217.
**Qué gana.** El comando promete «lista para pegar en un escrito» y no lo está. HECHO MEDIDO dentro del `.docx`: `orient="landscape"`, siete `gridCol` idénticos de 2163 twips (la columna «N.º», 2 caracteres de media, recibe lo mismo que «Quién lo produjo», con 110 de media y 214 de máximo), cero ocurrencias de `tblHeader` en cuatro tablas, cuerpo a 8,5 pt. Hoy, para usarla, ella tiene que girar la página, redimensionar siete columnas, repetir los títulos a mano y borrar dos columnas y cuatro filas.
**Qué cuesta.** Nada. Es forma. Único riesgo: fijar anchos concretos envejece mal — se da la regla, no la tabla de valores.
**Qué garantía toca.** Ninguna.
**Esfuerzo.** BAJO. **Veredicto: SOSTIENE — la de mayor rendimiento para ella en todo el lote.**

---

### M-6 · Prohibir la re-transcripción
**Qué.** Numerar las líneas de los apartados 2, 3 y 4 de `revisar-documento`, y establecer que una frase ya transcrita no se vuelve a copiar en los apartados 5, 6 y 7: se remite por número con un fragmento corto al lado. Añadir al §9: «¿alguna cita aparece dos veces?» y «¿alguna remisión apunta a un número que no existe?».
**Dónde.** `revisar-documento/SKILL.md:143-153` y §9.
**Qué gana.** HECHO MEDIDO sobre la salida: el apartado 6 repite 9 de sus 11 citas largas del apartado 3; el 5 repite 17 de 41; el 7 repite 16 de 28. **223 de 597 líneas son material que ella ya pasó.** La revisión es 5.327 palabras contra 4.168 de la demanda que revisa: devuelve un 28 % **más** texto del que ahorra leer. Se van ~110 líneas sin borrar una sola cita.
**Qué cuesta.** Ella pierde la comodidad de leer un apartado sin saltar. Y aparece un modo de fallo nuevo — la remisión rota — que por eso va al §9.
**Qué garantía toca.** Ninguna: cada cita sigue en la salida, íntegra, con su página, **una vez**.
**Esfuerzo.** BAJO. **Veredicto: SOSTIENE — mejor relación del lote de salida.**

---

### M-7 · Lote de higiene: cuatro arreglos gratis que hoy son incumplimientos
**Qué.** (a) Sacar de la salida el vocabulario interno del método — «sin ancla» → «nada en el material dice cuándo fue», «coordenada» → «documento y página»; (b) cerrar el sexto estado clandestino, dejando escrito que `SOLO ALEGADO` es la etiqueta del bloque de pruebas, no un estado; (c) dejar de imprimir las líneas que salen vacías con un guion; (d) cerrar la única fuga de derecho sustantivo y el criterio que la abrió.
**Dónde.** (a) `cronologia/SKILL.md:134, 161`, §2 regla 1 y ocho filas de la salida. (b) `FORMATO-DE-SALIDA.md:75, 106` contra `:97` y `SKILL.md:144`. (c) `FORMATO-DE-SALIDA.md:189-191` y el ejemplo, líneas 360 y 400. (d) salida línea 2121 y `hechos-con-prueba/SKILL.md:190`.
**Qué gana.** (a) «Cero jerga» es regla dura y hoy se incumple en al menos ocho filas, **con la traducción ya escrita en la columna de al lado**. (b) El archivo se salta su propia regla dos veces y la salida tuvo que reconciliarlo 45 veces. (c) 35 líneas «Alcance de la cita: —» + 24 «Qué haría falta: nada» — y ese hábito entrena el ojo a saltarse la línea justo donde a veces dice lo único que importa (H-14, H-43, H-68). (d) HECHO VERIFICADO en la salida, línea 2121: *«es la pieza del requisito de procedibilidad que sí está»* — categoría jurídica en voz propia del método. Una sola en 2.156 líneas, pero es la regla 1.
**Qué cuesta.** Nada. En (d) la prioridad de esa entrada no cambia: se dice sin nombrar la categoría.
**Qué garantía toca.** Refuerza tres reglas duras que hoy están rotas en sitios localizados.
**Esfuerzo.** BAJO. **Veredicto: SOSTIENE las cuatro.**

---

### M-8 · Escritura dirigida del archivo de estado
**Qué.** Sustituir «reescribe el archivo entero conservando sus notas» por: se reemplaza únicamente el texto por encima de la línea marcadora `NOTAS SUYAS`; lo de debajo **no se lee para volver a teclearlo**. Si la marca no aparece, no se escribe: resumen en pantalla y se dice por qué. Y regla nueva para el texto suyo que aparezca fuera del bloque: baja al bloque de notas transcrito, con una línea que diga de dónde venía, y se le avisa en pantalla.
**Dónde.** `estado-del-caso/SKILL.md:162-163, 171, 174`, §8.9; y la contradicción entre la línea 65 (Fase 0) y §4 líneas 180-212.
**Qué gana.** El propio método admite el fallo en la línea 171: conservar sus notas «depende de volver a teclearlo bien». **Eso es autoatestación sobre justo lo que un modelo hace mal.** No hay copia en este sistema: cada vez que un texto aparece en una salida se re-emite token a token (R-3). Es el único punto del producto donde un texto **de ella** puede salir parafraseado, y la copia de seguridad solo lo salva si ella lo nota — una normalización silenciosa no se nota. Y está pasando hoy: el `0-Estado del caso` real está escrito a mano y sus dos mejores bloques no existen en la plantilla de §4; una pasada que aplique §4 al pie de la letra los borra.
**Qué cuesta.** Depende de una línea marcadora estable. Si ella la borra, el comando se detiene sin escribir — correcto pero visible.
**Qué garantía toca.** Refuerza «proponer, nunca decidir»: lo que ella escribió pasa a ser intocable a nivel de bytes, no de buena voluntad.
**Esfuerzo.** MEDIO. **Veredicto: SOSTIENE — la única del corpus que le quita al modelo la copia de un texto de ella.**

---

### M-9 · Dos niveles de ficha — y la hoja de decisiones con cita literal y página
**Qué.** Nivel completo para todo hecho con al menos una prueba de cualquier polaridad, más todo lo contradicho (41 en este caso). Nivel de una línea, en bloque, para los hechos cuyo único origen es un escrito de una parte y que no tienen ninguna prueba (35). **Condición innegociable:** el renglón comprimido lleva **cita literal y página**, y la marca de bloque **no es un `SÍ`** sino una marca propia («acepto como alegado»).
**Dónde.** `FORMATO-DE-SALIDA.md` §1.2 y la plantilla de §1.7; `hechos-con-prueba/SKILL.md` Fase 5. Hoja de decisiones: salida líneas 99-188.
**Qué gana.** HECHO MEDIDO: las 35 fichas puras de «solo alegado» ocupan 662 líneas —18,9 de media— y la frase «Lo único detrás es el escrito de la parte demandante» aparece **42 veces literal**. En cada una, tres líneas dicen el mismo dato tres veces. 662 líneas bajan a ~120. La superficie de decisión pasa de 76 casillas a 41 más una marca de bloque.
**Qué cuesta.** **Aquí está la condición y no es negociable.** HECHO VERIFICADO (R-8): la hoja de decisiones actual **no tiene columna de cita ni de página**, y su «Enunciado (una línea)» es prosa del modelo. Comprimir sin añadir la cita convierte esto en aprobar 45 frases escritas por el modelo sin ver el texto de origen — que es exactamente la garantía que el producto vende. Y una marca de bloque que se registre como `SÍ` deja a `redactar-escrito` sin poder distinguir aprobado-como-alegado de aprobado-como-probado.
**Qué garantía toca.** «Proponer, nunca decidir», en su borde. Solo se sostiene con la cita en el renglón, la marca propia, las 76 casillas individuales conservadas, y un encabezado de bloque que diga con todas las letras que esos descansan en la palabra de una sola parte.
**Esfuerzo.** MEDIO. **Veredicto: DUDOSA, entra condicionada a R-8. Cuenta como UNA de las cinco de composición. Su argumento de venta original —«esto es lo que hoy bloquea `redactar-escrito`»— es falso (R-1) y no debe usarse para justificarla.**

---

### M-10 · El lote de despliegue
**Qué.** (a) Ejecutar el camino de instalación completo una vez, en una máquina que no sea la del dueño, antes de sentarse con ella; (b) publicar un repositorio **dedicado al plugin** y nada más; (c) una carpeta plantilla que ella duplique para abrir un caso; (d) el cuadro «qué puede renombrar y qué no» en su guía, más la cláusula de degradación en los cinco métodos que no la tienen; (e) borrar o marcar OBSOLETO `docs/discovery/guia-carpetas-para-la-abogada.md`; (f) corregir el README §5, que contradice a la decisión A-2 del diseño.
**Dónde.** `plugins/despacho/README.md` §3-§5 y §9; raíz del repositorio; `GUIA-PARA-LA-ABOGADA.md` §2; los cinco `SKILL.md`.
**Qué gana.** HECHO VERIFICADO: `git remote -v` vacío, `installed_plugins.json` = `{}`. **El mecanismo que tiene que llevar el producto a su máquina es la única pieza del sistema con cero ejecuciones**, y seis filas de la tabla de comprobaciones del README son suposiciones que se resuelven en un intento. HECHO MEDIDO: `git ls-files` da 216 archivos, de los cuales **206 no son el plugin**; `docs/` pesa 4,4 MB contra 273 KB de `plugins/`. Publicando este repositorio, en su disco aterrizan el informe de inspección, la revisión arquitectónica y una tabla donde su propia disponibilidad figura como dependencia operativa.
**Qué cuesta.** Una tarde, una cuenta de GitHub y un segundo repositorio que mantener. El riesgo de descubrir que algo no funciona es el motivo para hacerlo ahora y no delante de ella.
**Qué garantía toca.** Ninguna. Refuerza «cero jerga» por vía posicional: el vocabulario técnico que no está en su disco no le puede llegar.
**Esfuerzo.** BAJO (a, c, d, e, f) / MEDIO (b). **Veredicto: las diez propuestas de despliegue SOSTIENEN. Es la única evaluación construida sobre comprobaciones y no sobre estimaciones.**

---

### M-11 · Una sola lista «Lo que falta», con a quién pedírselo
**Qué.** Los cuatro comandos que hoy producen su lista escriben en un único `2-Borradores/Lo que falta - <caso>.md`, en modo **añadir**, cada entrada con su etiqueta de origen y el formato del inventario: qué es, quién lo menciona y dónde, y **a quién pedírselo**. El archivo no se depura nunca solo.
**Dónde.** `hechos-con-prueba/FORMATO-DE-SALIDA.md` §5; `cronologia/SKILL.md` §5.2; `inventario-de-anexos/SKILL.md` §5; cierre de `redactar-escrito`; consumidor en `estado-del-caso` §4-§5.
**Qué gana.** HECHO MEDIDO: la misma lista sale **cuatro veces en cuatro archivos y tres formatos**, con 13, 9/13, 14 y 7 entradas que no coinciden entre sí, y **solo una dice a quién pedir cada cosa**. El video de la audiencia del 14/10/2025 aparece cuatro veces; el acta 0128-2025, otras cuatro. ~130 líneas pasan a ~40, y ella sale con **una** llamada a la Comisaría de Guarne pidiendo cuatro cosas, en lugar de con cuatro listas que hay que cruzar a mano. Es la única parte del día que se convierte en trabajo ejecutable.
**Qué cuesta.** Rompe la simetría con «nunca se sobrescribe»: hay que fijar que se añade un bloque por pasada, con fecha y comando, y que nada anterior se toca. **RIESGO:** si el archivo se depurase solo cuando algo aparece, el sistema estaría afirmando que ya llegó. Lo tacha ella, o lo tacha la pasada siguiente diciendo dónde lo encontró.
**Qué garantía toca.** «No encontrado ≠ no existe» queda intacta: el texto de cada entrada no cambia, se deja de repetir.
**Esfuerzo.** MEDIO. **Veredicto: SOSTIENE. Pero es una forma suave de «apoyarse en derivados»: cuenta contra la regla de composición si en la misma versión entra M-9 o M-12.**

---

### M-12 · Mapa del material, escrito una vez por caso
**Qué.** Un `2-Borradores/Mapa del material - <fecha>.md` con la extracción literal página a página, qué páginas traen texto y cuáles no, con recuento de caracteres, tamaño y fecha de cada PDF. Lo produce quien primero abra el expediente; los demás lo leen, **comparan el listado de `1-Documentos recibidos/` contra el que el mapa registra, y si difieren lo rehacen**. Toda cita sigue anclada a la página del PDF, nunca a una línea del mapa.
**Dónde.** Fase 1 de los seis. Decisión de arnés, no de un comando.
**Qué gana.** HECHO MEDIDO: los mismos dos PDF y las mismas 25 páginas ilegibles se derivaron **cuatro veces el mismo día sobre la misma carpeta**, enumerando los mismos números de página. Es la duplicación más cara del arnés y la más mecánica de eliminar. SUPUESTO: −20 a −35 % en cada comando posterior al primero.
**Qué cuesta.** **RIESGO, y es el mayor del plan.** Punto único de fallo: si la extracción sale mal, los seis salen mal a la vez **y de forma coherente**, que es la peor manera de estar equivocado. Y retira el detector cruzado: que los cuatro comandos coincidieran hoy en las 25 páginas fue una **medición**, no redundancia; presentar como beneficio que «ya no puedan discrepar» es desactivar el único control cruzado del arnés.
**Qué garantía toca.** «No inventar» solo se conserva si (i) el mapa contiene extracción literal y nunca una ficha, un enunciado ni una interpretación — ese es exactamente el límite; (ii) la comprobación de vigencia falla hacia el lado seguro: ante cualquier duda, se re-extrae; (iii) el mapa se encabeza como propuesta, no como hecho verificado del expediente; (iv) toda salida construida sobre él dice de qué fecha es.
**Esfuerzo.** ALTO. **Veredicto: DUDOSA condicionada. Es la mayor palanca estructural y la que más control retira. Cuenta como UNA de las cinco de composición. Entra sola, en su propia versión, con el fixture antes y después.**

---

### Lo que NO entra, y por qué

| Propuesta | Veredicto | Motivo |
|---|---|---|
| **Verificación de anclajes dirigida** (100 % → ~10 %) | **RECHAZADA** | Dominada por M-4: mismo ahorro, cobertura entera, más detectora (R-2). Y reutiliza el criterio de la Fase 6.4 como el permiso que su propio autor prohíbe: *«el orden es una propuesta… Esta lista no es un permiso para no mirar lo demás»* (`SKILL.md:192`). |
| **Marca por rango** (aprobar H-01 a H-25 en una línea) | **RECHAZADA** | Paga con la garantía un tapón que no existe (R-1). Permite aprobar sin leer, y la fricción de las 76 casillas estaba haciendo trabajo real. |
| **OCR de las 25 páginas** | **RECHAZADA por ahora** | El activo del inventario son las discordancias: *dos cédulas para la misma apoderada* (1.034.959.525 / 1.094.959.625), *«Kteren.65» frente a «kterin.65»*. **Un dígito mal transcrito por OCR es indistinguible de una discordancia genuina.** Un motor de OCR alimentando un detector de discordancias es una fábrica de discrepancias falsas. Si algún día entra: texto OCR nunca alimenta el §4 de discordancias, y toda cita OCR va marcada e inverificable hasta que ella mire la página. |
| **Recortar las seis autoevaluaciones** | **RECHAZADAS hasta M-1** | La propuesta más repetida del corpus apunta directamente a la maquinaria que produjo el cero fabricaciones, sin un solo dato de qué pregunta atrapó qué. |
| **Recortar el ejemplo relleno** (223 → 50 líneas) | **RECHAZADA** | La salida real reprodujo su estructura entera. Recortar 4 de 6 casos de contraste para ahorrar el token más cacheable del sistema es el peor cambio riesgo/beneficio del corpus. Se sostiene la otra mitad: borrar el esqueleto de `SKILL.md:196-229`, que sí diverge de la plantilla real. |
| **Escribir en `1-Documentos recibidos/`** | **RECHAZADA** | Innecesaria. La carpeta quedó byte-idéntica; la extracción vivió fuera. Los tres problemas reales (nadie crea la carpeta, nadie sabe a quién representa, no hay ficha de entrada) se resuelven sin tocar la regla 5. |
| **Núcleo común para el bloque anti-inyección** | **RECHAZADA** | Moverlo a un archivo cuya ausencia falle en silencio es lo contrario de lo que esa regla necesita. La única frase que sí justifica un archivo común es la del derecho ajeno (§7, DP-1). |
| **Recortar la hoja de decisiones a 41 filas** | **RECHAZADA** | Choca con M-9: la hoja es la superficie de trabajo de ella y se queda con las 76 filas. Lo que hay que hacerle es **añadirle** cita y página. |

---

## §4 — Lo que falta construir

Tres huecos. Los tres son la razón de que el día de hoy empiece fuera del producto y termine sin nada presentable.

### 4.1 El comando que crea la oficina y el caso

**HECHO VERIFICADO:** ninguna de las seis skills nombra `Despacho/`, `Oficina/` ni `Casos/`; **ninguna crea carpetas**. El diseño dice que «el Core crea el esqueleto de cada caso nuevo» y el Core no existe. Hoy funciona porque el dueño montó a mano la carpeta de el caso de familia.

Peor, hay una pescadilla: la guía presenta `0-Estado del caso (no editar).txt` como una de las cuatro cosas que debe haber, pero ese archivo solo aparece **después** de correr `/estado-del-caso`. Una carpeta recién hecha nunca tiene la forma que la guía dibuja.

| Opción | Coste | Riesgo |
|---|---|---|
| **Carpeta plantilla** que el dueño deja en el Escritorio y ella duplica | ninguno: no añade código | ninguno; se explica en una frase |
| `/abrir-caso` como séptimo comando | un método más que mantener | primer comando que crea estructura en su disco; debe enseñar la ruta y esperar el sí |

**Recomendación: la plantilla.** Resuelve el caso dos hoy y sin riesgo. El comando puede venir después, y **debe crear `2-`, `3-` y el archivo de estado sin tocar `1-`** — la regla 5 no hay que reescribirla para esto.

### 4.2 La ingesta de documentos

**El agujero que nadie tenía en la lista.** HECHO VERIFICADO hoy: `1-Documentos recibidos/` contiene `Demanda.pdf` y `Anexos documentales.pdf`. Las salidas citan como fuente `Demanda - custodia visitas y alimentos.txt` y `Anexos documentales.txt`. **Alguien extrajo el texto a mano y ese paso no está en ninguna parte del producto.**

**RIESGO:** si ella va a comprobar una cita, no encuentra el archivo que la salida nombra. Es lo más parecido a una cita fantasma que produjo la corrida — a nivel de archivo en vez de página. La corrección inmediata es de una línea y va con M-10(d): **la cabecera nombra el archivo tal como está en la carpeta; que se trabajó sobre un texto extraído se dice aparte.** La ingesta propiamente dicha es M-12, con sus condiciones.

Y hace falta una **ficha de entrada** por caso: por archivo, nombre, tamaño, páginas, si tiene capa de texto y cuáles no, y la fecha en que entró. Sin ella, las tres reglas de segunda pasada que ya existen (`cronologia:246`, `FORMATO §1.6`, `inventario:19`) no pueden saber qué es nuevo sin releerlo todo — es decir, **cada documento nuevo cuesta otra vez la pasada entera y otra vez las dos horas de marcado.**

### 4.3 La consolidación de lo que falta

Es M-11. Se subraya aquí porque es lo único de todo el día que se convierte en trabajo ejecutable: cuatro listas inertes contra una llamada de teléfono.

### 4.4 Dos huecos menores, ambos con daño real

- **Arrastre de marcas entre pasadas.** La condición propuesta era «etiqueta y enunciado sin cambios» — **el estado no está en la condición**. Cuando llegue el acta completa, un hecho que ella aprobó como «sólo alegado, inofensivo» vuelve con su `SÍ` puesto siendo ya «contradicho». **El arrastre debe exigir estado idéntico, o no arrastrar.** Y debe mostrarse siempre como arrastrado y ser revocable con una línea.
- **La aprobación parcial no está definida.** Una ficha en blanco dentro de un archivo `- REVISADO` no es SÍ, ni NO, ni A MEDIAS, y `redactar-escrito` solo sabe leer esas tres. Hay que cerrarlo hacia el lado seguro: **en blanco = no aprobada**, nunca «probablemente sí», y el cierre la lista bajo «material aprobado que no se usó — motivo: sin marcar».

---

## §5 — Cómo se mide el resultado

**Sin medición antes y después, esto es opinión.** El mismo caso sirve de banco, y además ya existe un banco escrito que nadie usó.

### 5.1 El banco que ya existe y nadie mencionó

**HECHO VERIFICADO:** `docs/skills-support/evals/` — 678 líneas, seis fixtures, protocolo con truth set bajo custodia, y el caso adversarial exacto que hace falta (instrucción maliciosa embebida, material irrelevante, revisión obsoleta). Nueve evaluaciones y ~65 propuestas sobre la única propiedad demostrada del producto, **cero menciones del banco**. Es la omisión mayor del lote.

**Reserva honesta:** el fixture es pequeño (6 evidencias) y no detecta fallos que solo aparecen a escala. Hace falta además un caso grande **con una cita fantasma sembrada a propósito**. Hoy no existe ninguna prueba capaz de fallar.

### 5.2 Baseline del 2026-08-26 y umbrales

| Métrica | Baseline | Fuente | Umbral tras cada cambio |
|---|---:|---|---|
| Contenido atribuido a páginas ilegibles | **0** | verificación exhaustiva | **0. Innegociable.** |
| Páginas ilegibles declaradas una por una | **25 / 25** | idem | 25 / 25 |
| Fragmentos citados contrastados | **647** | idem | sin regresión |
| Anclajes verificados / errores | **239 / 1** | idem | ≤ 1, **y saber cuál era** |
| Derecho sustantivo en voz propia | **0** según el informe · **1** según la evaluación | ver 5.3 | 0, con criterio unificado |
| Cálculo de días · escrituras fuera de `2-Borradores/` | **0 · 0** | idem | 0 · 0 |
| `1-Documentos recibidos/` tras la pasada | **byte-idéntico** | idem | byte-idéntico |
| Turnos por comando | 16 / 30 / 37 / 97 | tabla de coste | **falta etiquetar dos filas** |
| Salida por comando | 19 / 48 / 64 / 76 KB | idem | |
| Decisiones que se le piden a ella | **76** | salida | |
| Anclajes corregidos por la Fase 6.1 | **desconocido** | — | **M-1(c) lo hace medible** |
| Preguntas de autoevaluación que dispararon | **desconocido** | — | **M-1(d) lo hace medible** |

### 5.3 Una contradicción del baseline que hay que resolver antes de usarlo

El informe declara **0 derecho sustantivo propio** tras una verificación exhaustiva. La evaluación de `hechos-con-prueba` encontró **1**, y lo verifiqué: salida línea 2121, *«es la pieza del requisito de procedibilidad que sí está»*, en voz propia del método y no en cita.

**POR VERIFICAR:** o la comprobación exhaustiva no cubrió esa dimensión, o las dos partes no entienden lo mismo por «derecho sustantivo». Cualquiera de las dos respuestas invalida el uso de ese 0 como baseline. **Hay que fijar el criterio por escrito y volver a contar** antes de que ese número sirva para comparar nada.

### 5.4 Protocolo por cambio

1. Correr el fixture del banco **antes**.
2. Aplicar **un** cambio — y como máximo **una** de las cinco de composición.
3. Correr el fixture **después**, más el caso de familia completo.
4. Registrar las trece filas de 5.2. Si cualquiera de las cuatro primeras se mueve, **el cambio se revierte**, no se discute.
5. Guardar versión de skill, fixture, prompt y salida. El baseline se conserva limpio.

---

## §6 — El orden de trabajo

### Fase 0 — Medir (antes de tocar una línea del método)
**M-1** completo. **Desbloquea:** decidir si veinte propuestas de recorte valen algo (b); autorizar o enterrar las seis de autoevaluación (d); saber si la Fase 6.1 se puede tocar algún día (c); y contestar dos preguntas de dos evaluaciones (a). **Sin esto, todo §2 es aritmética sobre supuestos.**
Y en paralelo, sin riesgo: **5.3** — fijar el criterio de «derecho sustantivo» y recontar.

### Fase 1 — Que llegue, y que no castigue a quien trabaja
**M-2**, **M-10** (a, c, d, e, f), y la corrección de cabecera de 4.2.
**Desbloquea:** que el producto exista fuera de la máquina del dueño; que el caso dos lo pueda abrir ella; que las dos horas de marcado no se pierdan por una extensión oculta; que seis suposiciones del README pasen a ser hechos.
**Ninguno toca el método. Ninguno gasta garantía.**

### Fase 2 — Los dos cambios que de verdad mueven la aguja
**M-3** y **M-4**. Fixture antes y después.
**Desbloquea:** el flujo deja de tener un camino que siempre falla caro (M-3); el comando caro deja de recorrer el material 315 veces donde caben 28 (M-4). Es todo el ahorro estructural que se puede obtener sin gastar un gramo de garantía.

### Fase 3 — La salida, sin tocar la garantía
**M-5**, **M-6**, **M-7**. Fixture antes y después.
**Desbloquea:** que la única promesa de producto terminado del arnés (la tabla del inventario) sea cierta; que la revisión deje de devolver más texto del que ahorra; que tres reglas duras dejen de estar rotas.

### Fase 4 — Las notas de ella
**M-8**. **Desbloquea:** que el archivo de estado pueda reescribirse sin que un texto suyo pase por el modelo. Prerrequisito de cualquier trabajo futuro sobre `0-Estado del caso`.

### Fase 5 — Composición, de una en una
**M-11**, y solo después **M-9** o **M-12**, nunca las dos juntas, cada una en su propia versión con fixture antes y después.
**Desbloquea:** M-11, el único trabajo ejecutable del día. M-9, bajar la superficie de decisión de 76 a 41 — **condicionada a R-8**. M-12, la ingesta única — **el mayor riesgo del plan**.

### Fase 6 — Lo que no se hace todavía
Ingesta con OCR, verificación dirigida, marca por rango, recorte de autoevaluaciones: **ninguna entra hasta que exista una prueba capaz de fallar**, es decir, hasta que 5.1 tenga el caso grande con la cita fantasma sembrada.

---

## §7 — Decisiones que solo puede tomar el dueño

| # | Decisión | Qué depende de ella | Recomendación |
|---|---|---|---|
| **DP-1** | **¿La salida puede contener el derecho que el documento invoca, transcrito y marcado como ajeno?** Hoy `revisar-documento:15` y su autoevaluación 9 lo prohíben en términos absolutos, y la corrida se saltó la prohibición por su cuenta inventándose una marca. Es la única regla del corpus que se contradice consigo misma. | La única justificación real de un archivo común, y la conducta de `revisar-documento` ante el apartado de normas de cualquier demanda. | **Sí, con una frase única y literal:** *«el método no contiene derecho; la salida puede contener derecho ajeno, entrecomillado, con página y marcado como transcripción».* Una regla contradictoria empuja a la salida fácil, que es omitir. |
| **DP-2** | **Ante texto roto por la extracción, ¿se repara en silencio o se transcribe tal cual y se anota?** Dos comandos resolvieron al revés en la misma corrida (`«31 y 1 de enero»` frente a `«31y 1 de enero» [así]`). El informe lo dejó abierto y las nueve evaluaciones lo ignoraron. | En un producto cuya promesa es la cita literal, **la reparación silenciosa es la puerta exacta por la que entra la primera fabricación**. | **Transcribir y anotar, siempre.** Y escribirlo una vez, en un solo sitio. Ya hay precedente bueno: conservar «MUN OZ» para que la cita se pueda buscar en el texto que ella tiene delante. |
| **DP-3** | **¿Se acepta la decisión en bloque de M-9?** ¿Le sirven a ella 45 hechos como renglón de tabla con cita y página, o cada uno necesita su ficha? | El 37 % de la salida y la diferencia entre ~35 minutos y ~2 horas de su jornada. | No la puede tomar nadie más que ella. **Se pregunta enseñando un renglón de muestra con la cita dentro**, no en abstracto. |
| **DP-4** | **¿Entra M-12, el mapa compartido?** | La mayor palanca de coste del arnés, y la retirada del único detector cruzado que hoy existe. | **Solo después de las fases 1-4, sola, y con las cuatro condiciones de §3 escritas en el método.** Si no se van a escribir esas condiciones, no entra. |
| **DP-5** | **¿Cuántos comandos debe haber?** Cuatro derivan el mismo mapa; cinco propuestas del corpus parchean eso con una caché. **Nadie hizo la pregunta previa:** ¿hacen falta cuatro puertas de entrada, o una que produce el mapa y tres vistas sobre él? | Toda la arquitectura del arnés. Es la pregunta que hay debajo de M-12. | **Plantearla antes de construir M-12**, no después. |
| **DP-6** | **¿Repositorio público o privado?** | Con privado hay que verificar antes cómo se autentica el anfitrión contra GitHub desde su máquina — marcado bloqueante en el README — y eso no se prueba delante de ella. | Con **repositorio dedicado al plugin** (M-10b) la pregunta casi desaparece: público, sin que nadie tenga que pensarlo dos veces. |
| **DP-7** | **¿Se acepta que sea ella quien pulse Update?** La decisión A-2 del diseño («la actualización la dispara el dueño») quedó revertida por el anfitrión, sin registrar. | Si se quiere volver atrás, el modelo de mercado no lo permite: hay que decidirlo a sabiendas. | **Aceptarlo y anotarlo**, junto con las cuatro piezas de ingeniería que el cambio de anfitrión regaló (lanzador, ACL, cuenta aparte, manifest) y que hoy siguen figurando como trabajo pendiente. |
| **DP-8** | **El nivel `Casos/`: se instaura ahora o se renuncia por escrito.** El árbol real es `Despacho/Familia/<caso>/`; el diseño preveía tres o cuatro niveles. | Con un caso, mover cuesta cero. Con cuarenta, no. | Decidirlo ahora, en cualquiera de los dos sentidos, **pero por escrito**. La renuncia por omisión es la única opción mala. |

### Preguntas que hay que hacerle a ella, y que ningún evaluador puede contestar

1. **¿A quién representa en el caso de familia?** Todo el trabajo del día está esperando un dato de una línea. Si representa a la madre, los hechos que habría que redactar **no están en esta carpeta**.
2. **¿Tiene las extensiones de archivo visibles en su Explorador?** Decide si M-2 es teórico o va a fallar el primer día. Se comprueba mirando su pantalla, en diez segundos.
3. **¿`.md` abre con doble clic en su máquina?** El archivo más caro del sistema —las 76 fichas— es `.md`. Si le sale «¿con qué desea abrir este archivo?», el paso más caro empieza con un obstáculo.
4. **¿Cuánto está dispuesta a esperar por un comando antes de darlo por colgado?** Fija si la acotación es un extra o el modo normal.
5. **¿Cuál de los dos abre primero al llegar un caso: la cronología de 202 líneas o los hechos de 2.156?** Si es la cronología, el orden de producción está al revés.

---

## Veredicto final, sin adornos

**Este plan no demuestra que el producto sea rentable, y hoy nadie puede demostrarlo en ninguna dirección.** La razón es §2.2: los logs no separan lectura de caché de entrada nueva, así que ni siquiera se sabe qué parte de los ~3 M facturables pagó el método. Cualquier promesa de ahorro que se escriba antes de M-1 —incluida cualquiera de las de este documento— es aritmética sobre supuestos.

Lo que sí se puede afirmar:

- **El plan hace el producto usable**, que es un problema distinto y anterior a la rentabilidad. Hoy el camino de instalación tiene cero ejecuciones, el día empieza en el Explorador, el flujo tiene un camino que siempre falla caro, y las dos horas de marcado pueden perderse por una extensión oculta. Las fases 0 a 2 arreglan eso y no gastan garantía.
- **El plan protege lo único demostrado.** Ocho de las propuestas más aplaudidas del corpus salen rechazadas o condicionadas precisamente por eso.
- **El plan no cambia el orden de magnitud del coste.** M-4 y M-3 quizá bajen el comando caro a la mitad. Los dos verdaderos motores del gasto —4.000 líneas de salida sobre 31 páginas legibles, y 76 casillas de trabajo humano— solo se mueven con el conjunto que la regla de composición limita a **uno por versión**. Llegar ahí, si se llega, son cuatro o cinco versiones con medición entre cada una.

Y una advertencia de escala que nadie del corpus midió: **RIESGO.** Todo lo anterior sale de un caso de 56 páginas con 14 legibles. El coste crece con los turnos y los turnos crecen con el material. Un expediente de 300 páginas legibles no cuesta cinco veces más: cuesta más que eso, porque cada turno rearrastra todo lo acumulado. **Nada de lo medido hoy autoriza a decir que este arnés funciona en un caso grande.** Esa es la siguiente medición que hace falta, y no está en ninguna de las nueve evaluaciones.
