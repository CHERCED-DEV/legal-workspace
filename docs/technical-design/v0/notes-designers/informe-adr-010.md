# Informe del disenador: adr-010

Retorno crudo del agente que redacto este documento. Contiene: rutas, decisiones que requieren aprobacion, conflictos y POST-V0 / POR VERIFICAR.

---

(1) RUTAS ESCRITAS
- `C:/Users/HITMA/Desktop/legal-workspace/docs/architecture/adrs/ADR-010-mcp-surface-and-command-classification.md` (único archivo creado; Estado = Proposed; secciones exactas del formato exigido)

(2) DECISIONES QUE REQUIEREN APROBACIÓN
1. **Resolución del conflicto de §11** (bloqueante): opción A (enmendar ADR-001 a 8 y la literalidad de ADR-006 inv. 3/val. 3), B (mantener 9 exponiendo `register_artifact`), C (declarada pero no expuesta) o D (retirar sin enmendar — marcada inaceptable). Recomendación del technical design: A, coherente con `05-mcp-contract.md` §11.1. **No resuelta en este ADR.**
2. **REX como regla normativa** de exposición (+ corolarios REX-1..REX-4), incluida la exclusión por autoridad como criterio separado.
3. **Presupuesto de superficie**: V0 = la cuenta que resulte de (1); techo V1 = 12 (SUPUESTO, sin calibración empírica).
4. **Checklist de admisión de ocho puntos** y régimen de cambio de contrato para añadir/retirar/reclasificar tools.
5. **Compromiso sobre `ADMIN`**: la primera tool de esa clase exige amendment de ADR-010 y de ADR-001.
6. **Definición operativa de "manifiesto"** para el test de superficie (tools declaradas vs. invocables) — decisiva solo bajo la opción C, pero necesaria antes de escribir F16.
7. **Cola de candidatas POST-V0** con canal y clase esperada (§9), incluida la clase futura de `verify_legal_source` (`COMMAND` o `PROPOSAL`).
8. **`list_inbox`**: entra solo si se rechaza la resolución interna del Inbox dentro de `ingest_evidence`.

(3) CONFLICTOS CON ADRs ACCEPTED
- **ADR-001 (Accepted) inv. 3 y val. 7 — cuenta de tools: nueve (literal) vs. ocho (kernel v0.4 §6).** Documentado en §11 con ADR afectado, hecho nuevo, evidencia literal, cuatro impactos y cuatro opciones. **No resuelto.** Por precedencia (kernel §14), mientras ADR-010 esté `Proposed` la superficie normativa sigue siendo la de ADR-001 (nueve), y el test F16 exige nueve.
- **ADR-006 (Accepted) inv. 3 y val. 3 — conflicto secundario de literalidad**: nombran `register_artifact` como punto de validación de `inputs[]`. El invariante sustantivo se conserva; caduca el nombre del punto de aplicación. Requiere prueba sustituta (validación 8) o el amendment debilita ADR-006 de hecho.
- Ningún otro. El hallazgo del spike de Cowork **no** genera conflicto: cambia el mecanismo de plataforma (que ADR-001 ya clasificaba como detalle de implementación) y refuerza la no-exposición como única prohibición efectiva.

(4) POST-V0 / POR VERIFICAR
- **POST-V0:** `verify_legal_source` (fuera por alcance, decisión de los dueños); `RecordProfessionalDetermination` y `WithdrawFact` (canal humano, nombres reservados); `ExtractStatements` (interno; `Statement` no se materializa en V0); `list_inbox`; `export_*`; cualquier tool de clase `ADMIN`; plano administrativo auditado y separado (ADR-002).
- **POR VERIFICAR:** soporte de recursos MCP en el host (alternativa a la resolución interna del Inbox); transporte del sobre y de los errores en la capa de protocolo MCP (detalle de adapter, no altera la clasificación); punto **B-04** del spike de Cowork —si un servidor MCP local alcanza rutas fuera de las carpetas adjuntadas— que no cambia esta superficie pero condiciona la elección de anfitrión.
- **SUPUESTO declarado:** el techo de 12 tools para V1 no está calibrado empíricamente; su función es forzar la conversación al superarlo.
- **RIESGOS declarados propios de este ADR:** erosión incremental; bloqueo de F16 mientras el conflicto siga abierto; opción C mal implementada (si el nombre sobrevive en `tools/list`, la tool es invocable porque el host no filtra); falso "interno" por mala aplicación de REX; checklist convertida en trámite.