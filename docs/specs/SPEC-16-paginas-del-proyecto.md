# SPEC-16 — Las páginas del proyecto: una puerta de entrada, y lo guardado comprobado

**Estado:** prototipo validado en un caso real el 2026-09-24; el dueño pidió que sea **estándar** («todo esto debe quedar como estándar en el legal-workspace para futuras iteraciones»). Falta integrarlo en el plugin.
**Prototipo:** `tools/paginas-del-proyecto/` · **Destino:** `plugins/despacho/scripts/` (programa y plantilla), skills y `GUIA-PARA-LA-ABOGADA.md`

---

## 1. El problema

Una reunión grabada deja, tras la etapa 1, **dos herramientas en carpetas distintas**, la página de voces (`2-Borradores/Voces/`) y las páginas de cada grabación (`2-Borradores/Entregas/ENTREGA …/Transcripciones/`), más un resumen, una guía de qué oír, un manual y los compromisos. Quien declara tiene que saber **por dónde empezar, qué hace en cada sitio, cuándo guardar y si lo que guardó llegó**, porque lo que devuelve es la fuente de verdad de la etapa 2 (el acta, los compromisos y sus responsables).

## 2. El principio

> **Lo que ella declara oyendo es la fuente de verdad, y solo cuenta si llega guardado a donde la etapa 2 lo recoge.** Las páginas nuevas no deciden nada, no escriben nada suyo y no repiten lo que ya se ve: orientan, añaden datos y comprueban.

## 3. Lo que se genera (por reunión, desde los datos, sin teclear)

| Página | Dónde | Qué lleva |
|---|---|---|
| **INICIO - `<corto>`.html** | Raíz del proyecto (**enmienda a ADR-023**: quinto elemento; hoy, excepción autorizada) | Barra de navegación a todas las páginas; **Apariencia** (6 temas y 4 tamaños de letra, recordados entre páginas); **Cuándo guardar**; recorrido en tarjetas; dos maneras de guardar; **Comprobar lo que he guardado**; carpetas; cuándo ha terminado |
| **Compromisos - `<corto>` - `<fecha>`.html** | `2-Borradores/Compromisos/` | Cifras por grabación; filtros por grabación, estado y tipo; buscador; ▶ Oírlo en su minuto; la cita partida en una « » por línea (así la comprueba `verificar_citas`); nunca un campo de quién |
| **Guía ilustrada** (Word) | `2-Borradores/` | Capturas reales de cada pantalla, sacadas con Edge sin ventana (por generalizar: el prototipo aún tiene textos del caso) |
| **Paquete** (.zip, nombre corto) | Fuera del proyecto | Todo menos `.trabajo`, el .zip de la entrega, `_fuentes (no enviar)`, `_anteriores` y el mapa del dueño |

Entradas: `entrega.json`, `A<N> - compromisos.json`, el genoma, `datos/A<N> - datos completos.json` y las fuentes .md de la entrega. A mano solo van el nombre largo, el corto y la fecha.

## 4. Reglas de la experiencia (pedidas por el dueño)

1. **Cuándo guardar, a la vista**: bloque propio arriba en INICIO, con lo que se pulsa en cada herramienta al terminar **cada** sesión.
2. **Los tooltips añaden, no repiten.** Llevan datos que no están a la vista y que salen del proyecto: apartados y número de citas del resumen, puntos que oír por grabación y cuál va primero, voces, líneas y rescates, compromisos sin cerrar, duraciones y tramos en discordia, y teclas útiles.
3. **Los tooltips no estorban**:
   - se abren solo sobre el título o el ⓘ (no sobre toda la tarjeta), con un retardo de ~0,35 s;
   - `pointer-events: none`: el clic siempre llega;
   - no tapan el botón «Abrir»;
   - en táctil y en pantallas estrechas, no salen.
4. **Móvil**: la barra no es fija, va en su propia fila y se desplaza por dentro. Nada desborda en horizontal.
5. Cero red, ninguna ruta de la máquina, « » solo para lo literal (los nombres de botones, con “ ” o en negrita).

## 5. El comprobador (INICIO) — solo lee

`showDirectoryPicker({mode:'read'})`. Encuentra el proyecto aunque se elija una carpeta por encima (p. ej. Descargas con la carpeta que crea el Explorador al extraer). Luego:

- **Declaración de voces**: `voces declaradas*.json` en `2-Borradores/Voces/`. Comprueba el formato `despacho/voces-linea-a-linea`, que **la clave sea la del genoma**, quién declara, cuántas líneas decididas y la claridad por grabación contra la meta. Sale en ámbar si no llega.
- **Lo guardado de cada grabación**: `2-Borradores/Lo que declaré/<entrega>/`, «en curso» y copias fechadas, contado con el mismo criterio que `guardado.js` (`cuantoHay`).
- Nunca escribe, mueve ni borra.

## 6. Validación de punta a punta (se corre antes de entregar)

Medido el 2026-09-24. Cada fila se probó en una pestaña propia, con un perfil temporal y `file://`:

| Qué dice la página | Cómo se prueba | Resultado |
|---|---|---|
| Voces: «⤓ Guardar mi declaración» la descarga | Guion 1 + `genoma_de_voz.py aplicar` | ✔ la acepta; la claridad coincide |
| Grabación: avisa de lo pendiente | Guion 2 | ✔ «Tiene marcas que aún no ha guardado…» |
| Grabación: guarda en el proyecto, con copia fechada y autoguardado | Guion 2, carpeta simulada | ✔ `2-Borradores/Lo que declaré/<entrega>/` |
| Lo guardado sirve para la etapa 2 | `probar_recoger.py` | ✔ `recoger_lo_declarado.py` lo recoge |
| El comprobador lee las dos cosas | Guion 2 | ✔ |
| Los tooltips añaden y no estorban; el tema se recuerda; móvil | Guion 3 | ✔ |

## 7. Lo que queda abierto

1. **Integrarlo en el plugin**: programa, plantilla, pruebas, skills y guía. Llevar los mismos temas, tamaños y barra a `pagina.html` y `voces.html`.
2. **Enmienda a ADR-023** (INICIO en la raíz).
3. **Estado compartido** entre la página de voces y las de cada grabación (tarea aparte).
4. `guardado.js` aparta como «en curso anterior» su propio guardado de minutos antes, en la misma sesión: ruido, y nombres más largos.
5. **MAX_PATH**: el peor caso medido llegó a 224 de 260 con un .zip de nombre corto. Con 267, Edge no abre la página.
6. Fallos de otros instrumentos del plugin, encontrados el mismo día:
   - `md2html.ilegibles_de` solo enseña los rescates de los huecos de 8 s o más;
   - `verificar_citas` no parte las citas unidas con « / »;
   - `md2docx` deja columnas estrechas junto a los hashes;
   - los nombres con la tilde descompuesta (o + U+0301).
7. La **guía ilustrada** está sin generalizar.
