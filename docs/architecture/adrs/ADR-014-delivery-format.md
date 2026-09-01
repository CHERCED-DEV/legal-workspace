# ADR-014 — Forma de entrega: el entregable es un documento de Word, y el Markdown no es una forma de entrega

## Estado

Proposed

## Contexto

El informe de crítica registró como H-13 que las tablas de Markdown pegadas en Word son una hilera de tuberías, y que la promesa «lista para pegar» falla al primer intento.

> **CORRECCIÓN — 2026-08-28.** La versión anterior de este párrafo decía que H-13 «era una predicción de diseño» que el pase de Salento «convirtió en hecho observado». **Es inexacto y hay que corregirlo:** el pase anterior sobre el caso de familia (2026-08-26) **ya había producido dos `.docx`** —`Inventario de anexos … pasada 1` y `pasada 2`—, y `inventario-de-bienes/SKILL.md` **ya especificaba** salida en Word. Es decir: la necesidad estaba identificada y parcialmente atendida antes de este ADR.
>
> **Lo que el pase de Salento sí aportó, y es lo que este ADR decide:** que la salida en Word deje de ser un acierto de una pasada y pase a ser **forma nativa con reglas** —dos capas, tablas reales obligatorias, encabezado de propuesta, fallo declarado—, más un conversor reutilizable en vez de trabajo a mano cada vez.

Con esa precisión hecha, el pase del 2026-08-27/28 sobre el expediente [radicado del expediente] añadió algo que la predicción no decía: **el problema no es el pegado, es la forma del entregable**.

Tres datos del pase, verificables en `docs/PASE-REAL-SALENTO-2026-08-27.md`:

1. **La usuaria no abre Markdown.** El dueño lo formuló sin ambigüedad: *«ella no es una persona de nivel técnico, ella lo que hace es ver words»*. Las doce salidas en `.md` fueron, para ella, doce archivos que no se abren solos.
2. **Cuatro de los seis SKILL prometen tablas «listas para pegar»** —`inventario-de-anexos` §7, `inventario-de-bienes`, `cronologia` §6, `redactar-escrito` §7— y solo dos añaden que eso exige una tabla de verdad. La regla existe a medias.
3. **Producir `.docx` con tablas reales es barato.** El pase generó tres documentos: 27 tablas, 133 filas, con un script de ~120 líneas. No requiere Core, ni MCP, ni conector.

Un cuarto dato, sobre el material de entrada: las 23 fotografías se consolidaron en **un PDF ordenado**, enderezado y con un pie que dice qué es cada página. Resolvió un problema que ningún skill contemplaba —la usuaria tenía 23 JPG sueltos y las citas del sistema decían «auto p. 3»— y plantea la pregunta de arquitectura que este ADR debe cerrar: **qué es ese PDF respecto de los originales**.

## Decision

### 1. Dos capas de salida, ambas obligatorias, con destinatarios distintos

| Capa | Formato | Para quién | Qué contiene |
|---|---|---|---|
| **Trabajo** | `.md` | El sistema, la auditoría, la pasada siguiente | La salida completa, con todos los localizadores y conteos |
| **Entrega** | `.docx` | La profesional | Lo mismo, con la forma que ella puede abrir, leer e imprimir |

Ambas en `2-Borradores/`. **La capa de trabajo no desaparece:** es la que permite comparar dos pasadas y la única que un comando posterior puede leer como pista. **La capa de entrega no es un resumen:** si omite algo, lo dice.

### 2. Toda tabla prometida «lista para pegar» es una tabla de Word real

Prohibido entregar una tabla de Markdown como entregable. La promesa «lista para pegar» **solo puede escribirse en un SKILL si el comando produce `.docx`**.

### 3. El encabezado de propuesta viaja en el `.docx`, no solo en el `.md`

`redactar-escrito` §7 ya lo exige para el borrador. Se generaliza: **toda salida de entrega lleva en su primera página el bloque que dice qué es —propuesta, no revisada, sin comprobación de ningún sistema— y de qué material se hizo.** Un documento de Word con aspecto terminado se lee como terminado.

### 4. Fallo declarado, nunca archivo supuesto

Regla ya presente en dos skills, elevada a decisión: **si no se puede producir el `.docx`, se escribe el contenido en texto y se dice que no se pudo.** Y si no se pudo **verificar el render**, también se dice: en el pase real no había suite ofimática en la máquina, la estructura se comprobó programáticamente y el no haberlo visto quedó declarado en la entrega.

### 5. Los entregables se numeran por orden de lectura

`0 -`, `1 -`, `2 -`… en el nombre. Motivo observado: doce archivos con nombres igualmente descriptivos no le dicen a nadie por dónde empezar. Es orden de **lectura**, no de importancia ni de fecha.

### 6. El material recibido se consolida en un PDF ordenado, y ese PDF es un derivado

Cuando el material llega como piezas sueltas de imagen se produce **una** consolidación: páginas en orden procesal, enderezadas, con un pie que declara qué documento es y de qué archivo original salió.

**Y aquí la parte que toca ADR-011:** el número de página de ese PDF **no es coordenada de cita**. Es un índice de conveniencia sobre un derivado. La coordenada de cita sigue siendo la del original —documento y su página propia—. El pie de página existe para poder recorrer las dos en ambos sentidos sin que la derivada suplante a la original.

### 7. `1-Documentos recibidos/` no se toca, y la consolidación no lo contradice

El PDF se escribe en `2-Borradores/`. Rotaciones, recortes y escalados se hacen sobre copias fuera de la carpeta del caso. Los originales quedan intactos, con su huella registrada.

### 8. Alcance: esto no espera al Core

Las dos capas, las tablas reales y el PDF consolidado se producen hoy. Ninguna parte de este ADR depende del Core, del MCP ni de un conector.

## Invariantes derivados

1. **Ninguna salida de entrega se produce solo en Markdown.** Si falta la capa de entrega, la entrega está incompleta y se dice.
2. **Ninguna tabla del entregable es texto con tuberías.**
3. **Toda salida de entrega lleva su encabezado de propuesta en la primera página.**
4. **Nunca se afirma haber dejado un archivo que no se dejó, ni haber visto un render que no se vio.**
5. **El PDF consolidado no sustituye a los originales** y su numeración **no se usa jamás como coordenada de cita**, ni en un `EvidenceFragment` ni en el texto de una salida.
6. **La capa de trabajo y la de entrega dicen lo mismo**; si la de entrega omite algo, lo declara.

## Consecuencias positivas

- Cierra H-13 con una regla, no con una advertencia.
- La profesional deja de necesitar traducción: abre, lee, imprime y marca.
- El PDF consolidado convierte 23 archivos sueltos en un expediente navegable y hace verificables las citas del sistema sin tocar los originales.
- La capa de trabajo conserva la comparabilidad entre pasadas, que es lo único que permite medir si el método mejora.

## Consecuencias negativas

- **Duplicación real:** dos artefactos por salida, que pueden divergir. El invariante 6 lo acota; no lo elimina.
- **Dependencia nueva** de un generador de `.docx` y, para verificar el render, de una suite ofimática que en el pase real **no estaba instalada**.
- Un `.docx` bien maquetado **se lee como más terminado que un `.md`**. Es el riesgo que `redactar-escrito` §1 identifica en sí mismo, ahora extendido a todas las salidas. El encabezado obligatorio es la única mitigación, y es débil.
- Introduce una segunda numeración de páginas en el caso. La decisión 6 la subordina; la subordinación hay que sostenerla en cada salida.

## Alternativas consideradas

### (a) Solo Markdown, y que ella lo convierta
Descartada: traslada a la usuaria el paso técnico que es la causa de H-13. «Lista para pegar» pasa a ser una promesa que falla al primer intento.

### (b) Solo `.docx`, sin capa de trabajo
Descartada: sin `.md` no hay forma barata de comparar dos pasadas ni de que un comando posterior lea la salida anterior como pista. Se perdería el único instrumento de medición del método.

### (c) HTML o PDF como entregable
Descartada: ella edita. Un entregable no editable en su herramienta obliga a copiar y pegar, que es el problema original.

### (d) Plantilla `.dotx` del despacho
Aplazada, no descartada. Es mejor que un formato fijado por nosotros y requiere una plantilla real suya, que hoy no tenemos.

### (e) Consolidar el material dentro de `1-Documentos recibidos/`
Descartada frontalmente: violaría la intocabilidad del material tal como llegó, que es lo único del caso que no se puede reconstruir.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Las dos capas divergen | Se generan de una sola fuente en la misma pasada; nunca se edita una sin la otra |
| El `.docx` aparenta terminado | Encabezado en primera página; cierre obligatorio con lo que el documento no tiene |
| El generador falla en otra máquina | Fallo declarado (decisión 4); nunca se supone el archivo |
| La numeración del PDF se cuela como cita | Invariante 5; el pie de cada página nombra la coordenada original |
| Ella edita el `.docx` y la pasada siguiente lo pisa | La regla de no sobrescritura ya vigente se aplica igual a la capa de entrega |

## Validación / pruebas necesarias

1. **Abrir los tres `.docx` del pase real en su Word** y comprobar que las 27 tablas se ven como tablas. *No hecho: en la máquina del pase no había con qué renderizar.* **Bloquea la aceptación de este ADR.**
2. Comprobar que el PDF consolidado se abre, se busca y se imprime en su equipo.
3. Medir si el encabezado de propuesta **se lee**: preguntarle qué entendió que era el documento, sin sugerirle la respuesta.
4. Verificar que una segunda pasada no sobrescribe ni el `.md` ni el `.docx` anteriores.

## Preguntas pendientes

1. **¿Plantilla propia de ella o formato nuestro?** Depende de que entregue un escrito suyo de modelo.
2. ~~**¿Quién genera el `.docx`: la skill o el Core?**~~ **CERRADA el 2026-09-01 por ADR-018.** La premisa era falsa: **un plugin sí puede llevar y ejecutar código** —`scripts/`, `bin/`, `${CLAUDE_PLUGIN_ROOT}` y `allowed-tools`—. «Texto puro» describía lo construido y se leyó como límite de lo posible. **La skill genera el `.docx` llamando a un script bundleado; ni el Core ni nadie a mano.** Cinco días abierta por una suposición que nadie comprobó.
3. ¿El PDF consolidado se regenera cuando entra material nuevo, o se produce uno por tanda?
4. ¿Se entrega también `.pdf` de las salidas, para imprimir sin riesgo de edición accidental?

## Relaciones con otros ADRs

- **ADR-011** (locators): la decisión 6 se subordina a la regla de doble coordenada y a la prohibición de coordenadas derivadas con apariencia de originales. Este ADR **no introduce** ninguna coordenada nueva en el locator.
- **ADR-002** (case store) y **ADR-006** (incorporación): la consolidación no escribe sobre el material incorporado.
- **ADR-012** (distribución): la capa de entrega vive en la zona 2 —el escritorio de ella—, nunca en la zona 1.
- **ADR-005** (autoridad humana): el encabezado de propuesta es la forma visible de que ninguna salida está aprobada por el hecho de existir.
- **ADR-016** (ingesta sin capa de texto): el PDF consolidado es el punto donde una y otra decisión se tocan.
