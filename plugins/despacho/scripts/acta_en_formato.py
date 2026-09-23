# -*- coding: utf-8 -*-
"""acta_en_formato — el acta con el membrete y la forma del despacho.

    python acta_en_formato.py <acta.md> <salida.docx> --formato <formato.json>
                              [--escudo <imagen>]

POR QUE NO VALE EL CONVERSOR DE SIEMPRE. `md2docx.py` entrega bien cualquier
documento de trabajo, pero un acta institucional **circula con la cara de la
entidad**: escudo, titulo repetido en cada pagina, direccion al pie, «Pagina N
de M», y una tabla de datos generales con un reparto fijo. Eso no es adorno --
es lo que hace que el documento se reconozca como suyo.

DE DONDE SALE LA FORMA. De un `formato.json` que describe el membrete de ESA
entidad: que dice el titulo, que direccion va al pie, que tipografias usa. Ese
archivo se escribe UNA vez por despacho y **no vive en el repositorio**, porque
nombra a la entidad.

LO QUE NO HACE. No redacta, no rellena huecos y no inventa un membrete: si el
formato no trae escudo, sale sin escudo y lo dice. Los datos del acta salen del
.md que se le pasa, y de ningun otro sitio.
"""
import argparse, io, json, os, re, sys

MARCA = re.compile(r"\[\[(FALTA[^\]]*|LE TOCA A USTED[^\]]*)\]\]")


def falla(msg):
    sys.stderr.write("\nDETENIDO: " + msg + "\n")
    raise SystemExit(2)


def campo(doc, etiqueta, valor, F):
    from docx.shared import Pt
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(etiqueta + " ")
    r.bold = True
    r.font.name, r.font.size = F["cuerpo"], Pt(F["tam_cuerpo"])
    r2 = p.add_run(valor)
    r2.font.name, r2.font.size = F["cuerpo"], Pt(F["tam_cuerpo"])
    return p


def numero_de_pagina(parrafo):
    """«Pagina N de M». Word lo calcula solo; hay que meterle los campos."""
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    for texto, instruccion in ((None, "PAGE"), (None, "NUMPAGES")):
        if instruccion == "NUMPAGES":
            parrafo.add_run(" de ")
        r = parrafo.add_run()._r
        for tipo, contenido in (("begin", None), ("instrText", instruccion), ("end", None)):
            e = OxmlElement("w:fldChar") if tipo != "instrText" else OxmlElement("w:instrText")
            if tipo == "instrText":
                e.set(qn("xml:space"), "preserve")
                e.text = " %s " % contenido
            else:
                e.set(qn("w:fldCharType"), tipo)
            r.append(e)


def encabezado(doc, F, escudo):
    """El escudo, el titulo y la direccion — en el ENCABEZADO, para que se
    repita en todas las paginas sin copiarlo a mano."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, Cm
    sec = doc.sections[0]
    cab = sec.header
    cab.is_linked_to_previous = False
    for p in list(cab.paragraphs):
        p._element.getparent().remove(p._element)

    t = cab.add_table(rows=1, cols=2, width=sec.page_width - sec.left_margin - sec.right_margin)
    t.autofit = True
    izq, der = t.rows[0].cells
    if escudo and os.path.isfile(escudo):
        izq.paragraphs[0].add_run().add_picture(escudo, height=Cm(F.get("alto_escudo_cm", 1.6)))
    else:
        izq.paragraphs[0].add_run(F.get("entidad", ""))
    p = der.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(F["titulo"])
    r.bold = True
    r.font.name, r.font.size = F["titulo_fuente"], Pt(F["titulo_tam"])

    for linea in F.get("direccion", []):
        q = cab.add_paragraph()
        q.alignment = WD_ALIGN_PARAGRAPH.CENTER
        q.paragraph_format.space_after = Pt(0)
        rr = q.add_run(linea)
        rr.font.name, rr.font.size = F["cuerpo"], Pt(F.get("tam_pie", 8))

    q = cab.add_paragraph()
    q.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rr = q.add_run("Página ")
    rr.font.name, rr.font.size = F["cuerpo"], Pt(F.get("tam_pie", 8))
    numero_de_pagina(q)
    for r2 in q.runs:
        r2.font.name, r2.font.size = F["cuerpo"], Pt(F.get("tam_pie", 8))


def fila_titulo(tabla, texto, F, columnas):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt
    fila = tabla.add_row()
    celda = fila.cells[0]
    for otra in fila.cells[1:]:
        celda = celda.merge(otra)
    celda.text = ""
    p = celda.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(texto)
    r.bold = True
    r.font.name, r.font.size = F["cuerpo"], Pt(F["tam_cuerpo"])
    return fila


def leer_acta(md):
    """Parte el .md en sus piezas. No interpreta: reparte."""
    campos, desarrollo, compromisos, cierre, dirigio = [], [], [], [], []
    donde = None
    for linea in md.split("\n"):
        t = linea.rstrip()
        if t.startswith("## "):
            n = t[3:].strip().upper()
            donde = ("campos" if "DATOS GENERALES" in n else
                     "desarrollo" if "DESARROLLO" in n else
                     "compromisos" if "COMPROMISOS" in n else "cierre")
            continue
        if t.startswith("# ") or t.strip() in ("---", ""):
            continue
        if t.startswith("**Dirigió:**"):
            dirigio.append(t)
            donde = "dirigio"
            continue
        if donde == "dirigio" and not t.startswith("##"):
            dirigio.append(t)
            continue
        {"campos": campos, "desarrollo": desarrollo,
         "compromisos": compromisos, "cierre": cierre}.get(donde, cierre).append(t)
    return campos, desarrollo, compromisos, cierre, dirigio


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("acta")
    ap.add_argument("salida")
    ap.add_argument("--formato", required=True, help="el .json que describe el membrete")
    ap.add_argument("--escudo", default=None)
    ap.add_argument("--forzar", action="store_true")
    a = ap.parse_args()

    for p, q in ((a.acta, "el acta"), (a.formato, "el formato")):
        if not os.path.isfile(p):
            falla("no está %s: %s" % (q, p))
    if os.path.exists(a.salida) and not a.forzar:
        falla("ya existe %s. Regenerar produce versión nueva, nunca sobrescribe (ADR-011 §8)" % a.salida)

    try:
        import docx
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.shared import Pt, Cm
    except ImportError:
        falla("hace falta python-docx (pip install python-docx)")

    F = json.load(io.open(a.formato, encoding="utf-8"))
    for k in ("titulo", "cuerpo", "tam_cuerpo", "titulo_fuente", "titulo_tam"):
        if k not in F:
            falla("al formato le falta «%s»" % k)
    escudo = a.escudo or F.get("escudo")
    if escudo and not os.path.isabs(escudo):
        escudo = os.path.join(os.path.dirname(os.path.abspath(a.formato)), escudo)

    campos, desarrollo, compromisos, cierre, dirigio = leer_acta(
        io.open(a.acta, encoding="utf-8").read())

    doc = docx.Document()
    sec = doc.sections[0]
    sec.top_margin, sec.bottom_margin = Cm(F.get("margen_sup_cm", 3.2)), Cm(2)
    sec.left_margin = sec.right_margin = Cm(F.get("margen_lat_cm", 2.1))
    encabezado(doc, F, escudo)

    ancho = sec.page_width - sec.left_margin - sec.right_margin
    t = doc.add_table(rows=0, cols=2)
    t.style = "Table Grid"
    fila_titulo(t, "DATOS GENERALES", F, 2)
    for linea in campos:
        m = re.match(r"^\*\*(.+?):\*\*\s*(.*)$", linea)
        if not m:
            continue
        fila = t.add_row()
        # El rotulo va COMO LO ESCRIBE EL MODELO, no en mayusculas: el modelo
        # pone «Acta No:» y «Fecha:», y cambiarlo seria inventar su forma.
        for celda, texto, negrita in ((fila.cells[0], m.group(1) + ":", True),
                                      (fila.cells[1], limpio(m.group(2)), False)):
            celda.text = ""
            r = celda.paragraphs[0].add_run(texto)
            r.bold = negrita
            r.font.name, r.font.size = F["cuerpo"], Pt(F["tam_cuerpo"])

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    r = p.add_run("DESARROLLO DE LA REUNIÓN.")
    r.bold = True
    r.font.name, r.font.size = F["cuerpo"], Pt(F["tam_cuerpo"])

    for linea in desarrollo:
        if not linea.strip():
            continue
        q = doc.add_paragraph()
        q.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        cursiva = linea.startswith(">")
        texto = linea.lstrip("> ").strip()
        for trozo, es_marca in partir(texto):
            r = q.add_run(trozo)
            r.font.name, r.font.size = F["cuerpo"], Pt(F["tam_cuerpo"])
            r.italic = cursiva
            if es_marca:
                r.bold = True

    filas = [l for l in compromisos if l.strip().startswith("|")
             and not re.match(r"^\|[\s|:-]+\|$", l.strip())]
    if filas:
        p = doc.add_paragraph()
        cuerpo = [[c.strip() for c in f.strip().strip("|").split("|")] for f in filas]
        tc = doc.add_table(rows=0, cols=len(cuerpo[0]))
        tc.style = "Table Grid"
        fila_titulo(tc, "COMPROMISOS", F, len(cuerpo[0]))
        for i, cols in enumerate(cuerpo):
            fila = tc.add_row()
            for celda, texto in zip(fila.cells, cols):
                celda.text = ""
                pp = celda.paragraphs[0]
                if i == 0:
                    pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = pp.add_run(texto)
                r.bold = (i == 0)
                r.font.name, r.font.size = F["cuerpo"], Pt(F["tam_cuerpo"])

    if dirigio:
        doc.add_paragraph()
        for i, linea in enumerate(dirigio):
            texto = linea.replace("**", "").strip()
            q = doc.add_paragraph()
            q.paragraph_format.space_after = Pt(0)
            r = q.add_run(texto)
            r.bold = (i == 1)
            r.font.name, r.font.size = F["cuerpo"], Pt(F["tam_cuerpo"])

    if cierre:
        doc.add_page_break()
        for linea in cierre:
            if not linea.strip():
                continue
            estilo = None
            texto = linea
            if linea.startswith("## "):
                texto, estilo = linea[3:], "titulo"
            q = doc.add_paragraph()
            q.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            for trozo, es_marca in partir(texto.lstrip("> ").strip()):
                r = q.add_run(trozo)
                r.font.name = F["cuerpo"]
                r.font.size = Pt(F["tam_cuerpo"] if estilo else F["tam_cuerpo"] - 1)
                r.bold = bool(estilo) or es_marca

    doc.save(a.salida)
    huecos = sum(len(MARCA.findall(l)) for l in desarrollo + compromisos)
    print("OK  %s" % os.path.basename(a.salida))
    print("   %d párrafos de desarrollo · %d filas de compromisos · %d huecos marcados"
          % (len([l for l in desarrollo if l.strip()]), max(len(filas) - 1, 0), huecos))
    if not (escudo and os.path.isfile(escudo)):
        print("   AVISO: sin escudo — el formato no trae imagen, y no me la invento.")
    return 0


def partir(texto):
    """El texto, separando las marcas de hueco para poder resaltarlas."""
    fuera, ultimo = [], 0
    for m in MARCA.finditer(texto):
        if m.start() > ultimo:
            fuera.append((limpio(texto[ultimo:m.start()]), False))
        fuera.append(("[[" + m.group(1) + "]]", True))
        ultimo = m.end()
    if ultimo < len(texto):
        fuera.append((limpio(texto[ultimo:]), False))
    return fuera or [(limpio(texto), False)]


def limpio(t):
    return t.replace("**", "").replace("⚠", "").strip() + (" " if t.endswith(" ") else "")


if __name__ == "__main__":
    sys.exit(main())
