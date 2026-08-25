# SPIKE — Transporte del canal de autorización humana

> ## NON-PRODUCTION SPIKE
>
> Este documento es un **spike**. No es normativo. No contiene código de producción.
> Todo bloque de código es **TypeScript conceptual de diseño**, escrito para fijar un contrato y
> discutirlo; no compila, no se importa y no se copia a `src/`. Regla de dependencias del
> kernel §13: **`src/` nunca importa de `experiments/`**.
>
> **Nivel documental: 6** (Discovery / research / spikes), el más bajo de la precedencia del
> kernel §14. Sus resultados son **observaciones**, jamás garantías de plataforma. Si algo aquí
> contradice un ADR Accepted o el kernel técnico v0.4, **gana el documento superior** y este se corrige.

| Campo | Valor |
|---|---|
| Spike | Autorización humana — transporte del canal de aprobación |
| Fase | TECHNICAL DESIGN V0 |
| Kernel de referencia | `docs/technical-design/v0/00-technical-kernel.md` v0.4, §3, §4, §5.2, §7, §8.3, §10 |
| ADR de referencia | ADR-005 (Accepted), §5 y "Preguntas pendientes" §2 |
| Estado | **Diseño y verificación documental completos. Verificación empírica NO ejecutada.** |
| Fecha de consulta de fuentes | 2026-08-24 |
| Autor | Technical Design |

---

## 0. Pregunta, criterios de salida y normalización de vocabulario

### 0.1 Pregunta del spike

> ¿Qué transporte puede materializar el contrato de `HumanAuthorization` del kernel §3 cumpliendo
> los tres criterios de salida?

### 0.2 Criterios de salida (propios del sistema, no de una spec)

Se enuncian como propiedades del sistema. Ninguna spec externa los define; una spec externa a lo
sumo aporta **precedente** de que son alcanzables (addendum v0.3 §B.15).

| # | Criterio |
|---|---|
| **C1** | **Consentimiento humano explícito por acto** — una decisión deliberada por cada operación sensible; nunca una habilitación general ni un consentimiento reutilizable. |
| **C2** | **Superficie de decisión no inspeccionable ni accionable por el cliente ni por el LLM** — el modelo no puede leer lo que se decide ni responder en lugar de la profesional. |
| **C3** | **Vinculación verificable** de la decisión al `item_content_hash` y al `expected_case_revision` del item revisado. |

### 0.3 Normalización de vocabulario (obligatoria, kernel §14)

Dos correcciones respecto de documentos de nivel inferior, que este spike aplica literalmente:

1. **`proposal_content_hash` → `item_content_hash`.** ADR-005 §2 y el addendum v0.3 §B.15 escriben
   `proposal_content_hash` (hash de la propuesta entera). El kernel v0.4 §3 fija **una autorización
   por item** con `item_content_hash`. El kernel tiene precedencia sobre el addendum en materia
   técnica (§14). Este spike usa `item_content_hash` en todo el texto. Consecuencia real, no
   cosmética: **el canal humano debe permitir decisión item por item**, no aprobación en bloque —
   lo que descarta cualquier transporte que solo ofrezca un sí/no único por propuesta.

2. **`actor_type = HUMAN_DECISION` → `principal_type = HUMAN` + `provenance_kind = HUMAN_DECISION`.**
   Kernel v0.4 §1.5, supersede §16.13. Los invariantes de ADR-005 que dicen
   `actor_type = HUMAN_DECISION` se leen con el par correcto.

### 0.4 Ambigüedad normativa abierta que este spike NO resuelve y debe respetar

**DECISIÓN PENDIENTE (dueños).** El significado de `expected_case_revision` difiere entre dos
documentos vigentes, y el amendment que lo resolvería **no está aprobado**:

| Modelo | Fuente | `expected_case_revision` es… |
|---|---|---|
| **A** | ADR-005 §2 y §4 (Accepted) | la revisión **resultante** del acto de revisión (`ProposalReviewed` avanza `case_revision`) |
| **B** | Kernel v0.4 §5.2 (**ADR AMENDMENT CANDIDATE**, no aplicado) | la revisión **contra la que se generó y se revisó** la propuesta (`ProposalReviewed` avanza `event_seq` pero no `case_revision`) |

**Implicación para este spike:** ninguna. **El transporte es indiferente al modelo elegido**, porque
—como se demuestra en §2.2— el transporte nunca transporta la revisión: la escribe el Core. Se
registra aquí solo para que la implementación del port no congele accidentalmente uno de los dos
modelos, y para que el test AT-013 no dependa de cuál se apruebe.

---

## 1. Método y fuentes

### 1.1 Método

1. Lectura del kernel técnico v0.4 y de ADR-005 como contrato a satisfacer.
2. Verificación de la spec MCP **contra la documentación oficial primaria**
   (`modelcontextprotocol.io`), revisión vigente, con extracción literal de los MUST/SHOULD.
3. Verificación del soporte del runtime **contra la documentación oficial primaria del producto**
   (`code.claude.com/docs`, `support.claude.com`).
4. Evaluación de los tres candidatos criterio por criterio.
5. Diseño del port, del stub y del mecanismo FAIL TO START.

**No se ejecutó ningún experimento.** No se levantó ningún servidor MCP, no se instrumentó ningún
cliente, no se midió nada. Todo lo que sigue es **verificación documental y razonamiento de
diseño**. Ver §13 para el detalle de qué queda `NOT_TESTED` y por qué.

### 1.2 Fuentes consultadas y su autoridad

| Fuente | URL | Autoridad | Uso |
|---|---|---|---|
| MCP — Elicitation, rev. 2026-07-28 | `modelcontextprotocol.io/specification/2026-07-28/client/elicitation` | **Oficial primaria** (spec) | MUSTs de form y URL mode |
| MCP — Versioning | `modelcontextprotocol.io/specification/versioning` | **Oficial primaria** (spec) | Confirmar revisión vigente |
| Claude Code — Connect to tools via MCP | `code.claude.com/docs/en/mcp` | **Oficial primaria** (producto) | Soporte de elicitation en el runtime |
| Claude Code — Hooks reference | `code.claude.com/docs/en/hooks` | **Oficial primaria** (producto) | Hooks `Elicitation` / `ElicitationResult` |
| Cowork — Get started | `support.claude.com/en/articles/13345190-...` | **Oficial primaria** (producto) | Verificado previamente en `notes/research-v0_1/verif-cowork.md` |

**Blogs de terceros: ninguno citado.** No se usó ninguna fuente no autoritativa en este spike.

---

## 2. Hallazgo estructural previo a la comparación

Antes de comparar candidatos hay que decir **qué parte del criterio puede decidir un transporte**.
Sin esto, la comparación mide lo que no debe.

### 2.1 C3 no discrimina transportes; discrimina diseños

**HECHO VERIFICADO (kernel §3.3, ratificado por los dueños §28):** la autorización **no viaja al
modelo**; `commit_reviewed_facts(proposal_id, item_ids[])` no recibe ningún secreto y el Core
resuelve internamente si existe autorización válida.

De ahí se sigue que **C3 lo satisface el Core, no el transporte**, en los tres candidatos:

- El Core es quien conoce `item_content_hash` (lo calculó al crear el `ProposalItem`).
- El Core es quien conoce `case.current_revision`.
- El Core es quien construye la `HumanAuthorization` y quien la verifica en el commit (kernel §2.3).

El transporte solo debe cumplir **dos condiciones negativas**:

- **N1 — El transporte no transporta contenido vinculante.** Ni el hash ni la revisión son
  parámetros del canal. El canal lleva una **referencia opaca** (`pending_review_id`,
  `proposal_item_id`), nunca valores que el Core deba creerse.
- **N2 — El transporte no permite elegir a qué item se aplica una decisión tomada sobre otro.**
  La decisión debe llegar ligada a la referencia opaca que el Core emitió, no a un índice ni a un
  nombre reconstruible.

**Conclusión:** cualquiera de los tres candidatos cumple C3 **si y solo si se diseña así**. C3 es
un criterio de **disciplina de contrato**, y su incumplimiento sería un error de diseño nuestro, no
una carencia de la plataforma. La comparación real se juega en **C1 y C2**.

### 2.2 En URL mode, la decisión NO viaja por la elicitation

**HECHO VERIFICADO** (spec 2026-07-28, Elicitation, sección "URL Mode Elicitation Requests"), cita
literal:

> "The response with `action: "accept"` indicates that the user has consented to the interaction.
> It does not mean that the interaction is complete. The interaction occurs out of band and the
> client is not directly informed of the outcome."

Esto es **el hallazgo central del spike**, y cambia la naturaleza de la comparación:

- En **URL mode**, la elicitation transporta **un puntero (`url`) y un consentimiento para abrirlo**.
  La decisión de la profesional ocurre **fuera de banda**, contra una superficie servida por el
  propio servidor MCP —es decir, por **nuestro Core**—, y llega al Core por un camino que no es MCP.
- Por tanto, **la superficie de autorización del candidato (a) es exactamente el candidato (b)**.
  URL mode no es una alternativa a la UI local: es **la UI local más un mecanismo de lanzamiento**.

**Implicación arquitectónica inmediata:** (a) y (b) no compiten. **(b) es el sustrato; (a) es un
lanzador opcional que se apoya en (b).** Elegir (a) *sin* construir (b) es imposible: no hay a qué
apuntar la URL. Esto reordena por completo el cálculo de coste (§6).

---

## 3. Candidato (a) — MCP elicitation, modo URL

### 3.1 Estado de la spec (verificado hoy contra fuente oficial primaria)

**HECHO VERIFICADO** — Revisión vigente: **2026-07-28**. Cita literal
(`/specification/versioning`): *"The **current** protocol version is **2026-07-28**"*.

**HECHO VERIFICADO** — URL mode sigue marcado como característica nueva y potencialmente
inestable. Cita literal:

> "**New feature:** URL mode elicitation is introduced in the `2025-11-25` version of the MCP
> specification. Its design and implementation may change in future protocol revisions."

**RIESGO** derivado: construir la garantía nuclear del producto sobre una característica que la
propia spec declara sujeta a cambio. Mitigado si (a) es lanzador y no sustrato (§2.2).

**HECHO VERIFICADO** — Mecanismo de transporte en 2026-07-28: la elicitation ya no es una petición
server→client independiente, sino que viaja dentro de un `InputRequiredResult` (patrón Multi
Round-Trip Requests) y el cliente **reintenta la petición original** con `inputResponses`. Cita
literal: *"Servers **MAY** request information from a user during the processing of a client
request, by sending an `InputRequiredResult` containing an `elicitation/create` request."*

### 3.2 Qué MUSTs impone al cliente (extracto literal)

**HECHO VERIFICADO** — Sección "Safe URL Handling". Los clientes que implementan URL mode:

> 1. **MUST NOT** automatically pre-fetch the URL or any of its metadata.
> 2. **MUST NOT** open the URL without explicit consent from the user.
> 3. **MUST** show the full URL to the user for examination before consent.
> 4. **MUST** open the URL provided by the server in a secure manner that does not enable the
>    client or LLM to inspect the content or user inputs.

Y en el bloque de advertencia general, para los clientes MCP:

> * Provide UI that makes it clear which server is requesting information
> * Respect user privacy and provide clear decline and cancel options
> * For URL mode, clearly display the target domain/host and gather user consent before navigation
>   to the target URL

**HECHO VERIFICADO** — Definición de los dos modos, cita literal:

> * `"form"`: In-band structured data collection with optional schema validation. **Data is exposed
>   to the client.**
> * `"url"`: Out-of-band interaction via URL navigation. **Data (other than the URL itself) is
>   *not* exposed to the client.**

### 3.3 Qué NO garantiza

**HECHO VERIFICADO** — La spec no impone ningún modelo de interacción. Cita literal:

> "Implementations are free to expose elicitation through any interface pattern that suits their
> needs—the protocol itself does not mandate any specific user interaction model."

**HECHO VERIFICADO** — Los controles de aprobación de usuario son **SHOULD, no MUST**. Cita literal
(Security Considerations): *"Clients **SHOULD** implement user approval controls"*.

**NOT FOUND** — La spec **no dice en ninguna parte** que la cadena de texto de la `url` quede fuera
del contexto del LLM. El MUST 4 protege *el contenido de la página y las entradas del usuario*, no
la URL misma; y el MUST 3 obliga a mostrarla al usuario. **RIESGO derivado, con peso real:** si el
runtime coloca la URL en el contexto del modelo y el modelo dispone de ejecución local (lo dispone,
§7), el modelo puede abrir esa URL. Consecuencia de diseño obligatoria: **abrir la URL no puede
autorizar nada** (§4.3, D-4).

**HECHO VERIFICADO** — Restricciones sobre lo que el servidor puede poner en la URL:

> 1. **MUST NOT** include sensitive information about the end-user, including credentials,
>    personally identifiable information, etc., in the URL […]
> 2. **MUST NOT** provide a URL which is pre-authenticated to access a protected resource, as the
>    URL could be used to impersonate the user by a malicious client.

El punto 2 **prohíbe explícitamente** el atajo tentador de que la URL misma sea la autorización.
Coincide con la conclusión anterior por un camino independiente.

**HECHO VERIFICADO** — Obligación de verificar identidad, sección "Phishing":

> "The MCP Server **MUST** verify the identity of the user who opens the URL before accepting
> information."

**SUPUESTO / POR VERIFICAR:** el mecanismo canónico que la spec sugiere (cookie de sesión + `sub`
del authorization server MCP) presupone un servidor accesible por web con OAuth. **Nuestro Legal MCP
es un servidor local para una única profesional en una única máquina** (ADR-002). La propia spec
admite ese caso: *"In other cases, the server may not be accessible via the web and may not be able
to use a session cookie to identify the user. In this case, the server must use a different
mechanism"*. Qué mecanismo concreto usamos es **DECISIÓN PENDIENTE** (§12, D-5) y su fuerza real
está acotada por §7.

### 3.4 Comparación con form mode — por qué form mode está descartado

| Propiedad | form mode | URL mode |
|---|---|---|
| ¿Los datos de la decisión pasan por el cliente? | **Sí** — "Data is exposed to the client" (literal) | **No** — "Data […] is *not* exposed to the client" (literal) |
| ¿Garantía de que la respuesta la produjo un humano? | **No.** Aprobación de usuario es SHOULD | Consentimiento de apertura es MUST; la decisión ni siquiera viaja |
| ¿Admitido por la spec para información sensible? | **Prohibido** — "Servers **MUST NOT** use form mode elicitation to request sensitive information" | **Obligatorio** para ese caso — "Servers **MUST** use URL mode" |
| Veredicto contra C2 | **FALLA** | Ver §3.5 |

**Decisión: form mode RECHAZADO como canal de autorización.** Confirma —con la spec vigente
2026-07-28, no con la de 2025-06-18 sobre la que se escribió ADR-005— la alternativa 4 ya rechazada
en ADR-005. El rechazo se refuerza con §3.6.

### 3.5 Evaluación criterio por criterio

| Criterio | Veredicto | Fundamento |
|---|---|---|
| **C1** — consentimiento humano por acto | **PARCIAL, y no por sí mismo** | El MUST "no abrir sin consentimiento explícito" es consentimiento **para abrir una URL**, no para autorizar un commit. El consentimiento *del acto sensible* lo produce la página, que es (b). Además, **§3.6 documenta un mecanismo oficial del runtime que puede suprimir el diálogo.** |
| **C2** — no inspeccionable ni accionable | **CUMPLE por delegación, no estructuralmente** | El MUST 4 es fuerte y literal, pero **lo cumple el cliente, no nosotros**. Es una *documented platform guarantee* sobre el comportamiento de terceros, no una propiedad de nuestro sistema. No podemos verificarla en runtime. |
| **C3** — vinculación verificable | **CUMPLE si se respeta N1/N2** | Igual que los otros dos candidatos (§2.1). |

### 3.6 HALLAZGO CRÍTICO — el runtime documenta un mecanismo oficial para auto-responder elicitations

**HECHO VERIFICADO** (documentación oficial primaria de producto, `code.claude.com/docs/en/mcp`),
cita literal:

> "MCP servers can request structured input from you mid-task using elicitation. When a server
> needs information it can't get on its own, Claude Code displays an interactive dialog and passes
> your response back to the server. No configuration is required on your side: elicitation dialogs
> appear automatically when a server requests them."
>
> * "**Form mode**: Claude Code shows a dialog with form fields defined by the server […]"
> * "**URL mode**: Claude Code opens a browser URL for authentication or approval. Complete the flow
>   in the browser, then confirm in the CLI."
>
> "**To auto-respond to elicitation requests without showing a dialog, use the `Elicitation` hook.**"

**HECHO VERIFICADO** (`code.claude.com/docs/en/hooks`), filas literales de las tablas:

| Evento | Cuándo dispara |
|---|---|
| `Elicitation` | "When an MCP server requests user input during a tool call" |
| `ElicitationResult` | "After a user responds to an MCP elicitation, before the response is sent back to the server" |

| Evento | ¿Puede bloquear? | Qué ocurre en exit 2 |
|---|---|---|
| `Elicitation` | Sí | "Denies the elicitation" |
| `ElicitationResult` | Sí | "Blocks the response (action becomes decline)" |

**Lo que esto significa, con precisión y sin exagerar:**

- **HECHO VERIFICADO:** existe un mecanismo de configuración **documentado y soportado** para
  **auto-responder elicitations sin mostrar diálogo**. La frase del producto dice *"auto-respond"*,
  no *"auto-deny"*.
- **POR VERIFICAR / INCONCLUSIVE:** el esquema exacto de `hookSpecificOutput` mediante el cual un
  hook `Elicitation` fabrica una respuesta **de aceptación**. La documentación consultada detalla la
  dirección de denegación (exit 2) y advierte que *"On `Elicitation` and `ElicitationResult`, an
  exit-2 hook's `hookSpecificOutput` is ignored"*, pero **no se localizó** el esquema del camino de
  aceptación. **No se afirma que exista; se afirma que el producto documenta "auto-respond" y que el
  camino de aceptación no pudo verificarse ni descartarse.**
- **Postura de diseño obligada:** hay que diseñar **como si un hook pudiera fabricar un
  `action: "accept"`**, porque el coste de equivocarse en esa dirección es una autorización falsa en
  un expediente jurídico, y el coste de equivocarse en la contraria es una defensa redundante.

**Consecuencia decisiva, y es una buena noticia para URL mode:** aun suponiendo el peor caso —un
hook que auto-acepta—, en **URL mode** ese `accept` significa únicamente *"consiento en abrir la
URL"*. **No completa nada** (§2.2, cita literal). El hook podría abrir la página; nadie la
rellenaría; el Core no registraría ninguna decisión; `commit_reviewed_facts` seguiría emitiendo
`HUMAN_REVIEW_REQUIRED`. **El sistema falla cerrado.**

En **form mode**, el mismo hook auto-aceptando **sí fabricaría la decisión**, porque en form mode la
decisión *es* el contenido de la respuesta. Esto eleva el rechazo de form mode de "la spec no lo
garantiza" (argumento de ADR-005) a **"el runtime documenta el mecanismo que lo rompe"**. Es un
argumento más fuerte y de naturaleza distinta: no es una laguna, es una capacidad.

### 3.7 HALLAZGO — la elicitation solo puede nacer dentro de una tool call del modelo

**HECHO VERIFICADO** (spec, "User Interaction Model" y "Protocol Messages"): la elicitation ocurre
*"nested inside other MCP server features"* y se emite *"during the processing of a client
request"*. **HECHO VERIFICADO** (hooks del runtime): `Elicitation` dispara *"When an MCP server
requests user input **during a tool call**"*.

**Implicación arquitectónica, en tensión directa con ADR-005:** si el canal de revisión es URL-mode
elicitation, entonces **la revisión humana solo puede ofrecerse mientras hay una tool call del
modelo en vuelo**. Es decir: **el modelo controla *cuándo* se le ofrece revisar a la profesional.**

Kernel §7 dice literalmente que `ReviewProposal` entra por *"canal humano, no MCP"*, y que eso *"es
la materialización de que la revisión humana no pasa por el modelo"*. Un canal que solo se abre
cuando el modelo invoca una tool **contradice esa materialización en el eje temporal**, aunque la
respete en el eje del contenido.

Grado real del problema, sin dramatizar:

- El modelo **no puede falsificar** la decisión (§3.6). El fallo es cerrado.
- El modelo **sí puede no ofrecerla nunca** ⇒ no hay commit ⇒ **fallo cerrado, aceptable**.
- El modelo **sí puede elegir el momento** ⇒ superficie de manipulación de la atención de la
  profesional (ofrecer la revisión sepultada tras una explicación larga y convincente). Es
  exactamente el vector de la **fatiga de revisión** que ADR-005 ya registra como su RIESGO
  principal, ahora con un actor que puede optimizarlo.
- Con una UI local (b), la profesional **abre la revisión cuando quiere**, sin que el modelo
  intervenga. Propiedad estrictamente superior en términos de autoridad.

### 3.8 POR VERIFICAR — soporte en Cowork

- **HECHO VERIFICADO** (`support.claude.com`, verificado en `notes/research-v0_1/verif-cowork.md`):
  Cowork *"uses the same agentic architecture that powers Claude Code, with no terminal required"* y
  soporta conectores MCP con modos de aprobación.
- **POR VERIFICAR — NO se localizó documentación oficial que afirme que Cowork soporta MCP
  elicitation, ni en form mode ni en URL mode.** La arquitectura compartida con Claude Code es un
  indicio, **no una garantía de plataforma**: "misma arquitectura agentic" no es "misma superficie de
  cliente MCP", y la superficie de cliente es precisamente donde vive elicitation.
- **HIPÓTESIS (explícitamente marcada como tal):** dado que Cowork es *"no terminal required"*, la
  instrucción documentada de Claude Code para URL mode —*"Complete the flow in the browser, then
  confirm in the CLI"*— **no puede aplicarse literalmente en Cowork**: no hay CLI donde confirmar.
  Cowork necesitaría una superficie propia equivalente. Si existe o no es POR VERIFICAR.
- **HECHO VERIFICADO (spec) — y este es el punto operativamente útil:** el soporte es
  **detectable en runtime**. Cita literal:

  > "Clients that support elicitation **MUST** declare the `elicitation` capability in
  > `_meta.io.modelcontextprotocol/clientCapabilities` **on each request**"
  >
  > "For backwards compatibility, an empty capabilities object is equivalent to declaring support
  > for `form` mode only"
  >
  > "Servers **MUST NOT** send elicitation requests with modes that are not supported by the client."

  Es decir: el Core puede leer, **en cada petición**, si el cliente declara `url`. Si no lo declara,
  el Core **tiene prohibido** enviar URL mode y debe degradar al canal propio. **Esto convierte una
  incertidumbre de plataforma en una rama de código determinista**, y es el argumento que permite
  adoptar (a) sin apostar por ella.

### 3.9 Coste de construcción y riesgo residual

**Coste (HIPÓTESIS de esfuerzo, no medida):** **bajo, condicionado a que (b) exista.** Emitir un
`InputRequiredResult` con `mode: "url"`, gestionar `requestState` y el reintento MRTR, y leer las
capabilities por petición. Si (b) no existe, el coste es (b) entero más esto.

**Riesgo residual:**

- **RIESGO** — La garantía C2 la cumple **un tercero**, y no es verificable por nosotros en runtime.
- **RIESGO** — URL mode declarado por la spec como sujeto a cambio.
- **RIESGO** — El modelo controla el momento de la oferta de revisión (§3.7).
- **RIESGO** — La URL puede llegar al contexto del modelo (§3.3, NOT FOUND).
- **POR VERIFICAR** — Soporte en Cowork (§3.8).

---

## 4. Candidato (b) — UI local mínima propia del producto

Dos sub-variantes, con propiedades distintas y que conviene no confundir:

- **(b1) Página local servida por el Core** sobre loopback, abierta en el navegador del sistema.
- **(b2) Ventana nativa** de un proceso propio, comunicada con el Core por IPC local.

### 4.1 Evaluación criterio por criterio

| Criterio | Veredicto | Fundamento |
|---|---|---|
| **C1** | **CUMPLE, y es el único que lo cumple estructuralmente** | La superficie la diseñamos nosotros: un acto por item, sin "aprobar todo", sin recordar la decisión, sin valor por defecto en el control de aprobación. C1 deja de depender de un tercero y pasa a ser una **decisión de producto verificable en nuestro propio test**. |
| **C2** | **CUMPLE estructuralmente hasta el límite del §7** | La superficie **no está en el canal MCP en absoluto**. No hay nada que el cliente deba honrar, porque el cliente no participa. No hay hook que interceptar, porque no hay elicitation. La no-inspeccionabilidad no se delega: se obtiene por construcción. |
| **C3** | **CUMPLE si se respeta N1/N2** | Igual que los demás (§2.1). |

### 4.2 La propiedad que solo (b) tiene

**(b) es el único candidato en el que la profesional puede iniciar la revisión sin el modelo.**
Abre la ventana, ve las propuestas pendientes (kernel §9, scope `pending`), decide item por item. El
modelo no sabe cuándo ocurre, no puede provocarlo ni retrasarlo, y no participa en el ciclo. Esa es
la lectura literal de kernel §7: *"la revisión humana no pasa por el modelo"* — en contenido **y en
tiempo**.

### 4.3 Decisiones de diseño obligatorias (no negociables si se elige b1)

| Id | Decisión | Razón |
|---|---|---|
| **D-1** | El `pending_review_id` **nunca aparece en ningún resultado de tool MCP, ni en ningún archivo bajo una ruta que el runtime pueda leer.** | Si el modelo lo ve, puede navegarlo (§7). |
| **D-2** | La **URL/página de revisión no aparece nunca en un resultado de tool.** Solo en el campo `url` de una elicitation URL-mode, o en la ventana propia. | Refuerza D-1 y coincide con el SHOULD NOT de la spec sobre URLs clicables en campos de form. |
| **D-3** | **`GET` es puramente de lectura.** Abrir la página no aprueba, no reserva, no consume, no muta. | La spec **prohíbe** URLs pre-autenticadas (§3.3, MUST NOT 2), y §3.6 obliga a asumir apertura automática. |
| **D-4** | La aprobación exige un **`POST` con un valor de un solo uso que solo aparece renderizado en la superficie humana** y que **jamás se escribe en disco, ni en logs, ni en el `Tool Invocation Log`**. | Eleva el coste de una aprobación fabricada de "una petición" a "leer la superficie renderizada". Ver §7 sobre hasta dónde llega esto. |
| **D-5** | El listener liga **exclusivamente a loopback**, con puerto efímero, y **rechaza toda petición con `Origin`/`Referer` presente** (una página web no debe poder postear contra él). | Reduce la superficie a procesos locales. |
| **D-6** | Una aprobación que llegue **sin un evento previo de render de la superficie humana** para ese `pending_review_id` se **rechaza** y se registra como anomalía. | Detección, no prevención. Coherente con "tamper-evident, no tamper-proof" (kernel §8.3). |
| **D-7** | La sesión de revisión **expira** y su expiración es independiente de `expires_at` de la autorización (más corta). | Cierra la ventana en que el `pending_review_id` es útil. |

### 4.4 Coste de construcción

**HIPÓTESIS de esfuerzo (no medida, sin base empírica):**

| Variante | Coste relativo | Comentario |
|---|---|---|
| **(b1) página local** | **Medio-bajo** | Servidor HTTP de loopback + una vista de lista con decisión por item. Sin framework, sin build de frontend, sin dependencias de UI. Reutiliza el scope `pending` que el kernel §9 ya exige construir. |
| **(b2) ventana nativa** | **Alto** | Introduce una dependencia de UI de escritorio, empaquetado, actualización y superficie de seguridad propia. **No se justifica en v0.** |

**Observación de coste que cambia el cálculo:** la vista de revisión **no es trabajo adicional**. El
kernel §9 ya obliga a un scope `pending` que "hace visibles las Proposals pendientes y las
condiciones activas" (ADR-005, relación con ADR-004). (b1) es esa vista, con controles de decisión.

### 4.5 Riesgo residual

- **RIESGO** — Loopback es alcanzable por cualquier proceso del mismo usuario del SO, **incluido el
  runtime del modelo**. Este es el límite duro; se trata en §7, no se disimula aquí.
- **RIESGO** — UX de conmutación de ventana: la profesional debe salir del chat. Es coste de
  atención real; en parte **es la fricción deseada** (ADR-005: *"la fricción es requisito, no defecto
  de UX"*), pero puede degenerar en no revisar nunca.
- **POR VERIFICAR** — Comportamiento de apertura del navegador por defecto en el Windows de la
  usuaria objetivo. La edición concreta de Windows es **SUPUESTO** del proyecto (ADR-002).
- **DECISIÓN PENDIENTE** — Si (b1) se abre sola o solo bajo acción de la profesional.

---

## 5. Candidato (c) — CLI

El encargo dice "CLI del runtime". Hay **dos lecturas materialmente distintas** y conviene separarlas,
porque una está descartada y la otra no.

### 5.1 (c1) La CLI/TUI del propio runtime como superficie de decisión

Es decir: la profesional decide en el diálogo que Claude Code renderiza en su terminal.

| Criterio | Veredicto |
|---|---|
| **C1** | **FALLA.** El diálogo lo renderiza el cliente y **§3.6 documenta el mecanismo oficial para suprimirlo** (`Elicitation` hook, "auto-respond […] without showing a dialog"). Un consentimiento suprimible por configuración no es consentimiento explícito por acto. |
| **C2** | **FALLA.** La superficie vive **dentro del proceso que hospeda al LLM**. Es la definición literal de "inspeccionable y accionable por el cliente". |
| **C3** | Cumpliría si N1/N2, pero es irrelevante habiendo fallado C1 y C2. |

**HECHO VERIFICADO adicional que lo cierra:** Cowork es *"no terminal required"*
(`support.claude.com`). **El canal no existe en el host previsto.** Diseñar la garantía nuclear del
producto sobre una superficie ausente del host objetivo no es una opción.

**Veredicto: (c1) RECHAZADO.**

### 5.2 (c2) Una CLI propia del Core, ejecutada por la profesional en su propia terminal

Es decir: un binario nuestro, `legal-os review --case …`, que la profesional lanza ella.

| Criterio | Veredicto | Fundamento |
|---|---|---|
| **C1** | **CUMPLE** | Un acto por item, en un proceso que ella arrancó. |
| **C2** | **CUMPLE hasta el límite del §7** | Igual que (b): la superficie está fuera del canal MCP por construcción. |
| **C3** | **CUMPLE si N1/N2** | Igual que los demás. |

**Coste: bajo** (el más bajo de los tres, si el Core ya expone sus casos de uso internamente).

**Riesgo residual y por qué no es la recomendación principal:**

- **RIESGO — Idoneidad para la usuaria.** El sistema se diseña para una abogada, no para una
  ingeniera. Una superficie de terminal para el acto jurídicamente más significativo del producto es
  una decisión de producto discutible, y la **fatiga de revisión** (ADR-005) empeora cuando el acto
  es incómodo: la aprobación en bloque para "quitárselo de encima" se vuelve más tentadora.
- **RIESGO — Sin descubrimiento.** Nada le indica que hay algo que revisar. Depende de que recuerde
  ejecutarlo.
- **HECHO VERIFICADO — Riesgo específico del host, no menor:** en Claude Code el modelo **ejecuta
  comandos locales**. Una CLI de aprobación es, por construcción, invocable por el modelo. Mitigable
  solo por D-4 (valor que no está en disco) — el mismo límite del §7, pero con una superficie de
  ataque más cómoda para el atacante, porque el "ataque" es literalmente ejecutar nuestro binario.

**Veredicto: (c2) admisible como *fallback* y como canal de test; no como UX primaria.** Su valor
principal es **habilitar entornos headless y los tests de aceptación**, que es mucho.

---

## 6. Tabla comparativa

| | **(a) elicitation URL mode** | **(b1) página local del Core** | **(c1) CLI del runtime** | **(c2) CLI propia** |
|---|---|---|---|---|
| **C1** consentimiento por acto | Parcial — consiente *abrir*, no *aprobar*; diálogo suprimible por hook | **Cumple, estructural** | **Falla** | Cumple |
| **C2** no inspeccionable/accionable | Cumple **por delegación** en un MUST de terceros | **Cumple, estructural** (hasta §7) | **Falla** | Cumple (hasta §7) |
| **C3** vinculación verificable | Cumple si N1/N2 | Cumple si N1/N2 | — | Cumple si N1/N2 |
| **¿La decisión pasa por el canal del modelo?** | **No** (out of band, literal) | **No** (no hay canal) | **Sí** | **No** |
| **¿Quién inicia la revisión?** | El modelo (§3.7) | **La profesional** | El modelo | La profesional |
| **¿Existe en Cowork?** | **POR VERIFICAR** | Sí (es nuestro) | **No** ("no terminal required") | Sí (es nuestro) |
| **¿Detectable en runtime?** | **Sí**, capabilities por petición | N/A | N/A | N/A |
| **Coste** | Bajo **si (b1) existe**; si no, (b1)+esto | Medio-bajo (reusa scope `pending`) | — | Bajo |
| **Veredicto** | **Lanzador opcional** | **Sustrato normativo** | **RECHAZADO** | **Fallback + canal de test** |

---

## 7. El límite duro, dicho por escrito: la frontera del usuario del SO

Este apartado existe porque **omitirlo convertiría todo lo anterior en una garantía falsa**.

**HECHO VERIFICADO:** en el host previsto, el modelo dispone de ejecución local (Claude Code ejecuta
comandos; Cowork tiene acceso directo a archivos locales en Desktop —
`support.claude.com/en/articles/13345190`). El modelo **no es un cliente remoto**: es un proceso que
corre como **el mismo usuario del sistema operativo** que la profesional.

**Consecuencia, enunciada sin adornos:**

> **Dentro de una única cuenta de usuario del SO, ningún transporte local ofrece una frontera dura
> "solo el humano puede accionar esto".** Loopback, named pipes, sockets, archivos: todo es
> alcanzable por cualquier proceso de ese usuario. Lo que se obtiene no es imposibilidad, sino
> **coste elevado, no accidentalidad y detectabilidad**.

Esto es **coherente con el threat model ya declarado** en kernel §8.3 (*"tamper-evident, no
tamper-proof"*; el actor local con control total está **fuera del threat model V0**) y con ADR-005
(*"no resiste a un actor local con control total de la máquina"*). Este spike no lo empeora: lo
**localiza** en el canal de autorización, que es donde más duele.

**Matiz que sí es nuevo y que los dueños deben ver.** El threat model V0 excluye "usuaria hostil".
Pero el riesgo realista aquí **no es una usuaria hostil**, sino tres cosas distintas:

1. **El atajo plausible.** Un modelo que "ayuda" completando un paso que percibe como trámite.
2. **La inyección de prompt desde la evidencia ingerida.** Este producto ingiere, por diseño,
   documentos de la contraparte: correos, oficios, contratos. **Material adversarial es la materia
   prima del dominio.** Un documento que contenga instrucciones dirigidas al modelo es un vector
   ordinario, no exótico. Esta es la razón por la que C2 pesa más en este producto que en uno genérico.
3. **La configuración bienintencionada.** Un hook `Elicitation` puesto para reducir fricción en otro
   flujo (§3.6).

Contra los tres, la defensa que funciona es la misma: **que la decisión no sea producible por el
canal del modelo aunque el modelo lo intente** (D-3, D-4), y **que un intento quede registrado**
(D-6).

**Camino de evolución (señalado, NO diseñado aquí):** un segundo principal fuera del contexto del
modelo — prompt de credenciales del SO, biométrico de plataforma, o un dispositivo aparte. **POR
VERIFICAR:** disponibilidad y forma de acceso desde Node LTS en el Windows objetivo. **No se afirma
que exista una API accesible.** Post-V0 (kernel §15).

---

## 8. Diseño del port `HumanAuthorizationProvider` y del stub

### 8.1 Reconciliación previa con ADR-005 (PROPUESTA DEL TECHNICAL DESIGN, requiere ratificación)

Hay una tensión de forma —no de fondo— entre dos documentos vigentes:

- **ADR-005 §5** y **kernel §7** describen el canal humano como un **driving adapter**: algo que
  *entra* invocando `ReviewProposal`.
- **Kernel §4** describe un **`HumanAuthorizationProvider` que se "resuelve"** y cuya resolución se
  comprueba **al arrancar** — vocabulario de **puerto driven** inyectado en el composition root.

**PROPUESTA:** ambas cosas son ciertas de partes distintas, y el port las concilia sin contradecir
ninguna:

- El **puerto** `HumanAuthorizationProvider` es **driven**: Application lo invoca para *solicitar*
  que se abra una sesión de revisión y para *obtener* sus decisiones. Es el seam donde el stub
  sustituye, y por eso es comprobable al arranque.
- El **adapter que lo implementa** contiene su propio borde de entrada (el handler HTTP de la página,
  la CLI, el callback de la elicitation). Ese borde **no es visible para Application** y no se expone
  como puerto.
- `ReviewProposal` sigue siendo un use case de Application que **no está en la superficie MCP**.

**POR RATIFICAR (dueños):** que esta lectura es un refinamiento de ADR-005 §5 y no un cambio de
decisión. No altera quién autoriza, ni con qué fuerza, ni por dónde.

### 8.2 Regla de diseño que hace al port seguro por construcción

> **El provider NUNCA construye una `HumanAuthorization`.** Devuelve **decisiones**; el
> **Application** construye la autorización, leyendo `item_content_hash` y `expected_case_revision`
> **de su propio estado**, nunca de lo que devuelve el provider.

Por qué importa, y por qué es la decisión más importante de esta sección: **acota lo que un provider
comprometido, defectuoso o stub puede hacer.** Lo peor que puede hacer es **mentir sobre que hubo un
humano**. **No puede** mentir sobre qué contenido se aprobó ni sobre qué revisión estaba vigente,
porque no toca esos campos. C3 queda **fuera del alcance de cualquier provider**, que es
exactamente donde debe estar (§2.1).

Corolario sobre la marca: **`authorization_source` no lo aporta el provider en cada llamada.** Lo
estampa Application a partir del **descriptor estático del provider resuelto** en el composition
root. Un provider **no puede declararse `REAL`**: no participa en esa decisión. Es la diferencia
entre "el stub debe acordarse de marcarse" (frágil) y "el stub no puede dejar de estar marcado"
(kernel §4, *"marca indeleble"*).

### 8.3 Interfaz conceptual del port

```ts
// ─────────────────────────────────────────────────────────────────────────────
// NON-PRODUCTION SPIKE — TypeScript CONCEPTUAL. No compila. No se importa.
// Vive en experiments/. Regla del kernel §13: src/ nunca importa de experiments/.
// Propósito: fijar la FORMA del contrato para discutirla, no la implementación.
// ─────────────────────────────────────────────────────────────────────────────

/** Kernel §3. Estampado por Application desde el descriptor del provider, NUNCA por el provider. */
type AuthorizationSource = 'REAL' | 'DEV_STUB';

/** Kernel §2.2. Dimensión de decisión; ortogonal a commit_state. */
type ReviewDecision = 'PENDING' | 'APPROVED' | 'REJECTED';

/**
 * Lo que Application PIDE al provider.
 * Contiene SOLO referencias opacas y material presentable.
 * No contiene item_content_hash ni expected_case_revision: el canal no los transporta (N1).
 */
interface ReviewSessionRequest {
  readonly review_session_id: string;   // UUIDv7, kernel §11 — PROPUESTA, sujeta a spike de deps
  readonly case_id: string;
  readonly proposal_id: string;
  /** Un elemento por item. La decisión es POR ITEM (kernel §3.2) — no hay aprobación en bloque. */
  readonly items: ReadonlyArray<{
    readonly proposal_item_id: string;  // identidad opaca y estable, NUNCA índice posicional
    readonly presentation: ItemPresentation; // texto ya renderizado para la humana
  }>;
  /** Ventana de la SESIÓN, más corta que expires_at de la autorización (D-7). */
  readonly session_expires_at: string;
}

/** Proyección de presentación. Deliberadamente sin hashes: kernel §11 — un hash nunca se muestra. */
interface ItemPresentation {
  readonly headline: string;
  readonly body: string;
  readonly supporting_evidence_refs: ReadonlyArray<string>;
  readonly uncertainty_notes: ReadonlyArray<string>;
}

/**
 * Lo que el provider DEVUELVE. Nótese lo que NO está aquí:
 * ni item_content_hash, ni expected_case_revision, ni authorization_source, ni authorization_id.
 * El provider no puede influir en la vinculación (C3) ni en la marca de origen.
 */
interface ItemDecision {
  readonly proposal_item_id: string;
  readonly decision: ReviewDecision;
  readonly note?: string;
  readonly decided_at: string;
}

interface ReviewSessionOutcome {
  readonly review_session_id: string;
  /** principal_type = HUMAN (kernel §1.4, regla dura). Quién lo determina: ver POR VERIFICAR §12 D-6. */
  readonly principal_id: string;
  readonly decisions: ReadonlyArray<ItemDecision>;
  readonly completed: boolean;   // false = expiró o se abandonó sin decidir todo
}

/** Capacidades declaradas por el adapter; permiten a Application degradar de forma determinista. */
interface ProviderCapabilities {
  /** ¿La profesional puede iniciar la revisión sin el modelo? (b) y (c2) = true; (a) = false (§3.7). */
  readonly human_initiated: boolean;
  /** ¿Requiere una tool call en vuelo para poder ofrecer la revisión? (a) = true. */
  readonly requires_inflight_tool_call: boolean;
}

/**
 * EL PORT. Driven. Lo resuelve el composition root. Es el seam del FAIL TO START (§9).
 * Application depende de esta interfaz; jamás de un transporte.
 */
interface HumanAuthorizationProvider {
  readonly provider_id: string;
  capabilities(): ProviderCapabilities;
  openReviewSession(request: ReviewSessionRequest): Promise<void>;
  awaitOutcome(review_session_id: string, signal: AbortSignal): Promise<ReviewSessionOutcome>;
  cancelReviewSession(review_session_id: string, reason: string): Promise<void>;
}

/**
 * Descriptor ESTÁTICO. Vive en el registro del composition root, NO en el provider.
 * De aquí sale authorization_source. Un provider no puede escribir su propio descriptor.
 */
interface ProviderDescriptor {
  readonly provider_id: string;
  readonly source: AuthorizationSource;
  /** Perfiles en los que este provider puede resolverse. El stub NO incluye 'production'. */
  readonly admissible_profiles: ReadonlyArray<DeploymentProfile>;
  readonly factory: () => HumanAuthorizationProvider;
}
```

### 8.4 Implementación stub para DEV/TEST

```ts
// ─────────────────────────────────────────────────────────────────────────────
// NON-PRODUCTION SPIKE — stub conceptual para DEV/TEST. Kernel §4.
// ─────────────────────────────────────────────────────────────────────────────

type StubScript =
  | { readonly kind: 'APPROVE_ALL' }
  | { readonly kind: 'REJECT_ALL' }
  | { readonly kind: 'NEVER_RESPOND' }        // para ejercitar timeout y fallo cerrado
  | { readonly kind: 'PARTIAL'; readonly approve: ReadonlyArray<string> }
  | { readonly kind: 'ABANDON_AFTER'; readonly n: number };

/**
 * NO decide nada: REPRODUCE un guion fijado por el test.
 * Ausencia deliberada de heurísticas: un stub que "parece" decidir invita a razonar sobre él
 * como si fuera un humano, y ese es el error que este objeto existe para hacer imposible.
 */
class DevHumanAuthorizationProvider implements HumanAuthorizationProvider {
  readonly provider_id = 'dev-stub';

  constructor(private readonly script: StubScript) {}

  capabilities(): ProviderCapabilities {
    // Miente en la dirección INCÓMODA a propósito: declara las capacidades más restrictivas,
    // para que el código de Application ejercitado en DEV sea el de la rama degradada.
    return { human_initiated: false, requires_inflight_tool_call: true };
  }

  async openReviewSession(request: ReviewSessionRequest): Promise<void> {
    // Efecto observable OBLIGATORIO en DEV: dejar rastro de que NO hubo humano.
    // No es telemetría; es la contrapartida de la marca indeleble en el lado del proceso.
    emitDevStubTrace('review_session_opened_by_stub', request.review_session_id);
  }

  async awaitOutcome(id: string, signal: AbortSignal): Promise<ReviewSessionOutcome> {
    // Aplica el guion. NO devuelve authorization_source: no es suyo (§8.2).
    return applyScript(this.script, id, signal);
  }

  async cancelReviewSession(id: string, reason: string): Promise<void> {
    emitDevStubTrace('review_session_cancelled_by_stub', id, reason);
  }
}

/** El descriptor es lo que hace la marca INDELEBLE: no depende de la conducta del stub. */
const DEV_STUB_DESCRIPTOR: ProviderDescriptor = {
  provider_id: 'dev-stub',
  source: 'DEV_STUB',                                  // ← única fuente de authorization_source
  admissible_profiles: ['development', 'test'],        // ← 'production' AUSENTE, no "prohibido"
  factory: () => new DevHumanAuthorizationProvider({ kind: 'APPROVE_ALL' }),
};
```

**Nota sobre `admissible_profiles`.** El perfil de producción está **ausente** de la lista, no
listado como prohibido. Es intencionado: la comprobación de §9 es *"¿está el perfil efectivo en la
lista de admisibles?"* (allow-list), no *"¿está en una lista de vetados?"* (deny-list). Una allow-list
falla del lado seguro cuando aparece un perfil nuevo que nadie recordó vetar.

### 8.5 Propagación de la marca (kernel §4, requisito 2)

`authorization_source` se persiste y se propaga en **cuatro** lugares, y esto es comprobable:

1. El registro `HumanAuthorization` (kernel §3).
2. El `payload` del `CaseEvent` `ProposalReviewed` (kernel §8.1).
3. El `payload` del `CaseEvent` `FactsCommitted` que la consume.
4. El `Tool Invocation Log` de la invocación de `commit_reviewed_facts` (kernel §8.2).

Los puntos 2 y 3 entran en el `payload_hash` y por tanto en el hash-chain: **borrar la marca rompe
la cadena de forma detectable** (tamper-evident, kernel §8.3 — **no** tamper-proof; no se afirma
imposibilidad).

---

## 9. FAIL TO START — detección y justificación

**Requisito literal (kernel §4.1):** *"Si la configuración efectiva es de producción y el provider
resuelto es el stub, el arranque **aborta** con error de configuración. No hay modo degradado ni
advertencia ignorable."*

### 9.1 Cómo se detecta que una configuración es de producción

**Principio rector: la determinación debe fallar del lado seguro.** El accidente que tememos es *una
instalación de producción corriendo el stub*. Por tanto, **toda ambigüedad se resuelve como
producción**, nunca como desarrollo.

**PROPUESTA DEL TECHNICAL DESIGN — señal declarada y explícita, sin valor por defecto:**

```ts
// NON-PRODUCTION SPIKE — conceptual
type DeploymentProfile = 'production' | 'development' | 'test';
```

Reglas de determinación, en orden:

| # | Regla | Resultado |
|---|---|---|
| **R1** | El perfil se declara en **una clave explícita** de la configuración efectiva. **No tiene valor por defecto.** | — |
| **R2** | Clave **ausente**, ilegible, o con un valor **no reconocido** ⇒ **`production`**. | Fail-safe |
| **R3** | Cualquiera de las **señales de corroboración** (abajo) es cierta ⇒ **`production`**, *aunque la clave declare otra cosa*. Las señales solo **escalan**; nunca degradan. | Fail-safe |
| **R4** | El perfil se resuelve **una vez, antes de cualquier efecto**, y es **inmutable** durante la vida del proceso. No hay recarga en caliente del perfil. | — |

**Por qué NO se usa `NODE_ENV`:** tiene valores por defecto de facto, lo tocan herramientas de
terceros, y su ausencia se interpreta habitualmente como "development" — exactamente la dirección de
fallo equivocada. **Si se lee, es solo como señal de corroboración que escala** (R3), nunca como
fuente del perfil.

**Señales de corroboración (cualquiera ⇒ producción):**

| Señal | Razón |
|---|---|
| El case store apunta a una ruta **fuera del sandbox de desarrollo declarado** | Un store real es un expediente real. |
| El `Case` a abrir lleva `store_mode = PRODUCTION` en su propio registro | El expediente declara su naturaleza; viaja con el archivo. Impide que copiar un `case.db` de producción a una máquina de desarrollo lo "convierta" en de desarrollo. |
| La build es la de distribución (no la de desarrollo) | — |

**Comprobación recíproca (kernel §4.2, segunda mitad):** en perfil `production`, abrir un `Case` que
contenga autorizaciones `DEV_STUB` **consumidas** se rechaza. Son dos comprobaciones distintas y
ambas hacen falta: R1–R3 protegen **el proceso** en el arranque; esta protege **el dato** en la
apertura. Sin la segunda, un `case.db` contaminado en desarrollo entraría luego en producción por un
proceso perfectamente configurado.

**Regla de resolución del provider (allow-list, §8.4):**

```
perfil_efectivo ∉ descriptor.admissible_profiles  ⇒  ABORT
```

Con esto, el caso del kernel §4.1 es **una instancia** de una regla general, no un `if` especial
sobre el stub. Un futuro provider de pruebas nuevo hereda la protección sin que nadie recuerde
añadirla.

**Momento del aborto — obligatorio:** **antes de cualquier efecto observable**. Antes de abrir el
case store para escritura, antes de ligar ningún listener, antes de aceptar la primera petición MCP,
antes de escribir un solo evento. Salida con código distinto de cero y un código de error estable y
legible por máquina (p. ej. `CONFIG_FATAL_DEV_PROVIDER_IN_PRODUCTION`), nombrando el perfil
detectado, la señal que lo determinó y el `provider_id` resuelto.

**No existe bandera de anulación.** Ni `--force`, ni variable de entorno, ni clave de configuración.
Kernel §4.1: *"No hay modo degradado ni advertencia ignorable"*. Una anulación convierte el aborto en
una advertencia con pasos extra, que es precisamente lo que la decisión prohíbe.

### 9.2 Por qué el arranque debe abortar en vez de advertir

Seis razones, de la más fuerte a la más débil:

1. **Asimetría entre la señal y el daño.** La advertencia es **efímera** (una línea en un flujo que
   nadie lee); el daño es **durable** (un `case.db` con actos de autoridad humana fabricados, que
   sobrevive al proceso, a la sesión y probablemente al proyecto). Una señal efímera no es
   proporcionada a un daño permanente.
2. **Es una condición decidible a coste cero en t=0.** No hace falta ejecutar nada para saberlo:
   basta leer la configuración. Un sistema que **puede saber que es inseguro antes de hacer nada** y
   aun así procede está **eligiendo** producir registros jurídicos inválidos. Advertir sería honesto
   solo si la condición se descubriera tarde; no es el caso.
3. **Preserva un invariante comprobable a nivel de store, no registro por registro.** Con aborto:
   *"en un store de producción, una autorización es un acto humano"* — verificable de un vistazo. Sin
   aborto: cada lectura de cada autorización de cada caso debe comprobar `authorization_source` para
   saber si significa algo. **Un solo proceso mal configurado degradaría la fuerza probatoria de todo
   el corpus**, no solo la de los registros que produjo.
4. **Las advertencias se normalizan.** Una advertencia recurrente se convierte en ruido de fondo en
   semanas. La única propiedad que esta advertencia protege es **la propiedad por la que existe toda
   la cadena ADR-005**. No puede depender de que alguien siga leyéndola.
5. **Un modo degradado es un modo.** Habría que especificarlo, testearlo, documentarlo y mantenerlo:
   ¿qué hace el sistema con autorizaciones `DEV_STUB` en producción? ¿Se pueden commitear? ¿Se
   marcan? ¿Se purgan? No hay respuesta buena, porque **no hay comportamiento correcto para "produce
   consentimiento humano falso pero avisando"**. Abortar es el único fallo cuya semántica es limpia:
   no se escribió nada.
6. **Coherencia con el Product Floor.** PF-001 dice que la IA no puede asignar estado epistémico
   sensible y que la configuración **no puede relajarlo** (kernel §12). Un stub que emite
   autorizaciones en producción es **una configuración que relaja PF-001**. Si PF-001 no admite
   relajación, su gate no admite advertencia. **Nota:** esto sugiere que la sexta política candidata
   del kernel §12.6 podría ser más ancha de lo escrito allí — *"la marca de origen de la autoridad no
   es relajable por configuración"*. **DECISIÓN PENDIENTE (dueños), §12 D-4.**

**Contraargumento honesto, y su respuesta.** *"Abortar convierte un error de configuración en una
caída total; en producción eso es un incidente."* Cierto, y se acepta: **es un fallo en el arranque,
no en caliente.** No hay tráfico que cortar, no hay sesión que perder, no hay transacción a medias.
El coste es que alguien no puede empezar a trabajar hasta arreglar una clave de configuración; el
coste alternativo es un expediente con consentimiento fabricado. **La comparación no está reñida.**

---

## 10. AT-013 — diseño del test

**Enunciado del kernel §4:** *"arrancar con configuración de producción y provider stub ⇒ el proceso
no llega a estado operativo."*

### 10.1 Naturaleza del test — y por qué no puede ser un test unitario

**AT-013 es un test de proceso, de caja negra, sobre el composition root real.** Un test unitario de
la función de resolución **no verifica el requisito**: la función podría devolver el error correcto
mientras el cableado real lo ignora, lo captura, o lo evalúa después de abrir el store. El requisito
es *"el proceso no llega a estado operativo"* — una propiedad **del proceso**, observable solo
ejecutándolo.

**Regla dura del test:** arranca el binario real con la configuración real. **Prohibido** sustituir el
composition root por un doble; ese es el único componente que AT-013 pone a prueba.

### 10.2 Definición operativa de "no llegó a estado operativo"

No se acepta como prueba la lectura de un mensaje de log: un log es una afirmación del propio proceso
sobre sí mismo. Se exige **evidencia externa**, y las cuatro deben cumplirse:

| # | Aserción | Cómo se observa |
|---|---|---|
| **O1** | Código de salida distinto de cero, y **estable** | Código de salida del proceso |
| **O2** | **Nunca** emitió su señal de readiness (no aceptó la primera petición MCP; no creó su lock file) | Ausencia externa de la señal |
| **O3** | El case store **no fue modificado**: mismo tamaño, misma mtime, mismo hash de archivo antes y después | Hash del archivo antes/después |
| **O4** | **Cero eventos nuevos** en el Case Event Log; `event_seq` máximo idéntico | Consulta al store tras el intento |
| O5 | (complementaria, no suficiente por sí sola) stderr contiene el código de error estable | Captura de stderr |

**O3 es la aserción que impide el falso positivo más peligroso**: un proceso que aborta *después* de
haber tocado el store habría "fallado el arranque" y aun así dejado rastro.

### 10.3 Casos

| Id | Perfil declarado | Provider | Otras condiciones | Resultado exigido |
|---|---|---|---|---|
| **AT-013.a** | `production` | `dev-stub` | — | **ABORT.** O1–O4. Código `CONFIG_FATAL_DEV_PROVIDER_IN_PRODUCTION`. |
| **AT-013.b** | **ausente** | `dev-stub` | — | **ABORT** (R2, fail-safe). *Este es el caso del accidente real: nadie declara "producción"; simplemente nadie declara nada.* |
| **AT-013.c** | valor **no reconocido** (`"prod"`, `"PRODUCTION "`, `""`) | `dev-stub` | — | **ABORT** (R2). Tabla de valores hostiles, incluida diferencia de caja y espacios. |
| **AT-013.d** | `development` | `dev-stub` | store fuera del sandbox de dev | **ABORT** (R3: la señal escala a producción pese al perfil declarado). |
| **AT-013.e** | `development` | `dev-stub` | store dentro del sandbox | **ARRANCA.** Y toda autorización emitida lleva `authorization_source = DEV_STUB` en los **cuatro** puntos de §8.5. |
| **AT-013.f** | `production` | provider real | — | **ARRANCA.** *Control obligatorio: sin él, un binario que aborta siempre pasaría a–d.* |
| **AT-013.g** | `production` | provider real | el `Case` contiene autorizaciones `DEV_STUB` **consumidas** | **ARRANCA pero `open_case` se RECHAZA** con código propio y distinto del de a–d. Kernel §4.2. |
| **AT-013.h** | `test` | `dev-stub` | — | **ARRANCA.** El perfil `test` es admisible. |

### 10.4 Tests de arquitectura que acompañan a AT-013

No sustituyen a AT-013; cubren lo que un test de proceso no ve.

| Id | Qué comprueba | Etiqueta |
|---|---|---|
| **AT-013.i** | `authorization_source` **no puede** proceder del valor devuelto por el provider. Test de propiedad: un provider malicioso que intente inyectar `source: 'REAL'` produce igualmente `DEV_STUB`. Verifica §8.2. | Diseñable hoy |
| **AT-013.j** | Regla de dependencias: **ningún archivo de `src/` importa de `experiments/`**, y ningún archivo de `src/` fuera del registro de composición importa el módulo del stub. Kernel §13. | Diseñable hoy |
| **AT-013.k** | El artefacto de distribución **no contiene** el símbolo del stub. | **HIPÓTESIS** sobre el comportamiento del empaquetador. No se afirma que ninguna herramienta lo garantice. Defensa complementaria; **AT-013.a–d no dependen de ella.** |
| **AT-013.l** | Añadir un `ProviderDescriptor` nuevo sin `admissible_profiles` **no compila** o falla en el registro. Evita que la protección se pierda por omisión. | Diseñable hoy |

### 10.5 Relación con la batería de ADR-005

AT-013 **no reemplaza** los seis tests negativos de ADR-005 ("Validación / pruebas necesarias"), que
siguen siendo criterios de aceptación de primera clase: cubren el **gate de commit**. AT-013 cubre el
**gate de arranque**. Son gates distintos y ambos pueden fallar por separado. Punto de contacto:
AT-013.e verifica la marca; el test 3 de ADR-005 (reuso) verifica el consumo.

---

## 11. Recomendación priorizada

### R1 — Construir la superficie de revisión propia del Core (b1) como **canal normativo**. *Prioridad máxima.*

Fundamento, en orden de peso:

1. **Es el único candidato que satisface C1 y C2 estructuralmente**, sin delegar la garantía en un
   MUST que cumple software de terceros y que no podemos verificar en runtime (§3.5, §4.1).
2. **No es opcional aunque se adopte (a):** en URL mode la decisión ocurre fuera de banda contra una
   página del servidor, luego **(b1) hay que construirlo de todos modos** (§2.2). No es un coste
   alternativo; es el coste base.
3. **Es el único donde la profesional inicia la revisión sin el modelo** (§4.2), que es la lectura
   literal de kernel §7.
4. **Su coste marginal es menor de lo que parece:** el scope `pending` del kernel §9 ya obliga a
   construir la proyección; (b1) le añade controles de decisión.

Con las decisiones D-1 a D-7 (§4.3) como obligatorias, no opcionales.

### R2 — Añadir URL-mode elicitation como **lanzador oportunista**, detectado en runtime. *Prioridad media.*

- Se activa **solo** si el cliente declara `elicitation: { url: {} }` en las capabilities de la
  petición (§3.8). Si no, el Core no lo envía — la spec se lo **prohíbe**.
- Su función es **descubrimiento y comodidad**: evitar que la profesional tenga que acordarse de
  abrir la ventana. Nunca es la garantía.
- **Requisito de diseño no negociable:** el sistema debe comportarse **exactamente igual** si la
  elicitation es auto-aceptada por un hook (§3.6). Abrir la URL no aprueba (D-3). Esta propiedad
  merece su propio test.
- **Descartar si** la verificación de Cowork (§3.8) resulta negativa. No se pierde nada: (b1) ya
  cubre el caso.

### R3 — CLI propia (c2) como **fallback y canal de test**. *Prioridad baja, valor alto en test.*

Habilita AT-013 y los tests de ADR-005 sin instrumentar navegador, y cubre entornos headless. **No es
la UX primaria** (§5.2).

### R4 — Rechazos, con su fundamento

| Rechazado | Fundamento |
|---|---|
| **form mode elicitation** en cualquier rol del canal de autorización | "Data is exposed to the client" (literal); aprobación de usuario solo SHOULD; y el runtime **documenta** el mecanismo que la auto-responde (§3.4, §3.6). |
| **(c1) CLI/TUI del runtime** como superficie de decisión | Falla C1 y C2, y **no existe en Cowork** (§5.1). |
| **Ventana nativa (b2)** en v0 | Coste alto sin ganancia de garantía frente a (b1) dentro del límite del §7 (§4.4). |
| **Cualquier bandera de anulación del FAIL TO START** | Kernel §4.1, literal (§9.2). |

### R5 — Secuencia sugerida

1. Port `HumanAuthorizationProvider` + stub + FAIL TO START + **AT-013**. *Se puede hacer ya: no
   depende de ninguna verificación pendiente.*
2. (c2) CLI propia ⇒ desbloquea la batería de ADR-005 end-to-end.
3. (b1) página local ⇒ canal normativo.
4. Verificar Cowork (§3.8) ⇒ decidir R2 con dato, no con hipótesis.

**Observación deliberada sobre esta secuencia:** los pasos 1–3 **no dependen de ninguna verificación
pendiente de plataforma**. El spike, por tanto, **no bloquea la implementación**; solo bloquea R2.
Esto corrige el "el slice no cierra sin el spike de transporte" de ADR-005: el slice cierra con (b1);
lo que falta verificar es únicamente si además puede tener un lanzador cómodo.

---

## 12. Decisiones que necesitan tomar los dueños

| Id | Decisión | Por qué no puede tomarla el Technical Design | Coste de cada opción |
|---|---|---|---|
| **D-1** | **¿Se acepta que la superficie de autorización sea producto propio (b1), con su coste, en lugar de apoyarse en la del host?** | Es un compromiso de alcance y presupuesto de producto. | Aceptar: construir y mantener una superficie de UI. Rechazar: la garantía nuclear queda delegada en terceros y **POR VERIFICAR** en Cowork. |
| **D-2** | **¿Se ratifica la lectura del port como driven (§8.1)** como refinamiento de ADR-005 §5, y no como cambio de decisión? | Toca la interpretación de un ADR **Accepted**. | Ratificar: coherencia entre kernel §4 y §7. No ratificar: hay que rediseñar dónde vive el seam del FAIL TO START. |
| **D-3** | **¿Se acepta que un perfil de despliegue ausente o no reconocido se trate como PRODUCCIÓN (R2)?** | Hace el arranque en desarrollo más incómodo. Es una elección de valores: seguridad sobre conveniencia del equipo. | Aceptar: los desarrolladores deben declarar el perfil siempre. Rechazar: **AT-013.b —el caso del accidente real— dejaría de estar cubierto.** |
| **D-4** | **¿Entra "el origen de la autoridad no es relajable por configuración" en el Product Floor** como PF-006, junto a la candidata de auditoría del kernel §12.6? | El Product Floor es decisión de los dueños. | Entrar: la regla vive en el nivel más alto y no se erosiona. No entrar: hoy **ninguna** de las cinco políticas cubre este caso explícitamente. |
| **D-5** | **¿Qué mecanismo de identificación se exige en la superficie humana:** un clic, o un acto de identificación por acto? | Es el compromiso central entre fuerza probatoria y fatiga de revisión (RIESGO principal de ADR-005). | Clic: fluido, más falsificable. Identificación: más fuerte, alimenta la fatiga. **POR VERIFICAR** su disponibilidad técnica antes de poder elegirla (§7). |
| **D-6** | **¿De dónde sale el `principal_id` de la revisión** en una instalación monousuaria? ¿Identidad configurada al instalar, o identidad del SO? | Determina qué significa "humano identificado" en ADR-005. | Configurada: simple, débil. Del SO: más fuerte, **POR VERIFICAR** en Windows. |
| **D-7** | **¿Entra el lanzador (a) en v0, o se difiere?** | Alcance de v0. | Entrar: mejor descubrimiento, dependencia POR VERIFICAR. Diferir: v0 más pequeño y sin dependencias externas; la profesional debe abrir la revisión ella misma. |
| **D-8** | **¿Se aprueba el amendment de `case_revision` del kernel §5.2?** (ya abierta) | Ya registrada como ADR AMENDMENT CANDIDATE. | **No afecta a este spike** (§0.4), pero afecta a qué escribe el Core en `expected_case_revision`. |

---

## 13. Qué quedó NOT_TESTED o INCONCLUSIVE

### 13.1 `NOT_TESTED` — no se ejecutó ningún experimento

| Qué | Por qué no se probó | Qué haría falta |
|---|---|---|
| Que Cowork acepte y presente una elicitation URL-mode de un servidor MCP local | **No se construyó ningún servidor MCP ni se instrumentó ningún cliente.** El spike fue documental por alcance. | Servidor MCP mínimo bajo `experiments/` que registre las capabilities recibidas por petición y emita un `InputRequiredResult` URL-mode; ejecutarlo en Cowork y en Claude Code y **observar**. |
| Que Claude Code presente el diálogo tal como lo describe su documentación | Ídem. **La documentación es *documented platform guarantee*; lo que haga la versión instalada sería *observed in current environment*, y no se observó nada.** | Ídem. |
| Que un hook `Elicitation` pueda auto-**aceptar** (no solo denegar) | Requiere configurar un hook y observar. **No se hizo.** | Hook de prueba + servidor de prueba. **Resultado esperado irrelevante para el diseño**: R1/R2 ya asumen el peor caso. |
| Que la URL de una elicitation URL-mode llegue —o no— al contexto del modelo | Requiere observar el transcript real. **No se hizo.** | Servidor de prueba + inspección del transcript. **Tiene peso de seguridad real** (§3.3). |
| Comportamiento del navegador por defecto en el Windows objetivo | Depende de la máquina de la usuaria, que es **SUPUESTO** del proyecto (ADR-002). | Prueba en el equipo real. |
| Coste real de construcción de (b1) y (c2) | **Toda cifra de esfuerzo de este documento es HIPÓTESIS**, no medida. | Prototipo desechable con límite de tiempo. |
| Que el artefacto de distribución excluya el stub (AT-013.k) | Depende de una cadena de build que **no existe todavía**. | Verificar cuando exista. **No bloquea AT-013.a–d.** |

### 13.2 `INCONCLUSIVE` — se buscó en fuente oficial y no se resolvió

| Qué | Estado exacto | Impacto |
|---|---|---|
| **Soporte de MCP elicitation en Cowork** (form o URL) | **NOT FOUND en documentación oficial.** Cowork comparte arquitectura agentic con Claude Code (verificado) y soporta conectores MCP (verificado), **pero ninguna fuente oficial afirma que soporte elicitation.** No se afirma que no lo soporte: se afirma que **no se encontró**. | **Bloquea R2 y solo R2.** Mitigado porque la spec obliga a declarar la capability por petición ⇒ **detectable en runtime** (§3.8). |
| **Esquema de `hookSpecificOutput` para que un hook `Elicitation` acepte** | **INCONCLUSIVE.** El producto documenta *"auto-respond […] without showing a dialog"*; la referencia de hooks consultada documenta el camino de **denegación** (exit 2) y que en estos eventos *"an exit-2 hook's `hookSpecificOutput` is ignored"*. **No se localizó** el esquema del camino de aceptación. | **Ninguno sobre el diseño**: R1/R2 asumen el peor caso. Importa solo para dimensionar el riesgo si alguien propusiera form mode. |
| **Superficie equivalente a "confirm in the CLI" en Cowork** | **INCONCLUSIVE.** Claude Code documenta *"Complete the flow in the browser, then confirm in the CLI"*; Cowork es *"no terminal required"*. **HIPÓTESIS** de que necesita una superficie propia; no verificada. | Afecta a la UX de R2, no a la garantía. |
| **Mecanismo de verificación de identidad** que satisfaga el MUST anti-phishing en un servidor **local** | La spec admite el caso y remite a *"a different mechanism"* sin prescribir ninguno. **Queda como DECISIÓN PENDIENTE** (D-5, D-6), no como hecho pendiente. | Real; acotado por §7. |
| **Segundo principal fuera del contexto del modelo** (credencial del SO / biométrico) desde Node LTS en Windows | **POR VERIFICAR. No se investigó.** **No se afirma que exista API accesible alguna.** | Es el camino de evolución del §7, post-V0 (kernel §15). |

### 13.3 Lo que este spike **sí** resolvió, para que conste

- **C3 no es un criterio de transporte** (§2.1) — cierra una comparación mal planteada.
- **(a) no es alternativa a (b): es (b) más un lanzador** (§2.2) — reordena coste y decisión.
- **form mode queda rechazado con un argumento más fuerte** que el de ADR-005: no es una laguna de la
  spec, es una **capacidad documentada del runtime** (§3.6).
- **(c1) queda rechazado** por fallar C1 y C2 y por **no existir en el host previsto** (§5.1).
- **El diseño del port, del stub, del FAIL TO START y de AT-013 no depende de ninguna verificación
  pendiente** y puede implementarse ya (§11, R5).

---

## 14. Anexo — extractos literales de fuente oficial primaria

> Consultados el **2026-08-24**. Se reproducen para que cualquier lector pueda auditar las
> afirmaciones sin repetir la búsqueda. **Son citas de documentación de plataforma, no resultados de
> experimento.** La documentación describe lo que la plataforma *debe* hacer; nadie ha observado aquí
> lo que la versión instalada *hace*.

### A. MCP — Elicitation, revisión 2026-07-28

`https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation`

- Modos: *"`"form"`: In-band structured data collection with optional schema validation. Data is
  exposed to the client."* / *"`"url"`: Out-of-band interaction via URL navigation. Data (other
  than the URL itself) is not exposed to the client."*
- Modelo de interacción: *"Implementations are free to expose elicitation through any interface
  pattern that suits their needs—the protocol itself does not mandate any specific user interaction
  model."*
- Información sensible: *"Servers MUST NOT use form mode elicitation to request sensitive
  information such as passwords, API keys, access tokens, or payment credentials"* / *"Servers MUST
  use URL mode for interactions involving such sensitive information"*.
- Capabilities: *"Clients that support elicitation MUST declare the `elicitation` capability in
  `_meta.io.modelcontextprotocol/clientCapabilities` on each request"*; *"an empty capabilities
  object is equivalent to declaring support for `form` mode only"*; *"Servers MUST NOT send
  elicitation requests with modes that are not supported by the client."*
- Safe URL Handling (clientes): *"MUST NOT automatically pre-fetch the URL"*; *"MUST NOT open the URL
  without explicit consent from the user"*; *"MUST show the full URL to the user for examination
  before consent"*; *"MUST open the URL provided by the server in a secure manner that does not
  enable the client or LLM to inspect the content or user inputs."*
- Safe URL Handling (servidores): *"MUST NOT include sensitive information about the end-user […] in
  the URL"*; *"MUST NOT provide a URL which is pre-authenticated to access a protected resource"*.
- Semántica de `accept` en URL mode: *"The response with `action: "accept"` indicates that the user
  has consented to the interaction. It does not mean that the interaction is complete. The
  interaction occurs out of band and the client is not directly informed of the outcome."*
- Aprobación: *"Clients SHOULD implement user approval controls."*
- Phishing: *"The MCP Server MUST verify the identity of the user who opens the URL before accepting
  information."*
- Estabilidad: *"URL mode elicitation is introduced in the `2025-11-25` version […] Its design and
  implementation may change in future protocol revisions."*

### B. MCP — Versioning

`https://modelcontextprotocol.io/specification/versioning`

- *"The current protocol version is 2026-07-28."*

### C. Claude Code — MCP

`https://code.claude.com/docs/en/mcp`

- *"MCP servers can request structured input from you mid-task using elicitation. […] No
  configuration is required on your side: elicitation dialogs appear automatically when a server
  requests them."*
- *"Form mode: Claude Code shows a dialog with form fields defined by the server […]"*
- *"URL mode: Claude Code opens a browser URL for authentication or approval. Complete the flow in
  the browser, then confirm in the CLI."*
- *"To auto-respond to elicitation requests without showing a dialog, use the `Elicitation` hook."*

### D. Claude Code — Hooks

`https://code.claude.com/docs/en/hooks`

- `Elicitation` — dispara: *"When an MCP server requests user input during a tool call"*; en exit 2:
  *"Denies the elicitation"*.
- `ElicitationResult` — dispara: *"After a user responds to an MCP elicitation, before the response
  is sent back to the server"*; en exit 2: *"Blocks the response (action becomes decline)"*.
- *"On `Elicitation` and `ElicitationResult`, an exit-2 hook's `hookSpecificOutput` is ignored."*

### E. Cowork

`https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork` — verificado
previamente en `docs/architecture/notes/research-v0_1/verif-cowork.md`

- *"Claude Cowork uses the same agentic architecture that powers Claude Code, with no terminal
  required."*
- Acceso directo a archivos locales en Desktop; conectores MCP con modos de aprobación.
- **NOT FOUND:** mención de elicitation, en cualquiera de sus modos.
