# -*- coding: utf-8 -*-
"""Que el contador pueda fallar, y que no cuente de mas ni de menos.

El riesgo aqui es concreto y ya se materializo una vez: «Apoyado y contradicho»
empieza por «Apoyado», y un contador ingenuo lo suma a los apoyados. Esa es la
mitad de por que la cuenta a ojo salio mal.

    python3 evals/scripts/test_contar_fichas.py
"""
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import contar_fichas as C

SALIDA = (Path(__file__).resolve().parents[1] / "casos"
          / "caso-03-hidraulica-desde-el-diseno" / "2-Borradores"
          / "Hechos - Hidraulica - 2026-09-05.md")


def doc(*fichas):
    return "\n".join("## %s — enunciado\n\n- **Estado:** %s\n" % f for f in fichas)


class ContarPorEstado(unittest.TestCase):

    def test_apoyado_y_contradicho_no_cuenta_como_apoyado(self):
        """El fallo concreto que este archivo existe para impedir."""
        _, por, _ = C.contar(doc(("H-01", "Apoyado."),
                                 ("H-02", "Apoyado y contradicho.")))
        self.assertEqual(1, por["Apoyado"])
        self.assertEqual(1, por["Apoyado y contradicho"])

    def test_un_estado_con_coletilla_sigue_contando(self):
        _, por, sin = C.contar(doc(("H-01", "Apoyado y contradicho (en el saldo).")))
        self.assertEqual(1, por["Apoyado y contradicho"])
        self.assertEqual([], sin)

    def test_un_sexto_estado_inventado_se_denuncia(self):
        """La Fase 5 dice que los estados son los que son: no hay un sexto."""
        _, _, sin = C.contar(doc(("H-01", "Parcialmente apoyado.")))
        self.assertEqual(1, len(sin))
        self.assertIn("H-01", sin[0])

    def test_una_ficha_sin_estado_se_denuncia(self):
        fichas, _, sin = C.contar("## H-01 — enunciado\n\nsin la linea de estado\n")
        self.assertEqual(["H-01"], fichas)
        self.assertEqual(["H-01"], sin)


class ContrastarConLoDeclarado(unittest.TestCase):

    def test_detecta_el_conteo_mal_escrito(self):
        """Reproduce el fallo real: se declararon 10 y 7 donde habia 9 y 6."""
        cuerpo = doc(*[("H-%02d" % i, "Apoyado.") for i in range(1, 10)]
                     + [("H-%02d" % i, "Sin apoyo.") for i in range(10, 16)])
        malo = cuerpo + u"\n**15 hechos propuestos** · **10 apoyados** · **7 sin apoyo**\n"
        d = C.conteo_escrito(malo)
        _, por, _ = C.contar(malo)
        self.assertEqual(10, d["Apoyado"])
        self.assertEqual(9, por["Apoyado"])

    def test_la_salida_real_del_caso_03_cuadra(self):
        """Y el control positivo: la pasada corregida coincide consigo misma."""
        self.assertTrue(SALIDA.exists(), SALIDA)
        self.assertEqual(0, C.main([str(SALIDA)]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
