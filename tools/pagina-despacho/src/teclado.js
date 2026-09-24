/* Teclado primero.
 *
 * Con 298 pasajes por comprobar, el raton es el cuello de botella: es la
 * diferencia entre comprobar trescientos y comprobar treinta. Quien revisa
 * transcripciones no levanta la mano del teclado.
 *
 * Este modulo no sabe que hace cada tecla: recibe un mapa y lo despacha. Lo que
 * cada tecla significa lo decide quien lo monta.
 */

const ESCRIBIENDO = new Set(['INPUT', 'TEXTAREA', 'SELECT'])
const PANELES = '#voces, #ilegibles, #glosario, .vz-dock, .il-dock, .pestanas, .cp-suyo, .ol-oir, .ol-cuerpo, dialog'

export function montarTeclado(mapa, { titulo = 'Atajos de teclado' } = {}) {
  const dialogo = crearAyuda(mapa, titulo)

  function alPulsar(ev) {
    if (ev.ctrlKey || ev.metaKey || ev.altKey) return
    const a = document.activeElement
    if (a && (ESCRIBIENDO.has(a.tagName) || a.isContentEditable)) return
    if (dialogo.open) {
      if (ev.key === 'Escape') { dialogo.close(); ev.preventDefault() }
      else if (ev.key === '?') { dialogo.close(); ev.preventDefault() }
      return
    }
    // Enter y Espacio pulsan el botón con foco SOLO en los paneles de pregunta
    // (y en un desplegable). En la transcripción no: tras un clic el foco se
    // queda en «Confirmado», y Espacio lo desmarcaba y Enter lo volvía a marcar
    // sin oír nada. Ahí siguen siendo «reproducir» y «oír el bloque».
    if ((ev.key === 'Enter' || ev.key === ' ') && a
        && (a.tagName === 'SUMMARY' || (['BUTTON', 'A'].includes(a.tagName) && a.closest(PANELES)))) return

    const clave = ev.key === ' ' ? 'Space' : ev.key
    const entrada = mapa[clave] || mapa[clave.toLowerCase()]
    if (!entrada) return
    ev.preventDefault()
    entrada.fn()
  }

  document.addEventListener('keydown', alPulsar)

  return {
    ayuda: () => (dialogo.open ? dialogo.close() : dialogo.showModal()),
    destruir: () => document.removeEventListener('keydown', alPulsar),
  }
}

function nombreVisible(k) {
  return { Space: 'Espacio', ArrowDown: '↓', ArrowUp: '↑', Enter: '↵', Escape: 'Esc' }[k] || k.toUpperCase()
}

function crearAyuda(mapa, titulo) {
  const d = document.createElement('dialog')
  d.className = 'ayuda'
  const filas = Object.entries(mapa)
    .filter(([, v]) => v.desc)
    .map(([k, v]) => `<tr><td><kbd>${nombreVisible(k)}</kbd></td><td>${v.desc}</td></tr>`)
    .join('')
  d.innerHTML = `
    <h2>${titulo}</h2>
    <table><tbody>${filas}</tbody></table>
    <p class="nota">Los atajos no funcionan mientras escribe en un campo.</p>
    <form method="dialog"><button class="boton">Cerrar</button></form>`
  document.body.appendChild(d)
  return d
}
