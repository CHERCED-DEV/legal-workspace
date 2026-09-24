"""Ultimo eslabon de la validacion: lo que la pagina de una grabacion ESCRIBIO al guardar
(volcado de la carpeta simulada, guion 2) lo tiene que recoger recoger_lo_declarado.py,
que es lo que usa la etapa 2. Monta un proyecto minimo en una carpeta de trabajo, con las
paginas de la entrega (sin audio ni Word) y lo escrito, y corre el recogedor.

Por MAX_PATH la carpeta de la entrega y los archivos llevan nombres cortos en la copia:
el recogedor los casa por la CLAVE que llevan dentro, no por el nombre. Use una
--trabajo de ruta corta.

Uso:
  python probar_recoger.py --proyecto <proyecto> --entrega "<ENTREGA - ...>" \
      --arbol <carpeta con arbol.json> --trabajo <carpeta corta, se vacia>
"""
import argparse
import io
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RECOGER = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "plugins", "despacho", "scripts", "recoger_lo_declarado.py"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--proyecto", required=True)
    ap.add_argument("--entrega", required=True, help="nombre de la carpeta de la entrega")
    ap.add_argument("--arbol", required=True, help="carpeta con arbol.json (volcado del guion 2)")
    ap.add_argument("--trabajo", required=True, help="carpeta de trabajo de ruta corta; se vacia")
    a = ap.parse_args()
    if os.path.exists(a.trabajo):
        shutil.rmtree(a.trabajo)
    prueba = os.path.join(a.trabajo, "P")
    corta = "ENTREGA - X"
    destino = os.path.join(prueba, "2-Borradores", "Entregas", corta)
    shutil.copytree(os.path.join(a.proyecto, "2-Borradores", "Entregas", a.entrega), destino,
                    ignore=shutil.ignore_patterns("*.mp4", "*.m4a", "*.docx"))
    arbol = json.load(io.open(os.path.join(a.arbol, "arbol.json"), encoding="utf-8"))
    lo = arbol["2-Borradores"]["Lo que declaré"][a.entrega]
    carpeta = os.path.join(prueba, "2-Borradores", "Lo que declaré", corta)
    os.makedirs(carpeta)
    for i, (n, texto) in enumerate(sorted(lo.items())):
        nombre = "A - en curso.json" if n.endswith(" - en curso.json") else "A - copia %d.json" % i
        io.open(os.path.join(carpeta, nombre), "w", encoding="utf-8", newline="").write(texto)
        print("puesto", nombre, "<-", n)
    salida = os.path.join(a.trabajo, "rec")
    os.makedirs(salida)
    r = subprocess.run([sys.executable, RECOGER, destino, "--salida", salida], capture_output=True, text=True,
                       encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    print(r.stdout[-2000:], r.stderr[-1000:])
    for f in os.listdir(salida):
        if f.endswith(".md"):
            t = io.open(os.path.join(salida, f), encoding="utf-8").read()
            i = t.find("### El texto")
            print("RECOGIDO:", " ".join(t[i:i + 120].split()) if i >= 0 else "(sin apartado de texto)")
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
