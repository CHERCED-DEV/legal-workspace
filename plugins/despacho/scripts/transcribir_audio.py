# -*- coding: utf-8 -*-
"""
transcribir_audio — grabaciones a texto citable, sin que el audio salga del computador.

    python transcribir_audio.py <audios o carpeta...> --destino "<ruta>"

Opciones:
    --sin-voces        no separa hablantes
    --sin-glosario     no hace la pasada que senala nombres propios
    --pasadas N        decodificaciones neutrales (2 a 4; por defecto 4)
    --glosario "a, b"  terminos del caso para la pasada de avisos
    --dispositivo cpu  fuerza CPU (por defecto usa la GPU si esta disponible)

Que hace, en orden: decodifica, diagnostica la senal, limpia de forma conservadora,
decodifica varias veces con distintas condiciones, publica la que mas coincide con
las demas, separa voces sin nombrarlas, y escribe la transcripcion, los subtitulos,
el registro de metodo y la lista de minutos donde conviene oir.

Requiere: faster-whisper, av, numpy. Opcional: sherpa-onnx (voces).
Si algo falta, lo dice y no supone nada.
"""
import argparse, datetime, difflib, json, math, os, re, sys, time, unicodedata, wave

SR = 16000
VENTANA, UMBRAL_ACUERDO = 20.0, 0.80
UMBRAL_PALABRA, UMBRAL_NOVOZ, UMBRAL_COMPRESION, UMBRAL_LOGPROB = 0.45, 0.50, 2.20, -0.65
UMBRAL_PUREZA_VOZ, UMBRAL_VOCES, MAX_SEGMENTO = 0.60, 0.90, 18.0
EXT = (".mp3", ".mp4", ".m4a", ".wav", ".ogg", ".opus", ".aac", ".flac", ".wma", ".mkv", ".mov", ".webm")
MODELOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modelos")
# Que decodificaciones se hacen, y sobre que pista. El orden es de mas valiosa
# a menos: si se piden menos pasadas, se quedan las primeras.
#
# Con dos canales distintos se prefiere UN CANAL sobre otra cuantizacion, porque
# dos microfonos no comparten punto ciego acustico y dos cuantizaciones si.
PASADAS_ESTEREO = [
    ("mezcla_f16",  "mezcla_limpio", "float16"),
    ("der_int8",    "der_limpio",    "int8_float16"),
    ("izq_int8",    "izq_limpio",    "int8_float16"),
    ("crudo_int8",  "mezcla_crudo",  "int8_float16"),
]
PASADAS_MONO = [
    ("limpio_f16",  "mezcla_limpio", "float16"),
    ("crudo_int8",  "mezcla_crudo",  "int8_float16"),
    ("limpio_int8", "mezcla_limpio", "int8_float16"),
    ("crudo_f16",   "mezcla_crudo",  "float16"),
]


def aviso(*a):
    print(*a, flush=True)


# ------------------------------------------------------------------ utilidades
def hms(s, ms=False):
    seg = float(s)
    h, r = divmod(int(seg), 3600)
    m, sg = divmod(r, 60)
    return "%02d:%02d:%02d" % (h, m, sg) + (",%03d" % int((seg % 1) * 1000) if ms else "")


def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]+", " ", t).split()


def num(x, dec=0):
    s = "%.*f" % (dec, float(x))
    neg = s.startswith("-")
    ent, _, d = s.lstrip("-").partition(".")
    return ("-" if neg else "") + format(int(ent), ",").replace(",", ".") + ("," + d if d else "")


def db(x):
    return float("-inf") if x <= 0 else 20.0 * math.log10(x)


# ------------------------------------------------------------------ audio
def decodificar(ruta, estereo=False):
    """Devuelve mono, o (izquierdo, derecho) si se pide estereo y lo hay.

    Por que importa el estereo: mezclar los dos canales a mono PROMEDIA dos
    capturas distintas de la sala hasta convertirlas en una. Medido sobre
    material real: los canales coinciden entre si menos que dos decodificaciones
    del mismo mono (0,650 frente a 0,737 en la peor grabacion), y la mezcla
    pierde cientos de palabras que un canal si produce. Dos microfonos son una
    redundancia mas fuerte que dos cuantizaciones: no comparten punto ciego
    acustico.
    """
    import av
    import numpy as np
    cont = av.open(ruta)
    st = next((s for s in cont.streams if s.type == "audio"), None)
    if st is None:
        cont.close()
        raise RuntimeError("el archivo no tiene pista de audio")
    st.thread_type = "AUTO"
    layout = "stereo" if estereo else "mono"
    res = av.audio.resampler.AudioResampler(format="fltp", layout=layout, rate=SR)
    izq, der = [], []
    for f in list(cont.decode(st)) + [None]:
        for g in res.resample(f):
            a = g.to_ndarray()
            if estereo and a.shape[0] >= 2:
                izq.append(a[0].copy().astype(np.float32))
                der.append(a[1].copy().astype(np.float32))
            else:
                izq.append(a.reshape(-1).astype(np.float32))
    cont.close()
    if not izq:
        return (np.zeros(0, np.float32), np.zeros(0, np.float32)) if estereo else np.zeros(0, np.float32)
    l = np.concatenate(izq)
    if not estereo:
        return l
    if not der:
        return l, l
    r = np.concatenate(der)
    n = min(len(l), len(r))
    return l[:n], r[:n]


def canales_distintos(l, r, umbral=0.98):
    """¿Vale la pena tratarlos por separado, o es mono duplicado?"""
    import numpy as np
    n = min(len(l), len(r), SR * 120)
    if n < SR:
        return False, 1.0
    c = float(np.corrcoef(l[:n], r[:n])[0, 1])
    return (c < umbral), round(c, 4)


def diagnostico(x):
    import numpy as np
    v = int(0.02 * SR)
    m = (len(x) // v) * v
    rms = np.sqrt((x[:m].reshape(-1, v).astype(np.float64) ** 2).mean(axis=1) + 1e-20)
    piso, voz = float(np.percentile(rms, 10)), float(np.percentile(rms, 90))
    return {"duracion_s": round(len(x) / SR, 2), "pico_dbfs": round(db(float(np.abs(x).max())), 2),
            "muestras_saturadas": int((np.abs(x) >= 0.999).sum()),
            "piso_ruido_dbfs": round(db(piso), 2), "nivel_voz_dbfs": round(db(voz), 2),
            "snr_estimada_db": round(db(voz) - db(piso), 2)}


def pasa_altos(x, corte=75.0, tr=25.0):
    import numpy as np
    n = len(x)
    N = 1 << (n - 1).bit_length()
    X = np.fft.rfft(x, N)
    fr = np.fft.rfftfreq(N, 1.0 / SR)
    g = np.ones_like(fr)
    g[fr <= corte - tr] = 0.0
    b = (fr > corte - tr) & (fr < corte + tr)
    g[b] = 0.5 - 0.5 * np.cos(math.pi * (fr[b] - (corte - tr)) / (2 * tr))
    return np.fft.irfft(X * g, N)[:n].astype(np.float32)


def resta_espectral(x, nfft=1024, salto=256, sobre=1.0, suelo_db=-12.0):
    """Suelo espectral: ninguna banda se atenua mas de `suelo_db`. Limpiar de mas borra habla."""
    import numpy as np
    vent = np.hanning(nfft).astype(np.float32)
    xs = np.concatenate([np.zeros(nfft, np.float32), x, np.zeros(nfft * 2, np.float32)])
    idx = range(0, len(xs) - nfft, salto)
    E = np.stack([np.fft.rfft(xs[i:i + nfft] * vent) for i in idx])
    mag, fase = np.abs(E), np.angle(E)
    ruido = np.percentile(mag, 10, axis=0)
    g = np.maximum((mag - sobre * ruido) / (mag + 1e-12), 10 ** (suelo_db / 20.0))
    Y = g * mag * np.exp(1j * fase)
    sal, nor = np.zeros(len(xs), np.float32), np.zeros(len(xs), np.float32)
    for k, i in enumerate(idx):
        sal[i:i + nfft] += np.fft.irfft(Y[k], nfft).astype(np.float32) * vent
        nor[i:i + nfft] += vent ** 2
    return (sal / np.maximum(nor, 1e-8))[nfft:nfft + len(x)].astype(np.float32)


def normalizar(x, rms_db=-23.0, pico_db=-1.0):
    import numpy as np
    r = float(np.sqrt((x.astype(np.float64) ** 2).mean()) + 1e-20)
    y = x * (10 ** (rms_db / 20.0) / r)
    p, lim = float(np.abs(y).max()), 10 ** (pico_db / 20.0)
    return (y * (lim / p) if p > lim else y).astype(np.float32)


def escribir_wav(ruta, x):
    import numpy as np
    with wave.open(ruta, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767.0).astype("<i2").tobytes())


def leer_wav(ruta):
    import numpy as np
    with wave.open(ruta, "rb") as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32768.0


def limpiar(x):
    y = x - float(x.mean())
    return normalizar(resta_espectral(pasa_altos(y)))


def preparar(ruta, destinos):
    """Escribe las pistas que pidan las pasadas. Si la grabacion trae dos canales
    distintos, se conservan por separado: promediarlos pierde informacion."""
    import numpy as np
    l, r = decodificar(ruta, estereo=True)
    hay_dos, corr = canales_distintos(l, r)
    mezcla = (l + r) / 2.0 if hay_dos else l
    # El diagnostico del ORIGEN se hace sobre los canales, no sobre la mezcla:
    # promediar dos canales baja el pico y puede esconder un recorte que SI
    # estaba en la grabacion. Un registro que oculta un defecto del origen no
    # sirve para nada.
    antes = diagnostico(l if not hay_dos else np.maximum(np.abs(l), np.abs(r)) * np.sign(l + r + 1e-12))
    if hay_dos:
        dl, dr = diagnostico(l), diagnostico(r)
        antes["muestras_saturadas"] = dl["muestras_saturadas"] + dr["muestras_saturadas"]
        antes["pico_dbfs"] = max(dl["pico_dbfs"], dr["pico_dbfs"])
        antes["snr_estimada_db"] = min(dl["snr_estimada_db"], dr["snr_estimada_db"])
        antes["por_canal"] = {"izq": dl, "der": dr}
    pistas = {
        "mezcla_limpio": limpiar(mezcla),
        "mezcla_crudo": normalizar(mezcla - float(mezcla.mean())),
    }
    if hay_dos:
        pistas["izq_limpio"] = limpiar(l)
        pistas["der_limpio"] = limpiar(r)
    for nombre, ruta_salida in destinos.items():
        if nombre in pistas:
            escribir_wav(ruta_salida, pistas[nombre])
    return {"original": antes, "limpio": diagnostico(pistas["mezcla_limpio"]),
            "estereo_util": hay_dos, "correlacion_canales": corr,
            "pistas": [k for k in pistas]}


# ------------------------------------------------------------------ reconocimiento
def parametros(glosario=None):
    from faster_whisper.vad import VadOptions
    return dict(language="es", beam_size=5, best_of=5, patience=1,
                temperature=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
                compression_ratio_threshold=2.4, log_prob_threshold=-1.0, no_speech_threshold=0.6,
                condition_on_previous_text=False, initial_prompt=None,
                hotwords=glosario or None, word_timestamps=True,
                hallucination_silence_threshold=2.0, vad_filter=True,
                vad_parameters=VadOptions(threshold=0.35, min_speech_duration_ms=0,
                                          min_silence_duration_ms=700, speech_pad_ms=400))


def transcribir(mod, x, etiqueta, glosario=None):
    t0 = time.time()
    segs, info = mod.transcribe(x, **parametros(glosario))
    out, ult = [], 0.0
    for s in segs:
        out.append({"i": s.id, "inicio": round(s.start, 3), "fin": round(s.end, 3),
                    "texto": s.text.strip(), "logprob": round(s.avg_logprob, 4),
                    "no_voz": round(s.no_speech_prob, 4), "compresion": round(s.compression_ratio, 3),
                    "temperatura": s.temperature,
                    "palabras": [{"p": w.word.strip(), "i": round(w.start, 3), "f": round(w.end, 3),
                                  "c": round(w.probability, 4)} for w in (s.words or [])]})
        if s.end - ult >= 180:
            ult = s.end
            aviso("    %s  %.1f min (%.0fs)" % (etiqueta, s.end / 60, time.time() - t0))
    return {"etiqueta": etiqueta, "modelo": "large-v3", "glosario": bool(glosario),
            "duracion_s": round(len(x) / SR, 2),
            "duracion_tras_vad_s": round(info.duration_after_vad, 2),
            "segundos_computo": round(time.time() - t0, 1), "segmentos": out}


def diarizar(x):
    import sherpa_onnx as so
    seg = os.path.join(MODELOS, "pyannote-segmentation-3-0.onnx")
    emb = os.path.join(MODELOS, "wespeaker-voxceleb-CAMPP.onnx")
    for p in (seg, emb):
        if not os.path.exists(p):
            raise RuntimeError("falta el modelo %s (ver modelos/PROCEDENCIA.md)" % os.path.basename(p))
    cfg = so.OfflineSpeakerDiarizationConfig(
        segmentation=so.OfflineSpeakerSegmentationModelConfig(
            pyannote=so.OfflineSpeakerSegmentationPyannoteModelConfig(model=seg)),
        embedding=so.SpeakerEmbeddingExtractorConfig(model=emb),
        clustering=so.FastClusteringConfig(num_clusters=-1, threshold=UMBRAL_VOCES),
        min_duration_on=0.3, min_duration_off=0.5)
    if not cfg.validate():
        raise RuntimeError("configuracion de diarizacion invalida")
    res = so.OfflineSpeakerDiarization(cfg).process(x).sort_by_start_time()
    turnos = [{"inicio": round(s.start, 3), "fin": round(s.end, 3), "hablante": int(s.speaker)}
              for s in res]
    dur = {}
    for t in turnos:
        dur[t["hablante"]] = dur.get(t["hablante"], 0) + (t["fin"] - t["inicio"])
    return {"umbral": UMBRAL_VOCES, "turnos": turnos,
            "hablantes": {str(k): round(v, 2) for k, v in sorted(dur.items(), key=lambda kv: -kv[1])}}


# ------------------------------------------------------------------ consenso
def palabras_en(doc, a, b):
    out = []
    for s in doc["segmentos"]:
        if s["fin"] <= a or s["inicio"] >= b:
            continue
        if s["palabras"]:
            out += [w["p"] for w in s["palabras"] if a <= (w["i"] + w["f"]) / 2 < b]
        elif a <= (s["inicio"] + s["fin"]) / 2 < b:
            out.append(s["texto"])
    return " ".join(out)


def acuerdo(docs, dur):
    claves, vent, t = list(docs), [], 0.0
    while t < dur:
        tx = {k: palabras_en(docs[k], t, t + VENTANA) for k in claves}
        nz = {k: norm(v) for k, v in tx.items()}
        if any(nz.values()):
            por, suma, pares = {k: [] for k in claves}, 0.0, 0
            for i, a in enumerate(claves):
                for b in claves[i + 1:]:
                    r = difflib.SequenceMatcher(None, nz[a], nz[b]).ratio()
                    suma += r; pares += 1; por[a].append(r); por[b].append(r)
            vent.append({"t": t, "medio": suma / max(pares, 1), "textos": tx,
                         "por_pasada": {k: sum(v) / len(v) for k, v in por.items()} if pares else
                                       {k: 1.0 for k in claves}})
        t += VENTANA
    return vent


def dividir_largos(doc, maximo=MAX_SEGMENTO):
    salida = []
    for s in doc["segmentos"]:
        pal = s["palabras"]
        if (s["fin"] - s["inicio"]) <= maximo or len(pal) < 8:
            salida.append(s); continue
        trozos, act, ini = [], [], s["inicio"]
        for w in pal:
            act.append(w)
            if (w["p"].rstrip().endswith((".", "?", "!")) and w["f"] - ini >= 8.0) or w["f"] - ini >= maximo:
                trozos.append((ini, w["f"], act)); act, ini = [], w["f"]
        if act:
            trozos.append((ini, s["fin"], act))
        hijos = [dict(s, inicio=round(a, 3), fin=round(b, 3),
                      texto=" ".join(x["p"] for x in ws), palabras=ws) for a, b, ws in trozos]
        # solo se acepta el corte si no cambio ni una palabra
        if len(hijos) < 2 or norm(" ".join(h["texto"] for h in hijos)) != norm(s["texto"]):
            salida.append(s)
        else:
            salida.extend(hijos)
    for i, s in enumerate(salida):
        s["i"] = i
    doc["segmentos"] = salida
    return doc


def asignar_voces(doc, dia):
    orden = {int(k): i + 1 for i, k in enumerate(dia["hablantes"])}
    for s in doc["segmentos"]:
        sol = {}
        for t in dia["turnos"]:
            a, b = max(s["inicio"], t["inicio"]), min(s["fin"], t["fin"])
            if b > a:
                sol[t["hablante"]] = sol.get(t["hablante"], 0.0) + (b - a)
        if sol:
            h = max(sol, key=sol.get)
            s["voz"], s["pureza"] = orden.get(h, h), round(sol[h] / sum(sol.values()), 3)
        else:
            s["voz"], s["pureza"] = None, 0.0
    return doc


def avisos_glosario(pub, glos, terminos):
    """Donde la pasada con glosario escribio un termino del caso y la publicada no.

    ADR-017 §5: el minuto que se publica es el del SEGMENTO de la version
    publicada que contiene ese punto, no la marca de palabra.
    """
    pp = [w for s in pub["segmentos"] for w in s["palabras"]]
    pg = [w for s in glos["segmentos"] for w in s["palabras"]]

    def segmento_de(t):
        for s in pub["segmentos"]:
            if s["inicio"] <= t <= s["fin"]:
                return s["inicio"]
        anteriores = [s["inicio"] for s in pub["segmentos"] if s["inicio"] <= t]
        return anteriores[-1] if anteriores else (pub["segmentos"][0]["inicio"]
                                                  if pub["segmentos"] else 0.0)

    fin, vistos = [], set()
    for w in pg:
        nw = norm(w["p"])
        if not nw or nw[0] not in terminos:
            continue
        medio = (w["i"] + w["f"]) / 2
        cerca = [v for v in pp if abs((v["i"] + v["f"]) / 2 - medio) <= 2.5]
        if nw[0] in {norm(v["p"])[0] for v in cerca if norm(v["p"])}:
            continue
        k = (round(w["i"] / 30), nw[0])
        if k in vistos:
            continue
        vistos.add(k)
        fin.append({"t": segmento_de(medio), "sugiere": w["p"], "c": w["c"],
                    "dice_publicada": " ".join(v["p"] for v in cerca)[:90] or "(nada)"})
    return sorted(fin, key=lambda a: a["t"])


def marcar(s, malas, con_voces):
    m = []
    if s["logprob"] < UMBRAL_LOGPROB: m.append("confianza baja")
    if s["no_voz"] > UMBRAL_NOVOZ: m.append("puede no ser habla")
    if s["compresion"] > UMBRAL_COMPRESION: m.append("posible repeticion")
    if s["temperatura"] > 0: m.append("decodificacion forzada")
    if any(w["c"] < UMBRAL_PALABRA for w in s["palabras"]): m.append("palabra dudosa")
    if any(v <= s["inicio"] < v + VENTANA for v in malas): m.append("las pasadas no coinciden")
    if con_voces:
        if s.get("voz") is None: m.append("sin voz asignada")
        elif s["pureza"] < UMBRAL_PUREZA_VOZ: m.append("voz dudosa")
    return m


def riesgosas(doc):
    """Cifras y nombres propios de baja confianza.

    ADR-017 §5: ningun anclaje depende de la marca de palabra, porque el
    alineamiento por palabra falla justo en cifras y fechas en numeros. Por eso
    el localizador que se publica es **el minuto del segmento** que contiene la
    palabra, no el de la palabra. Quien va a comprobar, oye el segmento entero.
    """
    r = []
    for s in doc["segmentos"]:
        for k, w in enumerate(s["palabras"]):
            p = w["p"].strip(".,;:()[]¿?¡!\"'")
            if not p:
                continue
            cifra = bool(re.search(r"\d", p))
            prev = s["palabras"][k - 1]["p"].strip() if k else "."
            propio = p[:1].isupper() and k and not prev.endswith((".", "?", "!"))
            if (cifra or propio) and w["c"] < 0.85:
                r.append({"t": s["inicio"], "palabra": p, "c": w["c"],
                          "tipo": "cifra" if cifra else "nombre propio"})
    return sorted(r, key=lambda x: x["c"])


# ------------------------------------------------------------------ salidas
def escribir_transcripcion(ruta, doc, marcas, titulo, origen, gana, dia, hoy):
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("# TRANSCRIPCIÓN — %s\n\n" % titulo)
        f.write("**Archivo de origen:** `%s`  \n**Duración:** %s  \n" % (origen, hms(doc["duracion_s"])))
        f.write("**La produjo un programa, no una persona:** faster-whisper 1.2.1, modelo "
                "`large-v3`, el %s. Se decodificó varias veces y se publica la versión «%s», la que "
                "**más coincide con las demás** — no la que el modelo consideró más segura.  \n"
                % (hoy, gana))
        if dia:
            f.write("**Voces:** separadas automáticamente, **%d hablantes**, anónimos y numerados por "
                    "cuánto hablan. **«Hablante 1» no es una persona identificada: es una voz.**  \n"
                    % len(dia["hablantes"]))
        f.write("**Marca `[?]`:** hay un motivo para dudar de esa línea; va al final entre paréntesis.\n\n")
        f.write("> **Esta transcripción no es la grabación.** El original es el audio. Ninguna cita "
                "literal debería salir de aquí sin oír el minuto exacto.")
        f.write(" Y **que dos líneas lleven el mismo número de hablante no prueba que sea la misma "
                "persona**: es lo que estimó un programa.\n\n---\n\n" if dia else
                " Y **no se distinguen las voces**: ninguna línea está atribuida a nadie.\n\n---\n\n")
        ult = object()
        for s in doc["segmentos"]:
            mk = marcas[s["i"]]
            if dia:
                v = "Hablante %s" % s["voz"] if s["voz"] else "Hablante ?"
                cab = "**[%s] · %s**" % (hms(s["inicio"]), v) if s["voz"] != ult else "**[%s]**" % hms(s["inicio"])
                ult = s["voz"]
            else:
                cab = "**[%s]**" % hms(s["inicio"])
            f.write("%s %s%s\n\n" % (cab, s["texto"],
                                     "  `[?]` *(%s)*" % "; ".join(mk) if mk else ""))


def escribir_subtitulos(doc, srt, vtt):
    with open(srt, "w", encoding="utf-8") as f:
        for i, s in enumerate(doc["segmentos"], 1):
            f.write("%d\n%s --> %s\n%s\n\n" % (i, hms(s["inicio"], 1), hms(s["fin"], 1), s["texto"]))
    with open(vtt, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for s in doc["segmentos"]:
            f.write("%s --> %s\n%s\n\n" % (hms(s["inicio"], 1).replace(",", "."),
                                           hms(s["fin"], 1).replace(",", "."), s["texto"]))


NO_DICE = """```text
LO QUE ESTA TRANSCRIPCION NO DICE
- La transcripcion NO es la grabacion. Un dato decisivo se comprueba
  oyendo el minuto exacto, no leyendo aqui.
- Que algo NO aparezca aqui no significa que no se dijera. El
  reconocedor falla callandose, y lo que el detector de voz descarto
  no se midio: ese numero no existe y no puede existir.
- Que las pasadas coincidan NO prueba que el texto sea correcto:
  comparten modelo y comparten punto ciego. Que difieran SI prueba
  que ahi hay algo que revisar.
- Los nombres propios y las cifras son lo que peor sale.
- NO se ha leido el contenido ni se ha interpretado nada.
```"""

NO_DICE_VOCES = """```text
SOBRE LAS VOCES
- Los numeros de hablante son VOCES estimadas por un programa, NO
  personas identificadas. Que dos lineas lleven el mismo numero no
  prueba que las dijera la misma persona.
- NO hay verdad de referencia: nadie marco a mano quien habla, asi
  que no se sabe que porcentaje de las asignaciones es correcto.
- Ningun nombre propio sale de aqui asignado a una voz.
```"""


def escribir_registro(ruta, fichas, hoy, con_voces, con_glosario, pasadas=None):
    L = []; w = L.append
    w("# REGISTRO DE TRANSCRIPCIÓN\n")
    w("Escrito el %s. **Lo produjo un programa, no una persona.** Este registro existe para que "
      "usted pueda juzgar cuánto vale lo que hay en esta carpeta y para poder repetirlo.\n" % hoy)
    w("**Si el audio no dice en qué fecha se grabó, esta carpeta tampoco lo dice.** La fecha de "
      "arriba es la de la transcripción.\n")
    w("---\n")
    w("## 1. El material, y lo que traía mal de origen\n")
    w("| Grabación | Duración | Pico | Muestras saturadas | Señal / ruido |")
    w("|---|---|---|---|---|")
    for f in fichas:
        d = f["diag"]["original"]
        w("| %s | %s | %s dBFS | %s | %s dB |" % (f["titulo"], hms(d["duracion_s"]),
          num(d["pico_dbfs"], 2), num(d["muestras_saturadas"]), num(d["snr_estimada_db"], 2)))
    w("")
    sat = [f for f in fichas if f["diag"]["original"]["muestras_saturadas"] > 0]
    if sat:
        w("**%d de %d grabaciones vienen saturadas** (muestras recortadas contra el techo). Eso **no "
          "se puede reparar**: lo que el recorte borró no está en el archivo. La limpieza baja el "
          "nivel para que no vuelva a ocurrir, pero no devuelve lo perdido.\n" % (len(sat), len(fichas)))
    w("## 2. La receta\n")
    w("```")
    w("programa      faster-whisper 1.2.1 (CTranslate2)" + ("   ·   voces: sherpa-onnx" if con_voces else ""))
    w("modelo        Systran/faster-whisper-large-v3    (pesos locales, sin descarga)")
    if con_voces:
        w("modelo voces  pyannote-segmentation-3.0 + wespeaker VoxCeleb CAM++ (ONNX)")
    w("audio         16 kHz, decodificado con PyAV")
    if pasadas:
        w("pistas        " + ", ".join(sorted({u[1] for u in pasadas})))
        w("pasadas       " + ", ".join("%s (%s)" % (u[0], u[2]) for u in pasadas))
    w("limpieza      sin continua · pasa-altos 75 Hz fase lineal · resta espectral")
    w("              con suelo -12 dB · nivelado a -23 dBFS, tope -1 dBFS")
    w("idioma        es  (fijado a mano: NO se dejo detectar)")
    w("busqueda      beam_size=5  best_of=5   ·   SIN inferencia por lotes")
    w("contexto      condition_on_previous_text = FALSE")
    w("detector voz  Silero VAD, umbral 0.35, silencio 700 ms, margen 400 ms")
    if con_voces:
        w("agrupar voces umbral %.2f" % UMBRAL_VOCES)
    w("sugerencias   en las pasadas neutrales: initial_prompt=NINGUNO, hotwords=NINGUNA")
    w("```")
    w("Tres valores no son los de fábrica:\n")
    w("- **`condition_on_previous_text = FALSE`.** De fábrica el modelo se realimenta con lo que "
      "acaba de escribir, y en audio largo eso produce **bucles**: una frase se repite sola durante "
      "minutos con apariencia de texto normal.\n")
    w("- **Sin sugerencias al modelo en el texto publicado.** Sugerir un término hace que lo escriba "
      "**también donde no se dijo**, y ese acierto falso es indistinguible del verdadero.\n")
    w("- **Umbral del detector de voz en 0,35** en vez de 0,50: conserva habla dudosa a cambio de "
      "algo de ruido.\n")
    w("- **Sin inferencia por lotes.** Es varias veces más rápida, pero **pierde palabras y su "
      "confianza sube al hacerlo**: parece mejor porque transcribe menos.\n")
    w("## 3. La instrumentación\n")
    w("| Grabación | Publicada | Acuerdo entre pasadas | Tramos flojos | Habla detectada | Palabras |"
      + (" Voces |" if con_voces else ""))
    w("|---|---|---|---|---|---|" + ("---|" if con_voces else ""))
    for f in fichas:
        w("| %s | %s | %s %% | %s de %s | %s de %s | %s |%s" % (
            f["titulo"], f["gana"], num(100 * f["acuerdo_medio"], 1), num(len(f["malas"])),
            num(len(f["vent"])), hms(f["doc"].get("duracion_tras_vad_s", 0)),
            hms(f["doc"]["duracion_s"]), num(f["palabras"]),
            (" %s |" % num(len(f["dia"]["hablantes"]))) if con_voces and f.get("dia") else ""))
    w("")
    w("**Y lo que nada de esto mide:** cuánto habla real quedó del lado descartado. Ese número **no "
      "existe y no puede existir** — para conocerlo habría que saber ya lo que se dijo. La confianza "
      "mide la calidad de lo que se reconoció; **jamás la completitud de lo que se debió reconocer**.\n")
    if con_voces:
        # CC BY 4.0 obliga a dar credito. No es cortesia: es la condicion de la
        # licencia del modelo de voz. Ver modelos/PROCEDENCIA.md.
        w("## 4. Créditos de los modelos\n")
        w("La separación de voces usa el modelo **wespeaker CAM++** entrenado sobre **VoxCeleb** "
          "(Nagrani, Chung y Zisserman; Visual Geometry Group, Universidad de Oxford), distribuido "
          "bajo **Creative Commons Attribution 4.0**, más el modelo de segmentación **pyannote 3.0** "
          "(licencia MIT). **Los pesos no se modificaron.**\n")
    w("## %d. Lo que esta transcripción no dice\n" % (5 if con_voces else 4))
    w(NO_DICE)
    if con_voces:
        w("")
        w(NO_DICE_VOCES)
    w("\n## %d. Cómo repetir esto\n" % (6 if con_voces else 5))
    w("Mismos archivos, mismo modelo y los parámetros de la sección 2. La búsqueda es por haces con "
      "temperatura inicial 0, que es determinista. Los datos completos —cada palabra con su tiempo y "
      "su probabilidad, en todas las pasadas— están en `datos/`.\n")
    open(ruta, "w", encoding="utf-8").write("\n".join(L))


def escribir_pasajes(ruta, fichas, hoy, con_voces, con_glosario, nombres_pasada):
    L = []; w = L.append
    w("# PASAJES A VERIFICAR — dónde conviene oír el audio\n")
    w("%s. Los puntos exactos donde la transcripción tiene más probabilidad de estar mal. **No es "
      "una lista de errores encontrados** —nadie ha oído las grabaciones para comprobarlo—: es la "
      "lista de **dónde mirar primero** si algo va a sostener una afirmación.\n" % hoy)
    w("---\n")
    for f in fichas:
        w("## %s — `%s`\n" % (f["titulo"], f["origen"]))
        flojas = sorted([v for v in f["vent"] if v["medio"] < UMBRAL_ACUERDO], key=lambda v: v["medio"])
        w("### A. Donde las pasadas no coinciden (%s tramos)\n" % num(len(flojas)))
        if not flojas:
            w("Ninguno. **Eso no prueba que sea correcto**: todas comparten modelo y punto ciego.\n")
        else:
            w("Varias decodificaciones del mismo audio escribieron cosas distintas. **Es la señal más "
              "fuerte de que ahí hay un problema.**\n")
            for v in flojas[:15]:
                w("**%s** — acuerdo %s %%\n" % (hms(v["t"]), num(100 * v["medio"], 0)))
                for k in nombres_pasada:
                    if k in v["textos"]:
                        w("- %s *%s*: %s" % ("**›**" if k == f["gana"] else " ", k,
                                             (v["textos"][k] or "—")[:210]))
                w("")
            if len(flojas) > 15:
                w("*(Los 15 de menor acuerdo, de %s. El resto en `datos/`.)*\n" % num(len(flojas)))
        if con_glosario:
            w("### B. Avisos del glosario (%s)\n" % num(len(f["avisos"])))
            w("Donde una pasada con los términos del caso sugeridos escribió algo distinto. **El texto "
              "publicado no se cambió.** Si el glosario acierta, lo confirma usted oyendo.\n")
            w("*El minuto es el del segmento, no el de la palabra.*\n")
            if not f["avisos"]:
                w("Ninguno.\n")
            else:
                w("| Minuto | El glosario habría escrito | La versión publicada dice |")
                w("|---|---|---|")
                for a in f["avisos"][:40]:
                    w("| %s | `%s` | %s |" % (hms(a["t"]), a["sugiere"],
                                              a["dice_publicada"].replace("|", "/")))
            w("")
        rg = riesgosas(f["doc"])[:40]
        w("### C. Cifras y nombres propios con poca confianza (%s)\n" % num(len(riesgosas(f["doc"]))))
        w("El punto ciego clásico de un reconocedor: apellidos, números de expediente, fechas, "
          "cantidades. **Ninguno debería copiarse a un escrito sin oírlo.**\n")
        w("*El minuto es el del segmento que contiene la palabra, no el de la palabra: la marca "
          "de palabra falla precisamente en cifras y fechas, que es lo que aquí se lista.*\n")
        if not rg:
            w("Ninguno por debajo del umbral.\n")
        else:
            w("| Minuto | Lo que escribió | Tipo | Confianza |")
            w("|---|---|---|---|")
            for x in rg:
                w("| %s | `%s` | %s | %s %% |" % (hms(x["t"]), x["palabra"], x["tipo"], num(100 * x["c"], 0)))
        w("")
        if con_voces and f.get("dia"):
            vd = [s for s in f["doc"]["segmentos"] if s["voz"] is None or s["pureza"] < UMBRAL_PUREZA_VOZ]
            w("### D. Líneas donde la voz asignada es dudosa (%s de %s)\n"
              % (num(len(vd)), num(len(f["doc"]["segmentos"]))))
            w("O no se pudo asignar voz, o la línea se reparte entre dos hablantes. **Ahí el número de "
              "hablante no significa gran cosa.**\n")
            if not vd:
                w("Ninguna.\n")
            else:
                w("| Minuto | Voz | Pureza | Texto |")
                w("|---|---|---|---|")
                for s in sorted(vd, key=lambda s: s["pureza"])[:25]:
                    w("| %s | %s | %s %% | %s |" % (hms(s["inicio"]),
                      ("Hablante %s" % s["voz"]) if s["voz"] else "—", num(100 * s["pureza"], 0),
                      s["texto"].replace("|", "/")[:150]))
            w("")
        w("---\n")
    w("## Lo que esta lista no es\n")
    w("**No es una lista de errores comprobados.** Son sospechas producidas por medidas automáticas. "
      "Puede señalar pasajes perfectos y **puede dejar fuera errores reales**: un reconocedor también "
      "se equivoca con toda confianza. La única comprobación que vale es oír el audio.\n")
    open(ruta, "w", encoding="utf-8").write("\n".join(L))


# ------------------------------------------------------------------ principal
def reunir_entradas(entradas):
    arch = []
    for e in entradas:
        if os.path.isdir(e):
            arch += [os.path.join(e, f) for f in sorted(os.listdir(e))
                     if f.lower().endswith(EXT)]
        elif os.path.isfile(e) and e.lower().endswith(EXT):
            arch.append(e)
        else:
            aviso("  se omite (no es audio reconocible): %s" % e)
    return arch


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("entradas", nargs="+")
    ap.add_argument("--destino", required=True)
    ap.add_argument("--sin-voces", action="store_true")
    ap.add_argument("--sin-glosario", action="store_true")
    ap.add_argument("--pasadas", type=int, default=4)
    ap.add_argument("--glosario", default="")
    ap.add_argument("--dispositivo", default="auto", choices=("auto", "cpu", "cuda"))
    ap.add_argument("--umbral-voces", type=float, default=UMBRAL_VOCES,
                    help="cuanto tienen que parecerse dos tramos para contarlos como la misma "
                         "voz (por defecto %.2f). MEDIDO en una reunion de 22 minutos: con 0,90 "
                         "una sola voz se lleva el 74 %%%% del habla y dos personas distintas "
                         "quedan fundidas; con 0,60 quedan separadas, pero salen 15 voces y la "
                         "misma persona aparece varias veces. Para poner nombres, equivocarse "
                         "PARTIENDO es mas barato que equivocarse FUNDIENDO: lo primero se "
                         "arregla diciendo «estas dos son la misma», lo segundo mete en boca de "
                         "una las palabras de otra." % UMBRAL_VOCES)
    a = ap.parse_args()
    globals()["UMBRAL_VOCES"] = a.umbral_voces

    try:
        from faster_whisper import WhisperModel
        import numpy  # noqa: F401
        import av     # noqa: F401
    except Exception as e:
        aviso("NO SE PUDO EMPEZAR: falta una biblioteca -> %s" % e)
        aviso("No se transcribio nada. Instale faster-whisper, av y numpy, o siga a mano.")
        return 2

    con_voces = not a.sin_voces
    if con_voces:
        try:
            import sherpa_onnx  # noqa: F401
        except Exception as e:
            aviso("AVISO: no hay separacion de voces (%s). Se continua SIN voces." % e)
            con_voces = False
    terminos = {t for g in a.glosario.split(",") for t in norm(g)}
    con_glosario = bool(terminos) and not a.sin_glosario

    arch = reunir_entradas(a.entradas)
    if not arch:
        aviso("No se encontro ningun archivo de audio en lo indicado."); return 2
    npas = max(2, min(4, a.pasadas))
    usar = None  # se decide tras preparar el audio
    dest = os.path.abspath(a.destino)
    trabajo = os.path.join(dest, ".trabajo")
    os.makedirs(os.path.join(dest, "datos"), exist_ok=True)
    os.makedirs(trabajo, exist_ok=True)
    hoy = datetime.date.today().isoformat()
    disp = "cuda" if a.dispositivo == "auto" else a.dispositivo
    aviso("%d grabacion(es) · %d pasadas · voces=%s · glosario=%s"
          % (len(arch), npas, "si" if con_voces else "no", "si" if con_glosario else "no"))

    aviso("\n== 1. preparando el audio ==")
    fichas = []
    for i, r in enumerate(arch, 1):
        cod = "A%d" % i
        destinos = {n: os.path.join(trabajo, "%s_%s.wav" % (cod, n))
                    for n in ("mezcla_limpio", "mezcla_crudo", "izq_limpio", "der_limpio")}
        d = preparar(r, destinos)
        aviso("  %s  %s  senal/ruido %.1f -> %.1f dB%s" % (
            cod, os.path.basename(r), d["original"]["snr_estimada_db"], d["limpio"]["snr_estimada_db"],
            "  SATURADO EN ORIGEN" if d["original"]["muestras_saturadas"] else ""))
        if d["estereo_util"]:
            aviso("       dos canales distintos (correlacion %.2f): se transcriben aparte"
                  % d["correlacion_canales"])
        else:
            aviso("       un solo canal util (correlacion %.2f): no hay estereo que aprovechar"
                  % d["correlacion_canales"])
        fichas.append({"cod": cod, "origen": os.path.basename(r), "ruta": r, "diag": d,
                       "titulo": "Audio %d" % i, "pistas": destinos,
                       "limpio": destinos["mezcla_limpio"]})

    if con_voces:
        aviso("\n== 2. separando voces ==")
        for f in fichas:
            t0 = time.time()
            try:
                f["dia"] = diarizar(leer_wav(f["limpio"]))
                aviso("  %s  %d voces, %d turnos (%.0fs)" % (f["cod"], len(f["dia"]["hablantes"]),
                                                             len(f["dia"]["turnos"]), time.time() - t0))
            except Exception as e:
                aviso("  %s  SIN VOCES: %s" % (f["cod"], e)); f["dia"] = None

    aviso("\n== 3. transcribiendo ==")
    hay_estereo = all(f["diag"]["estereo_util"] for f in fichas)
    usar = (PASADAS_ESTEREO if hay_estereo else PASADAS_MONO)[:npas]
    aviso("   pasadas: " + ", ".join(u[0] for u in usar))
    docs = {f["cod"]: {} for f in fichas}
    for etq, var, ct in usar:
        try:
            mod = WhisperModel("large-v3", device=disp, compute_type=ct, local_files_only=True)
        except Exception as e:
            aviso("  no se pudo cargar el modelo en %s/%s: %s" % (disp, ct, e))
            if disp == "cuda":
                aviso("  se reintenta en CPU (mas lento)")
                disp, ct = "cpu", "int8"
                mod = WhisperModel("large-v3", device=disp, compute_type=ct, local_files_only=True)
            else:
                return 2
        for f in fichas:
            d = transcribir(mod, leer_wav(f["pistas"][var]), "%s/%s" % (f["cod"], etq))
            docs[f["cod"]][etq] = d
            aviso("  %s/%s  %d seg, %d pal, %.1f min" % (f["cod"], etq, len(d["segmentos"]),
                  sum(len(s["palabras"]) for s in d["segmentos"]), d["segundos_computo"] / 60))
        del mod
    if con_glosario:
        aviso("\n== 4. pasada de glosario (solo para avisar) ==")
        mod = WhisperModel("large-v3", device=disp, compute_type="int8_float16" if disp == "cuda" else "int8",
                           local_files_only=True)
        for f in fichas:
            f["glos"] = transcribir(mod, leer_wav(f["limpio"]), "%s/glosario" % f["cod"], a.glosario)
        del mod

    aviso("\n== 5. consenso y salidas ==")
    for f in fichas:
        dd = docs[f["cod"]]
        vent = acuerdo(dd, dd[usar[0][0]]["duracion_s"])
        punt = {k: sum(v["por_pasada"][k] for v in vent) / max(len(vent), 1) for k in dd}
        f["gana"] = max(punt, key=punt.get)
        f["vent"], f["puntajes"] = vent, punt
        f["malas"] = [v["t"] for v in vent if v["medio"] < UMBRAL_ACUERDO]
        f["acuerdo_medio"] = sum(v["medio"] for v in vent) / max(len(vent), 1)
        doc = dividir_largos(dd[f["gana"]])
        if con_voces and f.get("dia"):
            doc = asignar_voces(doc, f["dia"])
        f["doc"] = doc
        f["marcas"] = {s["i"]: marcar(s, f["malas"], con_voces and f.get("dia")) for s in doc["segmentos"]}
        f["avisos"] = avisos_glosario(doc, f["glos"], terminos) if con_glosario else []
        f["palabras"] = sum(len(s["palabras"]) for s in doc["segmentos"])
        base = "Transcripcion - %s - %s" % (f["titulo"], hoy)
        escribir_transcripcion(os.path.join(dest, base + ".md"), doc, f["marcas"], f["titulo"],
                               f["origen"], f["gana"], f.get("dia") if con_voces else None, hoy)
        open(os.path.join(dest, base + ".txt"), "w", encoding="utf-8").write(
            " ".join(s["texto"] for s in doc["segmentos"]))
        escribir_subtitulos(doc, os.path.join(dest, base + ".srt"), os.path.join(dest, base + ".vtt"))
        json.dump({"publicada": doc, "puntajes": punt, "ventanas": vent, "avisos": f["avisos"],
                   "voces": f.get("dia"), "diagnostico": f["diag"],
                   "marcas": {str(k): v for k, v in f["marcas"].items()}},
                  open(os.path.join(dest, "datos", "%s - datos completos.json" % f["cod"]), "w",
                       encoding="utf-8"), ensure_ascii=False)
        aviso("  %s  gana «%s» · acuerdo %.1f%% · %d tramos flojos%s" % (
            f["cod"], f["gana"], 100 * f["acuerdo_medio"], len(f["malas"]),
            " · %d voces" % len(f["dia"]["hablantes"]) if con_voces and f.get("dia") else ""))

    escribir_registro(os.path.join(dest, "00 - REGISTRO DE TRANSCRIPCION - %s.md" % hoy),
                      fichas, hoy, con_voces, con_glosario, usar)
    escribir_pasajes(os.path.join(dest, "00 - PASAJES A VERIFICAR - %s.md" % hoy),
                     fichas, hoy, con_voces, con_glosario, [u[0] for u in usar])
    aviso("\nLISTO. Escrito en: %s" % dest)
    aviso("Los WAV intermedios quedan en .trabajo/ — se pueden borrar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
