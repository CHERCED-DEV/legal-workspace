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
  // Cuenta los cambios: el autoguardado solo da por guardado lo que escribió.
  // Sin esto, una marca hecha MIENTRAS se escribía quedaba como guardada.
  let version = 0

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
    get version() { return version },
    get todo() { return datos },
    de: (id) => datos[id] || null,
    cuantos: () => Object.keys(datos).length,

    /** `origen` (opcional, solo en correcciones): de qué lectura automática
     *  partió ella, { partio_de, sugerido }. Queda dicho: no es lo mismo
     *  escribirlo que aceptar y ajustar lo que leyó otra máquina. */
    marcar(id, tipo, correccion, origen = null) {
      if (almacenOK) { try { datos = leer() } catch { /* sigue con lo que tiene */ } }
      if (tipo === 'corregido') datos[id] = { estado: tipo, fecha: hoy(), correccion, ...(origen || {}) }
      else if (datos[id]?.estado === tipo) delete datos[id]
      else datos[id] = { estado: tipo, fecha: hoy() }
      sucio = true
      version++
      persistir()
      alCambiar?.(id)
    },

    /** Algo que se guarda aparte (las voces) tambien cuenta como «sin guardar
     *  en un archivo»: si no, el aviso callaba justo lo que mas trabajo cuesta. */
    tocar() {
      sucio = true
      version++
      alCambiar?.('voces')
    },

    reemplazar(nuevos) {
      datos = nuevos || {}
      sucio = false
      version++
      persistir()
      alCambiar?.(null)
    },

    /** Lo que se ha hecho en esta página, como documento: lo que se guarda. */
    documento(documento, extra = {}) {
      return {
        formato: 'despacho/estado-de-comprobacion',
        version: 2,
        documento: documento.titulo || '',
        clave,
        exportado: new Date().toISOString(),
        nota: 'Constancia de lo que una persona hizo oyendo el original. NO es verificacion '
            + 'de que el texto sea correcto.',
        estado: datos,
        ...extra,
      }
    },

    /** Ya está en un archivo: no hay nada sin guardar. `hasta` = la versión que
     *  se escribió; si después cambió algo, sigue habiendo algo sin guardar. */
    limpiar(hasta = null) {
      if (hasta != null && hasta !== version) return
      sucio = false
      alCambiar?.('guardado')
    },

    exportar(documento, extra = {}) {
      const doc = {
        formato: 'despacho/estado-de-comprobacion',
        version: 2,
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
        // Quien habla, fragmento a fragmento, segun ELLA oyendolo. La maquina
        // solo propuso la voz; lo que va aqui lo afirmo ella.
        atribucion: extra.atribucion || {},
        resumen_voces: extra.resumen_voces || {},
        ...extra,
      }
      const a = document.createElement('a')
      a.href = URL.createObjectURL(new Blob([JSON.stringify(doc, null, 1)],
        { type: 'application/json' }))
      // Con la fecha en el nombre: si no, Descargas los numeraba «(1)», «(2)»…
      // y no se sabía cuál era el último.
      const d = new Date(), p = (n) => String(n).padStart(2, '0')
      const sello = `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}.${p(d.getMinutes())}.${p(d.getSeconds())}`
      a.download = `comprobado - ${(documento.titulo || 'documento').replace(/[\\/:*?"<>|]/g, '')} - ${sello}.json`
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
            // De otra transcripción (u otra versión de esta), no se carga NADA:
            // las líneas, tramos y compromisos se nombran por su sitio, y lo
            // que declaró quedaría pegado a otra cosa. Sigue en su archivo.
            if (!d.clave || (claveEsperada && d.clave !== claveEsperada)) {
              return rej(new Error('Ese archivo es de otra transcripción, o de otra versión de esta: no se carga, '
                + 'para no pegar lo que usted declaró a líneas que no son. Lo que declaró sigue en ese archivo.'))
            }
            this.reemplazar(d.estado || {})
            res(d)
          } catch { rej(new Error('No se pudo leer ese archivo.')) }
        }
        fr.readAsText(file)
      })
    },
  }
}
