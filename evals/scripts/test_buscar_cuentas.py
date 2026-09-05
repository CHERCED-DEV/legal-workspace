# -*- coding: utf-8 -*-
"""Que el detector de cuentas encienda donde debe y calle donde no.

Un aviso que enciende siempre no se mira nunca. La primera version de este
programa encendia con el verbo «llevar» en cualquier sentido -- «lleva rubrica»,
«lleva un solo estado» -- y esas dos lineas son la razon de la mitad de estas
pruebas.

    python3 evals/scripts/test_buscar_cuentas.py
"""
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import buscar_cuentas as B

MATERIAL = (Path(__file__).resolve().parents[1] / "casos"
            / "caso-03-hidraulica-desde-el-diseno" / "1-Documentos recibidos")


def hallar(texto, con_material=False):
    fd, ruta = tempfile.mkstemp(suffix=".md")
    os.close(fd)
    io.open(ruta, "w", encoding="utf-8").write(texto)
    try:
        m = B.material(str(MATERIAL)) if con_material else None
        return B.revisar(ruta, m)
    finally:
        os.unlink(ruta)


def expresiones(texto, **kw):
    return sorted(e for _, e, _, _, _ in hallar(texto, **kw))


class EnciendeDondeDebe(unittest.TestCase):

    def test_el_defecto_real_que_lo_origino(self):
        """«veintiún días de diferencia» entre dos actas: salio de una resta."""
        self.assertIn(u"veintiun dias de diferencia",
                      expresiones(u"Las dos actas, con veintiún días de diferencia."))

    def test_dias_despues(self):
        self.assertIn(u"tres dias despues",
                      expresiones(u"El acta se firmo tres días después."))

    def test_han_transcurrido(self):
        self.assertIn(u"han transcurrido mas de seis meses",
                      expresiones(u"Han transcurrido más de seis meses desde la entrega."))

    def test_vencimiento(self):
        self.assertTrue(hallar(u"El plazo venció el martes."))


class CallaDondeDebe(unittest.TestCase):

    def test_llevar_como_verbo_no_enciende(self):
        """Las dos lineas que hicieron inutil la primera version."""
        self.assertEqual([], expresiones(
            u"El acta lleva rúbrica bajo el rótulo del cliente."))
        self.assertEqual([], expresiones(u"Cada ficha lleva un solo estado."))

    def test_una_fecha_sola_no_es_una_cuenta(self):
        self.assertEqual([], expresiones(
            u"El acta de visita técnica es del 20 de junio de 2025."))

    def test_dos_fechas_entregadas_sin_restarlas_no_encienden(self):
        """Lo correcto de escribir, que es lo que reemplazo al defecto."""
        self.assertEqual([], expresiones(
            u"Las dos fechas son las que están escritas: 30 de mayo y 20 de junio de 2025."))


class ContrastarConElMaterial(unittest.TestCase):

    def test_lo_que_el_contrato_dice_se_marca_como_presente(self):
        """«Seis meses» esta en la clausula septima: citarlo es correcto."""
        r = hallar(u"El contrato fija una garantía de «seis meses» (DOC-01, cl. 7).",
                   con_material=True)
        self.assertTrue(r, "no encontro la expresion")
        self.assertTrue(all(en for _, _, _, en, _ in r),
                        "marca como ausente algo que el contrato dice")

    def test_lo_que_no_esta_se_marca_como_ausente(self):
        r = hallar(u"Entre las dos actas pasaron veintiún días.", con_material=True)
        self.assertTrue(r)
        self.assertFalse(any(en for _, _, _, en, _ in r))

    def test_la_salida_real_ya_no_afirma_ninguna_cuenta(self):
        """Control positivo sobre la pasada corregida.

        Lo unico que queda es la propia nota de correccion, que CITA la cifra
        para decir que no se escribe -- y va marcada como cita.
        """
        salida = (Path(__file__).resolve().parents[1] / "casos"
                  / "caso-03-hidraulica-desde-el-diseno" / "2-Borradores"
                  / "Hechos - Hidraulica - 2026-09-05.md")
        self.assertTrue(salida.exists())
        m = B.material(str(MATERIAL))
        afirmadas = [e for _, e, cita, en, _ in B.revisar(str(salida), m)
                     if not cita and en is False]
        self.assertEqual([], afirmadas, "hay una cuenta afirmada sin comillas")


class ImportesQueSalenDeUnaCuenta(unittest.TestCase):
    """El segundo defecto de la misma clase, en el mismo archivo.

    La salida escribio «la diferencia es de $500.000 en las dos cifras».
    4.800.000 menos 4.300.000. Esa cifra no esta en ninguna pieza, y la guarda
    de esa manana solo miraba fechas.
    """

    def _importes(self, texto):
        fd, ruta = tempfile.mkstemp(suffix=".md")
        os.close(fd)
        io.open(ruta, "w", encoding="utf-8").write(texto)
        try:
            return B.importes(ruta, B.material(str(MATERIAL)))
        finally:
            os.unlink(ruta)

    def test_la_resta_de_importes_se_detecta(self):
        r = self._importes(u"La diferencia es de $500.000 en las dos cifras.")
        self.assertEqual([u"500.000"], [c for c, _, _ in r])

    def test_los_importes_del_contrato_no_encienden(self):
        """Las cuatro cifras del caso estan escritas: citarlas es lo correcto."""
        r = self._importes(u"El contrato dice $4.800.000 de total y $2.800.000 "
                           u"de saldo; el correo dice $4.300.000 y $2.300.000. "
                           u"El anticipo fue de $2.000.000.")
        self.assertEqual([], r)

    def test_un_total_inventado_se_detecta(self):
        """El «total asciende a» que `inventario-de-bienes` prohibe por su nombre."""
        r = self._importes(u"Total de bienes: $7.100.000.")
        self.assertEqual([u"7.100.000"], [c for c, _, _ in r])

    def test_las_dos_salidas_reales_no_afirman_ningun_importe_calculado(self):
        borradores = (Path(__file__).resolve().parents[1] / "casos"
                      / "caso-03-hidraulica-desde-el-diseno" / "2-Borradores")
        m = B.material(str(MATERIAL))
        for f in sorted(borradores.glob("*.md")):
            afirmados = [c for c, cita, _ in B.importes(str(f), m) if not cita]
            self.assertEqual([], afirmados, "%s afirma un importe calculado" % f.name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
