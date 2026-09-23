// Copia la pagina compilada al plugin y deja HUELLAS.json, igual que
// tools/pagina-despacho: `voces.html` es un ARTEFACTO COMPILADO dentro del
// repositorio, y quien edite `src/` sin volver a publicar deja al plugin
// entregando la pagina vieja sin que nada lo diga. El guardian de Python
// comprueba estas huellas sin Node.
import { copyFileSync, mkdirSync, statSync, readFileSync, writeFileSync, readdirSync } from 'node:fs'
import { createHash } from 'node:crypto'
import { dirname, resolve, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const aqui = dirname(fileURLToPath(import.meta.url))
const origen = resolve(aqui, 'dist/index.html')
const destino = resolve(aqui, '../../plugins/despacho/scripts/plantilla/voces.html')
mkdirSync(dirname(destino), { recursive: true })
copyFileSync(origen, destino)

const huella = (p) => createHash('sha256').update(readFileSync(p)).digest('hex')

const fuentes = {}
for (const f of readdirSync(join(aqui, 'src')).sort())
  fuentes[`src/${f}`] = huella(join(aqui, 'src', f))
for (const f of ['index.html', 'vite.config.js', 'package.json'])
  fuentes[f] = huella(join(aqui, f))

writeFileSync(join(aqui, 'HUELLAS.json'), JSON.stringify({
  _que_es: 'Huellas de las fuentes y de la pagina de voces publicada. Las comprueba ' +
           'evals/scripts/test_pagina_publicada.py, sin Node. Si no cuadran, ' +
           'la plantilla del plugin no corresponde a estas fuentes: publique.',
  publicado: new Date().toISOString().slice(0, 10),
  artefacto: 'plugins/despacho/scripts/plantilla/voces.html',
  huella_del_artefacto: huella(destino),
  fuentes,
}, null, 2) + '\n')

console.log(`pagina de voces publicada  ${(statSync(destino).size / 1024).toFixed(1)} KB  ->  ${destino}`)
console.log(`huellas escritas           ${Object.keys(fuentes).length} fuentes  ->  HUELLAS.json`)
