# Informe del disenador: 14-repo

Retorno crudo del agente que redacto este documento. Contiene: rutas, decisiones que requieren aprobacion, conflictos y POST-V0 / POR VERIFICAR.

---

(1) RUTAS ESCRITAS
- `C:/Users/HITMA/Desktop/legal-workspace/docs/technical-design/v0/14-repository-layout.md` (71.5 KB, único archivo creado; ningún ADR nuevo — el encargo no producía decisión de nivel ADR: el layout es materialización de kernel §13 y `01` §2.3, no una decisión de arquitectura nueva)

(2) DECISIONES QUE REQUIEREN APROBACIÓN (§9.3 del documento, 15)
1. `src/bootstrap/` como composition root + plano administrativo; sumidero del grafo (nadie lo importa); sin lógica de negocio. Cubre la omisión más grave de la estructura orientativa: `01` §5.4 y el FAIL-TO-START de kernel §4 no tenían dónde vivir.
2. `src/human-authorization/` como segundo driving adapter con carpeta propia, hermano de `src/mcp/` (ADR-005 no aparecía en el árbol: afirmaba un solo canal de entrada).
3. `src/application/contracts/` como única superficie importable por adapters de entrada, con re-exportación —no duplicación— de primitivos de `domain/shared`.
4. `domain/evidence-link/` como agregado propio (ampliación sobre `case/evidence/fact/provenance`).
5. `plugin/skills/` fuera de `src/` y sin ningún archivo de código (hace estructural la prueba de `01` §2.2 precisión 2).
6. Seis reglas mecánicas M1–M6 (aristas+re-exports, cero terceros en domain, E/S solo en infrastructure+bootstrap, reloj/identidad solo en `platform`, env solo en `bootstrap/config`, prosa de usuaria solo en `templates`).
7. Barrels solo en `application/contracts/`; imports dinámicos prohibidos en `src/`.
8. Los imports solo de tipo cuentan como arista de dependencia.
9. `tests/architecture/` como quinto bucket; tests en árbol separado espejando `src/`, no co-locados (razón: el producto sellado se hashea, `01` §7.2).
10. `benchmark/` como carpeta propia fuera de `tests/` (mide tasas, no aprueba builds).
11. Prefijo obligatorio del identificador del corpus (`AT-`, `T-UX-`, `ADV-`, `FSC-`, `M`) en el nombre de archivo de todo test identificado.
12. Los cuatro sufijos que se ganan su lugar (`.port.ts`, `.adapter.ts`, `.use-case.ts`, `.test.ts`) y rechazo explícito de `.service/.manager/.helper/.util/.entity/.dto/.impl`.
13. Nombres prohibidos (`utils/`, `helpers/`, `common/`, `misc/`, `core/`, `lib/`, `manager`, `service`), con `domain/shared/` como excepción única y sin comportamiento.
14. Promoción de spikes solo por reescritura bajo `src/`, nunca por `git mv` (E4).
15. Test de higiene del repositorio en `tests/architecture/` en vez de hook local.
Propuesta adicional dentro de §2.5: `ToolInvocationLogPort` declarado por Application, implementado en `infrastructure/persistence`, inyectado por `bootstrap` en el adapter MCP (evita un segundo escritor del private state contra ADR-002 inv. 2).

(3) CONFLICTOS CON ADRs ACCEPTED
Ninguno. Ninguna decisión del layout contradice ADR-001…ADR-006. Los conflictos vivos ya registrados en `ESTADO-Y-HALLAZGOS-CRITICOS` §6 (8 vs 9 tools, aritmética de revisión, `completeness`, alcance del Product Floor) no se reabren: ninguno depende del layout.
Sí quedan registradas cuatro TENSIONES internas del Technical Design (§9.2), declaradas y no disimuladas:
- T1: `01` §2.2 agrupa `skills/`+`presentation/` bajo `legal-plugin`; aquí se separan físicamente (amparado en `01` §2.1: la frontera no implica jerarquía de carpetas; la frontera se conserva íntegra en el mapa §8.1).
- T2: la regla "mcp no importa domain" es comprobable sobre RUTAS; tipos originados en `domain/shared` alcanzan `mcp` re-exportados por `contracts/`. La garantía es acoplamiento nulo a la implementación, no aislamiento nominal de tipos.
- T3: `ports/` anidado en `application/` frente al listado hermano de `01` §2.2.
- T4: quién declara `ToolInvocationLogPort`.

(4) POST-V0 / POR VERIFICAR
POST-V0: separación en paquetes o repos (inventario de coste en §8.2, no se ejecuta); superficie propia del plano administrativo (CLI de soporte e identidad de quien repara — `bootstrap/admin/` reserva posición, no diseña); carpeta de Knowledge Packs (viven en el root `configuration/`, no en el repo); locales más allá de `es-CO`; conectores externos; telemetría/licenciamiento/administración empresarial.
POR VERIFICAR (6): (1) mecanismo concreto de extracción del grafo de imports para el test de arquitectura; (2) si existe regla de lint que exprese la tabla de aristas incluyendo re-exports transitivos e imports de tipo; (3) si las referencias de proyecto del compilador admiten granularidad de subdirectorio (`infrastructure → application/ports` sí, `→ use-cases` no); (4) flags exactos del compilador y versión de Node (heredado de `01` §5.1); (5) si la regla "un agregado no importa otro agregado" se comprueba mecánicamente en V0; (6) heurística concreta de M6 y su tasa de falsos positivos.
RIESGOS declarados en el texto: si el checker de §3.5 no se escribe, el documento entrega convención y no garantía (`01` §2.3 exige declararlo así); M6 y el test de higiene detectan el descuido, no la evasión deliberada (misma honestidad que kernel §8.3); el trigger vivo de separación es el punto B-04 del spike de Cowork, empírico y abierto.