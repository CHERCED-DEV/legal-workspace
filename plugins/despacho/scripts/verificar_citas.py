# -*- coding: utf-8 -*-
"""Comprueba que cada cita entre comillas angulares de un documento aparezca,
palabra por palabra, en las transcripciones. Uso:
    python verificar_citas.py <documento.md> <carpeta de transcripciones>"""
import io, re, sys, glob, difflib, unicodedata, os

def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]+", " ", t).split()

def limpiar(md):
    md = re.sub(r"\*\*\[\d\d:\d\d:\d\d\][^*]*\*\*", " ", md)
    md = re.sub(r"`\[\?\]`\s*\*\([^)]*\)\*", " ", md)
    return md

def main(doc, carpeta):
    todo = []
    for f in sorted(glob.glob(os.path.join(carpeta, "Transcripcion*.md"))):
        todo += norm(limpiar(io.open(f, encoding="utf-8").read()))
    texto = io.open(doc, encoding="utf-8").read()
    citas = list(dict.fromkeys(re.findall(r"«([^»]{18,})»", texto)))
    malas = 0
    for c in citas:
        peor = 1.0
        for p in [p for p in re.split(r"\[…\]|…", c) if len(norm(p)) >= 4]:
            q, mejor = norm(p), 0.0
            for i in range(0, len(todo) - len(q) + 1):
                r = difflib.SequenceMatcher(None, q, todo[i:i+len(q)]).ratio()
                if r > mejor: mejor = r
                if mejor > 0.995: break
            peor = min(peor, mejor)
        if peor <= 0.97:
            malas += 1
            print("  NO TEXTUAL %.2f  «%s»" % (peor, c[:100]))
    print("%d citas comprobadas, %d textuales, %d NO textuales" % (len(citas), len(citas)-malas, malas))
    return 1 if malas else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
