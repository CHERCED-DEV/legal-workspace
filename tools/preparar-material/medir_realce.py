# -*- coding: utf-8 -*-
"""Mide si el realce de imagen aumenta lo que el OCR ve, sobre el material real.

No toca 1-Documentos recibidos: lee, trabaja en memoria, escribe solo el informe.
Instrumentacion de tres niveles, la misma de preparar_material.py:
  cajas detectadas -> lineas reconocidas -> lineas devueltas tras el filtro.
"""
import os, sys, time, json
from pathlib import Path
import numpy as np
import cv2
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
CASO = Path(os.environ.get("CASO_RECIBIDOS", "")).expanduser()
MODELOS = REPO / "tools" / "preparar-material" / "modelos"
SALIDA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("informe_realce.json")

OCR_CTOR = dict(max_side_len=4000, det_limit_type="max", det_limit_side_len=2560)
OCR_CALL = dict(box_thresh=0.3, unclip_ratio=2.0, text_score=0.0)
UMBRAL = 0.5

# Cinco paginas bastan: la variacion entre paginas es mayor que entre variantes.
MUESTRA = sorted(CASO.rglob("*.jpg"))[:5] if CASO.exists() else []


# ---------------------------------------------------------------- variantes
def v_base(a):
    return a


def v_clahe(a):
    lab = cv2.cvtColor(a, cv2.COLOR_RGB2LAB)
    l, u, v = cv2.split(lab)
    l = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(l)
    return cv2.cvtColor(cv2.merge((l, u, v)), cv2.COLOR_LAB2RGB)


def v_x2(a):
    h, w = a.shape[:2]
    return cv2.resize(a, (w * 2, h * 2), interpolation=cv2.INTER_LANCZOS4)


def v_clahe_x2(a):
    return v_x2(v_clahe(a))


def v_nitidez(a):
    """CLAHE + reduccion de ruido preservando bordes + mascara de enfoque."""
    b = v_clahe(a)
    b = cv2.bilateralFilter(b, 7, 50, 50)
    borroso = cv2.GaussianBlur(b, (0, 0), 3)
    return cv2.addWeighted(b, 1.6, borroso, -0.6, 0)


def v_enderezar(a):
    """Corrige inclinacion global por el angulo dominante de las lineas de texto."""
    g = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
    g = cv2.bitwise_not(g)
    th = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    co = np.column_stack(np.where(th > 0))
    if len(co) < 100:
        return a
    ang = cv2.minAreaRect(co.astype(np.float32))[-1]
    if ang < -45:
        ang = 90 + ang
    if abs(ang) > 15:          # giro absurdo: no es inclinacion, es otra cosa
        return a
    h, w = a.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), ang, 1.0)
    return cv2.warpAffine(a, M, (w, h), flags=cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_REPLICATE)


def v_enderezar_clahe_x2(a):
    return v_x2(v_clahe(v_enderezar(a)))


VARIANTES = [
    ("A base", v_base),
    ("B clahe", v_clahe),
    ("C x2", v_x2),
    ("D clahe+x2", v_clahe_x2),
    ("E nitidez", v_nitidez),
    ("F enderezar+clahe+x2", v_enderezar_clahe_x2),
]


# ---------------------------------------------------------------- medicion
def medir(ocr, arr):
    t0 = time.time()
    cajas, _ = ocr(arr, use_rec=False, **OCR_CALL)
    res, _ = ocr(arr, **OCR_CALL)
    conf = [float(x[2]) for x in (res or [])]
    texto = "\n".join(x[1] for x in (res or []))
    return dict(
        alto=int(arr.shape[0]), ancho=int(arr.shape[1]),
        cajas=len(cajas) if cajas is not None else 0,
        reconocidas=len(res or []),
        devueltas=sum(1 for c in conf if c >= UMBRAL),
        caracteres=len(texto),
        conf_mediana=round(float(np.median(conf)), 3) if conf else 0.0,
        segundos=round(time.time() - t0, 1),
    )


def main():
    from rapidocr_onnxruntime import RapidOCR
    ctor = dict(OCR_CTOR)
    rec, dic = MODELOS / "ppocrv5-mobile-rec.onnx", MODELOS / "ppocrv5_dict.txt"
    if rec.exists() and dic.exists():
        ctor.update(rec_model_path=str(rec), rec_keys_path=str(dic))
        print("reconocedor: PP-OCRv5")
    else:
        print("AVISO: reconocedor por defecto — los diacriticos saldran mal")
    ocr = RapidOCR(**ctor)

    filas = []
    for ruta in MUESTRA:
        if not ruta.exists():
            print("FALTA", ruta)
            continue
        with Image.open(ruta) as im:
            base = np.asarray(im.convert("RGB").rotate(-270, expand=True))
        print(f"\n{ruta.name}  {base.shape[1]}x{base.shape[0]}")
        for nombre, fn in VARIANTES:
            try:
                m = medir(ocr, fn(base.copy()))
            except Exception as e:
                print(f"  {nombre:24s} FALLO: {e}")
                continue
            m.update(archivo=ruta.name, variante=nombre)
            filas.append(m)
            print(f"  {nombre:24s} {m['ancho']:5d}x{m['alto']:<5d} "
                  f"cajas={m['cajas']:4d} dev={m['devueltas']:4d} "
                  f"car={m['caracteres']:6d} conf={m['conf_mediana']:.3f} "
                  f"{m['segundos']:5.1f}s")

    SALIDA.write_text(json.dumps(filas, ensure_ascii=False, indent=1), encoding="utf-8")

    print("\n" + "=" * 78)
    print("RESUMEN — suma sobre la muestra, y variacion frente a A base")
    print("=" * 78)
    base = {}
    for n, _ in VARIANTES:
        s = [f for f in filas if f["variante"] == n]
        if not s:
            continue
        tot = {k: sum(f[k] for f in s) for k in ("cajas", "devueltas", "caracteres")}
        tot["conf"] = float(np.mean([f["conf_mediana"] for f in s]))
        tot["seg"] = sum(f["segundos"] for f in s)
        if n == "A base":
            base = tot
        d = lambda k: (100.0 * (tot[k] - base[k]) / base[k]) if base.get(k) else 0.0
        print(f"{n:24s} cajas={tot['cajas']:5d} ({d('cajas'):+6.1f}%)  "
              f"dev={tot['devueltas']:5d} ({d('devueltas'):+6.1f}%)  "
              f"car={tot['caracteres']:6d} ({d('caracteres'):+6.1f}%)  "
              f"conf={tot['conf']:.3f}  {tot['seg']:5.0f}s")
    print(f"\ninforme: {SALIDA}")


if __name__ == "__main__":
    main()
