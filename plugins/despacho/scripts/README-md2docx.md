> **RETIRADO EL CONVERSOR DE NODE — 2026-09-01.** `md2docx.js` y `lib.js` se eliminaron. Dependían de Node y de `NODE_PATH='C:
vm4w
odejs
ode_modules'`, **una ruta que solo existe en la máquina de quien lo escribió**: en la de ella el conversor habría fallado siempre.
>
> Lo sustituye **`md2docx.py`**, mismo comportamiento, sin segundo tiempo de ejecución (ADR-018). **Verificado idéntico en cuatro documentos reales** —incluidos dos entregables del expediente—: 36 tablas, 290 filas, 55.848 caracteres, **cero diferencias** en tablas, filas, celdas y caracteres. La retención medida sobre el original es del **100 %**.
>
> Se retira en vez de conservarse porque dos conversores derivan, y ADR-014 invariante 6 exige que las dos capas digan lo mismo.
>
> **Uso:** `python md2docx.py entrada.md salida.docx "Título" "Subtítulo"`

---

# md2docx — convertir una salida del arnés en un documento de Word

**Qué es.** Un conversor de Markdown a `.docx` con **tablas de Word de verdad**, escrito para que las salidas del arnés lleguen a la abogada en el formato que ella usa.

**Qué NO es, y conviene decirlo primero.** Esto es un **apaño consciente**, no una pieza del producto. ADR-014 fija que el entregable del arnés es un documento de Word, y su pregunta abierta 2 dice exactamente lo que pasa mientras no se resuelva:

> Mientras el plugin sea texto puro, la skill no puede ejecutar código. **O el Core asume la generación del `.docx`, o el entregable Word depende de que alguien corra un script a mano.**

Esta carpeta es esa segunda rama, hecha explícita. Vive en `tools/` y no en `plugins/` por eso.

---

## Por qué existe

El informe de crítica lo predijo como **H-13**: «tablas de Markdown en `.txt` pegadas en Word son una hilera de tuberías; "lista para pegar" falla al primer intento». El pase real del 2026-08-27/28 sobre el expediente [radicado del expediente] lo confirmó y añadió lo que la predicción no decía: el problema no es el pegado, **es la forma del entregable**. La usuaria no abre Markdown.

Cuatro de los seis `SKILL.md` prometen tablas «listas para pegar». Esa promesa solo se cumple si sale una tabla de verdad.

## Requisitos

- **Node.js** con el paquete `docx` accesible.
- **Python** con `python-docx`, solo para el control de fidelidad.

`docx` suele estar instalado de forma global, y entonces Node no lo encuentra desde esta carpeta. Hay que decirle dónde está:

```bash
export NODE_PATH='C:\nvm4w\nodejs\node_modules'
```

Compruébelo antes de nada:

```bash
node -e "require('docx'); console.log('docx ok')"
```

## Uso

```bash
node md2docx.js entrada.md salida.docx "Título" "Subtítulo"
```

Título y subtítulo son opcionales. Si no se pasan, se toman del primer `#` del archivo y de la línea que le sigue.

**Si se fuerza el subtítulo, el original no se pierde:** baja al cuerpo del documento como bloque destacado. Esto no es un capricho: la línea que va bajo el título de las salidas del arnés suele ser el descargo («Propuesta para su revisión. Nada de esto está comprobado por ningún sistema»), y en la primera versión del conversor **desaparecía sin dejar rastro**.

## Qué convierte

| En el Markdown | En el Word |
|---|---|
| `#` (el primero) | Título del documento |
| `##`, `###`, `####` | Encabezados 1, 2 y 3 — navegables desde el panel de Word |
| `**negrita**`, `*cursiva*` | Negrita y cursiva, dentro del párrafo |
| Tabla `\| … \|` | **Tabla de Word real**, con encabezado sombreado y filas alternas |
| `> cita` | Bloque destacado sobre fondo de color |
| `- viñeta` | Viñeta |
| `- **Campo:** valor` (3 o más seguidas) | **Tabla de dos columnas** Campo/Contenido |
| `- Campo: valor` (3 o más seguidas) | Lo mismo |
| `**H-01 — …**`, `**F-03 — …**` | Encabezado de ficha |
| `1.` `2.` `3.` | Párrafos con sangría |
| `---` | Se descarta (la separación la da el espaciado) |
| `[texto](enlace)` | Solo el texto |

Las dos reglas de «tres o más seguidas» son las que convirtieron el informe de rigor judicial de un muro de 155 viñetas en 15 tablas legibles, y la hoja de hechos en 36 fichas navegables. **Sin ellas el documento se abre y se cierra.**

## El control de fidelidad — no es opcional

Después de convertir, compruebe que no se perdió nada:

```bash
python verificar-fidelidad.py salida.docx entrada.md
```

Umbrales: **≥ 99 % ok** · **95-99 % REVISAR** · **< 95 % PERDIDA**.

Entre 95 y 99 % lo que suele faltar es ruido de la propia medición: una etiqueta que en el Markdown lleva dos puntos («target:») y en la tabla del Word queda sin ellos. **Mírelo igual.** Este control existe porque encontró una pérdida real que una lectura por encima no habría visto.

## Limitaciones conocidas

- **No renderiza.** No comprueba cómo se ve el documento, solo que el contenido esté. En la máquina del pase real no había LibreOffice ni `pdftoppm`, así que los tres primeros entregables se enviaron **sin que nadie los hubiera visto**. Ábralos antes de mandarlos.
- **No hace bloques de código** ni notas al pie ni imágenes: las salidas del arnés no los usan.
- **El encabezado genérico de las tablas Campo/Contenido** a veces queda flojo (en una tabla de discordancias, «Campo» es en realidad un nombre de documento). Es honesto pero mejorable.
- **Depende de `NODE_PATH`.** No vendoriza `docx`.

## Ficheros

| Fichero | Qué es |
|---|---|
| `md2docx.js` | El conversor. Se ejecuta desde la línea de comandos |
| `lib.js` | Los ladrillos: párrafo, encabezado, viñeta, caja, tabla, documento. Sirve también para escribir un `.docx` a mano, sin Markdown de por medio |
| `verificar-fidelidad.py` | El control de que no se perdió contenido |

## Relación con los ADR

- **ADR-014** — Forma de entrega. Este conversor implementa las decisiones 1 (dos capas), 2 (tablas reales) y 3 (encabezado de propuesta en la primera página), y es la rama «alguien lo corre a mano» de su pregunta abierta 2.
- **ADR-015** — El informe del séptimo comando es el caso más exigente: 14 hallazgos por 13 campos.
