#!/usr/bin/env python
"""
Control de fidelidad Markdown -> Word.

Comprueba que la conversion no perdio contenido. NO es una comparacion exacta:
mide que fraccion de las palabras del .md aparece en el .docx, ignorando la
puntuacion de Markdown.

Por que existe: en el primer uso real, forzar el titulo desde la linea de
comandos hacia desaparecer la linea de descargo que iba debajo del titulo
("Propuesta para su revision. Nada de esto esta comprobado por ningun
sistema."). Se veia bien y faltaba justo la frase que no puede faltar. Este
script lo detecto; una lectura por encima no lo habria detectado.

Uso:
    python verificar-fidelidad.py salida.docx entrada.md
    python verificar-fidelidad.py --pares lista.txt      (una linea "docx<TAB>md")

Umbrales:
    >= 99 %   ok
    95-99 %   REVISAR  (suele ser ruido de la propia medicion: etiquetas con
                        dos puntos que en el Word quedan sin ellos)
    < 95 %    PERDIDA  (hay que mirar que falta, de verdad)

Requiere: python-docx
"""
import re
import sys
from pathlib import Path


def normaliza(texto: str) -> str:
    """Quita la puntuacion propia de Markdown y colapsa espacios."""
    texto = re.sub(r"[*`|>#_-]", " ", texto)
    return re.sub(r"\s+", " ", texto).strip().lower()


def texto_del_docx(ruta: str) -> str:
    # Declarar, no reventar. `INSTALACION.md` promete que «las bibliotecas las
    # pide cada programa cuando le hacen falta, DICIENDO CUAL», y este las
    # pedia con un traceback de Python en la pantalla de quien instala. Es el
    # programa que comprueba que el Word diga lo mismo que el .md, y lo
    # declaran nueve metodos: reventar aqui es reventar el control de la
    # entrega, en el sitio donde menos se puede.
    try:
        from docx import Document
    except ImportError:
        sys.stderr.write(
            "FALTA python-docx, y este control no existe sin el.\n"
            "  El .docx se entrega igual -- lo produce md2docx.py -- pero NADIE\n"
            "  habra comprobado que diga lo mismo que el .md. Digalo en la\n"
            "  entrega: «no se pudo comprobar la fidelidad del Word».\n"
            "  pip install python-docx\n")
        raise SystemExit(3)

    doc = Document(ruta)
    partes = [p.text for p in doc.paragraphs]
    partes += [c.text for t in doc.tables for f in t.rows for c in f.cells]
    return normaliza(" ".join(partes))


def compara(ruta_docx: str, ruta_md: str):
    # Un archivo que no esta se DICE. Antes salia un traceback de Python con
    # `FileNotFoundError`, que en la pantalla de quien instala no distingue
    # «te equivocaste al teclear la ruta» de «este programa esta roto».
    for ruta, que in ((ruta_md, "el .md de origen"), (ruta_docx, "el .docx")):
        if not Path(ruta).exists():
            sys.stderr.write("NO EXISTE %s: %s\n"
                             "  Se comprueba un .docx contra el .md del que salio.\n"
                             "  Uso: python verificar_fidelidad.py <salida.docx> <entrada.md>\n"
                             % (que, ruta))
            raise SystemExit(2)
    origen = normaliza(open(ruta_md, encoding="utf-8").read())
    destino = texto_del_docx(ruta_docx)

    # Solo palabras largas: las cortas generan ruido y no distinguen nada.
    palabras = [p for p in set(origen.split()) if len(p) > 5]
    if not palabras:
        return 100.0, []
    faltan = sorted(p for p in palabras if p not in destino)
    retencion = 100.0 * (len(palabras) - len(faltan)) / len(palabras)
    return retencion, faltan


def veredicto(retencion: float) -> str:
    if retencion >= 99:
        return "ok"
    if retencion >= 95:
        return "REVISAR"
    return "PERDIDA"


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help", "ayuda"):
        sys.stdout.write(__doc__)
        return 0
    if len(argv) == 3 and argv[1] == "--pares":
        pares = [
            linea.rstrip("\n").split("\t")
            for linea in open(argv[2], encoding="utf-8")
            if linea.strip()
        ]
    elif len(argv) == 3:
        pares = [(argv[1], argv[2])]
    else:
        print(__doc__)
        return 2

    problemas = 0
    for ruta_docx, ruta_md in pares:
        retencion, faltan = compara(ruta_docx, ruta_md)
        marca = veredicto(retencion)
        nombre = ruta_docx.split("\\")[-1].split("/")[-1]
        print(f"{nombre[:52]:54s} {retencion:5.1f}%  {marca}")
        if marca != "ok":
            print("    faltan:", ", ".join(faltan[:25]))
            if marca == "PERDIDA":
                problemas += 1
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
