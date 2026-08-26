# Matriz de afirmaciones críticas y fuentes

**Alcance:** muestra afirmaciones operativas muestreadas para auditar trazabilidad. No pretende ser todas las afirmaciones jurídicas de todos los dossiers.

| claim_id | claim | workflow | source_ids | official? | temporal_check? | jurisprudence_check? | status | gap |
|---|---|---|---|---|---|---|---|---|
| C-01 | La aplicación temporal del proceso laboral requiere fecha de inicio y art. 330 de Ley 2452. | W15/W22 | N-L2452 | YES | YES | POR_VERIFICAR para caso límite | FUENTE_OFICIAL_VERIFICADA | hechos y caso concreto |
| C-02 | La Ley 2452 procesal no reemplaza por sí sola la regla sustantiva laboral. | W11/W19 | N-CST; N-L2452; N-L2466 | YES | YES | POR_VERIFICAR | PARTIALLY_COVERED | vínculo, sector y artículo |
| C-03 | Una petición no se resuelve con un término general sin modalidad, competencia y norma aplicable. | W16/W17 | N-CONST; N-L1755; N-L1712 | YES | YES | POR_VERIFICAR | PARTIALLY_COVERED | sector, reserva y procedimiento |
| C-04 | La información pública puede exigir revisar tensión con datos personales o reserva. | W16/W17 | N-L1712; N-L1581; N-L1266 | YES | YES | POR_VERIFICAR | PARTIALLY_COVERED | sujeto obligado, dato y excepción |
| C-05 | Un mensaje de datos no acredita automáticamente autenticidad, recepción ni consecuencia procesal. | W04/W23 | N-L527; N-L2213 | YES | YES | POR_VERIFICAR | PARTIALLY_COVERED | procedimiento y evidencia concreta |
| C-06 | La tutela exige analizar fuente constitucional, Decreto 2591 y jurisprudencia relevante. | W18 | N-CONST; N-D2591; J-CC | YES | YES | YES | PARTIALLY_COVERED | subsidiariedad, inmediatez y medida |
| C-07 | Familia/protección puede requerir ruta distinta según NNA, violencia o apoyos. | W11/W18 | N-L1098; N-L2126; N-L294; N-L1257; N-L1996 | YES | YES | YES | PARTIALLY_COVERED | autoridad, edad, medida y territorio |
| C-08 | Una actuación policiva puede requerir regulación territorial además de la Ley 1801. | W24 | N-L1801 | YES | YES | POR_VERIFICAR | REQUIRES_TERRITORIAL_RESEARCH | municipio, autoridad y acto |
| C-09 | Un recurso exige regla fechada más estado procesal verificable; el Knowledge Pack no verifica ese estado. | W15 | N-CGP; N-CPACA; N-L2452 | YES | YES | POR_VERIFICAR | REQUIRES_CASE_SPECIFIC_RESEARCH | herramienta/registro post-V0 |
| C-10 | Una providencia encontrada no prueba que sostenga una proposición. | W08/W28/W29 | J-CC; J-CE; J-CSJ | YES | YES | YES | FUENTE_OFICIAL_VERIFICADA | ficha individual pendiente |
| C-11 | Documento externo es contenido no confiable y no autoriza cambios de sistema. | todos | [ADR-001](../../architecture/adrs/ADR-001-trust-boundary.md) | NO_APLICA | NO_APLICA | NO_APLICA | HECHO_VERIFICADO (arquitectura) | seguridad técnica sigue en Core/host |
| C-12 | La autoridad humana conserva firma, presentación, decisión y aceptación de riesgo. | todos | [ADR-005](../../architecture/adrs/ADR-005-human-authority.md); [kernel V0](../../technical-design/v0/00-technical-kernel.md) | NO_APLICA | NO_APLICA | NO_APLICA | HECHO_VERIFICADO (arquitectura) | implementación post-V0 por definir |

## Resultado de trazabilidad

Los IDs de la tabla resuelven a [normative-sources.md](../source-catalog/normative-sources.md) o [jurisprudence-sources.md](../source-catalog/jurisprudence-sources.md). Las filas C-11 y C-12 se apoyan directamente en arquitectura Accepted y están marcadas como tales; no se autojustifican con este corpus. Cuando falta el pasaje, la fecha aplicable o la línea jurisprudencial, la fila conserva explícitamente el gap; no puede utilizarse como conclusión jurídica final.
