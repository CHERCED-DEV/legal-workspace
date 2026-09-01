# preparar-material — la tubería de ingesta

Hace de una vez lo que en el primer pase real sobre el expediente [radicado del expediente] fueron **seis pasos a mano**: descomprimir, ordenar, detectar la orientación, calcular huellas, extraer texto, construir el PDF consolidado y escribir el registro de ingesta.

```bash
python preparar_material.py querella1.zip anexos1.zip --caso "Caso de ejemplo" --destino "C:\...\Despacho\Policivo"
```

Crea `1-Documentos recibidos/`, `2-Borradores/` y `3-Para presentar/`, copia los originales **sin modificarlos**, y deja en `2-Borradores/` el registro de ingesta, el texto de referencia y el PDF consolidado.

| Opción | Qué hace |
|---|---|
| `--sin-ocr` | Solo inventario, huellas y PDF |
| `--sin-rotacion` | No prueba las cuatro orientaciones. Más rápido y **peor**: en el material de prueba, sin rotación se detectaron 760 regiones y con ella 809 |
| `--sin-pdf` | No construye el PDF consolidado |

**Requiere:** `pillow`, y `rapidocr-onnxruntime` si se quiere OCR.

---

## Por qué la configuración del OCR es la que es

**No la cambie sin leer esto.** El script usa `max_side_len=4000`, `det_limit_type="max"` y `det_limit_side_len=2560`, y no son valores de gusto.

Con los valores **por defecto** de la librería:

| Parámetro | Defecto | Qué hace en realidad |
|---|---|---|
| `Global.max_side_len` | **2000** | **Reduce la imagen a 2000 px de lado largo antes de mirarla.** Una foto de 4000 px pierde la mitad de su resolución, siempre, en silencio |
| `Det.limit_type` | `min` | Convierte `det_limit_side_len` en un **piso**, no un techo. **Subirlo no hace absolutamente nada** |
| `Global.text_score` | 0,5 | Descarta toda línea reconocida por debajo de esa confianza, **sin avisar ni contarla** |

Los tres borran texto sin dar ningún error. En el pase real esto costó dos días: se probaron cuatro variantes de resolución y tres de preprocesado, todas dieron el mismo resultado, y de ahí se concluyó —**mal**— que la causa era la curvatura del papel. La causa era que la palanca que se estaba moviendo no estaba conectada.

**Medido sobre las mismas 23 fotografías, al corregirlo:**

| | Por defecto | Corregido |
|---|---|---|
| Regiones de texto detectadas | 546 | **711 (+30 %)** |
| Caracteres extraídos | 20.164 | **22.721 (+13 %)** |
| Identificadores críticos correctos | 12 de 12 | **12 de 12** (sin regresión) |
| Frases que la configuración anterior había perdido | — | **3 de 4 recuperadas** |

> **Lección, que vale más que los parámetros:** cuando un experimento da resultado nulo en varias variantes, la primera hipótesis debe ser **que la palanca no está conectada**, no que la causa está en otra parte.

---

## La instrumentación es el punto, no un extra

Por cada página se cuentan **tres números**:

```
regiones detectadas  →  líneas reconocidas  →  líneas devueltas tras el filtro
```

**La diferencia entre la primera y la última es texto que el motor vio y decidió tirar.** Ese número no existía en ninguna parte, y sin él un OCR que falla lo hace en silencio — en un expediente, **una ausencia se lee como un hecho**.

También dice **de qué murió** el texto: si la caída está entre la primera y la segunda columna, murió en la detección; si está entre la segunda y la tercera, en el filtro de confianza. Son dos enfermedades distintas con dos curas distintas.

### El aviso de páginas atípicas no es un umbral de calidad

Se intentó un umbral absoluto —«marcar la página que tire más de un cuarto de lo detectado»— y marcaba **14 de 23**. Antes se había intentado medir qué fracción de la tinta quedaba dentro de una caja, y marcaba **21 de 23**, porque cuenta como tinta los membretes, los logos y las sombras.

**Una alarma que suena siempre no es un control.** Así que el script no compara contra un número inventado: compara cada página **contra la mediana de su propio lote**, con una desviación robusta. Es un detector de atípicas, no un veredicto de calidad, y **la salida lo dice con esas palabras**.

**No existe umbral calibrado.** Cuando lo haya, se cambia; mientras tanto se declara que no lo hay.

### El límite que ninguna instrumentación salva

> **La confianza mide la calidad de lo que se leyó, jamás la completitud de lo que se debió leer.**

Una región que el detector nunca propuso no genera caja, ni confianza, ni entrada: **no hay ningún objeto al que asignarle un número bajo.** No es un problema de umbral, es de tipo.

Por eso el registro que emite este script repite, en su propia salida, la regla de ADR-016: **que algo no aparezca en el texto extraído no significa que no esté en el documento.** Lo único que detecta una omisión silenciosa es una segunda lectura independiente.

---

## Lo que NO hace, y es deliberado

- **No toca los originales.** Los copia y no los modifica. Rotaciones y recortes van sobre copias, fuera de `1-Documentos recibidos/`.
- **No interpreta el contenido.** No dice qué es cada documento ni qué afirma. Eso es trabajo del método, no de un script.
- **No decide nada.** Emite números y los deja a la vista.
- **Arregla los diacríticos solo a medias.** Usa un reconocedor cuyo vocabulario **sí tiene `ñ` minúscula y las tildes** —`señora` sale bien—, pero **no tiene `Ñ` mayúscula, ni `Ú`, ni `¿`, ni `¡`**. En providencias colombianas los encabezados van en mayúsculas, así que **ahí la eñe sigue saliendo mal**. Ver `modelos/PROCEDENCIA.md`.
- **Si el modelo no está en `modelos/`, el script no falla: usa el de la librería y lo declara en el registro**, con las palabras «los diacríticos SALDRÁN MAL». Fallo declarado, nunca silencioso.

## Limitaciones conocidas

- **Sin segunda opinión.** Un solo motor no puede detectar lo que no vio. Falta el paso de contraste con un segundo lector de arquitectura distinta.
- **La detección de orientación cuesta cuatro pasadas de detección por página.** Vale la pena —49 regiones más en el lote de prueba— pero triplica el tiempo.
- **La heurística de foto contra escaneo** se apoya en los metadatos de cámara y en las proporciones. Se declara como heurística en el registro, no como certeza.
- **No procesa PDF ni audio todavía.** Solo imágenes.

## Relación con los ADR

- **ADR-016** — Ingesta de material sin capa de texto. Este script es su implementación: instrumenta la cobertura (§6), declara el modo de captura (§7) y repite el invariante 1 en su salida.
- **ADR-014** — El PDF consolidado es un derivado y **su numeración no es coordenada de cita**.
- **ADR-011** — Los originales se copian con su huella y no se modifican nunca.

---

## `medir_realce.py` — el instrumento, no la mejora

Mide si aclarar la imagen antes del OCR aumenta lo que el reconocedor ve. **No modifica la tubería:** lee, mide y escribe un informe. Existe para que ninguna mejora de imagen entre en producción sin números.

```bash
CASO_RECIBIDOS="/ruta/al/caso/1-Documentos recibidos" python medir_realce.py informe.json
```

Seis variantes contra la pasada actual, con la instrumentación de tres niveles —cajas detectadas, líneas devueltas tras el filtro, caracteres—, más el solapamiento de cajas entre pasadas.

**Lo que midió el 2026-08-31** sobre cinco páginas reales, en `docs/CAPACIDADES-PYTHON-VERIFICADAS.md` §4:

| | |
|---|---|
| Ampliar la imagen al doble | **No sirve.** `det_limit_side_len=2560` la reduce otra vez. La palanca no está conectada |
| Realce de nitidez (CLAHE + suavizado con bordes + máscara de enfoque) | **+11,8 % líneas devueltas, +43,7 % caracteres** — y pierde renglones en otras páginas |
| Cajas detectadas | **Entre −1,9 % y +0,6 %.** El realce **no ayuda a detectar** |
| Solapamiento de cajas entre base y realce | **93 %** |

> **La conclusión que gobierna esta carpeta:** el realce mejora **el reconocimiento**, no **la detección**. **No reduce la omisión silenciosa** que ADR-016 declara, y no sustituye a la segunda opinión de `segunda_opinion.py`. Presentarlo como si lo hiciera sería vender lo contrario de lo que hace.
