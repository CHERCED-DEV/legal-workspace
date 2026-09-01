# SPEC-10 — El límite del material extraído, dentro de los `SKILL.md`

**Estado:** ejecutada · **Cierra:** `H-16` · `EP-1.1-COORDENADA` · **Familia:** defecto

---

## 1. Qué problema cierra

`BACKLOG-CONSOLIDADO` §4 lo tiene entre los parciales, y lo dice exacto:

> *«ADR-016 y ADR-017 documentan el límite; **no consta la regla de fallo declarado dentro de los `SKILL.md`**.»*

**Comprobado el 2026-08-31, y es peor de lo que el ítem sugiere: no consta en ninguna.**

| | Skills que lo llevan |
|---|---|
| Cómo se abre un escaneado sin texto | 8 de 9 |
| **Qué vale y qué no vale el texto ya extraído** | **0 de 9** |

Ocho skills saben abrir una imagen. **Ninguna sabe que el archivo `Texto de referencia - <fecha>.txt` que la tubería deja en `2-Borradores/` no es el documento.** Y `revision-de-rigor` —la que audita el rigor de las demás— **no tiene ninguna de las dos**.

**Por qué esto no es una omisión de redacción.** ADR-016 invariante 1 dice que *ninguna ausencia en el texto extraído es información sobre el documento*. Ese invariante **solo existe en el ADR**. El comando que lee la carpeta, encuentra un `.txt` con el texto de las 23 páginas y no ve ahí una fecha, **no tiene hoy ninguna regla escrita que le impida concluir que la fecha no está**. Es exactamente el fallo que ADR-016 nació para impedir, sin barrera en el sitio donde ocurriría.

**Y la medición del 2026-08-31 añade dos cosas que el ADR no podía saber** (`docs/CAPACIDADES-PYTHON-VERIFICADAS.md` §4.4):

1. **El filtro de confianza deja pasar basura.** Con el umbral vigente de 0,5 entraron al texto renglones como `sso d nn i` (0,52) y `Rla` (0,88).
2. **El reconocedor emite ideogramas chinos** sobre un documento en español, porque su vocabulario es multilingüe. **Un expediente colombiano no contiene nunca un carácter CJK**, así que es una marca de basura de certeza absoluta — y gratis.

## 2. Comportamiento observable

Cuando un comando encuentra texto extraído automáticamente:

1. **Lo usa para saber dónde mirar**, y abre el documento para citar.
2. **No concluye nada de que algo no aparezca ahí.**
3. **No cita** un renglón sin palabras reconocibles ni uno con caracteres CJK.
4. Si una cita literal sale solo del texto extraído y el documento no se abrió, **la salida lo dice**.

## 3. Reglas duras

| # | Regla | De dónde sale |
|---|---|---|
| R-1 | **Ninguna ausencia en el texto extraído es información sobre el documento** | ADR-016 invariante 1 |
| R-2 | **Ninguna cita literal proviene de un texto marcado no citable** | ADR-016 invariante 4 |
| R-3 | **El texto extraído nunca sustituye al original como fuente de la cita** | ADR-016 invariante 9 |
| R-4 | **Ninguna cita literal proviene de un segmento de audio no cotejado contra el original** | ADR-017 §2 |
| R-5 | **El bloque es el mismo texto en todas**, como el de anti-inyección: una regla que cada skill enuncia distinto deja de ser una regla | `H-10` · la lección del «séptimo comando» |

## 4. Qué NO hace

- **No cambia la tubería de ingesta.** El umbral de 0,5 y el filtro CJK se corregirán en `preparar_material.py`; esta spec solo hace que **quien lea el resultado sepa lo que tiene delante**.
- **No obliga a abrir todos los documentos siempre.** Obliga a **declarar** si no se abrieron.
- **No añade el bloque a `preguntas-de-derecho`**, que no lee material.
- **No inventa una regla nueva.** Los cuatro invariantes ya estaban decididos; esta spec los pone donde se ejecutan.

## 5. Cómo se sabe que quedó

| # | Observable | Resultado |
|---|---|---|
| O-1 | Las ocho skills que leen material llevan el bloque | **PASA** — 8 de 8 |
| O-2 | El texto es **idéntico** en las ocho | **PASA** — comprobado por huella |
| O-3 | `preguntas-de-derecho` **no** lo lleva, y por la razón escrita | **PASA** |
| O-4 | La autoevaluación de cada skill pregunta por él | **PASA** — 8 de 8 |
| O-5 | Una pasada real sobre material con basura de OCR no cita esa basura | **Pendiente — necesita una pasada** |

## 6. Qué toca

`plugins/despacho/skills/*/SKILL.md` — las ocho que leen material: bloque nuevo en §2, justo después de «el trabajo del propio sistema no es fuente de nada», que es la regla hermana; y una línea más en la autoevaluación.

## 7. Qué queda fuera y por qué

- **Corregir el umbral de 0,5 y filtrar CJK en la ingesta.** Es trabajo de `preparar_material.py` y tiene su propia entrada en `CAPACIDADES-PYTHON-VERIFICADAS` §8. **Van por separado a propósito:** si la ingesta mejora, el bloque sigue siendo necesario, porque **ningún umbral convierte el texto extraído en el documento**.
- **La versión del plugin.** Deferida al hueco `V-10`, igual que en SPEC-01 y SPEC-09. **Van ya tres specs esperando esa decisión**, y es el argumento más fuerte para tomarla.
- **La doble lectura** medida el mismo día. Cuando exista, este bloque tendrá que decir además de cuál pasada salió cada renglón.
