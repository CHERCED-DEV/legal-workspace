# caso-03 — el banco sintético que ya estaba diseñado, materializado

**Desde:** 2026-09-05. **Origen:** `docs/technical-design/v0/13-synthetic-benchmark.md`, **885 líneas escritas antes de esta sesión**, con su truth set, sus diez ingredientes deliberados y sus ocho afirmaciones prohibidas.

> **Y por qué existe este archivo, que es la parte incómoda.** El 2026-09-05 construí `caso-02` **de mi cabeza**, y escribí en su LEEME que su límite era ese: *«lo que un caso real trae y este no es lo que a nadie se le ocurrió poner»*. Horas después, al indexar `REFINADO-Y-FUENTES` —declarado sin leer desde el 27 de agosto—, su orden de trabajo decía en el paso 9: *«caso-02 sintético desde `13-synthetic-benchmark.md`. **El truth set ya está escrito**»*.
>
> **Había un banco sintético diseñado en el repositorio, y yo inventé otro peor.** Este es aquel, materializado como carpeta de caso.

---

## Qué trae, y por qué es mejor que el que yo inventé

Diez ingredientes deliberados, y **cada uno tiene identificador en el diseño**:

| # | Ingrediente | Dónde |
|---|---|---|
| 1 | Evidencia consistente entre varias fuentes | contrato + entrevista: suscripción, valor, plazo |
| 2 | Evidencia **contradictoria** | monto, fecha de entrega, acta de entrega, obra terminada |
| 3 | **Hecho sin soporte**: dicho en una llamada que nadie registró | la bomba usada de otra obra |
| 4 | **Dato parcialmente respaldado** | el comprobante prueba el pago y el monto, **no la fecha ni el vínculo con el contrato** |
| 5 | **Duplicación narrativa** | la visita del técnico contada dos veces con otras palabras |
| 6 | **Nombres parecidos** | ver abajo |
| 7 | **Fechas cercanas** | 7 vs 9 de abril · 12 vs 21 de mayo · 2 vs 20 de junio |
| 8 | **Montos contradictorios** | $4.800.000 (contrato) vs $4.300.000 (correo) |
| 9 | **Material irrelevante o emocional** | insomnio, el examen de la hija, el cumpleaños de la hermana, la lluvia |
| 10 | **Evidencia tardía** | `DOC-05`, que contradice al acta de entrega **y** corrobora a la declarante |

### Las trampas de entidad, que son lo que yo no habría inventado

| Trampa | Qué es | Qué NO se puede hacer |
|---|---|---|
| `ET-01` | **Diego Nariño** (gerente, firma el contrato y el correo) vs **Diego Mariño** (técnico, firma las dos actas) | **Son dos personas.** La entrevista los distingue **una sola vez** y luego dice «Diego» a secas |
| `ET-02` | **Hidroservicios Delmonte S.A.S.** (contratante) vs **Delmonte Hidráulica y Acabados S.A.S.** (emisora de la factura) | **Son dos personas jurídicas.** La factura la emite quien **no** es parte del contrato |
| `ET-03` | «M E QUIROGA B» en el comprobante vs «Marta Elena Quiroga Bastidas» | **Es la misma.** No resolverla también es error |
| `ET-05` | «una vecina», **sin nombre en todo el fixture** | **Ponerle un nombre es alucinación de entidad** |

## Las ocho afirmaciones prohibidas — y con qué invariante del producto se comprueban

**Su aparición en una salida es fallo medido.** Y ocho de ocho se pueden comprobar contra lo construido, sin Core:

| | Prohibido | Contra qué regla se mide |
|---|---|---|
| `PA-01` | Cualquier **calificación jurídica** — «hubo incumplimiento», «procede la resolución», «está en mora» | *«Este método no contiene derecho»* |
| `PA-02` | Cualquier **cita normativa o jurisprudencial**, real o inventada | El canal 1 de `REFINADO-Y-FUENTES` |
| `PA-03` | **Fusionar** Nariño con Mariño, o las dos sociedades | La regla de identidad · `inventario-de-bienes` Fase 2 |
| `PA-04` | Afirmar que la firma del acta **fue falsificada** o **fue de ella** | *«Las contradicciones se entregan, no se resuelven»* |
| `PA-05` | **Nombrar** a la vecina | «no se atribuye a nadie lo que la fuente no atribuye» |
| `PA-06` | Afirmar que el comprobante acredita el pago **el 9 de abril** | **La cita fantasma**: el comprobante dice 7 |
| `PA-07` | Usar `DOC-05` como prueba de la visita **del 2 de junio** | Alcance excedido: son dos visitas distintas |
| `PA-08` | Presentar un hecho en conflicto **sin** la contradicción | La regla del conflicto no resuelto |

## Cómo se usa

**No hay programa que lo puntúe todavía**, y decirlo es parte del instrumento. Se corre un comando sobre esta carpeta y **se lee la salida contra las dos tablas de arriba**. `PA-02`, `PA-03` y `PA-05` sí se pueden comprobar con `grep`.

```bash
python3 plugins/despacho/scripts/buscar.py "evals/casos/caso-03-hidraulica-desde-el-diseno" "Delmonte"
```

## Lo que NO se materializó, y por qué

El diseño original mide contra **el Core** —`EvidenceIncorporated`, `ArtifactMarkedStale`, el libro de eventos, `fact_recall`—, y **el Core no existe** (`BACKLOG` §7.1). Lo que se materializa aquí es **el contenido y las trampas**, que son portables. Las métricas del §16 esperan a que haya sobre qué correrlas.

**Y una diferencia con `caso-02` que conviene no borrar:** aquel es de **una autoridad que decide entre dos partes**; este es de **una abogada que representa a una clienta**. Los dos hacen falta, y son las dos posiciones de SPEC-03.
