# SPEC-11 — La primera instalación: que empezar no dependa de preguntar

**Estado:** ejecutada salvo lo que ocurre en su máquina · **Cierra:** `H-08` · el defecto abierto de SPEC-01 · parte de `EP-ENTRADA-0` · **Familia:** defecto

---

## 1. Qué problema cierra

La pregunta era **cómo empezamos**, y al buscar la respuesta apareció que no está escrita en ninguna parte.

### Defecto 1 — Nadie ha escrito cómo se instala

`GUIA-PARA-LA-ABOGADA.md` empieza así, en su tercera línea:

> *«Quien le instaló esto debe mostrarle en qué ventana escribe y en qué carpeta quedaron sus casos. **Esta guía empieza cuando eso ya está hecho.**»*

Correcto como decisión de alcance —la guía es para usar, no para instalar—. **El problema es que el documento que debía empezar donde esa acaba no existe.** El `README.md` es para quien desarrolla el plugin, no para quien lo instala una vez.

**Resultado:** el paso número uno del producto es el único sin instrucción escrita. Con **cero instalaciones fuera de la máquina del dueño**, es literalmente lo que impide empezar.

### Defecto 2 — Todo lo que ella leería describe un producto más pequeño del que recibiría

**Comprobado el 2026-09-01:**

| Documento | Cuántos comandos describe | Cuáles faltan |
|---|---|---|
| `plugin.json` — *lo que ella lee al instalar* | **5 capacidades** | Nombra por rasgos, no cubre |
| `marketplace.json` — *lo primero que se ve* | **5 capacidades** | Idem |
| `GUIA-PARA-LA-ABOGADA.md` §1 | **6** | `inventario-de-bienes` · `preguntas-de-derecho` · `revision-de-rigor` |
| `README.md` — prosa | **«seis métodos»** (7 veces) | La tabla lista 8: falta `revision-de-rigor` |
| **La realidad** | **9** | — |

> **Tres comandos son invisibles en todo lo que se lee antes de usarlo**, y uno de ellos —`revision-de-rigor`— es el que se construyó con su propio ADR hace cinco días.

Este es el defecto que SPEC-01 encontró y **deliberadamente no arregló**, razonando que cambiar lo instalado sin subir la versión violaría R-4.

> **Ese razonamiento era una precaución mal aplicada, y se corrige aquí.** R-4 no dice «no cambies»: dice **«si cambias, sube la versión»**. La versión aplazada al hueco `V-10` es *cuál es la versión 1.0*, que es una decisión de producto — no si se puede pasar de `0.1.0` a `0.2.0`. **Y el propio `README.md` §5 ya lo decía:** *«sí conviene subir `version` en `plugin.json`»*. Las nueve skills subieron versión ayer por esta misma regla; el `plugin.json` se quedó sin subir por una cautela que no tenía fundamento.

### Lo que se comprobó y **no** era un defecto

`H-10` decía: *«la guía publica la forma corta `/cronologia` como fiable»*. **Falso.** La guía ya advierte, en §1:

> *«Puede que en su pantalla no aparezcan exactamente así, sino con `despacho:` delante […] escriba la barra sola y espere un segundo; sale la lista […] con el nombre que tienen en su máquina.»*

**Es el cuarto ítem del backlog que resulta mal contado al leerlo contra el archivo.** Se corrige en su sitio.

## 2. Comportamiento observable

1. Quien vaya a instalarlo abre **un** documento y sabe qué hacer, en orden, sin preguntar.
2. Ese documento dice **qué pasos nadie ha ejecutado todavía** y qué hacer si la pantalla no coincide.
3. Al instalar, la descripción que aparece **nombra los nueve comandos**, no cinco rasgos.
4. La guía de ella lista **los nueve**, con el suyo en su idioma.
5. La versión instalada **cambia** cuando cambia lo que se instala.

## 3. Reglas duras

| # | Regla | De dónde sale |
|---|---|---|
| R-1 | **Ningún paso se escribe como comprobado si nadie lo ha ejecutado.** Se escribe, y se marca sin comprobar | SPEC-01 R-3 · `H-10` |
| R-2 | **La versión sube cuando cambia lo que se instala** | SPEC-01 R-4 · `README` §5 |
| R-3 | **La instalación no escribe en la carpeta de ningún caso** | ADR-012 · SPEC-01 R-1 |
| R-4 | **Lo que se describe es lo que hay: ni un comando de más ni de menos** | `H-08` |
| R-5 | **La hoja de instalación no repite la guía de uso.** Termina donde la guía empieza | El alcance que la guía ya fijó |

## 4. Qué NO hace

- **No instala nada.** Nadie puede instalar en una máquina ajena desde aquí.
- **No decide dónde se procesa el material.** Eso ya está dicho en la guía §3 y es decisión de ella.
- **No decide qué es la versión 1.0** — sigue siendo el hueco `V-10`.
- **No arregla los `POR COMPROBAR` del README.** Los deja donde están, que es lo honesto.

## 5. Cómo se sabe que quedó

| # | Observable | Resultado |
|---|---|---|
| O-1 | Existe una hoja de instalación, y la guía de ella la nombra | **PASA** |
| O-2 | `plugin.json` y `marketplace.json` nombran los nueve | **PASA** |
| O-3 | La guía §1 lista los nueve | **PASA** |
| O-4 | `README.md` no dice «seis» donde hay nueve | **PASA** |
| O-5 | `plugin.json` subió de versión | **PASA** — `0.1.0` → `0.2.0` |
| O-6 | Los JSON siguen siendo válidos y sus rutas resuelven | **PASA** |
| O-7 | **Alguien sigue la hoja y el plugin queda instalado** | **Pendiente — solo en su máquina** |
| O-8 | **Los nueve comandos aparecen, y con qué nombre** | **Pendiente — solo en su máquina** |

## 6. Qué toca

| Archivo | Qué |
|---|---|
| `plugins/despacho/INSTALACION.md` | **Nuevo.** La hoja: qué se necesita, los pasos, qué mirar, qué hacer si falla |
| `plugins/despacho/.claude-plugin/plugin.json` | Descripción de los nueve · versión `0.2.0` |
| `.claude-plugin/marketplace.json` | Descripción de los nueve |
| `plugins/despacho/GUIA-PARA-LA-ABOGADA.md` | §1 con los nueve · enlace a la hoja |
| `plugins/despacho/README.md` | «seis» → nueve · `revision-de-rigor` en la tabla |
| `docs/BACKLOG-CONSOLIDADO.md` | `H-10` mal contado |

## 7. Qué queda fuera y por qué

- **Ejecutar la instalación.** Es el punto entero: hace falta alguien delante de esa máquina. **O-7 y O-8 quedan abiertos y no se cierran con un commit.**
- **Qué es la versión 1.0.** Hueco `V-10`. Van cuatro specs esperándolo.
- **Los dos `POR COMPROBAR` del README** —el prefijo de los comandos y el `.docx` en su entorno—: se comprueban en la primera sesión real, no antes.
- **Verificar cada paso de la hoja.** Están escritos desde el mecanismo conocido de instalación de plugins, **no desde haberlos ejecutado**. R-1 obliga a decirlo, y la hoja lo dice en su primera línea.
