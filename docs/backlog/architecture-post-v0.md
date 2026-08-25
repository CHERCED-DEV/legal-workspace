# Backlog de arquitectura post-V0 — lo que no se construye y no se olvida

**Estado:** documento de **registro**. No es normativo, no crea decisiones y no autoriza trabajo.
**Precedencia:** por debajo de los ADRs Accepted y del Technical Design V0 (kernel §14). Donde este registro parezca contradecir un documento superior, gana el superior y este se corrige.
**Referenciado por:** kernel técnico §15, que remite aquí el alcance excluido de la iteración.

## Para qué existe

Un backlog de arquitectura no es una lista de deseos. Es el registro de que **una exclusión fue decidida y no olvidada**, para que dentro de seis meses nadie tenga que reconstruir por qué algo no está — ni lo construya por segunda vez desde cero creyendo que nadie lo pensó.

Cada ítem responde tres preguntas, y las tres son obligatorias:

| Pregunta | Qué previene |
|---|---|
| **Por qué está fuera de V0** | Que la exclusión se lea como descuido y alguien la "arregle" |
| **Qué disparador lo traería de vuelta** | Que entre por presión de una demo o por entusiasmo, sin criterio |
| **Qué NO debe romperse hoy para que sea posible mañana** | El retrabajo caro: descubrir que una decisión de V0 cerró la puerta |

La tercera es la que justifica el documento. Las dos primeras son memoria; la tercera es **una restricción activa sobre el diseño de hoy**.

**Etiquetas:** HECHO VERIFICADO / DECISIÓN APROBADA / HIPÓTESIS / SUPUESTO / POR VERIFICAR / RIESGO / DECISIÓN PENDIENTE. Nada aquí afirma capacidades de plataformas, proveedores ni rendimiento: lo que no está verificado se dice sin verificar.

---

# i. Conceptos de dominio reservados

## La regla de entrada

**DECISIÓN APROBADA (dueños, prompt de consolidación §7; citada literalmente en el addendum v0.3 Anexo B.1):**

> *"La regla será: Una entidad entra al dominio cuando existe evidencia de que tiene lifecycle, identidad o invariantes propios."*

Y la instrucción que la acompaña (Anexo B.2):

> *"Reserva conceptualmente para evolución posterior: Assertion, Contradiction, Gap, LegalIssue, Hypothesis, Argument, Ruling, ProceduralEvent, Term, Deadline — pero NO los conviertas automáticamente en entidades v0."*

Los tres criterios son **alternativos, no acumulativos** ("lifecycle, identidad **o** invariantes propios"), y el sustantivo que manda es **evidencia**: no basta con que el concepto sea nombrable ni con que un ingeniero imagine un ciclo de vida plausible. Hace falta un caso real de trabajo donde el concepto se comporte como entidad.

**Por qué la regla protege algo.** El error natural en un dominio jurídico es modelar el vocabulario en lugar de modelar el trabajo. "Contradicción", "vacío probatorio" y "problema jurídico" son palabras que la profesional usa a diario; convertirlas en tablas por eso sería confundir el léxico del oficio con la estructura del sistema. Cada entidad prematura cuesta invariantes que nadie verificará, estados que nadie transicionará y una migración cuando el trabajo real resulte no parecerse a la suposición.

## Precisión sobre tres estatus distintos

Los conceptos de abajo **no comparten estatus**, y tratarlos como un bloque induce a error. Esta tabla es una **precisión de este registro** sobre la enumeración del kernel §15, no una decisión nueva:

| Estatus | Qué significa | Cuáles |
|---|---|---|
| **Definido en el Domain, sin productor en V0** | La entidad existe en el modelo, con definición e invariantes fijados. Lo diferido es **quién la crea**, no si existe | `Statement`, `ProfessionalDetermination` |
| **Nombre reservado — NO es entidad** | No existe en el modelo. Ningún documento debe tratarlo como existente | `Assertion`, `Contradiction`, `Gap`, `LegalIssue`, `Hypothesis`, `Argument`, `Ruling`, `ProceduralEvent`, `Term`/`Deadline` |
| **Use case diferido con nombre reservado** | Operación conocida, nombrada para no improvisarla después | `ExtractStatements`, `RecordProfessionalDetermination`, `WithdrawFact` |

**Observación de consistencia registrada.** La enumeración del kernel §15 (*"Statement (reservado, §Q5), Contradiction, Gap, LegalIssue, Hypothesis, Ruling, Term/Deadline"*) **omite `Argument` y `ProceduralEvent`**, que sí figuran en la lista literal de los dueños (Anexo B.2). Este registro usa la **lista de los dueños**, que es la fuente. No se trata de una contradicción normativa —el kernel enumera de forma abreviada, no cierra la lista— pero conviene que la próxima revisión del kernel la complete. Igualmente, el kernel lista `Statement` junto a los nombres reservados cuando su estatus es el de la primera fila: **está en el Domain** y es uno de los trece términos del vocabulario canónico.

---

## Statement

**Estatus:** definido en el Domain (glosario §4), **no materializado en V0** (DECISIÓN APROBADA, addendum v0.3 B.7).

**Por qué está fuera de V0.** No por dudas sobre su pertenencia al dominio, sino porque **no existe extractor**. La cadena de provenance efectivamente ejercitada en el slice —`Fact → EvidenceLink → fragmento → DerivedRepresentation → Source`— es suficiente para la propiedad de trazabilidad exigida a V0. Añadir Statements sin un productor real solo agregaría una tabla vacía.

**Nota importante sobre la regla de entrada:** `Statement` **ya la satisface**, y por los tres criterios a la vez — lifecycle (inmutable tras extracción; corrección = anulación + nuevo registro, nunca edición), identidad propia, e invariantes propios (ancla siempre resoluble contra el **original**, no contra el derivado). Lo que le falta no es evidencia de ser dominio: es un productor. Por eso su estatus difiere del de los nombres reservados.

**Disparador de vuelta.** La construcción del use case `ExtractStatements` (nombre ya reservado), que a su vez depende de un proveedor de derivación con capacidades de anclaje verificadas.

**Qué NO debe romperse hoy.**
- Los anclajes deben referir **siempre a la línea de tiempo o paginación del original**, nunca a la del derivado ni a un recorte. Si V0 anclara contra la transcripción, los Statements futuros heredarían anclas que dejan de resolver cuando la transcripción se regenere.
- `DerivedRepresentation` **nunca** se sirve como si fuera el Source.
- La entidad permanece definida en el Domain y entre los trece términos del glosario: no se borra por no materializarse.

**POR VERIFICAR:** capacidades reales de timestamps del proveedor de transcripción. Mientras no se verifique, la granularidad del ancla temporal es **SUPUESTO** y no debe prometerse en ninguna interfaz.

---

## Contradiction

**Estatus:** nombre reservado. **No es entidad.**

**Por qué está fuera de V0.** La contradicción ya está representada, y de forma más honesta que como entidad: es un `EvidenceLink` con polaridad `CONTRADICTS` y un **estado derivado** `CONTRADICTED` que se **computa en cada proyección desde los links `ACTIVE`, jamás se almacena** (glosario §5, invariante 5). Promoverla a entidad hoy significaría persistir algo que hoy no puede divergir de la realidad — introducir exactamente el defecto que el modelo epistémico evita.

**Disparador de vuelta.** Evidencia de que una contradicción necesita **identidad propia**: que la profesional quiera referirse a *esta* contradicción concreta, asignarla, anotarla, seguir su resolución. O evidencia de **lifecycle propio**: detectada → analizada → resuelta/descartada, con estados que no son los de ningún link. Señal concreta a vigilar: si aparece la necesidad de decir "esta contradicción ya la resolví" sin retirar ninguno de los dos links, el concepto tiene lifecycle propio y entra.

**Qué NO debe romperse hoy.**
- Los estados derivados (`SUPPORTED`, `CONTRADICTED`, `UNSUPPORTED`) **jamás se persisten como status**. Si mañana `Contradiction` es entidad, debe construirse **encima** de los links vigentes, no migrando un campo almacenado que se haya desincronizado.
- Determinar un Fact **no** retira ni desactiva sus links `CONTRADICTS` (ADR-003, invariante 5). Es la garantía de que la prueba en contra sobrevive a la decisión — y sería la materia prima de cualquier `Contradiction` futura.
- El enum de polaridad es **cerrado** en V0. La regla acordada es **señalar** un caso real donde tres polaridades no basten, no ampliarlo preventivamente.

---

## Gap

**Estatus:** nombre reservado. **No es entidad.**

**Por qué está fuera de V0.** El vacío probatorio ya está representado como estado derivado `UNSUPPORTED` = **cero links de polaridad probatoria (`SUPPORTS`/`CONTRADICTS`) activos** (addendum v0.3 B.14). Y hay una decisión explícita que conviene no perder: **`UNSUPPORTED` no es una alerta**. Es **dato de proyección** (`facts`, `pending`), no condición del catálogo — la condición `NO_SUPPORT_FOUND` quedó **registrada como superseded** (kernel §9, §16.5). Un hecho sin soporte todavía es el estado normal de un hecho recién propuesto, no una anomalía que merezca interrumpir a nadie.

**Disparador de vuelta.** Evidencia de que un vacío necesita **identidad**: que la profesional lo nombre, lo priorice y lo siga como "lo que todavía me falta probar" — una lista de trabajo con estados propios, no una consecuencia aritmética de qué links existen. Señal concreta: si quiere registrar *por qué* un vacío sigue abierto, o *qué* piensa hacer para cerrarlo, eso es contenido que ningún cómputo sobre links puede sostener.

**Qué NO debe romperse hoy.**
- `UNSUPPORTED` sigue siendo **derivado y no almacenado**.
- **No reintroducir una condición del catálogo para la ausencia de soporte.** La supersede de `NO_SUPPORT_FOUND` fue deliberada; revivirla convertiría el estado normal de un hecho nuevo en una alarma, y el ruido de condiciones erosiona la atención que las condiciones reales necesitan.
- Los links `CONTEXTUALIZES` **no cuentan** en el cómputo: un Fact cuyos únicos links activos sean contextuales se computa como `UNSUPPORTED`. Esa precisión debe sobrevivir a cualquier entidad `Gap` futura.

---

## LegalIssue

**Estatus:** nombre reservado. **No es entidad.**

**Por qué está fuera de V0.** Exige conocimiento jurídico anclado a una jurisdicción, y V0 **no carga ningún Knowledge Pack** ni ejercita el skill `legal-issue-spotting`. La declaración de alcance es explícita: el slice es de **caso + evidencia + hechos + memoria + provenance + autoridad humana, no de investigación jurídica**. Un `LegalIssue` sin fuentes jurídicas verificadas sería una etiqueta generada por el modelo con apariencia de estructura — precisamente el tipo de cosa contra la que existe PF-004.

**Disparador de vuelta.** Que exista el Knowledge Pack Colombia con fuentes verificadas **y** evidencia del trabajo real de que la profesional organiza sus casos por problemas jurídicos con lifecycle propio (abierto → investigado → resuelto), no solo que los mencione al hablar.

**Qué NO debe romperse hoy.**
- **`Case` es el agregado raíz y todo lo epistémico vive dentro de un Case.** Un `LegalIssue` futuro cuelga del Case; no se convierte en una raíz paralela que fragmente el aislamiento entre expedientes.
- **PF-004** (una fuente jurídica no verificada no se vuelve verificada por afirmación del modelo) es no relajable por configuración. Es el piso sobre el que cualquier análisis jurídico futuro tendrá que apoyarse.

---

## Hypothesis

**Estatus:** nombre reservado. **No es entidad.**

**Por qué está fuera de V0.** Hoy es **indistinguible de un `Fact` en estado `PROPOSED` que aún no se ha commiteado**. Sin un caso real donde una hipótesis se comporte distinto de un hecho propuesto, crear la entidad duplicaría el modelo sin añadir capacidad.

**RIESGO específico a vigilar cuando entre.** Una `Hypothesis` es un candidato natural a **puerta trasera del techo epistémico**: un concepto "más blando" que un Fact podría tentar a permitir que la IA lo cree y transicione libremente, y desde ahí se promueva a Fact sin revisión humana. Si el concepto entra, su relación con el commit humano debe diseñarse **antes** que su lifecycle.

**Disparador de vuelta.** Evidencia de lifecycle propio: una hipótesis que se explora, se confirma o se descarta **sin llegar nunca a tocar el estatus epistémico del expediente** — un espacio de trabajo que hoy no existe. O de identidad propia: que necesite referenciar varios hechos a la vez, cosa que un `Fact` no hace.

**Qué NO debe romperse hoy.**
- **El techo epistémico de la IA** (PF-001, ADR-003 invariante 1): ningún actor `AI_*` crea ni transiciona un Fact más allá de `PROPOSED`, y el Domain lo rechaza **con independencia de qué superficie lo transporte**. Que la regla viva en el Domain y no en la superficie MCP es lo que impide que un concepto nuevo la esquive.
- **`PROPOSED → ALLEGED` solo por commit con `HumanAuthorization` viva.**

---

## Argument

**Estatus:** nombre reservado. **No es entidad.** *(Presente en la lista de los dueños; omitido en la enumeración abreviada del kernel §15 — ver observación de consistencia arriba.)*

**Por qué está fuera de V0.** Requiere drafting y fuentes jurídicas, ninguno de los cuales existe en el slice (`legal-drafting` y `adversarial-review` están fuera). El análogo más cercano hoy es `Artifact` — el **registro de trabajo** del plano Application que deja constancia de que un análisis se generó, con qué insumos exactos, bajo qué metodología y en qué revisión del Case.

**Disparador de vuelta.** Que exista drafting **y** evidencia de que un argumento necesita persistir con identidad propia, revisarse y ser superseded **independientemente del Artifact que lo produjo** — hoy un argumento es contenido de un artifact, no algo que sobreviva a él.

**Qué NO debe romperse hoy.**
- **`Artifact` no es entidad jurídica del dominio.** Si un producto de trabajo llegara a tener valor probatorio, entra al expediente **por incorporación**, como cualquier otro material (ADR-006). Un `Argument` futuro no puede convertirse en el atajo que salte la frontera de incorporación.
- **`inputs[]` se registra por id + `content_hash`, jamás por nombre de archivo**, e incluye la versión exacta de la `DerivedRepresentation` consumida. Es la maquinaria que hace posible el staleness, y un `Argument` la heredaría.
- La propagación de staleness (`stale` + `stale_reasons[]`, condición `ANALYSIS_STALE`) ocurre **dentro de la misma transacción** que la mutación que la causa.

---

## Ruling

**Estatus:** nombre reservado. **No es entidad.**

**Por qué está fuera de V0.** Pertenece al **contexto B (autoridad/decisor)**, cuyo trabajo real **NO HA SIDO LEVANTADO**: no existe descripción validada de su flujo, sus gates ni su vocabulario. **NO TENEMOS INFORMACIÓN SUFICIENTE**, y el corpus lo declara así de forma consistente. Que la primera usuaria opere ambos contextos es **SUPUESTO, no hecho verificado** — la verificación de consistencia señaló un documento que lo afirmaba sin etiqueta.

**Disparador de vuelta.** El levantamiento del contexto B, y en particular la respuesta a la **pregunta de negocio 7** (definición del expediente oficial en contexto autoridad), que puede **invertir la política de custodia**: si existe un expediente digital oficial en un sistema externo, nuestro almacén sería copia de trabajo y no custodio primario.

**Qué NO debe romperse hoy.**
- **`DETERMINED(kind)` lleva un `kind` desde el diseño inicial**, con `DECLARED_PROVEN` **reservado** para el contexto B. Es la decisión que permite que una providencia entre mañana **sin reabrir la máquina de estados del `Fact`** — el mismo patrón que `authorized_operation` en `HumanAuthorization`, que se conserva aunque V0 tenga un solo valor.
- **`DECLARED_PROVEN` no se implementa ni se le afirma semántica** mientras el contexto B no se levante. Reservar un nombre no es definirlo.
- El rol se resuelve **por Case / contexto activo**, no por organización (DECISIÓN APROBADA). Anclarlo a la organización rompería con el primer usuario que atienda ambos contextos.

---

## ProceduralEvent

**Estatus:** nombre reservado. **No es entidad.** *(Presente en la lista de los dueños; omitido en la enumeración abreviada del kernel §15.)*

**Por qué está fuera de V0.** El slice **no contiene lógica procesal**, y la exclusión está materializada en dos lugares: el scope `procedural` de `get_case_context` está **RESERVADO — documentado, no implementado** (kernel §9), y el glosario dice explícitamente que un `Case` **no es el proceso judicial ni la actuación procesal**. La lógica procesal depende de reglas de jurisdicción que nadie ha levantado ni verificado.

**Disparador de vuelta.** Levantamiento del trabajo procesal real, con reglas de jurisdicción verificadas contra fuente oficial. No basta con que la profesional describa su procedimiento: hace falta la fuente.

**Qué NO debe romperse hoy.**
- **El scope `procedural` permanece reservado en el enum de scopes.** Tenerlo reservado es lo que permite implementarlo mañana sin romper el contrato de `get_case_context`.
- **El `Case` no se convierte en espejo del expediente del juzgado.** Es una **frontera de aislamiento**, no una réplica de la actuación.
- La lista cerrada de eventos V0 no se amplía preventivamente con eventos procesales.

---

## Term / Deadline

**Estatus:** nombre reservado. **No es entidad.**

**Por qué está fuera de V0.** Depende del motor de plazos (ver §ii) y de reglas de cómputo de términos por jurisdicción, que **NO TENEMOS INFORMACIÓN SUFICIENTE** para afirmar y que no se citan de memoria.

**RIESGO — el más grave de este documento.** Un plazo mal calculado tiene consecuencias profesionales directas e irreversibles para la usuaria: no es un error de software, es un término vencido. Un plazo **correcto pero mostrado con apariencia de certeza cuando la regla no fue verificada** es igual de peligroso, porque induce confianza. Este concepto **no debe entrar por conveniencia ni por demo**, y cuando entre, debe entrar con la incertidumbre visible.

**Disparador de vuelta.** Reglas de cómputo verificadas contra fuente oficial **y** una decisión explícita de los dueños asumiendo la responsabilidad del producto sobre esa función. Los dos requisitos, no uno.

**Qué NO debe romperse hoy — la restricción más dura del documento.**
- **Nada en V0 debe calcular, almacenar ni mostrar algo que se parezca a un plazo.** Ni un campo de fecha derivada presentado como término, ni un "vence en N días" en ninguna proyección, ni una fecha calculada que la usuaria pueda leer como cómputo procesal.
- La razón es de confianza, no de arquitectura: **una fecha que aparece en la pantalla se lee como afirmación del sistema**, aunque en el código sea un cálculo ingenuo. Introducir una sola fecha así hoy crea la expectativa que el motor de plazos tendría que honrar mañana.

---

# ii. Capacidades de producto

## Knowledge Pack Colombia

**Por qué está fuera de V0.** **DECISIÓN APROBADA (kernel §11):** ningún pack se carga en el slice. V0 no ejercita conocimiento jurídico; el contrato de pack se documenta aparte.

**Disparador de vuelta.** Necesidad de análisis jurídico real, alimentada por la **pregunta de negocio 4** (fuentes jurídicas habituales). **POR VERIFICAR** antes de construirlo: los términos de uso de las bases de datos comerciales respecto de reproducción de contenido — no se afirma de memoria qué permite ninguna suscripción.

**Qué NO debe romperse hoy.**
- **`knowledge_pack_versions[]` existe en el schema del `Artifact` desde el inicio** y va **vacío** en el slice, pero es **obligatorio en cuanto un Artifact dependa de un pack** (glosario §9, invariante 5). Es exactamente la decisión que evita migrar artifacts existentes cuando lleguen los packs.
- La configuración **solo endurece, nunca relaja** por debajo del Product Floor (PF-005).

## Jurisprudencia y verificación de fuentes jurídicas

**Por qué está fuera de V0.** **DECISIÓN APROBADA (dueños):** `verify_legal_source` está **fuera de la superficie**, y es una de las dos tools retiradas respecto de versiones previas. La consecuencia es deliberada y elegante: **la única respuesta posible del sistema a "marca esta sentencia como verificada" es que la operación no existe** — y eso es **mensaje de producto, no condición del catálogo** (addendum v0.3 B.6), porque la tool no está en el manifiesto y el Core nunca ve la operación.

**Disparador de vuelta.** Knowledge Pack con fuentes verificadas y una decisión sobre qué significa "verificada" operativamente.

**Qué NO debe romperse hoy.**
- **PF-004**, no relajable por configuración.
- **La reserva de `OPERATION_NOT_PERMITTED`**: se emite **únicamente** cuando la capacidad **existe** y una política o el perfil la vetan. Para operaciones inexistentes en la superficie no hay condición del catálogo. Confundir ambos casos haría creer que existe un camino vetado donde no existe camino alguno.
- **El test de superficie** verifica que el manifiesto contiene exactamente las tools V0 con su clase. `verify_legal_source` no está, y su ausencia es comprobable.

## Legal Auditor

**Por qué está fuera de V0.** Capacidad de producto post-slice; V0 construye el sustrato que auditaría, no el auditor.

**Disparador de vuelta.** Demanda real de revisión sistemática de expedientes, o exigencia externa de auditoría.

**Qué NO debe romperse hoy.**
- **El Case Event Log es append-only, hash-chained y no desactivable ni editable por configuración.** Un auditor futuro lee ese log: si hoy se debilitara —eventos editables, cadena opcional—, la auditoría de lo ya ocurrido sería **irrecuperable retroactivamente**. Es el ítem donde la tercera pregunta más pesa.
- **Todo evento lleva `Principal` y `provenance_kind`**, que son las dos dimensiones que un auditor necesita separadas: quién ejecutó y de dónde procede el conocimiento.
- **La retención del Tool Invocation Log es política, no arbitrariedad.** Podarlo destruye material de diagnóstico; conviene decidir la retención antes de que el volumen fuerce la decisión.
- **HONESTIDAD OBLIGATORIA (kernel §8.3):** el hash-chain es **tamper-evident, no tamper-proof**. Detecta modificación, truncamiento y reordenamiento por un proceso que no controle deliberadamente toda la cadena; **una usuaria hostil con control total de la máquina puede regenerar la cadena completa**, y eso está **fuera del threat model V0**. Un Legal Auditor **no puede venderse como garantía de inalterabilidad**, ni hoy ni cuando exista.

## Conectores Gmail / Drive / Calendar

**Por qué está fuera de V0.** **DECISIÓN APROBADA (kernel §11):** conectores externos, NINGUNO; solo Inbox local. La frontera se **diseña ahora** y se ejercita con material local — a efectos de la regla, el Inbox es una fuente externa más: **lo que reposa en `Inbox/` tampoco es evidencia hasta ser incorporado**.

**Disparador de vuelta.** La respuesta a la **pregunta de negocio 2** (canales reales de recepción), que además fija la prioridad entre conectores. **DECISIÓN PENDIENTE (ADR-006):** si el material transita por Inbox (el conector deposita, el Core ingiere) o el Core lo obtiene vía adapter detrás de `ingest_evidence`. **La regla es invariante ante ambas.**

**Qué NO debe romperse hoy.**
- **`ingest_evidence` referencia el material por identificador de Inbox resuelto por el Core, nunca por rutas arbitrarias** suministradas por el modelo.
- **EvidenceLink solo contra Evidence incorporada.** Crear un link contra una URL, un id de conector, una ruta o texto pegado **falla** — test negativo de primera clase.
- **Invariante 8 de ADR-006:** los conectores son **canales de ingestión, no dependencias de ejecución**. Ningún flujo con relevancia procesal puede depender de un token OAuth vigente ni de una cuota de API. Esta es la que se rompe con más facilidad y la más cara de recuperar.
- **`INTEGRATION_ERROR` ya existe** en la familia **Infrastructure** del catálogo de condiciones, declarada **sin disparador ejercitado en V0** (honesto, en vez de simulado). Activar un conector no exige inventar una familia nueva: exige afirmar el `effect_on_state`, que en V0 es `NONE`.
- **POR VERIFICAR:** granularidad de permisos y garantías de sandbox/filesystem del host. **El Domain no depende de ese resultado** — los modos de aprobación de conectores o las deny rules del host **pueden endurecer** el perímetro, pero **ninguno es la regla ni puede sustituirla**.

## Motor de plazos

**Por qué está fuera de V0.** Ver **Term / Deadline** en §i. Reglas de cómputo por jurisdicción no levantadas ni verificadas.

**Disparador de vuelta.** Reglas verificadas contra fuente oficial + decisión explícita de los dueños asumiendo la responsabilidad del producto.

**Qué NO debe romperse hoy.** Nada en V0 calcula, almacena ni muestra algo que se parezca a un plazo. **RIESGO de la clase más grave** — ver §i.

## Motor procesal

**Por qué está fuera de V0.** El slice no contiene lógica procesal; el scope `procedural` está reservado y `Case` no es la actuación procesal.

**Disparador de vuelta.** Levantamiento del trabajo procesal real con reglas verificadas.

**Qué NO debe romperse hoy.** El scope `procedural` permanece **reservado en el enum** (implementable sin romper el contrato); el `Case` no se convierte en espejo del expediente del juzgado; la lista cerrada de eventos no se amplía preventivamente.

---

# iii. Infraestructura

## Multi-máquina y sincronización

**Por qué está fuera de V0.** **DECISIÓN APROBADA (kernel §11):** una usuaria, una máquina. Con escritor único por caso, la concurrencia distribuida no existe como problema.

**Disparador de vuelta.** Una segunda máquina real, o la respuesta a la **pregunta de negocio 5** revelando personas que necesitan trabajar en paralelo sobre el mismo expediente.

**Qué NO debe romperse hoy.**
- **El Case Event Log append-only con `event_seq` monotónico por caso** es el registro completo de lo que le pasó al expediente. **Toda mutación produce exactamente un evento** (biyección mutación↔evento). Si algún estado se mutara por fuera del log, reconstruir o reconciliar sería imposible.
- **Concurrencia optimista con preservación: nunca sobrescritura silenciosa, nunca descarte del trabajo.** Ante conflicto, la propuesta se preserva (`PRESERVED_FOR_RECONCILIATION`) y se emite `REVISION_CHANGED`. Esa semántica —conflicto detectado, trabajo conservado, decisión devuelta a la persona— es la que cualquier sync necesitaría.

**HIPÓTESIS (no garantía):** un log append-only y hash-chained por caso es un sustrato **favorable** para una sincronización futura. **No se afirma que la resuelva**: la reconciliación entre máquinas es un problema genuinamente distinto —orden causal, conflictos semánticos, autoridad sobre la resolución— y nada de lo hecho en V0 lo soluciona. Lo que se afirma es lo contrario en fuerza: **no se está cerrando la puerta**.

## PostgreSQL

**Por qué está fuera de V0.** V0 es **local, una máquina, una usuaria**. Un servidor de base de datos añade operación, despliegue y superficie sin resolver ningún problema del slice.

**Disparador de vuelta.** Multi-máquina, multiusuario concurrente real, o volúmenes que la **pregunta de negocio 3** revele incompatibles con el almacén local.

**Qué NO debe romperse hoy.**
- **La regla de dependencias (kernel §13):** `domain` no importa `application` ni `infrastructure`; `infrastructure` **implementa puertos definidos por `application`**. Es lo único que hace sustituible la persistencia. Si el dominio conociera el motor, cambiarlo sería reescribirlo.
- El almacén concreto se fija en el documento de infraestructura correspondiente; **este registro no lo prejuzga**. **POR VERIFICAR:** las propiedades de SQLite que el corpus previo citó como HECHO VERIFICADO sin verificación en esta iniciativa (WAL, locking en filesystems de red, límites de tamaño, FTS5 y stemming español) fueron señaladas por la crítica y deben confirmarse contra documentación oficial antes de apoyarse en ellas.

## Búsqueda vectorial

**Por qué está fuera de V0.** `search_case` existe como QUERY; su implementación no requiere embeddings para el slice, y una búsqueda semántica añade un proveedor, un índice y un modo de fallo sin cubrir ninguna propiedad exigida a V0.

**Disparador de vuelta.** Volumen que haga insuficiente la búsqueda disponible (**pregunta 3**), o evidencia de que la profesional busca por concepto y no por término.

**Qué NO debe romperse hoy.**
- **Todo resultado de búsqueda debe resolver a un fragmento de Evidence incorporada.** Un índice semántico no puede convertirse en la vía por la que aparece material que nadie incorporó.
- **Los índices son derivados desechables, jamás estado primario, y jamás objetivo de escritura del modelo.** El backup los trata como desechables. Un índice vectorial futuro hereda esa condición: regenerable desde el estado canónico, nunca fuente de verdad.

## Multi-agente

**Por qué está fuera de V0.** **DECISIÓN APROBADA (kernel §11):** **0 subagentes**; un solo skill ejercitado (`fact-builder` v0).

**Disparador de vuelta.** Evidencia de que un análisis real requiere especialización que un solo skill no cubre.

**Qué NO debe romperse hoy.**
- **El techo epistémico vive en el Domain**, no en la superficie: se rechaza **con independencia de qué superficie lo transporte**. N agentes no multiplican la autoridad porque ninguno la tiene.
- **Todo evento, mutación y registro de auditoría lleva un `Principal`.** Con varios agentes, distinguir cuál actuó es exactamente para lo que `principal_id` existe.
- **`HumanAuthorization` es server-side y no viaja al modelo.** `commit_reviewed_facts` no recibe ningún secreto: el Core resuelve internamente si existe autorización válida. **Superficie de ataque: cero tokens en el contexto** — propiedad que se mantiene igual con uno o con veinte agentes, y que se perdería si alguna vez un token viajara en un prompt.
- **Una operación se expone solo si el modelo debe decidir cuándo ocurre**; si es consecuencia necesaria de otra, es interna (regla derivada del retiro de `register_artifact`).

## Actualizaciones automáticas

**Por qué está fuera de V0.** **No-objetivo de release declarado**: sin auto-update, sin firma de código, sin telemetría, sin canales, sin delta updates. Declararlo bloquea administrativamente que esta dimensión crezca hacia una plataforma de distribución y consuma el presupuesto del slice.

**Disparador de vuelta.** Más de una instalación que mantener, o una decisión de distribución comercial.

**Qué NO debe romperse hoy.**
- El mínimo V0 completo: **product version (semver) + schema version del workspace + manifest con hashes del producto sellado + verificación de integridad al arranque + migraciones numeradas solo-hacia-adelante + backup verificado antes de cada migración + degradación a solo-lectura ante fallo de integridad.** Nada más.
- **Un backup sin round-trip de restauración probado no cuenta como backup.**
- **Límite documentado y no ocultable:** sin firma, el manifest **detecta accidente, no ataque**. Mitigación barata disponible: publicar el hash del manifest de cada release fuera del equipo.
- **Rollback en dos planos que no deben confundirse:** producto (puntero a la release anterior) y datos (restaurar backup pre-migración aceptando perder lo posterior). Es un trinquete de un solo sentido, y **es preferible documentarlo a fingir reversibilidad**.

## Telemetría

**Por qué está fuera de V0.** No-objetivo de release declarado.

**Disparador de vuelta.** Necesidad de diagnóstico que el Tool Invocation Log local no cubra — y, antes de eso, una decisión de negocio explícita.

**Qué NO debe romperse hoy.**
- **PF-005:** las condiciones obligatorias de incertidumbre e integridad **no pueden suprimirse por configuración del cliente**. Un canal de telemetría no puede convertirse en la vía por la que una organización silencia avisos.
- **La configuración solo endurece, nunca relaja.**
- **Frontera a fijar desde ahora, antes de que exista el primer byte de telemetría:** **el contenido del expediente nunca sale de la máquina por esa vía.** Es más fácil sostenerla como principio declarado hoy que como excepción negociada el día que alguien quiera "solo un poco de contexto" para depurar.

## Licenciamiento

**Por qué está fuera de V0.** No-objetivo de release declarado. V0 es una instalación para una usuaria.

**Disparador de vuelta.** Decisión de comercialización.

**Qué NO debe romperse hoy.** El **Product Floor no es materia de licencia**: PF-001 a PF-005 no son características de un plan superior. Una política que previene un riesgo del dominio jurídico no puede quedar detrás de un nivel de pago — si se relajara por edición, dejaría de ser piso.

## Admin empresarial y multi-tenant

**Por qué está fuera de V0.** Una usuaria, una máquina, una organización. No existe el problema.

**Disparador de vuelta.** Segunda organización cliente, o exigencia de administración centralizada.

**Qué NO debe romperse hoy.**
- **El aislamiento entre Cases es test negativo de primera clase:** ninguna operación sobre un Case retorna datos de otro, y una operación sobre el Case A con ids del Case B se rechaza. **Esa es la propiedad sobre la que se construiría cualquier multi-tenancy** — y es infinitamente más barata de mantener desde el día uno que de retrofitear.
- **La tripleta de actor en el schema desde el inicio**, aunque hoy la llene siempre la misma persona.
- **Los identificadores son opacos, emitidos por el Core, no derivados de nombres ni de contenido.** Un id que codificara la organización sería una fuga de aislamiento disfrazada de conveniencia.

---

# iv. Plano administrativo — POST-SLICE

## Estado real: un hueco reconocido, no un diseño diferido

Conviene decirlo sin adornos, porque el corpus lo dice: la crítica de la revisión colectiva registró que **el plano administrativo no tiene dueño de diseño** — nadie especifica quién ejecuta migraciones, instala Knowledge Packs o repara instalaciones, con qué identidad y con qué auditoría. **ADR-002 lo registra como DECISIÓN PENDIENTE (post-slice).**

Este documento **no lo diseña ni lo insinúa**. Registra únicamente los **dos principios** que ya están decididos y que cualquier diseño futuro debe respetar. Todo lo demás —qué operaciones existen, cómo se autentican, qué interfaz tienen— es **DECISIÓN PENDIENTE** y no se inventa aquí.

## Principio 1 — Las operaciones ADMIN nunca se exponen al LLM

**DECISIÓN APROBADA (kernel §6; ADR-001 invariante 3).** La clase `ADMIN` está **vacía por diseño** en la superficie del modelo. Migraciones, gestión de Knowledge Packs y reparación existen **solo en el runtime/CLI del producto**, nunca como tools expuestas a Claude. **Se documenta como decisión, no como omisión.**

**Por qué es verificable y no una intención.** La cuenta en cero de la clase `ADMIN` es un **canario**: el test de superficie comprueba que el manifiesto contiene exactamente las tools V0 con su clase declarada y que `ADMIN` cuenta **cero elementos**. **Si algún día cuenta más de cero, la frontera se movió** — y se sabrá por una prueba que falla, no por una revisión de código que alguien recuerde hacer.

**RIESGO que el canario vigila — erosión incremental.** Cada tool nueva "por conveniencia" ensancha la superficie. La presión no llega como una propuesta de romper la frontera; llega como una tool pequeña y razonable.

## Principio 2 — La administración tiene identidad y auditoría independientes

**DECISIÓN APROBADA (registrada desde la revisión arquitectónica v0.1.1; ADR-002).** Instalar packs, cambiar políticas, migrar y reparar son operaciones del runtime/CLI **con identidad propia y auditoría propia**. Quien administra no es la profesional actuando sobre su expediente, y su rastro no puede confundirse con el de ella.

**RIESGO que este principio previene — deriva por conveniencia (ADR-002).** Atajos operativos —un script de reparación, una edición manual "puntual"— que escriban el private state **sin pasar por el Core** erosionan la frontera **sin dejar evento**. Un expediente reparado a mano es un expediente cuya historia miente por omisión, y el hash-chain no lo detectaría como manipulación porque nunca vio la escritura.

## Qué NO debe romperse hoy

- **`ADMIN` sigue contando cero elementos**, verificable por el test de superficie.
- **Toda mutación del Case Store ocurre vía Application** — invocada desde la superficie MCP o desde el plano administrativo del runtime/CLI, que está fuera de la superficie del modelo. **Ninguna escritura directa al private state, por ningún camino, por ninguna razón operativa.**
- **La biyección mutación↔evento se mantiene también para las operaciones administrativas** que toquen estado canónico. Una migración que mueva estado sin dejar rastro rompe la reconstrucción.
- **El Case Event Log no es desactivable ni editable por configuración** (Product Floor). Aplica al plano administrativo con más fuerza que a ninguno: es precisamente quien tendría el poder técnico de desactivarlo.
- **`DevHumanAuthorizationProvider`: FAIL TO START, no warning.** Si la configuración efectiva es de producción y el provider resuelto es el stub, **el arranque aborta**. No hay modo degradado ni advertencia ignorable. Y toda autorización emitida por el stub lleva `authorization_source = DEV_STUB` **persistido, propagado al evento y al registro de auditoría** — un `case.db` con autorizaciones `DEV_STUB` es identificable **para siempre** como caso de desarrollo. Es la pieza donde el plano administrativo y la autoridad humana se tocan, y donde un atajo sería más tentador y más grave.

## Qué queda explícitamente sin decidir

**DECISIÓN PENDIENTE (post-slice), sin propuesta en este registro:** qué operaciones administrativas existen exactamente, con qué identidad se autentica quien las ejecuta, qué registro dejan, dónde vive ese registro y si es el mismo Case Event Log o uno separado. **NO TENEMOS INFORMACIÓN SUFICIENTE** y no se propone nada: el hueco está identificado, y llenarlo con una propuesta no solicitada lo convertiría en una decisión que nadie tomó.

**Disparador que obliga a diseñarlo.** El primer momento en que una operación administrativa deba ejecutarla **alguien distinto de quien desarrolla** —una migración en la máquina de la profesional, la instalación de un pack, una reparación tras un fallo de integridad—, o la existencia de una segunda instalación. Hasta entonces, el plano administrativo tiene un solo operador que es también su autor, y esa coincidencia es lo que hace tolerable que su diseño no exista.
