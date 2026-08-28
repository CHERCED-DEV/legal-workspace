# Modelos de reconocimiento — de dónde salieron

**No se versionan en git** (ver `.gitignore`): pesan 16 MB y son binarios de terceros.
Este archivo existe para que se sepa **qué se descargó, de dónde y por qué**, conforme a
ADR-011 §7 (todo derivado declara su receta) y ADR-016 §9 (cambiar de reconocedor produce
versión nueva, no sobrescribe).

| Archivo | Origen | Descargado |
|---|---|---|
| `ppocrv5-mobile-rec.onnx` (16,5 MB) | `huggingface.co/bukuroo/PPOCRv5-ONNX` | 2026-08-28 |
| `ppocrv5_dict.txt` (18.383 caracteres) | mismo repositorio | 2026-08-28 |

`sha256` del modelo, primeros 32: `bf66820f48fa99f779974c4df78e5274`

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
