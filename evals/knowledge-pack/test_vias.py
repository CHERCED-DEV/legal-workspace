# -*- coding: utf-8 -*-
"""
Un test por vía. Cada uno **intenta colarse** y falla si lo consigue.

Las dos críticas de `docs/knowledge-pack/` son la especificación de las dos
primeras secciones: cinco vías originales (V1-V5) y siete que abrió la
corrección (N1-N8), más los cinco campos que la prosa dice leer y no lee.

La tercera sección (A01-A18) tiene otro origen y por eso se lee distinto. No
salió de una crítica en prosa sino de una suite adversaria —`test_ataque.py`—
donde cada test se escribía para **tener éxito cuando hay un agujero**: los
dieciocho pasaban, y que pasaran era la demostración de dieciocho vías
abiertas. Cerradas las dieciocho, cada ataque se reescribió afirmando la
conducta correcta y se mudó aquí. Ese es el ciclo, y es visible en un solo
número: **este archivo solo sube**. Diecinueve tras las dos críticas, treinta
y siete tras la primera ronda adversaria. `test_ataque.py` queda vacío,
esperando la siguiente.

Nada más entra aquí: un test que no corresponda a una vía, a un campo de las
críticas o a un ataque cerrado, sobra.

La única excepción, y es deliberada, es `test_control_positivo`. Sin él, un
contrato que contestara «no» a todo pasaría los demás tests con nota
perfecta. El control positivo es lo que obliga a que las negativas
signifiquen algo. Los tests de la tercera sección llevan además su propio
control positivo dentro, por el mismo motivo y a escala más fina: una guarda
nueva que negara de más no la cazaría nadie.

    cd evals/knowledge-pack && python -m unittest -v

Sin dependencias externas: `unittest` de la biblioteca estándar, porque esto
tiene que correr en la máquina de cualquiera.
"""

import inspect
import os
import sys
import unittest
from datetime import date, datetime, timedelta

# El directorio tiene un guion en el nombre y no es un paquete importable.
# Esto permite lanzar la suite desde la raíz del repositorio
# (`python -m unittest discover -s evals/knowledge-pack`) igual que desde aquí.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from contrato import (EJES_DE_CONSULTA, Pack, TIPOS_DE_FECHA,        # noqa: E402
                      cadencia_de, caducada, evaluar, mas_meses,
                      revisar_antes_de, _referencia_publicada)
from fichas import (HOY, FIRMANTE, consulta_norma, consulta_providencia,     # noqa: E402
                    ficha_norma, ficha_providencia, meses, sin)

# Los alcances que se repiten en la tercera y la cuarta sección.
ART_00 = {"norma_completa": "no", "articulos": ["00"], "incisos": []}
ART_00_Y_01 = {"norma_completa": "no", "articulos": ["00", "01"], "incisos": []}
LEY_ENTERA = {"norma_completa": "si", "articulos": [], "incisos": []}


def sin_serie(token):
    """El token sin su parte opaca: lo que un modelo podría reconstruir. Dos
    tokens que solo se distinguen en la serie son, para quien los escribe de
    memoria, el mismo token."""
    return " · ".join(p for p in token.split(" · ") if not p.startswith("serie:"))


class Via(unittest.TestCase):
    """Base común. `codigo()` evalúa una ficha contra su consulta natural."""

    def codigo(self, ficha, consulta=None, hoy=HOY):
        if consulta is None:
            consulta = (consulta_providencia() if ficha.get("tipo") == "providencia"
                        else consulta_norma())
        return evaluar(ficha, consulta, hoy).codigo

    def no_sale_citable(self, ficha, consulta=None, hoy=HOY):
        if consulta is None:
            consulta = (consulta_providencia() if ficha.get("tipo") == "providencia"
                        else consulta_norma())
        r = evaluar(ficha, consulta, hoy)
        self.assertFalse(r.citable, "se coló como %s: %s" % (r.codigo, r.motivo))
        return r.codigo


# ───────────────────────── el control positivo ─────────────────────────

class ControlPositivo(Via):

    def test_control_positivo_la_ficha_perfecta_si_es_citable(self):
        """No es una vía. Es lo que impide que `return NO_CITABLE` sea una
        implementación perfecta del contrato: las cuatro respuestas citables
        tienen que ser alcanzables con una ficha completa y firmada."""
        self.assertEqual("CITABLE", self.codigo(ficha_norma()))
        self.assertEqual("CITABLE_PRECEDENTE", self.codigo(ficha_providencia()))

        reforma = ficha_norma(
            estado_vigencia="VIGENTE_CON_REFORMA_AL " + meses(-1),
            nota_de_vigencia="consta reforma dentro del alcance; la redaccion no se comprobo")
        self.assertEqual("CITABLE_CON_REFORMA", self.codigo(reforma))

        derogada = ficha_norma(estado_vigencia="SIN_VIGENCIA_DESDE " + meses(-24),
                               vigencia_desde=meses(-120))
        self.assertEqual("CITABLE_SIN_VIGENCIA_HOY",
                         self.codigo(derogada, consulta_norma(fecha_del_caso=meses(-36))))


# ──────────────────── las cinco vías originales ────────────────────

class CincoViasOriginales(Via):

    def test_V1_alcance_comprobado_en_una_direccion(self):
        """Comprobado el art. 00, se pedía la ley entera: la petición no era
        «más fina», no entraba por esa rama, y salía CITABLE. P2 empuja a
        estrechar, así que la mayoría de las fichas son de artículo y la
        mayoría eran vulnerables. La prueba no es de finura sino de contención,
        y lo que no se puede comparar cae fuera."""
        ficha = ficha_norma()   # comprobado: art. 00

        mas_ancha = {"norma_completa": "si", "articulos": [], "incisos": []}
        self.assertEqual("FUERA_DEL_ALCANCE_COMPROBADO",
                         self.no_sale_citable(ficha, consulta_norma(peticion=mas_ancha)))

        disjunta = {"norma_completa": "no", "articulos": ["XX"], "incisos": []}
        self.assertEqual("FUERA_DEL_ALCANCE_COMPROBADO",
                         self.no_sale_citable(ficha, consulta_norma(peticion=disjunta)))

        # La contención entre niveles no está definida en el documento. Se
        # elige la lectura estricta de conjuntos —comprobar el art. 00 no
        # cubre el inciso 00.0— porque es la única que no depende de que
        # alguien lea con buena voluntad.
        un_inciso = {"norma_completa": "no", "articulos": [], "incisos": ["00.0"]}
        self.assertEqual("FUERA_DEL_ALCANCE_COMPROBADO",
                         self.no_sale_citable(ficha, consulta_norma(peticion=un_inciso)))

        # V1' — la petición es el operando izquierdo de la única comparación
        # que cierra V1, y en la prosa nadie decía qué forma tiene ni quién la
        # produce. Aquí llega tipada o no se compara.
        for informe in ("la norma completa", "art. 00", None, {}, {"articulos": ["00"]},
                        {"norma_completa": "no", "articulos": "00", "incisos": []}):
            self.assertEqual("FUERA_DEL_ALCANCE_COMPROBADO",
                             self.no_sale_citable(ficha, consulta_norma(peticion=informe)))

        vacia = {"norma_completa": "no", "articulos": [], "incisos": []}
        self.assertEqual("FUERA_DEL_ALCANCE_COMPROBADO",
                         self.no_sale_citable(ficha, consulta_norma(peticion=vacia)))

    def test_V2_norma_reformada_sin_comprobar_que_se_busco(self):
        """El hallazgo principal de la segunda crítica. `VIGENTE_AL` escrito
        tras buscar la reforma era literalmente indistinguible de `VIGENTE_AL`
        escrito sin mirarla: ningún campo registraba que el paso ocurriera.
        Salía CITABLE limpio, sin nota y sin aviso, que es la respuesta más
        tranquilizadora del contrato. El defecto tiene que ser el inseguro."""
        # `SI` en mayúsculas sí cuenta como valor distinto: tolerar el cambio
        # de caja es donde empieza la generosidad. Los espacios alrededor, en
        # cambio, se recortan en TODOS los campos por igual, y ese recorte
        # uniforme es justamente lo que hace que «   » valga como vacío.
        for valor in ("no", "", "   ", "no_comprobado", None, 0, "SI", "no comprobado"):
            self.assertEqual("VIGENCIA_NO_COMPROBADA",
                             self.no_sale_citable(ficha_norma(reforma_buscada=valor)),
                             "reforma_buscada=%r no debería comprobar nada" % (valor,))

        # El campo ausente vale lo que el campo en blanco.
        self.assertEqual("VIGENCIA_NO_COMPROBADA",
                         self.no_sale_citable(sin(ficha_norma(), "reforma_buscada")))

        # Y con la constancia, el caso más frecuente del derecho tiene salida.
        reforma = ficha_norma(estado_vigencia="VIGENTE_CON_REFORMA_AL " + meses(-1),
                              nota_de_vigencia="consta reforma dentro del alcance",
                              reforma_buscada="si")
        self.assertEqual("CITABLE_CON_REFORMA", self.codigo(reforma))

    def test_V3_casilla_vacia_o_valor_imprevisto(self):
        """El algoritmo era lista negra: todo lo que no fuera uno de los dos
        valores malos terminaba en CITABLE. La casilla vacía, el espacio en vez
        del guion bajo, el valor con un comentario detrás, la etiqueta escrita
        en minúsculas: cada errata era una autorización."""
        for valor in ("", "   ", None, 0,
                      "VIGENTE AL " + meses(-1),           # espacio por guion bajo
                      "vigente_al " + meses(-1),           # minúsculas
                      "VIGENTE_AL  " + meses(-1),          # dos espacios
                      "VIGENTE_AL " + meses(-1) + " # comprobado",   # comentario detrás
                      "VIGENTE_AL",                        # sin su fecha
                      "VIGENTE_AL AAAA-MM-DD",             # con el relleno dentro
                      "VIGENCIA_POR_VERIFICAR"):           # etiqueta de otro vocabulario
            self.assertEqual("VIGENCIA_NO_COMPROBADA",
                             self.no_sale_citable(ficha_norma(estado_vigencia=valor)),
                             "estado_vigencia=%r no debería reconocerse" % (valor,))

        for valor in ("", "   ", None, "IDENTIDAD VERIFICADA", "identidad_verificada",
                      "VERIFIED_OFFICIAL", "FUENTE_OFICIAL_VERIFICADA"):
            self.assertEqual("IDENTIDAD_POR_VERIFICAR",
                             self.no_sale_citable(ficha_norma(estado_identidad=valor)))

        # La clase de fuente, tipada y aparte. Una cadena que contiene las
        # letras PRIMARY_OFFICIAL no es una fuente primaria: eso era media vía.
        fuentes_malas = (
            {"clase": "NINGUNA", "referencia": "no se localizo fuente para el art. 00",
             "consultada": meses(-1)},
            {"clase": "SECONDARY", "referencia": "https://ejemplo.invalido/portal",
             "consultada": meses(-1)},
            {"clase": "OFFICIAL_CONSOLIDATED", "referencia": "https://ejemplo.invalido/portal",
             "consultada": meses(-1)},
            {"clase": "PRIMARY_OFFICIAL", "referencia": "", "consultada": meses(-1)},
            {"clase": "PRIMARY_OFFICIAL", "referencia": "https://ejemplo.invalido/x",
             "consultada": "AAAA-MM-DD"},
            "https://ejemplo.invalido/x PRIMARY_OFFICIAL consultada 1000-05-15",
            "", None, {},
        )
        for fuente in fuentes_malas:
            self.assertEqual("VIGENCIA_NO_COMPROBADA",
                             self.no_sale_citable(ficha_norma(fuente_vigencia=fuente)),
                             "fuente_vigencia=%r no debería comprobar nada" % (fuente,))

        # Un alcance en prosa no se puede comparar, y antes se comparaba.
        for alcance in ("art. 00", "", None, {"norma_completa": "quizas",
                                              "articulos": ["00"], "incisos": []}):
            self.assertEqual("FUERA_DEL_ALCANCE_COMPROBADO",
                             self.no_sale_citable(ficha_norma(alcance_comprobado=alcance)))

    def test_V4_providencia_superada_o_sin_busqueda_adversa(self):
        """`estado_uso` y `busqueda_adversa` —«el mecanismo entero» contra
        citar un precedente superado— no se leían en ninguna parte, y la
        providencia atravesaba la tabla de las normas sin que nada la tocara.
        Lo único que la salvaba era un desajuste de cadena que el renombrado
        iba a borrar: estar a salvo por una errata no es estar a salvo."""
        for valor in ("SUPERSEDED_OR_LIMITED", "CONFLICTING"):
            self.assertEqual("PRECEDENTE_SUPERADO_O_LIMITADO",
                             self.no_sale_citable(ficha_providencia(estado_uso=valor)))

        for valor in ("JURISPRUDENCIA_POR_VERIFICAR", "", "   ", None, 0,
                      "relevance_reviewed", "PROFESSIONALLY CONFIRMED"):
            self.assertEqual("JURISPRUDENCIA_POR_VERIFICAR",
                             self.no_sale_citable(ficha_providencia(estado_uso=valor)))

        for valor in ("", "   ", None,
                      "JURISPRUDENCE_GAP",
                      "JURISPRUDENCE_GAP — buscada " + meses(-1) + "; la cobertura no alcanza"):
            self.assertEqual("SIN_BUSQUEDA_ADVERSA",
                             self.no_sale_citable(ficha_providencia(busqueda_adversa=valor)))

        # La providencia no entra por la tabla de las normas, ni siquiera
        # cuando le faltan los campos que esa tabla mira: era exactamente así
        # como salía citable por omisión.
        muda = sin(ficha_providencia(), "estado_uso", "busqueda_adversa", "pasaje")
        self.assertNotIn(self.no_sale_citable(muda),
                         ("CITABLE", "CITABLE_CON_REFORMA", "CITABLE_SIN_VIGENCIA_HOY"))

        # Y una ficha que no declara qué es tampoco se cuela por la rama de
        # las normas: el tipo se declara, no se deduce de qué campos hay.
        self.assertEqual("NO_TENEMOS_INFORMACION_SUFICIENTE",
                         self.no_sale_citable(sin(ficha_providencia(), "tipo"),
                                              consulta_providencia()))

        # La proposición se compara literal: la unidad es el par
        # providencia + proposición, no la providencia.
        self.assertEqual("FUERA_DEL_ALCANCE_COMPROBADO",
                         self.no_sale_citable(
                             ficha_providencia(),
                             consulta_providencia(proposicion="proposicion de ejemplo numero XX")))

    def test_V5_cita_sin_token_o_token_falsificado(self):
        """El token cerraba «el modelo no preguntó y citó igual», pero no tenía
        nada infalsificable: cuatro campos que un modelo puede escribir. Y la
        prueba de banco enumeraba cuatro condiciones de fallo sin la que
        importa —«token que no corresponde a ninguna ficha»—, así que un token
        inventado junto a una cita inventada las pasaba las cuatro.

        `verificar_token` recibe ahora un cuarto argumento obligatorio, el
        caso para el que se cita: es la vía A03 y está probada en su propio
        test. Aquí solo cambia la llamada; ninguna de las seis condiciones que
        este test comprueba cambia."""
        pack = Pack([ficha_norma()], curator=FIRMANTE, version="0.1.0")
        citado = {"norma_completa": "no", "articulos": ["00"], "incisos": []}
        caso = consulta_norma()

        servida = pack.responder(consulta_norma(), HOY)
        token = servida.respuestas[0].token
        self.assertTrue(pack.verificar_token(token, citado, HOY, caso)[0],
                        "el token realmente servido tiene que resolver")

        # 1. cita sin token
        for nada in (None, "", "   "):
            self.assertFalse(pack.verificar_token(nada, citado, HOY, caso)[0])

        # 2. token plausible escrito a mano, con la huella correcta del pack y
        #    una serie que nunca se emitió
        inventado = ("CITABLE · LEY-0000-0000 + {norma_completa: no, articulos: [00], "
                     "incisos: []} · %s · %s · pack:0.1.0@%s · serie:0123456789abcdef"
                     % (meses(-1), HOY.isoformat(), pack.checksum()))
        self.assertFalse(pack.verificar_token(inventado, citado, HOY, caso)[0])

        # 3. token real manipulado: la serie existe, la cadena ya no es la que
        #    se sirvió
        self.assertFalse(pack.verificar_token(
            token.replace("CITABLE", "CITABLE_CON_REFORMA", 1), citado, HOY, caso)[0])

        # 4. token real, cita más ancha que el alcance que ampara
        self.assertFalse(pack.verificar_token(
            token, {"norma_completa": "si", "articulos": [], "incisos": []}, HOY, caso)[0])

        # 5. token real, ficha ya caducada el día en que se comprueba
        self.assertFalse(pack.verificar_token(token, citado, mas_meses(HOY, 24), caso)[0])

        # 6. una respuesta no citable no lleva token que exhibir
        otro = Pack([ficha_norma(reforma_buscada="no")], curator=FIRMANTE)
        self.assertIsNone(otro.responder(consulta_norma(), HOY).respuestas[0].token)


# ─────────────── las siete que abrió la corrección (N1-N8) ───────────────

class ViasNuevasDeLaCorreccion(Via):

    def test_N1_el_renombrado_planta_la_cadena_en_el_catalogo(self):
        """Después del renombrado, el catálogo dice literalmente
        `IDENTIDAD_VERIFICADA` al lado de cada norma —en campos marcados
        copiables— y la cuarentena de P0.b alcanza solo a las fechas, no a la
        columna de estado. Además los dos términos no significaban lo mismo:
        el del catálogo verificaba el enlace y los metadatos; el del pack, que
        una persona vio el texto en fuente oficial. Copiar del corpus no
        comprueba nada."""
        del_corpus = (
            "docs/skills-support/source-catalog/temporal-law-matrix.md",
            "normative-sources.md, fila 9",
            "C:/Users/HITMA/Desktop/legal-workspace/docs/knowledge-pack/01-ficha-y-verificacion.md",
            "./source-catalog/normative-sources.md",
        )
        for referencia in del_corpus:
            ficha = ficha_norma(fuente_identidad={"clase": "PRIMARY_OFFICIAL",
                                                  "referencia": referencia,
                                                  "consultada": meses(-1)})
            self.assertEqual("IDENTIDAD_POR_VERIFICAR", self.no_sale_citable(ficha),
                             "una fila del catálogo no comprueba la identidad")

            ficha = ficha_norma(fuente_vigencia={"clase": "PRIMARY_OFFICIAL",
                                                 "referencia": referencia,
                                                 "consultada": meses(-1)})
            self.assertEqual("VIGENCIA_NO_COMPROBADA", self.no_sale_citable(ficha))

        # Y la etiqueta del catálogo tampoco es una clase de fuente.
        ficha = ficha_norma(fuente_identidad={"clase": "VERIFIED_OFFICIAL",
                                              "referencia": "https://ejemplo.invalido/oficial",
                                              "consultada": meses(-1)})
        self.assertEqual("IDENTIDAD_POR_VERIFICAR", self.no_sale_citable(ficha))

    def test_N2_ventana_de_vigencia_acotada_por_un_solo_lado(self):
        """A.6 exigía `fecha_del_caso >= vigencia_desde` y nada acotaba el caso
        por arriba. Una comprobación firmada no dice nada de lo que pasó
        después, y con cadencia de doce meses se servía como comprobada hasta
        un año de vigencia que nadie miró. Es V1 otra vez, en el eje del
        tiempo: el límite superior existía en la frase servida —«va de X a
        Y»— y no en el algoritmo."""
        firmada_hace_once = ficha_norma(verificado_el=meses(-11),
                                        estado_vigencia="VIGENTE_AL " + meses(-11))

        # Sigue viva —la cadencia es de doce meses— y responde dentro de su
        # ventana.
        self.assertEqual("CITABLE",
                         self.codigo(firmada_hace_once,
                                     consulta_norma(fecha_del_caso=meses(-11))))

        # Pero un caso posterior al día de la comprobación no está comprobado.
        for cuando in (meses(-10), meses(-5), meses(-1), HOY.isoformat()):
            self.assertEqual("FUERA_DE_LA_VIGENCIA_COMPROBADA",
                             self.no_sale_citable(firmada_hace_once,
                                                  consulta_norma(fecha_del_caso=cuando)),
                             "el caso %s es posterior a la comprobación" % cuando)

    def test_N3_providencia_no_caduca(self):
        """La tabla de cadencias está escrita entera sobre `estado_vigencia`,
        campo que una providencia no tiene —es el argumento mismo para darle
        rama propia—. Ninguna fila aplicaba, la cadencia quedaba indefinida y
        B.1 no podía fallar nunca: una providencia firmada hoy seguía siendo
        citable en 2040."""
        vieja = ficha_providencia(verificado_el=meses(-60))
        self.assertEqual("PACK_CADUCADO", self.no_sale_citable(vieja))

        limite = revisar_antes_de(ficha_providencia())
        self.assertIsNotNone(limite, "una providencia tiene que tener fecha de revisión")
        self.assertEqual("CITABLE_PRECEDENTE", self.codigo(ficha_providencia(), hoy=limite))
        self.assertEqual("PACK_CADUCADO",
                         self.no_sale_citable(ficha_providencia(), hoy=limite + timedelta(days=1)))

    def test_N4_problema_de_vigencia_bajo_codigo_de_identidad(self):
        """Dos fichas del mismo par (identificador, alcance) que discrepan en
        la **vigencia** se servían bajo `CONFLICTO_DE_FUENTES`, que está
        definido como `estado_identidad = CONFLICTO_DE_FUENTES` y cuya frase
        habla de dos fuentes oficiales que discrepan. Es el fallo simétrico del
        que la corrección arregló: un problema de vigencia bajo un código de
        identidad."""
        alcance = {"norma_completa": "no", "articulos": ["00"], "incisos": []}
        una = ficha_norma(alcance_comprobado=alcance)
        otra = ficha_norma(alcance_comprobado=alcance, estado_vigencia="VIGENCIA_NO_COMPROBADA")

        r = Pack([una, otra], curator=FIRMANTE).responder(consulta_norma(), HOY)
        self.assertFalse(r.citable)
        self.assertNotIn("CONFLICTO_DE_FUENTES", r.codigos + [r.codigo],
                         "un problema de vigencia no se sirve bajo el código de identidad")
        self.assertEqual("CONFLICTO_ENTRE_FICHAS", r.codigo)

        # Y el código de identidad sigue siendo para lo que es.
        self.assertEqual("CONFLICTO_DE_FUENTES",
                         self.no_sale_citable(ficha_norma(estado_identidad="CONFLICTO_DE_FUENTES")))

    def test_N5_respuesta_multiple_sin_regla_de_composicion(self):
        """El caso normal, no el raro: P2 empuja a estrechar, luego habrá
        varias fichas por norma. R2 dice que una respuesta distinta de una
        citable cierra el turno; con dos fichas, una citable y otra no, las dos
        lecturas posibles eran «se cierra igual» y «el consumidor se queda con
        la citable», que es el pack eligiendo la mejor coincidencia trasladado
        al consumidor. El documento no decía cuál."""
        estrecha = ficha_norma()
        ancha = ficha_norma(alcance_comprobado={"norma_completa": "no",
                                                "articulos": ["00", "XX"], "incisos": []},
                            estado_vigencia="VIGENCIA_NO_COMPROBADA")

        r = Pack([estrecha, ancha], curator=FIRMANTE).responder(consulta_norma(), HOY)
        self.assertEqual(2, len(r.respuestas), "se devuelven todas, el pack no elige")
        self.assertIn("CITABLE", r.codigos)
        self.assertIn("VIGENCIA_NO_COMPROBADA", r.codigos)
        self.assertFalse(r.citable, "el conjunto es citable solo si lo son todas")

    def test_N6_cadencia_que_depende_de_interpretar_la_nota(self):
        """El primer portón del algoritmo necesita la cadencia, y la fila que
        cubre las fichas peligrosas —«la nota registra un cambio con fecha
        futura… o el día anterior a esa fecha si es antes»— exige leer la nota
        y extraerle una fecha. El campo 9 prohíbe interpretarla. Las dos no
        pueden ser verdad, y si se respeta la prohibición esa fila no se aplica
        nunca y las fichas peligrosas caen a la cadencia larga."""
        con_nota = ficha_norma(verificado_el=meses(-5),
                               estado_vigencia="VIGENTE_AL " + meses(-5),
                               nota_de_vigencia="control pendiente anunciado para " + meses(2))
        self.assertEqual("PACK_CADUCADO",
                         self.no_sale_citable(con_nota,
                                              consulta_norma(fecha_del_caso=meses(-6))))

        # La misma ficha sin nota sigue viva: la cadencia larga es para las
        # fichas sin nada pendiente, y solo para ellas.
        sin_nota = ficha_norma(verificado_el=meses(-5),
                               estado_vigencia="VIGENTE_AL " + meses(-5))
        self.assertEqual("CITABLE",
                         self.codigo(sin_nota, consulta_norma(fecha_del_caso=meses(-6))))

        # Y la cadencia no depende del CONTENIDO de la nota: una nota con una
        # fecha dentro y otra sin ninguna dan la misma fecha de revisión. Esa
        # igualdad es la prueba de que el pack no la está interpretando.
        con_fecha = ficha_norma(nota_de_vigencia="cambio anunciado para " + meses(3))
        sin_fecha = ficha_norma(nota_de_vigencia="observacion sin ninguna fecha dentro")
        self.assertEqual(revisar_antes_de(con_fecha), revisar_antes_de(sin_fecha))

    def test_N7_una_ficha_nueva_rejuvenece_el_reloj_global(self):
        """El interruptor de los 18 meses colgaba de `max(verificado_el)` sobre
        todos los registros: una sola ficha nueva rejuvenece el reloj del pack
        entero. Verificar un registro cada diecisiete meses lo mantiene
        encendido indefinidamente con veinticinco fichas podridas dentro."""
        podridas = [ficha_norma(identificador_canonico="LEY-0000-%04d" % (i + 1),
                                verificado_el=meses(-20))
                    for i in range(25)]
        impecable = ficha_norma()          # firmada hace un mes, todo en regla
        pack = Pack(podridas + [impecable], curator=FIRMANTE)

        self.assertTrue(pack.apagado(HOY), "veinticinco fichas de hace 20 meses apagan el pack")
        r = pack.responder(consulta_norma(), HOY)
        self.assertFalse(r.citable, "la ficha nueva no vuelve a encender el pack")
        self.assertEqual("NO_TENEMOS_INFORMACION_SUFICIENTE", r.codigo)

        # Y el interruptor no está siempre puesto: un pack mantenido responde.
        self.assertFalse(Pack([ficha_norma()], curator=FIRMANTE).apagado(HOY))

    def test_N8_min_sobre_valores_indefinidos(self):
        """`revisar_antes_de = min(verificado_el + cadencia, acortamiento_manual)`
        no es una función total, y el propio instrumento lo demuestra: su ficha
        de ejemplo lleva `acortamiento_manual: null`. Y `SIN_VIGENCIA_DESDE`
        tenía cadencia «no aplica», que en código significa inmortal."""
        firmado = date.fromisoformat(meses(-1))
        self.assertEqual(mas_meses(firmado, 12), revisar_antes_de(ficha_norma()),
                         "un acortamiento nulo no rompe la cuenta ni la alarga")

        # Un acortamiento posterior a la fecha calculada se ignora: cuando la
        # fecha era escribible, una sola casilla hacía inmortal una ficha.
        for tarde in ("9999-01-01", meses(120)):
            self.assertEqual(revisar_antes_de(ficha_norma()),
                             revisar_antes_de(ficha_norma(acortamiento_manual=tarde)))

        # Uno ilegible tampoco alarga nada.
        for basura in ("manana", "", 0, [], "AAAA-MM-DD", {"fecha": meses(-2)}):
            self.assertEqual(revisar_antes_de(ficha_norma()),
                             revisar_antes_de(ficha_norma(acortamiento_manual=basura)),
                             "acortamiento_manual=%r no debería mover la cuenta" % (basura,))

        # Uno anterior sí adelanta: solo puede acortar.
        self.assertEqual("PACK_CADUCADO",
                         self.no_sale_citable(ficha_norma(acortamiento_manual=meses(-1))))

        # `SIN_VIGENCIA_DESDE` no es inmortal.
        derogada = ficha_norma(estado_vigencia="SIN_VIGENCIA_DESDE " + meses(-24),
                               vigencia_desde=meses(-120), verificado_el=meses(-60))
        self.assertEqual("PACK_CADUCADO",
                         self.no_sale_citable(derogada,
                                              consulta_norma(fecha_del_caso=meses(-36))))

        # Y una firma ilegible no da una ficha inmortal: da una sin fecha de
        # revisión, que es una ficha caducada.
        self.assertIsNone(revisar_antes_de(ficha_norma(verificado_el="")))


# ────────── los campos que la prosa dice leer y no lee ──────────

class CamposQueNoSeLeian(Via):

    def test_campo_verificado_por_vacio(self):
        """«No existe la ficha anónima: una ficha sin `verificado_por` no es
        una ficha a medias, es una ficha que el pack no sirve.» Ni A ni B lo
        miraban, y la frase servida imprimía «Comprobado por » con el hueco."""
        for valor in ("", "   ", None, 0, []):
            self.assertEqual("FICHA_NO_FIRMADA",
                             self.no_sale_citable(ficha_norma(verificado_por=valor)))
        self.assertEqual("FICHA_NO_FIRMADA",
                         self.no_sale_citable(sin(ficha_norma(), "verificado_por")))
        self.assertEqual("FICHA_NO_FIRMADA",
                         self.no_sale_citable(ficha_providencia(verificado_por="")))

    def test_campo_verificado_el_invalido_o_futuro(self):
        """No había condición de que fuera una fecha válida ni de que no fuera
        futura: vacío o malformado rompía el cálculo de la caducidad sin
        resultado definido, y futuro hacía la ficha inmortal."""
        for valor in ("", "   ", None, "AAAA-MM-DD", "15 de junio", "1000-13-01",
                      "1000/05/15", 10000515):
            self.assertEqual("FICHA_NO_FIRMADA",
                             self.no_sale_citable(ficha_norma(verificado_el=valor)),
                             "verificado_el=%r no es una firma legible" % (valor,))
        self.assertEqual("FICHA_NO_FIRMADA",
                         self.no_sale_citable(sin(ficha_norma(), "verificado_el")))

        for futuro in (meses(1), meses(600)):
            self.assertEqual("FICHA_NO_FIRMADA",
                             self.no_sale_citable(ficha_norma(verificado_el=futuro)),
                             "una firma futura haría inmortal la ficha")

    def test_campo_fuente_identidad_vacia(self):
        """Podía ir vacía con `estado_identidad = IDENTIDAD_VERIFICADA`: la
        columna de vigencia tenía puerta con clase tipada y la de identidad no
        tenía ninguna."""
        malas = (
            "", "   ", None, {},
            "https://ejemplo.invalido/oficial — consultada " + meses(-1),   # sin tipar
            {"clase": "NINGUNA", "referencia": "https://ejemplo.invalido/x",
             "consultada": meses(-1)},
            {"clase": "SECONDARY", "referencia": "https://ejemplo.invalido/x",
             "consultada": meses(-1)},
            {"clase": "PRIMARY_OFFICIAL", "referencia": "", "consultada": meses(-1)},
            {"clase": "PRIMARY_OFFICIAL", "referencia": "https://ejemplo.invalido/x",
             "consultada": ""},
            {"clase": "PRIMARY_OFFICIAL", "referencia": "https://ejemplo.invalido/x"},
        )
        for fuente in malas:
            self.assertEqual("IDENTIDAD_POR_VERIFICAR",
                             self.no_sale_citable(ficha_norma(fuente_identidad=fuente)),
                             "fuente_identidad=%r no comprueba una identidad" % (fuente,))
        self.assertEqual("IDENTIDAD_POR_VERIFICAR",
                         self.no_sale_citable(sin(ficha_norma(), "fuente_identidad")))
        self.assertEqual("IDENTIDAD_POR_VERIFICAR",
                         self.no_sale_citable(ficha_providencia(fuente_identidad={})))

    def test_campo_nota_de_vigencia_obligatoria_y_vacia(self):
        """La nota es obligatoria con `VIGENTE_CON_REFORMA_AL` y con
        `VIGENCIA_PARCIAL_AL`, y ninguna condición comprobaba que estuviera
        llena: `CITABLE_CON_REFORMA` con nota vacía era alcanzable, y esa
        respuesta existe justamente para transcribir la nota."""
        for valor in ("", "   ", None, 0):
            reformada = ficha_norma(estado_vigencia="VIGENTE_CON_REFORMA_AL " + meses(-1),
                                    nota_de_vigencia=valor)
            self.assertEqual("FICHA_INCOMPLETA", self.no_sale_citable(reformada))

        sin_campo = sin(ficha_norma(estado_vigencia="VIGENTE_CON_REFORMA_AL " + meses(-1)),
                        "nota_de_vigencia")
        self.assertEqual("FICHA_INCOMPLETA", self.no_sale_citable(sin_campo))

        # Con la nota llena sí sale, y la respuesta la lleva transcrita.
        completa = ficha_norma(estado_vigencia="VIGENTE_CON_REFORMA_AL " + meses(-1),
                               nota_de_vigencia="consta reforma dentro del alcance")
        r = evaluar(completa, consulta_norma(), HOY)
        self.assertEqual("CITABLE_CON_REFORMA", r.codigo)
        self.assertEqual("consta reforma dentro del alcance", r.nota)

    def test_campo_pasaje_vacio_en_una_providencia(self):
        """B no lo miraba: salía `CITABLE_PRECEDENTE` con el pasaje vacío y la
        frase decía «sostiene la proposición … en ‹›». El pasaje es lo que
        impide sustituirlo por el título o el resumen del buscador."""
        for valor in ("", "   ", None, 0):
            self.assertEqual("FICHA_INCOMPLETA",
                             self.no_sale_citable(ficha_providencia(pasaje=valor)))
        self.assertEqual("FICHA_INCOMPLETA",
                         self.no_sale_citable(sin(ficha_providencia(), "pasaje")))


# ────────── las dieciocho de la primera ronda adversaria (A01-A18) ──────────
#
# Cada uno de estos tests fue un ataque que pasaba. La conducta que describían
# está entre comillas en su docstring, en pasado, porque leer qué se rompió
# vale más que leer qué se arregló: la vía se cierra una vez y el patrón se
# repite.


# ── I. El token: no había que falsificarlo, lo regalaban ──

class ElTokenComoCredencial(Via):

    def test_A01_el_pack_que_niega_el_conjunto_no_entrega_token(self):
        """LA VÍA PRINCIPAL. «`responder` emite token para toda respuesta
        individual citable, antes de calcular la composición y sin mirarla»:
        en el escenario exacto de N4 el pack contestaba
        `CONFLICTO_ENTRE_FICHAS` y `citable = False`, y al mismo tiempo ponía
        en manos de quien consume un token registrado que la prueba de banco
        aceptaba. El token es lo único que sobrevive hasta la publicación: si
        el «no» vive en la respuesta y el «sí» en el token, el «no» no
        existe."""
        una = ficha_norma(alcance_comprobado=ART_00)
        otra = ficha_norma(alcance_comprobado=ART_00, estado_vigencia="VIGENCIA_NO_COMPROBADA")
        pack = Pack([una, otra], curator=FIRMANTE, version="0.1.0")

        r = pack.responder(consulta_norma(), HOY)
        self.assertEqual("CONFLICTO_ENTRE_FICHAS", r.codigo)
        self.assertFalse(r.citable, "el pack niega el conjunto")
        self.assertEqual([], [x.token for x in r.respuestas if x.token],
                         "y no entrega ningún token que diga lo contrario")
        self.assertEqual({}, pack.registro, "no se registró ninguna respuesta servida")

    def test_A02_la_regla_de_composicion_de_N5_tambien_gobierna_el_token(self):
        """«N5 eligió *el conjunto es citable solo si lo son todas* para que
        nadie se quede con la mejor coincidencia. El token deshacía la
        elección sin discutirla»: el consumidor se quedaba con la citable, que
        es exactamente la lectura descartada."""
        estrecha = ficha_norma()
        ancha = ficha_norma(alcance_comprobado={"norma_completa": "no",
                                                "articulos": ["00", "XX"], "incisos": []},
                            estado_vigencia="VIGENCIA_NO_COMPROBADA")
        pack = Pack([estrecha, ancha], curator=FIRMANTE)

        r = pack.responder(consulta_norma(), HOY)
        self.assertIn("CITABLE", r.codigos, "la respuesta individual no se esconde")
        self.assertFalse(r.citable)
        self.assertEqual([], [x.token for x in r.respuestas if x.token])

        # Control positivo: cuando el conjunto sí es citable, el token se emite.
        solo = Pack([ficha_norma()], curator=FIRMANTE)
        self.assertIsNotNone(solo.responder(consulta_norma(), HOY).respuestas[0].token)

    def test_A03_el_token_dice_para_que_caso_se_pidio_y_se_comprueba(self):
        """«N2 acotó la ventana por arriba en la evaluación, y el token no
        registraba para qué caso se emitió: dos consultas con fechas de caso
        distintas producían el mismo token salvo la serie, y `verificar_token`
        no tenía parámetro donde recibir una fecha de caso.» Un token obtenido
        para un caso de dentro de la ventana amparaba literalmente una cita en
        un caso de fuera."""
        pack = Pack([ficha_norma()], curator=FIRMANTE, version="0.1.0")
        dentro = consulta_norma(fecha_del_caso=meses(-2))
        otro_caso = consulta_norma(fecha_del_caso=meses(-11))

        t1 = pack.responder(dentro, HOY).respuestas[0].token
        t2 = pack.responder(otro_caso, HOY).respuestas[0].token
        self.assertNotEqual(sin_serie(t1), sin_serie(t2), "el token distingue el caso")
        self.assertIn("caso:" + meses(-2), t1)
        self.assertIn("caso", inspect.signature(Pack.verificar_token).parameters,
                      "la prueba de banco tiene dónde recibir el caso")

        self.assertTrue(pack.verificar_token(t1, ART_00, HOY, dentro)[0])
        self.assertFalse(pack.verificar_token(t1, ART_00, HOY, otro_caso)[0],
                         "el token de un caso no ampara otro caso")

        # La consulta con el caso fuera de ventana se niega y no lleva token...
        fuera = consulta_norma(fecha_del_caso=HOY.isoformat())
        negada = pack.responder(fuera, HOY)
        self.assertEqual("FUERA_DE_LA_VIGENCIA_COMPROBADA", negada.codigo)
        self.assertIsNone(negada.respuestas[0].token)
        # ...y el token de la consulta anterior tampoco la ampara.
        self.assertFalse(pack.verificar_token(t1, ART_00, HOY, fuera)[0])

        # Citar sin decir para qué caso se cita no es citar con token.
        for nada in (None, "", {}, {"fecha_del_caso": meses(-2)}):
            self.assertFalse(pack.verificar_token(t1, ART_00, HOY, nada)[0])

    def test_A04_la_huella_del_pack_que_el_token_exhibe_se_lee(self):
        """«V5' exigía `checksum` + `version` porque *sin ellos no hay a qué
        resolver un token*. Estaban dentro del token y `verificar_token` no
        los comparaba con nada»: el registro sobrevivía a que la ficha saliera
        del pack y a que la ficha se retractara entera."""
        f = ficha_norma()
        pack = Pack([f], curator=FIRMANTE, version="0.1.0")
        caso = consulta_norma()
        token = pack.responder(caso, HOY).respuestas[0].token
        self.assertIn(pack.checksum(), token)
        self.assertTrue(pack.verificar_token(token, ART_00, HOY, caso)[0])

        # 1. la ficha sale del pack
        pack.fichas = []
        pasa, motivo = pack.verificar_token(token, ART_00, HOY, caso)
        self.assertFalse(pasa, "un token de una ficha que el pack ya no tiene")
        self.assertIn("otra versión del pack", motivo)

        # 2. la ficha se retracta entera: identidad, vigencia y reforma
        g = ficha_norma()
        pack2 = Pack([g], curator=FIRMANTE, version="0.1.0")
        token2 = pack2.responder(caso, HOY).respuestas[0].token
        g["estado_identidad"] = "CONFLICTO_DE_FUENTES"
        g["estado_vigencia"] = "VIGENCIA_NO_COMPROBADA"
        g["reforma_buscada"] = "no"
        self.assertFalse(pack2.responder(caso, HOY).citable, "el pack ya no la sirve")
        self.assertFalse(pack2.verificar_token(token2, ART_00, HOY, caso)[0],
                         "y su token tampoco")

        # 3. la versión cuenta igual que el contenido
        pack3 = Pack([ficha_norma()], curator=FIRMANTE, version="0.1.0")
        token3 = pack3.responder(caso, HOY).respuestas[0].token
        pack3.version = "0.2.0"
        self.assertFalse(pack3.verificar_token(token3, ART_00, HOY, caso)[0])

    def test_A05_el_token_se_resuelve_contra_la_foto_no_contra_la_ficha_viva(self):
        """«El token decía *LEY-0000-0000 + {…articulos: [00]…}* y
        `verificar_token` comparaba lo citado contra el `alcance_comprobado`
        de la ficha leído hoy, no contra el alcance que el token exhibe.»
        Ensanchar la ficha después de emitir el token ensanchaba el token.

        La comprobación se monta sin mover la huella del pack —contenido
        idéntico, objeto distinto— para que sea esta guarda y no la de A04 la
        que tenga que sostener el peso."""
        f = ficha_norma()
        pack = Pack([f], curator=FIRMANTE, version="0.1.0")
        caso = consulta_norma()
        token = pack.responder(caso, HOY).respuestas[0].token
        self.assertIn("articulos: [00]", token)

        art_99 = {"norma_completa": "no", "articulos": ["99"], "incisos": ["99.9"]}
        self.assertFalse(pack.verificar_token(token, art_99, HOY, caso)[0])

        huella = pack.checksum()
        pack.fichas = [ficha_norma()]
        f["alcance_comprobado"] = LEY_ENTERA
        f["verificado_el"] = meses(-60)
        self.assertEqual(huella, pack.checksum(), "el pack sigue siendo el mismo")

        pasa, motivo = pack.verificar_token(token, art_99, HOY, caso)
        self.assertFalse(pasa, "el token sigue diciendo [00] y sigue amparando [00]")
        self.assertIn("no contiene lo que se cita", motivo)
        self.assertTrue(pack.verificar_token(token, ART_00, HOY, caso)[0],
                        "y lo que amparaba lo sigue amparando: el pack no ha cambiado")

        # La caducidad del token es la que se calculó el día en que se sirvió,
        # por el mismo motivo: se mide sobre la foto y no sobre nada vivo.
        self.assertFalse(pack.verificar_token(token, ART_00, mas_meses(HOY, 24), caso)[0])


# ── II. Lo que la consulta trae y nadie comparaba con la ficha ──

class LaConsultaContraLaFicha(Via):

    def test_A06_materia_y_territorial_se_miran_tambien_cuando_hay_ficha(self):
        """«`materia` y `territorial` decidían la respuesta en la rama C —la
        de *no tengo esa ficha*— y desaparecían en cuanto había
        coincidencia.» El pack se contradecía en la misma sesión: para un
        identificador que no tenía decía «no cubro esta área, aquí no hay
        información de ninguna clase»; para uno que sí tenía, en esa misma
        área, decía `CITABLE`."""
        pack = Pack([ficha_norma()], curator=FIRMANTE)
        ajena = "derecho-espacial-lunar"
        self.assertNotIn(ajena, pack.cobertura(HOY)["materias_declaradas"])

        sin_ficha = pack.responder(consulta_norma(identificador="LEY-0000-9999", materia=ajena), HOY)
        self.assertEqual("FUERA_DE_COBERTURA", sin_ficha.codigo)

        con_ficha = pack.responder(consulta_norma(materia=ajena), HOY)
        self.assertEqual("FUERA_DEL_ALCANCE_COMPROBADO", con_ficha.codigo)
        self.assertFalse(con_ficha.citable, "tener la ficha no cubre el área")

        # La materia que declara la ficha entra en la cuenta.
        otro = Pack([ficha_norma(materia=["area-que-no-es-la-de-la-consulta"])], curator=FIRMANTE)
        self.assertFalse(otro.responder(consulta_norma(), HOY).citable)

        # `territorial` igual: que el pack tenga el registro no lo vuelve competente.
        terr = pack.responder(consulta_norma(territorial=True), HOY)
        self.assertEqual("FUERA_DE_COBERTURA", terr.codigo)
        self.assertFalse(terr.citable)

        # Y la providencia, que es donde `materia[]` se añadió para esto.
        precedentes = Pack([ficha_providencia()], curator=FIRMANTE)
        self.assertFalse(precedentes.responder(consulta_providencia(materia=ajena), HOY).citable)

        # Control positivo: en la materia que la ficha declara, sí.
        self.assertTrue(pack.responder(consulta_norma(), HOY).citable)
        self.assertTrue(precedentes.responder(consulta_providencia(), HOY).citable)

    def test_A07_el_tipo_de_fecha_llega_al_token_y_se_comprueba(self):
        """«R3 exige `tipo_de_fecha` porque *la fecha del caso no existe en
        singular*. Se comprobaba que el valor estuviera en el vocabulario de
        `05` y después ningún camino lo leía»: los cinco tipos daban el mismo
        código y el mismo token, y la condición era una formalidad de forma.

        Los cinco siguen dando el mismo código, y eso NO es la vía: cuál de
        las cinco fechas gobierna es una pregunta de derecho que el pack no
        puede contestar sin inventarse un campo. Lo que sí puede, y ahora
        hace, es impedir que un token pedido para un tipo de fecha ampare una
        cita hecha para otro."""
        codigos = {t: self.codigo(ficha_norma(), consulta_norma(tipo_de_fecha=t))
                   for t in sorted(TIPOS_DE_FECHA)}
        self.assertEqual({"CITABLE"}, set(codigos.values()), codigos)

        pack = Pack([ficha_norma()], curator=FIRMANTE, version="0.1.0")
        tokens = {}
        for t in sorted(TIPOS_DE_FECHA):
            consulta = consulta_norma(tipo_de_fecha=t)
            tokens[t] = pack.responder(consulta, HOY).respuestas[0].token
            self.assertTrue(pack.verificar_token(tokens[t], ART_00, HOY, consulta)[0])

        self.assertEqual(len(TIPOS_DE_FECHA), len({sin_serie(x) for x in tokens.values()}),
                         "el tipo de fecha llega al token")
        self.assertFalse(pack.verificar_token(tokens["event_date"], ART_00, HOY,
                                              consulta_norma(tipo_de_fecha="decision_date"))[0])


# ── III. La rama B se había quedado sin las correcciones de la A ──

class LaRamaBAlDiaDeLaA(Via):

    def test_A08_la_providencia_tiene_el_mismo_techo_temporal_que_la_norma(self):
        """«N2 cerró la ventana por arriba en A —*el techo es el día de la
        comprobación*— y B no leía `fecha_del_caso` en ninguna línea»: un
        precedente firmado hace un mes se servía para un caso fechado
        cincuenta años después de la firma. La jurisprudencia cambia por el
        mismo eje por el que cambia la vigencia.

        No hay suelo, y la ausencia es una decisión: un precedente gobierna
        hechos anteriores a él con toda normalidad. Ponerle suelo exigiría
        saber cuándo se dictó la providencia, y ese campo no existe en `01`
        §4; inventarlo sería el pack produciendo derecho."""
        p = ficha_providencia()          # firmada hace un mes
        for cuando in (meses(1), meses(600)):
            self.assertEqual("FUERA_DE_LA_VIGENCIA_COMPROBADA",
                             self.no_sale_citable(p, consulta_providencia(fecha_del_caso=cuando)),
                             "caso %s, firma de %s" % (cuando, meses(-1)))

        # La rama A contesta lo mismo para la misma fecha: ya no hay asimetría.
        self.assertEqual("FUERA_DE_LA_VIGENCIA_COMPROBADA",
                         self.no_sale_citable(ficha_norma(), consulta_norma(fecha_del_caso=meses(600))))

        # Una fecha con la que no se pueden hacer cuentas no es una fecha.
        for imposible in ("9999-12-31", "0001-01-01"):
            self.assertEqual("EL_PACK_NO_CONTESTA",
                             self.no_sale_citable(p, consulta_providencia(fecha_del_caso=imposible)))

        # Dentro de la ventana, y hacia atrás, sigue habiendo precedente.
        self.assertEqual("CITABLE_PRECEDENTE",
                         self.codigo(p, consulta_providencia(fecha_del_caso=meses(-2))))
        self.assertEqual("CITABLE_PRECEDENTE",
                         self.codigo(p, consulta_providencia(fecha_del_caso=meses(-600))))


# ── IV. El mismo campo leído de dos maneras distintas ──

class UnSoloLector(Via):

    def test_A09_tipo_se_lee_igual_en_todas_partes(self):
        """«`evaluar` normalizaba `tipo` con `_texto` y `cadencia_de`,
        `_citable_en_si`, `recuento` y `verificar_token` lo comparaban con
        `==` crudo.» Un espacio partía la ficha en dos: para la tabla de
        decisión era una providencia, para el recuento y para la prueba de
        banco era una norma. El recuento que «viaja en CADA respuesta» decía
        cero citables en la respuesta que acababa de servir un citable con
        token, y el token de un precedente se comprobaba contra un alcance de
        norma."""
        p = ficha_providencia(tipo=" providencia ")
        pack = Pack([p], curator=FIRMANTE, version="0.1.0")
        caso = consulta_providencia()
        r = pack.responder(caso, HOY)
        self.assertEqual("CITABLE_PRECEDENTE", r.codigo)
        self.assertEqual(1, r.recuento["citables_hoy"], "sirve un citable y cuenta uno")
        self.assertEqual(0, r.recuento["vigencia_no_comprobada"],
                         "una providencia no es una norma sin vigencia comprobada")

        # La prueba de banco la lee como providencia: acepta su proposición.
        self.assertTrue(pack.verificar_token(r.respuestas[0].token,
                                             "proposicion de ejemplo numero 00", HOY, caso)[0])

        # Y un `alcance_comprobado` de norma dentro de una providencia no
        # ampara un articulado: en una providencia ese campo no se lee.
        q = ficha_providencia(tipo=" providencia ", alcance_comprobado=LEY_ENTERA)
        pack2 = Pack([q], curator=FIRMANTE, version="0.1.0")
        r2 = pack2.responder(caso, HOY)
        self.assertEqual("CITABLE_PRECEDENTE", r2.codigo)
        self.assertFalse(pack2.verificar_token(
            r2.respuestas[0].token,
            {"norma_completa": "no", "articulos": ["cualquier-articulo"], "incisos": []},
            HOY, caso)[0])

        # Y al revés: una norma con un espacio de más sigue contando como
        # norma en el recuento que viaja en cada respuesta.
        floja = ficha_norma(tipo=" norma ", reforma_buscada="no")
        censo = Pack([floja], curator=FIRMANTE).recuento(HOY)
        self.assertEqual(1, censo["vigencia_no_comprobada"])
        self.assertEqual(0, censo["citables_hoy"])

        # Un tipo que no es ninguno de los dos no entra por ninguna rama.
        for basura in ("Norma", "norma ficticia", "", "   ", None, 0, ["norma"]):
            self.assertEqual("NO_TENEMOS_INFORMACION_SUFICIENTE",
                             self.no_sale_citable(ficha_norma(tipo=basura)),
                             "tipo=%r no declara qué es la ficha" % (basura,))

    def test_A10_materia_exige_lista_y_no_se_recorre_letra_a_letra(self):
        """«`leer_alcance` exigía lista y rechazaba la cadena; `cobertura`
        iteraba `materia` sin comprobar nada.» Una `materia` escrita en
        singular —el error de tecleo más barato de la ficha— hacía que el pack
        declarara como materias cubiertas las **letras** del área, y
        `NO_ESTA_EN_EL_PACK` desplazaba a `FUERA_DE_COBERTURA` para consultas
        de una letra."""
        pack = Pack([ficha_norma(materia="civil")], curator=FIRMANTE)
        self.assertEqual([], pack.cobertura(HOY)["materias_declaradas"])
        self.assertEqual("FUERA_DE_COBERTURA",
                         pack.responder(consulta_norma(identificador="LEY-0000-9999",
                                                       materia="c"), HOY).codigo)

        for basura in ("civil", 0, None, [], [""], ["civil", None], "['civil']"):
            roto = Pack([ficha_norma(materia=basura)], curator=FIRMANTE)
            self.assertFalse(roto.responder(consulta_norma(), HOY).citable,
                             "materia=%r no declara ninguna materia" % (basura,))

        # Control positivo: una lista de verdad sí declara sus materias.
        buena = Pack([ficha_norma(materia=["civil", "comercial"])], curator=FIRMANTE)
        self.assertEqual(["civil", "comercial"], buena.cobertura(HOY)["materias_declaradas"])


# ── V. El orden de las comprobaciones y el borde del calendario ──

class ElCalendarioYElCenso(Via):

    def test_A11_una_fecha_imposible_no_tumba_el_pack(self):
        """«*Ninguna función de este archivo levanta una excepción por un dato
        malo: un dato malo es un no.* No era cierto»: `revisar_antes_de` sumaba
        la cadencia sin comprobar el rango del calendario, y `cobertura` y
        `recuento` llamaban a `caducada` antes que a `_firma_valida`. Una sola
        casilla con `9999-01-01` dejaba el pack entero sin responder a nada, ni
        siquiera a las consultas sobre las demás fichas."""
        bomba = ficha_norma(identificador_canonico="LEY-0000-0001", verificado_el="9999-01-01")
        self.assertEqual("FICHA_NO_FIRMADA", self.no_sale_citable(bomba))
        self.assertTrue(caducada(bomba, HOY), "lo que no se puede contar no es una firma")
        self.assertIsNone(revisar_antes_de(bomba))

        # Y una firma futura pero legible tampoco da una ficha viva: `caducada`
        # y la tabla de decisión tienen que contar la misma ficha igual, que es
        # el mismo patrón que A09 en el eje del tiempo.
        manana = ficha_norma(verificado_el=meses(6))
        self.assertEqual("FICHA_NO_FIRMADA", self.no_sale_citable(manana))
        self.assertTrue(caducada(manana, HOY))

        sanas = [ficha_norma()] + [ficha_norma(identificador_canonico="LEY-0000-%04d" % (i + 2))
                                   for i in range(3)]
        pack = Pack(sanas + [bomba], curator=FIRMANTE, version="0.1.0")
        self.assertEqual(4, pack.recuento(HOY)["citables_hoy"])
        self.assertEqual(1, pack.recuento(HOY)["caducados_hoy"])
        self.assertEqual(["area-de-ejemplo"], pack.cobertura(HOY)["materias_declaradas"])
        self.assertFalse(pack.degradado(HOY))
        self.assertFalse(pack.apagado(HOY))
        self.assertEqual("CITABLE", pack.responder(consulta_norma(), HOY).codigo,
                         "la ficha sana, que no tiene nada que ver, sigue respondiendo")

        # El borde del calendario tampoco entra por la puerta de la consulta.
        for imposible in ("9999-12-31", "0001-01-01"):
            self.assertEqual("EL_PACK_NO_CONTESTA",
                             self.no_sale_citable(ficha_norma(),
                                                  consulta_norma(fecha_del_caso=imposible)))

    def test_A12_la_fuente_se_consulto_dentro_de_la_ventana_de_la_ficha(self):
        """«`verificado_el` no puede ser futuro y `consultada` no tenía ningún
        techo ni ningún suelo. `_identidad` recibía `hoy` y no lo usaba en
        ninguna línea, que es la huella de la comprobación que se quiso
        hacer.» Una ficha firmada ayer podía declarar que consultó la fuente
        oficial en el año 9999, o hace un siglo, y salía `CITABLE`: la
        cadencia medía la edad de la firma y nada medía la edad de lo que se
        firmó."""
        publicada = "https://ejemplo.invalido/publicacion"
        for cuando in ("9999-12-31", "0001-01-01", meses(1), meses(1200), meses(-14), meses(-1200)):
            fuente = {"clase": "PRIMARY_OFFICIAL", "referencia": publicada, "consultada": cuando}
            self.assertEqual("IDENTIDAD_POR_VERIFICAR",
                             self.no_sale_citable(ficha_norma(fuente_identidad=fuente)),
                             "consultada=%s cae fuera de la ventana de la ficha" % cuando)
            self.assertEqual("VIGENCIA_NO_COMPROBADA",
                             self.no_sale_citable(ficha_norma(fuente_vigencia=dict(fuente))))

        # Los dos bordes son inclusivos: la firma menos la cadencia, y hoy.
        for borde in (meses(-13), meses(-1), HOY.isoformat()):
            fuente = {"clase": "PRIMARY_OFFICIAL", "referencia": publicada, "consultada": borde}
            self.assertEqual("CITABLE", self.codigo(ficha_norma(fuente_identidad=fuente)),
                             "consultada=%s está dentro de la ventana" % borde)

    def test_A13_el_apagado_mide_si_el_pack_sirve_y_no_la_edad_de_las_firmas(self):
        """«N7 cambió `max` por mediana, y el escenario literal de la crítica
        —*veinticinco fichas podridas dentro*— volvía a montarse bajando 20
        meses a 17»: la mediana quedaba por debajo del umbral de 18, el
        interruptor no saltaba y el pack respondía `CITABLE` con 25 de sus 26
        fichas caducadas. `degradado` sí lo veía, y no gobernaba nada: era un
        booleano que viajaba al lado de una respuesta citable."""
        podridas = [ficha_norma(identificador_canonico="LEY-0000-%04d" % (i + 1),
                                verificado_el=meses(-17),
                                estado_vigencia="VIGENTE_AL " + meses(-17))
                    for i in range(25)]
        pack = Pack(podridas + [ficha_norma()], curator=FIRMANTE, version="0.1.0")

        self.assertTrue(all(caducada(f, HOY) for f in podridas), "las 25 están caducadas")
        self.assertTrue(pack.degradado(HOY))
        self.assertTrue(pack.apagado(HOY), "y ahora el interruptor salta")

        r = pack.responder(consulta_norma(), HOY)
        self.assertFalse(r.citable)
        self.assertEqual("NO_TENEMOS_INFORMACION_SUFICIENTE", r.codigo)
        self.assertTrue(r.apagado)
        self.assertIsNone(r.respuestas[0].token)

        # Y no está siempre puesto: un pack mantenido responde.
        self.assertFalse(Pack([ficha_norma()], curator=FIRMANTE).apagado(HOY))

    def test_A14_el_censo_cuenta_las_fichas_que_no_se_saben_fechar(self):
        """«La mediana se calculaba sobre las firmas legibles: cualquier ficha
        cuya fecha no se pudiera leer desaparecía del censo en vez de contar
        como la más vieja.» Cien fichas sin firma y una recién hecha daban un
        pack encendido cuya mediana era la de una sola ficha."""
        mudas = [ficha_norma(identificador_canonico="LEY-0001-%04d" % i, verificado_el="")
                 for i in range(100)]
        pack = Pack(mudas + [ficha_norma()], curator=FIRMANTE)

        self.assertEqual(100, pack.recuento(HOY)["caducados_hoy"],
                         "una firma ilegible no desaparece del censo")
        self.assertEqual(1, pack.recuento(HOY)["citables_hoy"])
        self.assertTrue(pack.apagado(HOY))
        self.assertFalse(pack.responder(consulta_norma(), HOY).citable)


# ── VI. Lo que la respuesta afirma sobre el mundo ──

class LaFraseServida(Via):

    def test_A15_citable_sin_vigencia_hoy_solo_se_dice_si_se_comprobo(self):
        """«`SIN_VIGENCIA_DESDE` con fecha futura es la forma normal de una
        derogatoria de vigencia diferida. Nada exigía que la fecha del estado
        fuera pasada, y la frase de `CITABLE_SIN_VIGENCIA_HOY` dice, literal,
        *Hoy no rige* —de una norma que la propia ficha declara vigente hasta
        dentro de cinco años—.» Es la única frase del contrato que afirma algo
        sobre el mundo, y el algoritmo no comprobaba la afirmación.

        Se elige comprobarla antes de decirla, no callarla: la cesación que
        todavía no ocurrió deja lo comprobado en `CITABLE` —que no afirma nada
        de hoy— con la nota obligatoria transcrita."""
        futura = ficha_norma(estado_vigencia="SIN_VIGENCIA_DESDE " + meses(60),
                             vigencia_desde=meses(-120))
        self.assertEqual("FICHA_INCOMPLETA", self.no_sale_citable(futura),
                         "una cesación anunciada sin nota es una ficha incompleta")

        con_nota = ficha_norma(estado_vigencia="SIN_VIGENCIA_DESDE " + meses(60),
                               vigencia_desde=meses(-120),
                               nota_de_vigencia="cesacion anunciada, no consumada al firmar")
        r = evaluar(con_nota, consulta_norma(), HOY)
        self.assertEqual("CITABLE", r.codigo)
        self.assertNotIn("Hoy no rige", r.frase)
        self.assertEqual("cesacion anunciada, no consumada al firmar", r.nota)
        self.assertEqual(3, cadencia_de(con_nota), "un cambio con fecha futura acorta la cadencia")

        # Y la cesación ya ocurrida sí se dice, porque ahí sí se comprobó.
        pasada = ficha_norma(estado_vigencia="SIN_VIGENCIA_DESDE " + meses(-24),
                             vigencia_desde=meses(-120))
        r2 = evaluar(pasada, consulta_norma(fecha_del_caso=meses(-36)), HOY)
        self.assertEqual("CITABLE_SIN_VIGENCIA_HOY", r2.codigo)
        self.assertIn("Hoy no rige", r2.frase)
        self.assertEqual(12, cadencia_de(pasada))

    def test_A16_el_codigo_de_composicion_tiene_como_decir_su_frase(self):
        """«*La frase importa tanto como el código: el silencio se lee como no
        hay regla, y esa lectura es el fallo que el pack existe para
        impedir.*» El código de composición era una cadena suelta en
        `RespuestaCompuesta`, que no construía ninguna `Respuesta` y no tenía
        atributo `frase`: la de `CONFLICTO_ENTRE_FICHAS` estaba escrita en
        `FRASES` y no había camino que la sirviera. Se servían las dos frases
        individuales, y una de ellas decía `CITABLE`."""
        una = ficha_norma(alcance_comprobado=ART_00)
        otra = ficha_norma(alcance_comprobado=ART_00, estado_vigencia="VIGENCIA_NO_COMPROBADA")
        r = Pack([una, otra], curator=FIRMANTE).responder(consulta_norma(), HOY)

        self.assertEqual("CONFLICTO_ENTRE_FICHAS", r.codigo)
        self.assertIn("discrepan en la vigencia comprobada", r.frase)
        self.assertIn("LEY-0000-0000", r.frase)

        # Con una sola respuesta, la frase compuesta es la de esa respuesta.
        sola = Pack([ficha_norma()], curator=FIRMANTE).responder(consulta_norma(), HOY)
        self.assertEqual(sola.respuestas[0].frase, sola.frase)


# ── VII. La lista negra que había dentro de la lista blanca ──

class ListaBlancaHastaElFinal(Via):

    def test_A17_la_referencia_se_acepta_por_lo_que_es_no_se_rechaza_por_lo_que_parece(self):
        """«Todo el contrato era lista blanca menos esta función, que decidía
        si una referencia era del corpus buscando seis subcadenas. Quitar la
        extensión, usar la barra de Windows o nombrar el archivo de otra
        manera desactivaba N1 entero.» Una lista negra deja fuera lo que no se
        pensó, y lo que no se pensó es infinito.

        El coste de la lista blanca es real y se acepta a sabiendas: una
        referencia legítima que no sea una URL —el ejemplar en papel de un
        diario oficial— se rechaza y obliga a rehacer la ficha."""
        disfrazadas = (
            "01-ficha-y-verificacion",                       # sin extensión
            "temporal-law-matrix, fila 9",
            "docs\\fichas\\catalogo-normativo.txt",          # barra de Windows
            "C:\\Users\\HITMA\\Desktop\\corpus\\normative-sources.txt",
            "normative-sources.markdown",                    # otra extensión
            "ver la ficha anterior",                         # ni siquiera un archivo
            "consultado internamente",
            "ejemplo.invalido/publicacion",                  # sin esquema
            "https:/ejemplo.invalido/publicacion",           # esquema a medias
            "https://localhost/publicacion",                 # sin dominio
            "https://ejemplo.invalido/../docs/catalogo",     # subiendo al corpus
        )
        for referencia in disfrazadas:
            fuente = {"clase": "PRIMARY_OFFICIAL", "referencia": referencia,
                      "consultada": meses(-1)}
            self.assertEqual("IDENTIDAD_POR_VERIFICAR",
                             self.no_sale_citable(ficha_norma(fuente_identidad=fuente)),
                             "referencia=%r no es una fuente publicada" % (referencia,))
            self.assertEqual("VIGENCIA_NO_COMPROBADA",
                             self.no_sale_citable(ficha_norma(fuente_vigencia=dict(fuente))))

        # Lo que se acepta se enumera, y se acepta.
        for publicada in ("https://ejemplo.invalido/publicacion",
                          "http://ejemplo.invalido/serie/00?art=00"):
            fuente = {"clase": "PRIMARY_OFFICIAL", "referencia": publicada,
                      "consultada": meses(-1)}
            self.assertEqual("CITABLE",
                             self.codigo(ficha_norma(fuente_identidad=fuente,
                                                     fuente_vigencia=dict(fuente))))


# ── VIII. Condiciones que no se alcanzaban ──

class SinCodigoMuerto(Via):

    def test_A18_la_nota_obligatoria_de_vigencia_parcial_se_exige(self):
        """«`ESTADOS_QUE_OBLIGAN_NOTA` tenía dos miembros y el segundo,
        `VIGENCIA_PARCIAL_AL`, retornaba cuatro líneas antes de que se
        comprobara la nota: la mitad de esa constante era inalcanzable.» No
        abría una cita —parcial nunca es citable— pero decidía la cadencia:
        una ficha de vigencia parcial sin la nota que su estado obliga vivía
        doce meses en vez de tres, y alimentaba `cobertura` y `recuento` como
        cualquier otra. La cadencia cuelga de la obligación, no de que alguien
        se acordara de llenar la casilla."""
        parcial = ficha_norma(estado_vigencia="VIGENCIA_PARCIAL_AL " + meses(-1),
                              nota_de_vigencia="")
        self.assertEqual("FICHA_INCOMPLETA", self.no_sale_citable(parcial))
        self.assertEqual(3, cadencia_de(parcial))

        con_nota = ficha_norma(estado_vigencia="VIGENCIA_PARCIAL_AL " + meses(-1),
                               nota_de_vigencia="rige en parte")
        self.assertEqual(3, cadencia_de(con_nota))
        self.assertEqual("VIGENCIA_PARCIAL", self.no_sale_citable(con_nota))

        # Una ficha que nunca se sirve no declara cobertura de nada.
        for ficha in (parcial, con_nota):
            self.assertEqual([], Pack([ficha], curator=FIRMANTE)
                             .cobertura(HOY)["materias_declaradas"])

        # Control positivo: la nota obligatoria del otro estado sigue abriendo.
        reformada = ficha_norma(estado_vigencia="VIGENTE_CON_REFORMA_AL " + meses(-1),
                                nota_de_vigencia="consta reforma dentro del alcance")
        self.assertEqual("CITABLE_CON_REFORMA", self.codigo(reformada))
        self.assertEqual(["area-de-ejemplo"], Pack([reformada], curator=FIRMANTE)
                         .cobertura(HOY)["materias_declaradas"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
