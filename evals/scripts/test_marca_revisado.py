# -*- coding: utf-8 -*-
"""La regla de SPEC-05, implementada tal como está escrita, puesta a clasificar.

**Esto no es parte del producto.** El plugin es prosa que ejecuta un modelo, y
la regla de la marca ` - REVISADO` vive en los seis `SKILL.md` que la citan. Lo
que hace este archivo es **traducir esa prosa a código y comprobar que decide
lo mismo que la prosa dice** sobre un expediente con las trampas puestas.

Sirve para una cosa concreta y vale decir cuál: **una regla en prosa que no se
puede implementar sin inventar un criterio es una regla ambigua**, y una regla
ambigua la resuelve el modelo por su cuenta, distinto en cada pasada. Si mañana
alguien edita la redacción de los seis `SKILL.md` y la vuelve ambigua o la
cambia de sentido, este archivo se cae.

Lo que NO prueba: que el modelo aplique la regla. Eso solo lo dice una pasada.

    python3 evals/scripts/test_marca_revisado.py
"""
import unicodedata
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
EXPEDIENTE = RAIZ / "evals" / "casos" / "caso-02-sintetico-autoridad" / "2-Borradores"
SKILLS = RAIZ / "plugins" / "despacho" / "skills"

# Las seis skills que citan la marca. Si una pierde la regla, se cae aquí.
CON_LA_REGLA = ["cronologia", "estado-del-caso", "hechos-con-prueba",
                "inventario-de-anexos", "inventario-de-bienes", "redactar-escrito"]
FRASE = "la marca se reconoce por el nombre, no por la extensión"

# La implementacion NO vive aqui: vive en el producto, y esta prueba comprueba
# esa. Tenerla en el test era tener la regla mas consecuente del producto en un
# sitio donde el producto no podia usarla -- y en cuanto un segundo programa la
# necesito, habrian sido dos copias.
sys.path.insert(0, str(RAIZ / "plugins" / "despacho" / "scripts"))
from marca import esta_marcado, casi_marcado, plano, sin_extensiones  # noqa: E402


class LaReglaDecide(unittest.TestCase):
    """Las cinco formas que cuentan, y las que no."""

    def test_forma_canonica(self):
        self.assertTrue(esta_marcado("Hechos - Salento - 2026-04-10 - REVISADO.md"))

    def test_extension_duplicada_por_windows(self):
        self.assertTrue(esta_marcado("Hechos - Salento - 2026-04-10 - REVISADO.md.md"))

    def test_guardado_como_txt(self):
        self.assertTrue(esta_marcado("Hechos - Salento - 2026-04-10 - REVISADO.txt"))

    def test_sin_extension(self):
        self.assertTrue(esta_marcado("Hechos - Salento - 2026-04-12 - REVISADO"))

    def test_sin_el_espacio_y_en_minusculas(self):
        self.assertTrue(esta_marcado("Hechos - Salento -REVISADO.md"))
        self.assertTrue(esta_marcado("Hechos - Salento - revisado.md"))

    def test_ninguna_tolerancia_alcanza_a_uno_sin_marca(self):
        """Control positivo: sin él, una regla que dijera 'sí' a todo pasaría."""
        self.assertFalse(esta_marcado("Hechos - Salento - 2026-04-10.md"))
        self.assertFalse(esta_marcado("Cronologia - Salento - 2026-04-09.md"))

    def test_los_casi_candidatos_no_cuentan_y_no_se_ignoran(self):
        for nombre in ("Hechos - Salento (revisar).md",
                       "REVISADO - Hechos - Salento.md",
                       "Hechos - Salento - REVISADO - v2.md"):
            self.assertFalse(esta_marcado(nombre), nombre)
            self.assertTrue(casi_marcado(nombre), nombre)


class SobreElExpedienteDePrueba(unittest.TestCase):
    """La regla, aplicada a la carpeta del caso-02, con sus trampas."""

    def setUp(self):
        self.nombres = sorted(p.name for p in EXPEDIENTE.iterdir() if p.is_file())

    def test_encuentra_el_que_windows_le_cambio_el_nombre(self):
        marcados = [n for n in self.nombres if esta_marcado(n)]
        self.assertIn("Hechos - Salento - 2026-04-10 - REVISADO.md.md", marcados)

    def test_hay_dos_marcados_y_por_eso_no_se_elige(self):
        marcados = [n for n in self.nombres if esta_marcado(n)]
        self.assertEqual(2, len(marcados), marcados)
        # La regla dice: se nombran los dos y se pregunta. No se elige el
        # mas reciente por ser el mas reciente.

    def test_el_casi_candidato_se_detecta_para_poder_nombrarlo(self):
        casi = [n for n in self.nombres if casi_marcado(n)]
        self.assertEqual(["Hechos - Salento (revisar).md"], casi)

    def test_el_sin_marcar_sigue_sin_contar(self):
        self.assertFalse(esta_marcado("Hechos - Salento - 2026-04-10.md"))


class LaReglaSigueEscritaDondeDebe(unittest.TestCase):
    """Si alguien la borra de un SKILL.md, esto se cae."""

    def test_las_seis_skills_la_traen(self):
        faltan = [s for s in CON_LA_REGLA
                  if FRASE not in (SKILLS / s / "SKILL.md").read_text(encoding="utf-8")]
        self.assertEqual([], faltan)

    def test_las_seis_dicen_que_reconocer_no_es_renombrar(self):
        faltan = [s for s in CON_LA_REGLA
                  if "Reconocer no es renombrar" not in (SKILLS / s / "SKILL.md").read_text(encoding="utf-8")]
        self.assertEqual([], faltan)


if __name__ == "__main__":
    unittest.main(verbosity=2)
