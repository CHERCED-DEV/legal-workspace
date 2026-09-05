# -*- coding: utf-8 -*-
"""El canario de `ADMIN`, traducido al producto que sí existe.

`architecture-post-v0.md` §iv, Principio 1: las operaciones administrativas
—migraciones, instalación de packs, reparación— **nunca se exponen al modelo**,
y eso *«se comprueba con una prueba, no con una revisión de código que alguien
recuerde hacer»*. La forma que le da es una cuenta: **si `ADMIN` cuenta más de
cero, la frontera se movió**.

Ese documento escribe para un Core que no existe (§7 del backlog, ADR-018), y
la tentación es archivar el principio como «no aplica». **Sí aplica.** La
superficie por la que este producto ejecuta código no es un manifiesto MCP: es
el `allowed-tools` de cada `SKILL.md`. Así que la cuenta se hace sobre eso.

El riesgo que vigila lo nombra el propio documento y no es una propuesta de
romper la frontera: *«la presión llega como una tool pequeña y razonable»*.

    python3 evals/scripts/test_superficie.py
"""
import re
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
SKILLS = RAIZ / "plugins" / "despacho" / "skills"
SCRIPTS = RAIZ / "plugins" / "despacho" / "scripts"

# Los seis que el modelo puede invocar, y por qué cada uno.
EXPUESTOS = {
    "buscar.py":              "buscar sin leerlo todo",
    # Septimo, anadido el 2026-09-05 con la medicion delante: la Fase 6 pide un
    # conteo que llama «instrumento de honestidad», y la primera pasada real lo
    # dio mal. Contar es trabajo mecanico con respuesta correcta comprobable.
    "contar_fichas.py":       "contar las fichas por estado y contrastar",
    "estado_del_caso.py":     "sustituir la cabecera conservando sus notas",
    "md2docx.py":             "entregar en el formato que ella abre",
    "preparar_material.py":   "el trabajo mecánico de la ingesta",
    "segunda_opinion.py":     "segunda pasada de OCR sobre lo dudoso",
    "verificar_fidelidad.py": "comprobar que el .docx dice lo que el .md",
}

# Los dos de clase ADMIN: existen en el disco y NO se exponen.
RESERVADOS = {
    "traer_modelos.py": "instala modelos de terceros = instalar un pack",
    "medir_realce.py":  "instrumentación de desarrollo sobre material real",
}


def declarados():
    """{nombre de programa: [skills que lo declaran]}, leyendo el frontmatter."""
    fuera = {}
    for p in sorted(SKILLS.glob("*/SKILL.md")):
        cabecera = p.read_text(encoding="utf-8").split("---", 2)[1]
        for m in re.finditer(r"scripts/([A-Za-z0-9_]+\.py)", cabecera):
            fuera.setdefault(m.group(1), []).append(p.parent.name)
    return fuera


class LaSuperficieSeCuenta(unittest.TestCase):

    def test_la_superficie_es_exactamente_la_declarada(self):
        """Si aparece un octavo programa expuesto, esta prueba falla.

        Fueron seis hasta el 2026-09-05, y el septimo entro con su medicion
        delante y esta linea escrita. Que crezca no esta prohibido; que crezca
        sin que nadie lo decida, si.
        """
        self.assertEqual(sorted(EXPUESTOS), sorted(declarados()))

    def test_admin_cuenta_cero(self):
        """Los dos administrativos no son invocables por el modelo.

        Es la cuenta literal del Principio 1. Cero, no «pocos».
        """
        expuestos_admin = [n for n in RESERVADOS if n in declarados()]
        self.assertEqual([], expuestos_admin,
                         "un programa administrativo quedó expuesto al modelo")

    def test_todo_lo_declarado_existe_en_el_disco(self):
        """Una skill que declara un programa que no está no falla al instalar:

        falla el día del caso, delante de ella, cuando lo invoque.
        """
        for nombre, quienes in sorted(declarados().items()):
            self.assertTrue((SCRIPTS / nombre).exists(),
                            "%s declaran %s y no está" % (quienes, nombre))

    def test_todo_programa_del_disco_esta_clasificado(self):
        """Control positivo: un programa nuevo obliga a decidir de qué lado va.

        Sin esto, añadir un script y no exponerlo pasaría inadvertido -- y
        exponerlo después también.
        """
        en_disco = sorted(p.name for p in SCRIPTS.glob("*.py"))
        clasificados = sorted(list(EXPUESTOS) + list(RESERVADOS))
        self.assertEqual(clasificados, en_disco,
                         "hay un programa sin clasificar: decide si se expone")

    def test_solo_preguntas_de_derecho_no_declara_nada(self):
        """Y es correcto: es el único método que no toca material."""
        sin = [p.parent.name for p in sorted(SKILLS.glob("*/SKILL.md"))
               if "allowed-tools" not in p.read_text(encoding="utf-8")]
        self.assertEqual(["preguntas-de-derecho"], sin)


class LaCarpetaDeLoRecibidoNoSeToca(unittest.TestCase):
    """La protección de escritura más fuerte del producto, contada.

    `technical-design/v0/ESTADO-Y-HALLAZGOS-CRITICOS.md` §1.1.2 verificó contra
    documentación oficial que **en Cowork no existe deny por ruta**: adjuntar una
    carpeta concede su árbol entero, y *«el único remedio documentado es
    posicional: dejar los datos fuera de las carpetas permitidas»*. De ahí §1.3:
    **la protección no puede ser una regla; tiene que ser una posición.**

    Para `1-Documentos recibidos/` **el remedio posicional no está disponible**:
    los métodos tienen que leer esa carpeta, así que no puede estar fuera. Hoy
    la protección es prosa, y descansa en que el modelo obedezca -- nueve veces.

    Esta prueba no la convierte en perímetro. Hace lo único que se puede hacer
    desde aquí: **fijar la cuenta**. Si un método nuevo nombra la carpeta y no
    trae prohibición, falla; si un método deja de traerla, falla.
    """

    # Los nueve que nombran la carpeta, y qué prohibición trae cada uno.
    CON_REGLA = {
        "cronologia":           "Nunca escribes en `1-Documentos recibidos/`",
        "estado-del-caso":      "Nunca escribe dentro de `1-Documentos recibidos/`",
        "hechos-con-prueba":    "**Nunca en `1-Documentos recibidos/`.**",
        "inventario-de-anexos": "Nunca escribas, renombres, muevas ni corrijas nada dentro de `1-Documentos recibidos/`",
        "inventario-de-bienes": "Nunca escribas, renombres, muevas ni corrijas nada dentro de `1-Documentos recibidos/`",
        "redactar-escrito":     "En `1-Documentos recibidos/` **no se escribe nunca**",
        "revisar-documento":    "Nunca se escribe en `1-Documentos recibidos/`",
        "revision-de-rigor":    "**Nunca en `1-Documentos recibidos/`**",
        # El único que escribe ahí, y una sola vez: copia los originales.
        "preparar-material":    "**No escribe en `1-Documentos recibidos/`** después de copiar los originales",
    }

    def _nombran(self):
        return {p.parent.name for p in sorted(SKILLS.glob("*/SKILL.md"))
                if "1-Documentos recibidos" in p.read_text(encoding="utf-8")}

    def test_quien_nombra_la_carpeta_trae_su_prohibicion(self):
        for skill, regla in sorted(self.CON_REGLA.items()):
            t = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(regla, t,
                          "%s perdió su prohibición de escritura" % skill)

    def test_no_hay_un_decimo_que_la_nombre_sin_regla(self):
        """El modo de fallo real: un método nuevo que lee ahí y no lo dice."""
        self.assertEqual(sorted(self.CON_REGLA), sorted(self._nombran()))

    def test_la_razon_sigue_siendo_la_misma_en_los_siete(self):
        """Y la razón está EN REVISIÓN, no fija: ver A-4/A-5 del backlog.

        Siete la dan; si en contexto autoridad existe un expediente digital
        oficial, «lo único que no se puede reconstruir» sería falso ahí. La
        prohibición no cambiaría -- su razón declarada sí. Esta prueba fija la
        cuenta para que el día que se decida se toquen los siete, no tres.
        """
        con_razon = sorted(p.parent.name for p in sorted(SKILLS.glob("*/SKILL.md"))
                           if "no se puede reconstruir" in p.read_text(encoding="utf-8"))
        self.assertEqual(
            ["cronologia", "estado-del-caso", "hechos-con-prueba",
             "inventario-de-anexos", "inventario-de-bienes",
             "redactar-escrito", "revisar-documento"], con_razon)


if __name__ == "__main__":
    unittest.main(verbosity=2)
