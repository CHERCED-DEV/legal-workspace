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
import argparse, hashlib, html, io, json, os, re, sys, urllib.parse

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


def _alternativas(ventanas, inicio, gana, limite=3):
    """Que escribieron las OTRAS decodificaciones en este punto. Es un dato que ya
    tenemos y que no estabamos usando: donde difieren, ahi hay algo.
    Devuelve (lista, desacuerdo) donde desacuerdo va de 0 a 1."""
    for v in ventanas or []:
        if not (v["t"] <= inicio < v["t"] + 20.0):
            continue
        if v.get("medio", 1) >= 0.80:
            return [], 0.0
        out = []
        for k, t in (v.get("textos") or {}).items():
            if k == gana or not t.strip():
                continue
            out.append({"fuente": fuente_visible(k), "texto": t[:260]})
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
    """{segundo de inicio: compromiso} leido del archivo que los senala.

    Va en un archivo aparte y no en los datos de la transcripcion porque son
    dos cosas distintas: la transcripcion dice lo que se oye, y esto dice
    donde alguien se obligo. Lo segundo es una lectura, y las lecturas se
    revisan.
    """
    if not ruta or not os.path.isfile(ruta):
        return {}
    try:
        d = json.load(io.open(ruta, encoding="utf-8"))
    except Exception:
        return {}
    fuera = {}
    for c in (d.get("compromisos") or []):
        m = re.match(r"(\d+):(\d\d):(\d\d)", (c.get("minuto") or "").strip())
        if not m:
            continue
        seg = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        fuera[seg] = c
    return fuera


def etiqueta_compromiso(c):
    """Lo que ella ve: una etiqueta roja que se lee de un vistazo, y debajo
    de que va. El minuto ya lo lleva la linea; aqui no se repite."""
    estado = "sin cerrar" if not c.get("cerrado", True) else "asumido"
    plazo = (c.get("plazo") or "").strip()
    detalle = html.escape(c.get("de_que_se_trata") or "")
    if plazo and plazo.lower() not in ("no consta", ""):
        detalle += ' <span class="compromiso-plazo">plazo: %s</span>' % html.escape(plazo)
    return ('<p class="compromiso"><span class="compromiso-sello">COMPROMISO</span>'
            '<span class="compromiso-estado">%s</span> %s</p>'
            % (html.escape(estado), detalle))


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
    except Exception:
        return {}, {}
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


def construir_bloques(doc, marcas, ventanas, gana, etiquetas=None, compromisos=None):
    """Devuelve (html, bloques del contrato). El HTML se lee sin JavaScript;
    el contrato lleva los metadatos que la pagina necesita para trabajar.

    Los segmentos se agrupan en TURNOS de habla. Era el defecto que mas pesaba
    en la primera entrega: trescientas ochenta y seis lineas sueltas no dejan
    ver quien habla ni que dice. Un turno se lee como una intervencion.
    """
    partes, bloques = [], []
    compromisos = compromisos or {}
    # A que linea se pega cada compromiso. Los minutos vienen con resolucion de
    # SEGUNDO y las lineas empiezan con decimales, asi que exigir que el segundo
    # caiga dentro dejaba fuera uno de cada cuatro -- y en silencio, que es lo
    # peor: la pagina salia con menos etiquetas de las que habia y nadie lo veia.
    #
    # Y el minuto que se cita es el que la linea IMPRIME, que es su inicio
    # truncado al segundo. Buscar primero «la linea que contiene ese segundo»
    # pegaba la etiqueta a la ANTERIOR cuando esta acaba despues: en el Audio 2
    # de Calarca, 5 de 10 cayeron una linea arriba, y el sello «asumido» quedo
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
    voz_previa = object()
    fin_previo = -99.0
    abierto = False

    def cerrar():
        nonlocal abierto
        if abierto:
            partes.append("</section>")
            abierto = False

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
        hueco = s["inicio"] - fin_previo
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
        elif hueco > 10.0 and abierto:
            partes.append('<p class="pausa">— %d segundos sin habla detectada —</p>' % round(hueco))
        voz_previa, fin_previo = voz, s["fin"]

        if s['i'] in abre_bucle:
            partes.append(abre_bucle[s['i']])
        # La etiqueta va DELANTE de la linea: asi el ojo la encuentra bajando
        # por la pagina sin tener que leer el texto.
        for _seg in _donde.get(s["i"], []):
            partes.append(etiqueta_compromiso(compromisos[_seg]))

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
            '<p class="motivos">%s</p>' % _linea(h["detalle"]),
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


def partir(md):
    """Encabezado (antes del primer ---) y cuerpo."""
    m = re.search(r"\n---+\n", md)
    return (md[:m.start()], md[m.end():]) if m else (md, "")


def ficha_desde(cabecera):
    """Las lineas «**Campo:** valor» del encabezado se convierten en lista de definicion."""
    filas, resto = [], []
    for l in cabecera.split("\n"):
        m = re.match(r"^\*\*(.+?):\*\*\s*(.*?)\s*$", l.strip())
        if m and not l.strip().startswith("# "):
            filas.append(f"<dt>{_linea(m.group(1))}</dt><dd>{_linea(m.group(2).rstrip())}</dd>")
        else:
            resto.append(l)
    return "".join(filas), "\n".join(resto)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada")
    ap.add_argument("salida")
    ap.add_argument("--datos", default=None)
    ap.add_argument("--compromisos", default=None,
                    help="el .json que señala dónde se habló de un compromiso")
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
    ficha, _ = ficha_desde(cabecera)

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
            contenido, bloques = construir_bloques(doc, marcas, d.get("ventanas"), gana,
                                                   d.get("etiquetas"),
                                                   compromisos_de(a.compromisos))
            contenido = bloque_voces(d) + contenido
            n_hall = None
            tipo = "Transcripción · superficie de trabajo"
        datos["bloques"] = bloques
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
                 ("{{DATOS}}", json.dumps(datos, ensure_ascii=False))):
        out = out.replace(k, v)

    io.open(a.salida, "w", encoding="utf-8").write(out)
    print("OK  %s  -  %.1f KB%s" % (os.path.basename(a.salida), len(out) / 1024,
                                    "  (interactiva)" if a.datos else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
