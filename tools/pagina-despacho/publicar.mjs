// Copia la plantilla compilada al plugin. Es lo unico que viaja a la maquina
// de la abogada: ya compilada, sin Node, sin node_modules. ADR-018 / ADR-020.
import { copyFileSync, mkdirSync, statSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const aqui = dirname(fileURLToPath(import.meta.url))
const origen = resolve(aqui, 'dist/index.html')
const destino = resolve(aqui, '../../plugins/despacho/scripts/plantilla/pagina.html')
mkdirSync(dirname(destino), { recursive: true })
copyFileSync(origen, destino)
console.log(`plantilla publicada  ${(statSync(destino).size / 1024).toFixed(1)} KB  ->  ${destino}`)
