/* Piezas comunes de la pagina de voces. */

export function hms(s) {
  s = Math.max(0, Math.floor(s || 0))
  const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), x = s % 60
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(x).padStart(2, '0')}`
}

/** Duracion legible: «4 min 12 s», no «00:04:12» -- una duracion no es un minuto. */
export function duracion(s) {
  s = Math.round(s || 0)
  if (s < 60) return `${s} s`
  const m = Math.floor(s / 60), x = s % 60
  if (m < 60) return `${m} min ${String(x).padStart(2, '0')} s`
  return `${Math.floor(m / 60)} h ${String(m % 60).padStart(2, '0')} min`
}

export const pct = (x) => `${Math.round((x || 0) * 100)} %`

export function esc(t) {
  return String(t ?? '').replace(/[&<>"']/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]))
}

/** Crear elementos sin plantillas de cadena para lo que lleva datos. */
export function el(tag, attrs = {}, ...hijos) {
  const e = document.createElement(tag)
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v == null || v === false) continue
    if (k === 'class') e.className = v
    else if (k === 'text') e.textContent = v
    else if (k === 'html') e.innerHTML = v
    else if (k.startsWith('on')) e.addEventListener(k.slice(2), v)
    else if (k === 'style' && typeof v === 'object') Object.assign(e.style, v)
    else e.setAttribute(k, v === true ? '' : v)
  }
  for (const h of hijos.flat()) {
    if (h == null || h === false) continue
    e.append(h.nodeType ? h : document.createTextNode(String(h)))
  }
  return e
}

// Paleta cualitativa. El color AYUDA, pero nunca es lo unico que distingue:
// cada voz lleva ademas su numero, y lo declarado lleva ✔ (ADR-020 §6).
export const PALETA = ['#2563a8', '#c0392b', '#2e8b57', '#8e44ad', '#d4780f', '#138d90',
  '#8a5a2b', '#c2408a', '#5d6d7e', '#9a9a1f', '#34495e', '#6b8e23']

/** Todo lo que hace falta para PINTAR una voz: color, numero de tecla, nombre. */
export function catalogoVoces(modelo, estado, vivas) {
  const cat = {}
  const usados = new Set()
  const inicial = modelo.datos.voces
  inicial.forEach((v, k) => {
    const n = parseInt(v.etiqueta.replace(/\D/g, ''), 10) || k + 1
    cat[v.id] = { id: v.id, color: PALETA[k % PALETA.length], etiqueta: v.etiqueta, tecla: null, n }
  })
  for (const c of Object.values(cat)) if (c.n <= 9) usados.add(c.n)
  for (const vid of vivas) {
    const c = cat[vid]
    if (c && c.n <= 9) c.tecla = String(c.n)
  }
  let k = inicial.length
  for (const [vid, info] of Object.entries(estado.voces)) {
    if (!info.nueva) continue
    const num = parseInt(vid.slice(1), 10)
    cat[vid] = { id: vid, color: PALETA[k++ % PALETA.length], etiqueta: `Persona nueva ${num}`, tecla: null, n: null }
    if (vivas.includes(vid)) {
      for (let d = 1; d <= 9; d++) if (!usados.has(d)) { cat[vid].tecla = String(d); usados.add(d); break }
    }
  }
  for (const [vid, c] of Object.entries(cat)) {
    const info = estado.voces[vid] || {}
    c.nombre = (info.nombre || '').trim()
    c.cargo = (info.cargo || '').trim()
    c.como = (info.como_lo_sabe || '').trim()
    c.rotulo = c.nombre || c.etiqueta
    c.largo = c.nombre ? `${c.etiqueta} — ${c.nombre}${c.cargo ? ' · ' + c.cargo : ''}` : c.etiqueta
    c.fusionada = info.fusionada_en || null
  }
  return cat
}

/** Un chip de voz. `declarada` pinta relleno y ✔; si no, borde discontinuo y ≈. */
export function chipVoz(c, { declarada = false, banda = null, tecla = false, onclick, titulo, opcion = false, elegida = false } = {}) {
  if (!c) return el('span', { class: 'chip chip-nadie', text: '— sin voz —' })
  if (opcion) {
    // Un BOTON para elegir: ni ✔ ni ≈, porque todavia no es nada.
    return el('button', { class: 'chip chip-opcion' + (elegida ? ' elegida' : ''), style: { '--c': c.color },
      title: titulo || `Elegir ${c.largo}`, onclick, type: 'button' },
    el('span', { class: 'chip-marca' }),
    tecla && c.tecla ? el('kbd', { text: c.tecla }) : null,
    el('span', { class: 'chip-texto', text: c.rotulo }))
  }
  const e = el('button', {
    class: `chip ${declarada ? 'chip-declarada' : 'chip-propuesta'}${banda ? ' banda-' + banda : ''}`,
    style: { '--c': c.color },
    title: titulo || (declarada ? 'Declarado por una persona oyendo' : 'Propuesta de la máquina: nadie lo ha oído'),
    onclick,
    type: 'button',
  },
  el('span', { class: 'chip-marca', text: declarada ? '✔' : '≈' }),
  tecla && c.tecla ? el('kbd', { text: c.tecla }) : null,
  el('span', { class: 'chip-texto', text: c.rotulo }))
  if (!onclick) e.setAttribute('tabindex', '-1')
  return e
}

/** El «genoma»: los 32 valores del ADN como franja de barras. */
export function dibujarAdn(canvas, adn, color = '#333') {
  const ctx = canvas.getContext('2d')
  const W = canvas.width, H = canvas.height
  ctx.clearRect(0, 0, W, H)
  if (!adn) {
    ctx.fillStyle = '#ccc'
    ctx.fillRect(0, H / 2, W, 1)
    return
  }
  // Se escala por su propio maximo: lo que se compara a simple vista es la
  // FORMA de la huella, no su tamano.
  let mx = 0
  for (const x of adn) mx = Math.max(mx, Math.abs(x))
  mx = mx || 1
  const n = adn.length, w = W / n
  for (let i = 0; i < n; i++) {
    const v = adn[i] / mx
    const h = Math.abs(v) * (H / 2 - 1)
    ctx.fillStyle = color
    ctx.globalAlpha = 0.35 + 0.65 * Math.abs(v)
    if (v >= 0) ctx.fillRect(i * w + 0.5, H / 2 - h, Math.max(1, w - 1), h)
    else ctx.fillRect(i * w + 0.5, H / 2, Math.max(1, w - 1), h)
  }
  ctx.globalAlpha = 1
  ctx.fillStyle = 'rgba(0,0,0,.25)'
  ctx.fillRect(0, H / 2, W, 1)
}

export function lienzo(w, h, clase) {
  const c = el('canvas', { class: clase })
  const r = window.devicePixelRatio || 1
  c.width = Math.round(w * r)
  c.height = Math.round(h * r)
  c.style.width = w + 'px'
  c.style.height = h + 'px'
  return c
}

export function descargar(nombre, contenido, tipo = 'application/json') {
  const a = document.createElement('a')
  a.href = URL.createObjectURL(new Blob([contenido], { type: tipo + ';charset=utf-8' }))
  a.download = nombre.replace(/[\\/:*?"<>|]/g, '')
  document.body.appendChild(a)
  a.click()
  setTimeout(() => { URL.revokeObjectURL(a.href); a.remove() }, 1000)
}

export async function copiar(texto) {
  try { await navigator.clipboard.writeText(texto); return true } catch { /* sigue */ }
  const t = el('textarea', { style: { position: 'fixed', left: '-9999px' } })
  t.value = texto
  document.body.appendChild(t)
  t.select()
  let ok = false
  try { ok = document.execCommand('copy') } catch { ok = false }
  t.remove()
  return ok
}
