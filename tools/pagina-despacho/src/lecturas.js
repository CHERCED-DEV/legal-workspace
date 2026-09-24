/* Las otras lecturas automáticas de una línea: qué parte de cada una parece
 * corresponder a ESTA línea, y dónde no coinciden con la transcripción.
 *
 * Cada lectura es el texto de un tramo de 20 s (la línea y las de alrededor),
 * no el de la línea: enseñarla entera hacía creer que otra máquina había oído
 * un párrafo donde la transcripción tiene cuatro palabras. La parte que
 * «corresponde» se busca por parecido del texto: es una estimación, y la
 * página lo dice. Nada de esto cambia la transcripción.
 */

const quitarTildes = (s) => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '')
/** Una palabra para comparar: minúsculas, sin tildes ni signos. */
export const normal = (w) => quitarTildes(String(w ?? '').toLowerCase()).replace(/[^\p{L}\p{N}]/gu, '')
export const palabras = (texto) => String(texto ?? '').split(/\s+/).filter(Boolean)
const FIN_DE_FRASE = /[.?!…]["»)]*$/

/** Pares [i, j] de la subsecuencia común más larga (palabras vacías no casan). */
function lcs(a, b) {
  const n = a.length, m = b.length
  const L = Array.from({ length: n + 1 }, () => new Uint16Array(m + 1))
  for (let i = n - 1; i >= 0; i--) {
    for (let j = m - 1; j >= 0; j--) {
      L[i][j] = a[i] && a[i] === b[j] ? L[i + 1][j + 1] + 1 : Math.max(L[i + 1][j], L[i][j + 1])
    }
  }
  const pares = []
  let i = 0, j = 0
  while (i < n && j < m) {
    if (a[i] && a[i] === b[j]) { pares.push([i, j]); i++; j++ }
    else if (L[i + 1][j] >= L[i][j + 1]) i++
    else j++
  }
  return pares
}

/**
 * La parte de `lectura` que parece corresponder a `linea`.
 * `pos` (0–1, opcional): dónde cae la línea dentro del tramo de la lectura;
 * desempata a favor de lo que está a esa altura.
 * Devuelve null si no se parece lo bastante (menos de la mitad de las palabras
 * en común: con un tercio, «los» y «de» bastaban para emparejar), o { antes, tramo: [{ w, igual }], despues, comunes, de, igual }.
 */
export function alinear(linea, lectura, pos = null) {
  const A = palabras(linea), B = palabras(lectura)
  const a = A.map(normal), b = B.map(normal)
  const n = a.filter(Boolean).length
  if (!n || !B.length) return null
  let mejor = null
  for (let i = 0; i < B.length; i++) {
    for (let m = Math.max(1, A.length - 2); m <= A.length + 3 && i + m <= B.length; m++) {
      const pares = lcs(a, b.slice(i, i + m))
      if (!pares.length) continue
      let nota = pares.length - 0.15 * Math.abs(m - A.length)
      if (pos != null) nota -= Math.abs(i / B.length - pos)
      if (!mejor || nota > mejor.nota + 1e-9) mejor = { i, pares, nota }
    }
  }
  if (!mejor || mejor.pares.length < Math.ceil(n / 2)) return null
  // Se ensancha para que quepa lo que la línea tiene antes de la primera
  // coincidencia y después de la última, sin cruzar un final de frase.
  const p0 = mejor.pares[0], p1 = mejor.pares[mejor.pares.length - 1]
  const j0 = mejor.i + p0[1], j1 = mejor.i + p1[1]
  let s = Math.max(0, j0 - p0[0])
  for (let k = j0 - 1; k >= s; k--) if (FIN_DE_FRASE.test(B[k])) { s = k + 1; break }
  let e = Math.min(B.length, j1 + 1 + (A.length - 1 - p1[0]))
  if (FIN_DE_FRASE.test(A[A.length - 1])) {
    for (let k = j1; k < e; k++) if (FIN_DE_FRASE.test(B[k])) { e = k + 1; break }
  }
  const pares = lcs(a, b.slice(s, e))
  const iguales = new Set(pares.map(([, j]) => j))
  const tramo = B.slice(s, e).map((w, j) => ({ w, igual: iguales.has(j) || !normal(w) }))
  return {
    antes: B.slice(0, s), tramo, despues: B.slice(e), comunes: pares.length, de: n,
    igual: pares.length === n && tramo.every((x) => x.igual) && tramo.length === A.length,
    pares, desde: s,
  }
}

const limpio = (ws) => ws.join(' ').replace(/^[«"(¿¡]+|[.,;:?!…»")]+$/g, '')

/**
 * Dónde no coinciden: [{ dice, lecturas: [{ lee, fuente }] }], en el orden de
 * la línea. `dice` es lo de la transcripción; `lee`, lo que escribió otra
 * lectura en ese sitio ('' si no escribió nada).
 */
export function discordias(linea, lecturas) {
  const A = palabras(linea)
  const por = new Map()
  for (const l of lecturas) {
    const al = alinear(linea, l.texto, l.pos ?? null)
    if (!al || al.igual) continue
    const B = al.tramo.map((x) => x.w)
    const pares = [[-1, -1], ...lcs(A.map(normal), B.map(normal)), [A.length, B.length]]
    for (let k = 1; k < pares.length; k++) {
      const [ia, ja] = pares[k - 1], [ib, jb] = pares[k]
      const dice = A.slice(ia + 1, ib), lee = B.slice(ja + 1, jb)
      if (!dice.length || !dice.some((w) => normal(w))) continue
      if (normal(dice.join('')) === normal(lee.join(''))) continue
      const clave = `${ia + 1}:${dice.map(normal).join(' ')}`
      if (!por.has(clave)) por.set(clave, { orden: ia + 1, dice: limpio(dice), lecturas: [] })
      por.get(clave).lecturas.push({ lee: limpio(lee), fuente: l.fuente, cambio: [ia + 1, ib] })
    }
  }
  return [...por.values()].sort((x, y) => x.orden - y.orden)
}

/** La línea con un trozo cambiado por lo que escribió otra lectura: para
 *  ofrecerlo como punto de partida de SU corrección, nunca como corrección. */
export function conCambio(linea, [desde, hasta], lee) {
  const A = palabras(linea)
  const fin = A.slice(desde, hasta).join(' ').match(/[.,;:?!…»")]+$/)?.[0] || ''
  const antes = A.slice(0, desde)
  if (!lee && fin && antes.length) antes[antes.length - 1] += fin
  return [...antes, ...(lee ? [lee + fin] : []), ...A.slice(hasta)].join(' ')
}
