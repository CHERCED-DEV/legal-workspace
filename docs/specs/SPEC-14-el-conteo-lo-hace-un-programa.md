# SPEC-14 — El conteo que se pedía a ojo

**Estado:** ejecutada · **Origen:** la primera pasada real de `hechos-con-prueba` sobre el `caso-03`, 2026-09-05 · **Familia:** defecto

---

## 1. Qué problema cierra

La Fase 6 de `hechos-con-prueba` pide, punto 3:

> *«**Cuenta y entrega el conteo:** cuántos hechos propuestos, cuántos apoyados, cuántos sin apoyo, cuántos contradichos, cuántos vacíos, cuántos descartes. **El conteo es un instrumento de honestidad**: obliga a mirar la proporción real de lo que produjiste.»*

**Y no dice con qué hacerlo.**

El 2026-09-05 se ejecutó el método entero contra el `caso-03` —seis piezas, veinte fichas— y el conteo de esa pasada salió **mal**: declaró *«10 apoyados · 7 sin apoyo»* donde había **9 y 6**. El total (20) sí cuadraba, que es lo que hace peligroso este error: **la cifra que se revisa está bien y las que se leen están mal.**

**La causa es concreta y reproducible, no un descuido:**

> **«Apoyado y contradicho» empieza por «Apoyado».**

Tres fichas llevaban ese estado. Al recorrer la salida, cada una se leyó como apoyada *y además* se contó en su propia categoría. El mismo mecanismo, en la otra dirección, infló los *sin apoyo*.

### Por qué esto no se arregla pidiendo más cuidado

Es el **tercer conteo mal hecho del mismo día** en este repositorio, y los tres son la misma operación:

| Cuándo | Qué se contó | Dijo | Era |
|---|---|---|---|
| 2026-08-26 | Skills que tocan fechas (`H-03` del commit del arnés) | tres | **siete** |
| 2026-09-05 | `SKILL.md` que justifican la protección de escritura (§10 del backlog) | tres | **siete** |
| 2026-09-05 | Fichas apoyadas y sin apoyo de esta pasada | 10 y 7 | **9 y 6** |

Los tres se corrigieron **con un comando**, ninguno releyendo. Y el segundo lo cometió quien estaba señalando el primero, dos apartados más abajo. **La conclusión de esta sesión, aplicada aquí:** *el cuidado no basta y hace falta la guarda*.

## 2. Comportamiento observable

1. Tras escribir el `.md`, el método **ejecuta el programa** que cuenta las fichas por estado.
2. El programa **contrasta lo contado con el conteo que la salida declara** y, si no coinciden, lo dice y sale distinto de cero.
3. El programa **no juzga la salida**: cuenta lo que dice. La proporción sigue siendo información para ella.
4. **Si el programa no está o falla**, el conteo se hace listando las fichas una por una —nunca de memoria— **y se dice en la entrega**. El comando funciona sin él, peor, y diciéndolo. Es la misma regla que ya rige para el conversor a Word.
5. Una ficha **sin estado legible**, o con un **sexto estado inventado**, se denuncia por su etiqueta. La Fase 5 dice que los estados son cinco y que no se renombra ninguno; ahora eso se comprueba.

## 3. Qué se cambió

| Dónde | Qué |
|---|---|
| `plugins/despacho/scripts/contar_fichas.py` | **Nuevo.** Cuenta por estado, contrasta con lo declarado, denuncia fichas sin estado y estados inventados |
| `hechos-con-prueba` frontmatter | `contar_fichas.py` entra en `allowed-tools` |
| `hechos-con-prueba` Fase 6, punto 3 | La invocación, el porqué con su medición, y qué hacer si el programa no está |
| `evals/scripts/test_contar_fichas.py` | **Nuevo.** Seis pruebas. La primera es el fallo concreto: que «Apoyado y contradicho» no se cuente como apoyado |
| `evals/scripts/test_superficie.py` | La superficie pasa de **seis programas a siete**, con la razón escrita en la propia línea |

## 4. Lo que esta spec NO hace

- **No cambia ningún estado, ni añade uno.** Los cinco de la Fase 5 siguen siendo los cinco.
- **No decide nada sobre la salida.** Que seis de veinte hechos se sostengan solo en lo que la clienta dijo es información para ella, no un veredicto del programa.
- **No convierte el conteo en un control de calidad.** Un conteo correcto de una salida mala sigue siendo un conteo correcto.

## 5. Y una nota sobre la superficie, porque crece

`architecture-post-v0` §iv pide que las operaciones que el modelo puede invocar **se cuenten**, y que la cuenta la vigile una prueba: *«si algún día cuenta más de cero, la frontera se movió»*. Aquí la frontera se movió **de seis a siete**, y por eso esta sección existe.

**El criterio que lo justifica ya estaba escrito en el plugin**, en `preparar-material`: *«descomprimir, ordenar, copiar sin tocar, calcular huellas […] son trabajo mecánico con respuesta correcta comprobable: los hace un programa»*. Contar fichas por estado es exactamente eso — y a diferencia de las otras seis, **esta entró con la medición del fallo delante**, no por adelantarse a él.
