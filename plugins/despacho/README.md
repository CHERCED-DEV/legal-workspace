# Despacho — guía del dueño

Esta guía es para **quien publica e instala el plugin**, no para la abogada que lo usa.
Cubre cuatro cosas: qué trae el plugin, cómo se instala en la máquina de ella, cómo se
publica una actualización, y qué **no** hace todavía.

Las afirmaciones sobre la plataforma van marcadas. **HECHO VERIFICADO** es documentación
oficial contrastada. **POR COMPROBAR** es algo que hay que ver con los propios ojos antes
de darlo por cierto — no está inventado ni está confirmado. **SUPUESTO DECLARADO** es una
decisión tomada sin confirmación, que puede resultar falsa.

---

## 1. Qué es Despacho

Un plugin de Claude que aporta **once métodos de trabajo jurídico**. No es un programa: es
texto. Cada método le dice a Claude cómo hacer una tarea concreta del despacho con un
procedimiento fijo, qué **no** puede hacer nunca dentro de esa tarea, y cómo tiene que
entregar el resultado.

La regla que comparten los once: **todo sale del material del caso, y de dónde sale se
dice**. Ninguno valora prueba, ninguno calcula plazos, ninguno pone derecho. Lo que el
material no da, se marca como faltante en vez de rellenarse.

### Los comandos

| Comando | Qué hace de verdad |
|---|---|
| `/preparar-material` | **Llama a un programa**, no lo hace a mano: descomprime, ordena, copia los originales sin tocarlos, calcula huellas, detecta duplicados, extrae texto de fotografías con instrumentación de cobertura, arma el PDF consolidado y escribe el registro de ingesta. **Con cero fichas de lectura.** No lee el caso: lo monta. |
| `/buscar-en-el-caso` | **Llama a un programa:** dice en qué archivo y en qué renglón aparece un nombre, una cifra o una fecha, sin abrir ni leer nada. Marca los renglones que son basura del OCR. **No cita y no concluye ausencia**: cero resultados no significa que no esté en el papel. |
| `/hechos-con-prueba` | Recorre el material del caso y devuelve **hechos candidatos**, cada uno emparejado con el fragmento concreto que lo apoya, lo contradice o lo sitúa; los que no tienen nada detrás quedan marcados como tales. No valora prueba ni decide estrategia. |
| `/revisar-documento` | Lee **un** documento que llegó (escrito de contraparte, requerimiento, contrato, respuesta) y devuelve en una pasada qué es, qué afirma, qué pide, qué decide, qué referencias de tiempo trae **textualmente** y qué parece exigir actuación. No calcula plazos ni dice si algo está vencido. |
| `/estado-del-caso` | Lee la carpeta del caso y reconstruye **solo con lo que dicen los archivos** qué documentos hay y de qué fecha, qué entró y qué se produjo, cuál es la última actuación que consta y qué quedó a medias o sin respuesta. Lista aparte **las salidas del propio sistema**, con qué comando las produjo y cuáles están revisadas. No pronostica ni valora solidez. **Llama a un programa** para escribir el resumen: reemplaza solo la cabecera y **lo que ella escribió bajo `NOTAS SUYAS` se conserva byte a byte**, sin volver a pasar por el modelo. |
| `/cronologia` | Extrae **todo evento con fecha**, con el documento y la página de donde sale cada una y **el grado de certeza de esa fecha** (documentada, referida, aproximada, deducida, en conflicto); añade los eventos sin fecha situados por anclas, los conflictos sin resolver y los periodos sobre los que el material calla. No cuenta plazos ni decide cuál fecha es la buena. |
| `/inventario-de-anexos` | Produce la **tabla de anexos numerada** lista para pegar en un escrito —qué es cada documento, quién lo produjo, de qué fecha es, a qué afirmación sirve— y, en bloque aparte, **lo que falta**, separado en sus tres clases. No decide qué se aporta. |
| `/inventario-de-bienes` | Recorre el material e inventaría **bienes y deudas**: qué documento respalda cada uno, a nombre de quién figura según ese documento, qué fecha trae y qué valor **transcrito**; más lo que falta y las contradicciones entre documentos. Señala el bien que aparece en un papel de un tercero y **en ninguna lista de las partes**. No decide qué bienes entran, no calcula, no reparte. |
| `/revision-de-rigor` | Pone a prueba **una conclusión, un escrito propio o un expediente entero** con una sola pregunta: qué de esto no se sostiene con el material. Cada hallazgo lleva su localizador, **lo que lo refutaría** y su grado de soporte; y cuando hay dos partes, declara qué buscó en cada una y qué encontró en cada una, incluso donde no encontró nada. No valora prueba ni declara parcialidad. |
| `/redactar-escrito` | A partir de material **que ella ya revisó**, arma un borrador en Word con la parte fáctica redactada, la estructura montada y **cada hueco marcado a la vista**; entrega aparte un segundo archivo con de dónde sale cada frase. No redacta fundamentos de derecho, no cita normas ni jurisprudencia, no califica jurídicamente nada. |
| `preguntas-de-derecho` | **No se teclea: se activa solo.** Intercepta la pregunta que no se responde leyendo la carpeta —*«¿qué dice la ley sobre…?»*, *«¿esto caducó?»*, *«¿qué dijo la Corte?»*— y en vez de contestarla explica por qué no puede y ofrece lo que sí sale del material. Sin él, esa pregunta **no activa ningún comando** y contesta el modelo suelto, sin método y sin la regla de cero derecho. |

**POR COMPROBAR (primera instalación):** que los comandos aparezcan escritos exactamente
así en la caja de mensaje y no con algún prefijo del plugin. Se ve en el primer intento;
si no aparecen, lo primero que hay que revisar es que el plugin esté instalado y activo.

**POR COMPROBAR:** que `/redactar-escrito` consiga producir de verdad un archivo `.docx`
en el entorno de ella. El propio método contempla el fallo (si no puede, escribe el mismo
contenido en texto y lo dice), pero conviene verlo funcionar una vez.

**POR COMPROBAR — con material real de ella, antes de sentarse a trabajar.** Dos capacidades
que los métodos dan por supuestas y que nadie ha visto funcionar aquí. No se comprueban leyendo
documentación: se comprueban abriendo un archivo suyo.

- **Que pueda transcribir o citar el minuto exacto de una grabación.** `/hechos-con-prueba`
  promete citar la entrevista con su minuto (`entrevista, 00:08:12`), y el Ejemplo 2 de la guía
  de ella lo imprime así. Si no puede oír el audio, o puede pero no sitúa el minuto, ese ejemplo
  es falso y media promesa del método se cae: habría que decirle que la entrevista entra
  transcrita por ella, no en audio.
- **Qué hace con un PDF escaneado sin capa de texto.** Es el formato en que llegan la mitad de
  los documentos de un despacho. Si no lo lee, **no hay método que funcione**: los once parten de
  leer el material y citar página. Hay que saber si lo lee, si lo lee mal en silencio, o si avisa
  de que no puede — y las tres respuestas llevan a instrucciones distintas para ella.

---

## 2. Requisito de plan — leer antes de prometer nada

**HECHO VERIFICADO:** *"Plugins are available in Cowork and Code. They aren't used in Chat."*

Es decir: **el plugin no funciona en el Claude de conversación normal**. Si ella abre Claude
y escribe `/cronologia` en un chat corriente, no pasa nada. Tiene que estar en **Cowork**.

**HECHO VERIFICADO:** Cowork exige plan de pago — Pro, 17 USD/mes en facturación anual.

Consecuencia práctica: **antes de instalar nada, ella necesita una cuenta con plan de pago
activo y acceso a Cowork.** No hay camino gratuito. Si esto no está resuelto, el resto de
la guía no se puede ejecutar.

---

## 3. Publicar el repositorio

**HECHO VERIFICADO:** un repositorio de git que contiene paquetes de plugin **es** el
mercado. *"A Git repository that contains plugin packages can serve as a marketplace...
Repositories on GitHub are supported."* No hay que publicar en ningún sitio aparte, ni
registrar el plugin en ningún directorio: el repositorio es el mercado.

Lo que hace que un repositorio sea un mercado es el archivo `.claude-plugin/marketplace.json`
**en la raíz**, que ya existe aquí y declara el plugin `despacho` con su ruta.

### Estado real hoy

**HECHO VERIFICADO (comprobado en esta máquina, 2026-08-25):** el repositorio
`C:\Users\HITMA\Desktop\legal-workspace` **no tiene ningún remoto configurado**
(`git remote -v` no devuelve nada) y la rama es `master`.

Traducido: **hoy no hay nada publicado**. Mientras el repositorio viva solo en el escritorio
del dueño, no existe URL que ella pueda añadir. El primer paso es crear el repositorio en
GitHub y subirlo.

### Antes de subir: qué se sube

El repositorio contiene, además del plugin, la documentación de arquitectura del proyecto.
**Antes del primer push hay que decidir conscientemente qué se publica**, sobre todo si el
repositorio va a ser público. Dos opciones:

- **Repositorio dedicado solo al plugin** — más limpio, y lo único que ella ve. Exige mover
  o duplicar `.claude-plugin/marketplace.json` y `plugins/despacho/` a un repositorio nuevo.
- **Este mismo repositorio** — un solo sitio, sin duplicación, pero ella tendría acceso a
  todos los `docs/`.

**SUPUESTO DECLARADO:** esta guía está escrita para el segundo caso (este mismo repositorio,
tal como está). Si se opta por el primero, las rutas siguen siendo las mismas pero la raíz
cambia.

### El repositorio tiene que ser alcanzable desde la cuenta de ella

Este es el punto que rompe la instalación si se pasa por alto. Cowork añade el mercado
descargando el repositorio: **si su cuenta no puede leerlo, no hay instalación**.

- **Si el repositorio es público:** cualquiera lo lee. Es el camino con menos piezas que
  fallar, y el precio es que la documentación queda a la vista de todo el mundo.
- **Si el repositorio es privado:** hay que darle acceso a la cuenta de GitHub de ella
  (invitación de colaborador, o el equipo correspondiente).
  **POR COMPROBAR — bloqueante:** que Cowork sepa autenticarse contra un repositorio privado
  de GitHub desde la máquina de ella, y con qué credencial. No está verificado aquí. Si se
  elige repositorio privado, **hay que probarlo antes de sentarse con ella**, no delante.

---

## 4. Instalación en la máquina de ella

Antes de empezar, comprobado: (a) tiene plan de pago con Cowork; (b) el repositorio está en
GitHub y **su cuenta puede leerlo**.

1. Ella abre **Cowork** (no un chat corriente de Claude).
2. Va a **Customize -> Plugins -> Add marketplace**.
3. Pega la dirección del repositorio: `https://github.com/owner/repo`, o la forma corta
   `owner/repo`. (Sustituir por la dirección real; hoy todavía no existe — ver §3.)
4. Sobre el plugin **Despacho** que aparece en ese mercado, pulsa **Install**.
5. Comprobación de que quedó bien: en una sesión nueva, escribir `/estado-del-caso` y ver
   que el comando existe. Es la prueba más barata; si no aparece, no siga adelante.

**No inventar pasos intermedios.** Lo anterior es lo que está verificado. Si en pantalla
aparece algo distinto —una confirmación, una lista de componentes, un permiso—, **léalo y
decida**, pero no dé por hecho que esta guía lo previó.

**POR COMPROBAR:** si los comandos aparecen en una sesión que ya estaba abierta, o solo en
las que se abran después de instalar. Ante la duda, abrir sesión nueva.

Después de instalar hay una segunda mitad que esta guía no cubre y que es la que de verdad
decide si esto sirve: **explicarle a ella cómo pedir las cosas**, y dejar montada la carpeta
del caso con la estructura que los métodos esperan (`1-Documentos recibidos/`,
`2-Borradores/`, `3-Para presentar/`). Eso está en la guía de carpetas del proyecto, no aquí.

---

## 5. Publicar una actualización

El ciclo completo tiene tres partes, y **la tercera la hace ella**:

1. **El dueño edita** el archivo que toque dentro de `plugins/despacho/` — normalmente un
   `SKILL.md`.
2. **El dueño sube el cambio:**
   ```
   git add plugins/despacho
   git commit -m "despacho: <qué cambió>"
   git push
   ```
3. **Ella actualiza:** en **Customize -> Plugins**, pulsa **Update** sobre el mercado. Eso
   trae las versiones nuevas.

Mientras ella no pulse **Update**, sigue usando la versión que instaló. Un `push` por sí
solo no cambia nada en su máquina. Esto es bueno —nada le cambia debajo de los pies a mitad
de un caso— y hay que tenerlo presente: **si se corrige algo importante, hay que avisarle
de que pulse Update**, no basta con arreglarlo.

**Subir también la versión.** En `plugins/despacho/.claude-plugin/plugin.json` está el campo
`version` (hoy `0.1.0`). Conviene subirlo en cada cambio publicado: es lo que permite saber,
mirando su pantalla, qué versión tiene ella puesta.
**POR COMPROBAR:** si **Update** exige que el número de versión haya cambiado para traer lo
nuevo, o si trae lo que haya en el repositorio de todos modos. Subir la versión siempre es
la disciplina segura mientras esto no esté verificado.

**Regla de contenido, no de herramienta:** estos archivos son el método con el que se trabajan
casos reales. Un cambio en un `SKILL.md` cambia cómo se produce trabajo jurídico. No se
publican cambios sin leerlos completos.

---

## 6. Dónde se procesa el material de la clienta

Esto **no** es un problema de arquitectura futura. Es un problema de **secreto profesional hoy**,
desde el primer expediente que ella abra y aunque el Core no exista nunca.

**HECHO VERIFICADO:** *"Cowork sessions run in the cloud by default: the agent loop and code
execution run on Anthropic's servers"*, y *"The agent's work, including any local files it
opens through the desktop app, is processed on Anthropic's servers rather than staying on
the device."*

**HECHO VERIFICADO:** *"Local MCP servers don't run in sessions in the cloud."*

**Qué significa esto hoy.** Que el plugin sea solo texto no cambia nada: lo que viaja no es el
plugin, es **el material de la clienta**. Un expediente que vive en el disco de ella, sin copia
en ningún sitio, deja de estar confinado en el momento en que ella lo abre en una sesión — los
archivos locales que la sesión abre se procesan fuera de la máquina. **El confinamiento del
material de una clienta no depende de que exista un servidor propio**: depende de dónde se
procesa lo que ella abre, y eso ya está decidido por defecto, hoy, con Core o sin él.

**Qué obliga a hacer.** Decírselo a ella **antes** de que abra el primer caso, en esos términos
y sin adornos, porque es de lo poco que puede cambiar lo que ella hace: hay material que decidirá
no abrir aquí, y esa decisión es suya y es de su oficio. Está escrito para ella en
`GUIA-PARA-LA-ABOGADA.md`, §3. **Entregar el plugin sin esa conversación es entregarlo mal**, y
no es un descuido reparable después: el material que ya se abrió, ya se abrió.

**Lo que sí es problema de mañana**, y que no sustituye a lo anterior: cuando se le añada un
**servidor MCP propio** —el Core: el expediente con garantías, el registro de autorizaciones, la
copia inmutable de la prueba—, la tercera cita pasa a ser el problema de ingeniería central: **un
servidor MCP local no corre en una sesión en la nube**, y las sesiones son en la nube por defecto.
Un Core local instalado bajo ese supuesto sin comprobarlo simplemente no aparecería.

**Las comprobaciones, en su máquina y antes de que abra material real:**

1. Verificar en la máquina de ella si su sesión corre en la nube o en local, y si en su plan
   existe algún control para cambiarlo. **POR COMPROBAR:** el interruptor documentado
   ("Run Cowork in the cloud") aparece como control de administrador en planes Team y
   Enterprise; **para Pro no se ha localizado un control equivalente** — no localizado no es
   inexistente, hay que mirarlo en su cuenta. Lo que se encuentre se le dice a ella tal cual,
   incluido que no se encontró nada; y si no lo hay, el diseño del Core tiene que asumirlo,
   no desearlo.
2. Verificar qué ve la sesión de la carpeta del caso en cada modo. Los once métodos leen y
   escriben archivos de su carpeta; conviene saber con qué ruta trabaja realmente antes de
   apoyar nada encima.

Ninguna de estas dos comprobaciones se puede sustituir por lectura de documentación: hay que
hacerlas en su máquina, con su cuenta y su plan.

---

## 7. Estructura del repositorio y cómo se añade un comando

```text
legal-workspace/
├─ .claude-plugin/
│  └─ marketplace.json          <- esto convierte el repo en mercado (va en la RAIZ)
├─ plugins/
│  └─ despacho/
│     ├─ .claude-plugin/
│     │  └─ plugin.json         <- nombre, version, descripcion del plugin
│     ├─ README.md              <- este archivo
│     ├─ GUIA-PARA-LA-ABOGADA.md  <- lo que lee ella; viaja con el plugin
│     └─ skills/
│        ├─ cronologia/
│        │  └─ SKILL.md
│        ├─ estado-del-caso/
│        │  └─ SKILL.md
│        ├─ hechos-con-prueba/
│        │  ├─ SKILL.md
│        │  └─ FORMATO-DE-SALIDA.md          <- material de apoyo del metodo
│        ├─ inventario-de-anexos/
│        │  └─ SKILL.md
│        ├─ redactar-escrito/
│        │  └─ SKILL.md
│        └─ revisar-documento/
│           └─ SKILL.md
└─ docs/                        <- arquitectura del proyecto; NO es parte del plugin
   └─ discovery/                <- material de pruebas y guias de trabajo del dueno
```

Dos archivos mandan: `marketplace.json` (raíz) dice qué plugins hay y dónde están;
`plugin.json` (dentro del plugin) dice cómo se llama y qué versión es.

**Dos movimientos ya hechos, para que nadie los busque donde estaban:** la carpeta
`fact-builder/` se llama ahora `hechos-con-prueba/` —el nombre de la carpeta es el nombre del
comando, así que el comando cambió con ella—, y el `COMO-USARLO-EN-EL-BASELINE.md` que vivía
dentro de esa carpeta **salió del plugin**: hoy es
`docs/discovery/baseline-como-usar-fact-builder.md` y no se instala. Era
material de pruebas del dueño, no método; dentro del plugin viajaba a la máquina de ella sin
tener nada que hacer allí.

### Añadir un comando nuevo

**HECHO VERIFICADO:** cada skill expone un comando derivado de su campo `name`.

1. Crear la carpeta `plugins/despacho/skills/<nombre-del-comando>/`. El nombre de la carpeta
   es el nombre del comando: `skills/contar-terminos/` -> `/contar-terminos`.
2. Dentro, un `SKILL.md` que empiece por el bloque de metadatos, igual que los once que ya
   están:
   ```yaml
   ---
   name: contar-terminos
   description: Método para... Úsalo cuando... No lo uses para...
   version: 0.1.0
   ---
   ```
   El campo `name` **debe coincidir con el nombre de la carpeta**. La `description` es lo que
   decide cuándo se activa el método: se escribe con las tres partes —qué hace, cuándo usarlo,
   cuándo **no**— porque la tercera es la que evita que el método se meta donde no debe.
3. Escribir el método siguiendo la forma de los que ya existen: propósito y límites,
   principio rector, procedimiento, formato de salida, autoevaluación antes de entregar.
4. No hay que tocar `marketplace.json` ni `plugin.json` para añadir un comando: basta con la
   carpeta nueva dentro de `skills/`. Sí conviene subir `version` en `plugin.json` (§5).
5. Publicar según §5, y decirle a ella que pulse **Update**.

Material de apoyo: los archivos extra junto a un `SKILL.md` (como el `FORMATO-DE-SALIDA.md` de
`hechos-con-prueba/`) son parte del método y viajan con él — con el mismo criterio al revés: lo
que no sea método no debe estar ahí, porque se instala en la máquina de ella.

---

## 8. Lo que este plugin todavía NO hace

Hay que ser exacto con esto, porque el plugin resuelve la parte visible del trabajo y eso
hace fácil creer que resuelve más de lo que resuelve. **Despacho es método, no garantía.**

**No hay expediente con garantías.** Los archivos del caso son archivos normales en carpetas
normales. Cualquiera con acceso a la máquina puede abrirlos, editarlos o borrarlos, y nada
lo registra. No hay integridad verificable: si algo cambia, no hay forma de demostrarlo.

**No hay autorización registrada.** Cuando ella acepta un hecho, aprueba un borrador o
descarta un anexo, esa decisión no queda anotada en ningún sitio como decisión suya, con
fecha y con qué se le mostró exactamente al decidirlo. Los métodos se lo piden al modelo
—que marque huecos, que no rellene, que no dé por aceptado lo que no aceptó ella— y eso es
disciplina, no barrera. **Un método no impide nada: describe la conducta correcta.**

**No hay copia inmutable de la prueba.** El material que llega no se sella al entrar. Cuando
un método cita "documento X, página 3", cita el archivo tal como está **hoy**; si mañana ese
archivo es otro, la cita apunta al nuevo sin que nada avise. Los métodos protegen la carpeta
`1-Documentos recibidos/` por convención —está escrito que ahí no se escribe nunca— y una
convención se cumple hasta que no se cumple.

**No hay memoria del caso entre sesiones** más allá de lo que quede escrito en los archivos
de la carpeta.

Todo eso es el **Core**: un servidor propio con el expediente, el registro de eventos, la
autorización humana y la incorporación sellada de la prueba. Está diseñado en `docs/architecture/`
y **viene después**. Este plugin es la mitad que se puede entregar hoy, y entregarla ya tiene
valor; pero mientras el Core no exista, **lo que hay son buenos métodos sobre archivos
corrientes**, y así hay que presentarlo — a ella la primera.

---

## 9. Resumen de lo que falta comprobar

| Qué | Cuándo bloquea |
|---|---|
| El repositorio no está en GitHub: no hay remoto configurado (§3) | **Ahora.** Sin esto no hay instalación posible. |
| Acceso de su cuenta si el repositorio es privado, y cómo se autentica Cowork (§3) | **Antes de instalar**, si se elige repositorio privado. |
| Que su cuenta tenga plan de pago con Cowork (§2) | **Antes de instalar.** No hay alternativa gratuita. |
| Que los comandos aparezcan con el nombre esperado (§1) | En la primera sesión. Se ve en un intento. |
| Que **Update** traiga lo nuevo sin subir `version` (§5) | Al publicar el primer cambio. |
| Que `/redactar-escrito` produzca `.docx` en su entorno (§1) | En el primer borrador real. |
| Que pueda transcribir o citar minutos de una grabación (§1) | **Antes de sentarse a trabajar**, con un archivo real de ella. Bloquea el Ejemplo 2 de su guía y media promesa de `/hechos-con-prueba`. |
| Qué hace con un PDF escaneado sin capa de texto (§1) | **Antes de sentarse a trabajar**, con un archivo real de ella. Si no lo lee, no funciona ninguno de los once. |
| Nube o local, y si en Pro hay control para elegirlo (§6) | **Antes de que abra material de una clienta.** Es secreto profesional hoy, no arquitectura de mañana. |
