# -*- coding: utf-8 -*-
"""Regresión de `buscar.py` — lo que la búsqueda NO puede dejar de decir.

Salió de correr el programa de verdad contra `caso-02` el 2026-09-05: devolvía
el trabajo del propio sistema mezclado con el material, en una sola lista y sin
decirlo. Una aparición dentro de una hoja de hechos marcada ` - REVISADO` tiene
aspecto de fuente autorizada **y no lo es para esto**.

    python3 evals/scripts/test_buscar.py
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PROGRAMA = RAIZ / "plugins" / "despacho" / "scripts" / "buscar.py"
CASO = RAIZ / "evals" / "casos" / "caso-02-sintetico-autoridad"


def correr(*args):
    r = subprocess.run([sys.executable, str(PROGRAMA), str(CASO)] + list(args),
                       capture_output=True, text=True)
    return r.stdout


class LaBusquedaDiceQueEsMaterialYQueNo(unittest.TestCase):

    def test_marca_lo_que_no_es_material(self):
        s = correr("cerca")
        self.assertIn("2-Borradores/Hechos - Salento - 2026-04-10.md   <- NO es material", s)
        self.assertIn("3-Para presentar/proyecto-resolucion.txt   <- NO es material", s)

    def test_no_marca_lo_que_si_lo_es(self):
        """Control positivo: sin esto, marcarlo TODO pasaría el anterior."""
        s = correr("cerca")
        for linea in s.splitlines():
            if linea.startswith("### 1-Documentos recibidos"):
                self.assertNotIn("NO es material", linea)
        self.assertIn("### 1-Documentos recibidos/acta-inspeccion.txt", s)

    def test_cuenta_cuantas_estan_fuera(self):
        s = correr("cerca")
        self.assertIn("De estas apariciones, 5 estan FUERA de 1-Documentos recibidos", s)

    def test_una_hoja_marcada_revisado_tambien_se_marca(self):
        """El caso peligroso: parece fuente autorizada y no lo es para esto."""
        s = correr("cerca")
        self.assertIn("REVISADO.md.md   <- NO es material", s)


class LoQueNuncaSeDejaDeDecir(unittest.TestCase):

    def test_el_descargo_sale_con_resultados(self):
        self.assertIn("cero resultados NO significa que no este en el papel", correr("cerca"))

    def test_el_descargo_sale_tambien_sin_resultados(self):
        s = correr("palabraqueseguronoesta")
        self.assertIn("CERO APARICIONES", s)
        self.assertIn("cero resultados NO significa que no este en el papel", s)

    def test_declara_cuantos_archivos_miro(self):
        self.assertIn("Se miraron", correr("cerca"))


class ElJsonDiceLoMismo(unittest.TestCase):

    def test_cada_hallazgo_lleva_su_origen(self):
        d = json.loads(correr("cerca", "--json"))
        self.assertEqual(5, d["fuera_de_recibidos"])
        self.assertEqual({"material", "otro"}, {x["origen"] for x in d["hallazgos"]})


if __name__ == "__main__":
    unittest.main(verbosity=2)
