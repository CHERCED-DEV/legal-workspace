# Preguntas de negocio para la profesional — siguiente ronda

**Estado:** documento de registro de la fase Technical Design V0. **No es normativo.**
**Precedencia:** nivel 6 (Discovery), kernel técnico §14. Nada de lo escrito aquí redefine una regla fijada en un ADR Accepted, en el Technical Design o en el glosario.
**Propósito:** dejar por escrito las ocho preguntas que los dueños llevarán a la profesional, con qué decisión técnica depende de cada una y cómo formularla sin jerga.

## Cómo leer este documento

- **Etiquetas:** HECHO VERIFICADO / DECISIÓN APROBADA / HIPÓTESIS / SUPUESTO / POR VERIFICAR / RIESGO / DECISIÓN PENDIENTE. Donde no hay información se dice **NO TENEMOS INFORMACIÓN SUFICIENTE**, no se rellena con plausibilidad.
- **`¿BLOQUEA el Technical Design?`** significa una sola cosa: si sin la respuesta **no puede escribirse un contrato, un invariante o una decisión** del diseño técnico V0. No significa "es importante" ni "conviene saberlo pronto". Casi todo lo importante no bloquea.
- **Ninguna de las ocho bloquea el Technical Design.** El resultado no se forzó: es consecuencia de que varias decisiones ya tomadas se tomaron **precisamente para que estas preguntas no bloquearan** (el actor triple en el schema desde el inicio, la frontera de incorporación invariante al origen, la ausencia de productor para `ProfessionalDetermination` en V0). Donde una pregunta sí condiciona algo, se dice **exactamente qué** condiciona: un nombre, un número, la operación con datos reales o el diseño de un contexto que aún no se levanta.
- **La redacción sugerida es para una profesional del derecho, no para un ingeniero.** Nombra situaciones de su oficio, no entidades del sistema. Ninguna pregunta menciona `Fact`, `Source`, `provenance` ni ningún término del glosario: si la profesional tuviera que aprender nuestro vocabulario para responder, la respuesta ya estaría contaminada por él.
- **Advertencia de método:** estas preguntas buscan **describir el trabajo real**, no validar el diseño. Una pregunta que sugiere su propia respuesta ("¿verdad que necesita X?") produce confirmación, no información. Las redacciones de abajo están escritas para que la respuesta pueda contradecirnos.

---

## 1. Significado exacto de "hecho acreditado"

**Por qué importa.** El modelo epistémico distingue lo que la profesional **alega** de lo que **da por acreditado**, y esa distinción es el eje de todo el dominio. Hoy el nombre del estado es `DETERMINED(kind = ACCREDITED_BY_PROFESSIONAL)`, elegido por nosotros a partir de una intuición del oficio, no de su vocabulario. **RIESGO registrado (ADR-003):** un nombre equivocado en la interfaz puede sugerir efectos procesales que un acto interno de la profesional no tiene — hacerle creer al sistema, y a quien lo lea después, que "acreditado" significa "probado ante la autoridad".

**Qué decisión técnica depende.** El **naming fino** del `kind` de `DETERMINED` y el texto que la usuaria ve en la interfaz. Secundariamente, si `DECLARED_PROVEN` —reservado para el contexto B— es de verdad un estado distinto o la misma palabra usada con dos sentidos. **No depende de esta respuesta** el mecanismo de transición, que exige actor humano identificado, motivación y lista explícita de links valorados incluidos los `CONTRADICTS` (ADR-003, invariantes 3 y 4).

**¿BLOQUEA el Technical Design?** **NO.** Y aquí el margen es especialmente amplio: **DECISIÓN APROBADA (addendum v0.3 B.5)** — `ProfessionalDetermination` **no tiene productor en V0**. Ninguna tool, use case ni evento de la lista cerrada produce la transición a `DETERMINED`. V0 recorre `PROPOSED → ALLEGED` y nada más. La respuesta llega mucho antes de que exista el código que la necesita.

**Redacción sugerida.**

> Cuando usted dice que un hecho ya está acreditado, ¿qué quiere decir exactamente? ¿Que usted, como profesional, ya se convenció de que ese hecho va a quedar probado con lo que tiene en la mano? ¿O que una autoridad ya lo dio por probado en una decisión? ¿Usa la misma palabra para las dos cosas, o las distingue?
>
> Y dígamelo desde el trabajo: si tuviera que explicárselo a alguien que acaba de llegar a la oficina, ¿qué tiene que pasar para que usted deje de decir "esto lo estoy alegando" y empiece a decir "esto está acreditado"? ¿Es un momento concreto, o se va dando de a poco?

---

## 2. Canales reales de recepción de evidencia

**Por qué importa.** Determina **qué puede afirmarse honestamente sobre el origen de un material y qué no**. El sistema registra un hash en el momento de la incorporación, y ese hash acredita "estos son los bytes que recibimos y cuándo" — **integridad, no autenticidad** (glosario §2). Si el material llega por un canal que no deja rastro de remitente, el sistema no puede fingir que sí lo deja. Saber cómo llega hoy el material evita que el sobre de origen prometa más de lo que el canal permite sostener.

**Qué decisión técnica depende.** El contenido del sobre de ingestión (`declared_origin`) y la metadata por tipo de origen; la **prioridad** de los conectores post-slice (Gmail antes que Drive, o al revés, según lo que ella use de verdad). **POR VERIFICAR (ADR-006, pregunta abierta):** qué metadata expone realmente cada conector — no se afirma de memoria qué campos entrega un proveedor.

**¿BLOQUEA el Technical Design?** **NO.** **DECISIÓN APROBADA (ADR-006):** V0 opera con **Inbox local únicamente**, sin conectores externos, y la frontera de incorporación se diseña de forma **invariante al origen**: los conectores cambian de dónde viene el material, no la operación que lo convierte en Evidence. Los mismos invariantes que se ejercitan hoy con archivos locales gobernarán mañana a los conectores sin cambio en Domain ni Application.

**Redacción sugerida.**

> Cuénteme cómo le llegan los documentos y las grabaciones de un caso, en la práctica y sin idealizar: ¿por correo, por WhatsApp, en una memoria USB, escaneados en la oficina, descargados de una plataforma, en papel? ¿Qué es lo más frecuente y qué es lo más incómodo?
>
> Y una que me importa mucho: cuando le llega algo, ¿de qué queda constancia de quién se lo mandó y cuándo? ¿Le ha pasado que después no pueda establecer de dónde salió un documento que ya tenía?

---

## 3. Volumen semanal

**Por qué importa.** Dimensiona almacenamiento, costo y latencia de las derivaciones (transcripción, OCR) y el presupuesto de las proyecciones. Hoy es **SUPUESTO** en todo el corpus (glosario §1, §2, §13): nadie ha dado un número y ninguna decisión debería fingir que sí.

**Qué decisión técnica depende.** Los **valores numéricos** del presupuesto por scope de `get_case_context` (pendiente abierto de ADR-004) y el dimensionamiento del almacén local. **No depende de esta respuesta** el contrato: el mecanismo `completeness ∈ COMPLETE | PARTIAL` con `omissions[]` obligatorio cuando es `PARTIAL` está fijado (kernel §9) y es correcto con cualquier volumen — lo que cambia es a partir de qué tamaño empieza a omitirse, no que la omisión se declare.

**¿BLOQUEA el Technical Design?** **NO.** V0 opera con **datos sintéticos o anonimizados, una usuaria, una máquina** (kernel §11). Los umbrales se fijan provisionalmente en implementación y quedan marcados como calibrables; ningún invariante depende de su valor.

**Redacción sugerida.**

> En una semana normal, ¿cuántos documentos nuevos entran a sus casos? ¿Y cuántas horas de audio o de video —audiencias, entrevistas, declaraciones— le caen encima?
>
> No necesito el número exacto. Quiero saber si hablamos de cinco documentos o de quinientos, y de media hora de grabación o de veinte. ¿Hay semanas atípicas? ¿Qué las vuelve atípicas?
>
> Y otra cosa: cuando un caso ya se acabó, ¿por cuánto tiempo necesita seguir teniendo todo el material a la mano?

---

## 4. Fuentes jurídicas habituales

**Por qué importa.** Es el insumo del Knowledge Pack Colombia y del futuro diseño de verificación de fuentes. Además toca el **riesgo n.º 1 del dominio**, que ya está cubierto por política: **PF-004 — jurisprudencia o normas inventadas no pueden volverse verificadas por afirmación del modelo** (kernel §12). Saber dónde consulta ella de verdad define contra qué se verificaría.

**Qué decisión técnica depende.** El contenido y las fuentes del Knowledge Pack Colombia; el diseño de `verify_legal_source` cuando exista. **POR VERIFICAR:** los términos de uso de bases de datos comerciales respecto de reproducción de contenido — no se afirma de memoria qué permite ninguna suscripción.

**¿BLOQUEA el Technical Design?** **NO**, con margen amplio. **DECISIÓN APROBADA (dueños):** `verify_legal_source` está **fuera de la superficie V0** y **ningún Knowledge Pack se carga** en el slice. V0 es un slice de caso, evidencia, hechos, memoria, provenance y autoridad humana — **no de investigación jurídica**. Hoy la única respuesta posible del sistema a "marca esta sentencia como verificada" es que la operación no existe.

**Redacción sugerida.**

> ¿Dónde consulta cuando necesita apoyar algo en derecho? ¿Qué páginas, buscadores, bases de datos o libros usa de verdad en el día a día — no los que uno debería usar, los que usa?
>
> ¿Hay alguna a la que la oficina esté suscrita y pague?
>
> Y cuando cita una sentencia o una norma en un escrito, ¿cómo se asegura hoy de que existe y de que dice lo que usted cree que dice? ¿Le ha tocado alguna vez descubrir tarde que una cita estaba mal?

---

## 5. Personas que intervienen en expedientes

**Por qué importa.** Define si la trazabilidad debe identificar **personas** o basta con la oficina. En un expediente que puede mirarse un año después, "quién hizo esto" es una pregunta con consecuencias profesionales.

**Qué decisión técnica depende.** Si `principal_id` identifica individuos o una entidad colectiva; qué valores necesita `principal_role` más allá del único valor V0 (`lawyer`); y si hacen falta perfiles con capacidades distintas por clase de operación.

**¿BLOQUEA el Technical Design?** **NO**, y es el caso más limpio de una pregunta desactivada por una decisión previa. **DECISIÓN APROBADA (ADR-003):** la tripleta de actor (`principal_id`, `principal_type`, `principal_role`) existe **en el schema desde el inicio** aunque V0 tenga una sola usuaria, **precisamente para evitar una migración dolorosa** cuando aparezcan auxiliares o roles distintos. V0 opera bajo **SUPUESTO mono-usuaria** con la deuda declarada, no bajo un schema que codifique ese supuesto.

**Redacción sugerida.**

> Además de usted, ¿quién más mete mano en un expediente? Pienso en dependientes, practicantes, la secretaria, un colega que la reemplaza en una audiencia, alguien que escanea o que radica.
>
> ¿Qué hace cada uno exactamente? ¿Alguno de ellos toma decisiones sobre el caso, o solo mueven material?
>
> Y una importante: si dentro de un año hubiera que mirar hacia atrás y saber quién hizo cada cosa en el expediente, ¿le importaría que quedara el nombre de cada persona? ¿O le basta con que quede el de la oficina?

---

## 6. Mecanismo viable de backups

**Por qué importa.** Local-only significa que **el robo del portátil destruye y expone todo a la vez**. El corpus registra el modelo de amenazas: la usuaria accidental y el fallo de hardware son los escenarios principales, y el backup con restauración probada es la mitigación de ambos. Además hay una regla dura ya fijada: **un backup sin round-trip de restauración probado no cuenta como backup** (vertical slice, criterio 10).

**Qué decisión técnica depende.** Si existe y es aceptable una **segunda ubicación** (disco externo, un servicio en la nube que la oficina ya pague) y bajo qué condiciones de confidencialidad. Condiciona la operación real, no la estructura del almacén.

**¿BLOQUEA el Technical Design?** **NO** — pero es la única de las ocho que **bloquea otra cosa con nombre propio: operar con datos reales.** El requisito V0 (backup verificado con restauración probada antes de cualquier migración) se satisface **localmente** y no necesita su respuesta. Lo que su respuesta habilita es el paso de datos sintéticos a expedientes reales, que es una decisión de negocio y no de diseño. Registrado también como **POR VERIFICAR:** disponibilidad de cifrado de disco en la edición de Windows del equipo real — no se afirma de memoria qué ofrece una edición Home.

**Redacción sugerida.**

> Hoy, si se le daña el computador o se lo roban esta noche, ¿qué pasa con sus expedientes? ¿Los perdió?
>
> ¿Tiene copia en algún otro lado — un disco externo, un servicio en la nube que la oficina ya pague, el equipo de un colega? Y si la tiene: ¿alguna vez le ha tocado recuperar algo de esa copia? ¿Funcionó?
>
> Y por el otro lado, que es igual de importante: ¿hay algún lugar donde usted **no** guardaría información de sus clientes, sea por confidencialidad o simplemente porque no se sentiría cómoda?

---

## 7. Definición del expediente oficial en contexto autoridad

**Por qué importa.** Si en el contexto de autoridad existe un **expediente digital oficial en un sistema externo**, nuestro almacén sería **copia de trabajo y no custodio primario** — lo que **invierte parte de la política de custodia** y puede cambiar qué significa "original" en ese contexto. Es una inversión, no un ajuste.

**Qué decisión técnica depende.** El diseño del contexto B completo: política de custodia (primario vs secundario), semántica de "original", y si `DECLARED_PROVEN` tiene sentido propio. Alimenta también los conceptos reservados `Ruling` y `ProceduralEvent`.

**¿BLOQUEA el Technical Design?** **NO.** V0 es **contexto A (rol `LITIGANT`) únicamente** (kernel §11). **NO TENEMOS INFORMACIÓN SUFICIENTE** sobre el contexto B: su trabajo real **no ha sido levantado**, no hay descripción validada de su flujo, sus gates ni su vocabulario. Que la primera usuaria opere ambos contextos es **SUPUESTO, no hecho verificado**, y está registrado como tal (hallazgo de la verificación de consistencia). Esta pregunta bloquea el diseño del contexto B — que no se está haciendo.

**Redacción sugerida.**

> Esta es por si usted alguna vez actúa como autoridad y no como parte — y si no lo hace, dígamelo y saltamos la pregunta.
>
> Cuando le toca decidir, ¿cuál es el expediente que vale? ¿El que está en el sistema de la entidad, o el que usted arma para poder trabajar?
>
> Si son dos: ¿cuál manda? ¿Qué pasa si no coinciden? Y lo que usted tiene en su computador, ¿sería una copia de trabajo suya, o sería el expediente mismo?

---

## 8. Ritmo de trabajo que afecta performance y experiencia de uso

**Por qué importa.** Dos afirmaciones cuantitativas sobre el ritmo de trabajo circulan por el corpus sosteniendo decisiones de arquitectura. La verificación de veracidad las señaló: *"el propio corpus declara que el ritmo real de trabajo, el volumen y la latencia son preguntas de negocio abiertas y SUPUESTO. Aquí esas magnitudes se usan sin etiqueta como fundamento fáctico"*. Se corrigieron a `SUPUESTO` (addendum v0.3 B.11), pero el addendum dejó abierto un punto que **esta pregunta cierra**: *"Las etiquetas SUPUESTO de B.11 remiten a preguntas de negocio que aún no existen como tales"* (addendum v0.3 §D.4). **Aquí existen.** Ver la sección siguiente.

**Qué decisión técnica depende.** El **fundamento declarado** —no el contenido— de dos decisiones: separar el Tool Invocation Log del Case Event Log, y rechazar el locking pesimista en favor de concurrencia optimista. Además, con valor propio: el valor por defecto de `expires_at` de la `HumanAuthorization` (**SUPUESTO a validar**, ADR-005: ¿minutos, una sesión de trabajo?); el tamaño de propuesta que puede revisarse con atención real, que es insumo directo contra el **RIESGO de fatiga de revisión** (ADR-005); y el presupuesto de latencia por clase de operación, un hueco que la crítica señaló sin dueño: *"ninguna respuesta de UX define qué ve la usuaria durante operaciones de minutos"*.

**¿BLOQUEA el Technical Design?** **NO**, y conviene ser exacto sobre por qué. **Las dos decisiones que estos supuestos sostienen no cambian con la respuesta.** ADR-004 lo dice de sí mismo: la separación de logs se mantiene aunque las lecturas no sean más frecuentes que las mutaciones —el Tool Invocation Log seguiría siendo no canónico, no hash-chained y podable—, y la concurrencia optimista con preservación protege el estado sin bloquear a nadie con independencia de cuánto dure un análisis. Lo etiquetado como supuesto es **el fundamento cuantitativo declarado, no la decisión**. Si la profesional nos contradice, corregimos una frase, no un diseño.

**Redacción sugerida.**

> Descríbame una tarde típica trabajando un caso. ¿Cuánto tiempo seguido le dedica a un mismo expediente antes de pasar a otra cosa?
>
> Mientras está metida en un expediente, ¿es normal que le entre material nuevo **de ese mismo** expediente? ¿O eso pasa en otros momentos, cuando no está trabajándolo?
>
> ¿Qué hace más veces a lo largo del día: consultar y releer lo que ya tiene, o meter cosas nuevas?
>
> Y una sobre la paciencia: cuando le pide a alguien —o a un programa— algo que se demora, ¿cuánto está dispuesta a esperar antes de que le estorbe? ¿Prefiere dejarlo corriendo y seguir con otra cosa, o quedarse esperando hasta que termine? ¿Le molesta que le avisen a mitad de camino, o lo agradece?
>
> Última: cuando le toca revisar y aprobar cosa por cosa, ¿cuántas puede mirar seguidas **con atención de verdad** antes de empezar a aprobar en piloto automático? Dígame el número honesto, no el que suena bien.

---

## BUSINESS ASSUMPTIONS — NON BLOCKING

Supuestos de ritmo de trabajo que el corpus venía arrastrando como si fueran datos. Quedan aquí registrados con etiqueta explícita y **vinculados a la pregunta 8**, que es la que puede confirmarlos o desmentirlos.

Esta sección es la **descarga del punto §D.4 del addendum v0.3**, que exigía o crear las preguntas de negocio correspondientes o redirigir las etiquetas. Se optó por crearlas: la pregunta 8 existe y estos dos supuestos cuelgan de ella.

### BA-01 — Frecuencia de lecturas frente a mutaciones

> **SUPUESTO (a validar con uso real; pregunta 8).** Las lecturas son **órdenes de magnitud más frecuentes** que las mutaciones.

- **Dónde se usa:** ADR-004 §(b)2, como fundamento del volumen esperado que justifica mantener el Tool Invocation Log separado del Case Event Log.
- **Qué sostiene:** el fundamento cuantitativo de la separación, **no la separación**.
- **Qué pasa si es falso:** nada estructural. El Tool Invocation Log seguiría siendo no canónico, no hash-chained y podable, porque no forma parte de la historia del expediente — que es la razón cualitativa y es independiente del volumen. Cambiaría la política de retención y el dimensionamiento, no el contrato.
- **Cómo se confirmaría:** con la respuesta a la pregunta 8 ("¿qué hace más veces: consultar o meter cosas nuevas?") y, definitivamente, con el propio Tool Invocation Log una vez haya uso real — el instrumento que mediría este supuesto es uno de los que el supuesto justifica.

### BA-02 — Duración típica de un análisis

> **SUPUESTO (a validar con uso real; pregunta 8).** El escritor típico es un agente cuya operación **dura minutos**, de modo que un lock bloquearía a la usuaria —por ejemplo, para incorporar un documento— durante todo un análisis.

- **Dónde se usa:** ADR-004 Alternativas §4 (rechazo del locking pesimista) y vertical slice V0, sección *Revision behavior*.
- **Qué sostiene:** el fundamento del rechazo del locking pesimista, **no el rechazo**.
- **Qué pasa si es falso:** nada estructural. Si los análisis fueran de segundos, la concurrencia optimista con preservación sigue siendo correcta: protege el estado sin bloquear a nadie y **sin descartar trabajo**, que es la propiedad que se quería. Un análisis corto simplemente hace menos probable el conflicto; no lo vuelve mal manejado.
- **Riesgo asociado que sí depende del número:** los **conflictos espurios**. Cuanto más largo el análisis y más frecuentes las incorporaciones intercaladas, más veces una incorporación irrelevante invalidará trabajo que no dependía de ella (**RIESGO registrado en ADR-004**). El plan de granularidad ya está declarado —si molesta, pasar a revisiones por agregado **antes** que a locking—, y la pregunta 8 mide si molestará de verdad o solo en teoría.

### Nota sobre la naturaleza de ambos supuestos

Los dos comparten una propiedad que conviene no perder de vista: **son supuestos sobre el mundo, medidos por un sistema que aún no se usa.** Ninguna respuesta en una conversación los confirma con precisión — una profesional puede estimar mal su propio ritmo sin faltar a la verdad. La pregunta 8 sirve para **detectar un orden de magnitud equivocado**, que es todo lo que necesitamos: ninguna de las dos decisiones que sostienen es sensible a un error de factor dos, y ambas se revisan con datos del uso real cuando los haya.

**POR VERIFICAR** queda, en consecuencia, el umbral a partir del cual conviene pasar a revisiones por agregado (`facts_rev`, `evidence_rev`, `artifacts_rev`), que ADR-004 ya registra como pendiente y que solo el uso real puede fijar.

---

## Preguntas que este documento NO recoge

Registrado para que la omisión sea visible y deliberada. El corpus contiene otras preguntas de negocio abiertas que **no** entran en esta ronda de ocho, y no por ser menos importantes:

- Granularidad real del par "hecho, prueba" — por cláusula, por página, por pasaje (glosario §6). Hoy es **SUPUESTO** derivado del flujo aprobado del slice.
- Cómo imagina materialmente aprobar algo — una ventana propia, la revisión de un documento, otra forma (glosario §12). Define cuánta interfaz propia exige el diseño del canal humano.
- Si una misma instalación atenderá asuntos de contextos distintos con obligaciones de confidencialidad distintas (glosario §3). Parcialmente cubierta por la pregunta 7.
- Presupuesto aceptable de costo por operación de derivación y análisis (glosario §9), que es pregunta **a los dueños** antes que a la profesional.

Ninguna bloquea el Technical Design V0. Se dejan registradas para la ronda siguiente.
