# Páginas del proyecto — prototipo validado

Lo que se construyó y se validó de punta a punta el 2026-09-24 en un caso real (una mesa de trabajo de tres grabaciones), para que **cada reunión nueva salga igual**. La especificación está en [`docs/specs/SPEC-16-paginas-del-proyecto.md`](../../docs/specs/SPEC-16-paginas-del-proyecto.md).

**Estado:** prototipo fuera del plugin. Llevarlo a `plugins/despacho` (programa, plantilla, pruebas, skills y guía) es la tarea pendiente. Aquí no hay ningún dato de ningún caso: las rutas y los nombres se pasan como parámetros.

## Qué hay

| Archivo | Qué hace |
|---|---|
| `paginas_del_proyecto.py` | Genera **INICIO** (en la raíz del proyecto) y **COMPROMISOS** (en `2-Borradores/Compromisos/`). Autocontenidas, cero red |
| `compendio.py` | Empaqueta el proyecto para quien declara, sin lo que no debe viajar, y mide el riesgo de MAX_PATH |
| `validar/cdp.mjs` | Maneja Edge sin ventana por DevTools (Node 20, `--experimental-websocket`, sin instalar nada) y ejecuta guiones |
| `validar/carpeta_simulada.js` | Carpeta en memoria con la API de acceso a archivos: con `file://` no hay OPFS |
| `validar/guiones/1-voces.json` | Página de voces: oír, decidir, descargar la declaración |
| `validar/guiones/2-grabacion-y-comprobador.json` | Página de una grabación con `file://`: aviso de pendiente, guardar, autoguardado; y el comprobador de INICIO |
| `validar/guiones/3-apariencia-y-tooltips.json` | Tooltips que no estorban, tema recordado, filtros y móvil sin desborde |
| `validar/probar_recoger.py` | Lo escrito por la página lo recoge `recoger_lo_declarado.py` |
| `validar/citas_cortas.py` | Las citas « » de menos de 18 caracteres, cerca de su minuto |

## Cómo se usa

```text
python paginas_del_proyecto.py <proyecto> <proyecto>/2-Borradores/Entregas/_fuentes (no enviar)/entrega.json \
       --reunion "<nombre largo>" --corto "<corto>" --fecha AAAA-MM-DD
python <plugin>/scripts/verificar_citas.py "<proyecto>/2-Borradores/Compromisos/Compromisos - <corto> - <fecha>.html" "<transcripciones>"
python compendio.py <proyecto> "<scratch>/<corto>.zip"
```

No sobrescribe: si una página existe, se detiene. La versión anterior va a `_anteriores/`.

## Validación de punta a punta (obligatoria antes de entregar)

1. Arrancar Edge **con perfil temporal**: `msedge --headless=new --remote-debugging-port=9333 --user-data-dir=<scratch>\edge --no-first-run --disable-sync --autoplay-policy=no-user-gesture-required about:blank`
2. `node --experimental-websocket validar/cdp.mjs validar/guiones/1-voces.json SALIDA=<scratch>/v DESCARGAS=<scratch>/v/descargas VOCES_URL=file:///…/Voces%20-%20….html`, y después `genoma_de_voz.py aplicar <genoma> "<descarga>" --salida <scratch>/aplicar`. **Tiene que aceptarla.**
3. Guion 2 con `AUDIO_URL`, `INICIO_URL`, `CARPETA_SIMULADA`, `PROYECTO` (nombre de la carpeta), `ARBOL_DIR` y `DECLARACION` (la del paso 2). Lo esperado: el aviso «Tiene marcas que aún no ha guardado», «Guardado en «<proyecto> › 2-Borradores › Lo que declaré › <entrega>»», más escrituras al marcar otra vez, y el comprobador leyendo las dos cosas.
4. `python validar/probar_recoger.py --proyecto … --entrega "<ENTREGA - …>" --arbol <ARBOL_DIR> --trabajo <carpeta corta>`. **Tiene que recoger lo confirmado.**
5. Guion 3 con `INICIO_URL` y `COMPROMISOS_URL`. Ningún tooltip tapa «Abrir», el clic llega, el tema se recuerda y en móvil no hay desborde.
6. Cerrar **solo** los procesos de Edge con el perfil temporal.

Las URL `file:///` van con `%20` en los espacios. Los valores con barras: siempre `/`.

## Lecciones de instrumento (ver memoria `instrumentos-que-mienten`)

- **Pestaña propia siempre.** La primera de `/json/list` puede ser `edge://sync-confirmation-dialog` (360×505): todo lo medido sale falso.
- **Descargas a nivel de navegador** (`Browser.setDownloadBehavior`), y esa sesión **abierta hasta el final**. A nivel de página se ignora; cerrándola, la descarga no cae en ninguna parte.
- **`file://`, no `http://`.** Servida por http, la página de una grabación no reconoce el proyecto y guarda en otro sitio. La prueba tiene que ser como la usa ella.
- **MAX_PATH.** El scratchpad ya es largo. Las copias de prueba llevan nombres cortos (el recogedor casa por clave). Para ella: `.zip` de nombre corto y extraer en Descargas o en el Escritorio.
- **Un aviso de «no encontrada» puede ser del instrumento.** `citas_cortas.py` empareja una fila con dos minutos con el primero.
