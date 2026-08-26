# Mapas de dependencia jurídica

Estos mapas no convierten una cadena normativa en respuesta automática. Muestran qué debe verificarse antes de afirmar una regla en un workflow: fuente principal, regla especial, reformas, reglamentación, control constitucional, jurisprudencia, transición y territorio.

## Estados

| Estado | Significado |
|---|---|
| `NATIONAL_RULE_VERIFIED` | **Fuente nacional base identificada**; no significa que la regla esté verificada para el caso concreto. |
| `TERRITORIAL_RULE_REQUIRED` | **Se necesita regla territorial:** la materia puede depender de autoridad, municipio o territorio específico. |
| `TERRITORIAL_RULE_NOT_YET_LOADED` | **Regla territorial aún no registrada** en el corpus. |
| `COVERAGE_GAP` | **Brecha de cobertura:** falta una relación normativa o jurisprudencial material. |
| `REQUIRES_CASE_SPECIFIC_RESEARCH` | **Requiere estudio del caso:** depende de hechos, fecha, rol, acto o expediente concreto. |

## Regla especial antes que general

| Campo | Pregunta |
|---|---|
| general_rule | ¿Qué norma general se usaría inicialmente? |
| special_rule | ¿Existe régimen especial por materia, sujeto, procedimiento o territorio? |
| priority_basis | ¿Qué fuente y pasaje justifican la prioridad? |
| scope | ¿A qué persona, acto, materia o procedimiento aplica? |
| temporal_basis | ¿Qué fecha, reforma o transición decide la versión? |

Nunca aplicar CGP, CPACA o una regla nacional como sustituto de una regla especial sin recorrer estas preguntas.

## Mapas disponibles

- [Petición, transparencia y datos](petition-transparency-data.md)
- [Procedimiento, digitalización y evidencia](procedure-digital-evidence.md)
- [Familia, protección y apoyos](family-protection-supports.md)
- [Laboral y transición](labor-and-transition.md)
- [Policivo y territorialidad](police-and-territoriality.md)
- [Constitucionalidad y tratados](constitutional-block-and-treaties.md)
