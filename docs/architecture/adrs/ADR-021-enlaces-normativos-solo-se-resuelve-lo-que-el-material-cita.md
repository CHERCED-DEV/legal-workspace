# ADR-021 — Enlaces normativos: se resuelve lo que el material cita, y nada más

## Estado

**CANDIDATO** — propuesto el 2026-09-19. No se implementa hasta autorización explícita.
**Depende de una comprobación que nadie ha hecho** (ver Validación nº 1). Si esa comprobación
falla, este ADR no es realizable y la decisión correcta es no enlazar nada.

## Contexto

Se pidió que la superficie de trabajo (`ADR-020`) lleve **hipervínculos a las leyes y artículos
citados**, para no obligar a buscarlos a mano.

**El arnés entero está construido sobre no poner derecho.** `redactar-escrito` «no redacta
fundamentos de derecho, no cita normas ni jurisprudencia, no califica jurídicamente nada»;
`preguntas-de-derecho` existe **solo** para interceptar la pregunta jurídica y explicar por qué
no se responde. Es la frontera más defendida del producto.

> **Un hipervínculo a un artículo es una afirmación de que ese artículo viene al caso.** Puesto
> por el arnés, es derecho puesto por el arnés — por la puerta de atrás y sin que nadie lo decida.

Y hay una versión que **no** cruza la frontera, que es la que este ADR decide. La distinción es
fina y es todo el contenido de la decisión:

| Esto es resolver una referencia del material | Esto es poner derecho |
|---|---|
| El expediente dice «decreto 2181» → enlazar **esa mención** | Enlazar el decreto que el arnés considere aplicable |
| Mostrar el identificador **tal como lo escribió el material** | Corregirlo, completarlo o normalizarlo |
| «Ir a la fuente oficial» | «Norma vigente», «norma aplicable», «según el artículo…» |

El material real ya lo exige: en la reunión transcrita el 2026-09-18 se mencionan «decreto 2181»,
«1077», «convenio 3F, 14F» y «sentencias de la Corte Constitucional». **Hoy esa abogada los
busca a mano, uno por uno.**

Existe además material previo: una bibliografía con **26 identificadores normativos verificados
contra Diario Oficial**. **No es del renderizador: es del Knowledge Pack**, que hoy no existe.

## Decision

### 1. Solo se enlaza el identificador que el material cita, literal

El enlace se **ancla sobre el texto tal como aparece** en el documento o en la transcripción.
**No se corrige, no se completa, no se normaliza.** Si el material dice «el 1077» y eso es
ambiguo, se enlaza «el 1077» con su ambigüedad, o **no se enlaza**.

**Prohibido** añadir al entregable una norma que el material no menciona.

### 2. Nunca se afirma vigencia, aplicabilidad ni contenido

El texto visible del enlace es de navegación —«ir a la fuente oficial»— y **nunca** de
calificación. Ninguna salida dice «norma vigente», «norma aplicable», «conforme al artículo» ni
resume lo que la norma establece.

### 3. Fuente oficial, y fecha de consulta declarada

Solo fuentes oficiales del Estado. **Con la fecha en que se comprobó el enlace**, porque un
enlace normativo es material perecedero.

### 4. La trampa de la versión, que es el riesgo mayor de este ADR

Los repositorios oficiales sirven habitualmente el **texto compilado** —con las modificaciones
posteriores ya aplicadas—. **En un caso jurídico lo que suele importar es el texto que regía
cuando ocurrieron los hechos**, que puede ser otro.

> **Un enlace a la versión de hoy sobre hechos de hace cinco años es peor que ningún enlace**,
> porque parece comprobado.

Por eso, toda salida que lleve enlaces normativos **declara, junto a ellos**, que apuntan al
texto que la fuente sirve hoy, que puede no ser el que regía en la fecha de los hechos, y que
**esa comprobación es de la profesional**.

### 5. Si no se puede verificar que el enlace resuelve, no se enlaza

Un enlace roto o equivocado es peor que su ausencia. **En la duda, se muestra el identificador
sin enlace** y se dice que no se pudo resolver.

### 6. El registro de fuentes pertenece al Knowledge Pack, no al renderizador

El renderizador **no sabe derecho y no debe aprenderlo**. Se limita a buscar identificadores en
un registro que le dan hecho. Ese registro —qué fuentes son oficiales por jurisdicción, qué
patrón de identificador se reconoce, cómo se construye la dirección— es **Knowledge Pack**, con
su versión y su jurisdicción.

**Consecuencia de alcance:** mientras no exista Knowledge Pack, **este ADR no se puede
implementar completo**. Lo que sí se puede hacer antes es reconocer y **resaltar** los
identificadores sin enlazarlos, que ya ahorra búsqueda visual sin afirmar nada.

### 7. Seguir un enlace sale del perímetro, y la página lo dice

`ADR-020` §3 exige cero peticiones de red. **Un enlace no las hace: hacerle clic, sí** — y
comunica a un servidor del Estado que alguien consultó esa norma.

No es la página llamando a casa: es un acto deliberado de la usuaria. Pero **tiene que ser
deliberado y saberlo**: los enlaces se marcan visiblemente como salida a internet, se abren en
ventana aparte y se emiten sin referente (`rel="noreferrer noopener"`), para que el sitio de
destino no reciba de dónde se hizo clic.

## Invariantes derivados

1. **Ningún enlace normativo apunta a una norma que el material no cita.**
2. **La cita del material no se corrige, completa ni normaliza** para poder enlazarla.
3. **Ninguna salida afirma vigencia, aplicabilidad ni contenido de una norma.**
4. **Todo enlace normativo declara su fuente y su fecha de consulta.**
5. **Todo bloque con enlaces declara que la versión servida puede no ser la aplicable a los hechos.**
6. **Ante la duda no se enlaza**, y la falta de enlace se declara.
7. **Los enlaces se ven como salida a internet** y no filtran de dónde se hizo clic.
8. **El renderizador no contiene conocimiento jurídico**: lo consulta en un registro versionado.

## Consecuencias positivas

- Ahorra búsqueda manual real sin mover la frontera de cero derecho.
- Hace **visible** lo que el material cita, que hoy se pierde en el cuerpo del texto.
- Obliga a construir el registro de fuentes oficiales —el Knowledge Pack— con un caso de uso
  concreto en vez de en abstracto.
- El invariante 5 pone delante de la profesional un riesgo —la versión aplicable— que hoy nadie
  le recuerda.

## Consecuencias negativas

- **Es la parte más vistosa y la más peligrosa** de `ADR-020`. La tentación de «enlazar también
  lo que claramente aplica» va a aparecer, y es exactamente lo prohibido.
- **Depende de un componente inexistente.** Sin Knowledge Pack solo se puede resaltar, no enlazar.
- **Mantenimiento perpetuo:** los enlaces se pudren y las normas se derogan. Un entregable de hace
  un año puede llevar enlaces que hoy engañan.
- **Introduce una salida del perímetro** que hasta ahora no existía en ningún entregable.
- El invariante 2 producirá enlaces sobre citas mal escritas por el material. **Es deliberado** —
  el material dice lo que dice— y va a parecer un defecto.

## Alternativas consideradas

### (a) Enlazar la norma que el modelo considere aplicable
**Descartada.** Es poner derecho. Rompe la frontera que `preguntas-de-derecho` defiende y que es
el argumento de venta del producto.

### (b) No enlazar nada
Es el estado actual. Defendible y **es el resultado correcto si la Validación nº 1 falla**.
Coste: la profesional sigue buscando a mano lo que el propio expediente ya cita.

### (c) Resaltar sin enlazar
**Se adopta como primera fase.** Reconocer los identificadores y hacerlos visibles no afirma nada
y no depende del Knowledge Pack. Es lo único de este ADR ejecutable hoy.

### (d) Copia local de las normas citadas
Resolvería la pudrición del enlace y la trampa de la versión, y crearía **un derivado jurídico
dentro del caso** que hay que fechar, versionar y defender. Más honesto y mucho más caro.
**Queda abierta** para cuando exista Knowledge Pack.

### (e) Enlazar a un buscador en vez de a la norma
Descartada: traslada el problema a un tercero y entrega resultados que nadie controla.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| El enlace apunta a una versión que no regía en los hechos | Invariante 5, declarado junto a los enlaces y no al pie |
| Se enlaza una norma derogada sin decirlo | Fuente oficial y fecha de consulta; y la comprobación sigue siendo de la profesional |
| El enlace se lee como respaldo jurídico del arnés | Invariantes 1 a 3; el texto del enlace es de navegación, jamás de calificación |
| Alguien añade «solo por comodidad» una norma no citada | Invariante 1, y prueba adversarial nº 3 |
| Los enlaces se pudren en silencio | Fecha de consulta visible; el entregable envejece a la vista |
| El clic revela al Estado qué norma se consulta en qué caso | Marca visible, ventana aparte, sin referente. **No se elimina: se hace consciente** |

## Validación / pruebas necesarias

1. **BLOQUEANTE — ¿resuelven los enlaces profundos?** Comprobar, contra fuentes oficiales
   colombianas, que existe un patrón de dirección **estable y verificable** para al menos: un
   decreto, una ley, un artículo concreto y una sentencia de la Corte Constitucional.
   **Nadie lo ha comprobado.** Si no existe patrón estable, se aplica la alternativa (b).
2. **Prueba de la versión:** tomar una norma modificada después de su expedición y comprobar qué
   texto sirve la fuente oficial. Confirma o refuta la premisa de la decisión 4.
3. **Prueba adversarial:** dar al sistema material que menciona una norma **y otra norma que
   claramente vendría al caso pero el material no menciona**, y comprobar que **solo enlaza la
   primera**.
4. **Prueba de identificador ambiguo:** material que dice «el 1077» sin más. Debe resaltarse sin
   enlace y declararse que no se pudo resolver.

## Preguntas pendientes

1. **¿Qué fuentes acepta la abogada como oficiales**, y con cuál se queda cuando varias sirven la
   misma norma con textos distintos? **No es una pregunta técnica y no la decide quien escribe esto.**
2. **¿Qué exige la ley colombiana aplicable** sobre incorporar referencias normativas a un
   entregable de trabajo? Igual que en `ADR-020`: aquí solo se garantizan propiedades técnicas.
3. ¿El resaltado sin enlace de la alternativa (c) necesita ya un registro mínimo de patrones, o
   basta reconocer formas generales —«decreto NNNN», «ley NNNN de AAAA», «sentencia X-NNN/AA»—?
4. ¿Qué se hace con las referencias a material del propio caso —«el convenio 3F, 14F»— que no son
   normas y no tienen fuente oficial? ¿Se enlazan al documento del expediente?

## Relaciones con otros ADRs

- **ADR-020**: este ADR define un contenido de esa superficie; la decisión 7 es la única excepción
  consciente a su §3.
- **ADR-011** (locators): un enlace normativo es un localizador hacia fuera del caso; se le aplican
  receta, versión y fecha.
- **ADR-003** (modelo epistémico): un enlace no sube el estado de nada.
- **ADR-006** (frontera de incorporación de prueba): una norma enlazada **no queda incorporada** al
  caso por el hecho de enlazarla.
- **`preguntas-de-derecho`**: este ADR es la única forma en que el arnés toca una norma **sin**
  activar esa frontera, y solo porque no afirma nada sobre ella.
