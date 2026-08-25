# Estado del Technical Design V0 y hallazgos críticos del spike de Cowork

**Fecha:** 2026-08-24 · **Documento de continuidad**: permite retomar el trabajo sin depender de la conversación.

---

## 1. HALLAZGO CRÍTICO — el spike de Cowork invalida un supuesto de mecanismo

El spike documental de Cowork (`docs/research/cowork-runtime-spike-v0.md`, 49 filas, 44 VERIFIED / 21 INCONCLUSIVE / 8 NOT_TESTED / 7 NOT_SUPPORTED) produjo cinco hechos verificados que **cambian el mecanismo de enforcement**, aunque no invalidan ninguna decisión de los ADRs Accepted.

### 1.1 Hechos verificados contra documentación oficial

1. **Cowork no hereda la configuración de Claude Code.** La documentación oficial afirma que Cowork *no lee el directorio `~/.claude` de la CLI de Claude Code*. **Consecuencia dura: ninguna regla `deny`, `allowedTools` ni hook de Claude Code gobierna Cowork.** Todo razonamiento por analogía entre ambos productos queda invalidado — incluido el que el corpus previo usaba como base del perímetro.
2. **No existe deny por ruta en Cowork.** Adjuntar una carpeta concede su árbol completo; el agente puede leer y escribir todo lo que alcance la cuenta del sistema operativo. El único remedio documentado es **posicional**: dejar los datos fuera de las carpetas permitidas.
3. **Los servidores MCP locales corren en el host, no en la VM.** El bucle del agente (lecturas y escrituras en carpetas conectadas, servidores MCP locales de plugin) se ejecuta nativamente en el dispositivo; el shell sí corre en una VM aislada.
4. **El modo Auto delega la decisión de seguridad en el propio modelo**, que revisa cada acción y bloquea lo que *determine* inseguro. Un control juzgado por el sistema evaluado no puede sostener una garantía de producto.
5. **Elicitation en modo form no prueba acto humano en este stack.** En Claude Code existe un hook de elicitation que puede responder automáticamente sin mostrar diálogo, con advertencia oficial de que evita la confirmación del usuario.

### 1.2 La hipótesis de la que depende ADR-002 — y que la documentación no resuelve

**B-04, INCONCLUSIVE:** la documentación enuncia el confinamiento a carpetas siempre sobre *acceso local a archivos* y *llamadas a herramientas locales*, **nunca sobre el proceso del servidor MCP**. Es decir: no está documentado si un servidor MCP local puede alcanzar rutas fuera de las carpetas adjuntadas.

Esta es **la pregunta decisiva de todo el perímetro**:

- Si el MCP local **sí** puede alcanzar el private state mientras el host **no** → ADR-002 es implementable tal como está.
- Si el MCP local **está confinado igual que el host** → el Core no podría alcanzar su propio estado canónico sin que el host también lo alcance, y **el mecanismo de ADR-002 no sería realizable sobre Cowork** (la decisión seguiría siendo correcta; haría falta otro anfitrión o un Core como proceso independiente).

**Es un riesgo bloqueante para la implementación, y solo se resuelve empíricamente.** El protocolo está listo en `experiments/cowork-capability-spike/README.md` (31 pasos) con la estructura de prueba en `experimental-root/`.

### 1.3 Implicación arquitectónica, sin cambiar ningún ADR

- **La protección del case store no puede ser una regla; tiene que ser una posición.** `case.db`, originales y event log fuera de toda carpeta adjuntable. Esto es exactamente lo que ADR-002 decidió ("la regla es la separación, no el path"), pero el mecanismo deja de apoyarse en reglas del host.
- **Cowork no es una frontera de seguridad: es defensa en profundidad.** La frontera real es el Core. ADR-001 ya lo dice; ahora hay evidencia de por qué es imprescindible que lo diga.
- **Los cinco hallazgos refuerzan, sin alterarlo, el diseño de autorización server-side** del kernel §3.3: la `HumanAuthorization` se resuelve dentro del Core, sin token para el modelo, ligada a `item_content_hash` + `expected_case_revision` + `consumed_at` + `expires_at`. **La UI del host es notificación, nunca autoridad.** Si el host puede auto-aprobar, cualquier diseño que confíe en su diálogo queda comprometido; el nuestro no lo hace.

**Veredicto: NO hay `CONFLICTO CON ADR ACCEPTED`.** Hay un cambio de *mecanismo de plataforma* (que los ADRs ya clasificaban como detalle de implementación) y una dependencia empírica sin resolver.

---

## 2. Estado de los entregables

### Producidos y guardados

| Documento | Ruta |
|---|---|
| Kernel técnico normativo v0.4 | `docs/technical-design/v0/00-technical-kernel.md` |
| System design | `docs/technical-design/v0/01-system-design.md` |
| Domain model | `docs/technical-design/v0/02-domain-model.md` |
| Human authorization | `docs/technical-design/v0/06-human-authorization.md` |
| Synthetic benchmark | `docs/technical-design/v0/13-synthetic-benchmark.md` |
| Spike Cowork (documental) | `docs/research/cowork-runtime-spike-v0.md` |
| Spike dependencias/runtime | `docs/research/runtime-dependencies-spike-v0.md` |
| Resúmenes de los seis spikes | `docs/research/spike-summaries/` |
| Spike Cowork (protocolo empírico) | `experiments/cowork-capability-spike/` |
| Spike transcripción | `experiments/transcription-spike/README.md` |
| Spike autorización | `experiments/authorization-spike/README.md` |
| Preguntas de negocio | `docs/discovery/business-questions-next.md` |
| Backlog post-V0 | `docs/backlog/architecture-post-v0.md` |
| Nota de normalización Principal/provenance | `docs/architecture/notes/normalizacion-principal-provenance-v0_4.md` |

### En curso al momento de escribir esto

Un workflow (`wsb65tbht`) redacta los documentos técnicos restantes: `03-application-use-cases`, `04-persistence-model` (+ ADR-007), `05-mcp-contract` (+ ADR-010), `07-provenance-and-locators` (+ ADR-011), `08-case-context-projections`, `09-events-and-audit` (+ ADR-009), `10-artifact-lifecycle`, `11-ux-condition-catalog`, `12-testing-strategy`, `14-repository-layout`, `15-product-floor-proposal`, `16-open-implementation-decisions`. Cada agente escribe su archivo directamente, de modo que lo terminado queda guardado aunque el proceso se interrumpa.

### Pendiente tras esos documentos

1. **Normalización** de `actor_type` → `Principal` / `provenance_kind` en los documentos anteriores (ADR-003, ADR-005, glosario, vertical-slice, kernel v0.2, addendum v0.3). La regla ya está escrita en la nota de normalización; falta aplicarla al texto.
2. **Validación cruzada** de los seis *drifts*: vocabulary, status, ownership, revision, trust, provenance y UX.
3. **Informe final A–H** con el veredicto de readiness.

---

## 3. Decisiones que esperan aprobación de los dueños

Registradas aquí para no perderlas:

1. `principal_type` sin `EXTERNAL` (solo `HUMAN | AI | SYSTEM`).
2. Lifecycle de ProposalItem en dos dimensiones (`review_decision` × `commit_state`), eliminando `DEFERRED` e `INVALIDATED`.
3. **ADR AMENDMENT CANDIDATE sobre ADR-004:** separar `event_seq` (todos los eventos) de `case_revision` (solo mutaciones del estado epistémico), de modo que la revisión humana no avance la revisión del caso.
4. Retiro de `register_artifact` de la superficie MCP (8 tools en vez de 9).
5. Una `HumanAuthorization` por item, agrupadas por `review_session_id`.
6. Conservar `expires_at`; eliminar `decision` del contrato de autorización.
7. Las cinco políticas del Product Floor (estado `PROPOSED`), más la decisión sobre si entra como sexta "el log de auditoría no es desactivable ni editable por configuración".
8. Los ADRs 007–011 en estado `Proposed`.

---

## 4. Riesgo abierto de mayor gravedad

**El punto B-04 del spike de Cowork.** Hasta resolverlo empíricamente no puede afirmarse que el perímetro de ADR-002 sea realizable sobre Cowork Desktop. No bloquea el Technical Design —que es independiente del anfitrión—, pero **sí bloquea comprometerse con Cowork como host de producción**. La alternativa de contingencia, si B-04 resulta desfavorable, es el Core como proceso independiente con permisos de sistema operativo propios, que ADR-002 ya contempla como opción.

---

## 5. Actualización de progreso (reintento tras límite de sesión)

El primer intento del workflow de documentos alcanzó el límite de sesión con 12 de 14 agentes cortados. **Sin embargo, la mayoría había escrito ya su archivo antes de fallar al retornar**: el fallo ocurrió al generar la respuesta final del agente, no durante la escritura. Verificado en disco.

### Completados y verificados en disco

| Documento | Tamaño |
|---|---|
| `00-technical-kernel.md` | 27 KB |
| `01-system-design.md` | 59 KB |
| `02-domain-model.md` | 60 KB |
| `03-application-use-cases.md` | 83 KB |
| `04-persistence-model.md` | 72 KB |
| `05-mcp-contract.md` | 68 KB |
| `06-human-authorization.md` | 58 KB |
| `13-synthetic-benchmark.md` | 79 KB |
| `ADR-008-proposal-and-human-authorization-model.md` | 28 KB |

### En curso en el reintento

`07-provenance-and-locators` (+ ADR-011), `08-case-context-projections`, `09-events-and-audit` (+ ADR-009), `10-artifact-lifecycle`, `11-ux-condition-catalog`, `12-testing-strategy`, `14-repository-layout`, `15-product-floor-proposal`, `16-open-implementation-decisions`, ADR-007 y ADR-010.

## 6. Conflictos con ADRs Accepted detectados por los diseñadores

Registrados aquí para no perderlos; **ninguno resuelto unilateralmente**.

1. **CONFLICTO — ADR-001 inv. 3: ocho tools frente a nueve.** El kernel técnico retira `register_artifact` de la superficie y deja 8; ADR-001 (Accepted) dice literalmente *nueve*. Por precedencia manda el ADR Accepted. Opciones: mantener 9 exponiendo `register_artifact`; enmendar ADR-001 a 8; o dejar la tool declarada pero no expuesta. **Requiere decisión de los dueños.**
2. **CONFLICTO — aritmética de revisión (ADR-004 (b)1 y ADR-005 inv. 9–10).** El kernel propone que `ProposalReviewed` no avance `case_revision`, pero declara que no se aplica hasta aprobación, mientras su propia tabla §7 ya lo presenta como "no": contradicción interna del kernel. Los documentos aplican el **Modelo A** (el de los ADRs Accepted) en las tablas numeradas y muestran el Modelo B en columna aparte. **Requiere decisión: es el ADR AMENDMENT CANDIDATE.**
3. **Divergencia menor — `completeness`.** Dos valores en el kernel (`COMPLETE | PARTIAL`) frente a tres en ADR-004 Accepted (`COMPLETE | TRUNCATED | PARTIAL`).
4. **Divergencia de alcance — Product Floor.** El conjunto del kernel no contiene la política de inmutabilidad de la auditoría que sí aparece en el anexo de `principles.md`. Por precedencia gana el kernel, con la consecuencia de que **hoy ninguna política del piso cubre esa garantía**: debe decidirse explícitamente, no por precedencia silenciosa.
