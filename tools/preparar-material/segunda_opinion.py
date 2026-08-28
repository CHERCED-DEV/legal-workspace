#!/usr/bin/env python
"""
segunda-opinion — el unico control que detecta una omision silenciosa.

POR QUE EXISTE
  La confianza de un OCR mide la calidad de lo que leyo, JAMAS la completitud
  de lo que debio leer. Una region que el detector nunca propuso no genera
  caja, ni score, ni entrada: no hay ningun objeto al que asignarle un numero
  bajo. No es un problema de umbral, es de tipo.

  Por eso ninguna instrumentacion de un solo motor puede decir "aqui falto
  texto". Lo unico que lo detecta es una SEGUNDA LECTURA INDEPENDIENTE con
  otra arquitectura, y una alarma donde los dos difieran EN PRESENCIA -no en
  ortografia-.

  ADR-016 §3: la ausencia en el OCR no es informacion sobre el documento.
  Este script es lo que convierte esa regla en un control ejecutable.

LOS DOS MOTORES SE ELIGEN POR TENER MODOS DE FALLO OPUESTOS
  RapidOCR / PaddleOCR : detecta y luego reconoce -> OMITE EN SILENCIO
  Tesseract            : analiza la pagina entera -> PRODUCE BASURA VISIBLE

  Para un uso donde una ausencia se lee como un hecho, fallar ruidosamente es
  una propiedad de seguridad, no un defecto. Un motor que produce basura donde
  el otro produce vacio es una alarma. Dos motores del mismo tipo que ambos
  callan, no.

QUE NO HACE
  - No fusiona las salidas. No elige cual tiene razon. No corrige.
  - No dice cual motor es mejor. Dice DONDE DISCREPAN, que es lo util.
  - No decide nada.

USO
    python segunda_opinion.py CARPETA_DE_IMAGENES [--salida informe.md]
    python segunda_opinion.py CARPETA --tesseract "C:\\ruta\\tesseract.exe"

REQUIERE
    rapidocr-onnxruntime · pillow · Tesseract instalado con el idioma espanol
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

IMAGENES = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}
RUTAS_TESSERACT = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Users\%USERNAME%\Tesseract-OCR\tesseract.exe",
    r"C:\Users\%USERNAME%\AppData\Local\Programs\Tesseract-OCR\tesseract.exe",
]


def localizar_tesseract(dado=None):
    if dado:
        return dado if Path(dado).exists() else None
    hallado = shutil.which("tesseract")
    if hallado:
        return hallado
    for r in RUTAS_TESSERACT:
        r = os.path.expandvars(r)
        if Path(r).exists():
            return r
    return None


def palabras(texto):
    """Palabras significativas, normalizadas. Se ignoran tildes y mayusculas:
    lo que se compara es PRESENCIA, no ortografia — los dos motores escriben
    distinto y eso no es lo que buscamos."""
    t = texto.lower()
    for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ñ", "n"), ("ü", "u")):
        t = t.replace(a, b)
    return {p for p in re.findall(r"[a-z0-9][a-z0-9\.\-]{4,}", t)}


def leer_rapidocr(ocr, ruta):
    res, _ = ocr(str(ruta), box_thresh=0.3, unclip_ratio=2.0, text_score=0.0)
    return "\n".join(x[1] for x in (res or [])), len(res or [])


def leer_tesseract(exe, ruta, idioma="spa"):
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "salida"
        r = subprocess.run([exe, str(ruta), str(base), "-l", idioma, "--psm", "3"],
                           capture_output=True, text=True, timeout=300)
        f = base.with_suffix(".txt")
        if not f.exists():
            return "", 0, (r.stderr or "").strip()[:200]
        t = f.read_text(encoding="utf-8", errors="replace")
        return t, len([l for l in t.splitlines() if l.strip()]), None


def main():
    ap = argparse.ArgumentParser(description="Contraste entre dos motores de OCR.")
    ap.add_argument("carpeta")
    ap.add_argument("--salida", default=None)
    ap.add_argument("--tesseract", default=None)
    ap.add_argument("--idioma", default="spa")
    a = ap.parse_args()

    exe = localizar_tesseract(a.tesseract)
    if not exe:
        print("NO SE ENCONTRO TESSERACT — y sin el, este control no existe.")
        print()
        print("  Instalarlo (Apache-2.0, gratuito, permite uso comercial):")
        print("    winget install --id UB-Mannheim.TesseractOCR")
        print("  Requiere aceptar el dialogo de elevacion de Windows.")
        print()
        print("  Despues, el idioma espanol:")
        print("    descargar spa.traineddata de github.com/tesseract-ocr/tessdata_best")
        print("    y ponerlo en la carpeta tessdata de la instalacion.")
        return 2

    idiomas = subprocess.run([exe, "--list-langs"], capture_output=True, text=True).stdout
    if a.idioma not in idiomas:
        print(f"AVISO: el idioma '{a.idioma}' no esta instalado en Tesseract.")
        print(f"       Idiomas disponibles: {' '.join(idiomas.split()[1:]) or '(ninguno)'}")
        print("       Se continua, pero el reconocimiento sera peor de lo que deberia.")

    try:
        from rapidocr_onnxruntime import RapidOCR
    except ImportError:
        sys.exit("Falta rapidocr-onnxruntime.")
    ctor = dict(max_side_len=4000, det_limit_type="max", det_limit_side_len=2560)
    modelos = Path(__file__).resolve().parent / "modelos"
    if (modelos / "ppocrv5-mobile-rec.onnx").exists():
        ctor.update(rec_model_path=str(modelos / "ppocrv5-mobile-rec.onnx"),
                    rec_keys_path=str(modelos / "ppocrv5_dict.txt"))
    ocr = RapidOCR(**ctor)

    imgs = sorted(p for p in Path(a.carpeta).rglob("*") if p.suffix.lower() in IMAGENES)
    if not imgs:
        sys.exit("No hay imagenes en esa carpeta.")

    print(f"Contrastando {len(imgs)} paginas con dos motores...\n")
    print(f"{'pagina':26s} {'rapid':>6s} {'tess':>6s} {'solo-R':>7s} {'solo-T':>7s}")
    print("-" * 60)
    filas = []
    for img in imgs:
        tr, nr = leer_rapidocr(ocr, img)
        tt, nt, err = leer_tesseract(exe, img, a.idioma)
        pr, pt = palabras(tr), palabras(tt)
        solo_r, solo_t = pr - pt, pt - pr
        filas.append(dict(pagina=img.name, n_r=nr, n_t=nt, solo_r=sorted(solo_r),
                          solo_t=sorted(solo_t), comunes=len(pr & pt), err=err))
        print(f"{img.name[:26]:26s} {nr:6d} {nt:6d} {len(solo_r):7d} {len(solo_t):7d}")

    salida = Path(a.salida) if a.salida else Path(a.carpeta) / "contraste-de-motores.md"
    escribir(salida, filas)
    print(f"\nInforme: {salida}")

    graves = [f for f in filas if len(f["solo_t"]) >= 12]
    if graves:
        print(f"\n{len(graves)} paginas donde el segundo motor vio bastante que el primero NO:")
        for f in graves:
            print(f"   {f['pagina']}: {len(f['solo_t'])} palabras solo en Tesseract")
        print("   Eso es exactamente lo que ninguna instrumentacion de un solo motor detecta.")
    return 0


def escribir(ruta: Path, filas):
    L = ["# Contraste entre dos motores de OCR", "",
         "**Propuesta para su revisión. Esto no dice cuál motor tiene razón: dice dónde discrepan.**", "",
         "Se comparan **presencias, no ortografías**: se ignoran tildes, mayúsculas y palabras cortas, "
         "porque los dos motores escriben distinto y eso no es lo que se busca. Lo que se busca es "
         "**texto que un motor vio y el otro no**.", "",
         "> **Por qué importa:** la confianza de un OCR mide la calidad de lo que leyó, jamás la "
         "completitud de lo que debió leer. Una región que el detector nunca propuso no genera "
         "ninguna señal. **Lo único que detecta una omisión silenciosa es una segunda lectura.**", "",
         "| Página | Líneas motor 1 | Líneas motor 2 | Solo en el 1 | Solo en el 2 | Comunes |",
         "|---|---|---|---|---|---|"]
    for f in filas:
        marca = " ⚠" if len(f["solo_t"]) >= 12 else ""
        L.append(f"| `{f['pagina']}` | {f['n_r']} | {f['n_t']} | {len(f['solo_r'])} "
                 f"| {len(f['solo_t'])}{marca} | {f['comunes']} |")
    L += ["", "## Dónde el segundo motor vio lo que el primero no", "",
          "**Estas son las candidatas a omisión silenciosa del motor principal.** No es prueba de "
          "que falte texto: es dónde mirar.", ""]
    hubo = False
    for f in filas:
        if len(f["solo_t"]) >= 12:
            hubo = True
            L += [f"### `{f['pagina']}` — {len(f['solo_t'])} palabras solo en el segundo motor", "",
                  "```", " · ".join(f["solo_t"][:60]), "```", ""]
    if not hubo:
        L += ["Ninguna página supera el umbral. **Eso no significa que no falte nada**: significa "
              "que los dos motores coinciden en lo que vieron, y **los dos podrían estar omitiendo "
              "lo mismo**.", ""]
    errores = [f for f in filas if f["err"]]
    if errores:
        L += ["## Páginas donde el segundo motor falló", ""]
        for f in errores:
            L.append(f"- `{f['pagina']}`: {f['err']}")
    L += ["", "*Trabajo, no evidencia. Ninguna actuación debería citar este informe.*"]
    ruta.write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
