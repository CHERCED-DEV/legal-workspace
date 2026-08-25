# Informe del disenador: 12-testing

Retorno crudo del agente que redacto este documento. Contiene: rutas, decisiones que requieren aprobacion, conflictos y POST-V0 / POR VERIFICAR.

---

(1) RUTAS ESCRITAS
- `C:/Users/HITMA/Desktop/legal-workspace/docs/technical-design/v0/12-testing-strategy.md` (106 KB, 707 líneas). Único archivo creado; ningún ADR nuevo (el encargo no lo pedía).

(2) DECISIONES QUE REQUIEREN APROBACIÓN (18, listadas en §8.1)
1. Numeración definitiva `AT-001..AT-013` y su correspondencia con los 10 adversariales aprobados del slice — **cierra el `POR VERIFICAR` de `06-human-authorization.md` §9 y §11**. Mapeo: adv.1→AT-001, adv.2→AT-002 (+AT-003, AT-004 como variantes con id propio), adv.3→AT-005, adv.4→AT-011, adv.5→AT-007, adv.6→AT-008, adv.7→AT-006, adv.8→AT-009, adv.10→AT-010, F18→AT-012, kernel §4→AT-013. Coherente con todos los usos ya publicados en kernel §4/§12 y en `06` §9.
2. `F18` asciende a adversarial (`AT-012`); `F9` se disuelve en `FT-006.c` por retiro de `register_artifact`.
3. El test de **expiración** de autorización es `FT-008.c`, sin `AT` propio (su sujeto no es una acción del modelo) — **cierra la fila 5 de `06` §10, que el kernel dejó sin numerar**.
4. Consolidación `FT-001..FT-014` de `F1`–`F18` más las 7 pruebas nuevas de `05` §13. Ningún test del slice se pierde.
5. Prohibición de literales de hash en todo test; se afirman las propiedades `P1`–`P5` de la cadena.
6. Golden inputs (`FX-P2`) con cuatro reglas duras (captura única, sin regeneración automática, entrada y no expectativa, sin truth set).
7. Los tests pueden usar los **bytes** del fixture del benchmark; jamás su `expected/`.
8. `FakeModel` no existe: donde el flujo real recibe salida del modelo, el test usa payload fijo.
9. Test de conformidad de dobles (`FT-012.c`): `InMemoryCaseStore` y SQLite real dan veredictos idénticos.
10. Mecanismo (A) — test de arquitectura sobre el grafo de imports con **mapa de capas declarado** — como verificación normativa; (B) fronteras del compilador como defensa en profundidad; (C) regla de lint **rechazada** como mecanismo único.
11. El import de solo-tipo cuenta como arista prohibida; se cuentan re-exports, `import()` y `require`.
12. Lista negativa de plataforma para `domain` (`fs`, `net`, `http`, `child_process`, `os`, reloj, aleatoriedad), con hashing **excluido** de la prohibición.
13. Sin excepciones inline a la comprobación de dependencias.
14. Seis comprobaciones estructurales `SC-01..SC-06` como gate previo, no como octavo nivel.
15. Cuatro perfiles de ejecución, con los trece `AT` obligatorios en el perfil Completo.
16. Veredicto `OBSERVED` para N7-métricas y evals, distinto de `PASS`/`FAIL`.
17. Procedimiento de cinco pasos ante una métrica que se mueve, con migración obligatoria del defecto determinista a la pirámide.
18. `FT-008` no codifica número de revisión: afirma la relación y registra el modelo (A/B) observado.

(3) CONFLICTOS CON ADRs ACCEPTED
**Ninguno.** El documento no toma decisiones de arquitectura; decide cómo comprobar las ya tomadas. Los cinco conflictos vivos de los hermanos se acatan sin reabrirse, y §8.2 registra su efecto concreto sobre la suite (aritmética de revisiones; 8 vs 9 tools; `ProposalPreservedForReconciliation`; granularidad de `HumanAuthorization`; reingestión con procedencia distinta).

**DECISIONES PENDIENTES que este documento expone** (§8.3): (a) dos listas cerradas de `ErrorCode` vivas a la vez — 14 con prefijo `E_` en `03` §0.3 vs 9 sin prefijo en `05` §4.2: un test de contrato no puede afirmar un código estable con dos listas cerradas; mitigación provisional por constante compartida. (b) El **hueco del adversarial 9** (`verify_legal_source`): los doce ids de los dueños no le dejan slot; su cobertura sobrevive en `FT-013`, pero **PF-004 —el riesgo n.º 1 del dominio— queda probado solo desde la matriz funcional**. Opciones (a) dejarlo con referencia cruzada [recomendada] / (b) añadir `AT-014`. (c) `DEV_STUB` no consumidas; (d) valor de `expires_at`; (e) atomicidad del commit; (f) juez LLM en la adjudicación; (g) segundo fixture held-out.

(4) POST-V0 / POR VERIFICAR
- **POR VERIFICAR:** requisitos del runner cumplidos por el runtime elegido; estabilidad de la API del analizador de TypeScript para el grafo de imports (condiciona el mecanismo A); soporte de UUIDv7; soporte de índices parciales (de él depende `AT-003` en N3); semántica de `rename` con destino existente en Windows; mecanismo de configuración del perfil efectivo (condiciona `AT-013` y PF-005); **punto B-04 del spike de Cowork — RIESGO BLOQUEANTE que ninguna prueba nuestra puede sustituir**.
- **NO verificable en V0, declarado con razón** (§6.5): `Statement`, `DETERMINED`/`ProfessionalDetermination`, `WITHDRAWN`, retiro de `EvidenceLink` (todos `NOT_APPLICABLE` por falta de sujeto/productor); verificación **periódica** de hashes de PF-002 (`NOT_IMPLEMENTED`: no hay job ni planificador); derivación material audio→transcripción con `L0` (`NOT_TESTED`); `UNCERTAIN_FRAGMENT` e `INTEGRATION_ERROR` desde fallo real (`NOT_TESTED`, solo inyección); `authorized_operation` distinto (solo por siembra); confinamiento del host y entrega efectiva del texto de una condición a la usuaria (**fuera de la suite**); umbrales de eval (`INCONCLUSIVE por diseño`).
- **POST-V0:** tests de rendimiento y volumen; concurrencia real; fuzzing de schemas; tests de condiciones sin disparador; use cases diferidos; métricas de fatiga de revisión; segundo fixture held-out; matcher automático de adjudicación.