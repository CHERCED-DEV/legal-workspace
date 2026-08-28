#!/usr/bin/env python
"""
preparar-material — tuberia de ingesta para el material de un caso.

Hace de una vez lo que en el primer pase real fueron seis pasos a mano:
descomprimir, ordenar, detectar la orientacion, calcular huellas, extraer texto
con OCR instrumentado, construir el PDF consolidado y emitir el registro de
ingesta.

QUE NO HACE, Y ES DELIBERADO
  - No toca los originales. Los copia a 1-Documentos recibidos/ y no los
    modifica nunca. Las rotaciones y recortes se hacen sobre copias.
  - No interpreta el contenido. No dice que es cada documento ni que afirma:
    eso es trabajo del metodo, no de un script.
  - No decide nada. Emite numeros y los deja a la vista.

POR QUE ESTA CONFIGURADO ASI (leer antes de cambiar parametros)
  El paso de OCR usa `max_side_len=4000`, `det_limit_type="max"` y
  `det_limit_side_len=2560`. NO son ajustes arbitrarios. Con los valores por
  defecto de la libreria, `Global.max_side_len=2000` reduce cada imagen a menos
  de la mitad de su resolucion ANTES de mirarla, en silencio, y
  `det_limit_side_len` es un PISO y no un techo, de modo que subirlo no hace
  nada. Medido sobre 23 fotografias reales: la correccion recupero un 30% mas
  de regiones de texto y un 13% mas de caracteres, y rescato dos frases que la
  configuracion por defecto habia perdido sin dar ningun error.

  Ver docs/PLAN-DE-COSTE-Y-PRODUCTIZACION.md §7-bis y ADR-016.

LA INSTRUMENTACION ES EL PUNTO, NO UN EXTRA
  Por cada pagina se cuentan tres numeros: regiones detectadas, lineas
  reconocidas y lineas devueltas tras el filtro de confianza. La diferencia
  entre la primera y la ultima es TEXTO QUE EL MOTOR VIO Y DECIDIO TIRAR.
  Sin ese numero, un OCR que falla lo hace en silencio, y una ausencia se lee
  como un hecho. Con el, el fallo queda declarado.

  Y el limite que ninguna instrumentacion salva, que va escrito en la salida:
  la confianza mide la calidad de lo que se leyo, jamas la completitud de lo
  que se debio leer.

USO
    python preparar_material.py ENTRADA... --caso "Nombre del caso" [opciones]

    ENTRADA puede ser uno o varios .zip, carpetas, o archivos sueltos.

    --destino RUTA        carpeta del despacho (por defecto: junto al script)
    --sin-ocr             solo inventario, huellas y PDF; no extrae texto
    --sin-rotacion        no intenta detectar la orientacion (mas rapido)
    --sin-pdf             no construye el PDF consolidado

REQUIERE
    pillow · rapidocr-onnxruntime (opcional, solo para --con OCR)
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
import time
import zipfile
from datetime import date
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Falta Pillow.  pip install pillow")

IMAGENES = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}
OTROS = {".pdf", ".docx", ".doc", ".txt", ".md", ".rtf", ".odt"}

# Configuracion corregida del OCR. Ver el encabezado de este archivo.
OCR_CTOR = dict(max_side_len=4000, det_limit_type="max", det_limit_side_len=2560)
OCR_CALL = dict(box_thresh=0.3, unclip_ratio=2.0, text_score=0.0)
UMBRAL_DEVUELTA = 0.5  # el filtro que la libreria aplica por defecto

# Reconocedor con vocabulario que incluye la 'n' con virgulilla minuscula y las
# tildes. El modelo por defecto de la libreria NO las tiene en su vocabulario de
# salida -no es fallo de imagen, el simbolo no existe para el modelo-, asi que
# 'senora' nunca puede salir bien. Si estos archivos no estan, el script sigue
# funcionando con el modelo por defecto Y LO DECLARA en el registro.
# Procedencia y medicion: modelos/PROCEDENCIA.md
MODELOS = Path(__file__).resolve().parent / "modelos"
REC_ONNX = MODELOS / "ppocrv5-mobile-rec.onnx"
REC_DICT = MODELOS / "ppocrv5_dict.txt"


# ---------------------------------------------------------------- utilidades

def huella(ruta: Path) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def humano(n: int) -> str:
    for unidad in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.0f} {unidad}" if unidad == "B" else f"{n:.1f} {unidad}"
        n /= 1024
    return f"{n:.1f} TB"


def recolectar(entradas, temporal: Path):
    """Devuelve la lista de archivos, descomprimiendo los .zip que haga falta."""
    archivos = []
    for e in entradas:
        p = Path(e)
        if not p.exists():
            print(f"  AVISO: no existe, se omite: {p}")
            continue
        if p.is_file() and p.suffix.lower() == ".zip":
            destino = temporal / p.stem
            destino.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(p) as z:
                # Nunca extraer fuera del destino (zip-slip).
                for m in z.namelist():
                    if os.path.isabs(m) or ".." in Path(m).parts:
                        print(f"  AVISO: entrada de zip sospechosa, omitida: {m}")
                        continue
                    z.extract(m, destino)
            archivos += [q for q in destino.rglob("*") if q.is_file()]
        elif p.is_dir():
            archivos += [q for q in p.rglob("*") if q.is_file()]
        else:
            archivos.append(p)
    return sorted(archivos)


def modo_de_captura(ruta: Path):
    """Heuristica declarada: distingue foto de escaneo. No es certeza."""
    if ruta.suffix.lower() not in IMAGENES:
        return "no es imagen", None
    try:
        with Image.open(ruta) as im:
            w, h = im.size
            exif = im.getexif()
            marca = exif.get(271) if exif else None      # Make
            modelo = exif.get(272) if exif else None     # Model
    except Exception:
        return "no se pudo abrir", None
    aparato = " ".join(x for x in (marca, modelo) if x) or None
    if aparato:
        return "FOTOGRAFIA (el archivo declara camara)", (w, h, aparato)
    if max(w, h) > 2400 and abs((w / h) - (4 / 3)) < 0.25:
        return "probable fotografia", (w, h, None)
    return "probable escaneo", (w, h, None)


def atipicas(cobertura):
    """Paginas que tiran mucho mas que sus companeras DE ESTE MISMO LOTE.

    No existe umbral absoluto calibrado que separe una pagina mal leida de una
    normal. Se intento uno -medir que fraccion de la tinta quedaba dentro de una
    caja- y marcaba 21 de 23 paginas, porque cuenta como tinta los membretes,
    los logos y las sombras. Una alarma que suena siempre no es un control.

    Asi que aqui no se compara contra un numero inventado: se compara cada
    pagina contra la mediana del lote. Es un detector de atipicas, no un
    veredicto de calidad, y la salida lo dice con esas palabras.
    """
    tasas = [(p, p["tiradas"] / p["cajas"]) for p in cobertura if p["cajas"]]
    if len(tasas) < 5:
        return []
    orden = sorted(t for _, t in tasas)
    mediana = orden[len(orden) // 2]
    # desviacion absoluta mediana: robusta, no la arrastra un solo caso extremo
    desv = sorted(abs(t - mediana) for t in orden)[len(orden) // 2] or 0.05
    return [p for p, t in tasas if t > mediana + 3 * desv]


def mejor_orientacion(ocr, ruta: Path):
    """Prueba las cuatro orientaciones y devuelve la que mas texto detecta."""
    from PIL import Image as I
    import numpy as np
    mejor, giros = (-1, 0), {0: None, 90: I.ROTATE_270, 180: I.ROTATE_180, 270: I.ROTATE_90}
    with I.open(ruta) as base:
        base = base.convert("RGB")
        for grados, op in giros.items():
            img = base if op is None else base.transpose(op)
            cajas, _ = ocr(np.asarray(img), use_rec=False, **OCR_CALL)
            n = len(cajas) if cajas is not None else 0
            if n > mejor[0]:
                mejor = (n, grados)
    return mejor[1], mejor[0]


# ------------------------------------------------------------------- proceso

def main():
    ap = argparse.ArgumentParser(description="Tuberia de ingesta del material de un caso.")
    ap.add_argument("entradas", nargs="+", help="zips, carpetas o archivos")
    ap.add_argument("--caso", required=True, help="nombre de la carpeta del caso")
    ap.add_argument("--destino", default=".", help="carpeta del despacho")
    ap.add_argument("--sin-ocr", action="store_true")
    ap.add_argument("--sin-rotacion", action="store_true")
    ap.add_argument("--sin-pdf", action="store_true")
    a = ap.parse_args()

    caso = Path(a.destino) / a.caso
    recibidos = caso / "1-Documentos recibidos"
    borradores = caso / "2-Borradores"
    temporal = caso / ".temporal-ingesta"
    for d in (recibidos, borradores, caso / "3-Para presentar", temporal):
        d.mkdir(parents=True, exist_ok=True)
    derivados = temporal / "derivados"
    derivados.mkdir(exist_ok=True)

    print(f"Caso: {caso}")
    print("Recolectando...")
    archivos = recolectar(a.entradas, temporal)
    if not archivos:
        sys.exit("No se encontro ningun archivo.")

    # --- copiar a 1-Documentos recibidos, sin tocar los originales -----------
    print(f"Copiando {len(archivos)} archivos a '1-Documentos recibidos'...")
    piezas, vistos = [], {}
    for f in archivos:
        hh = huella(f)
        destino = recibidos / f.name
        n = 1
        while destino.exists() and huella(destino) != hh:
            destino = recibidos / f"{f.stem}_{n}{f.suffix}"
            n += 1
        if not destino.exists():
            shutil.copy2(f, destino)
        modo, dims = modo_de_captura(destino)
        piezas.append({
            "archivo": destino.name, "bytes": destino.stat().st_size,
            "sha256": hh, "modo": modo,
            "ancho": dims[0] if dims else None, "alto": dims[1] if dims else None,
            "aparato": dims[2] if dims else None,
            "duplicado_de": vistos.get(hh),
        })
        vistos.setdefault(hh, destino.name)

    duplicados = [p for p in piezas if p["duplicado_de"]]
    imagenes = [p for p in piezas if Path(p["archivo"]).suffix.lower() in IMAGENES]
    print(f"  {len(piezas)} piezas · {len(imagenes)} imagenes · {len(duplicados)} duplicados exactos")

    # --- OCR instrumentado ---------------------------------------------------
    ocr, cobertura, reconocedor = None, [], "no se ejecuto OCR"
    if not a.sin_ocr and imagenes:
        try:
            from rapidocr_onnxruntime import RapidOCR
            import numpy as np
            ctor = dict(OCR_CTOR)
            if REC_ONNX.exists() and REC_DICT.exists():
                ctor.update(rec_model_path=str(REC_ONNX), rec_keys_path=str(REC_DICT))
                reconocedor = "PP-OCRv5 (vocabulario con tildes y n con virgulilla minuscula)"
            else:
                reconocedor = ("POR DEFECTO de la libreria — su vocabulario NO tiene n con "
                               "virgulilla ni signos de apertura: los diacriticos SALDRAN MAL")
                print(f"  AVISO: {reconocedor}")
                print(f"  Reponer con: ver {MODELOS / 'PROCEDENCIA.md'}")
            ocr = RapidOCR(**ctor)
        except ImportError:
            print("  AVISO: rapidocr-onnxruntime no esta instalado. Se omite el OCR.")
    if ocr:
        print("Extrayendo texto (con instrumentacion de cobertura)...")
        from PIL import Image as I
        import numpy as np
        t0 = time.time()
        for p in imagenes:
            ruta = recibidos / p["archivo"]
            giro, _ = (0, 0) if a.sin_rotacion else mejor_orientacion(ocr, ruta)
            with I.open(ruta) as im:
                im = im.convert("RGB")
                if giro:
                    im = im.rotate(-giro, expand=True)
                arr = np.asarray(im)
                im.save(derivados / f"{Path(p['archivo']).stem}.jpg", quality=90)
            cajas, _ = ocr(arr, use_rec=False, **OCR_CALL)
            n_cajas = len(cajas) if cajas is not None else 0
            res, _ = ocr(arr, **OCR_CALL)
            n_rec = len(res) if res else 0
            n_dev = sum(1 for x in (res or []) if float(x[2]) >= UMBRAL_DEVUELTA)
            texto = "\n".join(x[1] for x in (res or []))
            (temporal / f"{Path(p['archivo']).stem}.txt").write_text(texto, encoding="utf-8")
            p.update(giro=giro, cajas=n_cajas, reconocidas=n_rec, devueltas=n_dev,
                     tiradas=n_cajas - n_dev, caracteres=len(texto))
            cobertura.append(p)
        print(f"  {len(cobertura)} paginas en {time.time()-t0:.0f}s")

    # --- texto de referencia -------------------------------------------------
    if cobertura:
        partes = ["TEXTO DE REFERENCIA — extraido automaticamente", "",
                  "NO ES CITABLE COMO LITERAL. Sirve para buscar dentro del material.",
                  "LA AUSENCIA DE ALGO AQUI NO SIGNIFICA QUE NO ESTE EN EL DOCUMENTO.", "",
                  "=" * 70, ""]
        for p in cobertura:
            partes += ["#" * 70, f"### {p['archivo']}", "#" * 70,
                       (temporal / f"{Path(p['archivo']).stem}.txt").read_text(encoding="utf-8"), ""]
        (borradores / f"Texto de referencia - {date.today()}.txt").write_text(
            "\n".join(partes), encoding="utf-8")

    # --- PDF consolidado -----------------------------------------------------
    if not a.sin_pdf and cobertura:
        try:
            from PIL import Image as I, ImageDraw, ImageFont
            try:
                f1 = ImageFont.truetype("arialbd.ttf", 28); f2 = ImageFont.truetype("arial.ttf", 22)
            except Exception:
                f1 = f2 = ImageFont.load_default()
            paginas = []
            for i, p in enumerate(cobertura, 1):
                with I.open(derivados / f"{Path(p['archivo']).stem}.jpg") as im:
                    im = im.convert("RGB")
                    nw = 1700; nh = int(im.height * nw / im.width)
                    im = im.resize((nw, nh), I.LANCZOS)
                    lienzo = I.new("RGB", (nw, nh + 80), "white")
                    lienzo.paste(im, (0, 0))
                    d = ImageDraw.Draw(lienzo)
                    d.line([(30, nh + 8), (nw - 30, nh + 8)], fill=(120, 120, 120), width=2)
                    d.text((30, nh + 18), f"{i:02d}  ·  {p['archivo']}", font=f1, fill=(20, 40, 90))
                    d.text((30, nh + 50), f"sha256 {p['sha256'][:16]}", font=f2, fill=(110, 110, 110))
                    paginas.append(lienzo)
            salida = borradores / f"0 - Material completo - {len(paginas)} paginas - {date.today()}.pdf"
            paginas[0].save(salida, "PDF", resolution=150, save_all=True, append_images=paginas[1:])
            print(f"  PDF: {salida.name} ({humano(salida.stat().st_size)})")
        except Exception as e:
            print(f"  AVISO: no se pudo construir el PDF: {e}")

    escribir_registro(borradores, caso, piezas, cobertura, duplicados, reconocedor)
    json.dump(piezas, open(borradores / f"ingesta-{date.today()}.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    shutil.rmtree(temporal, ignore_errors=True)

    if cobertura:
        tot_c = sum(p["cajas"] for p in cobertura)
        tot_d = sum(p["devueltas"] for p in cobertura)
        print(f"\nCOBERTURA: {tot_c} regiones detectadas · {tot_d} devueltas · "
              f"{tot_c - tot_d} tiradas ({100*(tot_c-tot_d)/max(tot_c,1):.0f}%)")
        print("  El umbral que separa una pagina mala de una normal NO esta calibrado.")
        print("  Se senalan las atipicas RESPECTO DE ESTE LOTE, no contra un valor absoluto.")
        for p in atipicas(cobertura):
            print(f"   ATIPICA  {p['archivo']}: tiro {p['tiradas']} de {p['cajas']} "
                  f"({100*p['tiradas']/max(p['cajas'],1):.0f}%)")
    print(f"\nListo. Registro en: {borradores}")


def escribir_registro(borradores: Path, caso: Path, piezas, cobertura, duplicados, reconocedor="—"):
    L = [f"# REGISTRO DE INGESTA — {caso.name}", "",
         f"Generado el {date.today()} por `preparar_material.py`. "
         "**Propuesta para su revisión. Nada de esto está comprobado por ningún sistema.**", "",
         "## 1. Qué llegó", "",
         "| Archivo | Tamaño | Modo de captura | sha256 (16) |", "|---|---|---|---|"]
    for p in piezas:
        L.append(f"| `{p['archivo']}` | {humano(p['bytes'])} | {p['modo']} | `{p['sha256'][:16]}` |")
    L += ["", f"**{len(piezas)} piezas.**"]
    if duplicados:
        L += ["", "**Duplicados exactos** (misma huella):", ""]
        for p in duplicados:
            L.append(f"- `{p['archivo']}` es copia de `{p['duplicado_de']}`")
    fotos = [p for p in piezas if "FOTOGRAF" in p["modo"].upper() or "fotografia" in p["modo"]]
    if fotos:
        L += ["", f"> **{len(fotos)} de {len(piezas)} piezas parecen fotografías, no escaneos.** "
              "Eso multiplica el coste de leerlas y obliga a marcar como *por comprobar* todo dato "
              "numérico. Ver `docs/INSTRUCCION-DE-CAPTURA-DEL-MATERIAL.md`."]
    if cobertura:
        atip = atipicas(cobertura)
        L += ["", "## 2. Cómo se leyó, y cuánto se leyó", "",
              f"**Reconocedor usado:** {reconocedor}", "",
              "Tres números por página. **La diferencia entre lo detectado y lo devuelto es texto "
              "que el motor vio y decidió tirar.**", "",
              "| Página | Giro | Detectadas | Devueltas | Tiradas | Caracteres |", "|---|---|---|---|---|---|"]
        for p in cobertura:
            marca = " ⚠" if p in atip else ""
            L.append(f"| `{p['archivo']}` | {p['giro']}° | {p['cajas']} | {p['devueltas']} "
                     f"| {p['tiradas']}{marca} | {p['caracteres']} |")
        tc = sum(p["cajas"] for p in cobertura); td = sum(p["devueltas"] for p in cobertura)
        L += ["", f"**Total: {tc} detectadas · {td} devueltas · {tc-td} tiradas "
              f"({100*(tc-td)/max(tc,1):.0f}%).**", "",
              "Las páginas marcadas ⚠ son **atípicas respecto de este lote**, no respecto de un "
              "umbral de calidad: **no existe umbral calibrado** que separe una página mal leída de "
              "una normal, y fabricar uno produciría una alarma que suena siempre. Se comparan contra "
              "la mediana del propio lote.", "",
              "### El límite que estos números NO cubren", "",
              "> **La confianza mide la calidad de lo que se leyó, jamás la completitud de lo que se "
              "debió leer.** Una región que el detector nunca propuso no genera caja, ni confianza, "
              "ni entrada: no hay nada a lo que asignarle un número bajo. **No es un problema de "
              "umbral: es de tipo.**", "",
              "Por eso: **que algo no aparezca en el texto extraído no significa que no esté en el "
              "documento.** Lo único que detecta una omisión silenciosa es una segunda lectura "
              "independiente — otro motor, u ojos.", ""]
    L += ["", "## 3. Qué se hizo y qué no", "",
          "- Los originales se copiaron a `1-Documentos recibidos/` y **no se modificaron**.",
          "- Las rotaciones se hicieron sobre copias, fuera de esa carpeta.",
          "- **No se interpretó ningún contenido.** Este registro no dice qué es cada documento.",
          "", "*Trabajo, no evidencia. Ninguna actuación debería citar este registro como origen "
          "de un hecho: el origen son los documentos.*"]
    (borradores / f"Registro de ingesta - {date.today()}.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()
