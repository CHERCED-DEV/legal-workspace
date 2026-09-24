# -*- coding: utf-8 -*-
"""Lo que ella declara en las páginas, y lo que la página le pregunta.

Pruebas de lo añadido el 2026-09-23 a la superficie de trabajo, todo con
datos sintéticos (nada de ningún caso):

  · «Lo que no se entiende»: qué tramos se le preguntan (huecos, discordia,
    tramos señalados), juntos si se tocan, con las pistas de la máquina como
    pistas; y el hueco ya no dice «sin habla detectada», que no se sabía.
  · Los compromisos: su ficha no inventa campos, y si la lectura cree que no
    es un compromiso, la etiqueta lo pregunta en vez de afirmarlo.
  · El glosario sugerido llega a la página como sugerencia.
  · `recoger_lo_declarado`: casa cada declaración con su página por la clave,
    descarta la de otra versión, no sobrescribe, y el informe dice lo que ella
    declaró y nada que la máquina propusiera.
  · `releer_tramo`: sus recortes y su cuenta de «en cuántas lecturas sale».

    python3 evals/scripts/test_lo_declarado.py
"""
import contextlib
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

import md2html as M  # noqa: E402
import recoger_lo_declarado as R  # noqa: E402
import releer_tramo as RT  # noqa: E402

# El hijo escribe en UTF-8 aunque la consola no lo sea (en Windows, cp1252).
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def seg(i, a, b, texto, voz=1):
    return {"i": i, "inicio": a, "fin": b, "texto": texto, "voz": voz,
            "palabras": [{"p": p, "c": 0.9} for p in texto.split()]}


SEGS = [seg(0, 0, 4, "buenas tardes"), seg(1, 4, 8, "vamos con el tema"),
        seg(2, 20, 24, "aquí se oye lejos"), seg(3, 24, 30, "y esto es otra cosa", 2),
        seg(4, 30, 34, "la cuenta del municipio"), seg(5, 34, 38, "gracias")]
DOC = {"etiqueta": "A/x", "segmentos": SEGS}
VENTANAS = [{"t": 20.0, "medio": 0.3, "textos": {"A/x": "aquí se oye lejos", "otra": "aquí se oye el ejido"}},
            {"t": 0.0, "medio": 0.95, "textos": {}}]


class LoQueNoSeEntiende(unittest.TestCase):

    def test_hueco_discordia_y_senalado_se_juntan_si_se_tocan(self):
        il = M.ilegibles_de(DOC, VENTANAS, "A/x",
                            tramos=[{"desde": "00:00:30", "hasta": "00:00:34"}],
                            rescates=[{"ini": 9, "fin": 19, "texto": "se oye algo lejos", "invencion": False}])
        self.assertEqual(1, len(il), il)          # hueco 8-20, discordia 20-40 y señalado 30-34: todo junto
        x = il[0]
        self.assertEqual(["discordia", "hueco", "senalado"], x["motivos"])
        self.assertEqual(8, x["desde"])
        self.assertAlmostEqual(0.3, x["acuerdo"])
        fuentes = [l["fuente"] for l in x["lecturas"]]
        self.assertTrue(any("aislada" in f for f in fuentes), "la lectura del rescate va como pista")

    def test_un_hueco_corto_no_se_pregunta(self):
        doc = {"segmentos": [seg(0, 0, 4, "uno"), seg(1, 9, 12, "dos")]}   # 5 s: no llega a 8
        self.assertEqual([], M.ilegibles_de(doc, [], "A/x"))

    def test_la_pagina_no_dice_sin_habla_detectada(self):
        """Lo único que se sabe de un hueco es que no hay transcripción."""
        html, _ = M.construir_bloques(DOC, {}, [], "A/x")
        self.assertNotIn("sin habla detectada", html)
        self.assertIn("sin transcribir", html)
        self.assertIn('class="pausa hueco"', html)

    def test_el_principio_y_el_final_sin_transcribir_se_preguntan(self):
        """Antes de la primera línea y, si se sabe cuánto dura, después de la última."""
        doc = {"duracion_s": 90.0, "segmentos": [seg(0, 30, 34, "uno"), seg(1, 34, 60, "dos")]}
        self.assertEqual([(0.0, 30), (60, 90.0)], [(x["desde"], x["hasta"]) for x in M.ilegibles_de(doc, [], "A/x")])
        html, _ = M.construir_bloques(doc, {}, [], "A/x")
        self.assertIn('data-desde="0.00" data-hasta="30.00"', html)
        self.assertIn('data-desde="60.00" data-hasta="90.00"', html)

    def test_sin_la_duracion_no_se_inventa_el_final(self):
        doc = {"segmentos": [seg(0, 0, 4, "uno"), seg(1, 4, 60, "dos")]}
        self.assertEqual([], M.ilegibles_de(doc, [], "A/x"))
        html, _ = M.construir_bloques(doc, {}, [], "A/x")
        self.assertNotIn("pausa hueco", html)

    def test_ninguna_ventana_acaba_antes_de_empezar(self):
        """Una ventana en discordia tras la última línea daba hasta < desde:
        un tramo que no se puede oír ni contar."""
        doc = {"segmentos": [seg(0, 0, 4, "uno"), seg(1, 4, 60, "dos")]}
        v = [{"t": 70.0, "medio": 0.2, "textos": {}}]
        self.assertEqual([], M.ilegibles_de(doc, v, "A/x"))
        con = M.ilegibles_de(dict(doc, duracion_s=80.0), v, "A/x")
        self.assertTrue(con and all(x["hasta"] - x["desde"] >= 1 for x in con), con)
        self.assertTrue(all(x["hasta"] <= 80.0 for x in con), con)
        self.assertEqual([], M.ilegibles_de({"segmentos": []}, [{"t": 5.0, "medio": 0.1, "textos": {}}], "A/x"))

    def test_el_id_de_un_tramo_sale_del_tramo_y_no_de_su_orden(self):
        """Lo que ella cuenta se guarda por id: un tramo nuevo delante no puede
        dejar su declaración pegada a otro tramo."""
        doc = {"segmentos": [seg(0, 0, 4, "uno"), seg(1, 20, 24, "dos"), seg(2, 40, 44, "tres")]}
        antes = {x["id"]: (x["desde"], x["hasta"]) for x in M.ilegibles_de(doc, [], "A/x")}
        doc["segmentos"][1] = seg(1, 10, 24, "dos")
        despues = {x["id"]: (x["desde"], x["hasta"]) for x in M.ilegibles_de(doc, [], "A/x")}
        self.assertEqual(["i-24-40"], [k for k in antes if k in despues])
        self.assertTrue(all(antes[k] == despues[k] for k in antes if k in despues))


class LosCompromisos(unittest.TestCase):

    def test_sin_detalle_no_se_inventan_campos(self):
        h = M.etiqueta_compromiso({"minuto": "00:00:04", "cita": "vamos con el tema", "cerrado": False,
                                   "de_que_se_trata": "algo", "plazo": "no consta"})
        self.assertNotIn("Quién lo asume", h)
        self.assertIn("COMPROMISO", h)

    def test_con_detalle_sale_quien_plazo_y_lo_que_falta(self):
        h = M.etiqueta_compromiso({"minuto": "00:00:04", "cita": "vamos con el tema", "cerrado": False,
                                   "de_que_se_trata": "algo", "plazo": "no consta", "quien": "no se dice",
                                   "quien_cita": "", "plazo_cita": "", "falta": ["que alguien lo asuma"],
                                   "tipo": "tarea", "por_que_estado": "nadie lo asume"})
        self.assertIn("Quién lo asume:</b> <strong>no se dice</strong>", h)
        self.assertIn("que alguien lo asuma", h)
        self.assertIn("nadie lo ha oído", h)

    def test_si_la_lectura_cree_que_no_lo_es_la_etiqueta_pregunta(self):
        h = M.etiqueta_compromiso({"minuto": "00:00:04", "cita": "x", "cerrado": False,
                                   "de_que_se_trata": "algo", "tipo": "no_es_compromiso"})
        self.assertIn("¿COMPROMISO?", h)
        self.assertIn("según la lectura, no lo es", h)

    def test_lo_critico_va_en_negrita_y_la_cita_queda_literal(self):
        h = M.etiqueta_compromiso({"minuto": "00:00:04", "cita": "nadie lo sabe todavía", "cerrado": False,
                                   "de_que_se_trata": "algo", "plazo": "no consta", "quien": "no se dice",
                                   "falta": ["un plazo"], "tipo": "tarea",
                                   "por_que_estado": "Sin cerrar: nadie lo asume en la grabación.",
                                   "nota": "La línea de 00:00:04 lleva «palabra dudosa»."})
        self.assertIn("<strong>Sin cerrar:</strong>", h)
        self.assertIn("<strong>nadie</strong> lo asume", h)
        self.assertIn("<strong>00:00:04</strong>", h)
        # Lo que va entre « » es literal: ni la cita ni las marcas se tocan.
        self.assertIn("«nadie lo sabe todavía»", h)
        self.assertIn("«palabra dudosa»", h)

    def test_resaltar_escapa_antes_de_marcar(self):
        self.assertEqual("x &lt;b&gt;<strong>no se dice</strong>&lt;/b&gt;", M.resaltar("x <b>no se dice</b>"))
        self.assertEqual("", M.resaltar(None))
        self.assertEqual("en «nadie 00:00:01» sí", M.resaltar("en «nadie 00:00:01» sí"))

    def test_la_pagina_resalta_igual_que_el_word(self):
        """resalte.js (la página) y md2html.resaltar dan el mismo HTML."""
        if not shutil.which("node"):
            self.skipTest("sin Node")
        casos = ["no se dice. Se le pidió a «Inca» un reporte, pero el texto no dice que «Inca» lo aceptara.",
                 "Sin cerrar: nadie lo asume (00:01:02).", "Asumido: se anuncia para «mañana».",
                 "la transcripción no recoge nada aquí; las lecturas automáticas no se ponen de acuerdo",
                 "a & b < c; Conviene oír antes de citar una cifra.", "el municipio, probablemente.",
                 "**ya** hecho", "Nadie"]
        js = ("import { resaltar } from './src/resalte.js';"
              "let d='';process.stdin.on('data',c=>d+=c).on('end',()=>"
              "process.stdout.write(JSON.stringify(JSON.parse(d).map(resaltar))))")
        r = subprocess.run(["node", "--input-type=module", "-e", js], cwd=str(RAIZ / "tools" / "pagina-despacho"),
                           input=json.dumps(casos), capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(0, r.returncode, r.stderr)
        self.assertEqual([M.resaltar(c) for c in casos], json.loads(r.stdout))

    def test_el_contrato_lleva_las_lineas_de_la_cita(self):
        """Se oye desde la primera hasta la última línea donde está la cita:
        «otra» está dos líneas más abajo, en b3."""
        comp = {4: {"minuto": "00:00:04", "cita": "vamos con el tema / otra", "cerrado": False, "_i": 1}}
        c = M.contrato_compromisos(comp, DOC)
        self.assertEqual(["b1", "b2", "b3"], c[0]["bloques"])
        self.assertEqual([], c[0]["sin_localizar"])

    def test_la_cita_en_lineas_anteriores_tambien_se_oye(self):
        """Contar n líneas hacia abajo dejaba sin oír la parte que va antes."""
        comp = {30: [{"minuto": "00:00:30", "cita": "buenas tardes / la cuenta del municipio", "_i": 4}]}
        self.assertEqual(["b0", "b1", "b2", "b3", "b4"], M.contrato_compromisos(comp, DOC)[0]["bloques"])

    def test_una_barra_sin_espacios_no_parte_la_cita(self):
        doc = {"segmentos": [seg(0, 0, 4, "el 3/4 del presupuesto"), seg(1, 4, 8, "otra cosa")]}
        c = M.contrato_compromisos({0: [{"minuto": "00:00:00", "cita": "el 3/4 del presupuesto", "_i": 0}]}, doc)
        self.assertEqual((["b0"], []), (c[0]["bloques"], c[0]["sin_localizar"]))

    def test_lo_que_no_esta_en_la_transcripcion_se_dice(self):
        """Si una parte de la cita no está en ninguna línea, la página no puede
        hacerla oír: va en «sin_localizar» para que no deje declarar."""
        comp = {4: [{"minuto": "00:00:04", "cita": "vamos con el tema / esto no lo dijo nadie", "_i": 1}]}
        c = M.contrato_compromisos(comp, DOC)[0]
        self.assertEqual(["esto no lo dijo nadie"], c["sin_localizar"])
        self.assertEqual(["b1"], c["bloques"])

    def test_el_id_sale_del_segundo_y_de_la_cita(self):
        """Otra lectura con un compromiso más delante no cambia el id de los demás."""
        uno = {30: [{"minuto": "00:00:30", "cita": "la cuenta del municipio", "_i": 4}]}
        dos = {4: [{"minuto": "00:00:04", "cita": "vamos con el tema", "_i": 1}],
               30: [{"minuto": "00:00:30", "cita": "la cuenta del municipio", "_i": 4}]}
        a = {x["minuto"]: x["id"] for x in M.contrato_compromisos(uno, DOC)}
        b = {x["minuto"]: x["id"] for x in M.contrato_compromisos(dos, DOC)}
        self.assertEqual(a["00:00:30"], b["00:00:30"])
        self.assertNotEqual(b["00:00:04"], b["00:00:30"])
        self.assertTrue(a["00:00:30"].startswith("c-30-"), a)

    def test_dos_compromisos_en_el_mismo_segundo_son_dos(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            p = tmp / "c.json"
            p.write_text(json.dumps({"compromisos": [
                {"minuto": "00:00:04", "de_que_se_trata": "PRIMERO", "cita": "vamos"},
                {"minuto": "00:00:04", "de_que_se_trata": "SEGUNDO", "cita": "vamos"},
                {"minuto": "0:00:04", "de_que_se_trata": "TERCERO", "cita": "el tema"}]}), encoding="utf-8")
            comps = M.compromisos_de(str(p))
            self.assertEqual(["PRIMERO", "SEGUNDO", "TERCERO"], [c["de_que_se_trata"] for c in comps[4]])
            html, _ = M.construir_bloques(DOC, {}, [], "A/x", compromisos=comps)
            for t in ("PRIMERO", "SEGUNDO", "TERCERO"):
                self.assertIn(t, html)
            ids = [x["id"] for x in M.contrato_compromisos(comps, DOC)]
            self.assertEqual(3, len(set(ids)), ids)
            self.assertEqual(sorted(ids), sorted(re.findall(r'class="compromiso[^"]*" data-minuto="[^"]*" data-id="([^"]+)"', html)))
        finally:
            shutil.rmtree(str(tmp), ignore_errors=True)

    def test_sin_cerrado_no_dice_asumido_ni_inventa_el_plazo(self):
        """Lo que la lectura no trae no se afirma: ni «asumido» ni «Plazo: no se dice»."""
        h = M.etiqueta_compromiso({"minuto": "00:01:00", "de_que_se_trata": "enviar el informe",
                                   "quien": "el secretario"})
        self.assertNotIn("asumido", h)
        self.assertNotIn("Plazo", h)
        self.assertIn("Quién lo asume", h)
        self.assertIsNone(M.estado_compromiso({}))
        self.assertEqual("asumido", M.estado_compromiso({"cerrado": True}))

    def test_la_cara_visible_dice_que_es_una_lectura(self):
        """El aviso va fuera de la ficha plegada, que ni se imprime."""
        h = M.etiqueta_compromiso({"minuto": "00:01:00", "de_que_se_trata": "algo", "quien": "x", "cerrado": True})
        visible = re.sub(r"<details.*?</details>", "", h, flags=re.S)
        self.assertIn("lectura automática", visible)
        self.assertIn("nadie lo ha oído", visible)


def datos_de(html):
    return json.loads(re.search(r'id="datos">(.*?)</script>', Path(html).read_text(encoding="utf-8"), re.S).group(1))


def pagina_sintetica(tmp, clave_md="# Transcripción\n\n---\n\n**[00:00:00] · Hablante 1** buenas tardes\n",
                     ent=None, n=1, extra=()):
    ent = ent or tmp / "ENTREGA - prueba"
    (ent / "Transcripciones").mkdir(parents=True, exist_ok=True)
    md = tmp / ("t%d.md" % n)
    md.write_text(clave_md + "\n**[00:00:04]** vamos con el tema\n", encoding="utf-8")
    datos = tmp / ("d%d.json" % n)
    datos.write_text(json.dumps({"publicada": {"etiqueta": "A/x", "segmentos": SEGS[:2]}, "marcas": {}, "ventanas": []},
                                ensure_ascii=False), encoding="utf-8")
    html = ent / "Transcripciones" / ("Audio %d - oir y marcar.html" % n)
    r = subprocess.run([sys.executable, str(SCRIPTS / "md2html.py"), str(md), str(html), "--datos", str(datos)]
                       + [str(x) for x in extra], capture_output=True, text=True, encoding="utf-8", env=ENV)
    assert r.returncode == 0, r.stderr
    return ent, datos_de(html)["clave"]


class RecogerLoDeclarado(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.ent, self.clave = pagina_sintetica(self.tmp)
        (self.ent / R.CARPETA).mkdir()
        self.sal = self.tmp / "salida"

    def tearDown(self):
        shutil.rmtree(str(self.tmp), ignore_errors=True)

    def declarar(self, nombre, clave, exportado, **extra):
        d = {"formato": "despacho/estado-de-comprobacion", "version": 2, "clave": clave, "exportado": exportado,
             "documento": "Transcripción", "estado": {"b1": {"estado": "corregido", "fecha": "23/09/2026",
                                                             "correccion": "vamos con el acta"}}}
        d.update(extra)
        (self.ent / R.CARPETA / nombre).write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")

    def correr(self, *extra):
        return R.main([str(self.ent), "--salida", str(self.sal)] + list(extra))

    def informe(self):
        return next(self.sal.glob("*.md")).read_text(encoding="utf-8")

    def test_recoge_lo_ultimo_de_cada_pagina(self):
        self.declarar("a - en curso.json", self.clave, "2026-09-23T10:00:00Z",
                      ilegibles={"i0": {"entiende": "si", "idea": "la idea VIEJA", "desde": 8, "hasta": 20, "oido": 1}})
        self.declarar("a - 2026-09-23 11.00.json", self.clave, "2026-09-23T11:00:00Z",
                      ilegibles={"i0": {"entiende": "si", "idea": "la idea que contó", "quien": "2", "desde": 8, "hasta": 20, "oido": 1}},
                      voces={"2": "Persona Dos"},
                      compromisos={"c0": {"es": "si", "quien": "no_se_dice", "plazo": "el lunes", "minuto": "00:00:04"}},
                      glosario=[{"oye": "Popayan", "dijo": "Popayán", "estado": "aceptada"}])
        self.assertEqual(0, self.correr())
        t = self.informe()
        self.assertIn("la idea que contó", t)
        self.assertNotIn("la idea VIEJA", t)
        self.assertIn("vamos con el acta", t)
        self.assertIn("Persona Dos, según ella", t)
        self.assertIn("el lunes", t)
        self.assertIn("| Popayan | Popayán |", t)

    def test_lo_de_otra_version_se_descarta_y_se_dice(self):
        self.declarar("bueno.json", self.clave, "2026-09-23T10:00:00Z")
        self.declarar("viejo.json", "otra-clave", "2026-09-23T12:00:00Z")
        self.assertEqual(0, self.correr())
        self.assertIn("viejo.json", self.informe())
        self.assertIn("otra versión", self.informe())

    def test_sin_declaraciones_de_esta_entrega_se_detiene(self):
        self.declarar("viejo.json", "otra-clave", "2026-09-23T12:00:00Z")
        with self.assertRaises(SystemExit):
            self.correr()

    def test_no_sobrescribe(self):
        self.declarar("bueno.json", self.clave, "2026-09-23T10:00:00Z")
        self.assertEqual(0, self.correr())
        antes = sorted(p.name for p in self.sal.iterdir())
        import time; time.sleep(1.1)
        self.assertEqual(0, self.correr())
        despues = sorted(p.name for p in self.sal.iterdir())
        self.assertEqual(len(antes) * 2, len(despues))
        self.assertTrue(set(antes) <= set(despues))

    def test_lo_que_propuso_la_maquina_no_entra_como_hecho(self):
        """Las propuestas de la máquina no viajan en la declaración; el informe lo dice."""
        self.declarar("bueno.json", self.clave, "2026-09-23T10:00:00Z")
        self.correr()
        self.assertIn("Lo que la máquina propuso y ella no confirmó no está aquí como hecho", self.informe())

    def test_la_correccion_dice_de_que_lectura_partio(self):
        self.declarar("bueno.json", self.clave, "2026-09-23T10:00:00Z", estado={
            "b1": {"estado": "corregido", "correccion": "vamos con el acta", "partio_de": "Lectura del canal derecho",
                   "sugerido": "vamos con el ata"}})
        self.assertEqual(0, self.correr())
        self.assertIn("vamos con el acta (partió de la lectura del canal derecho, que decía «vamos con el ata»)",
                      self.informe())

    def test_sin_de_donde_partio_la_correccion_sale_como_antes(self):
        self.declarar("bueno.json", self.clave, "2026-09-23T10:00:00Z")
        self.assertEqual(0, self.correr())
        self.assertIn("| vamos con el tema | vamos con el acta |", self.informe())
        self.assertNotIn("partió", self.informe())

    def test_una_celda_no_rompe_la_tabla(self):
        """Saltos de línea y «|» en lo que ella escribe no parten la fila ni
        abren columnas: cada fila tiene las columnas de su cabecera."""
        self.declarar("bueno.json", self.clave, "2026-09-23T10:00:00Z",
                      estado={"b1": {"estado": "corregido", "correccion": "vamos | al\nacta"}},
                      voces={"1": "Ana | jefa\nde área"}, resumen_voces={"1": {"segundos": 8, "confirmado": 1}},
                      ilegibles={"i-8-20": {"entiende": "si", "idea": "pide el acta\n| no | inventado |",
                                            "palabras": "a|b\r\nc", "quien": "1", "desde": 8, "hasta": 20}},
                      compromisos={"c-4-x": {"es": "si", "quien": "otra", "quien_texto": "Ana | jefa\nx",
                                             "plazo": "lunes|martes", "minuto": "00:00:04"}},
                      glosario=[{"oye": "a|b", "dijo": "c\nd", "estado": "aceptada", "nota": "x|y"}])
        self.assertEqual(0, self.correr())
        t = self.informe()
        tablas, actual = [], None
        for l in t.split("\n"):
            if l.startswith("|"):
                celdas = re.split(r"(?<!\\)\|", l.strip())[1:-1]
                if actual is None:
                    actual = [len(celdas)]
                    tablas.append(actual)
                else:
                    actual.append(len(celdas))
            else:
                actual = None
        self.assertGreaterEqual(len(tablas), 5, t)
        for tb in tablas:
            self.assertEqual(len(set(tb)), 1, t)
        self.assertIn("pide el acta / \\| no \\| inventado \\|", t)
        self.assertIn("vamos \\| al / acta", t)

    def test_no_es_compromiso_no_lleva_quien_ni_plazo(self):
        """Si dijo «sí, lo asume X» y luego «No lo es», lo de antes no se atribuye."""
        self.declarar("bueno.json", self.clave, "2026-09-23T10:00:00Z",
                      compromisos={"c-4-x": {"es": "no", "quien": "2", "plazo": "el lunes", "minuto": "00:00:04"}})
        self.assertEqual(0, self.correr())
        t = self.informe()
        self.assertNotIn("el lunes", t)
        self.assertNotIn("Hablante 2", t)
        self.assertIn("| 00:00:04 | no | — (no es compromiso) | — (no es compromiso) |", t)

    def test_quien_sin_contestar_no_es_no_sabe_quien(self):
        self.declarar("bueno.json", self.clave, "2026-09-23T10:00:00Z",
                      ilegibles={"i-8-20": {"entiende": "si", "idea": "piden aplazar", "desde": 8, "hasta": 20},
                                 "i-30-40": {"entiende": "no", "desde": 30, "hasta": 40}})
        self.assertEqual(0, self.correr())
        t = self.informe()
        self.assertIn("| piden aplazar | — (no lo dijo) |", t)
        self.assertIn("| no se entiende | — | — | — |", t)
        self.assertNotIn("no sabe quién", t)

    def test_lo_guardado_dentro_de_transcripciones_se_recoge(self):
        """Si al guardar eligió «Transcripciones», la carpeta queda ahí dentro."""
        c = self.ent / "Transcripciones" / R.CARPETA
        c.mkdir()
        d = {"formato": "despacho/estado-de-comprobacion", "clave": self.clave, "exportado": "2026-09-23T10:00:00Z",
             "estado": {"b1": {"estado": "corregido", "correccion": "DENTRO DE TRANSCRIPCIONES"}}}
        (c / "a.json").write_text(json.dumps(d), encoding="utf-8")
        self.assertEqual(0, self.correr())
        self.assertIn("DENTRO DE TRANSCRIPCIONES", self.informe())

    def test_en_un_proyecto_se_recoge_de_2_borradores_y_de_donde_se_guardaba_antes(self):
        proyecto = self.tmp / "Proyecto"
        ent = proyecto / "3-Para presentar" / self.ent.name
        ent.parent.mkdir(parents=True)
        shutil.move(str(self.ent), str(ent))
        for donde, nombre, hora, texto in ((R.EN_PROYECTO, "nuevo.json", "11", "EN BORRADORES"),
                                           (R.ANTES_EN_PROYECTO, "antiguo.json", "10", "DONDE SE GUARDABA ANTES")):
            c = proyecto.joinpath(*donde, ent.name)
            c.mkdir(parents=True)
            (c / nombre).write_text(json.dumps({
                "formato": "despacho/estado-de-comprobacion", "clave": self.clave,
                "exportado": "2026-09-23T%s:00:00Z" % hora,
                "estado": {"b1": {"estado": "corregido", "correccion": texto}}}), encoding="utf-8")
        self.assertEqual("2-Borradores", R.EN_PROYECTO[0])
        self.assertEqual(0, R.main([str(ent), "--salida", str(self.sal)]))
        t = self.informe()
        self.assertIn("EN BORRADORES", t)
        self.assertIn("antiguo.json` (no se usa", t)

    def test_con_la_entrega_en_2_borradores_entregas_tambien_encuentra_el_proyecto(self):
        """ADR-023: la entrega vive en «<proyecto>/2-Borradores/Entregas/»."""
        proyecto = self.tmp / "Proyecto"
        ent = proyecto / "2-Borradores" / "Entregas" / self.ent.name
        ent.parent.mkdir(parents=True)
        shutil.move(str(self.ent), str(ent))
        c = proyecto.joinpath(*R.EN_PROYECTO, ent.name)
        c.mkdir(parents=True)
        (c / "en curso.json").write_text(json.dumps({
            "formato": "despacho/estado-de-comprobacion", "clave": self.clave, "exportado": "2026-09-23T11:00:00Z",
            "estado": {"b1": {"estado": "corregido", "correccion": "EN LA FORMA NUEVA"}}}), encoding="utf-8")
        self.assertEqual(0, R.main([str(ent), "--salida", str(self.sal)]))
        self.assertIn("EN LA FORMA NUEVA", self.informe())

    def test_lo_arrastrado_a_lo_que_declare_a_secas_tambien_se_recoge(self):
        """Safari, en el Mac, no deja escribir en carpetas: lo guardado se descarga y
        ella lo ARRASTRA a «2-Borradores/Lo que declaré», sin la subcarpeta de la
        entrega. Tiene que recogerse sin pasarlo a mano; y la declaración de voces,
        que puede caer en la misma carpeta, no es un error (2026-09-24)."""
        proyecto = self.tmp / "Proyecto"
        ent = proyecto / "2-Borradores" / "Entregas" / self.ent.name
        ent.parent.mkdir(parents=True)
        shutil.move(str(self.ent), str(ent))
        c = proyecto.joinpath(*R.EN_PROYECTO)
        c.mkdir(parents=True)
        (c / "comprobado - Audio 1 - 2026-09-24 10.00.json").write_text(json.dumps({
            "formato": "despacho/estado-de-comprobacion", "clave": self.clave, "exportado": "2026-09-24T10:00:00Z",
            "estado": {"b1": {"estado": "corregido", "correccion": "ARRASTRADO DESDE DESCARGAS"}}}), encoding="utf-8")
        (c / "voces declaradas - Reunion.json").write_text(json.dumps({
            "formato": "despacho/voces-linea-a-linea", "clave": "otra", "lineas": {}}), encoding="utf-8")
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(0, R.main([str(ent), "--salida", str(self.sal)]))
        self.assertIn("ARRASTRADO DESDE DESCARGAS", self.informe())
        self.assertIn("es la declaración de voces", err.getvalue())
        self.assertNotIn("se ignora", err.getvalue())

    def test_lo_pasado_a_mano_dice_de_donde_vino(self):
        """La cabecera no puede decir «de Lo que declaré» de un archivo de Descargas."""
        suelto = self.tmp / "Descargas" / "comprobado - Audio 1.json"
        suelto.parent.mkdir()
        suelto.write_text(json.dumps({"formato": "despacho/estado-de-comprobacion", "clave": self.clave,
                                      "exportado": "2026-09-23T10:00:00Z", "estado": {}}), encoding="utf-8")
        self.assertEqual(0, self.correr(str(suelto)))
        t = self.informe()
        cab = t[:t.index("**Qué es:**")]
        self.assertIn("pasados a mano", cab)
        self.assertIn(str(suelto), cab)
        self.assertNotIn("de la carpeta", cab)
        self.assertIn("(pasado a mano)", t)


class RecogerCasaConLaPagina(unittest.TestCase):
    """Lo declarado se casa con los compromisos y los tramos de la página por
    su id, que sale del contenido; lo que no casa se dice aparte."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        comp = self.tmp / "c.json"
        comp.write_text(json.dumps({"compromisos": [{"minuto": "00:00:04", "cita": "vamos con el tema",
                                                     "de_que_se_trata": "algo", "cerrado": False}]}), encoding="utf-8")
        self.ent, self.clave = pagina_sintetica(self.tmp, extra=["--compromisos", comp])
        (self.ent / R.CARPETA).mkdir()
        self.d = datos_de(self.ent / "Transcripciones" / "Audio 1 - oir y marcar.html")
        self.sal = self.tmp / "salida"

    def tearDown(self):
        shutil.rmtree(str(self.tmp), ignore_errors=True)

    def test_casa_por_id_y_lo_que_no_casa_se_dice_aparte(self):
        cid = self.d["compromisos"][0]["id"]
        self.assertTrue(cid.startswith("c-4-"), cid)
        d = {"formato": "despacho/estado-de-comprobacion", "clave": self.clave, "exportado": "2026-09-23T10:00:00Z",
             "estado": {},
             "compromisos": {cid: {"es": "si", "quien": "no_se_dice", "plazo": "PLAZO BUENO", "minuto": "00:00:04"},
                             "c0": {"es": "si", "quien": "no_se_dice", "plazo": "PLAZO VIEJO", "minuto": "00:00:04"}},
             "ilegibles": {"i0": {"entiende": "si", "idea": "IDEA SUELTA", "quien": "1", "desde": 100, "hasta": 110}}}
        (self.ent / R.CARPETA / "a.json").write_text(json.dumps(d), encoding="utf-8")
        self.assertEqual(0, R.main([str(self.ent), "--salida", str(self.sal)]))
        t = next(self.sal.glob("*.md")).read_text(encoding="utf-8")
        self.assertLess(t.index("PLAZO BUENO"), t.index("no casan con ningún compromiso"))
        self.assertLess(t.index("no casan con ningún compromiso"), t.index("PLAZO VIEJO"))
        self.assertLess(t.index("ya no pregunta"), t.index("IDEA SUELTA"))


class RecogerElGlosario(unittest.TestCase):
    """El glosario es uno por caso: vale el del guardado más reciente."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.ent = self.tmp / "ENTREGA - prueba"
        self.sal = self.tmp / "salida"

    def tearDown(self):
        shutil.rmtree(str(self.tmp), ignore_errors=True)

    def paginas(self, *extra):
        _, c1 = pagina_sintetica(self.tmp, "# Audio uno\n\n---\n\n**[00:00:00]** buenas tardes\n", self.ent, 1, extra)
        _, c2 = pagina_sintetica(self.tmp, "# Audio dos\n\n---\n\n**[00:00:00]** buenas tardes\n", self.ent, 2, extra)
        (self.ent / R.CARPETA).mkdir(exist_ok=True)
        return c1, c2

    def declarar(self, nombre, clave, exportado, glosario):
        (self.ent / R.CARPETA / nombre).write_text(json.dumps(
            {"formato": "despacho/estado-de-comprobacion", "clave": clave, "exportado": exportado, "estado": {},
             "glosario": glosario}, ensure_ascii=False), encoding="utf-8")

    def informe(self):
        self.assertEqual(0, R.main([str(self.ent), "--salida", str(self.sal)]))
        return next(self.sal.glob("*.md")).read_text(encoding="utf-8")

    def test_lo_que_quito_despues_no_vuelve_como_aceptado(self):
        c1, c2 = self.paginas("--caso", "X")
        # La del Audio 2 se guardó antes y por nombre se recorre después.
        self.declarar("z - Audio 2.json", c2, "2026-09-23T10:00:00Z",
                      [{"oye": "Lugarviejo", "dijo": "Lugarnuevo", "estado": "aceptada", "origen": "usted",
                        "excepciones": ["b0"], "fecha": "23/09/2026"}])
        self.declarar("a - Audio 1.json", c1, "2026-09-23T11:00:00Z", [])
        t = self.informe()
        self.assertNotIn("| Lugarviejo | Lugarnuevo |", t)
        self.assertIn("No se usan:** «Lugarviejo» → «Lugarnuevo»", t)

    def test_excepciones_origen_y_nota_de_la_maquina(self):
        c1, c2 = self.paginas("--caso", "X")
        self.declarar("a.json", c1, "2026-09-23T11:00:00Z", [
            {"oye": "Lugarviejo", "dijo": "Lugarnuevo", "estado": "aceptada", "origen": "usted",
             "excepciones": [{"clave": c2, "id": "b1"}, {"clave": "otra", "id": "b0", "dijo": "Lugarviejo"}],
             "nota": "lo oí yo"},
            {"id": "u1", "de": "s0", "oye": "Sigla", "dijo": "SIGLA", "estado": "aceptada",
             "origen": "sugerencia aceptada por usted", "nota": "dice la máquina"},
            {"id": "u2", "de": "s1", "oye": "Otra", "dijo": "OTRA", "estado": "aceptada",
             "origen": "sugerencia aceptada por usted", "nota": "la mía", "nota_maquina": "la de la máquina"}])
        self.declarar("b.json", c2, "2026-09-23T10:00:00Z", [])
        t = self.informe()
        self.assertIn("| Lugarviejo | Lugarnuevo | aceptada | suya | Audio dos, 00:00:04; línea b0 de otra versión "
                      "de la transcripción (según ella, ahí se dijo «Lugarviejo») | lo oí yo |", t)
        self.assertIn("| Sigla | SIGLA | aceptada | sugerencia aceptada | — | (nota de la sugerencia, de la máquina: "
                      "dice la máquina) |", t)
        self.assertIn("| la mía (nota de la sugerencia, de la máquina: la de la máquina) |", t)

    def test_sin_caso_gana_la_entrada_mas_reciente_y_no_el_orden_de_archivo(self):
        c1, c2 = self.paginas()
        self.declarar("a.json", c1, "2026-09-23T12:00:00Z",
                      [{"oye": "Lugarviejo", "dijo": "VIEJA", "estado": "aceptada", "fecha": "22/09/2026"}])
        self.declarar("z.json", c2, "2026-09-23T09:00:00Z",
                      [{"oye": "lugarviejo", "dijo": "NUEVA", "estado": "aceptada", "fecha": "23/09/2026"}])
        t = self.informe()
        self.assertIn("| NUEVA |", t)
        self.assertNotIn("VIEJA", t)


class ReleerTramo(unittest.TestCase):

    def test_recortes(self):
        v = RT.ventanas(441.0, 452.0, duracion=1327)
        self.assertEqual((440.5, 452.5), v[0])
        self.assertEqual((437.0, 456.0), v[1])
        self.assertEqual(4, len(v))
        self.assertTrue(all(b - a >= 1.0 for a, b in v))

    def test_no_sale_del_audio(self):
        v = RT.ventanas(0.5, 3.0, duracion=4.0)
        self.assertTrue(all(a >= 0 and b <= 4.0 for a, b in v))

    def test_cuenta_palabra_entera(self):
        ls = [{"texto": "esto es lo que dice la norma"}, {"texto": "la regla dijo"}, {"texto": "arreglar la ley"}]
        self.assertEqual((1, 3), RT.cuantas_dicen(ls, "regla"))   # «arreglar» no cuenta
        self.assertEqual((1, 3), RT.cuantas_dicen(ls, "Norma"))

    def test_hora_mal_escrita_detiene(self):
        with self.assertRaises(SystemExit):
            RT.a_segundos("7:21")

    def test_la_cuenta_va_partida_y_el_recorte_ancho_aparte(self):
        """Una palabra que solo sale en el contexto del recorte ancho no se
        cuenta como si sostuviera la del tramo; y se ve por recorte y por pista."""
        rs = RT.recortes(441.0, 452.0, duracion=1327)
        self.assertEqual(RT.ventanas(441.0, 452.0, duracion=1327), [(a, b) for _n, a, b in rs])
        pistas = ["la mezcla tal cual", "la mezcla limpia", "el canal izquierdo", "el canal derecho"]
        ls = [{"recorte": n, "pista": p, "texto": "dijo la palabra" if n == RT.ANCHO else "otra cosa"}
              for n, _a, _b in rs for p in pistas]
        c = RT.cuentas(ls, "palabra")
        self.assertEqual({"dicen": 0, "de": 12}, c["sin_el_recorte_ancho"])
        self.assertEqual({"dicen": 4, "de": 4}, c["recorte_ancho"])
        self.assertEqual({"dicen": 0, "de": 3}, c["por_pista"]["el canal derecho"])
        self.assertEqual({"dicen": 0, "de": 4}, c["por_recorte"]["el tramo"])
        self.assertNotIn(RT.ANCHO, c["por_recorte"])
        self.assertIn("0 de 12", RT.cuentas_txt("palabra", c))


class ElGlosarioSugerido(unittest.TestCase):

    def test_llega_a_la_pagina_como_sugerencia(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            g = tmp / "g.json"
            g.write_text(json.dumps({"sugerencias": [{"oye": "Popayan", "dijo": "Popayán", "nota": "n"},
                                                     {"oye": "", "dijo": "x"}]}, ensure_ascii=False), encoding="utf-8")
            md = tmp / "t.md"
            md.write_text("# T\n\n---\n\n**[00:00:00] · Hablante 1** en Popayan\n", encoding="utf-8")
            datos = tmp / "d.json"
            datos.write_text(json.dumps({"publicada": {"etiqueta": "A/x", "segmentos": [seg(0, 0, 3, "en Popayan")]},
                                         "marcas": {}, "ventanas": []}, ensure_ascii=False), encoding="utf-8")
            html = tmp / "p.html"
            r = subprocess.run([sys.executable, str(SCRIPTS / "md2html.py"), str(md), str(html), "--datos", str(datos),
                                "--glosario", str(g), "--caso", "abc"], capture_output=True, text=True, encoding="utf-8",
                               env=ENV)
            self.assertEqual(0, r.returncode, r.stderr)
            d = json.loads(re.search(r'id="datos">(.*?)</script>', html.read_text(encoding="utf-8"), re.S).group(1))
            self.assertEqual([{"oye": "Popayan", "dijo": "Popayán", "nota": "n"}], d["glosario"])
            self.assertEqual("abc", d["caso"])
        finally:
            shutil.rmtree(str(tmp), ignore_errors=True)


class ElContratoNoSeRompe(unittest.TestCase):
    """Un «</script>» en cualquier texto del contrato cortaba el bloque de
    datos: la página se quedaba sin paneles, lo de detrás entraba como HTML
    vivo y recoger_lo_declarado dejaba de ver la página."""

    MALO = "</script><h1 id=inyectado>x</h1><!--<script>"

    def test_ningun_texto_corta_el_bloque_de_datos(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            m = self.MALO
            g = tmp / "g.json"
            g.write_text(json.dumps({"sugerencias": [{"oye": "uno" + m, "dijo": "dos" + m, "nota": m}]}), encoding="utf-8")
            c = tmp / "c.json"
            c.write_text(json.dumps({"compromisos": [{"minuto": "00:00:04", "cita": "vamos" + m, "de_que_se_trata": m,
                                                      "quien": m, "plazo": m, "tipo": m}]}), encoding="utf-8")
            r_ = tmp / "r.json"
            r_.write_text(json.dumps({"rescates": [{"audio": "A1", "ini": 9, "fin": 19, "texto": m}]}), encoding="utf-8")
            segs = [seg(0, 0, 4, "buenas" + m), seg(1, 4, 8, "vamos" + m), seg(2, 20, 24, "sigue")]
            datos = tmp / "d.json"
            datos.write_text(json.dumps({"publicada": {"etiqueta": "A/x", "segmentos": segs, "duracion_s": 40},
                                         "marcas": {}, "etiquetas": {"1": {"texto": m}},
                                         "ventanas": [{"t": 0.0, "medio": 0.3, "textos": {"A/x": "a", "otra": m}}]}),
                             encoding="utf-8")
            md = tmp / "t.md"
            md.write_text("# T\n\n---\n\n**[00:00:00] · Hablante 1** buenas\n", encoding="utf-8")
            ent = tmp / "ENTREGA - prueba"
            (ent / "Transcripciones").mkdir(parents=True)
            html = ent / "Transcripciones" / "Audio 1 - oir y marcar.html"
            r = subprocess.run([sys.executable, str(SCRIPTS / "md2html.py"), str(md), str(html), "--datos", str(datos),
                                "--glosario", str(g), "--compromisos", str(c), "--rescates", str(r_),
                                "--rescates-audio", "A1", "--caso", m],
                               capture_output=True, text=True, encoding="utf-8", env=ENV)
            self.assertEqual(0, r.returncode, r.stderr)
            t = html.read_text(encoding="utf-8")
            bloque = re.search(r'<script type="application/json" id="datos">(.*?)</script>', t, re.S).group(1)
            d = json.loads(bloque)
            self.assertNotIn("<", bloque)
            self.assertEqual(m, d["caso"])
            self.assertEqual(m, d["glosario"][0]["nota"])
            self.assertEqual(m, d["compromisos"][0]["de_que_se_trata"])
            self.assertTrue(any(m in l["texto"] for x in d["ilegibles"] for l in x["lecturas"]))
            self.assertNotIn("<h1 id=inyectado>", t)
            self.assertIn(d["clave"], R.paginas(str(ent)))
        finally:
            shutil.rmtree(str(tmp), ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
