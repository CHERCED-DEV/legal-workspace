/* ¿Está la página en su sitio, con las grabaciones a su lado?
 *
 * Abrir con doble clic un archivo DENTRO de un .zip hace que Windows copie
 * solo ese archivo a una carpeta temporal y lo abra desde ahí: la página se ve,
 * pero sola, y no suena nada. Pasó el 2026-09-24 con la entrega de una mesa de
 * trabajo, y la página no dijo nada: parecía rota. Ahora lo dice arriba, grande,
 * con los pasos para arreglarlo.
 *
 * Dos señales, independientes:
 *   - la dirección de la página tiene la forma de una copia temporal de un .zip
 *     (se sabe al abrir, antes de intentar cargar nada);
 *   - las grabaciones no cargan (se sabe cuando el navegador lo dice).
 */

// Cómo nombran esa carpeta temporal los programas que abren un .zip.
const PATRONES_ZIP = [
  // Explorador de Windows 11: …\Temp\<guid>_<nombre>.zip.<3 letras>\
  /\/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}_[^/]*\.zip\.[0-9a-z]{1,8}\//i,
  // Explorador de Windows 10: …\Temp\Temp1_<nombre>.zip\
  /\/Temp\d*_[^/]*\.zip\//i,
  // 7-Zip: …\Temp\7zO1A2B3C4D\
  /\/7zO[0-9A-F]{4,}\//i,
  // WinRAR: …\Temp\Rar$DIa1234.5678\
  /\/Rar\$[A-Z]{2}[0-9a-z.]+\//i,
  // Cualquier visor que enseñe el .zip como si fuera una carpeta.
  /\.zip\//i,
]

export function abiertaDesdeZip(href) {
  let camino = ''
  try {
    const u = new URL(href)
    if (u.protocol !== 'file:') return false
    camino = decodeURIComponent(u.pathname)
  } catch { return false }
  return PATRONES_ZIP.some((re) => re.test(camino))
}

/** 'mac' | 'windows' | 'otro': los pasos para extraer un .zip no son los mismos. */
export function sistema(ua = (typeof navigator !== 'undefined' ? navigator.userAgent : ''), plataforma = (typeof navigator !== 'undefined' ? navigator.platform : '')) {
  if (/Mac/i.test(plataforma) || /Macintosh|Mac OS X/i.test(ua)) return 'mac'
  if (/Win/i.test(plataforma) || /Windows/i.test(ua)) return 'windows'
  return 'otro'
}

/** El navegador, solo para NOMBRARLO en los avisos. Lo que decide qué se puede
 *  hacer es la capacidad (showDirectoryPicker), no el nombre. */
export function navegador(ua = (typeof navigator !== 'undefined' ? navigator.userAgent : '')) {
  if (/Edg\//.test(ua)) return 'Edge'
  if (/Firefox\//.test(ua)) return 'Firefox'
  if (/Chrome\/|Chromium\//.test(ua)) return 'Chrome'
  if (/Safari\//.test(ua)) return 'Safari'
  return 'este navegador'
}

export function pasosExtraer(so = sistema()) {
  if (so === 'mac') {
    return 'Cierre esta pestaña. En el Finder, haga doble clic sobre el archivo .zip: el Mac crea al lado '
      + 'una carpeta con el mismo nombre. Abra esa carpeta y, dentro, la página “INICIO”, sin mover ni '
      + 'renombrar nada.'
  }
  return 'Cierre esta pestaña. En la carpeta donde está el .zip, haga clic derecho sobre él, '
    + 'elija “Extraer todo…” y después “Extraer”. Abra la página desde la carpeta que se crea '
    + '(empiece por “INICIO”), sin mover ni renombrar nada de dentro.'
}

/** El aviso que toca, o null si todo está en su sitio.
 *  `faltan` = nombres de archivo de las grabaciones que no cargan; `total` = cuántas hay. */
export function avisoDeSitio({ zip = false, faltan = [], total = 0, so = sistema() } = {}) {
  const EXTRAER = pasosExtraer(so)
  if (zip) {
    return {
      grave: true,
      titulo: 'Está abriendo esta página desde dentro del archivo .zip',
      texto: 'Así se abre sola, sin las grabaciones ni las demás páginas: no suena nada y no se puede '
        + 'guardar en el proyecto. ' + EXTRAER,
    }
  }
  if (total && faltan.length >= total) {
    return {
      grave: true,
      titulo: total === 1 ? 'Esta página no encuentra la grabación a su lado'
        : `Esta página no encuentra ninguna de las ${total} grabaciones a su lado`,
      texto: 'Sin ellas no se puede oír ninguna línea, y lo que decida sin oír no cuenta como declarado '
        + 'oyendo. Suele pasar al abrirla desde dentro del .zip, o al sacarla de su carpeta. ' + EXTRAER,
    }
  }
  if (faltan.length) {
    const lista = faltan.map((n) => `“${n}”`).join(', ')
    return {
      grave: false,
      titulo: faltan.length === 1 ? `Falta una grabación junto a esta página: ${lista}`
        : `Faltan ${faltan.length} grabaciones junto a esta página: ${lista}`,
      texto: 'Las líneas de esa grabación no se pueden oír. Compruebe que extrajo el .zip entero y que '
        + 'no movió ni renombró nada. Si la tiene en otro sitio, puede buscarla desde la tarjeta de '
        + 'cualquiera de sus líneas (no sale de su equipo).',
    }
  }
  return null
}
