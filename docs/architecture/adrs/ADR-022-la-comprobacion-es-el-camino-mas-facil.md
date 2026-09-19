# ADR-022 — La comprobación es el camino más fácil, y deja rastro

## Estado

**CANDIDATO** — propuesto el 2026-09-19. Depende de `ADR-020`.
No se implementa hasta autorización explícita.

## Contexto

Tres ADR anteriores fijaron invariantes que **dependen de que una persona haga un trabajo
incómodo**, y los tres lo reconocen por escrito:

- `ADR-017` inv. 1 — ninguna cita literal sin cotejar contra la grabación. *«Difícil de hacer
  cumplir: nada impide técnicamente citar un segmento sin haberlo escuchado.»*
- `ADR-016` — la ausencia en el texto extraído no es información sobre el papel; hay que mirar
  la imagen.
- `ADR-014` §3 — el encabezado de propuesta es *«la única mitigación, y es débil»*.

El pase real del 2026-09-18/19 lo midió sin querer. Se produjeron **más de cien pasajes a
verificar** entre las tres grabaciones. Comprobar uno cuesta abrir el audio, buscar el minuto y
arrastrar la barra; **no comprobarlo cuesta cero**. Y cuando se comprueba, **no queda rastro**:
tres semanas después nadie sabe qué se oyó ni qué se dio por bueno.

> El problema no es que la profesional no quiera comprobar. Es que **el sistema hace más barato
> no hacerlo, y luego olvida que no se hizo.**

## Decision

### 1. Toda marca de tiempo es reproducible con un clic

En la superficie de trabajo, una marca de tiempo **no es texto: es un control**. Un clic
reproduce ese punto de la grabación. Sin buscar, sin arrastrar, sin salir de la página.

**Ese es el mecanismo central de este ADR.** Todo lo demás se apoya en que comprobar cueste un
clic en vez de un minuto.

### 2. Copiar arrastra la procedencia

El botón de copiar entrega **la frase con su localizador y su marca de material derivado**.

> «que es como la figura que creo que la que se quiere utilizar en este caso»
> — Transcripción automática, Audio 2, 00:04:14. Material derivado, no cotejado con la grabación.

**Por qué el localizador va por defecto:** una cita pegada en un escrito **necesita** su
coordenada; quitarla es un acto, ponerla no debería serlo. Se ofrece también copiar sin
procedencia, **y esa es la opción que cuesta un clic más**.

Y cuando el fragmento está marcado como comprobado, **la marca lo dice**, con su fecha.

### 3. Cuatro estados, y los marca ella

| Estado | Qué significa | Quién lo pone |
|---|---|---|
| **Sin comprobar** | Nadie ha oído ni mirado el original. **Es el estado inicial de todo** | El sistema |
| **Oído** | Ella fue al original | Ella |
| **Confirmado** | Ella fue al original y el texto corresponde | Ella |
| **Corregido** | Ella fue al original y el texto **no** corresponde; deja lo que sí dice | Ella |

### 4. El estado NO es prueba de nada, y la salida lo dice

**Es la decisión epistémica de este ADR y la que más importa.**

«Confirmado» significa **«ella afirma haber ido al original y haberlo dado por bueno»**. No
significa que sea correcto, no lo verifica ningún sistema y **no sube el estado epistémico de
nada** (`ADR-003`). Es memoria de trabajo de una persona, con su fecha.

**Prohibido** presentar un fragmento como fiable por estar marcado como confirmado, igual que
`ADR-017` §3 prohíbe presentarlo como fiable por su confianza alta. **Es el mismo error con otro
disfraz, y este es más creíble porque lo firma un humano.**

### 5. Una corrección es una anotación, nunca una edición

Cuando ella corrige, **el texto derivado no se toca**. `ADR-017` §7 es explícito: la transcripción
cruda es inmutable y es la que vale.

La corrección se guarda como **anotación anclada al fragmento**, y es la primera cosa de toda
la cadena con **procedencia humana** (`HUMAN_DECISION`): todo lo demás son derivaciones de
máquina. Eso la hace **más valiosa que el texto que corrige**, y por eso no puede vivir solo en
un navegador.

Para el anclaje se adopta el modelo ya verificado en la revisión v0.1.1 —**W3C Web Annotation,
Recomendación de 2017**—, en vez de inventar un formato propio.

### 6. Dónde vive el estado: en el navegador, y exportable

- **Por defecto** el estado vive en el almacenamiento local del navegador, ligado a la huella del
  documento. Cero fricción, cero configuración, cero red.
- **Un botón lo exporta** a un archivo pequeño junto al caso, y otro lo vuelve a cargar.
- **La exportación es lo que convierte memoria privada en material del caso**, y es un acto
  deliberado de ella. Mientras no exporte, es suya y no existe para nadie más.

**Y hay que decirlo sin adornos:** el almacenamiento del navegador **se puede perder** —al limpiar
datos, al cambiar de navegador, al mover el archivo—. Si el estado importa, **se exporta**. La
página lo advierte cuando hay trabajo sin exportar.

### 7. El estado no viaja con la página

Enviada a un colega, la página llega **sin estado** — que es lo correcto: lo que ella comprobó es
afirmación suya, no del archivo. Si quiere enviarlo, envía también el archivo de estado, **y
entonces llega con su nombre y su fecha**, no como un hecho anónimo.

### 8. Lo mismo vale para lo que no es audio

El mecanismo no es del audio: es de **cualquier cosa que el arnés marca como dudosa**. Una cifra
de `ADR-016` que hay que mirar en la fotografía, un aviso de glosario de `ADR-019`, un hallazgo
de `revision-de-rigor`. **Un clic lleva al original que corresponda**, y el estado es el mismo.

## Invariantes derivados

1. **Todo fragmento marcado como dudoso ofrece un camino de un clic hacia su original.**
2. **Copiar entrega por defecto el localizador y la marca de material derivado.**
3. **El estado inicial de todo es «sin comprobar».** Nada nace verificado.
4. **Ningún estado puesto por una persona sube el estado epistémico de nada**, y la salida lo declara.
5. **Ninguna corrección modifica el derivado.** Se guarda como anotación anclada, con su autora y su fecha.
6. **El estado no se afirma como dato del caso hasta que ella lo exporta.**
7. **La página avisa cuando hay trabajo sin exportar** y declara que el almacenamiento del navegador puede perderse.
8. **Si no hay original disponible** —falta el audio, falta la imagen—, no se ofrece marcar «oído»: se dice que no se puede comprobar.

## Consecuencias positivas

- Convierte tres invariantes declarativos en comportamiento por defecto.
- Hace **visible lo que falta por comprobar**, que hoy es invisible.
- Produce la primera capa de **procedencia humana** del sistema, que es exactamente lo que el
  modelo epistémico necesita y hoy no tiene de dónde sacar.
- El invariante 2 convierte el atajo peligroso —copiar y pegar— en el camino correcto.
- Sirve igual para audio, imagen y hallazgos: un solo mecanismo para las tres fronteras.

## Consecuencias negativas

- **Un estado firmado por un humano se cree más que una confianza de máquina.** La decisión 4 lo
  prohíbe y **la prohibición es débil**, exactamente como la de `ADR-014` §3.
- **El estado se puede perder.** Es el precio de no montar base de datos ni servidor, y hay que
  decirlo cada vez.
- **Aparece estado en un entregable**, que hasta ahora no tenía ninguno. En cuanto se exporta,
  entra en el modelo canónico y le aplican `ADR-005` y `ADR-008` — **con lo que este ADR toca el
  borde del Core y hay que vigilar que no lo cruce sin decisión**.
- **Marcar puede volverse un trámite**: ciento y pico de casillas cansan, y una casilla marcada
  por cansancio es peor que ninguna.
- Añade complejidad real a la página: reproductor, estado, exportación, anotaciones.

## Alternativas consideradas

### (a) Dejarlo a la disciplina
Es el estado actual. Los tres ADR anteriores ya declararon que no funciona.

### (b) Bloquear la copia de lo no comprobado
Descartada: la llevaría a copiar del `.docx`, donde no hay control ninguno. **Un control que se
puede esquivar por un camino peor es un control que empeora el sistema.**

### (c) Guardar el estado siempre en la carpeta del caso
Más robusto y obliga a escribir en disco desde el navegador, lo que exige servidor o permisos
especiales — contra `ADR-020` §3. **La exportación deliberada consigue casi lo mismo** y además
hace explícito el paso de memoria privada a material del caso.

### (d) Permitir editar el texto directamente
Descartada por `ADR-017` §7: la cruda es inmutable. La anotación consigue el valor sin el daño.

### (e) Marcar automáticamente como comprobado al reproducir
**Descartada, y conviene decir por qué:** reproducir no es oír, y oír no es comprobar. Un
automatismo así produciría comprobaciones falsas con apariencia de trabajo hecho — el peor
resultado posible de este ADR.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| «Confirmado» se lee como «verificado por el sistema» | Invariante 4; la marca lleva **quién** y **cuándo**, no solo el estado |
| Se marca por cansancio | Ninguna: es un riesgo humano. Se acota mostrando **cuántos** quedan y no premiando el cero |
| El estado se pierde y se rehace el trabajo | Aviso de trabajo sin exportar; exportación en un clic |
| La anotación humana se pierde con el navegador | Es lo más valioso del sistema: **hay que exportarla**, y la página insiste |
| El estado exportado entra al caso sin autorización | Invariante 6; y en cuanto es dato del caso, `ADR-008` |
| **El almacenamiento local no funciona en archivos abiertos desde disco** | Ver Validación nº 1. **Si falla, el modo por defecto pasa a exportación manual** |

## Validación / pruebas necesarias

1. **BLOQUEANTE — almacenamiento local en `file://`.** Los navegadores tratan los archivos
   abiertos desde disco como origen opaco, y el almacenamiento local **puede estar bloqueado o
   compartido entre archivos distintos**. Hay que comprobarlo en el navegador real de ella, con
   dos páginas de casos distintos abiertas. **Si falla o se mezcla, la decisión 6 cambia.**
2. **Prueba de reproducción:** elegir diez marcas de tiempo al azar y comprobar que el audio suena
   donde dice. Es además la prueba de deriva que `ADR-017` dejó pendiente.
3. **Prueba del pegado:** copiar un fragmento y pegarlo en Word. Comprobar que llega el
   localizador y la marca de derivado, y que se ve.
4. **Prueba con la usuaria:** darle cincuenta pasajes y medir cuántos comprueba, cuánto tarda y
   **si entiende que «confirmado» es afirmación suya y no del sistema**. La decisión 4 se sostiene
   o se cae aquí.
5. **Prueba de pérdida:** marcar veinte, limpiar los datos del navegador y comprobar que la página
   lo detecta y lo dice en vez de mostrar todo como sin comprobar sin explicación.

## Preguntas pendientes

1. **¿El estado exportado es dato del caso o documento de trabajo?** Si es dato del caso, entra en
   el modelo canónico y deja de ser un detalle de interfaz. **Los dueños ya señalaron que esto se
   discute con la abogada.**
2. **¿Qué exige la ley colombiana aplicable** sobre dejar constancia de quién comprobó qué y
   cuándo, y sobre conservarlo? Aquí solo se garantizan propiedades técnicas.
3. ¿La anotación de corrección debe llevar firma o basta el nombre y la fecha?
4. ¿Qué pasa cuando el Markdown se regenera y las anotaciones estaban ancladas al anterior?
   `ADR-011` §8 dice que regenerar produce versión nueva; **las anotaciones tendrían que migrar o
   declararse huérfanas**, y no está decidido.

## Relaciones con otros ADRs

- **ADR-020**: este ADR define el comportamiento de esa superficie. Sin ella no existe.
- **ADR-017** inv. 1, **ADR-016**, **ADR-014** §3: los tres declararon mitigaciones débiles; este
  ADR es el intento de hacerlas fuertes.
- **ADR-003** (modelo epistémico): la decisión 4 lo aplica; la 5 produce el primer
  `provenance_kind = HUMAN_DECISION` real del sistema.
- **ADR-005** (autoridad humana) y **ADR-008** (propuesta y autorización): se activan en cuanto el
  estado se exporta como dato del caso.
- **ADR-011** §8: las anotaciones frente a la regeneración son una pregunta abierta suya.
- **ADR-019**: los avisos de glosario son uno de los tipos de marca que este mecanismo sirve.
