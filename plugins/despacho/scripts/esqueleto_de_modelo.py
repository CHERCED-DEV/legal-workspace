# -*- coding: utf-8 -*-
"""esqueleto_de_modelo — qué forma tiene el documento que ella dio de ejemplo.

    python esqueleto_de_modelo.py <modelo> [--salida esqueleto.json]
                                  [--ver] [--umbral 1.0] [--umbral-cobertura 0.98]

QUE ABRE. .docx y .md/.txt directamente. PDF, .doc, .rtf, .odt, .html y
plantillas de Word, convirtiendolos con el Word instalado (sin Word, el PDF se
lee con pypdf y la estructura sale aproximada: lo dice). Imagenes y PDF
escaneados, con el OCR local. Nada sale del computador.

PARA QUE. Cuando ella entrega un documento suyo como modelo, lo que se copia es
la FORMA -- que apartados lleva, en que orden, con que nombres y con que
formulas fijas -- y nunca el contenido. Este programa saca esa forma y, sobre
todo, **mide si la saco entera**.

LA MEDIDA, QUE ES LO QUE IMPORTA. Decir «entendi el documento» no significa
nada. Aqui significa dos cosas comprobables:

1. Reconstruccion interna: con lo extraido se vuelve a armar cada parrafo y
   tiene que salir identico. Mide que la plantilla no pierde nada.
2. Cobertura contra el original: las palabras del documento, leidas por OTRA
   via (el XML crudo del .docx, o pypdf sobre el PDF), tienen que estar todas
   en lo extraido, y ninguna de mas. **Sin esta segunda medida la primera es
   circular**: compara lo extraido consigo mismo, y dio «100 %» sobre una
   lectura que repetia cada celda combinada cinco veces y tenia 22 apartados
   inventados. El instrumento aprobaba su propio defecto.

«Reconstruye el 97 %» no es un aprobado: es un aviso de que hay un 3 % que
nadie miro. Y una lectura por OCR no tiene segunda via: sale, pero NO MEDIDA,
y el programa termina con codigo 3 para que nadie la tome por medida.

LO QUE NO HACE. No redacta, no rellena y no opina sobre el contenido. Marcar
que un dato es variable **no es saber cual va**: los valores que extrae son los
del modelo -- de otro caso, de otras personas -- y no se copian nunca. En el
documento nuevo, cada uno de esos huecos es un hueco hasta que alguien lo
llene con material del caso.
"""
import argparse, io, json, os, re, subprocess, sys, tempfile, unicodedata
from collections import Counter

SEPARADOR = "\n"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
CON_WORD = {".doc", ".dot", ".dotx", ".dotm", ".docm", ".rtf", ".odt", ".wpd",
            ".wps", ".htm", ".html", ".mht", ".mhtml", ".xml"}
IMAGENES = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}

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
    # Una sigla o palabra en mayusculas, EN CUALQUIER SITIO. Sin esta, la sigla
    # de una entidad sola en una celda de responsable pasaba por formula fija
    # -- no va a mitad de frase -- y se habria copiado a la nueva acta.
    ("sigla", re.compile(r"\b[A-ZÁÉÍÓÚÑ]{3,}\b")),
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


def _en_fallback(e):
    """El XML de Word guarda cada cuadro de texto DOS veces (mc:Choice y
    mc:Fallback). Leer los dos duplicaba el texto sin que se notara."""
    return any(a.tag.endswith("}Fallback") for a in e.iterancestors())


def _mayusculas(t):
    # 90 % y no 100 %: el OCR devuelve «REUNIóN», con la vocal tildada en
    # minuscula, y el apartado se perdia.
    letras = [c for c in t if c.isalpha()]
    return bool(letras) and sum(c.isupper() for c in letras) >= 0.9 * len(letras)


def leer_docx(ruta):
    """Cada pieza del documento, en el orden en que va, sin saltarse tablas.

    Recorre el cuerpo por el XML y no por `paragraphs`, porque esa lista **se
    salta las tablas** -- y en un acta los asistentes suelen ir en una.

    Tres cosas que la version anterior hacia mal y NO se notaba:
    - Una celda combinada, python-docx la devuelve una vez POR COLUMNA que
      ocupa. Se leia «DATOS GENERALES» cinco veces. Ahora se lee una.
    - Los controles de contenido (w:sdt) y los cuadros de texto no son hijos
      directos del cuerpo: se saltaban enteros.
    - Encabezado y pie de pagina no se leian: son el membrete, y van aparte."""
    try:
        import docx
        from docx.table import Table
        from docx.text.paragraph import Paragraph
    except ImportError:
        falla("hace falta python-docx para leer un .docx (pip install python-docx)")
    d = docx.Document(ruta)
    piezas = []

    def parrafo(p, dentro=None, fila_unica=False):
        piezas.append({"clase": "parrafo", "estilo": p.style.name if p.style else "",
                       "texto": _norm(p.text), "dentro": dentro, "fila_unica": fila_unica})
        for tx in p._p.iter(W + "txbxContent"):
            if _en_fallback(tx):
                continue
            for q in tx.iter(W + "p"):
                piezas.append({"clase": "parrafo", "estilo": "",
                               "texto": _norm("".join(t.text or "" for t in q.iter(W + "t"))),
                               "dentro": "cuadro de texto", "fila_unica": False})

    def tabla(elem):
        t = Table(elem, d)
        piezas.append({"clase": "tabla_inicio", "filas": len(t.rows),
                       "columnas": len(t.columns), "texto": "", "estilo": "", "dentro": None})
        tras_cabecera = False
        for i, fila in enumerate(t.rows):
            distintas = []
            for celda in fila.cells:
                if not any(celda._tc is c._tc for c in distintas):
                    distintas.append(celda)
            textos = [_norm(c.text) for c in distintas]
            cabecera = (len(distintas) >= 2 and all(textos)
                        and all(_mayusculas(x) and not x.endswith(":") for x in textos))
            for j, celda in enumerate(distintas):
                for hijo in celda._tc.iterchildren():
                    if hijo.tag == W + "p":
                        parrafo(Paragraph(hijo, celda), dentro="tabla[%d,%d]" % (i, j),
                                fila_unica=len(distintas) == 1)
                        if cabecera:
                            piezas[-1]["cabecera_de_columna"] = True
                        elif tras_cabecera:
                            piezas[-1]["fila_de_datos"] = True
                    elif hijo.tag == W + "tbl":
                        tabla(hijo)
            tras_cabecera = tras_cabecera or cabecera
        piezas.append({"clase": "tabla_fin", "texto": "", "estilo": "", "dentro": None})

    def recorrer(padre):
        for hijo in padre.iterchildren():
            if hijo.tag == W + "p":
                parrafo(Paragraph(hijo, d))
            elif hijo.tag == W + "tbl":
                tabla(hijo)
            elif hijo.tag == W + "sdt":
                for c in hijo.iterchildren(W + "sdtContent"):
                    recorrer(c)

    recorrer(d.element.body)

    vistos = set()
    for s in d.sections:
        for parte in (s.header, s.first_page_header, s.even_page_header,
                      s.footer, s.first_page_footer, s.even_page_footer):
            try:
                if parte.is_linked_to_previous:
                    continue
                elems = parte._element.iter(W + "p")
            except Exception:
                continue
            for q in elems:
                if _en_fallback(q):
                    continue
                txt = _norm("".join(t.text or "" for t in q.iter(W + "t")))
                if txt and txt not in vistos:
                    vistos.add(txt)
                    piezas.append({"clase": "membrete", "texto": txt, "estilo": "",
                                   "dentro": "encabezado o pie de página"})
    return piezas


def texto_crudo_docx(ruta):
    """El texto del .docx leido por OTRA via: el XML crudo, sin python-docx.
    Es la segunda lectura contra la que se mide la primera."""
    import zipfile
    import xml.etree.ElementTree as ET
    trozos = []

    def baja(e):
        if e.tag.endswith("}Fallback"):
            return
        if e.tag == W + "t":
            trozos.append(e.text or "")
        for h in e:
            baja(h)
    with zipfile.ZipFile(ruta) as z:
        for n in z.namelist():
            if re.match(r"word/(document|header\d*|footer\d*)\.xml$", n):
                baja(ET.fromstring(z.read(n)))
    return " ".join(trozos)


def convertir_con_word(ruta):
    """El documento pasado a .docx por el Word instalado. Las rutas van por
    variables de entorno y no en la linea de ordenes: una tilde en el nombre
    del archivo («grabación») llegaba rota por el shell."""
    if os.name != "nt":
        return None, "Word solo se puede usar en Windows"
    tmp = tempfile.mkdtemp(prefix="esqueleto_")
    salida = os.path.join(tmp, "convertido.docx")
    ps = ("$ErrorActionPreference='Stop';"
          "$w=New-Object -ComObject Word.Application;$w.Visible=$false;$w.DisplayAlerts=0;"
          "try{$d=$w.Documents.Open($env:ESQ_ORIGEN,$false,$true,$false);"
          "$d.SaveAs2($env:ESQ_DESTINO,16);$d.Close($false)}finally{$w.Quit()}")
    env = dict(os.environ, ESQ_ORIGEN=os.path.abspath(ruta), ESQ_DESTINO=salida)
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                           env=env, capture_output=True, timeout=300)
    except Exception as e:
        return None, "no se pudo llamar a Word (%s)" % e
    if r.returncode != 0 or not os.path.isfile(salida):
        err = (r.stderr or b"").decode("utf-8", "replace").strip().splitlines()
        return None, "Word no lo convirtió (%s)" % (err[0][:160] if err else "sin mensaje")
    return salida, None


def _clave(t):
    return re.sub(r"\d+", "#", _norm(t).lower())


def lineas_pdf(ruta):
    try:
        import pypdf
    except ImportError:
        falla("hace falta pypdf para leer un PDF (pip install pypdf)")
    r = pypdf.PdfReader(ruta)
    return [[_norm(l) for l in (p.extract_text() or "").split("\n") if _norm(l)]
            for p in r.pages]


def membrete_pdf(paginas):
    """Los renglones que se repiten arriba o abajo de TODAS las paginas: el
    membrete. Los numeros se igualan, porque «Pagina 1 de 2» y «Pagina 2 de 2»
    son el mismo renglon."""
    if len(paginas) < 2:
        return set()
    borde = lambda pg: set(_clave(l) for l in pg[:6] + pg[-6:])
    comunes = borde(paginas[0])
    for pg in paginas[1:]:
        comunes &= borde(pg)
    return comunes


def marcar_membrete_y_saltos(piezas, membrete):
    """En un PDF convertido, el membrete sale como texto del cuerpo una vez por
    pagina, y parte los apartados; y un parrafo cortado por el salto de pagina
    sale como dos. Lo primero se aparta; lo segundo se vuelve a unir, solo si
    el primero no cierra frase y el segundo empieza en minuscula."""
    for p in piezas:
        if p["clase"] == "parrafo" and p["texto"] and _clave(p["texto"]) in membrete:
            p["clase"] = "membrete"
    abierto, cruzo = None, False
    for p in piezas:
        if p["clase"] == "membrete":
            cruzo = abierto is not None
            continue
        if p["clase"] != "parrafo" or not p["texto"]:
            continue
        t = p["texto"]
        if (abierto is not None and cruzo and t[:1].islower()
                and not re.search(r"[.:;!?»\")]$", abierto["texto"])):
            abierto["texto"] = abierto["texto"] + " " + t
            p["clase"], p["unido_a_la_pieza_anterior"] = "continuacion", True
            cruzo = False
            continue
        abierto, cruzo = p, False
    return piezas


def piezas_pdf_sin_word(paginas, membrete):
    """Sin Word: renglones de pypdf agrupados en parrafos. No hay tablas, y
    por eso se declara aproximada."""
    piezas, actual = [], []
    largos = sorted(len(l) for pg in paginas for l in pg) or [80]
    lleno = largos[int(len(largos) * 0.8)]

    def cierra():
        if actual:
            piezas.append({"clase": "parrafo", "estilo": "", "texto": _norm(" ".join(actual)),
                           "dentro": None})
            del actual[:]
    for pg in paginas:
        for l in pg:
            if _clave(l) in membrete:
                piezas.append({"clase": "membrete", "texto": l, "estilo": "", "dentro": None})
                continue
            if es_titulo({"clase": "parrafo", "texto": l}):
                cierra()
                piezas.append({"clase": "parrafo", "estilo": "", "texto": l, "dentro": None})
                continue
            actual.append(l)
            if l.endswith((".", ":")) and len(l) < 0.85 * lleno:
                cierra()
    cierra()
    return piezas


def ocr_piezas(imagenes):
    """Texto de imagenes con el OCR local, en renglones agrupados en parrafos
    por la distancia vertical. Sin segunda via de lectura: NO MEDIDO."""
    try:
        from rapidocr_onnxruntime import RapidOCR
        import numpy as np
    except ImportError:
        falla("hace falta rapidocr-onnxruntime para leer imágenes o PDF escaneados")
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        from preparar_material import OCR_CTOR, OCR_CALL, REC_ONNX, REC_DICT
        ctor = dict(OCR_CTOR)
        if REC_ONNX.exists() and REC_DICT.exists():
            ctor.update(rec_model_path=str(REC_ONNX), rec_keys_path=str(REC_DICT))
    except Exception:
        ctor, OCR_CALL = {}, {}
    ocr = RapidOCR(**ctor)
    piezas = []
    for im in imagenes:
        res, _ = ocr(np.asarray(im.convert("RGB")), **OCR_CALL)
        cajas = []
        for caja, texto, _conf in (res or []):
            ys = [pt[1] for pt in caja]
            cajas.append((min(ys), max(ys), min(pt[0] for pt in caja), texto))
        cajas.sort()
        renglones = []
        for y0, y1, x, t in cajas:
            if renglones and abs((y0 + y1) / 2 - renglones[-1]["yc"]) < 0.5 * (y1 - y0):
                renglones[-1]["t"].append((x, t))
            else:
                renglones.append({"yc": (y0 + y1) / 2, "y0": y0, "y1": y1, "t": [(x, t)]})
        altos = sorted(r["y1"] - r["y0"] for r in renglones) or [20]
        alto = altos[len(altos) // 2]
        actual, fin_previo = [], None
        for r in renglones:
            linea = _norm("  ".join(t for _, t in sorted(r["t"])))
            if fin_previo is not None and r["y0"] - fin_previo > 0.9 * alto and actual:
                piezas.append({"clase": "parrafo", "estilo": "", "texto": _norm(" ".join(actual)),
                               "dentro": None})
                actual = []
            actual.append(linea)
            fin_previo = r["y1"]
        if actual:
            piezas.append({"clase": "parrafo", "estilo": "", "texto": _norm(" ".join(actual)),
                           "dentro": None})
    return piezas


def imagenes_de_pdf(ruta):
    import pypdf
    fuera = []
    for p in pypdf.PdfReader(ruta).pages:
        ims = list(p.images)
        if ims:
            fuera.append(max(ims, key=lambda i: len(i.data)).image)
    return fuera


def palabras(texto):
    return re.findall(r"\w+", unicodedata.normalize("NFC", texto or "").lower())


def cobertura(independiente, piezas):
    """Cuanto del original (leido por otra via) esta en lo extraido, y cuanto
    de lo extraido NO esta en el original (repetido o inventado)."""
    a = Counter(palabras(independiente))
    b = Counter(w for p in piezas if p["clase"] in ("parrafo", "membrete")
                for w in palabras(p["texto"]))
    faltan, sobran = a - b, b - a
    return (1 - sum(faltan.values()) / max(sum(a.values()), 1),
            sum(sobran.values()) / max(sum(b.values()), 1), faltan, sobran)


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
    if pieza["clase"] != "parrafo" or pieza.get("cabecera_de_columna"):
        return False
    if re.match(r"^(Heading|T[ií]tulo)\s*\d", pieza.get("estilo") or "", re.I):
        return True
    # Dentro de una tabla, solo una banda que ocupa la fila entera es apartado.
    # Una celda entre otras es un rotulo o un valor: «MESA DE TRABAJO …» en
    # mayusculas es el valor de un campo, no un apartado.
    if (pieza.get("dentro") or "").startswith("tabla") and not pieza.get("fila_unica"):
        return False
    t = pieza["texto"]
    if not t or len(t) > 90 or t.endswith(":"):
        return False
    mayusculas = _mayusculas(t)
    # «DESARROLLO DE LA REUNIÓN.» es un apartado aunque lleve punto; una frase
    # corriente con punto no lo es.
    if t.endswith(".") and not (mayusculas and len(t.split()) <= 8):
        return False
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
        # La cabecera de una tabla y el rotulo de un campo («Dirigió:») son
        # forma aunque vayan en mayusculas: se copian, y no llevan dato.
        rotulo = p.get("cabecera_de_columna") or (
            (p.get("dentro") or "").startswith("tabla") and p["texto"].endswith(":")
            and len(p["texto"]) <= 60)
        plant, datos = (p["texto"], []) if rotulo else plantilla_de(p["texto"])
        # Debajo de una cabecera de columnas, cada fila es un registro del otro
        # caso ENTERO: «Remitir información sobre…» no tiene ni una cifra ni un
        # nombre, y pasaba por formula fija -- se habria copiado tal cual.
        if p.get("fila_de_datos") and not rotulo and p["texto"]:
            plant, datos = "{celda:0}", [{"ranura": "celda:0", "valor_en_el_modelo": p["texto"]}]
        pieza = dict(p, i=i, plantilla=plant, datos=datos,
                     tipo=("formula" if not datos and p["texto"] else
                           "mixto" if datos and re.search(r"\w", re.sub(r"\{\w+:\d+\}", "", plant)) else
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
    ap.add_argument("--umbral-cobertura", type=float, default=0.98,
                    help="qué proporción de las palabras del original tiene que estar en lo "
                         "extraído (ELEGIDO, no medido: deja margen a cómo parte palabras cada lector)")
    ap.add_argument("--forzar", action="store_true")
    a = ap.parse_args()

    if not os.path.isfile(a.modelo):
        falla("no está el modelo: %s" % a.modelo)
    if a.salida and os.path.exists(a.salida) and not a.forzar:
        falla("ya existe %s. Regenerar produce versión nueva, nunca sobrescribe (ADR-011 §8)" % a.salida)

    ext = os.path.splitext(a.modelo)[1].lower()
    via, independiente, avisos = "", None, []
    if ext == ".docx":
        piezas, via = leer_docx(a.modelo), "python-docx"
        independiente = texto_crudo_docx(a.modelo)
    elif ext in (".md", ".txt"):
        piezas, via = leer_md(a.modelo), "texto"
        independiente = io.open(a.modelo, encoding="utf-8").read()
    elif ext == ".pdf":
        paginas = lineas_pdf(a.modelo)
        letras = sum(len(l) for pg in paginas for l in pg)
        if letras < 40 * max(len(paginas), 1):
            piezas, via = ocr_piezas(imagenes_de_pdf(a.modelo)), "OCR (PDF escaneado)"
        else:
            independiente = "\n".join(l for pg in paginas for l in pg)
            membrete = membrete_pdf(paginas)
            convertido, error = convertir_con_word(a.modelo)
            if convertido:
                piezas, via = leer_docx(convertido), "Word (PDF convertido) + python-docx"
                marcar_membrete_y_saltos(piezas, membrete)
            else:
                avisos.append("Sin Word (%s): estructura APROXIMADA, sin tablas." % error)
                piezas, via = piezas_pdf_sin_word(paginas, membrete), "pypdf (sin Word)"
    elif ext in CON_WORD:
        convertido, error = convertir_con_word(a.modelo)
        if not convertido:
            falla("%s solo se puede leer convirtiéndolo con Word, y %s" % (ext, error))
        piezas, via = leer_docx(convertido), "Word (%s convertido) + python-docx" % ext
        independiente = texto_crudo_docx(convertido)
        avisos.append("La segunda lectura sale del mismo .docx que convirtió Word: mide la "
                      "lectura, NO la conversión.")
    elif ext in IMAGENES:
        try:
            from PIL import Image
        except ImportError:
            falla("hace falta pillow para abrir una imagen")
        piezas, via = ocr_piezas([Image.open(a.modelo)]), "OCR (imagen)"
    else:
        falla("no sé abrir %s. Se abren: .docx .md .txt .pdf %s y las imágenes %s"
              % (ext or "sin extensión", " ".join(sorted(CON_WORD)), " ".join(sorted(IMAGENES))))

    apartados, sueltas = analizar(piezas)

    # LA COMPROBACION. Con lo extraido se rearma el original; lo que no cuadre
    # es exactamente lo que la lectura se dejo.
    original = [p["texto"] for p in piezas if p["clase"] == "parrafo"]
    vuelto = rearmar(apartados, sueltas)
    iguales = sum(1 for x, y in zip(original, vuelto) if x == y)
    proporcion = iguales / max(len(original), 1)

    print("\n%s" % os.path.basename(a.modelo))
    print("Leído con: %s" % via)
    for av in avisos:
        print("AVISO: %s" % av)
    print("Piezas: %d párrafos, %d apartados, %d tablas, %d renglones de membrete"
          % (len(original), len(apartados), sum(1 for p in piezas if p["clase"] == "tabla_inicio"),
             sum(1 for p in piezas if p["clase"] == "membrete")))
    unidos = sum(1 for p in piezas if p.get("unido_a_la_pieza_anterior"))
    if unidos:
        print("Párrafos cortados por un salto de página y vueltos a unir: %d" % unidos)
    print("1. Reconstrucción interna: %d de %d (%.1f %%)" % (iguales, len(original), 100 * proporcion))
    cub, sob = None, None
    if independiente is None:
        print("2. Cobertura contra el original: NO MEDIBLE — %s no tiene segunda vía de lectura."
              " Esta forma hay que confirmarla mirando el original." % via)
    else:
        cub, sob, faltan, sobran = cobertura(independiente, piezas)
        print("2. Cobertura contra el original (palabras leídas por otra vía): %.1f %% presentes,"
              " %.1f %% de más" % (100 * cub, 100 * sob))
        if faltan:
            print("   faltan: %s" % ", ".join("«%s»×%d" % kv for kv in faltan.most_common(10)))
        if sobran:
            print("   sobran: %s" % ", ".join("«%s»×%d" % kv for kv in sobran.most_common(10)))

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
        print("\nLa forma, pieza a pieza. {ranura} = dato del otro caso, NO se copia:")
        for grupo, titulo in [(sueltas, "(antes del primer apartado)")] + \
                             [(a2["piezas"], a2["titulo"]) for a2 in apartados]:
            print("  ▸ %s" % titulo[:70])
            fila_cab = []
            for p in grupo:
                if p.get("cabecera_de_columna"):
                    fila_cab.append(p["texto"])
                    continue
                if fila_cab:
                    print("      [columnas de tabla] %s" % " | ".join(fila_cab))
                    fila_cab = []
                if p.get("clase") == "membrete":
                    print("      [membrete] %s" % _clave(p["texto"])[:80])
                elif p.get("tipo") in ("formula", "mixto", "dato"):
                    print("      [%s] %s" % (p["tipo"], p["plantilla"][:110]))
            if fila_cab:
                print("      [columnas de tabla] %s" % " | ".join(fila_cab))

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
    if cub is not None and (cub < a.umbral_cobertura or sob > 1 - a.umbral_cobertura):
        falla("la lectura cubre el %.1f %% del original y trae un %.1f %% de más. Por debajo "
              "de %.1f %% (o por encima de %.1f %% de más) lo extraído NO es el documento."
              % (100 * cub, 100 * sob, 100 * a.umbral_cobertura, 100 * (1 - a.umbral_cobertura)))
    if cub is None:
        sys.stderr.write("\nNO MEDIDO: forma leída sin segunda vía (%s). Confírmela mirando "
                         "el original antes de usarla.\n" % via)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
