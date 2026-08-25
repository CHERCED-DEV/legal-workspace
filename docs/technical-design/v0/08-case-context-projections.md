# 08 — Memoria, proyecciones y delta de sesión (`get_case_context`)

**Estado:** Technical Design V0 (nivel 2 de precedencia, kernel §14). Materializa el **kernel técnico v0.4 §9** y hace operativo **ADR-004** (Canonical Case State + Derived Projections), en particular su bloque (a) y sus invariantes 1, 2 y 3. Consume sin redefinir: **ADR-001** (el modelo es cliente externo no confiable; sobre uniforme), **ADR-002** (private state vs user workspace), **ADR-003** (estados derivados del `Fact`, jamás persistidos), **ADR-006** (nada no incorporado aparece como contenido del Case).

**Qué NO se decide aquí:** la superficie MCP (`05-mcp-contract.md`), la frontera transaccional de las lecturas (`03-application-use-cases.md` §0.4 y §6), el esquema de tablas (`04-persistence-model.md`), el ciclo de autorización (`06-human-authorization.md`), el catálogo de condiciones (kernel §10) ni el modelo de eventos (kernel §8). Este documento define **qué contiene cada proyección, qué la alimenta, qué política decide el recorte y cómo se demuestra que un recorte nunca pasa por expediente completo**.

**Nota de vocabulario obligatoria (kernel §1).** `Principal` (`principal_id`, `principal_type ∈ HUMAN | AI | SYSTEM`, `principal_role`) responde **quién ejecutó**. `provenance_kind` (`EXTERNAL_SOURCE | AI_DERIVATION | AI_INFERENCE | HUMAN_DECISION | SYSTEM`) responde **cuál es la naturaleza epistémica del origen**. Las proyecciones exponen ambos por separado y nunca los mezclan; la forma `actor_type = HUMAN_DECISION` del texto histórico es la errata que el kernel §1.5 normaliza y no se reproduce aquí.

**Alcance de `Statement`:** no se materializa en V0 (kernel §15). Ninguna proyección lo expone ni deja hueco visible para él.

---

## 0. Convenciones de lectura

- Las interfaces TypeScript son **conceptuales**: fijan forma y nombres, no implementación. El SQL es **pseudocódigo conceptual** sobre el DDL de `04-persistence-model.md` §3; no es ejecutable y no fija plan de consulta ni índices (esos viven en `04` §5).
- Los tipos transversales (`Uuid`, `Sha256`, `CaseRevision`, `EventSeq`, `Iso8601`, `Principal`, `TypedCondition`) son los de `03-application-use-cases.md` §0.1 y no se redefinen.
- Etiquetas: `HECHO VERIFICADO` (con fuente) · `DECISIÓN APROBADA` · `PROPUESTA DEL TECHNICAL DESIGN` (requiere aprobación) · `HIPÓTESIS` · `SUPUESTO` · `POR VERIFICAR` · `RIESGO` · `DECISIÓN PENDIENTE` · `POST-V0`.
- Los identificadores de invariante de este documento son `INV-P-nn` (P de *projection*). Su trazabilidad a pruebas está en §11.

---

## 1. Qué es una proyección, y qué no

### 1.1 Definición operativa

> Una **proyección** es una **función determinista y total del Canonical Case State a la revisión vigente**, servida bajo demanda, sin caché, y **sin ninguna capacidad de escritura asociada**.

De ahí se siguen tres propiedades que este documento debe hacer verificables, no solo declarar:

| Propiedad | Enunciado exacto | Dónde se verifica |
|---|---|---|
| **Determinista** | Mismo estado canónico + misma revisión + misma versión de política ⇒ salida **idéntica byte a byte** | Golden test, §8 |
| **Regenerable** | Ninguna proyección es insumo de otra proyección ni de ningún use case; borrarla no pierde información | §7.3, §11 |
| **No autoritativa** | Ninguna proyección es fuente de verdad; el Core nunca la lee de vuelta | §7.4, INV-P-2 |

**Corolario que conviene decir en voz alta:** *"la memoria de Claude"* no existe como objeto de este sistema. Lo que existe es un estado canónico y una vista tipada de ese estado. La palabra "memoria" en el nombre de este documento designa **la función**, no un almacén: la continuidad entre sesiones la produce el Core consultando su propio estado, no el modelo recordando.

### 1.2 Invariante estructural: ninguna proyección es objetivo de escritura del modelo

**`INV-P-1` (ADR-004 inv. 1, literal).** Ninguna proyección —`overview`, `facts`, `evidence`, `pending`, `changes_since`, ni la orientation projection `memory.md` de §7— es objetivo de escritura del modelo.

Se sostiene sobre **tres capas independientes**, y conviene saber cuál de las tres es la que realmente aguanta:

1. **Ausencia de capacidad.** La superficie de 8 tools (kernel §6) no contiene ninguna operación de escritura de proyección, ni parámetro que altere su contenido más allá de `scope`/`params`. Verificable por el test de superficie (F16). *Esta capa protege contra el camino normal.*
2. **Posición.** El estado canónico vive en el LEGAL OS PRIVATE STATE (ADR-002); una proyección materializada hacia el workspace no es canónica por serlo. *Esta capa protege contra la confusión de zonas, no contra la escritura.*
3. **Ausencia de lectura.** **Ningún use case, ninguna consulta y ningún puerto del Core acepta como entrada el contenido de una proyección.** No existe un `read_projection`, ni una re-ingestión de `memory.md`, ni una reconciliación que compare la proyección con el estado. *Esta es la capa que aguanta.*

**Por qué la tercera es la decisiva — `HECHO VERIFICADO` (fuente: `ESTADO-Y-HALLAZGOS-CRITICOS.md` §1.1, hallazgos 1 y 2, sobre documentación oficial de Cowork):** en el anfitrión candidato **no existe `deny` por ruta**, adjuntar una carpeta concede su árbol completo con lectura y escritura, y la configuración de Claude Code no gobierna Cowork. Por tanto **no puede prometerse que un archivo materializado en el workspace sea inescribible por el agente**. La garantía honesta no es *"el modelo no puede escribir la proyección"*, sino:

> **El modelo puede escribir un archivo de proyección materializado; lo que no puede es que ese archivo signifique algo, porque nada lo lee.**

Esta formulación es la que se somete a prueba (§9.3, assert 5) y la que se comunica. La formulación fuerte —"inescribible"— sería una capacidad de plataforma que no está verificada, y afirmarla sería exactamente el tipo de promesa que este proyecto prohíbe.

### 1.3 Lo que una proyección nunca contiene

| Nunca contiene | Regla de origen |
|---|---|
| Diálogo crudo ni razonamiento intermedio del modelo | ADR-004 inv. 3; no existe tabla que los admita (`04` §3) |
| Material **no incorporado** (rutas, URLs, texto pegado, contenido de `Inbox/` sin `ingest_evidence`) | ADR-006 inv. 1; recíproco declarado en ADR-004 §Relaciones |
| Estados derivados del `Fact` **almacenados** | ADR-003 inv. 6: se computan en la proyección, no se leen de una columna |
| `content_hash` de ningún tipo | kernel §11: un hash nunca es identificador de entidad ni se muestra a la usuaria (§2.3.3) |
| Prosa generada por un modelo | §3.4: todo `content` es dato estructurado o plantilla fija del producto |
| Secretos de autorización | kernel §3.3: cero tokens en el contexto del modelo |
| Entidades de otro Case | ADR-003 inv. 10 / INV-D-07: el aislamiento es por base de datos (`04` §1.1) |

---

## 2. El sobre de respuesta

### 2.1 Contrato literal (kernel §9, sin desviación)

```ts
// CONCEPTUAL. Idéntico al de 03 §6.3 y 05 §6.2; aquí se especifican sus reglas.

type Scope = 'overview' | 'facts' | 'evidence' | 'pending' | 'changes_since';
// 'procedural' RESERVADO: documentado, NO implementado, NO miembro del enum (§5.6)

interface CaseContextResponse {
  case_id:       Uuid;
  case_revision: CaseRevision;   // revisión vigente al generar
  event_seq:     EventSeq;       // ancla del delta (kernel §9, enmienda AC-02 aprobada)
  scope:         Scope;
  params:        Record<string, unknown>;   // eco normalizado de lo recibido (§2.2.4)
  content:       unknown;                   // dependiente del scope (§5)
  completeness:  'COMPLETE' | 'PARTIAL';
  omissions:     Omission[];                // NO vacío si completeness = 'PARTIAL'
  conditions:    TypedCondition[];          // catálogo cerrado, kernel §10
}
```

`TRUNCATED` **no existe** (kernel §9): el corpus previo lo absorbe en `PARTIAL` con `reason = 'budget'`, porque para la usuaria y para el modelo la distinción operativa es idéntica —falta algo y está declarado— y dos valores para el mismo hecho son dos oportunidades de divergir.

### 2.2 Reglas por campo

**2.2.1 `case_revision` y `event_seq` describen exactamente el contenido servido.** Ambos se leen del **mismo snapshot de lectura único** que produjo el `content` (`03` §0.4 regla 6). Un sobre que declare una revisión distinta de la que generó el contenido es un **defecto de veracidad**, no una carrera aceptable. Consecuencia práctica: el `event_seq` devuelto por cualquier scope es un cursor legítimo para el `changes_since` de la sesión siguiente (§6.2).

**Los dos relojes divergen, y por eso el ancla del delta es `event_seq` — `DECISIÓN APROBADA` (enmienda AC-02, kernel §5.2 y §8.1).** `event_seq` avanza en **todo** evento del Case Event Log; `case_revision` avanza **solo** en los eventos que mutan el estado epistémico canónico y es **NULL** en los que no lo mutan (caso de `ProposalReviewed`). De ahí se siguen dos reglas del sobre: (a) `case_revision ≤ event_seq` siempre, y la diferencia es exactamente el número de eventos no canónicos ocurridos en el Case; (b) el único de los dos que identifica **un punto del log sin ambigüedad** es `event_seq`, por lo que es el que cursa el delta (§6.1) y el que portan los `orientation_cursors` (§5.1). `case_revision` sigue en el sobre porque es lo que fecha el **contenido** servido —una proyección es función del estado canónico a la revisión vigente (§1.1)—, no porque sirva de cursor.

**2.2.2 `case_revision` no avanza.** Leer no es mutar (`03` §6.8). Cero eventos, cero entradas en `fact_status_history`, cero escrituras en `case.db`. Lo único que se escribe es una fila del Tool Invocation Log, que es operacional y podable (kernel §8.2) y **jamás fuente para reconstruir estado canónico** (ADR-004 inv. 8).

**2.2.3 `completeness` es obligatorio y sin valor por defecto.** No existe "ausente significa completo". Un serializador que lo omita **falla el contract test** (F15, criterio estructural 2). Es la diferencia entre un contrato y una costumbre.

**2.2.4 `params` es eco normalizado, no eco literal.** Se devuelve la forma **resuelta** de los parámetros: si el invocador pasó `since_revision`, el eco incluye además el `since_event_seq` al que el Core lo resolvió (§6.1). Razón: el invocador debe poder encadenar la llamada siguiente sin repetir la resolución ni recordarla. Nunca se ecoan parámetros desconocidos: un parámetro no declarado es `VALIDATION_FAILED` en el adapter (`05` §4.2), no un campo silenciosamente ignorado.

**2.2.5 `conditions[]` viaja también en el éxito.** Una proyección puede ser `COMPLETE` y aun así llevar `ANALYSIS_STALE` adherida a un artifact (`03` §12.11), `HUMAN_REVIEW_REQUIRED` por items pendientes visibles en `pending`, `INTEGRATION_ERROR` por una derivación `FAILED` o `UNCERTAIN_FRAGMENT`. Que el expediente esté completo en un scope no significa que no haya nada que decirle a la profesional.

**2.2.6 `completeness = PARTIAL` no emite condición del catálogo.** `PROPUESTA DEL TECHNICAL DESIGN.` La parcialidad viaja en el sobre, no en `conditions[]`. Razones: (a) el catálogo del kernel §10 es **lista cerrada** y añadirle un código es cambio de contrato; (b) duplicar el mismo hecho en dos campos crea exactamente la clase de divergencia que el kernel evita al derivar `INVALIDATED` en vez de almacenarlo (kernel §2.2). Consecuencia sobre el pipeline de presentación (kernel §10): éste gana un **segundo punto de entrada**,

```text
completeness = PARTIAL  →  presentation category LIMITED_CERTAINTY  →  plantilla por locale
```

en paralelo al ya existente `internal condition → presentation category → human message`. **Alternativa considerada y rechazada:** añadir `CONTEXT_PARTIAL` al catálogo — rechazada por (a) y (b).

### 2.3 `omissions[]`

**2.3.1 `section` es vocabulario cerrado, no texto libre.** `PROPUESTA DEL TECHNICAL DESIGN.` Si `section` fuera prosa, la omisión sería legible por una persona y opaca para todo lo demás: no habría contract test posible, ni agregación, ni forma de comprobar que **lo omitido pertenece al scope pedido**. El vocabulario por scope está en §5 y es cerrado como la lista de eventos: ampliarlo es cambio de contrato.

**2.3.2 `reason` es el enum de `05` §6.2**, sin ampliación:

| `reason` | Significado exacto | Ejemplo |
|---|---|---|
| `budget` | La sección existe y tiene contenido, pero no cabe en el presupuesto del scope (§4) | 400 hechos, caben 120 |
| `not_implemented` | La sección está declarada en el contrato y no se implementa en V0 | `procedural` (§5.6) |
| `unavailable` | La sección depende de un estado que hoy no puede computarse | derivación `FAILED`: no hay texto que listar |

**2.3.3 Extensión aditiva propuesta.** `PROPUESTA DEL TECHNICAL DESIGN — requiere aprobación.`

```ts
interface Omission {
  section: string;                 // vocabulario cerrado, §5
  reason: 'budget' | 'not_implemented' | 'unavailable';
  // — extensión aditiva propuesta —
  omitted_count?: number;          // cuántos elementos quedaron fuera
  total_count?: number;            // cuántos hay en total en la sección
  next_cursor?: string;            // opaco; permite pedir la continuación por otra vía
}
```

**Argumento a favor:** `{section:'facts.list', reason:'budget'}` informa de que falta algo, pero no de **cuánto**. La diferencia entre *faltan 2 hechos* y *faltan 400* es la diferencia entre un contexto utilizable y uno engañoso, y es exactamente la magnitud que el invariante de §10 debe proteger. **Argumento en contra, y por qué no gana:** `total_count` puede ser caro en un caso grande; pero todas las secciones de lista de §5 se cuentan con un `COUNT(*)` sobre el mismo snapshot que ya está abierto, y el coste es despreciable frente a la serialización del contenido que sí cabe.

**Divergencia declarada:** `05-mcp-contract.md` §6.2 y `03-application-use-cases.md` §6.3 declaran `omissions` con exactamente `{section, reason}`. La extensión es **aditiva** y no invalida ninguna respuesta conforme; si no se aprueba, este documento se corrige y el invariante de §10 queda sostenido solo por los contadores de sección de §3.2 R-2, que entonces pasan a ser **obligatorios sin excepción**.

**2.3.4 Invariante duro.** **`INV-P-3`:** `completeness = 'PARTIAL' ⇔ omissions.length > 0`. Bicondicional, no implicación: `COMPLETE` con `omissions` no vacío es tan defectuoso como `PARTIAL` con `omissions` vacío. El kernel §9 enuncia la implicación; la forma bicondicional es la que hace el contract test decidible en ambos sentidos.

### 2.4 Lo que el sobre deliberadamente no tiene

| Campo ausente | Por qué |
|---|---|
| `generated_from_revision` | Toda proyección se genera **siempre** desde la revisión vigente, sin caché: sería idéntico a `case_revision` (ADR-004 (a)). Vuelve al contrato el día que se cacheen proyecciones |
| `generated_at` | **`PROPUESTA DEL TECHNICAL DESIGN`.** Un reloj de pared en la salida haría que dos generaciones del mismo estado difirieran, **destruyendo el golden test** (§8.2) por un dato que no describe el expediente. Los instantes que sí importan (`incorporated_at`, `reviewed_at`) viven en el contenido y proceden del estado, no del reloj de la llamada |
| `limit` / `budget` en la entrada | El presupuesto es política del producto y **no es decisión del modelo en runtime** (§4.1). Sin este campo, el modelo no puede reintentar hasta que la respuesta "parezca completa" |
| `format` | En V0 hay una sola forma de salida (dato estructurado). La representación markdown de §7 es un **renderizado del producto**, no una variante del contrato |

### 2.5 Coherencia con `search_case`

`search_case` declara su recorte con `exhaustive: boolean` (`05` §6.3) y `get_case_context` con `completeness` + `omissions[]`. **Divergencia menor señalada, no resuelta aquí:** son dos nombres para la misma obligación —declarar lo que falta—. Este documento **no** cambia el contrato de `search_case`; deja registrado que la regla de §10 (un resultado parcial nunca puede parecer exhaustivo) aplica a ambas superficies y que la unificación de nombres, si se hace, es trabajo de reconciliación de `05`.

---

## 3. Política editorial: quién decide qué entra

### 3.1 El problema que resuelve

ADR-004 rechazó el `memory.md` monolítico con un argumento que aquí hay que honrar: *"carece de política editorial — quien decidiera qué entra sería el modelo, reintroduciendo el problema que se quería evitar"*. Si el recorte se resuelve pidiéndole al modelo que "resuma lo importante", el sistema entero descansa sobre el juicio del componente que se declaró no confiable (ADR-001).

Por tanto: **la política editorial es un algoritmo declarado, determinista y versionado, propiedad del producto.** No es un prompt, no es una heurística del modelo, y no cambia entre dos llamadas con el mismo estado.

### 3.2 Las seis reglas

**R-1 — Unidad de omisión: el elemento completo.**
Nunca se trunca un elemento por la mitad. Se omiten hechos enteros, evidencias enteras, entradas de delta enteras o secciones enteras. **Razón:** medio hecho se lee como un hecho completo; un `statement_text` cortado en "el contratista entregó la obra el" es una afirmación distinta de la real. La única excepción son los campos de texto largo con **política de recorte declarada por campo** (§3.3), y en ese caso el campo lleva su propia marca.

**R-2 — Todo contenedor de lista declara su cardinalidad real.**
Cada sección de lista emite `{ total, included }` **siempre**, quepa o no quepa todo. Los contadores no están sujetos al presupuesto: cuestan bytes constantes y son lo que impide que una respuesta recortada se lea como el expediente entero (§10.2, mecanismo 3).

**R-3 — El recorte nunca es sesgo optimista.**
Cuando hay que recortar, **se recorta primero lo tranquilizador y nunca lo problemático**. Un hecho contradicho por la evidencia, una derivación fallida, una propuesta esperando decisión humana o un análisis obsoleto **preceden** en el orden de llenado a un hecho sostenido y a una evidencia ya utilizada. Es la regla más consecuente de este documento: sin ella, el presupuesto se convierte en un filtro que hace que todo caso grande parezca en orden.

**R-4 — Orden total y determinista.**
El orden de llenado de cada sección es un **orden total** computado desde el estado canónico, con desempate final por identificador opaco ascendente. Prohibido ordenar por texto sujeto a *collation* de locale, por valores en coma flotante sin regla de precisión, o por cualquier cosa que dependa del plan de consulta.

**R-5 — Selección por prefijo (omisión monótona).**
La selección es el **prefijo** del orden de R-4 que cabe en el presupuesto. Consecuencia comprobable: **aumentar el presupuesto nunca elimina un elemento que estaba presente con un presupuesto menor**. Es una propiedad testeable (§8.3) que impide que la política se implemente como una heurística de "relevancia" no reproducible.

**R-6 — Secciones obligatorias.**
Cada scope declara secciones `mandatory` que se sirven siempre, aunque la respuesta acabe `PARTIAL`, y secciones `discretionary` que son las primeras en caer. Ninguna sección que contenga **decisiones humanas pendientes** (familia `AUTHORITY` del kernel §10) puede ser `discretionary`.

### 3.3 La primitiva `emit-or-omit`

`PROPUESTA DEL TECHNICAL DESIGN.` El invariante `INV-P-3` no se sostiene con disciplina de programación: se sostiene con que **no exista un camino de código que descarte un elemento sin registrar la omisión**.

```ts
// CONCEPTUAL. Único punto por el que un elemento puede quedar fuera.
interface ProjectionBuilder {
  // Emite si cabe; si no cabe, incrementa el contador de omisión de la sección.
  // NO existe un método `drop`, `skip` ni `truncate` accesible al constructor de scopes.
  emitOrOmit(section: SectionId, element: unknown): 'EMITTED' | 'OMITTED';

  // Cierra la sección: escribe {total, included} (R-2) y, si included < total,
  // añade la Omission correspondiente. Llamada obligatoria por sección declarada.
  closeSection(section: SectionId, total: number): void;

  // Deriva completeness de las omisiones acumuladas. No es asignable desde fuera.
  seal(): CaseContextResponse;
}
```

El recorte de un **campo** de texto largo (por ejemplo un `rationale` extenso) es el único caso de truncamiento intra-elemento, va declarado en la política por campo, y produce su propia omisión con `section = '<scope>.<campo>'`. No hay tercera vía.

### 3.4 Lo que la política editorial explícitamente **no** hace

- **No resume.** `content` es dato estructurado o renderizado de plantilla fija del producto. Ninguna proyección invoca un modelo para condensar. Si el presupuesto no alcanza, se **omite y se declara**; no se comprime con pérdida semántica silenciosa.
- **No interpreta.** No hay campo "relevancia", "importancia" ni "prioridad jurídica" calculado por heurística: el orden de R-3/R-4 es una función explícita de estados epistémicos, no una puntuación.
- **No elige el scope por el modelo.** El scope lo pide el invocador; el Core no degrada silenciosamente un scope a otro (por ejemplo `procedural` ⇒ `VALIDATION_FAILED`, nunca `overview`).
- **No adivina el cursor.** `changes_since` sin cursor es rechazo, no un valor por defecto (§6.2).

---

## 4. El presupuesto de tamaño por scope

### 4.1 Presupuesto como política, no como decisión del modelo

**DECISIÓN APROBADA (ADR-004 (a), literal):** *"cada scope tiene un presupuesto máximo de tamaño definido como política del producto (no como instrucción de prompt)"*.

Tres consecuencias que este documento fija:

1. **No hay parámetro de presupuesto en la entrada** (§2.4). El modelo no puede pedir más. Su único recurso legítimo ante un `PARTIAL` es **preguntar más estrecho** —`search_case`, `get_evidence_fragment`, o el mismo scope con `params` más restrictivos—, que es precisamente la conducta deseada: recuperación selectiva en vez de volcado del expediente (`03` §7.1).
2. **El presupuesto es entrada de la función de proyección**, y por tanto parte de la definición de determinismo: *mismo estado + misma revisión + **misma versión de política** ⇒ misma salida* (§8.1). Cambiar el presupuesto cambia legítimamente la salida; el golden test fija la versión.
3. **El presupuesto se carga y valida en el arranque**, no en la llamada. Una política malformada es fallo de configuración, no una respuesta degradada.

### 4.2 Unidad de medida: bytes de serialización canónica, no tokens

`PROPUESTA DEL TECHNICAL DESIGN — requiere aprobación.`

El presupuesto se mide en **bytes UTF-8 de la serialización canónica de `content`** (§8.2), más topes por sección expresados en número de elementos.

**Por qué no en tokens**, aunque el consumidor sea un modelo y el coste real sea en tokens:

- Un tokenizador es propiedad de un proveedor y **cambia entre versiones de modelo**. Medir el presupuesto en tokens haría que la misma proyección del mismo estado cambiara al actualizar el proveedor: el golden test (§8) dejaría de ser una prueba de nuestro sistema para pasar a ser una prueba del tokenizador ajeno.
- Contradice la regla de independencia de proveedor que atraviesa el corpus (kernel §13): el Core no puede tener una dependencia dura de un artefacto del proveedor para computar su propia salida.
- El acoplamiento sería inobservable desde fuera: un cambio de tokenizador movería el punto de corte de las proyecciones **sin ningún evento, sin ninguna configuración modificada y sin ningún aviso**.

**`HIPÓTESIS` (a validar con uso real):** los bytes de la serialización canónica correlacionan lo bastante con el coste real de contexto como para que un presupuesto en bytes sea una política útil. **`POR VERIFICAR`:** el margen de seguridad necesario entre el presupuesto en bytes y el límite real de contexto del host. Mientras no se mida, el presupuesto se calibra por observación, no por cálculo, y **no se afirma ninguna equivalencia**.

### 4.3 Descriptor de política

```ts
// CONCEPTUAL. Vive en la configuración efectiva del Core; se valida al arrancar.
interface ScopeBudgetPolicy {
  policy_version: string;                  // entra en el golden test (§8.1)
  scopes: Record<Scope, {
    max_content_bytes: number;             // presupuesto total del scope
    section_order: SectionId[];            // orden de llenado; R-6 clasifica cada una
    mandatory_sections: SectionId[];       // nunca discrecionales (R-6)
    per_section_max_items?: Partial<Record<SectionId, number>>;
    per_field_max_chars?: Record<string, number>;   // único truncamiento intra-elemento (§3.3)
  }>;
}
```

### 4.4 Qué es configurable y qué no

| Elemento | ¿Configurable? | Regla |
|---|---|---|
| `max_content_bytes`, topes por sección, topes por campo | **Sí**, dentro del rango declarado por el descriptor | Subir o bajar es legítimo: cambia cuánto entra, nunca si se declara lo que falta |
| `section_order` | **Sí**, con una restricción | No puede colocar una sección `mandatory` después de una `discretionary`, ni degradar a `discretionary` una sección de familia `AUTHORITY` (R-6) |
| Presencia de `completeness` | **No** | Campo obligatorio del sobre |
| Emisión de `omissions[]` cuando hubo recorte | **No** | `INV-P-3`; una configuración que lo intente **se rechaza en la carga** |
| Contadores `{total, included}` (R-2) | **No** | Son el mecanismo 3 de §10.2 |
| Sustituir omisión por resumen generado | **No** | §3.4; la capacidad no existe |

**Nota de alcance honesta:** el Product Floor (kernel §12) tiene cinco políticas y **ninguna cubre la no-supresibilidad de `omissions`**. PF-005 cubre condiciones, no el sobre de proyección. La regla sí está cubierta a nivel de ADR Accepted —ADR-004 inv. 2—, que es nivel 1 de precedencia y por tanto suficiente para que sea normativa. Se deja registrado como **candidata a política de Product Floor**, junto con la sexta candidata que el propio kernel §12.6 señala (el log de auditoría), para que los dueños decidan explícitamente y no por omisión.

### 4.5 Valores iniciales

**`DECISIÓN PENDIENTE` heredada de ADR-004** (*"valores concretos del presupuesto por scope (política del producto; calibrar con casos reales de la usuaria)"*). Lo que sigue son **`SUPUESTO`s de arranque para poder implementar y calibrar**, no valores decididos. No se afirma que sean adecuados: se afirma que son un punto de partida explícito y modificable sin tocar código.

| Scope | `max_content_bytes` (SUPUESTO) | Topes por sección (SUPUESTO) | Justificación del orden de magnitud |
|---|---|---|---|
| `overview` | 8 KB | `recent_activity` ≤ 10 entradas | Es orientación: debe caber siempre y entero. Sus secciones caras son contadores, que son O(1) |
| `facts` | 32 KB | `list` ≤ 120 hechos | Es el scope que más crece con la vida del caso; el más expuesto a `PARTIAL` |
| `evidence` | 16 KB | `list` ≤ 80 evidencias | Inventario, no corpus: cada fila es metadato, nunca contenido |
| `pending` | 16 KB | sin tope de items en secciones `AUTHORITY` (R-6) | Si lo pendiente no cabe, el problema es el caso, no el presupuesto |
| `changes_since` | 24 KB | `detail` ≤ 200 entradas; `summary` sin tope | Los contadores agregados del delta **nunca** se recortan (§6.5) |

---

## 5. Los cinco scopes

### 5.0 Resumen

| Scope | Pregunta que responde | Secciones `mandatory` | Secciones `discretionary` | Riesgo de `PARTIAL` |
|---|---|---|---|---|
| `overview` | *¿Qué es este expediente y en qué punto está?* | `identity`, `counters`, `orientation_cursors` | `recent_activity` | Bajo |
| `facts` | *¿Qué hechos hay y cómo están sostenidos?* | `counters` | `list` | **Alto** |
| `evidence` | *¿Qué material está incorporado y en qué estado?* | `counters` | `list` | Medio |
| `pending` | *¿Qué espera una decisión o una acción?* | `awaiting_human_decision`, `counters` | `derivations`, `stale_artifacts` | Medio |
| `changes_since` | *¿Qué ha pasado desde el punto X?* | `summary` | `detail` | Medio |

Notación de las consultas: pseudocódigo conceptual sobre las tablas de `04` §3, todas dentro del **mismo snapshot de lectura** y todas acotadas por `case_id` (que en el layout adoptado es una base por Case, `04` §1.1: el aislamiento no depende de recordar el `WHERE`).

**Capa y puerto de esas consultas (locus, corrección de drift).** El SQL de este documento describe **qué dato hace falta**, no dónde se escribe. Las consultas se ejecutan **detrás de `CaseStorePort`** (`01` §2.2): el adapter de `infrastructure` las implementa y **Application consume el resultado tipado**; el código de proyección **no conoce el DDL**, no compone SQL y no importa `infrastructure` — arista prohibida por `01` §2.3 y verificada por `SC-01` (`12` §7.4). El armado de la proyección (política editorial §3, presupuesto §4, `omissions[]`) es **Application**; la ejecución del acceso, **Infrastructure**. Leer estos bloques como si Application hablara SQL sería justo la lectura que la regla de dependencias prohíbe.

---

### 5.1 Scope `overview`

**Qué responde.** La orientación mínima suficiente para retomar un expediente sin memoria previa. Es el scope que `open_case` sirve al resolver (slice, paso 2) y el que se renderiza como `memory.md` (§7).

**Contenido exacto.**

```ts
interface OverviewContent {
  identity: {                                   // sección MANDATORY
    case_id: Uuid;
    display_label: string;                      // de cases.natural_labels
    context: 'A';
    created_at: Iso8601;
    current_revision: CaseRevision;
    current_event_seq: EventSeq;
  };
  counters: {                                   // sección MANDATORY — nunca sujeta a presupuesto
    evidence_total: number;
    evidence_with_ready_derivation: number;
    derivations_pending: number;
    derivations_failed: number;
    facts_total: number;
    // Enum canónico COMPLETO (ADR-003; `02` §5.1); las cuatro claves SIEMPRE presentes.
    // En V0 solo `ALLEGED` tiene productor: `PROPOSED` es 0 por la materialización diferida
    // (`02` §5.2, §5.2 de este documento) y `DETERMINED`/`WITHDRAWN` son 0 por no tener
    // productor (mismo patrón declarativo que `FactWithdrawn`). Un cero declarado es un dato;
    // una clave ausente obligaría a cambiar el contrato al aparecer el productor.
    facts_by_stored_status: { PROPOSED: number; ALLEGED: number;
                              DETERMINED: number; WITHDRAWN: number };
    facts_by_derived_state: { supported: number; contradicted: number; unsupported: number };
    active_links_by_polarity: { SUPPORTS: number; CONTRADICTS: number; CONTEXTUALIZES: number };
    proposals_with_pending_items: number;
    proposal_items_pending: number;
    artifacts_registered: number;
    artifacts_stale: number;
  };
  orientation_cursors: {                        // sección MANDATORY — §6.2
    // TODOS los cursores son `event_seq` y NINGUNO es `case_revision`: bajo la enmienda AC-02
    // (kernel §5.2) el evento ancla `ProposalReviewed` lleva `case_revision` NULA, de modo que
    // no existe revisión equivalente que ofrecer. Ofrecer una sería inventarla.
    current_event_seq: EventSeq;
    last_human_review_event_seq: EventSeq | null;
    last_human_review_at: Iso8601 | null;
    case_created_event_seq: EventSeq;           // fallback universal del delta
  };
  recent_activity: {                            // sección DISCRETIONARY
    total: number; included: number;
    entries: DeltaEntry[];                      // mismo vocabulario cerrado que §6.3
  };
}
```

**Consultas que lo alimentan.**

```sql
-- identity
SELECT case_id, natural_labels, context, created_at, current_revision, current_event_seq FROM cases;

-- counters (todos COUNT/GROUP BY sobre el mismo snapshot)
SELECT COUNT(*) FROM evidence;
SELECT state, COUNT(*) FROM derived_representations GROUP BY state;
SELECT COUNT(*) FROM facts;
-- estatus ALMACENADO vigente = última entrada de la historia (ADR-003; jamás columna en facts)
SELECT h.status, COUNT(*) FROM fact_status_history h
  JOIN (SELECT fact_id, MAX(seq) AS seq FROM fact_status_history GROUP BY fact_id) u
    ON u.fact_id = h.fact_id AND u.seq = h.seq
  GROUP BY h.status;
-- estados DERIVADOS: se computan aquí, no se leen (ADR-003 inv. 6; tabla de verdad 02 §5.3)
SELECT polarity, COUNT(*) FROM evidence_links WHERE link_state = 'ACTIVE' GROUP BY polarity;

-- decisión EFECTIVA, jamás la almacenada (ADR-008 Consecuencias; `06` §2.5). Ver §5.4.
WITH effective AS ( /* definición única en §5.4 */ )
SELECT COUNT(DISTINCT proposal_id) FILTER (WHERE effective_decision = 'PENDING'),
       COUNT(*)                    FILTER (WHERE effective_decision = 'PENDING')
  FROM effective;                        -- proposals_with_pending_items, proposal_items_pending

SELECT stale, COUNT(*) FROM artifacts WHERE status = 'REGISTERED' GROUP BY stale;

-- orientation_cursors
SELECT MAX(event_seq), MAX(occurred_at) FROM case_events WHERE event_type = 'ProposalReviewed';
SELECT event_seq FROM case_events WHERE event_type = 'CaseCreated';

-- recent_activity: los N últimos eventos, proyectados al vocabulario cerrado de §6.3
SELECT event_seq, event_type, payload, occurred_at, principal_type, provenance_kind
  FROM case_events ORDER BY event_seq DESC LIMIT :n;
```

**Política editorial.**
`identity`, `counters` y `orientation_cursors` son `mandatory` y de tamaño acotado por construcción: `overview` prácticamente nunca es `PARTIAL`. Lo único discrecional es `recent_activity`, cuyo orden es `event_seq` descendente (R-4) y cuyo recorte es por el extremo antiguo. **Los contadores son el ancla de todo el resto del contrato**: son baratos, siempre completos y describen la magnitud real del caso, de modo que ninguna lista recortada en otro scope puede hacer creer que el expediente es más pequeño de lo que es (§10.2, mecanismo 3).

**Presupuesto conceptual.** El más pequeño de los cinco (SUPUESTO: 8 KB). Es deliberado: `overview` se pide **en cada apertura de caso**, y un `overview` caro convertiría cada saludo en un volcado.

**Regla de decisión efectiva (ADR-008, obligatoria).** Los contadores `proposals_with_pending_items` y `proposal_items_pending` se computan sobre la **decisión efectiva** (`effective_decision`, §5.4), nunca sobre `proposal_items.review_decision` almacenado. ADR-008 §Consecuencias es literal: *"Exige que las proyecciones expongan siempre la efectiva y nunca la almacenada"*, y su RIESGO declarado es que *"si una proyección expusiera la almacenada, mostraría como aprobado algo que no puede commitearse"*. Aquí el efecto sería el simétrico y peor: un item aprobado cuya autorización quedó invalidada **desaparecería** del recuento de pendientes, y `overview` —el scope que se sirve en cada apertura de caso— diría que no hay nada esperando decisión humana cuando sí lo hay. Ver §5.4 para la definición única de `effective_decision` y el contract test que la protege.

**Regla de no-elevación de estado.** `overview` reporta `facts_by_stored_status` **y** `facts_by_derived_state` como dos bloques distintos y nunca los fusiona. `supported` no es un estatus del hecho: es una propiedad computada de sus links (`02` §5.3). Presentar "3 hechos acreditados" cuando lo que hay son 3 hechos `ALLEGED` con links `SUPPORTS` sería exactamente la elevación de estado que el slice prohíbe (*"'alegado' ≠ 'acreditado'"*).

---

### 5.2 Scope `facts`

**Qué responde.** El conjunto de hechos que **son estado curado del Case**, con su estatus almacenado vigente y su estado derivado computado.

**Frontera crítica.** `facts` **no contiene candidatos**. Bajo la materialización diferida (`02` §5.2, `PROPUESTA DEL TECHNICAL DESIGN`), un `Fact` se materializa en el commit: los items propuestos y no aprobados viven en `proposal_items` y se ven por `pending`, nunca aquí. Consecuencia declarada: **en V0 ningún `Fact` tiene estatus vigente `PROPOSED`** —la entrada `PROPOSED` se escribe en la misma transacción que la `ALLEGED`—, de modo que `params.status_filter: ['PROPOSED']` es sintácticamente válido y **devuelve lista vacía con `completeness: COMPLETE`**. No es un error ni una omisión: es la respuesta correcta. Si la materialización diferida no se aprueba, esta frontera cambia y este apartado se corrige.

**Contenido exacto.**

```ts
interface FactsContent {
  counters: {                                   // MANDATORY
    total: number;
    by_stored_status: Record<'PROPOSED'|'ALLEGED'|'DETERMINED'|'WITHDRAWN', number>;  // §5.1
    by_derived_state: { supported: number; contradicted: number; unsupported: number };
    both_supported_and_contradicted: number;    // no es una anomalía: es un dato del caso
  };
  list: {                                       // DISCRETIONARY
    total: number; included: number;
    items: Array<{
      fact_id: Uuid;
      statement_text: string;                   // recorte por campo posible (§3.3), declarado
      alleged_only: boolean;
      stored_status: 'PROPOSED' | 'ALLEGED' | 'DETERMINED' | 'WITHDRAWN';  // enum canónico
                                                               // completo; SIEMPRE presente
                                                               // (INV-D-38). En V0 solo
                                                               // `ALLEGED` es alcanzable
      stored_status_at_revision: CaseRevision;
      derived_state: { supported: boolean; contradicted: boolean; unsupported: boolean };
      links_summary: { SUPPORTS: number; CONTRADICTS: number; CONTEXTUALIZES: number }; // ACTIVE
      provenance: { provenance_kind: ProvenanceKind;
                    principal_type: 'HUMAN'|'AI'|'SYSTEM';
                    principal_role: string };
      origin: { proposal_id: Uuid; proposal_item_id: Uuid } | null;
    }>;
  };
}
```

**Consultas que lo alimentan.**

```sql
-- hechos + estatus almacenado vigente
SELECT f.fact_id, f.statement_text, f.alleged_only,
       f.provenance_kind, f.principal_type, f.principal_role,
       h.status AS stored_status, h.at_revision
  FROM facts f
  JOIN fact_status_history h ON h.fact_id = f.fact_id
  JOIN (SELECT fact_id, MAX(seq) AS seq FROM fact_status_history GROUP BY fact_id) u
    ON u.fact_id = h.fact_id AND u.seq = h.seq;

-- links ACTIVE agregados por hecho y polaridad → insumo del cómputo derivado
SELECT fact_id, polarity, COUNT(*) FROM evidence_links
 WHERE link_state = 'ACTIVE' GROUP BY fact_id, polarity;

-- origen del hecho (trazabilidad a la propuesta que lo produjo)
SELECT committed_fact_id, proposal_id, proposal_item_id FROM proposal_items
 WHERE commit_state = 'COMMITTED';
```

El estado derivado se computa en memoria con la función pura y total de `02` §5.3: `CONTEXTUALIZES` **no participa**; `supported` y `contradicted` **no son excluyentes**; `unsupported === !(supported || contradicted)`.

**Política editorial.**

Orden de llenado de `list` (aplicación literal de R-3, *el recorte nunca es optimista*), por clases de prioridad descendente:

| Clase | Criterio | Por qué va primero |
|---|---|---|
| **P1** | `derived_state.contradicted = true` | Hay prueba en el expediente que contradice el hecho. Es lo que la profesional no puede permitirse no ver |
| **P2** | `stored_status = 'ALLEGED'` **y** `derived_state.unsupported = true` | Se alegó y hoy nada en el expediente lo sostiene |
| **P3** | `alleged_only = true` | Declarado explícitamente como solo alegado: legítimo, pero no debe leerse como acreditado |
| **P4** | Resto | Hechos alegados y sostenidos |

Dentro de cada clase: `stored_status_at_revision` descendente, desempate `fact_id` ascendente (R-4). Con presupuesto insuficiente, lo que cae es P4 —lo tranquilizador— y nunca P1.

**Presupuesto conceptual.** El mayor de los scopes de lista (SUPUESTO: 32 KB / 120 hechos). Es el candidato natural a `PARTIAL` y por tanto el que ejercita el invariante de §10 en el caso sintético grande (F15).

**Vocabulario de omisión.** `facts.list` (`budget`), `facts.list.statement_text` (recorte por campo).

---

### 5.3 Scope `evidence`

**Qué responde.** Qué material está **incorporado** en este Case, en qué estado utilizable se encuentra y qué sostiene.

**Frontera crítica.** `evidence` es un **inventario, no un corpus**. No devuelve contenido de Sources ni de derivaciones ni fragmentos: eso es `search_case` (recuperación selectiva) y `get_evidence_fragment` (contenido exacto con provenance). Volcar contenido aquí anularía la razón de existir de esas dos tools (`03` §7.1).

**Contenido exacto.**

```ts
interface EvidenceContent {
  counters: {                                   // MANDATORY
    total: number;
    with_ready_derivation: number;
    derivations_pending: number;
    derivations_failed: number;
    not_referenced_by_any_active_link: number;
  };
  list: {                                       // DISCRETIONARY
    total: number; included: number;
    items: Array<{
      evidence_id: Uuid;
      source_id: Uuid;
      media_type: string;
      byte_size: number;
      incorporated_at: Iso8601;
      declared_origin: { label: string; kind: string };   // del sobre de ingestión, kernel §1.2
      derivations: Array<{ derivation_id: Uuid; kind: 'TRANSCRIPT'|'NORMALIZED_TEXT'|'OCR_TEXT';
                           version: number; state: 'PENDING'|'READY'|'FAILED';
                           failure_reason_code?: string }>;
      citable: boolean;                          // true ⇔ existe derivación READY o el original es citable directo
      active_links: number;
      provenance: { provenance_kind: 'EXTERNAL_SOURCE';
                    principal_type: 'HUMAN'|'SYSTEM'; principal_role: string };
    }>;
  };
}
```

**Sin `content_hash`.** Aplicación de kernel §11: un hash no es identificador de entidad y no se muestra. El modelo no necesita el hash para nada que pueda hacer (no puede verificar integridad, no puede usarlo como id), y exponerlo invita a que lo use como identificador — el error exacto que la regla prohíbe. La verificación periódica de integridad (PF-002) es operación interna del Core y no pasa por la superficie.

**Consultas que lo alimentan.**

```sql
SELECT e.evidence_id, e.source_id, e.incorporated_at,
       s.media_type, s.byte_size, s.provenance_kind, s.principal_type, s.principal_role
  FROM evidence e JOIN sources s ON s.source_id = e.source_id;

SELECT source_id, derivation_id, kind, version, state, failure_reason
  FROM derived_representations;

SELECT evidence_id, COUNT(*) FROM evidence_links
 WHERE link_state = 'ACTIVE' GROUP BY evidence_id;

-- último sobre de ingestión declarado por Source
SELECT source_id, declared_origin, ingested_at FROM source_ingestions;
```

**Política editorial.** Orden de llenado por R-3:

1. Evidencia con derivación `FAILED` (material incorporado que **no puede usarse** y que puede pasar inadvertido).
2. Evidencia con derivación `PENDING` (aún no utilizable).
3. Evidencia `READY` **sin ningún link activo** (material incorporado que no sostiene nada: el candidato más probable a haberse olvidado).
4. Resto, por `incorporated_at` descendente.

Desempate final: `evidence_id` ascendente.

**Presupuesto conceptual.** SUPUESTO: 16 KB / 80 evidencias. Al ser metadato puro, el tamaño por elemento es estable y predecible, a diferencia de `facts`.

**Vocabulario de omisión.** `evidence.list` (`budget`), `evidence.list.derivations` (`budget`, cuando una evidencia tiene muchas versiones).

---

### 5.4 Scope `pending`

**Qué responde.** Todo lo que **espera algo**: una decisión humana, una derivación, una reconciliación o una revisión de un análisis obsoleto. Es el scope que hace visible el trabajo que el sistema **no** hará solo.

**Contenido exacto** (ADR-004 (a) fija la lista: *"Proposals en estado PENDING, DerivedRepresentations en PENDING/FAILED, Artifacts marcados stale y condiciones activas"*; se añade la preservación por conflicto, exigida por ADR-004 (c) y por `06` §5).

```ts
interface PendingContent {
  counters: { proposals_pending: number; items_pending: number;   // sobre `effective_decision`
              proposals_preserved: number; derivations_pending: number;
              derivations_failed: number; artifacts_stale: number };   // MANDATORY

  awaiting_human_decision: {                    // MANDATORY — familia AUTHORITY, jamás discrecional
    total: number; included: number;
    proposals: Array<{
      proposal_id: Uuid;
      base_case_revision: CaseRevision;
      methodology_version: string;
      model_id: string | null;
      items_total: number;
      // SIEMPRE la decisión EFECTIVA; JAMÁS `proposal_items.review_decision` almacenado (ADR-008)
      items_by_effective_decision: { PENDING: number; APPROVED: number; REJECTED: number };
      items_effective_approved_uncommitted: number;
      status_derived: ProposalDerivedStatus;   // rótulo agregado DERIVADO — vocabulario único,
                                               // orden de evaluación y predicados: 06 §2.7.
                                               // Esta proyección NO define rótulos propios.
      created_at: Iso8601;
    }>;
  };

  derivations: {                                // DISCRETIONARY
    total: number; included: number;
    items: Array<{ derivation_id: Uuid; evidence_id: Uuid; kind: string;
                   state: 'PENDING' | 'FAILED'; failure_reason_code?: string }>;
  };

  stale_artifacts: {                            // DISCRETIONARY
    total: number; included: number;
    items: Array<{ artifact_id: Uuid; type: 'FactAnalysis';
                   case_revision: CaseRevision;      // revisión a la que se registró
                   stale_reasons: Array<'NEW_EVIDENCE'|'INPUT_SUPERSEDED'|'METHODOLOGY_CHANGED'>;
                   marked_at: Iso8601 }>;
  };

  active_conditions: TypedCondition[];          // MANDATORY — computadas del estado, no almacenadas
}
```

**Consultas que lo alimentan.**

```sql
-- DEFINICIÓN ÚNICA de la decisión EFECTIVA. Materializa `effectiveReviewDecision` de `06` §2.5.
-- Toda proyección de este documento la consume; NINGUNA lee `review_decision` directamente.
-- Parámetros del MISMO snapshot de lectura (`03` §0.4): :current_revision, :now.
WITH effective AS (
  SELECT i.proposal_id, i.proposal_item_id, i.commit_state,
         CASE
           -- (0) lo ya commiteado no puede invalidarse a posteriori: su autorización fue
           --     consumida y `FactsCommitted` está en el log. ADR-008 inv. 2 hace de
           --     APPROVED+COMMITTED la única combinación commiteada alcanzable.
           WHEN i.commit_state = 'COMMITTED'   THEN 'APPROVED'
           -- (1) PENDING y REJECTED se proyectan tal cual: no hay nada que invalidar
           WHEN i.review_decision <> 'APPROVED' THEN i.review_decision
           -- (2) el contenido de la ÚLTIMA revisión ya no es el contenido actual
           --     (kernel §2.3, cond. 2; `06` §2.5 compara contra `lastReview`, no contra
           --      cualquier revisión histórica: una aprobación vieja no revive un item)
           WHEN ( SELECT r.item_content_hash
                    FROM proposal_item_reviews r
                    JOIN case_events ev ON ev.event_id = r.event_id
                   WHERE r.proposal_item_id = i.proposal_item_id
                   ORDER BY ev.event_seq DESC      -- ORDEN POR `event_seq`, JAMÁS por
                   LIMIT 1 ) <> i.item_content_hash --   `reviewed_at` (`09` §2.7)
             THEN 'PENDING'
           -- (3) no hay autorización VIVA: existe, no consumida, hash y revisión coincidentes,
           --     operación correspondiente y no expirada   (kernel §2.3, cond. 1–5)
           WHEN NOT EXISTS (
                  SELECT 1 FROM human_authorizations a
                   WHERE a.proposal_item_id       = i.proposal_item_id
                     AND a.consumed_at            IS NULL
                     AND a.item_content_hash      = i.item_content_hash
                     -- AC-02: `expected_case_revision` es la revisión contra la que se GENERÓ y se
                     --   REVISÓ la Proposal; `ProposalReviewed` NO la avanza. Sin circularidad
                     AND a.expected_case_revision = :current_revision
                     AND a.authorized_operation   = 'COMMIT_FACT'   -- AC-01: singular, por item
                     AND a.expires_at             > :now )
             THEN 'PENDING'
           ELSE 'APPROVED'
         END AS effective_decision
    FROM proposal_items i )

SELECT p.proposal_id, p.base_case_revision, p.methodology_version, p.model_id, p.created_at,
       SUM(e.effective_decision = 'PENDING')  AS pending,
       SUM(e.effective_decision = 'APPROVED') AS approved,
       SUM(e.effective_decision = 'REJECTED') AS rejected,
       SUM(e.effective_decision = 'APPROVED' AND e.commit_state = 'UNCOMMITTED')
         AS effective_approved_uncommitted
  FROM proposals p JOIN effective e ON e.proposal_id = p.proposal_id
 GROUP BY p.proposal_id;

SELECT d.derivation_id, e.evidence_id, d.kind, d.state, d.failure_reason
  FROM derived_representations d JOIN evidence e ON e.source_id = d.source_id
 WHERE d.state IN ('PENDING','FAILED');

SELECT a.artifact_id, a.type, a.case_revision, r.reason, r.marked_at
  FROM artifacts a JOIN artifact_stale_reasons r ON r.artifact_id = a.artifact_id
 WHERE a.stale = 1;
```

**La proyección expone la decisión EFECTIVA, nunca la almacenada — regla dura de ADR-008.**

ADR-008 §Consecuencias no admite lectura suave: *"Exige que las proyecciones expongan siempre la efectiva y nunca la almacenada"*, y su RIESGO declarado es que *"si una proyección expusiera la almacenada, mostraría como aprobado algo que no puede commitearse"*. Este documento lo materializa así:

| Regla | Contenido |
|---|---|
| Nombre del valor proyectado | **`effective_decision`**. `proposal_items.review_decision` es **dato almacenado, no dato de salida**: ninguna proyección de §5 lo emite, lo cuenta ni lo filtra |
| Predicado | `effective_decision = 'APPROVED'` **⇔** `review_decision = 'APPROVED'` **y** existe autorización **viva** para el item: no consumida, con `item_content_hash` **y** `expected_case_revision` coincidentes con el estado vigente, `authorized_operation = 'COMMIT_FACT'` (singular y **por `ProposalItem`**, enmienda AC-01) y no expirada (kernel §2.3, condiciones 1–5; `06` §2.5). En cualquier otro caso el item se proyecta `PENDING`. **Lectura de `expected_case_revision` bajo la enmienda AC-02:** es la revisión contra la que se **generó y se revisó** la Proposal, no la que dejaría el propio acto de revisión —`ProposalReviewed` no avanza `case_revision`—. La comparación con la revisión vigente no cambia de forma (sigue exigiendo que el Case no haya mutado) pero sí de significado, y desaparece la circularidad que el Modelo A anterior obligaba a corregir |
| Nombres de salida | `items_by_effective_decision` y `items_effective_approved_uncommitted` (aquí); `counters.items_pending` / `counters.proposals_pending` (aquí); `proposal_items_pending` / `proposals_with_pending_items` (§5.1). **Todos** computados sobre el CTE `effective` de arriba, que es su **definición única** |
| Locus | **Application**, al construir la proyección. No es columna: almacenarla reintroduciría el estado derivable-que-puede-divergir que ADR-008 inv. 3 elimina (*"la invalidación de una aprobación es derivada, jamás almacenada"*) |

**Por qué `commit_state = 'COMMITTED'` va primero en el CTE.** Un item ya commiteado tiene su autorización **consumida** (`consumed_at NOT NULL`), de modo que el predicado de autorización viva fallaría y lo proyectaría como `PENDING` — mostrando como pendiente de decisión un hecho que ya está en el expediente. La guarda no es una excepción al principio: ADR-008 inv. 2 hace de `APPROVED + COMMITTED` la única combinación commiteada alcanzable, y `commit_state` no retrocede (`06` §2.6).

**`RIESGO` heredado que esta proyección no cierra.** La condición "no expirada" depende del **reloj de pared**, no de la cadena de eventos: un reloj atrasado puede hacer aparecer viva una autorización expirada, y entonces la proyección mostraría `APPROVED` un item que el gate también aceptaría. `09-events-and-audit.md` §2.7 lo registra como `DECISIÓN PENDIENTE` (guarda de monotonía del reloj) y aquí **no se resuelve**. Lo que sí se garantiza es que **proyección y gate evalúan el mismo predicado**: no puede existir un item que la proyección declare aprobado y el gate rechace por una razón distinta del tiempo.

**Contract test que ADR-008 exige como mitigación** — `INV-P-13` (§11). Sobre `get_case_context(pending)` y `get_case_context(overview)`, con el montaje de `AT-004` (`12` §3.5: aprobar un item y alterar después su `item_content_hash` a nivel de store):

1. **Antes** de alterar: el item cuenta en `items_by_effective_decision.APPROVED` y en `items_effective_approved_uncommitted`.
2. **Después** de alterar, **con cero mutaciones canónicas**: el mismo item cuenta en `items_by_effective_decision.PENDING`, y `overview` incrementa `proposal_items_pending`. El `ProposalItemReview` y la `HumanAuthorization` **siguen íntegros en el store**: lo que cambia es la proyección, no el registro (ADR-008 alternativa 6, rechazada).
3. **Assert negativo — es el que cierra el riesgo declarado por ADR-008:** ninguna respuesta de `pending` ni de `overview` contiene un valor procedente de `review_decision` almacenado. Property: para todo estado sembrado, `proyección(estado) == proyección_recomputada_solo_con_effective_decision(estado)`.
4. **Simétrico de expiración** (reutiliza `FT-008.c` y `FakeClock`): avanzar el reloj más allá de `expires_at` ⇒ el item pasa a `PENDING` en la proyección **sin evento nuevo**.

`DIVERGENCIA A RECONCILIAR` con `12-testing-strategy.md`: `AT-004` afirma hoy la decisión efectiva sobre el **gate**, no sobre la **proyección**. Los asserts 1–4 son un añadido a `AT-004`, no un `FT` nuevo — la matriz `FT-001…FT-014` está declarada cerrada en V0 (`12` §0). Registrado en §12.3.

**`status_derived` y su dependencia declarada.** `04-persistence-model.md` §10 **C1** deja abierto cómo se representa `PRESERVED_FOR_RECONCILIATION` (la tabla `proposals` no tiene columna de estado agregado). Este documento **no reabre C1 y no define vocabulario**: el conjunto de rótulos (`PENDING | PARTIALLY_COMMITTED | RESOLVED | PRESERVED_FOR_RECONCILIATION`), su **orden de evaluación** y el **predicado canónico** de `PRESERVED_FOR_RECONCILIATION` —anclado en el evento `ProposalPreservedForReconciliation` sin `FactsCommitted` posterior que lo consuma— están fijados en **`06` §2.7** y se citan sin reformular.

Ese predicado es computable desde el log canónico sin columna nueva, y por tanto compatible con las dos salidas de C1. **RESUELTO — enmienda AC-04 aprobada** (antes `DECISIÓN PENDIENTE` heredada, en los mismos términos que `03` §0.5 y `06` §2.7): `ProposalPreservedForReconciliation` **queda en la lista cerrada de eventos sin productor en v0**, con el mismo patrón declarativo que `FactWithdrawn`; la **preservación de una propuesta ante conflicto es la conducta por defecto del Core y un estado derivado, no un estado almacenado ni un evento que se emita**. Consecuencias exactas para esta proyección: en V0 `status_derived` **nunca** toma el valor `PRESERVED_FOR_RECONCILIATION` y `counters.proposals_preserved` es siempre `0`; ninguna consulta de §5.4 espera encontrar ese evento en `case_events`; y el predicado citado de `06` §2.7 queda como **contrato del día en que el evento tenga productor**, no como camino alcanzable hoy. Se declara aquí para que un contador permanentemente en cero no se lea como "no hay conflictos" sino como "el rótulo no tiene productor en v0".

**Política editorial.**

- `awaiting_human_decision` y `active_conditions` son `mandatory` por R-6: **nunca** se recortan por presupuesto. Si lo pendiente no cabe, la respuesta se sirve `PARTIAL` habiendo cortado antes `derivations` y `stale_artifacts`.
- Orden interno: primero las propuestas con `status_derived = 'PRESERVED_FOR_RECONCILIATION'` (trabajo bloqueado por un conflicto, ADR-004 lo describe como flujo de trabajo, no como error), luego por `items_pending` descendente —**contado sobre `effective_decision`**, de modo que una propuesta cuyas aprobaciones quedaron invalidadas sube en el orden en vez de hundirse—, desempate `proposal_id`.
- `stale_artifacts` lleva **siempre** su `stale_reasons`: la marca es acumulativa y **ninguna tool puede limpiarla** (`04` §3.4). Un artifact stale sin razón sería una condición `ANALYSIS_STALE` que no puede explicarse.

**Presupuesto conceptual.** SUPUESTO: 16 KB, sin tope de items en las secciones `AUTHORITY`.

**`RIESGO` heredado (ADR-004):** *señal/ruido de `pending`*. Si `pending` acumula demasiado, la usuaria dejará de mirarlo. Este documento aporta dos mitigaciones y ninguna garantía: (a) los contadores permiten ver la magnitud sin leer la lista; (b) el orden por R-3 pone arriba lo bloqueado. La calibración real es con uso.

---

### 5.5 Scope `changes_since`

Contrato, cursor, vocabulario, agregación y presupuesto en **§6**, por ser el mecanismo central del encargo.

---

### 5.6 Scope `procedural` — RESERVADO

`procedural` **no es miembro del enum** `Scope`. Está documentado en el contrato y **no implementado** (kernel §9; ADR-004 (a)). Pedirlo produce `VALIDATION_FAILED` (`05` §6.2) / `E_SCHEMA_INVALID` (`03` §6.4), **jamás** una degradación silenciosa a otro scope: *un scope reservado que se acepta en silencio deja de ser reservado*.

Se reserva el par `{ section: 'procedural', reason: 'not_implemented' }` del vocabulario de omisiones para el día que exista un scope compuesto que lo incluya. En V0 **nada lo emite**: no hay scope que lo contenga, y por tanto no hay omisión que declarar. Declararlo sin productor sería simular una capacidad ausente.

Razón del reservado (ADR-004): el slice **no contiene lógica procesal**. Motor de plazos y motor procesal son POST-V0 (kernel §15).

---

## 6. El delta de sesión: `changes_since`

### 6.1 El cursor es `event_seq`, no `case_revision`

**PROPUESTA DEL TECHNICAL DESIGN, heredada de `03` §0.7 y adoptada aquí sin cambios.** Con la **enmienda AC-02 aprobada** (kernel §5.2) deja de ser una elección defensiva y pasa a ser la **única opción correcta**: ver el desenlace al final de esta sección.

Bajo el modelo vigente del kernel §5.2 hay eventos que **no** avanzan `case_revision` —`ProposalReviewed`, que lleva `case_revision` **nula**, y `ProposalPreservedForReconciliation` el día que tenga productor (hoy declarado en la lista cerrada **sin productor en v0**, enmienda AC-04; §5.4)—. Si el delta se cursara por revisión, esos actos serían invisibles: **desaparecerían del resumen de sesión precisamente las decisiones de la profesional**, que es la información más valiosa del delta.

```ts
interface ChangesSinceParams {
  since_event_seq?: EventSeq;    // cursor exacto
  since_revision?: CaseRevision; // admitido; se resuelve internamente al event_seq de esa revisión
}
```

- Exactamente uno de los dos es obligatorio. Ninguno ⇒ `VALIDATION_FAILED`. Los dos ⇒ `VALIDATION_FAILED` (no se elige por el invocador: si discrepan, adivinar sería exactamente lo que el sistema no hace).
- Rango válido: `since_event_seq ∈ [0, current_event_seq]` (0 significa "desde el origen"); `since_revision ∈ [1, case_revision]` (`05` §6.2). Fuera de rango ⇒ `VALIDATION_FAILED`; **nunca** se recorta silenciosamente al extremo.
- El eco en `params` devuelve **ambos** resueltos (§2.2.4), de modo que la llamada siguiente no tenga que volver a resolver nada. **Con una asimetría que la enmienda AC-02 hace explícita:** `since_revision` es `null` en el eco cuando el evento ancla no mutó estado epistémico canónico —caso típico, `ProposalReviewed`—, porque ese evento **no tiene revisión asociada** y devolver la revisión vigente en ese punto haría pasar por equivalentes dos cursores que no lo son. La resolución `since_revision → since_event_seq` es total; la inversa **no**, y ésa es exactamente la razón de que el cursor canónico sea `event_seq`.

**Divergencia declarada:** `05-mcp-contract.md` §6.2 declara en su `input` solo `since_revision` como obligatorio. La admisión de `since_event_seq` es **aditiva** y procede de `03` §0.7; sin ella, bajo el modelo vigente (enmienda AC-02) el delta **no puede referirse a un acto de revisión**, porque ese acto no tiene revisión que citar. Requiere reconciliación de `05`, y con AC-02 aprobada deja de ser una mejora opcional: es condición de corrección del scope.

**RESUELTO — enmienda AC-02 aprobada. Desenlace del análisis de los dos modelos, conservado por trazabilidad.**

| | **Modelo A — anterior, superado por AC-02** | **Modelo B — VIGENTE (kernel §5.2)** |
|---|---|---|
| `ProposalReviewed` y `case_revision` | Avanzaba `case_revision` | Avanza `event_seq`; `case_revision` **nula** |
| Cursor suficiente para el delta | `case_revision` habría bastado | **Solo `event_seq`**; por revisión el acto de revisión es invisible |
| `expected_case_revision` de la autorización | La revisión resultante del propio acto de revisión (circular) | La revisión contra la que se generó **y se revisó** la propuesta; sin circularidad |

Lo que este documento eligió antes de la aprobación —cursar por `event_seq`— era correcto bajo los dos modelos y el único correcto bajo B; por eso el diseño del delta **no cambió** al aprobarse la enmienda. Lo que sí cambia, y está aplicado en §6.3, §6.4 y §9.2, es la **aritmética**: qué eventos llevan `case_revision` no nula y, en consecuencia, qué revisión declara el sobre para un `event_seq` dado.

### 6.2 De dónde sale el cursor **sin memoria de sesión**

Éste es el punto donde el diseño se juega la propiedad 8 del slice (*reapertura en otra sesión*). Si el cursor tuviera que recordarse, `changes_since` sería inútil justo en el caso para el que existe.

**PROPUESTA DEL TECHNICAL DESIGN — requiere aprobación.** `overview` incluye una sección `mandatory` `orientation_cursors` (§5.1) con un **ancla canónica computable**:

```text
last_human_review_event_seq  :=  MAX(event_seq) de los eventos ProposalReviewed del Case
                                 (NULL si el Case aún no ha tenido ninguna revisión humana)
case_created_event_seq       :=  event_seq del evento CaseCreated  (fallback universal)
```

Semántica: **la última vez que la profesional miró el expediente**. Es exactamente el punto de referencia que el slice usa en su paso 14 (`changes_since(7)`, *"la última revisión que la usuaria conoció antes del commit"*), y es **estado canónico**, no memoria.

**Por qué `ProposalReviewed` y no "el último evento con `principal_type = HUMAN`":** en V0 casi todos los eventos llevan principal humano —incorporar una evidencia por orden de la usuaria es `principal_type = HUMAN` con `provenance_kind = EXTERNAL_SOURCE` (kernel §1.4)—, de modo que ese criterio devolvería casi siempre el evento anterior y el delta sería vacío. `ProposalReviewed` es el único evento que registra **un acto de atención deliberada de la profesional sobre el contenido del expediente**.

**El Core sigue sin adivinar.** El ancla se **ofrece** en `overview`; no se aplica por defecto. `changes_since` sin cursor es rechazo (§6.1). La diferencia importa: el invocador declara el punto de referencia y la respuesta lo ecoa, de modo que el delta siempre dice **respecto de qué** es un delta.

**Secuencia completa de reapertura, con cero memoria:**

```mermaid
sequenceDiagram
    participant P as Profesional
    participant C as Modelo (sesión nueva, contexto vacío)
    participant C0 as Core
    P->>C: "Retomemos el caso de X"
    C->>C0: open_case("X")
    C0-->>C: RESOLVED { case_id, case_revision }  (o candidatos; nunca adivina)
    C->>C0: get_case_context(overview)
    C0-->>C: identity + counters + orientation_cursors{ last_human_review_event_seq: 7 }
    C->>C0: get_case_context(changes_since, { since_event_seq: 7 })
    C0-->>C: summary + detail + completeness + omissions
    C->>P: orientación + delta, sin haber recordado nada
```

**Tres llamadas QUERY, cero eventos, cero mutaciones.** Es el montaje de AT-010 (§9).

### 6.3 Vocabulario cerrado de entradas de delta

El delta **no es un volcado del Case Event Log**. Tres razones: (a) el `payload` de un evento es *"suficiente para reconstrucción"* (ADR-004 (b)1) y puede ser grande — volcarlo agota el presupuesto con datos que nadie necesita para orientarse; (b) el log es auditoría canónica y el delta es orientación: audiencias y criterios de completitud distintos; (c) sin vocabulario cerrado no hay agregación posible ni plantilla de presentación estable.

```ts
type DeltaEntryKind =
  | 'CASE_CREATED'
  | 'EVIDENCE_ADDED'
  | 'EVIDENCE_BECAME_CITABLE'
  | 'DERIVATION_FAILED'
  | 'FACTS_PROPOSED'
  | 'PROPOSAL_REVIEWED'
  | 'FACT_STATUS_CHANGED'
  | 'ANALYSIS_REGISTERED'
  | 'ANALYSIS_MARKED_STALE'
  | 'PROPOSAL_PRESERVED';   // sin productor en V0 (enmienda AC-04, §5.4)

interface DeltaEntry {
  kind: DeltaEntryKind;
  event_seq: EventSeq;
  case_revision: CaseRevision | null;   // NULL si el evento no mutó estado epistémico canónico
                                        // (kernel §5.2, enmienda AC-02 aprobada: caso de
                                        // `ProposalReviewed`). `event_seq` es SIEMPRE no nulo
  occurred_at: Iso8601;
  principal_type: 'HUMAN' | 'AI' | 'SYSTEM';
  provenance_kind: ProvenanceKind;
  refs: Record<string, Uuid | Uuid[]>;  // ids de las entidades afectadas
  facts: Record<string, string | number>;  // datos mínimos, vocabulario del contrato
}
```

**Mapeo evento → entrada** (la lista de eventos v0 es cerrada, kernel §8.1; el mapeo es total):

| `event_type` | `DeltaEntryKind` | Proyectado desde el payload |
|---|---|---|
| `CaseCreated` | `CASE_CREATED` | `display_label` |
| `EvidenceIncorporated` | `EVIDENCE_ADDED` | `evidence_id`, `media_type`, `declared_origin.label` |
| `DerivedRepresentationGenerated` | `EVIDENCE_BECAME_CITABLE` | `evidence_id`, `kind`, `version` |
| `DerivedRepresentationFailed` | `DERIVATION_FAILED` | `evidence_id`, `kind`, `failure_reason_code` |
| `FactsProposed` | `FACTS_PROPOSED` | `proposal_id`, `items_total`, `methodology_version` |
| `ProposalReviewed` | `PROPOSAL_REVIEWED` | `proposal_id`, `approved`, `rejected`, `pending`. **`case_revision` de la entrada es `null`** (AC-02): es el único evento con productor en v0 que no muta estado epistémico canónico |
| `FactsCommitted` | `FACT_STATUS_CHANGED` | `fact_ids[]`, `from: 'PROPOSED'`, `to: 'ALLEGED'`, `count` |
| `ArtifactRegistered` | `ANALYSIS_REGISTERED` | `artifact_id`, `type` |
| `ArtifactMarkedStale` | `ANALYSIS_MARKED_STALE` | `artifact_id`, `reason` |
| `ProposalPreservedForReconciliation` | `PROPOSAL_PRESERVED` | *(sin productor en V0)* — `proposal_id`, `expected`, `current` el día que lo tenga. Enmienda **AC-04**: la preservación es conducta por defecto y **estado derivado**, no evento emitido; el mapeo existe para no reabrir el contrato (§5.4) |
| `FactWithdrawn` | *(sin productor en V0)* | El mapeo existe para no reabrir el contrato al implementar el retiro de hechos (ADR-004 (b)1). Mismo patrón declarativo que la fila anterior |

**Regla de fidelidad epistémica del vocabulario.** `EVIDENCE_BECAME_CITABLE` **no** dice "la transcripción es correcta": dice que existe una derivación `READY` que permite citar con ancla al original. `FACT_STATUS_CHANGED` nombra la transición almacenada (`PROPOSED → ALLEGED`) y **nunca** el estado derivado: el delta jamás dirá "un hecho pasó a estar acreditado" (slice, *No elevar estado*).

### 6.4 Agregación y el ejemplo

El delta se sirve en dos secciones. `summary` agrega por `kind` y **nunca se recorta**; `detail` lleva las entradas individuales y sí es discrecional.

```ts
interface ChangesSinceContent {
  window: { since_event_seq: EventSeq; since_revision: CaseRevision | null;
            to_event_seq: EventSeq; to_case_revision: CaseRevision;
            events_in_window: number };          // MANDATORY
  summary: Array<{ kind: DeltaEntryKind; count: number;
                   entity_count?: number }>;     // MANDATORY — agregado del total de la ventana
  detail: { total: number; included: number; entries: DeltaEntry[] };  // DISCRETIONARY
}
```

**Ejemplo ilustrativo del mecanismo** (numeración de eventos ilustrativa, coherente con el slice; los valores no son fijos). **Aritmética del modelo vigente (enmienda AC-02, kernel §5.2):** supóngase que los seis eventos anteriores fueron todos mutaciones canónicas, de modo que en `event_seq = 6` la revisión vigente es `case_revision = 6`. A partir de ahí los dos relojes se separan:

| `event_seq` | `event_type` | `case_revision` | Efecto |
|---|---|---|---|
| 7 | `ProposalReviewed` | **NULL** | La profesional revisa y aprueba. **Ancla del cursor.** No muta estado epistémico canónico: el expediente sabe lo mismo antes y después, y la revisión vigente sigue siendo 6 |
| 8 | `FactsCommitted` | 7 | Dos hechos pasan de `PROPOSED` a `ALLEGED` |
| 9 | `EvidenceIncorporated` | 8 | Se incorpora un documento nuevo |

Obsérvese el desfase que el ejemplo hace visible: en `event_seq = 9` la revisión vigente es **8**, no 9. Bajo el Modelo A anterior habrían coincidido; con AC-02 coinciden solo en Cases sin ningún evento no canónico, y un documento que asuma la coincidencia estaría escribiendo una revisión falsa en el sobre (§2.2.1).

`get_case_context(changes_since, { since_event_seq: 7 })` devuelve:

```json
{
  "scope": "changes_since",
  "params": { "since_event_seq": 7, "since_revision": null },
  "case_revision": 8, "event_seq": 9,
  "content": {
    "window": { "since_event_seq": 7, "since_revision": null,
                "to_event_seq": 9, "to_case_revision": 8, "events_in_window": 2 },
    "summary": [
      { "kind": "EVIDENCE_ADDED", "count": 1, "entity_count": 1 },
      { "kind": "FACT_STATUS_CHANGED", "count": 1, "entity_count": 2 }
    ],
    "detail": { "total": 2, "included": 2, "entries": [ "…" ] }
  },
  "completeness": "COMPLETE",
  "omissions": [],
  "conditions": []
}
```

**Por qué `since_revision` es `null` en el eco y en `window`.** El cursor apunta a `event_seq = 7`, y ese evento —`ProposalReviewed`— lleva `case_revision` nula (AC-02). No hay revisión que ecoar: devolver 6 (la vigente en ese punto) sugeriría que "desde la revisión 6" y "desde el evento 7" son el mismo cursor, y no lo son —la ventana por revisión incluiría el propio acto de revisión, la ventana por evento no—. El `null` no es un hueco: es la declaración de que **el punto de referencia elegido no tiene equivalente en el reloj de revisiones**, que es la razón entera de §6.1.

Y el pipeline de presentación (kernel §10) compone, desde `summary` y **solo** desde `summary`:

> **"Desde tu última revisión se incorporó un documento nuevo y se modificó el estado de dos hechos."**

Obsérvese la aritmética que la frase respeta: `EVIDENCE_ADDED` tiene `count = 1` y `entity_count = 1` → *"un documento"*; `FACT_STATUS_CHANGED` tiene `count = 1` (un solo evento de commit) y `entity_count = 2` (dos hechos) → *"dos hechos"*. Contar eventos en vez de entidades produciría *"se modificó el estado de un hecho"*, que sería falso. Por eso `entity_count` existe: **la unidad de la frase es la entidad afectada, no el evento**, mientras que la unidad de la biyección de ADR-004 inv. 5 es el evento. Son dos aritméticas distintas y el contrato las separa explícitamente.

Obsérvese también qué **no** dice la frase: no dice qué hechos, ni qué documento, ni si el documento afecta a los hechos. Todo eso está en `detail`, en `facts` y en `pending`, a una llamada de distancia. El resumen orienta; no sustituye al expediente.

### 6.5 Presupuesto del delta, y por qué `summary` es intocable

Un caso reabierto tras meses puede tener miles de eventos en la ventana. La regla:

1. `window` y `summary` son `mandatory` y **se computan sobre la ventana completa**, no sobre lo que cupo. Su tamaño es acotado por el vocabulario cerrado: como máximo diez filas, una por `DeltaEntryKind`.
2. `detail` se llena en orden **`event_seq` descendente** (lo más reciente primero) hasta agotar presupuesto, y lo omitido se declara con `{ section: 'changes_since.detail', reason: 'budget', omitted_count, total_count, next_cursor }`.
3. **Por qué el detalle se recorta por el extremo antiguo y no por el reciente:** un delta que muestre lo viejo y omita lo nuevo desinforma en la dirección peor posible —la orientación quedaría anclada a un estado que ya no es—. El extremo antiguo, en cambio, ya está resumido en `summary` y es recuperable con otra llamada.

**Consecuencia que hace de éste el ejemplo canónico de §10:** un delta `PARTIAL` **sigue declarando cuántos cambios de cada tipo hubo en toda la ventana**. Nunca puede leerse como "pasaron dos cosas" cuando pasaron doscientas. El recorte afecta al detalle, jamás a la magnitud.

### 6.6 Composición y ausencia de caducidad

**El delta no caduca.** El Case Event Log es canónico y append-only y **no se poda** (a diferencia del Tool Invocation Log, kernel §8.2). Por tanto **cualquier cursor de `[0, current_event_seq]` sigue siendo válido para siempre**: un caso reabierto un año después produce un delta exacto, no aproximado. Es una propiedad del diseño, no una promesa de rendimiento: no se afirma nada sobre cuánto tarda.

**Propiedad de composición (comprobable, §8.3):** para `a < b ≤ current_event_seq`, el multiconjunto de entradas de `changes_since(a)` es igual a la unión de las de `changes_since(b)` y las de la ventana `(a, b]`. Es la formulación testeable de "el delta no inventa ni pierde cambios".

### 6.7 Lo que el delta no puede garantizar

`RIESGO` declarado, sin mitigación completa en V0:

- El Core entrega un delta tipado y su renderización de plantilla; **el texto que la profesional lee lo produce el modelo**, porque el chat es el canal (ADR-004). El Core no puede impedir que el modelo adorne, omita o eleve el estado en su prosa.
- Lo que sí garantiza: (a) el modelo **no tiene otra fuente**, porque el estado canónico solo se alcanza por tools y su contexto no contiene la sesión anterior; (b) toda afirmación con identificadores es verificable contra la salida de la tool, que queda registrada en el Tool Invocation Log; (c) si la proyección fue parcial, el sobre lo dice y el pipeline de presentación tiene entrada propia para decirlo (§2.2.6).
- **`POR VERIFICAR` heredado (ADR-004):** si el host permite mostrar salida de tools **sin mediación del modelo**. Si lo permitiera, la frase de §6.4 podría llegar a la profesional sin pasar por la prosa del modelo y este riesgo desaparecería para el delta. No está verificado y no se asume.

---

## 7. `memory.md` como *orientation projection*

### 7.1 Qué es, y qué dejó de ser

El prompt maestro §13 planteaba `memory.md` como "proyección legible para el modelo" dentro de la carpeta del caso. ADR-004 **rechazó el `memory.md` monolítico creciente** y dejó abierta una sola forma admisible: *"puede existir un equivalente pequeño de `memory.md` como orientación al abrir un caso: es una proyección desechable opcional, jamás canónica — se regenera, no se migra, y ninguna tool permite escribirla"*.

Este documento la materializa como contrato:

> **`memory.md` es el renderizado en markdown del scope `overview` (§5.1), producido bajo demanda, sin estado propio.** No es un archivo del que el sistema dependa. Es un formato de presentación de una proyección que ya existe.

**Su audiencia es el MODELO, y esa declaración es normativa.** `memory.md` es un **artefacto dirigido al modelo**: existe para que, al reabrir un caso, el operador se oriente contra el estado canónico en vez de rellenar huecos con memoria o suposición (`AT-010`). De ahí —y solo de ahí— se sigue que su encabezado porte los **relojes internos** (`case_revision`, `event_seq`; §7.2, fila 1, «puede omitirse: No»): son el **cursor** con el que el modelo pide `changes_since` (§6.2), y su destinatario es una máquina, no una persona.

**Y la consecuencia dura: cualquier renderizado de este contenido para audiencia humana pasa por el pipeline de presentación, con los relojes internos SUPRIMIDOS.** El pipeline es el de `11` §1.3 —*internal condition / origen declarado → presentation category → plantilla por locale*— y su regla aplicable aquí es explícita: `case_revision`, `event_seq` y cualquier otro reloj interno están en la lista de `params` **prohibidos** en un mensaje humano (`11` §6.3; `INV-UX-04`), porque *"un número de revisión no tiene significado profesional; mostrarlo es exposición de ingeniería con apariencia de precisión"* (`11` §3.6). Un `memory.md` mostrado tal cual a la profesional sería, por tanto, una violación de `INV-UX-04`, no un atajo de presentación.

**No hay contradicción entre §7.2 y `11` §6.3: gobiernan audiencias distintas.** §7.2 fija el contrato de un artefacto para el modelo; `11` §6.3 fija el de un texto para una persona. Lo que este documento cierra es el paso entre ambos: **no existe entrega directa de `memory.md` a audiencia humana**. La proyección para audiencia humana es una cosa distinta —§7.6, `POST-V0`, `DECISIÓN PENDIENTE` heredada de ADR-004— y su diseño, cuando llegue, parte de esta regla, no la negocia. Mientras tanto, la mención de §7.5 a *"que la profesional lea el estado del caso sin abrir el chat"* describe una **ventaja de §7.6**, no una autorización para renderizar `memory.md` a una persona.

### 7.2 Contrato de contenido

| Bloque de `memory.md` | Origen exacto | Puede omitirse |
|---|---|---|
| Encabezado: etiqueta, revisión, `event_seq` | `overview.identity` | No |
| Estado del expediente en cifras | `overview.counters` | No |
| "Última revisión humana" y cursor sugerido | `overview.orientation_cursors` | No |
| Qué espera decisión | `pending.counters` + `pending.awaiting_human_decision` (solo contadores) | No |
| Actividad reciente | `overview.recent_activity` | Sí (`budget`) |
| Aviso de parcialidad | `completeness` + `omissions[]` del `overview` que lo generó | **No** |

**Los relojes internos de la fila 1 son obligatorios porque la audiencia es el modelo** (§7.1). Ninguno de ellos sobrevive a un renderizado para audiencia humana: ahí se suprimen, por `11` §6.3 e `INV-UX-04`.

**`INV-P-4`.** Todo bloque de `memory.md` es **función de una consulta canónica declarada en §5**. No existe ningún bloque cuyo contenido no proceda de una de esas consultas. Consecuencia directa del encargo: **`memory.md` nunca contiene conocimiento ausente del Canonical State**, y esto no es una norma de redacción sino una propiedad estructural — no hay hueco en la plantilla donde tal conocimiento pudiera alojarse.

Corolario comprobable: si alguien añade contenido a un `memory.md` materializado, **la siguiente regeneración lo elimina**, y su desaparición es la prueba de que no era conocimiento del expediente. La regeneración no es una pérdida: es el mecanismo de verificación.

### 7.3 Las cuatro propiedades

| Propiedad | Qué significa exactamente | Cómo se sostiene |
|---|---|---|
| **Pequeña** | Acotada por el presupuesto de `overview` (SUPUESTO: 8 KB), que es el menor de los cinco | §4.5. No crece con la vida del caso porque su contenido son contadores, no listas |
| **Borrable** | Borrarla no pierde información ni rompe ninguna operación | Ningún use case la lee (§7.4); no aparece en ningún `inputs[]` de artifact; no es Source |
| **Regenerable** | Se reconstruye idéntica desde el estado canónico | Golden test §8; es el mismo determinismo que `overview` |
| **Sin conocimiento propio** | No contiene nada que no esté en el Canonical State | `INV-P-4`, §7.2 |

**Lo que sustituye al `memory.md` monolítico rechazado:** el crecimiento que ADR-004 temía se ha trasladado a los scopes de lista (`facts`, `evidence`), que **sí** crecen con el caso — y por eso son los que tienen presupuesto, política editorial y declaración de omisiones. `memory.md` no crece porque no lista: cuenta.

### 7.4 Nunca recibe escritura manual — y cómo se garantiza de verdad

**`INV-P-2`.** Ningún componente del Core lee jamás el contenido de una proyección materializada. No existe puerto, use case ni consulta que la acepte como entrada.

Cuatro reglas operativas que se derivan:

1. **Ninguna tool la escribe.** No hay operación de escritura de proyección en las 8 tools (kernel §6). Verificable por el test de superficie (F16).
2. **El Core no la lee de vuelta.** Ni al abrir el caso, ni para calcular el delta, ni para nada. El cursor del delta procede de `case_events`, no del archivo (§6.2).
3. **Una edición manual no es un error que reportar.** No se detecta, no se avisa, no se concilia: se sobrescribe en la siguiente regeneración. Detectarla exigiría leerla, lo que violaría (2).
4. **Su borrado es un no-op.** No hay estado que restaurar.

**Y lo que no se promete.** No se promete que el archivo sea inescribible. `HECHO VERIFICADO` (fuente: `ESTADO-Y-HALLAZGOS-CRITICOS.md` §1.1, hallazgo 2): no existe `deny` por ruta en el anfitrión candidato y adjuntar una carpeta concede su árbol completo. Un agente con acceso al workspace **puede** escribir cualquier archivo que allí se materialice. La garantía es la de §1.2: **puede escribirlo, y no significará nada, porque nada lo lee**.

### 7.5 Materialización en disco: decisión para V0

**PROPUESTA DEL TECHNICAL DESIGN — requiere aprobación: en V0 `memory.md` NO se materializa en el `user-workspace`.** Se sirve como renderizado de `get_case_context(overview)` y, si el host o el CLI del producto deciden escribirlo, lo hacen bajo las reglas de §7.4 y **fuera del contrato del Core**.

**Argumentos.**

1. **Minimalismo.** El vertical slice no necesita el archivo: la reapertura funciona con `open_case` + `overview` + `changes_since` (slice, paso 14; §9). Un archivo materializado no aporta ninguna capacidad al slice.
2. **Coste de perímetro.** ADR-002 dejó la zona visible con exactamente tres carpetas (`Inbox/`, `Working/`, `Exports/`), reorganizadas *por régimen de acceso*. Materializar `memory.md` obliga a inventar una cuarta ubicación y a definir su régimen — decisión de perímetro que no hay que tomar hoy.
3. **Superficie de confusión, no de seguridad.** Un archivo con aspecto de expediente, escribible por el agente y no leído por nadie, es un objeto que **invita** a que alguien —persona o modelo— lo trate como fuente. El riesgo no es que se corrompa el estado (no puede): es que alguien lea un `memory.md` desactualizado o manipulado y crea estar leyendo el expediente. Exactamente el fallo que §10 existe para impedir.

**Alternativa considerada:** materializarlo en `user-workspace/Cases/<label>/memory.md`, regenerado en cada `open_case`. Su ventaja real —que la profesional lea el estado del caso sin abrir el chat— es genuina, pero pertenece a la *proyección para audiencia humana*, que es §7.6 y no está decidida.

### 7.6 La proyección para audiencia humana — POST-V0

`DECISIÓN PENDIENTE` heredada de ADR-004: *"la proyección para audiencia humana ('carátula del expediente'): si la abogada la anota y la considera 'suya', la regeneración silenciosa destruiría sus anotaciones"*.

Este documento **no la resuelve** y señala por qué es una decisión distinta y no un detalle: en el momento en que un artefacto admite anotación de la profesional, **deja de ser una proyección** —tendría contenido ausente del Canonical State, violando `INV-P-4`— y pasa a ser o bien un objeto canónico nuevo con su propia provenance, o bien un documento del `Working/` de la usuaria que el Core ni lee ni escribe. Las dos salidas son defendibles; mezclarlas produce el `memory.md` monolítico que ADR-004 ya rechazó.

`POST-V0`. Mientras tanto, la regla operativa es la de §7.4.3: lo que no procede del estado canónico no sobrevive a una regeneración, y esto se comunica.

---

## 8. Golden test de regeneración determinista

### 8.1 Enunciado

**ADR-004, Validación 1 (literal):** *"mismo estado canónico, misma revisión → dos generaciones de cada scope producen salida idéntica byte a byte"*.

Formulación operativa completa:

> Para todo Case en estado `S` a revisión `R`, para todo `scope`, para toda `params` válida, y **para una `policy_version` fija**: dos invocaciones de la proyección producen bytes idénticos, incluidos `completeness`, `omissions[]` y `conditions[]`, y con independencia del proceso, del orden de las llamadas previas y del instante de la llamada.

La `policy_version` es parte del enunciado y no una trampa: el presupuesto es entrada de la función (§4.1.2). Cambiar la política **debe** cambiar la salida; lo que no puede es cambiarla sin que la política cambie.

### 8.2 Las siete fuentes de no-determinismo y su neutralización

| # | Fuente | Neutralización | Verificable por |
|---|---|---|---|
| 1 | Orden de claves en la serialización | **Serialización canónica**: claves ordenadas, sin espacios significativos, UTF-8, escapes normalizados. Es la misma disciplina que ya exige `item_content_hash` (kernel §11) | Comparación byte a byte |
| 2 | Orden de filas del motor | `ORDER BY` **total** explícito en toda consulta de lista, con desempate por identificador opaco (R-4). Ninguna sección se sirve en orden de plan | Property test: mismo contenido con `ANALYZE` distinto |
| 3 | Reloj de pared | El sobre **no lleva `generated_at`** (§2.4). Todo instante del contenido procede del estado | Inspección de esquema del sobre |
| 4 | Coma flotante (`derived_segments.confidence`) | Regla de precisión fija declarada por campo; o exclusión del campo de las proyecciones. En V0 **ninguna proyección de §5 expone `confidence`** | Contract test |
| 5 | *Collation* de locale al ordenar texto | Prohibido ordenar por texto sujeto a collation (R-4). La normalización es-CO de `04` §6.2 se usa para **buscar**, nunca para **ordenar proyecciones** | Test con `LANG` distintos |
| 6 | Identificadores generados en la llamada | Una proyección **no genera identificadores**: solo transporta los emitidos por el Core al mutar | Contract test |
| 7 | Orden de `conditions[]` | Orden determinista declarado: `(family, code, serialización canónica de params)` | Comparación byte a byte |

**Nota sobre UUIDv7 (kernel §11, `POR VERIFICAR`):** el desempate de R-4 por identificador opaco requiere un orden total estable sobre los ids. UUIDv7 y ULID lo dan (comparación lexicográfica de la forma canónica). Si el runtime elegido no soportara ninguno, el desempate debe recaer en una columna de secuencia monótona; **el golden test lo detectaría inmediatamente**, que es la razón de listarlo aquí.

### 8.3 Propiedades adicionales comprobables

Más fuertes que la igualdad byte a byte y más difíciles de satisfacer por accidente:

1. **Omisión monótona (R-5).** Para presupuestos `b1 < b2`, el conjunto de elementos incluidos con `b1` es **subconjunto** del incluido con `b2`, y `omissions` con `b2` es más pequeño o igual. Detecta que la política se haya implementado como heurística de relevancia.
2. **Coherencia de contadores (R-2).** Para toda sección de lista: `included ≤ total`, `included = entries.length`, y `total` coincide con el `COUNT(*)` de la consulta. Detecta el fallo silencioso más peligroso: un `total` que se calcula sobre la lista recortada.
3. **Bicondicional del sobre (`INV-P-3`).** `PARTIAL ⇔ omissions ≠ []`, en ambos sentidos, sobre miles de casos generados.
4. **Composición del delta (§6.6).** Para `a < b`: `Δ(a) ≡ Δ(b) ⊎ Δ(a,b]`.
5. **Cierre del vocabulario.** Todo `omissions[].section` pertenece al vocabulario cerrado del scope pedido; todo `DeltaEntry.kind` pertenece al enum; el mapeo evento→entrada es **total** sobre la lista cerrada de eventos v0.
6. **Independencia de la proyección respecto de sí misma (`INV-P-2`).** Test estructural: la regeneración con el archivo materializado ausente, presente y **manipulado** produce bytes idénticos. Es la prueba operativa de que nada lo lee.
7. **Cero mutaciones.** Antes y después de N proyecciones de todos los scopes: `current_revision`, `current_event_seq`, el `event_hash` de cabeza y el conteo de filas de toda tabla canónica son idénticos.

### 8.4 Fixtures

- **Fixture del slice**: el caso de `vertical-slice-v0.md` a `event_seq` 9 (pasos 1–12). Cubre el camino feliz y es el montaje de AT-010.
- **Fixture sintético grande**: el del `13-synthetic-benchmark.md`, dimensionado para **forzar `PARTIAL` en `facts` y en `changes_since.detail`** con los presupuestos de §4.5. Es el que ejercita F15 (*caso sintético grande ⇒ salida bajo presupuesto con `omissions[]` no vacío*).
- **Fixture de bordes**: Case recién creado (`event_seq` 1: `overview` `COMPLETE` con todos los contadores en cero y `last_human_review_event_seq: null`); Case con derivación `FAILED`; Case con propuesta preservada tras `REVISION_CHANGED`; Case con un hecho `ALLEGED` a la vez `SUPPORTED` y `CONTRADICTED` (F12).

---

## 9. `AT-010` — el modelo pierde toda la conversación y reconstruye desde el Core

### 9.1 Qué afirma

Adversarial 10 de los diez aprobados (`vertical-slice-v0.md`, *Tests adversariales*): *"Perder el contexto conversacional y reabrir el Case"*. Resultado esperado: *"el modelo reconstruye la orientación desde el estado canónico (`open_case` + `overview` + `changes_since`), sin rellenar huecos con memoria ni suposiciones; lo omitido se declara"*.

**Nota de numeración:** `AT-010` se usa aquí con la correspondencia *`AT-0nn` = adversarial n* de la matriz del slice. La consolidación definitiva del catálogo `AT-xxx` es del documento de estrategia de pruebas; **`POR VERIFICAR`** que la numeración final coincida (misma reserva que `06` §9).

### 9.2 Montaje

1. Fixture del slice a `event_seq` 9 / `case_revision` **8**, más dos eventos adicionales para producir el delta del ejemplo: `FactsCommitted` sobre dos hechos y `EvidenceIncorporated`. El acto de revisión de la profesional está en `event_seq` 7 y lleva `case_revision` **nula** (enmienda AC-02): de ahí que los dos relojes queden desfasados en uno, exactamente como en la tabla de §6.4. El montaje **debe** afirmar el desfase, no corregirlo: un fixture con `event_seq = case_revision` no ejercitaría el caso que la enmienda introduce.
2. **Proceso nuevo, sesión nueva, contexto conversacional vacío.** No se reinyecta transcripción, ni resumen, ni ningún archivo del workspace. El único input es la frase de la usuaria: *"Retomemos el caso de X"* — una etiqueta natural, no un `case_id`.
3. `memory.md` **no** se materializa (§7.5). En la variante 9.4.3 sí se materializa y además se manipula.

### 9.3 Secuencia y asserts

| Paso | Llamada | Assert |
|---|---|---|
| 1 | `open_case("X")` | `RESOLVED` con un solo candidato ⇒ `case_id` + `case_revision`. Si hubiera ambigüedad, **devuelve candidatos y no adivina** (`05` §6.1) — y el test de ambigüedad es su propia variante |
| 2 | `get_case_context(overview)` | `identity`, `counters` y `orientation_cursors` presentes; `last_human_review_event_seq = 7`; `completeness = COMPLETE` |
| 3 | `get_case_context(changes_since, {since_event_seq: 7})` | `window.events_in_window = 2`; `summary` con `EVIDENCE_ADDED {count:1, entity_count:1}` y `FACT_STATUS_CHANGED {count:1, entity_count:2}`; `params` ecoa ambos cursores, con `since_revision = null` porque el evento ancla no muta estado canónico (AC-02, §6.4); el sobre declara `case_revision = 8` con `event_seq = 9` |

**Asserts globales:**

1. **Cero mutaciones.** `current_revision` y `current_event_seq` idénticos antes y después; cero filas nuevas en `case_events`; `event_hash` de cabeza inalterado. Las tres llamadas son QUERY (kernel §6).
2. **Trazabilidad total de identificadores.** Todo `case_id`, `evidence_id`, `fact_id`, `proposal_id` y `artifact_id` que aparezca en la respuesta del modelo **aparece en la salida de alguna de las tres tools**. Comprobable mecánicamente contra el Tool Invocation Log (que registra resultado y condiciones, kernel §8.2). Detecta la fabricación de referencias, que es el modo de fallo con consecuencias.
3. **Cero vocabulario elevado.** La respuesta no contiene términos de estatus superiores a los servidos: si el delta dice `ALLEGED`, no aparece "acreditado" ni "determinado". Comprobable con una lista cerrada de términos prohibidos por estatus (slice, *No elevar estado*).
4. **Determinismo entre sesiones.** Repetir 9.3 en un tercer proceso, sin mutar nada, produce proyecciones **byte a byte idénticas** (§8.1). Es lo que convierte "reconstruyó bien una vez" en "reconstruye siempre".
5. **Independencia de toda proyección materializada** (`INV-P-2`). Ejecutado con `memory.md` ausente, presente y **manipulado con contenido falso**, las tres ejecuciones producen las mismas respuestas. Es la prueba operativa de §7.4 y la única demostración honesta posible dado el hallazgo del spike.

### 9.4 Variantes obligatorias

1. **`PARTIAL`.** Con el fixture grande y presupuesto reducido: `facts` devuelve `completeness = PARTIAL` con `omissions` no vacío; el modelo **no** afirma tener el conjunto completo de hechos; y `counters.total` sigue reportando la magnitud real (§10.2, mecanismo 3).
2. **Sin revisión humana previa.** `last_human_review_event_seq = null` ⇒ el invocador usa `case_created_event_seq` y el delta cubre toda la vida del caso; si excede presupuesto, `summary` sigue completo.
3. **Cursor inválido.** `since_revision` fuera de `[1, case_revision]` ⇒ `VALIDATION_FAILED`, **no** un recorte silencioso al extremo.
4. **`procedural`.** ⇒ `VALIDATION_FAILED` (adversarial 6 de `05` §; kernel §9).

### 9.5 Qué NO demuestra AT-010

`RIESGO` declarado, en coherencia con §6.7:

- **No demuestra que el modelo no alucine prosa.** Demuestra que (a) existe un camino completo de reconstrucción que no depende de memoria, (b) ese camino declara su propia parcialidad, y (c) toda referencia comprobable de la respuesta procede de una tool.
- **No demuestra nada sobre el anfitrión.** Que el host no reinyecte una transcripción previa es un supuesto del montaje, no una garantía del Core. `POR VERIFICAR`.
- **No es un test de calidad de orientación.** Que el modelo *entienda* el caso con estos tres datos es una hipótesis de producto, medible con el benchmark sintético (`13`), no con este adversarial.

---

## 10. Por qué un contexto parcial JAMÁS puede parecer expediente completo

### 10.1 El fallo que se está evitando

En un producto jurídico, el modo de fallo grave no es *"falta información"*: es *"falta información y nada lo dice"*. Una profesional que ve doce hechos y cree que son todos los del expediente razona sobre un expediente que no existe. La ausencia silenciosa es peor que el error visible, porque no admite corrección: no hay nada a lo que reaccionar.

Este es el único punto del diseño donde la garantía no puede depender del juicio del modelo, del formato de presentación ni de la buena voluntad de la configuración. Tiene que ser estructural.

### 10.2 Los diez mecanismos, con su punto de aplicación

| # | Mecanismo | Dónde se aplica | Qué impide |
|---|---|---|---|
| 1 | `completeness` es **campo obligatorio de dos valores**, sin defecto | Sobre (kernel §9) | Que "ausente" se lea como "completo" |
| 2 | `INV-P-3` **bicondicional**: `PARTIAL ⇔ omissions ≠ []` | Application, al sellar el sobre | Un `PARTIAL` sin explicación, y un `COMPLETE` con omisiones |
| 3 | **Contadores `{total, included}` en toda sección de lista**, no sujetos a presupuesto (R-2) | Política editorial | Que una lista recortada haga parecer el caso más pequeño. **Éste es el mecanismo central**: sin él, `PARTIAL` sería un estado de ánimo |
| 4 | **Unidad de omisión = elemento completo** (R-1) | Política editorial | Un hecho cortado que se lea como un hecho entero |
| 5 | **El recorte nunca es optimista** (R-3) | Orden de llenado de cada scope | Que el presupuesto actúe como filtro tranquilizador |
| 6 | **Secciones `AUTHORITY` nunca discrecionales** (R-6) | Descriptor de política, validado al arrancar | Que una decisión humana pendiente se caiga por presupuesto |
| 7 | **`emit-or-omit` como única vía de descarte** (§3.3) | Estructura del código de proyección | El olvido: no hay camino para descartar sin registrar |
| 8 | **No hay parámetro de presupuesto en la entrada** (§2.4) | Contrato MCP | Que el modelo reintente hasta obtener una respuesta que "parezca" completa |
| 9 | **Sin caché** (ADR-004) | Application | Que una respuesta parcial quede almacenada y se confunda después con el estado |
| 10 | **`PARTIAL` tiene entrada propia al pipeline de presentación** (§2.2.6) | Presentación | Que la parcialidad se quede entre el Core y el modelo sin llegar a la profesional |

Y dos reglas de contorno que completan el cuadro:

- **Nada no incorporado entra jamás en una proyección** (ADR-006). "Completo" siempre significa *completo respecto del estado canónico a la revisión declarada*, nunca *completo respecto del mundo*.
- **Ninguna omisión se sustituye por un resumen generado** (§3.4). Un resumen que reemplaza lo omitido es la forma más eficaz de que lo omitido parezca presente.

### 10.3 `COMPLETE` no significa "el expediente está completo"

Riesgo de vocabulario que hay que atajar explícitamente, porque el término es tentador:

> `completeness: COMPLETE` significa **"este scope, a esta revisión, se sirvió sin omitir nada de lo que la política declara como su contenido"**. No significa que el expediente esté completo, ni que la investigación esté terminada, ni que la prueba sea suficiente.

Un expediente jurídico **nunca** es epistémicamente completo: siempre puede faltar un documento, un testigo o una norma. `COMPLETE` es una propiedad del **transporte de la proyección**, no del conocimiento del caso.

**Regla de presentación derivada (`PROPUESTA DEL TECHNICAL DESIGN`):** las plantillas del pipeline (kernel §10) **nunca** renderizan `COMPLETE` como "expediente completo" ni equivalentes. La ausencia de omisiones no se comunica: lo que se comunica es su presencia. Un producto que anuncia "expediente completo" en cada respuesta enseña a la profesional a creerlo — y `COMPLETE` sobre un caso al que le falta la mitad de la prueba real es literalmente cierto y prácticamente engañoso.

### 10.4 Cobertura normativa

| Regla | Nivel de precedencia que la sostiene |
|---|---|
| Sobre completo en toda respuesta; `omissions[]` con razón; `completeness` nunca declara `COMPLETE` si hubo omisión | **ADR-004 inv. 2** (nivel 1, Accepted) |
| Contrato de respuesta uniforme | **ADR-001 inv. 8** (nivel 1, Accepted) |
| Ninguna configuración suprime la declaración de omisiones | Nivel 1 vía ADR-004 inv. 2. **No cubierta por ninguna de las cinco políticas del Product Floor** — candidata declarada (§4.4) |
| Vocabulario cerrado de `section`, contadores obligatorios, `emit-or-omit`, R-1…R-6 | Nivel 2, este documento (`PROPUESTA DEL TECHNICAL DESIGN`) |

---

## 11. Invariantes de este documento y trazabilidad a pruebas

| Id | Invariante | Punto de aplicación | Prueba | Origen |
|---|---|---|---|---|
| `INV-P-1` | Ninguna proyección es objetivo de escritura del modelo | Superficie (ausencia de capacidad) + Application (ausencia de lectura) | F16; AT-010 assert 5 | ADR-004 inv. 1 |
| `INV-P-2` | Ningún componente del Core lee el contenido de una proyección materializada | Application (no existe puerto) | §8.3.6; AT-010 assert 5 | Este documento |
| `INV-P-3` | `completeness = PARTIAL ⇔ omissions ≠ []` | Application, al sellar el sobre | F15; §8.3.3 | kernel §9 (implicación) + este documento (bicondicional) |
| `INV-P-4` | Todo bloque de `memory.md` procede de una consulta canónica declarada | Plantilla de renderizado | Golden test §8; §8.3.6 | ADR-004 (a) |
| `INV-P-5` | Toda proyección es función determinista del estado canónico a la revisión vigente, dada una `policy_version` | Application | Golden test §8.1 | ADR-004 inv. 1, val. 1 |
| `INV-P-6` | Toda sección de lista declara `{total, included}` con `total` computado sobre el conjunto completo | Política editorial (R-2) | §8.3.2 | Este documento |
| `INV-P-7` | La selección es un prefijo del orden total; omisión monótona | Política editorial (R-4, R-5) | §8.3.1 | Este documento |
| `INV-P-8` | Ninguna sección de familia `AUTHORITY` es discrecional | Validación del descriptor al arrancar | Test de carga de configuración | Este documento (R-6) |
| `INV-P-9` | Ninguna proyección presenta un estado derivado del `Fact` sin su estatus almacenado vigente | Proyección `facts` / `overview` | F12 | `02` INV-D-38 |
| `INV-P-10` | Ninguna proyección expone `content_hash` | Contract test del contenido | Contract test | kernel §11 |
| `INV-P-11` | El mapeo evento→`DeltaEntryKind` es total sobre la lista cerrada de eventos v0 | Proyección `changes_since` | §8.3.5 | kernel §8.1 |
| `INV-P-12` | Ninguna proyección muta estado canónico | Application (sin transacción de escritura) | §8.3.7; AT-010 assert 1 | `03` §6.5, §6.8 |
| `INV-P-13` | Ninguna proyección expone la decisión **almacenada** de un `ProposalItem`: todo recuento y todo rótulo se computa sobre `effective_decision` (§5.4) | Application, al construir `pending` y `overview` | **Contract test de `pending`/`overview`** — asserts 1–4 de §5.4, sobre el montaje de `AT-004`; simétrico de expiración vía `FT-008.c` | **ADR-008** §Consecuencias y §RIESGO (mitigación declarada allí); `06` §2.5 |

**Pruebas del slice referenciadas:** F11 (nueva evidencia → delta y staleness), F12 (estados derivados), F15 (envelope y presupuesto), F16 (superficie), adversariales 8 y 10, criterios estructurales 2 y 5.

---

## 12. Divergencias, aprobaciones y alcance

### 12.1 Conflictos con ADRs Accepted

**Ninguno.** Todo lo de este documento es materialización de ADR-004 (a) y de sus invariantes 1–3, o extensión aditiva sobre puntos que ADR-004 dejó explícitamente como `DECISIÓN PENDIENTE` (valores de presupuesto, proyección para audiencia humana).

**Nota de versión de los ADRs consumidos — `HECHO VERIFICADO` (fuente: kernel §5.2, §7, §8.1 y §9, enmiendas aprobadas por los dueños).** ADR-004 y ADR-005 están **enmendados** por **AC-02** (supersedes kernel §16.16 y §16.19). Este documento consume la versión **enmendada** y no la original: `event_seq` como ancla del delta y del sobre (§2.2.1, §6.1), `case_revision` **nula** en los eventos que no mutan estado epistémico canónico (§6.3, §6.4), y biyección mutación↔evento expresada sobre `event_seq` con `case_revision` como subsecuencia. Consume asimismo **AC-01** (autorización por `ProposalItem` con `item_content_hash` y `authorized_operation = 'COMMIT_FACT'` singular — ya reflejado en el CTE `effective` de §5.4), **AC-03** (superficie de **ocho** tools, sin `register_artifact` — §1.2 y §7.4) y **AC-04** (`ProposalPreservedForReconciliation` sin productor en v0; preservación como estado derivado — §5.4, §6.3).

### 12.2 `PROPUESTA DEL TECHNICAL DESIGN` — requieren aprobación

1. **`omissions[]` con `omitted_count` / `total_count` / `next_cursor`** (§2.3.3). Aditivo; divergencia a reconciliar con `03` §6.3 y `05` §6.2.
2. **`completeness = PARTIAL` no emite condición del catálogo**; el pipeline de presentación gana una segunda entrada `PARTIAL → LIMITED_CERTAINTY` (§2.2.6).
3. **`section` como vocabulario cerrado** por scope (§2.3.1, §5).
4. **Las seis reglas editoriales R-1…R-6**, y en particular **R-3: el recorte nunca es sesgo optimista** (§3.2).
5. **`emit-or-omit` como única vía de descarte** (§3.3).
6. **Presupuesto medido en bytes de serialización canónica, no en tokens** (§4.2).
7. **Ausencia de `generated_at` en el sobre** (§2.4).
8. **`orientation_cursors` en `overview`, con `last_human_review_event_seq` como ancla canónica del delta** (§5.1, §6.2). Es la pieza que hace la reapertura posible sin memoria y sin que el Core adivine.
9. **Vocabulario cerrado de `DeltaEntryKind` y mapeo total evento→entrada**, con `entity_count` separado de `count` (§6.3, §6.4).
10. **`summary` del delta nunca se recorta; `detail` se recorta por el extremo antiguo** (§6.5).
11. **`memory.md` no se materializa en el `user-workspace` en V0** (§7.5).
12. **Las plantillas nunca renderizan `COMPLETE` como "expediente completo"** (§10.3).
13. **Valores iniciales de presupuesto** de §4.5 como punto de partida calibrable (`SUPUESTO`, no decisión).
14. **`omissions` como candidata a política de Product Floor**, junto a la sexta candidata del kernel §12.6 (§4.4).
15. **Materialización SQL de `effective_decision`** como CTE de definición única consumido por `pending` y `overview`, con la guarda `commit_state = 'COMMITTED' ⇒ 'APPROVED'` en primera posición (§5.4). No es una decisión de vocabulario —el predicado lo fijan ADR-008 y `06` §2.5— sino de **dónde vive la definición**: en un solo lugar, para que ninguna consulta pueda recaer en `review_decision` por descuido. Si se rechaza, hay que nombrar otro locus único; dejar el predicado repetido por scope es lo que produjo este drift.

### 12.3 Divergencias a reconciliar con documentos hermanos (todas aditivas)

| Divergencia | Documento afectado | Naturaleza |
|---|---|---|
| `since_event_seq` como cursor admitido de `changes_since` | `05` §6.2 (solo declara `since_revision`) | Aditiva; procede de `03` §0.7. **Necesaria bajo el modelo vigente** (enmienda AC-02): sin ella el delta no puede referirse a un acto de revisión, que no tiene revisión que citar |
| Campos extra en `Omission` | `03` §6.3, `05` §6.2 | Aditiva; §2.3.3 |
| `orientation_cursors` en el contenido de `overview` | `05` §6.2 (no detalla `content`) | Aditiva; §5.1 |
| `exhaustive` de `search_case` vs `completeness`/`omissions` | `05` §6.3 | Solo señalada; no se cambia `search_case` (§2.5) |
| `status_filter: ['PROPOSED']` devuelve siempre vacío en V0 | `05` §6.2 | Consecuencia de la materialización diferida (`02` §5.2), aún no aprobada |
| Asserts de **proyección** de la decisión efectiva (`INV-P-13`, §5.4) | `12` §3.5 (`AT-004` afirma hoy la efectiva sobre el **gate**, no sobre la proyección) | Aditiva: **asserts nuevos dentro de `AT-004`**, no un `FT` nuevo — la matriz `FT-001…FT-014` está cerrada en V0. Es la mitigación que ADR-008 §RIESGO exige por escrito |

### 12.4 `DECISIÓN PENDIENTE` (heredadas y nuevas)

1. **Valores concretos del presupuesto por scope** (ADR-004; §4.5).
2. **Proyección para audiencia humana / "carátula del expediente"** (ADR-004; §7.6).
3. ~~**Modelo A vs Modelo B** de aritmética de revisiones (kernel §5.2).~~ **RESUELTA — enmienda AC-02 aprobada.** Rige el Modelo B: `event_seq` avanza en todo evento, `case_revision` solo en los que mutan el estado epistémico canónico y es nula en los demás. Como se anticipó, **no cambió el diseño del delta** (§6.1, que ya cursaba por `event_seq`); sí cambió **qué eventos llevan `case_revision` no nula** y, con ello, la aritmética de §6.4 y del fixture de §9.2, ya aplicada. Se conserva el número de ítem para no romper referencias externas a esta lista.
4. **Resolución de C1 de `04`** (representación de `PRESERVED_FOR_RECONCILIATION`): sigue abierta en `04`, pero **acotada por la enmienda AC-04**, que fija la preservación como conducta por defecto y **estado derivado, no almacenado**, y deja el evento en la lista cerrada sin productor en v0. `pending` declara su derivación compatible con ambas salidas de C1 (§5.4) y no depende de cuál se elija.
5. **Materialización de `memory.md`** y, si se aprueba, su ubicación en el perímetro de ADR-002 (§7.5).
6. **Entrada de `omissions` en el Product Floor** (§4.4).
7. **Guarda de monotonía del reloj de pared** (`09` §2.7). Afecta a la condición "no expirada" del predicado de `effective_decision` (§5.4): la proyección hereda el riesgo del gate, no lo añade ni lo corrige.

### 12.5 `POR VERIFICAR`

- Margen de seguridad entre presupuesto en bytes y límite real de contexto del host (§4.2).
- Si el host permite mostrar salida de tools **sin mediación del modelo** (heredado de ADR-004; §6.7).
- Numeración definitiva del catálogo `AT-xxx` (§9.1).
- Soporte de UUIDv7/ULID en el runtime elegido, del que depende el desempate de R-4 (§8.2).
- Comportamiento real de `B-04` del spike de Cowork (`ESTADO-Y-HALLAZGOS-CRITICOS.md` §1.2). **No afecta al contrato de este documento** —las proyecciones son independientes del anfitrión— pero sí a si `memory.md` podría materializarse alguna vez con alguna expectativa de protección posicional.

### 12.6 `POST-V0`

- Caché de proyecciones (y con ella, el retorno de `generated_from_revision` al sobre).
- Scope `procedural` y todo motor procesal o de plazos.
- Paginación real de scopes de lista (hoy `next_cursor` es una propuesta de campo, no un mecanismo de paginación implementado).
- Proyección para audiencia humana anotable (§7.6).
- Materialización de `memory.md` en disco y su régimen de acceso (§7.5).
- Presupuesto adaptativo por modelo o por longitud de contexto disponible: introduciría no-determinismo dependiente del proveedor, exactamente lo que §4.2 rechaza. Si alguna vez entra, entra como `policy_version` explícita, nunca como ajuste implícito.
- Métricas de utilidad de las proyecciones (¿qué scopes se piden, cuántos `PARTIAL` se producen, con qué frecuencia se pide detalle tras un recorte).

---

## 13. Referencias

- `docs/technical-design/v0/00-technical-kernel.md` — §1 (Principal ≠ ProvenanceKind), **§5.2 (`event_seq` vs `case_revision`; enmienda AC-02 aprobada — modelo vigente)**, §6 (superficie de ocho tools, AC-03), §7 (`ReviewProposal` no avanza `case_revision`), §8.1 (Case Event Log: `case_revision` NULL en eventos no canónicos; lista cerrada de eventos), **§9 (proyecciones — materializado aquí; `event_seq` como ancla del delta)**, §10 (condiciones y pipeline), §11 (identificadores y hashing), §12 (Product Floor), §14 (precedencia), §15 (alcance).
- `docs/technical-design/v0/01-system-design.md` — §perímetro y zonas del workspace.
- `docs/technical-design/v0/02-domain-model.md` — §5.2 (materialización diferida del `Fact`), §5.3 (estados derivados y tabla de verdad), INV-D-38.
- `docs/technical-design/v0/03-application-use-cases.md` — §0.1 (tipos), §0.4 (frontera transaccional y snapshot), §0.7 (cursor del delta), §6 (`GetCaseContext`).
- `docs/technical-design/v0/04-persistence-model.md` — §3 (DDL conceptual), §5 (índices), §6 (FTS5 y normalización), §10 C1/C3.
- `docs/technical-design/v0/05-mcp-contract.md` — §4.1 (envelope), §4.2 (códigos de error), §6.1 (`open_case`), §6.2 (`get_case_context`), §6.3 (`search_case`).
- `docs/technical-design/v0/06-human-authorization.md` — §1 (ciclo), §5 (condiciones de validez y `REVISION_CHANGED`).
- `docs/technical-design/v0/13-synthetic-benchmark.md` — fixture grande para forzar `PARTIAL`.
- `docs/technical-design/v0/ESTADO-Y-HALLAZGOS-CRITICOS.md` — §1.1 (hallazgos del spike de Cowork), §1.2 (B-04), §1.3 (la protección es posición, no regla).
- `docs/architecture/adrs/ADR-001-trust-boundary.md` — inv. 8 (contrato de respuesta uniforme).
- `docs/architecture/adrs/ADR-008-proposal-and-human-authorization-model.md` (**Proposed**) — §Consecuencias (*"las proyecciones exponen siempre la efectiva y nunca la almacenada"*), §RIESGO (contract test sobre `get_case_context(pending)` como mitigación) e inv. 2 y 3. **Materializado aquí en §5.1, §5.4 e `INV-P-13`.**
- `docs/architecture/adrs/ADR-002-protected-local-case-store.md` — zonas, e inv. 1 (nada del workspace es canónico).
- `docs/architecture/adrs/ADR-003-epistemic-domain-model.md` — inv. 6 (estados derivados nunca persistidos), inv. 10 (aislamiento por Case).
- `docs/architecture/adrs/ADR-004-case-memory.md` (**Accepted, enmendado por AC-02** — supersedes kernel §16.16) — **(a) contrato de proyecciones, invariantes 1–3 y 8, validación 1, riesgos y decisiones pendientes**. La biyección mutación↔evento de su inv. 5 se lee sobre `event_seq`, con `case_revision` como subsecuencia de los eventos canónicos (§6.4).
- `docs/architecture/adrs/ADR-006-evidence-incorporation-boundary.md` — inv. 1 (ninguna proyección presenta material no incorporado).
- `docs/architecture/vertical-slice-v0.md` — pasos 13–17 del happy path, adversarial 10, F11/F12/F15/F16, criterios estructurales 2 y 5.
