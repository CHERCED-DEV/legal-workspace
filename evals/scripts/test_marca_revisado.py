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
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
EXPEDIENTE = RAIZ / "evals" / "casos" / "caso-02-sintetico-autoridad" / "2-Borradores"
SKILLS = RAIZ / "plugins" / "despacho" / "skills"

# Las seis skills que citan la marca. Si una pierde la regla, se cae aquí.
CON_LA_REGLA = ["cronologia", "estado-del-caso", "hechos-con-prueba",
                "inventario-de-anexos", "inventario-de-bienes", "redactar-escrito"]
FRASE = "la marca se reconoce por el nombre, no por la extensión"

EXTENSIONES = {".md", ".txt", ".docx", ".doc", ".rtf"}


def plano(s):
    d = unicodedata.normalize("NFD", s)
    return "".join(c for c in d if unicodedata.category(c) != "Mn").upper()


def sin_extensiones(nombre):
    """«quitada la extensión, o las dos si quedaron dos, o ninguna si no tiene»."""
    p = Path(nombre)
    for _ in range(2):
        if p.suffix.lower() in EXTENSIONES:
            p = p.with_suffix("")
        else:
            break
    return p.name


def esta_marcado(nombre):
    """«termina en REVISADO, en mayúsculas o minúsculas, con el guion o sin él»."""
    return plano(sin_extensiones(nombre)).rstrip().endswith("REVISADO")


def casi_marcado(nombre):
    """«la raíz «revis»... sin cerrar el nombre: se nombra y se pregunta».

    La raíz y no la palabra, y esto lo encontró esta prueba: la redacción
    anterior decía «revisado» de cualquier otra forma y ponía `(revisar)` de
    ejemplo -- pero «revisar» NO contiene «revisado». Quien buscara la palabra
    pasaba por encima del ejemplo de la propia regla sin verlo.
    """
    return not esta_marcado(nombre) and "REVIS" in plano(nombre)


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
