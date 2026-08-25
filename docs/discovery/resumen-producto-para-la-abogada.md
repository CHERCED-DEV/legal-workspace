# Qué estamos construyendo — resumen para la profesional

**Fecha:** 2026-08-24 · **Estado:** diseño terminado, construcción no iniciada.
**Para qué sirve este documento:** explicar, sin lenguaje técnico, qué es el producto, qué hará y qué no hará, en qué punto estamos y qué necesitamos de usted.

---

## 1. El problema que queremos resolver

Usted ya usa herramientas de inteligencia artificial para redactar, resumir, analizar documentos y preparar escritos. Funcionan, pero tienen cuatro problemas que en materia jurídica son graves:

1. **Pueden inventar** normas, sentencias o citas y presentarlas con total seguridad.
2. **Olvidan.** Cada conversación empieza de cero; lo trabajado ayer se pierde o hay que volver a explicarlo.
3. **Confunden lo alegado con lo probado.** Para un escrito, esa diferencia lo es todo.
4. **No dejan rastro.** Si algo termina en una demanda, no hay forma de volver atrás y ver de dónde salió.

No estamos construyendo un asistente que redacte mejor. Estamos construyendo el **expediente** que hay debajo: un sistema donde cada afirmación tiene origen comprobable, donde el trabajo se conserva entre sesiones, y donde la máquina **no puede** dar por probado lo que usted no ha aprobado.

---

## 2. Cómo va a funcionar, en la práctica

Usted trabaja conversando, como ya lo hace hoy. Lo que cambia está detrás:

**Incorporar material.** Usted entrega una grabación de entrevista, un contrato, un oficio. El sistema guarda el archivo original tal cual llegó y calcula una huella de su contenido. **El original nunca se modifica ni se borra.** Si más adelante ese archivo desaparece de donde estaba (un Drive, un correo), el expediente conserva lo que se incorporó.

**Derivar.** De la grabación se produce una transcripción. La transcripción es una **ayuda**, no la fuente: cuando el sistema cite un pasaje, siempre podrá llevarla al minuto exacto de la grabación original. Los pasajes que no se entendieron bien quedan marcados como dudosos, no maquillados.

**Construir los hechos.** Este es el cuello de botella que usted describió: convertir una historia larga en hechos ordenados con su prueba. El sistema lee la entrevista y los documentos y **propone** hechos candidatos, cada uno con el fragmento exacto que lo respalda o lo contradice. Un mismo hecho puede tener varias pruebas, y una prueba puede servir a varios hechos.

**Revisar y decidir — aquí manda usted.** Los hechos propuestos **no entran al expediente solos**. Usted los revisa uno por uno y decide sobre cada uno por separado: aprobar, rechazar o dejar pendiente. Aprobar el hecho 3 no aprueba el 4. Y si después de su revisión el texto de un hecho cambia, su aprobación anterior **deja de valer** para ese hecho: hay que volver a mirarlo. Esto no es un permiso que se pueda saltar: el sistema está construido para que la máquina no pueda fabricar su aprobación.

**Volver días después.** Abre el caso y el sistema le dice qué cambió desde su última revisión, sin que usted tenga que recordar nada ni conservar la conversación anterior.

**Evidencia que llega tarde.** Si entra un documento nuevo después de un análisis, el sistema **marca ese análisis como desactualizado** y se lo dice. No puede presentárselo como vigente en silencio.

---

## 3. Lo que el sistema nunca hará

Estas no son buenas intenciones: son restricciones construidas en el sistema.

| Nunca | Por qué importa |
|---|---|
| Dar por acreditado un hecho por su cuenta | Solo su decisión profesional puede hacerlo |
| Marcar una norma o sentencia como verificada porque la generó | Es el riesgo más grave del oficio |
| Modificar o borrar un documento original | El original es la base de todo lo demás |
| Usar como prueba algo que no fue incorporado formalmente | Lo que la IA "vio por ahí" puede orientarla, nunca fundamentar |
| Mezclar dos expedientes | — |
| Ocultarle que algo quedó desactualizado o incierto | Podemos ocultarle la ingeniería; **nunca la incertidumbre** |

Sobre lo último: si el sistema no encuentra respaldo para algo, se lo dirá. Si una búsqueda falló, le dirá que falló — que es distinto de decirle que no existe prueba. Esa diferencia está escrita en el diseño y se verifica con pruebas automáticas.

---

## 4. Qué verá usted y qué no

**No** verá: nombres de programas, códigos de error, huellas digitales de archivos, números de versión, jerga de sistemas.

**Sí** verá mensajes como estos, que ya están redactados:

> «Preparé 12 hechos candidatos. Necesito que revise cuáles desea incorporar al caso.»

> «Se incorporó nueva información al expediente desde que se preparó esta propuesta. El trabajo anterior se conserva, pero debe revisarse antes de incorporarlo.»

> «No pude determinar con suficiente claridad este fragmento. Conviene revisar el audio entre 18:42 y 18:57.»

Ese último ejemplo muestra el criterio: el sistema no adivina lo que no oyó bien; le dice dónde escuchar.

---

## 5. En qué punto estamos

**Terminado:** todo el diseño. Diecisiete documentos técnicos y once decisiones de arquitectura formales que definen qué se guarda, qué puede pedir la IA, qué requiere su aprobación, y cómo se demuestra que no puede romperse.

**Terminado también:** un caso de prueba ficticio —inventado, sin datos reales— con entrevista, documentos, contradicciones deliberadas, montos que no cuadran y un documento que llega tarde. Sirve para medir si el sistema hace bien su trabajo antes de que usted le confíe un expediente real.

**No empezado:** la construcción. Es deliberado. No se escribe una línea de programa hasta que el diseño esté cerrado.

**Primera versión:** un solo computador, una sola usuaria, **datos inventados**. No trabajaremos con expedientes reales hasta resolver por escrito la confidencialidad y el secreto profesional.

---

## 6. Lo que necesitamos de usted

Ninguna de estas preguntas detiene el trabajo, pero todas mejoran el resultado:

1. Cuando usted dice que un hecho **«está acreditado»**, ¿se refiere a su juicio profesional sobre lo que quedará probado, o a lo que ya declaró la autoridad? Puede que necesitemos distinguir ambas cosas.
2. ¿Cómo le llegan hoy los documentos y las grabaciones: correo, WhatsApp, USB, escáner, plataforma judicial?
3. ¿Cuánto material maneja por semana, y cuántas horas de audiencia?
4. ¿Qué fuentes jurídicas consulta y por qué medio?
5. ¿Quién más toca los expedientes además de usted?
6. ¿Qué respaldo de la información es viable en su oficina?
7. En el trabajo como autoridad, ¿cuál es el expediente oficial?

---

## 7. Una advertencia honesta

Hay un punto que todavía no podemos garantizar. El producto se apoyaría en una aplicación de escritorio, y verificamos en su documentación oficial que **esa aplicación no permite proteger una carpeta específica**: cuando se le da acceso a una carpeta, alcanza todo su contenido. Nuestro diseño resuelve esto colocando el expediente **fuera** del alcance de la aplicación, de modo que solo nuestro sistema pueda tocarlo.

Falta comprobar en la práctica que esa separación funciona como esperamos. Es una prueba concreta, ya preparada. **Hasta que dé resultado, no vamos a afirmar que el expediente está protegido.** Preferimos decirle esto ahora a prometerle una garantía que todavía no tenemos — que es exactamente el criterio con el que está construido todo el producto.
