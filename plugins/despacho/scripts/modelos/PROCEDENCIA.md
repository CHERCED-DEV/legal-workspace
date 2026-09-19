# Modelos de reconocimiento — de dónde salieron

**No se versionan en git** (ver `.gitignore`): son binarios de terceros.
Este archivo existe para que se sepa **qué se descargó, de dónde y por qué**, conforme a
ADR-011 §7 (todo derivado declara su receta) y ADR-016 §9 (cambiar de reconocedor produce
versión nueva, no sobrescribe).

| Archivo | Para qué | Origen | Descargado |
|---|---|---|---|
| `ppocrv5-mobile-rec.onnx` (16,5 MB) | Texto en imágenes | `huggingface.co/bukuroo/PPOCRv5-ONNX` | 2026-08-28 |
| `ppocrv5_dict.txt` (18.383 caracteres) | ídem | mismo repositorio | 2026-08-28 |
| `pyannote-segmentation-3-0.onnx` (6,0 MB) | Dónde hay voz y dónde cambia | `github.com/k2-fsa/sherpa-onnx`, publicación `speaker-segmentation-models` | 2026-09-18 |
| `wespeaker-voxceleb-CAMPP.onnx` (29,3 MB) | Huella de voz, para agrupar hablantes | mismo repositorio, publicación `speaker-recongition-models` | 2026-09-18 |

`sha256`, primeros 32:

- `ppocrv5-mobile-rec.onnx` → `bf66820f48fa99f779974c4df78e5274`
- `pyannote-segmentation-3-0.onnx` → `220ad67ca923bef2fa91f2390c786097`
- `wespeaker-voxceleb-CAMPP.onnx` → `c46fad10b5f81e1aa4a60c1627142085`

---

# Los dos modelos de voz (separación de hablantes)

## Por qué estos y no `pyannote.audio`

`pyannote.audio` es el estándar, pero **exige PyTorch** (unos 2,5 GB), una cuenta en Hugging Face
y aceptar condiciones de uso modelo por modelo. Estos dos corren sobre `onnxruntime`, que **ya
estaba instalado**, pesan 35 MB entre los dos y no requieren cuenta ninguna. El motor es
`sherpa-onnx` (2,3 MB).

El modelo de huella de voz está entrenado sobre **VoxCeleb**, que es material en inglés. Se eligió
por encima de las alternativas de 3D-Speaker —entrenadas sobre chino y chino-inglés— porque una
huella de voz modela **el timbre, no el idioma**; aun así **esto no está medido sobre español
colombiano**, y es una limitación real de la que hay que hablar.

## Qué se midió al calibrarlo (7 min 16 s de reunión real, 2026-09-18)

El umbral de agrupamiento decide cuántas voces distintas se cree que hay. **Es el parámetro que
más daño puede hacer**, porque inventar hablantes inventa personas:

| Umbral | Voces detectadas | Con 15 s o más | % del habla en esas |
|---|---|---|---|
| 0,60 | **12** | 4 | 92,1 % |
| 0,75 | 7 | 2 | 93,2 % |
| **0,90 (el elegido)** | **4** | **3** | **97,8 %** |
| 1,05 | 2 | 2 | 100 % — **funde personas distintas** |

Con 0,60 aparecen voces de menos de tres segundos que no son nadie. Con 1,05 dos personas
distintas quedan como una sola. **0,90 es el punto donde deja de inventar sin empezar a fundir.**

Velocidad medida: **5,7 × tiempo real** en la GPU de esta máquina.

## Lo que sigue roto, y hay que saberlo

**No hay verdad de referencia.** Nadie ha marcado a mano quién habla en estas grabaciones, así que
**no se sabe qué porcentaje de las asignaciones es correcto**. Lo único medido es cuántas voces
salen con cada umbral, que no es lo mismo.

Y la regla que no cambia con ningún umbral: **un número de hablante es una voz estimada, no una
persona identificada.** Que dos líneas lleven el mismo número **no prueba** que las dijera la
misma persona, y ponerle un nombre a una voz **no lo hace este método jamás**.

## Cómo reponerlos

    curl -L -o seg.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/speaker-segmentation-models/sherpa-onnx-pyannote-segmentation-3-0.tar.bz2
    # extraer model.onnx y renombrarlo a pyannote-segmentation-3-0.onnx
    curl -L -o wespeaker-voxceleb-CAMPP.onnx "https://github.com/k2-fsa/sherpa-onnx/releases/download/speaker-recongition-models/wespeaker_en_voxceleb_CAM%2B%2B.onnx"

*(La errata `recongition` está en el repositorio de origen, no aquí.)*

---

# El modelo de texto en imágenes

## Por qué este y no el que trae la librería

El modelo por defecto de `rapidocr-onnxruntime` es `ch_PP-OCRv4_rec_infer.onnx`, cuyo
diccionario de 6.623 caracteres **no contiene `ñ`, `Ñ`, `¿` ni `¡`**. No es un fallo de
imagen: el modelo no tiene esos símbolos en su vocabulario de salida, así que
`señora` sale `senora` y **ningún ajuste de imagen puede cambiarlo**.

## Qué se midió al cambiarlo (23 fotografías reales, 2026-08-28)

| | v4 (por defecto) | v5 (este) |
|---|---|---|
| Caracteres acentuados en la salida | ~0 | **124** |
| Identificadores críticos correctos | 12 de 12 | **12 de 12** — sin regresión |
| Regiones detectadas | 711 | 711 — la detección no cambia |
| Caracteres totales | 22.721 | 21.650 |

## Lo que sigue roto, y hay que saberlo

El diccionario del v5 **tiene `ñ` minúscula pero NO tiene `Ñ` mayúscula**, ni `Ú`, ni `¿`, ni `¡`.

> **En providencias colombianas los encabezados van en mayúsculas** —«SEÑOR», «AÑO», «DAÑO»—,
> así que ahí la eñe **sigue saliendo mal**. Para eso hace falta un modelo latino
> (`ppocrv5_latin_dict.txt`, 502 caracteres, con los cuatro), que solo se distribuye
> en ModelScope y **no fue alcanzable desde esta máquina**. Queda pendiente.

Y la regla que no cambia con ningún modelo: **este texto no es citable como literal.**
Sirve para buscar dentro del material y para cotejar cifras.

## Cómo reponerlos

    curl -L -o ppocrv5-mobile-rec.onnx https://huggingface.co/bukuroo/PPOCRv5-ONNX/resolve/main/ppocrv5-mobile-rec.onnx
    curl -L -o ppocrv5_dict.txt        https://huggingface.co/bukuroo/PPOCRv5-ONNX/resolve/main/ppocrv5_dict.txt
