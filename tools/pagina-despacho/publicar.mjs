// Copia la plantilla compilada al plugin. Es lo unico que viaja a la maquina
// de la abogada: ya compilada, sin Node, sin node_modules. ADR-018 / ADR-020.
//
// Y ademas deja HUELLAS.json, que es lo que permite comprobar SIN Node que la
// plantilla que viaja corresponde a estas fuentes. El problema que resuelve es
// concreto y silencioso: `pagina.html` es un ARTEFACTO COMPILADO dentro del
// repositorio. Quien edite `src/` y no vuelva a publicar deja al plugin
// entregando la pagina vieja, y nada lo dice. Su ADR (020 §2) ademas prohibe
// editar a mano un `.html` de salida, y hasta hoy esa prohibicion no tenia
// nada que la hiciera cumplir.
import { copyFileSync, mkdirSync, statSync, readFileSync, writeFileSync, readdirSync } from 'node:fs'
import { createHash } from 'node:crypto'
import { dirname, resolve, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const aqui = dirname(fileURLToPath(import.meta.url))
const origen = resolve(aqui, 'dist/index.html')
const destino = resolve(aqui, '../../plugins/despacho/scripts/plantilla/pagina.html')
mkdirSync(dirname(destino), { recursive: true })
copyFileSync(origen, destino)

const huella = (p) => createHash('sha256').update(readFileSync(p)).digest('hex')

// Todo lo que entra en la compilacion. Si un dia se anade otra entrada --otro
// html, otra carpeta-- hay que anadirla aqui, y la prueba de Python avisa:
// comprueba que lo listado sea EXACTAMENTE lo que hay en el disco.
const fuentes = {}
for (const f of readdirSync(join(aqui, 'src')).sort())
  fuentes[`src/${f}`] = huella(join(aqui, 'src', f))
for (const f of ['index.html', 'vite.config.js', 'package.json', 'package-lock.json'])
  fuentes[f] = huella(join(aqui, f))

writeFileSync(join(aqui, 'HUELLAS.json'), JSON.stringify({
  _que_es: 'Huellas de las fuentes y de la plantilla publicada. Las comprueba ' +
           'evals/scripts/test_pagina_publicada.py, sin Node. Si no cuadran, ' +
           'la plantilla del plugin no corresponde a estas fuentes: publique.',
  publicado: new Date().toISOString().slice(0, 10),
  artefacto: 'plugins/despacho/scripts/plantilla/pagina.html',
  huella_del_artefacto: huella(destino),
  fuentes,
}, null, 2) + '\n')

console.log(`plantilla publicada  ${(statSync(destino).size / 1024).toFixed(1)} KB  ->  ${destino}`)
console.log(`huellas escritas     ${Object.keys(fuentes).length} fuentes  ->  HUELLAS.json`)
