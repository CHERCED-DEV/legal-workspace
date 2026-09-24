/* Oír UNA línea y compararla con las otras lecturas automáticas.
 *
 * Pedido del dueño el 2026-09-23 sobre el desplegable «Otras lecturas…»:
 * poder oír ahí lo que se dice para confirmar las palabras que no están
 * claras. Tres cosas:
 *   - oír la línea (y solo la línea: se para al final), despacio o en bucle;
 *   - de cada lectura, la parte que parece corresponder a la línea, con lo
 *     que difiere en negrita (lecturas.js); lo de alrededor, en gris;
 *   - dónde no coinciden, y desde ahí empezar SU corrección con lo que
 *     escribió otra lectura. Solo después de oírla: una lectura de la
 *     máquina no es lo que se dijo, y proponerla sin oír sería dictársela.
 * Nada cambia la transcripción.
 */
import { crearOido, anunciarPanel, alAbrirOtro } from './oido.js'
import { alinear, discordias, conCambio, normal } from './lecturas.js'
import { escapar as esc } from './resalte.js'
import { hms } from './contrato.js'

const tramoDe = (b) => ({ id: 'linea:' + b.id, desde: b.ancla.inicio, hasta: b.ancla.fin })
const corta = (f) => String(f || '').replace(/^Lectura (del |de los |de la )?/, '')

/** El reproductor de una línea, uno para toda la página. */
export function crearOirLinea(medios, { alCambiar } = {}) {
  const oido = crearOido(medios)
  let actual = null, repetir = false, despacio = false, antes = null, reloj = null
  const restaurar = () => { if (antes != null) { medios.velocidad = antes; antes = null } }
  const avisa = (b) => b && alCambiar?.(b)

  const api = {
    get actual() { return actual },
    get repetir() { return repetir },
    get despacio() { return despacio },
    sonandoEn(b) { return actual?.id === b.id && oido.sonandoAqui },
    fraccion(b) { return oido.fraccion(tramoDe(b)) },
    oida(b) { return oido.basta(tramoDe(b)) },
    oir(b) {
      clearTimeout(reloj)
      if (api.sonandoEn(b)) { medios.pausar(); restaurar(); avisa(b); return }
      anunciarPanel('linea')
      const previo = actual
      actual = b
      restaurar()
      if (despacio) { antes = medios.velocidad; medios.velocidad = Math.min(antes, 0.75) }
      oido.abrir(tramoDe(b))
      oido.oir()
      if (previo && previo.id !== b.id) avisa(previo)
      avisa(b)
    },
    alternarDespacio(b) {
      despacio = !despacio
      if (api.sonandoEn(b)) {
        if (despacio) { antes = medios.velocidad; medios.velocidad = Math.min(antes, 0.75) } else restaurar()
      }
      avisa(b)
    },
    alternarRepetir(b) { repetir = !repetir; if (!repetir) clearTimeout(reloj); avisa(b) },
    parar() {
      clearTimeout(reloj)
      if (!actual) return
      const b = actual
      oido.cerrar(); restaurar(); actual = null
      avisa(b)
    },
    alTiempo(t) {
      if (!actual) return
      const b = actual
      const sonaba = oido.sonandoAqui
      oido.alTiempo(t)
      if (sonaba && !oido.sonandoAqui) {
        restaurar()
        // Al final de la línea (no un salto a otra parte), y en bucle: otra vez.
        if (repetir && !medios.sonando && t >= b.ancla.fin) reloj = setTimeout(() => { if (actual === b) api.oir(b) }, 700)
      }
      avisa(b)
    },
  }
  alAbrirOtro('linea', () => api.parar())
  return api
}

/** El desplegable de una línea. `texto()` da la línea transcrita (sin glosario). */
export function montarOtrasLecturas(b, { oir, texto, alCorregir }) {
  const d = document.createElement('details')
  d.className = 'alternativas'
  const n = b.alternativas.length
  d.innerHTML = `<summary>${n === 1 ? 'Otra lectura automática escribió' : `Otras ${n} lecturas automáticas escribieron`} algo distinto — óigalo y compare</summary>
    <div class="ol-oir">
      <button type="button" class="boton primaria ol-play">▶ Oír la línea</button>
      <button type="button" class="boton ol-despacio" aria-pressed="false" title="A 0,75×, solo esta línea">🐢 Despacio</button>
      <button type="button" class="boton ol-repetir" aria-pressed="false" title="Vuelve a sonar al acabar">↻ Repetir</button>
      <span class="vz-barra oir ol-barra" aria-hidden="true"><i></i></span>
      <span class="ol-estado"></span>
    </div>
    <div class="ol-cuerpo"></div>`
  const $d = (s) => d.querySelector(s)
  let hecho = false

  function pintarCuerpo() {
    hecho = true
    const linea = texto()
    const ds = discordias(linea, b.alternativas)
    const partes = []
    if (ds.length) {
      partes.push('<div class="ol-discordias"><p class="ol-t"><strong>Donde no coinciden</strong> con la transcripción'
        + ' <span class="ol-sub">— tras oírla, pulse la que se oye para empezar su corrección con ella</span></p><ul>')
      ds.forEach((x, i) => {
        const grupos = new Map()
        x.lecturas.forEach((l) => {
          const k = normal(l.lee) || '∅'
          if (!grupos.has(k)) grupos.set(k, { ...l, fuentes: [], largas: [] })
          grupos.get(k).fuentes.push(corta(l.fuente))
          grupos.get(k).largas.push(l.fuente)
        })
        partes.push(`<li><span class="ol-dice">aquí dice <strong>«${esc(x.dice)}»</strong></span> <span class="ol-flecha">→</span> `
          + [...grupos.values()].map((g, j) => `<button type="button" class="ol-usar" data-i="${i}" data-j="${j}" disabled>`
            + `${g.lee ? `«${esc(g.lee)}»` : '<em>nada</em>'}</button> <span class="ol-fuente">${esc(g.fuentes.join(', '))}</span>`).join(' ')
          + '</li>')
        x.grupos = [...grupos.values()]
      })
      partes.push('</ul></div>')
    }
    partes.push('<div class="ol-lecturas">')
    for (const a of b.alternativas) {
      const al = alinear(linea, a.texto, a.pos ?? null)
      const et = `<span class="et">${esc(a.fuente)}${a.desde != null ? ` · ${hms(a.desde)}–${hms(a.hasta)}` : ''}</span>`
      if (!al) {
        partes.push(`<p class="ol-lectura">${et}<span class="ol-ctx">${esc(a.texto)}</span> <em class="ol-sin">(no se ve qué parte corresponde a esta línea)</em></p>`)
        continue
      }
      const antes = al.antes.length > 10 ? '… ' + al.antes.slice(-10).join(' ') : al.antes.join(' ')
      const despues = al.despues.length > 12 ? al.despues.slice(0, 12).join(' ') + ' …' : al.despues.join(' ')
      const tramo = al.tramo.map((x) => x.igual ? esc(x.w) : `<strong>${esc(x.w)}</strong>`).join(' ')
      partes.push(`<p class="ol-lectura">${et}${antes ? `<span class="ol-ctx">${esc(antes)}</span> ` : ''}`
        + `<span class="ol-tramo">${tramo}</span>${despues ? ` <span class="ol-ctx">${esc(despues)}</span>` : ''}`
        + `${al.igual ? ' <span class="ol-igual">✓ coincide con la transcripción</span>' : ''}</p>`)
    }
    partes.push('</div><p class="ol-nota">Cada lectura escribió un tramo de 20 s: esta línea y las de alrededor, que van en gris. '
      + 'La parte que parece corresponder a esta línea se busca por <strong>parecido del texto</strong>, y en ella va '
      + '<strong>en negrita lo que difiere</strong>. Son lecturas de una máquina: <strong>solo oír dice qué se dijo</strong>.</p>')
    $d('.ol-cuerpo').innerHTML = partes.join('')
    d.querySelectorAll('.ol-usar').forEach((btn) => btn.addEventListener('click', (e) => {
      e.stopPropagation()
      const x = ds[Number(btn.dataset.i)], g = x.grupos[Number(btn.dataset.j)]
      alCorregir(b, conCambio(texto(), g.cambio, g.lee), g.largas.join('; '))
    }))
    pintar()
  }

  function pintar() {
    const fr = oir.fraccion(b), ya = oir.oida(b), aqui = oir.sonandoEn(b)
    $d('.ol-play').textContent = aqui ? '❚❚ Pausa' : fr > 0 ? '↻ Oír otra vez' : '▶ Oír la línea'
    $d('.ol-despacio').setAttribute('aria-pressed', String(oir.despacio))
    $d('.ol-despacio').classList.toggle('elegida', oir.despacio)
    $d('.ol-repetir').setAttribute('aria-pressed', String(oir.repetir))
    $d('.ol-repetir').classList.toggle('elegida', oir.repetir)
    $d('.ol-barra i').style.width = `${Math.min(100, fr * 100)}%`
    $d('.ol-barra').classList.toggle('llega', ya)
    $d('.ol-estado').textContent = ya ? 'Oída' : fr > 0 ? `Oída al ${Math.floor(fr * 100)} %` : ''
    d.querySelectorAll('.ol-usar').forEach((x) => {
      x.disabled = !ya
      x.title = ya ? 'Empezar su corrección con esta lectura (la puede cambiar antes de aceptar)' : 'Óigala primero'
    })
  }

  d.addEventListener('toggle', () => { if (d.open && !hecho) pintarCuerpo() })
  d.addEventListener('click', (e) => { if (e.target.closest('button')) e.stopPropagation() })
  $d('.ol-play').addEventListener('click', () => oir.oir(b))
  $d('.ol-despacio').addEventListener('click', () => oir.alternarDespacio(b))
  $d('.ol-repetir').addEventListener('click', () => oir.alternarRepetir(b))
  return { nodo: d, pintar: () => { if (hecho) pintar() } }
}
