/* La pagina del genoma de voz. SPEC-15.
 *
 * La maquina propone por parecido. Ella declara oyendo. Las dos cosas se ven
 * distintas en toda la pagina, y solo lo declarado cuenta como declaracion.
 */
import './estilo.css'
import { el, hms, pct, duracion, chipVoz, dibujarAdn, lienzo, catalogoVoces, descargar } from './util.js'
import {
  montar, centroides, proponer, claridad, siguiente, cambiadas, acierto,
  vocesVivas, parecidas, adnDeVoz, resolver, DECLARADAS, OIDA_MINIMA,
} from './genoma.js'
import { crearEstado } from './estado.js'
import { crearSonido } from './sonido.js'
import { renderRevision } from './revision.js'
import { renderLineas } from './lineas.js'
import { renderMapa } from './mapa.js'
import { renderFranjas } from './franjas.js'
import { renderSalida, declaracion, leerDeclaracion } from './salida.js'

const $ = (s) => document.querySelector(s)

function arrancar() {
  let datos
  try { datos = JSON.parse($('#datos').textContent) } catch { datos = null }
  if (!datos || datos.formato !== 'despacho/genoma-de-voz') {
    document.body.replaceChildren(el('div', { class: 'vacio' },
      el('h2', { text: 'Esta página no trae datos' }),
      el('p', { text: 'Se genera con genoma_de_voz.py preparar. No se edita a mano.' })))
    return
  }
  const modelo = montar(datos)
  const app = {
    modelo,
    oidas: new Set(),
    historial: [],
    pestana: 'revisar',
    foco: null,
    props: new Map(),
    propsPrevias: null,
  }
  app.estado = crearEstado(datos.clave, (info) => { recalcular(app); if (info?.externo) app.toast('Se actualizó desde otra pestaña'); render(app) })
  app.cober = {}
  app.sonido = crearSonido(datos.audios, {
    alEstado: (id, e) => {
      if (e === 'falta' || e === 'lista' || e === 'otra') render(app)
      if (e === 'otra') app.toast('Ese archivo no es la grabación de esta página: dura distinto. No se usa.')
      if (e === 'bloqueado') app.toast('El navegador no dejó reproducir: pulse «Oír» otra vez.')
    },
    // Cuanto de la linea se oyo DE VERDAD: desde que el audio entra en ella
    // hasta donde llega. Antes contaba como oida al empezar a sonar.
    alTiempo: (actual, t) => anotarOido(app, actual, t),
    alTerminar: (actual) => { anotarOido(app, actual, actual.fin); render(app) },
  })
  const v0 = app.estado.todo.velocidad || 1
  app.sonido.fijarVelocidad(v0)

  Object.assign(app, acciones(app))
  document.title = `Voces · ${datos.titulo}`
  $('#titulo').textContent = datos.titulo
  $('#generado').textContent = `Preparada el ${datos.generado} · ${datos.lineas.length} líneas · ${datos.audios.length} grabaciones`

  recalcular(app)
  app.foco = siguiente(modelo, app.estado.todo, app.props)
  montarPestanas(app)
  montarTeclado(app)
  window.addEventListener('resize', () => { clearTimeout(app._r); app._r = setTimeout(() => render(app), 150) })
  window.addEventListener('beforeunload', (e) => {
    if (app.estado.pendiente && !app.estado.almacenOK) { e.preventDefault(); e.returnValue = '' }
  })
  render(app)
  if (!app.estado.todo.declarado_por) app.modalBienvenida()
}

function anotarOido(app, actual, t) {
  const lid = actual?.marca?.lid
  if (!lid) return
  const l = app.modelo.porId.get(lid)
  if (!l || t < l.ini) return
  const c = app.cober[lid] ||= { lo: Math.max(l.ini, actual.ini), hi: Math.max(l.ini, actual.ini) }
  c.lo = Math.min(c.lo, Math.max(l.ini, actual.ini))
  c.hi = Math.max(c.hi, Math.min(t, l.fin))
}

function recalcular(app) {
  const E = app.estado.todo
  app.vivas = vocesVivas(app.modelo, E)
  app.cat = catalogoVoces(app.modelo, E, app.vivas)
  app.cent = centroides(app.modelo, E)
  app.propsPrevias = app.props
  app.props = proponer(app.modelo, E, app.cent)
  app.acierto = acierto(E)
  app.clar = claridad(app.modelo, E, app.props)
}

function acciones(app) {
  const E = () => app.estado.todo

  function avanzar(desde) {
    if (app.foco?.linea) app.historial.push(app.foco)
    if (app.historial.length > 300) app.historial.shift()
    const excl = new Set([desde?.id].filter(Boolean))
    app.foco = siguiente(app.modelo, E(), app.props, excl)
    app.dividiendo = null; app.partes = null; app.varios = null; app.selVarios = null
    if (app.foco?.linea && app.yaOyo && E().autoOir !== false
        && app.sonido.estado(app.foco.linea.audio) === 'lista') {
      setTimeout(() => app.oir(app.foco.linea), 150)
    }
  }

  function registrar(l, dec, origen) {
    if (!E().declarado_por) {
      app.modalDeclarante(() => registrar(l, dec, origen))
      return
    }
    const p = app.props.get(l.id)
    const esFoco = app.foco?.linea?.id === l.id
    const antes = app.props
    const oida = app.oido(l) >= OIDA_MINIMA
    if (l.rescate) {
      const texto = (E().borradores?.[l.id] ?? E().lineas[l.id]?.texto ?? l.texto).trim()
      const acepta = dec.decision !== 'descartado'
      // Un tramo que nadie tenia no entra sin que ella lo oiga, ni vacio.
      if (acepta && !oida) { app.toast('Óigalo entero antes de aceptarlo: nadie lo ha oído todavía.'); return }
      if (acepta && !texto) { app.toast('Escriba lo que se dijo, o descártelo.'); return }
      dec = { ...dec, rescate: true, se_dijo: acepta, texto }
    }
    // Si ya estaba decidida, lo que la maquina proponia AL PRINCIPIO se
    // conserva: la huella ya aprendio de la decision anterior, y la maquina
    // «acertaria» copiandola a ella.
    const previa = E().lineas[l.id]
    app.estado.decidir(l.id, {
      ...dec,
      propuesta_maquina: previa ? previa.propuesta_maquina : (p?.voz || null),
      banda_maquina: previa ? previa.banda_maquina : (p?.banda || null),
      origen: previa ? previa.origen : (origen || (esFoco ? app.foco.motivo : 'lista')),
      oida,
    })
    const cambian = cambiadas(antes, app.props, E())
    if (esFoco) avanzar(l)
    render(app)
    let msg = app.estado.almacenOK ? 'Guardado en este navegador.' : '⚠ No se pudo guardar en este navegador: guarde su declaración antes de cerrar.'
    if (!oida && !l.rescate) msg += ' Anotada como «sin oír»: no cuenta para la claridad.'
    if (cambian.length) msg += ` Con esto, ${cambian.length} línea${cambian.length === 1 ? '' : 's'} cambi${cambian.length === 1 ? 'ó' : 'aron'} de voz propuesta.`
    app.toast(msg)
  }

  return {
    render: () => render(app),

    /** Fraccion de la linea que se oyo de verdad, de 0 a 1. */
    oido(l) {
      const c = app.cober[l.id]
      return c ? Math.max(0, Math.min(1, (c.hi - c.lo) / Math.max(0.01, l.fin - l.ini))) : 0
    },

    oir(l, { antes, hasta, desde } = {}) {
      app.yaOyo = true
      const ini = desde ?? l.ini, fin = hasta ?? l.fin
      const ok = app.sonido.oir(l.audio, ini, fin, { antes: antes ?? 0.25, marca: { lid: l.id } })
      if (!ok) app.toast('No se puede oír: falta la grabación junto a la página.')
    },

    fijarAutoOir(si) {
      app.estado.autoOir(si)
      render(app)
    },

    textoRescate(l, texto) {
      if (E().lineas[l.id]) {
        clearTimeout(app._tr)
        app._tr = setTimeout(() => { app.estado.retocar(l.id, { texto: texto.trim() }); app.toast('Texto corregido y guardado.') }, 600)
      } else app.estado.borrador(l.id, texto)
    },

    deshacer() {
      const r = app.estado.deshacer()
      if (!r) return
      const l = r.lid && app.modelo.porId.get(r.lid)
      app.toast(`Deshecho: ${r.etiqueta}${l ? ` (${hms(l.ini)})` : ''}.`)
      if (l) app.abrir(l, 'deshacer')
      else render(app)
    },

    velocidad(x) {
      app.sonido.fijarVelocidad(x)
      app.estado.velocidad(x)
      render(app)
    },

    confirmar(l) {
      // Enter sobre una linea ya decidida NO la cambia: antes sustituia en
      // silencio su correccion por la propuesta de la maquina.
      if (E().lineas[l.id]) {
        app.toast('Esa línea ya la decidió usted. Para cambiarla, elija otra opción o quite su decisión.')
        return
      }
      const p = app.props.get(l.id)
      if (!p?.voz) return
      registrar(l, { decision: 'confirmada', voz: p.voz })
    },
    corregir(l, vid) {
      const p = app.props.get(l.id)
      registrar(l, { decision: vid === p?.voz ? 'confirmada' : 'corregida', voz: vid })
    },
    asignarDesdeLista(l, vid) {
      const p = app.props.get(l.id)
      registrar(l, { decision: vid === p?.voz ? 'confirmada' : 'corregida', voz: vid }, 'lista')
    },
    dividir(l, sel) {
      registrar(l, { decision: 'corregida', partes: [{ voz: sel[0] }, { voz: sel[1] }] })
    },
    declararVarios(l, vs) {
      registrar(l, { decision: 'varios', voces: vs })
    },
    noSeDistingue(l) {
      registrar(l, { decision: 'no_se_distingue' })
    },
    descartar(l) {
      if (!l.rescate) return
      registrar(l, { decision: 'descartado' })
    },
    saltar(l) {
      if (app.foco?.linea?.id === l.id && app.foco.paso === 2) {
        app.toast('En la prueba de la máquina no se salta: si no puede decidir, marque «No se distingue» (X). Cuenta en contra de la máquina, que es lo honesto.')
        return
      }
      app.estado.saltar(l.id)
      avanzar(l)
      render(app)
    },
    atras() {
      const f = app.historial.pop()
      if (f) { app.foco = f; render(app) }
    },
    abrir(l, origen) {
      if (app.foco?.linea && app.foco.linea.id !== l.id) app.historial.push(app.foco)
      app.foco = { linea: l, paso: null, motivo: origen }
      app.dividiendo = null; app.varios = null
      if (app.pestana !== 'revisar') cambiarPestana(app, 'revisar')
      render(app)
    },
    volverACola() {
      app.foco = siguiente(app.modelo, E(), app.props)
      render(app)
    },
    nuevaPersona(l) {
      app.modalNombrar(null, false, (vid) => registrar(l, { decision: 'corregida', voz: vid }))
    },

    exportar() {
      if (!E().declarado_por) return app.modalDeclarante(() => app.exportar())
      const d = declaracion(app)
      descargar(`voces declaradas - ${app.modelo.datos.titulo}.json`, JSON.stringify(d, null, 1))
      app.estado.marcarExportado()
      app.toast('Se descargó su declaración. Compruebe que está en Descargas y póngala junto a la grabación.')
      render(app)
    },

    async importar(file) {
      if (!file) return
      try {
        const d = await leerDeclaracion(file)
        if (d.formato !== 'despacho/voces-linea-a-linea') throw new Error('Ese archivo no es una declaración de voces.')
        // De otra preparacion NO se carga: las lineas se identifican por su
        // numero, y la misma posicion puede ser otra frase. Cargarla y volver
        // a exportarla la hacia pasar por buena.
        if (d.clave !== app.modelo.datos.clave) {
          throw new Error('Ese archivo es de otra preparación de esta página: sus líneas no son estas. No se carga.')
        }
        const n = Object.keys(E().lineas).length
        if (n) {
          app.modalConfirmar(`Cargar ese archivo reemplaza lo que tiene ahora en esta página (${n} decisiones). ¿Seguro?`, () => cargar(d))
          return
        }
        cargar(d)
      } catch (e) { app.toast(e.message) }
      function cargar(d) {
        app.estado.reemplazar({ declarado_por: d.declarado_por || '', voces: d.voces || {}, lineas: d.lineas || {} })
        app.foco = siguiente(app.modelo, E(), app.props)
        app.toast('Declaración cargada.')
        render(app)
      }
    },

    toast(msg) {
      const t = $('#aviso')
      t.textContent = msg
      t.hidden = false
      clearTimeout(app._t)
      app._t = setTimeout(() => { t.hidden = true }, 4200)
    },

    modalBienvenida() {
      abrirModal(app, el('div', {},
        el('h2', { text: 'Quién habla en cada línea' }),
        el('p', { text: 'La máquina agrupó las voces de estas grabaciones por su parecido y propone quién dice cada línea. Usted la oye y decide. Lo que usted decide es lo único que vale como declaración.' }),
        el('ol', { class: 'pasos-bienvenida' },
          el('li', {}, el('b', { text: 'Conozca las voces. ' }), 'Óigalas y dígales quién es cada una.'),
          el('li', {}, el('b', { text: 'Ponga a prueba a la máquina. ' }), 'Unas líneas al azar miden cuánto acierta. Sus propuestas solo cuentan si acierta el 90 %.'),
          el('li', {}, el('b', { text: 'Aclare lo dudoso ' }), `hasta que cada grabación llegue al ${pct(app.modelo.datos.meta_claridad)} de claridad.`)),
        el('p', { class: 'nota', html: '<b>Teclas:</b> <kbd>Espacio</kbd> oír · <kbd>Enter</kbd> sí, es esa voz · <kbd>1</kbd>–<kbd>9</kbd> es esa otra voz · <kbd>N</kbd> otra persona · <kbd>V</kbd> varios · <kbd>X</kbd> no se distingue · <kbd>→</kbd> saltar · <kbd>Z</kbd> deshacer' }),
        el('p', { class: 'nota', text: 'Una línea cuenta como oída cuando ha oído al menos el 70 % de ella. Lo que decida sin oírla queda anotado así y no cuenta para la claridad.' }),
        campoDeclarante(app, () => cerrarModal())))
    },

    modalDeclarante(despues) {
      abrirModal(app, el('div', {},
        el('h2', { text: '¿Quién declara?' }),
        el('p', { text: 'Cada decisión queda firmada con este nombre: es lo que la convierte en una declaración y no en una conjetura.' }),
        campoDeclarante(app, () => { cerrarModal(); despues?.() })))
    },

    modalNombrar(vid, suave = false, alCrear = null) {
      const c = vid ? app.cat[vid] : null
      const info = vid ? (E().voces[vid] || {}) : {}
      const nombre = el('input', { type: 'text', value: info.nombre || '', placeholder: 'Nombre y apellidos' })
      const cargo = el('input', { type: 'text', value: info.cargo || '', placeholder: 'Cargo o entidad (opcional)' })
      const como = el('input', { type: 'text', value: info.como_lo_sabe || '', placeholder: '¿Cómo lo sabe?' })
      const conocidas = (app.modelo.datos.personas_conocidas || []).filter((p) =>
        !Object.entries(E().voces).some(([k, v]) => k !== vid && !v.fusionada_en && (v.nombre || '').toLowerCase() === p.nombre.toLowerCase()))
      const bib = vid ? (app.modelo.datos.voces.find((v) => v.id === vid)?.biblioteca || []) : []
      const guardar = () => {
        const d = { nombre: nombre.value.trim(), cargo: cargo.value.trim(), como_lo_sabe: como.value.trim() }
        let id = vid
        if (!id) id = app.estado.nuevaVoz(d)
        else app.estado.nombrar(id, d)
        cerrarModal()
        alCrear?.(id)
        // El mismo nombre en dos voces casi siempre es una persona partida en
        // dos por la maquina. Se pregunta; no se une solo.
        const gemela = d.nombre && app.vivas.find((v) => v !== id
          && (E().voces[v]?.nombre || '').trim().toLowerCase() === d.nombre.toLowerCase())
        if (gemela) {
          setTimeout(() => app.modalConfirmar(
            `${app.cat[gemela].etiqueta} también se llama «${d.nombre}». ¿Son la misma persona? Si dice que sí, sus líneas y sus huellas se juntan (se puede deshacer).`,
            () => { app.estado.fusionar(id, gemela); app.toast(`Unidas: ahora «${d.nombre}» es una sola voz.`) }), 200)
        }
      }
      abrirModal(app, el('div', {},
        el('h2', { text: c ? (suave ? `¿Sabe quién es ${c.etiqueta}?` : `¿Quién es ${c.etiqueta}?`) : 'Otra persona' }),
        c ? el('div', { class: 'modal-oir' },
          el('button', { class: 'btn', type: 'button', onclick: () => oirMuestra(app, vid) }, '▶ Oír una muestra de esta voz')) : null,
        bib.length ? el('div', { class: 'sugerencias' },
          el('div', { class: 'sug-t', text: 'En la biblioteca de otras reuniones hay una voz muy parecida. Es una sugerencia de la máquina, no un reconocimiento: si la reconoce oyendo, dígalo con sus palabras en «¿Cómo lo sabe?».' }),
          ...bib.map((b) => el('button', { class: 'btn sug', type: 'button', title: b.fuente,
            onclick: () => { nombre.value = b.nombre; cargo.value = b.cargo || ''; como.focus() } },
          `${b.nombre}${b.cargo ? ' · ' + b.cargo : ''} — ${pct(b.parecido)}`))) : null,
        conocidas.length ? el('div', { class: 'sugerencias' },
          el('div', { class: 'sug-t', text: 'Personas ya nombradas en este caso:' }),
          ...conocidas.map((p) => el('button', { class: 'btn sug', type: 'button', title: p.fuente,
            onclick: () => { nombre.value = p.nombre; cargo.value = p.cargo || '' } }, p.nombre + (p.cargo ? ' · ' + p.cargo : '')))) : null,
        el('label', {}, 'Nombre', nombre),
        el('label', {}, 'Cargo', cargo),
        el('label', {}, '¿Cómo lo sabe?', como,
          el('span', { class: 'como-rapido' }, ...['Estuve en la reunión', 'Reconozco su voz', 'Se presenta en la grabación', 'Me lo dijo quien estuvo']
            .map((t) => el('button', { class: 'btn mini', type: 'button', text: t, onclick: () => { como.value = t } })))),
        el('div', { class: 'modal-botones' },
          el('button', { class: 'btn primario', type: 'button', onclick: guardar, text: 'Guardar' }),
          el('button', { class: 'btn', type: 'button', onclick: () => { if (!vid) { cerrarModal(); guardarSinNombre() } else cerrarModal() }, text: vid ? 'Todavía no lo sé' : 'Sin nombre por ahora' }))))
      setTimeout(() => nombre.focus(), 50)
      function guardarSinNombre() {
        const id = app.estado.nuevaVoz({})
        alCrear?.(id)
      }
    },

    modalConfirmar(texto, si) {
      abrirModal(app, el('div', {},
        el('p', { text: texto }),
        el('div', { class: 'modal-botones' },
          el('button', { class: 'btn primario', type: 'button', text: 'Sí', onclick: () => { cerrarModal(); si() } }),
          el('button', { class: 'btn', type: 'button', text: 'No', onclick: cerrarModal }))))
    },

    modalUnir(vid) {
      const c = app.cat[vid]
      abrirModal(app, el('div', {},
        el('h2', { text: `${c.largo} es la misma persona que…` }),
        el('p', { text: 'Sus líneas pasan a esa voz y las dos huellas se juntan. Se puede deshacer.' }),
        el('div', { class: 'parte-voces' }, ...app.vivas.filter((v) => v !== vid).map((v) =>
          chipVoz(app.cat[v], { opcion: true, onclick: () => { cerrarModal(); app.estado.fusionar(vid, v); app.toast(`${c.etiqueta} unida a ${app.cat[v].rotulo}.`) } }))),
        el('div', { class: 'modal-botones' }, el('button', { class: 'btn', type: 'button', text: 'Cancelar', onclick: cerrarModal }))))
    },
  }
}

function campoDeclarante(app, alListo) {
  const inp = el('input', { type: 'text', value: app.estado.todo.declarado_por || '', placeholder: 'Su nombre' })
  const ok = () => {
    if (!inp.value.trim()) { inp.focus(); return }
    app.estado.declarante(inp.value)
    alListo()
    render(app)
  }
  inp.addEventListener('keydown', (e) => { if (e.key === 'Enter') ok() })
  setTimeout(() => inp.focus(), 50)
  return el('div', { class: 'declarante' },
    el('label', {}, 'Quien declara', inp),
    el('button', { class: 'btn primario', type: 'button', text: 'Empezar', onclick: ok }))
}

function oirMuestra(app, vid) {
  const v = app.modelo.datos.voces.find((x) => x.id === vid)
  let cand = (v?.tipicas || []).map((id) => app.modelo.porId.get(id)).filter(Boolean)
  if (!cand.length) {
    cand = app.modelo.lineas.filter((l) => {
      const d = app.estado.todo.lineas[l.id]
      return d && DECLARADAS.has(d.decision) && !d.partes && resolver(d.voz, app.estado.todo.voces) === vid
    }).sort((a, b) => b.dur - a.dur)
  }
  if (!cand.length) return app.toast('Esta voz aún no tiene líneas para oír.')
  app._muestra = ((app._muestra || 0) + 1) % cand.length
  const l = cand[app._muestra]
  app.oir(l)
  app.toast(`Oyendo ${app.cat[vid]?.rotulo}: «${l.texto.slice(0, 70)}»`)
}

// ------------------------------------------------------------------ vistas ---

function render(app) {
  renderClaridad(app)
  renderVoces(app)
  const caja = $('#p-' + app.pestana)
  if (app.pestana === 'revisar') renderRevision(app, caja)
  else if (app.pestana === 'lineas') renderLineas(app, caja)
  else if (app.pestana === 'mapa') renderMapa(app, caja)
  else if (app.pestana === 'salida') renderSalida(app, caja)
  renderFranjas(app, $('#franjas'))
  renderGuardado(app)
}

function renderGuardado(app) {
  const g = $('#guardado')
  const E = app.estado.todo
  const n = Object.keys(E.lineas).length
  g.replaceChildren()
  if (!app.estado.almacenOK) {
    g.append(el('span', { class: 'guardado mal', text: '⚠ Este navegador no deja guardar aquí: guarde su declaración antes de cerrar' }))
  } else if (n) {
    g.append(el('span', { class: 'guardado', text: `✔ ${n} decisiones guardadas en este navegador` }))
  }
  if (app.estado.pendiente && n) g.append(el('span', { class: 'guardado pendiente', text: 'Aún no ha guardado su declaración (en «Lo que se entrega»)' }))
  if (E.declarado_por) g.append(el('span', { class: 'quien', text: `Declara: ${E.declarado_por}` }))
}

function renderClaridad(app) {
  const caja = $('#claridad')
  caja.replaceChildren()
  const meta = app.modelo.datos.meta_claridad
  const barra = (o, rot, grande) => {
    const c = o?.claridad || 0
    const ella = o?.total ? o.ella / o.total : 0
    const maq = o?.total ? o.maquina / o.total : 0
    return el('div', { class: 'clar' + (grande ? ' clar-global' : '') + (c >= meta ? ' ok' : ''),
      title: `Usted declaró ${pct(ella)} · la máquina aporta ${pct(maq)} · queda dudoso ${pct(1 - c)}` },
    el('div', { class: 'clar-rot' }, el('span', { text: rot }), el('b', { text: pct(c) }), c >= meta ? el('span', { class: 'clar-ok', text: '✔' }) : null),
    el('div', { class: 'clar-barra' },
      el('i', { class: 'ella', style: { width: (ella * 100) + '%' } }),
      el('i', { class: 'maq', style: { width: (maq * 100) + '%' } }),
      el('span', { class: 'meta', style: { left: (meta * 100) + '%' }, title: `Meta: ${pct(meta)}` })))
  }
  // El ✔ grande solo cuando TODAS las grabaciones llegan: un 86 % global puede
  // esconder una grabacion en el 40 %.
  const faltan = app.modelo.datos.audios.filter((a) => (app.clar.audios[a.id]?.claridad || 0) < meta)
  const g = barra(app.clar.global, 'Claridad de las voces, todas las grabaciones', true)
  if (faltan.length) g.querySelector('.clar-ok')?.remove()
  caja.append(g)
  for (const a of app.modelo.datos.audios) caja.append(barra(app.clar.audios[a.id], a.nombre))
  caja.append(el('div', { class: 'clar-falta' + (faltan.length ? '' : ' ok') },
    faltan.length ? `Para terminar, cada grabación debe llegar al ${pct(meta)}. Faltan: ${faltan.map((a) => `${a.nombre} (${pct(app.clar.audios[a.id]?.claridad)})`).join(', ')}.`
      : `✔ Las ${app.modelo.datos.audios.length} grabaciones llegan al ${pct(meta)}. Guarde su declaración en «Lo que se entrega».`))
  const { n, ok } = app.acierto
  const req = app.modelo.cal.revisiones_minimas
  const txt = n < req
    ? `La máquina aún no se ha puesto a prueba (${n} de ${req} revisiones): sus propuestas no cuentan todavía.`
    : app.clar.cuenta
      ? `La máquina acierta ${ok} de ${n} en lo que da por seguro: sus propuestas seguras cuentan.`
      : `La máquina acierta solo ${ok} de ${n} en lo que da por seguro: por debajo del ${pct(app.modelo.cal.precision_minima)}, no cuenta.`
  caja.append(el('div', { class: 'clar-maquina' + (app.clar.cuenta ? ' ok' : '') },
    el('span', { class: 'ley-ella' }), 'usted ', el('span', { class: 'ley-maq' }), 'máquina (si pasa la prueba) · ', txt))
}

function renderVoces(app) {
  const caja = $('#voces')
  caja.replaceChildren()
  const E = app.estado.todo
  const meta = app.modelo.datos.meta_claridad
  caja.append(el('div', { class: 'voces-cab' },
    el('h2', { text: 'Las voces' }),
    el('button', { class: 'btn mini', type: 'button', text: '+ Persona', onclick: () => app.modalNombrar(null) })))
  const pares = parecidas(app.cent, 0.9)
  const orden = app.vivas.slice().sort((a, b) => (app.clar.voces[b]?.total || 0) - (app.clar.voces[a]?.total || 0))
  for (const vid of orden) {
    const c = app.cat[vid]
    const o = app.clar.voces[vid] || { total: 0, ella: 0, maquina: 0, claridad: 0 }
    const nDecl = app.cent.cuentas[vid] || 0
    const cv = lienzo(200, 30, 'adn')
    dibujarAdn(cv, adnDeVoz(app.modelo, E, app.props, vid), c.color)
    const par = pares.find(([a, b]) => a === vid || b === vid)
    const otra = par ? (par[0] === vid ? par[1] : par[0]) : null
    const bib = app.modelo.datos.voces.find((v) => v.id === vid)?.biblioteca?.[0]
    caja.append(el('div', { class: 'voz', style: { '--c': c.color } },
      el('div', { class: 'voz-cab' },
        c.tecla ? el('kbd', { text: c.tecla }) : null,
        el('span', { class: 'punto', style: { background: c.color } }),
        el('div', { class: 'voz-nombre' },
          el('b', { text: c.nombre || c.etiqueta }),
          c.nombre ? el('span', { class: 'voz-etq', text: c.etiqueta + (c.cargo ? ' · ' + c.cargo : '') }) :
            el('button', { class: 'btn enlace', type: 'button', text: '¿Quién es?', onclick: () => app.modalNombrar(vid) }))),
      c.como ? el('div', { class: 'voz-como', text: `Lo sabe: ${c.como}` }) : null,
      el('div', { class: 'voz-clar' + (o.claridad >= meta ? ' ok' : '') },
        el('div', { class: 'clar-barra' },
          el('i', { class: 'ella', style: { width: (o.total ? o.ella / o.total * 100 : 0) + '%' } }),
          el('i', { class: 'maq', style: { width: (o.total ? o.maquina / o.total * 100 : 0) + '%' } }),
          el('span', { class: 'meta', style: { left: (meta * 100) + '%' } })),
        el('span', { text: `${pct(o.claridad)}${o.claridad >= meta ? ' ✔' : ''}` })),
      el('div', { class: 'voz-adn', title: 'Huella de esta voz: las 32 direcciones en que más varían las voces de esta reunión' }, cv),
      el('div', { class: 'voz-datos', text: `${duracion(o.total)} · ${nDecl} línea${nDecl === 1 ? '' : 's'} declarada${nDecl === 1 ? '' : 's'}${nDecl < 2 ? ' — huella aún provisional' : ''}` }),
      el('div', { class: 'voz-botones' },
        el('button', { class: 'btn mini', type: 'button', text: '▶ Oír', onclick: () => oirMuestra(app, vid) }),
        el('button', { class: 'btn mini', type: 'button', text: c.nombre ? '✎ Nombre' : '✎ Nombrar', onclick: () => app.modalNombrar(vid) }),
        el('button', { class: 'btn mini', type: 'button', text: '⤳ Es la misma que…', onclick: () => app.modalUnir(vid) }),
        el('button', { class: 'btn mini', type: 'button', text: '☰ Sus líneas', onclick: () => { app.filtro = { audio: 'todos', voz: vid, tipo: 'todas', q: '' }; cambiarPestana(app, 'lineas') } })),
      otra ? el('div', { class: 'voz-aviso' },
        `Su huella se parece ${pct(par[2])} a la de ${app.cat[otra].rotulo}. ¿Son la misma persona? `,
        el('button', { class: 'btn mini', type: 'button', text: 'Oír las dos', onclick: () => { oirMuestra(app, vid); setTimeout(() => oirMuestra(app, otra), 4000) } }),
        el('button', { class: 'btn mini', type: 'button', text: 'Son la misma…', onclick: () => app.modalConfirmar(
          `La máquina ve parecidas las huellas de ${c.rotulo} y ${app.cat[otra].rotulo}. Eso no dice que sean la misma persona: óigalas antes. Si lo son, sus líneas y sus huellas se juntan (se puede deshacer con Z). ¿Son la misma persona?`,
          () => { app.estado.fusionar(otra, vid); app.toast(`Unidas: ${app.cat[otra].etiqueta} pasa a ser ${c.rotulo}.`) }) })) : null,
      bib && !c.nombre ? el('div', { class: 'voz-aviso bib' },
        `Se parece ${pct(bib.parecido)} a ${bib.nombre} (biblioteca). `,
        el('button', { class: 'btn mini', type: 'button', text: 'Comprobar', onclick: () => app.modalNombrar(vid) })) : null))
  }
  const fundidas = Object.entries(E.voces).filter(([, v]) => v.fusionada_en)
  if (fundidas.length) {
    caja.append(el('div', { class: 'fundidas' }, el('div', { class: 'sug-t', text: 'Unidas:' }),
      ...fundidas.map(([vid, v]) => el('div', { class: 'fundida' },
        `${app.cat[vid]?.etiqueta || vid} → ${app.cat[resolver(vid, E.voces)]?.rotulo || '?'} `,
        el('button', { class: 'btn enlace', type: 'button', text: 'separar', onclick: () => app.estado.separar(vid) })))))
  }
}

// ------------------------------------------------------ pestanas y teclado ---

function montarPestanas(app) {
  for (const b of document.querySelectorAll('#pestanas button')) {
    b.addEventListener('click', () => cambiarPestana(app, b.dataset.p))
  }
}

function cambiarPestana(app, p) {
  app.pestana = p
  for (const b of document.querySelectorAll('#pestanas button')) b.classList.toggle('activa', b.dataset.p === p)
  for (const x of document.querySelectorAll('.panel')) x.hidden = x.id !== 'p-' + p
  render(app)
}

function montarTeclado(app) {
  document.addEventListener('keydown', (e) => {
    if ($('#modal') && !$('#modal').hidden) {
      if (e.key === 'Escape') cerrarModal()
      return
    }
    const t = e.target
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'SELECT')) return
    if (e.ctrlKey || e.metaKey || e.altKey) return
    const l = app.foco?.linea
    const k = e.key
    if (k === 'z' || k === 'Z') { app.deshacer(); return }
    if (app.pestana !== 'revisar' || !l) return
    if (k === ' ') {
      // Solo en «Revisar»: en la lista o el mapa la linea de la tarjeta no
      // esta a la vista, y oirla ahi confunde.
      e.preventDefault()
      if (app.sonido.suena()) app.sonido.parar()
      else app.oir(l)
      return
    }
    if (k === 'Enter') { e.preventDefault(); app.confirmar(l) }
    else if (/^[1-9]$/.test(k)) {
      const vid = app.vivas.find((v) => app.cat[v].tecla === k)
      if (vid) { e.preventDefault(); app.corregir(l, vid) }
    } else if (k === 'n' || k === 'N') { e.preventDefault(); app.nuevaPersona(l) }
    else if (k === 'v' || k === 'V') { if (!l.rescate) { app.varios = l.id; render(app) } }
    else if (k === 'x' || k === 'X') app.noSeDistingue(l)
    else if (k === 'Delete') { if (l.rescate) app.descartar(l) }
    else if (k === 'd' || k === 'D') { if (l.cambio && l.partes) { app.dividiendo = l.id; render(app) } }
    else if (k === 'a' || k === 'A') app.oir(l, { antes: 3 })
    else if (k === 'ArrowRight') { e.preventDefault(); app.saltar(l) }
    else if (k === 'ArrowLeft') { e.preventDefault(); app.atras() }
  })
}

// ------------------------------------------------------------------- modal ---

function abrirModal(app, contenido) {
  const m = $('#modal')
  m.replaceChildren(el('div', { class: 'modal-caja', role: 'dialog', 'aria-modal': 'true' },
    el('button', { class: 'modal-x', type: 'button', 'aria-label': 'Cerrar', text: '×', onclick: cerrarModal }),
    contenido))
  m.hidden = false
}

function cerrarModal() {
  const m = $('#modal')
  m.hidden = true
  m.replaceChildren()
}

arrancar()
