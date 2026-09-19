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
  const donde = b.ancla.tipo === 'tiempo' ? hms(b.ancla.inicio)
    : b.ancla.tipo === 'pagina' ? `p. ${b.ancla.n}` : ''
  const base = `— ${C.documento.origen || C.documento.titulo}${donde ? ', ' + donde : ''}. `
             + `${C.documento.tipoMaterial || 'Material derivado'}`
  return (e?.estado === 'confirmado' || e?.estado === 'corregido')
    ? `${base}, cotejado con el original el ${e.fecha}.`
    : `${base}, NO cotejado con el original.`
}

/* -------------------------------------------------------------------- estado */
const estado = crearEstado(C.clave, () => {
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

function pintarProgreso() {
  const el = $('#progreso-texto')
  if (!el) return
  const pend = C.dudosos.filter((b) => !estado.de(b.id)).length
  el.textContent = pend
    ? `${estado.cuantos()} comprobadas · quedan ${pend} con motivo de duda`
    : C.dudosos.length ? `${estado.cuantos()} comprobadas · ninguna pendiente`
                       : `${estado.cuantos()} comprobadas`
}

function pintarAviso() {
  const el = $('#aviso-persistencia')
  if (!el) return
  const p = []
  if (!estado.almacenOK) p.push('Este navegador no conserva lo marcado al cerrar la página.')
  if (estado.sucio) p.push('Tiene trabajo sin guardar: use «Guardar lo comprobado».')
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
      const txt = $('.texto', n).textContent.trim()
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
    d.innerHTML = `<summary>Las otras decodificaciones escribieron algo distinto</summary>`
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
      await copiar(`«${$('.texto', nodoDe(b)).textContent.trim()}»\n${procedencia(b)}`)
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
}

document.readyState === 'loading'
  ? document.addEventListener('DOMContentLoaded', iniciar)
  : iniciar()
