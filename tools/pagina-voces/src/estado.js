/* Lo que ella declara. SPEC-15 §4.4 y ADR-022.
 *
 * Se guarda en el navegador en CADA accion, para que cerrar la pestana no
 * cueste nada. Pero el almacenamiento del navegador NO es la fuente de verdad:
 * abierto desde disco puede estar bloqueado, o borrarse. La fuente es el
 * archivo que ella exporta, y la pagina lo recuerda.
 */

const VACIO = () => ({
  version: 1,
  declarado_por: '',
  voces: {},          // vid -> { nombre, cargo, como_lo_sabe, fusionada_en, nueva }
  lineas: {},         // lid -> { decision, voz, voces, partes, propuesta_maquina, banda_maquina, oida, origen, fecha }
  saltadas: [],
  borradores: {},     // lid -> texto de un rescate que ella esta corrigiendo
  velocidad: 1,
  autoOir: true,
  actualizado: '',
})

export function crearEstado(clave, alCambiar) {
  const llave = 'despacho:voces:' + clave
  let almacenOK = true
  let datos = VACIO()
  const pila = []                 // para deshacer: instantaneas previas
  let exportado = null            // cuando se exporto por ultima vez

  const leer = () => {
    const t = localStorage.getItem(llave)
    return t ? { ...VACIO(), ...JSON.parse(t) } : VACIO()
  }
  try { datos = leer() } catch { almacenOK = false }
  try { exportado = localStorage.getItem(llave + ':exportado') } catch { /* nada */ }

  window.addEventListener('storage', (e) => {
    if (e.key !== llave) return
    try { datos = leer() } catch { return }
    pila.length = 0
    alCambiar?.({ externo: true })
  })

  const persistir = () => {
    datos.actualizado = new Date().toISOString()
    try { localStorage.setItem(llave, JSON.stringify(datos)); almacenOK = true }
    catch { almacenOK = false }   // bloqueado, o lleno (quiza por otras reuniones)
  }
  const hoy = () => new Date().toISOString().slice(0, 10)
  const foto = () => JSON.stringify(datos)

  function cambiar(fn, etiqueta, lid = null) {
    pila.push({ antes: foto(), etiqueta, lid })
    if (pila.length > 200) pila.shift()
    fn(datos)
    persistir()
    alCambiar?.({ etiqueta })
  }

  return {
    get almacenOK() { return almacenOK },
    get todo() { return datos },
    get puedeDeshacer() { return pila.length > 0 },
    get ultimaAccion() { return pila.length ? pila[pila.length - 1].etiqueta : '' },
    get exportado() { return exportado },
    get pendiente() {
      return !!datos.actualizado && (!exportado || exportado < datos.actualizado)
    },

    declarante(nombre) {
      cambiar((d) => { d.declarado_por = nombre.trim() }, 'nombre de quien declara')
    },

    decidir(lid, decision) {
      cambiar((d) => {
        d.lineas[lid] = { ...decision, fecha: hoy() }
        d.saltadas = d.saltadas.filter((x) => x !== lid)
        if (d.borradores) delete d.borradores[lid]
      }, 'la decisión de una línea', lid)
    },

    /** Cambia algo de una decision ya tomada sin tocar lo demas -- sobre todo
     * lo que la maquina proponia cuando ella decidio, que es la prueba. */
    retocar(lid, cambios) {
      if (!datos.lineas[lid]) return
      cambiar((d) => { d.lineas[lid] = { ...d.lineas[lid], ...cambios } }, 'el texto de un tramo', lid)
    },

    /** Lo que escribe en un rescate aun sin decidir: se guarda al vuelo, para
     * que cerrar la pestana no lo pierda. No entra en la pila de deshacer. */
    borrador(lid, texto) {
      datos.borradores ||= {}
      datos.borradores[lid] = texto
      persistir()
    },

    olvidar(lid) {
      cambiar((d) => { delete d.lineas[lid] }, 'quitar una decisión', lid)
    },

    saltar(lid) {
      cambiar((d) => { if (!d.saltadas.includes(lid)) d.saltadas.push(lid) }, 'saltar')
    },

    nombrar(vid, info) {
      cambiar((d) => { d.voces[vid] = { ...(d.voces[vid] || {}), ...info } }, 'nombre de voz')
    },

    nuevaVoz(info) {
      let k = 1
      while (datos.voces['n' + k]) k++
      const vid = 'n' + k
      cambiar((d) => { d.voces[vid] = { nueva: true, ...info } }, 'persona nueva')
      return vid
    },

    fusionar(de, en) {
      if (de === en) return
      cambiar((d) => {
        const destino = d.voces[en] || {}
        const origen = d.voces[de] || {}
        // Si solo la que se funde tenia nombre, el nombre pasa a la otra.
        if (!destino.nombre && origen.nombre) {
          d.voces[en] = { ...destino, nombre: origen.nombre, cargo: origen.cargo,
            como_lo_sabe: origen.como_lo_sabe, heredado_de: de }
        }
        d.voces[de] = { ...origen, fusionada_en: en }
      }, 'unir voces')
    },

    separar(vid) {
      cambiar((d) => {
        if (d.voces[vid]) delete d.voces[vid].fusionada_en
        for (const info of Object.values(d.voces)) {
          if (info.heredado_de === vid) {
            delete info.nombre; delete info.cargo; delete info.como_lo_sabe; delete info.heredado_de
          }
        }
      }, 'deshacer una unión')
    },

    velocidad(x) {
      datos.velocidad = x
      persistir()
    },

    autoOir(si) {
      datos.autoOir = !!si
      persistir()
    },

    /** Devuelve QUE se deshizo y de que linea, para decirlo y volver a ella. */
    deshacer() {
      const u = pila.pop()
      if (!u) return null
      datos = JSON.parse(u.antes)
      persistir()
      alCambiar?.({ etiqueta: 'deshacer' })
      return { etiqueta: u.etiqueta, lid: u.lid }
    },

    reemplazar(nuevo) {
      pila.push({ antes: foto(), etiqueta: 'cargar declaración' })
      datos = { ...VACIO(), ...nuevo }
      persistir()
      alCambiar?.({ etiqueta: 'cargar' })
    },

    marcarExportado() {
      exportado = new Date().toISOString()
      try { localStorage.setItem(llave + ':exportado', exportado) } catch { /* nada */ }
    },
  }
}
