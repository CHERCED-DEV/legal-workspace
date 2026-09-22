/* La fuente original, cuando es navegable.
 *
 * Hoy solo audio. El contrato admite imagen y PDF, y ese es el sitio donde
 * entrarian sin tocar nada mas.
 *
 * ADR-020 §5: si la fuente no esta, se DICE y se desactiva la comprobacion. No
 * se finge poder comprobar.
 */
import { hms } from './contrato.js'

export function crearMedios(nodoAudio, fuente, { alTiempo, alEstado } = {}) {
  let listo = false

  const api = {
    get listo() { return listo },
    get tiempo() { return nodoAudio?.currentTime ?? 0 },
    get sonando() { return nodoAudio ? !nodoAudio.paused : false },
    duracion: () => nodoAudio?.duration ?? 0,

    /** Retrocede un poco para oir el arranque de la frase. */
    irA(segundos) {
      if (!listo) return false
      nodoAudio.currentTime = Math.max(0, segundos - 0.3)
      nodoAudio.play()
      return true
    },
    alternar() {
      if (!listo) return
      nodoAudio.paused ? nodoAudio.play() : nodoAudio.pause()
    },
    pausar() { if (listo) nodoAudio.pause() },
  }

  if (!nodoAudio || !fuente?.ruta) {
    alEstado?.({ listo: false, motivo: 'sin-fuente' })
    return api
  }

  nodoAudio.src = encodeURI(fuente.ruta)
  nodoAudio.addEventListener('loadedmetadata', () => {
    listo = true
    alEstado?.({ listo: true, duracion: nodoAudio.duration, texto: hms(nodoAudio.duration) })
  })
  nodoAudio.addEventListener('error', () => {
    listo = false
    alEstado?.({ listo: false, motivo: 'no-encontrada' })
  })
  nodoAudio.addEventListener('timeupdate', () => alTiempo?.(nodoAudio.currentTime))
  nodoAudio.addEventListener('play', () => alEstado?.({ listo, sonando: true }))
  nodoAudio.addEventListener('pause', () => alEstado?.({ listo, sonando: false }))
  return api
}
