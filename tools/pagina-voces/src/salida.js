/* Lo que sale de la pagina. SPEC-15 §5.
 *
 * Dos cosas distintas:
 *   - la DECLARACION (.json): la fuente de verdad. La lee `genoma_de_voz.py
 *     aplicar`, que recalcula todo por su cuenta y no se fia del resumen.
 *   - la TRANSCRIPCION CON VOCES (.md): para leer, o pegar en un chat y
 *     refinar actas y resumenes. Lleva ✔ / ≈ / ? en cada linea.
 */
import { el, hms, pct, descargar, copiar } from './util.js'
import { nombreVigente } from './carpeta.js'
import { DECLARADAS, resolver, oyendo } from './genoma.js'

export function declaracion(app) {
  const E = app.estado.todo
  const voces = {}
  for (const v of app.modelo.datos.voces) voces[v.id] = { ...(E.voces[v.id] || {}) }
  for (const [vid, info] of Object.entries(E.voces)) if (info.nueva) voces[vid] = { ...info }
  const maquina = {}
  // La propuesta de TODAS las lineas, decididas o no: `aplicar` la necesita
  // para contar la claridad igual que esta pagina.
  for (const l of app.modelo.lineas) {
    const p = app.props.get(l.id)
    if (p) maquina[l.id] = { voz: p.voz, banda: p.banda, parecido: +p.parecido.toFixed(4), margen: +p.margen.toFixed(4) }
  }
  const claridad = {}
  for (const [k, o] of Object.entries(app.clar.audios)) claridad[k] = +o.claridad.toFixed(4)
  return {
    formato: 'despacho/voces-linea-a-linea',
    version: 1,
    clave: app.modelo.datos.clave,
    titulo: app.modelo.datos.titulo,
    declarado_por: E.declarado_por,
    exportado: new Date().toISOString(),
    nota: 'Lo que una persona declaró oyendo. La máquina propuso por el parecido de la voz; ella decidió. '
      + 'Las líneas sin decisión van en «maquina» y son propuestas: nadie las ha oído.',
    voces,
    lineas: E.lineas,
    maquina,
    resumen: { claridad, acierto_alta: [app.acierto.ok, app.acierto.n], maquina_cuenta: app.clar.cuenta },
  }
}

export function transcripcionMd(app, soloAudio = null) {
  const E = app.estado.todo
  const quien = E.declarado_por || '(sin nombre de quien declara)'
  const r = (v) => {
    const c = app.cat[resolver(v, E.voces)]
    return c ? (c.nombre ? `${c.nombre}${c.cargo ? ' · ' + c.cargo : ''}` : `${c.etiqueta} (sin nombre)`) : '—'
  }
  const out = [
    `# Transcripción con voces — ${app.modelo.datos.titulo}`,
    '',
    `**Quién habla, según ${quien}.** La máquina propuso por el parecido de la voz; ella decidió oyendo.`,
    '',
    `- **✔** lo declaró ${quien} oyendo la línea. Si dice _«sin oír»_, lo decidió sin oírla: es suyo, pero no oyendo`,
    '- **≈** lo propone la máquina: **nadie lo ha oído** y no sirve para atribuir',
    '- **?** ella marcó que no se distingue quién habla',
    '',
  ]
  for (const au of app.modelo.datos.audios) {
    if (soloAudio && au.id !== soloAudio) continue
    const cl = app.clar.audios[au.id]
    const deElla = cl?.total ? cl.ella / cl.total : 0
    const deMaq = cl?.total ? cl.maquina / cl.total : 0
    out.push('---', '', `## ${au.nombre}`, '',
      `Claridad de las voces: **${pct(cl?.claridad)}** (meta ${pct(app.modelo.datos.meta_claridad)}) — `
      + `declarado por ella oyendo ${pct(deElla)}, propuesto por la máquina puesta a prueba ${pct(deMaq)} · archivo \`${au.archivo}\``, '')
    const huecos = app.modelo.datos.huecos.filter((h) => h.audio === au.id)
    const sinHuella = (app.modelo.datos.sin_huella || []).filter((s) => s.audio === au.id)
    const items = [...(app.modelo.porAudio[au.id] || []).map((l) => ({ t: l.ini, l })),
      ...huecos.map((h) => ({ t: h.ini, h })), ...sinHuella.map((s) => ({ t: s.ini, s }))].sort((a, b) => a.t - b.t)
    for (const it of items) {
      if (it.s) {
        out.push(`**[${hms(it.s.ini)}] ? Sin huella de voz: demasiado corta para reconocerla** ${it.s.texto}`, '')
        continue
      }
      if (it.h) {
        out.push(`_[${hms(it.h.ini)}] — ${Math.round(it.h.fin - it.h.ini)} s sin transcribir —_`, '')
        continue
      }
      const l = it.l
      const d = E.lineas[l.id]
      if (l.rescate) {
        // Solo lo que ella acepto oyendo. Lo demas no existe para la salida.
        if (d && d.se_dijo !== false && d.texto && (DECLARADAS.has(d.decision) || d.decision === 'no_se_distingue')) {
          const quienHabla = DECLARADAS.has(d.decision) ? `✔ ${r(d.voz)}` : '? No se distingue quién'
          out.push(`**[${hms(l.ini)}] ${quienHabla}** ${d.texto}  _(rescatada: no estaba en la transcripción; la oyó ${quien})_`, '')
        }
        continue
      }
      const dud = l.dudas?.length ? `  \`[?]\` (${l.dudas.slice(0, 2).join(' · ')})` : ''
      const sinOir = d && !oyendo(d) ? ' _(sin oír)_' : ''
      if (d && DECLARADAS.has(d.decision)) {
        if (d.partes && l.partes) {
          d.partes.forEach((p, k) => out.push(`**[${hms(k ? l.cambio.en : l.ini)}] ✔ ${r(p.voz)}**${sinOir} ${l.partes[k]}${dud}`, ''))
        } else out.push(`**[${hms(l.ini)}] ✔ ${r(d.voz)}**${sinOir} ${l.texto}${dud}`, '')
      } else if (d?.decision === 'varios' && (d.voces || []).length >= 2) {
        out.push(`**[${hms(l.ini)}] ✔ Varios a la vez: ${d.voces.map(r).join(' y ')}**${sinOir} ${l.texto}${dud}`, '')
      } else if (d?.decision === 'varios') {
        out.push(`**[${hms(l.ini)}] ? Varios a la vez, sin distinguir quiénes** ${l.texto}${dud}`, '')
      } else if (d?.decision === 'no_se_distingue') {
        out.push(`**[${hms(l.ini)}] ? No se distingue quién habla** ${l.texto}${dud}`, '')
      } else {
        const p = app.props.get(l.id)
        out.push(`**[${hms(l.ini)}] ≈ ${r(p?.voz)}** _(propuesta, seguridad ${p?.banda || '—'})_ ${l.texto}${dud}`, '')
      }
    }
  }
  return out.join('\n')
}

export function renderSalida(app, caja) {
  caja.replaceChildren()
  const E = app.estado.todo
  const meta = app.modelo.datos.meta_claridad
  const sinOir = Object.values(E.lineas).filter((d) => d.oida === false).length
  const nDec = Object.keys(E.lineas).length
  const comprobaciones = [
    [!!E.declarado_por, E.declarado_por ? `Declara: ${E.declarado_por}` : 'Falta decir quién declara', () => app.modalDeclarante()],
    ...app.modelo.datos.audios.map((a) => {
      const c = app.clar.audios[a.id]?.claridad || 0
      return [c >= meta, `${a.nombre}: claridad ${pct(c)} ${c >= meta ? '— llega al ' + pct(meta) : '— no llega al ' + pct(meta)}`]
    }),
    [app.clar.cuenta, app.clar.cuenta
      ? `La máquina acertó ${app.acierto.ok} de ${app.acierto.n} en lo que daba por segura: sus propuestas seguras cuentan`
      : `La máquina no ha superado la prueba (${app.acierto.ok} de ${app.acierto.n}): solo cuenta lo que usted declaró`],
    [sinOir === 0, sinOir ? `${sinOir} de ${nDec} decisiones se tomaron sin oír la línea: quedan anotadas «sin oír» y no cuentan para la claridad` : `Todas sus decisiones se tomaron oyendo la línea (al menos el 70 % de cada una)`],
  ]
  const nombre = nombreVigente(app.modelo.datos.titulo)
  const enCarpeta = app.carpeta?.disponible
  const destino = app.carpeta?.donde?.modo === 'proyecto'
    ? `“${app.carpeta.donde.proyecto} › 2-Borradores › Voces”` : 'la carpeta “Voces” del proyecto'
  caja.append(
    el('h2', { text: 'Lo que se entrega' }),
    el('ul', { class: 'comprobaciones' }, ...comprobaciones.map(([ok, t, fn]) =>
      el('li', { class: ok ? 'ok' : 'no' }, el('span', { class: 'ico', text: ok ? '✔' : '!' }), t,
        fn && !ok ? el('button', { class: 'btn mini', type: 'button', text: 'Resolver', onclick: fn }) : null))),
    el('div', { class: 'salida-botones' },
      el('button', { class: 'btn primario', type: 'button', onclick: () => app.exportar() },
        enCarpeta ? '💾 Guardar mi declaración en el proyecto' : '💾 Guardar mi declaración (se descarga)'),
      el('button', { class: 'btn', type: 'button', onclick: () => app.descargarDeclaracion() },
        '⤓ Descargar una copia (.json)'),
      el('button', { class: 'btn', type: 'button', onclick: () => {
        descargar(`Transcripcion con voces - ${app.modelo.datos.titulo}.md`, transcripcionMd(app), 'text/markdown')
      } }, '⤓ Transcripción con voces (.md)'),
      el('button', { class: 'btn', type: 'button', onclick: async () => {
        app.toast(await copiar(transcripcionMd(app)) ? 'Copiada. Péguela en el chat para refinar el acta o el resumen.' : 'No se pudo copiar: use el botón de descarga.')
      } }, '⧉ Copiar para pegar en el chat'),
      el('label', { class: 'btn' }, '⤒ Cargar una declaración guardada…',
        el('input', { type: 'file', accept: '.json,application/json', hidden: true, onchange: (e) => app.importar(e.target.files[0]) }))),
    el('p', { class: 'nota' },
      el('b', { text: 'La declaración es lo que vale. ' }),
      enCarpeta
        ? `Con “💾 Guardar” se escribe en ${destino} como “${nombre}”, y desde entonces se guarda sola con cada decisión; cada vez que pulse, además, queda una copia con la fecha. `
        : `Con “💾 Guardar” se descarga como “${nombre}”. Al terminar, arrástrela desde Descargas a la carpeta “Lo que declaré” del proyecto (dentro de “2-Borradores”). `,
      'El arnés la convierte en la transcripción con voces, el registro de su declaración y la biblioteca de voces para la próxima reunión. ',
      el('b', { text: 'Lo que usted marca aquí se guarda también en este navegador' }),
      ', pero eso es una comodidad: si se borran los datos del navegador, se pierde.'),
    el('h3', { text: 'Vista previa de la transcripción con voces' }),
    el('pre', { class: 'previa', text: transcripcionMd(app).split('\n').slice(0, 80).join('\n') + '\n…' }))
}

export function leerDeclaracion(file) {
  return new Promise((res, rej) => {
    const fr = new FileReader()
    fr.onload = () => { try { res(JSON.parse(fr.result)) } catch { rej(new Error('Ese archivo no es una declaración legible.')) } }
    fr.onerror = () => rej(new Error('No se pudo leer el archivo.'))
    fr.readAsText(file)
  })
}
