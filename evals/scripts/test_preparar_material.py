# -*- coding: utf-8 -*-
"""El preparador, corrido de verdad sobre material que llega.

Es el unico metodo cuyo trabajo es integramente mecanico -- descomprimir,
copiar sin tocar, calcular huellas, detectar duplicados -- y por eso es el
unico que se puede probar de punta a punta sin un modelo.

Las dos cosas que estas pruebas fijan salieron de la PRIMERA corrida real, el
2026-09-07:

  * Pillow se exigia al arrancar, y hace falta solo para las imagenes. Un ZIP
    de .txt no se podia preparar, y `--help` tampoco funcionaba: el programa no
    podia decir como se usa sin una libreria que ese uso no necesita.
  * El registro se saltaba su seccion 2 en silencio cuando no habia imagenes,
    dejando un salto del 1 al 3. Todos los demas metodos dicen que una seccion
    quedo vacia en vez de borrarla, y por la misma razon: un salto no permite
    distinguir «no habia nada» de «se omitio algo».

    python3 evals/scripts/test_preparar_material.py
"""
import io
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PROGRAMA = RAIZ / "plugins" / "despacho" / "scripts" / "preparar_material.py"


def material_de_prueba(carpeta):
    """Un ZIP con cuatro archivos de texto, uno de ellos duplicado exacto."""
    z = carpeta / "material.zip"
    with zipfile.ZipFile(z, "w") as f:
        f.writestr("acta.txt", u"ACTA DE ENTREGA\nFecha: 3 de marzo de 2025\n")
        f.writestr("contrato.txt", u"CONTRATO\nValor: $1.000.000\n")
        f.writestr("copia del contrato.txt", u"CONTRATO\nValor: $1.000.000\n")
        f.writestr("sub/correo.txt", u"CORREO\nDe: alguien\n")
    return z


class ElPreparadorCorreSinPillow(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.zip = material_de_prueba(self.tmp)
        self.destino = self.tmp / "despacho"

    def tearDown(self):
        shutil.rmtree(str(self.tmp), ignore_errors=True)

    def correr(self, *args):
        return subprocess.run(
            [sys.executable, str(PROGRAMA), "--caso", "caso-prueba",
             "--destino", str(self.destino), str(self.zip)] + list(args),
            capture_output=True, text=True)

    def test_help_no_necesita_pillow(self):
        r = subprocess.run([sys.executable, str(PROGRAMA), "--help"],
                           capture_output=True, text=True)
        self.assertEqual(0, r.returncode)
        self.assertIn("--caso", r.stdout)
        self.assertNotIn("Falta Pillow", r.stdout + r.stderr)

    def test_un_zip_de_texto_se_prepara(self):
        r = self.correr()
        self.assertEqual(0, r.returncode, r.stderr)
        recibidos = self.destino / "caso-prueba" / "1-Documentos recibidos"
        self.assertEqual(4, len(list(recibidos.glob("*.txt"))))

    def test_el_original_se_copia_sin_tocarlo(self):
        self.correr()
        acta = (self.destino / "caso-prueba" / "1-Documentos recibidos" / "acta.txt")
        self.assertEqual(u"ACTA DE ENTREGA\nFecha: 3 de marzo de 2025\n",
                         acta.read_text(encoding="utf-8"))

    def test_el_duplicado_exacto_se_detecta(self):
        r = self.correr()
        self.assertIn("1 duplicados", r.stdout)


class ElRegistroNoSeSaltaSecciones(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.zip = material_de_prueba(self.tmp)
        self.destino = self.tmp / "despacho"
        subprocess.run(
            [sys.executable, str(PROGRAMA), "--caso", "caso-prueba",
             "--destino", str(self.destino), str(self.zip)],
            capture_output=True, text=True)
        borradores = self.destino / "caso-prueba" / "2-Borradores"
        self.registro = next(borradores.glob("Registro de ingesta*.md")).read_text(
            encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(str(self.tmp), ignore_errors=True)

    def test_la_seccion_2_existe_aunque_no_haya_imagenes(self):
        self.assertIn(u"## 2. Cómo se leyó", self.registro)

    def test_y_dice_que_quedo_vacia_y_por_que(self):
        self.assertIn(u"Vacía, y se dice", self.registro)
        self.assertIn(u"no hubo ninguna imagen que reconocer", self.registro)

    def test_no_deja_entender_que_todo_se_leyo_bien(self):
        """La mitad que importa de decir que algo quedo vacio."""
        self.assertIn(u"no significa que todo se haya", self.registro)

    def test_las_tres_secciones_van_en_orden(self):
        i1 = self.registro.index(u"## 1.")
        i2 = self.registro.index(u"## 2.")
        i3 = self.registro.index(u"## 3.")
        self.assertLess(i1, i2)
        self.assertLess(i2, i3)

    def test_el_registro_no_se_cita_como_origen(self):
        self.assertIn(u"Trabajo, no evidencia", self.registro)


if __name__ == "__main__":
    unittest.main(verbosity=2)
