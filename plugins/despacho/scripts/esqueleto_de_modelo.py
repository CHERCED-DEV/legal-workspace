# -*- coding: utf-8 -*-
"""esqueleto_de_modelo — qué forma tiene el documento que ella dio de ejemplo.

    python esqueleto_de_modelo.py <modelo.docx|.md> [--salida esqueleto.json]
                                  [--ver] [--umbral 1.0]

PARA QUE. Cuando ella entrega un documento suyo como modelo, lo que se copia es
la FORMA -- que apartados lleva, en que orden, con que nombres y con que
formulas fijas -- y nunca el contenido. Este programa saca esa forma y, sobre
todo, **mide si la saco entera**.

LA MEDIDA, QUE ES LO QUE IMPORTA. Decir «entendi el documento» no significa
nada. Aqui significa una cosa comprobable: con lo extraido se vuelve a armar el
texto del original y **tiene que salir identico**. Si al rearmarlo falta un
parrafo, una celda o un renglon de una lista, la lectura se dejo algo, y el
programa dice cual y cuanto: «reconstruye el 97 %» no es un aprobado, es un
aviso de que hay un 3 % que nadie miro.

LO QUE NO HACE. No redacta, no rellena y no opina sobre el contenido. Marcar
que un dato es variable **no es saber cual va**: los valores que extrae son los
del modelo -- de otro caso, de otras personas -- y no se copian nunca. En el
documento nuevo, cada uno de esos huecos es un hueco hasta que alguien lo
llene con material del caso.
"""
import argparse, io, json, os, re, sys, unicodedata

SEPARADOR = "\n"

# Lo que hace variable a un trozo de texto. Son criterios ELEGIDOS, no medidos,
# y por eso se declaran juntos: marcan DONDE puede haber un dato de otro caso,
# no que ahi vaya un dato concreto.
VARIABLE = [
    ("fecha_larga", re.compile(r"\b\d{1,2}\s+de\s+[a-záéíóúñ]+\s+de\s+(?:dos mil\s+\w+|\d{4})\b", re.I)),
    ("fecha_corta", re.compile(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b")),
    ("hora", re.compile(r"\b\d{1,2}[:.]\d{2}\s*(?:a\.?\s?m\.?|p\.?\s?m\.?|horas)?\b", re.I)),
    ("identificacion", re.compile(r"\b(?:c\.?\s?c\.?|nit|t\.?\s?p\.?|radicad\w*)\s*\.?\s*[\dNnºo°.\-]+", re.I)),
    ("cifra", re.compile(r"\b\d[\d.,]*\b")),
    ("nombre_propio", re.compile(r"\b(?:[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,}|[A-ZÁÉÍÓÚÑ]{3,})"
                                 r"(?:\s+(?:de|del|la|las|los|y)?\s*"
                                 r"(?:[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,}|[A-ZÁÉÍÓÚÑ]{3,}))+")),
    # Una mayuscula suelta a mitad de frase. Va la ultima a proposito: las de
    # arriba se quedan con lo que reconocen mejor, y esta recoge el resto.
    #
    # Por que existe, aunque marque de mas: sin ella un apellido solo --
    # «Guzman» -- no es «nombre propio» (hacen falta dos palabras), pasa por
    # formula fija y **se copia**. La asimetria decide: marcar de mas crea un
    # hueco que alguien llena en treinta segundos; marcar de menos mete el
    # nombre de otro cliente en el documento, que es el peor accidente posible.
    ("mayuscula_suelta", re.compile(r"(?<=[^.!?\n]\s)"
                                    r"(?:[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,}|[A-ZÁÉÍÓÚÑ]{2,})\b")),
]


def falla(msg):
    sys.stderr.write("\nDETENIDO: " + msg + "\n")
    raise SystemExit(2)


def _norm(s):
    s = unicodedata.normalize("NFC", s or "")
    return re.sub(r"[ \t]+", " ", s).strip()


def leer_docx(ruta):
    """Cada pieza del documento, en el orden en que va, sin saltarse tablas.

    Recorre el cuerpo por el XML y no por `paragraphs`, porque esa lista **se
    salta las tablas** -- y en un acta los asistentes suelen ir en una."""
    try:
        import docx
        from docx.table import Table
        from docx.text.paragraph import Paragraph
    except ImportError:
        falla("hace falta python-docx para leer un .docx (pip install python-docx)")
    d = docx.Document(ruta)
    piezas = []

    def parrafo(p, dentro=None):
        piezas.append({"clase": "parrafo", "estilo": p.style.name if p.style else "",
                       "texto": _norm(p.text), "dentro": dentro})

    for hijo in d.element.body.iterchildren():
        if hijo.tag.endswith("}p"):
            parrafo(Paragraph(hijo, d))
        elif hijo.tag.endswith("}tbl"):
            t = Table(hijo, d)
            piezas.append({"clase": "tabla_inicio", "filas": len(t.rows),
                           "columnas": len(t.columns), "texto": "", "estilo": "", "dentro": None})
            for i, fila in enumerate(t.rows):
                for j, celda in enumerate(fila.cells):
                    for p in celda.paragraphs:
                        parrafo(p, dentro="tabla[%d,%d]" % (i, j))
            piezas.append({"clase": "tabla_fin", "texto": "", "estilo": "", "dentro": None})
    return piezas


def leer_md(ruta):
    piezas = []
    for linea in io.open(ruta, encoding="utf-8").read().split("\n"):
        t = linea.rstrip()
        m = re.match(r"^(#{1,6})\s+(.*)$", t)
        estilo = ("Heading %d" % len(m.group(1))) if m else ""
        piezas.append({"clase": "parrafo", "estilo": estilo,
                       "texto": _norm(m.group(2) if m else t), "dentro": None})
    return piezas


def es_titulo(pieza):
    """Un apartado. Por estilo si el documento lo trae; si no, por la forma:
    linea corta, sin punto final, en mayusculas o numerada."""
    if pieza["clase"] != "parrafo":
        return False
    if re.match(r"^(Heading|T[ií]tulo)\s*\d", pieza.get("estilo") or "", re.I):
        return True
    t = pieza["texto"]
    if not t or len(t) > 90 or t.endswith("."):
        return False
    letras = [c for c in t if c.isalpha()]
    mayusculas = letras and all(c.isupper() for c in letras)
    numerado = bool(re.match(r"^(\d+[.)]|[IVXLC]+[.)]|[A-Z][.)])\s+\S", t))
    return bool(mayusculas or numerado)


def partes_variables(texto):
    """Los trozos que podrian ser datos de otro caso, sin solaparse."""
    marcas = []
    for nombre, patron in VARIABLE:
        for m in patron.finditer(texto):
            if all(m.end() <= a or m.start() >= b for a, b, _ in marcas):
                marcas.append((m.start(), m.end(), nombre))
    return sorted(marcas)


def plantilla_de(texto):
    """El texto con cada dato sustituido por su ranura, y los datos aparte."""
    fuera, datos, ultimo = [], [], 0
    for a, b, nombre in partes_variables(texto):
        fuera.append(texto[ultimo:a])
        fuera.append("{%s:%d}" % (nombre, len(datos)))
        datos.append({"ranura": "%s:%d" % (nombre, len(datos)), "valor_en_el_modelo": texto[a:b]})
        ultimo = b
    fuera.append(texto[ultimo:])
    return "".join(fuera), datos


def rellenar(plantilla, datos):
    t = plantilla
    for d in datos:
        t = t.replace("{%s}" % d["ranura"], d["valor_en_el_modelo"], 1)
    return t


def analizar(piezas):
    apartados, sueltas = [], []
    actual = None
    for i, p in enumerate(piezas):
        if p["clase"] != "parrafo":
            (actual["piezas"] if actual else sueltas).append(dict(p, i=i))
            continue
        if es_titulo(p):
            actual = {"titulo": p["texto"], "estilo": p.get("estilo") or "", "i": i, "piezas": []}
            apartados.append(actual)
            continue
        plant, datos = plantilla_de(p["texto"])
        pieza = dict(p, i=i, plantilla=plant, datos=datos,
                     tipo=("formula" if not datos and p["texto"] else
                           "mixto" if datos and _norm(plant.replace("{", "").replace("}", "")) else
                           "dato" if datos else "vacio"))
        (actual["piezas"] if actual else sueltas).append(pieza)
    return apartados, sueltas


def rearmar(apartados, sueltas):
    """El texto del original, reconstruido SOLO con lo extraido."""
    fuera = []

    def mete(p):
        # Solo parrafos: los marcadores de tabla no son texto del documento, y
        # colarlos aqui desplazaba la comparacion entera una posicion -- con lo
        # que el programa denunciaba como «no entendido» un documento que si
        # habia leido. El instrumento medía su propio defecto.
        if p.get("clase") == "parrafo":
            fuera.append(rellenar(p.get("plantilla", p["texto"]), p.get("datos") or []))

    for p in sueltas:
        mete(p)
    for a in apartados:
        fuera.append(a["titulo"])
        for p in a["piezas"]:
            mete(p)
    return fuera


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("modelo")
    ap.add_argument("--salida", default=None, help="dónde dejar el esqueleto en JSON")
    ap.add_argument("--ver", action="store_true", help="enseñar el esqueleto por pantalla")
    ap.add_argument("--umbral", type=float, default=1.0,
                    help="qué proporción hay que reconstruir para no fallar (1.0 = todo)")
    ap.add_argument("--forzar", action="store_true")
    a = ap.parse_args()

    if not os.path.isfile(a.modelo):
        falla("no está el modelo: %s" % a.modelo)
    if a.salida and os.path.exists(a.salida) and not a.forzar:
        falla("ya existe %s. Regenerar produce versión nueva, nunca sobrescribe (ADR-011 §8)" % a.salida)

    ext = os.path.splitext(a.modelo)[1].lower()
    if ext == ".docx":
        piezas = leer_docx(a.modelo)
    elif ext in (".md", ".txt"):
        piezas = leer_md(a.modelo)
    else:
        falla("solo se leen .docx, .md o .txt; esto es %s" % (ext or "sin extensión"))

    apartados, sueltas = analizar(piezas)

    # LA COMPROBACION. Con lo extraido se rearma el original; lo que no cuadre
    # es exactamente lo que la lectura se dejo.
    original = [p["texto"] for p in piezas if p["clase"] == "parrafo"]
    vuelto = rearmar(apartados, sueltas)
    iguales = sum(1 for x, y in zip(original, vuelto) if x == y)
    proporcion = iguales / max(len(original), 1)

    print("\n%s" % os.path.basename(a.modelo))
    print("Piezas: %d párrafos, %d apartados, %d tablas"
          % (len(original), len(apartados), sum(1 for p in piezas if p["clase"] == "tabla_inicio")))
    print("Reconstruye: %d de %d (%.1f %%)" % (iguales, len(original), 100 * proporcion))

    if len(original) != len(vuelto) or proporcion < a.umbral:
        print("\nLo que NO se pudo rearmar — la lectura se dejó esto:")
        mostrados = 0
        for k, x in enumerate(original):
            y = vuelto[k] if k < len(vuelto) else "<nada>"
            if x != y and mostrados < 8:
                print("   original: «%s»" % x[:88])
                print("   rearmado: «%s»" % y[:88])
                mostrados += 1
        if len(original) != len(vuelto):
            print("   y sobran o faltan %d piezas enteras" % abs(len(original) - len(vuelto)))

    todos = [p for a2 in apartados for p in a2["piezas"]] + [p for p in sueltas if "tipo" in p]
    cuenta = {t: sum(1 for p in todos if p.get("tipo") == t)
              for t in ("formula", "mixto", "dato", "vacio")}
    print("\nDe los %d párrafos con texto:" % sum(v for k, v in cuenta.items() if k != "vacio"))
    print("   fórmula fija (se copia tal cual) ....... %d" % cuenta["formula"])
    print("   mezcla de fórmula y dato ............... %d" % cuenta["mixto"])
    print("   solo dato (no se copia NADA) ........... %d" % cuenta["dato"])

    if a.ver:
        print("\nApartados, en su orden:")
        for a2 in apartados:
            n = sum(len(p.get("datos") or []) for p in a2["piezas"])
            print("   %-52s %2d párrafos, %2d datos del otro caso"
                  % ("«" + a2["titulo"][:48] + "»", len(a2["piezas"]), n))

    print("\nLos %d datos que trae el modelo son de OTRO caso: no se copia ninguno."
          % sum(len(p.get("datos") or []) for p in todos))

    if a.salida:
        json.dump({"modelo": os.path.basename(a.modelo),
                   "reconstruye": round(proporcion, 4),
                   "apartados": apartados, "sueltas": sueltas},
                  io.open(a.salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("OK  %s" % os.path.basename(a.salida))

    if proporcion < a.umbral:
        falla("solo se reconstruye el %.1f %% del modelo. Por debajo de %.1f %% la forma "
              "extraída NO representa el documento, y copiarla dejaría fuera lo que falta."
              % (100 * proporcion, 100 * a.umbral))
    return 0


if __name__ == "__main__":
    sys.exit(main())
