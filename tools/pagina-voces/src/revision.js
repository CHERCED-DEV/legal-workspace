/* La tarjeta de revision: una linea, oirla, y decir quien habla.
 *
 * Todo lo que hace falta para decidir esta en la tarjeta: el texto, las
 * lineas de alrededor con su voz, oir la linea (o con contexto, o mas lenta),
 * lo que propone la maquina y con que seguridad, y la huella de la linea al
 * lado de la de la voz propuesta. Cada decision tiene su tecla.
 *
 * Revision del 2026-09-23: una linea contaba como «oida» en cuanto empezaba a
 * sonar, y con el auto-avance sonaban todas. Ahora cuenta cuando se oyo al
 * menos el 70 % de ella, y la tarjeta dice cuanto se oyo.
 */
import { el, hms, pct, chipVoz, dibujarAdn, lienzo, duracion } from './util.js'
import { adnDeVoz, resolver, DECLARADAS, OIDA_MINIMA } from './genoma.js'

const PASOS = {
  1: ['Conocer las voces', 'Estas son las líneas más típicas de cada voz. Óigala y diga quién habla: así la página aprende cómo suena cada persona.'],
  2: ['Poner a prueba a la máquina', 'Líneas sorteadas entre las que la máquina da por seguras. Óigalas enteras y diga quién habla: solo así se mide cuánto acierta, y sus propuestas solo cuentan si acierta el 90 %.'],
  3: ['Lo que más aclara', 'Las líneas donde la máquina duda más, primero las más largas. Cada una que usted decide oyendo mejora la huella de esa voz.'],
  R: ['Lo que la transcripción no tenía', 'Tramos donde la transcripción no trae nada y, al volver a oírlos pista por pista, algo se oye. Nada de esto entra en su entrega si usted no lo oye y dice que se dijo.'],
}

/** La voz con la que se pinta una linea, y si lo que se pinta es de ella. */
export function chipDeLinea(app, x, opciones = {}) {
  const E = app.estado.todo
  const dx = E.lineas[x.id]
  if (dx?.decision === 'descartado' || dx?.decision === 'no_se_dijo')
    return el('span', { class: 'chip chip-nadie', text: '✗ descartado' })
  if (dx?.decision === 'no_se_distingue')
    return el('span', { class: 'chip chip-nadie', text: '? no se distingue' })
  if (dx?.decision === 'varios')
    return el('span', { class: 'chip chip-declarada chip-varios', text: (dx.voces || []).length >= 2 ? '✔ varios a la vez' : '? varios, sin distinguir' })
  if (dx?.partes)
    return el('span', { class: 'chip chip-declarada chip-varios', text: '✔ dividida en dos' })
  if (dx && DECLARADAS.has(dx.decision))
    return chipVoz(app.cat[resolver(dx.voz, E.voces)], { declarada: true, ...opciones })
  const p = app.props.get(x.id)
  return chipVoz(app.cat[p?.voz], { banda: p?.banda, ...opciones })
}

function textoPrueba(app) {
  const { n, ok } = app.acierto
  const req = app.modelo.cal.revisiones_minimas
  if (n < req) return ` — ${n} de ${req} revisadas`
  if (app.clar.cuenta) return ` — superada: acertó ${ok} de ${n}`
  return ` — ${n} revisadas, acertó ${ok}: aún no llega al ${pct(app.modelo.cal.precision_minima)}`
}

function frasePropuesta(app, p) {
  if (!p?.voz) return ''
  const cat = app.cat
  const a = cat[p.voz]?.rotulo || '—', b = cat[p.segunda]?.rotulo || '—'
  const dif = p.parecido - p.parecido2
  const cuanto = dif >= app.modelo.cal.bandas.alta ? 'con diferencia clara'
    : dif >= app.modelo.cal.bandas.media ? 'por poco' : 'casi empatadas: puede ser cualquiera de las dos'
  // Parecidos en decimales, NO en %: «87 %» se lee como probabilidad y se
  // confunde con la meta del 85 %.
  const n = (x) => x.toFixed(2).replace('.', ',')
  let estado
  const { n: rev } = app.acierto
  if (rev < app.modelo.cal.revisiones_minimas) estado = ' La máquina aún no se ha puesto a prueba: esto es solo lo que ella cree.'
  else if (!app.clar.cuenta) estado = ' La máquina no superó la prueba: tómelo con cuidado.'
  else estado = ''
  return `Se parece más a ${a} (${n(p.parecido)}) que a ${b} (${n(p.parecido2)}): ${cuanto}.${estado}`
}

export function renderRevision(app, caja) {
  caja.replaceChildren()
  const f = app.foco
  if (!f) {
    caja.append(el('div', { class: 'vacio' },
      el('h2', { text: 'No queda nada por revisar' }),
      el('p', { text: 'Todas las líneas tienen una decisión suya o una propuesta que ya cuenta como clara. Puede repasar cualquiera en «Todas las líneas», o guardar su declaración.' })))
    return
  }
  const l = f.linea
  const E = app.estado.todo
  const d = E.lineas[l.id]
  const p = app.props.get(l.id)
  const cat = app.cat
  const au = app.modelo.datos.audios.find((a) => a.id === l.audio)
  const estadoAudio = app.sonido.estado(l.audio)
  const sinAudio = estadoAudio === 'falta' || estadoAudio === 'otra'
  const R = l.rescate

  // --- el paso
  if (f.paso) {
    const [t, expl] = PASOS[f.motivo === 'rescate' ? 'R' : f.paso]
    caja.append(el('div', { class: 'paso' },
      el('span', { class: 'paso-n', text: `Paso ${f.paso} de 3` }),
      el('strong', { text: t + (f.paso === 2 ? textoPrueba(app) : '') }),
      el('span', { class: 'paso-expl', text: expl })))
  } else {
    caja.append(el('div', { class: 'paso paso-libre' },
      el('strong', { text: 'Línea abierta por usted' }),
      el('span', { class: 'paso-expl', text: 'Lo que decida aquí cuenta como declaración, pero no como prueba de la máquina: esa sale solo de las líneas sorteadas.' }),
      el('button', { class: 'btn enlace', text: 'Volver a lo que tocaba revisar', onclick: () => app.volverACola() })))
  }

  // --- donde esta
  const insignias = []
  if (R)
    insignias.push(el('span', { class: 'insignia insignia-rescate', title: 'Este tramo no está en la transcripción: se volvió a oír pista por pista', text: 'Rescatado: no estaba en la transcripción' }))
  if (l.invencion)
    insignias.push(el('span', { class: 'insignia insignia-pisa', title: 'Frases que el reconocedor suele escribir sobre ruido o silencio', text: 'Puede ser invención del reconocedor' }))
  if (l.bucle)
    insignias.push(el('span', { class: 'insignia insignia-pisa', title: 'Una lectura repite la misma palabra una y otra vez', text: 'El reconocedor se repite' }))
  if (l.pisa >= app.modelo.cal.pisa_max)
    insignias.push(el('span', { class: 'insignia insignia-pisa', title: 'La separación de voces oye a dos o más personas a la vez en esta línea', text: `Se pisan (${pct(l.pisa)} de la línea)` }))
  if (l.corta)
    insignias.push(el('span', { class: 'insignia', title: 'Menos de un segundo de voz: la huella es poco fiable', text: 'Muy corta' }))
  if (l.cambio)
    insignias.push(el('span', { class: 'insignia insignia-cambio', title: 'La huella de la primera parte y la de la segunda no se parecen', text: 'La voz puede cambiar a mitad' }))
  if (l.dudas?.length)
    insignias.push(el('span', { class: 'insignia insignia-texto', title: l.dudas.join(' · '), text: 'El texto también es dudoso' }))

  caja.append(el('div', { class: 'donde' },
    el('span', { class: 'donde-audio', text: au?.nombre || l.audio }),
    el('span', { class: 'donde-min', text: `${hms(l.ini)} → ${hms(l.fin)}` }),
    el('span', { class: 'donde-dur', text: duracion(l.dur) }),
    ...insignias))

  // --- el texto, con las lineas de alrededor
  const vecina = (x, rot) => {
    if (!x) return null
    return el('div', { class: 'vecina', onclick: () => app.abrir(x, 'contexto'), title: 'Abrir esta línea' },
      el('span', { class: 'vecina-rot', text: rot }),
      el('span', { class: 'vecina-min', text: hms(x.ini) }),
      chipDeLinea(app, x),
      el('span', { class: 'vecina-txt' + (x.rescate ? ' fila-rescate' : ''), text: E.lineas[x.id]?.texto || x.texto }))
  }
  if (R) {
    const guardado = E.borradores?.[l.id] ?? d?.texto ?? l.texto
    const area = el('textarea', { class: 'texto-rescate', rows: 3, 'aria-label': 'Lo que se dijo' })
    area.value = guardado
    area.addEventListener('input', () => app.textoRescate(l, area.value))
    const ac = l.acuerdo
    const unaSola = (l.lecturas || []).filter((x) => x.texto).length < 2 || (l.lecturas || []).length < 2
    caja.append(el('div', { class: 'texto-bloque' },
      vecina(l.prev, 'antes'),
      el('div', { class: 'rescate-acuerdo' + (!unaSola && ac >= 0.6 ? ' ok' : '') },
        unaSola ? 'Solo una lectura oyó algo aquí: no hay con qué compararla. Óigalo antes de aceptar nada.'
          : ac >= 0.6 ? `Las lecturas se parecen bastante (${pct(ac)}). Ojo: son tres lecturas de la misma grabación, no tres testigos — también se parecen cuando el reconocedor inventa lo mismo sobre el mismo ruido.`
            : ac >= 0.3 ? `Las lecturas se parecen poco (${pct(ac)}): óigalo antes de aceptar nada.`
              : `Las lecturas no se parecen (${pct(ac || 0)}): puede ser habla cruzada, ruido o algo que el reconocedor inventó.`),
      el('div', { class: 'lecturas' }, ...(l.lecturas || []).map((x) => el('div', { class: 'alt' },
        el('span', { class: 'alt-f', text: x.fuente }),
        el('span', { class: x.texto ? '' : 'nada', text: x.texto ? `«${x.texto}»` : '(no oyó nada)' })))),
      el('label', { class: 'rescate-label' }, 'Lo que se dijo — corríjalo oyendo. Se guarda mientras escribe:', area),
      vecina(l.next, 'después')))
  } else caja.append(el('div', { class: 'texto-bloque' },
    vecina(l.prev, 'antes'),
    el('blockquote', { class: 'texto-linea' + (l.dudas?.length ? ' texto-dudoso' : '') }, `«${l.texto}»`),
    l.dudas?.length ? el('div', { class: 'texto-dudas', text: '[?] ' + l.dudas.join(' · ') }) : null,
    // Si las lecturas no coinciden, se ven SIN abrir nada: ahi estaba «la
    // ministra», con su aviso y dentro de un desplegable.
    l.alternativas?.length ? el('details', { class: 'alternativas', open: (l.dudas || []).some((x) => /no coinciden/.test(x)) },
      el('summary', { text: 'Qué escribió cada lectura automática' }),
      ...l.alternativas.map((a) => el('div', { class: 'alt' }, el('span', { class: 'alt-f', text: a.fuente }), el('span', { text: a.texto })))) : null,
    vecina(l.next, 'después')))

  // --- oir
  const oido = app.oido(l)
  const vel = app.sonido.velocidad
  caja.append(el('div', { class: 'oir' },
    el('button', { class: 'btn primario btn-oir', disabled: sinAudio, onclick: () => app.oir(l), type: 'button' },
      '▶ Oír la línea ', el('kbd', { text: 'Espacio' })),
    el('button', { class: 'btn', disabled: sinAudio, onclick: () => app.oir(l, { antes: 3 }), type: 'button' },
      '⟲ Con 3 s antes ', el('kbd', { text: 'A' })),
    el('span', { class: 'velocidades' }, 'Velocidad:',
      ...[0.75, 1, 1.25, 1.5].map((x) => el('button', {
        class: 'btn mini' + (x === vel ? ' activo' : ''), type: 'button',
        onclick: () => app.velocidad(x), text: String(x).replace('.', ',') + '×' }))),
    el('label', { class: 'auto-oir', title: 'Al pasar a la línea siguiente, empieza a sonar sola' },
      el('input', { type: 'checkbox', checked: app.estado.todo.autoOir !== false, onchange: (e) => app.fijarAutoOir(e.target.checked) }),
      ' que suene sola la siguiente'),
    el('span', { class: 'oida ' + (oido >= OIDA_MINIMA ? 'si' : 'no'),
      text: oido >= 0.97 ? '✔ La oyó entera' : oido >= OIDA_MINIMA ? `✔ Oyó el ${pct(oido)}` : oido > 0 ? `Oyó solo el ${pct(oido)}` : 'Aún no la ha oído' })))
  if (sinAudio) {
    const inp = el('input', { type: 'file', accept: 'audio/*,video/*', onchange: (e) => app.sonido.usarArchivo(l.audio, e.target.files[0]) })
    caja.append(el('div', { class: 'falta-audio' },
      el('strong', { text: estadoAudio === 'otra'
        ? `Ese archivo no es «${au?.archivo || l.audio}»: dura distinto. No se usa.`
        : `No puedo reproducir «${au?.archivo || l.audio}»: o no está junto a esta página, o este navegador no lee ese formato.` }),
      el('span', { text: ' Sin oírla, lo que decida no es una declaración oyendo. Búsquela en su equipo (no sale de él): ' }),
      inp))
  }

  // --- lo que ya decidio, y lo que propone la maquina
  const pv = p?.voz ? cat[p.voz] : null
  if (d) {
    caja.append(el('div', { class: 'ya-decidida' },
      el('strong', { text: 'Usted ya decidió esta línea: ' }),
      describirDecision(d, cat, E),
      d.oida === false ? el('span', { class: 'insignia insignia-pisa', text: 'sin oírla' }) : null,
      el('span', { class: 'nota', text: 'Enter no la cambia. Para cambiarla, elija otra opción o ' }),
      el('button', { class: 'btn enlace', text: 'quite su decisión', onclick: () => app.estado.olvidar(l.id) })))
  }
  const seg = { alta: 'alta', media: 'media', baja: 'baja' }[p?.banda] || 'baja'
  const barras = { alta: 3, media: 2, baja: 1 }[seg]
  const prop = el('div', { class: 'propuesta banda-' + seg },
    el('div', { class: 'prop-cab' },
      el('span', { text: 'La máquina propone:' }),
      chipVoz(pv, { banda: seg }),
      el('span', { class: 'seguridad', title: 'Cuánto más se parece a esta voz que a la siguiente' },
        'Seguridad ', el('span', { class: 'barras' }, ...[1, 2, 3].map((k) => el('i', { class: k <= barras ? 'on' : '' }))),
        ` ${seg}`),
      pv && !pv.nombre ? el('button', { class: 'btn enlace', type: 'button', text: `¿Quién es ${pv.etiqueta}? Nómbrela`, onclick: () => app.modalNombrar(pv.id) }) : null),
    el('div', { class: 'prop-expl', text: frasePropuesta(app, p) }))
  const cl = lienzo(220, 34, 'adn'), cv = lienzo(220, 34, 'adn')
  dibujarAdn(cl, l.a, '#333')
  dibujarAdn(cv, pv ? adnDeVoz(app.modelo, E, app.props, pv.id) : null, pv?.color)
  prop.append(el('div', { class: 'huellas' },
    el('figure', {}, cl, el('figcaption', { text: 'Huella de esta línea' })),
    el('figure', {}, cv, el('figcaption', { text: `Huella de ${pv?.rotulo || '—'}` }))))
  caja.append(prop)

  // --- decidir
  if (app.dividiendo === l.id && l.cambio && l.partes) { caja.append(panelDividir(app, l)); return }
  if (app.varios === l.id) { caja.append(panelVarios(app, l)); return }

  const vivasOrden = app.vivas.slice().sort((a, b) => (cat[a].tecla || 'z').localeCompare(cat[b].tecla || 'z'))
  const otras = vivasOrden.filter((v) => v !== p?.voz)
  const exigeOir = R && oido < OIDA_MINIMA
  caja.append(el('div', { class: 'decidir' },
    el('div', { class: 'decidir-t', text: R ? '¿Se dijo esto? ¿Quién lo dice?' : '¿Quién habla aquí?' }),
    exigeOir ? el('div', { class: 'aviso-oir fuerte', text: 'Un tramo rescatado solo se acepta después de oírlo: nadie lo ha oído todavía.' }) : null,
    pv ? el('button', { class: 'btn si', type: 'button', disabled: !!d || exigeOir, onclick: () => app.confirmar(l) },
      R ? '✔ Sí, se dijo, y es ' : '✔ Sí, es ', el('span', { class: 'punto', style: { background: pv.color } }), ` ${pv.largo} `, el('kbd', { text: 'Enter' })) : null,
    el('div', { class: 'no-es' },
      el('span', { class: 'no-es-t', text: R ? 'Se dijo, y es:' : pv ? 'No, es:' : 'Es:' }),
      ...otras.map((v) => chipVoz(cat[v], { opcion: true, tecla: true, titulo: `Declarar que habla ${cat[v].largo}`, onclick: () => app.corregir(l, v) })),
      el('button', { class: 'btn', type: 'button', disabled: exigeOir, onclick: () => app.nuevaPersona(l) }, '+ Otra persona ', el('kbd', { text: 'N' }))),
    el('div', { class: 'otras-acciones' },
      R ? el('button', { class: 'btn', type: 'button', disabled: exigeOir, onclick: () => app.noSeDistingue(l) }, '? Se dijo, pero no distingo quién ', el('kbd', { text: 'X' })) : null,
      R ? el('button', { class: 'btn no-dijo', type: 'button', onclick: () => app.descartar(l) }, '✗ Descartar: no se entiende, o no se dijo ', el('kbd', { text: 'Supr' })) : null,
      l.cambio && l.partes ? el('button', { class: 'btn', type: 'button', onclick: () => { app.dividiendo = l.id; app.render() } },
        `✂ La voz cambia en «${(l.partes[1] || '').split(' ')[0]}» — dividir `, el('kbd', { text: 'D' })) : null,
      R ? null : el('button', { class: 'btn', type: 'button', onclick: () => { app.varios = l.id; app.render() } }, 'Hablan varios a la vez ', el('kbd', { text: 'V' })),
      R ? null : el('button', { class: 'btn', type: 'button', onclick: () => app.noSeDistingue(l) }, '? No se distingue ', el('kbd', { text: 'X' })),
      el('button', { class: 'btn', type: 'button', onclick: () => app.saltar(l) }, 'Saltar ', el('kbd', { text: '→' })),
      el('button', { class: 'btn', type: 'button', disabled: !app.historial.length, onclick: () => app.atras() }, '← Anterior'),
      el('button', { class: 'btn', type: 'button', disabled: !app.estado.puedeDeshacer, onclick: () => app.deshacer() }, '↶ Deshacer ', el('kbd', { text: 'Z' }))),
    !R && oido < OIDA_MINIMA && !sinAudio ? el('div', { class: 'aviso-oir', text: 'Óigala antes de decidir: lo que decida sin oírla queda anotado como «sin oír» y no cuenta para la claridad.' }) : null))
}

export function describirDecision(d, cat, E) {
  const r = (v) => cat[resolver(v, E.voces)]?.largo || v
  switch (d.decision) {
    case 'confirmada': return `✔ ${r(d.voz)} (confirmó la propuesta)`
    case 'corregida': return d.partes ? `✔ dividida: ${d.partes.map((p) => r(p.voz)).join(' / ')}` : `✔ ${r(d.voz)} (corrigió a la máquina)`
    case 'varios': return (d.voces || []).length >= 2 ? `✔ varios a la vez: ${d.voces.map(r).join(', ')}` : '? varios a la vez, sin distinguir quiénes'
    case 'no_se_distingue': return d.rescate ? '? se dijo, pero no se distingue quién' : '? no se distingue quién habla'
    case 'descartado': case 'no_se_dijo': return '✗ descartado: no se entiende, o no se dijo'
    default: return d.decision
  }
}

function panelDividir(app, l) {
  const cat = app.cat
  const sel = app.partes || (app.partes = [null, null])
  const fila = (k) => el('div', { class: 'parte' },
    el('button', { class: 'btn mini', type: 'button', onclick: () => app.oir(l, k === 0 ? { hasta: l.cambio.en } : { desde: l.cambio.en }) }, '▶'),
    el('span', { class: 'parte-t', text: `«${l.partes[k]}»` }),
    el('div', { class: 'parte-voces' },
      ...app.vivas.map((v) => chipVoz(cat[v], { opcion: true, elegida: sel[k] === v, onclick: () => { sel[k] = v; app.render() } }))))
  return el('div', { class: 'dividir' },
    el('div', { class: 'decidir-t', text: 'Diga quién dice cada parte' }),
    fila(0), fila(1),
    el('div', { class: 'otras-acciones' },
      el('button', { class: 'btn si', type: 'button', disabled: !(sel[0] && sel[1]), onclick: () => app.dividir(l, sel) }, 'Listo'),
      el('button', { class: 'btn', type: 'button', onclick: () => { app.dividiendo = null; app.partes = null; app.render() } }, 'Cancelar')))
}

function panelVarios(app, l) {
  const cat = app.cat
  const sel = app.selVarios || (app.selVarios = new Set())
  return el('div', { class: 'dividir' },
    el('div', { class: 'decidir-t', text: '¿Quiénes hablan a la vez?' }),
    el('div', { class: 'nota', text: 'Marque al menos dos para que cuente como línea clara. Si no sabe quiénes, déjelo vacío: queda como «no se distingue».' }),
    el('div', { class: 'parte-voces' },
      ...app.vivas.map((v) => chipVoz(cat[v], { opcion: true, elegida: sel.has(v), onclick: () => { sel.has(v) ? sel.delete(v) : sel.add(v); app.render() } }))),
    el('div', { class: 'otras-acciones' },
      el('button', { class: 'btn si', type: 'button', onclick: () => app.declararVarios(l, [...sel]) }, 'Listo'),
      el('button', { class: 'btn', type: 'button', onclick: () => { app.varios = null; app.selVarios = null; app.render() } }, 'Cancelar')))
}
