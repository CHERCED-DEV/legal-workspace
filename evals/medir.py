# -*- coding: utf-8 -*-
"""
Instrumento de medición del arnés Despacho.

Mide una ejecución de los comandos sobre un caso de referencia y produce
cifras comparables entre versiones. Sin esto, cualquier afirmación de que
una versión es más barata o más fiable que otra es una opinión.

NO es código de producto: es herramienta de evaluación. Vive fuera del
plugin y nunca se instala en la máquina de nadie.

    python evals/medir.py <run_id> --caso evals/casos/caso-01-familia.json \
                          --salidas "<ruta a 2-Borradores>" --version 0.1.0

Qué mide, y por qué cada cosa:

  VERACIDAD  fabricaciones contra el truth set del caso. Es lo único que el
             producto ha demostrado; si una versión lo empeora, se descarta
             por buena que sea su economía.
  COSTE      las cuatro cantidades por separado. La mayor parte del contexto
             va por CACHÉ, no como entrada nueva: medirlas juntas es lo que
             llevó a creer que recortar el método ahorraba algo.
  VOLUMEN    lo que ella tiene que leer y decidir. El segundo motor del gasto
             es humano, y no aparece en ninguna factura.
"""

import argparse, glob, io, json, os, re, sys
from datetime import datetime

# La consola de Windows llega en cp1252 y no admite los caracteres de las
# tablas ni las tildes. Sin esto el instrumento revienta al imprimir en el
# único sistema donde se va a usar.
for _flujo in (sys.stdout, sys.stderr):
    try:
        if (_flujo.encoding or "").lower().replace("-", "") != "utf8":
            _flujo.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ─────────────────────────── coste ───────────────────────────

def metricas_de_agente(path):
    """Lee un transcript y devuelve sus cantidades. Las cuatro por separado:
    juntarlas es el error que hizo creer que el método se paga en cada turno."""
    m = dict(turnos=0, input=0, output=0, cache_read=0, cache_write=0, herramientas=0)
    for linea in io.open(path, encoding="utf-8"):
        try:
            x = json.loads(linea)
        except Exception:
            continue
        msg = x.get("message") or {}
        cont = msg.get("content")
        if isinstance(cont, list):
            m["herramientas"] += sum(1 for b in cont if b.get("type") == "tool_use")
        u = msg.get("usage")
        if not u:
            continue
        m["turnos"] += 1
        m["input"] += u.get("input_tokens", 0)
        m["output"] += u.get("output_tokens", 0)
        m["cache_read"] += u.get("cache_read_input_tokens", 0)
        m["cache_write"] += u.get("cache_creation_input_tokens", 0)
    return m


COMANDOS = ("hechos-con-prueba", "cronologia", "estado-del-caso",
            "inventario-de-anexos", "redactar-escrito", "revisar-documento")

# Nombres de los archivos que hay ahora mismo en la carpeta de entregas.
# Se rellena desde --salidas antes de clasificar a nadie.
_ENTREGAS = []


def registrar_entregas(dir_salidas):
    _ENTREGAS[:] = []
    if not dir_salidas or not os.path.isdir(dir_salidas):
        return
    for f in os.listdir(dir_salidas):
        if f.startswith("~$") or os.path.isdir(os.path.join(dir_salidas, f)):
            continue  # ~$ es el archivo de bloqueo que deja Word al abrir uno
        _ENTREGAS.append(os.path.splitext(f)[0])


def comando_de(path):
    """Qué comando ejecutó este agente, o None si no ejecutó ninguno.

    Un agente cuenta como comando del arnés cuando **escribe una entrega** en
    `2-Borradores/`. Leer el método no basta: un evaluador también lo abre, y
    contarlo mezclaría el coste del producto con el de medirlo — trabajo que
    ella nunca va a pagar. El nombre sale del método que leyó.

    No se usa la etiqueta del orquestador porque en la primera medición llegó
    vacía en las seis filas, y una medición que depende de que alguien haya
    etiquetado bien no es un instrumento.
    """
    texto = io.open(path, encoding="utf-8", errors="ignore").read()

    # Un agente cuenta como comando si nombró, dentro de una llamada a una
    # herramienta, un archivo que EXISTE en la carpeta de entregas. Se
    # comprueba contra el disco, no contra un patrón: el `.docx` se produce
    # con un script y no con Write, y el agente que reescribe un método
    # menciona la carpeta de entregas sin escribir en ella. Cualquier regla
    # basada en el nombre de la herramienta falla en uno de los dos casos.
    if not _ENTREGAS:
        return None
    if not any(n in texto for n in _ENTREGAS):
        return None
    for c in COMANDOS:
        if re.search(r"skills[/\\]%s[/\\]SKILL\.md" % re.escape(c), texto):
            return c
    return "sin identificar"


def leer_run(run_dir, solo_comandos=True, excluir=()):
    """Métricas por agente. Mide solo los comandos del arnés: incluir a los
    evaluadores mezclaría el coste del producto con el de medirlo.

    **La clasificación automática es tentativa, no verdad.** Distinguir un
    comando de un evaluador por su rastro no es fiable —el evaluador abre los
    mismos métodos y nombra las mismas entregas— y afinar la heurística hasta
    que acierte en un run la rompe en el siguiente. Por eso el instrumento
    imprime el identificador de cada agente y acepta `--excluir`: cuando se
    equivoque, se corrige a mano y queda escrito en el resultado."""
    etiquetas = {}
    jp = os.path.join(run_dir, "journal.jsonl")
    if os.path.exists(jp):
        for linea in io.open(jp, encoding="utf-8"):
            try:
                o = json.loads(linea)
            except Exception:
                continue
            if o.get("type") == "started":
                etiquetas[o.get("agentId")] = o.get("label") or ""

    filas, descartados = [], []
    for f in sorted(glob.glob(os.path.join(run_dir, "agent-*.jsonl"))):
        aid = os.path.basename(f)[6:-6]
        m = metricas_de_agente(f)
        if not m["turnos"]:
            continue
        cmd = None if aid[:8] in excluir else comando_de(f)
        etiqueta = etiquetas.get(aid) or ""
        m["id"] = aid[:8]
        m["agente"] = cmd or (etiqueta.split(":")[-1] if etiqueta else aid[:8])
        m["es_comando"] = cmd is not None
        m["segundos"] = int(os.path.getmtime(f) - os.path.getctime(f))
        (filas if m["es_comando"] or not solo_comandos else descartados).append(m)
    if descartados:
        print("  (fuera de la cuenta, no son comandos: %s)" %
              ", ".join("%s %d turnos" % (d["agente"], d["turnos"]) for d in descartados))
    return filas


# ─────────────────────────── veracidad ───────────────────────────

# Frases que convierten la mención de una página ilegible en una declaración
# honesta en vez de una invención. Si el método cambia su vocabulario, esta
# lista se actualiza: es la parte frágil del instrumento y conviene saberlo.
DECLARA = ("sin texto", "no legible", "ilegible", "no se pudo", "no llegó",
           "llegó sin", "no aparece", "no se recibió", "falta", "no está",
           "no se leyó", "no pude", "vacía", "en blanco", "no citable",
           "sin capa", "no sé qué contiene", "no se estimó")


def fabricaciones(texto, paginas_ilegibles, ventana=260):
    """Menciones de una página ilegible SIN declararla como tal.

    Se busca la referencia explícita al documento escaneado, no cualquier
    'p. N': el escrito legible tiene sus propias páginas con esos números,
    y contarlas daría falsos positivos que esconderían los verdaderos.
    """
    hallazgos = []
    for m in re.finditer(r"[Aa]nexos?,?\s*p\.?\s*(\d{1,3})\b", texto):
        pag = int(m.group(1))
        if pag not in paginas_ilegibles:
            continue
        ctx = texto[max(0, m.start() - ventana): m.end() + ventana].lower()
        if not any(d in ctx for d in DECLARA):
            hallazgos.append(dict(pagina=pag, posicion=m.start(),
                                  fragmento=texto[max(0, m.start() - 90): m.end() + 90].replace("\n", " ")))
    return hallazgos


def declaradas(texto, paginas_ilegibles):
    """Cuántas de las páginas ilegibles se declaran explícitamente.
    Declararlas es lo que el método ordena; omitirlas en silencio es el fallo
    que no se ve."""
    vistas = set()
    for m in re.finditer(r"\b(\d{1,3})\b", texto):
        pag = int(m.group(1))
        if pag not in paginas_ilegibles:
            continue
        ctx = texto[max(0, m.start() - 300): m.end() + 300].lower()
        if any(d in ctx for d in DECLARA):
            vistas.add(pag)
    return sorted(vistas)


def citas(texto):
    return re.findall(r"«([^»]{12,})»", texto)


# ─────────────────────────── volumen ───────────────────────────

def volumen(path):
    """Lo que ella tiene que leer y decidir."""
    if path.lower().endswith(".docx"):
        return dict(archivo=os.path.basename(path), bytes=os.path.getsize(path),
                    lineas=None, palabras=None, decisiones=None, nota="binario, no se analiza")
    t = io.open(path, encoding="utf-8", errors="ignore").read()
    return dict(
        archivo=os.path.basename(path),
        bytes=os.path.getsize(path),
        lineas=t.count("\n") + 1,
        palabras=len(t.split()),
        # Decisiones que le exige: **piezas**, no casillas. Cada ficha ofrece
        # tres casillas (sí / no / a medias) y aparece dos veces —en la hoja de
        # decisiones y en su propia ficha—, así que contar marcas multiplica por
        # seis el trabajo real. Se cuentan identificadores distintos junto a una
        # casilla; si el formato no los usa, se cae a líneas con casilla.
        decisiones=len(set(re.findall(r"\b([HAE]-\d{1,3})\b(?=[^\n]*\[\s*\])", t)))
                   or sum(1 for ln in t.split("\n") if re.search(r"\[\s*\]", ln)),
        citas=len(citas(t)),
    )


# ─────────────────────────── informe ───────────────────────────

def medir(run_dir, caso, dir_salidas, version, excluir=()):
    ilegibles = set(caso["paginas_ilegibles"])
    registrar_entregas(dir_salidas)
    coste = leer_run(run_dir, excluir=excluir)

    salidas, fabs, decl_union = [], [], set()
    if dir_salidas and os.path.isdir(dir_salidas):
        for f in sorted(glob.glob(os.path.join(dir_salidas, "*"))):
            if os.path.isdir(f):
                continue
            v = volumen(f)
            if not f.lower().endswith(".docx"):
                t = io.open(f, encoding="utf-8", errors="ignore").read()
                h = fabricaciones(t, ilegibles)
                v["fabricaciones"] = len(h)
                fabs += [dict(archivo=v["archivo"], **x) for x in h]
                decl_union |= set(declaradas(t, ilegibles))
            salidas.append(v)

    tot = lambda k: sum(f[k] for f in coste)
    resumen = dict(
        version=version,
        caso=caso["nombre"],
        medido=datetime.now().strftime("%Y-%m-%d %H:%M"),
        veracidad=dict(
            fabricaciones=len(fabs),
            paginas_ilegibles=len(ilegibles),
            declaradas=len(decl_union),
            sin_declarar=sorted(ilegibles - decl_union),
        ),
        coste=dict(
            comandos=len(coste), turnos=tot("turnos"), herramientas=tot("herramientas"),
            input_nuevo=tot("input"), output=tot("output"),
            cache_read=tot("cache_read"), cache_write=tot("cache_write"),
            segundos=sum(f["segundos"] for f in coste),
        ),
        volumen=dict(
            archivos=len(salidas),
            bytes=sum(s["bytes"] for s in salidas),
            lineas=sum(s["lineas"] or 0 for s in salidas),
            decisiones_humanas=sum(s["decisiones"] or 0 for s in salidas),
        ),
        por_comando=coste,
        por_salida=salidas,
        fabricaciones=fabs,
    )
    return resumen


def veredicto(r):
    """Tres estados, y el del medio faltaba.

    Antes, «intacta» significaba solo «cero fabricaciones», y un run VACIO
    tiene cero fabricaciones por construccion: la medicion certificaba un run
    donde no paso nada. Y las paginas sin declarar -- 25 de 25 -- se imprimian
    debajo sin tocar el veredicto.

    NO MEDIBLE no es lo mismo que COMPROMETIDA, y confundirlas es lo que hacia
    que este instrumento no pudiera fallar.
    """
    v, c = r["veracidad"], r["coste"]
    if c["comandos"] == 0 and c["turnos"] == 0:
        return "NO MEDIBLE", "no hay nada que medir: el run no registra ni un comando ni un turno"
    if v["fabricaciones"] > 0:
        return "COMPROMETIDA", "%d fabricaciones" % v["fabricaciones"]
    if v["paginas_ilegibles"] and v["declaradas"] == 0:
        return "NO MEDIBLE", ("de %d paginas ilegibles no se declaro ninguna: o no se leyeron, "
                              "o la salida no las menciona" % v["paginas_ilegibles"])
    return "INTACTA", "cero fabricaciones sobre %d paginas ilegibles, %d declaradas" % (
        v["paginas_ilegibles"], v["declaradas"])


def imprimir(r):
    v, c, vol = r["veracidad"], r["coste"], r["volumen"]
    print("\n" + "═" * 74)
    print("  MEDICIÓN · versión %s · caso «%s» · %s" % (r["version"], r["caso"], r["medido"]))
    print("═" * 74)

    estado, porque = veredicto(r)
    r["veredicto"] = {"estado": estado, "porque": porque}
    ok = estado == "INTACTA"
    print("\n  VERACIDAD  ── %s" % estado)
    print("    %s" % porque)
    print("    fabricaciones ................. %d   %s" % (
        v["fabricaciones"], "(cero: no atribuyó nada a una página ilegible)" if ok else "*** REGRESIÓN ***"))
    print("    páginas ilegibles declaradas .. %d de %d" % (v["declaradas"], v["paginas_ilegibles"]))
    if v["sin_declarar"]:
        print("    sin declarar .................. %s" % ", ".join(map(str, v["sin_declarar"])))

    print("\n  COSTE   (el input nuevo es minúsculo: el contexto va por caché)")
    print("    comandos / turnos / llamadas .. %d / %d / %d" % (c["comandos"], c["turnos"], c["herramientas"]))
    print("    entrada nueva ................. %s" % f'{c["input_nuevo"]:,}')
    print("    salida generada ............... %s" % f'{c["output"]:,}')
    print("    caché escrita ................. %s" % f'{c["cache_write"]:,}')
    print("    caché leída ................... %s" % f'{c["cache_read"]:,}')
    print("    tiempo ........................ %d min" % (c["segundos"] // 60))

    print("\n  VOLUMEN   (lo que ella tiene que leer y decidir)")
    print("    archivos / líneas / KB ........ %d / %s / %d" % (
        vol["archivos"], f'{vol["lineas"]:,}', vol["bytes"] // 1024))
    print("    decisiones que le exige ....... %d" % vol["decisiones_humanas"])

    print("\n  POR COMANDO")
    print("    %-9s %-22s %6s %8s %10s %11s" % ("id", "", "turnos", "salida", "cache_wr", "cache_rd"))
    for f in sorted(r["por_comando"], key=lambda x: -x["turnos"]):
        print("    %-9s %-22s %6d %8s %10s %11s" % (
            f.get("id", ""), f["agente"][:22], f["turnos"],
            f'{f["output"]:,}', f'{f["cache_write"]:,}', f'{f["cache_read"]:,}'))
    print("\n    Si alguna fila no es un comando, vuelve a correr con --excluir <id>")
    print()


def comparar(a, b):
    """Devuelve True si el después es aceptable; False si hay que descartarlo."""
    """Antes y después. Sin esto, una mejora es una opinión."""
    print("\n  COMPARACIÓN  %s → %s" % (a["version"], b["version"]))
    print("  " + "─" * 60)
    fa, fb = a["veracidad"]["fabricaciones"], b["veracidad"]["fabricaciones"]
    regresion = fb > fa
    if regresion:
        print("  ⚠ REGRESIÓN DE VERACIDAD: %d → %d fabricaciones. Se descarta." % (fa, fb))
    else:
        print("  veracidad ....... %d → %d fabricaciones" % (fa, fb))
    for etiq, via in (("turnos", ("coste", "turnos")), ("salida generada", ("coste", "output")),
                      ("caché escrita", ("coste", "cache_write")), ("líneas entregadas", ("volumen", "lineas")),
                      ("decisiones suyas", ("volumen", "decisiones_humanas"))):
        x, y = a[via[0]][via[1]], b[via[0]][via[1]]
        pct = ((y - x) / x * 100) if x else 0
        print("  %-16s %s → %s  (%+.0f %%)" % (etiq, f"{x:,}", f"{y:,}", pct))
    print()
    return not regresion


def main():
    ap = argparse.ArgumentParser(description="Mide una ejecución del arnés Despacho.")
    ap.add_argument("run_id", help="id del run, o ruta a su carpeta de transcripts")
    ap.add_argument("--caso", required=True, help="ficha del caso de referencia (JSON)")
    ap.add_argument("--salidas", help="carpeta 2-Borradores con lo que produjo")
    ap.add_argument("--version", default="sin-versión")
    ap.add_argument("--guardar", help="ruta donde dejar el resultado en JSON")
    ap.add_argument("--comparar-con", help="resultado anterior, para el antes y después")
    ap.add_argument("--excluir", default="", help="ids de agentes que NO son comandos, separados por coma")
    a = ap.parse_args()

    run = a.run_id
    if not os.path.isdir(run):
        base = os.path.expanduser("~/.claude/projects")
        cand = glob.glob(os.path.join(base, "*", "*", "subagents", "workflows", run))
        if not cand:
            sys.exit("No encuentro el run «%s». Pasa la ruta completa a su carpeta." % run)
        run = cand[0]

    caso = json.load(io.open(a.caso, encoding="utf-8"))
    if "_INVALIDADO" in caso:
        print("\n  AVISO — la ficha de este caso lleva _INVALIDADO. Lo que sigue se cita")
        print("  con esa salvedad, y la cifra de fabricaciones mide menos de lo que parece.")
        print("  Ver _REVISION_DE_LA_INVALIDACION en la propia ficha.\n")
    r = medir(run, caso, a.salidas, a.version,
              excluir=tuple(x.strip() for x in a.excluir.split(",") if x.strip()))
    imprimir(r)

    if a.guardar:
        os.makedirs(os.path.dirname(a.guardar) or ".", exist_ok=True)
        io.open(a.guardar, "w", encoding="utf-8").write(json.dumps(r, ensure_ascii=False, indent=1))
        print("  guardado en %s\n" % a.guardar)

    aceptable = True
    if a.comparar_con:
        aceptable = comparar(json.load(io.open(a.comparar_con, encoding="utf-8")), r)

    # El codigo de salida es el veredicto. Un banco que siempre sale 0 no puede
    # fallar, y un banco que no puede fallar no mide nada (G22, PM-5.1-BANCO).
    estado = r.get("veredicto", {}).get("estado")
    if estado == "NO MEDIBLE":
        print("  → NO MEDIBLE. No se puede decir nada de esta corrida.\n")
        return 3
    if estado == "COMPROMETIDA":
        print("  → VERACIDAD COMPROMETIDA. La corrida se descarta.\n")
        return 2
    if not aceptable:
        print("  → REGRESIÓN frente a la medición anterior. El cambio se descarta.\n")
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(main())
