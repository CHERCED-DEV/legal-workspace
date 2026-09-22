# La primera instalación

> **Léase esto primero: nadie ha ejecutado todavía estos pasos.** El plugin está publicado y comprobado del lado del repositorio —los archivos están, el JSON es válido, un clon limpio los trae todos—, pero **nunca se ha instalado en una máquina que no sea la de quien lo escribió**. Los pasos de abajo están escritos desde cómo se instalan los plugins, no desde haberlos hecho.
>
> **Si algo en su pantalla no coincide con lo que dice esta hoja, la que está mal es la hoja.** Mande la pantalla y se corrige. Es la primera vez, y se sabe que es la primera vez.

Esta hoja **es para quien instala**, no para quien usa. Termina exactamente donde empieza `GUIA-PARA-LA-ABOGADA.md`, que es la que ella lee.

---

## 1. Qué hace falta antes de empezar

| | |
|---|---|
| **Claude Code**, instalado y con sesión iniciada | Es la ventana donde se escribe |
| **Conexión** | Solo para instalar y para trabajar. El plugin son trece métodos de texto más una carpeta de programas |
| **Nada más** | No hay servidor, ni base de datos, ni clave que pedir, ni nada que pagar aparte de la suscripción de ella |

**No hace falta** Git ni saber programar. **Python es opcional y hace la diferencia:** sin él los doce comandos funcionan igual —el modelo hace a mano el trabajo mecánico, más lento y gastando mucha más lectura—; con él, la oficina de programas del plugin prepara el material, busca dentro del expediente, produce los Word y **conserva intactas sus notas del archivo de estado**. **Ningún comando exige Python para arrancar, y todos declaran cuándo no lo tuvieron.**

Si va a instalarlo: `python.org`, versión 3.9 o posterior, marcando «Add to PATH». Las bibliotecas las pide cada programa cuando le hacen falta, diciendo cuál — **y desde el 2026-09-21 eso es cierto en todos**: dos reventaban con un error de Python en pantalla, y se comprobó uno por uno. Los catorce programas de hoy lo cumplen, y hay una prueba que falla el día que uno deje de cumplirlo.

### Las bibliotecas, y qué se pierde sin cada una

**No hace falta instalarlas todas, y ninguna hace falta para que los doce comandos arranquen.** La tabla está aquí para que quien instala pueda decidir, en vez de descubrirlo cuando un comando lo diga:

| Si instala | Con qué | Qué gana | Qué pasa sin ella |
|---|---|---|---|
| **python-docx** | `pip install python-docx` | **Las entregas en Word** — y la comprobación de que el Word dice lo mismo que el `.md` | El comando entrega el contenido **en texto y lo declara**. La entrega existe, peor, y diciéndolo |
| **pypdf** | `pip install pypdf` | Que la búsqueda mire **dentro de los PDF** | La búsqueda no ve esos PDF **y lo dice en su salida** |
| **Pillow · numpy · rapidocr-onnxruntime** | `pip install pillow numpy rapidocr-onnxruntime` | **Sacar el texto de las fotografías y los escaneados** — es lo que convierte 23 fotos de un expediente en algo con lo que se puede trabajar | El preparador monta la carpeta y copia los originales igual, **sin extraer texto**. Los comandos leen las imágenes a mano: más lento y mucha más lectura |
| **faster-whisper · av · numpy** | `pip install faster-whisper av numpy` | **Pasar una grabación a texto** en esta misma máquina, sin que el audio salga de ella | `/transcribir-audio` **no transcribe nada y lo dice**, nombrando la biblioteca que falta. Es la única de esta tabla sin camino degradado: el resto del caso sigue, la grabación se declara y no se usa |
| **sherpa-onnx** | `pip install sherpa-onnx` | Que la transcripción **separe las voces** —«Hablante 1», «Hablante 2»— sin ponerles nombre | La transcripción sale igual, **sin números de hablante y avisando de ello**. Se pierde saber si dos frases seguidas son de la misma persona |
| **Tesseract** *(programa, no biblioteca)* | Ver lo que dice `segunda_opinion.py` al correrlo | Una **segunda opinión** sobre lo que el primer reconocedor leyó mal | Ese control no existe, y el programa lo dice con esas palabras |

> **Lo que ninguna biblioteca cambia:** los doce métodos, sus reglas y lo que se niegan a hacer. Python no añade criterio — **añade que el trabajo mecánico lo haga un programa** en vez de gastarse la lectura del modelo en él.

**Y el orden si va a instalar solo una:** `python-docx`. Es la que produce el archivo que ella abre.

**Todo de una vez, si quiere terminar:**

```
pip install python-docx pypdf pillow numpy rapidocr-onnxruntime faster-whisper av sherpa-onnx
```

> **Y una advertencia sobre las tres últimas:** `faster-whisper` y `sherpa-onnx` **descargan modelos la primera vez que se usan**, y pesan. Si no va a transcribir grabaciones, la línea de arriba sin ellas le sirve igual.

---

## 2. Los pasos

**Paso 1 — Añadir el repositorio como origen de plugins.**

```
/plugin marketplace add CHERCED-DEV/legal-workspace
```

Debería responder que encontró el catálogo `legal-workspace` y, dentro, un plugin llamado `despacho`.

**Paso 2 — Instalarlo.**

```
/plugin install despacho@legal-workspace
```

**Paso 3 — Comprobar que aparecieron los comandos.** Escribir una barra `/` sola y esperar un segundo. Debería salir la lista.

> **Este paso es el que importa, y es el que nadie ha visto.** Hay que anotar **con qué nombre exacto aparecen**: `/cronologia` o `/despacho:cronologia`. **Las dos formas son normales**; lo que no vale es suponer cuál es. La guía de ella ya está escrita para las dos, así que no bloquea nada — pero conviene saberlo.

**Paso 4 — Probar uno, sobre una carpeta de verdad.** El más barato y el más informativo:

```
/estado-del-caso
```

sobre una carpeta con la forma de la guía §2. Debería leer la carpeta y devolver qué hay, de qué fecha, qué entró y qué falta — **sin escribir en `1-Documentos recibidos/`**.

---

## 3. Qué mirar en esa primera prueba

Cuatro cosas, y las cuatro están sin comprobar:

| Qué | Por qué importa |
|---|---|
| **Con qué nombre aparecen los comandos** | Es el único paso que nadie ha visto nunca |
| **Que aparezcan los doce**, no seis | Hasta el 2026-09-01 la documentación decía seis. Si salen menos de doce, algo no se instaló |
| **Que no escriba en `1-Documentos recibidos/`** | Es la regla dura de todo el sistema. Se comprueba mirando la fecha de modificación de esa carpeta antes y después |
| **Qué hace con un PDF escaneado sin texto** | Si no lo lee, no funciona ninguno de los doce con material fotografiado. **Con Python, `/preparar-material` lo resuelve antes**: extrae el texto una vez y los demás trabajan sobre él. Conviene probarlo con un archivo real **antes** de sentarse a trabajar |

---

## 4. Si algo falla

| Lo que pasa | Qué mirar |
|---|---|
| No encuentra el catálogo | Que el nombre esté bien escrito, y que haya conexión. El repositorio es público |
| Instala pero no aparecen comandos | Probar en una **sesión nueva**: está sin comprobar si aparecen en una sesión ya abierta |
| Aparecen menos de doce | Falta alguno de los `SKILL.md`. Se ve comparando con la lista del `README.md` |
| Un comando arranca y no hace lo que dice | **Eso no es de instalación, es de método.** Mande la salida: se corrige el `SKILL.md` y se vuelve a instalar |

**Y una regla que vale para todo lo anterior:** si el resultado no coincide con lo que dice esta hoja, **no lo dé por bueno «porque más o menos funciona»**. La primera instalación es la única oportunidad de ver el producto con ojos limpios, y lo que se anote aquí es lo que corrige la documentación para todos los demás.

---

## 5. Después de instalar

Dos cosas, en este orden:

1. **Mostrarle a ella en qué ventana escribe y en qué carpeta quedan sus casos.** La guía dice explícitamente que empieza cuando eso ya está hecho.
2. **Entregarle `GUIA-PARA-LA-ABOGADA.md`.** Está escrita para leerse sola, sin nada técnico.

**Y antes de que abra la primera carpeta**, que lea la §3 de esa guía —*dónde se procesa lo que usted abre aquí*—. Es secreto profesional, la decisión es suya, y **conviene tomarla antes de arrastrar el primer archivo, no después**.

---

## 6. Cómo se actualiza

Cuando se corrige un método, se corrige su `SKILL.md`, **sube la versión** y se vuelve a instalar desde el mismo sitio. **La carpeta de los casos no se toca nunca**: instalar es una operación del programa, no del expediente.
