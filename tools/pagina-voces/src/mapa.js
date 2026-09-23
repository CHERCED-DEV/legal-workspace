/* El mapa de voces: cada punto es una linea; las que suenan parecido quedan
 * cerca. Es un dibujo APROXIMADO de 512 numeros en dos dimensiones, y lo dice:
 * dos puntos lejanos pueden ser la misma persona. Sirve para ver de un golpe si
 * una voz esta partida en dos nubes, o si dos voces se mezclan.
 */
import { el, lienzo, hms } from './util.js'
import { DECLARADAS, resolver } from './genoma.js'

export function renderMapa(app, caja) {
  caja.replaceChildren()
  const W = Math.min(900, caja.clientWidth || 860), H = 520
  const c = lienzo(W, H, 'mapa')
  const tip = el('div', { class: 'mapa-tip', hidden: true })
  const E = app.estado.todo
  const r = window.devicePixelRatio || 1
  const ctx = c.getContext('2d')
  ctx.scale(r, r)
  const pad = 20
  const pos = (l) => [pad + (l.xy[0] + 1) / 2 * (W - 2 * pad), pad + (1 - (l.xy[1] + 1) / 2) * (H - 2 * pad)]
  const puntos = []
  for (const l of app.modelo.lineas) {
    if (!l.xy) continue
    const d = E.lineas[l.id]
    const decl = d && DECLARADAS.has(d.decision) && !d.partes
    const vid = decl ? resolver(d.voz, E.voces) : app.props.get(l.id)?.voz
    const [x, y] = pos(l)
    const rad = 2 + Math.min(5, l.dur / 2)
    puntos.push({ l, x, y, rad })
    // Lo que ella declaro que NO es una voz (no se distingue, varios, dividida,
    // descartado) no se pinta como una propuesta pendiente: una cruz gris.
    if (d && !decl) {
      ctx.globalAlpha = 0.8; ctx.strokeStyle = '#666'; ctx.lineWidth = 1.4
      ctx.beginPath(); ctx.moveTo(x - rad, y - rad); ctx.lineTo(x + rad, y + rad)
      ctx.moveTo(x + rad, y - rad); ctx.lineTo(x - rad, y + rad); ctx.stroke()
      continue
    }
    ctx.beginPath()
    ctx.arc(x, y, rad, 0, Math.PI * 2)
    const col = app.cat[vid]?.color || '#999'
    if (decl) { ctx.fillStyle = col; ctx.globalAlpha = 0.9; ctx.fill() }
    else { ctx.strokeStyle = col; ctx.globalAlpha = 0.55; ctx.lineWidth = 1.2; ctx.stroke() }
    if (app.foco?.linea?.id === l.id) {
      ctx.globalAlpha = 1; ctx.strokeStyle = '#000'; ctx.lineWidth = 2
      ctx.beginPath(); ctx.arc(x, y, rad + 4, 0, Math.PI * 2); ctx.stroke()
    }
  }
  ctx.globalAlpha = 1
  c.addEventListener('mousemove', (e) => {
    const b = c.getBoundingClientRect()
    const mx = e.clientX - b.left, my = e.clientY - b.top
    const p = cercano(puntos, mx, my)
    if (!p) { tip.hidden = true; return }
    const au = app.modelo.datos.audios.find((a) => a.id === p.l.audio)
    tip.hidden = false
    tip.style.left = (mx + 14) + 'px'
    tip.style.top = (my + 10) + 'px'
    tip.textContent = `${au?.nombre} ${hms(p.l.ini)} — «${p.l.texto.slice(0, 90)}»`
  })
  c.addEventListener('mouseleave', () => { tip.hidden = true })
  c.addEventListener('click', (e) => {
    const b = c.getBoundingClientRect()
    const p = cercano(puntos, e.clientX - b.left, e.clientY - b.top)
    if (p) { app.abrir(p.l, 'mapa'); app.oir(p.l) }
  })
  caja.append(el('p', { class: 'nota', html: 'Cada punto es una línea. <b>Relleno</b>: usted dijo quién habla. <b>Hueco</b>: lo propone la máquina. <b>Cruz gris</b>: usted dijo que ahí no se distingue, que hablan varios, o la dividió. Las que suenan parecido quedan cerca. <i>Es un dibujo aproximado: dos puntos lejanos pueden ser la misma persona.</i> Pulse un punto para oírlo.' }),
    el('div', { class: 'mapa-caja' }, c, tip),
    el('div', { class: 'leyenda' }, ...app.vivas.map((v) => el('span', { class: 'ley' },
      el('i', { style: { background: app.cat[v].color } }), app.cat[v].largo))))
}

function cercano(puntos, x, y) {
  let m = null, dm = 144
  for (const p of puntos) {
    const d = (p.x - x) ** 2 + (p.y - y) ** 2
    if (d < dm) { dm = d; m = p }
  }
  return m
}
