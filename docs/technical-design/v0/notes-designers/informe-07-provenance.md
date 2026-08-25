# Informe del disenador: 07-provenance

Retorno crudo del agente que redacto este documento. Contiene: rutas, decisiones que requieren aprobacion, conflictos y POST-V0 / POR VERIFICAR.

---

(1) RUTAS ESCRITAS
- `C:/Users/HITMA/Desktop/legal-workspace/docs/technical-design/v0/07-provenance-and-locators.md` (757 líneas)
- `C:/Users/HITMA/Desktop/legal-workspace/docs/architecture/adrs/ADR-011-evidence-locator-strategy.md` (195 líneas, Estado = Proposed, secciones exactas)

(2) DECISIONES QUE REQUIEREN APROBACIÓN
1. Regla de doble coordenada: todo fragmento y segmento porta coordenada de cita (original) y de recuperación (representación). §1.3
2. Tres columnas aditivas en `derived_representations`: `generated_at`, `recipe_hash`, `derived_from_content_hash` (tautológica en V0; hace aditivos los derivados encadenados). §2.2
3. Interfaz consolidada de `EvidenceFragment` con `original_locator` explícito y campo `v` de versión de contrato. §3.1
4. Convenciones fijadas: intervalos semiabiertos, páginas cerradas 1-based, offsets en puntos de código sobre NFC, milisegundos enteros, contexto de 32 caracteres. §3.2
5. `prefix`/`suffix` **obligatorios** en `TEXT_QUOTE` (en `02` §2.5 eran opcionales). §3.4
6. INV-L-04: `TIME_RANGE` y `PAGE_RANGE` prohibidos como selectores sobre un derivado. §3.3
7. Criterio de admisión de adapter: proveedor de transcripción sin marcas de tiempo referidas al original **no admisible en V0**. §3.6 — RIESGO alto declarado.
8. Sin bounding boxes en V0. §3.9
9. Subconjunto W3C adoptado (TextQuoteSelector §4.2.4, TextPositionSelector §4.2.5, idea de refinamiento §4.2.9) + **no reclamar conformidad**. §4
10. Re-anclaje como mapeo aditivo, nunca mutación del fragmento commiteado; matriz de 4 resultados; tratamiento del fragmento no re-anclable. §5.4–§5.6
11. Retención sin excepciones de versiones referenciadas (incluidos links `RETIRED` y `artifact_inputs`). §5.2
12. Nombres prohibidos en schema y plantillas (`verified`/`authentic`/`validated`/`trusted`); verbo "verificar" nunca aplicado a un `Source`. §6.3–§6.4
13. Re-hash en lectura por umbral de tamaño + verificación periódica completa. §1.5

(3) CONFLICTOS CON ADRs ACCEPTED
Ninguno. Todo estrecha ADR-003 inv. 7/8 y ADR-006 inv. 3/5/6/7 sin relajarlos. El único choque potencial (proveedor sin timestamps sobre el original) se resuelve restringiendo el adapter, no el invariante.

DIVERGENCIAS ENTRE DOCUMENTOS HERMANOS (nivel 2 vs nivel 2, con reconciliación propuesta, §9.2):
- D1: monotonía de `version` — `02` §3.4 dice por `(source_id, recipe)`; `04` §3.2 impone `UQ(source_id, kind, version)`. Propuesta: conservar `04`, añadir `recipe_hash`, corregir una frase de `02`.
- D2: nombres de selector — `02` §2.5 usa `CHAR_RANGE`/`QUOTE`; `04` §3.3 usa `TEXT_POSITION`/`TEXT_QUOTE`. Propuesta: adoptar los de `04`.
- D3: `04` §2.6/§3.2 menciona `bbox` como ejemplo de `original_locator`. Propuesta: marcarlo POST-V0 o retirarlo.
- D4: `02` §2.5 no nombra `original_locator`, que `04` §3.3 exige `NOT NULL`. Propuesta: nombrarlo (hecho en §3.1).

(4) POST-V0 / POR VERIFICAR / DECISIÓN PENDIENTE
POST-V0: bounding boxes y toda coordenada espacial · derivados de segundo orden encadenados · ejecución del re-anclaje y sus dos eventos · métodos de re-anclaje distintos de la coincidencia exacta única · alineamiento por palabra · expurgo de versiones sin referencias · export en formato W3C · locator portado por `Statement` · deduplicación de blobs.
DECISIÓN PENDIENTE: (a) `FragmentReanchored`/`FragmentReanchorFailed` frente a la lista cerrada de eventos del kernel §8.1; (b) si el fragmento no re-anclable reutiliza `UNCERTAIN_FRAGMENT` con `reason` o entra como código propio en `11-ux-condition-catalog.md` (recomendación: reutilizar); (c) umbral de re-hash; (d) política de expurgo.
POR VERIFICAR: numeración de las secciones W3C de los selectores **no** adoptados (solo §4.2.4/§4.2.5/§4.2.9 están verificadas) · correspondencia literal entre la unidad de offset fijada y la redacción de §4.2.5 · estabilidad de la enumeración de páginas del extractor PDF · qué proveedores entregan timestamps por segmento sobre el original (`experiments/transcription-spike/`) · suficiencia de 32 caracteres de contexto (fixture de `13-synthetic-benchmark.md`) · coste real del digest en lectura · que la unidad de offset sea la que devuelven realmente extractores y proveedor.