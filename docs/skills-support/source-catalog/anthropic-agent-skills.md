# Fuente de plataforma — Agent Skills de Anthropic

**Fuente:** [Anthropic Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).
**Checked at:** 2026-08-25. **Status:** `VERIFIED_OFFICIAL` para estructura/documentación; disponibilidad concreta por plan/superficie debe verificarse de nuevo.

## Lo que esta fuente confirma

| Tema | Hallazgo útil para el corpus |
|---|---|
| Forma | Una Skill personalizada es un directorio con `SKILL.md`, frontmatter de `name` y `description`, e instrucciones/recursos opcionales. |
| Descubrimiento | El `description` debe explicar qué hace y cuándo usarla; la metadata se carga antes de las instrucciones. |
| Carga progresiva | Primero metadata, luego `SKILL.md` al activarse y por último recursos/código que se necesiten. |
| Composición | Las Skills pueden aportar método y recursos modulares, en vez de un mega-prompt. |
| Seguridad | Se debe auditar toda Skill/recurso y tratar contenido externo como riesgoso; puede inducir uso de tools o exposición de datos. |
| Superficies | API, Claude Code y Claude.ai tienen modelos de distribución y límites distintos; las Skills no se sincronizan automáticamente entre superficies. |
| Limitaciones | En API, las Skills ejecutan sin red ni instalación de paquetes en tiempo de ejecución; no trasladar supuestos de una superficie a otra. |

## Decisiones de este corpus derivadas de esa fuente

1. No escribir ahora Skills finales: este directorio prepara recursos, métodos y evals bajo demanda.
2. Mantener las futuras Skills pequeñas, con un método específico y documentación profunda fuera de `SKILL.md`.
3. Guardar jurisdicción/fuentes/temporalidad en recursos o Knowledge Packs, no dentro de una metodología universal.
4. Tratar instalación/distribución de Skills como una decisión de plataforma y seguridad, no como enforcement del Legal Core.
5. Auditar cualquier recurso que pueda traer instrucciones, scripts, conectores o llamadas externas.

## Lo que esta fuente no confirma

No confirma que una Skill pueda leer expedientes locales, usar Cowork, tener acceso a MCP local, funcionar en un plan concreto ni preservar confidencialidad por sí sola. Esas preguntas se remiten al inventario de plataforma del repositorio y a pruebas empíricas de la cuenta/equipo objetivo.

