# SPEC-05 — La marca ` - REVISADO`: que Windows no le anule una decisión suya

**Estado:** ejecutada · **Cierra:** `PM-M-2` · grupo `G25` · lo que quedó vivo de `G17` · **Familia:** defecto

---

## 1. Qué problema cierra

La marca ` - REVISADO` es **el único mecanismo de todo el producto por el que la autoridad cambia de manos**. Sin ella, una hoja de hechos es una propuesta que nadie miró; con ella, es una decisión suya registrada. Cinco skills la consumen y tres se detienen sin ella.

Y hoy **se reconoce con una regla exacta que su computador puede romper sin que ella se entere**:

> «Solo el archivo cuyo nombre termina en ` - REVISADO.md` cuenta como hechos aprobados.»
> — `redactar-escrito/SKILL.md` §3 · `hechos-con-prueba/SKILL.md` §4 · `inventario-de-anexos/SKILL.md` §5

**El Explorador de Windows oculta las extensiones conocidas de forma predeterminada.** Ella abre la carpeta, ve `Hechos - Salento - 2026-08-27`, pulsa F2, escribe ` - REVISADO` al final y guarda. Según cómo esté configurado ese equipo y con qué programa haya abierto el archivo, en el disco queda una de estas:

| Lo que queda en el disco | Por qué |
|---|---|
| `Hechos - Salento - 2026-08-27 - REVISADO.md` | Extensiones ocultas. **Es la forma canónica y funciona** |
| `Hechos - Salento - 2026-08-27 - REVISADO.md.md` | Extensiones visibles: escribió sobre el nombre completo y el programa añadió la suya |
| `Hechos - Salento - 2026-08-27 - REVISADO.txt` | «Guardar como» desde el Bloc de notas |
| `Hechos - Salento - 2026-08-27 - REVISADO` | Renombró borrando la extensión visible |
| `Hechos - Salento - 2026-08-27 -REVISADO.md` | Se comió el espacio al teclear |

**Cuatro de las cinco no cumplen la regla escrita.** Y lo que pasa entonces no es que el comando falle: es que **dice, con todas sus letras, que no hay hechos aprobados** —*«en la carpeta hay siete documentos y ningún archivo de hechos terminado en ` - REVISADO`»*— con el archivo aprobado a la vista, en esa misma carpeta.

> **Por qué esto pesa más de lo que parece.** El defecto **castiga a la usuaria justo después del trabajo más caro que el producto le pide**: leer setenta y seis fichas una por una y decidir `SÍ`, `NO` o `A MEDIAS` en cada una. Hecho eso, el sistema le contesta que no lo hizo. Y el mensaje es peor que un error, porque **es verosímil**: ella no tiene cómo saber que el problema es un punto-eme-de-más en un nombre que su computador no le enseña.

**Verificado contra el código el 2026-09-05**, que es la regla 4 de esta capa: los seis `SKILL.md` que citan la marca la describen únicamente en su forma canónica; `grep` de `.md.md`, «extensión oculta» y cualquier tolerancia de nombre no devuelve **nada** en todo `plugins/`. **El defecto está vivo y entero.**

## 2. Comportamiento observable

1. Ella guarda su archivo revisado **en cualquiera de las cinco formas de arriba** y el comando siguiente lo encuentra y trabaja con él.
2. La salida del comando **dice el nombre exacto del archivo que aceptó como marcado**. Ella puede desmentirlo de un vistazo.
3. Si en la carpeta hay un archivo con «revisado» en el nombre **de una forma que no cuenta** —al principio del nombre, en medio, `(revisar)`—, el comando **no lo ignora en silencio**: lo nombra, dice por qué no cuenta y pregunta.
4. Si hay **más de un** archivo marcado del mismo caso, el comando **no elige**: los nombra con su fecha y pregunta cuál manda.
5. Si no hay ninguno, el comando se detiene **exactamente igual que hoy**, y su mensaje ahora dice también qué formas del nombre habría aceptado.

## 3. Reglas duras

| # | Regla | De dónde sale |
|---|---|---|
| R-1 | **La marca la pone ella y nunca el sistema.** Esta spec amplía cómo se *reconoce*, jamás quién la *pone* | ADR-005 · ADR-008 |
| R-2 | **Reconocer no es renombrar.** El comando no corrige el nombre del archivo, no lo mueve y no lo copia con otro nombre. Arreglarle el nombre sería decidir por ella que esa era la intención | `estado-del-caso` §1, regla de escritura · `H-11` |
| R-3 | **Ninguna tolerancia alcanza a un archivo sin marca.** Un archivo cuyo nombre no termina en `REVISADO` no cuenta, aunque esté completo, bien hecho y coincida con los documentos | `redactar-escrito` §3 |
| R-4 | **La ambigüedad no se resuelve sola.** Dos candidatos, o un casi-candidato, se entregan a ella. No se elige el más reciente por ser el más reciente | `cronologia` §3 — «se entregan las dos y no se elige» |
| R-5 | **Lo que se aceptó se declara.** El nombre exacto del archivo aceptado va en la salida, siempre. Una tolerancia que no se declara es una tolerancia que nadie puede auditar | `H-12` — «un autoinforme no es control» |

## 4. Qué NO hace

- **No renombra, no mueve y no crea archivos.** Ni siquiera para «arreglar» un nombre evidente.
- **No pone la marca**, ni la sugiere puesta, ni trata como marcado lo que no lo está.
- **No adivina la intención.** `REVISADO - Hechos.md`, `Hechos (revisar).md` y `Hechos - REVISADO - v2.md` **no cuentan**: se nombran y se pregunta.
- **No toca el mecanismo de aprobación** —qué escribe ella dentro del archivo, `SÍ`/`NO`/`A MEDIAS`—, que está cerrado y verificado desde antes (la retirada de SPEC-02).
- **No añade un programa.** La regla es de lectura y funciona sin Python, como el resto del producto sin sus siete programas.

## 5. Cómo se sabe que quedó

Observables, cada uno capaz de fallar:

| # | Observable | Cómo se comprueba |
|---|---|---|
| O-1 | Los **seis** `SKILL.md` que citan la marca traen la regla de reconocimiento, con la misma redacción | `grep -c` de la frase canónica = 6 |
| O-2 | Un archivo `... - REVISADO.md.md` **cuenta como marcado** | `test_marca_revisado.py` sobre `caso-02` | **Pasa** |
| O-3 | En una pasada, la salida **nombra el archivo aceptado**, con su extensión tal cual | Solo una pasada real | **Pendiente** |
| O-4 | Un archivo `Hechos (revisar).md` **no cuenta y se detecta** para poder nombrarlo | `test_marca_revisado.py` | **Pasa — y no pasaba** |
| O-5 | Con dos archivos marcados, **la regla no elige**: los reconoce a los dos | `test_marca_revisado.py` | **Pasa** |
| O-6 | La guía de ella explica las cinco formas y **le dice que no tiene que acertar con la extensión** | Se lee `GUIA-PARA-LA-ABOGADA.md` |
| O-7 | Ninguna skill renombra nada: la regla R-2 está escrita donde se reconoce la marca | `grep` de la regla |

**O-1, O-6 y O-7 se comprobaron al escribirla. O-2, O-4 y O-5 se comprobaron el 2026-09-05** contra `evals/casos/caso-02-sintetico-autoridad`, con la regla traducida a código en `evals/scripts/test_marca_revisado.py`. **O-3 sigue pendiente: solo una pasada real lo enseña.**

### Lo que encontró ejecutarla, y es la razón de que valga la pena traducir una regla en prosa a código

**La prueba falló en su primera ejecución, y el defecto era de la regla, no del código.** La redacción decía:

> *«Si hay un archivo con «revisado» de cualquier otra forma —al principio del nombre, en medio, `(revisar)`— … se nombran y se pregunta»*

**Y «revisar» no contiene «revisado».** Son dos palabras distintas: la regla ofrecía como ejemplo un caso que su propio enunciado no cubre. Un modelo que aplicara la regla al pie —buscando «revisado»— **pasaría de largo por encima de `Hechos - Salento (revisar).md` sin verlo**, que es exactamente el fallo silencioso que esta spec existe para impedir, reproducido dentro de la spec.

**Corregido en los seis:** la señal que se busca es **la raíz «revis»**, no la palabra, y la regla ahora dice por qué.

> **La lección es sobre el método, no sobre esta regla.** Una regla en prosa que no se puede implementar sin inventar un criterio **es una regla ambigua**, y una regla ambigua la resuelve el modelo por su cuenta, distinto en cada pasada. Traducirla a código no la convierte en producto —el producto sigue siendo la prosa—: **la somete a la única pregunta que la prosa no se hace sola, que es si decide.**

## 6. Qué toca

| Archivo | Qué |
|---|---|
| `cronologia` · `estado-del-caso` · `hechos-con-prueba` · `inventario-de-anexos` · `inventario-de-bienes` · `redactar-escrito` — bloque §2 | La regla de reconocimiento, **idéntica en los seis**, dentro del bloque que ya define la marca |
| `redactar-escrito/SKILL.md` §3 | La tabla de las cinco formas · el casi-candidato · los dos candidatos · el mensaje de «no hay hechos aprobados» ampliado · autoevaluación |
| `inventario-de-anexos/SKILL.md` §5 | La misma tabla, abreviada, donde hoy define qué cuenta como aprobado |
| `inventario-de-bienes/SKILL.md` Fase 1 | Igual |
| `hechos-con-prueba/SKILL.md` §4 | La instrucción a ella: **que no tiene que acertar con la extensión** |
| `hechos-con-prueba/FORMATO-DE-SALIDA.md` | Las dos plantillas que le dicen cómo guardar |
| `GUIA-PARA-LA-ABOGADA.md` | Lo mismo, en su idioma y sin nombres de archivo técnicos |

## 7. Qué queda fuera y por qué

- **Detectar la marca dentro del archivo** (que ella escriba «REVISADO» en la primera línea en vez de en el nombre). Sería un segundo mecanismo de aprobación conviviendo con el primero, y **dos mecanismos de autoridad es exactamente la enfermedad que este repositorio ya documentó**. Si el nombre resulta ser un mal soporte, se cambia el mecanismo entero por ADR, no se le añade uno paralelo.
- **Un programa que normalice los nombres.** Escribiría en la carpeta de ella para arreglar algo que ella no pidió arreglar (R-2).
- **Enseñarle a mostrar las extensiones en Windows.** Es la solución de raíz y no está en nuestras manos; además le pone a ella la carga de configurar su equipo para que el producto funcione. **La guía lo menciona como algo que puede hacer, no como algo que tiene que hacer.**
- **La marca en `3-Para presentar/`.** Hoy la marca solo gobierna lo que se usa como fuente. Que también signifique algo en la carpeta de entregas es una decisión de producto, no un defecto.
