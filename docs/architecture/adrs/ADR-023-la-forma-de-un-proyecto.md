# ADR-023 — La forma de un proyecto: cada programa sabe dónde deja cada cosa

## Estado

**ACEPTADO** en sus tres puntos en disputa (§2), decididos por el dueño el 2026-09-23. El árbol
de §1 es la convención que se aplica desde esa fecha; se revisa si la migración (§5) enseña algo
que no se vio. Lo que sigue abierto está en «Lo que este ADR no decide».

Refina `docs/technical-design/v0/17-deployment-layout.md` §3 (que no es un ADR y marcaba la
estructura por caso como «Requiere aprobación», D-2) y se apoya en `ADR-011` §8 (regenerar es
versión nueva) y `ADR-018` (ningún script escribe en `1-Documentos recibidos/`).

## Contexto

El 2026-09-23, el dueño comparó los dos proyectos de un mismo cliente y pidió estandarizarlos:
*«hay una diferencia muy grande entre un proyecto y el otro»*. El inventario de ese día
(**HECHO VERIFICADO**, carpeta por carpeta y con MD5 en los duplicados):

- Los dos proyectos comparten solo el esqueleto `1-/2-/3-` y una carpeta `_fuentes (no enviar)`
  que **ninguna convención prevé**. A **ninguno** le hay `0-Estado del caso`.
- Dentro de `2-Borradores/`, **seis maneras distintas de guardar versiones**: `previa N - fecha/`,
  `vigente - fecha (etiqueta)/`, `_versiones anteriores/`, sufijos `v2`/`v3`, una carpeta hermana
  `(con detalle)`, y un `_Respaldo/` en la raíz de Despacho que no dice de qué proyecto es.
  **Tres carpetas se llaman «vigente» a la vez.**
- Unos **1,4 GB duplicados** (audios en cinco sitios, WAV intermedios dos veces).
- Siete programas escriben donde se les diga (`--destino`, `--salida` libres): de ahí salen
  `Transcripciones/`, `Voces/`, `Verdad de referencia/`, `Forma del acta anterior/`, cada una
  improvisada en un solo proyecto.
- El plugin **se contradecía a sí mismo**: `construir_entrega.py` escribía las entregas en
  `3-Para presentar/` y la guía de la abogada dice que en esa carpeta la máquina *«no mueve nada
  para allá»*. Y ese mismo día la página «oír y marcar» empezó a guardar en
  `1-Documentos recibidos/`, que es plana y de solo lectura para los programas; se corrigió en
  horas, pero muestra el problema: **sin una forma escrita, cada programa nuevo elige la suya.**

> Una carpeta es una afirmación silenciosa (`PENDIENTE-FORMA-DE-ENTREGA.md`). Seis maneras de
> guardar una versión son seis afirmaciones distintas sobre qué vale y qué no.

## Decisión

### 1. El árbol

```text
<Cliente o área>/
├─ Papelería de la oficina/                  formatos propios: membrete de actas (formato.json, escudo)
└─ <Proyecto>/
   ├─ 0-Estado del caso (no editar).txt      lo escribe estado-del-caso
   ├─ 1-Documentos recibidos/                PLANA · lo que llega · ningún programa escribe aquí
   ├─ 2-Borradores/
   │  ├─ Transcripciones/<AAAA-MM-DD> - <qué cambió>/   transcribir-audio (con datos/)
   │  ├─ Resumenes/<AAAA-MM-DD> - <qué cambió>/
   │  ├─ Actas/                              acta-de-reunion: el acta, «De dónde sale cada frase»,
   │  │                                      la revisión de rigor y la forma del acta modelo
   │  ├─ Compromisos/<AAAA-MM-DD> - <qué cambió>/       A<N> - compromisos.json
   │  ├─ Voces/                              genoma-de-voz, nombrar-voces, verdad de referencia
   │  ├─ Glosario/                           sugerencias de la máquina (hipótesis)
   │  ├─ Entregas/
   │  │  ├─ ENTREGA - <proyecto> - <AAAA-MM-DD>[ (<qué cambió>)]/   y su .zip
   │  │  ├─ _fuentes (no enviar)/            entrega.json, fuentes .md, correos, _generado/
   │  │  └─ _anteriores/                     entregas sustituidas
   │  ├─ Lo que declaré/<ENTREGA …>/         lo que ELLA declara en las páginas (lo escribe la página)
   │  ├─ Lo que declaró ella/                recoger_lo_declarado: su declaración, junta y fechada
   │  ├─ <salidas de una sola pieza>         hechos, cronología, inventarios, escritos… (como ya
   │  │                                      dicen sus skills: «2-Borradores/<Nombre> - <caso> - <fecha>»)
   │  ├─ _anteriores/                        lo sustituido que no vive en una carpeta con fecha
   │  └─ _intermedios (se puede borrar)/     WAV y demás trabajo de máquina regenerable
   └─ 3-Para presentar/                      SOLO lo que ella decide presentar
```

**Cuatro elementos por proyecto, y ni uno más** (`17-deployment-layout` §3.1). Todo lo que la
máquina produce vive en `2-Borradores/`, que es donde la convención ya permitía subcarpetas.

### 2. Las tres decisiones del dueño (2026-09-23)

1. **Las entregas que arma la máquina viven en `2-Borradores/Entregas/`**, no en
   `3-Para presentar/`. Así se cumple la guía: `3-` es de ella. Pasar una entrega a `3-` es un
   acto suyo.
2. **`_fuentes (no enviar)` vive dentro de `2-Borradores/Entregas/`**, no en la raíz del proyecto.
3. **Los proyectos que ya existen se migran**, con un plan que se enseña antes y un manifiesto
   que permite deshacerlo (§5).

### 3. Versiones: una sola manera

- Lo que se regenera por entero (transcripciones, resúmenes, compromisos) va en **una carpeta
  por versión**: `<AAAA-MM-DD> - <qué cambió>`. La fecha es **la de producción**, no la de la
  reunión. **No se usan las palabras «vigente» ni «previa»**: la vigente es la que nombra la
  configuración que la usa (p. ej. `entrega.json`), y si nada la nombra, la más reciente.
- Lo que es una pieza suelta (un acta, un informe) lleva la fecha en el nombre, y **lo sustituido
  va a `_anteriores/`** de su carpeta, nunca se sobrescribe (`ADR-011` §8).
- Una copia idéntica de algo que ya está en su carpeta con fecha **no se deja suelta**: va a
  `_anteriores/` con el nombre de dónde está el original.

### 4. Lo que no se toca

- `1-Documentos recibidos/` es **plana y de solo lectura** para todo programa, la página incluida.
- En `3-Para presentar/` **no escribe ningún programa**.
- El nombre del proyecto no se cambia en la migración.

### 5. Migración con manifiesto

Un programa (`ordenar_proyecto.py`) que:

1. **Lee** el proyecto y **escribe un plan**: cada archivo, de dónde a dónde y por qué; qué
   duplicados encontró (por contenido); qué rutas de configuración y de páginas hay que ajustar.
   **No mueve nada.**
2. Con el plan aprobado por el dueño, **mueve** (nunca copia y borra; nunca borra), ajusta las
   rutas de `entrega.json` y las rutas relativas de las páginas, y **deja un manifiesto**
   (`2-Borradores/_anteriores/ordenado - <fecha>.json`) con cada movimiento, para deshacerlo con
   el mismo programa.
3. Se detiene si un destino ya existe, si un archivo está abierto o si una ruta queda fuera del
   proyecto.

### 6. Cómo se hace cumplir

- Las rutas están **en un solo sitio** (`plugins/despacho/scripts/estructura.py` y su gemela en
  la página, `guardado.js`), y los programas las toman de ahí en vez de pedir `--destino`.
- Las skills nombran la carpeta de cada salida con este árbol.
- Una prueba comprueba que ningún programa ni skill nombre `3-Para presentar` como destino ni
  escriba en `1-Documentos recibidos`.

## Consecuencias

- **La página «oír y marcar» detecta el proyecto por `…/2-Borradores/Entregas/ENTREGA - …/`** (y
  por la forma antigua `…/3-Para presentar/ENTREGA - …/`, mientras quede alguna) y guarda en
  `2-Borradores/Lo que declaré/<entrega>/`. Una entrega suelta, fuera de un proyecto, guarda
  dentro de sí misma, como hasta ahora.
- **Coste:** la ruta de una entrega se alarga un nivel, y las entregas ya enviadas por correo
  siguen diciendo en sus notas la forma antigua (no se reescriben: son lo que se envió).
- **Coste:** un programa con destino fijo es menos flexible. Es la intención: la flexibilidad es
  lo que produjo seis maneras de guardar una versión.

## Lo que este ADR no decide

- El nivel `Casos/` entre oficina y caso, y el nombre `AAAA-NNN partes` (`17` §3.2, DP-8).
- Si `_intermedios (se puede borrar)/` debe vivir fuera del proyecto (en la zona del sistema) para
  que no viaje con él: hoy pesa cientos de MB por grabación.
- Los proyectos de otros clientes con subcarpetas dentro de `1-Documentos recibidos/`: se
  **señalan** en el plan, no se aplanan sin que ella lo diga (son material recibido).
