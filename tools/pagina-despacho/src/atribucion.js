/* Quién habla: lo que ella confirma OYENDO, voz por voz. Solo cuentas, sin DOM.
 *
 * La máquina agrupó sonidos parecidos y numeró los grupos. Eso no dice quién
 * habla: lo dice ella, fragmento a fragmento, después de oírlo. Aquí se cuenta
 * cuánto de cada voz ha confirmado, y nada más.
 *
 * Reglas que no se pueden aflojar sin que la cifra mienta:
 *  - Solo cuenta lo que ella oyó: al menos el 70 % del HABLA del fragmento,
 *    contada una sola vez (oír dos veces el mismo trozo no suma), y medida
 *    sobre las líneas, no sobre los silencios de en medio.
 *  - «No sé quién» y «hablan varios» cuentan EN CONTRA: se quedan en la voz que
 *    propuso la máquina sin confirmar. Si no, la meta se alcanza saltándose lo
 *    difícil.
 *  - «Es otra voz» mueve el fragmento a esa voz, y ahí cuenta como confirmado:
 *    lo afirmó ella oyéndolo.
 *  - Una decisión vale para el fragmento que ella oyó, no para el que hoy
 *    lleve su mismo nombre: lleva su FIRMA (líneas, inicio, fin, voz de la
 *    máquina), y si la transcripción cambió, no cuenta.
 *  - La cifra va por SEGUNDOS, no por fragmentos: diez «sí» cortos no pesan
 *    lo mismo que un minuto de discurso.
 */

export const META = 0.85
export const OIDA_MINIMA = 0.7
/* Una intervención larga se parte en fragmentos de este largo como mucho, por
   frontera de línea. Con la separación que funde voces, un «turno» de cinco
   minutos casi seguro mezcla personas, y ella tiene que poder decir «este trozo
   es de otra voz». */
export const FRAGMENTO_MAX_S = 30
/* Un silencio así dentro de una intervención también la parte: no se le pide
   oír medio minuto de nada para decidir. */
export const HUECO_S = 10

export const DECISIONES = ['si', 'otra', 'no_se', 'varios']
export const esNueva = (v) => typeof v === 'string' && /^nueva-\d+$/.test(v)

/** Fragmentos, en orden: tramos seguidos de la MISMA voz propuesta, partidos
 *  por largo y por silencios. `vozDe(bloque)` -> string o null. Cada uno
 *  lleva sus `zonas`: los intervalos de habla de sus líneas. */
export function fragmentar(bloques, vozDe) {
  const out = []
  let cur = null
  for (const b of bloques) {
    if (b.ancla?.tipo !== 'tiempo') continue
    const v = vozDe(b)
    const ini = b.ancla.inicio
    const fin = Math.max(b.ancla.fin, ini)
    const corta = !cur || cur.maquina !== v
      || (ini - cur.fin) > HUECO_S
      || (fin - cur.inicio) > FRAGMENTO_MAX_S
    if (corta) {
      cur = { id: b.id, maquina: v, bloques: [], zonas: [], inicio: ini, fin, dur: 0 }
      out.push(cur)
    }
    cur.bloques.push(b.id)
    cur.zonas.push([ini, fin])
    cur.fin = Math.max(cur.fin, fin)
    cur.dur += fin - ini
  }
  out.forEach((f, i) => { f.n = i })
  return out
}

/** Lo que identifica al fragmento que ella oyó. */
export const firma = (f) => ({ lineas: f.bloques.length, inicio: Math.round(f.inicio * 10) / 10,
  fin: Math.round(f.fin * 10) / 10, maquina: f.maquina })
export const coincide = (d, f) => !!d?.firma && !!f && d.firma.lineas === f.bloques.length
  && Math.abs(d.firma.inicio - f.inicio) < 0.15 && Math.abs(d.firma.fin - f.fin) < 0.15
  && d.firma.maquina === f.maquina

/** ¿Es una decisión bien formada? (lo que llega de un archivo puede no serlo) */
export const valida = (d) => !!d && DECISIONES.includes(d.decision)
  && typeof d.oido === 'number' && d.oido >= 0 && d.oido <= 1

/** La voz a la que pertenece el fragmento: la que dijo ella, si dijo otra y
 *  la decisión es de ESTE fragmento. */
export const efectiva = (f, d) => (d && d.decision === 'otra' && d.voz && (!f || !d.firma || coincide(d, f)))
  ? d.voz : f.maquina

/** ¿Cuenta como confirmado? Solo sí u otra, bien formada, oyéndolo, y del
 *  fragmento que es (si se da `f`). */
export const cuenta = (d, f = null) => valida(d)
  && (d.decision === 'si' || (d.decision === 'otra' && !!d.voz))
  && d.oido >= OIDA_MINIMA
  && (!f || coincide(d, f))

/** Estado de un fragmento para pintarlo. */
export function estadoDe(f, d) {
  if (!d) return 'pendiente'
  if (f && !coincide(d, f)) return 'otra_version'
  if (!cuenta(d, f)) return d.decision === 'varios' ? 'varios' : 'no_se'
  return d.decision === 'otra' && d.voz !== f.maquina ? 'movido' : 'confirmado'
}

/** Cuentas por voz y totales. `decisiones` = { idFragmento: decision }. */
export function resumir(frags, decisiones) {
  const voces = new Map()
  const de = (v) => {
    if (!voces.has(v)) voces.set(v, { voz: v, total: 0, confirmado: 0, frags: [], hechos: 0, dudas: 0, pendientes: 0, anadida: esNueva(v) })
    return voces.get(v)
  }
  let total = 0, confirmado = 0, sinVoz = 0, sinVozPend = 0
  for (const f of frags) {
    const d0 = decisiones[f.id]
    const d = d0 && coincide(d0, f) ? d0 : null   // lo de otra versión no cuenta
    const v = efectiva(f, d)
    total += f.dur
    if (cuenta(d, f)) confirmado += f.dur
    if (v == null) {
      sinVoz += f.dur
      if (!d) sinVozPend += 1
      continue
    }
    const e = de(v)
    e.total += f.dur
    e.frags.push(f)
    if (cuenta(d, f)) { e.confirmado += f.dur; e.hechos += 1 }
    else if (d) e.dudas += 1
    else e.pendientes += 1
  }
  for (const e of voces.values()) {
    e.pct = e.total ? e.confirmado / e.total : 0
    // Una voz que añadió ella está confirmada por construcción: no se cuenta
    // como «identificada», que es lo que se dice de las voces de la máquina.
    e.identificada = !e.anadida && e.total > 0 && e.pct >= META
  }
  const lista = [...voces.values()].sort((a, b) => (a.anadida - b.anadida) || (b.total - a.total))
  const deMaquina = lista.filter((e) => !e.anadida)
  return {
    voces: lista,
    porVoz: voces,
    total, confirmado, pct: total ? confirmado / total : 0,
    identificadas: deMaquina.filter((e) => e.identificada).length,
    deMaquina: deMaquina.length,
    sinVoz, sinVozPend,
  }
}

/** El siguiente fragmento que hay que preguntar para la voz `v` (o `null` =
 *  sin voz asignada), después de `desdeId`.
 *  - modo 'pendientes': los que la máquina le dio y ella no ha decidido,
 *    dejando para el final los que saltó en esta sesión (`saltados`).
 *  - modo 'repaso': los que dejó en «no sé» o «varios» y no ha vuelto a ver
 *    en esta pasada (`vistos`). Termina: no da vueltas sin fin. */
export function siguiente(frags, decisiones, v, desdeId = null, { modo = 'pendientes', saltados = new Set(), vistos = new Set() } = {}) {
  const suyos = frags.filter((f) => f.maquina === v)
  if (!suyos.length) return null
  const k = desdeId ? suyos.findIndex((f) => f.id === desdeId) : -1
  const rota = [...suyos.slice(k + 1), ...suyos.slice(0, k + 1)]
  const decidido = (f) => decisiones[f.id] && coincide(decisiones[f.id], f)
  if (modo === 'repaso') {
    return rota.find((f) => decidido(f) && !cuenta(decisiones[f.id], f) && !vistos.has(f.id)) || null
  }
  // Lo saltado no vuelve en esta pasada: cuando solo queda eso, se termina y
  // se dice cuánto quedó sin decidir.
  return rota.find((f) => !decidido(f) && !saltados.has(f.id) && f.id !== desdeId) || null
}

/** Cuántos quedan de una voz: sin decidir, y en «no sé»/«varios». */
export function quedan(frags, decisiones, v) {
  let pendientes = 0, dudas = 0
  for (const f of frags) {
    if (f.maquina !== v) continue
    const d = decisiones[f.id]
    if (!d || !coincide(d, f)) pendientes += 1
    else if (!cuenta(d, f)) dudas += 1
  }
  return { pendientes, dudas }
}

/* ---------------------------------------------------------- lo oído */
/** Añade [a, b] a una lista de intervalos, fundiendo los que se tocan. */
export function unir(lista, a, b) {
  if (!(b > a)) return lista
  const out = []
  let [x, y] = [a, b]
  for (const [p, q] of lista) {
    if (q < x - 0.05 || p > y + 0.05) out.push([p, q])
    else { x = Math.min(x, p); y = Math.max(y, q) }
  }
  out.push([x, y])
  return out.sort((m, n) => m[0] - n[0])
}
/** Cuánto de las `zonas` cubre la lista de intervalos oídos. */
export function cubierto(lista, zonas) {
  let s = 0
  for (const [a, b] of zonas) {
    for (const [p, q] of lista) s += Math.max(0, Math.min(b, q) - Math.max(a, p))
  }
  return s
}
export const largo = (zonas) => zonas.reduce((s, [a, b]) => s + Math.max(0, b - a), 0)
/** Fracción oída de unas zonas: 0..1. Una zona de largo cero no se puede oír. */
export const fraccionOida = (lista, zonas) => {
  const L = largo(zonas)
  return L > 0 ? Math.min(1, cubierto(lista, zonas) / L) : 0
}

/* ---------------------------------------------------------- textos */
export function mmss(s) {
  s = Math.max(0, Math.floor(s || 0))
  const m = Math.floor(s / 60)
  return m ? `${m}:${String(s % 60).padStart(2, '0')}` : `${s} s`
}
/** Hacia abajo: 84,9 % se lee 84 %, nunca «85 %» sin haber llegado. */
export const pct = (x) => `${Math.floor((x || 0) * 100)} %`
export const plural = (n, uno, varios) => `${n} ${n === 1 ? uno : varios}`
