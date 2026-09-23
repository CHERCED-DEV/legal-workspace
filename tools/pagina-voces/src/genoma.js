/* El genoma de voz, en funciones puras. SPEC-15 §4.
 *
 * Regla que gobierna este archivo: la maquina PROPONE por parecido; lo que ella
 * declara manda. Una propuesta nunca se convierte en declaracion aqui dentro.
 *
 * Nada de esto toca el DOM: se prueba con Node (prueba-genoma.mjs).
 */

export function deB64(s) {
  const bin = atob(s)
  const v = new Float32Array(bin.length)
  let n = 0
  for (let i = 0; i < bin.length; i++) {
    let b = bin.charCodeAt(i)
    if (b > 127) b -= 256
    v[i] = b
    n += b * b
  }
  n = Math.sqrt(n) || 1
  for (let i = 0; i < v.length; i++) v[i] /= n
  return v
}

/** El ADN: 32 valores con escala comun a todas las lineas. No se normaliza. */
export function adnDeB64(s) {
  const bin = atob(s)
  const v = new Float32Array(bin.length)
  for (let i = 0; i < bin.length; i++) {
    let b = bin.charCodeAt(i)
    if (b > 127) b -= 256
    v[i] = b / 127
  }
  return v
}

export function punto(a, b) {
  let s = 0
  for (let i = 0; i < a.length; i++) s += a[i] * b[i]
  return s
}

export function media(vs) {
  if (!vs.length) return null
  const m = new Float32Array(vs[0].length)
  for (const v of vs) for (let i = 0; i < m.length; i++) m[i] += v[i]
  let n = 0
  for (let i = 0; i < m.length; i++) n += m[i] * m[i]
  n = Math.sqrt(n) || 1
  for (let i = 0; i < m.length; i++) m[i] /= n
  return m
}

export const DECLARADAS = new Set(['confirmada', 'corregida'])

/** Cuanto de una linea hay que haber oido para que cuente como «oida». */
export const OIDA_MINIMA = 0.7

/** Una decision tomada sin oir es de ella, pero no es una declaracion OYENDO:
 * no alimenta la huella, no cuenta para la claridad, no pone a prueba a la
 * maquina. `undefined` (datos anteriores a esta regla) cuenta como oida. */
export const oyendo = (d) => d && d.oida !== false

/** La voz a la que de verdad apunta un id, siguiendo las fusiones. */
export function resolver(vid, voces) {
  const vistos = new Set()
  while (vid && voces[vid]?.fusionada_en && !vistos.has(vid)) {
    vistos.add(vid)
    vid = voces[vid].fusionada_en
  }
  return vid
}

/**
 * Prepara el modelo en memoria: vectores decodificados una sola vez.
 * `datos` es el JSON de genoma_de_voz; devuelve un objeto con todo indexado.
 */
export function montar(datos) {
  // Los rescates -- tramos que la transcripcion no tenia, oidos otra vez -- van
  // con las lineas para oirlos y proponer quien habla, pero marcados: no
  // cuentan en la claridad ni en el acierto, y no existen si ella no los acepta.
  const todas = [...datos.lineas, ...(datos.rescates || []).map((r) => ({ ...r, rescate: true }))]
  const lineas = todas.map((l, k) => ({
    ...l,
    k,
    dur: Math.max(0.01, l.fin - l.ini),
    v: deB64(l.vec),
    a: l.adn ? adnDeB64(l.adn) : null,
    va: l.cambio ? deB64(l.cambio.vec_a) : null,
    vb: l.cambio ? deB64(l.cambio.vec_b) : null,
  }))
  // Las primeras direcciones del ADN varian mucho mas que las ultimas: sin
  // estandarizar, la huella dibujada son tres barras y ruido. Cada direccion se
  // divide por su dispersion en ESTA reunion, para que las 32 cuenten igual.
  const conAdn = lineas.filter((l) => l.a)
  if (conAdn.length > 2) {
    const n = conAdn[0].a.length
    for (let i = 0; i < n; i++) {
      let s = 0, s2 = 0
      for (const l of conAdn) { s += l.a[i]; s2 += l.a[i] * l.a[i] }
      const m = s / conAdn.length
      const sd = Math.sqrt(Math.max(1e-12, s2 / conAdn.length - m * m))
      for (const l of conAdn) l.a[i] = (l.a[i] - m) / sd
    }
  }
  const porId = new Map(lineas.map((l) => [l.id, l]))
  const inicial = {}
  for (const v of datos.voces) inicial[v.id] = deB64(v.vec)
  // Vecinas en la misma grabacion, para el contexto y el oido.
  const porAudio = {}
  for (const l of lineas) (porAudio[l.audio] ||= []).push(l)
  for (const arr of Object.values(porAudio)) {
    arr.sort((x, y) => x.ini - y.ini)
    arr.forEach((l, i) => { l.prev = arr[i - 1] || null; l.next = arr[i + 1] || null })
  }
  return { datos, lineas, porId, inicial, porAudio, cal: datos.calibracion }
}

/** Las voces vivas: las iniciales no fusionadas, mas las nuevas que ella anadio. */
export function vocesVivas(modelo, estado) {
  const out = []
  for (const v of modelo.datos.voces) {
    if (!estado.voces[v.id]?.fusionada_en) out.push(v.id)
  }
  for (const [vid, info] of Object.entries(estado.voces)) {
    if (info.nueva && !info.fusionada_en) out.push(vid)
  }
  return out
}

/**
 * Centroide de cada voz viva. Con 2+ lineas declaradas, SOLO lo declarado.
 * Con menos, la huella inicial (y la de las voces fusionadas en ella) mas lo
 * declarado. Las lineas que se pisan, «varios» y «no se distingue» no entran.
 */
export function centroides(modelo, estado) {
  const vivas = vocesVivas(modelo, estado)
  const miembros = Object.fromEntries(vivas.map((v) => [v, []]))
  const iniciales = Object.fromEntries(vivas.map((v) => [v, []]))
  for (const v of modelo.datos.voces) {
    const destino = resolver(v.id, estado.voces)
    if (iniciales[destino]) iniciales[destino].push(modelo.inicial[v.id])
  }
  for (const [lid, d] of Object.entries(estado.lineas)) {
    if (!DECLARADAS.has(d.decision) || !oyendo(d)) continue
    const l = modelo.porId.get(lid)
    if (!l || l.pisa >= modelo.cal.pisa_max) continue
    if (d.partes && l.va && l.vb) {
      const [p0, p1] = d.partes
      const a = resolver(p0?.voz, estado.voces), b = resolver(p1?.voz, estado.voces)
      if (miembros[a]) miembros[a].push(l.va)
      if (miembros[b]) miembros[b].push(l.vb)
      continue
    }
    const vid = resolver(d.voz, estado.voces)
    if (miembros[vid]) miembros[vid].push(l.v)
  }
  const out = {}
  const cuentas = {}
  for (const vid of vivas) {
    const m = miembros[vid]
    cuentas[vid] = m.length
    if (m.length >= 2) out[vid] = media(m)
    else if (iniciales[vid].length || m.length) out[vid] = media([...iniciales[vid], ...m])
  }
  return { c: out, cuentas }
}

export function bandaDe(l, margen, cal) {
  if (l.corta || l.pisa >= cal.pisa_max) return 'baja'
  if (margen >= cal.bandas.alta) return 'alta'
  if (margen >= cal.bandas.media) return 'media'
  return 'baja'
}

/**
 * Lo que la maquina propone para CADA linea (declarada o no: para las
 * declaradas sirve de comparacion). Devuelve Map id -> propuesta.
 */
export function proponer(modelo, estado, cent) {
  const ids = Object.keys(cent.c)
  const res = new Map()
  for (const l of modelo.lineas) {
    let mejor = null, segundo = null
    const sims = []
    for (const vid of ids) {
      const s = punto(l.v, cent.c[vid])
      sims.push([vid, s])
      if (!mejor || s > mejor[1]) { segundo = mejor; mejor = [vid, s] }
      else if (!segundo || s > segundo[1]) segundo = [vid, s]
    }
    sims.sort((a, b) => b[1] - a[1])
    // Con una sola voz no hay con que comparar: seguridad baja, no alta.
    const margen = mejor && segundo ? mejor[1] - segundo[1] : 0
    res.set(l.id, {
      voz: mejor ? mejor[0] : null,
      parecido: mejor ? mejor[1] : 0,
      segunda: segundo ? segundo[0] : null,
      parecido2: segundo ? segundo[1] : 0,
      margen,
      banda: bandaDe(l, margen, modelo.cal),
      sims,
    })
  }
  return res
}

/** Cuanto acierta la maquina en lo que da por seguro, segun lo que ella reviso.
 *
 * SOLO cuentan las lineas SORTEADAS en el paso 2 (origen «prueba») y OIDAS.
 * Revision del 2026-09-23: antes contaba cualquier linea de banda alta que ella
 * decidiera, y eso sesgaba la prueba de dos maneras -- las de «conocer las
 * voces» son las mas tipicas (la maquina casi seguro acierta), y las que ella
 * elige en la lista son las que le parecen raras --; y bastaba pulsar Enter
 * ocho veces sin oir para aprobarla. */
export function acierto(estado) {
  let n = 0, ok = 0
  for (const d of Object.values(estado.lineas)) {
    if (d.banda_maquina !== 'alta' || !d.propuesta_maquina) continue
    if (d.origen !== 'prueba' || d.rescate || !oyendo(d)) continue
    n++
    if (d.decision === 'confirmada' && !d.partes) ok++
  }
  return { n, ok }
}

export function maquinaCuenta(estado, cal) {
  const { n, ok } = acierto(estado)
  return n >= cal.revisiones_minimas && ok >= cal.precision_minima * n
}

export const ES_CLARA_DECISION = new Set(['confirmada', 'corregida', 'varios'])

/** ¿Esta decision deja clara la linea? Oida, y si es «varios», con quienes. */
export function esClara(d) {
  if (!d || !ES_CLARA_DECISION.has(d.decision) || !oyendo(d)) return false
  if (d.decision === 'varios') return (d.voces || []).length >= 2
  return true
}

/**
 * Claridad por grabacion y por voz. SPEC-15 §4.2.
 * Devuelve { audios: {A1: {total, ella, maquina, claridad}}, voces: {vid: ...}, cuenta }
 */
export function claridad(modelo, estado, props) {
  const cuenta = maquinaCuenta(estado, modelo.cal)
  const audios = {}, voces = {}
  const sumar = (obj, k, campo, s) => {
    obj[k] ||= { total: 0, ella: 0, maquina: 0 }
    obj[k][campo] += s
  }
  for (const l of modelo.lineas) {
    if (l.rescate) continue
    const d = estado.lineas[l.id]
    const p = props.get(l.id)
    sumar(audios, l.audio, 'total', l.dur)
    if (esClara(d)) {
      sumar(audios, l.audio, 'ella', l.dur)
      if (d.decision !== 'varios') {
        if (d.partes && l.partes) {
          for (const pa of d.partes) {
            const v = resolver(pa.voz, estado.voces)
            sumar(voces, v, 'total', l.dur / 2)
            sumar(voces, v, 'ella', l.dur / 2)
          }
        } else {
          const v = resolver(d.voz, estado.voces)
          sumar(voces, v, 'total', l.dur)
          sumar(voces, v, 'ella', l.dur)
        }
      }
      continue
    }
    const v = p?.voz
    // Si ella dijo que ahi no se distingue quien habla, la maquina no puede
    // «aclararlo» por su cuenta: esa linea queda dudosa.
    if (d && ['no_se_distingue', 'varios', 'descartado', 'no_se_dijo'].includes(d.decision)) continue
    if (v) sumar(voces, v, 'total', l.dur)
    if (p && p.banda === 'alta' && cuenta) {
      sumar(audios, l.audio, 'maquina', l.dur)
      if (v) sumar(voces, v, 'maquina', l.dur)
    }
  }
  for (const o of [...Object.values(audios), ...Object.values(voces)]) {
    o.claridad = o.total ? (o.ella + o.maquina) / o.total : 0
  }
  let T = 0, E = 0, M = 0
  for (const o of Object.values(audios)) { T += o.total; E += o.ella; M += o.maquina }
  return { audios, voces, cuenta, global: { total: T, ella: E, maquina: M, claridad: T ? (E + M) / T : 0 } }
}

/** Pseudoaleatorio estable, sembrado con la clave: la misma pagina elige igual. */
export function barajar(arr, semilla) {
  let h = 2166136261
  for (const ch of semilla) { h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619) }
  const a = arr.slice()
  for (let i = a.length - 1; i > 0; i--) {
    h ^= h << 13; h ^= h >>> 17; h ^= h << 5
    const j = Math.abs(h) % (i + 1);
    [a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

/**
 * Que revisar ahora. SPEC-15 §4.3. Devuelve { linea, paso, motivo } o null.
 *   1. Conocer las voces: 2 lineas tipicas de cada voz con 20 s o mas.
 *   2. Poner a prueba a la maquina: lineas de banda alta al azar, hasta 8.
 *   3. Lo que mas aclara.
 */
export function siguiente(modelo, estado, props, excluir = new Set()) {
  const libre = (l) => !estado.lineas[l.id] && !excluir.has(l.id)
  const saltadas = new Set(estado.saltadas || [])

  // Paso 1
  const segs = {}
  for (const l of modelo.lineas) {
    const v = props.get(l.id)?.voz
    if (v) segs[v] = (segs[v] || 0) + l.dur
  }
  const cent = centroides(modelo, estado)
  for (const v of modelo.datos.voces) {
    const vid = resolver(v.id, estado.voces)
    if (vid !== v.id) continue
    if ((segs[vid] || 0) < 20 || (cent.cuentas[vid] || 0) >= 2) continue
    const t = (v.tipicas || []).map((id) => modelo.porId.get(id))
      .find((l) => l && libre(l) && !saltadas.has(l.id))
    if (t) return { linea: t, paso: 1, motivo: 'conocer', voz: vid }
  }

  // Paso 2. Sigue muestreando mientras la maquina no haya pasado la prueba,
  // hasta 30: con un solo fallo en 8 no llega al 90 %, y parar ahi la dejaria
  // suspendida para siempre por una sola muestra.
  const { n } = acierto(estado)
  if (n < modelo.cal.revisiones_minimas || (!maquinaCuenta(estado, modelo.cal) && n < 30)) {
    const altas = modelo.lineas.filter((l) => libre(l) && !saltadas.has(l.id) && !l.rescate
      && props.get(l.id)?.banda === 'alta')
    const orden = barajar(altas.map((l) => l.id), modelo.datos.clave)
    if (orden.length) return { linea: modelo.porId.get(orden[0]), paso: 2, motivo: 'prueba' }
  }

  // Paso 3
  const alta = modelo.cal.bandas.alta || 0.1
  let mejor = null, pm = -Infinity
  for (const l of modelo.lineas) {
    if (!libre(l)) continue
    const p = props.get(l.id)
    if (!p) continue
    if (p.banda === 'alta' && maquinaCuenta(estado, modelo.cal) && !l.rescate) continue
    let prio = l.dur * (1 - Math.min(1, Math.max(0, p.margen) / alta))
    // Lo rescatado primero: son pocos tramos y es texto que hoy no esta en la
    // transcripcion. Los que oyen dos pistas o mas, antes que los de una sola.
    if (l.rescate) {
      const palabras = (l.texto || '').split(/\s+/).filter(Boolean).length
      prio += 20 + 5 * (l.oyen || 0) + 10 * (l.acuerdo || 0) + Math.min(20, palabras)
      if (l.invencion) prio -= 35
    }
    if (l.cambio) prio += 3
    if (l.pisa >= modelo.cal.pisa_max) prio += 1
    if (saltadas.has(l.id)) prio -= 1000
    if (prio > pm) { pm = prio; mejor = l }
  }
  return mejor ? { linea: mejor, paso: 3, motivo: mejor.rescate ? 'rescate' : 'aclarar' } : null
}

/** Cuantas lineas NO declaradas cambian de voz propuesta entre dos estados. */
export function cambiadas(antes, despues, estado) {
  const out = []
  for (const [id, p] of despues) {
    if (estado.lineas[id]) continue
    const q = antes.get(id)
    if (q && q.voz !== p.voz) out.push(id)
  }
  return out
}

/** Pares de voces que se parecen tanto que quiza son la misma persona. */
export function parecidas(cent, umbral = 0.9) {
  const ids = Object.keys(cent.c)
  const out = []
  for (let i = 0; i < ids.length; i++)
    for (let j = i + 1; j < ids.length; j++) {
      const s = punto(cent.c[ids[i]], cent.c[ids[j]])
      if (s >= umbral) out.push([ids[i], ids[j], s])
    }
  return out.sort((a, b) => b[2] - a[2])
}

/** El ADN de una voz: media de los ADN de sus lineas (el ADN es lineal). */
export function adnDeVoz(modelo, estado, props, vid) {
  const acc = new Float32Array(32)
  let n = 0
  for (const l of modelo.lineas) {
    if (!l.a) continue
    const d = estado.lineas[l.id]
    const v = d && DECLARADAS.has(d.decision) && !d.partes ? resolver(d.voz, estado.voces)
      : (!d ? props.get(l.id)?.voz : null)
    if (v !== vid) continue
    for (let i = 0; i < acc.length; i++) acc[i] += l.a[i]
    n++
  }
  if (!n) return null
  for (let i = 0; i < acc.length; i++) acc[i] /= n
  return acc
}
