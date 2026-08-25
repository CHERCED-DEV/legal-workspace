# Spike de dependencias y runtime — V0

**Documento:** `docs/research/runtime-dependencies-spike-v0.md`
**Nivel de precedencia:** 6 (Discovery / research / spikes), según kernel técnico v0.4 §14.
**Naturaleza:** este documento contiene **observaciones**, no garantías de plataforma. Ningún resultado aquí puede redefinir una regla fijada en un ADR Accepted o en el Technical Design.
**Fecha de verificación de las fuentes:** 2026-08-24.
**Alimenta:** kernel técnico v0.4 §11 (identificadores) y §13 (stack), y las decisiones de dependencia pendientes de aprobación de los dueños.

---

## 0. Cómo leer este documento

### 0.1 Etiquetas usadas

| Etiqueta | Significado |
|---|---|
| **HECHO VERIFICADO** | Afirmación leída directamente en documentación oficial primaria, con URL. |
| **DECISIÓN APROBADA** | Ya aprobada por los dueños en el corpus previo. |
| **PROPUESTA DEL TECHNICAL DESIGN** | Decisión mía, sujeta a aprobación. |
| **HIPÓTESIS** | Inferencia razonable no confirmada por fuente. |
| **SUPUESTO** | Premisa que asumo y que debe hacerse explícita. |
| **POR VERIFICAR** | Debe comprobarse en el momento de implementar, contra fuente viva. |
| **RIESGO** | Consecuencia adversa identificada. |
| **DECISIÓN PENDIENTE** | Requiere elección explícita de los dueños. |

### 0.2 Distinción obligatoria: dos clases de evidencia

Este spike distingue de forma estricta, y el lector debe hacerlo también:

- **`documented platform guarantee`** — la documentación oficial del proveedor afirma un comportamiento. Es lo que se puede citar como base de diseño.
- **`observed in current environment`** — lo que ocurrió en esta máquina, hoy, con estas versiones. **Jamás** es una garantía de plataforma: es una muestra de tamaño uno, en un sistema operativo, una arquitectura y una versión concretos.

Una tercera categoría, más débil todavía, que aparece en §3:

- **`vendor self-reported`** — afirmaciones de rendimiento o calidad hechas por el propio mantenedor de una librería en su README. No son documentación de plataforma ni medición independiente. **No se usan como base de decisión en este documento.**

### 0.3 Alcance de lo que se hizo y lo que NO se hizo

**Lo que se hizo:** verificación documental contra fuentes oficiales primarias (nodejs.org, rfc-editor.org, sqlite.org, repositorios oficiales de las librerías) y una sonda mínima de entorno (§5).

**Lo que NO se hizo:** no se escribió ningún spike ejecutable bajo `experiments/`, no se midió rendimiento, no se probó FTS5 con corpus en español, no se probó ningún driver de SQLite. Todo lo empírico queda como `NOT_TESTED`, listado en §9.

**Regla respetada:** no se escribió código de producción. `src/` nunca importa de `experiments/` (kernel §13).

---

## 1. Node.js LTS

### 1.1 Regla de no congelación

**DECISIÓN APROBADA (kernel §13):** "TypeScript + Node.js LTS. Versión concreta: se fija en implementación contra fuente oficial; no se congela aquí."

Este spike **respeta esa regla**: no fija una versión. Fija **dónde** consultarla y **qué criterio** aplicar.

### 1.2 Dónde se consulta el calendario oficial

**HECHO VERIFICADO.** La página oficial de releases de nodejs.org delega explícitamente el calendario al repositorio `nodejs/Release`:

> "Full details regarding the Node.js release schedule are available on GitHub."
> — https://nodejs.org/en/about/previous-releases

Fuentes canónicas, en orden de autoridad para esta cuestión:

1. **`https://github.com/nodejs/Release#release-schedule`** — tabla de calendario mantenida por el Release WG. **Fuente autoritativa.**
2. **`https://raw.githubusercontent.com/nodejs/Release/main/schedule.json`** — la misma información en forma **legible por máquina**. Es la que debe usar cualquier chequeo automatizado en CI; no se debe parsear HTML de nodejs.org.
3. **`https://nodejs.org/en/about/previous-releases`** — página de presentación, derivada de lo anterior.
4. **`https://nodejs.org/api/documentation.html#stability-index`** — para interpretar el estado de estabilidad de **APIs concretas**, que es una dimensión distinta del estado LTS de la **release line** (ver §3.2). Confundir ambas es un error clásico.

### 1.3 Política de ciclo de vida (lo que no cambia)

**HECHO VERIFICADO**, `https://github.com/nodejs/Release`:

- "New *semver-major* releases of Node.js are branched from `main` every six months. New even-numbered versions are released in April and odd-numbered versions in October."
- "Every even (LTS) major version will be actively maintained for 12 months from the date it enters LTS coverage. Following those 12 months of active support, the major version will transition into 'maintenance' mode for 18 months."
- Las versiones **impares nunca entran en LTS**.
- nodejs.org añade: el estado LTS "typically guarantees critical bug fixes for a total of 30 months", y las aplicaciones en producción deben usar solo **Active LTS** o **Maintenance LTS**.

Esta política es estructural y estable; el **calendario concreto** es lo volátil.

### 1.4 Estado del calendario en la fecha de verificación

**HECHO VERIFICADO** en `https://github.com/nodejs/Release` a fecha 2026-08-24. **Este bloque caduca**: es una foto, no una decisión.

| Línea | Codename | Estado (2026-08-24) | Release inicial | Entra en Active LTS | Entra en Maintenance | End-of-Life |
|---|---|---|---|---|---|---|
| 26.x | — | **Current** | 2026-05-05 | 2026-10-28 | 2027-10-20 | 2029-04-30 |
| 24.x | Krypton | **Active LTS** | 2025-05-06 | 2025-10-28 | 2026-10-20 | 2028-04-30 |
| 22.x | Jod | **Maintenance LTS** | 2024-04-24 | 2024-10-29 | 2025-10-21 | 2027-04-30 |
| 20.x | Iron | **End-of-Life** | 2023-04-17 | 2023-10-24 | 2024-10-22 | 2026-04-30 |

**Consecuencia temporal que hay que anticipar (HECHO VERIFICADO sobre el calendario, no predicción):** el 2026-10-20 la línea 24.x pasa a Maintenance y el 2026-10-28 la línea 26.x entra en Active LTS. Si la implementación arranca cerca de esas fechas, la elección "la Active LTS del momento" cambia de respuesta.

### 1.5 Nota de honestidad sobre una discrepancia de extracción

**INCONCLUSIVE.** La extracción automática de `https://nodejs.org/en/about/previous-releases` devolvió etiquetas internamente inconsistentes (marcaba 22.x como "LTS / Active LTS" y 20.x simultáneamente como "EOL" y "Maintenance LTS (transitioning)"). La tabla de `nodejs/Release` es coherente y es la fuente que nodejs.org designa como autoritativa, por lo que §1.4 se toma de ahí. **Se registra la discrepancia en lugar de ocultarla**: indica que la página de presentación no debe usarse como fuente para automatismos.

### 1.6 Criterio de selección propuesto

**PROPUESTA DEL TECHNICAL DESIGN.** En lugar de una versión, se aprueba una **regla**:

> El Core declara en `package.json#engines` un **piso mínimo** (`>=X.Y.Z`), no una versión exacta. El piso mínimo se determina en el momento de implementar como **la menor versión que satisfaga simultáneamente**: (a) estar en Active LTS o Maintenance LTS según `schedule.json`; (b) contener todas las APIs de las que dependa el Core (hoy: `crypto.randomUUIDv7`, §2.4); (c) tener fecha de EOL posterior al horizonte de soporte comprometido con la usuaria.

**RIESGO si no se hace así:** congelar una versión exacta en el kernel produce documentación falsa en menos de doce meses, y anclar a "la última" produce roturas silenciosas al cambiar de línea.

### 1.7 Tabla de verificación — Node.js LTS

| Afirmación | Fuente oficial (URL) | Estado |
|---|---|---|
| El calendario oficial de releases se mantiene en `nodejs/Release`, y nodejs.org delega en él | https://nodejs.org/en/about/previous-releases | **VERIFIED** |
| Existe una forma legible por máquina del calendario (`schedule.json`) | https://github.com/nodejs/Release | **VERIFIED** |
| Majors semver cada seis meses; pares en abril, impares en octubre; solo los pares entran en LTS | https://github.com/nodejs/Release | **VERIFIED** |
| Active LTS dura 12 meses; Maintenance dura 18 meses después | https://github.com/nodejs/Release | **VERIFIED** |
| Producción debe usar solo Active LTS o Maintenance LTS | https://nodejs.org/en/about/previous-releases | **VERIFIED** |
| A 2026-08-24: 26.x Current, 24.x Active LTS, 22.x Maintenance LTS, 20.x EOL | https://github.com/nodejs/Release | **VERIFIED** (foto con fecha; caduca) |
| Etiquetas de estado en la página `previous-releases` de nodejs.org | https://nodejs.org/en/about/previous-releases | **INCONCLUSIVE** (extracción inconsistente; ver §1.5) |
| Qué versión exacta usará el Core | — | **POR VERIFICAR** (por diseño, §1.6) |

---

## 2. UUIDv7 frente a ULID

### 2.1 ¿Está UUIDv7 estandarizado?

**HECHO VERIFICADO. Sí.**

- **RFC 9562**, "Universally Unique IDentifiers (UUIDs)", autores K. Davis, B. Peabody, P. Leach, publicado en **2024**.
- Estado: **Proposed Standard** (Internet Standards Track). **Obsoletes: RFC 4122.**
- Fuente: https://www.rfc-editor.org/info/rfc9562

Esto responde a la pregunta del encargo: RFC 9562 no es "candidato", es el RFC vigente, y sustituye al RFC 4122 que definía las versiones 1–5.

**Layout de UUIDv7 (§5.7 de RFC 9562), HECHO VERIFICADO:**

```text
 48 bits  unix_ts_ms   timestamp Unix en milisegundos, big-endian, sin signo
  4 bits  ver          = 0b0111 (7)
 12 bits  rand_a       datos pseudoaleatorios
  2 bits  var          = 0b10
 62 bits  rand_b       datos pseudoaleatorios
```

**Ordenabilidad (§6.11 "Sorting"), cita:**
> "UUIDv6 and UUIDv7 are designed so that implementations that require sorting […] sort as opaque raw bytes without the need for parsing or introspection."

**Opacidad (§6.12 "Opacity"), cita:**
> "Avoiding parsing UUID values unnecessarily is recommended; instead, treat UUIDs as opaquely as possible."

Esto **coincide literalmente** con el requisito del kernel §11: identificadores opacos.

**Monotonicidad (§6.2 "Monotonicity and Counters"), cita:**
> "Implementations SHOULD employ the following methods for single-node UUID implementations that require batch UUID creation or are otherwise concerned about monotonicity with high-frequency UUID generation."

Es un **SHOULD**, no un MUST, y describe tres métodos alternativos (contador de longitud fija, incremento monótono del aleatorio, sustituir bits aleatorios por precisión de reloj adicional). **Consecuencia:** que un generador concreto sea monótono dentro del mismo milisegundo **no es una garantía del estándar**; depende de la implementación.

**Reloj (§6.1 "Timestamp Considerations"), cita:**
> "if it is possible for the system clock to move backward due to either manual adjustment or corrections from a time synchronization protocol, implementations need to determine how to handle such cases."

**Seguridad (§8), cita:**
> "Implementations SHOULD NOT assume that UUIDs are hard to guess. For example, they MUST NOT be used as security capabilities (identifiers whose mere possession grants access)."

**Compatibilidad con el kernel:** esto es **compatible** con nuestro diseño, porque el kernel §3.3 ya establece que la autorización humana es server-side y no viaja como token: la posesión de un `proposal_item_id` no otorga nada. Si en algún momento se quisiera que un id fuera una capacidad, el RFC lo prohíbe explícitamente. **Registrar como restricción permanente.**

### 2.2 ¿Node lo soporta nativamente?

**Esta es la respuesta más importante del spike, y cambió recientemente.**

#### 2.2.1 `crypto.randomUUID()` genera v4 — confirmado

**HECHO VERIFICADO.** `crypto.randomUUID([options])` genera **UUID versión 4** (aleatoria), añadido en **v15.7.0**.
Fuente: https://nodejs.org/docs/latest-v24.x/api/crypto.html

**Consecuencia:** `crypto.randomUUID()` **no sirve** para el requisito de ordenabilidad temporal del kernel §11. Es aleatorio puro.

#### 2.2.2 `crypto.randomUUIDv7()` — existe, es nativo, y es reciente

**HECHO VERIFICADO.** Node.js incorporó una API nativa dedicada:

| Línea | Versión donde aparece | Fuente |
|---|---|---|
| 26.x (Current) | **v26.1.0** (2026-05-07) | https://github.com/nodejs/node/releases/tag/v26.1.0 |
| 24.x (LTS) | **v24.16.0** (2026-05-21), retroportada | https://nodejs.org/en/blog/release/v24.16.0 |
| 22.x (Maintenance LTS) | **NO EXISTE** en la documentación de v22 | https://nodejs.org/docs/latest-v22.x/api/crypto.html |

Entrada de changelog, cita verbatim:
> "**(SEMVER-MINOR)** **crypto**: implement randomUUIDv7() (nabeel378) [#62553]"

Documentación añadida, cita verbatim (commit `b267f6bca3`):
> "Generates a random RFC 9562 version 7 UUID. The UUID contains a millisecond precision Unix timestamp in the most significant 48 bits, followed by cryptographically secure random bits for the remaining fields, making it suitable for use as a database key with time-based sorting."

Opción documentada: `disableEntropyCache` (por defecto `false`); Node cachea entropía suficiente para hasta 128 UUIDs para mejorar rendimiento.

#### 2.2.3 La advertencia que hay que leer entera

**HECHO VERIFICADO.** Un commit de documentación posterior (`1684ab8ff8`, PR #62600, presente en v26.1.0 y retroportado a v24.16.0) añade esta frase, cita verbatim:

> "The embedded timestamp relies on a non-monotonic clock and is not guaranteed to be strictly increasing."

**Esta frase es determinante para el diseño y se desarrolla en §2.6.**

### 2.3 Librerías que implementan UUIDv7

| Librería | Versiones UUID | Notas verificadas | Fuente |
|---|---|---|---|
| `uuid` (uuidjs/uuid) | v1, v3, v4, v5, v6, v7 (v8 no implementada) | v7 añadida en **10.0.0 (2024-06-07)**, entrada de changelog: "support rfc9562 v7 uuids". No marcada como experimental. Última versión vista: **14.0.2 (2026-08-18)**. **Desde `uuid@12` no soporta CommonJS** (ESM-only). Soporta "Node.js LTS releases plus one prior version". | https://github.com/uuidjs/uuid |
| `uuidv7-js` (TheEdoRan) | v7 | Aparece en resultados de búsqueda como "RFC 9562 compliant". **NO verificado en profundidad en este spike.** | — |

**Madurez de `uuid` v7:** el paquete expone `v7(options)` con opciones `msecs`, `random`/`rng`, `seq`, `buf`, `offset`. La opción `seq` está documentada así, cita:
> "32-bit sequence Number between 0 - 0xffffffff. This may be provided to help ensure uniqueness for UUIDs generated within the same millisecond time interval."

Es decir: `uuid` **expone** un mecanismo de secuencia para el mismo milisegundo, y su changelog muestra trabajo sostenido sobre el estado interno de v7 (`11.0.0`: "refactor v7 internal state and options logic"; `14.0.2`: "align default seq formula in v7Bytes with updateV7State"). **HIPÓTESIS**, no verificada en la doc: eso implica que mantiene estado monótono interno por proceso. **POR VERIFICAR** si se elige esta vía.

**Observación de riesgo de dependencia (RIESGO):** el propio historial de `14.0.2` corrigiendo la fórmula de secuencia demuestra que la monotonicidad intra-milisegundo es **superficie de bug activa**, en cualquier implementación. No debe construirse ninguna invariante del Core sobre ella. Ver §2.6.

### 2.4 Comparación UUIDv7 vs ULID

| Dimensión | UUIDv7 | ULID |
|---|---|---|
| **Estatus normativo** | **RFC 9562, IETF Proposed Standard**, obsoleta RFC 4122 | **Especificación comunitaria** en `github.com/ulid/spec`; **no publicada por IETF ni ISO** |
| **Tamaño binario** | 128 bits | 128 bits |
| **Forma canónica en texto** | 36 caracteres (hex con guiones) | **26 caracteres**, Crockford base32 (`0123456789ABCDEFGHJKMNPQRSTVWXYZ`, sin I/L/O/U) |
| **Timestamp** | 48 bits, Unix ms | 48 bits, Unix ms ("till the year 10889 AD") |
| **Aleatoriedad** | 74 bits (12 en `rand_a` + 62 en `rand_b`) | 80 bits |
| **Ordenabilidad** | Ordenable como bytes opacos (§6.11) | Lexicográficamente ordenable en ASCII |
| **Monotonicidad intra-ms** | **SHOULD** del RFC; dependiente de implementación | La spec define incremento del componente aleatorio con acarreo, en modo monótono |
| **Case sensitivity** | Hex; canónicamente minúsculas | **Case-insensitive** por spec |
| **Generación offline / sin autoridad central** | Sí | Sí |
| **Derivado de nombre o de hash** | No (eso son v3/v5 y v8-hash) | No |
| **Soporte nativo en Node** | **Sí**, `crypto.randomUUIDv7()` desde v24.16.0 / v26.1.0 | No |
| **Soporte como tipo nativo en motores de BD** | Amplio en el ecosistema SQL (tipo `UUID`) | Sin tipo nativo; se almacena como texto o blob |

Fuentes: https://www.rfc-editor.org/rfc/rfc9562.html · https://github.com/ulid/spec · https://nodejs.org/api/crypto.html

### 2.5 Recomendación para el Core

**PROPUESTA DEL TECHNICAL DESIGN: UUIDv7.** Confirma la propuesta del kernel §11 y cierra la alternativa ULID.

Contraste contra los cinco criterios literales del kernel §11:

| Criterio del kernel §11 | UUIDv7 | ULID | Discriminante |
|---|---|---|---|
| Opacos | Sí — §6.12 del RFC lo **prescribe** | Sí, de facto | Empate, ligera ventaja UUIDv7 (está escrito en una norma) |
| Generados por el Core | Sí | Sí | Empate |
| Offline-friendly | Sí | Sí | Empate |
| No derivados de nombres ni de hash | Sí | Sí | Empate |
| Ordenables por tiempo | Sí, §6.11 | Sí | Empate |

Los cinco criterios los cumplen ambos. **La decisión se toma, por tanto, sobre criterios de segundo orden**, y ahí UUIDv7 gana por tres razones, en orden de peso:

1. **Estatus normativo (decisiva).** RFC 9562 es Standards Track del IETF y obsoleta al RFC 4122. ULID es una especificación comunitaria sin cuerpo de estandarización. Para un producto cuyo dominio es jurídico y cuya arquitectura declara *vendor-independence*, apoyar la identidad de todas las entidades del expediente sobre una norma publicada, versionada y citable es cualitativamente distinto de apoyarla sobre un repositorio.
2. **Cero dependencias de terceros para la identidad.** Con piso Node ≥ 24.16.0, la generación de identidad usa `crypto.randomUUIDv7()` de la biblioteca estándar. La identidad de las entidades del expediente es el elemento de infraestructura **menos** apropiado para depender de un paquete de npm: no puede cambiar nunca, no puede fallar, y su superficie de suministro debe ser mínima.
3. **Interoperabilidad de tipo.** Si en el futuro post-V0 se materializa PostgreSQL (kernel §15), el tipo `UUID` existe nativamente; ULID requeriría representación ad hoc.

**Argumento a favor de ULID que hay que reconocer, y por qué no gana:** 26 caracteres frente a 36, sin guiones, case-insensitive — más cómodo si el identificador aparece en URLs o se dicta por teléfono. No gana porque el kernel §11 exige que los identificadores sean **opacos**, y un identificador opaco no está pensado para ser leído ni dictado por la usuaria; optimizar su ergonomía humana es optimizar una propiedad que el diseño declara irrelevante. Los 10 caracteres de diferencia no compensan la pérdida de estatus normativo.

### 2.6 Implicación arquitectónica: separar *ordenabilidad* de *ordenación canónica*

**Esta es la corrección más importante que este spike aporta al kernel.**

El kernel §11 dice que los identificadores son "ordenables por tiempo". Es cierto, pero la documentación de Node es explícita:

> "The embedded timestamp relies on a non-monotonic clock and is not guaranteed to be strictly increasing."

Y RFC 9562 §6.1 advierte que el reloj del sistema puede retroceder por ajuste manual o por corrección NTP.

**PROPUESTA DEL TECHNICAL DESIGN — invariante a añadir:**

> El orden canónico de los eventos del Case Event Log es **`event_seq`** (kernel §8.1), y **nunca** el orden de los `event_id`. La ordenabilidad temporal de UUIDv7 es una propiedad **de localidad de índice y de conveniencia de depuración**, no una fuente de verdad. Ninguna consulta, proyección, hash-chain ni invariante del dominio puede depender de que ordenar por identificador produzca el orden de ocurrencia.

Justificación: el Legal OS corre en la máquina de la usuaria (Windows), donde el reloj **puede** retroceder — corrección NTP, cambio manual, suspensión/reanudación. Si el orden de los hechos de un expediente jurídico dependiera del reloj local, un ajuste de reloj produciría un expediente cuyo relato está desordenado. El kernel ya tiene el contador correcto (`event_seq`, monotónico por caso, +1 en todo evento); esta nota solo prohíbe explícitamente el atajo de ordenar por id.

**Corolario sobre el hash-chain (kernel §8.3):** `prev_event_hash` encadena por `event_seq`, no por tiempo. La propiedad *tamper-evident* no se degrada por un reloj no monótono. **HECHO VERIFICADO** por construcción del propio contrato del kernel, no por fuente externa.

**Corolario sobre `occurred_at`:** un `occurred_at` que retroceda respecto al evento anterior es **posible** y no debe hacer fallar ninguna invariante. **DECISIÓN PENDIENTE:** si el Core debe además registrar un reloj monótono independiente (p. ej. `process.hrtime.bigint()` de arranque) para diagnóstico, o si `event_seq` basta. **PROPUESTA:** basta `event_seq`; añadir un segundo reloj es complejidad sin consumidor en V0.

### 2.7 Implicación arquitectónica: puerto `IdGenerator`

**PROPUESTA DEL TECHNICAL DESIGN.** La generación de identidad se expone como un **puerto** en `application`, implementado en `infrastructure`:

```text
IdGenerator
  newId() -> EntityId      // UUIDv7 en forma canónica
```

Razones:
1. El dominio no debe importar `node:crypto` — violaría la regla de dependencias del kernel §13 (`domain` no importa infraestructura).
2. Permite sustituir la implementación nativa por `uuid@14` si el piso de Node no puede cumplirse (§2.8), **sin tocar dominio ni aplicación**.
3. Permite un generador determinista en tests, que es lo que hace verificables invariantes como "reordenar la propuesta no cambia ningún `proposal_item_id`" (kernel §2.1).

**Regla dura que se mantiene (kernel §11):** `entity identity ≠ content identity`. `IdGenerator` **nunca** produce `item_content_hash` ni `payload_hash`; esos son SHA-256 sobre la forma normalizada y viven en un puerto distinto (`ContentHasher`). Un puerto que hiciera ambas cosas invitaría exactamente al error que la regla prohíbe.

### 2.8 Consecuencia sobre el piso de Node

**PROPUESTA DEL TECHNICAL DESIGN.** Si se aprueba UUIDv7 nativo, el piso mínimo queda acotado por abajo:

- `crypto.randomUUIDv7()` **no existe** en 22.x (Maintenance LTS). Por tanto **22.x queda descartada** si se quiere identidad nativa sin dependencias.
- El piso más bajo compatible sería **>= 24.16.0**.

**DECISIÓN PENDIENTE para los dueños — dos caminos mutuamente excluyentes:**

- **Camino A (recomendado):** piso `>= 24.16.0`, identidad con `crypto.randomUUIDv7()`, **cero dependencias de identidad**. Coste: excluye 22.x.
- **Camino B:** piso más bajo, identidad con `uuid@14` (`v7()`). Coste: una dependencia de npm en el elemento más crítico de la infraestructura, y `uuid@12+` es **ESM-only** — lo que condiciona la configuración de módulos de TypeScript de todo el proyecto.

**PROPUESTA:** Camino A. 22.x llega a EOL el 2027-04-30 según §1.4; adoptarla hoy compraría poco margen a cambio de una dependencia permanente.

### 2.9 Tabla de verificación — UUIDv7 y ULID

| Afirmación | Fuente oficial (URL) | Estado |
|---|---|---|
| UUIDv7 está estandarizado en RFC 9562, Proposed Standard, que obsoleta RFC 4122 | https://www.rfc-editor.org/info/rfc9562 | **VERIFIED** |
| Layout de UUIDv7: 48b unix_ts_ms + 4b ver + 12b rand_a + 2b var + 62b rand_b | https://www.rfc-editor.org/rfc/rfc9562.html | **VERIFIED** |
| El RFC declara que v6/v7 se ordenan como bytes opacos (§6.11) | https://www.rfc-editor.org/rfc/rfc9562.html | **VERIFIED** |
| El RFC recomienda tratar los UUIDs opacamente (§6.12) | https://www.rfc-editor.org/rfc/rfc9562.html | **VERIFIED** |
| La monotonicidad intra-ms es SHOULD, no MUST (§6.2) | https://www.rfc-editor.org/rfc/rfc9562.html | **VERIFIED** |
| Los UUIDs no deben usarse como *security capabilities* (§8) | https://www.rfc-editor.org/rfc/rfc9562.html | **VERIFIED** |
| `crypto.randomUUID()` genera UUID v4; añadida en v15.7.0 | https://nodejs.org/docs/latest-v24.x/api/crypto.html | **VERIFIED** |
| `crypto.randomUUIDv7()` existe en Node y genera UUID v7 RFC 9562 | https://nodejs.org/api/crypto.html#cryptorandomuuidv7options | **VERIFIED** |
| Añadida en v26.1.0 (Current) | https://github.com/nodejs/node/releases/tag/v26.1.0 | **VERIFIED** |
| Retroportada a v24.16.0 (LTS), 2026-05-21, PR #62553 | https://nodejs.org/en/blog/release/v24.16.0 | **VERIFIED** |
| NO está documentada en la línea v22 | https://nodejs.org/docs/latest-v22.x/api/crypto.html | **VERIFIED** (ausencia en doc oficial) |
| La doc oficial advierte: reloj no monótono, no estrictamente creciente | https://github.com/nodejs/node/commit/1684ab8ff8 | **VERIFIED** |
| `crypto.randomUUIDv7()` acepta `disableEntropyCache`; Node cachea entropía para hasta 128 UUIDs | https://github.com/nodejs/node/commit/b267f6bca3 | **VERIFIED** |
| ¿`crypto.randomUUIDv7()` implementa contador monótono intra-ms? | — | **NOT_FOUND** (no documentado) |
| `uuid` implementa v7 desde 10.0.0 (2024-06-07), no marcada experimental | https://github.com/uuidjs/uuid/blob/main/CHANGELOG.md | **VERIFIED** |
| `uuid@12+` no soporta CommonJS (ESM-only) | https://github.com/uuidjs/uuid | **VERIFIED** |
| `uuid.v7()` expone `seq` para unicidad dentro del mismo milisegundo | https://github.com/uuidjs/uuid | **VERIFIED** |
| `uuid` mantiene estado monótono interno por proceso | — | **INCONCLUSIVE** (indicios en changelog, no afirmado en doc) |
| ULID: 26 caracteres, Crockford base32, 48b timestamp + 80b aleatorio | https://github.com/ulid/spec | **VERIFIED** |
| ULID es especificación comunitaria, no publicada por IETF ni ISO | https://github.com/ulid/spec | **VERIFIED** |
| `uuidv7-js` es RFC 9562 compliant | — | **INCONCLUSIVE** (no verificado en profundidad) |

---

## 3. SQLite desde Node

### 3.1 Opciones identificadas

Se verificaron tres opciones con fuente oficial. Se nombran otras dos sin verificar, marcadas como tales.

### 3.2 `node:sqlite` (módulo integrado)

**HECHO VERIFICADO**, https://nodejs.org/api/sqlite.html

| Propiedad | Valor | Notas |
|---|---|---|
| Añadido en | **v22.5.0** | |
| Sin flag experimental desde | **v22.13.0 / v23.4.0** ("no longer behind `--experimental-sqlite` but still experimental") | |
| Estabilidad en docs v22 | **Stability: 1.1 - Active development** | |
| Estabilidad en docs v24 y v26 | **Stability: 1.2 - Release candidate** (pasó a RC en **v25.7.0**) | |
| Modelo de ejecución | **Síncrono** — clases `DatabaseSync` / `StatementSync`. La única excepción documentada es `sqlite.backup()`, que devuelve una Promise | |
| Prepared statements | Sí — `.all()`, `.get()`, `.run()`, `.iterate()` | |
| Carga de extensiones | Sí — `allowExtension`, `enableLoadExtension()`, `loadExtension()` | |
| Otras opciones del constructor | `open`, `readOnly`, `enableForeignKeyConstraints` (default `true`), `enableDoubleQuotedStringLiterals` (default `false`), `timeout` (busy timeout, default `0`), `readBigInts`, `returnArrays`, `allowBareNamedParameters`, `allowUnknownNamedParameters`, `defensive` (default `true`), `limits` | |
| WAL | **NO mencionado en la documentación del módulo** | Ver §3.5 |
| FTS5 | **NO mencionado en la documentación del módulo** | Ver §3.6 |
| Versión de SQLite embebida | **NO documentada** | **POR VERIFICAR** con `SELECT sqlite_version()` |

**El dato que manda sobre esta opción — cita verbatim del índice de estabilidad de Node** (https://nodejs.org/api/documentation.html#stability-index), aplicable a todo Stability 1 incluidos sus subniveles:

> "Stability: 1 - Experimental. The feature is not subject to semantic versioning rules. Non-backward compatible changes or removal may occur in any future release. **Use of the feature is not recommended in production environments.**"

Y sobre el subnivel 1.2 concretamente:

> "1.2 - Release candidate. Experimental features at this stage are hopefully ready to become stable. No further breaking changes are anticipated but may still occur in response to user feedback or the features' underlying specification development."

**Lectura honesta:** 1.2 es la antesala de estable y "no se anticipan más cambios rompedores", pero el texto de nivel 1 es inequívoco: **no está sujeto a semver y su uso en producción no está recomendado por el propio proyecto Node.** Citar solo "1.2 - Release candidate" y omitir la frase de producción sería seleccionar la evidencia.

**RIESGO concreto:** un cambio no retrocompatible en `node:sqlite` dentro de una release **patch o minor** de Node no violaría ninguna promesa de Node, pero sí rompería un producto que persiste expedientes jurídicos. La superficie afectada sería el adapter de persistencia, no el dominio — que es exactamente el argumento a favor del puerto (§3.7).

### 3.3 `better-sqlite3`

**HECHO VERIFICADO**, https://github.com/WiseLibs/better-sqlite3

| Propiedad | Valor |
|---|---|
| Modelo de ejecución | **Síncrono**, por diseño declarado |
| Prepared statements | Sí (`.prepare()`) |
| Transacciones | "Full transaction support" |
| WAL | **Documentado explícitamente**: "it is generally important to set the WAL pragma", con ejemplo `db.pragma('journal_mode = WAL')` |
| Distribución | Módulo **nativo**; "prebuilt binaries available for major platforms/architectures"; requiere "a currently supported Node.js version" |
| Licencia | **MIT** |
| SQLite embebido | **3.53.4** según su `docs/compilation.md` |
| Opciones de compilación por defecto | Incluyen `SQLITE_ENABLE_FTS3`, `SQLITE_ENABLE_FTS4`, **`SQLITE_ENABLE_FTS5`**, `SQLITE_ENABLE_JSON1`, `SQLITE_ENABLE_RTREE`, `SQLITE_ENABLE_GEOPOLY`, `SQLITE_ENABLE_MATH_FUNCTIONS`, `SQLITE_ENABLE_STAT4`, `SQLITE_DEFAULT_CACHE_SIZE=-16000`, `SQLITE_DEFAULT_FOREIGN_KEYS=1`, `SQLITE_THREADSAFE=2` |
| Amalgamation personalizada | Soportada vía `--build-from-source --sqlite3=<dir>` |

**Sobre el rendimiento — declaración explícita de este spike:** el README de `better-sqlite3` contiene afirmaciones comparativas de rendimiento con enlace a su propia guía de benchmark. Son **`vendor self-reported`**. La extracción automática de esas cifras además produjo un resultado incoherente (invertía el sentido de la comparación), por lo que **no se reproducen aquí**. Estado: **INCONCLUSIVE**. **Ninguna decisión de este documento se apoya en rendimiento**, conforme al encargo.

**RIESGO específico del entorno objetivo (Windows):** al ser módulo nativo, si no existe binario precompilado para la combinación exacta (versión de Node × ABI × arquitectura × plataforma), `npm install` intenta compilar y requiere toolchain (en Windows, Visual Studio Build Tools). Para un producto que se instala en la máquina de una profesional del derecho, un fallo de compilación en instalación es un fallo de producto. **POR VERIFICAR** en el momento de implementar: existencia de prebuild para el piso de Node elegido en `win32-x64` y, si aplica, `win32-arm64`.

### 3.4 `sqlite3` (TryGhost/node-sqlite3) — descartada

**HECHO VERIFICADO**, https://github.com/TryGhost/node-sqlite3

| Propiedad | Valor |
|---|---|
| Nombre npm | `sqlite3` |
| Modelo | **Asíncrono**, "Asynchronous, non-blocking SQLite3 bindings for Node.js" |
| Binarios | `prebuild-install`; Node-API v3 y v6; Node **v20.17.0+** |
| SQLite embebido | 3.52.0, con json1 |
| **Estado de mantenimiento** | **"Note: This repository is currently unmaintained. We will not update any of its issues or pull requests."** |

**PROPUESTA DEL TECHNICAL DESIGN: descartada.** Una dependencia declarada sin mantenimiento por su propio repositorio no es admisible para el almacén canónico de un expediente jurídico. No se evalúa más.

### 3.5 WAL — hechos y qué implica

**HECHO VERIFICADO**, https://www.sqlite.org/wal.html

- Se activa con `PRAGMA journal_mode=WAL;`. Devuelve `"wal"` si tuvo éxito.
- **Es persistente**: "If a process sets WAL mode, then closes and reopens the database, the database will come back in WAL mode."
- Introducido en SQLite **3.7.0** (2010-07-21).
- Limitaciones documentadas: **todos los procesos deben estar en el mismo host** ("WAL does not work over a network filesystem"); requiere memoria compartida (wal-index) y soporte VFS de shared-memory v2; crea ficheros `-wal` y `-shm`; no se puede cambiar `page_size` en WAL; transacciones sobre varias bases `ATTACH`ed no son atómicas como conjunto; no ideal para transacciones muy grandes.

**Implicaciones para el diseño:**

1. **WAL es una propiedad del motor SQLite, no del driver.** Se activa ejecutando SQL. Por tanto la pregunta "¿el driver soporta WAL?" se reduce a "¿el driver puede ejecutar ese PRAGMA y el SQLite embebido lo soporta?". `better-sqlite3` lo documenta explícitamente. Para `node:sqlite`, la doc **no lo menciona**; que `database.exec('PRAGMA journal_mode = WAL')` funcione es **HIPÓTESIS** razonable (expone `exec()` y el PRAGMA es SQL estándar de SQLite), pero **NO es una garantía documentada de plataforma**. → **POR VERIFICAR** empíricamente antes de comprometerse.
2. **Persistencia del modo:** como WAL persiste en el fichero, basta activarlo una vez al crear el `case.db`. No obstante, **PROPUESTA:** el Core debe **verificar** el modo al abrir cada caso y no asumirlo — un `case.db` restaurado desde copia, o creado por una versión anterior, puede no estar en WAL.
3. **RIESGO OPERATIVO ALTO — carpetas sincronizadas.** La limitación de "mismo host / no network filesystem" tiene una consecuencia directa y muy probable en el entorno objetivo: si el `case.db` se guarda en una carpeta sincronizada por OneDrive, Dropbox o Google Drive, o en una unidad de red del despacho, la premisa de SQLite se rompe. **PROPUESTA DEL TECHNICAL DESIGN:** el Core detecta y **rechaza o advierte** al abrir un Case cuya ruta esté en una ubicación de ese tipo. **DECISIÓN PENDIENTE:** rechazar (seguro, rígido) frente a advertir (permisivo, arriesgado). Dado PF-002 ("Original evidence cannot be overwritten or deleted through the product surface"), la coherencia empuja a **rechazar**. **POR VERIFICAR:** cómo se detecta de forma fiable una carpeta sincronizada en Windows — no hay API documentada universal para ello; es **NOT_TESTED** en este spike.
4. **Compatible con V0 por alcance:** el kernel §15 sitúa multi-máquina y sync fuera de V0, de modo que la limitación de "mismo host" no bloquea el diseño; solo obliga a proteger el caso patológico del punto 3.

### 3.6 FTS5: ¿está disponible desde cada driver?

**HECHO VERIFICADO — SQLite en general** (https://www.sqlite.org/fts5.html):
- FTS5 está incluido en SQLite desde la versión **3.9.0 (2015-10-14)**.
- **No siempre está compilado**: "FTS5 is **disabled by default** in the source-tree configure script" pero **"enabled by default for the amalgamation configure script"**. Se habilita con `--enable-fts5` o `-DSQLITE_ENABLE_FTS5`.

**Consecuencia:** "SQLite soporta FTS5" es una afirmación sobre el **build**, no sobre el motor. Hay que verificarla por driver.

| Driver | ¿FTS5? | Evidencia | Estado |
|---|---|---|---|
| `better-sqlite3` | Sí | `SQLITE_ENABLE_FTS5` listado entre las opciones de compilación por defecto en su `docs/compilation.md` | **VERIFIED** (doc del proyecto) |
| `node:sqlite` | Sí, aparentemente | `'SQLITE_ENABLE_FTS5',` aparece en `deps/sqlite/sqlite.gyp` de `nodejs/node`, rama `main` | **VERIFIED como fichero de build; NO como garantía de API** — ver aviso abajo |

**Aviso de precisión sobre `node:sqlite` y FTS5.** El fichero `deps/sqlite/sqlite.gyp` es el fichero de build del propio proyecto Node, y es fuente primaria de **cómo se compila hoy la rama `main`**. Pero:
- **no es documentación de API**, y por tanto **no es una `documented platform guarantee`**: Node no promete en `nodejs.org/api/sqlite.html` que FTS5 esté disponible, y podría dejar de compilarlo sin romper ninguna promesa;
- `main` **no es** necesariamente la línea de release que se vaya a usar.
→ **POR VERIFICAR** contra el binario concreto del piso de Node elegido, en el momento de implementar.

Otros defines observados en `deps/sqlite/sqlite.gyp` (rama `main`): `SQLITE_DEFAULT_MEMSTATUS=0`, `SQLITE_ENABLE_COLUMN_METADATA`, `SQLITE_ENABLE_DBSTAT_VTAB`, `SQLITE_ENABLE_FTS3`, `SQLITE_ENABLE_FTS3_PARENTHESIS`, `SQLITE_ENABLE_FTS5`, `SQLITE_ENABLE_GEOPOLY`, `SQLITE_ENABLE_MATH_FUNCTIONS`, `SQLITE_ENABLE_PERCENTILE`, `SQLITE_ENABLE_PREUPDATE_HOOK`, `SQLITE_ENABLE_RBU`, `SQLITE_ENABLE_RTREE`, `SQLITE_ENABLE_SESSION`. No se observó `SQLITE_ENABLE_JSON1` ni ningún `SQLITE_OMIT_*`; la ausencia de `SQLITE_ENABLE_JSON1` **no** implica falta de JSON, porque (**HECHO VERIFICADO**, https://www.sqlite.org/json1.html) "The JSON functions and operators are built into SQLite by default, as of SQLite version 3.38.0 (2022-02-22)" y se excluyen con `-DSQLITE_OMIT_JSON`. Sobre `SQLITE_THREADSAFE` no se observó define explícito: **INCONCLUSIVE**, no se afirma nada.

### 3.7 Implicación arquitectónica: el puerto de persistencia

**PROPUESTA DEL TECHNICAL DESIGN.** El diseño del adapter debe absorber la diferencia entre drivers, no propagarla. Cinco reglas:

1. **El puerto vive en `application`; el driver vive en `infrastructure`.** Ningún tipo de `node:sqlite` ni de `better-sqlite3` (`DatabaseSync`, `Statement`, …) puede aparecer en firmas de `domain` ni de `application`. Es la regla de dependencias del kernel §13 aplicada a esta decisión concreta.

2. **El contrato del puerto es asíncrono (`Promise`) aunque ambos drivers sean síncronos.** Este es el punto contraintuitivo y por eso se justifica: los dos candidatos verificados son **síncronos** (`node:sqlite` con `DatabaseSync`/`StatementSync`; `better-sqlite3` por diseño declarado). Sería tentador definir el puerto síncrono para reflejarlo. **No debe hacerse**: congelaría el contrato de Application a una propiedad del driver, y cualquier futuro backend (kernel §15 menciona PostgreSQL post-V0) obligaría a reescribir todas las firmas del Core. Envolver una llamada síncrona en una `Promise` resuelta es trivial; desenvolver lo contrario no lo es. **La asimetría del coste decide.**

3. **Aislar en un único seam las dos cosas que difieren entre drivers**: (a) apertura/configuración de la conexión (pragmas: `journal_mode`, `foreign_keys`, `busy_timeout`) y (b) el manejo de transacciones. Todo lo demás es SQL, que es común.

4. **Ejecución síncrona = bloqueo del hilo.** **HECHO VERIFICADO** que ambos drivers son síncronos; **ANÁLISIS, no medición:** una llamada síncrona a disco bloquea el event loop del proceso mientras dura. En un servidor MCP que atiende invocaciones del modelo, eso significa que una operación de persistencia larga no se solapa con nada. **No se afirma nada sobre magnitud** — eso sería una afirmación de rendimiento sin fuente. Lo que sí se puede afirmar es la **consecuencia de diseño**: la decisión de mover la persistencia a un worker thread, si alguna vez hiciera falta, debe ser posible **sin cambiar el puerto**, y la regla 2 es precisamente lo que la deja abierta.

5. **`case.db` por caso** (implícito en el corpus previo) encaja bien con WAL persistente por fichero, y significa que la configuración de pragmas es una rutina de apertura de caso, no un arranque global.

### 3.8 Recomendación

**DECISIÓN PENDIENTE — se presentan las dos opciones con sus costes reales, sin ocultar el coste de la recomendada.**

| | `node:sqlite` | `better-sqlite3` |
|---|---|---|
| Dependencias externas | **Cero** | Una, nativa |
| Toolchain / prebuilds en instalación | **No aplica** | Sí — riesgo en Windows (§3.3) |
| Estabilidad declarada por su propio proyecto | Stability 1.2; **"not recommended in production environments"** | Sin declaración equivalente; proyecto MIT establecido |
| WAL documentado por el proyecto | **No** (hipótesis vía `exec()`) | **Sí**, con ejemplo |
| FTS5 | En el build de `main`; no en la doc de API | En su doc de compilación |
| Superficie de rotura | Cualquier release de Node | Versión mayor de la librería, controlada por lockfile |

**PROPUESTA DEL TECHNICAL DESIGN:** implementar V0 sobre **`better-sqlite3`**, detrás del puerto de §3.7, y **reevaluar `node:sqlite` cuando alcance Stability 2 — Stable**.

Razón única y decisiva: el proyecto Node dice, por escrito y en su propia documentación, que las features Stability 1 no están sujetas a semver y **no se recomiendan en producción**. Construir el almacén canónico de expedientes jurídicos sobre una API con esa etiqueta significa aceptar que una actualización de Node pueda romper la persistencia. El coste de `better-sqlite3` (una dependencia nativa, un riesgo de instalación **acotado y verificable**) es un coste conocido y mitigable; el de `node:sqlite` es un riesgo abierto que no controlamos.

**Coste que se acepta explícitamente al elegir `better-sqlite3`, y no se disimula:** riesgo de instalación en máquinas Windows sin prebuild disponible; dependencia de un mantenedor externo; necesidad de recompilar al cambiar de línea de Node.

**Condición de reversión, escrita ahora para que sea verificable después:** cuando `nodejs.org/api/sqlite.html` muestre **"Stability: 2 - Stable"** en la línea LTS que use el producto, se reabre la decisión. El puerto de §3.7 es lo que hace que reabrirla cueste un adapter y no un rediseño.

### 3.9 Tabla de verificación — SQLite desde Node

| Afirmación | Fuente oficial (URL) | Estado |
|---|---|---|
| `node:sqlite` fue añadido en v22.5.0 | https://nodejs.org/api/sqlite.html | **VERIFIED** |
| Sin flag `--experimental-sqlite` desde v22.13.0 / v23.4.0 | https://nodejs.org/api/sqlite.html | **VERIFIED** |
| `node:sqlite` es Stability 1.1 en la doc de v22 | https://nodejs.org/docs/latest-v22.x/api/sqlite.html | **VERIFIED** |
| `node:sqlite` es Stability 1.2 - Release candidate en v24/v26 (RC desde v25.7.0) | https://nodejs.org/api/sqlite.html | **VERIFIED** |
| Stability 1 no está sujeto a semver y su uso no se recomienda en producción | https://nodejs.org/api/documentation.html#stability-index | **VERIFIED** |
| `node:sqlite` es síncrono (`DatabaseSync`/`StatementSync`); `backup()` es la excepción asíncrona | https://nodejs.org/api/sqlite.html | **VERIFIED** |
| `node:sqlite` soporta prepared statements y carga de extensiones | https://nodejs.org/api/sqlite.html | **VERIFIED** |
| `node:sqlite` documenta WAL | https://nodejs.org/api/sqlite.html | **NOT_FOUND** (no mencionado) |
| `node:sqlite` documenta FTS5 o la versión de SQLite embebida | https://nodejs.org/api/sqlite.html | **NOT_FOUND** (no mencionado) |
| El build de Node (`main`) define `SQLITE_ENABLE_FTS5` | https://github.com/nodejs/node/blob/main/deps/sqlite/sqlite.gyp | **VERIFIED como build config**, no como garantía de API |
| `better-sqlite3` es síncrono, MIT, con prebuilds para plataformas mayores | https://github.com/WiseLibs/better-sqlite3 | **VERIFIED** |
| `better-sqlite3` documenta WAL con ejemplo `db.pragma('journal_mode = WAL')` | https://github.com/WiseLibs/better-sqlite3 | **VERIFIED** |
| `better-sqlite3` compila con `SQLITE_ENABLE_FTS5` y bundlea SQLite 3.53.4 | https://github.com/WiseLibs/better-sqlite3/blob/master/docs/compilation.md | **VERIFIED** |
| Afirmaciones de rendimiento de `better-sqlite3` | README del proyecto | **INCONCLUSIVE** — `vendor self-reported`, no reproducidas |
| `sqlite3` (TryGhost) es asíncrono y su repositorio se declara sin mantenimiento | https://github.com/TryGhost/node-sqlite3 | **VERIFIED** |
| WAL se activa con `PRAGMA journal_mode=WAL` y es persistente en el fichero | https://www.sqlite.org/wal.html | **VERIFIED** |
| WAL exige que todos los procesos estén en el mismo host; no funciona sobre sistemas de ficheros en red | https://www.sqlite.org/wal.html | **VERIFIED** |
| Las funciones JSON están integradas por defecto desde SQLite 3.38.0 | https://www.sqlite.org/json1.html | **VERIFIED** |
| ¿`node:sqlite` acepta `PRAGMA journal_mode=WAL` vía `exec()`? | — | **NOT_TESTED** (HIPÓTESIS) |
| Existencia de prebuild de `better-sqlite3` para el piso de Node elegido en Windows | — | **POR VERIFICAR** al implementar |
| `SQLITE_THREADSAFE` en el build de Node | https://github.com/nodejs/node/blob/main/deps/sqlite/sqlite.gyp | **INCONCLUSIVE** (no observado; no se afirma) |

---

## 4. FTS5 y español

### 4.1 Tokenizers que trae SQLite de serie

**HECHO VERIFICADO**, https://www.sqlite.org/fts5.html — FTS5 provee **cuatro** tokenizers integrados:

| Tokenizer | Qué hace | Aptitud para español |
|---|---|---|
| **`unicode61`** | **Por defecto.** Basado en Unicode 6.1. Case-folding según reglas Unicode 6.1. Por defecto son separadores todos los caracteres de espacio y puntuación, y son caracteres de token los de categorías generales que empiezan por "L" o "N", más "Co" | **Es la opción base.** Ver §4.2 |
| **`ascii`** | Como `unicode61` pero solo ASCII: todos los codepoints > 127 son **siempre** caracteres de token; case-folding solo ASCII ("A/a equivalentes, pero Ã/ã distintos"); **no soporta `remove_diacritics`** | **Inadecuado**: trataría `Á` y `á` como distintos |
| **`porter`** | Envuelve otro tokenizer (por defecto `unicode61`) y aplica el algoritmo de stemming de Porter. La doc dice que es **para inglés** y que "results with other languages may vary" | **NO usar en español** — así lo advierte la propia doc |
| **`trigram`** | Cada secuencia contigua de tres caracteres es un token; permite búsqueda de subcadena y `LIKE`/`GLOB` indexados. Opciones: `case_sensitive` (0 por defecto), `remove_diacritics` (0 por defecto; solo puede ser 1 si `case_sensitive` es 0). Subcadenas de menos de 3 caracteres no hacen match | Complementario, no sustituto. Ver §4.5 |

**Consecuencia dura y explícita: SQLite no trae stemmer de español de serie.** El único stemmer integrado es Porter para inglés. Buscar "notificar" no encontrará "notificaciones" con ningún tokenizer integrado.

### 4.2 `remove_diacritics` — existencia y semántica exacta

**HECHO VERIFICADO**, https://www.sqlite.org/fts5.html. La opción **existe**, pertenece a `unicode61`, acepta **0, 1 o 2**, y **su valor por defecto es 1**:

| Valor | Semántica documentada |
|---|---|
| **0** | No se eliminan diacríticos |
| **1** | Se eliminan los diacríticos de caracteres de escritura latina, **excepto** en el caso poco común de que un único codepoint Unicode represente un carácter con **múltiples** diacríticos (ejemplo citado por la doc: codepoint 0x1ED9). La doc lo califica de bug técnico que no puede corregirse sin romper compatibilidad hacia atrás |
| **2** | Los diacríticos se eliminan **correctamente de todos** los caracteres latinos |

Sintaxis, ejemplo de la doc oficial:

```sql
CREATE VIRTUAL TABLE ft USING fts5(a, b,
    tokenize = "unicode61 remove_diacritics 0 tokenchars '-_'"
);
```

Otras opciones de `unicode61` verificadas: `categories` (por defecto `"L* N* Co"`), `tokenchars` (caracteres adicionales a tratar como token), `separators` (caracteres adicionales a tratar como separador).

### 4.3 Mayúsculas y acentos en español: qué queda cubierto y qué no

**Cubierto por `unicode61`:**
- **Mayúsculas/minúsculas:** case-folding case-insensitive según Unicode 6.1. `DEMANDA` = `demanda`. **HECHO VERIFICADO.**
- **Acentos:** con `remove_diacritics 2`, `notificación` y `notificacion` producen el mismo token. **HECHO VERIFICADO** por la semántica documentada.

**NO cubierto, y hay que decirlo:**
- **Stemming en español.** Ver §4.1. No hay opción integrada.
- **`upper()` / `lower()` fuera de FTS5.** **HECHO VERIFICADO**, https://www.sqlite.org/lang_corefunc.html: "The default built-in lower() function works for ASCII characters only. To do case conversions on non-ASCII characters, load the ICU extension." Es decir: `lower('CAFÉ')` **no** normaliza la `É`. **RIESGO de inconsistencia:** el índice FTS5 sí normaliza y las comparaciones ordinarias con `=`/`LIKE`/`lower()` **no**. Dos rutas de búsqueda con semánticas distintas sobre el mismo texto.
- **No existe una función `unaccent` integrada** en SQLite. **VERIFIED por ausencia** en la doc de funciones core.

### 4.4 El problema de la eñe — RIESGO no resuelto por la documentación

**RIESGO / POR VERIFICAR.** La documentación de sqlite.org describe `remove_diacritics` como "eliminar diacríticos de caracteres latinos", pero **no enumera** qué codepoints trata. En español esto importa de forma específica:

- La **`ñ`** es, en Unicode, `n` con tilde combinable (`U+00F1` descompone a `n` + `U+0303`). Si `remove_diacritics` la trata como diacrítico, **`año` y `ano` se indexarían con el mismo token**. En lenguaje jurídico y cotidiano en español eso produce colisiones desafortunadas y, más relevante para el producto, degrada la precisión de búsqueda.
- La **`ü`** de "argüir"/"bilingüe" también se normalizaría a `u`, lo cual es **deseable**.

**Estado: HIPÓTESIS no confirmada por fuente.** La doc oficial no lo especifica y **no se ejecutó ninguna prueba** (§9). No se afirma en qué sentido se comporta.

**Spike requerido antes de fijar el esquema FTS** (a escribir bajo `experiments/`, marcado `NON-PRODUCTION SPIKE`):

```text
Objetivo: determinar el comportamiento real de unicode61 remove_diacritics {0,1,2}
          sobre el conjunto de caracteres del español.
Corpus mínimo: ñ Ñ á é í ó ú Á É Í Ó Ú ü Ü ¿ ¡ ºª — guiones, apóstrofos,
               y términos jurídicos reales: "año", "ano", "peña", "pena",
               "señor", "senor", "bilingüe", "bilingue".
Método: CREATE VIRTUAL TABLE con cada valor; consultar y comparar tokens
        (fts5vocab o la tabla auxiliar de términos).
Salida esperada: matriz carácter × valor de remove_diacritics.
Etiqueta obligatoria del resultado: "observed in current environment",
        NUNCA "documented platform guarantee".
```

**DECISIÓN PENDIENTE que depende del resultado:** si `ñ` colapsa a `n`, hay tres salidas posibles, todas con coste: (a) aceptar la colisión y documentarla; (b) usar `remove_diacritics 0` y perder la insensibilidad a acentos, compensando con una columna normalizada en la aplicación; (c) indexar dos columnas FTS con configuraciones distintas. **No se propone ninguna hasta tener el dato**, porque proponerla ahora sería decidir sobre una hipótesis.

### 4.5 Nota sobre `trigram` como complemento

**HECHO VERIFICADO.** El tokenizer `trigram` permite búsqueda de subcadena y habilita `LIKE`/`GLOB` indexados (salvo si se activa `remove_diacritics`). Sus opciones son `case_sensitive` (0 por defecto) y `remove_diacritics` (0 por defecto, incompatible con `case_sensitive 1`). Subcadenas de menos de 3 caracteres no hacen match en consultas full-text.

**PROPUESTA:** considerarlo **complemento**, no sustituto, para el caso de buscar fragmentos como números de radicado o identificadores dentro de texto. **Fuera del alcance de la decisión de V0**; se anota para que no se reinvestigue.

### 4.6 Nota sobre la versión de Unicode

**HECHO VERIFICADO / RIESGO menor.** `unicode61` está basado en **Unicode 6.1**, una versión antigua del estándar. Para el repertorio de caracteres del español (latín básico + suplemento latino-1) esto **no debería** suponer diferencia, porque esos bloques son estables desde hace décadas. Se registra como **HIPÓTESIS** y no como hecho, porque no se verificó carácter por carácter.

### 4.7 Implicación arquitectónica: la configuración FTS es parte del contrato de datos

**PROPUESTA DEL TECHNICAL DESIGN — invariante a registrar.**

> La cláusula `tokenize` de una tabla FTS5 se fija **en el `CREATE VIRTUAL TABLE`** y determina cómo se tokenizó todo lo ya indexado. Cambiarla **no** reindexará el contenido existente. Por tanto, la configuración de tokenizer del índice de búsqueda de un `case.db` es **parte del contrato de datos persistido**, no un parámetro de configuración ajustable.

Consecuencias:
1. La configuración efectiva de tokenizer debe **persistirse y versionarse** en el `case.db` (p. ej. en la tabla de metadatos de esquema), de forma que el Core sepa con qué semántica se indexó un caso antiguo.
2. Cambiarla en el futuro exige una **migración con reindexación completa**, que es un evento de `provenance_kind = SYSTEM` con `principal_type = SYSTEM` (kernel §1.4) y que avanza `case_revision`.
3. **Refuerza la condición `SEARCH_INCONCLUSIVE`** del catálogo epistémico (kernel §10): si la búsqueda de un caso corre con una configuración de tokenizer distinta de la actual, esa es una razón legítima y tipada para declarar la búsqueda no concluyente en lugar de devolver resultados silenciosamente peores.

**Este punto no lo pedía el encargo pero sale directamente de los hechos verificados, y afecta al esquema de V0.**

### 4.8 Tabla de verificación — FTS5 y español

| Afirmación | Fuente oficial (URL) | Estado |
|---|---|---|
| FTS5 provee cuatro tokenizers integrados: `unicode61`, `ascii`, `porter`, `trigram` | https://www.sqlite.org/fts5.html | **VERIFIED** |
| `unicode61` es el tokenizer por defecto y hace case-folding según Unicode 6.1 | https://www.sqlite.org/fts5.html | **VERIFIED** |
| La opción `remove_diacritics` **existe** y acepta 0, 1 o 2 | https://www.sqlite.org/fts5.html | **VERIFIED** |
| El valor por defecto de `remove_diacritics` es 1 | https://www.sqlite.org/fts5.html | **VERIFIED** |
| `remove_diacritics 1` falla con codepoints de múltiples diacríticos (ej. 0x1ED9); es un bug conservado por compatibilidad | https://www.sqlite.org/fts5.html | **VERIFIED** |
| `remove_diacritics 2` elimina diacríticos correctamente de todos los caracteres latinos | https://www.sqlite.org/fts5.html | **VERIFIED** |
| `unicode61` admite además `categories`, `tokenchars`, `separators` | https://www.sqlite.org/fts5.html | **VERIFIED** |
| `ascii` no soporta `remove_diacritics` | https://www.sqlite.org/fts5.html | **VERIFIED** |
| `porter` es un stemmer de inglés; la doc advierte que otros idiomas "may vary" | https://www.sqlite.org/fts5.html | **VERIFIED** |
| SQLite **no** trae stemmer de español de serie | https://www.sqlite.org/fts5.html | **VERIFIED por ausencia** |
| `trigram`: `case_sensitive` (def. 0) y `remove_diacritics` (def. 0, incompatible con `case_sensitive 1`) | https://www.sqlite.org/fts5.html | **VERIFIED** |
| FTS5 existe desde SQLite 3.9.0; deshabilitado por defecto en el árbol de fuentes, habilitado en la amalgamation | https://www.sqlite.org/fts5.html | **VERIFIED** |
| `lower()`/`upper()` integrados operan **solo sobre ASCII**; hace falta la extensión ICU para el resto | https://www.sqlite.org/lang_corefunc.html | **VERIFIED** |
| SQLite no tiene función `unaccent` integrada | https://www.sqlite.org/lang_corefunc.html | **VERIFIED por ausencia** |
| Comportamiento de `remove_diacritics` sobre `ñ` (¿colapsa a `n`?) | — | **NOT_FOUND / NOT_TESTED** — ver §4.4 |
| Unicode 6.1 cubre sin diferencias el repertorio del español | — | **INCONCLUSIVE** (HIPÓTESIS, no verificada carácter a carácter) |
| Cambiar `tokenize` no reindexa el contenido existente | https://www.sqlite.org/fts5.html | **HIPÓTESIS** derivada del contrato de `CREATE VIRTUAL TABLE`; **POR VERIFICAR** |

---

## 5. Estado del entorno de desarrollo actual

**`observed in current environment` — NO es una garantía de plataforma.** Sonda ejecutada el 2026-08-24 en la máquina de trabajo (Windows 11):

```text
node --version   ->  v20.19.0
npm --version    ->  11.10.1
typeof crypto.randomUUID     ->  'function'
typeof crypto.randomUUIDv7   ->  'undefined'
require('node:sqlite')       ->  ERR_UNKNOWN_BUILTIN_MODULE
```

**Lectura, y RIESGO inmediato:**
1. **La máquina de desarrollo corre Node 20.19.0, una línea que alcanzó End-of-Life el 2026-04-30** según §1.4. **RIESGO:** desarrollar sobre una línea EOL significa desarrollar sin parches de seguridad y contra un runtime distinto del de destino.
2. Coherente con §2.2.2 y §3.2: en esta versión **no existe** `crypto.randomUUIDv7` ni el módulo `node:sqlite`. Ambas ausencias son la consecuencia esperada, y **confirman por vía independiente** que las dos capacidades están acotadas por versión.
3. **ACCIÓN REQUERIDA antes de implementar:** actualizar el entorno de desarrollo a la línea que se apruebe en §1.6/§2.8, y fijarla con `.nvmrc` o equivalente + `package.json#engines`.

**Lo que estas tres líneas NO demuestran:** nada sobre cómo se comportan esas APIs donde sí existen. Una ausencia observada confirma una ausencia documentada; una presencia observada no confirmaría ninguna garantía.

---

## 6. Implicaciones arquitectónicas consolidadas

1. **`event_seq` es el orden canónico; el identificador nunca lo es.** (§2.6) La ordenabilidad de UUIDv7 es localidad de índice, no verdad. Node documenta explícitamente que el timestamp embebido no es estrictamente creciente.
2. **Dos puertos separados para identidad y contenido:** `IdGenerator` (UUIDv7) y `ContentHasher` (SHA-256). Nunca uno solo. (§2.7, kernel §11)
3. **El puerto de persistencia es asíncrono aunque ambos drivers verificados sean síncronos**, por asimetría de coste de cambio. (§3.7)
4. **La ubicación física del `case.db` es una restricción de integridad, no una preferencia**: WAL no funciona sobre sistemas de ficheros en red ni tolera carpetas sincronizadas. (§3.5)
5. **La configuración del tokenizer FTS5 es parte del contrato de datos persistido** y debe versionarse en el `case.db`; cambiarla exige migración con reindexación. Alimenta `SEARCH_INCONCLUSIVE`. (§4.7)
6. **No hay stemming de español disponible de serie.** Cualquier expectativa de producto sobre "buscar por raíz" debe declararse fuera de V0 o resolverse en la capa de aplicación. (§4.1)
7. **El piso de Node deja de ser una preferencia y pasa a ser una consecuencia** de la elección de identidad: UUIDv7 nativo implica `>= 24.16.0`. (§2.8)

---

## 7. Decisiones de dependencia que los dueños deben aprobar

| # | Decisión | Propuesta | Coste que se acepta | Estado |
|---|---|---|---|---|
| **D-1** | Regla de versión de Node: piso mínimo en `engines`, determinado en implementación contra `schedule.json`, nunca versión congelada en documentación | Aprobar la **regla**, no una versión | Requiere un chequeo en CI contra `schedule.json` | **DECISIÓN PENDIENTE** |
| **D-2** | Identidad de entidad = **UUIDv7** (confirma kernel §11, cierra la alternativa ULID) | **UUIDv7** | 36 caracteres frente a 26 de ULID; irrelevante para ids opacos | **DECISIÓN PENDIENTE** |
| **D-3** | Generación de UUIDv7 vía `crypto.randomUUIDv7()` **nativo**, con piso `>= 24.16.0` (Camino A de §2.8) | **Camino A** | Excluye la línea 22.x (Maintenance LTS, EOL 2027-04-30) | **DECISIÓN PENDIENTE** |
| **D-4** | Invariante: el orden canónico es `event_seq`; **prohibido** ordenar por identificador | Aprobar como invariante del kernel | Ninguno; formaliza lo ya implícito | **DECISIÓN PENDIENTE** |
| **D-5** | Driver SQLite para V0 = **`better-sqlite3`**, detrás del puerto de §3.7 | `better-sqlite3` | Dependencia nativa; riesgo de instalación en Windows sin prebuild | **DECISIÓN PENDIENTE** |
| **D-6** | Condición de reversión a `node:sqlite`: cuando su doc oficial muestre **Stability 2 - Stable** en la línea LTS en uso | Aprobar el criterio | Ninguno; hace la decisión revisable con un test objetivo | **DECISIÓN PENDIENTE** |
| **D-7** | El puerto de persistencia expone contrato **asíncrono** aunque el driver sea síncrono | Aprobar | Un envoltorio trivial por operación | **DECISIÓN PENDIENTE** |
| **D-8** | El Core **rechaza** (no solo advierte) abrir un `case.db` en ubicación de red o carpeta sincronizada | **Rechazar**, por coherencia con PF-002 | Fricción para usuarias que guardan todo en OneDrive; exige mensaje UX de categoría `CANNOT_DO_THAT` | **DECISIÓN PENDIENTE** |
| **D-9** | La configuración del tokenizer FTS5 se persiste y versiona en el `case.db` | Aprobar | Una tabla de metadatos de esquema | **DECISIÓN PENDIENTE** |
| **D-10** | `sqlite3` (TryGhost) queda **descartada** por estar declarada sin mantenimiento | Descartar | Ninguno | **PROPUESTA, sin objeción prevista** |
| **D-11** | Valor de `remove_diacritics` para el índice FTS5 en español | **No se propone valor** hasta ejecutar el spike de §4.4 | Bloquea el esquema FTS hasta tener el dato | **BLOQUEADA POR DATO** |

---

## 8. Qué queda POR VERIFICAR en el momento de implementar

Lista ejecutable. Cada punto debe resolverse **contra fuente viva**, no contra este documento.

| # | Qué verificar | Contra qué fuente | Por qué no se puede fijar ahora |
|---|---|---|---|
| V-1 | Estado LTS vigente de cada línea de Node | `https://raw.githubusercontent.com/nodejs/Release/main/schedule.json` | El calendario avanza; 24.x pasa a Maintenance el 2026-10-20 |
| V-2 | Que la versión concreta del piso incluya `crypto.randomUUIDv7` | `nodejs.org/docs/latest-vXX.x/api/crypto.html` + `node -p "typeof require('crypto').randomUUIDv7"` | Es una retroportación reciente; no toda 24.x la tiene, solo `>= 24.16.0` |
| V-3 | Estabilidad actual de `node:sqlite` (¿llegó a Stability 2?) | `https://nodejs.org/api/sqlite.html` | Es RC; puede pasar a estable y disparar D-6 |
| V-4 | Existencia de prebuild de `better-sqlite3` para (piso de Node × `win32-x64` × `win32-arm64`) | Releases del repo / `npm install` en máquina limpia | Depende del ABI de la versión de Node elegida |
| V-5 | Versión de SQLite embebida en el driver elegido | `SELECT sqlite_version();` | No documentada por `node:sqlite`; puede cambiar en `better-sqlite3` |
| V-6 | Que FTS5 esté realmente compilado en el binario elegido | `SELECT sqlite_compileoption_used('ENABLE_FTS5');` o crear una tabla FTS5 de prueba | El define observado es de la rama `main` de Node, no de una release |
| V-7 | Que `PRAGMA journal_mode=WAL` devuelva `wal` con el driver elegido | Ejecutar el pragma y leer el valor devuelto | No documentado para `node:sqlite` |
| V-8 | Comportamiento de `remove_diacritics {0,1,2}` sobre `ñ`, `ü` y el resto del repertorio español | Spike de §4.4 bajo `experiments/`, `NON-PRODUCTION SPIKE` | La doc de sqlite.org no enumera codepoints; desbloquea D-11 |
| V-9 | Que cambiar `tokenize` no reindexa contenido existente | Spike bajo `experiments/` | Deducido del contrato de `CREATE VIRTUAL TABLE`, no leído literalmente |
| V-10 | Método fiable de detección de carpeta sincronizada / unidad de red en Windows | Documentación de Microsoft | No existe API universal documentada; condiciona la viabilidad de D-8 |
| V-11 | Si `uuid@14` mantiene estado monótono intra-milisegundo | Doc de `uuidjs/uuid` | Solo relevante si se elige el Camino B de §2.8 |

---

## 9. Qué quedó NOT_TESTED o INCONCLUSIVE, y por qué

**Este spike fue documental, no experimental.** No se escribió ni ejecutó ningún spike bajo `experiments/`. La única ejecución fue la sonda de tres líneas de §5.

### 9.1 NOT_TESTED — no se ejecutó ninguna prueba

| Elemento | Por qué |
|---|---|
| Comportamiento de `remove_diacritics` sobre el repertorio español (§4.4) | Requiere un SQLite con FTS5 en ejecución; la máquina actual (Node 20.19.0) no tiene `node:sqlite` ni driver instalado. **Es el NOT_TESTED de mayor impacto**: bloquea D-11 y el esquema FTS |
| Que `node:sqlite` acepte `PRAGMA journal_mode=WAL` vía `exec()` (§3.5) | Módulo no disponible en el runtime local; y la doc oficial no lo afirma, así que no puede resolverse documentalmente |
| Instalación de `better-sqlite3` en Windows y disponibilidad de prebuild (§3.3) | Habría requerido instalar dependencias en el workspace; fuera del alcance de un spike documental |
| Que FTS5 esté compilado en un binario de release de Node (§3.6) | El define solo se verificó en el fichero de build de la rama `main` |
| Comportamiento monótono intra-milisegundo de `crypto.randomUUIDv7()` (§2.3) | El runtime local no tiene la API; y ninguna prueba local demostraría una garantía de plataforma aunque la tuviera |
| Que cambiar `tokenize` no reindexe (§4.7) | Deducción del contrato, no verificada |
| Detección de carpetas sincronizadas en Windows (§3.5, punto 3) | Ni siquiera se identificó una fuente documental; queda abierto |

### 9.2 INCONCLUSIVE — se buscó fuente y no resolvió

| Elemento | Por qué quedó sin resolver |
|---|---|
| Etiquetas de estado LTS en `nodejs.org/en/about/previous-releases` (§1.5) | La extracción devolvió etiquetas mutuamente contradictorias. Se resolvió usando la fuente autoritativa (`nodejs/Release`) y se dejó constancia de la discrepancia en vez de ocultarla |
| Afirmaciones de rendimiento de `better-sqlite3` (§3.3) | Son `vendor self-reported`, y además la extracción produjo un resultado incoherente que invertía el sentido de la comparación. **Deliberadamente no reproducidas.** Ninguna decisión se apoya en rendimiento |
| Si `uuid@14` mantiene estado monótono interno (§2.3) | Hay indicios fuertes en el changelog (`updateV7State`, refactor de estado interno de v7) pero la documentación **no lo afirma**. Los indicios de changelog no son documentación de API |
| `SQLITE_THREADSAFE` en el build de Node (§3.6) | No se observó el define; su ausencia significa "valor por defecto", que no se verificó. No se afirma nada |
| Que Unicode 6.1 cubra sin diferencias el repertorio español (§4.6) | Plausible, no verificado carácter a carácter |
| Madurez de `uuidv7-js` (§2.3) | Apareció en resultados de búsqueda; no se abrió su documentación. No se evaluó porque el Camino A lo hace innecesario |

### 9.3 NOT_FOUND — la documentación oficial simplemente no lo dice

| Elemento | Dónde se buscó |
|---|---|
| WAL en la documentación de `node:sqlite` | https://nodejs.org/api/sqlite.html |
| FTS5 en la documentación de `node:sqlite` | https://nodejs.org/api/sqlite.html |
| Versión de SQLite embebida en `node:sqlite` | https://nodejs.org/api/sqlite.html |
| Si `crypto.randomUUIDv7()` implementa contador monótono intra-ms | https://nodejs.org/api/crypto.html y el commit de implementación |
| Qué codepoints exactos trata `remove_diacritics` | https://www.sqlite.org/fts5.html |
| Función `unaccent` integrada en SQLite | https://www.sqlite.org/lang_corefunc.html |

---

## 10. Índice de fuentes citadas

**Documentación oficial primaria — única autoridad de este documento:**

- Node.js — calendario y política de releases: https://github.com/nodejs/Release · https://nodejs.org/en/about/previous-releases
- Node.js — índice de estabilidad: https://nodejs.org/api/documentation.html#stability-index
- Node.js — `node:crypto`: https://nodejs.org/api/crypto.html · https://nodejs.org/docs/latest-v24.x/api/crypto.html · https://nodejs.org/docs/latest-v22.x/api/crypto.html
- Node.js — `node:sqlite`: https://nodejs.org/api/sqlite.html · https://nodejs.org/docs/latest-v22.x/api/sqlite.html
- Node.js — releases y changelogs: https://github.com/nodejs/node/releases/tag/v26.1.0 · https://nodejs.org/en/blog/release/v24.16.0
- Node.js — commits de implementación y documentación: https://github.com/nodejs/node/commit/b267f6bca3 · https://github.com/nodejs/node/commit/1684ab8ff8
- Node.js — build de SQLite: https://github.com/nodejs/node/blob/main/deps/sqlite/sqlite.gyp
- IETF — RFC 9562: https://www.rfc-editor.org/info/rfc9562 · https://www.rfc-editor.org/rfc/rfc9562.html
- SQLite — FTS5: https://www.sqlite.org/fts5.html
- SQLite — WAL: https://www.sqlite.org/wal.html
- SQLite — funciones core: https://www.sqlite.org/lang_corefunc.html
- SQLite — JSON: https://www.sqlite.org/json1.html
- `uuidjs/uuid`: https://github.com/uuidjs/uuid · https://github.com/uuidjs/uuid/blob/main/CHANGELOG.md
- `WiseLibs/better-sqlite3`: https://github.com/WiseLibs/better-sqlite3 · https://github.com/WiseLibs/better-sqlite3/blob/master/docs/compilation.md
- `TryGhost/node-sqlite3`: https://github.com/TryGhost/node-sqlite3
- `ulid/spec`: https://github.com/ulid/spec

**Fuentes NO autoritativas usadas:** ninguna. No se citó ningún blog de terceros. Los resultados de búsqueda web se usaron exclusivamente para **localizar** documentación oficial, nunca como autoridad; toda afirmación etiquetada VERIFIED se leyó en la fuente oficial correspondiente.

**Advertencia final de caducidad:** todas las verificaciones se hicieron el **2026-08-24**. Las páginas web cambian. Este documento es una **observación fechada** (nivel 6 de precedencia, kernel §14), no una garantía. Antes de implementar, ejecutar la lista de §8.
