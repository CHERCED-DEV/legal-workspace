# -*- coding: utf-8 -*-
"""
El contrato de consumo del Knowledge Pack, escrito como código ejecutable.

NO es producto y no vive en `plugins/`: es herramienta de verificación, como
`evals/medir.py`. Responde una sola pregunta —¿esta ficha se puede citar para
esta consulta?— de una forma que no admite interpretación.

POR QUÉ EN CÓDIGO. El contrato se escribió dos veces en prosa
(`docs/knowledge-pack/02-contrato-de-consumo.md`). La primera versión dejaba
cinco vías por las que una norma sin vigencia comprobada salía `CITABLE`; la
corrección cerró una, dejó tres abiertas y abrió siete nuevas. Un algoritmo
con veinte respuestas, contención de conjuntos, aritmética de fechas y
validación de campos no se puede especificar en prosa sin agujeros. Aquí cada
vía es un test que pasa o falla, y eso no se interpreta.

LA REGLA DE DISEÑO, Y ES LA ÚNICA QUE HAY QUE RECORDAR: **lista blanca**. Se
es citable solo si se cumplen TODAS las condiciones positivas, cada una
comprobada sobre un valor reconocido. Cualquier otra cosa —casilla vacía,
valor escrito de otra forma, comparación imposible, fecha ilegible— cae en el
estado inseguro. Ninguna función de este archivo levanta una excepción por un
dato malo: un dato malo es un «no». Esa es la diferencia entre un contrato y
un formulario.

QUÉ SE APARTA DE LA PROSA, y por qué (todo viene de las dos críticas):
  - Campo nuevo `reforma_buscada` en la norma. Sin él, `VIGENTE_AL` escrito
    tras buscar la reforma es indistinguible de `VIGENTE_AL` escrito sin
    mirarla (V2, el hallazgo principal de la segunda crítica).
  - `fuente_identidad` pasa a ser tipada, como ya lo era `fuente_vigencia`.
    La columna de vigencia tenía puerta y la de identidad no tenía ninguna.
  - `materia[]` también en providencias: si no, el pack sirve un precedente
    en una materia que él mismo declara excluida.
  - `tipo` declarado en la ficha. Deducir si es norma o providencia por los
    campos que tiene ES la vía V4: la providencia atravesaba entera la tabla
    de las normas precisamente porque no tenía sus campos.
  - Tres códigos añadidos a los diecisiete: `FICHA_NO_FIRMADA`,
    `FICHA_INCOMPLETA` y `CONFLICTO_ENTRE_FICHAS`. Los tres existen para no
    servir un fallo bajo un código que habla de otra cosa, que es el error
    que las dos críticas señalan en las dos direcciones (H8 y N4).

TERCERA RONDA (A01-A18). Una suite adversaria atacó este archivo por donde las
dos críticas no miraron y encontró dieciocho vías más. Todas están cerradas y
todas tienen su test de regresión en `test_vias.py`. Lo que enseñaron, en tres
frases, porque el patrón vale más que la lista:

  - **El token era una credencial al portador.** Se emitía antes de saber si
    el pack decía que sí (A01, A02), no registraba para qué caso se pidió
    (A03, A07), y la prueba de banco no leía ni la huella del pack que el
    token exhibe (A04) ni el alcance con el que se emitió (A05). Ahora el
    token se emite solo cuando el conjunto es citable y se resuelve contra la
    foto de la ficha del día en que se sirvió.
  - **Lo que se valida en la frontera no vuelve a doler dentro.** Una fecha
    del año 9999 tumbaba el pack entero por desbordamiento del calendario
    (A11), una `materia` en cadena se recorría letra a letra (A10), un `tipo`
    con un espacio partía la ficha en dos lecturas (A09) y una fuente podía
    declararse consultada dentro de ocho mil años (A12). Cuatro lectores
    totales —`_fecha`, `leer_materias`, `tipo_de`, la ventana de `leer_fuente`—
    cierran los cuatro en la puerta.
  - **Una lista negra siempre se rodea.** `_apunta_al_corpus` decidía por seis
    subcadenas y bastaba quitar la extensión del archivo (A17). Ahora la
    referencia se acepta por lo que es —una publicación con esquema y
    dominio—, no se rechaza por lo que parece.

Ni una norma, ni una fecha de vigencia, ni un estado jurídico reales: aquí ni
en `fichas.py`.
"""

import calendar
import hashlib
import json
import secrets
import statistics
import sys
from datetime import date, datetime

# La consola de Windows llega en cp1252 y no admite las tildes de los motivos.
# Mismo remedio que en `evals/medir.py`, por el mismo motivo.
for _flujo in (sys.stdout, sys.stderr):
    try:
        if (_flujo.encoding or "").lower().replace("-", "") != "utf8":
            _flujo.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ─────────────────────── §A. Vocabularios y códigos ───────────────────────

IDENTIDAD_VERIFICADA = "IDENTIDAD_VERIFICADA"
IDENTIDAD_POR_VERIFICAR = "IDENTIDAD_POR_VERIFICAR"
CONFLICTO_DE_FUENTES = "CONFLICTO_DE_FUENTES"

VIGENTE_AL = "VIGENTE_AL"
VIGENTE_CON_REFORMA_AL = "VIGENTE_CON_REFORMA_AL"
SIN_VIGENCIA_DESDE = "SIN_VIGENCIA_DESDE"
VIGENCIA_PARCIAL_AL = "VIGENCIA_PARCIAL_AL"
VIGENCIA_NO_COMPROBADA = "VIGENCIA_NO_COMPROBADA"

# Los cuatro estados que llevan fecha pegada: `VIGENTE_AL AAAA-MM-DD`.
ESTADOS_CON_FECHA = frozenset({
    VIGENTE_AL, VIGENTE_CON_REFORMA_AL, SIN_VIGENCIA_DESDE, VIGENCIA_PARCIAL_AL,
})
# Los tres que pueden llegar a ser citables. `VIGENCIA_PARCIAL_AL` no está, y
# esa ausencia es la regla: rige en parte y nunca se sirve como citable.
ESTADOS_QUE_PUEDEN_SER_CITABLES = frozenset({
    VIGENTE_AL, VIGENTE_CON_REFORMA_AL, SIN_VIGENCIA_DESDE,
})
# La nota es obligatoria en estos dos (`01` §2). Obligatoria quiere decir que
# la ficha está incompleta sin ella, no que se recuerde llenarla.
ESTADOS_QUE_OBLIGAN_NOTA = frozenset({VIGENTE_CON_REFORMA_AL, VIGENCIA_PARCIAL_AL})

# Clases de fuente de `04-source-governance.md` §4.1. Fuera de esta lista, la
# clase no es una clase: es una cadena que alguien escribió.
CLASES_DE_FUENTE = frozenset({
    "PRIMARY_OFFICIAL", "OFFICIAL_CONSOLIDATED", "OFFICIAL_JURISPRUDENCE",
    "OFFICIAL_INTERPRETIVE", "SECONDARY", "NINGUNA",
})
# La vigencia exige `PRIMARY_OFFICIAL` y nada más (`01` P4, `02` A.5): es la
# regla que separa «comprobé» de «el portal no decía nada».
CLASES_DE_VIGENCIA = frozenset({"PRIMARY_OFFICIAL"})
# La identidad admite las dos clases oficiales de texto normativo. La
# asimetría con la vigencia es deliberada y está en el procedimiento: P1 pide
# ver el texto en fuente oficial; P4 pide una fuente primaria.
CLASES_DE_IDENTIDAD_NORMA = frozenset({"PRIMARY_OFFICIAL", "OFFICIAL_CONSOLIDATED"})
CLASES_DE_IDENTIDAD_PROVIDENCIA = frozenset({"OFFICIAL_JURISPRUDENCE", "PRIMARY_OFFICIAL"})

ESTADOS_DE_USO_CITABLES = frozenset({"PROFESSIONALLY_CONFIRMED", "RELEVANCE_REVIEWED"})
ESTADOS_DE_USO_SUPERADOS = frozenset({"SUPERSEDED_OR_LIMITED", "CONFLICTING"})

# Vocabulario de `05-temporal-applicability.md` §1. «La fecha del caso» no
# existe en singular: pasar la equivocada convierte una respuesta negativa en
# citable sin que nada lo note.
TIPOS_DE_FECHA = frozenset({
    "case_relevant_date", "procedural_start_date", "event_date",
    "decision_date", "published_at",
})

# Plantillas de formato del propio instrumento. Si una casilla llega con la
# plantilla dentro es que nadie la llenó, así que vale lo que vale una casilla
# vacía. Solo van aquí las plantillas de FORMA: `LEY-0000-0000` o `art. 00`
# son contenido de ejemplo y tienen que circular como cualquier otro valor,
# porque son los únicos con los que este instrumento puede probarse.
RELLENOS = frozenset({"AAAA-MM-DD", "TIPO-NUMERO-AÑO", "null", "None", "-", "—"})

# Las dos ramas de la tabla de decisión, y no hay una tercera. `tipo` se
# declara y se lee por lista blanca en TODAS partes: leerlo con `_texto` en un
# sitio y con `==` en otro partía la ficha en dos —providencia para la tabla,
# norma para el recuento y para la prueba de banco— y esa era A09.
TIPOS_DE_FICHA = frozenset({"norma", "providencia"})

# El calendario en el que este contrato sabe hacer cuentas. No es un juicio
# sobre qué fechas son plausibles: es que la ÚNICA operación que el contrato
# hace con una fecha —sumarle la cadencia, o los 18 meses del apagado— se sale
# del calendario de `date` a partir del año 9999 y levanta. Una fecha con la
# que no se puede hacer esa cuenta no es una fecha comparable, y lo que no se
# puede comparar cae fuera; el margen cubre la cadencia más larga por los dos
# lados. Era A11: una casilla con `9999-01-01` dejaba el pack entero sin
# responder a nada, ni siquiera a las consultas sobre las demás fichas.
ANIO_MINIMO = 10
ANIO_MAXIMO = 9990

# Esquemas con los que una referencia puede señalar algo publicado. Lista
# blanca, y sustituye a la lista negra de seis subcadenas de A17.
ESQUEMAS_PUBLICADOS = ("https://", "http://")

# El alfabeto de una etiqueta de dominio. Se enumera en vez de usar
# `str.isalnum()` porque `isalnum()` es verdadero para «á» y para «٣», y un
# nombre de dominio del DNS público no se escribe con eso: aceptarlos sería
# volver a decidir por parecido en lugar de por forma comprobable.
ASCII_LETRAS = frozenset("abcdefghijklmnopqrstuvwxyz")
ASCII_DIGITOS = frozenset("0123456789")
CARACTERES_DE_ETIQUETA = ASCII_LETRAS | ASCII_DIGITOS | frozenset("-")

# Los dominios de primer nivel que los propios estándares apartan del DNS
# público (RFC 2606 §2, RFC 6761 §6). No es una lista negra de las de A17 —una
# conjetura sobre qué nombres «parecen» del corpus, y lo que no se pensó es
# infinito—: es un registro cerrado y escrito por alguien más, y lo que
# enumera son nombres que por definición no designan nada fuera de la máquina
# o de la red donde se escribe la ficha. Era B06: `localhost.localdomain` y
# `127.0.0.1` señalan el mismo archivo del corpus servido por un
# `python -m http.server`, y eso reabría N1 entero.
TLD_RESERVADOS = frozenset({
    "localhost", "localdomain", "local", "internal", "intranet", "lan",
    "home", "corp", "private", "test", "example", "invalid", "onion", "alt",
})

# Los ejes con los que el pack decide una consulta, enumerados una sola vez.
# Es la pieza central del rediseño del token (B01): el token registra la
# consulta ENTERA y no una selección de campos, así que un eje nuevo entra en
# la prueba de banco por añadirlo aquí y no por acordarse de tocar
# `_emitir_token` y `verificar_token` a la vez. La ronda anterior cerró dos de
# los cinco —la fecha del caso y su tipo (A03, A07)— y dejó los otros tres,
# que es lo que costó B01: la materia y el nivel territorial se comprobaban en
# `responder` y se evaporaban en la única puerta que llega a la publicación.
EJES_DE_CONSULTA = ("identificador", "peticion", "proposicion", "fecha_del_caso",
                    "tipo_de_fecha", "materia", "jurisdiccion", "nivel_territorial")

# El nivel territorial de una consulta que no dice ninguno. Un pack nacional
# contesta a una consulta que no declara nivel: el silencio es «nacional» y no
# «indeterminable», porque lo contrario dejaría sin respuesta a toda consulta
# que no conozca el manifiesto.
NIVEL_POR_DEFECTO = "nacional"
# El valor con que se lee un nivel escrito y no legible, o el `territorial`
# booleano de A06. La cadena vacía no puede coincidir con ningún nivel
# declarado —los declarados pasan por `_texto` y `_texto` nunca devuelve
# vacío—, de modo que «hay algo territorial y no sé qué» cae fuera sin
# necesidad de un centinela que alguien pudiera escribir dentro de una ficha.
NIVEL_SIN_NOMBRAR = ""

CODIGOS_CITABLES = frozenset({
    "CITABLE", "CITABLE_CON_REFORMA", "CITABLE_SIN_VIGENCIA_HOY", "CITABLE_PRECEDENTE",
})

# Una frase por código. La frase importa tanto como el código: el silencio se
# lee como «no hay regla», y esa lectura es el fallo que el pack existe para
# impedir. Ninguna afirma nada sobre el mundo: todas hablan del pack.
FRASES = {
    "CITABLE": "{id} — identidad comprobada; vigente dentro del alcance y de la ventana comprobadas.",
    "CITABLE_CON_REFORMA": "{id} — rige en redacción distinta de la original. La comprobación cubre el identificador y su vigencia, no la redacción.",
    "CITABLE_SIN_VIGENCIA_HOY": "{id} rigió dentro de la ventana comprobada y el caso cae dentro. Hoy no rige.",
    "CITABLE_PRECEDENTE": "{id} — identidad comprobada; sostiene la proposición atribuida en el pasaje registrado.",
    "FUERA_DE_LA_VIGENCIA_COMPROBADA": "Para la fecha de este caso, la comprobación firmada de {id} no la cubre. Qué regía en esa fecha es una pregunta que el pack no contesta.",
    "VIGENCIA_NO_COMPROBADA": "El pack tiene {id} y no tiene comprobada su vigencia. Eso no es lo mismo que decir que no rige, ni que sí.",
    "VIGENCIA_PARCIAL": "El pack tiene {id} con vigencia parcial comprobada; nunca se sirve como citable.",
    "IDENTIDAD_POR_VERIFICAR": "Nadie ha comprobado que {id} sea la norma que dice ser. Esto no es un problema de vigencia: es anterior.",
    "CONFLICTO_DE_FUENTES": "Dos fuentes oficiales discrepan sobre {id}. El pack no elige.",
    "CONFLICTO_ENTRE_FICHAS": "Dos fichas de {id} que cubren lo que se pide discrepan en la vigencia comprobada. Es un problema de vigencia, no de identidad, y el pack no elige.",
    "FUERA_DEL_ALCANCE_COMPROBADO": "Lo comprobado de {id} no llega hasta lo que se pide.",
    "PRECEDENTE_SUPERADO_O_LIMITADO": "{id} está marcada como superada o limitada, o en conflicto con otra.",
    "SIN_BUSQUEDA_ADVERSA": "Nadie buscó autoridad en contra de {id}, o la búsqueda quedó en JURISPRUDENCE_GAP. Un solo resultado no es una revisión.",
    "JURISPRUDENCIA_POR_VERIFICAR": "El pack tiene {id} y nadie ha revisado si sigue en pie.",
    "PACK_CADUCADO": "La ficha de {id} caducó. Lo que dice es lo que se comprobó el día de la firma, y desde entonces nadie lo ha vuelto a mirar.",
    "NO_ESTA_EN_EL_PACK": "El pack cubre esta área y no tiene {id}. Nadie la ha metido ni comprobado. No significa que no exista.",
    "FUERA_DE_COBERTURA": "El pack no cubre esta área, este nivel territorial o esta fecha. Aquí no hay información de ninguna clase.",
    "NO_TENEMOS_INFORMACION_SUFICIENTE": "No se puede saber si esto entra en lo que el pack cubre. Las dos lecturas están abiertas.",
    "FICHA_NO_FIRMADA": "La ficha de {id} no está firmada, o su firma no se puede leer. Un registro sin nombre y sin fecha está afirmado, no comprobado.",
    "FICHA_INCOMPLETA": "La ficha de {id} deja vacía una casilla que su propio estado hace obligatoria.",
    "EL_PACK_NO_CONTESTA": "La consulta no trae fecha del caso y tipo de fecha. Sin las dos, el pack no contesta.",
}


# ──────────────── §B. Lectura defensiva de casillas ────────────────
# Todo lo de esta sección es total: recibe lo que haya —None, un número, una
# lista, el relleno del instrumento— y devuelve un valor utilizable o None.
# Nunca levanta. Un dato que no se puede leer no es un error del pack: es una
# casilla que no se llenó, y una casilla que no se llenó nunca es citable.

def _texto(valor):
    """La cadena limpia, o None si no hay nada utilizable en la casilla."""
    if not isinstance(valor, str):
        return None
    v = valor.strip()
    if not v or v in RELLENOS:
        return None
    return v


def _fecha(valor):
    """`AAAA-MM-DD` estricto y dentro del calendario útil → date. Cualquier
    otra cosa → None.

    Estricto significa estricto: `2 de enero`, `AAAA-MM-DD`, `1000-13-01` y
    una cadena vacía valen lo mismo, que es nada. Una fecha que no se puede
    leer no puede compararse, y lo que no se puede comparar cae fuera.

    Y `9999-01-01` tampoco se puede comparar, aunque el módulo `datetime` la
    lea: sumarle la cadencia sale del calendario y **levanta**. El encabezado
    promete que ninguna función de este archivo levanta por un dato malo, y
    esa promesa se cumple aquí, en la frontera, o no se cumple en ninguna
    parte —A11 entraba por ahí y tumbaba `cobertura`, `recuento`, `degradado`,
    `apagado` y la consulta sobre las fichas sanas del mismo pack—.
    """
    if isinstance(valor, datetime):
        f = valor.date()
    elif isinstance(valor, date):
        f = valor
    else:
        v = _texto(valor)
        if v is None:
            return None
        try:
            f = datetime.strptime(v, "%Y-%m-%d").date()
        except ValueError:
            return None
    return f if ANIO_MINIMO <= f.year <= ANIO_MAXIMO else None


def _reloj(hoy):
    """El día en que se pregunta, leído por la misma puerta que las casillas.

    B10: `hoy` era la única fecha del contrato que no pasaba por `_fecha`.
    Entraba cruda en `evaluar`, `caducada`, `responder`, `verificar_token` y
    `apagado`, y se comparaba con fechas de ficha que sí habían pasado. Un
    `datetime` —lo que devuelve `datetime.now()`, el error de tecleo más
    barato que hay— levantaba `TypeError` y dejaba el pack sin contestar a
    nada, ni siquiera a las consultas sobre las fichas sanas: el daño exacto
    de A11, por la puerta que A11 no cerró.

    La asimetría era lo que lo delataba: el mismo `datetime` DENTRO de una
    ficha se leía sin problema. Aquí se lee igual, y por eso esta función no
    hace nada más que llamar a `_fecha`: existe para que la frontera se vea y
    se pueda buscar, no para inventar una segunda regla de lectura.
    """
    return _fecha(hoy)


def tipo_de(ficha):
    """`norma`, `providencia` o None. El único lector de `tipo` que hay.

    A09: `evaluar` lo normalizaba con `_texto` y `cadencia_de`,
    `_citable_en_si`, `recuento` y `verificar_token` lo comparaban con `==`
    crudo. Un espacio alrededor bastaba para que la misma ficha fuera una cosa
    para la tabla de decisión y otra para la prueba de banco. Los espacios se
    recortan en TODOS los campos por igual: ese recorte uniforme es lo que
    hace que «   » valga como vacío, y aquí vale lo mismo que en el resto.
    """
    if not isinstance(ficha, dict):
        return None
    t = _texto(ficha.get("tipo"))
    return t if t in TIPOS_DE_FICHA else None


def leer_materias(valor):
    """El conjunto de materias declaradas, o el conjunto vacío.

    A10: `cobertura` iteraba el campo sin mirar qué era, y una `materia`
    escrita en singular —`"civil"` en vez de `["civil"]`, el error de tecleo
    más barato de la ficha— hacía que el pack declarara cubiertas las
    **letras** del área. Una cadena es iterable; que lo sea no la convierte en
    una lista. Se exige la lista, y una casilla mala invalida la lista entera:
    media lista leída es una lista que nadie comprobó.
    """
    if not isinstance(valor, (list, tuple)):
        return frozenset()
    limpias = [_texto(m) for m in valor]
    if not limpias or any(m is None for m in limpias):
        return frozenset()
    return frozenset(limpias)


def leer_nivel_territorial(consulta):
    """El nivel territorial por el que se pregunta. Siempre una cadena.

    B07: el manifiesto publica el eje con el nombre `nivel_territorial` y
    `responder` preguntaba por `territorial`. Quien consumía el manifiesto y
    escribía en la consulta el nombre que el manifiesto le había enseñado no
    estaba declarando nada —su campo se ignoraba en silencio y el pack
    contestaba como si la consulta fuera nacional—.

    El nombre publicado manda, y `territorial` se conserva como su forma
    booleana porque A06 la dejó establecida y quitarla rompería una respuesta
    negativa que ya está en pie. Las dos formas entran por AQUÍ y por ningún
    otro sitio: dos maneras de escribir el mismo eje son tolerables mientras
    haya un solo lector que las resuelva; dos lectores no lo son, y eso era la
    vía.
    """
    if not isinstance(consulta, dict):
        return NIVEL_SIN_NOMBRAR
    crudo = consulta.get("nivel_territorial")
    if isinstance(crudo, (list, tuple)):
        # Se lee con el mismo lector total de las materias: una lista de
        # cadenas limpias o nada. Varios niveles a la vez no son un nivel.
        leidos = leer_materias(crudo)
        nombrado = sorted(leidos)[0] if len(leidos) == 1 else None
    else:
        nombrado = _texto(crudo)
    if nombrado is not None:
        return nombrado
    if crudo is not None:
        return NIVEL_SIN_NOMBRAR      # había algo escrito y no se pudo leer
    return NIVEL_SIN_NOMBRAR if consulta.get("territorial") else NIVEL_POR_DEFECTO


def leer_consulta(consulta):
    """La consulta entera leída de una sola vez, eje por eje, o None si eso no
    es una consulta. Ninguna clave cruda se lee dos veces en dos sitios.

    Es el lector total que le faltaba a la consulta. Las fichas tenían cuatro
    —`_fecha`, `leer_materias`, `tipo_de`, la ventana de `leer_fuente`— y la
    consulta no tenía ninguno: cada camino sacaba las claves que necesitaba
    con `_texto` por su cuenta, y por eso el token pudo quedarse con dos de
    los cinco ejes sin que se notara (B01).
    """
    if not isinstance(consulta, dict):
        return None
    tipo_de_fecha = _texto(consulta.get("tipo_de_fecha"))
    return {
        "identificador": _texto(consulta.get("identificador")),
        "peticion": leer_alcance(consulta.get("peticion")),
        "proposicion": _texto(consulta.get("proposicion")),
        "fecha_del_caso": _fecha(consulta.get("fecha_del_caso")),
        "tipo_de_fecha": tipo_de_fecha if tipo_de_fecha in TIPOS_DE_FECHA else None,
        "materia": _texto(consulta.get("materia")),
        "jurisdiccion": _texto(consulta.get("jurisdiccion")),
        "nivel_territorial": leer_nivel_territorial(consulta),
    }


def mas_meses(f, meses):
    """`f` + n meses, recortando el día al último del mes de destino.

    Sin biblioteca externa: esto tiene que correr en la máquina de cualquiera.
    """
    total = f.year * 12 + (f.month - 1) + meses
    anio, mes = divmod(total, 12)
    mes += 1
    return date(anio, mes, min(f.day, calendar.monthrange(anio, mes)[1]))


def leer_estado_vigencia(valor):
    """`(nombre, fecha)` si el valor es uno de los cinco reconocidos, si no
    `(None, None)`.

    Estricto a propósito. `VIGENTE_AL` con un comentario detrás, con dos
    espacios, con un guion bajo cambiado por un espacio o sin su fecha **no
    es** `VIGENTE_AL`. La lista blanca se rompe entera si aquí se hace la
    vista gorda con una errata: eso era V3, y convertía cada errata en una
    autorización.
    """
    v = _texto(valor)
    if v is None:
        return (None, None)
    partes = v.split(" ")
    if len(partes) == 1:
        return (v, None) if v == VIGENCIA_NO_COMPROBADA else (None, None)
    if len(partes) != 2 or partes[0] not in ESTADOS_CON_FECHA:
        return (None, None)
    f = _fecha(partes[1])
    return (partes[0], f) if f else (None, None)


def leer_alcance(valor):
    """`{norma_completa, articulos, incisos}` → `(completa, articulos, incisos)`,
    o None si no es comparable.

    None quiere decir NO COMPARABLE, y no comparable es
    `FUERA_DEL_ALCANCE_COMPROBADO`. Prosa, un dict con claves de más o de
    menos, una lista de números en vez de cadenas: todo eso cae aquí. El
    algoritmo viejo fingía comparar dos cadenas de prosa y daba por bueno lo
    que no podía comparar.
    """
    if not isinstance(valor, dict) or set(valor) != {"norma_completa", "articulos", "incisos"}:
        return None
    completa = valor["norma_completa"]
    if completa in ("si", True):
        completa = True
    elif completa in ("no", False):
        completa = False
    else:
        return None
    listas = []
    for clave in ("articulos", "incisos"):
        elementos = valor[clave]
        if not isinstance(elementos, (list, tuple)):
            return None
        limpios = [_texto(e) for e in elementos]
        if any(e is None for e in limpios):
            return None
        listas.append(frozenset(limpios))
    return (completa, listas[0], listas[1])


def contenido_en(peticion, alcance):
    """¿`peticion` ⊆ `alcance`? True o False. Cualquier duda es False.

    Contención estricta de conjuntos, nivel por nivel: un inciso solo está
    cubierto si está escrito en `incisos`. Comprobar el art. 00 **no** cubre
    el inciso 00.0. La crítica avisa de que la lectura jurídica natural diría
    lo contrario y de que el documento no elige ninguna: aquí se elige la que
    se niega más, porque es la única que no depende de que alguien lea bien.

    Y una petición que no pide nada no está contenida en nada: si valiera
    como contenida, preguntar por el vacío devolvería citable.
    """
    if peticion is None or alcance is None:
        return False
    p_completa, p_articulos, p_incisos = peticion
    a_completa, a_articulos, a_incisos = alcance
    if not p_completa and not p_articulos and not p_incisos:
        return False
    if a_completa:
        return True          # se comprobó la norma entera: cubre cualquier petición
    if p_completa:
        return False         # se pide la norma entera habiendo comprobado un trozo: V1
    return p_articulos <= a_articulos and p_incisos <= a_incisos


def _referencia_publicada(referencia):
    """¿La referencia señala algo publicado fuera de este proyecto?

    `01` §5 regla 3 y `04` §7: mover una afirmación de un archivo del corpus a
    una ficha no la comprueba. Es el mecanismo exacto de N1 —el renombrado
    deja escrita la cadena `IDENTIDAD_VERIFICADA` en el catálogo, al lado de
    cada norma, en un campo marcado copiable— y también el de la cuarentena
    de P0.b.

    ESTA FUNCIÓN ERA LA ÚNICA LISTA NEGRA DEL CONTRATO, y A17 la rodeó con lo
    primero que se le ocurrió: quitar la extensión del archivo, escribirlo con
    la barra de Windows, ponerle `.markdown`, o no nombrar archivo ninguno
    —«ver la ficha anterior», «consultado internamente»—. Una lista negra deja
    fuera lo que no se pensó, y lo que no se pensó es infinito.

    Ahora se enumera lo que se ACEPTA: un esquema y un nombre de dominio del
    DNS público. Con eso, «no es del corpus» deja de ser una conjetura sobre
    la forma del nombre y pasa a ser una propiedad comprobable de la
    referencia. El coste queda dicho, porque es real: una referencia legítima
    que no sea una URL —el ejemplar en papel de un diario oficial— se rechaza
    y obliga a rehacer la ficha con el enlace de la publicación. Rechazar de
    más cuesta trabajo; aceptar de más cuesta una cita fabricada.

    B06 — «un dominio con punto» no era un nombre de dominio. `localhost` se
    rechazaba por accidente, por no llevar punto, y no porque la función
    supiera lo que es: bastaba el bucle local escrito con números, el nombre
    largo de la misma máquina o cualquier dirección privada, y el archivo del
    corpus servido por un `python -m http.server` volvía a ser una fuente
    «publicada», o sea N1 entero otra vez. Ahora el nombre tiene que ser un
    nombre —etiquetas del alfabeto del DNS, dos o más, y un primer nivel
    alfabético—, lo que deja fuera todo literal IP sin nombrar ninguno, y su
    primer nivel no puede ser de los que los estándares apartan del DNS
    público.

    QUEDA DICHO LO QUE ESTA FUNCIÓN NO HACE, porque la promesa de su nombre es
    más grande que su cuerpo: comprueba la FORMA de un nombre público, no que
    haya algo publicado detrás. Saber lo segundo exige la red, y este archivo
    tiene que correr en la máquina de cualquiera sin dependencias. La lista
    blanca sube el precio de la referencia inventada; no lo hace infinito.
    """
    r = _texto(referencia)
    if r is None:
        return False
    if any(c.isspace() for c in r) or "\\" in r or ".." in r:
        return False
    minusculas = r.lower()
    for esquema in ESQUEMAS_PUBLICADOS:
        if minusculas.startswith(esquema):
            autoridad = r[len(esquema):].split("/")[0].split("?")[0].split("#")[0]
            break
    else:
        return False
    return _dominio_publicado(autoridad)


def _dominio_publicado(autoridad):
    """¿La autoridad de la URL es un nombre de dominio del DNS público?"""
    # Credenciales dentro de la autoridad: además de no ser una forma en que
    # se publique nada, `http://ejemplo.invalido@127.0.0.1/` pone un nombre
    # creíble delante de la máquina de uno. Lo que decide es lo de después
    # de la arroba, así que aquí no hay nada que leer.
    if "@" in autoridad:
        return False
    host, hay_puerto, puerto = autoridad.partition(":")
    if hay_puerto and not (puerto and all(c in ASCII_DIGITOS for c in puerto)):
        return False
    etiquetas = host.lower().split(".")
    if len(etiquetas) < 2:
        return False
    for etiqueta in etiquetas:
        if not 1 <= len(etiqueta) <= 63 or etiqueta[0] == "-" or etiqueta[-1] == "-":
            return False
        if any(c not in CARACTERES_DE_ETIQUETA for c in etiqueta):
            return False
    # El primer nivel alfabético es lo que descarta los literales IP sin
    # tener que reconocerlos: `127.0.0.1` y `0.0.0.0` terminan en un número, y
    # `[::1]` no pasa el alfabeto de las etiquetas. Se niega por lo que el
    # nombre ES, no por parecerse a una dirección conocida.
    tld = etiquetas[-1]
    if not 2 <= len(tld) <= 24 or any(c not in ASCII_LETRAS for c in tld):
        return False
    return tld not in TLD_RESERVADOS


def leer_fuente(valor, clases_admitidas, ventana):
    """`{clase, referencia, consultada}` → la clase, o None si la fuente no
    sirve para lo que se le pide.

    Tipada y aparte, nunca la clase escrita dentro de la cadena de la URL:
    una cadena que contiene las letras `PRIMARY_OFFICIAL` no es una fuente
    primaria, y esa confusión era media vía V3.

    `ventana` es `(desde, hasta)` y es A12. `consultada` no tenía ni techo ni
    suelo: una ficha firmada ayer podía declarar que consultó la fuente
    oficial en el año 9999, o hace un siglo, y salía citable. La cadencia
    medía la edad de la firma y nada medía la edad de lo que se firmó. Los dos
    bordes salen de lo que el pack ya dice, sin constantes nuevas: nadie
    consulta el futuro (`hasta` = hoy), y una consulta anterior a la ventana
    de revisión de la propia ficha es, por la política del propio pack, una
    consulta vencida (`desde` = firma − cadencia).
    """
    if not isinstance(valor, dict) or set(valor) != {"clase", "referencia", "consultada"}:
        return None
    clase = _texto(valor["clase"])
    referencia = _texto(valor["referencia"])
    if clase not in CLASES_DE_FUENTE or clase not in clases_admitidas:
        return None
    if referencia is None or not _referencia_publicada(referencia):
        return None
    consultada = _fecha(valor["consultada"])
    if consultada is None:
        return None
    desde, hasta = ventana
    if desde is None or hasta is None or not (desde <= consultada <= hasta):
        return None
    return clase


# ───────────────────── §C. La cuenta de la caducidad ─────────────────────

CADENCIA_MESES = 12                  # `02` §6, fila 1. Política operativa, no derecho.
CADENCIA_CORTA_MESES = 3             # `02` §6, fila 3.
CADENCIA_PROVIDENCIA_MESES = 12      # N3: la tabla de cadencias no tenía fila para ellas.


def obliga_nota(ficha):
    """¿El estado de esta ficha hace obligatoria la `nota_de_vigencia`?

    Dos casos, y el segundo es A15. El primero es la constante
    `ESTADOS_QUE_OBLIGAN_NOTA` de `01` §2. El segundo es
    `SIN_VIGENCIA_DESDE` con fecha **posterior a la firma**: eso no es una
    norma que dejó de regir, es una cesación anunciada que el día de la
    comprobación todavía no había ocurrido, que es literalmente la fila 3 de
    la tabla de cadencias («la nota registra un cambio con fecha futura»).
    Se compara contra la firma y no contra `hoy` a propósito: la cadencia no
    puede depender del día en que se lea, o la misma ficha caducaría o no
    según cuándo se la mire.
    """
    estado, fecha_estado = leer_estado_vigencia(ficha.get("estado_vigencia"))
    if estado in ESTADOS_QUE_OBLIGAN_NOTA:
        return True
    firmado = _fecha(ficha.get("verificado_el"))
    return (estado == SIN_VIGENCIA_DESDE and firmado is not None
            and fecha_estado > firmado)


def cadencia_de(ficha):
    """Los meses que vale la firma de esta ficha. Siempre un número.

    Tres decisiones que la prosa no cierra, y aquí hay que cerrarlas:

    N6 — la fila 3 de la tabla («la nota registra un cambio con fecha futura…
    o el día anterior a esa fecha futura si es antes») exige leer la nota y
    extraerle una fecha, y `01` campo 9 prohíbe interpretarla. Las dos no
    pueden ser verdad. Se resuelve sin leerla: **si hay nota, cadencia corta**.
    La fecha exacta la aporta la verificadora en `acortamiento_manual`, que es
    justo lo que P5 ya le manda hacer. Coste: `VIGENTE_CON_REFORMA_AL`, que
    obliga a nota, vence a los tres meses y no a los doce. Es el lado seguro.

    N8 — `SIN_VIGENCIA_DESDE` tenía cadencia «no aplica», que en código
    significa inmortal. Ninguna ficha puede ser inmortal: la comprobación
    puede haber sido sincera y equivocada, y `CITABLE_SIN_VIGENCIA_HOY` se
    serviría para siempre.

    N3 — las providencias no tenían ninguna fila, porque la tabla entera está
    escrita sobre `estado_vigencia`, campo que una providencia no tiene.

    A18 — la cadencia colgaba SOLO de que la nota estuviera, y entonces
    dejarla vacía la alargaba de tres meses a doce: la ficha peor llenada era
    la que más vivía. Se añadió la obligación, que es un hecho del estado, al
    lado de la casilla, que es un hecho de quien la llenó.

    B04 dijo que ese `or` era una vía y que la cadencia tenía que colgar solo
    de la obligación, «como este docstring dice que hace». Lo segundo era
    verdad —el párrafo anterior estaba escrito como si A18 hubiera sustituido
    la regla de N6 en vez de sumarse a ella, y ese es el defecto que había que
    arreglar aquí— y lo primero no: la casilla manda porque N6 lo decidió y
    tiene test. Las dos condiciones son independientes y las dos acortan:

      - N6 dice que **si hay nota, cadencia corta**, y con eso resuelve una
        contradicción del instrumento, no un descuido. Quitarla devolvería a
        doce meses la ficha que su autora marcó con algo pendiente.
      - A18 dice que el estado que OBLIGA a nota acorta aunque la casilla esté
        vacía, para que no llenarla no premie.

    La objeción de fondo de B04 —quitar información de una ficha ensancha lo
    que se acepta de ella— es real y no tiene arreglo por este lado: la ficha
    sin nota no dice menos, dice otra cosa, y lo que dice es «no hay nada
    pendiente», que es exactamente la fila 1 de la tabla. Un contrato no puede
    leer la nota que nadie escribió, y darle a la ficha sin nota una cadencia
    más corta que doce dejaría la fila 1 sin ningún caso. Lo que sí se puede
    hacer, y se hace, es que ninguna de las dos condiciones pueda desaparecer
    sin que un test lo diga.
    """
    if tipo_de(ficha) == "providencia":
        return CADENCIA_PROVIDENCIA_MESES
    if obliga_nota(ficha) or _texto(ficha.get("nota_de_vigencia")):
        return CADENCIA_CORTA_MESES
    return CADENCIA_MESES


def revisar_antes_de(ficha):
    """La cuenta de `02` §6, hecha total: una fecha, o None si no se puede
    calcular —y no poderla calcular es una ficha caducada, nunca una viva—.

    `min(verificado_el + cadencia, acortamiento_manual)` no es una función
    total: `acortamiento_manual: null` es el valor de la ficha de ejemplo del
    propio instrumento, y `min` sobre indefinidos no está definido (N8). Aquí
    el acortamiento participa solo si es una fecha legible, y solo si adelanta:
    una fecha posterior a la calculada se ignora, porque cuando era escribible
    una sola casilla hacía inmortal una ficha.
    """
    firmado = _fecha(ficha.get("verificado_el"))
    if firmado is None:
        return None
    calculada = mas_meses(firmado, cadencia_de(ficha))
    acortamiento = _fecha(ficha.get("acortamiento_manual"))
    if acortamiento is not None and acortamiento < calculada:
        return acortamiento
    return calculada


def caducada(ficha, hoy):
    """True si esta ficha ya no se sirve. La degradación es el resultado por
    defecto de no hacer nada: nadie tiene que leer un aviso.

    Incluye la firma, y no solo su aritmética: una firma futura da una fecha
    de revisión futura y por tanto una ficha «viva» para todo el que pregunte
    por la caducidad —`recuento`, `cobertura`, la prueba de banco— mientras
    `_evaluar_norma` la rechaza. Que dos partes del pack cuenten distinto la
    misma ficha es el patrón de A09 y de A11; aquí hay un solo predicado.

    B10 — el reloj entra por `_reloj` como cualquier otra fecha. Un día que no
    se puede leer no da un `TypeError`: da una ficha caducada, que es el «no»
    de esta función. Sin reloj no se puede sostener que una firma siga
    valiendo, y una firma que no se puede sostener no se sirve.
    """
    dia = _reloj(hoy)
    if dia is None:
        return True
    if _firma_valida(ficha, dia) is None:
        return True
    limite = revisar_antes_de(ficha)
    return limite is None or dia > limite


# ───────────────────────── §D. La respuesta ─────────────────────────

class Respuesta(object):
    """Un código, un motivo técnico, la frase que lee ella y —si es citable—
    su token. `nota` viaja transcrita literal, sin interpretar, en toda
    respuesta que hable de una ficha con nota.

    B08 — esa promesa era falsa. `nota` se asignaba aquí y no la consultaba
    ninguna línea del archivo: ni `frase`, ni `RespuestaCompuesta.frase`, ni
    el token. La casilla que `obliga_nota` cobra —sin ella, `FICHA_INCOMPLETA`—
    no se servía en ninguna parte, así que la ficha que declara que la norma
    deja de regir dentro de cinco años y la que no declara nada producían el
    mismo código y la misma frase, carácter por carácter. Es el silencio que
    `FRASES` dice existir para impedir: el silencio se lee como «no hay
    regla».

    Se transcribe LITERAL y se dice que es transcrita. No se resume, no se
    interpreta y no se convierte en un código: `01` campo 9 prohíbe leerla, y
    servirla entre comillas es la única forma de respetar las dos cosas —que
    llegue y que nadie la haya interpretado por el camino—.
    """

    def __init__(self, codigo, motivo, ficha=None, nota=None):
        self.codigo = codigo
        self.motivo = motivo
        self.ficha = ficha
        self.nota = nota
        self.token = None            # lo estampa el pack: solo él tiene el registro
        self.identificador = identificador_de(ficha) if ficha is not None else ""
        self.frase = FRASES.get(codigo, "").format(id=self.identificador or "la ficha")
        transcribible = _texto(nota)
        if transcribible is not None and self.frase:
            self.frase += " Nota de la ficha, transcrita: «%s»" % transcribible

    @property
    def citable(self):
        return self.codigo in CODIGOS_CITABLES

    def __repr__(self):
        return "Respuesta(%s, %s)" % (self.codigo, self.motivo)


def identificador_de(ficha):
    """El identificador de una ficha, del campo que le toque según su tipo."""
    if not isinstance(ficha, dict):
        return ""
    return (_texto(ficha.get("identificador_canonico"))
            or _texto(ficha.get("identificador")) or "")


# ─────────── §E. La tabla de decisión: A para normas, B para providencias ───────────

def _consulta_incompleta(consulta):
    """R3: sin `fecha_del_caso` y `tipo_de_fecha`, el pack no contesta.

    Las dos las aporta quien consulta, tomadas de la carpeta del caso. Una
    norma no es vigente o no vigente: lo es *para una fecha*, y «la fecha del
    caso» no existe en singular.

    Lee por `leer_consulta` y no por su cuenta: la consulta se lee en un solo
    sitio, que es la mitad del rediseño de B01.
    """
    ejes = leer_consulta(consulta)
    if ejes is None:
        return "la consulta no es una consulta"
    if ejes["fecha_del_caso"] is None:
        return "falta `fecha_del_caso` o no es una fecha legible"
    if ejes["tipo_de_fecha"] is None:
        return "falta `tipo_de_fecha` o no es uno del vocabulario de `05`"
    return None


def _firma_valida(ficha, hoy):
    """La firma, o None. Sin firma no hay ficha —no hay una ficha a medias—.

    Cierra dos campos que la prosa dice leer y no leía: `verificado_por` vacío
    (la ficha anónima salía citable e imprimía «Comprobado por » con el hueco)
    y `verificado_el` inválido o futuro (inválido rompía el cálculo de la
    caducidad sin resultado definido; futuro hacía la ficha inmortal).
    """
    quien = _texto(ficha.get("verificado_por"))
    cuando = _fecha(ficha.get("verificado_el"))
    if quien is None or cuando is None or cuando > hoy:
        return None
    return (quien, cuando)


def ventana_de_consulta(ficha, hoy):
    """`(desde, hasta)`: cuándo pudo consultarse una fuente para que valga
    como la fuente de ESTA ficha. Ver `leer_fuente`. `(None, None)` si la
    firma no se puede leer, y con eso ninguna fuente pasa."""
    firmado = _fecha(ficha.get("verificado_el"))
    if firmado is None:
        return (None, None)
    return (mas_meses(firmado, -cadencia_de(ficha)), hoy)


def _identidad(ficha, hoy, clases_admitidas):
    """A.2 / B.2. Devuelve None si la identidad pasa, o la Respuesta que la
    frena. Un fallo de identidad nunca se sirve bajo un código de vigencia.

    `hoy` llegaba a esta función y no se usaba en ninguna línea —era la huella
    de la comprobación que se quiso hacer y no se hizo—. Ahora acota por
    arriba la fecha de consulta de la fuente: A12.
    """
    estado = _texto(ficha.get("estado_identidad"))
    if estado == CONFLICTO_DE_FUENTES:
        return Respuesta(CONFLICTO_DE_FUENTES, "dos fuentes oficiales discrepan; el pack no elige", ficha)
    if estado != IDENTIDAD_VERIFICADA:
        return Respuesta(IDENTIDAD_POR_VERIFICAR, "estado_identidad no es IDENTIDAD_VERIFICADA", ficha)
    if leer_fuente(ficha.get("fuente_identidad"), clases_admitidas,
                   ventana_de_consulta(ficha, hoy)) is None:
        return Respuesta(IDENTIDAD_POR_VERIFICAR,
                         "fuente_identidad vacía, de clase inadmisible, sin referencia publicada "
                         "o consultada fuera de la ventana de la ficha", ficha)
    return None


def _materia(ficha, consulta, nota=None):
    """A06. La materia por la que se pregunta tiene que estar entre las que la
    ficha declara. Devuelve None si pasa, o la Respuesta que la frena.

    `materia` y `territorial` decidían la respuesta en la rama C —«no tengo
    esa ficha»— y desaparecían en cuanto había coincidencia. El pack se
    contradecía en la misma sesión: para un identificador que no tenía decía
    «no cubro esta área, aquí no hay información de ninguna clase»; para uno
    que sí tenía, en esa misma área, decía `CITABLE`. El encabezado declaraba
    cerrada esta vía al añadir `materia[]` a las providencias: el campo se
    añadió y no se comparaba con nada.

    Los dos códigos son distintos a propósito. Que la consulta no diga en qué
    materia pregunta deja las dos lecturas abiertas; que la diga y la ficha no
    la declare es una respuesta cerrada, y es la misma que la de un alcance
    que no llega: lo comprobado no cubre lo que se pide.
    """
    pedida = _texto(consulta.get("materia"))
    if pedida is None:
        return Respuesta("NO_TENEMOS_INFORMACION_SUFICIENTE",
                         "la consulta no dice en qué materia pregunta", ficha, nota)
    if pedida not in leer_materias(ficha.get("materia")):
        return Respuesta("FUERA_DEL_ALCANCE_COMPROBADO",
                         "la ficha no declara la materia por la que se pregunta", ficha, nota)
    return None


def _evaluar_norma(ficha, consulta, hoy):
    """La rama A. Siete condiciones en la prosa; nueve aquí, y las dos de más
    son las dos vías que la prosa dejaba abiertas (V2 y N2)."""
    fecha_caso = _fecha(consulta.get("fecha_del_caso"))
    nota = _texto(ficha.get("nota_de_vigencia"))

    if _firma_valida(ficha, hoy) is None:
        return Respuesta("FICHA_NO_FIRMADA", "verificado_por vacío, o verificado_el ilegible o futuro", ficha)

    # A.1 — caducidad. Va primero porque una ficha caducada no dice nada, ni
    # siquiera lo que dijo bien el día que se firmó.
    if caducada(ficha, hoy):
        return Respuesta("PACK_CADUCADO", "hoy es posterior a revisar_antes_de", ficha, nota)

    # A.2 — identidad, con su fuente. Antes de la vigencia: es anterior.
    frenada = _identidad(ficha, hoy, CLASES_DE_IDENTIDAD_NORMA)
    if frenada is not None:
        return frenada

    # A.2.bis — la materia (A06). Va con el alcance porque es lo mismo que el
    # alcance: hasta dónde llega lo comprobado.
    frenada = _materia(ficha, consulta, nota)
    if frenada is not None:
        return frenada

    # A.3 — contención de alcance en las DOS direcciones (V1). El operando
    # izquierdo llega tipado desde la consulta y nunca lo produce el modelo:
    # una `peticion` en prosa no es comparable, y no comparable cae fuera.
    if not contenido_en(leer_alcance(consulta.get("peticion")), leer_alcance(ficha.get("alcance_comprobado"))):
        return Respuesta("FUERA_DEL_ALCANCE_COMPROBADO",
                         "la petición no está contenida en alcance_comprobado, o no son comparables", ficha, nota)

    # A.4 — estado de vigencia, leído como lista blanca.
    estado, fecha_estado = leer_estado_vigencia(ficha.get("estado_vigencia"))

    # Casilla obligatoria vacía. Va ANTES del corte de la vigencia parcial, y
    # ese orden es A18: `VIGENCIA_PARCIAL_AL` retornaba cuatro líneas antes,
    # así que la mitad de `ESTADOS_QUE_OBLIGAN_NOTA` era inalcanzable y su
    # única consecuencia visible era la cadencia. Sin la nota,
    # `CITABLE_CON_REFORMA` sale afirmando una reforma de la que no dice nada,
    # y una ficha parcial sin nota no dice en qué parte rige.
    if obliga_nota(ficha) and nota is None:
        return Respuesta("FICHA_INCOMPLETA", "el estado obliga a nota_de_vigencia y está vacía", ficha)

    if estado == VIGENCIA_PARCIAL_AL:
        return Respuesta("VIGENCIA_PARCIAL", "rige en parte; nunca se sirve como citable", ficha, nota)
    if estado not in ESTADOS_QUE_PUEDEN_SER_CITABLES:
        return Respuesta(VIGENCIA_NO_COMPROBADA,
                         "estado_vigencia vacío o no reconocido", ficha, nota)

    # A.5 — la fuente de la vigencia, tipada, de clase primaria y consultada
    # dentro de la ventana de la propia ficha (A12).
    if leer_fuente(ficha.get("fuente_vigencia"), CLASES_DE_VIGENCIA,
                   ventana_de_consulta(ficha, hoy)) is None:
        return Respuesta(VIGENCIA_NO_COMPROBADA,
                         "fuente_vigencia vacía, de clase distinta de PRIMARY_OFFICIAL, sin "
                         "referencia publicada o consultada fuera de la ventana de la ficha",
                         ficha, nota)

    # A.5.bis — V2, el hallazgo principal. Sin constancia de que la reforma se
    # buscó, `VIGENTE_AL` escrito tras buscarla es indistinguible de
    # `VIGENTE_AL` escrito sin mirarla. El defecto es el inseguro: cualquier
    # cosa distinta del `si` literal no comprueba nada.
    if _texto(ficha.get("reforma_buscada")) != "si":
        return Respuesta(VIGENCIA_NO_COMPROBADA,
                         "no consta que se buscara reforma dentro del alcance", ficha, nota)

    # A.6 — desde cuándo. `ESCALONADA` no es una fecha y no se puede comparar.
    desde = _fecha(ficha.get("vigencia_desde"))
    if desde is None or fecha_caso < desde:
        return Respuesta("FUERA_DE_LA_VIGENCIA_COMPROBADA",
                         "vigencia_desde no es una fecha comparable, o el caso es anterior", ficha, nota)

    # A.7 — hasta cuándo, cuando la norma dejó de regir.
    if estado == SIN_VIGENCIA_DESDE and not fecha_caso < fecha_estado:
        return Respuesta("FUERA_DE_LA_VIGENCIA_COMPROBADA",
                         "el caso no es anterior a la fecha en que la norma dejó de regir", ficha, nota)

    # A.8 — N2. La ventana se comprobaba por un solo lado: nada acotaba el
    # caso por arriba, y con cadencia de doce meses se servía como comprobado
    # hasta un año de vigencia que nadie miró. El techo es el día de la
    # comprobación, que es hasta donde llega lo que la verificadora firmó.
    _, firmado = _firma_valida(ficha, hoy)
    techo = firmado if estado == SIN_VIGENCIA_DESDE else min(firmado, fecha_estado)
    if fecha_caso > techo:
        return Respuesta("FUERA_DE_LA_VIGENCIA_COMPROBADA",
                         "el caso es posterior al día hasta el que llega la comprobación firmada", ficha, nota)

    # A.9 — qué código. A15: `CITABLE_SIN_VIGENCIA_HOY` es la única frase del
    # contrato que afirma algo sobre el mundo —«Hoy no rige»— y se servía sin
    # comprobar la afirmación. `SIN_VIGENCIA_DESDE` con fecha futura es la
    # forma normal de una derogatoria de vigencia diferida: la norma sí rige
    # hoy, y la ficha lo dice. Se elige comprobar la afirmación antes de
    # hacerla, no callarla: si la cesación no ha ocurrido, lo comprobado es
    # que la norma regía en la ventana, que es exactamente lo que dice
    # `CITABLE`, y la cesación anunciada viaja en la nota que `obliga_nota` ya
    # hizo obligatoria. `hoy` y no la firma, porque la frase habla del día en
    # que se sirve.
    if estado == SIN_VIGENCIA_DESDE:
        codigo = "CITABLE_SIN_VIGENCIA_HOY" if fecha_estado <= hoy else "CITABLE"
    else:
        codigo = {VIGENTE_AL: "CITABLE",
                  VIGENTE_CON_REFORMA_AL: "CITABLE_CON_REFORMA"}[estado]
    return Respuesta(codigo, "cumple las diez condiciones", ficha, nota)


def _evaluar_providencia(ficha, consulta, hoy):
    """La rama B. No entra por A y no puede: no tiene `estado_vigencia`, ni
    `vigencia_desde`, ni `alcance_comprobado`, y una tabla de normas la
    atraviesa entera sin tocarla —eso era V4—."""
    if _firma_valida(ficha, hoy) is None:
        return Respuesta("FICHA_NO_FIRMADA", "verificado_por vacío, o verificado_el ilegible o futuro", ficha)

    # B.1 — caducidad con cadencia propia (N3). Sin ella una providencia
    # firmada hoy seguía siendo citable dentro de quince años.
    if caducada(ficha, hoy):
        return Respuesta("PACK_CADUCADO", "hoy es posterior a revisar_antes_de", ficha)

    frenada = _identidad(ficha, hoy, CLASES_DE_IDENTIDAD_PROVIDENCIA)
    if frenada is not None:
        return frenada

    # B.2.bis — la materia (A06). Es el motivo por el que `materia[]` se le
    # añadió a la providencia: sin comparar, el pack sirve un precedente en un
    # área que él mismo declara excluida.
    frenada = _materia(ficha, consulta)
    if frenada is not None:
        return frenada

    # El pasaje: campo que la prosa dice leer y no leía. Sin él la frase
    # servida dice «sostiene la proposición … en ‹›».
    if _texto(ficha.get("pasaje")) is None:
        return Respuesta("FICHA_INCOMPLETA", "pasaje vacío: nada sostiene la proposición atribuida", ficha)

    # B.3 — el mecanismo entero contra citar un precedente superado.
    estado_uso = _texto(ficha.get("estado_uso"))
    if estado_uso in ESTADOS_DE_USO_SUPERADOS:
        return Respuesta("PRECEDENTE_SUPERADO_O_LIMITADO", "estado_uso superado o en conflicto", ficha)
    if estado_uso not in ESTADOS_DE_USO_CITABLES:
        return Respuesta("JURISPRUDENCIA_POR_VERIFICAR", "estado_uso vacío o no reconocido", ficha)

    # B.4 — la búsqueda adversa. Se comprueba también el `JURISPRUDENCE_GAP`
    # dentro de la constancia, porque su forma honesta documentada es
    # «JURISPRUDENCE_GAP — buscada el …, la cobertura no alcanza».
    adversa = _texto(ficha.get("busqueda_adversa"))
    if adversa is None or "JURISPRUDENCE_GAP" in adversa:
        return Respuesta("SIN_BUSQUEDA_ADVERSA", "búsqueda adversa vacía o cerrada en JURISPRUDENCE_GAP", ficha)

    # B.5 — el techo temporal (A08). N2 cerró la ventana por arriba en la rama
    # A —«el techo es el día de la comprobación, hasta donde llega lo que la
    # verificadora firmó»— y B no leía `fecha_del_caso` en ninguna línea: un
    # precedente firmado hace un mes amparaba un caso fechado cincuenta años
    # después. La jurisprudencia cambia por el mismo eje por el que cambia la
    # vigencia, y la búsqueda adversa dice «no apareció autoridad en contra»
    # hasta el día en que se hizo y ni un día más.
    #
    # NO hay suelo, y la ausencia es deliberada: un precedente gobierna hechos
    # anteriores a él con toda normalidad, y ponerle un suelo exigiría saber
    # cuándo se dictó la providencia, que es un campo que `01` §4 no tiene.
    # Inventarlo sería el pack produciendo derecho.
    fecha_caso = _fecha(consulta.get("fecha_del_caso"))
    _, firmado = _firma_valida(ficha, hoy)
    if fecha_caso > firmado:
        return Respuesta("FUERA_DE_LA_VIGENCIA_COMPROBADA",
                         "el caso es posterior al día hasta el que llega la comprobación firmada",
                         ficha)

    # B.6 — la proposición, literal. Sin normalizar de ninguna forma: la
    # unidad no es la providencia, es el par providencia + proposición, y
    # cualquier tolerancia aquí la elige el intérprete generoso.
    pedida = _texto(consulta.get("proposicion"))
    if pedida is None or pedida != _texto(ficha.get("proposicion_atribuida")):
        return Respuesta("FUERA_DEL_ALCANCE_COMPROBADO",
                         "se comprobó para la proposición atribuida, no para la que se pide", ficha)

    return Respuesta("CITABLE_PRECEDENTE", "cumple las ocho condiciones", ficha)


def evaluar(ficha, consulta, hoy):
    """Una ficha, una consulta, una respuesta. El corazón del contrato.

    El tipo se **declara**, no se deduce de qué campos tiene la ficha.
    Deducirlo es exactamente V4: la providencia recorría la tabla de las
    normas y salía citable precisamente porque no tenía sus campos, y lo único
    que la atrapaba era un desajuste de cadena que el renombrado iba a borrar.

    El reloj se lee ANTES que nada (B10). Sin día no hay caducidad, no hay
    ventana de consulta y no hay techo temporal: las tres condiciones que
    separan «se comprobó» de «se afirmó» cuelgan de él, así que un reloj
    ilegible no puede dar más que un no.
    """
    dia = _reloj(hoy)
    if dia is None:
        return Respuesta("NO_TENEMOS_INFORMACION_SUFICIENTE",
                         "el día en que se pregunta no es una fecha legible",
                         ficha if isinstance(ficha, dict) else None)
    hoy = dia
    problema = _consulta_incompleta(consulta)
    if problema is not None:
        return Respuesta("EL_PACK_NO_CONTESTA", problema, ficha if isinstance(ficha, dict) else None)
    if not isinstance(ficha, dict):
        return Respuesta("NO_TENEMOS_INFORMACION_SUFICIENTE", "eso no es una ficha")
    tipo = tipo_de(ficha)
    if tipo == "norma":
        return _evaluar_norma(ficha, consulta, hoy)
    if tipo == "providencia":
        return _evaluar_providencia(ficha, consulta, hoy)
    return Respuesta("NO_TENEMOS_INFORMACION_SUFICIENTE",
                     "la ficha no declara si es norma o providencia", ficha)


# ─────────────────── §F. El pack: varias fichas, cobertura, tokens ───────────────────

MESES_DE_APAGADO = 18                 # `02` §6. Política operativa, no derecho.


class RespuestaCompuesta(object):
    """Lo que devuelve el pack a una consulta: una respuesta por ficha que
    coincide, más la regla de composición.

    N5 — R2 no estaba definida para respuesta múltiple, y el caso es el normal
    y no el raro: P2 empuja a estrechar, luego habrá varias fichas por norma.
    Las dos lecturas posibles eran «el turno se cierra pese a haber una
    citable» y «el consumidor se queda con la citable», que es el pack
    eligiendo la mejor coincidencia trasladado al consumidor. Aquí se elige la
    primera: **el conjunto es citable solo si lo son todas**. Ninguna respuesta
    se esconde —van todas—, pero nadie elige entre ellas.
    """

    def __init__(self, respuestas, codigo_de_composicion=None,
                 cobertura=None, recuento=None, degradado=False, apagado=False):
        self.respuestas = list(respuestas)
        self.codigo_de_composicion = codigo_de_composicion
        self.cobertura = cobertura or {}
        self.recuento = recuento or {}
        self.degradado = degradado
        self.apagado = apagado

    @property
    def codigos(self):
        return [r.codigo for r in self.respuestas]

    @property
    def citable(self):
        return (bool(self.respuestas) and self.codigo_de_composicion is None
                and all(r.citable for r in self.respuestas))

    @property
    def codigo(self):
        """Atajo para el caso de una sola ficha, que es el que se lee en los
        tests. Con varias, el código lo da la composición."""
        if self.codigo_de_composicion is not None:
            return self.codigo_de_composicion
        if len(self.respuestas) == 1:
            return self.respuestas[0].codigo
        return "MULTIPLE"

    @property
    def frase(self):
        """A16. «La frase importa tanto como el código: el silencio se lee
        como no hay regla, y esa lectura es el fallo que el pack existe para
        impedir.» El código de composición era una cadena suelta: la frase de
        `CONFLICTO_ENTRE_FICHAS` estaba escrita en `FRASES` y ningún camino la
        servía. Se servían las dos frases individuales, que no dicen que haya
        conflicto —una de ellas dice `CITABLE`—.
        """
        if self.codigo_de_composicion is not None:
            identificadores = [r.identificador for r in self.respuestas if r.identificador]
            return FRASES.get(self.codigo_de_composicion, "").format(
                id=identificadores[0] if identificadores else "la ficha")
        return "\n".join(r.frase for r in self.respuestas)

    def __repr__(self):
        return "RespuestaCompuesta(%s, citable=%s)" % (self.codigos, self.citable)


class Pack(object):
    """El pack: sus fichas, su cobertura calculada, su reloj y su registro de
    respuestas servidas.

    El pack no almacena estados: almacena afirmaciones fechadas y el estado se
    calcula al leer. Consecuencia buscada: si nadie lo mantiene, se apaga solo.
    """

    def __init__(self, fichas, curator="", version="0.0.0",
                 jurisdiccion="colombia", niveles_territoriales=("nacional",)):
        self.fichas = list(fichas)
        self.curator = curator
        self.version = version
        # B07 — los dos ejes que `cobertura` publicaba escritos a mano dentro
        # de la función. `"colombia"` era la misma cadena tuviera el pack las
        # fichas que tuviera, y ningún camino leía `consulta["jurisdiccion"]`:
        # el manifiesto enumeraba tres ejes y el contrato solo sabía decir que
        # no por uno de ellos. O se comparan o no se publican; se comparan, y
        # para eso tienen que ser del pack y no de una constante escondida.
        # Son del pack y no de las fichas a propósito: la competencia es una
        # declaración de quien cura, no un dato que se pueda deducir de los
        # registros que haya dentro.
        self.jurisdiccion = jurisdiccion
        self.niveles_territoriales = tuple(niveles_territoriales)
        self.registro = {}   # serie -> token servido. Sin esto no hay a qué
                             # resolver un token, y un token inventado pasa.

    # ── el reloj del pack ──

    def checksum(self):
        """Huella de las fichas. El manifiesto de `boundaries.md` la exige y
        sin ella un token no se puede resolver contra una versión del pack."""
        crudo = json.dumps(self.fichas, sort_keys=True, default=str, ensure_ascii=False)
        return hashlib.sha256(crudo.encode("utf-8")).hexdigest()[:16]

    def _huella(self):
        """Versión + checksum, la cadena que el token exhibe y que A04 demostró
        que nadie volvía a leer. Una sola función para escribirla y para
        comprobarla: si se escriben en dos sitios, se separan."""
        return "pack:%s@%s" % (self.version, self.checksum())

    def apagado(self, hoy):
        """N7 — el interruptor de los 18 meses.

        La prosa lo colgaba de `max(verificado_el)`, y entonces **una sola
        ficha nueva rejuvenece el reloj del pack entero**: verificar un
        registro cada diecisiete meses lo mantiene encendido con veinticinco
        fichas podridas dentro. Aquí cuelga de la **mediana**, que es la que
        contesta la pregunta que se quería hacer —¿hay alguien manteniendo
        esto?— y que una ficha sola no mueve. El mínimo sería aún más seguro,
        pero apaga el pack entero por un registro viejo que quizá ya no
        importa; queda dicho el trade-off.

        A13 y A14 — y la mediana sola no bastaba, porque contesta una pregunta
        parecida y no la que hay que hacer. «¿Cuándo se firmó?» no es «¿esto
        todavía sirve?»: bajando las veinticinco fichas podridas de veinte
        meses a diecisiete, la mediana queda por debajo del umbral, el
        interruptor no salta y el pack responde `CITABLE` con veinticinco de
        sus veintiséis registros caducados. Y las fichas cuya firma no se
        puede leer desaparecían del censo en vez de contar como las más
        viejas: cien fichas mudas y una recién hecha daban un pack encendido.

        Las dos las cierra la misma línea: **`degradado` gobierna**. Era un
        booleano que viajaba al lado de una respuesta citable y que ningún
        camino consultaba; ahora apaga. El coste, y es real: un pack con
        muchas fichas viejas que nadie consulta deja de contestar también
        sobre las pocas que sí se mantienen. Se elige ese lado porque la
        alternativa es un aviso que viaja pegado a un `CITABLE`, y un aviso
        pegado a un sí es un aviso que nadie lee.

        B10 — sin reloj legible el pack está apagado. No es una cortesía: la
        pregunta que contesta esta función es «¿hay alguien manteniendo
        esto?», y sin día no se puede contestar que sí.
        """
        dia = _reloj(hoy)
        if dia is None:
            return True
        firmas = [f for f in (_fecha(x.get("verificado_el")) for x in self.fichas) if f]
        if not firmas:
            return True
        mediana = date.fromordinal(int(statistics.median([f.toordinal() for f in firmas])))
        if dia > mas_meses(mediana, MESES_DE_APAGADO):
            return True
        return self.degradado(dia)

    def _citable_en_si(self, ficha, hoy):
        """Si la ficha pasa las condiciones que no dependen de la consulta.
        Es lo único contable sin una consulta delante, y así se dice.

        Una ficha sin materias legibles no es contable como citable: no hay
        ninguna consulta que pueda casar con ella (`_materia`), de modo que
        contarla sería contar una ficha que nunca se va a servir.

        B05 — ese razonamiento valía igual para otros dos campos y solo se
        había aplicado a la materia. Un `alcance_comprobado` ilegible hace que
        `contenido_en` sea False para toda petición, y un `vigencia_desde`
        ilegible hace que A.6 corte siempre: ninguno de los dos depende de la
        consulta y ninguno de los dos se miraba. La consecuencia no era de
        precisión sino de seguridad, porque este censo gobierna: `citables_hoy`
        es el denominador de `degradado` y `degradado` es el interruptor, así
        que **tres fichas que no se pueden servir jamás encendían un pack que
        sin ellas estaba apagado**, y de paso declaraban cubierta un área en la
        que el pack no podía contestar nada.

        La condición general, escrita una vez: es contable lo que alguna
        consulta podría llegar a hacer citable. Lo demás es inventario.
        """
        dia = _reloj(hoy)
        if dia is None:
            return False
        hoy = dia
        firma = _firma_valida(ficha, hoy)
        if firma is None or caducada(ficha, hoy):
            return False
        materias = leer_materias(ficha.get("materia"))
        if not materias:
            return False
        if tipo_de(ficha) == "providencia":
            # La fecha del caso es la de la firma y no `hoy`: es el techo de
            # B.5, o sea el último día para el que esta ficha puede contestar
            # que sí. Preguntar por `hoy` la haría incontable desde el día
            # siguiente a la firma.
            return _evaluar_providencia(
                ficha, {"proposicion": ficha.get("proposicion_atribuida"),
                        "fecha_del_caso": firma[1].isoformat(),
                        "tipo_de_fecha": "case_relevant_date",
                        "materia": sorted(materias)[0]}, hoy).citable
        estado, _ = leer_estado_vigencia(ficha.get("estado_vigencia"))
        return (estado in ESTADOS_QUE_PUEDEN_SER_CITABLES
                # B05, los dos campos que no dependen de la consulta y que
                # ninguna consulta puede salvar si no se pueden leer.
                and leer_alcance(ficha.get("alcance_comprobado")) is not None
                and _fecha(ficha.get("vigencia_desde")) is not None
                and not (obliga_nota(ficha) and _texto(ficha.get("nota_de_vigencia")) is None)
                and _identidad(ficha, hoy, CLASES_DE_IDENTIDAD_NORMA) is None
                and leer_fuente(ficha.get("fuente_vigencia"), CLASES_DE_VIGENCIA,
                                ventana_de_consulta(ficha, hoy)) is not None
                and _texto(ficha.get("reforma_buscada")) == "si")

    def recuento(self, hoy):
        """Viaja en CADA respuesta, no solo en el manifiesto: un pack donde 22
        de 26 registros están sin vigencia comprobada tiene que verse así desde
        fuera, y tiene que verlo quien consume.

        Sin reloj legible no hay nada fresco que contar: `caducada` devuelve
        True y `_citable_en_si` False para todas, así que el recuento sale
        entero de las mismas dos funciones y no de un caso aparte (B10)."""
        caducados = sum(1 for f in self.fichas if caducada(f, hoy))
        citables = sum(1 for f in self.fichas if self._citable_en_si(f, hoy))
        sin_comprobar = sum(1 for f in self.fichas
                            if tipo_de(f) == "norma" and not self._citable_en_si(f, hoy))
        return {"registros": len(self.fichas), "citables_hoy": citables,
                "vigencia_no_comprobada": sin_comprobar, "caducados_hoy": caducados}

    def degradado(self, hoy):
        """Más de un tercio de los citables caducados: el pack lo dice en cada
        respuesta, citables incluidas."""
        r = self.recuento(hoy)
        return r["caducados_hoy"] * 3 > r["citables_hoy"]

    def cobertura(self, hoy):
        """Se calcula, no se declara. Una lista escrita una vez por versión
        sigue diciendo «yo cubro esta área» cuando dentro no queda una sola
        ficha viva: la más tranquilizadora de las respuestas negativas servida
        por un pack vacío.

        «Viva» quiere decir `_citable_en_si`, y no solo firmada y sin caducar.
        Un área cuyas fichas están todas sin vigencia comprobada, o todas en
        vigencia parcial —que nunca se sirve como citable, A18—, es un área en
        la que el pack no puede contestar nada: decir que la cubre es la misma
        promesa vacía por otro camino. Se paga un precio y queda dicho: para
        un identificador ausente en un área así, la respuesta baja de
        `NO_ESTA_EN_EL_PACK` a `FUERA_DE_COBERTURA`. Ninguna de las dos es
        citable, así que el precio es de precisión, no de seguridad.

        Y las materias se leen con `leer_materias`: una cadena no es una lista
        de materias (A10).

        Los otros dos ejes vienen ahora del pack y no de una constante escrita
        aquí dentro (B07). Los tres se publican y los tres se comparan: el eje
        que se publica sin compararse es una promesa que quien consume no
        puede usar, y peor, una que el manifiesto le enseña a escribir.
        """
        declaradas = set()
        for f in self.fichas:
            if self._citable_en_si(f, hoy):
                declaradas |= leer_materias(f.get("materia"))
        return {"jurisdiccion": self.jurisdiccion,
                "nivel_territorial": list(self.niveles_territoriales),
                "materias_declaradas": sorted(declaradas)}

    # ── responder ──

    def responder(self, consulta, hoy):
        # B10 — el reloj primero, y por la misma puerta que las casillas. Todo
        # lo que viene después cuenta días.
        dia = _reloj(hoy)
        if dia is None:
            # Los dos banderines van en el lado que no dice «sano»: es la
            # lección de B09 aplicada al caso en que no hay con qué medir.
            return RespuestaCompuesta(
                [Respuesta("NO_TENEMOS_INFORMACION_SUFICIENTE",
                           "el día en que se pregunta no es una fecha legible")],
                degradado=True, apagado=True)
        hoy = dia

        # B09 — el estado del pack se calcula ANTES del corte de R3 y viaja en
        # todas las respuestas, la incompleta incluida. `recuento` dice de sí
        # mismo que viaja en CADA respuesta, y `degradado`/`apagado` no son
        # huecos rellenables por defecto: son afirmaciones. Un pack apagado que
        # contestaba `apagado=False` a la primera consulta que hace cualquiera
        # —la que todavía no trae la fecha del caso— le decía a quien consume
        # que estaba sano. Un banderín de salud vale por lo que dice cuando
        # dice que sí.
        comunes = dict(cobertura=self.cobertura(hoy), recuento=self.recuento(hoy),
                       degradado=self.degradado(hoy), apagado=self.apagado(hoy))

        problema = _consulta_incompleta(consulta)
        if problema is not None:
            return RespuestaCompuesta([Respuesta("EL_PACK_NO_CONTESTA", problema)], **comunes)
        ejes = leer_consulta(consulta)

        # El pack apagado no responde afirmativamente ni siquiera con una ficha
        # impecable dentro: un pack sin mantenedor que solo responde identidad
        # reproduce el fallo original —identidad leída como vigencia— en el
        # peor momento posible.
        if comunes["apagado"]:
            return RespuestaCompuesta(
                [Respuesta("NO_TENEMOS_INFORMACION_SUFICIENTE",
                           "el pack está apagado: nadie lo mantiene; la identidad, si la hay, "
                           "es un dato no citable y esto no dice que rija")],
                **comunes)

        # A06 y B07 — los ejes de competencia se miran SIEMPRE, y no solo
        # cuando el pack no tiene la ficha. El pack cubre la jurisdicción y los
        # niveles que declara tenga o no tenga el registro que se le pide: que
        # lo tenga no lo vuelve competente. La jurisdicción callada se lee como
        # la propia, y ahí esta condición se aparta a sabiendas de `_materia`,
        # que trata el silencio como indeterminable: la materia la aporta la
        # carpeta del caso y varía consulta a consulta, mientras que preguntarle
        # a un pack sin decir jurisdicción es preguntarle en la suya. El coste
        # queda dicho: quien consulta el pack equivocado sin declarar
        # jurisdicción recibe una respuesta, y por eso el token registra el eje
        # tal como se pidió —callado— y no tal como se resolvió.
        if ejes["jurisdiccion"] is not None and ejes["jurisdiccion"] != self.jurisdiccion:
            return RespuestaCompuesta(
                [Respuesta("FUERA_DE_COBERTURA",
                           "la consulta declara otra jurisdicción que la del pack")], **comunes)
        if ejes["nivel_territorial"] not in self.niveles_territoriales:
            return RespuestaCompuesta(
                [Respuesta("FUERA_DE_COBERTURA",
                           "el nivel territorial de la consulta no está entre los que cubre "
                           "el pack")], **comunes)

        pedido = ejes["identificador"]
        coincidencias = [f for f in self.fichas if identificador_de(f) == pedido] if pedido else []
        if not coincidencias:
            return RespuestaCompuesta([self._sin_ficha(consulta, hoy)], **comunes)

        respuestas = [evaluar(f, consulta, hoy) for f in coincidencias]
        composicion = self._composicion(coincidencias, ejes)

        # A01 y A02, LA VÍA PRINCIPAL. El token se emitía por respuesta
        # individual, antes de calcular la composición y sin mirarla: en el
        # escenario de N4 el pack contestaba `CONFLICTO_ENTRE_FICHAS` y ponía
        # en la mano de quien consume un token que la prueba de banco aceptaba.
        # El token es lo único que sobrevive hasta la publicación: si el «no»
        # vive en la respuesta y el «sí» en el token, el «no» no existe. Y en
        # una respuesta múltiple deshacía la regla de N5 sin discutirla —el
        # consumidor se quedaba con la mejor coincidencia, que es justo la
        # lectura descartada—. Se emite si el conjunto es citable, o no se
        # emite: es la misma condición que `RespuestaCompuesta.citable`, y por
        # eso se escribe una vez y se comprueba aquí.
        if composicion is None and all(r.citable for r in respuestas):
            for r in respuestas:
                r.token = self._emitir_token(r, hoy, consulta)

        return RespuestaCompuesta(respuestas, codigo_de_composicion=composicion, **comunes)

    def _composicion(self, fichas, ejes):
        """N4 — dos fichas que discrepan en la vigencia es un problema de
        **vigencia**, y la prosa lo servía bajo `CONFLICTO_DE_FUENTES`, que
        está definido como un problema de identidad y cuya frase habla de dos
        fuentes oficiales. Es H8 al revés: se arregló una dirección y se creó
        la simétrica. Aquí tiene código propio, y el de identidad queda para lo
        que es.

        B03 — LA LLAVE ERA MÁS ESTRECHA QUE LA PREGUNTA QUE CONTESTA. Se
        agrupaba por `(identificador, alcance_comprobado)` comparado por
        igualdad exacta, y la pregunta no es esa: es si dos fichas que **cubren
        lo que se pide** discrepan. P2 empuja a estrechar, así que la forma
        normal del pack son varias fichas por norma con alcances distintos y
        solapados; dos que cubren el art. 00 —una comprobada solo para él, otra
        para él y el 01— y que dicen lo contrario sobre si la norma rige tenían
        llaves distintas, no había conflicto, las dos salían citables con su
        token cada una, y el consumidor elegía entre «vigente dentro del
        alcance comprobado» y «Hoy no rige» del mismo artículo. Eso es
        exactamente la lectura que N5 descartó, reaparecida por debajo.

        La llave es la petición. Solo entran las fichas cuyo alcance contiene
        lo que se pide: una ficha que no llega hasta ahí no contesta a esta
        consulta, y hacerla discrepar sería inventar un conflicto que nadie
        podría ver en la respuesta.
        """
        peticion = ejes["peticion"]
        por_identificador = {}
        for f in fichas:
            if not contenido_en(peticion, leer_alcance(f.get("alcance_comprobado"))):
                continue
            por_identificador.setdefault(identificador_de(f), set()).add(
                _texto(f.get("estado_vigencia")))
        for estados in por_identificador.values():
            if len(estados) > 1:
                return "CONFLICTO_ENTRE_FICHAS"
        return None

    def _sin_ficha(self, consulta, hoy):
        """La rama C. La materia la aporta quien consulta: inferirla de un
        identificador que el pack no tiene sería el modelo produciendo derecho
        por la puerta de la consulta.

        Ya no comprueba `territorial`: eso lo hace `responder` para todas las
        ramas. Dejarlo aquí además sería dejar escrita una condición que no se
        alcanza nunca, que es de dónde salía A18.
        """
        materia = _texto(consulta.get("materia"))
        if materia is None:
            return Respuesta("NO_TENEMOS_INFORMACION_SUFICIENTE",
                             "materia indeterminable: las dos lecturas están abiertas")
        if materia in self.cobertura(hoy)["materias_declaradas"]:
            return Respuesta("NO_ESTA_EN_EL_PACK", "materia cubierta, identificador ausente")
        return Respuesta("FUERA_DE_COBERTURA", "materia no cubierta por el pack")

    # ── R4: el token ──

    def _emitir_token(self, respuesta, hoy, consulta):
        """R4, más lo que le faltaba (V5).

        El formato de la prosa —código · identificador + alcance ·
        verificado_el · fecha_de_consulta— son cuatro campos que un modelo
        puede escribir de memoria, y la prueba de banco no incluía «token que
        no corresponde a ninguna ficha». Se le añaden dos cosas: la huella del
        pack, y una **serie opaca registrada al servir**. Un token que no está
        en el registro no se sirvió nunca, por plausible que se lea.

        B01 — Y LA CONSULTA ENTERA, que es el rediseño de esta ronda. La ronda
        anterior le metió dentro dos ejes de los cinco, la fecha del caso y su
        tipo (A03, A07), campo a campo y a mano. Los otros tres se quedaron
        fuera, y no por descuido sino porque no había ninguna pieza que dijera
        de qué se compone una consulta: `responder` sacaba las claves que
        necesitaba con `_texto` en cada rama, y el token hacía lo mismo con las
        suyas. Dos lecturas separadas se separan más con cada corrección.
        Ahora hay una: `leer_consulta` enumera los ejes en `EJES_DE_CONSULTA`,
        el registro guarda el resultado entero y la prueba de banco lo compara
        entero. Un eje nuevo entra en el token por añadirlo a esa tupla.

        Del digest y de por qué la consulta no viaja legible dentro del token:
        el token es una cadena partida por « · », y la consulta trae texto que
        escribe quien consulta. Meterla literal dejaría escribir campos falsos
        dentro del token con solo ponerlos en la materia. El digest identifica
        la consulta sin transportarla; lo que decide es siempre el registro.
        """
        f = respuesta.ficha
        tipo = tipo_de(f)
        # El alcance solo lo tiene una norma: leerlo en una providencia era
        # media vía A09 —un `alcance_comprobado` de más en una ficha de
        # jurisprudencia hacía que su token amparara un articulado—.
        alcance = leer_alcance(f.get("alcance_comprobado")) if tipo == "norma" else None
        proposicion = _texto(f.get("proposicion_atribuida")) if tipo == "providencia" else None
        parte_alcance = _serializar_alcance(alcance) if alcance else (proposicion or "")
        ejes = leer_consulta(consulta)
        serie = secrets.token_hex(8)
        token = " · ".join([respuesta.codigo,
                            identificador_de(f) + " + " + parte_alcance,
                            str(_fecha(f.get("verificado_el"))),
                            hoy.isoformat(),
                            # A03 y A07 — para qué caso se pidió, legible.
                            # Sin esto dos consultas con fechas de caso
                            # distintas producían el mismo token salvo la
                            # serie, y el tipo de fecha se validaba contra el
                            # vocabulario de `05` sin que ningún camino
                            # volviera a leerlo. Se queda a la vista porque es
                            # el eje que quien lee la cita necesita comprobar
                            # sin preguntarle al pack.
                            "caso:%s#%s" % (ejes["fecha_del_caso"].isoformat(),
                                            ejes["tipo_de_fecha"]),
                            # B01 — y los cinco ejes juntos, en una huella. Dos
                            # consultas que solo se distingan en la materia o
                            # en el nivel territorial ya no producen el mismo
                            # token.
                            "consulta:" + _huella_de_consulta(ejes),
                            self._huella(),
                            "serie:" + serie])
        # La entrada del registro es una FOTO, y no guarda la ficha: guarda lo
        # que se comprobó de ella el día en que se sirvió. La ficha es un dict
        # vivo, y A05 ensanchaba un token ya emitido ensanchando después el
        # `alcance_comprobado` de la ficha a la que el registro apuntaba —el
        # token seguía exhibiendo el alcance estrecho y amparaba el ancho—.
        # Sin puntero no hay nada que ensanchar por detrás: la caducidad
        # también se calcula aquí, una vez, y es la de la firma que se sirvió.
        self.registro[serie] = {"token": token, "codigo": respuesta.codigo,
                                "tipo": tipo, "alcance": alcance,
                                "proposicion": proposicion, "consulta": ejes,
                                "huella": self._huella(),
                                "revisar_antes_de": revisar_antes_de(f),
                                "servido_el": hoy}
        return token

    def verificar_token(self, token, lo_citado, hoy, caso):
        """La prueba de banco, hecha mecánica. `(pasa, motivo)`.

        Diez condiciones de fallo. Las cinco de la primera ronda —cita sin
        token; token que no resuelve contra ninguna respuesta servida, o sea
        el inventado; código que no es de los cuatro citables; ficha caducada
        hoy; alcance del token que no contiene lo citado—, tres que la segunda
        ronda obligó a añadir y dos de esta:

          - **el pack vivo** (B02). Ni `apagado` ni `degradado` se consultaban
            aquí en ninguna línea, y el apagado no necesita que nadie toque el
            pack: bascula solo con el calendario, o sea sin mover la huella que
            A04 sí comprueba. Dos meses después, el mismo pack contestaba
            `NO_TENEMOS_INFORMACION_SUFICIENTE` a todo el mundo y seguía
            respaldando la cita que había salido de él. Era el argumento de
            A01 —«si el no vive en la respuesta y el sí en el token, el no no
            existe»— un piso más arriba. El pack que no responde tampoco
            respalda.

            Convive con A05 sin contradecirlo, y la línea entre los dos hay
            que decirla: de la FICHA se lee la foto del día en que se sirvió,
            para que ensancharla después no ensanche el token; del PACK se lee
            el estado de hoy, porque la pregunta que contesta la prueba de
            banco es si esta cita se sostiene ahora.
          - **la consulta entera** (B01). El registro guardaba dos ejes de los
            cinco, así que un token pedido en la materia buena respaldaba una
            cita que declaraba la materia ajena —la misma que `responder`
            acababa de negar con `FUERA_DEL_ALCANCE_COMPROBADO`—. Se comparan
            todos los de `EJES_DE_CONSULTA`, y el motivo dice cuál falló.

          - **la huella del pack** (A04). `version` + `checksum` se escribían
            dentro del token «porque sin ellos no hay a qué resolver un token»
            y después no se comparaban con nada: el registro sobrevivía a que
            la ficha saliera del pack y a que la ficha se retractara entera
            —identidad, vigencia y reforma—, y el token seguía pasando.
          - **el caso** (A03, A07). El token no registraba para qué caso se
            emitió y esta función no tenía dónde recibirlo, así que un token
            obtenido para un caso de dentro de la ventana amparaba
            literalmente una cita en un caso de fuera. `caso` es obligatorio y
            es la consulta: quien cita tiene que decir para qué cita.
          - **la foto, no el puntero** (A05). El alcance, la proposición y la
            caducidad se leían de la ficha **viva**, no de lo que el token
            registró: ensanchar la ficha después ensanchaba un token ya
            emitido, que seguía exhibiendo el alcance estrecho. El registro ya
            no guarda la ficha, así que no hay nada que ensanchar por detrás.

        `lo_citado` llega **estructurado**, igual que la petición. La prosa
        pedía comprobar «lo que la entrega cita», que exige parsear prosa, que
        es justo lo que el propio documento declara imposible. Exigir la
        estructura es lo que devuelve esta condición al terreno mecánico.
        """
        dia = _reloj(hoy)
        if dia is None:
            return (False, "el día en que se comprueba la cita no es una fecha legible")
        hoy = dia
        t = _texto(token)
        if t is None:
            return (False, "cita sin token")
        marca = [p for p in t.split(" · ") if p.startswith("serie:")]
        if not marca:
            return (False, "el token no lleva serie: no lo emitió este pack")
        entrada = self.registro.get(marca[0][len("serie:"):])
        if entrada is None or entrada["token"] != t:
            return (False, "el token no corresponde a ninguna respuesta servida")
        if entrada["codigo"] not in CODIGOS_CITABLES:
            return (False, "el código del token no es uno de los cuatro citables")
        # La huella va antes que el estado del pack, y el orden importa: si el
        # pack ya no es el mismo, decir que está apagado sería contestar por
        # otro. Primero se comprueba de qué pack habla el token.
        if entrada["huella"] != self._huella():
            return (False, "el token se emitió contra otra versión del pack")
        if self.apagado(hoy):
            return (False, "el pack está apagado: hoy no responde, y lo que no responde "
                           "tampoco respalda")
        limite = entrada["revisar_antes_de"]
        if limite is None or hoy > limite:
            return (False, "el token apunta a una ficha caducada")
        if not isinstance(caso, dict):
            return (False, "la prueba de banco necesita el caso para el que se cita")
        declarada = leer_consulta(caso)
        for eje in EJES_DE_CONSULTA:
            if declarada[eje] != entrada["consulta"][eje]:
                return (False, "el token se emitió para otra consulta: no coincide `%s`" % eje)
        if entrada["tipo"] == "providencia":
            if _texto(lo_citado) != entrada["proposicion"]:
                return (False, "lo citado no es la proposición para la que se comprobó")
        elif not contenido_en(leer_alcance(lo_citado), entrada["alcance"]):
            return (False, "el alcance del token no contiene lo que se cita")
        return (True, "el token resuelve contra una respuesta servida")


def _serializar_alcance(alcance):
    completa, articulos, incisos = alcance
    return "{norma_completa: %s, articulos: [%s], incisos: [%s]}" % (
        "si" if completa else "no", ", ".join(sorted(articulos)), ", ".join(sorted(incisos)))


def _huella_de_consulta(ejes):
    """La huella de una consulta leída. Dos consultas distintas en cualquiera
    de sus ejes dan huellas distintas, y por eso dan tokens distintos (B01).

    Se recorre `EJES_DE_CONSULTA` y no las claves del diccionario: el orden
    fijo es lo que hace que la huella sea la misma cada vez, y recorrer la
    tupla es lo que hace que añadir un eje allí baste para que entre aquí.
    """
    partes = []
    for eje in EJES_DE_CONSULTA:
        valor = ejes[eje]
        if eje == "peticion":
            valor = _serializar_alcance(valor) if valor is not None else None
        elif isinstance(valor, date):
            valor = valor.isoformat()
        partes.append("%s=%s" % (eje, "" if valor is None else valor))
    crudo = "; ".join(partes)
    return hashlib.sha256(crudo.encode("utf-8")).hexdigest()[:16]
