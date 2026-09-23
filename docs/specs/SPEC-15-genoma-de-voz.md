# SPEC-15 — El genoma de voz: quién dice cada línea, con la última palabra de ella

**Estado:** en construcción, autorizada por el dueño el 2026-09-23.
**Programa:** `plugins/despacho/scripts/genoma_de_voz.py` · **Página:** `tools/pagina-voces/` → `plugins/despacho/scripts/plantilla/voces.html`

---

## 1. El problema, medido

Sobre una mesa de trabajo real de tres grabaciones (2026-09-23):

| Hecho | Cifra |
|---|---|
| Lo transcrito que la separación automática le da a UNA sola voz, en la primera grabación | **96,5 %** |
| Turnos donde dos personas hablan a la vez | 19–34 % |
| Parecido de huella entre las dos mitades de un mismo turno largo | 0,96 |
| Parecido entre dos turnos distintos | 0,75 |
| Parecido de una línea entera con su propia mitad, midiendo sin ventana fija | 0,82 *(absurdo: el todo debe parecerse más)* |
| Lo mismo, con ventanas fijas de 1,5 s | 0,95 |

**Conclusión:** la huella distingue personas; lo que falla es decidir sin que nadie oiga. Y la huella se desplaza con el largo del trozo, así que todo se mide en ventanas fijas.

## 2. El principio

> **La máquina propone por parecido. Ella declara oyendo. Las dos cosas se ven distintas en todo momento, y solo lo declarado sostiene una atribución.**

## 3. `genoma - <título> - <fecha>.json` — lo que produce `preparar`

Es el mismo objeto que se inyecta en la página en `<script id="datos" type="application/json">`.

```json
{
  "formato": "despacho/genoma-de-voz", "version": 1,
  "clave": "16 hex — identifica ESTA preparación",
  "titulo": "…", "generado": "AAAA-MM-DD",
  "modelo": {"huella": "wespeaker-voxceleb-CAMPP.onnx", "dim": 512, "ventana_s": 1.5, "salto_s": 0.75, "umbral_grupo": 0.25},
  "calibracion": {
    "bandas": {"alta": 0.0xx, "media": 0.0xx},
    "cambio": 0.xx, "precision_minima": 0.90, "revisiones_minimas": 8,
    "fiable_s": 1.5, "pisa_max": 0.30, "corta_s": 1.0
  },
  "meta_claridad": 0.85,
  "audios": [{"id": "A1", "nombre": "Audio 1", "ruta": "ruta relativa a la página", "archivo": "…", "duracion": 1648.2}],
  "voces":  [{"id": "v1", "etiqueta": "Voz 1", "vec": "b64 int8[512]", "tipicas": ["A1-12", "…"],
              "biblioteca": [{"nombre", "cargo", "parecido", "fuente"}]}],
  "lineas": [{
    "id": "A1-12", "audio": "A1", "i": 12, "ini": 34.1, "fin": 37.9, "texto": "…",
    "vec": "b64 int8[512]", "adn": "b64 int8[32]", "xy": [x, y],
    "voz": "v1", "parecido": 0.91, "margen": 0.12,
    "pisa": 0.0, "corta": false,
    "dudas": ["las lecturas automáticas no coinciden"],
    "alternativas": [{"fuente": "Lectura del canal derecho", "texto": "…"}],
    "cambio": {"parecido": 0.52, "en": 36.0, "palabra": 5, "vec_a": "b64", "vec_b": "b64"},
    "partes": ["texto hasta la palabra 5", "texto desde la palabra 5"]
  }],
  "huecos": [{"audio": "A2", "ini": 395.3, "fin": 441.2,
              "otras": [{"fuente": "Lectura del canal derecho", "desde": 400, "hasta": 420, "texto": "…"}]}],
  "personas_conocidas": [{"nombre", "cargo", "fuente"}]
}
```

- `vec`: huella de la línea = media normalizada de sus ventanas de 1,5 s, cuantizada a int8 (escala por vector; para el coseno solo importa la dirección).
- `adn`: proyección de la huella sobre las 32 direcciones en que más varían las huellas **de esa reunión**, con una escala común a todas las líneas. Es lo que la página dibuja como «genoma». La de una voz es la media de las de sus líneas.
- `margen`: parecido con la voz más cercana menos parecido con la segunda. **Las bandas se calibran en cada reunión**: `alta` = mediana del margen en las líneas fiables, `media` = percentil 25.
- `pisa`: fracción de la línea en que la diarización oye a dos o más a la vez. Con `pisa ≥ 0,30` la línea **no entra en la huella de nadie**.
- `cambio`: solo si el mejor corte dentro de la línea separa dos partes con parecido por debajo del percentil 5 de la reunión. `partes` es el texto partido por esa palabra.
- `huecos[].otras`: solo ventanas de 20 s **enteramente dentro** del hueco. Una ventana que lo desborda hereda texto de alrededor.

## 4. La página

Un solo HTML autocontenido, cero red (ADR-020). El audio va por ruta relativa; si falta, la página lo dice y no ofrece oír.

### 4.1 El genoma se recalcula en vivo

- **Centroide de una voz** = media normalizada de las huellas de sus líneas **declaradas**. Mientras una voz tenga menos de 2 líneas declaradas, se usa la huella inicial de la propuesta.
- Líneas con `pisa ≥ 0,30`, las marcadas «varios» y «no se distingue» **no entran** en ningún centroide.
- **Propuesta de la máquina para una línea no declarada** = voz de centroide más parecido; `margen` = mejor − segundo. **Banda:** `alta` si `margen ≥ bandas.alta` y la línea no es corta ni se pisa; `media` si `margen ≥ bandas.media`; si no, `baja`.
- Cada decisión recalcula centroides y propuestas. La página dice **cuántas líneas cambiaron de voz** con esa decisión.

### 4.2 La claridad, y el 85 %

```
claridad(audio) = segundos claros / segundos de todas sus líneas publicadas

línea clara  =  declarada por ella OYENDO (confirmada, corregida, dividida,
                o «varios» con al menos dos voces marcadas)
             o  propuesta en banda ALTA, SOLO SI la máquina pasó la prueba:
                 ≥ 8 líneas SORTEADAS y OÍDAS  Y  acierto ≥ 90 %
```

- **Oída** = ella oyó al menos el **70 %** de la línea (la página lo mide mientras suena; antes contaba al empezar a sonar). Lo decidido sin oír es suyo pero **no** es una declaración oyendo: lleva `oida: false`, sale marcado _(sin oír)_ en toda salida, no cuenta para la claridad, no entra en ninguna huella ni en la biblioteca, y no prueba a la máquina.
- **Acierto medido** = de las líneas **sorteadas** en el paso 2 (`origen: "prueba"`) y **oídas**, cuántas confirmó tal cual. Las de «conocer las voces» son las más típicas y las que ella elige a mano no son una muestra: **ninguna de las dos cuenta**. En la prueba no se salta: si no puede decidir, «no se distingue», que cuenta en contra de la máquina.
- Volver a decidir una línea **conserva** la propuesta, la banda y el origen de la primera decisión: si no, la máquina «acertaría» copiándola a ella.
- Donde ella dijo «no se distingue» o «varios» sin dos voces, **la máquina no puede aclarar la línea por su cuenta**.
- Se guarda en cada decisión la propuesta y la banda **de ese momento** (`propuesta_maquina`, `banda_maquina`).
- Si el acierto no llega, **la máquina no suma**: la página lo dice con el número.
- La página muestra la claridad **por grabación y por voz**, y la descompone: cuánto declaró ella, cuánto suma la máquina, cuánto queda dudoso.

### 4.3 Qué revisar primero

1. **Conocer las voces:** 2 líneas típicas de cada voz con más de 20 s — «¿quién es esta voz?».
2. **Poner a prueba a la máquina:** líneas de banda alta **al azar**, hasta 8. Se le dice por qué.
3. **Lo que más aclara:** el resto por `segundos × (1 − margen normalizado)`, primero las que cambian de voz a mitad y las que se pisan.

### 4.4 Estado

`localStorage`, clave `despacho:voces:<clave>`. Se guarda en cada acción; la página muestra «guardado». Si el almacenamiento falla, lo dice y pide exportar. **La fuente de verdad es el archivo exportado** (ADR-022).

## 5. `voces declaradas - <título>.json` — lo que exporta la página, y lee `aplicar`

```json
{
  "formato": "despacho/voces-linea-a-linea", "version": 1,
  "clave": "la del genoma", "titulo": "…",
  "declarado_por": "nombre de quien declaró — OBLIGATORIO",
  "exportado": "ISO 8601",
  "voces": {"v1": {"nombre": "…", "cargo": "…", "como_lo_sabe": "…", "fusionada_en": null},
            "n1": {"nombre": "…", "nueva": true}},
  "lineas": {
    "A1-12": {"decision": "confirmada|corregida|varios|no_se_distingue|descartado",
              "voz": "v1", "voces": ["v1", "v2"],
              "partes": [{"voz": "v1"}, {"voz": "v2"}],
              "propuesta_maquina": "v1", "banda_maquina": "alta",
              "origen": "conocer|prueba|aclarar|rescate|lista|mapa|contexto",
              "oida": true, "fecha": "AAAA-MM-DD"},
    "A2-r3": {"decision": "corregida|no_se_distingue|descartado", "voz": "v2",
              "rescate": true, "se_dijo": true, "texto": "lo que ella oyó y dejó escrito"}
  },
  "maquina": {"A1-13": {"voz": "v2", "banda": "alta", "parecido": 0.91, "margen": 0.12}},
  "resumen": {"claridad": {"A1": 0.87}, "acierto_alta": [29, 30], "maquina_cuenta": true}
}
```

- `voces` con id `n…` son personas nuevas que ella añadió.
- `fusionada_en`: ella declaró que esa voz es la misma persona que otra.
- `partes`: la línea dividida en `cambio.palabra`; cada parte con su voz. En la salida, la segunda parte va en el minuto `cambio.en`.
- Un **rescate** solo entra si ella lo oyó, dijo que se dijo y dejó texto. «No se distingue» en un rescate significa *se dijo, pero no sé quién*, y entra con «?». «Descartado» no afirma que no se dijo: dice que ella no pudo confirmarlo.
- `maquina` trae la propuesta de **todas** las líneas, decididas o no, para que `aplicar` cuente igual que la página.
- **`aplicar` NO se fía de `resumen`**: recalcula el acierto y la claridad desde `lineas` y `maquina`.

## 6. Lo que produce `aplicar`

| Archivo | Para qué |
|---|---|
| `Transcripcion con voces - <Audio> - <fecha>.md` | La transcripción con quién dice cada línea: **✔** declarado, **≈** propuesto, **?** no se distingue. Sin color se sigue distinguiendo |
| `Declaracion de voces - <título> - <fecha>.md` | El registro: quién declaró, quién es cada voz y cómo lo sabe, claridad por grabación contra el 85 %, acierto medido, correcciones |
| `voces por linea - <título> - <fecha>.json` | Lo mismo, para otro programa o para un chat |
| `Biblioteca de voces.json` (`--biblioteca`) | La huella de cada persona **nombrada**, hecha **solo con líneas declaradas** (mínimo 3). La copia anterior va a `_anteriores/` |

Nunca sobrescribe (ADR-011 §8). Sin `declarado_por`, se detiene.

## 7. Lo que NO hace

- No nombra a nadie. Los nombres de `personas_conocidas` y de la biblioteca se **ofrecen**; no se aplican.
- No construye la biblioteca con propuestas de la máquina.
- No convierte una propuesta en declaración por tener un nombre: una línea ≈ con la voz ya nombrada sigue siendo ≈.
