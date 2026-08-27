# El instrumento de verificación — la ficha y cómo se llena

**Fecha: 2026-08-27. Material de trabajo, no una Skill.** Se escribe porque §8.2 quedó decidida: hay una abogada que verifica, y se acepta la regla dura *sin vigencia comprobada y firmada, la norma no se sirve como citable*.

**Este archivo no contiene una sola norma, una sola fecha de vigencia ni un solo estado.** Todo lo que aquí parece un dato jurídico es un relleno evidente (`LEY-0000-0000`, `AAAA-MM-DD`). El contenido lo escribe la verificadora. Si el modelo escribe un dato en una ficha, el instrumento queda anulado: ver §5, regla 1.

El contrato de consumo —qué contesta el pack y qué no— está en [02-contrato-de-consumo.md](02-contrato-de-consumo.md). Los dos archivos se leen juntos: la ficha sin el contrato es una tabla bonita, y el contrato sin la ficha no tiene qué servir.

---

## §0 — Qué sustituye este instrumento

Hoy lo único que impide que el sistema cite una norma derogada es que **no cita normas** (`REFINADO-Y-FUENTES.md` §1.a). Es una abstinencia, no un mecanismo, y se acaba el día que exista el pack. Esto es lo que la reemplaza.

El fallo concreto que hay que hacer imposible ya ocurrió dentro del propio corpus: **un registro comprobado en su identidad —«esta norma existe y es esta»— leído como comprobado en su vigencia —«esta norma rige»—**. Hoy las dos cosas comparten una sola etiqueta (`VERIFIED_OFFICIAL` / `FUENTE_OFICIAL_VERIFICADA`) y esa etiqueta convive con la columna de vigencia en blanco en el 100 % de las filas.

Volumen: **25 identificadores normativos y 4 providencias**. Ninguno tiene vigencia comprobada hoy.

---

## §1 — La regla de diseño: dos columnas que nunca se juntan

1. **`estado_identidad` y `estado_vigencia` son dos campos.** No hay ningún campo, ninguna etiqueta y ninguna respuesta del pack que combine las dos en un solo valor. Tampoco hay un estado «verificado» a secas.
2. **La disciplina baja hasta la fuente.** Identidad y vigencia se comprueban contra fuentes distintas y se registran en campos distintos (`fuente_identidad`, `fuente_vigencia`). Una sola casilla de «fuente» vuelve a fundir las dos columnas por la puerta de atrás.
3. **Antes de que nada del catálogo actual entre al pack, `VERIFIED_OFFICIAL` / `FUENTE_OFICIAL_VERIFICADA` se renombra `IDENTIDAD_VERIFICADA`** en `source-catalog/`. Es una sustitución de texto y es media causa del error documentado.
4. **Un registro sin nombre y sin fecha está afirmado, no comprobado.** No existe la ficha anónima: una ficha sin `verificado_por` no es una ficha a medias, es una ficha que el pack no sirve.

---

## §2 — La ficha de una norma: 12 campos

`Quién`: **V** = la verificadora. **C** = copiado del catálogo actual y confirmado por ella (barato). **=** = se calcula al leer, coste humano cero. `Cómo` remite al paso del procedimiento (§5).

| # | Campo | Valores admitidos | Quién | Cómo | Qué fallo concreto evita |
|---|---|---|---|---|---|
| 1 | `identificador_canonico` | `TIPO-NUMERO-AÑO` (`LEY-0000-0000`) | C | P1 | La clave de hecho hoy es la URL, y el mismo texto convive con tres formas de dirección dentro del catálogo |
| 2 | `alcance_comprobado` | texto corto y cerrado: `norma completa` \| `art. 00` \| `art. 00, inciso 0` | V | P2 | Comprobar la ley y citar el inciso. Es también lo que permite trabajar sin haber decidido §8.1 (unidad ley o artículo): la ficha declara qué se comprobó de verdad, no qué se supone |
| 3 | `materia[]` | vocabulario ya usado en `source-catalog/` | C | P1 | Sin esto, la respuesta «el pack no cubre esa área» no se puede calcular y la ausencia se lee como inexistencia |
| 4 | `estado_identidad` | `IDENTIDAD_VERIFICADA` \| `IDENTIDAD_POR_VERIFICAR` \| `CONFLICTO_DE_FUENTES` | V | P1 | La cita fantasma: un identificador plausible que nadie comprobó |
| 5 | `fuente_identidad` | URL o referencia de publicación oficial + fecha de consulta | C+V | P1 | «Verificado» contra un compilador que en sus propios avisos dice que no certifica |
| 6 | `estado_vigencia` | `VIGENTE_AL AAAA-MM-DD` \| `SIN_VIGENCIA_DESDE AAAA-MM-DD` \| `VIGENCIA_PARCIAL_AL AAAA-MM-DD` \| `VIGENCIA_POR_VERIFICAR` | V | P4 | **El campo del encargo.** Convierte «norma derogada» en un fallo detectable en vez de en una salida fluida |
| 7 | `vigencia_desde` | `AAAA-MM-DD` \| `ESCALONADA` | V | P3 | Aplicar la norma nueva a un caso anterior a su entrada en vigor. Es la prueba de calidad temporal que el propio corpus se impuso |
| 8 | `fuente_vigencia` | URL o referencia + fecha de consulta, y su clase (`PRIMARY_OFFICIAL`, `OFFICIAL_CONSOLIDATED`… de `04-source-governance.md` §4.1) | V | P4 | Que la vigencia se dé por buena porque «el portal no decía nada». La ausencia de aviso no es una comprobación |
| 9 | `nota_de_vigencia` | prosa, máximo dos líneas | V | P3-P4 | La mentira forzada: derogación parcial, entrada escalonada o control pendiente que no caben en un valor. **El pack nunca la interpreta**: se muestra tal cual a la abogada |
| 10 | `verificado_por` | nombre completo de la persona | V | P5 | Sin nombre no hay nadie que responda, y el registro vuelve a estar afirmado |
| 11 | `verificado_el` | `AAAA-MM-DD` | V | P5 | Un pack sin fechas no envejece: se pudre en silencio |
| 12 | `revisar_antes_de` | `AAAA-MM-DD`; por defecto `verificado_el` + la cadencia; ella puede acortarla, nunca alargarla | = / V | §6 de `02` | Que el pack siga sirviendo datos viejos con la misma cara |

**Por qué doce y no más.** Seis campos (2, 4, 6, 7, 8, 9) son el trabajo real; tres (1, 3, 5) son copia confirmada del catálogo que ya existe; dos (10, 11) son la firma; uno (12) se calcula. Cada campo añadido se llena 25 veces: los que se propusieron y no entran están en §3, con el motivo y con el riesgo que queda abierto.

### Los dos estados, escritos entero

`estado_identidad`
- `IDENTIDAD_VERIFICADA` — la persona vio el texto en fuente oficial y el identificador corresponde. **No dice nada sobre si rige.**
- `IDENTIDAD_POR_VERIFICAR` — no se pudo cerrar. Es un valor legítimo, no un fracaso.
- `CONFLICTO_DE_FUENTES` — dos fuentes oficiales discrepan en la identidad. Se registran las dos en `fuente_identidad` y **no se elige** (`04-source-governance.md` §4).

`estado_vigencia`
- `VIGENTE_AL AAAA-MM-DD` — al día de la comprobación, y **solo dentro de `alcance_comprobado`**.
- `SIN_VIGENCIA_DESDE AAAA-MM-DD` — dato positivo y valioso: el pack sabe que no rige y puede decirlo.
- `VIGENCIA_PARCIAL_AL AAAA-MM-DD` — rige en parte. Obliga a llenar `nota_de_vigencia` y **nunca se sirve como citable** para el alcance completo.
- `VIGENCIA_POR_VERIFICAR` — se buscó y no se pudo establecer, o no se buscó. Etiqueta ya existente en el corpus. **Será el valor mayoritario del primer pack, y así debe verse desde fuera.**

### Ficha de ejemplo — datos inventados

```yaml
identificador_canonico: LEY-0000-0000
alcance_comprobado: "art. 00"
materia: [area-de-ejemplo]
estado_identidad: IDENTIDAD_VERIFICADA
fuente_identidad: "https://ejemplo.invalido/publicacion-oficial — consultada AAAA-MM-DD"
estado_vigencia: VIGENCIA_POR_VERIFICAR
vigencia_desde: ESCALONADA
fuente_vigencia: "no se localizó fuente de clase PRIMARY_OFFICIAL para el art. 00"
nota_de_vigencia: "la entrada en vigor no es única para toda la norma; no se pudo fijar la del art. 00 en el tiempo disponible"
verificado_por: "Nombre Apellido"
verificado_el: AAAA-MM-DD
revisar_antes_de: AAAA-MM-DD
```

Esta ficha —incompleta, firmada y honesta— **es una ficha válida**. Lo que el pack hará con ella es negarse a servirla como citable y decir por qué. Eso es exactamente lo que se está comprando.

---

## §3 — Lo que se propuso y no entra en la ficha

| Campo del refinado §1.a | Qué se hace | Por qué | Riesgo que queda abierto |
|---|---|---|---|
| `texto_literal` + `locator` + `fecha_de_captura` | **Fuera.** El pack no contiene texto normativo | Transcribir 25 normas es el campo más caro de todos y reabre la superficie de invención justo donde más duele. La decisión de citabilidad no lo necesita | El pack puede confirmar que una norma existe y rige, y el sistema atribuirle algo que no dice. Lo contiene la regla 1 del método («el método no contiene derecho») y el §3 del contrato, no la ficha |
| `regla_de_entrada_en_vigor` + su pasaje | **Plegado** en `vigencia_desde: ESCALONADA` + `nota_de_vigencia` | La parte comparable contra la fecha de un caso es la fecha; el resto es prosa, y como campo propio era prosa que se creía dato | Una norma escalonada solo sirve citable si se estrecha `alcance_comprobado` hasta donde hay fecha |
| `derogada_por` + `derogada_desde` | **Plegado** en `SIN_VIGENCIA_DESDE` + nota | Para decidir si se cita basta la fecha. Como campo propio invitaba a copiar una afirmación que ya está en otro archivo del corpus y darla por comprobada — el lavado que prohíbe `04-source-governance.md` §7 | La abogada ve la fecha y la nota, no un identificador estructurado del acto derogatorio |
| `modificada_por[]` | **Fuera** | N entradas por registro, y solo muerde a nivel de artículo, que es lo que ya declara `alcance_comprobado` | **El pack no avisa de que se está citando la redacción original de un artículo reformado.** Es la exclusión más cara y hay que decirla en voz alta |
| `alcance_derogacion` + `pasaje_derogatorio` | **Fuera** | Ya rechazados en `REFINADO-Y-FUENTES.md` §6. No se resucitan | — |
| `unidad` (ley/artículo/inciso/parágrafo) como taxonomía | **Sustituido** por `alcance_comprobado` | §8.1 sigue sin decidir. Una taxonomía obliga a decidirla; declarar qué se comprobó funciona bajo cualquiera de las dos respuestas | Ninguno: el campo es más honesto que la taxonomía |
| `url_acceso[]` (varias) | **Colapsado** en `fuente_identidad` (una) + `fuente_vigencia` | Tres URLs por registro son copia que no cambia ninguna decisión | — |

**Campos que no estaban en la tabla del refinado y sí entran:** `materia[]` (sin él la respuesta de cobertura no se puede calcular), `fuente_vigencia` (el refinado pedía quién comprobó, pero no contra qué) y `alcance_comprobado`.

---

## §4 — La ficha de una providencia: 9 campos

**La unidad no es la providencia: es el par providencia + proposición.** La misma sentencia puede sostener una afirmación y no sostener otra; el propio catálogo ya tiene una registrada como control negativo. Una providencia usada para dos cosas son dos fichas.

La identidad ya está bien capturada en las 4 fichas actuales (corporación, sala, expediente, fecha, ponente) y **no se rehace**: se copia. Lo que falta es el pasaje, la regla atribuida y la constancia de la búsqueda adversa — que `07-jurisprudence-governance.md` declara obligatoria y que las cuatro fichas dejaron en `POR_VERIFICAR`.

| # | Campo | Valores | Quién | Qué fallo evita |
|---|---|---|---|---|
| 1 | `identificador` | el del catálogo (`J-XX-0000-0000`) + enlace oficial | C | — |
| 2 | `estado_identidad` | `IDENTITY_VERIFIED` \| `JURISPRUDENCIA_POR_VERIFICAR` (`07`, sin cambios) | C+V | La providencia inexistente con radicado, sala y ponente plausibles |
| 3 | `proposicion_atribuida` | la frase exacta que se pretende sostener. **Nunca un resumen** | V | «La Corte dijo que…» sobre una providencia que decidió otra cosa |
| 4 | `pasaje` | párrafo / numeral / página del texto que la sostiene | V | Sustituir el pasaje por el título o el resumen del buscador |
| 5 | `estado_uso` | `PROFESSIONALLY_CONFIRMED` \| `RELEVANCE_REVIEWED` \| `CONFLICTING` \| `SUPERSEDED_OR_LIMITED` \| `JURISPRUDENCIA_POR_VERIFICAR` (`07`, sin cambios) | V | Citar un precedente superado. `SUPERSEDED_OR_LIMITED` es el mecanismo entero contra eso y hoy no se usa una sola vez fuera de su definición |
| 6 | `busqueda_adversa` | constancia en una línea —**dónde, con qué criterio, qué día y qué salió**— o `JURISPRUDENCE_GAP` | V | Presentar como exhaustivo lo que fue un solo resultado. Es el campo que las cuatro fichas dejaron abierto |
| 7 | `verificado_por` | nombre completo | V | — |
| 8 | `verificado_el` | `AAAA-MM-DD` | V | — |
| 9 | `revisar_antes_de` | `AAAA-MM-DD` | = / V | — |

Ejemplo de `busqueda_adversa` con datos inventados: `"buscada AAAA-MM-DD en <relatoría oficial>, criterio «<tema>», años 0000-0000; apareció una decisión posterior en sentido contrario, SENTENCIA-X-000-0000 — por eso estado_uso = CONFLICTING"`. Y su forma honesta cuando no se cerró: `JURISPRUDENCE_GAP — buscada AAAA-MM-DD; la cobertura del portal no alcanza el periodo`.

**No hay ficha de providencia sin `busqueda_adversa` llena.** Vacía significa que nadie buscó, y una providencia sin búsqueda adversa entra al pack como `JURISPRUDENCIA_POR_VERIFICAR`, nunca como citable.

---

## §5 — El procedimiento, paso a paso

### Las cinco reglas que no se negocian

1. **El modelo no llena ninguna casilla de ninguna ficha, ni siquiera una que «ya sabe».** Puede abrir un buscador, transcribir una URL que ella dicte o formatear la tabla. En el momento en que produce un valor, este instrumento deja de existir: el pack pasaría a certificar exactamente aquello que estaba puesto para vigilar.
2. **Ninguna casilla se queda vacía.** Vacío se lee como «no aplica». `VIGENCIA_POR_VERIFICAR` y `JURISPRUDENCE_GAP` son respuestas correctas y frecuentes.
3. **No se copia una afirmación de otro archivo del corpus a una ficha.** Que un archivo del proyecto diga algo no es una comprobación; moverlo de sitio tampoco (`04-source-governance.md` §7).
4. **La ausencia de aviso en un compilador no es una comprobación de vigencia.** Los propios portales institucionales advierten que no certifican vigencia por sí solos.
5. **Si se acaba el tiempo, se firma lo comprobado y se para.** Media ficha firmada vale; una ficha entera completada de memoria destruye el pack, y no se nota hasta el caso real.

### P0 — Una sola vez, antes de empezar (≈1 hora)

Fijar con el dueño la cadencia por defecto de `revisar_antes_de` (§6 de `02`) y, cuando las dos cosas sean posibles, si se comprueba a nivel de norma completa o de artículo (§8.1). Hacer **una ficha completa entre los dos** y cronometrarla: es la única forma de saber cuánto cuesta de verdad el resto.

### P1 — Identidad (5-10 min)

Localizar el texto en fuente de publicación oficial. Orden de trabajo: el de `04-source-governance.md` §2; los portales, en `source-catalog/colombia-official-sources.md`. Llenar 1, 3, 4, 5. Si dos fuentes oficiales discrepan → `CONFLICTO_DE_FUENTES`, las dos anotadas, no se elige.

### P2 — Alcance (2 min, y decide el coste de todo lo demás)

Escribir en `alcance_comprobado` qué se va a comprobar. Estrechar es siempre legítimo y casi siempre más barato: comprobar un artículo concreto es trabajo acotado; comprobar «la norma completa» obliga a descartar cambios sobre todo su articulado.

### P3 — Desde cuándo (5-10 min)

Buscar la regla de entrada en vigor **para el alcance elegido**. Si es una fecha, va en `vigencia_desde`. Si la norma entra por partes y no se puede fijar la del alcance: `ESCALONADA`, la explicación en `nota_de_vigencia`, y `estado_vigencia = VIGENCIA_POR_VERIFICAR` salvo que se estreche el alcance hasta donde sí hay fecha.

### P4 — Hasta cuándo (10-15 min; es el paso caro y el que justifica todo)

Buscar activamente si algo posterior alcanza lo comprobado: derogatoria, sustitución, reforma o decisión de control. **La comprobación no es leer una etiqueta: es buscar y registrar qué se buscó.**
- Se encontró algo y llega hasta el alcance → `SIN_VIGENCIA_DESDE AAAA-MM-DD`.
- Se encontró algo y alcanza solo una parte → `VIGENCIA_PARCIAL_AL AAAA-MM-DD` + nota.
- Se buscó y no apareció nada, **con al menos una fuente de clase `PRIMARY_OFFICIAL`** → `VIGENTE_AL AAAA-MM-DD` (la fecha de hoy).
- Se buscó y no se pudo cerrar, o solo hubo fuente consolidada → `VIGENCIA_POR_VERIFICAR`, y en `fuente_vigencia` **qué se consultó y por qué no basta**.

### P5 — Firma (2 min)

`verificado_por`, `verificado_el`. `revisar_antes_de` sale por defecto de la cadencia; ella lo acorta si la nota registra un cambio con fecha futura o un control pendiente. Nunca lo alarga.

### PJ — Providencias (45-75 min por par providencia+proposición)

**PJ1** copiar la identidad del catálogo y confirmarla (5 min). **PJ2** escribir `proposicion_atribuida` **antes** de leer, para no ajustar la frase al pasaje que aparezca (5 min). **PJ3** localizar el pasaje y decidir si de verdad la sostiene (15-25 min). **PJ4 búsqueda adversa**: autoridad contraria, limitante, posterior, de unificación y hechos distinguibles (20-40 min; domina el coste, y es el paso que hoy no se ha hecho nunca).

### El coste real, sin adornos

| | Por unidad | Total |
|---|---|---|
| Norma sencilla, alcance de artículo | 20-30 min | |
| Norma con entrada escalonada, reformas o control pendiente | 45-90 min | |
| **25 normas** | media ≈35 min | **12-18 h** |
| **Providencias**, por par providencia+proposición | 45-75 min | **3-5 h** |
| P0 y calibración de la primera sesión | | **+2 h** |
| | | **≈17-25 h de trabajo profesional** |

En sesiones de dos horas son unas dos semanas de calendario a ritmo de encargo secundario. **La reverificación posterior es mucho más barata —10-15 min— porque solo se mueve la columna de vigencia**: la identidad no se pudre. Ese es el argumento económico para separar las dos columnas, además del argumento de veracidad.
