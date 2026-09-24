# -*- coding: utf-8 -*-
"""genoma_de_voz — quién dice cada línea, con la huella de cada voz y la última palabra de ella.

    python genoma_de_voz.py preparar --par A1 <datos.json> <audio> [--par A2 <datos> <audio> ...]
                                     --titulo "<reunión>" --salida <carpeta>
                                     [--personas <declaracion.json> ...] [--biblioteca <json>]

    python genoma_de_voz.py aplicar  <genoma.json> <voces declaradas.json> --salida <carpeta>
                                     [--biblioteca <json>] [--word]

    python genoma_de_voz.py pagina   <genoma.json> --salida <carpeta>

`preparar` saca de cada línea de la transcripción su HUELLA DE VOZ —un vector de
512 números que calcula el mismo modelo que ya usa el arnés, `wespeaker-voxceleb-
CAMPP.onnx`—, propone unas voces agrupando las huellas, y escribe una página donde
ella oye cada línea y dice quién habla. Todas las grabaciones de una misma reunión
van JUNTAS: la misma persona es la misma voz en el Audio 1 y en el Audio 3.

`aplicar` toma lo que ella exportó de esa página y produce la transcripción con
quién dijo cada línea, el registro de su declaración, y la biblioteca de voces que
servirá en la reunión siguiente.

`pagina` rehace SOLO la página de un genoma ya preparado, con la plantilla de
ahora. No vuelve a oír nada ni a calcular huellas: cuando se arregla la página,
lo que ella ya declaró sigue valiendo, porque la clave no cambia.

POR QUE EXISTE. Medido el 2026-09-23 sobre una mesa de trabajo real de tres
grabaciones: la separación de voces del arnés le atribuía al Audio 1 el 96,5 % de
lo dicho a UN solo hablante, con al menos tres personas en la sala. No era un
umbral mal puesto: el agrupamiento automático no aguanta ese material. Pero la
huella SI distingue —las dos mitades de un mismo turno se parecen 0,96, dos turnos
distintos 0,75—. Lo que falla es decidir sin nadie que oiga. Este programa pone la
huella delante de quien oye, y aprende de lo que ella decide.

TRES COSAS MEDIDAS QUE ESTE PROGRAMA RESPETA:

  1. La huella DEPENDE DEL LARGO del trozo: una línea entera se parecía a su propia
     mitad 0,82 y las dos mitades entre sí 0,93, lo que es físicamente absurdo.
     Por eso todo se mide en ventanas fijas de 1,5 s y cada línea es la media de
     sus ventanas. Con eso la coherencia de las mitades pasó del 53 % al 82 %.
  2. El 19-34 % de los turnos SE PISAN: dos personas hablando a la vez. Esas
     líneas se marcan y no entran en la huella de nadie.
  3. Un número no es una decisión. Lo que la máquina propone nunca se escribe como
     lo que ella declaró: en la página se ve distinto, en la salida lleva otra
     marca, y la biblioteca de voces se construye SOLO con lo declarado.

LO QUE NO HACE: no nombra a nadie —el nombre lo pone ella—, no toca el audio ni la
transcripción original, y nunca sobrescribe un archivo (ADR-011 §8).
"""
import argparse, base64, datetime, hashlib, html, io, json, os, re, shutil, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
PLANTILLA = os.path.join(AQUI, "plantilla", "voces.html")
MODELO = os.path.join(AQUI, "modelos", "wespeaker-voxceleb-CAMPP.onnx")
VERSION = "1.0"

VENT, SALTO = 1.5, 0.75       # ventana fija: la huella se desplaza con el largo
UMBRAL_GRUPO = 0.25           # distancia coseno, enlace promedio. Medido: 0,25
                              # parte de más; 0,35 funde. Unir es un clic;
                              # separar obliga a revisar todo: se prefiere partir.
FIABLE_S, PISA_MAX = 1.5, 0.30
CORTA_S = 1.0
MIN_VOZ_S = 20.0
HUECO_S = 3.0
DIM_ADN = 32
META_CLARIDAD = 0.85
PRECISION_MINIMA, REVISIONES_MINIMAS = 0.90, 8
# Lo que exporta la pagina. NO es "despacho/voces-declaradas": ese nombre ya lo
# usa nombrar_voces con otra estructura, y con el mismo nombre cada programa
# aceptaria el archivo del otro y lo leeria mal sin avisar.
FORMATO_DECLARACION = "despacho/voces-linea-a-linea"


def falla(msg):
    sys.stderr.write("\nDETENIDO: %s\n" % msg)
    raise SystemExit(2)


def hms(s):
    s = max(0, int(float(s or 0)))
    return "%02d:%02d:%02d" % (s // 3600, (s % 3600) // 60, s % 60)


def duracion(s):
    s = int(round(float(s or 0)))
    return "%d min %02d s" % (s // 60, s % 60) if s >= 60 else "%d s" % s


def hoy():
    return datetime.date.today().isoformat()


def cargar(ruta, que):
    if not os.path.isfile(ruta):
        falla("no está %s: %s" % (que, ruta))
    try:
        with io.open(ruta, encoding="utf-8") as f:
            return json.load(f)
    except ValueError:
        falla("%s no es JSON legible: %s" % (que, ruta))


def _escribir(ruta, texto):
    with io.open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)


def _json(obj):
    """numpy se cuela en los datos (un bool, un float): se pasa a Python."""
    for tipo in ("item",):
        if hasattr(obj, tipo):
            return obj.item()
    raise TypeError("no se puede escribir %r en JSON" % type(obj).__name__)


def seguro(nombre):
    return re.sub(r'[\\/:*?"<>|]', "", nombre).strip()


def nuevo(ruta):
    """ADR-011 §8: regenerar produce versión nueva. Nunca se pisa nada."""
    if os.path.exists(ruta):
        falla("ya existe %s. Regenerar produce versión nueva, nunca sobrescribe "
              "(ADR-011 §8): muévalo o cambie --salida." % ruta)
    return ruta


# ---------------------------------------------------------------- huellas ---

class Huellas(object):
    """El extractor de huellas, y la regla de las ventanas fijas."""

    def __init__(self):
        try:
            import numpy as np
            import sherpa_onnx as so
        except ImportError as e:
            falla("falta una biblioteca: %s. Instálela con: pip install sherpa-onnx numpy"
                  % e.name)
        if not os.path.isfile(MODELO):
            falla("falta el modelo de huellas de voz en %s. Es el mismo que usa "
                  "transcribir_audio para separar voces." % MODELO)
        self.np = np
        self.ext = so.SpeakerEmbeddingExtractor(
            so.SpeakerEmbeddingExtractorConfig(model=MODELO, num_threads=6))
        self.dim = self.ext.dim

    def _uno(self, x, sr, a, b):
        np = self.np
        trozo = np.ascontiguousarray(x[max(0, int(a * sr)):max(0, int(b * sr))])
        if trozo.size < int(0.5 * sr):
            return None
        s = self.ext.create_stream()
        s.accept_waveform(sample_rate=sr, waveform=trozo)
        s.input_finished()
        if not self.ext.is_ready(s):
            return None
        e = np.asarray(self.ext.compute(s), dtype=np.float32)
        return e / (np.linalg.norm(e) + 1e-9)

    def ventanas(self, x, sr, a, b):
        """[(t, vector)] de ventanas de VENT s. Un tramo más corto que una ventana
        toma contexto a los dos lados: es la única forma de medirlo a la misma
        escala que los demás, y por eso esas líneas se marcan como cortas."""
        dur_total = x.size / float(sr)
        if b - a <= VENT:
            lo = max(0.0, min((a + b) / 2 - VENT / 2, dur_total - VENT))
            v = self._uno(x, sr, lo, lo + VENT)
            return [(lo, v)] if v is not None else []
        out, t = [], a
        while t + VENT <= b + 1e-6:
            v = self._uno(x, sr, t, t + VENT)
            if v is not None:
                out.append((t, v))
            t += SALTO
        if out and out[-1][0] + VENT < b - 0.3:
            v = self._uno(x, sr, b - VENT, b)
            if v is not None:
                out.append((b - VENT, v))
        return out

    def media(self, vs):
        np = self.np
        m = np.mean(vs, axis=0)
        return m / (np.linalg.norm(m) + 1e-9)


def aglomerar(np, V, umbral):
    """Enlace promedio sobre distancia coseno, en numpy (aquí no hay scipy)."""
    n = len(V)
    if n == 0:
        return np.zeros(0, int)
    M = (V @ V.T).astype(np.float64)
    np.fill_diagonal(M, -np.inf)
    tam = np.ones(n)
    grupos = {i: [i] for i in range(n)}
    while len(grupos) > 1:
        idx = int(np.argmax(M))
        a, b = divmod(idx, n)
        if M[a, b] < 1.0 - umbral:
            break
        nueva = (M[a] * tam[a] + M[b] * tam[b]) / (tam[a] + tam[b])
        M[a, :] = nueva
        M[:, a] = nueva
        M[a, a] = -np.inf
        M[b, :] = -np.inf
        M[:, b] = -np.inf
        tam[a] += tam[b]
        grupos[a].extend(grupos.pop(b))
    et = np.empty(n, int)
    for k, (_, miembros) in enumerate(sorted(grupos.items(), key=lambda kv: -len(kv[1]))):
        et[miembros] = k
    return et


def b64_int8(np, v, escala=None):
    """Un vector a int8 en base64. Para el coseno solo importa la dirección."""
    v = np.asarray(v, dtype=np.float32)
    m = escala if escala else (float(np.max(np.abs(v))) or 1.0)
    q = np.clip(np.round(v / m * 127.0), -127, 127).astype(np.int8)
    return base64.b64encode(q.tobytes()).decode("ascii")


def de_b64(np, s):
    return np.frombuffer(base64.b64decode(s), dtype=np.int8).astype(np.float32)


def solape(a, b, turnos):
    """Fracción de la línea en que la diarización oye a dos o más a la vez. La
    segmentación de pyannote detecta bien el habla simultánea aunque agrupe mal."""
    act = [(max(a, t["inicio"]), min(b, t["fin"])) for t in turnos
           if min(b, t["fin"]) > max(a, t["inicio"])]
    if len(act) < 2 or b <= a:
        return 0.0
    pasos = max(int((b - a) * 20), 2)
    n = 0
    for k in range(pasos):
        p = a + (b - a) * (k + 0.5) / pasos
        if sum(1 for lo, hi in act if lo <= p < hi) >= 2:
            n += 1
    return n / float(pasos)


def cambio_en_linea(H, np, vens, palabras, ini):
    """¿Cambia la voz dentro de la línea? Busca el corte que más separa las dos
    partes. Devuelve (parecido, t, indice_palabra, vec_a, vec_b) o None."""
    if len(vens) < 4:
        return None
    mejor = None
    for k in range(2, len(vens) - 1):
        a = H.media([v for _, v in vens[:k]])
        b = H.media([v for _, v in vens[k:]])
        s = float(a @ b)
        if mejor is None or s < mejor[0]:
            t = vens[k][0] + VENT / 2 - SALTO / 2
            mejor = (s, t, a, b)
    s, t, a, b = mejor
    # Se lleva al borde de palabra más cercano, para poder partir el texto.
    k = None
    if palabras:
        k = min(range(len(palabras)), key=lambda i: abs(float(palabras[i]["i"]) - t))
        if k == 0:
            k = 1 if len(palabras) > 1 else None
        if k is not None:
            t = float(palabras[k]["i"])
    return s, t, k, a, b


# ---------------------------------------------------------------- preparar ---

def _ruta_relativa(ruta, desde):
    """La grabacion vista desde la pagina. En Windows, si esta en OTRA unidad
    no hay ruta relativa posible (relpath revienta): se da la ruta completa."""
    try:
        return os.path.relpath(ruta, desde).replace("\\", "/")
    except ValueError:
        return "file:///" + os.path.abspath(ruta).replace("\\", "/")


def _personas(rutas):
    out, vistos = [], set()
    for r in rutas or []:
        d = cargar(r, "la declaración de personas")
        quien = (d.get("declarado_por") or "").strip() or "alguien sin identificar"
        cuando = ((d.get("fecha") or d.get("exportado") or "").strip()[:10]) or "sin fecha"
        for _, info in sorted((d.get("voces") or {}).items()):
            if info.get("fusionada_en"):
                continue
            nombre = (info.get("nombre") or info.get("quien") or "").strip()
            if not nombre or nombre.lower() in vistos:
                continue
            vistos.add(nombre.lower())
            out.append({"nombre": nombre, "cargo": (info.get("cargo") or "").strip(),
                        "fuente": "Declarado por %s el %s, sobre otra separación de "
                                  "voces. Sirve para no escribir el nombre; no dice "
                                  "quién habla cada línea." % (quien, cuando)})
    return out


def _biblioteca(ruta):
    if not ruta or not os.path.isfile(ruta):
        return []
    d = cargar(ruta, "la biblioteca de voces")
    if d.get("formato") != "despacho/biblioteca-de-voces":
        falla("%s no es una biblioteca de voces" % ruta)
    return d.get("voces") or []


def _numpy():
    try:
        import numpy
        return numpy
    except ImportError:
        falla("falta una biblioteca: numpy. Instálela con: pip install numpy")


# ---------------------------------------------------------------- rescate ---
#
# Medido el 2026-09-23: 38 huecos de mas de 3 s sin una sola linea publicada
# -- 6 min 18 s de reunion --, y 27 con forma de habla. En el mayor, el canal
# derecho tenia 51 palabras que la pasada publicada no trae. El arnes publica
# UNA lectura entera por grabacion; donde esa calla, lo que otra oyo se pierde.
#
# El rescate vuelve a oir SOLO esos huecos, cada pista por separado, y mide
# cuanto coinciden. Nada de lo rescatado entra en ninguna salida si ella no
# dice, oyendolo, que se dijo.

PISTAS_RESCATE = (("mezcla", "Lectura de los dos canales mezclados"),
                  ("izq", "Lectura del canal izquierdo"),
                  ("der", "Lectura del canal derecho"))
MARGEN_RESCATE = 0.4
# Frases que el reconocedor escribe sobre ruido o silencio. No se borran: se
# marcan, porque tambien podrian haberse dicho.
# La misma palabra cuatro veces seguidas: el reconocedor se engancho.
BUCLE = re.compile(r"(\b[\w¿?¡!]+\b)(?:\W+\1\b){3,}", re.IGNORECASE)
INVENCIONES = ("subtítulos", "subtitulos", "amara.org", "suscríbete", "suscribete",
               "gracias por ver", "gracias por su atención", "¡gracias!")


def _similitud(a, b):
    import difflib
    na = re.sub(r"[^\wáéíóúüñ ]", " ", (a or "").lower()).split()
    nb = re.sub(r"[^\wáéíóúüñ ]", " ", (b or "").lower()).split()
    if not na or not nb:
        return 0.0
    return difflib.SequenceMatcher(None, na, nb).ratio()


def _modelo_whisper():
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        falla("falta una biblioteca: faster-whisper. Sin ella no se puede rescatar: "
              "corra preparar sin --rescatar, o instálela con: pip install faster-whisper")
    for disp, ct in (("cuda", "int8_float16"), ("cpu", "int8")):
        try:
            return WhisperModel("large-v3", device=disp, compute_type=ct, local_files_only=True), disp
        except Exception:
            continue
    falla("no se pudo cargar el modelo large-v3 en local (ni en GPU ni en CPU). "
          "Corra preparar sin --rescatar.")


def _oir_tramo(mod, x, sr, a, b):
    """Una lectura del tramo [a, b]. Sin filtro de silencio: el hueco existe
    precisamente porque ese filtro, o el reconocedor, lo dieron por vacio."""
    trozo = x[max(0, int(a * sr)):int(b * sr)]
    if trozo.size < sr // 2:
        return "", []
    segs, _ = mod.transcribe(trozo, language="es", beam_size=5, best_of=5,
                             temperature=[0.0, 0.2, 0.4], condition_on_previous_text=False,
                             no_speech_threshold=0.6, log_prob_threshold=-1.0,
                             compression_ratio_threshold=2.4, word_timestamps=True,
                             vad_filter=False)
    textos, palabras = [], []
    for s in segs:
        if s.no_speech_prob > 0.8 or s.avg_logprob < -1.2:
            continue
        textos.append(s.text.strip())
        for w in (s.words or []):
            palabras.append({"p": w.word.strip(), "i": round(a + w.start, 2), "f": round(a + w.end, 2)})
    return " ".join(x for x in textos if x).strip(), palabras


def rescatar(huecos_por_audio, senales, H, np):
    """[(audio, ini, fin, texto, lecturas, acuerdo, invencion, vec)] de los huecos
    donde alguna pista oyo algo."""
    mod, disp = _modelo_whisper()
    print("\nRescate: se vuelven a oír %d huecos, pista por pista (%s)"
          % (sum(len(v) for v in huecos_por_audio.values()), "GPU" if disp == "cuda" else "CPU, más lento"))
    out = []
    for ident, huecos in huecos_por_audio.items():
        sen = senales[ident]
        sr = sen["sr"]
        for (h0, h1) in huecos:
            a = max(0.0, h0 - MARGEN_RESCATE)
            b = min(sen["dur"], h1 + MARGEN_RESCATE)
            lecturas, pals = [], {}
            for clave, fuente in PISTAS_RESCATE:
                x = sen.get(clave)
                if x is None:
                    continue
                txt, pw = _oir_tramo(mod, x, sr, a, b)
                lecturas.append({"fuente": fuente, "texto": txt})
                pals[clave] = pw
            con = [l for l in lecturas if l["texto"]]
            if not con:
                continue
            # La lectura que mas se parece a las otras (la mediana), no la mas larga.
            def media_parecido(l):
                otras = [o for o in lecturas if o is not l]
                return sum(_similitud(l["texto"], o["texto"]) for o in otras) / max(len(otras), 1)
            mejor = max(con, key=lambda l: (media_parecido(l), len(l["texto"])))
            acuerdo = media_parecido(mejor)
            clave_mejor = next(k for k, f in PISTAS_RESCATE if f == mejor["fuente"])
            pw = pals.get(clave_mejor) or []
            ini = max(h0, pw[0]["i"]) if pw else h0
            fin = min(h1, pw[-1]["f"]) if pw else h1
            if fin - ini < 0.3:
                ini, fin = h0, h1
            vens = H.ventanas(sen["mezcla"], sr, ini, fin)
            if not vens:
                continue
            bajo = mejor["texto"].lower()
            # «Gracias.» a secas es LA invencion del reconocedor sobre silencio:
            # que las tres pistas la «oigan» no prueba nada, porque las tres
            # inventan lo mismo sobre el mismo ruido.
            inv = (any(frase in bajo for frase in INVENCIONES)
                   or re.sub(r"[^a-záéíóúñ ]", "", bajo).strip() in ("gracias", "gracias gracias"))
            out.append((ident, round(ini, 2), round(fin, 2), mejor["texto"], lecturas,
                        round(acuerdo, 3), inv, H.media([w for _, w in vens]),
                        sum(1 for l in lecturas if l["texto"])))
    del mod
    print("   %d tramos con algo oído" % len(out))
    return out


def preparar(a):
    np = _numpy()
    sys.path.insert(0, AQUI)
    try:
        import transcribir_audio as TA
    except ImportError as e:
        falla("no se pudo cargar transcribir_audio: %s" % e)
    try:
        from md2html import _alternativas, fuente_visible
    except ImportError:
        _alternativas, fuente_visible = None, (lambda k: k)

    if not a.par:
        falla("hace falta al menos un --par <id> <datos.json> <audio>")
    if not os.path.isdir(a.salida):
        os.makedirs(a.salida)
    fecha = hoy()
    base = "%s - %s" % (seguro(a.titulo), fecha)
    ruta_html = nuevo(os.path.join(a.salida, "Voces - %s.html" % base))
    ruta_json = nuevo(os.path.join(a.salida, "genoma - %s.json" % base))
    if not os.path.isfile(PLANTILLA):
        falla("falta la plantilla compilada de la página en %s. Se compila en "
              "tools/pagina-voces con: npm run publicar" % PLANTILLA)

    if a.rescatar:
        try:
            import faster_whisper  # noqa: F401
        except ImportError:
            falla("--rescatar necesita faster-whisper y no está. Corra sin --rescatar, "
                  "o instálela con: pip install faster-whisper")
    H = Huellas()
    print("\nHuellas de voz con %s (%d números por huella)" % (os.path.basename(MODELO), H.dim))

    audios, lineas, huecos = [], [], []
    vecs, fiables = [], []
    senales, huecos_por_audio = {}, {}
    sin_huella = []
    for ident, ruta_datos, ruta_audio in a.par:
        d = cargar(ruta_datos, "el archivo de datos de %s" % ident)
        pub = d.get("publicada") or {}
        seg = pub.get("segmentos") or []
        if not seg:
            falla("%s no trae segmentos publicados" % ruta_datos)
        if not os.path.isfile(ruta_audio):
            falla("no está el audio de %s: %s" % (ident, ruta_audio))
        turnos = (d.get("voces") or {}).get("turnos") or []
        marcas = d.get("marcas") or {}
        ventanas20 = d.get("ventanas") or []
        gana = pub.get("etiqueta") or ""
        x = TA.decodificar(ruta_audio)
        if isinstance(x, tuple):
            x = x[0]
        x = np.asarray(x, dtype=np.float32)
        sr = TA.SR
        dur = x.size / float(sr)
        if a.rescatar:
            sen = {"mezcla": x, "sr": sr, "dur": dur}
            try:
                l_, r_ = TA.decodificar(ruta_audio, estereo=True)
                if l_ is not None and r_ is not None:
                    l_ = np.asarray(l_, dtype=np.float32)
                    r_ = np.asarray(r_, dtype=np.float32)
                    distintos, _ = TA.canales_distintos(l_, r_)
                    if distintos:
                        sen["izq"], sen["der"] = l_, r_
            except Exception:
                pass
            senales[ident] = sen
        nombre = "Audio %s" % re.sub(r"\D", "", ident) if re.search(r"\d", ident) else ident
        audios.append({"id": ident, "nombre": nombre,
                       "ruta": _ruta_relativa(ruta_audio, a.salida),
                       "archivo": os.path.basename(ruta_audio), "duracion": round(dur, 2)})

        n0 = len(lineas)
        for g in seg:
            ini, fin = float(g["inicio"]), float(g["fin"])
            vens = H.ventanas(x, sr, ini, fin)
            if not vens:
                sin_huella.append({"id": "%s-%d" % (ident, g["i"]), "audio": ident,
                                   "ini": round(ini, 2), "fin": round(fin, 2),
                                   "texto": g.get("texto", "").strip()})
                continue
            v = H.media([w for _, w in vens])
            pisa = solape(ini, fin, turnos)
            palabras = g.get("palabras") or []
            li = {"id": "%s-%d" % (ident, g["i"]), "audio": ident, "i": g["i"],
                  "ini": round(ini, 2), "fin": round(fin, 2), "texto": g.get("texto", "").strip(),
                  "pisa": round(pisa, 2), "corta": (fin - ini) < CORTA_S,
                  "dudas": [m for m in (marcas.get(str(g["i"])) or [])
                            if m not in ("voz dudosa",)]}
            ch = cambio_en_linea(H, np, vens, palabras, ini)
            if ch is not None:
                li["_cambio"] = ch
                li["_palabras"] = palabras
            if _alternativas:
                alts, _ = _alternativas(ventanas20, ini, gana)
                if alts:
                    li["alternativas"] = alts
            lineas.append(li)
            vecs.append(v)
            fiables.append((fin - ini) >= FIABLE_S and pisa < PISA_MAX)

        # Huecos: tramos sin ninguna línea publicada. Se dice que existen y, si
        # otra lectura escribió algo en una ventana ENTERA dentro del hueco, se
        # enseña. Solo ventanas enteras: una de 20 s sobre un hueco de 3 s
        # "hereda" el texto de alrededor, y ese error ya se cometió una vez.
        prev = 0.0
        tramos = []
        for g in seg:
            if g["inicio"] - prev > HUECO_S:
                tramos.append((prev, g["inicio"]))
            prev = max(prev, g["fin"])
        if dur - prev > HUECO_S:
            tramos.append((prev, dur))
        for (h0, h1) in tramos:
            otras = []
            for w in ventanas20:
                if w["t"] >= h0 and w["t"] + TA.VENTANA <= h1:
                    for k, t in (w.get("textos") or {}).items():
                        if t and t.strip() and k != gana.split("/")[-1] and k != gana:
                            otras.append({"fuente": fuente_visible(k), "desde": w["t"],
                                          "hasta": w["t"] + TA.VENTANA, "texto": t.strip()[:400]})
            huecos.append({"audio": ident, "ini": round(h0, 2), "fin": round(h1, 2),
                           "otras": otras})
            huecos_por_audio.setdefault(ident, []).append((h0, h1))
        print("  %-4s %4d líneas · %s · %d huecos de más de %.0f s"
              % (ident, len(lineas) - n0, hms(dur), len(tramos), HUECO_S))

    rescatados = rescatar(huecos_por_audio, senales, H, np) if a.rescatar else []
    senales.clear()

    V = np.stack(vecs)
    fiables = np.array(fiables)
    idx = np.where(fiables)[0]
    if len(idx) < 4:
        falla("hay menos de cuatro líneas largas y limpias: no alcanza para proponer voces")

    # Propuesta inicial de voces: SOLO con lineas fiables.
    et = aglomerar(np, V[idx], UMBRAL_GRUPO)
    durs = np.array([l["fin"] - l["ini"] for l in lineas])
    peso = {}
    for e, j in zip(et, idx):
        peso[e] = peso.get(e, 0.0) + durs[j]
    grandes = [e for e in sorted(peso, key=lambda e: -peso[e]) if peso[e] >= MIN_VOZ_S]
    if not grandes:
        grandes = [max(peso, key=peso.get)]
    C = np.stack([V[idx][et == e].mean(0) for e in grandes])
    C /= np.linalg.norm(C, axis=1, keepdims=True)
    S = V @ C.T
    orden = np.argsort(-S, axis=1)
    best = S[np.arange(len(V)), orden[:, 0]]
    # Con una sola voz no hay con que comparar: margen 0 (seguridad baja).
    margen = (best - S[np.arange(len(V)), orden[:, 1]]) if C.shape[0] > 1 else best * 0
    mf = margen[fiables]
    bandas = {"alta": round(float(np.percentile(mf, 50)), 4),
              "media": round(float(np.percentile(mf, 25)), 4)}

    # Umbral de cambio de voz dentro de una línea, medido en ESTA reunión: el
    # 5 % más bajo de los cortes de las líneas largas y limpias. Casi nadie se
    # releva a mitad de línea, así que eso es lo raro.
    cortes = [l["_cambio"][0] for l, f in zip(lineas, fiables) if "_cambio" in l and f]
    umbral_cambio = float(np.percentile(cortes, 5)) if len(cortes) >= 20 else 0.60
    umbral_cambio = min(umbral_cambio, 0.75)

    # ADN: las 32 direcciones en que más varían las huellas de ESTA reunión.
    mu = V.mean(0)
    U, s_, Wt = np.linalg.svd(V - mu, full_matrices=False)
    P = (V - mu) @ Wt[:DIM_ADN].T
    escala_adn = float(np.percentile(np.abs(P), 99)) or 1.0
    xy = P[:, :2] / (np.abs(P[:, :2]).max(0) + 1e-9)

    voces = []
    for k, e in enumerate(grandes):
        miembros = [j for j in range(len(V)) if orden[j, 0] == k]
        tipicas = sorted([j for j in miembros if fiables[j]],
                         key=lambda j: -(S[j, k] * min(durs[j], 6.0)))[:6]
        voces.append({"id": "v%d" % (k + 1), "etiqueta": "Voz %d" % (k + 1),
                      "vec": b64_int8(np, C[k]),
                      "tipicas": [lineas[j]["id"] for j in tipicas]})

    # Biblioteca de otras reuniones: SUGIERE, nunca asigna.
    for ent in _biblioteca(a.biblioteca):
        try:
            bv = de_b64(np, ent["vec"])
        except Exception:
            continue
        bv /= (np.linalg.norm(bv) + 1e-9)
        sims = C @ bv
        k = int(np.argmax(sims))
        if sims[k] >= 0.80:
            voces[k].setdefault("biblioteca", []).append(
                {"nombre": ent.get("nombre", ""), "cargo": ent.get("cargo", ""),
                 "parecido": round(float(sims[k]), 3),
                 "fuente": "Declarado por %s el %s en «%s»" % (
                     ent.get("declarado_por", "?"), ent.get("fecha", "?"), ent.get("origen", "?"))})

    n_cambio = 0
    for j, l in enumerate(lineas):
        l["vec"] = b64_int8(np, V[j])
        l["adn"] = b64_int8(np, P[j], escala_adn)
        l["xy"] = [round(float(xy[j, 0]), 3), round(float(xy[j, 1]), 3)]
        l["voz"] = voces[int(orden[j, 0])]["id"]
        l["parecido"] = round(float(best[j]), 3)
        l["margen"] = round(float(margen[j]), 3)
        ch = l.pop("_cambio", None)
        palabras = l.pop("_palabras", None)
        partes = _partir_texto(palabras, ch[2]) if ch is not None else None
        if ch is not None and ch[0] < umbral_cambio and partes:
            n_cambio += 1
            l["cambio"] = {"parecido": round(ch[0], 3), "en": round(ch[1], 2),
                           "palabra": ch[2], "vec_a": b64_int8(np, ch[3]),
                           "vec_b": b64_int8(np, ch[4])}
            l["partes"] = partes

    rescates = []
    for k, (ident, ini, fin, texto, lecturas, acuerdo, inv, v, n_oye) in enumerate(rescatados):
        s = C @ v
        o = np.argsort(-s)
        mg = float(s[o[0]] - s[o[1]]) if len(o) > 1 else 1.0
        pr = (v - mu) @ Wt[:DIM_ADN].T
        xy_r = pr[:2] / (np.abs(P[:, :2]).max(0) + 1e-9)
        rescates.append({
            "id": "%s-r%d" % (ident, k), "audio": ident, "ini": ini, "fin": fin,
            "texto": texto, "rescate": True, "lecturas": lecturas, "acuerdo": acuerdo,
            "oyen": n_oye, "invencion": bool(inv),
            "bucle": any(BUCLE.search(l["texto"] or "") for l in lecturas),
            "vec": b64_int8(np, v), "adn": b64_int8(np, pr, escala_adn),
            "xy": [round(float(np.clip(xy_r[0], -1, 1)), 3), round(float(np.clip(xy_r[1], -1, 1)), 3)],
            "voz": voces[int(o[0])]["id"], "parecido": round(float(s[o[0]]), 3), "margen": round(mg, 3),
            "pisa": 0.0, "corta": (fin - ini) < CORTA_S, "dudas": [],
        })

    clave = hashlib.sha256()
    clave.update(a.titulo.encode("utf-8"))
    for l in lineas + rescates:
        clave.update(("%s|%.2f|%.2f|%s\n" % (l["id"], l["ini"], l["fin"], l["vec"])).encode("utf-8"))

    datos = {
        "formato": "despacho/genoma-de-voz", "version": 1, "generador": "genoma_de_voz %s" % VERSION,
        "clave": clave.hexdigest()[:16], "titulo": a.titulo, "generado": fecha,
        "modelo": {"huella": os.path.basename(MODELO), "dim": int(H.dim),
                   "ventana_s": VENT, "salto_s": SALTO, "umbral_grupo": UMBRAL_GRUPO},
        "calibracion": {"bandas": bandas, "cambio": round(umbral_cambio, 3),
                        "precision_minima": PRECISION_MINIMA,
                        "revisiones_minimas": REVISIONES_MINIMAS,
                        "fiable_s": FIABLE_S, "pisa_max": PISA_MAX, "corta_s": CORTA_S},
        "meta_claridad": META_CLARIDAD,
        "audios": audios, "voces": voces, "lineas": lineas, "huecos": huecos,
        "rescates": rescates,
        "sin_huella": sin_huella,
        "personas_conocidas": _personas(a.personas),
    }

    _escribir(ruta_json, 
        json.dumps(datos, ensure_ascii=False, separators=(",", ":"), default=_json))
    with io.open(PLANTILLA, encoding="utf-8") as f:
        plantilla = f.read()
    incrustado = json.dumps(datos, ensure_ascii=False, separators=(",", ":"), default=_json).replace("</", "<\\/")
    if "{{DATOS}}" not in plantilla:
        falla("la plantilla %s no tiene el hueco {{DATOS}}" % PLANTILLA)
    out = plantilla.replace("{{TITULO}}", html.escape(a.titulo)).replace("{{DATOS}}", incrustado)
    _escribir(ruta_html, out)

    # Resumen para quien lo corre.
    tot = float(durs.sum())
    print()
    print("Voces propuestas (agrupamiento automático, SIN nombre y SIN confirmar):")
    for k, v in enumerate(voces):
        seg_v = float(durs[orden[:, 0] == k].sum())
        extra = ""
        if v.get("biblioteca"):
            extra = "  · se parece a «%s» de la biblioteca (%.0f %%)" % (
                v["biblioteca"][0]["nombre"], 100 * v["biblioteca"][0]["parecido"])
        print("   %-7s %5.1f %% del habla%s" % (v["etiqueta"], 100 * seg_v / tot, extra))
    alta = durs[margen >= bandas["alta"]].sum() / tot
    print()
    print("Líneas: %d · se pisan: %d · cortas: %d · con posible cambio de voz: %d"
          % (len(lineas), sum(1 for l in lineas if l["pisa"] >= PISA_MAX),
             sum(1 for l in lineas if l["corta"]), n_cambio))
    print("Huecos sin transcribir: %d (%s en total), %d con texto en otra lectura"
          % (len(huecos), hms(sum(h["fin"] - h["ini"] for h in huecos)),
             sum(1 for h in huecos if h["otras"])))
    if a.rescatar:
        print("Rescatados: %d tramos con algo oído en los huecos (%d los oyen dos pistas o más; "
              "%d parecen invención del reconocedor). NADIE los ha oído: ella decide."
              % (len(rescates), sum(1 for r in rescates if r["oyen"] >= 2),
                 sum(1 for r in rescates if r["invencion"])))
    print("Seguridad alta de la máquina: %.0f %% del habla — SIN MEDIR: se mide con lo "
          "que ella revise." % (100 * alta))
    print("Claridad declarada hoy: 0 %%. La meta es el %.0f %%." % (100 * META_CLARIDAD))
    print()
    print("OK  %s  (%.0f KB)" % (os.path.basename(ruta_html), os.path.getsize(ruta_html) / 1024))
    print("OK  %s" % os.path.basename(ruta_json))
    return 0


def _partir_texto(palabras, k):
    """El texto de la línea partido en la palabra k, con las palabras que traen
    su tiempo. Si no hay dónde partir, no se parte."""
    if not palabras or k is None or k <= 0 or k >= len(palabras):
        return None
    a = "".join(w["p"] if w["p"].startswith(" ") else " " + w["p"] for w in palabras[:k]).strip()
    b = "".join(w["p"] if w["p"].startswith(" ") else " " + w["p"] for w in palabras[k:]).strip()
    return [a, b] if a and b else None


# ------------------------------------------------------------------ aplicar ---

MARCA = {"declarada": "✔", "propuesta": "≈", "sin": "?"}
SIN_OIR = " _(sin oír)_"
DESCARTES = ("descartado", "no_se_dijo")


def _quien(voces_decl, vid, genoma_voces):
    info = voces_decl.get(vid) or {}
    vistos = set()
    while info.get("fusionada_en") and vid not in vistos:
        vistos.add(vid)
        vid = info["fusionada_en"]
        info = voces_decl.get(vid) or {}
    nombre = (info.get("nombre") or "").strip()
    cargo = (info.get("cargo") or "").strip()
    etiqueta = next((v["etiqueta"] for v in genoma_voces if v["id"] == vid), None)
    if etiqueta is None:
        # Las personas nuevas se llaman igual aqui que en la pagina.
        etiqueta = ("Persona nueva %s" % str(vid)[1:]) if str(vid).startswith("n") else str(vid)
    return vid, nombre, cargo, etiqueta


def _rotulo(nombre, cargo, etiqueta):
    if nombre:
        return nombre + (" · " + cargo if cargo else "")
    return etiqueta + " (sin nombre)"


def _oyendo(dc):
    """Lo decidido sin oir es de ella, pero no es una declaracion OYENDO."""
    return bool(dc) and dc.get("oida") is not False


def _clara(dc):
    """La MISMA regla que la pagina (genoma.js, esClara): oida, y si es
    «varios», con al menos dos voces."""
    if not _oyendo(dc):
        return False
    if dc.get("decision") in ("confirmada", "corregida"):
        return True
    if dc.get("decision") == "varios":
        return len(dc.get("voces") or []) >= 2
    return False


def pagina(a):
    """Rehace la página con la plantilla ACTUAL a partir del genoma ya preparado.

    Pasó el 2026-09-24: la página no avisaba cuando se abría desde dentro de un
    .zip, y la abogada no oía nada. Arreglada la plantilla, había que llevarla a
    la reunión ya preparada, y `preparar` vuelve a calcular todas las huellas en
    la GPU (y los rescates, con otra pasada del reconocedor). Aquí se escribe la
    página exactamente como la escribe `preparar` —los mismos datos, la misma
    clave—, así que lo que ella haya declarado sobre la versión anterior se carga
    igual. El nombre lleva la fecha de la preparación, no la de hoy: los enlaces
    de otras páginas a esta siguen llegando. Nunca sobrescribe (ADR-011 §8)."""
    try:
        with io.open(a.genoma, encoding="utf-8") as f:
            datos = json.loads(f.read())
    except (OSError, ValueError) as e:
        falla("no se pudo leer el genoma %s: %s" % (a.genoma, e))
    if not isinstance(datos, dict) or datos.get("formato") != "despacho/genoma-de-voz":
        falla("%s no es un genoma de voz (formato despacho/genoma-de-voz)" % a.genoma)
    for k in ("titulo", "clave", "audios", "lineas"):
        if k not in datos:
            falla("al genoma %s le falta «%s»: no se puede rehacer la página" % (a.genoma, k))
    if not os.path.isfile(PLANTILLA):
        falla("falta la plantilla compilada de la página en %s. Se compila en "
              "tools/pagina-voces con: npm run publicar" % PLANTILLA)
    with io.open(PLANTILLA, encoding="utf-8") as f:
        plantilla = f.read()
    if "{{DATOS}}" not in plantilla:
        falla("la plantilla %s no tiene el hueco {{DATOS}}" % PLANTILLA)
    if not os.path.isdir(a.salida):
        os.makedirs(a.salida)
    base = "%s - %s" % (seguro(datos["titulo"]), datos.get("generado") or hoy())
    ruta_html = nuevo(os.path.join(a.salida, "Voces - %s.html" % base))
    incrustado = json.dumps(datos, ensure_ascii=False, separators=(",", ":"), default=_json).replace("</", "<\\/")
    out = plantilla.replace("{{TITULO}}", html.escape(datos["titulo"])).replace("{{DATOS}}", incrustado)
    _escribir(ruta_html, out)
    print("OK  %s  -  %d líneas, %d grabaciones, clave %s (la misma: lo ya declarado sigue valiendo)"
          % (os.path.basename(ruta_html), len(datos["lineas"]), len(datos["audios"]), datos["clave"]))
    return 0


def aplicar(a):
    np = _numpy()
    g = cargar(a.genoma, "el genoma")
    d = cargar(a.declaracion, "la declaración exportada")
    if g.get("formato") != "despacho/genoma-de-voz":
        falla("%s no es un genoma de voz" % a.genoma)
    if d.get("formato") != FORMATO_DECLARACION:
        falla("%s no es una exportación de la página de voces (formato %r, se esperaba %r)"
              % (a.declaracion, d.get("formato"), FORMATO_DECLARACION))
    if d.get("clave") != g.get("clave"):
        falla("esa declaración es de OTRA preparación (clave %s, se esperaba %s). "
              "Úsela con el genoma que generó la página donde se hizo."
              % (d.get("clave"), g.get("clave")))
    quien = (d.get("declarado_por") or "").strip()
    if not quien:
        falla("la declaración no dice quién la hizo («declarado_por»). Sin eso no "
              "hay declaración: es una propuesta sin autor.")
    fecha = (d.get("exportado") or hoy())[:10]
    decl_voces = d.get("voces") or {}
    for vid in decl_voces:
        cadena = [vid]
        while (decl_voces.get(cadena[-1]) or {}).get("fusionada_en"):
            sig = decl_voces[cadena[-1]]["fusionada_en"]
            if sig in cadena:
                falla("la declaración fusiona voces en círculo (%s): no dice quién es "
                      "quién. Corríjalo en la página y exporte otra vez."
                      % " -> ".join(cadena + [sig]))
            cadena.append(sig)
    decis = d.get("lineas") or {}
    maquina = d.get("maquina") or {}
    if not os.path.isdir(a.salida):
        os.makedirs(a.salida)
    base = "%s - %s" % (seguro(g["titulo"]), hoy())

    # El acierto de la maquina se RECALCULA aqui, desde las decisiones: la
    # pagina escribe un resumen, pero un resumen no es prueba (SPEC-15 §5).
    # Y SOLO con las lineas SORTEADAS para la prueba y OIDAS: las elegidas a
    # mano o por ser tipicas sesgan, y un Enter sin oir no prueba nada.
    cal = g["calibracion"]
    rev = [dc for dc in decis.values()
           if dc.get("banda_maquina") == "alta" and dc.get("propuesta_maquina")
           and dc.get("origen") == "prueba" and _oyendo(dc) and not dc.get("rescate")]
    acierto = sum(1 for dc in rev if dc.get("decision") == "confirmada" and not dc.get("partes"))
    maquina_cuenta = (len(rev) >= cal["revisiones_minimas"]
                      and acierto >= cal["precision_minima"] * len(rev))

    def banda_de(l, mq):
        if l.get("corta") or l.get("pisa", 0) >= cal["pisa_max"]:
            return "baja"
        if mq.get("banda") in ("alta", "media", "baja"):
            return mq["banda"]
        m = l.get("margen", 0)
        return ("alta" if m >= cal["bandas"]["alta"] else
                "media" if m >= cal["bandas"]["media"] else "baja")

    rutas = {au["id"]: os.path.join(a.salida, "Transcripcion con voces - %s - %s.md" % (au["nombre"], hoy()))
             for au in g["audios"]}
    ruta_decl = os.path.join(a.salida, "Declaracion de voces - %s.md" % base)
    ruta_json = os.path.join(a.salida, "voces por linea - %s.json" % base)
    for r in list(rutas.values()) + [ruta_decl, ruta_json]:
        nuevo(r)

    salidas, por_linea = [], []
    claridad, de_ella, de_maq = {}, {}, {}
    corregidas, confirmadas = [], 0
    seg_decl = {}

    def sumar_decl(vid, s):
        seg_decl[vid] = seg_decl.get(vid, 0.0) + max(0.0, s)

    # Los rescates: tramos que la transcripcion no tenia. Entran SOLO los que
    # ella oyo y dijo que se dijeron, con el texto que ella dejo. No cuentan
    # en la claridad, que es de las lineas publicadas.
    rescates_si, cuenta_r = {}, {"descartados": 0, "sin_revisar": 0, "sin_texto": 0, "sin_oir": 0}
    for r in g.get("rescates") or []:
        dc = decis.get(r["id"])
        if not dc:
            cuenta_r["sin_revisar"] += 1
        elif dc.get("decision") in DESCARTES or dc.get("se_dijo") is False:
            cuenta_r["descartados"] += 1
        elif not (dc.get("texto") or "").strip():
            cuenta_r["sin_texto"] += 1
        elif not _oyendo(dc):
            cuenta_r["sin_oir"] += 1
        elif dc.get("decision") in ("confirmada", "corregida", "no_se_distingue"):
            rescates_si.setdefault(r["audio"], []).append((r, dc))

    for au in g["audios"]:
        ls = [l for l in g["lineas"] if l["audio"] == au["id"]]
        tot = sum(l["fin"] - l["ini"] for l in ls) or 1.0
        ella = maq = 0.0
        filas = []   # (minuto, orden, texto): los huecos, luego lo rescatado, luego la linea

        for h in g.get("huecos") or []:
            if h["audio"] == au["id"]:
                filas.append((h["ini"], 0, "_[%s] — %s sin transcribir —_" % (hms(h["ini"]), duracion(h["fin"] - h["ini"]))))

        for s_ in g.get("sin_huella") or []:
            if s_["audio"] == au["id"]:
                filas.append((s_["ini"], 2, "**[%s] %s Sin huella de voz: demasiado corta para reconocerla** %s"
                              % (hms(s_["ini"]), MARCA["sin"], s_["texto"])))

        for r, dcr in rescates_si.get(au["id"], []):
            texto = dcr["texto"].strip()
            cambio = " · texto corregido por ella" if texto != r["texto"].strip() else ""
            if dcr.get("decision") == "no_se_distingue":
                vid, rot, marca = None, "No se distingue quién", MARCA["sin"]
            else:
                vid, n, c, e = _quien(decl_voces, dcr.get("voz"), g["voces"])
                rot, marca = _rotulo(n, c, e), MARCA["declarada"]
                sumar_decl(vid, r["fin"] - r["ini"])
            filas.append((r["ini"], 1, "**[%s] %s %s** %s  _(rescatada: no estaba en la transcripción; "
                           "la oyó %s%s)_" % (hms(r["ini"]), marca, rot, texto, quien, cambio)))
            por_linea.append({"id": r["id"], "audio": au["id"], "ini": r["ini"], "fin": r["fin"],
                              "texto": texto, "decision": "rescatada", "voz": vid, "quien": rot,
                              "texto_maquina": r["texto"], "oida": True})

        for l in ls:
            dc = decis.get(l["id"])
            mq = maquina.get(l["id"]) or {"voz": l["voz"], "banda": ""}
            dur = l["fin"] - l["ini"]
            dud = "  `[?]` (%s)" % " · ".join(l["dudas"][:2]) if l.get("dudas") else ""
            sin = "" if (not dc or _oyendo(dc)) else SIN_OIR
            reg = {"id": l["id"], "audio": au["id"], "ini": l["ini"], "fin": l["fin"], "texto": l["texto"],
                   "oida": _oyendo(dc) if dc else None}
            credito_maquina = True
            if dc and dc.get("decision") in ("confirmada", "corregida"):
                if dc.get("partes") and l.get("partes"):
                    en = (l.get("cambio") or {}).get("en", l["ini"])
                    trozos = []
                    for k, (parte, txt) in enumerate(zip(dc["partes"], l["partes"])):
                        vid, n, c, e = _quien(decl_voces, parte["voz"], g["voces"])
                        t0 = l["ini"] if k == 0 else en
                        trozos.append((vid, _rotulo(n, c, e), txt))
                        filas.append((t0, 2, "**[%s] %s %s**%s %s%s" % (hms(t0), MARCA["declarada"], _rotulo(n, c, e), sin, txt, dud)))
                        if _oyendo(dc):
                            sumar_decl(vid, (en - l["ini"]) if k == 0 else (l["fin"] - en))
                    reg.update({"decision": "dividida", "partes": [
                        {"voz": vid, "quien": rot, "texto": txt} for vid, rot, txt in trozos]})
                else:
                    vid, n, c, e = _quien(decl_voces, dc["voz"], g["voces"])
                    filas.append((l["ini"], 2, "**[%s] %s %s**%s %s%s" % (hms(l["ini"]), MARCA["declarada"],
                                                                        _rotulo(n, c, e), sin, l["texto"], dud)))
                    reg.update({"decision": dc["decision"], "voz": vid, "quien": _rotulo(n, c, e)})
                    if _oyendo(dc):
                        sumar_decl(vid, dur)
                if dc["decision"] == "corregida":
                    corregidas.append((au["nombre"], l, dc))
                else:
                    confirmadas += 1
            elif dc and dc.get("decision") == "varios":
                vs = dc.get("voces") or []
                if len(vs) >= 2:
                    nombres = [_rotulo(*_quien(decl_voces, v, g["voces"])[1:]) for v in vs]
                    rot = "Varios a la vez: " + " y ".join(nombres)
                    filas.append((l["ini"], 2, "**[%s] %s %s**%s %s%s" % (hms(l["ini"]), MARCA["declarada"], rot, sin, l["texto"], dud)))
                else:
                    rot = "Varios a la vez, sin distinguir quiénes"
                    filas.append((l["ini"], 2, "**[%s] %s %s** %s%s" % (hms(l["ini"]), MARCA["sin"], rot, l["texto"], dud)))
                reg.update({"decision": "varios", "voces": vs, "quien": rot})
                credito_maquina = False
            elif dc and dc.get("decision") == "no_se_distingue":
                filas.append((l["ini"], 2, "**[%s] %s No se distingue quién habla** %s%s" % (hms(l["ini"]), MARCA["sin"], l["texto"], dud)))
                reg.update({"decision": "no_se_distingue"})
                credito_maquina = False
            else:
                vid, n, c, e = _quien(decl_voces, mq.get("voz") or l["voz"], g["voces"])
                banda = banda_de(l, mq)
                filas.append((l["ini"], 2, "**[%s] %s %s** _(propuesta de la máquina, seguridad %s; nadie lo ha oído)_ %s%s"
                              % (hms(l["ini"]), MARCA["propuesta"], _rotulo(n, c, e), banda, l["texto"], dud)))
                reg.update({"decision": "propuesta", "voz": vid, "quien": _rotulo(n, c, e), "banda": banda})
            # La claridad: lo que ella declaro oyendo; y si no, la maquina solo
            # si paso la prueba y la linea es de banda alta. Igual que la pagina.
            if _clara(dc):
                ella += dur
                reg["clara"] = "ella"
            elif credito_maquina and maquina_cuenta and banda_de(l, mq) == "alta":
                maq += dur
                reg["clara"] = "maquina"
            por_linea.append(reg)

        claridad[au["id"]] = (ella + maq) / tot
        de_ella[au["id"]], de_maq[au["id"]] = ella / tot, maq / tot
        filas.sort(key=lambda x: (x[0], x[1]))
        md = [
            "# Transcripción con voces — %s" % au["nombre"],
            "",
            "**%s** · `%s`" % (g["titulo"], au["archivo"]),
            "",
            "**Quién habla, según %s**, declarado el %s oyendo la grabación. "
            "La máquina propuso; ella decidió." % (quien, fecha),
            "",
            "| Marca | Qué significa |",
            "|---|---|",
            "| **✔** | Lo declaró %s oyendo esa línea. Si dice _(sin oír)_, lo decidió sin oírla: es suyo, pero no oyendo, y no cuenta para la claridad |" % quien,
            "| **≈** | Lo propone la máquina por el parecido de la voz. **Nadie lo ha oído**: no sirve para atribuir |",
            "| **?** | Ella marcó que no se distingue quién habla |",
            "",
            "**Claridad de las voces en esta grabación: %.0f %%** (meta: %.0f %%) — declarado por ella oyendo "
            "%.0f %%, propuesto por la máquina puesta a prueba %.0f %%." % (
                100 * claridad[au["id"]], 100 * g["meta_claridad"], 100 * de_ella[au["id"]], 100 * de_maq[au["id"]]),
            "",
            "---",
            "",
        ] + [f[2] + "\n" for f in filas]
        r = rutas[au["id"]]
        _escribir(r, "\n".join(md))
        salidas.append(r)

    # La declaración, como registro.
    filas_v = []
    for v in g["voces"]:
        info = decl_voces.get(v["id"]) or {}
        if info.get("fusionada_en"):
            continue
        filas_v.append("| %s | %s | %s | %s | %s |" % (
            v["etiqueta"], info.get("nombre") or "_sin nombre_", info.get("cargo") or "—",
            info.get("como_lo_sabe") or "—", duracion(seg_decl.get(v["id"], 0))))
    for vid, info in sorted(decl_voces.items()):
        if str(vid).startswith("n") and not info.get("fusionada_en"):
            filas_v.append("| %s | %s | %s | %s | %s |" % (
                _quien(decl_voces, vid, g["voces"])[3], info.get("nombre") or "_sin nombre_",
                info.get("cargo") or "—", info.get("como_lo_sabe") or "—", duracion(seg_decl.get(vid, 0))))
    fusiones = ["- %s se declaró la misma persona que %s" % (
        _quien({}, vid, g["voces"])[3],
        _rotulo(*_quien(decl_voces, info["fusionada_en"], g["voces"])[1:]))
        for vid, info in sorted(decl_voces.items()) if info.get("fusionada_en")]
    if not rev:
        prec = "sin medir: no revisó, oyéndola, ninguna de las líneas sorteadas para la prueba"
    else:
        prec = "acertó %d de %d líneas sorteadas y oídas (%.0f %%)" % (acierto, len(rev), 100.0 * acierto / len(rev))
        if not maquina_cuenta:
            prec += (". **No basta** para que sus propuestas cuenten como claras: hacen falta "
                     "%d revisiones y un acierto del %.0f %%, así que la claridad de abajo "
                     "es solo lo que ella declaró oyendo" % (cal["revisiones_minimas"], 100 * cal["precision_minima"]))
    pagina = (d.get("resumen") or {}).get("claridad") or {}
    distintas = ["%s: la página decía %.0f %%, aquí sale %.0f %%" % (
        au["nombre"], 100 * float(pagina[au["id"]]), 100 * claridad[au["id"]])
        for au in g["audios"] if au["id"] in pagina and abs(float(pagina[au["id"]]) - claridad[au["id"]]) > 0.01]
    md = [
        "# Declaración de voces — %s" % g["titulo"],
        "",
        "**Declarado por %s** el %s, oyendo las grabaciones en la página de voces." % (quien, fecha),
        "",
        "> La máquina propuso a partir del parecido de las voces. **Cada línea marcada ✔ la decidió "
        "%s**; si además dice _(sin oír)_, la decidió sin oírla. Lo marcado ≈ es propuesta y no sirve "
        "para atribuir una intervención en un acta." % quien,
        "",
        "## Quién es cada voz",
        "",
        "| Voz | Nombre | Cargo | Cómo lo sabe | Tiempo declarado oyendo |",
        "|---|---|---|---|---|",
    ] + filas_v + [""] + (["## Voces que resultaron ser la misma persona", ""] + fusiones + [""] if fusiones else []) + [
        "## Cuánto quedó claro",
        "",
        "| Grabación | Claridad | De ella, oyendo | De la máquina, puesta a prueba | Meta |",
        "|---|---|---|---|---|",
    ] + ["| %s | %.0f %% %s | %.0f %% | %.0f %% | %.0f %% |" % (
        au["nombre"], 100 * claridad[au["id"]],
        "✔" if claridad[au["id"]] >= g["meta_claridad"] else "— no llega",
        100 * de_ella[au["id"]], 100 * de_maq[au["id"]], 100 * g["meta_claridad"]) for au in g["audios"]] + [
        "",
    ]
    if distintas:
        md += ["> **La claridad se recalculó aquí y no coincide con la que mostraba la página:** "
               + "; ".join(distintas) + ". Vale la de esta tabla, recalculada desde sus decisiones.", ""]
    md += [
        "**Líneas confirmadas tal como las propuso la máquina:** %d. **Corregidas:** %d." % (confirmadas, len(corregidas)),
        "",
        "**Cuánto acertó la máquina en lo que daba por seguro**, según lo que %s revisó: %s." % (quien, prec),
        "",
    ]
    if g.get("rescates"):
        md += ["**Tramos que la transcripción no tenía, oídos otra vez:** %d aceptados por %s oyéndolos, "
               "%d descartados, %d sin revisar%s. Solo los aceptados están en la transcripción." % (
                   sum(len(v) for v in rescates_si.values()), quien, cuenta_r["descartados"], cuenta_r["sin_revisar"],
                   (", %d sin texto y %d sin oír (no entran)" % (cuenta_r["sin_texto"], cuenta_r["sin_oir"]))
                   if cuenta_r["sin_texto"] or cuenta_r["sin_oir"] else ""), ""]
    sin_oir = sum(1 for dc in decis.values() if dc.get("oida") is False)
    if sin_oir:
        md += ["**%d de %d decisiones se tomaron sin oír la línea** en la página. Son suyas, pero no "
               "«oyendo»: no cuentan para la claridad, no alimentan la biblioteca de voces, y en la "
               "transcripción llevan _(sin oír)_." % (sin_oir, len(decis)), ""]
    incompletas = []
    for v in list(g["voces"]) + [{"id": k, "etiqueta": _quien(decl_voces, k, g["voces"])[3]}
                                 for k in decl_voces if str(k).startswith("n")]:
        info = decl_voces.get(v["id"]) or {}
        if info.get("fusionada_en") or not seg_decl.get(v["id"]):
            continue
        falta = [x for x, k in (("nombre", "nombre"), ("cargo o entidad", "cargo"), ("cómo lo sabe", "como_lo_sabe"))
                 if not (info.get(k) or "").strip()]
        if falta:
            incompletas.append("- %s: falta %s" % (info.get("nombre") or v["etiqueta"], ", ".join(falta)))
    md += ["## Para atribuir en un acta",
           "",
           "Una línea ✔ oída dice quién habla. Para que sostenga una atribución en un acta "
           "(`acta-de-reunion` §2.3, condición 7) hace falta además que esa voz tenga **nombre, "
           "cargo o entidad, y cómo lo sabe**, y que la línea no diga _(sin oír)_. " + (
               "A estas voces con líneas declaradas les falta algo:" if incompletas else
               "Todas las voces con líneas declaradas lo tienen."), ""] + incompletas + ([""] if incompletas else [])
    if corregidas:
        md += ["## Lo que la máquina proponía, y ella corrigió", "",
               "| Grabación | Minuto | Texto | La máquina proponía | Ella declaró |", "|---|---|---|---|---|"]
        for nom, l, dc in corregidas[:400]:
            # Lo que la maquina proponia CUANDO ella decidio, no la propuesta inicial.
            antes = _rotulo(*_quien(decl_voces, dc.get("propuesta_maquina") or l["voz"], g["voces"])[1:])
            if dc.get("partes"):
                ahora = "dividida: " + " / ".join(_rotulo(*_quien(decl_voces, p_["voz"], g["voces"])[1:]) for p_ in dc["partes"])
            else:
                ahora = _rotulo(*_quien(decl_voces, dc.get("voz"), g["voces"])[1:])
            md.append("| %s | %s | %s | %s | %s |" % (nom, hms(l["ini"]), l["texto"][:60].replace("|", "/"), antes, ahora))
        md.append("")
    md += ["---", "", "_Generado por `genoma_de_voz %s` a partir de `%s`. El original es la grabación._"
           % (VERSION, os.path.basename(a.declaracion))]
    _escribir(ruta_decl, "\n".join(md))
    salidas.append(ruta_decl)

    _escribir(ruta_json, json.dumps({
        "formato": "despacho/voces-por-linea", "version": 1, "titulo": g["titulo"],
        "declarado_por": quien, "fecha": fecha, "clave": g["clave"],
        "nota": "decision=confirmada|corregida|dividida|varios|rescatada: las declaró ella; "
                "oida=false: sin oír la línea. decision=propuesta es de la máquina y nadie lo ha oído. "
                "clara=ella|maquina: por qué cuenta para la claridad.",
        "claridad": {k: round(v, 4) for k, v in claridad.items()},
        "de_ella": {k: round(v, 4) for k, v in de_ella.items()},
        "de_la_maquina": {k: round(v, 4) for k, v in de_maq.items()},
        "lineas": por_linea}, ensure_ascii=False, indent=1))
    salidas.append(ruta_json)

    if a.biblioteca:
        _actualizar_biblioteca(np, a.biblioteca, g, decis, decl_voces, quien, fecha)

    if a.word:
        md2docx = os.path.join(AQUI, "md2docx.py")
        import subprocess
        for s in [x for x in salidas if x.endswith(".md")]:
            subprocess.call([sys.executable, md2docx, s, s[:-3] + ".docx"])

    print()
    for s in salidas:
        print("OK  %s" % os.path.basename(s))
    for au in g["audios"]:
        c = claridad[au["id"]]
        print("   %-8s claridad %3.0f %% (de ella %3.0f %%, de la máquina %3.0f %%)  %s" % (
            au["nombre"], 100 * c, 100 * de_ella[au["id"]], 100 * de_maq[au["id"]],
            "✔" if c >= g["meta_claridad"] else "(no llega al %.0f %%)" % (100 * g["meta_claridad"])))
    return 0


def _actualizar_biblioteca(np, ruta, g, decis, decl_voces, quien, fecha):
    """La huella de cada persona NOMBRADA, hecha SOLO con líneas que ella
    declaró. Nunca con propuestas de la máquina: una biblioteca que se alimenta
    de sus propias conjeturas acaba creyéndoselas."""
    lib = {"formato": "despacho/biblioteca-de-voces", "version": 1, "voces": []}
    if os.path.isfile(ruta):
        lib = cargar(ruta, "la biblioteca de voces")
        dest = os.path.join(os.path.dirname(ruta) or ".", "_anteriores")
        if not os.path.isdir(dest):
            os.makedirs(dest)
        raiz = "%s - %s" % (os.path.splitext(os.path.basename(ruta))[0],
                            datetime.datetime.now().strftime("%Y-%m-%d %H%M%S"))
        copia, n = os.path.join(dest, raiz + ".json"), 2
        while os.path.exists(copia):
            copia, n = os.path.join(dest, "%s (%d).json" % (raiz, n)), n + 1
        shutil.copy2(ruta, copia)
    vecs = {l["id"]: de_b64(np, l["vec"]) for l in g["lineas"]}
    lin = {l["id"]: l for l in g["lineas"]}
    cal = g["calibracion"]
    grupos = {}
    for lid, dc in decis.items():
        if dc.get("decision") not in ("confirmada", "corregida") or not dc.get("voz") or dc.get("partes"):
            continue
        if dc.get("oida") is False:
            continue            # decidida sin oir: no es la huella de nadie
        l = lin.get(lid) or {}
        if l.get("corta") or l.get("pisa", 0) >= cal["pisa_max"]:
            continue            # habla simultanea o casi nada de voz: no es la huella de nadie
        vid, nombre, cargo, _ = _quien(decl_voces, dc["voz"], g["voces"])
        if not nombre or lid not in vecs:
            continue
        v = vecs[lid] / (np.linalg.norm(vecs[lid]) + 1e-9)
        grupos.setdefault((nombre, cargo), []).append(v)
    n = 0
    ya = 0
    for (nombre, cargo), vs in grupos.items():
        if len(vs) < 3:
            continue
        previa = next((e for e in lib["voces"] if e.get("nombre", "").lower() == nombre.lower()), None)
        if previa and any(h.get("clave") == g["clave"] for h in previa.get("historial") or []):
            ya += 1
            continue
        m = np.mean(vs, axis=0)
        m /= np.linalg.norm(m) + 1e-9
        ent = next((e for e in lib["voces"] if e.get("nombre", "").lower() == nombre.lower()), None)
        if ent:
            viejo = de_b64(np, ent["vec"])
            viejo /= np.linalg.norm(viejo) + 1e-9
            k = int(ent.get("lineas", 0))
            m = (viejo * k + m * len(vs))
            m /= np.linalg.norm(m) + 1e-9
            ent.update({"vec": b64_int8(np, m), "lineas": k + len(vs), "cargo": cargo or ent.get("cargo", "")})
            ent.setdefault("historial", []).append({"origen": g["titulo"], "fecha": fecha, "clave": g["clave"],
                                                    "declarado_por": quien, "lineas": len(vs)})
        else:
            lib["voces"].append({"nombre": nombre, "cargo": cargo, "vec": b64_int8(np, m),
                                 "lineas": len(vs), "declarado_por": quien, "fecha": fecha,
                                 "origen": g["titulo"], "modelo": g["modelo"]["huella"],
                                 "historial": [{"origen": g["titulo"], "fecha": fecha, "clave": g["clave"],
                                                "declarado_por": quien, "lineas": len(vs)}]})
        n += 1
    tmp = ruta + ".tmp"
    _escribir(tmp, json.dumps(lib, ensure_ascii=False, indent=1))
    os.replace(tmp, ruta)
    print("Biblioteca de voces: %d persona(s) actualizada(s) con lo declarado -> %s" % (n, ruta))
    if ya:
        print("   %d persona(s) ya tenían esta misma declaración: no se cuenta dos veces" % ya)


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="orden")
    p = sub.add_parser("preparar", help="huellas, voces propuestas y la página")
    p.add_argument("--par", nargs=3, action="append", metavar=("ID", "DATOS", "AUDIO"))
    p.add_argument("--titulo", required=True)
    p.add_argument("--salida", required=True)
    p.add_argument("--personas", action="append", help="declaración previa, solo para ofrecer nombres")
    p.add_argument("--biblioteca", help="biblioteca de voces de otras reuniones")
    p.add_argument("--rescatar", action="store_true",
                   help="vuelve a oír solo los huecos sin transcribir, pista por pista (necesita faster-whisper)")
    q = sub.add_parser("aplicar", help="lo que ella declaró -> transcripción con voces")
    q.add_argument("genoma")
    q.add_argument("declaracion")
    q.add_argument("--salida", required=True)
    q.add_argument("--biblioteca")
    q.add_argument("--word", action="store_true")
    g = sub.add_parser("pagina", help="rehace solo la página de un genoma ya preparado, con la plantilla de ahora")
    g.add_argument("genoma")
    g.add_argument("--salida", required=True)
    a = ap.parse_args(argv)
    if a.orden == "preparar":
        return preparar(a)
    if a.orden == "aplicar":
        return aplicar(a)
    if a.orden == "pagina":
        return pagina(a)
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
