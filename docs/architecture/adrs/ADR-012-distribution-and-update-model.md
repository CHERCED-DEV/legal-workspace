# ADR-012 — Modelo de distribución y actualización: repositorio clonado, tres zonas posicionalmente separadas y arranque que migra o no arranca

## Estado

Proposed

## Contexto

Los dueños han fijado el modelo de distribución (**DECISIÓN APROBADA**, sesión de diseño de distribución): todo el programa vive en un **repositorio de GitHub**; en la máquina de la abogada se **clona**; ella abre Cowork y trabaja, y el Claude que ya tiene usa por debajo el **MCP local** que construimos; las actualizaciones llegan por **`git pull`**, con el requisito literal de *«que siempre funcione bien, que no borre nada, que no se pierdan las memorias, que no rompa los expedientes, que todo siga estable»*; la estructura de carpetas debe ser legible para ella (*«aquí pones los anexos, aquí las demandas, aquí la oficina tal»*); los `memory.md` pueden ir por caso, en la carpeta del caso, advirtiéndole que no debe tocarlos; y el coste de mantenimiento debe tender a cero.

Ese enunciado es correcto en su intención y **mezcla dos zonas que son tres**. La corrección ya está acordada con los dueños y es el punto de partida de este ADR:

| Zona | Contenido | Quién escribe | ¿Bajo git? | ¿La ve Cowork? |
|---|---|---|---|---|
| **1 — PROGRAMA** | Core, Legal MCP, skills, migraciones, configuración sellada, manifest | Release (`git pull`) | **Sí** — es el working tree | **No** |
| **2 — ESCRITORIO DE ELLA** | Anexos que aporta, borradores, entregables, proyecciones materializadas | Ella, y el Core solo para materializar proyecciones | **No** | **Sí** — es su zona de trabajo |
| **3 — EXPEDIENTE** | `case.db`, Sources originales, Case Event Log, derivados, índices, integrity metadata | **Solo el Core** | **No** | **No** |

Las tres se corresponden exactamente con los tres ciclos de vida ya fijados en `boundaries.md` §10 (Runtime / Configuration / Workspace + Private State) y con la frontera de ADR-002 (USER WORKSPACE / LEGAL OS PRIVATE STATE). Este ADR no inventa una frontera nueva: **le da posición física y mecanismo de actualización a una frontera que ya era Accepted**, y decide qué se distribuye, cómo se actualiza y qué ocurre con los datos cuando el programa cambia.

Lo que hace que el problema no sea trivial es que `git` es una herramienta destructiva por diseño sobre su propio working tree, y que la protección habitual —`.gitignore`— **no protege de lo que hace falta protegerse**. **HECHO VERIFICADO** (documentación oficial de git: `git-clean`, `git-reset`, `git-merge`, `githooks`; re-verificación empírica en la máquina Windows objetivo exigida en D-01…D-03):

1. `git clean -fdx` **elimina también los archivos ignorados**. Un expediente colocado dentro del working tree y protegido solo por `.gitignore` es exactamente el caso que ese comando borra.
2. `git reset --hard` descarta modificaciones de archivos *trackeados* y no toca los no trackeados; `git checkout` de otra rama **rehúsa** sobrescribir archivos no trackeados. Es decir: el daño no viene del comando más temido, sino del comando de limpieza — que es el que alguien ejecuta *para arreglar* un problema.
3. Los hooks viven en `$GIT_DIR/hooks` y **no se copian al clonar**. Un hook de protección versionado en el repositorio no está activo en el clon salvo que algo lo instale o redirija `core.hooksPath`. Por tanto **un hook no puede ser la frontera**; a lo sumo es defensa en profundidad.
4. `git pull --ff-only` rehúsa integrar cuando el avance no es fast-forward, en vez de abrir un merge con conflictos.

De (1) y (3) se sigue la tesis central: **la separación entre el programa y los datos de clientes tiene que ser posicional —árboles distintos, ninguno descendiente de otro— y no una regla dentro de un mismo árbol.** Es el mismo razonamiento que el spike de Cowork obligó a aplicar a la zona 3: **HECHO VERIFICADO** (`docs/research/cowork-runtime-spike-v0.md`, A-02; fuente: `/docs/third-party/claude-desktop/local-access`) que Cowork **no tiene deny por ruta** y que adjuntar una carpeta concede su árbol completo, siendo el único remedio documentado el posicional: *"To keep data out of reach entirely, leave it outside the allowed roots."* Dos superficies distintas (git y Cowork), ninguna de las dos con reglas fiables por ruta, y la misma respuesta: **posición, no regla**.

Hechos de plataforma adicionales que condicionan este diseño, todos del spike de Cowork:

- **HECHO VERIFICADO** (B-01, B-02): los servidores MCP locales funcionan **solo en Desktop** y corren **en el host**, como proceso del sistema operativo, no dentro de la VM Linux del shell.
- **HECHO VERIFICADO** (D-05): Cowork *"doesn't read the Claude Code CLI's `~/.claude` directory"*. Ninguna regla `deny`, `allowedTools` ni hook de usuario de Claude Code gobierna Cowork.
- **HECHO VERIFICADO** (B-07, B-08): los plugins de Cowork pueden traer conectores MCP, skills, subagentes, slash commands y hooks en un solo paso, con habilitación por **componente** (no por tool).
- **HECHO VERIFICADO** (B-09): la política por tool (`allow`/`ask`/`blocked`) existe **solo** con configuración gestionada por administrador (MDM, planes Team/Enterprise).
- **HECHO VERIFICADO** (modo Auto): Cowork delega la decisión de seguridad en el propio modelo. Cowork **no es una frontera de seguridad**; es defensa en profundidad. La frontera es el Core.
- **`INCONCLUSIVE` y BLOQUEANTE (B-04)**: **no está documentado** si un servidor MCP local está o no sujeto al confinamiento de las carpetas adjuntadas. De ello depende que la zona 3 pueda estar fuera del alcance de Cowork y simultáneamente ser leída por el Core.

**SUPUESTO DECLARADO — B-04 favorable.** Todo el diseño de este ADR asume que el proceso del MCP local, por ser proceso del host con los privilegios de la cuenta del sistema operativo (B-02, `VERIFIED`), **puede alcanzar rutas fuera de las carpetas adjuntadas**. Es una hipótesis con base fuerte, **no un hecho**. La §*Decisión 9* trae el plan de contingencia obligatorio si resulta desfavorable.

Lo que este ADR **no** reabre: la frontera de confianza (ADR-001), el perímetro y el camino único de acceso (ADR-002), el estatuto de las proyecciones (ADR-004), la autoridad humana (ADR-005), el layout interno del case store (ADR-007) ni la superficie MCP (ADR-010). Lo que sí hace es **darles domicilio**.

---

## Decision

### 1. Tres raíces disjuntas: ninguna zona es descendiente de otra

La unidad de separación es la **raíz de árbol**, no la carpeta ni la regla. Las tres zonas se materializan en tres raíces tales que **ninguna es ancestro de ninguna otra**, y ese predicado se comprueba en el arranque sobre rutas **canónicas resueltas** (con enlaces simbólicos y junctions ya resueltos), no sobre las cadenas de texto.

**Ejemplo ilustrativo, NO-PRODUCCIÓN — las rutas concretas son detalle de despliegue, no decisión de arquitectura (ADR-002, alternativa 2 rechazada):**

```text
ZONA 1 — PROGRAMA  (el ÚNICO working tree de git de la máquina)
C:\LegalOS\programa\
├─ .git\
├─ core\                       Core, Application, Domain
├─ mcp\                        servidor MCP local (legal-mcp)
├─ skills\
├─ migrations\                 numeradas, solo-adelante (ADR-007 / boundaries §10)
├─ plantillas\                 ORIGEN sellado de "3 Plantillas" de la zona 2
├─ config-schema\              ESQUEMA de la Client Config. Nunca sus valores.
├─ scripts\
│   ├─ arrancar.*              lo que dispara el acceso directo
│   └─ restaurar-programa.*    descarta cambios locales del programa. Nunca toca zonas 2 y 3.
├─ manifest.*                  hashes del producto sellado (boundaries §10, punto 3)
└─ VERSION                     semver; coincide con el tag de git

ZONA 2 — ESCRITORIO DE ELLA  (la ÚNICA carpeta que se adjunta a Cowork)
C:\Escritorio Legal\
└─ (ver Decisión 6)

ZONA 3 — EXPEDIENTE  (estado canónico; solo el Core)
%LOCALAPPDATA%\LegalOS\
├─ instalacion.json            puntero de instalación: nombra las tres raíces
└─ estado\
    ├─ cases\<case_id>\case.db + blobs\      (layout de ADR-007)
    ├─ catalog.db · operational.db
    ├─ config.local.*          Client Config con SUS valores + nombres de oficina
    ├─ backups\                copias verificadas previas a migración
    └─ integrity\
```

Tres consecuencias buscadas, cada una cerrando un riesgo concreto del encargo:

- **`git clean -fdx` en la zona 1 no puede alcanzar un byte de las zonas 2 y 3**, porque no están ahí. No hay `.gitignore` que confiar.
- **`git push` no puede subir documentos de clientes**, porque no hay documentos de clientes dentro del working tree que puedan quedar staged.
- **Adjuntar la zona 2 a Cowork no concede la zona 3 ni la zona 1**, porque no son descendientes suyas.

`.gitignore` se mantiene, con entradas defensivas para nombres de carpeta de datos, **declarado explícitamente como defensa en profundidad y jamás como la frontera**. Un `.gitignore` presentado como protección es peor que ausente: produce la confianza sin la propiedad.

### 2. La ubicación de las zonas 2 y 3 **no depende de dónde se clone el repositorio**

Esta es la decisión que cierra el riesgo de la nube (Decisión 8) y, de paso, la clase entera de errores "clonó en otro sitio y se rompió todo".

El clon puede estar donde sea. Las zonas 2 y 3 **las fija la instalación**, una sola vez, en rutas locales de máquina, y quedan registradas en un **puntero de instalación** (`instalacion.json` del ejemplo) que vive en una ruta local conocida y **fuera de las tres zonas de trabajo**: no está en el repositorio (no puede entrar en conflicto en un `pull`), no está en la zona 2 (ella no puede romperlo sin querer y el modelo no lo alcanza), y resuelve el arranque en frío —el lanzador necesita saber dónde está la zona 3 *antes* de poder leer nada de la zona 3—.

El puntero contiene rutas, no secretos. Si alguien lo lee, aprende dónde están las carpetas; no obtiene acceso a ellas.

### 3. La actualización es `git pull --ff-only`, es un acto humano explícito y **nunca ocurre en mitad de una sesión**

- **Solo fast-forward.** Ante divergencia, el proceso **se detiene y lo dice**; no abre un merge, no resuelve conflictos, no reintenta con estrategias. Un merge automático en el árbol del programa produciría un producto que no corresponde a ningún release y cuyo manifest de integridad no cuadraría.
- **Un solo acceso directo**, «Iniciar Legal OS». Al arrancar, y **antes** de abrir ningún `case.db`, el lanzador comprueba si hay versión nueva y **le pregunta a ella** si aplicarla. Sí ⇒ actualiza y continúa el arranque completo (Decisión 4). No ⇒ arranca con la versión actual. Sin red ⇒ arranca con la versión actual y lo dice.
- **Nunca automática, nunca en segundo plano, nunca a mitad de trabajo.** Esto no contradice el *"sin auto-update"* de `boundaries.md` §10: preguntar y esperar un acto humano no es auto-update. Lo que §10 excluye —firma de código, telemetría, canales de release— sigue excluido de V0.
- **Nunca con el Core corriendo.** Un lock de instancia única impide actualizar mientras hay una sesión abierta; en Windows los archivos en uso producen fallos parciales de actualización, que es la peor forma de fallo posible aquí.
- **Nunca la ejecuta el modelo.** Ver Decisión 7.

Si el working tree está sucio (ella abrió y guardó un archivo del programa por curiosidad), el `pull` se rechaza y el arranque **lo reporta en su idioma** y ofrece la acción soportada «restaurar programa», que descarta los cambios locales del programa y **no toca las zonas 2 y 3**. Nunca se hace un `reset --hard` silencioso "para desatascar".

### 4. El arranque **migra o no arranca**: secuencia obligatoria y ordenada

`git pull` no migra nada. Todo lo que hace que una actualización sea segura ocurre en el arranque, en este orden y con estas condiciones de parada. **Pseudocódigo ILUSTRATIVO, NO-PRODUCCIÓN:**

```text
ARRANQUE  (lo dispara ella con el acceso directo; nunca el modelo)

 0. tomar lock de instancia unica            -> si ya hay una, no arrancar segunda
 1. leer puntero de instalacion              -> ausente o ilegible => NO ARRANCA (instalacion rota)
 2. resolver las tres raices a ruta canonica
    comprobar disjuncion (ninguna ancestro de otra, tras resolver enlaces)
                                             -> falla => NO ARRANCA
 3. comprobar que zona 3 es almacenamiento local y NO sincronizado (Decision 8)
                                             -> falla => NO ARRANCA EN ESCRITURA
 4. si hay version nueva -> PREGUNTAR -> si acepta: git pull --ff-only
                                             -> no fast-forward => se detiene, sigue version anterior
 5. verificar manifest de integridad del producto sellado (zona 1)
                                             -> falla => solo lectura, y lo dice (boundaries §10.7)
 6. leer schema_version esperada por el producto
    para cada case.db:
       igual        -> OK
       menor        -> backup -> VERIFICAR el backup -> migrar -> verificar -> OK
                       backup no verificado => NO MIGRA, ese Case en solo lectura
                       fallo a mitad        => restaurar backup, ese Case en solo lectura
       mayor        -> SOLO LECTURA. Nunca migracion hacia atras. (ver abajo)
 7. materializar zona 2: crear lo que falte, NUNCA sobrescribir lo que exista (Decision 6)
 8. arrancar el servidor MCP local
 9. mostrarle una tarjeta de estado: version, cuantos expedientes, cuales en solo lectura y por que
```

Cuatro reglas duras dentro de esa secuencia:

- **El backup se verifica, no solo se escribe.** Verificar significa, como mínimo (`ADR-007`, V10): restaurar la copia a ubicación aislada, comprobar integridad, **verificar la cadena de eventos sobre la copia**, comparar conteos por tabla y `schema_version`. Solo un veredicto positivo habilita migrar.
- **La unidad de migración es el Case.** Un fallo compromete un expediente, no todos. Un conjunto en estados mixtos es un resultado aceptable y **declarado**, no un accidente que se oculta (ADR-007, R3, invariante 9).
- **`schema_version` mayor que la esperada ⇒ solo lectura, jamás migración hacia atrás.** Este caso no es teórico: es lo que ocurre cuando se vuelve a una versión anterior del programa (`git checkout` de un tag previo) sobre datos ya migrados. Las migraciones son solo-adelante y no existe down-migration (`boundaries.md` §10, punto 5).
- **La degradación es visible.** Ningún `case.db` se abre en escritura "a ver si funciona". El sistema deja de escribir y lo dice (`boundaries.md` §10, punto 7).

**Registro de la migración.** Una migración reescribe almacenamiento canónico y por tanto **debe quedar registrada**; pero la lista de eventos del Case Event Log está **cerrada en V0** (kernel §8.1) y este ADR **no inventa un evento nuevo**. En V0 la migración se registra en el **plano administrativo/operacional** (fuera de la superficie del modelo, ADR-002). Si debe existir un evento canónico `SchemaMigrated`, es un cambio de contrato y requiere su propio ADR — queda como pregunta pendiente 6, con la misma disciplina que ADR-011 aplicó a los eventos de re-anclaje.

### 5. La configuración local **no vive en el working tree**

El repositorio transporta **esquemas y valores por defecto**; nunca los valores de ella. Sus valores —rutas de zonas, nombres de oficina, preferencias, políticas `require_*` de la Client Config— viven en la zona 3.

Esto no es una preferencia de organización: es lo que **elimina por construcción** la clase de riesgo "conflictos de merge en configuración local". Un archivo de configuración versionado y editado localmente **es** un conflicto de merge esperando el siguiente `pull`; sacarlo del árbol lo convierte en un archivo que git no ve, no compara y no puede pisar. Y refuerza la regla ya vigente de `boundaries.md` §7: una configuración inválida se rechaza de forma visible y **la configuración solo endurece**.

### 6. La zona 2 en el idioma de ella, y el Core **nunca sobrescribe** nada suyo

`Inbox/`, `Working/` y `Exports/` de ADR-002 son **regímenes de contenido, no nombres de carpeta**. Esta es su materialización en nombres que una profesional no técnica entiende sin explicación. **Árbol ILUSTRATIVO — la estructura concreta es DECISIÓN PENDIENTE a validar con la profesional (pregunta 7):**

```text
C:\Escritorio Legal\
├─ 1 Bandeja de entrada\                 lo que llega y aun no es de ningun caso
├─ 2 Casos\
│   ├─ Oficina Bogota\
│   │   └─ 2026-014 Perez vs Constructora XYZ\
│   │       ├─ Anexos y pruebas\         lo que usted aporta al caso
│   │       ├─ Borradores\               lo que estamos escribiendo
│   │       ├─ Documentos finales\       lo que sale listo para radicar
│   │       ├─ memoria-del-caso.md       LO ESCRIBE EL SISTEMA - no lo edite
│   │       └─ mis-notas.md              SUYO - escriba aqui lo que quiera
│   └─ Oficina Medellin\
├─ 3 Plantillas\                         copia de solo lectura, viene del programa
└─ LEEME - como funciona esto.txt
```

Correspondencia con la frontera Accepted:

| Régimen (ADR-002) | Lo que ve ella |
|---|---|
| `Inbox/` | `1 Bandeja de entrada\` y, dentro de cada caso, `Anexos y pruebas\` |
| `Working/` | `Borradores\` |
| `Exports/` | `Documentos finales\` |
| Proyección materializada (ADR-004) | `memoria-del-caso.md` |
| — (espacio propio, sin régimen) | `mis-notas.md` |

Cinco reglas:

1. **Nada de la zona 2 es canónico** (ADR-002 inv. 1). Es entrada aún no incorporada, borrador o salida regenerable.
2. **El Core crea lo que falta y jamás sobrescribe lo que existe.** Si ella renombra, mueve o borra una carpeta suya, el arranque la recrea vacía; ninguna operación del Core falla por eso, porque nada canónico depende de la zona 2.
3. **`memoria-del-caso.md` es proyección derivada y regenerable, nunca fuente** (ADR-004). El Core la reescribe; **no la lee jamás como entrada** y **no es objetivo de escritura del modelo**. Lleva encabezado en español diciendo exactamente eso.
4. **`mis-notas.md` existe precisamente porque (3) es cierto.** Si el único archivo de texto del caso es uno que el sistema reescribe, ella escribirá ahí y perderá lo escrito. Darle un archivo propio, contiguo, cuesta una línea de código y cierra el modo de fallo.
5. **La partición por oficina es convención humana, no mecanismo.** El agrupamiento canónico vive en el estado, no en el árbol de carpetas (mismo criterio que `boundaries.md` §8 aplica a los Knowledge Packs). Mover un caso de carpeta no cambia nada canónico, y no debe romper nada.

**Sobre *«que no se pierdan las memorias»*:** la respuesta honesta que hay que darle, en sus términos, es que **la memoria no vive en ese archivo**. Vive en el expediente (zona 3), del que el `.md` es una vista impresa. Por eso el archivo puede regenerarse tras cualquier actualización sin que se pierda nada — y por eso lo que ella escriba *dentro* de él sí se pierde.

### 7. El modelo no ejecuta el arranque, ni la actualización, ni la migración

Ninguna de estas operaciones —`git pull`, lanzar el Core, migrar, verificar backups, restaurar, escribir el puntero de instalación— está en la superficie MCP. La clase `ADMIN` **permanece vacía por diseño** (ADR-010, decisión 3; kernel §4) y este ADR **no la abre**. No hay tool que las exponga, y por tanto no hay nada que el modelo pueda invocar, encadenar ni pedir que se le autorice.

Consecuencia práctica: **ella lo ejecuta una vez, con un acceso directo, no con una terminal.** No se le pide que escriba comandos, no se le pide que interprete la salida de git, y no se le pide que decida entre estrategias de merge. Lo único que se le pide es un sí/no ante una pregunta en español (Decisión 3).

Esto es consistente con ADR-001: el LLM es cliente externo no confiable, no ejecuta comandos, no escribe estado y no fabrica autorizaciones. Un modelo capaz de correr `git` sería un modelo capaz de reescribir el producto que lo restringe.

### 8. La nube personal se trata como riesgo de primer orden, no como nota al pie

Que la usuaria clone —o después *mueva, o "respalde" copiando*— el árbol a una carpeta sincronizada con OneDrive o Google Drive es el escenario más probable de daño real, porque **no parece un error**: parece prudencia.

**HECHO VERIFICADO** (documentación de Microsoft sobre OneDrive *Known Folder Move*): existe una configuración —habitualmente ofrecida y con frecuencia activada en equipos con cuenta Microsoft— que **redirige `Escritorio`, `Documentos` e `Imágenes` al árbol de OneDrive**. **POR VERIFICAR** si está activa en la máquina de la abogada. **HECHO VERIFICADO** (documentación de Microsoft, *Files On-Demand*): un archivo sincronizado puede existir como marcador sin contenido local, materializándose al abrirse. **HECHO VERIFICADO** (`boundaries.md` §6; fuente sqlite.org): SQLite en modo WAL **no funciona sobre filesystems de red**, exige que todos los procesos estén en la misma máquina, y hay corrupción documentada por locking defectuoso.

Un agente de sincronización sobre un directorio con un `case.db` **abierto en WAL** no es el caso de "filesystem de red" que sqlite.org describe, pero comparte su patrón de fallo: un tercero copiando, bloqueando y reemplazando archivos que el motor considera bajo su control exclusivo, y copiando `.db`, `.db-wal` y `.db-shm` en instantes distintos. **POR VERIFICAR** el modo de fallo exacto; **no se afirma corrupción como certeza y no se afirma ningún número**. Lo que sí es afirmable es que ninguna de las garantías de ADR-007 (atomicidad, un escritor, backup verificado) se sostiene bajo esas condiciones, y que la respuesta correcta a un riesgo así **no es medirlo, es excluirlo**.

Y hay una segunda dimensión, no técnica: sincronizar la zona 3 significa **subir originales de clientes a una nube personal de consumo**, fuera de cualquier decisión de custodia que este proyecto haya tomado. Eso toca secreto profesional y régimen de datos personales, y no es una decisión que corresponda tomar por omisión ni a nosotros ni al agente de sincronización.

**Tres defensas, en orden de fuerza:**

1. **Estructural (la que de verdad cierra el riesgo):** la zona 3 **no la elige ella**. La fija la instalación en una ruta local de máquina que las redirecciones de carpetas conocidas no alcanzan, y **es independiente de dónde esté el clon** (Decisión 2). Si clona dentro de OneDrive, sincroniza el *programa* —que es público para el efecto práctico, degrada el rendimiento y puede corromper el `.git`—, pero **no arrastra un solo byte de expediente**.
2. **Detección al arranque (best-effort, declarada como tal):** el paso 3 de la secuencia comprueba si la zona 3 resuelve bajo una raíz sincronizada conocida, mediante heurísticas —variables de entorno del tipo `%OneDrive%`, atributos de archivo de nube (`FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS`, `FILE_ATTRIBUTE_OFFLINE`), puntos de reanálisis— y, si acierta, **no arranca en escritura**. **SUPUESTO / POR VERIFICAR:** la disponibilidad y fiabilidad de cada una de esas señales en la máquina objetivo. Es una red, no una garantía: se comunica como red.
3. **Un camino soportado para respaldar.** Ella va a querer respaldar; si no le damos una forma, inventará una, y la que inventará es copiar la carpeta a la nube. Debe existir una acción de respaldo soportada, que produzca una copia **consistente y verificada** (misma definición de "verificado" que la migración) y que sea lo que se le enseñe desde el primer día. Su destino, frecuencia y cifrado son **DECISIÓN PENDIENTE** (pregunta 8).

### 9. Plan de contingencia si **B-04 resulta desfavorable**

Si se comprueba que el servidor MCP local **sí** está confinado a las carpetas adjuntadas, la zona 3 no puede ser simultáneamente inalcanzable para Cowork y legible por el Core dentro del mismo proceso. El diseño no se relaja: **cambia de mecanismo**.

**Contingencia (opción conocida, ya prevista en `boundaries.md` §6 y ADR-002):** el Core pasa a ser un **proceso independiente con permisos de sistema operativo propios**, y el servidor MCP que Cowork arranca queda reducido a un **stub de transporte** que no toca el filesystem de la zona 3 en absoluto: recibe la llamada de tool y la reenvía por canal local (named pipe / socket de loopback) al proceso Core, que es el único con acceso a la zona 3.

Nótese que la contingencia es **forzada y única**: proteger la zona 3 con ACLs manteniendo el Core dentro del proceso MCP no funcionaría, porque ese proceso corre bajo **la misma cuenta** que Cowork; denegarle acceso a ella se lo deniega también al Core. Solo separar la cuenta —o el proceso con su propia cuenta— produce la asimetría necesaria.

Lo que la contingencia cuesta, dicho sin adornos:

- **Un proceso más que instalar, arrancar y supervisar**, lo que tensiona el objetivo de coste de mantenimiento tendiendo a cero.
- **Una cuenta de servicio o una instalación con privilegios**, que probablemente exija un instalador — es decir, empuja hacia la alternativa (b) y **cambia el modelo de distribución de este ADR**, no solo su implementación.
- **Una superficie nueva: la autenticación del canal IPC.** Un canal local sin autenticar sería un camino alternativo de escritura al estado canónico, exactamente lo que ADR-002 prohíbe.
- **No cambia** la restricción de co-localización de ADR-007: sigue siendo una máquina.

Este ADR se declara **condicionado**: si B-04 resulta desfavorable, sus decisiones 1, 2, 4, 5, 6, 7 y 8 se conservan íntegras y **la decisión 3 y el mecanismo de arranque se revisan** en un ADR sucesor.

### 10. Alcance V0 y lo que queda `POST-V0`

**V0:** repositorio privado clonado, `pull --ff-only` disparado desde el acceso directo, arranque con verificación de integridad y migración por Case con backup verificado, tres raíces disjuntas, configuración local fuera del árbol, zona 2 en español.

**`POST-V0`, con trigger declarado (nada de esto entra sin él):** plugin de Cowork (trigger: **segunda oficina o segunda máquina**); instalador (trigger: la contingencia de B-04, o un runtime que no pueda empaquetarse); firma de código y canales de release (trigger: distribución fuera del círculo conocido); respaldo automatizado a destino externo (trigger: la decisión de la pregunta 8); evento canónico de migración (trigger: un ADR que abra la lista cerrada de eventos).

---

## Invariantes derivados

1. **El expediente nunca está bajo control de versión.** La zona 3 no es descendiente de ningún working tree de git; ningún archivo suyo está trackeado, ni ignorado, ni presente en el árbol — sencillamente no está ahí.
2. **`git pull` no toca las zonas 2 ni 3**, y no puede tocarlas: no son descendientes del working tree. La propiedad es posicional, no reglada.
3. **Ninguna operación de git puede borrar el expediente.** Corolario comprobable de 1 y 2: `git clean -fdx`, `git reset --hard` y `git checkout` ejecutados en la zona 1 no alteran un byte de las zonas 2 y 3.
4. **`.gitignore` nunca es la frontera.** Ningún documento, mensaje ni decisión puede invocarlo como protección de datos de cliente; es defensa en profundidad y se declara como tal.
5. **La ubicación de las zonas 2 y 3 no depende de dónde se clone el repositorio.**
6. **El arranque migra o no arranca.** Ningún `case.db` con `schema_version` distinto del esperado se abre en escritura, y ninguna migración se ejecuta sin backup **verificado** previo.
7. **Nunca hay migración hacia atrás.** `schema_version` mayor que la esperada ⇒ solo lectura, y se dice por qué.
8. **El modelo no ejecuta el arranque, la actualización ni la migración.** Ninguna de esas operaciones está en la superficie MCP; la clase `ADMIN` sigue vacía.
9. **La actualización es un acto humano explícito**, previo a la sesión, nunca automática, nunca en segundo plano, nunca con el Core corriendo, y solo fast-forward.
10. **La única carpeta adjuntada a Cowork es la zona 2**, y desde ella no se alcanzan las zonas 1 ni 3 — ni por descendencia ni por enlace simbólico o junction.
11. **La disjunción de las tres raíces se comprueba sobre rutas canónicas resueltas**, en cada arranque, y su fallo impide arrancar.
12. **La configuración local no vive en el working tree**: no puede entrar en conflicto en un `pull` ni viajar en un `push`.
13. **El repositorio no contiene material de cliente en ninguna rama ni en ningún punto del historial.**
14. **El Core nunca sobrescribe un archivo existente de la zona 2**; solo crea lo que falta.
15. **Toda proyección materializada en la zona 2 es regenerable, está marcada como tal, no es leída jamás por el Core como fuente y no es objetivo de escritura del modelo** (ADR-004).
16. **La verificación de integridad del producto sellado precede a la apertura de cualquier `case.db`**, y su fallo degrada a solo lectura de forma visible.
17. **La zona 3 reside en almacenamiento local no sincronizado**; ante detección en contrario, no se arranca en escritura.
18. **Ninguna operación del Core falla porque falte, se renombre o se mueva algo de la zona 2.**

---

## Consecuencias positivas

- **Los cuatro riesgos del encargo quedan cerrados por construcción, no por disciplina.** Conflictos de `pull` que tocan sus datos, `checkout`/`reset` que borran el expediente, `push` que sube documentos de clientes y conflictos de configuración local: los cuatro dejan de ser errores posibles-pero-improbables y pasan a ser **imposibles dentro del modelo**, porque el objeto que podría dañarse no está donde el comando opera.
- **El coste de mantenimiento es realmente bajo, y por la razón correcta.** No hay infraestructura de release que construir, ni instalador que firmar, ni actualizador que mantener: git ya es un mecanismo de distribución con historial, atomicidad razonable y capacidad de volver atrás. Se está reutilizando algo probado en vez de construir una versión peor de ello.
- **La actualización tiene un solo momento y una sola pregunta.** Ella no aprende git, no ve una terminal, no elige estrategias de merge y no interpreta mensajes en inglés. Ve una pregunta en español y un estado al final.
- **El daño de una actualización mala está acotado y es reversible.** Volver a la versión anterior del programa es un `checkout` de tag; los datos ya migrados quedan en solo lectura, visiblemente, en vez de ser degradados en silencio.
- **La misma respuesta —posición, no regla— sirve para dos superficies distintas.** Git y Cowork comparten la propiedad de no ofrecer restricciones fiables por ruta; un único principio arquitectónico cubre ambas, y seguirá cubriendo la tercera que aparezca.
- **El repositorio puede volverse público sin que sea una catástrofe de confidencialidad.** Por el invariante 13, la exposición sería de propiedad intelectual y de superficie de ataque, no de secreto profesional. Diseñar para que el peor caso sea vergonzoso en vez de irreparable es la propiedad que hay que buscar.
- **La zona 2 le da un espacio propio real.** `mis-notas.md` junto a una proyección regenerable convierte "no toques ese archivo" en una instrucción con alternativa, que es la única clase de instrucción que la gente cumple.
- **El camino a la segunda oficina queda abierto y nombrado.** El plugin no se descarta: se aplaza con un trigger explícito, y las decisiones de este ADR (tres raíces, config fuera del árbol, arranque que migra) son las mismas que ese camino necesitará.

---

## Consecuencias negativas

- **Se depende de que `git` esté disponible y funcional en su máquina**, incluidas sus condiciones de Windows: rutas largas, acentos y espacios, finales de línea, y un antivirus que puede interferir. Es una dependencia externa donde antes no había ninguna, y su fallo se manifiesta en el peor momento — durante una actualización.
- **La actualización requiere una credencial contra un repositorio privado**, y esa credencial está en su máquina. Es superficie nueva, y su gestión es una pregunta abierta (pregunta 1).
- **Tres raíces disjuntas son más difíciles de explicar y de mover** que una sola carpeta. Si algún día hay que trasladar la instalación a otro equipo, hay tres cosas que trasladar y un puntero que reescribir, no una carpeta que copiar.
- **El puntero de instalación es un punto único de fallo operativo.** Si se pierde o se corrompe, el sistema no arranca hasta que alguien lo reponga. Es fricción deliberada —preferible a que el arranque adivine rutas—, pero es fricción real.
- **La migración por Case puede dejar el conjunto en estados mixtos**, y explicarle a una profesional que tres expedientes están al día y uno está en solo lectura es peor experiencia que "todo funciona". Es la opción correcta y no es agradable.
- **`git pull --ff-only` puede bloquearse por causas triviales** —un archivo del programa abierto y guardado, un cambio de finales de línea— y producir un "no se pudo actualizar" que a ella no le dice nada. Se mitiga con la acción «restaurar programa», que es una capacidad más que construir y mantener.
- **La detección de nube es best-effort y puede fallar en ambos sentidos**: dejar pasar una configuración de sincronización que no reconoce, o negarse a arrancar en un caso legítimo. Un falso positivo que impide trabajar es un incidente.
- **Se acepta conscientemente un modelo de distribución que no escala.** Con dos oficinas, este mecanismo empieza a doler. Está elegido para una usuaria conocida y así se declara, en vez de construir hoy lo que hará falta después.

---

## Alternativas consideradas

### (a) Plugin de Cowork

**Lo que está verificado:** **HECHO VERIFICADO** (spike Cowork, B-07; fuente: `claude.com/docs/cowork/guide/plugins`) que un plugin puede aportar *"skills, MCP connectors, subagents, slash commands, or hooks in a single step"*. **HECHO VERIFICADO** (B-08) que los componentes se habilitan y deshabilitan individualmente —con granularidad de **componente**, no de tool: desactivar "el conector" es todo o nada para la superficie completa—. **HECHO VERIFICADO** (B-05) que la vía alternativa, servidor MCP local desde *Settings → Developer*, también existe.

**Lo que NO está verificado, y es decisivo:** **POR VERIFICAR — si un plugin puede empaquetar el runtime.** La documentación describe *componentes* (skills, conectores, agentes, hooks), no el transporte de un intérprete o de binarios nativos. Si el runtime debe instalarse aparte de todos modos, el plugin resuelve la mitad del problema y deja la otra mitad exactamente donde estaba. También **POR VERIFICAR**: qué hace la actualización de un plugin —si es que la hay— con el estado de la zona 3, que es la pregunta que de verdad importa.

**Por qué no es el camino de V0:** tres razones, ninguna estética. Primera, **la actualización de un plugin no ejecuta migraciones**: sea cual sea su mecanismo, el momento de "los datos deben migrar" seguiría necesitando el arranque de la Decisión 4, de modo que el plugin no ahorra la pieza cara. Segunda, **empaquetar hooks en el mismo artefacto es un arma cargada**: **HECHO VERIFICADO** (C-04) que en Claude Code el hook `Elicitation` puede *"auto-respond to elicitation requests without showing a dialog"*, con advertencia oficial de que *"bypasses the user confirmation dialog"*, y **HECHO VERIFICADO** (D-03) que Cowork admite hooks de plugin y que un hook puede ser fuente de una decisión de permiso; distribuir el producto por una vía que normaliza el envío de hooks invita, más adelante, a "resolver" una fricción de autorización con un hook que la elimina. Tercera, **con una usuaria conocida el plugin no compra nada que el clon no dé**, y sí añade dependencia de un mecanismo de terceros cuyo comportamiento ante actualización no está documentado.

**Por qué SÍ es el camino cuando haya una segunda oficina:** porque entonces el problema cambia de naturaleza. Con N máquinas, `git pull` deja de ser barato: hay que enseñar git a gente que no lo quiere aprender, hay que gestionar N credenciales, y hay N clones que pueden divergir. El plugin instala en un paso, sin literacy de git, con habilitación por componente y con actualización gobernada por la plataforma. El trabajo hecho aquí no se tira: las tres raíces, la configuración fuera del árbol y el arranque que migra son exactamente lo que ese camino necesitará, y el plugin sustituye **solo** el transporte de la zona 1. Condición de entrada, además de la segunda oficina: resolver el **POR VERIFICAR** del runtime y decidir explícitamente que el plugin **no transporta hooks que respondan confirmaciones**.

### (b) Instalador clásico (MSI / Inno / NSIS)

**A favor, y es más de lo que parece:** un instalador es la única de las tres alternativas que hace de forma natural lo que este ADR tiene que hacer a mano — **colocar las tres raíces en su sitio, escribir el puntero de instalación, registrar el servidor MCP, crear el acceso directo, y desinstalar dejando el sistema limpio**—. Y es el compañero obligado de la contingencia de B-04, porque una cuenta de servicio o una ACL sobre la zona 3 exigen privilegios en el momento de instalar.

**En contra:** hay que **construir el mecanismo de actualización desde cero** —que es precisamente lo que `git pull` regala—, con el trabajo de empaquetar cada versión, decidir diferencial o completa, y verificar la aplicación. Requiere infraestructura de build. Y sin **firma de código** —explícitamente fuera de V0, `boundaries.md` §10— un instalador descargado dispara advertencias de SmartScreen (**HECHO VERIFICADO**, documentación de Microsoft sobre Microsoft Defender SmartScreen), lo que obliga a enseñarle a una abogada a saltarse una advertencia de seguridad de su propio sistema operativo: exactamente el hábito que no queremos crear.

**Veredicto:** rechazada para V0 por coste desproporcionado frente a una usuaria conocida; **retenida como la alternativa que se activa si B-04 sale desfavorable**, y probablemente combinada con (a) cuando llegue la segunda oficina — instalador para el runtime y la zona 3, plugin para el conector y las skills.

### (c) Servicio en la nube

**Rechazada, y no por coste: porque sería otro producto.** Conviene decir exactamente qué cambiaría, para que la conversación no se reabra como si fuera una opción de despliegue:

- **Contradice ADR-002 (Accepted).** El invariante 1 exige que el estado canónico no resida donde el host tenga escritura directa, y `principles.md` exige **custodia local**. Un servicio en la nube no relaja ese invariante: lo sustituye por otro distinto —custodia delegada en un operador— con un modelo de amenaza que este proyecto no ha analizado.
- **Rompe ADR-007 (`Proposed`) inv. 7** de forma literal: *un `case.db` fuera de almacenamiento local no es despliegue válido*. La persistencia entera —SQLite/WAL, un escritor, co-localización, backup verificado por directorio de Case— es una decisión tomada **para** una máquina.
- **Añade un principal nuevo a ADR-001.** Hoy hay dos: la profesional y el modelo como cliente externo no confiable. Un servicio añade al **operador de la infraestructura**, con acceso potencial al estado canónico. La frontera de confianza no se ajusta: se rediseña.
- **Cambia el régimen jurídico de la custodia.** Documentos de clientes salen del despacho hacia un tercero, con las obligaciones de secreto profesional y de protección de datos que eso conlleva. **Este ADR no afirma qué exige la normativa colombiana**: afirma que la pregunta se abre, que hoy no está contestada y que contestarla no es una tarea técnica.
- **Convierte el coste de mantenimiento de ~0 en recurrente y creciente**, y añade compromisos que hoy no existen: disponibilidad, recuperación ante desastre, respaldo del operador, soporte.

Si algún día se quiere, **es un producto nuevo con sus propios ADR-001/002/007**, no una opción de distribución del actual.

### (d) Descarga de un `.zip` sin git

Rechazada en una línea: no tiene camino de actualización, no tiene historial, no permite volver atrás, y para hacerla segura habría que reconstruir a mano lo que git ya da. Es la peor combinación de (b) sin sus ventajas.

### (e) Datos dentro del working tree, protegidos por `.gitignore`

Rechazada, y es la alternativa que más importa rechazar por escrito porque es la que se propondría sola: **HECHO VERIFICADO** (`git-clean`) que `git clean -fdx` elimina también los archivos ignorados. Un `.gitignore` no es una frontera; es una preferencia de visualización que además produce la falsa sensación de estar protegido. Se conserva como defensa en profundidad y con esa etiqueta.

---

## Riesgos

1. **`RIESGO` alto — `git push` accidental con datos de clientes.** *Cerrado estructuralmente* por los invariantes 1 y 13: no hay datos de cliente dentro del working tree que puedan quedar staged. **Residual:** que alguien copie manualmente un documento de cliente dentro de la zona 1 (para "adjuntarlo a un reporte de error", el motivo clásico). Mitigaciones, en orden de fuerza: **(i)** que ella **no tenga credencial de escritura** sobre el remoto —credencial de solo lectura, ver pregunta 1—, que reduce el riesgo casi a cero por la vía correcta; **(ii)** comprobación del lado del servidor en el remoto, la única que no se puede saltar desde su máquina; **(iii)** hook local vía `core.hooksPath`, **declarado explícitamente como defensa en profundidad** porque **HECHO VERIFICADO** que los hooks no se clonan y por tanto un hook versionado no está activo por sí solo; **(iv)** el manifest de integridad, que en el arranque detecta archivos inesperados en la zona 1.
2. **`RIESGO` alto — la usuaria clona, mueve o "respalda" el árbol en una carpeta sincronizada con la nube, arrastrando el expediente.** Tratamiento completo en la Decisión 8. *Cerrado estructuralmente* por el invariante 5 (la zona 3 no depende de dónde esté el clon) más el invariante 17 (no arrancar en escritura si se detecta sincronización). **Residual y real:** que copie deliberadamente la zona 3 a la nube creyendo que se respalda. La mitigación no es técnica sino de producto — darle un camino de respaldo soportado y enseñárselo antes de que invente el suyo (pregunta 8). **POR VERIFICAR:** el modo de fallo exacto de un `case.db` en WAL bajo un agente de sincronización; no se afirma corrupción como certeza.
3. **`RIESGO` alto — B-04 desfavorable.** Consecuencia: el modelo de custodia de la zona 3 se rediseña y este ADR pasa a condicionado (Decisión 9). Estado: `INCONCLUSIVE`, protocolo empírico pendiente en `experiments/cowork-capability-spike/`. **No se mitiga suponiendo que saldrá bien**: se mitiga teniendo el plan escrito antes de necesitarlo.
4. **`RIESGO` medio — repositorio público por error.** Consecuencia acotada por el invariante 13: exposición de código y de superficie de ataque, **no de secreto profesional**. Mitigación de diseño: **tratar la publicidad del repositorio como un supuesto de trabajo** — ningún secreto, ninguna credencial, ninguna Client Config con datos reales, ningún nombre de cliente en un test fixture, ningún path de máquina real. Si el peor caso de un repositorio público es "se ve nuestro código", el riesgo está gestionado; si es cualquier otra cosa, hay un invariante roto.
5. **`RIESGO` medio — conflictos de merge en configuración local.** *Cerrado estructuralmente* por el invariante 12. **Residual:** el registro del servidor MCP en Cowork puede exigir un archivo que contenga **rutas absolutas de la máquina**; si ese archivo tuviera que vivir en el repositorio, el riesgo volvería por la puerta de atrás. Mitigación: el repositorio transporta una **plantilla**, y el arranque genera el archivo concreto fuera del árbol. **POR VERIFICAR** (B-05): dónde registra Cowork el servidor MCP local y si admite rutas relativas o variables de entorno.
6. **`RIESGO` medio — actualización a mitad de camino con el Core corriendo o con archivos en uso.** Producto parcialmente actualizado, manifest que no cuadra, comportamiento indefinido. Mitigación: lock de instancia única y actualización solo antes de abrir sesión (Decisión 3); el manifest lo detecta y degrada a solo lectura si algo quedó a medias.
7. **`RIESGO` medio — salto de varias versiones de esquema de una vez.** Si no actualiza durante meses, el arranque encadena N migraciones. Mitigación: migraciones numeradas solo-adelante y **encadenables**, con la cadena probada explícitamente (D-12), no solo el paso individual.
8. **`RIESGO` medio — migración parcial del conjunto de Cases.** Ya registrado como R3 en ADR-007. Mitigación heredada: fricción deliberada — todo Case con `schema_version` inesperado en solo lectura, reportado, sin arreglos al vuelo.
9. **`RIESGO` medio — falso positivo de la detección de nube** que impide trabajar un día en que hay término procesal. Mitigación: el mensaje debe decir exactamente qué detectó y ofrecer un camino de contacto; y la detección **no debe** poder desactivarse desde la superficie del modelo.
10. **`RIESGO` medio — E-07 (`INCONCLUSIVE`): el servidor MCP no arranca y Cowork no lo dice con claridad.** Escenario peligroso porque **el modelo podría intentar trabajar el expediente sin el Core**, respondiendo desde su propio contexto. No es un riesgo de este ADR pero lo agrava, porque un `pull` mal aplicado es una causa nueva y plausible de que el MCP no arranque. Mitigación: la tarjeta de estado del arranque (paso 9) y la prueba D-10.
11. **`RIESGO` bajo — la abogada modifica archivos del programa** y bloquea el `pull`. Mitigación: acción «restaurar programa», que nunca toca las zonas 2 y 3.
12. **`RIESGO` bajo — condiciones de Windows:** rutas largas, acentos y espacios en la ruta del clon, finales de línea que corrompen un script de arranque, antivirus que pone en cuarentena un binario. Mitigaciones conocidas (`core.longpaths`, `.gitattributes`) **POR VERIFICAR** en la máquina objetivo; se prueban en D-14, no se suponen.
13. **`RIESGO` bajo — junction o enlace simbólico dentro de la zona 2 que apunte a la zona 1 o a la zona 3**, creado sin intención por una herramienta de respaldo o por un atajo. Rompería la disjunción sin que nada lo delate. Mitigación: comprobación en el arranque sobre rutas canónicas (invariante 11). **`NOT_TESTED` (A-08):** ninguna documentación de Cowork trata junctions ni symlinks de Windows, y **no se extrapola** desde la regla que sí existe para contenido de plugins.
14. **`RIESGO` declarado y no mitigable — usuaria local con control total del equipo.** Nada de esto es inmutable frente a alguien que decida deliberadamente romperlo desde su propia máquina (`boundaries.md` §10). El objetivo es proteger de accidentes, y así se enuncia; el documento no promete lo contrario.

---

## Validación / pruebas necesarias

Identificadores provisionales, a consolidar en `docs/technical-design/v0/12-testing-strategy.md`. Las pruebas D-01 a D-03 valen además como **re-verificación empírica** de los hechos de git citados en el Contexto: se afirman desde la documentación oficial y se comprueban en la máquina Windows objetivo antes de depender de ellas.

1. **D-01** — `git clean -fdx` en la zona 1 ⇒ checksum del árbol completo de las zonas 2 y 3 idéntico antes y después (invariantes 2, 3).
2. **D-02** — `git reset --hard <commit anterior>` y `git checkout <tag anterior>` en la zona 1 ⇒ mismo resultado que D-01.
3. **D-03** — `git status` no lista ningún archivo de cliente; `git ls-files` no lo contiene; búsqueda sobre **todo el historial y todas las ramas** ⇒ vacío (invariante 13).
4. **D-04** — `pull` que introduce `schema_version` N+1 ⇒ backup escrito **y verificado** (restaurado, integridad comprobada, cadena de eventos verificada sobre la copia, conteos comparados) ⇒ migración ⇒ verificación. Con backup deliberadamente corrupto ⇒ **no migra** y arranca en solo lectura (invariante 6).
5. **D-05** — programa revertido a versión anterior con datos ya en N+1 ⇒ solo lectura, sin migración hacia atrás, con mensaje que explica por qué (invariante 7).
6. **D-06** — remoto divergente ⇒ `pull --ff-only` se detiene, no abre merge, y el sistema **arranca igualmente** con la versión anterior (Decisión 3).
7. **D-07** — working tree sucio ⇒ actualización rechazada; «restaurar programa» ⇒ zona 1 limpia y checksum de zonas 2 y 3 inalterado.
8. **D-08** — zona 3 colocada bajo una raíz sincronizada conocida ⇒ no arranca en escritura (invariante 17). Variante negativa: ruta local normal ⇒ arranca sin falso positivo.
9. **D-09** — junction o symlink dentro de la zona 2 apuntando a la zona 3 ⇒ el arranque lo detecta y no arranca. **Prueba complementaria y `NOT_TESTED` hoy (A-08):** comprobar empíricamente si Cowork sigue ese enlace, porque de ello depende que la comprobación sea una defensa o una formalidad.
10. **D-10** — servidor MCP no disponible ⇒ ella lo ve, y el sistema no permite trabajar como si estuviera. Cubre E-07 (`INCONCLUSIVE`).
11. **D-11** — recorrido de la superficie MCP: ninguna tool ejecuta git, arranca el Core, migra, restaura ni escribe el puntero de instalación. La clase `ADMIN` sigue con **cuenta cero** (invariante 8, ADR-010).
12. **D-12** — cadena de migraciones N → N+3 aplicada de una sola vez, con backup verificado por cada paso o por la cadena completa, y verificación final.
13. **D-13** — alterar un archivo del producto sellado ⇒ el arranque lo detecta y degrada a solo lectura antes de abrir ningún `case.db` (invariante 16).
14. **D-14** — clon en ruta con espacios, acentos y longitud próxima al límite de Windows ⇒ arranque, actualización y migración funcionan. Incluye finales de línea de los scripts de arranque.
15. **D-15** — el arranque crea lo que falta de la zona 2 y **no sobrescribe** un archivo existente; borrar o renombrar una carpeta suya no hace fallar ninguna operación del Core (invariantes 14, 18).
16. **D-16** — `memoria-del-caso.md` editado a mano por ella ⇒ se regenera; el contenido canónico es idéntico antes y después; `mis-notas.md` **no** se toca (invariante 15).
17. **D-17** — prueba de humo con la profesional: doble clic, ve el estado en español, acepta una actualización, trabaja, cierra. Sin terminal, sin comandos, sin mensajes en inglés.
18. **D-18** — auditoría de las tres raíces sobre rutas canónicas resueltas: ninguna es ancestro de otra; si se fuerza el solapamiento, no arranca (invariantes 10, 11).

---

## Preguntas pendientes

1. **Repositorio privado y acceso de ella — cómo obtiene el `pull`.** Tres opciones: clon inicial hecho por los dueños con credencial de **solo lectura** instalada una vez y almacenada por el gestor de credenciales de Windows; token propio de ella; o cuenta de GitHub suya con acceso al repositorio. **Recomendación: la primera** — ella nunca escribe una credencial, nunca tiene permiso de escritura sobre el remoto, y el riesgo 1 se cierra por la vía correcta. **Opción conocida y POR VERIFICAR en la cuenta concreta:** claves de despliegue de solo lectura. Decisión de los dueños.
2. **B-04 — ¿puede un servidor MCP local alcanzar rutas fuera de las carpetas adjuntadas?** `INCONCLUSIVE` y **bloqueante**. Determina si aplica la Decisión 9.
3. **¿El runtime se empaqueta o se instala aparte?** Depende de una decisión anterior aún abierta —**lenguaje/runtime de implementación del Core**, `boundaries.md`, *Preguntas abiertas*—. Si exige instalación separada, el "coste de mantenimiento tendiendo a cero" no se cumple tal cual y la alternativa (b) gana peso. Ligada a: **POR VERIFICAR si un plugin de Cowork puede empaquetar un runtime**.
4. **¿Dónde registra Cowork el servidor MCP local, y admite rutas relativas o variables de entorno?** De la respuesta depende si hay un archivo con rutas absolutas y, con él, el riesgo 5 residual. **POR VERIFICAR** (B-05: la ruta de UI *Settings → Developer* está verificada sobre documentación de página de terceros y debe confirmarse en el Claude Desktop concreto de los dueños).
5. **¿Necesita `git` instalado en su máquina?** Y si no lo tiene: ¿se empaqueta un git portable, se usa una biblioteca, o lo instalan los dueños en el momento de la instalación inicial? Afecta directamente a la consecuencia negativa 1.
6. **¿La migración necesita un evento canónico?** Este ADR **no** abre la lista cerrada de eventos de V0 y registra la migración en el plano operacional. Si una reescritura de almacenamiento canónico debe dejar rastro canónico, es un cambio de contrato con su propio ADR.
7. **Estructura y nombres exactos de la zona 2** — a validar **con la profesional**, no entre nosotros. El árbol de la Decisión 6 es propuesta. Incluye: si la partición por oficina es de primer nivel, cómo nombra ella los casos, y si `mis-notas.md` le resulta natural o sobra.
8. **Política de respaldo de la zona 3** — destino, frecuencia, cifrado, quién verifica, y qué se le enseña a ella. Ni `boundaries.md` §10 ni ADR-007 la fijan, y **es su riesgo real de pérdida total**: git no respalda nada de lo que importa. Bloquea la defensa (iii) del riesgo 2.
9. **¿Quién dispara la actualización en la práctica: ella, o los dueños por sesión remota?** La segunda da más control y rompe el coste ~0. Decisión de los dueños.
10. **¿Se protege el `.git` y la zona 1 frente a escritura accidental de ella** (ACL, atributos)? Añadiría defensa a bajo coste, y podría interferir con el propio `pull`. **POR VERIFICAR**.
11. **Trigger operativo de la segunda oficina.** Este ADR nombra el disparador del plugin; falta acordar quién declara que se cruzó y qué se hace ese día con el clon existente.

---

## Relaciones con otros ADRs

- **ADR-001 (Accepted) — frontera de confianza.** Este ADR **la extiende al plano de despliegue**: si el modelo no ejecuta comandos ni escribe estado, tampoco ejecuta `git`, ni el lanzador, ni las migraciones (Decisión 7, invariante 8). Recíprocamente, ADR-001 solo se sostiene si el producto que impone la frontera no puede ser reescrito por quien la sufre — que es lo que la separación de la zona 1 garantiza.
- **ADR-002 (Accepted) — case store protegido.** Este ADR **le da domicilio físico** a la frontera USER WORKSPACE / LEGAL OS PRIVATE STATE, sin alterarla: la zona 2 es el USER WORKSPACE con nombres en español (Decisión 6), la zona 3 es el LEGAL OS PRIVATE STATE, y el camino único host → MCP → Application → Case Store no cambia. Respeta la alternativa 2 rechazada allí: **las rutas concretas siguen siendo detalle de despliegue, no decisión de arquitectura**. Añade la zona 1 como tercera posición, que ADR-002 no necesitaba nombrar porque no trataba distribución.
- **ADR-004 (Accepted) — memoria del caso y proyecciones.** Fundamenta la Decisión 6.3: `memoria-del-caso.md` en la carpeta del caso es **proyección derivada y regenerable**, jamás fuente y jamás objetivo de escritura del modelo. Este ADR aporta la consecuencia operativa que ADR-004 no tenía por qué dar: **por eso puede reescribirse tras cada actualización sin que se pierda nada**, y por eso hace falta `mis-notas.md`.
- **ADR-005 (Accepted) — autoridad humana.** La actualización y la migración son actos humanos, pero **no son `HumanAuthorization`**: no consolidan estado jurídico, no consumen autorización y no viven en el plano del modelo. Se ejercen desde el plano administrativo, fuera de la superficie MCP. Este ADR no toca el mecanismo de ADR-005 y depende de él en un punto: el registro server-side de las autorizaciones vive en la zona 3, y por tanto hereda todas las garantías de posición que aquí se establecen.
- **ADR-007 (`Proposed`) — estrategia de persistencia.** Es el ADR con el que este se acopla más fuerte. Consume su layout (`cases/<case_id>/case.db` + `blobs/`), su invariante 7 (almacenamiento local o no es despliegue válido — base de la Decisión 8), su invariante 9 (`schema_version` inesperada ⇒ solo lectura), su invariante 10 (fallo de integridad ⇒ solo lectura visible), su unidad de backup/migración por directorio de Case y su definición de "backup verificado" (V10). **No modifica ninguno**: los sitúa en el tiempo (el arranque) y en el espacio (la zona 3).
- **ADR-010 (`Proposed`) — superficie MCP.** Este ADR **no añade ni una tool**. Confirma la clase `ADMIN` vacía con cuenta cero y aporta una aserción comprobable más (D-11): ninguna operación de distribución, actualización o migración es alcanzable desde la superficie del modelo.
- **ADR-011 (`Proposed`) — locators de evidencia.** Relación indirecta pero real: su invariante 11 exige que ningún locator contenga rutas de filesystem, y su retención exige que ninguna versión referenciada se descarte. Ambas propiedades sobreviven a este ADR porque **ninguna operación de git alcanza la zona 3**; una migración que reubicara blobs sería una migración de copia hacia adelante, nunca un `UPDATE` masivo de rutas — que es justamente por lo que allí no se almacenan rutas.
- **`boundaries.md` §10 — mínimo de release v0.** Este ADR **implementa los siete puntos** (product version, schema version, manifest, verificación de integridad al arranque, migraciones numeradas solo-adelante, backup verificado previo, degradación a solo lectura) y **respeta las cuatro exclusiones** (sin auto-update, sin firma de código, sin telemetría, sin canales de release). Refinamiento a señalar, no contradicción: preguntar por una actualización y esperar un acto humano no es auto-update; y el *tag* de git es el portador natural de la *product version* que §10 ya exigía.
- **`docs/research/cowork-runtime-spike-v0.md`** — fuente de todos los `HECHO VERIFICADO` de plataforma citados aquí (A-02, A-08, B-01, B-02, B-04, B-05, B-07, B-08, B-09, C-04, D-03, D-05, E-07) y del `INCONCLUSIVE` B-04 del que este ADR depende y cuya contingencia trae.
