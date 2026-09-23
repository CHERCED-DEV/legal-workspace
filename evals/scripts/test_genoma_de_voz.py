# -*- coding: utf-8 -*-
"""El genoma de voz (SPEC-15), probado con datos INVENTADOS de punta a punta.

Lo que estas pruebas fijan es el principio del SPEC-15 §2: la máquina propone
por parecido, ella declara oyendo, y solo lo declarado sostiene una
atribución. Por eso lo que más se prueba no es el cálculo, sino las fronteras:

  * una propuesta con la voz ya nombrada sigue siendo ≈, nunca ✔;
  * el `resumen` que escribe la página no se cree: la claridad se recalcula
    desde las decisiones, y la máquina solo suma si ha sido puesta a prueba
    (8 revisiones de banda alta y 90 % de acierto);
  * la biblioteca de voces se hace SOLO con líneas declaradas y nombradas;
  * nada se sobrescribe (ADR-011 §8).

Todo dato es sintético: vectores numpy generados aquí, textos inventados,
personas que no existen, audio de tonos y ruido. Ningún contenido real.

    python3 evals/scripts/test_genoma_de_voz.py
"""
import contextlib
import glob
import io
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path
from unittest import mock

RAIZ = Path(__file__).resolve().parents[2]
SCRIPTS = RAIZ / "plugins" / "despacho" / "scripts"
PROGRAMA = SCRIPTS / "genoma_de_voz.py"
sys.path.insert(0, str(SCRIPTS))

try:
    import numpy as np
except ImportError:  # pragma: no cover
    np = None

if np is not None:
    import genoma_de_voz as G  # noqa: E402
else:  # pragma: no cover
    G = None

FECHA = "2026-01-15"
DIM = 512


def unit(v):
    v = np.asarray(v, dtype=np.float64)
    return v / (np.linalg.norm(v) + 1e-12)


def cos(a, b):
    return float(unit(a) @ unit(b))


def callado(f, *args, **kw):
    """Corre f sin ensuciar la salida de la suite."""
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return f(*args, **kw)


def direcciones(n, dim=DIM, semilla=11):
    rng = np.random.default_rng(semilla)
    return [unit(rng.standard_normal(dim)) for _ in range(n)]


# ------------------------------------------------------------ piezas sueltas

@unittest.skipIf(np is None, "numpy no está instalado")
class AglomerarSeparaPersonasSinteticas(unittest.TestCase):

    def personas(self):
        rng = np.random.default_rng(3)
        dirs = direcciones(3, semilla=5)
        V, verdad = [], []
        for k, d in enumerate(dirs):
            for _ in range(12):
                V.append(unit(d + 0.015 * rng.standard_normal(DIM)))
                verdad.append(k)
        orden = rng.permutation(len(V))
        return np.stack([V[i] for i in orden]), np.array([verdad[i] for i in orden])

    def test_tres_personas_salen_en_tres_grupos(self):
        V, verdad = self.personas()
        et = G.aglomerar(np, V, G.UMBRAL_GRUPO)
        self.assertEqual(3, len(set(et.tolist())))
        for k in range(3):
            self.assertEqual(1, len(set(et[verdad == k].tolist())),
                             "una misma persona quedó partida en varios grupos")
        self.assertEqual(3, len({tuple(sorted(set(verdad[et == e].tolist()))) for e in set(et.tolist())}))

    def test_con_un_umbral_enorme_se_funden(self):
        V, _ = self.personas()
        et = G.aglomerar(np, V, 5.0)
        self.assertEqual({0}, set(et.tolist()))

    def test_vacio(self):
        self.assertEqual(0, len(G.aglomerar(np, np.zeros((0, DIM), np.float32), G.UMBRAL_GRUPO)))


@unittest.skipIf(np is None, "numpy no está instalado")
class LaHuellaCuantizadaConservaLaDireccion(unittest.TestCase):

    def test_ida_y_vuelta(self):
        rng = np.random.default_rng(21)
        for _ in range(20):
            v = rng.standard_normal(DIM).astype(np.float32)
            w = G.de_b64(np, G.b64_int8(np, v))
            self.assertEqual(DIM, w.size)
            self.assertGreater(cos(v, w), 0.999)

    def test_ida_y_vuelta_con_escala_comun(self):
        rng = np.random.default_rng(22)
        v = rng.standard_normal(32).astype(np.float32)
        w = G.de_b64(np, G.b64_int8(np, v, float(np.max(np.abs(v)))))
        self.assertGreater(cos(v, w), 0.999)


@unittest.skipIf(np is None, "numpy no está instalado")
class ElSolapeMideDosALaVez(unittest.TestCase):

    def test_sin_turnos_que_se_pisen_da_cero(self):
        turnos = [{"inicio": 0.0, "fin": 5.0}, {"inicio": 5.0, "fin": 10.0}]
        self.assertEqual(0.0, G.solape(2.0, 8.0, turnos))
        self.assertEqual(0.0, G.solape(2.0, 8.0, []))

    def test_dos_turnos_simultaneos_sobre_toda_la_linea(self):
        turnos = [{"inicio": 0.0, "fin": 10.0}, {"inicio": 1.0, "fin": 9.0}]
        self.assertAlmostEqual(1.0, G.solape(2.0, 8.0, turnos), places=6)

    def test_mitad(self):
        turnos = [{"inicio": 0.0, "fin": 10.0}, {"inicio": 5.0, "fin": 10.0}]
        self.assertAlmostEqual(0.5, G.solape(0.0, 10.0, turnos), delta=0.02)


@unittest.skipIf(np is None, "numpy no está instalado")
class PartirElTextoPorUnaPalabra(unittest.TestCase):

    PAL = [{"p": " Buenos", "i": 1.0}, {"p": " días", "i": 1.4}, {"p": " a", "i": 1.8},
           {"p": " todos.", "i": 2.0}, {"p": " Gracias", "i": 2.6}, {"p": " señora.", "i": 3.0}]

    def test_parte_por_la_palabra_k(self):
        self.assertEqual(["Buenos días a todos.", "Gracias señora."], G._partir_texto(self.PAL, 4))
        self.assertEqual(["Buenos", "días a todos. Gracias señora."], G._partir_texto(self.PAL, 1))

    def test_palabras_sin_espacio_delante(self):
        pal = [{"p": "Uno", "i": 0.0}, {"p": "dos", "i": 0.5}, {"p": "tres", "i": 1.0}]
        self.assertEqual(["Uno dos", "tres"], G._partir_texto(pal, 2))

    def test_sin_donde_partir_no_parte(self):
        self.assertIsNone(G._partir_texto(self.PAL, 0))
        self.assertIsNone(G._partir_texto(self.PAL, 6))
        self.assertIsNone(G._partir_texto(self.PAL, 99))
        self.assertIsNone(G._partir_texto(self.PAL, -1))
        self.assertIsNone(G._partir_texto(self.PAL, None))
        self.assertIsNone(G._partir_texto([], 2))
        self.assertIsNone(G._partir_texto(None, 2))


# ------------------------------------------------------------------ aplicar

def texto_de(lid):
    return "Frase sintética %s sobre un asunto inventado." % lid


def genoma_sintetico(n_a1=20, n_a2=4, clave="0123456789abcdef", vec_de=None):
    """Un genoma inventado: dos audios, tres voces, líneas de 4 s.

    `vec_de(lid, voz)` permite fijar la huella de cada línea; por defecto es la
    dirección de su voz con un poco de ruido."""
    rng = np.random.default_rng(99)
    dirs = dict(zip(["v1", "v2", "v3"], direcciones(3, semilla=41)))
    voces = [{"id": v, "etiqueta": "Voz %s" % v[1:], "vec": G.b64_int8(np, dirs[v]), "tipicas": []}
             for v in ("v1", "v2", "v3")]
    lineas = []
    for au, n in (("A1", n_a1), ("A2", n_a2)):
        for i in range(n):
            lid = "%s-%d" % (au, i)
            voz = ("v1", "v2", "v3")[i % 3]
            vec = vec_de(lid, voz) if vec_de else unit(dirs[voz] + 0.01 * rng.standard_normal(DIM))
            li = {"id": lid, "audio": au, "i": i, "ini": 5.0 * i, "fin": 5.0 * i + 4.0,
                  "texto": texto_de(lid), "vec": G.b64_int8(np, vec),
                  "adn": G.b64_int8(np, rng.standard_normal(32)), "xy": [0.0, 0.0],
                  "voz": voz, "parecido": 0.9, "margen": 0.2, "pisa": 0.0, "corta": False,
                  "dudas": []}
            lineas.append(li)
    return {
        "formato": "despacho/genoma-de-voz", "version": 1, "clave": clave,
        "titulo": "Reunión sintética de prueba", "generado": FECHA,
        "modelo": {"huella": "wespeaker-voxceleb-CAMPP.onnx", "dim": DIM, "ventana_s": 1.5,
                   "salto_s": 0.75, "umbral_grupo": 0.25},
        "calibracion": {"bandas": {"alta": 0.10, "media": 0.05}, "cambio": 0.6,
                        "precision_minima": 0.90, "revisiones_minimas": 8,
                        "fiable_s": 1.5, "pisa_max": 0.30, "corta_s": 1.0},
        "meta_claridad": 0.85,
        "audios": [{"id": "A1", "nombre": "Audio 1", "ruta": "a1.wav", "archivo": "a1.wav", "duracion": 200.0},
                   {"id": "A2", "nombre": "Audio 2", "ruta": "a2.wav", "archivo": "a2.wav", "duracion": 40.0}],
        "voces": voces, "lineas": lineas, "huecos": [], "personas_conocidas": [],
    }, dirs


def declaracion(clave="0123456789abcdef", quien="Persona Declarante Inventada", voces=None,
                lineas=None, maquina=None, resumen=None):
    d = {"formato": G.FORMATO_DECLARACION, "version": 1, "clave": clave,
         "titulo": "Reunión sintética de prueba", "declarado_por": quien,
         "exportado": FECHA + "T10:00:00", "voces": voces or {}, "lineas": lineas or {},
         "maquina": maquina or {},
         "resumen": resumen or {"claridad": {}, "acierto_alta": [0, 0], "maquina_cuenta": False}}
    if quien is None:
        del d["declarado_por"]
    return d


def dc(decision, voz=None, propuesta="v1", banda="alta", **extra):
    """Una decision como la registra la pagina. Por defecto, tomada OYENDO la
    linea y sobre una linea SORTEADA para la prueba de la maquina."""
    out = {"decision": decision, "propuesta_maquina": propuesta, "banda_maquina": banda,
           "origen": "prueba", "oida": True, "fecha": FECHA}
    if voz:
        out["voz"] = voz
    out.update(extra)
    return out


@unittest.skipIf(np is None, "numpy no está instalado")
class AplicarDePuntaAPunta(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.salida = self.tmp / "salida"
        self._hoy = mock.patch.object(G, "hoy", lambda: FECHA)
        self._hoy.start()

    def tearDown(self):
        self._hoy.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def escribir(self, nombre, obj):
        r = self.tmp / nombre
        r.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
        return r

    def aplicar(self, genoma, decl, salida=None, biblioteca=None):
        rg = self.escribir("genoma.json", genoma)
        rd = self.escribir("voces declaradas.json", decl)
        args = ["aplicar", str(rg), str(rd), "--salida", str(salida or self.salida)]
        if biblioteca:
            args += ["--biblioteca", str(biblioteca)]
        return callado(G.main, args)

    def leer(self, patron, salida=None):
        rs = sorted(glob.glob(str((salida or self.salida) / patron)))
        self.assertEqual(1, len(rs), "no hay exactamente un %s: %s" % (patron, rs))
        with io.open(rs[0], encoding="utf-8") as f:
            return f.read()

    def por_linea(self, salida=None):
        return json.loads(self.leer("voces por linea - *.json", salida))

    def renglones_de(self, md, lid):
        return [r for r in md.splitlines() if r.startswith("**[") and texto_de(lid) in r]

    # -- la declaración completa ---------------------------------------------

    def declaracion_completa(self):
        g, _ = genoma_sintetico(n_a1=8, n_a2=2)
        partida = next(l for l in g["lineas"] if l["id"] == "A1-5")
        partida["partes"] = ["Primera mitad inventada de la línea", "segunda mitad inventada de la línea"]
        partida["cambio"] = {"parecido": 0.4, "en": 27.0, "palabra": 5}
        voces = {"v1": {"nombre": "Persona Alfa", "cargo": "Cargo inventado", "como_lo_sabe": "Se presenta al inicio",
                        "fusionada_en": None},
                 "v2": {"nombre": "Persona Beta", "cargo": "", "como_lo_sabe": "La llaman por su nombre"},
                 "v3": {"fusionada_en": "v1"}}
        lineas = {"A1-0": dc("confirmada", "v1"),
                  "A1-1": dc("corregida", "v2", propuesta="v1"),
                  "A1-2": dc("no_se_distingue"),
                  "A1-3": dc("varios", voces=["v1", "v2"]),
                  "A1-4": dc("confirmada", "v3", propuesta="v3"),
                  "A1-5": dc("confirmada", partes=[{"voz": "v1"}, {"voz": "v2"}])}
        return g, declaracion(voces=voces, lineas=lineas)

    def test_produce_los_tres_archivos(self):
        g, d = self.declaracion_completa()
        self.assertEqual(0, self.aplicar(g, d))
        nombres = sorted(os.listdir(self.salida))
        self.assertEqual(sorted([
            "Transcripcion con voces - Audio 1 - %s.md" % FECHA,
            "Transcripcion con voces - Audio 2 - %s.md" % FECHA,
            "Declaracion de voces - Reunión sintética de prueba - %s.md" % FECHA,
            "voces por linea - Reunión sintética de prueba - %s.json" % FECHA]), nombres)

    def test_las_tres_marcas(self):
        g, d = self.declaracion_completa()
        self.aplicar(g, d)
        md = self.leer("Transcripcion con voces - Audio 1 - *.md")
        r0, = self.renglones_de(md, "A1-0")
        self.assertIn("✔ Persona Alfa · Cargo inventado", r0)
        r1, = self.renglones_de(md, "A1-1")
        self.assertIn("✔ Persona Beta", r1)
        r2, = self.renglones_de(md, "A1-2")
        self.assertIn("? No se distingue", r2)
        self.assertNotIn("✔", r2)
        r3, = self.renglones_de(md, "A1-3")
        self.assertIn("✔ Varios a la vez", r3)
        r7, = self.renglones_de(md, "A1-7")
        self.assertIn("≈", r7)
        self.assertIn("nadie lo ha oído", r7)
        self.assertNotIn("✔", r7)

    def test_una_voz_nombrada_en_una_linea_solo_propuesta_sigue_siendo_propuesta(self):
        g, d = self.declaracion_completa()
        self.aplicar(g, d)
        md = self.leer("Transcripcion con voces - Audio 1 - *.md")
        r6, = self.renglones_de(md, "A1-6")
        self.assertEqual("v1", next(l for l in g["lineas"] if l["id"] == "A1-6")["voz"])
        self.assertIn("≈ Persona Alfa", r6)
        self.assertIn("nadie lo ha oído", r6)
        self.assertNotIn("✔", r6)
        reg = next(x for x in self.por_linea()["lineas"] if x["id"] == "A1-6")
        self.assertEqual("propuesta", reg["decision"])

    def test_voz_fusionada_sale_con_el_nombre_de_la_destino(self):
        g, d = self.declaracion_completa()
        self.aplicar(g, d)
        md = self.leer("Transcripcion con voces - Audio 1 - *.md")
        r4, = self.renglones_de(md, "A1-4")
        self.assertIn("✔ Persona Alfa", r4)
        self.assertNotIn("Voz 3", r4)
        reg = next(x for x in self.por_linea()["lineas"] if x["id"] == "A1-4")
        self.assertEqual("v1", reg["voz"])
        decl = self.leer("Declaracion de voces - *.md")
        self.assertIn("Voz 3 se declaró la misma persona que Persona Alfa", decl)

    def test_linea_dividida_sale_en_dos_renglones(self):
        g, d = self.declaracion_completa()
        self.aplicar(g, d)
        md = self.leer("Transcripcion con voces - Audio 1 - *.md")
        a = [r for r in md.splitlines() if "Primera mitad inventada" in r]
        b = [r for r in md.splitlines() if "segunda mitad inventada" in r]
        self.assertEqual(1, len(a))
        self.assertEqual(1, len(b))
        self.assertIn("✔ Persona Alfa", a[0])
        self.assertIn("✔ Persona Beta", b[0])
        self.assertNotIn("segunda mitad", a[0])
        reg = next(x for x in self.por_linea()["lineas"] if x["id"] == "A1-5")
        self.assertEqual("dividida", reg["decision"])
        self.assertEqual(["v1", "v2"], [p["voz"] for p in reg["partes"]])

    def test_la_claridad_de_la_declaracion_completa(self):
        g, d = self.declaracion_completa()
        self.aplicar(g, d)
        # A1: 8 líneas; claras las 0,1,3,4,5 (A1-2 «no se distingue» no cuenta,
        # y 6 y 7 son propuestas de una máquina que nadie puso a prueba).
        self.assertAlmostEqual(5 / 8.0, self.por_linea()["claridad"]["A1"], places=4)
        self.assertEqual(0.0, self.por_linea()["claridad"]["A2"])

    # -- se detiene ---------------------------------------------------------

    def test_sin_declarado_por_se_detiene(self):
        g, _ = genoma_sintetico()
        for quien in (None, "", "   "):
            with self.assertRaises(SystemExit):
                self.aplicar(g, declaracion(quien=quien, lineas={"A1-0": dc("confirmada", "v1")}))
            self.assertFalse(self.salida.exists() and os.listdir(self.salida))

    def test_clave_distinta_se_detiene(self):
        g, _ = genoma_sintetico(clave="aaaaaaaaaaaaaaaa")
        with self.assertRaises(SystemExit):
            self.aplicar(g, declaracion(clave="bbbbbbbbbbbbbbbb"))
        self.assertFalse(self.salida.exists() and os.listdir(self.salida))

    def test_nunca_sobrescribe(self):
        g, d = self.declaracion_completa()
        self.aplicar(g, d)
        antes = {n: (self.salida / n).read_bytes() for n in os.listdir(self.salida)}
        with self.assertRaises(SystemExit):
            self.aplicar(g, d)
        despues = {n: (self.salida / n).read_bytes() for n in os.listdir(self.salida)}
        self.assertEqual(antes, despues)

    def test_una_fusion_circular_no_cuelga_el_programa(self):
        """v1 -> v2 -> v1, o v1 -> v1: una declaración incoherente se detiene
        antes de escribir nada, no gira para siempre. Va en otro proceso para
        que un cuelgue sea un fallo y no una suite detenida."""
        g, _ = genoma_sintetico(n_a1=4, n_a2=1)
        rg = self.escribir("genoma.json", g)
        for voces in ({"v1": {"nombre": "Persona Alfa", "fusionada_en": "v2"}, "v2": {"fusionada_en": "v1"}},
                      {"v1": {"nombre": "Persona Alfa", "fusionada_en": "v1"}}):
            d = declaracion(voces=voces, lineas={"A1-0": dc("confirmada", "v1")})
            rd = self.escribir("voces declaradas.json", d)
            try:
                r = subprocess.run([sys.executable, str(PROGRAMA), "aplicar", str(rg), str(rd),
                                    "--salida", str(self.salida)],
                                   capture_output=True, text=True, encoding="utf-8", errors="replace",
                                   timeout=60, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
            except subprocess.TimeoutExpired:
                self.fail("una fusión circular deja al programa girando para siempre")
            self.assertNotEqual(0, r.returncode)
            self.assertIn("en círculo", r.stderr)
            self.assertFalse(self.salida.exists() and os.listdir(self.salida))

    # -- el resumen no se cree ------------------------------------------------

    def exportacion_con_revisiones(self, revisadas, aciertos):
        """A1 tiene 20 líneas de 4 s. Las primeras `revisadas` las decidió ella
        cuando la máquina las daba en banda alta; de ellas `aciertos` confirmadas.
        De las restantes, las líneas hasta la 15 son propuestas altas y de la 16
        en adelante propuestas medias. El resumen MIENTE: dice que la máquina
        cuenta y que la claridad es del 99 %."""
        g, _ = genoma_sintetico(n_a1=20, n_a2=2)
        lineas, maquina = {}, {}
        for i in range(20):
            lid = "A1-%d" % i
            if i < revisadas:
                lineas[lid] = (dc("confirmada", "v1", propuesta="v1") if i < aciertos
                               else dc("corregida", "v2", propuesta="v1"))
            else:
                maquina[lid] = {"voz": "v1", "banda": "alta" if i < 16 else "media",
                                "parecido": 0.9, "margen": 0.2}
        return g, declaracion(voces={"v1": {"nombre": "Persona Alfa"}}, lineas=lineas, maquina=maquina,
                              resumen={"claridad": {"A1": 0.99}, "acierto_alta": [30, 30],
                                       "maquina_cuenta": True})

    def test_siete_revisiones_no_bastan_aunque_el_resumen_diga_que_si(self):
        g, d = self.exportacion_con_revisiones(7, 7)
        self.aplicar(g, d)
        self.assertAlmostEqual(7 / 20.0, self.por_linea()["claridad"]["A1"], places=4)
        self.assertIn("**No basta**", self.leer("Declaracion de voces - *.md"))

    def test_ocho_revisiones_y_ocho_aciertos_si(self):
        g, d = self.exportacion_con_revisiones(8, 8)
        self.aplicar(g, d)
        # 8 declaradas + 8 propuestas altas (8..15); las medias no suman.
        self.assertAlmostEqual(16 / 20.0, self.por_linea()["claridad"]["A1"], places=4)
        self.assertNotIn("**No basta**", self.leer("Declaracion de voces - *.md"))

    def test_diez_revisiones_y_ocho_aciertos_no(self):
        g, d = self.exportacion_con_revisiones(10, 8)
        self.aplicar(g, d)
        # 80 % < 90 %: solo lo declarado (10 líneas).
        self.assertAlmostEqual(10 / 20.0, self.por_linea()["claridad"]["A1"], places=4)
        self.assertIn("acertó 8 de 10 líneas sorteadas y oídas (80 %)", self.leer("Declaracion de voces - *.md"))

    # -- la biblioteca ---------------------------------------------------------

    def caso_biblioteca(self):
        """v1 (Persona Alfa): 4 líneas declaradas cerca de D1, y líneas NO
        declaradas, «varios» y divididas con huella cerca de D3, que no deben
        entrar. v2 (Persona Beta): solo 2 declaradas. v3: 3 declaradas sin nombre."""
        rng = np.random.default_rng(5)
        D1, D2, D3 = direcciones(3, semilla=77)
        declaradas_v1 = {"A1-0", "A1-3", "A1-6", "A1-9"}

        def vec_de(lid, voz):
            if voz == "v1" and lid not in declaradas_v1:
                return unit(D3 + 0.01 * rng.standard_normal(DIM))
            return unit({"v1": D1, "v2": D2, "v3": D3}[voz] + 0.01 * rng.standard_normal(DIM))

        g, _ = genoma_sintetico(n_a1=15, n_a2=3, vec_de=vec_de)
        g["lineas"][12]["partes"] = ["una parte inventada", "otra parte inventada"]
        lineas = {lid: dc("confirmada", "v1") for lid in declaradas_v1}
        lineas.update({"A1-1": dc("confirmada", "v2"), "A1-4": dc("corregida", "v2"),
                       "A1-2": dc("confirmada", "v3"), "A1-5": dc("confirmada", "v3"),
                       "A1-8": dc("confirmada", "v3"),
                       "A1-10": dc("varios", voces=["v1", "v2"]),
                       "A1-12": dc("confirmada", partes=[{"voz": "v1"}, {"voz": "v1"}])})
        voces = {"v1": {"nombre": "Persona Alfa", "cargo": "Cargo inventado"},
                 "v2": {"nombre": "Persona Beta"}}
        return g, declaracion(voces=voces, lineas=lineas), D1, D3

    def test_la_biblioteca_solo_con_lo_declarado_y_nombrado(self):
        g, d, D1, D3 = self.caso_biblioteca()
        bib = self.tmp / "bib" / "Biblioteca de voces.json"
        bib.parent.mkdir()
        self.aplicar(g, d, biblioteca=bib)
        lib = json.loads(bib.read_text(encoding="utf-8"))
        self.assertEqual("despacho/biblioteca-de-voces", lib["formato"])
        self.assertEqual(["Persona Alfa"], [v["nombre"] for v in lib["voces"]],
                         "Persona Beta tiene 2 líneas (mínimo 3) y la Voz 3 no tiene nombre")
        alfa = lib["voces"][0]
        self.assertEqual(4, alfa["lineas"])
        self.assertEqual("Persona Declarante Inventada", alfa["declarado_por"])
        v = G.de_b64(np, alfa["vec"])
        self.assertGreater(cos(v, D1), 0.95)
        self.assertLess(cos(v, D3), 0.3, "entraron propuestas, «varios» o divididas")
        self.assertFalse((bib.parent / "_anteriores").exists(),
                         "sin biblioteca previa no hay nada que guardar")

    def test_la_misma_declaracion_no_cuenta_dos_veces(self):
        """Re-aplicar es un uso normal: aplicar nunca pisa, así que se vuelve a
        correr con otra --salida. Antes eso sumaba OTRA VEZ las mismas líneas y
        la persona pesaba el doble en la biblioteca."""
        g, d, D1, _ = self.caso_biblioteca()
        bib = self.tmp / "bib" / "Biblioteca de voces.json"
        bib.parent.mkdir()
        self.aplicar(g, d, salida=self.tmp / "s1", biblioteca=bib)
        self.aplicar(g, d, salida=self.tmp / "s2", biblioteca=bib)
        lib = json.loads(bib.read_text(encoding="utf-8"))
        self.assertEqual(4, lib["voces"][0]["lineas"], "la misma declaración se contó dos veces")
        self.assertEqual(1, len(lib["voces"][0]["historial"]))

    def test_otra_reunion_si_suma_y_ninguna_copia_se_pisa(self):
        g, d, D1, _ = self.caso_biblioteca()
        bib = self.tmp / "bib" / "Biblioteca de voces.json"
        bib.parent.mkdir()
        self.aplicar(g, d, salida=self.tmp / "s1", biblioteca=bib)
        v1 = bib.read_bytes()
        g2, d2 = json.loads(json.dumps(g)), json.loads(json.dumps(d))
        g2["clave"] = d2["clave"] = "fedcba9876543210"
        self.aplicar(g2, d2, salida=self.tmp / "s2", biblioteca=bib)
        v2 = bib.read_bytes()
        g3, d3 = json.loads(json.dumps(g)), json.loads(json.dumps(d))
        g3["clave"] = d3["clave"] = "aaaabbbbccccdddd"
        # Las tres en el mismo segundo: el nombre de la copia lleva la hora al
        # segundo, asi que sin sufijo la segunda copia pisaria a la primera.
        with mock.patch.object(G.datetime, "datetime") as dt:
            dt.now.return_value.strftime.return_value = "2026-01-15 100000"
            self.aplicar(g3, d3, salida=self.tmp / "s3", biblioteca=bib)
        anteriores = sorted((bib.parent / "_anteriores").iterdir())
        self.assertEqual(2, len(anteriores), "una copia anterior pisó a otra")
        self.assertEqual({v1, v2}, {x.read_bytes() for x in anteriores})
        lib = json.loads(bib.read_text(encoding="utf-8"))
        self.assertEqual(12, lib["voces"][0]["lineas"])
        self.assertEqual(3, len(lib["voces"][0]["historial"]))

    def test_la_biblioteca_no_toma_lineas_que_se_pisan_ni_cortas(self):
        g, d, D1, D3 = self.caso_biblioteca()
        # Dos lineas mas de Persona Alfa, declaradas, pero una se pisa y otra es
        # corta, y las dos con la huella de OTRA direccion: si entran, se nota.
        for k, (campo, valor) in zip((13, 14), (("pisa", 0.6), ("corta", True))):
            li = g["lineas"][k]
            li[campo] = valor
            li["vec"] = G.b64_int8(np, D3)
            d["lineas"][li["id"]] = dc("confirmada", "v1")
        bib = self.tmp / "bib" / "Biblioteca de voces.json"
        bib.parent.mkdir()
        self.aplicar(g, d, biblioteca=bib)
        alfa = json.loads(bib.read_text(encoding="utf-8"))["voces"][0]
        self.assertEqual(4, alfa["lineas"], "entró habla simultánea o casi nada de voz")


@unittest.skipIf(np is None, "numpy no está instalado")
class LoQueLaRevisionEncontro(unittest.TestCase):
    """Defectos y huecos que encontró la revisión del 2026-09-23."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.salida = self.tmp / "salida"
        self._hoy = mock.patch.object(G, "hoy", lambda: FECHA)
        self._hoy.start()

    def tearDown(self):
        self._hoy.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def aplicar(self, genoma, decl):
        rg = self.tmp / "genoma.json"
        rg.write_text(json.dumps(genoma, ensure_ascii=False), encoding="utf-8")
        rd = self.tmp / "decl.json"
        rd.write_text(json.dumps(decl, ensure_ascii=False), encoding="utf-8")
        return callado(G.main, ["aplicar", str(rg), str(rd), "--salida", str(self.salida)])

    def por_linea(self):
        r = glob.glob(str(self.salida / "voces por linea - *.json"))
        with io.open(r[0], encoding="utf-8") as f:
            return json.loads(f.read())

    def declaracion_md(self):
        r = glob.glob(str(self.salida / "Declaracion de voces - *.md"))
        with io.open(r[0], encoding="utf-8") as f:
            return f.read()

    def test_la_cuantizacion_recorta_en_vez_de_desbordar(self):
        """El ADN usa como escala el percentil 99: el 1 % la supera. Sin recorte,
        127 * 3 se sale de int8, da la vuelta y el genoma queda corrupto."""
        v = np.array([3.0, -3.0, 0.5, -0.5] + [0.1] * 28, dtype=np.float32)
        q = np.frombuffer(__import__("base64").b64decode(G.b64_int8(np, v, 1.0)), dtype=np.int8)
        self.assertEqual(127, int(q[0]))
        self.assertEqual(-127, int(q[1]))
        self.assertGreater(cos(v[2:], q[2:].astype(np.float64)), 0.99)

    def test_el_enlace_es_promedio_y_no_simple(self):
        """Tres grupos en cadena: A parecido a B, B parecido a C, A nada a C.
        El enlace simple los funde todos; el promedio deja A-B aparte de C."""
        d1, d2 = direcciones(2, semilla=8)
        mid = unit(d1 + d2)
        rng = np.random.default_rng(4)
        V = np.stack([unit(c + 0.01 * rng.standard_normal(DIM)) for c in (d1, mid, d2) for _ in range(5)])
        et = G.aglomerar(np, V, 0.35)
        self.assertEqual(2, len(set(et.tolist())), "el enlace no es promedio")

    def test_si_una_salida_existe_no_se_escribe_nada(self):
        g, _ = genoma_sintetico(n_a1=6, n_a2=2)
        d = declaracion(lineas={"A1-0": dc("confirmada", "v1")})
        self.salida.mkdir()
        (self.salida / ("Declaracion de voces - %s - %s.md" % (g["titulo"], FECHA))).write_text("x", encoding="utf-8")
        with self.assertRaises(SystemExit):
            self.aplicar(g, d)
        self.assertEqual(["Declaracion de voces - %s - %s.md" % (g["titulo"], FECHA)],
                         sorted(os.listdir(self.salida)), "escribió a medias antes de detenerse")

    def test_conocer_las_voces_no_cuenta_en_el_acierto(self):
        """Las lineas del paso 1 se eligen por ser las mas tipicas: la maquina
        casi seguro acierta ahi. Contarlas inflaria el acierto."""
        g, _ = genoma_sintetico(n_a1=20, n_a2=2)
        lineas = {"A1-%d" % i: dc("confirmada", "v1", origen="conocer") for i in range(8)}
        maquina = {"A1-%d" % i: {"voz": "v1", "banda": "alta"} for i in range(8, 20)}
        self.aplicar(g, declaracion(lineas=lineas, maquina=maquina))
        self.assertAlmostEqual(8 / 20.0, self.por_linea()["claridad"]["A1"], places=4)

    def test_una_linea_corta_o_que_se_pisa_nunca_es_alta(self):
        g, _ = genoma_sintetico(n_a1=20, n_a2=2)
        g["lineas"][10]["corta"] = True
        g["lineas"][11]["pisa"] = 0.5
        lineas = {"A1-%d" % i: dc("confirmada", "v1") for i in range(8)}
        maquina = {"A1-%d" % i: {"voz": "v1", "banda": "alta"} for i in range(8, 20)}
        self.aplicar(g, declaracion(lineas=lineas, maquina=maquina))
        pl = {x["id"]: x for x in self.por_linea()["lineas"]}
        self.assertEqual("baja", pl["A1-10"]["banda"])
        self.assertEqual("baja", pl["A1-11"]["banda"])
        self.assertAlmostEqual(18 / 20.0, self.por_linea()["claridad"]["A1"], places=4)

    def test_lo_decidido_sin_oir_se_dice(self):
        g, _ = genoma_sintetico(n_a1=6, n_a2=2)
        d = declaracion(lineas={"A1-0": dc("confirmada", "v1", oida=False),
                                "A1-1": dc("confirmada", "v2", oida=True)})
        self.aplicar(g, d)
        self.assertIn("1 de 2 decisiones se tomaron sin oír", self.declaracion_md())

    def test_para_atribuir_hace_falta_nombre_cargo_y_como_lo_sabe(self):
        g, _ = genoma_sintetico(n_a1=6, n_a2=2)
        d = declaracion(voces={"v1": {"nombre": "Persona Alfa"},
                               "v2": {"nombre": "Persona Beta", "cargo": "Cargo inventado",
                                      "como_lo_sabe": "Estuve en la reunión"}},
                        lineas={"A1-0": dc("confirmada", "v1"), "A1-1": dc("confirmada", "v2")})
        self.aplicar(g, d)
        md = self.declaracion_md()
        self.assertIn("Persona Alfa: falta cargo o entidad, cómo lo sabe", md)
        self.assertNotIn("Persona Beta: falta", md)

    def test_el_formato_de_nombrar_voces_no_se_confunde_con_este(self):
        g, _ = genoma_sintetico(n_a1=6, n_a2=2)
        d = declaracion(lineas={"A1-0": dc("confirmada", "v1")})
        d["formato"] = "despacho/voces-declaradas"
        with self.assertRaises(SystemExit):
            self.aplicar(g, d)

    def test_personas_de_nombrar_voces_y_de_la_pagina(self):
        a = self.tmp / "nombrar.json"
        a.write_text(json.dumps({"formato": "despacho/voces-declaradas", "declarado_por": "Alguien",
                                 "fecha": "2026-01-01", "voces": {"1": {"quien": "Persona Gamma", "cargo": "C"}}}),
                     encoding="utf-8")
        b = self.tmp / "pagina.json"
        b.write_text(json.dumps({"formato": G.FORMATO_DECLARACION, "declarado_por": "Otra",
                                 "exportado": "2026-01-02T10:00:00",
                                 "voces": {"v1": {"nombre": "Persona Delta"},
                                           "v2": {"nombre": "Persona Epsilon", "fusionada_en": "v1"}}}),
                     encoding="utf-8")
        out = G._personas([str(a), str(b)])
        self.assertEqual(["Persona Gamma", "Persona Delta"], [x["nombre"] for x in out])
        self.assertIn("2026-01-02", out[1]["fuente"])


@unittest.skipIf(np is None, "numpy no está instalado")
class ElRescateSoloEntraSiElloLoAcepta(unittest.TestCase):
    """Tramos que la transcripción no tenía, oídos otra vez. Nada de eso
    existe para la salida si ella no dice, oyéndolo, que se dijo."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.salida = self.tmp / "salida"
        self._hoy = mock.patch.object(G, "hoy", lambda: FECHA)
        self._hoy.start()

    def tearDown(self):
        self._hoy.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def caso(self):
        g, dirs = genoma_sintetico(n_a1=6, n_a2=2)
        g["rescates"] = [
            {"id": "A1-r%d" % k, "audio": "A1", "ini": 5.0 * k + 4.2, "fin": 5.0 * k + 4.8,
             "texto": "Tramo rescatado inventado %d." % k, "rescate": True,
             "lecturas": [{"fuente": "Lectura del canal derecho", "texto": "Tramo rescatado inventado %d." % k}],
             "acuerdo": 0.8, "oyen": 2, "invencion": False, "bucle": False,
             "vec": G.b64_int8(np, dirs["v2"]), "adn": G.b64_int8(np, np.ones(32)), "xy": [0, 0],
             "voz": "v2", "parecido": 0.9, "margen": 0.2, "pisa": 0.0, "corta": True, "dudas": []}
            for k in range(3)]
        lineas = {
            "A1-r0": dc("corregida", "v1", propuesta="v2", rescate=True, se_dijo=True,
                        texto="Lo que ella oyó de verdad."),
            "A1-r1": dc("no_se_dijo", propuesta="v2", rescate=True, se_dijo=False),
        }
        return g, declaracion(voces={"v1": {"nombre": "Persona Alfa"}}, lineas=lineas)

    def aplicar(self, g, d):
        rg = self.tmp / "g.json"
        rg.write_text(json.dumps(g, ensure_ascii=False), encoding="utf-8")
        rd = self.tmp / "d.json"
        rd.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        callado(G.main, ["aplicar", str(rg), str(rd), "--salida", str(self.salida)])

    def leer(self, patron):
        r = glob.glob(str(self.salida / patron))
        with io.open(r[0], encoding="utf-8") as f:
            return f.read()

    def test_solo_el_aceptado_y_con_su_texto(self):
        g, d = self.caso()
        self.aplicar(g, d)
        md = self.leer("Transcripcion con voces - Audio 1 - *.md")
        self.assertIn("Lo que ella oyó de verdad.", md)
        self.assertIn("rescatada: no estaba en la transcripción", md)
        self.assertIn("texto corregido por ella", md)
        self.assertNotIn("Tramo rescatado inventado 0.", md, "salió el texto de la máquina en vez del de ella")
        self.assertNotIn("Tramo rescatado inventado 1.", md, "entró un tramo que ella dijo que no se dijo")
        self.assertNotIn("Tramo rescatado inventado 2.", md, "entró un tramo que nadie oyó")

    def test_el_aceptado_va_en_su_minuto(self):
        g, d = self.caso()
        self.aplicar(g, d)
        md = self.leer("Transcripcion con voces - Audio 1 - *.md")
        self.assertLess(md.index(texto_de("A1-0")), md.index("Lo que ella oyó de verdad."))
        self.assertLess(md.index("Lo que ella oyó de verdad."), md.index(texto_de("A1-1")))

    def test_el_rescate_no_toca_la_claridad_ni_el_acierto(self):
        g, d = self.caso()
        self.aplicar(g, d)
        with io.open(glob.glob(str(self.salida / "voces por linea - *.json"))[0], encoding="utf-8") as f:
            pl = json.load(f)
        self.assertEqual(0.0, pl["claridad"]["A1"], "un rescate subió la claridad de las líneas publicadas")
        self.assertIn("1 aceptados", self.leer("Declaracion de voces - *.md"))
        self.assertIn("sin medir", self.leer("Declaracion de voces - *.md"))


@unittest.skipIf(np is None, "numpy no está instalado")
class LoDecididoSinOirYLaPruebaDeLaMaquina(unittest.TestCase):
    """Revisión adversaria del 2026-09-23: aplicar debe contar IGUAL que la
    página (genoma.js), y ninguno de los dos puede aprobar a la máquina con
    decisiones sin oír o elegidas a mano."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.salida = self.tmp / "salida"
        self._hoy = mock.patch.object(G, "hoy", lambda: FECHA)
        self._hoy.start()

    def tearDown(self):
        self._hoy.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def aplicar(self, g, d, biblioteca=None):
        rg = self.tmp / "g.json"
        rg.write_text(json.dumps(g, ensure_ascii=False), encoding="utf-8")
        rd = self.tmp / "d.json"
        rd.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        args = ["aplicar", str(rg), str(rd), "--salida", str(self.salida)]
        if biblioteca:
            args += ["--biblioteca", str(biblioteca)]
        callado(G.main, args)

    def leer(self, patron):
        with io.open(glob.glob(str(self.salida / patron))[0], encoding="utf-8") as f:
            return f.read()

    def claridad(self):
        return json.loads(self.leer("voces por linea - *.json"))["claridad"]["A1"]

    def exportacion(self, n, **extra):
        g, _ = genoma_sintetico(n_a1=20, n_a2=2)
        lineas = {"A1-%d" % i: dc("confirmada", "v1", **extra) for i in range(n)}
        maquina = {"A1-%d" % i: {"voz": "v1", "banda": "alta"} for i in range(20)}
        return g, declaracion(voces={"v1": {"nombre": "Persona Alfa"}}, lineas=lineas, maquina=maquina)

    def test_ocho_enter_sin_oir_no_aprueban_a_la_maquina(self):
        g, d = self.exportacion(10, oida=False)
        self.aplicar(g, d)
        self.assertEqual(0.0, self.claridad(), "lo decidido sin oír contó, o aprobó a la máquina")
        md = self.leer("Transcripcion con voces - Audio 1 - *.md")
        self.assertIn("_(sin oír)_", md)
        self.assertIn("10 de 10 decisiones se tomaron sin oír", self.leer("Declaracion de voces - *.md"))

    def test_las_elegidas_a_mano_no_son_la_prueba(self):
        g, d = self.exportacion(10, origen="lista")
        self.aplicar(g, d)
        self.assertAlmostEqual(10 / 20.0, self.claridad(), places=4,
                               msg="líneas elegidas a mano aprobaron a la máquina")

    def test_varios_con_una_voz_no_aclara_y_la_maquina_no_lo_rellena(self):
        g, _ = genoma_sintetico(n_a1=20, n_a2=2)
        lineas = {"A1-%d" % i: dc("confirmada", "v1") for i in range(10)}
        # Fuera de la prueba: si fueran lineas sorteadas, «varios» o «no se
        # distingue» contarian (con razon) como fallos de la maquina.
        lineas["A1-10"] = dc("varios", voces=["v2"], origen="aclarar")
        lineas["A1-11"] = dc("varios", voces=["v1", "v2"], origen="aclarar")
        lineas["A1-12"] = dc("no_se_distingue", origen="aclarar")
        maquina = {"A1-%d" % i: {"voz": "v1", "banda": "alta"} for i in range(20)}
        self.aplicar(g, declaracion(lineas=lineas, maquina=maquina))
        # 10 + la de dos voces = 11 de ella; la maquina aprobada suma 13..19 = 7;
        # «varios» de una voz y «no se distingue» no suman por ningún lado.
        self.assertAlmostEqual(18 / 20.0, self.claridad(), places=4)
        md = self.leer("Transcripcion con voces - Audio 1 - *.md")
        self.assertIn("? Varios a la vez, sin distinguir quiénes", md)

    def test_la_biblioteca_no_toma_lo_decidido_sin_oir(self):
        g, dirs = genoma_sintetico(n_a1=12, n_a2=2)
        lineas = {"A1-%d" % i: dc("confirmada", "v1") for i in (0, 3, 6)}
        lineas["A1-9"] = dc("confirmada", "v1", oida=False)
        bib = self.tmp / "b" / "Biblioteca de voces.json"
        bib.parent.mkdir()
        self.aplicar(g, declaracion(voces={"v1": {"nombre": "Persona Alfa"}}, lineas=lineas), biblioteca=bib)
        self.assertEqual(3, json.loads(bib.read_text(encoding="utf-8"))["voces"][0]["lineas"])

    def test_la_segunda_parte_va_en_su_minuto(self):
        g, _ = genoma_sintetico(n_a1=6, n_a2=2)
        li = g["lineas"][3]
        li["partes"] = ["primera parte inventada", "segunda parte inventada"]
        li["cambio"] = {"en": li["ini"] + 2.0, "palabra": 3, "parecido": 0.4, "vec_a": li["vec"], "vec_b": li["vec"]}
        d = declaracion(lineas={"A1-3": dc("corregida", partes=[{"voz": "v1"}, {"voz": "v2"}])})
        self.aplicar(g, d)
        md = self.leer("Transcripcion con voces - Audio 1 - *.md")
        self.assertIn("[%s] ✔ Voz 2 (sin nombre)** segunda parte" % G.hms(li["ini"] + 2.0), md)

    def test_la_maquina_decia_lo_que_proponia_al_decidir(self):
        g, _ = genoma_sintetico(n_a1=6, n_a2=2)
        d = declaracion(voces={"v3": {"nombre": "Persona Gamma"}},
                        lineas={"A1-0": dc("corregida", "v2", propuesta="v3")})
        self.aplicar(g, d)
        self.assertIn("| Persona Gamma | Voz 2 (sin nombre) |", self.leer("Declaracion de voces - *.md"))

    def test_los_huecos_se_dicen_en_la_transcripcion(self):
        g, _ = genoma_sintetico(n_a1=6, n_a2=2)
        g["huecos"] = [{"audio": "A1", "ini": 30.5, "fin": 42.0, "otras": []}]
        self.aplicar(g, declaracion())
        self.assertIn("sin transcribir", self.leer("Transcripcion con voces - Audio 1 - *.md"))

    def test_si_la_pagina_decia_otra_claridad_se_avisa(self):
        g, d = self.exportacion(4)
        d["resumen"] = {"claridad": {"A1": 0.99}}
        self.aplicar(g, d)
        self.assertIn("no coincide con la que mostraba la página", self.leer("Declaracion de voces - *.md"))


# ------------------------------------------------------ preparar, de humo

def _hay_sherpa():
    if np is None:
        return "numpy no está instalado"
    for mod in ("sherpa_onnx", "av"):
        try:
            __import__(mod)
        except ImportError:
            return "falta la biblioteca %s" % mod
    if not os.path.isfile(G.MODELO):
        return "falta el modelo %s" % G.MODELO
    return None


def escribir_wav(ruta, x, sr=16000):
    q = np.clip(np.round(x * 32767), -32768, 32767).astype("<i2")
    with wave.open(str(ruta), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(q.tobytes())


class PrepararDeHumo(unittest.TestCase):
    """Audio SINTÉTICO: tres «voces» hechas de tonos armónicos y ruido."""

    SR = 16000

    def setUp(self):
        motivo = _hay_sherpa()
        if motivo:
            self.skipTest(motivo)
        self.tmp = Path(tempfile.mkdtemp())
        self._hoy = mock.patch.object(G, "hoy", lambda: FECHA)
        self._hoy.start()
        plantilla = self.tmp / "voces.html"
        plantilla.write_text('<!doctype html><html><head><title>{{TITULO}}</title></head><body>'
                             '<script id="datos" type="application/json">{{DATOS}}</script>'
                             '</body></html>', encoding="utf-8")
        self._pl = mock.patch.object(G, "PLANTILLA", str(plantilla))
        self._pl.start()

    def tearDown(self):
        self._pl.stop()
        self._hoy.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def voz(self, tipo, dur, rng):
        t = np.arange(int(dur * self.SR)) / float(self.SR)
        if tipo == "grave":
            f0 = 120 + 8 * np.sin(2 * math.pi * 3 * t)
            fase = 2 * math.pi * np.cumsum(f0) / self.SR
            x = sum(np.sin(k * fase) / k for k in range(1, 12))
        elif tipo == "aguda":
            f0 = 230 + 15 * np.sin(2 * math.pi * 5 * t)
            fase = 2 * math.pi * np.cumsum(f0) / self.SR
            x = sum(np.sin(k * fase) / (k * k) for k in range(1, 8))
        else:
            x = np.convolve(rng.standard_normal(t.size), np.ones(6) / 6, mode="same")
        x = x / (np.max(np.abs(x)) + 1e-9) * 0.5
        x = x * (0.6 + 0.4 * np.abs(np.sin(2 * math.pi * 2 * t)))
        return x + 0.01 * rng.standard_normal(t.size)

    def material(self):
        rng = np.random.default_rng(8)
        tipos = ["grave", "aguda", "ruido", "grave", "aguda", "grave", "ruido", "aguda"]
        durs = [4.0, 3.5, 4.0, 3.0, 4.5, 2.0, 3.5, 4.0]
        x, segs, t = [], [], 0.2
        x.append(0.01 * rng.standard_normal(int(0.2 * self.SR)))
        for i, (tp, du) in enumerate(zip(tipos, durs)):
            x.append(self.voz(tp, du, rng))
            texto = "Línea inventada número %d del ensayo." % i
            seg = {"i": i, "inicio": round(t, 3), "fin": round(t + du, 3), "texto": texto}
            if i == 2:
                seg["texto"] = "Texto con </script><b>etiquetas</b> inventadas."
            if i == 4:
                seg["palabras"] = [{"p": " palabra%d" % k, "i": round(t + 0.5 * k, 3)} for k in range(8)]
            segs.append(seg)
            t += du
            x.append(0.01 * rng.standard_normal(int(0.5 * self.SR)))
            t += 0.5
        x.append(0.01 * rng.standard_normal(int(6.0 * self.SR)))
        audio = self.tmp / "grabacion sintetica.wav"
        escribir_wav(audio, np.concatenate(x))
        turnos = [{"inicio": s["inicio"], "fin": s["fin"], "voz": "SPEAKER_00"} for s in segs]
        turnos.append({"inicio": segs[6]["inicio"], "fin": segs[6]["fin"], "voz": "SPEAKER_01"})
        datos = {"publicada": {"etiqueta": "mono/principal", "segmentos": segs},
                 "voces": {"turnos": turnos},
                 "marcas": {"1": ["las lecturas automáticas no coinciden", "voz dudosa"]},
                 "ventanas": []}
        rd = self.tmp / "datos.json"
        rd.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
        return rd, audio, segs

    def test_preparar_escribe_la_pagina_y_el_genoma_y_no_sobrescribe(self):
        rd, audio, segs = self.material()
        salida = self.tmp / "salida"
        titulo = "Reunión <sintética> de prueba"
        args = ["preparar", "--par", "A1", str(rd), str(audio), "--titulo", titulo, "--salida", str(salida)]
        self.assertEqual(0, callado(G.main, args))

        base = "Reunión sintética de prueba - %s" % FECHA
        pagina = (salida / ("Voces - %s.html" % base)).read_text(encoding="utf-8")
        genoma = json.loads((salida / ("genoma - %s.json" % base)).read_text(encoding="utf-8"))

        self.assertIn("<title>Reunión &lt;sintética&gt; de prueba</title>", pagina)
        ab = '<script id="datos" type="application/json">'
        incrustado = pagina[pagina.index(ab) + len(ab):pagina.rindex("</script>")]
        self.assertNotIn("</", incrustado, "un «</» crudo cierra el <script> antes de tiempo")
        datos = json.loads(incrustado)
        self.assertEqual(genoma, datos)

        self.assertEqual("despacho/genoma-de-voz", datos["formato"])
        self.assertEqual(16, len(datos["clave"]))
        self.assertEqual(len(segs), len(datos["lineas"]))
        self.assertIn("Texto con </script><b>etiquetas</b> inventadas.",
                      [l["texto"] for l in datos["lineas"]])
        ids_voces = {v["id"] for v in datos["voces"]}
        self.assertTrue(ids_voces)
        for l in datos["lineas"]:
            self.assertIn(l["voz"], ids_voces)
            self.assertEqual(DIM, G.de_b64(np, l["vec"]).size)
        l1 = next(l for l in datos["lineas"] if l["i"] == 1)
        self.assertEqual(["las lecturas automáticas no coinciden"], l1["dudas"])
        l6 = next(l for l in datos["lineas"] if l["i"] == 6)
        self.assertGreaterEqual(l6["pisa"], G.PISA_MAX)
        self.assertTrue(any(h["fin"] - h["ini"] > G.HUECO_S for h in datos["huecos"]),
                        "el silencio final no salió como hueco")
        self.assertEqual("grabacion sintetica.wav", datos["audios"][0]["ruta"].split("/")[-1])

        with self.assertRaises(SystemExit):
            callado(G.main, args)


if __name__ == "__main__":
    unittest.main()
