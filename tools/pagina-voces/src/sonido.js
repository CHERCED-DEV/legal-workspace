/* Oir exactamente una linea. ADR-020 §5.
 *
 * Una etiqueta <audio> por grabacion, para no recargar al saltar entre
 * grabaciones. El audio va por ruta relativa; si no esta, se DICE y se ofrece
 * buscarlo a mano -- el archivo se abre en local, no se sube a ningun sitio, y
 * se rechaza si no dura lo mismo que la grabacion: oir otra y declarar
 * «oyendo» seria peor que no oir.
 *
 * Quien habla rapido se oye mejor mas lento, y quien habla lento aburre: la
 * velocidad se cambia sin cambiar el tono (preservesPitch).
 */

/** Cada tramo de la ruta, codificado: un «#» o un «?» en un nombre de archivo
 * cortaba la ruta, y la grabacion no sonaba nunca al abrir desde disco. */
export function rutaSegura(ruta) {
  if (/^[a-z]+:/i.test(ruta)) return encodeURI(ruta)
  return ruta.split('/').map((s) => (s === '..' || s === '.' ? s : encodeURIComponent(s))).join('/')
}

export function crearSonido(audios, { alEstado, alTiempo, alTerminar } = {}) {
  const pistas = {}
  let actual = null            // { id, ini, fin, marca }
  let velocidad = 1
  let vigilante = 0

  for (const a of audios) {
    const el = document.createElement('audio')
    el.preload = 'metadata'
    el.dataset.audio = a.id
    const p = { el, a, listo: false, fallo: false, otra: false, manual: false }
    pistas[a.id] = p
    el.addEventListener('loadedmetadata', () => {
      if (p.manual && a.duracion && Math.abs(el.duration - a.duracion) > 1.5) {
        p.listo = false; p.fallo = true; p.otra = true
        alEstado?.(a.id, 'otra')
        return
      }
      p.listo = true; p.fallo = false; p.otra = false
      alEstado?.(a.id, 'lista')
    })
    el.addEventListener('error', () => { p.listo = false; p.fallo = true; alEstado?.(a.id, 'falta') })
    el.addEventListener('pause', () => alEstado?.(a.id, 'pausa'))
    el.addEventListener('play', () => alEstado?.(a.id, 'suena'))
    // Respaldo del vigilante: con la pestana en segundo plano el navegador
    // congela requestAnimationFrame y la linea seguia sonando mas alla de su
    // final. timeupdate sigue llegando (unas 4 veces por segundo).
    el.addEventListener('timeupdate', () => { if (actual?.id === a.id) comprobar() })
    el.addEventListener('ended', () => {
      if (actual?.id !== a.id) return
      const hecho = actual
      parar()
      alTerminar?.({ ...hecho, fin: Math.min(hecho.fin, el.duration || hecho.fin) })
    })
    el.src = rutaSegura(a.ruta)
    document.body.appendChild(el)
  }

  function parar() {
    cancelAnimationFrame(vigilante)
    if (actual) {
      pistas[actual.id]?.el.pause()
      actual = null
    }
  }

  function comprobar() {
    if (!actual) return false
    const p = pistas[actual.id]
    alTiempo?.(actual, p.el.currentTime)
    if (p.el.currentTime >= actual.fin) {
      const hecho = actual
      parar()
      alTerminar?.(hecho)
      return false
    }
    return true
  }

  function vigilar() {
    if (comprobar()) vigilante = requestAnimationFrame(vigilar)
  }

  return {
    get velocidad() { return velocidad },
    estado(id) {
      const p = pistas[id]
      return !p ? 'no' : p.listo ? 'lista' : p.otra ? 'otra' : p.fallo ? 'falta' : 'cargando'
    },
    suena() { return !!actual },

    /** Oye [ini, fin] de la grabacion `id`. `marca` viaja con los avisos de
     * tiempo, para saber de que linea es lo que se esta oyendo. */
    oir(id, ini, fin, { antes = 0.25, despues = 0.2, marca = null } = {}) {
      const p = pistas[id]
      if (!p || p.fallo || p.otra) return false
      parar()
      p.el.playbackRate = velocidad
      try { p.el.preservesPitch = true } catch { /* navegadores viejos */ }
      p.el.currentTime = Math.max(0, ini - antes)
      actual = { id, ini, fin: fin + despues, marca }
      const r = p.el.play()
      if (r && r.catch) r.catch(() => { actual = null; alEstado?.(id, 'bloqueado') })
      vigilante = requestAnimationFrame(vigilar)
      return true
    },

    parar,

    fijarVelocidad(x) {
      velocidad = x
      for (const p of Object.values(pistas)) p.el.playbackRate = x
    },

    /** Si la ruta relativa no llega, ella elige el archivo. Todo en local. */
    usarArchivo(id, file) {
      const p = pistas[id]
      if (!p || !file) return
      p.fallo = false; p.listo = false; p.otra = false; p.manual = true
      p.el.src = URL.createObjectURL(file)
      p.el.load()
    },
  }
}
