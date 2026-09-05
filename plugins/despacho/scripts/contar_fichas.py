# -*- coding: utf-8 -*-
"""Cuenta las fichas de una salida de `hechos-con-prueba`, por estado.

**No es parte del producto.** Es la guarda de un conteo que el propio metodo
pide -- Fase 6, punto 3: *«cuenta y entrega el conteo: cuantos hechos
propuestos, cuantos apoyados, cuantos sin apoyo, cuantos contradichos, cuantos
vacios, cuantos descartes. El conteo es un instrumento de honestidad»*.

Y el metodo pide ese conteo **sin dar con que hacerlo**. En la primera pasada
real contra el caso-03 salio «10 apoyados · 7 sin apoyo» donde eran **9 y 6**:
la tercera cuenta mal hecha del mismo dia en este repositorio. Un instrumento de
honestidad que se calcula a ojo mide sobre todo el cansancio de quien cuenta.

Esto no juzga la salida. Cuenta lo que dice, y la persona compara.

    python3 evals/scripts/contar_fichas.py <salida.md>

Codigos:  0 el conteo escrito coincide · 2 no coincide o falta · 1 error de uso
"""
import io
import os
import re
import sys

ESTADOS = [u"Apoyado y contradicho", u"Apoyado", u"Contradicho",
           u"Sin apoyo", u"No verificable con este material"]


def contar(texto):
    fichas = re.findall(r"(?m)^##\s+(H-\d+)\b", texto)
    por_estado = dict((e, 0) for e in ESTADOS)
    sin_estado = []
    for ficha, cuerpo in bloques(texto):
        m = re.search(r"(?m)^-\s+\*\*Estado:\*\*\s*(.+)$", cuerpo)
        if not m:
            sin_estado.append(ficha)
            continue
        dicho = m.group(1).strip()
        # El mas largo primero: «Apoyado y contradicho» contiene «Apoyado».
        for e in ESTADOS:
            if dicho.startswith(e):
                por_estado[e] += 1
                break
        else:
            sin_estado.append("%s (estado no reconocido: %s)" % (ficha, dicho))
    return fichas, por_estado, sin_estado


def bloques(texto):
    partes = re.split(r"(?m)^##\s+(H-\d+)", texto)
    return list(zip(partes[1::2], partes[2::2]))


def conteo_escrito(texto):
    """Los numeros que la propia salida declara, para poder contrastarlos."""
    m = re.search(u"\\*\\*(\\d+) hechos propuestos\\*\\*", texto)
    fuera = {"total": int(m.group(1)) if m else None}
    for clave, patron in ((u"Apoyado", u"\\*\\*(\\d+) apoyados\\*\\*"),
                          (u"Sin apoyo", u"\\*\\*(\\d+) sin apoyo\\*\\*"),
                          (u"Contradicho", u"\\*\\*(\\d+) contradichos\\*\\*"),
                          (u"Apoyado y contradicho",
                           u"\\*\\*(\\d+) apoyados y contradichos\\*\\*")):
        m = re.search(patron, texto)
        fuera[clave] = int(m.group(1)) if m else None
    return fuera


def main(args):
    if len(args) != 1:
        sys.stderr.write(__doc__)
        return 1
    if not os.path.exists(args[0]):
        print("no existe: %s" % args[0])
        return 1
    texto = io.open(args[0], encoding="utf-8").read()
    fichas, por_estado, sin_estado = contar(texto)
    escrito = conteo_escrito(texto)

    print("\n== %s" % args[0])
    print("   fichas encontradas: %d  (%s)" % (len(fichas), ", ".join(fichas)))
    suma = 0
    for e in ESTADOS:
        if por_estado[e]:
            print("   %-34s %d" % (e, por_estado[e]))
        suma += por_estado[e]
    if sin_estado:
        print("   SIN ESTADO LEGIBLE: %s" % ", ".join(sin_estado))

    problemas = []
    if suma != len(fichas):
        problemas.append("los estados suman %d y hay %d fichas" % (suma, len(fichas)))
    if escrito["total"] is None:
        problemas.append(u"la salida no declara su conteo, y el metodo lo pide")
    elif escrito["total"] != len(fichas):
        problemas.append(u"declara %d hechos y hay %d fichas"
                         % (escrito["total"], len(fichas)))
    for e in ESTADOS[:4]:
        if escrito.get(e) is not None and escrito[e] != por_estado[e]:
            problemas.append(u"declara %d «%s» y hay %d" % (escrito[e], e, por_estado[e]))

    print("")
    if problemas:
        for x in problemas:
            print("   NO COINCIDE: %s" % x)
        return 2
    print("   el conteo escrito coincide con las fichas")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
