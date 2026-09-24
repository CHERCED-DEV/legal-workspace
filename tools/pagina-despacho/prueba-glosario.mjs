// Pruebas del glosario (src/glosario.js): lo que no necesita navegador.
//   node prueba-glosario.mjs
import { apariciones, plano, preparar, idSug, momento, normalizar, fusionar, exceptuada } from './src/glosario.js'
let fallos = 0, n = 0
const ok = (c, m) => { n++; if (!c) { fallos++; console.log('FALLA:', m) } }
const J = JSON.stringify

// El buscador
ok(J(apariciones('empresas públicas de Riohacha', 'Riohacha')) === '[[21,29]]', 'palabra entera')
ok(apariciones('Riohachero', 'Riohacha').length === 0, 'no dentro de otra palabra')
ok(apariciones('en Popayán', 'Popayan').length === 0, 'distingue tildes: Popayán bien escrito no se marca')
ok(apariciones('en Popayan y POPAYAN', 'popayan').length === 2, 'no distingue mayúsculas')
ok(apariciones('gracias señor secretario por', 'señor secretario').length === 1, 'frases')
ok(apariciones('arreglar', 'regla').length === 0, 'arreglar no es regla')
ok(apariciones('algo', '  ').length === 0, 'vacío no marca nada')
ok(plano('ÁBC') === 'ábc', 'plano solo baja a minúsculas')

// Una línea en NFD o con «İ» ya no se queda sin marcar entera, y las
// posiciones son las del texto original.
const nfd = 'en Popayán y Riohacha'.normalize('NFD')
ok(J(apariciones(nfd, 'Riohacha')) === '[[14,22]]', 'NFD: posiciones del original')
ok(nfd.slice(...apariciones(nfd, 'Riohacha')[0]) === 'Riohacha', 'NFD: el trozo es la palabra')
ok(J(apariciones(nfd, 'Popayán')) === '[[3,11]]', 'NFD: «Popayán» escrito en NFC la encuentra en NFD')
ok(apariciones(nfd, 'Popayan').length === 0, 'NFD: sigue distinguiendo tildes')
const conI = 'İstmina y Riohacha'
ok(conI.slice(...apariciones(conI, 'Riohacha')[0]) === 'Riohacha', '«İ» no descuadra el resto de la línea')
ok(apariciones('Popayán'.normalize('NFD'), 'Popaya').length === 0, 'no corta una letra de su tilde')
for (const s of [nfd, conI, 'á́b', '́x', 'emoji 🙂 y Riohacha']) {
  const p = preparar(s)
  ok(p.t.length === p.ini.length && p.ini.length === p.fin.length, 'preparar: una posición por carácter')
  ok(p.fin.at(-1) === s.length, 'preparar: cubre el texto entero: ' + J(s))
}

// Las sugerencias, por su contenido
ok(idSug('Riohacha', 'Río Hacha') === idSug(' RIOHACHA ', 'Río Hacha'), 'idSug: da igual mayúsculas y espacios en lo oído')
ok(idSug('Riohacha', 'Río Hacha') !== idSug('Riohacha', 'Rioacha'), 'idSug: lo que se dijo cuenta')

// Fechas
ok(momento({ cuando: '2026-09-23T15:00:00.000Z' }) === Date.parse('2026-09-23T15:00:00.000Z'), 'momento: cuando')
ok(momento({ fecha: '23/09/2026' }) === Date.UTC(2026, 8, 23), 'momento: fecha dd/mm/aaaa de las antiguas')
ok(momento({}) === 0 && momento(null) === 0, 'momento: sin fecha, 0')

// Lo guardado por versiones anteriores
const viejo = [
  { id: 'u1', de: 's0', oye: 'Popayan', dijo: 'Popayán', nota: 'Hipótesis de la máquina.', origen: 'sugerencia aceptada por usted', estado: 'aceptada', excepciones: ['b0', 'b3'] },
  { id: 'u2', oye: 'regla', dijo: 'arreglar', nota: 'lo oí', origen: 'usted', estado: 'aceptada', excepciones: [{ pagina: 'P1', linea: 'b2', fecha: '23/09/2026' }] },
  { id: 'u3', de: 's1', oye: 'Riohacha', dijo: 'Río Hacha', origen: 'sugerencia', estado: 'rechazada' },
  { id: 'u4', oye: '', dijo: 'x' }, null,
]
const { lista, quitadas } = normalizar(viejo)
ok(lista.length === 3, 'normalizar: descarta entradas vacías')
ok(quitadas === 2, 'normalizar: cuenta las excepciones antiguas quitadas')
ok(J(lista[0].excepciones) === '[]', 'normalizar: una excepción sin página ni oído no vale')
ok(lista[0].de === idSug('Popayan', 'Popayán'), 'normalizar: la decisión antigua pasa a ir por contenido')
ok(lista[0].nota === '' && lista[0].nota_maquina === 'Hipótesis de la máquina.', 'normalizar: la nota de la máquina deja de ser de ella')
ok(lista[1].nota === 'lo oí' && !('nota_maquina' in lista[1]), 'normalizar: la nota de ella se queda')
ok(lista[1].excepciones.length === 1, 'normalizar: la excepción con página se queda')
ok(lista[2].de === idSug('Riohacha', 'Río Hacha') && !('excepciones' in lista[2]), 'normalizar: la rechazada, por contenido')
ok(J(normalizar(lista).lista) === J(lista) && normalizar(lista).quitadas === 0, 'normalizar: pasar dos veces no cambia nada')
ok(viejo[0].de === 's0', 'normalizar: no toca lo que recibe')

// Excepciones por página y línea
ok(exceptuada(lista[1], 'P1', 'b2'), 'exceptuada: en su página y su línea')
ok(!exceptuada(lista[1], 'P2', 'b2'), 'exceptuada: la misma línea de OTRA grabación no')
ok(!exceptuada(lista[1], 'P1', 'b3'), 'exceptuada: otra línea no')

// Cargar un archivo: se junta, no se sustituye
const T = (d) => `2026-09-${String(d).padStart(2, '0')}T12:00:00.000Z`
const aqui = [
  { id: 'a', oye: 'Popayan', dijo: 'Popayán', estado: 'aceptada', cuando: T(20) },
  { id: 'b', oye: 'regla', dijo: 'arreglar', estado: 'aceptada', cuando: T(22) },
]
const archivo = [
  { id: 'c', oye: 'Riohacha', dijo: 'Río Hacha', estado: 'aceptada', cuando: T(10) },
  { id: 'd', oye: 'REGLA', dijo: 'reglar', estado: 'aceptada', cuando: T(21) },
]
let f = fusionar(aqui, archivo)
ok(J(f.map((x) => x.id)) === '["a","b","c"]', 'fusionar: lo de otras grabaciones se queda y la más reciente gana: ' + J(f.map((x) => x.id)))
f = fusionar(aqui, [{ ...archivo[1], cuando: T(23) }])
ok(J(f.map((x) => x.id)) === '["a","d"]', 'fusionar: la del archivo, si es más reciente')
f = fusionar([{ id: 'x', oye: 'Popayan', dijo: 'A', estado: 'aceptada', fecha: '20/09/2026' }],
  [{ id: 'y', oye: 'popayan', dijo: 'B', estado: 'aceptada', fecha: '20/09/2026' }])
ok(J(f.map((x) => x.id)) === '["y"]', 'fusionar: a igual fecha, la del archivo')
const s = idSug('Riohacha', 'Río Hacha')
f = fusionar([{ id: 'p', de: s, oye: 'Riohacha', dijo: 'Río Hacha', estado: 'aceptada', cuando: T(5) }],
  [{ id: 'q', de: s, oye: 'Riohacha', dijo: 'Río Hacha', estado: 'rechazada', cuando: T(6) }])
ok(J(f.map((x) => x.id)) === '["q"]', 'fusionar: una sola decisión por sugerencia, la última')
f = fusionar([{ id: 'r', oye: 'Riohacha', dijo: 'Riohacha la vieja', estado: 'aceptada', cuando: T(5) }],
  [{ id: 'q', de: s, oye: 'Riohacha', dijo: 'Río Hacha', estado: 'rechazada', cuando: T(6) }])
ok(f.length === 2, 'fusionar: rechazar una sugerencia no choca con una regla suya de lo mismo')
f = fusionar([{ id: 'a', oye: 'Popayan', dijo: 'Popayán', estado: 'aceptada', cuando: T(9), excepciones: [{ pagina: 'P', linea: 'b1' }] }],
  [{ id: 'a', oye: 'Popayan', dijo: 'Popayán', estado: 'aceptada', cuando: T(8), excepciones: [] }])
ok(f.length === 1 && f[0].excepciones.length === 1, 'fusionar: la misma entrada, la versión más reciente')

console.log(fallos ? fallos + ' de ' + n + ' FALLAN' : n + ' comprobaciones, todas bien')
process.exit(fallos ? 1 : 0)
