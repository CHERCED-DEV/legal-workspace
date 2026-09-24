// Pruebas de lo que cuenta la página de «quién habla». Sin navegador: solo las
// cuentas de src/atribucion.js, que son las que no pueden mentir.
//
//   node prueba-atribucion.mjs
import { fragmentar, resumir, siguiente, quedan, efectiva, cuenta, estadoDe, firma, coincide, valida,
         unir, cubierto, fraccionOida, META, OIDA_MINIMA, FRAGMENTO_MAX_S, HUECO_S, pct, plural } from './src/atribucion.js'

let fallos = 0, n = 0
const ok = (c, msg) => { n++; if (!c) { fallos++; console.log('FALLA:', msg) } }

const b = (id, ini, fin, voz) => ({ id, ancla: { tipo: 'tiempo', inicio: ini, fin }, etiqueta: voz == null ? null : `Hablante ${voz}` })
const vozDe = (x) => { const m = /Hablante (\S+)/.exec(x.etiqueta || ''); return m ? m[1] : null }
// Una decisión como la guarda la página: con la firma del fragmento que se oyó.
const dec = (f, decision, extra = {}) => ({ decision, oido: 1, firma: firma(f), ...(decision === 'si' ? { voz: f.maquina } : {}), ...extra })

// 1. Fragmentos: por voz, por largo y por silencio; con sus zonas de habla.
{
  const bl = [b('a', 0, 5, 1), b('b', 5, 10, 1), b('c', 10, 14, 2), b('d', 14, 20, 1),
              b('e', 20, 40, 1), b('f', 40, 50, 1), b('g', 70, 75, 1), b('h', 75, 80, null)]
  const fr = fragmentar(bl, vozDe)
  ok(fr.map((f) => f.id).join() === 'a,c,d,f,g,h', 'cortes: ' + fr.map((f) => f.id).join())
  ok(fr[0].dur === 10 && fr[0].bloques.join() === 'a,b', 'el primero junta a y b')
  ok(JSON.stringify(fr[0].zonas) === '[[0,5],[5,10]]', 'lleva sus zonas de habla')
  ok(fr.every((f) => f.fin - f.inicio <= FRAGMENTO_MAX_S || f.bloques.length === 1), 'ninguno pasa de 30 s salvo una línea sola')
  ok(fr.find((f) => f.id === 'g').inicio - fr.find((f) => f.id === 'f').fin > HUECO_S, 'el silencio largo parte')
  ok(fr.find((f) => f.id === 'h').maquina === null, 'sin voz es su propio fragmento')
}

// 2. Lo oído: una sola vez, y sobre el habla.
{
  let l = []
  l = unir(l, 0, 10.5); l = unir(l, 0, 10.5)
  ok(Math.abs(fraccionOida(l, [[0, 29]]) - 10.5 / 29) < 1e-9, 'oír dos veces el mismo trozo no suma')
  l = unir(l, 10, 20)
  ok(l.length === 1 && l[0][1] === 20, 'lo que se toca se funde')
  const zonas = [[0, 5], [15, 20]]   // habla con 10 s de silencio en medio
  ok(fraccionOida([[0, 10]], zonas) === 0.5, 'se mide sobre el habla, no sobre el silencio')
  ok(cubierto([[4, 16]], zonas) === 2, 'cubierto cuenta solo lo que cae en el habla')
  ok(fraccionOida([[0, 1]], [[3, 3]]) === 0, 'una zona sin largo no se puede oír')
}

// 3. Solo cuenta lo oído, bien formado y del fragmento que es.
{
  const [f] = fragmentar([b('a', 0, 10, 1)], vozDe)
  ok(!cuenta(null, f), 'sin decisión no cuenta')
  ok(cuenta(dec(f, 'si', { oido: OIDA_MINIMA }), f), 'sí oído al 70 % cuenta')
  ok(!cuenta(dec(f, 'si', { oido: OIDA_MINIMA - 0.01 }), f), 'sí sin oír no cuenta')
  ok(!cuenta({ ...dec(f, 'si'), oido: '0.9' }, f), 'oído que no es número no cuenta')
  ok(!cuenta({ ...dec(f, 'si'), oido: true }, f), 'oído true no cuenta')
  ok(!valida({ decision: 'quizas', oido: 1 }), 'una decisión desconocida no es válida')
  ok(cuenta(dec(f, 'otra', { voz: '2' }), f), 'otra con voz cuenta')
  ok(!cuenta(dec(f, 'otra'), f), 'otra sin decir cuál no cuenta')
  ok(!cuenta(dec(f, 'no_se'), f) && !cuenta(dec(f, 'varios'), f), 'no sé y varios no cuentan')
  const [g] = fragmentar([b('a', 0, 12, 1)], vozDe)   // la misma línea, otra versión
  ok(!coincide(dec(f, 'si'), g) && !cuenta(dec(f, 'si'), g), 'una decisión de otra versión no cuenta')
  const [h] = fragmentar([b('a', 0, 10, 2)], vozDe)   // la misma línea, otra voz de la máquina
  ok(!cuenta(dec(f, 'si'), h), 'si la máquina cambió la voz, el sí no pasa a la otra')
  ok(!cuenta({ decision: 'si', voz: '1', oido: 1 }, f), 'sin firma no cuenta')
}

// 4. Las cuentas por voz, en segundos; «no sé» cuenta en contra; «otra» mueve.
{
  const bl = [b('a', 0, 10, 1), b('b', 10, 14, 2), b('c', 14, 44, 1), b('d', 44, 50, 1)]
  const fr = fragmentar(bl, vozDe)  // a(10 s, v1) · b(4 s, v2) · c(30 s, v1) · d(6 s, v1)
  const F = Object.fromEntries(fr.map((f) => [f.id, f]))
  ok(fr.length === 4, 'cuatro fragmentos: ' + fr.map((f) => f.id).join())
  let r = resumir(fr, {})
  ok(r.porVoz.get('1').total === 46 && r.porVoz.get('1').pct === 0, 'sin decisiones: 0 %')
  r = resumir(fr, { a: dec(F.a, 'si'), c: dec(F.c, 'si', { oido: 0.9 }) })
  ok(Math.abs(r.porVoz.get('1').pct - 40 / 46) < 1e-9, 'por segundos, no por fragmentos')
  ok(r.porVoz.get('1').identificada === (40 / 46 >= META), 'identificada según la meta')
  r = resumir(fr, { a: dec(F.a, 'si'), c: dec(F.c, 'no_se'), d: dec(F.d, 'si') })
  ok(Math.abs(r.porVoz.get('1').pct - 16 / 46) < 1e-9, '«no sé» se queda en el total sin confirmar')
  ok(r.porVoz.get('1').dudas === 1, 'y se cuenta como duda')
  r = resumir(fr, { c: dec(F.c, 'otra', { voz: '2' }) })
  ok(r.porVoz.get('1').total === 16, 'lo movido sale de la voz de la máquina')
  ok(r.porVoz.get('2').total === 34 && r.porVoz.get('2').confirmado === 30, 'y entra confirmado en la otra')
  ok(r.total === 50, 'el total no cambia al mover')
  r = resumir(fr, { c: dec(F.c, 'si', { oido: 0.5 }) })
  ok(r.porVoz.get('1').confirmado === 0, 'sin oír no suma aunque diga sí')
  r = resumir(fr, { b: dec(F.b, 'otra', { voz: 'nueva-1' }) })
  ok(r.porVoz.get('nueva-1').anadida && !r.porVoz.get('nueva-1').identificada, 'una voz añadida no cuenta como identificada')
  ok(r.deMaquina === 1 && r.identificadas === 0, 'ni en la cuenta de voces identificadas')
  r = resumir(fr, { a: { ...dec(F.a, 'si'), firma: { ...firma(F.a), fin: 99 } } })
  ok(r.porVoz.get('1').confirmado === 0, 'lo de otra versión no suma')
}

// 5. Nunca se llega a la meta saltándose lo difícil.
{
  const bl = [b('a', 0, 20, 1), b('b', 20, 22, 2), b('c', 22, 42, 1), b('d', 42, 44, 2), b('e', 44, 60, 1)]
  const fr = fragmentar(bl, vozDe)
  const F = Object.fromEntries(fr.map((f) => [f.id, f]))
  const r = resumir(fr, { a: dec(F.a, 'si'), c: dec(F.c, 'no_se'), e: dec(F.e, 'varios') })
  ok(!r.porVoz.get('1').identificada, 'con «no sé» y «varios» no llega')
  ok(pct(0.8499) === '84 %', 'el porcentaje no redondea hacia la meta')
}

// 6. El siguiente: en orden, sin volver a lo saltado, y el repaso termina.
{
  const bl = [b('a', 0, 5, 1), b('x', 5, 6, 2), b('b', 6, 9, 1), b('y', 9, 10, 2), b('c', 10, 12, 1)]
  const fr = fragmentar(bl, vozDe)
  const F = Object.fromEntries(fr.map((f) => [f.id, f]))
  ok(siguiente(fr, {}, '1', null).id === 'a', 'empieza por el primero')
  ok(siguiente(fr, {}, '1', 'a').id === 'b', 'sigue en orden')
  ok(siguiente(fr, { a: dec(F.a, 'si') }, '1', 'c').id === 'b', 'da la vuelta y salta lo decidido')
  ok(siguiente(fr, {}, '1', 'a', { saltados: new Set(['b', 'c']) }) === null, 'lo saltado no vuelve: termina')
  const todo = { a: dec(F.a, 'si'), b: dec(F.b, 'no_se'), c: dec(F.c, 'no_se') }
  ok(siguiente(fr, todo, '1', 'c') === null, 'sin pendientes, el recorrido normal termina (no recicla los «no sé»)')
  ok(siguiente(fr, todo, '1', null, { modo: 'repaso' }).id === 'b', 'el repaso va a los «no sé»')
  ok(siguiente(fr, todo, '1', 'b', { modo: 'repaso', vistos: new Set(['b', 'c']) }) === null, 'y termina cuando los vio todos')
  ok(JSON.stringify(quedan(fr, todo, '1')) === '{"pendientes":0,"dudas":2}', 'cuenta lo que queda')
  ok(siguiente(fr, {}, '9', null) === null, 'una voz sin fragmentos no tiene siguiente')
  ok(siguiente(fragmentar([b('s', 0, 3, null)], vozDe), {}, null, null).id === 's', 'también lo que no tiene voz')
}

// 7. Estados para pintar.
{
  const [f] = fragmentar([b('a', 0, 10, 1)], vozDe)
  ok(estadoDe(f, null) === 'pendiente', 'pendiente')
  ok(estadoDe(f, dec(f, 'si')) === 'confirmado', 'confirmado')
  ok(estadoDe(f, dec(f, 'otra', { voz: '2' })) === 'movido', 'movido')
  ok(estadoDe(f, dec(f, 'si', { oido: 0.2 })) === 'no_se', 'sin oír no se pinta como confirmado')
  ok(estadoDe(f, dec(f, 'varios')) === 'varios', 'varios')
  ok(estadoDe(f, { decision: 'si', voz: '1', oido: 1 }) === 'otra_version', 'sin firma es de otra versión')
  ok(efectiva(f, dec(f, 'otra', { voz: '3' })) === '3', 'la voz efectiva es la de ella')
  ok(plural(1, 'fragmento', 'fragmentos') === '1 fragmento' && plural(2, 'voz', 'voces') === '2 voces', 'plurales')
}

console.log(fallos ? `${fallos} de ${n} FALLAN` : `${n} comprobaciones, todas bien`)
process.exit(fallos ? 1 : 0)
