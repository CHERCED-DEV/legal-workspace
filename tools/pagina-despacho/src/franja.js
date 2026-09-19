/* La franja de resumen.
 *
 * Responde de un vistazo la pregunta que una lista de 386 elementos no responde:
 * DONDE invierto el tiempo. Un rectangulo por bloque, ancho proporcional a su
 * duracion, color segun el riesgo. Debajo, una marca por cada bloque ya
 * comprobado, para ver el avance sobre el documento entero y no como un numero.
 *
 * Idea tomada de Confides (analitica visual sobre salidas de reconocimiento de
 * voz). Aqui el color codifica RIESGO, no confianza: un numero de dinero dudoso
 * y una muletilla dudosa no son el mismo problema.
 */
import { hms } from './contrato.js'

const NS = 'http://www.w3.org/2000/svg'
const ALTO = 34
const ALTO_BARRA = 22

export function crearFranja(cont, contrato, estado, alPulsar) {
  const bloques = contrato.bloques
  if (!cont || !bloques.length) return { refrescar() {}, playhead() {} }

  const temporal = contrato.temporal
  const total = temporal
    ? Math.max(...bloques.map((b) => b.ancla.fin || 0))
    : bloques.length

  const svg = document.createElementNS(NS, 'svg')
  svg.setAttribute('class', 'franja-svg')
  svg.setAttribute('viewBox', `0 0 ${total} ${ALTO}`)
  svg.setAttribute('preserveAspectRatio', 'none')
  svg.setAttribute('role', 'img')
  svg.setAttribute('aria-label',
    `Resumen del documento: ${contrato.dudosos.length} de ${bloques.length} bloques con motivo de duda`)

  const fondo = document.createElementNS(NS, 'rect')
  fondo.setAttribute('x', 0); fondo.setAttribute('y', 0)
  fondo.setAttribute('width', total); fondo.setAttribute('height', ALTO_BARRA)
  fondo.setAttribute('class', 'franja-fondo')
  svg.appendChild(fondo)

  const rects = new Map()
  const sellos = new Map()

  bloques.forEach((b, i) => {
    const x = temporal ? b.ancla.inicio : i
    const w = Math.max(temporal ? (b.ancla.fin - b.ancla.inicio) : 1, total / 4000)

    const r = document.createElementNS(NS, 'rect')
    r.setAttribute('x', x); r.setAttribute('y', 0)
    r.setAttribute('width', w); r.setAttribute('height', ALTO_BARRA)
    r.setAttribute('class', `franja-b riesgo-${b.riesgo}`)
    r.dataset.id = b.id
    const donde = temporal ? hms(b.ancla.inicio) : `bloque ${i + 1}`
    r.innerHTML = `<title>${donde}${b.marcas.length ? ' — ' + b.marcas.join('; ') : ''}</title>`
    svg.appendChild(r)
    rects.set(b.id, r)

    const s = document.createElementNS(NS, 'rect')
    s.setAttribute('x', x); s.setAttribute('y', ALTO_BARRA + 3)
    s.setAttribute('width', w); s.setAttribute('height', ALTO - ALTO_BARRA - 3)
    s.setAttribute('class', 'franja-sello')
    s.setAttribute('visibility', 'hidden')
    svg.appendChild(s)
    sellos.set(b.id, s)
  })

  const marca = document.createElementNS(NS, 'rect')
  marca.setAttribute('y', -2); marca.setAttribute('width', Math.max(total / 900, 0.6))
  marca.setAttribute('height', ALTO_BARRA + 4)
  marca.setAttribute('class', 'franja-marca')
  marca.setAttribute('visibility', 'hidden')
  svg.appendChild(marca)

  svg.addEventListener('click', (ev) => {
    const id = ev.target?.dataset?.id
    if (id) { alPulsar?.(id); return }
    // Pulsar el fondo: ir a la posicion proporcional
    const caja = svg.getBoundingClientRect()
    const p = ((ev.clientX - caja.left) / caja.width) * total
    const b = temporal
      ? bloques.find((x) => p >= x.ancla.inicio && p < x.ancla.fin) ||
        bloques.reduce((a, x) => (x.ancla.inicio <= p ? x : a), bloques[0])
      : bloques[Math.min(bloques.length - 1, Math.floor(p))]
    if (b) alPulsar?.(b.id)
  })

  cont.appendChild(svg)

  const leyenda = document.createElement('p')
  leyenda.className = 'franja-leyenda'
  leyenda.innerHTML = `
    <span><i class="pt riesgo-alto"></i> cifra o nombre en duda, o las pasadas difieren</span>
    <span><i class="pt riesgo-medio"></i> palabra dudosa</span>
    <span><i class="pt riesgo-bajo"></i> puede no ser habla</span>
    <span><i class="pt sello"></i> ya comprobado</span>`
  cont.appendChild(leyenda)

  return {
    refrescar() {
      bloques.forEach((b) => {
        const hecho = !!estado.de(b.id)
        sellos.get(b.id)?.setAttribute('visibility', hecho ? 'visible' : 'hidden')
        rects.get(b.id)?.classList.toggle('hecho', hecho)
      })
    },
    playhead(t) {
      if (!temporal || t == null) return
      marca.setAttribute('x', t)
      marca.setAttribute('visibility', 'visible')
    },
    enfocar(id) {
      svg.querySelectorAll('.franja-b.enfocado').forEach((r) => r.classList.remove('enfocado'))
      rects.get(id)?.classList.add('enfocado')
    },
  }
}
