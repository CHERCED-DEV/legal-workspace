# -*- coding: utf-8 -*-
"""La plantilla que viaja al plugin es un ARTEFACTO COMPILADO, y nada lo vigilaba.

`plugins/despacho/scripts/plantilla/pagina.html` no se escribe: **se compila**
desde `tools/pagina-despacho/src/` y se copia. Eso crea dos averias silenciosas,
y las dos se ven igual de bien en el editor:

  1. **La plantilla envejece.** Alguien toca `src/estado.js`, no vuelve a
     publicar, y el plugin sigue entregando la pagina vieja. No hay error, no
     hay aviso, y lo que ella abre no es lo que dice el codigo.
  2. **Alguien edita el `.html` compilado a mano.** `ADR-020` §2 lo prohibe con
     todas las letras --*«Prohibido editar un `.html` de salida a mano. Si algo
     esta mal en la pagina, esta mal en el Markdown»*-- y **esa prohibicion no
     tenia nada que la hiciera cumplir.** Una correccion a mano se pierde en la
     siguiente compilacion, sin dejar rastro de que existio.

La comprobacion fuerte --compilar y comparar byte a byte-- necesita Node y
`node_modules`, y **este corredor tiene que correr sin red**. Asi que hay dos:

  · La que corre SIEMPRE: `HUELLAS.json`, escrito por `publicar.mjs`, contra
    lo que hay en el disco. Es exacta y no necesita nada.
  · La que corre SI SE PUEDE: la compilacion de verdad. Si falta Node o
    `node_modules`, **se salta diciendolo** -- no se finge que paso.

    python3 evals/scripts/test_pagina_publicada.py
"""
import hashlib
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
TOOLS = RAIZ / "tools" / "pagina-despacho"
HUELLAS = TOOLS / "HUELLAS.json"
ARTEFACTO = RAIZ / "plugins" / "despacho" / "scripts" / "plantilla" / "pagina.html"


def huella(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def registro():
    return json.loads(HUELLAS.read_text(encoding="utf-8"))


class LaPlantillaCorrespondeASusFuentes(unittest.TestCase):

    def test_existe_el_registro_de_huellas(self):
        """Sin el, todo lo demas de este archivo pasaria sin comprobar nada."""
        self.assertTrue(HUELLAS.exists(),
                        u"falta HUELLAS.json: corra `npm run publicar`")
        self.assertTrue(ARTEFACTO.exists(), u"falta la plantilla publicada")

    def test_ninguna_fuente_cambio_desde_la_ultima_publicacion(self):
        """La averia nº 1: se toca `src/` y se olvida publicar.

        El mensaje dice QUE hacer, porque el que se encuentre esta prueba roja
        puede no saber que aqui hay un paso de compilacion.
        """
        movidas = []
        for rel, h in sorted(registro()["fuentes"].items()):
            f = TOOLS / rel
            if not f.exists():
                movidas.append(u"%s ya no está" % rel)
            elif huella(f) != h:
                movidas.append(u"%s cambió" % rel)
        self.assertEqual([], movidas,
                         u"la plantilla del plugin NO corresponde a estas "
                         u"fuentes. Corra: cd tools/pagina-despacho && "
                         u"npm ci && npm run publicar")

    def test_la_plantilla_no_se_edito_a_mano(self):
        """La averia nº 2, que es la que `ADR-020` §2 prohibe y nadie vigilaba.

        Una correccion escrita a mano sobre el `.html` compilado se pierde en
        la siguiente compilacion **sin dejar rastro de que existio**. Es peor
        que no haberla hecho: alguien la dio por hecha.
        """
        self.assertEqual(registro()["huella_del_artefacto"], huella(ARTEFACTO),
                         u"la plantilla publicada no es la que se compiló: o "
                         u"se editó a mano (ADR-020 §2 lo prohíbe), o se copió "
                         u"otra cosa encima")

    def test_el_registro_cubre_TODO_lo_que_entra_en_la_compilacion(self):
        """La mitad que se olvida, y la que hace de esto una guarda y no un gesto.

        Un registro que solo cubra la mitad de las fuentes protege esa mitad y
        nada mas. Si manana aparece `src/nuevo.js`, esta prueba falla hasta que
        `publicar.mjs` lo incluya -- y no cuando ya haya derivado.
        """
        en_disco = {"src/" + f.name for f in (TOOLS / "src").iterdir() if f.is_file()}
        en_disco |= {"index.html", "vite.config.js", "package.json", "package-lock.json"}
        self.assertEqual(sorted(en_disco), sorted(registro()["fuentes"]),
                         u"hay fuentes que HUELLAS.json no cubre: actualice "
                         u"publicar.mjs y vuelva a publicar")

    def test_el_registro_apunta_al_artefacto_que_usa_el_plugin(self):
        """Que no apunte a `dist/`, que no viaja."""
        self.assertEqual("plugins/despacho/scripts/plantilla/pagina.html",
                         registro()["artefacto"])
        self.assertTrue((RAIZ / registro()["artefacto"]).exists())


class LaPlantillaEsDeVerasUnaCompilacionDeEstasFuentes(unittest.TestCase):
    """Control positivo de lo anterior, y no es redundante.

    Las huellas comprueban que **nada cambio desde la ultima publicacion**.
    No comprueban que la publicacion de entonces saliera de estas fuentes: un
    `HUELLAS.json` escrito sobre un artefacto equivocado cuadraria igual de
    bien. Esto lo ata por el otro lado, con frases que la compilacion conserva
    literales.
    """

    @classmethod
    def setUpClass(cls):
        cls.pagina = ARTEFACTO.read_text(encoding="utf-8")

    def _frases(self, ruta):
        """Frases en castellano de un fuente. La minificacion NO toca literales."""
        t = (TOOLS / ruta).read_text(encoding="utf-8")
        fuera = set()
        for l in re.findall(r"""["'`]([^"'`\n]{15,160})["'`]""", t):
            if any(c in l for c in "${}<>\\") or l.startswith("."):
                continue
            if " " in l and re.search(u"[áéíóúñ¿¡]| (que|de|la|el|no|se|su|por) ", l):
                fuera.add(l)
        return fuera

    def test_las_frases_de_los_fuentes_estan_en_la_pagina(self):
        anclas = set()
        for rel in ("src/estado.js", "src/pagina.js", "src/teclado.js", "index.html"):
            anclas |= self._frases(rel)
        self.assertGreater(len(anclas), 10, u"el extractor de frases se rompió")
        faltan = sorted(a for a in anclas if a not in self.pagina)
        self.assertEqual([], faltan,
                         u"la página no contiene texto que sus fuentes escriben")

    def test_la_pagina_declara_que_es_material_derivado(self):
        """`ADR-020` §6: la incertidumbre es estructural y va lo primero."""
        self.assertIn(u"Esto es material derivado, no es el original", self.pagina)


class LaCompilacionDeVerdad(unittest.TestCase):
    """Y la comprobacion fuerte, cuando la maquina la permite.

    Se salta diciendolo. **Una prueba que se salta en silencio es una prueba
    que no existe**, y en un corredor sin red esto se salta casi siempre.
    """

    def test_compilar_otra_vez_da_el_mismo_archivo(self):
        if not shutil.which("npm"):
            self.skipTest("sin npm: la comprobacion fuerte no se hizo")
        if not (TOOLS / "node_modules").is_dir():
            self.skipTest("sin node_modules (hace falta red): "
                          "corra `cd tools/pagina-despacho && npm ci`")
        r = subprocess.run(["npm", "run", "build"], cwd=str(TOOLS),
                           capture_output=True, text=True)
        self.assertEqual(0, r.returncode, r.stderr[-600:])
        salida = TOOLS / "dist" / "index.html"
        self.assertEqual(huella(salida), huella(ARTEFACTO),
                         u"compilar de nuevo NO da la plantilla que viaja")


if __name__ == "__main__":
    unittest.main(verbosity=2)
