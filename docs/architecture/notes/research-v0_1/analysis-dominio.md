## Hallazgos

1. **SÓLIDO — El núcleo epistemológico de la sección 15 es la idea más valiosa del documento.** Distinguir afirmación / evidencia / hecho candidato / hecho acreditado / inferencia ataca directamente el riesgo #3 de la sección 3 (confundir alegado con acreditado), que es el fallo más grave posible en este dominio. Es una decisión de dominio, no de prompts, y eso es correcto.

2. **SÓLIDO — La relación N:M hecho↔prueba con hechos sin soporte (sección 5.1).** Refleja la práctica real ("hecho, prueba" es la presentación, no el modelo) y evitar el 1:1 ingenuo es acertado. Falta, sin embargo, elevarla a entidad de primera clase (ver Respuesta 2).

3. **REFINAR — Desalineación entre la lista de entidades (sección 8) y el modelo epistemológico (sección 15).** La sección 15 exige Afirmación, Inferencia, Contradicción y Vacío; ninguna aparece en la lista de entidades de la sección 8. A la inversa, la sección 8 tiene `Statement` y `Fact` sin definir su relación con "Afirmación". Si el modelo epistemológico es el corazón del sistema, las entidades deben derivarse de él, no coexistir en paralelo.

4. **REFINAR — Solapamiento `Fact` / `Event` / `Statement` sin semántica definida.** Un `Event` (ocurrencia en el mundo) y un `Fact` (proposición sobre esa ocurrencia con estatus epistémico) son cosas distintas; el documento no dice cuál es cuál. RIESGO de que el equipo los use de forma intercambiable y el estatus epistémico termine adherido al objeto equivocado.

5. **REFINAR — `Decision` está sobrecargado.** Puede significar: (a) providencia de la autoridad (contexto B), (b) decisión profesional interna que acredita un hecho (contexto A), (c) decisión estratégica del caso. Son tres conceptos con reglas y trazabilidad distintas. Un solo nombre garantiza confusión.

6. **RIESGO — El estatus epistémico como campo mutable.** El documento habla de hechos "alegados/acreditados/controvertidos" (sección 14) como categorías de memoria, pero no establece que la transición de estado sea un evento registrado y no una sobrescritura. Si `status` es un campo que se pisa, se pierde exactamente la trazabilidad que la sección 16 exige.

7. **RIESGO — "Controvertido" es ambiguo.** Puede ser un estado derivado (existe prueba a favor y en contra) o un estado procesal (la contraparte lo negó en la contestación). En derecho procesal son cosas distintas con consecuencias distintas. NO TENEMOS INFORMACIÓN SUFICIENTE sobre cuál necesita la usuaria; el modelo debe soportar ambos sin colapsarlos.

8. **RIESGO — La neutralidad del contexto B no tiene mecanismo estructural en el documento.** La sección 5.2 lista propiedades deseables (neutralidad, contradicción, valoración equilibrada) y la sección 24 las reduce a `role.type: decision_maker` en YAML que "modifica comportamiento". Si ese comportamiento se implementa como variación de prompt, la neutralidad es una sugerencia, no una propiedad. Contradice el propio principio de la sección 12 ("no prohibir solo mediante prompt").

9. **RIESGO — Procedencia humana sin identidad.** La sección 15 exige validación profesional para acreditar, pero en un sistema local mono-usuario "decisión humana" puede degradar a "alguien hizo clic". El documento no define qué constituye un actor humano identificado. Esto no requiere criptografía en v0, pero requiere decisión explícita.

10. **REFINAR — Faltan entidades que el propio documento implica:** vínculo hecho↔prueba con polaridad (secciones 5.1 y 15), Contradicción y Vacío (sección 15), términos/plazos procesales (implícitos en "responder de acuerdo con la etapa procesal", sección 5.1), y el registro de procedencia como concepto transversal (sección 14: "conocimiento con procedencia"). `Party` además debería ser la relación Persona/Organización↔Caso con rol, no una entidad paralela a `Person`.

11. **PREMATURO — Modelar a fondo `Hypothesis`, `Argument` y `LegalIssue` antes del vertical slice.** El slice (sección 34) no los necesita; su semántica depende de observar más trabajo real. Mantenerlos como nombres reservados, no diseñarlos ahora.

12. **PREMATURO — Máquina de estados epistémicos configurable por jurisdicción en v0.** Es la dirección correcta a largo plazo (Knowledge Packs), pero para el slice basta un vocabulario fijo con historia append-only; configurar lo que aún no se comprende produce el "modelo universal sobreabstracto" que la pregunta 1 teme.

---

## Respuestas

### 1. ¿El conjunto de entidades es suficiente y agnóstico sin sobreabstraerse?

**No es suficiente tal como está, y el riesgo principal no es la sobreabstracción sino la incoherencia interna** (hallazgo 3). Ajustes concretos:

**Falta:**
- `Assertion` (o unificar con `Statement`, ver Respuesta 2) — exigida por la sección 15.
- `EvidenceLink` (hecho↔evidencia con polaridad) — la relación N:M es el corazón del caso de uso "hecho, prueba" y debe ser entidad, no tabla implícita.
- `Contradiction` y `Gap` (Vacío) — la sección 15 los declara categorías mínimas; si no son entidades consultables, "¿qué falta en este expediente?" (sección 11) no tiene sustrato.
- `ProvenanceRecord`/origen tipado — transversal, exigido por la sección 14.
- `Term`/`Deadline` — HIPÓTESIS: en la práctica procesal colombiana los términos gobiernan el trabajo diario; el documento los omite. POR VERIFICAR con la usuaria.

**Sobra o cambia de capa:**
- `Artifact` no es entidad de dominio jurídico; es un concepto de Application (registro de trabajo producido, sección 17). Mezclarlo con `Fact` y `Evidence` en la misma lista confunde dos planos.
- `Event` vs `ProceduralEvent`: mantener ambos solo si `Event` se define como "ocurrencia del mundo referida por hechos" y `ProceduralEvent` como "actuación dentro del trámite". Si no se va a dar esa semántica, eliminar `Event` y dejar que `Fact` cubra el plano fáctico.

**Mal nombrado:**
- `Decision` → separar en `Ruling` (providencia/acto de autoridad, es a la vez un `Document` con efectos), `ProfessionalDetermination` (acto interno que fija estatus epistémico) y dejar las decisiones estratégicas fuera del dominio v0.
- `Party` → relación con rol (`Person|Organization` × `Case` × rol procesal), no entidad hermana de `Person`.

**Antídoto contra la sobreabstracción:** la tentación será modelar todo como "nodo assertion con metadatos" en un grafo universal. RIESGO: eso hace imposible expresar invariantes específicos (p. ej. "solo un humano acredita"). Regla propuesta: cada entidad existe solo si tiene lifecycle o invariantes propios; lo que no los tenga es un atributo.

### 2. ¿`Fact`, `Assertion`, `Statement` y `Evidence` independientes? Relaciones y lifecycle.

**Sí, las cuatro, pero con una definición estricta de cada una — y con `EvidenceLink` como quinta pieza:**

- **`Statement`** — acto de expresión anclado a una fuente: quién lo dijo/escribió, dónde (documento+página/párrafo, audio+timestamps), cuándo. Inmutable tras ingestión. Cardinalidad: un Statement pertenece a exactamente 1 fragmento de fuente; una fuente contiene 0..N Statements. Lifecycle: `extraído → verificado_contra_fuente → (anulado si la extracción era errónea, sin borrado)`. Es el ancla de provenance.
- **`Assertion`** — contenido proposicional sostenido por un actor ("el contrato se firmó el 3 de marzo"). Relación: una Assertion se sustenta en 1..N Statements (la misma proposición puede afirmarse en la entrevista y en la demanda); un Statement puede contener 0..N Assertions. Lifecycle: `propuesta (por IA) → confirmada (por humano) → retirada`. SUPUESTO simplificador legítimo para v0: colapsar Assertion en Statement (un Statement porta su proposición) y separar solo cuando aparezca la necesidad real de agregación multi-fuente. Esta es una decisión, no un hecho; la marco DECISIÓN PENDIENTE.
- **`Fact`** — proposición fáctica curada a nivel de caso, con **estatus epistémico e historia de estados**. Relaciones: deriva de 0..N Assertions (0 permite el hecho alegado directamente por el abogado en el escrito); conecta a Evidence únicamente vía EvidenceLink. Lifecycle: ver Respuesta 3.
- **`Evidence`** — rol probatorio de un material en un caso. **No es el `Document`**: el documento/audio es la fuente (con hash, inmutable); Evidence es su incorporación a un caso concreto con metadata probatoria. Un mismo Document puede ser Evidence en varios casos con estados independientes. Lifecycle: `incorporada → (derivados generados) → valorada → (excluida/inadmitida, sin borrado)`.
- **`EvidenceLink`** — asociación Fact×fragmento-de-Evidence con `polaridad ∈ {respalda, contradice, contextualiza}`, actor que lo creó, justificación, y estado `activo|retirado`. Cardinalidad N:M plena; anclaje a fragmento (página/offset/timestamp), no a documento entero — un vínculo a "el expediente de 200 páginas" destruye la trazabilidad de la sección 16.

Por qué no fusionar Fact con Assertion: la Assertion pertenece a quien la sostiene (no cambia de estado por el juicio del sistema); el Fact pertenece al análisis del caso (su estatus evoluciona). Fusionarlos reproduce exactamente el riesgo #3 de la sección 3.

### 3. Representación del hecho alegado → probado a favor y en contra → controvertido → acreditado

Con el modelo anterior, el escenario se registra así (todo append-only):

```
t1  Statement S-9 extraído de entrevista (audio E-5, 00:12:31–00:13:04)
t2  Fact F-12 creado desde S-9
      status_history: [{estado: ALEGADO, actor: HUMANO(commit) sobre propuesta IA, base: S-9}]
t3  EvidenceLink L-1 {F-12, E-7 contrato p.3, polaridad: RESPALDA, actor: IA propuesto → humano confirmado}
      → estado derivado: ALEGADO_CON_SOPORTE (el soporte NO acredita)
t4  EvidenceLink L-2 {F-12, E-9 testimonio 00:41:10, polaridad: CONTRADICE, ...}
      → estado derivado: CONTRADICHO_POR_EVIDENCIA
t5  (si aplica) ProceduralEvent "contestación niega el hecho"
      → estado procesal: CONTROVERTIDO
t6  ProfessionalDetermination D-4 {actor: HUMANO identificado, fecha, motivación,
      links_valorados: [L-1, L-2]}
      status_history += {estado: ACREDITADO, fundamento: D-4}
```

**Qué cambia:** solo se agrega una entrada a `status_history` y se crean D-4 y los links. **Qué se registra:** cada transición con actor, momento, y qué evidencia fue valorada — incluida la contraria. **Qué NO se sobrescribe:** S-9, L-1, **L-2 (la prueba en contra permanece visible y activa)**, y todos los estados anteriores. Distinción crítica del paso t4/t5: "contradicho por evidencia" es **derivable** de los links; "controvertido" procesalmente es un **evento externo**. El modelo debe registrar ambos por separado (hallazgo 7). Si después entra nueva evidencia, el estado puede regresar a controvertido con D-4 intacto y marcado como superado — nunca borrado.

Nota de dominio: la validez de exigir D-4 con humano depende de la configuración (sección 15: "en determinados contextos, validación profesional"). El invariante correcto es condicional a la política, pero la transición sin el registro correspondiente debe ser imposible, no desaconsejada.

### 4. Distinción técnica: extraído / inferencia IA / decisión humana / fuente original

Un `ProvenanceRecord` obligatorio en toda entidad epistémica, con **tipo de actor como discriminante de primer nivel**:

- **`EXTERNAL_SOURCE`** — originales: blob inmutable + hash + metadata de incorporación. Nunca producidos por IA. La grabación original como fuente primaria (sección 6) vive aquí.
- **`AI_DERIVATION`** (dato extraído) — derivado con ancla exacta al fragmento original (página/offsets/timestamps), herramienta/skill+versión, identificador del modelo, y marca de confianza. Importante: la extracción por IA **es** una inferencia de bajo nivel; lo que la hace "dato extraído" es que es verificable contra el ancla, no que sea confiable per se.
- **`AI_INFERENCE`** — conclusión con registro de derivación: conjunto de inputs (por hash/id), skill+versión, modelo. Restricción estructural: un actor de este tipo jamás puede escribir un estado epistémico superior a "candidato/propuesto". Esto se rechaza en el Domain, no en el prompt (coherente con sección 12).
- **`HUMAN_DECISION`** — única fuente válida de transiciones sensibles (acreditar, confirmar, excluir), con identidad del profesional y motivación. RIESGO abierto: en un despliegue local mono-usuario la "identidad" es débil; para el slice basta SUPUESTO explícito (un solo usuario profesional, confirmación interactiva vía operación MCP dedicada tipo `commit_reviewed_fact`), documentado como deuda.
- **`SYSTEM`** — mutaciones mecánicas (regeneración de memory.md, migraciones), para que la auditoría no las confunda con juicios.

La distinción se refuerza en tres capas: el tipo de actor viaja en cada operación MCP; el Domain valida qué transiciones admite cada tipo; la auditoría (audit.log) lo persiste. POR VERIFICAR: qué identidad de modelo/versión expone en runtime la plataforma anfitriona (Claude/Cowork) para poblar `AI_*` con precisión; no debe asumirse.

**Sobre litigante vs autoridad (punto e de la misión):** un solo modelo de dominio — Statement/Assertion/Fact/Evidence/provenance son invariantes en ambos contextos — con **dos diferencias que NO son prompts**: (1) la semántica de "acreditado" difiere: en A es un juicio profesional interno ("considero que esto quedará probado"); en B es una determinación con efectos dentro de una providencia. Deben ser estados distintos (`acreditado_profesionalmente` vs `declarado_probado`), no el mismo estado con otro tono. (2) las políticas de transición difieren: en modo decisor, un invariante de Application debe exigir que toda acreditación referencie la valoración explícita de los links contradictorios y de las afirmaciones de ambas partes — verificable estructuralmente (¿existen links CONTRADICE sin entrada en `links_valorados`? → transición rechazada). Eso convierte "neutralidad" en propiedad comprobable. Dos modelos de dominio separados duplicarían el 80% del sistema sin ganancia; un flag que solo cambia prompts es el anti-patrón que la sección 12 prohíbe. La opción intermedia: dominio único + servicios de Application por contexto + políticas en configuración validada. HIPÓTESIS razonable, pendiente de contrastar con el trabajo real del contexto B, que el documento describe con menos detalle que el A.

---

## Invariantes candidatos

1. **Ningún `Fact` alcanza un estado epistémico sensible (acreditado/declarado probado) sin una `ProfessionalDetermination` con actor `HUMAN_DECISION`, cuando la política del contexto lo exige.** Capa: Domain (regla de transición) + Configuración (política). Prueba: test unitario que intenta la transición con actor `AI_INFERENCE` y espera rechazo.
2. **Toda entidad epistémica porta `ProvenanceRecord` con tipo de actor.** Capa: Domain. Prueba: construcción sin procedencia falla; validación de schema en persistencia.
3. **`status_history` de un `Fact` es append-only; ninguna transición elimina entradas previas.** Capa: Domain + Infraestructura. Prueba: secuencia de transiciones y verificación de historia completa; test de que no existe operación de borrado.
4. **Acreditar un hecho no elimina ni desactiva sus `EvidenceLink` de polaridad CONTRADICE.** Capa: Domain. Prueba: escenario de la Respuesta 3; asserts sobre L-2 tras D-4.
5. **Todo `EvidenceLink` ancla a un fragmento verificable (página/offset/timestamp) de un original con hash.** Capa: Domain (obligatoriedad) + Infraestructura (verificación de hash). Prueba: creación sin ancla falla; re-hash detecta alteración.
6. **Un derivado (transcripción, OCR, extracto) referencia siempre su original y nunca lo sustituye.** Capa: Infraestructura + Domain. Prueba: borrar/alterar el original con derivados vivos es rechazado; el derivado expone `source_id`.
7. **Un actor `AI_*` no puede crear entidades en estado distinto de "propuesto/candidato".** Capa: Application (gate de operaciones MCP) + Domain. Prueba: llamada a operación de commit con procedencia IA → rechazo.
8. **El estatus epistémico es relativo al caso: el mismo `Document` como `Evidence` en dos casos mantiene estados y links independientes.** Capa: Domain. Prueba: dos casos comparten documento; transición en uno no afecta al otro.
9. **Toda regeneración de `memory.md` preserva la partición alegado/controvertido/acreditado sin fusión de categorías.** Capa: Application. Prueba: regenerar proyección y verificar que ningún hecho no-acreditado aparece bajo acreditados.
10. **Los hechos con cero `EvidenceLink` activos son enumerables como tales.** Capa: Application (query) sobre Domain. Prueba: crear hecho sin links y verificar que aparece en la consulta de vacíos probatorios.
11. **En contexto decisor, ninguna determinación puede registrarse si existen links CONTRADICE no incluidos en `links_valorados`.** Capa: Domain (regla) activada por Configuración. Prueba: intento de determinación omitiendo un link contradictorio → rechazo.

---

## ADR candidatos

1. **Separación Statement/Assertion/Fact/Evidence + EvidenceLink de primera clase.** Contexto: sección 8 y 15 desalineadas. Decisión posible: las cinco entidades con las semánticas de la Respuesta 2, colapsando Assertion en Statement para v0. Alternativas: modelo mínimo Fact+Evidence (pierde provenance fina); grafo universal de assertions (pierde invariantes tipados). Consecuencias: más entidades en el slice, pero trazabilidad de la sección 16 realizable. Información faltante: si la agregación multi-fuente de una misma proposición aparece de verdad en el trabajo de la usuaria.
2. **Estatus epistémico como historia de transiciones tipadas por actor (no campo mutable).** Contexto: hallazgos 6 y 9; secciones 14–16. Decisión posible: `status_history` append-only + transiciones validadas por tipo de actor. Alternativas: event-sourcing completo del caso (más costoso, más potente); campo + audit.log separado (auditable pero no impone la regla). Consecuencias: define el schema de case.db y la semántica de `commit_reviewed_fact`. Información faltante: requisitos reales de auditoría/responsabilidad profesional (preguntas de la sección 31).
3. **"Controvertido" dual: estado derivado de links vs estado procesal por evento.** Contexto: hallazgo 7. Decisión posible: dos dimensiones separadas (evidencial computada, procesal registrada). Alternativas: un solo estado (ambiguo); solo procesal (pierde la señal automática de conflicto de evidencia). Consecuencias: consultas de contradicciones más ricas; ligera complejidad extra. Información faltante: vocabulario real de la profesional en ambos contextos.
4. **Un dominio, dos contextos: servicios de Application y políticas por rol, no dos modelos ni solo prompts.** Contexto: secciones 5, 24; hallazgo 8. Decisión posible: dominio único + estados distintos para acreditación A/B + invariante 11 estructural. Alternativas: dos bounded contexts (duplicación); flag de rol que solo cambia prompts (neutralidad no verificable). Consecuencias: el contexto B exige diseño de políticas comprobables antes de habilitarlo. Información faltante: levantamiento detallado del trabajo decisorio real (el documento describe B mucho menos que A).
5. **Vocabulario de estados epistémicos fijo en v0, configurable después vía Knowledge Packs.** Contexto: hallazgo 12; sección 23. Decisión posible: enum fijo + historia, con punto de extensión declarado. Alternativas: máquina configurable desde el inicio (sobreingeniería); hardcode sin plan de extensión (bloquea multi-jurisdicción). Consecuencias: slice simple; deuda explícita. Información faltante: variabilidad real de estándares probatorios entre las ramas/jurisdicciones objetivo — POR VERIFICAR con juristas, no asumible.

---

## Decisiones bloqueantes

1. **Subconjunto exacto de entidades del slice** (propuesta: Case, Document/original, Evidence, Statement, Fact, EvidenceLink, ProvenanceRecord, ProfessionalDetermination; excluidos: Hypothesis, Argument, LegalIssue, Claim, contexto B). Bloquea: el schema de case.db, la proyección memory.md y las operaciones MCP (`propose_facts`, `commit_reviewed_fact`) dependen de esto; las propiedades 4, 5, 6 y 10 de la sección 34 no son demostrables sin fijarlo.
2. **ADR 2 (historia de estados tipada por actor).** Bloquea: `commit_reviewed_fact` no puede diseñarse sin saber si commit = sobrescribir campo o = registrar transición; cambiarlo después implica migración del núcleo del estado.
3. **Representación mínima de procedencia (los 5 tipos de actor y sus campos).** Bloquea: la propiedad 6 del slice (provenance) es literalmente esta decisión; toda ingestión y extracción del slice la escribe desde el primer byte.
4. **Semántica de anclaje a fragmento (cómo se identifica página/offset/timestamp de forma estable).** Bloquea: los EvidenceLinks y la cadena de la sección 16 dependen de que el ancla sobreviva a regeneración de derivados; retrofitearlo invalida links existentes.
5. **SUPUESTO de identidad humana para v0** (un solo profesional; la confirmación interactiva cuenta como `HUMAN_DECISION`). Bloquea: sin declararlo, el invariante 1 es indefinible; debe quedar como supuesto escrito con su deuda asociada.

No bloquean (y debe decidirse explícitamente aplazarlas): máquina de estados configurable, modelado del contexto B, Assertion como entidad separada, términos/plazos.

---

## Preguntas para los dueños

1. **En el contexto A, cuando la abogada dice que un hecho "está acreditado", ¿se refiere a su juicio profesional sobre lo que quedará probado, a lo ya declarado por la autoridad, o usa ambas nociones?** Importa porque define si necesitamos uno o dos estados terminales y su semántica; bloquea parcialmente el diseño de la máquina de estados del slice.
2. **En el contexto B, ¿qué categorías usa realmente para el estado de los hechos durante el trámite y en qué acto formal quedan fijadas?** Importa para validar la HIPÓTESIS de dominio único (ADR 4); no bloquea el slice si este se limita al contexto A, pero bloquea el diseño dual.
3. **¿Una misma instalación/oficina manejará simultáneamente casos como litigante y como autoridad?** Importa porque decide si el rol es configuración por instalación o por caso, y si se requiere aislamiento entre contextos; bloquea la estructura de Client Pack, no el modelo de entidades.
4. **¿Quiénes podrán ejecutar acreditaciones — solo la profesional titular o también auxiliares/judicantes — y necesitan quedar identificados individualmente en la trazabilidad?** Importa para el diseño de `HUMAN_DECISION` y permisos MCP; puede esperar al slice bajo el SUPUESTO mono-usuario si se acepta explícitamente.
5. **¿Los hechos de una demanda requieren identidad estable a través de reformas/sustituciones del escrito (el "hecho 3" sigue siendo el mismo hecho tras una reforma)?** Importa para separar identidad del `Fact` de su presentación en el `Artifact` y para el diseño de identificadores; puede esperar, pero conviene resolverla antes del primer `legal-drafting`.