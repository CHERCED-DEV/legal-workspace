---
name: nombrar-voces
description: Método para ponerle nombre y cargo a las voces de una transcripción ya hecha, con una regla que no se rompe: quien nombra es la profesional, nunca la máquina. Mide primero si la separación de voces de esa grabación aguanta; si no aguanta, lo dice y se niega a etiquetar. Prepara una ficha con cuánto habla cada voz, tres muestras enlazadas al minuto para reconocerla y las presentaciones que haya en el audio, sin darlas por buenas. Recoge lo que ella declare —quién es, qué cargo, cómo lo sabe— y regenera la transcripción con las etiquetas y su procedencia. Úsalo después de transcribir-audio, cuando haga falta saber quién dijo qué. No interpreta, no deduce nombres y NO redacta actas.
version: 0.1.0
allowed-tools: Bash(python ${CLAUDE_PLUGIN_ROOT}/scripts/nombrar_voces.py *), Bash(python ${CLAUDE_PLUGIN_ROOT}/scripts/md2html.py *), Bash(python ${CLAUDE_PLUGIN_ROOT}/scripts/md2docx.py *)
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

### Fase 1 — Mirar si la separación de esa grabación aguanta

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

Después, si el entregable lleva página y Word, se regeneran desde el `.md` nuevo con `md2html.py` y `md2docx.py` — otra vez, **a archivos nuevos**.

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

## 9. Autoevaluación antes de entregar

1. ¿Corrí el diagnóstico de separación **antes** de preguntar nada?
2. ¿Presenté el veredicto con sus números, y dije que **los umbrales son una elección**?
3. ¿Puse algún nombre que **ella no haya afirmado**? **Jamás.**
4. ¿Apliqué una presentación del audio como si fuera un dato? **Solo se enseña como candidata.**
5. ¿Cada etiqueta lleva **quién la afirmó y cuándo**?
6. ¿Dejé claro **qué voces siguen sin nombre**, en vez de callarlo?
7. ¿Etiqueté una voz que el diagnóstico marcó como fundida, sin que ella aceptara la advertencia?
8. ¿Sobrescribí la transcripción anterior? **Nunca: archivo nuevo.**
9. ¿Me pidieron un acta y la hice «de paso»? **Eso no se hace aquí.**
