"""Comprueba las citas « » que verificar_citas.py no mira (menos de 18 caracteres) y,
de paso, TODAS contra la transcripcion de SU grabacion, cerca de su minuto [[A<n> hh:mm:ss]].
Complemento de verificar_citas.py, no sustituto.

Uso:  python citas_cortas.py <documento.md> <carpeta de la version de transcripciones>

La expresion de linea admite la etiqueta del hablante DENTRO de la negrita
(«**[00:00:00] · Hablante 1**»): sin eso se descartaban justo esas lineas y el
instrumento daba por inventadas citas que si estaban (paso el 2026-09-24).
"""
import glob
import io
import os
import re
import sys
import unicodedata

LINEA = re.compile(r"\*\*\[(\d\d:\d\d:\d\d)\](?: · Hablante [^*]+)?\*\*\s*(.*?)(?:\s+`\[\?\]`.*)?$")


def plano(s):
    s = unicodedata.normalize("NFC", s).lower()
    return " ".join(re.sub(r"[^\w\s]", " ", s).split())


def seg(t):
    h, m, s = (int(x) for x in t.split(":"))
    return h * 3600 + m * 60 + s


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    doc, carpeta = sys.argv[1], sys.argv[2]
    lineas = {}
    for f in glob.glob(os.path.join(carpeta, "Transcripcion - Audio * - *.md")):
        n = int(re.search(r"Audio (\d+)", os.path.basename(f)).group(1))
        lineas[n] = [(seg(m.group(1)), plano(m.group(2))) for m in (LINEA.match(l.strip()) for l in io.open(f, encoding="utf-8")) if m]
    texto = io.open(doc, encoding="utf-8").read()
    cortas = malas = total = 0
    for m in re.finditer(r"«([^»]+)»([^«]{0,40}?)\[\[A(\d+) (\d\d:\d\d:\d\d)(?: hora)?\]\]", texto):
        frag, n, t = m.group(1), int(m.group(3)), seg(m.group(4))
        total += 1
        cortas += len(frag) < 18
        q = " %s " % plano(frag)
        cerca = [p for s, p in lineas.get(n, []) if abs(s - t) <= 90]
        if not any(q in " %s " % " ".join(cerca[k:k + largo]) for largo in (1, 2, 3, 4) for k in range(len(cerca))):
            malas += 1
            print("NO ENCONTRADA cerca de su minuto: A%d %s «%s»" % (n, m.group(4), frag))
    print("citas con minuto: %d (%d de menos de 18 caracteres) · no encontradas: %d" % (total, cortas, malas))
    print("Ojo: una fila con dos minutos se empareja con el primero; revise a mano las que salgan aqui.")
    return 1 if malas else 0


if __name__ == "__main__":
    sys.exit(main())
