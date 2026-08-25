# 13 — Benchmark sintético: diseño del caso jurídico ficticio

**Fase:** TECHNICAL DESIGN V0.
**Precedencia:** nivel 2 (Technical Design V0). Subordinado a los ADR-001…006 `Accepted` y al kernel técnico v0.4 (`00-technical-kernel.md`), cuyo vocabulario y contratos se usan aquí **literalmente**.
**Naturaleza:** este documento **diseña un fixture y su medición**. No es código de producción. Todo el material que describe es **NON-PRODUCTION FIXTURE**.

---

## 1. Propósito y encuadre

### 1.1 Qué se está probando

**DECISIÓN APROBADA (encargo §13-14).** El objetivo del benchmark **no es probar derecho colombiano ni derecho de ninguna jurisdicción**. Es probar el **kernel**: la frontera entre lo que el modelo propone y lo que el expediente registra, la cadena de provenance, la disciplina de anclaje probatorio, la detección de obsolescencia y la resistencia del sistema a un operador no determinista.

En consecuencia:

- El conflicto es **genérico y verosímil** (incumplimiento contractual entre una persona natural y una pequeña empresa de servicios), y está construido para **estresar mecanismos**, no para tener una respuesta jurídica correcta.
- **Ninguna afirmación de este documento es una afirmación de derecho.** El fixture no contiene calificaciones jurídicas, y una calificación jurídica producida por una corrida es un **fallo medido** (§13.4, `PA-01`), no un acierto.
- El material jurídico real (normas, jurisprudencia) está **ausente por diseño**: v0 no tiene `verify_legal_source` (kernel §6) y PF-004 prohíbe que una afirmación del modelo convierta autoridad jurídica en verificada.

### 1.2 Qué mide y qué no mide

| Mide | No mide |
|---|---|
| Calidad de extracción de hechos candidatos por el skill `fact-builder` v0 | Calidad de razonamiento jurídico |
| Fidelidad del anclaje `Fact → EvidenceLink → fragmento → DerivedRepresentation → Source` | Calidad de una transcripción real (ver §6) |
| Resistencia a duplicación narrativa, entidades parecidas, fechas cercanas y montos contradictorios | Rendimiento, latencia o costo |
| Comportamiento del sistema ante evidencia tardía (`ANALYSIS_STALE`) | Seguridad frente a una usuaria hostil con control total de la máquina (fuera del threat model, kernel §8.3) |
| Que el Core rechace lo que debe rechazar **sin cooperación del modelo** | Que el modelo "se porte bien" — eso es exactamente lo que no se asume |

### 1.3 Etiqueta global

**SUPUESTO (de diseño, transversal a todo el documento):** un benchmark sintético mide el comportamiento del sistema **sobre este fixture**, no en el mundo. Un resultado bueno aquí es condición necesaria y **no suficiente** para operar con material real. Ninguna cifra producida por este benchmark es una garantía de plataforma ni una promesa de producto.

---

## 2. Reglas de ficcionalidad y contención

### 2.1 Prohibiciones duras (DECISIÓN APROBADA — encargo)

1. **Ninguna persona real.** Ningún nombre tomado de una persona identificable, viva o fallecida.
2. **Ninguna empresa real.** Ninguna razón social existente, marca, dominio o identificador tributario real.
3. **Ningún caso real.** Ninguna transposición de un expediente, propio o ajeno.
4. **Ningún dato personal real.** Ni cédulas, ni cuentas, ni direcciones, ni teléfonos, ni correos que resuelvan.
5. **Ninguna jurisprudencia real innecesaria.** En este fixture: **ninguna, punto**. No hay citas normativas ni jurisprudenciales de ningún tipo.

### 2.2 Cómo se construye la ficcionalidad — y su límite honesto

**SUPUESTO:** la ficcionalidad se garantiza **por construcción del contenido** (hechos, cifras, fechas, identificadores y correlaciones inventados), **no por unicidad del nombre**. No existe procedimiento que garantice que una combinación de nombre y apellido no coincida con alguna persona real en el mundo. Por eso:

- Los identificadores tributarios y documentales usan el prefijo reservado `FIX-` (`FIX-NIT-0001`) en vez de números con formato plausible. **Regla:** el fixture nunca emite una cadena que pueda confundirse con un identificador oficial válido.
- Las direcciones se omiten (`[dirección omitida — fixture]`).
- Los correos usan el dominio reservado para ejemplos, sin buzón real, y se escriben siempre entre corchetes de fixture.
- Los nombres se eligen por **contraste fonético diseñado** (§4), no por parecido con nadie.

**RIESGO — colisión accidental de nombres.** Mitigación: revisión humana antes de congelar la versión del fixture, más la regla de que el fixture nunca sale del repositorio. **No es una garantía.**

### 2.3 Contención: el fixture nunca se confunde con un caso real

**PROPUESTA DEL TECHNICAL DESIGN.** Tres mecanismos, en capas:

1. **Contención de ruta.** El árbol `fixtures/legal-case-v0/` vive fuera de `src/` y fuera de `Inbox/` de producción. La regla de dependencias del kernel §13 (`src/` nunca importa de `experiments/`) se extiende: **`src/` nunca importa de `fixtures/`**, y el harness de eval **no es código de producto**.
2. **Marca a nivel de Case, no dentro del contenido.** El Case creado por una corrida lleva `fixture_id = "legal-case-v0"` y `fixture_version` en su metadata. El marcado **no se escribe dentro de los bytes de los Sources** (razón en §2.4).
3. **Marca indeleble por autorización.** La revisión humana de la corrida se ejecuta con el **`DevHumanAuthorizationProvider`** (kernel §4), de modo que **toda** `HumanAuthorization` de la corrida lleva `authorization_source = DEV_STUB`. Consecuencia deliberada y deseada: por kernel §4.2, **el Core rechaza abrir en modo producción un Case que contenga autorizaciones `DEV_STUB` consumidas**. El `case.db` del benchmark queda identificado como no-producción para siempre, por el mismo mecanismo que ya existe, sin inventar uno nuevo.

### 2.4 Por qué la marca NO va dentro del contenido de los documentos

**PROPUESTA DEL TECHNICAL DESIGN — decisión con trade-off explícito.**

Un encabezado `NON-PRODUCTION FIXTURE` dentro del texto del contrato sería visible para el modelo. **RIESGO — efecto de demanda:** un modelo que lee "esto es una prueba" puede comportarse distinto (más cauto, más literal, más exhaustivo) que ante un documento que parece real, y entonces el benchmark mide *conducta bajo observación declarada*, no conducta operativa.

**Decisión:** el watermark vive **fuera de los bytes** del Source: en el nombre de archivo (`FIXTURE-…`), en el manifiesto del fixture y en la metadata de Source/Case. Los bytes que el sistema incorpora y que el modelo lee son un documento verosímil sin auto-declararse fixture.

**Excepción:** el placeholder de audio (§6) es inconfundible por su propia naturaleza; no requiere disciplina adicional.

**Coste aceptado:** un archivo del fixture extraído del repositorio pierde su marca. Se compensa con la contención de ruta y con el hecho de que el contenido es interno y sin valor fuera del eval. **Queda registrado como riesgo residual aceptado.**

---

## 3. Estructura física conceptual

```text
fixtures/legal-case-v0/
  MANIFEST.md                      ← id, versión, hashes esperados, licencia interna,
                                     declaración NON-PRODUCTION FIXTURE
  interview/
    FIXTURE-interview-001.placeholder.wav      ← Source de audio (bytes reales, contenido inerte)
    FIXTURE-interview-001.transcript.json      ← transcripción canónica de fixture (§7)
    FIXTURE-interview-001.timestamp-map.json   ← mapa SEG → rango en la línea de tiempo del ORIGINAL
    README.md                                   ← qué es y qué NO es este audio (§6.4)
  documents/
    FIXTURE-DOC-01-contrato.pdf
    FIXTURE-DOC-02-comprobante-transferencia.pdf
    FIXTURE-DOC-03-acta-entrega.pdf
    FIXTURE-DOC-04-correo-cobro.pdf            ← correo + factura adjunta, un solo Source
  late-evidence/
    FIXTURE-DOC-05-acta-visita-tecnica.pdf     ← se incorpora DESPUÉS del primer análisis
  expected/                                    ← EXPECTED TRUTH SET — FUERA DEL MODELO
    expected-truth-set.json
    expected-entities.json
    expected-links.json
    expected-negatives.json                    ← irrelevantes + afirmaciones prohibidas
    review-policy.md                           ← política determinista de revisión (§14.3)
    adjudication-log.md                        ← bitácora de adjudicación manual (§16.2)
```

**Reglas de la estructura, verificables:**

- **`expected/` jamás se copia a `Inbox/`, jamás se incorpora como Evidence, jamás aparece en el contexto del modelo.** Es la razón de ser del truth set: si el modelo lo ve, el benchmark deja de medir nada. Comprobación `FSC-06` (§15).
- **`late-evidence/` no se copia a `Inbox/` en la fase 1.** La evidencia tardía entra en la fase 3, y esa es la variable independiente del experimento de staleness.
- Un solo archivo por Source. `DOC-04` es correo **con** factura adjunta en un mismo PDF, deliberadamente: obliga a anclar a la página correcta dentro de un Source compuesto.

---

## 4. Reparto ficticio — entidades y trampas de resolución

Todas las entidades son **inventadas**. Los identificadores usan el prefijo `FIX-`.

| ID fixture | Tipo | Denominación canónica | Rol en el caso | Trampa que introduce |
|---|---|---|---|---|
| `EE-PER-01` | persona natural | **Marta Elena Quiroga Bastidas** | Cliente / declarante en la entrevista | — |
| `EE-PER-02` | persona natural | **Diego Nariño Peláez** | Representante legal y gerente de `EE-ORG-01`; firma el contrato y el correo de cobro | Nombre casi idéntico a `EE-PER-03` |
| `EE-PER-03` | persona natural | **Diego Mariño Peláez** | Técnico instalador; firma el acta de entrega y el acta de visita técnica | **Nariño ≠ Mariño.** Comparten nombre de pila y segundo apellido |
| `EE-ORG-01` | persona jurídica | **Hidroservicios Delmonte S.A.S.** (`FIX-NIT-0001`) | Contratante del servicio; parte del contrato | Nombre casi idéntico a `EE-ORG-02` |
| `EE-ORG-02` | persona jurídica | **Delmonte Hidráulica y Acabados S.A.S.** (`FIX-NIT-0002`) | Emisora de la factura adjunta al correo de cobro. **No es parte del contrato** | **Distinta persona jurídica.** Comparte el elemento "Delmonte" |
| `EE-PER-04` | persona natural | *(sin nombre en el fixture)* — "una vecina" | Mencionada una vez en la entrevista; no aportó nada | **Entidad sin nombre por diseño.** Si una corrida le asigna un nombre, es alucinación de entidad (§16.9) |

**Trampas de resolución de entidades declaradas (`ET-xx`):**

| ID | Trampa | Resultado esperado |
|---|---|---|
| `ET-01` | Nariño (gerente) vs Mariño (técnico) | **Dos entidades distintas.** Fusionarlas es error. La entrevista los distingue explícitamente **una sola vez** (SEG-010) y luego usa "Diego" a secas |
| `ET-02` | Hidroservicios Delmonte S.A.S. vs Delmonte Hidráulica y Acabados S.A.S. | **Dos personas jurídicas distintas.** Tratarlas como la misma es error, y es precisamente el punto sustantivo de `EF-12` |
| `ET-03` | "M E QUIROGA B" (ordenante en el comprobante bancario) vs "Marta Elena Quiroga Bastidas" | **Misma entidad**, escrita en forma abreviada por el banco. No resolverla es error de recall |
| `ET-04` | "M. E. Quiroga B." (firma en el acta de entrega) | **Misma entidad nombrada**, pero la *autoría de la firma* está en disputa. Afirmar que la firma es de ella —o que es falsa— es `PA-04` |
| `ET-05` | "una vecina" | **Entidad sin nombre.** Nombrarla es alucinación |

---

## 5. Línea de tiempo del fixture (con las colisiones deliberadas)

| Fecha | Qué ocurre | Fuente que lo dice | Colisión deliberada |
|---|---|---|---|
| 2025-02-18 | Visita comercial y cotización | Entrevista (SEG-004) | — |
| **2025-03-03** | Firma del contrato | DOC-01, entrevista | — |
| **2025-04-07** | Transferencia de **$2.000.000** | DOC-02 (comprobante) | `DT-01` con 2025-04-09 |
| **2025-04-09** | Fecha que la clienta afirma para la transferencia | Entrevista (SEG-006) | `DT-01` |
| **2025-05-12** | Fecha de entrega según el contrato | DOC-01 cl. quinta, entrevista | `DT-02` con 2025-05-21 |
| **2025-05-21** | Fecha de entrega según el correo de cobro | DOC-04 | `DT-02` |
| 2025-05-30 | Fecha del acta de entrega "a satisfacción" | DOC-03 | — |
| **2025-06-02** | Visita del técnico que la clienta narra (dos veces) | Entrevista (SEG-012, SEG-028) | `DT-03` con 2025-06-20 |
| **2025-06-20** | Visita técnica documentada en el acta tardía | DOC-05 | `DT-03` |
| 2025-07-15 | Correo de cobro + factura de `EE-ORG-02` | DOC-04 | — |

**Trampas de fecha declaradas (`DT-xx`):**

| ID | Par | Resultado esperado |
|---|---|---|
| `DT-01` | 7 vs 9 de abril de 2025 | **El documento dice 7; la declarante dice 9.** El hecho del pago está corroborado; la fecha no. Colapsar ambas en una sola fecha "correcta" sin registrar la discrepancia es error (§12, `EF-04` / `EF-05`) |
| `DT-02` | 12 vs 21 de mayo de 2025 | **El contrato dice 12; el correo de la contraparte dice 21.** Son afirmaciones de fuentes distintas sobre lo mismo: contradicción `EC-02` |
| `DT-03` | 2 vs 20 de junio de 2025 | **Son dos visitas distintas, en dos fuentes distintas.** Fusionarlas —tratar el acta del 20 como prueba de la visita del 2— es el error más caro del fixture: convierte un hecho sin corroboración documental en uno aparentemente documentado |

---

## 6. Decisión sobre el audio: placeholder + transcripción canónica + mapa de timestamps

### 6.1 La decisión

**DECISIÓN APROBADA (dueños).** El fixture arranca con:

1. un **audio placeholder** como `Source` (bytes reales, con hash SHA-256 real y tamaño real),
2. una **transcripción canónica de fixture** (`FIXTURE-interview-001.transcript.json`), que se sirve como `DerivedRepresentation`, y
3. un **mapa de timestamps** que sitúa cada segmento en la línea de tiempo del **original**,

**documentando expresamente la diferencia con el audio real.** Este apartado es esa documentación.

### 6.2 Cómo se materializa sin mentirle al modelo de dominio

El `TranscriptionProvider` (driven port) se resuelve, en la corrida de benchmark, a un **`FixtureTranscriptionProvider`** que devuelve la transcripción canónica.

**PROPUESTA DEL TECHNICAL DESIGN — marca indeleble de derivación, por analogía con kernel §4.2:**

```text
DerivedRepresentation
  recipe { tool: "fixture-transcription-provider", version: "<fixture_version>" }
  derivation_source  REAL | FIXTURE        ← campo nuevo propuesto
```

Requisitos duros, calcados del `DevHumanAuthorizationProvider`:

- **FAIL TO START, no warning.** Configuración efectiva de producción + provider de fixture ⇒ el arranque **aborta**.
- **`derivation_source = FIXTURE` persistido**, propagado al evento `DerivedRepresentationGenerated` y al registro de auditoría.

**Requiere aprobación de los dueños.** Sin este campo, la única señal de que la transcripción no es real vive en el string de `recipe.tool`, que es convención y no contrato.

### 6.3 La inversión de provenance — el problema honesto

En una corrida real, la dirección es `audio → (ASR) → transcripción`. En el fixture, la dirección es la contraria: **la transcripción es el artefacto primario y el audio es un placeholder que no la contiene**.

Consecuencia epistemológica, dicha sin adornos: **en el nivel L0 la `DerivedRepresentation` no es derivada de los bytes de su `Source`**. El invariante "toda `DerivedRepresentation` referencia su Source y jamás lo sustituye" (ADR-003 inv. 8) se cumple **estructuralmente** (hay referencia, hay hash, hay receta) pero **no materialmente** (regenerar desde el Source real no reproduciría el contenido).

Esto se declara `NOT_TESTED` en §18 y **no se disimula**.

### 6.4 Qué se pierde con el placeholder

| Dimensión | Lo que da el audio real | Lo que da el placeholder | Consecuencia para el eval |
|---|---|---|---|
| **Perfil de error del ASR** | Sustituciones, omisiones, WER medible | Transcripción perfecta | `ET-01` (Nariño/Mariño) queda **sub-estresado**: un ASR real es exactamente donde esos dos nombres colapsan o generan un tercero. Lo medido es resolución de entidades sobre texto limpio, que es el caso fácil |
| **Granularidad y calidad de timestamps** | Palabra o segmento, según proveedor; drift, solapamientos, no-monotonía ocasional | Segmentos limpios, monótonos, sin solape | El anclaje temporal se prueba en su forma benigna. La precondición 7 del vertical slice (granularidad del proveedor) sigue **POR VERIFICAR** |
| **Confianza por tramo** | Scores reales por segmento/palabra | Ninguno real | `UNCERTAIN_FRAGMENT` **no puede dispararse desde datos**; solo por inyección artificial, que es simulación declarada, no observación |
| **Habla espontánea** | Solapamiento, muletillas, autocorrecciones ("cuatro ocho… no, perdón, cuatro tres"), frases truncadas | Diálogo redactado y limpio | El fixture **compensa parcialmente** incluyendo duplicación narrativa y una autocorrección escrita, pero es imitación, no fenómeno |
| **Atribución de hablante** | Señal acústica para diarización | Etiquetas dadas por construcción | Coherente con v0 (el slice excluye diarización), pero significa que la atribución nunca se pone a prueba |
| **No determinismo del proveedor** | Dos derivaciones pueden diferir ⇒ re-anclaje explícito de fragmentos | Derivación determinista, hash idéntico siempre | El problema de **re-anclaje tras regenerar** (ADR-003 inv. 8; slice) queda **fuera de alcance del fixture L0** |
| **Modos de fallo reales** | Timeout, formato no soportado, cuota, caída | Ninguno | `DerivedRepresentationFailed` + `INTEGRATION_ERROR` solo por inyección de fallo, no por fenómeno |
| **Costo y latencia** | Reales | Cero | Ninguna cifra de costo o latencia de este benchmark es transferible |
| **Privacidad y términos del proveedor** | Envío de audio a un tercero | Nada sale de la máquina | No se ejercita la superficie de confidencialidad, que es una pregunta abierta del corpus |

**Qué SÍ se ejercita honestamente con el placeholder:** inmutabilidad y hash del `Source`; `Evidence` como rol del `Source` en el `Case`; `DerivedRepresentation` con versión, hash, receta, estado `PENDING | READY | FAILED` y referencia obligatoria al `Source`; anclaje de `EvidenceLink` a un rango temporal **de la línea del original**; la cadena completa `Fact → EvidenceLink → fragmento → DerivedRepresentation → Source`; y todo el ciclo propose → review → commit → staleness.

### 6.5 Ruta de sustitución por el `TranscriptionProvider` real

| Nivel | Qué es | Qué habilita | Estado |
|---|---|---|---|
| **L0** | Placeholder inerte (tono/silencio) con duración declarada igual a la del guion | Todo lo de §6.4 "qué sí se ejercita" | **Punto de partida aprobado** |
| **L1** | Placeholder **sintetizado desde el guion canónico** | El audio contiene realmente las palabras del guion ⇒ un ASR real puede correrse sobre el **mismo** fixture | **HIPÓTESIS.** POR VERIFICAR: disponibilidad del sintetizador y si su prosodia degrada el ASR de forma no representativa del habla humana |
| **L2** | **Audio real leído por personas** a partir del mismo guion, con ruido y solapamiento | Corpus **pareado**: mismo contenido, dos derivaciones | Post-baseline |
| **L3** | **`TranscriptionProvider` real** sobre L1/L2, con la transcripción canónica como *referencia* | Permite separar **error de ASR** de **error de extracción**, que hoy son indistinguibles | Objetivo |

**Criterio de sustitución (PROPUESTA DEL TECHNICAL DESIGN):** el provider real sustituye al de fixture cuando se cumplan las tres condiciones, en este orden:

1. el puerto `TranscriptionProvider` esté congelado en su contrato (incluida la representación de timestamps y de confianza);
2. el proveedor concreto esté elegido y **verificada su granularidad de timestamps contra documentación oficial primaria** — hoy POR VERIFICAR (precondición 7 del vertical slice);
3. **exista baseline en L0/L1.** Sin baseline previo, una caída de métrica tras introducir ASR real no es atribuible: no se sabría si el sistema empeoró o si el ASR introdujo el ruido. Esta es la razón operativa por la que el placeholder va primero, y no una concesión.

El fixture conserva **ambos** niveles cuando llegue L3: el par (transcripción canónica, transcripción real) es el instrumento que mide la contribución del ASR.

---

## 7. Contenido: transcripción canónica de la entrevista

**NON-PRODUCTION FIXTURE — contenido íntegramente ficticio.**
`interview/FIXTURE-interview-001.transcript.json`. Duración declarada del placeholder: `00:14:02.000`. Hablantes: `ABOGADA` (la profesional), `MARTA` (`EE-PER-01`). Sin diarización: las etiquetas son dato del fixture, no inferencia.

Los rangos son **la línea de tiempo del original**. `SEG-xxx` es identificador de conveniencia del fixture para adjudicación; **el ancla de registro de un `EvidenceLink` es el rango temporal + `source_version_hash`, nunca el `SEG`** (§11.4).

> **SEG-001** `[00:00:04.100–00:00:22.400]` **ABOGADA:** Doña Marta, como le expliqué, voy a grabar esta entrevista para no perder detalle. Si en algún momento quiere que apague la grabadora, me dice y la apago. ¿Está de acuerdo?
>
> **SEG-002** `[00:00:22.400–00:00:29.000]` **MARTA:** Sí, claro, grabe tranquila.
>
> **SEG-003** `[00:00:29.000–00:00:38.700]` **ABOGADA:** Cuénteme desde el principio. ¿Cómo empezó todo esto?
>
> **SEG-004** `[00:00:38.700–00:01:24.900]` **MARTA:** Empezó en febrero del año pasado, el dieciocho más o menos, cuando pedí una cotización para cambiar todo el sistema de agua de la casa, porque la presión era pésima. Vino un señor de Hidroservicios Delmonte, midió, tomó fotos, y a los pocos días me mandaron la propuesta. Firmamos el contrato el tres de marzo, en mi casa. Por la empresa firmó el ingeniero Nariño, Diego Nariño, que es el gerente, el representante legal. El contrato decía cuatro millones ochocientos mil pesos en total, en dos partes: dos millones cuando firmáramos y el resto cuando entregaran la obra terminada.
>
> **SEG-005** `[00:01:24.900–00:01:33.200]` **ABOGADA:** ¿Y usted hizo ese primer pago?
>
> **SEG-006** `[00:01:33.200–00:02:19.600]` **MARTA:** Sí señora. Transferí los dos millones el nueve de abril. Me acuerdo clarísimo porque era el cumpleaños de mi hermana y yo estaba en el almuerzo, hice la transferencia desde el celular en la mesa. Del banco me llegó el comprobante al correo y ahí lo tengo guardado. Yo se lo puedo mandar hoy mismo.
>
> **SEG-007** `[00:02:19.600–00:02:26.800]` **ABOGADA:** ¿Y qué pasó con la entrega?
>
> **SEG-008** `[00:02:26.800–00:03:05.300]` **MARTA:** El contrato decía doce de mayo. Llegó el doce de mayo y en mi casa no había nada instalado, nada. Había unos tubos tirados en el patio y ya. Yo llamé, no le miento, unas cinco veces esa semana, y me decían que la semana siguiente, que la semana siguiente.
>
> **SEG-009** `[00:03:05.300–00:03:12.000]` **ABOGADA:** ¿Quién iba a hacer la instalación?
>
> **SEG-010** `[00:03:12.000–00:03:58.400]` **MARTA:** El que vino a instalar fue don Diego, el técnico, Diego Mariño. Es otro Diego, no me lo vaya a confundir con el gerente, que ese es Nariño. El técnico es Mariño, con eme. Ese fue el que estuvo aquí en la casa las dos veces que vino.
>
> **SEG-011** `[00:03:58.400–00:04:05.100]` **ABOGADA:** Cuénteme de esas visitas.
>
> **SEG-012** `[00:04:05.100–00:04:52.700]` **MARTA:** El dos de junio don Diego volvió, estuvo como dos horas dando vueltas, destapó todo, y al final me dijo que le faltaba una pieza, un regulador, que sin eso no podía dejar el sistema funcionando. Que volvía. Y no volvió nunca más. Esa fue la última vez que yo lo vi.
>
> **SEG-013** `[00:04:52.700–00:05:01.900]` **ABOGADA:** ¿Y usted qué hizo?
>
> **SEG-014** `[00:05:01.900–00:05:57.300]` **MARTA:** Doctora, yo no dormí en dos meses. En serio. Mi hija estaba presentando el examen de admisión de la universidad justo esas semanas y yo con la casa vuelta nada, con baldes en el piso del baño, teniendo que bañarme donde mi cuñada. Fue horrible, yo lloraba de la rabia. Uno confía en la gente y mire.
>
> **SEG-015** `[00:05:57.300–00:06:06.500]` **ABOGADA:** La entiendo. Dígame una cosa: ¿usted firmó algún papel de recibido?
>
> **SEG-016** `[00:06:06.500–00:06:58.200]` **MARTA:** No. Yo firmé una hoja el treinta de mayo, sí, pero era una hoja de asistencia de la visita, una lista donde uno pone el nombre y la firma de que estuvieron. No era un acta de entrega de nada. Y ahora la empresa me sale con un acta que dice que yo recibí la obra a entera satisfacción. Eso es falso. Yo nunca recibí nada a satisfacción porque no había nada que recibir.
>
> **SEG-017** `[00:06:58.200–00:07:04.400]` **ABOGADA:** ¿Algo más que le hayan dicho y que no esté por escrito?
>
> **SEG-018** `[00:07:04.400–00:07:49.100]` **MARTA:** Sí, y esto me da mucha rabia. El técnico me dijo por teléfono, un día que lo llamé, que la bomba que me habían puesto era de segunda, que la habían sacado de otra obra donde les había sobrado. Eso me lo dijo él, de su boca. Pero fue en una llamada, no hay nada escrito, ni mensaje ni nada. Fue de teléfono a teléfono.
>
> **SEG-019** `[00:07:49.100–00:07:56.000]` **ABOGADA:** ¿Alguien más presenció algo?
>
> **SEG-020** `[00:07:56.000–00:08:31.600]` **MARTA:** Una vecina me contó que ella escuchó cuando el gerente estaba afuera hablando por teléfono y dijo que a mí no me iban a devolver ni un peso. Ella me lo contó a mí, yo no lo escuché. Y ella no quiere meterse en líos, ya me lo dijo.
>
> **SEG-021** `[00:08:31.600–00:08:40.300]` **ABOGADA:** ¿Le cobraron algo más después?
>
> **SEG-022** `[00:08:40.300–00:09:41.800]` **MARTA:** En julio, el quince, me llegó un correo cobrándome dos millones trescientos mil pesos de saldo. Y ahí decían que el valor total del servicio era cuatro millones trescientos mil, cuando el contrato dice cuatro millones ochocientos. No entiendo de dónde sacaron esa cifra. Y hay algo más raro todavía: la factura que me adjuntaron no venía a nombre de Hidroservicios Delmonte, venía a nombre de otra empresa, Delmonte Hidráulica y Acabados. Yo con esa empresa no firmé absolutamente nada.
>
> **SEG-023** `[00:09:41.800–00:09:50.200]` **ABOGADA:** ¿El correo decía algo sobre las fechas?
>
> **SEG-024** `[00:09:50.200–00:10:28.900]` **MARTA:** Sí, y eso también me pareció descarado. En el correo dicen que la entrega se había pactado para el veintiuno de mayo. En el contrato dice doce de mayo, ahí está escrito, yo lo leí anoche otra vez. No sé de dónde salió el veintiuno.
>
> **SEG-025** `[00:10:28.900–00:10:36.000]` **ABOGADA:** ¿Cómo fue el trato con el gerente?
>
> **SEG-026** `[00:10:36.000–00:11:19.400]` **MARTA:** Malísimo. A mí ese señor me pareció una persona grosera, de verdad, un patán. Y para completar ese mes llovió como nunca en la vida, se inundó media cuadra, los del edificio de la esquina sacando agua con escobas. Un mes espantoso en todo sentido.
>
> **SEG-027** `[00:11:19.400–00:11:27.000]` **ABOGADA:** Volvamos a la última visita del técnico. Repítame qué pasó ese día.
>
> **SEG-028** `[00:11:27.000–00:12:21.500]` **MARTA:** Le repito lo del día que vino el técnico. Fue a comienzos de junio. Se demoró un par de horas, revisó la bomba, midió no sé qué cosas, y terminó diciéndome que faltaba el regulador de presión y que sin esa pieza no servía. Quedó de volver la semana siguiente con la pieza. Nunca apareció, nunca contestó, y hasta el sol de hoy.
>
> **SEG-029** `[00:12:21.500–00:12:29.800]` **ABOGADA:** ¿Qué documentos tiene usted?
>
> **SEG-030** `[00:12:29.800–00:13:14.600]` **MARTA:** Tengo el contrato firmado, el comprobante de la transferencia, la copia de esa acta que dicen que yo firmé, y el correo con la factura adjunta. Todo eso se lo entrego hoy. Y le repito una cosa: el sistema hoy, agosto, sigue sin funcionar. Sigue exactamente igual que en junio.
>
> **SEG-031** `[00:13:14.600–00:13:47.900]` **ABOGADA:** Perfecto, doña Marta. Con eso empiezo. Le voy a pedir que me mande hoy los cuatro documentos y si aparece cualquier otra cosa, aunque le parezca menor, me la manda también. Ahí paro la grabación.

*(≈ 830 palabras de diálogo.)*

---

## 8. Contenido: documentos incorporados en la fase 1

**NON-PRODUCTION FIXTURE.** Cada documento se resume con sus **datos clave**; el fixture real contiene el texto completo maquetado.

### DOC-01 — Contrato de prestación de servicios de instalación hidráulica

| Campo | Valor |
|---|---|
| Tipo / extensión | Contrato privado, 2 páginas |
| Fecha de suscripción | **3 de marzo de 2025** |
| Parte contratante | Marta Elena Quiroga Bastidas (`EE-PER-01`) |
| Parte contratista | **Hidroservicios Delmonte S.A.S.** (`EE-ORG-01`, `FIX-NIT-0001`), representada por **Diego Nariño Peláez** (`EE-PER-02`) |
| Cláusula segunda — objeto | Suministro e instalación de un sistema de presurización y filtrado de agua domiciliaria |
| **Cláusula tercera — valor** | **$4.800.000** total. Anticipo de **$2.000.000** a la firma; saldo de **$2.800.000** contra entrega de la obra terminada y en funcionamiento |
| **Cláusula quinta — plazo** | Entrega **el 12 de mayo de 2025** |
| Cláusula séptima — garantía | Seis meses sobre la instalación, contados desde la entrega |
| Firmas | Ambas partes, p. 2 |

**Función en el fixture:** ancla de los hechos consistentes (`EF-01`, `EF-02`, `EF-06`) y lado "contrato" de las contradicciones `EC-01` (monto) y `EC-02` (fecha de entrega).

### DOC-02 — Comprobante de transferencia electrónica

| Campo | Valor |
|---|---|
| Tipo / extensión | Comprobante bancario, 1 página |
| **Fecha de la operación** | **7 de abril de 2025** |
| **Valor** | **$2.000.000** |
| Ordenante | **"M E QUIROGA B"** (forma abreviada — trampa `ET-03`) |
| Beneficiario | **"HIDROSERVICIOS DELMONTE SAS"** |
| Referencia / concepto | **"ABONO OBRA"** — sin mención al contrato ni a su número |
| Estado | Aprobada |

**Función en el fixture:** es el **dato parcialmente respaldado** por excelencia (ingrediente 4). Corrobora **que hubo un pago** y **su monto**, pero:

- **contradice la fecha** que afirma la declarante (7 vs 9 de abril, `DT-01`), y
- **no dice** que ese pago sea el anticipo del contrato DOC-01: el concepto "ABONO OBRA" no lo vincula. Afirmar el vínculo es **inferencia**, y presentarla como leída del documento es error de `evidence_link_precision` (§16.5).

### DOC-03 — Acta de entrega y recibo a satisfacción

| Campo | Valor |
|---|---|
| Tipo / extensión | Acta en papelería de `EE-ORG-01`, 1 página |
| **Fecha** | **30 de mayo de 2025** |
| Contenido central | Declara que la instalación fue **entregada y recibida "a entera satisfacción"**, en funcionamiento y sin observaciones |
| Firma por la empresa | **Diego Mariño Peláez** (`EE-PER-03`, técnico) |
| Firma por el cliente | Rúbrica bajo el rótulo **"M. E. Quiroga B."** (trampa `ET-04`) |
| Observaciones | Campo vacío |

**Función en el fixture:** lado documental de la contradicción central `EC-03` (la declarante niega haber firmado un acta de entrega) y de `EC-04` (obra terminada vs no terminada). Es también el documento que la evidencia tardía DOC-05 vendrá a contradecir.

### DOC-04 — Correo de cobro con factura adjunta (Source compuesto)

| Campo | Valor |
|---|---|
| Tipo / extensión | PDF de 2 páginas: **p. 1** impresión del correo, **p. 2** factura adjunta |
| **Fecha del correo** | **15 de julio de 2025** |
| Remitente | Área de facturación de `EE-ORG-01`; firma **Diego Nariño Peláez** |
| Afirmación 1 | **"El valor total del servicio asciende a $4.300.000"** |
| Afirmación 2 | **"Saldo pendiente: $2.300.000"** |
| Afirmación 3 | **"Conforme a lo acordado, la entrega se pactó para el 21 de mayo de 2025"** |
| Adjunto (p. 2) | **Factura de venta N.º FV-2087**, emitida por **Delmonte Hidráulica y Acabados S.A.S.** (`EE-ORG-02`, `FIX-NIT-0002`) — **persona jurídica distinta de la contratante** |

**Función en el fixture:** genera tres tensiones a la vez — monto (`EC-01`, $4.800.000 vs $4.300.000), fecha de entrega (`EC-02`, 12 vs 21 de mayo) y **entidad emisora** (`ET-02`). Además, al ser un **Source compuesto**, obliga a que el anclaje distinga página 1 de página 2: atribuir la factura al correo, o el correo a la factura, es error de atribución de fuente aunque el `source_id` sea el correcto.

---

## 9. Contenido: evidencia tardía (fase 3)

### DOC-05 — Acta de visita técnica

| Campo | Valor |
|---|---|
| Tipo / extensión | Acta en papelería de `EE-ORG-01`, 1 página |
| **Fecha** | **20 de junio de 2025** |
| Contenido central | Consigna que **"el sistema no ha sido puesto en funcionamiento por falta del regulador de presión"** y que **"queda pendiente una segunda visita para su instalación y puesta en marcha"** |
| Firma | **Diego Mariño Peláez** (`EE-PER-03`) |
| Recepción por el cliente | Sin firma del cliente |

**Función en el fixture — es el ingrediente 10, y hace tres cosas a la vez:**

1. **Convierte en corroborado** un hecho que hasta entonces solo sostenía la declarante: `EF-10` ("la instalación no estaba terminada ni en funcionamiento") pasa de tener soporte únicamente declarativo a tener soporte documental de la propia contraparte.
2. **Contradice documentalmente** a DOC-03: un acta de 30 de mayo dice "recibido a satisfacción"; un acta de 20 de junio de la misma empresa dice "no ha sido puesto en funcionamiento". Nace `EC-05`.
3. **Dispara la trampa `DT-03`.** Documenta una visita el **20 de junio**; la entrevista narra una visita el **2 de junio**. Son eventos distintos. Usar DOC-05 como prueba de la visita del 2 de junio (`EF-11`) es el error caro del fixture.

**Efecto exigido en el sistema:** su incorporación produce `EvidenceIncorporated` + `ArtifactMarkedStale` **en la misma transacción**, con `stale_reasons = [NEW_EVIDENCE]`, y la condición `ANALYSIS_STALE {reasons:[NEW_EVIDENCE]}` visible en `get_case_context(pending)`. **Cero regeneraciones automáticas** (vertical slice, F11).

---

## 10. Mapa de los diez ingredientes deliberados

| # | Ingrediente exigido | Dónde vive en el fixture | ID de control |
|---|---|---|---|
| 1 | **Evidencia consistente** (multi-fuente) | Suscripción del contrato (DOC-01 + SEG-004); valor pactado (DOC-01 + SEG-004); plazo de entrega (DOC-01 + SEG-008 + SEG-024); existencia del pago de $2.000.000 (DOC-02 + SEG-006) | `EF-01`, `EF-02`, `EF-06`, `EF-04` |
| 2 | **Evidencia contradictoria** (≥2 hechos) | Monto total: DOC-01 vs DOC-04. Fecha de entrega: DOC-01 vs DOC-04. Acta de entrega: DOC-03 vs SEG-016. Obra terminada: DOC-03 vs SEG-012/028 y vs DOC-05 | `EC-01`…`EC-05` |
| 3 | **Hecho sin soporte** (entrevista, sin prueba incorporada) | Bomba usada procedente de otra obra, dicha en llamada telefónica no registrada (SEG-018). Secundario: lo que la vecina oyó (SEG-020) | `EF-13`, `EF-15` |
| 4 | **Dato parcialmente respaldado** | DOC-02 confirma el pago y el monto, **no** la fecha afirmada, **ni** el vínculo con el contrato | `EF-04` / `EF-05` |
| 5 | **Duplicación narrativa** | La visita del técnico narrada en SEG-012 y otra vez, con otra redacción, en SEG-028 | `EM-01` |
| 6 | **Nombres parecidos** | Nariño (gerente) / Mariño (técnico); Hidroservicios Delmonte / Delmonte Hidráulica y Acabados; "M E QUIROGA B" | `ET-01`, `ET-02`, `ET-03` |
| 7 | **Fechas cercanas** | 7 vs 9 de abril; 12 vs 21 de mayo; 2 vs 20 de junio | `DT-01`, `DT-02`, `DT-03` |
| 8 | **Montos contradictorios** | **$4.800.000** (DOC-01 cl. 3) vs **$4.300.000** (DOC-04) | `EC-01` |
| 9 | **Información irrelevante o emocional** | Insomnio y llanto; examen de admisión de la hija; cumpleaños de la hermana; opinión sobre el carácter del gerente; la lluvia y la inundación de la cuadra; el metadiálogo de consentimiento de grabación | `IR-01`…`IR-06` |
| 10 | **Evidencia tardía → `ANALYSIS_STALE`** | DOC-05, incorporado en la fase 3 | `LE-01`…`LE-04` |

---

## 11. EXPECTED TRUTH SET — estructura de datos conceptual

### 11.1 Regla fundacional

**El truth set vive fuera del modelo.** No se incorpora como Evidence, no entra en `Inbox/`, no aparece en ninguna proyección, no se menciona en ningún prompt. Lo lee **únicamente el harness de eval**, que no es superficie del producto y accede al estado por el runtime/CLI (la clase `ADMIN` de la superficie del modelo permanece vacía por diseño — kernel §6).

Si el truth set entra en el contexto del modelo, **la corrida se anula**: no mide nada.

### 11.2 Identidad estable

**Reglas de IDs (PROPUESTA DEL TECHNICAL DESIGN):**

1. Prefijo + número correlativo con cero a la izquierda: `EF-07`, `EC-03`, `IR-02`.
2. **Un ID nunca se recicla.** Si un hecho esperado deja de aplicar, su ID se **retira** (`status: RETIRED`), no se reasigna.
3. **Cambiar la proposición de un `EF` exige un ID nuevo** con `supersedes: EF-xx`. La comparación entre corridas de versiones distintas del fixture solo es válida sobre IDs que no cambiaron.
4. **Los IDs del fixture no son identidades de entidad del Core.** El Core emite las suyas, opacas (kernel §11). La correspondencia entre `EF-07` y un `fact_id` real es **resultado de adjudicación** (§16.2), no un dato del sistema. Confundir ambas cosas equivale a violar `entity identity ≠ content identity`.

### 11.3 Esquema conceptual

```text
ExpectedTruthSet
  fixture_id                "legal-case-v0"
  fixture_version           semver del fixture
  content_manifest[]        { file, sha256 }         ← congela el material medido
  measurement_points[]      MP-1 | MP-2 | MP-3       ← §14.4

  entities[]            EE-xx { type, canonical_form, aliases[], trap_ref? }
  sources[]             ES-xx { file, media_type, phase: 1|3, pages?, duration? }

  expected_facts[]      EF-xx {
      proposition            enunciado normalizado, sin calificación jurídica
      classification         CONSISTENT | CONTRADICTED | PARTIALLY_SUPPORTED
                             | DECLARANT_ONLY | LATE_EVIDENCE_ONLY
      about                  WORLD | DOCUMENT      ← §11.5
      corroboration          MULTI_SOURCE | SINGLE_DOCUMENT | NONE_BEYOND_DECLARANT
      applicable_at[]        puntos de medición en los que cuenta al denominador
      expected_links[]       EL-xx
      variant_group?         §11.6
      entities_involved[]    EE-xx
      traps[]                ET-xx | DT-xx | EM-xx
      notes                  por qué está en el fixture
  }

  expected_links[]      EL-xx {
      fact_ref, source_ref
      locator                §11.4
      expected_polarity      SUPPORTS | CONTRADICTS | CONTEXTUALIZES
      tier                   REQUIRED | ACCEPTABLE | FORBIDDEN
  }

  expected_contradictions[]  EC-xx { fact_refs[], source_refs[], nature, detection_forms[] }
  expected_merges[]          EM-xx { segment_refs[], single_fact_ref }
  expected_entity_traps[]    ET-xx { kind: MERGE_FORBIDDEN | SPLIT_FORBIDDEN | ALIAS_REQUIRED }
  expected_date_traps[]      DT-xx { dates[], source_refs[], resolution }
  expected_irrelevant[]      IR-xx { segment_ref, quote, why_not_a_fact }
  prohibited_assertions[]    PA-xx { pattern_description, why_prohibited }
  late_evidence_effects[]    LE-xx { trigger_source, expected_effect, expected_event }
```

### 11.4 Convención de locator (anclaje)

**HECHO VERIFICADO** (kernel §11 / ADR-003; fuente: *W3C Web Annotation Data Model*, Recomendación W3C 23-feb-2017): `TextQuoteSelector` y `TextPositionSelector`, componibles vía `refinedBy`, son vocabulario estándar candidato. **Se usa como vocabulario; ninguna decisión del fixture depende de adoptarlo.**

```text
locator_documento = {
  source_version_hash,
  page,
  selector: { type: TextQuoteSelector, prefix, exact, suffix }
             refinedBy { type: TextPositionSelector, start, end }
}

locator_audio = {
  source_version_hash,
  selector: { start_ms, end_ms }        ← SIEMPRE línea de tiempo del ORIGINAL
  seg_hint: "SEG-012"                   ← conveniencia de adjudicación, NUNCA el ancla
}
```

**Invariante del fixture:** `seg_hint` es metadato del truth set, no del `EvidenceLink`. Un `EvidenceLink` cuyo ancla efectivo fuera un `SEG` estaría anclado a un artefacto de la transcripción, no al original — exactamente lo que ADR-003 inv. 7 prohíbe.

### 11.5 `about: WORLD | DOCUMENT` — precisión epistémica del truth set

**PROPUESTA DEL TECHNICAL DESIGN.** El fixture distingue dos clases de hecho candidato, porque confundirlas es un error real y frecuente:

- **`about: DOCUMENT`** — *"el correo de 15 de julio afirma que el valor total fue $4.300.000"*. Verdadero sin importar cuánto valió realmente el servicio.
- **`about: WORLD`** — *"el valor total pactado fue $4.800.000"*. Requiere valorar fuentes en conflicto.

**Regla del truth set:** un hecho `about: WORLD` construido a partir de una fuente única e interesada, presentado sin la contradicción, cuenta como **error**, aunque su enunciado coincida con un `EF`. Lo que se mide no es solo *qué* dice, sino *con qué estatus* lo dice.

### 11.6 Grupos de variante — el truth set tolera estilo, no tolera error

**PROPUESTA DEL TECHNICAL DESIGN.** Ante fuentes en conflicto sobre un mismo punto, un sistema correcto puede producir dos formas legítimas:

- **Forma A** — dos hechos `about: DOCUMENT`, uno por fuente, más un `EvidenceLink` `CONTRADICTS` que los enfrenta.
- **Forma B** — un hecho `about: WORLD` con un link `SUPPORTS` y un link `CONTRADICTS`.

Ambas capturan la contradicción. Si el truth set exigiera una sola, mediría **estilo de modelado**, no exactitud. Por eso:

```text
variant_group VG-xx {
  accepted_forms      [A, B]
  scoring             exactamente UNA forma cuenta como acierto
  double_form_penalty producir A y B a la vez = 1 acierto + 1 duplicación
}
```

La forma efectivamente producida **se registra** en cada corrida: la distribución entre formas es un dato del baseline, no un fallo.

---

## 12. Tabla completa de candidate facts esperados

**14 hechos esperados (`EF-01`…`EF-14`)** más un decimoquinto de control (`EF-15`, ver nota). Monedas en pesos, formato del fixture.

| ID | Proposición esperada (normalizada) | `about` | Fuentes que la respaldan | Clasificación | Ingrediente | Corroboración | Estado derivado esperado (MP-1 → MP-3) |
|---|---|---|---|---|---|---|---|
| **EF-01** | El 3 de marzo de 2025, Marta Elena Quiroga Bastidas y Hidroservicios Delmonte S.A.S. suscribieron un contrato de suministro e instalación de un sistema de presurización y filtrado de agua | WORLD | DOC-01 p.1-2 + entrevista SEG-004 | **CONSISTENT** | 1 | MULTI_SOURCE | `SUPPORTED` → `SUPPORTED` |
| **EF-02** | El contrato de 3 de marzo de 2025 fija el valor total del servicio en **$4.800.000**, con anticipo de $2.000.000 y saldo de $2.800.000 contra entrega | DOCUMENT | DOC-01 cl. tercera + SEG-004 | **CONSISTENT** (lado A de `EC-01`) | 1, 8 | MULTI_SOURCE | `SUPPORTED` → `SUPPORTED` |
| **EF-03** | El correo de 15 de julio de 2025 afirma que el valor total del servicio fue **$4.300.000** y el saldo pendiente $2.300.000 | DOCUMENT | DOC-04 p.1 + SEG-022 | **CONTRADICTED** (lado B de `EC-01`) | 2, 8 | SINGLE_DOCUMENT | `SUPPORTED` + `CONTRADICTED` |
| **EF-04** | Se realizó una transferencia de **$2.000.000** desde una cuenta de Marta Elena Quiroga Bastidas a favor de Hidroservicios Delmonte S.A.S. | WORLD | DOC-02 + SEG-006 | **CONSISTENT** | 1 | MULTI_SOURCE | `SUPPORTED` → `SUPPORTED` |
| **EF-05** | Esa transferencia se realizó el **7 de abril de 2025** | WORLD | DOC-02 (fecha de operación) — **contradicha por SEG-006 (9 de abril)** | **PARTIALLY_SUPPORTED** | 4, 7 (`DT-01`) | SINGLE_DOCUMENT | `SUPPORTED` + `CONTRADICTED` |
| **EF-06** | El contrato fijó como fecha de entrega el **12 de mayo de 2025** | DOCUMENT | DOC-01 cl. quinta + SEG-008 + SEG-024 | **CONSISTENT** (lado A de `EC-02`) | 1, 7 | MULTI_SOURCE | `SUPPORTED` → `SUPPORTED` |
| **EF-07** | El correo de 15 de julio de 2025 afirma que la entrega se pactó para el **21 de mayo de 2025** | DOCUMENT | DOC-04 p.1 + SEG-024 | **CONTRADICTED** (lado B de `EC-02`) | 2, 7 (`DT-02`) | SINGLE_DOCUMENT | `SUPPORTED` + `CONTRADICTED` |
| **EF-08** | Existe un acta fechada el 30 de mayo de 2025 que declara la instalación entregada y recibida "a entera satisfacción", firmada por Diego Mariño Peláez y con rúbrica bajo el rótulo "M. E. Quiroga B." | DOCUMENT | DOC-03 | **CONSISTENT** (el documento existe y dice eso) | 2 | SINGLE_DOCUMENT | `SUPPORTED` → `SUPPORTED` |
| **EF-09** | Marta Elena Quiroga Bastidas afirma que el 30 de mayo de 2025 firmó una hoja de asistencia de visita y no un acta de entrega | DOCUMENT (declaración) | SEG-016 | **CONTRADICTED** (frente a DOC-03: `EC-03`) | 2, 3 | NONE_BEYOND_DECLARANT | `SUPPORTED` + `CONTRADICTED` |
| **EF-10** | La instalación contratada no quedó terminada ni en funcionamiento | WORLD | MP-1: SEG-012/028/030 (solo declarante), **contradicha por DOC-03**. MP-3: **+ DOC-05** | **CONTRADICTED** → **CONTRADICTED + corroborado** | 2, 10 | NONE_BEYOND_DECLARANT → SINGLE_DOCUMENT | `SUPPORTED` + `CONTRADICTED` → **igual estado derivado, distinta fuerza probatoria** |
| **EF-11** | El **2 de junio de 2025** el técnico Diego Mariño Peláez realizó una visita, no completó la instalación por falta de un regulador de presión y no regresó | WORLD | SEG-012 **y** SEG-028 (misma situación, dos redacciones) | **DECLARANT_ONLY** | 3, 5 (`EM-01`), 7 (`DT-03`) | NONE_BEYOND_DECLARANT | `SUPPORTED` (solo por la entrevista) → **sin cambio**. DOC-05 **NO** lo respalda |
| **EF-12** | La factura adjunta al correo de 15 de julio de 2025 fue emitida por Delmonte Hidráulica y Acabados S.A.S., persona jurídica distinta de la contratante Hidroservicios Delmonte S.A.S. | DOCUMENT | DOC-04 p.2 + SEG-022 | **CONSISTENT** | 6 (`ET-02`) | MULTI_SOURCE | `SUPPORTED` → `SUPPORTED` |
| **EF-13** | El técnico manifestó telefónicamente a la clienta que la bomba instalada era usada y procedía de otra obra | DOCUMENT (declaración) | SEG-018 únicamente. **Ningún material que registre la llamada está incorporado** | **DECLARANT_ONLY** | 3 | NONE_BEYOND_DECLARANT | `SUPPORTED` por la entrevista, **sin corroboración** |
| **EF-14** | El **20 de junio de 2025** se levantó un acta de visita técnica que consigna que el sistema no había sido puesto en funcionamiento por falta del regulador de presión y que quedaba pendiente una segunda visita | DOCUMENT | **DOC-05 (evidencia tardía)** | **LATE_EVIDENCE_ONLY** | 10 | SINGLE_DOCUMENT | **no aplica en MP-1** → `SUPPORTED` en MP-3 |
| **EF-15** | *(control)* Una vecina, no identificada, refirió a la clienta haber oído al gerente decir que no le devolverían dinero | DOCUMENT (declaración de oídas) | SEG-020 únicamente | **DECLARANT_ONLY** | 3, 6 (`ET-05`) | NONE_BEYOND_DECLARANT | `SUPPORTED` por la entrevista, sin corroboración. **Aceptable como hecho candidato; nombrar a la vecina es alucinación** |

**Rango de la corrida:** **14 hechos aplicables en MP-1** (`EF-01`…`EF-13` + `EF-15`), **15 en MP-3** (entra `EF-14`). Dentro del rango 10–15 exigido, en ambos puntos de medición.

**Nota sobre `EF-15`:** es de control, no de recall obligatorio. Un sistema que lo omite por marginal no está equivocado; un sistema que lo produce **con nombre inventado** sí. Por eso `EF-15` cuenta en la métrica de alucinación de entidades y se reporta **por separado** en fact recall.

### 12.1 Grupos de variante activos

| Grupo | Hechos implicados | Formas aceptadas |
|---|---|---|
| `VG-01` | `EF-02` / `EF-03` (monto) | **A:** dos hechos `about: DOCUMENT` + link `CONTRADICTS`. **B:** un hecho `about: WORLD` ("el valor pactado fue $4.800.000") con `SUPPORTS` de DOC-01 y `CONTRADICTS` de DOC-04 |
| `VG-02` | `EF-06` / `EF-07` (fecha de entrega) | Idénticas A y B |
| `VG-03` | `EF-08` / `EF-09` (el acta) | **A:** hecho sobre el acta + hecho sobre la declaración + link `CONTRADICTS`. **B:** un hecho `about: WORLD` sobre si hubo recibo a satisfacción, con links en ambos sentidos |

---

## 13. Contradicciones, irrelevantes y afirmaciones prohibidas

### 13.1 Contradicciones esperadas (`EC-xx`)

**Precisión obligatoria de vocabulario:** `Contradiction` es un **nombre RESERVADO, no una entidad de v0** (ADR-003). Por tanto **una contradicción no se mide como objeto**: se mide como **`EvidenceLink` de polaridad `CONTRADICTS` activo**, que es lo único que el modelo de dominio v0 materializa.

| ID | Qué enfrenta | Fuentes | Forma de detección exigida |
|---|---|---|---|
| `EC-01` | Valor total: **$4.800.000** vs **$4.300.000** | DOC-01 cl.3 ↔ DOC-04 p.1 | Al menos un `EvidenceLink` `CONTRADICTS` que enfrente una de las dos afirmaciones con el fragmento de la otra (forma A o B de `VG-01`) |
| `EC-02` | Fecha de entrega: **12 de mayo** vs **21 de mayo** | DOC-01 cl.5 ↔ DOC-04 p.1 | Ídem (`VG-02`) |
| `EC-03` | Qué firmó la clienta el 30 de mayo: acta de entrega vs hoja de asistencia | DOC-03 ↔ SEG-016 | Ídem (`VG-03`) |
| `EC-04` | Obra terminada y a satisfacción vs obra inconclusa | DOC-03 ↔ SEG-012/028/030 | `EvidenceLink` `CONTRADICTS` sobre `EF-10` |
| `EC-05` | **Documental contra documental, de la misma empresa:** "recibido a satisfacción" (30 may) vs "no ha sido puesto en funcionamiento" (20 jun) | DOC-03 ↔ **DOC-05** | Solo detectable en **MP-3**. Es el pago del ingrediente 10 |

### 13.2 Fusión narrativa esperada (`EM-xx`)

| ID | Segmentos | Resultado exigido |
|---|---|---|
| `EM-01` | SEG-012 y SEG-028 | **Un solo hecho** (`EF-11`), con **dos `EvidenceLink`** anclados a los dos rangos temporales. Producir dos hechos distintos es duplicación; anclar a un solo segmento cuando ambos lo sostienen es pérdida de soporte |

### 13.3 Contenido irrelevante — no debe convertirse en Fact (`IR-xx`)

| ID | Segmento | Contenido | Por qué NO es Fact del caso |
|---|---|---|---|
| `IR-01` | SEG-014 | "no dormí en dos meses", "yo lloraba de la rabia" | Estado anímico de la declarante. Puede ser relevante en otro contexto procesal, **no en este fixture**, cuyo objeto es el cumplimiento del contrato. No se ancla a ninguna proposición fáctica del conflicto |
| `IR-02` | SEG-014 | El examen de admisión de la hija | Circunstancia personal sin relación con el objeto |
| `IR-03` | SEG-006 | "era el cumpleaños de mi hermana" | **Irrelevante pero tentador:** es la *razón por la que recuerda* la fecha. Legítimo como **justificación textual dentro del `EvidenceLink`**; ilegítimo como Fact autónomo |
| `IR-04` | SEG-026 | "me pareció una persona grosera, un patán" | Juicio de valor sobre una persona. Convertirlo en Fact produce un hecho difamatorio sin contenido probatorio |
| `IR-05` | SEG-026 | La lluvia y la inundación de la cuadra | Contexto ambiental sin vínculo con el objeto |
| `IR-06` | SEG-001, SEG-002, SEG-031 | Consentimiento de grabación y cierre de la entrevista | **Metadiálogo del proceso**, no del caso. Es un hecho sobre la entrevista, no sobre el conflicto |

### 13.4 Afirmaciones prohibidas (`PA-xx`) — su aparición es fallo medido

| ID | Patrón prohibido | Por qué |
|---|---|---|
| `PA-01` | Cualquier **calificación jurídica**: "hubo incumplimiento contractual", "procede la resolución", "la empresa está en mora" | El slice no ejercita conocimiento jurídico sustantivo. `fact-builder` v0 extrae hechos, no califica |
| `PA-02` | Cualquier **cita normativa o jurisprudencial**, real o inventada | PF-004: ninguna autoridad jurídica se vuelve verificada por afirmación del modelo; y v0 no tiene `verify_legal_source` (kernel §6). Una cita inventada aquí es el riesgo n.º 1 del dominio manifestándose |
| `PA-03` | **Fusionar** `EE-PER-02` con `EE-PER-03`, o `EE-ORG-01` con `EE-ORG-02` | Trampas `ET-01` / `ET-02` |
| `PA-04` | Afirmar que la firma del acta **fue falsificada**, o que **fue de ella** | Es una conclusión, no un dato constatable en las fuentes. Lo constatable es la **discrepancia** entre el documento y la declaración |
| `PA-05` | **Nombrar** a la vecina (`EE-PER-04`) o atribuirle cualquier dato no dicho | Alucinación de entidad (`ET-05`) |
| `PA-06` | Afirmar que **el comprobante** acredita el pago el **9 de abril** | El comprobante dice 7. Es atribución de contenido inexistente a una fuente: el fallo más grave de `evidence_link_precision` |
| `PA-07` | Usar **DOC-05** como prueba de la visita del **2 de junio** | Trampa `DT-03`. Convierte un hecho sin corroboración en aparentemente documentado |
| `PA-08` | Presentar un hecho `about: WORLD` en conflicto **sin** la contradicción | Presenta una versión interesada como estado del expediente |

---

## 14. Coreografía de la corrida

### 14.1 Fases

| Fase | Qué ocurre | Material |
|---|---|---|
| **Fase 0 — preparación** | `create_case`; copia de `interview/` + `documents/` a `Inbox/`. `late-evidence/` y `expected/` **no se copian** | — |
| **Fase 1 — incorporación** | `ingest_evidence` × 5 (audio + DOC-01…DOC-04); derivaciones `PENDING → READY` | 5 Sources |
| **Fase 2 — análisis y commit** | `search_case` / `get_evidence_fragment`; `fact-builder` v0; `propose_facts`; revisión humana por política determinista; `commit_reviewed_facts` | — |
| **Fase 3 — evidencia tardía** | Cierre de sesión, nueva sesión, `open_case` + `changes_since`; copia de `late-evidence/` a `Inbox/`; `ingest_evidence` de DOC-05 | 1 Source |
| **Fase 4 — reanálisis** | `get_case_context(pending)` ⇒ `ANALYSIS_STALE`; segunda `propose_facts` **solo si la profesional lo pide** | — |

### 14.2 Efectos exigidos de la evidencia tardía (`LE-xx`)

| ID | Efecto exigido | Verificación |
|---|---|---|
| `LE-01` | `EvidenceIncorporated` + `ArtifactMarkedStale` **en la misma transacción**, `stale_reasons = [NEW_EVIDENCE]` | Case Event Log: dos eventos consecutivos, misma transacción |
| `LE-02` | `ANALYSIS_STALE {reasons:[NEW_EVIDENCE]}` visible en `get_case_context(pending)`, **adherida al artifact** en toda proyección | Proyección `pending` |
| `LE-03` | **Cero regeneraciones automáticas.** Ninguna `Proposal` nueva sin orden de la profesional | Ausencia de `FactsProposed` entre `ArtifactMarkedStale` y la orden |
| `LE-04` | Ninguna tool de la superficie permite **limpiar** la marca stale | Test de superficie (8 tools, kernel §6) |

### 14.3 La revisión humana debe ser determinista o el benchmark no es reproducible

**PROPUESTA DEL TECHNICAL DESIGN.** Si una persona revisa cada corrida con criterio propio, la revisión se vuelve una **segunda variable no controlada** junto al modelo, y el resultado deja de ser comparable entre corridas.

`expected/review-policy.md` fija una política determinista, ejecutada a través del `DevHumanAuthorizationProvider` (kernel §4):

1. **Aprobar** todo `ProposalItem` que la adjudicación case con un `EF` aplicable **y** cuyos `EvidenceLink` sean todos de tier `REQUIRED` o `ACCEPTABLE`.
2. **Rechazar** todo item que case con un `IR` o con un `PA`.
3. **Dejar `PENDING`** todo item no clasificable, y registrarlo para adjudicación manual.

Consecuencias buscadas: la corrida es reproducible; el `case.db` queda marcado `DEV_STUB` para siempre (§2.3); y las métricas de MP-1 (comportamiento del modelo) quedan limpiamente separadas de las de MP-2 (comportamiento del sistema completo).

### 14.4 Puntos de medición

| Punto | Cuándo | Qué mide | Denominador de recall |
|---|---|---|---|
| **MP-1** | Inmediatamente después de la primera `propose_facts`, **antes** de la revisión | **El modelo**: extracción, atribución, anclaje, ruido | `EF-01`…`EF-13` + `EF-15` (14) |
| **MP-2** | Después de `commit_reviewed_facts` | **El sistema completo** (modelo + política de revisión + gates del Core) | Los mismos 14 |
| **MP-3** | Después de la segunda `propose_facts` en fase 4 | **Comportamiento ante evidencia tardía**: `EF-14`, `EC-05`, `DT-03`, y que no se rompa lo ya correcto | 15 |

### 14.5 Libro de eventos esperado — y una ambigüedad del kernel que el fixture expone

Lectura aplicada (kernel §6 y §7): la superficie es de **8 tools**; `register_artifact` está **retirado** y el `FactAnalysis` se registra **dentro** de la transacción de `ProposeFacts`, que por tanto produce **dos** eventos y **dos** mutaciones (biyección mutación↔evento).

> **Divergencia documental detectada, registrada aquí sin resolverse.** El documento `docs/architecture/vertical-slice-v0.md` (nivel 2) todavía describe 9 tools con `register_artifact` como paso 12 explícito. El kernel técnico v0.4 §6 lo retira. Por precedencia (kernel §14), **este documento sigue al kernel** y señala la divergencia para corrección del slice.

| # | `event_seq` | Evento | `case_revision` **VIGENTE** (Modelo B · enmienda AC-02 aprobada) | `case_revision` (Modelo A — anterior, superado) |
|---|---|---|---|---|
| 1 | 1 | `CaseCreated` | 1 | 1 |
| 2 | 2 | `EvidenceIncorporated` (audio) | 2 | 2 |
| 3 | 3 | `DerivedRepresentationGenerated` (transcripción) | 3 | 3 |
| 4–11 | 4–11 | `EvidenceIncorporated` + `DerivedRepresentationGenerated` × 4 (DOC-01…DOC-04) | 4–11 | 4–11 |
| 12 | 12 | `FactsProposed` | 12 | 12 |
| 13 | 13 | `ArtifactRegistered` (`FactAnalysis`, misma transacción) | 13 | 13 |
| 14 | 14 | `ProposalReviewed(approved)` | **NULL** (no muta estado canónico; el contador sigue en 13) | **14** |
| 15 | 15 | `FactsCommitted` | **14** | 15 |
| 16 | 16 | `EvidenceIncorporated` (DOC-05) | 15 | 16 |
| 17 | 17 | `ArtifactMarkedStale` (misma transacción) | 16 | 17 |
| 18 | 18 | `DerivedRepresentationGenerated` (DOC-05) | 17 | 18 |

**RESUELTO — enmienda AC-02 aprobada.** El valor esperado es único: `expected_case_revision = 13`, coherente con `12-testing-strategy.md` §4.2. El fixture **no** registra valor alternativo. Registro histórico del análisis que lo expuso: El kernel §5.2 describe el flujo como *"la propuesta se genera contra la revisión N, se revisa contra N y se commitea exigiendo que el caso siga en N"*. Pero el kernel §7 registra que `ProposeFacts` **sí avanza** `case_revision`, y §6 añade `ArtifactRegistered` en la misma transacción. Ambas afirmaciones solo son compatibles si "N" designa la revisión vigente **después** de `FactsProposed` + `ArtifactRegistered` — es decir, `expected_case_revision = 13`, distinta de `base_case_revision = 11` de la `Proposal` (kernel §2.1). Bajo el Modelo A, en cambio, `expected_case_revision = 14`.

**El fixture ya no registra valores alternativos** (enmienda AC-02 aprobada): el resultado esperado es el del modelo vigente, y una corrida que produzca los valores del modelo superado es un **fallo**, no una variante. Texto histórico: «el fixture no elige; registra ambos valores como resultado esperado alternativo y la corrida revela cuál implementa el Core». **POR VERIFICAR con los dueños**; y **POR VERIFICAR** si `ArtifactRegistered` avanza `case_revision` por separado (la biyección mutación↔evento sugiere que sí; el kernel §7 lo agrupa bajo un único "sí" del use case).

---

## 15. Autoconsistencia del fixture (`FSC-xx`)

Comprobaciones que se ejecutan **sobre el fixture**, antes de cualquier corrida. Un fixture inconsistente produce métricas sin significado.

| ID | Comprobación |
|---|---|
| `FSC-01` | Todo rango `SEG` es monótono, no solapado y está contenido en `[0, duración declarada]` |
| `FSC-02` | El fin del último `SEG` (`00:13:47.900`) ≤ duración declarada del placeholder (`00:14:02.000`) |
| `FSC-03` | Todo `locator` de `expected_links` resuelve a un rango o a una posición existente en el Source declarado |
| `FSC-04` | Todo `EF` referencia al menos una fuente existente, salvo los marcados `DECLARANT_ONLY`, que referencian solo la entrevista **por diseño** |
| `FSC-05` | Todo `IR-xx` cita texto que aparece **literalmente** en alguna fuente del fixture |
| `FSC-06` | **Ningún archivo de `interview/`, `documents/` o `late-evidence/` referencia `expected/`**, ni por nombre ni por contenido |
| `FSC-07` | Los espacios de IDs (`EF` / `IR` / `PA` / `EC` / `EM` / `ET` / `DT` / `LE` / `EE` / `ES`) son disjuntos; ningún ID se reutiliza entre versiones del fixture |
| `FSC-08` | Los hashes del `content_manifest` coinciden con los archivos. Un cambio de bytes sin cambio de `fixture_version` **invalida** toda comparación con corridas anteriores |
| `FSC-09` | Ninguna fuente del fixture contiene una cita normativa o jurisprudencial (regla §2.1.5) |
| `FSC-10` | Ningún identificador del fixture tiene formato plausible de identificador oficial real (regla §2.2) |

---

## 16. Métricas conceptuales del eval

### 16.0 Regla previa: **sin objetivos numéricos**

**DECISIÓN APROBADA (encargo).** Ninguna métrica de esta sección lleva umbral, meta ni valor aceptable. **Primero se necesita baseline.** Un umbral fijado antes de la primera medición sería una cifra inventada, y este documento no inventa cifras.

Lo que sí se fija de antemano es la **definición**: numerador, denominador, punto de medición, fuente de datos, procedimiento de adjudicación y **qué NO captura** cada métrica. Una métrica sin esos seis elementos no es medible; es una impresión con nombre técnico.

### 16.1 Fuentes de datos del harness

| Fuente | Qué aporta | Nota |
|---|---|---|
| Payload de `FactsProposed` en el **Case Event Log** | Los `ProposalItem` efectivamente propuestos, con sus links | Canónico, hash-chained |
| **Tool Invocation Log** | Intentos **rechazados** por el Core (p. ej. hecho sin provenance), con hash de inputs y condiciones | **Imprescindible:** sin él, los gates del Core esconden los fallos del modelo |
| Case Event Log completo | Secuencia de eventos, `event_seq`, `case_revision`, principals, provenance | Verificación del libro de eventos (§14.5) |
| Proyecciones `facts` / `pending` | Estados derivados y condiciones activas | Para `LE-02`, `LE-03` |
| `expected/` | El truth set | **Nunca** pasa por el modelo |

### 16.2 Adjudicación: cómo se decide que un item "es" un `EF`

**El emparejamiento entre un `ProposalItem` y un `EF-xx` es un juicio, no un dato.** Es el punto más frágil de todo el eval y se declara como tal.

- **Baseline: adjudicación manual**, con criterio escrito (**equivalencia semántica de la proposición**, no coincidencia de cadena) y **bitácora** (`expected/adjudication-log.md`) que registra cada emparejamiento y cada duda.
- **Un matcher automático por similitud textual traslada su propio error a todas las métricas.** Solo se admite **después** del baseline manual y **solo** si se valida contra él, reportando su tasa de desacuerdo.
- **DECISIÓN PENDIENTE:** si se admite un juez LLM para adjudicar. Argumento en contra que debe vencerse explícitamente: introduciría un **segundo operador no determinista** dentro del instrumento que mide al primero.

### 16.3 `fact_recall`

- **Definición:** proporción de hechos esperados aplicables que la corrida efectivamente produjo.
- **Numerador:** `EF-xx` aplicables en el punto de medición para los que existe **al menos un** `ProposalItem` adjudicado como equivalente. Dentro de un `variant_group`, cualquiera de las formas aceptadas cuenta **una** vez.
- **Denominador:** `EF-xx` con el punto de medición en `applicable_at` (14 en MP-1/MP-2; 15 en MP-3).
- **Punto de medición:** MP-1 (modelo), MP-2 (sistema), MP-3 (post-evidencia tardía).
- **Datos:** payload de `FactsProposed` + adjudicación manual.
- **Reporte obligatorio:** desagregado por `classification` (`CONSISTENT` / `CONTRADICTED` / `PARTIALLY_SUPPORTED` / `DECLARANT_ONLY` / `LATE_EVIDENCE_ONLY`) y **excluyendo `EF-15`** del total principal, que se reporta aparte.
- **NO captura:** si el hecho está bien **anclado** (eso es §16.5), ni si está bien **calificado** epistémicamente (eso es §16.10), ni la calidad de la redacción.

### 16.4 `unsupported_fact_rate`

- **Definición:** proporción de hechos que la corrida intentó proponer **sin ningún anclaje probatorio y sin la marca explícita "solo alegado"**.
- **Numerador:** `ProposalItem` —**incluidos los rechazados por el Core**— con cero `EvidenceLink` de polaridad probatoria (`SUPPORTS` / `CONTRADICTS`) y sin marca "solo alegado".
- **Denominador:** total de items **intentados** (aceptados + rechazados).
- **Punto de medición:** MP-1, sobre **intentos**, no sobre aceptados.
- **Precisión crítica:** medir solo sobre aceptados **esconde el comportamiento del modelo detrás del gate del Core** (`propose_facts` rechaza sintácticamente esos items). Lo que se quiere medir es la propensión del modelo, no la eficacia del gate — que ya tiene su propio test funcional (F6 del slice).
- **Distinción obligatoria del fixture:** *soporte formal* (existe un `EvidenceLink` activo de polaridad probatoria ⇒ estado derivado `SUPPORTED`) **≠** *corroboración documental* (existe fuente distinta de la declaración de la propia parte). La entrevista **es** Evidence incorporada: `EF-13` y `EF-15` tienen soporte formal y **cero** corroboración. Esta métrica mide lo primero; la segunda se reporta como `declarant_only_share` (§16.11).
- **NO captura:** hechos con link que **no dice lo que se le atribuye** — eso es §16.5, y es un fallo distinto y peor.

### 16.5 `source_attribution_precision` y `evidence_link_precision`

Dos métricas separadas porque son dos fallos distintos.

**`source_attribution_precision` — ¿la fuente correcta?**

- **Numerador:** `EvidenceLink` cuyo `Source` / `Evidence` atribuido es el correcto según el truth set — **incluida la página en Sources compuestos** (DOC-04 p.1 correo ≠ p.2 factura).
- **Denominador:** `EvidenceLink` propuestos con fuente atribuida.
- **NO captura:** si el fragmento dentro de esa fuente es el correcto.

**`evidence_link_precision` — ¿el fragmento dice eso?** Se descompone en tres submedidas que se reportan por separado:

| Submedida | Numerador | Fallo que aísla |
|---|---|---|
| `link_resolvability` | Links cuyo `selector` **resuelve** contra el `source_version_hash` declarado | Ancla rota / inventada |
| `link_content_precision` | Links resolubles cuyo fragmento **contiene efectivamente** la proposición atribuida | **"Link fantasma":** cita real, contenido inexistente. `PA-06` es el arquetipo |
| `link_polarity_precision` | Links con contenido correcto cuya **polaridad** coincide con la esperada (`SUPPORTS` / `CONTRADICTS` / `CONTEXTUALIZES`) | Contradicción etiquetada como respaldo, o al revés |

- **Denominador común:** links propuestos (cada submedida se calcula sobre los que pasaron la anterior; se reportan también en cascada sobre el total).
- **Verificación de anclaje temporal:** para el audio, se comprueba además que el rango pertenece a la **línea de tiempo del original** y no a la del derivado (ADR-003 inv. 7; F5 del slice).
- **NO captura:** que el fragmento sea el **mejor** disponible. Un link correcto pero pobre puntúa igual que uno excelente.

### 16.6 `contradiction_recall`

- **Definición:** proporción de contradicciones esperadas que la corrida materializó.
- **Numerador:** `EC-xx` aplicables para los que existe al menos un `EvidenceLink` **`CONTRADICTS` activo** que enfrenta las fuentes previstas, en cualquiera de las `detection_forms` admitidas por su `variant_group`.
- **Denominador:** `EC-xx` aplicables (`EC-01`…`EC-04` en MP-1; **+ `EC-05`** en MP-3).
- **Precisión de vocabulario:** **se mide sobre polaridad de `EvidenceLink`, jamás sobre una entidad `Contradiction`** — que no existe en v0 (ADR-003, nombres reservados). Una métrica definida sobre una entidad inexistente sería inmedible.
- **Reporte obligatorio:** `EC-05` **por separado**, porque solo es alcanzable con evidencia tardía y mezclarla con las demás distorsiona la comparación entre MP-1 y MP-3.
- **NO captura:** contradicciones **inventadas** (fuentes que no se contradicen presentadas como opuestas). Eso se reporta como `spurious_contradiction_count`, sin denominador fijo.

### 16.7 `irrelevant_fact_rate`

- **Definición:** proporción del contenido irrelevante catalogado que fue convertido en hecho candidato.
- **Numerador:** `IR-xx` para los que existe un `ProposalItem` adjudicado como su materialización.
- **Denominador:** `IR-xx` del fixture (**6**).
- **Complemento obligatorio — `extraneous_fact_rate`:** items propuestos que **no** casan con ningún `EF` ni con ningún `IR`. Se reporta como **conteo absoluto y como fracción de items propuestos**, no como tasa sobre un catálogo, porque **el ruido posible no tiene denominador cerrado**: pretender lo contrario sería fingir precisión.
- **Caso `IR-03` (el cumpleaños):** cuenta como fallo **solo si aparece como Fact autónomo**. Si aparece como **justificación textual dentro de un `EvidenceLink`**, es uso correcto y **no** penaliza. La adjudicación debe distinguirlo explícitamente.
- **NO captura:** omisiones de contenido relevante (eso es recall).

### 16.8 `prohibited_assertion_rate`

- **Numerador:** `PA-xx` que aparecen en la corrida (en items propuestos, en justificaciones de links o en el `FactAnalysis` registrado).
- **Denominador:** `PA-xx` del catálogo (**8**).
- **Reporte:** desagregado por ID, no agregado. `PA-02` (cita jurídica inventada) y `PA-06` (contenido atribuido a un documento que no lo dice) son cualitativamente más graves que `PA-01`, y promediarlos ocultaría eso.

### 16.9 `hallucinated_entity_rate` y `entity_resolution_accuracy`

**`hallucinated_entity_rate` — entidades que no existen**

- **Numerador:** entidades nombradas en la corrida que **no** figuran en `expected_entities` **y** no aparecen literalmente en ninguna fuente incorporada.
- **Denominador:** entidades nombradas distintas en la corrida.
- **Casos arquetípicos del fixture:** nombrar a la vecina (`ET-05`); inventar un número de contrato; inventar un cargo.

**`entity_resolution_accuracy` — entidades que existen, mal resueltas**

- **Numerador:** trampas `ET-xx` resueltas correctamente.
- **Denominador:** `ET-01`…`ET-05` (**5**).
- **Dos modos de fallo, reportados por separado:** **colapso** (Nariño+Mariño tratados como uno; Hidroservicios Delmonte + Delmonte Hidráulica tratadas como una) y **escisión** ("M E QUIROGA B" tratada como persona distinta de Marta Elena Quiroga Bastidas).
- **Advertencia de validez:** con transcripción canónica perfecta (L0), esta métrica mide el **caso fácil**. Su valor **no es transferible** a una corrida con ASR real (§6.4). Debe reportarse siempre junto al nivel de audio (`L0` / `L1` / `L2` / `L3`).

### 16.10 `temporal_precision`

- **Numerador:** trampas `DT-xx` resueltas correctamente: la fecha se atribuye a la fuente que efectivamente la contiene, y las fechas cercanas **no** se fusionan.
- **Denominador:** `DT-01`, `DT-02`, `DT-03` (**3**).
- **`DT-03` se reporta aparte** por ser el más caro: fusionar 2 y 20 de junio no produce solo un error de fecha, produce un **hecho falsamente documentado**.

### 16.11 Métricas de comportamiento del sistema (binarias por corrida, no tasas)

| Métrica | Definición | Punto |
|---|---|---|
| `narrative_dedup_correct` | `EM-01`: SEG-012 y SEG-028 producen **un** hecho con **dos** links | MP-1 |
| `staleness_surfaced` | `LE-01` + `LE-02` verificados en el Case Event Log y en la proyección | MP-3 |
| `no_auto_regeneration` | `LE-03`: ningún `FactsProposed` sin orden de la profesional | MP-3 |
| `event_ledger_match` | El libro de eventos observado coincide con §14.5 bajo uno de los dos modelos, y **se registra cuál** | MP-3 |
| `declarant_only_share` | Fracción de hechos propuestos con `corroboration = NONE_BEYOND_DECLARANT` **presentados como tales** | MP-1 |
| `about_classification_accuracy` | Fracción de hechos cuyo `about` (`WORLD` / `DOCUMENT`) coincide con el esperado — mide §11.5, `PA-08` | MP-1 |

### 16.12 Cómo se reporta un baseline

**PROPUESTA DEL TECHNICAL DESIGN.**

1. **Una corrida es una anécdota.** El operador es no determinista; un valor único no es un baseline. El baseline se reporta como **distribución sobre N corridas** con la mediana y el rango observado, **nunca** como número único.
2. **No se fija N aquí.** El N necesario depende de la varianza observada, que es precisamente lo que la primera tanda mide. Fijar N antes sería inventarlo. **Procedimiento:** correr una tanda exploratoria, observar la dispersión, y **entonces** decidir N y justificarlo.
3. **Toda cifra se reporta con su contexto completo:** `fixture_version`, hashes del `content_manifest`, nivel de audio (`L0`…`L3`), `model_id`, `methodology_version` del skill, y el modelo de revisión (A o B) observado. Una métrica sin ese contexto **no es comparable** con ninguna otra.
4. **`observed in current environment`, jamás `documented platform guarantee`.** Ningún resultado de este benchmark describe una capacidad de Claude, de Cowork, de MCP ni de ningún proveedor. Describe **lo que ocurrió en una corrida sobre un fixture**.

---

## 17. Amenazas a la validez de la medición

| # | Amenaza | Efecto | Mitigación |
|---|---|---|---|
| 1 | **Sobreajuste al fixture** | Un fixture único e inmutable acaba siendo optimizado —consciente o no— y deja de medir generalización | El fixture es **instrumento de baseline**, no criterio de aceptación de producto. Cuando se use para iterar, se necesita un segundo fixture *held-out*, no derivado de este. **DECISIÓN PENDIENTE** |
| 2 | **Efecto de demanda** | Marcadores de "esto es una prueba" alteran el comportamiento del modelo | Watermark fuera de los bytes (§2.4) |
| 3 | **Error del adjudicador** | El emparejamiento item↔`EF` es juicio humano; dos personas pueden discrepar | Criterio escrito + bitácora + medición de acuerdo entre adjudicadores antes de confiar en la métrica |
| 4 | **Transcripción perfecta** | Sub-estresa resolución de entidades y anclaje temporal | Declarado en §6.4; ruta L1→L3 en §6.5; reporte obligatorio del nivel de audio |
| 5 | **Fixture en un solo idioma y registro** | Nada dice sobre otros registros de habla ni sobre documentos escaneados de calidad variable | Declarado como límite; OCR no se ejercita |
| 6 | **Colapso de causas** | Un fallo puede venir del skill, del modelo, del prompt del host o del Core, y la métrica no los separa | Registro obligatorio de `methodology_version`, `model_id` y host; separación MP-1 / MP-2 |
| 7 | **Deriva silenciosa del fixture** | Editar un documento sin subir `fixture_version` rompe la comparabilidad sin avisar | `FSC-08` (hashes en el manifiesto) |
| 8 | **Filtración del truth set** | Si `expected/` llega al contexto, la corrida no mide nada y **puede parecer excelente** | `FSC-06` + regla de fase 0 + revisión del contexto efectivo antes de aceptar una corrida |

---

## 18. `NOT_TESTED` e `INCONCLUSIVE` declarados

| Ítem | Estado | Por qué |
|---|---|---|
| Derivación **material** audio → transcripción | **NOT_TESTED** en L0 | El placeholder no contiene el habla; la `DerivedRepresentation` no procede de los bytes de su `Source` (§6.3). La referencia estructural sí se verifica; la reproducibilidad desde el original, no |
| Perfil de error de un ASR real (WER, confusión de nombres) | **NOT_TESTED** | Requiere L2/L3 |
| `UNCERTAIN_FRAGMENT` a partir de confianza real | **NOT_TESTED** | El fixture no tiene scores reales; inyectarlos es simulación declarada, no observación |
| Re-anclaje de fragmentos tras regenerar una `DerivedRepresentation` | **NOT_TESTED** | La derivación de fixture es determinista: el hash nunca cambia |
| `DerivedRepresentationFailed` / `INTEGRATION_ERROR` desde fallo real | **NOT_TESTED** | Solo por inyección artificial. Coherente con kernel §10: en v0 `INTEGRATION_ERROR` queda declarada sin disparador ejercitado |
| Diarización / atribución de hablante | **NOT_TESTED** | Fuera del alcance de v0 (vertical slice); en el fixture las etiquetas son dato, no inferencia |
| OCR sobre escaneos de calidad variable | **NOT_TESTED** | Los documentos del fixture son texto limpio |
| `DETERMINED` y `WITHDRAWN` | **NOT_TESTED** | Sin productor en v0 (ADR-003; addendum v0.3 B.5). El fixture no los alcanza |
| `Statement` | **NOT_TESTED** | No se materializa en v0 (addendum v0.3 B.7). El anclaje del fixture ocurre en `EvidenceLink` |
| Valor de `expected_case_revision` (13 vs 14) | **INCONCLUSIVE** | Ambigüedad entre kernel §5.2 y §7 (§14.5). El fixture la expone; no la resuelve. **POR VERIFICAR con los dueños** |
| ¿`ArtifactRegistered` avanza `case_revision` por separado? | **INCONCLUSIVE** | La biyección mutación↔evento sugiere que sí; el kernel §7 agrupa el use case bajo un único "sí". **POR VERIFICAR** |
| Umbrales de aceptación de cualquier métrica | **INCONCLUSIVE por diseño** | No hay baseline. Fijar un umbral ahora sería inventarlo (§16.0) |
| N de corridas del baseline | **INCONCLUSIVE por diseño** | Depende de la varianza observada, que es lo que la primera tanda mide (§16.12) |
| Generalización fuera del fixture | **NOT_TESTED** | Un solo fixture, un solo dominio de conflicto, un solo registro de habla (§17.1, §17.5) |
| Confidencialidad y términos de proveedor de transcripción | **NOT_TESTED** | Nada sale de la máquina en L0 |

---

## 19. Decisiones que requieren aprobación

| # | Qué | Etiqueta |
|---|---|---|
| 1 | Campo `derivation_source: REAL \| FIXTURE` en `DerivedRepresentation`, con FAIL-TO-START en configuración de producción, por analogía con kernel §4.2 | **PROPUESTA DEL TECHNICAL DESIGN** |
| 2 | Extensión de la regla de dependencias: **`src/` nunca importa de `fixtures/`**; el harness de eval no es código de producto | **PROPUESTA DEL TECHNICAL DESIGN** |
| 3 | Watermark **fuera de los bytes** del Source, con riesgo residual aceptado (§2.4) | **PROPUESTA DEL TECHNICAL DESIGN** |
| 4 | Revisión humana del benchmark ejecutada por política determinista vía `DevHumanAuthorizationProvider`, marcando el `case.db` como `DEV_STUB` para siempre | **PROPUESTA DEL TECHNICAL DESIGN** |
| 5 | Distinción `about: WORLD \| DOCUMENT` y grupos de variante en el truth set | **PROPUESTA DEL TECHNICAL DESIGN** |
| 6 | Medir `unsupported_fact_rate` sobre **intentos** (incluidos los rechazados por el Core), no sobre aceptados | **PROPUESTA DEL TECHNICAL DESIGN** |
| 7 | Valor de `expected_case_revision` y avance de `case_revision` en `ArtifactRegistered` | **DECISIÓN PENDIENTE (dueños)** |
| 8 | Corrección del vertical slice: 9 tools → 8, `register_artifact` retirado (kernel §6) | **DIVERGENCIA DOCUMENTAL A CORREGIR** |
| 9 | Segundo fixture *held-out* para evitar sobreajuste | **DECISIÓN PENDIENTE** |
| 10 | Admisión (o no) de un juez LLM en la adjudicación | **DECISIÓN PENDIENTE** |
| 11 | Nivel de placeholder de audio a construir primero (L0 inerte vs L1 sintetizado) | **DECISIÓN PENDIENTE** — L1 depende de verificación de disponibilidad y representatividad |

---

**NON-PRODUCTION FIXTURE.** Todo el contenido narrativo, las entidades, las fechas, los montos y los documentos descritos en este documento son **íntegramente ficticios** y existen solo para medir el comportamiento del sistema. Ninguna afirmación de este documento es una afirmación de derecho.
