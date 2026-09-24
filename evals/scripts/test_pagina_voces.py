# -*- coding: utf-8 -*-
"""La pagina de voces (SPEC-15) viaja COMPILADA, y eso hay que vigilarlo.

Mismo problema que `test_pagina_publicada.py` vigila en la otra pagina:
`plugins/despacho/scripts/plantilla/voces.html` no se escribe, se compila desde
`tools/pagina-voces/src/`. Si alguien toca las fuentes y no publica, el plugin
entrega la pagina vieja sin que nada lo diga; si alguien edita el `.html`
compilado a mano, la correccion se pierde en la siguiente compilacion.

Y dos cosas propias de ESTA pagina:

  · **Cero red** (ADR-020 §3). La pagina lleva dentro la huella de voz de
    cada linea de una reunion. Una sola peticion a fuera contaria de quien
    es la voz. Se comprueba sobre lo compilado, que es lo que viaja.
  · **El motor cuenta igual que `aplicar`.** La claridad que ella ve en la
    pagina y la que escribe `genoma_de_voz.py aplicar` salen de dos
    implementaciones: JavaScript y Python. `prueba-genoma.mjs` fija las
    mismas reglas del lado de la pagina. Necesita Node; si no lo hay, **se
    salta diciendolo**, no se finge que paso.

    python3 evals/scripts/test_pagina_voces.py
"""
import hashlib
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
TOOLS = RAIZ / "tools" / "pagina-voces"
HUELLAS = TOOLS / "HUELLAS.json"
ARTEFACTO = RAIZ / "plugins" / "despacho" / "scripts" / "plantilla" / "voces.html"
FIJOS = ("index.html", "vite.config.js", "package.json")


def huella(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


class LasHuellasCuadran(unittest.TestCase):

    def setUp(self):
        self.assertTrue(HUELLAS.is_file(), "falta %s: publique con `npm run publicar`" % HUELLAS)
        self.h = json.loads(HUELLAS.read_text(encoding="utf-8"))

    def test_lo_listado_es_exactamente_lo_que_hay(self):
        en_disco = {"src/" + p.name for p in (TOOLS / "src").iterdir() if p.is_file()} | set(FIJOS)
        self.assertEqual(en_disco, set(self.h["fuentes"]),
                         "HUELLAS.json no lista exactamente las fuentes: publique otra vez")

    def test_cada_fuente_es_la_que_se_publico(self):
        distintas = [f for f, v in self.h["fuentes"].items() if huella(TOOLS / f) != v]
        self.assertEqual([], distintas,
                         "estas fuentes cambiaron despues de publicar: la pagina que viaja es vieja")

    def test_la_plantilla_es_la_que_se_publico(self):
        self.assertTrue(ARTEFACTO.is_file(), "falta la plantilla %s" % ARTEFACTO)
        self.assertEqual(self.h["huella_del_artefacto"], huella(ARTEFACTO),
                         "voces.html no es lo que se compilo: se edito a mano o se publico a medias")


class LaPlantillaViajaSola(unittest.TestCase):

    def setUp(self):
        self.t = ARTEFACTO.read_text(encoding="utf-8")

    def test_tiene_donde_van_los_datos(self):
        self.assertEqual(1, self.t.count("{{DATOS}}"))
        self.assertIn("{{TITULO}}", self.t)
        self.assertIn('<script id="datos" type="application/json">{{DATOS}}</script>', self.t)

    def test_cero_red(self):
        self.assertEqual([], re.findall(r"https?://", self.t), "la pagina nombra una direccion de red")
        for api in ("fetch(", "XMLHttpRequest", "WebSocket", "sendBeacon", "EventSource", "importScripts"):
            self.assertNotIn(api, self.t, "la pagina puede pedir algo a un servidor: %s" % api)

    def test_todo_va_dentro(self):
        self.assertIsNone(re.search(r'<script[^>]+src=', self.t), "un script se carga de fuera")
        self.assertIsNone(re.search(r'<link[^>]+stylesheet', self.t), "un estilo se carga de fuera")


class ElAvisoDeSitioEsElMismoEnLasDosPaginas(unittest.TestCase):
    """`sola.js` (abierta desde un .zip, los pasos del Mac o de Windows) va copiado
    en las dos paginas: cada una se compila y se vigila por separado. Si una copia
    cambia y la otra no, una pagina avisaria distinto que la otra."""

    def test_las_dos_copias_son_iguales(self):
        a = TOOLS / "src" / "sola.js"
        b = RAIZ / "tools" / "pagina-despacho" / "src" / "sola.js"
        self.assertTrue(a.is_file() and b.is_file(), "falta una de las dos copias de sola.js")
        self.assertEqual(huella(a), huella(b), "las dos copias de sola.js difieren: copie la buena en las dos y publique las dos")


class ElMotorDeLaPagina(unittest.TestCase):

    def test_prueba_genoma(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("no hay Node en esta maquina: el motor de la pagina NO se comprobo")
        r = subprocess.run([node, "prueba-genoma.mjs"], cwd=str(TOOLS), capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=120)
        self.assertEqual(0, r.returncode, r.stdout + r.stderr)

    def test_prueba_sola(self):
        """La pagina en su sitio y el guardado en la carpeta del proyecto: abierta
        desde un .zip se dice, en el Mac con sus pasos, y escribir en la carpeta no
        pierde nada de lo que habia (2026-09-24: la abrio desde el .zip y no sono nada)."""
        node = shutil.which("node")
        if not node:
            self.skipTest("no hay Node en esta maquina: el aviso y el guardado NO se comprobaron")
        r = subprocess.run([node, "prueba-sola.mjs"], cwd=str(TOOLS), capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=120)
        self.assertEqual(0, r.returncode, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
