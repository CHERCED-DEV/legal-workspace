# -*- coding: utf-8 -*-
"""separar_voces — volver a separar las voces sin volver a transcribir.

    python separar_voces.py <audio> <datos.json> --salida <nuevos.json>
                            [--umbral 0.60] [--comparar]

POR QUE EXISTE. Cuando la separacion funde a dos personas en una sola voz, la
unica salida era volver a transcribir entero -- media hora larga de computo
para cambiar unas etiquetas, sin tocar una sola palabra del texto. Este paso
rehace SOLO la separacion y reescribe las etiquetas.

EL UMBRAL, Y POR QUE SE BAJA. Cuanto mas alto, menos voces distintas reconoce;
cuanto mas bajo, mas. El valor de la tuberia es 0,90 y sobre este material
funde a los dos protagonistas. La asimetria manda: **separar de mas es
recuperable y fundir no lo es**. Con quince voces, una persona oye una muestra
de cada una y junta las que sean la misma; con dos fundidas, no hay nada que
hacer -- la informacion de que eran dos ya se perdio.

QUE NO HACE. No toca el texto: ni una palabra cambia. No pone nombres -- eso
es `nombrar_voces.py`, y lo afirma una persona. Y no dice cual umbral es el
bueno: enseña en que cambia el reparto y **eso lo decide quien oye**.

NUNCA sobrescribe (ADR-011 §8).
"""
import argparse, io, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def falla(msg):
    sys.stderr.write("\nDETENIDO: " + msg + "\n")
    raise SystemExit(2)


def hms(s):
    s = max(0, float(s or 0))
    return "%02d:%02d:%02d" % (s // 3600, (s % 3600) // 60, s % 60)


def reparto(doc):
    """Cuanto habla cada voz, y cuantas lineas se quedan sin voz."""
    v = {}
    for s in doc["segmentos"]:
        k = s.get("voz")
        d = v.setdefault(k, {"segundos": 0.0, "lineas": 0})
        d["segundos"] += max(0.0, s["fin"] - s["inicio"])
        d["lineas"] += 1
    return v


def enseñar(titulo, doc, dia):
    v = reparto(doc)
    total = sum(d["segundos"] for k, d in v.items() if k is not None) or 1.0
    con = {k: d for k, d in v.items() if k is not None}
    dom = max((d["segundos"] for d in con.values()), default=0.0) / total
    print("\n%s  —  umbral %.2f" % (titulo, dia["umbral"]))
    print("   voces: %d   ·   la mayor se lleva el %d %%   ·   sin voz: %d líneas"
          % (len(con), round(100 * dom), v.get(None, {}).get("lineas", 0)))
    for k, d in sorted(con.items(), key=lambda kv: -kv[1]["segundos"])[:16]:
        print("      Hablante %-3s %5.0f s  %4d líneas  (%2d %%)"
              % (k, d["segundos"], d["lineas"], round(100 * d["segundos"] / total)))
    if len(con) > 16:
        print("      … y %d voces más" % (len(con) - 16))
    return dom, len(con)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio")
    ap.add_argument("datos")
    ap.add_argument("--salida", required=True, help="dónde dejar los datos nuevos")
    ap.add_argument("--umbral", type=float, default=0.60,
                    help="cuanto más bajo, más voces distintas reconoce (0,90 es el de la tubería)")
    ap.add_argument("--forzar", action="store_true")
    a = ap.parse_args()

    for p, q in ((a.audio, "la grabación"), (a.datos, "el archivo de datos")):
        if not os.path.isfile(p):
            falla("no está %s: %s" % (q, p))
    if os.path.exists(a.salida) and not a.forzar:
        falla("ya existe %s. Regenerar produce versión nueva, nunca sobrescribe (ADR-011 §8)" % a.salida)
    if not (0.1 <= a.umbral <= 1.5):
        falla("el umbral %.2f está fuera de lo razonable (0,1 a 1,5)" % a.umbral)

    import transcribir_audio as T
    d = json.load(io.open(a.datos, encoding="utf-8"))
    doc = d.get("publicada") or d.get("principal")
    if not doc:
        falla("ese archivo de datos no trae la pasada publicada")

    antes_dom, antes_n = enseñar("ANTES", doc, d.get("voces") or {"umbral": 0.0})
    texto_antes = [s.get("texto") for s in doc["segmentos"]]

    print("\nSeparando otra vez con umbral %.2f. El texto no se toca." % a.umbral)
    x = T.decodificar(a.audio)
    T.UMBRAL_VOCES = a.umbral
    dia = T.diarizar(x)
    T.asignar_voces(doc, dia)
    d["voces"] = dia

    if [s.get("texto") for s in doc["segmentos"]] != texto_antes:
        falla("la separación cambió el texto transcrito, y eso no puede pasar")

    dom, n = enseñar("DESPUÉS", doc, dia)

    print("\nQué cambió: de %d voces a %d; la mayor pasa del %d %% al %d %%."
          % (antes_n, n, round(100 * antes_dom), round(100 * dom)))
    if dom >= 0.80:
        print("AVISO: una sola voz sigue llevándose el %d %%. Con eso NO se puede "
              "atribuir nada a nadie." % round(100 * dom))
    elif n > 10:
        print("Son muchas voces, y está bien: separar de más es recuperable. Quien oiga\n"
              "junta las que sean la misma persona; fundir dos no tiene arreglo.")

    json.dump(d, io.open(a.salida, "w", encoding="utf-8"), ensure_ascii=False)
    print("\nOK  %s  -  el archivo anterior no se tocó." % os.path.basename(a.salida))
    print("El texto es idéntico: solo cambian las etiquetas de hablante.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
