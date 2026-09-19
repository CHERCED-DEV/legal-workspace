/* Superficie de trabajo del despacho — ADR-020 y ADR-022.
 *
 * Reglas que este archivo NO puede romper:
 *  - Cero red. Ninguna peticion, a nada, por ningun motivo.
 *  - El contenido ya viene renderizado por el generador. Esto solo ANADE
 *    interaccion: si este script falla, la pagina se sigue leyendo entera.
 *  - El estado que marca ella NO es prueba de nada (ADR-022 §4).
 *  - Una correccion es anotacion, nunca edicion del texto derivado (§5).
 */
import './estilo.css'

const $ = (s, r = document) => r.querySelector(s)
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s))

const DATOS = (() => {
  try { return JSON.parse($('#datos')?.textContent || '{}') } catch { return {} }
})()

const hms = (s) => {
  s = Math.max(0, Math.floor(s || 0))
  const h = String(Math.floor(s / 3600)).padStart(2, '0')
  const m = String(Math.floor((s % 3600) / 60)).padStart(2, '0')
  const g = String(s % 60).padStart(2, '0')
  return `${h}:${m}:${g}`
}
const hoy = () => new Date().toLocaleDateString('es-CO', { year: 'numeric', month: '2-digit', day: '2-digit' })

/* ------------------------------------------------------------- persistencia
 * El almacenamiento del navegador NO es fiable en archivos abiertos desde
 * disco: puede estar bloqueado o compartido entre archivos distintos. Por eso
 * NO es la fuente de verdad: la fuente es el archivo que ella exporta.
 * Aqui es una comodidad, y si falla la pagina lo dice. */
const CLAVE = 'despacho:estado:' + (DATOS.clave || 'sin-clave')
let almacenOK = true
const almacen = {
  leer() {
    try { return JSON.parse(localStorage.getItem(CLAVE) || '{}') }
    catch { almacenOK = false; return {} }
  },
  escribir(v) {
    try { localStorage.setItem(CLAVE, JSON.stringify(v)); return true }
    catch { almacenOK = false; return false }
  },
}

let estado = almacen.leer()
let sucioDesdeExport = false

function guardar() {
  sucioDesdeExport = true
  almacen.escribir(estado)
  pintarProgreso()
  pintarAviso()
}

function pintarAviso() {
  const el = $('#aviso-persistencia')
  if (!el) return
  const partes = []
  if (!almacenOK) partes.push('Este navegador no conserva lo marcado al cerrar la pagina.')
  if (sucioDesdeExport) partes.push('Tiene trabajo sin guardar: use «Guardar lo comprobado».')
  el.textContent = partes.join(' ')
  el.hidden = partes.length === 0
}

/* ------------------------------------------------------------------- audio */
let audio = null
let hayAudio = false

function montarAudio() {
  const barra = $('#barra')
  if (barra) barra.hidden = false
  audio = $('#audio')
  const caja = $('#reproductor')
  const nada = $('#sin-audio')
  if (!audio || !DATOS.audio) { if (nada) nada.hidden = false; return }

  audio.src = encodeURI(DATOS.audio)
  audio.addEventListener('loadedmetadata', () => {
    hayAudio = true
    if (caja) caja.hidden = false
    if (nada) nada.hidden = true
    $('#reloj-total').textContent = hms(audio.duration)
    habilitarHoras(true)
  })
  audio.addEventListener('error', () => {
    hayAudio = false
    if (caja) caja.hidden = true
    if (nada) nada.hidden = false
    habilitarHoras(false)
  })
  audio.addEventListener('timeupdate', () => {
    $('#reloj-actual').textContent = hms(audio.currentTime)
    resaltarSonando(audio.currentTime)
  })
  audio.addEventListener('play', () => { $('#btn-play').textContent = '❚❚' })
  audio.addEventListener('pause', () => { $('#btn-play').textContent = '▶' })
  $('#btn-play')?.addEventListener('click', () => (audio.paused ? audio.play() : audio.pause()))
}

function habilitarHoras(ok) {
  $$('.hora').forEach((b) => { b.disabled = !ok })
}

let sonandoActual = null
function resaltarSonando(t) {
  const seg = $$('.seg').find((s) => t >= +s.dataset.inicio && t < +s.dataset.fin)
  if (seg === sonandoActual) return
  sonandoActual?.classList.remove('sonando')
  sonandoActual = seg || null
  sonandoActual?.classList.add('sonando')
}

function irA(segundos, seg) {
  if (!hayAudio || !audio) return
  // Se retrocede un poco para oir el arranque de la frase; pero el segmento que
  // se ilumina es el que ella pulso, no el anterior.
  audio.currentTime = Math.max(0, segundos - 0.3)
  if (seg) {
    sonandoActual?.classList.remove('sonando')
    sonandoActual = seg
    seg.classList.add('sonando')
  }
  audio.play()
}

/* ------------------------------------------------------------ portapapeles
 * En archivos abiertos desde disco el portapapeles moderno puede no existir.
 * Respaldo con textarea temporal: nunca se queda sin copiar en silencio. */
async function copiar(texto) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(texto); return true
    }
  } catch { /* cae al respaldo */ }
  try {
    const t = document.createElement('textarea')
    t.value = texto
    t.setAttribute('readonly', '')
    t.style.cssText = 'position:fixed;top:-1000px;opacity:0'
    document.body.appendChild(t)
    t.select()
    const ok = document.execCommand('copy')
    document.body.removeChild(t)
    return ok
  } catch { return false }
}

function procedencia(seg) {
  const e = estado[seg.dataset.i] || {}
  const hora = hms(+seg.dataset.inicio)
  const base = `— ${DATOS.origen || 'grabacion'}, ${hora}. ${DATOS.tipoMaterial || 'Material derivado'}`
  return e.estado === 'confirmado' || e.estado === 'corregido'
    ? `${base}, cotejado con el original el ${e.fecha}.`
    : `${base}, NO cotejado con el original.`
}

/* ------------------------------------------------------------------ estados */
const ETIQUETA = { oido: 'Oído', confirmado: 'Confirmado', corregido: 'Corregido' }

function montarSegmento(seg) {
  const i = seg.dataset.i

  $('.hora', seg)?.addEventListener('click', () => irA(+seg.dataset.inicio, seg))

  const acciones = document.createElement('div')
  acciones.className = 'acciones'
  acciones.innerHTML = `
    <button type="button" data-a="oido">Oído</button>
    <button type="button" data-a="confirmado">Confirmado</button>
    <button type="button" data-a="corregido">Corregir…</button>
    <button type="button" data-a="copiar">Copiar con procedencia</button>
    <button type="button" data-a="copiar-solo" class="tenue">Solo el texto</button>`
  seg.appendChild(acciones)

  acciones.addEventListener('click', async (ev) => {
    const b = ev.target.closest('button')
    if (!b) return
    const a = b.dataset.a
    if (a === 'copiar' || a === 'copiar-solo') {
      const txt = $('.texto', seg).textContent.trim()
      const ok = await copiar(a === 'copiar' ? `«${txt}»\n${procedencia(seg)}` : txt)
      b.textContent = ok ? 'Copiado' : 'No se pudo copiar'
      setTimeout(() => { b.textContent = a === 'copiar' ? 'Copiar con procedencia' : 'Solo el texto' }, 1600)
      return
    }
    if (a === 'corregido') {
      const previo = estado[i]?.correccion || ''
      const v = prompt('Escriba lo que SÍ dice el original.\n\nNo se modifica la transcripción: queda como anotación suya, con la fecha.', previo)
      if (v === null) return
      estado[i] = { estado: 'corregido', fecha: hoy(), correccion: v.trim() }
    } else {
      estado[i] = estado[i]?.estado === a ? undefined : { estado: a, fecha: hoy() }
      if (!estado[i]) delete estado[i]
    }
    pintarSegmento(seg)
    guardar()
    aplicarFiltro()
  })

  pintarSegmento(seg)
}

function pintarSegmento(seg) {
  const e = estado[seg.dataset.i]
  seg.classList.toggle('comprobado', !!e)
  $$('.acciones button', seg).forEach((b) => {
    b.classList.toggle('marcado', !!e && b.dataset.a === e.estado)
  })
  $('.sello', seg)?.remove()
  $('.correccion', seg)?.remove()
  if (!e) return

  const sello = document.createElement('p')
  sello.className = 'sello'
  sello.textContent = `${ETIQUETA[e.estado]} por usted el ${e.fecha}. Es constancia de que fue al original, no de que el texto sea correcto.`
  seg.insertBefore(sello, $('.acciones', seg))

  if (e.estado === 'corregido' && e.correccion) {
    const c = document.createElement('p')
    c.className = 'correccion'
    c.innerHTML = '<span class="et">Lo que sí dice el original, según usted:</span>'
    c.append(document.createTextNode(e.correccion))
    seg.insertBefore(c, $('.acciones', seg))
  }
}

/* ------------------------------------------------------------------ filtros */
let filtro = 'todo'
function aplicarFiltro() {
  $$('.seg').forEach((s) => {
    const dud = s.dataset.dudoso === '1'
    const hecho = !!estado[s.dataset.i]
    const ver = filtro === 'todo' || (filtro === 'dudoso' && dud) ||
                (filtro === 'pendiente' && dud && !hecho) || (filtro === 'hecho' && hecho)
    s.classList.toggle('oculto', !ver)
  })
}

function pintarProgreso() {
  const dud = $$('.seg').filter((s) => s.dataset.dudoso === '1').length
  const hechos = $$('.seg').filter((s) => estado[s.dataset.i]).length
  const el = $('#progreso-texto')
  if (el) el.textContent = dud ? `${hechos} comprobadas · ${dud} con motivo de duda` : `${hechos} comprobadas`
}

/* -------------------------------------------------------- exportar/importar */
function exportar() {
  const doc = {
    formato: 'despacho/estado-de-comprobacion',
    version: 1,
    documento: DATOS.titulo || '',
    origen: DATOS.origen || '',
    clave: DATOS.clave || '',
    exportado: new Date().toISOString(),
    nota: 'Constancia de que una persona fue al original. NO es verificacion de que el texto sea correcto.',
    estado,
  }
  const a = document.createElement('a')
  a.href = URL.createObjectURL(new Blob([JSON.stringify(doc, null, 1)], { type: 'application/json' }))
  a.download = `comprobado - ${(DATOS.titulo || 'documento').replace(/[\\/:*?"<>|]/g, '')}.json`
  a.click()
  URL.revokeObjectURL(a.href)
  sucioDesdeExport = false
  pintarAviso()
}

function importar(file) {
  const fr = new FileReader()
  fr.onload = () => {
    try {
      const d = JSON.parse(fr.result)
      if (d.clave && DATOS.clave && d.clave !== DATOS.clave) {
        if (!confirm('Ese archivo es de otro documento. ¿Cargarlo de todos modos?')) return
      }
      estado = d.estado || {}
      $$('.seg').forEach(pintarSegmento)
      guardar(); sucioDesdeExport = false; pintarAviso(); aplicarFiltro()
    } catch { alert('No se pudo leer ese archivo.') }
  }
  fr.readAsText(file)
}

/* -------------------------------------------------------------------- inicio */
function iniciar() {
  montarAudio()
  $$('.seg').forEach(montarSegmento)
  $$('.chip').forEach((c) => c.addEventListener('click', () => {
    $$('.chip').forEach((o) => o.classList.toggle('activo', o === c))
    filtro = c.dataset.filtro
    aplicarFiltro()
  }))
  $('#btn-exportar')?.addEventListener('click', exportar)
  $('#btn-importar')?.addEventListener('click', () => $('#archivo-estado').click())
  $('#archivo-estado')?.addEventListener('change', (e) => e.target.files[0] && importar(e.target.files[0]))
  window.addEventListener('beforeunload', (e) => {
    if (sucioDesdeExport) { e.preventDefault(); e.returnValue = '' }
  })
  almacen.leer()
  pintarProgreso()
  pintarAviso()
  aplicarFiltro()
}

document.readyState === 'loading'
  ? document.addEventListener('DOMContentLoaded', iniciar)
  : iniciar()
