# 02 — Matriz de frontera: documento ≠ Skill

**Regla:** la tabla clasifica responsabilidades; no autoriza capacidades ni modifica la superficie MCP V0.

| Trabajo | Skill/metodología | Core / Application | Knowledge Pack | Template / recurso | Conector | Humana / gate |
|---|---|---|---|---|---|---|
| Construir hechos | `fact-builder` | incorporar, validar EvidenceLink, Proposal, commit y staleness | — | formato de salida | transcripción/OCR futuros | revisar y decidir |
| Clasificar/contrastar evidencia | `evidence-analysis` | identidad, hashes, locators, cobertura determinista | reglas por materia solo si aplica | matriz probatoria | OCR/transcripción | decidir relevancia/peso |
| Verificar existencia de norma/sentencia | — | retrieval/identity verificable, snapshot y estado de verificación futuros | catálogo de fuentes | protocolo de consulta | web/fuente jurídica | decidir pertinencia |
| Analizar relevancia de autoridad | `legal-research` | provenance de la consulta futura | jurisdicción, fecha, jerarquía | ficha de ratio | buscador jurídico | validar lectura y conclusión |
| Redactar demanda/petición/memorial | `legal-drafting` | contexto de caso y provenance de inputs | requisitos procedimentales vigentes | plantilla de oficina y dossier | Word/export futuro | aprobar, firmar/radicar |
| Revisar una demanda | `legal-document-review` | checks deterministas y presentación de condiciones | requisitos por procedimiento | checklist de tipo documental | lector DOCX/PDF futuro | resolver juicio jurídico |
| Contestar demanda | composición | estado de caso y trazabilidad | carga/forma/procedimiento | workflow de contestación | — | estrategia y admisiones |
| Recursos | composición | estado procesal y cálculo verificable futuro | regla fechada sobre disponibilidad/término/legitimación; no verifica el estado actual | workflow de recurso | consulta de expediente | decidir si procede/firmar |
| Derecho de petición | composición | contexto, fuente y checklist determinista futuro | Constitución art. 23 / Ley 1755 y régimen aplicable | patrón de petición/respuesta | canal/radicación futuro | juicio y envío |
| Audiencia antes/después | `hearing-analysis` | Source/derivación/locators/staleness | reglas de audiencia por área | guion y matriz | transcripción | validar hablante, compromisos y estrategia |
| Contradicciones | `contradiction-analysis` | detectar igualdad/diferencia formal donde proceda | — | taxonomía de contradicciones | — | decidir si es contradicción material |
| Adversarial review | `adversarial-review` | no aplica cambios | derecho/contexto de la causa | checklist falsable | — | valorar riesgo y respuesta |
| Providencia/decisión | composición posterior | expediente, gates y log | procedimiento/rol de autoridad | patrón de motivación | expediente externo futuro | autoridad competente decide |
| Backups, permisos, actualización | — | bootstrap, policy, infraestructura | — | guía operativa | SO/disco | dueños/operador |
| Ética, confidencialidad, conflicto de interés | — | policy/product floor donde sea verificable | reglas deontológicas fechadas | checklist de intake | — | profesional y organización |

## Checks por tipo

| Tipo de check | Ejemplo | Dueño |
|---|---|---|
| Determinista | campo obligatorio, ID existente, hash, fecha que no tiene formato válido, item ajeno al Case | Core/Application |
| De fuente/identidad | la URL/identificador recupera la norma o providencia indicada | adapter/Core futuro + source registry |
| Semántico | una pretensión contradice el relato; una cita no sostiene la proposición | Skill propone hallazgo falsable |
| Jurídico/profesional | procedencia, estrategia, alcance de ratio, valoración probatoria, decisión | humana con Knowledge Pack/fuentes |

## Decisiones explícitas de no duplicación

`petition-assistance`, `demand-assistance` y `appeal-assistance` no sobreviven como Skills autónomas iniciales. Son composiciones de `legal-drafting`, `legal-document-review`, `legal-research`, `fact-builder`/`evidence-analysis`, un workflow específico, un Knowledge Pack fechado y gates humanos. Crear una Skill por nombre de documento duplicaría metodología y volvería opaco qué cambia realmente entre jurisdicciones.
