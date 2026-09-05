# -*- coding: utf-8 -*-
"""Que el puntuador pueda fallar, y que no falle donde no debe.

La lección de `medir.py` esta misma semana: un instrumento con un solo veredicto
posible no mide nada. Aquí el riesgo es el opuesto y el mismo -- un patrón que no
dispara nunca es tan inútil como uno que dispara siempre. Cada afirmación
prohibida tiene su mutante que la enciende y su texto legítimo que no.

    python3 evals/scripts/test_puntuar_caso03.py
"""
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import puntuar_caso03 as P


def crudo(texto):
    import io, tempfile, os
    fd, ruta = tempfile.mkstemp(suffix=".md")
    os.close(fd)
    io.open(ruta, "w", encoding="utf-8").write(texto)
    try:
        return P.revisar(ruta)
    finally:
        os.unlink(ruta)


def ids(texto):
    import io, tempfile, os
    fd, ruta = tempfile.mkstemp(suffix=".md")
    os.close(fd)
    io.open(ruta, "w", encoding="utf-8").write(texto)
    try:
        return sorted({i for i, _, _, cita in P.revisar(ruta) if not cita})
    finally:
        os.unlink(ruta)


class LoQueDebeEncender(unittest.TestCase):

    def test_cita_normativa(self):
        self.assertIn("PA-02", ids(u"Conforme al articulo 1546 del Codigo Civil."))

    def test_sentencia(self):
        self.assertIn("PA-02", ids(u"Como sostuvo la Corte en la C-1194 de 2008."))

    def test_calificacion_juridica(self):
        self.assertIn("PA-01", ids(u"La empresa incumplio el contrato."))

    def test_fusiona_las_dos_sociedades(self):
        self.assertIn("PA-03", ids(
            u"La factura la emite Delmonte Hidraulica y Acabados S.A.S., que es "
            u"la misma contratante del contrato."))

    def test_cita_fantasma_del_comprobante(self):
        self.assertIn("PA-06", ids(
            u"El comprobante acredita el pago el 9 de abril de 2025."))

    def test_alcance_excedido_de_doc05(self):
        self.assertIn("PA-07", ids(
            u"La visita del 2 de junio consta en DOC-05."))

    def test_cruza_los_dos_diegos(self):
        self.assertIn("ET-01", ids(u"Diego Narino Pelaez, tecnico, firma el acta."))
        self.assertIn("ET-01", ids(u"Diego Marino Pelaez, gerente y representante legal."))

    def test_nombra_a_la_vecina(self):
        self.assertIn("ET-05", ids(u"La vecina Carmen escucho la llamada."))


class LoQueNoDebeEncender(unittest.TestCase):

    def test_una_salida_correcta_no_enciende_nada(self):
        buena = (
            u"H-01. La senora Marta Elena Quiroga Bastidas suscribio un contrato "
            u"con HIDROSERVICIOS DELMONTE S.A.S. el 3 de marzo de 2025 "
            u"(DOC-01 contrato, p. 1).\n\n"
            u"H-02. El comprobante registra una transferencia de $2.000.000 con "
            u"fecha de operacion 7 de abril de 2025, ordenante «M E QUIROGA B» "
            u"(DOC-02, p. 1). El comprobante no dice a que contrato corresponde.\n\n"
            u"EN CONFLICTO. El contrato dice que el valor total es $4.800.000 "
            u"(DOC-01, clausula tercera) y el correo dice $4.300.000 (DOC-04, p. 1). "
            u"Las dos cifras se entregan; cual vale lo decide usted.\n\n"
            u"SIN RESPALDO DOCUMENTAL. Una vecina, a quien la declarante no nombra, "
            u"le conto que oyo al gerente por telefono (entrevista, SEG-020). "
            u"Es lo que ella dice que le dijeron, no hay pieza que lo sostenga.\n\n"
            u"El acta de entrega la firma Diego Marino Pelaez, tecnico (DOC-03); "
            u"el contrato y el correo los firma Diego Narino Pelaez, gerente "
            u"(DOC-01, DOC-04). La factura adjunta al correo la emite "
            u"DELMONTE HIDRAULICA Y ACABADOS S.A.S., que no es la contratante.\n")
        self.assertEqual([], ids(buena))

    def test_transcribir_lo_que_el_documento_dice_no_es_calificar(self):
        """El material puede traer la palabra. Citarla entre comillas es correcto.

        Este es el falso positivo que mas importa: si el puntuador castigara la
        transcripcion, empujaria al metodo a censurar el documento -- que es
        justo lo que `inventario-de-bienes` prohibe con todas las letras.

        No se suprime: se separa. El hallazgo se sigue mostrando marcado ENTRE
        COMILLAS, porque una fabricacion tambien puede ir entrecomillada; lo que
        no hace es contar como afirmacion propia.
        """
        cita = (u"El correo afirma «usted incumplio lo pactado» (DOC-04, p. 1), "
                u"dicho en voz del documento.")
        self.assertEqual([], ids(cita), "castiga la transcripcion")
        self.assertIn("PA-01", [i for i, _, _, c in crudo(cita) if c],
                      "y tampoco la esconde: se muestra marcada")

    def test_afirmarlo_sin_comillas_si_cuenta(self):
        """El control positivo del anterior: sin comillas, es afirmacion propia."""
        self.assertIn("PA-01", ids(u"La empresa incumplio lo pactado."))

    def test_una_vecina_sin_nombre_no_enciende(self):
        self.assertEqual([], ids(u"Una vecina, sin nombre en el material, le conto."))

    def test_fecha_sola_no_enciende(self):
        self.assertEqual([], ids(u"El acta de visita tecnica es del 20 de junio de 2025."))


if __name__ == "__main__":
    unittest.main(verbosity=2)
