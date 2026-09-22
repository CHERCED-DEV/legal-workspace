# -*- coding: utf-8 -*-
"""verdad_de_referencia — quién habla de verdad, marcado por una persona.

    python verdad_de_referencia.py hoja  <datos.json> [--desde 00:03:00] [--minutos 5]
                                                      [--salida hoja.md]
    python verdad_de_referencia.py medir <hoja.md> <datos.json> [<otros datos.json> ...]

Sin esto no se puede mejorar nada: hoy se puede comparar un metodo con otro,
pero **no se sabe cual acierta**. `ADR-017` lo pide como validacion 3 desde el
principio y nadie lo ha hecho.

`hoja` escoge un tramo y saca una hoja para marcar oyendo: una linea por
intervencion, con su minuto y su texto, y un hueco. Quien oye escribe una letra
por persona -- A, B, C... --, `?` si no lo sabe y `+` si hablan varias a la vez.

`medir` lee esa misma hoja ya marcada y dice, para uno o varios metodos, que
porcentaje de lineas quedaria atribuido a la persona correcta, a quien funde y
a quien parte. Un solo archivo de ida y vuelta: no hay que copiar nada a mano.

Por que se mide POR LINEA y no por fotograma: el error academico de diarizacion
(DER) mezcla habla no detectada, falsa alarma y confusion de hablante. Lo que
este producto promete es otra cosa mas concreta -- que la linea que ella va a
citar este atribuida a quien la dijo --, y eso es lo que se mide aqui. La
contrapartida se dice sin adornos: esta hoja NO mide el habla que el programa
no detecto, porque parte de las lineas que el programa ya encontro.

Lo que este programa NO hace:
  · No oye nada. La referencia la produce una persona, y sin ella no hay medida.
  · No arregla la separacion de voces: la mide.
  · No convierte lo marcado en material del caso: es instrumentacion.
"""
import argparse, hashlib, io, itertools, json, os, re, sys

MARCA = re.compile(r"^#(\d+)\s+(\d\d:\d\d:\d\d)\s+\[([^\]]*)\]")


def hms(s):
    s = max(0, int(float(s or 0)))
    return "%02d:%02d:%02d" % (s // 3600, (s % 3600) // 60, s % 60)


def s_de(t):
    p = [int(x) for x in t.split(":")]
    return p[0] * 3600 + p[1] * 60 + p[2] if len(p) == 3 else p[0] * 60 + p[1]


def falla(msg):
    sys.stderr.write("\nDETENIDO: " + msg + "\n")
    raise SystemExit(2)


def cargar(ruta):
    if not os.path.isfile(ruta):
        falla("no está %s" % ruta)
    d = json.load(io.open(ruta, encoding="utf-8"))
    doc = d.get("publicada") or d.get("principal")
    if not doc:
        falla("%s no trae la pasada publicada" % os.path.basename(ruta))
    return d, doc


# ---------------------------------------------------------------------- hoja
def mejor_tramo(doc, minutos):
    """El tramo con mas intervenciones cortas: conversacion, no monologo.

    Se elige SIN mirar las etiquetas de voz de la maquina, y a proposito: si se
    escogiera el tramo donde ella cree que hay mas cambios, se estaria midiendo
    justo donde ya le va bien. Lo que senala conversacion sin depender de su
    criterio es el ritmo: muchas intervenciones cortas seguidas."""
    seg = doc["segmentos"]
    if not seg:
        falla("esa transcripción no tiene segmentos")
    ancho = minutos * 60
    fin_total = seg[-1]["fin"]
    mejor, mejor_n = 0.0, -1
    t = 0.0
    while t + ancho <= max(fin_total, ancho):
        dentro = [s for s in seg if t <= s["inicio"] < t + ancho]
        cortas = sum(1 for s in dentro if s["fin"] - s["inicio"] <= 4.0)
        if cortas > mejor_n:
            mejor, mejor_n = t, cortas
        t += 30.0
    return mejor, mejor_n


def hoja(args):
    d, doc = cargar(args.datos)
    minutos = args.minutos
    if args.desde:
        ini = float(s_de(args.desde))
        motivo = "lo pediste tú"
    else:
        ini, cambios = mejor_tramo(doc, minutos)
        motivo = ("es el tramo con más intervenciones cortas (%d), o sea el que más se parece "
                  "a una conversación. Se eligió **sin mirar** qué voces cree la máquina que "
                  "hay ahí" % cambios)
    fin = ini + minutos * 60
    dentro = [s for s in doc["segmentos"] if ini <= s["inicio"] < fin]
    if not dentro:
        falla("no hay ninguna línea entre %s y %s" % (hms(ini), hms(fin)))

    w = []
    w.append("# Quién habla de verdad — %s a %s\n\n" % (hms(ini), hms(fin)))
    w.append("**Para qué es esto.** Hoy se puede comparar un método con otro, pero **no se "
             "sabe cuál acierta**. Esta hoja, marcada oyendo, es la única forma de saberlo.\n\n")
    w.append("**Tramo elegido:** %s. **%d líneas**, %d minutos de audio.\n\n" % (motivo, len(dentro), minutos))
    w.append("## Cómo marcarla\n\n")
    w.append("Oiga el tramo con la página de esa grabación y escriba **una letra por persona** "
             "dentro de los corchetes: `A` para la primera voz que oiga, `B` para la segunda, y "
             "así. **La misma persona lleva siempre la misma letra.**\n\n")
    w.append("- `[?]` si no distingue quién es. **Es una respuesta válida y no se cuenta como error.**\n")
    w.append("- `[+]` si hablan **varias a la vez**.\n")
    w.append("- Deje el hueco vacío si se saltó la línea.\n\n")
    w.append("**No mire los números de hablante de la transcripción antes de marcar.** Si los "
             "mira, marcará lo mismo que la máquina y la medición no valdrá nada.\n\n")
    w.append("---\n\n```text\n")
    for s in dentro:
        texto = " ".join(s["texto"].split())[:76]
        w.append("#%-5d %s [ ]  %s\n" % (s["i"], hms(s["inicio"]), texto))
    w.append("```\n\n---\n\n")
    w.append("**Cuando esté marcada**, mídase con:\n\n")
    w.append("```bash\npython verdad_de_referencia.py medir \"<esta hoja>.md\" \"<datos>.json\"\n```\n")

    # Sin nombre por defecto a proposito: esto es instrumentacion y NO va a la
    # carpeta del caso, asi que no le toca inventarse un nombre alli. Lo dice
    # quien lo corre.
    salida = args.salida
    if os.path.exists(salida) and not args.forzar:
        falla("ya existe %s (usa --forzar para reemplazarlo)" % salida)
    io.open(salida, "w", encoding="utf-8").write("".join(w))
    print("OK  %s  -  %d líneas de %s a %s" % (os.path.basename(salida), len(dentro), hms(ini), hms(fin)))
    if args.pagina:
        if not args.audio:
            falla("--pagina necesita --audio: una página para marcar sin la grabación no sirve")
        try:
            rel = os.path.relpath(os.path.abspath(args.audio),
                                  os.path.dirname(os.path.abspath(args.pagina)))
        except ValueError:
            rel = os.path.basename(args.audio)
        if not os.path.exists(args.audio):
            sys.stderr.write("AVISO: no está la grabación en %s. La página lo dirá.\n" % args.audio)
        clave = hashlib.sha256("".join(w).encode("utf-8")).hexdigest()[:16]
        pagina(dentro, "".join(w), os.path.basename(salida),
               "%s a %s" % (hms(ini), hms(fin)), rel.replace("\\", "/"), clave, args.pagina)
        print("OK  %s  -  para marcar pulsando, con el audio al lado" % os.path.basename(args.pagina))
    print("    Marcarla es trabajo de una persona: el programa no oye.")
    return 0


# --------------------------------------------------------------------- pagina
# Una pagina aparte, y NO la del producto: esto es instrumentacion. Meterlo en la
# pagina que usa ella anadiria un modo mas a algo que ya hace bastante.
#
# Dos reglas de esta pagina, y las dos son para que la medida valga:
#   1. NO ensena que voz cree la maquina. Ensenarla contagia la respuesta, y
#      entonces se estaria midiendo si la persona sabe copiar.
#   2. Al exportar devuelve la MISMA hoja de texto, con las marcas puestas en su
#      sitio. Asi `medir` la lee sin cambiar una linea de codigo.
PAGINA = """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><link rel="icon" href="data:,">
<title>Quién habla de verdad — %(titulo)s</title>
<style>
 :root { --tinta:#1a1a1a; --papel:#fbfaf7; --linea:#dcd8cf; --acento:#7a5c00; --hecho:#1f5c3d; }
 * { box-sizing:border-box }
 body { margin:0; background:var(--papel); color:var(--tinta);
        font:16px/1.5 ui-serif,Georgia,serif }
 header { position:sticky; top:0; background:var(--papel); border-bottom:1px solid var(--linea);
          padding:.8rem 1rem; z-index:5 }
 .env { max-width:46rem; margin:0 auto }
 h1 { font-size:1.15rem; margin:0 0 .3rem }
 .ayuda { font:13px/1.45 ui-sans-serif,system-ui,sans-serif; color:#5b5750 }
 .barra { display:flex; gap:.5rem; align-items:center; flex-wrap:wrap;
          font:13px ui-sans-serif,system-ui,sans-serif; margin-top:.5rem }
 button { font:inherit; border:1px solid var(--linea); background:#fff; border-radius:5px;
          padding:.25rem .6rem; cursor:pointer }
 button:hover { border-color:var(--acento) }
 main { max-width:46rem; margin:1rem auto 6rem; padding:0 1rem }
 .fila { display:flex; gap:.6rem; align-items:baseline; padding:.35rem .5rem;
         border-left:3px solid transparent; border-radius:4px }
 .fila.foco { background:#fff; border-left-color:var(--acento); box-shadow:0 1px 4px #0001 }
 .fila.hecha .txt { color:#6b6760 }
 .hora { font:12px ui-monospace,monospace; color:#6b6760; cursor:pointer; white-space:nowrap }
 .hora:hover { color:var(--acento); text-decoration:underline }
 .letra { font:600 13px ui-sans-serif,system-ui,sans-serif; min-width:2.2rem; text-align:center;
          border-radius:4px; padding:.05rem .3rem }
 .letra.puesta { background:var(--hecho); color:#fff }
 .letra.duda { background:#8a8a8a; color:#fff }
 .txt { flex:1 }
 .pie { position:fixed; bottom:0; left:0; right:0; background:var(--papel);
        border-top:1px solid var(--linea); padding:.5rem 1rem;
        font:13px ui-sans-serif,system-ui,sans-serif }
 .teclas b { display:inline-block; border:1px solid var(--linea); border-radius:4px;
             padding:0 .3rem; background:#fff; font-family:ui-monospace,monospace }
 mark { background:#ffe9a8 }
</style></head><body>
<header><div class="env">
  <h1>Quién habla de verdad — %(titulo)s</h1>
  <p class="ayuda"><strong>Esta página no te enseña qué voz cree la máquina, a propósito.</strong>
     Si la vieras, marcarías lo mismo que ella y la medición no valdría nada.</p>
  <div class="barra">
    <audio id="au" preload="metadata"></audio>
    <button id="play">▶</button><span id="reloj">00:00:00</span>
    <span id="prog"></span>
    <button id="exportar">Guardar la hoja marcada</button>
    <span id="aviso" style="color:#8a4b00"></span>
  </div>
</div></header>
<main id="lista"></main>
<div class="pie"><div class="env teclas">
  <b>A</b>…<b>F</b> la persona &nbsp; <b>0</b> no sé &nbsp; <b>9</b> varias a la vez &nbsp;
  <b>espacio</b> oír o parar &nbsp; <b>↵</b> repetir &nbsp; <b>↑ ↓</b> moverse &nbsp;
  <b>retroceso</b> borrar la marca
</div></div>
<script id="datos" type="application/json">%(datos)s</script>
<script>
const D = JSON.parse(document.getElementById('datos').textContent);
const LL = 'ABCDEF';
const clave = 'verdad:' + D.clave;
let marcas = {};
try { marcas = JSON.parse(localStorage.getItem(clave) || '{}') } catch (e) {}
let foco = 0;
const au = document.getElementById('au');
au.src = encodeURI(D.audio);

const hms = s => [s/3600, s%%3600/60, s%%60].map(x => String(Math.floor(x)).padStart(2,'0')).join(':');

const lista = document.getElementById('lista');
D.lineas.forEach((l, k) => {
  const d = document.createElement('div');
  d.className = 'fila'; d.id = 'f' + k;
  d.innerHTML = '<span class="hora">' + hms(l.t) + '</span>' +
                '<span class="letra" id="l' + k + '"></span>' +
                '<span class="txt"></span>';
  d.querySelector('.txt').textContent = l.texto;
  d.querySelector('.hora').onclick = e => { e.stopPropagation(); ir(k, true) };
  d.onclick = () => ir(k, false);
  lista.appendChild(d);
});

function pintar(k) {
  const l = document.getElementById('l' + k), m = marcas[D.lineas[k].id];
  l.textContent = m || '';
  l.className = 'letra' + (m ? (m === '?' || m === '+' ? ' duda' : ' puesta') : '');
  document.getElementById('f' + k).classList.toggle('hecha', !!m);
}
function progreso() {
  const n = Object.keys(marcas).length;
  document.getElementById('prog').textContent = n + ' de ' + D.lineas.length + ' marcadas';
  document.getElementById('aviso').textContent = n && !D.guardada ? 'sin guardar en archivo' : '';
}
function ir(k, sonar) {
  foco = Math.max(0, Math.min(D.lineas.length - 1, k));
  document.querySelectorAll('.fila.foco').forEach(n => n.classList.remove('foco'));
  const n = document.getElementById('f' + foco);
  n.classList.add('foco');
  n.scrollIntoView({ block: 'center', behavior: 'smooth' });
  if (sonar) { au.currentTime = Math.max(0, D.lineas[foco].t - 0.3); au.play() }
}
function marcar(letra) {
  const id = D.lineas[foco].id;
  if (letra === null) delete marcas[id]; else marcas[id] = letra;
  try { localStorage.setItem(clave, JSON.stringify(marcas)) } catch (e) {}
  D.guardada = false;
  pintar(foco); progreso();
  if (letra !== null && foco < D.lineas.length - 1) ir(foco + 1, true);
}
document.addEventListener('keydown', e => {
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  const k = e.key.toUpperCase();
  if (LL.includes(k) && k.length === 1) { e.preventDefault(); marcar(k) }
  else if (k === '0') { e.preventDefault(); marcar('?') }
  else if (k === '9') { e.preventDefault(); marcar('+') }
  else if (e.key === 'Backspace') { e.preventDefault(); marcar(null) }
  else if (e.key === ' ') { e.preventDefault(); au.paused ? au.play() : au.pause() }
  else if (e.key === 'Enter') { e.preventDefault(); ir(foco, true) }
  else if (e.key === 'ArrowDown') { e.preventDefault(); ir(foco + 1, false) }
  else if (e.key === 'ArrowUp') { e.preventDefault(); ir(foco - 1, false) }
});
document.getElementById('play').onclick = () => au.paused ? au.play() : au.pause();
au.ontimeupdate = () => document.getElementById('reloj').textContent = hms(au.currentTime);
au.onplay = () => document.getElementById('play').textContent = '❚❚';
au.onpause = () => document.getElementById('play').textContent = '▶';
au.onerror = () => document.getElementById('aviso').textContent =
  'No se encontró la grabación junto a esta página';

document.getElementById('exportar').onclick = () => {
  // Se devuelve la MISMA hoja, con las marcas en su sitio: `medir` no cambia.
  // Sustitucion LITERAL, sin expresiones regulares: cada linea trae su prefijo
  // exacto. Una barra invertida de menos dentro de una plantilla se come el
  // arreglo entero y el boton seguia diciendo que habia guardado.
  let texto = D.hoja, puestas = 0;
  for (const l of D.lineas) {
    const m = marcas[l.id];
    if (!m) continue;
    const antes = texto;
    texto = texto.replace(l.pref + '[ ]', l.pref + '[' + m + ']');
    if (texto !== antes) puestas++;
  }
  if (puestas !== Object.keys(marcas).length) {
    document.getElementById('aviso').textContent =
      'NO se guardaron ' + (Object.keys(marcas).length - puestas) + ' marcas: avise';
    return;
  }
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([texto], { type: 'text/markdown' }));
  a.download = D.nombre;
  a.click();
  D.guardada = true;
  progreso();
};
window.addEventListener('beforeunload', e => {
  if (Object.keys(marcas).length && !D.guardada) { e.preventDefault(); e.returnValue = '' }
});
D.lineas.forEach((_, k) => pintar(k));
progreso(); ir(0, false);
// El audio empieza en el tramo, no en el minuto cero: pulsar espacio sin
// haber elegido linea sonaba el principio de la grabacion, que no es esto.
au.addEventListener('loadedmetadata', () => { au.currentTime = D.lineas[0].t; }, { once: true });
</script></body></html>
"""


def pagina(dentro, hoja_texto, nombre_hoja, titulo, audio_rel, clave, salida):
    datos = {
        "titulo": titulo, "audio": audio_rel, "clave": clave, "nombre": nombre_hoja,
        "hoja": hoja_texto, "guardada": True,
        "lineas": [{"id": s["i"], "t": round(s["inicio"], 2),
                    "pref": "#%-5d %s " % (s["i"], hms(s["inicio"])),
                    "texto": " ".join(s["texto"].split())} for s in dentro],
    }
    html = PAGINA % {"titulo": html_escapa(titulo),
                     "datos": json.dumps(datos, ensure_ascii=False)}
    io.open(salida, "w", encoding="utf-8").write(html)
    return salida


def html_escapa(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# --------------------------------------------------------------------- medir
def leer_hoja(ruta):
    if not os.path.isfile(ruta):
        falla("no está la hoja %s" % ruta)
    ref, sin_marcar, dudosas, solapadas = {}, 0, 0, 0
    for l in io.open(ruta, encoding="utf-8"):
        m = MARCA.match(l.strip())
        if not m:
            continue
        i, letra = int(m.group(1)), m.group(3).strip().upper()
        if not letra:
            sin_marcar += 1
        elif letra == "?":
            dudosas += 1
        elif letra == "+":
            solapadas += 1
        else:
            ref[i] = letra
    if not ref:
        falla("esa hoja no tiene ni una línea marcada. Hay que oírla primero: el programa no oye.")
    return ref, sin_marcar, dudosas, solapadas


def emparejar(ref, dicho):
    """La mejor correspondencia posible entre grupos y personas.

    Se prueba con la mejor correspondencia a proposito: un metodo no tiene por
    que llamar «1» a quien la persona llamo «A». Lo que se mide es si SEPARA a
    las mismas personas, no como las numera."""
    personas = sorted(set(ref.values()))
    grupos = sorted({dicho[i] for i in ref if i in dicho and dicho[i] is not None},
                    key=lambda x: str(x))
    if not grupos:
        return {}, 0
    if len(grupos) <= 7 and len(personas) <= 7:
        mejor, mejor_n = {}, -1
        for combo in itertools.permutations(personas, min(len(personas), len(grupos))):
            mapa = dict(zip(grupos, combo))
            n = sum(1 for i, p in ref.items() if i in dicho and mapa.get(dicho[i]) == p)
            if n > mejor_n:
                mejor, mejor_n = mapa, n
        return mejor, mejor_n
    # Muchas voces: cada grupo va a la persona con la que mas coincide.
    mapa = {}
    for g in grupos:
        cuenta = {}
        for i, p in ref.items():
            if dicho.get(i) == g:
                cuenta[p] = cuenta.get(p, 0) + 1
        if cuenta:
            mapa[g] = max(cuenta, key=cuenta.get)
    n = sum(1 for i, p in ref.items() if mapa.get(dicho.get(i)) == p)
    return mapa, n


def medir_uno(ref, datos):
    d, doc = cargar(datos)
    dicho = {s["i"]: s.get("voz") for s in doc["segmentos"]}
    comunes = {i: p for i, p in ref.items() if i in dicho}
    if not comunes:
        falla("la hoja y %s no comparten ni una línea: ¿son de la misma grabación?"
              % os.path.basename(datos))
    mapa, aciertos = emparejar(comunes, dicho)
    # Fusiones: un grupo que se reparte entre varias personas de la referencia.
    fusiones, divisiones = [], []
    por_grupo, por_persona = {}, {}
    for i, p in comunes.items():
        g = dicho.get(i)
        por_grupo.setdefault(g, {}).setdefault(p, 0)
        por_grupo[g][p] += 1
        por_persona.setdefault(p, {}).setdefault(g, 0)
        por_persona[p][g] += 1
    for g, personas in por_grupo.items():
        if len([p for p, n in personas.items() if n >= 2]) > 1:
            fusiones.append((g, sorted(personas)))
    for p, grupos in por_persona.items():
        if len([g for g, n in grupos.items() if n >= 2]) > 1:
            divisiones.append((p, len([g for g, n in grupos.items() if n >= 2])))
    sin_voz = sum(1 for i in comunes if dicho.get(i) is None)
    return {"archivo": os.path.basename(datos), "lineas": len(comunes), "aciertos": aciertos,
            "porcentaje": 100.0 * aciertos / len(comunes), "fusiones": fusiones,
            "divisiones": divisiones, "sin_voz": sin_voz, "grupos": len(por_grupo)}


def medir(args):
    ref, sin_marcar, dudosas, solapadas = leer_hoja(args.hoja)
    print("Referencia: %d líneas marcadas por una persona." % len(ref))
    if dudosas or solapadas or sin_marcar:
        print("            %d sin distinguir, %d con varias voces a la vez, %d sin marcar."
              % (dudosas, solapadas, sin_marcar))
        print("            Esas no se cuentan ni a favor ni en contra.")
    print("            Personas distintas oídas: %d\n" % len(set(ref.values())))

    print("%-34s %8s %9s %8s" % ("método", "líneas", "acierta", "grupos"))
    resultados = []
    for datos in args.datos:
        r = medir_uno(ref, datos)
        resultados.append(r)
        print("%-34s %8d %8.1f%% %8d" % (r["archivo"][:34], r["lineas"], r["porcentaje"], r["grupos"]))

    for r in resultados:
        detalles = []
        for g, personas in r["fusiones"]:
            detalles.append("FUNDE en el grupo %s a: %s" % (g, ", ".join(personas)))
        for p, n in r["divisiones"]:
            detalles.append("PARTE a la persona %s en %d grupos" % (p, n))
        if r["sin_voz"]:
            detalles.append("%d línea%s sin voz asignada"
                            % (r["sin_voz"], "" if r["sin_voz"] == 1 else "s"))
        if detalles:
            print("\n%s:" % r["archivo"])
            for x in detalles:
                print("  - %s" % x)

    print("\nLo que esta medida NO dice: nada sobre el habla que el programa no detectó,")
    print("porque parte de las líneas que ya encontró. Y una referencia es lo que UNA")
    print("persona oyó: si se marcó deprisa, mide lo que se marcó deprisa.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="orden", required=True)

    h = sub.add_parser("hoja", help="sacar el tramo para marcar oyendo")
    h.add_argument("datos")
    h.add_argument("--desde", default=None, help="hh:mm:ss; si no, se elige el tramo más difícil")
    h.add_argument("--minutos", type=int, default=5)
    h.add_argument("--salida", required=True, help="dónde se escribe la hoja")
    h.add_argument("--pagina", default=None, help="además, una página para marcar pulsando")
    h.add_argument("--audio", default=None, help="la grabación, para la página")
    h.add_argument("--forzar", action="store_true")
    h.set_defaults(fn=hoja)

    m = sub.add_parser("medir", help="comparar uno o varios métodos contra la hoja marcada")
    m.add_argument("hoja")
    m.add_argument("datos", nargs="+")
    m.set_defaults(fn=medir)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
