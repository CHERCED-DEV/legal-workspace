# -*- coding: utf-8 -*-
"""
El adversario, **segunda ronda**. Diez vías, y las diez pasan.

La convención es al revés que en todas partes: **si el test pasa, la vía está
abierta**. Cada uno intenta colar una cita falsa —o tumbar el pack, o hacerle
afirmar lo que no comprobó— y tiene éxito cuando hay un agujero. Ninguno
corrige nada; todos documentan. Este archivo en verde es la lista de vías
abiertas, contadas y reproducibles.

EL CICLO, que es lo único que hay que saber para usar esto:

  1. Se ataca `contrato.py` por donde la ronda anterior no miró y se escribe
     un test por cada agujero, **redactado para pasar**.
  2. Se cierran en `contrato.py`. Se arregla el código, nunca el test: si un
     ataque describe una conducta que en realidad es correcta, eso se dice y
     se razona, no se ablanda en silencio.
  3. Cada ataque cerrado se reescribe afirmando la conducta correcta y se
     **muda a `test_vias.py`** con su prefijo. Este archivo vuelve a quedar
     vacío y aquel sube: 19 tras las dos críticas en prosa, 37 tras la primera
     ronda adversaria, 47 cuando estas diez se cierren.

POR DÓNDE ENTRÓ ESTA RONDA, porque el patrón vale más que la lista y la
primera ronda ya había tapado sus cuatro puertas —el token al portador, el
orden de las comprobaciones, los campos que nadie compara y el borde del
calendario—:

  - **La prueba de banco quedó por detrás de la respuesta.** A01-A07 pusieron
    el token bajo la composición y le metieron dentro la fecha del caso, pero
    `verificar_token` sigue sin mirar dos cosas que `responder` sí mira: la
    materia y el nivel territorial de la consulta (B01), y si el pack sigue
    encendido el día en que se cita (B02). El «no» vive en `responder` y el
    «sí» en el token, y el token es lo único que llega a la publicación.
  - **Las guardas nuevas comparten supuesto.** `cadencia_de` gobierna la
    caducidad Y la ventana de `leer_fuente` (A12) Y el censo, así que la
    corrección de A18 —«la cadencia cuelga de la obligación, no de la
    casilla»— se quedó a medias y borrar una casilla voluntaria vuelve a
    ensanchar lo que se acepta (B04). `_composicion` y `_citable_en_si`
    heredan el mismo defecto por otro lado: las dos deciden con una llave más
    estrecha que la pregunta que contestan (B03, B05).
  - **Lo que la respuesta publica no es lo que la respuesta comprueba.**
    `cobertura` declara una jurisdicción y un nivel territorial que ningún
    camino compara (B07), la nota obligatoria que A15 dejó como única señal de
    una cesación anunciada no llega a la frase servida (B08), y una consulta
    incompleta devuelve el recuento vacío y `apagado=False` de un pack apagado
    (B09).
  - **Las dos listas blancas que quedaron sin cerrar del todo.** La
    referencia publicada acepta la máquina de quien escribe la ficha (B06), y
    `hoy` es la única fecha del contrato que no pasa por `_fecha` (B10).

    cd evals/knowledge-pack && python -m unittest test_ataque -v

Con las mismas fichas de ejemplo de `fichas.py`: aquí tampoco hay derecho.
"""

import os
import sys
import unittest
from datetime import date, datetime

# El directorio tiene un guion en el nombre y no es un paquete importable.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from contrato import (Pack, cadencia_de, caducada, evaluar,      # noqa: E402
                      mas_meses, _referencia_publicada)
from fichas import (HOY, FIRMANTE, consulta_norma, ficha_norma,  # noqa: E402
                    meses)

ART_00 = {"norma_completa": "no", "articulos": ["00"], "incisos": []}
ART_00_Y_01 = {"norma_completa": "no", "articulos": ["00", "01"], "incisos": []}
PUBLICADA = "https://ejemplo.invalido/diario-oficial"


class Ataque(unittest.TestCase):
    """Base común. `pack()` arma un pack con versión, que es lo que el token
    exhibe en su huella."""

    def pack(self, *fichas):
        return Pack(list(fichas), curator=FIRMANTE, version="0.1.0")

    def token_de(self, pack, consulta, hoy=HOY):
        r = pack.responder(consulta, hoy)
        self.assertTrue(r.citable, "el control positivo del ataque no es citable: %s" % r.codigos)
        return r.respuestas[0].token


# ── I. La prueba de banco se quedó por detrás de la respuesta ──

class ElTokenNoSabeLoQueLaRespuestaSabia(Ataque):

    def test_B01_el_token_no_registra_ni_la_materia_ni_el_nivel_territorial(self):
        """A03 y A07 metieron dentro del token la fecha del caso y su tipo
        —«quien cita tiene que decir para qué cita»— y dejaron fuera los otros
        dos ejes de la misma consulta. A06 había establecido justo antes que
        `materia` y `territorial` se miran SIEMPRE, y no solo cuando el pack
        no tiene la ficha.

        El resultado es que las dos comprobaciones de A06 se evaporan en la
        última puerta, que es la única que llega a la publicación: `responder`
        dice `FUERA_DEL_ALCANCE_COMPROBADO` a la consulta en materia ajena y
        `FUERA_DE_COBERTURA` a la territorial, y `verificar_token` acepta un
        token pedido en la materia buena para respaldar una cita que declara
        exactamente esas dos consultas negadas. `caso` llega entero a la
        función y de él solo se leen dos claves de cinco.

        DEBERÍA FALLAR: el token tendría que registrar la materia y el nivel
        territorial con que se pidió, y `verificar_token` compararlos, igual
        que ya compara la fecha del caso.
        """
        p = self.pack(ficha_norma())
        buena = consulta_norma()
        token = self.token_de(p, buena)

        ajena = consulta_norma(materia="derecho-espacial-lunar")
        territorial = consulta_norma(territorial=True)

        # Lo que el pack contesta a esas dos consultas.
        self.assertEqual("FUERA_DEL_ALCANCE_COMPROBADO", p.responder(ajena, HOY).codigo)
        self.assertEqual("FUERA_DE_COBERTURA", p.responder(territorial, HOY).codigo)

        # Y lo que la prueba de banco dice de una cita hecha PARA esas
        # consultas, con el token pedido para otra.
        self.assertEqual((True, "el token resuelve contra una respuesta servida"),
                         p.verificar_token(token, ART_00, HOY, ajena))
        self.assertEqual((True, "el token resuelve contra una respuesta servida"),
                         p.verificar_token(token, ART_00, HOY, territorial))
        # Ni siquiera hace falta declarar materia: el caso puede no traerla.
        self.assertTrue(p.verificar_token(token, ART_00, HOY,
                                          {"fecha_del_caso": meses(-2),
                                           "tipo_de_fecha": "procedural_start_date"})[0])

        # Control: la mitad que A03 y A07 SÍ cerraron sigue cerrada, y por eso
        # esta vía es la otra mitad de la misma condición.
        self.assertFalse(p.verificar_token(token, ART_00, HOY,
                                           consulta_norma(fecha_del_caso=meses(-3)))[0])
        self.assertFalse(p.verificar_token(token, ART_00, HOY,
                                           consulta_norma(tipo_de_fecha="event_date"))[0])

    def test_B02_el_token_sobrevive_al_apagado_del_pack(self):
        """A13 y A14 hicieron que `degradado` gobierne: «un aviso pegado a un
        sí es un aviso que nadie lee», así que el pack degradado se apaga y
        deja de responder afirmativamente «ni siquiera con una ficha impecable
        dentro». `verificar_token` no consulta `apagado` ni `degradado` en
        ninguna línea.

        Y el apagado no necesita que nadie toque el pack: `degradado` es
        `caducados·3 > citables` y bascula **solo con el calendario**, sin
        cambiar una ficha, o sea sin mover la huella que A04 sí comprueba. La
        misma ficha impecable, el mismo token, el mismo pack: dos meses
        después el pack contesta `NO_TENEMOS_INFORMACION_SUFICIENTE` a
        cualquiera que pregunte, y la prueba de banco sigue validando la cita
        que salió de él.

        DEBERÍA FALLAR: un token de un pack apagado no puede pasar la prueba
        de banco. El pack que no responde tampoco respalda.
        """
        despues = mas_meses(HOY, 2)
        impecable = ficha_norma(identificador_canonico="LEY-0000-0001", verificado_el=meses(0))
        # Tres fichas sanas hoy que caducan dentro de un mes: la firma es de
        # hace once y la cadencia larga son doce.
        vencederas = [ficha_norma(identificador_canonico="LEY-0000-000%d" % i,
                                  verificado_el=meses(-11),
                                  estado_vigencia="VIGENTE_AL " + meses(-11))
                      for i in (2, 3, 4)]
        p = self.pack(impecable, *vencederas)
        consulta = consulta_norma(identificador="LEY-0000-0001")

        self.assertFalse(p.apagado(HOY))
        token = self.token_de(p, consulta)

        # Dos meses después, sin tocar una sola casilla del pack.
        self.assertTrue(all(caducada(f, despues) for f in vencederas))
        self.assertTrue(p.degradado(despues))
        self.assertTrue(p.apagado(despues))
        self.assertFalse(caducada(impecable, despues), "la ficha del token sigue viva")

        r = p.responder(consulta, despues)
        self.assertEqual("NO_TENEMOS_INFORMACION_SUFICIENTE", r.codigo)
        self.assertTrue(r.apagado)
        self.assertIsNone(r.respuestas[0].token, "apagado no entrega tokens nuevos")

        # Y el que entregó cuando estaba encendido sigue valiendo.
        self.assertEqual((True, "el token resuelve contra una respuesta servida"),
                         p.verificar_token(token, ART_00, despues, consulta))


# ── II. Dos llaves más estrechas que la pregunta que contestan ──

class LaLlaveEquivocada(Ataque):

    def test_B03_la_composicion_solo_ve_el_conflicto_si_el_alcance_es_identico(self):
        """N4 dio código propio al conflicto de vigencia entre fichas y A02
        colgó el token de esa composición. La llave es
        `(identificador, alcance_comprobado)` comparada por **igualdad exacta
        de tuplas**, y la pregunta que hay que contestar no es esa: es si dos
        fichas que **cubren lo que se pide** discrepan.

        P2 empuja a estrechar, así que la forma normal del pack es varias
        fichas por norma con alcances distintos y solapados. Dos que cubren el
        art. 00 —una comprobada solo para él, otra para él y el 01— y que
        discrepan en si la norma sigue rigiendo tienen llaves distintas, no
        hay conflicto, las dos son citables, el conjunto es citable y salen
        **dos tokens**. Las dos frases servidas juntas dicen «vigente dentro
        del alcance y de la ventana comprobadas» y «Hoy no rige» del mismo
        identificador y del mismo artículo, y el consumidor elige: que es
        exactamente la lectura que N5 descartó.

        DEBERÍA FALLAR: la llave tiene que ser la petición, no el alcance
        declarado. Dos fichas cuyos alcances contienen ambas lo que se pide y
        cuyos estados de vigencia difieren son `CONFLICTO_ENTRE_FICHAS`.
        """
        estrecha = ficha_norma(alcance_comprobado=ART_00)
        ancha = ficha_norma(alcance_comprobado=ART_00_Y_01,
                            estado_vigencia="SIN_VIGENCIA_DESDE " + meses(-1),
                            vigencia_desde=meses(-120))
        r = self.pack(estrecha, ancha).responder(consulta_norma(), HOY)

        self.assertEqual(["CITABLE", "CITABLE_SIN_VIGENCIA_HOY"], r.codigos)
        self.assertIsNone(r.codigo_de_composicion, "no se detecta el conflicto")
        self.assertTrue(r.citable, "el conjunto sale citable")
        self.assertTrue(all(x.token for x in r.respuestas), "y con un token cada una")

        # Las dos afirmaciones contradictorias, servidas juntas.
        self.assertIn("vigente dentro del alcance", r.frase)
        self.assertIn("Hoy no rige", r.frase)

        # Control: con el alcance escrito igual sí se detecta. La diferencia
        # entre las dos llamadas es una lista de artículos, no el conflicto.
        misma_llave = self.pack(estrecha, ficha_norma(
            alcance_comprobado=ART_00,
            estado_vigencia="SIN_VIGENCIA_DESDE " + meses(-1),
            vigencia_desde=meses(-120))).responder(consulta_norma(), HOY)
        self.assertEqual("CONFLICTO_ENTRE_FICHAS", misma_llave.codigo)

    def test_B05_el_censo_cuenta_como_citables_fichas_que_nunca_se_sirven(self):
        """`_citable_en_si` dice de sí misma por qué excluye la ficha sin
        materias legibles: «no hay ninguna consulta que pueda casar con ella,
        de modo que contarla sería contar una ficha que nunca se va a servir»,
        y A18 lo asentó como principio —«una ficha que nunca se sirve no
        declara cobertura de nada»—. El razonamiento se aplicó a `materia` y
        no a los otros dos campos que tienen exactamente la misma propiedad:
        `alcance_comprobado` ilegible hace que `contenido_en` sea siempre
        False, y `vigencia_desde` ilegible hace que A.6 corte siempre. Ninguno
        de los dos depende de la consulta, y ninguno de los dos se mira.

        La consecuencia no es de precisión, es de seguridad, porque el censo
        es el que gobierna: `citables_hoy` es el denominador de `degradado`, y
        `degradado` es el interruptor. **Tres fichas que no se pueden servir
        jamás encienden un pack que sin ellas estaría apagado**, y de paso
        declaran cubierta un área en la que el pack no puede contestar nada.

        DEBERÍA FALLAR: `_citable_en_si` tiene que exigir también que
        `leer_alcance(alcance_comprobado)` y `_fecha(vigencia_desde)` se
        puedan leer, por el mismo motivo por el que ya exige las materias.
        """
        caducada_ = ficha_norma(identificador_canonico="LEY-0000-0009",
                                verificado_el=meses(-14))
        # Un pack con esa sola ficha está degradado y apagado.
        self.assertTrue(self.pack(caducada_).apagado(HOY))

        inservibles = [ficha_norma(identificador_canonico="LEY-0000-000%d" % i,
                                   alcance_comprobado="toda la ley, segun consta")
                       for i in (1, 2, 3)]
        p = self.pack(caducada_, *inservibles)

        self.assertEqual(3, p.recuento(HOY)["citables_hoy"])
        self.assertFalse(p.degradado(HOY), "las tres inservibles sostienen el denominador")
        self.assertFalse(p.apagado(HOY), "y encienden un pack que estaba apagado")
        self.assertEqual(["area-de-ejemplo"], p.cobertura(HOY)["materias_declaradas"])

        # Ninguna de las tres se puede servir, hoy ni nunca.
        for f in inservibles:
            r = p.responder(consulta_norma(identificador=f["identificador_canonico"]), HOY)
            self.assertEqual("FUERA_DEL_ALCANCE_COMPROBADO", r.codigo)
            self.assertFalse(r.citable)

        # Y el pack promete lo que no puede cumplir a quien pregunta por otra.
        ausente = p.responder(consulta_norma(identificador="LEY-0000-7777"), HOY)
        self.assertEqual("NO_ESTA_EN_EL_PACK", ausente.codigo)
        self.assertIn("El pack cubre esta área", ausente.frase)

        # `vigencia_desde` ilegible cuenta igual, y es el mismo agujero.
        escalonadas = [ficha_norma(identificador_canonico="LEY-0000-010%d" % i,
                                   vigencia_desde="ESCALONADA") for i in (1, 2, 3)]
        p2 = self.pack(caducada_, *escalonadas)
        self.assertEqual(3, p2.recuento(HOY)["citables_hoy"])
        self.assertFalse(p2.apagado(HOY))

        # Control: la exclusión que sí está escrita funciona. La diferencia
        # entre este bloque y los dos de arriba es qué campo se rompió.
        self.assertEqual(0, self.pack(ficha_norma(materia="area-de-ejemplo"))
                         .recuento(HOY)["citables_hoy"])


# ── III. La cadencia gobierna tres cosas y solo se corrigió una ──

class LasGuardasQueCompartenLaCadencia(Ataque):

    def test_B04_borrar_una_nota_voluntaria_ensancha_lo_que_se_acepta(self):
        """A18 corrigió `cadencia_de` para que «se pregunte por la obligación,
        que es un hecho del estado, y no por la casilla, que es un hecho de
        quien la llenó», porque «la ficha peor llenada era la que más vivía».
        El código quedó preguntando por las dos: `obliga_nota(ficha) or
        _texto(ficha.get("nota_de_vigencia"))`. Con la obligación bastaba; el
        `or` deja la casilla mandando en el caso simétrico, la nota
        **voluntaria** en un estado que no la obliga.

        Y no es solo la caducidad: A12 colgó de la misma cadencia el suelo de
        la ventana de consulta de las fuentes. Así que una ficha con una
        observación escrita a mano tiene ventana de tres meses y sin ella de
        doce, y **borrar la observación convierte un no en un sí**. La ficha
        que dice menos es la que se acepta.

        DEBERÍA FALLAR: quitar información de una ficha no puede ensanchar lo
        que el contrato acepta de ella. La cadencia tiene que colgar solo de
        `obliga_nota`, como su propio docstring dice que hace.
        """
        vieja = {"clase": "PRIMARY_OFFICIAL", "referencia": PUBLICADA,
                 "consultada": meses(-10)}
        con_nota = ficha_norma(fuente_vigencia=dict(vieja),
                               nota_de_vigencia="observacion voluntaria: sin nada pendiente")
        sin_nota = ficha_norma(fuente_vigencia=dict(vieja))

        self.assertEqual(3, cadencia_de(con_nota))
        self.assertEqual(12, cadencia_de(sin_nota))
        self.assertFalse(caducada(con_nota, HOY), "no es que caduque: es la ventana")

        self.assertEqual("VIGENCIA_NO_COMPROBADA",
                         evaluar(con_nota, consulta_norma(), HOY).codigo)
        self.assertEqual("CITABLE",
                         evaluar(sin_nota, consulta_norma(), HOY).codigo)

        # Lo mismo por la puerta de la identidad, que comparte ventana.
        con_nota_id = ficha_norma(fuente_identidad=dict(vieja),
                                  nota_de_vigencia="observacion voluntaria")
        self.assertEqual("IDENTIDAD_POR_VERIFICAR",
                         evaluar(con_nota_id, consulta_norma(), HOY).codigo)
        self.assertEqual("CITABLE",
                         evaluar(ficha_norma(fuente_identidad=dict(vieja)),
                                 consulta_norma(), HOY).codigo)


# ── IV. La otra grieta de la lista blanca de A17 ──

class LaListaBlancaTieneSuPropiaGrieta(Ataque):

    def test_B06_una_referencia_a_la_maquina_de_uno_pasa_por_publicada(self):
        """A17 cambió la lista negra de seis subcadenas por una lista blanca
        que responde a la pregunta «¿la referencia señala algo publicado
        **fuera de este proyecto**?» con un esquema y un dominio con punto. El
        `https://localhost/publicacion` de su propia suite lo rechaza por
        accidente —`localhost` no lleva punto—, no porque la función sepa lo
        que es. Basta el bucle local escrito con números, el nombre largo de
        la misma máquina, o cualquier dirección privada, y el archivo del
        corpus servido por un `python -m http.server` es una fuente
        «publicada».

        Eso reabre N1 entero: el mecanismo era «mover una afirmación de un
        archivo del corpus a una ficha no la comprueba», y la lista blanca
        vuelve a dejar que el archivo del corpus sea la fuente con solo
        servirlo por http desde el mismo portátil donde se escribe la ficha.

        DEBERÍA FALLAR: un dominio que resuelve a la propia máquina o a una
        red privada no es una publicación. La lista blanca tiene que exigir un
        nombre de dominio —no un literal IP, no un bucle local—.
        """
        caseras = ("http://127.0.0.1:8000/docs/knowledge-pack/01-fichas-normativas.md",
                   "https://localhost.localdomain/docs/catalogo-normativo",
                   "http://192.168.0.10/corpus/normative-sources.txt",
                   "http://0.0.0.0/corpus/temporal-law-matrix")
        for referencia in caseras:
            self.assertTrue(_referencia_publicada(referencia), referencia)
            fuente = {"clase": "PRIMARY_OFFICIAL", "referencia": referencia,
                      "consultada": meses(-1)}
            self.assertEqual("CITABLE",
                             evaluar(ficha_norma(fuente_identidad=dict(fuente),
                                                 fuente_vigencia=dict(fuente)),
                                     consulta_norma(), HOY).codigo,
                             "referencia=%r pasa por publicada" % (referencia,))

        # Control: lo que A17 sí rechaza lo rechaza por no llevar punto, no
        # por ser la máquina de uno. Las dos referencias siguientes apuntan al
        # mismo sitio y el contrato las trata al revés.
        self.assertFalse(_referencia_publicada("https://localhost/publicacion"))
        self.assertTrue(_referencia_publicada("https://localhost.localdomain/publicacion"))


# ── V. Lo que la respuesta publica y lo que la respuesta comprueba ──

class LoPublicadoYLoComprobado(Ataque):

    def test_B07_la_cobertura_declara_dos_ejes_que_ningun_camino_compara(self):
        """A06 cerró `materia` y `territorial` con el argumento de que «el
        campo se añadió y no se comparaba con nada». `cobertura` devuelve, en
        cada respuesta, tres ejes: `jurisdiccion`, `nivel_territorial` y
        `materias_declaradas`. Se compara el tercero. `jurisdiccion` está
        escrito a mano —`"colombia"`, la misma cadena tenga el pack las fichas
        que tenga— y ningún camino lee `consulta.get("jurisdiccion")`.

        Y el nivel territorial se publica con un nombre y se lee con otro:
        `cobertura` dice `nivel_territorial` y `responder` pregunta por
        `territorial`. Quien consume el manifiesto y escribe en la consulta el
        nombre que el manifiesto le enseñó no está declarando nada: su campo
        se ignora en silencio y el pack contesta como si la consulta fuera
        nacional. La frase de `FUERA_DE_COBERTURA` enumera tres ejes —«esta
        área, este nivel territorial o esta fecha»— y el contrato solo sabe
        decir que no por uno.

        DEBERÍA FALLAR: o los ejes que se publican se comparan, o no se
        publican. Y el nombre tiene que ser uno solo.
        """
        p = self.pack(ficha_norma())
        self.assertEqual("colombia", p.cobertura(HOY)["jurisdiccion"])
        self.assertEqual(["nacional"], p.cobertura(HOY)["nivel_territorial"])

        for ajena in ({"jurisdiccion": "peru"},
                      {"jurisdiccion": "otra-jurisdiccion-cualquiera"},
                      {"nivel_territorial": "municipal"},
                      {"nivel_territorial": ["municipal"], "jurisdiccion": "peru"}):
            r = p.responder(consulta_norma(**ajena), HOY)
            self.assertEqual("CITABLE", r.codigo, ajena)
            self.assertTrue(r.citable, "%r no cambia nada" % (ajena,))

        # Control: el nombre que el manifiesto NO publica sí se lee.
        self.assertEqual("FUERA_DE_COBERTURA",
                         p.responder(consulta_norma(territorial=True), HOY).codigo)

    def test_B08_la_nota_obligatoria_de_la_cesacion_anunciada_no_llega_a_la_frase(self):
        """A15 eligió no decir «Hoy no rige» de una norma cuya cesación aún no
        ocurrió, y dejó dicho dónde queda entonces esa información: «la
        cesación anunciada viaja en la nota que `obliga_nota` ya hizo
        obligatoria». La nota se exige —sin ella, `FICHA_INCOMPLETA`— y
        después no viaja a ninguna parte que se lea. `Respuesta.nota` se
        asigna en el constructor y **no lo consulta ninguna línea del
        archivo**: ni `frase`, ni `RespuestaCompuesta.frase`, ni el token.

        Resultado: la ficha que declara que la norma deja de regir dentro de
        cinco años y la que no declara nada producen el **mismo código y la
        misma frase, carácter por carácter**. La casilla obligatoria se cobra
        y no se sirve, y quien consume no tiene por dónde enterarse: es el
        mismo silencio que `FRASES` dice existir para impedir —«el silencio se
        lee como no hay regla»—.

        DEBERÍA FALLAR: la frase de una respuesta con nota tiene que
        transcribirla, que es lo que el docstring de `Respuesta` promete
        —«`nota` viaja transcrita literal, sin interpretar, en toda respuesta
        que hable de una ficha con nota»—.
        """
        nota = "la norma deja de regir el " + meses(60) + "; al firmar no se habia consumado"
        anunciada = ficha_norma(estado_vigencia="SIN_VIGENCIA_DESDE " + meses(60),
                                vigencia_desde=meses(-120), nota_de_vigencia=nota)
        corriente = ficha_norma()

        r_anunciada = evaluar(anunciada, consulta_norma(), HOY)
        r_corriente = evaluar(corriente, consulta_norma(), HOY)

        self.assertEqual("CITABLE", r_anunciada.codigo)
        self.assertEqual(nota, r_anunciada.nota, "la nota está en el objeto…")
        self.assertEqual(r_corriente.frase, r_anunciada.frase, "…y no en lo que se sirve")
        self.assertNotIn(nota, r_anunciada.frase)

        # Tampoco por el pack, ni por el token, que es lo que se publica.
        r = self.pack(anunciada).responder(consulta_norma(), HOY)
        self.assertNotIn(nota, r.frase)
        self.assertNotIn(nota, r.respuestas[0].token)

        # Y lo mismo con la reforma, que es el otro estado que obliga a nota.
        reformada = ficha_norma(estado_vigencia="VIGENTE_CON_REFORMA_AL " + meses(-1),
                                nota_de_vigencia=nota)
        self.assertNotIn(nota, evaluar(reformada, consulta_norma(), HOY).frase)

    def test_B09_la_consulta_incompleta_miente_sobre_la_salud_del_pack(self):
        """`recuento` dice de sí mismo que «viaja en CADA respuesta, no solo
        en el manifiesto: un pack donde 22 de 26 registros están sin vigencia
        comprobada tiene que verse así desde fuera». El corte de R3 va antes
        que el cálculo de `comunes` y devuelve una `RespuestaCompuesta` con
        los valores por defecto: `recuento={}`, `cobertura={}`,
        `degradado=False`, `apagado=False`.

        Los dos últimos no son huecos: son **afirmaciones falsas**. Un pack
        apagado, preguntado con una consulta a la que le falta la fecha del
        caso, contesta `apagado=False` y `degradado=False`. Quien consume y
        mira esos banderines —que es para lo que A13 los puso a gobernar— lee
        que el pack está sano. Y la consulta incompleta es el caso normal, no
        el raro: es la primera que hace cualquiera.

        DEBERÍA FALLAR: `comunes` tiene que calcularse antes del corte de R3 y
        viajar también en `EL_PACK_NO_CONTESTA`. Un banderín de salud vale por
        lo que dice cuando dice que sí.
        """
        podridas = [ficha_norma(identificador_canonico="LEY-0000-%04d" % i,
                                verificado_el=meses(-30)) for i in range(9)]
        p = self.pack(*podridas)
        self.assertTrue(p.apagado(HOY))
        self.assertTrue(p.degradado(HOY))

        r = p.responder({"tipo_de_fecha": "event_date"}, HOY)
        self.assertEqual("EL_PACK_NO_CONTESTA", r.codigo)
        self.assertFalse(r.apagado, "un pack apagado se declara encendido")
        self.assertFalse(r.degradado, "y sano")
        self.assertEqual({}, r.recuento, "y el recuento que viaja en CADA respuesta, vacío")
        self.assertEqual({}, r.cobertura)


# ── VI. La única fecha que no pasa por la puerta ──

class LaFechaQueNadieLee(Ataque):

    def test_B10_hoy_es_la_unica_fecha_del_contrato_que_no_se_valida(self):
        """A11 dejó escrita la regla: «lo que se valida en la frontera no
        vuelve a doler dentro», y nombró los cuatro lectores totales que la
        cumplen —`_fecha`, `leer_materias`, `tipo_de`, la ventana de
        `leer_fuente`—. `hoy` no pasa por ninguno. Entra crudo en `evaluar`,
        `caducada`, `responder`, `verificar_token` y `apagado`, y se compara
        con fechas de ficha que sí pasaron por `_fecha`.

        Un `datetime` en vez de un `date` —que es lo que devuelve
        `datetime.now()`, y es el error de tecleo más barato que hay— levanta
        `TypeError` y tumba el pack entero: no contesta a nada, ni siquiera a
        las consultas sobre las fichas sanas, que es el daño exacto de A11. La
        asimetría deja el fallo a la vista: el mismo `datetime` **dentro** de
        una ficha se lee sin problema, porque ahí sí hay un lector total.

        DEBERÍA FALLAR: `hoy` tiene que pasar por `_fecha` en la frontera de
        cada función pública, y una fecha ilegible tiene que ser un «no», no
        una excepción.
        """
        ahora = datetime(1000, 6, 15, 9, 30)
        p = self.pack(ficha_norma())

        for llamada in (lambda: evaluar(ficha_norma(), consulta_norma(), ahora),
                        lambda: p.responder(consulta_norma(), ahora),
                        lambda: p.apagado(ahora),
                        lambda: caducada(ficha_norma(), ahora)):
            self.assertRaises(TypeError, llamada)

        # El mismo valor dentro de la ficha se lee sin levantar: la frontera
        # existe para las casillas y no para el reloj.
        self.assertEqual("CITABLE",
                         evaluar(ficha_norma(verificado_el=ahora), consulta_norma(), HOY).codigo)

        # Y otras formas de reloj ilegible tumban igual, en vez de decir que no.
        for reloj in ("1000-06-15", None):
            self.assertRaises(TypeError, evaluar, ficha_norma(), consulta_norma(), reloj)


if __name__ == "__main__":
    unittest.main(verbosity=2)
