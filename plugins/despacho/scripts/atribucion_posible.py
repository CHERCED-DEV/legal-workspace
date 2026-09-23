# -*- coding: utf-8 -*-
"""atribucion_posible — hasta dónde se puede decir quién dijo qué.

    python atribucion_posible.py <transcripcion.md> <datos.json>
                                 --entidades <entidades.json> [--json]

EL PROBLEMA. Un acta escribe «la Secretaría manifestó que…». Eso afirma dos
cosas de golpe: que la Secretaría estuvo, y que dijo eso. El acta modelo lo
sostiene porque **la firma quien estuvo en la sala**. Una maquina no estuvo, y
por eso no puede sostenerlo sola.

QUE COMPRUEBA ESTE PROGRAMA, Y QUE NO. De las condiciones que hacen segura una
atribucion, **tres se pueden comprobar sin oir** y son las que se miran aqui:

  1. Que la entidad aparezca en PRIMERA PERSONA en ese turno -- «nosotros como
     la corporacion», «desde la secretaria vamos a» --. **La mencion en tercera
     persona NUNCA atribuye**: en una mesa, el nombre de una entidad aparece
     casi siempre porque se le habla o se habla DE ella.
  2. Que en esa ventana haya UNA sola entidad. Con dos, elegir es apostar.
  3. Que el tramo NO este en discordia. Si el texto no es fiable como texto,
     no puede sostener un sujeto.

Las otras cuatro **no son de maquina** y el programa no las finge: la planilla
de asistencia, cuantas personas trajo cada entidad, si el pasaje es discurso
referido de un ausente, y la declaracion de ella. Este programa **nunca
aprueba una atribucion**: dice cuales estan bloqueadas y por que, y del resto
dice que dependen de una persona.
"""
import argparse, io, json, os, re, sys, unicodedata

LINEA = re.compile(r"^\*\*\[(\d\d:\d\d:\d\d)\][^*]*\*\*\s+(.*?)(?:\s+`\[\?\]`.*)?$")
VENTANA = 20.0          # segundos: el turno alrededor de la mencion
ACUERDO_MINIMO = 0.80   # por debajo, el texto no sostiene un sujeto

# Primera persona pegada a la entidad. Son las formas en que alguien habla
# COMO su entidad; cualquier otra cosa es hablar DE ella.
PRIMERA = re.compile(
    r"\b(nosotros|nosotras|yo|mi|nuestr[oa]s?|desde (?:la|el)|como (?:la|el)|"
    r"vamos a|voy a|hicimos|hemos|tenemos|estamos|le contamos|les contamos)\b", re.I)


def falla(msg):
    sys.stderr.write("\nDETENIDO: " + msg + "\n")
    raise SystemExit(2)


def norm(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9ñ ]", " ", s)).strip()


def segundos(v):
    m = re.match(r"(\d+):(\d\d):(\d\d)", (v or "").strip())
    return None if not m else int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))


def hms(s):
    s = max(0, float(s or 0))
    return "%02d:%02d:%02d" % (s // 3600, (s % 3600) // 60, s % 60)


def acuerdo_en(ventanas, t):
    """Cuanto coinciden las lecturas automaticas en ese punto."""
    for v in ventanas or []:
        if v["t"] <= t < v["t"] + 20.0:
            return v.get("medio")
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("transcripcion")
    ap.add_argument("datos")
    ap.add_argument("--entidades", required=True,
                    help="el .json con las entidades y cómo se las nombra en el audio")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    for p, q in ((a.transcripcion, "la transcripción"), (a.datos, "el archivo de datos"),
                 (a.entidades, "el archivo de entidades")):
        if not os.path.isfile(p):
            falla("no está %s: %s" % (q, p))

    d = json.load(io.open(a.datos, encoding="utf-8"))
    doc = d.get("publicada") or d.get("principal")
    if not doc:
        falla("ese archivo de datos no trae la pasada publicada")
    ventanas = d.get("ventanas")

    ents = json.load(io.open(a.entidades, encoding="utf-8")).get("entidades")
    if not ents:
        falla("ese archivo no trae «entidades»")

    lineas = []
    for l in io.open(a.transcripcion, encoding="utf-8").read().split("\n"):
        m = LINEA.match(l)
        if m:
            lineas.append((segundos(m.group(1)), norm(m.group(2)), m.group(2)))

    hallazgos = []
    for e in ents:
        nombre = e.get("entidad") or "?"
        variantes = [norm(v) for v in (e.get("variantes") or []) if norm(v)]
        for t, texto, crudo in lineas:
            if t is None:
                continue
            cual = next((v for v in variantes if v and v in texto), None)
            if not cual:
                continue
            # La ventana del turno, para mirar alrededor y no solo la linea.
            cerca = [x for x in lineas if x[0] is not None and abs(x[0] - t) <= VENTANA / 2]
            ventana_txt = " ".join(x[1] for x in cerca)
            otras = sorted({o.get("entidad") for o in ents
                            for v in (norm(z) for z in (o.get("variantes") or []))
                            if v and v in ventana_txt} - {nombre})
            primera = bool(PRIMERA.search(texto))
            med = acuerdo_en(ventanas, t)

            bloqueos = []
            if not primera:
                bloqueos.append("la nombra en tercera persona")
            if otras:
                bloqueos.append("hay %d entidad(es) más en la ventana" % len(otras))
            if med is not None and med < ACUERDO_MINIMO:
                bloqueos.append("las lecturas coinciden solo el %d %%" % round(100 * med))
            hallazgos.append({"entidad": nombre, "minuto": hms(t), "cita": crudo[:70],
                              "primera_persona": primera, "otras": otras,
                              "acuerdo": med, "bloqueos": bloqueos})

    libres = [h for h in hallazgos if not h["bloqueos"]]
    print("\n%s" % os.path.basename(a.transcripcion))
    print("Menciones de una entidad: %d" % len(hallazgos))
    print("   BLOQUEADAS para atribuir ....... %d" % (len(hallazgos) - len(libres)))
    print("   dependen de una persona ........ %d" % len(libres))

    porque = {}
    for h in hallazgos:
        for b in h["bloqueos"]:
            clave = re.sub(r"\d+", "N", b)
            porque[clave] = porque.get(clave, 0) + 1
    if porque:
        print("\nPor qué se bloquean:")
        for k, v in sorted(porque.items(), key=lambda kv: -kv[1]):
            print("   %3d  %s" % (v, k))

    if libres:
        print("\nLas que NO están bloqueadas — y aun así NO están aprobadas:")
        for h in libres[:12]:
            print("   %s  %-34s «%s»" % (h["minuto"], h["entidad"][:34], h["cita"][:52]))
        if len(libres) > 12:
            print("   … y %d más" % (len(libres) - 12))

    print("\nNinguna de las de arriba queda atribuida por este programa. Faltan las")
    print("cuatro condiciones que no son de máquina: la planilla firmada, cuántas")
    print("personas trajo esa entidad, si el pasaje relata a un ausente, y que una")
    print("persona que estuvo en la sala lo declare oyendo.")

    if a.json:
        print(json.dumps({"menciones": len(hallazgos), "bloqueadas": len(hallazgos) - len(libres),
                          "dependen_de_persona": len(libres), "detalle": hallazgos},
                         ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
