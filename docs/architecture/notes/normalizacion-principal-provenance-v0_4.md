# Nota de normalización — `Principal` frente a `provenance_kind` (v0.4)

**Origen:** corrección semántica ordenada por los dueños (prompt de Technical Design V0, §3).
**Estado:** normativa. Aplica a todo el corpus. No destruye información histórica.
**Registro de supersedes:** ítem **§16.13** (continúa el registro del addendum v0.3 §C).

---

## 1. El defecto corregido

El corpus previo usaba un solo campo, `actor_type`, para responder dos preguntas distintas:

- *¿quién ejecutó la operación?* — pregunta **operacional**;
- *¿cuál es la naturaleza epistemológica del origen de esto?* — pregunta **epistémica**.

El síntoma visible fue la expresión `actor_type = HUMAN_DECISION`, que mezcla ambas: "decisión humana" no es un tipo de actor, es una **clase de procedencia**. El mismo colapso hacía imposible expresar sin ambigüedad casos legítimos como "el sistema ejecutó la incorporación de un material cuyo origen es externo".

## 2. La separación

### `Principal` — quién ejecutó

```text
Principal
  principal_id      identificador opaco y estable
  principal_type    HUMAN | AI | SYSTEM
  principal_role    rol funcional en la organización (v0: 'lawyer')
```

Acompaña a toda operación, evento y registro de auditoría.

### `provenance_kind` — naturaleza epistemológica del origen

```text
EXTERNAL_SOURCE | AI_DERIVATION | AI_INFERENCE | HUMAN_DECISION | SYSTEM
```

Acompaña a toda entidad epistémica, dentro de su `ProvenanceRecord`.

## 3. Por qué `principal_type` no incluye `EXTERNAL`

Los dueños propusieron `HUMAN | AI | SYSTEM | EXTERNAL` y autorizaron proponer algo mejor.

Un *principal* es quien **invoca** una operación contra el Core. Un tercero externo —la contraparte que envió un correo, la autoridad que emitió un oficio— nunca invoca nada en este sistema: aparece como **origen del material**, que es exactamente lo que `provenance_kind = EXTERNAL_SOURCE` ya expresa, junto con los metadatos de origen declarado en el sobre de incorporación.

Admitir `EXTERNAL` como `principal_type` produciría registros de auditoría cuyo ejecutor no ejecutó nada, y reintroduciría por la puerta de atrás la mezcla que esta normalización elimina. Cuando haya que registrar de quién procede un material, se usa `declared_origin` en la incorporación; el principal de esa operación es la profesional que incorpora (`HUMAN`) o el proceso que lo hace en su nombre (`SYSTEM`).

**Estado:** `PROPUESTA DEL TECHNICAL DESIGN`, pendiente de ratificación por los dueños.

## 4. Combinaciones válidas

Las dos dimensiones son ortogonales, pero no toda combinación tiene sentido:

| `provenance_kind` | `principal_type` admisible | Ejemplo |
|---|---|---|
| `EXTERNAL_SOURCE` | `HUMAN`, `SYSTEM` | La profesional incorpora un contrato recibido |
| `AI_DERIVATION` | `AI`, `SYSTEM` | Transcripción generada a partir del audio |
| `AI_INFERENCE` | `AI` | Hecho candidato propuesto por el modelo |
| `HUMAN_DECISION` | `HUMAN` | Aprobación de un ProposalItem |
| `SYSTEM` | `SYSTEM` | Regeneración de una proyección, migración |

**Invariante comprobable:** `provenance_kind = HUMAN_DECISION` exige `principal_type = HUMAN`. Ningún principal de tipo `AI` puede producir procedencia `HUMAN_DECISION`. Esta es la formulación correcta de lo que el corpus previo escribía como `actor_type = HUMAN_DECISION`.

## 5. Tabla de equivalencias (para leer documentos anteriores)

| Escritura previa | Escritura normalizada |
|---|---|
| `actor_id` | `principal_id` |
| `actor_type` en uso operacional (`HUMAN`, `AI`, `SYSTEM`) | `principal_type` |
| `actor_type = HUMAN_DECISION` | `provenance_kind = HUMAN_DECISION` **y** `principal_type = HUMAN` |
| `actor_role` | `principal_role` |
| `actor_type ∈ EXTERNAL_SOURCE \| AI_DERIVATION \| AI_INFERENCE \| HUMAN_DECISION \| SYSTEM` | `provenance_kind` con ese mismo enum |
| "la triple `actor_id, actor_type, actor_role`" | "el `Principal`" |

Los documentos anteriores conservan su texto histórico; esta tabla permite leerlos sin ambigüedad. La corrección de `actor_type = HUMAN` a `HUMAN_DECISION` registrada en el addendum v0.3 §B.1 (supersede §16.7) queda **subsumida** por esta normalización: aquel arreglo trataba el síntoma —un valor fuera del enum— y esta nota corrige la causa —dos preguntas en un solo campo—. El valor correcto para el campo epistémico sigue siendo `HUMAN_DECISION`; lo que cambia es que ese campo ya no se llama `actor_type` sino `provenance_kind`, y que junto a él viaja un `Principal` con su propio tipo.

## 6. Documentos afectados

`ADR-003`, `ADR-005`, `docs/domain/glossary.md`, `docs/architecture/vertical-slice-v0.md`, `docs/architecture/notes/kernel-consolidacion-v0_2.md`, `docs/architecture/notes/addendum-correcciones-v0_3.md`, y todo el Technical Design V0, que nace ya con la nomenclatura correcta.

Los ADRs **001–006 conservan su estado `Accepted`**: esta es una normalización de vocabulario que no altera ninguna decisión. Ninguna regla, invariante o frontera cambia de contenido; cambia cómo se nombra el campo que la expresa.
