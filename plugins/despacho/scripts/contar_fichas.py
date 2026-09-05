# -*- coding: utf-8 -*-
"""Cuenta las fichas de una salida y contrasta el conteo que la salida declara.

Sirve a los tres metodos que cuentan: `hechos-con-prueba` (fichas H-NN por
estado), `cronologia` (eventos E-NN por grado de certeza) y `revision-de-rigor`
(hallazgos F-NN por grado de soporte). Reconoce cual es por su forma.

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

# Los cinco grados de `cronologia` §3. Vocabulario fijo: no hay un sexto.
GRADOS = [u"en conflicto", u"documentada", u"referida", u"aproximada", u"deducida"]

# Los tres grados de soporte de `revision-de-rigor` §5.
SOPORTES = [u"sin soporte", u"soportado", u"limitado"]


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


def contar_cronologia(texto):
    """Los grados de la tabla de `cronologia`, contados por su ultima celda.

    Existe por el cuarto conteo mal hecho del 2026-09-05, que fue el peor: la
    cronologia del caso-03 declaro «5 documentadas» donde habia cuatro, los
    numeros no cuadraron -- 15 donde habia 14 eventos -- y en vez de recontar se
    escribio un parrafo explicando la discrepancia. **El conteo existe para eso,
    y una discrepancia pide recontar, no justificar.**
    """
    # Solo la tabla 2. La tabla 3 -- eventos SIN fecha -- tiene otra ultima
    # columna («de donde sale la ubicacion»), y contarla aqui hacia que sus
    # filas salieran como «grado no reconocido». Cada tabla se cuenta donde va.
    linea, sin = partir_tablas(texto)
    filas = re.findall(r"(?m)^\|\s*(E-\d+)\s*\|.*\|([^|]*)\|\s*$", linea)
    por_grado = dict((g, 0) for g in GRADOS)
    sin_grado = []
    for ev, celda in filas:
        d = plano(celda.strip())
        for g in GRADOS:                      # «en conflicto» primero: ver ESTADOS
            if d.startswith(plano(g)):
                por_grado[g] += 1
                break
        else:
            sin_grado.append("%s (grado no reconocido: %s)" % (ev, celda.strip()))
    sin_fecha = re.findall(r"(?m)^\|\s*(E-\d+)\s*\|", sin)
    return [e for e, _ in filas], por_grado, sin_grado, sin_fecha


def partir_tablas(texto):
    """(la linea de tiempo, los eventos sin fecha), por sus encabezados."""
    def corte(marca, desde=0):
        m = re.search(marca, texto[desde:])
        return desde + m.start() if m else None
    i = corte(r"(?im)^#+.*L[IÍ]NEA DE TIEMPO")
    j = corte(r"(?im)^#+.*EVENTOS SIN FECHA")
    k = corte(r"(?im)^#+.*CONFLICTOS DE FECHA")
    if i is None:
        return texto, ""
    fin_linea = j if j is not None else (k if k is not None else len(texto))
    if j is None:
        return texto[i:fin_linea], ""
    return texto[i:j], texto[j:(k if k is not None else len(texto))]


def plano(t):
    import unicodedata
    t = unicodedata.normalize("NFD", t)
    return "".join(c for c in t if unicodedata.category(c) != "Mn").lower()


def conteo_cronologia_escrito(texto):
    fuera = {}
    m = re.search(u"\\*\\*(\\d+) eventos\\*\\*", texto)
    fuera["total"] = int(m.group(1)) if m else None
    for g, patron in ((u"documentada", u"\\*\\*(\\d+) documentadas\\*\\*"),
                      (u"referida", u"\\*\\*(\\d+) referidas\\*\\*"),
                      (u"aproximada", u"\\*\\*(\\d+) aproximadas\\*\\*"),
                      (u"deducida", u"\\*\\*(\\d+) deducidas\\*\\*"),
                      (u"en conflicto", u"\\*\\*(\\d+) en conflicto\\*\\*")):
        m = re.search(patron, texto)
        fuera[g] = int(m.group(1)) if m else None
    m = re.search(u"\\*\\*(\\d+) sin fecha\\*\\*", texto)
    fuera["sin fecha"] = int(m.group(1)) if m else None
    return fuera


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


def main_cronologia(ruta, texto):
    eventos, por_grado, sin_grado, sin_fecha = contar_cronologia(texto)
    d = conteo_cronologia_escrito(texto)
    print("\n== %s   (cronologia)" % ruta)
    print("   en la linea de tiempo: %d  (%s)" % (len(eventos), ", ".join(eventos)))
    if sin_fecha:
        print("   sin fecha:             %d  (%s)"
              % (len(sin_fecha), ", ".join(sin_fecha)))
    for g in GRADOS:
        if por_grado[g]:
            print("   %-16s %d" % (g, por_grado[g]))
    if sin_grado:
        print("   SIN GRADO LEGIBLE: %s" % ", ".join(sin_grado))

    problemas = []
    for g in GRADOS:
        if d.get(g) is not None and d[g] != por_grado[g]:
            problemas.append(u"declara %d «%s» y hay %d" % (d[g], g, por_grado[g]))
    con_fecha = sum(por_grado.values())
    if d.get("sin fecha") is not None and d["sin fecha"] != len(sin_fecha):
        problemas.append(u"declara %d sin fecha y la tabla 3 tiene %d"
                         % (d["sin fecha"], len(sin_fecha)))
    if d.get("total") is not None and con_fecha + len(sin_fecha) != d["total"]:
        problemas.append(u"%d con fecha + %d sin fecha = %d, y declara %d eventos"
                         % (con_fecha, len(sin_fecha),
                            con_fecha + len(sin_fecha), d["total"]))
    print("")
    if problemas:
        for x in problemas:
            print("   NO COINCIDE: %s" % x)
        print("\n   Una discrepancia pide RECONTAR, no explicarla.")
        return 2
    print("   el conteo escrito coincide con la tabla")
    return 0


def contar_rigor(texto):
    """Los grados de soporte de las fichas F-NN de `revision-de-rigor`."""
    fichas = re.findall(r"(?m)^#+\s+(F-\d+)\b", texto)
    por = dict((s, 0) for s in SOPORTES)
    sin = []
    partes = re.split(r"(?m)^#+\s+(F-\d+)\b", texto)
    for ficha, cuerpo in zip(partes[1::2], partes[2::2]):
        m = re.search(r"(?im)^-\s+\*\*Grado de soporte:\*\*\s*(.+)$", cuerpo)
        if not m:
            sin.append(ficha)
            continue
        d = plano(re.sub(r"[*_`.]", "", m.group(1)).strip())
        for s in SOPORTES:                    # «sin soporte» antes que «soportado»
            if d.startswith(plano(s)):
                por[s] += 1
                break
        else:
            sin.append("%s (grado no reconocido: %s)" % (ficha, m.group(1).strip()))
    return fichas, por, sin


def conteo_rigor_escrito(texto):
    fuera = {}
    m = re.search(u"\\*\\*(\\d+) hallazgos?\\*\\*", texto)
    fuera["total"] = int(m.group(1)) if m else None
    for s, patron in ((u"soportado", u"\\*\\*(\\d+) soportados?\\*\\*"),
                      (u"limitado", u"\\*\\*(\\d+) limitados?\\*\\*"),
                      (u"sin soporte", u"\\*\\*(\\d+) sin soporte\\*\\*")):
        m = re.search(patron, texto)
        fuera[s] = int(m.group(1)) if m else None
    return fuera


def main_rigor(ruta, texto):
    fichas, por, sin = contar_rigor(texto)
    d = conteo_rigor_escrito(texto)
    print("\n== %s   (revision de rigor)" % ruta)
    print("   hallazgos: %d  (%s)" % (len(fichas), ", ".join(fichas)))
    for s in SOPORTES:
        if por[s]:
            print("   %-14s %d" % (s, por[s]))
    if sin:
        print("   SIN GRADO LEGIBLE: %s" % ", ".join(sin))

    problemas = []
    if sum(por.values()) != len(fichas):
        problemas.append(u"los grados suman %d y hay %d fichas"
                         % (sum(por.values()), len(fichas)))
    if d.get("total") is not None and d["total"] != len(fichas):
        problemas.append(u"declara %d hallazgos y hay %d" % (d["total"], len(fichas)))
    for s in SOPORTES:
        if d.get(s) is not None and d[s] != por[s]:
            problemas.append(u"declara %d «%s» y hay %d" % (d[s], s, por[s]))
    print("")
    if problemas:
        for x in problemas:
            print("   NO COINCIDE: %s" % x)
        print("\n   Una discrepancia pide RECONTAR, no explicarla.")
        return 2
    print("   el conteo escrito coincide con las fichas")
    return 0


def main(args):
    if len(args) != 1:
        sys.stderr.write(__doc__)
        return 1
    if not os.path.exists(args[0]):
        print("no existe: %s" % args[0])
        return 1
    texto = io.open(args[0], encoding="utf-8").read()
    if re.search(r"(?m)^#+\s+F-\d+\b", texto):
        return main_rigor(args[0], texto)
    if re.search(r"(?m)^\|\s*E-\d+\s*\|", texto) and not re.search(r"(?m)^##\s+H-", texto):
        return main_cronologia(args[0], texto)
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
