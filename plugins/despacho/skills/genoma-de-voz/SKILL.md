---
name: genoma-de-voz
description: "Método para saber quién dice cada línea de una reunión grabada, con la huella de voz de cada línea y la declaración de ella. La máquina propone por parecido y ella declara oyendo, en una página que se abre en el navegador, guarda cada decisión y mide cuánto de cada grabación quedó claro contra una meta del 85 %. Solo lo que ella declaró sostiene una atribución. Úsalo después de transcribir-audio, con todas las grabaciones de la misma reunión juntas, cuando haga falta saber quién dijo qué y la separación automática de voces no aguanta o nombrar-voces se niega a etiquetar. No lo uses para transcribir, para poner un nombre que ella no declaró ni para redactar el acta. No toca el audio ni la transcripción."
version: 0.1.0
allowed-tools: Bash(python ${CLAUDE_PLUGIN_ROOT}/scripts/genoma_de_voz.py *)
---

# genoma-de-voz — quién dice cada línea, con la huella de la voz y la última palabra de ella

## 1. Cuándo usar este método y cuándo no

**Propósito.** Una transcripción dice **qué** se dijo. Este método dice **quién lo dijo, línea por línea**, y deja escrito cuánto de eso lo declaró ella oyendo y cuánto es solo una propuesta de la máquina. Cada línea tiene una **huella de voz** —512 números que calcula el mismo modelo que ya usa `transcribir-audio`—; la máquina agrupa las huellas que se parecen y **propone** una voz; ella oye la línea y **declara** quién habla, o que no se distingue, o que hablan varios a la vez.

**Úsalo cuando:**

- `nombrar-voces` dijo que la separación **no sirve** y se negó a etiquetar. Este método **no depende de ese agrupamiento**: trabaja línea por línea, con la huella de cada una.
- Hace falta atribuir intervenciones —en un acta, en un resumen, en un compromiso— y hay que saber quién habla en cada tramo, no en cada grupo de sonido.
- La reunión quedó partida en varias grabaciones. **Van juntas**, en una sola preparación, y así la misma persona es la misma voz en todas.

**No lo uses para:**

- **Transcribir.** Eso es `transcribir-audio`, y va antes: este método necesita, por cada grabación, su archivo `datos/<código> - datos completos.json` y el audio original.
- **Poner un nombre que ella no declaró.** Ni aunque la biblioteca de voces lo sugiera con un parecido alto.
- **Redactar el acta o el resumen.** Eso es `acta-de-reunion`, y este método le da de comer (§6), no lo sustituye.

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

## 2. El principio rector

> **La máquina propone por parecido. Ella declara oyendo. Las dos cosas se ven distintas en todo momento, y solo lo declarado sostiene una atribución.**

Tres consecuencias que no se negocian:

1. **Una propuesta no se convierte en declaración por tener un nombre.** Si ella dijo quién es la Voz 2, una línea que la máquina le atribuye a la Voz 2 y que nadie ha oído **sigue siendo propuesta**, y se escribe como propuesta.
2. **Nadie nombra salvo ella.** Los nombres de una declaración anterior y los de la biblioteca de voces **se ofrecen**, para no teclearlos otra vez; ninguno se aplica solo.
3. **La biblioteca de voces se hace solo con lo declarado.** Una biblioteca que se alimenta de las conjeturas de la máquina acaba creyéndoselas, y en la reunión siguiente las propone con más seguridad.

### 2.1 Lo que está medido, y por qué el método es así

Medido el 2026-09-23 sobre una mesa de trabajo real de tres grabaciones (`SPEC-15-genoma-de-voz` §1). **No son estimaciones.**

| Hecho | Cifra | Lo que obliga |
|---|---|---|
| Lo transcrito que la separación automática le dio a **una sola voz** en la primera grabación, con al menos tres personas en la sala | **96,5 %** | No se decide sin que alguien oiga: el agrupamiento solo no aguanta este material |
| Turnos donde dos personas hablan a la vez | **19–34 %** | Una línea que se pisa en el 30 % o más de su duración **no entra en la huella de nadie** |
| Parecido entre las dos mitades de un mismo turno largo | **0,96** | La huella **sí distingue** personas… |
| Parecido entre dos turnos distintos | **0,75** | …y esa distancia es la que la máquina usa para proponer |
| Parecido de una línea entera con su propia mitad, midiendo sin ventana fija | **0,82** | Absurdo: el todo debería parecerse más. **La huella se desplaza con el largo del trozo** |
| Lo mismo, con ventanas fijas de 1,5 s | **0,95** | Por eso todo se mide en ventanas fijas de 1,5 s, y cada línea es la media de sus ventanas |

**La conclusión de esas cifras es la que da forma a todo lo demás:** la huella distingue personas; lo que falla es **decidir sin que nadie oiga**.

**Y lo que significa para cómo habla la gente.** Unos hablan rápido y en frases cortas; otros despacio y en parrafadas. Con ventana fija, una línea de diez segundos y una de dos se miden **a la misma escala**: la larga es la media de muchas ventanas, la corta de pocas. Una línea de **menos de un segundo** no llena ni una ventana: se mide tomando contexto a los dos lados, se marca **corta**, y **nunca** entra en la banda alta. Es la cautela correcta — en un segundo cabe un «sí» de cualquiera.

**Y cuando la voz cambia a mitad de línea** —alguien interrumpe, o el reconocedor juntó dos turnos—, el programa busca el corte que más separa las dos partes. Si esas dos partes se parecen menos que casi todo lo demás de la reunión, la línea sale marcada con **la palabra donde cambia**, y ella puede dividirla ahí.

---

## 3. El procedimiento

### Fase 1 — Preparar: todas las grabaciones de la misma reunión, en una sola corrida

```
python ${CLAUDE_PLUGIN_ROOT}/scripts/genoma_de_voz.py preparar \
  --par A1 "datos/A1 - datos completos.json" "<grabación 1>" \
  --par A2 "datos/A2 - datos completos.json" "<grabación 2>" \
  --titulo "<reunión>" --salida "<proyecto>/2-Borradores/Voces"
```

Los `datos/` son los de la versión de la transcripción que se va a usar, en `2-Borradores/Transcripciones/<AAAA-MM-DD> - <qué cambió>/datos/`. **La salida, en un proyecto del Despacho, es `2-Borradores/Voces/`** (ADR-023), y ahí van también las de `aplicar`.

| Opción | Cuándo |
|---|---|
| `--par <código> <datos> <audio>` | **Una vez por grabación, y todas las de la misma reunión en la misma corrida.** Prepararlas por separado da voces que no se corresponden: la Voz 1 de una no es la Voz 1 de otra |
| `--personas <declaración>.json` | Una declaración de `nombrar-voces`, o una que ella ya exportó de esta página en otra preparación. **Solo ofrece nombres** para no teclearlos; no dice quién habla ninguna línea |
| `--biblioteca <biblioteca>.json` | Las huellas de personas que ella ya declaró en otras reuniones. Si una voz se parece 0,80 o más, la página **sugiere** el nombre con su parecido y de dónde sale; nunca lo asigna |
| `--rescatar` | **Vuelve a oír solo los huecos** —los tramos de más de 3 s sin ninguna línea publicada—, en la mezcla, el canal izquierdo y el derecho por separado, y mide cuánto coinciden. Necesita `faster-whisper` y tarda unos minutos en GPU. Ver abajo |

**`--personas` y `--biblioteca` no se pasan por defecto.** Cada una trae algo que no salió de esta reunión, y eso se decide, no se hereda. **`--rescatar` sí conviene casi siempre**: medido el 2026-09-23 sobre una mesa real, los huecos sumaban 6 min 18 s de reunión, y al volver a oírlos salió contenido de fondo que la transcripción entregada no tenía.

> **Por qué hay huecos.** `transcribir-audio` decodifica cuatro veces y publica **una** de las cuatro entera, la que más coincide con las demás. La elección es por grabación, no por tramo: donde esa lectura calla y otra oyó algo, lo que oyó la otra se pierde. El rescate recupera ese síntoma; la causa —elegir tramo a tramo— es trabajo de `transcribir-audio`.

**Deja dos archivos, y nunca pisa uno que ya exista:** `Voces - <reunión> - <fecha>.html`, la página donde ella trabaja, y `genoma - <reunión> - <fecha>.json`, los mismos datos para que `aplicar` los lea después. **La página no se mueve lejos de los audios**: los oye por ruta relativa, y si no los encuentra lo dice y no ofrece oír.

**Lo que imprime, y cómo se le presenta:**

- Las **voces propuestas**, con qué parte del habla se lleva cada una. **Sin nombre y sin confirmar**: son grupos de huellas, no personas.
- Cuántas líneas **se pisan**, cuántas son **cortas** y cuántas tienen un **posible cambio de voz** dentro.
- Los **huecos**: tramos de más de 3 s sin ninguna línea publicada. Si otra lectura de `transcribir-audio` escribió algo en una ventana que cae **entera** dentro del hueco, la página lo enseña; si no, el hueco se dice y no se rellena.
- Con `--rescatar`, **cuántos tramos rescató**, cuántos oyen dos pistas o más, y cuántos **parecen invención del reconocedor** —un «Gracias.» suelto sobre ruido es la invención más típica, y que las tres pistas lo «oigan» no prueba nada, porque las tres inventan lo mismo sobre el mismo ruido—. **Nadie ha oído ninguno**: se dice así.
- La **seguridad alta de la máquina**, marcada **«SIN MEDIR»**. **Eso no es claridad**: es lo que la máquina cree de sí misma, y todavía nadie lo ha comprobado. Presentarlo como claridad es el error que este método existe para no cometer.

**Si el programa se detiene**, escribe `DETENIDO:` y el motivo. **Se le dice tal cual y no se supone el resultado.** Los motivos posibles: falta `numpy` o `sherpa-onnx` (se instalan como dice `INSTALACION.md`); falta el modelo de huellas en `scripts/modelos/` (reponerlo es una operación de instalación, **no de este método**: se le dice al dueño); falta la página compilada; hay menos de cuatro líneas largas y limpias, y con eso no se puede proponer nada; o el archivo de salida ya existe (ADR-011 §8: se cambia `--salida` o se mueve el anterior, nunca se sobrescribe).

**Y si no hay Python, o no está `sherpa-onnx`, este método no tiene camino a mano.** El modelo no oye la grabación ni puede calcular una huella de 512 números: **no se finge**, ni se «estima» quién habla leyendo el texto. Se le dice que sin el programa no hay genoma, y se le ofrece lo que sí existe: `nombrar-voces` si la separación de voces aguanta, o escribir el acta en impersonal, que es el nivel 0 de `acta-de-reunion` §2.3.

### Fase 2 — Ella trabaja en la página

**Lo rescatado aparece como otra clase de línea**, marcada «Rescatado: no estaba en la transcripción», con las tres lecturas a la vista, cuánto se parecen —con el aviso de que tres lecturas de la misma grabación **no son tres testigos**—, y un campo con el texto para que **ella lo corrija oyendo** (se guarda mientras escribe). La pregunta ya no es solo quién habla, sino **si se dijo**: «Sí, se dijo, y es…», «Se dijo, pero no distingo quién» (`X`) o «Descartar: no se entiende, o no se dijo» (`Supr`). **Un rescate solo se acepta después de oírlo, y con texto.** Uno que ella no acepta no existe para ninguna salida, y los rescates no cuentan ni en la claridad —que es de las líneas publicadas— ni en el acierto de la máquina.

**Lo que cuenta como oído.** Una línea cuenta como oída cuando ella oyó **al menos el 70 %**; la página lo mide mientras suena y lo dice en la tarjeta. **Lo que decide sin oír es suyo pero no «oyendo»**: queda anotado, sale con _(sin oír)_ en las transcripciones, no cuenta para la claridad, no entra en la biblioteca de voces y no pone a prueba a la máquina.



Se le entrega la página y se le dice, en pocas frases, qué va a encontrar. La página la lleva en **tres momentos, en este orden**:

1. **Conocer las voces.** Dos líneas típicas de cada voz que pase de 20 s de habla, y una pregunta: **¿quién es esta voz?** Con tres partes —quién es, qué cargo o entidad, **cómo lo sabe**—, igual que en `nombrar-voces`. **«No sé» es una respuesta completa.**
2. **Poner a prueba a la máquina.** Líneas que la máquina da por seguras —banda alta—, **elegidas al azar**, hasta ocho. **Se le dice por qué:** de lo que ella conteste sale el acierto de la máquina, y sin ese acierto las propuestas de la máquina **no cuentan** para la claridad (§4). Al azar, porque si se eligen las más fáciles el acierto sale inflado.
3. **Lo que más aclara.** El resto, ordenado por segundos de habla multiplicados por la duda: primero las que cambian de voz a mitad y las que se pisan.

**Lo que ella puede decir de cada línea:**

| Ella dice | Qué queda escrito |
|---|---|
| **Es la voz que propone** | Confirmada: declarada por ella |
| **Es otra** | Corregida: otra voz de la reunión, o una persona nueva que ella añade |
| **Aquí cambia de voz** | Dividida en la palabra donde cambia, cada parte con su voz |
| **Hablan varios a la vez** | Declarada como habla simultánea. No entra en la huella de nadie |
| **No se distingue** | Declarada como tal. **No cuenta como clara**, y es una respuesta honesta, no un hueco |
| **Estas dos voces son la misma persona** | Se funden bajo una persona, y queda escrito que la máquina las tenía separadas |

**Cada decisión recalcula la huella de cada voz y las propuestas de todas las líneas que ella no ha decidido**, y la página dice **cuántas líneas cambiaron de voz** con esa decisión. Mientras una voz tenga menos de dos líneas declaradas, se usa la huella inicial de la propuesta. Las líneas que se pisan, las de «varios» y las de «no se distingue» **no entran en la huella de ninguna voz**.

**Se guarda sola, en cada acción**, en el almacenamiento del navegador, y la página dice «guardado». Ella puede cerrarla y volver: sigue donde iba, **en ese navegador y en esa máquina**. Si el almacenamiento falla, la página lo dice y pide guardar. **Guardar en el navegador no es entregar: lo que vale es el archivo** (ADR-022).

**Y en la carpeta del proyecto, sin pasar por Descargas** (desde 2026-09-24). El botón **“💾 Guardar”** va en la cabecera, siempre a la vista. La primera vez ella elige la carpeta del proyecto (vale una por encima: la página baja sola por el camino que conoce). Desde ahí la página escribe `voces declaradas - <reunión>.json` en `2-Borradores/Voces` con cada decisión, y una copia fechada cada vez que pulsa. **Nunca escribe encima de lo que otro navegador dejó**: si ella está vacía y la carpeta tiene decisiones, le ofrece cargarlas; si la carpeta tiene algo que la página no tiene, lo aparta con fecha. **Donde el navegador no deja escribir en carpetas** (Safari en el Mac, Firefox), “💾 Guardar” descarga, y la página le dice que arrastre el archivo a `2-Borradores/Lo que declaré`: **una sola carpeta para todo lo descargado**, venga de la página que venga.

**La cabecera dice también si suenan las grabaciones** («🔊 3 de 3 grabaciones listas»). Si la página se abre desde dentro de un `.zip` —Windows la copia sola a una carpeta temporal— o sin las grabaciones a su lado, un aviso arriba, en rojo, lo dice con los pasos **del sistema que ella tiene**: en el Mac, doble clic sobre el `.zip`; en Windows, «Extraer todo…». Pasó el 2026-09-24: abierta desde el `.zip`, no sonaba nada y la página no lo decía.

**Si se arregla la página después de preparar**, no se vuelve a preparar —eso recalcula todas las huellas en la GPU—:

```
python ${CLAUDE_PLUGIN_ROOT}/scripts/genoma_de_voz.py pagina "genoma - <reunión> - <fecha>.json" --salida "<proyecto>/2-Borradores/Voces"
```

Rehace solo la página, con la plantilla de ahora y **la misma clave**: lo que ella ya declaró se carga igual. La anterior se mueve antes a `_anteriores/` (nunca se sobrescribe).

### Fase 3 — Revisar hasta la claridad, y exportar

La página enseña la claridad **por grabación y por voz**, contra la meta del 85 %, y la descompone: **cuánto declaró ella, cuánto suma la máquina y cuánto queda dudoso** (§4). Ella decide cuándo parar; lo que se le dice es cuánto falta y qué líneas lo reducen más.

Al terminar, su declaración `voces declaradas - <reunión>.json` está en `2-Borradores/Voces` (o, con Safari, la que arrastró a `2-Borradores/Lo que declaré`). **La página exige el nombre de quien declara**: sin él no hay declaración, hay una propuesta sin autor.

### Fase 4 — Aplicar lo que ella declaró

```
python ${CLAUDE_PLUGIN_ROOT}/scripts/genoma_de_voz.py aplicar \
  "genoma - <reunión> - <fecha>.json" "voces declaradas - <reunión>.json" \
  --salida "<proyecto>/2-Borradores/Voces"
```

| Opción | Cuándo |
|---|---|
| `--biblioteca <biblioteca>.json` | Si ella quiere que las personas que nombró se reconozcan en la próxima reunión. Ver la advertencia de §5 |
| `--word` | Si ella quiere los `.md` también en Word |

**Se detiene, y está bien que se detenga**, si la declaración es de **otra** preparación (la clave no coincide), si no dice quién la hizo, o si alguno de los archivos de salida ya existe.

**`aplicar` no se fía del resumen que escribe la página:** recalcula el acierto y la claridad desde cada decisión. Si sus números y los de la página no coinciden, **mandan los de `aplicar`**, y la diferencia se dice.

---

## 4. La claridad del 85 %, y por qué la máquina sola no la da

```
claridad de una grabación = segundos claros / segundos de todas sus líneas
```

**Una línea es clara si:**

- **ella la declaró oyéndola**: confirmada, corregida, dividida, o «varios» con al menos dos voces marcadas; **o**
- la máquina la propone en **banda alta**, y **solo si la máquina ya fue puesta a prueba**: ella revisó, **oyéndolas**, **al menos 8** líneas de banda alta **sorteadas por la página** —no elegidas por ella—, y la máquina acertó **al menos el 90 %**.

**Esa es la regla que hay que decir siempre que se dé la cifra: la claridad del 85 % no la da la máquina sola.** Sus propuestas solo cuentan cuando ella ha revisado **8 líneas sorteadas de banda alta, oyéndolas, con un acierto del 90 %**. Antes de eso, la claridad es **exactamente lo que ella declaró**, y la seguridad de la máquina no suma un segundo.

**El acierto** es, de las líneas que la máquina daba por seguras en el momento en que ella las decidió, cuántas confirmó tal cual. Una línea que ella tuvo que dividir **no cuenta como acierto**. Y se guarda la propuesta y la banda **de ese momento**, no las de después: si no, la máquina se calificaría con lo que aprendió de las correcciones de ella.

**Las bandas se calibran en cada reunión**, no se fijan de antemano. El margen de una línea es cuánto más se parece a su voz más cercana que a la segunda. **Alta** es un margen igual o mayor que la mediana de las líneas largas y limpias de esa reunión; **media**, el percentil 25; **baja**, el resto. **Una línea corta o que se pisa nunca es alta.**

**Lo que se le dice, siempre con el número:**

1. **Si la máquina fue puesta a prueba**, y cómo salió: *«acertó 29 de 30 (97 %)»*, o *«acertó 6 de 8 (75 %): no basta, así que la claridad es solo lo que usted declaró»*.
2. **La claridad de cada grabación contra el 85 %**, y cuánto de ella es declarado y cuánto suma la máquina.
3. **Qué grabaciones no llegan, y cuánto les falta.** La salida se produce igual: las líneas ≈ van marcadas como lo que son. **No se redondea hacia arriba, y las líneas que quedan no se callan.**

> **Y el 85 % no es una garantía de nada.** Es la meta de trabajo que fija `SPEC-15-genoma-de-voz`: que quede claro a quién pertenece la mayor parte del habla. **Una línea concreta se atribuye por ser ✔, nunca porque su grabación pase del 85 %.**

---

## 5. Qué entrega

Lo que escriben `preparar` y `aplicar` va en `2-Borradores/Voces/` (ADR-023), y ese es también el sitio de la declaración que ella exporta. La biblioteca de voces no: no es de un proyecto, es de la máquina de ella (ver la advertencia de abajo).

| Archivo | Qué es |
|---|---|
| `Voces - <reunión> - <fecha>.html` | La página donde ella oye y declara. Sale de `preparar` |
| `genoma - <reunión> - <fecha>.json` | Los datos de la preparación: huellas, voces propuestas, bandas. `aplicar` lo necesita |
| `voces declaradas - <reunión>.json` | Lo que ella guardó desde la página —la escribe la página en `2-Borradores/Voces`, o ella la arrastra a `2-Borradores/Lo que declaré` si su navegador descarga—: **su declaración**. Las copias con fecha al lado no se tocan |
| `Transcripcion con voces - <grabación> - <fecha>.md` | Una por grabación: cada línea con quién habla y su marca |
| `Declaracion de voces - <reunión> - <fecha>.md` | El registro: quién declaró, quién es cada voz y cómo lo sabe, la claridad de cada grabación contra el 85 %, el acierto medido de la máquina y lo que ella le corrigió |
| `voces por linea - <reunión> - <fecha>.json` | Lo mismo, para otro programa o para un chat |
| La biblioteca de voces | Solo con `--biblioteca`: la huella de cada persona **nombrada**, hecha **solo con líneas que ella declaró**, y con un mínimo de tres. La copia anterior va a `_anteriores/` |

**Las tres marcas, que se distinguen sin color:**

| Marca | Qué significa |
|---|---|
| **✔** | Lo declaró ella oyendo esa línea |
| **≈** | Lo propone la máquina por el parecido de la voz. **Nadie lo ha oído: no sirve para atribuir** |
| **?** | Ella marcó que no se distingue quién habla |

> **Una advertencia que va con la biblioteca.** La huella de voz de una persona con nombre es un dato biométrico de esa persona. **Vive en la máquina de ella y en ningún otro sitio**: no se adjunta a un chat, no se copia a otra carpeta compartida, no viaja con el caso. Si ella no quiere guardar huellas de nadie, no se pasa `--biblioteca`, y el método funciona igual.

**Y cierra siempre con lo que la salida no permite:**

```text
LO QUE ESTA ATRIBUCION DE VOCES NO DICE
· Solo las lineas ✔ las declaro ella oyendolas. Las ≈ son parecido de
  voz calculado por un programa: nadie las ha oido.
· Que una voz tenga nombre no convierte sus lineas ≈ en declaradas.
· La claridad mide cuanto del habla quedo atribuido, no si el texto es
  correcto: la transcripcion sigue sin ser la grabacion.
· El acierto de la maquina se midio sobre las lineas que ella reviso,
  no sobre todas.
· Los huecos sin transcribir no tienen voz porque no tienen texto.
  Que existan se dice; no se rellenan.
```

---

## 6. Qué hacer con la salida

**Sirve para refinar actas y resúmenes.** Se le pasa `voces por linea` —o la `Transcripcion con voces` de cada grabación— al chat donde se trabaja el acta o el resumen, **con la instrucción de respetar las marcas**: lo ✔ se puede atribuir; lo ≈ y lo ? se escriben **sin sujeto**, en impersonal. Un resumen que diga *«la Voz 2 propuso…»* sobre una línea ≈ atribuye algo que nadie oyó.

**En `acta-de-reunion`, la escala de atribución de su §2.3 exige siete condiciones para el nivel 2.** Este método aporta **una**:

- **Una línea ✔ es necesaria, pero no basta, para la condición 7.** La condición pide quién habla, **de qué entidad y cómo lo sabe**. Una línea ✔ de una voz sin nombre, sin cargo o sin «cómo lo sabe» dice que ella la oyó, no quién es. Por eso `aplicar` escribe en la `Declaracion de voces` una sección **«Para atribuir en un acta»** con lo que le falta a cada voz. Un párrafo del acta cumple la condición 7 si **todas** las líneas en que se apoya son ✔, de la misma persona, **y esa voz no aparece en esa lista**.
- **Las ≈ no la cumplen nunca**: ni en banda alta, ni con la máquina puesta a prueba, ni en una grabación que pase del 85 %. La claridad sirve para saber cuánto falta; **no convierte una propuesta en declaración**.
- **Las otras seis condiciones no las da este método.** Planilla firmada, una sola persona por entidad, autorreferencia en primera persona, una sola entidad en la ventana, tramo sin discordia y que no sea discurso referido **se siguen exigiendo igual**, y siguen siendo del acta.

**En `compromisos-de-una-reunion`**, el campo de quién se compromete se llena solo con una línea ✔. Con una ≈ se queda vacío, como si este método no se hubiera corrido.

**Con `nombrar-voces` no se mezcla.** Aquel nombra **grupos enteros** cuando la separación aguanta; este declara **línea por línea** cuando no aguanta, o cuando hace falta más precisión que la de un grupo. Si una grabación ya tiene sus voces nombradas con `nombrar-voces` y el diagnóstico dijo que la separación servía, este método no hace falta.

---

## 7. Lo que este método NO hace

- **No nombra a nadie.** Los nombres de una declaración anterior y los de la biblioteca **se ofrecen**; no se aplican.
- **No convierte una propuesta en declaración** por tener un nombre, por tener banda alta ni porque la grabación pase del 85 %.
- **No construye la biblioteca con propuestas de la máquina.** Solo con líneas ✔.
- **No decide que dos voces son la misma persona**, ni que una línea son dos voces. Lo propone; lo declara ella.
- **No rellena los huecos.** Si otra lectura escribió algo en un tramo sin transcribir, se enseña con su fuente; no pasa a la transcripción.
- **No toca el audio ni la transcripción original**, y **nunca sobrescribe** un archivo (ADR-011 §8).
- **No sube nada.** El audio, las huellas y la página se quedan en esta máquina; la página no usa la red (ADR-020).
- **No redacta el acta ni el resumen.**
- **No pone la marca ` - REVISADO`.** Esa la pone ella.

---

## 8. Autoevaluación antes de entregar

1. ¿Preparé **todas** las grabaciones de la misma reunión en **una sola** corrida?
2. ¿Corrió el programa de verdad? Si se detuvo, ¿dije el `DETENIDO` tal cual, sin suponer el resultado?
3. ¿Presenté la seguridad alta que imprime `preparar` como si fuera claridad? **No lo es: está sin medir.**
4. ¿La claridad que di es la que imprimió `aplicar`, y no la del resumen de la página?
5. ¿Dije si la máquina fue puesta a prueba, con cuántas revisó ella y cuántas acertó?
6. ¿Dije qué grabaciones no llegan al 85 %, y cuánto les falta?
7. ¿Hay algún nombre que no venga de una declaración de ella? **Jamás.**
8. ¿Traté alguna línea ≈ como atribución —en un acta, un resumen o un compromiso—? **Jamás.**
9. Si se pasó `--biblioteca`, ¿se quedó en su máquina?

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
