# Primera ejecución real del arnés — hallazgos

**Fecha:** 2026-08-26.
**Material:** una demanda de familia real y sus anexos, aportada por la profesional que va a usar el producto. **El material NO está en este repositorio ni lo estará**: se trabajó en directorio temporal, fuera de git. Aquí solo constan hallazgos anonimizados.
**Método:** cinco comandos ejecutados sobre el caso por agentes que **no sabían que era una prueba** —recibieron el `SKILL.md` y la carpeta, con la petición redactada como la haría ella—. Si lo hubieran sabido, se habrían esforzado más de lo normal y el resultado no diría nada sobre el uso real.

> **Contexto: hasta este día el producto solo se había leído.** Diecinueve hallazgos corregidos por revisión, y ni una sola pasada sobre un caso. Todo lo de abajo es lo primero que el proyecto sabe por medición y no por argumento.

---

## 1. El truth set — por qué esta prueba vale

El PDF de anexos venía **escaneado**: de sus 39 páginas, **25 no contienen una sola letra de texto extraíble**. Eso da un instrumento que no depende del criterio de nadie: **cualquier afirmación sobre el contenido de esas páginas es una fabricación**, sin margen de interpretación.

Un caso sintético escrito por nosotros no habría dado esto. Es la razón por la que material real era necesario.

---

## 2. HECHO MEDIDO — el 64% del material probatorio no es citable

| Documento | Páginas | Sin texto extraíble |
|---|---|---|
| Demanda | 17 | **0** |
| Anexos | 39 | **25 (64%)** |

**Confirma el riesgo H-16 que estaba diagnosticado a ciegas**, y lo confirma con la peor distribución posible: lo legible es el escrito de parte, y lo ilegible es **la prueba**. Justo al revés de lo que conviene.

**Consecuencia de producto, no de implementación:** un expediente colombiano típico llega escaneado. Cualquier comando que prometa coordenada exacta —página, cláusula, minuto— la va a poder dar para el escrito y **no** para los anexos. La regla añadida el 2026-08-25 (declarar lo que no se puede leer, jamás estimar una coordenada) deja de ser una precaución teórica: es la ruta principal del material.

**RIESGO abierto:** sin capa de texto no hay OCR en el flujo. Está POR VERIFICAR qué puede hacer la plataforma con un escaneado, y es ahora la comprobación más urgente de la lista.

---

## 3. HECHO MEDIDO — cuánto tarda cada comando

Sobre un caso de 56 páginas, un comando por vez:

| | Tiempo |
|---|---|
| Comando más rápido | **4 min 43 s** |
| Intermedios | 11 min 30 s · 13 min 39 s |
| Comando más lento | **20 min 06 s** |

**Lo que esto significa para ella.** No es espera frente a la pantalla —el anfitrión trabaja en segundo plano— y la comparación honesta no es contra cero, sino contra hacerlo a mano, que son horas. Pero **hay que decírselo**: una espera de quince minutos sin aviso se lee como que el programa se rompió.

**Pendiente:** la guía debe declarar cuánto tarda cada comando y cuáles son los lentos.

---

## 4. VERIFICADO — dos correcciones del día anterior funcionaron en su primera prueba

| Corrección | Prueba | Resultado |
|---|---|---|
| **H-05** — la cadena rota: nadie escribía la hoja de hechos, y dos comandos la consumían | Se pidió un borrador sin que existiera ningún archivo terminado en ` - REVISADO` | **`redactar-escrito` se negó a redactar** y entregó un archivo explicando por qué. Es exactamente la conducta que se le programó el día anterior |
| **H-13** — la tabla «lista para pegar» salía como Markdown dentro de un `.txt` | Se pidió el inventario de anexos | **Produjo un `.docx` real** |

Son las dos únicas correcciones del lote que podían verificarse sin leer el contenido. Las demás dependen del informe de evaluación.

---

## 5. SEÑAL DE ALARMA — el tamaño de la salida

| Salida | Peso |
|---|---|
| Hechos | **125 KB** |
| Cronología | 34 KB |
| Revisión de la demanda | 35 KB |
| Inventario de anexos | 51 KB (`.docx`) |

125 KB de fichas son del orden de cuarenta a sesenta páginas para revisar una por una, con casilla `SÍ`/`NO`/`A MEDIAS` en cada una.

**El riesgo, dicho sin rodeos: si el producto le devuelve más papel del que le quitó, no la está ayudando — la está mudando de trabajo.** Y el modelo de autoridad humana lo agrava: cada ficha exige una decisión suya, así que el coste de revisión crece con la exhaustividad del método. Un método más completo produce un producto peor si nadie puede revisarlo.

**No está juzgado todavía.** Puede que un caso de custodia con tres audiencias de conciliación tenga de verdad esa cantidad de hechos. Pero es el primer candidato a fallo de producto que ninguna lectura del método habría revelado, y hay que resolverlo antes de ponerlo en sus manos.

**Líneas de solución a evaluar, ninguna decidida:** entregar los hechos por tandas priorizadas en vez de todos de una vez; separar el núcleo del caso de lo accesorio; o revisar por excepción —ella aprueba en bloque y solo mira las fichas marcadas como dudosas—. La tercera choca con el principio de autoridad humana y hay que pensarla con cuidado.

---

## 6. Lo que queda por saber

Pendiente del informe de evaluación en curso: si alguien citó una página ilegible (**la pregunta central**), si las citas textuales coinciden palabra por palabra, si se coló derecho inventado, si se calcularon días entre fechas, y si la salida le sirve de verdad a una abogada.

---

## 7. Lo que esta ejecución deja para siempre

El proyecto no tenía **ningún** fixture ejecutable ni forma de medir si una versión de skill mejora a la anterior. Ahora tiene un caso real con **truth set conocido**: 25 páginas cuya mención es, por construcción, una fabricación. Cualquier versión futura de los métodos puede medirse contra él.

**Condición de uso:** el material vive fuera del repositorio y no se distribuye. Lo reutilizable es el procedimiento y las 25 páginas de referencia, no los documentos.
