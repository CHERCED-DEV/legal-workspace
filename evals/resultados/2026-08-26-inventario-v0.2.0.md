# Ataque a `inventario-de-anexos` — resultado

**Fecha:** 2026-08-26. **Qué se probó:** reducir de cuatro recorridos del material a dos —una captura y una verificación en bloque— conservando todas las garantías.

---

## 1. El resultado, sin adornos

| `inventario-de-anexos` | v0.1.0 | v0.2.0 | |
|---|---:|---:|---|
| Turnos | 97 | **136** | **+40 %** |
| Salida generada | 75.524 | 87.801 | +16 % |
| Caché escrita | 320.293 | 709.506 | +122 % |
| Fabricaciones | 0 | 0 | igual |

**La reescritura no abarató el comando: lo encareció.** Y el experimento **no permite concluir que el método sea peor**, porque a mitad de la prueba cambió lo que el comando podía hacer. Se explica abajo.

**Ninguna de las dos cosas era la esperada, y las dos importan más que el ahorro que se buscaba.**

---

## 2. HECHO VERIFICADO — los escaneados sí se leen

El ejecutor de la v0.2.0 no se limitó al texto extraído: **abrió el PDF y recibió las páginas como imagen**. Comprobado en su rastro, no en su palabra: una llamada de lectura con rango `4-19` y **40 bloques de imagen en los resultados**.

Es decir: **lo que llamábamos «25 páginas ilegibles» no es ilegible.** Son páginas sin capa de texto, que la extracción no ve y el modelo sí.

### Lo que eso cambia

- **El 64 % del material probatorio vuelve a estar disponible.** Era el riesgo abierto más grave del proyecto y resulta que no existía en los términos en que se planteó.
- **La regla de fallo declarado sigue siendo necesaria pero cambia de sitio:** no es «si no hay texto, no lo uses», es «si no puedes leerlo *ni como texto ni como imagen*, dilo y no lo uses».
- **Explica el sobrecoste.** La v0.2.0 hizo un trabajo que la v0.1.0 no hizo: leer 40 imágenes cuesta turnos y cuesta contexto. **No son comparables**, y presentar el +40 % como un fallo del método sería tan falso como presentarlo como un éxito.

### Lo que encontró al leerlas — y esto es lo que decide el caso

Al abrir lo que antes se daba por perdido apareció material sustantivo que ninguna pasada anterior tenía:

- **La misma acta existe dos veces con texto distinto**: mismo número, misma fecha, misma hora de cierre, y tres cláusulas que dicen cosas diferentes. Una de las dos versiones **no tiene ninguna firma**; la otra está firmada solo por una de las partes.
- **El texto de la segunda versión coincide casi palabra por palabra con lo que una de las partes pidió por correo el día siguiente.** El método señaló la coincidencia y **no dijo qué se sigue de ella**, que es exactamente su trabajo.
- **Existe una tercera acta que no figuraba** en ningún inventario anterior.
- Las dos páginas descritas antes como «solo dicen CamScanner» son **dos citaciones**.

Nada de esto se habría visto nunca por la vía del texto extraído.

---

## 3. RIESGO — el truth set queda invalidado

El instrumento medía fabricaciones contra la lista de 25 páginas «ilegibles», bajo la regla de que *cualquier afirmación sobre ellas es una invención por construcción*.

**Esa regla ya no vale.** Si el modelo puede leerlas como imagen, afirmar algo sobre esas páginas puede ser perfectamente legítimo — y el instrumento lo contaría como acierto por el motivo equivocado: el «0 fabricaciones» de la v0.2.0 se debe a que el método **declaró** las páginas, no a que se abstuviera de inventar.

**Cómo se rehace, y es más trabajo pero da un instrumento mejor:** el truth set deja de ser *«qué páginas están vacías»* y pasa a ser *«qué dice cada página»*. Es decir, una transcripción de referencia de las 25, contra la que se contrasta lo que el comando afirme. Más caro de construir, y a cambio detecta el error que de verdad importa: **no citar una página vacía, sino citarla mal**.

Hasta que exista, **la cifra de fabricaciones de este banco mide menos de lo que parece** y hay que decirlo cada vez que se cite.

---

## 4. Qué se hace con la v0.2.0

**Se conserva.** No por el coste —que empeoró— sino porque:

- Cierra la duplicación de salida que un evaluador había medido (§4 y §5-C describían los mismos anexos dos veces).
- Saca a la luz las discordancias entre documentos, que antes quedaban enterradas.
- Conserva las garantías: la verificación contra el original sigue existiendo, reagrupada en una pasada, y la cita se sigue capturando al leer.

**Lo que no se puede afirmar:** que la estructura de «una captura, una verificación» ahorre. **Está sin probar**, porque la única corrida que la usó hizo un trabajo distinto. Para saberlo hace falta volver a correrla ahora que las dos versiones pueden leer imágenes.

---

## 5. Lo que este experimento enseña sobre cómo medir

Tres cosas, y las tres valen más que el resultado que se buscaba:

1. **Una medición se contamina en cuanto cambia la capacidad, no solo el método.** Nadie previó que el ejecutor abriría el PDF de otra forma. La próxima comparación tiene que fijar también **cómo se accede al material**, no solo qué método se usa.
2. **El instrumento no puede clasificar solo con fiabilidad.** Distinguir un comando de un evaluador por su rastro falla en los dos sentidos: el evaluador abre los mismos métodos y nombra las mismas entregas. Se intentó afinar la heurística tres veces y cada arreglo rompía el caso anterior. **Ahora la clasificación es tentativa, imprime el identificador de cada agente y se corrige con `--excluir`.** Un instrumento que admite que no puede decidir solo es mejor que uno que decide mal en silencio.
3. **El hallazgo llegó por hacer, no por analizar.** Once evaluadores leyeron los seis métodos y las salidas durante horas, y ninguno descubrió que los escaneados se podían leer. Lo descubrió un ejecutor al que se le pidió trabajo real.
