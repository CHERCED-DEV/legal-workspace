# La fusión que trajo el duodécimo método — qué se rompió y qué lo dijo

**Fecha:** 2026-09-22 · **Rama:** `claude/backlog-continuacion-jm9x69` ← `origin/master`

`master` traía un método nuevo, `/transcribir-audio`, cuatro programas, cuatro ADR
y una página local. La rama traía las guardas. **Lo que sigue es lo que las guardas
dijeron al juntarlas, y es el resultado que más vale de este documento: se juntaron
dos trabajos que no se habían visto nunca, y la suite dijo exactamente en qué se
contradecían, en el primer intento.**

---

## 1. Lo que falló, y por qué eso es lo que se quería

Dieciséis fallos en cuatro archivos de prueba, **ninguno por un error de la fusión**
y **todos porque el producto cambió de tamaño**:

| Guarda | Qué dijo | Era |
|---|---|---|
| `test_bloques_identicos` | el método nuevo **no tiene** el bloque de posición, ni el de la pasada, ni la cláusula de la fecha | cierto: llegó sin ninguno de los seis bloques compartidos |
| `test_superficie` | hay cuatro programas **sin clasificar**, y un método que nombra `1-Documentos recibidos/` y no está en la cuenta | cierto |
| `test_dependencias` | hay **tres** bibliotecas externas que este archivo no conoce | cierto: `faster-whisper`, `av`, `sherpa-onnx` |
| `test_documentos_vigentes` | el `ESTADO-DEL-PROYECTO` dice **once métodos y diez programas**, y en el disco hay **doce y catorce** | cierto |

**Ninguno de los cuatro se habría visto leyendo.** El `SKILL.md` nuevo está bien
escrito y se lee entero sin que salte nada; lo que falta en él es **lo que los otros
once tienen y él no**, que es una comparación, no una lectura.

---

## 2. La contradicción de fondo, que no era de conteo

Tres métodos —`hechos-con-prueba`, `inventario-de-anexos`, `inventario-de-bienes`—
decían de una transcripción: **«este método no la produce»**, y remataban con que,
sin ella, la grabación se declara y ahí termina.

**Desde la fusión, la primera mitad sigue siendo verdad y la segunda dejó de serlo.**
Ninguno de los tres la produce; pero hay un camino, y antes no lo había.

Lo que **no** cambia, y es lo que había que escribir sin partirlo en tres:

> Lo que sale de `/transcribir-audio` **es trabajo del sistema** —pista, nunca
> origen—. **No entra como material por haber salido**; entra cuando ella lo revisa
> y le pone ` - REVISADO`. Mientras no lleve esa marca, la grabación sigue declarada
> y sin usar. **Que ahora se pueda transcribir no es que ahora se pueda oír.**

Está escrito **una vez**, copiado byte a byte en los tres, y hay una guarda que falla
si alguno de los tres lo reescribe con otras palabras — que es el modo de avería que
este repositorio lleva documentado desde el principio.

---

## 3. Los cuatro programas nuevos, y la clase que hubo que inventar

`test_superficie` obligó a decidir de qué lado va cada uno, y **tres de los cuatro no
cabían en ninguna de las clases que había**:

- `transcribir_audio.py` → **expuesto**. Su método lo declara. Octavo de la superficie.
- `comparar_iteraciones.py`, `md2html.py`, `verificar_citas.py` → **ninguno de los dos
  lados**. No son `ADMIN` —no instalan, no migran, no reparan— y ningún método los pide.

Llamarlos `ADMIN` habría sido cómodo y habría diluido la clase **justo por donde el
documento de arquitectura avisa que se dilata**: *«la presión llega como una tool
pequeña y razonable»*. Así que se abrió una cuarta clase, `A_MANO`, con esto escrito:
**que no estén expuestos no es una regla de seguridad — es una decisión que nadie ha
tomado todavía.** La guarda que los cubre es la misma: mientras estén ahí, no pueden
aparecer en ningún `allowed-tools`.

---

## 4. Tres defectos **de las guardas**, encontrados al correrlas sobre código ajeno

Es el mismo resultado que el día 7, y por tercera vez: **lo que más encuentra es pasar
una guarda por encima de algo que no escribió su autor.**

1. **`test_integridad_del_metodo` solo conocía una forma de nombrar un archivo.**
   Buscaba `f"Nombre - {date...` y `transcribir_audio.py` usa `"Nombre - %s" % hoy`.
   **Los siete archivos que ese programa deja por grabación pasaron por delante de la
   guarda sin que los viera.** Una guarda ajustada a la forma que usaba su autor
   protege esa forma y nada más.

2. **`contar_fichas.py` acusaba a una salida correcta.** Sobre una transcripción decía
   «0 fichas» y «NO COINCIDE» — que además de ser falso es la manera de apagar el
   instrumento: un aviso encendido para siempre es un aviso que nadie mira. Ya había
   pasado con `preguntas-de-derecho`; ahora se reconoce también la familia de la
   transcripción, **por el título que escribe el propio programa y no por el nombre
   del archivo**, que se cambia al guardarlo en otro sitio. Y hay una prueba que lee
   el código del otro programa y falla si ese título cambia, porque si cambia el
   reconocedor se queda ciego **y nada falla**.

3. **`V-12` se había cerrado «con un grep» y sin dejar la guarda puesta.** El árbol del
   `README` del plugin —lo primero que lee quien instala— volvió a quedar mal en esta
   misma fusión. Ahora hay cuatro pruebas sobre él: que estén todos los métodos del
   disco, todos los programas, **que no nombre nada que no exista**, y que la cifra
   que dice sea la que hay.

---

## 4.bis Y los tres programas que llegaron sin una sola prueba

De los catorce programas, **cuatro entraron por la fusión y ninguno traía prueba**. Uno
—`transcribir_audio.py`— no se puede probar aquí. Los otros tres no dependen de nada, y
**cada uno cargaba un defecto ya corregido en `master` y sin nada que lo sujetara**.

| Programa | Lo que ahora se sujeta | El defecto del que sale |
|---|---|---|
| `verificar_citas.py` | una cita corta que **no** está puntúa bajo; una partida con `[…]` vale lo que su **mitad peor** | *«aprobaba en blanco toda cita de menos de cuatro palabras»* |
| `comparar_iteraciones.py` | dos carpetas idénticas **no listan ni un tramo**; dos distintas sí | *«rellenaba la lista hasta N»*, haciendo pasar por dudoso lo que no lo era |
| `md2html.py` | **cero peticiones de red**: ni direcciones, ni `src`/`href` a otro origen, ni tipografías remotas | `ADR-020` §3 — **una página que pide algo a un servidor cuenta lo que ella está leyendo** |

Veintiuna pruebas, en `evals/scripts/test_programas_de_la_fusion.py`. Las tres familias se
comprobaron con mutantes; meter una tipografía de Google en la plantilla hace fallar **tres
guardas independientes**.

> **Y lo que esta tanda NO encontró, dicho porque el instrumento también se equivoca.** Una
> de mis pruebas afirmaba que la página no debía traer elemento de audio cuando no hay
> grabación. **Lo trae siempre, vacío y oculto, y declara la ausencia con todas las letras**
> —*«no se encontró la grabación… no se puede comprobar oyendo»*—, que es lo que `ADR-020` §5
> pide, y es mejor que no traer nada: sin esa frase, quien lee no sabe si falta el audio o si
> ese material no lo tiene. **La prueba que estaba mal era la mía.**

**Un defecto pequeño y real, corregido de paso:** `verificar_citas.py` abría los archivos sin
cerrarlos. En CPython el contador de referencias los cierra enseguida y no se nota; se arregló
porque era el archivo que se estaba probando. **El mismo patrón está en otros ocho sitios del
plugin y NO se tocó**: cambiarlo sería reescribir programas ajenos sin una prueba que pudiera
demostrar la diferencia, y en este repositorio eso no cuenta como corrección.

---

## 5. Lo que este documento NO puede decir

- **`/transcribir-audio` no se ha ejecutado aquí, y no se puede.** `faster-whisper`,
  `av` y `sherpa-onnx` no están en este entorno. Lo único que se comprobó es que,
  sin ellas, **declara cuál falta y no revienta** — y que la línea de comando que su
  Fase 2 documenta es la que su `argparse` acepta, con las tres opciones de su tabla.
- **Su medición no es de aquí.** Los números de su §4 —3,1× más rápido, 8,4 % de
  palabras perdidas por lotes, 12 hablantes con el umbral a 0,60— vienen de la máquina
  donde se escribió, sobre 56 min 52 s de reunión real. **No se reprodujeron.**
- **Nadie ha visto una transcripción de este producto al lado de su audio.** Que el
  método diga bien lo que no sabe no prueba que lo que sí escribe sea correcto.
