# Índice de candidatas de Skill

**Regla de lectura:** una candidata no es una Skill instalada ni un compromiso de implementación. `fact-builder` ya existe y es la única Skill ejercitada de V0; sus fichas no lo reescriben.

| Candidate | Status | Priority | Reuse | Risk | Depends on | Recommendation |
|---|---|---:|---|---|---|---|
| [fact-builder](../../../plugins/despacho/skills/fact-builder/SKILL.md) | KEEP (existente) | P0 | alta | alto | Core para modo B/revisión | mantener; no reescribir en esta fase |
| [intake-structuring](intake-structuring.md) | KEEP | P1 | alta | medio | contexto mínimo, gate humano | diseñar tras baseline |
| [evidence-analysis](evidence-analysis.md) | KEEP | P1 | alta | alto | Evidence/locators/Proposal | separar de fact-builder por matriz y cobertura |
| [legal-document-review](legal-document-review.md) | KEEP | P1 | alta | muy alto | Knowledge Pack, contexto, checks Core | diseñar antes de Skills por tipo documental |
| [legal-research](legal-research.md) | KEEP | P1 | alta | muy alto | source registry, Knowledge Pack, retrieval futuro | diseñar metodología y evals antes de runtime |
| [legal-drafting](legal-drafting.md) | KEEP | P1 | alta | muy alto | facts/evidence, research, templates | Skill transversal; no demanda/petición aisladas |
| [legal-issue-spotting](legal-issue-spotting.md) | KEEP | P2 | alta | alto | facts/context/Knowledge Pack | mantener separada de research |
| [hearing-analysis](hearing-analysis.md) | KEEP | P2 | media | alto | transcripción/locators, contexto | diseñar cuando adapters estén validados |
| [contradiction-analysis](contradiction-analysis.md) | KEEP | P2 | alta | alto | Evidence/locators | separada por método/evals, compone con otras |
| [adversarial-review](adversarial-review.md) | KEEP | P2 | media | alto | contexto bilateral, sources | diseñar como hallazgos falsables |
| legal-opinion | MERGE | P2 | alta | alto | research + drafting + humana | no crear Skill propia |
| petition/demand/appeal-assistance | MERGE | P2 | media | muy alto | workflow + Knowledge Pack + drafting/review | no crear Skills documentales |
| client-communication | DEFER | P2 | alta | medio | contexto aprobado, templates | resource/pattern primero |
| conciliation-negotiation | NEEDS_DISCOVERY | P3 | media | alto | Knowledge Pack + práctica real | no diseñar aún |
| authority-decision-support | DEFER | P3 | media | muy alto | contexto B, expediente oficial, human authority | no diseñar antes de discovery específico |
