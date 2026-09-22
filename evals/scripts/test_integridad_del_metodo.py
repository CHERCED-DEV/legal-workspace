# -*- coding: utf-8 -*-
"""Lo que un metodo declara sobre si mismo, contado y ejecutado.

Dos familias, y las dos tienen al MODELO por lector -- que es lo que las hace
distintas de una comprobacion de estilo:

**1. Las cardinalidades de los vocabularios cerrados.** «Los cinco grados»,
«los tres grados de soporte», «las siete cosas», «ocho apartados». Un metodo que
dice cinco y enumera cuatro le esta dando al modelo una lista incompleta con una
promesa de completitud, y **eso no falla: produce una salida con un estado de
menos**. Es la misma operacion que en este repositorio salio mal seis veces en
dos dias, aqui dentro del producto.

**2. Las lineas de comando que los metodos llevan escritas.** Una invocacion con
los argumentos cambiados **funciona en la cabeza de quien la escribe y falla en
el escritorio de ella**, la primera vez, delante de un caso real.

Y una trampa que esta bien resuelta y conviene no «arreglar»:

    md2docx.py            <entrada.md>  <salida.docx>
    verificar_fidelidad.py <salida.docx> <entrada.md>

**Los dos programas se usan seguidos y toman los argumentos AL REVES.** Los
siete metodos que los invocan lo tienen bien. Una prueba lo fija, porque el
error natural al leerlos juntos es igualarlos.

    python3 evals/scripts/test_integridad_del_metodo.py
"""
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
S = RAIZ / "plugins" / "despacho" / "skills"
SCRIPTS = RAIZ / "plugins" / "despacho" / "scripts"


def texto(skill):
    return (S / skill / "SKILL.md").read_text(encoding="utf-8")


def filas_entre(t, desde, hasta):
    i, j = t.index(desde), None
    j = t.index(hasta, i)
    return [l for l in t[i:j].split("\n")
            if l.strip().startswith("| **")]


def numerados_entre(t, desde, hasta):
    i, j = t.index(desde), t.index(hasta, t.index(desde))
    return re.findall(r"(?m)^(\d+)\.\s+\*\*", t[i:j])


def apartados_entre(t, desde, hasta):
    i, j = t.index(desde), t.index(hasta, t.index(desde))
    return re.findall(r"(?m)^(\d)\. [A-ZÁÉÍÓÚÑ]", t[i:j])


class LosVocabulariosCerradosTienenLosQueDicen(unittest.TestCase):

    def test_cronologia_cinco_grados(self):
        t = texto("cronologia")
        self.assertIn(u"Vocabulario fijo: estas cinco palabras y ninguna otra", t)
        f = filas_entre(t, u"| Grado | Qué significa exactamente", u"### 3.1")
        self.assertEqual(5, len(f), [x[:40] for x in f])

    def test_hechos_cinco_estados(self):
        t = texto("hechos-con-prueba")
        self.assertIn(u"**Los cinco estados.**", t)
        f = filas_entre(t, u"**Los cinco estados.**", u"Dos reglas gobiernan esa lista")
        self.assertEqual(5, len(f), [x[:40] for x in f])

    def test_rigor_tres_grados_y_cinco_veredictos(self):
        t = texto("revision-de-rigor")
        self.assertEqual(3, len(filas_entre(t, u"### Grado de cada hallazgo",
                                            u"**El grado `sin soporte`")))
        self.assertEqual(5, len(filas_entre(t, u"### Veredicto global",
                                            u"**No hay sexto valor")))
        self.assertIn(u"No hay sexto valor, no se renombra ninguno", t)

    def test_rigor_las_siete_cosas(self):
        t = texto("revision-de-rigor")
        n = numerados_entre(t, u"### Fase 3 — Buscar las siete cosas", u"### Fase 4")
        self.assertEqual([str(i) for i in range(1, 8)], n)

    def test_revisar_documento_ocho_apartados(self):
        t = texto("revisar-documento")
        self.assertIn(u"Ocho apartados", t)
        self.assertEqual([str(i) for i in range(1, 9)],
                         apartados_entre(t, u"Ocho apartados", u"CONTEO:"))

    def test_estado_del_caso_seis_bloques(self):
        t = texto("estado-del-caso")
        self.assertIn(u"Seis bloques", t)
        self.assertEqual([str(i) for i in range(1, 7)],
                         apartados_entre(t, u"Seis bloques", u"CONTEO:"))

    def test_inventario_de_bienes_seis_partes(self):
        t = texto("inventario-de-bienes")
        self.assertIn(u"Seis partes", t)
        self.assertEqual([str(i) for i in range(1, 7)],
                         apartados_entre(t, u"Seis partes", u"**Ejemplo de cuatro filas**"))


class LasLineasDeComandoEscritasFuncionan(unittest.TestCase):
    """Cada invocacion documentada se PASA al programa de verdad.

    Un `usage:` con codigo 2 significa que argparse rechazo los argumentos:
    ahi la linea escrita en el metodo esta mal. Cualquier otro codigo es un
    fallo de contenido -- falta un archivo, falta una biblioteca -- y no dice
    nada sobre la forma de la llamada, que es lo que se comprueba aqui.
    """

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "caso" / "1-Documentos recibidos").mkdir(parents=True)
        (self.tmp / "caso" / "2-Borradores").mkdir(parents=True)
        (self.tmp / "a.md").write_text(u"# x\n", encoding="utf-8")

    def _acepta(self, prog, *args):
        r = subprocess.run([sys.executable, str(SCRIPTS / prog)] + list(args),
                           capture_output=True, text=True)
        rechazado = r.returncode == 2 and "usage:" in (r.stderr + r.stdout)
        self.assertFalse(rechazado, "%s rechazo los argumentos que el metodo "
                                    "escribe:\n%s" % (prog, r.stderr[:300]))

    def test_buscar(self):
        self._acepta("buscar.py", str(self.tmp / "caso"), "hola")

    def test_contar_fichas(self):
        self._acepta("contar_fichas.py", str(self.tmp / "a.md"))

    def test_estado_del_caso(self):
        self._acepta("estado_del_caso.py", str(self.tmp / "caso"), "--comprobar")

    def test_segunda_opinion(self):
        self._acepta("segunda_opinion.py", str(self.tmp / "caso"))

    def test_preparar_material(self):
        self._acepta("preparar_material.py", str(self.tmp / "a.md"),
                     "--caso", "k", "--destino", str(self.tmp / "d"))


class ElOrdenInvertidoEstaBienYNoSeIguala(unittest.TestCase):
    """Los dos programas se usan seguidos y toman los argumentos al reves.

    El error natural al leerlos juntos es igualarlos. Los siete metodos que los
    invocan lo tienen bien; esto lo fija.
    """

    def test_md2docx_recibe_el_md_primero(self):
        cod = (SCRIPTS / "md2docx.py").read_text(encoding="utf-8")
        self.assertIn("entrada, salida = Path(sys.argv[1]), Path(sys.argv[2])", cod)
        for f in sorted(S.glob("*/SKILL.md")):
            t = f.read_text(encoding="utf-8")
            if "md2docx.py" not in t:
                continue
            self.assertIn(u'md2docx.py "<el .md>" "<el .docx>"', t, f.parent.name)

    def test_verificar_fidelidad_recibe_el_docx_primero(self):
        cod = (SCRIPTS / "verificar_fidelidad.py").read_text(encoding="utf-8")
        self.assertIn("<salida.docx> <entrada.md>", cod)
        for f in sorted(S.glob("*/SKILL.md")):
            t = f.read_text(encoding="utf-8")
            if "verificar_fidelidad.py \"" not in t:
                continue
            self.assertIn(u'verificar_fidelidad.py "<el .docx>" "<el .md>"', t,
                          f.parent.name)

    def test_los_siete_lo_escriben_igual(self):
        formas = set()
        for f in sorted(S.glob("*/SKILL.md")):
            for m in re.finditer(r"md2docx\.py ([^\n`]*)",
                                 f.read_text(encoding="utf-8")):
                if "*)" not in m.group(1):          # no el allowed-tools
                    formas.add(" ".join(m.group(1).split()))
        self.assertEqual(1, len(formas), formas)


if __name__ == "__main__":
    unittest.main(verbosity=2)
