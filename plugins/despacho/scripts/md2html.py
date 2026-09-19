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
import argparse, hashlib, html, io, json, os, re, sys

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
    return t


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


def segmentos_html(doc, marcas):
    partes = []
    voz_previa = object()
    for s in doc["segmentos"]:
        i = s["i"]
        mk = marcas.get(str(i)) or marcas.get(i) or []
        voz = s.get("voz")
        cab = [f'<button type="button" class="hora" disabled>{hms(s["inicio"])}</button>']
        if voz is not None and voz != voz_previa:
            cab.append(f'<span class="voz">Hablante {html.escape(str(voz))}</span>')
        voz_previa = voz
        cuerpo = [
            f'<article class="seg{" dudoso" if mk else ""}" id="s{i}" data-i="{i}"',
            f' data-inicio="{s["inicio"]}" data-fin="{s["fin"]}" data-dudoso="{1 if mk else 0}">',
            f'<div class="seg-cab">{"".join(cab)}</div>',
            f'<p class="texto">{_linea(s["texto"])}</p>',
        ]
        if mk:
            cuerpo.append(f'<p class="motivos">{html.escape("; ".join(mk))}</p>')
        cuerpo.append("</article>")
        partes.append("".join(cuerpo))
    return "\n".join(partes)


# -------------------------------------------------------------------- pagina
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
    ap.add_argument("--audio", default=None)
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
    datos = {"titulo": titulo, "origen": os.path.basename(a.entrada),
             "tipoMaterial": "Material derivado", "version": VERSION}

    if a.datos:
        d = json.load(io.open(a.datos, encoding="utf-8"))
        doc = d.get("publicada") or d.get("principal")
        if not doc:
            sys.stderr.write("El archivo de datos no trae la pasada publicada.\n")
            return 2
        marcas = d.get("marcas", {})
        contenido = segmentos_html(doc, marcas)
        tipo = "Transcripción · superficie de trabajo"
        datos["origen"] = titulo
        if a.audio:
            # Ruta RELATIVA desde la pagina hasta la grabacion: asi la carpeta se
            # puede mover entera. Si el audio no esta, la pagina lo dice (ADR-020 §5).
            try:
                rel = os.path.relpath(os.path.abspath(a.audio),
                                      os.path.dirname(os.path.abspath(a.salida)))
            except ValueError:
                rel = os.path.basename(a.audio)
            datos["audio"] = rel.replace("\\", "/")
            if not os.path.exists(a.audio):
                sys.stderr.write("AVISO: no se encontro la grabacion en %s. "
                                 "La pagina se genera y dira que no puede comprobar.\n" % a.audio)
        n_dud = sum(1 for s in doc["segmentos"] if marcas.get(str(s["i"])))
        advertencia += (" Hay <strong>%d líneas con motivo de duda</strong> de %d. "
                        "Cada marca de tiempo reproduce ese punto de la grabación; "
                        "lo que usted marque como comprobado es constancia suya, "
                        "<strong>no verificación de ningún sistema</strong>."
                        % (n_dud, len(doc["segmentos"])))
    else:
        contenido = md_a_html(cuerpo if cuerpo else md)

    datos["clave"] = hashlib.sha256(md.encode("utf-8")).hexdigest()[:16]

    pie = ("<p>Página generada por <code>md2html %s</code> a partir de "
           "<code>%s</code>. No es el original y no sustituye al documento de Word. "
           "Lo que usted marque aquí vive en este navegador: <strong>use «Guardar lo "
           "comprobado» antes de cerrar</strong>.</p>"
           % (VERSION, html.escape(os.path.basename(a.entrada))))

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
