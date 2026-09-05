# Pasada de escritorio sobre el caso-02: qué aguantó y qué se cayó

**Fecha:** 2026-09-05. **Qué es:** la primera vez que las specs escritas estos días se ejecutan contra un expediente, en vez de declararse ejecutadas.

> **Y lo que no es, dicho primero.** El expediente es **sintético y lo construí yo, que escribí las reglas**. Está sesgado hacia esas reglas por construcción: **lo que un caso real trae y este no es lo que a nadie se le ocurrió poner**. Esto no sustituye la pasada real, no mide veracidad y no dice que el producto sirva. Dice una cosa más pequeña y que no se tenía: **si las reglas deciden cuando se les pone delante el caso que dicen manejar.**

---

## El resultado en una línea

**Cinco defectos, los cinco míos y los cinco de esta semana.** Ninguno se veía leyendo la spec. Aparecieron al poner las reglas a decidir sobre nombres de archivo concretos, sobre un expediente con dos partes, y —el quinto— **dentro del propio registro de esta pasada**, en el párrafo donde yo explicaba por qué las otras cosas fallaban por no comprobarse.

| # | Spec | Qué estaba mal |
|---|---|---|
| 1 | SPEC-05 | La regla se contradecía con su propio ejemplo: `(revisar)` no contiene «revisado» |
| 2 | SPEC-03 | La simetría autorizaba a valorar un requisito, que es hacer derecho |
| 3 | SPEC-04 | Lo que ella escribe bajo `NOTAS SUYAS` no contaba como suyo |
| 4 | SPEC-05 | «Pregunta cuál manda» **sin «y te detienes»** |
| 5 | — | **Mi propio registro**: dije dónde dispara la simetría sin ir a mirar |

---

## Defecto 1 — SPEC-05 se contradecía con su propio ejemplo

**Cómo apareció.** Traduje la regla de la marca a código para ver si decide. **Falló en la primera ejecución.**

**Qué decía la regla:**

> *«Si hay un archivo con «revisado» de cualquier otra forma —al principio del nombre, en medio, `(revisar)`— … se nombran y se pregunta»*

**«revisar» no contiene «revisado».** Son dos palabras distintas. La regla ofrecía como ejemplo un caso **que su propio enunciado no cubre**, así que un modelo aplicándola al pie —buscando «revisado»— **pasaría por encima de `Hechos - Salento (revisar).md` sin verlo**.

**Por qué importa más de lo que parece:** ese es exactamente el fallo silencioso que SPEC-05 existe para impedir —el comando que no ve el archivo y se calla—, **reproducido dentro de SPEC-05**, escrita el mismo día.

**Corregido:** la señal que se busca es **la raíz «revis»**, no la palabra, en los seis `SKILL.md`, y la regla explica por qué.

## Defecto 2 — La simetría de SPEC-03 ensanchaba lo que un método puede decir

**Cómo apareció.** Al aplicar `/estado-del-caso` al expediente. Los dos apoderados firman y **ninguno acredita su calidad** — la trampa 1, puesta para que dispare la simetría. Y al ir a escribirlo: **`estado-del-caso` no puede decirlo.** Que la acreditación se exija es una regla de derecho, y este método tiene prohibido contener derecho.

**Qué decía mi regla:**

> *«Toda carencia que señales de una parte —un documento que no acreditó, una afirmación sin respaldo, **un requisito que no consta**— se busca en las demás…»*

**«Un requisito que no consta» es una invitación a valorar un requisito**, es decir, a hacer derecho, en once métodos que lo tienen prohibido. Escribí una regla de imparcialidad que abría la puerta a la infracción más grave del producto.

**Corregido en los once:** la simetría alcanza a *«toda carencia que **este método ya pueda señalar**»*, con una advertencia explícita: *«esta regla no ensancha lo que puedes señalar: solo obliga a mirar a los dos lados de lo que ya señalabas»*.

> **Y la trampa 1 no se pierde por eso: cambia de sitio.** En `estado-del-caso` lo correcto es **no decirlo**, y que la simetría no dispare ahí no es un fallo: es la regla comportándose bien.

---

## Defecto 5 — Dije dónde dispara la simetría sin comprobarlo, y me equivoqué de comando

**Añadido el 2026-09-05, unas horas después, ejecutando `/inventario-de-anexos` contra el mismo expediente.**

El párrafo de arriba decía, en su primera versión, que quien hace visible la carencia *«es `inventario-de-anexos`, con «quién produjo el documento»»*. **Escrito sin comprobarlo. Es falso.**

`inventario-de-anexos` Fase 2 toma las afirmaciones que hay que sostener **de tres sitios y solo tres**: la hoja de hechos aprobada, el borrador del escrito, o lo que ella indique. **Ninguno es «lo que el propio material afirma».** Una firma de alguien que se presenta como apoderado, sin nada detrás, **no tiene entrada ahí tampoco**.

**Dónde sí dispara, comprobado esta vez:** en **`hechos-con-prueba`**. Su Fase 2 recoge afirmaciones de *«algo que alguien dice o que un documento consigna»* —el material mismo—, la Fase 3 las consolida en hechos candidatos, y la Fase 5 marca **sin apoyo** al que no tiene ninguna pieza detrás. Ese es el estado exacto de la afirmación «X actúa como apoderado», y ahí la simetría tiene de qué agarrarse.

**Y hacía falta algo más que saberlo: la regla no tenía anclaje.** Estaba escrita como principio general en el bloque de posición de los once, y **un principio sin punto de enganche es un principio que no dispara**. Se ancló en la fila «Sin apoyo» de la Fase 5 de `hechos-con-prueba`, con el caso real como ejemplo y con la distinción escrita al lado: *no estás diciendo que haga falta acreditar nada —eso es derecho— estás diciendo que una afirmación del material no tiene detrás ninguna pieza, aplicado a los dos lados en vez de a uno.*

**La cadena correcta, entonces, es de dos pasos y no de uno:** `hechos-con-prueba` lo hace visible y aplica la simetría → ella lo aprueba → `inventario-de-anexos` lo empareja con el documento ausente. Que sea una cadena y no un solo comando **es la razón por la que no se veía**.

---

## Defecto 4 — La regla decía «pregunta» y no decía «y te detienes»

**Encontrado ejecutando `/redactar-escrito`** —«el comando más peligroso del despacho»— contra el mismo expediente, que tiene **dos** archivos de hechos marcados a propósito.

La regla de SPEC-05 decía: *«no eliges. Los nombras los dos con su fecha y preguntas cuál manda.»* **Y ahí terminaba.**

**Compárese con el caso de cero marcados**, que sí está resuelto desde antes: *«Si no hay hechos aprobados, **dilo y detente** … — y esperas.»* Con cero hay una parada explícita. **Con dos había una orden de preguntar y ninguna de parar.**

**Por qué el fallo es más fácil aquí, y no al revés.** Con cero marcados **no hay sobre qué redactar** y la parada se impone sola. **Con dos hay dos archivos completos y utilizables delante**, y seguir es cómodo: un modelo con prisa pregunta, se contesta solo *«será el más reciente»* y sigue. Y entonces **ha elegido él cuál de las dos decisiones de ella vale** — que es exactamente lo que la marca existe para no decidir.

> **Y deja algo peor que no haber preguntado:** deja escrito en la salida que se consultó, así que quien la lea creerá que la elección la hizo ella.

**Corregido:** en el bloque §2 de las seis, *«se nombran, se pregunta **y se espera la respuesta**»*, con la razón al lado —*preguntar no es seguir*—; y en `redactar-escrito` e `inventario-de-anexos`, la parada dicha con las mismas palabras que la de «no hay hechos aprobados», porque es el mismo alto.

---

## Lo que aguantó

| Spec | Qué se ejercitó | Resultado |
|---|---|---|
| **SPEC-06** | La pasada entera sobre una copia del expediente: `--comprobar`, cabecera nueva de 1.912 bytes, copia previa, comprobación | **Las notas de ella volvieron idénticas byte a byte** — 296 bytes, con tildes, «comillas españolas», guiones largos y `¿`. La cabecera cambió. La copia quedó en `2-Borradores/` |
| **SPEC-06** | Que el programa no enseñe sus notas | No apareció ni una palabra suya en la salida: solo `5 renglones` |
| **SPEC-05** | `- REVISADO.md.md` · sin extensión · `(revisar)` · dos marcados | Los cuatro clasificados como manda la regla, **una vez corregida** |
| **SPEC-08** | El índice de salidas sobre cinco archivos producidos por el sistema | Se pudo escribir con comando, fecha y estado de revisión, **y el que no encaja se listó sin adivinarle comando** |
| **SPEC-05 + SPEC-08 juntas** | Dos archivos marcados en la misma carpeta | El índice **nombró los dos y devolvió la decisión**, en vez de elegir el más reciente |
| **SPEC-03** | La posición se dedujo de la carpeta —membrete de la inspección, «se constituye el despacho»— sin preguntar | La salida no dice «su clienta» en ninguna parte |

---

## Lo que sigue sin comprobarse, y no lo puede comprobar esto

- **Que un modelo aplique la prosa.** Aquí la apliqué yo leyéndola, que es el mejor caso posible: **conozco lo que quise decir**. Una pasada real la aplica quien no.
- **Veracidad.** No hay escaneados ni ocasión de fabricar sobre una página vacía. Eso es el caso-01 y sigue bloqueado en su material.
- **Que el bloque de SPEC-12 produzca cifras.** No se ejercitó: exige una pasada completa de un método, no la lectura de una carpeta.
- **Coste.** Nada de esto mide un turno.

## La conclusión, que es sobre cómo trabajar y no sobre estas dos correcciones

**Nueve specs se declararon ejecutadas leyéndolas. Dos estaban mal, y las dos se vieron en la primera hora de ponerlas a decidir.** No hay razón para creer que la proporción sea distinta en las otras siete: lo único que cambia es que a esas todavía no se les ha puesto nada delante.

**«Ejecutada» seguirá significando poco mientras signifique «escrita y releída».** Un expediente sintético lo mejora un peldaño y no más; el peldaño que falta es el mismo desde hace días, y no depende de mí.
