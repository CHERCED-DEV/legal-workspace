# ADR-011 — Estrategia de locators de evidencia y subconjunto adoptado del W3C Web Annotation Data Model

## Estado

Proposed

## Contexto

ADR-003 (Accepted) fijó en su invariante 7 que **todo `EvidenceLink` ancla a un fragmento verificable de una `Evidence`** —página, offsets o timestamps **referidos al original**—, nunca al documento entero ni a un derivado sin referencia a su `Source`. ADR-006 (Accepted) lo reforzó desde el lado de la incorporación: el fragmento **siempre resuelve a un `Source`** (inv. 5) y el hash prueba **integridad desde la ingestión, no autenticidad** (inv. 6).

Ninguno de los dos dice **cómo** se expresa esa ancla. El corpus previo la escribía como `fragment { source_version_hash, selector }` (`vertical-slice-v0.md`, *Persisted state*), una forma que deja tres preguntas sin responder y que ya obligó a refinamientos dispersos en tres documentos técnicos:

1. **Contra qué representación se resolvió el selector.** Un solo hash no dice si es el original o una transcripción, y por tanto no permite comprobar que la cadena termina en el `Source`, que es lo que ADR-003 inv. 7 exige.
2. **Qué formas de selector existen y cómo se añaden.** `02-domain-model.md` §2.5 y `04-persistence-model.md` §3.3 llegaron a nombres distintos para la misma unión (`CHAR_RANGE`/`QUOTE` frente a `TEXT_POSITION`/`TEXT_QUOTE`), señal de que la unión no estaba contratada en ningún sitio con autoridad.
3. **Qué ocurre al regenerar un derivado.** El corpus registra que *"una versión referenciada por fragmentos no se descarta"* y que *"el re-anclaje es explícito y auditado, nunca silencioso"*, sin definir qué es re-anclar ni qué pasa con un fragmento que no puede re-anclarse.

A esto se suma un hecho externo disponible y una tentación asociada. **HECHO VERIFICADO** (kernel técnico v0.4 §1 / ADR-003; fuente: *W3C Web Annotation Data Model*, Recomendación W3C de **23 de febrero de 2017**): el estándar define `TextQuoteSelector` (§4.2.4), `TextPositionSelector` (§4.2.5) y la relación de refinamiento `refinedBy` (§4.2.9). Tres documentos técnicos lo citan ya como *"vocabulario candidato, sin dependencia"*. La tentación es adoptarlo entero por prestigio de estándar; el problema es que necesitamos alrededor del 10 % de su superficie y el resto trae un modelo de identidad (IRI), una serialización (JSON-LD) y un vocabulario de anotación cuya semántica no es la del anclaje probatorio.

Y un hecho de plataforma que condiciona el material temporal: **`POR VERIFICAR`** (`boundaries.md` §5; `experiments/transcription-spike/`) si el proveedor de transcripción entrega marcas de tiempo referidas a la línea de tiempo del original. Si no las entrega, un ancla de audio solo podría expresarse sobre el derivado — y eso **rompería ADR-003 inv. 7**.

El diseño técnico completo —cadena de resolución, metadatos de derivados, contrato de selectores, protocolo de regeneración y redacción obligatoria— está en `docs/technical-design/v0/07-provenance-and-locators.md`. Este ADR registra las decisiones y sus consecuencias.

Lo que este ADR **no** reabre: el modelo epistémico y sus invariantes (ADR-003), la frontera de incorporación (ADR-006), la frontera de confianza (ADR-001), el perímetro del case store (ADR-002), la semántica de revisión (ADR-004) ni la autoridad humana (ADR-005).

## Decision

### 1. El ancla es un value object con **tres partes obligatorias**, y siempre desciende hasta el original

`EvidenceFragment` = `{ v, source_id, anchored_in, derivation_id?, representation_hash, selectors[], original_locator }`.

- `source_id` es **obligatorio siempre**, con independencia de que la cita pase o no por un derivado.
- `representation_hash` identifica **la representación exacta** contra la que el selector es válido: o bien `sources.content_hash`, o bien `derived_representations.content_hash` de una versión concreta.
- `selectors[]` nunca está vacío: **no existe el ancla al material entero**.

### 2. Regla de doble coordenada

Todo fragmento porta **dos** coordenadas:

- **Coordenada de cita** (`original_locator`): siempre en el plano del **original**. Es la que se muestra, se audita y sobrevive a cualquier regeneración.
- **Coordenada de recuperación** (`selectors[]`): sobre la representación que nombra `representation_hash`. Es la que permite extraer el texto exacto.

La coordenada de cita es **la más fina que el medio soporta de forma estable**: rango de caracteres para texto plano, **página** para documentos paginados, **milisegundos** para audio y vídeo. Guardar solo la derivada rompería ADR-003 inv. 7 en la primera regeneración; guardar solo la original impediría extraer y verificar el texto.

### 3. Unión de selectores **cerrada en V0** y extensible con fricción

`TEXT_POSITION` · `TEXT_QUOTE` · `PAGE_RANGE` · `TIME_RANGE` (nombres de `04-persistence-model.md` §3.3, alineados con el vocabulario W3C). `OriginalLocator`: `ORIGINAL_CHAR_RANGE` · `ORIGINAL_PAGE` · `ORIGINAL_TIME_RANGE`.

Extensibilidad gobernada: campo `v` de versión de contrato en el propio value object; **fail-closed** ante `kind` o `v` desconocidos (el fragmento no se resuelve, no se interpreta a medias); alta de un `kind` nuevo solo con caso real documentado y ADR, resolutor antes que emisor, y **sin migrar los fragmentos existentes**, que son estado canónico append-only.

### 4. `TIME_RANGE` y `PAGE_RANGE` **jamás** son selectores sobre un derivado

```text
anchored_in = 'DERIVED_REPRESENTATION'  ⇒  ∀ s ∈ selectors : s.kind ∈ { TEXT_POSITION, TEXT_QUOTE }
```

Tiempo y página son coordenadas del original. Un `TIME_RANGE` sobre una transcripción estaría midiendo la línea de tiempo del **derivado**: exactamente lo que ADR-003 inv. 7 prohíbe. Cuando se cita un audio a través de su transcripción, el tiempo vive en `original_locator` y el texto en `selectors[]`.

**Consecuencia sobre el adapter, no sobre el invariante:** un proveedor de transcripción que no entregue marcas de tiempo referidas al original con granularidad al menos de segmento **no es admisible para V0**. Cuando el hecho externo choca con un invariante Accepted, se restringe el proveedor.

### 5. Para texto se exigen **los dos** selectores, con funciones distintas

`TEXT_POSITION` **y** `TEXT_QUOTE` (con `prefix` y `suffix` **obligatorios**, 32 caracteres propuestos):

- **Dentro** de una representación fija: la posición recupera, la cita **comprueba**. Como `representation_hash` ya garantiza bytes idénticos, una discrepancia entre ambas no es deriva de contenido sino corrupción o bug ⇒ **fallo duro, jamás re-búsqueda silenciosa**.
- **Entre versiones**: la posición es inútil (los offsets se desplazan) y la cita es el **único mecanismo de re-anclaje** posible.

### 6. Subconjunto adoptado del estándar W3C — y no-reclamación de conformidad

**Se adopta:** la forma y semántica de `TextQuoteSelector` (`exact`/`prefix`/`suffix`), la de `TextPositionSelector` (`start`/`end`, `end` exclusivo) y **la idea** de refinamiento, materializada como contención y orden en un array en vez de anidamiento `refinedBy`.

**No se adopta:** la serialización JSON-LD y `@context`; la identificación por IRI/URI; el modelo `Annotation`/`Body`/`Target` (nuestro `EvidenceLink` ya es la anotación, con polaridad, justificación y provenance que el estándar no tiene); los demás selectores (`FragmentSelector`, `CssSelector`, `XPathSelector`, `DataPositionSelector`, `SvgSelector`, `RangeSelector`); los `State` (nuestro `representation_hash` es más fuerte: identidad de contenido, no de instante); el vocabulario de `motivation`; y la semántica de selectores alternativos, porque nuestra composición es **conjuntiva** y elegir sería adivinar.

**No se reclama conformidad** con el estándar en documentación, UI ni export. Se usa su vocabulario como **convención de nombres**. El mapeo completo entre nuestros nombres y los suyos está en `07-provenance-and-locators.md` §4.4.

### 7. Metadatos obligatorios de todo derivado

Parent `source_id` (no nulo, inmutable), `recipe.tool`, `recipe.version`, `recipe.params`, instante de generación, `content_hash` cuando `state = READY`, y `ProvenanceRecord` embebido (`provenance_kind = AI_DERIVATION`, `principal_type ∈ {AI, SYSTEM}`). Se añaden tres columnas **aditivas**: `generated_at`, `recipe_hash` y `derived_from_content_hash` — esta última tautológica en V0 (siempre igual al hash del Source) y presente para que los derivados encadenados sean después un cambio aditivo y no una reconstrucción inferida de la cadena de derivación de material probatorio.

### 8. Regeneración: nueva versión, retención, y re-anclaje **aditivo**

- Regenerar produce **versión nueva**; nunca sobrescribe (blobs write-once; PF-002).
- **Retención:** una versión referenciada por cualquier fragmento persistido —incluidos los de links `RETIRED`— o por un `artifact_input`, **no se descarta**. Retención de la versión completa: fila, blob y segmentos.
- **El re-anclaje no reescribe el fragmento de un link ya commiteado.** Añade un registro de correspondencia entre la versión N y la N+1, con provenance y evento. Motivo: el fragmento vive dentro de un `EvidenceLink` commiteado bajo `HumanAuthorization` (ADR-005); reescribirlo cambiaría sin acto humano nuevo aquello que una persona aprobó — y con retención no hay ninguna necesidad técnica de mutar.
- **Fragmento no re-anclable** (cita ambigua o ausente en la versión nueva): el link **sigue siendo válido** contra la versión retenida; no se retira, no cambia el estatus del `Fact`, y se emite una condición dirigida a la profesional. Nunca en silencio.
- El **handle** `fragment_ref` sí se invalida al regenerar (`05-mcp-contract.md` §6.5); el **ancla persistida** no. Son objetos distintos: uno es un token efímero de recuperación, el otro es estado canónico.

### 9. Sin bounding boxes en V0

No hay coordenadas espaciales en el locator. Exigirían fijar sistema de coordenadas, origen, unidades, rotación y caja de referencia — convenciones que hoy no podemos verificar y que difieren por extractor —, no añaden verificabilidad a la cita (que se hace por página y texto), y serían una coordenada derivada del render con apariencia de coordenada del original. `POST-V0`.

### 10. Integridad ≠ autenticidad, reflejado en schema y mensajes

El hash prueba que los bytes son los mismos **desde la incorporación**; no prueba autenticidad, autoría, fecha, no-fabricación previa ni admisibilidad. Consecuencias contratadas: no existe —ni se añadirá sin ADR— columna `authentic`, `verified`, `validated` o `trusted` sobre `sources`, `evidence` o `derived_representations`; `declared_origin` conserva el adjetivo; `state = READY` no se renombra a `VERIFIED`; el verbo "verificar" no se aplica nunca a un `Source` en la superficie; y toda presentación de texto derivado dice que es derivado y que **el original sigue siendo la fuente**.

## Invariantes derivados

1. **El fragmento siempre resuelve a un `Source`.** `source_id` no nulo en todo `EvidenceFragment`, con o sin derivado intermedio.
2. **Nunca se ancla al material entero.** `selectors[]` no vacío; construir un fragmento sin selector falla en el Domain.
3. **Coherencia de anclaje.** `anchored_in='SOURCE'` ⇒ sin `derivation_id` y `representation_hash = Source.content_hash`; `anchored_in='DERIVED_REPRESENTATION'` ⇒ con `derivation_id`, `representation_hash` de esa versión, y la derivación referencia el mismo `source_id`.
4. **Ningún selector `TIME_RANGE` o `PAGE_RANGE` sobre un derivado.**
5. **`original_locator` siempre presente y siempre en el plano del original**; cuando el ancla es directa al `Source`, coincide con la coordenada del selector.
6. **Todo fragmento de texto lleva `TEXT_QUOTE` con contexto** (`prefix` y `suffix` no vacíos).
7. **Fallo duro ante discrepancia posición↔cita** con `representation_hash` ya verificado: no se re-busca, no se reubica.
8. **Fail-closed ante `kind` o `v` desconocidos.**
9. **Retención:** ninguna operación descarta una versión de derivado referenciada por un fragmento persistido o por un `artifact_input`, con independencia del estado del link.
10. **El re-anclaje no muta un `EvidenceFragment` commiteado**, y ningún resultado de re-anclaje retira un link, cambia el estatus de un `Fact` ni consume una autorización.
11. **El locator no contiene rutas de filesystem ni URLs** (refuerza ADR-002 inv. 3).
12. **Ningún nombre de columna, campo de API ni mensaje afirma autenticidad, verificación o validación de un `Source`.**

## Consecuencias positivas

- **ADR-003 inv. 7 pasa de enunciado a regla comprobable.** "Referido al original" deja de ser una intención de redacción y se convierte en un campo obligatorio (`original_locator`) más un invariante estructural (nº 4) que un test puede violar deliberadamente.
- **Las citas sobreviven a la regeneración sin que nadie las reinterprete.** La combinación retención + re-anclaje aditivo elimina la categoría entera de bug "la cita apunta ahora a otro sitio".
- **La fabricación de anclas por el modelo es estructuralmente imposible**, no solo desaconsejada: el handle es opaco y verificable por re-resolución, y un `kind` inventado falla cerrado.
- **La deriva silenciosa se vuelve detectable.** El caso `ORIGINAL_COORDINATE_DRIFT` —dos transcripciones coinciden en el texto pero discrepan en el minuto— sería invisible sin la doble coordenada; con ella es una condición dirigida a la profesional.
- **Se toma del estándar exactamente lo que resuelve un problema real** (re-anclaje por cita con contexto) sin importar identidad IRI, JSON-LD ni un modelo de anotación con semántica ajena. El coste de exportar al estándar más adelante queda reducido a un adapter de serialización, sin tocar el Domain.
- **Cierra tres divergencias abiertas entre documentos técnicos** (nombres de selector, monotonía de `version`, ausencia de `original_locator` en la interfaz del Domain) en un único lugar con autoridad.
- **La distinción integridad/autenticidad deja de depender del cuidado de quien redacte**: se sostiene en nombres de columna y plantillas revisables.

## Consecuencias negativas

- **El almacenamiento de derivados crece de forma monótona.** La retención sin excepciones implica que ninguna versión referenciada se poda; la política de expurgo de versiones sin referencias queda pendiente y vive en el plano administrativo.
- **Cada fragmento de texto es más caro:** dos selectores, contexto de 64 caracteres y una coordenada redundante cuando el ancla es directa al `Source`. Se acepta a cambio de re-anclaje posible y lectura sin condicionales.
- **El criterio de admisión del proveedor de transcripción puede excluir opciones adecuadas en todo lo demás**, encarecer el slice o retrasarlo. Es una restricción real derivada de un invariante Accepted, y su impacto solo se conocerá al medir.
- **Sin bounding boxes**, la experiencia de citar un documento escaneado es menos precisa visualmente que la de productos que resaltan la región exacta.
- **Un fragmento no re-anclable deja al expediente citando una versión antigua**, y hay que explicárselo a la profesional. Es peor UX que re-anclar automáticamente, y es la opción correcta.
- **El re-anclaje exige dos tipos de evento nuevos**, contra una lista de eventos que V0 declara cerrada: es deuda de contrato declarada, no resuelta.
- **Fricción deliberada para extender la unión de selectores**: añadir un `kind` exige ADR. Ralentiza adrede algo que debería ser lento.

## Alternativas consideradas

1. **Adoptar el Web Annotation Data Model completo.** Rechazada: se necesita ~10 % de su superficie; el resto aporta IRI, JSON-LD, `Annotation`/`Body`/`Target` y `motivation`, con semántica que duplicaría `EvidenceLink` y su polaridad. Además, adoptar dos selectores y presentarse como conforme sería una afirmación sin respaldo.
2. **No usar el estándar en absoluto e inventar nombres propios.** Rechazada: `exact`/`prefix`/`suffix` y `start`/`end` con la semántica del estándar son exactamente lo que se necesita, están probados por uso masivo, y usar nombres propios encarecería sin beneficio cualquier export futuro.
3. **Locator opaco específico del proveedor** (guardar el identificador de segmento que devuelve el transcriptor). Rechazada: ancla la prueba a un artefacto del proveedor —es literalmente lo que `13-synthetic-benchmark.md` §11.4 prohíbe con `seg_hint`—, muere al cambiar de proveedor y no resuelve al original.
4. **Anclar solo al derivado y considerar el original un adjunto.** Rechazada: contradice ADR-003 inv. 7 y ADR-006 inv. 5; convertiría una transcripción automática en la prueba.
5. **Anclar solo por offsets de carácter, sin cita.** Rechazada: hace imposible el re-anclaje y deja la deriva indetectable.
6. **Anclar solo por cita, sin posición.** Rechazada: pierde la recuperación exacta, obliga a re-buscar en cada lectura y no distingue dos apariciones idénticas dentro de la misma representación.
7. **Re-anclaje mutando el fragmento del link.** Rechazada: cambiaría sin acto humano nuevo el contenido de un link commiteado bajo autorización (ADR-005) y destruiría la evidencia de qué se aprobó.
8. **Descartar la versión antigua tras regenerar y re-anclar todo automáticamente.** Rechazada: convierte cada regeneración en un evento de riesgo probatorio, y ante un fragmento no re-anclable no habría a qué volver.
9. **Incluir bounding boxes en V0.** Rechazada: exigiría fijar convenciones no verificables hoy y añade precisión visual, no verificabilidad.
10. **Promover `EvidenceFragment` a entidad con identidad y tabla.** Rechazada: la regla de entrada al dominio (ADR-003) lo impide —sin lifecycle, sin invariantes propios— y crearía identidad referenciable desde otros sitios. Decisión ya tomada en `02-domain-model.md` §1.1 y `04-persistence-model.md` §2.2.

## Riesgos

1. **`RIESGO` alto — el proveedor de transcripción no entrega marcas de tiempo sobre el original.** Consecuencia: el material de audio no sería anclable conforme a ADR-003 inv. 7 con ningún proveedor disponible, y el slice tendría que reducir alcance o cambiar de proveedor. Estado: `POR VERIFICAR` en `experiments/transcription-spike/`. **No se mitiga relajando el invariante.**
2. **`RIESGO` medio — el contexto de 32 caracteres resulta insuficiente en el corpus real**, dejando citas ambiguas al re-anclar. Mitigación: es un parámetro, no una decisión estructural; se mide en el fixture antes de fijarlo.
3. **`RIESGO` medio — crecimiento de almacenamiento por retención**, hasta que exista política de expurgo. Mitigación: V0 no regenera, así que el riesgo no se materializa dentro del slice.
4. **`RIESGO` medio — granularidad de la coordenada del original limitada al segmento.** Una cita de audio es exacta al segmento, no a la palabra. Está declarado como límite, no oculto; el alineamiento por palabra es `HIPÓTESIS` no verificada y ninguna regla depende de él.
5. **`RIESGO` medio — deriva de redacción.** La distinción integridad/autenticidad se erosiona con facilidad en textos de producto y de marketing. Mitigación: nombres prohibidos en schema y revisión de plantillas como prueba (L-12), no confianza en el cuidado individual.
6. **`RIESGO` bajo — la unidad de offset fijada (puntos de código sobre NFC) no coincide con la que devuelven los extractores**, produciendo anclas desplazadas. Mitigación: la comprobación posición↔cita lo convierte en fallo detectable en la primera lectura, no en una cita silenciosamente equivocada.
7. **`RIESGO` bajo — normalización asimétrica** entre escritura y lectura del texto derivado (`04-persistence-model.md` §6.2, decisión pendiente sobre la `ñ`). Mismo mecanismo de detección que el anterior.
8. **`RIESGO` bajo — coste del re-hash en lectura** sobre material grande. Mitigación propuesta: umbral de tamaño más verificación periódica completa. **No se afirma ningún número de rendimiento**: está `POR VERIFICAR`.

## Validación / pruebas necesarias

Identificadores provisionales, a consolidar en `docs/technical-design/v0/12-testing-strategy.md`. Detalle en `07-provenance-and-locators.md` §8.

1. **L-01** — fragmento con `selectors = []` ⇒ rechazo en construcción (invariante 2).
2. **L-02** — fragmento sobre transcripción con selector `TIME_RANGE` ⇒ rechazo (invariante 4).
3. **L-03 / F5** — cita de audio: el `original_locator` devuelto está en la línea de tiempo del original y es coherente con la duración del `Source`.
4. **L-04 / F18** — `fragment_ref` fabricado por el modelo ⇒ `UNKNOWN_REFERENCE` y traza en el Tool Invocation Log.
5. **L-05 / AT-011** — blob de derivado alterado ⇒ mismatch de hash ⇒ no se sirve contenido; degradación a solo lectura declarada.
6. **L-06** — `TEXT_POSITION` desplazado con `representation_hash` intacto ⇒ discrepancia con `TEXT_QUOTE` ⇒ fallo duro sin re-búsqueda (invariante 7).
7. **L-07** — cita duplicada que `prefix`/`suffix` no desambigua ⇒ el fragmento no se construye.
8. **L-08** — `original_locator` recomputado desde los segmentos ≠ el persistido ⇒ `VALIDATION_FAILED` (invariante 5).
9. **L-09** — `kind` o `v` desconocidos ⇒ fail-closed (invariante 8).
10. **L-10** — intento de descartar una versión de derivado referenciada por un link `RETIRED` ⇒ rechazo (invariante 9).
11. **L-11** — locator con ruta o URL en cualquier campo ⇒ rechazo de validación (invariante 11).
12. **L-12** — revisión de nombres: ninguna columna, campo de API ni plantilla contiene `verified`/`authentic`/`validated` sobre material incorporado (invariante 12).
13. **L-13 `POST-V0`** — re-anclaje: los cuatro resultados posibles producen el efecto contratado y ninguno muta el fragmento existente (invariantes 10 y 11).

**Validación documental adicional:** las citas al estándar W3C se limitan a §4.2.4, §4.2.5 y §4.2.9 (Recomendación de 23-feb-2017); cualquier afirmación sobre otras secciones debe verificarse contra la fuente antes de escribirse.

## Preguntas pendientes

1. **Eventos de re-anclaje.** `FragmentReanchored` y `FragmentReanchorFailed` frente a la lista cerrada de eventos de V0 (kernel §8.1): ¿se añaden ahora al contrato aunque no tengan productor, como ya se hizo con `FactWithdrawn`, o se difieren?
2. **Condición del fragmento no re-anclable:** ¿reutilizar `UNCERTAIN_FRAGMENT` con un `reason`, o crear código propio en el catálogo UX? Recomendación: reutilizar.
3. **Longitud de contexto** de `prefix`/`suffix`: 32 es propuesta; el valor se fija tras medir en el fixture.
4. **Umbral de tamaño** para el re-hash en lectura, y frecuencia de la verificación periódica completa.
5. **Política de expurgo** de versiones de derivado sin referencias: ¿existe, y quién la ejecuta desde el plano administrativo?
6. **Unidad de offset** frente a lo que devuelvan realmente extractores y proveedor: si divergen, ¿se normaliza en el adapter o se cambia la convención?
7. **Derivados de segundo orden:** ¿se admiten POST-V0 encadenados, o la normalización se mantiene siempre dentro de la receta de una única derivación?
8. **Alcance de la retención frente al archivado de expedientes:** cuando exista archivo o exportación de un Case, ¿viajan todas las versiones retenidas o solo las referenciadas?

## Relaciones con otros ADRs

- **ADR-003 (Accepted) — modelo epistémico.** Este ADR **implementa** su invariante 7 (ancla verificable referida al original) y su invariante 8 (Source inmutable, derivado que nunca sustituye y siempre referencia). No lo modifica ni lo relaja. Mantiene además la decisión de que `EvidenceFragment` **no es entidad**.
- **ADR-006 (Accepted) — frontera de incorporación.** Implementa su invariante 5 (el fragmento siempre resuelve a un `Source`), su invariante 6 (integridad ≠ autenticidad, §10) y sostiene su invariante 3 mediante la retención de versiones consumidas por artifacts.
- **ADR-002 (Accepted) — case store protegido.** El locator no contiene rutas: la ubicación es función pura del hash. Refuerza su invariante 3 y la superficie del test de path traversal.
- **ADR-005 (Accepted) — autoridad humana.** Fundamenta la decisión 8: un fragmento commiteado bajo `HumanAuthorization` no se reescribe sin acto humano nuevo.
- **ADR-004 (Accepted) — memoria del caso.** La regeneración de un derivado avanza `case_revision`; el re-anclaje, cuando exista, requerirá eventos nuevos en el log canónico.
- **ADR-007 (`Proposed`) — estrategia de persistencia.** Aporta los tres refinamientos aditivos sobre `derived_representations` y la retención como restricción del almacén de blobs.
- **ADR-008 (`Proposed`) — proposal y autorización.** Complementario: aquel gobierna qué se aprueba; este, qué significa exactamente aquello a lo que la aprobación apunta.
- **ADR-010 (`Proposed`) — superficie MCP.** Fija el handle `fragment_ref` como opaco y verificable; este ADR fija qué hay detrás del handle y cuándo se invalida.
- **Kernel técnico v0.4** §1 (Principal ≠ `provenance_kind`), §8.1 (lista cerrada de eventos), §10 (pipeline de condiciones), §11 (identidad de entidad ≠ identidad de contenido) y §14 (precedencia): este ADR se subordina a todos ellos.
