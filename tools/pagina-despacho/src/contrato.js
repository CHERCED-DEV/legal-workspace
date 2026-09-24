/* El contrato. Es lo unico que la pagina sabe del mundo.
 *
 * La pagina NO sabe que existen las transcripciones, ni las cronologias, ni los
 * inventarios. Sabe de BLOQUES con un ancla, un riesgo y unas marcas. Cualquier
 * metodo del despacho que emita esta forma gana pagina sin tocar la plantilla.
 *
 *   documento  { titulo, tipo, advertencia }
 *   fuentes[]  { tipo: 'audio'|'imagen'|'pdf', ruta }
 *   bloques[]  { id, ancla, riesgo, marcas[], etiqueta?, confianza?, alternativas[] }
 *   vistas[]   que montar
 *
 * `ancla` es lo que hace generico el sistema:
 *   { tipo:'tiempo',  inicio, fin }   una grabacion
 *   { tipo:'pagina',  n }             un documento escaneado
 *   { tipo:'ninguna' }                texto sin origen navegable
 */

export const RIESGOS = ['ninguno', 'bajo', 'medio', 'alto']

/** Orden de gravedad, para ordenar y para pintar. */
export const peso = (r) => Math.max(0, RIESGOS.indexOf(r))

const BLOQUE_VACIO = {
  id: '', ancla: { tipo: 'ninguna' }, riesgo: 'ninguno',
  marcas: [], etiqueta: null, gravedad: 0, alternativas: [],
}

export function leerContrato(nodo) {
  let crudo = {}
  try { crudo = JSON.parse(nodo?.textContent || '{}') } catch { crudo = {} }

  const bloques = (crudo.bloques || []).map((b, i) => ({
    ...BLOQUE_VACIO, ...b,
    id: b.id || `b${i}`,
    ancla: b.ancla || { tipo: 'ninguna' },
    marcas: Array.isArray(b.marcas) ? b.marcas : [],
    alternativas: Array.isArray(b.alternativas) ? b.alternativas : [],
    riesgo: RIESGOS.includes(b.riesgo) ? b.riesgo : (b.marcas?.length ? 'medio' : 'ninguno'),
    gravedad: Number(b.gravedad) || 0,
  }))

  return {
    documento: crudo.documento || { titulo: 'Documento', tipo: '', advertencia: '' },
    fuentes: crudo.fuentes || [],
    bloques,
    vistas: crudo.vistas || ['lectura'],
    clave: crudo.clave || 'sin-clave',
    /** Un archivo que deberia estar junto a la pagina: si no carga, esta sola. */
    sonda: crudo.sonda || null,
    /** Lo que la maquina no sabe leer: tramos para que ella los oiga y cuente. */
    ilegibles: Array.isArray(crudo.ilegibles) ? crudo.ilegibles : [],
    /** Cada compromiso senalado, con las lineas que lo sostienen. */
    compromisos: Array.isArray(crudo.compromisos) ? crudo.compromisos : [],
    /** Sugerencias de glosario (hipótesis, nadie las ha oído) y el caso al que
     *  pertenece la página: el glosario de ella vale para todo el caso. */
    glosario: Array.isArray(crudo.glosario) ? crudo.glosario : [],
    caso: crudo.caso || null,
    porId: new Map(bloques.map((b) => [b.id, b])),
    /** La fuente navegable principal, si la hay. */
    audio: (crudo.fuentes || []).find((f) => f.tipo === 'audio') || null,
    temporal: bloques.some((b) => b.ancla?.tipo === 'tiempo'),
    dudosos: bloques.filter((b) => b.riesgo !== 'ninguno'),
    /** El riesgo dice QUE clase de problema es; la gravedad, a CUAL ir primero. */
    porGravedad: bloques.filter((b) => b.riesgo !== 'ninguno')
      .slice().sort((a, b) => b.gravedad - a.gravedad),
  }
}

/** El texto visible de un bloque sale del DOM, no del contrato: el contrato
 *  lleva metadatos, y el texto ya viene renderizado para que se lea sin JS. */
export const nodoDe = (b) => document.getElementById(b.id)

/** El texto TRANSCRITO de un nodo, sin lo que la página le puso encima (lo
 *  que se dijo según el glosario). Copiar una cita tiene que dar la
 *  transcripción tal cual, no una mezcla. */
export function textoTranscrito(nodo) {
  if (!nodo) return ''
  const c = nodo.cloneNode(true)
  c.querySelectorAll('.gl-dijo').forEach((n) => n.remove())
  return c.textContent.trim()
}

export const hms = (s) => {
  s = Math.max(0, Math.floor(s || 0))
  const p = (n) => String(Math.floor(n)).padStart(2, '0')
  return `${p(s / 3600)}:${p((s % 3600) / 60)}:${p(s % 60)}`
}
