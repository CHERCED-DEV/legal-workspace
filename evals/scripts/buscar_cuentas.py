# -*- coding: utf-8 -*-
"""Busca en una salida los numeros que solo pueden haber salido de una cuenta.

La regla esta en los siete metodos que pueden escribir una fecha, con una sola
redaccion desde el 2026-09-05: *«nunca sumas ni restas dias sobre una fecha para
producir otra, aunque el resultado no sea un plazo»*.

**Se unifico esa manana y se rompio esa misma tarde.** La primera salida
producida bajo la regla -- la pasada de `hechos-con-prueba` sobre el caso-03 --
escribio «con veintiun dias de diferencia» entre dos actas. Veintiuno no esta en
ninguna pieza: salio de restar 30 de mayo de 20 de junio.

Ese es el argumento entero de este archivo. La regla estaba escrita, recien
unificada, y quien la escribio la rompio a las pocas horas. **El cuidado no
basta y hace falta la guarda.**

Que hace: busca duraciones y distancias temporales en el texto y las devuelve
para que una persona compruebe si estan en el material o salieron de una resta.
NO decide: una duracion puede estar escrita en el contrato -- «seis meses de
garantia» lo esta -- y entonces citarla es correcto y obligatorio.

    python3 evals/scripts/buscar_cuentas.py <salida.md> [--material <carpeta>]

Con --material comprueba ademas si la expresion aparece en alguna pieza, que es
la mitad que convierte el aviso en un hallazgo.

Codigos:  0 nada que mirar · 2 hay expresiones que mirar · 1 error de uso
"""
import io
import os
import re
import sys
import unicodedata

NUM = (u"(?:\\d+|un|una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|"
       u"trece|catorce|quince|dieciseis|diecisiete|dieciocho|diecinueve|veinte|"
       u"veintiun|veintiuno|veintidos|treinta|cuarenta|cincuenta|sesenta)")
UNIDAD = u"(?:dias?|semanas?|meses|mes|anos?|horas?)"

PATRONES = [
    (u"duracion", u"\\b%s\\s+%s\\b" % (NUM, UNIDAD)),
    (u"distancia", u"\\b(?:%s)\\s+(?:de\\s+)?(?:diferencia|despues|antes|mas tarde)\\b"
                   % (u"%s\\s+%s" % (NUM, UNIDAD))),
    # Exige numero Y unidad: la primera version encendia con el verbo «llevar»
    # en cualquier sentido -- «lleva rubrica», «lleva un solo estado» -- y un
    # aviso que enciende siempre no se mira nunca.
    (u"transcurso", u"\\b(?:han? transcurrido|han pasado|llevan?|desde hace|hace ya)"
                    u"\\s+(?:mas de\\s+)?%s\\s+%s\\b" % (NUM, UNIDAD)),
    (u"vencimiento", u"\\b(?:vencio|vence|venc[ei]|quedan?\\s+%s\\s+%s)\\b" % (NUM, UNIDAD)),
]


def plano(t):
    t = unicodedata.normalize("NFD", t)
    return "".join(c for c in t if unicodedata.category(c) != "Mn").lower()


def citado(pos, bruto):
    for abre, cierra in ((u"«", u"»"), (u'"', u'"'), (u"“", u"”")):
        i = 0
        while True:
            a = bruto.find(abre, i)
            if a < 0:
                break
            b = bruto.find(cierra, a + 1)
            if b < 0:
                break
            if a <= pos <= b:
                return True
            i = b + 1
    return False


def material(carpeta):
    """El texto plano de todas las piezas, para saber si la expresion ya estaba."""
    trozos = []
    for raiz, _, ficheros in os.walk(carpeta):
        for f in ficheros:
            if f.lower().endswith((".txt", ".md")):
                try:
                    trozos.append(io.open(os.path.join(raiz, f),
                                          encoding="utf-8", errors="replace").read())
                except IOError:
                    pass
    return plano("\n".join(trozos))


# Un importe se escribe con separadores de miles: $4.800.000, 2.300.000.
# Se comparan por sus digitos, que es como aparecen en el material aunque el
# documento los escriba ademas en letras.
IMPORTE = u"\\$?\\s?(\\d{1,3}(?:[.,]\\d{3})+)"


def importes(ruta, texto_material):
    """Cifras de dinero de la salida que NO estan en ninguna pieza.

    Existe por el segundo defecto de la misma clase en el mismo archivo: la
    pasada de `hechos-con-prueba` escribio «la diferencia es de $500.000 en las
    dos cifras». $500.000 no aparece en el material -- salio de restar 4.800.000
    menos 4.300.000. La guarda de esa manana solo miraba fechas.

    Es la misma regla y no una nueva: **ningun dato se produce operando.**
    """
    bruto = io.open(ruta, encoding="utf-8", errors="replace").read()
    fuera = []
    vistos = set()
    for m in re.finditer(IMPORTE, bruto):
        cifra = m.group(1)
        if cifra in vistos:
            continue
        vistos.add(cifra)
        if cifra not in texto_material:
            fuera.append((cifra, citado(m.start(), bruto),
                          " ".join(bruto[max(0, m.start() - 60):m.end() + 60].split())))
    return fuera


def revisar(ruta, texto_material=None):
    bruto = io.open(ruta, encoding="utf-8", errors="replace").read()
    t = plano(bruto)
    vistos = set()
    fuera = []
    for clase, patron in PATRONES:
        for m in re.finditer(patron, t):
            clave = (m.start(), m.group(0))
            if clave in vistos:
                continue
            vistos.add(clave)
            en_material = None
            if texto_material is not None:
                en_material = m.group(0) in texto_material
            fuera.append((clase, m.group(0), citado(m.start(), bruto), en_material,
                          " ".join(bruto[max(0, m.start() - 60):m.end() + 60].split())))
    return fuera


def main(args):
    ruta = None
    carpeta = None
    i = 0
    while i < len(args):
        if args[i] == "--material" and i + 1 < len(args):
            carpeta = args[i + 1]
            i += 2
        else:
            ruta = args[i]
            i += 1
    if not ruta or not os.path.exists(ruta):
        sys.stderr.write(__doc__)
        return 1
    texto_material = material(carpeta) if carpeta else None

    hallazgos = revisar(ruta, texto_material)
    print("\n== %s" % ruta)
    if not hallazgos:
        print("   ninguna expresion de duracion o distancia temporal")
        return 0
    mirar = 0
    for clase, expr, es_cita, en_material, trozo in hallazgos:
        if en_material is True:
            marca = "ESTA EN EL MATERIAL"
        elif en_material is False:
            marca = "NO ESTA EN EL MATERIAL -- mirelo"
        else:
            marca = "sin material que comparar"
        # Citar no es afirmar, igual que en `puntuar_caso03.py`: una nota que
        # dice «aqui decia N dias y esa cifra salio de una resta» tiene que
        # poder escribirse sin dejar la guarda en rojo para siempre.
        if es_cita:
            marca += " (entre comillas)"
        elif en_material is not True:
            mirar += 1
        print("   %-11s «%s»  %s" % (clase, expr, marca))
        print("       ...%s..." % trozo)
    if texto_material is not None:
        raros = importes(ruta, texto_material)
        if raros:
            print("\n   IMPORTES que no aparecen en ninguna pieza:")
            for cifra, es_cita, trozo in raros:
                marca = " (entre comillas)" if es_cita else ""
                if not es_cita:
                    mirar += 1
                print("   importe     «%s»  NO ESTA EN EL MATERIAL -- mirelo%s"
                      % (cifra, marca))
                print("       ...%s..." % trozo)

    print("\n   Este programa NO decide. Una duracion o un importe escritos en"
          "\n   el material se citan y es correcto; los que salen de una cuenta,"
          "\n   no se escriben. Es la misma regla: ningun dato se produce operando.")
    print("\n%d expresion(es) que mirar." % mirar)
    return 2 if mirar else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
