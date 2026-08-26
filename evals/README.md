# Banco de medición del arnés Despacho

> **Por qué existe.** Hasta hoy toda afirmación sobre si una versión del arnés es mejor o más barata que otra era una opinión. Este banco la convierte en una cifra. La primera vez que se corrió ya corrigió tres errores del plan de mejora que iban a dirigir el trabajo al sitio equivocado.

**Esto no es producto.** Vive fuera del plugin, no se instala en la máquina de nadie y no viaja al Despacho de ella.

---

## Cómo se corre

```bash
python evals/medir.py <run_id> \
  --caso evals/casos/caso-01-familia.json \
  --salidas "<ruta a la carpeta 2-Borradores del caso>" \
  --version 0.2.0 \
  --guardar evals/resultados/<fecha>-v0.2.0.json \
  --comparar-con evals/resultados/2026-08-26-v0.1.0.json
```

`--comparar-con` es lo que convierte la medición en evidencia: imprime el antes y el después de cada cifra, y **avisa en primer lugar si la veracidad ha retrocedido**.

---

## Qué mide, y por qué cada cosa

### Veracidad — manda sobre todo lo demás

| Cifra | Qué significa |
|---|---|
| **fabricaciones** | Veces que una salida atribuyó contenido a una página que no tiene ni una letra. **Debe ser cero.** No es cuestión de criterio: esas páginas están vacías, y afirmar algo sobre ellas es inventar |
| **páginas declaradas** | Cuántas de las ilegibles se dicen ilegibles. Omitirlas en silencio es el fallo que no se ve |

> **Regla de aceptación: una versión que baje el coste a la mitad y produzca una sola fabricación se descarta.** La fiabilidad es lo caro de conseguir y lo que no se repara después.

### Coste — las cuatro cantidades **por separado**

Medirlas juntas fue lo que hizo creer que recortar el método ahorraba algo. No lo hace:

| Cantidad | Qué es | Lo medido en v0.1.0 |
|---|---|---|
| **entrada nueva** | Lo que se paga a precio completo | **528 tokens** para los cinco comandos |
| **caché escrita** | Contexto nuevo que se guarda | 2,2 M |
| **caché leída** | Contexto reutilizado | 33,8 M |
| **salida** | Lo que el modelo escribe | 360 K |

**El método va al frente del contexto, que es lo más cacheable que existe.** Por eso la entrada nueva de un comando entero son decenas de tokens: recortar prosa del método no ahorra lo que parece. El gasto está en la salida y en el contexto nuevo que cada turno acumula.

### Volumen — el motor que no aparece en ninguna factura

**Decisiones que le exige** cuenta *piezas*, no marcas. Cada ficha ofrece tres casillas y aparece dos veces —en la hoja y en su propia ficha—, así que contar marcas multiplica por seis el trabajo real. Es la cifra que traduce el diseño a horas de ella.

---

## Cómo distingue un comando de un evaluador

**Por lo que escribe, no por lo que lee.** Un comando deja una entrega en `2-Borradores/`; un evaluador abre los mismos métodos para juzgarlos y no escribe nada. Contarlos juntos mezclaría el coste del producto con el de medirlo — trabajo que ella nunca va a pagar.

No se usan las etiquetas del orquestador: en la primera medición llegaron **vacías en las seis filas**, y una medición que depende de que alguien haya etiquetado bien no es un instrumento.

---

## Lo que la primera medición corrigió

El plan de mejora, escrito antes de que existiera este banco, afirmaba tres cosas que resultaron falsas:

| El plan decía | La medición dice |
|---|---|
| El comando más caro es `hechos-con-prueba` (97 turnos) | Es **`inventario-de-anexos`**. `hechos-con-prueba` son 84 |
| El más barato es `revisar-documento` (16 turnos), *«y salió barato por el alcance»* | El de 16 es **`redactar-escrito`**, que **se negó a trabajar** — barato por no hacer nada. `revisar-documento` son 37 |
| No se puede separar lectura de caché de entrada nueva, así que no se sabe qué paga el método | **Sí se separan.** La entrada nueva son 528 tokens en total: el método casi no se paga |

De ahí colgaba la mejora principal del plan, apuntada al comando equivocado con una teoría construida sobre una atribución falsa. **Ese es el argumento entero a favor de medir antes de optimizar.**

---

## El material del caso

**No está en este repositorio y no lo estará.** `casos/caso-01-familia.json` contiene solo el truth set y las cifras de referencia; los documentos son de una clienta real, con datos de una menor, y los custodia el dueño. Para volver a correr la medición hacen falta los dos PDF originales.

**Por qué el truth set vale:** los anexos llegaron escaneados y 25 de sus 39 páginas no tienen una sola letra. Cualquier afirmación sobre ellas es una fabricación *por construcción*, sin margen de interpretación y sin depender de quién evalúe. Un caso sintético escrito por nosotros nunca habría dado ese instrumento.

---

## Límites de lo medido — leer antes de citar estas cifras

- **Un solo caso, de 56 páginas con 14 legibles.** El coste crece con lo que hay que recorrer, y cada turno rearrastra lo acumulado: **un expediente de 300 páginas no cuesta cinco veces más, cuesta más que eso**. Nada de lo medido autoriza a decir que el arnés funciona en un caso grande. Es la siguiente medición que hace falta.
- **Una sola ejecución por comando.** No hay varianza: no se sabe cuánto de lo medido es el método y cuánto es esa pasada concreta.
- **Ejecutado por agentes de orquestación**, no desde la ventana de ella. Los números sirven para comparar versiones entre sí; **no** para prometer cuántas jornadas de un plan de pago aguanta.
- **La detección de fabricaciones depende del vocabulario** con que los métodos declaran lo ilegible (la lista `DECLARA` en `medir.py`). Si un método cambia esas palabras, hay que actualizarla. Es la parte frágil del instrumento y conviene saberlo.
