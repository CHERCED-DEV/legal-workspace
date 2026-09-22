# -*- coding: utf-8 -*-
"""Regresión de `estado_del_caso.py` — SPEC-06.

Cada test afirma **una** de las reglas duras de la spec, y cada uno **puede
fallar**: si mañana alguien hace que el programa reescriba el archivo entero,
o que escriba sin la línea marcadora, o que copie la cola por la vía del
texto en vez de por la de los bytes, aquí se cae algo.

El test que importa más que todos es `test_cola_identica_byte_a_byte`, y su
control positivo está al lado: `test_la_cabecera_si_cambia`. Sin él, un
programa que no escribiera nada pasaría el primero con nota perfecta.

    python3 -m unittest discover -s evals/scripts -v
"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PROGRAMA = RAIZ / "plugins" / "despacho" / "scripts" / "estado_del_caso.py"

CABECERA_VIEJA = (
    "ESTADO DEL CASO — Ríos\n"
    "Revisado el 2026-08-27.\n"
    "\n"
    "EN QUÉ VA\n"
    "  lo que decía la pasada anterior\n"
    "\n"
)
# Con tildes, comillas españolas, guiones largos y un signo de apertura:
# justo lo que una re-emisión token a token normaliza sin que se note.
NOTAS_DE_ELLA = (
    "NOTAS SUYAS (el sistema no toca esta parte)\n"
    "  Llamé a la señora Ríos el 3/IX. Dijo que el acta está en Armenia.\n"
    "  OJO: la numeración de anexos va corrida — ¿confirmar con el juzgado?\n"
    "  «lo del año pasado»\tquedó pendiente\n"
    "\n"
    "Revisiones anteriores\n"
    "  2026-08-27 — primera revisión\n"
)
CABECERA_NUEVA = (
    "ESTADO DEL CASO — Ríos\n"
    "Revisado el 2026-09-05.\n"
    "\n"
    "EN QUÉ VA\n"
    "  lo que dicen hoy los documentos\n"
)


class Base(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.caso = self.tmp / "Caso Ríos"
        (self.caso / "1-Documentos recibidos").mkdir(parents=True)
        (self.caso / "2-Borradores").mkdir(parents=True)
        self.estado = self.caso / "0-Estado del caso (no editar).txt"
        self.cabecera = self.tmp / "cabecera.txt"
        self.cabecera.write_text(CABECERA_NUEVA, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def correr(self, *args):
        r = subprocess.run([sys.executable, str(PROGRAMA), str(self.caso)] + list(args),
                           capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def poblar(self, codec="utf-8"):
        self.estado.write_bytes(CABECERA_VIEJA.encode(codec) + NOTAS_DE_ELLA.encode(codec))
        return NOTAS_DE_ELLA.encode(codec)

    def copias(self):
        return sorted((self.caso / "2-Borradores").glob("0-Estado*"))


class LoDeElla(Base):
    """R-1 · lo que ella escribió no vuelve a pasar por el modelo."""

    def test_cola_identica_byte_a_byte(self):
        cola = self.poblar()
        rc, salida = self.correr("--cabecera", str(self.cabecera))
        self.assertEqual(0, rc, salida)
        self.assertTrue(self.estado.read_bytes().endswith(cola))

    def test_la_cabecera_si_cambia(self):
        """Control positivo: sin esto, un programa que no escriba nada pasa."""
        self.poblar()
        self.correr("--cabecera", str(self.cabecera))
        quedo = self.estado.read_text(encoding="utf-8")
        self.assertIn("lo que dicen hoy los documentos", quedo)
        self.assertNotIn("lo que decía la pasada anterior", quedo)

    def test_archivo_de_windows_en_cp1252(self):
        """Su equipo no escribe UTF-8 necesariamente. Los bytes son los bytes."""
        cola = self.poblar(codec="cp1252")
        rc, salida = self.correr("--cabecera", str(self.cabecera))
        self.assertEqual(0, rc, salida)
        self.assertTrue(self.estado.read_bytes().endswith(cola))

    def test_no_saca_las_notas_por_pantalla(self):
        """Lo que no se imprime no se puede re-emitir parafraseado."""
        self.poblar()
        _, salida = self.correr("--cabecera", str(self.cabecera))
        for suyo in ("Armenia", "numeración", "juzgado", "año pasado"):
            self.assertNotIn(suyo, salida)


class SinMarcaNoSeEscribe(Base):
    """R-2 · sin la línea marcadora no hay forma de saber dónde empieza lo suyo."""

    def test_sin_marca_no_toca_el_archivo(self):
        a_mano = "ESTADO DEL CASO — Ríos\nesto lo escribió ella entero, sin plantilla\n"
        self.estado.write_text(a_mano, encoding="utf-8")
        rc, salida = self.correr("--cabecera", str(self.cabecera))
        self.assertEqual(3, rc, salida)
        self.assertEqual(a_mano, self.estado.read_text(encoding="utf-8"))

    def test_sin_marca_tampoco_deja_copia(self):
        self.estado.write_text("sin marca\n", encoding="utf-8")
        self.correr("--cabecera", str(self.cabecera))
        self.assertEqual([], self.copias())

    def test_la_marca_se_reconoce_en_minusculas(self):
        self.estado.write_text(CABECERA_VIEJA + "Notas suyas (el sistema no toca esta parte)\n  algo\n",
                               encoding="utf-8")
        rc, salida = self.correr("--cabecera", str(self.cabecera))
        self.assertEqual(0, rc, salida)


class LaCopiaPrevia(Base):
    """R-3 · sin copia no se toca el archivo (H-11)."""

    def test_deja_copia_del_original_entero(self):
        self.poblar()
        antes = self.estado.read_bytes()
        self.correr("--cabecera", str(self.cabecera))
        self.assertEqual(1, len(self.copias()))
        self.assertEqual(antes, self.copias()[0].read_bytes())

    def test_dos_pasadas_el_mismo_dia_no_se_pisan(self):
        self.poblar()
        self.correr("--cabecera", str(self.cabecera))
        self.correr("--cabecera", str(self.cabecera))
        self.assertEqual(2, len(self.copias()))


class LaPrimeraVez(Base):
    """R-4 · crear no es reescribir, y no se hace por descuido."""

    def test_no_crea_sin_pedirselo(self):
        rc, salida = self.correr("--cabecera", str(self.cabecera))
        self.assertEqual(2, rc, salida)
        self.assertFalse(self.estado.exists())

    def test_con_crear_nace_con_el_bloque_de_ella(self):
        rc, salida = self.correr("--cabecera", str(self.cabecera), "--crear")
        self.assertEqual(0, rc, salida)
        self.assertIn("NOTAS SUYAS", self.estado.read_text(encoding="utf-8"))
        rc2, salida2 = self.correr("--cabecera", str(self.cabecera))
        self.assertEqual(0, rc2, salida2)


class Comprobar(Base):
    """`--comprobar` es lo que el método corre en la Fase 0: mira y no escribe."""

    def test_comprobar_no_escribe_ni_copia(self):
        self.poblar()
        antes = self.estado.read_bytes()
        rc, salida = self.correr("--comprobar")
        self.assertEqual(0, rc, salida)
        self.assertEqual(antes, self.estado.read_bytes())
        self.assertEqual([], self.copias())

    def test_comprobar_cuenta_sin_transcribir(self):
        self.poblar()
        _, salida = self.correr("--comprobar")
        self.assertIn("renglones", salida)
        self.assertNotIn("Armenia", salida)


if __name__ == "__main__":
    unittest.main(verbosity=2)
