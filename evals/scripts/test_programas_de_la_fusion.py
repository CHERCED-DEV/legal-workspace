# -*- coding: utf-8 -*-
"""Los tres programas que llegaron el 2026-09-22 sin una sola prueba.

De los catorce programas del plugin, cuatro entraron por la fusion. Uno de
ellos --`transcribir_audio.py`-- no se puede probar aqui: sus bibliotecas no
estan en este entorno, y de el solo se comprueba que declare cual le falta
(`test_dependencias.py`). **Los otros tres no dependen de nada y se probaron
cero veces.**

Y los tres traen, en su propio codigo o en su historia de commits, **un
defecto ya corregido y sin prueba que lo sujete**:

  · `verificar_citas.py` -- «aprobaba en blanco toda cita de menos de cuatro
    palabras». En un programa cuyo unico trabajo es cazar citas inventadas,
    un aprobado en blanco es peor que no tenerlo.
  · `comparar_iteraciones.py` -- «rellenaba la lista hasta N», haciendo pasar
    por dudoso lo que no lo era.
  · `md2html.py` -- su ADR (020 §3) exige **cero peticiones de red**, porque
    una pagina que pide algo a un servidor cuenta lo que ella esta leyendo.
    Esa es la clase de invariante que se cumple el dia que se escribe y se
    rompe callando el dia que alguien anade una tipografia bonita.

Una correccion sin prueba es una correccion que se puede deshacer sin que
nadie se entere.

    python3 evals/scripts/test_programas_de_la_fusion.py
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
SCRIPTS = RAIZ / "plugins" / "despacho" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import verificar_citas as VC
import comparar_iteraciones as CI


def escribir(ruta, texto):
    """Con el archivo cerrado. Un descriptor abierto por prueba ensucia la salida."""
    with io.open(str(ruta), "w", encoding="utf-8") as f:
        f.write(texto)


def transcripcion(texto):
    """Un `Transcripcion*.md` minimo, con la forma que `cargar` espera."""
    return u"# TRANSCRIPCIÓN — x\n\n**[00:00:01]** «H1» %s\n" % texto


class ElAprobadoEnBlancoNoVuelve(unittest.TestCase):
    """El defecto del 2026-09-19, con prueba que lo sujeta en los dos sentidos."""

    FUENTE = u"la administradora entrego el acta de la reunion del martes"

    def _puntuar(self, cita):
        return VC.puntuar(cita, VC.norm(self.FUENTE))

    def test_una_cita_corta_que_SI_esta_puntua_alto(self):
        self.assertGreater(self._puntuar(u"el acta de la reunion"), 0.97)

    def test_una_cita_corta_que_NO_esta_puntua_bajo(self):
        """Tres palabras. Antes del 19/09 salia con 1.0 sin comprobarse."""
        self.assertLessEqual(self._puntuar(u"el acta notarial"), 0.97)

    def test_dos_palabras_tampoco_se_aprueban_solas(self):
        """El minimo es de DOS palabras, no de cuatro. Debajo de dos no hay que cotejar."""
        self.assertLessEqual(self._puntuar(u"acta notarial"), 0.97)

    def test_el_peor_tramo_manda_sobre_los_puntos_suspensivos(self):
        """Una cita partida con […] vale lo que valga su MITAD peor.

        Es lo que impide que una mitad textual arrastre a una inventada.
        """
        buena = u"la administradora entrego"
        mala = u"el certificado de libertad"
        self.assertGreater(self._puntuar(buena), 0.97)
        self.assertLessEqual(self._puntuar(u"%s […] %s" % (buena, mala)), 0.97)

    def test_una_palabra_sola_no_rompe_el_programa(self):
        """El `if not partes` existe para esto. Sin el, `peor` sale 1.0 intacto."""
        self.assertIsInstance(self._puntuar(u"acta"), float)


class LoQueVerificarCitasComprueba(unittest.TestCase):
    """De punta a punta, y sobre una carpeta de verdad."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.carpeta = self.tmp / "pasada-1"
        self.carpeta.mkdir()
        escribir(self.carpeta / "Transcripcion - a - 2026-09-22.md",
                 transcripcion(u"la administradora entrego el acta de la reunion "
                               u"del martes y dijo que el pago se hizo por "
                               u"transferencia"))

    def tearDown(self):
        shutil.rmtree(str(self.tmp), ignore_errors=True)

    def _doc(self, cuerpo):
        f = self.tmp / "d.md"
        escribir(f, cuerpo)
        return str(f)

    def test_una_cita_textual_pasa(self):
        d = self._doc(u"Dijo «la administradora entrego el acta de la reunion».")
        self.assertEqual(0, VC.main(d, [str(self.carpeta)]))

    def test_una_cita_inventada_no_pasa(self):
        """Cambiar UNA palabra. Es el defecto original de este programa."""
        d = self._doc(u"Dijo «la administradora entrego el acta de la asamblea».")
        self.assertEqual(1, VC.main(d, [str(self.carpeta)]))

    def test_una_carpeta_sin_transcripciones_se_dice_y_no_se_aprueba(self):
        """El modo de fallo peor: aprobar por no haber tenido con que comparar."""
        vacia = self.tmp / "vacia"
        vacia.mkdir()
        d = self._doc(u"Dijo «cualquier cosa que no este en ningun sitio».")
        self.assertEqual(2, VC.main(d, [str(vacia)]))

    def test_con_varias_carpetas_basta_una(self):
        """Para los documentos que comparan iteraciones: cada cita es de una."""
        otra = self.tmp / "pasada-2"
        otra.mkdir()
        escribir(otra / "Transcripcion - a - 2026-09-22.md",
                 transcripcion(u"el pago se hizo por transferencia"))
        d = self._doc(u"Uno «la administradora entrego el acta de la reunion» "
                      u"y dos «el pago se hizo por transferencia».")
        self.assertEqual(0, VC.main(d, [str(self.carpeta), str(otra)]))


class NoSeRellenaLaListaDeDiscrepancias(unittest.TestCase):
    """El defecto del comparador: «ocho peores no son ocho problemas»."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(str(self.tmp), ignore_errors=True)

    def _carpeta(self, nombre, texto):
        c = self.tmp / nombre
        (c / "datos").mkdir(parents=True)
        pal = texto.split()
        doc = {"duracion_s": 40.0, "segmentos": [{
            "i": 0, "inicio": 0.0, "fin": 40.0, "texto": texto,
            "palabras": [{"p": p, "i": float(i), "f": float(i) + 0.9}
                         for i, p in enumerate(pal)]}]}
        escribir(c / "datos" / "A1 - datos completos.json",
                 json.dumps({"publicada": doc, "ventanas": [{"medio": 0.9}]}))
        return str(c)

    def _correr(self, *carpetas):
        r = subprocess.run([sys.executable, str(SCRIPTS / "comparar_iteraciones.py")]
                           + list(carpetas), capture_output=True, text=True)
        return r

    def test_dos_carpetas_identicas_no_listan_ni_un_tramo(self):
        """Lo que el defecto hacia: sacar los N peores aunque no discrepara nadie."""
        t = u"la administradora entrego el acta de la reunion del martes pasado"
        r = self._correr(self._carpeta("a", t), self._carpeta("b", t))
        self.assertEqual(0, r.returncode, r.stderr[:300])
        self.assertIn("Ninguno: las versiones no se contradicen", r.stdout)

    def test_dos_carpetas_distintas_si_listan(self):
        """Control positivo: si nunca listara nada, el test de arriba pasaria solo."""
        r = self._correr(
            self._carpeta("a", u"la administradora entrego el acta del martes"),
            self._carpeta("b", u"ninguna otra frase parecida ocurre jamas aqui"))
        self.assertEqual(0, r.returncode, r.stderr[:300])
        self.assertIn("acuerdo medio", r.stdout)

    def test_una_sola_carpeta_no_compara_nada(self):
        r = self._correr(self._carpeta("a", u"algo"))
        self.assertEqual(2, r.returncode)

    def test_una_carpeta_sin_datos_se_dice_y_no_se_compara(self):
        vacia = self.tmp / "vacia"
        vacia.mkdir()
        r = self._correr(self._carpeta("a", u"algo mas largo aqui"), str(vacia))
        self.assertEqual(2, r.returncode)
        self.assertIn("No se comparo nada", r.stderr)

    def test_el_acuerdo_de_un_texto_consigo_mismo_es_uno(self):
        doc = {"duracion_s": 20.0, "segmentos": [{
            "i": 0, "inicio": 0.0, "fin": 20.0, "texto": u"a b c",
            "palabras": [{"p": p, "i": float(i), "f": float(i) + .5}
                         for i, p in enumerate(u"a b c".split())]}]}
        self.assertAlmostEqual(1.0, CI.acuerdo(doc, doc, 20.0))


class LaPaginaNoPideNadaAUnServidor(unittest.TestCase):
    """`ADR-020` §3: «Cero red. Ni una peticion.»

    La razon no es de rendimiento: **una pagina que pide algo a un servidor
    cuenta lo que esta leyendo**. Es aplicacion directa de ADR-001.

    Esta es la guarda de un invariante que hoy se cumple y que se rompe
    callando: nadie ve la peticion, la pagina se ve igual de bien, y el
    unico sintoma esta en un registro que no es nuestro.
    """

    # El espacio de nombres de SVG es un IDENTIFICADOR, no una direccion: el
    # navegador no lo pide. Es la unica `http://` legitima de una pagina.
    PERMITIDAS = ("http://www.w3.org/2000/svg",
                  "http://www.w3.org/1999/xhtml")

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.md = self.tmp / "e.md"
        escribir(self.md,
                 u"# Título\n\nUn párrafo con «una cita larga de prueba aquí».\n\n"
                 u"| a | b |\n|---|---|\n| 1 | 2 |\n\n- uno\n- dos\n")
        self.html = self.tmp / "s.html"
        r = subprocess.run([sys.executable, str(SCRIPTS / "md2html.py"),
                            str(self.md), str(self.html)],
                           capture_output=True, text=True)
        self.assertEqual(0, r.returncode, r.stderr[:400])
        self.pagina = self.html.read_text(encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(str(self.tmp), ignore_errors=True)

    def test_ni_una_direccion_de_red(self):
        fuera = [u for u in re.findall(r"https?://[^\s\"'<>)]+", self.pagina)
                 if not u.startswith(self.PERMITIDAS)]
        self.assertEqual([], sorted(set(fuera)),
                         u"la página pide algo a un servidor: ADR-020 §3")

    def test_ni_un_src_ni_un_href_a_otro_sitio(self):
        """Tambien sin protocolo: `//cdn...` hereda el del documento."""
        refs = re.findall(r"""(?:src|href)\s*=\s*["']([^"']+)["']""", self.pagina)
        fuera = [r for r in refs
                 if r.startswith("//") or re.match(r"^[a-z]+:", r)
                 and not r.startswith(("#", "data:"))]
        self.assertEqual([], sorted(set(fuera)), u"referencia a otro origen")

    def test_ni_una_tipografia_remota(self):
        """La forma concreta en que esto se rompe, y la mas facil de colar."""
        for palabra in ("@import", "fonts.googleapis", "fonts.gstatic",
                        "cdn.jsdelivr", "cdnjs", "unpkg"):
            self.assertNotIn(palabra, self.pagina, palabra)

    def test_la_prueba_mira_una_pagina_de_verdad(self):
        """Control positivo: sobre un archivo vacio, todo lo de arriba pasaria."""
        self.assertGreater(len(self.pagina), 5000)
        self.assertIn(u"Título", self.pagina)
        self.assertIn("<style", self.pagina)

    def test_el_contenido_sale_del_markdown_y_no_se_inventa(self):
        """`ADR-020` §2: nada se redacta en HTML; la pagina es derivada."""
        self.assertIn(u"una cita larga de prueba aquí", self.pagina)
        self.assertIn("<table", self.pagina)

    def test_sin_audio_la_ausencia_SE_DECLARA(self):
        """`ADR-020` §5, y no es lo que parece a primera vista.

        La pagina trae siempre el elemento `<audio>`, **vacio y oculto**, y
        declara la ausencia con todas las letras. Esa es la forma correcta:
        el reproductor no se promete, y lo que ella ve dicho es que no se
        puede comprobar oyendo. Una pagina que simplemente no trajera nada
        dejaria a quien la lee sin saber si falta el audio o si este material
        no lo tiene.
        """
        self.assertIn(u"No se encontró la grabación", self.pagina)
        self.assertIn(u"no se puede comprobar oyendo", self.pagina)

    def test_sin_audio_el_elemento_va_vacio(self):
        """Lo que si seria un defecto: un `src` apuntando a algo que no esta."""
        m = re.search(r"<audio[^>]*>", self.pagina)
        self.assertIsNotNone(m, u"la página perdió el elemento de audio")
        self.assertNotIn("src", m.group(0), u"apunta a una grabación que no se le dio")


if __name__ == "__main__":
    unittest.main(verbosity=2)
