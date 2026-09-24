# -*- coding: utf-8 -*-
"""construir_entrega — arma el paquete que recibe ella, y lo comprueba.

    python construir_entrega.py <entrega.json>

El .json describe UNA entrega: dónde está el material, qué grabaciones
lleva, qué documentos la forman y qué dice el aviso de cada uno; y, si
hace falta, los tramos que hay que señalar a mano (`tramos_senalados`:
audio, desde, hasta, titulo, detalle y cierre opcional), que van entre
dos avisos en el Word y en la página sin tocar el texto transcrito. **Ese
archivo se queda fuera del repositorio**, porque nombra el caso y las
rutas de la máquina; aquí vive solo el cómo.

Se puede ejecutar las veces que haga falta: BORRA Y REHACE la carpeta de
salida y el .zip, y nunca toca el material de origen (grabaciones,
transcripciones, resúmenes).

Lo que comprueba antes de dar por buena una entrega, y por lo que se
detiene si falla:
  · que cada grabación copiada sea idéntica al original (SHA-256);
  · que ningún Word haya perdido contenido al convertirlo;
  · que cada cita entre « » esté LITERAL en alguna transcripción;
  · que no quede sintaxis de enlace cruda a la vista;
  · que todos los enlaces resuelvan dentro del paquete;
  · que no viaje ninguna ruta de esta máquina.

Ninguna de esas comprobaciones mira si el documento se VE bien: eso solo
se sabe abriéndolo.
"""
import argparse, glob, hashlib, html, io, json, os, re, shutil, subprocess, sys, zipfile
from urllib.parse import unquote

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS)
from estado_transcripcion import bucles as detectar_bucles, hms as a_hms  # noqa: E402
from md2html import _ORDEN_MOTIVOS, visible as VISIBLE_DE, hms as hms_pagina  # noqa: E402


def _config():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("config", help="el .json que describe ESTA entrega")
    a = ap.parse_args()
    if not os.path.isfile(a.config):
        sys.exit("\nDETENIDO: no está la configuración: %s" % a.config)
    c = json.load(io.open(a.config, encoding="utf-8"))
    falta = [k for k in ("raiz", "nombre", "origen", "audios", "documentos",
                         "transcripcion", "audio_destino") if k not in c]
    if falta:
        sys.exit("\nDETENIDO: a la configuración le faltan: %s" % ", ".join(falta))
    c["_aqui"] = os.path.dirname(os.path.abspath(a.config))
    return c


ANOTACION = re.compile(r"`\[\?\]` \*\(([^)]*)\)\*")

# La etiqueta del hablante va DENTRO de la negrita -- «**[00:00:00] · Hablante 1**» --,
# asi que la expresion tiene que admitirla. Sin esto se descartaban justo las
# lineas que llevan hablante, que son las que mas importan, y el programa
# denunciaba como inventadas citas que si estaban.
LINEA = re.compile(r"^\*\*\[(\d\d:\d\d:\d\d)\][^*]*\*\*\s+(.*?)(?:\s+`\[\?\]`.*)?$")

# La misma linea, con la etiqueta de voz aparte para poder rehacerla.
ETIQUETA = re.compile(r"^(\*\*\[(\d\d:\d\d:\d\d)\])( · Hablante [^*]+)?(\*\*)(\s+.*)$")


def voces(segmentos):
    """Cuantas voces distintas tienen los datos (sin contar las lineas sin voz)."""
    return len({s.get("voz") for s in segmentos if s.get("voz") is not None})


def voces_desde_datos(cuerpo, segmentos, etiquetas=None):
    """Solo las etiquetas de voz; los avisos de cada linea quedan como estan."""
    return lineas_desde_datos(cuerpo, segmentos, None, etiquetas)


def rotulo_de_voz(v, etiquetas=None):
    """« · Hablante N», o « · Hablante N — Nombre» si una persona la nombro:
    el mismo formato que escribe nombrar_voces y que pinta la pagina."""
    if v is None:
        return " · Hablante ?"
    nombre = ((etiquetas or {}).get(str(v)) or {}).get("texto")
    return " · Hablante %s%s" % (v, " — %s" % nombre if nombre else "")


def lineas_desde_datos(cuerpo, segmentos, marcas, etiquetas=None):
    """Rehace las etiquetas de hablante del Markdown -- y, si se dan `marcas`,
    los avisos `[?]` de cada linea -- desde los MISMOS datos que usa la pagina
    de oir y marcar.

    Los avisos, por lo mismo que las voces: «voz dudosa» y «sin voz asignada»
    dependen de la separacion de voces. Cuando se rehizo, el Markdown se quedo
    con los avisos de la separacion vieja, y el Word marcaba como dudosa una voz
    que la pagina daba por clara, y al reves.

    Existe porque se separaron: cuando se rehizo la separacion de voces de una
    grabacion, los datos cambiaron y el Markdown no. El Word salia con la
    numeracion vieja y la pagina con la nueva, y la misma linea era «Hablante 2»
    en uno y «Hablante 4» en la otra. Dos numeraciones de la misma grabacion en
    la misma entrega no son una duda: son una contradiccion.

    La convencion es la del Markdown: la etiqueta va solo donde cambia la voz,
    y una linea sin voz es «Hablante ?». Aplicada a los datos de los que salio
    un Markdown, lo reproduce identico.

    Se detiene si las lineas no casan una a una con los segmentos, por hora
    impresa y por texto: rehacer etiquetas a ciegas pondria la voz de una
    linea en otra. Y si una etiqueta lleva, con el MISMO numero, algo que los
    datos no permiten rehacer -- un nombre que no esta en `etiquetas` --: se
    tiraria una atribucion que hizo una persona.

    Una transcripcion sin voces (ninguna etiqueta en el Markdown y ninguna voz
    en los datos) se deja como esta: no hay nada que rehacer, y ponerle
    «Hablante ?» a todo seria inventar una atribucion.

    Devuelve (cuerpo, lineas que cambian)."""
    lineas = cuerpo.split("\n")
    sin_voces = voces(segmentos) == 0 and not any(
        (ETIQUETA.match(l) or [None, None, None, None])[3] for l in lineas)
    k, previa, cambiadas = 0, object(), 0
    for j, l in enumerate(lineas):
        m = ETIQUETA.match(l)
        if not m:
            continue
        if k >= len(segmentos):
            falla("la transcripcion tiene mas lineas que segmentos los datos (%d)" % len(segmentos))
        s = segmentos[k]
        texto = LINEA.match(l).group(2).strip()
        if hms_pagina(s["inicio"]) != m.group(2) or texto != (s.get("texto") or "").strip():
            falla("la linea de las %s no casa con el segmento %d de los datos (%s, «%s»): "
                  "no se rehacen las voces a ciegas"
                  % (m.group(2), k, hms_pagina(s["inicio"]), (s.get("texto") or "")[:60]))
        v = s.get("voz")
        et = "" if (v == previa or sin_voces) else rotulo_de_voz(v, etiquetas)
        previa = v
        viejo = m.group(3) or ""
        numero = re.match(r" · Hablante (\S+)", viejo)
        if et and numero and numero.group(1) == str("?" if v is None else v) and viejo != et:
            falla("la etiqueta «%s» de las %s lleva algo que los datos no permiten rehacer "
                  "(saldria «%s»): no se tira una atribucion que hizo una persona"
                  % (viejo.strip(" ·"), m.group(2), et.strip(" ·")))
        resto = m.group(5)
        if marcas is not None:
            # El mismo formato con que lo escribe transcribir_audio.
            mk = marcas.get(str(s.get("i", k))) or marcas.get(s.get("i", k)) or []
            resto = " %s%s" % (s["texto"], "  `[?]` *(%s)*" % "; ".join(mk) if mk else "")
        nueva = m.group(1) + et + m.group(4) + resto
        if nueva != l:
            cambiadas += 1
        lineas[j] = nueva
        k += 1
    if k != len(segmentos):
        falla("la transcripcion tiene %d lineas y los datos %d segmentos" % (k, len(segmentos)))
    return "\n".join(lineas), cambiadas


def bucles_de(carpeta, n):
    ruta = os.path.join(carpeta, "datos", "A%d - datos completos.json" % n)
    if not os.path.isfile(ruta):
        return None
    d = json.load(io.open(ruta, encoding="utf-8"))
    return detectar_bucles(d.get("publicada") or d.get("principal"))


def marcar_bucles(cuerpo, n):
    """Pone el aviso DONDE ella lee, no en otro documento.

    El aviso por linea ya existia -- «posible repeticion» --, pero llega ahogado:
    esas lineas llevan cuatro motivos cada una y el 71 % del Audio 2 lleva alguno.
    Un tramo repetido no es una duda mas: es texto que probablemente nadie dijo,
    y se ve sin oir. Por eso va como bloque, antes y despues.

    No borra nada: repetir de verdad existe."""
    bs = bucles_de(ORIGEN, n)
    if not bs:
        return cuerpo, 0
    lineas = cuerpo.split("\n")
    for b in sorted(bs, key=lambda x: -x["desde"]):
        ts, texto = a_hms(b["desde"]), b["texto"]
        pos = [k for k, l in enumerate(lineas)
               if (LINEA.match(l) or [None]) and LINEA.match(l)
               and LINEA.match(l).group(1) == ts and LINEA.match(l).group(2).strip() == texto]
        if len(pos) != 1:
            falla("Audio %d: la repeticion de %s no se localiza en la transcripcion "
                  "(%d coincidencias)" % (n, ts, len(pos)))
        a = pos[0]
        z, vistas = a, 0
        while z < len(lineas) and vistas < b["veces"]:
            m = LINEA.match(lineas[z])
            if m:
                if m.group(2).strip() != texto:
                    break
                vistas += 1
            z += 1
        if vistas != b["veces"]:
            falla("Audio %d: la repeticion de %s tiene %d lineas en la transcripcion y %d en "
                  "los datos" % (n, ts, vistas, b["veces"]))

        # Solo se afirma de las otras lecturas lo que se ha comprobado aqui.
        otras, repiten = 0, 0
        for c in OTRAS:
            ob = bucles_de(c, n)
            if ob is None:
                continue
            otras += 1
            if any(x["hasta"] >= b["desde"] and x["desde"] <= b["hasta"] for x in ob):
                repiten += 1
        if otras and not repiten:
            prueba = ("Ninguna de las otras %d lecturas automáticas de esta grabación repite "
                      "aquí." % otras)
        elif otras:
            prueba = ("%d de las otras %d lecturas automáticas repiten también aquí: puede que "
                      "sea real." % (repiten, otras))
        else:
            prueba = "No hay otras lecturas con las que contrastarlo."

        lineas.insert(z, "> ⚠ **Fin del tramo repetido.**")
        lineas.insert(z, "")
        lineas.insert(a, "")
        lineas.insert(a, "> ⚠ **Aquí la máquina se repitió: las %d líneas siguientes dicen lo "
                         "mismo**, de %s a %s. %s Lo más probable es que **%d de estas %d líneas "
                         "no las dijera nadie**. Nadie lo ha comprobado oyendo: son %d segundos. "
                         "No se ha borrado nada."
                      % (b["veces"], ts, a_hms(b["hasta"]), prueba, b["veces"] - 1, b["veces"],
                         round(b["hasta"] - b["desde"])))
    return "\n".join(lineas), len(bs)


HORA = re.compile(r"^\d\d:\d\d:\d\d$")


def tramos_de(config, n):
    """Los tramos que ESTA entrega senala en la grabacion n.

    Un tramo repetido lo detecta el programa; esto no. Aqui entra lo que se
    descubrio despues, mirando -- una palabra que ninguna otra lectura
    sostiene, un pasaje mal leido --, y que el programa no sabe ver. El texto
    del aviso vive en la configuracion de la entrega, fuera del repositorio,
    porque nombra lo que se dijo en el caso."""
    out = []
    for t in config.get("tramos_senalados") or []:
        if t.get("audio") != n:
            continue
        for k in ("desde", "hasta", "titulo", "detalle"):
            if not isinstance(t.get(k), str) or not t[k].strip():
                falla("un tramo senalado del Audio %d no trae «%s»" % (n, k))
        if not (HORA.match(t["desde"]) and HORA.match(t["hasta"])):
            falla("un tramo senalado del Audio %d no trae horas HH:MM:SS" % n)
        if hms_a_s(t["hasta"]) < hms_a_s(t["desde"]):
            falla("el tramo senalado del Audio %d acaba antes de empezar (%s-%s)"
                  % (n, t["desde"], t["hasta"]))
        out.append(t)
    return out


def aviso_de_tramo(t):
    """(apertura, cierre) del aviso de un tramo senalado. El mismo texto va al
    Word y a la pagina, para que las dos digan lo mismo."""
    abre = ("**%s** %s Va de %s a %s. **No se ha borrado ni cambiado nada del texto "
            "transcrito**: las líneas siguen ahí, entre este aviso y el de cierre."
            % (t["titulo"].strip(), t["detalle"].strip(), t["desde"], t["hasta"]))
    cierra = "**Fin del tramo señalado.**"
    if (t.get("cierre") or "").strip():
        cierra += " " + t["cierre"].strip()
    return abre, cierra


def marcar_tramos(cuerpo, n, tramos):
    """Pone cada tramo senalado entre dos avisos, DONDE ella lee.

    Igual que el tramo repetido: no borra ni cambia una palabra. Corregir el
    texto seria poner otra lectura en lugar de la que hay, y nadie ha oido el
    tramo para saber cual es la buena. Lo que si se puede es impedir que lo
    lea como si nada.

    Localiza las lineas por su hora impresa, y se detiene si una hora no
    esta o esta dos veces: un aviso en la linea equivocada es peor que
    ninguno."""
    lineas = cuerpo.split("\n")
    for t in tramos:
        horas = [(k, m.group(1)) for k, m in ((k, LINEA.match(l)) for k, l in enumerate(lineas)) if m]
        a = [k for k, h in horas if h == t["desde"]]
        z = [k for k, h in horas if h == t["hasta"]]
        if len(a) != 1 or len(z) != 1:
            falla("Audio %d: el tramo senalado %s-%s no se localiza en la transcripcion "
                  "(%d lineas a las %s y %d a las %s)"
                  % (n, t["desde"], t["hasta"], len(a), t["desde"], len(z), t["hasta"]))
        a, z = a[0], z[0]
        if z < a:
            falla("Audio %d: en el tramo senalado %s-%s la ultima linea va antes que la primera"
                  % (n, t["desde"], t["hasta"]))
        abre, cierra = aviso_de_tramo(t)
        lineas.insert(z + 1, "> ⚠ " + cierra)
        lineas.insert(z + 1, "")
        lineas.insert(a, "")
        lineas.insert(a, "> ⚠ " + abre)
    return "\n".join(lineas), len(tramos)


def nombre_audio(n, hora):
    return C["audio_destino"] % (n, hora)


def _senalados(n):
    """Los compromisos de esa grabacion, si el caso los tiene senalados.

    Va aparte de los datos de la transcripcion porque son cosas distintas: la
    transcripcion dice lo que se oye, y esto dice donde alguien se obligo --
    que es una lectura, y las lecturas se revisan sin tocar el texto."""
    carpeta = C.get("compromisos")
    if not carpeta:
        return []
    ruta = os.path.join(DESPACHO, carpeta, "A%d - compromisos.json" % n)
    return ["--compromisos", ruta] if os.path.isfile(ruta) else []


def _de_caso(n):
    """Lo que las paginas de una misma entrega comparten o reciben del caso:
    el identificador del caso (el glosario de ella vale para todas), las
    sugerencias de glosario (hipotesis) y las lecturas de los huecos que se
    volvieron a oir (pistas para «lo que no se entiende»)."""
    extra = ["--caso", hashlib.sha256(os.path.normpath(DESPACHO).lower().encode("utf-8")).hexdigest()[:12]]
    g = C.get("glosario")
    if g:
        ruta = os.path.join(DESPACHO, g)
        if not os.path.isfile(ruta):
            falla("no esta el glosario %s" % ruta)
        extra += ["--glosario", ruta]
    r = C.get("genoma")
    if r:
        ruta = os.path.join(DESPACHO, r)
        if not os.path.isfile(ruta):
            falla("no esta el genoma de voz %s" % ruta)
        extra += ["--rescates", ruta, "--rescates-audio", "A%d" % n]
    return extra


def pagina_audio(n):
    return "Audio %d - oir y marcar.html" % n


# Donde la pagina guarda lo que ella declara, DENTRO de la entrega (guardado.js
# y recoger_lo_declarado usan el mismo nombre).
LO_QUE_DECLARO = "Lo que declaré"


def lo_suyo_dentro(salida):
    """Los archivos que ella ha guardado dentro de una entrega, en una carpeta
    «Lo que declaré» de CUALQUIER nivel: si al guardar eligio «Transcripciones»,
    la carpeta queda ahi dentro. Rehacer la entrega borra la carpeta entera:
    con esto dentro, seria borrar su trabajo."""
    if not os.path.isdir(salida):
        return []
    return sorted(os.path.relpath(os.path.join(r, f), salida)
                  for r, _, fs in os.walk(salida)
                  if LO_QUE_DECLARO in os.path.relpath(r, salida).split(os.sep) for f in fs)


def falla(msg):
    sys.exit("\nDETENIDO: " + msg)


def py(*args):
    r = subprocess.run([sys.executable] + [str(a) for a in args], capture_output=True,
                       text=True, encoding="utf-8",
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    return r.returncode, (r.stdout + r.stderr).strip()


def py_ok(*args):
    code, out = py(*args)
    if code != 0:
        falla("%s\n%s" % (" ".join(os.path.basename(str(a)) for a in args[:1]), out))
    return out


def hms_a_s(v):
    h, m, s = (int(x) for x in v.split(":"))
    return h * 3600 + m * 60 + s


def enlazar(md):
    """[[A2 00:04:33]] -> enlace a ese minuto de la pagina del Audio 2.
    En Word queda solo el texto: «Audio 2, 00:04:33»."""
    def uno(m):
        n, t, corto = m.group(1), m.group(2), m.group(3)
        texto = t if corto else "Audio %s, %s" % (n, t)
        return "[%s](<Transcripciones/%s#t=%d>)" % (texto, pagina_audio(int(n)), hms_a_s(t))
    # [[A2 00:04:33 hora]] enlaza igual pero muestra solo la hora: para tablas
    # que ya estan dentro de la seccion de esa grabacion.
    return re.sub(r"\[\[A(\d+) (\d\d:\d\d:\d\d)( hora)?\]\]", uno, md)


def main():
    """Arma la entrega entera. Se ejecuta; importarlo no hace nada, que es
    lo que exige la superficie: un programa invocable se invoca a proposito."""
    global C, DESPACHO, AQUI, ORIGEN, OTRAS, NOMBRE, SALIDA, RENDER, AUDIOS
    global _s, _SONDA
    C = _config()
    DESPACHO = C["raiz"]
    AQUI = C["_aqui"]
    ORIGEN = os.path.join(DESPACHO, C["origen"])
    OTRAS = [os.path.join(DESPACHO, x) for x in C.get("otras") or []]
    NOMBRE = C["nombre"]
    # Sin «salida», donde dice ADR-023: 2-Borradores/Entregas. En 3-Para
    # presentar no escribe ningun programa: esa carpeta es de ella.
    SALIDA = os.path.join(DESPACHO, *(C.get("salida") or "2-Borradores/Entregas").split("/"), NOMBRE)
    RENDER = os.path.join(AQUI, "_generado")
    AUDIOS = [tuple(a) for a in C["audios"]]
    _s = C.get("audio_sonda") or AUDIOS[-1][0]
    _SONDA = next((n, h) for n, _f, h in AUDIOS if n == _s)

    # ------------------------------------------------------------------ 1. limpiar
    # El cerrojo: esto BORRA Y REHACE la carpeta de salida, asi que antes se
    # comprueba que sea una carpeta de entrega y que este dentro del caso.
    # Antes exigia que fuera hija DIRECTA de la raiz, y eso impedia guardarla
    # donde le corresponde -- hoy `2-Borradores/Entregas/` (ADR-023); antes
    # `3-Para presentar/` --, obligando a dejarla
    # suelta al lado del material. La condicion nueva no afloja nada: sigue
    # sin poder borrar nada de fuera del caso, ni nada que no se llame asi.
    _raiz = os.path.normpath(DESPACHO)
    _dest = os.path.normpath(SALIDA)
    if not (_dest.startswith(_raiz + os.sep) and _dest != _raiz
            and os.path.basename(SALIDA).startswith("ENTREGA - ")):
        falla("ruta de salida inesperada: %s" % SALIDA)
    suyo = lo_suyo_dentro(SALIDA)
    if suyo:
        falla("la entrega «%s» ya tiene %d archivo(s) que ella guardo en «%s» (%s). Rehacerla los "
              "borraria. Recojalos (recoger_lo_declarado.py) y ponga otro nombre a la entrega: "
              "version nueva, ADR-011 §8." % (os.path.basename(SALIDA), len(suyo), LO_QUE_DECLARO, suyo[0]))
    for p in (SALIDA, RENDER):
        if os.path.isdir(p):
            shutil.rmtree(p)
    if os.path.exists(SALIDA + ".zip"):
        os.remove(SALIDA + ".zip")
    for sub in ("Transcripciones", "Word", "audio", "anexos"):
        os.makedirs(os.path.join(SALIDA, sub))
    os.makedirs(os.path.join(RENDER, "transcripciones"))
    print("Carpeta: %s" % SALIDA)

    # ------------------------------------------------------------ 2. grabaciones
    huellas = {}
    for n, original, hora in AUDIOS:
        src = os.path.join(DESPACHO, original)
        if not os.path.isfile(src):
            falla("no esta la grabacion %s" % src)
        dst = os.path.join(SALIDA, "audio", nombre_audio(n, hora))
        shutil.copy2(src, dst)
        h = hashlib.sha256(open(src, "rb").read()).hexdigest()
        if hashlib.sha256(open(dst, "rb").read()).hexdigest() != h:
            falla("la copia de %s no es identica al original" % original)
        huellas[n] = (original, h, os.path.getsize(src))
    print("Grabaciones: %d copiadas, identicas al original (SHA-256)" % len(AUDIOS))

    # ---------------------------------------------------------- 3. transcripciones
    for n, original, hora in AUDIOS:
        src = os.path.join(ORIGEN, C["transcripcion"] % n)
        md = io.open(src, encoding="utf-8").read()
        cab, sep, cuerpo = md.partition("\n---\n")
        if not sep:
            falla("la transcripcion %d no tiene separador de cabecera" % n)
        dur = re.search(r"\*\*Duración:\*\*\s*(\S+)", cab).group(1)
        aviso = re.search(r"^> .*$", cab, re.M).group(0)
        dia, hh = C["audio_recibido"], hora.replace(".", ":")

        # Las voces salen de los datos que usa la pagina, no del Markdown: asi el
        # Word y la pagina numeran igual. Y la cuenta de la cabecera, tambien.
        ruta_datos = os.path.join(ORIGEN, "datos", "A%d - datos completos.json" % n)
        _d = json.load(io.open(ruta_datos, encoding="utf-8"))
        segmentos = (_d.get("publicada") or _d.get("principal") or {}).get("segmentos") or []
        etiquetas = _d.get("etiquetas") or {}
        antes = cuerpo
        cuerpo, n_cambian = lineas_desde_datos(cuerpo, segmentos, _d.get("marcas"), etiquetas)
        if [m.group(2) for m in (LINEA.match(l) for l in antes.split("\n")) if m] != \
                [m.group(2) for m in (LINEA.match(l) for l in cuerpo.split("\n")) if m]:
            falla("al rehacer las voces del Audio %d cambio texto transcrito" % n)
        # Que el Word cambie de voces respecto de su transcripcion de origen no
        # puede pasar callado: quien anoto «Hablante 2 dice...» sobre la entrega
        # anterior tiene que saberlo. Lo correcto es regenerar la transcripcion
        # vigente desde sus datos, como version nueva; si no, declararlo.
        if n_cambian and not C.get("rehacer_voces"):
            falla("Audio %d: %d lineas de la transcripcion de origen no llevan la voz o los avisos "
                  "de los datos que usa la pagina. Regenere la transcripcion vigente desde sus datos "
                  "(version nueva), o ponga \"rehacer_voces\": true en la configuracion y digalo en "
                  "la entrega." % (n, n_cambian))
        if n_cambian:
            print("  Audio %d: %d lineas rehechas desde los datos de la pagina (voz o avisos)"
                  % (n, n_cambian))
        hab = voces(segmentos)
        if not hab:
            texto_voces = "**Voces:** no se distinguen: ninguna línea está atribuida a nadie.  \n"
        else:
            tope = max(s["voz"] for s in segmentos if isinstance(s.get("voz"), int)) \
                if any(isinstance(s.get("voz"), int) for s in segmentos) else hab
            texto_voces = (
                "**Voces:** separadas automáticamente en **%d hablantes**, numerados por cuánto hablan. "
                % hab if tope <= hab else
                "**Voces:** separadas automáticamente: **%d voces** con alguna línea, numeradas hasta el "
                "%d por el tiempo que les dio la separación; los números que faltan son voces que la "
                "separación detectó sin quedarse con ninguna línea. " % (hab, tope))
            texto_voces += ("**Los nombres que acompañan a algunas voces los declaró una persona; las "
                            "demás son voces sin identificar.**  \n"
                            if any((e or {}).get("texto") for e in etiquetas.values()) else
                            "**«Hablante 1» es una voz, no una persona identificada.**  \n")
        # Quien nombro las voces, si alguien lo hizo: lo escribe nombrar_voces en
        # la cabecera, y rehacer la cabecera lo tiraba.
        declaradas = re.search(r"^\*\*Quién es cada voz:\*\*.*(?:\n- .*)*", cab, re.M)

        nueva = (
            "# Transcripción del Audio %d\n\n"
            "**Recibido:** por WhatsApp el %s a las %s  \n"
            "**Grabación:** `audio/%s`  \n"
            "**Duración:** %s  \n"
            "**Quién la hizo:** un programa de reconocimiento de voz, **no una persona**. El audio se "
            "leyó varias veces de formas distintas y se publica la lectura que **más coincide con las "
            "demás**, no la que la máquina daba por más segura.  \n"
            "%s"
            "**Marca `[?]`:** hay algún motivo para dudar de esa línea. Al final, entre "
            "paréntesis, va **el más grave**, y cuántos más hay. La página de «oír y marcar» "
            "los muestra todos.  \n"
            "**Comprobación:** nadie ha oído todavía la grabación para cotejar esta transcripción.\n\n"
            "%s\n"
        ) % (n, dia, hh, nombre_audio(n, hora), dur, texto_voces, aviso)
        if declaradas:
            nueva += "\n" + declaradas.group(0) + "\n"
        # Un campo por parrafo: md2docx no respeta el salto de linea de dos espacios
        # y en Word los fundia en uno solo.
        nueva = nueva.replace("  \n**", "\n\n**")

        def traducir(m):
            # Ordenados de mas a menos grave. En el Word no hay pliegue ni subrayado
            # -- los dos canales que en la pagina permiten callar lo redundante --,
            # asi que aqui no se quita ninguno: solo llegan en orden, y el que
            # importa llega primero.
            crudos = sorted((x.strip() for x in m.group(1).split(";")),
                            key=lambda x: _ORDEN_MOTIVOS.index(x)
                            if x in _ORDEN_MOTIVOS else 99)
            # Solo el mas grave, y cuantos quedan. En papel no hay clic: si van los
            # cinco, la linea se lee como decoracion y el grave se pierde -- que es
            # justo lo que paso con el tramo repetido. Decir cuantos faltan impide
            # que se caiga ninguno en silencio: estan todos en la pagina.
            resto = len(crudos) - 1
            texto = VISIBLE_DE(crudos[0])
            if resto > 0:
                texto += " · y %d motivo%s más" % (resto, "" if resto == 1 else "s")
            return "`[?]` *(" + texto + ")*"

        cuerpo2 = ANOTACION.sub(traducir, cuerpo)
        if ANOTACION.sub("", cuerpo) != ANOTACION.sub("", cuerpo2):
            falla("al traducir las anotaciones del Audio %d cambio texto transcrito" % n)

        cuerpo3, n_bucles = marcar_bucles(cuerpo2, n)
        solo_texto = lambda c: [m.group(2) for m in (LINEA.match(l) for l in c.split("\n")) if m]
        if solo_texto(cuerpo3) != solo_texto(cuerpo2):
            falla("al marcar las repeticiones del Audio %d cambio texto transcrito" % n)
        cuerpo2 = cuerpo3
        if n_bucles:
            print("  Audio %d: %d tramo(s) repetido(s) marcados en la transcripcion" % (n, n_bucles))

        tramos = tramos_de(C, n)
        cuerpo3, n_tramos = marcar_tramos(cuerpo2, n, tramos)
        if solo_texto(cuerpo3) != solo_texto(cuerpo2):
            falla("al senalar tramos del Audio %d cambio texto transcrito" % n)
        cuerpo2 = cuerpo3
        con_tramos = []
        if n_tramos:
            ruta_tramos = os.path.join(RENDER, "transcripciones", "Audio %d - tramos.json" % n)
            # La pagina recibe el aviso ya redactado: asi Word y pagina dicen
            # lo mismo, palabra por palabra, sin dos redacciones que mantener.
            para_pagina = []
            for t in tramos:
                abre, cierra = aviso_de_tramo(t)
                para_pagina.append({"desde": t["desde"], "hasta": t["hasta"],
                                    "abre": abre, "cierra": cierra})
            with io.open(ruta_tramos, "w", encoding="utf-8") as f:
                json.dump(para_pagina, f, ensure_ascii=False, indent=1)
            con_tramos = ["--tramos", ruta_tramos]
            print("  Audio %d: %d tramo(s) senalado(s) en la transcripcion" % (n, n_tramos))

        md_nuevo = os.path.join(RENDER, "transcripciones", "Audio %d.md" % n)
        io.open(md_nuevo, "w", encoding="utf-8").write(nueva + sep + cuerpo2)

        py_ok(os.path.join(SCRIPTS, "md2html.py"), md_nuevo,
              os.path.join(SALIDA, "Transcripciones", pagina_audio(n)),
              "--datos", ruta_datos,
              "--audio", os.path.join(SALIDA, "audio", nombre_audio(n, hora)),
              "--origen", "Transcripción automática del Audio %d (recibido por WhatsApp el %s a las %s)"
              % (n, dia, hh), *(_senalados(n) + con_tramos + _de_caso(n)))
        py_ok(os.path.join(SCRIPTS, "md2docx.py"), md_nuevo,
              os.path.join(SALIDA, "Word", "Audio %d - transcripcion.docx" % n))
    print("Transcripciones: %d paginas y %d Word; texto transcrito identico al original"
          % (len(AUDIOS), len(AUDIOS)))

    # --------------------------------------------------------------- 4. documentos
    peso = sum(os.path.getsize(os.path.join(SALIDA, "audio", f))
               for f in os.listdir(os.path.join(SALIDA, "audio")))
    sustituir = {"{{PESO_AUDIO_MB}}": "%d" % round(peso / 1e6)}
    for n, (original, h, tam) in huellas.items():
        sustituir["{{ORIGINAL_%d}}" % n] = original
        sustituir["{{SHA_%d}}" % n] = h
        sustituir["{{MB_%d}}" % n] = "%.1f" % (tam / 1e6)

    DOCUMENTOS = [tuple(d) for d in C["documentos"]]

    pares_fidelidad, renderizados = [], {}
    for fuente, dest_html, dest_word, tipo, advertencia in DOCUMENTOS:
        src = os.path.join(AQUI, fuente)
        if not os.path.isfile(src):
            falla("falta el documento fuente %s" % fuente)
        md = io.open(src, encoding="utf-8").read()
        for k, v in sustituir.items():
            md = md.replace(k, v)
        if "{{" in md:
            falla("quedan marcadores sin sustituir en %s: %s" % (fuente, re.findall(r"\{\{\w+\}\}", md)))
        md = enlazar(md)
        if dest_html.startswith("anexos/"):
            md = md.replace("](<Transcripciones/", "](<../Transcripciones/")
            md = re.sub(r"\]\(<(?!\.\./)([^>]+\.(?:html|docx))>\)", r"](<../\1>)", md)
        out_md = os.path.join(RENDER, os.path.basename(fuente))
        io.open(out_md, "w", encoding="utf-8").write(md)
        renderizados[fuente] = out_md
        py_ok(os.path.join(SCRIPTS, "md2html.py"), out_md, os.path.join(SALIDA, dest_html),
              "--tipo", tipo, "--advertencia", advertencia,
              "--sonda", os.path.join(SALIDA, "audio", nombre_audio(*_SONDA)))
        if dest_word:
            py_ok(os.path.join(SCRIPTS, "md2docx.py"), out_md, os.path.join(SALIDA, dest_word))
            pares_fidelidad.append((os.path.join(SALIDA, dest_word), out_md))
    print("Documentos: %d paginas, %d Word" % (len(DOCUMENTOS), len(pares_fidelidad)))

    # La nota externa, si esta entrega trae una. Se regenera desde su fuente porque
    # el Word original llevaba las marcas de un bloque de codigo a la vista. Solo
    # cambia ese bloque; el resto del texto va tal cual.
    _nota = C.get("nota_externa")
    if _nota:
        nota_md = io.open(os.path.join(DESPACHO, _nota["fuente"]), encoding="utf-8").read()
        bloques_nota = re.findall(r"```text\n.*?\n```", nota_md, re.S)
        if len(bloques_nota) != 1 or _nota["marca"] not in bloques_nota[0]:
            falla("la nota externa no tiene el bloque esperado; no se toca a ciegas")
        nota_md = nota_md.replace(bloques_nota[0], _nota["bloque"])
        nota_render = os.path.join(RENDER, _nota["render"])
        io.open(nota_render, "w", encoding="utf-8").write(nota_md)
        nota_docx = os.path.join(SALIDA, _nota["destino"])
        py_ok(os.path.join(SCRIPTS, "md2docx.py"), nota_render, nota_docx)
        pares_fidelidad.append((nota_docx, nota_render))

    # ------------------------------------------------------------- 5. comprobar
    print("\nComprobaciones:")
    for n, _o, _h in AUDIOS:
        pares_fidelidad.append((os.path.join(SALIDA, "Word", "Audio %d - transcripcion.docx" % n),
                                os.path.join(RENDER, "transcripciones", "Audio %d.md" % n)))
    malas = []
    for docx, md in pares_fidelidad:
        code, out = py(os.path.join(SCRIPTS, "verificar_fidelidad.py"), docx, md)
        if not re.search(r"\sok\s*$", out.strip().splitlines()[-1]):
            malas.append(out.strip().splitlines()[-1])
    if malas:
        falla("Word que perdio contenido:\n  " + "\n  ".join(malas))
    print("  Word: %d documentos, todos con el 100 %% del contenido" % len(pares_fidelidad))

    for fuente in ("1 - Resumen de la reunion.md", "2 - Lo que hay que oir.md"):
        code, out = py(os.path.join(SCRIPTS, "verificar_citas.py"), renderizados[fuente], ORIGEN, *OTRAS)
        ultima = [l for l in out.splitlines() if "citas comprobadas" in l]
        if code != 0 or not ultima:
            falla("citas no textuales en %s:\n%s" % (fuente, out))
        print("  Citas de «%s»: %s" % (fuente[4:-3], ultima[0].strip()))

    import docx as _docx
    crudos = []
    for docx_path in glob.glob(os.path.join(SALIDA, "**", "*.docx"), recursive=True):
        d = _docx.Document(docx_path)
        texto = "\n".join(p.text for p in d.paragraphs)
        texto += "\n".join(c.text for t in d.tables for f in t.rows for c in f.cells)
        if "](<" in texto or "[[A" in texto:
            crudos.append(os.path.relpath(docx_path, SALIDA))
    for pagina in glob.glob(os.path.join(SALIDA, "**", "*.html"), recursive=True):
        t = io.open(pagina, encoding="utf-8").read()
        if "[[A" in t or "](&lt;" in t:
            crudos.append(os.path.relpath(pagina, SALIDA))
    if crudos:
        falla("quedo sintaxis de enlace sin convertir en: %s" % crudos)
    print("  Sin sintaxis de enlace cruda en Word ni en las paginas")

    rotos, absolutas = [], []
    for pagina in glob.glob(os.path.join(SALIDA, "**", "*.html"), recursive=True):
        txt = io.open(pagina, encoding="utf-8").read()
        if re.search(r"HITMA|[A-Za-z]:[\\/]{1,2}Users", txt):
            absolutas.append(os.path.relpath(pagina, SALIDA))
        rutas = re.findall(r'href="([^"#][^"]*)"', txt)
        rutas += [m for m in re.findall(r'"(?:ruta|sonda)":\s*"([^"]+)"', txt)]
        for r in rutas:
            if re.match(r"^(https?:|mailto:|data:|blob:)", r):
                continue
            destino = os.path.normpath(os.path.join(os.path.dirname(pagina), unquote(r.split("#")[0])))
            if not os.path.exists(destino):
                rotos.append("%s -> %s" % (os.path.relpath(pagina, SALIDA), r))
    if absolutas:
        falla("paginas con rutas de esta maquina dentro: %s" % absolutas)
    if rotos:
        falla("enlaces rotos:\n  " + "\n  ".join(rotos))
    print("  Enlaces y rutas de audio: todos resuelven dentro del paquete; ninguna ruta de esta maquina")

    # ------------------------------------------------------------------ 6. zip
    zpath = SALIDA + ".zip"
    with zipfile.ZipFile(zpath, "w") as z:
        for raiz, _, archivos in os.walk(SALIDA):
            for f in sorted(archivos):
                p = os.path.join(raiz, f)
                arc = os.path.join(NOMBRE, os.path.relpath(p, SALIDA))
                z.write(p, arc, zipfile.ZIP_STORED if f.endswith(".mp4") else zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(zpath) as z:
        if z.testzip() is not None:
            falla("el zip salio corrupto")
        n_arch = len(z.namelist())
    print("\nZip: %s  (%d archivos, %.0f MB)" % (os.path.basename(zpath), n_arch, os.path.getsize(zpath) / 1e6))
    print("LISTO.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
