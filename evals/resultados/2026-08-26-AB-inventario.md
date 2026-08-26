# A/B de `inventario-de-anexos` — v0.1.0 contra v0.2.0

**Fecha:** 2026-08-26. **Diseño:** las dos versiones ejecutadas a la vez, con instrucción idéntica palabra por palabra, cada una sobre su copia limpia del mismo caso, con `2-Borradores/` vacía y **la capacidad igualada** — a las dos se les dijo que las páginas escaneadas se pueden leer abriendo el PDF por rangos.

**Que la capacidad quedó igualada no es una suposición: se comprobó.** v0.1.0 leyó 46 imágenes y v0.2.0 leyó 48. Esa era la contaminación que invalidó la medición anterior.

---

## 1. El resultado

| | v0.1.0 (4 recorridos) | v0.2.0 (2 recorridos) | |
|---|---:|---:|---|
| **Relecturas del material** | 29 | **13** | **−55 %** |
| **Turnos** | 175 | **115** | **−34 %** |
| Llamadas a herramientas | 112 | 74 | −34 % |
| **Tiempo** | 35 min 58 s | **28 min 58 s** | **−19 %** |
| Salida generada | 88.580 | 150.299 | **+70 %** |
| Caché escrita | 829.679 | 1.037.857 | +25 % |
| Imágenes leídas | 46 | 48 | +4 % |

### La entrega que recibe ella

| | KB | Palabras | Tablas | Filas |
|---|---:|---:|---:|---:|
| v0.1.0 | 52,9 | 7.197 | 3 | 54 |
| v0.2.0 | **51,6** | **7.169** | **2** | 46 |

---

## 2. Qué significa

**La hipótesis se confirma en lo que predijo.** Fusionar cuatro recorridos del material en dos baja las relecturas un 55 %, los turnos un 34 % y el tiempo un 19 %. La estructura de «una captura, una verificación en bloque» funciona.

**Pero el coste no desaparece: se traslada.** La v0.2.0 genera un 70 % más de tokens. Menos turnos, y cada turno más pesado — capturarlo todo de una vez tiene su precio, y se paga en generación, que es lo que más cuesta por unidad.

**Y aquí está el dato que decide:** ese 70 % **no llega a ella**. La entrega es de idéntico tamaño —de hecho 28 palabras menos— y con **una tabla menos**, que es justo la duplicación que un evaluador había medido (dos secciones describían los mismos anexos). El exceso se queda en trabajo interno: la captura completa de la Fase 1 se escribe como razonamiento, no como entregable.

Es decir: **el segundo motor del gasto —el humano, las páginas que ella tiene que leer y decidir— no empeora.** Ese era el riesgo real de una captura exhaustiva y no se materializó.

### Y encontró más

Con el mismo material y las dos leyendo las mismas imágenes, la v0.2.0 identificó **13 discordancias entre documentos** que la v0.1.0 no reunió, incluidas dos horas de terminación distintas para la misma audiencia y dos números de cédula para la misma persona. También pasó de 5 a 8 los hechos de la demanda que hoy no tienen ningún documento detrás.

Que encuentre más con menos turnos es coherente con el diseño: cuando el material se recorre una vez y se anota todo, las contradicciones quedan una al lado de otra en la misma tabla. Cuando se recorre cuatro veces buscando cosas distintas, no.

---

## 3. Veredicto

**Se adopta la v0.2.0.** Menos turnos, menos tiempo, la misma entrega, más hallazgos y una duplicación cerrada. El +70 % de generación interna es el precio, y hay que decirlo en vez de esconderlo tras las cifras que salieron bien.

**Lo que no se puede afirmar:** que esto se traduzca en más jornadas de trabajo para ella con su plan. Depende de cómo pese cada cantidad en la cuota, y eso no está publicado. Lo que sí se puede afirmar es la dirección: **menos turnos, menos tiempo y la misma entrega, con más trabajo hecho.**

---

## 4. Lo que queda por hacer con esto

- **Aplicar la misma estructura a los otros comandos**, midiendo cada uno. `hechos-con-prueba` tiene la patología contraria —26 ediciones para construir la salida, no 29 relecturas— así que la receta no se le puede copiar sin pensar.
- **Volver a medir con el truth set reconstruido.** El actual quedó invalidado y la cifra de fabricaciones mide menos de lo que parece. Este A/B compara coste con solvencia; no compara veracidad.
- **Fijar la capacidad en el propio método.** La lección de la medición anterior: si un método deja al modelo decidir *cómo* accede al material, dos pasadas del mismo método no son comparables entre sí. Los seis deberían decir explícitamente que un escaneado se abre como imagen.
