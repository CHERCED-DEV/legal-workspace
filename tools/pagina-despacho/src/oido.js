/* Cuánto de un tramo ha OÍDO ella. Lo comparten los tres paneles que
 * preguntan algo después de hacer oír un trozo: ninguno deja decidir sin oír.
 *
 * Lo oído es la UNIÓN de lo que sonó, medida sobre las zonas que importan (el
 * habla de las líneas, no los silencios de en medio). Oír dos veces el mismo
 * trozo no suma; saltar al final o dejar sonar otra parte, tampoco.
 */
import { unir, fraccionOida, OIDA_MINIMA } from './atribucion.js'

export function crearOido(medios) {
  const oidos = new Map()     // id -> intervalos oídos
  let tramo = null, ultimo = null, cortar = false

  const zonasDe = (t) => t.zonas?.length ? t.zonas : [[t.desde, t.hasta]]
  const api = {
    get tramo() { return tramo },
    get sonandoAqui() { return !!tramo && cortar && medios.sonando },
    fraccion(t = tramo) { return t ? fraccionOida(oidos.get(t.id) || [], zonasDe(t)) : 0 },
    basta(t = tramo) { return medios.listo && api.fraccion(t) >= OIDA_MINIMA },
    /** `t` = { id, desde, hasta, zonas? } */
    abrir(t) { tramo = t; ultimo = null },
    /** Desde el principio del tramo. */
    oir() {
      if (!tramo) return false
      cortar = true
      ultimo = null
      return medios.irA(tramo.desde)
    },
    /** Pausa, o sigue desde donde se paró si está dentro del tramo. */
    alternar() {
      if (!tramo) return
      if (api.sonandoAqui) { medios.pausar(); return }
      const t = medios.tiempo
      if (t > tramo.desde + 0.3 && t < tramo.hasta - 0.3 && medios.reanudar) {
        cortar = true; ultimo = null; medios.reanudar()
      } else api.oir()
    },
    /** ¿Pausado a mitad? Para decir «Seguir oyendo» en vez de «Oír otra vez». */
    get pausadoAMitad() {
      if (!tramo || medios.sonando) return false
      const t = medios.tiempo
      return t > tramo.desde + 0.3 && t < tramo.hasta - 0.3 && api.fraccion() > 0
    },
    cerrar() {
      if (cortar && medios.sonando) medios.pausar()
      tramo = null; cortar = false; ultimo = null
    },
    /** En cada instante del audio. Devuelve true si hay tramo abierto. */
    alTiempo(t) {
      if (!tramo) return false
      if (medios.sonando && ultimo != null && t > ultimo && t - ultimo < 1.5) {
        const a = Math.max(ultimo, tramo.desde), b = Math.min(t, tramo.hasta)
        if (b > a) oidos.set(tramo.id, unir(oidos.get(tramo.id) || [], a, b))
      }
      // Un salto (ella pulsó otra hora, la franja, «n»…) no es el fragmento:
      // ese audio es suyo y no se corta.
      if (ultimo != null && (Math.abs(t - ultimo) > 1.5 || t < tramo.desde - 0.6 || t > tramo.hasta + 1.5)) cortar = false
      ultimo = t
      if (cortar && medios.sonando && t >= tramo.hasta + 0.15) { medios.pausar(); cortar = false }
      return true
    },
  }
  return api
}

/** Avisa a los demás paneles de que este abre su pregunta: solo una a la vez. */
export function anunciarPanel(nombre) {
  document.dispatchEvent(new CustomEvent('despacho:panel', { detail: nombre }))
}
export function alAbrirOtro(nombre, fn) {
  document.addEventListener('despacho:panel', (e) => { if (e.detail !== nombre) fn() })
}

/** Con un panel de pregunta abierto, las teclas de la página se quedan fuera:
 *  «c» marcaba el TEXTO de la línea como confirmado sin haberla oído. */
export const TECLAS_DE_LA_PAGINA = new Set(['c', 'C', 'o', 'O', 'x', 'X', 's', 'S', 'n', 'N', 'j', 'J', 'k', 'K',
  'd', 'D', 't', 'T', 'v', 'V', 'l', 'L', 'Enter', 'ArrowUp', 'ArrowDown', '?'])
