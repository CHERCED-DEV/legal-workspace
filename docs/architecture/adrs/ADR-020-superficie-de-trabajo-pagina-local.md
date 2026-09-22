# ADR-020 — La superficie de trabajo: una tercera capa, local y autocontenida

## Estado

**CANDIDATO** — propuesto el 2026-09-19. **Extiende `ADR-014`**, no lo sustituye.
No se implementa hasta autorización explícita de los dueños.

## Contexto

`ADR-014` fijó dos capas de salida y dejó **dos consecuencias negativas escritas y sin resolver**:

> «**Duplicación real:** dos artefactos por salida, que pueden divergir. El invariante 6 lo acota; no lo elimina.»
>
> «Un `.docx` bien maquetado **se lee como más terminado que un `.md`** […] El encabezado obligatorio es la única mitigación, **y es débil**.»

`ADR-017` dejó otra, del mismo tipo:

> «El invariante 1 es **difícil de hacer cumplir**: nada impide técnicamente citar un segmento sin haberlo escuchado. Depende de la disciplina de cada salida.»

El pase real del 2026-09-18/19 puso número a esa última. Se transcribieron **56 min 52 s** de reunión y se produjo una lista de pasajes a verificar. **Comprobar uno cuesta hoy: abrir el archivo de audio, buscar el minuto, arrastrar la barra.** Es más caro que no comprobarlo. Un invariante cuyo cumplimiento es más caro que su incumplimiento **no es un invariante: es una aspiración**.

**El problema que este ADR ataca no es estético.** Es que las tres decisiones anteriores dependen de la disciplina de una persona cansada un martes por la tarde.

## Decision

### 1. Se añade una tercera capa, con destinatario propio

| Capa | Formato | Para quién | Para qué |
|---|---|---|---|
| **Trabajo del sistema** | `.md` | El sistema, la auditoría, la pasada siguiente | Es **la fuente**. De aquí salen las otras dos |
| **Entrega externa** | `.docx` | Fuera del despacho | Va al juzgado, al cliente, se firma, se imprime |
| **Superficie de trabajo** | `.html` | Ella, trabajando | Leer, comprobar, decidir, marcar |

**El `.docx` no se toca.** `ADR-014` decidió que el entregable externo es Word y esa decisión sigue entera. Lo que no existía era una superficie para **trabajar**, que es una tarea distinta de entregar.

### 2. Nada se redacta en HTML. La página es siempre derivada del Markdown

**Es la respuesta a la duplicación que `ADR-014` no pudo cerrar.** Tres artefactos divergen más que dos — **salvo que dos de ellos sean generados y ninguno editable**. La página se regenera; no se corrige.

**Prohibido** editar un `.html` de salida a mano. Si algo está mal en la página, está mal en el Markdown.

### 3. Cero red. Ni una petición

Ni tipografías remotas, ni bibliotecas de CDN, ni iconos, ni analítica, ni comprobación de versión. **Una página que pide algo a un servidor cuenta lo que está leyendo.** Aplicación directa de `ADR-001` y de `ADR-017` §6.

### 4. Autocontenida, con una sola fuente de estilo

El CSS y el JavaScript viven **en un único lugar del repositorio** y el generador los **inyecta** en cada página. El código fuente no se duplica; la salida sí, y es desechable.

**Consecuencia buscada:** la página funciona sola. Se puede mover, copiar a una memoria o enviar a un colega y **sigue funcionando sin la carpeta del caso**. Coste: del orden de 80 KB por archivo.

### 5. El audio va por ruta relativa, y su ausencia se declara

La página no incrusta la grabación por defecto: la referencia junto a ella. **Si el audio no está, la página lo dice y desactiva la reproducción** — no finge poder comprobar lo que no puede.

**Por qué así y no incrustado:** incrustar 27 MB de audio produce una página de ~36 MB que ningún correo acepta y que carga lenta. La página sin audio **sigue siendo útil** —texto, marcas, avisos, estado— y **honesta**, porque declara qué perdió.

### 6. La incertidumbre es estructural, no un bloque al principio

`ADR-014` §3 obliga al encabezado de propuesta y admite que **es una mitigación débil**. En una página bien diseñada el problema es peor: **el diseño aumenta la credibilidad percibida sin aumentar la verdad.**

Por eso el encabezado se mantiene **y no basta**:

- Lo no comprobado **se ve no comprobado en todo momento**, no solo arriba.
- Lo comprobado oyendo **se ve distinto** de lo que nadie ha oído.
- Un dato marcado por el control automático **conserva su marca** aunque se desplace, se copie o se imprima.

**Regla de diseño que se deriva:** si al quitar los colores y los iconos la página deja de distinguir lo verificado de lo dudoso, el diseño está mal.

### 7. La página no es citable

La coordenada de cita sigue siendo la del original —el documento y su página, la grabación y su minuto—. **La página es una vista, y una vista nunca es fuente.** Mismo estatuto que `ADR-014` §6 dio al PDF consolidado y que `ADR-017` §7 dio al refinado.

### 8. Alcance: esto no espera al Core

Como en `ADR-014` §8: un generador y una plantilla. No depende del Core, ni del MCP, ni de un conector.

## Invariantes derivados

1. **Ninguna página de trabajo se redacta a mano.** Toda página es derivada del Markdown y regenerable.
2. **Ninguna página hace una petición de red**, por ningún motivo.
3. **La página no sustituye al `.docx`** como entregable externo, ni al `.md` como capa de trabajo del sistema.
4. **La página nunca es la fuente de una cita.**
5. **Si falta el audio, la página lo declara** y no ofrece una comprobación que no puede hacer.
6. **Lo no verificado se ve no verificado en toda la página**, no solo en el encabezado.
7. **Nada se afirma en la página que no esté en su Markdown de origen.**

## Consecuencias positivas

- Convierte la comprobación en el camino barato, que es lo único que puede hacer exigible `ADR-017` invariante 1.
- **Cierra la duplicación de `ADR-014`** por construcción: tres artefactos, un solo original editable.
- Mejora la mitigación que `ADR-014` declaró débil, porque una página puede mostrar estado y un papel no.
- No añade dependencia de servidor, puerto ni proceso: se abre con doble clic.

## Consecuencias negativas

- **Tercer artefacto que mantener.** Un generador más, una plantilla más, y una forma más de que algo se vea mal.
- **Una página bonita se cree más.** Es el riesgo de `ADR-014` amplificado, y la decisión 6 es una mitigación **mejor que un encabezado, no una garantía**.
- **Se renuncia a bibliotecas de terceros.** Habrá que sostenerlo cada vez que alguien proponga un framework.
- **El HTML es ejecutable.** Un `.docx` se lee; una página corre JavaScript. Abrir material de un tercero en el navegador **es una superficie de ataque que el Word no tenía** — ver Riesgos.
- **Duplica ~80 KB por archivo.** Irrelevante en disco, no en revisión: hay que comprobar que la plantilla inyectada es la misma en todas.

## Alternativas consideradas

### (a) Artifact publicado en la nube
**Descartada por frontera de confianza.** Enviaría material del caso —y en las grabaciones, voces de terceros que no autorizaron nada— a un servidor. Contra `ADR-001` y `ADR-017` §6. Es la opción más cómoda de construir y la única inaceptable.

### (b) Servidor local
Descartada por coste de uso: obliga a arrancar un proceso y recordar un puerto. **La usuaria abre archivos, no lanza servicios** — el mismo dato que motivó `ADR-014`.

### (c) Solo Word, mejorando la maquetación
Es el estado actual. No resuelve nada de lo que este ADR ataca: un documento no reproduce un minuto de audio ni recuerda qué se comprobó.

### (d) CSS y JS en archivos compartidos junto a la carpeta del caso
Más limpio de mantener y **rompe el requisito de que la página viaje sola**: enviada a un colega, llegaría sin estilo y sin funciones. Se prefiere duplicar la salida y mantener una sola fuente.

### (e) Incrustar el audio siempre
Descartada como comportamiento por defecto por tamaño. **Se deja como opción explícita** para el caso en que realmente haga falta un archivo único.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| La página se acaba citando como si fuera fuente | Invariante 4, y la propia página declara su coordenada de origen en cada bloque |
| El diseño hace creíble lo dudoso | Decisión 6; y la prueba de que al quitar color se siguen distinguiendo |
| Alguien edita el HTML a mano y diverge del `.md` | Invariante 1; el generador sobrescribe sin preguntar y la página lleva la huella de su Markdown |
| **Abrir una página de procedencia desconocida ejecuta su JavaScript** | La página la genera el arnés, no llega de fuera. **Regla: no se abre en el navegador una página HTML recibida de un tercero como material del caso** — ese material se trata como documento, no como programa |
| El audio no acompaña a la página y ella cree haber comprobado | Invariante 5: sin audio, la reproducción se desactiva y se dice |
| La plantilla cambia y las páginas viejas quedan distintas | Cada página lleva la versión de la plantilla con la que se generó (`ADR-011` §7) |

## Validación / pruebas necesarias

1. **Prueba de red cero:** abrir la página con el equipo desconectado y con el registro de red del navegador abierto. **Cero peticiones.** Si hay una, el ADR está incumplido.
2. **Prueba del viaje:** copiar solo el `.html` a otra carpeta y otra máquina. Debe abrir, verse igual y declarar que no tiene el audio.
3. **Prueba de la vista honesta:** imprimir la página en blanco y negro y comprobar que **sigue distinguiéndose** lo verificado de lo dudoso.
4. **Prueba de no divergencia:** modificar el `.md`, regenerar, y comprobar que la página cambia y que no existe ningún camino para el cambio inverso.
5. **Prueba con la usuaria real**, que es la única que dice si esto sirve: darle una lista de pasajes a verificar en Word y otra en página, y medir **cuántos comprueba en cada una**. Es la hipótesis central de este ADR y **hoy no está medida**.

## Preguntas pendientes

1. **¿Qué exige la ley colombiana aplicable sobre el tratamiento de este material?** Este ADR garantiza propiedades técnicas —cero red, local, original intacto—. **Si eso satisface el estándar legal de confidencialidad y de datos personales no lo decide este documento ni quien lo escribe.** Lo decide la abogada, y hasta entonces queda abierto.
2. **¿La página puede contener datos personales de terceros —voces, nombres, documentos de identidad— y salir del despacho hacia un colega?** Compartir es un requisito aceptado; **el régimen de ese envío no está resuelto**.
3. ¿El generador lee solo el Markdown, o también el `datos/*.json` que producen algunos métodos? El reproductor necesita tiempos que el Markdown no lleva.
4. ¿Qué pasa con las páginas de una versión anterior de la plantilla cuando la plantilla cambia? ¿Se regeneran, o se conservan como estaban por `ADR-011` §8?

## Relaciones con otros ADRs

- **ADR-014** (forma de entrega): este ADR lo **extiende** con una tercera capa y **ataca dos de sus consecuencias negativas declaradas**. No modifica ninguna de sus decisiones.
- **ADR-001** (frontera de confianza) y **ADR-017** §6: fundan la decisión 3.
- **ADR-017** (transcripción): la decisión 5 y `ADR-022` existen para hacer exigible su invariante 1.
- **ADR-011** §7 y §8: la página es derivada, lleva su receta y su regeneración no borra la anterior.
- **ADR-019**: la corrección de anclaje que allí se propone se ve mejor en una página que en un documento.
