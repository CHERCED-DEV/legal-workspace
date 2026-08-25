# Alineación con la arquitectura y conflictos

**Resultado del research:** `NO RESEARCH CONFLICT WITH ACCEPTED ARCHITECTURE` al 2026-08-25.

El corpus no modifica entidades, tools, transiciones ni permisos. Clasifica capacidades como post-V0, Knowledge Pack, recurso, connector o decisión humana. Cuando una candidata requiera una nueva tool, entidad, garantía o transición, debe abrirse como decisión de arquitectura; no se resuelve agregando texto a una Skill.

## Reglas vigentes que este corpus usa

- La superficie MCP V0 tiene **ocho** tools; `register_artifact` es interno a `propose_facts`.
- La autorización humana es por `ProposalItem`, vinculada a `item_content_hash`; la revisión humana no es MCP.
- `event_seq` y `case_revision` son relojes distintos; no usar `seq == revision` en ejemplos/evals.
- `verify_legal_source` no existe en V0; Knowledge Packs no se cargan en el slice.
- Contradicciones, gaps, issues, términos y estado procesal no son entidades canónicas V0.

## Residuos documentales heredados

La verificación interna del repositorio registra documentos que todavía reflejan diseños previos (por ejemplo, nueve tools, aritmética de revisión antigua o shapes anteriores). Son **drift heredado**, no conflicto generado por este corpus. Si un research necesita citar esos documentos, debe aplicar la precedencia de ADRs Accepted/enmiendas y kernel, etiquetar la discrepancia y no propagarla.

## Riesgo de plataforma separado

El inventario de Cowork/capa gratuita abre preguntas sobre plan, nube/local, MCP local, confidencialidad y formatos. No es un conflicto con el principio Accepted de que el Core es la frontera de confianza: es una condición de despliegue que puede impedir usar un host concreto. Hasta validarlo, ninguna candidata promete que una Skill pueda leer archivos locales, usar conectores o proteger datos por sí sola.

## Cuándo abrir un conflicto real

Use exactamente la etiqueta `RESEARCH CONFLICT WITH ACCEPTED ARCHITECTURE` únicamente si una conclusión de investigación exige de manera inevitable que una regla Accepted sea falsa o insuficiente, por ejemplo: una garantía de evidencia no es realizable con las fronteras aprobadas. Debe incluir evidencia, documento afectado, impacto y opciones; no debe proponer un cambio directamente dentro del corpus.
