# Informe del disenador: 15-16

Retorno crudo del agente que redacto este documento. Contiene: rutas, decisiones que requieren aprobacion, conflictos y POST-V0 / POR VERIFICAR.

---

(1) RUTAS ESCRITAS

- `C:/Users/HITMA/Desktop/legal-workspace/docs/technical-design/v0/15-product-floor-proposal.md` (47 KB)
- `C:/Users/HITMA/Desktop/legal-workspace/docs/technical-design/v0/16-open-implementation-decisions.md` (43 KB)
- `C:/Users/HITMA/Desktop/legal-workspace/docs/architecture/adrs/ADR-007-persistence-strategy-v0.md` (33 KB, Estado = Proposed, secciones exactas verificadas)

(2) DECISIONES QUE REQUIEREN APROBACIÓN

De `15`:
1. Aprobar las cinco políticas PF-001..PF-005 tal como se enuncian (hoy `PROPOSED`).
2. **PF-006 (auditoría): ¿entra como sexta?** Tres opciones en §6.4; **recomendación (b) = sí entra**, porque el coste marginal en mecanismo es cero (append-only + trigger + hash-chain ya existen por ADR-004) y sin ella el validador de Client Config no tiene regla contra la que rechazar una poda del log.
3. Si se elige (a): retirar formalmente la política 5 del anexo de `principles.md`, con razón escrita.
4. Criterio operativo de "endurecer" (§7.2) y secuencia de validación de Client Config en seis pasos (§7.3) — `PROPUESTA DEL TECHNICAL DESIGN`.
5. PF-004 sin `AT` propio: opción (a) referencia cruzada desde PF-004 a `FT-013` (recomendada) vs (b) crear `AT-014`.
6. Registrar la candidata 2 (no-supresibilidad de `omissions[]`, `08`) como conocida y **no** promovida.

De `16` (bloqueantes, todos decisión de los dueños salvo donde se indica):
7. **OD-01** modelo de revisión A vs B (amendment ADR-004/ADR-005) — recomendado B.
8. **OD-02** 8 vs 9 tools (amendment ADR-001 inv. 3) — recomendado 8.
9. **OD-03** binding SQLite — recomendado `better-sqlite3` tras el puerto; Technical Design propone, dueños ratifican (riesgo de producto en Windows).
10. **OD-04** aprobar ADR-008 (autorización por item; enmienda ADR-005 §2).
11. **OD-05** mecanismo de configuración del perfil efectivo — **detectada al evaluar, no encargada**; bloquea `AT-013` y el test de PF-005.

De ADR-007: binding concreto (=OD-03); rechazar vs advertir ante ubicación no local (recomendado rechazar); más 9 preguntas pendientes listadas en el ADR.

(3) CONFLICTOS CON ADRs ACCEPTED

**Ninguno nuevo.** No abrí ningún bloque `CONFLICTO CON ADR ACCEPTED`. Los tres documentos registran y remiten a los ya declarados por los documentos hermanos, sin resolverlos: ADR-001 inv. 3 (8 vs 9 tools, `01` §9.1), ADR-004 (c)/inv. 5 + ADR-005 inv. 9–10 (aritmética de revisión, `01` §9.2 / `04` C3), ADR-005 §2 (granularidad de `HumanAuthorization`, `04` C2), ADR-004 (b)1 (`ProposalPreservedForReconciliation`, `04` C1), ADR-004 inv. 5 vs ADR-006 inv. 7 (reingestión con procedencia distinta, `04` C4). ADR-007 mantiene el esquema **neutral** ante el amendment `event_seq`/`case_revision` y no fija ningún `CHECK` que decida por los dueños.

Divergencia de nivel (no conflicto entre ADRs): kernel §12 (nivel 2) vs anexo de `principles.md` (nivel 3) sobre la política de auditoría — tratada en `15` §5.3 y §6 para que no se resuelva por precedencia silenciosa.

(4) POST-V0 / POR VERIFICAR

POR VERIFICAR / NOT_IMPLEMENTED declarados:
- Mecanismo de configuración del perfil efectivo (`production|development|test` y forma de Client Config) — condiciona `AT-013` y el test de PF-005.
- Verificación **periódica** de hashes de PF-002: `NOT_IMPLEMENTED` en V0 (no hay job ni planificador); solo bajo demanda.
- PF-004 se cumple hoy **por ausencia de superficie**; su test de transición no tiene sujeto en V0.
- Punto **B-04** del spike de Cowork (`INCONCLUSIVE`): no bloquea Fase 1, sí bloquea comprometerse con Cowork como host de producción.
- Ocho `POR VERIFICAR` del binding (FK por conexión, índices parciales, copia consistente, integridad, FTS5, `synchronous` bajo WAL, `rename` con destino existente en Windows, PK de texto): mientras no se verifiquen, la defensa que dependa de ellos **no se cuenta como activa**.
- Prebuilds nativos `win32-x64` / `win32-arm64` para el piso de Node elegido.
- Detección fiable de carpeta sincronizada en Windows: `NOT_TESTED`, sin API documentada universal.
- Capacidad real de timestamps del proveedor de transcripción (condiciona `INV-D-33` y ADR-003 inv. 7 para audio).
- ADR-009 y ADR-010 **no existen en disco** (verificado): no puede afirmarse que no contradigan nada.
- Nomenclatura: el encargo dice `FixtureTranscriptionProvider`; el nombre canónico del corpus (`12` §2.9) es **`FixtureDerivationProvider`** — usé el canónico y lo hice explícito para no crear un segundo nombre.

POST-V0 mencionado sin diseñar: deduplicación física de Sources con refcount, caché de proyecciones, PostgreSQL, stemmer español y búsqueda vectorial, anclaje externo del hash-cabeza, `verify_legal_source` con cotejo determinista, gates adicionales por configuración (p. ej. doble revisión), materialización de `Statement`.