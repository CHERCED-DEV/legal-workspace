# SPEC-08 — El índice de las salidas: qué produjo este sistema y cuál aprobó ella

**Estado:** ejecutada · **Cierra:** `P-07` · grupo `G37` · **Familia:** defecto

---

## 1. Qué problema cierra

`P-07`, del registro del pase real: **«Nada consolida las salidas. Doce archivos y ningún índice.»** Y su consecuencia, anotada en el mismo renglón: *«se escribió a mano un análisis forense que hace de documento de entrada»*.

Doce archivos en `2-Borradores/` después de una pasada, y para saber qué hay ella tiene que abrirlos uno por uno. **Verificado contra el código el 2026-09-05:** `grep` de «índice» en los once `SKILL.md` no devuelve **ninguna** línea.

### Por qué el sitio de esto es `estado-del-caso` y no un comando nuevo

`estado-del-caso` **ya recorre las tres carpetas y ya lista todo lo que hay**. Lo que no hace es distinguir. Hoy, en su bloque «QUÉ HAY», un archivo de hechos producido por el sistema y una carta que escribió ella aparecen en la misma lista, `Ella produjo (2-Borradores / 3-Para presentar)` — y **no es verdad que ella los produjera**.

Faltan, entonces, cuatro cosas que la carpeta sí permite decir:

| Qué falta | Por qué importa |
|---|---|
| **Cuál salida es del sistema y cuál es de ella** | Una propuesta del sistema y un escrito suyo no valen lo mismo, y hoy se leen igual |
| **Qué comando la produjo** | El nombre del archivo lo dice, y nadie lo lee: `Hechos - …`, `Cronologia - …`, `Inventario de anexos — …` |
| **Si lleva la marca de revisada** | Es la única distinción con consecuencias: sin ella, ningún otro comando la puede usar de fuente |
| **De qué pasada es cada una** | Con dos pasadas en la carpeta, saber cuál es de cuándo es la diferencia entre releerlo todo y no releer nada |

**Un comando nuevo para esto sería el duodécimo, y sobra:** el índice no es trabajo nuevo, es **la lectura que este comando ya hace, ordenada por una columna que hoy no mira**.

## 2. Comportamiento observable

1. En pantalla, las salidas del sistema **aparecen aparte** de lo que ella produjo, cada una con qué comando la hizo, de qué fecha es y **si lleva la marca de revisada**.
2. Ese mismo índice **queda guardado** en `0-Estado del caso (no editar).txt`: es lo que ella abre para saber qué hay, sin releer la carpeta.
3. Un archivo que no encaja en ninguna convención de nombre **se lista igual**, diciendo que no se pudo saber de dónde salió. **Nunca se le adivina un comando.**
4. El conteo dice cuántas salidas hay y cuántas están revisadas.
5. Si no hay ninguna, se dice: *«este sistema no ha producido nada en esta carpeta todavía»*.

## 3. Reglas duras

| # | Regla | De dónde sale |
|---|---|---|
| R-1 | **El nombre del archivo es una pista, no una prueba de origen.** Si no encaja, se dice que no se sabe. Adivinar el comando es inventar | `estado-del-caso` §2.1, distinción 3 |
| R-2 | **«Revisada» se decide con la regla de reconocimiento de la marca**, la de SPEC-05, y se escribe **el nombre exacto** del archivo que se contó como marcado | SPEC-05 · `H-12` |
| R-3 | **El índice no valora ni ordena por importancia.** Es un inventario, no una recomendación de qué leer primero | `estado-del-caso` §6 — no recomendar |
| R-4 | **Listar una salida no la convierte en fuente.** Sigue siendo trabajo del sistema: pista, nunca origen, salvo la marca | §2 de las seis skills |
| R-5 | **Una salida que no se pudo abrir se lista con su motivo**, como cualquier otro archivo | `estado-del-caso` §3, Fase 1 |
| R-6 | **El índice vive por encima de `NOTAS SUYAS`**, porque el sistema tiene que poder actualizarlo | SPEC-06, R-4 |

## 4. Qué NO hace

- **No es un comando nuevo.** Once siguen siendo once.
- **No abre las salidas para resumirlas.** Dice qué son por su nombre y su encabezado, como hace con cualquier archivo.
- **No dice cuál leer primero, ni cuál está mejor, ni cuál sobra.**
- **No borra, no mueve y no consolida archivos.** Consolidar es un índice, no una fusión.
- **No pone ni quita la marca de revisada.** Solo la lee.

## 5. Cómo se sabe que quedó

| # | Observable | Cómo se comprueba | Resultado |
|---|---|---|---|
| O-1 | El formato de salida §5 tiene las salidas del sistema **en su propia lista**, separada de lo que produjo ella | Se lee §5, bloque 2 | **Pasa** |
| O-2 | Cada línea prevé comando, fecha de la pasada y estado de revisión | Se lee la plantilla | **Pasa** |
| O-3 | La plantilla del archivo guardado (§4) trae la sección, **por encima de `NOTAS SUYAS`** | Se lee §4 | **Pasa** |
| O-4 | El `SKILL.md` trae la tabla de convenciones de nombre de los comandos que escriben | Se lee §3, Fase 2 | **Pasa** |
| O-5 | Está escrito que un nombre que no encaja se lista **sin adivinarle comando** | `grep` de la regla | **Pasa** |
| O-6 | El conteo incluye salidas y revisadas | Se lee el `CONTEO` | **Pasa** |
| O-7 | La autoevaluación pregunta por el índice | Se lee §8 | **Pasa** |
| O-8 | Una pasada real sobre una carpeta con varias salidas | — | **Pendiente** |

## 6. Qué toca

| Archivo | Qué |
|---|---|
| `estado-del-caso/SKILL.md` §3, Fase 2 | La tercera categoría pasa a cuatro: se separa «salida de este sistema» de «notas de trabajo», con la tabla de convenciones de nombre |
| `estado-del-caso/SKILL.md` §5 | La lista dentro del bloque 2, y el conteo |
| `estado-del-caso/SKILL.md` §4 | La sección en el archivo guardado |
| `estado-del-caso/SKILL.md` §8 | Una pregunta de autoevaluación |

## 7. Qué queda fuera y por qué

- **Un archivo índice aparte.** El archivo de estado ya es el documento de entrada de la carpeta; un segundo índice al lado sería **dos documentos que dicen lo mismo y derivan** — la enfermedad que este repositorio lleva documentada desde `BACKLOG-CONSOLIDADO` §0.2.
- **Resumir el contenido de cada salida.** Abrir doce archivos para resumirlos es justo el coste que el índice existe para ahorrar. Para eso está `/buscar-en-el-caso`.
- **Un orden de lectura recomendado.** Sería una recomendación, y este método no recomienda (R-3).
- **Detectar que dos salidas se contradicen.** Es cotejo entre documentos —grupo `G3`, `H-15.1`—, otro ítem, y hoy expresamente prohibido a este método.
- **Marcar salidas viejas como superadas.** «La salida envejece» es el grupo `G18` y tiene su propio diseño pendiente.
