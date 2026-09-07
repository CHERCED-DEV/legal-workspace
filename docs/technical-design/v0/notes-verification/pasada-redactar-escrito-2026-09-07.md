# `redactar-escrito` sobre el `caso-03`, con la hoja marcada — 2026-09-07

**Qué se quiso probar.** La cadena completa del producto: el comando de hechos escribe, **ella marca**, y `/redactar-escrito` consume esa marca para producir lo único que ella firma.

**Y por qué no se había podido probar nunca.** Los dos casos de banco estaban, sin querer, en los dos estados de parada:

| Caso | Hojas marcadas | Qué hace el método |
|---|---|---|
| `caso-03` (antes de hoy) | **cero** | Se detiene: *«no hay hechos aprobados»* |
| `caso-02` | **dos** | Se detiene: *«no elijo cuál manda»* |

**Los dos estados de parada estaban probados y el estado normal no.** Por eso se materializó el que faltaba: `2-Borradores/Hechos - Hidraulica - 2026-09-05 - REVISADO.md`, un **fixture que lo dice en su primera línea** y que lleva un `NO` y un `A MEDIAS` a propósito.

---

## La Fase 1 pasa, por primera vez

**Hechos aprobados: sí.** Un archivo y solo uno, y se declara con su nombre exacto tal como está en el disco, que es lo que le permite a ella desmentirlo de un vistazo:

> `2-Borradores/Hechos - Hidraulica - 2026-09-05 - REVISADO.md`

**Lo que se usaría, y lo que no:**

| Pieza | Cuenta como | Por qué |
|---|---|---|
| `Hechos - Hidraulica - 2026-09-05 - REVISADO.md` | **fuente** | Termina en `REVISADO`. Es la decisión de ella |
| `Hechos - Hidraulica - 2026-09-05.md` | **no cuenta** | Es la propuesta sin marcar. Se nombra y no se usa de atajo |
| `Cronologia - Hidraulica - 2026-09-05.md` | **pista, no fuente** | No lleva la marca. Sirve para saber dónde mirar |
| `Revision de rigor - Hidraulica - 2026-09-05.md` | **pista, no fuente** | Igual |
| Inventario de anexos | **no existe** | Los anexos se nombrarían por lo que cada documento dice de sí mismo, y el cierre lo advertiría |
| DOC-01 a DOC-05 y la transcripción | **material** | Los cinco se abren y se leen por dentro |

**Y lo que la marca cambia de verdad, que es el punto:** de los veinte hechos, **dos llevan `NO` y uno lleva `A MEDIAS`**.

- `H-16` — la bomba de segunda, dicha en una llamada — **NO**. No entra en ningún escrito.
- `H-17` — lo que la vecina oyó — **NO**. No entra.
- `H-06` — la fecha del pago — **A MEDIAS:** *«dejar que yo dije el 9 y el comprobante dice el 7, sin dar por buena ninguna»*.

Sin la marca, los veinte se leen igual de bien y los tres pasarían. **Eso es lo que la marca hace, y no se puede sustituir por cuidado.**

## Y el método se detiene igual — en la Fase 2

Pasar la Fase 1 **no abre el paso**. La Fase 2 pide cuatro cosas que son de ella y de nadie más, y su regla es dura: *«no propones una clase de escrito. Elegir qué se presenta es decisión jurídica y estratégica; sugerirla es decidir por ella, aunque vaya en forma de pregunta amable»*.

Lo que el método produce, entonces, es esto:

> *Para armar el borrador necesito cuatro cosas suyas:*
> *1. ¿Qué escrito quiere que redacte? Dígamelo con el nombre que usa usted.*
> *2. ¿A quién va dirigido? Escríbamelo tal como debe aparecer.*
> *3. ¿Qué apartados debe llevar y en qué orden? O páseme un escrito suyo de modelo, o dígame si sigue el orden del que se contesta.*
> *4. ¿Qué hechos entran? Si prefiere, entran todos los que usted aprobó y le digo cuáles quedaron fuera.*
>
> *Y le adelanto lo de la cuarta: usted marcó `NO` en dos —la llamada del técnico sobre la bomba, y lo que la vecina oyó— y `A MEDIAS` en la fecha del pago. Esos tres los trato como usted los dejó.*

**Y espera.** La Fase 3 lo dice sin rodeos: *«si no dictó ninguno, no hay esqueleto que enseñar todavía — se pregunta y se espera»*.

---

## El resultado, dicho entero

**La salida más importante del producto tiene dos puertas independientes, y las dos son de ella.**

| Puerta | Qué exige | Se probó con |
|---|---|---|
| **Fase 1** | Que ella haya mirado los hechos, ficha por ficha, y lo haya guardado con la marca | Cero marcados (`caso-03` antes) · dos marcados (`caso-02`) · **uno marcado (hoy)** |
| **Fase 2** | Que ella diga qué escrito, para quién, con qué apartados y qué hechos entran | **Hoy**, y con la hoja marcada delante |

**Abrir la primera no abre la segunda.** Es la cuarta parada del producto en dos días de ejecutarlo, y las cuatro son correctas:

| # | Método | Dónde para | Por qué |
|---|---|---|---|
| 1 | `inventario-de-anexos` sobre el `caso-03` | Fase 2 | **Cero** hojas marcadas |
| 2 | `inventario-de-anexos` sobre el `caso-02` | Fase 2 | **Dos** hojas marcadas |
| 3 | `redactar-escrito` sobre el `caso-02` | Fase 1 | **Dos** hojas marcadas |
| 4 | `redactar-escrito` sobre el `caso-03` | **Fase 2** | Falta lo que solo ella puede decir |

> **Ninguna de las cuatro es un fallo, y conviene decirlo junto:** un producto que se detiene ante una precondición que no se cumple es lo que separa a este de uno que «va adelantando». Lo que sí es un dato para el dueño es la forma que tiene ese producto: **no produce nada que ella pueda firmar sin dos intervenciones suyas**, y la primera —revisar veinte fichas— no es rápida.

## Lo que sigue sin probarse

**El borrador mismo.** Ninguna de estas pasadas ha producido una sola frase de un escrito, porque las cuatro respuestas de la Fase 2 son suyas y no se inventan. Para probar la redacción haría falta **una quinta pieza de fixture: las cuatro respuestas**, y esa ya no es una simulación menor —es dictar la estructura de un escrito jurídico— así que **se deja sin hacer y se dice**, en vez de inventarla y medir contra ella.
