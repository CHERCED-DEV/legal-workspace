// Pruebas de las otras lecturas de una línea (src/lecturas.js), sin navegador.
//   node prueba-lecturas.mjs
import { alinear, discordias, conCambio, normal } from './src/lecturas.js'
let fallos = 0, n = 0
const ok = (c, m) => { n++; if (!c) { fallos++; console.log('FALLA:', m) } }
const tramo = (a) => a && a.tramo.map((x) => x.w).join(' ')
const difieren = (a) => a && a.tramo.filter((x) => !x.igual).map((x) => x.w).join(' ')

const linea = 'Los centros de la regla.'
let a = alinear(linea, 'Los centros de arreglo. Esas cosas son para poder intervenir y seguir con el tema.', 0)
ok(tramo(a) === 'Los centros de arreglo.', 'corta en el final de frase: ' + tramo(a))
ok(difieren(a) === 'arreglo.', 'solo difiere lo distinto: ' + difieren(a))
ok(a.despues.length === 11 && a.antes.length === 0, 'lo de alrededor queda como contexto')

a = alinear(linea, 'Los centros de la regla. Amén.', 0)
ok(a.igual, 'igual cuando dice lo mismo, aunque la lectura siga')
ok(tramo(a) === 'Los centros de la regla.', 'la parte igual: ' + tramo(a))

a = alinear('Amén.', 'Esas cosas son para poder intervenir. Amén.', 0.9)
ok(tramo(a) === 'Amén.' && a.antes.length === 6, 'una palabra al final del tramo: ' + tramo(a))

ok(alinear(linea, 'Nada que ver con esto otro aquí.', 0) === null, 'sin parecido no inventa correspondencia')
ok(alinear(linea, 'El, los empleados, los empleados de coja. Amén.', 0) === null, 'dos palabras sueltas en común no bastan')
ok(alinear('', 'algo', 0) === null && alinear(linea, '', 0) === null, 'vacíos')

a = alinear('bueno vamos con el tema', 'y bueno bueno vamos con el tema de hoy', 0)
ok(tramo(a) && tramo(a).includes('vamos con el tema'), 'palabras repetidas: ' + tramo(a))

// Con dos apariciones, gana la que está a la altura de la línea.
a = alinear('el plazo', 'el plazo es corto. Luego se dijo que el plazo', 0.95)
ok(a && a.antes.length >= 5, 'la posición desempata: ' + (a && a.antes.join(' ')))

const ds = discordias(linea, [
  { fuente: 'canal derecho', texto: 'Los centros de arreglos. Esas cosas son', pos: 0 },
  { fuente: 'sin limpiar', texto: 'Los centros de arreglo. Gracias.', pos: 0 },
  { fuente: 'mezcla', texto: 'Los centros de la regla. Amén.', pos: 0 },
])
ok(ds.length === 1, 'una discordia: ' + JSON.stringify(ds))
ok(ds[0]?.dice === 'la regla', 'lo que dice la transcripción: ' + ds[0]?.dice)
ok(JSON.stringify(ds[0]?.lecturas.map((x) => x.lee)) === '["arreglos","arreglo"]', 'lo que leen las otras: ' + JSON.stringify(ds[0]?.lecturas))
ok(!ds[0]?.lecturas.some((x) => x.fuente === 'mezcla'), 'la que coincide no sale')

ok(conCambio(linea, [3, 5], 'arreglo') === 'Los centros de arreglo.', 'la línea con el cambio: ' + conCambio(linea, [3, 5], 'arreglo'))
ok(conCambio('dijo que sí, luego', [2, 3], '') === 'dijo que, luego', 'quitar una palabra: ' + conCambio('dijo que sí, luego', [2, 3], ''))
ok(normal('Árbol.') === 'arbol', 'normal')
console.log(fallos ? fallos + ' de ' + n + ' FALLAN' : n + ' comprobaciones, todas bien')
process.exit(fallos ? 1 : 0)
