## 1. RUTAS ESCRITAS

- `C:/Users/HITMA/Desktop/legal-workspace/experiments/authorization-spike/README.md` (73.4 KB, 1132 líneas, 14 secciones + anexo de citas literales, marcado NON-PRODUCTION SPIKE / nivel documental 6)

## 2. HALLAZGOS CLAVE

- **HECHO VERIFICADO** — En URL mode, `action: "accept"` significa solo consentimiento para abrir la URL, no la decisión. Cita literal (spec 2026-07-28): *"It does not mean that the interaction is complete. The interaction occurs out of band and the client is not directly informed of the outcome."* La decisión nunca viaja por MCP: ocurre contra una superficie servida por el propio servidor MCP — es decir, por nuestro Core.

- **HECHO VERIFICADO** — El runtime documenta un mecanismo oficial para suprimir el diálogo humano: *"To auto-respond to elicitation requests without showing a dialog, use the `Elicitation` hook"* (`code.claude.com/docs/en/mcp`). Esto eleva el rechazo de form mode de "la spec no lo garantiza" (argumento de ADR-005) a **"el runtime documenta la capacidad que lo rompe"**. En URL mode el mismo hook solo abriría la URL: nadie la rellena, el Core no registra decisión, el sistema **falla cerrado**.

- **HECHO VERIFICADO** — Form mode expone los datos al cliente por definición de la spec: *"`"form"`: … Data is exposed to the client"* vs *"`"url"`: … Data (other than the URL itself) is not exposed to the client"*. Además la aprobación de usuario es solo SHOULD. Falla C2 por texto normativo, no por interpretación.

- **HECHO VERIFICADO** — La elicitation solo nace dentro de una tool call del modelo (*"during the processing of a client request"*; hook: *"during a tool call"*). Consecuencia: con (a), **el modelo controla cuándo se le ofrece revisar a la profesional**, en tensión con kernel §7 (*"la revisión humana no pasa por el modelo"*) en el eje temporal. No puede falsificar la decisión, pero sí elegir el momento — vector directo de la fatiga de revisión de ADR-005.

- **HECHO VERIFICADO** — El soporte es detectable en runtime: *"Clients that support elicitation MUST declare the `elicitation` capability … on each request"*, empty = form only, y *"Servers MUST NOT send elicitation requests with modes that are not supported by the client."* Convierte la incertidumbre de plataforma en rama de código determinista.

- **HECHO VERIFICADO** — (c1) CLI/TUI del runtime queda descartado dos veces: falla C1 y C2 (superficie dentro del proceso que hospeda al LLM, suprimible por hook) y **no existe en el host previsto** — Cowork es *"no terminal required"*.

- **RIESGO (nuevo, no registrado en ADR-005)** — El modelo corre como **el mismo usuario del SO** que la profesional y tiene ejecución local. Dentro de una cuenta de usuario **ningún transporte local da una frontera dura "solo el humano"**; se obtiene coste elevado, no-accidentalidad y detectabilidad. Agravante específico del dominio: el producto ingiere por diseño material adversarial (correos y oficios de la contraparte), así que la inyección de prompt es vector ordinario, no exótico.

- **POR VERIFICAR** — No se localizó documentación oficial que afirme que **Cowork** soporta MCP elicitation, en ningún modo. "Misma arquitectura agentic" ≠ "misma superficie de cliente MCP", y elicitation vive exactamente en la superficie de cliente.

- **NOT FOUND** — La spec no dice en ninguna parte que la cadena `url` quede fuera del contexto del LLM. El MUST 4 protege el contenido de la página y las entradas del usuario, no la URL. Con ejecución local, el modelo podría navegarla ⇒ obliga a que `GET` sea puramente de lectura (la spec ya prohíbe URLs pre-autenticadas por vía independiente).

- **PROPUESTA DEL TECHNICAL DESIGN** — El provider **nunca construye** la `HumanAuthorization`: devuelve decisiones, y Application estampa `item_content_hash`, `expected_case_revision` y `authorization_source` desde su propio estado y desde el descriptor estático del provider. Lo peor que puede hacer un provider comprometido o stub es mentir sobre que hubo un humano; **no puede** mentir sobre qué se aprobó ni sobre qué revisión regía. La marca pasa de "el stub debe acordarse de marcarse" a "el stub no puede dejar de estar marcado".

## 3. IMPLICACIÓN ARQUITECTÓNICA

**(a) y (b) no compiten: (a) es (b) más un lanzador.** Como en URL mode la decisión ocurre fuera de banda contra una página del servidor, elegir elicitation URL mode *sin* construir la UI local es imposible — no hay a qué apuntar la URL. Esto reordena el cálculo de coste y decisión:

- **(b1) página local del Core = canal normativo.** Único candidato que satisface C1 y C2 **estructuralmente**, sin delegar la garantía en un MUST que cumple software de terceros y que no podemos verificar en runtime. Único donde la profesional **inicia** la revisión sin el modelo. Coste marginal menor de lo aparente: el scope `pending` del kernel §9 ya obliga a construir la proyección.
- **(a) URL mode = lanzador oportunista**, activado solo si el cliente declara `elicitation:{url:{}}`; el sistema debe comportarse **idénticamente** si un hook auto-acepta.
- **(c2) CLI propia = fallback y canal de test** (desbloquea AT-013 y la batería de ADR-005 sin instrumentar navegador).

Segunda implicación: **C3 no es criterio de transporte** — lo satisface el Core en los tres candidatos, siempre que el canal lleve una referencia opaca y nunca valores vinculantes. C3 discrimina diseños, no transportes; la comparación real se juega en C1 y C2.

Tercera: **el spike no bloquea la implementación.** Port + stub + FAIL TO START + AT-013 + (c2) + (b1) no dependen de ninguna verificación pendiente. Corrige el "el slice no cierra sin el spike de transporte" de ADR-005: el slice cierra con (b1); lo pendiente es solo si además tiene lanzador cómodo.

Cuarta, sobre FAIL TO START: la regla se generaliza a **allow-list** (`perfil ∉ descriptor.admissible_profiles ⇒ ABORT`), no un `if` sobre el stub, y **perfil ausente o no reconocido ⇒ producción** (fail-safe). El caso del accidente real no es "alguien declaró producción", es "nadie declaró nada" — cubierto por AT-013.b. AT-013 debe ser test **de proceso sobre el composition root real**, con evidencia externa (exit code, ausencia de readiness, hash del store inalterado, cero eventos), nunca un log del propio proceso ni un doble del composition root.

## 4. NOT_TESTED / INCONCLUSIVE

**NOT_TESTED — no se ejecutó ningún experimento; el spike fue documental por alcance:**
- Que Cowork acepte y presente una elicitation URL-mode de un servidor MCP local.
- Que Claude Code presente el diálogo tal como su documentación describe (la doc es *documented platform guarantee*; lo que haga la versión instalada sería *observed in current environment*, y no se observó nada).
- Que un hook `Elicitation` pueda auto-**aceptar**, no solo denegar.
- Si la URL de una elicitation llega al contexto del modelo (tiene peso de seguridad real).
- Comportamiento del navegador por defecto en el Windows objetivo (la máquina es SUPUESTO del proyecto, ADR-002).
- Coste real de (b1) y (c2): toda cifra de esfuerzo del documento es HIPÓTESIS, no medida.
- AT-013.k (el artefacto de distribución excluye el stub): depende de una cadena de build inexistente; no bloquea AT-013.a–d.

**INCONCLUSIVE — se buscó en fuente oficial y no se resolvió:**
- **Elicitation en Cowork**: NOT FOUND en documentación oficial. No se afirma que no lo soporte; se afirma que no se encontró. Bloquea R2 y solo R2; mitigado por la detección de capabilities por petición.
- **Esquema de `hookSpecificOutput` para que un hook `Elicitation` acepte**: el producto documenta *"auto-respond"*, la referencia de hooks documenta el camino de denegación (exit 2) y que en estos eventos *"an exit-2 hook's `hookSpecificOutput` is ignored"*; no se localizó el camino de aceptación. Impacto nulo sobre el diseño: R1/R2 asumen el peor caso.
- **Superficie equivalente a "confirm in the CLI" en Cowork** (que es *"no terminal required"*): HIPÓTESIS de que necesita una propia, no verificada. Afecta a UX de R2, no a la garantía.
- **Mecanismo de verificación de identidad** que satisfaga el MUST anti-phishing en un servidor local: la spec admite el caso y remite a *"a different mechanism"* sin prescribir ninguno ⇒ es DECISIÓN PENDIENTE (D-5, D-6), no hecho pendiente.
- **Segundo principal fuera del contexto del modelo** (credencial del SO / biométrico) desde Node LTS en Windows: POR VERIFICAR, **no se investigó**; no se afirma que exista API accesible alguna. Es el camino de evolución post-V0.

**8 decisiones abiertas para los dueños** quedan tabuladas en §12 (D-1 a D-8), siendo las de mayor consecuencia: D-1 (¿se acepta que la superficie de autorización sea producto propio, con su coste?), D-3 (¿perfil ausente ⇒ producción, aunque incomode al equipo de desarrollo? — si se rechaza, AT-013.b deja de estar cubierto) y D-4 (¿entra "el origen de la autoridad no es relajable por configuración" como PF-006? — hoy ninguna de las cinco políticas del Product Floor lo cubre).