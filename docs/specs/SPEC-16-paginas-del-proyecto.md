# SPEC-16 — Las páginas del proyecto: una puerta de entrada, y lo guardado comprobado

**Estado:** prototipo validado en un caso real el 2026-09-24, y **endurecido el mismo día**. Ese día quien iba a declarar abrió las páginas desde dentro del `.zip`, no sonaba nada y ninguna página lo dijo. Además, trabaja en un **Mac**. El dueño pidió que sea **estándar** («todo esto debe quedar como estándar en el legal-workspace para futuras iteraciones»).

**Dónde vive cada parte:**
- **Prototipo** (INICIO, Compromisos, compendio y validación): `tools/paginas-del-proyecto/`.
- **Ya en el plugin 0.17.0:** el aviso de sitio en las dos páginas, el guardado de voces en la carpeta, el tema compartido, las tablas en el móvil y `genoma_de_voz.py pagina`.
- **Destino del resto:** `plugins/despacho/scripts/` (programa y plantilla), las skills y `GUIA-PARA-LA-ABOGADA.md`.

---

## 1. El problema

Una reunión grabada deja, tras la etapa 1, **dos herramientas en carpetas distintas**:
- la página de voces, en `2-Borradores/Voces/`;
- las páginas de cada grabación, en `2-Borradores/Entregas/ENTREGA …/Transcripciones/`.

Además hay un resumen, una guía de qué oír, un manual y los compromisos. Quien declara tiene que saber cuatro cosas: **por dónde empezar, qué hace en cada sitio, cuándo guardar y si lo que guardó llegó**. Lo que devuelve es la fuente de verdad de la etapa 2: el acta, los compromisos y sus responsables.

## 2. El principio

> **Lo que ella declara oyendo es la fuente de verdad, y solo cuenta si llega guardado a donde la etapa 2 lo recoge.** Las páginas nuevas no deciden nada, no escriben nada suyo y no repiten lo que ya se ve: orientan, añaden datos y comprueban.
>
> **Y si algo impide trabajar —no suena, no puede guardar—, la página lo dice arriba, en grande, con los pasos del sistema que ella tiene.** Una página que falla en silencio parece rota.

## 3. Lo que se genera (por reunión, desde los datos, sin teclear)

| Página | Dónde | Qué lleva |
|---|---|---|
| **INICIO - `<corto>`.html** | Raíz del proyecto (**enmienda a ADR-023**: quinto elemento; hoy, excepción autorizada) | Al abrirse, **comprueba el sitio**:<br>• si se abrió desde un `.zip`;<br>• si encuentra las grabaciones que buscan las páginas;<br>• si el navegador puede guardar en carpetas.<br>Además: barra de navegación; **Apariencia** (6 temas y 4 tamaños); **Cuándo guardar** para Chrome/Edge y para Safari; recorrido en tarjetas; **Comprobar lo que he guardado**; carpetas; cuándo ha terminado |
| **Compromisos - `<corto>` - `<fecha>`.html** | `2-Borradores/Compromisos/` | Cifras por grabación; filtros; buscador; ▶ Oírlo; la cita partida en una « » por línea; nunca un campo de quién |
| **`2-Borradores/Lo que declaré/LÉAME…txt`** | Se crea en el proyecto | Para que la carpeta exista antes de que ella arrastre ahí lo que descargue con Safari |
| **Guía ilustrada** (Word) | `2-Borradores/` | Capturas reales, con una sección “Antes de empezar” (Mac y Windows, qué navegador). Por generalizar: el prototipo aún tiene textos del caso |
| **Paquete** (.zip, nombre corto) | Fuera del proyecto | Todo menos `.trabajo`, el .zip de la entrega, `_fuentes (no enviar)`, `_anteriores` y el mapa del dueño |

Entradas: `entrega.json`, `A<N> - compromisos.json`, el genoma, `datos/A<N> - datos completos.json`, las fuentes .md de la entrega y **las páginas de la entrega ya construidas**, de las que INICIO lee la clave de cada página. A mano solo van el nombre largo, el corto y la fecha. **Orden:** entrega, página de voces e INICIO.

## 4. Reglas de la experiencia

1. **Cuándo guardar, a la vista.** Arriba en INICIO, con lo que se pulsa en cada herramienta, **para Chrome/Edge y para Safari**.
2. **Guardar va a la carpeta del proyecto, no a Descargas**, donde el navegador lo permite:
   - la página de voces escribe `voces declaradas - <reunión>.json` en `2-Borradores/Voces`;
   - las de cada grabación escriben en `2-Borradores/Lo que declaré/<entrega>/`.
   El botón de voces (**💾 Guardar**) va en la cabecera, siempre a la vista, y se ilumina mientras haya decisiones que no están en el proyecto.
3. **Donde no se puede (Safari, Firefox), una sola regla:** todo lo descargado, venga de la página que venga, se arrastra a `2-Borradores/Lo que declaré`. Cada página lo dice al descargar, INICIO lo dice al abrirse, y el recogedor y el comprobador miran ahí.
4. **Nunca se pisa lo de otro navegador.**
   - Si la página está vacía y la carpeta tiene decisiones, ofrece cargarlas.
   - Si la carpeta tiene algo que la página no tiene, lo aparta con fecha antes de escribir.
   - Lo que la propia página escribió en la sesión **no** se aparta (antes se apartaba y llenaba la carpeta de copias).
5. **El sitio, dicho arriba.** Si la página se abrió desde dentro de un `.zip` o no encuentra sus grabaciones, un aviso rojo lo dice antes que nada, y ninguna ventana lo tapa. Los pasos son **los del sistema de quien la abre**: en el Mac, doble clic sobre el `.zip`; en Windows, «Extraer todo…».
6. **Los tooltips añaden, no repiten, y no estorban.**
   - Datos que no están a la vista.
   - Solo sobre el título o el ⓘ, con retardo, `pointer-events: none` y sin tapar «Abrir».
   - **Ocultos no ocupan sitio.** Se abren hacia el lado donde caben.
7. **Un solo tema en todas las páginas.** El de INICIO (`despacho-apariencia`) manda; las páginas de cada grabación lo siguen y lo devuelven.
8. **Nada se sale por el lado** a 390, 768, 1024 y 1280 px. Las tablas largas se desplazan por dentro.
9. Cero red, ninguna ruta de la máquina y « » solo para lo literal: los nombres de botones van con “ ” o en negrita. **Las rutas visibles con “›”**, que valen en Mac y en Windows.

## 5. El comprobador (INICIO) — solo lee

Hay dos maneras de elegir la carpeta, y la lectura es la misma:
- **Chrome y Edge:** `showDirectoryPicker({mode:'read'})`.
- **Safari y Firefox:** `<input webkitdirectory>`. La lista de archivos se envuelve con la misma forma que el selector. Safari dice «Subir» en el cuadro, y la página avisa de que no se sube nada.

Encuentra el proyecto aunque se elija una carpeta por encima. Lee **todos** los `.json` de `2-Borradores/Voces` y de `2-Borradores/Lo que declaré` (a cualquier nivel) y **los reconoce por la clave, no por el nombre**:
- **La declaración de voces** (la más reciente): quién declara, cuántas líneas y la claridad por grabación contra la meta.
- **Cada grabación, una por una**, por la clave de su página: cuántas declaraciones, cuándo y dónde. Si no hay nada, lo dice, con qué pulsar.
- **Lo que es de otra versión de las páginas**, que se nombra para que no se pierda.

Nunca escribe, mueve ni borra.

## 6. Validación de punta a punta (se corre antes de entregar)

Medida el 2026-09-24 sobre el **.zip final**, extraído **con el extractor del Explorador de Windows** (Shell.Application) **y con uno que respeta los nombres como el Mac**. Los nombres salen idénticos, con la tilde descompuesta intacta. Cada fila se probó en una pestaña propia, con perfil temporal y `file://`:

| Qué dice la página | Cómo se prueba | Resultado |
|---|---|---|
| INICIO: todo en su sitio; el navegador guarda o no | Guion 4 | ✔ en verde; en modo Safari, el aviso con los pasos del Mac |
| Voces: encuentra y **reproduce** las grabaciones | Guion 4 (Espacio y `currentTime`) | ✔ suena |
| Voces: 💾 Guardar escribe en `2-Borradores/Voces`, con copia fechada, y se autoguarda | Guion 4, carpeta simulada | ✔ |
| Voces: otro navegador no pisa lo que hay | Guion 4, página vacía y carpeta con trabajo | ✔ pregunta; 0 escrituras antes de decidir; carga |
| La etapa 2 acepta lo escrito y lo descargado | `genoma_de_voz.py aplicar` | ✔ los dos |
| Grabación: avisa de lo pendiente, guarda en el proyecto y se autoguarda sin copias de ruido | Guion 2 | ✔ 3 escrituras (antes 4) |
| Lo guardado lo recoge la etapa 2 | `probar_recoger.py`; lo arrastrado a `Lo que declaré`, por prueba unitaria | ✔ |
| Comprobador: lee las dos cosas (Chrome) y lo arrastrado (Safari) | Guiones 2 y 4 | ✔ grabación por grabación |
| Modo Safari: las dos páginas descargan y dicen a dónde llevarlo | Guion 4 (agente de Safari y sin `showDirectoryPicker`) | ✔ |
| Abierta desde un `.zip`: aviso rojo con los pasos del sistema | Guion 4, copias sueltas en `Temp\<guid>_…zip.xxx\` | ✔ Mac y Windows; la bienvenida no lo tapa |
| Tooltips, tema recordado y filtros | Guion 3 | ✔ |
| Nada se sale por el lado | `medir_anchos.py`: 11 páginas × 4 anchos | ✔ 44 de 44 |

**Lo que no se puede probar aquí:** el motor de Safari (WebKit) de verdad y el selector de carpetas con el clic humano que da el permiso. Los audios son AAC-LC en MP4, que Safari reproduce de fábrica. **Queda por verificar en un Mac.**

## 7. Lo que queda abierto

1. **Integrar en el plugin** el programa de INICIO y Compromisos, la plantilla, las pruebas, las skills y la guía. Hacer genérica la guía ilustrada.
2. **Enmienda a ADR-023** (INICIO en la raíz).
3. **Estado compartido** entre la página de voces y las de cada grabación (tarea aparte).
4. ~~`guardado.js` aparta como «en curso anterior» su propio guardado~~ — **arreglado** el 2026-09-24, con prueba que falla sin el arreglo.
5. **MAX_PATH** (solo Windows): el peor caso medido llega a 219 de 260 con un .zip de nombre corto.
6. La **página de voces** aún no tiene los temas de INICIO: solo claro.
7. **Probar en un Mac de verdad**: Safari y Chrome, extracción con doble clic, reproducción y descarga.
8. Fallos de instrumentos del plugin, vistos el mismo día:
   - `md2html.ilegibles_de` solo enseña los rescates de los huecos de 8 s o más;
   - `verificar_citas` no parte las citas « / »;
   - `md2docx` deja columnas estrechas;
   - los nombres NFD.
9. Dos pruebas del repositorio fallan **por el entorno Windows** y no por el código:
   - `test_pagina_publicada.test_ninguno`: la copia de trabajo tiene CRLF por `core.autocrlf=true`; lo guardado en git no;
   - `test_dependencias`: esconder una biblioteca instalada no surte efecto en esta máquina.
