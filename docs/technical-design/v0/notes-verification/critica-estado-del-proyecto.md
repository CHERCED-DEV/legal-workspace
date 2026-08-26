# Crítica del documento de estado

**Fecha:** 2026-08-26. **Auditado:** `docs/ESTADO-DEL-PROYECTO.md` contra el árbol real.
**Estado: gravedad 1 y 3.1 aplicadas al documento; el resto SIN APLICAR.**

---

## Crítica del documento de estado

Ruta auditada: `C:/Users/HITMA/Desktop/legal-workspace/docs/ESTADO-DEL-PROYECTO.md`
Verificado contra el árbol real en HEAD (`6b6a86e`), que es el commit que el propio documento declara haber leído. La mayor parte del documento resiste: verifiqué uno por uno los conteos del corpus (20 workflows, 6 dossiers de práctica, 18 fichas, 7 mapas), las 29 filas y el `COVERAGE_GAPS_PRESENT` de `06-colombian-law-coverage-ledger.md`, las colisiones W12/W16/W18 con `workflows/12|16|18`, los 26 IDs normativos, las 4 providencias individualizadas entre 10 filas `J-*`, el control negativo `J-CC-T200-2026`, `legal_reference_count = 36`, la densidad normativa de los seis dossiers de práctica, los 13 campos y 5 veredictos de `workflows/20`, el choque de `unsupported_fact_rate` y la regla `b_` del baseline, y la contradicción de `family.md` contra `family-protection-supports.md`. Nada de eso está inventado. Los fallos están en otra parte.

---

## GRAVEDAD 1 — El documento omite que el producto no existe todavía como producto

**El plugin no es instalable hoy por nadie, y el documento afirma lo contrario en su primera línea.**

`§0.1` dice, con etiqueta **HECHO VERIFICADO**: *"instalables como plugin porque el repositorio ya es marketplace de Cowork"*. Comprobado en la máquina:

```
$ git remote -v
(vacío)
```

Y el propio `plugins/despacho/README.md` §3 lo dice con todas las letras: *"el repositorio (…) **no tiene ningún remoto configurado** (`git remote -v` no devuelve nada) (…) **hoy no hay nada publicado** (…) no existe URL que ella pueda añadir"*. Su §9 lo coloca como **la primera fila** de la tabla de bloqueos: *"El repositorio no está en GitHub (…) **Ahora.** Sin esto no hay instalación posible."*

El documento de estado no lo menciona **en ninguna parte**: ni en §0, ni en la tabla de §1.1, ni entre las diez entradas de §5, ni en la tabla de §6 ("Lo que está bloqueado"). §6 roza el tema al preguntar si un repo privado sirve como marketplace, lo que da por supuesto que hay repositorio. La consecuencia es que `§5 entrada 1` promete "poder entregarle el producto" e "imprimir la guía" cuando no hay nada que instalar.

**Corrección concreta.** Añadir una **entrada 0** a §5, delante de todo: *decidir repo dedicado o este mismo, decidir público o privado (con el invariante de "ningún material de cliente en ninguna rama ni punto del historial" como precondición), crear el remoto y hacer el primer push*. Y corregir §0.1: el marketplace **está declarado**, no publicado. La frase correcta es "empaquetados como plugin y declarados en `.claude-plugin/marketplace.json`; sin publicar".

---

## GRAVEDAD 2 — Afirmaciones sin respaldo en ningún archivo

**2.1 · "seis campos" del techo de subida a claude.ai (§4, último bloque).**
El documento afirma: *"`version`, campo que no admite la vía de subida de ZIP a claude.ai (techo de 200 caracteres, seis campos)"*. En `docs/research/capacidades-cowork-y-capa-gratuita.md`:
- línea 306: el techo de 200 caracteres es de **la `description`**, no un límite de número de campos;
- línea 316: *"**Seis pasos**: empaquetar la carpeta como ZIP → Customize > Skills → …"* — son los seis **pasos del procedimiento de subida**, no seis campos de esquema;
- línea 581: del límite de tamaño del ZIP, *"el error existe (…) **la cifra no**"*.

No hay una sola línea en el repo que diga que la vía ZIP rechace un frontmatter con `version`. El "seis campos" nace de leer "seis pasos" como si fuera un esquema. **Corrección:** reescribir el acoplamiento como lo que sí está respaldado — *las seis `description` miden entre 435 y 653 caracteres (medidas: fact-builder 435, estado-del-caso 489, inventario 518, revisar-documento 536, redactar-escrito 576, cronologia 653) y la vía ZIP a claude.ai las trunca a 200; el efecto de `version` por esa vía es **POR VERIFICAR**, no un hecho*. De paso: el "~600 caracteres" del documento también está inflado; tres de las seis están por debajo de 540.

**2.2 · El hecho (a) se presenta como VERIFICADO cuando su fuente lo clasifica NOT FOUND (§4).**
§4 abre: *"Tres hechos de plataforma, verificados con cita literal y refutación adversarial (…) **HECHO VERIFICADO los tres**"*, y (a) es *"No existe deny por ruta en Cowork para un usuario individual"*. La fila fuente (línea 147 del inventario) está rotulada **`NOT FOUND`**: lo verificado es la cita *"Unrestricted. Users can attach any folder…"*; la inexistencia del deny es una **inferencia desde la ausencia de documentación**. En un proyecto cuya regla suprema es la veracidad y que etiqueta `NOT FOUND` justo para no hacer esto, ascender un `NOT FOUND` a `HECHO VERIFICADO` es el error que más caro cuesta, porque de (a) cuelgan tres conclusiones de §4 (la caída del invariante 10 de ADR-012, *"ese principal ya existe"* y la enmienda 1 de ADR-002).
**Corrección:** partir (a) en dos — *HECHO VERIFICADO: el material que se abre se procesa en servidores de Anthropic (líneas 47 y 479, dos citas literales)* / *NOT FOUND: no se localizó control de denegación por ruta para cuenta individual; el modo solo-lectura y la lista blanca solo se documentan bajo administrador*. Las conclusiones que dependen de la segunda quedan como RIESGO, no como consecuencia verificada.

**2.3 · "52 de 876 líneas" (§0.9).**
No pude reproducir el denominador con ningún recorte del repo: `practice-areas/` son 567 líneas (488 sin el dossier huérfano), `legal-dependency-maps/` 147, `source-catalog/` 188, la raíz 717, `workflows/` 1765. Ninguna suma da 876, y "876" no aparece en ningún archivo salvo el propio documento de estado. El numerador sí es congruente con lo que se cuenta a mano en `practice-areas/` (26 líneas con norma concreta por mi conteo; las cifras por archivo del §2.2 —2, 2, 3, 4, 5, 6— sí las reproduje casi exactamente). **Corrección:** decir qué conjunto de archivos es "el dominio entero" y recomputar, o bajar la afirmación a lo defendible: *"seis dossiers de práctica, ~81 líneas cada uno, con entre 2 y 6 menciones de norma concreta y ninguna transcripción de artículo"*, que ya prueba el punto y es verificable en un `grep`.

---

## GRAVEDAD 3 — Optimismo

**3.1 · "Funciona hoy" y "los seis se ejecutan hoy" (§0.1–§0.3, §1.1) no es una observación: es una inferencia.**
La columna "Estado real" de §1.1 dice "Corre" seis veces. Nadie ha corrido ninguno: no hay remoto, no hay instalación, H-10 (¿`/cronologia` o `/despacho:cronologia`?) sigue POR VERIFICAR por decisión del propio documento, y §0.10 declara que no existe un solo dato sobre el trabajo real. Lo que está verificado es que los seis SKILL.md **no declaran dependencias externas**, que es otra cosa. **Corrección:** cambiar el encabezado de columna de "Estado real" a "Dependencias externas declaradas", y sustituir "Corre" por "Sin dependencia externa; **no ejecutado nunca**". Es el mismo rigor que el documento exige a los demás.

**3.2 · §0.3 se contradice con §1.2 en la misma página.**
§0.3 celebra que *"la prohibición de calcular plazos está mejor escrita en los seis `SKILL.md` que en los veinte dossiers"*, y §1.2 registra H-02 como VIVO: `cronologia/SKILL.md` línea 143 manda declarar el vacío *"con sus dos extremos y **su duración en días**"*, la línea 147 pone `(84 días)` en la columna **Bien**, y la línea 223 lo fija en la plantilla (`«N» días`). Verificado. **Corrección:** acotar §0.3 — el producto supera al corpus en las reglas **anti-inferencia** y en el **registro de descartes**; en cálculo con fechas el producto tiene una fuga que el corpus no tiene, aunque el corpus traza mal la frontera.

**3.3 · "El `README.md` del dueño sí lo dice, con rigor ejemplar" (§0.5) es demasiado generoso, y por eso la entrada 1 del §5 queda incompleta.**
El README §6 (líneas 168-200) sí trae las dos citas literales. Pero las enmarca así: *"Esto hoy **no bloquea nada**"*, *"**Por qué hoy da igual.** Despacho es solo texto"*, y difiere la comprobación a *"antes de añadir el servidor propio (**no antes de instalar el plugin**)"*. Es decir: el README lee el hecho como problema de **arquitectura del Core**, nunca como problema de **secreto profesional** — exactamente el error que el propio §6 del documento de estado diagnostica ("declarada pendiente en tres sitios como si fuera **prospectiva**, y el hecho (a) la hizo **retroactiva**"). El documento premia como ejemplar el archivo que comete el error que denuncia.
**Corrección:** §5 entrada 1 debe añadir un punto (iv): *corregir el §6 del README del dueño — quitar "por qué hoy da igual" y "no antes de instalar el plugin", porque el confinamiento del material de clienta no depende de que exista Core*.

**3.4 · "tres afirmaciones falsas" en la guía (§0.5 y §5 entrada 1) son al menos cuatro.**
Verificadas en `GUIA-PARA-LA-ABOGADA.md`: forma corta de los comandos (§1, contra README §1 POR COMPROBAR); *"nunca sobrescribe un archivo que ya está en `2-Borradores`"* (línea 298, contra `inventario-de-anexos/SKILL.md` §1, que no tiene la regla); el choque `sitúa` (línea 277) contra `RESPALDA` (línea 152); **y la promesa anti-inyección de la línea 283**, que solo cumple 1 de 6. El documento la cuenta aparte porque la corrige en la entrada 2, pero al lector de §0 le da un número más bajo del real. **Corrección:** decir cuatro, y enumerarlas.

**3.5 · §2.1 sobrevende `workflows/20` como "única pieza convertible en `SKILL.md` sin inventarle la forma".**
La forma está (13 campos, 5 veredictos: verificado). El **idioma** no: los 13 campos son `finding_id`, `attack`, `residual_risk`, `support_status`…, y los veredictos son `ROBUST`, `DEFENSIBLE_WITH_RISKS`, `MATERIAL_WEAKNESSES`, `HIGH_RISK`, `INSUFFICIENT_BASIS`. Es la clase exacta de jerga que H-08 prohíbe que llegue a su pantalla. El propio §7.7 lo reconoce ("traducir cinco familias de etiquetas en mayúsculas"), pero §2.1 vende coste cero. **Corrección:** "convertible sin inventarle la estructura; **la traducción del vocabulario es trabajo aparte y es condición**".

---

## GRAVEDAD 4 — Omisiones frente a `critica-arnes-despacho.md`

**4.1 · H-14 está descrito por completo en la crítica y el documento dice que no lo recibió.**
§1.2 escribe: *"H-14 y el segundo hueco de H-15 no vienen descritos en el material que recibí, así que no los describo"*. H-14 ocupa las líneas 177-185 del archivo que el documento cita como fuente. Y está **vivo y verificado** contra los `description` reales: `fact-builder` dice *"construir, extraer u **ordenar los hechos**"* y `cronologia` dice *"**ordenar los hechos** en el tiempo"*; `estado-del-caso` dice *"**inventariar la carpeta**"* e `inventario-de-anexos` dice *"armar la **lista de anexos**"*. Dos pares que se pisan.
Esto no es un hueco menor: H-14 **socava directamente el §0.1** ("funciona hoy") y la promesa de la guía de que se puede pedir en español, y su corrección son cuatro ediciones de una línea — **más barata que cualquiera de las diez entradas del §5**. **Corrección:** describir H-14 en la tabla, y meterlo en la entrada 3 (que ya toca `fact-builder`) o crear una entrada propia de 15 minutos: quitar *"ordenar los hechos"* de `fact-builder`, quitar *"inventariar la carpeta"* de `estado-del-caso`, y añadir la exclusión cruzada explícita a las cuatro.

**4.2 · H-15.2 ("buscar dentro del material") desaparece.**
§1.3 lista los huecos de capacidad y no lo incluye; §5 entrada 10 escoge H-15.3. La crítica lo describe como *"una pregunta de treinta segundos"* que hoy solo se resuelve con una pasada completa de `fact-builder`. **Corrección:** añadirlo a §1.3 y evaluarlo como candidato en la §7.5, donde compite bien por coste.

**4.3 · La entrada 2 del §5 propagaría la jerga que la entrada 3 va a quitar.**
§5 entrada 2 manda *"Copiar **literalmente** `revisar-documento/SKILL.md` §7"* a los otros cinco. Ese §7 abre con: *"**HECHO VERIFICADO:** el fabricante advierte de este riesgo…"* — etiqueta de epistemología interna del proyecto, sin fuente, dentro de un archivo de producto. La crítica ya lo señala en sus Menores. Copiarlo literalmente lo multiplica por seis, en el mismo documento que hace de H-08 su tercera prioridad. **Corrección:** *"copiar §7 **desde el párrafo 'Un documento externo puede traer…'**, dejando fuera la línea de etiqueta"*.

**4.4 · Ningún "Menor" de la crítica sobrevive al documento.**
Comprobados y vivos: `plugins/despacho/README.md` describe la estructura de carpetas solo como `1-`, `2-`, `3-` (líneas 133-134) y **omite `0-Estado del caso (no editar).txt`**, que la guía sí incluye y que `estado-del-caso` necesita para funcionar; siguen la jurisdicción implícita (radicado, tutela, S.A.S., pesos) y la fatiga de advertencia. **Corrección:** una fila de "menores pendientes" al final de §1.2, aunque sea de tres líneas; hoy la tabla de diecisiete se lee como el inventario completo de la deuda y no lo es.

**4.5 · Imprecisión menor en §1.1.** *"Es el único de los seis **sin sección 'Dónde se escribe'**"*. Literalmente falso: ese título exacto solo lo tiene `inventario-de-anexos` (línea 17); los demás la llaman *"Dónde escribes y dónde no"* (cronologia 181), *"Dónde entra y dónde sale"* (revisar-documento 17), *"Destino: `2-Borradores/`"* (redactar-escrito 189). La sustancia sí se sostiene y es más fuerte dicha como la dijo la crítica: **`fact-builder` es el único de los seis sin una sola mención de `1-Documentos recibidos/`, `2-Borradores/` ni de un nombre de archivo de salida** — comprobado, `grep` devuelve cero.

---

## GRAVEDAD 5 — La priorización del §5

**No, la entrada 1 no es la de mayor valor por esfuerzo bajo el criterio que el propio documento declara.**

§5 dice ordenar por *"valor para ella dividido por esfuerzo"* y añade *"Ninguna entrada depende del Core, del Knowledge Pack ni de una herramienta nueva"*. Eso es cierto y a la vez engañoso: **la entrada 1 es la única de las diez con dos dependencias humanas**, que son más caras que cualquier dependencia técnica.

1. **§5 y §6 se contradicen sobre la misma entrada.** §6 dice de la decisión de confidencialidad: *"Solo los dueños. **Mientras no se tome, no debería presentarse el producto con ninguna afirmación sobre dónde se procesa el material — ni positiva ni omitida.**"* La entrada 1(i) es exactamente escribir una afirmación positiva sobre dónde se procesa el material. O §6 está mal, o la entrada 1(i) está bloqueada y no puede encabezar una lista de ejecución.
2. **La entrada 1(ii) y (iii) requieren agenda con ella**; (iii) depende de (ii). Cuesta 1-2 h *más* el tiempo de calendario de otra persona.
3. **La entrada 2 gana por el criterio declarado**: media hora, cero dependencias, cierra *"la única promesa del producto que puede fallar en silencio con un tercero interesado del otro lado"*, hace verdadera una frase que la guía ya publicó, y llega con su regresión escrita (los cinco fixtures sembrados). Valor alto / esfuerzo mínimo / desbloqueo inmediato: no hay ninguna otra entrada con ese perfil.

**Además hay un error de secuencia dentro de las tres primeras.** La entrada 3 renombra `fact-builder` → `hechos-con-prueba` y el propio documento lo llama *"ventana que se cierra: renombrar después de que ella lo aprenda cuesta el triple"*. Pero va **después** de la entrada 1, cuya parte (ii)-(iii) es sentarse con ella y escribir en la guía la forma real de los comandos. Ejecutado en ese orden, la sesión verifica y le enseña un nombre que la entrada 3 va a cambiar dos horas después, y obliga a repetir la verificación. **El renombre tiene que ir antes de cualquier sesión con ella.**

**Y la entrada 7 está declarada bloqueada en §6** (*"¿Va ella a abrir un `.md` y escribir SÍ al lado de cada ficha…? Solo ella. Si no lo va a hacer, el mecanismo es papel mojado"*) y aparece en la lista de ejecución sin la marca. Medio día de trabajo contra una pregunta sin responder.

**Orden corregido y concreto** (mismo criterio, dependencias explícitas):

| # | Entrada | Coste | Dependencia |
|---|---|---|---|
| **0** | Publicar el repositorio (decidir alcance, crear remoto, primer push) | ½ día + decisión de alcance | Dueño |
| **1** | Bloque anti-inyección en los seis (ex-2), **sin la línea `HECHO VERIFICADO`** | 30 min | ninguna |
| **2** | H-14: desambiguar las cuatro `description` | 15 min | ninguna |
| **3** | Vaciar la plantilla de apartados de `redactar-escrito` (ex-5) | 30 min | ninguna |
| **4** | Sacar la aritmética de fechas y escribir la frontera por operación (ex-4) | 1 h | ninguna |
| **5** | No sobrescribir y no afirmar sin mirar (ex-6) | 30 min | ninguna |
| **6** | Limpiar `fact-builder`: vocabulario, jerga y **renombre** (ex-3) | 1½ h | decisión §7.3 |
| **7** | "Qué comprobar primero" al cierre de las seis salidas (ex-8) | 1 h | ninguna |
| **8** | Verdad sobre el procesamiento + sesión de comprobación en su máquina + corregir README §6 (ex-1) | 1-2 h | **decisión de los dueños (§6) + agenda con ella** |
| **9** | Sincronizar corpus y producto (ex-9) | 1 h | decisión §7.1 |
| **10** | Hoja de hechos revisada (ex-7) | ½ día | **respuesta de ella (§6)** |
| **11** | Séptimo comando (ex-10) | ½ día | decisión §7.5 |

Las entradas 1 a 7 no dependen de nadie y suman menos de cinco horas: hoy están enterradas debajo de dos entradas que no se pueden ejecutar sin terceros. Ese es el fallo de razonamiento del §5 — no confunde valor, confunde **ejecutabilidad con esfuerzo**.

Si de verdad el argumento de que la veracidad manda obliga a poner la entrada 1 primero (es un argumento legítimo y el documento lo hace bien), entonces hay que decirlo así explícitamente y renunciar al rótulo "ordenadas por valor dividido por esfuerzo", porque bajo ese rótulo la entrada 1 no gana.