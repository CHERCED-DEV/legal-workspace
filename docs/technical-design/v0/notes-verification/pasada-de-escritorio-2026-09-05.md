# Pasada de escritorio sobre el caso-02: qué aguantó y qué se cayó

**Fecha:** 2026-09-05. **Qué es:** la primera vez que las specs escritas estos días se ejecutan contra un expediente, en vez de declararse ejecutadas.

> **Y lo que no es, dicho primero.** El expediente es **sintético y lo construí yo, que escribí las reglas**. Está sesgado hacia esas reglas por construcción: **lo que un caso real trae y este no es lo que a nadie se le ocurrió poner**. Esto no sustituye la pasada real, no mide veracidad y no dice que el producto sirva. Dice una cosa más pequeña y que no se tenía: **si las reglas deciden cuando se les pone delante el caso que dicen manejar.**

---

## El resultado en una línea

**Nueve specs ejecutadas, dos defectos, los dos míos y los dos de esta semana.** Ninguno se veía leyendo la spec; los dos aparecieron al ponerla a decidir sobre nombres de archivo concretos y sobre un expediente con dos partes.

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

> **Y la trampa 1 no se pierde por eso: cambia de sitio.** Quien puede hacerla visible sin hacer derecho es `inventario-de-anexos`, con «quién produjo el documento» —fue lo que más valor produjo en el pase real—, y `revision-de-rigor`. En `estado-del-caso` lo correcto es **no decirlo**, y que la simetría no dispare ahí no es un fallo: es la regla comportándose bien.

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
