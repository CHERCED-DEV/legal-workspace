// Pruebas de lo que deciden los paneles «lo que no se entiende» y «compromisos».
// Sin navegador: solo las funciones puras de src/ilegibles.js y
// src/compromisos.js, que son las que dicen qué se guarda y cuándo.
//
//   node prueba-paneles.mjs
import { puedeGuardar, contado, loDeclarado, esIdea, motivosDe, citar, accionDeTecla } from './src/ilegibles.js'
import { puedeCambiar, fundir } from './src/compromisos.js'
import { TECLAS_DE_LA_PAGINA } from './src/oido.js'
import { OIDA_MINIMA } from './src/atribucion.js'

let fallos = 0, n = 0
const ok = (c, msg) => { n++; if (!c) { fallos++; console.log('FALLA:', msg) } }
const casi = OIDA_MINIMA - 0.01

// 1. Lo que no se entiende: no se guarda sin oír, sin respuesta, ni con una idea que no es idea.
{
  ok(!puedeGuardar({ oida: casi, entiende: 'no' }), 'sin oír lo bastante no se guarda')
  ok(puedeGuardar({ oida: OIDA_MINIMA, entiende: 'no' }), 'oído justo lo bastante, «no se entiende» se guarda')
  ok(!puedeGuardar({ oida: 1, grabacion: false, entiende: 'no' }), 'sin la grabación no se guarda')
  ok(!puedeGuardar({ oida: 1 }), 'sin respuesta no se guarda')
  ok(!puedeGuardar({ oida: 1, entiende: 'quizas' }), 'una respuesta que no es de las cuatro no se guarda')
  ok(puedeGuardar({ oida: 1, entiende: 'sin_habla' }), '«no hay nadie hablando» no pide idea')
  ok(!puedeGuardar({ oida: 1, entiende: 'si', idea: '' }), '«sí» sin idea no se guarda')
  ok(!puedeGuardar({ oida: 1, entiende: 'en_parte', idea: '3' }), 'una idea «3» no es una idea')
  ok(!puedeGuardar({ oida: 1, entiende: 'si', idea: ' 3, 4. ' }), 'números y signos no son una idea')
  ok(!puedeGuardar({ oida: 1, entiende: 'si', idea: 'a' }), 'una letra sola no es una idea')
  ok(puedeGuardar({ oida: 1, entiende: 'si', idea: 'se habla del horario' }), 'una frase sí')
  ok(esIdea('él') && esIdea('ñu') && esIdea('3 veces'), 'cuenta las letras con tilde y eñe')
}

// 2. Contado: lo mismo sobre lo guardado.
{
  ok(!contado(null) && !contado({}), 'nada guardado no está contado')
  ok(!contado({ oido: casi, entiende: 'no' }), 'guardado sin oír lo bastante no cuenta')
  ok(!contado({ oido: 1, entiende: 'en_parte', idea: '3' }), 'la idea «3» de antes no cuenta')
  ok(contado({ oido: 1, entiende: 'si', idea: 'se habla del horario' }), 'con idea cuenta')
}

// 3. Lo que se guarda es lo que ella declaró, y nada más.
{
  const sinQuien = loDeclarado({ entiende: 'si', idea: '  se habla del horario ' })
  ok(!('quien' in sinQuien), 'si no eligió quién, no se guarda «no sabe quién»: ' + JSON.stringify(sinQuien))
  ok(sinQuien.idea === 'se habla del horario', 'la idea se guarda sin espacios de los lados')
  ok(loDeclarado({ entiende: 'si', idea: 'x y', quien: 'no_se' }).quien === 'no_se', '«no sé quién» se guarda si lo pulsó')
  ok(loDeclarado({ entiende: 'en_parte', idea: 'x y', quien: '2' }).quien === '2', 'la voz elegida se guarda')
  const no = loDeclarado({ entiende: 'no', idea: 'de antes', quien: '2', palabras: 'algo' })
  ok(JSON.stringify(no) === '{"entiende":"no"}', '«no se entiende» no arrastra idea, quién ni palabras: ' + JSON.stringify(no))
  ok(!('palabras' in loDeclarado({ entiende: 'si', idea: 'x y', palabras: '   ' })), 'palabras vacías no se guardan')
}

// 4. Las teclas con la pregunta abierta: las de la página nunca llegan a su atajo.
{
  const sueltas = [...TECLAS_DE_LA_PAGINA].filter((k) => accionDeTecla({ key: k }) === null)
  ok(!sueltas.length, 'sin escribir, estas teclas llegaban a la página: ' + sueltas.join(' '))
  ok(accionDeTecla({ key: 'c' }) === 'aviso', '«c» avisa en vez de confirmar la línea')
  ok(accionDeTecla({ key: 'c', escribiendo: true }) === null, 'escribiendo, «c» se escribe')
  ok(accionDeTecla({ key: '3', escribiendo: true, ideaVacia: true }) === 'respuesta', 'con la idea vacía, «3» cambia la respuesta')
  ok(accionDeTecla({ key: '3', escribiendo: true }) === null, 'con la idea empezada, «3» se escribe')
  ok(accionDeTecla({ key: '2' }) === 'respuesta', 'sin escribir, «2» es la respuesta')
  ok(accionDeTecla({ key: '5' }) === null, '«5» no es una respuesta')
  ok(accionDeTecla({ key: 'Enter', ctrl: true, escribiendo: true }) === 'guardar', 'Ctrl+Intro guarda aunque esté escribiendo')
  ok(accionDeTecla({ key: 'c', ctrl: true }) === null, 'Ctrl+C sigue copiando')
  ok(accionDeTecla({ key: 'Enter', enBoton: true }) === null && accionDeTecla({ key: ' ', enBoton: true }) === null,
    'Intro y Espacio sobre un botón los toma el botón')
  ok(accionDeTecla({ key: 'Enter' }) === 'aviso', 'Intro sin botón no hace sonar otra línea')
  ok(accionDeTecla({ key: 'Escape', escribiendo: true }) === 'dejar_de_escribir' && accionDeTecla({ key: 'Escape' }) === 'cerrar', 'Esc')
  ok(accionDeTecla({ key: 'ArrowDown' }) === 'desplazar', 'las flechas desplazan, no mueven la línea enfocada')
}

// 5. Por qué se pregunta, sin contradecirse, y la cita sin cortar a media palabra.
{
  const hueco = { motivos: ['hueco'], transcripcion: [] }
  ok(/no recoge nada aquí/.test(motivosDe(hueco)), 'un hueco sin texto: no recoge nada aquí')
  const conTexto = { motivos: ['discordia', 'hueco'], transcripcion: [{ texto: 'se oye lejos' }] }
  ok(!/no recoge nada aquí/.test(motivosDe(conTexto)) && /en parte/.test(motivosDe(conTexto)),
    'un hueco con texto no dice «no recoge nada aquí»: ' + motivosDe(conTexto))
  ok(citar('se oye lejos') === '«se oye lejos»', 'una cita corta va entera')
  const largo = Array.from({ length: 80 }, (_, i) => 'palabra' + i).join(' ')
  const c = citar(largo)
  const dentro = c.slice(1, c.indexOf('»'))
  ok(c.endsWith('» [sigue…]'), 'la cita larga cierra las comillas y dice fuera que sigue: ' + c.slice(-30))
  ok(largo.startsWith(dentro + ' '), 'lo citado es el principio exacto del texto, cortado en un espacio')
  ok(citar('a < b') === '«a &lt; b»', 'la cita va escapada')
}

// 6. Compromisos: no se cambia sin oír; «no lo es» no lleva quién ni plazo.
{
  ok(!puedeCambiar({ oida: casi }), 'sin oír lo bastante no se cambia')
  ok(puedeCambiar({ oida: OIDA_MINIMA }), 'oído lo bastante, sí')
  ok(!puedeCambiar({ oida: 1, grabacion: false }), 'sin la grabación, no')
  const antes = { es: 'si', quien: 'otra', quien_texto: 'nombre y cargo', plazo: 'el lunes', minuto: '00:00:05' }
  const despues = fundir(antes, { es: 'no' })
  ok(!('quien' in despues) && !('quien_texto' in despues) && !('plazo' in despues),
    '«no lo es» borra quién y plazo: ' + JSON.stringify(despues))
  ok(despues.minuto === '00:00:05' && antes.plazo === 'el lunes', 'lo demás se queda, y lo anterior no se toca')
  const otro = fundir(antes, { quien: '2', quien_texto: undefined })
  ok(otro.quien === '2' && !('quien_texto' in otro) && otro.plazo === 'el lunes', 'cambiar de quién quita el nombre escrito')
  ok(fundir({ es: 'no' }, { plazo: 'mañana' }).plazo === undefined, 'con «no lo es», un plazo no se guarda')
}

ok(!puedeCambiar({ oida: 1, grabacion: true, sinLocalizar: ['esto no se dijo'] }), 'con parte de la cita sin localizar no se declara')
ok(puedeCambiar({ oida: 1, grabacion: true, sinLocalizar: [] }), 'con la cita localizada y oída, sí')
console.log(fallos ? `${fallos} de ${n} FALLAN` : `${n} comprobaciones, todas bien`)
process.exit(fallos ? 1 : 0)
