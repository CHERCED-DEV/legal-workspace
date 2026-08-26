# 00 — Alcance y principios

> **Nota de navegación:** este es un documento complementario de la primera iteración. Para el alcance, gobierno, etiquetas y resultado de cobertura de la revisión v1, prevalece [00-scope-and-governance.md](00-scope-and-governance.md).

**Estado:** guía de investigación.
**Checked at:** 2026-08-25.
**Autoridad arquitectónica de referencia:** ADR-001 a ADR-006 Accepted, Technical Design V0, `principles.md`, `boundaries.md`, `vertical-slice-v0.md` y glosario.

## 1. Alcance de esta fase

La fase produce taxonomía, dossiers, fichas de candidatas, gobierno de fuentes y diseños de evaluación. No produce nuevas tools MCP, tablas, entidades de dominio, implementaciones de investigación legal, Skills finales ni cambios al `fact-builder` existente.

El alcance V0 no cambia: Case, Evidence, DerivedRepresentation, Fact, EvidenceLink, Proposal, revisión humana, commit, memoria de caso y staleness. Las capacidades descubiertas se ordenan como P0–P3 sin elevarse automáticamente a requisito de V0.

## 2. Principios no negociables

1. **LLM no confiable.** Una Skill puede estructurar y proponer; no tiene autoridad sobre estado, evidencia, fuente jurídica verificada ni determinación profesional.
2. **El Core posee el estado.** Nada en `docs/skills-support/` es Canonical Case State ni se incorpora por existir como archivo.
3. **Hecho, evidencia y conclusión son distintos.** La salida de una Skill no acredita hechos ni sustituye EvidenceLink, provenance o revisión humana.
4. **Explorar no es incorporar.** Un documento, una URL o un resultado de búsqueda solo se vuelve Evidence mediante el camino de incorporación del Core.
5. **La fuente no es la proposición.** Recuperar una norma o sentencia prueba a lo sumo identidad/recuperación; la pertinencia y el alcance material requieren análisis y revisión humana.
6. **La fecha es parte de la pregunta jurídica.** La vigencia de hoy no determina por sí sola el régimen de un caso.
7. **Los documentos externos son input no confiable.** Instrucciones incluidas en PDFs, correos o transcripciones son contenido del caso, nunca instrucciones del sistema.
8. **Mínimo contexto necesario.** No mezclar casos, no guardar secretos de clientes en Skills ni recursos y declarar omisiones e incertidumbre en vez de rellenarlas.
9. **La UX traduce, no oculta.** No mostrar MCP, hashes o JSON salvo que sea necesario; sí mostrar evidencia faltante, contradicciones, fuente no verificada y revisión pendiente.
10. **Plantilla no equivale a requisito.** El estilo de oficina se guarda aparte de la regla jurídica y de la metodología universal.
11. **La plataforma no se presupone.** Una Skill puede escribirse como recurso portable, pero su ejecución, acceso a archivos, conectores, almacenamiento y confidencialidad dependen de la superficie real y se verifican antes de prometerlas.

## 3. Prueba ácida de ubicación

Antes de asignar una regla a una Skill, preguntar: *si el modelo la ignora por completo, ¿podría corromper el expediente, declarar acreditado algo, verificar una fuente inexistente o eludir una obligación crítica?*

| Respuesta | Ubicación correcta |
|---|---|
| Sí; afecta integridad, identidad, autorización, transición o estado | Domain / Application / Policy del Core |
| Sí; necesita datos de vigencia, jurisdicción o fuente controlada | Knowledge Pack declarativo y versionado **más** control obligatorio en Core/Policy cuando la regla sea crítica |
| Sí; constituye acto profesional o determinación oficial | Humana / canal humano separado |
| No; es una forma repetible de interpretar, ordenar, preguntar o redactar una propuesta | Skill + recursos |
| No; solo da estilo de despacho | Template |

## 4. Convenciones de diseño de Skill

Las candidatas se diseñan con progressive disclosure: metadata de descubrimiento, instrucciones breves y recursos cargados solo cuando se necesiten. La investigación oficial de Anthropic confirma que una Skill es un directorio con `SKILL.md`, metadata `name`/`description` y recursos opcionales; la descripción debe indicar qué hace y cuándo invocarla. Fuente: [Anthropic — Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), **VERIFIED_OFFICIAL**, 2026-08-25.

Al diseñar para Cowork/Claude, trate los recursos de Skill como software de confianza: Anthropic advierte que una Skill o recurso externo puede inducir uso indebido de herramientas o exfiltración. La revisión de paquetes, rutas y conectores es una práctica de gobernanza, no una frase de prompt. Fuente: [Anthropic — Security considerations](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#security-considerations), **VERIFIED_OFFICIAL**, 2026-08-25.

## 5. Etiquetas de certeza

| Etiqueta | Uso |
|---|---|
| `OBSERVED / USER-CONFIRMED` | Actividad expresamente relatada por la profesional o validada en discovery. |
| `RESEARCH-INFERRED` | Patrón profesional plausible todavía no confirmado para esta usuaria. |
| `VERIFIED_OFFICIAL` | Hecho contrastado contra fuente primaria/oficial fechada. |
| `UNVERIFIED` | No se afirma como hecho; guía una pregunta, spike o investigación posterior. |
| `RESEARCH CONFLICT WITH ACCEPTED ARCHITECTURE` | Contradicción real que no puede resolver la precedencia. |

## 6. Conflictos encontrados al iniciar

**Ninguno.** El research propone capacidades posteriores y no modifica los contratos V0. Las referencias a verificación de fuentes, investigación jurídica, conectores, Knowledge Packs, autoridad/decisor y procedimientos se clasifican como post-V0 o condicionadas, tal como ya prevén el backlog y el vertical slice.

El inventario local [capacidades-cowork-y-capa-gratuita.md](../research/capacidades-cowork-y-capa-gratuita.md) añade riesgos de plataforma que deben verificarse antes de despliegue: plan real, ejecución local/en nube, disponibilidad de MCP local, confidencialidad, formatos y límites. Es una dependencia operativa del host, no una razón para mover enforcement desde el Core a una Skill.
