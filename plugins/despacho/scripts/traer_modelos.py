# -*- coding: utf-8 -*-
"""Trae los modelos de reconocimiento que el plugin no versiona.

Los modelos pesan 16 MB, son binarios de terceros y estan en .gitignore. Este
programa los baja, comprueba lo unico que importa de su diccionario -- que
tenga los caracteres del espanol -- y deja la receta escrita.

    python traer_modelos.py                 # el general, que es el que se usa
    python traer_modelos.py --latino        # ademas, el latino (ver abajo)
    python traer_modelos.py --solo-mirar    # no baja nada: solo dice que hay

POR QUE EXISTE. En agosto se anoto que el modelo latino "solo se distribuye en
ModelScope y no fue alcanzable desde esta maquina". El 2026-09-05 se comprobo
que SI esta en Hugging Face, con licencia Apache-2.0, y que su diccionario trae
la N con virgulilla MAYUSCULA, la U con tilde y la apertura de interrogacion --
los tres que el general no tiene y que en un encabezado colombiano en
mayusculas ("SENOR", "ANO", "DANO") salen mal siempre.

LO QUE ESTE PROGRAMA NO DICE. Que el latino reconozca mejor. El general se
midio sobre 23 fotografias reales; el latino no se ha medido sobre ninguna, y
cambiar de reconocedor es VERSION NUEVA y no sobrescritura (ADR-016 §9): antes
de adoptarlo hay que repetir la medida, y en particular los 12 identificadores
criticos que hoy salen 12 de 12.
"""
import argparse
import re
import sys
import urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent / "modelos"
BASE = "https://huggingface.co/%s/resolve/main/%s"

GENERAL = {
    "repo": "bukuroo/PPOCRv5-ONNX",
    "licencia": "ver el repositorio de origen",
    "archivos": [("ppocrv5-mobile-rec.onnx", "ppocrv5-mobile-rec.onnx"),
                 ("ppocrv5_dict.txt", "ppocrv5_dict.txt")],
}
LATINO = {
    "repo": "PaddlePaddle/latin_PP-OCRv5_mobile_rec_onnx",
    "licencia": "apache-2.0",
    "archivos": [("inference.onnx", "ppocrv5-latin-rec.onnx"),
                 ("inference.yml", "_latin.yml")],
}
# Los del espanol que deciden si un encabezado en mayusculas sale bien.
ESPANOL = ["A", "E", "I", "O", "U", "a", "e", "i", "o", "u",
           "Á", "É", "Í", "Ó", "Ú",
           "á", "é", "í", "ó", "ú",
           "Ñ", "ñ", "Ü", "ü", "¿", "¡"]
CRITICOS = ["Ñ", "Ú", "¿", "¡"]   # N mayuscula, U tilde, ¿ ¡


def bajar(repo, remoto, local):
    destino = AQUI / local
    if destino.exists():
        print("  ya esta: %s (%d bytes)" % (local, destino.stat().st_size))
        return destino
    url = BASE % (repo, remoto)
    print("  bajando %s ..." % local)
    try:
        with urllib.request.urlopen(url, timeout=120) as r, open(destino, "wb") as f:
            f.write(r.read())
    except Exception as e:
        print("  FALLO: %s\n    %s" % (local, e))
        return None
    print("  ok: %s (%d bytes)" % (local, destino.stat().st_size))
    return destino


def dict_del_yml(ruta):
    """El export ONNX de Paddle mete el diccionario dentro del .yml."""
    t = ruta.read_text(encoding="utf-8", errors="replace")
    i = t.find("character_dict")
    if i < 0:
        return None
    chars = []
    for l in t[i:].splitlines()[1:]:
        s = l.strip()
        if s.startswith("- "):
            chars.append(s[2:])
        elif chars:
            break
    return chars


def informar(nombre, chars):
    print("\n%s: %d caracteres" % (nombre, len(chars)))
    faltan = [c for c in ESPANOL if c not in chars]
    criticos = [c for c in CRITICOS if c not in chars]
    if not faltan:
        print("  tiene TODOS los del espanol.")
    else:
        print("  NO tiene: %s" % " ".join(faltan))
    if criticos:
        print("  Y de los que rompen un encabezado en mayusculas, faltan: %s"
              % " ".join(criticos))
        print("  Un caracter que no esta en el vocabulario NO SALE NUNCA:")
        print("  no es un problema de imagen y ningun ajuste lo arregla.")
    return not criticos


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--latino", action="store_true", help="baja tambien el modelo latino")
    ap.add_argument("--solo-mirar", action="store_true", help="no baja nada")
    a = ap.parse_args()
    AQUI.mkdir(parents=True, exist_ok=True)

    if a.solo_mirar:
        print("En %s hay:" % AQUI)
        hay = sorted(p.name for p in AQUI.iterdir() if p.name != "PROCEDENCIA.md")
        print("  " + ("\n  ".join(hay) if hay else "(nada)"))
        return 0

    print("MODELO GENERAL (%s)" % GENERAL["repo"])
    ok = all(bajar(GENERAL["repo"], r, l) for r, l in GENERAL["archivos"])
    d = AQUI / "ppocrv5_dict.txt"
    if d.exists():
        informar("diccionario general", d.read_text(encoding="utf-8").splitlines())

    if a.latino:
        print("\nMODELO LATINO (%s, %s)" % (LATINO["repo"], LATINO["licencia"]))
        for r, l in LATINO["archivos"]:
            bajar(LATINO["repo"], r, l)
        yml = AQUI / "_latin.yml"
        if yml.exists():
            chars = dict_del_yml(yml)
            if chars:
                (AQUI / "ppocrv5_latin_dict.txt").write_text("\n".join(chars), encoding="utf-8")
                print("  diccionario extraido a ppocrv5_latin_dict.txt")
                informar("diccionario latino", chars)
        print("\n  Y NO SE ADOPTA POR TENER MEJOR VOCABULARIO.")
        print("  Cambiar de reconocedor es version nueva, no sobrescritura")
        print("  (ADR-016 §9). Antes hay que repetir la medida sobre fotografias")
        print("  reales, y en particular los 12 identificadores criticos que hoy")
        print("  salen 12 de 12. Un modelo mejor de vocabulario puede ser peor")
        print("  de reconocimiento, y eso no se sabe hasta medirlo.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
