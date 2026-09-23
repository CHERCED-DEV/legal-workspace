/* Todas las lineas: repasar, filtrar y corregir directamente.
 *
 * Mismo principio que la tarjeta: lo declarado lleva ✔ y fondo lleno; lo
 * propuesto lleva ≈, borde discontinuo y su seguridad.
 */
import { el, hms, chipVoz } from './util.js'
import { DECLARADAS, resolver } from './genoma.js'
import { chipDeLinea } from './revision.js'

const FILTROS = [
  ['todas', 'Todas'],
  ['pendientes', 'Sin decidir'],
  ['baja', 'La máquina duda'],
  ['declaradas', 'Decididas por usted'],
  ['pisan', 'Se pisan'],
  ['cambio', 'Cambia la voz a mitad'],
  ['rescates', 'Rescatado de los huecos'],
]

export function renderLineas(app, caja) {
  const E = app.estado.todo
  const f = app.filtro ||= { audio: 'todos', voz: 'todas', tipo: 'todas', q: '' }
  caja.replaceChildren()

  const barra = el('div', { class: 'filtros' },
    el('select', { onchange: (e) => { f.audio = e.target.value; app.render() } },
      el('option', { value: 'todos', text: 'Todas las grabaciones' }),
      ...app.modelo.datos.audios.map((a) => el('option', { value: a.id, text: a.nombre, selected: f.audio === a.id }))),
    el('select', { onchange: (e) => { f.voz = e.target.value; app.render() } },
      el('option', { value: 'todas', text: 'Todas las voces' }),
      ...app.vivas.map((v) => el('option', { value: v, text: app.cat[v].largo, selected: f.voz === v }))),
    el('span', { class: 'filtro-tipos' },
      ...FILTROS.map(([k, t]) => el('button', { class: 'btn mini' + (f.tipo === k ? ' activo' : ''), type: 'button', onclick: () => { f.tipo = k; app.render() }, text: t }))),
    el('input', { type: 'search', id: 'buscar-lineas', placeholder: 'Buscar en el texto…', value: f.q, oninput: (e) => { f.q = e.target.value; app._buscando = true; clearTimeout(app._tq); app._tq = setTimeout(() => app.render(), 250) } }))
  caja.append(barra)
  if (app._buscando) {
    const b = barra.querySelector('#buscar-lineas')
    b.focus()
    b.setSelectionRange(b.value.length, b.value.length)
    b.addEventListener('blur', () => { app._buscando = false }, { once: true })
  }

  const q = f.q.trim().toLowerCase()
  const filas = []
  let total = 0
  for (const l of app.modelo.lineas) {
    if (f.audio !== 'todos' && l.audio !== f.audio) continue
    const d = E.lineas[l.id]
    const p = app.props.get(l.id)
    const decl = d && DECLARADAS.has(d.decision)
    const vid = decl && !d.partes ? resolver(d.voz, E.voces) : p?.voz
    if (f.voz !== 'todas' && vid !== f.voz) continue
    if (f.tipo === 'pendientes' && d) continue
    if (f.tipo === 'baja' && (d || p?.banda === 'alta')) continue
    if (f.tipo === 'declaradas' && !d) continue
    if (f.tipo === 'pisan' && l.pisa < app.modelo.cal.pisa_max) continue
    if (f.tipo === 'cambio' && !l.cambio) continue
    if (f.tipo === 'rescates' && !l.rescate) continue
    if (q && !l.texto.toLowerCase().includes(q)) continue
    total++
    if (filas.length >= 400) continue
    // La misma regla que la tarjeta: lo que es de ella se ve de ella, lo que
    // propone la maquina se ve propuesto, y lo que no es una voz no se pinta
    // como si lo fuera.
    const chip = chipDeLinea(app, l, { onclick: (e) => { e.stopPropagation(); menuVoz(app, l, e.currentTarget) } })
    const au = app.modelo.datos.audios.find((a) => a.id === l.audio)
    filas.push(el('div', { class: 'fila' + (app.foco?.linea?.id === l.id ? ' actual' : ''), onclick: () => app.abrir(l, 'lista') },
      el('button', { class: 'btn mini', type: 'button', title: 'Oír', onclick: (e) => { e.stopPropagation(); app.oir(l) }, text: '▶' }),
      el('span', { class: 'fila-min', text: `${au?.nombre.replace('Audio ', 'A') || l.audio} ${hms(l.ini)}` }),
      chip,
      l.rescate ? el('span', { class: 'insignia insignia-rescate', text: 'rescatado' }) : null,
      d && d.oida === false ? el('span', { class: 'insignia insignia-pisa', title: 'Se decidió sin oír la línea: no cuenta para la claridad', text: 'sin oír' }) : null,
      el('span', { class: 'fila-txt' + (l.dudas?.length ? ' texto-dudoso' : '') + (l.rescate ? ' fila-rescate' : ''), text: d?.texto || l.texto }),
      l.pisa >= app.modelo.cal.pisa_max ? el('span', { class: 'insignia insignia-pisa', text: 'se pisan' }) : null,
      l.cambio ? el('span', { class: 'insignia insignia-cambio', text: 'cambia' }) : null))
  }
  caja.append(el('div', { class: 'cuenta', text: total > 400 ? `${total} líneas · se muestran las primeras 400: afine el filtro` : `${total} líneas` }))
  caja.append(el('div', { class: 'filas' }, ...filas))
}

function menuVoz(app, l, ancla) {
  document.querySelector('.menu-voz')?.remove()
  const r = ancla.getBoundingClientRect()
  const m = el('div', { class: 'menu-voz', style: { left: r.left + 'px', top: (r.bottom + window.scrollY + 4) + 'px' } },
    el('div', { class: 'menu-t', text: 'Declarar que habla:' }),
    ...app.vivas.map((v) => chipVoz(app.cat[v], { opcion: true, tecla: true, onclick: () => { m.remove(); app.asignarDesdeLista(l, v) } })),
    el('button', { class: 'btn mini', type: 'button', text: 'Cerrar', onclick: () => m.remove() }))
  document.body.appendChild(m)
  setTimeout(() => document.addEventListener('click', function fuera(e) {
    if (!m.contains(e.target)) { m.remove(); document.removeEventListener('click', fuera) }
  }), 0)
}
