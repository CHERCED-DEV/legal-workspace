# SPEC-12 — Que cada pasada diga qué se corrigió a sí misma

**Estado:** ejecutada · **Cierra:** `PM-M-1` (c) y (d) · grupo `G23` · **Familia:** defecto

---

## 1. Qué problema cierra

`PM-M-1` es el ítem que más cosas bloquea de todo el backlog: **nueve ítems y las ~20 propuestas de recorte del corpus**. Su veredicto es *«prerrequisito de todo lo demás»*, y su argumento es que **ninguna de sus cuatro medidas toca el producto**: solo producen información.

Tiene cuatro partes. **Dos son mías y dos no:**

| Parte | Qué pide | Quién |
|---|---|---|
| (a) | Etiquetar con nombre de comando las cuatro filas de la tabla de coste | Necesita **los logs de una corrida** |
| (b) | Separar `input` / `cache_creation` / `cache_read` en esos logs | Necesita **los logs de una corrida** |
| **(c)** | **Que la fase de comprobación registre cuántos anclajes corrigió** | **Texto en los `SKILL.md`** |
| **(d)** | **Que cada pasada imprima qué preguntas de la autoevaluación provocaron una corrección** | **Texto en los `SKILL.md`** |

**Verificado contra el código el 2026-09-05:** `grep` de «cuántos anclajes», «anclajes corregidos», «qué pregunta», «disparó» en los once `SKILL.md` no devuelve **ninguna línea**. `hechos-con-prueba` §Fase 6 manda *«vuelve al material y abre cada anclaje que citaste, uno por uno»* y **no manda anotar el resultado de haberlo hecho**. Los once tienen autoevaluación y ninguno dice qué hizo con ella.

### Por qué (c) y (d) valen lo que valen

No es medición por medición. Cada una desbloquea una decisión concreta que hoy se tomaría a ciegas:

> **(c) decide si la Fase 6.1 se puede tocar.** Hecho medido: **un error atravesó esa fase y llegó al entregable**. Lo que nadie sabe es **cuántos atrapó**. Si atrapó cuarenta, recortarla es desmontar el control que sostiene el producto; si no atrapó ninguno en dos casos, es un coste que se paga por costumbre. **Hoy las dos historias son igual de defendibles, y esa es exactamente la situación que impide decidir.**
>
> **(d) desactiva o autoriza las seis propuestas de recortar autoevaluación.** Seis propuestas del corpus quieren quitar preguntas. Ninguna sabe qué pregunta atrapa qué. Una pregunta que no ha corregido nada en dos casos reales es candidata; una que corrige en cada pasada no se toca. **Sin este dato, recortar es tirar una moneda con el nombre de una ingeniería.**

### Y el límite, dicho antes que nada porque es una objeción real

> **`H-12`: «un autoinforme no es control».** Este instrumento es exactamente eso — **el propio modelo contando lo que él mismo hizo**— y esta spec **no pretende lo contrario**.
>
> Lo que produce no es evidencia de que la pasada esté bien: es evidencia de **qué hizo la pasada**, que es una afirmación distinta y más débil. Sirve para **comparar dos versiones del método** —si la versión B corrige la mitad de anclajes que la A, algo cambió— y **no sirve** para afirmar que una salida es correcta.
>
> **Y solo se vuelve fiable cuando algo pueda contradecirlo**, que es el banco de `G22` — bloqueado hoy porque el material del único fixture no está en este repositorio ni lo estará. Mientras tanto, este número **se cita siempre con esa salvedad**. Se construye igual, porque un instrumento imperfecto que se declara imperfecto es mejor que ningún instrumento y que veinte propuestas discutidas de oídas.

## 2. Comportamiento observable

1. Al final de cada entrega aparece un bloque fijo que dice **cuántos datos se volvieron a comprobar, cuántos se corrigieron al comprobarlos, y cuáles**.
2. Dice también **qué preguntas de la autoevaluación, por su número, hicieron corregir algo**.
3. Dice **cuántos no se pudieron comprobar y por qué**.
4. Si no corrigió nada, **lo dice, y dice que eso significa que la comprobación no encontró nada — no que no haya nada**.
5. El bloque **no cambia ni una palabra de lo que se entrega**. Es lo mismo de siempre, con una etiqueta al final que cuenta lo que pasó.
6. En los dos comandos cuyo trabajo lo hace un programa y **no reabren documentos**, el primer renglón dice `no aplica: lo hizo un programa` en vez de un número. **Inventar una cifra para llenar el hueco es peor que el hueco.**

## 3. Reglas duras

| # | Regla | De dónde sale |
|---|---|---|
| R-1 | **Cuenta correcciones hechas, nunca errores restantes.** «Cero corregidos» significa *la comprobación no encontró ninguno*, jamás *no los hay* | `H-06` · el vocabulario de la ausencia, que este proyecto ya tiene en las nueve skills |
| R-2 | **Registrar no sustituye a corregir.** La corrección entra en la entrega; el bloque solo dice que ocurrió | `PM-M-1` — «ninguna medida toca el producto» |
| R-3 | **Este bloque no decide nada.** No retiene una entrega, no rebaja una ficha, no cambia una etiqueta. Si empezara a gobernar algo, sería un decisor nuevo y no autorizado | ADR-008 |
| R-4 | **Ni se infla ni se esconde.** Un número alto es buena noticia —la comprobación funciona—; cero con muchas comprobaciones también es información. **Lo único que destruye la medida es un número que no sea verdad** | `H-12` |
| R-5 | **Se cita siempre con su salvedad:** es un autoinforme y no prueba que la salida sea correcta | `H-12` · `G22` |
| R-6 | **No mide nada de ella.** Ni su tiempo, ni sus decisiones, ni cuántas veces cambió de opinión. Mide la pasada | `V-3` mide horas-persona y es otro ítem, con su propio consentimiento |
| R-7 | **La redacción del bloque es idéntica en los once**, para que dos pasadas de dos comandos se puedan comparar | `EP-C06` — métricas homónimas con denominadores distintos |

## 4. Qué NO hace

- **No autoriza ningún recorte.** Produce el dato con el que después se discutirá cada propuesta, una por una y con la regla de composición de `PLAN-DE-MEJORA` §1 —**como máximo una por versión**— intacta.
- **No añade una fase.** La comprobación ya existe en los once; lo único nuevo es anotar su resultado.
- **No cuenta tokens, turnos ni coste.** Eso es (a) y (b), y necesita los logs de una corrida.
- **No es un control de calidad** y no se presenta como tal (R-5).
- **No se guarda en ningún registro acumulado.** Un archivo que acumule métricas a lo largo del caso es otro diseño y no está decidido.

## 5. Cómo se sabe que quedó

| # | Observable | Cómo se comprueba | Resultado |
|---|---|---|---|
| O-1 | Los **once** `SKILL.md` traen el bloque, con la misma redacción | `grep -c` de la frase canónica = 11 | **Pasa** |
| O-2 | En los once, el bloque exige el número de comprobados, el de corregidos y **cuáles** | Se lee la plantilla | **Pasa** |
| O-3 | En los once está escrito que cero corregidos **no** significa cero errores | `grep` de la regla | **Pasa** |
| O-4 | En los once se pide **el número de las preguntas** de autoevaluación que dispararon corrección | `grep` | **Pasa** |
| O-5 | En los once está la salvedad de que esto es un autoinforme | `grep` | **Pasa** |
| O-6 | En los once está la cláusula `no aplica: lo hizo un programa`, para que los dos que no reabren documentos **no inventen una cifra** | `grep -c` = 11 | **Pasa** |
| O-7 | Una pasada real que produzca el bloque con cifras | — | **Pendiente** |
| O-8 | Dos pasadas comparables del mismo caso, que es para lo que existe | — | **Pendiente, y depende de O-7** |

## 6. Qué toca

Los once `SKILL.md`, en la cabecera de su sección de autoevaluación: la instrucción de escribir el bloque, con su plantilla y sus tres reglas. **Un solo punto de inserción por archivo, texto idéntico**, para que no derive.

## 7. Qué queda fuera y por qué

- **`PM-M-1` (a) y (b).** Necesitan los logs de una corrida, que no tengo. Quedan en el bloque de lo que depende de una pasada real.
- **Acumular las cifras entre pasadas.** Sería un registro de medición dentro de la carpeta de ella, y **escribir en su carpeta algo que no le sirve a ella** necesita una decisión, no una spec.
- **Medir su tiempo** (`V-3`). Es el hueco más valioso del backlog del lado del negocio y **no se resuelve instrumentando al modelo**: se resuelve preguntándole a ella, con su permiso.
- **Que el número gobierne algo.** Un umbral que retenga una entrega convertiría un instrumento en un decisor (R-3). Si algún día hace falta, es un ADR.
