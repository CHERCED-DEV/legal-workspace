/* Lo crítico en negrita, igual que md2html.resaltar: el veredicto corto del
   principio («Sin cerrar:», «no se dice.»), los minutos y las alertas. Dentro
   de una cita entre « » no se toca nada: es texto literal. Devuelve HTML con el
   texto ya escapado; las únicas etiquetas son las <strong> que pone esto. */

const CRITICAS = ['no se dice', 'no consta', 'no lo asume', 'nadie', 'no se entiende', 'no es un compromiso',
  'sin cerrar', 'palabra dudosa', 'puede no ser habla', 'las pasadas no coinciden', 'voz dudosa',
  'conviene oír', 'hay que oír', 'probablemente', 'no dice', 'no sé', 'no se ponen de acuerdo',
  'no recoge nada', 'no se sostienen']
const CRITICAS_RE = new RegExp(`(?<![\\p{L}\\p{N}_])(${CRITICAS.map((x) => x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|')})(?![\\p{L}\\p{N}_])`, 'giu')

export const escapar = (s) => String(s ?? '').replace(/[&<>"']/g, (c) =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]))

export function resaltar(texto) {
  let t = escapar(texto)
  t = t.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
  t = t.split(/(«[^»]*»)/).map((p) => p.startsWith('«') ? p
    : p.replace(/(?<!\d)(\d\d:\d\d:\d\d)(?!\d)/g, '<strong>$1</strong>').replace(CRITICAS_RE, '<strong>$1</strong>')).join('')
  const m = t.match(/^((?:&#?\w+;|<[^>]*>|«[^»]*»|[^«.:;&<]){2,}?[.:;])(?=\s|$)/)
  if (m && m[1].replace(/<[^>]*>/g, '').length <= 60) {
    t = `<strong>${m[1].replace(/<\/?strong>/g, '')}</strong>${t.slice(m[1].length)}`
  }
  return t
}
