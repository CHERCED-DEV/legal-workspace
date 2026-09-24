/* Guardar la declaración en la carpeta del PROYECTO, sin pasar por Descargas.
 *
 * Antes solo se descargaba, y ella tenía que mover el archivo de Descargas a
 * «2-Borradores/Voces»: el paso que más se pierde, y del que depende la
 * etapa 2. Ahora, donde el navegador lo permite (Edge y Chrome, también con la
 * página abierta desde el disco), se elige UNA vez una carpeta y la página
 * escribe en ella. Misma idea que tools/pagina-despacho/src/guardado.js:
 *   - «voces declaradas - <título>.json» se reescribe al momento con cada
 *     decisión. Es lo que leen `genoma_de_voz.py aplicar` y el comprobador
 *     de INICIO;
 *   - cada vez que pulsa Guardar, además, una copia fechada que no se pisa nunca.
 *
 * DÓNDE. La página vive en «<proyecto>/2-Borradores/Voces/» y escribe a su lado.
 * Vale elegir el proyecto o cualquier carpeta por encima (el Escritorio,
 * Descargas): baja sola por el camino que conoce, y comprueba que llega.
 *
 * NUNCA SE PIERDE LO DE OTRO NAVEGADOR. Lo que ella marca vive también en el
 * navegador, y otro navegador (u otro equipo) no lo tiene. Antes de la primera
 * escritura de cada sesión se lee lo que hay en la carpeta:
 *   - si esta página está vacía y en la carpeta hay decisiones, se le ofrece
 *     cargarlas; no se escribe encima;
 *   - si en la carpeta hay decisiones que esta página no tiene, se apartan con
 *     fecha («… - anterior.json») antes de escribir.
 * Lo guardado minutos antes en la misma sesión NO se aparta: lo tiene ya
 * (la página de las grabaciones sí lo hacía, y llenaba la carpeta de copias).
 *
 * Donde no se puede (Firefox, una dirección http, o abierta desde un .zip),
 * se descarga como antes.
 */
import { abiertaDesdeZip } from './sola.js'

const BD = 'despacho-guardado', ALMACEN = 'carpetas'
const igual = (a, b) => String(a || '').normalize('NFC') === String(b || '').normalize('NFC')

/** Dónde guardar, según la dirección de la página. Sin tocar el disco. */
export function dondeVoces(href) {
  let segs = []
  try {
    const u = new URL(href)
    if (u.protocol === 'file:') segs = decodeURIComponent(u.pathname).split('/').filter(Boolean)
  } catch { /* sin camino conocido */ }
  const n = segs.length
  if (n >= 4 && igual(segs[n - 2], 'Voces') && igual(segs[n - 3], '2-Borradores')) {
    return { modo: 'proyecto', camino: segs.slice(0, n - 3), proyecto: segs[n - 4], dentro: ['2-Borradores', 'Voces'] }
  }
  return { modo: 'libre', camino: segs.slice(0, Math.max(0, n - 1)), proyecto: null, dentro: [] }
}

/** Desde la carpeta que eligió hasta la de destino. Devuelve { dir, ruta } o { error }. */
export async function bajarVoces(h, donde) {
  if (donde.modo === 'libre') return { dir: h, ruta: [h.name] }
  const c = donde.camino
  let j = -1
  for (let i = c.length - 1; i >= 0; i--) if (igual(c[i], h.name)) { j = i; break }
  const meta = donde.proyecto
  if (j < 0) {
    return { error: igual(h.name, 'Voces') || igual(h.name, '2-Borradores')
      ? `Eligió “${h.name}”. Elija la carpeta del PROYECTO, “${meta}” (o una por encima, como el Escritorio).`
      : `“${h.name}” no está en el camino de esta página. Elija “${meta}” o una carpeta por encima de ella.` }
  }
  let dir = h
  try {
    for (const nombre of c.slice(j + 1)) dir = await dir.getDirectoryHandle(nombre)
  } catch {
    return { error: `Desde “${h.name}” no se llega a “${meta}”. Elija “${meta}” directamente.` }
  }
  const ruta = [dir.name]
  try {
    for (const nombre of donde.dentro) { dir = await dir.getDirectoryHandle(nombre); ruta.push(nombre) }
  } catch {
    return { error: `“${ruta[0]}” no tiene “${donde.dentro.join(' › ')}” dentro: no parece el proyecto de esta página. Elija “${meta}”.` }
  }
  return { dir, ruta }
}

/** ¿Tiene `ahora` todo lo que había en `antes`? Si no, escribir encima perdería algo. */
export function cubre(ahora, antes) {
  if (!antes || typeof antes !== 'object') return true
  const L = ahora?.lineas || {}
  for (const k of Object.keys(antes.lineas || {})) if (!L[k]) return false
  const V = ahora?.voces || {}
  for (const [k, v] of Object.entries(antes.voces || {})) {
    if (v && String(v.nombre || '').trim() && !String(V[k]?.nombre || '').trim()) return false
  }
  if (antes.declarado_por && ahora?.declarado_por && !igual(antes.declarado_por, ahora.declarado_por)) return false
  return true
}

export const decididas = (d) => Object.keys(d?.lineas || {}).length

export const limpio = (s) => (s || 'reunion').replace(/[\\/:*?"<>|]/g, '').trim().slice(0, 100)
const sello = () => {
  const d = new Date(), p = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}.${p(d.getMinutes())}.${p(d.getSeconds())}`
}
export const nombreVigente = (titulo) => `voces declaradas - ${limpio(titulo)}.json`

function bd() {
  return new Promise((res, rej) => {
    const r = indexedDB.open(BD, 1)
    r.onupgradeneeded = () => r.result.createObjectStore(ALMACEN)
    r.onsuccess = () => res(r.result)
    r.onerror = () => rej(r.error)
  })
}
async function leerRecordada(llave) {
  try {
    const d = await bd()
    return await new Promise((res) => {
      const q = d.transaction(ALMACEN).objectStore(ALMACEN).get(llave)
      q.onsuccess = () => res(q.result || null); q.onerror = () => res(null)
    })
  } catch { return null }
}
async function recordar(llave, valor) {
  try {
    const d = await bd()
    d.transaction(ALMACEN, 'readwrite').objectStore(ALMACEN).put(valor, llave)
  } catch { /* se pedirá otra vez */ }
}

/**
 * `documento()` = la declaración completa (la misma que se descarga).
 * `alEstado({ texto, bien, escrito, activo })` para la cabecera.
 */
export function crearCarpetaVoces({ titulo, clave, documento, alEstado, href = location.href }) {
  const zip = abiertaDesdeZip(href)
  const puede = typeof window.showDirectoryPicker === 'function' && window.isSecureContext && !zip
  const donde = dondeVoces(href)
  const llave = `voces:${donde.modo}:${donde.proyecto || ''}:${clave}`
  const vigente = nombreVigente(titulo)
  let carpeta = null
  let ruta = []
  let permiso = 'no'        // 'si' | 'pedir' | 'no'
  let revisada = false      // ya se miró lo que había en la carpeta en esta sesión
  let reloj = null
  let ocupado = false
  let ultimo = null

  const dondeTexto = () => `“${ruta.join(' › ')}”`
  const hora = (d) => d.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' })
  const avisar = (texto, bien = true, escrito = false) =>
    alEstado?.({ texto, bien, escrito, activo: permiso === 'si', ruta: ruta.slice() })

  async function comprobar(pedir = false) {
    if (!carpeta) { permiso = 'no'; return false }
    try {
      let p = await carpeta.queryPermission({ mode: 'readwrite' })
      if (p !== 'granted' && pedir) p = await carpeta.requestPermission({ mode: 'readwrite' })
      permiso = p === 'granted' ? 'si' : 'pedir'
    } catch { permiso = 'pedir' }
    return permiso === 'si'
  }

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
  async function leerVigente() {
    try {
      const f = await (await carpeta.getFileHandle(vigente)).getFile()
      const texto = await f.text()
      let datos = null
      try { datos = JSON.parse(texto) } catch { datos = null }
      return { texto, datos, cuando: f.lastModified ? new Date(f.lastModified) : null }
    } catch { return null }
  }

  /** Lo que hay en la carpeta antes de escribir por primera vez en esta sesión.
   *  Devuelve null si se puede escribir, o { previo } si hay que preguntarle. */
  async function revisar(forzar) {
    if (revisada) return null
    const hay = await leerVigente()
    const ahora = documento()
    if (hay) {
      const antes = hay.datos
      const deOtra = !antes || antes.formato !== 'despacho/voces-linea-a-linea' || antes.clave !== clave
      if (!deOtra && !forzar && decididas(antes) && !decididas(ahora)) return { previo: antes, cuando: hay.cuando }
      if (deOtra || !cubre(ahora, antes)) {
        await escribir(await libre(`voces declaradas - ${limpio(titulo)} - ${sello()} - anterior`), hay.texto)
      }
    }
    revisada = true
    return null
  }

  async function elegir() {
    const explica = donde.modo === 'proyecto'
      ? `Elija la carpeta del PROYECTO: “${donde.proyecto}”.\n`
        + 'También vale una por encima (por ejemplo, el Escritorio): la página baja sola.\n\n'
        + `Su declaración se guardará en “${donde.proyecto} › 2-Borradores › Voces”, y desde entonces se guarda sola con cada decisión.`
      : 'Elija la carpeta donde guardar su declaración (lo normal: la carpeta “Voces” del proyecto).\n\n'
        + 'Desde entonces se guarda sola con cada decisión.'
    if (!confirm(explica)) return false
    let h
    try {
      h = await window.showDirectoryPicker({ id: 'despacho-voces', mode: 'readwrite', startIn: 'desktop' })
    } catch { return false }
    let r
    try { r = await bajarVoces(h, donde) } catch (e) { r = { error: 'No se pudo abrir esa carpeta: ' + (e?.message || e) } }
    if (r.error) { avisar(r.error, false); alert(r.error); return { error: r.error } }
    carpeta = r.dir
    ruta = r.ruta
    revisada = false
    await recordar(llave, { dir: carpeta, ruta })
    return comprobar(true)
  }

  const api = {
    get disponible() { return puede },
    get activo() { return permiso === 'si' },
    get zip() { return zip },
    get donde() { return donde },
    get ruta() { return ruta.slice() },

    async iniciar() {
      if (!puede) return
      const g = await leerRecordada(llave)
      if (g?.dir) { carpeta = g.dir; ruta = g.ruta || [g.dir.name] }
      if (!carpeta) return
      if (await comprobar(false)) {
        const r = await revisar(false)
        if (r?.previo) {
          avisar(`En ${dondeTexto()} hay una declaración con ${decididas(r.previo)} líneas decididas que este navegador no tiene. Pulse “💾 Guardar” para cargarla. No se escribe encima.`, false)
          return
        }
        avisar(`Se guarda sola en ${dondeTexto()}.`)
        api.cambio()
      } else {
        avisar(`Para seguir guardando en ${dondeTexto()}, pulse “💾 Guardar” (el navegador pide permiso una vez por sesión).`, false)
      }
    },

    /** Lo pulsó ella. Devuelve:
     *   true            guardado en la carpeta
     *   { previo, cuando }  hay en la carpeta algo que esta página no tiene: preguntarle
     *   'cancelado'     no eligió carpeta
     *   { error }       eligió una carpeta que no es la del proyecto
     *   false           no se pudo (usar la descarga) */
    async guardar({ forzar = false } = {}) {
      if (!puede) return false
      if (ocupado) return true
      ocupado = true
      try {
        if (!carpeta || !(await comprobar(true))) {
          // Cancelar el selector no es lo mismo que elegir una carpeta que no sirve:
          // a ella se le dice lo que pasó de verdad.
          const e = await elegir()
          if (e !== true) return e && e.error ? { error: e.error } : 'cancelado'
        }
        const r = await revisar(forzar)
        if (r?.previo) return r
        const texto = JSON.stringify(documento(), null, 1)
        await escribir(vigente, texto)
        await escribir(await libre(`voces declaradas - ${limpio(titulo)} - ${sello()}`), texto)
        ultimo = new Date()
        avisar(`Guardado en ${dondeTexto()} a las ${hora(ultimo)}, con una copia fechada.`, true, true)
        return true
      } catch (e) {
        avisar('No se pudo guardar en la carpeta: ' + (e?.message || e) + '. Use la descarga.', false)
        return false
      } finally { ocupado = false }
    },

    /** Tras cada cambio: la declaración vigente, sin preguntar nada, si ya hay permiso. */
    cambio() {
      if (permiso !== 'si' || !revisada) return
      clearTimeout(reloj)
      reloj = setTimeout(async () => {
        try {
          await escribir(vigente, JSON.stringify(documento(), null, 1))
          ultimo = new Date()
          avisar(`Guardado solo en ${dondeTexto()} a las ${hora(ultimo)}.`, true, true)
        } catch {
          permiso = 'pedir'
          avisar('Se perdió el permiso para guardar en la carpeta: pulse “💾 Guardar”.', false)
        }
      }, 1500)
    },
  }
  return api
}
