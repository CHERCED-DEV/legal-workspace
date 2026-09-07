# -*- coding: utf-8 -*-
"""Que el contador pueda fallar, y que no cuente de mas ni de menos.

El riesgo aqui es concreto y ya se materializo una vez: «Apoyado y contradicho»
empieza por «Apoyado», y un contador ingenuo lo suma a los apoyados. Esa es la
mitad de por que la cuenta a ojo salio mal.

    python3 evals/scripts/test_contar_fichas.py
"""
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]
                / "plugins" / "despacho" / "scripts"))
import contar_fichas as C

SALIDA = (Path(__file__).resolve().parents[1] / "casos"
          / "caso-03-hidraulica-desde-el-diseno" / "2-Borradores"
          / "Hechos - Hidraulica - 2026-09-05.md")


def doc(*fichas):
    return "\n".join("## %s — enunciado\n\n- **Estado:** %s\n" % f for f in fichas)


class ContarPorEstado(unittest.TestCase):

    def test_apoyado_y_contradicho_no_cuenta_como_apoyado(self):
        """El fallo concreto que este archivo existe para impedir."""
        _, por, _ = C.contar(doc(("H-01", "Apoyado."),
                                 ("H-02", "Apoyado y contradicho.")))
        self.assertEqual(1, por["Apoyado"])
        self.assertEqual(1, por["Apoyado y contradicho"])

    def test_un_estado_con_coletilla_sigue_contando(self):
        _, por, sin = C.contar(doc(("H-01", "Apoyado y contradicho (en el saldo).")))
        self.assertEqual(1, por["Apoyado y contradicho"])
        self.assertEqual([], sin)

    def test_un_sexto_estado_inventado_se_denuncia(self):
        """La Fase 5 dice que los estados son los que son: no hay un sexto."""
        _, _, sin = C.contar(doc(("H-01", "Parcialmente apoyado.")))
        self.assertEqual(1, len(sin))
        self.assertIn("H-01", sin[0])

    def test_una_ficha_sin_estado_se_denuncia(self):
        fichas, _, sin = C.contar("## H-01 — enunciado\n\nsin la linea de estado\n")
        self.assertEqual(["H-01"], fichas)
        self.assertEqual(["H-01"], sin)


class ContrastarConLoDeclarado(unittest.TestCase):

    def test_detecta_el_conteo_mal_escrito(self):
        """Reproduce el fallo real: se declararon 10 y 7 donde habia 9 y 6."""
        cuerpo = doc(*[("H-%02d" % i, "Apoyado.") for i in range(1, 10)]
                     + [("H-%02d" % i, "Sin apoyo.") for i in range(10, 16)])
        malo = cuerpo + u"\n**15 hechos propuestos** · **10 apoyados** · **7 sin apoyo**\n"
        d = C.conteo_escrito(malo)
        _, por, _ = C.contar(malo)
        self.assertEqual(10, d["Apoyado"])
        self.assertEqual(9, por["Apoyado"])

    def test_la_salida_real_del_caso_03_cuadra(self):
        """Y el control positivo: la pasada corregida coincide consigo misma."""
        self.assertTrue(SALIDA.exists(), SALIDA)
        self.assertEqual(0, C.main([str(SALIDA)]))


CRONO = (Path(__file__).resolve().parents[1] / "casos"
         / "caso-03-hidraulica-desde-el-diseno" / "2-Borradores"
         / "Cronologia - Hidraulica - 2026-09-05.md")


def crono(filas_linea, filas_sin=(), conteo=""):
    t = ["## 2. LÍNEA DE TIEMPO", "", "| Ev | Fecha | Qué | De dónde | Grado |",
         "|---|---|---|---|---|"]
    for ev, grado in filas_linea:
        t.append("| %s | 1/1/2025 | algo | pieza, p. 1 | %s |" % (ev, grado))
    t += ["", "## 3. EVENTOS SIN FECHA", "", "| Ev | Qué | Situado | De dónde |",
          "|---|---|---|---|"]
    for ev in filas_sin:
        t.append("| %s | algo | sin ancla | nada lo sitúa |" % ev)
    t += ["", "## 4. CONFLICTOS DE FECHA", "", conteo]
    return "\n".join(t)


class ContarCronologia(unittest.TestCase):

    def test_la_tabla_de_sin_fecha_no_ensucia_los_grados(self):
        """El primer fallo de esta parte: la tabla 3 tiene otra ultima columna.

        Sus filas salian como «grado no reconocido» porque se contaban con las
        de la linea de tiempo. Cada tabla se cuenta donde va.
        """
        _, _, sin_grado, sin_fecha = C.contar_cronologia(
            crono([("E-01", "documentada")], ["E-02", "E-03"]))
        self.assertEqual([], sin_grado)
        self.assertEqual(["E-02", "E-03"], sin_fecha)

    def test_en_conflicto_no_se_lee_como_otro_grado(self):
        _, por, _, _ = C.contar_cronologia(
            crono([("E-01", "en conflicto"), ("E-02", "documentada")]))
        self.assertEqual(1, por["en conflicto"])
        self.assertEqual(1, por["documentada"])

    def test_referida_con_coletilla_sigue_contando(self):
        _, por, sin, _ = C.contar_cronologia(
            crono([("E-01", "referida por la señora Quiroga")]))
        self.assertEqual(1, por["referida"])
        self.assertEqual([], sin)

    def test_un_sexto_grado_inventado_se_denuncia(self):
        """§3 dice: vocabulario fijo, cinco palabras y ninguna otra."""
        _, _, sin, _ = C.contar_cronologia(crono([("E-01", "probable")]))
        self.assertEqual(1, len(sin))
        self.assertIn("E-01", sin[0])

    def test_detecta_el_conteo_mal_escrito(self):
        """Reproduce el cuarto fallo del dia: 5 documentadas donde habia 4."""
        doc = crono([("E-0%d" % i, "documentada") for i in range(1, 5)],
                    ["E-05"],
                    u"**5 eventos** · **5 documentadas** · **1 sin fecha**")
        self.assertEqual(2, C.main_cronologia("x", doc))

    def test_la_cronologia_real_cuadra(self):
        self.assertTrue(CRONO.exists(), CRONO)
        self.assertEqual(0, C.main([str(CRONO)]))


RIGOR = (Path(__file__).resolve().parents[1] / "casos"
         / "caso-03-hidraulica-desde-el-diseno" / "2-Borradores"
         / "Revision de rigor - Hidraulica - 2026-09-05.md")


def rigor(*fichas, **kw):
    t = []
    for f, grado in fichas:
        t += ["### %s — la duda" % f, "",
              "- **Grado de soporte:** %s" % grado, ""]
    t.append(kw.get("conteo", ""))
    return "\n".join(t)


class ContarRevisionDeRigor(unittest.TestCase):

    def test_sin_soporte_no_cuenta_como_soportado(self):
        """El mismo fallo de forma que «Apoyado y contradicho», tercera vez.

        «sin soporte» contiene «soporte» y empieza distinto que «soportado»,
        pero el orden de la lista es lo que lo garantiza -- y por eso se prueba.
        """
        _, por, sin = C.contar_rigor(rigor(("F-01", "sin soporte"),
                                           ("F-02", "soportado")))
        self.assertEqual(1, por["sin soporte"])
        self.assertEqual(1, por["soportado"])
        self.assertEqual([], sin)

    def test_limitado_cuenta(self):
        _, por, _ = C.contar_rigor(rigor(("F-01", "limitado.")))
        self.assertEqual(1, por["limitado"])

    def test_un_cuarto_grado_inventado_se_denuncia(self):
        """§5 dice tres grados y ninguno mas."""
        _, _, sin = C.contar_rigor(rigor(("F-01", "parcialmente soportado")))
        self.assertEqual(1, len(sin))

    def test_detecta_el_conteo_mal_escrito(self):
        doc = rigor(("F-01", "soportado"), ("F-02", "limitado"),
                    conteo=u"**2 hallazgos** · **2 soportados** · **0 limitados**")
        self.assertEqual(2, C.main_rigor("x", doc))

    def test_la_revision_real_cuadra(self):
        self.assertTrue(RIGOR.exists(), RIGOR)
        self.assertEqual(0, C.main([str(RIGOR)]))


REF = (Path(__file__).resolve().parents[1] / "casos"
       / "caso-02-sintetico-autoridad" / "salidas-de-referencia")


class LaPlantillaDeTextoPlanoEsLaQueManda(unittest.TestCase):
    """El contador solo entendia la forma markdown de UNA pasada concreta.

    Las plantillas de los `SKILL.md` son texto plano -- «H-01 — enunciado» con
    «  Estado: APOYADO» debajo, vinetas «·» en vez de tablas, encabezados
    «2. LINEA DE TIEMPO» sin almohadilla -- y sobre las cuatro salidas de
    referencia del caso-02, escritas asi, el contador decia «0 fichas» y
    «no declara su conteo». **Una guarda ajustada a una sola muestra protege
    esa muestra y nada mas**, que es lo contrario de una guarda.
    """

    def test_ficha_en_texto_plano(self):
        fichas, por, sin = C.contar(
            u"H-01 — enunciado\n  Estado: APOYADO\n\n"
            u"H-02 — otro\n  Estado: SIN APOYO\n")
        self.assertEqual(["H-01", "H-02"], fichas)
        self.assertEqual(1, por["Apoyado"])
        self.assertEqual(1, por["Sin apoyo"])
        self.assertEqual([], sin)

    def test_grado_al_final_del_encabezado(self):
        """La plantilla de rigor lo escribe en la misma linea del hallazgo."""
        _, por, sin = C.contar_rigor(
            u"F-01 · ESTADO INFLADO — considerando 1 — Grado de soporte: sin soporte\n"
            u"  Dice: ...\n")
        self.assertEqual(1, por["sin soporte"])
        self.assertEqual([], sin)

    def test_encabezados_sin_almohadilla_separan_las_dos_tablas(self):
        texto = (u"2. LÍNEA DE TIEMPO\n"
                 u"| Ev | Fecha | Qué | De dónde | Grado |\n"
                 u"|----|----|----|----|----|\n"
                 u"| E-01 | 1/1 | algo | pieza | documentada |\n\n"
                 u"3. EVENTOS SIN FECHA\n"
                 u"| Ev | Qué | Situado | De dónde |\n"
                 u"|----|----|----|----|\n"
                 u"| E-02 | algo | sin ancla | nada |\n\n"
                 u"4. CONFLICTOS DE FECHA\n")
        eventos, por, sin, sin_fecha = C.contar_cronologia(texto)
        self.assertEqual(["E-01"], eventos)
        self.assertEqual(["E-02"], sin_fecha)
        self.assertEqual([], sin)

    def test_vinetas_en_vez_de_tabla(self):
        texto = (u"2. QUÉ AFIRMA\n   · una cosa (p. 1).\n   · otra (p. 2).\n\n"
                 u"3. QUÉ PIDE\n   · nada\n")
        self.assertEqual(2, C.contar_documento(texto)[u"afirmaciones"])

    def test_todas_las_salidas_de_referencia_cuadran(self):
        """Control positivo sobre todas, ya corregidas.

        Incluye la de `preguntas-de-derecho`, que no produce conteo y a la que
        el contador no debe pedirle ninguno.
        """
        for f in sorted(REF.glob("*.txt")):
            self.assertEqual(0, C.main([str(f)]), f.name)


CASO2 = (Path(__file__).resolve().parents[1] / "casos"
         / "caso-02-sintetico-autoridad")


class ContarEstadoDelCaso(unittest.TestCase):
    """La unica cifra que se comprueba contra el mundo, no contra el texto.

    «N archivos leidos» salio mal en la primera pasada real -- declaraba 12
    donde la carpeta tiene 13 -- y es la unica del CONTEO de ese metodo que
    tiene una respuesta comprobable fuera del propio documento.
    """

    def test_cuenta_los_archivos_de_la_carpeta(self):
        d = C.contar_estado(u"Revisión del x, hecha leyendo 13 archivos.\n"
                            u"CONTEO: 13 archivos leídos · 4 recibidos",
                            str(CASO2))
        self.assertEqual(13, d[u"declara archivos"])
        self.assertEqual(13, d[u"archivos en la carpeta"])

    def test_detecta_el_conteo_mal_escrito(self):
        """Reproduce el fallo real: declarar 12 donde hay 13."""
        self.assertEqual(2, C.main_estado(
            "x", u"1. EN QUÉ VA\nCONTEO: 12 archivos leídos", str(CASO2)))

    def test_no_cuenta_el_andamiaje_ni_las_salidas_de_referencia(self):
        """LEEME.md, NO-SON-SALIDAS.md y salidas-de-referencia/ no son del caso."""
        d = C.contar_estado(u"CONTEO: 13 archivos leídos", str(CASO2))
        reales = len([f for f in CASO2.rglob("*") if f.is_file()])
        self.assertLess(d[u"archivos en la carpeta"], reales)

    def test_sin_carpeta_no_inventa_una_cifra(self):
        d = C.contar_estado(u"CONTEO: 13 archivos leídos", None)
        self.assertNotIn(u"archivos en la carpeta", d)

    def test_la_salida_real_cuadra(self):
        f = CASO2 / "salidas-de-referencia" / "estado-del-caso-2026-09-07.txt"
        self.assertTrue(f.exists(), f)
        self.assertEqual(0, C.main([str(f), "--caso", str(CASO2)]))


class ContarInventarioDeBienes(unittest.TestCase):
    """Bienes distintos y apariciones NO son la misma cifra.

    La tabla 2 lleva una fila por cada vez que algo aparece, asi que el mismo
    B-NN sale varias veces. Y la tabla 3 los repite agrupados: contar las dos
    juntas daba 8 donde hay 5. Es el mismo fallo que ya habia salido en la
    cronologia -- **dos tablas con la misma etiqueta** -- por tercera vez.
    """

    def _doc(self, filas2, filas3=(), conteo=""):
        t = ["2. TABLA DE BIENES", "| Bien | x |", "|---|---|"]
        t += ["| %s | algo |" % b for b in filas2]
        t += ["", "3. QUÉ HAY DETRÁS DE CADA BIEN", "| Bien | x |", "|---|---|"]
        t += ["| %s | algo |" % b for b in filas3]
        t += ["", "6. CONTEO", conteo]
        return "\n".join(t)

    def test_el_mismo_bien_dos_veces_es_una_aparicion_mas(self):
        distintos, apariciones = C.contar_bienes(
            self._doc(["B-01", "B-01", "B-02"]))
        self.assertEqual(["B-01", "B-02"], distintos)
        self.assertEqual(3, apariciones)

    def test_la_tabla_3_no_se_cuenta(self):
        _, apariciones = C.contar_bienes(
            self._doc(["B-01", "B-02"], ["B-01", "B-02"]))
        self.assertEqual(2, apariciones)

    def test_detecta_el_conteo_mal_escrito(self):
        doc = self._doc(["B-01", "B-01"], (),
                        u"2 bienes distintos · 2 apariciones")
        self.assertEqual(2, C.main_bienes("x", doc))

    def test_el_inventario_real_cuadra(self):
        f = (CASO2 / "salidas-de-referencia"
             / "inventario-de-bienes-2026-09-07.txt")
        self.assertTrue(f.exists(), f)
        self.assertEqual(0, C.main([str(f)]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
