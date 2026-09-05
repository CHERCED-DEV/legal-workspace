# SPEC-03 — Cuando ella no representa a nadie: el método hablándole a quien decide

**Estado:** ejecutada en su primera mitad · **Cierra:** `P-02` · grupo `G7` · `PASE §6-4` · `PLAN §4-3` · **Familia:** defecto

---

## 1. Qué problema cierra

**La única usuaria real de este producto es autoridad**, no parte. Es inspectora: no defiende a nadie, **decide entre otros**. Y el arnés entero le habla como si tuviera un bando.

`P-02`, del pase real del 27/08: *«El contexto B no está diseñado. Los `SKILL.md` hablan de «la profesional», «su clienta», «el escrito que usted presenta».»* Consecuencia anotada el mismo día: **«Hubo que traducir el vocabulario en cada salida. Funcionó, pero a mano.»**

**Verificado contra el código el 2026-09-05.** El rastro es más pequeño de lo que el backlog sugiere, y está donde importa:

| Dónde | Cuántas | Qué son |
|---|---|---|
| `hechos-con-prueba` | 7 | Seis en ejemplos; **una es regla**: *«que alguien lo afirme —incluida tu propia clienta— no lo hace probado»* |
| `cronologia` | 3 | Los tres en ejemplos |
| `revisar-documento` | 1 | **Regla**: *«El documento se dirige a ella o a su clienta»* |
| `inventario-de-anexos` · `inventario-de-bienes` | «la propia interesada» | **No es esto**: ahí es una **categoría de quién produjo el documento**, y en contexto B sigue significando algo. No se toca |

> **Y por eso este ítem valía lo que decía, a diferencia de otros.** Nació de ejecutar el producto en un caso real, no de leer un documento sobre el producto. De los ítems verificados con ese origen, **cuatro de cuatro estaban vivos y exactos**. Este es el quinto.

### Lo que la traducción a mano cuesta, y no es la comodidad

Traducir «su clienta» a mano en cada salida es molesto. **Lo que no se ve es lo otro:** un método que presupone bando **orienta el trabajo hacia la ventaja de alguien**, y en manos de quien decide eso no es una molestia de redacción — es la máquina empujando en una dirección dentro de un expediente que ella tiene que resolver imparcialmente. La traducción a mano arregla las palabras y **no arregla la orientación**.

### La regla que el pase real ya probó, y que esta spec convierte en método

El pase del 27/08 anotó, entre lo que funcionó:

> **«La simetría obligatoria evitó el error más fácil del contexto B:** al plantear la falta de acreditación del apoderado de una parte, la misma carencia aparecía en la otra.»

**Eso se hizo a mano y funcionó.** No está escrito en ningún `SKILL.md`. Es la aportación central de esta spec: **cuando ella es autoridad, toda carencia que se señale de una parte se busca en las demás antes de entregarla**, y el resultado de esa búsqueda se dice — la haya o no.

## 2. Comportamiento observable

1. El método **sabe en qué posición está ella** antes de producir nada: parte —representa a alguien— o autoridad —decide entre otros—.
2. Si no puede saberlo por lo que ella dijo ni por lo que muestra la carpeta, **pregunta una vez y no adivina**.
3. En posición de autoridad, la salida **no dice «su clienta» ni nada equivalente** en ninguna parte.
4. En posición de autoridad, **ninguna carencia se señala de una sola parte** sin haberla buscado en las demás y decir qué se encontró.
5. En posición de autoridad, **nada se ordena ni se presenta por lo que le sirve a nadie**: no hay «esto le conviene», ni «lo más favorable», ni un orden por utilidad.
6. **Todo lo demás es idéntico en las dos posiciones**, y el método lo dice: mismas fuentes, mismas prohibiciones, mismo vocabulario de la ausencia, mismo «alegado no es acreditado».

## 3. Reglas duras

| # | Regla | De dónde sale |
|---|---|---|
| R-1 | **La posición no se adivina.** Se toma de lo que ella dijo, o de lo que la carpeta muestra; si no se puede, se pregunta una vez | ADR-005 · el mismo patrón que «no hay hechos aprobados» |
| R-2 | **Simetría obligatoria en posición de autoridad.** Una carencia señalada de una parte se busca en las demás y **el resultado se escribe, la haya o no** | **El pase real del 27/08**, donde funcionó |
| R-3 | **Ninguna salida se orienta a la ventaja de nadie** en posición de autoridad: ni en lo que se incluye, ni en el orden, ni en los adjetivos | ADR-008 — proponer, nunca decidir, llevado a su forma más estricta |
| R-4 | **Ningún invariante epistémico cambia con la posición.** Alegado no es acreditado; la fuente exacta; no calcular; no afirmar derecho; la ausencia formulada sobre el material. **Decirlo es parte de la regla**, para que la variante no se lea como permiso para aflojar algo | Las once skills |
| R-5 | **Una sola redacción para las dos posiciones, no dos versiones del método.** Bifurcar los `SKILL.md` en dos variantes garantiza que deriven, que es la enfermedad que este repositorio lleva documentada desde `BACKLOG` §0.2 | `EP-C06` · ADR-014 invariante 6 |
| R-6 | **«La propia interesada» y «la otra parte» siguen siendo categorías de quién produjo un documento**, y no se tocan: en contexto B siguen significando exactamente lo que significan | `inventario-de-anexos` §3 · `inventario-de-bienes` §3 |
| R-7 | **Los ejemplos del método no son la voz de la salida.** Están escritos desde el primer uso, que fue de parte; **la salida usa el vocabulario de la posición de ella**, no el del ejemplo | Este documento |

## 4. Qué NO hace

- **No crea una segunda versión de ninguna skill.** Un bloque, idéntico en los once (R-5).
- **No reescribe los ejemplos** a vocabulario de autoridad: eso solo invertiría el sesgo y duplicaría el trabajo de mantenerlos.
- **No cambia ninguna garantía epistémica** (R-4). Las endurece en un solo eje: la orientación.
- **No decide si una inspectora puede apoyar un acto administrativo en una salida de IA.** Eso es `V-7`, necesita criterio jurídico y necesita un ADR **antes** que una spec (regla 2 de esta capa). Ver §7.
- **No toca las categorías de productor** de los dos inventarios (R-6).

## 5. Cómo se sabe que quedó

| # | Observable | Cómo se comprueba | Resultado |
|---|---|---|---|
| O-1 | Los **once** `SKILL.md` traen el bloque de posición, con la misma redacción | `grep -c` de la frase canónica = 11 | **Pasa** |
| O-2 | En los once está escrito que si no se puede saber la posición, **se pregunta una vez y se espera la respuesta antes de producir nada** | `grep` | **Pasa — el «y se espera» no estaba.** Preguntar y seguir sobre una suposición produce una salida entera, bien escrita, en el registro que no era |
| O-3 | En los once está la **simetría obligatoria**, con la orden de escribir el resultado la haya o no | `grep` | **Pasa** |
| O-4 | En los once está que **ningún invariante cambia** con la posición | `grep` | **Pasa** |
| O-5 | En los once está que los ejemplos no son la voz de la salida | `grep` | **Pasa** |
| O-6 | **Las cinco reglas** que presuponían bando están reescritas sin presuponerlo. **Eran cinco, no dos:** al buscar los residuos aparecieron tres más —las dos listas de «formas prohibidas de resolver un conflicto» de `cronologia` y la de contradicciones de `hechos-con-prueba`—, **todas del mismo tipo y la más peligrosa de todas**: le decían al método que no eligiera la versión «de la clienta», y a quien decide eso le sonaría a que sí puede elegir la de alguien | `grep` de los residuos, descontando los ejemplos | **Pasa** |
| O-7 | Las categorías de productor de los dos inventarios **no cambiaron** | `git diff` de esas líneas: vacío | **Pasa** |
| O-8 | Una pasada real en posición de autoridad, en la que ella **no tenga que traducir nada** | — | **Pendiente. Es el observable que importa** |
| O-9 | En esa pasada, que la simetría dispare al menos una vez y se vea en la salida | — | **Pendiente** |
| O-10 | La posición se deduce de la carpeta sin preguntar cuando la carpeta lo dice | Pasada de escritorio sobre `caso-02` | **Pasa** |
| O-11 | **La simetría no ensancha lo que un método puede señalar** | La pasada de escritorio, que encontró que **sí lo ensanchaba** | **Pasa — y no pasaba.** Ver abajo |

### Lo que encontró ejecutarla

**La regla de simetría, tal como la escribí, abría la puerta a la infracción más grave del producto.** Decía que se buscara en las demás partes *«toda carencia que señales de una parte —un documento que no acreditó, una afirmación sin respaldo, **un requisito que no consta**—»*.

Al aplicarla al `caso-02` —donde ninguno de los dos apoderados acredita su calidad, que es la trampa puesta para esto— apareció el problema: **`estado-del-caso` no puede decir eso.** Que la acreditación se exija es una regla de derecho, y los once métodos tienen prohibido contener derecho. *«Un requisito que no consta»* **es una invitación a valorar un requisito**: escribí una regla de imparcialidad que autorizaba a hacer derecho.

**Corregido en los once:** la simetría alcanza a *«toda carencia que este método ya pueda señalar»*, con la advertencia escrita al lado — *«no ensancha lo que puedes señalar: solo obliga a mirar a los dos lados de lo que ya señalabas»*.

> **Y la trampa no se pierde, cambia de sitio** — aunque no al sitio que escribí primero. **Dije que la hacía visible `inventario-de-anexos`, y lo dije sin comprobarlo: es falso.** Ese comando toma las afirmaciones que sostiene de tres sitios —hoja de hechos aprobada, borrador, o lo que ella indique— y **ninguno es «lo que el propio material afirma»**.
>
> **Dispara en `hechos-con-prueba`**, cuya Fase 2 sí recoge lo que el material afirma y cuya Fase 5 marca **sin apoyo** lo que no tiene ninguna pieza detrás. **Y hacía falta anclarla ahí**: un principio general escrito en once bloques, sin punto de enganche, es un principio que no dispara. Queda anclado en esa fila, con el caso real de los dos apoderados como ejemplo.
>
> **La cadena es de dos pasos:** `hechos-con-prueba` lo hace visible y aplica la simetría → ella lo aprueba → `inventario-de-anexos` lo empareja con el documento ausente. **Que sea una cadena y no un comando es la razón por la que no se veía.**

## 6. Qué toca

| Archivo | Qué |
|---|---|
| Los once `SKILL.md` | El bloque de posición, **idéntico**, junto al principio rector de cada uno |
| `hechos-con-prueba/SKILL.md` §2 y §5 | *«incluida tu propia clienta»* y *«ni la de la propia clienta»* → sin presuponer bando |
| `cronologia/SKILL.md` §2 y §3.5 | Las dos listas de formas prohibidas de resolver un conflicto |
| `inventario-de-bienes/SKILL.md` §3 y Fase 2 | *«el documento de la propia clienta»* y *«ni el de tu propia clienta»* |
| `revisar-documento/SKILL.md` §5 | *«se dirige a ella o a su clienta»* → sin presuponer bando |
| `redactar-escrito/SKILL.md` §2 | **El valor conservador de `V-7`**: en posición de autoridad redacta la parte fáctica y se detiene, y lo dice |
| `GUIA-PARA-LA-ABOGADA.md` | Que le diga, en su idioma, que el sistema le pregunta en qué posición está y por qué |

## 7. Qué queda fuera y por qué

**Lo que está bloqueado, y no por falta de trabajo mío:**

- **Si una inspectora puede apoyar un acto administrativo en una salida de IA, si debe declararlo, y qué le pasa al acto si la cita sale mal.** Es `V-7`, **el riesgo mayor del producto en su único uso real**, y no tiene ni una línea en todo el repositorio. **Necesita un ADR con criterio jurídico antes que una spec**, por la regla 2 de esta capa.
- **Y mientras ese ADR no exista, esta spec deja puesto el valor conservador**, que es el único defendible sin él: en posición de autoridad, `/redactar-escrito` **redacta la parte fáctica y se detiene ahí** —que es exactamente lo que ya hace en su §1, así que no cuesta nada—, **no redacta la parte que decide**, y lo dice con esas palabras. Si el ADR después lo autoriza, se levanta; si lo prohíbe, ya estaba prohibido.

**Lo que se decidió posponer:**

- **Reescribir los ejemplos** (R-7). Serían ~10 ejemplos duplicados en dos voces, y el mantenimiento de un ejemplo duplicado es exactamente donde empiezan las derivas.
- **Una tercera posición.** Un mediador, un árbitro, un perito no son parte ni autoridad en el mismo sentido. **Dos posiciones cubren el uso real que existe**; inventar una tercera sin haberla visto es publicar una forma que nadie ha usado (`H-10`).
- **Detectar la posición automáticamente sin preguntar nunca.** Se podría intentar por los documentos, y **fallaría en silencio** — que es el modo de fallo que este producto persigue en todo lo demás.
