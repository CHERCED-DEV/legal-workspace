# Informe del disenador: 01-system

Retorno crudo del agente que redacto este documento. Contiene: rutas, decisiones que requieren aprobacion, conflictos y POST-V0 / POR VERIFICAR.

---

**(1) RUTAS ESCRITAS**

`C:/Users/HITMA/Desktop/legal-workspace/docs/technical-design/v0/01-system-design.md` (único archivo creado; ninguno modificado)

**(2) DECISIONES TÉCNICAS QUE REQUIEREN APROBACIÓN** (tabla completa en §10 del documento)

1. Regla de dependencias verificada con **test de arquitectura en CI** ya en V0 (kernel §13 la deja "para más adelante"; sin mecanismo, la regla queda declarada y no verificada justo cuando se erosiona).
2. **Una transacción por use case mutador**, con todas sus mutaciones, sus eventos y el hash-chain dentro de ella. Sin esto, la biyección mutación↔evento depende de que nada falle a mitad.
3. **Bytes antes de transacción canónica** en `IngestEvidence`: se acepta blob huérfano (basura recolectable), no referencia canónica a bytes inexistentes (corrupción). Recolección de huérfanos POST-V0.
4. **Tool Invocation Log fuera de la transacción canónica**, escrito también —y sobre todo— en rechazos; su fallo nunca revierte estado canónico.
5. `DerivedRepresentation` en `PENDING` **como parte del payload de `EvidenceIncorporated`**, no como mutación aparte: la lista cerrada de eventos v0 no admite una para ella y crearla sería cambio de contrato.
6. Rechazos de dominio/aplicación como **resultados tipados**, no excepciones (excepciones solo para fallos de infraestructura).
7. **Sin framework grande** con *triggers medibles* de reevaluación (superficie HTTP real, más de un transporte, composition root ilegible de una pasada, más de un autor concurrente del Core, observabilidad estandarizada). Lo que se aprueba aquí son los triggers; la decisión de fondo ya es del kernel §13.
8. `configuration_version` como **tercera versión** del release, y compatibilidad declarada en el manifest (`min_schema`/`max_schema`).
9. **Migraciones hash-chain-preserving**: pueden cambiar la representación física, no los bytes canónicos sobre los que se computó `event_hash`; re-anclar la cadena es cambio de contrato de auditoría, no efecto colateral. Las migraciones no emiten eventos del Case Event Log ni avanzan `case_revision` (`principal_type = SYSTEM`, `provenance_kind = SYSTEM`).
10. **Solo-lectura no escribe en ninguna parte**, `Exports/` incluido.
11. El Core **no lee `Working/`**; y **un export no es un Source**: reutilizar material salido por `Exports/` exige reincorporarlo por `Inbox/` con su propia provenance.
12. `BackupPort.verify()` exige **restauración a ubicación aislada + comparación**; `status = VERIFIED` es la única entrada válida al gate de migración.
13. El backup incluye las **DerivedRepresentations referenciadas por fragmentos**: regenerable ≠ prescindible; excluirlas deja Sources íntegros y cadenas de provenance rotas.
14. El mensaje de fallo de integridad debe emitirlo una **superficie que el producto controle**, no el chat: el fallo ocurre antes de cualquier invocación de tool. Redacción propuesta en §7.5, etiquetada SUPUESTO; no es condición del catálogo v0 sino mensaje de producto.

**(3) CONFLICTOS DETECTADOS** (bloques completos en §9)

- **CONFLICTO CON ADR ACCEPTED — ADR-001 inv. 3 (y validación 7), con efecto en ADR-006 inv. 3 y en `vertical-slice-v0.md` F16/F9.** El kernel §6 retira `register_artifact` y deja **8 tools**; ADR-001 Accepted dice literalmente **nueve**. Por precedencia manda el ADR. Documentado con impacto de ambas salidas y tres opciones; la tabla de flujo §4.3 está escrita con el registro interno del artifact dentro de la transacción de `ProposeFacts`, señalado como dependiente de esta decisión.
- **CONFLICTO CON ADR ACCEPTED — ADR-004 (b)1 y ADR-005 inv. 9–10.** Aritmética de revisión del acto de revisión: kernel §5.2 propone que `ProposalReviewed` no avance `case_revision` y declara que **no se aplica** hasta aprobación, pero el kernel §7 ya presenta la tabla con "no". Contradicción interna del propio kernel. El documento aplica el **Modelo A** (ADRs Accepted) en la tabla numerada y muestra en columna aparte los valores del **Modelo B**.
- **Divergencias menores registradas** (§9.3): (a) `completeness` de dos valores en kernel §9 frente a tres en ADR-004 Accepted; (b) el Product Floor del kernel §12 **no** contiene la política de inmutabilidad de la auditoría que sí lista el anexo de `principles.md` — por precedencia gana el kernel y el resultado es que hoy ninguna política del piso cubre esa garantía: debe decidirse explícitamente, no por precedencia silenciosa. (c) `actor_* → principal_* + provenance_kind` no es conflicto: normalización ya aprobada, aplicada literalmente en todo el documento.

**(4) POST-V0 / POR VERIFICAR**

- **POST-V0** (§11): arquitectura distribuida, multi-máquina, sync, colas, orquestador de jobs, PostgreSQL, búsqueda vectorial, caché de proyecciones; actualizador, firma de código, canales de release, telemetría, licenciamiento, multi-tenant; multi-agente, subagentes, Legal Auditor; conectores externos y su mecánica de incorporación; Knowledge Pack de Colombia, jurisprudencia, plazos, motor procesal, `verify_legal_source`; `Statement` y las demás entidades reservadas; `DETERMINED`/`WITHDRAWN` y sus use cases diferidos; plano administrativo; **export/portabilidad del expediente** (distinguido explícitamente de backup/restore, que sí es V0); proveedor concreto de backup, programación, retención, incrementales, cifrado y restauración parcial; recolección de blobs huérfanos.
- **POR VERIFICAR**: conjunto exacto de flags del compilador TypeScript (no consulté fuente oficial en esta fase; no lo etiqueté como hecho verificado); versión concreta de Node LTS; soporte real de UUIDv7 en Node LTS (alternativa ULID); granularidad de permisos y garantías de sandbox/filesystem de Cowork Desktop; soporte de elicitation modo URL en el host; si el host permite mostrar salida de tools sin mediación del modelo; proveedor de transcripción y semántica de sus timestamps.
- **DECISIONES PENDIENTES vivas y no resueltas aquí**: transporte del canal de autorización humana; mecanismo de enforcement del perímetro; aprobación parcial confirmada por los dueños; topología de backup (local-only vs segunda ubicación — decisión de negocio, no técnica); si el fallo de integridad merece condición propia del catálogo; retención/poda del Tool Invocation Log; anclaje del hash-cabeza fuera del workspace.