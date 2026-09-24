/* Quién habla — confirmarlo oyendo, voz por voz.
 *
 * La máquina agrupó sonidos parecidos y los numeró. Aquí ella recorre cada voz
 * fragmento a fragmento: suena, y se le pregunta «¿es el Hablante 1?». Sí; es
 * otra voz (y cuál); o no sé. Cada respuesta se guarda al momento, mueve la
 * barra de esa voz, y a los 85 % la voz queda identificada.
 *
 * Lo que NO hace, a propósito:
 *  - No deja decidir sin oír: los botones se activan al 70 % del HABLA del
 *    fragmento, contada una vez (oido.js).
 *  - No cuenta «no sé» como hecho: cuenta en contra.
 *  - No nombra a nadie: el nombre lo escribe ella, y solo se enseña sobre lo
 *    que ella confirmó para esa voz, con «según usted».
 *  - No toca la transcripción, ni sus marcas de «Confirmado» (el TEXTO), ni
 *    los nombres que otra persona declaró antes y vienen en la página.
 *  - No deja pasar las teclas de la página mientras pregunta: «c» marcaba el
 *    texto como confirmado sin haberlo oído.
 */
import { fragmentar, resumir, siguiente, quedan, efectiva, estadoDe, coincide, valida, firma,
         esNueva, META, OIDA_MINIMA, mmss, pct, plural } from './atribucion.js'
import { hms, textoTranscrito } from './contrato.js'
import { crearOido, anunciarPanel, alAbrirOtro, TECLAS_DE_LA_PAGINA } from './oido.js'

const NS = 'http://www.w3.org/2000/svg'
/* Catorce colores distinguibles. El texto nunca va en estos colores (en oscuro
   no llegan al contraste): solo puntos, bordes y la franja. */
const PALETA = ['#3d6fa8', '#b3582c', '#4f8a3c', '#8b52a6', '#a07f1d', '#2b8883', '#b0476e', '#6d6a64',
                '#5a63b8', '#8a6b3f', '#c0392b', '#16a085', '#7f8c2a', '#9b59b6']
const ESCRIBIENDO = new Set(['INPUT', 'TEXTAREA', 'SELECT'])
const LETRAS = 'abcdefghijklmopqrstuwyz'   // sin n, v ni x

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]))
const hoy = () => new Date().toLocaleDateString('es-CO', { year: 'numeric', month: '2-digit', day: '2-digit' })

export function montarVoces({ C, medios, enfocar, estado }) {
  const caja = document.getElementById('voces')
  const indicador = document.getElementById('btn-voces')
  if (!caja || !C.temporal) return null

  const vozDe = (b) => { const m = /Hablante ([^\s—-]+)/.exec(b.etiqueta || ''); return m ? m[1] : null }
  const frags = fragmentar(C.bloques, vozDe)
  const maquina = [...new Set(frags.map((f) => f.maquina).filter((v) => v != null))]
  if (!frags.length || !maquina.length) return null
  const porId = new Map(frags.map((f) => [f.id, f]))
  const duracion = Math.max(...C.bloques.map((b) => b.ancla?.fin || 0), 1)
  const vozValida = (v) => maquina.includes(v) || esNueva(v)

  /* ---------------------------------------------------------- almacenamiento */
  const LLAVE_NOMBRES = 'despacho:voces:' + C.clave
  const LLAVE = 'despacho:atribucion:' + C.clave
  const leer = (k) => { try { return JSON.parse(localStorage.getItem(k) || '{}') } catch { return {} } }
  /* Solo lo bien formado y de una voz que existe. Lo de otra versión de la
     transcripción se guarda, pero no cuenta: se ve como «vuelva a oírlo». */
  const depurar = (ds) => Object.fromEntries(Object.entries(ds || {}).filter(([id, d]) =>
    porId.has(id) && valida(d) && (d.decision !== 'otra' || vozValida(d.voz))))
  let nombres = leer(LLAVE_NOMBRES)
  let decisiones = depurar(leer(LLAVE))
  const guardar = () => {
    try { localStorage.setItem(LLAVE, JSON.stringify(decisiones)) } catch { /* lo dice el aviso de persistencia */ }
    estado.tocar?.()
  }
  const guardarNombres = () => { try { localStorage.setItem(LLAVE_NOMBRES, JSON.stringify(nombres)) } catch {} }
  window.addEventListener('storage', (e) => {
    if (e.key === LLAVE) { decisiones = depurar(leer(LLAVE)); pintar() }
    if (e.key === LLAVE_NOMBRES) { nombres = leer(LLAVE_NOMBRES); pintar() }
  })

  /* ------------------------------------------------------------------ voces */
  const orden = resumir(frags, {}).voces.map((e) => e.voz)
  /* Una voz nueva nunca reutiliza el número de otra que existió: heredaría su
     nombre y sus fragmentos se sumarían a otra persona. */
  const numeroNuevo = () => 1 + Math.max(0, ...[...Object.values(decisiones).map((d) => d.voz), ...Object.keys(nombres)]
    .filter(esNueva).map((v) => Number(v.slice(6))))
  const nuevas = () => [...new Set(Object.values(decisiones)
    .filter((d) => d.decision === 'otra' && esNueva(d.voz)).map((d) => d.voz))].sort()
  const color = (v) => {
    if (v == null) return '#8a877f'
    const i = orden.indexOf(v)
    return PALETA[(i >= 0 ? i : orden.length + nuevas().indexOf(v)) % PALETA.length]
  }
  const rotulo = (v) => v == null ? 'Sin voz asignada'
    : esNueva(v) ? `Voz nueva ${v.slice(6)}` : `Hablante ${v}`
  const declarados = {}
  for (const b of C.bloques) {
    const m = /Hablante ([^\s—-]+) — (.+)$/.exec(b.etiqueta || '')
    if (m) declarados[m[1]] = m[2].trim()
  }
  const conNombre = (v) => {
    const n = (nombres[v] || '').trim()
    if (n) return `${rotulo(v)} — ${n} (según usted)`
    return declarados[v] ? `${rotulo(v)} — ${declarados[v]} (declarado)` : rotulo(v)
  }

  /* ------------------------------------------------------------------ panel */
  caja.hidden = false
  caja.classList.add('vz')
  caja.innerHTML = `
    <div class="vz-cab">
      <div class="vz-cab-texto">
        <h2>Quién habla <span class="vz-sub">confírmelo oyendo, voz por voz</span></h2>
        <p class="vz-global-texto"></p>
        <div class="vz-barra grande" aria-hidden="true"><i></i><b class="vz-meta"></b></div>
        <p class="vz-fuera"></p>
      </div>
      <button type="button" class="boton tenue vz-plegar" aria-expanded="true">Ocultar</button>
    </div>
    <div class="vz-cuerpo">
      <div class="vz-tarjetas"></div>
      <details class="vz-menores" hidden>
        <summary></summary>
        <div class="vz-filas"></div>
      </details>
      <p class="vz-nota">Pulse <strong>Empezar</strong> en una voz: sonará cada fragmento que la máquina le atribuye
        y usted dice si es esa voz, otra, o que no lo sabe. Una voz queda <strong>identificada</strong> cuando usted ha
        confirmado <strong>oyendo</strong> el ${Math.round(META * 100)} % de lo que dice. «No sé» y «hablan varios» no cuentan
        como confirmado. <em>La máquina solo agrupó sonidos parecidos: lo que usted confirme aquí lo afirma usted.</em>
        Se guarda al momento; «Guardar lo comprobado» lo deja además en un archivo.</p>
    </div>`
  const tarjetas = caja.querySelector('.vz-tarjetas')
  const menores = caja.querySelector('.vz-menores')
  const filas = caja.querySelector('.vz-filas')
  /* Una voz con muy poca habla no merece una tarjeta entera: va en una fila
     compacta, plegada. Así el panel enseña primero donde está el trabajo. */
  const MENOR_S = 45
  const plegar = caja.querySelector('.vz-plegar')
  const LLAVE_PLEGADO = 'despacho:voces-plegado:' + C.clave
  const aplicarPlegado = (p) => {
    caja.classList.toggle('plegado', p)
    plegar.textContent = p ? 'Mostrar' : 'Ocultar'
    plegar.setAttribute('aria-expanded', String(!p))
  }
  try { aplicarPlegado(localStorage.getItem(LLAVE_PLEGADO) === '1') } catch { aplicarPlegado(false) }
  plegar.addEventListener('click', () => {
    const p = !caja.classList.contains('plegado')
    aplicarPlegado(p)
    try { localStorage.setItem(LLAVE_PLEGADO, p ? '1' : '0') } catch {}
  })
  indicador?.addEventListener('click', () => {
    aplicarPlegado(false)
    document.querySelector('.pestana[data-p="voces"]')?.click()
    const arriba = (() => { const b = document.getElementById('barra'); return b && getComputedStyle(b).position === 'sticky' ? b.getBoundingClientRect().height : 0 })()
    const destino = document.querySelector('.pestanas') || caja
    window.scrollTo({ top: destino.getBoundingClientRect().top + window.scrollY - arriba - 8, behavior: 'smooth' })
  })

  const tarjetaDe = new Map()
  function tarjeta(v) {
    if (tarjetaDe.has(v)) return tarjetaDe.get(v)
    const t = document.createElement('article')
    t.className = 'vz-tarjeta'
    t.dataset.voz = v ?? ''
    t.style.setProperty('--voz', color(v))
    t.innerHTML = `
      <header class="vz-t-cab">
        <span class="vz-punto" aria-hidden="true"></span>
        <span class="vz-t-nombre"></span>
        ${v == null ? '<span class="vz-quien-hueco"></span>' : `<input type="text" class="vz-quien"
          aria-label="Quién es ${esc(rotulo(v))}: nombre y cargo, lo escribe usted">`}
        <span class="vz-sello" hidden>✓ Identificada</span>
        <span class="vz-pct"></span>
      </header>
      <div class="vz-barra" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-label="Confirmado de ${esc(rotulo(v))}"><i></i><b class="vz-meta" title="meta ${Math.round(META * 100)} %"></b></div>
      <p class="vz-cuenta"></p>
      <div class="vz-t-pie"><div class="vz-mapa-caja"></div><button type="button" class="boton primaria vz-ir"></button></div>`
    const inp = t.querySelector('.vz-quien')
    if (inp) {
      inp.value = nombres[v] || ''
      inp.addEventListener('input', () => {
        nombres[v] = inp.value
        guardarNombres()
        estado.tocar?.()
        pintar()
      })
    }
    t.querySelector('.vz-ir').addEventListener('click', () => {
      empezar(v, t.querySelector('.vz-ir').dataset.modo || 'pendientes')
    })
    t.querySelector('.vz-mapa-caja').appendChild(mapa(v))
    tarjetaDe.set(v, t)
    return t
  }

  /* Una franja de la grabación entera con lo de ESTA voz: dónde habla, y qué
     está ya confirmado. Pulsar un trozo lo abre para decidir. */
  const mapas = new Map()
  function mapa(v) {
    const svg = document.createElementNS(NS, 'svg')
    svg.setAttribute('class', 'vz-mapa')
    svg.setAttribute('viewBox', `0 0 ${duracion} 10`)
    svg.setAttribute('preserveAspectRatio', 'none')
    svg.setAttribute('role', 'img')
    const fondo = document.createElementNS(NS, 'rect')
    fondo.setAttribute('x', 0); fondo.setAttribute('y', 4.5); fondo.setAttribute('width', duracion); fondo.setAttribute('height', 1)
    fondo.setAttribute('class', 'vz-mapa-fondo')
    svg.appendChild(fondo)
    const rects = new Map()
    const cabeza = document.createElementNS(NS, 'rect')
    cabeza.setAttribute('y', 0); cabeza.setAttribute('height', 10)
    cabeza.setAttribute('width', Math.max(duracion / 700, 0.5))
    cabeza.setAttribute('class', 'vz-mapa-cabeza'); cabeza.setAttribute('visibility', 'hidden')
    svg.addEventListener('click', (ev) => {
      const id = ev.target?.dataset?.id
      if (id) abrir(porId.get(id), v)
    })
    mapas.set(v, { svg, rects, cabeza })
    svg.appendChild(cabeza)
    return svg
  }
  function pintarMapa(v) {
    const m = mapas.get(v)
    if (!m) return
    const suyos = frags.filter((f) => f.maquina === v || efectiva(f, decisiones[f.id]) === v)
    for (const f of suyos) {
      let r = m.rects.get(f.id)
      if (!r) {
        r = document.createElementNS(NS, 'rect')
        r.setAttribute('x', f.inicio); r.setAttribute('y', 1)
        r.setAttribute('width', Math.max(f.fin - f.inicio, duracion / 900)); r.setAttribute('height', 8)
        r.dataset.id = f.id
        r.innerHTML = `<title>${hms(f.inicio)} · ${mmss(f.dur)}</title>`
        m.svg.insertBefore(r, m.cabeza)
        m.rects.set(f.id, r)
      }
      const d = decisiones[f.id]
      let e = estadoDe(f, d)
      if (e === 'movido') e = efectiva(f, d) === v ? 'confirmado movido-dentro' : 'movido-fuera'
      if (e === 'otra_version') e = 'pendiente'
      r.setAttribute('class', `vz-f vz-f-${e}${activo?.id === f.id ? ' vz-f-activo' : ''}`)
    }
    for (const [id, r] of m.rects) {
      const f = porId.get(id)
      if (!(f.maquina === v || efectiva(f, decisiones[id]) === v)) { r.remove(); m.rects.delete(id) }
    }
    const e = resumen.porVoz.get(v)
    m.svg.setAttribute('aria-label', `${rotulo(v)}: ${e ? pct(e.pct) : '0 %'} confirmado`)
  }

  /* ---------------------------------------------------------------- pintado */
  let resumen = resumir(frags, decisiones)
  let yaIdentificadas = new Set(resumen.voces.filter((e) => e.identificada).map((e) => e.voz))

  /** Repinta todo. Devuelve la voz que ACABA de llegar a la meta, si alguna. */
  function pintar() {
    resumen = resumir(frags, decisiones)
    const n = resumen.deMaquina
    caja.querySelector('.vz-global-texto').innerHTML = `Usted ha confirmado quién habla en el <strong>${pct(resumen.pct)}</strong>
      del habla transcrita (${mmss(resumen.confirmado)} de ${mmss(resumen.total)}) · <strong>${resumen.identificadas} de ${n}</strong>
      ${n === 1 ? 'voz identificada' : 'voces identificadas'}`
    const fuera = Math.max(0, (medios.duracion?.() || duracion) - resumen.total)
    caja.querySelector('.vz-fuera').textContent = fuera >= 60
      ? `${mmss(fuera)} de la grabación no tienen texto: ahí nadie ha dicho quién habla. Los tramos que conviene oír están en «Lo que no se entiende».`
      : ''
    barra(caja.querySelector('.vz-barra.grande'), resumen.pct)
    if (indicador) {
      indicador.hidden = false
      indicador.innerHTML = `<span class="vz-ind-t">Voces</span> <span class="vz-barra mini" aria-hidden="true"><i style="width:${Math.min(100, resumen.pct * 100)}%"></i></span> <span class="vz-ind-largo">${resumen.identificadas} de ${n} identificadas</span><span class="vz-ind-corto">${resumen.identificadas}/${n}</span>`
      indicador.title = `Quién habla: ${pct(resumen.pct)} del habla confirmado por usted oyendo`
    }

    const vistas = [...resumen.voces.map((e) => e.voz)]
    if (resumen.sinVoz > 0) vistas.push(null)
    for (const v of vistas) {
      const t = tarjeta(v)
      const e0 = v == null ? null : resumen.porVoz.get(v)
      const menor = v == null || (e0 && e0.total < MENOR_S && !e0.identificada)
      t.classList.toggle('menor', !!menor)
      const destino = menor ? filas : tarjetas
      if (t.parentNode !== destino) destino.appendChild(t)
      pintarTarjeta(v, t)
    }
    for (const [v, t] of tarjetaDe) if (!vistas.includes(v)) t.remove()
    const nMen = [...filas.children].filter((x) => x.dataset.voz !== '').length
    const conSinVoz = [...filas.children].some((x) => x.dataset.voz === '')
    menores.hidden = !filas.children.length
    menores.querySelector('summary').textContent = [
      nMen ? `${plural(nMen, 'voz', 'voces')} con muy poca habla (menos de ${MENOR_S} s cada una)` : '',
      conSinVoz ? `${plural(frags.filter((f) => f.maquina == null).length, 'fragmento', 'fragmentos')} sin voz asignada` : '',
    ].filter(Boolean).join(', y ')

    let recien = null
    for (const e of resumen.voces) if (e.identificada && !yaIdentificadas.has(e.voz)) recien = e
    yaIdentificadas = new Set(resumen.voces.filter((e) => e.identificada).map((e) => e.voz))
    if (recien) {
      const t = tarjetaDe.get(recien.voz)
      t?.classList.remove('recien'); void t?.offsetWidth; t?.classList.add('recien')
      avisar(`✓ ${rotulo(recien.voz)} queda identificada: ${pct(recien.pct)} confirmado oyendo.${nombres[recien.voz] ? '' : ' Ya puede escribir en su tarjeta quién es.'}`, 6000)
    }
    pintarTranscripcion()
    if (activo) pintarDock()
    return recien
  }

  function barra(el, x) {
    if (!el) return
    const i = el.querySelector('i')
    if (i) i.style.width = `${Math.min(100, x * 100)}%`
    el.classList.toggle('llega', x >= META)
    el.setAttribute?.('aria-valuenow', String(Math.floor(x * 100)))
  }

  function pintarTarjeta(v, t) {
    const e = v == null ? null : resumen.porVoz.get(v)
    t.querySelector('.vz-t-nombre').textContent = rotulo(v)
    const inp = t.querySelector('.vz-quien')
    if (inp) {
      if (document.activeElement !== inp) inp.value = nombres[v] || ''
      inp.placeholder = e?.identificada ? '¿quién es?' : '¿quién cree que es?'
      inp.title = e?.identificada ? 'Nombre y cargo: lo escribe usted'
        : 'Aún sin identificar: lo que escriba es lo que usted cree, y así se dirá'
    }
    const btn = t.querySelector('.vz-ir')
    const { pendientes, dudas } = quedan(frags, decisiones, v)
    if (v == null) {
      const n = frags.filter((f) => f.maquina == null)
      t.querySelector('.vz-pct').textContent = ''
      t.querySelector('.vz-barra').hidden = true
      t.querySelector('.vz-cuenta').textContent =
        `${plural(n.length, 'fragmento', 'fragmentos')} a los que la máquina no asignó voz · ${mmss(resumen.sinVoz)}${pendientes ? ` · ${pendientes} sin decidir` : ''}`
      btn.dataset.modo = pendientes ? 'pendientes' : 'repaso'
      btn.textContent = pendientes ? `▶ Decir de quién son · quedan ${pendientes}` : dudas ? `↻ Repasar ${dudas} sin saber` : 'Revisados todos'
      btn.disabled = !pendientes && !dudas
      pintarMapa(v)
      return
    }
    t.querySelector('.vz-pct').textContent = pct(e.pct)
    barra(t.querySelector('.vz-barra'), e.pct)
    t.classList.toggle('identificada', e.identificada)
    t.classList.toggle('anadida', e.anadida)
    t.querySelector('.vz-sello').hidden = !e.identificada
    const partes = e.anadida
      ? [`añadida por usted: ${mmss(e.confirmado)} en ${plural(e.hechos, 'fragmento', 'fragmentos')}`]
      : [`${e.hechos} de ${plural(e.frags.length, 'fragmento confirmado', 'fragmentos confirmados')}`, `${mmss(e.confirmado)} de ${mmss(e.total)}`]
    if (e.dudas) partes.push(`${e.dudas} sin saber quién`)
    const faltan = Math.max(0, META * e.total - e.confirmado)
    if (!e.anadida && !e.identificada && e.total) partes.push(`faltan ${mmss(faltan)} para el ${Math.round(META * 100)} %`)
    t.querySelector('.vz-cuenta').textContent = partes.join(' · ')
    const propios = frags.filter((f) => f.maquina === v).length
    btn.dataset.modo = pendientes ? 'pendientes' : 'repaso'
    btn.disabled = !propios || (!pendientes && !dudas)
    btn.textContent = !propios ? 'Voz añadida por usted'
      : e.hechos + e.dudas === 0 && pendientes ? '▶ Empezar'
        : pendientes ? `▶ Seguir · quedan ${pendientes}`
          : dudas ? `↻ Repasar ${dudas} sin saber` : 'Revisados todos'
    pintarMapa(v)
  }

  /* Encima de cada fragmento decidido, en la transcripción: qué dijo ella, y
     sobre qué líneas. El nombre que ella escribió solo sale aquí, sobre lo que
     ella confirmó para esa voz, con «según usted». */
  function pintarTranscripcion() {
    document.querySelectorAll('.seg.vz-decidido').forEach((n) => { n.classList.remove('vz-decidido'); n.style.removeProperty('--voz-suya') })
    for (const f of frags) {
      const n = document.getElementById(f.id)
      if (!n) continue
      let chip = n.previousElementSibling?.classList?.contains('vz-chip') ? n.previousElementSibling : null
      const d = decisiones[f.id]
      if (!d) { chip?.remove(); continue }
      if (!chip) {
        chip = document.createElement('button')
        chip.type = 'button'
        n.parentNode.insertBefore(chip, n)
        chip.addEventListener('click', (ev) => { ev.stopPropagation(); abrir(porId.get(f.id), f.maquina) })
      }
      const e = estadoDe(f, d)
      const suya = efectiva(f, coincide(d, f) ? d : null)
      chip.className = `vz-chip vz-chip-${e}`
      chip.style.setProperty('--voz', color(suya))
      const alcance = `${hms(f.inicio)}–${hms(f.fin)}`
      const maq = f.maquina == null ? 'la máquina no le asignó voz' : `la máquina decía ${rotulo(f.maquina)}`
      chip.textContent = e === 'confirmado' ? `✔ ${conNombre(f.maquina)} · confirmado por usted oyendo · ${alcance}`
        : e === 'movido' ? `↔ Según usted: ${conNombre(d.voz)} · ${maq} · ${alcance}`
          : e === 'varios' ? `? Según usted hablan varios a la vez · ${alcance}`
            : e === 'otra_version' ? `⟳ Lo decidió sobre otra versión de la transcripción: vuelva a oírlo · ${alcance}`
              : `? Usted no supo decir quién habla aquí · ${alcance}`
      chip.title = `Decidido el ${d.fecha}. Pulse para cambiarlo.`
      if (e === 'confirmado' || e === 'movido') {
        f.bloques.forEach((id) => {
          const s = document.getElementById(id)
          if (s) { s.classList.add('vz-decidido'); s.style.setProperty('--voz-suya', color(suya)) }
        })
      }
    }
  }

  /* ------------------------------------------------------------------ dock */
  const dock = document.createElement('div')
  dock.className = 'vz-dock'
  dock.hidden = true
  dock.setAttribute('role', 'region')
  dock.setAttribute('aria-label', 'Confirmar quién habla')
  dock.innerHTML = `
    <div class="envoltura vz-d-in">
      <div class="vz-d-cab">
        <span class="vz-punto" aria-hidden="true"></span>
        <strong class="vz-d-preg" tabindex="-1"></strong>
        <span class="vz-d-donde"></span>
        <button type="button" class="vz-cerrar" aria-label="Cerrar (Esc)" title="Cerrar (Esc)">×</button>
      </div>
      <p class="vz-d-texto"></p>
      <div class="vz-d-oir">
        <button type="button" class="boton vz-repetir" title="Pausa y seguir: Espacio · Desde el principio: R">▶ Oír</button>
        <div class="vz-barra oir" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-label="Oído del fragmento"><i></i><b class="vz-meta"></b></div>
        <span class="vz-d-oido"></span>
        <span class="vz-vivo" aria-live="polite"></span>
      </div>
      <div class="vz-d-botones">
        <button type="button" class="vz-b vz-si" data-a="si"><kbd>1</kbd><span></span></button>
        <button type="button" class="vz-b vz-otra" data-a="otra" aria-expanded="false"><kbd>2</kbd><span>Es otra voz…</span></button>
        <button type="button" class="vz-b vz-nose" data-a="no_se"><kbd>3</kbd><span>No sé quién es</span></button>
        <button type="button" class="vz-b vz-saltar" data-a="saltar" title="Pasar sin decidir"><kbd>→</kbd><span>Saltar</span></button>
      </div>
      <div class="vz-d-otras" hidden></div>
      <div class="vz-d-fin" hidden></div>
      <div class="vz-d-pie">
        <span class="vz-d-pie-nombre"></span>
        <div class="vz-barra vz-b-pie" aria-hidden="true"><i></i><b class="vz-meta"></b></div>
        <span class="vz-d-pie-pct"></span>
      </div>
    </div>`
  document.body.appendChild(dock)
  const $d = (s) => dock.querySelector(s)

  const oido = crearOido(medios)
  let activo = null          // el fragmento que se pregunta
  let vozEnCurso = undefined // la voz que se está recorriendo
  let modo = 'pendientes'
  let enFin = false
  let relojAvance = null
  let focoPrevio = null
  let puedeAntes = null
  let sonandoVisto = null
  const saltados = new Set()
  const vistos = new Set()
  const ultimoVisto = new Map()

  const tramoDe = (f) => ({ id: f.id, desde: f.inicio, hasta: f.fin, zonas: f.zonas })

  function empezar(v, m = 'pendientes') {
    vozEnCurso = v
    modo = m
    if (m === 'repaso') vistos.clear()
    const f = siguiente(frags, decisiones, v, ultimoVisto.get(v) || null, { modo: m, saltados, vistos })
      || siguiente(frags, decisiones, v, null, { modo: m, saltados, vistos })
    if (f) abrir(f, v)
    else { mostrarDock(); pantallaFinal() }
  }

  function mostrarDock() {
    if (dock.hidden) focoPrevio = document.activeElement
    anunciarPanel('voces')
    dock.hidden = false
    document.body.classList.add('con-dock')
    ajustarMargenes()
  }

  function abrir(f, v = f?.maquina) {
    if (!f) return
    clearTimeout(relojAvance)
    mostrarDock()
    activo = f
    enFin = false
    vozEnCurso = v
    ultimoVisto.set(v, f.id)
    if (modo === 'repaso') vistos.add(f.id)
    oido.abrir(tramoDe(f))
    puedeAntes = null
    sonandoVisto = null
    alternarOtras(false)
    $d('.vz-d-fin').hidden = true
    $d('.vz-d-botones').hidden = false
    $d('.vz-d-oir').hidden = false
    $d('.vz-d-texto').hidden = false
    $d('.vz-d-donde').hidden = false
    document.querySelectorAll('.seg.vz-activo').forEach((n) => n.classList.remove('vz-activo'))
    f.bloques.forEach((id) => document.getElementById(id)?.classList.add('vz-activo'))
    enfocar(f.id)
    pintarDock()
    oido.oir()
    pintar()
    $d('.vz-d-preg').focus({ preventScroll: true })
  }

  function cerrar() {
    clearTimeout(relojAvance)
    oido.cerrar()
    activo = null
    enFin = false
    dock.hidden = true
    if (!document.querySelector('.vz-dock:not([hidden])')) document.body.classList.remove('con-dock')
    document.querySelectorAll('.seg.vz-activo').forEach((n) => n.classList.remove('vz-activo'))
    ajustarMargenes()
    pintar()
    if (focoPrevio && document.contains(focoPrevio)) focoPrevio.focus({ preventScroll: true })
  }

  /* Que lo que suena quede en la franja libre: entre la barra fija de arriba
     y este panel de abajo. */
  function ajustarMargenes() {
    const arriba = (() => { const b = document.getElementById('barra'); return b && getComputedStyle(b).position === 'sticky' ? b.getBoundingClientRect().height : 0 })()
    const abajo = document.querySelector('.vz-dock:not([hidden])')?.getBoundingClientRect().height || 0
    document.documentElement.style.scrollPaddingTop = `${Math.round(arriba + 8)}px`
    document.documentElement.style.scrollPaddingBottom = `${Math.round(abajo + 8)}px`
  }
  window.addEventListener('resize', () => { if (!dock.hidden) ajustarMargenes() })

  function pintarDock() {
    if (!activo || enFin) return
    const f = activo
    const d = decisiones[f.id]
    const v = f.maquina
    dock.style.setProperty('--voz', color(v))
    const deVoz = frags.filter((x) => x.maquina === v)
    $d('.vz-d-preg').innerHTML = v == null
      ? '¿Quién habla aquí? <span class="vz-d-sub">La máquina no le asignó voz.</span>'
      : `¿Es <strong>${esc(conNombre(v))}</strong> quien habla aquí?`
    $d('.vz-d-donde').textContent = `${hms(f.inicio)} · ${mmss(f.fin - f.inicio)} · fragmento ${deVoz.indexOf(f) + 1} de los ${deVoz.length} que la máquina le asignó`
    const texto = f.bloques.map((id) => textoTranscrito(document.getElementById(id)?.querySelector('.texto'))).join(' ')
    $d('.vz-d-texto').textContent = texto ? `«${texto}»` : ''
    const si = $d('.vz-si')
    si.hidden = v == null
    si.querySelector('span').textContent = `Sí, es ${rotulo(v)}`
    $d('.vz-otra span').textContent = v == null ? 'Elegir la voz…' : 'Es otra voz…'
    dock.querySelectorAll('.vz-b').forEach((b) => b.classList.remove('elegido'))
    if (d && coincide(d, f)) {
      const sel = d.decision === 'si' ? '.vz-si' : d.decision === 'otra' ? '.vz-otra' : '.vz-nose'
      $d(sel)?.classList.add('elegido')
    }
    pintarOido()
    const e = v == null ? null : resumen.porVoz.get(v)
    $d('.vz-d-pie').hidden = !e
    if (e) {
      $d('.vz-d-pie-nombre').textContent = conNombre(v)
      barra($d('.vz-barra.vz-b-pie'), e.pct)
      $d('.vz-d-pie-pct').textContent = `${pct(e.pct)} confirmado · meta ${Math.round(META * 100)} %${e.identificada ? ' · ✓ identificada' : ''}`
    }
  }

  /* Lo que cambia mientras suena: solo esto se repinta a cada instante. Rehacer
     los botones cuatro veces por segundo se come los clics. */
  function pintarOido() {
    if (!activo || enFin) return
    const d = decisiones[activo.id]
    const fr = oido.fraccion()
    const puede = medios.listo && fr >= OIDA_MINIMA
    barra($d('.vz-barra.oir'), fr)
    $d('.vz-barra.oir').classList.toggle('llega', fr >= OIDA_MINIMA)
    const txt = !medios.listo
      ? 'No se encontró la grabación: sin oírlo no se puede confirmar.'
      : puede ? (d && coincide(d, activo) ? `Oído. Ya lo decidió el ${d.fecha}: puede cambiarlo.` : 'Oído. Decida.')
        : `Oyendo… ${Math.floor(fr * 100)} % del habla — al ${Math.round(OIDA_MINIMA * 100)} % puede decidir`
    const o = $d('.vz-d-oido')
    if (o.textContent !== txt) o.textContent = txt
    if (puede !== puedeAntes) {
      dock.querySelectorAll('.vz-si, .vz-otra, .vz-nose').forEach((b) => { b.disabled = !puede })
      $d('.vz-d-otras').classList.toggle('bloqueado', !puede)
      // Al lector de pantalla, solo los cambios de estado, no cada punto de porcentaje.
      $d('.vz-vivo').textContent = puede ? 'Oído. Puede decidir.' : 'Suena el fragmento.'
      if (puede && puedeAntes === false) { dock.classList.remove('listo'); void dock.offsetWidth; dock.classList.add('listo') }
      puedeAntes = puede
    }
    const rep = oido.sonandoAqui ? '❚❚ Pausa' : oido.pausadoAMitad ? '▶ Seguir oyendo' : fr > 0 ? '↻ Oír otra vez' : '▶ Oír'
    const r = $d('.vz-repetir')
    if (r.textContent !== rep) r.textContent = rep
  }

  /* «Es otra voz»: con la lista abierta, la fila de Sí / Otra / No sé se
     esconde, y las voces se eligen con LETRAS. Con números, «3» pensando en
     «No sé» guardaba «es el Hablante 3». */
  function pintarOtras() {
    const caja2 = $d('.vz-d-otras')
    const v = activo?.maquina
    const candidatas = [...orden, ...nuevas()].filter((x) => x !== v)
    caja2.innerHTML = `<p class="vz-d-otras-t">¿De quién es entonces? Elija con la letra o con el ratón.
      <button type="button" class="vz-volver">← Volver (Esc)</button></p>`
    candidatas.forEach((x, i) => {
      const b = document.createElement('button')
      b.type = 'button'
      b.className = 'vz-voz'
      b.dataset.voz = x
      if (i < LETRAS.length) b.dataset.letra = LETRAS[i]
      b.style.setProperty('--voz', color(x))
      b.innerHTML = `${i < LETRAS.length ? `<kbd>${LETRAS[i]}</kbd>` : ''}<span class="vz-punto"></span>${esc(conNombre(x))}`
      b.addEventListener('click', () => decidir('otra', x))
      caja2.appendChild(b)
    })
    const nueva = document.createElement('button')
    nueva.type = 'button'; nueva.className = 'vz-voz vz-voz-nueva'
    nueva.innerHTML = '<kbd>0</kbd>Una voz que no está en la lista'
    nueva.addEventListener('click', () => decidir('otra', `nueva-${numeroNuevo()}`))
    const varios = document.createElement('button')
    varios.type = 'button'; varios.className = 'vz-voz vz-voz-varios'
    varios.innerHTML = '<kbd>9</kbd>Hablan varios a la vez'
    varios.addEventListener('click', () => decidir('varios'))
    caja2.append(nueva, varios)
    caja2.querySelector('.vz-volver').addEventListener('click', () => alternarOtras(false))
  }

  function alternarOtras(abrirlas) {
    const c = $d('.vz-d-otras')
    const ab = abrirlas ?? c.hidden
    c.hidden = !ab
    $d('.vz-d-botones').hidden = ab
    $d('.vz-otra').setAttribute('aria-expanded', String(ab))
    if (ab) pintarOtras()
    ajustarMargenes()
  }

  function decidir(decision, voz) {
    if (!activo || enFin || !medios.listo) return
    if (oido.fraccion() < OIDA_MINIMA) {
      avisar(`Óigalo al menos hasta el ${Math.round(OIDA_MINIMA * 100)} % para decidir.`)
      return
    }
    const f = activo
    decisiones[f.id] = {
      decision,
      ...(decision === 'si' ? { voz: f.maquina } : {}),
      ...(decision === 'otra' ? { voz } : {}),
      maquina: f.maquina,
      firma: firma(f),
      oido: Math.floor(oido.fraccion() * 100) / 100,
      fecha: hoy(),
      cuando: new Date().toISOString(),
    }
    saltados.delete(f.id)
    guardar()
    const recien = pintar()
    dock.classList.remove('guardado'); void dock.offsetWidth; dock.classList.add('guardado')
    if (!recien) {
      const e = f.maquina == null ? null : resumen.porVoz.get(f.maquina)
      const que = decision === 'si' ? `es ${rotulo(f.maquina)}` : decision === 'otra' ? `según usted es ${conNombre(voz)}`
        : decision === 'varios' ? 'hablan varios' : 'no sabe quién es'
      avisar(`Guardado: ${que}${e ? ` · ${rotulo(f.maquina)}: ${pct(e.pct)}` : ''}`)
    }
    clearTimeout(relojAvance)
    relojAvance = setTimeout(() => { if (activo?.id === f.id) avanzar(f.id) }, 420)
  }

  function avanzar(desde) {
    if (!activo) return
    const sig = siguiente(frags, decisiones, vozEnCurso, desde, { modo, saltados, vistos })
    if (sig && sig.id !== desde) { abrir(sig, vozEnCurso); return }
    pantallaFinal()
  }

  /* Ya no queda nada que preguntar de esta voz en esta pasada. */
  function pantallaFinal() {
    oido.cerrar()
    enFin = true
    activo = null
    document.querySelectorAll('.seg.vz-activo').forEach((n) => n.classList.remove('vz-activo'))
    resumen = resumir(frags, decisiones)
    const v = vozEnCurso
    const e = v == null ? null : resumen.porVoz.get(v)
    const { pendientes, dudas } = quedan(frags, decisiones, v)
    const otra = resumen.voces.find((x) => !x.identificada && !x.anadida && x.voz !== v && quedan(frags, decisiones, x.voz).pendientes)
    dock.style.setProperty('--voz', color(v))
    $d('.vz-d-preg').textContent = `${rotulo(v)}: terminado por ahora`
    ;['.vz-d-botones', '.vz-d-oir', '.vz-d-otras', '.vz-d-texto', '.vz-d-donde'].forEach((s) => { $d(s).hidden = true })
    const fin = $d('.vz-d-fin')
    fin.hidden = false
    const partes = []
    if (e) partes.push(e.identificada ? `<strong>Queda identificada:</strong> ${pct(e.pct)} confirmado oyendo.` : `Lleva <strong>${pct(e.pct)} confirmado</strong>; la meta es el ${Math.round(META * 100)} %.`)
    if (pendientes) partes.push(`Quedan <strong>${plural(pendientes, 'fragmento que saltó', 'fragmentos que saltó')} sin decidir</strong>.`)
    if (dudas) partes.push(`<strong>${plural(dudas, 'fragmento quedó', 'fragmentos quedaron')}</strong> en «no sé» o «varios»: se pueden repasar.`)
    fin.innerHTML = `<p>${partes.join(' ') || 'No queda nada que preguntar.'}</p>`
    const botones = []
    if (pendientes) botones.push(['▶ Volver a los que saltó', () => { saltados.clear(); empezar(v, 'pendientes') }])
    if (dudas) botones.push([`↻ Repasar ${dudas} sin saber`, () => empezar(v, 'repaso')])
    if (otra) botones.push([`▶ Seguir con ${conNombre(otra.voz)}`, () => empezar(otra.voz, 'pendientes')])
    botones.forEach(([txt, fn], i) => {
      const b = document.createElement('button')
      b.type = 'button'; b.className = 'boton' + (i === botones.length - 1 ? ' primaria' : '')
      b.textContent = txt
      b.addEventListener('click', fn)
      fin.appendChild(b)
    })
    const c = document.createElement('button')
    c.type = 'button'; c.className = 'boton'; c.textContent = 'Cerrar (Esc)'
    c.addEventListener('click', cerrar)
    fin.appendChild(c)
    const pista = document.createElement('p')
    pista.className = 'vz-d-pista'
    pista.textContent = 'Intro o V: el botón resaltado · Esc: cerrar'
    fin.appendChild(pista)
    $d('.vz-d-pie').hidden = !e
    if (e) {
      $d('.vz-d-pie-nombre').textContent = conNombre(v)
      barra($d('.vz-barra.vz-b-pie'), e.pct)
      $d('.vz-d-pie-pct').textContent = `${pct(e.pct)} confirmado · meta ${Math.round(META * 100)} %${e.identificada ? ' · ✓ identificada' : ''}`
    }
    ajustarMargenes()
    ;(fin.querySelector('.boton.primaria') || c).focus()
    pintar()
  }

  dock.addEventListener('click', (ev) => {
    const b = ev.target.closest('button')
    if (!b || !dock.contains(b)) return
    if (b.classList.contains('vz-cerrar')) return cerrar()
    if (b.classList.contains('vz-repetir')) return oido.alternar()
    const a = b.dataset.a
    if (a === 'si') return decidir('si')
    if (a === 'no_se') return decidir('no_se')
    if (a === 'otra') return alternarOtras(true)
    if (a === 'saltar' && activo) { saltados.add(activo.id); return avanzar(activo.id) }
  })

  /* Con el panel abierto, las teclas son del panel. Van en captura para que
     no las tome antes el teclado general de la página, y las de la página
     que no son del panel se quedan quietas. */
  document.addEventListener('keydown', (ev) => {
    if (dock.hidden) return
    if (document.querySelector('dialog[open]')) return
    if (ev.ctrlKey || ev.metaKey || ev.altKey) return
    const a = document.activeElement
    if (a && (ESCRIBIENDO.has(a.tagName) || a.isContentEditable)) return
    const k = ev.key
    const otras = !$d('.vz-d-otras').hidden
    let hecho = true
    if (k === 'Escape') { otras ? alternarOtras(false) : cerrar() }
    else if (enFin) {
      if (k === 'v' || k === 'V') { const p = $d('.vz-d-fin .boton.primaria'); p ? p.click() : cerrar() }
      else if (k === 'Enter' || k === ' ' || k === 'Tab') hecho = false   // el botón con foco
      else if (!TECLAS_DE_LA_PAGINA.has(k)) hecho = false
    }
    else if (k === ' ') oido.alternar()
    else if (otras) {
      if (k === '0') $d('.vz-voz-nueva')?.click()
      else if (k === '9') $d('.vz-voz-varios')?.click()
      else if (k === '2') alternarOtras(false)
      else if (/^[a-z]$/i.test(k) && $d(`.vz-voz[data-letra="${k.toLowerCase()}"]`)) $d(`.vz-voz[data-letra="${k.toLowerCase()}"]`).click()
      else if (!TECLAS_DE_LA_PAGINA.has(k)) hecho = false
    }
    else if (k === '1' && activo?.maquina != null) decidir('si')
    else if (k === '2') alternarOtras(true)
    else if (k === '3') decidir('no_se')
    else if (k === 'r' || k === 'R') oido.oir()
    else if (k === 'ArrowRight' && activo) { saltados.add(activo.id); avanzar(activo.id) }
    else if (TECLAS_DE_LA_PAGINA.has(k)) avisar('Con la pregunta abierta: 1 Sí · 2 Otra voz · 3 No sé · Espacio pausa · R desde el principio · Esc cerrar')
    else hecho = false
    if (hecho) { ev.preventDefault(); ev.stopImmediatePropagation() }
  }, true)
  alAbrirOtro('voces', () => { if (!dock.hidden) cerrar() })

  /* --------------------------------------------------------------- avisos */
  const toast = document.createElement('div')
  toast.className = 'vz-toast'
  toast.setAttribute('role', 'status')
  toast.hidden = true
  document.body.appendChild(toast)
  let relojToast = null
  function avisar(t, ms = 2800) {
    toast.textContent = t
    toast.hidden = false
    toast.classList.remove('sale'); void toast.offsetWidth; toast.classList.add('sale')
    clearTimeout(relojToast)
    relojToast = setTimeout(() => { toast.hidden = true }, ms)
  }

  pintar()

  return {
    avisar,
    /** Lo llama la página en cada instante del audio. */
    alTiempo(t) {
      for (const [v, m] of mapas) {
        m.cabeza.setAttribute('x', t)
        m.cabeza.setAttribute('visibility', activo && (activo.maquina === v) ? 'visible' : 'hidden')
      }
      if (!oido.alTiempo(t) || !activo) return
      pintarOido()
      // La línea que suena, a la vista, si es de este fragmento.
      const s = document.querySelector('.seg.sonando')
      if (s && s.id !== sonandoVisto && activo.bloques.includes(s.id)) {
        sonandoVisto = s.id
        s.scrollIntoView({ block: 'nearest', behavior: 'smooth' })
      }
    },
    alEstado() { if (activo) pintarOido() },
    /** Seguir donde lo dejó: la voz de la máquina con más por hacer. */
    seguir() {
      if (enFin) { const p = $d('.vz-d-fin .boton.primaria'); if (p) { p.click(); return } }
      if (activo) return
      const conPend = (e) => quedan(frags, decisiones, e.voz).pendientes
      const v = resumen.voces.find((e) => !e.anadida && !e.identificada && conPend(e))
        || resumen.voces.find((e) => !e.anadida && conPend(e))
      if (v) return empezar(v.voz, 'pendientes')
      if (quedan(frags, decisiones, null).pendientes) return empezar(null, 'pendientes')
      const dudas = [...maquina, null].reduce((s, x) => s + quedan(frags, decisiones, x).dudas, 0)
      avisar(dudas
        ? `No queda nada sin decidir. ${plural(dudas, 'fragmento está', 'fragmentos están')} en «no sé» o «varios»: repáselos desde la tarjeta de cada voz.`
        : 'No queda nada por confirmar: todo está decidido.', 5000)
    },
    cifra() { return `${resumen.identificadas}/${resumen.deMaquina}` },
    lista() {
      return [...orden, ...nuevas()].map((v) => ({ voz: v, rotulo: conNombre(v), color: color(v) }))
    },
    rotulo(v) {
      if (v === 'nueva') return 'una voz que no está en la lista'
      if (v === 'no_se') return 'no sabe quién'
      return conNombre(v)
    },
    paraGuardar() {
      const r = resumir(frags, decisiones)
      return {
        voces: nombres,
        atribucion: decisiones,
        resumen_voces: Object.fromEntries(r.voces.map((e) => [e.voz,
          { confirmado: Math.floor(e.pct * 1000) / 1000, identificada: e.identificada, anadida_por_usted: e.anadida,
            segundos_confirmados: Math.floor(e.confirmado), segundos: Math.floor(e.total) }])),
      }
    },
    /** Lo que trae un archivo: el archivo es la fuente. Si no trae quién habla,
     *  lo de este navegador no se queda fingiendo estar guardado. */
    cargar(doc) {
      if (!doc?.clave || doc.clave !== C.clave) {
        avisar('Ese archivo es de otra versión de esta transcripción: «quién habla» no se ha cargado.', 6000)
        return { voces: 0, nombres: 0, cargado: false }
      }
      nombres = doc.voces && typeof doc.voces === 'object' ? { ...doc.voces } : {}
      guardarNombres()
      decisiones = depurar(doc.atribucion || {})
      try { localStorage.setItem(LLAVE, JSON.stringify(decisiones)) } catch {}
      pintar()
      return { voces: Object.keys(decisiones).length, nombres: Object.values(nombres).filter((x) => (x || '').trim()).length, cargado: true }
    },
    /** ¿Hay algo en este navegador? (para avisar antes de cargar encima) */
    get cuantos() { return Object.keys(decisiones).length + Object.values(nombres).filter((x) => (x || '').trim()).length },
  }
}
