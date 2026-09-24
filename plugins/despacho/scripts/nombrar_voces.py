# -*- coding: utf-8 -*-
"""nombrar_voces — qué voz es quién, SEGÚN UNA PERSONA.

    python nombrar_voces.py ficha    <datos.json> [--pagina RUTA] [--salida ficha.md]
    python nombrar_voces.py aplicar  <transcripcion.md> <datos.json> <declaracion.json>
                                     --md-salida NUEVA.md --datos-salida NUEVOS.json

`ficha` prepara lo que hace falta para decidir: cuánto habla cada voz, tres
muestras para reconocerla, las presentaciones que haya en el audio (sin darlas
por buenas) y un diagnóstico de si la separación de esa grabación aguanta.

`aplicar` toma lo que ella declaró y produce una transcripción NUEVA con las
etiquetas puestas, cada una con quién lo dijo y cuándo. Nunca sobrescribe
(ADR-011 §8), nunca cambia una palabra del texto transcrito, y nunca inventa un
nombre: si no está en la declaración, no aparece.

Por que este programa existe aparte de transcribir_audio: aquel tiene prohibido
nombrar voces -- «nunca, ni aunque en el audio alguien se presente» --, porque
la maquina no puede saberlo. Esto no rompe esa regla: la maquina sigue sin
nombrar. Lo que hace es RECOGER la afirmacion de una persona y dejarla escrita
con su procedencia, que es otra cosa.

Lo que este programa NO hace:
  · No deduce quien es nadie, ni del texto ni del audio.
  · No produce un acta ni ningun documento nuevo: solo etiqueta lo que hay.
  · No borra ni reescribe la transcripcion anterior.
"""
import argparse, io, json, os, re, sys

# El diagnostico de separacion NO se define aqui: vive en la puerta
# (estado_transcripcion.py) y se importa. Una sola redaccion de la regla.
from estado_transcripcion import perfil, diagnostico, PUREZA_BAJA  # noqa: E402

# Formas de presentarse. Solo sirven para ENSENAR candidatos, nunca para asignar.
PRESENTACION = re.compile(
    r"\b(soy|me llamo|mi nombre es|les habla|habla con|para los que no me conocen)\b",
    re.IGNORECASE)


def duracion(s):
    """«3 min 06 s», no «00:03:06»: una duracion no es una marca de tiempo, y
    confundirlas hace creer que la voz empieza en ese minuto."""
    s = int(round(float(s or 0)))
    return "%d min %02d s" % (s // 60, s % 60) if s >= 60 else "%d s" % s


def hms(s):
    s = max(0, int(float(s or 0)))
    return "%02d:%02d:%02d" % (s // 3600, (s % 3600) // 60, s % 60)


def falla(msg):
    sys.stderr.write("\nDETENIDO: %s\n" % msg)
    raise SystemExit(2)


def cargar(ruta, que):
    if not os.path.isfile(ruta):
        falla("no está %s: %s" % (que, ruta))
    return json.load(io.open(ruta, encoding="utf-8"))


def documento(d):
    doc = d.get("publicada") or d.get("principal")
    if not doc:
        falla("ese archivo de datos no trae la pasada publicada")
    return doc


# --------------------------------------------------------------------- ficha
def intervenciones(segs):
    """Tramos seguidos de esa voz, de más largo a más corto: sirven de muestra."""
    grupos, actual = [], []
    for s in segs:
        if actual and s["inicio"] - actual[-1]["fin"] > 3.0:
            grupos.append(actual); actual = []
        actual.append(s)
    if actual:
        grupos.append(actual)
    for g in grupos:
        g.sort(key=lambda x: x["inicio"])
    return sorted(grupos, key=lambda g: -(g[-1]["fin"] - g[0]["inicio"]))


def enlace(pagina, inicio, texto):
    if not pagina:
        return texto
    return "[%s](<%s#t=%d>)" % (texto, pagina, int(inicio))


def ficha(args):
    d = cargar(args.datos, "el archivo de datos")
    doc = documento(d)
    voces = perfil(doc)
    if not voces:
        falla("esta transcripción no tiene voces separadas: no hay nada que nombrar")
    dg = diagnostico(voces, doc)
    total = sum(p["segundos"] for p in voces.values()) or 1.0

    w = []
    w.append("# Quién es cada voz — %s\n\n" % (args.titulo or os.path.basename(args.datos)))
    w.append("**Qué se le pide:** decir quién es cada voz, o decir que no lo sabe. "
             "Las dos respuestas sirven.\n\n")
    w.append("**Qué NO se le pide:** adivinar. Una voz sin nombre es mejor que un nombre "
             "equivocado en un documento que puede acabar en un escrito.\n")
    w.append("\n---\n")
    w.append("## Antes de nada: ¿la separación de esta grabación aguanta?\n\n")
    w.append("**%s.** %s\n" % (dg["veredicto"], dg["porque"]))
    w.append("\n")
    w.append("\n| | |\n|---|---|\n")
    w.append("| Voces con 15 segundos o más | %d |\n" % dg["voces_con_15s"])
    w.append("| Parte del habla en la voz que más habla | %d %% |\n" % round(100 * dg["dominante"]))
    w.append("| Líneas sin voz asignada | %d |\n" % dg["sin_voz"])
    w.append("\n*Los umbrales de este veredicto (80 %, 60 %, 15 s) son una elección, no una "
             "medida: nadie ha comprobado a oído cuántas personas hablan en esta grabación.*\n")

    for v, p in sorted(voces.items(), key=lambda kv: -kv[1]["segundos"]):
        w.append("\n---\n")
        w.append("\n## Hablante %s\n\n" % v)
        w.append("\nHabla **%s** en total (%d %% de lo hablado), en **%d líneas**.%s\n"
                 % (duracion(p["segundos"]), round(100 * p["segundos"] / total), p["lineas"],
                    "  ⚠ %d de esas líneas tienen voz dudosa." % p["dudosas"] if p["dudosas"] else ""))
        grupos = intervenciones(p["segmentos"])
        muestras = []
        if grupos:
            muestras.append(("La intervención más larga", grupos[0]))
        primera = min(p["segmentos"], key=lambda s: s["inicio"])
        muestras.append(("La primera vez que aparece", [primera]))
        if len(grupos) > 1:
            muestras.append(("Otra intervención", grupos[1]))
        w.append("\n**Para reconocerla, oiga:**\n\n")
        vistos = set()
        for etiqueta, g in muestras:
            ini = g[0]["inicio"]
            if hms(ini) in vistos:
                continue
            vistos.add(hms(ini))
            texto = " ".join(s["texto"].strip() for s in g)[:180]
            w.append("- **%s** — %s: «%s…»\n"
                     % (etiqueta, enlace(args.pagina, ini, hms(ini)), texto))
        cand = [s for s in p["segmentos"] if PRESENTACION.search(s["texto"])]
        if cand:
            w.append("\n**Se presenta alguien en estas líneas** (⚠ sin comprobar, la máquina "
                     "escribe mal los nombres propios):\n\n")
            for s in cand[:4]:
                w.append("- %s: «%s»\n" % (enlace(args.pagina, s["inicio"], hms(s["inicio"])),
                                           s["texto"].strip()[:140]))
        w.append("\n**Quién es:** ______________________  ")
        w.append("**Cargo o entidad:** ______________________  \n")
        w.append("**Cómo lo sé:** la reconozco / se presentó en el minuto ___ / me lo dijeron / "
                 "no lo sé  \n")

    w.append("\n---\n")
    w.append("\n## Las tres respuestas que también valen\n\n")
    w.append("- **«No sé quién es»** — la voz se queda con su número.\n")
    w.append("- **«Esta voz son dos personas»** — se marca así, y **no se le pone nombre a ninguna**.\n")
    w.append("- **«Estas dos voces son la misma persona»** — se unen bajo un solo nombre.\n")
    salida = args.salida or (os.path.splitext(args.datos)[0] + " - quien es cada voz.md")
    if os.path.exists(salida) and not args.forzar:
        falla("ya existe %s (usa --forzar si de verdad quieres reemplazarlo)" % salida)
    io.open(salida, "w", encoding="utf-8").write("".join(w))
    print("OK  %s  -  %d voces, veredicto: %s" % (os.path.basename(salida), len(voces), dg["veredicto"]))
    return 0


# ------------------------------------------------------------------- aplicar
def etiqueta_de(v, decl, fundida):
    """Texto visible de una voz, con su advertencia si la lleva."""
    quien = (decl.get("quien") or "").strip()
    cargo = (decl.get("cargo") or "").strip()
    if decl.get("varias_personas"):
        return None, "⚠ esta voz agrupa a más de una persona: no atribuya nada a partir del número"
    if not quien:
        return None, None
    texto = quien + (" · " + cargo if cargo else "")
    aviso = ("⚠ el programa agrupó esta voz; puede contener a más de una persona"
             if fundida else None)
    return texto, aviso


def aplicar(args):
    d = cargar(args.datos, "el archivo de datos")
    doc = documento(d)
    decl = cargar(args.declaracion, "la declaración")
    if decl.get("formato") != "despacho/voces-declaradas":
        falla("esa declaración no tiene el formato «despacho/voces-declaradas»")
    quien_declara = (decl.get("declarado_por") or "").strip()
    fecha = (decl.get("fecha") or "").strip()
    if not quien_declara or not fecha:
        falla("la declaración tiene que decir QUIÉN la hace y CUÁNDO: sin eso, una etiqueta "
              "no es de nadie y no vale para nada")

    voces = perfil(doc)
    dg = diagnostico(voces, doc)
    fundida_general = dg["veredicto"].startswith("NO SIRVE")

    etiquetas, problemas = {}, []
    for v, info in (decl.get("voces") or {}).items():
        if str(v) not in {str(k) for k in voces}:
            problemas.append("la declaración habla de la voz %s, que no existe en esta grabación" % v)
            continue
        if info.get("mismo_que"):
            otro = str(info["mismo_que"])
            base = (decl["voces"].get(otro) or {})
            info = dict(base, nota=("Declarada como la misma persona que Hablante %s. " % otro)
                        + (info.get("nota") or ""))
        fundida = bool(info.get("varias_personas")) or fundida_general
        texto, aviso = etiqueta_de(v, info, fundida)
        if texto and fundida and not info.get("acepta_advertencia"):
            problemas.append(
                "voz %s: esta grabación no separa bien las voces (%s) y la declaración le pone "
                "nombre sin aceptar la advertencia. Añade \"acepta_advertencia\": true si aun "
                "así quieres etiquetarla — la advertencia viajará pegada a la etiqueta." % (v, dg["veredicto"]))
            continue
        if not texto and not aviso:
            continue
        etiquetas[str(v)] = {
            "texto": texto, "aviso": aviso,
            "como_lo_se": (info.get("como_lo_se") or "").strip(),
            "nota": (info.get("nota") or "").strip(),
            "procedencia": "Lo afirma %s, el %s. No lo comprobó ningún programa." % (quien_declara, fecha),
        }
    if problemas:
        falla("no se escribió nada:\n  - " + "\n  - ".join(problemas))
    if not etiquetas:
        falla("la declaración no pone ninguna etiqueta: no hay nada que aplicar")

    for ruta in (args.md_salida, args.datos_salida):
        if os.path.exists(ruta) and not args.forzar:
            falla("ya existe %s. Regenerar produce versión nueva, nunca sobrescribe (ADR-011 §8)" % ruta)

    md = io.open(args.transcripcion, encoding="utf-8").read()
    cab, sep, cuerpo = md.partition("\n---\n")
    if not sep:
        falla("esa transcripción no tiene separador de cabecera")

    # El nombre se pone por el NUMERO del Markdown y se guarda por el numero de
    # los datos. Si los dos no numeran igual -- se rehizo la separacion y el
    # Markdown se quedo viejo --, el nombre caeria en el Word sobre lineas de
    # otra persona. Se comprueba linea a linea antes de escribir nada.
    efectivas, cur = [], None
    for m in re.finditer(r"^\*\*\[\d\d:\d\d:\d\d\]( · Hablante ([^\s*]+)[^*]*)?\*\*", cuerpo, re.M):
        if m.group(2):
            cur = m.group(2)
        efectivas.append(cur)
    de_datos = ["?" if s.get("voz") is None else str(s.get("voz")) for s in doc["segmentos"]]
    if len(efectivas) != len(de_datos) or efectivas != de_datos:
        distintas = sum(1 for a, b in zip(efectivas, de_datos) if a != b)
        falla("la transcripción y los datos no numeran igual las voces (%d de %d líneas distintas, "
              "%d líneas frente a %d segmentos). Regenere la transcripción desde esos datos antes de "
              "poner nombres: si no, el nombre caería sobre líneas de otra voz. No se escribió nada."
              % (distintas, len(de_datos), len(efectivas), len(de_datos)))

    lineas = ["**Quién es cada voz:** lo declaró **%s** el **%s**. **No lo comprobó ningún "
              "programa**: la máquina agrupó las voces, y el nombre lo puso una persona."
              % (quien_declara, fecha)]
    for v in sorted(etiquetas, key=lambda x: int(x) if x.isdigit() else 99):
        e = etiquetas[v]
        partes = ["Hablante %s" % v]
        if e["texto"]:
            partes.append("**%s**" % e["texto"])
        if e["como_lo_se"]:
            partes.append("*(%s)*" % e["como_lo_se"])
        if e["aviso"]:
            partes.append(e["aviso"])
        lineas.append("- " + " — ".join(partes))
    cab = cab.rstrip() + "\n\n" + "\n".join(lineas) + "\n"

    # El cuerpo: solo se toca la CABECERA de turno, nunca el texto transcrito.
    def poner(m):
        v = m.group(2)
        e = etiquetas.get(v)
        if not e or not e["texto"]:
            return m.group(0)
        return "**[%s] · Hablante %s — %s**" % (m.group(1), v, e["texto"])

    antes = cuerpo
    cuerpo = re.sub(r"\*\*\[(\d\d:\d\d:\d\d)\] · Hablante (\d+)\*\*", poner, cuerpo)
    sin_cabeceras = lambda t: re.sub(r"\*\*\[\d\d:\d\d:\d\d\][^*]*\*\*", "", t)
    if sin_cabeceras(antes) != sin_cabeceras(cuerpo):
        falla("al poner las etiquetas cambió texto transcrito. No se escribió nada.")

    io.open(args.md_salida, "w", encoding="utf-8").write(cab + sep + cuerpo)
    d["etiquetas"] = etiquetas
    d["voces_declaradas"] = {"declarado_por": quien_declara, "fecha": fecha,
                             "declaracion": os.path.basename(args.declaracion)}
    json.dump(d, io.open(args.datos_salida, "w", encoding="utf-8"), ensure_ascii=False)
    print("OK  %s  -  %d voces etiquetadas, %d sin nombre"
          % (os.path.basename(args.md_salida), sum(1 for e in etiquetas.values() if e["texto"]),
             len(voces) - sum(1 for e in etiquetas.values() if e["texto"])))
    print("    La transcripción anterior no se tocó.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="orden", required=True)

    f = sub.add_parser("ficha", help="preparar lo necesario para que una persona decida")
    f.add_argument("datos")
    f.add_argument("--pagina", default=None,
                   help="ruta de la pagina de esa grabacion, para enlazar los minutos")
    f.add_argument("--titulo", default=None)
    f.add_argument("--salida", default=None)
    f.add_argument("--forzar", action="store_true")
    f.set_defaults(fn=ficha)

    a = sub.add_parser("aplicar", help="poner las etiquetas que una persona declaro")
    a.add_argument("transcripcion")
    a.add_argument("datos")
    a.add_argument("declaracion")
    a.add_argument("--md-salida", required=True)
    a.add_argument("--datos-salida", required=True)
    a.add_argument("--forzar", action="store_true")
    a.set_defaults(fn=aplicar)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
