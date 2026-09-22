# -*- coding: utf-8 -*-
"""Que ningun programa del plugin reviente al faltarle una biblioteca.

`INSTALACION.md` hace una promesa comprobable y nadie la habia comprobado:

    «Las bibliotecas las pide cada programa cuando le hacen falta,
     DICIENDO CUAL.»

**Dos de los diez la rompian con un traceback de Python.** Uno era
`verificar_fidelidad.py`, que comprueba que el Word diga lo mismo que el `.md`
y **lo declaran nueve metodos**: reventar ahi es reventar el control de la
entrega, en la pantalla de quien instala y la primera vez que se instala.

Y por que importa mas de lo que parece: la instalacion es el item que bloquea
todo el proyecto, lleva abierto desde la primera fase, y **habria fallado por un
motivo que nadie habia mirado**. No por algo de la maquina de ella -- por esto.

    python3 evals/scripts/test_dependencias.py
"""
import ast
import shutil
import subprocess
import tempfile
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
SCRIPTS = RAIZ / "plugins" / "despacho" / "scripts"
INSTALACION = RAIZ / "plugins" / "despacho" / "INSTALACION.md"

# Las diez externas del plugin, con quien las usa. Ninguna esta instalada en
# el entorno donde corre esta suite, y eso es lo que la hace util.
#
# Las tres ultimas entraron el 2026-09-22 con `transcribir_audio.py`, y traen
# algo que las otras siete no tienen: **no hay camino degradado**. Sin
# `python-docx` la entrega sale en texto; sin `faster-whisper` no hay
# transcripcion ninguna. Por eso lo que se le exige a ese programa es lo
# mismo que a los demas y no menos: que lo DIGA, nombrando la biblioteca.
EXTERNAS = {
    "av": "decodificar el audio de origen",
    "faster_whisper": "reconocer el habla",
    "PIL": "imagenes (rotacion, realce)",
    "PyPDF2": "leer PDF, alternativa de pypdf",
    "cv2": "realce de imagen",
    "docx": "producir y comprobar el .docx",
    "numpy": "imagenes",
    "pypdf": "leer PDF",
    "rapidocr_onnxruntime": "reconocer texto en fotografias",
    "sherpa_onnx": "separar voces, sin ponerles nombre",
    # Solo las usa `alineacion_forzada.py`, y solo dentro de una funcion:
    # sin ese experimento el plugin no las necesita. Estan MEDIDAS como no
    # aptas para este material (CER mediana 0,60), asi que se declaran
    # aparte en INSTALACION.md y no se piden para el uso normal.
    "torch": "el experimento de alineacion forzada por CTC",
    "transformers": "el modelo acustico de ese experimento",
}


def externas_de(fichero):
    arbol = ast.parse(fichero.read_text(encoding="utf-8"))
    propios = {p.stem for p in SCRIPTS.glob("*.py")}
    mods = set()
    for n in ast.walk(arbol):
        if isinstance(n, ast.Import):
            mods |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
            mods.add(n.module.split(".")[0])
    return {m for m in mods
            if m not in sys.stdlib_module_names and m not in propios}


class NingunProgramaRevientaPorUnaBiblioteca(unittest.TestCase):
    """Se corre cada uno de verdad, no con --help.

    `--help` pasaba en los dos que reventaban: argparse contesta antes de que
    el programa llegue a importar nada. **Probar con --help era no probar.**
    """

    def _correr(self, nombre, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / nombre)] + list(args),
                              capture_output=True, text=True)

    def setUp(self):
        """Con archivos que EXISTEN, o el programa muere antes de importar nada.

        La primera version de estas pruebas pasaba rutas inventadas, y los
        programas morian en `FileNotFoundError` sin llegar al import -- de modo
        que la prueba «pasaba» sin probar lo que dice probar. **Y al arreglarlo
        aparecio un segundo defecto**: un archivo que no esta producia un
        traceback en vez de decirse.
        """
        self.tmp = Path(tempfile.mkdtemp())
        self.md = self.tmp / "a.md"
        self.md.write_text(u"# t\n\nhola\n", encoding="utf-8")
        self.docx = self.tmp / "a.docx"
        self.docx.write_bytes(b"PK\x03\x04")      # basta con que exista

    def tearDown(self):
        shutil.rmtree(str(self.tmp), ignore_errors=True)

    def test_verificar_fidelidad_declara(self):
        r = self._correr("verificar_fidelidad.py", str(self.docx), str(self.md))
        self.assertNotIn("Traceback", r.stderr + r.stdout)
        self.assertIn("python-docx", r.stderr + r.stdout)

    def test_md2docx_declara(self):
        r = self._correr("md2docx.py", str(self.md), str(self.docx))
        self.assertNotIn("Traceback", r.stderr + r.stdout)
        self.assertIn("python-docx", r.stderr + r.stdout)

    def test_un_archivo_que_no_esta_se_dice_no_se_revienta(self):
        """El segundo defecto, que solo aparecio al arreglar la prueba."""
        r = self._correr("verificar_fidelidad.py",
                         str(self.tmp / "no.docx"), str(self.tmp / "no.md"))
        self.assertNotIn("Traceback", r.stderr + r.stdout)
        self.assertIn("NO EXISTE", r.stderr + r.stdout)

    def test_transcribir_audio_declara(self):
        """El unico sin camino degradado, y por eso el que mas obliga a decirlo.

        Sin `faster-whisper` no hay transcripcion peor: no hay ninguna. Un
        traceback aqui es, ademas, el primer contacto de quien instala con el
        metodo mas nuevo del producto.
        """
        r = self._correr("transcribir_audio.py", str(self.tmp / "a.m4a"),
                         "--destino", str(self.tmp))
        salida = r.stderr + r.stdout
        self.assertNotIn("Traceback", salida)
        self.assertIn("falta una biblioteca", salida)
        self.assertIn("faster-whisper", salida)

    def test_los_tres_nuevos_que_no_dependen_de_nada_arrancan(self):
        """Los otros tres que trajo la fusion: ninguno importa nada de fuera."""
        for n in ("comparar_iteraciones.py", "md2html.py", "verificar_citas.py"):
            r = self._correr(n)
            self.assertNotIn("Traceback", r.stderr + r.stdout, n)

    def test_medir_realce_declara(self):
        r = self._correr("medir_realce.py")
        self.assertNotIn("Traceback", r.stderr + r.stdout)
        self.assertIn("pip install", r.stderr + r.stdout)

    def test_los_que_no_dependen_de_nada_arrancan(self):
        """Control positivo: si TODO reventara, los de arriba pasarian solos."""
        for n in ("contar_fichas.py", "estado_del_caso.py", "traer_modelos.py"):
            r = self._correr(n, "--help")
            self.assertEqual(0, r.returncode, n + ": " + r.stderr[:200])

    def test_buscar_y_preparar_arrancan_sin_sus_bibliotecas(self):
        """Los dos que ya lo hacian bien, para que no se rompa."""
        for n in ("buscar.py", "preparar_material.py"):
            r = self._correr(n, "--help")
            self.assertEqual(0, r.returncode, n)
            self.assertNotIn("Traceback", r.stderr)


class LaPromesaDeINSTALACIONEsCierta(unittest.TestCase):

    def test_el_documento_sigue_haciendo_esa_promesa(self):
        """Si se quita la promesa, estas pruebas dejan de tener objeto."""
        t = INSTALACION.read_text(encoding="utf-8")
        self.assertIn(u"las pide cada programa cuando le hacen falta", t)

    def test_y_ahora_dice_cuales_son(self):
        """La promesa sola no basta: quien instala quiere la lista antes."""
        t = INSTALACION.read_text(encoding="utf-8")
        for paquete in ("python-docx", "pillow", "numpy", "rapidocr",
                        "faster-whisper", "av", "sherpa-onnx"):
            self.assertIn(paquete, t.lower(), paquete)

    def test_no_hay_una_dependencia_mas_sin_declarar(self):
        """El canario: una biblioteca nueva obliga a decidir y a documentarla."""
        halladas = set()
        for f in sorted(SCRIPTS.glob("*.py")):
            halladas |= externas_de(f)
        self.assertEqual(sorted(EXTERNAS), sorted(halladas),
                         "hay una dependencia que este archivo no conoce: "
                         "clasifiquela y añadala a INSTALACION.md")

    def test_ningun_programa_importa_de_fuera_del_plugin(self):
        """Lo que funcionaria aqui y fallaria en su maquina.

        Un programa del plugin que importara algo de `evals/` correria en este
        repositorio y moriria al instalarse, porque `evals/` no viaja.
        """
        propios = {p.stem for p in SCRIPTS.glob("*.py")}
        for f in sorted(SCRIPTS.glob("*.py")):
            arbol = ast.parse(f.read_text(encoding="utf-8"))
            for n in ast.walk(arbol):
                if isinstance(n, ast.ImportFrom) and n.module:
                    raiz_mod = n.module.split(".")[0]
                    if raiz_mod in ("evals", "docs", "tests"):
                        self.fail("%s importa de %s, que no viaja con el plugin"
                                  % (f.name, raiz_mod))
                    if raiz_mod not in sys.stdlib_module_names and \
                            raiz_mod not in EXTERNAS and raiz_mod not in propios:
                        self.fail("%s importa %s, desconocido" % (f.name, raiz_mod))


if __name__ == "__main__":
    unittest.main(verbosity=2)
