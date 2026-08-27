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
    "CONFLICTO_ENTRE_FICHAS": "Dos fichas del mismo alcance de {id} discrepan en la vigencia comprobada. Es un problema de vigencia, no de identidad, y el pack no elige.",
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
    """`AAAA-MM-DD` estricto → date. Cualquier otra cosa → None.

    Estricto significa estricto: `2 de enero`, `AAAA-MM-DD`, `1000-13-01` y
    una cadena vacía valen lo mismo, que es nada. Una fecha que no se puede
    leer no puede compararse, y lo que no se puede comparar cae fuera.
    """
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    v = _texto(valor)
    if v is None:
        return None
    try:
        return datetime.strptime(v, "%Y-%m-%d").date()
    except ValueError:
        return None


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


def _apunta_al_corpus(referencia):
    """¿La referencia es un archivo de este proyecto?

    `01` §5 regla 3 y `04` §7: mover una afirmación de un archivo del corpus a
    una ficha no la comprueba. Es el mecanismo exacto de N1 — el renombrado
    deja escrita la cadena `IDENTIDAD_VERIFICADA` en el catálogo, al lado de
    cada norma, en un campo marcado copiable — y también el de la cuarentena
    de P0.b. La comprobación es deliberadamente burda: rechazar de más cuesta
    rehacer una ficha; aceptar de más cuesta una cita fabricada.
    """
    r = referencia.lower()
    return (".md" in r or "source-catalog" in r or "knowledge-pack" in r
            or "skills-support" in r or "legal-workspace" in r
            or r.startswith("docs/") or r.startswith("./") or r.startswith("../"))


def leer_fuente(valor, clases_admitidas):
    """`{clase, referencia, consultada}` → la clase, o None si la fuente no
    sirve para lo que se le pide.

    Tipada y aparte, nunca la clase escrita dentro de la cadena de la URL:
    una cadena que contiene las letras `PRIMARY_OFFICIAL` no es una fuente
    primaria, y esa confusión era media vía V3.
    """
    if not isinstance(valor, dict) or set(valor) != {"clase", "referencia", "consultada"}:
        return None
    clase = _texto(valor["clase"])
    referencia = _texto(valor["referencia"])
    if clase not in CLASES_DE_FUENTE or clase not in clases_admitidas:
        return None
    if referencia is None or _apunta_al_corpus(referencia):
        return None
    if _fecha(valor["consultada"]) is None:
        return None
    return clase


# ───────────────────── §C. La cuenta de la caducidad ─────────────────────

CADENCIA_MESES = 12                  # `02` §6, fila 1. Política operativa, no derecho.
CADENCIA_CORTA_MESES = 3             # `02` §6, fila 3.
CADENCIA_PROVIDENCIA_MESES = 12      # N3: la tabla de cadencias no tenía fila para ellas.


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
    """
    if ficha.get("tipo") == "providencia":
        return CADENCIA_PROVIDENCIA_MESES
    return CADENCIA_CORTA_MESES if _texto(ficha.get("nota_de_vigencia")) else CADENCIA_MESES


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
    defecto de no hacer nada: nadie tiene que leer un aviso."""
    limite = revisar_antes_de(ficha)
    return limite is None or hoy > limite


# ───────────────────────── §D. La respuesta ─────────────────────────

class Respuesta(object):
    """Un código, un motivo técnico, la frase que lee ella y —si es citable—
    su token. `nota` viaja transcrita literal, sin interpretar, en toda
    respuesta que hable de una ficha con nota."""

    def __init__(self, codigo, motivo, ficha=None, nota=None):
        self.codigo = codigo
        self.motivo = motivo
        self.ficha = ficha
        self.nota = nota
        self.token = None            # lo estampa el pack: solo él tiene el registro
        self.identificador = identificador_de(ficha) if ficha is not None else ""
        self.frase = FRASES.get(codigo, "").format(id=self.identificador or "la ficha")

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
    """
    if not isinstance(consulta, dict):
        return "la consulta no es una consulta"
    if _fecha(consulta.get("fecha_del_caso")) is None:
        return "falta `fecha_del_caso` o no es una fecha legible"
    if _texto(consulta.get("tipo_de_fecha")) not in TIPOS_DE_FECHA:
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


def _identidad(ficha, hoy, clases_admitidas):
    """A.2 / B.2. Devuelve None si la identidad pasa, o la Respuesta que la
    frena. Un fallo de identidad nunca se sirve bajo un código de vigencia.
    """
    estado = _texto(ficha.get("estado_identidad"))
    if estado == CONFLICTO_DE_FUENTES:
        return Respuesta(CONFLICTO_DE_FUENTES, "dos fuentes oficiales discrepan; el pack no elige", ficha)
    if estado != IDENTIDAD_VERIFICADA:
        return Respuesta(IDENTIDAD_POR_VERIFICAR, "estado_identidad no es IDENTIDAD_VERIFICADA", ficha)
    if leer_fuente(ficha.get("fuente_identidad"), clases_admitidas) is None:
        return Respuesta(IDENTIDAD_POR_VERIFICAR,
                         "fuente_identidad vacía, de clase inadmisible o apuntando al corpus", ficha)
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

    # A.3 — contención de alcance en las DOS direcciones (V1). El operando
    # izquierdo llega tipado desde la consulta y nunca lo produce el modelo:
    # una `peticion` en prosa no es comparable, y no comparable cae fuera.
    if not contenido_en(leer_alcance(consulta.get("peticion")), leer_alcance(ficha.get("alcance_comprobado"))):
        return Respuesta("FUERA_DEL_ALCANCE_COMPROBADO",
                         "la petición no está contenida en alcance_comprobado, o no son comparables", ficha, nota)

    # A.4 — estado de vigencia, leído como lista blanca.
    estado, fecha_estado = leer_estado_vigencia(ficha.get("estado_vigencia"))
    if estado == VIGENCIA_PARCIAL_AL:
        return Respuesta("VIGENCIA_PARCIAL", "rige en parte; nunca se sirve como citable", ficha, nota)
    if estado not in ESTADOS_QUE_PUEDEN_SER_CITABLES:
        return Respuesta(VIGENCIA_NO_COMPROBADA,
                         "estado_vigencia vacío o no reconocido", ficha, nota)

    # Casilla obligatoria vacía. La nota lo es en dos estados, y sin ella
    # `CITABLE_CON_REFORMA` sale afirmando una reforma de la que no dice nada.
    if estado in ESTADOS_QUE_OBLIGAN_NOTA and nota is None:
        return Respuesta("FICHA_INCOMPLETA", "el estado obliga a nota_de_vigencia y está vacía", ficha)

    # A.5 — la fuente de la vigencia, tipada y de clase primaria.
    if leer_fuente(ficha.get("fuente_vigencia"), CLASES_DE_VIGENCIA) is None:
        return Respuesta(VIGENCIA_NO_COMPROBADA,
                         "fuente_vigencia vacía, de clase distinta de PRIMARY_OFFICIAL o apuntando al corpus",
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

    codigo = {VIGENTE_AL: "CITABLE",
              VIGENTE_CON_REFORMA_AL: "CITABLE_CON_REFORMA",
              SIN_VIGENCIA_DESDE: "CITABLE_SIN_VIGENCIA_HOY"}[estado]
    return Respuesta(codigo, "cumple las nueve condiciones", ficha, nota)


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

    # B.5 — la proposición, literal. Sin normalizar de ninguna forma: la
    # unidad no es la providencia, es el par providencia + proposición, y
    # cualquier tolerancia aquí la elige el intérprete generoso.
    pedida = _texto(consulta.get("proposicion"))
    if pedida is None or pedida != _texto(ficha.get("proposicion_atribuida")):
        return Respuesta("FUERA_DEL_ALCANCE_COMPROBADO",
                         "se comprobó para la proposición atribuida, no para la que se pide", ficha)

    return Respuesta("CITABLE_PRECEDENTE", "cumple las seis condiciones", ficha)


def evaluar(ficha, consulta, hoy):
    """Una ficha, una consulta, una respuesta. El corazón del contrato.

    El tipo se **declara**, no se deduce de qué campos tiene la ficha.
    Deducirlo es exactamente V4: la providencia recorría la tabla de las
    normas y salía citable precisamente porque no tenía sus campos, y lo único
    que la atrapaba era un desajuste de cadena que el renombrado iba a borrar.
    """
    problema = _consulta_incompleta(consulta)
    if problema is not None:
        return Respuesta("EL_PACK_NO_CONTESTA", problema, ficha if isinstance(ficha, dict) else None)
    if not isinstance(ficha, dict):
        return Respuesta("NO_TENEMOS_INFORMACION_SUFICIENTE", "eso no es una ficha")
    tipo = _texto(ficha.get("tipo"))
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

    def __repr__(self):
        return "RespuestaCompuesta(%s, citable=%s)" % (self.codigos, self.citable)


class Pack(object):
    """El pack: sus fichas, su cobertura calculada, su reloj y su registro de
    respuestas servidas.

    El pack no almacena estados: almacena afirmaciones fechadas y el estado se
    calcula al leer. Consecuencia buscada: si nadie lo mantiene, se apaga solo.
    """

    def __init__(self, fichas, curator="", version="0.0.0"):
        self.fichas = list(fichas)
        self.curator = curator
        self.version = version
        self.registro = {}   # serie -> token servido. Sin esto no hay a qué
                             # resolver un token, y un token inventado pasa.

    # ── el reloj del pack ──

    def checksum(self):
        """Huella de las fichas. El manifiesto de `boundaries.md` la exige y
        sin ella un token no se puede resolver contra una versión del pack."""
        crudo = json.dumps(self.fichas, sort_keys=True, default=str, ensure_ascii=False)
        return hashlib.sha256(crudo.encode("utf-8")).hexdigest()[:16]

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
        """
        firmas = [f for f in (_fecha(x.get("verificado_el")) for x in self.fichas) if f]
        if not firmas:
            return True
        mediana = date.fromordinal(int(statistics.median([f.toordinal() for f in firmas])))
        return hoy > mas_meses(mediana, MESES_DE_APAGADO)

    def _citable_en_si(self, ficha, hoy):
        """Si la ficha pasa las condiciones que no dependen de la consulta.
        Es lo único contable sin una consulta delante, y así se dice."""
        if _firma_valida(ficha, hoy) is None or caducada(ficha, hoy):
            return False
        if ficha.get("tipo") == "providencia":
            return _evaluar_providencia(ficha, {"proposicion": ficha.get("proposicion_atribuida"),
                                                "fecha_del_caso": hoy.isoformat(),
                                                "tipo_de_fecha": "case_relevant_date"},
                                        hoy).citable
        estado, _ = leer_estado_vigencia(ficha.get("estado_vigencia"))
        return (estado in ESTADOS_QUE_PUEDEN_SER_CITABLES
                and _identidad(ficha, hoy, CLASES_DE_IDENTIDAD_NORMA) is None
                and leer_fuente(ficha.get("fuente_vigencia"), CLASES_DE_VIGENCIA) is not None
                and _texto(ficha.get("reforma_buscada")) == "si")

    def recuento(self, hoy):
        """Viaja en CADA respuesta, no solo en el manifiesto: un pack donde 22
        de 26 registros están sin vigencia comprobada tiene que verse así desde
        fuera, y tiene que verlo quien consume."""
        caducados = sum(1 for f in self.fichas if caducada(f, hoy))
        citables = sum(1 for f in self.fichas if self._citable_en_si(f, hoy))
        sin_comprobar = sum(1 for f in self.fichas
                            if f.get("tipo") == "norma" and not self._citable_en_si(f, hoy))
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
        por un pack vacío."""
        declaradas = set()
        for f in self.fichas:
            if caducada(f, hoy) or _firma_valida(f, hoy) is None:
                continue
            for m in (f.get("materia") or []):
                if _texto(m):
                    declaradas.add(_texto(m))
        return {"jurisdiccion": "colombia", "nivel_territorial": ["nacional"],
                "materias_declaradas": sorted(declaradas)}

    # ── responder ──

    def responder(self, consulta, hoy):
        problema = _consulta_incompleta(consulta)
        if problema is not None:
            return RespuestaCompuesta([Respuesta("EL_PACK_NO_CONTESTA", problema)])

        comunes = dict(cobertura=self.cobertura(hoy), recuento=self.recuento(hoy),
                       degradado=self.degradado(hoy))

        # El pack apagado no responde afirmativamente ni siquiera con una ficha
        # impecable dentro: un pack sin mantenedor que solo responde identidad
        # reproduce el fallo original —identidad leída como vigencia— en el
        # peor momento posible.
        if self.apagado(hoy):
            return RespuestaCompuesta(
                [Respuesta("NO_TENEMOS_INFORMACION_SUFICIENTE",
                           "el pack está apagado: nadie lo mantiene; la identidad, si la hay, "
                           "es un dato no citable y esto no dice que rija")],
                apagado=True, **comunes)

        pedido = _texto(consulta.get("identificador"))
        coincidencias = [f for f in self.fichas if identificador_de(f) == pedido] if pedido else []
        if not coincidencias:
            return RespuestaCompuesta([self._sin_ficha(consulta, hoy)], **comunes)

        respuestas = [evaluar(f, consulta, hoy) for f in coincidencias]
        for r in respuestas:
            if r.citable:
                r.token = self._emitir_token(r, hoy, consulta)

        return RespuestaCompuesta(respuestas,
                                  codigo_de_composicion=self._composicion(coincidencias, respuestas),
                                  **comunes)

    def _composicion(self, fichas, respuestas):
        """N4 — dos fichas del mismo par (identificador, alcance) que discrepan
        en la vigencia es un problema de **vigencia**, y la prosa lo servía
        bajo `CONFLICTO_DE_FUENTES`, que está definido como un problema de
        identidad y cuya frase habla de dos fuentes oficiales. Es H8 al revés:
        se arregló una dirección y se creó la simétrica. Aquí tiene código
        propio, y el de identidad queda para lo que es."""
        por_clave = {}
        for f in fichas:
            alcance = leer_alcance(f.get("alcance_comprobado"))
            clave = (identificador_de(f), alcance)
            por_clave.setdefault(clave, set()).add(_texto(f.get("estado_vigencia")))
        for estados in por_clave.values():
            if len(estados) > 1:
                return "CONFLICTO_ENTRE_FICHAS"
        return None

    def _sin_ficha(self, consulta, hoy):
        """La rama C. La materia la aporta quien consulta: inferirla de un
        identificador que el pack no tiene sería el modelo produciendo derecho
        por la puerta de la consulta."""
        if consulta.get("territorial"):
            return Respuesta("FUERA_DE_COBERTURA", "consulta territorial; el pack es nacional")
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
        """
        f = respuesta.ficha
        alcance = leer_alcance(f.get("alcance_comprobado"))
        parte_alcance = (_serializar_alcance(alcance) if alcance
                         else _texto(f.get("proposicion_atribuida")) or "")
        serie = secrets.token_hex(8)
        token = " · ".join([respuesta.codigo,
                            identificador_de(f) + " + " + parte_alcance,
                            str(_fecha(f.get("verificado_el"))),
                            hoy.isoformat(),
                            "pack:%s@%s" % (self.version, self.checksum()),
                            "serie:" + serie])
        self.registro[serie] = {"token": token, "codigo": respuesta.codigo,
                                "ficha": f, "servido_el": hoy}
        return token

    def verificar_token(self, token, lo_citado, hoy):
        """La prueba de banco, hecha mecánica. `(pasa, motivo)`.

        Cinco condiciones de fallo, y la quinta es la que faltaba: cita sin
        token; token que no resuelve contra ninguna respuesta servida —el
        inventado—; código que no es de los cuatro citables; ficha caducada
        hoy; y alcance del token que no contiene lo citado.

        `lo_citado` llega **estructurado**, igual que la petición. La prosa
        pedía comprobar «lo que la entrega cita», que exige parsear prosa, que
        es justo lo que el propio documento declara imposible. Exigir la
        estructura es lo que devuelve esta condición al terreno mecánico.
        """
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
        if caducada(entrada["ficha"], hoy):
            return (False, "el token apunta a una ficha caducada")
        ficha = entrada["ficha"]
        if ficha.get("tipo") == "providencia":
            if _texto(lo_citado) != _texto(ficha.get("proposicion_atribuida")):
                return (False, "lo citado no es la proposición para la que se comprobó")
        elif not contenido_en(leer_alcance(lo_citado), leer_alcance(ficha.get("alcance_comprobado"))):
            return (False, "el alcance del token no contiene lo que se cita")
        return (True, "el token resuelve contra una respuesta servida")


def _serializar_alcance(alcance):
    completa, articulos, incisos = alcance
    return "{norma_completa: %s, articulos: [%s], incisos: [%s]}" % (
        "si" if completa else "no", ", ".join(sorted(articulos)), ", ".join(sorted(incisos)))
