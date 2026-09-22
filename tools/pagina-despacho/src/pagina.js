/* Superficie de trabajo del despacho — ADR-020 y ADR-022.
 *
 * Este archivo solo CONECTA piezas. No sabe de transcripciones: sabe de bloques,
 * anclas y riesgos (ver contrato.js). Cualquier metodo que emita ese contrato
 * gana pagina sin tocar nada de aqui.
 *
 * Reglas que no se pueden romper:
 *  - Cero red. Ninguna peticion, a nada, por ningun motivo.
 *  - El texto ya viene renderizado: si este script falla, la pagina se lee entera.
 *  - Lo que ella marca NO es prueba de nada (ADR-022 §4).
 *  - Una correccion es anotacion, nunca edicion del texto derivado (§5).
 */
import './estilo.css'
import { leerContrato, nodoDe, hms } from './contrato.js'
import { crearEstado, ETIQUETA } from './estado.js'
import { crearMedios } from './medios.js'
import { crearFranja } from './franja.js'
import { montarTeclado } from './teclado.js'

const $ = (s, r = document) => r.querySelector(s)
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s))

const C = leerContrato($('#datos'))
let filtro = 'todo'
let foco = null
let franja = null

/* --------------------------------------------------------------- utilidades */
const visibles = () => C.bloques.filter((b) => pasaFiltro(b))

function pasaFiltro(b) {
  const hecho = !!estado.de(b.id)
  if (filtro === 'todo') return true
  if (filtro === 'dudoso') return b.riesgo !== 'ninguno'
  if (filtro === 'pendiente') return b.riesgo !== 'ninguno' && !hecho
  if (filtro === 'hecho') return hecho
  return true
}

async function copiar(texto) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(texto); return true
    }
  } catch { /* cae al respaldo: en file:// el portapapeles moderno no existe */ }
  try {
    const t = document.createElement('textarea')
    t.value = texto
    t.style.cssText = 'position:fixed;top:-1000px;opacity:0'
    document.body.appendChild(t); t.select()
    const ok = document.execCommand('copy')
    document.body.removeChild(t)
    return ok
  } catch { return false }
}

function procedencia(b) {
  const e = estado.de(b.id)
  const donde = b.ancla.tipo === 'tiempo' ? `minuto ${hms(b.ancla.inicio)}`
    : b.ancla.tipo === 'pagina' ? `p. ${b.ancla.n}` : ''
  const base = `— ${C.documento.origen || C.documento.titulo}${donde ? ', ' + donde : ''}. `
             + `${C.documento.tipoMaterial || 'Material derivado'}`
  // Una linea CORREGIDA se copia con la correccion, no con el texto de la maquina:
  // antes salia el texto equivocado con la etiqueta «cotejado con el original».
  if (e?.estado === 'corregido') {
    return e.correccion
      ? `${base}. Texto corregido por usted tras oír el original el ${e.fecha}; la transcripción automática decía otra cosa.`
      : `${base}, marcado por usted como incorrecto el ${e.fecha}, sin escribir la corrección.`
  }
  if (e?.estado === 'confirmado') return `${base}, cotejado con el original el ${e.fecha}.`
  if (e?.estado === 'oido') return `${base}, oído en el original el ${e.fecha} sin poder confirmar el texto.`
  return `${base}, NO cotejado con el original.`
}

function textoDe(b) {
  const e = estado.de(b.id)
  if (e?.estado === 'corregido' && e.correccion) return e.correccion
  return $('.texto', nodoDe(b)).textContent.trim()
}

/* -------------------------------------------------------------------- estado */
const estado = crearEstado(C.clave, (id) => {
  if (id === null) { C.bloques.forEach(pintarBloque); aplicarFiltro() }
  pintarProgreso(); pintarAviso(); franja?.refrescar()
})

/* --------------------------------------------------------------------- foco */
function enfocar(id, { llevarAlAudio = false } = {}) {
  const b = C.porId.get(id)
  if (!b) return
  foco = id
  $$('.seg.enfocado').forEach((n) => n.classList.remove('enfocado'))
  const n = nodoDe(b)
  if (n) {
    n.classList.add('enfocado')
    n.scrollIntoView({ block: 'center', behavior: 'smooth' })
  }
  franja?.enfocar(id)
  if (llevarAlAudio && b.ancla.tipo === 'tiempo') medios.irA(b.ancla.inicio)
}

function mover(paso) {
  const lista = visibles()
  if (!lista.length) return
  const i = lista.findIndex((b) => b.id === foco)
  const j = i < 0 ? (paso > 0 ? 0 : lista.length - 1)
                  : Math.min(lista.length - 1, Math.max(0, i + paso))
  enfocar(lista[j].id)
}

function marcarFoco(tipo) {
  if (!foco) { mover(1); return }
  if (tipo === 'corregido') {
    const previo = estado.de(foco)?.correccion || ''
    const v = prompt('Escriba lo que SÍ dice el original.\n\n'
      + 'No se modifica la transcripción: queda como anotación suya, con la fecha.', previo)
    if (v === null) return
    estado.marcar(foco, 'corregido', v.trim())
  } else {
    estado.marcar(foco, tipo)
  }
  pintarBloque(C.porId.get(foco))
  aplicarFiltro()
}

/* ------------------------------------------------------------------ pintado */
function pintarBloque(b) {
  const n = nodoDe(b)
  if (!n) return
  const e = estado.de(b.id)
  n.classList.toggle('comprobado', !!e)
  $$('.acciones button', n).forEach((x) =>
    x.classList.toggle('marcado', !!e && x.dataset.a === e.estado))
  $('.sello', n)?.remove()
  $('.correccion', n)?.remove()
  if (!e) return

  const s = document.createElement('p')
  s.className = 'sello'
  s.textContent = `${ETIQUETA[e.estado]} por usted el ${e.fecha}. `
    + 'Es constancia de que fue al original, no de que el texto sea correcto.'
  n.insertBefore(s, $('.acciones', n))

  if (e.estado === 'corregido' && e.correccion) {
    const c = document.createElement('p')
    c.className = 'correccion'
    c.innerHTML = '<span class="et">Lo que sí dice el original, según usted:</span>'
    c.append(document.createTextNode(e.correccion))
    n.insertBefore(c, $('.acciones', n))
  }
}

function aplicarFiltro() {
  C.bloques.forEach((b) => nodoDe(b)?.classList.toggle('oculto', !pasaFiltro(b)))
  pintarProgreso()
}

function hechas() {
  const n = estado.cuantos()
  return n === 1 ? '1 comprobada' : `${n} comprobadas`
}

function pintarProgreso() {
  const el = $('#progreso-texto')
  if (!el) return
  const pend = C.dudosos.filter((b) => !estado.de(b.id)).length
  el.textContent = pend
    ? `${hechas()} · ${pend === 1 ? 'queda 1' : `quedan ${pend}`} con motivo de duda`
    : C.dudosos.length ? `${hechas()} · ninguna pendiente`
                       : hechas()
}

function pintarAviso() {
  const el = $('#aviso-persistencia')
  if (!el) return
  const p = []
  if (!estado.almacenOK) p.push('Este navegador no conserva lo marcado al cerrar la página.')
  if (estado.sucio) p.push('Tiene marcas que aún no ha guardado en un archivo: use «Guardar lo comprobado».')
  el.textContent = p.join(' ')
  el.hidden = !p.length
}

/* ------------------------------------------------------------------- medios */
const medios = crearMedios($('#audio'), C.audio, {
  alTiempo(t) {
    $('#reloj-actual').textContent = hms(t)
    franja?.playhead(t)
    const b = C.bloques.find((x) => x.ancla.tipo === 'tiempo'
      && t >= x.ancla.inicio && t < x.ancla.fin)
    if (b && b.id !== sonando) {
      $$('.seg.sonando').forEach((n) => n.classList.remove('sonando'))
      nodoDe(b)?.classList.add('sonando')
      sonando = b.id
    }
  },
  alEstado(s) {
    if (s.sonando !== undefined) $('#btn-play').textContent = s.sonando ? '❚❚' : '▶'
    if (s.listo === undefined) return
    $('#reproductor').hidden = !s.listo
    $('#sin-audio').hidden = s.listo
    if (s.texto) $('#reloj-total').textContent = s.texto
    $$('.hora').forEach((h) => { h.disabled = !s.listo })
  },
})
let sonando = null

/* ------------------------------------------------------------ enlace directo */
// «pagina.html#t=1140» o «#t=00:19:00» llega a ese punto y lo enfoca. NO lo hace
// sonar: el navegador no deja reproducir hasta que ella pulse algo, y fingir que
// va a sonar seria peor que decirle que pulse.
function segundosDe(v) {
  if (!v) return null
  if (/^\d+(\.\d+)?$/.test(v)) return parseFloat(v)
  const p = v.split(':').map(Number)
  return p.some(Number.isNaN) ? null : p.reduce((a, x) => a * 60 + x, 0)
}

let relojAviso = null
function irAlEnlace() {
  const m = /(?:^#|&)t=([^&]+)/.exec(location.hash)
  const t = segundosDe(m && decodeURIComponent(m[1]))
  if (t === null) return
  const conTiempo = C.bloques.filter((b) => b.ancla.tipo === 'tiempo')
  // Primero la linea cuya hora VISIBLE es la del enlace: las horas se muestran
  // truncadas al segundo, y una linea que empieza en 355,2 s se ve como 00:05:55.
  // Sin esto, el enlace a 00:05:55 caia en la linea anterior.
  let b = conTiempo.find((x) => x.ancla.inicio >= t && x.ancla.inicio < t + 1)
       || conTiempo.find((x) => t >= x.ancla.inicio && t < x.ancla.fin)
  // Si el minuto cae donde la transcripcion no tiene texto, se va a la linea
  // ANTERIOR: al oir desde ahi se pasa por el hueco. Ir a la siguiente hacia
  // saltarse justo lo que habia que oir — a veces un nombre que otras lecturas
  // si recogieron.
  const hueco = !b
  if (hueco) b = [...conTiempo].reverse().find((x) => x.ancla.inicio < t) || conTiempo[0]
  if (!b) return
  if (filtro !== 'todo') $('[data-filtro="todo"]')?.click()
  enfocar(b.id)
  const el = $('#aviso-enlace')
  if (!el) return
  el.textContent = hueco
    ? `El minuto ${hms(t)} cae en un hueco de la transcripción: ahí no hay texto. Pulse ↵ (Enter) y lo oirá desde la línea anterior.`
    : `Está en el minuto ${hms(t)}. Pulse ↵ (Enter) o la hora del bloque para oírlo.`
  el.hidden = false
  clearTimeout(relojAviso)
  relojAviso = setTimeout(() => { el.hidden = true }, 9000)
}

/* ------------------------------------------------------------------- montaje */
function montarBloque(b) {
  const n = nodoDe(b)
  if (!n) return
  n.addEventListener('click', () => { if (foco !== b.id) enfocar(b.id) })
  $('.hora', n)?.addEventListener('click', (e) => {
    e.stopPropagation(); enfocar(b.id, { llevarAlAudio: true })
  })

  // Una accion primaria visible; el resto se despliega. Un panel con cinco
  // botones por bloque inunda al revisor y frena la revision.
  const acc = document.createElement('div')
  acc.className = 'acciones'
  acc.innerHTML = `
    <button type="button" data-a="confirmado" class="primaria">Confirmado</button>
    <details class="mas"><summary>más</summary>
      <button type="button" data-a="oido">Oído</button>
      <button type="button" data-a="corregido">Corregir…</button>
      <button type="button" data-a="copiar">Copiar con procedencia</button>
      <button type="button" data-a="copiar-solo">Solo el texto</button>
    </details>`
  n.appendChild(acc)

  acc.addEventListener('click', async (ev) => {
    const x = ev.target.closest('button')
    if (!x) return
    ev.stopPropagation()
    const a = x.dataset.a
    if (a === 'copiar' || a === 'copiar-solo') {
      const txt = textoDe(b)
      const ok = await copiar(a === 'copiar' ? `«${txt}»\n${procedencia(b)}` : txt)
      const antes = x.textContent
      x.textContent = ok ? 'Copiado' : 'No se pudo copiar'
      setTimeout(() => { x.textContent = antes }, 1500)
      return
    }
    foco = b.id
    marcarFoco(a)
  })

  if (b.alternativas.length) {
    const d = document.createElement('details')
    d.className = 'alternativas'
    d.innerHTML = `<summary>Otras lecturas automáticas escribieron algo distinto</summary>`
    b.alternativas.forEach((alt) => {
      const p = document.createElement('p')
      p.innerHTML = `<span class="et">${alt.fuente}</span>`
      p.append(document.createTextNode(alt.texto))
      d.appendChild(p)
    })
    n.insertBefore(d, acc)
  }

  pintarBloque(b)
}

function iniciar() {
  // Sin bloques es un documento para leer: ni filtros, ni contador, ni «Guardar
  // lo comprobado» sobre algo que no tiene nada que comprobar.
  if (!C.bloques.length) return
  $('#barra').hidden = false
  C.bloques.forEach(montarBloque)

  franja = crearFranja($('#franja'), C, estado, (id) =>
    enfocar(id, { llevarAlAudio: true }))
  franja.refrescar()

  $$('.chip').forEach((c) => c.addEventListener('click', () => {
    $$('.chip').forEach((o) => o.classList.toggle('activo', o === c))
    filtro = c.dataset.filtro
    aplicarFiltro()
  }))
  $('#btn-play')?.addEventListener('click', () => medios.alternar())
  $('#btn-exportar')?.addEventListener('click', () => estado.exportar(C.documento))
  $('#btn-importar')?.addEventListener('click', () => $('#archivo-estado').click())
  $('#archivo-estado')?.addEventListener('change', (e) => {
    if (e.target.files[0]) {
      estado.importar(e.target.files[0], C.clave)
        .then(() => { C.bloques.forEach(pintarBloque); aplicarFiltro() })
        .catch((err) => alert(err.message))
    }
  })

  const atajos = montarTeclado({
    Space: { desc: 'Reproducir o pausar', fn: () => medios.alternar() },
    j: { desc: 'Siguiente bloque', fn: () => mover(1) },
    ArrowDown: { fn: () => mover(1) },
    k: { desc: 'Bloque anterior', fn: () => mover(-1) },
    ArrowUp: { fn: () => mover(-1) },
    Enter: { desc: 'Oír el bloque enfocado', fn: () => foco && enfocar(foco, { llevarAlAudio: true }) },
    c: { desc: 'Marcar como confirmado', fn: () => marcarFoco('confirmado') },
    o: { desc: 'Marcar como oído', fn: () => marcarFoco('oido') },
    x: { desc: 'Corregir', fn: () => marcarFoco('corregido') },
    s: { desc: 'Copiar con procedencia', fn: async () => {
      if (!foco) return
      const b = C.porId.get(foco)
      await copiar(`«${textoDe(b)}»\n${procedencia(b)}`)
    } },
    n: { desc: 'Ir a lo más grave que queda sin comprobar', fn: () => {
      const sig = C.porGravedad.find((b) => !estado.de(b.id))
      if (!sig) { pintarProgreso(); return }
      enfocar(sig.id, { llevarAlAudio: true })
    } },
    d: { desc: 'Ver solo lo que tiene motivo de duda', fn: () => $('[data-filtro="pendiente"]')?.click() },
    t: { desc: 'Ver todo', fn: () => $('[data-filtro="todo"]')?.click() },
    Escape: { desc: 'Quitar el foco', fn: () => { foco = null; $$('.seg.enfocado').forEach((n) => n.classList.remove('enfocado')) } },
    '?': { desc: 'Esta ayuda', fn: () => atajos.ayuda() },
  })
  $('#btn-ayuda')?.addEventListener('click', () => atajos.ayuda())

  window.addEventListener('beforeunload', (e) => {
    if (estado.sucio) { e.preventDefault(); e.returnValue = '' }
  })

  pintarProgreso(); pintarAviso(); aplicarFiltro()
  irAlEnlace()
  window.addEventListener('hashchange', irAlEnlace)
}

document.readyState === 'loading'
  ? document.addEventListener('DOMContentLoaded', iniciar)
  : iniciar()
