# -*- coding: utf-8 -*-
"""Cuantos SKILL.md dicen algo, y cuales. La pregunta que se contesto mal cinco veces.

El 2026-09-05 este repositorio se equivoco cinco veces en la misma operacion, y
las cinco veces la afirmacion tenia la misma forma -- «N de los M metodos»:

  | Cuando     | Que se conto                                  | Dijo | Era |
  |------------|-----------------------------------------------|------|-----|
  | 26-08      | skills que tocan fechas (H-03 del commit)     | 3    | 7   |
  | 05-09      | SKILL.md que justifican la proteccion (§10)   | 3    | 7   |
  | 05-09      | fichas apoyadas de la pasada                  | 10   | 9   |
  | 05-09      | documentadas de la cronologia                 | 5    | 4   |
  | 05-09      | metodos con el bucle anidado (SPEC-13)        | 2    | 4   |

Las cinco se corrigieron con un comando y ninguna releyendo. Este es el comando
para las tres primeras clases: **no adivina, lista**.

    python3 evals/scripts/contar_skills.py "no se puede reconstruir"
    python3 evals/scripts/contar_skills.py --regex "uno por uno|una por una"

Antes de escribir «N de los M» en un documento de este repositorio, correrlo.
"""
import io
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
SKILLS = RAIZ / "plugins" / "despacho" / "skills"


def main(args):
    como_regex = False
    if args and args[0] == "--regex":
        como_regex, args = True, args[1:]
    if len(args) != 1:
        sys.stderr.write(__doc__)
        return 1
    aguja = args[0]
    patron = re.compile(aguja) if como_regex else None

    todas = sorted(SKILLS.glob("*/SKILL.md"))
    con, sin = [], []
    for p in todas:
        t = io.open(p, encoding="utf-8").read()
        veces = len(patron.findall(t)) if patron else t.count(aguja)
        (con if veces else sin).append((p.parent.name, veces))

    print(u"\nBuscando: %s%s" % ("(regex) " if como_regex else "", aguja))
    print(u"\n%d de %d metodos lo traen:" % (len(con), len(todas)))
    for n, v in con:
        print(u"   %-22s %d vez/veces" % (n, v))
    if sin:
        print(u"\n%d NO lo traen:" % len(sin))
        print(u"   %s" % ", ".join(n for n, _ in sin))
    print(u"\n   %d de %d.  Esta es la cifra que se escribe, no la que se recuerda."
          % (len(con), len(todas)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
