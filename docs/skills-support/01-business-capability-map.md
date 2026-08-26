# 01 — Mapa de capacidades jurídicas

**Estado:** mapa inicial; no estima frecuencias no observadas.
**Base:** discovery existente + research metodológico. “`OBSERVED / USER-CONFIRMED`” significa que la actividad aparece en el material disponible o fue indicada por la usuaria; no sustituye una validación profesional adicional de frecuencia, alcance o prioridad. “UNKNOWN — preguntar a la profesional” significa que aún no se ha medido para esta profesional.

| ID | Familia funcional | Capacidad | Valor | Evidencia | Rol y alcance | Áreas | Frecuencia estimada | Dependencia del Core | Candidata / dueño | Riesgo | Prioridad | Confianza |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CAP-01 | Intake | Estructurar intake y relato inicial | Convierte relato disperso en agenda verificable | OBSERVED / USER-CONFIRMED | litigante | transversal | UNKNOWN — preguntar a la profesional | lectura de contexto; sin escritura canónica | intake-structuring + humana | medio | P1 | media |
| CAP-02 | Hechos y evidencia | Construir hechos con prueba | Hace revisable la relación hecho–soporte | OBSERVED / USER-CONFIRMED | litigante en V0; decisor solo post-V0/contexto B | transversal | UNKNOWN — preguntar a la profesional | alta: Evidence, Proposal, autorización y commit | fact-builder; Core para commit | alto | P0 | alta |
| CAP-03 | Hechos y evidencia | Analizar evidencia y matriz probatoria | Expone cobertura, huecos y conflictos | OBSERVED / USER-CONFIRMED | litigante; decisor post-V0 | transversal | UNKNOWN — preguntar a la profesional | Evidence/provenance de lectura; no escribe estado | evidence-analysis | alto | P1 | media |
| CAP-04 | Revisión documental | Revisar documentos del expediente | Encuentra defectos, datos faltantes y afirmaciones sin apoyo | OBSERVED / USER-CONFIRMED | litigante | transversal | UNKNOWN — preguntar a la profesional | acceso mínimo a material incorporado | legal-document-review | alto | P1 | media |
| CAP-05 | Investigación y problemas | Identificar problemas a investigar | Formula hipótesis jurídicas sin resolverlas | RESEARCH-INFERRED | litigante; decisor post-V0 | transversal | UNKNOWN — preguntar a la profesional | sin dependencia V0 de escritura | legal-issue-spotting | medio | P2 | media |
| CAP-06 | Investigación y citas | Investigar derecho y jurisprudencia | Recupera, verifica y analiza fuentes | OBSERVED / USER-CONFIRMED | litigante; decisor post-V0 | transversal | UNKNOWN — preguntar a la profesional | futura verificación/control de fuentes; no existe en V0 | legal-research + futuro caso de uso | muy alto | P1 | media |
| CAP-07 | Redacción y revisión | Redactar propuesta jurídica | Produce borrador trazable a hechos y fuentes | OBSERVED / USER-CONFIRMED | litigante; decisor post-V0 | transversal | UNKNOWN — preguntar a la profesional | lectura de hechos/fuentes; ningún commit por la Skill | legal-drafting + workflow/Knowledge Pack declarativo | muy alto | P1 | media |
| CAP-08 | Redacción y revisión | Revisar escrito | Separa checks formales, revisión semántica y juicio humano | OBSERVED / USER-CONFIRMED | litigante | civil, familia, laboral, administrativo | UNKNOWN — preguntar a la profesional | lectura controlada; validaciones duras siguen en Core | legal-document-review | muy alto | P1 | media |
| CAP-09 | Actuaciones procesales | Contestar demanda | Ordena respuestas, excepciones y pruebas sin “invertir” el texto | OBSERVED / USER-CONFIRMED | litigante | civil, familia, laboral, administrativo | UNKNOWN — preguntar a la profesional | futuro estado procesal verificable; no disponible en V0 | composición, no Skill documental propia | muy alto | P2 | media |
| CAP-10 | Actuaciones procesales | Elaborar actuaciones y memoriales | Aplica una intención procesal a un caso | OBSERVED / USER-CONFIRMED | litigante | transversal | UNKNOWN — preguntar a la profesional | futuro estado/canal verificable; no disponible en V0 | legal-drafting + recurso de workflow | alto | P2 | media |
| CAP-11 | Audiencias | Preparar / analizar audiencia | Ordena caso antes y extrae señales después | OBSERVED / USER-CONFIRMED | litigante; decisor post-V0 | transversal | UNKNOWN — preguntar a la profesional | Evidence/derivados en lectura; no decide ni registra acto | hearing-analysis | alto | P2 | media |
| CAP-12 | Contradicciones | Analizar contradicciones | Distingue conflicto formal de tensión semántica | OBSERVED / USER-CONFIRMED | litigante; decisor post-V0 | transversal | UNKNOWN — preguntar a la profesional | lectura de Evidence; contradicción no es entidad V0 | contradiction-analysis | alto | P2 | media |
| CAP-13 | Revisión adversarial | Revisar adversarialmente | Hace falsables vulnerabilidades y asimetrías | OBSERVED / USER-CONFIRMED | litigante; decisor post-V0 | transversal | UNKNOWN — preguntar a la profesional | lectura de contexto; decisión sigue siendo humana | adversarial-review | alto | P2 | media |
| CAP-14 | Derecho de petición | Preparar derecho de petición | Construye/revisa/contesta con contexto normativo | OBSERVED / USER-CONFIRMED | litigante | constitucional, administrativo | UNKNOWN — preguntar a la profesional | fuentes/reglas fechadas; sin verificación jurídica V0 | composición + Knowledge Pack declarativo Colombia | muy alto | P2 | media |
| CAP-15 | Actuaciones procesales | Preparar recursos | Identifica información necesaria, no decide disponibilidad | OBSERVED / USER-CONFIRMED | litigante | transversal | UNKNOWN — preguntar a la profesional | regla fechada + futuro registro oficial de estado/plazo | composición + Knowledge Pack declarativo | muy alto | P2 | media |
| CAP-16 | Conceptos jurídicos | Preparar concepto jurídico | Distingue pregunta, fuentes, alternativas y recomendación | OBSERVED / USER-CONFIRMED | litigante | transversal | UNKNOWN — preguntar a la profesional | futura investigación/verificación; no ejecutable en V0 | legal-research + legal-drafting; no Skill separada | alto | P2 | media |
| CAP-17 | Conciliación | Conciliación/negociación | Separa posiciones, intereses, riesgos y no negociables | RESEARCH-INFERRED | litigante | transversal | UNKNOWN — preguntar a la profesional | ninguna adicional en V0; reglas/decisión humana | DEFER; método específico por validar | alto | P3 | baja |
| CAP-18 | Decisión de autoridad | Apoyo a decisiones de autoridad | Prepara antecedentes, posiciones y borrador, sin decidir | OBSERVED / USER-CONFIRMED | decisor, solo post-V0/contexto B | policivo/administrativo | UNKNOWN — preguntar a la profesional | modelo de expediente, permisos y gates futuros | composición posterior y gate humano | muy alto | P3 | baja |
| CAP-19 | Comunicación con cliente | Comunicar al cliente | Traduce estado y próximos pasos sin alterar significado | OBSERVED / USER-CONFIRMED | litigante | transversal | UNKNOWN — preguntar a la profesional | lectura mínima de contexto; no canal externo en V0 | recurso de tono/template, no Skill inicial | medio | P2 | media |
| CAP-20 | Ética, calidad y confidencialidad | Gobernanza de calidad y confidencialidad | Evita que una salida se presente con garantías inexistentes | RESEARCH-INFERRED | todos los roles; decisor post-V0 | transversal | UNKNOWN — preguntar a la profesional | alta: aislamiento, permisos, autorización y auditoría | Core/policy/humana; no Skill | muy alto | P0 | alta |

### Notas de priorización

- **Frecuencia y tiempo:** no se inventan números. Cada fila conserva “UNKNOWN — preguntar a la profesional” hasta que discovery produzca una estimación verificable.
- **P0:** solo nombra lo necesario para el kernel/V0 vigente (fact-builder y sus límites), no añade trabajo V0.
- **P1:** siguiente ola, cuando haya baseline, fuentes y gates suficientes.
- **P2/P3:** capacidad valiosa pero dependiente de Knowledge Packs declarativos, de contexto de autoridad aún no levantado o de descubrimiento adicional.
- **Límite del Knowledge Pack:** puede aportar reglas y fuentes fechadas; nunca sustituye validaciones, autorizaciones, transiciones o control de estado del Core.

### Campos complementarios de evaluación v1

Los valores cualitativos de riesgo son **RESEARCH_INFERRED** hasta que la profesional los valide. Frecuencia y costo de tiempo permanecen en UNKNOWN para no fabricar datos.

| ID | frequency_source | time_cost | error_risk | legal_risk | knowledge_dependency | human_boundary | open_questions |
|---|---|---|---|---|---|---|---|
| CAP-01 | UNKNOWN — entrevista pendiente | UNKNOWN | medio | medio | ninguno si solo ordena relato | aceptar encargo, prioridad y alcance | Q1, Q2 |
| CAP-02 | UNKNOWN — uso V0 no mide frecuencia profesional | UNKNOWN | alto | alto | prueba/procedimiento por área | revisión, autorización y commit | Q2, Q8 |
| CAP-03 | UNKNOWN — entrevista pendiente | UNKNOWN | alto | alto | evidencia, regla probatoria y fecha | relevancia, peso y consecuencia | Q2, Q8, Q10 |
| CAP-04 | UNKNOWN — entrevista pendiente | UNKNOWN | alto | alto | tipo documental y procedimiento | corrección y uso final | Q3, Q11 |
| CAP-05 | UNKNOWN — entrevista pendiente | UNKNOWN | medio | alto | jurisdicción, materia y fecha | qué investigar y cómo encuadrarlo | Q4 |
| CAP-06 | UNKNOWN — entrevista pendiente | UNKNOWN | alto | muy alto | fuentes, jurisprudencia, transición y territorio | pertinencia, lectura y cita final | Q4, Q5 |
| CAP-07 | UNKNOWN — entrevista pendiente | UNKNOWN | alto | muy alto | requisitos por producto, área y fecha | afirmaciones, estrategia, firma y presentación | Q3, Q11 |
| CAP-08 | UNKNOWN — entrevista pendiente | UNKNOWN | alto | muy alto | checklist procedimental y fuente fechada | juicio jurídico y aprobación | Q3, Q11 |
| CAP-09 | UNKNOWN — entrevista pendiente | UNKNOWN | alto | muy alto | procedimiento, estado y plazo verificable | admisiones, excepciones y estrategia | Q3, Q10 |
| CAP-10 | UNKNOWN — entrevista pendiente | UNKNOWN | alto | alto | actuación, canal, fuente y fecha | intención, firma y envío | Q3, Q5 |
| CAP-11 | UNKNOWN — entrevista pendiente | UNKNOWN | alto | alto | audiencia, transcripción y regla especial | preguntas, estrategia y compromisos | Q9 |
| CAP-12 | UNKNOWN — entrevista pendiente | UNKNOWN | alto | alto | efecto jurídico por área | materialidad y respuesta | Q10 |
| CAP-13 | UNKNOWN — entrevista pendiente | UNKNOWN | alto | alto | derecho adverso y procedimiento | aceptación de riesgo y respuesta | Q11 |
| CAP-14 | UNKNOWN — entrevista pendiente | UNKNOWN | alto | muy alto | Ley 1755, transparencia, datos y sector | modalidad, reserva, traslado, firma y envío | Q5, Q13 |
| CAP-15 | UNKNOWN — entrevista pendiente | UNKNOWN | alto | muy alto | regla fechada más estado procesal | procedencia, agravios y firma | Q3, Q5 |
| CAP-16 | UNKNOWN — entrevista pendiente | UNKNOWN | alto | alto | derecho sustantivo, temporalidad y fuentes | recomendación y grado de certeza | Q4 |
| CAP-17 | UNKNOWN — entrevista pendiente | UNKNOWN | alto | alto | materia, mecanismo y regla especial | negociación, oferta, aceptación y acuerdo | Q15 |
| CAP-18 | UNKNOWN — discovery de autoridad pendiente | UNKNOWN | muy alto | muy alto | procedimiento, territorio y expediente oficial | competencia, prueba, decisión y firma | Q6 |
| CAP-19 | UNKNOWN — entrevista pendiente | UNKNOWN | medio | alto | confidencialidad, reserva y estado autorizado | revelación, compromiso y envío | Q12 |
| CAP-20 | UNKNOWN — evaluación de práctica pendiente | UNKNOWN | muy alto | muy alto | ética, datos, secreto y políticas | conflicto, riesgo crítico y autorización | Q2, Q6 |
