/* Lo que no se entiende — que ella lo oiga y lo cuente.
 *
 * Hay tramos donde la máquina no sabe qué se dice: huecos que la transcripción
 * no recoge (a veces la voz estaba lejos), o tramos donde las lecturas
 * automáticas no se ponen de acuerdo. Aquí se le pide a ella lo que ninguna
 * máquina puede dar: que lo oiga y diga la idea principal y quién la dijo, si
 * lo sabe. Eso es fuente de verdad; lo de la máquina, solo pista.
 *
 * Reglas: no se guarda sin oír (70 %); «no se entiende» y «no hay nadie
 * hablando» son respuestas válidas, y valen tanto como una idea; lo que creyó
 * oír la máquina se enseña como pista, con su fuente, nunca como respuesta.
 * «Quién lo dice» se guarda solo si ella lo eligió: no contestar no es «no sé».
 * Con la pregunta abierta, las teclas de la página no llegan a sus atajos.
 */
import { hms } from './contrato.js'
import { mmss, OIDA_MINIMA } from './atribucion.js'
import { crearOido, anunciarPanel, alAbrirOtro, TECLAS_DE_LA_PAGINA } from './oido.js'

const ESCRIBIENDO = new Set(['INPUT', 'TEXTAREA', 'SELECT'])
import { resaltar } from './resalte.js'

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]))
const hoy = () => new Date().toLocaleDateString('es-CO', { year: 'numeric', month: '2-digit', day: '2-digit' })

export const ENTIENDE = [
  ['si', 'Sí, se entiende'],
  ['en_parte', 'En parte'],
  ['no', 'No se entiende'],
  ['sin_habla', 'No hay nadie hablando'],
]
const MOTIVO = {
  hueco: 'la transcripción no recoge nada aquí',
  discordia: 'las lecturas automáticas no se ponen de acuerdo',
  senalado: 'la transcripción pone aquí palabras que no se sostienen',
}
// Hueco con algo de texto alrededor: no se puede decir «no recoge nada aquí».
const HUECO_EN_PARTE = 'en parte de este tramo la transcripción no recoge nada'
const CITA_MAX = 280

const conIdea = (k) => k === 'si' || k === 'en_parte'
/** Una idea es al menos una palabra: «3» o «,» no lo son. */
export const esIdea = (s) => /\p{L}{2,}/u.test(s || '')

/** ¿Se puede guardar? Con la grabación, oído al menos OIDA_MINIMA, con una
 *  respuesta de las cuatro, y con idea si dijo que se entiende. */
export function puedeGuardar({ oida = 0, grabacion = true, entiende, idea }) {
  if (!grabacion || !(oida >= OIDA_MINIMA)) return false
  if (!ENTIENDE.some(([k]) => k === entiende)) return false
  if (conIdea(entiende)) return esIdea(idea)
  return true
}

/** ¿Está contado? Lo mismo que para guardarlo, sobre lo guardado. */
export function contado(d) {
  return !!d && puedeGuardar({ oida: d.oido ?? 0, entiende: d.entiende, idea: d.idea })
}

/** Lo que ella declaró, sin añadirle nada: «quién» solo si lo eligió. */
export function loDeclarado(b) {
  const idea = conIdea(b.entiende)
  return {
    entiende: b.entiende,
    ...(idea ? { idea: (b.idea || '').trim() } : {}),
    ...(idea && b.quien ? { quien: b.quien } : {}),
    ...(idea && (b.palabras || '').trim() ? { palabras: b.palabras.trim() } : {}),
  }
}

export const dichoDe = (x) => (x.transcripcion || []).map((l) => l.texto).join(' ')
/** Por qué se pregunta. Un hueco con texto en el tramo no «no recoge nada aquí». */
export function motivosDe(x) {
  return (x.motivos || []).map((m) =>
    m === 'hueco' && dichoDe(x).trim() ? HUECO_EN_PARTE : MOTIVO[m] || m).join('; ')
}

/** La cita cortada por un espacio, con las comillas cerradas: lo que sigue se
 *  dice fuera. Devuelve HTML escapado. */
export function citar(texto) {
  const t = String(texto || '').trim()
  if (t.length <= CITA_MAX) return `«${esc(t)}»`
  const corte = t.lastIndexOf(' ', CITA_MAX)
  return `«${esc(t.slice(0, corte > CITA_MAX / 2 ? corte : CITA_MAX))}» [sigue…]`
}

/** Qué hace una tecla con la pregunta abierta. null: sigue su camino (se
 *  escribe, o la toma el botón con el foco). Una tecla de la página nunca
 *  llega a su atajo: o es del panel, o avisa. Con la idea vacía, 1–4 siguen
 *  cambiando la respuesta: si no, «3» se escribía y se guardaba como idea. */
export function accionDeTecla({ key: k, ctrl = false, alt = false, escribiendo = false, ideaVacia = false, enBoton = false }) {
  if (k === 'Escape') return escribiendo ? 'dejar_de_escribir' : 'cerrar'
  if (k === 'Enter' && ctrl) return 'guardar'
  if (ctrl || alt) return null
  if (/^[1-4]$/.test(k) && (!escribiendo || ideaVacia)) return 'respuesta'
  if (escribiendo) return null
  if ((k === 'Enter' || k === ' ') && enBoton) return null
  if (k === 'r' || k === 'R') return 'oir'
  if (k === 'ArrowRight') return 'saltar'
  if (k === 'ArrowUp' || k === 'ArrowDown') return 'desplazar'
  if (TECLAS_DE_LA_PAGINA.has(k)) return 'aviso'
  return null
}

export function montarIlegibles({ C, medios, enfocar, estado, voces }) {
  const lista = (C.ilegibles || []).map((x) => ({ ...x }))
  const caja = document.getElementById('ilegibles')
  if (!caja || !lista.length) return null
  const porId = new Map(lista.map((x) => [x.id, x]))

  const LLAVE = 'despacho:ilegibles:' + C.clave
  const leer = () => { try { return JSON.parse(localStorage.getItem(LLAVE) || '{}') } catch { return {} } }
  let resp = leer()
  const guardar = () => {
    try { localStorage.setItem(LLAVE, JSON.stringify(resp)) } catch { /* lo dice el aviso de persistencia */ }
    estado.tocar?.()
  }
  window.addEventListener('storage', (e) => { if (e.key === LLAVE) { resp = leer(); pintar() } })

  const oido = crearOido(medios)
  const motivos = motivosDe

  /* ------------------------------------------------------------- el panel */
  caja.hidden = false
  caja.classList.add('vz', 'il')
  caja.innerHTML = `
    <div class="vz-cab">
      <div class="vz-cab-texto">
        <h2>Lo que no se entiende <span class="vz-sub">óigalo y cuéntenos qué se dice</span></h2>
        <p class="vz-global-texto"></p>
        <div class="vz-barra grande" aria-hidden="true"><i></i></div>
      </div>
      <button type="button" class="boton primaria il-empezar">▶ Empezar</button>
    </div>
    <div class="il-filas"></div>
    <p class="vz-nota">En estos tramos la máquina no sabe qué se dice. Óigalos y cuente, en una frase,
      <strong>la idea principal y quién la dijo</strong>, si lo sabe. «No se entiende» o «no hay nadie hablando»
      también son respuestas. <em>Lo que usted cuente aquí es la mejor fuente que hay de estos tramos: lo que
      creyó oír la máquina solo es una pista.</em></p>`
  const filas = caja.querySelector('.il-filas')
  caja.querySelector('.il-empezar').addEventListener('click', () => {
    const sig = lista.find((x) => !contado(resp[x.id])) || lista[0]
    abrir(sig)
  })

  function pintar() {
    const n = lista.filter((x) => contado(resp[x.id])).length
    caja.querySelector('.vz-global-texto').innerHTML =
      `<strong>${n} de ${lista.length}</strong> tramos contados por usted · ${mmss(lista.reduce((a, x) => a + (x.hasta - x.desde), 0))} en total`
    const b = caja.querySelector('.vz-barra.grande')
    b.querySelector('i').style.width = `${(100 * n) / lista.length}%`
    b.classList.toggle('llega', n === lista.length)
    caja.querySelector('.il-empezar').textContent = n === lista.length ? '↻ Repasar' : n ? `▶ Seguir · quedan ${lista.length - n}` : '▶ Empezar'
    filas.replaceChildren(...lista.map(fila))
    pintarTranscripcion()
  }

  function fila(x) {
    const d = resp[x.id]
    const f = document.createElement('button')
    f.type = 'button'
    f.className = 'il-fila' + (contado(d) ? ' hecha' : '')
    f.dataset.il = x.id
    const lo =!d ? '' : d.entiende === 'si' || d.entiende === 'en_parte'
      ? `«${(d.idea || '').trim()}»${d.quien ? ' — ' + (voces?.rotulo(d.quien) || d.quien) : ''}`
      : (ENTIENDE.find(([k]) => k === d.entiende) || [, ''])[1]
    f.innerHTML = `<span class="il-cuando">${hms(x.desde)} – ${hms(x.hasta)}</span>
      <span class="il-dur">${mmss(x.hasta - x.desde)}</span>
      <span class="il-que">${contado(d) ? '✔ ' + esc(lo) : resaltar(motivos(x))}</span>`
    f.addEventListener('click', () => abrir(x))
    return f
  }

  /* En la transcripción: el hueco y el tramo en discordia se ven donde ocurren. */
  function pintarTranscripcion() {
    document.querySelectorAll('.il-marca').forEach((n) => n.remove())
    for (const x of lista) {
      const d = resp[x.id]
      let ancla = null
      const hueco = [...document.querySelectorAll('.pausa.hueco')].find((p) =>
        Math.abs(Number(p.dataset.desde) - x.desde) < 1 || (Number(p.dataset.desde) >= x.desde && Number(p.dataset.hasta) <= x.hasta + 1))
      if (hueco) ancla = hueco
      else if (x.transcripcion?.length) ancla = document.getElementById(x.transcripcion[0].id)
      if (!ancla) continue
      const b = document.createElement('button')
      b.type = 'button'
      b.className = 'il-marca' + (contado(d) ? ' hecha' : '')
      b.dataset.il = x.id
      b.innerHTML = contado(d)
        ? `✔ <strong>Usted contó</strong> ${hms(x.desde)}–${hms(x.hasta)}: ${esc(d.entiende === 'si' || d.entiende === 'en_parte' ? '«' + d.idea.trim() + '»' : (ENTIENDE.find(([k]) => k === d.entiende) || [, ''])[1])}`
        : `? <strong>${hms(x.desde)}–${hms(x.hasta)}</strong> · ${resaltar(motivos(x))}. <strong>Óigalo y cuéntenos qué se dice</strong>`
      b.addEventListener('click', (e) => { e.stopPropagation(); abrir(x) })
      ancla.parentNode.insertBefore(b, ancla)
      if (hueco) hueco.classList.add('con-marca')
    }
  }

  /* -------------------------------------------------------- la pregunta */
  const dock = document.createElement('div')
  dock.className = 'vz-dock il-dock'
  dock.hidden = true
  dock.setAttribute('role', 'region')
  dock.setAttribute('aria-label', 'Contar lo que se dice en un tramo')
  dock.innerHTML = `
    <div class="envoltura vz-d-in">
      <div class="vz-d-cab">
        <strong class="vz-d-preg">¿Qué se dice aquí?</strong>
        <span class="vz-d-donde"></span>
        <button type="button" class="vz-cerrar" aria-label="Cerrar (Esc)" title="Cerrar (Esc)">×</button>
      </div>
      <p class="il-motivo"></p>
      <details class="il-pistas"><summary>Lo que creyó oír la máquina — solo una pista, no se fíe</summary><div></div></details>
      <div class="vz-d-oir">
        <button type="button" class="boton vz-repetir" title="Oír (R)">▶ Oír</button>
        <div class="vz-barra oir" aria-hidden="true"><i></i><b class="vz-meta"></b></div>
        <span class="vz-d-oido" aria-live="polite"></span>
      </div>
      <div class="il-form">
        <div class="il-entiende" role="radiogroup" aria-label="¿Se entiende?"></div>
        <label class="il-campo il-idea-caja">La idea principal, en una frase
          <textarea class="il-idea" rows="2" placeholder="Qué se dice aquí, con sus palabras"></textarea></label>
        <div class="il-campo il-quien-caja"><span>¿Quién lo dice?</span><div class="il-quien"></div></div>
        <label class="il-campo il-palabras-caja">Palabras exactas que oyó <span class="il-opcional">(si quiere dejarlas)</span>
          <textarea class="il-palabras" rows="1"></textarea></label>
      </div>
      <div class="vz-d-botones">
        <button type="button" class="vz-b vz-si il-guardar"><kbd>Ctrl ↵</kbd><span>Guardar y seguir</span></button>
        <button type="button" class="vz-b vz-saltar il-saltar"><kbd>→</kbd><span>Saltar</span></button>
      </div>
    </div>`
  document.body.appendChild(dock)
  const $d = (s) => dock.querySelector(s)
  let actual = null
  let borrador = {}
  let focoPrevio = null
  const avisar = (t) => voces?.avisar?.(t)

  ENTIENDE.forEach(([k, t], i) => {
    const b = document.createElement('button')
    b.type = 'button'; b.className = 'vz-voz il-op'; b.dataset.k = k
    b.setAttribute('role', 'radio')
    b.innerHTML = `<kbd>${i + 1}</kbd>${esc(t)}`
    b.addEventListener('click', () => elegir(k))
    $d('.il-entiende').appendChild(b)
  })
  $d('.il-idea').addEventListener('input', (e) => { borrador.idea = e.target.value; pintarBoton() })
  $d('.il-palabras').addEventListener('input', (e) => { borrador.palabras = e.target.value })

  /* Con idea, el foco va a escribirla; sin idea, se queda en la respuesta
     (la caja de la idea se esconde y el foco no puede caer a la página). */
  function elegir(k) {
    borrador.entiende = k
    pintarForm()
    ;(conIdea(k) ? $d('.il-idea') : $d(`.il-op[data-k="${k}"]`))?.focus()
  }

  function pintarQuien() {
    const c = $d('.il-quien')
    const conFoco = c.contains(document.activeElement) ? document.activeElement?.dataset?.k : null
    const ops = [...(voces?.lista() || []).map((v) => [v.voz, v.rotulo, v.color]),
      ['nueva', 'Una voz que no está en la lista', null], ['no_se', 'No sé quién', null]]
    c.replaceChildren(...ops.map(([k, t, col]) => {
      const b = document.createElement('button')
      b.type = 'button'; b.className = 'vz-voz' + (borrador.quien === k ? ' elegida' : '')
      b.dataset.k = k
      b.setAttribute('aria-pressed', String(borrador.quien === k))
      if (col) b.style.setProperty('--voz', col)
      b.innerHTML = `${col ? '<span class="vz-punto"></span>' : ''}${esc(t)}`
      b.addEventListener('click', () => { borrador.quien = borrador.quien === k ? undefined : k; pintarQuien() })
      return b
    }))
    // Rehechos los botones, el foco vuelve al mismo: si no, caía a la página.
    if (conFoco != null) c.querySelector(`[data-k="${CSS.escape(conFoco)}"]`)?.focus({ preventScroll: true })
  }

  function pintarForm() {
    dock.querySelectorAll('.il-op').forEach((b) => {
      b.classList.toggle('elegida', b.dataset.k === borrador.entiende)
      b.setAttribute('aria-checked', String(b.dataset.k === borrador.entiende))
    })
    const idea = conIdea(borrador.entiende)
    $d('.il-idea-caja').hidden = !idea
    $d('.il-quien-caja').hidden = !idea
    $d('.il-palabras-caja').hidden = !idea
    pintarQuien()
    pintarBoton()
  }

  function listo() {
    return puedeGuardar({ oida: oido.fraccion(), grabacion: medios.listo, entiende: borrador.entiende, idea: borrador.idea })
  }
  function pintarBoton() { $d('.il-guardar').disabled = !listo() }

  function pintarOido() {
    if (!actual) return
    const fr = oido.fraccion()
    $d('.vz-barra.oir i').style.width = `${Math.min(100, fr * 100)}%`
    $d('.vz-barra.oir').classList.toggle('llega', fr >= OIDA_MINIMA)
    const t = !medios.listo ? 'No se encontró la grabación: sin oírlo no se puede contar.'
      : fr >= OIDA_MINIMA ? 'Oído. Cuéntenos.' : `Oyendo… ${Math.floor(fr * 100)} % — al ${Math.round(OIDA_MINIMA * 100)} % puede guardar`
    if ($d('.vz-d-oido').textContent !== t) $d('.vz-d-oido').textContent = t
    const r = oido.sonandoAqui ? '❚❚ Pausa' : fr > 0 ? '↻ Oír otra vez' : '▶ Oír'
    if ($d('.vz-repetir').textContent !== r) $d('.vz-repetir').textContent = r
    pintarBoton()
  }

  /* La marca del tramo, arriba de lo que queda libre: centrada, el panel la tapaba. */
  function mostrarMarca(x) {
    const m = document.querySelector(`.il-marca[data-il="${CSS.escape(x.id)}"]`)
    if (!m || !m.getClientRects().length) return
    const barra = document.getElementById('barra')
    const arriba = barra && window.getComputedStyle(barra).position === 'sticky' ? barra.getBoundingClientRect().height : 0
    window.scrollTo({ top: m.getBoundingClientRect().top + window.scrollY - arriba - 8, behavior: 'smooth' })
  }

  function abrir(x) {
    if (!x) return
    if (dock.hidden) focoPrevio = document.activeElement
    anunciarPanel('ilegibles')
    actual = x
    oido.abrir(x)
    borrador = { ...(resp[x.id] || {}) }
    dock.hidden = false
    document.body.classList.add('con-dock')
    const n = lista.indexOf(x) + 1
    $d('.vz-d-donde').textContent = `${hms(x.desde)} – ${hms(x.hasta)} · ${mmss(x.hasta - x.desde)} · tramo ${n} de ${lista.length}`
    const dice = dichoDe(x)
    $d('.il-motivo').innerHTML = '<strong>Por qué se lo preguntamos:</strong> ' + resaltar(motivos(x)) + '.'
      + (dice.trim() ? ` ${x.motivos.includes('hueco') ? 'Lo que sí recoge' : 'La transcripción dice aquí'}: ${citar(dice)}.` : '')
    const pistas = $d('.il-pistas')
    pistas.hidden = !x.lecturas?.length
    pistas.open = false
    pistas.querySelector('div').innerHTML = (x.lecturas || []).map((l) =>
      `<p><span class="et">${esc(l.fuente)}</span>${esc(l.texto)}</p>`).join('')
    $d('.il-idea').value = borrador.idea || ''
    $d('.il-palabras').value = borrador.palabras || ''
    pintarForm()
    $d('.vz-d-in').scrollTop = 0
    const primera = x.transcripcion?.[0]?.id
    if (primera) enfocar(primera)
    mostrarMarca(x)
    oido.oir()
    pintarOido()
    ;($d('.il-op.elegida') || $d('.il-op')).focus({ preventScroll: true })
  }

  /* El foco vuelve a donde estaba; si era una fila o una marca rehecha, a la nueva. */
  function cerrar({ devolver = true } = {}) {
    oido.cerrar()
    actual = null
    dock.hidden = true
    if (!document.querySelector('.vz-dock:not([hidden])')) document.body.classList.remove('con-dock')
    let f = focoPrevio
    focoPrevio = null
    if (!devolver || !f) return
    if (!document.contains(f) && f.dataset?.il) f = document.querySelector(`.${f.classList[0]}[data-il="${CSS.escape(f.dataset.il)}"]`)
    if (f && f !== document.body && document.contains(f)) f.focus?.({ preventScroll: true })
  }

  function guardarActual() {
    if (!actual || !listo()) return
    resp[actual.id] = {
      ...loDeclarado(borrador),
      desde: actual.desde, hasta: actual.hasta, motivos: actual.motivos,
      oido: Math.round(oido.fraccion() * 100) / 100,
      fecha: hoy(), cuando: new Date().toISOString(),
    }
    guardar()
    pintar()
    siguiente()
  }

  function siguiente() {
    const i = lista.indexOf(actual)
    const sig = [...lista.slice(i + 1), ...lista.slice(0, i)].find((x) => !contado(resp[x.id]))
    if (sig) abrir(sig)
    else cerrar()
  }

  dock.addEventListener('click', (e) => {
    const b = e.target.closest('button')
    if (!b) return
    if (b.classList.contains('vz-cerrar')) cerrar()
    else if (b.classList.contains('vz-repetir')) oido.alternar()
    else if (b.classList.contains('il-guardar')) guardarActual()
    else if (b.classList.contains('il-saltar')) siguiente()
  })
  /* Con el panel abierto, las teclas son del panel, en captura, para que no
     las tome antes el teclado de la página (accionDeTecla dice cuál es cuál). */
  document.addEventListener('keydown', (ev) => {
    if (dock.hidden || !actual) return
    if (document.querySelector('dialog[open]')) return
    const a = document.activeElement
    const ideaVacia = !!a && a === $d('.il-idea') && !a.value.trim()
    const que = accionDeTecla({
      key: ev.key, ctrl: ev.ctrlKey || ev.metaKey, alt: ev.altKey, ideaVacia,
      escribiendo: !!a && (ESCRIBIENDO.has(a.tagName) || a.isContentEditable),
      enBoton: !!a && ['BUTTON', 'A', 'SUMMARY'].includes(a.tagName),
    })
    if (!que) return
    // Las flechas desplazan (el panel o la página), pero no mueven la línea enfocada.
    ev.stopImmediatePropagation()
    if (que === 'desplazar') return
    ev.preventDefault()
    if (que === 'cerrar') cerrar()
    else if (que === 'dejar_de_escribir') dock.contains(a) ? ($d('.il-op.elegida') || $d('.il-op')).focus() : a.blur()
    else if (que === 'guardar') guardarActual()
    else if (que === 'respuesta') {
      const [clave, texto] = ENTIENDE[Number(ev.key) - 1]
      elegir(clave)
      if (ideaVacia) avisar(`Respuesta: «${texto}». Con la idea vacía, 1–4 cambian la respuesta.`)
    }
    else if (que === 'oir') oido.alternar()
    else if (que === 'saltar') siguiente()
    else if (que === 'aviso') avisar('Con la pregunta abierta: 1–4 la respuesta · R oír · → saltar · Ctrl ↵ guardar · Esc cerrar')
  }, true)
  // Otro panel abre su pregunta: se cierra sin quitarle el foco.
  alAbrirOtro('ilegibles', () => { if (actual) cerrar({ devolver: false }) })

  pintar()
  return {
    alTiempo(t) { if (oido.alTiempo(t)) pintarOido() },
    alEstado() { if (actual) pintarOido() },
    cifra() { return `${lista.filter((x) => contado(resp[x.id])).length}/${lista.length}` },
    paraGuardar() {
      return { ilegibles: Object.fromEntries(Object.entries(resp).filter(([id]) => porId.has(id))) }
    },
    cargar(doc) {
      if (doc?.ilegibles && typeof doc.ilegibles === 'object') {
        resp = Object.fromEntries(Object.entries(doc.ilegibles).filter(([id]) => porId.has(id)))
        try { localStorage.setItem(LLAVE, JSON.stringify(resp)) } catch {}
        pintar()
      }
    },
  }
}
