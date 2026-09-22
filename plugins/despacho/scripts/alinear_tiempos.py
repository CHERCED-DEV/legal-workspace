# -*- coding: utf-8 -*-
"""alinear_tiempos — que la marca de tiempo caiga donde empieza la voz.

    python alinear_tiempos.py <audio> <datos.json> [--salida nuevos.json]

El producto entero promete una cosa: **pulsa el minuto y suena lo que dice esa
linea**. Si la marca cae antes, suena el final de la frase anterior; si cae
despues, se pierde el arranque. Esa marca la pone el reconocedor por su cuenta,
y nadie habia comprobado si acierta.

COMO SE MIDE SIN UNA VERDAD HUMANA. Un detector de voz dice donde hay habla y
donde no. Con eso cada arranque cae en uno de tres casos, y solo dos se pueden
juzgar:

  1. EN SILENCIO      -- la linea empieza donde no habla nadie. Esta mal, y es
                         objetivo: no hace falta que nadie escuche para saberlo.
  2. ABRE RACHA TARDE -- la linea es la primera de una racha de habla pero su
                         marca cae despues del comienzo: al pulsarla ya se han
                         dicho las primeras silabas.
  3. EN MITAD DEL HABLA -- el detector NO opina. Solo dice que ahi hay voz, no
                         si es esta frase o la anterior. Es el caso mayoritario
                         cuando la gente se pisa, y es justo el que necesitaria
                         alineacion forzada por CTC para juzgarse.

QUE ARREGLA. Los casos 1 y 2, moviendo el arranque al comienzo de la racha,
nunca mas de la ventana que se le diga y nunca por detras del final de la linea
anterior. El caso 3 lo deja intacto y lo cuenta, porque cuantas lineas caen ahi
es lo que dira si merece la pena traer un modelo nuevo de 2,5 GB.

NUNCA sobrescribe (ADR-011 §8) y NUNCA toca el texto: solo numeros de tiempo.
"""
import argparse, io, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

EN_SILENCIO, ABRE_RACHA, EN_MITAD = "silencio", "abre", "mitad"


def falla(msg):
    sys.stderr.write("\nDETENIDO: " + msg + "\n")
    raise SystemExit(2)


def hms(s):
    s = max(0, float(s or 0))
    return "%02d:%02d:%02d" % (s // 3600, (s % 3600) // 60, s % 60)


def habla(x):
    """Tramos con voz, SIN margenes: para juzgar arranques hacen falta bordes
    apretados. La tuberia usa margen de 400 ms a proposito -- para no cortar
    habla al transcribir --, y ese margen aqui estorbaria."""
    from faster_whisper.vad import VadOptions, get_speech_timestamps
    op = VadOptions(threshold=0.5, min_speech_duration_ms=60,
                    min_silence_duration_ms=120, speech_pad_ms=0)
    return [(t["start"] / 16000.0, t["end"] / 16000.0) for t in get_speech_timestamps(x, op)]


def clasificar(segs, tramos):
    """Por cada linea: (caso, comienzo de racha al que deberia ir, desfase).

    Desfase positivo = la marca va tarde; negativo = va adelantada."""
    fuera = []
    fin_previo = 0.0
    for s in segs:
        t = s["inicio"]
        dentro = next(((a, b) for a, b in tramos if a <= t <= b), None)
        if dentro is None:
            # En silencio: al comienzo de habla mas cercano que no invada la
            # linea anterior ni se salga de esta.
            cand = [a for a, _ in tramos if a >= fin_previo - 0.02 and a < s["fin"]]
            ancla = min(cand, key=lambda c: abs(c - t)) if cand else None
            fuera.append((EN_SILENCIO, ancla, (ancla - t) if ancla is not None else None))
        elif dentro[0] >= fin_previo - 0.02:
            # La racha empieza despues de que acabara la linea anterior: esta
            # linea la abre, luego su marca deberia coincidir con el comienzo.
            fuera.append((ABRE_RACHA, dentro[0], dentro[0] - t))
        else:
            fuera.append((EN_MITAD, None, None))
        fin_previo = s["fin"]
    return fuera


def mediana(v):
    v = sorted(v)
    return v[len(v) // 2] if v else 0.0


def ms(v):
    return "mediana %4.0f ms, peor %5.0f ms" % (1000 * mediana(v), 1000 * max(v or [0]))


def informe(titulo, segs, casos, tarde_ms):
    sil = [(s, c) for s, c in zip(segs, casos) if c[0] == EN_SILENCIO]
    abre = [(s, c) for s, c in zip(segs, casos) if c[0] == ABRE_RACHA]
    mitad = [s for s, c in zip(segs, casos) if c[0] == EN_MITAD]
    n = max(len(segs), 1)
    print(titulo)
    d = [abs(c[2]) for _, c in sil if c[2] is not None]
    print("  Arrancan en un silencio ...... %3d de %d (%2d %%)%s"
          % (len(sil), len(segs), round(100 * len(sil) / n), ("   " + ms(d)) if d else ""))
    t = [-c[2] for _, c in abre if c[2] is not None and -c[2] > tarde_ms / 1000.0]
    print("  Abren racha y van tarde ...... %3d de %d (%2d %%)%s"
          % (len(t), len(segs), round(100 * len(t) / n), ("   " + ms(t)) if t else ""))
    print("  En mitad del habla ........... %3d de %d (%2d %%)   el detector no opina"
          % (len(mitad), len(segs), round(100 * len(mitad) / n)))
    return len(sil), len(t)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("audio")
    ap.add_argument("datos")
    ap.add_argument("--salida", default=None, help="datos nuevos con los tiempos ajustados")
    ap.add_argument("--ventana", type=float, default=0.7,
                    help="cuanto se permite mover un arranque, como mucho (segundos)")
    ap.add_argument("--tarde", type=float, default=250,
                    help="a partir de cuantos ms de retraso se considera que va tarde")
    ap.add_argument("--peores", type=int, default=6, help="cuantos ejemplos enseñar")
    ap.add_argument("--forzar", action="store_true")
    a = ap.parse_args()

    for p, q in ((a.audio, "la grabación"), (a.datos, "el archivo de datos")):
        if not os.path.isfile(p):
            falla("no está %s: %s" % (q, p))
    if a.salida and os.path.exists(a.salida) and not a.forzar:
        falla("ya existe %s. Regenerar produce versión nueva, nunca sobrescribe (ADR-011 §8)" % a.salida)

    from transcribir_audio import decodificar
    x = decodificar(a.audio)
    d = json.load(io.open(a.datos, encoding="utf-8"))
    doc = d.get("publicada") or d.get("principal")
    if not doc:
        falla("ese archivo de datos no trae la pasada publicada")
    segs = doc["segmentos"]

    tramos = habla(x)
    dur, voz = len(x) / 16000.0, sum(b - a2 for a2, b in tramos)
    print("\n%s" % os.path.basename(a.audio))
    print("Habla detectada: %d rachas, %.0f s de %.0f s (%d %% del tiempo)\n"
          % (len(tramos), voz, dur, round(100 * voz / max(dur, 1))))

    casos = clasificar(segs, tramos)
    sil0, tar0 = informe("ANTES", segs, casos, a.tarde)

    malas = sorted([(abs(c[2]), s, c) for s, c in zip(segs, casos)
                    if c[0] != EN_MITAD and c[2] is not None and abs(c[2]) > a.tarde / 1000.0],
                   key=lambda z: z[0], reverse=True)[:a.peores]
    if malas:
        print("\nLas peores, para comprobarlas a oído:")
        for delta, s, c in malas:
            print("  %s  %+5.0f ms  %s  «%s»"
                  % (hms(s["inicio"]), 1000 * c[2],
                     "en silencio" if c[0] == EN_SILENCIO else "abre tarde ",
                     (s.get("texto") or "").strip()[:52]))

    movidos, desplazamiento = 0, []
    for s, c in zip(segs, casos):
        if c[1] is None:
            continue
        if c[0] == ABRE_RACHA and abs(c[2]) <= a.tarde / 1000.0:
            continue
        if abs(c[2]) > a.ventana:
            continue
        nuevo = c[1]
        pal = s.get("palabras") or []
        if pal and abs(pal[0]["i"] - s["inicio"]) < 0.05:
            pal[0]["i"] = round(min(nuevo, pal[0]["f"] - 0.02), 3)
        s["inicio"] = round(nuevo, 3)
        movidos += 1
        desplazamiento.append(abs(c[2]))

    print("")
    sil1, tar1 = informe("DESPUÉS", segs, clasificar(segs, tramos), a.tarde)
    print("\nSe movieron %d arranques de %d, %.0f ms de media. Los que quedan o se pasan"
          % (movidos, len(segs), 1000 * mediana(desplazamiento)))
    print("de la ventana de %.1f s o no tienen comienzo de racha al que ir." % a.ventana)

    if a.salida:
        d["alineacion"] = {"metodo": "arranques ajustados al detector de voz",
                           "ventana_s": a.ventana, "tarde_ms": a.tarde,
                           "arranques_movidos": movidos,
                           "en_silencio_antes": sil0, "en_silencio_despues": sil1,
                           "tarde_antes": tar0, "tarde_despues": tar1,
                           "NO_es": "alineación forzada por CTC: no juzga ni recoloca "
                                    "las líneas que arrancan en mitad del habla"}
        json.dump(d, io.open(a.salida, "w", encoding="utf-8"), ensure_ascii=False)
        print("\nOK  %s  -  el archivo anterior no se tocó." % os.path.basename(a.salida))
    else:
        print("\n(Sin --salida no se escribió nada: esto ha sido solo la medición.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
