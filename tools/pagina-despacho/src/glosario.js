/* Glosario — lo que la máquina oye mal, y lo que de verdad se dijo.
 *
 * La máquina escribe un nombre de lugar por otro que suena parecido, o una
 * sigla por otra. Ella lo anota una vez y la página lo marca en toda la transcripción,
 * con lo que se dijo al lado. El texto transcrito NO cambia: lo suyo se pinta
 * encima (con CSS, fuera del texto: copiar una línea da la transcripción tal
 * cual), marcado como suyo. Vale para todas las grabaciones del caso.
 *
 * Las sugerencias que trae la página son hipótesis de la máquina (nadie las ha
 * oído): se ven aparte, y solo cuentan si ella las acepta.
 *
 * Lo que se guarda (localStorage y el archivo de «Guardar lo comprobado»,
 * bajo `glosario`), una entrada por regla:
 *   { id, oye, dijo, nota, origen, estado: 'aceptada' | 'rechazada', fecha, cuando,
 *     de?, nota_maquina?, excepciones: [{ pagina, linea, minuto, fecha, cuando, oido }] }
 * `de` es la sugerencia decidida, por su contenido; `nota` es solo de ella y lo
 * que decía la máquina va en `nota_maquina`; `cuando` es el último cambio.
 */
import { resaltar } from './resalte.js'

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]))
const hoy = () => new Date().toLocaleDateString('es-CO', { year: 'numeric', month: '2-digit', day: '2-digit' })
const ahora = () => new Date().toISOString()
const nuevoId = () => 'u' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6)

/** Para buscar: sin mayúsculas, pero CON tildes. Si se quitaran, «Popayan →
 *  Popayán» marcaría también las líneas que ya dicen «Popayán» bien escrito. */
export const plano = (s) => String(s || '').normalize('NFC').toLowerCase()
const mismaOye = (a, b) => plano(a).trim() === plano(b).trim()
const esLetra = (c) => /[\p{L}\p{N}\p{M}]/u.test(c || '')

/** El texto listo para buscar y, por cada carácter, de dónde viene en el
 *  original. Se prepara por grupos (una letra con sus tildes sueltas): una
 *  línea en NFD o con «İ» ya no descuadra las posiciones del resto. */
export function preparar(texto) {
  const s = String(texto ?? '')
  const ini = [], fin = []
  let t = '', k = 0
  for (const g of s.match(/\P{M}\p{M}*|\p{M}+/gu) || []) {
    const p = plano(g)
    for (let j = 0; j < p.length; j++) { ini.push(k); fin.push(k + g.length) }
    t += p
    k += g.length
  }
  return { t, ini, fin }
}

function buscar({ t, ini, fin }, oye) {
  const o = plano(oye).trim()
  const out = []
  if (!o) return out
  const borde = (j) => j === 0 || j === t.length || ini[j] !== ini[j - 1]
  let i = t.indexOf(o)
  while (i >= 0) {
    const j = i + o.length
    if (borde(i) && borde(j) && !esLetra(t[i - 1]) && !esLetra(t[j])) out.push([ini[i], fin[j - 1]])
    i = t.indexOf(o, i + 1)
  }
  return out
}

/** Dónde aparece `oye` en `texto`, como palabra o frase entera: [[inicio, fin]]
 *  en posiciones del texto original. */
export const apariciones = (texto, oye) => buscar(preparar(texto), oye)

/** Una sugerencia se reconoce por lo que dice, no por su sitio en la lista: si
 *  la lista cambia entre entregas, la decisión de ella sigue con la suya. */
export const idSug = (oye, dijo) => 's:' + plano(oye).trim() + '→' + String(dijo ?? '').trim()

/** Cuándo se hizo o cambió una entrada, para comparar: `cuando` o, en las
 *  antiguas, el día de `fecha` (dd/mm/aaaa). Sin nada, 0. */
export function momento(x) {
  const t = Date.parse(x?.cuando || '')
  if (!Number.isNaN(t)) return t
  const m = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/.exec(String(x?.fecha || '').trim())
  return m ? Date.UTC(+m[3], +m[2] - 1, +m[1]) : 0
}

/** ¿Esta regla está exceptuada en esta línea de esta página? */
export const exceptuada = (r, pagina, linea) =>
  (r?.excepciones || []).some((e) => e?.pagina === pagina && e?.linea === linea)

/** Pone al día lo guardado por versiones anteriores de la página. Las
 *  excepciones antiguas (solo el id de la línea) se quitan y se cuentan: se
 *  hicieron sin oír la línea y sin decir de qué grabación eran. */
export function normalizar(lista) {
  let quitadas = 0
  const out = (Array.isArray(lista) ? lista : [])
    .filter((x) => x && typeof x === 'object' && String(x.oye || '').trim() && String(x.dijo || '').trim())
    .map((x) => {
      const y = { ...x }
      if (typeof y.de === 'string' && /^s\d+$/.test(y.de)) y.de = idSug(y.oye, y.dijo)
      // Antes, al aceptar una sugerencia, la nota de la máquina se guardaba como de ella.
      if (y.de && !('nota_maquina' in y)) { y.nota_maquina = y.nota || ''; y.nota = '' }
      const exc = Array.isArray(y.excepciones) ? y.excepciones : []
      const buenas = exc.filter((e) => e && typeof e === 'object' && e.pagina && e.linea)
      quitadas += exc.length - buenas.length
      if (y.estado !== 'rechazada' || 'excepciones' in y) y.excepciones = buenas
      return y
    })
  return { lista: out, quitadas }
}

/** Dos entradas que no pueden estar a la vez: la misma, la decisión sobre una
 *  misma sugerencia, o dos reglas en vigor para lo mismo que se oye. */
const chocan = (x, y) => (!!x.id && x.id === y.id) || (!!x.de && x.de === y.de)
  || (x.estado === 'aceptada' && y.estado === 'aceptada' && mismaOye(x.oye, y.oye))

/** Lo de este navegador y lo de un archivo, juntos. Donde chocan se queda la
 *  más reciente; a igual fecha, la del archivo, que es lo que ella pidió
 *  cargar. El glosario es del caso: cargar el archivo de una grabación no
 *  borra lo anotado en las otras. */
export function fusionar(locales, traidas) {
  const todas = [...traidas.map((x) => [x, 0]), ...locales.map((x) => [x, 1])]
    .sort(([a, p], [b, q]) => momento(b) - momento(a) || p - q)
  const quedan = new Set()
  for (const [x] of todas) if (![...quedan].some((y) => chocan(x, y))) quedan.add(x)
  return [...locales, ...traidas].filter((x) => quedan.has(x))
}

/**
 * `oirLinea` ({ oir(b), oida(b), sonandoEn?(b), fraccion?(b) }) hace sonar una
 * línea sola y dice si ya la oyó; sin él no se puede exceptuar ninguna línea.
 * `bloqueDe(id)` da el bloque del contrato de una línea.
 */
export function montarGlosario({ C, caja, avisar, alIrA, oirLinea, bloqueDe }) {
  if (!caja) return null
  const LLAVE = 'despacho:glosario:' + (C.caso || C.clave)
  const PAGINA = C.clave
  const crudo = () => { try { return JSON.parse(localStorage.getItem(LLAVE) || '[]') } catch { return [] } }
  const escribir = () => { try { localStorage.setItem(LLAVE, JSON.stringify(suyas)) } catch {} }
  let alCambiar = null, abrirPestana = null
  const guardar = () => { escribir(); alCambiar?.() }

  const inicial = crudo()
  let { lista: suyas, quitadas } = normalizar(inicial)
  if (JSON.stringify(suyas) !== JSON.stringify(inicial)) escribir()
  if (quitadas) {
    setTimeout(() => avisar?.(quitadas === 1
      ? 'Glosario: se quitó 1 línea exceptuada de antes, hecha sin oírla y sin saber de qué grabación era. Si era buena, vuelva a hacerla oyendo la línea.'
      : `Glosario: se quitaron ${quitadas} líneas exceptuadas de antes, hechas sin oírlas y sin saber de qué grabación eran. Si alguna era buena, vuelva a hacerla oyendo la línea.`, 9000), 0)
  }
  window.addEventListener('storage', (e) => { if (e.key === LLAVE) { suyas = normalizar(crudo()).lista; pintar() } })

  const sugeridas = []
  for (const s of C.glosario || []) {
    if (!String(s?.oye || '').trim() || !String(s?.dijo || '').trim()) continue
    const id = idSug(s.oye, s.dijo)
    if (!sugeridas.some((x) => x.id === id)) sugeridas.push({ id, oye: s.oye, dijo: s.dijo, nota: s.nota || '' })
  }
  const decididaSug = (s) => suyas.find((x) => x.de === s.id)
  const aceptadas = () => suyas.filter((x) => x.estado === 'aceptada')

  caja.hidden = false
  caja.classList.add('vz', 'gl')
  caja.innerHTML = `
    <div class="vz-cab"><div class="vz-cab-texto">
      <h2>Glosario <span class="vz-sub">lo que la máquina oye mal, y lo que se dijo</span></h2>
      <p class="vz-global-texto">Anote aquí lo que la transcripción escribe mal y lo que de verdad se dijo. <strong>La transcripción
        no cambia</strong>: lo suyo se ve al lado de cada aparición, marcado como suyo, y no entra al copiar. Vale para todas las grabaciones del caso.
        También puede <strong>seleccionar una palabra</strong> en la transcripción y pulsar «Al glosario».</p>
    </div></div>
    <form class="gl-form">
      <label>La transcripción dice <input name="oye" required placeholder="lo que escribió la máquina" autocomplete="off"></label>
      <span class="gl-flecha" aria-hidden="true">→</span>
      <label>Se dijo <input name="dijo" required placeholder="lo que de verdad se dijo" autocomplete="off"></label>
      <label class="gl-nota">Nota <input name="nota" placeholder="opcional: cómo lo sabe" autocomplete="off"></label>
      <button type="submit" class="boton primaria">Añadir</button>
      <span class="gl-cuenta" aria-live="polite"></span>
    </form>
    <h3 class="gl-t">Suyas <span class="vz-sub">las que anotó usted y las sugerencias que aceptó</span></h3>
    <ul class="gl-lista gl-suyas"></ul>
    <h3 class="gl-t gl-t-sug">Sugerencias <span class="vz-sub">hipótesis de la máquina: nadie las ha oído. Acéptelas solo si está segura.</span></h3>
    <ul class="gl-lista gl-sugeridas"></ul>`
  const form = caja.querySelector('.gl-form')
  const cuenta = caja.querySelector('.gl-cuenta')

  const lineas = () => [...document.querySelectorAll('#contenido .seg .texto')]
  /** Los trozos de texto de una línea, sin nada de lo que pone el glosario. */
  function nodosDe(t) {
    const out = []
    const w = document.createTreeWalker(t, NodeFilter.SHOW_TEXT)
    while (w.nextNode()) if (!w.currentNode.parentElement?.closest('.gl-dijo')) out.push(w.currentNode)
    return out
  }
  /** Antes de añadir: dónde saldría marcado, con la misma búsqueda que al marcar. */
  const cuantasHabria = (oye) => lineas().reduce((n, t) => n + apariciones(nodosDe(t).map((x) => x.data).join(''), oye).length, 0)
  /** Lo que se cuenta es lo marcado de verdad en esta página. */
  let cuentas = new Map()
  const marcasDe = (id) => [...document.querySelectorAll('#contenido mark.gl:not(.gl-sigue)')].filter((m) => m.dataset.regla === id)

  form.addEventListener('input', () => {
    const o = form.oye.value.trim()
    const n = o ? cuantasHabria(o) : 0
    cuenta.textContent = o ? `aparece ${n} ${n === 1 ? 'vez' : 'veces'} en esta grabación` : ''
  })

  /** Una regla en vigor por cada cosa que se oye: la nueva sustituye a la
   *  anterior y se queda con las líneas que ella exceptuó oyéndolas. */
  function poner(x) {
    const previas = suyas.filter((y) => y.estado === 'aceptada' && mismaOye(y.oye, x.oye))
    const exc = [...(x.excepciones || [])]
    for (const e of previas.flatMap((y) => y.excepciones || [])) {
      if (!exc.some((f) => f.pagina === e.pagina && f.linea === e.linea)) exc.push(e)
    }
    suyas = [...suyas.filter((y) => !previas.includes(y)), { ...x, excepciones: exc }]
    return previas
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault()
    const oye = form.oye.value.trim(), dijo = form.dijo.value.trim()
    if (!oye || !dijo) return
    const id = nuevoId()
    const previas = poner({ id, oye, dijo, nota: form.nota.value.trim(), origen: 'usted', estado: 'aceptada', excepciones: [], fecha: hoy(), cuando: ahora() })
    form.reset()
    cuenta.textContent = ''
    guardar(); pintar()
    const n = cuentas.get(id) || 0
    avisar?.(`Al glosario: «${oye}» → «${dijo}». Marcado en ${n} ${n === 1 ? 'sitio' : 'sitios'} de esta grabación.`
      + (previas.length ? ` Sustituye a «${previas[0].oye}» → «${previas[0].dijo}».` : ''))
    volver()
  })

  /** Quitar una regla se lleva las líneas que ella exceptuó oyéndolas: se avisa. */
  function quitar(x) {
    const n = (x.excepciones || []).length
    if (n && !confirm(`En ${n} ${n === 1 ? 'línea' : 'líneas'} usted dijo, oyéndola, que sí se dijo «${x.oye}». Eso también se quita.\n\n¿Quitar «${x.oye}» → «${x.dijo}» del glosario?`)) return
    suyas = suyas.filter((y) => y !== x)
    guardar(); pintar()
  }

  function quitarExcepcion(r, e) {
    r.excepciones = (r.excepciones || []).filter((f) => f !== e)
    r.cuando = ahora()
    guardar(); pintar()
    avisar?.(`El glosario vuelve a aplicarse en la línea ${e.minuto || ''}.`)
  }

  const nuevaFila = (clase, html) => {
    const li = document.createElement('li')
    li.className = clase
    li.innerHTML = html + '<span class="gl-acc"></span>'
    const acc = li.querySelector('.gl-acc')
    const boton = (t, fn, cl = 'boton tenue') => {
      const b = document.createElement('button')
      b.type = 'button'; b.className = cl; b.textContent = t
      b.addEventListener('click', fn)
      acc.appendChild(b)
    }
    return { li, boton }
  }
  const par = (x) => `<span class="gl-oye">«${esc(x.oye)}»</span><span class="gl-flecha">→</span><span class="gl-dijo-t">«${esc(x.dijo)}»</span>`
  const veces = (n) => `<span class="gl-n">${n} ${n === 1 ? 'vez' : 'veces'}</span>`

  /* Suyas: las que anotó ella y las sugerencias que aceptó, cada una diciendo de dónde viene. */
  function filaSuya(x) {
    const n = cuentas.get(x.id) || 0
    const { li, boton } = nuevaFila('gl-fila aceptada', par(x) + veces(n)
      + `<span class="gl-origen">${x.de ? 'sugerencia aceptada por usted' : 'anotada por usted'}${x.fecha ? ' el ' + esc(x.fecha) : ''}</span>`
      + (x.nota ? `<span class="gl-nota-t">${resaltar(x.nota)}</span>` : '')
      + (x.nota_maquina ? `<span class="gl-nota-maq">La máquina decía: ${resaltar(x.nota_maquina)}</span>` : ''))
    if (n) boton('Ver dónde', () => irA(x.id, x.oye))
    if (x.de) boton('Deshacer', () => quitar(x))
    else boton('Quitar', () => quitar(x))
    const aqui = (x.excepciones || []).filter((e) => e.pagina === PAGINA)
    const fuera = (x.excepciones || []).length - aqui.length
    if (aqui.length || fuera) {
      const ul = document.createElement('ul')
      ul.className = 'gl-excs'
      for (const e of aqui) {
        const i = document.createElement('li')
        i.innerHTML = `No se aplica en la línea <strong>${esc(e.minuto || e.linea)}</strong>: según usted, ahí sí se dijo «${esc(x.oye)}»`
          + `${e.fecha ? ` (la oyó el ${esc(e.fecha)})` : ''}. `
        for (const [t, fn] of [['Ver', () => alIrA?.(e.linea)], ['Deshacer', () => quitarExcepcion(x, e)]]) {
          const b = document.createElement('button')
          b.type = 'button'; b.className = 'boton tenue'; b.textContent = t
          b.addEventListener('click', fn)
          i.appendChild(b)
        }
        ul.appendChild(i)
      }
      if (fuera) ul.appendChild(Object.assign(document.createElement('li'),
        { textContent: `Y en ${fuera} ${fuera === 1 ? 'línea' : 'líneas'} de otras grabaciones del caso.` }))
      li.appendChild(ul)
    }
    return li
  }

  /* Sugerencias: las que esperan decisión y las que ella no aceptó. */
  function filaSug(s, d) {
    const n = d ? 0 : cuentas.get(s.id) || 0
    const { li, boton } = nuevaFila('gl-fila' + (d ? ' rechazada' : ''), par(s)
      + (d ? `<span class="gl-estado">No la aceptó${d.fecha ? ' el ' + esc(d.fecha) : ''}</span>` : veces(n))
      + (s.nota ? `<span class="gl-nota-t">${resaltar(s.nota)}</span>` : ''))
    if (d) {
      boton('Deshacer', () => { suyas = suyas.filter((y) => y !== d); guardar(); pintar() }, 'boton')
      return li
    }
    if (n) boton('Ver dónde', () => irA(s.id, s.oye))
    boton('Aceptar', () => {
      poner({ id: nuevoId(), de: s.id, oye: s.oye, dijo: s.dijo, nota: '', nota_maquina: s.nota || '',
        origen: 'sugerencia aceptada por usted', estado: 'aceptada', excepciones: [], fecha: hoy(), cuando: ahora() })
      guardar(); pintar()
    }, 'boton')
    boton('No', () => {
      suyas.push({ id: nuevoId(), de: s.id, oye: s.oye, dijo: s.dijo, nota: '', nota_maquina: s.nota || '',
        origen: 'sugerencia', estado: 'rechazada', fecha: hoy(), cuando: ahora() })
      guardar(); pintar()
    })
    return li
  }

  const vueltas = new Map()
  function irA(id, oye) {
    const marcas = marcasDe(id)
    if (!marcas.length) return
    const k = ((vueltas.get(id) ?? -1) + 1) % marcas.length
    vueltas.set(id, k)
    const seg = marcas[k].closest('.seg')
    if (seg) alIrA?.(seg.id)
    document.querySelectorAll('mark.gl-foco').forEach((m) => m.classList.remove('gl-foco'))
    document.querySelectorAll(`#contenido mark.gl[data-m="${marcas[k].dataset.m}"]`).forEach((m) => m.classList.add('gl-foco'))
    avisar?.(`«${oye}»: ${k + 1} de ${marcas.length}`)
  }

  /* En la transcripción: se marca cada aparición y, si es suya y aceptada, se
     pinta al lado lo que se dijo. Una aparición puede cruzar varios trozos de
     texto (una palabra dudosa va en su propio <span>): se marca trozo a trozo.
     Antes de volver a marcar se quita todo lo anterior, a cualquier profundidad. */
  let nAparicion = 0
  function marcar() {
    document.querySelectorAll('#contenido .gl-exc').forEach((n) => n.remove())
    for (const t of lineas()) {
      t.querySelectorAll('.gl-dijo').forEach((n) => n.remove())
      t.querySelectorAll('mark.gl').forEach((m) => m.replaceWith(...m.childNodes))
      t.normalize()
    }
    const reglas = [...aceptadas().map((x) => ({ ...x, tipo: 'suya' })),
      ...sugeridas.filter((s) => !decididaSug(s)).map((x) => ({ ...x, tipo: 'sugerida' }))]
      .sort((a, b) => plano(b.oye).trim().length - plano(a.oye).trim().length)
    for (const t of lineas()) {
      const id = t.closest('.seg')?.id
      rastro(t, aceptadas().filter((r) => exceptuada(r, PAGINA, id)))
      if (!reglas.length) continue
      const nodos = nodosDe(t)
      const prep = preparar(nodos.map((n) => n.data).join(''))
      const hallados = []
      for (const r of reglas) {
        if (r.tipo === 'suya' && exceptuada(r, PAGINA, id)) continue
        for (const [a, b] of buscar(prep, r.oye)) {
          if (hallados.some((h) => a < h.b && b > h.a)) continue
          hallados.push({ a, b, r, m: ++nAparicion })
        }
      }
      if (!hallados.length) continue
      let desde = 0
      for (const nodo of nodos) {
        const hasta = desde + nodo.data.length
        const trozos = hallados.filter((h) => h.a < hasta && h.b > desde)
          .map((h) => ({ ...h, x: Math.max(h.a, desde) - desde, y: Math.min(h.b, hasta) - desde, primera: h.a >= desde, ultima: h.b <= hasta }))
          .sort((p, q) => p.x - q.x)
        if (trozos.length) partir(nodo, trozos)
        desde = hasta
      }
    }
  }

  /* Lo que se dijo según ella va en un <span> VACÍO: el texto lo pone el CSS
     (data-dijo), y así no entra en lo que se selecciona y se copia. */
  function partir(nodo, trozos) {
    const texto = nodo.data
    const frag = document.createDocumentFragment()
    let k = 0
    for (const { x, y, r, m, primera, ultima } of trozos) {
      if (x > k) frag.appendChild(document.createTextNode(texto.slice(k, x)))
      const mk = document.createElement('mark')
      mk.className = `gl gl-${r.tipo}` + (primera ? '' : ' gl-sigue')
      mk.dataset.oye = r.oye
      mk.dataset.regla = r.id
      mk.dataset.m = String(m)
      mk.textContent = texto.slice(x, y)
      mk.title = r.tipo === 'suya'
        ? `Según su glosario, aquí se dijo «${r.dijo}». Si en esta línea se dijo de verdad lo transcrito, pulse: primero la oirá.`
        : `Sugerencia sin aceptar: ¿se dijo «${r.dijo}»? Acéptela en el glosario si está segura.`
      frag.appendChild(mk)
      if (r.tipo === 'suya' && ultima) {
        const s = document.createElement('span')
        s.className = 'gl-dijo'
        s.dataset.dijo = r.dijo
        s.dataset.regla = r.id
        s.dataset.m = String(m)
        s.title = 'Lo que se dijo, según su glosario. La transcripción no cambia y esto no se copia con ella.'
        frag.appendChild(s)
      }
      k = y
    }
    if (k < texto.length) frag.appendChild(document.createTextNode(texto.slice(k)))
    nodo.replaceWith(frag)
  }

  /* El rastro de una línea exceptuada, debajo de su texto y fuera de él. */
  function rastro(t, reglas) {
    const id = t.closest('.seg')?.id
    for (const r of reglas) {
      const e = r.excepciones.find((f) => f.pagina === PAGINA && f.linea === id)
      const p = document.createElement('p')
      p.className = 'gl-exc'
      p.innerHTML = `Según usted, aquí sí se dijo «${esc(r.oye)}», no «${esc(r.dijo)}»${e.fecha ? ` (la oyó el ${esc(e.fecha)})` : ''}. `
      const b = document.createElement('button')
      b.type = 'button'; b.className = 'boton tenue'; b.textContent = 'Deshacer'
      b.addEventListener('click', (ev) => { ev.stopPropagation(); quitarExcepcion(r, e) })
      p.appendChild(b)
      t.after(p)
    }
  }

  /* Pulsar una marca suya: exceptuar esa línea («aquí sí se dijo eso»). Es una
     declaración suya sobre esa línea, así que antes tiene que oírla. Un doble
     o triple clic es seleccionar para copiar: no pide nada. */
  let pulsado = null
  document.addEventListener('click', (e) => {
    const m = e.target.closest?.('#contenido mark.gl-suya, #contenido .gl-dijo')
    if (!m) return
    e.stopPropagation()
    clearTimeout(pulsado)
    if (e.detail > 1) return
    if (e.detail === 1) pulsado = setTimeout(() => exceptuar(m), 300)
    else exceptuar(m)
  }, true)
  function exceptuar(m) {
    if (!m.isConnected) return
    const r = suyas.find((x) => x.id === m.dataset.regla)
    const seg = m.closest('.seg')
    if (!r || !seg) return
    const hora = seg.querySelector('.hora')?.textContent.trim() || ''
    const dice = [...seg.querySelectorAll(`mark.gl[data-m="${m.dataset.m}"]`)].map((x) => x.textContent).join('') || r.oye
    const b = bloqueDe?.(seg.id) || C.porId?.get(seg.id)
    if (!oirLinea || b?.ancla?.tipo !== 'tiempo') {
      avisar?.(`Para decir que en esta línea sí se dijo «${dice}» hay que oírla antes, y esta página no puede hacerla sonar.`, 7000)
      return
    }
    if (!oirLinea.oida(b)) {
      if (!oirLinea.sonandoEn?.(b)) oirLinea.oir(b)
      avisar?.(`Oiga la línea ${hora}. Cuando la haya oído, vuelva a pulsar «${dice}» si ahí se dijo de verdad «${dice}» y no «${r.dijo}».`, 8000)
      return
    }
    if (!confirm(`Ha oído la línea ${hora}.\n\n¿Se dijo ahí de verdad «${dice}», y no «${r.dijo}»?\n\n`
      + 'Si acepta, queda anotado como suyo, con la fecha, y el glosario deja de aplicarse en esta línea.')) return
    const fr = oirLinea.fraccion?.(b)
    r.excepciones = [...(r.excepciones || []).filter((x) => !(x.pagina === PAGINA && x.linea === seg.id)),
      { pagina: PAGINA, linea: seg.id, minuto: hora, fecha: hoy(), cuando: ahora(), ...(Number.isFinite(fr) ? { oido: Math.round(fr * 100) / 100 } : {}) }]
    r.cuando = ahora()
    guardar(); pintar()
    avisar?.(`Anotado como suyo: en la línea ${hora} se dijo «${dice}».`)
  }

  /* Seleccionar texto en la transcripción: «Al glosario». El botón sale al
     lado de lo seleccionado, a su altura: debajo están los botones de la línea
     y encima su hora, y los tapaba. Después de Añadir o Esc, vuelve a la línea. */
  const flota = document.createElement('button')
  flota.type = 'button'; flota.className = 'gl-flota'; flota.hidden = true
  flota.textContent = '＋ Al glosario'
  document.body.appendChild(flota)
  let origen = null
  function colocar(rango) {
    const rs = rango.getClientRects()
    const ult = rs[rs.length - 1] || rango.getBoundingClientRect()
    const pri = rs[0] || ult
    flota.hidden = false
    const w = flota.offsetWidth, h = flota.offsetHeight
    const ancho = document.documentElement.clientWidth
    let x = ult.right + 8, y = ult.top + (ult.height - h) / 2
    if (x + w > ancho - 8) { x = pri.left - w - 8; y = pri.top + (pri.height - h) / 2 }
    if (x < 8) { x = Math.min(Math.max(8, pri.left), ancho - w - 8); y = pri.top - h - 6 }
    flota.style.left = `${Math.round(x + window.scrollX)}px`
    flota.style.top = `${Math.round(y + window.scrollY)}px`
  }
  document.addEventListener('mouseup', () => setTimeout(() => {
    const sel = window.getSelection()
    const txt = sel?.toString().trim() || ''
    const nodo = sel?.anchorNode
    const dentro = (nodo?.nodeType === 1 ? nodo : nodo?.parentElement)?.closest('#contenido .texto')
    if (!txt || txt.length > 60 || /\n/.test(txt) || !dentro || !sel.rangeCount) { flota.hidden = true; return }
    flota.dataset.txt = txt
    flota.dataset.seg = dentro.closest('.seg')?.id || ''
    colocar(sel.getRangeAt(0))
  }, 0))
  flota.addEventListener('mousedown', (e) => e.preventDefault())
  flota.addEventListener('click', () => {
    flota.hidden = true
    origen = flota.dataset.seg || null
    form.oye.value = flota.dataset.txt
    form.dispatchEvent(new Event('input'))
    abrirPestana?.()
    form.dijo.focus()
  })
  function volver() {
    const id = origen
    origen = null
    if (!id) return
    document.activeElement?.blur?.()
    alIrA?.(id)
  }
  form.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape' || !origen) return
    e.preventDefault()
    form.reset()
    cuenta.textContent = ''
    volver()
  })
  // Si ella se va a otra parte de la página, ya no se la devuelve a la línea.
  document.addEventListener('pointerdown', (e) => { if (origen && !caja.contains(e.target) && e.target !== flota) origen = null }, true)

  function pintar() {
    marcar()
    cuentas = new Map()
    for (const m of document.querySelectorAll('#contenido mark.gl:not(.gl-sigue)')) cuentas.set(m.dataset.regla, (cuentas.get(m.dataset.regla) || 0) + 1)
    const mias = aceptadas()
    caja.querySelector('.gl-suyas').replaceChildren(...(mias.length ? mias.map(filaSuya)
      : [Object.assign(document.createElement('li'), { className: 'gl-vacia', textContent: 'Todavía ninguna.' })]))
    const filas = sugeridas.map((s) => [s, decididaSug(s)]).filter(([, d]) => d?.estado !== 'aceptada')
    caja.querySelector('.gl-sugeridas').replaceChildren(...filas.map(([s, d]) => filaSug(s, d)))
    caja.querySelector('.gl-t-sug').hidden = !filas.length
  }
  pintar()

  return {
    set alCambiar(fn) { alCambiar = fn },
    set abrirPestana(fn) { abrirPestana = fn },
    cuantas: () => aceptadas().length,
    paraGuardar() { return { glosario: suyas } },
    /** Junta el glosario del archivo con el de este navegador (ver fusionar).
     *  Devuelve cuántas entradas traía el archivo. */
    cargar(doc) {
      if (!Array.isArray(doc?.glosario)) return 0
      const traidas = normalizar(doc.glosario).lista
      suyas = fusionar(suyas, traidas)
      escribir(); pintar()
      return traidas.length
    },
  }
}
