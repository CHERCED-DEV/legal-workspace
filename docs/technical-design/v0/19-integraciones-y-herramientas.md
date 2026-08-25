# 19 — Integraciones y herramientas del anfitrión

> **Estado:** PROPUESTA de diseño. No autoriza implementación.
> **Insumo obligatorio:** `docs/research/capacidades-suscripcion-claude.md` (verificado 2026-08-25). **Este documento solo diseña sobre capacidades verificadas allí**; lo demás va marcado `POR VERIFICAR` y no se da por hecho.
> **Norma que gobierna:** ADR-006 (`Accepted`) — **EXPLORATION ≠ CASE EVIDENCE**.

---

## 0. La petición y la respuesta corta

Los dueños pidieron *«usar todo lo que tenga Claude a disposición… que se conecte con su OneDrive, que le permita hacer cosas de Office y demás herramientas de trabajo»*. Es la dirección correcta y ya estaba prevista: el prompt maestro §20 declara la intención de aprovechar lo que el cliente ya paga.

La respuesta corta, tras verificar:

- **Sí a Office, y con más fuerza de lo esperado** — pero por una vía distinta de la que se suponía: **el complemento de Word**, no un conector.
- **OneDrive: probablemente no, y no por culpa del plan de Claude.** El conector exige cuenta Microsoft corporativa en un tenant de Entra y consentimiento de un administrador global. Con OneDrive personal **no se activa**. Es un requisito de Microsoft, no de Anthropic.
- **Lo que no cambia con ningún conector:** nada de lo que el modelo *ve* se convierte en prueba del expediente. Eso lo decide ADR-006, y ningún plan lo compra.

**Y una advertencia que hay que decir antes que cualquier lista de capacidades: cada conector nuevo no solo añade poder, añade superficie donde el modelo puede confundir «lo que vi» con «lo que está en el expediente».** El resto del documento existe para que esa confusión sea imposible de cometer en silencio.

---

## 1. Las tres clases de uso — la distinción que ordena todo

Toda capacidad del anfitrión cae en **exactamente una** de estas tres clases. Clasificar antes de conectar es lo que impide que el perímetro se erosione una integración a la vez.

| Clase | Qué es | ¿Toca el estado canónico? | Vía |
|---|---|---|---|
| **EXPLORAR** | El modelo mira algo para orientarse: un archivo en la nube, una página, un documento abierto | **No.** No deja rastro en el expediente | Libre, con las cautelas de §5 |
| **INCORPORAR** | Un material pasa a ser evidencia del caso: copia de bytes, hash, procedencia | **Sí** | **`ingest_evidence`. Única vía. Sin excepciones** |
| **PRODUCIR** | El sistema genera algo para ella: un borrador, una tabla, un resumen | **No.** Lo producido **no es prueba de nada** | Sale por `3-Para presentar/` |

### 1.1 Dónde cae cada capacidad verificada

| Capacidad del anfitrión | Clase | Nota |
|---|---|---|
| Conector M365 buscando en OneDrive/SharePoint | **EXPLORAR** | Aunque encuentre el contrato exacto que prueba el hecho |
| Conector M365 leyendo Outlook | **EXPLORAR** | Un correo leído por el conector **no es** el correo aportado al expediente |
| Integración de Google Drive | **EXPLORAR** | Solo Google Docs, solo texto extraído (§A del inventario) |
| Búsqueda web | **EXPLORAR** | |
| Claude para Word leyendo el documento abierto | **EXPLORAR** | |
| **`ingest_evidence` del Core** | **INCORPORAR** | **La única** |
| Creación de `.docx` / `.xlsx` / `.pdf` desde la conversación | **PRODUCIR** | |
| Claude para Word editando en control de cambios | **PRODUCIR** | Con la particularidad de §3.2 |
| Conector M365 escribiendo en SharePoint | **PRODUCIR** | Y ver §2.3: recomendamos no habilitarlo |

### 1.2 Por qué la confusión entre EXPLORAR e INCORPORAR es el riesgo central

Porque **no se siente como un error**. Si el conector encuentra el contrato y el modelo dice *«el contrato establece un plazo de treinta días»*, la frase es verdadera, útil y suena a trabajo bien hecho. Lo que no se ve es que:

- **no hay copia** — si el archivo cambia mañana, el respaldo de esa afirmación cambió sin que nadie lo sepa;
- **no hay hash** — no se puede demostrar sobre qué versión se trabajó;
- **no hay procedencia** — no consta quién lo aportó ni cuándo entró;
- **no hay fragmento citable** — la cita no ancla a nada estable.

El daño no aparece el día en que se explora. Aparece **el día en que hay que sostener el hecho**, cuando ya nadie recuerda de dónde salió. Por eso la frontera no puede depender de que el modelo se acuerde: tiene que estar en el **tipo de operación disponible**. Explorar no ofrece ninguna herramienta que mute el Case; para mutarlo hay que pasar por `ingest_evidence`, que exige la copia.

> **Corolario de diseño, en una línea:** *la frontera no se defiende con advertencias en un prompt; se defiende porque la operación que la cruzaría no existe.*

---

## 2. OneDrive

### 2.1 Estado real — hay que decirlo antes de diseñar nada

**HECHO VERIFICADO:** el conector de Microsoft 365 —la única vía documentada a OneDrive— exige *«una cuenta Microsoft de trabajo o de estudios en un tenant de Microsoft Entra»* y **excluye las cuentas personales**. Exige además consentimiento de un **Administrador Global de Entra**, incluso en Free/Pro/Max.

**DECISIÓN PENDIENTE — V-1, la pregunta más urgente y más barata del proyecto:** ¿su OneDrive es personal o corporativo? Se resuelve preguntándole con qué correo entra. De la respuesta depende si esta sección entera es aplicable o teórica.

**RIESGO, si es personal:** no hay sustituto. No existe conector de OneDrive independiente (`NOT FOUND`), y la carpeta sincronizada de OneDrive en el disco **sí** es alcanzable por Cowork como carpeta local — pero eso ya no es «el conector de OneDrive», es el Inbox local que el slice v0 ya contempla, y conviene no venderlo como otra cosa.

### 2.2 Si está disponible: cómo se usa

**EXPLORAR.** El conector responde preguntas del tipo *«¿tengo algo de este cliente?»* sin que ella suba nada. Vale sobre todo para **encontrar** — es el buscador de un almacén que ella no tiene ordenado.

**INCORPORAR desde ahí.** Nunca automático. El recorrido es:

1. El conector encuentra el archivo y el modelo lo dice, **etiquetado como no incorporado** (§4).
2. Ella decide incorporarlo.
3. El archivo se trae al **Inbox local** del caso.
4. `ingest_evidence` hace la copia inmutable, el hash y el registro de procedencia.

**SUPUESTO explícito, no verificado (V-7):** el paso 3 requiere que el archivo llegue al disco. Con OneDrive sincronizado en Windows eso es trivial —ya está en el disco—; sin sincronización, hay que descargarlo. **No hemos verificado que el conector pueda escribir un archivo al disco local**, y no lo damos por hecho.

### 2.3 Escritura hacia OneDrive: recomendamos **no habilitarla**

**INCONCLUSIVE:** la documentación oficial se contradice sobre si la escritura alcanza OneDrive o solo SharePoint.

Pero incluso si alcanzara: la escritura del conector es una vía por la que el modelo modifica archivos **fuera de toda revisión del Core**, en un almacén que contiene material de todos sus casos. No compra nada que no dé la clase PRODUCIR con entrega local, y abre una superficie de daño desproporcionada. **PROPUESTA: mantener las write tools desactivadas.**

### 2.4 Qué pasa si el original externo cambia o desaparece

Nada que afecte al expediente. Es el punto entero de INCORPORAR: `ingest_evidence` guarda **la copia**, no un enlace. La copia es inmutable (ADR-006, `PF-002`).

Lo que sí se registra es el **desajuste**: si más tarde se comprueba que el original externo ya no existe o su contenido difiere del hash guardado, eso es un hecho sobre el mundo, se anota como tal y **no altera la evidencia**. La prueba sigue siendo lo que se incorporó; el desajuste es información sobre la fuente, no una corrección del expediente.

### 2.5 Regla dura: OneDrive nunca es el almacén del expediente

Ni ahora ni con conector ni con plan de empresa. El expediente vive donde ADR-002 lo pone y §17 lo ubica, con copias de respaldo según ADR-013. Un almacén en la nube gobernado por un tercero, sincronizado, con papelera propia y con acceso desde cualquier dispositivo, **no cumple ninguna de las propiedades que hacen defendible un expediente**: ni inmutabilidad, ni control de escritura, ni trazabilidad de quién tocó qué.

---

## 3. Office

### 3.1 Producir archivos desde la conversación — disponible ya, incluso en plan gratuito

**HECHO VERIFICADO:** creación de `.docx`, `.xlsx`, `.pptx` y `.pdf`, en Free/Pro/Max por defecto, hasta 30 MB por archivo.

**Dónde caen.** Los archivos producidos se entregan en `3-Para presentar/` del caso (§17). Nunca en `1-Documentos recibidos/`: esa carpeta es de material que **entra**, y confundirlas es exactamente el error de §1.2 con forma de carpeta.

**Regla dura, sin matices: un documento producido por el sistema no es prueba de nada.** No puede citarse como respaldo de un hecho, no puede incorporarse como evidencia del caso del que salió, y su existencia no acredita nada sobre el mundo. Un resumen de la declaración no es la declaración. Es trabajo, no prueba. Si alguna vez un documento producido tuviera que entrar como evidencia —por ejemplo, porque se presentó y la contraparte respondió a él—, entra **como cualquier otro material: por `ingest_evidence`**, y lo que consta entonces es *«este escrito fue presentado»*, no *«lo que dice este escrito es cierto»*.

### 3.2 El complemento de Word — el hallazgo más valioso, y hay que decir por qué

**HECHO VERIFICADO:** *Claude para Word* está disponible en **Pro y Max**, se instala desde Microsoft AppSource **sin administrador de Entra**, y trabaja **solo sobre el documento abierto**.

Por qué importa más que los conectores:

| Lo que hace | Por qué encaja con este proyecto |
|---|---|
| **Modo control de cambios**: cada edición aparece como revisión aceptable o rechazable en el panel nativo de Word | Es **autoridad humana con la interfaz que ella ya conoce**. No hay que enseñarle nada. La propuesta del modelo y la aceptación de la persona ya están separadas por Word |
| Citas por sección clicables | Es anclaje verificable, que es la mitad del método de `fact-builder` |
| Resumir el redlining de la contraparte | Es trabajo real de litigio, no una demo |
| Trabajar hilos de comentarios uno a uno | Es cómo se revisa de verdad un escrito |
| **Las Skills habilitadas aplican dentro de Word** | **`fact-builder` podría operar dentro de Word.** Habilita una medición del baseline que no habíamos previsto |

**Alcance acotado, y eso es una virtud:** *«Solo accede al documento que usted tiene abierto en Word»*, y *«no puede crear, abrir, cerrar ni cambiar de archivo directamente»*. Un perímetro estrecho impuesto por el fabricante, que además es **posicional** —lo que está abierto— y no depende de reglas que el modelo pueda ignorar. Es la misma forma de perímetro que el spike de Cowork nos obligó a adoptar.

**RIESGO ALTO, documentado por el propio fabricante:** *«Use Claude para Word solo con documentos de confianza. Documentos de fuentes externas como plantillas descargadas, archivos de la contraparte o archivos compartidos por correo pueden contener instrucciones ocultas»*.

**Esto no es un caso límite para una abogada: leer documentos de la contraparte es el trabajo.** No descalifica la herramienta —el fabricante la vende explícitamente para revisar redlining—, pero fija tres reglas:

1. **Con material adverso, el modo de control de cambios va activo siempre.** Toda edición queda como revisión rechazable.
2. **Ninguna acción no supervisada sobre documentos externos.** El complemento pide confirmación ante operaciones de riesgo; esas confirmaciones se leen, no se despachan.
3. **El complemento no toca el expediente.** Trabaja sobre un archivo de la zona de trabajo. Lo que produzca entra al expediente solo por `ingest_evidence`, como todo.

**RIESGO adicional, verificado y que conviene que los dueños sepan:** el complemento *«no hereda la configuración personalizada de retención de datos»* de la organización, su actividad *«no se incluye en registros de auditoría ni en la Compliance API»*, y su historial vive en el navegador. Si en algún momento hay compromisos de confidencialidad con clientes, esta herramienta queda fuera de esos controles y hay que decirlo antes, no después.

**Y la limitación que hay que citar textualmente a los dueños:** el fabricante desaconseja el complemento para *«presentaciones judiciales o documentos críticos para auditoría sin verificación»* y para *«sustituir el juicio jurídico»*. Coincide punto por punto con nuestro propio principio: el sistema propone, la profesional decide. No es una objeción al uso: es la confirmación de que la arquitectura de autoridad humana no es una precaución nuestra, sino la condición de uso del fabricante.

### 3.3 Requisitos que hay que comprobar antes de prometerlo

| # | Requisito | Estado |
|---|---|---|
| V-2 | Plan Pro o Max de Claude | POR VERIFICAR |
| V-3 | Suscripción a Microsoft 365, Word versión 2205 build 15202.10000 o posterior en Windows | POR VERIFICAR. **Word 2016/2019 perpetuo NO sirve** |
| — | Documentos en `.docx`; `.doc` heredado no soportado | Consecuencia práctica: material antiguo hay que convertirlo |

---

## 4. Cómo se le hace visible a **ella** la diferencia

Es la parte de mayor valor práctico del documento. La frontera de §1 solo funciona si ella puede verla sin que nadie le explique arquitectura.

### 4.1 El principio de redacción

**Nunca se le dice al usuario dónde vive un archivo. Se le dice qué se puede hacer con él.** «Está en OneDrive» no significa nada para su trabajo. «Todavía no cuenta como prueba del caso» sí.

### 4.2 Cuando el sistema encuentra algo que no está incorporado

> **Encontré un archivo que parece del caso: «Contrato Pérez–Alfa.docx», guardado en su nube el 12 de marzo.**
>
> Lo he leído para orientarme, pero **todavía no forma parte del expediente**: no puedo usarlo para sostener ningún hecho hasta que usted lo incorpore.
>
> **¿Lo incorporo al caso?** Al hacerlo guardo una copia propia que ya no cambia aunque el original se modifique o se borre.

Tres cosas hace ese texto, y ninguna es decorativa: **declara que lo leyó** (no oculta el acceso), **declara la consecuencia en términos de su trabajo** (no puede sostener un hecho), y **explica qué gana al incorporarlo** (una copia que no cambia), que es la razón real de la operación.

### 4.3 Cuando ella pide algo que exigiría cruzar la frontera

> Usted me pide que añada como hecho que el plazo era de treinta días, y ese dato lo vi en el contrato de su nube.
>
> **No puedo apoyarlo en ese archivo: no está en el expediente.** Puedo incorporarlo primero —tarda un momento— y después proponer el hecho con su respaldo. ¿Lo hago?

El sistema **no dice que no puede hacer el trabajo**. Dice cuál es el paso que falta y se ofrece a darlo. Una frontera que se percibe como un obstáculo se rodea; una que se percibe como un paso se recorre.

### 4.4 Marcado permanente, no solo en el momento

Todo lo que provenga de exploración lleva marca **mientras siga sin incorporarse**, no solo la primera vez. En la práctica, tres reglas:

| Regla | Por qué |
|---|---|
| Un hecho apoyado en material no incorporado **no puede pasar de `PROPOSED`** | Es la traducción exacta de ADR-006 al modelo de estados. La frontera es de estado, no de redacción |
| El resumen del caso lista aparte **«visto pero no incorporado»** | Para que el vacío sea visible sin tener que recordarlo |
| El lenguaje distingue siempre **«vi»** de **«está en el expediente»** | Dos verbos distintos para dos cosas distintas. Si el vocabulario los mezcla, el usuario los mezclará |

### 4.5 Lo que **nunca** se le dice

| Prohibido | Por qué |
|---|---|
| «Ya tengo el contrato» | Falso si no está incorporado. «Tener» sugiere posesión estable |
| «Según el expediente…» sobre material explorado | Miente sobre el origen. Es el error de §1.2 en una preposición |
| Jerga: hash, snapshot, provenance, conector, MCP | Nada de esto ayuda a decidir |
| «Lo incorporé automáticamente para agilizar» | **Incorporar es decisión suya, siempre.** Un atajo aquí destruye la única garantía que el sistema ofrece |

---

## 5. El modo Auto de aprobación de herramientas

**HECHO VERIFICADO (spike Cowork):** los conectores tienen modos de aprobación Manual / Auto / Skip, y **el modo Auto delega la decisión de seguridad en el propio modelo**.

**RIESGO:** eso convierte al modelo en su propio guardián — precisamente lo que ADR-001 declara inaceptable. Y se agrava con conectores: en modo Auto, un documento con instrucciones ocultas puede desencadenar llamadas a herramientas que nadie aprobó, y el conector que las ejecuta tiene acceso legítimo a todo lo que ella puede ver.

**PROPUESTA:**

| Clase de operación | Modo | Por qué |
|---|---|---|
| Lectura y búsqueda (EXPLORAR) | **Auto aceptable** | El daño de una lectura de más es acotado. Exigir aprobación en cada lectura entrena a aprobar sin leer, que es peor |
| Cualquier escritura hacia el exterior | **Manual, y por defecto desactivada** | §2.3 |
| Cualquier operación del Core que mute el Case | **Manual, siempre** | Y además el Core no depende de ello: `commit_reviewed_facts` exige autorización explícita por ítem (ADR-005). Aunque el anfitrión aprobara sola la llamada, **la mutación no ocurre sin la autorización humana registrada** |

**Nota de diseño, y es la que importa:** la última fila describe la propiedad que hace tolerable todo lo anterior. **No confiamos en la configuración de aprobación del anfitrión para la corrección del expediente.** Si mañana cambia el modo por defecto, o alguien lo pone en Auto sin pensarlo, el expediente sigue siendo correcto. La configuración es defensa en profundidad; la garantía está en el Core.

---

## 6. Qué se activa y cuándo

### 6.1 Slice v0: **ningún conector externo**

Se mantiene lo aprobado en ADR-006: solo Inbox local. Razón: el valor a demostrar en v0 es que **el ciclo hecho–prueba–autorización funciona**. Un conector no aporta a esa demostración y multiplica las formas de fallar.

### 6.2 Condiciones para activar el primero

Ninguna integración se activa hasta que se cumplan **todas**:

| # | Condición | Por qué es previa |
|---|---|---|
| C-1 | El ciclo `ingest_evidence → propose_facts → commit_reviewed_facts` funciona sobre Inbox local | Si INCORPORAR no está sólido, ampliar EXPLORAR solo aumenta lo que no se puede incorporar |
| C-2 | El marcado de §4.4 está implementado y **se ha probado que un hecho apoyado en material no incorporado no puede pasar de `PROPOSED`** | Es la frontera. Sin ella, el conector la borra el primer día |
| C-3 | El lenguaje de §4.2–§4.3 se ha probado con ella y lo entiende sin explicación previa | Si hay que explicarlo, no funciona |
| C-4 | Los requisitos de cuenta y plan están verificados (V-1 a V-3) | Para no diseñar sobre algo inalcanzable |

### 6.3 Orden propuesto — por relación valor/riesgo, no por vistosidad

| Orden | Integración | Valor | Riesgo | Razón |
|---|---|---|---|---|
| **1.º** | **Complemento de Word** | Alto | Medio | **No es un conector**: no toca el expediente, su perímetro es el documento abierto, y su interfaz de aprobación —control de cambios— ya la conoce ella. Es lo más valioso por lo menos invasivo. **Y no requiere nada del Core: puede probarse la semana que viene** |
| 2.º | Producción de `.docx` y `.xlsx` | Alto | Bajo | PRODUCIR es la clase menos peligrosa. Disponible ya |
| 3.º | Búsqueda en OneDrive/SharePoint, solo lectura | Medio | Medio | Solo si V-1 lo permite. Resuelve *«¿dónde está aquello?»*, que es dolor real |
| 4.º | Correo y calendario | Bajo aquí | Alto | Superficie de inyección grande, valor pequeño para el cuello de botella declarado. **No se propone** |
| Nunca | Escritura hacia almacenes externos | — | Alto | §2.3 |

---

## 7. Lo que **no** se debe construir

| No construir | Por qué |
|---|---|
| **Un adapter propio de OneDrive, Word o Excel** | Duplica lo que el anfitrión ya hace, hereda la obligación de mantenerlo, y —lo decisivo— **crearía una vía de acceso a material externo que corre dentro de nuestro proceso**, es decir, del lado confiable de la frontera. Lo que el anfitrión hace, que lo haga el anfitrión: así queda del lado no confiable, que es donde debe estar |
| **Un `ingest_from_connector` o cualquier tool que incorpore sin copia local** | Sería `ingest_evidence` sin lo único que lo hace valer: la copia, el hash y la procedencia |
| **Cualquier vía por la que un conector escriba en el estado canónico** | ADR-002. El expediente no es alcanzable desde el anfitrión, y un conector es anfitrión |
| **Sincronizar el expediente a la nube** | §2.5 |
| **Un modo «confiar en este conector» que salte la revisión humana** | La revisión humana no es fricción a optimizar: es el producto |
| **Presentar el conector M365 como disponible antes de resolver V-1** | Prometer una capacidad que un requisito de terceros puede volver imposible |

---

## 8. Efecto sobre decisiones ya tomadas

| Documento | Efecto | Estado |
|---|---|---|
| ADR-006 | **Ninguno.** Este documento lo operacionaliza; no lo modifica | Sin cambios |
| ADR-001 | **Ninguno.** §5 refuerza que la corrección no depende de la configuración del anfitrión | Sin cambios |
| ADR-012 (distribución) | **Posible impacto.** Se verificó que los plugins *«combinan conectores MCP, Skills, comandos y sub-agentes»*, están disponibles *«en Claude Code y Cowork»*, y que un servidor local puede distribuirse *«incluido en un plugin usando `.mcp.json`»*. Si se confirma en la práctica, **el plugin sería el vehículo de instalación** del Core y de `fact-builder` a la vez — y el `git pull` de ADR-012 seguiría siendo el mecanismo de actualización | **DECISIÓN PENDIENTE — depende de V-4** |
| §17 layout | Añadir que `3-Para presentar/` es también el destino de lo producido por el anfitrión (§3.1) | Enmienda menor pendiente |
| Baseline | **Oportunidad nueva:** el complemento de Word permite medir `fact-builder` dentro de Word, sin Core y sin instalar nada nuestro | Pendiente de valorar |

---

## 9. Preguntas abiertas

| # | Pregunta | Bloquea |
|---|---|---|
| V-1 | ¿OneDrive personal o corporativo en Entra? | Toda la §2 |
| V-2 | ¿Qué plan de Claude? | Complemento de Word (§3.2) |
| V-3 | ¿Microsoft 365 y qué versión de Word? | Complemento de Word |
| V-4 | ¿Se puede instalar un MCP local en Cowork con su plan, y por qué vía? | **La implementación entera.** Previa a B-04 |
| V-5 | ¿Un conector remoto alcanza el disco local? | Si no, la vía local es la única |
| V-7 | ¿Puede el conector M365 dejar un archivo en el disco local? | El paso 3 de §2.2 |
| D-19 | ¿Se acepta no habilitar nunca escritura hacia almacenes externos? | §2.3, §7 |
| D-20 | ¿Se acepta el orden de §6.3, con el complemento de Word primero y correo descartado? | §6 |
