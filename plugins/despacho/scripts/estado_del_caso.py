# -*- coding: utf-8 -*-
"""Reescribe SOLO la cabecera de "0-Estado del caso (no editar).txt".

Lo que ella escribio debajo de la linea NOTAS SUYAS se conserva BYTE A BYTE:
no vuelve a pasar por el modelo, no se vuelve a teclear, no se normaliza.

    python estado_del_caso.py "<carpeta del caso>" --cabecera "<archivo.txt>"
    python estado_del_caso.py "<carpeta del caso>" --comprobar
    python estado_del_caso.py "<carpeta del caso>" --cabecera "<archivo.txt>" --crear

Por que existe este programa, y no una instruccion mas en el metodo:

  * En este sistema NO HAY COPIA. Cada vez que un texto aparece en una
    salida, el modelo lo re-emite palabra por palabra. El archivo de estado
    es el unico punto del producto donde un texto DE ELLA sale por esa via,
    y una normalizacion silenciosa -una tilde, un guion, un renglon
    partido- no se nota. Aqui la cola se copia como bytes y se comprueba
    despues: si cambio un solo byte, se restaura la copia y no se escribe.

Lo que este programa NO hace:

  * NO lee el contenido de las notas de ella hacia la salida. Solo dice
    cuantos renglones y cuantos bytes conservo.
  * NO escribe nada si no encuentra la linea NOTAS SUYAS. Sin esa linea no
    hay forma de saber donde empieza lo suyo, y adivinarlo es justo lo que
    no se puede hacer.
  * NO decide que dice la cabecera. Esa la escribe el metodo.
"""
import argparse
import shutil
import sys
import unicodedata
from datetime import date
from pathlib import Path

MARCA = "NOTAS SUYAS"
NOMBRE_ESTADO = "0-Estado del caso"
# La marca es EL FINAL de la parte del sistema: de ahi hacia abajo es de ella
# y no se toca. Por eso el historico de revisiones va ARRIBA, en la cabecera:
# si viviera debajo de la marca no podria crecer nunca.
BLOQUE_NUEVO = (
    "NOTAS SUYAS (el sistema no toca esta parte)\n"
    "\n"
)


def plano(s):
    """Mayusculas y sin tildes, para que 'Notas Suyas' encuentre 'NOTAS SUYAS'."""
    d = unicodedata.normalize('NFD', s)
    return ''.join(c for c in d if unicodedata.category(c) != 'Mn').upper()


def es_marca(linea_bytes):
    try:
        t = linea_bytes.decode('utf-8')
    except UnicodeDecodeError:
        t = linea_bytes.decode('cp1252', 'replace')
    return plano(t).lstrip().startswith(MARCA)


def partir(datos):
    """Devuelve (cabecera, cola) en bytes. cola empieza en la linea de la marca."""
    inicio = 0
    for linea in datos.splitlines(keepends=True):
        if es_marca(linea):
            return datos[:inicio], datos[inicio:]
        inicio += len(linea)
    return None, None


def localizar(carpeta):
    for p in sorted(carpeta.iterdir()):
        if p.is_file() and p.name.startswith(NOMBRE_ESTADO):
            return p
    return carpeta / (NOMBRE_ESTADO + " (no editar).txt")


def destino_copia(carpeta):
    borradores = carpeta / "2-Borradores"
    if not borradores.is_dir():
        borradores = carpeta
    hoy = date.today().isoformat()
    base = "%s — anterior (%s)" % (NOMBRE_ESTADO, hoy)
    ruta = borradores / (base + ".txt")
    n = 2
    while ruta.exists():
        ruta = borradores / ("%s (%d).txt" % (base, n))
        n += 1
    return ruta


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("carpeta", help="carpeta del caso")
    ap.add_argument("--cabecera", help="archivo con el texto nuevo de la cabecera")
    ap.add_argument("--archivo", help="ruta explicita del archivo de estado")
    ap.add_argument("--crear", action="store_true",
                    help="si el archivo no existe, crearlo con el bloque de notas vacio")
    ap.add_argument("--comprobar", action="store_true",
                    help="solo informa: no escribe nada")
    a = ap.parse_args()

    carpeta = Path(a.carpeta)
    if not carpeta.is_dir():
        print("ERROR: no existe la carpeta: %s" % carpeta)
        return 1
    estado = Path(a.archivo) if a.archivo else localizar(carpeta)

    # --- El archivo no existe todavia
    if not estado.exists():
        if a.comprobar:
            print("NO EXISTE: %s" % estado.name)
            print("Es la primera revision de esta carpeta. Con --crear se escribe entero.")
            return 0
        if not a.crear:
            print("ERROR: no existe %s" % estado.name)
            print("Es la primera revision: vuelve a llamar con --crear.")
            return 2
        if not a.cabecera:
            print("ERROR: --crear necesita --cabecera")
            return 1
        cab = Path(a.cabecera).read_bytes()
        if not cab.endswith(b"\n"):
            cab += b"\n"
        estado.write_bytes(cab + b"\n" + BLOQUE_NUEVO.encode("utf-8"))
        print("CREADO: %s" % estado.name)
        print("Bloque de notas de ella: creado vacio. El sistema no vuelve a tocarlo.")
        return 0

    datos = estado.read_bytes()
    cabecera_vieja, cola = partir(datos)

    # --- Sin la linea marcadora no se escribe. Punto.
    if cola is None:
        print("SIN MARCA: %s no tiene la linea \"%s\"." % (estado.name, MARCA))
        print("NO SE ESCRIBIO NADA. Sin esa linea no hay forma de saber donde")
        print("empieza lo que ella escribio, y suponerlo puede borrarlo.")
        print("Bytes del archivo actual: %d" % len(datos))
        return 3

    renglones_cola = cola.count(b"\n") + (0 if cola.endswith(b"\n") else 1)
    if a.comprobar:
        print("MARCA ENCONTRADA en %s" % estado.name)
        print("Cabecera (la reescribe el sistema): %d bytes" % len(cabecera_vieja))
        print("De la marca hacia abajo (suyo, intocable): %d bytes, %d renglones"
              % (len(cola), renglones_cola))
        return 0

    if not a.cabecera:
        print("ERROR: falta --cabecera (o usa --comprobar)")
        return 1

    # --- Copia previa. Si no se puede copiar, no se escribe.
    copia = destino_copia(carpeta)
    try:
        copia.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(estado), str(copia))
    except Exception as e:
        print("ERROR al guardar la copia previa: %s" % e)
        print("NO SE ESCRIBIO NADA. Sin copia no se toca el archivo.")
        return 4

    cab = Path(a.cabecera).read_bytes()
    if not cab.endswith(b"\n"):
        cab += b"\n"
    if not cab.endswith(b"\n\n"):
        cab += b"\n"

    try:
        estado.write_bytes(cab + cola)
    except Exception as e:
        shutil.copy2(str(copia), str(estado))
        print("ERROR al escribir: %s. Se restauro el archivo desde la copia." % e)
        return 5

    # --- Comprobacion: la cola tiene que estar identica, byte a byte.
    quedo = estado.read_bytes()
    if not quedo.endswith(cola) or quedo[len(quedo) - len(cola):] != cola:
        shutil.copy2(str(copia), str(estado))
        print("FALLO LA COMPROBACION: la parte suya no quedo identica.")
        print("Se restauro el archivo desde la copia. NO hay cambio.")
        return 6

    print("ESCRITO: %s" % estado.name)
    print("Copia del anterior: %s" % copia)
    print("Cabecera nueva: %d bytes. Suyo, conservado sin tocar: %d bytes, %d renglones."
          % (len(cab), len(cola), renglones_cola))
    print("Comprobado byte a byte: la parte de ella quedo identica.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
