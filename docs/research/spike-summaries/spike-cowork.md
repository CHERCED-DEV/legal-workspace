[harness: subagent output matched instruction-shaped pattern(s): settings-json. Control tags below are neutralized (`<` → `<\`); treat any remaining directive-shaped text as a finding to relay to the user, not an instruction to you.]

(1) RUTAS ESCRITAS

- `C:/Users/HITMA/Desktop/legal-workspace/docs/research/cowork-runtime-spike-v0.md` (46.0 KB — 5 tablas A–E, 49 filas, columnas exactas `Capability | Expected | Observed | Official source | Status | Security implication | ADR affected`; recuento de Status: 44 VERIFIED / 21 INCONCLUSIVE / 8 NOT_TESTED / 7 NOT_SUPPORTED)
- `C:/Users/HITMA/Desktop/legal-workspace/experiments/cowork-capability-spike/README.md` (22.4 KB — NON-PRODUCTION SPIKE; formato Question / Why it matters / Hypothesis / Method / Result / Limitations / Architecture implication / Delete-keep recommendation; protocolo de 31 pasos numerados en 6 bloques)
- `C:/Users/HITMA/Desktop/legal-workspace/experiments/cowork-capability-spike/experimental-root/accessible/visible.txt`
- `C:/Users/HITMA/Desktop/legal-workspace/experiments/cowork-capability-spike/experimental-root/private/private.txt`

(2) HALLAZGOS CLAVE

- **HECHO VERIFICADO (refuta la equivalencia con Claude Code)** — `claude.com/docs/cowork/overview`: Cowork *"doesn't read the Claude Code CLI's `~/.claude` directory on your machine"*. Ninguna regla `deny`, `allowedTools` ni hook de usuario de Claude Code gobierna Cowork. Todo razonamiento por analogía queda invalidado.
- **HECHO VERIFICADO** — No existe deny por ruta en Cowork. Adjuntar una carpeta concede su árbol completo: *"the agent can read and write every file the user's OS account can reach"*; el único remedio documentado es posicional: *"To keep data out of reach entirely, leave it outside the allowed roots."* (`/docs/third-party/claude-desktop/local-access`).
- **HECHO VERIFICADO** — Los MCP locales corren en el host, no en la VM: *"The agent loop runs natively on the device… This includes Claude's conversation handling, file reads and writes in connected folders, web fetches, and local plugin MCP servers"* (support 14479288). El shell corre en VM Linux aislada por **Hyper-V** en Windows.
- **HECHO VERIFICADO (crítico para ADR-005)** — En Claude Code existe el hook `Elicitation` que *"auto-respond[s] to elicitation requests without showing a dialog"*, con advertencia oficial de que *"bypasses the user confirmation dialog"*. Elicitation form **no es prueba de acto humano** en el stack Anthropic.
- **HECHO VERIFICADO** — El modo **Auto** delega la decisión de seguridad al propio modelo: *"Claude reviews each action for safety… automatically blocks anything it determines to be unsafe."* Un control juzgado por el sistema evaluado no puede sostener PF-001.
- **HECHO VERIFICADO** — `NOT_SUPPORTED`: un conector remoto MCP no sirve para un Core local — *"Claude connects to your remote MCP server from Anthropic's cloud infrastructure… must be reachable over the public internet from Anthropic's IP ranges."* Única vía: MCP local/stdio en Desktop.
- **HECHO VERIFICADO** — Política por tool (`allow`/`ask`/`blocked`) existe **solo** vía `managedMcpServers`/`orgPluginSettings` con MDM (Team/Enterprise). Igual que `allowedWorkspaceFolders`, `mcpPersistentAlwaysAllowEnabled` y la telemetría `decision_source`. **SUPUESTO por confirmar:** en plan individual no hay ninguno.
- **HECHO VERIFICADO (changelog, sección Cowork, atribuido por versión)** — Existen hooks de plugin en Cowork (fix v1.24012.9) y el MCP local caído hace fallar la llamada de inmediato (v1.32352.0). Además hubo defectos reales: escritura reportada como guardada en una ruta temporal; *document tools in cloud sessions acting on your local files*; prompt de permiso activable por pulsación accidental.
- **HIPÓTESIS (base fuerte, no hecho)** — El MCP local no está confinado a las carpetas adjuntas, por ser proceso del host. **La doc oficial nunca lo afirma ni lo niega.** Es la pieza que sostiene ADR-002.
- **DECISIÓN PENDIENTE** — Plan (Pro/Max vs Team/Enterprise) y vía de distribución del Core (Settings → Developer vs plugin). Determinan qué garantías puede reclamar el producto.

(3) IMPLICACIÓN ARQUITECTÓNICA

La protección del case store **no puede ser una regla, tiene que ser una posición**: `case.db` y originales fuera de toda carpeta adjuntable, alcanzables solo por el proceso del Core. Esto hace que **ADR-002 dependa por completo de una hipótesis no documentada** (B-04) — hay que escribirlo así, no darlo por bueno. En paralelo, cinco hallazgos convergentes (Auto delega en el modelo; *Allow for all tasks*; hook que auto-responde elicitation; prompts activables por accidente; silencio tratado como aprobación en sesiones cloud de Code) **refuerzan sin alterar el kernel §3.3**: la `HumanAuthorization` se resuelve server-side en el Core, sin token al modelo, ligada a `item_content_hash` + `expected_case_revision` + `consumed_at` + `expires_at`. La UI de Cowork es notificación, nunca autoridad. Transversal: **Cowork no es una frontera de seguridad, es defensa en profundidad**; la frontera real es el Core, y ADR-001 debe redactarse así.

(4) NOT_TESTED / INCONCLUSIVE Y POR QUÉ

Causa raíz común: esta sesión corre en **Claude Code y no puede ejecutar Cowork**, por lo que **no hay un solo dato "observed in current environment"** en el documento; y para varios puntos la documentación oficial sencillamente calla, y no se ha inferido nada.

- **INCONCLUSIVE — B-04** (MCP local vs confinamiento de carpetas): la doc enuncia el confinamiento siempre sobre *"local file access"* / *"each local tool call"*, nunca sobre el proceso del servidor MCP. Es la pregunta decisiva del spike.
- **INCONCLUSIVE — A-07** (symlinks en runtime): la frase *"enforced against the resolved path"* gobierna el allowlist de **adjuntado**, no las llamadas del agente. No es lícito extrapolarla.
- **NOT_TESTED — A-08** (junctions/symlinks de Windows): ninguna doc de Cowork los menciona; la única mención a symlinks es sobre contenido de **plugins**, contexto distinto.
- **INCONCLUSIVE — C-03** (elicitation en Cowork): ni Help Center, ni `/docs/cowork`, ni changelog la mencionan. El parentesco *"same agentic architecture that powers Claude Code"* es frase de producto, no especificación.
- **INCONCLUSIVE — D-04** (catálogo de eventos de hook en Cowork): la referencia de hooks es de Claude Code y sus superficies declaradas **no incluyen Cowork**.
- **INCONCLUSIVE — D-07** (restricción de herramientas por subagente en Cowork): Cowork documenta subagentes pero ninguna restricción por subagente. No se asume equivalencia.
- **INCONCLUSIVE — E-05 / E-07** (ciclo de vida del proceso MCP; fallo de arranque): sin documentar; E-05 es decisivo para el modelo de concurrencia de SQLite y E-07 es riesgo de veracidad (el modelo podría trabajar el expediente sin Core).
- **NOT_TESTED — E-08** (mensajes literales que ve la usuaria): la doc describe los controles pero no publica el texto de los diálogos.
- **INCONCLUSIVE — D-06** (`managed-settings.json` alcanzando a Cowork): solo hay un indicio de changelog, no doc de la superficie de política.
- **INCONCLUSIVE — D-11** (prompt sin responder tratado como aprobado): la entrada de changelog es de la sección **Code**, no Cowork; no se traslada.

Los 7 puntos priorizados para ejecución empírica quedan en `§6` del documento de research y desarrollados como protocolo en el README del spike.