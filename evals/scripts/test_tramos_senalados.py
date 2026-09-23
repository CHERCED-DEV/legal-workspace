# -*- coding: utf-8 -*-
"""Los tramos que una entrega senala a mano (`tramos_senalados`).

El tramo repetido lo detecta el programa. Esto es lo que se descubre
despues, mirando: una palabra que ninguna otra lectura sostiene. Se senala
entre dos avisos, en el Word y en la pagina, **sin tocar una palabra del
texto transcrito**: corregirlo seria poner otra lectura en lugar de la que
hay, y nadie ha oido el tramo.

Lo que estas pruebas sujetan:
  · el texto transcrito sale identico;
  · el aviso cae en la linea que dice su hora, y no en otra;
  · si la hora no esta, o esta dos veces, se detiene: un aviso en la linea
    equivocada, o caido en silencio, es peor que ninguno;
  · el Word y la pagina dicen lo mismo.

Todo sintetico: nada de ningun caso.

    python3 evals/scripts/test_tramos_senalados.py
"""
import json
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

import construir_entrega as CE  # noqa: E402

CUERPO = u"""
**[00:00:01] · Hablante 1** buenas tardes a todos

**[00:00:04]** vamos a empezar  `[?]` *(palabra dudosa)*

**[00:00:07] · Hablante 2** esto es lo que dice la palabra rara  `[?]` *(las lecturas no coinciden)*

**[00:00:09]** y otra palabra rara

**[00:00:12] · Hablante 1** que es el tema

**[00:00:15]** el tema es otro
"""

TRAMO = {"audio": 2, "desde": "00:00:07", "hasta": "00:00:09",
         "titulo": u"Aquí la transcripción pone palabras que nadie sostiene.",
         "detalle": u"Ninguna otra lectura escribe *rara*.",
         "cierre": u"Desde aquí coinciden las lecturas."}


def solo_texto(c):
    return [m.group(2) for m in (CE.LINEA.match(l) for l in c.split("\n")) if m]


class ElWord(unittest.TestCase):

    def test_el_texto_transcrito_sale_identico(self):
        nuevo, n = CE.marcar_tramos(CUERPO, 2, [TRAMO])
        self.assertEqual(1, n)
        self.assertEqual(solo_texto(CUERPO), solo_texto(nuevo))

    def test_el_aviso_envuelve_justo_las_lineas_de_su_hora(self):
        nuevo, _ = CE.marcar_tramos(CUERPO, 2, [TRAMO])
        L = [l for l in nuevo.split("\n") if l.strip()]
        abre = next(k for k, l in enumerate(L) if TRAMO["titulo"] in l)
        cierra = next(k for k, l in enumerate(L) if u"Fin del tramo señalado" in l)
        self.assertTrue(L[abre + 1].startswith("**[00:00:07]"), L[abre + 1])
        self.assertTrue(L[cierra - 1].startswith("**[00:00:09]"), L[cierra - 1])
        self.assertTrue(L[cierra + 1].startswith("**[00:00:12]"), L[cierra + 1])
        self.assertTrue(L[abre].startswith(u"> ⚠ "))
        self.assertIn(TRAMO["cierre"], L[cierra])

    def test_el_aviso_dice_que_no_se_toco_nada(self):
        abre, _ = CE.aviso_de_tramo(TRAMO)
        self.assertIn(u"No se ha borrado ni cambiado nada del texto transcrito", abre)
        self.assertIn(u"Va de 00:00:07 a 00:00:09", abre)

    def test_una_hora_que_no_esta_detiene(self):
        with self.assertRaises(SystemExit):
            CE.marcar_tramos(CUERPO, 2, [dict(TRAMO, desde="00:00:08")])

    def test_una_hora_repetida_detiene(self):
        doble = CUERPO + u"\n**[00:00:09]** otra línea a la misma hora\n"
        with self.assertRaises(SystemExit):
            CE.marcar_tramos(doble, 2, [TRAMO])

    def test_al_reves_detiene(self):
        with self.assertRaises(SystemExit):
            CE.marcar_tramos(CUERPO, 2, [dict(TRAMO, desde="00:00:12", hasta="00:00:07")])


class LaConfiguracion(unittest.TestCase):

    def test_solo_los_de_esa_grabacion(self):
        c = {"tramos_senalados": [TRAMO, dict(TRAMO, audio=3)]}
        self.assertEqual([TRAMO], CE.tramos_de(c, 2))
        self.assertEqual([], CE.tramos_de({}, 2))

    def test_sin_texto_no_hay_aviso(self):
        for k in ("desde", "hasta", "titulo", "detalle"):
            with self.assertRaises(SystemExit, msg=k):
                CE.tramos_de({"tramos_senalados": [dict(TRAMO, **{k: "  "})]}, 2)

    def test_horas_mal_escritas_detienen(self):
        for mala in ("7:21", "00:07", "00-07-21"):
            with self.assertRaises(SystemExit, msg=mala):
                CE.tramos_de({"tramos_senalados": [dict(TRAMO, desde=mala)]}, 2)

    def test_acaba_antes_de_empezar_detiene(self):
        with self.assertRaises(SystemExit):
            CE.tramos_de({"tramos_senalados": [dict(TRAMO, desde="00:00:12", hasta="00:00:07")]}, 2)


def datos_sinteticos():
    textos = [(1.2, 3.9, 1, u"buenas tardes a todos"), (4.1, 6.8, 1, u"vamos a empezar"),
              (7.3, 8.9, 2, u"esto es lo que dice la palabra rara"), (9.0, 11.5, 2, u"y otra palabra rara"),
              (12.4, 14.8, 1, u"que es el tema"), (15.0, 17.0, 1, u"el tema es otro")]
    segs = [{"i": k, "inicio": a, "fin": b, "voz": v, "texto": t,
             "palabras": [{"p": p, "c": 0.9} for p in t.split()]}
            for k, (a, b, v, t) in enumerate(textos)]
    return {"publicada": {"etiqueta": "A/mezcla", "segmentos": segs}, "marcas": {}, "ventanas": []}


class LaPagina(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.md = self.tmp / "t.md"
        self.md.write_text(u"# Transcripción\n\n**Duración:** 00:00:17\n\n---\n" + CUERPO, encoding="utf-8")
        self.datos = self.tmp / "d.json"
        self.datos.write_text(json.dumps(datos_sinteticos(), ensure_ascii=False), encoding="utf-8")
        abre, cierra = CE.aviso_de_tramo(TRAMO)
        self.tramos = self.tmp / "tramos.json"
        self.tramos.write_text(json.dumps([{"desde": TRAMO["desde"], "hasta": TRAMO["hasta"],
                                            "abre": abre, "cierra": cierra}], ensure_ascii=False),
                               encoding="utf-8")
        self.html = self.tmp / "p.html"

    def tearDown(self):
        shutil.rmtree(str(self.tmp), ignore_errors=True)

    def generar(self, *extra):
        return subprocess.run([sys.executable, str(SCRIPTS / "md2html.py"), str(self.md), str(self.html),
                               "--datos", str(self.datos)] + list(extra),
                              capture_output=True, text=True, encoding="utf-8")

    def cuerpo(self):
        t = self.html.read_text(encoding="utf-8")
        return re.sub(r"<script\b.*?</script>", "", t, flags=re.S)

    def test_el_aviso_envuelve_las_mismas_lineas_que_en_el_word(self):
        r = self.generar("--tramos", str(self.tramos))
        self.assertEqual(0, r.returncode, r.stderr[-600:])
        t = self.cuerpo()
        abre = t.index('class="aviso-bucle tramo"')
        cierra = t.index('class="aviso-bucle tramo cierre"')
        self.assertLess(t.index('id="b1"'), abre)
        self.assertLess(abre, t.index('id="b2"'))
        self.assertLess(t.index('id="b3"'), cierra)
        self.assertLess(cierra, t.index('id="b4"'))

    def test_dice_lo_mismo_que_el_word(self):
        self.assertEqual(0, self.generar("--tramos", str(self.tramos)).returncode)
        t = self.cuerpo()
        for trozo in (TRAMO["titulo"], u"Ninguna otra lectura escribe <em>rara</em>",
                      u"No se ha borrado ni cambiado nada del texto transcrito", TRAMO["cierre"]):
            self.assertIn(trozo, t)

    def test_una_hora_que_no_esta_no_genera_la_pagina(self):
        malo = json.loads(self.tramos.read_text(encoding="utf-8"))
        malo[0]["desde"] = "00:00:08"
        self.tramos.write_text(json.dumps(malo), encoding="utf-8")
        r = self.generar("--tramos", str(self.tramos))
        self.assertNotEqual(0, r.returncode)
        self.assertFalse(self.html.exists(), u"salió una página con el aviso caído")

    def test_sin_tramos_no_aparece_ningun_aviso(self):
        """Control: el argumento es opcional, y sin el no hay aviso de tramo."""
        r = self.generar()
        self.assertEqual(0, r.returncode, r.stderr[-600:])
        self.assertNotIn("aviso-bucle tramo", self.cuerpo())


if __name__ == "__main__":
    unittest.main(verbosity=2)
