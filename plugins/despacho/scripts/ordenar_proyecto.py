# -*- coding: utf-8 -*-
"""ordenar_proyecto — llevar un proyecto que ya existe a la forma de ADR-023.

    python ordenar_proyecto.py <proyecto> --plan <plan.json> [--traer <carpeta>] [--cliente]
    python ordenar_proyecto.py --aplicar <plan.json>
    python ordenar_proyecto.py --deshacer <manifiesto.json>

TRES PASOS, Y EL PRIMERO NO TOCA NADA.
  --plan      lee el proyecto y escribe el plan (.json y un .md legible): cada
              movimiento, de donde a donde y por que; las copias identicas que
              encontro; las rutas de entrega.json y de las paginas que habra que
              ajustar; y lo que no sabe donde va (eso se señala y se deja).
  --aplicar   con el plan aprobado por el dueño: mueve (renombra; nunca copia y
              borra, nunca borra), ajusta las rutas y deja un MANIFIESTO con
              cada paso y una copia de cada archivo que edito.
  --deshacer  con el manifiesto: todo vuelve a donde estaba.

LO QUE NO HACE. No borra nada: las copias identicas se apartan a _anteriores,
no se eliminan. No toca «1-Documentos recibidos» ni lo que ella tenga en
«3-Para presentar» que no sea una entrega de la maquina. No arregla rutas que
ya estaban rotas antes de ordenar: las señala, porque no sabe a donde
apuntaban. Se detiene si un destino ya existe o si un archivo esta abierto, y
entonces deshace lo que habia movido.
"""
import argparse, datetime, hashlib, io, json, os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estructura as E  # noqa: E402

FORMATO_PLAN = "despacho/plan-de-orden"
FORMATO_MANIFIESTO = "despacho/manifiesto-de-orden"
VERSION_VIEJA = re.compile(r"^(previa|vigente|anterior)(?: (\d+))? - (\d{4}-\d{2}-\d{2})(?: \((.+)\))?$", re.I)
COMPROMISOS_VIEJO = re.compile(r"^Compromisos senalados(?: - (\d{4}-\d{2}-\d{2}) \((.+)\))?$")
# La ruta acaba donde acaba la comilla: «grabacion 4.m4a.mp4» no es «grabacion 4.m4a»
# (asi se dio por rota una ruta que funcionaba; 2026-09-23).
REF = re.compile(r"(?:\.\./)+[^\"'<>\n]+?\.(?:mp4|m4a|mp3|wav|ogg|html|json|md|docx|pdf|jpe?g|png)(?=[\"'<>)\]]|$)")
TEXTO = (".html", ".md", ".json", ".txt")


# Rutas largas. En Windows, sin el prefijo «\\?\», una ruta de mas de 259
# caracteres no se abre, y os.walk se salta esa carpeta SIN AVISAR: el plan
# habria dicho «esto es todo» sin haberlo mirado todo (2026-09-23: en un
# proyecto real ya habia un archivo de 264). Todo pasa por aqui.
PREFIJO = "\\\\?\\"
MAX_RUTA = 259


def L(p):
    if os.name != "nt":
        return p
    p = os.path.abspath(p)
    return p if p.startswith(PREFIJO) else PREFIJO + p


def sin(p):
    return p[len(PREFIJO):] if p.startswith(PREFIJO) else p


def andar(p, **kw):
    if not os.path.isdir(L(p)):
        return
    for r, ds, fs in os.walk(L(p), onerror=_no_se_pudo, **kw):
        yield sin(r), ds, fs


def _no_se_pudo(e):
    falla("no se pudo leer «%s» (%s): el plan no seria completo" % (sin(getattr(e, "filename", "") or ""), e))


listar = lambda p: os.listdir(L(p))              # noqa: E731
es_dir = lambda p: os.path.isdir(L(p))           # noqa: E731
es_arch = lambda p: os.path.isfile(L(p))         # noqa: E731
existe = lambda p: os.path.exists(L(p))          # noqa: E731
mtime = lambda p: os.path.getmtime(L(p))         # noqa: E731
renombrar = lambda a, b: os.rename(L(a), L(b))   # noqa: E731
crear = lambda p, **kw: os.makedirs(L(p), **kw)  # noqa: E731
quitar = lambda p: os.rmdir(L(p))                # noqa: E731
copiar = lambda a, b: shutil.copy2(L(a), L(b))   # noqa: E731


def falla(msg):
    sys.stderr.write("\nDETENIDO: " + msg + "\n")
    raise SystemExit(2)


def rel(p, base):
    return os.path.relpath(p, base).replace("\\", "/")


def md5(p):
    h = hashlib.md5()
    with open(L(p), "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def fecha_de_archivos(carpeta):
    """La fecha mas frecuente en los nombres; si no hay, la de modificacion mas reciente."""
    cuenta = {}
    ultima = 0
    for r, _, fs in andar(carpeta):
        for f in fs:
            m = E.FECHA.search(f)
            if m:
                cuenta[m.group(1)] = cuenta.get(m.group(1), 0) + 1
            ultima = max(ultima, mtime(os.path.join(r, f)))
    if cuenta:
        return max(cuenta, key=lambda k: (cuenta[k], k))
    return datetime.date.fromtimestamp(ultima).isoformat() if ultima else datetime.date.today().isoformat()


def leer_config(P):
    for c in (os.path.join(P, "_fuentes (no enviar)", "entrega.json"), E.en(P, E.FUENTES_DE_LA_ENTREGA + "/entrega.json")):
        if es_arch(c):
            try:
                with io.open(c, encoding="utf-8") as f:
                    return c, json.load(f)
            except ValueError:
                return c, None
    return None, None


# --------------------------------------------------------------------- plan
def planear(P, traer=(), cliente=False):
    P = os.path.abspath(P)
    if not E.es_proyecto(P):
        falla("%s no parece un proyecto: le falta «%s» o «%s»" % (P, E.RECIBIDOS, E.BORRADORES))
    mov, sen = [], []
    usados = set()

    def mover(de, a, por, raiz=P):
        de_abs = de if os.path.isabs(de) else os.path.join(raiz, *de.split("/"))
        a_rel = a
        if a_rel in usados or existe(E.en(P, a_rel)):
            falla("el destino «%s» ya existe o se usa dos veces (%s)" % (a_rel, de))
        usados.add(a_rel)
        mov.append({"de": de_abs, "a": a_rel, "por": por, "carpeta": es_dir(de_abs)})

    B = E.en(P, E.BORRADORES)
    ruta_config, config = leer_config(P)

    # 1. La raiz del proyecto: cuatro elementos y ni uno mas.
    for n in sorted(listar(P)):
        if n in E.RAIZ_DEL_PROYECTO:
            continue
        if n == "_fuentes (no enviar)":
            mover(n, E.FUENTES_DE_LA_ENTREGA, "Las fuentes de la entrega van con las entregas (ADR-023 §2.2)")
        else:
            sen.append("En la raíz del proyecto está «%s», que no es de la forma: no sé dónde va y se deja." % n)
    if not es_arch(os.path.join(P, E.ESTADO)):
        sen.append("Falta «%s»: se escribe con estado-del-caso después de ordenar." % E.ESTADO)

    # 2. Las entregas de la maquina salen de «3-Para presentar».
    T = E.en(P, E.PRESENTAR)
    entregas = sorted(n for n in (listar(T) if es_dir(T) else []) if n.startswith("ENTREGA - "))
    bases = sorted({n[:-4] if n.endswith(".zip") else n for n in entregas})
    actual = (config or {}).get("nombre") if config else (bases[-1] if bases else None)
    if config and actual not in bases and bases:
        sen.append("entrega.json nombra «%s», que no está en «%s»." % (actual, E.PRESENTAR))
    for n in entregas:
        base = n[:-4] if n.endswith(".zip") else n
        destino = E.ENTREGAS if base == actual else E.ENTREGAS_ANTERIORES
        mover(E.PRESENTAR + "/" + n, destino + "/" + n,
              "Las entregas de la máquina viven en 2-Borradores (ADR-023 §2.1)"
              + ("" if base == actual else "; esta está sustituida por «%s»" % actual))

    # 3. El trabajo de maquina regenerable (.trabajo): aparte, y se puede borrar.
    for r, ds, _ in andar(B):
        if ".trabajo" in ds:
            origen = os.path.join(r, ".trabajo")
            nombre = rel(r, B).replace("/", " - ")
            mover(origen, E.INTERMEDIOS + "/" + nombre, "Archivos de trabajo regenerables (ADR-023 §1)")
            ds.remove(".trabajo")

    # 4. Versiones de transcripciones y resumenes: «AAAA-MM-DD - que cambio».
    for tipo in (E.TRANSCRIPCIONES, E.RESUMENES):
        D = E.en(P, tipo)
        if not es_dir(D):
            continue
        sueltos = [n for n in listar(D) if es_arch(os.path.join(D, n))]
        if sueltos:
            fecha = fecha_de_archivos(D if not es_dir(os.path.join(D, "datos")) else D)
            destino = tipo + "/" + E.version(fecha)
            for n in sorted(sueltos):
                mover(tipo + "/" + n, destino + "/" + n, "Una versión suelta va en su carpeta con fecha (ADR-023 §3)")
            if es_dir(os.path.join(D, "datos")):
                mover(tipo + "/datos", destino + "/datos", "Los datos de esa versión, con ella")
        viejas = []
        for n in listar(D):
            m = VERSION_VIEJA.match(n)
            if m and es_dir(os.path.join(D, n)):
                viejas.append((m.group(3), 0 if m.group(1).lower() != "vigente" else 1, int(m.group(2) or 0), n, m))
        viejas.sort()
        for orden, (fecha, _, _, n, m) in enumerate(viejas, 1):
            que = m.group(4) or "lectura %d" % orden
            contenido = [x for x in listar(os.path.join(D, n)) if x != ".trabajo"]
            vacia = all(es_dir(os.path.join(D, n, x)) and not listar(os.path.join(D, n, x)) for x in contenido)
            if vacia:
                sen.append("«%s/%s» solo tiene archivos de trabajo o carpetas vacías: se queda vacía y se quita." % (tipo, n))
                continue
            mover(tipo + "/" + n, tipo + "/" + E.version(fecha, que),
                  "Una sola manera de nombrar versiones, sin «vigente» ni «previa» (ADR-023 §3)")

    # 5. Compromisos.
    for n in sorted(listar(B)):
        m = COMPROMISOS_VIEJO.match(n)
        if m and es_dir(os.path.join(B, n)):
            fecha = m.group(1) or fecha_de_archivos(os.path.join(B, n))
            mover(E.BORRADORES + "/" + n, E.COMPROMISOS + "/" + E.version(fecha, m.group(2) or ""),
                  "Los compromisos, en su carpeta con fecha (ADR-023 §1)")

    # 6. Piezas sueltas en 2-Borradores que tienen carpeta propia.
    for n in sorted(listar(B)):
        p = os.path.join(B, n)
        if es_arch(p):
            if re.match(r"^(Acta - |Revision de rigor|Revisión de rigor)", n):
                mover(E.BORRADORES + "/" + n, E.ACTAS + "/" + n, "Las actas y lo que las acompaña, en Actas (ADR-023 §1)")
            elif n.startswith("Glosario"):
                mover(E.BORRADORES + "/" + n, E.GLOSARIO + "/" + n, "El glosario, en su carpeta (ADR-023 §1)")
            elif n.endswith(" - oir y nombrar voces.html"):
                mover(E.BORRADORES + "/" + n, E.VOCES + "/" + n, "Lo de las voces, en Voces (ADR-023 §1)")
        elif n == "Forma del acta anterior":
            mover(E.BORRADORES + "/" + n, E.ACTAS + "/" + n, "La forma del acta modelo, con las actas")
        elif n == "Verdad de referencia":
            mover(E.BORRADORES + "/" + n, E.VOCES + "/" + n, "La verdad de referencia de las voces, con las voces")
        elif n == "_versiones anteriores":
            mover(E.BORRADORES + "/" + n, E.ANTERIORES + "/versiones anteriores", "Lo sustituido, en _anteriores (ADR-023 §3)")

    # 7. Copias identicas sueltas en 2-Borradores de algo que ya esta en su carpeta.
    huellas = {}
    for tipo in (E.TRANSCRIPCIONES, E.RESUMENES):
        for r, ds, fs in andar(E.en(P, tipo)):
            ds[:] = [d for d in ds if d != ".trabajo"]
            for f in fs:
                huellas.setdefault(md5(os.path.join(r, f)), rel(os.path.join(r, f), P))
    ya = {m["de"] for m in mov}
    for n in sorted(listar(B)):
        p = os.path.join(B, n)
        if es_arch(p) and p not in ya and n.lower().endswith((".md", ".docx", ".html", ".txt")):
            h = md5(p)
            if h in huellas:
                mover(E.BORRADORES + "/" + n, E.ANTERIORES + "/copias identicas/" + n,
                      "Copia idéntica de «%s»: se aparta, no se borra (ADR-023 §3)" % huellas[h])

    # 8. Lo que se trae de fuera del proyecto (p. ej. un _Respaldo en la raiz de
    #    Despacho), repartido por lo que es: una entrega vieja con las entregas,
    #    el trabajo de maquina con los intermedios, y lo demas a _anteriores.
    #    Meterlo entero en _anteriores dejaba rutas de mas de 300 caracteres.
    traidas = []
    for t in traer or ():
        t = os.path.abspath(t)
        if not es_dir(t):
            falla("no existe «%s»" % t)
        if os.path.commonpath([t, P]) == P:
            falla("«%s» ya está dentro del proyecto" % t)
        traidas.append(t)
        origen = os.path.basename(t).strip("_ ") or "traido"
        for r, ds, fs in andar(t):
            for d in list(ds):
                q = os.path.join(r, d)
                if d.startswith("ENTREGA - "):
                    mover(q, E.ENTREGAS_ANTERIORES + "/" + d, "Una entrega sustituida que estaba en «%s»" % rel(q, os.path.dirname(t)))
                    ds.remove(d)
                elif d in (".trabajo", "_generado"):
                    mover(q, E.INTERMEDIOS + "/" + origen + " - " + rel(r, t).replace("/", " - ").replace(".", "raiz"),
                          "Trabajo de máquina regenerable que estaba en «%s»" % rel(q, os.path.dirname(t)))
                    ds.remove(d)
            for f in fs:
                q = os.path.join(r, f)
                if f.startswith("ENTREGA - ") and f.endswith(".zip"):
                    mover(q, E.ENTREGAS_ANTERIORES + "/" + f, "Una entrega sustituida que estaba en «%s»" % rel(q, os.path.dirname(t)))
                else:
                    mover(q, E.ANTERIORES + "/" + origen + "/" + rel(q, t), "Estaba en «%s», fuera del proyecto" % rel(q, os.path.dirname(t)))

    # 9. Nivel de cliente: el membrete a «Papelería de la oficina», y las copias
    #    identicas sueltas de algo que esta en este proyecto.
    if cliente:
        C = os.path.dirname(P)
        viejo = os.path.join(C, "_formato de actas")
        if es_dir(viejo):
            mov.append({"de": viejo, "a": "../" + E.PAPELERIA + "/formato de actas",
                        "por": "Los formatos propios de la oficina, en su papelería (ADR-023 §1)", "carpeta": True})
        propios = {}
        for r, ds, fs in andar(P):
            ds[:] = [d for d in ds if d != ".trabajo"]
            for f in fs:
                if f.lower().endswith((".pdf", ".docx", ".doc")):
                    propios.setdefault(md5(os.path.join(r, f)), rel(os.path.join(r, f), P))
        for n in sorted(listar(C)):
            p = os.path.join(C, n)
            if es_arch(p):
                h = md5(p)
                if h in propios:
                    mover(p, E.ANTERIORES + "/copias identicas/" + n,
                          "Copia idéntica de «%s», suelta al nivel del cliente" % propios[h])
                else:
                    sen.append("Al nivel del cliente está «%s», que no es de ningún proyecto: se deja." % n)

    # Rutas que ya son largas, y las que lo serian despues de mover.
    largas_hoy = []
    for r, ds, fs in andar(P):
        for f in fs:
            q = os.path.join(r, f)
            if len(q) > MAX_RUTA:
                largas_hoy.append((len(q), rel(q, P)))
    for n, q in sorted(largas_hoy, reverse=True)[:10]:
        sen.append("Ya hoy la ruta de «%s» mide %d caracteres (más de %d): Word y el Explorador pueden no abrirla." % (q, n, MAX_RUTA))
    for m in mov:
        destino = os.path.normpath(os.path.join(P, *m["a"].split("/")))
        if m["carpeta"]:
            for r, ds, fs in andar(m["de"]):
                for f in fs:
                    q = os.path.join(destino, os.path.relpath(os.path.join(r, f), m["de"]))
                    if len(q) > MAX_RUTA:
                        sen.append("Después de mover, «%s» mediría %d caracteres (más de %d)." % (rel(q, P), len(q), MAX_RUTA))
        elif len(destino) > MAX_RUTA:
            sen.append("Después de mover, «%s» mediría %d caracteres (más de %d)." % (m["a"], len(destino), MAX_RUTA))

    # 10. Rutas que habra que ajustar.
    mapa = [(m["de"], os.path.normpath(E.en(P, m["a"]) if not m["a"].startswith("../") else os.path.join(P, *m["a"].split("/"))))
            for m in mov]
    rutas = ajustes_de_rutas(P, mapa, ruta_config, config, sen)
    return {"formato": FORMATO_PLAN, "proyecto": P, "fecha": datetime.datetime.now().isoformat(timespec="seconds"),
            "movimientos": mov, "rutas": rutas, "senalados": sen, "traidas": traidas}


def nuevo_de(p, mapa):
    """Donde queda `p` (absoluta) tras los movimientos."""
    p = os.path.normpath(p)
    for de, a in mapa:
        de = os.path.normpath(de)
        if p == de:
            return a
        if p.startswith(de + os.sep):
            return os.path.join(a, p[len(de) + 1:])
    return p


def ajustes_de_rutas(P, mapa, ruta_config, config, sen):
    out = []
    # entrega.json: sus rutas son relativas al proyecto.
    if config and ruta_config:
        cambios = []
        # Una sola pasada, la ruta mas larga primero, y solo si detras viene «/»
        # o el final: «Compromisos senalados» no es el principio de
        # «Compromisos senalados - (con detalle)».
        pares = []
        for de, a in mapa:
            dr = os.path.relpath(de, P).replace("\\", "/")
            if not dr.startswith(".."):
                pares.append((dr, os.path.relpath(a, P).replace("\\", "/")))
        pares.sort(key=lambda x: -len(x[0]))
        patron = re.compile(r"(?<![\w/])(" + "|".join(re.escape(d) for d, _ in pares) + r")(?=/|$)") if pares else None
        destino = dict(pares)

        def recorrer(x, camino):
            if isinstance(x, dict):
                for k, v in x.items():
                    recorrer(v, camino + [k])
            elif isinstance(x, list):
                for i, v in enumerate(x):
                    recorrer(v, camino + [i])
            elif isinstance(x, str) and camino and camino[0] not in ("raiz", "nombre") and patron:
                nuevo = patron.sub(lambda m: destino[m.group(1)], x)
                if nuevo != x:
                    cambios.append({"clave": camino, "antes": x, "despues": nuevo})
        recorrer(config, [])
        if any(os.path.normpath(de) == os.path.normpath(os.path.join(P, E.PRESENTAR, config.get("nombre", ""))) for de, _ in mapa):
            if config.get("salida") != E.ENTREGAS:
                cambios.append({"clave": ["salida"], "antes": config.get("salida"), "despues": E.ENTREGAS})
        if cambios:
            out.append({"archivo": rel(nuevo_de(ruta_config, mapa), P), "tipo": "entrega.json", "cambios": cambios})

    # Paginas y textos con rutas relativas («../…»): se recalculan si hoy
    # resuelven. Las que ya estaban rotas se señalan y se dejan.
    for r, ds, fs in andar(P):
        ds[:] = [d for d in ds if d != ".trabajo"]
        for f in fs:
            if not f.lower().endswith(".html"):
                continue
            viejo = os.path.join(r, f)
            nuevo = nuevo_de(viejo, mapa)
            try:
                with io.open(L(viejo), encoding="utf-8") as fh:
                    t = fh.read()
            except (UnicodeDecodeError, OSError):
                continue
            cambios, rotas = [], []
            for ref in sorted(set(REF.findall(t))):
                destino = os.path.normpath(os.path.join(os.path.dirname(viejo), ref))
                if not existe(destino):
                    rotas.append(ref)
                    continue
                nuevo_destino = nuevo_de(destino, mapa)
                nueva = os.path.relpath(nuevo_destino, os.path.dirname(nuevo)).replace("\\", "/")
                if nueva != ref:
                    cambios.append({"antes": ref, "despues": nueva})
            if cambios:
                out.append({"archivo": rel(nuevo, P), "tipo": "pagina", "cambios": cambios})
            if rotas:
                sen.append("«%s» ya tenía rutas rotas antes de ordenar (%s): se dejan como están." % (rel(viejo, P), "; ".join(rotas[:3])))
    return out


def plan_md(plan):
    w = ["# Plan para ordenar «%s»\n" % os.path.basename(plan["proyecto"]),
         "**Qué es:** lo que `ordenar_proyecto.py --aplicar` haría. **Todavía no se ha movido nada.** "
         "Nada se borra; todo se puede deshacer con el manifiesto que deja al aplicar. Forma: ADR-023.\n",
         "## Movimientos (%d)\n" % len(plan["movimientos"]), "| De | A | Por qué |", "|---|---|---|"]
    for m in plan["movimientos"]:
        de = rel(m["de"], plan["proyecto"]) if not os.path.relpath(m["de"], plan["proyecto"]).startswith("..") else m["de"]
        w.append("| `%s`%s | `%s` | %s |" % (de, "/" if m["carpeta"] else "", m["a"], m["por"]))
    w.append("\n## Rutas que se ajustan\n")
    for r in plan["rutas"]:
        w.append("- `%s` (%s): %d cambio(s)" % (r["archivo"], r["tipo"], len(r["cambios"])))
        for c in r["cambios"][:6]:
            w.append("  - «%s» → «%s»" % (c["antes"], c["despues"]))
    if not plan["rutas"]:
        w.append("Ninguna.")
    w.append("\n## Señalado, sin tocar\n")
    w.extend("- " + s for s in plan["senalados"]) if plan["senalados"] else w.append("Nada.")
    return "\n".join(w) + "\n"


# ------------------------------------------------------------------ aplicar
def aplicar(ruta_plan):
    with io.open(ruta_plan, encoding="utf-8") as f:
        plan = json.load(f)
    if plan.get("formato") != FORMATO_PLAN:
        falla("%s no es un plan de ordenar_proyecto" % ruta_plan)
    P = plan["proyecto"]
    sello = datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")
    dest = lambda a: os.path.normpath(os.path.join(P, *a.split("/")))  # noqa: E731
    for m in plan["movimientos"]:
        if not existe(m["de"]):
            falla("ya no existe «%s»: el proyecto cambió desde el plan; hágalo otra vez" % m["de"])
        if existe(dest(m["a"])):
            falla("ya existe «%s»" % m["a"])
    copias = E.en(P, E.ANTERIORES + "/ordenado - " + sello + "/antes de ajustar")
    hechos = []
    try:
        for m in plan["movimientos"]:
            d = dest(m["a"])
            creadas = []
            padre = os.path.dirname(d)
            while not es_dir(padre):
                creadas.append(padre)
                padre = os.path.dirname(padre)
            crear(os.path.dirname(d), exist_ok=True)
            renombrar(m["de"], d)
            hechos.append({"de": m["de"], "a": d, "creadas": creadas[::-1]})
        editados = []
        for r in plan["rutas"]:
            p = dest(r["archivo"])
            with io.open(L(p), encoding="utf-8", newline="") as f:
                t = f.read()
            copia = os.path.join(copias, *r["archivo"].split("/"))
            crear(os.path.dirname(copia), exist_ok=True)
            copiar(p, copia)
            if r["tipo"] == "entrega.json":
                d = json.loads(t)
                for c in r["cambios"]:
                    x = d
                    for k in c["clave"][:-1]:
                        x = x[k]
                    x[c["clave"][-1]] = c["despues"]
                t2 = json.dumps(d, ensure_ascii=False, indent=1) + "\n"
            else:
                t2 = t
                for c in r["cambios"]:
                    t2 = t2.replace(c["antes"], c["despues"])
            with io.open(L(p), "w", encoding="utf-8", newline="") as f:
                f.write(t2)
            editados.append({"archivo": p, "copia": copia})
    except OSError as e:
        for h in reversed(hechos):
            renombrar(h["a"], h["de"])
            for c in reversed(h["creadas"]):
                try:
                    quitar(c)
                except OSError:
                    pass
        falla("no se pudo mover (%s). Se deshizo lo que se había movido; ¿hay un archivo abierto?" % e)
    vacias = quitar_vacias(P, [os.path.dirname(h["de"]) for h in hechos])
    # Lo traido de fuera queda vacio: se quitan sus carpetas vacias (y se
    # apuntan, para deshacer).
    for t in plan.get("traidas", []):
        for r, ds, fs in sorted(andar(t, topdown=False), key=lambda x: len(x[0]), reverse=True):
            if es_dir(r) and not listar(r):
                quitar(r)
                vacias.append(r)
    man = {"formato": FORMATO_MANIFIESTO, "proyecto": P, "plan": os.path.abspath(ruta_plan), "fecha": sello,
           "movimientos": hechos, "editados": editados, "vacias_quitadas": vacias}
    ruta_man = E.en(P, E.ANTERIORES + "/ordenado - " + sello + "/manifiesto.json")
    crear(os.path.dirname(ruta_man), exist_ok=True)
    with io.open(ruta_man, "w", encoding="utf-8", newline="\n") as f:
        json.dump(man, f, ensure_ascii=False, indent=1)
    print("OK  %d movimientos, %d archivos ajustados, %d carpetas vacías quitadas.\nManifiesto: %s"
          % (len(hechos), len(editados), len(vacias), ruta_man))
    return ruta_man


def quitar_vacias(P, candidatas):
    """Quita las carpetas que quedaron vacias al mover. Nunca las de la forma
    del proyecto: «3-Para presentar» se quedo vacia al sacar las entregas y se
    quito, el 2026-09-23; es de ella y tiene que estar aunque este vacia."""
    fijas = {os.path.normpath(os.path.join(P, n)) for n in E.RAIZ_DEL_PROYECTO} | {os.path.normpath(P)}
    quitadas = []
    for c in sorted(set(candidatas), key=len, reverse=True):
        while (os.path.normpath(c).startswith(os.path.normpath(P) + os.sep) and os.path.normpath(c) not in fijas
               and es_dir(c) and not listar(c)):
            quitar(c)
            quitadas.append(c)
            c = os.path.dirname(c)
    # Carpetas que quedaron con solo carpetas vacias dentro (p. ej. un «datos» vacio).
    for r, ds, fs in sorted(andar(P, topdown=False), key=lambda x: len(x[0]), reverse=True):
        if r != P and os.path.normpath(r) not in fijas and not listar(r) and any(os.path.normpath(r).startswith(os.path.normpath(c) + os.sep) or r == c for c in candidatas):
            quitar(r)
            quitadas.append(r)
    return quitadas


def deshacer(ruta_man):
    with io.open(ruta_man, encoding="utf-8") as f:
        man = json.load(f)
    if man.get("formato") != FORMATO_MANIFIESTO:
        falla("%s no es un manifiesto de ordenar_proyecto" % ruta_man)
    for c in reversed(man.get("vacias_quitadas", [])):
        crear(c, exist_ok=True)
    for e in man["editados"]:
        copiar(e["copia"], e["archivo"])
    for h in reversed(man["movimientos"]):
        if existe(h["de"]):
            falla("ya existe «%s»: no se puede devolver" % h["de"])
        crear(os.path.dirname(h["de"]), exist_ok=True)
        renombrar(h["a"], h["de"])
        for c in reversed(h["creadas"]):
            try:
                quitar(c)
            except OSError:
                pass
    print("OK  deshecho: %d movimientos devueltos, %d archivos restaurados." % (len(man["movimientos"]), len(man["editados"])))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("proyecto", nargs="?")
    ap.add_argument("--plan", help="dónde escribir el plan (.json; al lado va el .md)")
    ap.add_argument("--traer", action="append", default=[], help="carpeta de fuera del proyecto que es suya")
    ap.add_argument("--cliente", action="store_true", help="ordenar también lo del nivel del cliente")
    ap.add_argument("--aplicar", help="un plan ya aprobado")
    ap.add_argument("--deshacer", help="el manifiesto de una aplicación")
    a = ap.parse_args(argv)
    if a.aplicar:
        aplicar(a.aplicar)
    elif a.deshacer:
        deshacer(a.deshacer)
    elif a.proyecto and a.plan:
        if existe(a.plan):
            falla("ya existe %s: no se sobrescribe" % a.plan)
        plan = planear(a.proyecto, a.traer, a.cliente)
        crear(os.path.dirname(os.path.abspath(a.plan)), exist_ok=True)
        with io.open(a.plan, "w", encoding="utf-8", newline="\n") as f:
            json.dump(plan, f, ensure_ascii=False, indent=1)
        with io.open(os.path.splitext(a.plan)[0] + ".md", "w", encoding="utf-8", newline="\n") as f:
            f.write(plan_md(plan))
        print("OK  plan: %d movimientos, %d archivos con rutas que ajustar, %d cosas señaladas.\n%s"
              % (len(plan["movimientos"]), len(plan["rutas"]), len(plan["senalados"]), os.path.splitext(a.plan)[0] + ".md"))
    else:
        ap.error("diga <proyecto> --plan, o --aplicar, o --deshacer")
    return 0


if __name__ == "__main__":
    sys.exit(main())
