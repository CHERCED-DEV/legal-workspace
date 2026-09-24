# -*- coding: utf-8 -*-
"""
md2html — la superficie de trabajo (ADR-020).

    python md2html.py entrada.md salida.html [--datos datos.json] [--audio audio.mp4]

Produce una pagina HTML **autocontenida y sin una sola peticion de red**: el estilo
y el comportamiento van dentro del archivo, asi que se puede mover, copiar o enviar
a un colega y sigue funcionando.

Con `--datos` (el JSON que deja transcribir_audio.py) la pagina es interactiva:
cada marca de tiempo reproduce ese punto de la grabacion, y ella puede marcar lo
que ya comprobo. Sin `--datos` produce una pagina legible sin reproductor.

Lo que este programa NO hace:
  · No edita el contenido. Todo sale del Markdown; si algo esta mal, esta mal alli.
  · No sustituye al .docx, que sigue siendo el entregable externo (ADR-014).
  · No es fuente de una cita: la coordenada sigue siendo la del original.

La plantilla se compila aparte, en tools/pagina-despacho, y viaja YA COMPILADA.
**Esta maquina no necesita Node para nada.**
"""
import argparse, hashlib, html, io, json, os, re, sys, unicodedata, urllib.parse

AQUI = os.path.dirname(os.path.abspath(__file__))
PLANTILLA = os.path.join(AQUI, "plantilla", "pagina.html")
VERSION = "0.1.0"


# ----------------------------------------------------------------- markdown
def _linea(t):
    """Negrita, cursiva, codigo y enlaces. El texto se escapa siempre primero."""
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
               r'<a href="\2" target="_blank" rel="noreferrer noopener">\1</a>', t)
    t = re.sub(r"\[([^\]]+)\]\(&lt;([^&]+)&gt;\)", _enlace_local, t)
    return t


def _enlace_local(m):
    """Enlace a otro archivo del mismo paquete: [texto](<ruta relativa>).

    Los que llevan #t= abren la pagina de esa grabacion en una pestana CON
    NOMBRE, la misma para todos los enlaces a esa grabacion: pulsar diez minutos
    distintos no abre diez pestanas que se pisarian las marcas unas a otras."""
    texto, ruta = m.group(1), html.unescape(m.group(2))
    href = urllib.parse.quote(ruta, safe="/#=:.-_~()")
    destino = ""
    if "#t=" in ruta:
        base = ruta.split("#", 1)[0]
        destino = ' target="%s"' % ("rec-" + re.sub(r"[^A-Za-z0-9]+", "-", base).strip("-"))
    return '<a href="%s"%s>%s</a>' % (html.escape(href, quote=True), destino, texto)


def _fila(l):
    return [c.strip() for c in l.strip().strip("|").split("|")]


def md_a_html(md):
    out, lineas, i = [], md.split("\n"), 0
    lista = None

    def cerrar():
        nonlocal lista
        if lista:
            out.append(f"</{lista}>")
            lista = None

    while i < len(lineas):
        l = lineas[i]
        s = l.strip()

        if s.startswith("```"):
            cerrar()
            i += 1
            buf = []
            while i < len(lineas) and not lineas[i].strip().startswith("```"):
                buf.append(html.escape(lineas[i]))
                i += 1
            out.append("<pre>" + "\n".join(buf) + "</pre>")
            i += 1
            continue

        if not s:
            cerrar()
            i += 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            cerrar()
            n = len(m.group(1))
            out.append(f"<h{n}>{_linea(m.group(2))}</h{n}>")
            i += 1
            continue

        if re.match(r"^(\*{3,}|-{3,}|_{3,})$", s):
            cerrar(); out.append("<hr>"); i += 1; continue

        if s.startswith("|") and i + 1 < len(lineas) and re.match(r"^\|[\s:|-]+\|$", lineas[i + 1].strip()):
            cerrar()
            cab = _fila(s)
            i += 2
            filas = []
            while i < len(lineas) and lineas[i].strip().startswith("|"):
                filas.append(_fila(lineas[i]))
                i += 1
            th = "".join(f"<th>{_linea(c)}</th>" for c in cab)
            cuerpo = "".join("<tr>" + "".join(f"<td>{_linea(c)}</td>" for c in f) + "</tr>" for f in filas)
            out.append(f"<table><thead><tr>{th}</tr></thead><tbody>{cuerpo}</tbody></table>")
            continue

        if s.startswith("> "):
            cerrar()
            buf = []
            while i < len(lineas) and lineas[i].strip().startswith(">"):
                buf.append(lineas[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote>" + " ".join(_linea(b) for b in buf if b) + "</blockquote>")
            continue

        m = re.match(r"^[-*·]\s+(.*)$", s)
        if m:
            if lista != "ul":
                cerrar(); out.append("<ul>"); lista = "ul"
            out.append(f"<li>{_linea(m.group(1))}</li>")
            i += 1
            continue

        m = re.match(r"^\d+\.\s+(.*)$", s)
        if m:
            if lista != "ol":
                cerrar(); out.append("<ol>"); lista = "ol"
            out.append(f"<li>{_linea(m.group(1))}</li>")
            i += 1
            continue

        cerrar()
        out.append(f"<p>{_linea(s)}</p>")
        i += 1

    cerrar()
    return "\n".join(out)


# ---------------------------------------------------------------- segmentos
def hms(s):
    s = max(0, int(float(s or 0)))
    return "%02d:%02d:%02d" % (s // 3600, (s % 3600) // 60, s % 60)


# El riesgo NO es un porcentaje. Un numero crudo como «37 %» no le dice a nadie
# que hacer; y una cifra de dinero dudosa y una muletilla dudosa no son el mismo
# problema aunque el modelo les de la misma confianza.
_ALTO = ("las pasadas no coinciden", "las dos pasadas difieren", "posible repeticion")
_BAJO = ("puede no ser habla", "voz dudosa", "sin voz asignada")

# Lo que ella LEE. La clasificacion de arriba sigue usando los nombres internos.
_VISIBLE = {
    "las pasadas no coinciden": "las lecturas automáticas no coinciden",
    "las dos pasadas difieren": "las lecturas automáticas no coinciden",
    "decodificacion forzada": "lectura forzada: la máquina pudo inventar texto aquí",
    "posible repeticion": "posible repetición",
}
_FUENTE = {
    "mezcla_f16": "Lectura de los dos canales mezclados",
    "der_int8": "Lectura del canal derecho",
    "izq_int8": "Lectura del canal izquierdo",
    "crudo_int8": "Lectura del audio sin limpiar",
}


# De mas a menos grave. Es una ELECCION, no una medida, y por eso se declara
# aqui en vez de quedar repartida por el codigo.
_ORDEN_MOTIVOS = (
    "decodificacion forzada",      # la maquina pudo inventar texto: lo peor
    "posible repeticion",
    "sin voz asignada",            # no se sabe quien habla
    "voz dudosa",
    "puede no ser habla",
    "confianza baja",
    "las pasadas no coinciden",    # casi siempre ya dicho por el desplegable
    "palabra dudosa",              # casi siempre ya dicho por el subrayado
)


def visible(motivo):
    return _VISIBLE.get(motivo, motivo)


def fuente_visible(k):
    return _FUENTE.get(k.split("/")[-1], "Otra lectura automática")


def _ya_dicho(motivo, seg, hay_alternativas, hay_subrayado):
    """¿Otro elemento de ESTA MISMA linea ya dice lo que dice el motivo?

    Medido el 2026-09-22 sobre las tres grabaciones: «las pasadas no coinciden»
    sale en 362 lineas y las 362 llevan ya el desplegable de otras lecturas --
    escribirlo ademas es duplicarlo. Y «palabra dudosa» sale en 353, de las que
    254 no senalaban ninguna palabra porque la dudosa era «y», «a» o «que»: un
    aviso sobre una conjuncion no es un aviso.

    Lo que NO se puede senalar sigue escribiendose. Nada se oculta: lo dicho
    dos veces se dice una, y todo sigue a un clic."""
    if motivo == "las pasadas no coinciden":
        return hay_alternativas
    if motivo == "palabra dudosa":
        if hay_subrayado:
            return True
        # Sin subrayado solo queda callarlo si lo dudoso eran palabras de
        # funcion; si hubiera una palabra con contenido sin senalar, se dice.
        for w in seg.get("palabras") or []:
            p = w["p"].strip(".,;:()[]¿?¡!\"'")
            if p and len(p) > 2 and p.lower() not in _FUNCION and w.get("c", 1.0) < 0.45:
                return False
        return True
    return False


def jerarquia(seg, marcas, hay_alternativas, hay_subrayado):
    """(el motivo que se escribe en claro, los que quedan plegados).

    Existe porque un aviso en el 71 % de las lineas no es un aviso. En el
    Audio 2 cada linea llevaba hasta seis motivos a la vez y el unico raro y
    grave -- la maquina repitiendose -- quedaba sepultado entre los comunes."""
    resto = sorted(marcas, key=lambda m: _ORDEN_MOTIVOS.index(m)
                   if m in _ORDEN_MOTIVOS else 99)
    for k, m in enumerate(resto):
        if not _ya_dicho(m, seg, hay_alternativas, hay_subrayado):
            return m, resto[:k] + resto[k + 1:]
    return None, resto


def _riesgo(marcas, tiene_dato_duro):
    if not marcas:
        return "ninguno"
    if tiene_dato_duro or any(m in _ALTO for m in marcas):
        return "alto"
    if all(m in _BAJO for m in marcas):
        return "bajo"
    return "medio"


def _datos_duros(seg, umbral=0.85):
    """Cifras y nombres propios con poca confianza: lo que peor sale y mas dano hace."""
    for k, w in enumerate(seg.get("palabras") or []):
        p = w["p"].strip(".,;:()[]¿?¡!\"'")
        if not p or w.get("c", 1) >= umbral:
            continue
        previa = seg["palabras"][k - 1]["p"].strip() if k else "."
        if re.search(r"\d", p) or (p[:1].isupper() and k and not previa.endswith((".", "?", "!"))):
            return True
    return False


VENTANA_S = 20.0


def _corta(t, n=700):
    """Hasta `n` caracteres, sin partir una palabra, y diciendo que sigue."""
    t = t.strip()
    if len(t) <= n:
        return t
    return t[:n].rsplit(" ", 1)[0] + " …"


def _alternativas(ventanas, inicio, gana, limite=6):
    """Que escribieron las OTRAS decodificaciones en este punto. Es un dato que ya
    tenemos y que no estabamos usando: donde difieren, ahi hay algo.
    Devuelve (lista, desacuerdo) donde desacuerdo va de 0 a 1.

    Cada texto es el de la VENTANA entera (20 s: esta linea y las de alrededor),
    no el de la linea: por eso va con su tramo (desde, hasta) y con `pos`, donde
    cae la linea dentro de la ventana; la pagina busca con eso la parte que
    corresponde. Van todas: con tres se escondia justo la que mas decia."""
    for v in ventanas or []:
        if not (v["t"] <= inicio < v["t"] + VENTANA_S):
            continue
        if v.get("medio", 1) >= 0.80:
            return [], 0.0
        out = []
        for k, t in (v.get("textos") or {}).items():
            if k == gana or not t.strip():
                continue
            out.append({"fuente": fuente_visible(k), "texto": _corta(t),
                        "desde": round(v["t"], 2), "hasta": round(v["t"] + VENTANA_S, 2),
                        "pos": round(max(0.0, min(1.0, (inicio - v["t"]) / VENTANA_S)), 3)})
        return out[:limite], round(1.0 - v.get("medio", 1.0), 3)
    return [], 0.0


def _gravedad(seg, marcas, desacuerdo):
    """Cuanto conviene mirar ESTE bloque antes que otro. Hace falta porque en una
    grabacion mala la mitad de las lineas sale en riesgo alto, y entonces el
    riesgo deja de ordenar nada. El riesgo dice QUE clase de problema es; la
    gravedad dice A CUAL ir primero."""
    g = desacuerdo
    for k, w in enumerate(seg.get("palabras") or []):
        p = w["p"].strip(".,;:()[]¿?¡!\"'")
        c = w.get("c", 1.0)
        if not p or c >= 0.85:
            continue
        previa = seg["palabras"][k - 1]["p"].strip() if k else "."
        if re.search(r"\d", p):
            g = max(g, 1.0 - c)                      # una cifra es lo que mas dano hace
        elif p[:1].isupper() and k and not previa.endswith((".", "?", "!")):
            g = max(g, (1.0 - c) * 0.8)              # un nombre propio, casi tanto
        else:
            g = max(g, (1.0 - c) * 0.5)
    if not marcas:
        g = 0.0
    return round(min(1.0, g), 3)


def _norm(t):
    return re.sub(r"[^a-z0-9ñ ]+", " ", t.lower()).split()


# Palabras donde la baja confianza NO importa: aunque el reconocedor dude de
# «de» o «su», la frase se entiende igual. Marcarlas manda el ojo a lo
# irrelevante. Medido sobre el Audio 2: marcar todo por debajo de 0,55 daba 394
# marcas (15 % de las palabras), casi todas asi.
_FUNCION = set((
    "de la el los las un una unos unas y o que en a al del se lo le les por con "
    "para su sus mi tu es son era fue ha he han no si sí ya pero como mas más ni "
    "ese esa eso este esta esto ahí allí aquí muy ya bien"
).split())


def texto_con_dudas(seg, umbral_importante=0.70, umbral_resto=0.45):
    """Marca DENTRO de la frase la palabra concreta de la que el reconocedor dudo.

    ADR-017 §5 prohibe que un ANCLAJE dependa de la marca de palabra, y se
    respeta: el localizador que se publica sigue siendo el minuto del segmento.
    Esto no es un anclaje: es senalar cual de las palabras de esa frase es la
    floja, para no obligarla a adivinarlo. La distincion esta en ADR-019.

    Y la salvaguarda de siempre: si rearmar la frase desde las palabras cambia
    aunque sea una, se devuelve el texto original sin marcar.
    """
    pal = seg.get("palabras") or []
    if not pal:
        return _linea(seg["texto"])
    partes = []
    for k, w in enumerate(pal):
        t = _linea(w["p"])
        c = w.get("c", 1.0)
        p = w["p"].strip(".,;:()[]¿?¡!\"'")
        if not p or p.lower() in _FUNCION or len(p) <= 2:
            partes.append(t); continue
        previa = pal[k - 1]["p"].strip() if k else "."
        importante = bool(re.search(r"\d", p)) or (
            p[:1].isupper() and k and not previa.endswith((".", "?", "!")))
        if c < (umbral_importante if importante else umbral_resto):
            partes.append('<span class="dudosa" title="%s: el reconocedor dudó de esta palabra">%s</span>'
                          % ("Cifra o nombre propio" if importante else "Palabra", t))
        else:
            partes.append(t)
    armado = " ".join(partes)
    llano = html.unescape(re.sub(r"<[^>]+>", "", armado))
    if _norm(llano) != _norm(seg["texto"]):
        return _linea(seg["texto"])
    return armado


def compromisos_de(ruta):
    """{segundo de inicio: [compromisos]} leido del archivo que los senala.

    Va en un archivo aparte y no en los datos de la transcripcion porque son
    dos cosas distintas: la transcripcion dice lo que se oye, y esto dice
    donde alguien se obligo. Lo segundo es una lectura, y las lecturas se
    revisan.

    Una LISTA por segundo: dos obligaciones en la misma frase, o «0:01:00» y
    «00:01:00», son dos compromisos. Con uno por segundo, el ultimo pisaba a
    los demas sin decirlo.
    """
    if not ruta or not os.path.isfile(ruta):
        return {}
    try:
        with io.open(ruta, encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return {}
    fuera = {}
    for c in (d.get("compromisos") or []):
        m = re.match(r"(\d+):(\d\d):(\d\d)", (c.get("minuto") or "").strip())
        if not m:
            continue
        seg = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        fuera.setdefault(seg, []).append(c)
    _poner_ids(fuera)
    return fuera


def _lista(v):
    """Los compromisos de un segundo. Admite tambien uno suelto (forma antigua)."""
    return v if isinstance(v, list) else [v]


def _plano(t):
    """Para localizar una cita: sin tildes, sin puntuacion, palabras separadas
    por un espacio. Una tilde perdida del reconocedor no hace fallar una cita."""
    t = unicodedata.normalize("NFD", (t or "").lower())
    t = "".join(ch for ch in t if unicodedata.category(ch) != "Mn")
    return " ".join(re.sub(r"[^a-z0-9ñ]+", " ", t).split())


def _poner_ids(compromisos):
    """Cada compromiso con un id que sale de lo que ES -- su segundo y su
    cita --, no de su sitio en la lista. Lo que ella declara se guarda por id:
    con el numero de orden, rehacer la lectura pegaba su declaracion a otro
    compromiso. Si dos coinciden en todo, el segundo lleva -2."""
    usados = {c["_id"] for v in compromisos.values() for c in _lista(v) if c.get("_id")}
    for seg in sorted(compromisos):
        for c in _lista(compromisos[seg]):
            if c.get("_id"):
                continue
            huella = hashlib.sha256(_plano(c.get("cita") or c.get("de_que_se_trata") or "")
                                    .encode("utf-8")).hexdigest()[:6]
            base = cid = "c-%d-%s" % (seg, huella)
            n = 1
            while cid in usados:
                n += 1
                cid = "%s-%d" % (base, n)
            usados.add(cid)
            c["_id"] = cid


_TIPO_COMPROMISO = {"tarea": "una tarea", "propuesta": "una propuesta", "condicion": "una condición",
                    "acuerdo": "un acuerdo", "peticion": "una petición",
                    "no_es_compromiso": "según la lectura, no es un compromiso"}


# Lo que tiene que saltar a la vista en un texto largo de la maquina: que algo
# no se dice, que nadie lo asume, que la linea es dudosa. Pedido por el dueno
# el 2026-09-23 al ver una ficha de compromiso: «resaltar esas cosas criticas».
_CRITICAS = ("no se dice", "no consta", "no lo asume", "nadie", "no se entiende", "no es un compromiso",
             "sin cerrar", "palabra dudosa", "puede no ser habla", "las pasadas no coinciden",
             "voz dudosa", "conviene oír", "hay que oír", "probablemente", "no dice", "no sé",
             "no se ponen de acuerdo", "no recoge nada", "no se sostienen")
# La pagina tiene la misma lista en tools/pagina-despacho/src/resalte.js: si
# cambia una, cambia la otra (lo comprueba test_lo_declarado).
_CRITICAS_RE = re.compile(r"(?<![\w])(%s)(?![\w])" % "|".join(re.escape(x) for x in _CRITICAS), re.I)


def resaltar(texto):
    """El texto, escapado, con lo critico en negrita: la etiqueta o veredicto
    corto del principio («Sin cerrar:», «no se dice.»), los minutos y las
    alertas. Dentro de las citas entre « » no se toca nada: son texto literal.
    **Negrita** escrita a mano tambien vale."""
    t = html.escape(texto or "", quote=False)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    partes = re.split(r"(«[^»]*»)", t)
    for k, p in enumerate(partes):
        if p.startswith("«"):
            continue
        p = re.sub(r"(?<!\d)(\d\d:\d\d:\d\d)(?!\d)", r"<strong>\1</strong>", p)
        partes[k] = _CRITICAS_RE.sub(r"<strong>\1</strong>", p)
    t = "".join(partes)
    # El principio, si es corto, es el veredicto. Una entidad (&amp;) no corta
    # la frase aunque lleve punto y coma.
    m = re.match(r"^((?:&#?\w+;|<[^>]*>|«[^»]*»|[^«.:;&<]){2,}?[.:;])(?=\s|$)", t)
    if m and len(re.sub(r"<[^>]*>", "", m.group(1))) <= 60:
        t = "<strong>%s</strong>%s" % (re.sub(r"</?strong>", "", m.group(1)), t[m.end(1):])
    return t


def _con_cita(texto, cita, minuto=""):
    """«texto» y, si la hay, la cita literal que lo sostiene."""
    t = resaltar(texto or "no se dice")
    if cita:
        t += ' <span class="compromiso-cita">«%s»%s</span>' % (
            html.escape(cita), (" " + html.escape(minuto)) if minuto else "")
    return t


def estado_compromiso(c):
    """Lo que la lectura dice del compromiso, o None si no lo dice: sin el
    campo «cerrado» no se sabe, y poner «asumido» era inventarlo."""
    if c.get("cerrado") is None:
        return None
    return "asumido" if c["cerrado"] else "sin cerrar"


def etiqueta_compromiso(c):
    """Lo que ella ve: una etiqueta roja que se lee de un vistazo, de que va,
    y lo que hace falta saber para usarlo en un acta -- quien lo asume, plazo,
    que falta para cerrarlo --, con la cita que lo sostiene.

    Todo es una LECTURA de la transcripcion: nadie lo ha oido, y lo dice en la
    cara visible de la tarjeta, no solo dentro de la ficha plegada (que ni se
    imprime). El minuto ya lo lleva la linea; aqui no se repite. Los campos
    que el archivo no trae no se inventan: simplemente no salen."""
    estado = estado_compromiso(c)
    plazo = (c.get("plazo") or "").strip()
    sin_plazo = not plazo or plazo.lower() in ("no consta", "")
    # «Plazo: no se dice» solo si la lectura habla del plazo (aunque sea para
    # decir que no consta); si no trae nada, no se escribe.
    trae_plazo = bool(plazo) or "plazo_cita" in c
    detalle = html.escape(c.get("de_que_se_trata") or "")
    if not sin_plazo:
        detalle += ' <span class="compromiso-plazo">plazo: %s</span>' % html.escape(plazo)
    # Si la lectura cree que NO es un compromiso, la etiqueta no lo afirma: lo
    # pregunta. Decide ella oyendo; no se borra.
    dudoso = c.get("tipo") == "no_es_compromiso"
    rotulo = "según la lectura, no lo es" if dudoso else estado
    linea = ('<p class="compromiso-linea"><span class="compromiso-sello">%s</span>%s %s</p>'
             % ("¿COMPROMISO?" if dudoso else "COMPROMISO",
                '<span class="compromiso-estado">%s</span>' % html.escape(rotulo) if rotulo else "",
                detalle))
    aviso = ('<p class="compromiso-aviso">Según la lectura automática de la transcripción: '
             'nadie lo ha oído todavía.</p>')

    resumen, ficha = [], []
    if "quien" in c:
        resumen.append("<b>Quién lo asume:</b> %s" % resaltar(c.get("quien") or "no se dice"))
        ficha.append(("Quién lo asume", _con_cita(c.get("quien"), c.get("quien_cita"), c.get("quien_minuto"))))
    if trae_plazo and ("quien" in c or "plazo_cita" in c):
        resumen.append("<b>Plazo:</b> %s" % resaltar("no se dice" if sin_plazo else plazo))
        ficha.append(("Plazo", _con_cita("no se dice" if sin_plazo else plazo, c.get("plazo_cita"))))
    if c.get("falta"):
        resumen.append("<b>Falta:</b> %s" % resaltar(", ".join(c["falta"])))
        ficha.append(("Qué falta para cerrarlo", resaltar("; ".join(c["falta"]))))
    if c.get("ante_quien"):
        ficha.append(("Ante quién", _con_cita(c.get("ante_quien"), c.get("ante_quien_cita"))))
    if c.get("tipo"):
        ficha.append(("Qué es", html.escape(_TIPO_COMPROMISO.get(c["tipo"], c["tipo"]))))
    if c.get("por_que_estado"):
        ficha.append(("Por qué está %s" % estado if estado else "Por qué, según la lectura",
                      resaltar(c["por_que_estado"])))
    if c.get("cita"):
        ficha.append(("Dicho así", "«%s»" % html.escape(c["cita"])))
    if c.get("nota"):
        ficha.append(("Ojo", resaltar(c["nota"])))

    partes = ['<div class="compromiso%s" data-minuto="%s"%s>' % (
        " dudoso" if dudoso else "", html.escape(c.get("minuto") or ""),
        ' data-id="%s"' % html.escape(c["_id"]) if c.get("_id") else ""), linea, aviso]
    if resumen:
        partes.append('<p class="compromiso-resumen">%s</p>' % " · ".join(resumen))
    if ficha:
        partes.append('<details class="compromiso-mas"><summary>Ver la ficha del compromiso</summary><dl>%s</dl>'
                      '</details>'
                      % "".join("<dt>%s</dt><dd>%s</dd>" % (html.escape(k), v) for k, v in ficha))
    partes.append("</div>")
    return "".join(partes)


# Hasta donde se busca cada parte de una cita, alrededor de la linea del minuto.
CITA_CERCA_S = 120.0


def partes_de_cita(cita):
    """Los trozos literales de una cita: van separados por « / » o por una
    elision (…, […]). Una barra sin espacios («3/4») es parte del texto."""
    return [p.strip() for p in re.split(r"\s+/\s+|\s*\[(?:…|\.\.\.)\]\s*|\s*…\s*", cita or "") if _plano(p)]


def localizar_cita(partes, segs, j):
    """(indices de las lineas donde esta cada parte, partes que no estan).

    Cada parte se busca en una linea o en dos o tres seguidas (una frase puede
    quedar partida), dentro de CITA_CERCA_S de la linea j, y gana la mas
    cercana. La cita puede estar en lineas ANTERIORES a la del minuto, o
    salteada: contar n lineas hacia abajo dejaba sin oir justo donde se dice."""
    planos = [_plano(s.get("texto")) for s in segs]
    t0 = segs[j]["inicio"]
    cerca = [abs(s["inicio"] - t0) <= CITA_CERCA_S for s in segs]
    donde, faltan = {j}, []
    for p in partes:
        q = " %s " % _plano(p)
        mejor = None
        for largo in (1, 2, 3):
            for k in range(len(segs) - largo + 1):
                if not all(cerca[k:k + largo]):
                    continue
                if q not in " %s " % " ".join(planos[k:k + largo]):
                    continue
                dist = 0 if k <= j < k + largo else min(abs(k - j), abs(k + largo - 1 - j))
                if mejor is None or (dist, largo) < mejor[0]:
                    mejor = ((dist, largo), range(k, k + largo))
        if mejor is None:
            faltan.append(p)
        else:
            donde.update(mejor[1])
    return sorted(donde), faltan


def contrato_compromisos(compromisos, doc):
    """Para la pagina: cada compromiso con las lineas que hay que oir antes de
    que ella lo declare: desde la primera hasta la ultima de las que llevan
    su cita y la de su minuto. Si una parte de la cita no esta en ninguna
    linea, va en «sin_localizar»: la pagina no deja declarar sin haberla oido,
    y oirla no se puede. Solo los que se colocaron en una linea."""
    segs = doc.get("segmentos") or []
    ids = [s["i"] for s in segs]
    _poner_ids(compromisos)
    out = []
    for seg in sorted(compromisos):
        for c in _lista(compromisos[seg]):
            if "_i" not in c or c["_i"] not in ids:
                continue
            j = ids.index(c["_i"])
            donde, faltan = localizar_cita(partes_de_cita(c.get("cita")), segs, j)
            out.append({"id": c["_id"], "minuto": c.get("minuto") or "",
                        "bloques": ["b%d" % x for x in ids[donde[0]:donde[-1] + 1]],
                        "sin_localizar": faltan,
                        "estado": estado_compromiso(c),
                        "de_que_se_trata": c.get("de_que_se_trata") or "",
                        "quien": c.get("quien"), "plazo": c.get("plazo"), "tipo": c.get("tipo")})
    return out


# Lo que la maquina no sabe leer y conviene que una persona oiga y cuente.
HUECO_ILEGIBLE_S = 8.0
ACUERDO_ILEGIBLE = 0.40


def _a_segundos(v):
    h, m, s = (int(x) for x in v.split(":"))
    return h * 3600 + m * 60 + s


def duracion_de(doc):
    """La duracion REAL del audio, si los datos la traen (transcribir_audio la
    escribe en «duracion_s»). None si no: el fin de la ultima linea no es el
    fin de la grabacion."""
    try:
        d = float(doc.get("duracion_s") or 0)
    except (TypeError, ValueError):
        return None
    return d if d > 0 else None


def _num(x):
    return ("%.2f" % x).rstrip("0").rstrip(".")


def ilegibles_de(doc, ventanas, gana, tramos=None, rescates=None):
    """Los tramos donde la maquina no sabe que se dice, para que una persona los
    oiga y cuente la idea principal y quien la dijo.

    Tres fuentes, y ninguna afirma que alli se hable: (1) huecos de al menos
    8 s sin transcribir -- entre lineas, antes de la primera y, si se sabe
    cuanto dura el audio, despues de la ultima; la transcripcion no recoge
    nada, y a veces es porque la voz estaba lejos --; (2) tramos de 20 s donde
    las lecturas automaticas coinciden menos del 40 %; (3) los tramos que la
    entrega senala a mano. Los que se tocan se juntan. Lo que la maquina creyo
    oir va como pista, con su fuente: no es lo que se dijo.

    El id sale del tramo (desde-hasta), no de su orden: lo que ella cuenta se
    guarda por id, y con el orden quedaba pegado a otro tramo en cuanto
    cambiaba uno anterior."""
    segs = doc.get("segmentos") or []
    fin_lineas = max([s["fin"] for s in segs] or [0])
    dur = duracion_de(doc)
    # Sin la duracion real, nada pasa del fin de la ultima linea: no se sabe
    # si ahi sigue habiendo grabacion.
    tope = dur if dur else fin_lineas
    cand = []
    primero = segs[0]["inicio"] if segs else tope
    if primero >= HUECO_ILEGIBLE_S:
        cand.append({"desde": 0.0, "hasta": primero, "motivos": ["hueco"]})
    for a, b in zip(segs, segs[1:]):
        if b["inicio"] - a["fin"] >= HUECO_ILEGIBLE_S:
            cand.append({"desde": a["fin"], "hasta": b["inicio"], "motivos": ["hueco"]})
    if segs and dur and dur - fin_lineas >= HUECO_ILEGIBLE_S:
        cand.append({"desde": fin_lineas, "hasta": dur, "motivos": ["hueco"]})
    for v in ventanas or []:
        if v.get("medio", 1) < ACUERDO_ILEGIBLE:
            hasta = min(tope, v["t"] + VENTANA_S)
            if hasta - v["t"] < 1.0:
                continue
            cand.append({"desde": v["t"], "hasta": hasta, "motivos": ["discordia"],
                         "acuerdo": round(v["medio"], 3)})
    for t in tramos or []:
        a = [s for s in segs if hms(s["inicio"]) == t["desde"]]
        b = [s for s in segs if hms(s["inicio"]) == t["hasta"]]
        if a and b:
            cand.append({"desde": a[0]["inicio"], "hasta": b[-1]["fin"], "motivos": ["senalado"]})
    cand.sort(key=lambda c: c["desde"])
    juntos = []
    for c in cand:
        if juntos and c["desde"] <= juntos[-1]["hasta"] + 2.0:
            j = juntos[-1]
            j["hasta"] = max(j["hasta"], c["hasta"])
            j["motivos"] = sorted(set(j["motivos"]) | set(c["motivos"]))
            if "acuerdo" in c:
                j["acuerdo"] = min(j.get("acuerdo", 1.0), c["acuerdo"])
        else:
            juntos.append(dict(c))
    out = []
    for j in juntos:
        a, b = j["desde"], j["hasta"]
        if b - a < 1.0:
            continue
        dentro = [s for s in segs if s["fin"] > a and s["inicio"] < b]
        lecturas = []
        for v in ventanas or []:
            if v["t"] < b and v["t"] + 20.0 > a and v.get("medio", 1) < 0.80:
                for kk, tx in (v.get("textos") or {}).items():
                    if kk != gana and tx.strip():
                        lecturas.append({"fuente": fuente_visible(kk), "texto": tx.strip()[:300]})
        for r in rescates or []:
            if r.get("ini", 0) < b and r.get("fin", 0) > a and (r.get("texto") or "").strip():
                lecturas.append({"fuente": "Lectura aislada de ese trozo" + (" (posible invención)"
                                 if r.get("invencion") else ""), "texto": r["texto"].strip()[:300]})
        out.append({
            "id": "i-%s-%s" % (_num(a), _num(b)), "desde": round(a, 2), "hasta": round(b, 2),
            "motivos": j["motivos"],
            "acuerdo": j.get("acuerdo"),
            "transcripcion": [{"id": "b%d" % s["i"], "hora": hms(s["inicio"]), "texto": s["texto"]} for s in dentro][:12],
            "lecturas": lecturas[:4],
        })
    return out


def _avisos_de_bucle(doc):
    """{indice de segmento: cartel} para abrir y cerrar cada tramo repetido.

    El criterio vive en `estado_transcripcion`, que es la puerta, y se importa
    en vez de copiarse: si un dia cambia lo que cuenta como repeticion, cambia
    en un sitio.

    Va como bloque y no como un motivo mas de la linea porque el motivo por
    linea ya existe -- «posible repeticion» -- y llega ahogado entre otros
    cuatro. Un tramo repetido se ve sin oir; los demas motivos, no.
    """
    try:
        from estado_transcripcion import bucles as detectar
    except ImportError as e:
        # Callarlo dejaba la pagina sin los carteles de «la maquina se repitio»
        # y el programa decia OK.
        raise SystemExit("NO SE PUDO GENERAR: falta estado_transcripcion (%s); sin el no se "
                         "pueden senalar los tramos repetidos." % e)
    abre, cierra = {}, {}
    for b in detectar(doc):
        n = b['veces']
        abre[b['lineas'][0]] = (
            '<div class="aviso-bucle"><strong>&#9888; Aquí la máquina se repitió: '
            'las %d líneas siguientes dicen lo mismo.</strong> De %s a %s. '
            'Lo más probable es que <strong>%d de estas %d no las dijera nadie</strong>; '
            'se sabe sin oír, porque el reconocedor se engancha y repite la última frase '
            'mientras la grabación sigue. Nadie lo ha comprobado oyendo: son %d segundos. '
            'No se ha borrado nada.</div>'
            % (n, hms(b['desde']), hms(b['hasta']), n - 1, n,
               round(b['hasta'] - b['desde'])))
        cierra[b['lineas'][-1]] = ('<div class="aviso-bucle cierre">'
                                   '<strong>&#9888; Fin del tramo repetido.</strong></div>')
    return abre, cierra


def rescates_de(ruta, audio):
    """Los huecos que se volvieron a oir (genoma de voz), de ESTA grabacion."""
    if not ruta or not audio:
        return []
    if not os.path.isfile(ruta):
        raise SystemExit("NO SE PUDO GENERAR: no esta el archivo de rescates %s" % ruta)
    g = json.load(io.open(ruta, encoding="utf-8"))
    return [r for r in (g.get("rescates") or []) if r.get("audio") == audio]


def tramos_de(ruta):
    """Los tramos que una entrega senala a mano: [{desde, hasta, abre, cierra}].

    El aviso llega ya redactado (Markdown de una linea): lo redacta quien arma
    la entrega, y el Word lleva el mismo texto. Aqui solo se coloca."""
    if not ruta:
        return []
    if not os.path.isfile(ruta):
        raise SystemExit("NO SE PUDO GENERAR: no esta el archivo de tramos %s" % ruta)
    tramos = json.load(io.open(ruta, encoding="utf-8"))
    for t in tramos:
        if not all(isinstance(t.get(k), str) and t[k].strip()
                   for k in ("desde", "hasta", "abre", "cierra")):
            raise SystemExit("NO SE PUDO GENERAR: un tramo senalado no trae desde, hasta, "
                             "abre y cierra")
    return tramos


def _avisos_de_tramos(doc, tramos):
    """{indice de segmento: cartel} para abrir y cerrar cada tramo senalado.

    La linea se busca por la hora que IMPRIME, que es la que se cita. Si no
    esta, o esta dos veces, no se genera la pagina: un aviso que cae en otra
    linea, o que se cae en silencio, es peor que no tenerlo."""
    abre, cierra = {}, {}
    for t in tramos:
        a = [s["i"] for s in doc["segmentos"] if hms(s["inicio"]) == t["desde"]]
        z = [s["i"] for s in doc["segmentos"] if hms(s["inicio"]) == t["hasta"]]
        if len(a) != 1 or len(z) != 1 or z[0] < a[0]:
            raise SystemExit("NO SE PUDO GENERAR: el tramo senalado %s-%s no se localiza en "
                             "los datos (%d lineas a las %s, %d a las %s)"
                             % (t["desde"], t["hasta"], len(a), t["desde"], len(z), t["hasta"]))
        abre[a[0]] = abre.get(a[0], "") + (
            '<div class="aviso-bucle tramo">&#9888; %s</div>' % _linea(t["abre"]))
        cierra[z[0]] = ('<div class="aviso-bucle tramo cierre">&#9888; %s</div>'
                        % _linea(t["cierra"])) + cierra.get(z[0], "")
    return abre, cierra


def construir_bloques(doc, marcas, ventanas, gana, etiquetas=None, compromisos=None,
                      tramos=None):
    """Devuelve (html, bloques del contrato). El HTML se lee sin JavaScript;
    el contrato lleva los metadatos que la pagina necesita para trabajar.

    Los segmentos se agrupan en TURNOS de habla. Era el defecto que mas pesaba
    en la primera entrega: trescientas ochenta y seis lineas sueltas no dejan
    ver quien habla ni que dice. Un turno se lee como una intervencion.
    """
    partes, bloques = [], []
    compromisos = compromisos or {}
    _poner_ids(compromisos)
    # A que linea se pega cada compromiso. Los minutos vienen con resolucion de
    # SEGUNDO y las lineas empiezan con decimales, asi que exigir que el segundo
    # caiga dentro dejaba fuera uno de cada cuatro -- y en silencio, que es lo
    # peor: la pagina salia con menos etiquetas de las que habia y nadie lo veia.
    #
    # Y el minuto que se cita es el que la linea IMPRIME, que es su inicio
    # truncado al segundo. Buscar primero «la linea que contiene ese segundo»
    # pegaba la etiqueta a la ANTERIOR cuando esta acaba despues: en el Audio 2
    # de un caso real, 5 de 10 cayeron una linea arriba, y el sello «asumido» quedo
    # sobre «y listo» en vez de sobre «quedamos con el compromiso». Por eso gana
    # primero la linea cuyo minuto impreso es exactamente el citado.
    _donde = {}
    for _k in compromisos:
        _mejor, _dist = None, None
        _exacta = next((_s for _s in doc["segmentos"] if int(_s["inicio"]) == _k), None)
        if _exacta is not None:
            _donde.setdefault(_exacta["i"], []).append(_k)
            continue
        for _s in doc["segmentos"]:
            if _s["inicio"] <= _k < _s["fin"]:
                _mejor, _dist = _s["i"], 0.0
                break
            _d = abs(_s["inicio"] - _k)
            if _dist is None or _d < _dist:
                _mejor, _dist = _s["i"], _d
        if _mejor is not None and _dist is not None and _dist <= 2.0:
            _donde.setdefault(_mejor, []).append(_k)
    abre_bucle, cierra_bucle = _avisos_de_bucle(doc)
    # Un tramo senalado puede envolver un tramo repetido: abre antes y cierra
    # despues.
    abre_t, cierra_t = _avisos_de_tramos(doc, tramos or [])
    for _k, _v in abre_t.items():
        abre_bucle[_k] = _v + abre_bucle.get(_k, "")
    for _k, _v in cierra_t.items():
        cierra_bucle[_k] = cierra_bucle.get(_k, "") + _v
    voz_previa = object()
    fin_previo = None
    abierto = False

    def cerrar():
        nonlocal abierto
        if abierto:
            partes.append("</section>")
            abierto = False

    def pausa(desde, hasta):
        return ('<p class="pausa hueco" data-desde="%.2f" data-hasta="%.2f">— %d s sin '
                'transcribir —</p>' % (desde, hasta, round(hasta - desde)))

    for s in doc["segmentos"]:
        bid = "b%d" % s["i"]
        mk = marcas.get(str(s["i"])) or marcas.get(s["i"]) or []
        duro = _datos_duros(s)
        riesgo = _riesgo(mk, duro)
        alts_previas, _desac_previo = _alternativas(ventanas, s["inicio"], gana)
        voz = s.get("voz")

        # Turno nuevo SOLO cuando cambia la voz. Una pausa larga dentro de la
        # misma voz es una pausa, no otra intervencion: cortar ahi fragmentaba
        # la lectura en turnos consecutivos del mismo hablante.
        # Si hay un silencio muy largo se marca la pausa, sin abrir turno.
        # El principio de la grabacion cuenta: antes de la primera linea
        # tambien puede haber audio sin transcribir.
        desde_h = 0.0 if fin_previo is None else fin_previo
        hueco = s["inicio"] - desde_h
        # Un hueco largo se marca SIEMPRE, cambie o no la voz. Decia «sin habla
        # detectada», y en un caso real una lectura aislada oyo habla en un hueco
        # de 46 s: lo unico que se sabe es que no hay transcripcion.
        if hueco >= HUECO_ILEGIBLE_S:
            if voz != voz_previa:
                cerrar()
            partes.append(pausa(desde_h, s["inicio"]))
        if voz != voz_previa:
            cerrar()
            quien = ("Hablante %s" % html.escape(str(voz))) if voz is not None else "Hablante ?"
            # El nombre, si una PERSONA lo declaro. La maquina agrupa; nombrar es
            # de ella, y por eso el nombre va pegado a quien lo afirma.
            et = (etiquetas or {}).get(str(voz)) if voz is not None else None
            segun = ""
            if et:
                if et.get("texto"):
                    quien += ' <span class="nombrada">%s</span>' % html.escape(et["texto"])
                avisos = [x for x in (et.get("aviso"), et.get("procedencia")) if x]
                if avisos:
                    segun = '<span class="segun">%s</span>' % html.escape(" · ".join(avisos))
            partes.append(
                '<section class="turno"><h3 class="turno-cab">'
                '<span class="quien">%s</span>%s'
                '<span class="desde">desde %s</span></h3>' % (quien, segun, hms(s["inicio"])))
            abierto = True
        voz_previa, fin_previo = voz, s["fin"]

        if s['i'] in abre_bucle:
            partes.append(abre_bucle[s['i']])
        # La etiqueta va DELANTE de la linea: asi el ojo la encuentra bajando
        # por la pagina sin tener que leer el texto.
        for _seg in _donde.get(s["i"], []):
            for _c in _lista(compromisos[_seg]):
                _c["_i"] = s["i"]
                partes.append(etiqueta_compromiso(_c))

        cuerpo = [
            '<article class="seg%s" id="%s">' % (" dudoso" if mk else "", bid),
            '<div class="seg-cab">'
            '<button type="button" class="hora" disabled>%s</button></div>' % hms(s["inicio"]),
            '<p class="texto">%s</p>' % texto_con_dudas(s),
        ]
        if mk:
            texto_seg = texto_con_dudas(s)
            principal, plegados = jerarquia(
                s, mk, bool(alts_previas), 'class="dudosa"' in texto_seg)
            partes_m = []
            if principal:
                partes_m.append('<span class="principal">%s</span>'
                                % html.escape(visible(principal)))
            if plegados:
                partes_m.append(
                    '<details class="motivos-mas"><summary>%s</summary>%s</details>'
                    % ("y %d motivo%s más" % (len(plegados), "" if len(plegados) == 1 else "s")
                       if principal else
                       # Sin principal, todos los motivos de esta linea ya los
                       # dice otro elemento o no pueden senalar nada. Decir
                       # «1 motivo» no informa; decir que es menor, si.
                       "%d motivo%s menor%s" % (len(plegados), "" if len(plegados) == 1 else "s",
                                                "" if len(plegados) == 1 else "es"),
                       html.escape("; ".join(visible(x) for x in plegados))))
            cuerpo.append('<div class="motivos">%s</div>' % "".join(partes_m))
        cuerpo.append("</article>")
        partes.append("".join(cuerpo))
        if s['i'] in cierra_bucle:
            partes.append(cierra_bucle[s['i']])

        alts, desacuerdo = alts_previas, _desac_previo
        bloques.append({
            "id": bid,
            "ancla": {"tipo": "tiempo", "inicio": round(s["inicio"], 3), "fin": round(s["fin"], 3)},
            "riesgo": riesgo,
            "gravedad": _gravedad(s, mk, desacuerdo),
            "marcas": mk,
            "etiqueta": ((("Hablante %s" % voz) + ((" — " + (etiquetas or {}).get(str(voz), {}).get("texto", ""))
                          if (etiquetas or {}).get(str(voz), {}).get("texto") else ""))
                         if voz is not None else None),
            "alternativas": alts,
        })
    cerrar()
    # Y el final: lo que queda de grabacion tras la ultima linea, si se sabe
    # cuanto dura. Son los mismos huecos que pregunta «Lo que no se entiende».
    dur = duracion_de(doc)
    ultimo = max([s["fin"] for s in doc["segmentos"]] or [0.0])
    if dur and dur - ultimo >= HUECO_ILEGIBLE_S:
        partes.append(pausa(ultimo, dur))
    return "\n".join(partes), bloques


def bloque_voces(d):
    """Quien declaro las voces, en la propia pagina.

    Va en el CUERPO y no en la ficha de la cabecera porque la ficha solo admite
    «Campo: valor», y esto es una lista donde cada linea lleva su procedencia."""
    et = d.get("etiquetas") or {}
    if not et:
        return ""
    dec = d.get("voces_declaradas") or {}
    quien = dec.get("declarado_por") or "una persona"
    fecha = dec.get("fecha") or "sin fecha"
    filas = []
    for v in sorted(et, key=lambda x: int(x) if str(x).isdigit() else 99):
        e = et[v]
        partes = ["<strong>Hablante %s</strong>" % html.escape(str(v))]
        if e.get("texto"):
            partes.append(html.escape(e["texto"]))
        if e.get("como_lo_se"):
            partes.append("<em>%s</em>" % html.escape(e["como_lo_se"]))
        if e.get("aviso"):
            partes.append(html.escape(e["aviso"]))
        filas.append("<li>%s</li>" % " — ".join(partes))
    return ('<section class="voces-declaradas"><h2>Quién es cada voz</h2>'
            '<p>Lo declaró <strong>%s</strong> el <strong>%s</strong>. '
            '<strong>No lo comprobó ningún programa:</strong> la máquina agrupó las voces por '
            'su sonido, y el nombre lo puso una persona.</p><ul>%s</ul></section>'
            % (html.escape(quien), html.escape(fecha), "".join(filas)))


# -------------------------------------------------------------------- pagina
def construir_lista(d, doc, marcas):
    """«Pasajes a verificar» como cola de trabajo, no como documento.

    Patron «check your answers» de GOV.UK: una fila por cosa que comprobar, con
    su sitio, lo que dice y una accion. Aqui cada hallazgo es un BLOQUE del mismo
    contrato que usa la transcripcion, asi que hereda la franja, el teclado, los
    estados y la copia con procedencia sin una sola linea nueva de interfaz.
    """
    segs = doc["segmentos"]

    def seg_en(t):
        for s in segs:
            if s["inicio"] <= t <= s["fin"]:
                return s
        anteriores = [s for s in segs if s["inicio"] <= t]
        return anteriores[-1] if anteriores else (segs[0] if segs else None)

    hallazgos = []

    for v in d.get("ventanas") or []:
        if v.get("medio", 1) >= 0.80:
            continue
        otras = [(k, t) for k, t in (v.get("textos") or {}).items() if t.strip()]
        hallazgos.append({
            "clase": "Las lecturas automáticas no coinciden",
            "t": v["t"], "riesgo": "alto", "gravedad": round(1 - v["medio"], 3),
            "detalle": "Coinciden solo en un %d %%." % round(100 * v["medio"]),
            "variantes": otras[:4],
        })

    for a in d.get("avisos_glosario") or []:
        hallazgos.append({
            "clase": "El glosario habría escrito otra cosa",
            "t": a["t"], "riesgo": "alto", "gravedad": 0.75,
            "detalle": "Sugiere «%s» donde la versión publicada dice: %s"
                       % (a["sugiere"], a["dice_publicada"]),
            "variantes": [],
        })

    for s in segs:
        for k, w in enumerate(s.get("palabras") or []):
            p = w["p"].strip(".,;:()[]¿?¡!\"'")
            if not p or w.get("c", 1) >= 0.85:
                continue
            previa = s["palabras"][k - 1]["p"].strip() if k else "."
            cifra = bool(re.search(r"\d", p))
            propio = p[:1].isupper() and k and not previa.endswith((".", "?", "!"))
            if not (cifra or propio):
                continue
            hallazgos.append({
                "clase": "Cifra en duda" if cifra else "Nombre propio en duda",
                "t": s["inicio"], "riesgo": "alto" if cifra else "medio",
                "gravedad": round((1 - w["c"]) * (1.0 if cifra else 0.8), 3),
                "detalle": "Escribió «%s»." % p, "variantes": [],
            })
        if s.get("voz") is not None and s.get("pureza", 1) < 0.60:
            hallazgos.append({
                "clase": "La voz asignada es dudosa", "t": s["inicio"], "riesgo": "bajo",
                "gravedad": round(0.4 * (1 - s.get("pureza", 0)), 3),
                "detalle": "La línea se reparte entre hablantes; ahí el número de hablante "
                           "no significa gran cosa.",
                "variantes": [],
            })

    hallazgos.sort(key=lambda h: -h["gravedad"])

    partes, bloques = [], []
    for i, h in enumerate(hallazgos):
        bid = "h%d" % i
        s = seg_en(h["t"])
        texto = s["texto"] if s else ""
        cuerpo = [
            '<article class="seg ficha-hallazgo dudoso" id="%s">' % bid,
            '<div class="seg-cab">',
            '<button type="button" class="hora" disabled>%s</button>' % hms(h["t"]),
            '<span class="clase r-%s">%s</span></div>' % (h["riesgo"], html.escape(h["clase"])),
            '<p class="texto">%s</p>' % _linea(texto),
            '<p class="motivos">%s</p>' % (resaltar(h["detalle"]) if "**" not in h["detalle"] and "`" not in h["detalle"] else _linea(h["detalle"])),
        ]
        if h["variantes"]:
            cuerpo.append('<details class="alternativas"><summary>Qué escribió cada lectura automática</summary>')
            for k, t in h["variantes"]:
                cuerpo.append('<p><span class="et">%s</span>%s</p>'
                              % (html.escape(fuente_visible(k)), html.escape(t[:240])))
            cuerpo.append("</details>")
        cuerpo.append("</article>")
        partes.append("".join(cuerpo))
        bloques.append({
            "id": bid,
            "ancla": {"tipo": "tiempo", "inicio": round(h["t"], 3),
                      "fin": round(h["t"] + 20, 3)},
            "riesgo": h["riesgo"], "gravedad": h["gravedad"],
            "marcas": [h["clase"]], "etiqueta": None, "alternativas": [],
        })
    return "\n".join(partes), bloques, len(hallazgos)


def datos_en_script(datos):
    """El contrato, listo para ir dentro de <script type="application/json">.

    Un texto con «</script>» -- en una nota del glosario, una lectura o una
    linea transcrita -- cortaba el bloque, y lo que venia detras entraba en la
    pagina como HTML vivo. En JSON un «<» solo puede ir dentro de una cadena,
    y ahi \\u003c es el mismo caracter: JSON.parse y json.loads lo leen igual."""
    return json.dumps(datos, ensure_ascii=False).replace("<", "\\u003c")


def partir(md):
    """Encabezado (antes del primer ---) y cuerpo."""
    m = re.search(r"\n---+\n", md)
    return (md[:m.start()], md[m.end():]) if m else (md, "")


def ficha_desde(cabecera):
    """Las lineas «**Campo:** valor» del encabezado se convierten en lista de definicion.

    Un valor que sigue en la linea de abajo -- sin linea en blanco en medio y
    sin empezar por otra marca -- es del mismo campo: antes se partia y la
    continuacion quedaba suelta, sin su campo."""
    campos, resto = [], []
    abierto = False
    for l in cabecera.split("\n"):
        m = re.match(r"^\*\*(.+?):\*\*\s*(.*?)\s*$", l.strip())
        if m and not l.strip().startswith("# "):
            campos.append([m.group(1), m.group(2).rstrip()])
            abierto = True
        elif abierto and l.strip() and not re.match(r"^\s*(\*\*|>|#|-|\||\d+\.|<!--)", l):
            campos[-1][1] += " " + l.strip()
        else:
            abierto = False
            resto.append(l)
    filas = [f"<dt>{_linea(c)}</dt><dd>{_linea(v)}</dd>" for c, v in campos]
    return "".join(filas), "\n".join(resto)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada")
    ap.add_argument("salida")
    ap.add_argument("--datos", default=None)
    ap.add_argument("--compromisos", default=None,
                    help="el .json que señala dónde se habló de un compromiso")
    ap.add_argument("--tramos", default=None,
                    help="el .json de tramos que la entrega senala a mano, con su aviso "
                         "ya redactado: [{desde, hasta, abre, cierra}]")
    ap.add_argument("--glosario", default=None,
                    help="sugerencias de glosario del caso (.json): [{oye, dijo, nota}]. Son "
                         "hipotesis: la pagina las ensena aparte y solo cuentan si ella las acepta")
    ap.add_argument("--caso", default=None,
                    help="identificador del caso: el glosario que ella escribe vale para todas "
                         "las paginas con el mismo")
    ap.add_argument("--rescates", default=None,
                    help="el genoma de voz (.json) con los huecos que se volvieron a oir: sus "
                         "lecturas van como pista en «lo que no se entiende»")
    ap.add_argument("--rescates-audio", default=None, help="que audio del genoma es este (p. ej. A2)")
    ap.add_argument("--audio", default=None)
    ap.add_argument("--sonda", default=None,
                    help="archivo que deberia estar junto a la pagina; si no carga, "
                         "la pagina avisa de que esta sola (abierta desde el .zip)")
    ap.add_argument("--origen", default=None,
                    help="como se nombra el documento al copiar una cita con su procedencia")
    ap.add_argument("--tipo", default=None,
                    help="etiqueta de la cabecera en paginas sin grabacion")
    ap.add_argument("--advertencia", default=None,
                    help="aviso de cabecera en paginas sin grabacion (admite **negrita**)")
    ap.add_argument("--lista", action="store_true",
                    help="produce la cola de comprobacion en vez del documento")
    a = ap.parse_args()

    if not os.path.exists(PLANTILLA):
        sys.stderr.write(
            "NO SE PUDO GENERAR: falta la plantilla compilada en\n  %s\n"
            "Se compila con: cd tools/pagina-despacho && npm run publicar\n"
            "No se escribio ningun archivo.\n" % PLANTILLA)
        return 2

    md = io.open(a.entrada, encoding="utf-8").read()
    plantilla = io.open(PLANTILLA, encoding="utf-8").read()
    cabecera, cuerpo = partir(md)

    titulo = "Documento"
    m = re.search(r"^#\s+(.*)$", cabecera, re.M)
    if m:
        titulo = re.sub(r"[*`]", "", m.group(1)).strip()
    ficha, resto_cabecera = ficha_desde(cabecera)
    # Lo que la cabecera trae y no es «**Campo:** valor» -- un aviso, un parrafo
    # que dice que esta entrega sustituye a otra -- se tiraba en silencio: el
    # Word lo llevaba y la pagina no. Asi, el enlace a una correccion no salio
    # nunca en la portada. Va ahora al principio del contenido.
    _lineas, _titulo_visto = [], False
    for l in resto_cabecera.split("\n"):
        if not _titulo_visto and re.match(r"^\s*#\s", l):
            _titulo_visto = True
            continue
        if re.match(r"^\s*<!--.*-->\s*$", l):
            continue
        _lineas.append(l)
    sueltas = "\n".join(_lineas).strip()
    # Solo si hubo separador: sin el, todo el Markdown ya es contenido (y, con
    # --datos, se pintaria la transcripcion entera dos veces).
    cabecera_html = md_a_html(sueltas) if sueltas and cuerpo else ""

    advertencia = ("El original es la grabación o el documento del que salió esto. "
                   "Ninguna cita debería usarse sin comprobarla contra él.")
    tipo = "Superficie de trabajo"
    # El contrato: lo unico que la pagina sabe del mundo. No menciona
    # transcripciones en ninguna parte, a proposito.
    datos = {
        "documento": {"titulo": titulo, "tipo": tipo,
                      "origen": os.path.basename(a.entrada),
                      "tipoMaterial": "Material derivado"},
        "fuentes": [], "bloques": [], "vistas": ["lectura"], "version": VERSION,
    }

    if a.datos:
        d = json.load(io.open(a.datos, encoding="utf-8"))
        doc = d.get("publicada") or d.get("principal")
        if not doc:
            sys.stderr.write("El archivo de datos no trae la pasada publicada.\n")
            return 2
        marcas = d.get("marcas", {})
        gana = doc.get("etiqueta", "")
        if a.lista:
            contenido, bloques, n_hall = construir_lista(d, doc, marcas)
            tipo = "Cola de comprobación"
            titulo = "QUÉ COMPROBAR — " + re.sub(r"^TRANSCRIPCI[ÓO]N\s*[—-]\s*", "", titulo)
        else:
            comps = compromisos_de(a.compromisos)
            contenido, bloques = construir_bloques(doc, marcas, d.get("ventanas"), gana,
                                                   d.get("etiquetas"), comps,
                                                   tramos_de(a.tramos))
            datos["compromisos"] = contrato_compromisos(comps, doc)
            contenido = bloque_voces(d) + contenido
            n_hall = None
            tipo = "Transcripción · superficie de trabajo"
        datos["bloques"] = bloques
        if a.caso:
            datos["caso"] = a.caso
        if a.glosario:
            if not os.path.isfile(a.glosario):
                raise SystemExit("NO SE PUDO GENERAR: no esta el glosario %s" % a.glosario)
            g = json.load(io.open(a.glosario, encoding="utf-8"))
            datos["glosario"] = [{"oye": s["oye"], "dijo": s["dijo"], "nota": s.get("nota", "")}
                                 for s in (g.get("sugerencias") or []) if s.get("oye") and s.get("dijo")]
        if not a.lista:
            datos["ilegibles"] = ilegibles_de(doc, d.get("ventanas"), gana, tramos_de(a.tramos),
                                              rescates_de(a.rescates, a.rescates_audio))
        datos["vistas"] = ["lectura", "resumen", "comprobacion"]
        datos["documento"]["tipo"] = tipo
        datos["documento"]["origen"] = a.origen or titulo
        if a.audio:
            # Ruta RELATIVA desde la pagina hasta la grabacion: asi la carpeta se
            # puede mover entera. Si el audio no esta, la pagina lo dice (ADR-020 §5).
            try:
                rel = os.path.relpath(os.path.abspath(a.audio),
                                      os.path.dirname(os.path.abspath(a.salida)))
            except ValueError:
                rel = os.path.basename(a.audio)
            datos["fuentes"].append({"tipo": "audio", "ruta": rel.replace("\\", "/")})
            if not os.path.exists(a.audio):
                sys.stderr.write("AVISO: no se encontro la grabacion en %s. "
                                 "La pagina se genera y dira que no puede comprobar.\n" % a.audio)
        alto = sum(1 for b in bloques if b["riesgo"] == "alto")
        n_dud = sum(1 for b in bloques if b["riesgo"] != "ninguno")
        if a.lista:
            advertencia = (
                "Esta no es la transcripción: es <strong>la lista de lo que conviene comprobar "
                "oyendo</strong>, ordenada de más grave a menos. <strong>%d cosas</strong>, "
                "de las que <strong>%d son de las que más daño hacen</strong>. Pulse una hora "
                "y sonará ese punto. Márquelas a medida que las oiga; <strong>lo que marque es "
                "constancia suya, no verificación de ningún sistema</strong>. "
                "No es una lista de errores comprobados: es dónde mirar primero."
                % (n_hall, alto))
        else:
            advertencia += (
            " De %d líneas, <strong>%d tienen algún motivo de duda</strong>, y de esas "
            "<strong>%d son de las que más daño hacen</strong>: una cifra o un nombre "
            "propio en duda, o un punto donde las lecturas automáticas no coinciden. "
            "La franja de arriba dice dónde están. Cada marca de tiempo reproduce ese "
            "punto de la grabación; lo que usted marque como comprobado es constancia "
            "suya, <strong>no verificación de ningún sistema</strong>."
                % (len(bloques), n_dud, alto))
    else:
        contenido = md_a_html(cuerpo if cuerpo else md)
        if a.tipo:
            tipo = datos["documento"]["tipo"] = a.tipo
        if a.advertencia:
            advertencia = _linea(a.advertencia)
    if cabecera_html and a.datos and not a.lista:
        # En la transcripcion, el aviso de su cabecera va al recuadro de arriba,
        # que es lo primero que se ve: al principio del contenido quedaba debajo
        # del pliegue y de la barra fija.
        advertencia += '<div class="propuesta-mas">%s</div>' % cabecera_html
    elif cabecera_html and not a.lista:
        contenido = cabecera_html + contenido

    if a.sonda:
        try:
            rel = os.path.relpath(os.path.abspath(a.sonda),
                                  os.path.dirname(os.path.abspath(a.salida)))
        except ValueError:
            rel = os.path.basename(a.sonda)
        datos["sonda"] = rel.replace("\\", "/")

    # La lista y la transcripcion salen del MISMO Markdown pero numeran sus bloques
    # distinto (h0.. frente a b0..). Con la misma clave, el contador de una contaba
    # las marcas de la otra, y con las dos abiertas cada marca borraba las ajenas.
    datos["clave"] = hashlib.sha256(
        (md + ("\x00lista" if a.lista else "")).encode("utf-8")).hexdigest()[:16]

    pie = ("<p>Página generada por <code>md2html %s</code> a partir de "
           "<code>%s</code>. Es material derivado: no es el original."
           % (VERSION, html.escape(os.path.basename(a.entrada))))
    if a.datos:
        pie += (" Lo que usted marque aquí vive en este navegador: <strong>use «Guardar "
                "lo comprobado» antes de cerrar</strong>.")
    pie += "</p>"

    out = plantilla
    for k, v in (("{{TITULO}}", html.escape(titulo)), ("{{TIPO}}", html.escape(tipo)),
                 ("{{FICHA}}", ficha), ("{{ADVERTENCIA}}", advertencia),
                 ("{{CONTENIDO}}", contenido), ("{{PIE}}", pie),
                 ("{{DATOS}}", datos_en_script(datos))):
        out = out.replace(k, v)

    io.open(a.salida, "w", encoding="utf-8").write(out)
    print("OK  %s  -  %.1f KB%s" % (os.path.basename(a.salida), len(out) / 1024,
                                    "  (interactiva)" if a.datos else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
