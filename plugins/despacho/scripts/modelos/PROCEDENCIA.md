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
**Comprobado sobre el archivo, el 2026-09-05:** 18.383 caracteres, y esos cuatro no están.

> **En providencias colombianas los encabezados van en mayúsculas** —«SEÑOR», «AÑO», «DAÑO»—,
> así que ahí la eñe **sigue saliendo mal**. Un carácter que no está en el vocabulario
> **no sale nunca**: no es un problema de imagen y ningún ajuste lo arregla.

## El modelo latino: sí es alcanzable, y este documento decía que no

> **CORRECCIÓN — 2026-09-05.** Este apartado decía que el modelo latino
> *«solo se distribuye en ModelScope y no fue alcanzable desde esta máquina»*, y que su
> diccionario tenía **502 caracteres**. **Las dos cosas son falsas**, comprobadas hoy
> bajando los archivos:

| | Lo que decía | Lo comprobado el 2026-09-05 |
|---|---|---|
| Dónde está | Solo ModelScope, inalcanzable | **Hugging Face: `PaddlePaddle/latin_PP-OCRv5_mobile_rec_onnx`**, bajado sin problema |
| Licencia | no constaba | **Apache-2.0** — permite cobrar, que es la regla de este proyecto |
| Tamaño del diccionario | 502 caracteres | **836** |
| Los cuatro rotos | «con los cuatro» | **Tres de cuatro:** trae `Ñ`, `Ú` y `¿`. **`¡` tampoco está ahí** |
| Tamaño del modelo | no constaba | 8,0 MB — **la mitad** que el general (16,5 MB) |

**Y trae además** las mayúsculas acentuadas `Á É Í Ó`, la `Ü`, y `« » º ª`.

### Cómo se traen los dos, sin volver a buscarlos

```bash
python plugins/despacho/scripts/traer_modelos.py            # el general
python plugins/despacho/scripts/traer_modelos.py --latino   # además el latino
```

El programa baja, **extrae el diccionario del `.yml`** —que es donde el export ONNX de
Paddle lo mete— y **dice qué caracteres del español faltan**. Nada de esto se versiona.

### Por qué NO se ha adoptado el latino, y no es pereza

**Cambiar de reconocedor es versión nueva, no sobrescritura** (ADR-016 §9). El general
está medido sobre **23 fotografías reales**: 124 caracteres acentuados y **12 de 12
identificadores críticos sin regresión**. El latino **no está medido sobre ninguna**.

> **Un modelo con mejor vocabulario puede reconocer peor**, y esos 12 identificadores
> —las cifras y matrículas de las que cuelga un expediente— son justo lo que no se puede
> perder por ganar una eñe. **Adoptarlo exige repetir la medida, y para eso hacen falta
> fotografías reales, que no están en este repositorio.**

**Lo que sí queda cerrado hoy:** ya no hay que buscar el modelo, ni dudar de su licencia,
ni suponer su diccionario. Lo que falta es medir.

Y la regla que no cambia con ningún modelo: **este texto no es citable como literal.**
Sirve para buscar dentro del material y para cotejar cifras.

## Cómo reponerlos

    curl -L -o ppocrv5-mobile-rec.onnx https://huggingface.co/bukuroo/PPOCRv5-ONNX/resolve/main/ppocrv5-mobile-rec.onnx
    curl -L -o ppocrv5_dict.txt        https://huggingface.co/bukuroo/PPOCRv5-ONNX/resolve/main/ppocrv5_dict.txt
