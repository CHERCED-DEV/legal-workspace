# -*- coding: utf-8 -*-
"""
El adversario. Un test por vía NUEVA: cada uno intenta colar una cita falsa y
**pasa**, que es la demostración de que la vía está abierta.

`test_vias.py` prueba que las doce vías de las dos críticas están cerradas, y
lo están. Este archivo prueba otra cosa: que el perímetro que dibujan esas
doce no es el perímetro del instrumento. Se ataca por donde las críticas no
miraron —el token como credencial al portador, el orden de las
comprobaciones, los campos que la consulta trae y nadie compara, la rama B
que se quedó sin la corrección de la rama A, y la aritmética de fechas en el
borde del calendario—.

Convención: **si el test pasa, la vía está abierta**. Ningún test de aquí
corrige nada; todos documentan.

    cd evals/knowledge-pack && python -m unittest test_ataque -v

Aquí tampoco hay derecho: las mismas fichas de ejemplo de `fichas.py`.
"""

import inspect
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from contrato import (Pack, TIPOS_DE_FECHA, cadencia_de, caducada,       # noqa: E402
                      evaluar, revisar_antes_de)
from fichas import (HOY, FIRMANTE, consulta_norma, consulta_providencia,  # noqa: E402
                    ficha_norma, ficha_providencia, meses)

ART_00 = {"norma_completa": "no", "articulos": ["00"], "incisos": []}
LEY_ENTERA = {"norma_completa": "si", "articulos": [], "incisos": []}


def sin_serie(token):
    """El token sin su parte opaca: lo que un modelo podría reconstruir."""
    return " · ".join(p for p in token.split(" · ") if not p.startswith("serie:"))


class Ataque(unittest.TestCase):

    def codigo(self, ficha, consulta=None, hoy=HOY):
        if consulta is None:
            consulta = (consulta_providencia() if ficha.get("tipo") == "providencia"
                        else consulta_norma())
        return evaluar(ficha, consulta, hoy).codigo


# ───────────── I. El token: no hay que falsificarlo, lo regalan ─────────────

class ElToken(Ataque):

    def test_A01_el_pack_dice_que_no_y_entrega_un_token_que_dice_que_si(self):
        """LA VÍA PRINCIPAL. `responder` emite token para toda respuesta
        individual citable —antes de calcular la composición y sin mirarla—.
        En el escenario exacto de N4 (dos fichas del mismo identificador y
        alcance que discrepan en la vigencia) el pack contesta
        `CONFLICTO_ENTRE_FICHAS` y `citable = False`, y **al mismo tiempo pone
        en manos de quien consume un token registrado que la prueba de banco
        acepta**. El token es lo único que sobrevive hasta la publicación: si
        el «no» vive en la respuesta y el «sí» en el token, el «no» no existe.
        """
        una = ficha_norma(alcance_comprobado=ART_00)
        otra = ficha_norma(alcance_comprobado=ART_00, estado_vigencia="VIGENCIA_NO_COMPROBADA")
        pack = Pack([una, otra], curator=FIRMANTE, version="0.1.0")

        r = pack.responder(consulta_norma(), HOY)
        self.assertEqual("CONFLICTO_ENTRE_FICHAS", r.codigo)
        self.assertFalse(r.citable, "el pack niega el conjunto")

        tokens = [x.token for x in r.respuestas if x.token]
        self.assertEqual(1, len(tokens), "y aun así emitió un token")
        pasa, motivo = pack.verificar_token(tokens[0], ART_00, HOY)
        self.assertTrue(pasa, "la prueba de banco acepta el token de una respuesta negada")
        self.assertEqual("el token resuelve contra una respuesta servida", motivo)

    def test_A02_lo_mismo_con_la_regla_de_composicion_de_N5(self):
        """N5 eligió «el conjunto es citable solo si lo son todas» para que
        nadie se quede con la mejor coincidencia. El token deshace la elección
        sin discutirla: el consumidor se queda con la citable, que es
        exactamente la lectura descartada."""
        estrecha = ficha_norma()
        ancha = ficha_norma(alcance_comprobado={"norma_completa": "no",
                                                "articulos": ["00", "XX"], "incisos": []},
                            estado_vigencia="VIGENCIA_NO_COMPROBADA")
        pack = Pack([estrecha, ancha], curator=FIRMANTE)

        r = pack.responder(consulta_norma(), HOY)
        self.assertFalse(r.citable)
        vivo = [x for x in r.respuestas if x.token]
        self.assertEqual(1, len(vivo))
        self.assertTrue(pack.verificar_token(vivo[0].token, ART_00, HOY)[0])

    def test_A03_el_token_no_lleva_la_fecha_del_caso(self):
        """N2 acotó la ventana por arriba **en la evaluación**, y el token no
        registra para qué caso se emitió: dos consultas con fechas de caso
        distintas producen el mismo token salvo la serie, y `verificar_token`
        no tiene parámetro donde recibir una fecha de caso. Un token obtenido
        para un caso de dentro de la ventana ampara literalmente una cita en
        un caso de fuera: la prueba de banco no puede notarlo."""
        pack = Pack([ficha_norma()], curator=FIRMANTE, version="0.1.0")

        t1 = pack.responder(consulta_norma(fecha_del_caso=meses(-2)), HOY).respuestas[0].token
        t2 = pack.responder(consulta_norma(fecha_del_caso=meses(-11)), HOY).respuestas[0].token
        self.assertEqual(sin_serie(t1), sin_serie(t2),
                         "el token no distingue para qué caso se pidió")

        # La consulta con el caso fuera de ventana se niega...
        fuera = pack.responder(consulta_norma(fecha_del_caso=HOY.isoformat()), HOY)
        self.assertEqual("FUERA_DE_LA_VIGENCIA_COMPROBADA", fuera.codigo)
        self.assertIsNone(fuera.respuestas[0].token)

        # ...y el token de la consulta anterior sigue valiendo, sin que la
        # prueba de banco tenga dónde preguntar por la fecha del caso.
        self.assertTrue(pack.verificar_token(t1, ART_00, HOY)[0])
        self.assertNotIn("fecha", inspect.signature(Pack.verificar_token).parameters)

    def test_A04_el_checksum_se_escribe_en_el_token_y_no_se_lee_nunca(self):
        """V5' exigía `checksum` + `version` «porque sin él no hay a qué
        resolver un token». Están dentro del token y `verificar_token` no los
        compara con nada: el registro sobrevive a que la ficha salga del pack,
        y las cinco condiciones de fallo solo vuelven a mirar la caducidad."""
        f = ficha_norma()
        pack = Pack([f], curator=FIRMANTE, version="0.1.0")
        token = pack.responder(consulta_norma(), HOY).respuestas[0].token
        huella = pack.checksum()

        # 1. la ficha sale del pack: el token sigue resolviendo
        pack.fichas = []
        self.assertNotEqual(huella, pack.checksum(), "el pack ya no es el mismo")
        self.assertIn("pack:0.1.0@" + huella, token, "el token lleva la huella vieja")
        self.assertTrue(pack.verificar_token(token, ART_00, HOY)[0],
                        "un token de una ficha que el pack ya no tiene")

        # 2. la ficha se retracta entera: identidad, vigencia y reforma
        g = ficha_norma()
        pack2 = Pack([g], curator=FIRMANTE, version="0.1.0")
        token2 = pack2.responder(consulta_norma(), HOY).respuestas[0].token
        g["estado_identidad"] = "CONFLICTO_DE_FUENTES"
        g["estado_vigencia"] = "VIGENCIA_NO_COMPROBADA"
        g["reforma_buscada"] = "no"
        self.assertFalse(pack2.responder(consulta_norma(), HOY).citable,
                         "el pack ya no la sirve")
        self.assertTrue(pack2.verificar_token(token2, ART_00, HOY)[0],
                        "y su token sigue pasando la prueba de banco")

    def test_A05_el_texto_del_token_no_es_lo_que_se_comprueba(self):
        """El token dice «LEY-0000-0000 + {…articulos: [00]…}» y
        `verificar_token` compara lo citado contra el `alcance_comprobado`
        **de la ficha, leído hoy**, no contra el alcance que el token exhibe.
        Ensanchar la ficha después de emitir el token ensancha el token."""
        f = ficha_norma()
        pack = Pack([f], curator=FIRMANTE, version="0.1.0")
        token = pack.responder(consulta_norma(), HOY).respuestas[0].token
        self.assertIn("articulos: [00]", token)

        art_99 = {"norma_completa": "no", "articulos": ["99"], "incisos": ["99.9"]}
        self.assertFalse(pack.verificar_token(token, art_99, HOY)[0])

        f["alcance_comprobado"] = LEY_ENTERA
        self.assertTrue(pack.verificar_token(token, art_99, HOY)[0],
                        "el mismo token, que sigue diciendo [00], ahora ampara el 99")


# ───────── II. Lo que la consulta trae y nadie compara con la ficha ─────────

class LaConsulta(Ataque):

    def test_A06_materia_y_territorial_solo_se_miran_cuando_no_hay_ficha(self):
        """`materia` y `territorial` deciden la respuesta en la rama C —la de
        «no tengo esa ficha»— y **desaparecen en cuanto hay coincidencia**.
        El pack se contradice en la misma sesión: para un identificador que no
        tiene dice «no cubro esta área, aquí no hay información de ninguna
        clase»; para uno que sí tiene, en esa misma área, dice `CITABLE`. Es
        la vía que el encabezado de `contrato.py` declara cerrada al añadir
        `materia[]` a las providencias — el campo se añadió y no se compara.
        """
        pack = Pack([ficha_norma()], curator=FIRMANTE)
        ajena = "derecho-espacial-lunar"
        self.assertNotIn(ajena, pack.cobertura(HOY)["materias_declaradas"])

        # Sin ficha: el pack declara que el área está fuera.
        r_sin = pack.responder(consulta_norma(identificador="LEY-0000-9999", materia=ajena), HOY)
        self.assertEqual("FUERA_DE_COBERTURA", r_sin.codigo)

        # Con ficha: la misma área ya no se mira.
        r_con = pack.responder(consulta_norma(materia=ajena), HOY)
        self.assertEqual("CITABLE", r_con.codigo)
        self.assertTrue(r_con.citable)

        # Y la materia declarada por la propia ficha tampoco entra en la cuenta.
        otro = Pack([ficha_norma(materia=["area-que-no-es-la-de-la-consulta"])], curator=FIRMANTE)
        self.assertTrue(otro.responder(consulta_norma(), HOY).citable)

        # `territorial` igual: el pack es nacional y sirve la consulta territorial.
        terr = pack.responder(consulta_norma(territorial=True), HOY)
        self.assertEqual("CITABLE", terr.codigo)
        self.assertEqual(["nacional"], terr.cobertura["nivel_territorial"])

    def test_A07_tipo_de_fecha_se_valida_contra_el_vocabulario_y_no_se_usa(self):
        """R3 exige `tipo_de_fecha` porque «la fecha del caso no existe en
        singular: pasar la equivocada convierte una respuesta negativa en
        citable sin que nada lo note». Se comprueba que el valor esté en el
        vocabulario de `05` y después **ningún camino lo lee**: los cinco
        tipos dan el mismo código y el mismo token. La condición es una
        formalidad de forma, exactamente como `VIGENTE_AL` antes de V2."""
        codigos = {t: self.codigo(ficha_norma(), consulta_norma(tipo_de_fecha=t))
                   for t in sorted(TIPOS_DE_FECHA)}
        self.assertEqual({"CITABLE"}, set(codigos.values()), codigos)

        pack = Pack([ficha_norma()], curator=FIRMANTE, version="0.1.0")
        emitidos = {sin_serie(pack.responder(consulta_norma(tipo_de_fecha=t), HOY)
                              .respuestas[0].token) for t in sorted(TIPOS_DE_FECHA)}
        self.assertEqual(1, len(emitidos), "el tipo de fecha no llega ni al token")


# ─────────── III. La rama B se quedó sin las correcciones de la A ───────────

class LaRamaB(Ataque):

    def test_A08_la_providencia_no_tiene_techo_temporal_ninguno(self):
        """N2 cerró la ventana por arriba en A —«el techo es el día de la
        comprobación, hasta donde llega lo que la verificadora firmó»— y B no
        lee `fecha_del_caso` en ninguna línea. Un precedente firmado hace un
        mes se sirve como `CITABLE_PRECEDENTE` para un caso fechado cincuenta
        años después de la firma y para uno fechado quinientos años antes de
        que la providencia existiera. Y la jurisprudencia cambia por el mismo
        eje por el que cambia la vigencia."""
        p = ficha_providencia()
        for cuando in (meses(600), "9999-12-31", meses(-6000), "0001-01-01"):
            self.assertEqual("CITABLE_PRECEDENTE",
                             self.codigo(p, consulta_providencia(fecha_del_caso=cuando)),
                             "caso %s amparado por una firma de %s" % (cuando, meses(-1)))

        # La rama A, con la misma fecha, sí frena. La asimetría no está escrita
        # en ninguna parte.
        self.assertEqual("FUERA_DE_LA_VIGENCIA_COMPROBADA",
                         self.codigo(ficha_norma(), consulta_norma(fecha_del_caso=meses(600))))


# ─────────── IV. El mismo campo leído de dos maneras distintas ───────────

class DosLecturas(Ataque):

    def test_A09_tipo_se_lee_con_texto_en_evaluar_y_con_igualdad_en_todo_lo_demas(self):
        """`evaluar` normaliza `tipo` con `_texto` (que recorta espacios) y
        `cadencia_de`, `_citable_en_si`, `recuento` y `verificar_token` lo
        comparan con `==` crudo. Un espacio parte la ficha en dos: para la
        tabla de decisión es una providencia, para la prueba de banco y para
        el recuento es una norma.

        Consecuencia 1: el recuento que «viaja en CADA respuesta» dice cero
        citables en la respuesta que acaba de servir un citable con token.
        Consecuencia 2: el token de un precedente se comprueba contra un
        alcance de norma, y si la ficha lleva `alcance_comprobado` de norma
        completa, ampara la cita de cualquier artículo de cualquier cosa —
        mientras que la proposición correcta, la única que la ficha sostiene,
        es rechazada."""
        p = ficha_providencia(tipo=" providencia ")
        pack = Pack([p], curator=FIRMANTE, version="0.1.0")
        r = pack.responder(consulta_providencia(), HOY)
        self.assertEqual("CITABLE_PRECEDENTE", r.codigo)
        self.assertTrue(r.citable)
        self.assertEqual(0, r.recuento["citables_hoy"],
                         "sirve un citable y cuenta cero citables")
        self.assertEqual(0, r.recuento["vigencia_no_comprobada"])

        # La prueba de banco rechaza la proposición para la que se comprobó.
        self.assertFalse(pack.verificar_token(r.respuestas[0].token,
                                              "proposicion de ejemplo numero 00", HOY)[0])

        # Y con un `alcance_comprobado` de norma dentro, acepta lo que sea.
        q = ficha_providencia(tipo=" providencia ", alcance_comprobado=LEY_ENTERA)
        pack2 = Pack([q], curator=FIRMANTE, version="0.1.0")
        r2 = pack2.responder(consulta_providencia(), HOY)
        self.assertEqual("CITABLE_PRECEDENTE", r2.codigo)
        self.assertTrue(pack2.verificar_token(
            r2.respuestas[0].token,
            {"norma_completa": "no", "articulos": ["cualquier-articulo"], "incisos": []},
            HOY)[0], "el token de un precedente ampara la cita de un articulado")

    def test_A10_materia_en_cadena_se_recorre_letra_a_letra(self):
        """`leer_alcance` exige lista y rechaza la cadena; `cobertura` itera
        `materia` sin comprobar nada. Una `materia` escrita en singular —el
        error de tecleo más barato de la ficha— hace que el pack declare como
        materias cubiertas las **letras** del área, y `NO_ESTA_EN_EL_PACK`
        («materia cubierta, identificador ausente») desplaza a
        `FUERA_DE_COBERTURA` para consultas de una letra."""
        pack = Pack([ficha_norma(materia="civil")], curator=FIRMANTE)
        self.assertEqual(["c", "i", "l", "v"], pack.cobertura(HOY)["materias_declaradas"])
        r = pack.responder(consulta_norma(identificador="LEY-0000-9999", materia="c"), HOY)
        self.assertEqual("NO_ESTA_EN_EL_PACK", r.codigo)


# ─────── V. El orden de las comprobaciones y el borde del calendario ───────

class ElOrdenYElCalendario(Ataque):

    def test_A11_una_firma_del_ano_9999_tumba_el_pack_entero(self):
        """«Ninguna función de este archivo levanta una excepción por un dato
        malo: un dato malo es un no.» No es cierto. `revisar_antes_de` suma la
        cadencia sin comprobar el rango del calendario, y `cobertura` y
        `recuento` llaman a `caducada` **antes** que a `_firma_valida` —el
        orden inverso al de `_evaluar_norma`, que sí frena una firma futura—.
        Una sola casilla con `9999-01-01` deja el pack entero sin responder a
        nada, ni siquiera a las consultas sobre las demás fichas.

        `evaluar` sobre la misma ficha contesta `FICHA_NO_FIRMADA`: la
        diferencia es solo el orden de dos líneas."""
        bomba = ficha_norma(identificador_canonico="LEY-0000-0001", verificado_el="9999-01-01")
        self.assertEqual("FICHA_NO_FIRMADA", self.codigo(bomba), "evaluar sí la frena")

        self.assertRaises(ValueError, caducada, bomba, HOY)
        self.assertRaises(ValueError, revisar_antes_de, bomba)

        pack = Pack([ficha_norma(), bomba], curator=FIRMANTE)
        self.assertRaises(ValueError, pack.recuento, HOY)
        self.assertRaises(ValueError, pack.cobertura, HOY)
        self.assertRaises(ValueError, pack.degradado, HOY)
        # y la consulta sobre la ficha sana, que no tiene nada que ver:
        self.assertRaises(ValueError, pack.responder, consulta_norma(), HOY)

        # El interruptor de los 18 meses se rompe por el mismo sitio en cuanto
        # la mediana cae dentro del rango malo.
        self.assertRaises(ValueError, Pack([bomba], curator=FIRMANTE).apagado, HOY)

    def test_A12_la_fuente_puede_haberse_consultado_dentro_de_ocho_mil_anos(self):
        """`verificado_el` no puede ser futuro —`_firma_valida` lo cierra— y
        `consultada` no tiene ningún techo ni ningún suelo. `_identidad`
        recibe `hoy` y **no lo usa en ninguna línea**, que es la huella de la
        comprobación que se quiso hacer. Una ficha firmada ayer puede declarar
        que consultó la fuente oficial en el año 9999, o hace un siglo, y sale
        `CITABLE`: la cadencia mide la edad de la firma y nada mide la edad de
        lo que se firmó."""
        for cuando in ("9999-12-31", meses(1200), meses(-1200), "0001-01-01"):
            f = ficha_norma(
                fuente_identidad={"clase": "PRIMARY_OFFICIAL",
                                  "referencia": "https://ejemplo.invalido/publicacion",
                                  "consultada": cuando},
                fuente_vigencia={"clase": "PRIMARY_OFFICIAL",
                                 "referencia": "https://ejemplo.invalido/diario",
                                 "consultada": cuando})
            self.assertEqual("CITABLE", self.codigo(f),
                             "fuente consultada el %s y la ficha sigue citable" % cuando)

    def test_A13_apagado_mide_la_edad_de_las_firmas_no_si_el_pack_sirve(self):
        """N7 cambió `max` por mediana, y el escenario literal de la crítica
        —«veinticinco fichas podridas dentro»— vuelve a montarse bajando 20
        meses a 17: la mediana queda por debajo del umbral de 18, el
        interruptor no salta, y el pack responde `CITABLE` con 25 de sus 26
        fichas caducadas. El interruptor mide la antigüedad de las firmas y no
        cuántas fichas siguen sirviendo, que era la pregunta.

        `degradado` sí lo ve, y no gobierna nada: es un booleano que viaja al
        lado de una respuesta citable y ningún camino lo consulta."""
        podridas = [ficha_norma(identificador_canonico="LEY-0000-%04d" % (i + 1),
                                verificado_el=meses(-17),
                                estado_vigencia="VIGENTE_AL " + meses(-17))
                    for i in range(25)]
        pack = Pack(podridas + [ficha_norma()], curator=FIRMANTE, version="0.1.0")

        self.assertTrue(all(caducada(f, HOY) for f in podridas), "las 25 están caducadas")
        self.assertFalse(pack.apagado(HOY), "y el interruptor no salta")

        r = pack.responder(consulta_norma(), HOY)
        self.assertTrue(r.citable)
        self.assertEqual(25, r.recuento["caducados_hoy"])
        self.assertEqual(1, r.recuento["citables_hoy"])
        self.assertTrue(r.degradado, "lo dice, y sirve igual")
        self.assertIsNotNone(r.respuestas[0].token)

    def test_A14_apagado_no_cuenta_las_fichas_que_no_sabe_fechar(self):
        """Y la mediana se calcula sobre las firmas **legibles**: cualquier
        ficha cuya fecha no se pueda leer desaparece del censo en vez de
        contar como la más vieja. Cien fichas sin firma y una recién hecha
        dan un pack encendido cuya mediana es la de una sola ficha."""
        mudas = [ficha_norma(identificador_canonico="LEY-0001-%04d" % i, verificado_el="")
                 for i in range(100)]
        pack = Pack(mudas + [ficha_norma()], curator=FIRMANTE)
        self.assertFalse(pack.apagado(HOY))
        self.assertTrue(pack.responder(consulta_norma(), HOY).citable)


# ────────────── VI. Lo que la respuesta afirma sobre el mundo ──────────────

class LaFraseServida(Ataque):

    def test_A15_citable_sin_vigencia_hoy_afirma_que_hoy_no_rige_sin_saberlo(self):
        """`SIN_VIGENCIA_DESDE` con fecha futura es la forma normal de una
        derogatoria de vigencia diferida. Nada exige que la fecha del estado
        sea pasada, y la frase de `CITABLE_SIN_VIGENCIA_HOY` dice, literal,
        «Hoy no rige» — de una norma que la propia ficha declara vigente hasta
        dentro de cinco años. Es la única frase del contrato que afirma algo
        sobre el mundo, y el algoritmo no comprueba la afirmación."""
        futura = ficha_norma(estado_vigencia="SIN_VIGENCIA_DESDE " + meses(60),
                             vigencia_desde=meses(-120))
        r = evaluar(futura, consulta_norma(), HOY)
        self.assertEqual("CITABLE_SIN_VIGENCIA_HOY", r.codigo)
        self.assertIn("Hoy no rige", r.frase)
        self.assertIn(meses(60), futura["estado_vigencia"])

    def test_A16_conflicto_entre_fichas_no_tiene_como_decir_su_frase(self):
        """«La frase importa tanto como el código: el silencio se lee como no
        hay regla, y esa lectura es el fallo que el pack existe para
        impedir.» El código de composición es una cadena suelta en
        `RespuestaCompuesta`, que no construye ninguna `Respuesta` y no tiene
        atributo `frase`. La frase de `CONFLICTO_ENTRE_FICHAS` está escrita en
        `FRASES` y no hay camino que la sirva: se sirven las dos frases
        individuales, que no dicen que haya conflicto."""
        una = ficha_norma(alcance_comprobado=ART_00)
        otra = ficha_norma(alcance_comprobado=ART_00, estado_vigencia="VIGENCIA_NO_COMPROBADA")
        r = Pack([una, otra], curator=FIRMANTE).responder(consulta_norma(), HOY)

        self.assertEqual("CONFLICTO_ENTRE_FICHAS", r.codigo)
        self.assertFalse(hasattr(r, "frase"))
        self.assertNotIn("CONFLICTO_ENTRE_FICHAS", [x.codigo for x in r.respuestas])
        for x in r.respuestas:
            self.assertNotIn("discrepan en la vigencia comprobada", x.frase)


# ─────────────── VII. La lista negra dentro de la lista blanca ───────────────

class LaListaNegra(Ataque):

    def test_A17_apunta_al_corpus_es_una_lista_negra_de_seis_cadenas(self):
        """Todo el contrato es lista blanca menos esta función, que decide si
        una referencia es del corpus buscando seis subcadenas. Quitar la
        extensión, usar la barra de Windows o nombrar el archivo de otra
        manera desactiva N1 entero — y N1 es la vía que el renombrado del
        catálogo abre por sí solo. Ninguna de estas referencias apunta a una
        fuente oficial y todas dan `CITABLE`."""
        del_corpus_disfrazado = (
            "01-ficha-y-verificacion",                       # sin extensión
            "temporal-law-matrix, fila 9",                   # sin extensión
            "docs\\fichas\\catalogo-normativo.txt",          # barra de Windows
            "C:\\Users\\HITMA\\Desktop\\corpus\\normative-sources.txt",
            "normative-sources.markdown",                    # otra extensión
            "ver la ficha anterior",                         # ni siquiera un archivo
            "consultado internamente",
        )
        for referencia in del_corpus_disfrazado:
            fuente = {"clase": "PRIMARY_OFFICIAL", "referencia": referencia,
                      "consultada": meses(-1)}
            self.assertEqual("CITABLE",
                             self.codigo(ficha_norma(fuente_identidad=fuente,
                                                     fuente_vigencia=dict(fuente))),
                             "referencia=%r pasa como fuente primaria" % (referencia,))


# ─────────────────── VIII. Condiciones que no se alcanzan ───────────────────

class CodigoMuerto(Ataque):

    def test_A18_la_nota_obligatoria_de_vigencia_parcial_no_se_exige_nunca(self):
        """`ESTADOS_QUE_OBLIGAN_NOTA` tiene dos miembros y el segundo,
        `VIGENCIA_PARCIAL_AL`, retorna cuatro líneas antes de que se
        compruebe la nota: la mitad de esa constante es inalcanzable. No abre
        una cita —parcial nunca es citable— pero sí decide la **cadencia**:
        una ficha de vigencia parcial sin la nota que su estado obliga vive
        doce meses en vez de tres, y alimenta `cobertura` y `recuento` como
        cualquier otra."""
        parcial = ficha_norma(estado_vigencia="VIGENCIA_PARCIAL_AL " + meses(-1),
                              nota_de_vigencia="")
        self.assertEqual("VIGENCIA_PARCIAL", self.codigo(parcial),
                         "nunca llega a FICHA_INCOMPLETA")
        self.assertEqual(12, cadencia_de(parcial))
        self.assertEqual(3, cadencia_de(ficha_norma(
            estado_vigencia="VIGENCIA_PARCIAL_AL " + meses(-1),
            nota_de_vigencia="rige en parte")))

        # Y una ficha de vigencia parcial declara materia y cobertura como si
        # sirviera para algo.
        pack = Pack([parcial], curator=FIRMANTE)
        self.assertEqual(["area-de-ejemplo"], pack.cobertura(HOY)["materias_declaradas"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
