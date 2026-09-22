---
name: nombrar-voces
description: "Método para ponerle nombre y cargo a las voces de una transcripción ya hecha, con una regla que no se rompe: quien nombra es la profesional, nunca la máquina. Mide primero si la separación de voces de esa grabación aguanta; si no aguanta, lo dice y se niega a etiquetar. Prepara una ficha con cuánto habla cada voz, tres muestras enlazadas al minuto para reconocerla y las presentaciones que haya en el audio, sin darlas por buenas. Recoge lo que ella declare —quién es, qué cargo, cómo lo sabe— y regenera la transcripción con las etiquetas y su procedencia. Úsalo después de transcribir-audio, cuando haga falta saber quién dijo qué. No interpreta, no deduce nombres y NO redacta actas."
version: 0.1.0
allowed-tools: Bash(python ${CLAUDE_PLUGIN_ROOT}/scripts/nombrar_voces.py *), Bash(python ${CLAUDE_PLUGIN_ROOT}/scripts/estado_transcripcion.py *)
---

# nombrar-voces — qué voz es quién, según ella

## 1. Cuándo usar este método y cuándo no

**Propósito.** Una transcripción sale con voces numeradas —«Hablante 1», «Hablante 2»— que **no son personas: son grupos de sonido**. Este método convierte ese número en un nombre **cuando, y solo cuando, una persona que estuvo allí lo afirma**, y deja escrito quién lo afirmó y cuándo.

**Úsalo cuando** ya existe una transcripción de `transcribir-audio` y hace falta saber quién dijo qué: para citar en un escrito, para preparar una actuación, para entender una discusión con varios intervinientes.

**No lo uses para**: averiguar quién es alguien —eso no se puede hacer desde el texto—; redactar un acta o un resumen —**eso es otra cosa y no entra aquí**—; ni para «mejorar» una transcripción cuyo problema es otro.

**Si no hay transcripción todavía**, primero `transcribir-audio`. Este método no toca el audio.

---

## 2. El principio rector

> **La máquina agrupa sonido. La persona nombra. Y las dos cosas se ven por separado, siempre.**

De ahí salen tres consecuencias que no se negocian:

1. **Ningún nombre entra sin que alguien lo afirme.** Ni aunque en el audio alguien se presente: lo que se oye es «soy» seguido de un nombre propio, y los nombres propios son **lo que peor transcribe la máquina**. Una presentación se le **enseña** a ella como candidata; no se aplica sola.
2. **La etiqueta viaja con su procedencia.** «Lo afirma <quién>, el <fecha>. No lo comprobó ningún programa.» Sin eso, un nombre en una transcripción parece un dato del expediente, y no lo es.
3. **Una voz mal separada no se etiqueta.** Ponerle nombre a un grupo que contiene a dos personas es atribuirle a alguien las frases de otro — y eso, en un escrito, es peor que no tener nombre.

---

## 3. El procedimiento

### Fase 1 — Mirar en qué estado está esa transcripción

Antes de preguntar nada, **la puerta**: qué hay, quién habla, y qué comprobó ella oyendo.

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/estado_transcripcion.py \
  "Transcripcion - Audio 2.md" "datos/A2 - datos completos.json" \
  --comprobado "comprobado - Audio 2.json"
```

El informe termina diciendo **qué preguntarle antes de producir**. Si de ahí sale que hay que
nombrar voces, se sigue con la ficha:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/nombrar_voces.py ficha "<datos completos>.json" \
  --titulo "Audio 2" --pagina "Transcripciones/Audio 2 - oir y marcar.html" \
  --salida "Quien es cada voz - Audio 2.md"
```

El programa devuelve un **veredicto** y los números en que se apoya: cuántas voces pasan de quince segundos, qué parte del habla se lleva la que más habla, cuántas líneas quedaron sin voz.

| Veredicto | Qué hacer |
|---|---|
| **Sirve como punto de partida** | Seguir a la fase 2 |
| **DUDOSA** | Seguir, **diciéndoselo**: puede ser una persona que expone mucho, o dos fundidas. Las muestras lo aclaran |
| **NO SIRVE para distinguir quién habla** | **Parar.** Ir a la sección 7 |

**Los umbrales de ese veredicto son una elección declarada, no una medida.** Dilo así cuando lo presentes.

### Fase 2 — Preguntar, con lo necesario para contestar

Entrégale la ficha y **pregúntale voz por voz**. La ficha ya trae, para cada una: cuánto habla, tres muestras enlazadas al minuto —la intervención más larga, la primera aparición y otra— y las presentaciones candidatas si las hay.

**La pregunta es siempre la misma, y tiene tres partes:**

> **¿Quién es?** · **¿Qué cargo o entidad?** · **¿Cómo lo sabe?**

La tercera no es burocracia: es lo que separa «la reconozco, estuve en la reunión» de «me lo dijo alguien». Las dos valen; no valen lo mismo, y el entregable lo dice.

### Fase 3 — Escribir lo que declaró

Se guarda en un archivo `declaracion de voces - <grabación>.json`:

```json
{
  "formato": "despacho/voces-declaradas",
  "version": 1,
  "declarado_por": "<nombre de quien lo afirma>",
  "fecha": "<AAAA-MM-DD>",
  "voces": {
    "1": {"quien": "...", "cargo": "...", "como_lo_se": "La reconozco: estuve en la reunión"},
    "2": {"no_se": true},
    "3": {"mismo_que": "1"},
    "4": {"varias_personas": true}
  }
}
```

**`declarado_por` y `fecha` son obligatorios.** El programa se niega sin ellos: una etiqueta que no es de nadie no sirve para nada.

### Fase 4 — Aplicar, sin tocar el texto

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/nombrar_voces.py aplicar \
  "Transcripcion - Audio 2.md" "datos/A2 - datos completos.json" "declaracion de voces - A2.json" \
  --md-salida "Transcripcion - Audio 2 - con nombres.md" \
  --datos-salida "datos/A2 - con nombres.json"
```

Produce **archivos nuevos**: la transcripción anterior se queda donde estaba (`ADR-011` §8). El programa comprueba que **no cambió ni una palabra del texto transcrito** y se detiene si cambió.

Este método **no regenera la entrega**. La página y el Word se rehacen con los mismos
programas que los produjeron, y **ese paso se corre a mano**: exponerlos es una decisión
que nadie ha tomado todavía (ver `evals/scripts/test_superficie.py`). Lo que sí se dice al
entregar es **qué archivo nuevo hay que volver a convertir**.

---

## 4. Las tres respuestas incómodas, que son las que más valen

| Ella dice | Se escribe así |
|---|---|
| **«No sé quién es»** | La voz se queda con su número. **Es una respuesta completa**, no un hueco |
| **«Esta voz son dos personas»** | `"varias_personas": true`. Queda marcada, **y no se le pone nombre a ninguna** |
| **«Estas dos voces son la misma»** | `"mismo_que"`. Se unen bajo un nombre, y queda escrito que eran dos grupos |

Si ella duda, **la respuesta es «no sé»**. Nunca se empuja a decidir: el coste de un nombre equivocado lo paga un escrito, no esta conversación.

---

## 5. Qué entrega

1. **La ficha** «Quién es cada voz», con el veredicto de separación y las muestras. Es lo que se le enseña para preguntar.
2. **La transcripción con nombres**, archivo nuevo, con un bloque en la cabecera que dice **quién declaró las voces y cuándo**, y cada turno con su etiqueta.
3. **Los datos con etiquetas**, para que la página y el Word las muestren.
4. **Lo que quedó sin nombre**, dicho de frente: cuántas voces siguen siendo un número, y por qué.

---

## 6. Lo que este método NO hace

- **No redacta un acta.** Ni un resumen, ni un listado de acuerdos, ni un orden del día. Poner nombre a las voces y redactar un acta son **dos trabajos distintos**: el primero registra una afirmación de ella; el segundo interpreta la reunión. Mezclarlos convierte una etiqueta en una conclusión. Si hace falta un acta, es **otra skill**, con su propio alcance y sus propias reglas.
- **No deduce nombres.** Ni del texto, ni del audio, ni del contexto del caso, ni de una lista de asistentes. Solo enseña candidatos y espera.
- **No cambia una palabra de la transcripción.** Solo la cabecera del turno.
- **No decide que dos voces son la misma persona**, ni que una voz son dos. Eso lo dice ella.
- **No sobrescribe** la transcripción anterior.
- **No pone la marca ` - REVISADO`.** Esa la pone ella.
- **No mejora la separación de voces.** Si está mal, está mal: eso se arregla en `transcribir-audio`, no aquí.

---

## 7. Cuando el diagnóstico dice que la separación no sirve

Pasa, y hay que decirlo sin adornos: **en una grabación con varias personas, una sola voz puede llevarse casi todo el habla porque el programa las fundió.**

**Qué hacer:**

1. **Decírselo tal cual**: «en esta grabación el separador no distingue a las personas; los números de hablante no sirven para decir quién dijo qué».
2. **No etiquetar.** El programa se niega, y está bien que se niegue.
3. Si aun así ella quiere una etiqueta —porque reconoce la voz y asume el riesgo—, se añade `"acepta_advertencia": true`, y entonces **la advertencia viaja pegada a la etiqueta en todos los documentos**. No se puede quitar.
4. **Ofrecerle lo que sí funciona**: marcar los pasajes concretos que le importan oyéndolos, uno por uno, en la página de comprobación.

---

## 8. Lo que conviene pedirle para la próxima grabación

Esto no arregla lo ya grabado, pero cambia el resultado de la próxima vez, y **cuesta treinta segundos de reunión**:

> **Que cada persona diga su nombre y su cargo al empezar, una por una, sin hablar encima de otra.**

Con eso, la ficha de voces trae una presentación por voz, y ella confirma en vez de reconstruir. Si además se puede: **un micrófono más cerca de la mesa** y **que no se hable en paralelo** — el habla solapada es lo que más fusiona voces.

**Dilo una vez, como sugerencia, y no lo repitas en cada entrega.**

---

## 9. En qué posición está ella, y por qué cambia el trabajo

### En qué posición está ella, y por qué cambia la salida

**Dos posiciones, y no son la misma:**

| Posición | Qué significa | Cómo suena la salida |
|---|---|---|
| **Parte** | Representa a alguien y defiende su interés | «su clienta», «la parte que usted representa», «el escrito que usted presenta» |
| **Autoridad** | **Decide entre otros.** No defiende a nadie | «la querellante», «el querellado», «las partes», «la actuación», «lo que consta en el expediente». **Nunca «su clienta»: no la tiene** |

**Cómo se sabe.** Por lo que ella diga, o por lo que la carpeta muestre —un documento dirigido a su despacho, un radicado donde ella es la autoridad que recibe, una actuación que ella firma como quien resuelve—. **Si no se puede saber, se pregunta una vez** —*«¿usted representa a una de las partes, o le corresponde decidir este asunto?»*— **y se espera la respuesta antes de producir nada**. Ni se adivina, ni se pregunta y se sigue sobre una suposición: **lo segundo es adivinar con el trámite de la pregunta por delante**, y encima deja escrito que se consultó. Adivinar aquí no se nota en la salida —sale entera, bien escrita, en el registro que no era— **y lo cambia todo**: la posición gobierna a quién le hablas, si la simetría aplica, y si algo puede ordenarse por lo que le conviene a alguien.

**Y en posición de autoridad, tres cosas se endurecen:**

1. **Simetría obligatoria.** Toda carencia que **este método ya pueda señalar** —un documento que se anuncia y no está, una afirmación sin nada detrás, una firma sin el papel que la acompañe— **se busca en las demás partes antes de entregarla, y el resultado se escribe, lo encuentres o no**. Escribir *«se buscó lo mismo respecto de la otra parte: tampoco aparece»* es información; **no buscarlo es tomar partido con la selección**, que es la forma de tomar partido que no se ve. **Y también hacia dentro:** cuando quien decide es ella, **los defectos de lo que su propio despacho produjo se buscan igual que los de las partes**.

   > **Por qué se rompe, y casi nunca es por mala fe: se rompe por una razón material.** Una parte aportó diecinueve páginas y la otra cuatro, y **hay más superficie donde encontrar defectos**. Esa diferencia no es una diferencia de corrección, y si no se dice, **la salida miente por su forma**. Por eso **el conteo de la entrega reparte por lado** —cuántos de cada parte, y cuántos del propio despacho si lo hay—, y cuando el reparto queda desigual **se dice ahí mismo, con los números, y se dice si la causa es de volumen**. Un número que la regla exige y que el formato de salida no tiene dónde poner **es un número que no se escribe**.
   >
   > **Y esta regla no ensancha lo que puedes señalar: solo obliga a mirar a los dos lados de lo que ya señalabas.** Si este método no puede decir que a una parte le falta un requisito —porque decir qué se exige es derecho, y el derecho lo pone ella—, **la simetría no te autoriza a decirlo ahora**. Lo que hace es impedir que, de lo que sí puedes decir, salga solo la mitad.
   >
   > **Esta regla no es nueva y no es otra:** `revision-de-rigor` §2.3 la tiene desarrollada para su caso desde antes, y es **la misma**. Si alguna vez las dos redacciones dicen cosas distintas, manda la de `revision-de-rigor` y esta se corrige — **dos reglas para lo mismo es la avería que este arnés lleva documentada**.
2. **Nada se orienta a la ventaja de nadie.** Ni en lo que incluyes, ni en el orden, ni en los adjetivos. No existe «esto le sirve», «lo más favorable», ni un orden por utilidad: **quien decide no tiene un lado al que servirle.**
3. **Ninguna salida propone qué resolver.** Se entrega lo que el material dice; qué se decide con eso es de ella. Es la misma regla de siempre, y aquí es más estricta que en ningún otro sitio.
4. **Y mientras esto no esté decidido, el sistema no produce el contenido que decide.** Si una autoridad puede apoyar una decisión en lo que produce un sistema como este, **si debe declararlo**, y qué le pasa al acto si una cita sale mal, **no está resuelto en ninguna parte de este proyecto** — es el hueco `V-7`, y le falta una decisión con criterio jurídico, no una línea de método. **Hasta que exista, el valor por defecto es el estrecho.**

   > **Esta es la razón, y está escrita una sola vez.** Cada método dice qué significa en su caso —`/redactar-escrito` redacta los hechos y se detiene antes de la parte que decide; `/preguntas-de-derecho` no propone qué resolver— **y ninguno la reescribe**. Una razón con dos redacciones se parte, que es lo que le pasó a la simetría antes de que se le pusiera dueño.

> **Lo que NO cambia con la posición, y decirlo es parte de la regla:** las fuentes admitidas, «alegado no es acreditado», la fuente exacta de cada dato, no calcular, no afirmar derecho, y el vocabulario de la ausencia. **Esta variante endurece un solo eje —la orientación— y no afloja ninguno.** Si algo de aquí se leyera como permiso para relajar otra regla, se está leyendo mal.

> **Y los ejemplos de este método no son la voz de tu salida.** Están escritos desde el primer uso, que fue de parte, y por eso dicen «la clienta». **La salida usa el vocabulario de la posición de ella**, no el del ejemplo. (En los inventarios, «la propia interesada» y «la otra parte» son otra cosa: **categorías de quién produjo un documento**, y en posición de autoridad siguen significando lo mismo.)

---

## 10. Autoevaluación antes de entregar

1. ¿Corrí el diagnóstico de separación **antes** de preguntar nada?
2. ¿Presenté el veredicto con sus números, y dije que **los umbrales son una elección**?
3. ¿Puse algún nombre que **ella no haya afirmado**? **Jamás.**
4. ¿Apliqué una presentación del audio como si fuera un dato? **Solo se enseña como candidata.**
5. ¿Cada etiqueta lleva **quién la afirmó y cuándo**?
6. ¿Dejé claro **qué voces siguen sin nombre**, en vez de callarlo?
7. ¿Etiqueté una voz que el diagnóstico marcó como fundida, sin que ella aceptara la advertencia?
8. ¿Sobrescribí la transcripción anterior? **Nunca: archivo nuevo.**
9. ¿Me pidieron un acta y la hice «de paso»? **Eso no se hace aquí.**

**Al terminar esta lista, escribe este bloque al final de la entrega.** Es la única parte de este método que habla de sí mismo, y existe para una sola cosa: **hoy nadie sabe cuánto atrapa esta comprobación.** Se sabe que un error la atravesó y llegó al entregable; no se sabe si atrapó cuarenta o ninguno, y mientras no se sepa, **recortar esta sección y dejarla como está son las dos igual de defendibles**, que es justo lo que impide decidir.

```text
LO QUE ESTA PASADA SE CORRIGIÓ A SÍ MISMA
  Datos que volví a abrir y comprobar: «N»
  Corregidos al comprobarlos: «N» — «cuáles, por su etiqueta»
  No se pudieron comprobar: «N» — «cuáles y por qué»
  Preguntas de esta lista que me hicieron corregir algo: «sus números»
  «o: ninguna»
  Esto cuenta correcciones hechas, no errores que queden. Cero
  corregidos significa que la comprobación no encontró ninguno, nunca
  que no los haya. Y lo escribe quien hizo el trabajo: no prueba que
  esta salida sea correcta.
```

**Tres reglas sobre este bloque, y la tercera es la que lo hace servir de algo:**

1. **Anotar no sustituye a corregir.** La corrección va en la entrega como siempre; aquí solo se dice que ocurrió.
2. **Este bloque no decide nada.** No retiene la entrega, no rebaja ninguna etiqueta, no cambia una sola palabra de lo demás.
3. **Ni se infla ni se esconde.** Un número alto es buena noticia —quiere decir que la comprobación funciona—, y cero con muchas comprobaciones también es información. **Lo único que arruina esta medida es un número que no sea verdad**, y no hay nada que ganar falseándolo: no se te evalúa por él.
