# ADR-017 — Transcripción de audio: el reconocedor no omite, inventa

## Estado

Proposed

## Contexto

`ADR-016` fijó el límite del material sin capa de texto y su invariante 1 dice que **la ausencia en el OCR no es información sobre el documento**: el OCR **falla callándose**. Ese ADR nació de una medición sobre 23 fotografías del expediente [radicado del expediente].

El audio plantea el mismo problema de frontera y **el modo de fallo es de signo contrario**. La investigación del 2026-08-28 sobre reconocimiento de voz local en español lo dejó medido:

**Koenecke et al., «Careless Whisper: Speech-to-Text Hallucination Harms», FAccT 2024** (arXiv 2402.08021):

- **~1 % de las transcripciones contenían frases o sentencias enteras alucinadas** que no existían en ningún lugar del audio.
- **38 % de esas alucinaciones incluían daño explícito**: perpetuar violencia, fabricar asociaciones inexactas, o **implicar autoridad falsa**.
- Se concentran en **tramos largos de habla no vocalizada**. Una audiencia está llena de silencios, pausas procesales y ruido de sala.

> **En un expediente jurídico, «implicar autoridad falsa» es el peor resultado imaginable de una herramienta.** Y a diferencia de una omisión, **no se detecta leyendo**: el texto que inventa un reconocedor es fluido, gramatical y verosímil.

Tres hechos más, del mismo estudio de fuentes:

1. **Las señales de confianza existen pero no cubren este fallo.** Los motores exponen probabilidad media por segmento, probabilidad de no-habla y ratio de compresión. Detectan bien **el bucle repetitivo y el silencio**; detectan mal **el invento fluido**, que puede salir con confianza alta.
2. **La diarización no permite atribuir.** El error de atribución en los conjuntos de datos parecidos a una sala es de **17 % a 20 %** del tiempo de audio: del orden de una quinta parte queda asignada al hablante equivocado, sin decir cuál quinta parte.
3. **Las marcas de tiempo sí resuelven contra el original** —son desplazamientos en segundos sobre el audio de entrada—, pero **el mapeo ha tenido errores reales cuando el filtro de voz está activo**, y ese filtro es justamente el que hay que activar para contener la alucinación.

`ADR-011` §Riesgos nº 1 quedaba `POR VERIFICAR` sobre si un proveedor entrega marcas de tiempo referidas al original. **Para la vía local, este ADR lo resuelve** — con la condición del punto 3.

## Decision

### 1. La transcripción es una representación derivada, y el original es la grabación

Se aplica sin excepción `ADR-011` §7: `recipe.tool`, `recipe.version` y `recipe.params` obligatorios, con su huella y su procedencia. **La grabación es el `Source`; la transcripción no lo es nunca.**

Regla ya vigente en `hechos-con-prueba` §Fase 1, elevada aquí a decisión: **quien produjo la transcripción se declara siempre** — una persona, o **un programa y cuál, con su versión**. Un programa de transcripción es un productor de material como cualquier tercero, y sus errores tienen forma propia: nombres propios, cifras y apellidos poco frecuentes.

### 2. El invariante que ordena este ADR, y es el espejo invertido de ADR-016

> **Ninguna cita literal puede provenir de un segmento de audio no cotejado contra el original.**

`ADR-016` protege contra una ausencia que se lee como un hecho. **Aquí hay que protegerse de lo contrario: una presencia que no ocurrió.** Un dato decisivo que solo salga de la transcripción **se comprueba escuchando ese minuto**, igual que una cita de documento se comprueba abriendo su página.

### 3. Las señales de confianza son un filtro, no una garantía

Se registran por segmento y se usan para marcar tramos dudosos. **Y se declara, en la propia salida, qué detectan y qué no:** detectan bucle y silencio; **no detectan el invento fluido**.

**Prohibido** presentar un segmento como fiable porque su confianza es alta. Está permitido —y es obligatorio— marcar como dudoso el que la tiene baja.

### 4. Sin diarización fiable, no se atribuye ninguna frase a nadie

Regla ya escrita para la transcripción de la audiencia del expediente [radicado del expediente] y elevada aquí:

> **Si la transcripción no distingue las voces, no se atribuye ninguna frase a nadie.** Se escribe que no las distingue. Deducir quién habla por el contenido es inferencia.

Y con el error medido de 17-20 %, **la diarización automática de hoy no cuenta como distinción de voces para efectos de atribución.** Sirve para navegar el registro, no para afirmar quién dijo qué. Esto **confirma** la decisión ya tomada en el Glosario §4 (*v0 no modela diarización y no se afirma su fiabilidad*) y no la levanta.

### 5. Se ancla al segmento, nunca a la palabra

`ADR-011` §Riesgos nº 4 dejó el alineamiento por palabra como hipótesis no verificada. La investigación lo respalda con una razón concreta: **el alineamiento por palabra falla precisamente en cifras, fechas en números y cuantías** — que es lo que más se cita en un expediente.

**Ninguna regla del producto puede depender de la marca de palabra.**

### 6. El audio no sale de la máquina

Una grabación de audiencia contiene voces de terceros identificables que no autorizaron nada. **El reconocimiento se hace localmente.** Enviar el audio a un servicio de terceros es un cambio de frontera de confianza que `ADR-001` no admite sin decisión propia.

**Y el argumento no es de coste.** Está medido: 150 horas de audio al año costarían del orden de 25 dólares en un servicio por minuto. **El ahorro no justifica nada; la confidencialidad sí, y se sostiene sola.** Es la misma conclusión a la que `experiments/transcription-spike/README.md` había llegado el 2026-08-24.

### 7. El refinado del texto es otra representación, y no corrige contenido

Si se produce una versión legible de la transcripción —puntuada, con párrafos, con marcas de hablante—:

- **La transcripción cruda es inmutable y es la que vale.**
- El refinado es **otra representación derivada**, con su receta y su versión (`ADR-011` §8: regenerar produce versión nueva, nunca sobrescribe).
- **Toda cita resuelve contra la cruda, con su minuto.** Nunca contra la refinada.
- **El refinado no corrige contenido.** No «arregla» lo que alguien dijo mal, porque lo que alguien dijo mal es el dato.

**Por qué es decisión y no detalle:** un texto limpiado se lee mejor, se cita más cómodo, y semanas después nadie recuerda que la frase original decía otra cosa. Es el mismo mecanismo que hace peligroso a `redactar-escrito`.

### 8. Cotejo por redundancia cuando el dato es decisivo

Aplicación del mecanismo de `ADR-016` §4 al audio: cuando un dato sostiene un hecho, se contrasta **entre dos derivados independientes** — dos motores distintos, o motor y escucha humana. **Coincidencia no significa verdad; divergencia sí significa problema**, y el dato pasa a comprobación prioritaria.

### 9. Se registra el modo de captura de la grabación

Sala abierta · micrófono cercano · registro de sistema de audiencia · llamada. Igual que `ADR-016` §7 registra el modo de captura de la imagen, y por la misma razón: **predice el fallo mejor que cualquier parámetro del motor**.

## Invariantes derivados

1. **Ninguna cita literal proviene de un segmento de audio no cotejado contra el original.**
2. **Toda transcripción declara su productor** —persona, o programa con su versión— y sus parámetros.
3. **La grabación es el `Source`; la transcripción nunca lo es.**
4. **Si la transcripción no distingue voces, ninguna frase se atribuye a nadie**, y la diarización automática actual no cuenta como distinción para atribuir.
5. **Ningún anclaje depende de la marca de palabra.** El segmento es la coordenada.
6. **Ninguna salida presenta un segmento como fiable por su confianza alta.**
7. **El refinado nunca sustituye a la cruda como origen de una cita**, y no altera contenido.
8. **El audio no sale de la máquina** sin decisión expresa que modifique ADR-001.
9. **Toda grabación declara su modo de captura.**
10. **Cambiar de motor o de modelo produce versión nueva; nunca sobrescribe.**

## Consecuencias positivas

- Cierra la frontera que faltaba: `ADR-016` cubre lo que se lee, este cubre lo que se oye, **y nombra que los dos fallan de manera opuesta**.
- Resuelve, para la vía local, el riesgo nº 1 de `ADR-011` que llevaba abierto.
- Permite tocar material —audiencias grabadas— que hoy el producto no puede procesar en absoluto.
- El invariante 1 cierra un modo de fallo que **ninguna señal de confianza detecta** y que, a diferencia de la omisión, es indetectable leyendo.

## Consecuencias negativas

- **Encarece el uso del audio en trabajo humano**, no en cómputo: el invariante 1 obliga a escuchar los minutos decisivos. El coste real de esta decisión es tiempo de la profesional.
- **Añade dependencias pesadas** —motor, modelos de varios cientos de megabytes, quizá GPU— que hay que versionar y distribuir bajo `ADR-012`.
- **La diarización queda fuera**, y con ella la comodidad de tener el texto ya repartido por hablante. Es la consecuencia que más va a costar defender ante quien vea la herramienta funcionando.
- **El invariante 1 es difícil de hacer cumplir**: nada impide técnicamente citar un segmento sin haberlo escuchado. Depende de la disciplina de cada salida, igual que ADR-016 §3.

## Alternativas consideradas

### (a) Reconocimiento en la nube
Descartada por `ADR-001`. El audio lleva voces de terceros identificables. El coste habría sido menor y el trámite más simple; la frontera de confianza no lo admite.

### (b) Confiar en las señales de confianza como garantía
Descartada por medición: la alucinación fluida puede salir con confianza alta. Un umbral es un filtro útil, no una prueba.

### (c) Usar diarización automática para atribuir
Descartada por medición: 17-20 % de error en escenarios de sala. Se conserva como ayuda de navegación, marcada como tal.

### (d) Anclar por palabra
Descartada: falla en cifras y fechas, que es exactamente lo que se cita.

### (e) Prohibir el audio hasta tener transcripción humana
Descartada por desproporcionada. Con el invariante 1 y el cotejo del §8, el audio es utilizable. Prohibirlo dejaría fuera material que a menudo es el único registro de lo ocurrido.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Se cita un segmento sin escucharlo | Invariante 1, y marca visible en la salida de qué segmentos fueron cotejados |
| Una alucinación con confianza alta pasa por buena | Cotejo por redundancia (§8) para todo dato decisivo |
| La diarización se usa para atribuir «solo esta vez» | Invariante 4, y la salida declara que no distingue voces |
| Deriva de las marcas de tiempo con el filtro de voz activo | Prueba de anclaje: elegir segmentos al azar y comprobarlos contra la grabación |
| El refinado se convierte en la fuente citada | Invariante 7; el refinado lleva marca visible de que no es citable |
| La dependencia no está en la máquina de ella | Fallo declarado: si no hay motor, se dice y el audio no se usa |

## Validación / pruebas necesarias

1. **Diez minutos de una audiencia real, transcritos a mano** como referencia, y medir cuatro cosas por separado: error de palabra; **cuántos segmentos son texto inventado, contados aparte de los errores**; deriva de las marcas de tiempo; y **si las señales de confianza separan los segmentos malos de los buenos**. Si no separan, la decisión 3 pierde su base y hay que rehacerla.
2. **Prueba adversarial del invariante 1:** dar a un lector una transcripción con una frase fabricada insertada, y comprobar si la detecta sin escuchar el audio. La hipótesis es que no.
3. **Medir la diarización** con número de hablantes conocido, contando frases mal atribuidas. Si el resultado se parece al 17-20 % publicado, la decisión 4 queda confirmada empíricamente.
4. Comprobar que el cambio de motor produce versión nueva y no sobrescribe.

## Preguntas pendientes

1. **¿Qué motor?** La investigación recomienda uno concreto para Windows sin instalar entorno de desarrollo, pero **no hay ningún banco de pruebas de reconocimiento de voz para español colombiano**: la calidad real es desconocida hasta medirla.
2. **¿Dónde vive la transcripción** — zona 2 o zona 3 de `ADR-012`? Es un derivado de material incorporado, lo que sugiere zona 3.
3. **¿Se exige transcripción humana para los minutos que sostienen un hecho**, o basta la escucha de comprobación del invariante 1?
4. **¿Qué se hace cuando el audio no está disponible** y solo llega la transcripción producida por un tercero? Entonces la transcripción **es** el material recibido, y el invariante 1 no se puede cumplir. Hay que decidir si eso la inhabilita para citar o solo la marca.
5. **Dos licencias con problema:** algunos modelos de diarización que vienen empaquetados con los motores recomendados están restringidos a uso personal sin ánimo de lucro, y la herramienta específicamente construida contra la alucinación tiene pesos no comerciales. **Trabajo jurídico remunerado probablemente no cabe en esas licencias.**

## Relaciones con otros ADRs

- **ADR-016** (ingesta sin capa de texto): este ADR es su espejo. Aquel protege contra una ausencia que se lee como hecho; este, contra una presencia que no ocurrió. **Comparten el mecanismo de cotejo por redundancia y la obligación de declarar el productor del derivado.**
- **ADR-011** (locators): se aplica §7 (metadatos), §8 (regeneración aditiva) y §4 (tiempo en el plano del original). **Este ADR resuelve para la vía local el riesgo nº 1 de aquel** y respalda su límite del §Riesgos nº 4 sobre el anclaje por palabra.
- **ADR-001** (frontera de confianza): la decisión 6 es su aplicación directa.
- **ADR-003** (modelo epistémico): una transcripción no sube el estado de nada; lo transcrito sigue siendo lo que alguien dijo.
- **ADR-012** (distribución): motor y modelos entran en el modelo de actualización.
- **ADR-005** (autoridad humana): el invariante 1 traslada a la profesional la comprobación que ninguna máquina puede hacer por ella.
