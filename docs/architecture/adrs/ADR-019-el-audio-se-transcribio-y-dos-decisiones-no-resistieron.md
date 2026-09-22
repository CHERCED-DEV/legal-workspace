# ADR-019 — El audio se transcribió, y dos decisiones de ADR-017 no resistieron el contacto con el material

## Estado

**CANDIDATO** — propuesto el 2026-09-19. Modifica `ADR-017`, que está en `Proposed`.
**No se aplica hasta que el dueño decida.** Lo que ya se produjo bajo el método viejo se
declara, no se borra.

## Contexto

`ADR-017` se escribió **antes de tener una grabación**, a propósito y con buen criterio: las
reglas de lectura se fijan mejor cuando todavía no hay nada que se quiera que diga algo.

El 2026-09-18 llegó material real: **56 minutos y 52 segundos** de una mesa de trabajo
municipal, en tres grabaciones de WhatsApp. Se transcribieron **dos veces con métodos
distintos** —`Despacho\Transcripciones\` y `Despacho\Transcripciones (iteracion 2)\`— y se
compararon. Este ADR registra qué predijo bien `ADR-017`, qué no, y **dos decisiones suyas que
el trabajo real violó**.

**Importa decir cómo se descubrió:** el conflicto no se detectó al diseñar, sino al integrar,
**después** de ejecutar. `ADR-017` no se leyó antes de implementar. Esa es la causa raíz y no
la tapa ninguna de las propuestas de abajo.

---

## Lo que ADR-017 predijo bien, y quedó confirmado con medición

### §3 — «las señales de confianza detectan mal el invento fluido»

**Confirmado, y con un ejemplo que vale más que el argumento.** Se probó la inferencia por
lotes como optimización: resultó **4,9 veces más rápida**, perdió **el 8,4 % de las palabras**
(869 de 949) **y su confianza media subió** al hacerlo — de −0,179 a −0,086. Es decir:
**parecía mejor porque transcribía menos.** Se descartó.

En la misma línea, la iteración 1 produjo en un tramo malo la frase *«Esto es lo que dice la
ministra. Acá va a ser la ministra. Para que ustedes hagan muy bien el desempeño de los
pequeños agentes»*, gramatical y sin sentido, donde otras cuatro decodificaciones dicen
simplemente *«lo que dice la ley»*.

### §8 — «cotejo por redundancia; divergencia sí significa problema»

**Es el control más valioso de todo el método, y con diferencia.** Sin él:

- No se habría detectado que la iteración 1 **perdió 31 segundos seguidos** (00:04:59 a
  00:05:30 del Audio 2) **sin marcar nada**, y que dentro iba un compromiso con plazo.
- No se habría sabido que **el nombre de una persona es inestable**: de **once
  decodificaciones** del mismo segundo, una dio nombre y apellido, otra el mismo nombre con
  **otro apellido**, una solo el nombre de pila y **ocho no dieron ninguno**. No es un dato de
  baja confianza: es un dato que **se contradice a sí mismo**.
  *(Los nombres reales no se reproducen aquí: este repositorio es público y el material del
  caso no vive en él. La forma del fallo es lo que el ADR necesita.)*

### §1 — «sus errores tienen forma propia: nombres propios, cifras y apellidos poco frecuentes»

**Confirmado hasta el detalle**, con la forma exacta que el ADR predecía:

- Un **topónimo** de cuatro sílabas produjo cuatro variantes, y **dos de ellas son ciudades
  reales** — el error no se delata solo, se lee como un nombre legítimo.
- Una **sigla de cuatro letras** dio cuatro lecturas, **una de ellas una palabra común** en vez
  de una sigla, que es el peor caso: no parece un fallo.
- Dos **siglas de organismo** perdieron o cambiaron una letra cada una.
- Un **cargo público** se transcribió como un adjetivo corriente de grafía casi idéntica.

*(Los términos reales no se reproducen: el repositorio es público. Lo que el ADR necesita es
la forma del error, no el caso.)*

### §6 — «el audio no sale de la máquina»

**Cumplido sin esfuerzo y sin coste.** Todo corrió en local sobre la GPU de la máquina, a
1,8× tiempo real con `float16` y **5,7× con `int8_float16` sin pérdida de palabras**. La
frontera de confianza no costó dinero ni tiempo.

---

## Las dos decisiones que el trabajo real violó

### Conflicto 1 — §5 e invariante 5: «ningún anclaje depende de la marca de palabra»

**Lo que dice ADR-017:** el alineamiento por palabra falla precisamente en cifras y fechas en
números, que es lo que más se cita. **El segmento es la coordenada.**

**Lo que se hizo:** se transcribió con `word_timestamps=True` y se usó la marca de palabra
para tres cosas:

| Uso | ¿Viola el invariante? |
|---|---|
| Alinear las pasadas entre sí para detectar divergencias | **No.** Es un cálculo interno; ninguna salida ancla nada ahí |
| Partir los segmentos largos en puntos de puntuación | **Discutible.** Cambia dónde empieza un segmento publicado, con la salvaguarda de que el corte solo se acepta si el texto reconstruido conserva exactamente las mismas palabras |
| **La sección B de «Pasajes a verificar», que da el minuto de cada cifra y cada nombre propio dudoso** | **Sí. Viola el invariante 5 de frente** |

**Y lo viola justo donde ADR-017 dijo que fallaría:** la sección B lista *cifras, fechas y
nombres propios* con **la marca de palabra** como localizador. El ADR predijo que el
alineamiento por palabra falla exactamente en esas tres clases.

**Propuesta.** Distinguir dos cosas que ADR-017 no separa:

- **Anclaje** — la coordenada contra la que resuelve una cita. **Sigue siendo el segmento, sin
  excepción.** El invariante 5 se mantiene íntegro.
- **Aviso** — un puntero para ir a oír. No sostiene ninguna afirmación.

Y aun así, **la sección B debería dar el minuto del segmento que contiene la palabra, no el de
la palabra**: no pierde utilidad —quien va a oír, oye el segmento entero— y deja de depender
de una marca que el propio ADR declara poco fiable. **Se propone corregirlo en el programa.**

### Conflicto 2 — §4 e invariante 4: «la diarización automática no cuenta como distinción de voces»

**Lo que dice ADR-017:** con 17–20 % de error de atribución medido en escenarios de sala, la
diarización **sirve para navegar el registro, no para afirmar quién dijo qué**.

**Lo que se hizo:** la iteración 2 separa voces con `sherpa-onnx` y marca cada línea como
«Hablante 1», «Hablante 2»… El dueño lo autorizó expresamente **sin que se le pusiera delante
este ADR**, porque no se había leído.

**Qué parte es compatible y qué parte no:**

- **Compatible:** las voces son anónimas y numeradas por cuánto hablan; ningún nombre se asigna
  a ninguna voz; cada salida declara que un número de hablante es una voz estimada y no una
  persona; y hay una sección entera dedicada a las líneas donde la voz asignada es dudosa.
- **NO compatible:** el resumen de la iteración 2 usó las voces para afirmar que **quien objetó
  la figura jurídica y quien respondió son personas distintas**. Eso es exactamente «afirmar
  quién dijo qué» a partir de diarización. Estaba marcado como no verificado, y aun así el
  invariante 4 no admite grados.

**Y falta la medición que el propio ADR-017 exige.** Su validación nº 3 pide medir la
diarización con número de hablantes conocido. **No se hizo, y no se puede hacer con este
material**: no hay verdad de referencia. Lo único medido es cuántas voces salen con cada
umbral —0,60 da doce voces en siete minutos, 1,05 funde personas distintas, 0,90 da cuatro—,
**que no dice nada sobre si están bien asignadas**.

**Propuesta.** Mantener el invariante 4 sin tocarlo, y añadir que **la diarización anónima es
admisible como ayuda de navegación** si cumple cuatro condiciones, que la implementación actual
ya cumple salvo la última:

1. Las voces son anónimas y nunca se les asigna un nombre.
2. La salida declara que un número de hablante es una voz estimada, no una persona.
3. Se publica la instrumentación: cuántas voces, cómo se reparte el habla y qué líneas tienen
   la voz dudosa.
4. **Ninguna salida derivada —resumen, hoja de hechos, cronología— usa la separación de voces
   para afirmar quién dijo qué, ni siquiera marcándolo como hipótesis.** Un cambio de voz es una
   razón para ir a oír, nunca un hallazgo.

---

## Lo que sigue sin verificar, y hay que decirlo

1. **La licencia de los dos modelos de voz no se ha comprobado.** `ADR-017` §Preguntas nº 5
   advierte que algunos modelos de diarización están restringidos a uso personal sin ánimo de
   lucro y que **trabajo jurídico remunerado probablemente no cabe ahí**. Los modelos usados
   —`pyannote-segmentation-3.0` y `wespeaker VoxCeleb CAM++`, redistribuidos por `sherpa-onnx`—
   **no se han revisado.** Es un riesgo abierto y no se debe usar en trabajo facturado hasta
   resolverlo.
2. **No hay banco de pruebas para español colombiano.** Sigue siendo la pregunta nº 1 de
   `ADR-017`, y este pase no la responde: no había transcripción humana de referencia.
3. **La deriva de las marcas de tiempo con el filtro de voz activo no se midió.** `ADR-017`
   §Riesgos la señala y propone una prueba de anclaje al azar. No se hizo.
4. **La validación nº 1 de ADR-017 sigue pendiente entera:** diez minutos de audiencia real
   transcritos a mano, para medir error de palabra, segmentos inventados y si las señales de
   confianza separan lo malo de lo bueno.

---

## Consecuencias

**Positivas.** El producto pasó de no poder tocar audio a transcribir una hora de reunión en
local, con instrumentación, en media hora de cómputo. El `POR COMPROBAR` del README sobre citar
el minuto de una grabación queda cerrado con evidencia. Y `ADR-017` sale **reforzado en sus tres
decisiones centrales** —§3, §6 y §8—, que es lo que más importa de él.

**Negativas.** Dos salidas ya entregadas —las dos carpetas de transcripción— contienen la
sección B anclada por palabra. **No se reescriben**: se declara aquí, conforme a `ADR-011` §8
(regenerar produce versión nueva, nunca sobrescribe). Y el resumen de la iteración 2 contiene
una afirmación sobre dos hablantes distintos que el invariante 4 no admite; **se corrige en su
sitio, dejando constancia**.

**De proceso.** La causa raíz —implementar sin leer el ADR que gobierna el asunto— no se corrige
con un ADR. Se corrige leyendo `docs/architecture/adrs/` **antes** de tocar código en un área
que ya tiene decisión escrita.

## Relaciones

- **ADR-017**: este ADR lo modifica en §4 y §5 y lo confirma en §1, §3, §6 y §8.
- **ADR-011** §8: por eso las carpetas anteriores no se sobrescriben.
- **ADR-016**: el cotejo por redundancia se confirma como el control transversal de los dos.
- **ADR-018**: el plugin ejecuta código; `transcribir_audio.py` es otro caso de esa decisión.
