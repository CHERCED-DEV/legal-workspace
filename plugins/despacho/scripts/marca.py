# -*- coding: utf-8 -*-
"""Reconocer la marca ` - REVISADO` en el nombre de un archivo. Una sola vez.

**Esta es la regla más consecuente del producto**: es el único mecanismo por el
que la autoridad cambia de manos. Un archivo marcado son hechos que ella miró
ficha por ficha; uno sin marcar es una propuesta que nadie ha visto. Seis
`SKILL.md` la enuncian en prosa, con una redaccion identica en los seis.

**Y hasta el 2026-09-07 su unica implementacion vivia dentro de una prueba**
(`evals/scripts/test_marca_revisado.py`). En cuanto un segundo programa la
necesito -- el contador, para no pedirle un conteo a un archivo que es de ella
y no del sistema -- habria habido dos copias, y este repositorio ya sabe lo que
pasa entonces: *una regla con dos redacciones se parte*. Asi que vive aqui, y
la prueba comprueba ESTA contra los casos que la prosa enumera.

La prosa que manda, literal:

    «se mira el nombre sin la extension -- sin las dos, si quedaron dos -- y
     cuenta si termina en REVISADO, en mayusculas o minusculas, con guion o
     sin el»
"""
import unicodedata
from pathlib import Path

# Las que Windows oculta y que ella puede acabar arrastrando sin verlas.
EXTENSIONES = {".md", ".txt", ".docx", ".doc", ".rtf"}


def plano(s):
    d = unicodedata.normalize("NFD", s)
    return "".join(c for c in d if unicodedata.category(c) != "Mn").upper()


def sin_extensiones(nombre):
    """«quitada la extension, o las dos si quedaron dos, o ninguna si no tiene»."""
    p = Path(nombre)
    for _ in range(2):
        if p.suffix.lower() in EXTENSIONES:
            p = p.with_suffix("")
        else:
            break
    return p.name


def esta_marcado(nombre):
    """«termina en REVISADO, en mayusculas o minusculas, con el guion o sin el»."""
    return plano(sin_extensiones(nombre)).rstrip().endswith("REVISADO")


def casi_marcado(nombre):
    """«la raiz "revis"... sin cerrar el nombre: se nombra y se pregunta».

    La raiz y no la palabra: «revisar» NO contiene «revisado», asi que quien
    buscara la palabra pasaria por encima de `(revisar)` -- el ejemplo de la
    propia regla -- sin verlo.
    """
    return not esta_marcado(nombre) and "REVIS" in plano(nombre)
