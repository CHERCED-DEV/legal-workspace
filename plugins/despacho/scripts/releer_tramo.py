# -*- coding: utf-8 -*-
"""releer_tramo — volver a leer UN tramo dudoso, de muchas maneras, y contar.

    python releer_tramo.py <audio> --desde 00:01:10 --hasta 00:01:22 --salida <lecturas.json>
                           [--buscar palabra --buscar "una frase"]

POR QUE EXISTE. La transcripción publica UNA lectura de la grabación entera.
Cuando una palabra de esa lectura importa y no se sostiene -- el 2026-09-23,
un cargo que la máquina daba por seguro al 100 % --, la forma de salir de
dudas sin oír es volver a leer SOLO ese tramo, recortado, de varias maneras:
la mezcla tal cual, la mezcla limpia, cada canal por separado, y con recortes
de distinto largo. Y contar: en cuántas de esas lecturas sale la palabra.
La cuenta va partida, porque no son lecturas independientes: aparte el
recorte ancho (lleva contexto de fuera del tramo), y el resto por recorte y
por pista (la mezcla y sus canales suelen leerse casi igual).

Allí salió en 0 de 16 lecturas, y en su lugar otras tres palabras distintas.
Eso no dice qué se dijo (lo dice oír el tramo), pero sí que la palabra
publicada no se sostiene, y justifica señalarla.

QUE NO HACE. No decide qué se dijo: las lecturas son de una máquina, y un
recorte corto se inventa frases («Gracias por ver el video»); por eso se
cuenta en qué COINCIDEN. No toca la transcripción. Nada sale de esta máquina:
modelo local, sin red. Nunca sobrescribe (ADR-011 §8).
"""
import argparse, datetime, hashlib, io, json, os, re, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def falla(msg):
    sys.stderr.write("\nDETENIDO: " + msg + "\n")
    raise SystemExit(2)


def a_segundos(v):
    m = re.match(r"^(\d+):(\d\d):(\d\d(?:\.\d+)?)$", v.strip())
    if not m:
        falla("la hora «%s» no es HH:MM:SS" % v)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def hms(s):
    s = max(0, int(s))
    return "%02d:%02d:%02d" % (s // 3600, (s % 3600) // 60, s % 60)


ANCHO = "el recorte ancho (±4 s)"


def recortes(desde, hasta, duracion=None):
    """[(nombre, desde, hasta)]: los recortes que se leen. El tramo con un poco
    de margen, uno más ancho (con contexto: el reconocedor lee mejor con frase
    entera), y las dos mitades (un recorte corto no arrastra lo de alrededor)."""
    medio = (desde + hasta) / 2
    vs = [("el tramo", desde - 0.5, hasta + 0.5), (ANCHO, desde - 4.0, hasta + 4.0),
          ("la primera mitad", desde, medio + 1.0), ("la segunda mitad", medio - 1.0, hasta)]
    tope = duracion if duracion else float("inf")
    out = []
    for n, a, b in vs:
        a, b = max(0.0, a), min(tope, b)
        if b - a >= 1.0 and (round(a, 1), round(b, 1)) not in [(round(x, 1), round(y, 1)) for _n, x, y in out]:
            out.append((n, round(a, 2), round(b, 2)))
    return out


def ventanas(desde, hasta, duracion=None):
    return [(a, b) for _n, a, b in recortes(desde, hasta, duracion)]


def plano(s):
    s = unicodedata.normalize("NFC", s or "").lower()
    return re.sub(r"[^\w\s]", " ", s)


def cuantas_dicen(lecturas, palabra):
    """En cuántas lecturas (con texto) aparece `palabra` como palabra o frase entera."""
    p = plano(palabra).strip()
    patron = re.compile(r"(?<!\w)" + re.escape(p) + r"(?!\w)")
    return sum(1 for l in lecturas if patron.search(plano(l["texto"]))), len(lecturas)


def cuentas(lecturas, palabra):
    """La cuenta, partida para que no engañe.

    Un solo «N de 16» sumaba como independientes cosas que no lo son: el
    recorte ancho lleva 4 s de contexto que NO son el tramo (una palabra dicha
    solo ahí no sostiene la del tramo), y la mezcla, la mezcla limpia y los
    canales de una misma grabación suelen leerse casi igual. Por eso: aparte
    el recorte ancho, y el resto por recorte y por pista."""
    def dos(ls):
        n, t = cuantas_dicen(ls, palabra)
        return {"dicen": n, "de": t}
    dentro = [l for l in lecturas if l.get("recorte") != ANCHO]
    por_recorte, por_pista = {}, {}
    for l in dentro:
        por_recorte.setdefault(l.get("recorte") or "?", []).append(l)
        por_pista.setdefault(l.get("pista") or "?", []).append(l)
    return {"sin_el_recorte_ancho": dos(dentro),
            "recorte_ancho": dos([l for l in lecturas if l.get("recorte") == ANCHO]),
            "por_recorte": {k: dos(v) for k, v in por_recorte.items()},
            "por_pista": {k: dos(v) for k, v in por_pista.items()}}


def cuentas_txt(palabra, c):
    """Lo que se imprime de `cuentas`."""
    uno = lambda x: "%d de %d" % (x["dicen"], x["de"])
    return "\n".join([
        "«%s»:" % palabra,
        "   en los recortes del tramo: %s lecturas con texto" % uno(c["sin_el_recorte_ancho"]),
        "     por recorte: %s" % " · ".join("%s %s" % (k, uno(v)) for k, v in c["por_recorte"].items()),
        "     por pista:   %s" % " · ".join("%s %s" % (k, uno(v)) for k, v in c["por_pista"].items()),
        "   aparte, %s: %s (lleva contexto de fuera del tramo; no sostiene la palabra DENTRO del tramo)"
        % (ANCHO, uno(c["recorte_ancho"]))])


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio")
    ap.add_argument("--desde", required=True)
    ap.add_argument("--hasta", required=True)
    ap.add_argument("--salida", required=True, help="el .json con todas las lecturas (no se sobrescribe)")
    ap.add_argument("--buscar", action="append", default=[], help="palabra o frase que contar en las lecturas")
    a = ap.parse_args(argv)
    if not os.path.isfile(a.audio):
        falla("no está la grabación: %s" % a.audio)
    if os.path.exists(a.salida):
        falla("ya existe %s: no se sobrescribe (ADR-011 §8)" % a.salida)
    d, h = a_segundos(a.desde), a_segundos(a.hasta)
    if h <= d:
        falla("el tramo acaba antes de empezar")

    import numpy as np
    import transcribir_audio as TA
    import genoma_de_voz as G
    x = TA.decodificar(a.audio)
    x = np.asarray(x[0] if isinstance(x, tuple) else x, dtype=np.float32)
    sr = TA.SR
    pistas = {"la mezcla tal cual": x, "la mezcla limpia (la de la transcripción)": np.asarray(TA.limpiar(x), dtype=np.float32)}
    try:
        l_, r_ = TA.decodificar(a.audio, estereo=True)
        if l_ is not None and r_ is not None:
            pistas["el canal izquierdo"] = np.asarray(l_, dtype=np.float32)
            pistas["el canal derecho"] = np.asarray(r_, dtype=np.float32)
    except Exception:
        pass
    mod, disp = G._modelo_whisper()
    lecturas = []
    for recorte, va, vb in recortes(d, h, x.size / float(sr)):
        for nombre, sen in pistas.items():
            txt, pw = G._oir_tramo(mod, sen, sr, va, vb)
            lecturas.append({"desde": hms(va), "hasta": hms(vb), "desde_s": va, "hasta_s": vb,
                             "recorte": recorte, "pista": nombre, "texto": txt, "palabras": pw})
            print("%s-%s  %-24s %-44s %s" % (hms(va), hms(vb), recorte, nombre, txt or "(nada)"))
    con = [l for l in lecturas if l["texto"]]
    por_palabra = {p: cuentas(con, p) for p in a.buscar}
    for p, c in por_palabra.items():
        print(cuentas_txt(p, c))
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    with io.open(a.salida, "w", encoding="utf-8", newline="\n") as f:
        json.dump({
            "formato": "despacho/lecturas-de-un-tramo",
            "_que_es": "Lecturas automáticas de un tramo corto, cada una recortada y leída sola. Son lecturas de una "
                       "máquina, NO lo que se dijo: nadie ha oído el tramo. Sirven para saber si las palabras publicadas "
                       "se sostienen. Un recorte corto puede inventarse frases: cuenta en qué coinciden.",
            "como": "faster-whisper large-v3 en local (%s), idioma es, beam 5, sin filtro de silencio, sin texto previo "
                    "(genoma_de_voz._oir_tramo)" % ("GPU" if disp == "cuda" else "CPU"),
            "grabacion": os.path.basename(a.audio),
            "sha256": hashlib.sha256(open(a.audio, "rb").read()).hexdigest(),
            "tramo": {"desde": a.desde, "hasta": a.hasta},
            "fecha": datetime.date.today().isoformat(),
            "cuentas": por_palabra,
            "lecturas": lecturas,
        }, f, ensure_ascii=False, indent=1, default=G._json)
    print("\nOK  %s  -  %d lecturas" % (os.path.basename(a.salida), len(lecturas)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
