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
import { leerContrato, nodoDe, hms, textoTranscrito } from './contrato.js'
import { crearEstado, ETIQUETA } from './estado.js'
import { crearMedios } from './medios.js'
import { crearFranja } from './franja.js'
import { montarTeclado } from './teclado.js'
import { montarVoces } from './voces.js'
import { montarIlegibles } from './ilegibles.js'
import { montarCompromisos } from './compromisos.js'
import { crearGuardado } from './guardado.js'
import { crearOirLinea, montarOtrasLecturas } from './otras-lecturas.js'
import { montarGlosario } from './glosario.js'
import { abiertaDesdeZip, pasosExtraer, navegador } from './sola.js'

const $ = (s, r = document) => r.querySelector(s)
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s))

const C = leerContrato($('#datos'))
let filtro = 'todo'
let foco = null
let franja = null
let voces = null
let ilegibles = null
let compromisos = null
let guardado = null
let glosario = null
/** Todo lo que ella declara en esta página, junto: lo que se guarda. */
const extra = () => ({
  ...(voces?.paraGuardar() || {}),
  ...(ilegibles?.paraGuardar() || {}),
  ...(compromisos?.paraGuardar() || {}),
  ...(glosario?.paraGuardar() || {}),
})

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
  return textoTranscrito($('.texto', nodoDe(b)))
}

/* -------------------------------------------------------------------- estado */
const estado = crearEstado(C.clave, (id) => {
  if (id === null) { C.bloques.forEach(pintarBloque); aplicarFiltro() }
  pintarProgreso(); pintarAviso(); franja?.refrescar()
  if (id !== 'guardado') guardado?.cambio()
  pintarPestanas()
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

function marcarFoco(tipo, sugerido = '', partioDe = '') {
  if (!foco) { mover(1); return }
  if (tipo === 'corregido') {
    const previo = estado.de(foco)?.correccion || ''
    const v = prompt('Escriba lo que SÍ dice el original.\n\n'
      + (sugerido ? 'Viene escrito lo que leyó otra máquina: cámbielo por lo que usted oyó.\n\n' : '')
      + 'No se modifica la transcripción: queda como anotación suya, con la fecha.', sugerido || previo)
    if (v === null) return
    estado.marcar(foco, 'corregido', v.trim(), sugerido && partioDe ? { partio_de: partioDe, sugerido } : null)
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
  s.innerHTML = `<strong>${ETIQUETA[e.estado]} por usted</strong> el ${String(e.fecha).replace(/[&<>"']/g, '')}. `
    + 'Es constancia de que fue al original, <strong>no de que el texto sea correcto</strong>.'
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
  if (estado.sucio) p.push('Tiene marcas que <strong>aún no ha guardado</strong> en un archivo: use «Guardar lo comprobado».')
  el.innerHTML = p.join(' ')
  el.hidden = !p.length
}

/* ------------------------------------------------------------------- medios */
const medios = crearMedios($('#audio'), C.audio, {
  alTiempo(t) {
    $('#reloj-actual').textContent = hms(t)
    franja?.playhead(t)
    voces?.alTiempo(t)
    ilegibles?.alTiempo(t)
    compromisos?.alTiempo(t)
    oirLinea?.alTiempo(t)
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
    voces?.alEstado()
    ilegibles?.alEstado()
    compromisos?.alEstado()
    if (s.listo === undefined) return
    if (s.motivo === 'no-encontrada') avisarSola()
    $('#reproductor').hidden = !s.listo
    $('#sin-audio').hidden = s.listo
    if (s.texto) $('#reloj-total').textContent = s.texto
    $$('.hora').forEach((h) => { h.disabled = !s.listo })
  },
})
let sonando = null

/* Oír una sola línea (y compararla con las otras lecturas). Se para al final. */
const lecturasDe = new Map()
const oirLinea = crearOirLinea(medios, {
  alCambiar(b) {
    lecturasDe.get(b.id)?.pintar()
    const x = $('.acciones .oir-linea', nodoDe(b))
    if (x) x.textContent = oirLinea.sonandoEn(b) ? '❚❚' : '▶ Oír'
  },
})

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
    <button type="button" data-a="oir-linea" class="oir-linea" title="Oír solo esta línea">▶ Oír</button>
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
    if (a === 'oir-linea') { oirLinea.oir(b); return }
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
    const ol = montarOtrasLecturas(b, {
      oir: oirLinea,
      texto: () => textoTranscrito($('.texto', n)),
      alCorregir(bb, sugerido, partioDe) { foco = bb.id; marcarFoco('corregido', sugerido, partioDe) },
    })
    lecturasDe.set(b.id, ol)
    n.insertBefore(ol.nodo, acc)
  }

  pintarBloque(b)
}

/* ------------------------------------------------------------- pagina sola */
// Abierta desde dentro del .zip, Windows extrae SOLO esta pagina a una carpeta
// temporal: ni enlaces ni audio funcionan, y el aviso de «extraiga primero»
// estaba dentro de la pagina que ya se abrio mal. Se prueba si un archivo que
// deberia estar al lado carga; si no, se dice arriba y en grande.
/* La velocidad del audio: más lento para entender lo que se dice mal, y la
   página la recuerda. Oír más despacio o más deprisa sigue contando como oír. */
const VELOCIDADES = [0.5, 0.75, 1, 1.25, 1.5]
function montarVelocidad() {
  const s = $('#velocidad')
  if (!s) return
  const poner = (v) => {
    if (!VELOCIDADES.includes(v)) v = 1
    medios.velocidad = v
    s.value = String(v)
    try { localStorage.setItem('despacho:velocidad', String(v)) } catch { /* se aplica igual */ }
  }
  let inicial = 1
  try { inicial = Number(localStorage.getItem('despacho:velocidad')) || 1 } catch {}
  poner(inicial)
  s.addEventListener('change', () => poner(Number(s.value)))
  velocidadPaso = (paso) => {
    const i = VELOCIDADES.indexOf(Number(s.value))
    const v = VELOCIDADES[Math.max(0, Math.min(VELOCIDADES.length - 1, (i < 0 ? 2 : i) + paso))]
    poner(v)
    voces?.avisar(`Velocidad: ${String(v).replace('.', ',')}×`, 1500)
  }
}
let velocidadPaso = () => {}

/* Los tres paneles de trabajo en pestañas: uno a la vista. Apilados, los tres
   empujaban la transcripción una pantalla hacia abajo. */
const PESTANAS = [['voces', 'Quién habla'], ['ilegibles', 'Lo que no se entiende'], ['glosario', 'Glosario']]
function montarPestanas() {
  const hay = PESTANAS.filter(([id]) => $('#' + id) && !$('#' + id).hidden)
  if (!hay.length) return
  const barra = document.createElement('div')
  barra.className = 'pestanas envoltura'
  barra.setAttribute('role', 'tablist')
  barra.setAttribute('aria-label', 'Paneles de trabajo')
  barra.innerHTML = hay.map(([id, t]) =>
    `<button type="button" role="tab" class="pestana" data-p="${id}" aria-controls="${id}">${t} <span class="p-cifra"></span></button>`).join('')
    + '<button type="button" class="boton tenue p-ocultar" aria-expanded="true">Ocultar</button>'
  $('#' + hay[0][0]).before(barra)
  document.body.classList.add('con-pestanas')
  barra.addEventListener('click', (e) => {
    const b = e.target.closest('button')
    if (!b) return
    if (b.classList.contains('p-ocultar')) return ocultarPaneles(!document.body.classList.contains('paneles-ocultos'))
    abrirPestana(b.dataset.p)
  })
  // Las flechas cambian de pestaña, como en cualquier lista de pestañas.
  barra.addEventListener('keydown', (e) => {
    if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return
    const ps = [...barra.querySelectorAll('.pestana')]
    const i = ps.indexOf(document.activeElement)
    if (i < 0) return
    e.preventDefault()
    const sig = ps[(i + (e.key === 'ArrowRight' ? 1 : -1) + ps.length) % ps.length]
    abrirPestana(sig.dataset.p); sig.focus()
  })
  hay.forEach(([id]) => $('#' + id)?.setAttribute('role', 'tabpanel'))
  let inicial = hay[0][0]
  try { const g = localStorage.getItem('despacho:pestana'); if (hay.some(([id]) => id === g)) inicial = g } catch {}
  abrirPestana(inicial, false)
  try { ocultarPaneles(localStorage.getItem('despacho:paneles-ocultos:' + C.clave) === '1', false) } catch {}
  if (glosario) glosario.abrirPestana = () => abrirPestana('glosario')
  pintarPestanas()
}
function abrirPestana(id, recordar = true) {
  $$('.pestana').forEach((b) => {
    const si = b.dataset.p === id
    b.classList.toggle('activa', si)
    b.setAttribute('aria-selected', String(si))
    const s = $('#' + b.dataset.p)
    if (s) s.classList.toggle('pestana-oculta', !si)
  })
  if (document.body.classList.contains('paneles-ocultos')) ocultarPaneles(false)
  if (recordar) try { localStorage.setItem('despacho:pestana', id) } catch {}
}
function ocultarPaneles(si, recordar = true) {
  document.body.classList.toggle('paneles-ocultos', si)
  const b = $('.p-ocultar')
  if (b) { b.textContent = si ? 'Mostrar' : 'Ocultar'; b.setAttribute('aria-expanded', String(!si)) }
  if (recordar) try { localStorage.setItem('despacho:paneles-ocultos:' + C.clave, si ? '1' : '0') } catch {}
}
function pintarPestanas() {
  const cifra = { voces: voces?.cifra?.(), ilegibles: ilegibles?.cifra?.(), glosario: glosario ? String(glosario.cuantas()) : '' }
  $$('.pestana').forEach((b) => { const c = b.querySelector('.p-cifra'); if (c) c.textContent = cifra[b.dataset.p] || '' })
}

/* El tema: el del sistema, o el que ella elija, y se recuerda. Cambiar de
   golpe porque el sistema cambio a oscuro a media tarde desorienta. */
function montarTema() {
  const b = $('#btn-tema')
  if (!b) return
  const ORDEN = ['auto', 'claro', 'oscuro']
  const NOMBRE = { auto: '◐ automático', claro: '☀ claro', oscuro: '☾ oscuro' }
  const aplicar = (t) => {
    if (t === 'auto') delete document.documentElement.dataset.tema
    else document.documentElement.dataset.tema = t
    b.textContent = NOMBRE[t]
    b.title = 'Colores de la página: ' + NOMBRE[t].slice(2) + '. Pulse para cambiar.'
  }
  // El tema es UNO para todas las páginas del proyecto: el que se elige en
  // INICIO («despacho-apariencia», con más temas) manda; sus temas oscuros son
  // «oscuro» aquí y los claros, «claro». Lo que se elija aquí vuelve a INICIO.
  const deInicio = () => {
    try {
      const t = (JSON.parse(localStorage.getItem('despacho-apariencia')) || {}).tema
      return t === 'noche' ? 'oscuro' : t === 'papel' || t === 'contraste' ? 'claro' : t
    } catch { return null }
  }
  let actual = 'auto'
  try { actual = deInicio() || localStorage.getItem('despacho:tema') || 'auto' } catch { /* sin almacen: automatico */ }
  if (!ORDEN.includes(actual)) actual = 'auto'
  aplicar(actual)
  b.addEventListener('click', () => {
    actual = ORDEN[(ORDEN.indexOf(actual) + 1) % ORDEN.length]
    aplicar(actual)
    try {
      localStorage.setItem('despacho:tema', actual)
      let p = {}
      try { p = JSON.parse(localStorage.getItem('despacho-apariencia')) || {} } catch { p = {} }
      p.tema = actual
      localStorage.setItem('despacho-apariencia', JSON.stringify(p))
    } catch { /* se aplica igual */ }
  })
}

/* La página sola: abierta desde dentro de un .zip, o sin la entrega a su lado.
 * Los pasos son los del sistema de quien la abre: el Mac no tiene «Extraer
 * todo…», basta un doble clic sobre el .zip (2026-09-24: ella usa un Mac). */
function avisarSola(zip = false) {
  const el = $('#aviso-sola')
  if (!el) return
  if (zip) {
    $('#aviso-sola-titulo').textContent = 'Está abriendo esta página desde dentro del archivo .zip.'
    $('#aviso-sola-porque').textContent = 'Así se abre sola: no funcionan ni el audio ni los enlaces a las demás páginas, y no se puede guardar en el proyecto.'
  }
  $('#aviso-sola-pasos').textContent = pasosExtraer()
  el.hidden = false
}

function comprobarCompania() {
  if (C.audio || !C.sonda) return   // las paginas con grabacion avisan al fallar el audio
  const a = document.createElement('audio')
  a.preload = 'metadata'
  a.addEventListener('error', () => avisarSola())
  a.src = encodeURI(C.sonda)
}

function iniciar() {
  if (abiertaDesdeZip(location.href)) avisarSola(true)
  comprobarCompania()
  // Sin bloques es un documento para leer: ni filtros, ni contador, ni «Guardar
  // lo comprobado» sobre algo que no tiene nada que comprobar.
  if (!C.bloques.length) return
  $('#barra').hidden = false
  C.bloques.forEach(montarBloque)
  // Quien habla: despues de los bloques, porque pone su marca encima de ellos.
  voces = montarVoces({ C, medios, nodoDe, enfocar, estado })
  ilegibles = montarIlegibles({ C, medios, enfocar, estado, voces })
  compromisos = montarCompromisos({ C, medios, estado, voces })
  glosario = montarGlosario({ C, caja: $('#glosario'), avisar: (t, ms) => voces?.avisar(t, ms), alIrA: (id) => enfocar(id),
    oirLinea, bloqueDe: (id) => C.porId.get(id) })
  if (glosario) glosario.alCambiar = () => { estado.tocar(); pintarPestanas() }
  montarPestanas()
  guardado = crearGuardado({
    titulo: C.documento.titulo,
    documento: () => estado.documento(C.documento, extra()),
    version: () => estado.version,
    clave: C.clave,
    alEstado: (s) => {
      const el = $('#aviso-guardado')
      if (!el) return
      el.textContent = s.texto
      el.classList.toggle('mal', !s.bien)
      el.hidden = !s.texto
      if (s.escrito) estado.limpiar(s.version)
    },
  })
  guardado.iniciar()

  franja = crearFranja($('#franja'), C, estado, (id) =>
    enfocar(id, { llevarAlAudio: true }))
  franja.refrescar()

  $$('.chip').forEach((c) => c.addEventListener('click', () => {
    $$('.chip').forEach((o) => o.classList.toggle('activo', o === c))
    filtro = c.dataset.filtro
    aplicarFiltro()
  }))
  $('#btn-play')?.addEventListener('click', () => medios.alternar())
  montarVelocidad()
  // Guardar: en la carpeta de la entrega si el navegador lo permite; si no,
  // o si ella no elige carpeta, se descarga como antes, y se le dice dónde.
  $('#btn-exportar')?.addEventListener('click', async () => {
    if (guardado?.disponible) {
      const r = await guardado.guardar()
      if (r === true) return
      // Si ella canceló, no se descarga nada a sus espaldas.
      if (r === 'cancelado') { voces?.avisar('No se guardó: no eligió carpeta.', 5000); return }
    }
    estado.exportar(C.documento, extra())
    // Una sola regla para todo lo descargado, venga de la página que venga:
    // a «Lo que declaré», dentro de 2-Borradores. De ahí lo recoge la etapa 2.
    voces?.avisar(`Se descargó en Descargas como “comprobado - ${C.documento.titulo} - <fecha y hora>.json”`
      + (guardado?.disponible ? '' : ` (${navegador()} no deja que la página guarde en la carpeta)`)
      + '. Al terminar, arrástrelo a la carpeta “Lo que declaré” del proyecto (dentro de “2-Borradores”).', 12000)
  })
  $('#btn-importar')?.addEventListener('click', () => $('#archivo-estado').click())
  $('#archivo-estado')?.addEventListener('change', (e) => {
    const f = e.target.files[0]
    e.target.value = ''
    if (!f) return
    // Cargar SUSTITUYE lo de esta página en este navegador: se pregunta SIEMPRE
    // que haya algo declarado en cualquier panel, y antes se deja una copia.
    const cuenta = (o) => (o && typeof o === 'object' ? Object.keys(o).length : 0)
    const x = extra()
    const hay = estado.cuantos() + (voces?.cuantos || 0) + cuenta(x.ilegibles) + cuenta(x.compromisos)
    if (hay && !confirm('Al cargar ese archivo se sustituye lo que tiene declarado en esta página, en este navegador '
          + '(líneas, quién habla, lo que no se entiende y compromisos; el glosario se junta, no se sustituye).'
          + (guardado?.activo ? '\n\nAntes se guarda una copia fechada «antes de cargar» en su carpeta.'
            : estado.sucio ? '\n\nTiene cosas sin guardar en un archivo: si las quiere, cancele y pulse antes «Guardar lo comprobado».' : '')
          + '\n\n¿Cargar de todos modos?')) return
    const antes = hay && guardado?.activo ? guardado.copia('antes de cargar') : Promise.resolve(false)
    antes.then(() => estado.importar(f, C.clave))
      .then((d) => {
        if (!d) return
        const v = voces?.cargar(d)
        ilegibles?.cargar(d)
        compromisos?.cargar(d)
        const nGl = glosario?.cargar(d) || 0
        C.bloques.forEach(pintarBloque); aplicarFiltro(); pintarPestanas()
        const partes = [`${cuenta(d.estado)} líneas marcadas`]
        if (v?.cargado) partes.push(`${v.voces} fragmentos con quién habla y ${v.nombres} nombres`)
        if (cuenta(d.ilegibles)) partes.push(`${cuenta(d.ilegibles)} tramos contados`)
        if (cuenta(d.compromisos)) partes.push(`${cuenta(d.compromisos)} compromisos`)
        if (nGl) partes.push(`${nGl} ${nGl === 1 ? 'entrada' : 'entradas'} de glosario, juntadas con las de este navegador`)
        voces?.avisar(`Cargado: ${partes.join(', ')}`
          + (d.exportado ? ` (guardado el ${new Date(d.exportado).toLocaleString('es-CO')})` : '') + '.', 8000)
      })
      .catch((err) => alert(err.message))
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
    '-': { desc: 'Audio más lento', fn: () => velocidadPaso(-1) },
    '+': { desc: 'Audio más rápido', fn: () => velocidadPaso(1) },
    v: { desc: 'Quién habla: seguir confirmando voces donde lo dejó', fn: () => { abrirPestana('voces'); voces?.seguir() } },
    l: { desc: 'Lo que no se entiende: el siguiente tramo por contar', fn: () => { abrirPestana('ilegibles'); document.querySelector('.il-empezar')?.click() } },
    Escape: { desc: 'Quitar el foco', fn: () => { foco = null; $$('.seg.enfocado').forEach((n) => n.classList.remove('enfocado')) } },
    '?': { desc: 'Esta ayuda', fn: () => atajos.ayuda() },
  })
  $('#btn-ayuda')?.addEventListener('click', () => atajos.ayuda())
  montarTema()

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
