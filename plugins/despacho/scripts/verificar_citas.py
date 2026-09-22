# -*- coding: utf-8 -*-
"""Comprueba que cada cita entre comillas angulares de un documento aparezca,
palabra por palabra, en las transcripciones. Uso:

    python verificar_citas.py <documento.md> <carpeta> [<carpeta 2> ...]

Con UNA carpeta: una cita es textual si aparece en ella.

Con VARIAS: una cita es textual si aparece en AL MENOS UNA, y se dice en cual.
Eso hace falta para los documentos que comparan iteraciones, donde cada cita
viene a proposito de una version distinta: pasarlo contra una sola carpeta
marca como falsas las citas de las otras dos, y obliga a cruzar tres salidas
a mano — una comprobacion que solo puede repetir quien la hizo no comprueba
nada.

Existe porque en el primer resumen del expediente escribi tres citas que no
eran textuales sin darme cuenta: cambie una palabra, invente una frase y
sustitui un cargo. Las tres se leian perfectamente bien."""
import io, re, sys, glob, difflib, unicodedata, os

def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]+", " ", t).split()

def limpiar(md):
    md = re.sub(r"\*\*\[\d\d:\d\d:\d\d\][^*]*\*\*", " ", md)
    md = re.sub(r"`\[\?\]`\s*\*\([^)]*\)\*", " ", md)
    return md

def cargar(carpeta):
    todo = []
    for f in sorted(glob.glob(os.path.join(carpeta, "Transcripcion*.md"))):
        todo += norm(limpiar(io.open(f, encoding="utf-8").read()))
    return todo

def puntuar(cita, todo):
    # Las partes de menos de dos palabras no se pueden cotejar con sentido,
    # pero TAMPOCO pueden darse por buenas: hasta 2026-09-19 el minimo era de
    # cuatro palabras y una cita mas corta salia del bucle sin comprobar, con
    # peor = 1.0. Asi pasaron por textuales tres citas de dos y tres palabras
    # -- una de ellas la frase juridicamente mas cargada de aquel material --
    # sin que nadie las mirase. En un programa
    # cuyo unico trabajo es cazar citas inventadas, un aprobado en blanco es
    # peor que no tenerlo.
    partes = [p for p in re.split(r"\[…\]|…", cita) if len(norm(p)) >= 2]
    if not partes:
        partes = [cita]
    peor = 1.0
    for p in partes:
        q, mejor = norm(p), 0.0
        for i in range(0, len(todo) - len(q) + 1):
            r = difflib.SequenceMatcher(None, q, todo[i:i+len(q)]).ratio()
            if r > mejor: mejor = r
            if mejor > 0.995: break
        peor = min(peor, mejor)
    return peor

def main(doc, carpetas):
    fuentes = []
    for c in carpetas:
        palabras = cargar(c)
        if not palabras:
            sys.stderr.write("Sin transcripciones en: %s\n" % c)
            return 2
        fuentes.append((os.path.basename(c.rstrip("\\/")) or c, palabras))

    texto = io.open(doc, encoding="utf-8").read()
    citas = list(dict.fromkeys(re.findall(r"«([^»]{18,})»", texto)))
    varias = len(fuentes) > 1
    malas = 0
    for cita in citas:
        marcas = [(puntuar(cita, p), n) for n, p in fuentes]
        peor, donde = max(marcas)
        if peor <= 0.97:
            malas += 1
            print("  NO TEXTUAL %.2f  «%s»" % (peor, cita[:100]))
            if varias:
                print("       lo mas parecido esta en %s" % donde)
        elif varias:
            coinciden = [n for m, n in marcas if m > 0.97]
            print("  textual   en %s  «%s»" % (", ".join(coinciden), cita[:80]))

    print("%d citas comprobadas, %d textuales, %d NO textuales" %
          (len(citas), len(citas) - malas, malas))
    if varias and not malas:
        print("Cada cita aparece al menos en una de las %d carpetas." % len(fuentes))
    return 1 if malas else 0

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write(__doc__ + "\n")
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2:]))
