/* Las grabaciones enteras, como franjas de color por voz.
 *
 * Lleno = lo decidio ella. Rayado claro = propuesta de la maquina. Gris
 * rayado = hueco sin transcribir. Asi se ve de un vistazo donde falta trabajo,
 * y un clic lleva a esa linea.
 */
import { el, lienzo, hms } from './util.js'
import { DECLARADAS, resolver } from './genoma.js'

function rayas(ctx, color, alfa) {
  const p = document.createElement('canvas')
  p.width = p.height = 6
  const c = p.getContext('2d')
  c.globalAlpha = alfa
  c.fillStyle = color
  c.fillRect(0, 0, 6, 6)
  c.globalAlpha = Math.min(1, alfa + 0.35)
  c.strokeStyle = color
  c.lineWidth = 1.5
  c.beginPath(); c.moveTo(0, 6); c.lineTo(6, 0); c.stroke()
  return ctx.createPattern(p, 'repeat')
}

export function renderFranjas(app, caja) {
  caja.replaceChildren()
  const E = app.estado.todo
  const ancho = Math.max(400, (caja.clientWidth || 1200) - 150)
  for (const au of app.modelo.datos.audios) {
    const c = lienzo(ancho, 26, 'franja')
    const r = window.devicePixelRatio || 1
    const ctx = c.getContext('2d')
    ctx.scale(r, r)
    const T = au.duracion || 1
    const X = (t) => (t / T) * ancho
    ctx.fillStyle = '#eceae4'
    ctx.fillRect(0, 0, ancho, 26)
    for (const h of app.modelo.datos.huecos.filter((h) => h.audio === au.id)) {
      ctx.fillStyle = rayas(ctx, '#8a8a8a', 0.18)
      ctx.fillRect(X(h.ini), 0, Math.max(1, X(h.fin) - X(h.ini)), 26)
    }
    const lineas = app.modelo.porAudio[au.id] || []
    for (const l of lineas) {
      const d = E.lineas[l.id]
      if (l.rescate) {
        // Un rombo en el hueco: hueco = sin decidir, color = se dijo y quien, X = no se dijo.
        const x = X((l.ini + l.fin) / 2)
        ctx.beginPath(); ctx.moveTo(x, 13); ctx.lineTo(x + 5, 19); ctx.lineTo(x, 25); ctx.lineTo(x - 5, 19); ctx.closePath()
        if (d?.decision === 'descartado' || d?.decision === 'no_se_dijo') { ctx.strokeStyle = '#333'; ctx.lineWidth = 1.5; ctx.stroke(); ctx.beginPath(); ctx.moveTo(x - 3, 16); ctx.lineTo(x + 3, 22); ctx.moveTo(x + 3, 16); ctx.lineTo(x - 3, 22); ctx.stroke() }
        else if (d) { ctx.fillStyle = d.voz ? (app.cat[resolver(d.voz, E.voces)]?.color || '#333') : '#777'; ctx.fill() }
        else { ctx.fillStyle = '#fff'; ctx.fill(); ctx.strokeStyle = '#555'; ctx.lineWidth = 1.2; ctx.stroke() }
        continue
      }
      const decl = d && DECLARADAS.has(d.decision) && !d.partes
      const vid = decl ? resolver(d.voz, E.voces) : app.props.get(l.id)?.voz
      const col = app.cat[vid]?.color || '#999'
      const x = X(l.ini), w = Math.max(1, X(l.fin) - x)
      if (d?.decision === 'no_se_distingue') { ctx.fillStyle = '#555'; ctx.fillRect(x, 20, w, 6); continue }
      if (d?.decision === 'varios' || d?.partes) { ctx.fillStyle = '#333'; ctx.fillRect(x, 0, w, 26); continue }
      if (decl) { ctx.fillStyle = col; ctx.fillRect(x, 0, w, 26) }
      else {
        const p = app.props.get(l.id)
        ctx.fillStyle = rayas(ctx, col, p?.banda === 'alta' ? 0.45 : 0.15)
        ctx.fillRect(x, 5, w, 16)
      }
    }
    const f = app.foco?.linea
    if (f && f.audio === au.id) {
      ctx.fillStyle = '#000'
      const x = X(f.ini)
      ctx.beginPath(); ctx.moveTo(x - 5, 0); ctx.lineTo(x + 5, 0); ctx.lineTo(x, 7); ctx.fill()
      ctx.fillRect(x - 0.5, 0, 1.5, 26)
    }
    c.addEventListener('click', (e) => {
      const b = c.getBoundingClientRect()
      const t = (e.clientX - b.left) / b.width * T
      let mejor = null, dm = Infinity
      for (const l of lineas) {
        const dd = t < l.ini ? l.ini - t : t > l.fin ? t - l.fin : 0
        if (dd < dm) { dm = dd; mejor = l }
      }
      if (mejor) app.abrir(mejor, 'franja')
    })
    c.addEventListener('mousemove', (e) => {
      const b = c.getBoundingClientRect()
      c.title = hms((e.clientX - b.left) / b.width * T)
    })
    const cl = app.clar.audios[au.id]
    caja.append(el('div', { class: 'franja-fila' },
      el('span', { class: 'franja-rot', text: au.nombre }), c,
      el('span', { class: 'franja-pct' + (cl && cl.claridad >= app.modelo.datos.meta_claridad ? ' ok' : ''), text: cl ? Math.round(cl.claridad * 100) + ' %' : '' })))
  }
  caja.append(el('div', { class: 'franja-ley' },
    el('span', {}, el('i', { class: 'ley-llena' }), 'decidido por usted'),
    el('span', {}, el('i', { class: 'ley-rayada' }), 'propuesta de la máquina'),
    el('span', {}, el('i', { class: 'ley-hueco' }), 'sin transcribir'),
    el('span', {}, el('i', { class: 'ley-varios' }), 'varios a la vez / dividida'),
    el('span', {}, el('i', { class: 'ley-rombo' }), 'rescatado en un hueco')))
}
