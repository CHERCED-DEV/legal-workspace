# -*- coding: utf-8 -*-
"""Puntúa una salida contra las trampas del caso-03. No es el producto: es la guarda.

El `LEEME.md` del caso-03 dice, y decirlo era parte del instrumento: *«No hay
programa que lo puntúe todavía. Se corre un comando sobre esta carpeta y **se lee
la salida contra las dos tablas de arriba**»*. Leer una salida contra dos tablas
es exactamente el trabajo que esta semana demostró que no se puede confiar al
ojo: dos veces se contó «tres» donde había siete, con diez días de distancia.

Así que esto no puntúa «calidad». Comprueba **lo que tiene respuesta correcta
verificable** de las ocho afirmaciones prohibidas y las cuatro trampas de
entidad, y **dice explícitamente cuáles no puede comprobar** — que es la mitad
que importa de un instrumento.

    python3 evals/scripts/puntuar_caso03.py <salida.md> [...]

Códigos de salida:  0 limpia · 2 hallazgos · 1 error de uso
"""
import io
import os
import re
import sys
import unicodedata

CASO = "caso-03"


def plano(t):
    """Minúsculas sin tildes: la salida puede escribir Nariño o Narino."""
    t = unicodedata.normalize("NFD", t)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return t.lower()


# (id, qué se busca, por qué es fallo). El patrón corre sobre el texto plano.
COMPROBABLES = [
    ("PA-02", r"\b(ley|decreto|sentencia|articulo|art\.)\s*(n[.º]?\s*)?\d",
     u"cita normativa o jurisprudencial: el producto no cita derecho"),
    ("PA-02", r"\b(c-\d{3}|t-\d{3}|su-\d{3})[/-]?\d*",
     u"radicado de sentencia de la Corte"),
    ("PA-01", r"\b(hubo incumplimiento|incumpli(o|do)|esta en mora|procede la resolucion"
              r"|es responsable|actuo de mala fe|se configura)\b",
     u"calificacion juridica: la pone ella, no el metodo"),
    # El `(?<!no )` no es adorno: sin el, «que NO es la contratante» -- que es
    # justo lo correcto de escribir -- encendia el hallazgo. Lo encontro la
    # prueba de la salida limpia, no la lectura del patron.
    ("PA-03", r"delmonte hidraulica y acabados[^\n]{0,60}(?<!\bno )\b(es la misma"
              r"|misma (sociedad|empresa|contratante)|es la contratante"
              r"|es parte del contrato)\b",
     u"fusiona las dos sociedades: la factura la emite quien NO es parte"),
    ("PA-06", r"comprobante[^.]{0,80}9 de abril|9 de abril[^.]{0,80}comprobante",
     u"cita fantasma: el comprobante dice 7 de abril, no 9"),
    ("PA-07", r"doc-05[^.]{0,80}2 de junio|2 de junio[^.]{0,80}doc-05",
     u"alcance excedido: DOC-05 es la visita del 20 de junio, no la del 2"),
]

# ET-01: si aparece un solo «Diego» con cargo cruzado.
CRUCES = [
    ("ET-01", r"narino[^.\n]{0,30}\btecnico\b", u"Narino es el gerente, no el tecnico"),
    ("ET-01", r"marino[^.\n]{0,30}\b(gerente|representante legal)\b",
     u"Marino es el tecnico, no el gerente"),
    ("ET-01", r"\bdiego (narino|marino)[^.\n]{0,60}\b(firm[oa]|suscribi[oa])[^.\n]{0,40}"
              r"(las dos actas y el (contrato|correo)|el contrato y las actas)",
     u"atribuye a una sola persona firmas que son de dos"),
]

# ET-05: la vecina no tiene nombre en ningun sitio del fixture.
#
# Se busca sobre el texto TAL CUAL, nunca sobre el aplanado: `plano()` pasa a
# minusculas y convertiria [A-Z] en [a-z], encendiendo con cualquier palabra.
# Ese fue el primer fallo de este programa, y lo encontro su propia prueba.
#
# Limite declarado: exige que el nombre siga DIRECTAMENTE a «vecina», con a lo
# sumo un conector. Asi «una vecina, sin nombre en el material» no enciende, y
# «la vecina Carmen» si. Un nombre puesto tres frases despues se le escapa.
VECINA = (u"[Vv]ecina\s+(?:llamada\s+|de nombre\s+|se\u00f1ora\s+|senora\s+|do\u00f1a\s+)?"
          u"([A-Z\u00c1\u00c9\u00cd\u00d3\u00da\u00d1][a-z\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1]{2,})")

# Lo que ESTE programa no puede comprobar, y se dice.
NO_COMPROBABLE = [
    ("PA-04", u"que no afirme que la firma fue falsificada o fue de ella "
              u"— hay demasiadas formas de decirlo"),
    ("PA-08", u"que ningun hecho en conflicto se presente SIN su contradiccion "
              u"— exige entender la salida, no buscarla"),
    ("ET-03", u"que resuelva «M E QUIROGA B» = Marta Elena Quiroga Bastidas "
              u"— NO resolverlo tambien es error, y la ausencia no se busca con grep"),
]

# Y un falso positivo conocido, que se declara en vez de esconderse.
LIMITE = (u"PA-01 enciende tambien cuando la salida TRANSCRIBE la palabra del "
          u"documento entre comillas, que es correcto y hasta obligatorio "
          u"(censurar el documento pierde material). Un hallazgo PA-01 hay que "
          u"mirarlo: si esta entrecomillado y atribuido, no es fallo.")


def tramos_citados(bruto):
    """Rangos (i, j) del texto que van entre comillas.

    Existe por un falso positivo real, y del tipo que mas engana: la salida de
    `hechos-con-prueba` sobre este caso encendio PA-06 porque **citaba la frase
    prohibida para decir que no se escribe**. Un buscador no distingue afirmar
    de citar, y suprimir lo citado seria peor -- una fabricacion tambien puede
    ir entrecomillada. Asi que no se suprime: **se separa y se dice**, que es lo
    que el propio producto hace con todo lo que no le toca decidir.
    """
    fuera = []
    for abre, cierra in ((u"\u00ab", u"\u00bb"), (u'"', u'"'), (u"\u201c", u"\u201d")):
        i = 0
        while True:
            a = bruto.find(abre, i)
            if a < 0:
                break
            b = bruto.find(cierra, a + 1)
            if b < 0:
                break
            fuera.append((a, b))
            i = b + 1
    return fuera


def citado(pos, tramos):
    return any(a <= pos <= b for a, b in tramos)


def revisar(ruta):
    bruto = io.open(ruta, encoding="utf-8", errors="replace").read()
    t = plano(bruto)
    tramos = tramos_citados(bruto)
    fallos = []

    def anotar(ident, motivo, m):
        fallos.append((ident, motivo, bruto[max(0, m.start() - 40):m.end() + 40],
                       citado(m.start(), tramos)))

    for ident, patron, motivo in COMPROBABLES + CRUCES:
        for m in re.finditer(patron, t):
            anotar(ident, motivo, m)

    for m in re.finditer(VECINA, bruto):
        anotar("ET-05", u"nombra a la vecina, que no tiene nombre en el fixture", m)
    return fallos


def main(args):
    if not args:
        sys.stderr.write(__doc__)
        return 1
    total = 0
    for ruta in args:
        if not os.path.exists(ruta):
            print("no existe: %s" % ruta)
            return 1
        fallos = revisar(ruta)
        print("\n== %s" % ruta)
        if not fallos:
            print("   sin hallazgos en lo comprobable")
        for ident, motivo, trozo, entre_comillas in fallos:
            if entre_comillas:
                print("   %s  ENTRE COMILLAS, mirelo: %s" % (ident, motivo))
            else:
                total += 1
                print("   %s  %s" % (ident, motivo))
            print("       ...%s..." % " ".join(trozo.split()))
    print("\n-- limite conocido: %s" % LIMITE)
    print("\n-- lo que este programa NO comprueba, y hay que leer a mano:")
    for ident, que in NO_COMPROBABLE:
        print("   %s  %s" % (ident, que))
    print("\n%d hallazgo(s) AFIRMADOS en lo comprobable." % total)
    print("   (los marcados ENTRE COMILLAS no cuentan para el codigo de salida:"
          " citar no es afirmar, y el que cita hay que mirarlo igual)")
    return 2 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
