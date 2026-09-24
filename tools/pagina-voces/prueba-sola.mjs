// La pagina en su sitio (src/sola.js) y el guardado en la carpeta (src/carpeta.js),
// probados sin navegador: `node prueba-sola.mjs`. Sale con codigo 1 si algo falla.
//
// Lo que fija:
//   - abierta desde DENTRO de un .zip se reconoce en Windows (Explorador 10 y 11,
//     7-Zip, WinRAR), y una carpeta ya extraida, en Windows o en el Mac, no;
//   - el aviso dice los pasos del sistema que tiene ella (el Mac no tiene
//     «Extraer todo…»: basta doble clic);
//   - la pagina sabe cual es su proyecto con rutas de Windows y del Mac, y con
//     tildes compuestas o descompuestas (NFC / NFD);
//   - escribir encima de la carpeta solo cuando no se pierde nada de lo que habia.
import { abiertaDesdeZip, avisoDeSitio, sistema, navegador } from './src/sola.js'
import { dondeVoces, bajarVoces, cubre, decididas, nombreVigente } from './src/carpeta.js'

let fallos = 0, total = 0
const ok = (cond, que) => { total++; if (!cond) { fallos++; console.error('FALLA  ' + que) } }

// --- abierta desde un .zip ---------------------------------------------------
const U = (p) => 'file:///' + p.split('/').map(encodeURIComponent).join('/').replace(/^C%3A/, 'C:')
ok(abiertaDesdeZip(U('C:/Users/Ana/AppData/Local/Temp/04f40aef-5329-453d-b246-e84f939186aa_Reunion B.zip.6aa/Reunion B - mayo/INICIO - Reunion B.html')),
  'Explorador de Windows 11 (<guid>_<nombre>.zip.<ext>)')
ok(abiertaDesdeZip(U('C:/Users/Ana/AppData/Local/Temp/Temp1_Reunion B.zip/Reunion B - mayo/2-Borradores/Voces/Voces - X.html')),
  'Explorador de Windows 10 (Temp1_<nombre>.zip)')
ok(abiertaDesdeZip(U('C:/Users/Ana/AppData/Local/Temp/7zO8A1B2C3D/Voces - X.html')), '7-Zip')
ok(abiertaDesdeZip(U('C:/Users/Ana/AppData/Local/Temp/Rar$DIa1234.5678/Voces - X.html')), 'WinRAR')
ok(!abiertaDesdeZip(U('C:/Users/Ana/Desktop/Reunion B/Reunion B - mayo/INICIO - Reunion B.html')), 'extraida en el Escritorio de Windows: no es zip')
ok(!abiertaDesdeZip('file:///Users/ana/Downloads/Reunion%20B/Reunion%20B%20-%20mayo/INICIO%20-%20Reunion%20B.html'), 'extraida en el Mac: no es zip')
ok(!abiertaDesdeZip('https://ejemplo.org/a.zip/b.html'), 'una direccion web nunca cuenta como zip')
ok(!abiertaDesdeZip('no es una url'), 'una direccion rota no revienta')

// --- el sistema y los pasos ----------------------------------------------------
const MAC_SAFARI = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15'
const MAC_CHROME = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
const WIN_EDGE = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
ok(sistema(MAC_SAFARI, 'MacIntel') === 'mac', 'Mac con Safari')
ok(sistema(MAC_CHROME, 'MacIntel') === 'mac', 'Mac con Chrome')
ok(sistema(WIN_EDGE, 'Win32') === 'windows', 'Windows con Edge')
ok(navegador(MAC_SAFARI) === 'Safari', 'Safari se nombra Safari (su agente no dice Chrome)')
ok(navegador(MAC_CHROME) === 'Chrome', 'Chrome se nombra Chrome aunque su agente diga Safari')
ok(navegador(WIN_EDGE) === 'Edge', 'Edge se nombra Edge aunque su agente diga Chrome')

const zipMac = avisoDeSitio({ zip: true, so: 'mac' })
const zipWin = avisoDeSitio({ zip: true, so: 'windows' })
ok(zipMac.grave && /doble clic/.test(zipMac.texto) && !/Extraer todo/.test(zipMac.texto), 'en el Mac: doble clic, sin «Extraer todo»')
ok(zipWin.grave && /Extraer todo/.test(zipWin.texto), 'en Windows: «Extraer todo…»')
const todas = avisoDeSitio({ faltan: ['a.mp4', 'b.mp4', 'c.mp4'], total: 3, so: 'mac' })
ok(todas.grave && /ninguna de las 3/.test(todas.titulo), 'sin ninguna grabacion: aviso grave')
const una = avisoDeSitio({ faltan: ['Grabación de prueba 2.m4a'], total: 3 })
ok(!una.grave && /“Grabación de prueba 2\.m4a”/.test(una.titulo), 'falta una: la nombra, y no es grave')
ok(avisoDeSitio({ faltan: [], total: 3 }) === null, 'todo en su sitio: ningun aviso')
for (const a of [zipMac, zipWin, todas, una]) ok(!/[«»]/.test(a.titulo + a.texto), '« » son solo para lo literal: ' + a.titulo)

// --- el proyecto de la pagina -------------------------------------------------
const win = dondeVoces(U('C:/Users/Ana/Desktop/Reunion B/Reunion B - mayo/2-Borradores/Voces/Voces - Reunion B - 2026-09-24.html'))
ok(win.modo === 'proyecto' && win.proyecto === 'Reunion B - mayo', 'Windows: el proyecto es la carpeta de encima de 2-Borradores')
ok(win.camino.join('/') === 'C:/Users/Ana/Desktop/Reunion B/Reunion B - mayo', 'Windows: el camino llega al proyecto')
const mac = dondeVoces('file:///Users/ana/Downloads/Reunion%20B/Reunion%20B%20-%20mayo/2-Borradores/Voces/Voces%20-%20Reunion%20B.html')
ok(mac.modo === 'proyecto' && mac.proyecto === 'Reunion B - mayo' && mac.camino[0] === 'Users', 'Mac: /Users/…')
const suelta = dondeVoces(U('C:/Users/Ana/Desktop/Voces - X.html'))
ok(suelta.modo === 'libre', 'fuera de un proyecto: modo libre')

// --- bajar desde la carpeta elegida ---------------------------------------------
function carpeta(nombre, hijos = {}) {
  return {
    kind: 'directory', name: nombre,
    async getDirectoryHandle(n) { if (!hijos[n] || hijos[n].kind !== 'directory') throw new Error('no existe ' + n); return hijos[n] },
  }
}
const NFD = 'Asociacio\u0301n'   // la «ó» descompuesta, como la deja a veces el Mac
const voces = carpeta('Voces')
const proy = carpeta('Reunion B - mayo', { '2-Borradores': carpeta('2-Borradores', { Voces: voces }) })
const desc = carpeta('Downloads', { 'Reunion B': carpeta('Reunion B', { 'Reunion B - mayo': proy }) })
let r = await bajarVoces(desc, mac)
ok(r.dir === voces && r.ruta.join(' › ') === 'Reunion B - mayo › 2-Borradores › Voces', 'desde Descargas baja sola hasta Voces')
r = await bajarVoces(proy, mac)
ok(r.dir === voces, 'eligiendo el proyecto, llega a Voces')
r = await bajarVoces(voces, mac)
ok(r.error && /PROYECTO/.test(r.error), 'eligiendo Voces se le pide el proyecto')
r = await bajarVoces(carpeta('Otra'), mac)
ok(r.error && /no está en el camino/.test(r.error), 'una carpeta ajena se rechaza')
const conTilde = dondeVoces('file:///Users/m/' + encodeURIComponent('Asociación') + '/P/2-Borradores/Voces/V.html')
const pNFD = carpeta('P', { '2-Borradores': carpeta('2-Borradores', { Voces: voces }) })
r = await bajarVoces(carpeta(NFD, { P: pNFD }), conTilde)
ok(r.dir === voces, 'la misma carpeta con la tilde compuesta en la direccion y descompuesta en el disco')
const rota = carpeta('Reunion B - mayo', {})
r = await bajarVoces(carpeta('Reunion B', { 'Reunion B - mayo': rota }), mac)
ok(r.error && /no parece el proyecto/.test(r.error), 'un proyecto sin 2-Borradores › Voces se rechaza')

// --- no perder nada al escribir encima ------------------------------------------
const antes = { declarado_por: 'Ana Ruiz', lineas: { l1: { decision: 'confirmada' }, l2: {} }, voces: { v1: { nombre: 'Ana' } } }
ok(cubre({ declarado_por: 'Ana Ruiz', lineas: { l1: {}, l2: {}, l3: {} }, voces: { v1: { nombre: 'Ana' } } }, antes), 'lo tiene todo y mas: se escribe sin apartar')
ok(!cubre({ declarado_por: 'Ana Ruiz', lineas: { l1: {} }, voces: { v1: { nombre: 'Ana' } } }, antes), 'le falta una linea: se aparta antes')
ok(!cubre({ declarado_por: 'Ana Ruiz', lineas: { l1: {}, l2: {} }, voces: {} }, antes), 'le falta un nombre: se aparta antes')
ok(!cubre({ declarado_por: 'Otra', lineas: { l1: {}, l2: {} }, voces: { v1: { nombre: 'Ana' } } }, antes), 'otra persona declara: se aparta antes')
ok(cubre({ lineas: {} }, null), 'sin nada antes: se escribe')
ok(decididas(antes) === 2 && decididas(null) === 0, 'cuenta las lineas decididas')
ok(nombreVigente('Reunion: B/mayo') === 'voces declaradas - Reunion Bmayo.json', 'el nombre no lleva caracteres prohibidos en Windows')

console.log(`${total - fallos} de ${total} comprobaciones bien`)
process.exit(fallos ? 1 : 0)
