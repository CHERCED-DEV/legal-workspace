# SPEC-01 — Instalación del plugin desde el remoto

**Estado:** en ejecución · **Cierra:** `EP-ENTRADA-0` (entrada 0 del backlog) y `H-10`

---

## 1. Qué problema cierra

`EP-ENTRADA-0` lleva tres fases abierto y es el número 1 de los diez que más pesan:

> *«El plugin está escrito y empaquetado pero no publicado: no hay remoto, luego no hay URL de marketplace que la abogada pueda añadir.»*

El 2026-08-31 se publicó el repositorio. **El remoto ya existe**, así que por primera vez se puede intentar lo que `H-10` dejó `POR VERIFICAR`:

> *«Nadie ha comprobado si los comandos aparecen como `/cronologia` o como `/despacho:cronologia`; la guía publica la forma corta como fiable.»*

Y esa comprobación **bloquea imprimir la guía para la abogada**, porque hoy la guía afirma una forma que nadie ha visto funcionar.

## 2. Comportamiento observable

Lo que la abogada tiene que poder hacer, en su idioma:

1. Añade una dirección —una sola— y el sistema le dice que encontró el despacho.
2. Instala, y ve confirmación de que quedó instalado.
3. Escribe una barra `/` y **aparecen los nueve comandos en la lista**, con un nombre que ella reconoce.
4. Ejecuta uno sobre una carpeta de caso y **produce la salida que su `SKILL.md` describe**.

**El nombre con el que aparecen es un observable, no un detalle:** si aparecen como `/despacho:cronologia` y la guía dice `/cronologia`, la guía está mal y hay que corregirla antes de imprimirla.

## 3. Reglas duras

| # | Regla | De dónde sale |
|---|---|---|
| R-1 | **La instalación no escribe en la carpeta de ningún caso.** Instalar es una operación del programa, no del expediente | ADR-012, zonas 1 y 2 disjuntas |
| R-2 | **Ningún dato de caso viaja al repositorio.** Verificado: el expediente vive fuera de git y sigue fuera | ADR-002 · comprobado el 2026-08-31 |
| R-3 | **La guía que ella lee no puede afirmar una forma de invocación que nadie haya visto.** Si no se comprueba, se dice que no se comprobó | `H-10`, y la regla de veracidad del proyecto |
| R-4 | **La versión del plugin identifica lo instalado.** Si se corrige algo, sube la versión: sin eso nadie sabe qué está corriendo en su máquina | ADR-012, actualización |

## 4. Qué NO hace

- **No instala el Core.** No existe, y ninguno de los nueve comandos lo necesita: son texto puro.
- **No configura conectores, MCP ni credenciales.**
- **No migra nada** de las pasadas hechas a mano.
- **No garantiza que los comandos funcionen bien** — solo que **aparecen y se pueden invocar**. Que hagan bien su trabajo es cosa de cada `SKILL.md` y de su propia comprobación.

## 5. Cómo se sabe que quedó

Observables, en orden. **Cada uno puede fallar**, y si falla se dice cuál.

| # | Observable | Quién puede comprobarlo |
|---|---|---|
| O-1 | `marketplace.json` y `plugin.json` son JSON válido y sus rutas resuelven a carpetas que existen | Yo, sin instalar nada |
| O-2 | Las nueve carpetas de `skills/` tienen `SKILL.md` con `name`, `description` y `version` en su encabezado | Yo |
| O-3 | El `name` de cada `SKILL.md` **coincide con el nombre de su carpeta** — si no, la invocación puede resolver a otra cosa | Yo |
| O-4 | El repositorio remoto sirve esos archivos: se clona en limpio y están todos | Yo |
| O-5 | **La dirección se añade como marketplace y el sistema encuentra el plugin** | **Solo en su máquina** |
| O-6 | **Los nueve comandos aparecen al escribir `/`, y con qué nombre exacto** | **Solo en su máquina** |
| O-7 | Un comando se ejecuta y produce la salida que su `SKILL.md` describe | Solo en su máquina |

> **O-1 a O-4 los cierro yo ahora. O-5 a O-7 no puedo cerrarlos: ocurren dentro de su cliente.** Lo digo aquí para que no queden marcados como hechos cuando no lo están — que es exactamente el defecto que `H-10` denuncia.

## 6. Qué toca

| Archivo | Qué |
|---|---|
| `.claude-plugin/marketplace.json` | Se verifica; se corrige solo si O-1 falla |
| `plugins/despacho/.claude-plugin/plugin.json` | Idem. **Su `description` menciona cinco capacidades y hay nueve comandos** |
| `plugins/despacho/skills/*/SKILL.md` | Solo se leen los encabezados (O-2, O-3) |
| `plugins/despacho/GUIA-PARA-LA-ABOGADA.md` | **Se corrige después de O-6**, con la forma de invocación real |
| `plugins/despacho/README.md` | `H-08` dice que su árbol dibuja un plugin que ya no es el que hay |

---

## Ejecución — 2026-08-31

| Observable | Resultado | Cómo se comprobó |
|---|---|---|
| **O-1** · JSON válido, rutas resuelven | **PASA** | `marketplace.json` → `plugins/despacho`, existe. `plugin.json` válido, `name=despacho` |
| **O-2** · Los nueve `SKILL.md` con encabezado completo | **PASA** | 9 de 9 con `name`, `version` y `description` de 390 a 670 caracteres |
| **O-3** · `name` coincide con el nombre de la carpeta | **PASA** | 9 de 9 coinciden. Ninguna invocación resolvería a otra cosa |
| **O-4** · El remoto sirve todo: clon en limpio | **PASA** | Clonado desde GitHub: 71 commits, los nueve `SKILL.md`, README, guía y `plugin.json` presentes |
| **R-2** · Ningún dato de caso viajó | **PASA** | Siete patrones buscados en el clon público: cero ocurrencias |
| **O-5** · La dirección se añade como marketplace | **Pendiente — solo en su máquina** | — |
| **O-6** · Los nueve comandos aparecen al escribir `/` | **Pendiente — solo en su máquina** | — |
| **O-7** · Un comando se ejecuta y produce su salida | **Pendiente — solo en su máquina** | — |

**Lo que la ejecución encontró y no estaba previsto:**

> **La `description` de `plugin.json` nombra cinco capacidades y el plugin tiene nueve comandos.** Es el texto que la abogada lee al instalar, así que le describe un producto más pequeño del que va a recibir. *No se corrige aquí:* cambiar lo que se instala sin subir la versión violaría R-4, y la versión está deferida al §7. **Queda como defecto abierto de esta spec**, no como algo hecho.

**Estado: parcialmente ejecutada.** Todo lo verificable sin instalar está cerrado. Lo que falta ocurre dentro del cliente de la usuaria y **nadie puede darlo por hecho hasta que alguien lo vea**.

---

## 7. Qué queda fuera y por qué

- **Publicar en un marketplace público o registro de plugins.** No hace falta: se instala desde la dirección del repositorio.
- **Instalar en la máquina de ella.** Es el paso siguiente y no lo hago yo; hace falta que alguien esté delante de esa máquina.
- **Corregir los defectos de contenido de los `SKILL.md`** (`H-01`, `H-02`, `H-07`…). Cada uno tiene o tendrá su spec. **Esta solo se ocupa de que lleguen.**
- **La versión.** Sigue en `0.1.0` con nueve comandos cuando se publicó con seis. Subirla es correcto, pero **debe hacerse cuando se decida qué es la primera versión** (hueco V-10), no antes y no por inercia.
