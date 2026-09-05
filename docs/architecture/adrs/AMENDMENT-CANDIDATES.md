# ADR Amendment Candidates — enmiendas que requieren decisión de los dueños

> **AÑADIDO EL 2026-09-05 — hay un quinto candidato, y este está ABIERTO.** Las cuatro primeras son registro histórico; **AC-05 no**: nace de leer los ADR contra el código el 2026-09-05 y **espera decisión**. Ver el final de este documento.

**Estado de las cuatro primeras:** **APROBADAS POR LOS DUEÑOS.** Las cuatro enmiendas fueron aprobadas y **ya están aplicadas** a los ADRs correspondientes (001, 004, 005), que siguen `Accepted` con su texto enmendado y su supersede registrado. Este documento queda como **registro histórico** del análisis que las sustentó.

| Enmienda | ADR | Supersede | Estado |
|---|---|---|---|
| AC-01 autorización por item | ADR-005 | §16.17, §16.18 | **Aplicada** |
| AC-02 `event_seq` / `case_revision` | ADR-004, ADR-005 | §16.16, §16.19 | **Aplicada** |
| AC-03 ocho tools | ADR-001 | §16.14 | **Aplicada** |
| AC-04 `ProposalPreservedForReconciliation` sin productor | ADR-004 | §16.15 | **Aplicada** |
**Origen:** conflictos detectados durante el Technical Design V0 y declarados por los diseñadores en sus documentos, sin resolverlos unilateralmente.

Regla aplicada en todo el corpus: **por precedencia manda el ADR Accepted**; el Technical Design documenta el conflicto y deja el diseño neutral o fiel al ADR, según el caso. Nada se cambió en silencio.

---

## AC-01 — ADR-005: autorización por item (consecuencia directa de una decisión de ustedes)

**Este es el amendment más importante, y no nace de una discrepancia técnica: nace de una decisión suya.**

Cuando se aprobó ADR-005, la aprobación parcial de Proposals era `DECISIÓN PENDIENTE`; el ADR fijó por eso **una autorización por Proposal**, con `proposal_content_hash` y un campo `authorized_items[]` preparado pero no activado. En el prompt de Technical Design ustedes respondieron **Q1 = SÍ**: la aprobación parcial por item queda aprobada, cada ProposalItem tiene identidad estable y decisión propia.

Esa respuesta deja desactualizado a ADR-005 §2 e invariantes 4, 5 y 6.

| Aspecto | ADR-005 vigente | Enmienda propuesta |
|---|---|---|
| Granularidad | Una autorización por Proposal | **Una por ProposalItem**, agrupadas por `review_session_id` |
| Vínculo de contenido | `proposal_content_hash` | `item_content_hash` |
| Aprobación parcial | `authorized_items[]` preparado, no activado | Campo eliminado; la granularidad lo hace innecesario |
| Invariante 6 | «jamás commit parcial, degradado ni silencioso» | «jamás commit **no autorizado**, degradado ni silencioso» |
| Pregunta pendiente 1 | Abierta | **Resuelta afirmativamente** por Q1 |

**Por qué la forma por item y no la forma en bloque:** la invalidación pasa de total a quirúrgica. Si un item se edita tras la revisión, solo se invalida ese item; con autorización por Proposal, editar uno invalidaría la aprobación de todos los demás y penalizaría a la profesional por una corrección no relacionada. Además la forma por item **puede representar la semántica en bloque** (aprobar toda la Proposal son N autorizaciones), mientras que la inversa no es cierta.

**Sobre el invariante 6:** su letra actual, leída con aprobación parcial vigente, prohibiría exactamente el comportamiento que ustedes aprobaron. Lo que el invariante protege de verdad —que nada se commitee sin autorización válida, que ningún item se commitee a medias, que nada se degrade en silencio— se conserva íntegro con la reformulación.

**Discrepancia menor asociada:** `authorized_operation` toma valor `COMMIT_FACT` (singular) en el Technical Design y `COMMIT_FACTS` (plural) en ADR-005. Con autorización por item el singular es lo semánticamente correcto. Requiere ratificación.

---

## AC-02 — ADR-004 y ADR-005: separar `event_seq` de `case_revision`

Ya presentado en el kernel técnico §5 y desarrollado en `09-events-and-audit.md` §8.1. Ustedes lo pidieron explícitamente («reevalúa esto… si recomiendas modificarla, crea un ADR AMENDMENT CANDIDATE»).

**Vigente (Modelo A):** todo evento incrementa `CaseRevision`; `seq == revision`; `ProposalReviewed` avanza la revisión.

**Propuesto (Modelo B):** `event_seq` avanza en **todo** evento; `case_revision` avanza **solo** en eventos que mutan el estado epistémico canónico. `ProposalReviewed` avanza `event_seq` pero no `case_revision`.

**Argumento decisivo:** `case_revision` es el reloj de *lo que el expediente sabe*. Una revisión humana aún no commiteada no añade hechos, evidencia ni links: el expediente sabe exactamente lo mismo antes y después. Hacer avanzar ese reloj invalida análisis en vuelo que nada tienen que ver con la propuesta revisada, y produce la circularidad que ya obligó a una corrección en el addendum v0.3 (la autorización acababa portando *la revisión resultante de su propio acto de revisión*).

**Estado del diseño:** el esquema de persistencia (`04-persistence-model.md` §3.5) es **neutral**: sirve a los dos modelos sin cambio estructural. Bajo el Modelo A, `case_revision = event_seq` en todas las filas; bajo el Modelo B, `ProposalReviewed` lleva `case_revision` nulo. Decidir después no cuesta migración de esquema, pero sí decide la aritmética de los tests.

---

## AC-03 — ADR-001: tamaño de la superficie MCP (ocho tools frente a nueve)

**ADR-001 (Accepted) inv. 3 y validación 7 fijan literalmente nueve tools.** El kernel técnico retiró `register_artifact` por la regla de exposición —*una operación se expone solo si el modelo debe decidir cuándo ocurre; si es consecuencia necesaria de otra, es interna*— y quedaron ocho.

`FactAnalysis` es consecuencia necesaria de `propose_facts`. Exponer su registro abre dos formas de fallar (que el modelo olvide registrarlo, o que registre un artifact que no corresponde a ningún análisis real) sin aportar ninguna capacidad.

**Opciones:** (1) mantener nueve exponiendo `register_artifact`; (2) enmendar ADR-001 a ocho; (3) dejar la tool declarada en el contrato pero no expuesta al modelo.

**Recomendación:** opción 2. Es la coherente con el principio de superficie mínima que el propio ADR-001 defiende.

---

## AC-04 — ADR-004: el evento `ProposalPreservedForReconciliation`

La lista **cerrada** de eventos v0 de ADR-004 lo incluye; el kernel técnico lo omitió al reescribir la lista.

Hay además una cuestión de fondo: bajo el modelo de dos dimensiones (`review_decision` × `commit_state`), la preservación de una propuesta ante conflicto de revisión **no es un cambio de estado** — nada se descarta, la propuesta simplemente sigue viva. Emitir un evento por un commit *rechazado* registraría en el log canónico algo que no mutó nada, tensionando la biyección mutación↔evento.

**Opciones:** (1) mantener columna de estado y emitir el evento, fiel a ADR-004; (2) derivar el estado y conservar el evento solo como registro de auditoría del rechazo; (3) enmendar ADR-004: la preservación es la conducta por defecto, es derivada, y el evento queda sin productor en V0 igual que `FactWithdrawn`.

**Lo que hace el diseño mientras se decide:** no añade columna de estado (añadirla después es migración aditiva trivial) pero **sí admite el evento** en la validación de tipos, porque la lista de ADR-004 es cerrada y está Accepted.

---

## Resultado

Las cuatro fueron **APROBADAS**. Consecuencia principal para el corpus: el **Modelo B pasa a ser el vigente** (la revisión humana ya no avanza `case_revision`), la superficie MCP queda en **ocho tools**, la autorización es **por item** y `ProposalPreservedForReconciliation` queda **sin productor en v0**.

---

## Registro del procedimiento seguido (histórico)

Para cada enmienda basta una de estas tres respuestas:

- **APROBAR** — se enmienda el ADR, se actualiza el corpus y se registra el supersede.
- **RECHAZAR** — el ADR queda como está y el Technical Design se corrige para ser fiel a su letra.
- **APLAZAR** — se mantiene el diseño neutral donde lo es (AC-02 y AC-04 lo son; AC-01 y AC-03 no: bloquean el schema de autorizaciones y el manifiesto de tools respectivamente).

---

## AC-05 — ADR-016: dónde viven los derivados de máquina

**Estado: ABIERTO.** Propuesto el 2026-09-05. **No se aplica nada hasta que ustedes decidan**, por la misma regla que gobierna a los cuatro anteriores: los conflictos se declaran, no se resuelven unilateralmente.

### La pregunta original, y por qué ya no se puede contestar tal como está

**ADR-016, pregunta pendiente 3:**

> *«¿Dónde vive el texto extraído — zona 2 o zona 3 de ADR-012? Hoy se dejó en `2-Borradores/`, que es zona 2, y **probablemente esté mal**: es un derivado de material incorporado.»*

**En el producto construido no existe la zona 3.** Las zonas son del diseño de ADR-012 para un Core que no se construyó (ver `BACKLOG` §7.1): lo que hay en el disco son tres carpetas —`1-Documentos recibidos/`, `2-Borradores/`, `3-Para presentar/`— y nada más. **La pregunta, literalmente, no tiene respuesta posible hoy.**

### Pero el síntoma es real, y el 2026-09-05 se pudo medir

`2-Borradores/` guarda **tres cosas de naturaleza distinta**, y ninguna marca cuál es cuál:

| Qué hay | Quién lo produjo | Qué se puede hacer con ello |
|---|---|---|
| Hoja de hechos, cronología, inventarios | **El sistema** | Pista, nunca origen — salvo con la marca ` - REVISADO` |
| Borradores y notas de ella | **Ella** | Es suyo. Lo que escriba manda |
| `Texto de referencia - <fecha>.txt` | **Una máquina**, sin criterio | **Nunca se cita.** Sirve para saber en qué página mirar |

**Y la medida es esta: en un solo día, tres mecanismos distintos tuvieron que aprender a distinguirlas por su cuenta.**

1. **El índice de salidas** de SPEC-08, que deduce el comando por la convención de nombre.
2. **El clasificador de `buscar.py`**, que marca `<- NO es material del caso` todo lo que está fuera de `1-Documentos recibidos/`.
3. **La regla de la marca ` - REVISADO`**, que decide cuál de esos archivos puede usarse como fuente.

> **Tres mecanismos resolviendo la misma distinción por separado es la señal de que falta una decisión, no de que falten tres reglas.** Y los tres la resuelven **por inferencia** —por el nombre, por la carpeta— cuando podría estar dicha por la estructura.

### Las tres opciones, con lo que cuesta cada una

| | Qué es | A favor | En contra |
|---|---|---|---|
| **(a) Dejarlo como está** | Los tres mecanismos siguen infiriendo | Cuesta cero. Funciona hoy | **Cada mecanismo nuevo tendrá que aprenderlo otra vez**, y el cuarto puede aprenderlo distinto. Es deriva garantizada |
| **(b) Una subcarpeta `2-Borradores/derivados-de-maquina/`** | Los derivados salen del montón | **La distinción queda dicha por la estructura y no por inferencia.** Un mecanismo nuevo la hereda gratis. Y a ella le separa lo que no debe leer como borrador | Toca `preparar_material.py` y la mención del texto de referencia en seis `SKILL.md`. **Le cambia una carpeta a ella**, y eso no lo decidimos nosotros |
| **(c) Una convención de nombre** —prefijo fijo | Igual que (b) sin mover archivos | Más barato | Sigue siendo inferencia, solo que mejor. **No resuelve la causa** |

**Recomendación: (b)**, y con una condición — **preguntárselo a ella antes**, porque es su carpeta y ADR-012 q7 ya dice que la estructura de la zona de trabajo *«se valida con la profesional, no entre nosotros»*.

### Lo que esta enmienda haría con ADR-016

- **Cerrar la q3 tal como está** —zona 2 o zona 3— por **premisa inexistente**, igual que ADR-018 cerró la q2 de ADR-014.
- **Abrir en su lugar** la pregunta que sí tiene respuesta: *«¿los derivados de máquina se separan de los borradores dentro de `2-Borradores/`?»*.
- **No tocar ninguno de sus invariantes.** El límite del OCR —falla callándose, no se cita, la ausencia no es información— **sigue mandando entero**, esté el archivo donde esté.

### Y lo que no depende de ustedes

Independientemente de lo que decidan, **la distinción ya está escrita en los tres sitios** y con test donde se pudo (`evals/scripts/test_buscar.py`). Esta enmienda no arregla un defecto abierto: **evita el cuarto mecanismo.**

