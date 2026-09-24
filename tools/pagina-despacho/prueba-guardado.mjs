// Pruebas de DÓNDE guarda la página lo que ella declara (src/guardado.js).
//   node prueba-guardado.mjs
import { dondeGuardar, bajar, EN_PROYECTO, cuantoHay } from './src/guardado.js'
let fallos = 0, n = 0
const ok = (c, m) => { n++; if (!c) { fallos++; console.log('FALLA:', m) } }

const P = 'file:///C:/Users/x/Desktop/Despacho/Cliente%20A/Asunto%20B/3-Para%20presentar/ENTREGA%20-%20Asunto%20B%20-%202026-01-01/Transcripciones/Audio%201.html'
let d = dondeGuardar(P)
ok(d.modo === 'proyecto', 'en un proyecto: ' + d.modo)
ok(d.proyecto === 'Asunto B', 'el proyecto: ' + d.proyecto)
ok(d.entrega === 'ENTREGA - Asunto B - 2026-01-01', 'la entrega: ' + d.entrega)
ok(JSON.stringify(d.dentro) === JSON.stringify([...EN_PROYECTO, 'ENTREGA - Asunto B - 2026-01-01']), 'destino en el proyecto: ' + d.dentro)
ok(d.camino.at(-1) === 'Asunto B' && d.camino.includes('Despacho'), 'camino hasta el proyecto')

const N = 'file:///C:/Users/x/Desktop/Despacho/Cliente%20A/Asunto%20B/2-Borradores/Entregas/ENTREGA%20-%20Asunto%20B%20-%202026-02-02/Transcripciones/Audio%201.html'
d = dondeGuardar(N)
ok(d.modo === 'proyecto' && d.proyecto === 'Asunto B' && d.entrega === 'ENTREGA - Asunto B - 2026-02-02', 'forma nueva (2-Borradores/Entregas): ' + d.proyecto)
ok(d.camino.at(-1) === 'Asunto B', 'camino hasta el proyecto, forma nueva')

d = dondeGuardar('file:///C:/Users/x/Downloads/ENTREGA%20-%20algo/ENTREGA%20-%20algo/Transcripciones/Audio%201.html')
ok(d.modo === 'entrega' && d.camino.length === 6, 'entrega suelta, la carpeta de más adentro: ' + d.camino.join('/'))
ok(JSON.stringify(d.dentro) === '["Lo que declaré"]', 'dentro de la entrega')

ok(dondeGuardar('http://localhost:8765/Transcripciones/a.html').modo === 'libre', 'servida por http: libre')
ok(dondeGuardar('no es url').modo === 'libre', 'sin dirección: libre')

// Un disco de mentira: carpetas con nombre e hijos.
function carpeta(nombre, hijos = {}) {
  return {
    name: nombre, kind: 'directory', hijos,
    async getDirectoryHandle(n, o = {}) {
      if (!this.hijos[n]) { if (!o.create) throw new Error('NotFound'); this.hijos[n] = carpeta(n) }
      return this.hijos[n]
    },
  }
}
const disco = () => carpeta('Despacho', { 'Cliente A': carpeta('Cliente A', { 'Asunto B': carpeta('Asunto B', {
  '2-Borradores': carpeta('2-Borradores'),
  '3-Para presentar': carpeta('3-Para presentar', { 'ENTREGA - Asunto B - 2026-01-01': carpeta('ENTREGA - Asunto B - 2026-01-01') }),
}) }) })
d = dondeGuardar(P)
const raiz = disco()
let r = await bajar(raiz, d)
ok(!r.error && r.ruta.join('/') === 'Asunto B/2-Borradores/Lo que declaré/ENTREGA - Asunto B - 2026-01-01', 'desde Despacho baja al proyecto: ' + (r.error || r.ruta.join('/')))
ok(raiz.hijos['Cliente A'].hijos['Asunto B'].hijos['2-Borradores'], 'crea las carpetas en el proyecto')
const suelta = carpeta('Mi entrega')
r = await bajar(suelta, dondeGuardar('http://localhost/x.html'))
ok(!r.error && r.ruta.join('/') === 'Mi entrega/Lo que declaré' && suelta.hijos['Lo que declaré'], 'libre: también en «Lo que declaré»: ' + (r.error || r.ruta.join('/')))
r = await bajar(disco().hijos['Cliente A'].hijos['Asunto B'], d)
ok(!r.error && r.ruta[0] === 'Asunto B', 'eligiendo el proyecto')
r = await bajar(carpeta('ENTREGA - Asunto B - 2026-01-01'), d)
ok(r.error && r.error.includes('PROYECTO'), 'la entrega no vale en un proyecto: ' + r.error)
r = await bajar(carpeta('Documentos'), d)
ok(r.error && r.error.includes('no está en el camino'), 'otra carpeta cualquiera no vale')
r = await bajar(carpeta('Asunto B'), d)
ok(r.error && r.error.includes('2-Borradores'), 'un homónimo sin «2-Borradores» no vale: ' + r.error)
ok(cuantoHay({ estado: {}, glosario: [] }) === 0, 'un documento vacío no cuenta')
ok(cuantoHay({ estado: { b1: {} }, compromisos: { 'c-1-a': {} }, voces: { 1: 'Ana', 2: ' ' }, glosario: [{}] }) === 4, 'cuenta lo declarado')

// «En curso anterior»: se aparta lo que había en la carpeta ANTES de la sesión (otro
// navegador, otro equipo), una vez; nunca lo que esta página acaba de escribir. Antes se
// apartaba su propio guardado de un minuto antes (SPEC-16 §7.4, 2026-09-24).
function disco2(previo) {
  const archivos = new Map()
  function dir(nombre, hijos = {}) {
    return {
      name: nombre, kind: 'directory', hijos,
      async getDirectoryHandle(k, o = {}) {
        if (!this.hijos[k]) { if (!o.create) throw new Error('NotFound'); this.hijos[k] = dir(k) }
        return this.hijos[k]
      },
      async getFileHandle(k, o = {}) {
        const clave = nombre + '/' + k
        if (!archivos.has(clave)) { if (!o.create) throw new Error('NotFound'); archivos.set(clave, '') }
        return {
          async getFile() { return { text: async () => archivos.get(clave), lastModified: 0 } },
          async createWritable() { let b = ''; return { write: async (x) => { b += x }, close: async () => { archivos.set(clave, b) } } },
        }
      },
      async queryPermission() { return 'granted' }, async requestPermission() { return 'granted' },
    }
  }
  const raiz = dir('Asunto B', { '2-Borradores': dir('2-Borradores') })
  if (previo) archivos.set('ENTREGA - Asunto B - 2026-02-02/Audio 1 - en curso.json', previo)
  return { raiz, archivos, nombres: () => [...archivos.keys()].map((k) => k.split('/').pop()) }
}
globalThis.window = globalThis
globalThis.isSecureContext = true
globalThis.confirm = () => true
globalThis.alert = () => {}
const { crearGuardado } = await import('./src/guardado.js')
const dormir = (ms) => new Promise((r) => setTimeout(r, ms))
async function sesion(previo) {
  const D = disco2(previo)
  globalThis.showDirectoryPicker = async () => D.raiz
  let doc = { estado: { b1: { estado: 'confirmado' } } }
  const g = crearGuardado({ titulo: 'Audio 1', documento: () => doc, href: N })
  ok((await g.guardar()) === true, 'guarda en la carpeta del proyecto')
  doc = { estado: { b1: { estado: 'confirmado' }, b2: { estado: 'oido' } } }
  g.cambio()
  await dormir(2800)
  return D
}
let D = await sesion(null)
ok(!D.nombres().some((x) => x.includes('en curso anterior')), 'lo que la página acaba de guardar no se aparta: ' + D.nombres().join(' ; '))
ok(D.nombres().includes('Audio 1 - en curso.json'), 'el en curso existe')
D = await sesion(JSON.stringify({ estado: { b9: { estado: 'confirmado' } } }))
ok(D.nombres().filter((x) => x.includes('en curso anterior')).length === 1, 'lo de otra sesión se aparta, UNA vez: ' + D.nombres().join(' ; '))

console.log(fallos ? fallos + ' de ' + n + ' FALLAN' : n + ' comprobaciones, todas bien')
process.exit(fallos ? 1 : 0)
