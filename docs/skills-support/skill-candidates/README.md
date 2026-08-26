# Fichas de candidatas de Skill

Cada ficha describe una capacidad posible; no instala una Skill ni autoriza cambios en el Core. Las fichas históricas más breves usan secciones agrupadas para evitar repetir información. Su correspondencia con la [plantilla v1](candidate-card-template.md) es:

| Campo de la plantilla v1 | Sección agrupada en fichas existentes |
|---|---|
| Purpose, Repeatable task, Trigger, Do not invoke when | Propósito; Tarea repetible; Cuándo usarla y cuándo no |
| Inputs, Canonical context, External research, Output | Entradas y salidas; Referencias y recursos |
| Method, Resources | Método; Referencias y recursos necesarios |
| Core dependencies, MCP dependencies, Knowledge dependencies, Temporal dependencies | Dependencias del Core y MCP; Paquete de conocimiento |
| Human review boundary, Hard prohibitions | Límite de revisión humana; Prohibiciones estrictas |
| Composition, Example requests | Composición, ejemplo y estructura esperada |
| Failure modes, Evals | Fallos previsibles y evaluación |
| Priority, Recommendation | Prioridad y recomendación |

Las fichas nuevas usan los campos de forma explícita. Antes de crear una Skill real se debe completar la [plantilla](candidate-card-template.md) con evidencia de práctica, una línea de fuentes fechadas y resultados de evaluación; no basta con copiar esta documentación.

## Estados de decisión

| Código | Significado en español |
|---|---|
| `KEEP` | conservar como candidata diferenciada; no significa implementarla ya. |
| `MERGE` | resolver como composición de capacidades existentes. |
| `SPLIT` | separar solo si hay métodos y evaluaciones distintos. |
| `REJECT` | no crear como Skill. |
| `DEFER` | aplazar hasta tener información, fuentes o arquitectura suficientes. |
| `NEEDS_DISCOVERY` | primero observar y validar el trabajo profesional real. |
