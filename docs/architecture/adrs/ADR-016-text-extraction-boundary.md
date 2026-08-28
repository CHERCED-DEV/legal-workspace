# ADR-016 — Ingesta de material sin capa de texto: el OCR audita la lectura, no la reemplaza

## Estado

Proposed

## Contexto

`ESTADO-DEL-PROYECTO.md` §1.1 registró una colisión verificada y no resuelta: los cuatro comandos que exigen coordenada exacta chocan con que **los PDF escaneados sin texto extraíble no son citables**. H-16 la registró como hallazgo vivo. Ninguno de los dos decía qué hacer.

El pase real la puso en su forma más dura: **las 23 piezas del expediente [radicado del expediente] eran fotografías de papel. Ninguna tenía capa de texto.** Todo el trabajo se hizo con el modelo leyendo imágenes y transcribiendo a ojo. Cada cifra del expediente quedó marcada «por comprobar», y con razón.

El 2026-08-28, con autorización, se probó OCR local (RapidOCR, `pip install rapidocr-onnxruntime`, sin binario externo). Lo medido:

| Medida | Resultado |
|---|---|
| Texto extraído | 20.164 caracteres ≈ 5.041 tokens, frente a ~225.000 de lectura de imagen |
| Tiempo | 272 s sobre 46 mitades · 145 s sobre 23 páginas |
| **Identificadores críticos** | **12 de 12 exactos** — dos matrículas, cuatro cédulas, dos tarjetas profesionales, radicado, PQRS, escritura |
| Extracción del cuerpo | **Parcial, y sin aviso.** En el auto perdió la mayor parte del texto |
| Diacríticos | Rotos: `C6digo`, `aplicaci6n`, `senora` |
| Correcciones intentadas | Resolución de detección 960 y 1600, y tres preprocesados. **Ninguna cambió el resultado** |

Y el hecho que ordena este ADR: **cuatro frases que el modelo sí había leído no aparecieron en el OCR** —«ley 1806», «afectación indebida de bienes de uso público», «19 de agosto de 2026», «artículo 223»—, y el OCR capturó las colas exactas de tres de ellas (`publico.`, `despacho.`, `querella.`). No las contradijo: **no las leyó, y no avisó de que no las había leído**.

> Un sistema que hubiera confiado en esa salida habría concluido que **el auto no fija fecha de audiencia**. No es ruido: es una ausencia que se lee como un hecho.

## Decision

### 1. Dos clases de derivado textual, que no son intercambiables

El dominio hoy tiene una sola noción de representación derivada. Se distinguen dos, y el productor viaja siempre con el texto:

| Clase | Productor | Reproducible | Diacríticos | Uso |
|---|---|---|---|---|
| `OCR_EXTRACTION` | Un programa, con `recipe.tool` y `recipe.version` | **Sí**: mismo insumo, misma receta, mismo texto | Depende del modelo, y se declara | Cotejo, búsqueda |
| `MODEL_READING` | El modelo leyendo la imagen | **No** | Correctos | Comprensión, cita provisional |

**Ninguna de las dos es el original.** Una tercera regla, ya vigente en `hechos-con-prueba` §Fase 1 para transcripciones de audio, se extiende aquí: quien produjo el derivado se declara siempre, y si fue un programa, cuál.

### 2. El OCR audita la lectura; no la reemplaza

**Esta decisión corrige una recomendación anterior del 2026-08-27**, que afirmaba que el OCR dividiría el coste por siete. Es falso para fotografías de papel: el modelo tiene que seguir leyendo las páginas y ahí está el gasto.

Lo que el OCR compra, por ~5.000 tokens y unos minutos, es **corroboración independiente**. Esa, y no el ahorro, es su justificación.

### 3. La ausencia en el OCR no es información sobre el documento

Invariante duro, y es el motivo principal de este ADR. Todo consumidor —skill, Core o persona— trata «no aparece en el texto extraído» como **«no leído»**, jamás como «no está en el documento». El artefacto de texto extraído lleva esa advertencia **en su cabecera**, no en una nota al pie.

### 4. Cotejo obligatorio de identificadores

Todo dato numérico que sostenga un hecho —cédula, matrícula, radicado, tarjeta profesional, número de escritura, cuantía, fecha en cifras— se contrasta entre `OCR_EXTRACTION` y `MODEL_READING`.

- **Coinciden:** el dato sigue siendo *por comprobar* contra el original, pero deja de depender de una sola lectura, y así se declara.
- **Difieren:** el dato entra en «qué comprobar primero» **con prioridad máxima**, con las dos versiones a la vista. No se elige ninguna.
- **El OCR no lo leyó:** se declara que la corroboración no fue posible. **No se cuenta como coincidencia.**

### 5. Citabilidad explícita, y prohibición de cita literal desde un OCR no citable

Todo `OCR_EXTRACTION` lleva un campo `citable` con su razón. Un reconocedor que no preserva tildes ni la eñe produce texto **no citable en español**: sirve para buscar, no para citar. **Ninguna cita literal de ninguna salida puede provenir de un texto marcado no citable.**

### 6. Cobertura declarada, aunque no se sepa medir

Cada página dice cómo se leyó y qué se sabe de la completitud de su extracción. Si no hay métrica calibrada —hoy no la hay: la que se probó marcó 21 de 23 páginas porque cuenta como tinta los membretes y las sombras— **se declara «cobertura no medida»**. Lo que no se hace nunca es omitir la pregunta.

### 7. Se registra el modo de captura, porque predice el fallo

`FOTOGRAFIA_DE_PAPEL`, `ESCANEO_PLANO`, `PDF_NATIVO`. En el pase, el modo de captura explicó mejor el fallo del OCR que cualquier parámetro del reconocedor. Es dato de ingesta, no metadato decorativo.

### 8. Las cajas del OCR no entran en el locator

Se respeta ADR-011 §9 sin excepción: **sin bounding boxes en V0**. Las cajas que devuelve el reconocedor son de uso interno —métrica de cobertura, diagnóstico— y **nunca** viajan en un `EvidenceFragment`. Son coordenadas del render con apariencia de coordenadas del original, que es exactamente lo que ADR-011 prohíbe.

### 9. Cambiar de reconocedor produce una versión nueva

Aplicación directa de ADR-011 §7 y §8: `recipe.tool`, `recipe.version` y `recipe.params` obligatorios; cambiar el modelo de reconocimiento **no sobrescribe** el texto anterior, produce otra versión, y ambas se retienen mientras algún fragmento las referencie.

### 10. El OCR no cambia qué es citable del original

La coordenada de cita sigue siendo la del original —documento y página—, con independencia de que el texto se haya obtenido por OCR, por lectura del modelo o por las dos. El OCR **no convierte en citable** un documento que no lo era: lo hace **buscable**, y hace **cotejables** sus cifras.

## Invariantes derivados

1. **Ningún consumidor infiere ausencia en el documento a partir de ausencia en el texto extraído.**
2. **Todo derivado textual declara su productor**: un programa —y cuál, con versión— o el modelo.
3. **Todo `OCR_EXTRACTION` lleva `citable` explícito con su razón.**
4. **Ninguna cita literal proviene de un texto marcado no citable.**
5. **Las cajas del reconocedor jamás entran en un `EvidenceFragment`.**
6. **Todo identificador numérico que sostenga un hecho lleva su estado de cotejo**: coincide, difiere, o no fue posible.
7. **Toda página declara su cobertura**, aunque el valor sea «no medida».
8. **Todo material de imagen declara su modo de captura.**
9. **El texto extraído nunca sustituye al original como fuente de la cita.**
10. **Cambiar de reconocedor produce versión nueva; nunca sobrescribe.**

## Consecuencias positivas

- Convierte la colisión de `ESTADO-DEL-PROYECTO.md` §1.1 y H-16 en una regla operativa, en vez de una advertencia.
- Añade el **primer control del producto que no depende de que el modelo haya leído bien**. En el pase corroboró 12 de 12 identificadores.
- Hace buscable un expediente que llegó como 23 fotografías, sin tocar los originales.
- El invariante 1 cierra un modo de fallo silencioso que ningún otro control detectaba.
- Deja escrita la corrección de una recomendación anterior, con la medición que la desmiente.

## Consecuencias negativas

- **Añade una dependencia** (`rapidocr-onnxruntime`, ~80 MB de modelos) que hay que versionar, distribuir y actualizar bajo ADR-012.
- **Aumenta el trabajo por página**: dos lecturas y un cotejo donde antes había una lectura.
- **Confianza falsa:** «12 de 12 coinciden» se lee como «el expediente está verificado». No lo está. La redacción de la salida tiene que impedirlo, y es difícil.
- La cobertura queda declarada como **no medida**, que es honesto y **no es un control**. Mientras siga así, el invariante 1 es lo único que protege, y depende de que cada consumidor lo respete.
- Los diacríticos rotos hacen el texto extraído inservible para lo que un usuario esperaría de él —copiar y pegar—, y eso hay que explicárselo cada vez.

## Alternativas consideradas

### (a) Que el OCR reemplace la lectura del modelo
**Descartada por medición.** Perdió cuatro frases que sí estaban, entre ellas la fecha de la audiencia, sin avisar. El ahorro habría sido real; el modo de fallo, inaceptable.

### (b) Seguir solo con lectura del modelo, como hasta ahora
Descartada: deja todo dato numérico dependiendo de una sola lectura no reproducible, y no hay ningún control que lo detecte.

### (c) Tesseract con `spa.traineddata`
No descartada: probablemente resuelve los diacríticos. Exige instalar un binario en la máquina de la abogada, lo que la mete en ADR-012. **Es la primera prueba pendiente.**

### (d) OCR en la nube
Descartada: enviar el expediente a un tercero es un cambio de frontera de confianza que ADR-001 no admite sin decisión propia.

### (e) Exigir escaneo plano en vez de fotografía
**No descartada, y es la más barata de todas.** No es técnica: es de flujo de trabajo. Un escaneo plano probablemente arregla más que cualquier ajuste del reconocedor. Requiere pedírselo a quien aporta el material, que no siempre es la usuaria.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Una ausencia del OCR se lee como ausencia del documento | Invariante 1 + advertencia en la cabecera del artefacto |
| «12 de 12» se lee como expediente verificado | La salida dice que sigue siendo *por comprobar* contra el original |
| El texto no citable acaba citado | Invariante 4; `citable` explícito en el artefacto |
| La dependencia se rompe en la máquina de ella | Fallo declarado: si no hay OCR, se dice y se trabaja sin cotejo |
| La métrica de cobertura se da por buena sin calibrar | Se declara «no medida» hasta que exista una calibrada |

## Validación / pruebas necesarias

1. **Calibrar la métrica de cobertura.** La probada marca 21 de 23 páginas y por tanto no discrimina. Sin esto, la decisión 6 se queda en declaración.
2. **Probar Tesseract con `spa.traineddata`** sobre las mismas 23 fotografías y medir si los diacríticos se arreglan.
3. **Medir el mismo expediente escaneado plano**, para cuantificar cuánto del fallo es del reconocedor y cuánto del modo de captura.
4. **Prueba adversarial del invariante 1:** dar a un lector un texto extraído incompleto y comprobar si concluye que algo no está en el documento.
5. Ejecutar el cotejo de identificadores sobre un caso con un error real sembrado, y comprobar que el desacuerdo se reporta.

## Preguntas pendientes

1. **¿Qué reconocedor para español?** **Parcialmente respondida el 2026-08-28.** Se adoptó un PP-OCRv5 cuyo vocabulario tiene `ñ` minúscula y las tildes: 124 caracteres acentuados donde antes había ~0, y **12 de 12 identificadores sin regresión**. Sigue faltando `Ñ` mayúscula, `Ú`, `¿` y `¡`; el modelo latino que los tiene no fue alcanzable desde esta máquina. Ver `tools/preparar-material/modelos/PROCEDENCIA.md`.
2. **¿El OCR corre siempre, o solo cuando el material no tiene capa de texto?** Con PDF nativo el cotejo pierde sentido: el texto ya es el del documento.
3. **¿Dónde vive el texto extraído** — zona 2 o zona 3 de ADR-012? Hoy se dejó en `2-Borradores/`, que es zona 2, y probablemente esté mal: es un derivado de material incorporado.
4. **¿El cotejo de identificadores es un comando, un paso de ingesta, o parte de `inventario-de-anexos`?**
5. ¿Qué se hace cuando OCR y modelo difieren **y el original no se puede consultar**?

## Relaciones con otros ADRs

- **ADR-011** (locators): este ADR es su aplicación al caso sin capa de texto. Respeta §7 (metadatos de derivado), §8 (regeneración aditiva) y §9 (sin bounding boxes) sin excepción, y **no añade ningún tipo de selector**.
- **ADR-003** (modelo epistémico): las dos clases de derivado textual son dos productores distintos de la misma clase de material; ninguna sube el estado de nada.
- **ADR-006** (incorporación): el OCR corre sobre material ya incorporado y nunca lo modifica.
- **ADR-001** (frontera de confianza): la alternativa (d) queda descartada por ella.
- **ADR-012** (distribución): la dependencia del reconocedor y sus modelos entra en el modelo de actualización.
- **ADR-014** (forma de entrega): el PDF consolidado y el texto extraído son dos derivados del mismo material, con reglas distintas y ninguna de las dos citable.
