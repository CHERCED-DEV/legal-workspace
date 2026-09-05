# SPEC-13 — Abrir cada pieza una vez, no veintiuna

**Estado:** ejecutada · **Cierra:** `PM-M-4` · grupo `G24` · §2 ítem 8 del backlog · **Familia:** defecto

---

## 1. Qué problema cierra

`PM-M-4` es la única propuesta del corpus con este veredicto: ***«SOSTIENE — la mejor del corpus… Cheaper and stronger»***. Y su medición es concreta:

> El método escribe **dos bucles anidados**. Este caso pide **76 barridas y 239 aperturas donde caben 14 y 14** — solo hay 14 páginas legibles más la demanda. Con 647 citas sobre 31 páginas, **cada página se visitó unas 21 veces**.

El defecto está en dos frases, las dos del mismo tipo: **indexan por lo que se busca, no por dónde está**.

| Dónde | Qué dice | Qué produce |
|---|---|---|
| `hechos-con-prueba` Fase 4 | *«Para cada hecho candidato, **recorre el material**»* | Un barrido del material entero **por cada hecho** |
| `hechos-con-prueba` Fase 6.1 | *«abre cada anclaje que citaste, **uno por uno**»* | Una apertura **por cada cita**, aunque doce citas salgan de la misma página |
| `cronologia` Fases 2 y 6.2 | La misma forma | Lo mismo |

**Verificado contra el código el 2026-09-05, y con una corrección al propio ítem.** `PM-M-4` dice que la cadena está también en `inventario-de-anexos` Fases 1-4. **Ya no:** ese comando —y `inventario-de-bienes`— tienen desde hace tiempo la forma buena, con su nombre puesto (*«Fase 1 — el recorrido de captura: se lee una vez y se anota todo»*, *«Fase 5 — numerar, comprobar en bloque y entregar»*). **El defecto sigue vivo en dos de los cuatro**, no en los cuatro.

> **SEGUNDA CORRECCIÓN, del mismo 2026-09-05 y unas horas después: «dos de los cuatro» tampoco era la cuenta.** Al ejecutar `revision-de-rigor` contra el `caso-03` apareció que **el defecto seguía vivo en dos sitios más**, los dos en el paso de comprobación y no en el de captura, que es donde esta spec miró:
>
> | Dónde | Qué decía | Qué es |
> |---|---|---|
> | `revision-de-rigor` Fase 6.1 | *«Abre cada localizador que citaste, **uno por uno**»* | **El mismo defecto.** Su objeto es un expediente con varias piezas: es el bucle anidado completo, y esta spec no lo miró porque solo revisó los cuatro métodos que leen material |
> | `hechos-con-prueba` §9, pregunta 7 | *«¿comprobé, **uno por uno**, que cada fragmento citado dice lo que le atribuyo?»* | **Una contradicción dentro del mismo archivo.** Su Fase 6.1 dice *«en bloque y una sola vez, nunca por hecho»* y su autoevaluación preguntaba lo contrario. Una regla con dos redacciones, en el mismo fichero |
>
> **Los dos corregidos.** Y uno que **NO** se toca, y decir por qué es parte de la corrección: `revisar-documento` dice *«abre cada cita una por una»* y **ahí no es defecto** — su objeto es **una sola pieza**, así que abrir sus citas una por una no son dos bucles anidados sobre el material. La forma correcta depende de cuántas piezas hay, no de la palabra.
>
> **Es la quinta cuenta mal hecha del día**, y la primera que se le hace a una spec. Ninguna se encontró releyendo.

> **Y eso hace que esta spec no invente nada.** No hay que diseñar la forma nueva: **hay que portar la que ya está escrita y funcionando en dos comandos del mismo plugin**, con su vocabulario y sus pasos. Es la diferencia entre una reforma y una copia.

## 2. Comportamiento observable

1. Cada documento del caso **se abre una vez** en la fase de captura, y de una vez se anota todo lo que las fases siguientes van a necesitar.
2. Al comprobar, cada documento **se vuelve a abrir una sola vez**, y se contrastan de golpe **todas** las citas que dicen salir de él.
3. **La cobertura no baja: se comprueba lo mismo que antes, todo.** Lo que cambia es el orden en que se visita.
4. Lo que no se pudo comprobar **se sigue declarando**, igual que hoy.

## 3. Reglas duras

| # | Regla | De dónde sale |
|---|---|---|
| R-1 | **No se comprueba menos.** Toda cita que iba a comprobarse se comprueba; cambia el orden, no el conjunto | `PM-M-4` — «conserva la cobertura al 100 %» |
| R-2 | **La lista de comprobación se ordena por dónde está el dato** —archivo, y dentro de él página—, **nunca por etiqueta** de hecho o de evento | La forma que ya usan los dos inventarios |
| R-3 | **Esto no es un recorte y no cuenta como una de las cinco de composición.** No retira ningún control; `PLAN-DE-MEJORA` §1 limita a una por versión las propuestas que **retiran un control distinto**, y esta no retira ninguno | `PLAN-DE-MEJORA` §1 |
| R-4 | **Y refuerza la detección, que es la razón de fondo.** Ver de una vez las doce afirmaciones que dicen «Anexos, p. 23» contra la página 23 real **detecta la que sobra**; abrirlas de una en una, no | `PM-M-4` · `H-12`, la cita fantasma |
| R-5 | **La forma es la que ya existe en los dos inventarios**, no una variante nueva | ADR-014 invariante 6 · `EP-C06` |

## 4. Qué NO hace

- **No recorta ninguna fase, ninguna pregunta de autoevaluación ni ningún control.**
- **No autoriza «verificación dirigida»** —comprobar solo lo importante—. `PM-M-4` la domina expresamente: *«mismo ahorro, cobertura entera, más detectora»*.
- **No toca los dos inventarios**, que ya la tienen.
- **No promete un número.** El ahorro medido —76 barridas a 14— sale de un caso; **cuánto ahorra en el siguiente no lo sabe nadie hasta medirlo**, y ahora hay con qué (SPEC-12).

## 5. Cómo se sabe que quedó

| # | Observable | Cómo se comprueba | Resultado |
|---|---|---|---|
| O-1 | `hechos-con-prueba` Fase 4 indexa **por pieza** y no por hecho | Se lee la fase | **Pasa** |
| O-2 | `hechos-con-prueba` Fase 6.1 reúne, **ordena por archivo y página**, y recorre una vez | Se lee la fase | **Pasa** |
| O-3 | `cronologia` hace lo mismo en sus dos sitios | Se lee | **Pasa** |
| O-4 | En los dos está escrito que **la cobertura no baja** | `grep` | **Pasa** |
| O-5 | Los dos inventarios **no cambiaron** | `git diff` de sus fases: vacío | **Pasa** |
| O-6 | Una pasada real que mida aperturas antes y después | — | **Pendiente.** Y ahora hay instrumento (SPEC-12) |

## 6. Qué toca

| Archivo | Qué |
|---|---|
| `hechos-con-prueba/SKILL.md` Fase 4 | El barrido por hecho pasa a barrido por pieza |
| `hechos-con-prueba/SKILL.md` Fase 6.1 | La comprobación en bloque, con la forma de los inventarios |
| `cronologia/SKILL.md` Fase 2 y Fase 6.2 | Lo mismo |

## 7. Qué queda fuera y por qué

- **Medir el ahorro.** Necesita una pasada real antes y después. El instrumento existe desde SPEC-12 y **no ha producido una sola cifra**.
- **Las otras propuestas de coste del grupo `G24`** (`PM-M-3`, `PM-M-6`, `H-17`). Ninguna tiene el veredicto de esta, y varias **sí** retiran controles: van al bloque 2, después de instrumentar y de una en una.
- **La verificación dirigida.** Descartada por dominancia, arriba.
