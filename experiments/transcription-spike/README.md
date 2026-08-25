# SPIKE — Transcripción: contrato del driven port y verificación de proveedores

> **NON-PRODUCTION SPIKE.**
> Este documento vive en `experiments/` y **no es código de producción**. No contiene implementación: solo contrato conceptual en TypeScript y verificación documental. Regla de dependencias vigente (kernel técnico §13): **`src/` nunca importa de `experiments/`**.
> **Nivel documental 6** (kernel §14 — Precedencia): los resultados de un spike son **observaciones**, jamás garantías de plataforma, y no pueden redefinir nada fijado en los ADRs Accepted, el Technical Design, los Architecture Principles ni el Glosario.
>
> **Fecha de consulta de toda fuente externa: 2026-08-24.** Todo precio, límite y capacidad de proveedor es un dato **fechado**, no una garantía contractual: los proveedores los cambian sin avisarnos.

---

## Question

Dos preguntas, una de diseño y una de verificación:

1. **CONTRATO.** ¿Cuál es la forma exacta del **driven port `TranscriptionProvider`** que produce la `DerivedRepresentation` de un `Source` de audio, de modo que (a) el Domain no lo conozca, (b) la entrada sea una referencia al Source incorporado y nunca una ruta, (c) la salida lleve texto + rango temporal + confianza + fragmentos inciertos + errores tipados, y (d) se cumpla el **invariante duro**: *todo timestamp resuelve contra la línea de tiempo del ORIGINAL, nunca contra un derivado arbitrario*?

2. **VERIFICACIÓN.** Contra **documentación oficial de proveedores**, ¿qué se puede afirmar hoy sobre los 10 puntos que piden los dueños (formatos, granularidad de timestamps, precisión temporal, confianza/fragmentos inciertos, errores, costo, latencia, español, tamaño máximo, audio de mala calidad), y qué **no** está publicado y por tanto queda `POR VERIFICAR`?

---

## Why it matters

Tres razones, en orden de gravedad.

1. **Es el bloqueante n.º 3 declarado del slice.** `vertical-slice-v0.md` §Bloqueantes lo dice literalmente: *"POR VERIFICAR — Proveedor de transcripción y sus capacidades de timestamps. Bloquea el diseño del adapter y, sobre todo, el anclaje de fragmentos"*. El glosario lo repite en tres entradas distintas (`Statement` §4, `EvidenceLink` §6, `DerivedRepresentation` §13).

2. **El invariante temporal es la base de la trazabilidad probatoria sobre audio.** La cadena que el slice debe recorrer entera es `Fact → EvidenceLink → fragmento → DerivedRepresentation → Source` (glosario, §Cadena de trazabilidad). Sobre un audio, "fragmento" **es** un rango de timestamps. Si ese rango está anclado a un derivado —a un recorte, a un chunk, a un archivo transcodificado— entonces la cadena **no resuelve al original** y el invariante 5 de `Source` queda roto:

   > *"Los anclajes (página, offsets, rangos de timestamps) refieren **siempre a la línea de tiempo o paginación del original**, nunca a la de un derivado o un recorte."* — Glosario §2, invariante 5.

   Y el invariante 2 de `Statement` (post-slice, pero ya contratado) dice lo mismo: *"los timestamps refieren a la línea de tiempo de la grabación, no a la del derivado ni a un recorte"*.

3. **Es donde un proveedor externo puede corromper silenciosamente el expediente.** Un adapter que trocea un audio de dos horas para caber en un límite de subida y devuelve offsets que reinician en `0` por cada trozo produce un expediente en el que `00:03:12` significa cosas distintas según el trozo. No hay excepción, no hay error, no hay condición: hay una cita que apunta a otro sitio. Es exactamente el fallo que ADR-006 y el modelo epistémico existen para impedir, y es **indetectable a posteriori** si el contrato no lo prohíbe estructuralmente.

---

## Hypothesis

Cuatro hipótesis, formuladas antes de consultar las fuentes.

- **H1 (contrato).** El invariante temporal se puede convertir en **propiedad del sistema de tipos**, no en una nota de documentación: si el port solo admite offsets de un tipo marcado que no se puede construir sin declarar la transformación aplicada, un adapter no puede devolver un timestamp anclado a un derivado *por descuido*, solo mintiendo explícitamente.
- **H2 (proveedores).** Todos los proveedores documentarán sus timestamps como **relativos al comienzo del audio enviado** —no del audio original—, con lo que el invariante se cumple **si y solo si** el original se envía íntegro, sin trocear ni recortar.
- **H3 (límites).** El factor que decide si hace falta normalización de línea de tiempo **no es la granularidad de los timestamps sino el tamaño máximo de archivo**: un límite bajo obliga a trocear, y trocear es exactamente lo que rompe el invariante.
- **H4 (honestidad).** Los datos de **precisión temporal** y de **comportamiento con audio de mala calidad** no estarán publicados en documentación oficial por ninguno, y tendrán que quedar `POR VERIFICAR` en lugar de rellenarse con plausibilidad.

**Resultado adelantado:** H1, H2 y H3 se confirman. H4 se confirma para precisión temporal y audio degradado; se confirma parcialmente para español (uno de los cinco publica una banda de exactitud, no una cifra).

---

## Method

**Qué se hizo.**

1. Lectura del corpus normativo para no reinventar vocabulario: kernel técnico v0.4 (`docs/technical-design/v0/00-technical-kernel.md`), ADR-006, glosario (§2 `Source`, §4 `Statement`, §6 `EvidenceLink`, §13 `DerivedRepresentation`) y `vertical-slice-v0.md` (Actors, esquemas conceptuales, matriz de pruebas, bloqueantes).
2. Redacción del contrato del port **derivando cada campo de un invariante ya aprobado**, no de preferencias de diseño. Cada decisión del contrato cita el invariante que la obliga.
3. Consulta de **documentación oficial de los cinco proveedores** (páginas de producto, referencia de API, límites/cuotas, idiomas y precios). Se registra la URL exacta por celda.

**Qué NO se hizo — y por qué importa para leer el Result.**

- **No se ejecutó ninguna llamada a ningún proveedor.** No hay cuentas, no hay claves, no hay audio de prueba en este spike. Por tanto **nada en la sección Result es "observed in current environment"**: todo es **"documented platform claim"**, que es una categoría más débil que una medición y más débil aún que una garantía contractual. Un dato publicado en una página de producto no es un SLA.
- **No se escribió código ejecutable.** El TypeScript de este documento es **contrato conceptual**: tipos e interfaces, sin implementación, sin `package.json`, sin build. No compila ni pretende compilar.
- **No se midió precisión temporal, ni WER en español, ni comportamiento con audio degradado.** Medir eso exige corpus etiquetado y es trabajo de un spike posterior (ver *Limitations*).

**Autoridad de fuentes.** Solo documentación oficial del proveedor. **No se citó ni un solo blog, benchmark de tercero ni comparativa comercial**, ni siquiera como contexto: en este dominio los benchmarks de terceros y los propios *leaderboards* de los proveedores son material de marketing, y una cifra de exactitud sin metodología publicada no es verificable. Donde la doc oficial calla, este documento dice `POR VERIFICAR`.

---

## Result

### PARTE 1 — Contrato del driven port `TranscriptionProvider`

#### 1.0 Dónde vive el port (y por qué el Domain no lo conoce)

**DECISIÓN APROBADA** (kernel §13, regla de dependencias): `domain` no importa `application` ni `infrastructure`; `infrastructure` implementa **puertos de `application`**.

```
Domain            conoce  DerivedRepresentation { version, content_hash, recipe, source_id, state }
                  NO conoce  TranscriptionProvider, ni proveedores, ni HTTP, ni audio.
                             ↑ El Domain no sabe que la transcripción existe como servicio.
                               Solo sabe que un Source puede tener un derivado regenerable.

Application       DEFINE el port  TranscriptionProvider   ← este contrato
                  lo consume el use case GenerateDerivedRepresentation (interno, kernel §7)

Infrastructure    IMPLEMENTA el port
                    · FixtureTranscriptionProvider   (v0)
                    · RealTranscriptionProvider      (post-v0, uno por proveedor)
```

El único actor del slice que toca este port es el **«Adapter de transcripción (driven port)»** ya listado en `vertical-slice-v0.md` §Actors, con `actor_type = AI_DERIVATION` y la columna Autoridad en: *"Ninguna: su salida es derivado regenerable, nunca sustituye al Source"*.

**Consecuencia dura:** cambiar de proveedor **no puede** tocar el Domain. Si tocarlo parece necesario, el diseño está mal — ver §1.8.

---

#### 1.1 El invariante duro, convertido en tipo

Este es el núcleo del contrato. El invariante no se documenta: **se hace inexpresable violarlo por accidente**.

```typescript
// ── NON-PRODUCTION SPIKE — contrato conceptual, sin implementación ──

declare const ORIGINAL_TIMELINE: unique symbol;

/**
 * INVARIANTE DURO (Glosario §2 Source, inv. 5; §4 Statement, inv. 2; §13
 * DerivedRepresentation, "No significa"):
 *
 *   Offset en milisegundos medido SIEMPRE desde t = 0 de la LÍNEA DE TIEMPO
 *   DEL ORIGINAL — entendido como el Source incorporado cuyos bytes quedaron
 *   sellados por el SHA-256 en `ingest_evidence`.
 *
 * Es un branded type deliberadamente: un `number` crudo NO es un
 * OriginalOffsetMs. Un adapter no puede devolver el offset que le dio el
 * proveedor "tal cual"; tiene que pasar por un constructor que le obliga a
 * declarar qué transformación aplicó al original (§1.4). Así, anclar a un
 * derivado deja de ser un descuido posible y pasa a ser una mentira explícita.
 *
 * Unidad: MILISEGUNDOS ENTEROS. Elegida porque es la unidad más fina que
 * alguno de los proveedores verificados publica (AssemblyAI) y porque evita
 * el error de redondeo acumulado de los segundos en coma flotante.
 * PROPUESTA DEL TECHNICAL DESIGN: la unidad no está fijada por ningún
 * documento superior.
 */
export type OriginalOffsetMs = number & { readonly [ORIGINAL_TIMELINE]: true };

/** Rango temporal cerrado-abierto [start, end) sobre la línea de tiempo del ORIGINAL. */
export interface OriginalTimeRange {
  readonly start: OriginalOffsetMs;
  readonly end: OriginalOffsetMs;
}
```

**Por qué un branded type y no un comentario.** El corpus ya tiene un precedente exacto de esta técnica de diseño: `HumanAuthorization` no lleva un campo `single_use`, porque un booleano es una promesa que alguien puede olvidar comprobar; lleva `consumed_at`, que **materializa** el invariante (kernel §3.1). Aquí ocurre lo mismo: un campo `timestamps_are_original: true` sería una promesa; un tipo que no se puede construir sin declarar la transformación es un mecanismo.

---

#### 1.2 Entrada — referencia al Source incorporado, **nunca** una ruta

```typescript
/** Identidad probatoria del material: el par (id emitido por el Core, content_hash). */
export interface SourceContentRef {
  readonly source_id: SourceId;        // id opaco emitido por el Core (kernel §11: UUIDv7 propuesto)
  readonly content_hash: Sha256;       // fija EXACTAMENTE qué bytes se transcriben
  readonly media_kind: 'AUDIO' | 'VIDEO';
  readonly byte_length: number;
  /** Duración declarada si el Core la conoce. NUNCA autoritativa: es metadato, no medición. */
  readonly declared_duration_ms: number | null;
}

/**
 * El Core abre el contenido; el adapter NO resuelve rutas y NO sabe dónde vive
 * el private state.
 *
 * Justificación (ADR-006, Contrato de incorporación): `ingest_evidence`
 * "referencia el material por identificador de Inbox resuelto por el Core,
 * nunca por rutas arbitrarias suministradas por el modelo". La misma razón que
 * prohíbe rutas en la ENTRADA al Case Store las prohíbe en la SALIDA hacia un
 * adapter: una ruta es una capacidad de leer cualquier cosa, y convierte al
 * adapter en un segundo camino de acceso al private state (ADR-002).
 */
export interface SourceContentHandle {
  readonly ref: SourceContentRef;
  /** El Core entrega un stream de los bytes YA incorporados. Sin path, sin URL local. */
  open(): Promise<ReadableStream<Uint8Array>>;
}

export interface TranscriptionRequest {
  /** Sugerencia de idioma; el adapter puede ignorarla si el proveedor autodetecta. */
  readonly language_hint: string | null;      // p.ej. 'es', 'es-CO'
  readonly want_granularity: 'SEGMENT' | 'WORD' | 'SEGMENT_AND_WORD';
  /**
   * Umbral bajo el cual un fragmento se reporta como incierto.
   * SUPUESTO declarado: su valor inicial NO está fijado por ningún documento
   * (Glosario §13: "Umbral de confianza de UNCERTAIN_FRAGMENT: NO TENEMOS
   * INFORMACIÓN SUFICIENTE"). Es configuración, y por PF-005 solo puede
   * endurecerse, nunca relajarse hasta suprimir la condición.
   */
  readonly uncertainty_threshold: number;
}
```

**Tres cosas que la entrada deliberadamente NO tiene**, cada una con su razón:

| Ausente | Por qué |
|---|---|
| `file_path` / `url` | ADR-006: el material se referencia por identidad, no por ubicación. Una ruta daría al adapter acceso lateral al private state (ADR-002). |
| `case_id` | El adapter no necesita saber a qué expediente pertenece el audio, y no debe. Minimiza el radio de un adapter comprometido y evita que la infraestructura razone sobre el Case (aislamiento entre Cases, Glosario §1 inv. 2). |
| Cualquier credencial del Core | Simetría con kernel §3.3: si la autorización humana no viaja al modelo, tampoco viaja al adapter nada que le confiera autoridad. El adapter produce un derivado; no consolida nada. |

---

#### 1.3 Salida — segmentos, confianza y fragmentos inciertos

```typescript
/** Confianza normalizada a [0,1] por el adapter. `null` ≠ 0: ver nota. */
export type ConfidenceScore = number | null;

export interface TranscriptWord {
  readonly text: string;
  readonly range: OriginalTimeRange;
  readonly confidence: ConfidenceScore;
}

export interface TranscriptSegment {
  /** Posición en la secuencia. NO es identidad — kernel §2.1: la identidad de
   *  un item nunca es su índice posicional. Si un segmento llegara a necesitar
   *  identidad estable (p. ej. para citarlo), la emite el Core, no el adapter. */
  readonly index: number;
  readonly text: string;
  readonly range: OriginalTimeRange;
  readonly confidence: ConfidenceScore;
  readonly words: readonly TranscriptWord[] | null;   // null = el proveedor no da palabra
}
```

**Regla de honestidad sobre `confidence` (PROPUESTA DEL TECHNICAL DESIGN, derivada de PF-005 y del pipeline de condiciones del kernel §10).**
`null` significa **"el proveedor no publica confianza para este nivel"**. No es `0`, no es "baja confianza", y **el adapter tiene prohibido fabricarla** —derivándola de un logprob, de una heurística de longitud o de cualquier otra cosa— sin declararlo en la receta. Un número inventado en este campo se propaga hasta un aviso de incertidumbre que la profesional leerá como medido.

```typescript
export type UncertaintyReason =
  | 'BELOW_CONFIDENCE_THRESHOLD'   // el proveedor dio confianza y quedó bajo umbral
  | 'PROVIDER_FLAGGED'             // el proveedor marcó el tramo por su cuenta
  | 'NO_SPEECH_SUSPECTED'          // señal tipo `no_speech_prob` alta
  | 'CONFIDENCE_NOT_AVAILABLE';    // ← ver regla de fail-safe abajo

export interface UncertainRange {
  readonly range: OriginalTimeRange;
  readonly reason: UncertaintyReason;
  readonly observed_confidence: ConfidenceScore;   // null si reason = CONFIDENCE_NOT_AVAILABLE
}
```

**Regla de fail-safe sobre incertidumbre (PROPUESTA DEL TECHNICAL DESIGN).**
Si el proveedor **no publica confianza en ninguna granularidad**, el adapter **no** devuelve `uncertain_ranges: []`. Devuelve **un único rango que cubre el derivado completo** con `reason = 'CONFIDENCE_NOT_AVAILABLE'`.

Justificación: la lista vacía y "no sé" son estados epistémicos opuestos, y colapsarlos hace que una transcripción sin medición de confianza se presente exactamente igual que una medida y verificada. Eso es la definición del riesgo que `UNCERTAIN_FRAGMENT` existe para cubrir —cuyo mensaje aprobado ya afirma que *"la fuente sigue siendo la grabación original"* (`vertical-slice-v0.md`, catálogo de condiciones)—. Es el mismo criterio con que el kernel §9 exige `completeness = PARTIAL ⇒ omissions` no vacío: **un contexto parcial nunca puede parecer expediente completo**.

---

#### 1.4 Atestación de línea de tiempo — el mecanismo que hace cumplir el invariante

```typescript
/** Qué le hizo el adapter al original ANTES de enviarlo al proveedor. */
export type TimelineTransform =
  /** Los bytes del Source se enviaron ÍNTEGROS. Único caso sin re-basado. */
  | { readonly kind: 'NONE' }
  /** El original se troceó. Cada trozo declara su desplazamiento en el ORIGINAL. */
  | {
      readonly kind: 'CHUNKED';
      readonly chunks: readonly {
        readonly index: number;
        readonly offset_in_original_ms: number;   // desplazamiento aplicado al re-basar
        readonly duration_ms: number;
      }[];
    }
  /** Recodificado sin alterar la duración (p.ej. contenedor no aceptado). */
  | { readonly kind: 'TRANSCODED'; readonly detail: string; readonly duration_preserving: true }
  | {
      readonly kind: 'CHUNKED_AND_TRANSCODED';
      readonly chunks: readonly { readonly index: number; readonly offset_in_original_ms: number; readonly duration_ms: number }[];
      readonly detail: string;
      readonly duration_preserving: true;
    };

export interface TimelineAttestation {
  /** Literal de valor único. NO existe otro valor legal: no hay forma de declarar
   *  en este contrato que los timestamps se anclan a otra cosa. */
  readonly basis: 'ORIGINAL_SOURCE';
  readonly transform: TimelineTransform;
  /** true ⇒ el adapter desplazó offsets para devolverlos a la línea del original. */
  readonly rebased: boolean;
  /** Granularidad temporal que el adapter puede sostener, en ms.
   *  `null` = NO DECLARADA. Ver Result Parte 2, punto 3: hoy es null para los cinco. */
  readonly resolution_ms: number | null;
}
```

**Las dos reglas que hacen que esto funcione:**

1. **`transform: 'NONE'` ⟺ `rebased: false`.** Cualquier otro `kind` **obliga** a `rebased: true` y a enumerar los desplazamientos. Un adapter que trocea y declara `NONE` está mintiendo en un campo persistido y auditable, no cometiendo un descuido silencioso.
2. **Fail closed.** Si el adapter no puede garantizar el re-basado —porque el proveedor no le dice a qué trozo corresponde un resultado, porque una transcodificación alteró la duración, o por lo que sea— **no devuelve una transcripción degradada**: devuelve el error tipado `TIMELINE_CONTRACT_VIOLATION` (§1.5) y la `DerivedRepresentation` termina en `FAILED`. El corpus ya fija la consecuencia y la considera aceptable: *"`FAILED` no es ausencia de evidencia. El Source sigue incorporado y consultable; lo que falta es el derivado"* (Glosario §13).

**`resolution_ms` no es cosmético.** Es el campo que impide prometer a la profesional más precisión de la que nadie ha medido. Mientras sea `null`, la UX de anclaje sobre audio debe presentar **rangos para escuchar**, no puntos exactos.

---

#### 1.5 Errores tipados — resultado, no excepción

```typescript
export type TranscriptionError =
  // ── Incompatibilidad detectable ANTES de gastar dinero y tiempo ──
  | { readonly kind: 'UNSUPPORTED_MEDIA_FORMAT'; readonly detail: string }
  | { readonly kind: 'SOURCE_TOO_LARGE'; readonly limit_bytes: number; readonly actual_bytes: number }
  | { readonly kind: 'SOURCE_TOO_LONG'; readonly limit_ms: number; readonly actual_ms: number | null }
  | { readonly kind: 'LANGUAGE_NOT_SUPPORTED'; readonly requested: string }
  // ── Violación del contrato: NUNCA degradar, siempre fallar ──
  | { readonly kind: 'TIMELINE_CONTRACT_VIOLATION'; readonly detail: string }
  | { readonly kind: 'CONTENT_HASH_MISMATCH'; readonly expected: Sha256; readonly actual: Sha256 }
  // ── Fallos del proveedor ──
  | { readonly kind: 'PROVIDER_UNAVAILABLE'; readonly retryable: true;  readonly detail: string }
  | { readonly kind: 'PROVIDER_TIMEOUT';     readonly retryable: true;  readonly elapsed_ms: number }
  | { readonly kind: 'PROVIDER_REJECTED';    readonly retryable: false; readonly provider_code: string }
  | { readonly kind: 'PROVIDER_QUOTA_EXCEEDED'; readonly retryable: true; readonly detail: string };

export type TranscriptionOutcome =
  | { readonly ok: true;  readonly value: TranscriptionResult }
  | { readonly ok: false; readonly error: TranscriptionError };
```

**Por qué `Outcome` y no excepciones.** Un fallo del adapter de transcripción es un **resultado esperado y modelado** del use case `GenerateDerivedRepresentation` —tiene su propio evento en la lista cerrada, `DerivedRepresentationFailed` (kernel §8.1)—, no una condición excepcional. Una excepción se puede tragar en un `catch` genérico; una unión discriminada obliga al llamador a decidir.

**Mapeo obligatorio a la lista cerrada de eventos y condiciones** (kernel §8.1 y §10 — el adapter **no inventa** eventos ni condiciones):

| Salida del port | Estado de `DerivedRepresentation` | Evento | Condición |
|---|---|---|---|
| `ok: true`, `uncertain_ranges` vacío | `READY` | `DerivedRepresentationGenerated` | — |
| `ok: true`, `uncertain_ranges` no vacío | `READY` | `DerivedRepresentationGenerated` | `UNCERTAIN_FRAGMENT {ranges}` — familia **Epistemic**, severidad info, **no bloquea** |
| `ok: false`, cualquier `kind` | `FAILED` | `DerivedRepresentationFailed` | `INTEGRATION_ERROR {integration, effect_on_state: NONE}` — familia **Infrastructure** |

Nota de precisión sobre `INTEGRATION_ERROR`: el kernel §10 la declara *"sin disparador ejercitado"* en v0 porque el slice no tiene conectores externos. Con un `RealTranscriptionProvider` **sí tendría disparador**; con el `FixtureTranscriptionProvider` de v0 sigue sin tenerlo salvo en el caso de prueba `F3b`, que fuerza el fallo deliberadamente. El dato relevante es que `effect_on_state` es `NONE`: el Source y la Evidence quedan intactos.

**`CONTENT_HASH_MISMATCH` merece una línea aparte.** Es el adapter re-verificando, antes de enviar, que los bytes que va a transcribir son los que el `content_hash` dice. Cuesta una pasada de hash y cierra el hueco entre "el Core me dio un handle" y "transcribí lo que el expediente cree que transcribí".

---

#### 1.6 El port completo

```typescript
export interface DerivationRecipe {
  readonly tool: string;               // p.ej. 'deepgram' | 'fixture'
  readonly version: string;            // modelo + versión de API, tal como el proveedor la nombre
  readonly parameters_hash: Sha256;    // hash de los parámetros efectivos de la llamada
  /** PROPUESTA DEL TECHNICAL DESIGN — ver §1.7. */
  readonly derivation_source: 'REAL' | 'DEV_FIXTURE';
}

export interface TranscriptionResult {
  /** Los MISMOS source_id + content_hash de la entrada: cierra la cadena de trazabilidad
   *  y hace verificable que el derivado corresponde a esos bytes y no a otros. */
  readonly source: SourceContentRef;
  readonly detected_language: string | null;
  readonly segments: readonly TranscriptSegment[];
  readonly uncertain_ranges: readonly UncertainRange[];
  readonly timeline: TimelineAttestation;
  /** Exigida por Glosario §13 inv. 3: "sin receta no es reproducible y no cumple su contrato". */
  readonly recipe: DerivationRecipe;
  readonly granularity: 'SEGMENT' | 'WORD' | 'SEGMENT_AND_WORD';
}

/** Capacidades DECLARADAS, verificables en el arranque y antes de cada llamada. */
export interface TranscriptionCapabilities {
  readonly max_bytes: number | null;
  readonly max_duration_ms: number | null;
  readonly granularity: 'SEGMENT' | 'WORD' | 'SEGMENT_AND_WORD';
  readonly publishes_confidence: 'PER_WORD' | 'PER_SEGMENT' | 'PER_SEGMENT_AND_WORD' | 'NONE';
  /** true ⇒ acepta el original íntegro para el perfil de uso previsto,
   *  y por tanto puede operar con transform 'NONE'. */
  readonly accepts_original_without_transform: boolean;
  /** true ⇒ el proveedor EXIGE depositar el original en almacenamiento de terceros
   *  antes de transcribir. Ver §Architecture implication, punto 4. */
  readonly requires_external_object_storage: boolean;
}

/**
 * EL PORT. Definido en Application; el Domain no lo conoce.
 * Lo consume el use case interno GenerateDerivedRepresentation (kernel §7).
 */
export interface TranscriptionProvider {
  readonly capabilities: TranscriptionCapabilities;
  transcribe(
    handle: SourceContentHandle,
    request: TranscriptionRequest,
  ): Promise<TranscriptionOutcome>;
}
```

**Para qué sirve `capabilities` en la práctica.** Permite a la Application comprobar `byte_length` y `declared_duration_ms` **contra los límites del proveedor antes de llamar**, y fallar con `SOURCE_TOO_LARGE` / `SOURCE_TOO_LONG` en lugar de que el adapter decida por su cuenta trocear el original. Ese es, literalmente, el punto de control donde el invariante temporal se salva o se pierde: **trocear tiene que ser una decisión declarada y visible, no un apaño interno del adapter.**

---

#### 1.7 `FixtureTranscriptionProvider` (v0)

```typescript
/**
 * NON-PRODUCTION. Implementación de v0: lee un fixture versionado junto a los
 * datos de prueba del slice. Sin red, sin claves, sin costo, determinista.
 */
export interface FixtureTranscriptionProvider extends TranscriptionProvider {
  readonly capabilities: TranscriptionCapabilities & {
    readonly accepts_original_without_transform: true;
    readonly requires_external_object_storage: false;
  };
}
```

**Qué garantiza por construcción.** El fixture se autora **contra el propio audio sintético del slice**, que *es* el Source. Por eso emite siempre `transform: { kind: 'NONE' }`, `rebased: false`, `basis: 'ORIGINAL_SOURCE'` — sin transformación no hay línea de tiempo derivada que pueda divergir. Es la única implementación que satisface el invariante **trivialmente**, y por eso mismo **no lo pone a prueba**: ver *Limitations*.

**Qué debe poder simular**, para que el slice ejercite su matriz de pruebas sin ningún proveedor real:

| Debe simular | Prueba del slice que lo consume |
|---|---|
| `PENDING → READY` con versión, hash y receta | `F3` |
| `PENDING → FAILED` + `INTEGRATION_ERROR {effect_on_state: NONE}` | `F3b` |
| `uncertain_ranges` no vacío ⇒ `UNCERTAIN_FRAGMENT {ranges}` | catálogo de condiciones |
| Granularidad `SEGMENT` y `WORD` | anclaje de `EvidenceLink`, `F5` |
| Regeneración ⇒ versión nueva con hash y receta propios | Glosario §13, lifecycle |

**PROPUESTA DEL TECHNICAL DESIGN — marca indeleble y fail-to-start.**
Se propone aplicar al fixture **el mismo régimen que el kernel §4 impone al `DevHumanAuthorizationProvider`**, por analogía y no por extensión automática (el kernel §4 habla solo del stub de autorización):

1. **FAIL TO START, no warning.** Si la configuración efectiva es de producción y el provider resuelto es el fixture, el arranque **aborta**. No hay modo degradado.
2. **Marca indeleble.** `recipe.derivation_source = 'DEV_FIXTURE'`, persistida en la `DerivedRepresentation` y propagada al evento `DerivedRepresentationGenerated`. Un `case.db` con derivados de fixture queda identificable para siempre como caso de desarrollo.

*Fuerza de esta propuesta:* el punto 2 es fuerte y barato —la receta ya es obligatoria por el invariante 3 de `DerivedRepresentation`, así que añadir el campo cuesta un enum—. El punto 1 es más discutible que en el caso de la autorización: una autorización falsa **fabrica autoridad humana**, mientras que una transcripción de fixture solo fabrica texto, que además está marcado. **DECISIÓN PENDIENTE de los dueños:** si el fail-to-start es proporcionado aquí o basta la marca.

---

#### 1.8 `RealTranscriptionProvider` (post-v0) — y la regla que no se negocia

```typescript
/**
 * POST-V0. Un adapter por proveedor. Cada uno declara sus capacidades
 * HONESTAMENTE: `accepts_original_without_transform: false` es una respuesta
 * legítima y preferible a trocear en silencio.
 */
export interface RealTranscriptionProvider extends TranscriptionProvider {}
```

> ### Regla explícita: si un proveedor real no cumple el contrato, **la respuesta NO es cambiar el Domain**
>
> Las tres respuestas admisibles, en este orden:
>
> 1. **Adapter** — traducir la forma del proveedor a la del port (unidades, nombres de campo, estructura de la respuesta). Es trabajo mecánico y siempre necesario: **ningún proveedor habla el idioma del port**, y eso no es un defecto de nadie.
> 2. **Normalización** — re-basar offsets a la línea de tiempo del original y **declarar la transformación** en `TimelineAttestation`. Legítima, auditable, con costo de complejidad y de superficie de error.
> 3. **Proveedor alternativo** — si ni siquiera con normalización se puede sostener el invariante, se cambia de proveedor. El port existe precisamente para que eso cueste un adapter y ninguna otra cosa.
>
> **Lo que NUNCA es respuesta:** relajar el invariante temporal, admitir un `basis` distinto de `ORIGINAL_SOURCE`, permitir `confidence` fabricada, o mover cualquiera de estas reglas al Domain para "acomodar" a un proveedor.
>
> Esto no es una preferencia de este spike: es la aplicación literal de lo que `vertical-slice-v0.md` ya fijó en su bloqueante n.º 3 — *"Si el proveedor no los entrega con esa semántica, **cambia el diseño del locator, no el invariante**"* — y de la regla de precedencia del kernel §14, según la cual un documento de nivel 6 (este) no puede redefinir nada de un nivel superior. **Un proveedor es infraestructura. El invariante es dominio. La infraestructura se adapta al dominio, nunca al revés.**

---

### PARTE 2 — Verificación contra documentación oficial

**Cómo leer estas tablas.** Una tabla por cada uno de los 10 puntos pedidos, con etiqueta y fuente **por celda**. Etiquetas usadas:

- **HECHO VERIFICADO** — publicado literalmente en documentación oficial del proveedor, consultada el 2026-08-24.
- **POR VERIFICAR** — la documentación oficial **no publica el dato**. No se rellena con estimaciones.
- **SUPUESTO** — inferencia razonada de este spike a partir de datos verificados; se marca como tal.

Ninguna celda de estas tablas es *"observed in current environment"*: **no se ejecutó ninguna llamada**. Todo es *documented platform claim*.

---

#### Punto 1 — Formatos de entrada

| Proveedor | Dato | Etiqueta | Fuente oficial |
|---|---|---|---|
| OpenAI | `mp3, mp4, mpeg, mpga, m4a, wav, webm` (lista cerrada) | HECHO VERIFICADO | developers.openai.com/api/docs/guides/speech-to-text |
| Deepgram | `MP3, MP4, MP2, AAC, WAV, FLAC, PCM, M4A, Ogg, Opus, WebM`; declara "over 100+" y que el formato es "largely unconstrained" | HECHO VERIFICADO | developers.deepgram.com/docs/supported-audio-formats |
| AssemblyAI | "most common audio and video formats — submit your file as-is, no transcoding needed" (sin enumerar) | HECHO VERIFICADO (enunciado cualitativo, no lista) | assemblyai.com/docs/speech-to-text/pre-recorded-audio |
| Google STT v2 | Ejemplos usan `AutoDetectDecodingConfig`; la página de batch **no enumera** formatos | POR VERIFICAR | docs.cloud.google.com/speech-to-text/v2/docs/batch-recognize |
| Azure Speech | `WAV, MP3, OPUS/OGG, FLAC, WMA, AAC, ALAW/MULAW en WAV, AMR, WebM, SPEEX`; recomienda WAV(PCM)/FLAC | HECHO VERIFICADO | learn.microsoft.com/…/batch-transcription-audio-data |

**Lectura para el contrato:** solo OpenAI publica una lista **cerrada y corta** que un audio de móvil o de grabadora puede no satisfacer. Es el único de los cinco donde `UNSUPPORTED_MEDIA_FORMAT` es un caso frecuente y previsible, y por tanto donde la tentación de transcodificar —y de ahí, de tocar la línea de tiempo— aparece primero.

---

#### Punto 2 — Timestamps: granularidad palabra / segmento

| Proveedor | Dato | Etiqueta | Fuente oficial |
|---|---|---|---|
| OpenAI | `timestamp_granularities[]` con `word` y `segment`; `verbose_json` expone segmentos (`id, start, end, text`) y palabras (`word, start, end`). **Solo soportado para `whisper-1`** | HECHO VERIFICADO | guides/speech-to-text; api-reference/audio/createTranscription |
| Deepgram | `words`: cada `word` con `start` y `end` **en segundos**; además `paragraphs` y `utterances` | HECHO VERIFICADO | developers.deepgram.com/docs/pre-recorded-audio |
| AssemblyAI | `words` con `start` y `end` **en milisegundos**; también `utterances` | HECHO VERIFICADO | assemblyai.com/docs/speech-to-text/pre-recorded-audio |
| Google STT v2 | `WordInfo.startOffset` / `endOffset`, condicionados a `enableWordTimeOffsets = true` y **solo en la hipótesis principal** | HECHO VERIFICADO | …/reference/rest/v2/…/recognize |
| Google STT v2 | Qué modelos (`chirp`, `chirp_2`) soportan word timestamps para español | POR VERIFICAR | la página de idiomas no lo documenta |
| Azure Speech | `recognizedPhrases[].offset/duration` (frase) y `words` / `displayWords` con `offset` y `duration`, condicionados a `wordLevelTimestampsEnabled` / `displayFormWordLevelTimestampsEnabled`. Formato ISO-8601 y **ticks de 100 ns** | HECHO VERIFICADO | learn.microsoft.com/…/batch-transcription-get |

**Hallazgo con consecuencia directa:** en OpenAI, los timestamps de palabra **existen solo en `whisper-1`**, el modelo más antiguo de su catálogo de audio. Los modelos `gpt-4o-transcribe` / `gpt-4o-mini-transcribe` **no los ofrecen**. Elegir el modelo "mejor" de ese proveedor implica **perder la granularidad de anclaje**, que es justo lo que el `EvidenceLink` sobre audio necesita.

---

#### Punto 3 — Precisión temporal (exactitud del timestamp)

| Proveedor | Dato | Etiqueta | Fuente oficial |
|---|---|---|---|
| OpenAI | Ninguna cifra de exactitud temporal publicada | **POR VERIFICAR** | consultadas guides/speech-to-text y api-reference |
| Deepgram | Ninguna cifra publicada. Menciona "high accuracy timestamps" para el modelo *legacy* Enhanced, **sin dato técnico** | **POR VERIFICAR** | developers.deepgram.com/docs/models-languages-overview |
| AssemblyAI | Ninguna cifra publicada (unidad ms ≠ exactitud ms) | **POR VERIFICAR** | assemblyai.com/docs/… |
| Google STT v2 | Ninguna cifra publicada | **POR VERIFICAR** | …/reference/rest/v2/… |
| Azure Speech | Ninguna cifra publicada (ticks de 100 ns es **resolución de representación**, no exactitud) | **POR VERIFICAR** | learn.microsoft.com/…/batch-transcription-get |

> **Este es el hallazgo negativo más importante del spike, y confirma H4.**
> **Ninguno de los cinco proveedores publica exactitud temporal en documentación oficial.** Todo lo que publican es la **unidad y la resolución de representación** —segundos, milisegundos, ticks de 100 ns—, que no dicen absolutamente nada sobre el error real del timestamp frente al audio.
>
> Confundir ambas cosas sería el error clásico: **Azure representa en ticks de 100 nanosegundos, y de ahí no se sigue que sepa dónde empieza una palabra con precisión de 100 ns.** Nadie ha publicado que lo sepa.
>
> Consecuencia contractual: `TimelineAttestation.resolution_ms` es **`null` para los cinco** hasta que se mida con corpus propio. Consecuencia de producto: la UX de anclaje sobre audio presenta **rangos para escuchar**, no puntos exactos — que además es lo que el mensaje aprobado de `UNCERTAIN_FRAGMENT` ya hace ("conviene escucharla antes de apoyarse en esos pasajes").

---

#### Punto 4 — Fragmentos inciertos y confianza

| Proveedor | Dato | Etiqueta | Fuente oficial |
|---|---|---|---|
| OpenAI | **Sin confianza por palabra.** Por segmento: `avg_logprob`, `no_speech_prob`, `compression_ratio`. Nota literal: *"If the value is lower than -1, consider the logprobs failed"*. `include[]=logprobs` (token-level) solo en `gpt-4o-transcribe` / `-mini` | HECHO VERIFICADO | api-reference/audio/createTranscription |
| Deepgram | `confidence` **por palabra** y `confidence` global del transcript, valor 0–1 | HECHO VERIFICADO | developers.deepgram.com/docs/pre-recorded-audio |
| AssemblyAI | `confidence` en **tres niveles**: transcript, `utterances` y `words` | HECHO VERIFICADO | assemblyai.com/docs/speech-to-text/pre-recorded-audio |
| Google STT v2 | `confidence` 0.0–1.0, *"only in the top hypothesis"*; la página de idiomas lista "Word-level confidence" como feature para español | HECHO VERIFICADO | …/reference/rest/v2/…; …/speech-to-text-supported-languages |
| Azure Speech | `confidence` por frase y por alternativa `nBest`. **Confianza por palabra: no documentada** — la tabla de propiedades y el ejemplo muestran `displayWords` solo con `offset`/`duration` | HECHO VERIFICADO (frase) / **POR VERIFICAR** (palabra) | learn.microsoft.com/…/batch-transcription-get |

**Lectura para el contrato:** `publishes_confidence` es `PER_SEGMENT_AND_WORD` para Deepgram, AssemblyAI y Google; `PER_SEGMENT` para Azure y OpenAI. En OpenAI hay un matiz adicional que el adapter **no puede disimular**: `avg_logprob` es una **log-probabilidad media, no una confianza en [0,1]**. Mapearla a `ConfidenceScore` exige una transformación que no es neutral y que **debe declararse en `recipe.parameters_hash`** — o, mejor, devolver `null` y `CONFIDENCE_NOT_AVAILABLE`. Es exactamente el caso que la regla de honestidad de §1.3 previene.

---

#### Punto 5 — Identificación de errores

| Proveedor | Dato | Etiqueta | Fuente oficial |
|---|---|---|---|
| OpenAI | Errores HTTP estándar de la API. Sin catálogo de errores específico de transcripción en la guía | POR VERIFICAR (catálogo completo) | guides/speech-to-text |
| Deepgram | `504: Gateway Timeout` documentado para requests que exceden **10 min** (Nova/Base/Enhanced) o **20 min** (Whisper) de **procesamiento** | HECHO VERIFICADO | developers.deepgram.com/docs/pre-recorded-audio |
| AssemblyAI | Campo `status` en el objeto transcript (incluye estado de error); límites de paralelismo documentados | HECHO VERIFICADO | assemblyai.com/docs/speech-to-text/pre-recorded-audio |
| AssemblyAI | Comportamiento tipado ante feature no soportada: con código de idioma manual **rechaza con error**; con detección automática la feature *"silently omitted from the response. The transcription itself still succeeds"* | HECHO VERIFICADO | …/pre-recorded-audio/supported-languages |
| Google STT v2 | Operación de larga duración con estado; catálogo de errores no detallado en la página de batch | POR VERIFICAR | …/batch-recognize |
| Azure Speech | `status` (`Running`/`Succeeded`), `recognitionStatus` por frase (*"Success" or "Failure"*), `report.json` con `successfulTranscriptionsCount`/`failedTranscriptionsCount`; `429` documentado con recomendación de retry | HECHO VERIFICADO | learn.microsoft.com/…/batch-transcription-get; …/quotas-and-limits |

> **Hallazgo con consecuencia de seguridad epistémica.** El comportamiento documentado de AssemblyAI —con detección automática de idioma, una feature no soportada se **omite silenciosamente** y la transcripción **igual reporta éxito**— es un modo de fallo que el port debe neutralizar. Si se pide `WORD` y llega `SEGMENT` sin error, el adapter **no** puede devolver `ok: true` con menos granularidad de la solicitada: debe comparar `granularity` devuelta contra `want_granularity` y, si difiere, declararlo. Es el mismo principio del kernel §9: **lo que falta se declara; nunca se presenta lo parcial como completo.**

---

#### Punto 6 — Costo

| Proveedor | Dato | Etiqueta | Fuente oficial |
|---|---|---|---|
| OpenAI | Whisper: **$0.006 / minuto**. `gpt-4o-transcribe`: $2.50/1M tokens in, $10.00/1M out, *"Estimated cost"* **$0.006/min**. `gpt-4o-mini-transcribe`: $1.25/$5.00 por 1M tokens, *"Estimated cost"* **$0.003/min** | HECHO VERIFICADO (2026-08-24) | developers.openai.com/api/docs/pricing |
| Deepgram | Nova-3 monolingüe **$0.0043/min** (PAYG) / $0.0036 (Growth); Nova-3 multilingüe **$0.0052/min** / $0.0043; Whisper Large **$0.0048/min** | HECHO VERIFICADO (2026-08-24) | deepgram.com/pricing |
| AssemblyAI | Universal-3.5 Pro **$0.21/hr**; Universal-2 **$0.15/hr** (pre-grabado). SLAM-1 deprecado | HECHO VERIFICADO (2026-08-24) | assemblyai.com/pricing |
| Google STT v2 | **No extraíble**: la página de precios no entregó las cifras en la consulta (contenido truncado / renderizado en cliente) | **POR VERIFICAR** | cloud.google.com/speech-to-text/pricing |
| Azure Speech | **No extraíble**: la página muestra los importes como marcador `"$-"`. Sí publica Free (F0): *"Real-time Transcription: 5 audio hours free per month"* | **POR VERIFICAR** (Standard) / HECHO VERIFICADO (F0) | azure.microsoft.com/…/pricing/details/cognitive-services/speech-services/ |

**Nota de veracidad, deliberada.** Habría sido trivial rellenar Google y Azure con cifras de memoria o de un comparador de terceros. **No se hizo.** Las páginas oficiales no entregaron el dato en la consulta y por tanto el dato **no se tiene**. Todos los precios verificados son **observaciones fechadas al 2026-08-24**, no compromisos: hay que re-verificarlos en el momento de decidir.

**Orden de magnitud (SUPUESTO, aritmética sobre cifras verificadas):** una hora de audio cuesta ~$0.26 en Deepgram Nova-3 multilingüe, ~$0.15–0.21 en AssemblyAI y ~$0.36 en OpenAI Whisper. **A esta escala el costo no es criterio de decisión** frente al cumplimiento del invariante; sí lo sería a volúmenes que hoy nadie ha cuantificado — el glosario registra la pregunta abierta de negocio *"horas de audio/video por caso y por semana"* (§13), todavía sin responder.

---

#### Punto 7 — Latencia

| Proveedor | Dato | Etiqueta | Fuente oficial |
|---|---|---|---|
| OpenAI | Sin cifras de latencia publicadas | POR VERIFICAR | guides/speech-to-text |
| Deepgram | Sin cifra de latencia. Publica un **timeout de procesamiento**: >10 min (Nova/Base/Enhanced) o >20 min (Whisper) ⇒ `504` | HECHO VERIFICADO (timeout) / POR VERIFICAR (latencia) | developers.deepgram.com/docs/pre-recorded-audio |
| AssemblyAI | Sin cifras de latencia publicadas | POR VERIFICAR | assemblyai.com/docs/… |
| Google STT v2 | Sin cifras. Batch es operación de larga duración, recomendada para audio >60 s | HECHO VERIFICADO (modelo async) / POR VERIFICAR (latencia) | …/batch-recognize |
| Azure Speech | *"Batch transcription jobs are scheduled on a best-effort basis. At peak hours, it might take up to 30 minutes for a transcription job to start processing and up to 24 hours to complete."* Además: *"increasing the quota doesn't improve transcription performance"* | **HECHO VERIFICADO** | learn.microsoft.com/…/batch-transcription-get; …/quotas-and-limits |

> **Azure es el único de los cinco que publica una cota de latencia — y es dura: hasta 30 minutos para empezar y hasta 24 horas para terminar, en modo *best-effort*.**
> Esto no descalifica a Azure: la derivación **ya es asíncrona por diseño** en el corpus (`PENDING | READY | FAILED`, sin motor de jobs genérico, kernel §11), precisamente para no acoplar el flujo de la profesional a la latencia de un derivado. Pero sí cambia la conversación de producto: con 24 h de cota superior, "incorpora la grabación y trabajamos sobre ella" deja de ser una interacción de una sesión. Azure ofrece además **fast transcription** (<500 MB, <5 h) como camino síncrono alternativo, que sería el adecuado para este uso.
> Que los otros cuatro **no publiquen** latencia no significa que sean rápidos: significa que **no lo sabemos**.

---

#### Punto 8 — Español

| Proveedor | Dato | Etiqueta | Fuente oficial |
|---|---|---|---|
| OpenAI | *"Supported language-code formats include: ISO 639-1 codes, such as `en`, `es`, and `fr`"* — `es` aparece como ejemplo de código admitido. **Sin exactitud por idioma** | HECHO VERIFICADO (soporte) / POR VERIFICAR (exactitud) | guides/speech-to-text |
| Deepgram | Nova-3 y Nova-2: *"Spanish: `es`, `es-419`"*. **Sin exactitud por idioma** | HECHO VERIFICADO (soporte) / POR VERIFICAR (exactitud) | developers.deepgram.com/docs/models-languages-overview |
| AssemblyAI | Universal-3.5 Pro: español entre 18 idiomas, con *"deep understanding of regional dialects and local variants"*. Universal-2: español entre 99 idiomas, en la banda *"High accuracy (≤ 10% WER)"* | HECHO VERIFICADO | …/pre-recorded-audio/supported-languages |
| Google STT v2 | `es-ES` y `es-US` (modelos `chirp`, `chirp_2`, `chirp_telephony`); **`es-419` solo en `chirp_2`**. Sin exactitud por idioma | HECHO VERIFICADO (soporte) / POR VERIFICAR (exactitud) | …/speech-to-text-supported-languages |
| Azure Speech | **22 locales de español**, incluido **`es-CO` (Spanish, Colombia)**, todos con soporte de fast transcription | HECHO VERIFICADO | learn.microsoft.com/…/language-support |

**Dos observaciones que importan.**

1. **AssemblyAI es el único de los cinco que publica una banda de exactitud** (*"≤ 10% WER"*) que incluya al español. Es una **banda declarada por el proveedor, sin metodología ni corpus publicados en esa página**: es mejor que nada y **no es** una medición independiente ni una garantía. No debe citarse como si lo fuera.
2. **Azure es el único que documenta `es-CO` como locale propio.** Dado que la jurisdicción del producto es Colombia —el *Knowledge Pack Colombia* está en el backlog post-V0 (kernel §15)—, la existencia de un modelo específico de español colombiano es una ventaja **plausible pero no demostrada**: nadie publica cuánto mejora frente a `es-419` o `es-ES`. **SUPUESTO, POR VERIFICAR con audio real del oficio.**

---

#### Punto 9 — Tamaño máximo de archivo

| Proveedor | Dato | Etiqueta | Fuente oficial |
|---|---|---|---|
| OpenAI | **25 MB**, literal: *"Files can be up to 25 MB."* | HECHO VERIFICADO | guides/speech-to-text |
| Deepgram | **2 GB**; *"For large video files, extract the audio stream first"* | HECHO VERIFICADO | developers.deepgram.com/docs/pre-recorded-audio |
| AssemblyAI | **5 GB** por request directo; **2.2 GB** para archivos locales subidos. Duración: *"160 ms to 10 hours per file"* | HECHO VERIFICADO | assemblyai.com/docs/speech-to-text/pre-recorded-audio |
| Google STT v2 | Duración: *"The upper limit for asynchronous speech recognition is 480 minutes (8 hours)"*. **Solo transcribe audio almacenado en Cloud Storage**. Límite de bytes no indicado en esa página | HECHO VERIFICADO (duración y requisito GCS) / POR VERIFICAR (bytes) | …/batch-recognize |
| Azure Speech | Batch: **1 GB** por archivo, **1.000** archivos por request, **10.000** blobs por contenedor; con diarización, **240 min** por archivo. Fast transcription: **<500 MB**, **<5 h** | HECHO VERIFICADO | learn.microsoft.com/…/quotas-and-limits |

> **Aquí se decide el invariante, y H3 queda confirmada.**
> **El límite de OpenAI (25 MB) es entre 80 y 200 veces menor que el de los demás.** Una entrevista de una hora en MP3 a 128 kbps ocupa del orden de 55 MB — **más del doble del límite**. Es decir: para el material real de este producto, usar OpenAI **obliga** a trocear o a recomprimir el original, y **trocear es exactamente la operación que rompe la línea de tiempo**.
> Ese troceo es perfectamente normalizable (§1.4, `transform: CHUNKED`), pero deja de ser gratis: pasa a ser **la parte del adapter donde vive el riesgo probatorio**, y donde cada corte es una oportunidad de desalinear una cita.

---

#### Punto 10 — Comportamiento con audio de mala calidad

| Proveedor | Dato | Etiqueta | Fuente oficial |
|---|---|---|---|
| OpenAI | Sin caracterización de comportamiento ante audio degradado. Señales indirectas publicadas: `no_speech_prob`, `avg_logprob`, `compression_ratio` | **POR VERIFICAR** | api-reference/audio/createTranscription |
| Deepgram | Sin caracterización publicada | **POR VERIFICAR** | docs consultadas |
| AssemblyAI | Sin caracterización publicada. Ofrece `confidence` en tres niveles como señal | **POR VERIFICAR** | docs consultadas |
| Google STT v2 | Sin caracterización publicada | **POR VERIFICAR** | docs consultadas |
| Azure Speech | Sin caracterización. Recomienda *"use lossless formats such as WAV (PCM encoding) and FLAC"* para *"the best transcription quality"* — recomendación cualitativa, sin datos | HECHO VERIFICADO (recomendación) / **POR VERIFICAR** (comportamiento) | learn.microsoft.com/…/batch-transcription-audio-data |

**Confirmación de H4 y nota de disciplina.** **Ninguno de los cinco caracteriza en documentación oficial qué hace con audio malo.** Existe literatura y experiencia de campo abundante sobre modos de fallo de estos sistemas —alucinación sobre silencio, repeticiones, texto inventado en tramos ruidosos—, pero **eso no es documentación oficial del proveedor y este spike no lo cita como si lo fuera**.

La consecuencia de diseño no depende de resolver esta incógnita, y esto es lo importante: el producto **ya está construido para no necesitar la respuesta**. `UNCERTAIN_FRAGMENT` existe, es `info` y no bloqueante, y su mensaje aprobado afirma que el original sigue siendo la fuente. La regla de fail-safe de §1.3 cubre el peor caso —proveedor sin confianza ⇒ derivado entero marcado incierto—. Y `DerivedRepresentation` **jamás sustituye al Source**: la profesional siempre puede escuchar el audio. **El diseño no depende de que el proveedor sea bueno; depende de que el sistema nunca presente su salida como más segura de lo que es.**

---

## Limitations

Lo que este spike **no** establece, dicho sin suavizar:

1. **Cero ejecución.** No se llamó a ningún proveedor, no se transcribió ningún audio, no se midió nada. **Nada aquí es "observed in current environment".** Todo es *documented platform claim* leído de páginas oficiales el **2026-08-24**.
2. **Un dato publicado no es una garantía de plataforma.** Límites, precios y capacidades cambian sin previo aviso y sin obligación contractual hacia nosotros. Deben re-verificarse en el momento de decidir y **anotarse con fecha** en el ADR que elija proveedor.
3. **El contrato no compila.** El TypeScript de este documento es conceptual: sin implementación, sin `package.json`, sin build, sin tests. Puede contener errores de tipos que solo un compilador revelaría.
4. **El `FixtureTranscriptionProvider` no pone a prueba el invariante: lo satisface trivialmente.** Al no transformar nada, nunca ejercita el camino de re-basado, que es donde vive el riesgo real. **El invariante temporal queda `NOT_TESTED` en v0** — con la particularidad, favorable, de que el contrato ya está diseñado para que el primer adapter real tenga que enfrentarlo explícitamente.
5. **Precisión temporal: `INCONCLUSIVE` para los cinco.** No por falta de búsqueda sino porque **nadie lo publica**. Solo se resuelve midiendo contra corpus propio etiquetado.
6. **Exactitud en español: sin dato utilizable.** Una sola banda declarada por un proveedor sobre sí mismo (AssemblyAI, *"≤ 10% WER"*), sin metodología publicada. No sustituye a una prueba con audio real del oficio: entrevistas, ruido de fondo, varios hablantes, léxico jurídico colombiano.
7. **Precio de Google y Azure: no obtenido.** Las páginas oficiales no entregaron cifras en la consulta. **No se sustituyó por memoria ni por terceros.**
8. **Retención y confidencialidad: no investigadas.** Qué hace cada proveedor con el audio subido —cuánto lo retiene, si lo usa para entrenar, dónde lo procesa— **no se consultó en este spike** y es material privilegiado. Es prerrequisito de cualquier decisión real, y probablemente más determinante que el precio.
9. **Diarización fuera de alcance.** El corpus ya lo fija: *"v0 no modela diarización y no se afirma su fiabilidad"* (Glosario §4). Varios proveedores la ofrecen; no se evaluó.

---

## Architecture implication

Seis consecuencias, de la más a la menos firme.

**1. El invariante temporal es una propiedad del adapter, no del proveedor — y eso es una buena noticia.**
Los cinco proveedores documentan sus offsets como **relativos al comienzo del audio enviado** (Google lo dice literalmente: *"Time offset relative to the beginning of the audio"*). **H2 confirmada.** Ninguno tiene el concepto de "audio original" ni puede tenerlo: no sabe qué es un `Source`. Por tanto el invariante **no puede delegarse en ningún proveedor, presente o futuro** — es responsabilidad estructural del adapter, y `TimelineAttestation` es el sitio donde esa responsabilidad se hace explícita, persistente y auditable en lugar de vivir en la cabeza de quien escribió el adapter.

**2. Quién cumple el invariante sin normalización de línea de tiempo.**

Distinción necesaria antes de responder: **normalización de unidades ≠ normalización de línea de tiempo**. Las cinco exigen lo primero (segundos → ms; ticks/ISO-8601 → ms) y eso es traducción mecánica, sin riesgo probatorio. Solo la segunda —re-basar offsets tras trocear— toca el invariante.

- **Cumplen con `transform: NONE`** (aceptan el original íntegro para audio jurídico realista): **Deepgram** (2 GB), **AssemblyAI** (5 GB / 10 h), **Azure** (batch 1 GB; fast <500 MB / <5 h). Los tres reciben el original entero y devuelven offsets sobre él. `rebased: false`.
- **Cumple con matices**: **Google STT v2** — 8 h de tope es holgado y `startOffset`/`endOffset` tienen la semántica correcta, pero **exige Cloud Storage** (ver punto 4) y no publica límite de bytes.
- **Exige normalización de línea de tiempo**: **OpenAI**, y no por su semántica de timestamps —que es correcta— sino por su **límite de 25 MB**, que fuerza troceo en material real. Adicionalmente, sus timestamps de palabra existen **solo en `whisper-1`**.

**3. El tamaño máximo de archivo es el criterio de selección dominante, por encima del precio y de la granularidad.**
H3 confirmada. La granularidad de timestamps es equivalente en los cinco (todos ofrecen palabra, con condiciones). El precio es despreciable a la escala prevista. **Lo que separa a los candidatos es si el original cabe entero**, porque de ahí depende que el adapter tenga o no que trocear, y trocear es la única operación de esta lista con riesgo probatorio.

**4. Los proveedores que exigen almacenamiento de objetos de terceros plantean un problema de ADR-002, no de rendimiento.**
**Google batch** *"is only able to transcribe audio stored in Cloud Storage"*; **Azure batch** requiere URI público accesible o Azure Blob Storage. Ambos obligan a **depositar una segunda copia del original privilegiado fuera del LEGAL OS PRIVATE STATE**, con su propio ciclo de vida, sus propios permisos y su propio borrado. **OpenAI, Deepgram y AssemblyAI aceptan subida directa en la petición** y no exigen esa copia persistente por diseño (lo cual **no** dice nada sobre qué retienen: ver *Limitations* §8). Azure ofrece **fast transcription** con subida directa, que esquiva el problema para archivos <500 MB. Por eso el port lleva `requires_external_object_storage` como capacidad explícita: es una **propiedad arquitectónica del adapter**, no un detalle de implementación.

**5. Ninguno de estos hallazgos toca el Domain — y esa es la verificación de que la arquitectura funciona.**
Cinco proveedores con cinco formas distintas de expresar el tiempo (segundos flotantes, milisegundos enteros, `Duration` protobuf, ISO-8601 con ticks de 100 ns), con confianza en niveles distintos y con límites que difieren en dos órdenes de magnitud. **Toda esa variedad muere en el adapter.** `DerivedRepresentation` no cambia. `EvidenceLink` no cambia. El invariante 5 de `Source` no cambia. El Domain no se entera de cuál se eligió — que es exactamente lo que la regla de dependencias del kernel §13 y ADR-006 prometían y aquí queda comprobado sobre un caso real.

**6. La incógnita sobre precisión temporal tiene una consecuencia de producto que conviene aceptar ya.**
Como nadie publica exactitud, `resolution_ms` es `null` y **el anclaje temporal de un `EvidenceLink` sobre audio debe presentarse como un rango a escuchar, no como un punto exacto**. Esto encaja sin fricción con lo ya aprobado: el mensaje de `UNCERTAIN_FRAGMENT` ya invita a escuchar el original, y `DerivedRepresentation` nunca lo sustituye. **Prometer precisión de milisegundos sobre una cifra que nadie ha medido sería exactamente el tipo de afirmación que este proyecto no hace.**

---

## Delete-keep recommendation

**KEEP — este documento (`experiments/transcription-spike/README.md`).** Es la única especificación existente del port `TranscriptionProvider` y la única verificación fechada de proveedores. Cierra el bloqueante n.º 3 de `vertical-slice-v0.md` en su parte de **diseño** (el contrato ya no depende de qué proveedor se elija) y lo acota en su parte de **verificación** (queda medición, no investigación documental).

**PROMOVER (no copiar) al Technical Design V0.** El contrato de §1.1–§1.6 debe subir al documento de ports & adapters de `docs/technical-design/v0/` cuando se escriba. Mientras viva solo aquí, es **nivel 6** (kernel §14): observación, no norma. Al promoverse, `src/` podrá implementarlo — hoy no, por la regla `src/` nunca importa de `experiments/`.

**NO CREAR todavía:** ningún adapter real, ninguna cuenta, ninguna clave. La decisión de proveedor **no está madura**: faltan los cuatro puntos de la lista de abajo.

**DELETE — nada.** Este spike no dejó código, dependencias ni configuración. No hay residuo que limpiar.

### Qué queda `POR VERIFICAR` antes de elegir proveedor

Ninguno de estos cuatro se resuelve leyendo más documentación. Los cuatro exigen ejecutar algo.

1. **Retención, confidencialidad y jurisdicción de procesamiento** de cada proveedor, sobre material privilegiado. **Es el primero y probablemente el decisivo.** Si un proveedor retiene o entrena con el audio, ninguna ventaja técnica lo compensa, y esto se decide antes que cualquier otra cosa.
2. **Precisión temporal medida**, contra corpus propio etiquetado. Determina el valor de `resolution_ms` y, con él, qué puede prometer la UX de anclaje. **Hoy `INCONCLUSIVE` para los cinco por ausencia de dato publicado.**
3. **Exactitud en español real del oficio** —entrevistas, ruido, varios hablantes, léxico jurídico colombiano— y si el `es-CO` de Azure aporta algo medible sobre `es-419` / `es-ES`. Hoy es **SUPUESTO**.
4. **Precio vigente de Google y Azure**, no obtenido de fuente oficial en esta consulta, más re-verificación fechada de los otros tres.

### Nota final de alcance

Este spike responde **qué contrato debe cumplir un proveedor** y **qué se puede afirmar hoy sobre cinco candidatos**. **No elige proveedor y no debe leerse como si lo hiciera.** Esa elección es un ADR, con los cuatro puntos anteriores resueltos y con la decisión de negocio sobre confidencialidad tomada por los dueños — no por un spike de nivel 6.
