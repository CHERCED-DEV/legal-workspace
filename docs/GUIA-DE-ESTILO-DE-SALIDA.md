# Guía de estilo de las salidas — arnés Despacho

v1.0 · 2026-08-27 · Obliga a los ocho comandos cuando se unifique el formato.

**Etiqueta de origen de cada regla:** **NORMA** (obliga en Colombia) · **ESTÁNDAR** (publicado, no obliga) · **PRÁCTICA** (consenso, sin publicar) · **NUESTRA** (decisión de producto sin respaldo externo; son legítimas, solo hay que decirlo). `[DUDOSO]` = entra, pero sin verificar.

**Admisión:** lo que el refutador tumbó no está aquí. Si alguien lo propone otra vez, §7 dice por qué no.

## §0 — La regla de oro

Una salida sirve si consigue estas tres cosas, y en este orden:

1. **Se entiende en dos minutos** leyendo solo la apertura, sin bajar al detalle.
2. **Se copia a su escrito sin reformatear** — la tabla llega a Word como tabla, el hecho como párrafo numerado.
3. **Enseña lo que falta** — el vacío y lo no verificado se ven sin buscarlos.

Si un cambio de formato no mejora una de las tres, no se hace.

## §1 — La forma del documento: qué va primero

Este es el orden fijo. **NUESTRA**, salvo donde se indique.

1. **Marca de naturaleza**, una línea al principio y otra al pie: «Documento de trabajo del arnés Despacho. No es un escrito para radicar.» **NUESTRA.** Con hechos numerados, tipografía de memorial y línea de anexos, el documento **se parece** a un memorial; esta línea es la contrapartida obligatoria.
2. **Bloque de identificación:** `Referencia` (partes y clase de proceso) · `Nro. Rad.` en extenso y abreviado · `Número interno` · `Archivo y versión` · `Fecha`. **ESTÁNDAR adaptado** (ANDJE, cap. VI num. 4). Adaptación declarada: ese numeral es la *salutación* de un memorial dirigido a un juzgado; tomamos las etiquetas, **nunca** el destinatario ni la firma.
3. **Apertura, 5 a 10 líneas:** qué hay, cuántas piezas, cuántas exigen decisión suya, qué falta. **Una sola capa de resumen.** No hay «respuesta breve» ni «encabezado de asunto» aparte: son el mismo objeto con otro nombre.
4. **Síntesis** — solo en entregas de hechos con más de 12 hechos. Un párrafo, **máximo 75 palabras, tope absoluto 100**. **ESTÁNDAR** (ANDJE 9.1.7, que fija esa cifra).
5. **Índice** — solo si hay más de 12 fichas. Una línea por ficha (§3).
6. **Cuerpo:** bloques con los mismos campos, en el mismo orden, siempre.
7. **Cierre:** lo pendiente y lo que falta, recogido en un solo sitio.

**Por qué este orden:** ella decide *antes* de leer. Lo que sirve para decidir va arriba; el volcado completo es material de consulta y va abajo. Es lo contrario de hoy, donde hay que recorrer 2.000 líneas para saber qué se encontró.

**Presupuesto de extensión. NUESTRA.** Apertura ≤ 10 líneas. Índice: exactamente una línea por ficha. Si el cuerpo pasa de 25 páginas, se parte en dos archivos por materia. **Regla de borrado:** ningún dato se emite dos veces; si algo ya está en el índice, no se repite como resumen dentro de la ficha. Sin este presupuesto, esta guía alarga el documento que venía a acortar.

## §2 — Qué se escribe y qué no, a nivel de caracteres

**Énfasis**
- Negrita **solo en títulos**. En el cuerpo, **cero énfasis tipográfico**. **ESTÁNDAR** (ANDJE: en el cuerpo «la negrita, el subrayado, la cursiva y, peor aún, la mayúscula sostenida resultan superfluos»).
- Prohibidos el **subrayado** y la **MAYÚSCULA SOSTENIDA en frases**. **ESTÁNDAR.**
- Etiquetas de estado en mayúscula (`POR VERIFICAR`, `HECHO VERIFICADO`): permitidas con dos topes — **máximo tres palabras** y **vocabulario cerrado**, nunca una oración. **NUESTRA.**
- Cursiva: no, salvo latinismos. **ESTÁNDAR.**

**Marcado**
- **Nada de sintaxis Markdown en la entrega**: ni asteriscos de negrita, ni tuberías de tabla. Medido: la misma tabla llega a Word con **0 tablas, 16 tuberías y 6 asteriscos literales**; en HTML llega como **1 tabla real de 6 celdas**. **NUESTRA (medido).**
- Títulos: `<h1>` / `<h2>` — Word los convierte en «Título 1» y «Título 2» y ella obtiene panel de navegación gratis. **Máximo dos niveles**, numeración decimal `1.` / `1.1.` **ESTÁNDAR** (ANDJE; el tercer nivel solo por encima de 15 páginas).
- Listas: `<ol>` cuando el orden importa o vamos a citar el ítem; `<ul>` cuando no. Frase introductoria siempre. Máximo dos niveles. **Una viñeta = una idea = un párrafo como máximo.** **ESTÁNDAR.** Medido: un guion en texto plano **no** se convierte en lista al pegar.
- Tablas: `<table>` con `<thead>` — el encabezado se repite al saltar de página, que con 76 filas es la diferencia entre una tabla y un amasijo. **Prueba de admisión: si una celda no cabe en una línea corta, eso no es una tabla, es una lista de fichas.** **ESTÁNDAR** (ANDJE: celdas extensas no transmiten la idea).
- Sangrado: **solo** la cita larga (§4). Sin sangría de primera línea. `[DUDOSO]` — no se leyó qué dice el cap. VI de la ANDJE sobre sangría y justificación.

**Redacción medible** — **ESTÁNDAR** (ANDJE), y son promedios, no topes por unidad:
- Oraciones: **20 palabras de promedio**. La fuente añade que el límite «es flexible». Un script que parta toda oración larga incumple la fuente que dice cumplir.
- Párrafos: **150 palabras de promedio**, **tope duro 250**, de tres a nueve oraciones.
- Títulos con **núcleo fáctico neutro y trazable** («Entrega de la mercancía — Orden de Trabajo No. 3»). Nunca la calificación jurídica («el demandado incumplió»): el sistema no califica. Nunca la etiqueta de carpeta («Hechos», «Pruebas»). **ESTÁNDAR, adoptado a medias y a propósito.**

**CSS mínimo — ESTÁNDAR** (ANDJE cap. VI): ancho de línea **65–90 caracteres** (`max-width`), cuerpo con **serifa, 11–13 pt**, títulos sin serifa, **máximo dos tipos de letra**, texto de tabla **no menor a 10 pt**, márgenes 2,7–3,1 cm. Tablas pequeñas sin bordes, grandes con bordes.

## §3 — Cómo se presenta una lista larga (el caso de las 76 fichas)

- **Umbral: más de 12 fichas obliga a índice.** **NUESTRA.**
- **Índice:** una línea por ficha, con los mismos campos y en el mismo orden — `ID · título · estado`. Va en `<table>` con `<thead>`. Sirve para triar sin abrir ninguna. **PRÁCTICA** (patrón *Table*, WorldCC).
- **No hay línea de resumen dentro de la ficha si hay índice.** Es el índice repetido. **NUESTRA.**
- **Orden: el del expediente, cronológico y consecutivo. No se reordena por estado de decisión.** El índice electrónico judicial exige orden cronológico y ella va a copiar bloques enteros; si reordenamos, reordena de vuelta. El estado se marca en un campo fijo, no moviendo filas. **ESTÁNDAR + NORMA** (Protocolo CSJ 7.4.2; CGP art. 82.5).
- **Dos identificadores distintos, y esto no es un detalle. NUESTRA.**
  - `ID interno` (`H-14`, `A-07`): **estable**, nunca se renumera ni se reutiliza entre versiones. Es lo que ella y el sistema citan.
  - `Número de hecho` para la demanda: **consecutivo, se recalcula** al intercalar. «Estable» y «consecutivo» son incompatibles en el mismo campo; separarlos es la única salida honesta.
- **Todas las fichas con los mismos campos etiquetados en el mismo orden, siempre.** Si un campo no tiene dato, se emite igual con su corchete (§4). La comparabilidad se destruye cuando cada ficha se estructura según lo que hubo a mano. **PRÁCTICA.**
- **Hechos: numerados y clasificados por materia**, un hecho por número, un solo conjunto de circunstancias por número. Es la forma exacta que la demanda le exige y le ahorra reformatear. **NORMA** (CGP art. 82.5: «debidamente determinado, clasificado y numerados» — literal, sin corregirle la concordancia).
- **Inventarios de más de 10 piezas:** además del detalle, una línea de resumen para radicar (cuántos archivos y en qué formatos) y la carpeta sugerida `AnexosMemorialAAAAMMDD`. **ESTÁNDAR** (Protocolo CSJ 7.1.1.1).
- **Cierre de un inventario de anexos:** `Anexos: tres (10 folios, un cheque y un folleto).` Cantidad en letras, folios en cifras, singular `Anexo:` si es uno. **ESTÁNDAR** (GTC 185, guía voluntaria de documentación *organizacional*: se adopta el formato, no se presenta como estándar judicial).

## §4 — Cómo se marca lo incierto, lo que falta y la cita textual

Es lo que distingue este producto. Tiene que verse sin buscarlo.

**El vacío. NUESTRA** (extensión por analogía de las normas de transcripción documental; se declara así, no como estándar).
- Se marca **en el sitio exacto**, entre corchetes, con vocabulario **cerrado**: `[ilegible]` · `[no consta en el documento]` · `[falta el folio]` · `[por verificar]`.
- Nunca una celda en blanco, nunca una fila omitida, nunca un relleno plausible.
- **Una sola gramática de corchete en todo el documento.** Por eso no hay casillas `[ ]` de revisión: colisionan con esta, y en Word no son marcables.

**La cita textual de un documento ajeno**
- **Cita larga:** `<p style="margin-left:36pt">`, **sin comillas** — la sangría ya significa «cita». **Nunca `<blockquote>`**: medido, pierde la sangría al pegar en Word incluso con CSS en línea. **ESTÁNDAR (RAE) + NUESTRA (medido).**
- **Cita corta:** «...» seguida del folio. **ESTÁNDAR (RAE).**
- Supresiones con `[...]`; aclaraciones nuestras entre corchetes; error del original conservado con `[sic]`, **nunca corregido en silencio**. **ESTÁNDAR (RAE).**
- No se reescribe ni se simplifica el término técnico que usa el documento ajeno. Se transcribe y, si hace falta, se glosa aparte.

**Derecho invocado por otro — apartado acotado**
- **El sistema no cita normas por su cuenta.** Nunca.
- Cuando un documento ajeno invoca una norma, se transcribe **literal**: «artículo 54 de la Ley 1437 de 2011». **Normalizarla** a `L. 1437/2011, art. 54` es alterar una transcripción. Si se añade la forma normalizada como índice, va **aparte y marcada como aportada por nosotros**, jamás sustituyendo la literal. **ESTÁNDAR + NUESTRA.**

**Cotejos que la salida debe hacer** (marcan desajustes; no concluyen nada)
- Anexos anunciados en el texto contra anexos listados, **en los dos sentidos**. **PRÁCTICA** (lo exige literalmente un juzgado de Medellín).
- Piezas exigidas para acompañar la demanda contra piezas presentes; la consecuencia de que falte una es la inadmisión. **NORMA** (CGP arts. 84 y 90.2) `[DUDOSO: verificar el articulado antes de programarlo]`. **La salida dice «falta la pieza X»; no cita el artículo** — citarlo sería derecho propio. **NUESTRA.**

## §5 — Formato de archivo y nombre

- **Extensión: `.html`.** Un solo formato para los ocho comandos. **NUESTRA (medido).** Razones, en orden: `.md` no tiene programa asociado y el doble clic abre el diálogo «¿Cómo quieres abrir este archivo?»; `.html` abre solo en Edge; y pegado en Word da tabla real, estilos de título y listas reales. `.rtf` queda descartado: Windows 24H2 ya no trae lector de RTF. *La medición de asociaciones es de la máquina del dueño; el comportamiento del convertidor de Word es propiedad de Word y sí es general.* `[DUDOSO en el equipo de ella]`
- Esto **no contradice** el «texto crudo y escueto» del encargo: escueto es *sin adorno*, no *sin forma*. El HTML es el envase que hace que la forma llegue intacta a Word.
- **`<meta charset="utf-8">` en el `<head>`, obligatorio.** Sin esa línea, medido: `Cesión Niño` se convierte en `CesiÃ³n NiÃ±o`. Se destruye cada tilde, cada eñe y cada cita textual. Es una línea, y sin ella el resto de la guía no sirve de nada. **NUESTRA (medido).**
- HTML **autocontenido**: CSS en un `<style>` o en línea, sin recursos externos, sin scripts.
- **Nombre, convención única. NUESTRA**, modelada en el num. 7.3 del Protocolo del CSJ (**ESTÁNDAR**): máximo 40 caracteres, sin espacios, sin guiones, sin tildes, sin caracteres especiales, mayúscula inicial en cada palabra, cero a la izquierda en dígitos sueltos, fechas `AAAAMMDD`.
  `ComandoCasoAAAAMMDDvNN.html` → `HechosPerezGomez20260827v01.html`
- **Una versión no se sobrescribe nunca:** `v02` es un archivo nuevo. Va a tener tres versiones abiertas a la vez y necesita saber cuál mira. **NUESTRA.**

## §6 — Un ejemplo, antes y después (material inventado)

**Antes** — lo que hoy emite un comando:

```
| Anexo | Descripción | Folios |
|---|---|---|
| 1 | **Contrato** de arrendamiento suscrito entre las partes, sin fecha visible en la última página, aportado por el cliente el 12 de marzo | 12 |
```

Lo que ella ve al pegarlo en Word: tuberías, guiones, dos asteriscos y **cero tablas**.

**Después:**

```html
<h2>1.1. Contrato de arrendamiento — folios 1 a 12</h2>
<table>
  <thead><tr><th>ID</th><th>Documento</th><th>Fecha</th><th>Folios</th><th>Estado</th></tr></thead>
  <tbody><tr><td>A-01</td><td>Contrato de arrendamiento</td><td>[no consta en el documento]</td><td>12</td><td>POR VERIFICAR</td></tr></tbody>
</table>
<p>Aportado por el cliente el 12 de marzo de 2026. La última página no trae fecha.</p>
<p style="margin-left:36pt">El arrendatario pagará el canon dentro de los cinco (5) primeros días [...] de cada mes.</p>
```

**Qué cambió, línea por línea:** la tabla llega a Word como tabla; las celdas caben en una línea y la prosa bajó a un párrafo aparte; el vacío está en su sitio y entre corchetes en vez de inventado; la cita va con sangría y sin comillas, con `[...]` en la supresión; el título trae el núcleo fáctico y el folio, sin calificar nada; y `POR VERIFICAR` es una etiqueta de dos palabras, no una frase en mayúsculas.

## §7 — Lo que NO se adopta, y por qué

- **Markdown como formato de entrega.** Ningún estándar jurídico lo respalda y Word lo pega literal (medido).
- **`.rtf`** (Windows ya no trae lector) y **PDF por «exigencia» de la Ley 2213.** Esa preferencia rige el escrito que **ella radica**, no nuestro documento de trabajo. El refutador tumbó la inferencia.
- **ISO 24495-1 y -2.** Nadie leyó el articulado: está tras pago. **No se nombra en el producto.** Afirmar que la entrega «sigue la ISO» sería afirmar conformidad con un texto desconocido. Sus cuatro preguntas se usan como checklist interno, sin atribuírselas.
- **El bloque estadounidense** (Federal Plain Language Guidelines —cuyo sitio fue retirado—, BLUF/AR 25-50 en fuente secundaria, memorando de Georgetown). Redundante: la ANDJE da las mismas cifras, en español, colombiana y verificable línea por línea. Mantenerlo añade riesgo de jurisdicción sin añadir una sola línea de salida.
- **FUID (Acuerdo 042 de 2002).** Obliga a entidades públicas y no aporta ninguna columna nueva. Vale como convergencia, no como regla.
- **Las columnas `Página Inicio`, `Página Fin`, `Tamaño` y `Origen`** del índice electrónico. Son metadatos de conservación del expediente **del despacho**; a ella no le sirven antes de radicar. Se conservan orden, nombre, fecha, folios y observaciones.
- **Títulos en forma de pregunta.** Vienen de guías dirigidas al ciudadano; la fuente colombiana escrita para operadores jurídicos dice lo contrario, y obligarla a una convención nueva es precisamente lo que hay que evitar.
- **Reordenar las fichas por estado de decisión.** Rompe el orden cronológico y la copia en bloque.
- **Casillas `[ ]`.** Dos gramáticas de corchete en un mismo documento, y en Word no son marcables.
- **Bloques de ancho fijo, separadores en texto plano, corte a 72 caracteres.** Residuos de la hipótesis «texto plano», muerta desde que la salida es HTML con fuente proporcional.
- **`<blockquote>`.** Pierde la sangría al pegar en Word, incluso con CSS en línea (medido).
- **Cuatro de las siete capas de resumen propuestas.** Apertura, respuesta breve, capa de acción y encabezado de asunto son el mismo objeto con cuatro nombres. Queda una.
- **Manifiesto de Legal Design** (no cambia una línea) y **patrón Accordion** (exige plegar y hacer clic; el documento tiene que funcionar en Word y en papel).
- **«20 palabras» y «150 palabras» como topes duros.** La fuente dice promedio y declara el límite flexible. Programarlo como tope incumple la fuente que se invoca.
- **La cita atribuida al DNP sobre «una idea por frase» y «párrafos de cinco líneas».** No existe en ese documento: cero ocurrencias verificadas. No se usa, ni siquiera reformulada.
