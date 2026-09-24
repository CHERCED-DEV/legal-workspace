# -*- coding: utf-8 -*-
"""ordenar_proyecto: llevar un proyecto a la forma de ADR-023 sin perder nada.

Con un proyecto sintético que tiene los mismos desórdenes que se encontraron
el 2026-09-23 (entregas en «3-Para presentar», «_fuentes» en la raíz,
versiones «previa/vigente», WAV de trabajo, copias idénticas sueltas, páginas
con rutas relativas a los audios): el plan no toca nada, aplicar deja la
forma, ajusta entrega.json y las rutas de las páginas, y deshacer devuelve el
proyecto byte a byte.

    python3 evals/scripts/test_ordenar_proyecto.py
"""
import hashlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "plugins" / "despacho" / "scripts"))

import estructura as E  # noqa: E402
import ordenar_proyecto as O  # noqa: E402


def escribir(p, texto="x"):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto, encoding="utf-8")


def foto(raiz):
    """{ruta relativa: md5} de todo lo que hay, carpetas vacías incluidas."""
    out = {}
    for r, ds, fs in os.walk(raiz):
        for d in ds:
            q = os.path.join(r, d)
            if not os.listdir(q):
                out[os.path.relpath(q, raiz) + "/"] = "vacía"
        for f in fs:
            q = os.path.join(r, f)
            out[os.path.relpath(q, raiz)] = hashlib.md5(open(q, "rb").read()).hexdigest()
    return out


def proyecto(base):
    P = base / "Cliente" / "Asunto de prueba"
    escribir(P / "1-Documentos recibidos" / "grabacion.mp4", "AUDIO")
    B = P / "2-Borradores"
    escribir(B / "Transcripciones" / "previa 1 - 2026-01-10" / "Transcripcion - Audio 1 - 2026-01-10.md", "uno")
    escribir(B / "Transcripciones" / "vigente - 2026-01-12 (otra lectura)" / "Transcripcion - Audio 1 - 2026-01-10.md", "dos")
    escribir(B / "Transcripciones" / "vigente - 2026-01-12 (otra lectura)" / "datos" / "A1 - datos completos.json", "{}")
    escribir(B / "Transcripciones" / "vigente - 2026-01-12 (otra lectura)" / ".trabajo" / "A1.wav", "WAV")
    escribir(B / "Transcripcion - Audio 1 - copia.md", "dos")                    # copia idéntica suelta
    escribir(B / "Compromisos senalados" / "A1 - compromisos.json", "[]")
    escribir(B / "Compromisos senalados - 2026-01-13 (con detalle)" / "A1 - compromisos.json", "[1]")
    escribir(B / "Acta - Reunion de prueba - 2026-01-09.md", "acta")
    escribir(B / "Glosario del caso - sugerencias - 2026-01-13.json", "[]")
    escribir(B / "Audio 1 - oir y nombrar voces.html",
             '<audio src="../1-Documentos recibidos/grabacion.mp4"></audio>')
    escribir(B / "Voces" / "Voces - prueba.html", '{"ruta":"../../1-Documentos recibidos/grabacion.mp4"}')
    escribir(B / "Verdad de referencia" / "Marcar - Audio 1.html",
             '<audio src="../../1-Documentos recibidos/grabacion.mp4"></audio> <a href="../ENTREGA - vieja/audio/x.mp4">rota</a>')
    for n in ("ENTREGA - Asunto - 2026-01-12", "ENTREGA - Asunto - 2026-01-13 (arreglada)"):
        escribir(P / "3-Para presentar" / n / "00 - EMPIECE AQUI.html", n)
        escribir(P / "3-Para presentar" / (n + ".zip"), "ZIP " + n)
    escribir(P / "3-Para presentar" / "Memorial que ella firmó.docx", "suyo")
    F = P / "_fuentes (no enviar)"
    escribir(F / "entrega.json", json.dumps({
        "raiz": str(P).replace("\\", "/"), "nombre": "ENTREGA - Asunto - 2026-01-13 (arreglada)",
        "origen": "2-Borradores/Transcripciones/vigente - 2026-01-12 (otra lectura)",
        "otras": ["2-Borradores/Transcripciones/previa 1 - 2026-01-10"],
        "compromisos": "2-Borradores/Compromisos senalados - 2026-01-13 (con detalle)",
        "glosario": "2-Borradores/Glosario del caso - sugerencias - 2026-01-13.json",
        "salida": "3-Para presentar",
        "nota": {"_de_donde": "_fuentes (no enviar)/lecturas.json y datos/A1"}}, ensure_ascii=False, indent=1))
    return P


class Ordenar(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.P = proyecto(Path(self.tmp.name))
        self.antes = foto(self.P)
        self.plan = Path(self.tmp.name) / "plan.json"
        O.main([str(self.P), "--plan", str(self.plan)])

    def tearDown(self):
        self.tmp.cleanup()

    def test_el_plan_no_toca_nada(self):
        self.assertEqual(self.antes, foto(self.P))
        self.assertTrue(self.plan.with_suffix(".md").is_file())

    def test_aplicar_deja_la_forma_y_ajusta_las_rutas(self):
        O.aplicar(str(self.plan))
        P = self.P
        raiz = sorted(os.listdir(P))
        self.assertEqual(["1-Documentos recibidos", "2-Borradores", "3-Para presentar"], raiz)
        self.assertEqual(["Memorial que ella firmó.docx"], os.listdir(P / "3-Para presentar"), "lo de ella se queda")
        self.assertTrue((P / E.ENTREGAS / "ENTREGA - Asunto - 2026-01-13 (arreglada)").is_dir())
        self.assertTrue((P / E.ENTREGAS_ANTERIORES / "ENTREGA - Asunto - 2026-01-12.zip").is_file())
        T = P / E.TRANSCRIPCIONES
        self.assertEqual(["2026-01-10 - lectura 1", "2026-01-12 - otra lectura"], sorted(os.listdir(T)))
        self.assertTrue((P / E.INTERMEDIOS).is_dir() and any((P / E.INTERMEDIOS).rglob("A1.wav")))
        self.assertEqual(["2026-01-13 - con detalle"] + [x for x in sorted(os.listdir(P / E.COMPROMISOS)) if x != "2026-01-13 - con detalle"],
                         sorted(os.listdir(P / E.COMPROMISOS), key=lambda x: x != "2026-01-13 - con detalle"))
        self.assertTrue((P / E.ACTAS / "Acta - Reunion de prueba - 2026-01-09.md").is_file())
        self.assertTrue((P / E.ANTERIORES / "copias identicas" / "Transcripcion - Audio 1 - copia.md").is_file())
        cfg = json.loads((P / E.FUENTES_DE_LA_ENTREGA / "entrega.json").read_text(encoding="utf-8"))
        self.assertEqual("2-Borradores/Transcripciones/2026-01-12 - otra lectura", cfg["origen"])
        self.assertEqual(["2-Borradores/Transcripciones/2026-01-10 - lectura 1"], cfg["otras"])
        self.assertEqual("2-Borradores/Compromisos/2026-01-13 - con detalle", cfg["compromisos"])
        self.assertEqual(E.ENTREGAS, cfg["salida"])
        self.assertIn("2-Borradores/Entregas/_fuentes (no enviar)/lecturas.json", cfg["nota"]["_de_donde"])
        # Las páginas que cambiaron de profundidad apuntan otra vez al audio.
        voces = (P / E.VOCES / "Audio 1 - oir y nombrar voces.html").read_text(encoding="utf-8")
        self.assertIn('"../../1-Documentos recibidos/grabacion.mp4"', voces)
        verdad = (P / E.VOCES / "Verdad de referencia" / "Marcar - Audio 1.html").read_text(encoding="utf-8")
        self.assertIn('"../../../1-Documentos recibidos/grabacion.mp4"', verdad)
        self.assertIn('"../ENTREGA - vieja/audio/x.mp4"', verdad, "la ruta que ya estaba rota no se toca")
        # Lo recibido, intacto.
        self.assertEqual(self.antes["1-Documentos recibidos" + os.sep + "grabacion.mp4"],
                         foto(P)["1-Documentos recibidos" + os.sep + "grabacion.mp4"])

    def test_3_para_presentar_no_desaparece_aunque_quede_vacia(self):
        (self.P / "3-Para presentar" / "Memorial que ella firmó.docx").unlink()
        self.antes = foto(self.P)
        plan = Path(self.tmp.name) / "plan2.json"
        O.main([str(self.P), "--plan", str(plan)])
        O.aplicar(str(plan))
        self.assertTrue((self.P / "3-Para presentar").is_dir())
        self.assertEqual([], os.listdir(self.P / "3-Para presentar"))

    def test_la_ruta_rota_se_senala(self):
        plan = json.loads(self.plan.read_text(encoding="utf-8"))
        self.assertTrue(any("rutas rotas" in s and "Marcar - Audio 1.html" in s for s in plan["senalados"]))
        self.assertTrue(any("0-Estado" in s for s in plan["senalados"]))

    def test_deshacer_devuelve_el_proyecto_byte_a_byte(self):
        man = O.aplicar(str(self.plan))
        self.assertNotEqual(self.antes, foto(self.P))
        O.deshacer(man)
        despues = {k: v for k, v in foto(self.P).items() if "ordenado - " not in k and not k.startswith(os.path.join("2-Borradores", "_anteriores"))}
        self.assertEqual(self.antes, despues)

    def test_un_destino_que_ya_existe_detiene_el_plan(self):
        escribir(self.P / E.ACTAS / "Acta - Reunion de prueba - 2026-01-09.md", "otra")
        with self.assertRaises(SystemExit):
            O.planear(str(self.P))

    def test_no_se_sobrescribe_el_plan(self):
        with self.assertRaises(SystemExit):
            O.main([str(self.P), "--plan", str(self.plan)])


if __name__ == "__main__":
    unittest.main(verbosity=2)
