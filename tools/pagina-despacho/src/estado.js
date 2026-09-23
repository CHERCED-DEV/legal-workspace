/* Lo que ella marca. ADR-022.
 *
 * Regla que gobierna este archivo: el estado NO es prueba de nada. «Confirmado»
 * significa que ella afirma haber ido al original, no que el texto sea correcto.
 *
 * El almacenamiento del navegador NO es la fuente de verdad: en archivos abiertos
 * desde disco puede estar bloqueado o compartido. La fuente es el archivo que ella
 * exporta. Aqui es una comodidad, y si falla la pagina lo dice.
 */

export const ETIQUETA = { oido: 'Oído', confirmado: 'Confirmado', corregido: 'Corregido' }

export function crearEstado(clave, alCambiar) {
  const llave = 'despacho:estado:' + clave
  let almacenOK = true
  let sucio = false
  let datos = {}

  const leer = () => JSON.parse(localStorage.getItem(llave) || '{}')

  try {
    datos = leer()
  } catch { almacenOK = false }

  // La misma pagina abierta en dos pestanas: cada una guardaba su copia entera y
  // la ultima en escribir borraba las marcas de la otra, sin decir nada. Ahora se
  // relee antes de escribir y se repinta cuando la otra pestana cambia algo.
  window.addEventListener('storage', (e) => {
    if (e.key !== llave) return
    try { datos = leer() } catch { return }
    alCambiar?.(null)
  })

  const persistir = () => {
    try { localStorage.setItem(llave, JSON.stringify(datos)) }
    catch { almacenOK = false }
  }

  const hoy = () => new Date().toLocaleDateString('es-CO',
    { year: 'numeric', month: '2-digit', day: '2-digit' })

  return {
    get almacenOK() { return almacenOK },
    get sucio() { return sucio },
    get todo() { return datos },
    de: (id) => datos[id] || null,
    cuantos: () => Object.keys(datos).length,

    marcar(id, tipo, correccion) {
      if (almacenOK) { try { datos = leer() } catch { /* sigue con lo que tiene */ } }
      if (tipo === 'corregido') datos[id] = { estado: tipo, fecha: hoy(), correccion }
      else if (datos[id]?.estado === tipo) delete datos[id]
      else datos[id] = { estado: tipo, fecha: hoy() }
      sucio = true
      persistir()
      alCambiar?.(id)
    },

    reemplazar(nuevos) {
      datos = nuevos || {}
      sucio = false
      persistir()
      alCambiar?.(null)
    },

    exportar(documento, extra = {}) {
      const doc = {
        formato: 'despacho/estado-de-comprobacion',
        version: 1,
        documento: documento.titulo || '',
        clave,
        exportado: new Date().toISOString(),
        nota: 'Constancia de que una persona fue al original. NO es verificacion '
            + 'de que el texto sea correcto.',
        estado: datos,
        // Quien dijo ELLA que es cada voz. Va aparte del estado de
        // comprobacion porque son dos cosas distintas: una es «fui al
        // original», la otra es «esta voz es esta persona».
        voces: extra.voces || {},
      }
      const a = document.createElement('a')
      a.href = URL.createObjectURL(new Blob([JSON.stringify(doc, null, 1)],
        { type: 'application/json' }))
      a.download = `comprobado - ${(documento.titulo || 'documento').replace(/[\\/:*?"<>|]/g, '')}.json`
      a.click()
      URL.revokeObjectURL(a.href)
      sucio = false
      alCambiar?.(null)
    },

    importar(file, claveEsperada) {
      return new Promise((res, rej) => {
        const fr = new FileReader()
        fr.onload = () => {
          try {
            const d = JSON.parse(fr.result)
            if (d.clave && claveEsperada && d.clave !== claveEsperada &&
                !confirm('Ese archivo es de otro documento. ¿Cargarlo de todos modos?')) return res(false)
            this.reemplazar(d.estado || {})
            res(true)
          } catch { rej(new Error('No se pudo leer ese archivo.')) }
        }
        fr.readAsText(file)
      })
    },
  }
}
