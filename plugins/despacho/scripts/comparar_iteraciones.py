# -*- coding: utf-8 -*-
"""
comparar_iteraciones — poner dos o mas pasadas del mismo material una al lado de otra.

    python comparar_iteraciones.py "<carpeta 1>" "<carpeta 2>" ["<carpeta 3>" ...] [--umbral=0.80] [--tope=12]

Cada carpeta es una salida de `transcribir_audio.py` (o equivalente) con su
subcarpeta `datos/`.

NO dice cual es mejor, y no puede: no hay verdad de referencia. Dice en que se
diferencian, con numeros, y **donde todas discrepan a la vez** — que es lo unico
que senala de verdad un problema, conforme a ADR-017 §8.

Por que existe: regenerar produce version nueva y nunca sobrescribe (ADR-011 §8),
asi que acaba habiendo varias carpetas del mismo material. Sin una forma de
compararlas, tener tres es tener tres veces el mismo trabajo sin saber cual mirar.

Lo que este programa NO hace:
  · No elige una ganadora.
  · No junta las versiones en una sola: mezclarlas produciria un texto que
    ninguna decodificacion dijo.
  · No rellena la lista de discrepancias hasta un numero fijo. Si una grabacion
    no tiene tramos por debajo del umbral, lo dice y no lista ninguno: devolver
    siempre los N peores hace pasar por dudoso lo que no lo es.
"""
import difflib, glob, io, itertools, json, os, re, sys, unicodedata

VENTANA = 20.0
UMBRAL = 0.80   # por encima de esto las versiones no se contradicen de verdad
TOPE = 12       # cuantos tramos se imprimen como mucho por grabacion


def dur_legible(s):
    s = int(round(s))
    return ("%d min %02d s" % (s // 60, s % 60)) if s >= 60 else ("%d s" % s)


def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]+", " ", t).split()


def hms(s):
    s = max(0, int(float(s or 0)))
    return "%02d:%02d:%02d" % (s // 3600, (s % 3600) // 60, s % 60)


def cargar(carpeta):
    """Devuelve {codigo: documento publicado} leyendo la subcarpeta datos/."""
    out = {}
    for p in sorted(glob.glob(os.path.join(carpeta, "datos", "*.json"))):
        d = json.load(io.open(p, encoding="utf-8"))
        doc = d.get("publicada") or d.get("principal")
        if not doc:
            continue
        cod = os.path.basename(p).split(" ")[0]
        out[cod] = (d, doc)
    return out


def palabras_en(doc, a, b):
    o = []
    for s in doc["segmentos"]:
        if s["fin"] <= a or s["inicio"] >= b:
            continue
        pal = s.get("palabras") or []
        if pal:
            o += [w["p"] for w in pal if a <= (w["i"] + w["f"]) / 2 < b]
        elif a <= (s["inicio"] + s["fin"]) / 2 < b:
            o.append(s["texto"])
    return " ".join(o)


def acuerdo(a, b, dur):
    t, tot, n = 0.0, 0.0, 0
    while t < dur:
        na, nb = norm(palabras_en(a, t, t + VENTANA)), norm(palabras_en(b, t, t + VENTANA))
        if na or nb:
            tot += difflib.SequenceMatcher(None, na, nb).ratio(); n += 1
        t += VENTANA
    return tot / max(n, 1)


def main():
    global UMBRAL, TOPE
    argumentos = sys.argv[1:]
    for a in list(argumentos):
        if a.startswith("--umbral="):
            UMBRAL = float(a.split("=", 1)[1]); argumentos.remove(a)
        elif a.startswith("--tope="):
            TOPE = int(a.split("=", 1)[1]); argumentos.remove(a)
    carpetas = argumentos
    if len(carpetas) < 2:
        sys.stderr.write(__doc__ + "\n")
        return 2
    nombres = [os.path.basename(c.rstrip("\\/")) or c for c in carpetas]
    datos = [cargar(c) for c in carpetas]
    faltan = [n for n, d in zip(nombres, datos) if not d]
    if faltan:
        sys.stderr.write("Sin datos/ utilizable en: %s\nNo se comparo nada.\n" % ", ".join(faltan))
        return 2

    codigos = sorted(set().union(*[set(d) for d in datos]))

    print("%-6s %-26s %9s %9s %9s %7s" %
          ("audio", "carpeta", "segment", "palabras", "acuerdo", "voces"))
    for cod in codigos:
        for nom, d in zip(nombres, datos):
            if cod not in d:
                print("%-6s %-26s  (no esta)" % (cod, nom)); continue
            meta, doc = d[cod]
            vent = meta.get("ventanas")
            acm = (sum(v["medio"] for v in vent) / len(vent)) if vent else None
            voces = meta.get("voces") or {}
            nv = len(voces.get("hablantes", {})) if isinstance(voces, dict) else 0
            print("%-6s %-26s %9d %9d %8s %7s" % (
                cod, nom, len(doc["segmentos"]),
                sum(len(s.get("palabras") or []) for s in doc["segmentos"]),
                ("%.1f%%" % (100 * acm)) if acm else "—", nv or "—"))
        print()

    print("=== parecido del TEXTO PUBLICADO entre carpetas ===")
    print("1,000 significa texto identico. Que dos carpetas coincidan NO prueba")
    print("que acierten: pueden compartir el mismo error.\n")
    for cod in codigos:
        presentes = [(n, d[cod][1]) for n, d in zip(nombres, datos) if cod in d]
        if len(presentes) < 2:
            continue
        dur = presentes[0][1]["duracion_s"]
        for (na, a), (nb, b) in itertools.combinations(presentes, 2):
            print("  %-5s %-22s vs %-22s  %.3f" % (cod, na, nb, acuerdo(a, b, dur)))
        print()

    print("=== donde TODAS discrepan a la vez (acuerdo por debajo del %d %%) ===" % round(100 * UMBRAL))
    print("Que metodos distintos escriban cosas distintas en el mismo punto es la")
    print("senal mas fuerte que hay aqui de que ahi hay un problema (ADR-017 §8).")
    print("Los tramos POR ENCIMA del umbral NO se listan: no discrepan, y rellenar")
    print("la lista con ellos hace pasar por dudoso lo que no lo es.\n")
    for cod in codigos:
        presentes = [(n, d[cod][1]) for n, d in zip(nombres, datos) if cod in d]
        if len(presentes) < 2:
            continue
        dur = presentes[0][1]["duracion_s"]
        malas, total, t = [], 0, 0.0
        while t < dur:
            tx = {n: palabras_en(doc, t, t + VENTANA) for n, doc in presentes}
            nz = {n: norm(v) for n, v in tx.items()}
            if any(nz.values()):
                total += 1
                pares = [difflib.SequenceMatcher(None, nz[a], nz[b]).ratio()
                         for a, b in itertools.combinations(nz, 2)]
                m = sum(pares) / len(pares)
                if m < UMBRAL:
                    malas.append((m, t, tx))
            t += VENTANA
        malas.sort()
        print("--- %s ---   %d de %d tramos por debajo del umbral" % (cod, len(malas), total))
        if not malas:
            print("      Ninguno: las versiones no se contradicen en esta grabacion.\n")
            continue
        print("      oirlos entero cuesta %s\n" % dur_legible(len(malas) * VENTANA))
        for m, t, tx in malas[:TOPE]:
            print("  [%s] acuerdo medio %d %%" % (hms(t), round(100 * m)))
            for n, v in tx.items():
                print("      %-24s %s" % (n + ":", (v or "—")[:140]))
            print()
        if len(malas) > TOPE:
            print("  (y %d tramos mas por debajo del umbral, no mostrados)\n" % (len(malas) - TOPE))
    print("Ninguna de estas carpetas sustituye a las otras: una version posterior")
    print("puede haber PERDIDO un dato que una anterior si tenia.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
