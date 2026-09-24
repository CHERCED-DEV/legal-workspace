# Páginas del proyecto — prototipo validado

Lo que se construyó y se validó de punta a punta el 2026-09-24 en un caso real (una mesa de trabajo de tres grabaciones), para que **cada reunión nueva salga igual**. La especificación está en [`docs/specs/SPEC-16-paginas-del-proyecto.md`](../../docs/specs/SPEC-16-paginas-del-proyecto.md).

**Estado:** prototipo fuera del plugin para INICIO, Compromisos, el compendio y la validación. Lo que tocaba a las páginas del plugin ya está en `plugins/despacho` 0.17.0: el aviso de sitio, el guardado de voces en la carpeta, el tema compartido, las tablas en el móvil y `genoma_de_voz.py pagina`. Aquí no hay ningún dato de ningún caso: las rutas y los nombres se pasan como parámetros.

## Qué hay

| Archivo | Qué hace |
|---|---|
| `paginas_del_proyecto.py` | Genera **INICIO** (en la raíz del proyecto) y **COMPROMISOS** (en `2-Borradores/Compromisos/`). Autocontenidas, cero red. INICIO comprueba al abrirse el sitio (abierta desde un `.zip`, grabaciones, navegador) y trae el comprobador de lo guardado, que funciona también en Safari |
| `compendio.py` | Empaqueta el proyecto para quien declara, sin lo que no debe viajar, y mide el riesgo de MAX_PATH (Windows) |
| `validar/cdp.mjs` | Maneja Edge sin ventana por DevTools (Node 20, `--experimental-websocket`, sin instalar nada) y ejecuta guiones |
| `validar/carpeta_simulada.js` | Carpeta en memoria con la API de acceso a archivos: con `file://` no hay OPFS |
| `validar/guiones/1-voces.json` | Página de voces: oír, decidir, descargar la declaración |
| `validar/guiones/2-grabacion-y-comprobador.json` | Página de una grabación con `file://`: aviso de pendiente, guardar, autoguardado; y el comprobador de INICIO |
| `validar/guiones/3-apariencia-y-tooltips.json` | Tooltips que no estorban, tema recordado, filtros y móvil sin desborde |
| `validar/guiones/4-sitio-voces-y-safari.json` | **El guion del Mac y del .zip**: INICIO en su sitio; voces que suena, guarda en la carpeta, se autoguarda y no pisa lo de otro navegador; modo Safari (sin escribir en carpetas); páginas sueltas en la carpeta temporal de un `.zip` |
| `validar/medir_anchos.py` | Guion que abre todas las páginas a 390, 768, 1024 y 1280 px y dice si algo se sale o si la página se desplaza hacia el lado |
| `validar/probar_recoger.py` | Lo escrito por la página lo recoge `recoger_lo_declarado.py` |
| `validar/citas_cortas.py` | Las citas « » de menos de 18 caracteres, cerca de su minuto |

## Cómo se usa, en este orden

```text
python <plugin>/scripts/construir_entrega.py <entrega.json>
python <plugin>/scripts/genoma_de_voz.py pagina "<genoma>.json" --salida "<proyecto>/2-Borradores/Voces"   (si cambió la plantilla)
python paginas_del_proyecto.py <proyecto> <entrega.json> --reunion "<nombre largo>" --corto "<corto>" --fecha AAAA-MM-DD
python <plugin>/scripts/verificar_citas.py "<proyecto>/2-Borradores/Compromisos/Compromisos - <corto> - <fecha>.html" "<transcripciones>"
python compendio.py <proyecto> "<scratch>/<corto>.zip"
```

- **INICIO se genera el último**, porque lee la clave de cada página de grabación ya construida.
- **No sobrescribe:** si una página existe, se detiene. La anterior va a `_anteriores/`.
- **Crear `2-Borradores/Lo que declaré/`** con un LÉAME, para que exista antes de que ella arrastre ahí lo que descargue con Safari.

## Validación de punta a punta (obligatoria antes de entregar)

1. **Arrancar Edge con perfil temporal:** `msedge --headless=new --remote-debugging-port=9333 --user-data-dir=<scratch>\edge --no-first-run --disable-sync --autoplay-policy=no-user-gesture-required about:blank`.
2. **Extraer el `.zip` final de dos maneras, en rutas cortas:**
   - con el extractor del Explorador, `Shell.Application` → `NameSpace(dest).CopyHere(NameSpace(zip).Items(), 1044)`;
   - con `zipfile`, que respeta los nombres como el Mac.
   Comprobar que los nombres salen idénticos y que cada archivo es igual al del proyecto.
3. **Para el caso del `.zip`:** copiar INICIO, la página de voces y una de grabación, cada una sola, a `%TEMP%\<guid>_<nombre>.zip.6aa\<proyecto>\…`, que es lo que hace Windows al abrir desde dentro.
4. **Guion 4 sobre las dos extracciones.** Variables: `SALIDA`, `DESCARGAS`, `INICIO_URL`, `VOCES_URL`, `AUDIO_URL`, `CARPETA_SIMULADA`, `PROYECTO`, `PADRE` (la carpeta que contiene el proyecto, **con su nombre real**), `ARBOL_DIR` y `ZIP_*_URL`. Tiene que salir:
   - “Todo en su sitio”;
   - `SUENA` con un `currentTime` que avanza;
   - 💾 Guardar en `2-Borradores/Voces`, y autoguardado;
   - “Ya hay una declaración guardada” con 0 escrituras;
   - en modo Safari, los avisos y las dos descargas;
   - el aviso rojo del `.zip` con los pasos del Mac y los de Windows.
5. **`genoma_de_voz.py aplicar`** sobre lo que la página escribió y sobre lo descargado. **Tiene que aceptar los dos.**
6. **Guion 2** y después **`probar_recoger.py`**. **Tiene que recoger lo confirmado.**
7. **Guion 3**, y **`medir_anchos.py`**: 0 líneas `MAL`.
8. **Cerrar solo** los procesos de Edge con el perfil temporal.

Las URL `file:///` se hacen con `pathlib.Path(...).as_uri()`: codifica espacios y tildes descompuestas. Los valores con barras: siempre `/`.

`cdp.mjs` entiende, además de lo básico:
- `{"agente": ua, "plataforma": "MacIntel"}`: hacerse pasar por Safari en un Mac;
- `{"antes_de_cargar": código}`: quitar `showDirectoryPicker` antes de que cargue la página, como en Safari;
- `{"foto": x, "elemento": expr}`: capturas recortadas para una guía;
- los selectores de archivos se interceptan y se registran.

**Esto no es Safari:** prueba la lógica sin la capacidad que le falta a Safari. Lo propio de WebKit se comprueba en un Mac de verdad.

## Lecciones de instrumento (ver memoria `instrumentos-que-mienten`)

- **Pestaña propia siempre.** La primera de `/json/list` puede ser `edge://sync-confirmation-dialog` (360×505), y entonces todo lo medido sale falso.
- **Descargas a nivel de navegador** (`Browser.setDownloadBehavior`), con esa sesión **abierta hasta el final**. A nivel de página se ignora; si se cierra la sesión, la descarga no cae en ninguna parte.
- **`file://`, no `http://`.** Servida por http, la página de una grabación no reconoce el proyecto y guarda en otro sitio. La prueba tiene que ser como la usa ella.
- **Extraer como ella.** Una extracción con Python no es la del Explorador. Y abrir con doble clic dentro del `.zip` copia la página **sola** a `Temp`: eso fue lo que pasó, y ninguna prueba lo había mirado.
- **Medir más de dos anchos.** A 390 y 1280 px todo cabía; a 768 y 1024, los recuadros de ayuda **ocultos** del borde derecho daban 40 px de desplazamiento lateral. Lo invisible también ocupa sitio.
- **La carpeta simulada tiene que llamarse como la real.** Con un nombre inventado («Descargas») la página rechazó, con razón, una carpeta que no estaba en su camino. Parecía un fallo de la página y era del instrumento.
- **Comprobar con la misma forma Unicode que el disco.** Una comprobación con «grabación» tecleada (NFC) no encontraba los audios, cuyo nombre lleva la tilde descompuesta (NFD). El fallo era del instrumento.
- **Barras invertidas:** en un heredoc de Bash o dentro de `"…"` se pierden. Los parches con rutas de Windows o con `\n` se escriben con Write o con Edit.
- **MAX_PATH.** El scratchpad ya es largo: las copias de prueba llevan nombres cortos, porque el recogedor casa por clave. Para ella, un `.zip` de nombre corto (solo afecta a Windows).
- **Un aviso de «no encontrada» puede ser del instrumento.** `citas_cortas.py` empareja una fila con dos minutos con el primero.
