# SPEC-04 — «Dicho por usted, no documentado en la carpeta»

**Estado:** ejecutada · **Cierra:** `P-05` · `P-06` · grupo `G6` · **Familia:** defecto

---

## 1. Qué problema cierra

Salió de un pase real, no de una revisión de escritorio. El registro del pase de Salento lo anotó dos veces:

| Ítem | Qué pasó |
|---|---|
| `P-05` | *«Sin `estado-del-caso` no hay dónde poner lo que el usuario dice y la carpeta no registra.»* **Hubo que inventar un bloque «DICHO POR USTED, NO DOCUMENTADO EN LA CARPETA» sobre la marcha.** El formato del `SKILL.md` no lo prevé |
| `P-06` | *«`cronologia` no tiene grado para "lo dijo el usuario en la conversación".»* El mismo agujero, en otra salida |

**Verificado contra el código el 2026-09-05:** ni `cronologia` ni `estado-del-caso` mencionan la conversación como origen de nada. `grep` de «conversación» en los dos `SKILL.md` no devuelve **ninguna** línea.

### Y la parte que hace que esto no sea cosmético

**`redactar-escrito` ya tiene la figura**, en su tabla de fuentes, desde antes:

> | **Lo que ella dijo** | Te lo dictó en la conversación | *"Lo dijo usted el «fecha»"*, textual |

Así que el producto **admite esa fuente en el comando que firma con su nombre, y no tiene dónde ponerla en los dos comandos que la producen**. Lo que ocurre entonces, y ocurrió, es una de estas dos, y las dos son malas:

- **Se pierde.** Ella dice *«el acta de la inspección se la llevó el otro despacho»*, la carpeta no lo registra, y a la salida no llega. La pasada siguiente vuelve a listarlo como ausencia inexplicada.
- **Se cuela disfrazada.** Entra en la línea de tiempo como una fecha más, o en «qué no está en la carpeta» como si el papel lo dijera. **Y esa es la peor**: una fecha que ella recordó de memoria, sentada en una lectura de carpeta, se lee después idéntica a una que salió de un acta.

> **La distinción de fondo, y por eso hay una regla y no un renglón más:** lo que ella dice en la conversación **es información buena y es la única que no deja rastro comprobable**. Una fecha referida en una entrevista se puede volver a comprobar: la transcripción está en la carpeta. Lo que dijo en el chat **no está en ninguna parte** — ni para la pasada siguiente, ni para quien lea el expediente, ni para ella dentro de tres semanas.

## 2. Comportamiento observable

1. Si durante la conversación ella aporta un dato que la carpeta no registra, **aparece en la salida**, en un bloque propio, con sus palabras y la fecha en que lo dijo.
2. Ese bloque **no se mezcla** con lo que sale de los documentos: no entra en la línea de tiempo, no lleva grado de certeza y no entra en los conteos.
3. Cada entrada dice **qué tendría que aparecer en la carpeta** para dejar de estar ahí.
4. Si ella no dijo nada, el bloque **dice que está vacío** en vez de desaparecer.
5. Nada de eso se guarda solo en `0-Estado del caso`: si quiere que persista, **lo pega ella** bajo `NOTAS SUYAS`.

## 3. Reglas duras

| # | Regla | De dónde sale |
|---|---|---|
| R-1 | **Solo entra lo que dijo ella**, en esta conversación. No lo que dice un documento, no lo que se dedujo, no lo que «se entiende» | ADR-005 |
| R-2 | **En sus palabras, no en las tuyas.** Se transcribe lo que dijo, no un resumen mejorado de lo que dijo | `redactar-escrito` §2 — *«textual»* |
| R-3 | **No se convierte en evento, ni en hecho, ni en ausencia del expediente.** Fuera de la tabla, fuera de los grados, fuera de los conteos | `P-06` · `cronologia` §3 |
| R-4 | **No se inventa un sexto grado de certeza.** Los cinco son vocabulario fijo, y el propio §3 manda decirlo en el documento cuando algo no cabe, en vez de crear una palabra nueva | `cronologia` §3 · `EP-C10` — cuántos estados tiene una ficha |
| R-5 | **Cada entrada lleva qué la sacaría de ahí:** el documento que habría que conseguir | `H-15.3` · la lista de «lo que falta» |
| R-6 | **El bloque vacío se declara vacío.** Y **jamás se rellena** con algo que ella no dijo | `estado-del-caso` §5 |
| R-7 | **No se guarda en el archivo de estado por decisión del sistema.** Ese archivo dice lo que la carpeta dice; esto no salió de la carpeta | SPEC-06 · `estado-del-caso` §4 |

## 4. Qué NO hace

- **No añade un grado de certeza** a `cronologia`. Los cinco siguen siendo cinco.
- **No convierte lo que ella dice en prueba.** Que lo diga la abogada no lo documenta: lo **atribuye**.
- **No le pregunta cosas para llenar el bloque.** Recoge lo que ella aportó por su cuenta; el método no entrevista.
- **No lo escribe en `0-Estado del caso`.** Persistirlo es decisión suya (R-7).
- **No toca `redactar-escrito`**, que ya tiene la figura y la registra bien.

## 5. Cómo se sabe que quedó

| # | Observable | Cómo se comprueba | Resultado |
|---|---|---|---|
| O-1 | `cronologia` tiene una sección de salida propia para esto, **fuera** de la línea de tiempo | Se lee la plantilla del §6 | **Pasa** |
| O-2 | El conteo de `cronologia` los cuenta **aparte**, y dice que están fuera de la tabla | Se lee el bloque `CONTEO` | **Pasa** |
| O-3 | `cronologia` §3 explica **por qué no hay un sexto grado** | Se lee §3.6 | **Pasa** |
| O-4 | `estado-del-caso` tiene el bloque en su formato de salida, con su nombre exacto | Se lee §5 | **Pasa** |
| O-5 | Las dos autoevaluaciones preguntan si algo dicho en la conversación se coló como si saliera de un documento | Se leen los §8 | **Pasa** |
| O-6 | Ninguna de las dos escribe esas entradas en `0-Estado del caso` | Se lee §4 de `estado-del-caso` | **Pasa** |
| O-7 | Una pasada real en la que ella aporte un dato de viva voz | — | **Pendiente** |

## 6. Qué toca

| Archivo | Qué |
|---|---|
| `cronologia/SKILL.md` §3.6 | **Nuevo.** Por qué esto no es un sexto grado y dónde va |
| `cronologia/SKILL.md` §6 | Sección 6 de la plantilla, y el conteo pasa a 7 |
| `cronologia/SKILL.md` §8 | Una pregunta de autoevaluación |
| `estado-del-caso/SKILL.md` §5 | Bloque 6 del formato de salida |
| `estado-del-caso/SKILL.md` §4 | Que esto **no** entra en el archivo guardado, y por qué |
| `estado-del-caso/SKILL.md` §8 | Una pregunta de autoevaluación |

## 7. Qué queda fuera y por qué

- **`hechos-con-prueba`.** `G6` junta expresamente `estado-del-caso` y `cronologia` — *«los dos `SKILL.md`, que cambian a la vez»*—, y ahí la figura ya está resuelta por otra vía: una ficha cuyo único respaldo es el dicho de alguien **ya se marca como tal**. Meterle esta sección sería un segundo mecanismo para lo mismo.
- **Un archivo que acumule lo dicho a lo largo del caso.** Sería la lista única de «lo que falta» (`PM-M-11`, grupo `G4`), que es otro ítem y tiene su propio diseño. Cuando exista, este bloque es una de sus entradas.
- **Preguntarle activamente.** Un método que entrevista es otro producto, y ninguno de los once comandos lo hace.
- **Distinguir si lo que ella dice lo sabe de primera mano o se lo contaron.** Es una distinción real y valiosa; también es una pregunta que habría que hacerle. Queda para cuando se decida si el producto pregunta.
