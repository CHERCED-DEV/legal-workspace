All 8 required sections present, 680 lines.

**(1) RUTAS ESCRITAS**

- `C:/Users/HITMA/Desktop/legal-workspace/experiments/transcription-spike/README.md` (único archivo; 59 KB, 680 líneas; formato Question / Why it matters / Hypothesis / Method / Result / Limitations / Architecture implication / Delete-keep recommendation; marcado NON-PRODUCTION SPIKE y nivel documental 6 por kernel §14)

**(2) HALLAZGOS CLAVE**

- **HECHO VERIFICADO** — Los cinco proveedores documentan sus timestamps como relativos al **comienzo del audio enviado**, no del original. Google lo dice literal: `startOffset` = *"Time offset relative to the beginning of the audio"*. Ningún proveedor tiene ni puede tener el concepto de `Source`: el invariante temporal **no es delegable a ningún proveedor, presente o futuro**.
- **HECHO VERIFICADO** — El límite de OpenAI es **25 MB** (*"Files can be up to 25 MB"*) frente a 2 GB (Deepgram), 5 GB / 10 h (AssemblyAI), 1 GB batch y <500 MB fast (Azure), 8 h (Google). Una entrevista de 1 h en MP3 128 kbps (~55 MB) **duplica el límite de OpenAI**: obliga a trocear, y trocear es la única operación de la lista con riesgo probatorio.
- **HECHO VERIFICADO** — En OpenAI, `timestamp_granularities[]` está soportado **solo en `whisper-1`**. Los modelos `gpt-4o-transcribe` / `-mini` **no dan timestamps de palabra**: elegir el modelo más nuevo de ese proveedor cuesta la granularidad de anclaje que el `EvidenceLink` sobre audio necesita.
- **POR VERIFICAR (los cinco)** — **Ninguno publica precisión temporal.** Solo publican unidad/resolución de representación (segundos, ms, ticks de 100 ns), que no dice nada sobre el error real. Azure representa en ticks de 100 ns y de ahí **no** se sigue exactitud de 100 ns.
- **POR VERIFICAR (los cinco)** — Ninguno caracteriza en doc oficial su comportamiento con audio de mala calidad. Azure solo recomienda cualitativamente WAV(PCM)/FLAC. No se citó literatura de terceros como si fuera oficial.
- **HECHO VERIFICADO** — Confianza asimétrica: Deepgram, AssemblyAI y Google dan confianza por palabra; Azure solo por frase/`nBest` (por palabra **POR VERIFICAR**); OpenAI **no da confianza por palabra** — solo `avg_logprob`/`no_speech_prob`/`compression_ratio` por segmento. `avg_logprob` es log-probabilidad, **no** confianza en [0,1].
- **HECHO VERIFICADO / RIESGO** — AssemblyAI documenta que con detección automática de idioma, una feature no soportada se *"silently omitted from the response. The transcription itself still succeeds"*. Modo de fallo que el port debe neutralizar comparando `granularity` devuelta contra `want_granularity`.
- **HECHO VERIFICADO / RIESGO** — Google batch *"is only able to transcribe audio stored in Cloud Storage"* y Azure batch exige URI público o Blob Storage: ambos obligan a una **segunda copia del original privilegiado fuera del private state** (problema de ADR-002, no de rendimiento).
- **HECHO VERIFICADO** — Azure es el único que publica cota de latencia, y es dura: *"up to 30 minutes ... to start processing and up to 24 hours to complete"*, best-effort. Los otros cuatro no publican latencia — lo que significa que **no la sabemos**, no que sean rápidos.
- **HECHO VERIFICADO / POR VERIFICAR** — Español: Azure documenta 22 locales incluido **`es-CO`**; Deepgram `es`/`es-419`; Google `es-ES`/`es-US` (y `es-419` solo en `chirp_2`). AssemblyAI es el único con banda de exactitud publicada (*"High accuracy (≤ 10% WER)"*), **declarada por el propio proveedor y sin metodología** — no es medición independiente. Precio de Google y Azure **no obtenido** de fuente oficial (páginas truncadas / importes como `"$-"`); **no se rellenó con memoria ni con terceros**.

**(3) IMPLICACIÓN ARQUITECTÓNICA**

El invariante temporal es propiedad **del adapter**, no del proveedor, y se materializa como tipo, no como comentario: `OriginalOffsetMs` es un branded type y `TimelineAttestation` tiene `basis: 'ORIGINAL_SOURCE'` como literal de valor único, con la regla `transform: NONE ⟺ rebased: false` y **fail-closed** vía `TIMELINE_CONTRACT_VIOLATION`. Misma técnica que kernel §3.1 usa con `consumed_at` en lugar de `single_use`: materializar el invariante en vez de prometerlo.

El criterio de selección dominante **no es precio ni granularidad** (equivalentes o despreciables) sino **si el original cabe entero**. Cumplen con `transform: NONE` para audio jurídico realista: **Deepgram, AssemblyAI y Azure**. Cumple con matices: **Google** (semántica correcta, pero exige GCS). **Exige normalización de línea de tiempo: OpenAI** — no por su semántica de timestamps, que es correcta, sino por los 25 MB.

Distinción que el documento fija: **normalización de unidades ≠ normalización de línea de tiempo**. Las cinco exigen lo primero (traducción mecánica, sin riesgo); solo el re-basado tras trocear toca el invariante.

Regla escrita explícitamente: si un proveedor no cumple, las respuestas admisibles son **adapter → normalización declarada → proveedor alternativo**, en ese orden. **Nunca** relajar el invariante, admitir otro `basis`, fabricar `confidence` ni mover reglas al Domain. Es aplicación literal del bloqueante n.º 3 del vertical slice (*"cambia el diseño del locator, no el invariante"*) y de la precedencia del kernel §14.

Verificación de que la arquitectura funciona: cinco proveedores con cuatro representaciones distintas del tiempo, confianza en niveles distintos y límites que difieren en dos órdenes de magnitud — **toda esa variedad muere en el adapter**. `DerivedRepresentation`, `EvidenceLink` y el invariante 5 de `Source` no cambian.

Propuestas mías, etiquetadas como tales: (a) regla de fail-safe — proveedor sin confianza ⇒ **un rango que cubre el derivado completo** con `CONFIDENCE_NOT_AVAILABLE`, nunca lista vacía (lista vacía y "no sé" son estados opuestos; mismo criterio que `PARTIAL ⇒ omissions` no vacío del kernel §9); (b) `derivation_source: REAL | DEV_FIXTURE` en la receta, con fail-to-start por analogía con kernel §4 — señalando que el punto de fail-to-start es **más discutible** aquí que en la autorización, porque una autorización falsa fabrica autoridad humana y una transcripción de fixture solo fabrica texto ya marcado. Queda como DECISIÓN PENDIENTE de los dueños.

**(4) NOT_TESTED / INCONCLUSIVE**

- **NOT_TESTED — todo el eje experimental.** Cero llamadas a proveedores, cero audio transcrito, cero medición. **Nada del documento es "observed in current environment"**; todo es *documented platform claim* fechado 2026-08-24. Un dato publicado no es un SLA.
- **NOT_TESTED — el invariante temporal en v0.** El `FixtureTranscriptionProvider` **no lo pone a prueba: lo satisface trivialmente** (no transforma nada ⇒ nunca ejercita el camino de re-basado, que es donde vive el riesgo). Mitigación estructural: el contrato ya obliga al primer adapter real a enfrentarlo explícitamente vía `TimelineTransform`.
- **INCONCLUSIVE — precisión temporal, los cinco.** No por falta de búsqueda sino porque **nadie lo publica**. Solo se resuelve midiendo contra corpus propio etiquetado. `resolution_ms = null` para los cinco.
- **INCONCLUSIVE — exactitud en español.** Una sola banda auto-declarada sin metodología (AssemblyAI). Si `es-CO` de Azure aporta algo medible sobre `es-419`/`es-ES` es **SUPUESTO**: nadie lo publica.
- **INCONCLUSIVE — comportamiento con audio degradado, los cinco.** Sin caracterización oficial. El diseño no depende de resolverlo: `UNCERTAIN_FRAGMENT` + la regla de fail-safe + `DerivedRepresentation` que nunca sustituye al Source cubren el peor caso.
- **NOT_TESTED — precio de Google y Azure.** Páginas oficiales no entregaron cifras (truncado / `"$-"`). Se dejó POR VERIFICAR en lugar de rellenar.
- **NO INVESTIGADO — retención, confidencialidad y jurisdicción de procesamiento.** Es el prerrequisito **decisivo** sobre material privilegiado y probablemente más determinante que el precio; queda como punto 1 de la lista previa a elegir proveedor.
- **NOT_TESTED — el contrato no compila.** TypeScript conceptual, sin implementación ni build; puede tener errores que solo un compilador revelaría.
- **FUERA DE ALCANCE — diarización**, por decisión ya fijada del corpus (Glosario §4: v0 no la modela y no se afirma su fiabilidad).

El spike **no elige proveedor y no debe leerse como si lo hiciera**: esa elección es un ADR, con los cuatro POR VERIFICAR resueltos y la decisión de confidencialidad tomada por los dueños.