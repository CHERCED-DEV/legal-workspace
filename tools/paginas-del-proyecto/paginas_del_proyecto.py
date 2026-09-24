"""Paginas propias del proyecto: INICIO (bienvenida, barra de navegacion, temas y
tamano de letra, «Cuando guardar», recorrido con tooltips que anaden datos, carpetas y
un comprobador de lo guardado que SOLO LEE) y COMPROMISOS (todos, con filtros).

Generico: lee la forma del proyecto (ADR-023), entrega.json, los A<N> - compromisos.json,
el genoma de voz, los datos de cada grabacion y las fuentes .md de la entrega. A mano
solo se le dan el nombre largo de la reunion, el corto y la fecha de produccion.

Prototipo validado en un caso real (2026-09-24). Especificacion: docs/specs/SPEC-16.
Llevarlo a plugins/despacho es la tarea pendiente; aqui no se toca plugins/.

Uso:
  python paginas_del_proyecto.py <proyecto> <entrega.json> --reunion "<nombre largo>" --corto "<corto>" --fecha AAAA-MM-DD
No sobrescribe: si una pagina ya existe, se detiene (muevala antes a _anteriores).
"""
import argparse, glob, html, io, json, os, re
from urllib.parse import quote

TIPO = {"tarea": "Tarea", "peticion": "Petición", "propuesta": "Propuesta",
        "condicion": "Condición", "acuerdo": "Acuerdo", "no_es_compromiso": "¿Compromiso?"}

CSS = r"""
:root{--r:12px;--sombra:0 1px 2px rgba(0,0,0,.06),0 4px 16px rgba(0,0,0,.06)}
html[data-tema="claro"],html[data-tema="auto"]{--fondo:#f6f5f2;--superficie:#ffffff;--superficie-2:#f0eee9;--texto:#1d1c1a;--suave:#5d5a54;--borde:#e3dfd7;--acento:#1f4e79;--acento-suave:#e5eef7;--sobre-acento:#ffffff;--rojo:#a3201f;--rojo-suave:#fcebea;--verde:#1f6b43;--verde-suave:#e6f3ec;--ambar:#8a5a00;--ambar-suave:#fdf3e1}
html[data-tema="papel"]{--fondo:#f3ead6;--superficie:#fbf6ea;--superficie-2:#efe4cc;--texto:#3a2e1f;--suave:#6b5a42;--borde:#dccdab;--acento:#7a4a12;--acento-suave:#f1e2c6;--sobre-acento:#fffaf0;--rojo:#9b2c1c;--rojo-suave:#f6dfd6;--verde:#3e6b2a;--verde-suave:#e4ecd6;--ambar:#8a5a00;--ambar-suave:#f6e7c8}
html[data-tema="oscuro"]{--fondo:#15171a;--superficie:#1e2125;--superficie-2:#262a2f;--texto:#e9e7e2;--suave:#a9a59d;--borde:#343940;--acento:#8ab8ea;--acento-suave:#1f2d3d;--sobre-acento:#0f1720;--rojo:#f08a80;--rojo-suave:#3a1f1d;--verde:#7fcf9f;--verde-suave:#1b3325;--ambar:#f0c066;--ambar-suave:#3a2e14;--sombra:none}
html[data-tema="noche"]{--fondo:#0e1a2b;--superficie:#152438;--superficie-2:#1b2d45;--texto:#e2ebf7;--suave:#9fb3cd;--borde:#294566;--acento:#f2c14e;--acento-suave:#2b3a50;--sobre-acento:#1a1405;--rojo:#ff9a8f;--rojo-suave:#3b2130;--verde:#8fe0b0;--verde-suave:#16362c;--ambar:#f2c14e;--ambar-suave:#3a3218;--sombra:none}
html[data-tema="contraste"]{--fondo:#000;--superficie:#000;--superficie-2:#111;--texto:#fff;--suave:#fff;--borde:#fff;--acento:#ffe600;--acento-suave:#222;--sobre-acento:#000;--rojo:#ff6b6b;--rojo-suave:#000;--verde:#6bff9e;--verde-suave:#000;--ambar:#ffe600;--ambar-suave:#000;--sombra:none}
@media (prefers-color-scheme: dark){html[data-tema="auto"]{--fondo:#15171a;--superficie:#1e2125;--superficie-2:#262a2f;--texto:#e9e7e2;--suave:#a9a59d;--borde:#343940;--acento:#8ab8ea;--acento-suave:#1f2d3d;--sobre-acento:#0f1720;--rojo:#f08a80;--rojo-suave:#3a1f1d;--verde:#7fcf9f;--verde-suave:#1b3325;--ambar:#f0c066;--ambar-suave:#3a2e14;--sombra:none}}
html{font-size:17px}html[data-letra="1"]{font-size:15px}html[data-letra="3"]{font-size:19px}html[data-letra="4"]{font-size:21px}
*{box-sizing:border-box}
body{margin:0;background:var(--fondo);color:var(--texto);font-family:"Segoe UI",system-ui,-apple-system,Roboto,Arial,sans-serif;line-height:1.6}
a{color:var(--acento)}a:focus-visible,button:focus-visible,summary:focus-visible,input:focus-visible{outline:3px solid var(--acento);outline-offset:2px}
.barra{position:sticky;top:0;z-index:10;background:var(--superficie);border-bottom:1px solid var(--borde);box-shadow:var(--sombra)}
.barra-dentro{max-width:1180px;margin:0 auto;padding:.45rem 1rem;display:flex;align-items:center;gap:.6rem;flex-wrap:wrap}
.marca{font-weight:700;text-decoration:none;color:var(--texto);white-space:nowrap;margin-right:.4rem}
.navega{display:flex;gap:.3rem;flex-wrap:wrap;flex:1}
.navega a{display:inline-block;padding:.3rem .65rem;border-radius:999px;text-decoration:none;color:var(--texto);border:1px solid var(--borde);background:var(--superficie-2);font-size:.86rem;white-space:nowrap}
.navega a:hover{border-color:var(--acento)}
.navega a[aria-current="page"]{background:var(--acento);color:var(--sobre-acento);border-color:var(--acento)}
.ajustes{position:relative}
.ajustes>summary{list-style:none;cursor:pointer;padding:.3rem .7rem;border-radius:999px;border:1px solid var(--borde);background:var(--superficie-2);font-size:.86rem}
.ajustes>summary::-webkit-details-marker{display:none}
.panel-ajustes{position:absolute;right:0;top:2.3rem;background:var(--superficie);border:1px solid var(--borde);border-radius:var(--r);box-shadow:0 8px 30px rgba(0,0,0,.18);padding:.9rem;width:18.5rem}
.panel-ajustes h3{margin:.1rem 0 .5rem;font-size:.85rem;color:var(--suave);font-weight:600;text-transform:uppercase;letter-spacing:.04em}
.temas{display:grid;grid-template-columns:1fr 1fr;gap:.4rem;margin-bottom:.8rem}
.temas button,.letra button{font:inherit;font-size:.85rem;cursor:pointer;border-radius:8px;border:1px solid var(--borde);background:var(--superficie-2);color:var(--texto);padding:.4rem .5rem;display:flex;align-items:center;gap:.45rem}
.temas button[aria-pressed="true"],.letra button[aria-pressed="true"]{border:2px solid var(--acento)}
.muestra{width:1.1rem;height:1.1rem;border-radius:50%;border:1px solid rgba(0,0,0,.25);flex:none}
.letra{display:flex;gap:.4rem}.letra button{justify-content:center;flex:1}
main{max-width:1180px;margin:0 auto;padding:1.4rem 1rem 4rem}
.cabeza{background:var(--superficie);border:1px solid var(--borde);border-radius:var(--r);padding:1.4rem 1.5rem;box-shadow:var(--sombra)}
.cabeza .etiqueta{font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;color:var(--suave)}
h1{font-size:1.9rem;line-height:1.25;margin:.25rem 0 .6rem}
h2{font-size:1.35rem;margin:2.2rem 0 .8rem}
h3{font-size:1.05rem;margin:0 0 .35rem}
.chips{display:flex;gap:.45rem;flex-wrap:wrap;margin-top:.6rem}
.chip{font-size:.82rem;padding:.2rem .6rem;border-radius:999px;background:var(--superficie-2);border:1px solid var(--borde)}
.chip.aviso{background:var(--ambar-suave);border-color:var(--ambar);color:var(--texto)}
.nota{border-left:4px solid var(--ambar);background:var(--ambar-suave);padding:.8rem 1rem;border-radius:0 var(--r) var(--r) 0;margin:1rem 0}
.rejilla{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:.9rem}
.tarjeta{background:var(--superficie);border:1px solid var(--borde);border-radius:var(--r);padding:1rem 1.1rem;box-shadow:var(--sombra);display:flex;flex-direction:column;gap:.35rem}
.tarjeta p{margin:0;color:var(--suave)}
.num{display:inline-flex;align-items:center;justify-content:center;width:1.9rem;height:1.9rem;border-radius:50%;background:var(--acento);color:var(--sobre-acento);font-weight:700;font-size:.95rem}
.tarjeta .pie{margin-top:auto;display:flex;gap:.4rem;flex-wrap:wrap;align-items:center;padding-top:.5rem}
.boton{display:inline-flex;align-items:center;gap:.35rem;padding:.42rem .9rem;border-radius:8px;background:var(--acento);color:var(--sobre-acento);text-decoration:none;font-weight:600;font-size:.9rem;border:1px solid var(--acento);cursor:pointer;font-family:inherit}
.boton.secundario{background:transparent;color:var(--acento)}
.tiempo{font-size:.8rem;color:var(--suave)}
table{width:100%;border-collapse:collapse;background:var(--superficie);border:1px solid var(--borde);border-radius:var(--r);overflow:hidden}
th,td{text-align:left;padding:.6rem .8rem;border-bottom:1px solid var(--borde);vertical-align:top}
th{background:var(--superficie-2);font-size:.85rem}
td code{white-space:nowrap}code{background:var(--superficie-2);padding:.05rem .35rem;border-radius:5px;font-size:.9em;border:1px solid var(--borde)}
.pasos{counter-reset:p;list-style:none;padding:0;margin:0;display:grid;gap:.6rem}
.pasos li{background:var(--superficie);border:1px solid var(--borde);border-radius:var(--r);padding:.7rem 1rem .7rem 3.2rem;position:relative}
.pasos li::before{counter-increment:p;content:counter(p);position:absolute;left:.9rem;top:.7rem;width:1.6rem;height:1.6rem;border-radius:50%;background:var(--acento);color:var(--sobre-acento);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.85rem}
.resultado{margin-top:1rem;display:grid;gap:.5rem}
.fila{display:flex;gap:.6rem;align-items:flex-start;background:var(--superficie);border:1px solid var(--borde);border-radius:10px;padding:.6rem .8rem}
.fila .ico{font-weight:700;width:1.3rem;flex:none;text-align:center}
.fila.ok{border-color:var(--verde);background:var(--verde-suave)}.fila.ok .ico{color:var(--verde)}
.fila.mal{border-color:var(--ambar);background:var(--ambar-suave)}.fila.mal .ico{color:var(--ambar)}
.fila small{color:var(--suave)}
.arriba{position:fixed;right:1rem;bottom:1rem;z-index:9;border-radius:999px;padding:.45rem .75rem;box-shadow:var(--sombra);opacity:.9;font-size:.82rem}
footer{max-width:1180px;margin:0 auto;padding:1rem;color:var(--suave);font-size:.82rem;border-top:1px solid var(--borde)}
.filtros{position:sticky;top:3.1rem;z-index:5;background:var(--fondo);padding:.6rem 0;display:flex;flex-wrap:wrap;gap:.8rem;align-items:center;border-bottom:1px solid var(--borde)}
.grupo{display:flex;gap:.3rem;flex-wrap:wrap;align-items:center}
.grupo span{font-size:.8rem;color:var(--suave);margin-right:.2rem}
.grupo button{font:inherit;font-size:.84rem;cursor:pointer;border-radius:999px;border:1px solid var(--borde);background:var(--superficie);color:var(--texto);padding:.25rem .7rem}
.grupo button[aria-pressed="true"]{background:var(--acento);color:var(--sobre-acento);border-color:var(--acento)}
.buscar{font:inherit;font-size:.9rem;padding:.35rem .7rem;border-radius:8px;border:1px solid var(--borde);background:var(--superficie);color:var(--texto);min-width:15rem}
.cuenta{font-size:.85rem;color:var(--suave);margin-left:auto}
.cifras{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:.8rem;margin-top:1rem}
.cifra{background:var(--superficie);border:1px solid var(--borde);border-radius:var(--r);padding:.8rem 1rem}
.cifra b{font-size:1.5rem;display:block}
.compromiso{background:var(--superficie);border:1px solid var(--borde);border-left:5px solid var(--rojo);border-radius:var(--r);padding:1rem 1.2rem;margin:.9rem 0;box-shadow:var(--sombra)}
.compromiso.asumido{border-left-color:var(--verde)}
.compromiso .arriba-c{display:flex;flex-wrap:wrap;gap:.45rem;align-items:center;margin-bottom:.45rem}
.sello{font-size:.75rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:.15rem .55rem;border-radius:6px;background:var(--rojo-suave);color:var(--rojo);border:1px solid var(--rojo)}
.compromiso.asumido .sello{background:var(--verde-suave);color:var(--verde);border-color:var(--verde)}
.tipo{font-size:.8rem;padding:.12rem .55rem;border-radius:6px;border:1px solid var(--borde);background:var(--superficie-2)}
.cita{border-left:3px solid var(--borde);padding:.2rem .8rem;margin:.5rem 0;font-family:Georgia,"Times New Roman",serif;font-size:1.02rem}
dl.ficha{display:grid;grid-template-columns:max-content 1fr;gap:.25rem .9rem;margin:.4rem 0 0}
dl.ficha dt{color:var(--suave);font-size:.88rem}dl.ficha dd{margin:0}
.oculto{display:none!important}
.con-ayuda{position:relative}
.con-ayuda .pop{display:block;visibility:hidden;opacity:0;pointer-events:none;transition:opacity .12s ease,visibility 0s linear .12s;position:absolute;z-index:30;left:0;top:calc(100% + 8px);width:min(19rem,86vw);background:var(--texto);color:var(--fondo);border-radius:9px;padding:.5rem .7rem;font-size:.8rem;line-height:1.4;font-weight:400;box-shadow:0 8px 24px rgba(0,0,0,.25);text-align:left;white-space:normal}
.con-ayuda .pop::before{content:"";position:absolute;top:-6px;left:1.2rem;border:6px solid transparent;border-top:0;border-bottom-color:var(--texto)}
.con-ayuda .pop b{color:inherit}
.con-ayuda:hover .pop,.con-ayuda:focus-visible .pop,.con-ayuda:focus-within .pop{visibility:visible;opacity:1;transition:opacity .15s ease .35s,visibility 0s linear .35s}
.navega .con-ayuda .pop{top:calc(100% + 10px)}
.fila-titulo.con-ayuda .pop{left:0;right:0;width:auto;top:calc(100% + 6px)}
.info{font-size:.75rem;color:var(--suave);border:1px solid var(--borde);border-radius:999px;width:1.25rem;height:1.25rem;display:inline-flex;align-items:center;justify-content:center;flex:none;cursor:help}
.tarjeta .fila-titulo{display:flex;align-items:center;gap:.55rem;cursor:help}
.tarjeta .fila-titulo h3{margin:0;flex:1}
.guardar{border:2px solid var(--acento);background:var(--acento-suave);border-radius:var(--r);padding:1rem 1.2rem;margin:1.2rem 0}
.guardar h2{margin:.1rem 0 .6rem;font-size:1.2rem}
.guardar code{white-space:nowrap}.guardar ol{margin:.2rem 0 0;padding-left:1.3rem}.guardar li{margin:.35rem 0}
@media (hover:none){.con-ayuda .pop{display:none!important}}
.ajustes:not([open]) .panel-ajustes{display:none}
.temas button,.letra button{min-width:0}
.panel-ajustes{max-width:calc(100vw - 1rem)}
@media (max-width:760px){.barra{position:static}.barra-dentro{flex-wrap:wrap;gap:.4rem}.navega{order:3;flex:1 1 100%;min-width:0;overflow-x:auto;flex-wrap:nowrap;padding-bottom:.25rem;scrollbar-width:thin}.ajustes{margin-left:auto}.marca{margin-right:.2rem}.con-ayuda .pop{display:none!important}.panel-ajustes{position:fixed;left:.5rem;right:.5rem;top:3.2rem;width:auto}.filtros{position:static}.buscar{min-width:0;width:100%}td code{white-space:normal;word-break:break-all}table{display:block;overflow-x:auto}}
body{overflow-x:hidden}
@media (max-width:700px){h1{font-size:1.5rem}.filtros{position:static}dl.ficha{grid-template-columns:1fr}.panel-ajustes{right:-4rem}}
@media (prefers-reduced-motion: reduce){*{scroll-behavior:auto!important}}
@media print{.barra,.filtros,.arriba,.ajustes{display:none!important}body{background:#fff;color:#000}}
"""

JS_CABEZA = r"""(function(){var p={};try{p=JSON.parse(localStorage.getItem('despacho-apariencia'))||{}}catch(e){}
document.documentElement.setAttribute('data-tema',p.tema||'auto');document.documentElement.setAttribute('data-letra',p.letra||'2')})();"""

JS_COMUN = r"""
(function(){
  var K='despacho-apariencia';
  function leer(){try{return JSON.parse(localStorage.getItem(K))||{}}catch(e){return {}}}
  function guardar(p){try{localStorage.setItem(K,JSON.stringify(p))}catch(e){}}
  function marcar(){var p=leer(),t=p.tema||'auto',l=p.letra||'2';
    document.querySelectorAll('[data-poner-tema]').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-poner-tema')===t?'true':'false')});
    document.querySelectorAll('[data-poner-letra]').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-poner-letra')===l?'true':'false')});}
  document.querySelectorAll('[data-poner-tema]').forEach(function(b){b.addEventListener('click',function(){var p=leer();p.tema=b.getAttribute('data-poner-tema');guardar(p);document.documentElement.setAttribute('data-tema',p.tema);marcar()})});
  document.querySelectorAll('[data-poner-letra]').forEach(function(b){b.addEventListener('click',function(){var p=leer();p.letra=b.getAttribute('data-poner-letra');guardar(p);document.documentElement.setAttribute('data-letra',p.letra);marcar()})});
  marcar();
  var a=document.getElementById('arriba');if(a){a.addEventListener('click',function(){window.scrollTo(0,0)})}
})();
"""

JS_COMPROMISOS = r"""
(function(){
  var f={audio:'todos',estado:'todos',tipo:'todos',q:''};
  var cartas=[].slice.call(document.querySelectorAll('.compromiso'));
  function aplicar(){var n=0;cartas.forEach(function(c){
      var ok=(f.audio==='todos'||c.dataset.audio===f.audio)&&(f.estado==='todos'||c.dataset.estado===f.estado)&&(f.tipo==='todos'||c.dataset.tipo===f.tipo)&&(!f.q||c.textContent.toLowerCase().indexOf(f.q)>=0);
      c.classList.toggle('oculto',!ok);if(ok)n++});
    document.querySelectorAll('.titulo-audio').forEach(function(h){var a=h.dataset.audio;var hay=cartas.some(function(c){return c.dataset.audio===a&&!c.classList.contains('oculto')});h.classList.toggle('oculto',!hay)});
    document.getElementById('cuenta').textContent='Se ven '+n+' de '+cartas.length;}
  document.querySelectorAll('[data-filtro]').forEach(function(b){b.addEventListener('click',function(){var k=b.dataset.filtro;f[k]=b.dataset.valor;
    document.querySelectorAll('[data-filtro="'+k+'"]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});aplicar()})});
  var q=document.getElementById('buscar');q.addEventListener('input',function(){f.q=q.value.trim().toLowerCase();aplicar()});
  aplicar();
})();
"""

JS_COMPROBADOR = r"""
var PROYECTO=@@PROYECTO@@, ENTREGA=@@ENTREGA@@, CLAVE=@@CLAVE@@, META=@@META@@;
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function fecha(ms){try{return new Date(ms).toLocaleString('es-CO',{dateStyle:'medium',timeStyle:'short'})}catch(e){return ''}}
function cuantoHay(d){if(!d||typeof d!=='object')return 0;function n(o){return o&&typeof o==='object'?Object.keys(o).length:0}
  return n(d.estado)+n(d.atribucion)+n(d.ilegibles)+n(d.compromisos)+Object.values(d.voces||{}).filter(function(x){return String(x||'').trim()}).length+(Array.isArray(d.glosario)?d.glosario.length:0)}
async function hijo(dir,nombre){try{return await dir.getDirectoryHandle(nombre)}catch(e){return null}}
async function hallarProyecto(h){
  if(await hijo(h,'2-Borradores'))return h;
  var p=await hijo(h,PROYECTO);if(p&&await hijo(p,'2-Borradores'))return p;
  for await (var par of h.entries()){if(par[1].kind!=='directory')continue;var q=await hijo(par[1],PROYECTO);if(q&&await hijo(q,'2-Borradores'))return q}
  return null}
async function analizarProyecto(raiz){
  var filas=[];var b=await hijo(raiz,'2-Borradores');
  var voces=b?await hijo(b,'Voces'):null;var decl=[];
  if(voces){for await (var par of voces.entries()){var n=par[0],h=par[1];if(h.kind==='file'&&/^voces declaradas/i.test(n)&&/[.]json$/i.test(n))decl.push(h)}}
  if(!decl.length){filas.push({ok:false,t:'No está su declaración de voces en 2-Borradores\\Voces.',d:'Si ya pulsó “⤓ Guardar mi declaración (.json)” en la página de voces, el archivo está en Descargas: muévalo a 2-Borradores\\Voces y vuelva a comprobar.'})}
  for(var i=0;i<decl.length;i++){var f=await decl[i].getFile(),j=null;try{j=JSON.parse(await f.text())}catch(e){}
    if(!j||j.formato!=='despacho/voces-linea-a-linea'){filas.push({ok:false,t:esc(f.name)+': no es una declaración de voces legible.',d:''});continue}
    if(j.clave!==CLAVE){filas.push({ok:false,t:esc(f.name)+': es de otra preparación de voces.',d:'No sirve para esta reunión.'});continue}
    var nl=Object.keys(j.lineas||{}).length,cl=(j.resumen&&j.resumen.claridad)||{},partes=[],llega=true;
    Object.keys(cl).sort().forEach(function(k){var v=Math.round(cl[k]*100);if(v<META)llega=false;partes.push(k.replace('A','Audio ')+': '+v+' %')});
    filas.push({ok:!!j.declarado_por&&nl>0&&llega,t:esc(f.name)+' — declarado por '+esc(j.declarado_por||'(sin nombre)')+', '+nl+' líneas decididas.',d:'Guardado el '+fecha(f.lastModified)+' · Claridad según la página: '+esc(partes.join(' · ')||'sin datos')+(llega?' — llega a la meta en todas.':' — todavía no llega: la meta es '+META+' % en cada grabación.')})}
  var ld=b?await hijo(b,'Lo que declaré'):null,de=ld?await hijo(ld,ENTREGA):null;
  if(!de){filas.push({ok:false,t:'Todavía no hay nada guardado de las páginas de cada grabación.',d:'En cada página pulse una vez “Guardar lo comprobado” y elija la carpeta del proyecto. Se crea 2-Borradores\\Lo que declaré.'})}
  else{var grupos={};for await (var p2 of de.entries()){var nn=p2[0],hh=p2[1];if(hh.kind!=='file'||!/[.]json$/i.test(nn))continue;
      var m=nn.match(/^(.*?) - (en curso|\d{4}-\d\d-\d\d.*)[.]json$/);var base=m?m[1]:nn;grupos[base]=grupos[base]||{curso:null,copias:0};
      if(m&&m[2]==='en curso')grupos[base].curso=hh;else grupos[base].copias++}
    var bases=Object.keys(grupos).sort();if(!bases.length)filas.push({ok:false,t:'La carpeta de lo declarado existe pero está vacía.',d:''});
    for(var k=0;k<bases.length;k++){var g=grupos[bases[k]];if(!g.curso){filas.push({ok:true,t:esc(bases[k])+': '+g.copias+' copia(s) fechada(s).',d:''});continue}
      var ff=await g.curso.getFile(),dd=null;try{dd=JSON.parse(await ff.text())}catch(e){}
      var c=cuantoHay(dd);filas.push({ok:c>0,t:esc(bases[k])+': '+c+' declaraciones guardadas.',d:'Última vez: '+fecha(ff.lastModified)+' · copias fechadas: '+g.copias+(g.copias?'':' — pulse “Guardar lo comprobado” para dejar una copia fechada que no se borra.')})}}
  return filas}
async function comprobar(){
  var out=document.getElementById('resultado');
  if(!('showDirectoryPicker' in window)){out.innerHTML='<div class="fila mal"><span class="ico">!</span><div>Este navegador no permite comprobarlo desde aquí. Abra esta página con Edge o Chrome.</div></div>';return}
  var h;try{h=await window.showDirectoryPicker({id:'despacho-proyecto',mode:'read'})}catch(e){return}
  var raiz=await hallarProyecto(h);
  if(!raiz){out.innerHTML='<div class="fila mal"><span class="ico">!</span><div>Esa carpeta no es el proyecto. Elija la carpeta “'+esc(PROYECTO)+'”.</div></div>';return}
  pintar(await analizarProyecto(raiz))}
function pintar(filas){document.getElementById('resultado').innerHTML=filas.map(function(r){return '<div class="fila '+(r.ok?'ok':'mal')+'"><span class="ico">'+(r.ok?'✓':'!')+'</span><div>'+r.t+(r.d?'<br><small>'+r.d+'</small>':'')+'</div></div>'}).join('')}
document.getElementById('comprobar').addEventListener('click',comprobar);
"""

TEMAS = [("auto", "Automático", "linear-gradient(90deg,#f6f5f2 50%,#15171a 50%)"),
         ("claro", "Claro", "#f6f5f2"), ("papel", "Papel", "#f3ead6"),
         ("oscuro", "Oscuro", "#1e2125"), ("noche", "Noche azul", "#152438"),
         ("contraste", "Alto contraste", "#000")]


def url(base, ruta):
    return base + quote(ruta.replace(os.sep, "/"), safe="/#=")


def seg(t):
    h, m, s = (int(x) for x in t.split(":"))
    return h * 3600 + m * 60 + s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("proyecto")
    ap.add_argument("entrega_json")
    ap.add_argument("--reunion", required=True, help="nombre largo de la reunion")
    ap.add_argument("--corto", required=True, help="nombre corto: va en los nombres de archivo")
    ap.add_argument("--fecha", required=True, help="AAAA-MM-DD de produccion")
    a = ap.parse_args()
    P = a.proyecto
    C = json.load(io.open(a.entrega_json, encoding="utf-8"))
    E = "/".join([C.get("salida") or "2-Borradores/Entregas", C["nombre"]])
    ORIGEN = os.path.join(P, *C["origen"].split("/"))
    audios = [n for n, _f, _h in C["audios"]]
    dur, segs = {}, 0
    for n in audios:
        md = io.open(os.path.join(ORIGEN, C["transcripcion"] % n), encoding="utf-8").read()
        m = re.search(r"\*\*Duración:\*\*\s*(\d\d):(\d\d):(\d\d)", md)
        dur[n] = "%d min %02d s" % (int(m.group(1)) * 60 + int(m.group(2)), int(m.group(3))) if m else "—"
        segs += (int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))) if m else 0
    gen = C.get("genoma")
    G = json.load(io.open(os.path.join(P, *gen.split("/")), encoding="utf-8")) if gen else None
    voces_html = sorted(glob.glob(os.path.join(P, "2-Borradores", "Voces", "Voces - *.html")))
    ruta_voces = os.path.relpath(voces_html[-1], P) if voces_html else None
    comp_dir = C.get("compromisos")
    comp = {}
    for n in audios:
        r = os.path.join(P, *comp_dir.split("/"), "A%d - compromisos.json" % n) if comp_dir else ""
        comp[n] = json.load(io.open(r, encoding="utf-8"))["compromisos"] if r and os.path.isfile(r) else []
    total = sum(len(v) for v in comp.values())
    guia = sorted(glob.glob(os.path.join(P, "2-Borradores", "Guia ilustrada - *.docx")))
    ruta_guia = os.path.relpath(guia[-1], P) if guia else None
    nombre_inicio = "INICIO - %s.html" % a.corto
    ruta_comp = "2-Borradores/Compromisos/Compromisos - %s - %s.html" % (a.corto, a.fecha)
    proyecto = os.path.basename(os.path.normpath(P))

    # Los tooltips dicen lo que la tarjeta o el boton NO dicen, sacado de los datos del
    # proyecto (pedido del dueño: «no debe hacer lo mismo, debe mejorar lo que ya hace»).
    FUENTES = os.path.dirname(os.path.abspath(a.entrega_json))

    def fuente_de(fragmento):
        for d in C["documentos"]:
            if fragmento in d[1]:
                r = os.path.join(FUENTES, *d[0].split("/"))
                return io.open(r, encoding="utf-8").read() if os.path.isfile(r) else ""
        return ""
    md_res, md_oir, md_man = fuente_de("Resumen"), fuente_de("Lo que hay que oir"), fuente_de("Manual")
    apartados = [h[3:].strip() for h in md_res.splitlines() if h.startswith("## ")]
    n_citas = len(re.findall(r"«[^»]{2,}»", md_res))
    puntos = {n: len(re.findall(r"^\| \[\[A%d \d\d:\d\d:\d\d hora\]\]" % n, md_oir, re.M)) for n in audios}
    primera = re.search(r"^\| \[\[A\d \d\d:\d\d:\d\d hora\]\] \| \*\*(.+?)\*\*", md_oir, re.M)
    discordia = {}
    for n in audios:
        dj = json.load(io.open(os.path.join(ORIGEN, "datos", "A%d - datos completos.json" % n), encoding="utf-8"))
        discordia[n] = sum(1 for v in dj.get("ventanas", []) if v.get("medio", 1) < 0.8)
    n_voces, n_lineas, n_resc = (len((G or {}).get(k, [])) for k in ("voces", "lineas", "rescates"))
    sin_cerrar = sum(1 for v in comp.values() for c in v if not c.get("cerrado"))
    n_img = 0
    if ruta_guia:
        try:
            import docx
            n_img = len(docx.Document(os.path.join(P, ruta_guia)).inline_shapes)
        except Exception:
            n_img = 0
    NB = "\u00a0"
    miles = lambda x: "{:,}".format(x).replace(",", ".")
    AYUDA = {
        "inicio": "Recorrido, cuándo guardar, qué hay en cada carpeta y el botón para comprobar lo guardado.",
        "resumen": "%d apartados; el primero, “%s”. %d citas, cada una con su minuto." % (len(apartados), apartados[0] if apartados else "", n_citas),
        "oir": "%d puntos marcados (%s)." % (sum(puntos.values()), " · ".join("Audio %d: %d" % (n, puntos[n]) for n in audios))
               + (" Empiece por: %s" % primera.group(1).rstrip(".") + "." if primera else ""),
        "voces": "%d voces · %s líneas · %d rescates sin oír. Si la máquina acierta el 90%s%% en su prueba, sus propuestas cuentan." % (n_voces, miles(n_lineas), n_resc, NB),
        "compromisos": "%d en total (%s). %d sin cerrar: el filtro “Sin cerrar” los deja solos." % (total, " · ".join("Audio %d: %d" % (n, len(comp[n])) for n in audios), sin_cerrar),
        "manual": "%d apartados: botones, teclas, dónde queda guardado y qué hacer si algo falla." % len([h for h in md_man.splitlines() if h.startswith("## ")]),
        "guia": "Word con %d imágenes de las pantallas, para leer o imprimir." % n_img,
    }
    for n in audios:
        AYUDA["a%d" % n] = "%s · %d compromisos · %d tramos de 20%ss donde las lecturas no coinciden." % (dur[n], len(comp[n]), discordia[n], NB)
    nav = [("inicio", "Inicio", nombre_inicio),
           ("resumen", "Resumen", E + "/1 - Resumen de la reunion.html"),
           ("oir", "Qué oír", E + "/2 - Lo que hay que oir.html")]
    if ruta_voces:
        nav.append(("voces", "Voces", ruta_voces))
    nav.append(("compromisos", "Compromisos", ruta_comp))
    for n in audios:
        nav.append(("a%d" % n, "Audio %d" % n, E + "/Transcripciones/Audio %d - oir y marcar.html" % n))
    nav.append(("manual", "Manual", E + "/3 - Manual de uso.html"))
    if ruta_guia:
        nav.append(("guia", "Guía", ruta_guia))

    def pagina(titulo, base, actual, cuerpo, extra_js=""):
        enl = "".join('<span class="con-ayuda"><a href="%s"%s aria-describedby="ayuda-%s">%s</a><span class="pop" role="tooltip" id="ayuda-%s">%s</span></span>'
                      % (url(base, r), ' aria-current="page"' if k == actual else "", k, html.escape(t), k, AYUDA.get(k, ""))
                      for k, t, r in nav)
        temas = "".join('<button type="button" data-poner-tema="%s"><span class="muestra" style="background:%s"></span>%s</button>'
                        % (k, bg, t) for k, t, bg in TEMAS)
        letra = "".join('<button type="button" data-poner-letra="%s" aria-label="%s">%s</button>' % (k, lab, t)
                        for k, lab, t in (("1", "Letra pequeña", "A−"), ("2", "Letra normal", "A"),
                                          ("3", "Letra grande", "A+"), ("4", "Letra muy grande", "A++")))
        return ("<!doctype html><html lang=\"es\" data-tema=\"auto\" data-letra=\"2\"><head><meta charset=\"utf-8\">"
                "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>%s</title>"
                "<script>%s</script><style>%s</style></head><body>"
                "<header class=\"barra\"><div class=\"barra-dentro\"><a class=\"marca\" href=\"%s\">⌂ %s</a>"
                "<nav class=\"navega\" aria-label=\"Páginas del proyecto\">%s</nav>"
                "<details class=\"ajustes\"><summary>🎨 Apariencia</summary><div class=\"panel-ajustes\">"
                "<h3>Tema</h3><div class=\"temas\">%s</div><h3>Tamaño de letra</h3><div class=\"letra\">%s</div>"
                "</div></details></div></header><main>%s</main>"
                "<footer>Página del proyecto “%s”, preparada el %s por un programa. Es material derivado: el original son las grabaciones. "
                "El tema y el tamaño de letra se recuerdan en este navegador.</footer>"
                "<button class=\"boton arriba\" id=\"arriba\" type=\"button\" aria-label=\"Volver arriba\">↑ Arriba</button>"
                "<script>%s</script><script>%s</script></body></html>") % (
                    html.escape(titulo), JS_CABEZA, CSS, url(base, nombre_inicio), html.escape(a.corto), enl, temas, letra,
                    cuerpo, html.escape(proyecto), a.fecha, JS_COMUN, extra_js)

    # ------------------------------------------------------------------ INICIO
    b0 = ""
    fila_audios = " · ".join('<a href="%s">Audio %d</a> (%s)' % (url(b0, E + "/Transcripciones/Audio %d - oir y marcar.html" % n), n, dur[n]) for n in audios)
    tarjetas = [
        ("Resumen de la reunión", "Qué se trató y cómo quedó cada asunto. Cada cita lleva su minuto: púlselo y suena la grabación en ese punto.", E + "/1 - Resumen de la reunion.html", "10 min"),
        ("Lo que hay que oír", "Dónde duda la máquina, empezando por lo que tiene algo en juego.", E + "/2 - Lo que hay que oir.html", "5 min"),
    ]
    if ruta_voces:
        tarjetas.append(("Quién habla: la página de voces", "<b>El trabajo principal.</b> Oiga cada línea y diga quién habla, en %d grabaciones a la vez. Meta: %d %% claro en cada una." % (len(audios), round(100 * (G or {}).get("meta_claridad", 0.85))), ruta_voces, "lo que haga falta"))
    tarjetas.append(("Compromisos", "Los %d puntos donde alguien pide, propone o asume algo, con filtros y el minuto de cada uno." % total, ruta_comp, "10 min"))
    tarjetas.append(("Cada grabación", "Comprobar el texto, contar lo que no se entiende, declarar los compromisos y anotar el glosario.", E + "/Transcripciones/Audio %d - oir y marcar.html" % audios[0], "lo que haga falta"))
    claves = ["resumen", "oir"] + (["voces"] if ruta_voces else []) + ["compromisos", "grabaciones"]
    corta = lambda s: re.sub(r"(\d+) min (\d+) s", r"\1:\2", s)
    AYUDA["grabaciones"] = ("%s. Teclas: <b>N</b>, lo más grave sin comprobar; <b>L</b>, lo que no se entiende; <b>?</b>, todas.") % " · ".join(
                                "Audio %d: %s" % (n, corta(dur[n])) for n in audios)
    cards = "".join('<article class="tarjeta"><div class="fila-titulo con-ayuda" tabindex="0" aria-describedby="t-ayuda-%d">'
                    '<span class="num">%d</span><h3>%s</h3><span class="info" aria-hidden="true">i</span>'
                    '<span class="pop" role="tooltip" id="t-ayuda-%d">%s</span></div><p>%s</p>'
                    '<div class="pie"><a class="boton" href="%s">Abrir →</a><span class="tiempo">%s</span></div></article>'
                    % (i + 1, i + 1, html.escape(t), i + 1, AYUDA.get(claves[i], ""), d, url(b0, r), html.escape(tm))
                    for i, (t, d, r, tm) in enumerate(tarjetas))
    carpetas = [
        ("1-Documentos recibidos", "Lo que llegó, tal cual.", "No. Es de solo lectura"),
        ("2-Borradores\\Transcripciones", "La transcripción de cada grabación en texto, subtítulos y datos.", "No hace falta"),
        ("2-Borradores\\Voces", "La página de voces. Aquí deja su declaración de voces.", "Sí: aquí deja su declaración"),
        ("2-Borradores\\Compromisos", "La página de compromisos y los datos de donde sale.", "Solo para leer"),
        ("2-Borradores\\Entregas", "Resumen, lo que hay que oír, manual, páginas de cada grabación y sus Word.", "Aquí trabaja"),
        ("2-Borradores\\Lo que declaré", "Lo que usted guarda en las páginas de cada grabación. Aparece al guardar por primera vez.", "Lo escribe la página por usted"),
        ("3-Para presentar", "Vacía. Solo usted pone aquí lo que dé por terminado.", "Cuando usted decida"),
    ]
    tabla = "".join("<tr><td><code>%s</code></td><td>%s</td><td>%s</td></tr>" % (html.escape(c), html.escape(q), html.escape(t)) for c, q, t in carpetas)
    cuerpo = """
<section class="cabeza"><div class="etiqueta">Proyecto · inicio</div><h1>Bienvenida — %s</h1>
<p>Aquí está todo lo que se preparó a partir de %d grabaciones recibidas el %s (%s). <b>La máquina transcribió, propuso quién habla y señaló lo que parecen compromisos. Usted lo aclara oyendo</b>: lo que usted declara es la fuente de verdad, y con eso se hacen después el acta y la lista de compromisos con sus responsables.</p>
<div class="chips"><span class="chip aviso">Nadie ha oído todavía las grabaciones</span><span class="chip">Las voces van sin nombre</span><span class="chip">Los compromisos van sin responsable</span><span class="chip">La fecha de la reunión está por llenar</span></div></section>
<div class="nota"><b>Abra todo desde esta carpeta, con Edge o Chrome, y no mueva ni renombre nada.</b> Las páginas se buscan unas a otras y a las grabaciones por su sitio. Use siempre el mismo navegador y el mismo computador.</div>
<section class="guardar" aria-labelledby="cuando-guardar"><h2 id="cuando-guardar">💾 Cuándo guardar</h2>
<p>Lo que usted marca se guarda solo en el navegador, pero <b>eso no es entregar</b>: si se borran los datos del navegador, se pierde. Al terminar <b>cada</b> sesión de trabajo:</p>
<ol><li><b>Página de voces</b> → pestaña <b>Lo que se entrega</b> → <b>⤓ Guardar mi declaración (.json)</b>. El archivo va a Descargas: muévalo a <code>2-Borradores\\Voces</code>. Si ya hay uno anterior, déjelo: se usa el más reciente.</li>
<li><b>Cada grabación</b> → <b>Guardar lo comprobado</b>. La primera vez elija la carpeta del proyecto; desde entonces se guarda sola cada vez que marca algo, y cada vez que pulse el botón deja además una copia con fecha. Si la página dice <i>“Tiene marcas que aún no ha guardado”</i>, púlselo.</li>
<li>Antes de devolvernos el proyecto: <a href="#comprobar-titulo">🔎 Comprobar lo que he guardado</a>.</li></ol></section>
<h2>Su recorrido</h2><div class="rejilla">%s</div>
<p>Grabaciones: %s. ¿Dudas? El <a href="%s">manual de uso</a>%s.</p>
<h2>Dos herramientas, dos maneras de guardar</h2>
<table><tr><th>Herramienta</th><th>Cómo se guarda</th><th>Dónde tiene que quedar</th></tr>
<tr><td><b>Página de voces</b></td><td>Se guarda sola en el navegador. Para entregarlo, pestaña <b>Lo que se entrega</b> → <b>⤓ Guardar mi declaración (.json)</b>: va a <b>Descargas</b>.</td><td>Muévalo a <code>2-Borradores\\Voces</code></td></tr>
<tr><td><b>Páginas de cada grabación</b></td><td>Pulse una vez <b>Guardar lo comprobado</b> y elija la carpeta del proyecto: desde entonces se guarda sola. Cada vez que lo pulse deja además una copia con fecha que no se borra.</td><td>Queda en <code>2-Borradores\\Lo que declaré</code></td></tr></table>
<h2 id="comprobar-titulo">Comprobar lo que he guardado</h2>
<p>Antes de devolvernos el proyecto, pulse el botón y elija la carpeta <b>%s</b>. La página <b>solo lee</b>: no escribe, no mueve ni borra nada. Le dice si su declaración de voces está donde tiene que estar, cuánto llega cada grabación a la meta, y qué hay guardado de cada página.</p>
<button class="boton" id="comprobar" type="button">🔎 Comprobar lo que he guardado</button><div class="resultado" id="resultado" aria-live="polite"></div>
<h2>Qué hay en cada carpeta</h2>
<table><tr><th>Carpeta</th><th>Qué guarda</th><th>¿La toca usted?</th></tr>%s</table>
<h2>Cuándo ha terminado, y qué nos devuelve</h2>
<ol class="pasos"><li>La página de voces dice que <b>cada grabación llega al %d %%</b>, y ha revisado los compromisos.</li>
<li>Guardó su declaración de voces y la movió de Descargas a <code>2-Borradores\\Voces</code>.</li>
<li>El botón <b>Comprobar lo que he guardado</b> sale todo en verde.</li>
<li>Nos avisa con un “ya terminé” y nos devuelve <b>la carpeta del proyecto entera</b>.</li></ol>
<h2>Antes de citar nada</h2>
<ol class="pasos"><li>La transcripción la hizo un programa. <b>Ninguna cita debería salir de aquí sin oír su minuto.</b></li>
<li>“Voz 3” o “Hablante 2” son voces, no personas. <b>No hay nombres hasta que usted los ponga.</b></li>
<li>Lo que usted marca es <b>constancia suya</b>, no una verificación del sistema.</li></ol>
""" % (html.escape(a.reunion), len(audios), html.escape(C.get("audio_recibido", "")),
       "unos %d minutos" % round(segs / 60),
       cards, fila_audios, url(b0, E + "/3 - Manual de uso.html"),
       (' y la <a href="%s">guía ilustrada en Word</a> lo explican paso a paso' % url(b0, ruta_guia)) if ruta_guia else " lo explica paso a paso",
       html.escape(proyecto), tabla, round(100 * (G or {}).get("meta_claridad", 0.85)))
    js = (JS_COMPROBADOR.replace("@@PROYECTO@@", json.dumps(proyecto, ensure_ascii=False))
          .replace("@@ENTREGA@@", json.dumps(C["nombre"], ensure_ascii=False))
          .replace("@@CLAVE@@", json.dumps((G or {}).get("clave", ""))).replace("@@META@@", str(round(100 * (G or {}).get("meta_claridad", 0.85)))))
    salida_inicio = os.path.join(P, nombre_inicio)

    # ------------------------------------------------------------- COMPROMISOS
    bC = "../../"

    def enlace_min(n, t, texto=None):
        return '<a href="%s">%s</a>' % (url(bC, E + "/Transcripciones/Audio %d - oir y marcar.html#t=%d" % (n, seg(t))), texto or t)

    def minutos(txt, n):
        txt = html.escape(txt, quote=False)
        txt = re.sub(r"\(A(\d) (\d\d:\d\d:\d\d)\)", lambda m: "(%s)" % enlace_min(int(m.group(1)), m.group(2), "Audio %s, %s" % (m.group(1), m.group(2))), txt)
        partes = re.split(r"(<a [^>]*>.*?</a>)", txt)
        return "".join(p if p.startswith("<a ") else
                       re.sub(r"(?<![\w/=])(\d\d:\d\d:\d\d)(?![\w])", lambda m: enlace_min(n, m.group(1)), p)
                       for p in partes)

    cifras = "".join('<div class="cifra"><a href="%s">Audio %d</a><b>%d</b>%d asumidos · %d sin cerrar</div>'
                     % (url(bC, E + "/Transcripciones/Audio %d - oir y marcar.html" % n), n, len(comp[n]),
                        sum(1 for c in comp[n] if c.get("cerrado")), sum(1 for c in comp[n] if not c.get("cerrado"))) for n in audios)
    tipos = sorted({c.get("tipo") for v in comp.values() for c in v if c.get("tipo")})
    filtros = ('<div class="filtros"><div class="grupo"><span>Grabación</span><button type="button" data-filtro="audio" data-valor="todos" aria-pressed="true">Todas</button>%s</div>'
               '<div class="grupo"><span>Estado</span><button type="button" data-filtro="estado" data-valor="todos" aria-pressed="true">Todos</button>'
               '<button type="button" data-filtro="estado" data-valor="sin-cerrar" aria-pressed="false">Sin cerrar</button>'
               '<button type="button" data-filtro="estado" data-valor="asumido" aria-pressed="false">Asumidos</button></div>'
               '<div class="grupo"><span>Tipo</span><button type="button" data-filtro="tipo" data-valor="todos" aria-pressed="true">Todos</button>%s</div>'
               '<input class="buscar" id="buscar" type="search" placeholder="Buscar: escuela, planeación, informe…" aria-label="Buscar en los compromisos">'
               '<span class="cuenta" id="cuenta"></span></div>') % (
        "".join('<button type="button" data-filtro="audio" data-valor="A%d" aria-pressed="false">Audio %d</button>' % (n, n) for n in audios),
        "".join('<button type="button" data-filtro="tipo" data-valor="%s" aria-pressed="false">%s</button>' % (t, html.escape(TIPO.get(t, t))) for t in tipos))
    bloques = []
    for n in audios:
        bloques.append('<h2 class="titulo-audio" data-audio="A%d">Audio %d — %d señalados</h2>' % (n, n, len(comp[n])))
        for c in comp[n]:
            asum = bool(c.get("cerrado"))
            dicho = " / ".join("«%s»" % html.escape(x.strip(), quote=False) for x in c["cita"].split(" / "))
            ficha = [("Plazo", html.escape("no se dice" if c.get("plazo") in (None, "", "no consta") else c["plazo"], quote=False))]
            if c.get("falta"):
                ficha.append(("Qué falta", html.escape("; ".join(c["falta"]), quote=False)))
            if c.get("por_que_estado"):
                ficha.append(("Por qué está así", minutos(c["por_que_estado"], n)))
            if c.get("nota"):
                ficha.append(("Ojo", minutos(c["nota"], n)))
            bloques.append(
                '<article class="compromiso%s" data-audio="A%d" data-estado="%s" data-tipo="%s">'
                '<div class="arriba-c"><span class="sello">%s</span><span class="tipo">%s</span>'
                '<a class="boton secundario" href="%s">▶ Oírlo en el Audio %d, %s</a></div>'
                '<p>%s</p><div class="cita">%s</div><dl class="ficha">%s</dl></article>' % (
                    " asumido" if asum else "", n, "asumido" if asum else "sin-cerrar", c.get("tipo") or "",
                    "Asumido, según la lectura" if asum else "Sin cerrar", html.escape(TIPO.get(c.get("tipo"), c.get("tipo") or "")),
                    url(bC, E + "/Transcripciones/Audio %d - oir y marcar.html#t=%d" % (n, seg(c["minuto"]))), n, c["minuto"],
                    html.escape(c["de_que_se_trata"], quote=False), dicho,
                    "".join("<dt>%s</dt><dd>%s</dd>" % (k, v) for k, v in ficha)))
    cuerpoC = """
<section class="cabeza"><div class="etiqueta">Compromisos · lectura automática</div><h1>Compromisos de la reunión</h1>
<p>Los <b>%d puntos</b> donde, según la lectura de la transcripción, alguien pide, propone o asume algo. <b>Nadie los ha oído, y ninguno lleva quién lo asume.</b> Pulse <b>▶ Oírlo</b> en cada uno: se abre la página de su grabación en ese minuto, y allí, en la etiqueta roja, declara si es un compromiso, quién lo asume y el plazo.</p>
<div class="cifras">%s</div>
<p class="tiempo">“Asumido” quiere decir que quien habla lo dice en primera persona. Quién es esa persona lo declara usted.</p></section>
%s%s
<h2>Lo que esta página NO dice</h2>
<ol class="pasos"><li><b>No dice quién asume ningún compromiso.</b> Eso lo declara usted, oyéndolo.</li>
<li><b>Que la frase exista no quiere decir que alguien se obligara.</b> Es una lectura de la transcripción.</li>
<li><b>No convierte ningún plazo hablado en una fecha.</b></li>
<li><b>Puede faltar alguno:</b> lo que la máquina no transcribió no se pudo leer.</li></ol>
""" % (total, cifras, filtros, "".join(bloques))
    salida_comp = os.path.join(P, *ruta_comp.split("/"))

    for ruta, contenido in ((salida_inicio, pagina("Inicio — " + a.corto, b0, "inicio", cuerpo, js)),
                            (salida_comp, pagina("Compromisos — " + a.corto, bC, "compromisos", cuerpoC, JS_COMPROMISOS))):
        if os.path.exists(ruta):
            raise SystemExit("DETENIDO: ya existe %s (muévalo a _anteriores antes de regenerar)" % ruta)
        io.open(ruta, "w", encoding="utf-8", newline="\n").write(contenido)
        print("escrito", ruta, "%.0f KB" % (len(contenido.encode("utf-8")) / 1024))


if __name__ == "__main__":
    main()
