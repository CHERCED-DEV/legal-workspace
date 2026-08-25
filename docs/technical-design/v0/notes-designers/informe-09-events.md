# Informe del disenador: 09-events

Retorno crudo del agente que redacto este documento. Contiene: rutas, decisiones que requieren aprobacion, conflictos y POST-V0 / POR VERIFICAR.

---

Ambos archivos escritos y verificados.

**(1) RUTAS ESCRITAS**
- `C:\Users\HITMA\Desktop\legal-workspace\docs\technical-design\v0\09-events-and-audit.md` (977 líneas)
- `C:\Users\HITMA\Desktop\legal-workspace\docs\architecture\adrs\ADR-009-event-and-audit-strategy.md` (265 líneas, Estado = Proposed, secciones exactas)

**(2) DECISIONES QUE REQUIEREN APROBACIÓN** (21 en `09` §9; 11 en la Decisión del ADR-009)
1. Preimagen completa del `event_hash`: separador de dominio versionado (`legal-os/case-event/v1`), separador de campo inyectivo (0x1F), cabecera completa (`principal_*` y `provenance_kind` dentro del hash) y `case_revision` incluido aunque sea `null`. El kernel §8.1 la dejaba con puntos suspensivos.
2. Forma canónica de serialización, incluida **prohibición de coma flotante** en payloads (evita falsos positivos de manipulación entre runtimes).
3. `chain_spec_version` en `cases` — aditivo sobre `04` §3.1.
4. `current_event_hash` en `cases` como testigo de cabeza redundante — aditivo sobre `04` §3.1; mitigación **parcial**, declarada como tal.
5. Regla N — no duplicación intra-log: referencia `(id, content_hash)` a contenido ya fijado.
6. `occurred_at` no ordena nada; el orden lo fija `event_seq`.
7. `ProposalReviewed` como **un** tipo con `approved/rejected/partial` derivados de `decisions_summary` (cierra D.1 del addendum v0.3; ratificación de letra Accepted).
8. Payload de `FactWithdrawn` **no contratado** en V0.
9. Forma de la política de retención: dos horizontes, eje único de antigüedad + 5 reglas duras de poda (por antigüedad nunca por contenido; marca de agua durable; solo runtime/CLI; nunca en transacción; no toca `case.db`).
10. **PF-006** — «el Case Event Log no es desactivable, editable ni podable por configuración» como sexta política del Product Floor.
11. **ADR AMENDMENT CANDIDATE sobre ADR-004/ADR-005**: separar `event_seq` de `case_revision` (Decisión 5 del ADR-009). Presentados ambos modelos con argumentos, traza numérica comparada, impacto punto por punto sobre addendum v0.3 B.2 y tabla de «qué cambia según cuál se apruebe». **NO aplicado**; `09` es neutral y usa dos columnas.

**(3) CONFLICTOS CON ADRs ACCEPTED**
- **C-A — Aritmética de revisiones** (ADR-004 (b)1/(c)/inv. 5; ADR-005 §1, §4, inv. 9–10; addendum B.2). Declarado, no aplicado. Incluye la contradicción interna del kernel (§5.2 dice «no se aplica», §7 ya lo aplica).
- **C-B — `ProposalPreservedForReconciliation`**: en la lista cerrada de ADR-004, ausente del kernel §8.1. Además **divergencia entre hermanos**: `03` §11.6/§11.9 emite el evento y persiste marcador; `04` §2 no añade columna a `proposals`. `09` admite el tipo (ADR-004 es nivel 1), contrata su payload y no elige productor.
- **C-C — `ProposalReviewed(approved/rejected/partial)`**: cambio de letra sobre lista cerrada Accepted (§8.5).
- **Hallazgo de coherencia (no es conflicto con ADR, es entre hermanos):** hoy conviven **dos aritméticas simultáneas** — `01` numera con Modelo A por precedencia, `03` con Modelo B por kernel §7. Los seis documentos declaran el conflicto, pero `01` y `03` numeran los mismos pasos con valores distintos. Recomendación: decidir el amendment **antes** de la normalización cruzada, y en la misma decisión resolver la tensión `FactsProposed`/`ArtifactRegistered`/`ArtifactMarkedStale` (§7.9), o se entrega la mitad del beneficio.
- **C4 heredado (procedencia adicional en reingestión)**: `09` §8.4 **rechaza con fundamento propio** la opción de registrarla solo en el log operacional (violaría ADR-004 inv. 8 y la poda destruiría custodia) y recomienda `EvidenceIncorporated` con `reingestion: true`, sin abrir la lista cerrada.

**(4) POST-V0 / POR VERIFICAR / RIESGOS**
- **POR VERIFICAR:** especificación de canonicalización adoptada y garantías del runtime sobre orden de claves y representación numérica; suficiencia del `input_hash` para diagnóstico real; soporte UUIDv7 (alt. ULID); numeración definitiva `F-xx`/`AT-xxx`; coste real de payloads suficientes para reconstrucción (**ninguna afirmación de rendimiento se hace**).
- **DECISIONES PENDIENTES no resueltas:** valores de los dos horizontes de retención; anclaje del hash-cabeza fuera del workspace; guarda de monotonía del reloj; `event_ref` como lista; log operacional propio del canal humano; si el reconstructor entra en V0 como test.
- **POST-V0:** firma criptográfica de eventos; anclaje externo (implementación); log multi-máquina y sync; reconstructor como camino de operación; poda del `OperationLedger`; revisiones por agregado; payload de `FactWithdrawn` y `RecordProfessionalDetermination`.
- **RIESGOS declarados** (honestidad obligatoria escrita): tamper-evident **no** tamper-proof, usuaria hostil con control total **fuera del threat model V0**; truncamiento por la cola sin testigo externo; **la cadena sella el log, no las tablas materializadas — hoy sin detección** salvo que se apruebe el reconstructor como test; sin firma, un `event_hash` correcto no prueba identidad; reloj de pared no afecta al orden pero sí a `expires_at`; los hallazgos verificados del spike de Cowork hacen la protección del log **posicional**, nunca apoyada en reglas del anfitrión.