# ADR-018 — La oficina: el plugin ejecuta código, y el modelo deja de hacer a mano lo que una máquina hace mejor

## Estado

Proposed

## Contexto

### El error, y de dónde salió

Nueve documentos de este repositorio dan por sentado que un comando del despacho **no puede ejecutar código**. Los más explícitos:

| Dónde | Qué dice |
|---|---|
| ADR-014, pregunta abierta 2 | *«Mientras el plugin sea texto puro la skill no puede ejecutar código: o el Core lo asume, o el entregable Word depende de que alguien corra un script a mano. Es la pregunta abierta más incómoda de este ADR.»* |
| `docs/specs/README.md` | *«Que una skill ejecute código (el Core): **no existe**. El plugin es texto puro.»* |
| SPEC-01 §4 | *«No instala el Core. No existe, y ninguno de los nueve comandos lo necesita: son texto puro.»* |
| `ESTADO-DEL-PROYECTO` §30 | *«Los seis son texto puro: sin servidor, sin herramientas, sin Core.»* |

**Es falso, y comprobado el 2026-09-01 contra la documentación oficial de la plataforma.**

> **Nadie decidió nunca que el plugin no pudiera ejecutar código.** «Texto puro» era una **descripción correcta de lo que se había construido** —nueve `SKILL.md` y nada más— y en algún punto se leyó como un **límite de lo que era posible**. Es el error de razonamiento más caro del proyecto hasta hoy: bloqueó `tools/preparar-material/` y `tools/md2docx/` fuera del producto, dejó la pregunta 2 de ADR-014 abierta cinco días, y puso «el Core» —una pieza que no existe y que nadie ha empezado— como dependencia de tres capacidades **que ya están construidas y funcionando**.

### Lo que la plataforma sí permite

Un plugin admite, además de `skills/`:

| Componente | Para qué sirve aquí |
|---|---|
| `scripts/` | Programas de utilidad — Python, shell, Node — que una skill invoca |
| `bin/` | Ejecutables que entran al `PATH` y se llaman por su nombre |
| `hooks/` | Manejadores de 30+ eventos del ciclo de vida, incluido `PreToolUse` |
| `agents/` | Subagentes con su propio modelo, esfuerzo y herramientas |
| `.mcp.json` | Servidores MCP que arrancan solos al activar el plugin |
| `monitors/` | Procesos de fondo que envían avisos durante la sesión |
| `${CLAUDE_PLUGIN_ROOT}` | Ruta de instalación, para referirse a lo que viene dentro |
| `${CLAUDE_PLUGIN_DATA}` | **Directorio persistente que sobrevive a las actualizaciones** |

Y el mecanismo concreto que lo hace utilizable sin fricción, tomado del patrón oficial:

```yaml
---
name: nombre-del-comando
description: ...
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/algo.py *)
---

Ejecuta `${CLAUDE_SKILL_DIR}/scripts/algo.py <argumento>`.
```

> Usar la misma variable en el cuerpo y en `allowed-tools` hace que **el script corra sin pedir permiso cada vez**. Sin eso, una oficina de diez herramientas sería diez interrupciones por caso.

### Por qué importa, y no es comodidad

Tres hechos medidos en este repositorio:

1. **La lectura del material fue el 89,6 % del coste de la sesión del pase real**, con del orden de 1,75 M de fichas gastadas en 35 agentes releyendo las mismas 23 fotografías.
2. **`preparar_material.py` hace ese trabajo en un minuto y con cero fichas**, y ya está escrito.
3. **`md2docx` produjo 139 tablas reales de Word**, y hoy depende de que alguien corra un script a mano fuera del producto.

**El modelo está haciendo a mano tres cosas que una máquina hace mejor, más rápido y gratis.** No es un problema de prompt: es que las herramientas están del lado equivocado de la frontera.

## Decision

### 1. El plugin lleva su propia oficina, y las skills la usan

`plugins/despacho/scripts/` pasa a ser parte del producto. Lo que hoy vive en `tools/` **se mueve dentro**, y las skills lo invocan por `${CLAUDE_PLUGIN_ROOT}`.

**El Core deja de ser dependencia de nada que ya funcione.** Si algún día existe, será para otra cosa; **ninguna capacidad construida vuelve a esperarlo.**

### 2. La regla que decide qué va a Python y qué se queda en el modelo

> **A la máquina, lo que tiene una respuesta correcta comprobable. Al modelo, lo que exige criterio.**

| Va a Python | Se queda en el modelo |
|---|---|
| Descomprimir, ordenar, calcular huellas, contar | Decidir si un hecho está apoyado o contradicho |
| Extraer texto, rotar, medir cobertura | Leer una firma manuscrita, entender qué pide un escrito |
| Buscar una cadena en el expediente | Redactar, emparejar afirmación con anexo |
| Construir un `.docx`, un PDF, un índice | Distinguir lo alegado de lo acreditado |
| Transcribir audio | Cualquier cosa que ella vaya a firmar |

**Y el corolario que evita el error simétrico:** que una tarea sea automatizable **no la vuelve fiable**. El OCR falla callándose y la transcripción inventa; ADR-016 y ADR-017 siguen mandando enteros. **La máquina hace el trabajo mecánico; no adquiere autoridad por hacerlo.**

### 3. Ninguna herramienta de la oficina decide nada

Toda salida de un script es **material derivado** con su receta —`ADR-011` §7— y entra al expediente como entra cualquier producto de un tercero: declarando quién lo produjo, con qué versión y con qué parámetros. **Un script no aprueba, no marca ` - REVISADO`, no escribe en `1-Documentos recibidos/` y no cita.**

### 4. Fallo declarado, y la oficina nunca es requisito para empezar

Si una herramienta no está, no arranca o falla:

- **El comando sigue funcionando sin ella**, del modo en que funciona hoy, y **lo dice en su salida**.
- **Nunca se supone el resultado de un script que no corrió.** Es la regla 4 de ADR-014 elevada a toda la oficina.

**Motivo:** la usuaria no tiene Python instalado, y **no se le va a pedir que instale nada para poder empezar**. La oficina mejora el resultado; no es la puerta de entrada.

### 5. Las dependencias viven en el directorio persistente, y se instalan solas

Las bibliotecas necesarias —lectura de imágenes, OCR, reconocimiento de voz— **no se piden al usuario**: un guion de preparación las instala bajo `${CLAUDE_PLUGIN_DATA}`, que sobrevive a las actualizaciones del plugin.

**Y se declara lo que cuesta:** son cientos de megabytes de modelos. **La instalación mínima no los baja**; se bajan la primera vez que hacen falta, avisando, **y solo si el usuario dice que sí**.

### 6. Todo lo que entra a la oficina es libre y permite cobrar

Restricción del dueño, sin excepción: **gratuito y con licencia que permita explotación comercial.** Verificado por pieza antes de entrar, y registrado. **Quedan fuera** —ya comprobado— Transkribus, los pesos de Surya, los modelos restringidos de `pyannote` y cualquier peso sin licencia declarada.

### 7. Lo que **no** se decide aquí

- **No se decide meter subagentes, hooks ni MCP.** La plataforma los permite; este ADR abre solo `scripts/` y `bin/`, que es lo que tres capacidades ya construidas necesitan. Lo demás, cuando haya un caso que lo pida.
- **No se decide qué es la versión 1.0** — hueco `V-10`.
- **No cambia dónde se procesa el material que ella abre en la ventana.** Guía §3 sigue vigente y sin tocar: **una herramienta local no convierte la sesión en local.**

## Invariantes derivados

1. **Ninguna capacidad construida depende del Core.**
2. **Todo comando funciona sin la oficina**, peor y diciéndolo.
3. **Toda salida de un script declara productor, versión y parámetros.**
4. **Ningún script escribe en `1-Documentos recibidos/`, en `0-Estado del caso` ni pone la marca ` - REVISADO`.**
5. **Ninguna pieza entra sin licencia libre verificada que permita cobrar.**
6. **Nada de la oficina se descarga sin avisar y sin permiso.**
7. **La automatización no confiere autoridad:** ADR-016 y ADR-017 se aplican igual a lo que produzca la oficina.

## Consecuencias positivas

- **El coste baja donde estaba el 89,6 %.** La lectura mecánica del material sale del presupuesto de fichas.
- **Tres capacidades ya construidas entran al producto** en vez de esperar a una pieza que no existe.
- **Se acaba «que alguien corra un script a mano»**, que era la forma en que ADR-014 admitía que el entregable Word no estaba terminado.
- **Se abre lo que el dueño pidió**: buscar dentro del expediente, transcribir una audiencia, medir el tiempo de ella — todo local y gratis.

## Consecuencias negativas

- **Superficie de ataque nueva.** Un plugin que ejecuta código es un plugin que ejecuta código. Se acota con `allowed-tools` estrecho y scripts que no aceptan rutas arbitrarias.
- **Deja de ser instalar-y-ya.** Aparece Python como dependencia real de la parte buena. La decisión 4 lo contiene, no lo elimina.
- **Dos formas de fallar en vez de una:** el método puede fallar, y ahora también la herramienta. El fallo declarado lo hace visible; no lo evita.
- **Peso.** Cientos de megabytes de modelos, en la máquina de ella.
- **Mantenimiento.** Un `SKILL.md` no se rompe con una actualización del sistema; un script sí.

## Alternativas consideradas

### (a) Seguir como hasta hoy — el dueño corre los scripts a mano
Descartada: es lo que hay, y es la razón de que la pregunta 2 de ADR-014 lleve cinco días abierta. **No escala a una segunda usuaria**, que es el objetivo entero.

### (b) Esperar al Core
Descartada frontalmente. **El Core no existe, nadie lo ha empezado y ninguna de las tres capacidades lo necesita.** Esperarlo fue el error que este ADR corrige.

### (c) Un servidor MCP en vez de scripts
Aplazada, no descartada. Es más limpio para herramientas con estado y **más caro de arrancar**. Para invocar un programa y leer su salida, `scripts/` basta. Se revisará cuando alguna herramienta necesite conservar estado entre llamadas.

### (d) Pedirle a ella que instale Python antes de empezar
Descartada: convierte la primera instalación —que ya es el paso más frágil, con cero ejecuciones— en dos instalaciones. La decisión 4 permite empezar sin nada.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Un script falla en su máquina y el comando se cae | Invariante 2: el comando funciona sin la oficina y lo declara |
| La salida de un script se lee como verificada | Invariante 3 y 7; ADR-016 y ADR-017 siguen enteros |
| `allowed-tools` demasiado ancho concede más de lo que hace falta | Una regla por script, con su ruta exacta. Nunca `Bash(*)` |
| Las descargas sorprenden a la usuaria | Invariante 6: se avisa y se pide permiso |
| La oficina crece sola y nadie la revisa | Cada herramienta entra con su spec de capacidad y su medición |

## Validación / pruebas necesarias

1. **Que un script bundleado corra desde una skill instalada**, con `allowed-tools` y sin pedir permiso. **No hecho: nadie ha instalado el plugin todavía.** Bloquea la aceptación de este ADR.
2. **Medir el ahorro real de fichas** de una pasada con la oficina frente a la de 2026-08-27. Hoy solo hay la estimación del 89,6 %.
3. Comprobar que la instalación de dependencias funciona en una máquina limpia con Windows.
4. Comprobar que un comando **sin** la oficina sigue produciendo su salida y lo declara.

## Relaciones con otros ADRs

- **ADR-014** — **cierra su pregunta abierta 2**: el `.docx` lo genera la skill llamando a un script bundleado. Ni el Core ni nadie a mano.
- **ADR-016** y **ADR-017** — **no se tocan.** La oficina ejecuta el OCR y la transcripción; sus límites y su fallo declarado siguen mandando enteros.
- **ADR-010** — su clasificación de superficie se escribió suponiendo un Core que aún no existe. **Este ADR no la contradice: abre una vía que no contemplaba.** Queda como candidato de enmienda.
- **ADR-012** — instalar sigue siendo operación del programa; **los scripts viven en la zona 1 y jamás escriben en la zona 2.**
- **ADR-001** — la frontera de confianza **no se mueve**: que una herramienta corra local no cambia dónde se procesa lo que ella abre en la ventana.
- **ADR-005** — un script **no aprueba nada**. La autoridad sigue siendo de ella.
