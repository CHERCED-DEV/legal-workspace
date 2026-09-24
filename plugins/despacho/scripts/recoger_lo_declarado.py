# -*- coding: utf-8 -*-
"""recoger_lo_declarado — junta lo que ella declaró oyendo, para refinar con ello.

    python recoger_lo_declarado.py <carpeta de la entrega> --salida <carpeta> [archivo.json ...]

Las páginas de «oír y marcar» guardan lo que ella hace en «Lo que declaré»:
si la entrega está dentro de un proyecto del Despacho (…/3-Para presentar/),
en el PROYECTO, en «2-Borradores/Lo que declaré/<entrega>/», para que rehacer
la entrega no lo toque; si no, dentro de la propia entrega, en cualquier
carpeta «Lo que declaré» que haya dentro, a cualquier nivel. (En navegadores
que no lo permiten, se descarga: esos archivos se pasan a mano.) También se
mira, solo para leer, donde lo guardaban las páginas antes: «1-Documentos
recibidos/Lo que declaré/<entrega>/». Este programa los recoge, casa cada uno
con su página por la CLAVE del documento, y escribe un informe legible y un
.json con todo junto:

  · el texto: qué líneas confirmó, oyó o corrigió (y la corrección);
  · quién habla: cuánto de cada voz confirmó oyendo, qué voces quedan
    identificadas, los nombres que escribió y cada fragmento decidido;
  · lo que no se entiende: la idea principal y quién la dijo, según ella;
  · los compromisos: si lo son, quién los asume y qué plazo oyó;
  · el glosario: lo que la máquina oye mal y lo que se dijo.

Eso es lo que sirve para refinar el resumen y el acta: es una DECLARACIÓN
suya, oyendo, con fecha. Lo que la máquina propuso y ella no confirmó no
entra aquí como hecho, y lo que ella no contestó no se rellena.

No sobrescribe nunca: cada informe lleva la fecha y hora en el nombre.
Un archivo cuya clave no es la de ninguna página de la entrega se descarta y
se dice: sería una declaración sobre otra versión de la transcripción. Y un
compromiso o un tramo declarado que no casa con los de la página (la lectura
de compromisos o los tramos cambiaron después) se dice aparte.
"""
import argparse, datetime, glob, html, io, json, os, re, sys, unicodedata

CARPETA = "Lo que declaré"
# Dentro del proyecto, lo mismo que escribe la página (src/guardado.js). En
# 2-Borradores y no en 1-Documentos recibidos, que es plana y donde ningún
# programa escribe (ADR-018).
EN_PROYECTO = ("2-Borradores", CARPETA)
# Donde la guardaban las páginas antes. Solo se lee: lo que ella dejó ahí
# sigue siendo suyo.
ANTES_EN_PROYECTO = ("1-Documentos recibidos", CARPETA)


def carpetas_de(entrega):
    """Donde puede estar lo que ella guardó de esta entrega: cualquier carpeta
    «Lo que declaré» dentro de la entrega (si al guardar eligió
    «Transcripciones», queda ahí dentro) y, si la entrega está en un
    proyecto, la del proyecto."""
    entrega = os.path.normpath(entrega)
    out = [os.path.join(entrega, CARPETA)]
    for r, ds, _ in os.walk(entrega):
        ds.sort()
        if os.path.basename(r) == CARPETA and r not in out:
            out.append(r)
    # El proyecto: la entrega vive en «<proyecto>/2-Borradores/Entregas/»
    # (ADR-023), o en «<proyecto>/3-Para presentar/» en proyectos sin ordenar.
    padre = os.path.dirname(entrega)
    proyecto = None
    if os.path.basename(padre) == "Entregas" and os.path.basename(os.path.dirname(padre)) == "2-Borradores":
        proyecto = os.path.dirname(os.path.dirname(padre))
    elif os.path.basename(padre) == "3-Para presentar":
        proyecto = os.path.dirname(padre)
    if proyecto:
        for donde in (EN_PROYECTO, ANTES_EN_PROYECTO):
            out.append(os.path.join(proyecto, *donde, os.path.basename(entrega)))
    return out


def falla(msg):
    sys.stderr.write("\nDETENIDO: " + msg + "\n")
    raise SystemExit(2)


def hms(s):
    s = max(0, int(float(s or 0)))
    return "%02d:%02d:%02d" % (s // 3600, (s % 3600) // 60, s % 60)


def paginas(entrega):
    """{clave: {titulo, archivo, caso, horas: {bloque: hh:mm:ss}, textos: {bloque: texto},
    ilegibles: {id: tramo}, compromisos: {id: compromiso}}}"""
    out = {}
    for p in glob.glob(os.path.join(entrega, "Transcripciones", "*.html")):
        with io.open(p, encoding="utf-8") as f:
            t = f.read()
        m = re.search(r'<script type="application/json" id="datos">(.*?)</script>', t, re.S)
        if not m:
            continue
        try:
            d = json.loads(m.group(1))
        except ValueError:
            continue
        if not d.get("clave"):
            continue
        horas = {b["id"]: hms(b["ancla"]["inicio"]) for b in d.get("bloques", []) if b.get("ancla", {}).get("tipo") == "tiempo"}
        textos = {}
        for a in re.finditer(r'<article class="seg[^"]*" id="(b\d+)">.*?<p class="texto">(.*?)</p>', t, re.S):
            textos[a.group(1)] = html.unescape(re.sub(r"<[^>]+>", "", a.group(2))).strip()
        out[d["clave"]] = {"titulo": d.get("documento", {}).get("titulo") or os.path.basename(p),
                           "archivo": os.path.basename(p), "caso": d.get("caso"), "horas": horas, "textos": textos,
                           "ilegibles": {x["id"]: x for x in d.get("ilegibles", [])},
                           "compromisos": {x["id"]: x for x in d.get("compromisos", [])}}
    return out


def declaraciones(entrega, extra):
    """Las declaraciones que se pueden leer, cada una con su procedencia real:
    «_carpeta» es la carpeta «Lo que declaré» de donde salió, o None si se
    pasó a mano."""
    rutas = [(r, c) for c in carpetas_de(entrega) for r in sorted(glob.glob(os.path.join(c, "*.json")))]
    rutas += [(r, None) for r in (extra or [])]
    docs, vistas = [], set()
    for r, c in rutas:
        k = os.path.normcase(os.path.abspath(r))
        if k in vistas:
            continue
        vistas.add(k)
        try:
            with io.open(r, encoding="utf-8") as f:
                d = json.load(f)
        except (ValueError, OSError) as e:
            sys.stderr.write("AVISO: no se pudo leer %s (%s)\n" % (r, e))
            continue
        if not isinstance(d, dict) or d.get("formato") != "despacho/estado-de-comprobacion":
            sys.stderr.write("AVISO: %s no es una declaración de la página; se ignora\n" % os.path.basename(r))
            continue
        d["_ruta"] = r
        d["_carpeta"] = c
        docs.append(d)
    return docs


def lo_ultimo(docs):
    """Por documento, la declaración más reciente (por fecha de guardado)."""
    por = {}
    for d in docs:
        k = d.get("clave")
        if k not in por or (d.get("exportado") or "") > (por[k].get("exportado") or ""):
            por[k] = d
    return por


ESTADO = {"confirmado": "confirmada", "oido": "oída sin poder confirmar", "corregido": "corregida"}
DECISION = {"si": "sí, es esa voz", "otra": "es otra voz", "no_se": "no sabe quién", "varios": "hablan varios"}
ENTIENDE = {"si": "se entiende", "en_parte": "se entiende en parte", "no": "no se entiende", "sin_habla": "no hay nadie hablando"}
NO_LO_DIJO = "— (no lo dijo)"


def celda(v):
    """Lo que va en una celda de tabla Markdown. Un salto de línea partía la
    fila y una «|» abría una columna que no existe: lo que ella escribió
    acababa en otra columna, atribuido a otra cosa."""
    t = "" if v is None else str(v)
    t = " / ".join(x.strip() for x in t.replace("\r\n", "\n").replace("\r", "\n").split("\n") if x.strip())
    return t.replace("|", "\\|") or "—"


def fila(*celdas):
    return "| %s |" % " | ".join(celda(c) for c in celdas)


def voz_txt(v, nombres):
    if v is None or v == "":
        return "sin voz"
    if v in ("no_se", "nueva"):
        return {"no_se": "no sabe quién", "nueva": "una voz que no está en la lista"}[v]
    rot = ("Voz nueva %s" % v[6:]) if str(v).startswith("nueva-") else "Hablante %s" % v
    n = (nombres or {}).get(str(v), "").strip()
    return "%s (%s, según ella)" % (rot, n) if n else rot


def mostrar(ruta, base):
    """La ruta como se enseña: relativa a `base` si cuelga de ahí; si no, entera."""
    try:
        r = os.path.relpath(ruta, base)
    except ValueError:
        return os.path.abspath(ruta)
    return os.path.abspath(ruta) if r.startswith("..") else r


def de_donde_partio(e):
    """Si al corregir partió de una lectura automática, cuál y qué decía."""
    p, s = (e.get("partio_de") or "").strip(), (e.get("sugerido") or "").strip()
    if not p and not s:
        return ""
    que = (p[:1].lower() + p[1:]) if p else "una lectura automática"
    # La página nombra las lecturas como en sus pistas: «Lectura del canal derecho».
    if que.startswith("lectura "):
        que = "la " + que
    return " (partió de %s%s)" % (que, ", que decía «%s»" % s if s else "")


def casa_compromiso(p, cid, x):
    """Lo declarado vale para ese compromiso solo si la página lo tiene con
    ese id y en ese minuto: el id sale del segundo y de la cita."""
    c = p["compromisos"].get(cid)
    return bool(c) and (c.get("minuto") or "") == (x.get("minuto") or "")


def _seg(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def casa_ilegible(p, iid, x):
    """Lo contado casa con un tramo de la página si es el mismo tramo
    (desde y hasta), se llame como se llame."""
    a, b = _seg(x.get("desde")), _seg(x.get("hasta"))
    if a is None or b is None:
        return False
    mismo = lambda y: (_seg(y.get("desde")) is not None and _seg(y.get("hasta")) is not None
                       and abs(_seg(y["desde"]) - a) < 0.01 and abs(_seg(y["hasta"]) - b) < 0.01)
    y = p["ilegibles"].get(iid)
    return mismo(y) if y is not None else any(mismo(y) for y in p["ilegibles"].values())


def fila_ilegible(x, nombres):
    # «¿Quién lo dice?» solo se pregunta si se entiende algo; si no eligió a
    # nadie, no lo dijo: no es «no sabe quién».
    pregunta = x.get("entiende") in ("si", "en_parte")
    q = x.get("quien")
    if q in (None, "", "sin_contestar"):
        quien = NO_LO_DIJO if pregunta else "—"
    else:
        quien = voz_txt(q, nombres)
    return fila("%s–%s" % (hms(x.get("desde")), hms(x.get("hasta"))), ENTIENDE.get(x.get("entiende"), "—"),
                x.get("idea") or "—", quien, x.get("palabras") or "—")


def fila_compromiso(x, nombres):
    # Quién y plazo solo si dijo que es un compromiso: si después cambió a
    # «No lo es», lo que quedó guardado de antes no se atribuye.
    es = x.get("es")
    if es == "si":
        q = x.get("quien")
        if q == "otra":
            quien = x.get("quien_texto") or NO_LO_DIJO
        elif q == "no_se_dice":
            quien = "no se dice"
        else:
            quien = voz_txt(q, nombres) if q else NO_LO_DIJO
        plazo = x.get("plazo") or NO_LO_DIJO
    else:
        quien = plazo = "— (no es compromiso)" if es == "no" else "— (no dijo si lo es)"
    return fila(x.get("minuto") or "—", {"si": "sí", "no": "no"}.get(es, "—"), quien, plazo)


def plano(s):
    return unicodedata.normalize("NFC", s or "").strip().lower()


def _cuando(e):
    """Fecha de una entrada del glosario, para ordenar: «cuando» (ISO) si la
    trae; si no, «fecha» (dd/mm/aaaa, como la escribe la página, o ISO)."""
    c = (e.get("cuando") or "").strip()
    if c:
        return c
    f = (e.get("fecha") or "").strip()
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", f)
    return "%s-%02d-%02d" % (m.group(3), int(m.group(2)), int(m.group(1))) if m else f


def glosario_del_caso(ultimas, paginas_):
    """({oye: (entrada, orden, clave si la página no tiene caso)}, {oye: entrada quitada}).

    El glosario es UNO por caso (la página lo guarda con el caso), así que
    cada guardado lleva el glosario entero de ese momento, y vale el del
    guardado más reciente de cada caso: lo que falta en él, ella lo quitó
    después, y darlo por bueno porque lo trae una página más vieja era
    atribuirle lo que ya no dice. Entre páginas sin caso, cada una con su
    glosario, se junta por «oye» y gana la entrada más reciente."""
    por_caso = {}
    for clave, d in ultimas.items():
        if isinstance(d.get("glosario"), list):
            caso = (paginas_.get(clave) or {}).get("caso")
            por_caso.setdefault(caso or ("clave", clave), []).append((clave, d))
    vigentes, quitadas = {}, {}
    for caso, ds in por_caso.items():
        ds.sort(key=lambda cd: cd[1].get("exportado") or "")
        clave, ultimo = ds[-1]
        suyo = {}
        for k, e in enumerate(ultimo["glosario"]):
            if isinstance(e, dict) and (e.get("oye") or "").strip():
                o = plano(e["oye"])
                if o not in suyo or (_cuando(e), k) >= (_cuando(suyo[o][0]), suyo[o][1]):
                    suyo[o] = (e, k)
        for _c, d in ds[:-1]:
            for e in d["glosario"]:
                if isinstance(e, dict) and (e.get("oye") or "").strip() and plano(e["oye"]) not in suyo:
                    quitadas.setdefault(plano(e["oye"]), e)
        sola = clave if isinstance(caso, tuple) else None
        for o, (e, _k) in suyo.items():
            orden = (_cuando(e), ultimo.get("exportado") or "")
            if o not in vigentes or orden >= vigentes[o][1]:
                vigentes[o] = (e, orden, sola)
    return vigentes, {o: e for o, e in quitadas.items() if o not in vigentes}


def es_sugerencia(e):
    return bool(e.get("de")) or "sugerencia" in (e.get("origen") or "")


def origen_glosario(e):
    if es_sugerencia(e):
        return "sugerencia rechazada" if e.get("estado") == "rechazada" else "sugerencia aceptada"
    return "suya"


def nota_glosario(e):
    """La nota de ella, y aparte la de la sugerencia, que es de la máquina.
    Antes, al aceptar una sugerencia, la página copiaba su nota como si fuera
    de ella: sin «nota_maquina», la nota de una sugerencia es de la máquina."""
    suya, maquina = (e.get("nota") or "").strip(), (e.get("nota_maquina") or "").strip()
    if es_sugerencia(e) and "nota_maquina" not in e:
        suya, maquina = "", suya
    partes = ([suya] if suya else []) + (["(nota de la sugerencia, de la máquina: %s)" % maquina] if maquina else [])
    return " ".join(partes) or "—"


def salvo_en(e, paginas_, sola):
    """Las líneas donde ella dijo que la regla no vale («aquí sí se dijo eso»).
    La página las guardaba como el id de la línea, sin decir de qué
    grabación; ahora como {clave, id}. Las dos formas se leen."""
    out = []
    for x in e.get("excepciones") or []:
        if isinstance(x, dict):
            clave, bid = x.get("clave"), x.get("id")
        else:
            clave, bid = sola, x
        p = paginas_.get(clave) if clave else None
        if p and bid in p["horas"]:
            t = "%s, %s" % (p["titulo"], p["horas"][bid])
        elif p:
            t = "%s, línea %s" % (p["titulo"], bid)
        elif clave:
            t = "línea %s de otra versión de la transcripción" % bid
        else:
            t = "línea %s, sin decir de qué grabación" % bid
        if isinstance(x, dict) and (x.get("dijo") or "").strip():
            t += " (según ella, ahí se dijo «%s»)" % x["dijo"].strip()
        out.append(t)
    return "; ".join(out) or "—"


def informe(entrega, paginas_, ultimas, descartadas, docs=None):
    w = []
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    base = os.path.dirname(os.path.dirname(os.path.normpath(entrega)))
    usados = {id(d) for d in ultimas.values()}
    w.append("# Lo que declaró ella, oyendo\n")
    w.append("**Recogido:** %s\n" % ahora)
    docs = docs if docs is not None else list(ultimas.values())
    if docs:
        # La procedencia REAL de cada archivo: de qué carpeta salió, o que se
        # pasó a mano. Decir «de Lo que declaré» de un archivo de Descargas es
        # falso.
        w.append("**De dónde salió cada archivo:**\n")
        por_carpeta = {}
        for d in docs:
            por_carpeta.setdefault(d.get("_carpeta"), []).append(d)
        for c in sorted(por_carpeta, key=lambda c: (c is None, c or "")):
            nombres = ", ".join("`%s`%s" % (os.path.basename(d["_ruta"]) if c else os.path.abspath(d["_ruta"]),
                                            "" if id(d) in usados else " (no se usa: hay uno más reciente, o es de otra versión)")
                                for d in sorted(por_carpeta[c], key=lambda d: d["_ruta"]))
            w.append("- %s: %s" % ("de la carpeta `%s`" % mostrar(c, base) if c else "pasados a mano", nombres))
        w.append("")
    w.append("**Qué es:** lo que una persona declaró **oyendo la grabación**, en las páginas de «oír y marcar». "
             "Es la fuente para refinar el resumen y el acta. **Lo que la máquina propuso y ella no confirmó no está "
             "aquí como hecho.**\n")
    if descartadas:
        w.append("> ⚠ Se descartaron %d archivos de otra versión de la transcripción (su clave no es la de ninguna "
                 "página de esta entrega): %s\n" % (len(descartadas), ", ".join(descartadas)))
    w.append("---\n")
    for clave, d in sorted(ultimas.items(), key=lambda kv: paginas_[kv[0]]["titulo"]):
        p = paginas_[clave]
        w.append("## %s\n" % p["titulo"])
        w.append("Guardado por ella el %s · página `%s` · archivo `%s` (%s)\n" % (
            (d.get("exportado") or "")[:16].replace("T", " "), p["archivo"], os.path.basename(d.get("_ruta") or "—"),
            "pasado a mano" if d.get("_ruta") and not d.get("_carpeta") else "de «%s»" % CARPETA))
        est = d.get("estado") or {}
        if est:
            cuenta = {}
            for e in est.values():
                cuenta[e.get("estado")] = cuenta.get(e.get("estado"), 0) + 1
            w.append("### El texto\n")
            w.append(", ".join("%d %s" % (n, ESTADO.get(k, k) + ("s" if n != 1 and k in ESTADO else "")) for k, n in cuenta.items()) + ".\n")
            corr = [(b, e) for b, e in est.items() if e.get("estado") == "corregido"]
            if corr:
                w.append("| Minuto | La transcripción dice | Según ella, dice |\n|---|---|---|")
                for b, e in sorted(corr, key=lambda x: p["horas"].get(x[0], "")):
                    w.append(fila(p["horas"].get(b, b), p["textos"].get(b, ""),
                                  (e.get("correccion") or "(no escribió la corrección)") + de_donde_partio(e)))
                w.append("")
        nombres = d.get("voces") or {}
        rv = d.get("resumen_voces") or {}
        at = d.get("atribucion") or {}
        if rv or at:
            w.append("### Quién habla\n")
            if rv:
                w.append("| Voz | Confirmado oyendo | Identificada (85 %) | Nombre que escribió ella |\n|---|---|---|---|")
                for v, r in sorted(rv.items(), key=lambda kv: -kv[1].get("segundos", 0)):
                    w.append(fila(voz_txt(v, None),
                                  "%d %% (%d de %d s)" % (int(r.get("confirmado", 0) * 100), r.get("segundos_confirmados", 0), r.get("segundos", 0)),
                                  "sí" if r.get("identificada") else ("añadida por ella" if r.get("anadida_por_usted") else "no"),
                                  (nombres.get(v) or "").strip() or "—"))
                w.append("")
            movidos = [(b, x) for b, x in at.items() if x.get("decision") in ("otra", "no_se", "varios")]
            if movidos:
                w.append("Fragmentos donde **no** es la voz que proponía la máquina, o no se sabe:\n")
                w.append("| Desde | La máquina decía | Según ella |\n|---|---|---|")
                for b, x in sorted(movidos, key=lambda kv: (kv[1].get("firma") or {}).get("inicio", 0)):
                    w.append(fila(hms((x.get("firma") or {}).get("inicio", 0)), voz_txt(x.get("maquina"), None),
                                  voz_txt(x.get("voz"), nombres) if x.get("decision") == "otra" else DECISION[x["decision"]]))
                w.append("")
        il = d.get("ilegibles") or {}
        if il:
            casan = [x for i, x in il.items() if casa_ilegible(p, i, x)]
            sueltos = [x for i, x in il.items() if not casa_ilegible(p, i, x)]
            cab = "| Tramo | ¿Se entiende? | La idea principal, según ella | Quién lo dice | Palabras que oyó |\n|---|---|---|---|---|"
            w.append("### Lo que no se entendía, contado por ella\n")
            if casan:
                w.append(cab)
                for x in sorted(casan, key=lambda x: _seg(x.get("desde")) or 0):
                    w.append(fila_ilegible(x, nombres))
                w.append("")
            if sueltos:
                w.append("> ⚠ %d tramo(s) que ella contó y que esta página ya no pregunta: la lista de tramos cambió "
                         "después. Lo que contó vale para esos minutos, que son los que oyó, pero no casa con ningún "
                         "tramo de ahora.\n" % len(sueltos))
                w.append(cab)
                for x in sorted(sueltos, key=lambda x: _seg(x.get("desde")) or 0):
                    w.append(fila_ilegible(x, nombres))
                w.append("")
        co = d.get("compromisos") or {}
        if co:
            casan = [x for i, x in co.items() if casa_compromiso(p, i, x)]
            sueltos = [x for i, x in co.items() if not casa_compromiso(p, i, x)]
            cab = "| Minuto | ¿Es un compromiso? | Quién lo asume | Plazo que oyó |\n|---|---|---|---|"
            w.append("### Los compromisos, según ella\n")
            if casan:
                w.append(cab)
                for x in sorted(casan, key=lambda x: x.get("minuto", "")):
                    w.append(fila_compromiso(x, nombres))
                w.append("")
            if sueltos:
                w.append("> ⚠ %d declaración(es) que no casan con ningún compromiso de esta página: se hicieron sobre "
                         "otra lectura de los compromisos. **No se sabe a qué compromiso se refieren**: antes de "
                         "usarlas, que ella lo confirme.\n" % len(sueltos))
                w.append(cab)
                for x in sorted(sueltos, key=lambda x: x.get("minuto", "")):
                    w.append(fila_compromiso(x, nombres))
                w.append("")
    gl, quitadas = glosario_del_caso(ultimas, paginas_)
    if gl or quitadas:
        w.append("---\n\n## Glosario del caso, según ella\n")
    if gl:
        w.append("Vale en todo el caso **salvo en las líneas de «Salvo en»**, donde ella dijo que ahí sí se dijo "
                 "lo que escribe la transcripción.\n")
        w.append("| La transcripción dice | Se dijo | Estado | Origen | Salvo en | Nota |\n|---|---|---|---|---|---|")
        for e, _orden, sola in sorted(gl.values(), key=lambda v: plano(v[0].get("oye"))):
            w.append(fila(e.get("oye", ""), e.get("dijo", ""),
                          "rechazada" if e.get("estado") == "rechazada" else "aceptada",
                          origen_glosario(e), salvo_en(e, paginas_, sola), nota_glosario(e)))
        w.append("")
    if quitadas:
        w.append("> Estaban en un guardado anterior y no en el último de ese caso (lo más probable: ella las quitó). "
                 "**No se usan:** %s\n" % "; ".join(
                     "«%s» → «%s»" % (celda(e.get("oye")), celda(e.get("dijo")))
                     for _o, e in sorted(quitadas.items())))
    return "\n".join(w) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrega", help="la carpeta de la entrega (la que tiene «Transcripciones»)")
    ap.add_argument("extra", nargs="*", help="declaraciones sueltas (p. ej. descargadas en Descargas)")
    ap.add_argument("--salida", required=True, help="dónde dejar el informe (se crea si no existe)")
    # Mezclados: como dice el uso, los archivos sueltos pueden ir después de
    # --salida (con parse_args, argparse los rechazaba).
    a = ap.parse_intermixed_args(argv)
    if not os.path.isdir(os.path.join(a.entrega, "Transcripciones")):
        falla("%s no parece la carpeta de una entrega: no tiene «Transcripciones»" % a.entrega)
    pags = paginas(a.entrega)
    if not pags:
        falla("no hay páginas de «oír y marcar» con clave en %s" % a.entrega)
    docs = declaraciones(a.entrega, a.extra)
    buenas = [d for d in docs if d.get("clave") in pags]
    descartadas = sorted({os.path.basename(d["_ruta"]) for d in docs if d.get("clave") not in pags})
    if not buenas:
        falla("no hay ninguna declaración de estas páginas en %s%s" % (
            " ni en ".join("«%s»" % c for c in carpetas_de(a.entrega)),
            " (se descartaron %d de otra versión)" % len(descartadas) if descartadas else ""))
    ultimas = lo_ultimo(buenas)
    os.makedirs(a.salida, exist_ok=True)
    sello = datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")
    base = os.path.join(a.salida, "Lo que declaró ella - %s" % sello)
    if os.path.exists(base + ".md") or os.path.exists(base + ".json"):
        falla("ya existe %s: no se sobrescribe" % base)
    with io.open(base + ".md", "w", encoding="utf-8", newline="\n") as f:
        f.write(informe(a.entrega, pags, ultimas, descartadas, docs))
    with io.open(base + ".json", "w", encoding="utf-8", newline="\n") as f:
        json.dump({"formato": "despacho/lo-que-declaro", "recogido": sello, "entrega": os.path.basename(os.path.normpath(a.entrega)),
                   "descartadas": descartadas,
                   "archivos": [{"ruta": d["_ruta"], "carpeta": d["_carpeta"], "a_mano": d["_carpeta"] is None,
                                 "usado": any(d is u for u in ultimas.values())} for d in docs],
                   "documentos": {k: {kk: vv for kk, vv in d.items() if not kk.startswith("_")} for k, d in ultimas.items()}},
                  f, ensure_ascii=False, indent=1)
    print("OK  %s (.md y .json)  -  %d documentos%s" % (os.path.basename(base), len(ultimas),
          "; %d descartados por ser de otra versión" % len(descartadas) if descartadas else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
