# fact-builder — Formato de salida

**Qué es este archivo.** El **contrato de entrega** del skill `fact-builder`: la forma exacta en que el trabajo sale del modelo. El *método* —cómo leer la entrevista, cómo descomponerla, cómo emparejar hecho y prueba, cómo reconocer lo que no tiene soporte— vive en el resto del skill. Aquí solo se fija **cómo se entrega lo que el método produjo**.

**Fecha:** 2026-08-25. **Estado:** primera versión ejecutable del modo 1; el modo 2 depende de contratos todavía en propuesta (ver §3.1).

**Regla que gobierna todo el documento:**

> El método es el mismo en los dos modos. **Lo único que cambia es el destino de la salida.** Si algún día hay que cambiar el método para que quepa en un formato, el formato está mal, no el método.

**Este archivo tiene dos audiencias y no se mezclan:**

| Sección | Para quién | Vocabulario |
|---|---|---|
| §1 y §2 (modo 1: plantilla y ejemplo) | La profesional, que lo lee en pantalla | Español corriente. **Cero jerga técnica**: ni identificadores, ni huellas de contenido, ni nombres de campos |
| §3 (modo 2) y §4 (garantías) | Quien construye el Core y quien adjudica el baseline | Nombres técnicos del proyecto, en inglés donde el proyecto los fijó |

Lo de §3 **nunca aparece en lo que ella lee**. Un documento del modo 1 que contenga un nombre de campo, un identificador opaco o la palabra "hash" es un documento mal producido.

---

## 1. Modo 1 — sin Core (el que se usa esta semana)

Contexto: el skill se carga en Cowork tal cual, sin base de datos, sin servidor, sin nada que valide. La salida es **texto que la profesional lee**.

### 1.1 Qué garantiza este modo: nada

Dicho sin rodeos, porque de esto depende que el baseline mida algo real:

**En el modo 1 no hay ninguna garantía técnica. Ninguna.** En concreto, nada impide que el modelo:

- no use este formato, o lo use a medias;
- escriba una cita literal **que suena perfecta y no existe**;
- atribuya una cita real al documento equivocado, o a la página equivocada;
- diga que leyó un archivo que no pudo abrir;
- omita en silencio un hecho importante;
- cambie la numeración entre una pasada y otra;
- presente como respaldado algo que solo está afirmado.

**La única verificación que existe en este modo es la lectura de la profesional, con el material delante.** No hay segunda línea de defensa.

Lo único que el formato puede hacer —y para eso está diseñado— es **abaratar la comprobación**: poner la cita literal y su coordenada exacta al lado del hecho, de modo que verificar un hecho cueste una sola mirada al documento. El formato no impide el error; hace barato encontrarlo.

**Riesgo propio de este modo, que conviene nombrar:** como no existe expediente, tampoco existe la contaminación del expediente. El peligro se mueve de sitio: es que este texto se copie directamente dentro de un escrito. Por eso el documento abre siempre con la advertencia de la plantilla y por eso ningún hecho se escribe con palabras de conclusión.

### 1.2 Las cinco partes fijas del entregable

Siempre las cinco, siempre en este orden, aunque alguna quede vacía (y si queda vacía, se dice que quedó vacía):

1. **Encabezado de la pasada** — de dónde salió todo esto y qué se leyó.
2. **Hoja de decisiones** — la lista completa en una tabla, para decidir de un vistazo.
3. **Las fichas** — un hecho por ficha, con sus pruebas.
4. **Lo que no se convirtió en hecho** — y por qué.
5. **Lo que se buscó y no se encontró** — con la advertencia de qué significa eso y qué no.

Las partes 4 y 5 no son relleno. Son la mitad del valor: la parte 4 evita que el descarte sea invisible, y la parte 5 impide que una búsqueda fallida se lea como prueba de que algo no existe.

### 1.3 Reglas de redacción

**Del enunciado del hecho:**

- **Una proposición por hecho.** Si al leerlo en voz alta hay un "y" que une dos cosas que podrían ser ciertas por separado, son dos hechos.
- **Comprobable en principio**: alguien podría, con el material adecuado, decir si ocurrió o no. Si nadie podría, no es un hecho.
- **Sin adjetivos de valor y sin calificación jurídica.** "Se entregó la máquina el 9 de abril" es un hecho. "Se entregó tarde" es una valoración. "Incumplió" es una calificación, y no le corresponde a este skill.
- **Palabras prohibidas dentro de una ficha:** *probado, acreditado, demostrado, queda claro, evidentemente, sin duda*. El skill nunca declara nada probado. Escribe qué dice el material y quién lo dice.
- **Precisión antes que elegancia.** Si el documento dice "marzo de 2024" y no un día exacto, el hecho dice "marzo de 2024".

**De la cita:**

- **Literal y entre comillas**, cortada donde deja de decir lo que se afirma.
- **Con coordenada exacta**: página para documentos, minuto y segundo para grabaciones, cláusula o apartado si el documento los numera. "En el contrato" no es una coordenada.
- **Nunca una cita reconstruida de memoria.** Si no se puede copiar el texto, no hay cita: hay una referencia sin cita, y así se escribe.

**De la relación entre la prueba y el hecho** — tres preguntas, en este orden, y la primera que dé "sí" fija la relación:

| Pregunta | Relación |
|---|---|
| ¿Este material **afirma el enunciado**? | **RESPALDA** |
| ¿Lo **niega**, o lo hace imposible tal como está redactado? | **CONTRADICE** |
| ¿Ni una cosa ni la otra, pero sin él el hecho se entiende mal? | **DA CONTEXTO** |
| ¿No hay ningún material detrás, solo el relato de alguien? | No hay prueba: el hecho va marcado **solo alegado** |

No hay una quinta relación. Si aparece un caso real donde estas tres no alcanzan, **se señala** en el propio documento y se deja constancia; no se inventa una categoría nueva.

**La regla que sostiene la distinción alegado / acreditado — no exceder la fuente:**

> Un material **respalda** un enunciado solo si el material **afirma ese enunciado**, no si afirma que alguien lo dijo.

De ahí salen dos caminos honestos, y uno prohibido:

- **Camino A (por defecto).** El hecho se redacta sobre el mundo ("la máquina se entregó el 2 de abril") y, si lo único que hay es el relato de la persona interesada, el hecho va **solo alegado**, con nota que dice quién lo afirma y en qué minuto de la entrevista.
- **Camino B.** El hecho se redacta sobre la declaración ("en la entrevista del 3 de mayo, la señora Ríos afirmó que la máquina se entregó el 2 de abril"), y entonces la entrevista sí lo respalda: el enunciado es sobre lo dicho. Se usa cuando lo que importa es que **se dijo** —un aviso que se dio, una promesa que se hizo—.
- **Prohibido:** redactarlo sobre el mundo y contarlo como respaldado porque la entrevista lo menciona. Eso es exactamente el error más grave del dominio.

**La entrevista es la fuente de las afirmaciones, no la prueba de ellas.** Esto no degrada la entrevista: es de donde sale casi todo. Solo fija qué establece.

**Regla de presentación que acompaña a la anterior:** la línea de respaldo **nunca dice "respaldado" a secas**. Siempre desglosa **quién produjo cada material**: no es lo mismo "1 a favor: documento firmado por ambas partes" que "1 a favor: lo dice la propia interesada". Un número sin ese desglose se lee como "probado", y no lo es.

### 1.4 Los estados de respaldo, y por qué "parcialmente respaldado" no es uno

El estado no se decide: **se lee de las pruebas de la ficha**, y siempre desglosado:

| Estado | Cuándo |
|---|---|
| **Respaldado** | Hay al menos una prueba que RESPALDA |
| **Contradicho** | Hay al menos una prueba que CONTRADICE |
| **Respaldado y contradicho** | Hay de las dos. **No es un error ni algo que resolver aquí**: es información, y la decisión es de ella |
| **Sin respaldo** | No hay ninguna prueba que respalde ni que contradiga |

**Atención — el contexto no respalda.** Un hecho cuyas únicas pruebas DAN CONTEXTO está **sin respaldo**, y así se escribe. Presentar contexto como apoyo es una forma elegante de mentir.

**"Parcialmente respaldado" no aparece en esa tabla a propósito.** El caso es real y frecuente —el recibo confirma el pago pero no la fecha afirmada—, pero no es un estado: es **la señal de que el hecho está redactado con el grano equivocado**. Un enunciado que la prueba cubre a medias son, casi siempre, dos enunciados pegados.

**Qué se hace entonces (y es obligatorio hacerlo, no redondear):**

1. **Se estrecha el hecho** hasta exactamente lo que la prueba cubre, y ese queda respaldado.
2. **El resto sale como hecho aparte**, marcado según lo que tenga: normalmente *solo alegado*.
3. Ambos llevan una línea **"Alcance de la cita"** que dice, con todas las letras, **qué no cubre** el documento citado.
4. Las dos fichas quedan emparejadas por una línea "Va con:", para que ella los lea juntos y pueda aceptar uno y rechazar el otro.

Si estrechar el hecho lo vuelve inútil para el caso, **no se estrecha**: se deja el enunciado completo, se marca *solo alegado* y la línea "Alcance de la cita" explica qué parte sí aparece en el documento. Lo que nunca se hace es dejarlo como "respaldado" y confiar en que ella note el matiz.

### 1.5 Las etiquetas de los hechos son etiquetas, no un orden

- Cada hecho lleva una etiqueta corta (`H-01`, `H-02`…) que sirve **solo para nombrarlo**: "el H-04 no me sirve".
- **La etiqueta no es un puesto en la lista.** Reordenar las fichas no renumera nada. Si un hecho se retira, su etiqueta se retira con él y **no se reutiliza jamás** para otro hecho.
- **Si el enunciado cambia, la ficha cambia y su etiqueta se retira**: el hecho nuevo entra con etiqueta nueva y una línea "Sustituye a: H-04". Motivo, en su idioma: *una aprobación vale para el texto exacto que usted leyó; si el texto cambia, la aprobación caduca.*

### 1.6 Segunda pasada sobre el mismo caso

No se reescribe el documento anterior: **se produce uno nuevo**, con su propio encabezado y su propia fecha, y con dos líneas más:

- **"Qué material es nuevo respecto de la pasada del \<fecha\>"**.
- **"Qué hechos de la pasada anterior podrían haber quedado afectados por ese material nuevo"** — nombrando etiquetas, sin rehacerlos por cuenta propia.

El skill **no** decide que un hecho anterior quedó superado. Señala el impacto y devuelve la decisión.

### 1.7 Plantilla completa

Se copia tal cual. Los textos entre « » se reemplazan; las líneas fijas no se tocan.

```text
════════════════════════════════════════════════════════════════════
HECHOS PROPUESTOS — «nombre corto del caso»
Pasada del «fecha». Preparado para su revisión.

  ESTO ES UNA PROPUESTA. Nada de lo que sigue es un hecho del caso
  hasta que usted lo decida hecho por hecho. Las citas hay que
  comprobarlas contra el documento: este texto no lo hace por usted.
════════════════════════════════════════════════════════════════════

1. DE DÓNDE SALE ESTO

Material que se leyó:
  · «documento o grabación» — «qué es» — «fecha» — «páginas o duración»
  · …
Material que se recibió y NO se pudo leer, o se leyó a medias:
  · «cuál y por qué» (si no hay ninguno, escribir: ninguno)
Material que se menciona en la entrevista y no está entre lo recibido:
  · «cuál y quién lo menciona»
Cómo se hizo: método fact-builder, «versión». Cuánto material quedó fuera
por decisión propia: «nada / esto y por qué».

2. HOJA DE DECISIONES

| Hecho | Enunciado (una línea)      | Respaldo                    | Sí | No | A medias |
|-------|----------------------------|-----------------------------|----|----|----------|
| H-01  | «…»                        | «…»                         | [] | [] | []       |
| H-02  | «…»                        | «…»                         | [] | [] | []       |

«A medias» = el hecho sirve pero hay que corregirlo. Escriba la corrección
al lado de la ficha.

3. LAS FICHAS

────────────────────────────────────────────────────────────────────
H-01 · «enunciado completo del hecho, una sola proposición»

  Respaldo: «desglose por origen del material, nunca un número solo»
  De dónde salió el enunciado: «quién lo dice y dónde, con coordenada»
  Va con: «H-0X» (solo si hay ficha emparejada)

  Pruebas:
   1) RESPALDA — «documento», «página/minuto exacto»
      Cita: «texto literal entre comillas»
      Qué establece exactamente: «una línea; ni una palabra más de lo
      que la cita dice»
      Quién produjo ese material: «una parte / ambas partes / un tercero
      / la propia interesada»
   2) CONTRADICE — …
   3) DA CONTEXTO — …
      (si no hay ninguna prueba, escribir: SOLO ALEGADO — «quién lo
      afirma, dónde y por qué no hay material detrás»)

  Alcance de la cita: «qué NO cubre el documento citado» (obligatorio
  cuando la prueba cubre el hecho a medias)
  Qué haría falta para respaldarlo: «documento concreto que lo cerraría»

  Su decisión:  [ ] sí   [ ] no   [ ] a medias — corregir: ______________
────────────────────────────────────────────────────────────────────

4. LO QUE NO SE CONVIRTIÓ EN HECHO

| Lo que se dijo o se leyó | Por qué no es un hecho |
|--------------------------|------------------------|
| «cita o resumen breve»   | «relato / valoración / calificación / no comprobable / no aporta al caso» |

Si alguno de estos le importa, dígalo: puede reformularse como hecho.

5. LO QUE SE BUSCÓ Y NO SE ENCONTRÓ

  · «qué se buscó» — se buscó en: «dónde exactamente» — no aparece.

  Que no aparezca aquí NO significa que no exista: significa que no está
  en el material que se revisó, o que no se supo encontrarlo.
```

---

## 2. Ejemplo relleno

**Material sintético, inventado para este ejemplo.** Nombres, cifras y documentos son ficticios; no describe ningún caso real y no afirma nada de derecho.

```text
════════════════════════════════════════════════════════════════════
HECHOS PROPUESTOS — Ríos / Distribuidora Andes
Pasada del 25 de agosto de 2026. Preparado para su revisión.

  ESTO ES UNA PROPUESTA. Nada de lo que sigue es un hecho del caso
  hasta que usted lo decida hecho por hecho. Las citas hay que
  comprobarlas contra el documento: este texto no lo hace por usted.
════════════════════════════════════════════════════════════════════

1. DE DÓNDE SALE ESTO

Material que se leyó:
  · Entrevista grabada con la señora Ríos — 3 de mayo de 2024 — 47 min
  · Contrato de compraventa firmado — 2 de febrero de 2024 — 6 páginas
  · Comprobante de transferencia bancaria — 1 página
  · Correo de Distribuidora Andes — 10 de abril de 2024 — 1 página
  · Acta de entrega firmada por ambas partes — 9 de abril de 2024 — 1 pág.
  · Recibo de Andes por instalación — 1 página
Material que se recibió y NO se pudo leer, o se leyó a medias:
  · Recibo de instalación: la fecha está sobre el sello y no se lee.
    El importe y el concepto sí se leen.
Material que se menciona en la entrevista y no está entre lo recibido:
  · Un correo en el que Andes aceptaría cubrir la instalación
    (lo menciona la señora Ríos, minuto 00:31:04)
Cómo se hizo: método fact-builder, versión 0. Cuánto material quedó fuera
por decisión propia: nada; los descartes están en el apartado 4.

2. HOJA DE DECISIONES

| Hecho | Enunciado (una línea)                                  | Respaldo                                                        | Sí | No | A medias |
|-------|--------------------------------------------------------|-----------------------------------------------------------------|----|----|----------|
| H-01  | El 14 de marzo salieron $12.000.000 hacia Andes        | 2 a favor: comprobante del banco + correo de la otra parte      | [] | [] | []       |
| H-02  | La máquina se entregó el 2 de abril                    | 1 en contra: acta firmada por ambas · 1 de contexto             | [] | [] | []       |
| H-03  | Andes aceptó por escrito cubrir la instalación         | Sin respaldo: solo alegado por la interesada                    | [] | [] | []       |
| H-04  | Se pagaron $800.000 por concepto de instalación        | 1 a favor: recibo de Andes (no cubre la fecha)                  | [] | [] | []       |
| H-05  | Ese pago se hizo el 3 de marzo de 2024                 | Sin respaldo: solo alegado (va con H-04)                        | [] | [] | []       |

«A medias» = el hecho sirve pero hay que corregirlo. Escriba la corrección
al lado de la ficha.

3. LAS FICHAS

────────────────────────────────────────────────────────────────────
H-01 · El 14 de marzo de 2024 salieron $12.000.000 de la cuenta de la
señora Ríos hacia una cuenta a nombre de Distribuidora Andes.

  Respaldo: 2 a favor — un comprobante del banco y un correo escrito por
  la otra parte. Ninguno es la propia interesada.
  De dónde salió el enunciado: entrevista, 00:08:12.

  Pruebas:
   1) RESPALDA — Comprobante de transferencia bancaria, página 1
      Cita: «14/03/2024 — Transferencia enviada $12.000.000 — Destino:
      DISTRIBUIDORA ANDES S.A.S.»
      Qué establece exactamente: que ese día salió esa suma hacia una
      cuenta con ese nombre. No dice por qué concepto.
      Quién produjo ese material: un tercero (el banco).
   2) RESPALDA — Correo de Distribuidora Andes, 10 de abril de 2024
      Cita: «confirmamos que recibimos su pago del 14 de marzo»
      Qué establece exactamente: que la otra parte reconoce por escrito
      haber recibido un pago con esa fecha.
      Quién produjo ese material: la otra parte.

  Alcance de la cita: ninguno de los dos documentos dice a qué concepto
  se imputó ese pago.
  Qué haría falta para respaldarlo: nada; para el concepto, una factura.

  Su decisión:  [ ] sí   [ ] no   [ ] a medias — corregir: ______________
────────────────────────────────────────────────────────────────────
H-02 · La máquina empacadora se entregó el 2 de abril de 2024.

  Respaldo: 1 en contra — acta firmada por ambas partes. Nada a favor:
  la fecha del 2 de abril solo aparece en el relato de la interesada.
  De dónde salió el enunciado: entrevista, 00:12:31 («llegó el 2 de
  abril, me acuerdo porque era martes»).

  Pruebas:
   1) CONTRADICE — Acta de entrega, página 1
      Cita: «Recibido a satisfacción el 9 de abril de 2024», con dos
      firmas.
      Qué establece exactamente: que hay un documento firmado por ambas
      partes que sitúa la entrega el 9 de abril.
      Quién produjo ese material: ambas partes.
   2) DA CONTEXTO — Correo de Distribuidora Andes, 10 de abril de 2024
      Cita: «la máquina quedó instalada ayer»
      Qué establece exactamente: que el 10 de abril la otra parte
      escribía que la instalación era del día anterior. Habla de la
      instalación, no de la entrega: por eso no se cuenta como prueba en
      contra.
      Quién produjo ese material: la otra parte.

  Alcance de la cita: el acta dice cuándo se firmó la recepción, no
  cuándo llegó físicamente la máquina. Las dos cosas pueden no coincidir.
  Qué haría falta para respaldarlo: una guía de transporte, un registro
  de portería, o un mensaje de esos días.

  No se corrigió la fecha por cuenta propia. La discrepancia entre lo
  que ella recuerda y lo que firmó es justamente lo que usted tiene que
  ver.

  Su decisión:  [ ] sí   [ ] no   [ ] a medias — corregir: ______________
────────────────────────────────────────────────────────────────────
H-03 · Distribuidora Andes aceptó por escrito cubrir el costo de la
instalación.

  Respaldo: sin respaldo.
  De dónde salió el enunciado: entrevista, 00:31:04.

  Pruebas:
   SOLO ALEGADO — Lo afirma la señora Ríos en la entrevista (00:31:04):
   «ellos me lo pusieron en un correo, que la instalación iba por su
   cuenta». Ese correo no está entre el material recibido, y ningún
   documento entregado dice eso. La entrevista establece que ella lo
   afirma; no establece que ocurriera.

  Alcance de la cita: —
  Qué haría falta para respaldarlo: el correo que ella menciona, o
  cualquier mensaje de Andes que hable del costo de instalación.

  Su decisión:  [ ] sí   [ ] no   [ ] a medias — corregir: ______________
────────────────────────────────────────────────────────────────────
H-04 · La señora Ríos pagó $800.000 por concepto de instalación.

  Respaldo: 1 a favor — recibo emitido por la otra parte. No cubre la
  fecha.
  De dónde salió el enunciado: entrevista, 00:33:40.
  Va con: H-05.

  Pruebas:
   1) RESPALDA — Recibo de Andes, página 1
      Cita: «Recibimos de Amparo Ríos la suma de $800.000 por concepto
      de instalación»
      Qué establece exactamente: que Andes reconoce haber recibido esa
      suma por ese concepto.
      Quién produjo ese material: la otra parte.

  Alcance de la cita: el recibo NO dice cuándo. La fecha está impresa
  sobre el sello y no se lee. Por eso la fecha salió a ficha aparte
  (H-05) en vez de darla por respaldada.
  Qué haría falta para respaldarlo: nada más para el pago; para la
  fecha, ver H-05.

  Su decisión:  [ ] sí   [ ] no   [ ] a medias — corregir: ______________
────────────────────────────────────────────────────────────────────
H-05 · Ese pago de $800.000 se hizo el 3 de marzo de 2024.

  Respaldo: sin respaldo.
  De dónde salió el enunciado: entrevista, 00:33:40.
  Va con: H-04.

  Pruebas:
   SOLO ALEGADO — La fecha la afirma la señora Ríos en la entrevista
   (00:33:40). El único documento que habla de ese pago —el recibo de
   H-04— tiene la fecha ilegible.

  Alcance de la cita: —
  Qué haría falta para respaldarlo: el extracto bancario de marzo de
  2024, o un recibo legible.

  Su decisión:  [ ] sí   [ ] no   [ ] a medias — corregir: ______________
────────────────────────────────────────────────────────────────────

4. LO QUE NO SE CONVIRTIÓ EN HECHO

| Lo que se dijo o se leyó                                      | Por qué no es un hecho                                                      |
|---------------------------------------------------------------|------------------------------------------------------------------------------|
| «Me sentí engañada desde el principio» (entrevista, 00:04:50)  | Relato de cómo vivió lo ocurrido. No es comprobable como suceso.              |
| «Esa gente se portó fatal» (entrevista, 00:29:15)              | Valoración. Si detrás hay conductas concretas, cada una sería un hecho aparte.|
| «Incumplieron el contrato» (entrevista, 00:30:02)              | Calificación, no hecho. Este método no califica.                              |
| La máquina es de color azul (contrato, página 2)               | Aparece en el material, pero no se ve a qué asunto del caso sirve.            |

Si alguno de estos le importa, dígalo: puede reformularse como hecho.

5. LO QUE SE BUSCÓ Y NO SE ENCONTRÓ

  · El correo donde Andes aceptaría cubrir la instalación (H-03) — se
    buscó en: los cinco documentos recibidos y la transcripción completa
    — no aparece.
  · Cualquier documento con la fecha real del pago de instalación (H-05)
    — se buscó en: comprobante bancario, recibo y correo — no aparece.

  Que no aparezca aquí NO significa que no exista: significa que no está
  en el material que se revisó, o que no se supo encontrarlo.
```

**Qué demuestra este ejemplo, para quien lo use como patrón:**

- **H-01** — un hecho con **dos** pruebas de fuentes distintas.
- **H-02** — un hecho **contradicho**, con el relato de la interesada como origen y no como apoyo, y con una prueba que **da contexto sin contar como apoyo**. Muestra además que el skill **no resuelve** la discrepancia.
- **Correo del 10 de abril** — la misma prueba sirve a **dos** hechos (respalda H-01, da contexto a H-02): la relación es de muchos a muchos y no se fuerza a uno a uno.
- **H-03** — un hecho **sin soporte**, y el hueco convertido en información útil (qué documento haría falta).
- **H-04 + H-05** — el caso **parcialmente respaldado**, desdoblado en lo que la prueba cubre y lo que no, en vez de redondearlo.

---

## 3. Modo 2 — con Core

### 3.1 A quién habla esta sección, y con qué estatus

**No es un texto para la profesional.** Es el contrato de canalización para quien construya el Core.

**HECHO VERIFICADO:** hoy no existe Core. Nada de esta sección es ejecutable; el modo 1 es el único modo real esta semana.

**Estatus de los contratos que se citan:** `propose_facts` está especificado en `docs/technical-design/v0/05-mcp-contract.md` §6.8 (nivel 2, con partes marcadas como propuesta) y el modelo de `Proposal`/`ProposalItem` en `ADR-008` (**Proposed**). Si esos contratos cambian, **cambia la tabla de mapeo de §3.3 y nada más**: el método y el modo 1 no dependen de ellos.

### 3.2 Qué pasa con la salida

La misma pasada que en el modo 1 produce un documento, en el modo 2 se canaliza por **`propose_facts`**, que registra una **`Proposal`** con un **`ProposalItem` por hecho**. Cada item recibe:

- **`proposal_item_id`** — identidad **estable y opaca emitida por el Core**, nunca un índice posicional. Reordenar la propuesta no cambia ningún identificador (ADR-008, invariante 1). Es el equivalente formal de la regla de §1.5: la etiqueta nombra al hecho, no a su puesto en la lista.
- **`item_content_hash`** — huella del contenido exacto del item. Es lo que hace ejecutable la frase que en el modo 1 es solo una promesa de método: *la aprobación vale para el texto exacto que se aprobó*. Si el contenido cambia, la aprobación queda invalidada por comparación, sin que nadie tenga que acordarse.
- **`review_decision`** (`PENDING` al nacer) y **`commit_state`** (`UNCOMMITTED`), dos dimensiones separadas.

Cada item lleva, **obligatoriamente y sin tercera vía**, una de estas dos cosas (ADR-006, invariante 2):

- **`evidence_basis[]`** — una o más referencias, cada una con `fragment_ref` (handle emitido por el Core, que resuelve al fragmento incorporado), `polarity` del enum cerrado `SUPPORTS | CONTRADICTS | CONTEXTUALIZES`, y `justification`.
- **`alleged_only.basis_note`** — la marca explícita "solo alegado" y por qué.

Un item sin ninguna de las dos, o con las dos, **es rechazado por forma**. El modo 1 pide exactamente lo mismo; la diferencia es que allí nadie lo comprueba.

**Techo epistémico, idéntico en los dos modos:** lo que sale de aquí nace `PROPOSED` y **jamás pasa de `PROPOSED` por acción del modelo**. `ALLEGED` exige el commit con autorización humana registrada del lado del Core (ADR-003, ADR-005, ADR-008).

### 3.3 Mapeo campo a campo

| Modo 1 — línea del documento | Modo 2 — dónde va | Nota |
|---|---|---|
| Nombre del caso en el encabezado | `case_id` | En el modo 1 es un rótulo; en el modo 2, identidad emitida por el Core |
| "Cómo se hizo: método fact-builder, versión X" | `methodology { skill, methodology_version }` | El versionado del skill lo gestiona el producto, no la plataforma (`vertical-slice-v0.md` §9) |
| — (no visible en el documento) | `model_id` | Metadato de la pasada |
| — | `expected_revision` (opcional) | Sin Core no hay revisión del expediente que verificar |
| Etiqueta `H-01` | **No viaja.** El Core emite `proposal_item_id` | La etiqueta del papel es una comodidad de lectura, no identidad |
| Enunciado del hecho | `fact_text` | Mismo texto, misma regla de una sola proposición |
| Cada bloque "Pruebas: n)" | un elemento de `evidence_basis[]` | Varios bloques = varios elementos: la relación es N:M en los dos modos |
| "RESPALDA / CONTRADICE / DA CONTEXTO" | `polarity: SUPPORTS / CONTRADICTS / CONTEXTUALIZES` | Enum cerrado; una cuarta palabra es un rechazo por forma |
| "«documento», página/minuto exacto" | `fragment_ref` | En el modo 1 es texto tecleado por el modelo; en el modo 2 es un handle que resuelve contra el original |
| Cita literal | **No viaja como texto**: se resuelve desde el `fragment_ref` | Cambio de garantía importante, ver §4 |
| "Qué establece exactamente" | `justification` | |
| "Quién produjo ese material" | Dentro de `justification` | **No tiene campo propio.** Ver §3.4 |
| "SOLO ALEGADO — quién lo afirma y por qué no hay material" | `alleged_only.basis_note` | Texto libre |
| Línea "Respaldo: n a favor / n en contra" | **No viaja.** El Core lo **computa** desde los links activos | `SUPPORTED / CONTRADICTED / UNSUPPORTED` se computan, nunca se almacenan (ADR-003). Los `CONTEXTUALIZES` no cuentan: coincide con la regla de §1.4 |
| "Va con: H-0X" (par de un hecho desdoblado) | **No tiene campo.** Se refleja redactando cada item completo | Ver §3.4 |
| "Alcance de la cita" | Dentro de `justification` | |
| Casilla `[ ] sí / [ ] no / [ ] a medias` | `review_decision` = `APPROVED / REJECTED / PENDING` | **No pasa por `propose_facts`**: se decide en el canal de revisión humana, fuera del alcance del modelo. "A medias" es `PENDING` con corrección pedida |
| Apartado 4 (lo descartado) y apartado 5 (lo no encontrado) | **No tienen campo.** Ver §3.4 | |

### 3.4 Lo que existe en el modo 1 y no tiene sitio en el modo 2

Se señala, no se resuelve aquí (y no se propone cambiar ningún contrato):

1. **Lo descartado y las búsquedas fallidas** (apartados 4 y 5) no son hechos propuestos y no tienen campo en `propose_facts`. Hoy solo pueden viajar como conversación, es decir, **se pierden al cerrar la sesión**. Es el material que el modo 1 conserva mejor que el modo 2.
2. **"Quién produjo el material"** no tiene campo propio; viaja dentro de la justificación, donde nadie lo puede leer de forma uniforme. Es la línea que impide leer "respaldado" como "acreditado", y es la que peor sobrevive al viaje.
3. **El emparejamiento de un hecho desdoblado** ("va con H-05") no tiene campo. Cada item debe quedar comprensible por separado.
4. **El ancla del "solo alegado"**: cuando un hecho va como `alleged_only`, el minuto exacto de la entrevista donde se afirma queda como texto libre en la nota, no como referencia resoluble. La coordenada existe, pero no se puede seguir automáticamente.

Los cuatro son observaciones para quien construya, con el mismo criterio del proyecto: **si el caso aparece de verdad, se señala; no se inventan categorías preventivas.**

### 3.5 Qué rechaza el Core por sí solo

Un hecho sin base ni marca (`PROVENANCE_REQUIRED`); una referencia a material no incorporado (`NOT_INCORPORATED`); un handle inventado (`UNKNOWN_REFERENCE`); una referencia a otro caso (`CROSS_CASE_REFERENCE`); una polaridad fuera del enum o las dos bases a la vez (`VALIDATION_FAILED`). En el modo 1, **cada uno de esos cinco rechazos es una lectura atenta de la profesional o no es nada.**

---

## 4. Qué garantiza cada modo

Cuatro columnas a propósito: la tercera es la que impide leer la segunda como un fracaso. El modo 1 no tiene garantías, pero **no es lo mismo que no tener nada**: tiene método, y el método es exactamente lo que el baseline va a medir.

| # | Lo que se quiere | Modo 1 (sin Core) | Qué lo sostiene en el modo 1 | Modo 2 (con Core) |
|---|---|---|---|---|
| 1 | Que la salida tenga la forma acordada | **Ninguna garantía** | Que el modelo siga el texto del skill | El esquema de la tool rechaza lo que no encaja |
| 2 | Que cada hecho traiga prueba o la marca "solo alegado" | **Ninguna garantía** | Regla de método, verificable de un vistazo por la posición fija de la línea | Rechazo por forma (`PROVENANCE_REQUIRED`) |
| 3 | Que la cita exista y esté donde se dice | **Ninguna garantía** | La coordenada exacta al lado de la cita: comprobar cuesta una mirada | El `fragment_ref` resuelve contra el original conservado; no hay cita "tecleada" |
| 4 | **Que la cita diga lo que la ficha afirma que dice** | **Ninguna garantía** | La línea "qué establece exactamente", que obliga a escribir el salto | **Ninguna tampoco.** El Core valida que el fragmento exista y sea de este caso, **no** que sostenga el hecho |
| 5 | Que la prueba citada sea de este caso y esté incorporada | **Ninguna garantía** | Nada: en el modo 1 no existe "incorporado" | `NOT_INCORPORATED`, `CROSS_CASE_REFERENCE`, `UNKNOWN_REFERENCE` |
| 6 | Que la relación sea una de las tres | **Ninguna garantía** | Las tres preguntas en orden (§1.3) | Enum cerrado; cualquier otra cosa es rechazo por forma |
| 7 | Que el estado de respaldo sea coherente con las pruebas listadas | **Ninguna garantía** | Regla de §1.4 y desglose obligatorio por origen del material | El estado se **computa** desde los links; no se envía ni se almacena |
| 8 | Que nada pase a ser hecho del caso sin decisión de ella | **Ninguna garantía técnica; garantía de hecho, por ausencia** | No hay expediente que contaminar. **El riesgo se mueve**: que el texto se copie tal cual dentro de un escrito | Techo `PROPOSED`; `ALLEGED` exige autorización humana registrada del lado del Core |
| 9 | Que la aprobación valga solo para el texto exacto aprobado | **Ninguna garantía** | Regla de las etiquetas: si cambia el enunciado, etiqueta nueva y "sustituye a" | `item_content_hash`: la aprobación se invalida por comparación |
| 10 | Que una aprobación no se reutilice ni caduque sin avisar | **Ninguna garantía** | Nada | Autorización de un solo uso, con expiración y atada a la revisión vigente |
| 11 | Que se pueda aprobar hecho por hecho | **Ninguna garantía** | La casilla por ficha; es papel, y el papel obedece | Aprobación parcial por item, con invalidación quirúrgica (ADR-008) |
| 12 | Que quede rastro de quién decidió qué y cuándo | **Ninguna garantía** | El documento firmado o guardado, si alguien lo guarda | Registro de revisión append-only y bitácora de eventos del caso |
| 13 | Que no falte ningún hecho importante | **Ninguna, y tampoco en el modo 2** | Método: la hoja previa de la profesional y el apartado de descartes | **Ninguna.** Ningún mecanismo del Core sabe qué falta |
| 14 | Que el hecho esté bien redactado y sirva al caso | **Ninguna, y tampoco en el modo 2** | Método: reglas de redacción de §1.3 | **Ninguna.** Es juicio profesional, y así debe seguir |

**Las tres lecturas que hay que sacar de esta tabla:**

1. **Las filas 1, 2, 3, 5, 6, 9, 10, 11 y 12 son exactamente lo que el Core añade.** Son la medida de cuánto vale construirlo.
2. **Las filas 4, 13 y 14 no las cubre nadie, en ningún modo.** Ninguna cantidad de infraestructura sustituye la lectura de la profesional. Prometer lo contrario sería el fallo más caro que este proyecto podría cometer.
3. **La columna tercera es el objeto del baseline.** Es lo único que existe esta semana.

### 4.1 Cómo se usa esta tabla después del baseline

Cada fila con "ninguna garantía" en el modo 1 es una **hipótesis comprobable**: *el método solo, sin nada que lo obligue, sostiene esta propiedad tantas veces de tantas*. La medición se hace con **conteos con denominador**, nunca con porcentajes ni tasas (regla de `docs/discovery/baseline-analisis-y-rubrica.md` §6): "3 de 24 citas comprobadas no estaban donde decía".

Lo que se compara después es la misma fila con el Core delante. Y la fila 4 es la que hay que mirar con más cuidado, porque es donde el Core **parece** ayudar y no ayuda: una cita que resuelve perfectamente al fragmento correcto puede seguir sin sostener el hecho que dice sostener.
