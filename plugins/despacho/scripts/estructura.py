# -*- coding: utf-8 -*-
"""estructura — la forma de un proyecto (ADR-023), en un solo sitio.

Cada programa que deja algo en el proyecto toma de aqui la carpeta, en vez de
pedir un --destino libre: con destinos libres cada proyecto acabo teniendo su
propia manera de guardar las cosas (seis maneras de guardar una version, tres
carpetas «vigente» a la vez; inventario del 2026-09-23).

La pagina «oir y marcar» tiene la misma forma en tools/pagina-despacho/src/
guardado.js (EN_PROYECTO): si cambia una, cambia la otra.
"""
import os
import re

ESTADO = "0-Estado del caso (no editar).txt"
RECIBIDOS = "1-Documentos recibidos"      # plana; ningun programa escribe aqui
BORRADORES = "2-Borradores"
PRESENTAR = "3-Para presentar"            # solo lo que ELLA decide presentar
RAIZ_DEL_PROYECTO = (ESTADO, RECIBIDOS, BORRADORES, PRESENTAR)

TRANSCRIPCIONES = BORRADORES + "/Transcripciones"
RESUMENES = BORRADORES + "/Resumenes"
ACTAS = BORRADORES + "/Actas"
COMPROMISOS = BORRADORES + "/Compromisos"
VOCES = BORRADORES + "/Voces"
GLOSARIO = BORRADORES + "/Glosario"
ENTREGAS = BORRADORES + "/Entregas"
FUENTES_DE_LA_ENTREGA = ENTREGAS + "/_fuentes (no enviar)"
ENTREGAS_ANTERIORES = ENTREGAS + "/_anteriores"
LO_QUE_DECLARE = BORRADORES + "/Lo que declaré"          # lo escribe la pagina
LO_QUE_DECLARO_ELLA = BORRADORES + "/Lo que declaró ella"  # lo escribe recoger_lo_declarado
ANTERIORES = BORRADORES + "/_anteriores"
INTERMEDIOS = BORRADORES + "/_intermedios (se puede borrar)"

# A nivel de cliente u oficina, al lado de los proyectos.
PAPELERIA = "Papelería de la oficina"

FECHA = re.compile(r"(\d{4}-\d{2}-\d{2})")


def version(fecha, que=""):
    """Nombre de la carpeta de una version: «AAAA-MM-DD - que cambio»."""
    return fecha + (" - " + que.strip() if que and que.strip() else "")


def es_proyecto(ruta):
    """Una carpeta es un proyecto si tiene las carpetas de trabajo."""
    return all(os.path.isdir(os.path.join(ruta, n)) for n in (RECIBIDOS, BORRADORES))


def proyecto_de(ruta):
    """El proyecto que contiene `ruta` (o None): sube hasta encontrarlo."""
    r = os.path.abspath(ruta)
    while True:
        if es_proyecto(r):
            return r
        padre = os.path.dirname(r)
        if padre == r:
            return None
        r = padre


def en(proyecto, relativa):
    return os.path.join(proyecto, *relativa.split("/"))
