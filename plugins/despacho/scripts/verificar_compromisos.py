# -*- coding: utf-8 -*-
"""verificar_compromisos — que cada compromiso señalado exista de verdad.

    python verificar_compromisos.py <compromisos.json> <transcripcion.md> <datos.json>
                                    [--json]

POR QUE EXISTE. Senalar un compromiso es un JUICIO: alguien lee la
transcripcion y dice «aqui se obligaron a algo». Un juicio no se puede
comprobar a maquina -- pero **sus dos apoyos si**:

    1. el MINUTO tiene que existir en la grabacion;
    2. la CITA tiene que estar LITERAL en la transcripcion.

Si la cita no esta, el compromiso se apoya en una frase que nadie dijo. Eso no
es un matiz: es la diferencia entre senalar una obligacion y fabricarla.

LO QUE NO HACE, Y HAY QUE DECIRLO. **No dice si el compromiso es real.** Que
la cita sea textual no significa que alguien se obligara: significa que la
frase existe. Decidir si eso es un compromiso sigue siendo de una persona, y
por eso el programa NUNCA aprueba: cuenta, senala lo que no cuadra, y calla
sobre el resto.
"""
import argparse, io, json, os, re, sys, unicodedata

TIEMPO = re.compile(r"(\d+):(\d\d):(\d\d)")
# La etiqueta del hablante va DENTRO de la negrita -- «**[00:00:00] · Hablante 1**» --,
# asi que la expresion tiene que admitirla. Sin esto se descartaban justo las
# lineas que llevan hablante, que son las que mas importan, y el programa
# denunciaba como inventadas citas que si estaban.
LINEA = re.compile(r"^\*\*\[(\d\d:\d\d:\d\d)\][^*]*\*\*\s+(.*?)(?:\s+`\[\?\]`.*)?$")
TOLERANCIA = 2.0     # segundos: los minutos vienen con resolucion de segundo


def falla(msg):
    sys.stderr.write("\nDETENIDO: " + msg + "\n")
    raise SystemExit(2)


def norm(s):
    """Para comparar citas: sin tildes, sin puntuacion, sin dobles espacios.

    NO se normaliza para relajar la exigencia, sino para que una tilde perdida
    del reconocedor no haga fallar una cita que si esta."""
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9ñ ]", " ", s)).strip()


def segundos(v):
    m = TIEMPO.match((v or "").strip())
    if not m:
        return None
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("compromisos")
    ap.add_argument("transcripcion")
    ap.add_argument("datos")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    for p, q in ((a.compromisos, "el archivo de compromisos"),
                 (a.transcripcion, "la transcripción"), (a.datos, "el archivo de datos")):
        if not os.path.isfile(p):
            falla("no está %s: %s" % (q, p))

    d = json.load(io.open(a.compromisos, encoding="utf-8"))
    cs = d.get("compromisos")
    if cs is None:
        falla("ese archivo no trae «compromisos»")
    doc = json.load(io.open(a.datos, encoding="utf-8"))
    doc = doc.get("publicada") or doc.get("principal")
    if not doc:
        falla("ese archivo de datos no trae la pasada publicada")
    segs = doc["segmentos"]
    dur = doc.get("duracion_s") or (segs[-1]["fin"] if segs else 0)

    md = io.open(a.transcripcion, encoding="utf-8").read()
    texto = norm(" ".join(m.group(2) for m in
                          (LINEA.match(l) for l in md.split("\n")) if m))

    sin_minuto, fuera, sin_cita, no_literal, ok = [], [], [], [], 0
    for i, c in enumerate(cs, 1):
        s = segundos(c.get("minuto"))
        etiqueta = "%d. %s" % (i, (c.get("de_que_se_trata") or "")[:58])
        if s is None:
            sin_minuto.append(etiqueta)
            continue
        if s > dur + TOLERANCIA:
            fuera.append("%s  —  %s, y la grabación dura %s"
                         % (etiqueta, c.get("minuto"), hms(dur)))
            continue
        if not any(abs(g["inicio"] - s) <= TOLERANCIA or g["inicio"] <= s < g["fin"]
                   for g in segs):
            fuera.append("%s  —  %s no cae en ninguna línea" % (etiqueta, c.get("minuto")))
            continue
        cita = c.get("cita")
        if not (cita or "").strip():
            sin_cita.append(etiqueta)
            continue
        partes = [p for p in re.split(r"\s*/\s*|\[…\]|…", cita) if len(norm(p)) >= 8]
        if not partes:
            partes = [cita]
        faltan = [p for p in partes if norm(p) not in texto]
        if faltan:
            no_literal.append("%s\n        no está: «%s»" % (etiqueta, faltan[0].strip()[:72]))
            continue
        ok += 1

    print("\n%s" % os.path.basename(a.compromisos))
    print("Compromisos señalados: %d" % len(cs))
    print("   con minuto que existe y cita LITERAL ..... %d" % ok)
    for titulo, lista in (("SIN MINUTO", sin_minuto),
                          ("MINUTO QUE NO EXISTE", fuera),
                          ("SIN CITA", sin_cita),
                          ("CITA QUE NO ESTÁ EN LA TRANSCRIPCIÓN", no_literal)):
        if lista:
            print("\n%s — %d:" % (titulo, len(lista)))
            for x in lista:
                print("   · %s" % x)

    malos = len(sin_minuto) + len(fuera) + len(sin_cita) + len(no_literal)
    print("")
    if malos:
        print("%d de %d no se sostienen. Un compromiso apoyado en una frase que nadie"
              % (malos, len(cs)))
        print("dijo no señala una obligación: la fabrica.")
    else:
        print("Los %d se apoyan en una frase que está en la transcripción." % len(cs))
        print("Eso NO dice que sean compromisos: dice que la frase existe. Lo otro")
        print("lo decide quien oiga.")

    if a.json:
        print(json.dumps({"total": len(cs), "sostenidos": ok, "sin_minuto": len(sin_minuto),
                          "minuto_inexistente": len(fuera), "sin_cita": len(sin_cita),
                          "cita_no_literal": len(no_literal)}, ensure_ascii=False))
    return 1 if malos else 0


def hms(s):
    s = max(0, float(s or 0))
    return "%02d:%02d:%02d" % (s // 3600, (s % 3600) // 60, s % 60)


if __name__ == "__main__":
    sys.exit(main())
