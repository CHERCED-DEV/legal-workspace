# -*- coding: utf-8 -*-
"""Que el Word y la pagina de una entrega digan lo mismo.

Dos defectos del 2026-09-23, los dos de la misma familia -- la pagina y el
Word salian de fuentes distintas y nadie los comparaba --, con prueba que los
sujeta:

  · **Las voces.** Se rehizo la separacion de voces de una grabacion; los
    datos cambiaron y el Markdown no. El Word decia «Hablante 2» donde la
    pagina decia «Hablante 4» para la misma linea. Ahora `construir_entrega`
    rehace las etiquetas desde los mismos datos que usa la pagina.
  · **La cabecera.** `md2html` tiraba en silencio lo que la cabecera trae y no
    es «**Campo:** valor». El aviso de que una entrega sustituia a otra, con el
    enlace a la correccion, no salio nunca en la portada.

Todo sintetico: nada de ningun caso.

    python3 evals/scripts/test_entrega_coherente.py
"""
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

import construir_entrega as CE  # noqa: E402

# El hijo escribe en UTF-8 aunque la consola no lo sea (en Windows, cp1252):
# sin esto, leer su salida como UTF-8 daba ERROR en esas consolas.
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def seg(i, inicio, texto, voz):
    return {"i": i, "inicio": inicio, "fin": inicio + 1.5, "texto": texto, "voz": voz,
            "palabras": [{"p": p, "c": 0.9} for p in texto.split()]}


VIEJOS = [seg(0, 1.2, u"buenas tardes", 1), seg(1, 3.4, u"gracias por venir", 1),
          seg(2, 5.1, u"una pregunta", 2), seg(3, 7.9, u"sí, dígame", 1),
          seg(4, 9.3, u"ruido", None), seg(5, 11.0, u"sigamos", 1)]

# El Markdown que la convencion produce desde VIEJOS: etiqueta solo donde cambia la voz.
MD = u"""
**[00:00:01] · Hablante 1** buenas tardes

**[00:00:03]** gracias por venir  `[?]` *(palabra dudosa)*

**[00:00:05] · Hablante 2** una pregunta

**[00:00:07] · Hablante 1** sí, dígame

**[00:00:09] · Hablante ?** ruido  `[?]` *(puede no ser habla)*

**[00:00:11] · Hablante 1** sigamos
"""

# La separacion rehecha: la segunda linea es de otra voz, y la voz 2 pasa a ser la 4.
NUEVOS = [dict(s) for s in VIEJOS]
NUEVOS[1]["voz"] = 3
NUEVOS[2]["voz"] = 4


def etiquetas(cuerpo):
    """La voz efectiva de cada linea, como la lee una persona: la ultima etiqueta vista."""
    out, cur = [], None
    for l in cuerpo.split("\n"):
        m = CE.ETIQUETA.match(l)
        if m:
            if m.group(3):
                cur = m.group(3).replace(u" · Hablante ", "")
            out.append(cur)
    return out


def texto(cuerpo):
    return [m.group(2) for m in (CE.LINEA.match(l) for l in cuerpo.split("\n")) if m]


class LasVoces(unittest.TestCase):

    def test_con_sus_propios_datos_el_markdown_sale_identico(self):
        nuevo, n = CE.voces_desde_datos(MD, VIEJOS)
        self.assertEqual(MD, nuevo)
        self.assertEqual(0, n)

    def test_con_los_datos_nuevos_cada_linea_lleva_la_voz_de_los_datos(self):
        nuevo, n = CE.voces_desde_datos(MD, NUEVOS)
        esperado = ["?" if s["voz"] is None else str(s["voz"]) for s in NUEVOS]
        self.assertEqual(esperado, etiquetas(nuevo))
        self.assertGreater(n, 0)

    def test_la_etiqueta_solo_donde_cambia_la_voz(self):
        nuevo, _ = CE.voces_desde_datos(MD, [dict(s, voz=1) for s in VIEJOS])
        self.assertEqual(1, nuevo.count(u"Hablante"), nuevo)

    def test_no_toca_el_texto_ni_los_avisos(self):
        nuevo, _ = CE.voces_desde_datos(MD, NUEVOS)
        self.assertEqual(texto(MD), texto(nuevo))
        self.assertEqual(MD.count("`[?]`"), nuevo.count("`[?]`"))
        self.assertIn(u"*(puede no ser habla)*", nuevo)

    def test_un_texto_que_no_casa_detiene(self):
        malos = [dict(s) for s in NUEVOS]
        malos[3]["texto"] = u"otra cosa"
        with self.assertRaises(SystemExit):
            CE.voces_desde_datos(MD, malos)

    def test_una_hora_que_no_casa_detiene(self):
        malos = [dict(s) for s in NUEVOS]
        malos[3]["inicio"] = 8.2
        with self.assertRaises(SystemExit):
            CE.voces_desde_datos(MD, malos)

    def test_distinto_numero_de_lineas_detiene(self):
        with self.assertRaises(SystemExit):
            CE.voces_desde_datos(MD, NUEVOS[:-1])
        with self.assertRaises(SystemExit):
            CE.voces_desde_datos(MD, NUEVOS + [seg(6, 13.0, u"más", 1)])

    def test_la_cuenta_de_voces_no_cuenta_las_lineas_sin_voz(self):
        self.assertEqual(2, CE.voces(VIEJOS))
        self.assertEqual(3, CE.voces(NUEVOS))  # 1, 3 y 4: la 2 paso a ser la 4


class LaCabeceraDeLaPagina(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.html = self.tmp / "p.html"

    def tearDown(self):
        shutil.rmtree(str(self.tmp), ignore_errors=True)

    def pagina(self, md, *extra):
        entrada = self.tmp / "e.md"
        entrada.write_text(md, encoding="utf-8")
        r = subprocess.run([sys.executable, str(SCRIPTS / "md2html.py"), str(entrada), str(self.html)]
                           + list(extra), capture_output=True, text=True, encoding="utf-8", env=ENV)
        self.assertEqual(0, r.returncode, r.stderr[-600:])
        t = self.html.read_text(encoding="utf-8")
        return re.sub(r"<script\b.*?</script>", "", t, flags=re.S)

    def test_un_parrafo_suelto_de_la_cabecera_sale_en_la_pagina(self):
        t = self.pagina(u"# Portada\n\n**Estado:** borrador\n\n"
                        u"**Sustituye a la anterior.** Vea [qué cambió](<nota.html>).\n\n---\n\n## Cuerpo\n\nTexto.\n")
        self.assertIn(u"<strong>Sustituye a la anterior.</strong>", t)
        self.assertIn(u'href="nota.html"', t)

    def test_ni_el_titulo_ni_los_campos_salen_dos_veces(self):
        t = self.pagina(u"# Portada única\n\n**Estado:** borrador singular\n\nUn aviso.\n\n---\n\nTexto.\n")
        cuerpo = t[t.index('id="contenido"'):]
        self.assertNotIn(u"Portada única", cuerpo)
        self.assertNotIn(u"borrador singular", cuerpo)
        self.assertIn(u"Un aviso.", cuerpo)

    def test_sin_separador_no_se_duplica_nada(self):
        """Sin `---` todo el Markdown ya es contenido: no hay cabecera que rescatar."""
        t = self.pagina(u"# Nota\n\nUn párrafo que solo debe salir una vez.\n")
        self.assertEqual(1, t.count(u"Un párrafo que solo debe salir una vez."))

    def test_en_la_transcripcion_sale_el_aviso_de_la_cabecera(self):
        datos = self.tmp / "d.json"
        datos.write_text(json.dumps({"publicada": {"etiqueta": "A/x", "segmentos": VIEJOS},
                                     "marcas": {}, "ventanas": []}, ensure_ascii=False), encoding="utf-8")
        t = self.pagina(u"# Transcripción\n\n**Duración:** 00:00:12\n\n"
                        u"> **Esta transcripción no es la grabación.** El mismo número de hablante "
                        u"no prueba que sea la misma persona.\n\n---\n" + MD, "--datos", str(datos))
        self.assertIn(u"no prueba que sea la misma persona", t)


MARCAS = {"0": [], "1": ["palabra dudosa"], "2": [], "3": [], "4": ["puede no ser habla"], "5": []}


class LosAvisosYLosNombres(unittest.TestCase):
    """Lo que encontro la revision adversaria del 2026-09-23."""

    def test_con_sus_marcas_los_avisos_salen_identicos(self):
        nuevo, n = CE.lineas_desde_datos(MD, VIEJOS, MARCAS)
        self.assertEqual((MD, 0), (nuevo, n))

    def test_los_avisos_salen_de_los_datos(self):
        marcas = dict(MARCAS, **{"2": ["voz dudosa"], "1": []})
        nuevo, _ = CE.lineas_desde_datos(MD, VIEJOS, marcas)
        self.assertIn(u"una pregunta  `[?]` *(voz dudosa)*", nuevo)
        self.assertNotIn(u"gracias por venir  `[?]`", nuevo)
        self.assertEqual(texto(MD), texto(nuevo))

    def test_los_nombres_declarados_se_conservan(self):
        et = {"1": {"texto": u"Persona Uno · Cargo"}}
        nombrado = MD.replace(u"· Hablante 1**", u"· Hablante 1 — Persona Uno · Cargo**")
        nuevo, n = CE.voces_desde_datos(nombrado, VIEJOS, et)
        self.assertEqual((nombrado, 0), (nuevo, n))

    def test_un_nombre_que_los_datos_no_traen_detiene(self):
        """Tirarlo en silencio borraba una atribucion que hizo una persona."""
        nombrado = MD.replace(u"· Hablante 1**", u"· Hablante 1 — Persona Uno**")
        with self.assertRaises(SystemExit):
            CE.voces_desde_datos(nombrado, VIEJOS, {})

    def test_una_transcripcion_sin_voces_se_deja_como_esta(self):
        sin = u"\n**[00:00:01]** buenas tardes\n\n**[00:00:03]** gracias por venir\n"
        segs = [{k: v for k, v in s.items() if k != "voz"} for s in VIEJOS[:2]]
        nuevo, n = CE.voces_desde_datos(sin, segs)
        self.assertEqual((sin, 0), (nuevo, n))
        self.assertNotIn(u"Hablante", nuevo)


class LosAvisosDeVozAlRehacerLaSeparacion(unittest.TestCase):

    def setUp(self):
        import separar_voces
        self.S = separar_voces

    def test_con_datos_coherentes_no_cambia_nada(self):
        segs = [dict(s, pureza=0.9) for s in VIEJOS]
        segs[4]["pureza"] = 0.0
        d = {"marcas": {"0": [], "1": ["palabra dudosa"], "2": [], "3": [], "4": ["sin voz asignada"], "5": []}}
        antes = json.loads(json.dumps(d))
        self.assertEqual(0, self.S.rehacer_avisos_de_voz(d, {"segmentos": segs}, 0.60))
        self.assertEqual(antes, d)

    def test_la_duda_de_voz_se_recalcula_y_lo_demas_no_se_toca(self):
        segs = [dict(s, pureza=0.9) for s in VIEJOS]
        segs[1]["pureza"] = 0.4
        d = {"marcas": {"0": ["voz dudosa"], "1": ["palabra dudosa"], "2": [], "3": [], "4": [], "5": []}}
        n = self.S.rehacer_avisos_de_voz(d, {"segmentos": segs}, 0.60)
        self.assertEqual([], d["marcas"]["0"])
        self.assertEqual(["palabra dudosa", "voz dudosa"], d["marcas"]["1"])
        self.assertEqual(["sin voz asignada"], d["marcas"]["4"])
        self.assertEqual(3, n)


class LaCabeceraSinSorpresas(LaCabeceraDeLaPagina):
    """Casos borde del rescate de la cabecera."""

    def _datos(self):
        datos = self.tmp / "d.json"
        datos.write_text(json.dumps({"publicada": {"etiqueta": "A/x", "segmentos": VIEJOS},
                                     "marcas": {}, "ventanas": []}, ensure_ascii=False), encoding="utf-8")
        return str(datos)

    def test_sin_separador_y_con_datos_no_se_duplica_la_transcripcion(self):
        t = self.pagina(u"# Transcripción\n\n**Duración:** 00:00:12\n" + MD, "--datos", self._datos())
        self.assertEqual(1, t.count(u"gracias por venir"))

    def test_un_comentario_no_se_pinta(self):
        t = self.pagina(u"# Nota\n\n<!-- generado; no editar -->\n\nUn aviso.\n\n---\n\nTexto.\n")
        self.assertNotIn(u"no editar", t)
        self.assertIn(u"Un aviso.", t)

    def test_un_segundo_titulo_no_se_pierde(self):
        t = self.pagina(u"# Título uno\n\n# Título dos\n\n---\n\nTexto.\n")
        self.assertIn(u"Título dos", t[t.index('id="contenido"'):])

    def test_un_campo_que_sigue_abajo_no_se_parte(self):
        t = self.pagina(u"# Portada\n\n**Estado:** propuesta para su revisión, nadie ha oído\n"
                        u"todavía las grabaciones\n\n---\n\nTexto.\n")
        self.assertIn(u"nadie ha oído todavía las grabaciones</dd>", t)


class NombrarVocesNoPoneNombresSobreOtraNumeracion(unittest.TestCase):

    def test_si_el_markdown_y_los_datos_numeran_distinto_se_detiene(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            md = tmp / "t.md"
            md.write_text(u"# T\n\n---\n" + MD, encoding="utf-8")
            datos = tmp / "d.json"
            datos.write_text(json.dumps({"publicada": {"segmentos": NUEVOS}}, ensure_ascii=False),
                             encoding="utf-8")
            decl = tmp / "decl.json"
            decl.write_text(json.dumps({"formato": "despacho/voces-declaradas", "declarado_por": "X",
                                        "fecha": "2026-09-23",
                                        "voces": {"1": {"quien": "Persona Uno", "acepta_advertencia": True}}}),
                            encoding="utf-8")
            r = subprocess.run([sys.executable, str(SCRIPTS / "nombrar_voces.py"), "aplicar", str(md),
                                str(datos), str(decl), "--md-salida", str(tmp / "o.md"),
                                "--datos-salida", str(tmp / "o.json")],
                               capture_output=True, text=True, encoding="utf-8", env=ENV)
            self.assertNotEqual(0, r.returncode, r.stdout[-400:])
            self.assertIn(u"no numeran igual", r.stderr + r.stdout)
            self.assertFalse((tmp / "o.md").exists())
        finally:
            shutil.rmtree(str(tmp), ignore_errors=True)


class RehacerNoBorraLoQueEllaGuardo(unittest.TestCase):
    """La pagina guarda lo que ella declara DENTRO de la entrega, y rehacer la
    entrega borra la carpeta entera: con algo suyo dentro, se detiene."""

    def test_sin_nada_suyo_no_hay_nada_que_proteger(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual([], CE.lo_suyo_dentro(d))
            (Path(d) / CE.LO_QUE_DECLARO).mkdir()
            self.assertEqual([], CE.lo_suyo_dentro(d))

    def test_lo_que_guardo_se_ve(self):
        with tempfile.TemporaryDirectory() as d:
            c = Path(d) / CE.LO_QUE_DECLARO
            c.mkdir()
            (c / "Audio 1 - en curso.json").write_text("{}", encoding="utf-8")
            self.assertEqual([str(Path(CE.LO_QUE_DECLARO) / "Audio 1 - en curso.json")], CE.lo_suyo_dentro(d))

    def test_lo_que_guardo_en_cualquier_nivel_tambien_se_ve(self):
        """Si al guardar eligió «Transcripciones», la carpeta queda ahí dentro,
        y rehacer la entrega la borraba sin detenerse."""
        with tempfile.TemporaryDirectory() as d:
            c = Path(d) / "Transcripciones" / CE.LO_QUE_DECLARO / "sub"
            c.mkdir(parents=True)
            (c / "Audio 2 - en curso.json").write_text("{}", encoding="utf-8")
            (Path(d) / "Transcripciones" / "Audio 2 - oir y marcar.html").write_text("", encoding="utf-8")
            self.assertEqual([str(Path("Transcripciones") / CE.LO_QUE_DECLARO / "sub" / "Audio 2 - en curso.json")],
                             CE.lo_suyo_dentro(d))

    def test_recoger_tambien_lo_busca_en_cualquier_nivel(self):
        import recoger_lo_declarado as R
        with tempfile.TemporaryDirectory() as d:
            c = Path(d) / "Transcripciones" / R.CARPETA
            c.mkdir(parents=True)
            self.assertIn(os.path.normpath(str(c)), R.carpetas_de(d))

    def test_el_nombre_es_el_mismo_en_la_pagina_y_al_recoger(self):
        import recoger_lo_declarado as R
        self.assertEqual(R.CARPETA, CE.LO_QUE_DECLARO)
        js = (RAIZ / "tools" / "pagina-despacho" / "src" / "guardado.js").read_text(encoding="utf-8")
        self.assertIn("'%s'" % CE.LO_QUE_DECLARO, js)


if __name__ == "__main__":
    unittest.main(verbosity=2)
