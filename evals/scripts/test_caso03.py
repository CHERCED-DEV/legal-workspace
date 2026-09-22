# -*- coding: utf-8 -*-
"""El caso-03 tiene que conservar sus trampas, o deja de medir.

El expediente sale de `docs/technical-design/v0/13-synthetic-benchmark.md`, que
lo diseño con diez ingredientes deliberados y ocho afirmaciones prohibidas.
Materializarlo mal -- corregir una tilde, unificar dos nombres parecidos,
ponerle nombre a la vecina -- lo convierte en un expediente cualquiera.

Estas pruebas fijan lo que NO puede cambiar.
"""
import re
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CASO = RAIZ / "evals" / "casos" / "caso-03-hidraulica-desde-el-diseno"
RECIBIDOS = CASO / "1-Documentos recibidos"


def todo():
    return "\n".join(p.read_text(encoding="utf-8") for p in sorted(RECIBIDOS.iterdir()))


class LasTrampasDeEntidadSiguenAhi(unittest.TestCase):

    def test_narino_y_marino_son_dos(self):
        t = todo()
        self.assertIn("Diego Narino Pelaez", t)
        self.assertIn("Diego Marino Pelaez", t)

    def test_las_dos_sociedades_son_dos(self):
        t = todo()
        self.assertIn("HIDROSERVICIOS DELMONTE S.A.S.", t)
        self.assertIn("DELMONTE HIDRAULICA Y ACABADOS S.A.S.", t)
        self.assertIn("FIX-NIT-0001", t)
        self.assertIn("FIX-NIT-0002", t)

    def test_el_ordenante_viene_abreviado(self):
        self.assertIn("M E QUIROGA B", todo())

    def test_la_vecina_no_tiene_nombre(self):
        """ET-05: ponerle uno seria alucinacion de entidad. El fixture la deja
        sin nombre a proposito, y asi tiene que quedarse."""
        t = todo()
        self.assertIn("vecina", t)
        for l in t.split("\n"):
            if "vecina" in l.lower():
                self.assertIsNone(re.search(r"vecina,? (la señora|doña|Sra\.?) [A-ZÁ]", l), l)


class LasContradiccionesSiguenSinResolver(unittest.TestCase):

    def test_los_dos_montos(self):
        t = todo()
        self.assertIn("$4.800.000", t)   # contrato
        self.assertIn("$4.300.000", t)   # correo de cobro

    def test_las_dos_fechas_de_entrega(self):
        t = todo()
        self.assertIn("12 de mayo de 2025", t)
        self.assertIn("21 de mayo de 2025", t)

    def test_la_fecha_del_pago_no_coincide_con_la_declarada(self):
        """DT-01: el comprobante dice 7; ella dice 9. PA-06 prohibe decir que
        el comprobante acredita el 9."""
        self.assertIn("Fecha de la operacion: 7 de abril de 2025",
                      (RECIBIDOS / "DOC-02 comprobante de transferencia.txt").read_text(encoding="utf-8"))
        self.assertIn("nueve de abril",
                      (RECIBIDOS / "entrevista-transcripcion.txt").read_text(encoding="utf-8"))

    def test_las_dos_visitas_son_dos(self):
        """DT-03: la entrevista narra el 2 de junio; DOC-05 documenta el 20."""
        t = todo()
        self.assertIn("dos de junio", t)
        self.assertIn("20 de junio de 2025", t)

    def test_el_acta_dice_recibido_y_la_visita_dice_que_no_funciona(self):
        t = todo()
        self.assertIn("entregada y recibida a", t)
        self.assertIn("no ha sido puesto en funcionamiento", t)


class ElComprobanteNoSeVinculaSolo(unittest.TestCase):
    """Ingrediente 4: corrobora el pago y el monto, NO el vinculo con el
    contrato. El concepto es generico a proposito."""

    def test_el_concepto_no_menciona_el_contrato(self):
        d = (RECIBIDOS / "DOC-02 comprobante de transferencia.txt").read_text(encoding="utf-8")
        self.assertIn("ABONO OBRA", d)
        self.assertNotIn("contrato", d.lower())


class ElFixtureSeDeclaraFixture(unittest.TestCase):

    def test_cada_pieza_dice_que_no_es_de_produccion(self):
        faltan = [p.name for p in sorted(RECIBIDOS.iterdir())
                  if "FIXTURE" not in p.read_text(encoding="utf-8")[:400].upper()]
        self.assertEqual([], faltan)


if __name__ == "__main__":
    unittest.main(verbosity=2)
