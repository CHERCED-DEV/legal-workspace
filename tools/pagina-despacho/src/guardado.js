/* Guardar lo que ella declara, ordenado, sin pasar por Descargas.
 *
 * Donde el navegador lo permite (Edge y Chrome, también con la página abierta
 * desde el disco), se elige UNA vez una carpeta y la página escribe en ella:
 *   - «<documento> - en curso.json», al momento, cada vez que marca algo;
 *   - «<documento> - AAAA-MM-DD HH.MM.json», cada vez que pulsa Guardar: esa
 *     copia no se sobrescribe nunca.
 *
 * DÓNDE. La página sabe desde dónde se abrió:
 *   - Dentro de un proyecto del Despacho (…/<proyecto>/2-Borradores/Entregas/
 *     ENTREGA …/, ADR-023; o la forma antigua …/3-Para presentar/ENTREGA …/):
 *     en el PROYECTO, «2-Borradores/Lo que declaré/<entrega>/».
 *     Pedido del dueño el 2026-09-23: lo de ella va con el proyecto, y así
 *     rehacer la entrega (que borra su carpeta) no lo toca. En 2-Borradores y
 *     no en 1-Documentos recibidos: esa es plana y ningún programa escribe en
 *     ella (ADR-018; docs/technical-design/v0/17-deployment-layout.md §3).
 *   - Una entrega suelta (la que ella descomprime): dentro de la entrega, en
 *     «Lo que declaré».
 * Vale elegir esa carpeta o cualquiera por encima (Despacho, el Escritorio):
 * la página baja sola por el camino que conoce, y comprueba que llega.
 * De ahí lo recoge `recoger_lo_declarado.py`, que mira en los dos sitios.
 *
 * Donde no se puede, descarga como antes. El permiso lo concede ella, y el
 * navegador lo vuelve a pedir en cada sesión: sin un clic suyo no se escribe.
 */
const CARPETA = 'Lo que declaré'
export const EN_PROYECTO = ['2-Borradores', CARPETA]
const BD = 'despacho-guardado', ALMACEN = 'carpetas'
const ENTREGA = /^ENTREGA - /

/** Dónde guardar, según la dirección de la página. Sin tocar el disco. */
export function dondeGuardar(href) {
  let segs = []
  try {
    const u = new URL(href)
    if (u.protocol === 'file:') segs = decodeURIComponent(u.pathname).split('/').filter(Boolean)
  } catch { /* sin camino conocido */ }
  // La entrega dentro de un proyecto: «<proyecto>/2-Borradores/Entregas/ENTREGA …/»
  // (ADR-023), o la forma antigua «<proyecto>/3-Para presentar/ENTREGA …/».
  let p = -1, en = -1
  for (let i = 1; i < segs.length - 1; i++) {
    if (!ENTREGA.test(segs[i + 1])) continue
    if (segs[i] === 'Entregas' && segs[i - 1] === '2-Borradores' && i >= 2) { p = i - 2; en = i + 1 }
    else if (segs[i] === '3-Para presentar') { p = i - 1; en = i + 1 }
  }
  if (p >= 0) {
    return { modo: 'proyecto', camino: segs.slice(0, p + 1), proyecto: segs[p], entrega: segs[en],
             dentro: [...EN_PROYECTO, segs[en]] }
  }
  let e = -1
  segs.forEach((s, i) => { if (ENTREGA.test(s) && i < segs.length - 1) e = i })
  if (e >= 0) return { modo: 'entrega', camino: segs.slice(0, e + 1), proyecto: null, entrega: segs[e], dentro: [CARPETA] }
  return { modo: 'libre', camino: [], proyecto: null, entrega: null, dentro: [CARPETA] }
}

/** Desde la carpeta que eligió hasta la de destino, por el camino conocido.
 *  `h` = la elegida. Devuelve { dir, ruta } o { error }. */
export async function bajar(h, donde) {
  const c = donde.camino
  if (donde.modo === 'libre') {
    // Aquí tampoco se escribe suelto: en su carpeta, como se le dijo.
    const dir = await h.getDirectoryHandle(CARPETA, { create: true })
    return { dir, ruta: [h.name, CARPETA] }
  }
  let j = -1
  for (let i = c.length - 1; i >= 0; i--) if (c[i] === h.name) { j = i; break }
  const meta = donde.modo === 'proyecto' ? donde.proyecto : donde.entrega
  if (j < 0) {
    return { error: donde.modo === 'proyecto' && h.name === donde.entrega
      ? `Eligió la carpeta de la entrega. Lo suyo se guarda en el PROYECTO: elija «${meta}» (o una por encima, como «Despacho»).`
      : `«${h.name}» no está en el camino de esta página. Elija «${meta}» o una carpeta por encima de ella.` }
  }
  let dir = h
  try {
    for (const n of c.slice(j + 1)) dir = await dir.getDirectoryHandle(n)
  } catch {
    return { error: `Desde «${h.name}» no se llega a «${meta}». Elija «${meta}» directamente.` }
  }
  if (donde.modo === 'proyecto') {
    try { await dir.getDirectoryHandle('2-Borradores') } catch {
      return { error: `«${dir.name}» no tiene «2-Borradores» dentro: no parece el proyecto. Elija «${meta}».` }
    }
  }
  const ruta = [dir.name]
  for (const n of donde.dentro) { dir = await dir.getDirectoryHandle(n, { create: true }); ruta.push(n) }
  return { dir, ruta }
}

function bd() {
  return new Promise((res, rej) => {
    const r = indexedDB.open(BD, 1)
    r.onupgradeneeded = () => r.result.createObjectStore(ALMACEN)
    r.onsuccess = () => res(r.result)
    r.onerror = () => rej(r.error)
  })
}
async function leerCarpeta(llave) {
  try {
    const d = await bd()
    return await new Promise((res) => {
      const q = d.transaction(ALMACEN).objectStore(ALMACEN).get(llave)
      q.onsuccess = () => res(q.result || null); q.onerror = () => res(null)
    })
  } catch { return null }
}
async function recordarCarpeta(llave, valor) {
  try {
    const d = await bd()
    d.transaction(ALMACEN, 'readwrite').objectStore(ALMACEN).put(valor, llave)
  } catch { /* se pedirá otra vez */ }
}

/** Cuántas declaraciones lleva un documento guardado (para no escribir un
 *  «en curso» vacío encima de uno con trabajo). */
export function cuantoHay(doc) {
  if (!doc || typeof doc !== 'object') return 0
  const n = (o) => (o && typeof o === 'object' ? Object.keys(o).length : 0)
  return n(doc.estado) + n(doc.atribucion) + n(doc.ilegibles) + n(doc.compromisos)
    + Object.values(doc.voces || {}).filter((x) => String(x || '').trim()).length
    + (Array.isArray(doc.glosario) ? doc.glosario.length : 0)
}

const limpio = (s) => (s || 'documento').replace(/[\\/:*?"<>|]/g, '').slice(0, 120)
const sello = () => {
  const d = new Date(), p = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}.${p(d.getMinutes())}.${p(d.getSeconds())}`
}

export function crearGuardado({ titulo, documento, alEstado, clave = '', version = () => null, href = location.href }) {
  const puede = typeof window.showDirectoryPicker === 'function' && window.isSecureContext
  const donde = dondeGuardar(href)
  // Sin entrega conocida, la llave lleva la clave del documento: dos versiones
  // de la misma página no comparten carpeta.
  const llave = `${donde.modo}:${donde.entrega || ''}${donde.modo === 'libre' ? ':' + clave : ''}`
  let carpeta = null      // la carpeta donde se escribe (ya la de destino)
  let ruta = []           // su camino, para decírselo
  let permiso = 'no'      // 'si' | 'pedir' | 'no'
  let reloj = null
  let ultimo = null
  let ocupado = false     // un doble clic no escribe dos veces la misma copia
  // Lo que había en «en curso» al empezar esta sesión. Abierta en otro
  // navegador u otro equipo, la página no sabe lo que ella hizo en el primero:
  // antes de la primera escritura, lo de la carpeta se aparta con fecha, y si
  // aquí no hay nada, no se escribe encima (el recogedor tomaría el vacío por
  // ser el más reciente).
  let previo
  let apartado = false

  const dondeTexto = () => `«${ruta.join(' › ')}»`
  const avisar = (texto, bien = true, escrito = false, v = null) =>
    alEstado?.({ texto, bien, escrito, version: v, carpeta: carpeta?.name || null, permiso })

  async function comprobar(pedir = false) {
    if (!carpeta) { permiso = 'no'; return false }
    try {
      let p = await carpeta.queryPermission({ mode: 'readwrite' })
      if (p !== 'granted' && pedir) p = await carpeta.requestPermission({ mode: 'readwrite' })
      permiso = p === 'granted' ? 'si' : 'pedir'
    } catch { permiso = 'pedir' }
    return permiso === 'si'
  }

  /** Un nombre que no existe todavía: la copia fechada no pisa nunca otra. */
  async function libre(base) {
    for (let k = 1; k < 100; k++) {
      const n = k === 1 ? `${base}.json` : `${base} (${k}).json`
      try { await carpeta.getFileHandle(n) } catch { return n }
    }
    return `${base} (${Date.now()}).json`
  }

  async function escribir(nombre, texto) {
    const f = await carpeta.getFileHandle(nombre, { create: true })
    const w = await f.createWritable()
    await w.write(texto)
    await w.close()
  }

  const enCurso = () => `${limpio(titulo)} - en curso.json`
  async function leerPrevio() {
    try {
      const f = await (await carpeta.getFileHandle(enCurso())).getFile()
      return await f.text()
    } catch { return null }
  }
  async function escribirEnCurso(texto) {
    if (previo === undefined) previo = await leerPrevio()
    if (previo && previo !== texto && !apartado) {
      let hay = 0
      try { hay = cuantoHay(JSON.parse(previo)) } catch { hay = 1 }
      if (hay) await escribir(await libre(`${limpio(titulo)} - ${sello()} - en curso anterior`), previo)
      apartado = true
    }
    await escribir(enCurso(), texto)
    previo = texto
  }

  function explicar() {
    if (donde.modo === 'proyecto') {
      return `Elija la carpeta del PROYECTO: «${donde.proyecto}».\n`
        + 'También vale una por encima (por ejemplo «Despacho»): la página baja sola.\n\n'
        + `Lo que usted declare se guardará en «${donde.proyecto} › ${donde.dentro.join(' › ')}», al momento. `
        + 'Rehacer la entrega no lo toca.'
    }
    if (donde.modo === 'entrega') {
      return `Elija la carpeta de la ENTREGA: «${donde.entrega}» (o una por encima: la página baja sola).\n\n`
        + `Dentro se creará «${CARPETA}», y ahí se guardará lo que usted declare, al momento.`
    }
    return 'Elija la carpeta de la ENTREGA: la que contiene «Transcripciones» y «00 - EMPIECE AQUI».\n\n'
      + `Dentro se creará la carpeta «${CARPETA}», y ahí se guardará lo que usted declare, al momento.`
  }

  async function elegir() {
    if (!confirm(explicar())) return false
    let h
    try {
      h = await window.showDirectoryPicker({ id: `despacho-${donde.modo}`, mode: 'readwrite', startIn: 'desktop' })
    } catch { return false }
    if (donde.modo === 'libre') {
      if (h.name === 'Transcripciones') {
        const e = 'Eligió «Transcripciones»: elija la carpeta de encima, la de la entrega.'
        avisar(e, false); alert(e); return false
      }
      let esEntrega = false
      for await (const [n, e] of h.entries()) if (e.kind === 'directory' && n === 'Transcripciones') esEntrega = true
      if (!esEntrega && !confirm(`«${h.name}» no parece la carpeta de la entrega (no tiene «Transcripciones» dentro). ¿Guardar ahí de todos modos?`)) return false
    }
    let r
    try { r = await bajar(h, donde) } catch (e) { r = { error: 'No se pudo preparar la carpeta: ' + (e?.message || e) } }
    if (r.error) { avisar(r.error, false); alert(r.error); return false }
    carpeta = r.dir
    ruta = r.ruta
    await recordarCarpeta(llave, { dir: carpeta, ruta })
    return comprobar(true)
  }

  const api = {
    get disponible() { return puede },
    get activo() { return permiso === 'si' },
    get carpeta() { return carpeta?.name || null },
    get donde() { return donde },
    async iniciar() {
      if (!puede) return
      const g = await leerCarpeta(llave)
      if (g?.dir) { carpeta = g.dir; ruta = g.ruta || [g.dir.name] }
      await comprobar(false)
      if (permiso === 'si') {
        previo = await leerPrevio()
        let antes = null
        try { antes = previo ? JSON.parse(previo) : null } catch { antes = null }
        if (antes && cuantoHay(antes) && !cuantoHay(documento()) && (!clave || antes.clave === clave)) {
          const cuando = antes.exportado ? new Date(antes.exportado).toLocaleString('es-CO') : 'antes'
          avisar(`En ${dondeTexto()} está lo que guardó el ${cuando} (${cuantoHay(antes)} declaraciones), y este navegador `
            + `no lo tiene: use «Cargar» con «${enCurso()}» para seguir con ello. No se escribe encima.`, false)
          return
        }
        avisar(`Guardando en ${dondeTexto()} al momento.`); api.cambio()
      }
      else if (carpeta) avisar(`Para seguir guardando en ${dondeTexto()}, pulse «Guardar lo comprobado».`, false)
    },
    /** Lo pulsó ella: guarda la copia fechada (y, si hace falta, pide la carpeta).
     *  true = guardado; 'cancelado' = no eligió carpeta; false = no se pudo. */
    async guardar() {
      if (!puede) return false
      if (ocupado) return true
      ocupado = true
      try {
        if (!carpeta || !(await comprobar(true))) {
          if (!(await elegir())) return 'cancelado'
        }
        const v = version()
        const texto = JSON.stringify(documento(), null, 1)
        await escribirEnCurso(texto)
        await escribir(await libre(`${limpio(titulo)} - ${sello()}`), texto)
        ultimo = new Date()
        avisar(`Guardado en ${dondeTexto()} a las ${ultimo.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' })}, con una copia fechada`, true, true, v)
        return true
      } catch (e) {
        avisar('No se pudo guardar en la carpeta: ' + (e?.message || e) + '. Use la descarga.', false)
        return false
      } finally { ocupado = false }
    },
    /** Una copia fechada de lo que hay AHORA, con un motivo en el nombre (p. ej.
     *  «antes de cargar»), si ya hay permiso. No pide nada. */
    async copia(motivo) {
      if (permiso !== 'si') return false
      try {
        await escribir(await libre(`${limpio(titulo)} - ${sello()} - ${motivo}`), JSON.stringify(documento(), null, 1))
        return true
      } catch { return false }
    },
    /** Tras cada cambio: el «en curso», sin preguntar nada, si ya hay permiso. */
    cambio() {
      if (permiso !== 'si') return
      clearTimeout(reloj)
      reloj = setTimeout(async () => {
        try {
          const v = version()
          await escribirEnCurso(JSON.stringify(documento(), null, 1))
          ultimo = new Date()
          avisar(`Guardado solo en ${dondeTexto()} a las ${ultimo.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' })}`, true, true, v)
          if (v != null && v !== version()) api.cambio()
        } catch {
          permiso = 'pedir'
          avisar('Se perdió el permiso para guardar en la carpeta: pulse «Guardar lo comprobado».', false)
        }
      }, 2500)
    },
  }
  return api
}
