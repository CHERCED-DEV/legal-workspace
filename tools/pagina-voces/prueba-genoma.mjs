// El motor de la pagina de voces (src/genoma.js), probado con datos INVENTADOS.
// Sin dependencias: `node prueba-genoma.mjs`. Sale con codigo 1 si algo falla.
//
// Lo que fija es lo mismo que fija test_genoma_de_voz.py del lado de Python,
// porque la pagina y `aplicar` tienen que contar IGUAL:
//   - una propuesta nunca es una declaracion;
//   - la maquina solo suma a la claridad si paso la prueba (8 revisiones de
//     banda alta, 90 % de acierto), y las lineas de «conocer» no cuentan;
//   - una linea corta o que se pisa nunca es de banda alta, ni entra en una huella.
import * as G from './src/genoma.js'

let fallos = 0, total = 0
const ok = (cond, que) => { total++; if (!cond) { fallos++; console.error('FALLA  ' + que) } }

const DIM = 64
function azar(semilla) {
  let h = semilla >>> 0
  return () => { h ^= h << 13; h ^= h >>> 17; h ^= h << 5; return ((h >>> 0) / 4294967296) * 2 - 1 }
}
function dir(semilla) { const r = azar(semilla); return Array.from({ length: DIM }, () => r()) }
function unit(v) { const n = Math.hypot(...v) || 1; return v.map((x) => x / n) }
function b64(v) {
  const m = Math.max(...v.map(Math.abs)) || 1
  const b = Uint8Array.from(v.map((x) => (Math.round((x / m) * 127) + 256) % 256))
  return Buffer.from(b).toString('base64')
}
const D = { v1: unit(dir(11)), v2: unit(dir(22)), v3: unit(dir(33)) }
function ruido(v, k, s = 0.02) { const r = azar(1000 + k); return unit(v.map((x) => x + s * r())) }

function datos() {
  const lineas = []
  for (let i = 0; i < 30; i++) {
    const voz = ['v1', 'v2', 'v3'][i % 3]
    lineas.push({ id: 'A1-' + i, audio: 'A1', i, ini: 5 * i, fin: 5 * i + 4, texto: 'frase inventada ' + i,
      vec: b64(ruido(D[voz], i)), voz, pisa: 0, corta: false, dudas: [] })
  }
  return {
    formato: 'despacho/genoma-de-voz', version: 1, clave: 'abcdefabcdefabcd', titulo: 'Reunion inventada',
    calibracion: { bandas: { alta: 0.05, media: 0.02 }, cambio: 0.6, precision_minima: 0.9,
      revisiones_minimas: 8, fiable_s: 1.5, pisa_max: 0.3, corta_s: 1 },
    meta_claridad: 0.85,
    audios: [{ id: 'A1', nombre: 'Audio 1', ruta: 'a1.wav', archivo: 'a1.wav', duracion: 150 }],
    voces: ['v1', 'v2', 'v3'].map((v, k) => ({ id: v, etiqueta: 'Voz ' + (k + 1), vec: b64(D[v]), tipicas: ['A1-' + k] })),
    lineas, huecos: [], personas_conocidas: [],
  }
}
const vacio = () => ({ voces: {}, lineas: {}, saltadas: [] })
const ciclo = (M, E) => { const c = G.centroides(M, E); const p = G.proponer(M, E, c); return { c, p, cl: G.claridad(M, E, p) } }

// 1. La propuesta inicial acierta las tres voces sinteticas.
{
  const M = G.montar(datos()), E = vacio()
  const { p } = ciclo(M, E)
  ok(M.lineas.every((l) => p.get(l.id).voz === l.voz), 'la propuesta inicial no reconoce voces bien separadas')
}

// 2. Sin prueba de la maquina, la claridad es solo lo declarado.
{
  const M = G.montar(datos()), E = vacio()
  const { p, cl } = ciclo(M, E)
  ok(cl.global.claridad === 0, 'sin declarar nada la claridad no es 0: la maquina suma sin haber sido puesta a prueba')
  for (let i = 0; i < 3; i++) {
    const l = M.lineas[i], q = p.get(l.id)
    E.lineas[l.id] = { decision: 'confirmada', voz: q.voz, propuesta_maquina: q.voz, banda_maquina: q.banda, origen: 'aclarar' }
  }
  const r = ciclo(M, E)
  ok(Math.abs(r.cl.global.claridad - 3 / 30) < 1e-9, 'con 3 declaradas y la maquina sin probar, la claridad no es 3/30')
}

// 3. «Conocer las voces» no cuenta en el acierto.
{
  const M = G.montar(datos()), E = vacio()
  const { p } = ciclo(M, E)
  for (let i = 0; i < 10; i++) {
    const l = M.lineas[i], q = p.get(l.id)
    E.lineas[l.id] = { decision: 'confirmada', voz: q.voz, propuesta_maquina: q.voz, banda_maquina: 'alta', origen: 'conocer' }
  }
  ok(G.acierto(E).n === 0, 'las lineas de «conocer» cuentan en el acierto')
  ok(!G.maquinaCuenta(E, M.cal), 'la maquina cuenta sin una sola prueba al azar')
}

// 4. 8 de 8 cuenta; 8 de 9 (88 %) no; 9 de 10 (90 %) si; 7 de 7 no.
{
  const M = G.montar(datos())
  const conRevisiones = (n, aciertos) => {
    const E = vacio()
    for (let i = 0; i < n; i++) {
      E.lineas['A1-' + i] = { decision: i < aciertos ? 'confirmada' : 'corregida', voz: i < aciertos ? 'v1' : 'v2',
        propuesta_maquina: 'v1', banda_maquina: 'alta', origen: 'prueba' }
    }
    return E
  }
  ok(G.maquinaCuenta(conRevisiones(8, 8), M.cal), '8 de 8 no basta')
  ok(!G.maquinaCuenta(conRevisiones(9, 8), M.cal), '8 de 9 (88 %) cuenta')
  ok(G.maquinaCuenta(conRevisiones(10, 9), M.cal), '9 de 10 (90 %) no cuenta')
  ok(!G.maquinaCuenta(conRevisiones(7, 7), M.cal), '7 revisiones bastan')
}

// 5. Una linea corta o que se pisa nunca es alta, y no entra en ninguna huella.
{
  const d = datos()
  d.lineas[4].corta = true
  d.lineas[5].pisa = 0.6
  d.lineas[5].vec = b64(D.v3)         // es de v3 pero la declaramos v1: si entrara, arrastraria la huella
  const M = G.montar(d), E = vacio()
  const { p } = ciclo(M, E)
  ok(p.get('A1-4').banda === 'baja' && p.get('A1-5').banda === 'baja', 'una linea corta o que se pisa sale en banda alta')
  E.lineas['A1-5'] = { decision: 'corregida', voz: 'v1' }
  E.lineas['A1-0'] = { decision: 'confirmada', voz: 'v1' }
  const c = G.centroides(M, E)
  ok(c.cuentas.v1 === 1, 'una linea que se pisa entro en la huella de una voz')
}

// 6. Fusiones: las lineas de la voz fundida van a la otra, y un circulo no cuelga.
{
  const M = G.montar(datos()), E = vacio()
  E.voces.v3 = { fusionada_en: 'v1' }
  const { p } = ciclo(M, E)
  ok([...p.values()].every((x) => x.voz !== 'v3'), 'una propuesta apunta a la voz fundida')
  ok(G.vocesVivas(M, E).length === 2, 'la voz fundida sigue viva')
  E.voces.v1 = { fusionada_en: 'v3' }        // circulo v1 -> v3 -> v1
  ok(typeof G.resolver('v1', E.voces) === 'string', 'resolver cuelga con una fusion circular')
}

// 7. El genoma aprende de lo que ella declara. La huella INICIAL de la Voz 3
//    viene mal (apunta a la de la Voz 2): la maquina no puede acertar sus
//    lineas. Con dos declaraciones de ella, todas deben pasar a la Voz 3.
{
  const d = datos()
  d.voces[2].vec = b64(D.v2)
  const M = G.montar(d), E = vacio()
  const antes = ciclo(M, E).p
  const deV3 = M.lineas.filter((l) => l.voz === 'v3')
  E.lineas[deV3[0].id] = { decision: 'corregida', voz: 'v3' }
  E.lineas[deV3[1].id] = { decision: 'corregida', voz: 'v3' }
  const despues = ciclo(M, E).p
  ok(deV3.slice(2).every((l) => despues.get(l.id).voz === 'v3'), 'dos declaraciones no le enseñaron la Voz 3 al genoma')
  ok(G.cambiadas(antes, despues, E).length > 0, 'aprender una voz no movio ninguna propuesta')
}

// 8. La cola: primero conocer, luego probar al azar, luego aclarar.
{
  const M = G.montar(datos()), E = vacio()
  const { p } = ciclo(M, E)
  const s = G.siguiente(M, E, p)
  ok(s && s.paso === 1 && s.motivo === 'conocer', 'la cola no empieza por conocer las voces')
}

// 9. Una propuesta nunca figura como declarada.
{
  const M = G.montar(datos()), E = vacio()
  const { cl } = ciclo(M, E)
  ok(cl.global.ella === 0, 'la claridad atribuye a ella lo que propuso la maquina')
}

// 10. Los rescates no cuentan en la claridad ni en el acierto, y van antes en la cola.
{
  const d = datos()
  d.rescates = [{ id: 'A1-r0', audio: 'A1', ini: 4.2, fin: 4.9, texto: 'algo rescatado de verdad largo',
    vec: b64(D.v2), voz: 'v2', pisa: 0, corta: true, dudas: [], lecturas: [], acuerdo: 0.9, oyen: 3 }]
  const M = G.montar(d), E = vacio()
  const antes = ciclo(M, E).cl.global.total
  ok(Math.abs(antes - 30 * 4) < 1e-9, 'un rescate cuenta en los segundos de la claridad')
  E.lineas['A1-r0'] = { decision: 'corregida', voz: 'v1', propuesta_maquina: 'v2', banda_maquina: 'alta', rescate: true, se_dijo: true }
  ok(G.acierto(E).n === 0, 'una decision sobre un rescate cuenta en el acierto de la maquina')
  const E2 = vacio()
  for (let i = 0; i < 12; i++) E2.lineas['A1-' + i] = { decision: 'confirmada', voz: M.lineas[i].voz, propuesta_maquina: M.lineas[i].voz, banda_maquina: 'alta', origen: 'prueba' }
  const p2 = ciclo(M, E2).p
  const s = G.siguiente(M, E2, p2)
  ok(s && s.linea.id === 'A1-r0' && s.motivo === 'rescate', 'lo rescatado no va primero en «lo que mas aclara»')
}

// 11. Revision del 2026-09-23: lo que se decide SIN OIR no es una declaracion
//     oyendo; la prueba de la maquina solo sale de lineas SORTEADAS y oidas;
//     «varios» sin dos voces no aclara nada; y donde ella dijo que no se
//     distingue, la maquina no puede aclararlo por su cuenta.
{
  const M = G.montar(datos())
  const prueba = (n, extra) => {
    const E = vacio()
    for (let i = 0; i < n; i++) E.lineas['A1-' + i] = { decision: 'confirmada', voz: M.lineas[i].voz, propuesta_maquina: M.lineas[i].voz, banda_maquina: 'alta', ...extra }
    return E
  }
  ok(!G.maquinaCuenta(prueba(10, { origen: 'prueba', oida: false }), M.cal), 'diez Enter sin oir aprueban a la maquina')
  ok(!G.maquinaCuenta(prueba(10, { origen: 'lista', oida: true }), M.cal), 'lineas elegidas a mano aprueban a la maquina')
  ok(G.maquinaCuenta(prueba(10, { origen: 'prueba', oida: true }), M.cal), 'diez sorteadas y oidas no aprueban a la maquina')

  const E = vacio()
  E.lineas['A1-0'] = { decision: 'confirmada', voz: 'v1', oida: false }
  E.lineas['A1-1'] = { decision: 'varios', voces: ['v2'], oida: true }
  E.lineas['A1-2'] = { decision: 'varios', voces: ['v1', 'v2'], oida: true }
  E.lineas['A1-3'] = { decision: 'confirmada', voz: 'v1', oida: true }
  const { cl } = ciclo(M, E)
  ok(Math.abs(cl.global.ella - 8) < 1e-9, 'la claridad cuenta lo decidido sin oir o «varios» de una sola voz (esperaba 2 lineas de 4 s)')
  ok(G.centroides(M, E).cuentas.v1 === 1, 'una linea decidida sin oir entro en la huella')

  const E2 = prueba(10, { origen: 'prueba', oida: true })
  E2.lineas['A1-20'] = { decision: 'no_se_distingue', oida: true }
  const r2 = ciclo(M, E2)
  ok(Math.abs(r2.cl.global.total - r2.cl.global.ella - r2.cl.global.maquina - 4) < 1e-9,
     'la maquina «aclaro» una linea que ella marco como no se distingue')
}

console.log(`${total - fallos} de ${total} comprobaciones del motor de la pagina de voces`)
process.exit(fallos ? 1 : 0)
