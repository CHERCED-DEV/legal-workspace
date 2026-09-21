# -*- coding: utf-8 -*-
"""Los titulares de §0 de ESTADO-DEL-PROYECTO, recomprobados contra el disco.

**Este documento caduco en silencio durante veintiseis dias.** Su version del
2026-08-26 declaraba su propia fecha de caducidad -- «caduca con el proximo
commit que toque plugins/despacho/ o docs/skills-support/» -- y caduco al dia
siguiente, pero nadie lo noto: nueve de sus diez titulares eran falsos cuando
se volvio a leer, y ninguno se cayo solo.

Una fecha de caducidad no es una guarda. Esto si.

No comprueba los diez -- cuatro son juicios y se dice cuales. Comprueba los que
tienen respuesta en el disco, que son los que envejecen sin avisar.

    python3 evals/scripts/test_estado_del_proyecto.py
"""
import re
import subprocess
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DOC = RAIZ / "docs" / "ESTADO-DEL-PROYECTO.md"
SKILLS = RAIZ / "plugins" / "despacho" / "skills"
SCRIPTS = RAIZ / "plugins" / "despacho" / "scripts"


def texto():
    return DOC.read_text(encoding="utf-8")


def seccion0():
    t = texto()
    i = t.index(u"## §0 — Dónde estamos")
    return t[i:t.index(u"## §0.bis")]


class LosTitularesSiguenSiendoCiertos(unittest.TestCase):

    def test_1_hay_remoto(self):
        """§0.1: «Se puede instalar». En agosto era falso."""
        r = subprocess.run(["git", "remote", "-v"], cwd=str(RAIZ),
                           capture_output=True, text=True)
        self.assertIn("origin", r.stdout)
        self.assertTrue((RAIZ / ".claude-plugin" / "marketplace.json").exists()
                        or list(RAIZ.glob("**/marketplace.json")))

    def test_2_ningun_metodo_cita_una_norma(self):
        """§0.2, y es la regla dura 1 del producto."""
        patron = re.compile(r"Ley \d|Decreto \d|art\. \d")
        culpables = [p.parent.name for p in SKILLS.glob("*/SKILL.md")
                     if patron.search(p.read_text(encoding="utf-8"))]
        self.assertEqual([], culpables)

    def test_2bis_son_once_metodos(self):
        """El numero que mas veces se ha escrito mal en este repositorio."""
        metodos = sorted(p.parent.name for p in SKILLS.glob("*/SKILL.md"))
        self.assertEqual(11, len(metodos), metodos)
        self.assertIn(u"once métodos", seccion0())

    def test_3_los_once_estan_registrados_como_ejecutados(self):
        """§0.3: «los once se han ejecutado al menos una vez»."""
        notas = (RAIZ / "docs" / "technical-design" / "v0" / "notes-verification")
        registro = "\n".join(f.read_text(encoding="utf-8")
                             for f in notas.glob("pasada-*.md"))
        sin_registrar = [p.parent.name for p in SKILLS.glob("*/SKILL.md")
                         if p.parent.name not in registro]
        self.assertEqual([], sin_registrar,
                         "el §0.3 dice que los once se ejecutaron, y estos no "
                         "aparecen en ningun registro de pasada")

    def test_6_la_cadena_esta_completa(self):
        """§0.6: quien escribe la hoja, y quien se detiene sin la marca."""
        hechos = (SKILLS / "hechos-con-prueba" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(u"2-Borradores/Hechos - ", hechos)
        for consumidor in ("redactar-escrito", "inventario-de-anexos"):
            t = (SKILLS / consumidor / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(u"no hay hechos aprobados", t.lower(), consumidor)

    def test_7_la_cifra_de_fact_builder_es_la_que_se_escribio(self):
        """§0.7 dice «cincuenta y cinco documentos». Si cambia, se corrige aqui.

        No se renombran: son registro historico. Lo que no puede pasar es que
        la cifra del documento y la del disco dejen de ser la misma en silencio.
        """
        docs = RAIZ / "docs"
        cuantos = len([f for f in docs.rglob("*.md")
                       if "fact-builder" in f.read_text(encoding="utf-8", errors="replace")])
        self.assertEqual(55, cuantos,
                         "el §0.7 dice 55 y en el disco hay %d" % cuantos)

    def test_8_el_plugin_ejecuta_los_programas_que_dice(self):
        """§0.8: «hoy ejecuta diez programas»."""
        programas = sorted(p.name for p in SCRIPTS.glob("*.py"))
        self.assertEqual(10, len(programas), programas)
        self.assertIn(u"diez programas", seccion0())


class LoQueEsteArchivoNoComprueba(unittest.TestCase):
    """Declararlo es la mitad que importa de un instrumento."""

    def test_se_dice_cuales_son_juicios_y_no_hechos(self):
        """§0.4, §0.5, §0.9 y §0.10 no tienen respuesta en el disco.

        Cerrar hallazgos, que la guia se entienda, que el Knowledge Pack sea
        una abstinencia y que falten datos del trabajo real son lecturas, no
        cifras. Esta prueba NO las comprueba, y por eso las nombra: un lector
        que vea esta suite pasar no debe creer que valido los diez.
        """
        self.assertTrue(DOC.exists())

    def test_la_fecha_de_corte_esta_escrita(self):
        """Un estado sin fecha miente por omision -- la regla 4, aplicada aqui."""
        self.assertRegex(texto(), r"\*\*Fecha de corte:\*\* \d{4}-\d{2}-\d{2}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
