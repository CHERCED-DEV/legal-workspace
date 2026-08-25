# Informe del disenador: 10-artifact

Retorno crudo del agente que redacto este documento. Contiene: rutas, decisiones que requieren aprobacion, conflictos y POST-V0 / POR VERIFICAR.

---

(1) RUTAS ESCRITAS
- `C:/Users/HITMA/Desktop/legal-workspace/docs/technical-design/v0/10-artifact-lifecycle.md` (69 KB, 12 secciones). Único archivo creado; ningún ADR nuevo (el encargo no asigna ADR a artifact lifecycle; los conflictos relevantes ya están abiertos en 05 §11.1).

(2) DECISIONES QUE REQUIEREN APROBACIÓN
- **§2.4 — `Principal` de un artifact registrado internamente.** `created_by.principal_type = AI` + `provenance_kind = AI_INFERENCE` (heredado de la invocación), **no** `SYSTEM`, pese a que la fila la escribe el Core. Contraste normativo: el evento `ArtifactMarkedStale` sí es `SYSTEM`/`SYSTEM` (computación determinista). Regla general derivada propuesta: heredar el Principal cuando el registro porta contenido del invocador; `SYSTEM` cuando es computación del Core.
- **§2.5 — `base_case_revision` en vez de `artifacts.case_revision`.** Precisión semántica: bajo kernel §7 literal la fila se escribe en N+2 mientras el análisis leyó N. La revisión de escritura no se pierde (está en `ArtifactRegistered`). Exige pase de corrección en 04 §3.4, kernel v0.2 §10 y vertical-slice.
- **§5.4 — clase de staleness DERIVADA, no almacenada.** `staleness_class(reason)` como función total; `DEFINITE` domina. Sin columna nueva, sin condición nueva (catálogo cerrado en 7).
- **§5.5 — regla de asimetría** (el modelo añade incertidumbre, nunca la retira) y **§5.6 — regla de redacción obligatoria** para 11 (un mensaje `POTENTIAL` no puede afirmar que un insumo cambió).
- **§3.1 — conservar el enum `status` de 4 valores** con 3 sin productor (alternativa minimalista: reducir a `REGISTERED`). Recomendación: conservar.
- **§4.5 — `proposal_id` obligatorio en el payload de `ArtifactRegistered`** (coste cero). Columna `artifacts.produced_by_proposal_id`: DECISIÓN PENDIENTE, diferida.
- **§8.4 — especificación de `AT-009`** en cuatro subtests (a/b/c verificables, d declarado no verificable).

(3) CONFLICTOS CON ADRs ACCEPTED
**Ninguno nuevo.** El único conflicto en el área (retiro de `register_artifact` vs ADR-001 inv. 3 / val. 7 y ADR-006 inv. 3 / val. 3) **ya está documentado en 05 §11.1**, con señalamiento en 01 y 04 §C5; este documento aplica el kernel §6 y lo referencia sin reabrirlo. Las divergencias de §2.5 y §4.3 son con documentos de nivel 5, no con ADRs.

(4) POST-V0 / POR VERIFICAR
- **POST-V0:** reuso idempotente de análisis (fingerprint por inputs+metodología, distinto de la idempotencia de operación de 03 §9.11; `ANALYSIS_REUSED`; regla dura: un artifact stale nunca se reutiliza); razones de supersede tipadas (sin productor hoy; la cadena simple mantiene la ampliación aditiva); propagación semántica fina (solo puede reducir ruido `POTENTIAL`, jamás suprimir `DEFINITE`); aristas Artifact→Artifact y propagación transitiva (hipótesis: `DEFINITE` propaga, `POTENTIAL` no); productores de `DRAFT`/`REVIEWED`/`SUPERSEDED`; disparador de `METHODOLOGY_CHANGED`; razón para cambio de Knowledge Pack.
- **POR VERIFICAR:** consistencia de `ANALYSIS_STALE { reasons[], class? }` con `11-ux-condition-catalog.md`; numeración `AT-xxx` contra `12-testing-strategy.md` (AT-009 designa el adversarial 8); vigencia temporal en Colombia (`boundaries.md`) — condiciona que `METHODOLOGY_CHANGED` sea `DEFINITE`; colisión de PK en `artifact_inputs` si dos items consumen dos `content_hash` de la misma `entity_id` (respuesta correcta: rechazar, no relajar la clave).
- **Hallazgos declarados sin ocultar:** en V0 solo se ejercita la clase `POTENTIAL` (único productor: `IngestEvidence` → `NEW_EVIDENCE`); `METHODOLOGY_CHANGED` **no tiene mecanismo admisible** en V0 porque no hay mutador de Case en cuyo interior ejecutarlo; `inputs[]` puede quedar **vacío** si todos los items son `alleged_only`, dejando el artifact inalcanzable por `INPUT_SUPERSEDED`; el claim C4 de AT-009 (gate de salida final) **no es verificable en V0** y el Core **no controla la narración del modelo** (ADR-001 RIESGO, SUPUESTO de 01).