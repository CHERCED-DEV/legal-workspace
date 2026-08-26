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

---

## 8. HECHO MEDIDO — el coste, y es el problema más serio del producto

**Planteado por el dueño el 2026-08-26:** *"la idea es que no se vaya a derrochar en tokens, que ella lo pueda utilizar con un plan Pro… que le pueda servir para todo un día de trabajo. Aquí hemos estado haciendo un monstruo… si no, esto no va a ser rentable."*

Consumo real de la ejecución de hoy, por comando, sobre un caso de 56 páginas:

| | Turnos | Salida | Contexto releído |
|---|---:|---:|---:|
| Comando más barato | **16** | 19.223 | 0,9 M |
| | 37 | 48.441 | 2,7 M |
| | 30 | 64.332 | 2,9 M |
| Comando más caro | **97** | 75.524 | 12,0 M |

**Total de la prueba: ~3 millones de tokens facturables y 50,8 M de contexto releído.**

### Dónde está el derroche

**El número que importa no es la salida: son los turnos.** Entre el comando barato y el caro hay 6× de diferencia en turnos (16 vs 97) y 13× en contexto releído. **Cada turno vuelve a arrastrar todo el contexto acumulado**, así que el coste crece con el cuadrado del trabajo, no linealmente. Un método que manda «lee todo antes de proponer nada» sobre 56 páginas, con un `SKILL.md` de 300+ líneas y un archivo de formato de 456 más, paga ese contexto en cada uno de sus turnos.

Tres causas, por orden de peso:

1. **Los métodos son largos y se releen enteros en cada turno.** Seis skills de 270 a 373 líneas, más `FORMATO-DE-SALIDA.md` con 456. Se escribieron optimizando exhaustividad, sin mirar el coste ni una vez.
2. **El procedimiento es exhaustivo por diseño.** Fases obligatorias, autoevaluaciones de 20+ preguntas, releer cada anclaje. Todo eso es calidad, y todo eso son turnos.
3. **La salida es desproporcionada** (§5): producir 125 KB cuesta, y además obliga a ella a revisarlos.

### Lo que NO se puede afirmar todavía

**No se puede traducir esto a «le alcanza para N horas de Pro».** Los límites del plan no están publicados en tokens —solo consta que Pro da *"at least five times the usage"* frente al gratuito— y además estas cifras vienen de agentes de orquestación, que cargan trabajo de herramientas que ella no tendrá. **El orden de magnitud es indicativo y preocupante; la conversión a jornadas sería inventada.**

### Líneas de ataque, ninguna decidida

- **Adelgazar los métodos** sin perder el método: lo que hace bueno a un skill es la distinción bien puesta, no la extensión. Hay margen.
- **Bajar los turnos**, que es la palanca real: menos idas y vueltas por pasada.
- **Graduar el esfuerzo**: no todo caso necesita la pasada exhaustiva. Una pasada rápida y una a fondo, y que ella elija.
- **Acotar la salida** (§5), que abarata a la vez el producir y el revisar.

**Medir antes y después es obligatorio**, y ahora se puede: el caso con truth set de §1 sirve también de banco de pruebas de coste.

---

## 9. VEREDICTO DE LA EVALUACIÓN — la veracidad aguantó; el volumen no

Comprobado **exhaustivamente, no por muestreo**, por un evaluador independiente y confirmado por una verificación propia hecha aparte con otro método.

### 9.1 Lo que aguantó

| Comprobación | Resultado |
|---|---:|
| Contenido atribuido a alguna de las 25 páginas ilegibles | **0** |
| Páginas ilegibles declaradas como tales, una por una | **25 de 25** |
| Fragmentos citados entre comillas contrastados contra el material | **647** |
| Anclajes de página verificados contra *la página citada* | 104 + 81 + 54, **1 solo error** |
| Derecho sustantivo propio · cálculo de días · escrituras fuera de `2-Borradores/` | **0 · 0 · 0** |
| `1-Documentos recibidos/` tras la ejecución | **byte-idéntico** |

**El fallo más peligroso del producto —la cita fantasma— no se produjo ni una vez**, teniendo 25 ocasiones servidas para producirlo. Es el resultado más importante que el proyecto ha obtenido, y solo era obtenible con material real.

**Conducta emergente que nadie programó:** un comando usó los metadatos de las páginas legibles para deducir qué falta — *«dice "Página 1 de 2"; la segunda página llegó sin texto»*, *«el encabezado dice "8 mensajes" y el pie dice "1/3"»*. Convirtió una limitación técnica en un inventario de material faltante, que es exactamente lo que una abogada necesita.

**`redactar-escrito` se negó a redactar, y por la razón correcta.** La corrección H-05 funcionó en su primera prueba real.

### 9.2 Lo que falló — y es de producto, no de veracidad

**~4.000 líneas de salida a partir de 31 páginas legibles.** El comando de hechos produjo **76 fichas**, cada una con su casilla `SÍ`/`NO`/`A MEDIAS`. Y entre ellas conviven una contradicción central del expediente y el lugar de expedición de una cédula: **ambas exigen la misma decisión formal de ella**.

**El cuello de botella del sistema, que ningún método menciona:** hasta que ella marque las 76 fichas y renombre el archivo a ` - REVISADO.md`, `redactar-escrito` está bloqueado **por diseño**. La autoridad humana, que es la garantía del producto, es también su tapón. Cuanto más exhaustivo el método, más caro el tapón.

Además, cuatro listas casi idénticas de material faltante repartidas en cuatro salidas distintas, sin que nadie las consolide.

### 9.3 Hallazgo de método — una pregunta que el producto no contesta

Ante el mismo texto dañado por la extracción del PDF, **dos comandos resolvieron al revés**: uno reparó la cita en silencio (`«31 y 1 de enero»`) y otro la transcribió tal cual y anotó el defecto (`«31y 1 de enero» [así, sin espacio]`).

Ninguno de los dos hizo nada malo, y ninguna reparación cambió el sentido. **El problema es que el método no dice cuál es la conducta correcta**, y en un producto cuya promesa es la cita literal, eso no puede quedar al criterio de cada pasada. **DECISIÓN PENDIENTE.**

### 9.4 Lo que esto significa para el rumbo

El producto **no tiene un problema de fiabilidad: tiene un problema de proporción**. Eso es una noticia buena, porque la fiabilidad es lo caro de conseguir y lo que no se puede reparar después; la proporción se ajusta.

Y reordena la prioridad: **acotar la salida y el coste (§5 y §8) pasa a ser el trabajo principal**, por delante de añadir comandos nuevos.
