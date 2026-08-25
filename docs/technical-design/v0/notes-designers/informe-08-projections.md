# Informe del disenador: 08-projections

Retorno crudo del agente que redacto este documento. Contiene: rutas, decisiones que requieren aprobacion, conflictos y POST-V0 / POR VERIFICAR.

---

(1) RUTAS ESCRITAS
- C:\Users\HITMA\Desktop\legal-workspace\docs\technical-design\v0\08-case-context-projections.md (90 KB; único archivo creado)

(2) DECISIONES QUE REQUIEREN APROBACION (14, todas etiquetadas PROPUESTA DEL TECHNICAL DESIGN en §12.2)
1. `omissions[]` extendido con `omitted_count` / `total_count` / `next_cursor` (aditivo). Sin esto, "falta algo" no distingue entre faltar 2 y faltar 400 hechos.
2. `completeness = PARTIAL` NO emite condicion del catalogo; el pipeline kernel §10 gana segunda entrada `PARTIAL -> LIMITED_CERTAINTY`. Alternativa rechazada: añadir `CONTEXT_PARTIAL` a la lista cerrada.
3. `omissions[].section` como vocabulario cerrado por scope (no texto libre).
4. Seis reglas editoriales R-1..R-6; la de mayor consecuencia es **R-3: el recorte nunca es sesgo optimista** (primero cae lo tranquilizador, nunca lo contradicho/pendiente).
5. Primitiva `emit-or-omit` como unica via de descarte (no existe `drop`/`skip`/`truncate` accesible).
6. Presupuesto medido en **bytes de serializacion canonica, no en tokens** (un tokenizador de proveedor destruiria el golden test y crearia dependencia dura de vendor).
7. Ausencia de `generated_at` en el sobre (reloj de pared rompe el determinismo).
8. `orientation_cursors` en `overview` con `last_human_review_event_seq` = MAX(event_seq) de `ProposalReviewed`, como **ancla canonica** del delta. Es la pieza que hace la reapertura sin memoria y sin que el Core adivine.
9. Vocabulario cerrado `DeltaEntryKind` + mapeo total evento->entrada, con `entity_count` separado de `count` (contar eventos daria "un hecho" donde son dos).
10. `summary` del delta nunca se recorta; `detail` se recorta por el extremo antiguo.
11. `memory.md` **no se materializa** en el user-workspace en V0.
12. Las plantillas nunca renderizan `COMPLETE` como "expediente completo".
13. Valores iniciales de presupuesto por scope (SUPUESTO calibrable: overview 8 KB, facts 32 KB, evidence 16 KB, pending 16 KB, changes_since 24 KB).
14. La no-supresibilidad de `omissions` como candidata a politica de Product Floor (hoy ninguna de las cinco la cubre; si esta cubierta por ADR-004 inv. 2, nivel 1).

(3) CONFLICTOS CON ADRs ACCEPTED
Ninguno. Todo es materializacion de ADR-004 (a) e invariantes 1-3, o extension aditiva sobre puntos que ADR-004 dejo como DECISION PENDIENTE.

Divergencias ADITIVAS con documentos hermanos, declaradas en §12.3 (requieren reconciliacion, no contradiccion):
- `since_event_seq` como cursor admitido: `05` §6.2 solo declara `since_revision`; procede de `03` §0.7 y es imprescindible bajo Modelo B.
- Campos extra en `Omission`: `03` §6.3 y `05` §6.2.
- `orientation_cursors` dentro del `content` de `overview`.
- `search_case.exhaustive` vs `completeness`/`omissions`: dos nombres para la misma obligacion; solo señalado, no se toca `05`.
- `status_filter: ['PROPOSED']` devuelve siempre lista vacia en V0 bajo la materializacion diferida de `02` §5.2 (respuesta correcta, no error). Si esa propuesta no se aprueba, §5.2 de este documento se corrige.
- Dependencia declarada de C1 de `04`: `pending.reconciliation_state` se deriva del log (`ProposalPreservedForReconciliation` sin `FactsCommitted` posterior), compatible con ambas salidas de C1.

(4) POST-V0 / POR VERIFICAR
POST-V0: cache de proyecciones (y retorno de `generated_from_revision`); scope `procedural` y motor procesal/plazos; paginacion real de listas (`next_cursor` es campo propuesto, no mecanismo); proyeccion anotable para audiencia humana ("caratula"); materializacion de `memory.md` en disco y su regimen de acceso; presupuesto adaptativo por modelo; metricas de utilidad de proyecciones.
POR VERIFICAR: margen entre presupuesto en bytes y limite real de contexto del host (HIPOTESIS de correlacion, sin equivalencia afirmada); si el host permite mostrar salida de tools sin mediacion del modelo (heredado ADR-004, condiciona §6.7); numeracion definitiva del catalogo AT-xxx (AT-010 = adversarial 10 del slice); soporte UUIDv7/ULID, del que depende el desempate de R-4; resultado de B-04 del spike de Cowork (no afecta al contrato: las proyecciones son independientes del anfitrion).
Nota de veracidad relevante: la garantia sobre `memory.md` se enuncia como "el modelo puede escribirlo y no significara nada porque nada lo lee", NO como "es inescribible" — apoyada en HECHO VERIFICADO de ESTADO-Y-HALLAZGOS §1.1 (no hay deny por ruta en Cowork).