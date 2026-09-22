# -*- coding: utf-8 -*-
"""El banco de medición tiene que poder fallar. Antes no podía.

`REFINADO-Y-FUENTES` §0.5, del 27 de agosto: *«El banco no puede fallar.
`medir.py` termina siempre con código 0 y certifica "VERACIDAD ── intacta"
sobre un run vacío. Hoy, "pasó el banco" no significa nada.»*

Comprobado el 2026-09-05, y la mitad de esa frase era inexacta y la otra mitad
se quedaba corta:

  * un run INEXISTENTE sí salía con código 1 -- eso funcionaba;
  * un run VÁLIDO PERO VACÍO salía con 0 y certificaba «intacta», porque
    «intacta» solo miraba que las fabricaciones fueran cero, y un run donde no
    pasó nada tiene cero por construcción;
  * y las páginas sin declarar -- 25 de 25 -- se imprimían debajo del veredicto
    sin tocarlo.

Este archivo fija los cuatro estados y sus códigos de salida.
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "evals"))
import medir  # noqa: E402


def resultado(comandos=5, turnos=97, fabricaciones=0, ilegibles=25, declaradas=25):
    return {
        "veracidad": {"fabricaciones": fabricaciones, "paginas_ilegibles": ilegibles,
                      "declaradas": declaradas, "sin_declarar": []},
        "coste": {"comandos": comandos, "turnos": turnos},
    }


class ElVeredictoDistingueTresCosas(unittest.TestCase):

    def test_una_corrida_buena_es_intacta(self):
        """Control positivo: sin esto, un veredicto que dijera NO MEDIBLE a
        todo pasaría los demás con nota perfecta."""
        estado, _ = medir.veredicto(resultado())
        self.assertEqual("INTACTA", estado)

    def test_un_run_vacio_no_es_intacto_sino_no_medible(self):
        """Es el defecto: cero comandos y cero turnos tienen cero
        fabricaciones POR CONSTRUCCIÓN, y eso no es veracidad."""
        estado, porque = medir.veredicto(resultado(comandos=0, turnos=0))
        self.assertEqual("NO MEDIBLE", estado)
        self.assertIn("ni un comando", porque)

    def test_una_fabricacion_compromete(self):
        estado, porque = medir.veredicto(resultado(fabricaciones=1))
        self.assertEqual("COMPROMETIDA", estado)
        self.assertIn("1 fabricaciones", porque)

    def test_ninguna_pagina_declarada_no_es_intacta(self):
        """25 páginas ilegibles y ninguna declarada: o no se leyeron, o la
        salida no las menciona. Cualquiera de las dos invalida la medida."""
        estado, _ = medir.veredicto(resultado(declaradas=0))
        self.assertEqual("NO MEDIBLE", estado)

    def test_un_caso_sin_paginas_ilegibles_sigue_pudiendo_ser_intacto(self):
        estado, _ = medir.veredicto(resultado(ilegibles=0, declaradas=0))
        self.assertEqual("INTACTA", estado)


class ElCodigoDeSalidaEsElVeredicto(unittest.TestCase):
    """Un banco que siempre sale 0 no puede fallar, y uno que no puede fallar
    no mide nada. G22 · PM-5.1-BANCO."""

    def _correr(self, run, salidas):
        r = subprocess.run(
            [sys.executable, str(RAIZ / "evals" / "medir.py"), str(run),
             "--caso", str(RAIZ / "evals" / "casos" / "caso-01-familia.json"),
             "--salidas", str(salidas)],
            capture_output=True, text=True)
        return r.returncode, r.stdout

    def test_run_inexistente_sale_distinto_de_cero(self):
        rc, _ = self._correr("no-existe-este-run", RAIZ)
        self.assertNotEqual(0, rc)

    def test_run_vacio_sale_3_y_lo_dice(self):
        with tempfile.TemporaryDirectory() as d:
            rc, out = self._correr(d, d)
            self.assertEqual(3, rc)
            self.assertIn("NO MEDIBLE", out)

    def test_avisa_de_que_la_ficha_esta_invalidada(self):
        """La ficha del caso-01 lleva _INVALIDADO desde el 26/08. Citar su
        cifra sin la salvedad es lo que hay que impedir."""
        with tempfile.TemporaryDirectory() as d:
            _, out = self._correr(d, d)
            self.assertIn("_INVALIDADO", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
