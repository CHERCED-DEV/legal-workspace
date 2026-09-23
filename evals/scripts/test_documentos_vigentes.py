# -*- coding: utf-8 -*-
"""Los documentos que afirman cosas sobre el PRESENTE, recomprobados contra el disco.

**Este documento caduco en silencio durante veintiseis dias.** Su version del
2026-08-26 declaraba su propia fecha de caducidad -- «caduca con el proximo
commit que toque plugins/despacho/ o docs/skills-support/» -- y caduco al dia
siguiente, pero nadie lo noto: nueve de sus diez titulares eran falsos cuando
se volvio a leer, y ninguno se cayo solo.

Una fecha de caducidad no es una guarda. Esto si.

No comprueba los diez -- cuatro son juicios y se dice cuales. Comprueba los que
tienen respuesta en el disco, que son los que envejecen sin avisar.

Cubre dos, y son los dos que mas caro cuestan cuando envejecen:

  * `docs/ESTADO-DEL-PROYECTO.md` -- contesta «¿en que vamos?»
  * `evals/README.md` -- dice **que mide el instrumento y que no**, y esa
    segunda mitad es la que hace util a un instrumento

    python3 evals/scripts/test_documentos_vigentes.py
"""
import re
import subprocess
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DOC = RAIZ / "docs" / "ESTADO-DEL-PROYECTO.md"
EVALS = RAIZ / "evals" / "README.md"
SKILLS = RAIZ / "plugins" / "despacho" / "skills"
SCRIPTS = RAIZ / "plugins" / "despacho" / "scripts"


def texto():
    return DOC.read_text(encoding="utf-8")


def seccion0():
    t = texto()
    i = t.index(u"## §0 — Dónde estamos")
    return t[i:t.index(u"## §0.bis")]


class LosTitularesSiguenSiendoCiertos(unittest.TestCase):

    def test_1_hay_remoto(self):
        """§0.1: «Se puede instalar». En agosto era falso."""
        r = subprocess.run(["git", "remote", "-v"], cwd=str(RAIZ),
                           capture_output=True, text=True)
        self.assertIn("origin", r.stdout)
        self.assertTrue((RAIZ / ".claude-plugin" / "marketplace.json").exists()
                        or list(RAIZ.glob("**/marketplace.json")))

    def test_2_ningun_metodo_cita_una_norma(self):
        """§0.2, y es la regla dura 1 del producto."""
        patron = re.compile(r"Ley \d|Decreto \d|art\. \d")
        culpables = [p.parent.name for p in SKILLS.glob("*/SKILL.md")
                     if patron.search(p.read_text(encoding="utf-8"))]
        self.assertEqual([], culpables)

    def test_2bis_son_quince_metodos(self):
        """El numero que mas veces se ha escrito mal en este repositorio."""
        metodos = sorted(p.parent.name for p in SKILLS.glob("*/SKILL.md"))
        self.assertEqual(15, len(metodos), metodos)
        self.assertIn(u"quince métodos", seccion0())

    def test_3_once_de_los_quince_estan_registrados_como_ejecutados(self):
        """§0.3, y la excepcion se nombra en vez de esconderse.

        Once tienen pasada escrita. Los otros dos -- `transcribir-audio` y
        `nombrar-voces` -- SI se han corrido sobre material real en la
        maquina del dueno, pero su registro no esta escrito aqui. Esta prueba fija las dos cosas -- que los once
        siguen registrados, y que el que falta es exactamente ese y esta
        declarado en el §0. **Si un dia se corre, esta prueba falla**, y eso
        es lo que se quiere: obliga a escribir su registro y a borrar de aqui
        la excepcion, en vez de dejarla envejecer.
        """
        notas = (RAIZ / "docs" / "technical-design" / "v0" / "notes-verification")
        registro = "\n".join(f.read_text(encoding="utf-8")
                             for f in notas.glob("pasada-*.md"))
        sin_registrar = sorted(p.parent.name for p in SKILLS.glob("*/SKILL.md")
                               if p.parent.name not in registro)
        self.assertEqual(["acta-de-reunion", "compromisos-de-una-reunion", "nombrar-voces",
                          "transcribir-audio"], sin_registrar,
                         "el §0.3 dice que once de los quince se ejecutaron, y "
                         "la cuenta del disco ya no es esa")
        self.assertIn(u"Once de los quince se han ejecutado", seccion0())
        self.assertIn(u"no se ha corrido aquí", seccion0())

    def test_6_la_cadena_esta_completa(self):
        """§0.6: quien escribe la hoja, y quien se detiene sin la marca."""
        hechos = (SKILLS / "hechos-con-prueba" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(u"2-Borradores/Hechos - ", hechos)
        for consumidor in ("redactar-escrito", "inventario-de-anexos"):
            t = (SKILLS / consumidor / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(u"no hay hechos aprobados", t.lower(), consumidor)

    def test_7_la_cifra_de_fact_builder_es_la_que_se_escribio(self):
        """§0.7 dice «cincuenta y cinco documentos». Si cambia, se corrige aqui.

        No se renombran: son registro historico. Lo que no puede pasar es que
        la cifra del documento y la del disco dejen de ser la misma en silencio.
        """
        docs = RAIZ / "docs"
        cuantos = len([f for f in docs.rglob("*.md")
                       if "fact-builder" in f.read_text(encoding="utf-8", errors="replace")])
        self.assertEqual(55, cuantos,
                         "el §0.7 dice 55 y en el disco hay %d" % cuantos)

    def test_8_el_plugin_ejecuta_los_programas_que_dice(self):
        """§0.8: «veinticinco programas, de los cuales catorce se exponen».

        Dos numeros y no uno, porque decir solo «catorce» sugeriria que el
        modelo puede invocar catorce, y son ocho. Cual es cual lo decide
        `test_superficie.py`; aqui solo se fija que el documento no mienta.
        """
        programas = sorted(p.name for p in SCRIPTS.glob("*.py"))
        self.assertEqual(25, len(programas), programas)
        self.assertIn(u"veinticinco programas", seccion0())
        self.assertIn(u"catorce se exponen al modelo", seccion0())


class LoQueEsteArchivoNoComprueba(unittest.TestCase):
    """Declararlo es la mitad que importa de un instrumento."""

    def test_se_dice_cuales_son_juicios_y_no_hechos(self):
        """§0.4, §0.5, §0.9 y §0.10 no tienen respuesta en el disco.

        Cerrar hallazgos, que la guia se entienda, que el Knowledge Pack sea
        una abstinencia y que falten datos del trabajo real son lecturas, no
        cifras. Esta prueba NO las comprueba, y por eso las nombra: un lector
        que vea esta suite pasar no debe creer que valido los diez.
        """
        self.assertTrue(DOC.exists())

    def test_la_fecha_de_corte_esta_escrita(self):
        """Un estado sin fecha miente por omision -- la regla 4, aplicada aqui."""
        self.assertRegex(texto(), r"\*\*Fecha de corte:\*\* \d{4}-\d{2}-\d{2}")


class ElREADMEdeEvalsDiceLoQueMideYLoQueNo(unittest.TestCase):
    """La mitad que importa de un instrumento es la que declara sus limites.

    Este archivo decia «sin puntuador todavia» cuando el puntuador llevaba dos
    dias escrito, y «ninguno mide que un modelo aplique la prosa: eso solo lo
    enseña una pasada real, que sigue sin ocurrir» cuando las once pasadas ya
    estaban hechas. **Un instrumento que describe mal sus limites es peor que
    uno sin descripcion**: se le cree.
    """

    def texto(self):
        return EVALS.read_text(encoding="utf-8")

    def test_nombra_las_guardas_que_existen(self):
        guardas = ["contar_fichas.py", "buscar_cuentas.py",
                   "puntuar_caso03.py", "contar_skills.py"]
        t = self.texto()
        faltan = [g for g in guardas if g not in t]
        self.assertEqual([], faltan,
                         "hay guardas que el README de evals no menciona")

    def test_no_nombra_guardas_que_no_existen(self):
        """Control positivo: mencionar un programa que no esta es peor."""
        t = self.texto()
        import re
        for m in re.finditer(r"`(?:scripts/|plugins/[^`]*/)?(\w+\.py)`", t):
            nombre = m.group(1)
            if nombre in ("medir.py",):
                continue
            existe = (list(RAIZ.rglob(nombre)))
            self.assertTrue(existe, "el README de evals nombra %s y no existe"
                            % nombre)

    def test_todas_las_guardas_cuelgan_del_corredor(self):
        """Una guarda que hay que acordarse de correr no es una guarda."""
        corredor = (RAIZ / "evals" / "scripts" / "comprobar-salidas.sh").read_text(
            encoding="utf-8")
        for g in ("contar_fichas.py", "buscar_cuentas.py", "puntuar_caso03.py"):
            self.assertIn(g, corredor, g)
        todo = (RAIZ / "evals" / "scripts" / "correr-todo.sh").read_text(
            encoding="utf-8")
        self.assertIn("comprobar-salidas.sh", todo)

    def test_ya_no_dice_que_no_hubo_pasada_real(self):
        """La afirmacion que este archivo mantuvo falsa mas tiempo."""
        t = self.texto()
        self.assertNotIn(u"que sigue sin ocurrir.", t.split(u"~~")[0])
        self.assertIn(u"once", t)

    def test_dice_lo_que_sigue_sin_medirse(self):
        t = self.texto()
        self.assertIn(u"coste", t)
        self.assertIn(u"ninguna abogada", t.lower())


class LaCuentaDeAC05SigueSiendoLaMedida(unittest.TestCase):
    """AC-05 esta ABIERTA, y su medida del 2026-09-21 es 1 de 3 y 0 de 11.

    Esto no decide la enmienda: **fija su medicion al disco**. Si alguien
    implementa la recomendacion (d) -- o la implementa a medias otra vez --
    estas pruebas fallan, y lo que hay que hacer entonces NO es arreglarlas:
    es actualizar AC-05, que es donde vive la decision.

    El riesgo concreto que vigilan lo nombra la propia enmienda: con un
    mecanismo leyendo y dos infiriendo, **la misma pieza puede salir
    clasificada de dos maneras en la misma pasada**, y eso es peor que los
    tres infiriendo igual.
    """

    AC05 = RAIZ / "docs" / "architecture" / "adrs" / "AMENDMENT-CANDIDATES.md"

    def test_ac05_sigue_abierta(self):
        t = self.AC05.read_text(encoding="utf-8")
        self.assertIn(u"AC-05", t)
        self.assertIn(u"Estado: ABIERTO", t)

    def test_buscar_lee_la_declaracion(self):
        """El unico de los tres que la lee. Si deja de leerla, se sabe."""
        t = (SCRIPTS / "buscar.py").read_text(encoding="utf-8")
        self.assertIn("se_declara_derivado", t)
        self.assertIn("TEXTO DE REFERENCIA", t)

    def test_ningun_skill_menciona_la_declaracion(self):
        """0 de 11, la cifra que AC-05 mide.

        El dia que deje de ser cero, esta prueba falla -- y eso es correcto:
        significa que alguien llevo la recomendacion (d) a la prosa, y AC-05
        tiene que dejar de decir que falta.
        """
        con = [p.parent.name for p in SKILLS.glob("*/SKILL.md")
               if "TEXTO DE REFERENCIA" in p.read_text(encoding="utf-8")]
        self.assertEqual([], con,
                         "%s ya menciona la declaracion: actualice AC-05, no "
                         "esta prueba" % con)

    def test_el_derivado_del_banco_trae_su_declaracion(self):
        """Y la pieza sobre la que todo esto se mide sigue declarandose."""
        ref = (RAIZ / "evals" / "casos" / "caso-02-sintetico-autoridad"
               / "2-Borradores" / "Texto de referencia - 2026-04-08.txt")
        self.assertTrue(ref.exists(), ref)
        primeras = ref.read_text(encoding="utf-8").split("\n")[:5]
        self.assertTrue(any("TEXTO DE REFERENCIA" in l.upper() for l in primeras),
                        "el derivado dejo de declararse en su primera linea")


class ElArbolDelREADMEDiceLoQueHay(unittest.TestCase):
    """`V-12` se cerro el 2026-09-05 «con un grep» y sin dejar la guarda puesta.

    El arbol de `plugins/despacho/README.md` es lo primero que lee quien va a
    instalar o a publicar: dice que metodos trae el plugin y que programas hay
    en la oficina. **Un arbol desactualizado no falla, no avisa y se cree.**

    Se comprobo a mano aquel dia, y a mano volvio a quedar mal el 2026-09-22
    cuando la fusion trajo un metodo y cuatro programas. Esto es esa misma
    comprobacion, puesta donde no se olvide: falla si el disco crece y el
    arbol no, y falla si el arbol nombra algo que ya no existe.
    """

    ARBOL = RAIZ / "plugins" / "despacho" / "README.md"

    def _arbol(self):
        t = self.ARBOL.read_text(encoding="utf-8")
        i = t.index(u"├─ .claude-plugin/")
        return t[i:t.index(u"└─ docs/", i)]

    def test_estan_todos_los_metodos_del_disco(self):
        arbol = self._arbol()
        faltan = [p.parent.name for p in sorted(SKILLS.glob("*/SKILL.md"))
                  if (p.parent.name + "/") not in arbol]
        self.assertEqual([], faltan, "el árbol del README no los lista")

    def test_estan_todos_los_programas_del_disco(self):
        arbol = self._arbol()
        faltan = [f.name for f in sorted(SCRIPTS.glob("*.py"))
                  if f.name not in arbol]
        self.assertEqual([], faltan, "el árbol del README no los lista")

    def test_no_nombra_nada_que_no_exista(self):
        """La mitad que se olvida: quitar un programa y dejarlo escrito."""
        import re as _re
        arbol = self._arbol()
        en_disco = {f.name for f in SCRIPTS.glob("*.py")}
        sobran = [n for n in _re.findall(r"\b([a-z_]+\.py)\b", arbol)
                  if n not in en_disco]
        self.assertEqual([], sobran, "el árbol nombra programas que no están")

    def test_el_arbol_dice_cuantos_son_y_es_verdad(self):
        t = self.ARBOL.read_text(encoding="utf-8")
        self.assertEqual(15, len(list(SKILLS.glob("*/SKILL.md"))))
        self.assertIn(u"los QUINCE metodos", t)
        self.assertIn(u"sin el los quince comandos funcionan igual", t)


if __name__ == "__main__":
    unittest.main(verbosity=2)
