/* Los compromisos — que ella los oiga y diga qué son de verdad.
 *
 * Cada compromiso que señaló la lectura de la transcripción lleva ya su ficha
 * (quién, plazo, qué falta, la cita). Aquí ella lo oye y declara: si de verdad
 * es un compromiso, quién lo asume y qué plazo se oye. Es lo que un acta
 * necesita en la columna de responsables, y ninguna máquina lo puede afirmar.
 *
 * Reglas: no se declara ni se cambia sin oír (70 % de sus líneas); «no se
 * dice quién» es una respuesta; «no lo es» no lleva quién ni plazo; lo que
 * ella diga va aparte de la lectura de la máquina, que no se borra.
 */
import { OIDA_MINIMA } from './atribucion.js'
import { crearOido, anunciarPanel, alAbrirOtro } from './oido.js'

import { resaltar } from './resalte.js'

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]))
const hoy = () => new Date().toLocaleDateString('es-CO', { year: 'numeric', month: '2-digit', day: '2-digit' })

/** ¿Puede declarar o cambiar? Con la grabación, oído al menos OIDA_MINIMA, y
 *  con toda la cita localizada: si una parte no está en la transcripción, no
 *  se sabe qué trozo hay que oír para declararlo. */
export function puedeCambiar({ oida = 0, grabacion = true, sinLocalizar = [] }) {
  return !!grabacion && oida >= OIDA_MINIMA && !(sinLocalizar && sinLocalizar.length)
}

/** Lo que queda guardado tras un cambio. Con «No lo es», sin quién ni plazo:
 *  si no, el informe los seguía dando como suyos. Lo vacío no se guarda. */
export function fundir(anterior, campos) {
  const r = { ...anterior, ...campos }
  if (r.es === 'no') { delete r.quien; delete r.quien_texto; delete r.plazo }
  for (const k of Object.keys(r)) if (r[k] === undefined) delete r[k]
  return r
}

export function montarCompromisos({ C, medios, estado, voces }) {
  const lista = (C.compromisos || []).filter((c) => c.bloques?.length)
  if (!lista.length) return null
  const LLAVE = 'despacho:compromisos:' + C.clave
  const leer = () => { try { return JSON.parse(localStorage.getItem(LLAVE) || '{}') } catch { return {} } }
  let resp = leer()
  const guardar = () => {
    try { localStorage.setItem(LLAVE, JSON.stringify(resp)) } catch { /* lo dice el aviso de persistencia */ }
    estado.tocar?.()
  }
  window.addEventListener('storage', (e) => { if (e.key === LLAVE) { resp = leer(); lista.forEach(pintar) } })

  const oido = crearOido(medios)
  const tramoDe = (c) => {
    const bs = c.bloques.map((id) => C.porId.get(id)).filter(Boolean)
    return { id: c.id, desde: Math.min(...bs.map((b) => b.ancla.inicio)), hasta: Math.max(...bs.map((b) => b.ancla.fin)) }
  }
  let abierto = null

  // Por su id: con dos compromisos en el mismo segundo, buscar por minuto
  // metía los dos formularios en la misma tarjeta.
  function nodo(c) {
    return document.querySelector(`.compromiso[data-id="${CSS.escape(c.id)}"]`)
      || document.querySelector(`.compromiso[data-minuto="${CSS.escape(c.minuto)}"]`)
  }

  function montar(c) {
    const n = nodo(c)
    if (!n) return
    const caja = document.createElement('div')
    caja.className = 'cp-suyo'
    caja.innerHTML = `
      <div class="cp-fila">
        <button type="button" class="boton cp-oir">▶ Oírlo</button>
        <div class="vz-barra oir cp-barra" aria-hidden="true"><i></i><b class="vz-meta"></b></div>
        <span class="cp-oido"></span>
      </div>
      <div class="cp-form">
        <div class="cp-grupo"><span class="cp-et">¿Es un compromiso?</span>
          <button type="button" class="vz-voz cp-es" data-es="si">Sí, lo es</button>
          <button type="button" class="vz-voz cp-es" data-es="no">No lo es</button></div>
        <div class="cp-grupo cp-quien-grupo"><span class="cp-et">¿Quién lo asume?</span>
          <select class="cp-quien" aria-label="Quién lo asume"></select>
          <input type="text" class="cp-quien-otro" placeholder="nombre y cargo" hidden></div>
        <div class="cp-grupo cp-plazo-grupo"><span class="cp-et">Plazo que se oye</span>
          <input type="text" class="cp-plazo" placeholder="tal como se dice, o vacío si no se dice"></div>
      </div>
      <p class="cp-dicho"></p>`
    n.appendChild(caja)
    const d = () => resp[c.id] || {}
    // Sin oírlo no se cambia: el campo vuelve a lo guardado y se dice por qué,
    // para que lo que se ve no sea distinto de lo guardado.
    const cambiar = (campos) => {
      const oida = oido.fraccion(tramoDe(c))
      if (!puedeCambiar({ oida, grabacion: medios.listo, sinLocalizar: c.sin_localizar })) {
        pintar(c, { forzar: true })
        voces?.avisar?.(resp[c.id] ? 'Óigalo otra vez para cambiarlo.' : 'Óigalo para poder declarar.')
        return
      }
      resp[c.id] = fundir(d(), { ...campos, minuto: c.minuto, oido: Math.round(oida * 100) / 100,
                                 fecha: hoy(), cuando: new Date().toISOString() })
      guardar()
      pintar(c)
    }
    caja.querySelector('.cp-oir').addEventListener('click', (e) => {
      e.stopPropagation()
      if (abierto?.id !== c.id) { anunciarPanel('compromisos'); abierto = c; oido.abrir(tramoDe(c)); oido.oir() }
      else oido.alternar()
      pintar(c)
    })
    caja.querySelectorAll('.cp-es').forEach((b) => b.addEventListener('click', (e) => {
      e.stopPropagation(); cambiar({ es: b.dataset.es })
    }))
    caja.querySelector('.cp-quien').addEventListener('change', (e) => {
      const v = e.target.value
      const otro = caja.querySelector('.cp-quien-otro')
      if (v === 'otra') { otro.hidden = false; otro.focus(); return }
      otro.hidden = true
      if (v) cambiar({ quien: v, quien_texto: undefined })
    })
    caja.querySelector('.cp-quien-otro').addEventListener('change', (e) => {
      const v = e.target.value.trim()
      if (v) cambiar({ quien: 'otra', quien_texto: v })
    })
    caja.querySelector('.cp-plazo').addEventListener('change', (e) => cambiar({ plazo: e.target.value.trim() || 'no se dice' }))
    caja.addEventListener('click', (e) => e.stopPropagation())
    pintar(c)
  }

  /** `forzar`: vuelve a poner lo guardado también en el campo que tiene el foco. */
  function pintar(c, { forzar = false } = {}) {
    const n = nodo(c)
    const caja = n?.querySelector('.cp-suyo')
    if (!caja) return
    const t = tramoDe(c)
    const fr = oido.fraccion(t)
    const puede = puedeCambiar({ oida: fr, grabacion: medios.listo, sinLocalizar: c.sin_localizar })
    const d = resp[c.id] || {}
    caja.querySelector('.cp-barra i').style.width = `${Math.min(100, fr * 100)}%`
    caja.querySelector('.cp-barra').classList.toggle('llega', fr >= OIDA_MINIMA)
    caja.querySelector('.cp-oir').textContent = abierto?.id === c.id && oido.sonandoAqui ? '❚❚ Pausa' : fr > 0 ? '↻ Oírlo otra vez' : '▶ Oírlo'
    caja.querySelector('.cp-oido').textContent = c.sin_localizar?.length
      ? `Una parte de la cita no está en la transcripción («${c.sin_localizar[0]}»): no se sabe qué trozo oír, y no se puede declarar.`
      : !medios.listo ? 'Sin la grabación no se puede declarar.'
      : puede ? 'Oído: puede declarar.' : fr > 0 ? `Oyendo… ${Math.floor(fr * 100)} %`
        : resp[c.id] ? 'Óigalo otra vez para cambiarlo.' : 'Óigalo para poder declarar.'
    const form = caja.querySelector('.cp-form')
    form.classList.toggle('bloqueado', !puede)
    // Bloqueado de verdad, no solo a la vista: con Tab se llegaba y se escribía.
    form.querySelectorAll('button, select, input').forEach((el) => { el.disabled = !puede })
    // El formulario se enseña cuando ya lo oyó, o si ya declaró algo: antes,
    // treinta formularios abiertos tapaban la transcripción.
    form.hidden = !puede && !resp[c.id]
    caja.querySelectorAll('.cp-es').forEach((b) => b.classList.toggle('elegida', b.dataset.es === d.es))
    caja.querySelector('.cp-quien-grupo').hidden = d.es === 'no'
    caja.querySelector('.cp-plazo-grupo').hidden = d.es === 'no'
    const quien = caja.querySelector('.cp-quien')
    if (forzar || document.activeElement !== quien) {
      const ops = [['', '— elija —'], ...(voces?.lista() || []).map((v) => [v.voz, v.rotulo]),
        ['no_se_dice', 'No se dice quién'], ['otra', 'Otra persona…']]
      quien.innerHTML = ops.map(([k, txt]) => `<option value="${esc(k)}"${(d.quien || '') === k ? ' selected' : ''}>${esc(txt)}</option>`).join('')
    }
    const otro = caja.querySelector('.cp-quien-otro')
    otro.hidden = d.quien !== 'otra' && (forzar || otro.hidden)
    if (forzar || document.activeElement !== otro) otro.value = d.quien === 'otra' ? d.quien_texto || '' : ''
    const pl = caja.querySelector('.cp-plazo')
    if (forzar || document.activeElement !== pl) pl.value = d.plazo && d.plazo !== 'no se dice' ? d.plazo : ''
    const dicho = caja.querySelector('.cp-dicho')
    if (!d.es) { dicho.replaceChildren(); n.classList.remove('declarado'); return }
    n.classList.add('declarado')
    const qn = d.quien === 'otra' ? d.quien_texto : d.quien === 'no_se_dice' ? 'no se dice quién' : d.quien ? voces?.rotulo(d.quien) : null
    dicho.innerHTML = d.es === 'no'
      ? `✔ <strong>Según usted</strong>, oyéndolo el ${esc(d.fecha)}: <strong>no es un compromiso</strong>.`
      : `✔ <strong>Según usted</strong>, oyéndolo el ${esc(d.fecha)}: <strong>es un compromiso</strong>${qn ? ' · lo asume: <strong>' + esc(qn) + '</strong>' : ''}${d.plazo ? ' · plazo: ' + resaltar(d.plazo) : ''}.`
  }

  lista.forEach(montar)
  let listoAntes = medios.listo
  alAbrirOtro('compromisos', () => { if (abierto) { oido.cerrar(); const c = abierto; abierto = null; pintar(c) } })

  return {
    alTiempo(t) { if (abierto && oido.alTiempo(t)) pintar(abierto) },
    alEstado() {
      // Cuando la grabación termina de cargar, todos dejan de decir «sin la grabación».
      if (medios.listo !== listoAntes) { listoAntes = medios.listo; lista.forEach(pintar); return }
      if (abierto) pintar(abierto)
    },
    repintar() { lista.forEach(pintar) },
    paraGuardar() { return { compromisos: resp } },
    cargar(doc) {
      if (doc?.compromisos && typeof doc.compromisos === 'object') {
        resp = { ...doc.compromisos }
        try { localStorage.setItem(LLAVE, JSON.stringify(resp)) } catch {}
        lista.forEach(pintar)
      }
    },
  }
}
