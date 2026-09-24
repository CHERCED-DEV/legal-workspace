"""Genera un guion para cdp.mjs que abre TODAS las paginas .html de un proyecto a varios
anchos y mide si algo se sale por el lado: el ancho de la pagina, si se puede desplazar de
verdad hacia el lado, y los elementos que se salen sin estar dentro de una caja que se
desplaza por si misma.

Uso:  python medir_anchos.py <proyecto> <salida_guion.json> <carpeta_fotos> [anchos...]
      (por defecto: 390 768 1024 1280 -- movil, tableta, portatil pequeno y escritorio)

Leccion (2026-09-24): midiendo solo a 390 y 1280 px no salio que a 768 y 1024 los
recuadros de ayuda OCULTOS del borde derecho daban 40 px de desplazamiento lateral.
Un elemento invisible tambien ocupa sitio: por eso aqui se cuenta tambien lo oculto.
"""
import json
import os
import pathlib
import sys

proyecto, salida, fotos = sys.argv[1], sys.argv[2], sys.argv[3]
anchos = [int(x) for x in sys.argv[4:]] or [390, 768, 1024, 1280]
EXCLUIR = ("_anteriores", "_fuentes (no enviar)", ".trabajo")

paginas = []
for raiz, dirs, archivos in os.walk(proyecto):
    dirs[:] = [d for d in dirs if d not in EXCLUIR]
    paginas += [os.path.join(raiz, a) for a in archivos if a.lower().endswith(".html")]
paginas.sort()

MEDIR = r"""(()=>{const W=document.documentElement.clientWidth,S=document.documentElement.scrollWidth;
window.scrollTo(300,scrollY);const lateral=scrollX;window.scrollTo(0,scrollY);
const sePasea=(e)=>{for(let p=e.parentElement;p&&p!==document.body;p=p.parentElement){const s=getComputedStyle(p);if(/(auto|scroll|hidden|clip)/.test(s.overflowX))return true}return false};
const fuera=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();if(!r.width||!r.height)return false;if(getComputedStyle(e).position==='fixed')return false;return r.right>W+1&&!sePasea(e)});
const hojas=fuera.filter(e=>!fuera.some(o=>o!==e&&e.contains(o)));
const mal=S>W||lateral>0;
return (mal?'MAL ':'ok  ')+'ancho '+W+' | pagina '+S+' | se desplaza al lado '+lateral+' px | '+hojas.length+' fuera'+(hojas.length?': '+hojas.slice(0,4).map(e=>(e.className&&typeof e.className==='string'?e.className.trim().split(/\s+/)[0]:e.tagName.toLowerCase())+(getComputedStyle(e).visibility==='hidden'?'(oculto)':'')+'@'+Math.round(e.getBoundingClientRect().right)).join(' , '):'')})()"""

pasos = []
for w in anchos:
    pasos.append({"tam": [w, 900]})
    for i, p in enumerate(paginas, 1):
        rel = os.path.relpath(p, proyecto).replace("\\", "/").replace("'", "")
        pasos.append({"ir": pathlib.Path(p).as_uri(), "espera": 2000})
        pasos.append({"ver": "'%d px · %02d %s'" % (w, i, rel)})
        pasos.append({"ver": MEDIR})
        if w == anchos[0]:
            pasos.append({"foto": "%d-%02d.png" % (w, i)})

json.dump({"_que_prueba": "desborde lateral de %d paginas a %s px" % (len(paginas), ", ".join(map(str, anchos))),
           "salida": fotos, "pasos": pasos}, open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(paginas), "paginas x", len(anchos), "anchos ->", salida)
