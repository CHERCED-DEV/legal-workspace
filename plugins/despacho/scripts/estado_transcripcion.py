# -*- coding: utf-8 -*-
"""estado_transcripcion — en qué estado está una transcripción, antes de usarla.

    python estado_transcripcion.py <transcripcion.md> <datos.json>
                                   [--comprobado "comprobado - X.json" ...]
                                   [--json] [--salida informe.md]

Es la puerta entre transcribir y producir cualquier otra cosa con eso. Contesta
tres preguntas y NADA MAS:

    1. ¿Que hay?            metodo, duracion, cuantas lineas tienen motivo de duda.
    2. ¿Quien habla?        cuantas voces, si la separacion aguanta, si estan
                            declaradas y por quien.
    3. ¿Que comprobo ella?  cuantos pasajes marco oyendo el original, y que
                            corrigio -- leyendo el archivo que exporta la pagina,
                            que hasta hoy no leia nadie.

Y termina con lo unico que hace falta saber para seguir: **que preguntarle antes
de producir**, distinto segun lo que se vaya a producir.

Por que existe aparte: el acta, el resumen o cualquier otro producto dependen de
ESTO, no del metodo que nombra voces. Si la puerta viviera dentro de aquel,
pedir un acta obligaria a pasar por el, y son trabajos distintos.

Lo que este programa NO hace:
  · No transcribe, no nombra, no interpreta y no produce ningun documento.
  · No decide si se puede hacer un acta: dice que falta y quien tiene que
    contestarlo, que siempre es una persona.
  · No da por comprobado nada que ella no haya marcado.
"""
import argparse, hashlib, io, json, os, sys

# Criterios ELEGIDOS, no medidos. Se declaran para poder discutirlos.
DOMINANTE_MALA = 0.80      # una voz con mas del 80 % del habla: separacion nominal
DOMINANTE_DUDOSA = 0.60
MINIMO_VOZ_S = 15.0
PUREZA_BAJA = 0.70


def hms(s):
    s = max(0, int(float(s or 0)))
    return "%02d:%02d:%02d" % (s // 3600, (s % 3600) // 60, s % 60)


def duracion(s):
    s = int(round(float(s or 0)))
    return "%d min %02d s" % (s // 60, s % 60) if s >= 60 else "%d s" % s


def plural(n, una, varias):
    return "%d %s" % (n, una if n == 1 else varias)


def falla(msg):
    sys.stderr.write("\nDETENIDO: " + msg + "\n")
    raise SystemExit(2)


def documento(d):
    doc = d.get("publicada") or d.get("principal")
    if not doc:
        falla("ese archivo de datos no trae la pasada publicada")
    return doc


def perfil(doc):
    """Cuanto habla cada voz, segun lo que se publico."""
    voces = {}
    for s in doc["segmentos"]:
        v = s.get("voz")
        if v is None:
            continue
        p = voces.setdefault(v, {"segundos": 0.0, "lineas": 0, "dudosas": 0, "segmentos": []})
        p["segundos"] += max(0.0, s["fin"] - s["inicio"])
        p["lineas"] += 1
        if s.get("pureza", 1) < PUREZA_BAJA:
            p["dudosas"] += 1
        p["segmentos"].append(s)
    return voces


def diagnostico(voces, doc):
    """¿La separacion de voces de esta grabacion sirve para distinguir personas?"""
    total = sum(p["segundos"] for p in voces.values()) or 1.0
    grandes = [v for v, p in voces.items() if p["segundos"] >= MINIMO_VOZ_S]
    dom = max((p["segundos"] for p in voces.values()), default=0.0) / total
    sin_voz = sum(1 for s in doc["segmentos"] if s.get("voz") is None)
    if dom >= DOMINANTE_MALA or len(grandes) < 2:
        veredicto = ("NO SIRVE para distinguir quién habla",
                     "Una sola voz se lleva el %d %% de lo hablado. Cuando eso pasa, lo más "
                     "probable es que el programa haya metido a varias personas en la misma "
                     "voz: ponerle un nombre sería atribuirle a alguien frases de otro."
                     % round(100 * dom))
    elif dom >= DOMINANTE_DUDOSA:
        veredicto = ("DUDOSA",
                     "La voz dominante se lleva el %d %%. Puede ser real —alguien que expone "
                     "durante casi toda la reunión— o una fusión de varias personas. Hay que "
                     "oír las muestras antes de etiquetar." % round(100 * dom))
    else:
        veredicto = ("Sirve como punto de partida",
                     "El habla está repartida entre %d voces. Aun así, que estén separadas no "
                     "prueba que cada una sea una sola persona." % len(grandes))
    return {"voces_con_15s": len(grandes), "dominante": dom, "sin_voz": sin_voz,
            "veredicto": veredicto[0], "porque": veredicto[1]}


def leer_comprobaciones(rutas, clave, doc):
    """Lo que ella marcó en la página. Hasta hoy, nadie volvía a leerlo."""
    res = {"archivos": [], "de_otro_documento": [], "confirmado": 0, "oido": 0,
           "corregido": 0, "correcciones": [], "lineas": set()}
    por_id = {"b%d" % s["i"]: s for s in doc["segmentos"]}
    for r in rutas or []:
        if not os.path.isfile(r):
            falla("no está el archivo de comprobación: %s" % r)
        d = json.load(io.open(r, encoding="utf-8"))
        if d.get("formato") != "despacho/estado-de-comprobacion":
            falla("%s no es un archivo de «Guardar lo comprobado»" % os.path.basename(r))
        # La clave la calcula la pagina como huella del Markdown: si no coincide,
        # esas marcas son de OTRA transcripcion y contarlas seria mentir.
        if clave and d.get("clave") and d["clave"] != clave:
            res["de_otro_documento"].append(os.path.basename(r))
            continue
        res["archivos"].append(os.path.basename(r))
        for bid, marca in (d.get("estado") or {}).items():
            tipo = marca.get("estado")
            if tipo in ("confirmado", "oido", "corregido"):
                res[tipo] += 1
                res["lineas"].add(bid)
            if tipo == "corregido" and marca.get("correccion"):
                s = por_id.get(bid)
                res["correcciones"].append({
                    "minuto": hms(s["inicio"]) if s else "?",
                    "dice_la_maquina": (s["texto"].strip()[:90] if s else ""),
                    "dice_ella": marca["correccion"][:90],
                    "fecha": marca.get("fecha", ""),
                })
    return res


def reunir(args):
    if not os.path.isfile(args.transcripcion):
        falla("no está la transcripción: %s" % args.transcripcion)
    if not os.path.isfile(args.datos):
        falla("no está el archivo de datos: %s" % args.datos)
    md = io.open(args.transcripcion, encoding="utf-8").read()
    clave = hashlib.sha256(md.encode("utf-8")).hexdigest()[:16]
    d = json.load(io.open(args.datos, encoding="utf-8"))
    doc = documento(d)
    voces = perfil(doc)
    dg = diagnostico(voces, doc) if voces else None
    marcas = d.get("marcas") or {}
    dudosas = sum(1 for s in doc["segmentos"]
                  if marcas.get(str(s["i"])) or marcas.get(s["i"]))
    comp = leer_comprobaciones(args.comprobado, clave, doc)
    etiquetas = d.get("etiquetas") or {}
    nombradas = [v for v, e in etiquetas.items() if e.get("texto")]
    return {
        "transcripcion": os.path.basename(args.transcripcion),
        "clave": clave,
        "duracion_s": doc.get("duracion_s"),
        "lineas": len(doc["segmentos"]),
        "lineas_con_duda": dudosas,
        "voces": {str(v): {"segundos": round(p["segundos"], 1), "lineas": p["lineas"]}
                  for v, p in voces.items()},
        "separacion": dg,
        "declaradas": {"cuantas": len(nombradas),
                       "por": (d.get("voces_declaradas") or {}).get("declarado_por"),
                       "fecha": (d.get("voces_declaradas") or {}).get("fecha")},
        "comprobado": {k: v for k, v in comp.items() if k != "lineas"},
        "lineas_marcadas": len(comp["lineas"]),
    }


def que_preguntarle(e):
    """Lo unico accionable: que falta, y para que producto hace falta."""
    faltas = []
    if not e["comprobado"]["archivos"]:
        faltas.append(
            "**Nadie ha comprobado nada oyendo**, o el archivo de «Guardar lo comprobado» no "
            "se ha traído. De %d líneas, **%d tienen motivo de duda**. Pregúntale si ya oyó "
            "algo y, si lo hizo, pídele ese archivo."
            % (e["lineas"], e["lineas_con_duda"]))
    elif e["lineas_marcadas"] < e["lineas_con_duda"]:
        faltas.append(
            "Comprobó **%d líneas** de las **%d con motivo de duda**. Lo que se produzca se "
            "apoya en el resto **sin comprobar**: dilo en el propio documento."
            % (e["lineas_marcadas"], e["lineas_con_duda"]))
    if e["comprobado"]["de_otro_documento"]:
        faltas.append(
            "El archivo de comprobación **es de otra transcripción** (%s): sus marcas NO se "
            "cuentan aquí." % ", ".join(e["comprobado"]["de_otro_documento"]))
    if e["separacion"] and e["separacion"]["veredicto"].startswith("NO SIRVE"):
        faltas.append(
            "**La separación de voces de esta grabación no distingue personas.** No se puede "
            "atribuir nada a nadie a partir del número de hablante, ni siquiera con nombres. "
            "Si el producto necesita decir quién dijo qué, **solo se resuelve oyendo**.")
    elif not e["declaradas"]["cuantas"]:
        faltas.append(
            "**Las voces no tienen nombre.** Si lo que va a producirse atribuye algo a alguien, "
            "pregúntale quién es cada voz (método `nombrar-voces`) o dilo sin nombres.")
    return faltas


def informe(e):
    w = []
    w.append("# Estado de la transcripción — %s\n\n" % e["transcripcion"])
    w.append("**Antes de producir nada con esto.** Contesta tres preguntas, y al final dice "
             "qué hay que preguntarle a ella.\n\n---\n\n")

    w.append("## 1. Qué hay\n\n")
    w.append("| | |\n|---|---|\n")
    w.append("| Duración | %s |\n" % duracion(e["duracion_s"]))
    w.append("| Líneas | %d |\n" % e["lineas"])
    w.append("| Con algún motivo de duda | **%d** (%d %%) |\n"
             % (e["lineas_con_duda"], round(100 * e["lineas_con_duda"] / max(e["lineas"], 1))))

    w.append("\n## 2. Quién habla\n\n")
    if not e["separacion"]:
        w.append("Esta transcripción **no trae voces separadas**.\n")
    else:
        s = e["separacion"]
        w.append("**%s.** %s\n\n" % (s["veredicto"], s["porque"]))
        w.append("| Voz | Habla | Líneas | Nombre |\n|---|---|---|---|\n")
        for v, p in sorted(e["voces"].items(), key=lambda kv: -kv[1]["segundos"]):
            w.append("| Hablante %s | %s | %d | %s |\n"
                     % (v, duracion(p["segundos"]), p["lineas"], "—"))
        if e["declaradas"]["cuantas"]:
            w.append("\n**%d voces declaradas** por %s el %s. No lo comprobó ningún programa.\n"
                     % (e["declaradas"]["cuantas"], e["declaradas"]["por"], e["declaradas"]["fecha"]))
        else:
            w.append("\n**Ninguna voz tiene nombre.** «Hablante N» es un grupo de sonido.\n")

    w.append("\n## 3. Qué comprobó ella oyendo\n\n")
    c = e["comprobado"]
    if not c["archivos"]:
        w.append("**Nada consta.** No se ha traído ningún archivo de «Guardar lo comprobado».\n")
    else:
        w.append("De %s: **%s**, **%s**, **%s**.\n"
                 % (", ".join(c["archivos"]),
                    plural(c["confirmado"], "línea confirmada", "líneas confirmadas"),
                    plural(c["oido"], "oída sin confirmar", "oídas sin confirmar"),
                    plural(c["corregido"], "corregida", "corregidas")))
        w.append("\n*Marcar es constancia de que fue al original, no de que el texto sea correcto.*\n")
        if c["correcciones"]:
            w.append("\n**Lo que ella corrigió — esto manda sobre el texto de la máquina:**\n\n")
            w.append("| Minuto | Dice la máquina | Dice ella |\n|---|---|---|\n")
            for x in c["correcciones"]:
                w.append("| %s | %s | **%s** |\n" % (x["minuto"], x["dice_la_maquina"], x["dice_ella"]))

    w.append("\n---\n\n## Qué preguntarle antes de producir\n\n")
    faltas = que_preguntarle(e)
    if not faltas:
        w.append("Nada pendiente de esta lista. Aun así, **lo que se produzca sigue siendo "
                 "propuesta**: el original es la grabación.\n")
    for f in faltas:
        w.append("- %s\n" % f)

    w.append("\n**Y según lo que se vaya a producir:**\n\n")
    w.append("| Lo que ella pide | Qué exige este estado |\n|---|---|\n")
    w.append("| Un resumen de lo que se dijo | Se puede. **Sin atribuir nada a nadie** |\n")
    w.append("| Un acta, o citar en un escrito | Voces declaradas —o decir expresamente que "
             "van sin nombre— y **los pasajes que se citen, oídos** |\n")
    return "".join(w)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("transcripcion")
    ap.add_argument("datos")
    ap.add_argument("--comprobado", nargs="*", default=[],
                    help="los archivos que deja «Guardar lo comprobado» en la página")
    ap.add_argument("--json", action="store_true", help="los hechos en crudo, sin informe")
    ap.add_argument("--salida", default=None)
    a = ap.parse_args()

    e = reunir(a)
    if a.json:
        print(json.dumps(e, ensure_ascii=False, indent=1))
        return 0
    texto = informe(e)
    if a.salida:
        io.open(a.salida, "w", encoding="utf-8").write(texto)
        print("OK  %s" % os.path.basename(a.salida))
    else:
        sys.stdout.write(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
