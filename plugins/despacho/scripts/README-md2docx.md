# md2docx — convertir una salida del arnés en un documento de Word

**Qué es.** El conversor de Markdown a `.docx` **con tablas de Word de verdad**, que hace llegar las salidas del arnés en el formato que ella usa. **Vive dentro del plugin** y lo invocan las siete skills que entregan documento.

> **Este archivo se reescribió el 2026-09-05, y por qué importa decirlo.** Hasta hoy describía un producto que ya no existe: mandaba instalar Node, exportar `NODE_PATH` y correr `node md2docx.js` —un archivo retirado el 01/09—, decía que el conversor «vive en `tools/` y no en `plugins/`», y repetía la premisa que ADR-018 derribó: *«mientras el plugin sea texto puro, la skill no puede ejecutar código»*. Llevaba arriba una nota de corrección **y el cuerpo entero seguía siendo el viejo**. Una nota no corrige un cuerpo: quien lo leyera de corrido haría lo que dice el cuerpo, y fallaría. Es el hueco `V-11` del backlog.

---

## Por qué existe

`H-13` lo predijo: *«tablas de Markdown en `.txt` pegadas en Word son una hilera de tuberías; "lista para pegar" falla al primer intento»*. El pase real del 2026-08-27/28 lo confirmó y añadió lo que la predicción no decía: el problema no es el pegado, **es la forma del entregable**. La usuaria no abre Markdown.

**Siete de los once `SKILL.md` prometen tablas «listas para pegar».** Esa promesa solo se cumple si sale una tabla de verdad.

## Requisitos

**Python con `python-docx`** (licencia MIT). Nada más: **un solo tiempo de ejecución, sin rutas fijas** (ADR-018).

**Y es opcional.** Sin él los once comandos funcionan igual: escriben el contenido en texto en la misma carpeta y **lo declaran**. Ningún comando exige el conversor para arrancar, y cada uno dice cuándo no lo tuvo. **Nunca se da por hecho un archivo que no se vio quedar.**

## Uso

```bash
python md2docx.py entrada.md salida.docx "Título" "Subtítulo"
```

Título y subtítulo son opcionales; sin ellos se toman del primer `#` del archivo y de la línea siguiente.

**Si se fuerza el subtítulo, el original no se pierde:** baja al cuerpo como bloque destacado. No es un capricho — esa línea suele ser el descargo (*«Propuesta para su revisión. Nada de esto está comprobado por ningún sistema»*), y en la primera versión del conversor **desaparecía sin dejar rastro**.

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

Las dos reglas de «tres o más seguidas» convirtieron el informe de rigor judicial de un muro de 155 viñetas en 15 tablas legibles, y la hoja de hechos en 36 fichas navegables. **Sin ellas el documento se abre y se cierra.**

## El control de fidelidad — no es opcional

```bash
python verificar_fidelidad.py salida.docx entrada.md
```

Umbrales: **≥ 99 % ok** · **95-99 % REVISAR** · **< 95 % PÉRDIDA**.

Entre 95 y 99 % lo que suele faltar es ruido de la propia medición: una etiqueta que en el Markdown lleva dos puntos («target:») y en la tabla del Word queda sin ellos. **Mírelo igual.** Este control existe porque encontró una pérdida real que una lectura por encima no habría visto.

## Cómo se comprobó el puerto a Python

El conversor de Node se **retiró** en vez de conservarse: dos conversores derivan, y ADR-014 invariante 6 exige que las dos capas digan lo mismo. Antes de retirarlo se comprobó el puerto **contra el viejo, en cuatro documentos reales** —dos de ellos entregables del expediente—:

| Medida | Resultado |
|---|---|
| Tablas · filas · celdas · caracteres | **36 tablas, 290 filas, 55.848 caracteres — cero diferencias** |
| Retención medida sobre el original | **100 %** |
| Párrafos | 6 de diferencia: los separadores entre tablas, que Word necesita o las fusiona |

## Limitaciones conocidas

- **No renderiza.** Comprueba que el contenido esté, no cómo se ve. En la máquina del pase real no había LibreOffice ni `pdftoppm`, así que los tres primeros entregables se enviaron **sin que nadie los hubiera visto**. Ábralos antes de mandarlos.
- **No hace bloques de código**, notas al pie ni imágenes: las salidas del arnés no los usan.
- **El encabezado genérico de las tablas Campo/Contenido** a veces queda flojo (en una tabla de discordancias, «Campo» es en realidad un nombre de documento). Es honesto pero mejorable.
- **No tiene banco de pruebas propio.** La comprobación de arriba fue una comparación puntual contra el conversor retirado, y **el conversor retirado ya no está para repetirla**. Hoy nada detectaría una regresión de este archivo.

## Ficheros

| Fichero | Qué es |
|---|---|
| `md2docx.py` | El conversor |
| `verificar_fidelidad.py` | El control de que no se perdió contenido |

## Relación con los ADR

- **ADR-014** — Forma de entrega. Implementa las decisiones 1 (dos capas), 2 (tablas reales) y 3 (encabezado de propuesta en la primera página). **Su pregunta abierta 2 quedó cerrada por ADR-018:** ya no depende de que alguien corra un script a mano ni de un Core que no existe — lo invoca la skill.
- **ADR-015** — El informe del séptimo comando es el caso más exigente: 14 hallazgos por 13 campos.
- **ADR-018** — Por qué esto vive dentro del plugin y no en `tools/`.
