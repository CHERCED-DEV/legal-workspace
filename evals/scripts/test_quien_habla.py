# -*- coding: utf-8 -*-
"""«Quién habla»: el panel de la página de oír y marcar donde ella confirma,
oyendo, quién dice cada fragmento.

Las cuentas viven en `tools/pagina-despacho/src/atribucion.js` y se prueban
con Node (`prueba-atribucion.mjs`): aquí se corren si hay Node, y se comprueba
sin Node que la plantilla publicada lleva el panel y sus reglas.

    python3 evals/scripts/test_quien_habla.py
"""
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PAGINA = RAIZ / "tools" / "pagina-despacho"
PLANTILLA = RAIZ / "plugins" / "despacho" / "scripts" / "plantilla" / "pagina.html"


class LasCuentas(unittest.TestCase):

    @unittest.skipUnless(shutil.which("node"), "sin Node no se pueden correr las cuentas")
    def test_las_cuentas_no_mienten(self):
        r = subprocess.run(["node", "prueba-atribucion.mjs"], cwd=str(PAGINA),
                           capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(0, r.returncode, r.stdout + r.stderr)
        self.assertIn("todas bien", r.stdout)


class ElGlosario(unittest.TestCase):

    @unittest.skipUnless(shutil.which("node"), "sin Node no se puede correr")
    def test_el_buscador_no_marca_de_mas(self):
        r = subprocess.run(["node", "prueba-glosario.mjs"], cwd=str(PAGINA),
                           capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(0, r.returncode, r.stdout + r.stderr)


class LasOtrasLecturasYElGuardado(unittest.TestCase):
    """Que parte de otra lectura corresponde a la linea (y donde no coincide), y
    donde guarda la pagina lo que ella declara (en el proyecto, si lo hay)."""

    @unittest.skipUnless(shutil.which("node"), "sin Node no se puede correr")
    def test_las_otras_lecturas(self):
        r = subprocess.run(["node", "prueba-lecturas.mjs"], cwd=str(PAGINA),
                           capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(0, r.returncode, r.stdout + r.stderr)

    @unittest.skipUnless(shutil.which("node"), "sin Node no se puede correr")
    def test_los_paneles_no_dejan_declarar_sin_oir(self):
        r = subprocess.run(["node", "prueba-paneles.mjs"], cwd=str(PAGINA),
                           capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(0, r.returncode, r.stdout + r.stderr)

    @unittest.skipUnless(shutil.which("node"), "sin Node no se puede correr")
    def test_donde_se_guarda(self):
        r = subprocess.run(["node", "prueba-guardado.mjs"], cwd=str(PAGINA),
                           capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(0, r.returncode, r.stdout + r.stderr)


class LaPlantillaPublicada(unittest.TestCase):

    def setUp(self):
        self.t = PLANTILLA.read_text(encoding="utf-8")

    def test_lleva_el_panel(self):
        for trozo in ("despacho:atribucion:", "Quién habla", "No sé quién es", "Es otra voz",
                      "Lo que no se entiende", "despacho:ilegibles:", "despacho:compromisos:",
                      "despacho:glosario:", "Lo que declaré", "2-Borradores", "Oír la línea"):
            self.assertIn(trozo, self.t, trozo)

    def test_el_panel_no_va_dentro_de_la_barra_fija(self):
        """Dentro de la barra crecía hasta tapar la transcripción."""
        barra = self.t[self.t.index('id="barra"'):self.t.index('id="contenido"')]
        self.assertLess(barra.index('</div>\n\n<!-- Quien habla'), barra.index('id="voces"'))

    def test_las_reglas_son_las_declaradas(self):
        """La meta y la regla de oír antes de decidir, en la fuente. Que la
        plantilla publicada corresponde a la fuente lo asegura HUELLAS.json
        (test_pagina_publicada)."""
        src = (PAGINA / "src" / "atribucion.js").read_text(encoding="utf-8")
        self.assertIn("export const META = 0.85", src)
        self.assertIn("export const OIDA_MINIMA = 0.7", src)


if __name__ == "__main__":
    unittest.main(verbosity=2)
