# Spike Cowork Runtime — verificación documental v0

**Fase:** TECHNICAL DESIGN V0
**Tipo de documento:** research / spike (nivel 6 de la precedencia documental del kernel §14).
**Naturaleza normativa:** ninguna. Este documento **no** fija reglas. Registra observaciones documentales y declara qué está sin verificar. Un resultado de spike **jamás** es una garantía de plataforma (kernel §14).
**Fecha de la verificación:** 2026-08-24.
**Verificador:** sesión de Claude Code (no Cowork). Ver §2 — *toda* la evidencia de este documento es **documental**, ninguna es empírica.

---

## 1. Objeto y alcance

Determinar qué garantiza **hoy y por escrito** la documentación oficial de Anthropic sobre Claude Cowork Desktop en cinco áreas que condicionan la arquitectura del Legal Workspace:

- **A. FILESYSTEM** — qué carpetas ve, cómo se conceden, si puede modificar, travesía de rutas, symlinks/junctions en Windows, qué herramientas genéricas recibe el agente.
- **B. MCP LOCAL** — soporte de servidores MCP locales/stdio, modos de aprobación de conectores, y la pregunta decisiva: *¿puede el host no tener acceso directo a una carpeta mientras un MCP local sí lo tenga?*
- **C. ELICITATION / CONFIRMACIONES** — soporte de elicitation, form mode, URL mode, qué ve la humana, qué puede inspeccionar el LLM.
- **D. PERMISOS** — deny por ruta, tool approval, tool restriction, hooks, permisos por subagente. **Sin asumir equivalencia con Claude Code.**
- **E. SESIÓN** — cierre/reapertura, relación sesión ↔ MCP local, comportamiento si el MCP está caído, qué mensajes ve la usuaria.

**Fuera de alcance:** rendimiento, límites de uso, precios, comportamiento de modelos, Cowork en web/móvil salvo donde condicione el acceso local.

---

## 2. Metodología y cómo leer la columna `Observed`

Esta sesión corre en **Claude Code**, no en Cowork. **No se ha ejecutado Cowork ni una sola vez durante esta verificación.** En consecuencia:

- **No existe en este documento ningún dato "observed in current environment".** Cero.
- La columna `Observed` registra **lo que la documentación oficial dice literalmente** (observación *documental*), no lo que un sistema hizo.
- Cada celda de `Observed` lleva un prefijo:
  - **`DOC:`** — la doc oficial lo afirma explícitamente. Es una *documented platform guarantee* solo si la fuente es normativa; una nota de changelog es evidencia de comportamiento, no promesa de estabilidad.
  - **`CHANGELOG:`** — proviene del changelog oficial de Claude Desktop. Es **HECHO VERIFICADO** sobre lo que se cambió, pero **no** es una garantía de plataforma: un changelog describe una versión, no un contrato.
  - **`SIN DATO:`** — la doc oficial no lo dice. No se infiere.
- La columna `Status` usa el enum exigido: `VERIFIED | NOT_SUPPORTED | INCONCLUSIVE | NOT_TESTED`.
  - `VERIFIED` = **la doc oficial lo afirma explícitamente**. No significa "comprobado empíricamente".
  - `NOT_SUPPORTED` = la doc oficial afirma explícitamente que no existe o no funciona.
  - `INCONCLUSIVE` = la doc no lo dice, o lo dice de forma ambigua o para un producto vecino.
  - `NOT_TESTED` = solo determinable ejecutando Cowork. **Toda la fila empírica es NOT_TESTED por construcción.**

**Regla de honestidad aplicada:** donde la doc oficial no lo dice, la fila es `INCONCLUSIVE` o `NOT_TESTED`. En ningún caso se ha inferido una capacidad a partir de otra.

### 2.1 Advertencia de alcance sobre las fuentes (leer antes de la tabla)

Tres de las fuentes más ricas exigen un matiz que condiciona la lectura de casi todas las filas de A y D:

1. **`claude.com/docs/third-party/claude-desktop/local-access`** (también servida en `claude.com/docs/cowork/3p/local-access`) es la página de **Claude Desktop on third-party (3P)** — despliegues sobre Bedrock/Vertex/Foundry/gateway. Se cita porque **se declara a sí misma equivalente**: *"Like Cowork in standard Claude Desktop, Claude Desktop on third-party (3P) works directly with files on the user's computer."* Aun así, **los controles administrativos que describe (`allowedWorkspaceFolders`, `mode: ro`) son de configuración gestionada**, no de la UI de una usuaria individual.
2. **`allowedWorkspaceFolders`** sí aparece listada como clave de configuración gestionada del **Claude Desktop estándar** (artículo *Enterprise configuration*, descrita como *"Filepath or filepaths the user can mount to Cowork"*), pero ese artículo restringe estos controles a **administradores en planes Team o Enterprise**. **SUPUESTO relevante para los dueños:** una profesional individual en plan Pro/Max, sin MDM, **no dispone de estos controles**. → `POR VERIFICAR` con el plan real de los dueños.
3. **`code.claude.com/docs/en/hooks`** documenta hooks *de Claude Code*. La página enumera como superficies *"the terminal, IDE extensions, the Desktop app, and Claude Code on the web"* — **no nombra Cowork**. Por tanto **no se asume equivalencia**: la existencia de hooks en Cowork se sostiene en otras dos fuentes (§D-03), y el **catálogo de eventos aplicable a Cowork queda INCONCLUSIVE**.

---

## 3. Tabla de capacidades

> Columnas exigidas. `Observed` = observación documental (§2), nunca empírica.

### A. FILESYSTEM

| Capability | Expected | Observed | Official source | Status | Security implication | ADR affected |
|---|---|---|---|---|---|---|
| **A-01** Modelo de concesión: la usuaria adjunta "workspace folders" | La usuaria elige carpetas y el agente queda confinado a ellas | `DOC:` *"Users attach one or more workspace folders to a session; the agent can then read, create, and modify files anywhere inside those folders, and run code against them inside the sandbox VM."* | claude.com/docs/third-party/claude-desktop/local-access | VERIFIED | El confinamiento es **por carpeta adjunta**, no por fichero ni por operación. La unidad de confianza es la carpeta entera | ADR-001, ADR-002 |
| **A-02** Confinamiento a carpetas conectadas | Cowork no lee fuera de lo concedido | `DOC:` *"Claude can only read and write files in folders you've connected"* y *"Local file access is limited to folders the member has connected on the desktop, and each local tool call is checked against the member's permissions before it runs."* | support.claude.com 13345190; support.claude.com 14479288 (architecture overview) | VERIFIED | Es la base sobre la que se puede afirmar que el `case.db` fuera de toda carpeta adjunta queda fuera del alcance de las file tools. **Afirmación documental, no comprobada aquí** | ADR-001, ADR-002 |
| **A-03** Escritura y modificación dentro de la carpeta adjunta | Lectura y escritura | `DOC:` *"Claude can read from and write to your local files without manual uploads or downloads."* + `DOC:` *"the agent can read and write every file the user's OS account can reach"* (dentro de una raíz permitida rw) | support.claude.com 13345190; local-access | VERIFIED | **No existe granularidad sub-carpeta.** Adjuntar una carpeta concede todo su árbol. Corolario: nunca adjuntar una carpeta que contenga el case store | ADR-002, ADR-006 |
| **A-04** ¿Existe deny por sub-ruta dentro de una carpeta adjunta? | Poder excluir `./private` dentro de una carpeta adjunta | `DOC:` *"To keep data out of reach entirely, leave it outside the allowed roots."* — la doc **prescribe exclusión por ubicación**, no ofrece regla de exclusión | local-access (nota) | NOT_SUPPORTED | La única exclusión documentada es **no adjuntar**. Un diseño que dependa de "carpeta adjunta con subcarpeta protegida" **no tiene soporte documentado** | ADR-002 |
| **A-05** Carpeta en solo lectura (`mode: ro`) | Leer sin poder modificar | `DOC:` *"The agent can view and search a read-only folder but cannot modify it in Cowork. In Code sessions, read-only applies to Claude's file tools only; shell commands and SSH sessions do not enforce it."* | local-access; `CHANGELOG:` v1.26832.0 (2026-08-06, sección 3P) | VERIFIED (para Cowork) | **Dos superficies de enforcement distintas**: file tools y shell no se comportan igual. En Cowork la doc afirma bloqueo de escritura; en Code explícitamente no cubre Bash. Requiere confirmación empírica en Cowork+Windows | ADR-002, ADR-006 |
| **A-06** Travesía de rutas (`..`) y symlinks al **adjuntar** | El allowlist no se puede evadir | `DOC:` *"The check is enforced against the resolved path, so symlinks and `..` traversal can't be used to escape an allowed root."* | local-access | VERIFIED (solo para el chequeo de `allowedWorkspaceFolders`) | La frase gobierna **qué puede adjuntar la usuaria** bajo allowlist administrativo. **No** afirma nada sobre las llamadas del agente en tiempo de ejecución | ADR-001 |
| **A-07** Travesía de rutas / symlinks en **tiempo de ejecución** del agente | Un symlink dentro de una carpeta adjunta que apunte fuera no debería ser seguible | `SIN DATO:` la doc no describe el comportamiento de las file tools ante un symlink que sale de la carpeta adjunta | — | INCONCLUSIVE | **Riesgo abierto de primer orden.** Si un symlink saliente se sigue, el confinamiento de A-02 se rompe sin que la usuaria lo perciba. Debe probarse | ADR-001, ADR-002 |
| **A-08** Junctions y symlinks de Windows (`mklink /J`, `/D`) | Tratamiento equivalente a symlinks POSIX | `SIN DATO:` ninguna doc oficial de Cowork menciona junctions ni symlinks de Windows. La única mención a symlinks en el corpus oficial es sobre **contenido de plugins**: *"Symlinks that point outside the plugin ... are skipped"* | 3p/extensions (nota, contexto de plugins, **no** de workspace folders) | NOT_TESTED | Windows distingue junction, symlink de directorio y hardlink, y las resuelve distinto. Extrapolar la regla de plugins a workspace folders sería una inferencia no autorizada | ADR-001, ADR-002 |
| **A-09** Rutas UNC crudas (`\\server\share`, `\\wsl$\...`) | Adjuntables | `DOC:` *"Raw UNC paths (`\\server\share`) are not supported; map the share to a drive letter first."* y lo mismo para `\\wsl$\<distro>` | local-access | VERIFIED | Reduce superficie: el material del expediente en un recurso de red solo entra por unidad mapeada, acto explícito de la usuaria | ADR-006 |
| **A-10** Unidad de red mapeada: file tools vs shell divergen | Comportamiento uniforme | `DOC:` *"Mapped and reachable at sandbox start: ... File tools and shell commands both work. Mapped later, or unreachable at sandbox start: file tools still work, but shell commands cannot reach the drive."* | local-access | VERIFIED | Confirma que **file tools y shell tienen alcances de filesystem distintos**. Cualquier razonamiento de seguridad debe tratarlos como dos superficies, no una | ADR-001, ADR-002 |
| **A-11** El agente no puede auto-adjuntar carpetas | Solo la usuaria concede | `DOC:` *"The agent cannot attach a network-drive path on its own; only the user can, through the folder picker. This is a security boundary."* | local-access | VERIFIED (enunciado explícitamente como frontera de seguridad, y **solo** para rutas de unidad de red) | Es la única frase de toda la doc que se autodenomina *security boundary*. **No** se ha encontrado la afirmación equivalente para carpetas locales → no extender por analogía | ADR-001 |
| **A-12** Protección ante borrado | Borrado permanente exige permiso explícito | `DOC:` *"Cowork requires your explicit permission before permanently deleting any files. You'll see a permission prompt and must select 'Allow' before Claude can perform deletion tasks."* | support.claude.com 13364135 | VERIFIED | Apoya PF-002 (kernel §12) **parcialmente**: cubre borrado, **no** sobrescritura. Un fichero de evidencia puede sobrescribirse sin ese prompt | ADR-002, ADR-006 |
| **A-13** Enumeración de las herramientas genéricas del agente | Lista nombrada (Read/Write/Edit/Bash/Glob/Grep…) | `SIN DATO:` ninguna doc oficial de Cowork enumera herramientas por nombre. La telemetría define el atributo `tool_name` pero **no publica sus valores**. Lo que sí está nombrado por capacidad: lectura/escritura de ficheros, shell y ejecución de código en la VM, web fetch, web search, navegador (Claude in Chrome), computer use, sub-agentes, generación de documentos ofimáticos | claude.com/docs/cowork/monitoring; cowork/overview; 13345190 | INCONCLUSIVE | **No se puede escribir un threat model basado en una lista cerrada de tools**, porque Anthropic no la publica y puede cambiarla sin aviso. El diseño no debe depender de que cierta tool no exista | ADR-001 |
| **A-14** Carpetas adjuntas visibles en telemetría | — | `DOC:` atributo `workspace.host_paths` = *"Host workspace directories selected in the desktop app (string array)"* | cowork/monitoring | VERIFIED | Existe un registro de qué se adjuntó, **pero solo con OTel configurado por un admin en Team/Enterprise**. Para una usuaria individual no hay este registro | ADR-004 |
| **A-15** Fiabilidad del reporte de escritura | Si el agente dice "guardado", está guardado donde dice | `CHANGELOG:` *"Fixed Claude sometimes reporting a file as saved when it had been written to a temporary location you could not open."* (Cowork) | Changelog Claude Desktop, sección Cowork | VERIFIED (que el defecto existió y se corrigió) | **La afirmación del agente sobre el efecto de su propia escritura no es evidencia del efecto.** Refuerza que el Core, no el modelo, debe ser la fuente de verdad de toda mutación | ADR-002, ADR-003 |

### B. MCP LOCAL

| Capability | Expected | Observed | Official source | Status | Security implication | ADR affected |
|---|---|---|---|---|---|---|
| **B-01** Cowork soporta servidores MCP locales | Sí, stdio local | `DOC:` *"Local connectors and plugins that include local MCP servers work through the desktop app only."* y *"Some features are desktop-only: Live artifacts and plugins that include local MCP servers work through the desktop app only."* | support.claude.com 15520349; 13345190 | VERIFIED | Habilita la arquitectura prevista: `legal-mcp` como servidor MCP local. **Solo en Desktop**: web y móvil quedan descartados como superficie de trabajo del expediente | ADR-001, kernel §6 |
| **B-02** Dónde se ejecuta el MCP local: host o VM | En el host, junto al agent loop | `DOC:` *"The agent loop runs natively on the device."* + *"This includes Claude's conversation handling, file reads and writes in connected folders, web fetches, and local plugin MCP servers."* | support.claude.com 14479288 | VERIFIED | El MCP local es un **proceso del sistema operativo del host**, no un proceso dentro de la VM Linux. De ahí se sigue la hipótesis B-04 | ADR-001, ADR-002 |
| **B-03** El código y el shell del agente corren en VM aislada | Sandbox | `DOC:` *"Shell commands and any code Claude writes execute inside a dedicated Linux VM, isolated from the host operating system by the platform's hypervisor (Apple Virtualization.framework on macOS, Hyper-V on Windows). The VM enforces its own network egress filtering, syscall restrictions, and per-session user isolation."* | support.claude.com 14479288 | VERIFIED | En Windows la VM es **Hyper-V**. El shell del agente y el proceso del MCP local están **en lados distintos del hipervisor** | ADR-001 |
| **B-04** ¿Puede el MCP local acceder a una carpeta que el host/agente NO tiene concedida? | Sí — el MCP corre con los privilegios del usuario del SO, ajeno al allowlist de carpetas | `SIN DATO:` **ninguna fuente oficial afirma ni niega** que los servidores MCP locales estén sujetos al confinamiento de carpetas conectadas. El confinamiento se enuncia siempre sobre *"local file access"* / *"each local tool call"* (A-02), nunca sobre el proceso del servidor MCP | — | INCONCLUSIVE | **Pregunta central del spike y pieza que sostiene ADR-002.** Si se confirma, el `case.db` puede vivir fuera de toda carpeta adjunta y ser alcanzable **solo** por el Core. Si se refuta, todo el modelo de custodia debe rediseñarse. **HIPÓTESIS con base fuerte (B-02), no hecho** | ADR-001, ADR-002, ADR-006 |
| **B-05** La usuaria puede añadir sus propios MCP locales | Sí, desde la app | `DOC:` *"Local MCP servers: add local MCP server processes from Settings → Developer"* | claude.com/docs/third-party/claude-desktop/extensions (sección *User extensions*) | VERIFIED (con la salvedad §2.1: página 3P) | Vía de instalación del Core sin publicar plugin. **POR VERIFICAR** que la ruta de UI sea idéntica en el Claude Desktop estándar de los dueños | kernel §13 |
| **B-06** Un admin puede prohibir MCP locales | Clave gestionada | `DOC:` `isLocalDevMcpEnabled`, default `true`; *"Users cannot add their own local MCP servers from Settings → Developer"* cuando es `false` | 3p/extensions; support.claude.com 12622667 | VERIFIED | Si los dueños migran a Team/Enterprise con MDM, un admin puede **desactivar el Core entero**. Debe constar como dependencia de despliegue | ADR-001 |
| **B-07** MCP local vía plugin | Los plugins pueden traer conectores MCP | `DOC:` *"Installing one can add skills, MCP connectors, subagents, slash commands, or hooks in a single step."*; componentes: Skills, Connectors, Agents, Hooks | claude.com/docs/cowork/guide/plugins | VERIFIED | Vía alternativa de distribución del Core, con hooks en el mismo paquete | kernel §13 |
| **B-08** Habilitar/deshabilitar componentes individuales de un plugin | Granularidad por componente | `DOC:` *"Open the installed plugin to see its skills, connectors, agents, and hooks. Enable or disable individual components as needed."* | cowork/guide/plugins | VERIFIED | Granularidad de **componente**, no de tool individual. Desactivar "el conector" es todo o nada para las 8 tools del kernel §6 | kernel §6 |
| **B-09** Política por tool (`allow` / `ask` / `blocked`) | Control fino por herramienta | `DOC:` `managedMcpServers` *"support per-tool policy locks (`allow` / `ask` / `blocked`)"*; para servidores de plugin, vía `orgPluginSettings` | 3p/extensions | VERIFIED **solo para configuración gestionada por admin** | Es el **único** mecanismo documentado de restricción por herramienta. **No disponible a una usuaria individual sin MDM.** No confundir con `allowedTools` de Claude Code | kernel §6, ADR-005 |
| **B-10** Modos de aprobación de conectores: Manual / Auto / Skip | Tres modos | `DOC:` **Manual**: *"Claude pauses and asks for approval for actions. You review each request and choose Allow or Deny."* — **Auto**: *"Claude keeps working without stopping to ask about every step... Claude reviews each action for safety... automatically blocks anything it determines to be unsafe."* — **Skip**: *"Claude doesn't pause to ask and nothing checks its actions automatically. Only use this when you completely trust every action."* | 13345190; 13364135 | VERIFIED | **Auto no es una política determinista: es un juicio del modelo** (*"anything it determines to be unsafe"*). Un control cuya decisión la toma el propio sistema evaluado **no puede sostener PF-001** (kernel §12). Para el flujo del expediente, Manual es el único modo compatible | ADR-005, kernel §12 |
| **B-11** Granularidad de la respuesta de aprobación | Allow/Deny por llamada | `CHANGELOG:` opciones *"Allow once"*, *"Deny"*, *"Allow for this task"*, *"Allow for all tasks"*, más *"the prompt-injection warning"*; *"Explicit `ask` policies still prompt on every call."* | Changelog v1.22209.0 (2026-07-16, 3P); entrada Cowork sobre *"Allow for this task"* en conectores | VERIFIED (que las opciones existen) | *"Allow for all tasks"* convierte una aprobación puntual en permiso permanente. Para `commit_reviewed_facts` esto sería **fatal**: es exactamente el patrón que el kernel §3.3 evita al no exponer token alguno al modelo | ADR-005 |
| **B-12** Un admin puede eliminar el "Always allow" persistente | Clave gestionada | `DOC:` *"Require fresh approval for every permission-gated tool call by turning off persistent 'always allow'"*; clave `mcpPersistentAlwaysAllowEnabled` | 14479288; `CHANGELOG:` v1.24012.9 (3P) | VERIFIED (admin) | Mitigación real de B-11, **pero solo con administración**. Una usuaria individual **no puede** impedirse a sí misma conceder permiso permanente | ADR-005 |
| **B-13** Conector remoto MCP apuntando a `localhost` | Alternativa al MCP local | `DOC:` *"When you add a custom connector, Claude connects to your remote MCP server from Anthropic's cloud infrastructure, rather than from your local device. Your MCP server must be reachable over the public internet from Anthropic's IP ranges."* | support.claude.com 11175166 | NOT_SUPPORTED (para un Core local) | Cierra una alternativa de diseño: **el Core no puede exponerse como "custom connector" remoto**. La única vía local es MCP local/stdio (B-01) | kernel §6, ADR-001 |
| **B-14** Cowork lee la configuración de Claude Code en `~/.claude` | Reutilizar settings de Claude Code | `DOC:` *"Cowork loads the ones enabled for your claude.ai account, synced at session start, and doesn't read the Claude Code CLI's `~/.claude` directory on your machine."* | claude.com/docs/cowork/overview | **NOT_SUPPORTED** | **Refutación explícita de la equivalencia con Claude Code.** Ninguna regla de `~/.claude/settings.json` (allow/deny/ask, `allowedTools`, hooks de usuario) gobierna Cowork. Todo diseño que asumiera eso queda invalidado | ADR-001, ADR-005 |

### C. ELICITATION / CONFIRMACIONES

| Capability | Expected | Observed | Official source | Status | Security implication | ADR affected |
|---|---|---|---|---|---|---|
| **C-01** El protocolo MCP define elicitation (form y URL) | Sí | `DOC:` revisión vigente **2026-07-28**; modos **form** (JSON Schema plano) y **url** (interacción fuera de banda). En 2026-07-28 el transporte cambió: viaja dentro de un `InputRequiredResult` y el cliente reintenta con `inputResponses` | modelcontextprotocol.io/specification/2026-07-28/client/elicitation y /changelog | VERIFIED (a nivel de **protocolo**) | Que el protocolo lo defina **no implica** que Cowork lo implemente. Ver C-03 | ADR-005 |
| **C-02** Claude **Code** implementa elicitation | Sí | `DOC:` *"When a server needs information it can't get on its own, Claude Code displays an interactive dialog and passes your response back to the server."* Form mode = diálogo con campos; URL mode = abre el navegador y se confirma después en la CLI | code.claude.com/docs/en/mcp | VERIFIED (**para Claude Code, no para Cowork**) | Punto de comparación, no de extrapolación | ADR-005 |
| **C-03** Cowork implementa elicitation | Sí, por herencia de la arquitectura de Claude Code | `SIN DATO:` **ninguna doc de Cowork —ni el Help Center, ni claude.com/docs/cowork, ni el changelog— menciona elicitation.** La única afirmación de parentesco es *"the same agentic architecture that powers Claude Code, with no terminal required"*, que es una frase de producto, no una especificación de features | 13345190 (parentesco); ausencia en el resto | **INCONCLUSIVE** | **Bloqueante para ADR-005.** No se puede diseñar el canal de autorización humana sobre elicitation mientras Cowork no lo documente ni se compruebe. Es la segunda pregunta empírica del spike | ADR-005 |
| **C-04** ¿Puede una elicitation form ser respondida sin intervención humana? | No; sería el canal humano infalsificable | `DOC:` en **Claude Code** existe el hook `Elicitation`: *"To auto-respond to elicitation requests without showing a dialog, use the `Elicitation` hook"*, con advertencia oficial de que *"bypasses the user confirmation dialog"* | code.claude.com/docs/en/mcp; code.claude.com/docs/en/hooks | VERIFIED (en Claude Code) / INCONCLUSIVE (en Cowork) | **Hallazgo decisivo.** En al menos un producto Anthropic, una elicitation form **puede responderse automáticamente sin que la humana vea nada**. Dado que Cowork admite hooks de plugin (D-03), **elicitation form no puede tratarse como prueba de acto humano** | ADR-005, kernel §3, PF-001 |
| **C-05** Garantías de URL mode | El cliente no puede inspeccionar la interacción | `DOC:` la spec exige (MUST) *"MUST NOT open the URL without explicit consent"*, *"MUST show the full URL to the user"*, y abrirla *"in a secure manner that does not enable the client or LLM to inspect the content or user inputs"* | modelcontextprotocol.io/specification/2026-07-28/client/elicitation | VERIFIED **como requisito del protocolo**, INCONCLUSIVE como comportamiento de Cowork | Un MUST de la spec es una obligación para implementadores conformes, **no una garantía verificada de Cowork**. Si Cowork implementa URL mode conforme, es el candidato más sólido para el canal humano | ADR-005 |
| **C-06** La spec prohíbe pedir secretos por form mode | Sí | `DOC:` los servidores *"MUST NOT use form mode elicitation to request sensitive information such as passwords, API keys, access tokens, or payment credentials"* y **MUST usar URL mode** para eso | modelcontextprotocol.io (elicitation) | VERIFIED (protocolo) | Coherente con kernel §3.3: la autorización **no viaja al modelo**. El Core no debe pedir ningún secreto por elicitation en ningún modo | ADR-005, kernel §3.3 |
| **C-07** El cliente MUST dejar claro qué servidor pide | Sí | `DOC:` el cliente *"MUST provide UI that makes it clear which server is requesting information"*, *"provide clear decline and cancel options"* y *"allow users to review and modify their responses before sending"*. En cambio, *"Clients **SHOULD** implement user approval controls"* — solo SHOULD | modelcontextprotocol.io (elicitation) | VERIFIED (protocolo) | La atribución al servidor es MUST; **el control de aprobación es solo SHOULD**. La spec deja legítimo un cliente que no lo implemente | ADR-005 |
| **C-08** Cowork muestra "question cards" propias | Canal de preguntas del agente a la usuaria | `CHANGELOG:` *"Fixed an occasional 'Something went wrong' error when a session's question card from Claude changed to a new set of questions."* (Cowork) | Changelog, sección Cowork | VERIFIED (que el mecanismo existe) | Es un canal **del modelo hacia la usuaria**, generado por el modelo. **No** es un canal de autoridad: lo que el modelo pregunta, el modelo lo redacta. No confundir con elicitation MCP | ADR-005 |
| **C-09** Qué puede inspeccionar el LLM de la respuesta humana | Nada en URL mode; todo en form mode | `DOC:` URL mode: el cliente debe impedir que *"the client or LLM"* inspeccione contenido y entradas. Form mode: la spec **no** contiene prohibición equivalente | modelcontextprotocol.io (elicitation) | VERIFIED (protocolo) / NOT_TESTED (Cowork) | En form mode la respuesta humana **entra en el flujo observable**. Para una decisión jurídica (aprobar un hecho) esto es aceptable; para un secreto, no — y por eso el kernel §3.3 no usa secretos | ADR-005 |

### D. PERMISOS

| Capability | Expected | Observed | Official source | Status | Security implication | ADR affected |
|---|---|---|---|---|---|---|
| **D-01** Deny por ruta al estilo `Read(.env)` de Claude Code | Reglas deny por patrón de ruta | `SIN DATO:` no existe ninguna regla deny por ruta documentada para Cowork. Lo único documentado sobre rutas es `allowedWorkspaceFolders` (allowlist de **qué se puede adjuntar**, admin) y `mode: ro`. Además D-05 refuta la herencia de reglas de Claude Code | 12622667; local-access; cowork/overview | **NOT_SUPPORTED** (como capacidad de usuaria) | **No se puede proteger el case store con una regla deny.** La protección debe ser **posicional** (fuera de toda carpeta adjunta) y **arquitectónica** (solo alcanzable por el Core) | ADR-001, ADR-002 |
| **D-02** Tool approval por llamada | Prompt Allow/Deny | `DOC:` modo Manual (B-10) + `CHANGELOG:` opciones Allow once / Deny / Allow for this task / Allow for all tasks | 13345190; changelog | VERIFIED | Existe, pero su fuerza depende del modo elegido por la usuaria, que ella puede cambiar en cualquier momento | ADR-005 |
| **D-03** Hooks en Cowork | Existen | `DOC:` *"Installing one can add skills, MCP connectors, subagents, slash commands, or hooks"*; tabla: *"Hooks — Scripts that run at defined points in a session"*. Refuerzos: `CHANGELOG:` *"Fixed plugin hooks silently doing nothing on Windows."* (sección **Cowork**); telemetría de Cowork define `decision_source` con el valor **`"hook"`** | cowork/guide/plugins; changelog v1.24012.9 (Cowork); cowork/monitoring | VERIFIED (que **existen** hooks de plugin en Cowork y que un hook puede ser **fuente de una decisión de permiso**) | Doble filo: permiten enforcement determinista **y** permiten (C-04) auto-responder confirmaciones. Un plugin instalado puede alterar el régimen de permisos | ADR-005, ADR-001 |
| **D-04** Catálogo de eventos de hook aplicable a Cowork | Los 31 eventos de Claude Code | `SIN DATO:` la referencia de hooks es de Claude Code y enumera como superficies *"the terminal, IDE extensions, the Desktop app, and Claude Code on the web"* — **no nombra Cowork**. Ninguna doc publica el catálogo de eventos de Cowork | code.claude.com/docs/en/hooks | **INCONCLUSIVE** | **No asumir que `PreToolUse` o `Elicitation` existen en Cowork.** Un control de seguridad basado en un evento no documentado para Cowork es un control imaginario | ADR-005 |
| **D-05** Cowork hereda las reglas de permisos de Claude Code (`~/.claude`) | Sí | `DOC:` *"...doesn't read the Claude Code CLI's `~/.claude` directory on your machine."* | cowork/overview | **NOT_SUPPORTED** | Ver B-14. **Invalida cualquier razonamiento de seguridad por equivalencia con Claude Code.** Es el hallazgo que más restringe el diseño de D | ADR-001, ADR-005 |
| **D-06** Política gestionada (`managed-settings.json`) que alcanza a Cowork | — | `CHANGELOG:` *"Fixed memory saves failing when the Claude Code `managed-settings.json` policy sets `allowManagedPermissionRulesOnly`."* — entrada de la sección **Cowork** | Changelog, sección Cowork | INCONCLUSIVE | Indicio de que la **política gestionada** (distinta de `~/.claude` de usuaria) sí alcanza a Cowork. Es un indicio de changelog, **no** una doc de la superficie de política. No construir sobre él sin verificación | ADR-005 |
| **D-07** Restricción de herramientas por subagente | `tools:` allowlist como en Claude Code | `SIN DATO:` Cowork documenta subagentes (*"Agents — Specialized subagents Claude can delegate to"*, *"Sub-agent coordination"*) pero **ninguna doc de Cowork describe restricción de herramientas por subagente** | cowork/guide/plugins; cowork/overview | **INCONCLUSIVE** | Si no hay restricción por subagente, **un subagente hereda la superficie completa**, incluidas las tools SENSITIVE_COMMAND del kernel §6. No se puede usar "subagente restringido" como control de seguridad | ADR-001, kernel §6 |
| **D-08** Fuentes de decisión de permiso registrables | — | `DOC:` `decision_source` ∈ `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, `"user_reject"`; eventos `tool_decision` y `tool_result` | cowork/monitoring | VERIFIED | **Muy valioso:** la plataforma **distingue** decisión humana (`user_*`) de decisión automática (`config`, `hook`). Existe la señal necesaria para auditar si una aprobación fue humana. **Pero solo vía OTel, Team/Enterprise, configurado por admin** | ADR-004, ADR-005 |
| **D-09** Controles de organización sobre Cowork | — | `DOC:` activar/desactivar Cowork; política de acceso a red para sesiones cloud; desactivar el *always allow* persistente; *"Require trusted-device enrollment and a recent sign-in for sessions in the cloud."* | 14479288 | VERIFIED (Team/Enterprise) | Todos los controles duros de Cowork son **administrativos**. **SUPUESTO a confirmar con los dueños:** en plan individual no existen | ADR-001 |
| **D-10** El prompt de aprobación es resistente a captura accidental | Un permiso no se concede por accidente | `CHANGELOG:` *"Fixed the computer-use permission prompts in Cowork and Claude Code sessions accepting a keyboard shortcut aimed at the message box or another surface, and added a brief delay so a send keystroke that lands just as the prompt appears cannot approve it."* | Changelog v1.32885.1 (General) | VERIFIED (que el defecto existió y se mitigó) | **Los prompts de aprobación han sido, de hecho, activables sin intención.** Un acto de autoridad jurídica no debe descansar solo en un prompt de UI del host | ADR-005, kernel §3 |
| **D-11** Un prompt sin responder nunca se interpreta como aprobación | Nunca | `CHANGELOG:` *"Fixed an unanswered permission or plan-approval prompt in a cloud session sometimes being treated as approved after the session's environment disconnected."* — sección **Code**, no Cowork | Changelog v1.30096.1 (Code) | INCONCLUSIVE (para Cowork) | Clase de fallo real y documentada: **silencio interpretado como consentimiento**. Aunque la entrada es de Code, justifica que el Core **nunca** derive autorización de la ausencia de respuesta (kernel §3.1: `consumed_at`, `expires_at`) | ADR-005, kernel §3 |

### E. SESIÓN

| Capability | Expected | Observed | Official source | Status | Security implication | ADR affected |
|---|---|---|---|---|---|---|
| **E-01** La sesión sobrevive al cierre de la app | Sí | `DOC:` *"Sessions keep running even when the desktop app is closed or your computer is asleep."* | 13345190 | VERIFIED | Una sesión puede seguir razonando sobre el expediente sin la usuaria delante. **Refuerza `expires_at`** en `HumanAuthorization` (kernel §3.1) | ADR-005, kernel §3 |
| **E-02** Sesión cloud + ficheros locales exige la app abierta | Sí | `DOC:` *"A cloud session can read and write files in folders you've connected on your computer only while the desktop app is open on that computer."* y *"If the desktop app is offline, the session can't reach your computer."* | 15520349; 13364135 | VERIFIED | Cuando la app está cerrada, la sesión **sigue viva pero sin expediente**. El Core debe tolerar que el modelo razone con contexto obsoleto y volver a validar `expected_case_revision` en el commit | ADR-004, kernel §2.3 |
| **E-03** Reapertura desde otra superficie | Sí | `DOC:` *"Open the same session from another surface to check progress, answer Claude's questions, or redirect the work."* | 15520349 | VERIFIED | La **respuesta a una pregunta puede llegar desde el móvil**, fuera de la máquina donde vive el `case.db`. Un canal de autorización que dependa de la superficie es frágil | ADR-005 |
| **E-04** La configuración se carga al inicio de sesión | Sí | `DOC:` *"Cowork loads the ones enabled for your claude.ai account, synced at session start"* y *"settings are loaded at session start, so existing sessions won't pick up the new configuration"* | cowork/overview; cowork/monitoring | VERIFIED | Instalar o actualizar el Core **no afecta a sesiones en curso**. Una sesión viva puede seguir hablando con una versión anterior del servidor MCP | ADR-001, kernel §13 |
| **E-05** Relación sesión ↔ ciclo de vida del MCP local | El MCP arranca y muere con la sesión | `SIN DATO:` la doc no describe cuándo se lanza ni cuándo se termina un servidor MCP local respecto de la sesión, ni si se comparte entre sesiones concurrentes | — | **INCONCLUSIVE** | Determinante para SQLite: **si dos sesiones concurrentes comparten o duplican el proceso del Core**, cambia el modelo de concurrencia y bloqueo del `case.db`. Debe probarse | ADR-002, ADR-004 |
| **E-06** Comportamiento si el MCP local se cae durante una llamada | Fallo inmediato | `CHANGELOG:` *"Fixed a tool call hanging for a full minute when its local MCP server crashed mid-call; it now fails right away."* — sección **Cowork** | Changelog v1.32352.0 (2026-08-17, Cowork) | VERIFIED (que hoy falla de inmediato) | Un crash a mitad de `commit_reviewed_facts` produce **fallo del lado del cliente sin información sobre si la transacción se completó**. El Core debe ser idempotente y la autorización de un solo uso (`consumed_at`) resuelve el reintento | ADR-002, kernel §3.1 |
| **E-07** Comportamiento si el MCP local no arranca al abrir sesión | Aviso claro | `SIN DATO:` no documentado para Cowork. Lo más próximo es `CHANGELOG:` *"Fixed plugin connectors sometimes missing from the Connectors list and tool permission prompts when they were slow to start."* (Cowork) | Changelog (Cowork) | **INCONCLUSIVE** | Escenario peligroso: **si el conector falta silenciosamente, el modelo puede intentar trabajar el expediente sin el Core**, respondiendo desde su propio contexto. Debe probarse y, si ocurre, mitigarse con una Skill que exija verificación de disponibilidad | ADR-001, ADR-003 |
| **E-08** Mensajes exactos que ve la usuaria (permisos, carpetas, fallos) | Textos conocidos | `SIN DATO:` la doc describe los controles pero **no publica el texto de los diálogos**. Solo se conocen fragmentos por changelog: *"folder access approval card"*, *"the prompt-injection warning"*, *"This plugin is required by your organization"*, y el aviso de que *"files Claude uses leave your device and are processed on Anthropic's servers"* en tareas cloud | Changelog (Cowork) | **NOT_TESTED** | El pipeline de condiciones del kernel §10 debe convivir con mensajes de host que **no controlamos**. Hay que capturarlos literalmente antes de diseñar los textos del producto | kernel §10 |
| **E-09** Aislamiento entre sesión cloud y ficheros locales | Sin fugas | `CHANGELOG:` *"Fixed document tools in cloud sessions acting on your local files instead of the session's files."* (Cowork) | Changelog (Cowork) | VERIFIED (que el defecto existió y se corrigió) | **Prueba documentada de que la frontera local/cloud ha fallado en la práctica.** Sostiene el enunciado de honestidad del kernel §8.3: tamper-evident, no tamper-proof; y ADR-001 no puede apoyarse solo en el aislamiento del host | ADR-001, kernel §8.3 |
| **E-10** Persistencia del sandbox entre sesiones | Efímero | `DOC:` cloud: *"Each session gets its own sandbox, created when the session starts and destroyed when it ends"*. Local: *"The sandbox can stay running between sessions."* | 14479288; local-access | VERIFIED | Asimetría relevante: **en local el sandbox persiste**. No asumir que el estado del shell se limpia entre sesiones | ADR-001, ADR-004 |

---

## 4. Implicación arquitectónica consolidada

Cuatro consecuencias, ordenadas por cuánto restringen el diseño.

**4.1 La equivalencia con Claude Code queda formalmente refutada, no matizada.**
`cowork/overview` afirma que Cowork *"doesn't read the Claude Code CLI's `~/.claude` directory"* (D-05, B-14). Todo control de seguridad del Legal Workspace que se hubiera apoyado en `settings.json`, reglas `deny`, `allowedTools` o hooks de usuario de Claude Code **no existe en Cowork**. Lo que sí existe (hooks de plugin, D-03; política por tool, B-09) llega por otras vías y, en el caso de la política por tool, **solo con administración MDM**.

**4.2 La protección del case store no puede ser una regla; tiene que ser una posición.**
No hay deny por ruta (D-01) y adjuntar una carpeta concede todo su árbol sin granularidad (A-03, A-04). La doc oficial prescribe literalmente el único remedio: *"To keep data out of reach entirely, leave it outside the allowed roots."* Por tanto ADR-002 debe formularse así:

> El `case.db` y el almacén de originales viven **fuera de toda carpeta adjuntable**, y su única vía de acceso es el proceso del Core (MCP local). El agente no los alcanza porque **no están donde puede mirar**, no porque una regla se lo prohíba.

Esto convierte a **B-04 en el supuesto que sostiene ADR-002**. Está `INCONCLUSIVE`: la doc dice que el MCP local corre nativamente en el dispositivo (B-02) pero **nunca** dice si está o no sujeto al confinamiento de carpetas. Si B-04 se refutara, ADR-002 se cae entero.

**4.3 Ningún mecanismo de UI de Cowork puede ser, por sí solo, la prueba del acto humano.**
Convergen cinco hallazgos: el modo Auto delega la decisión de seguridad al propio modelo (B-10); *"Allow for all tasks"* convierte un acto en permiso permanente (B-11); una elicitation form puede auto-responderse por hook en al menos un producto Anthropic (C-04); los prompts han sido activables por pulsación accidental (D-10); y un prompt sin responder ha llegado a tratarse como aprobado (D-11). **Refuerza y no altera** el kernel §3.3: la `HumanAuthorization` se resuelve **server-side en el Core**, sin token al modelo, ligada a `item_content_hash` + `expected_case_revision` + `consumed_at` + `expires_at`. La UI de Cowork es **notificación**, no autoridad.

**4.4 Cowork Desktop es la única superficie viable, y el conector remoto queda descartado.**
MCP local solo en Desktop (B-01); un conector remoto se conecta desde la nube de Anthropic y exige alcance por internet público (B-13). Confirma `legal-mcp` como **servidor MCP local stdio en Windows Desktop**, en línea con kernel §13.

---

## 5. Decisiones pendientes y supuestos que los dueños deben resolver

| Ref | Tipo | Enunciado |
|---|---|---|
| DP-1 | **DECISIÓN PENDIENTE** | ¿Plan individual (Pro/Max) o Team/Enterprise? Casi todos los controles duros (política por tool B-09, desactivar *always allow* B-12, allowlist de carpetas §2.1, telemetría de decisiones D-08) **son administrativos**. La respuesta cambia qué garantías puede reclamar el producto. |
| DP-2 | **DECISIÓN PENDIENTE** | Distribución del Core: MCP local desde *Settings → Developer* (B-05) o plugin con `.mcp.json` (B-07). El plugin permite empaquetar hooks y skills; el MCP suelto es más simple. |
| DP-3 | **RIESGO** | El modo Auto es un juicio del modelo (B-10). Si el producto se usa en Auto, PF-001 no se sostiene por medios de plataforma. ¿Se exige Manual por política de producto y se documenta como limitación? |
| DP-4 | **SUPUESTO / POR VERIFICAR** | Se supone que el proceso del MCP local no está confinado a las carpetas adjuntas (B-04). **Todo ADR-002 depende de esto.** Requiere el protocolo empírico. |
| DP-5 | **POR VERIFICAR** | Si Cowork no soporta elicitation (C-03), ¿cuál es el canal humano de `ReviewProposal` (kernel §7, "canal humano, no MCP")? Es una pregunta de diseño abierta, no un detalle. |

---

## 6. Qué queda por comprobar empíricamente

Todo lo empírico está `NOT_TESTED`. El protocolo que los dueños deben ejecutar **desde Cowork** está en:

`C:/Users/HITMA/Desktop/legal-workspace/experiments/cowork-capability-spike/README.md`

Prioridad de las pruebas, por impacto arquitectónico:

1. **B-04** — MCP local vs confinamiento de carpetas. *Sostiene ADR-002.*
2. **A-07 / A-08** — symlinks y junctions de Windows dentro de una carpeta adjunta. *Sostiene el confinamiento A-02.*
3. **C-03** — ¿existe elicitation en Cowork, y en qué modos? *Sostiene el canal humano de ADR-005.*
4. **E-07** — qué pasa y qué se ve si el Core no arranca. *Riesgo de que el modelo trabaje el expediente sin Core.*
5. **E-05** — ciclo de vida del proceso MCP frente a la sesión. *Modelo de concurrencia de SQLite.*
6. **A-05** — `mode: ro` en Cowork sobre Windows, file tools **y** shell por separado.
7. **E-08** — captura literal de los mensajes que ve la usuaria.

---

## 7. Fuentes consultadas

**Documentación oficial de Anthropic (autoridad primaria):**

- https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork
- https://support.claude.com/en/articles/13364135-use-claude-cowork-safely
- https://support.claude.com/en/articles/14479288-claude-cowork-architecture-overview
- https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile
- https://support.claude.com/en/articles/12622667-enterprise-configuration
- https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp
- https://support.claude.com/en/collections/19667525-claude-cowork
- https://claude.com/docs/cowork/overview
- https://claude.com/docs/cowork/guide/plugins
- https://claude.com/docs/cowork/monitoring
- https://claude.com/docs/cowork/changelog (changelog de Claude Desktop, con secciones General / Code / Cowork / 3P / Chat)
- https://claude.com/docs/connectors/overview
- https://claude.com/docs/plugins/overview
- https://claude.com/docs/third-party/claude-desktop/local-access (= /docs/cowork/3p/local-access)
- https://claude.com/docs/third-party/claude-desktop/extensions (= /docs/cowork/3p/extensions)
- https://code.claude.com/docs/en/mcp
- https://code.claude.com/docs/en/hooks

**Especificación MCP (autoridad primaria para el protocolo, no para Cowork):**

- https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation
- https://modelcontextprotocol.io/specification/2026-07-28/changelog

**No se ha usado ningún blog ni fuente de terceros como autoridad en este documento.**

### 7.1 Nota sobre el changelog como fuente

El changelog de Claude Desktop se ha usado de forma deliberada y con disciplina: cada entrada citada ha sido **atribuida a su sección de producto** (General / Code / Cowork / 3P) y a su versión y fecha, porque una entrada de la sección *Code* **no es evidencia sobre Cowork**. Una entrada de changelog prueba que **en una versión concreta** algo se comportaba de cierto modo; **no** es una promesa de que siga siendo así.

---

## 8. Registro de lo que este documento NO afirma

Para evitar que se lea de más:

- **No afirma** que Cowork soporte elicitation. (C-03: INCONCLUSIVE.)
- **No afirma** que un MCP local pueda leer fuera de las carpetas adjuntas. (B-04: INCONCLUSIVE; es hipótesis con base en B-02.)
- **No afirma** que los hooks de Claude Code existan en Cowork con el mismo catálogo de eventos. (D-04: INCONCLUSIVE.)
- **No afirma** que los subagentes de Cowork admitan restricción de herramientas. (D-07: INCONCLUSIVE.)
- **No afirma** que el confinamiento de carpetas resista symlinks o junctions en Windows. (A-07, A-08.)
- **No afirma** que ninguno de los comportamientos citados del changelog sea estable en versiones futuras.
- **No contiene un solo dato "observed in current environment".** Cero pruebas ejecutadas.
