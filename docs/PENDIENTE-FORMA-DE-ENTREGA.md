# Pendiente — la forma de la entrega y la forma de la carpeta

> **Origen:** feedback del dueño, 2026-08-27. Sus palabras: *«las salidas deben ser en formato de texto crudo, escueto pero contundente… título, media introducción, datos detallados, subtítulos, todo, que quede muy bien en un documento de Word, que ella pueda copiar y pegar, que le sea friendly; que cuando mire dentro de un caso vea carpetas y separación de responsabilidades por carpeta —qué es un anexo, qué son pruebas, qué son evidencias, qué son informes, qué son evaluaciones—. Todo eso tenemos que dejarlo muy fino, muy fácil de entender, algo muy ágil y contundente»*.
>
> **No es para este ciclo.** Se registra ahora para no perderlo y porque una de las dos mitades ya está diagnosticada y a medio corregir.

---

## 1. La forma de la entrega — el diagnóstico ya existe

**HECHO MEDIDO.** Los siete métodos no se ponen de acuerdo sobre en qué formato entregan: **13 menciones a `.md`, 11 a `.txt`, 8 a `.docx`**. Y la ejecución real sobre el caso produjo **dos de cada**:

| Salida | Formato |
|---|---|
| Hechos · Cronología | `.md` |
| Revisión · No se pudo redactar | `.txt` |
| Inventario de anexos | `.docx` |

La crítica del arnés ya lo había llamado **H-13 — «Formatos de salida que no encajan con la promesa»**: dos comandos prometen una tabla *«lista para pegar en un escrito»* y la entregan como tabla de Markdown dentro de un `.txt`. **Pegada en Word es una hilera de tuberías y guiones.**

**Y hay un agravante en Windows:** un `.md` puede no abrir con doble clic. Un archivo que ella no puede abrir es un archivo que no existe.

### Lo que ya funcionó, y conviene copiarlo

`inventario-de-anexos` produce **`.docx` con tablas de verdad**, y en la ejecución real salió bien: 51 KB, dos tablas, 46 filas. Es la prueba de que el camino existe y de que el método puede exigirlo sin depender de nada externo.

### La regla que habría que escribir

**Una sola, para los siete**, y con la distinción que el dueño hace bien:

- **Texto crudo y escueto** — sin marcas de formato que solo se ven bien en un visor de Markdown. Nada de `**negrita**` ni `|` de tabla en un archivo destinado a copiarse.
- **Pero con estructura visible**: título, una línea de qué es esto, subtítulos, y los datos debajo. «Escueto» no es «sin forma»: es sin adorno.
- **Lo que se copia y pega va en Word con tabla real.** Lo que se lee en pantalla puede ser texto.
- **Y una convención de nombres única**, que hoy son tres distintas (guion, raya, con y sin nombre de caso).

**DECISIÓN PENDIENTE:** ¿un solo formato para todo, o dos —uno de lectura y uno para pegar—? Dos duplica el trabajo del método; uno obliga a elegir cuál pierde.

---

## 2. La forma de la carpeta — aquí hay una objeción de fondo

### 2.a La restricción que el propio dueño fijó, y que sigue vigente

Está citada literal en `technical-design/v0/17-deployment-layout.md:548`:

> *«que sea muy intuitiva para ella y operable para todos… sin que ellos sientan que es demasiado ruidoso o **lleno de carpetas**»*

Y la resolución que se le dio entonces: *«las tres condiciones se cumplen a la vez **solo si la profundidad no la paga ella**»*.

Más carpetas **es** profundidad que paga ella. Eso no invalida el feedback nuevo —una estructura que no distingue nada tampoco ayuda— pero sí obliga a que cada carpeta nueva **se gane su sitio** en vez de añadirse por completitud.

### 2.b La objeción real, que no es de cantidad sino de clasificación

**Anexo, prueba y evidencia no son tres cajas: son tres cosas que se solapan sobre el mismo papel.**

Un mismo documento puede ser, a la vez:
- **anexo** — va numerado en un escrito que se presenta;
- **prueba** — sostiene o contradice un hecho concreto;
- y **no ser evidencia de nada** — porque en este proyecto «evidencia» tiene un sentido preciso: el **rol probatorio** que un material cumple dentro de un caso, no el material mismo.

**Una carpeta obliga a elegir una sola.** Y elegir cuál es **valorar prueba**, que es exactamente lo que los siete comandos tienen prohibido hacer y lo que el producto reserva para ella.

**RIESGO concreto:** el día que un documento esté en `Pruebas/`, esa ubicación **afirma algo** — que es prueba de algo — sin que nadie lo haya decidido. Una carpeta es una afirmación silenciosa, y este producto está construido para no hacer afirmaciones silenciosas.

### 2.c Lo que sí distingue sin clasificar

La estructura actual **no clasifica por naturaleza: clasifica por procedencia y destino**, que es comprobable y no opinable:

| Carpeta | Qué la define | ¿Es opinable? |
|---|---|---|
| `1-Documentos recibidos` | **Entró de fuera.** Se lee, nunca se escribe | No |
| `2-Borradores` | **Lo produjo el sistema o ella.** En curso | No |
| `3-Para presentar` | **Ella lo dio por terminado** | No — lo decide ella al moverlo |

Esa es la razón por la que funciona: **nadie tiene que juzgar nada para saber dónde va un archivo.**

### 2.d Por dónde sí se puede ir

Tres vías, ninguna decidida:

1. **Separar lo que el sistema produce por tipo de trabajo, no por naturaleza jurídica.** Dentro de `2-Borradores`: `Informes/` (lo que el sistema entrega para leer) y `Para el escrito/` (lo que se copia y pega). Es procedencia, sigue sin clasificar prueba, y responde a lo que el dueño pide: ver de un vistazo qué es cada cosa.
2. **Que lo diga el nombre del archivo, no la carpeta.** `Inventario de anexos — …`, `Hechos con prueba — …`, `Cronología — …` ya lo hacen. Cuesta cero carpetas y es lo que menos paga ella.
3. **Una carpeta de anexos, y solo esa.** Es la única de las cinco que el dueño nombra que **no es una valoración**: un anexo es lo que se numera y se acompaña a un escrito — lo decide ella al armarlo, y es comprobable. `Pruebas/`, `Evidencias/` y `Evaluaciones/` sí son valoraciones.

**DECISIÓN PENDIENTE, y es del dueño:** ¿la carpeta debe reflejar **qué es** un documento (clasificación, opinable, y hoy prohibida al sistema) o **de dónde viene y a dónde va** (procedencia, comprobable, que es lo que hay)? Las dos son defendibles; lo que no lo es es tener una estructura que parece decir lo primero y solo puede sostener lo segundo.

---

## 3. Lo que hay que hacer cuando se retome

1. **Unificar el formato de salida en los siete**, con la convención de nombres única. Es la mitad ya diagnosticada (H-13) y no depende de ninguna decisión pendiente.
2. **Resolver la decisión de §1**: un formato o dos.
3. **Resolver la decisión de §2.d**: naturaleza o procedencia.
4. **Y medirlo**: la prueba no es que el archivo se vea bien en el editor, sino que **ella lo abra con doble clic, lo copie y lo pegue en su escrito sin tocar nada**. Eso se comprueba con un archivo real en su máquina, no leyendo el método.
