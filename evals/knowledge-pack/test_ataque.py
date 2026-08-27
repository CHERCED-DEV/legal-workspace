# -*- coding: utf-8 -*-
"""
El adversario, **tercera ronda**. Diez vías, y las diez pasan.

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
     ronda adversaria, 46 con las nueve de la segunda que se cerraron, 56
     cuando se cierren estas diez.

POR DÓNDE ENTRÓ ESTA RONDA. Las dos anteriores ya taparon sus puertas —el
token al portador, el apagado, los tipos de entrada, lo que el token no
guardaba, la composición—, así que había que entrar por otro sitio. Los cuatro
que hubo:

  - **El contrato promete ser total sobre las fichas y no lo es.** El
    encabezado dice que «ninguna función de este archivo levanta una excepción
    por un dato malo», y `evaluar`, `tipo_de` e `identificador_de` defienden
    los tres el caso de una ficha que no es un dict —o sea que el contrato
    sabe que puede llegar—. El censo que corre en CADA consulta no lo defiende
    en ninguna línea: un `None` en la lista, o la lista olvidada, y el pack
    deja de contestar a todo, incluidas las fichas sanas. Es el daño exacto de
    A11 y de B10 por la puerta que ninguna de las dos cerró (C01).
  - **Las guardas de la ronda anterior se ensancharon a medias.** B03 ensanchó
    la LLAVE de `_composicion` —«la llave es la petición»— y dejó el
    DISCRIMINANTE donde estaba, en la cadena cruda de `estado_vigencia`: dos
    fichas discrepan sobre la vigencia del caso que se pregunta sin que esa
    cadena cambie (C03), y la regla entera es inalcanzable en la rama B, cuya
    llave la consulta no trae y cuyo discriminante la ficha no tiene (C04).
    B05 ensanchó el censo a dos campos más pidiéndoles que fueran LEGIBLES, y
    un alcance legible y vacío, o una vigencia que empieza después del techo,
    son tan inservibles como uno ilegible: tres de esas encienden un pack que
    sin ellas estaba apagado, que es la consecuencia que B05 dice cerrar (C05).
  - **La prueba de banco sigue un piso por detrás.** No compara la única cosa
    que toda cita nombra —de qué norma es el artículo que se cita—, y el token
    lleva ese identificador escrito y nunca lo lee, que es A04 otra vez (C06).
    Y la huella que sí lee cubre la versión y las fichas, pero no los dos ejes
    de competencia que B07 acaba de hacer comparables: estrechar la cobertura
    del pack deja vivos todos los tokens de lo que ya no cubre, mientras
    `responder` contesta `FUERA_DE_COBERTURA` a la misma consulta (C07).
  - **Las frases vuelven a afirmar más de lo comprobado.** `A15` era eso y
    `B08` también. Ahora es `CONFLICTO_ENTRE_FICHAS`, que dice «es un problema
    de vigencia, no de identidad» cuando lo que hay es un problema de
    identidad, y «discrepan en la vigencia comprobada» de una ficha que no
    tiene ninguna vigencia comprobada (C08); es el conjunto mixto, que se
    sirve bajo un código —`MULTIPLE`— que no está en ningún vocabulario, no
    tiene frase y vale igual para un conjunto entero citable que para uno con
    un precedente superado dentro (C10); y es la ventana de la fuente, cuyo
    techo es `hoy` y no la firma, de modo que una ficha sale `CITABLE`
    declarando que consultó la fuente oficial once meses DESPUÉS del día en
    que se firmó (C02). Falta el eje territorial, donde las dos formas de
    escribirlo se contradicen y una gana en silencio (C09).

    cd evals/knowledge-pack && python -B -m unittest test_ataque -v

Con las mismas fichas de ejemplo de `fichas.py`: aquí tampoco hay derecho.
"""

import os
import sys
import unittest

# El directorio tiene un guion en el nombre y no es un paquete importable.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from contrato import (CODIGOS_CITABLES, FRASES, Pack,          # noqa: E402
                      evaluar, leer_nivel_territorial)
from fichas import (HOY, FIRMANTE, consulta_norma,             # noqa: E402
                    consulta_providencia, ficha_norma,
                    ficha_providencia, meses, sin)

ART_00 = {"norma_completa": "no", "articulos": ["00"], "incisos": []}
ART_00_Y_01 = {"norma_completa": "no", "articulos": ["00", "01"], "incisos": []}
SIN_ARTICULOS = {"norma_completa": "no", "articulos": [], "incisos": []}
PUBLICADA = "https://ejemplo.invalido/diario-oficial"


def fuente(clase, consultada, referencia=PUBLICADA):
    return {"clase": clase, "referencia": referencia, "consultada": consultada}


class Ataque(unittest.TestCase):
    """Base común. `pack()` arma un pack con versión, que es lo que el token
    exhibe en su huella."""

    def pack(self, *fichas, **kw):
        kw.setdefault("curator", FIRMANTE)
        kw.setdefault("version", "0.1.0")
        return Pack(list(fichas), **kw)

    def token_de(self, pack, consulta, hoy=HOY, indice=0):
        r = pack.responder(consulta, hoy)
        self.assertTrue(r.citable, "el control positivo del ataque no es citable: %s" % r.codigos)
        return r.respuestas[indice].token


# ── I. Lo que el contrato da por hecho de quien lo llama ──

class ElPackSuponeQueLeDanFichas(Ataque):

    def test_C01_una_ficha_que_no_es_ficha_deja_al_pack_sin_contestar_a_nada(self):
        """El encabezado de `contrato.py` no lo deja en duda: «Ninguna función
        de este archivo levanta una excepción por un dato malo: un dato malo
        es un ‹no›. Esa es la diferencia entre un contrato y un formulario.»

        Y el contrato SABE que una ficha puede no ser un dict: lo defienden
        tres funciones distintas —`evaluar` («eso no es una ficha»), `tipo_de`
        e `identificador_de`, las tres con su `isinstance` escrito—. Lo que no
        lo defiende es el censo: `caducada`, `_firma_valida`, `_citable_en_si`,
        `revisar_antes_de` y `cadencia_de` llaman a `ficha.get` sin mirar qué
        tienen delante, y `recuento`, `cobertura` y `apagado` los recorren
        TODOS en cada consulta, porque B09 puso el estado del pack a calcularse
        antes que ninguna otra cosa.

        El resultado es literalmente el daño que A11 documentó —«una casilla
        con 9999-01-01 dejaba el pack entero sin responder a nada, ni siquiera
        a las consultas sobre las demás fichas»— y que B10 volvió a cerrar por
        el lado del reloj. Aquí no hace falta ni una fecha imposible: basta un
        `None` en la lista, o llamar `Pack(ficha)` en vez de `Pack([ficha])`,
        que es el error de tecleo más barato que hay y que el propio
        constructor invita a cometer al hacer `list(fichas)` sin preguntar.

        Lo que el pack devuelve no es un «no»: es un `AttributeError` que sube
        hasta quien consume, y quien consume es un modelo.
        """
        sana = ficha_norma()

        # a) un hueco en la lista y el pack enmudece para la ficha sana.
        con_hueco = self.pack(None, sana)
        with self.assertRaises(AttributeError):
            con_hueco.responder(consulta_norma(), HOY)
        # …y para todo lo demás: el estado del pack tampoco se puede calcular.
        with self.assertRaises(AttributeError):
            con_hueco.recuento(HOY)
        with self.assertRaises(AttributeError):
            con_hueco.apagado(HOY)
        with self.assertRaises(AttributeError):
            con_hueco.cobertura(HOY)

        # b) cualquier cosa que no sea un dict sirve igual.
        for basura in ("una ficha en prosa", 7, ["casi", "una", "ficha"]):
            with self.assertRaises(AttributeError):
                self.pack(basura, sana).responder(consulta_norma(), HOY)

        # c) olvidar los corchetes: `list({...})` son las CLAVES de la ficha.
        with self.assertRaises(AttributeError):
            Pack(sana, curator=FIRMANTE, version="0.1.0").responder(consulta_norma(), HOY)

        # El control: `evaluar` sí sabe contestar a lo mismo, con su código y
        # su frase. La defensa existe; no llega a donde se necesita.
        self.assertEqual("NO_TENEMOS_INFORMACION_SUFICIENTE",
                         evaluar(None, consulta_norma(), HOY).codigo)


# ── II. La ventana de la fuente tiene techo, y no es el de la firma ──

class LaFuenteSeConsultoDespuesDeFirmar(Ataque):

    def test_C02_la_fuente_se_puede_consultar_meses_despues_de_firmar_la_ficha(self):
        """A12 puso ventana a `consultada` porque «la cadencia medía la edad
        de la firma y nada medía la edad de lo que se firmó», y sacó los dos
        bordes de lo que el pack ya decía: el suelo, la firma menos la
        cadencia; el techo, **`hoy`**, con el argumento de que «nadie consulta
        el futuro».

        El techo está en el sitio equivocado, y el propio contrato tiene el
        argumento escrito dos veces. N2/A.8: «el techo es el día de la
        comprobación, que es hasta donde llega lo que la verificadora firmó».
        A15: la cesación se compara «contra la firma y no contra `hoy` a
        propósito», porque si no «la misma ficha caducaría o no según cuándo se
        la mire». Aquí pasan las dos cosas a la vez: la mitad de la ventana cae
        DESPUÉS de la firma, y esa mitad se ensancha sola cada día que pasa.

        Lo que sale de ahí es una ficha que declara, en su propia casilla, que
        la comprobación que la firma respalda ocurrió once meses después de
        firmarse. Nadie firmó eso. Y sale `CITABLE`.
        """
        # a) un mes de más: la ficha perfecta con la fuente consultada hoy.
        un_mes = ficha_norma(fuente_vigencia=fuente("PRIMARY_OFFICIAL", meses(0)))
        self.assertEqual(meses(-1), un_mes["verificado_el"])
        self.assertEqual("CITABLE", evaluar(un_mes, consulta_norma(), HOY).codigo)

        # b) once meses de más, que es toda la mitad delantera de la cadencia.
        tarde = ficha_norma(
            verificado_el=meses(-11),
            estado_vigencia="VIGENTE_AL " + meses(-11),
            fuente_identidad=fuente("PRIMARY_OFFICIAL", meses(0),
                                    "https://ejemplo.invalido/publicacion-oficial"),
            fuente_vigencia=fuente("PRIMARY_OFFICIAL", meses(0)))
        r = evaluar(tarde, consulta_norma(fecha_del_caso=meses(-12)), HOY)
        self.assertEqual("CITABLE", r.codigo)
        self.assertEqual("cumple las diez condiciones", r.motivo)

        # El control positivo de la guarda que sí existe: por el otro lado la
        # ventana corta donde A12 dijo, así que no es que la ventana no mida.
        pronto = ficha_norma(fuente_vigencia=fuente("PRIMARY_OFFICIAL", meses(-14)))
        self.assertEqual("VIGENCIA_NO_COMPROBADA", evaluar(pronto, consulta_norma(), HOY).codigo)


# ── III. La composición: se ensanchó la llave y no el discriminante ──

class LaLlaveSeEnsanchoYElDiscriminanteNo(Ataque):

    def test_C03_dos_fichas_discrepan_sobre_el_caso_sin_discrepar_en_la_cadena(self):
        """B03 dijo que la llave de `_composicion` era «más estrecha que la
        pregunta que contesta» y la ensanchó: ya no se agrupa por
        `(identificador, alcance_comprobado)` idénticos sino por las fichas que
        **cubren lo que se pide**. Perfecto, y a mitad de camino: el
        DISCRIMINANTE sigue siendo `_texto(f.get("estado_vigencia"))`, una
        cadena, comparada por igualdad.

        La pregunta que la regla contesta —lo dice su propia frase— es si dos
        fichas «discrepan en la vigencia comprobada». Y dos fichas pueden
        discrepar sobre si la norma regía **el día del caso que se pregunta**
        sin que esa cadena cambie ni un carácter, porque la vigencia del caso
        no la decide solo `estado_vigencia`: la deciden también `vigencia_desde`
        (A.6) y `verificado_el` (el techo de A.8).

        Aquí las dos fichas dicen `VIGENTE_AL` el mismo día. Una tiene la norma
        rigiendo desde hace cinco años y la otra desde hace tres meses. Para un
        caso de hace treinta meses, una contesta que sí y la otra que la
        comprobación firmada no lo cubre. No hay conflicto para el contrato, y
        lo que se sirve son las dos frases juntas: la afirmativa primero.

        Es exactamente el fallo que A16 describió —«se servían las dos frases
        individuales, que no dicen que haya conflicto; una de ellas dice
        CITABLE»— reaparecido por debajo de su corrección.
        """
        larga = ficha_norma(vigencia_desde=meses(-60))
        corta = ficha_norma(vigencia_desde=meses(-3))
        self.assertEqual(larga["estado_vigencia"], corta["estado_vigencia"])

        pack = self.pack(larga, corta)
        r = pack.responder(consulta_norma(fecha_del_caso=meses(-30)), HOY)

        self.assertEqual(["CITABLE", "FUERA_DE_LA_VIGENCIA_COMPROBADA"], r.codigos)
        self.assertNotEqual("CONFLICTO_ENTRE_FICHAS", r.codigo)
        self.assertIn("vigente dentro del alcance y de la ventana comprobadas", r.frase)
        self.assertIn("no la cubre", r.frase)
        self.assertNotIn("discrepan", r.frase)

        # El control: la regla FUNCIONA, solo que mira el campo equivocado.
        # Cambiada la cadena —y nada más—, el conflicto sí aparece.
        otra = ficha_norma(vigencia_desde=meses(-60),
                           estado_vigencia="VIGENTE_CON_REFORMA_AL " + meses(-1),
                           nota_de_vigencia="consta reforma dentro del alcance")
        self.assertEqual("CONFLICTO_ENTRE_FICHAS",
                         self.pack(larga, otra).responder(consulta_norma(), HOY).codigo)

    def test_C04_la_regla_de_composicion_es_inalcanzable_en_la_rama_B(self):
        """La regla de composición no puede dispararse NUNCA para una
        providencia, y por dos motivos independientes, cada uno suficiente:

          - su llave es la petición (`ejes["peticion"]`), y una consulta de
            providencia no trae `peticion` —`consulta_providencia` no la tiene
            y no puede tenerla: el alcance es de las normas—, así que
            `contenido_en(None, …)` es False y ninguna ficha entra al grupo;
          - su discriminante es `estado_vigencia`, campo que una providencia no
            tiene, de modo que aunque entraran todas darían el mismo `None`.

        La segunda parte ya estaba antes de B03; la primera la puso B03. El
        resultado es que dos fichas de la MISMA providencia y la MISMA
        proposición, una confirmada y otra superada, se sirven como dos frases
        seguidas —«sostiene la proposición atribuida» y «está marcada como
        superada o limitada»— sin ningún código que diga que el pack no elige.

        N4 abrió `CONFLICTO_ENTRE_FICHAS` para no servir un fallo bajo un
        código que habla de otra cosa. La rama B se quedó sin ninguno, y es la
        rama donde el conflicto es el estado normal: `estado_uso` tiene dos
        valores citables y dos superados escritos en el mismo vocabulario.
        """
        confirmada = ficha_providencia()
        superada = ficha_providencia(estado_uso="SUPERSEDED_OR_LIMITED")
        r = self.pack(confirmada, superada).responder(consulta_providencia(), HOY)

        self.assertEqual(["CITABLE_PRECEDENTE", "PRECEDENTE_SUPERADO_O_LIMITADO"], r.codigos)
        self.assertNotEqual("CONFLICTO_ENTRE_FICHAS", r.codigo)
        self.assertIn("sostiene la proposición atribuida", r.frase)
        self.assertIn("superada o limitada", r.frase)

        # Y con `CONFLICTING`, que es el valor que el vocabulario tiene puesto
        # justo para esto, tampoco.
        enconflicto = ficha_providencia(estado_uso="CONFLICTING")
        self.assertNotEqual(
            "CONFLICTO_ENTRE_FICHAS",
            self.pack(confirmada, enconflicto).responder(consulta_providencia(), HOY).codigo)

        # El control: la misma contradicción entre normas sí tiene código.
        self.assertEqual(
            "CONFLICTO_ENTRE_FICHAS",
            self.pack(ficha_norma(),
                      ficha_norma(estado_vigencia="SIN_VIGENCIA_DESDE " + meses(-24))
                      ).responder(consulta_norma(), HOY).codigo)

    def test_C10_el_conjunto_mixto_se_sirve_bajo_un_codigo_que_no_existe(self):
        """Lo que hace posibles C03 y C04 es que **no hay código para el
        conjunto**. `RespuestaCompuesta.codigo` devuelve la cadena `MULTIPLE`
        en cuanto hay más de una ficha, y `MULTIPLE`:

          - no está en las veintiuna claves de `FRASES`, así que no tiene
            frase que servir —el silencio que `FRASES` dice existir para
            impedir, con el añadido de que aquí no está en la lista de nadie—;
          - no está en `CODIGOS_CITABLES`, así que quien consume leyendo el
            código y quien consume leyendo `.citable` reciben cosas opuestas
            del mismo objeto. Es el patrón de A09 —el mismo valor leído de dos
            maneras— en la puerta de salida;
          - y vale exactamente igual para un conjunto ENTERO citable, con sus
            tokens emitidos, que para uno con un precedente superado dentro.
            El código no distingue el sí del no, o sea que no informa de nada.

        La regla de N5 —«el conjunto es citable solo si lo son todas»— está
        bien y no se discute: lo que falta es su código y su frase, que es lo
        que A16 le dio a `CONFLICTO_ENTRE_FICHAS` con este mismo argumento.
        """
        citable = self.pack(ficha_norma(), ficha_norma()).responder(consulta_norma(), HOY)
        mixta = self.pack(ficha_providencia(),
                          ficha_providencia(estado_uso="SUPERSEDED_OR_LIMITED")
                          ).responder(consulta_providencia(), HOY)

        self.assertEqual("MULTIPLE", citable.codigo)
        self.assertEqual("MULTIPLE", mixta.codigo)
        self.assertTrue(citable.citable)
        self.assertFalse(mixta.citable)
        self.assertNotIn("MULTIPLE", FRASES)
        self.assertNotIn("MULTIPLE", CODIGOS_CITABLES)
        # Dos tokens servidos bajo un código que el propio contrato no
        # reconoce como citable.
        self.assertEqual(2, len([r for r in citable.respuestas if r.token]))


# ── IV. El censo cuenta lo que ninguna consulta puede servir ──

class ElCensoCuentaInventario(Ataque):

    def test_C05_una_ficha_legible_e_inservible_enciende_un_pack_apagado(self):
        """B05 escribió la condición general y la dejó a medio aplicar: «es
        contable lo que alguna consulta podría llegar a hacer citable. Lo demás
        es inventario». Lo que comprueba, sin embargo, es que
        `alcance_comprobado` y `vigencia_desde` sean LEGIBLES, y legible no es
        servible:

          - un alcance legible y **vacío** —`articulos: []`, `incisos: []`,
            `norma_completa: no`— hace que `contenido_en` sea False para toda
            petición, porque una petición que no pide nada tampoco está
            contenida en nada. Ninguna consulta la puede servir;
          - una `vigencia_desde` legible y **posterior al techo de A.8** deja a
            A.6 y a A.8 pidiendo dos cosas incompatibles: el caso tiene que ser
            a la vez posterior a una fecha y anterior a otra más temprana.

        Y la consecuencia es la que B05 nombra, la de seguridad y no la de
        precisión: `citables_hoy` es el denominador de `degradado`, `degradado`
        es el interruptor, y **tres fichas que no se pueden servir jamás
        encienden un pack que sin ellas estaba apagado**. Palabra por palabra
        el daño que B05 dice haber cerrado, por dos campos que sí se leen.
        """
        podrida = ficha_norma(verificado_el=meses(-20),
                              estado_vigencia="VIGENTE_AL " + meses(-20))
        vacia = ficha_norma(alcance_comprobado=SIN_ARTICULOS)
        futura = ficha_norma(vigencia_desde=meses(+10))

        # Ninguna de las dos puede salir citable para ninguna consulta.
        self.assertEqual("FUERA_DEL_ALCANCE_COMPROBADO",
                         evaluar(vacia, consulta_norma(), HOY).codigo)
        self.assertEqual("FUERA_DEL_ALCANCE_COMPROBADO",
                         evaluar(vacia, consulta_norma(peticion=ART_00_Y_01), HOY).codigo)
        self.assertEqual("FUERA_DE_LA_VIGENCIA_COMPROBADA",
                         evaluar(futura, consulta_norma(), HOY).codigo)
        self.assertEqual("FUERA_DE_LA_VIGENCIA_COMPROBADA",
                         evaluar(futura, consulta_norma(fecha_del_caso=meses(+10)), HOY).codigo)

        # Sola, la podrida apaga el pack.
        solo_podrida = self.pack(podrida)
        self.assertTrue(solo_podrida.degradado(HOY))
        self.assertTrue(solo_podrida.apagado(HOY))

        # Con tres inservibles al lado, el mismo pack se declara sano.
        esperado = {id(vacia): "FUERA_DEL_ALCANCE_COMPROBADO",
                    id(futura): "FUERA_DE_LA_VIGENCIA_COMPROBADA"}
        for inservible in (vacia, futura):
            reanimado = self.pack(podrida, inservible, inservible, inservible)
            self.assertEqual(3, reanimado.recuento(HOY)["citables_hoy"])
            self.assertFalse(reanimado.degradado(HOY))
            self.assertFalse(reanimado.apagado(HOY))
            # …y declara cubierta un área en la que no puede contestar nada.
            self.assertIn("area-de-ejemplo", reanimado.cobertura(HOY)["materias_declaradas"])
            self.assertEqual(["PACK_CADUCADO"] + [esperado[id(inservible)]] * 3,
                             reanimado.responder(consulta_norma(), HOY).codigos)


# ── V. La prueba de banco, todavía un piso por detrás ──

class LaPruebaDeBancoNoVeLaCita(Ataque):

    def test_C06_la_prueba_de_banco_no_ve_de_que_norma_es_lo_que_se_cita(self):
        """`verificar_token` comprueba diez cosas y ninguna es la que toda
        cita nombra primero: **de qué norma** es el artículo que se publica.
        `lo_citado` llega como un alcance —`{norma_completa, articulos,
        incisos}`, tres claves exactas, y `leer_alcance` rechaza cualquier
        otra—, así que no hay ningún sitio donde decirlo. El `caso` sí fija el
        identificador, pero el caso es la CONSULTA, no la entrega: nada obliga
        a que se cite la norma que se preguntó.

        Y el identificador está escrito dentro del token, a la vista, en la
        parte «identificador + alcance». Se escribe y no se compara con nada,
        que es literalmente A04 —«version + checksum se escribían dentro del
        token y después no se comparaban con nada»— aplicado al otro campo.

        El escenario es el de siempre y no hace falta malicia: el pack tiene
        dos normas, contesta que sí a una y que no a la otra, y la entrega
        confunde cuál. La prueba de banco, que existe para cazar exactamente
        eso, dice que pasa.
        """
        citable = ficha_norma()
        negada = ficha_norma(identificador_canonico="LEY-1111-1111",
                             estado_vigencia="VIGENCIA_NO_COMPROBADA")
        pack = self.pack(citable, negada)

        self.assertEqual("VIGENCIA_NO_COMPROBADA",
                         pack.responder(consulta_norma(identificador="LEY-1111-1111"), HOY).codigo)
        token = self.token_de(pack, consulta_norma())
        self.assertIn("LEY-0000-0000", token)

        # La entrega publica «LEY-1111-1111, art. 00». El banco la respalda.
        self.assertEqual((True, "el token resuelve contra una respuesta servida"),
                         pack.verificar_token(token, ART_00, HOY, consulta_norma()))

        # Y no hay forma de decirle cuál se cita: el intento se rechaza por el
        # alcance, no por la identidad, así que el motivo también engaña.
        con_identidad = dict(ART_00, identificador="LEY-1111-1111")
        self.assertEqual((False, "el alcance del token no contiene lo que se cita"),
                         pack.verificar_token(token, con_identidad, HOY, consulta_norma()))

        # En la rama B es peor, porque B.6 dice que «la unidad no es la
        # providencia, es el par providencia + proposición»: se comprueba la
        # proposición, literal, y la providencia a la que se le atribuye no.
        buena = ficha_providencia()
        mala = ficha_providencia(identificador="J-YY-9999-9999",
                                 estado_uso="SUPERSEDED_OR_LIMITED")
        pack_b = self.pack(buena, mala)
        token_b = self.token_de(pack_b, consulta_providencia())
        self.assertTrue(pack_b.verificar_token(
            token_b, "proposicion de ejemplo numero 00", HOY, consulta_providencia())[0])

    def test_C07_la_huella_no_cubre_la_competencia_que_el_pack_publica(self):
        """B02 puso el estado del pack dentro de la prueba de banco con una
        frase que no admite excepciones: «El pack que no responde tampoco
        respalda». Y B07 hizo comparables los dos ejes que el manifiesto
        publicaba sin comparar, la jurisdicción y el nivel territorial,
        poniéndolos en el pack «porque la competencia es una declaración de
        quien cura».

        Las dos correcciones no se tocan, y en el hueco cabe esto: la huella
        que el token exhibe es `version + checksum(fichas)`, y los dos ejes de
        competencia no son fichas. Un curador que estrecha lo que su pack
        cubre —que es la forma normal de dejar de cubrir algo, y la que no
        obliga a tocar ni un registro— deja vivos todos los tokens ya emitidos
        para lo que acaba de soltar. El mismo pack, el mismo día, contesta
        `FUERA_DE_COBERTURA` a la consulta y `pasa` a la cita que salió de
        ella.

        A04 comprueba la huella «porque sin ella un token no se puede resolver
        contra una versión del pack». La huella resuelve contra las fichas y no
        contra el pack.
        """
        pack = self.pack(ficha_norma(), niveles_territoriales=("nacional", "municipal"))
        consulta = consulta_norma(nivel_territorial="municipal")
        token = self.token_de(pack, consulta)

        pack.niveles_territoriales = ("nacional",)
        self.assertEqual("FUERA_DE_COBERTURA", pack.responder(consulta, HOY).codigo)
        self.assertEqual((True, "el token resuelve contra una respuesta servida"),
                         pack.verificar_token(token, ART_00, HOY, consulta))

        # Lo mismo por el otro eje.
        otro = self.pack(ficha_norma())
        consulta_j = consulta_norma(jurisdiccion="colombia")
        token_j = self.token_de(otro, consulta_j)
        otro.jurisdiccion = "otra-jurisdiccion-de-ejemplo"
        self.assertEqual("FUERA_DE_COBERTURA", otro.responder(consulta_j, HOY).codigo)
        self.assertTrue(otro.verificar_token(token_j, ART_00, HOY, consulta_j)[0])

        # El control: tocar una ficha sí mueve la huella, así que el mecanismo
        # existe y lo que falta es qué mete dentro.
        tercero = self.pack(ficha_norma())
        token_t = self.token_de(tercero, consulta_norma())
        tercero.fichas[0]["alcance_comprobado"] = ART_00_Y_01
        self.assertEqual((False, "el token se emitió contra otra versión del pack"),
                         tercero.verificar_token(token_t, ART_00, HOY, consulta_norma()))


# ── VI. La frase que afirma más de lo que se comprobó ──

class LaFraseDelConflicto(Ataque):

    def test_C08_el_conflicto_entre_fichas_afirma_lo_que_no_miro(self):
        """A15 es el precedente exacto: «es la única frase del contrato que
        afirma algo sobre el mundo y se servía sin comprobar la afirmación».
        La frase de `CONFLICTO_ENTRE_FICHAS` afirma dos cosas sobre el pack, y
        `_composicion` no comprueba ninguna de las dos.

          - «**Es un problema de vigencia, no de identidad**». `_composicion`
            no lee `estado_identidad` en ninguna línea. Una ficha cuya
            identidad nadie ha comprobado tiene, por eso mismo, una cadena de
            vigencia distinta de la de su hermana sana, así que dispara el
            conflicto y la respuesta niega que el problema sea de identidad
            **cuando ese es exactamente el problema**. Y como A16 hizo que la
            frase de composición SUSTITUYA a las individuales, la única que lo
            decía —«Nadie ha comprobado que sea la norma que dice ser. Esto no
            es un problema de vigencia: es anterior»— desaparece.
          - «**discrepan en la vigencia comprobada**». Una ficha sin
            `estado_vigencia` no tiene ninguna vigencia comprobada con la que
            discrepar: su respuesta propia es «El pack tiene X y no tiene
            comprobada su vigencia. Eso no es lo mismo que decir que no rige,
            ni que sí», que es una frase escrita para no afirmar de más. Se
            reemplaza por una que afirma que hay dos comprobaciones y chocan.

        De paso se lleva la nota. B08 cerró que la nota obligatoria llegara a
        la frase servida —«la casilla que `obliga_nota` cobra no se servía en
        ninguna parte»— y por este camino vuelve a no llegar: la cesación
        anunciada de la ficha sana no se transcribe en ningún sitio.
        """
        sana = ficha_norma()
        sin_identidad = ficha_norma(estado_identidad="IDENTIDAD_POR_VERIFICAR",
                                    estado_vigencia="VIGENCIA_NO_COMPROBADA")
        r = self.pack(sana, sin_identidad).responder(consulta_norma(), HOY)

        self.assertEqual(["CITABLE", "IDENTIDAD_POR_VERIFICAR"], r.codigos)
        self.assertEqual("CONFLICTO_ENTRE_FICHAS", r.codigo)
        self.assertIn("Es un problema de vigencia, no de identidad", r.frase)
        self.assertNotIn("Nadie ha comprobado", r.frase)

        # Una ficha que no dice nada de la vigencia «discrepa» con la que sí.
        muda = sin(ficha_norma(), "estado_vigencia")
        r2 = self.pack(sana, muda).responder(consulta_norma(), HOY)
        self.assertEqual(["CITABLE", "VIGENCIA_NO_COMPROBADA"], r2.codigos)
        self.assertEqual("CONFLICTO_ENTRE_FICHAS", r2.codigo)
        self.assertIn("discrepan en la vigencia comprobada", r2.frase)
        self.assertNotIn("no tiene comprobada su vigencia", r2.frase)

        # Y la nota obligatoria de la cesación anunciada tampoco llega.
        anunciada = ficha_norma(
            estado_vigencia="SIN_VIGENCIA_DESDE " + meses(+60),
            nota_de_vigencia="la norma deja de regir el " + meses(+60))
        r3 = self.pack(anunciada, muda).responder(consulta_norma(), HOY)
        self.assertEqual("CONFLICTO_ENTRE_FICHAS", r3.codigo)
        self.assertNotIn("transcrita", r3.frase)


# ── VII. Las dos formas del mismo eje, y una gana en silencio ──

class DosManerasDeEscribirUnEje(Ataque):

    def test_C09_las_dos_formas_del_eje_territorial_se_contradicen_y_una_gana(self):
        """B07 juntó los dos nombres del eje territorial en un solo lector con
        el argumento correcto: «dos maneras de escribir el mismo eje son
        tolerables mientras haya un solo lector que las resuelva; dos lectores
        no lo son». Lo que el lector único no resuelve es qué pasa cuando las
        dos maneras **dicen cosas distintas**.

        `territorial: True` significa, por A06 y por el comentario de
        `NIVEL_SIN_NOMBRAR`, «hay algo territorial y no sé qué», y cae fuera.
        `nivel_territorial: "nacional"` significa que no lo hay. Una consulta
        que trae las dos —la del consumidor que aprendió el booleano de A06 y
        el nombre del manifiesto, que es el consumidor que B07 describe— se
        resuelve en silencio a favor del nombre, y el caso territorial recibe
        una respuesta nacional con su token.

        La regla que faltaba está escrita tres líneas más arriba, en la misma
        función y para el mismo eje: una lista de dos niveles no es un nivel y
        cae en `NIVEL_SIN_NOMBRAR`. Dos escrituras que se contradicen son el
        mismo caso —«hay algo territorial y no sé qué»— y aquí una gana. Es la
        lista blanca haciendo la vista gorda con una contradicción, que es lo
        que `leer_estado_vigencia` prohíbe expresamente: «la lista blanca se
        rompe entera si aquí se hace la vista gorda con una errata».
        """
        pack = self.pack(ficha_norma())

        solo_booleano = consulta_norma(territorial=True)
        self.assertEqual("", leer_nivel_territorial(solo_booleano))
        self.assertEqual("FUERA_DE_COBERTURA", pack.responder(solo_booleano, HOY).codigo)

        # La rama cerrada, que es el control: dos niveles a la vez no son uno.
        dos_niveles = consulta_norma(nivel_territorial=["nacional", "municipal"])
        self.assertEqual("", leer_nivel_territorial(dos_niveles))
        self.assertEqual("FUERA_DE_COBERTURA", pack.responder(dos_niveles, HOY).codigo)

        # La rama abierta: las dos escrituras juntas, contradiciéndose.
        ambas = consulta_norma(territorial=True, nivel_territorial="nacional")
        self.assertEqual("nacional", leer_nivel_territorial(ambas))
        r = pack.responder(ambas, HOY)
        self.assertEqual("CITABLE", r.codigo)
        self.assertTrue(r.citable)
        self.assertIsNotNone(r.respuestas[0].token)


if __name__ == "__main__":
    unittest.main()
