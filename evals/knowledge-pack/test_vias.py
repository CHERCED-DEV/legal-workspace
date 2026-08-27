# -*- coding: utf-8 -*-
"""
Un test por vía. Cada uno **intenta colarse** y falla si lo consigue.

Las dos críticas de `docs/knowledge-pack/` son la especificación de este
archivo: cinco vías originales (V1-V5) y siete que abrió la corrección
(N1-N8), más los cinco campos que la prosa dice leer y no lee. Nada más entra
aquí: un test que no corresponda a una vía o a un campo de las críticas sobra.

La única excepción, y es deliberada, es `test_control_positivo`. Sin él, un
contrato que contestara «no» a todo pasaría los dieciocho tests restantes con
nota perfecta. El control positivo es lo que obliga a que las negativas
signifiquen algo.

    cd evals/knowledge-pack && python -m unittest -v

Sin dependencias externas: `unittest` de la biblioteca estándar, porque esto
tiene que correr en la máquina de cualquiera.
"""

import os
import sys
import unittest
from datetime import date, timedelta

# El directorio tiene un guion en el nombre y no es un paquete importable.
# Esto permite lanzar la suite desde la raíz del repositorio
# (`python -m unittest discover -s evals/knowledge-pack`) igual que desde aquí.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from contrato import Pack, evaluar, mas_meses, revisar_antes_de   # noqa: E402
from fichas import (HOY, FIRMANTE, consulta_norma, consulta_providencia,     # noqa: E402
                    ficha_norma, ficha_providencia, meses, sin)


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
        inventado junto a una cita inventada las pasaba las cuatro."""
        pack = Pack([ficha_norma()], curator=FIRMANTE, version="0.1.0")
        citado = {"norma_completa": "no", "articulos": ["00"], "incisos": []}

        servida = pack.responder(consulta_norma(), HOY)
        token = servida.respuestas[0].token
        self.assertTrue(pack.verificar_token(token, citado, HOY)[0],
                        "el token realmente servido tiene que resolver")

        # 1. cita sin token
        for nada in (None, "", "   "):
            self.assertFalse(pack.verificar_token(nada, citado, HOY)[0])

        # 2. token plausible escrito a mano, con la huella correcta del pack y
        #    una serie que nunca se emitió
        inventado = ("CITABLE · LEY-0000-0000 + {norma_completa: no, articulos: [00], "
                     "incisos: []} · %s · %s · pack:0.1.0@%s · serie:0123456789abcdef"
                     % (meses(-1), HOY.isoformat(), pack.checksum()))
        self.assertFalse(pack.verificar_token(inventado, citado, HOY)[0])

        # 3. token real manipulado: la serie existe, la cadena ya no es la que
        #    se sirvió
        self.assertFalse(pack.verificar_token(
            token.replace("CITABLE", "CITABLE_CON_REFORMA", 1), citado, HOY)[0])

        # 4. token real, cita más ancha que el alcance que ampara
        self.assertFalse(pack.verificar_token(
            token, {"norma_completa": "si", "articulos": [], "incisos": []}, HOY)[0])

        # 5. token real, ficha ya caducada el día en que se comprueba
        self.assertFalse(pack.verificar_token(token, citado, mas_meses(HOY, 24))[0])

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
