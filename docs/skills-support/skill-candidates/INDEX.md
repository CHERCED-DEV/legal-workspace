# Índice de candidatas de Skill

**Regla de lectura:** una candidata no es una Skill instalada ni un compromiso de implementación. `fact-builder` ya existe y es la única Skill ejercitada de V0; su [ficha](fact-builder.md) no reescribe el archivo vigente en `plugins/despacho/skills/fact-builder/`.

Los códigos de decisión se explican en [README.md](README.md). “Conservar” significa que el método parece diferenciable, no que esté listo para producto.

| Candidata | Decisión visible | Prioridad | Reutilización / riesgo | Depende de | Recomendación |
|---|---|---:|---|---|---|
| [fact-builder](fact-builder.md) | `KEEP` — existente | P0 | alta / alto | Core para revisión y commit | mantener alcance V0; no reescribir en esta fase |
| [intake-structuring](intake-structuring.md) | `KEEP` | P1 | alta / medio | contexto mínimo y revisión humana | diseñar tras baseline |
| [evidence-analysis](evidence-analysis.md) | `KEEP` | P1 | alta / alto | evidencia, locators y propuesta | separar de fact-builder por método/evaluación |
| [legal-document-review](legal-document-review.md) | `KEEP` | P1 | alta / muy alto | conocimiento fechado, contexto y checks del Core | diseñar antes de Skills por tipo documental |
| [legal-research](legal-research.md) | `KEEP` | P1 | alta / muy alto | catálogo de fuentes, Knowledge Pack y retrieval futuro | diseñar metodología y evals antes de runtime |
| [legal-drafting](legal-drafting.md) | `KEEP` | P1 | alta / muy alto | hechos/evidencia, investigación y templates | capacidad transversal, no una Skill por documento |
| [legal-issue-spotting](legal-issue-spotting.md) | `KEEP` | P2 | alta / alto | hechos, contexto y conocimiento fechado | mantener separada de investigación |
| [hearing-analysis](hearing-analysis.md) | `KEEP` | P2 | media / alto | transcripción/locators y contexto | diseñar cuando los adapters estén validados |
| [contradiction-analysis](contradiction-analysis.md) | `KEEP` | P2 | alta / alto | evidencia y locators | método y evals distintos; compone con otras |
| [adversarial-review](adversarial-review.md) | `KEEP` | P2 | media / alto | contexto bilateral y fuentes | usar hallazgos falsables, no pronósticos |
| [legal-opinion](legal-opinion.md) | `MERGE` | P2 | alta / alto | investigación + redacción + humana | no crear Skill propia |
| [client-communication](client-communication.md) | `DEFER` | P2 | alta / medio | contexto aprobado y templates | empezar como patrón revisado |
| [petition-assistance](petition-assistance.md) | `MERGE` | P2 | media / muy alto | workflow + conocimiento + redacción/revisión | no crear Skill documental |
| [demand-assistance](demand-assistance.md) | `MERGE` | P2 | media / muy alto | workflow + conocimiento + redacción/revisión | no crear Skill documental |
| [appeal-assistance](appeal-assistance.md) | `MERGE` | P2 | media / muy alto | estado verificable futuro + conocimiento | no crear Skill documental |
| [tutela-assistance](tutela-assistance.md) | `DEFER` | P3 | media / muy alto | fuentes/jurisprudencia fechadas y revisión | no diseñar como Skill hasta discovery/evals propios |
| conciliación-negociación | `NEEDS_DISCOVERY` | P3 | media / alto | conocimiento + práctica real | no diseñar aún |
| apoyo a decisión de autoridad | `DEFER` | P3 | media / muy alto | contexto B, expediente oficial y autoridad humana | no diseñar antes de discovery específico |
