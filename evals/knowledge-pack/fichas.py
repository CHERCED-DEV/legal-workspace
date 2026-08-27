# -*- coding: utf-8 -*-
"""
Fichas y consultas de ejemplo para los tests del contrato.

**Aquí no hay derecho.** Ni una norma, ni una fecha de vigencia, ni un estado
jurídico reales: `LEY-0000-0000`, `art. 00`, `J-XX-0000-0000` y un año 1000
que ninguna norma colombiana puede tener. Si en este archivo apareciera un
dato jurídico verdadero, el instrumento quedaría anulado —sería el modelo
llenando una casilla, que es exactamente lo que existe para impedir—.

POR QUÉ HAY UNA FICHA PERFECTA. Todos los tests parten de `ficha_norma()` o
`ficha_providencia()` y le rompen **una** cosa. Así un test que falla señala
la condición exacta que se cayó, y —lo que importa más— un contrato que
dijera que no a todo no pasaría la suite: el control positivo lo cazaría.
"""

from datetime import date

from contrato import mas_meses

# Un ancla fija para toda la aritmética. Año 1000 a propósito: no se puede
# confundir con la fecha de vigencia de nada, y la aritmética de meses
# funciona igual que en cualquier otro año.
HOY = date(1000, 6, 15)


def meses(n):
    """El ancla desplazada n meses, en el formato `AAAA-MM-DD` de la ficha.
    Negativo es pasado. Toda fecha de estos ejemplos se escribe así, para que
    se vea de un vistazo a qué distancia de `HOY` cae cada una."""
    return mas_meses(HOY, n).isoformat()


FIRMANTE = "Nombre Apellido de Ejemplo"


def ficha_norma(**cambios):
    """La ficha de norma que SÍ es citable, con los doce campos de `01` §2 más
    `reforma_buscada` y `tipo`. `nota_de_vigencia` va vacía a propósito: es la
    fila 1 de la tabla de cadencias —«sin nada pendiente en la nota»— y el
    único estado en que la nota no es obligatoria."""
    f = {
        "tipo": "norma",
        "identificador_canonico": "LEY-0000-0000",
        "alcance_comprobado": {"norma_completa": "no", "articulos": ["00"], "incisos": []},
        "materia": ["area-de-ejemplo"],
        "estado_identidad": "IDENTIDAD_VERIFICADA",
        "fuente_identidad": {"clase": "PRIMARY_OFFICIAL",
                             "referencia": "https://ejemplo.invalido/publicacion-oficial",
                             "consultada": meses(-1)},
        "estado_vigencia": "VIGENTE_AL " + meses(-1),
        "vigencia_desde": meses(-60),
        "fuente_vigencia": {"clase": "PRIMARY_OFFICIAL",
                            "referencia": "https://ejemplo.invalido/diario-oficial",
                            "consultada": meses(-1)},
        "nota_de_vigencia": "",
        "reforma_buscada": "si",
        "verificado_por": FIRMANTE,
        "verificado_el": meses(-1),
        "acortamiento_manual": None,
    }
    f.update(cambios)
    return f


def ficha_providencia(**cambios):
    """La ficha de providencia que SÍ es citable: los nueve campos de `01` §4,
    más `materia` —sin ella el pack sirve un precedente en un área que él mismo
    declara excluida— y `tipo`."""
    f = {
        "tipo": "providencia",
        "identificador": "J-XX-0000-0000",
        "materia": ["area-de-ejemplo"],
        "estado_identidad": "IDENTIDAD_VERIFICADA",
        "fuente_identidad": {"clase": "OFFICIAL_JURISPRUDENCE",
                             "referencia": "https://ejemplo.invalido/relatoria",
                             "consultada": meses(-1)},
        "proposicion_atribuida": "proposicion de ejemplo numero 00",
        "pasaje": "parrafo 00",
        "estado_uso": "PROFESSIONALLY_CONFIRMED",
        "busqueda_adversa": "buscada " + meses(-1) + " en relatoria de ejemplo, criterio «tema 00»; no apareció autoridad posterior en contra",
        "verificado_por": FIRMANTE,
        "verificado_el": meses(-1),
        "acortamiento_manual": None,
    }
    f.update(cambios)
    return f


def consulta_norma(**cambios):
    """La consulta que acompaña a la ficha perfecta. `peticion` llega tipada
    con la misma estructura que `alcance_comprobado` y la aporta quien
    consulta: si la produjera el modelo traduciendo prosa, el operando
    izquierdo de la única comparación que cierra V1 lo escribiría el
    intérprete generoso."""
    c = {
        "identificador": "LEY-0000-0000",
        "peticion": {"norma_completa": "no", "articulos": ["00"], "incisos": []},
        "fecha_del_caso": meses(-2),
        "tipo_de_fecha": "procedural_start_date",
        "materia": "area-de-ejemplo",
    }
    c.update(cambios)
    return c


def consulta_providencia(**cambios):
    c = {
        "identificador": "J-XX-0000-0000",
        "proposicion": "proposicion de ejemplo numero 00",
        "fecha_del_caso": meses(-2),
        "tipo_de_fecha": "case_relevant_date",
        "materia": "area-de-ejemplo",
    }
    c.update(cambios)
    return c


def sin(ficha, *campos):
    """La ficha a la que le falta un campo entero, que no es lo mismo que
    tenerlo vacío: las dos formas del agujero se prueban por separado."""
    copia = dict(ficha)
    for campo in campos:
        copia.pop(campo, None)
    return copia
