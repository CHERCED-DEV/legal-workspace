# -*- coding: utf-8 -*-
"""Los bloques que se repiten en varias skills tienen que decir lo MISMO.

**Esto no es parte del producto.** Es la guarda mecánica de una regla que este
repositorio aprendió por la mala y volvió a romper el 2026-09-05: **una regla
con dos redacciones se parte.** El backlog lo llama su enfermedad —«dos ledgers
con identificadores que colisionan, seis archivos para una capacidad»— y ese
mismo día se cometió otra vez: se escribió una segunda regla de simetría, más
débil, al lado de la que `revision-de-rigor` §2.3 ya tenía.

Un `grep -l` dice que la frase está en los once. **No dice que diga lo mismo en
los once.** Eso es lo que comprueba este archivo, y es la diferencia entre
declarar una regla única y tenerla.

Y la segunda familia: **toda regla que mande preguntar tiene que mandar
esperar.** Salió de dos defectos del mismo día -- «pregunta cuál manda» sin «y
te detienes», y la posición preguntada sin esperar respuesta -- y es la clase
de fallo que vuelve solo: preguntar se siente como haber hecho lo correcto.

    python3 evals/scripts/test_bloques_identicos.py
"""
import re
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
SKILLS = RAIZ / "plugins" / "despacho" / "skills"
TODAS = sorted(p for p in SKILLS.glob("*/SKILL.md"))
# Las seis que citan la marca y el trabajo del sistema como fuente.
CON_FUENTE = ["cronologia", "estado-del-caso", "hechos-con-prueba",
              "inventario-de-anexos", "inventario-de-bienes", "redactar-escrito"]


def texto(p):
    return p.read_text(encoding="utf-8")


def entre(t, desde, hasta):
    """El trozo que va de una marca a otra, o None si no está."""
    i = t.find(desde)
    if i < 0:
        return None
    j = t.find(hasta, i + len(desde))
    return t[i:j] if j > 0 else t[i:]


class UnaReglaUnaRedaccion(unittest.TestCase):

    def _identico(self, archivos, extractor, nombre):
        trozos = {}
        for p in archivos:
            t = extractor(texto(p))
            self.assertIsNotNone(t, "%s no tiene el bloque «%s»" % (p.parent.name, nombre))
            trozos.setdefault(t, []).append(p.parent.name)
        if len(trozos) > 1:
            grupos = " || ".join("[%s]" % ", ".join(v) for v in trozos.values())
            self.fail("el bloque «%s» tiene %d redacciones distintas: %s"
                      % (nombre, len(trozos), grupos))

    def test_el_bloque_de_posicion_es_el_mismo_en_los_once(self):
        """SPEC-03 R-5: una sola redacción, no dos versiones del método."""
        self._identico(TODAS,
                       lambda t: entre(t, "### En qué posición está ella", "\n---\n"),
                       "posición (contexto B)")

    def test_el_bloque_de_la_pasada_es_el_mismo_en_los_once(self):
        """SPEC-12 R-7: para que dos pasadas de dos comandos se comparen."""
        self._identico(TODAS,
                       lambda t: entre(t, "**Al terminar esta lista, escribe este bloque",
                                       "no se te evalúa por él."),
                       "lo que la pasada se corrigió")

    def test_el_bloque_de_la_marca_es_el_mismo_en_las_seis(self):
        """SPEC-05 O-1: la regla de reconocimiento, idéntica donde se cita."""
        self._identico([SKILLS / s / "SKILL.md" for s in CON_FUENTE],
                       lambda t: entre(t, "> **Y la marca se reconoce por el nombre",
                                       "\n\n> **Y el texto que extrajo una máquina"),
                       "reconocimiento de la marca")

    def test_control_positivo_los_bloques_existen(self):
        """Sin esto, un extractor que devolviera siempre lo mismo pasaría."""
        for p in TODAS:
            self.assertIn("### En qué posición está ella", texto(p), p.parent.name)
        for s in CON_FUENTE:
            self.assertIn("Reconocer no es renombrar", texto(SKILLS / s / "SKILL.md"), s)


class PreguntarNoEsSeguir(unittest.TestCase):
    """Toda regla que manda preguntar manda esperar. Dos defectos del 05/09."""

    def test_la_posicion_se_pregunta_y_se_espera(self):
        faltan = [p.parent.name for p in TODAS
                  if "se espera la respuesta antes de producir nada" not in texto(p)]
        self.assertEqual([], faltan)

    def test_la_marca_dos_veces_puesta_se_pregunta_y_se_espera(self):
        faltan = [s for s in CON_FUENTE
                  if "se nombran, se pregunta y se espera" not in texto(SKILLS / s / "SKILL.md")]
        self.assertEqual([], faltan)

    def test_redactar_escrito_se_detiene_con_dos_marcados(self):
        t = texto(SKILLS / "redactar-escrito" / "SKILL.md")
        self.assertIn("te detienes ahí igual que si no hubiera ninguno", t)
        self.assertIn("Y esto es una parada, no un aviso", t)


class LaSimetriaTieneUnDueno(unittest.TestCase):
    """Defecto 7: dos reglas para lo mismo. La de revision-de-rigor manda."""

    def test_revision_de_rigor_conserva_la_regla_original(self):
        t = texto(SKILLS / "revision-de-rigor" / "SKILL.md")
        self.assertIn("La simetría es obligatoria, y no se negocia", t)
        self.assertIn("los defectos de sus propios actos se buscan igual", t)

    def test_los_once_apuntan_a_ella_en_vez_de_competir(self):
        faltan = [p.parent.name for p in TODAS
                  if "`revision-de-rigor` §2.3 la tiene desarrollada" not in texto(p)]
        self.assertEqual([], faltan)

    def test_los_once_traen_las_tres_piezas_que_les_faltaban(self):
        for pieza in ("los defectos de lo que su propio despacho produjo",
                      "hay más superficie donde encontrar defectos",
                      "se dice, con los números"):
            faltan = [p.parent.name for p in TODAS if pieza not in texto(p)]
            self.assertEqual([], faltan, pieza)


class ElFrontmatterCarga(unittest.TestCase):
    """V-13: un ':' sin comillas en description y un lector estricto no carga."""

    def test_las_once_descripciones_van_entrecomilladas(self):
        malas = []
        for p in TODAS:
            m = re.search(r"^description: (.*)$", texto(p), re.M)
            if not (m and m.group(1).startswith('"') and m.group(1).rstrip().endswith('"')):
                malas.append(p.parent.name)
        self.assertEqual([], malas)

    def test_el_frontmatter_parsea_como_yaml(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("sin PyYAML")
        for p in TODAS:
            yaml.safe_load(texto(p).split("\n---\n", 1)[0][4:])


if __name__ == "__main__":
    unittest.main(verbosity=2)
